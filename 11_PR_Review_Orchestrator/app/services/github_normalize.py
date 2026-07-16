"""Convert raw GitHub webhook payloads into NormalizedPREvent."""

from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone
from typing import Any

from app.models.events import NormalizedPREvent


def verify_github_signature(secret: str, body: bytes, signature_header: str | None) -> bool:
    """
    TODO: implement HMAC SHA-256 check against X-Hub-Signature-256.
    For local demo, you may temporarily return True when secret == 'dev-secret'.
    """
    raise NotImplementedError("Implement GitHub webhook signature verification")


def map_files_to_teams(changed_files: list[str]) -> list[str]:
    """
    TODO: map paths to owner teams.
    Example heuristic for MVP:
      - paths containing 'payments' -> payments-team
      - paths containing 'profile' -> profile-team
      - else -> platform-team
    Ensure unique teams, and prefer >=2 teams for cross-team demos.
    """
    raise NotImplementedError("Implement CODEOWNERS-style path -> team mapping")


def normalize_github_event(
    event_name: str,
    delivery_id: str,
    payload: dict[str, Any],
) -> NormalizedPREvent | None:
    """
    TODO: map GitHub event_name + payload into NormalizedPREvent.
    Handle at least: pull_request (opened/ready_for_review/closed/synchronize),
    pull_request_review (submitted).
    Return None for events you ignore.
    """
    raise NotImplementedError("Implement GitHub event normalization")


def make_pr_id(repo: str, pr_number: int) -> str:
    return f"{repo}#{pr_number}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
