"""Application settings loaded from environment."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    llm_model: str
    github_webhook_secret: str
    slack_bot_token: str
    slack_default_channel: str
    t1_sla_minutes: int
    t2_sla_minutes: int
    app_base_url: str


def get_settings() -> Settings:
    # TODO: validate required keys and raise a clear error if missing
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        github_webhook_secret=os.getenv("GITHUB_WEBHOOK_SECRET", "dev-secret"),
        slack_bot_token=os.getenv("SLACK_BOT_TOKEN", ""),
        slack_default_channel=os.getenv("SLACK_DEFAULT_CHANNEL", "#pr-reviews"),
        t1_sla_minutes=int(os.getenv("T1_SLA_MINUTES", "1")),
        t2_sla_minutes=int(os.getenv("T2_SLA_MINUTES", "2")),
        app_base_url=os.getenv("APP_BASE_URL", "http://localhost:8000"),
    )
