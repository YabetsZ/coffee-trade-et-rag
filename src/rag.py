from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer

from .config import EMBEDDING_MODEL, GENERATION_MODEL, MAX_NEW_TOKENS, TOP_K
from .index import load_index


class RAGSystem:
    def __init__(self) -> None:
        self.index, self.metadata = load_index()
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.tokenizer = AutoTokenizer.from_pretrained(GENERATION_MODEL)
        self.is_causal = True
        try:
            self.generator = AutoModelForCausalLM.from_pretrained(
                GENERATION_MODEL,
                device_map="auto",
            )
        except Exception:
            self.is_causal = False
            self.generator = AutoModelForSeq2SeqLM.from_pretrained(GENERATION_MODEL)

    def retrieve(self, query: str, top_k: int = TOP_K) -> List[dict]:
        query_embedding = self.embedder.encode(
            [f"query: {query}"],
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype("float32")

        scores, indices = self.index.search(query_embedding, top_k)
        results: List[dict] = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            item = dict(self.metadata[idx])
            item["score"] = float(score)
            results.append(item)

        return results

    def build_prompt(self, query: str, contexts: List[dict]) -> str:
        context_text = "\n\n".join(
            [
                f"[ምንጭ {i + 1}] {ctx['text']}"
                for i, ctx in enumerate(contexts)
            ]
        )
        user_content = (
            f"መረጃ (Context): {context_text}\n\n"
            f"ጥያቄ (Question): {query}\n\n"
            "እባክህ ከላይ ባለው መረጃ መሰረት ብቻ መልስ ስጥ። "
            "መልሱ አጭር እና ግልጽ ይሁን።"
        )

        if hasattr(self.tokenizer, "apply_chat_template") and self.is_causal:
            messages = [{"role": "user", "content": user_content}]
            return self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )

        return (
            "<start_of_turn>user\n"
            f"{user_content}<end_of_turn>\n"
            "<start_of_turn>model\n"
        )

    def generate(self, query: str, top_k: int = TOP_K) -> Tuple[str, List[dict]]:
        contexts = self.retrieve(query, top_k=top_k)
        prompt = self.build_prompt(query, contexts)

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)

        if self.is_causal:
            inputs = {k: v.to(self.generator.device) for k, v in inputs.items()}
            output_ids = self.generator.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            input_len = inputs["input_ids"].shape[1]
            answer_tokens = output_ids[0][input_len:]
            answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)
        else:
            output_ids = self.generator.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
            )
            answer = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return answer.strip(), contexts
