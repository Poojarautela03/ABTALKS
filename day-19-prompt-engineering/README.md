# Day 19 — Prompt Engineering for Reliable LLM Outputs

## 🎯 Objective

The goal of Day 19 was to systematically evaluate different prompt engineering techniques and identify which technique produces the most reliable LLM outputs for a RAG-based question-answering task.

## 🧠 What I Implemented

I evaluated a baseline prompt and five prompt engineering techniques on the same set of 10 diverse inputs:

1. **Baseline Prompt** — Basic question-answering instruction.
2. **Role Assignment** — Defined the model as a domain-specific assistant.
3. **Output Format Specification** — Enforced a consistent response structure.
4. **Chain-of-Thought Reasoning** — Encouraged structured reasoning before producing the answer.
5. **Few-Shot Examples** — Provided examples demonstrating the expected behavior.
6. **Negative Constraints** — Explicitly instructed the model about what it should not do.

Each version was evaluated for:

* Accuracy
* Format consistency
* Average evaluation score

## 📊 Prompt Version Tracking

A prompt version dictionary was created to store:

* Prompt version
* Average evaluation score
* Technique used
* Description of the change

This made it possible to compare the impact of each technique systematically.

## 🔍 Best Technique Analysis

After evaluating all versions, the technique with the highest average score was identified as the best-performing approach for the selected task.

The improvement was analyzed by considering how the technique affected instruction clarity, output consistency, and the model's ability to follow task-specific requirements.

## 🛡️ RAG Grounding

I also designed a grounding system prompt for the RAG assistant.

The assistant was instructed to:

* Answer only using the provided context.
* Avoid using unsupported information from its pretrained knowledge.
* Clearly refuse when the answer cannot be found in the retrieved context.

The grounding prompt was tested using **5 out-of-context questions** to check whether the model correctly refused unsupported questions instead of hallucinating answers.

## 🛠️ Technologies Used

* Python
* OpenAI API
* Prompt Engineering
* RAG
* LLM Evaluation

## 📌 Key Learning

Prompt engineering is not just about writing better instructions. It can be treated as an **experimental process** where different prompt strategies are tested, measured, and compared.

The biggest takeaway from Day 19 was that a reliable RAG system requires both **good retrieval and strong prompt-level grounding**.

---

**ABTalks 60-Day AI Challenge — Day 19**
