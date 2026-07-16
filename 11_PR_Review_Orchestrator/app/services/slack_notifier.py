"""Slack (or mock) notification surface."""

from __future__ import annotations

from app.config import Settings
from app.models.state import PRState


class SlackNotifier:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def post_initial_thread(self, state: PRState) -> str:
        """
        TODO: post enriched PR message to Slack channel.
        If SLACK_BOT_TOKEN is empty, write a mock thread id and append to state.notifications.
        Return thread_ts / mock id.
        """
        raise NotImplementedError("Implement initial Slack thread post")

    def send_nudge(self, state: PRState, pending_teams: list[str]) -> None:
        """TODO: mention only pending teams with concise context."""
        raise NotImplementedError("Implement T1 nudge")

    def send_escalation(self, state: PRState, pending_teams: list[str]) -> None:
        """TODO: escalate to fallback reviewer / team lead for pending teams."""
        raise NotImplementedError("Implement T2 escalation")

    def send_completion(self, state: PRState) -> None:
        """TODO: post 'all required teams reviewed' update."""
        raise NotImplementedError("Implement completion update")
