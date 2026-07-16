# Implementation order (fill every TODO)

Work top-to-bottom. After each step, run the app and verify.

## 1. Signature + team mapping (`app/services/github_normalize.py`)

- Implement `verify_github_signature`
- Implement `map_files_to_teams` (payments / profile / platform heuristics)
- Implement `normalize_github_event` for opened + review_submitted

## 2. Orchestrator (`app/services/orchestrator.py`)

- On `opened`: create `PRState`, set T1/T2 due times from settings
- Call summary + Slack (can mock Slack first)
- On `review_submitted`: mark matching team responded
- On all clear: completion notification

## 3. Slack notifier (`app/services/slack_notifier.py`)

- If no token: append strings to `state.notifications` and return mock thread id
- Implement nudge / escalation / completion

## 4. Summary + RAG (`app/services/summary_service.py`)

- Keyword retrieve from `app/data/policies/*.md`
- Call OpenAI if key present; else template summary grouped by team

## 5. SLA loop (`app/workflows/scheduler.py` + `main.py` lifespan)

- Periodic `check_slas()`
- Fire T1 once, then T2 once per PR

## 6. Demo APIs (`app/api/demo.py`)

- `simulate-pr` and `simulate-review` end-to-end without GitHub

## 7. Webhook (`app/api/webhooks.py`)

- Wire verify → normalize → orchestrator

## 8. Metrics + eval

- Implement `metrics_service.py`
- Finish `eval/run_eval.py` and paste table into submission doc

## 9. Deploy + Loom

- Deploy FastAPI
- Record <=10 min demo: simulate PR → nudge → reviews → metrics

## Suggested first command after implementing step 1–6

```bash
curl -X POST http://localhost:8000/demo/simulate-pr
open http://localhost:8000
```
