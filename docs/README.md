# Documentation

This directory holds the project's plans, phase records, operations runbook and
release evidence. The top-level [README](../README.md) is the entry point for the
atlas itself; this page is the map for the working documents.

## Plans

| File | Contents |
|---|---|
| [`plan/plan.md`](plan/plan.md) | Current V4 plan: national delivery atlas, 226 PSN projects + 24 programmes, bilingual UI, map and Data-view rebuild. |
| [`plan/plan-v3.md`](plan/plan-v3.md) | Completed three-phase overhaul backlog: site experience, data completeness and trust. |

## Phase records

| File | Contents |
|---|---|
| [`phases/phase-1-decisions.md`](phases/phase-1-decisions.md) | Confirmed design, scope, schema and payload budgets. |
| [`phases/phase-2-transport.md`](phases/phase-2-transport.md) | Transport PSN extraction, status mapping and conflicts. |
| [`phases/phase-2-estates.md`](phases/phase-2-estates.md) | Estate gap ledger and coordinate work. |
| [`phases/phase-2-factories.md`](phases/phase-2-factories.md) | Factory reference set, inclusion rules and conflicts. |
| [`phases/phase-2-roads.md`](phases/phase-2-roads.md) | BPJT PSN road additions and status mapping. |
| [`phases/phase-3-trust.md`](phases/phase-3-trust.md) | Claims, freshness, conflicts and local release evidence. |

## Data registers

| File | Contents |
|---|---|
| [`../data/curated/psn_register.csv`](../data/curated/psn_register.csv) | Official Permenko 16/2025 annex: 226 active projects, 24 active programmes and 3 deleted slots. |
| [`../data/curated/programmes.csv`](../data/curated/programmes.csv) | The 24 active PSN programmes with bilingual names, summaries, theme, lead agency and source. |
| [`../data/curated/programme_projects.csv`](../data/curated/programme_projects.csv) | Seven structural links between programmes and atlas projects. |
| [`../data/curated/estates.csv`](../data/curated/estates.csv) | 186 industrial estates and SEZs, including eight PSN industrial areas with dated area, manager and status sources. |
| [`../data/derived/psn_reconciliation.csv`](../data/derived/psn_reconciliation.csv) | Match ledger: 120 active PSN project or estate records and all 24 programmes matched; 106 project or estate records outstanding, with owner, next action and release. |

## Operations

| File | Contents |
|---|---|
| [`operations/refresh-runbook.md`](operations/refresh-runbook.md) | Monthly fetch, diff, review, rebuild and verify procedure. |

## Evidence

`evidence/phase-3/` contains the desktop and mobile screenshots and the browser
smoke report produced for the Phase 3 local release. The report records zero
external requests and zero console errors.

## Reading order

1. [README](../README.md) for what the atlas contains and how to open it.
2. [`plan/plan.md`](plan/plan.md) for the V4 scope, data expansion, bilingual
   architecture and delivery plan.
3. [`plan/plan-v3.md`](plan/plan-v3.md) for the completed v3 backlog and the
   history behind the current build.
4. [`phases/phase-3-trust.md`](phases/phase-3-trust.md) for how facts are sourced
   and verified.
5. [`operations/refresh-runbook.md`](operations/refresh-runbook.md) before
   refreshing any source.

The release is local only: there is no remote, push or Pages deployment.
