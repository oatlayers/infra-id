# Phase 3 — trust layer and local release

**Status:** complete, 8 November 2026. This phase ends with a **local release
only**. Nothing was pushed, no remote was added, and no GitHub Pages deployment
or public release was made.

**Scope:** Q1–Q5 (trust layer) and S1–S5 (local release and hand-off) from
[`plan-v3.md`](../plan/plan-v3.md). The site and the curated tables are the
deliverables; the evidence is in this document, `CHANGELOG.md` and
`docs/evidence/phase-3/`.

> **Historical snapshot.** The counts below describe the v3 release on
> 8 November 2026. V4 added the PSN register and reconciliation ledger; the
> current build has 19 curated tables and 26 generated files.

**Current build:** 107 projects, 178 estates and SEZs, 70 organisations, 89
sources, 5 corridors, 44 segments, 6 events, 18 investments, 479 project
claims, 20 estate claims and 19 conflicts. Validation passes, the site check
passes, and a deterministic rebuild leaves 25 generated files unchanged.

---

## 1. What "trust" means here

The atlas does not claim to be a live tracker. It makes four narrower promises:

1. **Every row has a source and a verification date.** `sources.csv` holds the
   document; `last_verified` and `status_as_of` hold the dates.
2. **Every populated status and numeric fact has an atomic claim.** A claim is
   one fact per row, linked to one source. This is what makes the evidence
   auditable instead of a free-text citation.
3. **A status change needs an official source or two independent sources.**
   Verification is recorded as `official`, `dual` or `single`; `single` is a
   warning, not a silent promotion.
4. **Disagreement stays visible.** The project row's `notes` and the conflict
   register keep both values and both sources. A resolution says what the atlas
   publishes; it does not erase the alternative.

A claim is not the same thing as a source. `sources.csv` answers "what document
did we read?"; `project_sources.csv` answers "which fact in that document
supports which field?"; `conflicts.csv` answers "where do two documents
disagree?".

## 2. Q1 — per-fact claims

### What changed

Phase 2 stored claims as combined strings such as
`status,length,operator,location` (283 rows, 87 with a comma-separated claim).
That made a per-fact audit impossible. `scripts/tools/normalize_claims.py` splits every
string into one row per claim type, lower-cases `PSN`, merges duplicate notes,
and backfills claims that existed only on the project row.

| Measure | Before | After |
|---|---:|---:|
| Project claim rows | 283 | **479** |
| Claims with more than one type | 87 | **0** |
| Projects with a status claim | 52 | **107 / 107** |
| Estate claims | 20 | 20 |

The 479 claims break down as: status 109, location 92, opening 58, length 45,
operator 43, investment 32, operational 31, capacity 28, coordinates 18, target
6, PSN 4, progress 3, and one each of restart, ramp-up, output, layoffs,
production halt, startup schedule, history, timeline, design capacity and
current capacity. The counts exceed the 107-project total because some projects
have more than one source for the same fact.

### Audit

`scripts/pipeline/audit_claims.py` writes `data/derived/claims_audit.csv`. For every
project it checks that the status and every populated numeric fact has a matching
atomic claim:

- status;
- length;
- operational km;
- progress;
- investment (an `investments.csv` row also satisfies this);
- capacity, design capacity or current capacity;
- opening year;
- location or coordinates.

**Result: 107 of 107 projects are fully claimed; no claim gaps.** The Data view
shows the same `107 / 107` figure from the generated payload.

### Honest limits

- **Claim values are not all transcribed.** 264 of the 479 claims carry a
  `claim_value`; 215 point to the source without repeating a short value. The
  value remains on the project row, and the source row is still linked. This is a
  deliberate time trade, not a claim that every number was copied twice.
- **Claim dates are not all stated.** 199 of 479 claims carry a `claim_date`.
  `claim_date` is the date the source states the fact, not the retrieval date.
  The retrieval date lives on `sources.csv` and is always present.
- **Claims are not independent evidence by themselves.** Two claims from the
  same publisher are not "dual" verification. The `verification` field encodes
  the actual rule: 84 projects are official, 8 dual and 15 single-source. The
  single-source rows are named in the phase-2 documents and their notes.
- **The audit checks coverage, not correctness.** A claim can point to a source
  that says something different. The conflict register and the review pass are
  what catch that.

## 3. Q2 — freshness

`scripts/pipeline/freshness.py` writes one row per project and estate to
`data/derived/freshness_report.csv`.

