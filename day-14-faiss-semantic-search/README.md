# Day 14 — Build a Semantic Search Engine 🔎

Built a semantic search engine backed by a FAISS vector index, and compared it directly against keyword search on the same 50-document corpus.

## 🎯 Objective

Show how semantic search retrieves documents by matching a query's intent — even with completely different words — while keyword search only matches literal word overlap.

## 🏗️ Approach

- Embedded a 50-document corpus spanning mixed topics (space, tech, food, travel, environment, etc.)
- Note: used **Google Gemini's `gemini-embedding-001`** model instead of OpenAI's `text-embedding-3-small` due to OpenAI API quota limits — same FAISS-based architecture and comparison methodology, just a different embeddings provider
- Stored all vectors as a NumPy `float32` array and built a FAISS **flat index** (`IndexFlatL2`) for exact nearest-neighbor search
- Verified index size matched corpus size (50 documents)
- Built `semantic_search(query, top_k)` — embeds the query and retrieves nearest neighbors from the FAISS index
- Built `keyword_search(query, corpus, top_k)` — a baseline using simple word overlap scoring
- Ran 10 test queries through both systems side by side

## 📊 Findings

**Semantic search won** on queries where the query and source document used different vocabulary but shared meaning — e.g. "training a computer to recognize images" correctly matched a document about computer vision despite almost no shared words. Keyword search missed these entirely due to zero literal overlap.

**Keyword search won** on precision for queries where the exact terms already appeared in the corpus — e.g. "electric cars" directly matching a document containing "electric vehicles." It's also instant and free, with no API call required.

## 💡 Trade-offs: When to Use Which

**Use semantic search when:**
- Queries use different vocabulary than the source documents
- User intent matters more than exact term matching (conversational search, RAG)
- The corpus is large and topically diverse

**Use keyword search when:**
- Exact term matching is required (product codes, legal/medical terms, proper nouns)
- Low latency and zero API cost are critical
- The corpus is small enough that literal precision outweighs recall

**Cost and latency at scale:**
- Semantic search requires an embedding API call per query (and per document at ingestion), adding real cost and network latency that keyword search doesn't have
- Keyword search is near-instant, in-memory, and free
- Production systems often use a **hybrid approach** — keyword search as a fast first-pass filter, with semantic re-ranking on the top candidates — balancing cost, latency, and retrieval quality
- At large scale, FAISS's approximate nearest-neighbor indexes (IVF, HNSW) replace the flat index used here, trading a small amount of accuracy for much faster search over millions of vectors

---
*Day 14 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
