# 🏗️ AI System Architecture Review and Refactoring

**Day 25 · ABTalks 60-Day AI Challenge · System Design Review**

> Two weeks of shipping fast leaves every AI system the same way: functional, but structurally messy. This is the day that pays down the debt — no new features, just making the existing system cleaner, safer, and easier to extend.

---

## 🎯 The Problem

By Day 20, the AI Knowledge Assistant worked — chunking, retrieval, grounded prompts, source citations, a live FastAPI endpoint. But "working" and "well-built" aren't the same thing. Hardcoded values, duplicated logic, and untested code paths had quietly piled up under the hood.

This project is a dedicated audit-and-refactor pass on that codebase.

## 🔍 What the Audit Found

| # | Issue | Where it lived |
|---|---|---|
| 1 | **Hardcoded configuration** — API key, chunk size, model name, thresholds mixed into logic | Module-level constants |
| 2 | **Triplicated validation logic** — the same empty-query check copy-pasted 3 times | `retrieve()`, `validate_input()`, `ask_endpoint()` |
| 3 | **Magic numbers duplicated instead of reusing config** | `500` and `3` hardcoded again despite existing constants |
| 4 | **Zero type hints or docstrings** — no discoverable function contracts | Every function |
| 5 | **A config value that silently did nothing** — `SIMILARITY_THRESHOLD` existed but was never enforced, so irrelevant chunks reached the LLM | `retrieve()` |
| 6 | **Zero tests** — none of the above was ever caught automatically | Whole file |

## 🛠️ What Got Fixed — Carefully

- **All config extracted** to `.env` / `config.py`, loaded once via `python-dotenv` into an immutable `Settings` object
- **Validation logic** now lives in exactly one place
- **Every function** typed and documented
- **Split into a clean `core/` package**: `validator.py`, `retriever.py`, `prompt_builder.py`, `llm_client.py`, `assistant.py`
- **10 pytest tests** — 5 run against the *original* code (before checkpoint), 5 equivalent tests against the *refactored* code (after checkpoint) — all pass

## ⚠️ The Bug That Almost Snuck In

The audit surfaced a real bug: the similarity threshold was never actually applied, so low-relevance chunks were reaching the LLM as if they mattered. Fixing it felt like the obvious move — until it broke **13 of 15** outputs in the regression check below.

That's the core lesson of this exercise: **a refactor and a bug fix are two different kinds of change.** The fix got logged as a documented follow-up instead of smuggled into a "just cleanup" commit — because a refactor's only job is to change *how* the code works, never *what* it does.

## ✅ Proof Nothing Broke

Every one of the 15 test queries from Day 20 was re-run against the refactored code and diffed field-by-field against the pre-refactor baseline:

```
15/15 queries → byte-for-byte identical output
```

Same answers. Same sources. Same confidence scores. Structural cleanup, zero behavior change — exactly what a refactor is supposed to be.

## ⚙️ Tech Stack

`Python` · `FastAPI` · `pytest` · `python-dotenv` · `matplotlib`
<img width="1089" height="740" alt="image" src="https://github.com/user-attachments/assets/230a9781-951e-4219-8d72-d0a4f2777c8d" />


## 🚀 Run It Yourself

```bash
pip install fastapi pytest python-dotenv matplotlib jupyter nbformat
jupyter notebook Day25_Architecture_Review.ipynb
```

Running the notebook top to bottom reconstructs the entire project structure — `.env`, `config.py`, the `core/` package, and both test files are written to disk via `%%writefile` as the notebook runs.

## 📌 Key Takeaway

> Refactoring isn't "make the code nicer while I'm in here." It's a scoped, verifiable claim: *the behavior is provably unchanged.* Tests before, tests after, and a query-by-query diff are what turn that claim into something you can actually trust — not just say.

---

🔗 Part of my **[60-Day AI Challenge with ABTalks](https://www.abtalks.in)** — building one AI project a day.
