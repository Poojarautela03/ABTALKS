# Day 27 — Structured Tool Calling with the OpenAI Functions API

Part of a 30-day AI build challenge. Day 26 built a manual ReAct agent that parsed tool calls out of raw LLM text with regex. This project rebuilds that agent using OpenAI's function-calling API — where the model returns structured JSON instead of free text — and measures the reliability difference directly.

## What's inside

- **4 tool schemas** in OpenAI function-calling format: `search_documents`, `get_weather_stub`, `calculate`, `get_today`
- **Day 26 recap agent** — the original regex-based text parser, plus 3 realistic formatting-drift inputs that break it
- **Day 27 agent** — a structured tool-calling loop that sends the schemas to the model, executes matching Python functions on `tool_calls`, and loops until a final text response
- **Five-problem comparison** — the same multi-step questions from Day 26, run through both agents, checked for matching tool selection and final answers
- **Two-sequential-tool-call trace** — a question requiring `search_documents` → `calculate`, with the full exchange printed
- **Argument validation wrapper** — catches 3 concrete cases of the model passing incorrect or missing arguments (bad enum value, malformed expression, missing required field) before they reach the tool function
- **FastAPI `/agent` endpoint** — accepts a question, returns the final answer plus the complete list of tool calls made
- **Reliability comparison document** — a written breakdown of exactly where structured calling helps (formatting reliability) and where it doesn't (semantic argument correctness still needs validation)

## Files

| File | Purpose |
|---|---|
| `Day27_Structured_Tool_Calling.ipynb` | Full notebook — tools, both agents, comparisons, validation, API demo, write-up |
| `agent_api.py` | Standalone FastAPI app exposing `POST /agent` |

## Running it

```bash
pip install openai fastapi uvicorn jupyter
jupyter notebook Day27_Structured_Tool_Calling.ipynb
```

By default the notebook runs fully offline against a deterministic mock client that mirrors the real OpenAI response shape (`choices[0].message.tool_calls[i].function.{name, arguments}`), so every cell executes without an API key.

To run it against the live API instead:

```bash
export OPENAI_API_KEY=sk-...
jupyter notebook Day27_Structured_Tool_Calling.ipynb
```

The notebook's `OpenAIClientAdapter` detects the key automatically and switches from the mock to `openai.OpenAI().chat.completions.create(...)` with no code changes needed.

To run the API server standalone:

```bash
uvicorn agent_api:app --reload
curl -X POST http://localhost:8000/agent -H "Content-Type: application/json" \
  -d '{"question": "What'\''s the per-person budget share for Project Alpha?"}'
```

## Key finding

Structured function calling doesn't make the model choose *better* arguments — it can still pass a syntactically valid but semantically wrong value (e.g. `unit="kelvin"`). What it eliminates is the entire class of *formatting* failures from Day 26's text parser: missing keywords, wrong brackets, unquoted strings, positional args. That shrinks the reliability problem from "does the model's free text match my regex" down to "does the model's chosen value pass my validator" — a much smaller, testable surface, especially as tool chains get longer.

## Stack

Python · OpenAI API (function calling) · FastAPI
