# PowerPoint Contents and Design Clues

## Slide 1 — Title Slide

**Title:** Amharic Coffee Trade Regulation RAG System  
**Subtitle:** A Retrieval-Augmented Generation Approach for Ethiopian Coffee Rules  
**Footer:** Your name, course name, instructor, date

**Design clue:**
- Use a clean coffee-themed background.
- Add a coffee bean or document icon.
- Keep the title large and centered.
- Use dark brown and beige colors.

---

## Slide 2 — Problem Statement

**Title:** Why this project is needed

**Content:**
- Ethiopian coffee trade rules exist in PDF documents.
- These documents are hard to search manually.
- Users may need quick answers about buying, selling, grading, or exporting coffee.
- Amharic support is important for local access.

**Design clue:**
- Use 2-column layout.
- Left side: short bullets.
- Right side: problem icon or document/search illustration.
- Keep text minimal.

---

## Slide 3 — Project Objective

**Title:** Project objectives

**Content:**
1. Build a question-answering system for Amharic coffee trade documents.
2. Retrieve relevant legal passages from PDFs.
3. Generate grounded answers in Amharic.
4. Demonstrate RAG using pretrained models.

**Design clue:**
- Use numbered boxes or cards.
- Put one objective per box.
- Use green or gold accent color for emphasis.

---

## Slide 4 — Why Coffee Trade Regulation?

**Title:** Why this domain?

**Content:**
- Coffee is central to Ethiopia’s economy.
- Trade rules are practical and meaningful.
- PDF legal documents are focused and structured.
- The topic is specific enough for a strong assignment.

**Design clue:**
- Use an infographic style.
- Add icons for economy, law, coffee, and PDF.
- Use a simple map of Ethiopia or a coffee cup symbol.

---

## Slide 5 — Data Sources

**Title:** Data collection sources

**Content:**
- Coffee proclamation PDF
- Coffee buying and selling rules PDF
- Coffee grading and quality regulation PDF
- Coffee export or licensing procedure PDF

**Optional source note:**
- Ministry of Agriculture
- Ethiopian Coffee and Tea Authority
- FAO Ethiopia

**Design clue:**
- Show the 4 PDFs as stacked document cards.
- Put source logos or website names underneath.
- Use a light background for readability.

---

## Slide 6 — Methodology Overview

**Title:** How the system works

**Content:**
1. Convert PDFs into text
2. Split text into chunks
3. Create embeddings for each chunk
4. Store vectors in FAISS
5. Search for the most similar chunks
6. Generate an answer using a pretrained model

**Design clue:**
- Use a horizontal pipeline diagram.
- Add arrows between steps.
- Make each step a separate colored block.

---

## Slide 7 — Document Preprocessing

**Title:** Preprocessing and chunking

**Content:**
- PDF text is cleaned and saved as `.txt` files.
- Long documents are split into smaller chunks.
- Overlap is used so important context is not lost.
- Chunking improves retrieval accuracy.

**Design clue:**
- Use a before-and-after visual.
- Left: long document block.
- Right: small chunk blocks.
- Highlight overlap with a shaded region.

---

## Slide 8 — Feature Extraction

**Title:** Embeddings and semantic representation

**Content:**
- The system uses multilingual sentence embeddings.
- Each chunk becomes a vector.
- The user query also becomes a vector.
- Similar meaning means similar vectors.

**Technical note:**
- Embedding model: intfloat/multilingual-e5-small

**Design clue:**
- Use a vector-space or dot-cloud illustration.
- Show query and document vectors moving close together.
- Use blue for query, orange for document chunks.

---

## Slide 9 — Retrieval and Generation

**Title:** FAISS retrieval + mT5 generation

**Content:**
- FAISS finds the nearest text chunks.
- Top relevant passages are passed to the generator.
- The generator answers in Amharic.
- This reduces hallucination and improves grounding.

**Technical note:**
- Retrieval: FAISS IndexFlatIP
- Generator: google/mt5-small

**Design clue:**
- Split the slide into two halves.
- Left: retrieval diagram.
- Right: generation diagram.
- Use a flow from query → chunks → answer.

---

## Slide 10 — Strengths, Limitations, and Conclusion

**Title:** Summary

**Content:**
### Strengths
- Works with a small dataset
- Supports Amharic
- Uses real retrieval, not just guessing

### Limitations
- Small corpus size
- PDF extraction may lose formatting
- Model may not always generate perfect Amharic

### Conclusion
- RAG is a practical way to answer coffee trade questions from documents.
- The system can be expanded with more PDFs later.

**Design clue:**
- Use three columns: strengths, limitations, conclusion.
- Put a closing message at the bottom.
- Use a clean and formal final slide.

---

## Optional closing slide

**Title:** Thank You

**Content:**
- Questions?
- Thank you for listening.

**Design clue:**
- Minimal text only.
- Coffee background or subtle texture.
- Large centered thank-you text.
