from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
INDEX_PATH = ARTIFACTS_DIR / "faiss.index"
META_PATH = ARTIFACTS_DIR / "chunks.json"

EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
GENERATION_MODEL = "google/mt5-small"
CHUNK_SIZE = 700
CHUNK_OVERLAP = 120
TOP_K = 3
