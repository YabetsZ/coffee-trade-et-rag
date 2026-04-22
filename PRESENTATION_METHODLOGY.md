# Presentation Notes: Methodology of the Amharic Coffee Trade RAG System

## 1. Project title

**Amharic Coffee Trade Regulation RAG System**

## 2. One-sentence summary

This project builds a Retrieval-Augmented Generation (RAG) system that answers questions in Amharic about Ethiopian coffee trade rulings, buying rules, quality grading, and related regulations by retrieving relevant passages from PDF-based documents and generating a grounded answer.

---

## 3. What the project is trying to solve

Many useful Ethiopian coffee trade documents exist in legal or policy form, but they are difficult to search manually. A user may want to ask questions such as:

- What rules apply to buying coffee?
- What are the quality or grading requirements?
- What does the proclamation say about coffee trading?
- What procedures are required for export or licensing?

The system helps by:

1. finding the most relevant text passages,
2. providing context to the language model,
3. generating an answer in Amharic.

---

## 4. Why RAG instead of fine-tuning

We are using **RAG** instead of training a model from scratch because:

- the available dataset is small,
- the documents are domain-specific,
- legal text changes over time,
- RAG is easier to build for an assignment,
- it can work well even with a small corpus.

### Key idea

RAG combines two tasks:

- **Retrieval**: find relevant document chunks,
- **Generation**: produce a final answer using the retrieved context.

---

## 5. Algorithm used

The system uses a standard RAG pipeline:

### Step 1: Document collection
- We collect 4 PDF documents related to coffee trade rulings and regulations.
- These are converted to plain text and stored as `.txt` files.

### Step 2: Chunking
- Each document is split into smaller overlapping chunks.
- Chunking is important because long legal documents cannot be passed as one huge input.
- Overlap helps preserve context across chunk boundaries.

### Step 3: Embedding / feature extraction
- Each chunk is converted into a dense vector embedding.
- The query is also converted into the same embedding space.

### Step 4: Vector search
- The system compares the query vector with all chunk vectors using FAISS.
- The most similar chunks are retrieved.

### Step 5: Prompt construction
- The retrieved chunks are inserted into a prompt.
- The prompt asks the model to answer in Amharic and use only the retrieved context.

### Step 6: Generation
- A pretrained sequence-to-sequence model generates the final answer.

---

## 6. Is it pretrained or custom-built?

This project is **mostly pretrained**, not custom-trained.

### Pretrained models used

- **Embedding model**: `intfloat/multilingual-e5-small`
- **Generator model**: `google/mt5-small`

### Custom-built parts

What is custom in this project is the **pipeline**, not the base models:

- document cleaning,
- chunking,
- indexing,
- retrieval logic,
- prompt design,
- data organization.

So the project is a **custom RAG system built on top of pretrained models**.

---

## 7. Feature extraction method

The main feature extraction method is **dense semantic embeddings**.

### Why embeddings?

Traditional keyword matching only checks exact words. That is weak for Amharic because:

- the same idea can be expressed with different wording,
- inflected forms may vary,
- synonyms may not match exactly.

Embeddings solve this by mapping text into a numerical vector that captures meaning.

### How it works

- Each text chunk becomes a vector.
- The query becomes a vector.
- Similar meanings produce vectors that are close together.

### In this project

The code uses:
- `SentenceTransformer` for embeddings,
- `normalize_embeddings=True` so vectors can be compared with cosine-like similarity,
- `FAISS IndexFlatIP` for fast similarity search.

Because embeddings are normalized, inner product behaves like cosine similarity.

---

## 8. Similarity search algorithm

The retrieval step uses **FAISS**.

### Why FAISS?

FAISS is used because it is:

- fast,
- simple,
- suitable for vector search,
- good for small and medium datasets.

### Search method used

- The code builds an `IndexFlatIP` index.
- `IP` means inner product.
- Since embeddings are normalized, the ranking reflects semantic similarity.

### Retrieval output

The system returns:
- the top matching chunks,
- their source file,
- chunk id,
- similarity score.

---

## 9. Why chunking matters

Chunking is one of the most important design choices.

### Reason 1: Model input limits
Large PDF text cannot be used directly as one input.

### Reason 2: Better retrieval precision
Smaller chunks make it easier to find the exact relevant rule or paragraph.

