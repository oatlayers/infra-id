# Changelog

Public-facing changes to the atlas. Dates are the day the change landed in this
repository. The Data view renders these entries from this file at build time.

## 2026-11-09 — Data dashboard charts

- Added native sector, status and freshness charts to the full-width Data view.
  Sector bars cover all 14 sectors; the status stack uses the same colours as
  the map and legend; freshness is shown separately for projects and estates.
- No chart library, remote request or new data. The charts read the existing
  `stats.js` payload and are labelled in both locales.
- The UI catalogue grows to 610 keys per locale; the smoke test checks two chart
  panels, 14 sector bars and the legend.
- Build, `--check`, smoke test, five-profile rehearsal, contrast check and link
  check pass. Nothing was pushed, deployed or published.

## 2026-11-09 — Companies and agencies view

- Added a full-width Companies view built from `organizations.csv` and
  `project_organizations.csv`: 101 profiles, 203 sourced role links, 79
  organisations with at least one link and 22 reference-only profiles.
- The view filters by type, searches the role text, expands each profile into
  its project roles with status, sector, share, years and source, and exports
  the filtered CSV. Data adds `companies.csv`, `company-projects.csv` and a
  101/300 coverage row.
- The UI catalogue grows to 604 keys per locale. The smoke test covers the
  English Companies view, the Indonesian tab label and the filtered CSV.
- Initial payload is 1,126 KB, data 1,612 KB and total 3,604 KB. Build,
  `--check`, smoke test, five-profile rehearsal, contrast check and link check
  pass. Nothing was pushed, deployed or published.

## 2026-11-09 — Indicators, values and project phases

- Added `indicators.csv`, `indicator_values.csv` and `project_phases.csv` with
  schema validation, dictionary entries and exports. The seed is deliberately
  small and sourced: the 100 GWp programme target (100 GWp against 5.3 GWp
  current), the Phase 1 target (17 GWp), Nusantara's 3,000 m runway, and nine
  phases including the five dams' 10 July 2026 operation.
- The Programme view now shows a target-versus-current block. The project drawer
  shows indicators and phases with their source. Data adds three downloads and
  an indicators-and-phases section.
- The build checks indicator values, project/programme links, phase dates and
  progress, and the new download files. The dictionary grows to 268 fields
  across 26 tables. The UI catalogue grows to 559 keys per locale.
- Initial payload is 1,099 KB (one locale plus core Explore data), runtime data
  1,467 KB and total 3,428 KB. Build, `--check`, smoke test, five-profile
  rehearsal, contrast check and link check pass. Nothing was pushed, deployed or
  published.

## 2026-11-09 — Bilingual shell and full-width registers

- Added the English and Indonesian editions at `site/en/index.html` and
  `site/id/index.html`, generated from one template, plus a bilingual chooser at
  `site/index.html`.
- Added 541 UI keys per locale in `data/i18n/ui.en.json` and `ui.id.json`, a
  validated `translations.csv` entity layer, `build_i18n.py` and
  `build_locales.py`. The build fails on catalogue drift or a missing programme
  or corridor translation.
- Translated all chrome, statuses, sectors, filters, programmes, corridors,
  estates, Data methods and the language switch. All 228 projects now have an
  Indonesian display name: 140 reviewed names plus the 88 official PSN aliases.
  Every project also has a factual one-sentence summary generated from its
  sourced fields in both locales and labelled `AUTO` / `OTOMATIS`; editorial
  review of those summaries remains open.
- Numbers, dates and coordinates now use `Intl` with `en-GB` or `id-ID`.
  Sourced English text in the Indonesian edition carries `lang="en"` and a
  visible `EN` tag.
- Data, Programmes, Corridors and Estates now use the full content width (max
  1180 px) instead of the 400 px rail. Programme and corridor cards use two
  columns on wide screens.
- Mobile sheet handle now cycles peek → half → full on tap, so filters are
  reachable without discovering the drag gesture.
- Added the design baseline: `docs/design/tokens-v4.md`,
  `docs/design/style-tile.html`, `docs/design/ux-audit-v4.md`,
  `scripts/dev/check_contrast.py` and `scripts/dev/ux_rehearsal.py`.
- The data dictionary grows to 238 fields across 23 tables with
  `translations.csv`. Payload is 1,360 KB runtime / 3,292 KB total, within the
  plan budgets. Build, `--check`, link check, smoke test and the five-profile
  rehearsal pass.
- Nothing was pushed, deployed or published.

## 2026-11-09 — PSN register-only closure

- Closed the remaining PSN coverage at Tier C: 88 active PSN projects and 18
  PSN industrial areas now have a record with the official name, number, sector,
  location and active designation.
- Added 264 project claims (PSN, location and active-in-register status) and 54
  estate claims, plus 88 official Indonesian-name aliases. No implementation
  status, cost, capacity, developer, area or boundary was inferred.
- Added `unknown` status, a `National` island group and five sectors: housing,
  technology, education, tourism and agriculture. The map omits province-centroid
  rows so they are not mistaken for site locations; they remain searchable and
  downloadable.
