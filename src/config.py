import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
INDEX_PATH = ARTIFACTS_DIR / "faiss.index"
META_PATH = ARTIFACTS_DIR / "chunks.json"

EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
GENERATION_MODEL = "google/mt5-small"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_PDF_CORPUS = os.getenv("USE_PDF_CORPUS", "true").lower() in {"1", "true", "yes"}
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
TOP_K = 3
