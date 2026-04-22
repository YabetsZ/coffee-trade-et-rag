from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import CORPUS_DIR
from .index import build_index, save_index
from .rag import RAGSystem


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=3, ge=1, le=8)


class ChatResponse(BaseModel):
    answer: str
    contexts: list[dict[str, Any]]


class RebuildResponse(BaseModel):
    chunks: int
    message: str


@lru_cache(maxsize=1)
def get_rag() -> RAGSystem:
    return RAGSystem()


app = FastAPI(title="Amharic Coffee RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    rag = get_rag()
    gemini_enabled = bool(rag.gemini_client)
    active_model = rag.active_gemini_model or "fallback-only"
    gemini_status = "ready" if (gemini_enabled and not rag.last_gemini_error) else "fallback"
    return {
        "status": "ok",
        "gemini_status": gemini_status,
        "gemini_enabled": str(gemini_enabled).lower(),
        "active_model": active_model,
        "gemini_error": rag.last_gemini_error[:280],
    }


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        rag = get_rag()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail="Index not found. Rebuild index first.") from exc

    answer, contexts = rag.generate(payload.message.strip(), top_k=payload.top_k)
    return ChatResponse(answer=answer, contexts=contexts)


@app.post("/index/rebuild", response_model=RebuildResponse)
def rebuild_index() -> RebuildResponse:
    index, metadata = build_index(CORPUS_DIR)
    save_index(index, metadata)
    get_rag.cache_clear()
    return RebuildResponse(chunks=len(metadata), message="Index rebuilt successfully.")
