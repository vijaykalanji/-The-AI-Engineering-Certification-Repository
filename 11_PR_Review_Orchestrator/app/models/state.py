"""In-memory / persisted PR orchestration state."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TeamReviewStatus(BaseModel):
    team: str
    status: Literal["pending", "responded", "approved"] = "pending"
    first_response_at: datetime | None = None
    nudged_at: datetime | None = None
    escalated_at: datetime | None = None


class PRState(BaseModel):
    pr_id: str
    repo: str
    pr_number: int
    author: str
    title: str
    html_url: str
    changed_files: list[str] = Field(default_factory=list)
    teams: list[TeamReviewStatus] = Field(default_factory=list)
    status: Literal["open", "merged", "closed"] = "open"
    summary: str = ""
    slack_thread_id: str | None = None
    created_at: datetime
    updated_at: datetime
    t1_due_at: datetime | None = None
    t2_due_at: datetime | None = None
    notifications: list[str] = Field(default_factory=list)

    @property
    def pending_teams(self) -> list[str]:
        return [t.team for t in self.teams if t.status == "pending"]

    @property
    def is_cross_team(self) -> bool:
        return len(self.teams) >= 2
