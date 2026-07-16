# Loom script (6–8 minutes)

Record this once. Keep camera optional. Share screen on the repo + docs.

## Setup before record
1. Open GitHub repo in browser
2. Open `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md`
3. Open `00_Docs/Modules/11_Claude_Code/PR_REVIEW_ORCHESTRATOR_DESIGN.md`
4. Open `11_PR_Review_Orchestrator/` folder

## Script

**0:00–0:45 — Problem**
> I’m Vijay. My project is a Cross-Team PR Review Orchestrator.
> At Spotnana-style workflows, GitHub already assigns reviewers and we post PRs in Slack.
> The pain is when a PR touches multiple owner teams and one team responds late — merges stall for 1–3 days.
> Goal metric: reduce P75 Time In Review and percent of PRs waiting over 48 hours.

**0:45–2:00 — Current vs proposed flow**
> Show Task 1 diagram in the submission doc.
> Today: manual Slack follow-ups.
> Proposed: GitHub webhook → Temporal workflow → Slack thread with team-specific context → T1 nudge → T2 escalation → metrics.

**2:00–3:30 — Architecture**
> Show design doc + Task 2 infrastructure diagram.
> Components: GitHub, Temporal on AWS, Slack, Postgres/metrics, LLM summary with local policy RAG.
> Important: we do not replace CODEOWNERS; we orchestrate timing and communication.

**3:30–5:00 — Prototype status + scaffold**
> Show `11_PR_Review_Orchestrator/` structure: FastAPI app, services, dashboard, policy docs, eval folder.
> Walk IMPLEMENTATION_GUIDE briefly: normalize → orchestrate → notify → SLA → metrics.
> Be honest: scaffold and design are submitted; runtime wiring is the next implementation step.

**5:00–6:30 — Evals**
> Show Task 5/6 tables: before/after P75 Time In Review, >48h rate, quality guardrail.
> Anchored on Meta’s P75 Time In Review approach and Google’s fast-response review practices.

**6:30–7:30 — Next steps / close**
> Keep Temporal + Slack-thread UX + percentile metrics.
> Next: finish MVP endpoints, deploy dashboard, run pilot metrics.
> Thanks.

## After recording
1. Copy Loom URL
2. Paste into submission form and top of `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md`
3. Submit form
