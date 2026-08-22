# Day 20 — Build a Working AI Knowledge Assistant 🤖

## The story so far

Weeks one and two were all about building pieces in isolation — a chunker here, a FAISS index there, a grounding prompt in its own notebook cell. Each piece worked, but none of them had ever met each other in a real system. Day 20 is where that changes: every component gets wired together into one working service that a real user could actually call.

## What this actually is

Not a notebook that prints results — a live API. Send it a question over HTTP, and it retrieves relevant knowledge, grounds its answer in that knowledge, cites exactly where the answer came from, and honestly flags when it isn't confident. This is the first project in the challenge that behaves like a deployed product rather than an experiment.

> **Provider note:** built with **Google Gemini** (`gemini-embedding-001` + `gemini-flash-lite-latest`) instead of OpenAI, due to OpenAI API quota limits hit earlier in the challenge — same architecture either way.

## How the pieces came together

- **Day 12's chunking** splits each source document into overlapping pieces using LangChain's recursive character splitter, so no single sentence gets cut off mid-thought.
- **Day 14's FAISS search** embeds every chunk and finds the ones most semantically relevant to a query.
- **Day 17's metadata filtering** rides along on top of that search — every request can optionally constrain results by category, document type, or date, not just raw similarity.
- **Day 19's grounding prompt** takes the retrieved chunks and forces the model to answer only from what's actually there, refusing outright when nothing relevant was found.

Stacked together, that's the full pipeline behind a single `POST /ask` endpoint.

## What's new for Day 20 specifically

Two things didn't exist in any earlier day's work:

1. **Source citations** — every answer now comes back with a `sources` list naming the exact document and chunk it drew from, and the model is instructed to cite `[source_id]` tags inline in its own answer text. No more trusting a black box.
2. **A confidence indicator** — if the best similarity score across retrieved chunks falls below `0.3`, the response is flagged `low_confidence: true` and a warning gets appended directly to the answer, so a user knows when to double-check rather than trust blindly.

## Running it

The notebook builds a fictional company's knowledge base ("Nimbus Robotics," reused from earlier RAG days), starts the FastAPI server inside Colab using a background thread, and hits it with both a Python `requests` call and a real `curl` command — proving the endpoint behaves exactly like it would running on any real machine.

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Who founded Nimbus Robotics and what is the Aster-7?"}'
```

## Testing it for real

Fifteen queries went in — five easy single-fact lookups, five medium ones needing light synthesis across chunks, and five hard ones, including two deliberately unanswerable questions to test whether the system would refuse honestly instead of guessing. Each query's retrieval quality and answer quality were scored separately, because a system can retrieve the right context and still phrase a bad answer — or the reverse.

## What this day was really about

Every earlier day proved a *concept* worked. Day 20 proved a *system* worked — the difference between a component that runs in a notebook cell and one that survives being called by something outside your control. That gap is bigger than it looks on paper.

---
*Day 20 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
