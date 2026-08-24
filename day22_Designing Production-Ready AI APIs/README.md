# Day 22 — Designing Production-Ready AI APIs 🛡️

Redesigns the Day 20 endpoint into a production-grade API — the difference between "it works when I call it correctly" and "it behaves predictably when it doesn't."

## 🎯 Objective

AI APIs face failure modes standard REST APIs don't: flaky upstream LLM calls, requests that hang indefinitely, and expensive operations that need to be rejected before they ever reach the model. This task adds proper validation, structured error handling, retry logic, streaming, and timeout protection to the Day 20 pipeline.

## 🏗️ Approach

- Note: used **Google Gemini** (`gemini-embedding-001` + `gemini-flash-lite-latest`) instead of OpenAI due to API quota limits — the retry/backoff logic targets the same `429` rate-limit failure mode OpenAI's API produces
- **Pydantic models with field validators** — `AskRequest` rejects queries under 5 characters, over 1000 characters, or made up entirely of whitespace/symbols, each with a clear validation message and schema examples
- **Retry with exponential backoff** — `call_llm_with_retry()` retries transient/rate-limit errors with delays that double each attempt (2s → 4s → 8s → 16s), up to a configurable max
- **Streaming responses** — a second endpoint, `/ask/stream`, streams generated text as it arrives instead of waiting for the full response, using FastAPI's `StreamingResponse`
- **15-second timeout guard** — the full pipeline runs in a thread pool with a hard timeout; if it doesn't complete in time, the request fails fast with a structured error instead of hanging
- **Three structured error codes**, each with a consistent `{code, message, request_id}` shape:
  - `INPUT_INVALID` (400) — validation failure
  - `RETRIEVAL_FAILURE` (502) — the retrieval step itself throws
  - `LLM_TIMEOUT` (504) — the pipeline exceeds the timeout window

## 🧪 Verification

Every error path was deliberately triggered and its response printed to confirm correctness:
1. Query too short (`"hi"`) → `400 INPUT_INVALID`
2. Query too long (1001 characters) → `400 INPUT_INVALID`
3. Whitespace/symbols only (`"!!!   ???"`) → `400 INPUT_INVALID`
4. Forced timeout (patched to 0.01s to avoid a real 15s wait) → `504 LLM_TIMEOUT`
5. Forced retrieval failure (simulated index corruption) → `502 RETRIEVAL_FAILURE`
6. A normal valid request, confirmed still working correctly after all error tests ran

The streaming endpoint was also tested directly, confirming text arrives incrementally rather than all at once.

## 💡 Key Learning

Most of the actual engineering effort in a "simple" API endpoint isn't the happy path — it's everywhere the happy path breaks. A validator that silently accepts garbage input, an LLM call with no retry logic, or a request with no timeout will all work fine in a demo and then fail unpredictably the first time something upstream hiccups. Structured, consistent error codes turn those failures from mysterious 500s into something a client application can actually catch and handle gracefully.

---
*Day 22 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
