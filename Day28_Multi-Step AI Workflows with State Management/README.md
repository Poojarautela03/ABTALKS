# 🔄 Multi-Step AI Workflows with State Management

**Day 28 · ABTalks 60-Day AI Challenge · Focus Area: Stateful Multi-Step Agent Workflows**

> Real-world AI tasks rarely finish in a single step. Generating a research report means searching, extracting key points, synthesizing findings, and formatting output — four sequential steps where each depends on the last. If step three crashes, a naive workflow throws away steps one and two and starts over. This one doesn't.

---

## 🎯 The Problem

A single LLM call is easy to retry — if it fails, just call it again. A four-step pipeline is different: by the time step three fails, steps one and two already did real, possibly expensive, work (search calls, extraction). Restarting from scratch every time a later step fails is wasteful and, at scale, expensive.

This project builds a research workflow with **persistent state**, so a crashed run resumes from its last completed step instead of redoing everything.

## 🏗️ What's Inside

| Component | What it does |
|---|---|
| **`WorkflowState`** | Dataclass carrying topic, chunks, points, synthesis, report, and `completed_steps` |
| **4 pure step functions** | `search_sources(topic)` → `extract_key_points(chunks)` → `synthesise_findings(points)` → `format_report(synthesis)` |
| **`run_workflow()` orchestrator** | Runs the steps in order, checkpointing after each success |
| **Checkpointing** | State serialized to a JSON file named after the step, after every successful step |
| **Resume** | `resume=True` loads the most advanced checkpoint and skips already-completed steps |
| **Error handling** | A failing step logs its name + a state snapshot, writes a partial-results file, and exits cleanly — no crash |

## 🧪 Proving Resume Actually Works

Rather than just claiming resume works, the notebook **injects a real crash** into step 3 (`synthesise_findings`), inspects the checkpoint files left behind, resumes the run, and then asserts the reused `chunks` and `points` are the *same objects* recovered from disk — not silently recomputed:

```python
assert resumed_state.chunks == crashed_state.chunks
assert resumed_state.points == crashed_state.points
```

A second test does the same thing for a **genuine, non-simulated failure** (an unknown topic triggering a real `KeyError`) — confirming the orchestrator handles unplanned failures exactly the same way it handles the planned test case.

## 📊 Three Topics, One Pipeline

The workflow ran end-to-end on three deliberately different topics — Retrieval-Augmented Generation, Renewable Energy Storage, and The Byzantine Empire — to see how one fixed pipeline handles different kinds of source material.

**What stayed constant:** report *structure* — every report has the identical `# Research Report` → `## Findings` → summary → bullets → footer shape, because that shape comes from the pipeline, not the topic.

**What varied:** report *quality*, tracking source density rather than topic difficulty. The point-extraction step uses sentence length as a relevance proxy (any sentence over 40 characters counts), not real relevance ranking — a real limitation worth naming rather than glossing over. A corpus with shorter, choppier source sentences would silently produce fewer, weaker points under this same pipeline.

## ⚙️ Tech Stack

`Python` · `dataclasses` · JSON checkpointing (no external framework required for the state layer)

## 🚀 Run It Yourself

```bash
pip install jupyter nbformat
jupyter notebook Day28_Multistep_Workflow.ipynb
```

Running top to bottom reconstructs the full project (`corpus.py`, `state.py`, `steps.py`, `orchestrator.py`) via `%%writefile`, fully offline and reproducible — no API key needed, since search and synthesis are lightweight rule-based stand-ins clearly documented as swappable for real API calls without touching the orchestrator.

## 📌 Key Takeaway

> State management isn't a nice-to-have on top of a workflow — it's what turns "restart from zero on any failure" into "resume from wherever it actually broke." The steps themselves stayed pure functions; all the resilience came from a thin state layer wrapped around them.

---

🔗 Part of my **[60-Day AI Challenge with ABTalks](https://www.abtalks.in)** — building one AI project a day.
