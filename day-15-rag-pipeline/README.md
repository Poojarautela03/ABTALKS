# Day 15 — Build Your First RAG Pipeline 🤖📚

As part of my **ABTalks 60-Day AI Challenge**, Day 15 focused on building my first **Retrieval-Augmented Generation (RAG)** pipeline.

The goal was to understand how retrieval can provide an LLM with relevant external context before generating an answer, helping it produce responses grounded in a specific knowledge base.

---

## 🎯 Objective

Build a complete RAG pipeline that connects:

**User Query → Semantic Retrieval → Relevant Documents → LLM → Grounded Answer**

The project also compares the RAG approach with a normal LLM call to understand the difference between:

- ❌ Generation without retrieved context
- ✅ Generation with retrieved context

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique that combines information retrieval with text generation.

Instead of asking an LLM to answer a question only from its training knowledge, RAG first searches a knowledge base for relevant information.

The retrieved information is then added to the LLM prompt as **context**.

### Basic Flow

```text
User Query
    ↓
Convert Query into Embedding
    ↓
Semantic Search
    ↓
Retrieve Top 3 Relevant Documents
    ↓
Add Documents as Context
    ↓
Send Context + Query to LLM
    ↓
Generate Grounded Answer
