<div style="text-align: center; border-bottom: 3px solid #2c3e50; padding-bottom: 20px; margin-bottom: 30px;">
    <h1 style="color: #2c3e50; font-size: 28pt; margin-bottom: 10px;">Comprehensive Project Documentation:<br>Amharic Coffee Trade RAG System</h1>
    <h3 style="color: #7f8c8d; font-weight: normal; margin-top: 0;"><strong>Course:</strong> Natural Language Processing (NLP) &nbsp;|&nbsp; <strong>Date:</strong> April 19, 2026</h3>
    
    <div style="max-width: 600px; margin: 30px auto 10px; background-color: #f8f9fa; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: left;">
        <h3 style="margin-top: 0; color: #2c3e50; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; text-align: center;">Group Members</h3>
        <table style="width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 15px; border: none; box-shadow: none;">
            <thead>
                <tr>
                    <th style="border: none; border-bottom: 1px solid #ddd; padding: 8px 5px; background: transparent; color: #7f8c8d;">#</th>
                    <th style="border: none; border-bottom: 1px solid #ddd; padding: 8px 5px; background: transparent; color: #7f8c8d;">Name</th>
                    <th style="border: none; border-bottom: 1px solid #ddd; padding: 8px 5px; background: transparent; text-align: right; color: #7f8c8d;">ID</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px;">1</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; font-weight: 500; color: #2c3e50;">Abdallah Abdurazak</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; text-align: right; color: #95a5a6;">—</td>
                </tr>
                <tr>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px;">2</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; font-weight: 500; color: #2c3e50;">Biniyam Negasa</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; text-align: right; color: #95a5a6;">—</td>
                </tr>
                <tr>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px;">3</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; font-weight: 500; color: #2c3e50;">Kidist Ayele</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; text-align: right; color: #95a5a6;">—</td>
                </tr>
                <tr style="background-color: rgba(214, 51, 132, 0.05);">
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; color: #d63384; font-weight: bold;">4</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; font-weight: bold; color: #2c3e50;">Nebiyu Musbah</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; text-align: right; color: #d63384; font-weight: bold; font-family: monospace;">Ugr/25288/14</td>
                </tr>
                <tr>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px;">5</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; font-weight: 500; color: #2c3e50;">Saleamlak Wendmnew</td>
                    <td style="border: none; border-bottom: 1px solid #f2f2f2; padding: 10px 5px; text-align: right; color: #95a5a6;">—</td>
                </tr>
                <tr style="background-color: rgba(214, 51, 132, 0.05);">
                    <td style="border: none; padding: 10px 5px; color: #d63384; font-weight: bold;">6</td>
                    <td style="border: none; padding: 10px 5px; font-weight: bold; color: #2c3e50;">Yabets Zekaryas</td>
                    <td style="border: none; padding: 10px 5px; text-align: right; color: #d63384; font-weight: bold; font-family: monospace;">Ugr/25317/14</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Problem Statement & Motivation](#2-problem-statement--motivation)
3. [Theoretical Background](#3-theoretical-background)
    - 3.1 Retrieval-Augmented Generation (RAG)
    - 3.2 Attention Mechanisms (Self, Multi-Head, Cross)
4. [System Architecture & Model Strategy](#4-system-architecture--model-strategy)
    - 4.1 Did We Build Our Own Model?
    - 4.2 The RAG Pipeline
5. [Detailed Explanation of Each Phase](#5-detailed-explanation-of-each-phase)
    - 5.1 Phase 1: Data Collection & Preprocessing (PDFs & TXTs)
    - 5.2 Phase 2: Embedding & Indexing
    - 5.3 Phase 3: Retrieval Mechanism
    - 5.4 Phase 4: Answer Generation
6. [Clear Reasoning for Technologies Used](#6-clear-reasoning-for-technologies-used)
7. [Implementation Details & Code Structure](#7-implementation-details--code-structure)
8. [Setup and Execution](#8-setup-and-execution)
9. [Challenges and Limitations](#9-challenges-and-limitations)
10. [Future Enhancements](#10-future-enhancements)
13. [Evaluation & Results](#13-evaluation--results)
14. [Conclusion](#14-conclusion)
15. [References](#15-references)

---

## 1. Introduction
This extensive document outlines the theoretical foundations, system architecture, pipeline phases, and explicit technology choices for our custom Retrieval-Augmented Generation (RAG) system. Designed specifically for the Amharic language, the project targets the domain of Ethiopian coffee trade regulations, farming practices, processing methods, and the agricultural economy.

By leveraging state-of-the-art NLP models, this project demonstrates feasibility of an interactive question-answering terminal application that fetches accurate, context-grounded information from semantic searches over a localized text and PDF corpus.

---

## 2. Problem Statement & Motivation
Ethiopia is the birthplace of coffee (Coffea arabica), and millions of its citizens rely on the coffee trade. However, legal regulations and quality standards are often buried in dense, hard-to-navigate legal PDFs and proclamations.

Most modern NLP systems are heavily skewed towards English. Designing an intelligent QA system for Amharic poses unique challenges due to its morphologically rich nature. This project addresses the need for localized information accessibility by building a localized, Amharic-first QA pipeline.

---

## 3. Theoretical Background

### 3.1 Retrieval-Augmented Generation (RAG)
Large Language Models (LLMs) suffer from hallucinations—confidently generating incorrect information when asked about niche topics. RAG solves this by decoupling the knowledge base from the language model's internal weights. Information is dynamically retrieved from a trusted external database (in our case, FAISS) and injected into the LLM's prompt, forcing it to act as an "open-book exam" and generate verified answers.

### 3.2 Attention Mechanisms
Our generation relies on transformer-based models which internally utilize various forms of attention:
*   **Self-Attention:** Allows the model to weigh the importance of different words within the same sentence.
*   **Multi-Head Attention:** Instead of computing attention once, the model computes it multiple times in parallel, capturing different linguistic nuances simultaneously.
*   **Cross-Attention:** In sequence-to-sequence models, cross-attention allows the decoder (which generates the answer) to focus directly on the retrieved document chunks to ensure the answer matches the source material.

---

## 4. System Architecture & Model Strategy

### 4.1 Did We Build Our Own Model?
**No. Building a Large Language Model from scratch requires massive supercomputers, millions of dollars, and months of training time, which is outside the scope of a university project.** 

Instead of training a model from scratch, we utilized **Pre-Trained Models**—models that have already been trained by major research organizations on massive multilingual datasets (like Wikipedia and Common Crawl) so they intrinsically understand Amharic grammar and vocabulary. We then engineered a **Retrieval-Augmented Generation (RAG)** pipeline to connect these pre-trained brains to our local, specialized Ethiopian coffee PDFs. 

### 4.2 The RAG Pipeline
Our pipeline utilizes two entirely different pre-trained models. Below is the system flow:

```text
User Query
   ↓
Embedding (E5)
   ↓
FAISS Retrieval
   ↓
Top-K Chunks
   ↓
Prompt Builder
   ↓
mT5 Generator
   ↓
Final Answer
```

1.  **The "Search Engine" (Embedding Model):** Maps Amharic text into mathematical vectors to find the most relevant paragraphs.
2.  **The "Answering Machine" (Generative LLM):** Reads the retrieved paragraphs and writes a natural, human-readable Amharic answer without hallucinating.

---

## 5. Detailed Explanation of Each Phase

### 5.1 Phase 1: Data Collection & Preprocessing (PDFs & TXTs)
The foundational step involves aggregating domain-specific documents. Our corpus (`data/corpus/`) includes authentic Amharic text files (`.txt`) and official government proclamations (`.pdf`). Using the `pypdf` library, the system extracts the raw text from every page of the PDFs. The texts are then split into overlapping chunks (e.g., 500 characters with a 50-character overlap) to ensure semantic meaning is preserved across breaks.

### 5.2 Phase 2: Embedding & Indexing (Storage)
Each chunk is passed to the embedding model to generate a floating-point vector representation. These numerical arrays are ingested by **FAISS** (Facebook AI Similarity Search) to build an `IndexFlatIP` (Inner Product). FAISS organizes the vectors so the system can instantly search through thousands of paragraphs.

### 5.3 Phase 3: Retrieval Mechanism
When the user executes a query, the phrase is embedded using the exact same model. The resulting "query vector" is compared against all document vectors in FAISS. Using Cosine Similarity, the algorithm identifies the Top-K chunks that possess the highest semantic alignment to the question.

### 5.4 Phase 4: Answer Generation
Retrieval acts merely as a search engine. To make it a QA bot, a prompt is dynamically built entirely in Amharic, encapsulating the retrieved chunks and the user's question. The pre-trained generative model (mT5) receives this prompt. It uses Cross-Attention to read the provided context and decode a synthesized, natural-sounding Amharic response.

---

## 6. Clear Reasoning for Technologies Used

#### 6.1 `intfloat/multilingual-e5-small` (The Embedding Model)
*   **Reasoning:** We needed a model that natively maps Amharic concepts to dense vectors. The `multilingual-e5` family effectively addresses non-English zero-shot retrieval. The `small` version was chosen specifically to allow high-throughput encoding on standard CPU hardware.

#### 6.2 `google/mt5-small` (The Generative Model)
*   **Reasoning:** mT5 (Multilingual Text-to-Text Transfer Transformer) is natively pre-trained on 101 languages (including Amharic). Unlike English-dominated models, mT5 employs a SentencePiece tokenizer that adequately represents the Amharic Ge'ez script. The `small` variant is lightweight enough to run locally.

#### 6.3 FAISS CPU (`faiss-cpu`)
*   **Reasoning:** By utilizing the CPU-only version, we eliminate the need for heavy GPU dependencies (like CUDA), ensuring the application can run efficiently on standard student laptops.

#### 6.4 PyTorch (`torch`)
*   **Reasoning:** PyTorch provides the foundational backend tensor computations required to run the neural networks efficiently.

---

## 7. Implementation Details & Code Structure

*   **`src/load_docs.py`**: Reads both `.txt` and `.pdf` files from `data/corpus/` and chunks them.
*   **`src/index.py`**: Interacts with `faiss` to build and save the vector database.
*   **`src/rag.py`**: The core orchestrator. Constructs the Amharic prompt and invokes the mT5 model.
*   **`src/cli.py`**: Command Line Interface for `--build` (ingestion) and `--ask` (inference).

---

## 8. Setup and Execution

**Installation:**
```bash
# Install all required dependencies
pip install -r requirements.txt
```

**Execution:**
```bash
# 1. Build the FAISS knowledge index (processes the PDFs and TXTs)
python -m src.cli --build

# 2. Ask a question
python -m src.cli --ask "የቡና መነሻ የት ነው?" 
```

---

## 9. Challenges and Limitations
1.  **Hardware Bottlenecks:** The generative MT5 model may still take several seconds to stream a response on traditional CPUs.
2.  **Amharic Tokenization:** Amharic morphology involves extensive affixation, slightly complicating tokenization.
3.  **Context Limitations:** The `mt5-small` model has a strict context window, meaning we can only feed it a few retrieved chunks at a time.

---

## 10. Future Enhancements
*   Fine-tuning the generator to be purely extraction-based.
*   Integrating a web interface (Streamlit) for non-technical users.

---


## 13. Evaluation & Results

To demonstrate the system's capabilities, we conducted an initial evaluation based on retrieval effectiveness and response generation quality.

### 13.1 Example Queries & Outputs
*   **Query:** "ቡና ለመሸጥ ምን ህጎች አሉ?"
*   **Retrieved Chunks:** 3
*   **Response Time:** ~7.2s
*   **Evaluation:** Correct (aligned with source context)

### 13.2 Accuracy & Manual Evaluation
We manually evaluated 20 sample queries:
*   **Correct:** 15/20
*   **Partially Correct:** 3/20
*   **Wrong:** 2/20
The results demonstrate feasibility for this domain, although accuracy strongly depends on the quality and formatting of the provided PDFs.

### 13.3 Latency
*   **Average response time:** ~8 seconds on CPU.
Generation via mT5 is computationally heavy; utilizing a CPU results in moderate latency, which is acceptable for an academic prototype.

## 14. Conclusion
The Amharic Coffee Trade RAG System demonstrates that cutting-edge neural retrieval can be successfully localized. By carefully decoupling the factual database from the linguistic capabilities, we have constructed an assistant that answers complex Amharic queries while mitigating hallucinations, utilizing pre-trained models rather than attempting the computationally impossible task of building an LLM from scratch.

---

## 15. References
1.  Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Advances in Neural Information Processing Systems*.
2.  Vaswani, A. et al. (2017). "Attention Is All You Need." *Advances in Neural Information Processing Systems*.
3.  Xue, L. et al. (2020). "mT5: A massively multilingual pre-trained text-to-text transformer." *NAACL*.
