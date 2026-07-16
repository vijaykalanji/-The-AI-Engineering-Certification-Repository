"""GitHub webhook ingress."""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request

from app.config import get_settings
from app.services.github_normalize import normalize_github_event, verify_github_signature
from app.services.orchestrator import Orchestrator

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
    x_github_event: str | None = Header(default=None),
    x_github_delivery: str | None = Header(default=None),
):
    """
    TODO:
    1. Read raw body bytes
    2. verify_github_signature(...)
    3. parse JSON payload
    4. normalize_github_event(...)
    5. if event is None -> return {"ok": True, "ignored": True}
    6. orchestrator.handle_event(event)
    7. return {"ok": True, "pr_id": ...}
    """
    raise HTTPException(status_code=501, detail="Implement GitHub webhook handler")
