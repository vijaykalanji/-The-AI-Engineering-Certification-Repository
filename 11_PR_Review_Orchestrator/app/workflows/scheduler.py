"""Lightweight background SLA loop (replace with Temporal in production)."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.orchestrator import Orchestrator


async def sla_loop(orchestrator: Orchestrator, interval_seconds: int = 15) -> None:
    """
    TODO: while True:
      - call orchestrator.check_slas()
      - await asyncio.sleep(interval_seconds)
    Start this from FastAPI lifespan in main.py.
    """
    raise NotImplementedError("Implement background SLA loop")