- `projects.csv` grows from 140 to 228 rows, `estates.csv` from 186 to 204,
  `project_sources.csv` from 599 to 863 claims and `estate_sources.csv` from 61
  to 115. PSN coverage is **226/226** project or estate records and **44/44**
  industrial areas; all 24 programmes remain matched.
- Added `scripts/imports/add_psn_register_records.py` (idempotent) and
  `scripts/tools/build_province_centroids.py`. The ledger now distinguishes
  `matched_register_project` and `matched_register_estate`.
- Updated the 2024 estate audit ledger: IPIP and Pulau Penebang are resolved,
  seven named additions remain open and ten count placeholders are retired. The
  179 industrial-estate target is met by count (186 designations).
- Nothing was pushed, deployed or published.

## 2026-11-09 — PSN industrial-area batch

- Added eight PSN industrial areas to `estates.csv`: Kuala Tanjung, Bantaeng,
  Pomalaa, Huali, Patimban, NEMIE, Pulau Penebang and Alumina Toba.
- Added 11 sources, including the official Kemenperin estate directory (181
  rows), the Pelindo and Waspada reporting on Kuala Tanjung, the DPN and Rebana
  pages on Patimban, the Luwu Timur government page on Huali, Neo Energy on
  NEMIE, ANTARA on Pulau Penebang, Global Energy Monitor on Alumina Toba and
  OpenStreetMap/Nominatim for place points.
- Added 8 developer organisations and 41 atomic estate claims. Seven rows are
  under construction and one is operating; each status has a dated source.
- `estates.csv` grows from 178 to 186 rows, `organizations.csv` from 93 to 101,
  `sources.csv` from 122 to 133 and `estate_sources.csv` from 20 to 61. PSN
  industrial coverage rises from 18/44 to 26/44; overall PSN coverage is
  120/226 with 106 project or estate records remaining.
- Added `scripts/imports/add_psn_industrial_estates.py`; idempotent.
- Nothing was pushed, deployed or published.

## 2026-11-09 — PSN programme layer

- Added `programmes.csv` with all 24 active PSN programmes: official number,
  official Indonesian name, English name, theme, lead agency, bilingual summary
  and source. The importer reads the Indonesian names from `psn_register.csv`
  and fails if the register or programme number set changes.
- Added `programme_projects.csv` with seven structural project links and
  `programme_sources.csv` with 48 atomic claims (PSN status and active status per
  programme). Targets, budgets and indicators are left blank because Permenko
  16/2025 does not state them.
- Added a Programmes view with theme filters, bilingual cards, linked projects
  and sources; a programme register section in Data; and three downloads
  (`programmes.csv`, `programme-projects.csv`, `programme-claims.csv`).
- Extended validation, the data dictionary to 229 fields across 22 tables, the
  site payload checks and the browser smoke test.
- PSN coverage is now 110/226 project or estate records plus 24/24 programmes;
  116 project or estate records remain. Added 10 government organisations.
- Nothing was pushed, deployed or published.

## 2026-11-09 — PSN road completion

- Added nine road rows for the remaining PSN road entries: Kisaran–Tebing
  Tinggi, Jambi–Rengat, Rengat–Pekanbaru, Serpong–Cinere, Cimanggis–Cibitung,
  Teluk Lamong, Patimban access, NPEA and the Bandung inner-city toll.
- Matched PSN 10 and 11 to the existing Padang–Pekanbaru corridor as aggregate
  components, and PSN 12 to the existing Kuala Tanjung–Tebing Tinggi–Parapat row
  as partial coverage. The ledger records both choices.
- Added 17 sources, 2 organisations, 43 claims, 4 investments and 2 events.
  Roads are now 50/50; PSN coverage is 110/226 records (94 to 88 project rows and
  16 to estates); 116 project or estate records and 24 programmes remain.
- The build now reports 140 projects, 122 sources, 599 claims and 30 events.
- Nothing was pushed, deployed or published.

## 2026-11-09 — 2026 flagship batch

- Added 24 flagship records: IKN Phase 2, Nusantara International Airport, Abadi
  Masela LNG, RDMP Balikpapan, the 100 GWp solar programme, the 13 Hilirisasi
  Stage II projects, five dams and the Giant Java Sea Wall.
- Added four sector classes: energy, water, urban and coastal. The map, filters
  and Data view use them automatically.
- Added 14 sources, 11 organisations, 77 atomic claims, 4 investments and 22
  dated events. The build now reports 131 projects, 105 sources and 556 claims.
- Linked nine PSN register records to the new rows: five dams, Masela, the RDMP
  aggregate, the Tanjung Enim DME component and the Jakarta/West Java coastal
  dyke. PSN coverage is now 98/226 records (82 to 77 project rows and 16 to
  estates); 128 project or estate records and 24 programmes remain.
- Extended the factory reference set from 27 to 34 and refreshed the coverage notes.
- Nothing was pushed, deployed or published.

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
