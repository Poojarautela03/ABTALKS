# 🚀 Day 17 — Improve RAG Precision with Metadata Filtering

## 📌 Overview

Day 17 focused on improving **RAG retrieval precision** using metadata filtering.

Vector search retrieves documents based on semantic similarity, but it may return irrelevant documents because it does not consider structured information like **date, category, or document type**.

---

## 🎯 Objectives

* Add metadata: `source`, `category`, `date`, `document_type`
* Store metadata with embeddings
* Implement `filtered_retrieve()`
* Add category and date filters
* Compare filtered vs unfiltered retrieval
* Identify limitations

---

## 🔎 Metadata Example

```python
Document(
    page_content="Machine learning models...",
    metadata={
        "source": "ml_guide.pdf",
        "category": "machine_learning",
        "date": "2024-06-15",
        "document_type": "technical"
    }
)
```

---

## ⚙️ Filtered Retrieval

```python
def filtered_retrieve(query, filters=None):
    results = vectorstore.similarity_search(query, k=10)

    if not filters:
        return results

    filtered = []

    for doc in results:
        metadata = doc.metadata
        match = True

        if "category" in filters:
            match &= metadata.get("category") == filters["category"]

        if "date_after" in filters:
            match &= metadata.get("date", "") >= filters["date_after"]

        if match:
            filtered.append(doc)

    return filtered
```

### Example

```python
filters = {
    "category": "machine_learning",
    "date_after": "2024-01-01"
}

results = filtered_retrieve(
    "Recent ML techniques",
    filters
)
```

---

## 🧪 Comparison

| Retrieval       | Result                            |
| --------------- | --------------------------------- |
| Without filters | More broad/irrelevant results     |
| With filters    | More focused and relevant results |

Five queries were tested with and without metadata filters. Filtering improved relevance by restricting results to the required **category and date range**.

---

## ⚠️ Limitations

**1. Missing metadata:**
Documents with incomplete metadata may be incorrectly excluded.

**2. Conflicting categories:**
A document can belong to multiple categories, which simple equality filtering may not handle correctly.

---

## 🛠️ Tech Stack

**Python · LangChain · FAISS · OpenAI API**

---

## 💡 Key Learning

> **Vector similarity finds semantically similar documents, while metadata filtering ensures they also satisfy structured constraints.**

This makes the RAG pipeline more precise and controlled.

---

## ✅ Status

**ABTalks 60-Day AI Challenge — Day 17**
**Focus:** Advanced Retrieval with Metadata Filtering
**Status:** ✅ Completed