| Rule | Value |
|---|---|
| Fresh | age ≤ 153 days |
| Due soon | 154–183 days |
| Stale | more than 183 days |
| Unknown | no `last_verified` or an invalid date |

**Current report:** 285 rows (107 projects + 178 estates), all `fresh` as of
**2026-11-08**; the next record falls due on **2027-05-08**.

The report is deterministic by default: the as-of date is the newest
`last_verified` in the curated tables. A real monthly check passes an explicit
date (`--as-of` or `INFRAA_AS_OF`), so the result cannot silently float with the
machine clock.

The UI adds a freshness badge to the project drawer (state, plain-language label
and due date) and a freshness field on every project and estate payload. The
Explore freshness filter uses `data_as_of` as its base, not the browser's current
date, so a stale local copy does not suddenly mark every row stale.

**Honest limit:** "fresh" means the row was checked within six months of the
build date. It does **not** mean the row was re-verified on 2026-11-08. Most rows
were curated on 6–8 November; the next refresh is the real test.

## 4. Q3 — Data view v2

The Data view is generated from the curated tables and the build outputs. It now
has:

- **Coverage** — current, target and gap for every layer, with the universe and
  source notes. The 160-vs-179 estate gap and the 178-vs-197 unique-zone gap are
  visible rather than hidden.
- **Claims coverage** — fully claimed projects, total atomic claims, and open
  gaps by fact type.
- **Freshness** — project and estate counts, as-of date, next due date, and a
  list of rows needing attention.
- **What this is** — the verification rule, including the atomic-claim and
  conflict-register behaviour.
- **Status definitions and inclusion rules** — the same vocabulary used by the
  validator.
- **Conflict register** — both values, both publishers, resolution and state.
- **Source register** — every document, its publisher, type, retrieval date,
  snapshot marker and link.
- **Downloads** — filtered project exports plus 13 static files, including the
  offline basemap GeoJSON.
- **Data dictionary** — 189 field definitions across 18 tables, grouped by
  table and downloadable as CSV.
- **Changelog** — parsed at build time from the root `CHANGELOG.md`.

A browser run on 2026-11-08 found 19 conflict rows, 18 dictionary tables, 12
static downloads, 3 filtered export buttons (project CSV, project GeoJSON and,
once the estate table is loaded, estate CSV), 107 / 107 claims coverage, and no
console error. Screenshot: `docs/evidence/phase-3/04-data-desktop.png`.

## 5. Q4 — downloads

| Download | Rows | Scope |
|---|---:|---|
| `projects.csv` / `projects.geojson` | 107 | All projects; static exports |
| `estates.csv` | 178 | All estates and SEZs |
| `estate-gap.csv` | 19 | 179-vs-160 estate reconciliation |
| `corridors.json` | 5 | Trans corridor summaries |
| `corridors-segments.csv` | 44 | Dated corridor segments |
| `events.csv` | 6 | Exact-dated events |
| `sources.csv` | 89 | Source register |
| `claims.csv` | 479 | Atomic project claims, joined to project and source metadata |
| `conflicts.csv` | 19 | Conflict register |
| `freshness.csv` | 285 | Row-level freshness report |
| `dictionary.csv` | 189 | Field-level data dictionary |
| `basemap.geojson` | — | Natural Earth-derived offline basemap |

The first two filtered buttons use the **current Explore filters**. The estate
button uses the current Estates filters. They are generated in the browser from
the same filtered list the user sees, not from a stale server export. The static
downloads live under `site/downloads/`, are relative-path files and work from
`file://`.

Browser-tested on 2026-11-08:

- filtered project CSV: 107 rows, includes `freshness_state`;
- filtered project GeoJSON: 107 Point features;
- filtered estate CSV: 178 rows;
- static `claims.csv`: 479 rows.

## 6. Q5 — conflict register

`data/curated/conflicts.csv` has **19 rows**: 11 `resolved` and 8 `open`.
By scope: 10 project, 8 corridor, 1 dataset. Each row records the subject, the
field, value A and value B, both source ids, a status, a resolution and notes.
`pipeline/validate.py` checks the scope, status, required text, both foreign keys and the
scope-specific subject link.

**Open conflicts (8):**

