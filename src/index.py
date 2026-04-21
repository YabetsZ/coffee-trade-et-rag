import json
from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .config import ARTIFACTS_DIR, EMBEDDING_MODEL, INDEX_PATH, META_PATH
from .load_docs import Chunk, load_chunks


def embed_texts(model: SentenceTransformer, texts: List[str]) -> np.ndarray:
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
        convert_to_numpy=True,
    )
    return embeddings.astype("float32")


def build_index(corpus_dir: Path) -> Tuple[faiss.Index, List[dict]]:
    chunks = load_chunks(corpus_dir)
    if not chunks:
        raise ValueError(f"No .txt files found in {corpus_dir}")

    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [f"passage: {chunk.text}" for chunk in chunks]
    embeddings = embed_texts(model, texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    metadata = [
        {
            "source": chunk.source,
            "chunk_id": chunk.chunk_id,
            "text": chunk.text,
        }
        for chunk in chunks
    ]
    return index, metadata


def save_index(index: faiss.Index, metadata: List[dict]) -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    META_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def load_index() -> Tuple[faiss.Index, List[dict]]:
    if not INDEX_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError("Index not found. Run `python -m src.cli --build` first.")
    index = faiss.read_index(str(INDEX_PATH))
    metadata = json.loads(META_PATH.read_text(encoding="utf-8"))
    return index, metadata
