"""LLM summary generation + lightweight RAG over local policy docs."""

from __future__ import annotations

from pathlib import Path

from app.config import Settings
from app.models.state import PRState

POLICY_DIR = Path(__file__).resolve().parents[1] / "data" / "policies"


class SummaryService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def retrieve_policy_context(self, changed_files: list[str]) -> str:
        """
        TODO: load markdown files from app/data/policies and pick chunks
        relevant to changed_files / team names (simple keyword match is fine for MVP).
        """
        raise NotImplementedError("Implement local policy RAG retrieval")

    def build_team_summary(self, state: PRState) -> str:
        """
        TODO: call LLM gateway (OpenAI) with:
          - PR title/url
          - files grouped by team
          - retrieved policy context
        Return a short multi-section summary for Slack + dashboard.
        If no API key, return a deterministic template summary.
        """
        raise NotImplementedError("Implement LLM/team summary generation")
