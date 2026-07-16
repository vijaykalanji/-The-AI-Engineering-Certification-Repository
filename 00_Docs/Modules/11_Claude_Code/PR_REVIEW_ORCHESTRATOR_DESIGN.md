# Cross-Team PR Review Orchestrator

Production-grade design document for reducing pull request (PR) review latency in a multi-team ownership model.

## 1) Executive Summary

This project introduces a production-grade orchestration service that reduces end-to-end PR review latency for cross-team changes while preserving review quality.

It integrates with existing developer behavior:

- PRs are created in GitHub.
- Reviewers are auto-assigned by existing rules (`CODEOWNERS` or current org policy).
- PRs are posted in team Slack channels.

The new system adds:

- Context-rich PR summaries for each owner team.
- SLA-aware nudges and fallback routing.
- Durable Temporal workflows for coordination and timers.
- Metrics and experiments to prove measurable improvement.

Primary optimization target follows Meta's publicly described approach: improve the slow tail of reviewer wait time (P75), not only median.

References:

- [Meta: Move faster, wait less](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/)
- [Google: Engineering code review practices](https://google.github.io/eng-practices/review/)

## 2) Problem Statement

In cross-team PRs, one team's delayed review can stall merges by 1-3 days even when other required reviewers respond quickly. This creates queueing delays, context switching, and lower engineering throughput.

### 2.1 Users

- Primary: PR authors (backend engineers)
- Secondary: reviewers across owner teams
- Stakeholders: tech leads and engineering managers responsible for delivery flow

### 2.2 Goals

1. Reduce reviewer wait latency on cross-team PRs.
2. Increase on-time review responses without increasing burden.
3. Preserve or improve review quality.
4. Provide defensible before/after evidence.

### 2.3 Non-goals (v1)

- Replacing human code review.
- Replacing existing reviewer assignment logic.
- Full auto-merge/autonomous code changes.
- Large org-wide policy engine from day 1.

## 3) Product Principles

1. **Augment, do not disrupt**: preserve current GitHub + Slack flow.
2. **Low-noise operations**: nudge by exception, not constant reminders.
3. **Tail-focused performance**: optimize P75/P90 wait states.
4. **Quality guardrails first**: speed improvements must not degrade quality.
5. **Deterministic orchestration**: Temporal workflow is source of truth for timing and state transitions.

## 4) Success Metrics (North Star + Guardrails)

### 4.1 North-star metric

- **P75 Time In Review (reviewer-wait only)**  
  The sum of intervals where PR is blocked on reviewer action.

This aligns with the Meta article's "Time In Review" framing.

### 4.2 Primary delivery metrics

- P75 time to first human review response
- P75 time to all required team reviews
- % PRs waiting >24h and >48h for required review

### 4.3 Quality and behavior guardrails

- Revert/hotfix rate within 7 days of merge
- Non-trivial review comment rate (to avoid rubber-stamping)
- Median reviewer "eyeball time" proxy (if available)
- Author/reviewer satisfaction pulse (weekly 2-question survey)

### 4.4 Suggested v1 targets

- >=20% reduction in P75 Time In Review
- >=15% reduction in time to all required reviews
- >=20% reduction in % PRs waiting >48h
- No regression in revert/hotfix rate

## 5) Functional Requirements

1. Ingest GitHub PR lifecycle events in near real time.
2. Correlate events to one durable workflow per PR.
3. Detect cross-team PRs (>=2 required owner teams) and apply orchestration policy.
4. Post enriched Slack thread context when PR is opened/ready.
5. Track SLA timers and pending teams.
6. Send targeted nudges only to pending team/reviewer.
7. Escalate to fallback reviewer/team lead on SLA breach.
8. Update Slack thread as review state changes.
9. End workflow on merge/close and emit metrics.
10. Support policy-by-repo/team configuration.

## 6) Non-functional Requirements

- **Reliability**: 99.9% workflow execution success (excluding upstream API outages)
- **Latency**: event ingestion to state update <60s P95
- **Scalability**: handle expected peak PR event fanout (repo-level spikes)
- **Security**: webhook signature validation, least-privilege tokens, audit trail
- **Operability**: replay-safe idempotent handlers, observability and on-call runbooks

## 7) High-Level Architecture

1. **GitHub Webhooks**
   - `pull_request`, `pull_request_review`, `pull_request_review_comment`, `issue_comment`
2. **Ingress API**
   - Validates signatures
   - Normalizes payloads
   - Publishes events
3. **Event Transport**
   - SQS (or direct Temporal signal dispatch for lower complexity)
4. **Temporal Workers (AWS-hosted)**
   - Long-running PR orchestration workflow
   - SLA timers, nudges, escalation logic
5. **Integrations**
   - GitHub API (read review state, post comments/status)
   - Slack API (post/update thread, targeted mentions)
6. **State + Analytics Store**
   - Postgres (operational snapshots) and/or data warehouse for metrics
7. **Monitoring**
   - CloudWatch + optional Datadog dashboards/alerts

## 8) Detailed Component Design

## 8.1 Ingress API

Responsibilities:

- Receive webhook requests.
- Verify GitHub signature (`X-Hub-Signature-256`).
- Generate idempotency key from delivery ID + event + PR number + revision.
- Persist raw event (for forensic replay).
- Forward normalized event to Temporal signal path.

Failure handling:

- Invalid signature -> `401`.
- Malformed payload -> `400`.
- Downstream unavailable -> retry with DLQ.

## 8.2 Temporal Workflow

Workflow key:

- `workflow_id = pr::<org>/<repo>#<pr_number>`

Signals:

- `PrOpenedOrReady`
- `ReviewSubmitted`
- `ReviewCommented`
- `PrSynchronized` (new commits)
- `ReviewerRequested`
- `PrClosedOrMerged`

Timers:

- `T1_first_response_sla`
- `T2_escalation_sla`
- optional `quiet_hours_resume_timer`

Core state in workflow memory:

- required teams/reviewers
- responded teams/reviewers
- slack channel + thread ts
- SLA deadlines and escalation status
- policy version used for decisions

Deterministic decision loop:

1. Initialize on `opened` or `ready_for_review`.
2. Post enriched Slack message.
3. Start T1.
4. On each signal, recompute pending teams.
5. If all required reviews satisfied -> complete.
6. If T1 fires and pending exists -> targeted nudge.
7. Start/re-arm T2 as configured.
8. If T2 fires and pending persists -> fallback/escalation.
9. On merge/close -> finalize metrics and close workflow.

## 8.3 Slack Notification Service

Message types:

- Initial enriched PR thread
- T1 nudge (pending-team only)
- T2 escalation (backup reviewer or team lead)
- Completion summary

Principles:

- Single thread per PR to reduce noise.
- Mention only needed actors.
- Support "remind later" and "acknowledge" actions where feasible.

## 8.4 Policy Service

Policy hierarchy:

- Global defaults -> repo overrides -> team overrides

Fields:

- first response SLA (business hours)
- escalation SLA
- quiet hours windows
- hotfix bypass labels
- fallback reviewer map
- escalation target map

Versioning:

- Every workflow stores `policy_version` to support deterministic auditing.

## 8.5 Metrics Pipeline

Raw facts captured:

- state transitions with timestamps
- reviewer actions and actor team
- nudge/escalation sends and outcomes

Derived metrics:

- Time In Review segments
- first response time
- all-required-response time
- stale thresholds (>24h, >48h)

## 9) Data Model (Operational)

### 9.1 `pr_workflow_state`

- `pr_id` (pk, string)
- `repo`
- `pr_number`
- `author`
- `status` (`OPEN`, `MERGED`, `CLOSED`)
- `cross_team` (bool)
- `required_teams` (jsonb)
- `responded_teams` (jsonb)
- `slack_channel`
- `slack_thread_ts`
- `policy_version`
- `created_at`, `updated_at`

### 9.2 `pr_events`

- `event_id` (pk)
- `pr_id`
- `source` (`github`, `slack`, `system`)
- `event_type`
- `actor`
- `event_ts`
- `payload` (jsonb)

### 9.3 `pr_sla_actions`

- `id` (pk)
- `pr_id`
- `action_type` (`NUDGE_T1`, `ESCALATE_T2`)
- `target_team`
- `target_user`
- `sent_ts`
- `ack_ts` (nullable)
- `result` (`RESPONDED`, `NO_RESPONSE`, `DISMISSED`)

## 10) Event Contract (Normalized)

```json
{
  "event_id": "github-delivery-id",
  "event_type": "pull_request_review",
  "repo": "org/repo",
  "pr_number": 1234,
  "pr_sha": "abcdef",
  "actor": "jdoe",
  "timestamp": "2026-07-13T12:00:00Z",
  "metadata": {
    "review_state": "APPROVED",
    "requested_reviewers": ["team-a", "team-b"]
  }
}
```

## 11) SLA and Time Semantics

All SLA computation must be business-hour aware and timezone aware.

Recommended defaults:

- T1 first response: 4 business hours
- T2 escalation: 8 business hours after T1
- stale threshold reports: 24h and 48h wall-clock

Edge cases:

- holidays/weekends -> paused SLA clock when configured
- hotfix label -> bypass nudge/escalation policy
- draft PR -> workflow initialization delayed until `ready_for_review`

## 12) Security and Compliance

1. GitHub webhook HMAC verification mandatory.
2. Slack and GitHub tokens in AWS Secrets Manager; rotate quarterly.
3. Least-privilege scopes:
   - GitHub: read PR metadata + comment/status updates only
   - Slack: post/update messages in approved channels only
4. Immutable audit log of automated actions.
5. PII minimization in logs (no full payload dumps in normal log path).

## 13) Reliability and Failure Strategy

1. Idempotent processing by delivery/event key.
2. Exponential backoff for GitHub/Slack activity failures.
3. Dead-letter queue for unrecoverable events.
4. Temporal retry policies per activity class:
   - transient API failures: retry
   - 4xx policy/config errors: no blind retries
5. Periodic reconciler job:
   - verifies open PR workflows against GitHub truth.

## 14) Observability and SRE

Dashboards:

- Workflow success/failure rate
- Signal-to-action latency
- Nudge volume and response conversion
- SLA breach trend by team/repo
- P50/P75/P90 Time In Review

Alerts:

- Temporal worker error rate spike
- Slack delivery failure rate > threshold
- Missing metric ingestion for >N minutes
- DLQ growth rate anomaly

Runbooks:

- replay stuck workflow
- drain DLQ
- rotate secrets
- disable automation via feature flag

## 15) Rollout Strategy

### Phase 0: Shadow Mode (2 weeks)

- No nudges or escalations.
- Compute metrics and validate baselines.

### Phase 1: Nudge-Only (2 weeks)

- Enable T1 nudges for selected repos.
- Validate noise and response behavior.

### Phase 2: Escalation (2-4 weeks)

- Enable T2 fallback/escalation for persistent waits.

### Phase 3: Policy Tuning

- Team-specific SLA thresholds based on observed data.

Release controls:

- per-repo feature flags
- kill switch for Slack actions
- canary subset (10-20% PRs)

## 16) Evaluation Plan (Before/After)

This section is designed to align with challenge expectations and industry-style rigor.

### 16.1 Cohort

- Include only cross-team PRs (`>=2` owner teams).
- Exclude hotfix and emergency labels from primary analysis.

### 16.2 Baseline and treatment windows

- Baseline: prior 4-6 weeks
- Treatment: 4-6 weeks after rollout
- Prefer A/B or stepped rollout for stronger causal claims

### 16.3 Report format

For each metric:

- before: P50/P75/P90
- after: P50/P75/P90
- absolute delta
- percentage delta

### 16.4 Statistical guidance

- Use bootstrap confidence intervals for percentile deltas.
- Segment by PR size and number of owner teams.
- Validate no guardrail degradation.

### 16.5 Example result table template

| Metric | Before P75 | After P75 | Delta | Delta % |
|---|---:|---:|---:|---:|
| Time In Review (hrs) | 28.0 | 20.5 | -7.5 | -26.8% |
| Time to all required reviews (hrs) | 31.2 | 24.8 | -6.4 | -20.5% |
| PRs waiting >48h | 18.4% | 12.7% | -5.7 pp | -31.0% |

## 17) Risks and Mitigations

1. **Alert fatigue**
   - mitigation: one nudge per SLA stage; targeted mentions only
2. **Rubber-stamp behavior**
   - mitigation: quality guardrails and review-depth monitoring
3. **Policy unfairness across teams**
   - mitigation: team-level overrides and transparent metrics
4. **Tool trust deficit**
   - mitigation: gradual rollout + visible opt-out for emergencies

## 18) Implementation Plan and Milestones

### Milestone 1

- Ingress + Temporal workflow scaffolding
- PR state model + event persistence
- Slack initial thread message

### Milestone 2

- SLA timers, T1 nudge, T2 escalation
- Policy service and feature flags
- Basic dashboards

### Milestone 3

- Experiment framework (control vs treatment)
- Full metric exports and reporting notebook
- Production hardening and on-call runbooks

## 19) Challenge Deliverable Mapping

1. **Task 1 (Problem/User)**: cross-team PR latency and impacted engineers.
2. **Task 2 (Solution)**: Temporal-based orchestration with GitHub + Slack + AWS.
3. **Task 3 (Data/API)**: GitHub events + Slack interactions + policy metadata.
4. **Task 4 (E2E prototype)**: deploy API + workers + Slack integration.
5. **Task 5 (Evals)**: before/after P75 wait-time analysis with guardrails.
6. **Task 6 (Improvement)**: add risk-aware prioritization or smarter nudge targeting.
7. **Task 7 (Next steps)**: org rollout strategy and governance.

## 20) Appendix: Industry Anchors Used

- Meta code review optimization (Time In Review, P75 focus, guardrails, experimentation):  
  [https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/)

- Google code review foundations (right reviewers, code quality dimensions):  
  [https://google.github.io/eng-practices/review/](https://google.github.io/eng-practices/review/)

- Google review speed and response expectations:  
  [https://google.github.io/eng-practices/review/reviewer/speed.html](https://google.github.io/eng-practices/review/reviewer/speed.html)

- Google small changes guidance for throughput:  
  [https://google.github.io/eng-practices/review/developer/small-cls.html](https://google.github.io/eng-practices/review/developer/small-cls.html)
