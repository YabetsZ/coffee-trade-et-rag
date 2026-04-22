from dataclasses import dataclass
from pathlib import Path
from typing import List
import pypdf

from .config import CHUNK_OVERLAP, CHUNK_SIZE, USE_PDF_CORPUS

@dataclass
class Chunk:
    source: str
    chunk_id: int
    text: str


def _normalize_pdf_text(text: str) -> str:
    cleaned = text
    cleaned = cleaned.replace("\x00", " ")
    cleaned = cleaned.replace("\u00ad", "")
    cleaned = cleaned.replace("…", " ")
    cleaned = cleaned.replace("::", ":")
    cleaned = cleaned.replace("‹", " ").replace("›", " ")
    cleaned = cleaned.replace("Ø", " ").replace("ø", " ")

    cleaned = cleaned.replace("፡", " ")
    cleaned = cleaned.replace("፤", "። ")

    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def _is_low_quality_pdf_text(text: str) -> bool:
    if len(text) < 180:
        return True

    letters = sum(ch.isalpha() for ch in text)
    ethiopic = sum("\u1200" <= ch <= "\u137F" for ch in text)
    digits = sum(ch.isdigit() for ch in text)
    odd_symbols = sum(ch in "<>[]{}|_`~@#$%^*=+\\" for ch in text)

    if letters < 120:
        return True
    if ethiopic < 30:
        return True
    if letters and (digits / letters) > 0.35:
        return True
    if letters and (odd_symbols / letters) > 0.08:
        return True

    noise_markers = ["federal negarit gazette", "page", "no..", "qü", "û"]
    lowered = text.lower()
    if sum(1 for marker in noise_markers if marker in lowered) >= 3:
        return True

    return False

def read_files(corpus_dir: Path) -> List[tuple[str, str]]:
    documents: List[tuple[str, str]] = []
    
    # Read text files
    for path in sorted(corpus_dir.glob("**/*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            documents.append((path.name, text))
            
    # Read PDF files only when explicitly enabled.
    if USE_PDF_CORPUS:
        for path in sorted(corpus_dir.glob("**/*.pdf")):
            text_content = []
            try:
                reader = pypdf.PdfReader(path)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        normalized = _normalize_pdf_text(extracted)
                        if not _is_low_quality_pdf_text(normalized):
                            text_content.append(normalized)
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
