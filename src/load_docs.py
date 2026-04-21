from dataclasses import dataclass
from pathlib import Path
from typing import List
import pypdf

from .config import CHUNK_OVERLAP, CHUNK_SIZE

@dataclass
class Chunk:
    source: str
    chunk_id: int
    text: str

def read_files(corpus_dir: Path) -> List[tuple[str, str]]:
    documents: List[tuple[str, str]] = []
    
    # Read text files
    for path in sorted(corpus_dir.glob("**/*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            documents.append((path.name, text))
            
    # Read PDF files
    for path in sorted(corpus_dir.glob("**/*.pdf")):
        text_content = []
        try:
            reader = pypdf.PdfReader(path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content.append(extracted)
            full_text = " ".join(text_content).strip()
            if full_text:
                documents.append((path.name, full_text))
        except Exception as e:
            print(f"Failed to read PDF {path.name}: {e}")
            
    return documents

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks: List[str] = []
    start = 0
    text = " ".join(text.split())

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap

    return chunks

def load_chunks(corpus_dir: Path) -> List[Chunk]:
    chunks: List[Chunk] = []
    for source, text in read_files(corpus_dir):
        for i, chunk in enumerate(chunk_text(text)):
            chunks.append(Chunk(source=source, chunk_id=i, text=chunk))
    return chunks
