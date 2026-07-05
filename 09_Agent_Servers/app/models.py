from __future__ import annotations

import json
import os
import re

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

DEFAULT_CHAT_MODEL = "gpt-5.4-mini"
DEFAULT_GATEWAY_BASE_URL = "https://ai-gateway.vercel.sh/v1"


def _openai_client_kwargs() -> dict:
    api_key = (
        os.environ.get("OPENAI_API_KEY")
        or os.environ.get("AI_GATEWAY_API_KEY")
        or os.environ.get("VERCEL_OIDC_TOKEN")
    )
    if not api_key:
        raise RuntimeError(
            "Set OPENAI_API_KEY or AI_GATEWAY_API_KEY in .env before running the agent."
        )

    kwargs: dict = {"openai_api_key": api_key}
    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get(
        "AI_GATEWAY_BASE_URL", DEFAULT_GATEWAY_BASE_URL
    )
    if base_url:
        kwargs["base_url"] = base_url
    return kwargs


def get_chat_model(model_name: str | None = None, *, temperature: float = 0) -> ChatOpenAI:
    name = model_name or os.environ.get("OPENAI_CHAT_MODEL", DEFAULT_CHAT_MODEL)
    return ChatOpenAI(
        model=name,
        temperature=temperature,
        **_openai_client_kwargs(),
    )


def fix_tool_calls(response: AIMessage) -> AIMessage:
    """Repair invalid tool calls when models append stray tokens to JSON args."""
    if not response.invalid_tool_calls:
        return response

    fixed = list(response.tool_calls)
    remaining_invalid = []

    for tc in response.invalid_tool_calls:
        cleaned = re.sub(r"\s*<\|call\|>\s*$", "", tc["args"])
        try:
            parsed = json.loads(cleaned)
            fixed.append(
                {
                    "name": tc["name"],
                    "args": parsed,
                    "id": tc["id"],
                    "type": "tool_call",
                }
            )
        except (json.JSONDecodeError, TypeError):
            remaining_invalid.append(tc)

    response.tool_calls = fixed
    response.invalid_tool_calls = remaining_invalid
    return response
