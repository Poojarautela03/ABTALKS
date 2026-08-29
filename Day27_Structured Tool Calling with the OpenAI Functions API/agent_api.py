"""
Day 27 FastAPI agent endpoint.
Run with:  uvicorn agent_api:app --reload
"""
import json
import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 27 Function-Calling Agent")


class AgentRequest(BaseModel):
    question: str


class AgentResponse(BaseModel):
    answer: Optional[str]
    tool_calls: list


@app.post("/agent", response_model=AgentResponse)
def agent_endpoint(req: AgentRequest):
    """
    Runs the structured function-calling agent loop for the given question
    and returns the final answer plus every tool call made along the way.

    NOTE: import the loop, client, and tool schemas defined in the notebook /
    a shared module (agent_core.py) when running this as a standalone service.
    """
    from agent_core import run_day27_agent, OpenAIClientAdapter, SCRIPT
    client = OpenAIClientAdapter(SCRIPT)
    answer, trace = run_day27_agent(req.question, client)
    tool_calls = [t for t in trace if "tool_call" in t]
    return AgentResponse(answer=answer, tool_calls=tool_calls)
