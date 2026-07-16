"""Demo endpoints so you can exercise the flow without real GitHub/Slack."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.models.events import NormalizedPREvent
from app.services.orchestrator import Orchestrator

router = APIRouter(prefix="/demo", tags=["demo"])


class SimulatePRRequest(BaseModel):
    repo: str = "acme/payments"
    pr_number: int = 101
    author: str = "vijay"
    title: str = "Update payment retry + profile schema"
    changed_files: list[str] = Field(
        default_factory=lambda: [
            "services/payments/retry.py",
            "services/profile/models.py",
            "services/profile/migration.sql",
            "docs/runbooks/payments.md",
        ]
    )
    required_teams: list[str] = Field(
        default_factory=lambda: ["payments-team", "profile-team"]
    )


@router.post("/simulate-pr")
async def simulate_pr(body: SimulatePRRequest):
    """
    TODO: build NormalizedPREvent(event_type='opened', ...) and call Orchestrator.handle_event.
    Useful for Loom demos and local testing.
    """
    raise NotImplementedError("Implement simulate-pr demo endpoint")


@router.post("/simulate-review")
async def simulate_review(pr_number: int = 101, repo: str = "acme/payments", team: str = "payments-team"):
    """
    TODO: emit review_submitted for a team and update state via orchestrator.
    """
    raise NotImplementedError("Implement simulate-review demo endpoint")
