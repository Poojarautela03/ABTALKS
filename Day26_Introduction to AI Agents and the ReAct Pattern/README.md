# 🤖 Introduction to AI Agents and the ReAct Pattern

**Day 26 · ABTalks 60-Day AI Challenge · Focus Area: AI Agents**

> A standard LLM answers a question in one step. An agent plans, uses tools, observes results, and decides what to do next — autonomously. The only way to really understand where that autonomy holds up and where it quietly breaks is to build the loop by hand, with no framework hiding the mechanics.

---

## 🎯 The Problem

Frameworks like LangChain make agents feel like magic — a few lines of config and suddenly the model is "using tools." That magic hides exactly the part worth understanding: how does an LLM's text output actually turn into a function call, and what happens when that reasoning goes wrong?

This project builds the **ReAct pattern** (Reason + Act) manually, from scratch, no framework:

```
Thought      → the model reasons about what it needs next
Action       → it names a tool and an input
Observation  → the tool actually runs, its real output is fed back in
...repeat...
Final Answer → the model has enough to answer
```

## 🛠️ What's Inside

| Component | What it does |
|---|---|
| **`calculator()`** | Safely evaluates arithmetic via Python's `ast` module — no `eval()`, no reachable builtins |
| **`search_docs()`** | Bag-of-words retrieval over a small knowledge base |
| **`get_today()`** | Returns today's real date |
| **`tool_registry` + `dispatch()`** | Maps action names to functions; unknown tools return an error string, not a crash |
| **The manual ReAct loop** | Fully generic — would work unchanged with a real LLM behind it |
| **5 multi-step problems** | Each requires 2+ tools used in sequence, full trace printed for every step |

## 🔍 The Failures — Caught by Code, Not Just Prose

Three of the five problems were run against a script designed to actually fail, and each failure is caught by an **automated detector**, not just a written observation:

- **Wrong tool selected** — the agent reaches for the calculator on a question that needs facts looked up first, gets an `ERROR:` back, and self-corrects to `search_docs`.
- **Looping without progress** — an unanswerable question (no data, no matching tool) triggers three near-identical searches in a row, all returning nothing. No new information gained between attempts.
- **Hallucinated result** — the most dangerous one. The calculator correctly returns **2,123,000**. The Final Answer states **2,715,500** — a number that appears nowhere in the trace. Read top to bottom, this trace looks completely normal. Only checking the final number against the real tool output catches it.

## 💡 What Makes an Agent Reliable

> An agent is reliable in proportion to how mechanically its next step follows from the last tool's real output — and unpredictable in exactly the gaps where that link is implicit instead of enforced.

The wrong-tool and looping failures are visible just by reading the trace. The hallucination isn't — it only shows up in the *gap* between the last Observation and the Final Answer, which is exactly the part people are least likely to double-check once the earlier steps look fine. That's the real argument for keeping the full trace instead of just the answer.

## ⚙️ Tech Stack

`Python` · deterministic offline mock LLM (swappable for the OpenAI API with zero changes to the loop itself)

## 🚀 Run It Yourself

```bash
pip install jupyter nbformat
jupyter notebook Day26_ReAct_Agent.ipynb
```

No API key needed — the notebook reconstructs the full project (`tools.py`, `registry.py`, `llm.py`, `agent.py`) via `%%writefile` as it runs, fully offline and reproducible.

## 📌 Key Takeaway

> The failure that matters most in an agent isn't the one that crashes loudly. It's the one that looks the most like success.

---

🔗 Part of my **[60-Day AI Challenge with ABTalks](https://www.abtalks.in)** — building one AI project a day.
