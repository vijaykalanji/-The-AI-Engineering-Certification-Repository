"""Compute before/after style review latency metrics."""

from __future__ import annotations

from statistics import quantiles
from typing import Any

from app.models.state import PRState


def reviewer_wait_hours(state: PRState) -> float | None:
    """
    TODO: compute hours spent waiting on pending teams.
    For completed PRs, use created_at -> last first_response across teams
    (or a simpler MVP: created_at -> when pending_teams became empty).
    """
    raise NotImplementedError("Implement Time In Review calculation")


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    # TODO: compute percentile robustly; quantiles() is fine for MVP
    raise NotImplementedError("Implement percentile helper")


def summarize_prs(states: list[PRState]) -> dict[str, Any]:
    """
    TODO: return dict with:
      - count
      - p50/p75/p90 time_in_review_hours
      - pct_waiting_over_24h / 48h (or simulated for open PRs)
    """
    raise NotImplementedError("Implement metrics summary")
