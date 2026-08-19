# Day 17 — Improve RAG Precision with Metadata Filtering 🎯

Added structured metadata filtering on top of my Day 15/16 RAG pipeline to measure whether constraining retrieval by category and date improves precision over pure vector similarity search.

## 🎯 Objective

Pure vector similarity is context-blind — it can't distinguish a 2020 document from a 2024 one, or a technical reference from a marketing overview. Metadata filtering adds structured constraints on top of vector search so retrieval returns the *right type* of document, not just the most similar one.

## 🏗️ Approach

- Note: used **Google Gemini** (`gemini-embedding-001` + `gemini-3.6-flash`) instead of OpenAI due to API quota limits — same methodology, different provider
- Restructured the knowledge base so each document carries metadata: `source`, `category`, `date`, and `document_type`, alongside the text content
- Paired metadata with embeddings by index position (FAISS's flat index has no native metadata support, so a parallel metadata list keyed by vector index was used)
- Built `filtered_retrieve(query, filters, top_k)` — over-fetches a larger candidate pool from FAISS, then applies metadata filters as a post-filter, then trims to `top_k`
- Implemented a **category filter** (restrict to a specified category string) and a **date filter** (exclude documents older than a configurable cutoff)
- Ran 5 queries with filters active and the same 5 without, comparing retrieved chunks side by side

## 📊 Findings

Unfiltered retrieval sometimes surfaced documents that were semantically similar but categorically wrong — e.g. a marketing roadmap document ranking high for a technical query purely due to shared vocabulary. Filtered retrieval consistently excluded these, staying confined to the genuinely relevant document type or category for each query.

## 🏛️ Architecture Update

The Day 15 architecture had a single "FAISS index search" step. The upgraded pipeline inserts a metadata filter stage between vector search and prompt construction:

`Query → Embed → FAISS search (over-fetch pool) → Metadata filter → Top-k selection → Prompt template → LLM`

This is a **post-filtering** approach — FAISS still ranks purely by vector similarity, and filtering happens afterward on the candidate pool. A more scalable production approach would push filters into the vector database itself (pre-filtering, as supported by systems like Pinecone or Weaviate), but FAISS's flat index has no native metadata support, making post-filtering the practical choice at this scale.

## ⚠️ Two Edge Cases This Still Can't Handle

1. **Missing metadata fields** — a document ingested without a `category` or `date` field is silently excluded from any filtered search (the equality check fails silently on a missing key), with no visible warning that a potentially relevant document was dropped.
2. **Conflicting or multi-valued categories** — this implementation assumes one category per document. A document that genuinely spans two categories (e.g. a pricing announcement that's both "product" and "finance") can only be tagged with one, making it invisible to filtered searches on the other — a limitation that would need list-based tags and "any-match" filter logic to properly resolve.

---
*Day 17 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
