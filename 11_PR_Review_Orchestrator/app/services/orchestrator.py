"""Core orchestration: event -> state -> notify -> schedule SLA checks."""

from __future__ import annotations

from app.config import Settings, get_settings
from app.models.events import NormalizedPREvent
from app.models.state import PRState
from app.services.slack_notifier import SlackNotifier
from app.services.store import store
from app.services.summary_service import SummaryService


class Orchestrator:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.summary = SummaryService(self.settings)
        self.slack = SlackNotifier(self.settings)

    def handle_event(self, event: NormalizedPREvent) -> PRState:
        """
        TODO:
        1. Build/update PRState from event
        2. On opened/ready: generate summary, post Slack thread, set T1/T2 due times
        3. On review_submitted: mark team responded/approved
        4. On all required done: send completion, clear timers
        5. Persist via store.upsert
        """
        raise NotImplementedError("Implement event handling orchestration")

    def check_slas(self) -> list[str]:
        """
        TODO: scan open PRs; for due T1/T2, call slack nudge/escalation once.
        Return list of actions taken (for dashboard/debug).
        """
        raise NotImplementedError("Implement SLA checker")
