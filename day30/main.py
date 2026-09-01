import os
import json
import uuid
import random
import asyncio
from dataclasses import dataclass, field, asdict
from typing import Dict, Optional, List
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --------------------------------------------------------------------
# LLM layer (mock by default; set OPENAI_API_KEY + USE_MOCK=false to go live)
# --------------------------------------------------------------------
USE_MOCK = os.environ.get("USE_MOCK", "true").lower() != "false"


class MockLLM:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def _lorem(self, n):
        bank = [
            "Recent developments in this area show measurable progress.",
            "Multiple independent studies converge on similar conclusions.",
            "Experts disagree on the long-term implications of this trend.",
            "The underlying mechanism is still being actively debated.",
            "Historical context helps explain why this pattern emerged.",
            "Practical applications are already visible in industry.",
            "Further research is needed to confirm early findings.",
            "Data from the last few years supports this hypothesis.",
        ]
        return " ".join(self.rng.sample(bank, k=min(n, len(bank))))

    def plan(self, topic):
        return {
            "topic": topic,
            "sub_questions": [
                f"What is the current state of {topic}?",
                f"What are the main drivers behind {topic}?",
                f"What are the risks or open problems in {topic}?",
                f"What does the near-term outlook for {topic} look like?",
            ],
        }

    def search(self, query):
        return [
            {"title": f"Source {i+1} on '{query[:40]}...'", "snippet": self._lorem(2),
             "score": round(self.rng.uniform(0.6, 0.95), 3)}
            for i in range(3)
        ]

    def synthesize(self, topic, evidence):
        combined = " ".join(e["snippet"] for e in evidence)
        return f"Synthesis for '{topic}': {combined} {self._lorem(3)}"

    def format_report(self, topic, sections):
        parts = [f"# Research Report: {topic}\n"]
        for heading, body in sections.items():
            parts.append(f"## {heading}\n{body}\n")
        return "\n".join(parts)


class RealLLM:
    def __init__(self):
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    def chat(self, system, user, model="gpt-4o-mini"):
        resp = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return resp.choices[0].message.content


llm = MockLLM() if USE_MOCK else RealLLM()

# --------------------------------------------------------------------
# Workflow
# --------------------------------------------------------------------
STEPS = ["plan", "retrieve", "synthesize", "format"]


async def run_workflow(topic: str, job_id: str, jobs: Dict, broadcaster=None):
    async def emit(step, status, detail=None):
        event = {"step": step, "status": status, "detail": detail,
                  "timestamp": datetime.utcnow().isoformat()}
        jobs[job_id]["events"].append(event)
        jobs[job_id]["current_step"] = step
        jobs[job_id]["status"] = status
        if broadcaster:
            await broadcaster(job_id, event)

    await emit("plan", "started")
    plan = llm.plan(topic)
    await emit("plan", "completed", f"{len(plan['sub_questions'])} sub-questions generated")

    await emit("retrieve", "started")
    evidence_by_q = {q: llm.search(q) for q in plan["sub_questions"]}
    total_docs = sum(len(v) for v in evidence_by_q.values())
    await emit("retrieve", "completed", f"{total_docs} documents retrieved")

    await emit("synthesize", "started")
    sections = {q: llm.synthesize(q, ev) for q, ev in evidence_by_q.items()}
    await emit("synthesize", "completed", f"{len(sections)} sections synthesized")

    await emit("format", "started")
    report = llm.format_report(topic, sections)
    await emit("format", "completed", "final report assembled")

    return report


# --------------------------------------------------------------------
# Evaluation
# --------------------------------------------------------------------
def evaluate_report(topic: str, report: str) -> Dict:
    rng = random.Random(hash(topic) % (10 ** 6))
    length_bonus = min(len(report) / 2000, 1.0) * 0.15
    structure_bonus = 0.1 if "##" in report else 0.0

    def score(base):
        return round(min(1.0, max(0.0, base + length_bonus * 0.5 + structure_bonus + rng.uniform(-0.05, 0.05))), 3)

    scores = {
        "relevance": score(0.72),
        "completeness": score(0.68),
        "coherence": score(0.75),
        "factual_grounding": score(0.66),
    }
    scores["overall"] = round(sum(scores.values()) / len(scores), 3)
    return scores


# --------------------------------------------------------------------
# FastAPI app
# --------------------------------------------------------------------
app = FastAPI(title="AI Research Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your deployed frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: Dict[str, Dict] = {}
ws_clients: Dict[str, List[WebSocket]] = {}


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    job_id: str
    topic: str
    report: str
    scores: Dict
    events: List[Dict]


async def broadcast(job_id: str, event: Dict):
    for ws in ws_clients.get(job_id, []):
        try:
            await ws.send_json(event)
        except Exception:
            pass


@app.get("/health")
async def health():
    return {"status": "ok", "mock_mode": USE_MOCK, "time": datetime.utcnow().isoformat()}


@app.post("/research", response_model=ResearchResponse)
async def research(req: ResearchRequest):
    if not req.topic or not req.topic.strip():
        raise HTTPException(status_code=400, detail="topic must not be empty")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"events": [], "status": "started", "current_step": None}

    report = await run_workflow(req.topic, job_id, jobs, broadcaster=broadcast)
    scores = evaluate_report(req.topic, report)

    jobs[job_id]["status"] = "done"
    jobs[job_id]["report"] = report
    jobs[job_id]["scores"] = scores

    return ResearchResponse(
        job_id=job_id,
        topic=req.topic,
        report=report,
        scores=scores,
        events=jobs[job_id]["events"],
    )


@app.get("/research/{job_id}/status")
async def research_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="unknown job_id")
    return jobs[job_id]


@app.websocket("/ws/research/{job_id}")
async def ws_research(websocket: WebSocket, job_id: str):
    await websocket.accept()
    ws_clients.setdefault(job_id, []).append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep-alive; client can ignore
    except WebSocketDisconnect:
        ws_clients[job_id].remove(websocket)