1. Paiton–Besuki section length: 25.60 km printed vs 26.185 km derived.
2. Trans Papua total vs connected and paved km.
3. Kayu Agung–Palembang–Betung: BPJT split vs the combined atlas row.
4. Demak–Tuban operator: English Wikipedia says `tba`; the Indonesian
   Wikipedia revision names PT. HM Sampoerna Tbk, which looks like an editing
   error; no BPJT row exists.
5. Cilacap–Yogyakarta length: 167.07 km vs 121.75 km.
6. Industrial-estate count: 179 vs 160.
7. Freeport Manyar cathode capacity: 480 ktpa vs the 600–650 ktpa range.
8. Benoa expansion: work reported 100% vs no exact opening date.

**Resolved examples:** the Trans Sumatra 982 km vs 1,051.84 km scope difference;
the BPJT `Operasi` label on Binjai–Langsa; the Makassar–Parepare summary vs
project-page completion; the East Kalimantan railway 2027 vs 2028 target; the
Patimban phase completion; and the Trans Java 1,232.78 vs 1,232.80 rounding.

**Known register gap:** two estate *location* conflicts (IPIP Central vs
Southeast Sulawesi; Tembesi West Kalimantan vs Batam) stay in
`data/derived/estate_gap_2026.csv` because the second side has no source row with
a citable id. They are recorded, but not in the two-source register. Add them
when a second source is saved.

## 7. S1 — build all and local CI

`scripts/build_all.py` runs the pipeline in order:

```text
validate → build_projects → build_dictionary → freshness
         → audit_claims → build_site_data → build_factories_ledger → check_site
```

`--check` hashes **25 generated files** before and after a full rebuild and
fails on any byte change. The 8 November 2026 run reports:

```text
OK: 107 projects, 178 estates, 70 organisations, 89 sources,
    5 corridors, 44 segments, 6 events, 0 geometry, 18 investments, 19 conflicts
OK: 189 field definitions across 18 tables
OK: 285 rows as of 2026-11-08: {'fresh': 285}
OK: 107 projects, 479 claims; 107/107 fully claimed; missing: none
OK: deterministic rebuild, 25 generated files unchanged
```

`generated_on` is deterministic: it uses the newest `last_verified` unless
`INFRAA_BUILD_DATE` is set. The freshness as-of date uses `--as-of` or
`INFRAA_AS_OF`. No git command, remote or deployment is involved.

## 8. S2 — local release build

The site is plain HTML, CSS and classic JavaScript with vendored Leaflet and
local fonts. There is no `fetch`, no XMLHttpRequest, no CDN, no tile server and
no remote font. The site payload is about **1.98 MB** (1,985 KB) raw.

Verified on 2026-11-08:

- `file:///D:/Workspace/infra-id/site/index.html` loads all four views;
- `python -m http.server --directory site` serves the same build;
- 107 projects and 19 conflicts render in both;
- the smoke test recorded **0 external page requests**.

The Data view and the map credits carry the Natural Earth, OpenStreetMap and
Leaflet attribution.

## 9. S3 — smoke tests

`scripts/dev/smoke_site.py` is a development-only Playwright script. It launches
the installed Microsoft Edge in headless mode and checks:

- Explore: 107 projects, 107 header count, sector filter to 13 railways, clear;
- Corridors: 5 cards; Trans Sumatra drawer with 13 segments;
- Estates: 178 rows and the 178-zone count;
- Data: 19 conflicts, 18 dictionary tables, 13 static downloads, 3 filtered
  export controls, 107 / 107 claims;
- project drawer: title, freshness line, source link, Escape close;
- keyboard: first Tab reaches the skip link, Ctrl+K focuses search, Escape
  clears it, ArrowDown moves between rows;
- downloads: project CSV 107, GeoJSON 107 points, estate CSV 178, claims 479;
- `file://` and a local HTTP server;
- no external request, no console error, no page error.

**Result: all checks pass.** Evidence:

| File | What it shows |
|---|---|
| `docs/evidence/phase-3/01-explore-desktop.png` | Explore, map and list |
| `docs/evidence/phase-3/02-corridors-desktop.png` | Five corridor cards |
| `docs/evidence/phase-3/02b-corridor-segments-desktop.png` | Trans Sumatra 13-row segment drawer |
| `docs/evidence/phase-3/03-estates-desktop.png` | 178-row estate table |
| `docs/evidence/phase-3/04-data-desktop.png` | Coverage, claims, freshness and downloads |
| `docs/evidence/phase-3/05-project-drawer.png` | Project drawer with freshness badge |
| `docs/evidence/phase-3/06-explore-mobile.png` | 390 px map and bottom sheet |
| `docs/evidence/phase-3/07-data-mobile.png` | 390 px Data view |
| `docs/evidence/phase-3/smoke-report.json` | Counts, protocols and zero-error record |

