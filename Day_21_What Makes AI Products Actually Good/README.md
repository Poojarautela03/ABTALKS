# Day 21 — What Makes AI Products Actually Good 🧪

A structured product-quality audit of the Day 20 AI knowledge assistant, testing it against five dimensions that matter to real users — not just whether it works on a happy-path demo.

## 🎯 Objective

A working prototype and a genuinely good AI product aren't the same thing. This audit tests the Day 20 assistant systematically across accuracy, latency, reliability, transparency, and graceful degradation, using at least 10 queries per dimension rather than eyeballing a single response.

## 📏 The Five Dimensions

1. **Accuracy** — the answer correctly reflects what the knowledge base actually states, with no fabricated or omitted facts.
2. **Latency** — the time between a user submitting a query and receiving a complete response, end to end.
3. **Reliability** — the system produces a valid, well-formed response consistently across repeated and varied queries, without crashing or returning malformed output.
4. **Transparency** — every answer clearly shows the user where the information came from, in a way a non-technical person could understand and verify.
5. **Graceful degradation** — when the system can't answer confidently, it says so honestly instead of guessing or failing silently.

## 🏗️ Approach

- Note: used **Google Gemini** (`gemini-embedding-001` + `gemini-flash-lite-latest`) instead of OpenAI due to API quota limits — same methodology, different provider
- Rebuilt the Day 20 pipeline (chunking, FAISS search, grounding prompt) with per-component timing added to every call
- **Accuracy + latency:** ran 10 factual queries, measured end-to-end response time and which pipeline component (retrieval vs. generation) consumed the most time
- **Reliability:** repeated the same query 10 times, checking whether every response was valid and well-formed
- **Transparency:** checked whether every response included a source citation with a human-readable title, not just an internal document ID
- **Graceful degradation:** sent 5 queries entirely outside the knowledge base, checking whether the system honestly refused instead of guessing
- **Natural language test:** wrote 10 queries the way a real, non-technical user would actually type them — casual, vague, typo-prone — to see how quality held up against clean engineered test queries

## 📊 Results

| Dimension | Score (1-5) | Notes |
|---|---|---|
| Accuracy | 5/5 | All 10 factual queries answered correctly, each citing the correct source document |
| Latency | 4/5 | Average end-to-end latency: 3.21s (retrieval: 2.03s, generation: 1.18s) — retrieval was the slowest component |
| Reliability | 5/5 | 100% of repeated calls returned a valid, well-formed response |
| Transparency | 5/5 | 100% of responses included clear, understandable source citations |
| Graceful degradation | 5/5 | 100% of out-of-scope queries were handled honestly, correctly refusing rather than guessing |

**Overall: 24/25** — the assistant performed strongly across every dimension. The one point lost was on latency, where retrieval — not generation — was unexpectedly the slower half of the pipeline.

## 🗣️ Engineered Queries vs. Real User Language

The 10 casual, typo-prone user-style queries ("hey so like who even started nimbus robotics lol", "battery life???") were handled with the same accuracy and citation quality as the clean engineered queries. The grounding prompt's instruction to answer only from retrieved context proved robust to informal phrasing — the model didn't need clean, well-formed input to correctly interpret intent and retrieve the right chunks.

## 🎯 Top 3 Priorities If Launching Next Week

1. **Investigate retrieval latency.** Retrieval (2.03s) outpaced generation (1.18s) as the slowest pipeline stage — counterintuitive, since FAISS search over a small flat index should be near-instant. This points to the embedding API call (not the vector search itself) as the real bottleneck, since every query requires a live embedding call before FAISS can even run. Caching frequent queries or batching embedding calls would meaningfully cut latency.
2. **Add explicit latency monitoring in production.** A 3.21s average is workable for a demo but borderline for a chat-like product experience; before real users arrive, add logging/alerting so a latency regression is caught immediately rather than discovered through complaints.
3. **Expand the knowledge base before scaling users.** Every dimension scored well specifically because queries stayed within a well-covered, 7-document knowledge base. Before launch, the same 5-dimension audit should be re-run against a larger, messier knowledge base more representative of real-world coverage gaps.

## 💡 Key Learning

A demo only has to work once, in front of you, on inputs you already know it can handle. A product has to work consistently, for people who phrase things differently than you expect, and it has to fail honestly when it doesn't know something. This audit made the gap between those two bars concrete instead of theoretical — and in this case, the pipeline held up well across the board, with latency (specifically the embedding call, not the vector search) as the one clear place to optimize before a real launch.

---
*Day 21 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
