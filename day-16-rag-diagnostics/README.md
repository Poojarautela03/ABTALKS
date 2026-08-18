# Day 16 — Diagnosing RAG Failure Modes 🩺

Systematically tested my Day 15 RAG pipeline against 15 queries designed to trigger five known failure modes, logged every retrieval and generation, and implemented fixes for the issues found.

## 🎯 Objective

A RAG pipeline can fail silently — returning confident-sounding wrong answers. This exercise builds a clear diagnostic map of exactly where and why the pipeline breaks down, rather than just trusting it works.

## 🏗️ Approach

- Note: used **Google Gemini** (`gemini-embedding-001` + `gemini-3.6-flash`) instead of OpenAI due to API quota limits — same methodology, different provider
- Designed a 15-query test suite, 3 queries per failure mode:
  1. **Retrieval failure** — questions the knowledge base genuinely doesn't cover
  2. **Context window overflow** — broad queries with `top_k` pushed high, diluting focus
  3. **Answer-context mismatch** — checking whether the generated answer actually matches the retrieved chunk
  4. **Vague context retrieved** — ambiguous, underspecified queries
  5. **Correct chunk retrieved, wrong answer generated** — testing whether the model faithfully uses good context
- Added logging to the pipeline so every call records the retrieved chunks, their similarity scores, and the final answer to a local `rag_diagnostic_results.json` file

## 📊 Failure Classification

Each of the 15 queries was classified by failure type with a one-sentence diagnosis — see the full table in the notebook. Two failures were traced back to root causes:

- **Vague queries like "Tell me about the competition"** failed because the knowledge base is made of short, atomic single-sentence chunks — there's no chunk that encodes broader concepts like "competition" as a topic, only a narrow "main competitor" fact, creating a lexical/semantic gap.
- **Queries like "What's new with the company?"** failed because embeddings have no inherent concept of recency — no chunk textually signals "this is the newest fact," so the model has no reliable signal to identify what counts as "new."

## 🔧 Fixes Implemented

1. **Similarity threshold** — added a distance cutoff so the pipeline explicitly declines to answer ("I don't have enough relevant information") instead of forcing a weak-context answer when the best match is too dissimilar.
2. **Tightened system prompt** — updated the prompt to explicitly forbid inferring or generalizing beyond the exact retrieved facts, reducing the model's tendency to synthesize plausible-but-unstated answers.

## 📈 Scorecard

Rated each of the 15 queries on retrieval quality (1-5) and answer quality (1-5) separately, then averaged both dimensions. Full per-query scores are in the notebook — as expected, context-overflow and vague-context queries scored noticeably lower on both dimensions than clean, specific single-fact queries.

## 💡 Key Learning

Retrieval quality and answer quality are separate failure surfaces — a RAG system can retrieve the right chunk and still generate a wrong answer, or retrieve a weak chunk and still get lucky with generation. Diagnosing these separately (rather than just checking "was the final answer right or wrong") is what turns a prototype into something you can actually trust and improve systematically.

---
*Day 16 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
