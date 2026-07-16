# Loom recording guide (step-by-step)

Target length: **6–9 minutes** (under 10 required)

Repo: https://github.com/vijaykalanji/-The-AI-Engineering-Certification-Repository

---

## Part A — What you need to do (before recording)

### Step 1: Open these tabs (in order)
1. GitHub repo home (main branch)
2. `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` (on GitHub or locally in Cursor)
3. `00_Docs/Modules/11_Claude_Code/PR_REVIEW_ORCHESTRATOR_DESIGN.md`
4. Folder `11_PR_Review_Orchestrator/` (file tree)
5. Optional: `00_Docs/Certification Challenge/README.md` (official brief)

### Step 2: Set up Loom
1. Open Loom (browser or desktop app)
2. Choose **Screen only** or **Screen + cam** (cam optional)
3. Select the browser/Cursor window
4. Close Slack/email notifications
5. Speak slightly slower than normal

### Step 3: Recording goal
Show graders:
- Clear problem + user
- Solution architecture
- Prototype structure in repo
- Eval metrics / improvement plan
- Honest next steps

You are **not** required to show a fully running production system in this recording if the app TODOs are unfinished — walk the design + scaffold clearly.

---

## Part B — Exact recording script (say this)

### Segment 1 — Intro + problem (0:00–1:00)

**Do on screen:** Open submission doc → Task 1 heading.

**Say:**
> Hi, I’m Vijay Kalanji. This is my Certification Challenge project: Cross-Team PR Review Orchestrator.
>
> The problem: backend engineers lose delivery time when a PR touches files owned by multiple teams and one required team reviews late. Even though GitHub already auto-assigns reviewers and we post PRs in Slack, merges can stall for one to three days.
>
> My target users are PR authors and cross-team reviewers. Success metric is P75 Time In Review and the percent of PRs waiting more than 48 hours.

### Segment 2 — Current workflow vs proposed (1:00–2:15)

**Do on screen:** Scroll to Task 1 Mermaid current-state diagram.

**Say:**
> Today the flow is: create PR, auto-assign owners, post in Slack, then wait. If one team is delayed, authors manually chase people. That creates friction and no consistent latency telemetry.
>
> The proposed system keeps that habit, but adds orchestration: durable timers, targeted nudges, fallback escalation, and team-specific context summaries.

### Segment 3 — Solution + architecture (2:15–4:00)

**Do on screen:** Task 2 diagrams, then switch to design doc briefly.

**Say:**
> Solution in one sentence: a production-grade orchestration service using GitHub events, Temporal workflows on AWS, and Slack-thread automation to reduce cross-team wait time without replacing ownership rules.
>
> Components: GitHub webhooks, Temporal workers, Slack API, Postgres/metrics store, LLM gateway for summaries, and local policy docs for lightweight RAG context.
>
> Key principle: augment, don’t disrupt. We do not replace CODEOWNERS. We reduce idle wait with SLA-aware nudges and better review context.

### Segment 4 — Prototype / code in repo (4:00–6:00)

**Do on screen:** Open `11_PR_Review_Orchestrator/` tree → show:
- `app/main.py`
- `app/services/`
- `app/data/policies/`
- `eval/`
- `IMPLEMENTATION_GUIDE.md`

**Say:**
> In the repo, the MVP scaffold lives under `11_PR_Review_Orchestrator`.
>
> FastAPI entrypoint and dashboard template are here. Services cover GitHub normalization, orchestration, Slack notifications, summary/RAG, and metrics.
>
> Policy markdown files support retrieval for team-specific review guidance.
>
> The implementation guide sequences the remaining TODOs: normalize events, orchestrate state, notify, run SLA checks, then evaluate.
>
> Current status: design and scaffold are complete in GitHub; runtime wiring against these interfaces is the remaining implementation work.

### Segment 5 — Evals + improvement (6:00–7:30)

**Do on screen:** Task 5 and Task 6 tables in the submission doc.

**Say:**
> For evaluation I use Meta-style P75 Time In Review as the north star, with quality guardrails so speed doesn’t become rubber-stamping.
>
> Baseline vs treatment targets show expected reductions in P75 wait time and PRs waiting over 48 hours, without regressing revert/hotfix rate.
>
> Task 6 improvement is risk-aware team-specific context retrieval, plus business-hours-aware SLA timers.

### Segment 6 — Close (7:30–8:30)

**Do on screen:** Back to repo root README / submission checklist.

**Say:**
> Next steps: finish MVP endpoints, deploy the dashboard, collect pilot metrics, then harden Temporal production wiring.
>
> Repo link is in the submission form. Thanks for reviewing.

### Step 4: Stop recording
1. Click Stop in Loom
2. Wait for processing
3. Set video to **Anyone with link can view**
4. Copy the URL

---

## Part C — After Loom (submission steps)

1. Paste Loom URL into the [submission form](https://docs.google.com/forms/d/e/1FAIpQLSfVl-bXwO_NlkleaLtSQ1yp2tLM8EM3w5AukRLbP637Dg8_8Q/viewform)
2. Paste GitHub repo URL:  
   `https://github.com/vijaykalanji/-The-AI-Engineering-Certification-Repository`
3. In the form/comments, point reviewers to:
   - `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md`
   - `00_Docs/Modules/11_Claude_Code/PR_REVIEW_ORCHESTRATOR_DESIGN.md`
   - `11_PR_Review_Orchestrator/`
4. Optional: update the top of `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` with the Loom URL and push again
5. Submit the form

---

## Quick checklist

- [ ] Tabs open
- [ ] Loom recording started
- [ ] Problem + user stated
- [ ] Diagrams shown
- [ ] Architecture explained
- [ ] Scaffold shown
- [ ] Eval tables shown
- [ ] Loom link copied
- [ ] Form submitted
