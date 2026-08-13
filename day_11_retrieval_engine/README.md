# Day 11 — Build Your First Document Retrieval System 🔍

Built a mini document retrieval engine on top of my Day 10 `Pipeline` class — the same core idea behind retrieval-augmented generation (RAG).

## 🎯 Objective

Given a user query, retrieve the most relevant documents from a knowledge base, ranked by similarity score — and honestly report when nothing relevant exists, instead of forcing a low-quality match.

## 🏗️ Approach

- Built a 20-document knowledge base on **space exploration**, mixed with a handful of unrelated documents to test out-of-domain behavior.
- Reused `PreprocessingModule` and `VectorizerModule` from Day 10 to clean and vectorize the corpus with TF-IDF.
- Built a `retrieve(query, corpus, top_k=3, threshold=0.1)` function that:
  - Vectorizes the query
  - Ranks all documents by cosine similarity
  - Returns the top-k matches with their scores
  - Returns `"No relevant document found"` if the highest similarity score falls below the threshold

## 🔬 Testing

Tested with 10 queries covering three categories:
- **Clear matches** — e.g. "Moon landing mission," "reusable rocket technology," "life on Mars"
- **Ambiguous queries** — e.g. "space," "orbit" (single words appearing across multiple unrelated documents)
- **Out-of-domain queries** — e.g. "best pizza recipe," "how to train a dog"

## 📊 Failure Analysis

- **"space"** and **"orbit"** — too broad/ambiguous; these words appear across multiple documents on different sub-topics (e.g. "interstellar space" vs. the "Space Station"), so TF-IDF's top result reflects word frequency rather than actual conceptual relevance.
- **"best pizza recipe"** and **"how to train a dog"** — correctly triggered the relevance threshold, returning "No relevant document found" instead of a forced, low-quality match. This is the threshold working as intended.

## 💡 Key Learning: Why Vocabulary Mismatch Breaks TF-IDF

TF-IDF retrieval only matches on literal, exact word overlap — it has no concept that "car" and "automobile," or "Moon landing" and "lunar mission," refer to the same thing. If a query uses different words than the source document, even with identical meaning, TF-IDF assigns a low or zero similarity score because the vectors share no common vocabulary dimensions.

This is exactly the limitation that motivates embeddings (Day 4). Embedding models learn that synonymous words end up close together in vector space, so meaning can be matched even without shared vocabulary. It's why production retrieval and RAG systems rely on embedding-based search — or a hybrid of TF-IDF and embeddings — rather than TF-IDF alone.

---
*Day 11 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
