# Documentation

This directory holds the current plan, data and source references, design notes,
phase records, operations runbook and release evidence. The top-level
[README](../README.md) is the entry point for the atlas itself; this page is the
map for the working documents.

## Start here

| Document | Contents |
|---|---|
| [`plan/plan.md`](plan/plan.md) | Remaining V4 work, coverage gaps, acceptance criteria, blockers and invariants. |
| [`data-model.md`](data-model.md) | Curated tables, project columns, status definitions, claims and generated outputs. |
| [`sources.md`](sources.md) | Source register, raw snapshots, archive rules and provenance gaps. |
| [`operations/refresh-runbook.md`](operations/refresh-runbook.md) | Monthly fetch, diff, review, rebuild and verify procedure. |

## Design

| File | Contents |
|---|---|
| [`design/tokens-v4.md`](design/tokens-v4.md) | Token values, type scale, layout, bilingual surface and contrast baseline. |
| [`design/style-tile.html`](design/style-tile.html) | Live specimen that imports `site/assets/tokens.css` and `app.css`. |
| [`design/ux-audit-v4.md`](design/ux-audit-v4.md) | Expert audit, five-profile rehearsal, open findings and the five-user protocol. |

## Phase records

These are historical records of completed work. They explain how the current
data, trust layer and local release were built.

| File | Contents |
|---|---|
| [`phases/phase-1-decisions.md`](phases/phase-1-decisions.md) | Confirmed design, scope, schema and payload budgets. |
| [`phases/phase-2-transport.md`](phases/phase-2-transport.md) | Transport PSN extraction, status mapping and conflicts. |
| [`phases/phase-2-estates.md`](phases/phase-2-estates.md) | Estate gap ledger, PSN industrial-area completion and coordinate work. |
| [`phases/phase-2-factories.md`](phases/phase-2-factories.md) | Factory reference set, inclusion rules and conflicts. |
| [`phases/phase-2-roads.md`](phases/phase-2-roads.md) | BPJT PSN road additions and status mapping. |
| [`phases/phase-3-trust.md`](phases/phase-3-trust.md) | Claims, freshness, conflicts and local release evidence. |

## Data registers

| File | Contents |
|---|---|
| [`../data/curated/psn_register.csv`](../data/curated/psn_register.csv) | Official Permenko 16/2025 annex: 226 active projects, 24 active programmes and 3 deleted slots. |
| [`../data/curated/programmes.csv`](../data/curated/programmes.csv) | The 24 active PSN programmes with bilingual names, summaries, theme, lead agency and source. |
| [`../data/curated/pkpn_programmes.csv`](../data/curated/pkpn_programmes.csv) | The eight 2027 PKPN priorities with bilingual summaries, targets, budgets and sources. |
| [`../data/curated/pkpn_sources.csv`](../data/curated/pkpn_sources.csv) | 27 atomic claims for the PKPN layer. |
| [`../data/curated/programme_projects.csv`](../data/curated/programme_projects.csv) | Seven structural links between programmes and atlas projects. |
| [`../data/curated/organizations.csv`](../data/curated/organizations.csv) | 116 companies, agencies and consortia, with type, country and website. |
| [`../data/curated/project_organizations.csv`](../data/curated/project_organizations.csv) | 232 sourced project-role links (sponsor, operator, owner, contractor). |
| [`../data/curated/translations.csv`](../data/curated/translations.csv) | Reviewed entity text and official Indonesian names used by the bilingual build. |
| [`../data/i18n/ui.en.json`](../data/i18n/ui.en.json) | English UI catalogue: 635 semantic keys. |
| [`../data/i18n/ui.id.json`](../data/i18n/ui.id.json) | Indonesian UI catalogue: the same 635 keys. |
| [`../data/curated/indicators.csv`](../data/curated/indicators.csv) | 45 programme and project targets, baselines and units. |
| [`../data/curated/indicator_values.csv`](../data/curated/indicator_values.csv) | 28 dated indicator observations. |
| [`../data/curated/project_phases.csv`](../data/curated/project_phases.csv) | Nine sourced project phases with dates, cost and progress where stated. |
| [`../data/curated/estates.csv`](../data/curated/estates.csv) | 204 industrial estates and SEZs, including eight reviewed and 18 register-only PSN industrial areas. |
| [`../data/derived/psn_reconciliation.csv`](../data/derived/psn_reconciliation.csv) | Match ledger: all 226 active PSN project or estate records represented and all 24 programmes matched; 88 projects and 18 estates are register-only. |

## Evidence

`evidence/phase-3/` contains the desktop and mobile screenshots, the English and
Indonesian views, the language chooser, the browser smoke report and the
five-profile UX rehearsal. The report records zero external requests and zero
console errors. The screenshots are evidence for the 9 November 2026 V4
bilingual shell and later increments.

## Reading order

1. [README](../README.md) for what the atlas contains and how to open it.
2. [`plan/plan.md`](plan/plan.md) for what remains.
3. [`data-model.md`](data-model.md) and [`sources.md`](sources.md) before editing
   data.
4. [`phases/phase-3-trust.md`](phases/phase-3-trust.md) for how facts are sourced
   and verified.
5. [`design/ux-audit-v4.md`](design/ux-audit-v4.md) for usability findings and the
   open five-user study.
6. [`operations/refresh-runbook.md`](operations/refresh-runbook.md) before
   refreshing any source.

The release is local only: there is no remote, push or Pages deployment.
