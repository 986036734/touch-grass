"""Minimal agentic loop over any OpenAI-compatible chat endpoint.

Works with:
  - local Ollama (OPENAI_BASE_URL=http://localhost:11434/v1, any model name)
  - any OpenAI-compatible gateway serving open-weight models
No vendor SDK required — plain `requests`.
"""
import json
import os

import requests

from .prompts import SYSTEM_PROMPT
from .tools import TOOLS, call_tool

BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1").rstrip("/")
API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = os.environ.get("OPENAI_MODEL", "qwen2.5:3b")
TIMEOUT = 120
MAX_TURNS = 6


def _chat(messages: list) -> dict:
    r = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": messages, "tools": TOOLS,
              "tool_choice": "auto", "temperature": 0.7},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    body = r.json()
    if "data" in body and isinstance(body["data"], dict):  # some gateways wrap
        body = body["data"]
    return body["choices"][0]["message"]


def plan(place: str, minutes: int, interests: str = "") -> str:
    """Run the agent loop and return the final Markdown plan."""
    user_msg = (
        f"Plan a {minutes}-minute outdoor micro-adventure near {place!r}."
        + (f" Interests: {interests}." if interests else "")
        + " Use tools when useful, then write the plan."
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]
    for _ in range(MAX_TURNS):
        msg = _chat(messages)
        messages.append(msg)
        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            return msg.get("content", "").strip()
        for tc in tool_calls:
            fn = tc["function"]
            args = json.loads(fn.get("arguments") or "{}")
            result = call_tool(fn["name"], args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": json.dumps(result, ensure_ascii=False),
            })
    # Fallback: one last non-tool answer
    messages.append({"role": "user",
                     "content": "No more tool calls. Write the final plan now."})
    return (_chat(messages).get("content") or "").strip()