### Reason 3: Context continuity
Overlap preserves meaning when a sentence or rule spans chunk boundaries.

### In this project

- chunk size is controlled in `src/config.py`,
- overlap is added to preserve context.

---

## 10. Why multilingual pretrained models?

We are using multilingual models because the text is in Amharic.

### Advantages

- they support many languages,
- they can handle Amharic better than English-only models,
- they allow the project to work without training a model from zero.

### Main limitation

A multilingual pretrained model may not be perfect for every legal phrase, but it is strong enough for a class project and a RAG demo.

---

## 11. How the answer is generated

After retrieval, the system builds a prompt like this:

- explain that the answer should be in Amharic,
- list the retrieved sources,
- provide the user question,
- ask the generator to answer.

This makes the response grounded in the retrieved text instead of hallucinating.

### Why this matters

Without retrieved context, the model may give a generic answer. With RAG, it can answer based on the actual coffee ruling text.

---

## 12. End-to-end workflow

1. Load `.txt` documents from `data/corpus/`
2. Split them into chunks
3. Embed chunks with a pretrained multilingual embedding model
4. Store vectors in FAISS
5. Embed the user question
6. Search for the most similar chunks
7. Send the chunks and question to the generator
8. Output the final answer in Amharic

---

## 13. What is technically interesting in this project?

If asked in class, emphasize these points:

- It is a real **RAG** system.
- It uses **pretrained multilingual embeddings**.
- It uses **vector search** rather than keyword search.
- It includes **Amharic language support**.
- It is based on **domain-specific legal documents**.
- It is designed to answer questions grounded in real text.

---

## 14. Strengths of the approach

- Works with a small corpus
- Easy to demonstrate
- Good for local language use cases
- Modular and extendable
- Can be improved later with more PDFs or a better generator model

---

## 15. Limitations

Be honest about these in the presentation:

- The corpus is still small.
- PDF text extraction may lose formatting.
- The generator may not always produce perfect Amharic.
- It is not fully fine-tuned on coffee law documents.
- Legal accuracy depends on the quality of the source text.

---

## 16. Possible improvements

If the lecturer asks how you could improve it:

- add more coffee regulation PDFs,
- improve PDF text extraction,
- use a stronger multilingual generator,
- add citation highlighting,
- create a web interface with Streamlit,
- compare RAG with keyword search,
- evaluate retrieval accuracy with sample questions.

---

## 17. Suggested presentation flow

### Slide 1: Title
- Project name
- Your name
- Course name

### Slide 2: Problem
- Why coffee rulings are hard to search manually
- Why Amharic matters

### Slide 3: Project objective
- What the system does

### Slide 4: Data
- The 4 PDF files
- Why they were chosen

### Slide 5: Methodology overview
- RAG pipeline diagram

### Slide 6: Document preprocessing
- Cleaning and chunking

### Slide 7: Feature extraction
- Embeddings
- Dense vectors

### Slide 8: Retrieval
- FAISS
- Similarity search

### Slide 9: Generation
- mT5
- Prompt construction

### Slide 10: Strengths and limitations
- What works well
- What can be improved

---

## 18. Short lecture-style explanation

You can say:

> This project uses a Retrieval-Augmented Generation approach to answer questions about Ethiopian coffee trade rulings in Amharic. Instead of training a model from scratch, we use pretrained multilingual models. First, the PDF documents are converted into smaller text chunks. Then each chunk is transformed into a semantic embedding, which is a vector representation of meaning. When a user asks a question, the system converts the query into the same vector space and retrieves the most similar chunks using FAISS. Those chunks are passed to a pretrained generator, which produces the final answer in Amharic. This makes the system more accurate and grounded than a pure language model response.

---

## 19. One-minute summary

- **Task**: Amharic coffee trade Q&A
- **Method**: RAG
- **Models**: pretrained multilingual embedding model + pretrained generator
- **Feature extraction**: dense sentence embeddings
- **Retrieval**: FAISS similarity search
- **Output**: grounded Amharic answer

---

## 20. Final takeaway

The most important idea to present is:

> We are not training a model from scratch. We are building a smart retrieval layer over pretrained language models so that the system can answer questions from coffee regulation documents in Amharic.
