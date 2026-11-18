# Indonesia Infrastructure Atlas — Remaining Work

**Status:** V4 data baseline complete; sources, indicators, UX and trust work remain.
**Baseline data:** 13 November 2026 build.

## 1. Remaining coverage

| Layer | Current | Target | Remaining |
|---|---:|---:|---:|
| Strategic and private records | 174 | 174 | **0** |
| Sources | 163 | 250 | **87** |
| Indicators | 105 | 300 | **195** |

Everything else is met: 226/226 PSN project and estate records, 24/24 PSN
programmes, 28/28 IKN packages, 314 companies against a 300 target, 204 estates,
35 factories, and the road, rail, airport, seaport and transport targets.

The 400-record reference set is complete: **226 PSN records + 174
strategic/private records**. The project table has 348 rows; 44 PSN records live
in the estate layer and eight share an existing project row, so 400 reference
records correspond to about 392 rows.

## 2. Strategic and private records — complete

The 17 remaining strategic and private records were added in the 13 November
2026 build. See
[`scripts/imports/add_17_strategic_records.py`](scripts/imports/add_17_strategic_records.py).
For future additions, search `projects.csv`, `psn_register.csv` and `estates.csv`
first; upgrade an existing row instead of creating a duplicate.

Acceptance for each record:

- a stable lowercase hyphenated `id`;
- source row with a dated snapshot or an explicit URL-only note;
- status, location and at least one atomic claim;
- bilingual display name and generated summary;
- no duplicate of a PSN, estate or existing project record;
- updated coverage count.

## 3. Sources — 87 documents

Priority order:

1. RPJMN 2025–2029 and the current Bappenas planning documents.
2. KPPIP sector pages for transport, energy, water and industry.
3. Budget speeches and Finance Ministry breakdowns beyond the two PKPN
   snapshots already archived.
4. Official delivery reports for education, health, housing, energy and water.
5. Company annual reports and project disclosures for the strategic records.
6. Missing archives for flagship and road sources currently registered by URL.

Every new source needs publisher, title, URL, publication date, retrieval date,
source type, language, snapshot hash and archive path. If a page cannot be
archived, record why in `notes`. At 13 November 2026, 83 of 163 sources are
URL-only (43 secondary, 24 company, 16 official); archive them or record the
reason before adding more URL-only rows.

## 4. Indicators — 195

Add an indicator only when the source states the name, unit and at least one of:
a baseline, a target or a dated observation. Never infer a target from the
atlas's own fields.

Priority order:

1. Project-level output indicators for IKN, flagships, transport and industry.
2. Ministry baselines and delivery values for education, health, housing, water
   and energy.
3. PKPN delivery values where a dated official release exists.
4. Programme targets only where the source states them.

Rules:

- Record a range as the stated bound and name the bound in `notes`.
- Record "more than X" as X and mark it as a lower bound.
- Do not copy a completion year from a different measure.
- Link every indicator to a programme, a project, or both.
- Add dated observations to `indicator_values.csv` with their own source.
- 17 PKPN indicators still have no dated value; fill them from existing official
  releases before adding new indicators.

## 5. UX workstream

| Pri | Item | Acceptance |
|---|---|---|
| P1 | Editorial summaries | Replace the generated `AUTO` / `OTOMATIS` text for flagships and high-traffic rows with reviewed bilingual summaries; keep the generated text for the long tail. |
| P1 | Mobile bottom navigation | Five-item bottom bar with a `More` item; full-screen filter sheet; 320 px and 390 px with no horizontal overflow. |
| P1 | Project and entity detail pages | Shareable hash routes for projects, programmes and companies, printable and keyboard accessible; the drawer remains the quick view. |
| P1 | Map v3 | Clustering or canvas rendering for 400+ markers, layer toggles, list↔map hover/focus linking, map-only mode and a collapsible rail. Measure frame rate at 300+ markers. |
| P2 | Data table | A general sortable table component and column chooser across Data tables; keep the coverage table's `aria-sort` behaviour. |
| P2 | Search | Fuzzy ranking and arrow-key navigation through grouped results. |
| P2 | Type scale | Complete the 14–16 px body and 12–13 px caption scale across every register view. |
| P2 | Table semantics and print | Captions, scoped headers and a print stylesheet for project and Data pages. |
| P3 | Geometry | Source corridor lines and estate polygons; keep unsourced geometry empty. |

## 6. Trust and evidence

- Resolve or document the 10 open conflicts. Do not pick a winner silently.
- Complete the missing official snapshots listed in section 3.
- Add the seven named 2024 estate additions and upgrade the 18 register-only PSN
  industrial areas with a sourced area, developer, status and boundary where
  possible.
- Geocode the remaining large estates and review the 12 PSN road rows with
  `psn=unknown`.
- 13 company profiles remain reference-only and 132 projects have no
  organisation role; add a role only where a source names one.
- Reconcile the 26-plant total with the published technology breakdown: the
  archived ESDM and GNFI releases give 3,222.75 MW across 26 plants but do not
  state per-plant capacity for 16 of them, so the rows stay blank rather than
  infer a share.

## 7. Priority order

1. **P0 — measurable coverage:** the 87 sources and 195 indicators.
2. **P1 — UX rebuild:** bottom navigation, detail pages, map v3, editorial
   summaries.
3. **P2 — Data and search polish:** column chooser, fuzzy ranking, type scale,
   table semantics, print.
4. **P3 — optional geometry and estate verification.**

## 8. Blockers

| Blocker | Effect | Workaround |
|---|---|---|
| IKN Authority returns HTTP 403 | Cannot cite the primary page directly | Use the archived Top Konstruksi and JournalArta reports of the same OIKN evaluations |
| KPPIP and Bappenas access intermittent | Some sector pages are unarchived | Retry, or use an official ministry mirror and record the substitution |
| RPJMN 2025–2029 not archived | Planning baseline is incomplete | Fetch and hash the official Bappenas document |
| Dishub Sanggau page returns HTTP 500 | Alumina Toba lacks that source | Use GEM and Kemenperin archives already filed |
| Some flagship and road sources are URL-only | Weaker provenance | Archive the page or record why it cannot be archived |

## 9. Invariants

- `data/curated/` is the source of truth. Never hand-edit `data/exports/`,
  `site/data/` or `site/downloads/`.
- Raw snapshots in `data/raw/` are never edited.
- One atomic fact per source claim. Comma-separated claims are rejected.
- No invented status, cost, capacity, target or date.
- PSN matching stays explicit in `data/derived/psn_reconciliation.csv`.
  Register-only records stay visible and labelled.
- Use "reference set", not "universe".
- Every new record needs a source, a status date and a verification level.
- Both locales must be updated together.
- The build is deterministic and offline. No `fetch`, CDN or remote tile server.

## 10. Verification

Run from the repository root:

```bash
python scripts/build_all.py
python scripts/build_all.py --check
python scripts/pipeline/check_site.py
python scripts/dev/smoke_site.py
python scripts/dev/ux_rehearsal.py
python scripts/dev/check_contrast.py
```

A change is complete only when the build is deterministic, the smoke tests pass
in both locales, and the coverage table and dictionary reflect the change.
