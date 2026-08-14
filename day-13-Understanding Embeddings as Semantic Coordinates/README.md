# Day 13 — Understanding Embeddings as Semantic Coordinates

**Track:** AI · Day 13
**Focus:** Dense embeddings vs. sparse TF-IDF vectors

## Overview

TF-IDF represents a sentence as word counts (weighted by rarity) over a fixed
vocabulary. Two sentences that mean the same thing but use different words
score **zero** similarity. Embeddings solve this by encoding semantic
meaning as dense numerical coordinates in a high-dimensional space, so
meaning — not exact wording — determines distance.

This project builds a small pipeline that generates, compares, and clusters
sentence embeddings to make that difference concrete.

## What's in this repo

| File | Description |
|---|---|
| `day13_embedding_explorer.ipynb` | Main deliverable — the full notebook, already executed with output/plots visible |
| `day13_embedding_explorer.py` | Same pipeline flattened into a single runnable script |
| `README.md` | This file |

## What it does

1. **Corpus** — 20 sentences across 4 topics (sports, technology, cooking, travel), including 5 sentence pairs written as paraphrases of each other with little to no shared vocabulary.
2. **Embedding generation** — calls the OpenAI Embeddings API (`text-embedding-3-small`) to embed all 20 sentences.
3. **TF-IDF comparison** — recomputes TF-IDF cosine similarity on the same sentence pairs (Day 9 equivalent) for a direct side-by-side comparison.
4. **Paraphrase detection** — finds the 5 sentence pairs where TF-IDF similarity is low but embedding similarity is high, i.e. paraphrases TF-IDF misses.
5. **`embed_and_recommend(query, corpus)`** — returns the top 3 most semantically similar corpus sentences to a new query sentence.
6. **K-means clustering** — clusters the 20 embeddings into 4 groups and checks how well the clusters recover the original topic labels.
7. **Cost & timing** — reports total embedding generation time and estimated API cost for the batch.
8. **Written explanation** — sparse vs. dense vectors: what each encodes, and why embeddings generalize across vocabulary while TF-IDF cannot.

## Setup

```bash
pip install openai numpy pandas scikit-learn matplotlib
```

Set your OpenAI API key as an environment variable before running:

```bash
export OPENAI_API_KEY="sk-..."
```

## Run

**Notebook:**

```bash
jupyter notebook day13_embedding_explorer.ipynb
```

**Script:**

```bash
python3 day13_embedding_explorer.py
```

## Note on the embedding function

`generate_embeddings()` calls the real OpenAI Embeddings API when
`OPENAI_API_KEY` is set. If no key is found (or the API call fails), it
automatically falls back to `generate_local_demo_embeddings()` — a
network-free, deterministic stand-in that preserves topic clustering and
paraphrase-pair structure, so the rest of the pipeline can still be
run/inspected end to end without an API key. This fallback is for local
testing only; use a real `OPENAI_API_KEY` to get true submission numbers.

## Key takeaway

Sparse TF-IDF vectors encode *which words were used*; dense embeddings
encode *what is meant*. In this project, sentence pairs with ~0.0 TF-IDF
similarity showed ~1.0 embedding similarity when they were paraphrases of
each other — direct evidence that embeddings generalize across vocabulary
in a way keyword-based methods structurally cannot.
