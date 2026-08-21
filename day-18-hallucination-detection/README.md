# Day 18 — Why LLMs Hallucinate and How to Measure It 🔬

Built a hallucination measurement experiment comparing an LLM's accuracy with and without RAG grounding, plus a four-signal automated hallucination detector.

## 🎯 Objective

Hallucination isn't a random bug — it's a predictable consequence of language models predicting the next likely token rather than retrieving verified facts. This experiment quantifies how often and why a model fabricates information, and tests whether RAG measurably reduces it.

## 🏗️ Approach

- Note: used **Google Gemini** (`gemini-3.6-flash` + `gemini-embedding-001`) instead of OpenAI's GPT-4o-mini due to API quota limits — same methodology, different provider
- Built a 20-question dataset with known ground-truth answers across 4 domains: history, science, geography, and technology
- Deliberately included 2 questions about fictional companies to reliably test fabrication under pressure
- Defined explicit scoring criteria *before* evaluating any response: **correct**, **partially correct**, or **hallucinated** — with hallucinations further split into fabricated facts, outdated information, confident wrong answers, and plausible-but-unverifiable claims
- Ran all 20 questions with no context/retrieval, logging every response verbatim
- Ran the same 20 questions through a RAG pipeline (reusing the Day 15 architecture) with a knowledge base covering both the real facts and the two fictional companies
- Calculated and compared hallucination rate percentages between the two conditions

## 🔍 Four-Signal Hallucination Detector

Built a rule-based detector combining four independent checks on every RAG response:

1. **Unsupported claim detection** — flags any number, date, or named entity in the response absent from the retrieved context
2. **Retrieval overlap check** — computes Jaccard similarity between response and retrieved chunks; flags responses below 0.15 overlap
3. **Contradiction detection** — a secondary LLM call asking whether the response contradicts the provided context
4. **Citation absence check** — flags factual-sounding responses that never reference any retrieved content

The four signals combine into a confidence score (1.0 = no flags, 0.0 = all four flagged), with a full per-response breakdown logged to `hallucination_detector_results.json`.

## 📊 Results

- **No-context hallucination rate:** [fill in with your actual percentage]
- **RAG hallucination rate:** [fill in with your actual percentage]
- **Reduction:** [fill in the percentage-point difference]

[Add 1-2 sentences on your most interesting specific example — e.g. how the model handled the fictional "Nimbus Robotics" and "Zylotech Dynamics" questions differently with and without RAG.]

## 💡 Key Learning

Hallucination isn't random — it's what a next-token predictor does by default when it has no grounding to fall back on. RAG doesn't eliminate the risk, but it gives the model something real to anchor to, measurably reducing fabrication. The four-signal detector also shows that catching hallucination doesn't require a single perfect test — combining cheap, independent signals (word overlap, entity checking, a contradiction check) catches more failure patterns than trusting any one method alone.

---
*Day 18 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
