import re
from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

try:
    from google import genai
except Exception:
    genai = None

from .config import (
    EMBEDDING_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    TOP_K,
    USE_PDF_CORPUS,
)
from .index import load_index


class RAGSystem:
    def __init__(self) -> None:
        self.index, self.metadata = load_index()
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.active_gemini_model = ""
        self.gemini_client = (
            genai.Client(api_key=GEMINI_API_KEY)
            if (GEMINI_API_KEY and genai is not None)
            else None
        )
        self.gemini_models = []
        self.last_gemini_error = ""
        for model in [
            GEMINI_MODEL,
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash",
            "models/gemini-flash-latest",
            "gemini-2.0-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro-latest",
        ]:
            if model and model not in self.gemini_models:
                self.gemini_models.append(model)

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
            "መመሪያ:\n"
            "- በአማርኛ ብቻ መልስ።\n"
            "- መልሱ እንደ ተፈጥሯዊ ውይይት አንድ አጭር አንቀጽ ይሁን፤ ዝርዝር/ቁጥር አትጠቀም።\n"
            "- ከተሰጡት ምንጮች ውጭ መረጃ አትጨምር።\n"
            "- በቂ መረጃ ካልተገኘ እንዲህ በል: ከተሰጠው ምንጭ ውስጥ በቂ መረጃ አልተገኘም።\n\n"
            f"ምንጮች:\n{context_text}\n\n"
            f"ጥያቄ: {query}\n"
            "የመጨረሻ መልስ:"
        )

    def _clean_answer(self, text: str) -> str:
        cleaned = text.strip()
        cleaned = re.sub(r"<extra_id_\d+>", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    def _is_low_quality_answer(self, answer: str) -> bool:
        if not answer:
            return True
        if re.search(r"<extra_id_\d+>", answer):
            return True
        prompt_leak_markers = ["ምንጮች:", "ጥያቄ:", "[ምንጭ", "የመጨረሻ መልስ"]
        if any(marker in answer for marker in prompt_leak_markers):
            return True
        if answer in {"።", "፣", ":", "-"}:
            return True
        if len(answer.replace(" ", "")) < 12:
            return True
        alnum_chars = re.findall(r"[A-Za-z0-9\u1200-\u137F]", answer)
        punct_chars = re.findall(r"[^A-Za-z0-9\u1200-\u137F\s]", answer)
        if alnum_chars and (len(punct_chars) / len(alnum_chars)) > 0.6:
            return True
        if not re.search(r"[A-Za-z\u1200-\u137F]", answer):
            return True
        return False

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[^\w\s\u1200-\u137F]", " ", text.lower())).strip()

    def _is_greeting(self, query: str) -> bool:
        q = self._normalize_text(query)
        greeting_patterns = [
            r"\bሰላም\b",
            r"\bሰላም ነው\b",
            r"\bጤና ይስጥልኝ\b",
            r"\bእንደምን አደርክ\b",
            r"\bእንደምን አደርሽ\b",
            r"\bhello\b",
            r"\bhi\b",
            r"\bhey\b",
        ]
        return any(re.search(pattern, q) for pattern in greeting_patterns)

    def _mentions_coffee(self, query: str) -> bool:
        q = self._normalize_text(query)
        coffee_keywords = [
            "ቡና",
            "buna",
            "coffee",
            "espresso",
            "cappuccino",
            "latte",
            "roast",
            "brew",
            "arabica",
            "robusta",
            "caffeine",
        ]
        return any(word in q for word in coffee_keywords)

    def _query_focus_terms(self, query: str) -> set[str]:
        terms = set(re.findall(r"[A-Za-z\u1200-\u137F]+", query.lower()))
        stop_terms = {
            "ቡና",
            "coffee",
            "buna",
            "እንዴት",
            "አንዴት",
            "እባክህ",
            "እባክዎ",
            "ይቻላል",
            "ነው",
            "what",
            "how",
            "can",
            "you",
            "ናቸው",
            "ምን",
            "ምንድን",
            "አሉ",
        }
        return {t for t in terms if len(t) > 2 and t not in stop_terms}

    def _intent_source_bonus(self, query: str, source: str, text: str) -> float:
        q = query.lower()
        source_l = source.lower()
        text_l = text.lower()

        brew_terms = ["ማፍላት", "አፈላል", "ጀበና", "አቦል", "ቶና", "በረካ", "brew", "brewing"]
        quality_terms = ["ጥራት", "grading", "quality", "ቅምሻ", "q-graders"]
        farming_terms = ["እርሻ", "ምርት", "farming", "shade-grown"]
        legal_terms = [
            "ህግ",
            "ሕግ",
            "ህጋዊ",
            "ሕጋዊ",
            "ደንብ",
            "መመሪያ",
            "ፈቃድ",
            "ሽያጭ",
            "መሸጥ",
            "ንግድ",
            "proclamation",
            "regulation",
            "license",
            "ecx",
        ]

        bonus = 0.0
        if any(t in q for t in brew_terms):
            if "brewing" in source_l or any(t in text_l for t in brew_terms):
                bonus += 5.0
            if "quality" in source_l:
                bonus -= 1.8
            if source_l.endswith(".pdf"):
                bonus -= 0.8
        if any(t in q for t in quality_terms):
            if "quality" in source_l or any(t in text_l for t in quality_terms):
                bonus += 4.0
        if any(t in q for t in farming_terms):
            if "farming" in source_l or any(t in text_l for t in farming_terms):
                bonus += 4.0
        if any(t in q for t in legal_terms):
            if source_l.endswith(".pdf"):
                bonus += 4.2
            if any(t in text_l for t in legal_terms):
                bonus += 2.0
        return bonus

    def _general_response(self, query: str) -> str:
        if self._is_greeting(query):
            return "ሰላም! እንኳን ደህና መጡ። እኔ በቡና ርዕሶች ላይ የምረዳ ረዳት ነኝ፤ ስለ ቡና ጥያቄዎን በደስታ እመልሳለሁ።"
        return "እኔ የቡና መረጃ ረዳት ነኝ። እባክዎ ስለ ቡና ታሪክ፣ ማብሰል፣ ጥራት ወይም እርሻ የተያያዘ ጥያቄ ይጠይቁ።"

    def _is_noisy_context(self, text: str) -> bool:
        letters = len(re.findall(r"[A-Za-z\u1200-\u137F]", text))
        ethiopic = len(re.findall(r"[\u1200-\u137F]", text))
        latin = len(re.findall(r"[A-Za-z]", text))
        symbols = len(re.findall(r"[^A-Za-z0-9\u1200-\u137F\s።፣፤፥፦?!,:;\-]", text))
        digits = len(re.findall(r"\d", text))
        noisy_markers = ["page", "gazette", "no..", "....", "qü", "ø", "›", "‹"]
        lowered = text.lower()
        if letters < 30:
            return True
        if letters and (symbols / letters) > 0.2:
            return True
        if letters and (digits / letters) > 0.35:
            return True
        if ethiopic < 40 and latin > max(40, ethiopic * 2):
            return True
        if sum(1 for marker in noisy_markers if marker in lowered) >= 3:
            return True
        return False

    def _clean_context_text(self, text: str) -> str:
        cleaned = text
        cleaned = re.sub(r"(?i)federal negarit gazette[^\n]*", " ", cleaned)
        cleaned = re.sub(r"(?i)page\s*\d+", " ", cleaned)
        cleaned = re.sub(r"[፩-፱\d]+\s*[/.):-]", " ", cleaned)
        cleaned = re.sub(r"\b[ሀ-ፐ]\)", " ", cleaned)
        cleaned = re.sub(r"[‹›Øø®©™]+", " ", cleaned)
        cleaned = re.sub(r"\.{2,}", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    def _filter_contexts(self, contexts: List[dict]) -> List[dict]:
        filtered = []
        for ctx in contexts:
            text = ctx.get("text", "").strip()
            if not text:
                continue
            if self._is_noisy_context(text):
                continue
            filtered.append(ctx)
        return filtered

    def _rerank_contexts(self, query: str, contexts: List[dict], top_k: int) -> List[dict]:
        q_words = set(re.findall(r"[A-Za-z\u1200-\u137F]+", query.lower()))
        focus_words = self._query_focus_terms(query)

        scored: List[tuple[float, dict]] = []
        for ctx in contexts:
            source = str(ctx.get("source", "")).lower()
            text = self._clean_context_text(ctx.get("text", ""))
            words = set(re.findall(r"[A-Za-z\u1200-\u137F]+", text.lower()))

            lexical = len(q_words.intersection(words))
            focus_lexical = len(focus_words.intersection(words))
            vector = float(ctx.get("score", 0.0))
            source_bonus = 0.6 if source.endswith(".txt") else 0.4
            length_penalty = 0.0 if len(text) <= 380 else -1.0
            intent_bonus = self._intent_source_bonus(query, source, text)

            final_score = (1.8 * lexical) + (3.0 * focus_lexical) + (1.4 * vector) + source_bonus + length_penalty + intent_bonus
            scored.append((final_score, ctx))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    def _extractive_answer(self, query: str, contexts: List[dict]) -> str:
        if not contexts:
            return "ከተሰጠው ምንጭ ውስጥ በቂ መረጃ አልተገኘም።"

        q_words = set(re.findall(r"[A-Za-z\u1200-\u137F]+", query.lower()))
        focus_words = self._query_focus_terms(query)
        candidates: List[tuple[int, int, int, str]] = []

        for rank, ctx in enumerate(contexts):
            text = self._clean_context_text(ctx.get("text", ""))
            parts = [s.strip() for s in re.split(r"[።.!?;፤:\n]", text) if s.strip()]
            for sent_idx, sent in enumerate(parts):
                if len(sent) < 25:
                    continue
                if len(sent) > 240:
                    continue
                sent_words = set(re.findall(r"[A-Za-z\u1200-\u137F]+", sent.lower()))
                overlap = len(q_words.intersection(sent_words))
                focus_overlap = len(focus_words.intersection(sent_words))
                if focus_words and focus_overlap == 0:
                    continue
                if overlap > 0:
                    candidates.append((overlap + (2 * focus_overlap), -rank, -sent_idx, sent))

        if not candidates:
            return self._fallback_answer(contexts)

        candidates.sort(reverse=True)
        best_sentences: List[str] = []
        seen = set()

        target_count = 4
        for _, _, _, sent in candidates:
            key = sent.lower()
            if key in seen:
                continue
            seen.add(key)
            best_sentences.append(sent)
            if len(best_sentences) >= target_count:
                break

        response = "። ".join(best_sentences).strip()
        if len(response) > 780:
            response = response[:780].rsplit(" ", 1)[0].strip()
        if response and response[-1] not in {"።", "?", "!"}:
            response += "።"
        return response or self._fallback_answer(contexts)

    def _fallback_answer(self, contexts: List[dict]) -> str:
        if not contexts:
            return "ከተሰጠው ምንጭ ውስጥ በቂ መረጃ አልተገኘም።"

        top_context = contexts[0]
        best_context = self._clean_context_text(top_context.get("text", "").strip())
        if not best_context:
            return "ከተሰጠው ምንጭ ውስጥ በቂ መረጃ አልተገኘም።"

        sentences = [s.strip() for s in re.split(r"[።!?]", best_context) if s.strip()]
        compact = [s for s in sentences if 18 <= len(s) <= 170]
        snippet = "። ".join(compact[:2]).strip() if compact else best_context[:170].strip()
        if snippet and snippet[-1] not in {"።", "?", "!"}:
            snippet += "።"
        source = top_context.get("source", "ምንጭ")
        return f"በተገኙ ምንጮች መሰረት፣ {snippet} ይህ መረጃ ከ {source} የተወሰደ ነው።"

    def _build_gemini_prompt(self, query: str, contexts: List[dict]) -> str:
        context_text = "\n\n".join(
            [
                f"[ምንጭ {i + 1} | {ctx['source']} | score={ctx['score']:.4f}] {ctx['text']}"
                for i, ctx in enumerate(contexts)
            ]
        )
        return (
            "አንተ የአማርኛ የቡና መረጃ ረዳት ነህ።\n"
            "መመሪያ:\n"
            "- በአማርኛ ብቻ መልስ።\n"
            "- እንደ ተፈጥሯዊ ንግግር አንድ አጭር አንቀጽ መልስ ስጥ።\n"
            "- ከተሰጡት ምንጮች ውጭ መረጃ አትጨምር።\n"
            "- በመጨረሻ 'ምንጭ:' ብለህ የተጠቀምክበትን ፋይል ስም ጻፍ።\n"
            "- በቂ መረጃ ካልተገኘ በግልጽ አስታውቅ።\n\n"
            f"ምንጮች:\n{context_text}\n\n"
            f"ጥያቄ: {query}\n"
            "መልስ:"
        )

    def _generate_with_gemini(self, query: str, contexts: List[dict]) -> str:
        if not self.gemini_client:
            return ""
        prompt = self._build_gemini_prompt(query, contexts)
        for model in self.gemini_models:
            try:
                response = self.gemini_client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                text = (response.text or "").strip()
                cleaned = self._clean_answer(text)
                if cleaned:
                    self.active_gemini_model = model
                    return cleaned
            except Exception as e:
                self.last_gemini_error = f"{type(e).__name__}: {e}"
                self.active_gemini_model = f"fallback-error: {model} ({type(e).__name__})"
                continue
        return ""

    def generate(self, query: str, top_k: int = TOP_K) -> Tuple[str, List[dict]]:
        # Keep scope strict: only coffee-domain queries should enter RAG answering.
        if not self._mentions_coffee(query):
            return self._general_response(query), []

        raw_contexts = self.retrieve(query, top_k=max(top_k * 8, 24))
        contexts = self._filter_contexts(raw_contexts)
        if not USE_PDF_CORPUS:
            txt_contexts = [ctx for ctx in contexts if str(ctx.get("source", "")).lower().endswith(".txt")]
            if txt_contexts:
                contexts = txt_contexts
        contexts = self._rerank_contexts(query, contexts, top_k=top_k)
        if not contexts:
            return "ከተሰጠው ምንጭ ውስጥ በቂ መረጃ አልተገኘም።", []

        gemini_answer = self._generate_with_gemini(query, contexts)
        if gemini_answer and not self._is_low_quality_answer(gemini_answer):
            return gemini_answer, contexts

        return self._extractive_answer(query, contexts), contexts
