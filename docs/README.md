# Documentation

This directory holds the project's plans, phase records, operations runbook and
release evidence. The top-level [README](../README.md) is the entry point for the
atlas itself; this page is the map for the working documents.

## Plans

| File | Contents |
|---|---|
| [`plan/plan.md`](plan/plan.md) | Scope, decisions, data architecture, history and the current status. |
| [`plan/plan-v3.md`](plan/plan-v3.md) | The three-phase overhaul backlog: site experience, data completeness and trust. |

## Phase records

| File | Contents |
|---|---|
| [`phases/phase-1-decisions.md`](phases/phase-1-decisions.md) | Confirmed design, scope, schema and payload budgets. |
| [`phases/phase-2-transport.md`](phases/phase-2-transport.md) | Transport PSN extraction, status mapping and conflicts. |
| [`phases/phase-2-estates.md`](phases/phase-2-estates.md) | Estate gap ledger and coordinate work. |
| [`phases/phase-2-factories.md`](phases/phase-2-factories.md) | Factory universe, inclusion rules and conflicts. |
| [`phases/phase-2-roads.md`](phases/phase-2-roads.md) | BPJT PSN road additions and status mapping. |
| [`phases/phase-3-trust.md`](phases/phase-3-trust.md) | Claims, freshness, conflicts and local release evidence. |

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
2. [`plan/plan-v3.md`](plan/plan-v3.md) for the work status and remaining gaps.
3. [`phases/phase-3-trust.md`](phases/phase-3-trust.md) for how facts are sourced
   and verified.
4. [`operations/refresh-runbook.md`](operations/refresh-runbook.md) before
   refreshing any source.

The release is local only: there is no remote, push or Pages deployment.
