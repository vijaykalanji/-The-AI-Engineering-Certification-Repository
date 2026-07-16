"""FastAPI entrypoint: dashboard + webhooks + demo APIs."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import demo, webhooks
from app.config import get_settings
from app.services.orchestrator import Orchestrator
from app.services.store import store
from app.workflows.scheduler import sla_loop


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: start asyncio.create_task(sla_loop(Orchestrator()))
    # and cancel it on shutdown
    yield


app = FastAPI(title="PR Review Orchestrator", lifespan=lifespan)
app.include_router(webhooks.router)
app.include_router(demo.router)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    TODO: render dashboard.html with store.list_all() and metrics summary.
    """
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "prs": store.list_all(),
            "settings": get_settings(),
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
