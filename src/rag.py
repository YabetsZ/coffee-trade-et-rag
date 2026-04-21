from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from .config import EMBEDDING_MODEL, GENERATION_MODEL, TOP_K
from .index import load_index


class RAGSystem:
    def __init__(self) -> None:
        self.index, self.metadata = load_index()
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.tokenizer = AutoTokenizer.from_pretrained(GENERATION_MODEL)
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
        return (
            "እባክህ በአማርኛ ብቻ መልስ። መልሱ አጭር እና ግልጽ ይሁን።\n\n"
            f"ምንጮች:\n{context_text}\n\n"
            f"ጥያቄ: {query}\n"
            "መልስ:"
        )

    def generate(self, query: str, top_k: int = TOP_K) -> Tuple[str, List[dict]]:
        contexts = self.retrieve(query, top_k=top_k)
        prompt = self.build_prompt(query, contexts)

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        output_ids = self.generator.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False,
        )
        answer = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return answer.strip(), contexts
