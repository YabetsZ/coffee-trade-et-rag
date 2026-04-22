# Amharic Coffee Trade RAG Assistant

A simple Retrieval-Augmented Generation (RAG) project for an NLP assignment using Amharic coffee trade and regulation text.

## Recommended domain

**Domain:** Coffee trade and regulation  
**Language:** Amharic  
**Project focus:** Ethiopian rulings on selling, buying, grading, and trading coffee

## Project title

**Amharic Coffee Trade Regulation RAG System**

## Project objectives

1. Build a retrieval-augmented question answering system for Amharic coffee trade content.
2. Collect and organize a small Amharic corpus from coffee proclamations and regulation PDFs.
3. Use pretrained multilingual embeddings to retrieve relevant passages.
4. Use a pretrained generative model to produce a grounded answer in Amharic.
5. Demonstrate that RAG can support local-language access to Ethiopian coffee trade rules.

## Why this is a good assignment topic

- Coffee is strongly connected to Ethiopian identity, economy, and exports.
- Legal and regulatory PDFs are clean, focused, and excellent for RAG.
- It demonstrates a real RAG pipeline.
- It can work with pretrained multilingual models.
- You can extend it with your own documents later.

## Actual data source options

Use these public sources to build the corpus. Check the pages for Amharic content, PDFs, proclamations, legal notices, or downloadable guides.

1. Ministry of Agriculture, Ethiopia
   - Coffee trade policies, extension guidance, farm management documents
   - https://www.moa.gov.et/

2. Ethiopian Institute of Agricultural Research (EIAR)
   - Coffee research reports, pest control guidance, technology notes
   - https://www.eiar.gov.et/

3. Ethiopian Coffee and Tea Authority
   - Coffee value-chain information, quality guidance, export-related materials
   - https://www.eca.gov.et/

4. Agricultural Transformation Institute (ATI)
   - Extension materials, value-chain reports, farmer support content
   - https://www.ati.gov.et/

5. FAO Ethiopia
   - Farmer guidance, sustainable agriculture, and coffee-related resources
   - https://www.fao.org/ethiopia/

6. Regional agriculture bureaus and extension offices
   - Practical local guides, training documents, bulletin-style materials
   - Example: Oromia, Amhara, and SNNPR regional websites

7. University repositories and theses
   - Coffee theses, processing studies, and extension research with local context
   - Look for institutional repositories from Ethiopian universities

8. Local Amharic news and coffee articles
   - Interviews, extension summaries, farming tips, seasonal crop advice
   - Good for small web-scraped additions

## Best immediate source set

If you already found 4 coffee PDF files, use them as the core corpus. That is enough for a class RAG demo if the PDFs are clear and topic-specific.

Recommended document types:

- coffee trading proclamation
- coffee grading or quality regulation
- coffee buying and selling rules
- coffee export or licensing procedure document

## Starter corpus structure

A small, clean starter corpus can be organized like this:

- `data/corpus/coffee_trade_law_1.txt` — main proclamation or legal text
- `data/corpus/coffee_trade_law_2.txt` — buying and selling rules
- `data/corpus/coffee_trade_law_3.txt` — grading, quality, and market rules
- `data/corpus/coffee_trade_law_4.txt` — export or licensing rules
- Optional extras: `data/corpus/coffee_trade_summary.txt`, `data/corpus/coffee_terms.txt`

You can keep the corpus small at first and add more legal or policy documents later.

## System architecture

1. Load Amharic text documents from `data/corpus/`
2. Split documents into overlapping chunks
3. Convert chunks into embeddings with a pretrained multilingual model
4. Store vectors in a FAISS index
5. Retrieve the most relevant chunks for a query
6. Generate a final answer with a pretrained text-to-text model

## Default models

- Embeddings: `intfloat/multilingual-e5-small`
- Generator: `google/mt5-small`

## Folder structure

- `data/corpus/` — Amharic source documents
- `data/sources.md` — list of source websites and collection notes
- `artifacts/` — saved FAISS index and metadata
- `src/` — code for loading, indexing, retrieval, and generation

## How to run

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Build the index:
   - `python -m src.cli --build`
3. Ask a question:
   - `python -m src.cli --ask "ቡና ለመሸጥ ምን የሕግ መመሪያዎች አሉ?"`
4. Run the API:
   - `python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload`
5. Run React frontend:
   - `cd frontend && npm install && npm run dev`

## Optional: Use Google Gemini for better answers

If you have Google AI credits, you can use Gemini as the generator while keeping your local retrieval/index.

1. Get a Gemini API key from Google AI Studio.
2. Set env vars before running:
   - `export GEMINI_API_KEY="your_api_key"`
   - `export GEMINI_MODEL="gemini-2.0-flash"` (optional)
   - or create `.env` from `.env.example` and fill values
3. Start backend API:
   - `python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload`
4. Start React frontend:
   - `cd frontend && npm run dev`

Frontend API base URL is configured through `frontend/.env`:

- `VITE_API_BASE=http://127.0.0.1:8000`

Use `python -m uvicorn` (not plain `uvicorn`) to ensure your active virtualenv is used.

If Gemini is not being picked up, put `GEMINI_API_KEY` in a project-level `.env` file and restart the backend.

When `GEMINI_API_KEY` is set, the API uses Gemini first and falls back to extractive answering if needed.
If your configured model is unavailable for your account, the backend tries fallback Gemini model names automatically.

## What to submit

For your assignment, you can submit:

- this code base
- a short report explaining the RAG pipeline
- screenshots of sample questions and answers
- a short explanation of the chosen dataset

## Notes

- The sample documents are small demo texts.
- For a stronger project, replace them with real Amharic PDFs, proclamations, regulations, or notices.
- If a source is not in Amharic, keep only the Amharic sections or use it as background reference.
