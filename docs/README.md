# Documentation

This directory holds the project's plans, phase records, operations runbook and
release evidence. The top-level [README](../README.md) is the entry point for the
atlas itself; this page is the map for the working documents.

## Plans

| File | Contents |
|---|---|
| [`plan/plan.md`](plan/plan.md) | Current V4 plan: national delivery atlas, 226 PSN projects + 24 programmes, bilingual UI, map and Data-view rebuild. |
| [`plan/plan-v3.md`](plan/plan-v3.md) | Completed three-phase overhaul backlog: site experience, data completeness and trust. |

## Design

| File | Contents |
|---|---|
| [`design/tokens-v4.md`](design/tokens-v4.md) | Token values, type scale, layout, bilingual surface and contrast baseline. |
| [`design/style-tile.html`](design/style-tile.html) | Live specimen that imports `site/assets/tokens.css` and `app.css`. |
| [`design/ux-audit-v4.md`](design/ux-audit-v4.md) | Expert audit, five-profile rehearsal, open findings and the five-user protocol. |

## Phase records

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
| [`../data/curated/organizations.csv`](../data/curated/organizations.csv) | 101 companies, agencies and consortia, with type, country and website. |
| [`../data/curated/project_organizations.csv`](../data/curated/project_organizations.csv) | 203 sourced project-role links (sponsor, operator, owner, contractor). |
| [`../data/curated/translations.csv`](../data/curated/translations.csv) | Reviewed entity text and official Indonesian names used by the bilingual build. |
| [`../data/i18n/ui.en.json`](../data/i18n/ui.en.json) | English UI catalogue: 635 semantic keys. |
| [`../data/i18n/ui.id.json`](../data/i18n/ui.id.json) | Indonesian UI catalogue: the same 635 keys. |
| [`../data/curated/indicators.csv`](../data/curated/indicators.csv) | Programme and project targets, baselines and units. |
| [`../data/curated/indicator_values.csv`](../data/curated/indicator_values.csv) | Dated indicator observations. |
| [`../data/curated/project_phases.csv`](../data/curated/project_phases.csv) | Sourced project phases with dates, cost and progress where stated. |
| [`../data/curated/estates.csv`](../data/curated/estates.csv) | 204 industrial estates and SEZs, including eight reviewed and 18 register-only PSN industrial areas. |
| [`../data/derived/psn_reconciliation.csv`](../data/derived/psn_reconciliation.csv) | Match ledger: 226 of 226 active PSN project or estate records represented and all 24 programmes matched; 88 projects and 18 estates are register-only. |

## Operations

| File | Contents |
|---|---|
| [`operations/refresh-runbook.md`](operations/refresh-runbook.md) | Monthly fetch, diff, review, rebuild and verify procedure. |

## Evidence

`evidence/phase-3/` contains the desktop and mobile screenshots, the English and
Indonesian views, the language chooser, the browser smoke report and the
five-profile UX rehearsal. The report records zero external requests and zero
console errors. The screenshots are evidence for the 9 November 2026 V4
bilingual shell.

## Reading order

1. [README](../README.md) for what the atlas contains and how to open it.
2. [`plan/plan.md`](plan/plan.md) for the V4 scope, data expansion, bilingual
   architecture and delivery plan.
3. [`plan/plan-v3.md`](plan/plan-v3.md) for the completed v3 backlog and the
   history behind the current build.
4. [`phases/phase-3-trust.md`](phases/phase-3-trust.md) for how facts are sourced
   and verified.
5. [`design/ux-audit-v4.md`](design/ux-audit-v4.md) for the current usability
   findings and the open five-user study.
6. [`operations/refresh-runbook.md`](operations/refresh-runbook.md) before
   refreshing any source.

The release is local only: there is no remote, push or Pages deployment.
