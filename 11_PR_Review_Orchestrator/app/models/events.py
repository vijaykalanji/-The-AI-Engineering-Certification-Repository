"""Normalized GitHub event shapes used by the orchestrator."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class NormalizedPREvent(BaseModel):
    event_id: str
    event_type: Literal[
        "opened",
        "ready_for_review",
        "review_submitted",
        "synchronized",
        "closed",
        "merged",
    ]
    repo: str
    pr_number: int
    author: str
    title: str = ""
    html_url: str = ""
    changed_files: list[str] = Field(default_factory=list)
    required_teams: list[str] = Field(default_factory=list)
    actor: str = ""
    review_state: str | None = None
    timestamp: datetime