Playwright is not in `requirements.txt`; the build and the site do not need it.
If Edge or Playwright is unavailable, the runbook's manual checks are the
fallback and the skip must be recorded.

## 10. S4 — refresh runbook

[`docs/operations/refresh-runbook.md`](../operations/refresh-runbook.md) documents the monthly sequence:
prepare and confirm a clean deterministic build → fetch and snapshot → diff and
triage → update curated rows and atomic claims → update the conflict register →
rebuild → verify locally → commit locally → stop without publishing. It also
lists the source order, the failure modes, the current 2027-05-08 due date and a
monthly checklist.

## 11. S5 — hand-off

Updated on 8 November 2026:

- `README.md` — current counts, trust layer, scripts, data model, site features,
  validation rules, known limitations, roadmap and "Where to pick up".
- `plan-v3.md` — Phase 3 marked complete; evidence and exit criteria recorded.
- `plan.md` — status, phases and next steps aligned with the 107-project build.
- `CHANGELOG.md` — public-facing Phase 3 entry, parsed by the Data view.
- `docs/operations/refresh-runbook.md` — the monthly procedure.
- `docs/phases/phase-3-trust.md` — this evidence log.

The repository is left with **no remote, no push, no Pages workflow and no
published URL**. The local release is `site/index.html` plus the generated
`site/data/` payload.

## 12. Remaining gaps

These are known, documented and not silently patched:

| Gap | Status |
|---|---|
| Industrial-estate count 160 vs Kemenperin's 179 | 19-name gap ledger; Kemenperin endpoint unreachable on 8 Nov 2026 |
| IPIP and Tembesi location conflicts | In the gap ledger; no second source id for the register |
| Estate status is blanket `operating` | Not independently verified for most estates; map layer stays off |
| Estate coordinates | 25 official SEZ points, 20 OSM points, 133 regency centroids |
| Corridor geometry (R6) | `project_geometry.csv` has 0 rows; map shows points only |
| Trans Sulawesi / Trans Kalimantan progress | Route totals only; no operational-km series |
| Trans Java Paiton–Besuki | 26.185 km derived vs 25.60 km printed; open conflict |
| Rail lengths and asset capacity | Not in the Kemenhub deck; documented as a data gap |
| Claim values and dates | 264/479 values and 199/479 fact dates transcribed |
| Open conflicts | 8 of 19; each says what is unresolved |
| Single-source projects | 15 of 107; named in the phase-2 docs and notes |
| Factories without investment | 9 of 27; capacity is design/nameplate, not output |
| 300-marker / 60 fps test | Deferred; 107 markers are clustered and load quickly |
| Lighthouse | Not run; axe-core was run in Phase 1/2, not in this phase |
| Publishing | Explicitly deferred by the repository owner |

## 13. Acceptance check

| ID | Acceptance | Evidence |
|---|---|---|
| Q1 | Status and numeric claims traced to sources | 479 atomic claims; 107/107 fully claimed; `claims_audit.csv` |
| Q2 | Stale report, UI badge, monthly refresh list | `freshness_report.csv`; drawer badge; runbook |
| Q3 | Data view has coverage, methods, sources, gaps, changelog | Data view v2; browser check; screenshot 04 |
| Q4 | Filtered CSV/GeoJSON and data dictionary | Browser-tested 107/107/178/479; `dictionary.csv` |
| Q5 | Known conflicts with both values and sources | 19-row register; 11 resolved, 8 open |
| S1 | `build_all.py`, validation, deterministic rebuild, no push | 25 files unchanged; `--check` passes |
| S2 | `file://` and local HTTP, relative paths, no CDN/tiles | Both protocols checked; 0 external requests |
| S3 | Desktop/mobile screenshots, keyboard, offline | 8 screenshots; smoke report; all checks pass |
| S4 | Monthly fetch → diff → review → update → rebuild → verify | `docs/operations/refresh-runbook.md` |
| S5 | README, changelog and plan current; gaps listed | README, `plan-v3.md`, `plan.md`, `CHANGELOG.md`, this file |

**Exit gate:** met, with the remaining gaps above. The release is local only.
