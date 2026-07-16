"""Simple in-memory PR store (swap for Postgres later)."""

from __future__ import annotations

from threading import Lock

from app.models.state import PRState


class PRStore:
    def __init__(self) -> None:
        self._prs: dict[str, PRState] = {}
        self._lock = Lock()

    def upsert(self, state: PRState) -> PRState:
        with self._lock:
            self._prs[state.pr_id] = state
            return state

    def get(self, pr_id: str) -> PRState | None:
        with self._lock:
            return self._prs.get(pr_id)

    def list_all(self) -> list[PRState]:
        with self._lock:
            return list(self._prs.values())


# Shared singleton for the MVP process
store = PRStore()
