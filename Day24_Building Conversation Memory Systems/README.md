# 🧠 Building Conversation Memory Systems

**Day 24 · ABTalks 60-Day AI Challenge · Stateful AI Conversations**

> LLMs forget everything the moment an API call ends. This project builds the memory layer that makes multi-turn conversation possible — the difference between an assistant that understands *"explain it more simply"* and one that just asks *"explain what?"*

---

## 🎯 The Problem

Every call to an LLM API is stateless — the model has zero awareness of anything said one message ago. Real assistant products need to remember, but sending the *entire* conversation history on every turn is expensive and eventually breaks the token limit.

This project builds a lightweight memory system that solves both problems at once: it remembers enough to hold a real conversation, and forgets *smartly* enough to stay cheap.

## 🏗️ What's Inside

| Component | What it does |
|---|---|
| **`ConversationHistory`** | Stores each session's messages and exposes `append()`, `get_context()`, `clear()` |
| **FastAPI `/chat` endpoint** | Accepts a `session_id`, maintains one conversation per session server-side |
| **Context injection** | Only the last **5 turns** are sent per prompt — enough memory, not enough to blow the budget |
| **Memory truncation** | Past 10 turns, the oldest 5 are auto-summarized by an LLM call and folded into a lightweight summary |
| **5-turn pronoun test** | Proves it works: *"give an example of **it**"* only resolves correctly when memory is on |
| **Token cost analysis** | Real numbers on what memory costs — per turn and per month, at scale |

## 🧪 The Experiment

The same 5-question conversation is run twice — once *with* memory, once *without*:

```
Turn 1 → "Can you explain recursion?"
Turn 2 → "What is a base case?"
Turn 3 → "Can you give me an example of it?"        ⟵ needs memory
Turn 4 → "How is that different from a loop?"        ⟵ needs memory
Turn 5 → "Explain it more simply."                   ⟵ needs memory
```

**Without memory**, the model hits a wall on turn 3 — it has no idea what *"it"* means.
**With memory**, it correctly resolves every pronoun and builds a coherent answer across all 5 turns.

That gap *is* the product.

## 💰 What Memory Actually Costs

Memory isn't free — every stored turn gets re-sent (and re-billed) as input on every future call, until it's pushed out of the window or compressed by truncation.

At **1,000 daily users × 10 turns/session**, a 5-turn memory window adds roughly:

- **+760 input tokens per turn** vs. a stateless call
- **+$57/month** (~61% increase) over a fully stateless baseline

The takeaway: memory buys the ability to hold a real conversation, but the window size is a dial — not a switch — and it's worth tuning deliberately rather than defaulting to "remember everything."

## ⚙️ Tech Stack

`Python` · `FastAPI` · `Pydantic` · `tiktoken` · OpenAI-compatible LLM client (pluggable — runs offline on a deterministic mock by default, or live on GPT models by setting `OPENAI_API_KEY`)

## 🚀 Run It Yourself

```bash
pip install fastapi tiktoken jupyter nbformat
jupyter notebook Day24_Conversation_Memory.ipynb
```

No API key needed to see it run end-to-end — the notebook ships with an offline mock LLM for reproducibility. Set `OPENAI_API_KEY` to switch it to live GPT calls with zero code changes.

## 📌 Key Takeaway

> Conversation memory isn't just "keep a chat log." It's a design problem with a real cost curve — balancing *how much the model remembers* against *how much it costs to remind it.* Getting that balance right is what separates a demo from a production assistant.

---

🔗 Part of my **[60-Day AI Challenge with ABTalks](https://www.abtalks.in)** — building one AI project a day.
