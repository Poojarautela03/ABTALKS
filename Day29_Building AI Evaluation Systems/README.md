# Day 29 — Building AI Evaluation Systems 🤖📊

**ABTalks 60-Day AI Challenge | Focus Area: AI Evaluation & Measurement**

> You cannot improve what you cannot measure.

For Day 29, I built an **automated AI evaluation framework** for a Day 20-style knowledge assistant. The goal was to move from subjective checking of AI responses to a measurable evaluation and regression-testing workflow.

The framework evaluates every response across three dimensions:

* **Groundedness** — Is the answer supported only by the retrieved context, without fabricated information?
* **Correctness** — Does the answer match the manually verified ground-truth answer?
* **Completeness** — Does the answer address the entire question without missing important information?

The notebook contains a 20-question evaluation suite and automatically identifies weaknesses in the assistant.

---

## 🚀 What I Built

### 1. 20-Question Evaluation Dataset

Created a manually labelled evaluation dataset containing:

* 20 questions
* Ground-truth answers
* Key points required for a complete answer
* 2 questions per knowledge-base document

The dataset covers topics including:

* Python
* Eiffel Tower
* Mount Everest
* Amazon rainforest
* Apollo 11
* Recursion
* Gradient Descent
* Neural Networks
* REST APIs
* Binary Search

The assistant intentionally contains several realistic errors so that the evaluation framework can demonstrate that it actually detects regressions.

---

## ⚖️ Evaluation Dimensions

### Groundedness

Checks whether the generated answer is supported by the retrieved context and detects fabricated additions.

### Correctness

Compares the generated response against the known ground-truth answer.

### Completeness

Checks whether the important labelled key points required to answer the question are present.

Each dimension receives a score from **1–5**.

---

## 🧠 `llm_judge()`

The core evaluation function follows:

```python
llm_judge(
    question,
    context,
    answer,
    ground_truth
)
```

It returns:

```python
{
    "groundedness": score,
    "correctness": score,
    "completeness": score
}
```

The notebook currently uses a deterministic offline heuristic implementation for reproducibility. It is designed so that a GPT-4o-mini structured-output judge can replace the heuristic without changing the rest of the evaluation pipeline.

---

## 📊 Evaluation Results

The assistant was evaluated across all 20 questions.

| Dimension    | Average Score |
| ------------ | ------------: |
| Groundedness |  **4.35 / 5** |
| Correctness  |  **4.55 / 5** |
| Completeness |  **4.50 / 5** |

### Lowest-performing dimension

**Groundedness — 4.35/5**

It was **0.15 points below correctness**, the next-lowest dimension.

The evaluation successfully surfaced fabricated information and incorrect facts, while also showing that qualitative hallucinations can be harder for a simple automated judge to detect.

---

## 🔄 Regression Testing

I implemented:

```python
regression_test_runner(answer_fn)
```

The runner:

1. Loads a stored baseline.
2. Runs the complete 20-question evaluation suite.
3. Calculates current aggregate scores.
4. Compares current scores with the baseline.
5. Checks whether any dimension drops beyond the threshold.
6. Returns **PASS** or **FAIL**.

The configured regression threshold is:

```python
REGRESSION_THRESHOLD = 0.15
```

This makes the evaluation suitable as a pre-deployment quality gate.

### Regression demonstration

The unchanged assistant passed:

```text
Overall: PASS
```

A deliberately broken assistant produced:

```text
groundedness   | 4.350 → 3.900 | -0.450 | FAIL
correctness    | 4.550 → 4.000 | -0.550 | FAIL
completeness   | 4.500 → 3.600 | -0.900 | FAIL

Overall: FAIL
```

The regression runner therefore detected the degradation and would block deployment.

---

## ⚠️ Limitations of LLM-as-Judge

Automated evaluation is powerful, but it is not perfect.

### 1. Paraphrasing can be difficult

Lexical-overlap approaches can incorrectly penalize valid answers that express the same idea using different wording.

### 2. Different hallucinations can be detected differently

The evaluation handled fabricated numbers more reliably than fabricated descriptive claims. This means a groundedness score should not automatically be interpreted as perfect hallucination detection.

### 3. The evaluation system itself can contain bugs

During development, bugs in retrieval and number extraction produced incorrect evaluation behaviour. This demonstrated that the evaluation harness itself needs testing and sanity checks.

### 4. Human evaluation is still important

Automated evaluation is less reliable for:

* Tone
* Pedagogical quality
* Subjective answers
* Open-ended questions
* Whether a summary preserves the intended emphasis
* Overall answer quality

Human review is still necessary for these cases.

---

## 🛠️ Tech Stack

* Python
* OpenAI API / GPT-4o-mini compatible judge interface
* Retrieval-based knowledge assistant
* JSON
* Automated regression testing

---

## 📁 Project Structure

```text
Day29_Building_AI_Evaluation_Systems/
│
├── Evaluation_Systems_(1).ipynb
├── knowledge_base.py
├── assistant.py
├── eval_dataset.py
├── judge.py
├── regression.py
├── assistant_broken.py
└── baseline_scores.json
```

---

## 🎯 Key Learning

The biggest lesson from this project was that **building an AI system is only half the job — measuring whether it remains reliable is equally important.**

Instead of asking:

> "Does this response look good?"

I can now ask:

> "Did the system's groundedness, correctness, or completeness score regress compared with the previous version?"

This turns AI quality from a subjective judgement into an **engineering feedback loop**.

---


**Challenge:** ABTalks 60-Day AI Challenge — Day 29
