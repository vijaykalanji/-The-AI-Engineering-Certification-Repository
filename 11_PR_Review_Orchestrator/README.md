# Cross-Team PR Review Orchestrator

Certification Challenge MVP: reduce cross-team PR review latency with GitHub events, SLA timers, Slack-style notifications, and measurable before/after metrics.

## Quick start

```bash
cd 11_PR_Review_Orchestrator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill OPENAI_API_KEY (or ANTHROPIC), GITHUB_WEBHOOK_SECRET, optional Slack tokens
uvicorn app.main:app --reload --port 8000
```

Open: http://localhost:8000

## MVP scope

1. Ingest GitHub webhook / simulated PR events
2. Track required teams + pending reviews
3. Generate team-specific LLM summary (RAG over local policy docs)
4. Fire T1 nudge / T2 escalation timers
5. Browser dashboard for PR state + metrics
6. Eval harness with before/after table

## Project layout

See file tree below. Fill every `TODO` before demo day.

## Deploy

Deploy FastAPI to Render / Railway / Fly. Point GitHub webhook at `/webhooks/github`.
