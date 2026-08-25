# Day 23 — Connect a Frontend to Your AI Backend 🖥️

A minimal but fully functional Next.js chat interface connected to the Day 22 FastAPI backend — the piece that turns the AI assistant from an engineer-only curl demo into something a non-technical person could actually use.

## 🎯 Objective

A backend that only responds to raw HTTP requests isn't a product. This task builds the missing frontend layer: a chat UI with real streaming, formatted markdown, source citations, and honest loading/error states.

## 🏗️ Approach

- Built with **Next.js + React**, connecting to the Day 22 FastAPI `/ask` and `/ask/stream` endpoints
- **Persistent conversation history** — held in React state, so multi-turn conversation survives without a page refresh
- **Streaming response rendering** — uses the Fetch API's `ReadableStream` to read the `/ask/stream` response body chunk by chunk, so tokens appear progressively instead of all at once
- **Markdown rendering** via `react-markdown` + `remark-gfm` — headings, bold text, code blocks, and bullet lists render correctly instead of showing raw `**`/backtick characters
- **Collapsible source citations** — a `<details>` panel under each assistant response listing the document title, chunk ID, and similarity score for every source used
- **Loading state** — a typing indicator (animated dots) shown while the request is in flight, before the first streamed token arrives
- **Error state** — the backend's structured error codes (`INPUT_INVALID`, `RETRIEVAL_FAILURE`, `LLM_TIMEOUT` from Day 22) are mapped to clear, human-readable messages instead of a raw JSON dump
- **Mobile-responsive layout** — verified in Chrome DevTools device emulation at 375px width, with no horizontal scrolling and a 16px input font size to prevent iOS auto-zoom on focus

## 🧩 Project structure

```
nimbus-chat/
├── app/
│   ├── layout.js       # root layout, imports global styles
│   ├── page.js          # main chat page — state, streaming logic, UI
│   └── globals.css      # base + markdown + mobile-responsive styles
├── components/
│   ├── MessageBubble.js     # renders one message, markdown + sources
│   ├── SourceCitations.js   # collapsible source panel
│   ├── TypingIndicator.js   # loading state
│   └── ErrorMessage.js      # human-readable error mapping
├── package.json
├── next.config.js
└── .env.local.example
```

## ▶️ Running it locally

1. Make sure the Day 22 FastAPI backend is running (`uvicorn app:app --reload`, listening on `http://127.0.0.1:8000`)
2. `npm install`
3. `cp .env.local.example .env.local`
4. `npm run dev`
5. Open `http://localhost:3000`

## 🧪 Testing checklist

- [x] Typing a query shows the loading indicator immediately
- [x] Streamed tokens appear progressively, not all at once
- [x] Markdown (bold, lists, code blocks) renders correctly
- [x] Source citations appear in a collapsible section below each answer
- [x] Conversation history persists across multiple turns without a page refresh
- [x] Sending an invalid query (e.g. under 5 characters) shows a clear message, not raw JSON
- [x] Verified at 375px width in Chrome DevTools — no horizontal scroll, input box sized correctly, text readable

## 💡 Key Learning

An AI system that only works via curl is a demo for engineers, not a product. The gap between the two is almost entirely in the details that don't show up in an API response: showing progress while something is loading, rendering formatted text instead of raw markdown symbols, translating a structured error code into a sentence a person can actually understand, and making sure none of it breaks on a small screen. None of that logic lives in the model — it's all in how the interface treats the person using it.

---
*Day 23 of the ABTalks 60-day AI challenge — Artificial Intelligence track*
