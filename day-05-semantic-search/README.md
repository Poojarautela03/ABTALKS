# 🔎 Day 5 — Semantic Search

## 🎯 Objective

Build a simple semantic search system and understand how it differs from traditional keyword-based search.

## ✅ Tasks Completed

- Created a small text corpus containing different topics.
- Generated sentence embeddings using Sentence Transformers.
- Converted user queries into embeddings.
- Compared query embeddings with document embeddings.
- Used cosine similarity to calculate relevance.
- Ranked search results based on similarity scores.
- Implemented a `top_k` system to return the best results.
- Compared semantic search with keyword-based search.

## 🔄 Semantic Search Workflow

User Query  
↓  
Generate Query Embedding  
↓  
Compare with Document Embeddings  
↓  
Calculate Cosine Similarity  
↓  
Rank Results  
↓  
Return Top-K Results

## 🆚 Semantic vs Keyword Search

**Keyword Search:** Looks for exact words shared between the query and documents.

**Semantic Search:** Looks for similarity in meaning using numerical embeddings.

## 💡 Key Learning

Semantic search can retrieve relevant results even when the query and document do not contain exactly the same words.

## 🛠️ Technologies Used

- Python 3
- Google Colab
- Sentence Transformers
- NumPy
- Cosine Similarity

---

📌 Day 5 of the ABTalks 60-Day AI Challenge — Artificial Intelligence Track
