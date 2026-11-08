# Changelog

Public-facing changes to the atlas. Dates are the day the change landed in this
repository. The Data view renders these entries from this file at build time.

## 2026-11-09 — PSN register and reconciliation

- Added the official Permenko 16/2025 register: 226 active projects, 24 active
  programmes and 3 deleted slots, with the PDF snapshots and SHA-256 hashes in
  `data/raw/2026-11-09/`.
- Added `data/derived/psn_reconciliation.csv`: 64 direct project matches, 6
  aggregate matches, 3 partial matches, 16 estate matches and 161 open records.
- Added `scripts/pipeline/build_psn_ledger.py` to the deterministic build; it
  fails if the register loses its official counts.
- Renamed the coverage-target `universe` field to `reference_set` so the Data
  view uses plain language. The new PSN rows show 89/226 projects, 0/24
  programmes and 16/44 industrial areas.
- Nothing was pushed, deployed or published.

## 2026-11-08 — Repository cleanup and layout

- Grouped scripts into `pipeline/`, `imports/`, `tools/` and `dev/`, keeping `build_all.py` as the stable entry point.
- Grouped documentation into `plan/`, `phases/` and `operations/`, with indexes in `docs/README.md` and `scripts/README.md`.
- Moved the flat export to `data/exports/projects.csv` and split the site payload into runtime JS in `site/data/` and downloads in `site/downloads/`.
- Exposed `basemap.geojson` as the 13th static download; the built site still works from `file://`.
- Removed the superseded `kek_details.json`, the duplicate Wikipedia HTML snapshot and two uncited BPJT snapshots. No atlas rows or cited evidence changed.

## 2026-11-08 — Phase 3: trust layer and local release

- Split 283 combined claim rows into 479 atomic project claims, one fact per row, and backfilled investment, operational, opening and location claims that were only on the project row.
- Added a 19-row conflict register with both values and both sources, and surfaced it in the Data view and as a CSV download.
- Added a row-level freshness report for 107 projects and 178 estates, with a fresh / due soon / stale state and the next refresh date.
- Added a generated data dictionary covering 189 fields across 18 tables, downloadable as CSV.
- Expanded the Data view with claims coverage, freshness, conflicts, the data dictionary and a generated changelog.
- Added filtered CSV and GeoJSON exports that use the current Explore filters.
- Added `build_all.py` with a deterministic rebuild check, `check_site.py` payload checks, a refresh runbook and a local release hand-off. Nothing was pushed or published.
- Added a repeatable Edge/Playwright smoke test covering all four views, keyboard access, filtered downloads, `file://` and local HTTP. The 8 November 2026 run recorded no console error and no external request.
- Added the monthly refresh runbook and the Phase 3 trust evidence log, with desktop and mobile screenshots under `docs/evidence/phase-3/`.

## 2026-11-08 — Corridors and segments

- Added five Trans corridor definitions and 44 dated segments: 13 Trans Sumatra, 23 Trans Java and 8 Trans Papua.
- Added the 7 September 2026 Gending–Paiton opening and five other exact-dated events.
- Roads reached the 45-corridor target with three planned Trans Sumatra concessions.
- Added corridor segment and event downloads and a four-part stacked bar with coverage states.

## 2026-11-08 — Factories and smelters

- Added 27 plants and smelters: 19 operating, 3 recently completed, 4 under construction and 1 stalled.
- Added 26 organisations and 18 investment rows, with plant or industrial-park coordinates and source claims.
- Recorded capacity for all 27 rows and investment for 18.

## 2026-11-08 — Estates and SEZs

- Reconciled the 179-estate Kemenperin benchmark against the 160-row 2024 table and published a 19-name gap ledger.
- Added OSM/Nominatim coordinates for 20 of the 40 largest industrial estates.
- Kept the estate layer table-only; 25 SEZs use official KEK points and 133 rows use regency centroids.

## 2026-11-07 — Transport PSN

- Added 35 transport PSN projects: 13 railways, 7 airports and 15 seaports.
- Recorded status, opening or target year, operators, aliases and 145 claims from the Kemenhub review of 19 February 2026.
- Documented why the atlas status counts differ from the deck's 29/6 headline.

## 2026-11-07 — Phase 1 experience

- Shipped the four-view shell: Explore, Corridors, Estates and Data.
- Added search, filters, URL state, the detail drawer, the mobile sheet and the v2 map.
- Added the offline Natural Earth basemap, local fonts and the schema-v3 data foundation.

## 2026-11-06 — Data foundation

- Rebuilt the atlas as a normalised curated dataset with sources, claims, organisations, events and coverage targets.
- Added 178 industrial estates and SEZs, 27 toll-road corridors and four Trans corridor summaries.
- Added the generated flat export and the site payload.
