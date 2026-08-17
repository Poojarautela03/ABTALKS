# Day 15 — Build Your First RAG Pipeline 🤖📚

Built my first **Retrieval-Augmented Generation (RAG) pipeline** by connecting my Day 14 semantic search engine to an LLM.

## 🎯 Objective

Understand how RAG retrieves relevant documents first and provides them as context to an LLM before generating an answer.

## 🏗️ Approach

- Connected the Day 14 **FAISS-based semantic search engine** to an OpenAI LLM
- Built `generate_with_rag(query)` to retrieve the top 3 relevant chunks and generate a grounded answer
- Built `generate_without_rag(query)` as a baseline without retrieved context
- Used a structured prompt separating the retrieved context from the user's question
- Tested both approaches on 5 queries based on custom knowledge-base information
- Compared the responses side by side
- Analyzed 2 failure cases where RAG still produced an incorrect answer
- Created a complete RAG architecture diagram showing the flow from query to final response

## 📊 Findings

**RAG improved grounding** for questions based on custom knowledge that was not available in the model's normal context.

Without RAG:

```text
User Query → LLM → Answer

With RAG:

User Query
    ↓
Semantic Search
    ↓
Top 3 Relevant Documents
    ↓
Context + Query
    ↓
LLM
    ↓
Grounded Answer

💡 Key Takeaway

RAG combines retrieval + generation:

Documents
    ↓
Embeddings
    ↓
FAISS Vector Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Final Answer

RAG is useful for working with custom and domain-specific information such as company documents, research papers, knowledge bases, and private data.

Day 15 of the ABTalks 60-day AI challenge — Artificial Intelligence track
