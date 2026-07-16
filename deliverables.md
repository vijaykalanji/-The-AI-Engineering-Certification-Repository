# Deliverables Traceability Map

Project: **Cross-Team PR Review Orchestrator**  
Author: Vijay Kalanji  
Repository: https://github.com/vijaykalanji/-The-AI-Engineering-Certification-Repository

This document maps each Certification Challenge task deliverable to the exact location in the repository (writeup section and/or code path).

Primary writeup: [`CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md`](../CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md)  
Design doc: [`00_Docs/Modules/11_Claude_Code/PR_REVIEW_ORCHESTRATOR_DESIGN.md`](../00_Docs/Modules/11_Claude_Code/PR_REVIEW_ORCHESTRATOR_DESIGN.md)  
Prototype code: [`11_PR_Review_Orchestrator/`](../11_PR_Review_Orchestrator/)

---

## Task 1 — Problem, Audience, and Scope

| # | Deliverable | Exact location |
|---|---|---|
| 1.1 | 1-sentence problem statement (no solution) | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 1 §1** |
| 1.2 | 1–2 paragraphs: who / what / today / why not enough | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 1 §2** |
| 1.3 | Current-state workflow diagram | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 1 §3** (Mermaid) |
| 1.4 | Evaluation questions / input-output pairs | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 1 §4** |

---

## Task 2 — Propose a Solution

| # | Deliverable | Exact location |
|---|---|---|
| 2.1 | One-sentence solution | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 2 §1** |
| 2.2 | Infrastructure diagram + component rationale (LLM, orchestration, tools, embeddings, vector DB, monitoring, eval, UI, deploy) | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 2 §2**; deeper detail in `00_Docs/Modules/11_Claude_Code/PR_REVIEW_ORCHESTRATOR_DESIGN.md` → **§7–8** |
| 2.3 | Agent workflow diagram + 1–2 paragraph explanation | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 2 §3** |
| 2.R1 | LLM gateway | Writeup Task 2 component list; runtime stub: `11_PR_Review_Orchestrator/app/services/summary_service.py` |
| 2.R2 | Memory component | Writeup Task 2; runtime: `11_PR_Review_Orchestrator/app/models/state.py`, `app/services/store.py`, workflow state in design doc **§8.2** |
| 2.R3 | Browser-accessible UI | `11_PR_Review_Orchestrator/app/main.py`, `app/templates/dashboard.html` |

---

## Task 3 — Dealing with the Data

| # | Deliverable | Exact location |
|---|---|---|
| 3.1 | Default chunking strategy + why | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 3 §1** |
| 3.2 | Data source + external API + interaction | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 3 §2** |
| 3.C1 | Personal / private RAG data | `11_PR_Review_Orchestrator/app/data/policies/*.md` (payments, profile, SLA policies) |
| 3.C2 | External API / agent tool | GitHub API + Slack API (design + writeup); ingress stubs: `app/api/webhooks.py`, `app/services/slack_notifier.py`, `app/services/github_normalize.py` |

---

## Task 4 — End-to-End Agentic RAG Prototype

| # | Deliverable | Exact location |
|---|---|---|
| 4.1 | End-to-end prototype | Scaffold: `11_PR_Review_Orchestrator/` — entry `app/main.py`; orchestration `app/services/orchestrator.py`; RAG/summary `app/services/summary_service.py`; demo API `app/api/demo.py`; status described in writeup **Task 4** |
| 4.2 | Public deployment | Deployment approach documented in writeup **Task 4 §2** and design doc **§15 / §18** (Render/Railway/Fly MVP; AWS Temporal production path). Live URL to be attached when deployed. |

---

## Task 5 — Evals

| # | Deliverable | Exact location |
|---|---|---|
| 5.1 | Test dataset | `11_PR_Review_Orchestrator/eval/baseline_vs_treatment.json`; described in writeup **Task 5 §1** |
| 5.2 | Evaluation harness | `11_PR_Review_Orchestrator/eval/run_eval.py`, `app/services/metrics_service.py`; method in writeup **Task 5 §2**; design doc **§16** |
| 5.3 | Conclusions | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 5 §3** (before/after table) |

---

## Task 6 — Improving the Prototype

| # | Deliverable | Exact location |
|---|---|---|
| 6.1 | Advanced retrieval technique + why | Writeup **Task 6 §1** (risk-aware, team-specific context retrieval); retrieval stub: `app/services/summary_service.py` + policies under `app/data/policies/` |
| 6.2 | Performance comparison table | Writeup **Task 6 §2** |
| 6.3 | Second improvement + evidence | Writeup **Task 6 §3** (business-hours-aware SLA timers); SLA loop stub: `app/workflows/scheduler.py`, `app/services/orchestrator.py` |

---

## Task 7 — Next Steps

| # | Deliverable | Exact location |
|---|---|---|
| 7.1 | Keep vs change for Demo Day + reasoning | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` → **Task 7**; roadmap also in design doc **§18–19** |

---

## Final package artifacts

| Artifact | Location |
|---|---|
| Written document (all tasks) | `CERTIFICATION_CHALLENGE_SUBMISSION_DRAFT.md` |
| Production design | `00_Docs/Modules/11_Claude_Code/PR_REVIEW_ORCHESTRATOR_DESIGN.md` |
| Prototype code | `11_PR_Review_Orchestrator/` |
| Implementation sequence | `11_PR_Review_Orchestrator/IMPLEMENTATION_GUIDE.md` |
| Official challenge brief | `00_Docs/Certification Challenge/README.md` |
| Loom demo (<=10 min) | Link pasted in submission form (and writeup header once recorded) |

---

## Status notes for graders

- Tasks **1–3, 5–7** are addressed in the written deliverable with diagrams and metric tables.
- Task **4** is represented by a production-oriented design plus an MVP FastAPI scaffold with service interfaces; remaining runtime TODOs are listed in `11_PR_Review_Orchestrator/IMPLEMENTATION_GUIDE.md`.
- This traceability file is the index from rubric deliverables → exact repo locations.
