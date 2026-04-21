# Amharic Coffee Trade RAG

End-to-end Retrieval-Augmented Generation (RAG) system for Ethiopian coffee trade and regulation documents in Amharic.

This guide explains how to run the project:
1. On Kaggle
2. On Google Colab
3. Locally with the JavaScript UI and an ngrok-backed API

## Overview

The pipeline does the following:
1. Loads documents from `data/corpus`
2. Splits text into overlapping chunks
3. Embeds chunks with multilingual embeddings
4. Stores vectors in FAISS
5. Retrieves top relevant chunks for a query
6. Generates an answer with an instruction-tuned LLM

Main implementation files:
1. `src/load_docs.py`
2. `src/index.py`
3. `src/rag.py`
4. `src/cli.py`
5. `ui/index.html`

## Requirements

1. Python 3.10+
2. `pip install -r requirements.txt`
3. Dataset files in `data/corpus`

## Quick Local CLI Test

Run from repo root:

```bash
pip install -r requirements.txt
python -m src.cli --build
python -m src.cli --ask "የቡና ጥራት መስፈርቶች ምንድን ናቸው?"
```

If `--build` succeeds, FAISS artifacts are written to `artifacts`.

## Kaggle Runbook

### 1. Notebook settings

1. Open a new notebook
2. Enable Internet
3. Use GPU T4

### 2. Clone repo and install dependencies

```python
import os
import shutil

REPO_URL = "https://github.com/YabetsZ/coffee-trade-et-rag.git"
PROJECT_NAME = "nlp-project"
WORKING_DIR = f"/kaggle/working/{PROJECT_NAME}"

if os.path.exists(WORKING_DIR):
    shutil.rmtree(WORKING_DIR)

!git clone {REPO_URL} {WORKING_DIR}
%cd {WORKING_DIR}

!pip install -U pip
!pip install -r requirements.txt
!pip install -U flask pyngrok flask-cors accelerate sentencepiece
```

### 3. Build index

```python
!ls -la data/corpus | head
!python -m src.cli --build
```

### 4. Start Flask + ngrok API bridge

Security note: never hardcode ngrok token in notebook cells. Store it in Kaggle Secrets as `NGROK_AUTHTOKEN`.

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
from kaggle_secrets import UserSecretsClient
import traceback

from src.rag import RAGSystem

secrets = UserSecretsClient()
NGROK_TOKEN = secrets.get_secret("NGROK_AUTHTOKEN")
ngrok.set_auth_token(NGROK_TOKEN)

app = Flask(__name__)
CORS(app)
rag = RAGSystem()

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/ask")
def ask():
    try:
        data = request.get_json(silent=True) or {}
        query = (data.get("query") or "").strip()
        if not query:
            return jsonify({"error": "query is required"}), 400

        answer, contexts = rag.generate(query)
        sources = [
            f"{c['source']} (chunk {c['chunk_id']}, score={c['score']:.4f})"
            for c in contexts
        ]
        return jsonify({"answer": answer, "sources": sources})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

tunnel = ngrok.connect(5000)
print("API BASE:", tunnel.public_url)
print("ASK URL :", f"{tunnel.public_url}/ask")

app.run(host="0.0.0.0", port=5000)
```

### 5. Test API quickly

```python
import requests

ASK_URL = "PASTE_NGROK_ASK_URL_HERE"
r = requests.post(ASK_URL, json={"query": "የቡና ሕጋዊ የሽያጭ መመሪያ ምንድን ነው?"}, timeout=120)
print(r.status_code)
print(r.json())
```

## Colab Runbook

### 1. Clone and install

```python
!git clone https://github.com/YabetsZ/coffee-trade-et-rag.git
%cd coffee-trade-et-rag
!pip install -U pip
!pip install -r requirements.txt
!pip install -U flask pyngrok flask-cors accelerate sentencepiece
```

### 2. Build index

```python
!ls -la data/corpus | head
!python -m src.cli --build
```

### 3. Run API bridge

Use the same Flask + ngrok cell from Kaggle. In Colab, read token from environment variable or input prompt, not hardcoded source.

## Local JavaScript UI

The local frontend is available in `ui/index.html`.

### 1. Start local static server

From repo root:

```bash
python -m http.server 5500
```

### 2. Open UI

Open in browser:

```text
http://localhost:5500/ui/index.html
```

### 3. Connect to Kaggle/Colab API

1. Paste current ngrok URL ending in `/ask`
2. Enter Amharic question
3. Click Ask

## Typical Workflow

1. Start notebook runtime (Kaggle/Colab)
2. Build index once (`python -m src.cli --build`)
3. Start Flask + ngrok bridge
4. Copy `/ask` URL
5. Open local UI and paste URL
6. Ask questions from your browser

## Troubleshooting

1. Empty or bad answers
   - Ensure you are using instruction-tuned model config in `src/config.py`
   - Rebuild index after major corpus changes

2. API connection failed
   - Check notebook server is still running
   - Check ngrok URL did not change
   - Verify `/ask` endpoint and CORS

3. `ModuleNotFoundError`
   - Reinstall dependencies: `pip install -r requirements.txt`

4. FAISS install issues on cloud
   - Retry install
   - If FAISS is preinstalled in environment, install remaining requirements without `faiss-cpu`

## Security Notes

1. Do not commit ngrok authtokens
2. Use notebook secrets for keys
3. If a token was exposed, revoke and regenerate it immediately

## Project Structure

```text
.
├── data/
│   └── corpus/
├── src/
│   ├── cli.py
│   ├── config.py
│   ├── index.py
│   ├── load_docs.py
│   └── rag.py
├── ui/
│   └── index.html
└── requirements.txt
```
