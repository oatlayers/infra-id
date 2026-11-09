# Indonesia Infrastructure Map

A curated, source-linked map of major Indonesian infrastructure. Every project
carries a source and a verification date. The map is deliberately **major and
curated, not exhaustive**.

- **Live data:** 228 projects — 54 toll and PSN roads, 13 railways, 8 airports,
  15 seaports, 34 factories, 24 energy, 66 water, 2 housing, 6 technology,
  1 education, 1 tourism, 1 agriculture, 1 urban and 1 coastal project — plus
  24 PSN programmes, 5 Trans corridor summaries, 44 dated corridor segments and
  30 project events. Of the 228, **88 are register-only PSN rows** with the
  official name, number, sector and province, but no implementation facts yet.
- **Transport PSN:** 35 of 35 represented. Status is as of 19 February 2026, the
  date of the Kemenhub review. The Nusantara airport is an additional national
  gateway, not a PSN row.
- **PSN reconciliation:** the official Permenko 16/2025 list has 226 active
  projects and 24 active programmes. The atlas represents **226 of 226** active
  project/estate records — 94 reviewed records map to 88 project rows, 26 map to
  reviewed estates, 88 are new register-only project rows and 18 are new
  register-only industrial areas — plus all 24 programmes. Every sector is
  complete: roads 50/50, airports 7/7, ports 15/15, railways 13/13, coastal
  defence 1/1, industrial areas 44/44, dams and irrigation 57/57, water and
  sanitation 9/9, energy 18/18, technology 6/6, housing 2/2, agriculture 2/2,
  education 1/1 and tourism 1/1. The register and ledger are
  [`data/curated/psn_register.csv`](data/curated/psn_register.csv) and
  [`data/derived/psn_reconciliation.csv`](data/derived/psn_reconciliation.csv).
- **Factories:** 34 plants and smelters: 19 operating, 3 recently completed,
  11 under construction and 1 stalled. 27 have capacity and 18 have investment.
- **V4 flagships:** IKN Phase 2, Nusantara airport, Abadi Masela LNG, RDMP
  Balikpapan, the 100 GWp solar programme, the 13 Hilirisasi Stage II projects,
  five dams and the Giant Java Sea Wall. Each has a dated source, a claim and a
  project-level note where only a package total was published.
- **PSN road completion:** the 12 remaining PSN road entries are resolved. Nine
  new rows cover the Kisaran–Tebing Tinggi, Jambi–Rengat, Rengat–Pekanbaru,
  Serpong–Cinere, Cimanggis–Cibitung, Teluk Lamong, Patimban access, NPEA and
  Bandung inner-city projects; three are matched to existing rows as aggregates
  or partial coverage.
- **Programme layer:** all 24 active PSN programmes are first-class records with
  an official number, Indonesian and English names, a summary, a theme and a
  source. Sixteen have a lead agency (10 distinct lead organisations) and five
  have at least one structural project link (seven links). Targets, budgets and
  indicators stay blank because the annex does not state them. The layer has its
  own view, download and 48 atomic claims.
- **Estate dataset:** 204 industrial estates and SEZs, shown as a table; the map
  layer is deliberately off until coordinates are verified. The 179
  industrial-estate benchmark is met: 179 pure industrial rows plus 7 shared
  SEZ/estate rows. Eight reviewed PSN industrial areas carry dated area, manager
  and status sources; 18 more are register-only with no invented area or boundary.
- **Companies and agencies:** 101 organisation profiles and 203 sourced project
  roles. 79 organisations have at least one project link; 22 are reference-only.
  The Companies view filters by type, searches the role text, expands each
  profile into its project roles and exports the filtered CSV. The V4 target is
  300 profiles; 199 remain.
- **Trust layer:** 863 atomic project claims, 115 estate claims and 48 programme
  claims; 228 of 228 projects have a claim for the status and every populated
  numeric fact. 19 conflicts are recorded with both values and both sources
  (11 resolved, 8 open). A 432-row freshness report marks each project and
  estate fresh, due soon or stale. A 268-field data dictionary covers all 26
  curated tables, including translations, indicators and project phases.
- **Bilingual shell:** `site/index.html` is a language chooser; `site/en/` and
  `site/id/` share one application and one data bundle. Both locales carry 604
  UI keys, all 24 programme names and summaries, all five corridor definitions,
  and an Indonesian display name for all 228 projects (140 reviewed, 88 official
  PSN aliases). Every project also has a factual one-sentence summary generated
  from its sourced fields in both locales and labelled auto-generated. The
  switch preserves the current hash, filters and selected record. Data,
  Programmes, Corridors, Estates and Companies are full-width register pages;
  Explore keeps the map.
- **Last verification:** 9 November 2026 for the flagship, PSN-road, PSN
  industrial-area and register-only rows; 8 November 2026 for the road, estate
  and factory batches; 7 November for transport; and 6 November for earlier
  rows. The 432-row freshness report is fresh as of 9 November 2026; the first
  record falls due on 11 May 2027.
- **Indicators and phases:** the new `indicators.csv`, `indicator_values.csv`
  and `project_phases.csv` tables carry three sourced indicators and nine
  sourced phases. The 100 GWp programme target (100 GWp, 5.3 GWp current), the
  Phase 1 target (17 GWp) and Nusantara's 3,000 m runway are in the Programme
  and project drawers. The five dams and Nusantara airport have operational
  phases. Targets, budgets and indicators remain blank where the source is
  silent.
- **Payload:** 1,099 KB initial (one locale plus core Explore data), 1,467 KB
  of runtime data and 3,428 KB including downloads, within the plan's 1.5 MB
  initial and 5 MB total budgets.
- **Status:** Phase 1, Phase 2 and Phase 3 of the v3 overhaul are complete as of
  8 November 2026. Track 2B (estates) is complete by count and corridor geometry
  (R6) is deferred; both are documented. The 50-entry PSN road reference set is complete.
  Phase 3 ends with a **local release only**: the site is verified from `file://`
  and a local HTTP server. There is **no GitHub remote, push, Pages deployment or
  published URL**. V4 foundation work started on 9 November 2026 with the PSN
  register, reconciliation ledger, 2026 flagship batch, PSN-road completion, the
  programme layer, the first PSN industrial-area batch, the register-only
  closure of the remaining PSN records and the bilingual shell. The released
  site is still the v3 build; V4 remains local.
- **V4 plan:** [`docs/plan/plan.md`](docs/plan/plan.md) is the current plan: a
  bilingual national delivery atlas with 400+ projects, 226 PSN projects, 24 PSN
  programmes, 8 PKPN programmes, 300 companies, 200 estates and a rebuilt map
  and Data view. It is a plan, not a released build. The completed v3 backlog stays in
  [`docs/plan/plan-v3.md`](docs/plan/plan-v3.md); phase records are in
  [`docs/phases/`](docs/phases/), and the monthly procedure is
  [`docs/operations/refresh-runbook.md`](docs/operations/refresh-runbook.md).

## What it is, and what it is not

It is a static site with four views: **Explore** (map, search, filters and a
detail drawer), **Corridors** (Trans network summaries), **Estates** (the
industrial-estate and SEZ table) and **Data** (coverage, methods, sources,
downloads and known gaps). Projects are coloured by status, filtered by sector,
status, island, province, PSN, corridor, precision and verification age, and
open a drawer with the evidence behind the status, the operator, the length,
every source and the dates.

It is **not** a live project tracker, an official government dataset, or a
complete list of Indonesian infrastructure. Rows are included only when they are
planned, under construction, recently completed, operating or stalled, and only
when a source supports that status.

## Current coverage

| Layer | Rows | Status | Notes |
|---|---:|---|---|
| Toll roads | 54 | 12 operating, 29 under construction, 13 planned | 50 PSN road entries plus four additional toll-road rows |
| Railways | 13 | 6 operating, 5 under construction, 2 planned | 13/13 PSN railways; no rail length or capacity in the source deck |
| Airports | 8 | 8 operating | 7/7 PSN airports plus Nusantara International (IVD), operating as a special airport |
| Seaports | 15 | 11 operating, 1 under construction, 1 recently completed, 2 planned | 15/15 PSN seaports; Patimban Phase I-2 still building, Benoa expansion completed 2025 |
| Transport PSN total | 35 | 24 operating, 1 recently completed, 6 under construction, 4 planned | 35/35; status as of 19 February 2026 |
| PSN projects (active) | 226 | 226 represented, 226/226 | 94 records to 88 reviewed project rows, 26 to reviewed estates, 88 register-only projects and 18 register-only industrial areas; 0 outstanding |
| PSN programmes (active) | 24 | 24 represented, 24/24 | one row per official number; bilingual names and summaries; 48 claims |
| All projects | 228 | 62 operating, 4 recently completed, 55 under construction, 18 planned, 1 stalled, 88 register-only | 54 roads, 13 railways, 8 airports, 15 seaports, 34 factories, 24 energy, 66 water, 2 housing, 6 technology, 1 education, 1 tourism, 1 agriculture, 1 urban and 1 coastal |
| Energy projects | 24 | 1 operating, 8 under construction, 15 register-only | Masela, RDMP Balikpapan, 100 GWp solar and six Hilirisasi Stage II energy projects, plus 15 register-only PSN energy rows |
| Water, dams and irrigation | 66 | 5 operating reviewed, 52 register-only, 9 register-only water and sanitation | Five reviewed dams plus 52 PSN dams/irrigation and 9 PSN water/sanitation rows |
| Other PSN sectors | 10 | 10 register-only | 2 housing, 6 technology, 1 education, 1 tourism and 2 agriculture rows |
| Urban and coastal | 2 | 1 under construction, 1 planned | IKN Phase 2 and the Giant Java Sea Wall |
| Trans corridor summaries | 5 | 5 with km totals; 3 with progress series | Sumatra, Java and Papua have a series; Sulawesi and Kalimantan publish route totals only |
| Corridor segments | 44 | 13 Sumatra, 23 Java, 8 Papua | Section tables only where a published list exists; Sulawesi and Kalimantan are route-total-only |
| Dated events | 30 | 2018–2026 | Exact dates only; month-end approximations are not used |
| Factories | 34 | 19 operating, 3 recently completed, 11 under construction, 1 stalled | 27 capacity figures, 18 investment figures; 17 official, 8 dual, 9 single-source |
| Industrial estates / SEZs | 204 | 179 industrial-only rows, 7 shared rows and 18 SEZ-only rows; 186 industrial-estate designations and 25 SEZs | table view only; 25 official SEZ points, 27 OSM place points, 133 regency centroids, 1 power-station point and 18 province centroids; 179 target met; 19-row 2024 audit ledger |
| Sources | 133 | 53 official, 53 secondary, 27 company | 43 factory-batch sources, 25 individual SEZ profiles, Permenko 16/2025 and 4/2026, the national register, OSM/Nominatim, the corridor series, the 2026 flagship releases, the PSN-road batch, the PSN industrial-area batch and the register-only batch; V4 target 250 |
| Project claims | 863 | 228/228 projects fully claimed | one atomic fact per row; 115 separate estate claims and 48 programme claims; register-only rows claim the listing, location and active designation, not implementation |
| Conflicts | 19 | 11 resolved, 8 open | both values and both sources, with a recorded resolution; downloadable register |
| Freshness | 432 | 432 fresh as of 2026-11-09 | 228 projects + 204 estates; 183-day threshold; next due 2027-05-11 |
| Data dictionary | 268 | 26 tables | generated from the schema; field type, required flag, description, allowed values and example |

**Why the transport status counts differ from Kemenhub's summary.** The deck's
headline says 29 complete and 6 under construction. The atlas uses its own
definitions and the deck's project pages: Patimban, the Java south double track,
Rantau Prapat–Kota Pinang and Lahat–Kertapati still have active work, while the
East Kalimantan railway, MRT East–West, New Palembang Port and Muaro Jambi had no
physical construction. The result is 24 operating, 1 recently completed, 6 under
construction and 4 planned. The full mapping and conflicts are in
[`docs/phases/phase-2-transport.md`](docs/phases/phase-2-transport.md).

**Factory reference set.** The 34 plants are PSN manufacturing projects, the
seven Hilirisasi Stage II plants and private plants with investment of at least
Rp 1 trillion. The list covers copper, nickel, steel, alumina, aluminium,
battery, petrochemical, oleochemical, pulp and fertiliser plants. Industrial
estates and pure mining pits are excluded; KIPI Bulungan is now in the estate
layer, while GEM steel and Hailiang announcements did not meet the dated
status-and-capacity rule. The original 27-plant batch is documented in
[`docs/phases/phase-2-factories.md`](docs/phases/phase-2-factories.md); the seven
Stage II additions are in `scripts/imports/add_flagships.py`.

**Recently completed.** Benoa Port (BMTH), the Amman copper smelter, the SGAR
Mempawah alumina refinery and the Lotte LINE petrochemical complex are the four
`recently_completed` rows. No full toll corridor opened between 2024-11-06 and
2026-11-06, so the road rows stay `under_construction` even where sections
opened. Those section openings are in each row's `notes` and in the six dated
events.

**Corridor series.** Five corridors now publish a kilometre total. Trans Sumatra,
Trans Java and Trans Papua have a progress series and a section table; Trans
Sulawesi (2,000 km) and Trans Kalimantan (3,901 km) publish route totals only,
because no current operational-km series was found. Trans Java is a composite:
1,056.38 km across 20 sections operating by January 2025, plus 23.515 km
Gending–Paiton opened on 7 September 2026, against a 1,232.80 km total. The
Sumatra table is partial (1,667.31 km of 2,854 km, 58.4%); the Papua table covers
the eight Papua-side sections only (2,345.40 km of 4,330 km). No percentage is
estimated where the series is missing. Details are in
[`docs/phases/phase-2-roads.md`](docs/phases/phase-2-roads.md).

## Quick start

The generated site files are committed, so no build step is needed to view the
map.

```bash
# Option 1: open the file directly
#   site/index.html

# Option 2: serve it locally
python -m http.server 8765 --directory site
# then open http://localhost:8765/
```

The page needs **no network**: Leaflet is vendored, project data is loaded from a
JavaScript file instead of `fetch`, and the basemap is bundled GeoJSON. It works
from `file://` and from any static host.

Rebuild and verify the whole pipeline:

```bash
python scripts/build_all.py          # validate, rebuild, site checks
python scripts/build_all.py --check  # fail if a rebuild changes any generated byte
```

The optional browser smoke test needs Playwright and an installed Microsoft Edge;
neither is needed to view or ship the site:

```bash
python scripts/dev/smoke_site.py
```

It checks the four views, keyboard access, filtered downloads, `file://`, a local
HTTP server and the no-network rule, then writes screenshots to
`docs/evidence/phase-3/`. The monthly procedure is
[`docs/operations/refresh-runbook.md`](docs/operations/refresh-runbook.md).

Deep links use hash routes, for example:

```
site/index.html#/project/tol-solo-yogyakarta-nyia
site/index.html#/explore?sector=road&island=Sumatra
site/index.html#/data
```

The old `#project-id` form still opens the project.

## Repository layout

```
infra-id/
├─ README.md
├─ CHANGELOG.md              public change log, parsed into the Data view
├─ requirements.txt          Python dependencies for the data scripts
├─ docs/
│  ├─ README.md              index of plans, phase records, operations and evidence
│  ├─ plan/
│  │  ├─ plan.md             V4 plan: delivery atlas, bilingual UI, data expansion
│  │  └─ plan-v3.md          completed v1-v3 backlog and status
│  ├─ phases/
│  │  ├─ phase-1-decisions.md
│  │  ├─ phase-2-transport.md
│  │  ├─ phase-2-estates.md
│  │  ├─ phase-2-factories.md
│  │  ├─ phase-2-roads.md
│  │  └─ phase-3-trust.md
│  ├─ operations/refresh-runbook.md
│  └─ evidence/phase-3/      desktop/mobile screenshots and smoke report
├─ data/
│  ├─ curated/               editable source of truth (26 tables)
│  ├─ derived/               generated reports, caches and extracted text
│  ├─ exports/projects.csv   generated flat export
│  └─ raw/2026-11-06/        sources as fetched, never edited
├─ scripts/
│  ├─ README.md              index: pipeline, batch importers, tools, dev
│  ├─ data_model.py          shared paths, fields, enums and CSV helpers
│  ├─ build_all.py           local CI and deterministic --check
│  ├─ pipeline/              deterministic build steps
│  ├─ imports/               batch import and extraction tools
│  ├─ tools/                 optional geocoding, migration and claim cleanup
│  └─ dev/smoke_site.py      optional Playwright/Edge browser smoke test
└─ site/
   ├─ index.html             shell, inline SVG sprite and mount points
   ├─ assets/                local CSS, JS, fonts and design tokens
   ├─ data/                  runtime JS payload (works from file://)
   ├─ downloads/             CSV, GeoJSON and JSON downloads
   └─ vendor/                Leaflet 1.9.4 and Leaflet.markercluster 1.5.3
```

**Do not edit `data/exports/projects.csv`.** It is generated from `data/curated/` by
`scripts/pipeline/build_projects.py`. Edit the curated tables and rebuild.

## How the data is built

```
data/curated/*.csv ──► pipeline/validate.py ──► pipeline/build_projects.py
                                                     │
                                                     ▼
                                        data/exports/projects.csv
                                                     │
pipeline/freshness.py, pipeline/audit_claims.py,     ▼
pipeline/build_dictionary.py ─────────► pipeline/build_site_data.py
                                                     │
                                      ┌──────────────┴──────────────┐
                                      ▼                             ▼
                                 site/data/                   site/downloads/
                                 runtime JS                   CSV / GeoJSON
                                      │
                                      ▼
                              pipeline/check_site.py
```

Rebuild and check the normal pipeline:

```bash
python scripts/build_all.py          # validate, rebuild, site checks
python scripts/build_all.py --check  # fail if a rebuild changes any generated byte
```

`build_all.py` runs, in order: `pipeline/validate.py` →
`pipeline/build_psn_ledger.py` → `pipeline/build_projects.py` →
`pipeline/build_dictionary.py` → `pipeline/freshness.py` →
`pipeline/audit_claims.py` → `pipeline/build_site_data.py` →
`pipeline/build_factories_ledger.py` → `pipeline/check_site.py`.

Source-import and extraction scripts are **one-off batch tools**, not part of the
monthly pipeline. Run them only when re-importing their batch; they are
idempotent, but they are not needed to rebuild the site:

```bash
python scripts/imports/build_estates.py           # only when estate sources change
python scripts/imports/extract_estate_gap.py      # 19-row 179-vs-160 ledger
python scripts/tools/geocode_estates.py           # optional; cached OSM results
python scripts/imports/extract_transport_psn.py   # checked Kemenhub extraction
python scripts/imports/build_transport.py         # import the 35 transport rows
python scripts/imports/add_bpjt_psn_roads.py      # 15 missing PSN toll corridors
python scripts/imports/add_factories.py           # import the 27 factory rows
python scripts/imports/add_flagships.py           # import the 24 flagship rows
python scripts/imports/add_psn_backlog_roads.py   # import the nine remaining PSN roads
python scripts/tools/geocode_factories.py         # optional; coordinate cache
python scripts/imports/build_basemap.py           # only when Natural Earth changes
```

What each script does:

| Script | Input | Output | Purpose |
|---|---|---|---|
| `tools/migrate_schema_v3.py` | Old curated tables | Schema-v3 headers and backfilled fields | One-off migration; idempotent enough to re-run |
| `imports/extract_wikipedia_toll_roads.py` | English Wikipedia HTML snapshot | `enwiki_toll_roads_parsed.csv` | Parses the toll-road table; no status decisions |
| `imports/extract_transport_psn.py` | Kemenhub PSN deck, checked transcription | `data/derived/transport_psn.csv` | 35 transport rows with page references and conflict notes |
| `imports/extract_estate_gap.py` | Kemenperin 179 count + 2024 table | `data/derived/estate_gap_2026.csv` | 19-row audit ledger: 2 resolved, 7 named additions open, 10 count placeholders no longer needed |
| `tools/geocode_estates.py` | Top 40 industrial estates + Nominatim | `data/derived/nominatim_estates.json`, updated estate coordinates | One request per second; accepts only industrial-landuse matches |
| `imports/build_transport.py` | `transport_psn.csv` + curated tables | Project, claim, link and alias rows | Idempotent transport import; does not touch roads or estates |
| `imports/add_bpjt_psn_roads.py` | BPJT snapshot + curated tables | 15 new PSN road rows, operators, claims and external IDs | Idempotent; leaves the 27 batch-1 roads in place |
| `imports/add_factories.py` | Factory research + curated tables | 27 plant rows, 43 sources, 26 organisations and 18 investment rows | Idempotent; replaces each factory’s claims on rerun |
| `imports/add_flagships.py` | 2026 flagship research + curated tables | 24 project rows, 14 sources, 11 organisations, 77 claims, 4 investments and 22 events | Idempotent; replaces the flagship rows on rerun |
| `imports/add_psn_backlog_roads.py` | PSN road research + curated tables | 9 project rows, 17 sources, 2 organisations, 43 claims, 4 investments and 2 events | Idempotent; completes the 50-entry PSN road set |
| `imports/add_psn_programmes.py` | Permenko 16/2025 programme annex + curated tables | 24 programme rows, 10 organisations, 7 project links and 48 claims | Reads the official Indonesian names from the register; idempotent |
| `imports/add_psn_industrial_estates.py` | Kemenperin directory + PSN industrial-area sources | 8 estate rows, 11 sources, 8 organisations and 41 claims | Explicit area, manager and status sources; idempotent |
| `imports/add_psn_register_records.py` | Permenko 16/2025 register + existing claims | 88 register-only project rows, 18 register-only estate rows, 264 project claims, 54 estate claims and 88 aliases | Adds only register-supported facts; idempotent and updates its own rows |
| `tools/build_province_centroids.py` | Bundled Natural Earth basemap + curated coordinates | `data/derived/province_centroids.json` | Deterministic province centroids; no network |
| `tools/geocode_factories.py` | Nominatim + factory queries | `data/derived/nominatim_factories.json` | Provenance cache only; does not change curated coordinates |
| `pipeline/build_factories_ledger.py` | Curated project, organisation, link and claim tables | `data/derived/factories_2026.csv` | Frozen review ledger for the 34 factory rows |
| `pipeline/build_psn_ledger.py` | `psn_register.csv` + curated projects, estates and programmes | `data/derived/psn_reconciliation.csv` | Explicit PSN-to-atlas match ledger; fails if the official counts change |
| `pipeline/validate.py` | `data/curated/*.csv` | exit code | Schema, enums, dates, coordinates, foreign keys, events, geometry, atomic claims, programmes, conflicts and coverage checks |
| `tools/normalize_claims.py` | Project and estate claim tables | Split claim rows | One atomic fact per row; backfills missing investment, operational, opening and location claims |
| `pipeline/build_projects.py` | Curated tables + BPJT JSON | `data/exports/projects.csv` | Joins operator and source, fills gaps from BPJT, writes the flat export |
| `imports/build_estates.py` | KEK HTML + BAJRA table + regency cache | `data/curated/estates.csv` + source rows | Merges the 25 SEZs and 153 industrial estates, handles overlaps; run `add_psn_industrial_estates.py` afterwards to restore the PSN rows |
| `pipeline/freshness.py` | Curated projects and estates | `data/derived/freshness_report.csv` | Fresh / due soon / stale by `last_verified`; deterministic as-of date |
| `pipeline/audit_claims.py` | Curated projects and claims | `data/derived/claims_audit.csv` | Checks that status and every populated numeric fact has an atomic claim |
| `pipeline/build_dictionary.py` | Schema field lists | `data/derived/data_dictionary.csv`, `site/downloads/dictionary.csv` | 268 field definitions across 26 tables |
| `pipeline/build_i18n.py` | `data/i18n/ui.*.json`, `translations.csv`, bilingual curated fields | `site/data/i18n.*.js`, `data/derived/i18n_report.csv` | Fails on key drift or a missing programme/corridor translation |
| `pipeline/build_locales.py` | `site/app.html`, `site/chooser.html` | `site/en/index.html`, `site/id/index.html`, `site/index.html` | Rewrites relative paths and the language switch |
| `dev/check_contrast.py` | `site/assets/tokens.css` | console report | WCAG AA check for every asserted token pair |
| `pipeline/build_site_data.py` | Flat projects + curated corridors, estates, sources, conflicts and derived reports | `site/data/*.js` and `site/downloads/*` | Site-ready runtime payload and downloads |
| `pipeline/check_site.py` | Generated payload | exit code | Payload counts, IDs, search coverage, downloads and local-only assets |
| `build_all.py` | The build scripts above | exit code | Local CI order plus deterministic `--check` hashing |
| `dev/smoke_site.py` | Generated site | screenshots and JSON report | Optional Playwright/Edge browser, keyboard, download and offline check |
| `imports/build_basemap.py` | Natural Earth countries, provinces, lakes, rivers, urban areas and places | `site/data/basemap.js`, `site/downloads/basemap.geojson` | Clipped, simplified offline basemap |

`pipeline/build_projects.py` expects the BPJT snapshot in
`data/raw/2026-11-06/bpjt_toll_road_list.json`. If it is missing, re-fetch it
from the API listed below before rebuilding.

## Data model

The curated data is normalised: one entity per row. Multi-province projects use
semicolon-separated province names; every other list has its own table. The full
rationale and target schema are in `docs/plan/plan.md`.

| Table | One row per | Key fields |
|---|---|---|
| `projects.csv` | project | `id`, `name`, `sector`, `status`, `corridor_id`, `island`, km, investment, location, `status_as_of`, `verification` |
| `organizations.csv` | company or agency | `id`, `name`, `org_type`, `country_code`, `parent_id`, `website` |
| `project_organizations.csv` | project–organisation role | `project_id`, `org_id`, `role`, `share_pct`, `source_id` |
| `investments.csv` | commitment or tranche | `project_id`, `investor_org_id`, `amount`, `currency`, `amount_idr_t`, `stage`, `instrument` |
| `sources.csv` | source document | `id`, `publisher`, `title`, `url`, `published_on`, `retrieved_on`, `source_type`, `language`, `archive_path` |
| `project_sources.csv` | project–source claim | `project_id`, `source_id`, one atomic `claim`, `claim_value`, `claim_date` |
| `project_external_ids.csv` | external key | `project_id`, `system`, `external_id` |
| `project_aliases.csv` | project alias | `project_id`, `alias`, `source_id` |
| `project_events.csv` | dated event | `project_id`, `event_date`, `event_type`, `description`, `source_id` |
| `project_geometry.csv` | geometry | `project_id`, `kind`, GeoJSON `geometry`, `precision`, `source_id` |
| `laws.csv` / `project_laws.csv` | regulation / relation | legal basis, kept separate from news |
| `corridors.csv` | Trans corridor | `total_km`, `operational_km`, `construction_km`, `planned_km`, `metric`, `as_of` |
| `corridor_segments.csv` | corridor segment | `segment_type`, section-level km, progress, status, opening year, geometry |
| `estates.csv` | industrial estate or SEZ | `id`, `name`, `type`, `province`, `regency`, `island`, `area_ha`, `developer`, `status`, `coordinate_source`, `source_id` |
| `estate_sources.csv` | estate–source claim | `estate_id`, `source_id`, one atomic `claim`, `claim_value`, `claim_date` |
| `coverage_targets.csv` | coverage layer | `layer`, `label`, `unit`, `target_count`, `reference_set`, `source_id` |
| `conflicts.csv` | source disagreement | `id`, `scope`, `subject`, `field`, `value_a`, `source_a`, `value_b`, `source_b`, `status`, `resolution` |
| `psn_register.csv` | official PSN project or programme | `id`, `kind`, `psn_no`, `sector`, official `name_id`, `location`, `status`, `source_id` |
| `programmes.csv` | PSN programme | `id`, `psn_no`, `name_id`, `name_en`, `theme`, `pkpn_id`, `lead_org_id`, bilingual summaries, `source_id` |
| `translations.csv` | reviewed locale text | `entity_type`, `entity_id`, `field`, `locale`, `text`, `status`, `translator`, `reviewed_on`, `source_id` |
| `programme_projects.csv` | programme–project link | `programme_id`, `project_id`, `role`, `source_id`, `notes` |
| `programme_sources.csv` | programme–source claim | `programme_id`, `source_id`, one atomic `claim`, `claim_value`, `claim_date` |

Project columns (`data/curated/projects.csv`):

| Column | Required | Allowed values / meaning |
|---|---|---|
| `id` | yes | Lowercase, hyphenated, unique. Used in deep links |
| `name` | yes | Project name, English with Indonesian proper names |
| `sector` | yes | `road`, `railway`, `airport`, `seaport`, `factory` |
| `subsector` | no | For example `toll`, `urban_rail`, `new_build`, `expansion`, `smelter`, `steel`, `alumina`, `battery`, `petrochemical`, `pulp`, `fertiliser` |
| `status` | yes | `planned`, `under_construction`, `operating`, `recently_completed`, `stalled` |
| `status_basis` | yes | The evidence for the status, with figures where possible |
| `corridor_id` | no | Links to `corridors.csv` |
| `island` | yes | `Sumatra`, `Java`, `Kalimantan`, `Sulawesi`, `Papua`, `Bali-Nusa Tenggara`, `Maluku` |
| `province` | yes | Province or provinces, semicolon-separated |
| `route` | yes | Route, corridor or location description |
| `length_km` | linear only | Total length; required for roads and railways |
| `operational_km` | no | Length in service |
| `construction_km` | no | Length under construction |
| `progress_pct` | no | Reported progress, 0–100; leave blank if not reported |
| `investment_idr_t` | no | Investment in trillion rupiah |
| `capacity` / `capacity_unit` | no | For airports, ports and factories; set both or neither |
| `psn` | yes | `yes`, `no`, `unknown` |
| `opened_year` | no | Required for `operating` and `recently_completed` |
| `opened_date` | no | Exact opening date when the source gives one |
| `expected_open_year` | no | Target year for planned or under-construction rows |
| `status_as_of` | yes | Date of the evidence behind the current status |
| `verification` | yes | `official`, `dual`, `single`, `unverified` |
| `lat`, `lon` | yes | Decimal degrees, inside 95–141°E and 11°S–6°N |
| `precision` | yes | `exact`, `approximate`, `regency`, `province` |
| `last_verified` | yes | Date the row was last checked (`YYYY-MM-DD`) |
| `notes` | yes | Conflicts, caveats, section openings, coordinate overrides |

The flat export adds `operator`, `source_url`, `source_type` and `retrieved_on`,
joined from the curated tables.

Status definitions:

| Status | Meaning |
|---|---|
| `planned` | Designated (PSN or KPBU) or tender announced; no groundbreaking |
| `under_construction` | Contract signed or groundbreaking held; latest evidence under 12 months old |
| `operating` | Major asset already in service, opened before 2024-11-06. Context, not a recent completion |
| `recently_completed` | Opened on or after 2024-11-06 |
| `stalled` | Officially delayed or reported stalled (*mangkrak*) |

## Sources

Each source is a row in `data/curated/sources.csv` with a dated snapshot where
possible.

| Source | URL | Used for | Caveats |
|---|---|---|---|
| BPJT toll-road API | <https://itrams-api.bpjt.pu.go.id/v1/reference/api/toll-road-list> | Official status, operating/construction km, operator, endpoint coordinates | 77 operating or partly operating rows; construction-only rows absent; status labels inconsistent |
| English Wikipedia, "Indonesian Toll Road System", revision 1329385293 (2025-12-25) | <https://en.wikipedia.org/w/index.php?oldid=1329385293> | Route names, lengths, operators, status markers | Secondary and stale in places; no coordinates or opening years |
| Indonesian Wikipedia, "Daftar jalan tol di Indonesia", oldid 30025554 (2026-10-03) | <https://id.wikipedia.org/w/index.php?oldid=30025554> | Cross-check of lengths, operating km and concessions | Secondary; figures often differ from BPJT |
| Kemenhub, "Capaian Progres PSN Sektor Transportasi" (19 Feb 2026) | <https://ppid.kemenhub.go.id/fileupload/informasi-berkala/20260406102830.R1_19022026_Update_PSN_Kemenhub_compressed.pdf> | Transport PSN status, opening years, progress, investment | 35 transport PSNs; 29 complete or operating, 6 in construction |
| KPPIP PSN pages | <https://kppip.go.id/proyek-strategis-nasional/> | Airport, seaport and industrial-area PSN lists | Names and provinces only; status must come from elsewhere |
| Hutama Karya via Palpres (4 Oct 2026) | <https://palpres.disway.id/news/read/780474/hutama-karya-buka-bukaan-soal-jtts-di-hadapan-bakn-dpr-ri-ini-progresnya> | Trans Sumatra km | Secondary; figures differ by scope and date |
| BPJT section list via detikFinance (26 Jan 2025) | <https://finance.detik.com/infrastruktur/d-7750531/tol-trans-jawa-belum-tersambung-penuh-masih-ada-sisa-ruas-ini> | Trans Java 20-section operating series | Secondary reporting of BPJT data; article prints 1,232.78 km, section sum is 1,232.80 km |
| Kementerian Sekretariat Negara (20 Dec 2018) | <https://setneg.go.id/baca/index/presiden_resmikan_4_ruas_jalan_tol_trans_jawa_di_jawa_timur> | East Java section-opening event | Official; one event covers four sections and is attached to the Ngawi–Kertosono–Kediri row |
| Katadata (21 Jul 2025) | <https://katadata.co.id/berita/industri/687e4748a975f/tni-targetkan-proyek-trans-papua-rampung-di-era-prabowo> | Trans Papua km | Secondary; connected vs paved metrics differ |
| Wikipedia Trans corridor revisions (2026) | <https://en.wikipedia.org/wiki/Trans-Papua_Highway> | Trans Java, Sulawesi, Kalimantan and Papua definitions, section lengths and opening years | Secondary; used for discovery and cross-checks, never for a status change |
| KEK National Council profiles (25 pages) | <https://kek.go.id/id/investment/distribution> | SEZ name, address, coordinates, area, developer, legal basis, category | Official; one page per zone. Operational maturity is not stated |
| Kemenperin estate directory (2026) | <https://kemenperin.go.id/kawasan> | Industrial estate name, manager, regency/province and land area | Official; 181 rows. It does not state operational status or coordinates |
| BAJRA, "Daftar Kawasan Industri Indonesia" (17 Aug 2024) | <https://www.bajra.id/2024/08/daftar-kawasan-industri-indonesia.html> | Industrial estate name, developer, regency, province, area | Secondary mirror of Kemenperin data; 159 estates, not the 179 reported in 2026 |
| PSN industrial-area batch (2024–2026) | Pelindo, Waspada, DPN, Rebana, Indonesiana, Luwu Timur, Neo Energy, ANTARA, GEM and OSM/Nominatim | Area, manager, status and place points for Kuala Tanjung, Bantaeng, Pomalaa, Huali, Patimban, NEMIE, Pulau Penebang and Alumina Toba | Each row names its own dated source; developer master-plan areas can exceed the licensed Kemenperin area |
| ANTARA, Kemenperin estate count (2026) | <https://www.antaranews.com/berita/5627392/kemenperin-catat-kawasan-industri-serap-235-juta-pekerja> | Coverage benchmark: 179 estates, 101,351.45 ha, 57.20% occupancy | Secondary; used only as a benchmark, not as a row source |
| Natural Earth 1:50m countries, provinces, lakes, rivers, urban areas and populated places | <https://www.naturalearthdata.com/> | Basemap layers and city labels | Public domain; clipped and simplified |

Raw snapshots are never edited. Current contents include the Wikipedia
snapshots, the BPJT JSON, the Kemenhub PDF, the KPPIP HTML pages, the 25 KEK
profile pages, the BAJRA estate table and the Natural Earth GeoJSON under
`data/raw/2026-11-06/`; Permenko 16/2025 and 4/2026, the Kemenperin directory and
the PSN industrial-area sources under `data/raw/2026-11-09/`.

The KPPIP pages and the Kemenhub PSN deck are saved for the transport batch and
are reflected in the 35 transport rows. Factory sources are the 43 source rows
listed in the source register and mapped in
[`docs/phases/phase-2-factories.md`](docs/phases/phase-2-factories.md): company and official
pages for capacity, location and status, plus secondary reporting for ramp-up,
investment and disputes. The coordinate checks use Nominatim; the cached
responses are in `data/derived/nominatim_factories.json`. The corridor batch adds
the Hutama Karya statement, the BPJT Trans Java section list, the Setneg East
Java opening, the Katadata Trans Papua report and the Trans corridor Wikipedia
revisions. Its mapping and conflicts are in
[`docs/phases/phase-2-roads.md`](docs/phases/phase-2-roads.md).

## Languages

The app has one source template and two generated entry points:

```
site/index.html      language chooser (plain HTML, no account or redirect)
site/en/index.html   <html lang="en">
site/id/index.html   <html lang="id">
```

UI strings live in [`data/i18n/ui.en.json`](data/i18n/ui.en.json) and
[`data/i18n/ui.id.json`](data/i18n/ui.id.json). Entity overrides live in
[`data/curated/translations.csv`](data/curated/translations.csv). Programmes
already carry `name_id`/`name_en` and bilingual summaries; project aliases carry
the 88 official Indonesian PSN names; corridor definitions are translated in
`translations.csv`.

`scripts/pipeline/build_i18n.py` fails if the two catalogues drift or if a
programme or corridor loses a required translation. It writes a coverage report
to `data/derived/i18n_report.csv`. The current build has 604 UI keys per locale,
an Indonesian display name for all 228 projects and a generated summary for all
228. Project summaries are generated from the curated fields, not editorial
copy; the drawer labels them `AUTO` / `OTOMATIS`. Sourced English notes keep an
`EN` tag rather than pretending to be translated.

Numbers, dates and coordinates use `Intl` with `en-GB` or `id-ID`. The header
switch preserves the current view and hash. Sourced English text inside the
Indonesian edition carries `lang="en"` and a small `EN` tag.

## Estates and SEZs

`data/curated/estates.csv` holds 204 records, gathered but deliberately **not
visualised yet**:

- **25 SEZs** from the official KEK National Council profiles. Each has a name,
  address, province/regency, official zone coordinate, area in hectares,
  developer, legal basis, establishment year and category.
- **179 industrial-only estates**: 153 from the 2024 Kemenperin-derived list,
  8 reviewed PSN industrial areas and 18 register-only PSN industrial areas.
  The older rows carry a developer, regency/province and area, with regency/city
  centroids; the reviewed PSN batch has a dated area, manager, status and
  place-level coordinate source. The register-only batch has the official name,
  province and PSN number only.
- **7 zones are both** a SEZ and an industrial estate; they are one row with
  `type=both`, not duplicates.
- **18 SEZ-only zones** complete the 204-row total.

The 2024 industrial-estate source is a secondary mirror of Kemenperin data.
Kemenperin reported 179 estates in 2026, and the official directory now in
`data/raw/2026-11-09/kemenperin_kawasan.html` lists 181 rows. The atlas has 186
industrial-estate designations (179 pure rows plus 7 shared), so the 179 target
is met. SEZ rows use `status=operating` as a designation-level default;
operational maturity is not independently verified. The eight reviewed PSN rows
use dated status claims. The 18 register-only rows use `status=unknown` and a
province centroid; no area, developer or boundary is invented.

Estate fields:

```
id,name,type,province,regency,island,lat,lon,precision,coordinate_source,
area_ha,developer,developer_org_id,status,sector_focus,legal_basis,
established_year,website,occupancy_pct,kemenperin_id,sez_id,source_id,
last_verified,notes
```

`type` is `industrial_estate`, `sez` or `both`. `coordinate_source` is
`official`, `osm`, `regency`, `manual` or `unknown`. The site reads the table
into `site/data/estates.js`; the map layer is still gated on verified
coordinates.

**Known gap.** The 179 count is met, but seven named 2024 additions still lack an
individual source: I-Sentra Lamongan, Huadi Bantaeng, Cikembar II, Losarang,
Purwakarta Integrated Industrial Park, Seafer and Tembesi. The 2024 audit ledger
also retains ten count placeholders that are no longer needed. IPIP and Pulau
Penebang are resolved. The 18 register-only PSN industrial areas still lack an
area, developer, implementation status and boundary; those facts need an
individual official or company source rather than a copied press release.

## Adding or updating a project

1. Save the source snapshot to `data/raw/<YYYY-MM-DD>/` (raw, unedited).
2. Add a row to `data/curated/sources.csv` if the source is new.
3. Add or edit the project in `data/curated/projects.csv`.
4. Link the source in `data/curated/project_sources.csv` with **one atomic claim
   per fact**: `status`, `length`, `operational`, `opening`, `investment`,
   `capacity`, `location`, `coordinates`, `operator`, `target` or `progress`.
   Never use a comma-separated claim; validation rejects it.
5. Add the operator/sponsor to `organizations.csv` and link it in
   `project_organizations.csv`. Do not put company names in `projects.csv`.
6. Set `status_basis` to the actual evidence, not just the status word. Include
   figures (km operational, completion date, decree number) where possible.
7. Set `island`, `status_as_of`, `last_verified` and `verification` (`official`,
   `dual`, `single` or `unverified`).
8. Put disagreements and caveats in `notes`, and add a row to
   `data/curated/conflicts.csv` when two sources disagree. Do not resolve
   conflicts silently.
9. Run the whole pipeline:

   ```bash
   python scripts/build_all.py
   python scripts/build_all.py --check
   ```

10. Reload the page and check the marker, the drawer freshness badge, the filters,
    the Estates table and the Data view (claims, freshness, conflicts, dictionary).
11. Update this README, the changelog and any affected phase document if the
    coverage, schema or behaviour changed.
12. Commit the curated rows, rebuilt exports and site data together. Do not push.

Rules that apply to every row:

- A status change needs an official source, or two independent sources.
- Coordinates must be plausible; prefer official or site-specific points over
  city centres.
- A row not re-checked within six months should be treated as unverified.
- Do not include test, placeholder or duplicate entries.
- Use only the status values above.
- Keep `data/exports/projects.csv`, `site/data/` and `site/downloads/` generated;
  never hand-edit them.
- Every populated status and numeric fact needs a matching atomic claim. Check
  `data/derived/claims_audit.csv` after a build; it must say `missing=none`.

## The site

`site/index.html` is the shell; CSS and JavaScript live under `site/assets/`.
Features:

- **Explore:** search across name, province, corridor and operator; sector,
  status, island, province, PSN, corridor, precision and freshness filters;
  five sort modes; URL state; map/list selection; keyboard navigation.
- **Map:** Natural Earth provinces, lakes, rivers, urban areas and city labels;
  sector glyphs inside status-coloured markers; status-ring clusters below zoom
  7; selected marker label; drawer-aware panning. The map is inert while the
  modal detail drawer is open.
- **Transport:** 35 PSN railways, airports and seaports with status, opening or
  target year, investment where stated, aliases and source claims.
- **Factories:** 34 plants and smelters on the map with a factory glyph, capacity
  and investment figures, operators, status basis and every source claim.
- **Energy, water, urban and coastal:** Masela, RDMP Balikpapan, the 100 GWp solar
  programme and six Stage II energy projects; five dams; IKN Phase 2; and the
  Java sea wall, each with its own glyph and source claims.
- **Detail drawer:** key figures, operational share, why-this-status, evidence,
  every source with claim and retrieval date, a freshness badge with the next
  due date, notes, related corridor, a project timeline where a dated event
  exists, previous/next and share.
- **Corridors:** five Trans corridors with km bars, a four-part legend, segment
  tables, grouped timelines, as-of dates, sources and explicit coverage states:
  complete series, partial segment table, route total only and no series.
- **Programmes:** all 24 active PSN programmes with theme filters, bilingual
  names and summaries, lead agency, PKPN mapping, linked projects and source,
  plus an explicit target gap.
- **Estates:** 204-row table with type/province filters, sort, inline detail,
  area totals, coordinate provenance, a filtered CSV button and CSV downloads
  (including the 19-row 2024 audit ledger). No map layer yet.
- **Data:** generated coverage matrix; programme register; claims coverage;
  freshness; status definitions; inclusion rules; conflict register with both
  values and sources; source register; 21 static downloads plus filtered project
  CSV/GeoJSON and estate CSV; the 268-field data dictionary; known gaps; and the
  changelog parsed from `CHANGELOG.md`.
- **Mobile:** full-viewport map and a draggable bottom sheet with peek, half and
  full snap points; filters stay in the sheet.
- **Offline:** no tile server, CDN or `fetch`. Leaflet and markercluster are
  vendored; fonts and all payloads are local; the page works from `file://`.

Deep links are hash routes:

```
site/index.html#/explore?sector=road&status=under_construction&island=Sumatra
site/index.html#/project/tol-bekasi-cawang-kampung-melayu
site/index.html#/corridors/trans-sumatera
site/index.html#/estates?type=sez
site/index.html#/data
```

The basemap is Natural Earth 1:50m geometry clipped to 92–144°E, 14°S–9°N and
simplified for offline use. It shows land, Indonesian provinces, lakes, rivers,
urban areas and major cities — not roads, terrain or small settlements. This is
a deliberate trade for reliability: OpenStreetMap's tile servers block
`file://` pages.

## Validation and quality rules

`python scripts/pipeline/validate.py` checks:

- every curated table has the expected header;
- required fields are present and enums are valid;
- dates are real `YYYY-MM-DD` values and years are plausible;
- ids are unique, lowercase and hyphenated;
- every foreign key resolves (project, organisation, source, corridor, law,
  estate, event, geometry);
- every project has at least one source claim;
- each source claim is one atomic type from the allowed set; comma-separated
  claims are rejected;
- each conflict has a valid scope and status, both source foreign keys and the
  subject link required by its scope;
- km figures are non-negative and do not exceed the total by more than 5%;
- roads have a `length_km`; a railway may omit it when the official source gives
  no km figure, but a km breakdown still requires a total;
- coordinates fall inside Indonesia's rough bounding box;
- operating and recently completed rows have an `opened_year`, and target years
  may run to 2040;
- `island`, `status_as_of` and `verification` are present and valid;
- estates have valid type/status/island/coordinate-source enums, positive area,
  plausible coordinates and a known source;
- estate–source claims, project events, project aliases and project geometry
  have valid foreign keys;
- project geometry is valid JSON;
- archive paths exist when they point into the repo;
- coverage targets are unique, positive and reference a known source when one is
  supplied;
- no duplicate project–organisation roles, external ids, aliases or claims.

Validating is not the same as verifying. Validation catches malformed rows; the
`status_basis`, `notes`, atomic claims and conflict register are what make a
project trustworthy.

The local CI gate adds three checks on top of validation:

```bash
python scripts/build_all.py --check       # 26 generated files must be byte-identical
python scripts/pipeline/check_site.py     # payload counts, IDs, search, downloads, offline assets
python scripts/dev/smoke_site.py          # optional browser, keyboard and download smoke test
```

`build_all.py --check` is the drift check. `scripts/pipeline/check_site.py` verifies that the
browser payload matches the curated tables and that no app asset uses `fetch`, a
CDN or a remote URL. `scripts/dev/smoke_site.py` is optional and needs Playwright plus Edge;
it writes screenshots and a zero-error report under `docs/evidence/phase-3/`.

## Known limitations

- **Corridor-level, not section-level.** A corridor with one open section and one
  section under construction is `under_construction`; the open section is in
  `notes`.
- **Approximate coordinates.** Batch 1 uses the midpoint of each BPJT endpoint
  pair, so every road row is `precision=approximate`. Bogor Ring Road uses Bogor
  city centre because the BPJT endpoints are misplaced. Most transport points
  are airport, port, road-midpoint or city reference points (Nusantara airport
  and the Teluk Lamong flyover are exact), and the 34 factory points are plant
  or industrial-park locators, not surveyed boundaries.
- **Mixed source quality.** 32 road rows are BPJT-backed (`official`); 13 rely on
  Wikipedia or a single secondary source. All 35 transport rows are backed by the
  Kemenhub deck, but that deck does not give rail lengths or asset capacity. The
  factory batch draws on 43 source rows: 23 company, 18 secondary and 2 official;
  Dexin and Huadi are single-source.
- **Claim coverage is not claim correctness.** 228/228 projects have the required
  atomic claims, but the 88 register-only rows claim only the PSN listing,
  location and active designation; they do not claim implementation status, cost
  or capacity. Twenty-eight reviewed projects are single-source. The audit proves
  coverage, not that every source agrees.
- **Freshness is a date check, not a live re-verification.** All 432 rows are
  fresh as of 9 November 2026 because they were curated in the 6–9 November
  batches. The first record falls due on 11 May 2027; the monthly runbook is the
  real test.
- **BPJT labels are inconsistent.** Some rows marked `Operasi` still have
  unopened length or active construction. Conflicts are recorded, not hidden.
- **Programme targets and budgets are not in the annex.** All 24 programmes are
  recorded, but only the official name and active status are claimed. Sixteen
  have a lead agency (10 distinct organisations) and five have structural project
  links (seven links); targets, budgets and indicators remain open.
- **No geometry.** Projects are points, not lines or polygons. `project_geometry`
  exists but is empty.
- **Factory figures are nameplate or project-level.** Capacity is not verified
  output. Investment is total project capex where the source gives one; 16 of 34
  factory rows have no investment figure. USD values are converted at
  Rp 16,500/USD for ranking, not at a transaction-date rate, except Masela and
  RDMP, which use the reported rupiah equivalents.
- **Factory coordinates are mixed.** 18 rows use an OSM/Nominatim point and 9 use
  a manual approximate plant or park point. Where Nominatim returned a village,
  estate or access point, that point is used instead of a plant boundary.
- **Corridor segments are partial.** 44 sections are recorded: 13 Trans Sumatra,
  23 Trans Java and 8 Trans Papua. Sumatra covers 1,667.31 km of the 2,854 km plan
  (58.4%); Papua covers the eight Papua-side sections (2,345.40 km of 4,330 km).
  Trans Sulawesi and Trans Kalimantan publish route totals only, with no segment
  table.
- **Trans Java is a composite series.** 1,056.38 km across 20 sections operating
  by January 2025 plus 23.515 km Gending–Paiton opened on 7 September 2026.
  Paiton–Besuki is derived as 26.185 km (49.70 − 23.515), while the section list
  prints 25.60 km, a 0.585 km discrepancy recorded in the notes.
- **Event coverage is still thin.** Thirty exact-dated events are recorded,
  including the 2026 flagship groundbreakings and openings. Month-end
  approximations were rejected, so most section openings remain in project notes
  rather than on a timeline.
- **Transport status is dated.** It reflects the Kemenhub review of 19 February
  2026, not a live check. `last_verified` is the curation date.
- **PSN status is incomplete for roads.** 12 of 54 road rows have `psn=unknown`; the 50-entry PSN road set is separately matched in the ledger.
- **Estate coordinates are mixed.** 25 SEZ/shared zones use official KEK points,
  27 industrial areas use OSM/Nominatim place points, 133 still use regency
  centroids, one uses a power-station point and 18 register-only PSN areas use
  province centroids, not estate boundaries. 20 of the 40 largest were geocoded
  against industrial landuse; the rest had no reliable OSM match.
- **Estate coverage is complete by count, not by fact.** The table has 186
  industrial-estate designations against Kemenperin's 179, so the target is met.
  The 19-row 2024 audit ledger is downloadable: 2 resolved, 7 named additions
  still open and 10 count placeholders no longer needed. The 18 register-only PSN
  areas still lack area, developer, status and boundary. The Kemenperin directory
  was snapshotted on 9 November 2026.
- **Estate status is mixed but still mostly defaulted.** The 160 older
  industrial-estate designations (153 pure rows plus 7 shared) carry the
  directory default `operating` and have not been individually re-verified. The
  eight reviewed PSN rows carry dated status claims: seven under construction and
  one operating. The 18 register-only PSN rows carry `status=unknown`. Sector
  focus, website, legal basis and established year are mostly blank.
- **Register-only PSN rows are not implementation records.** 88 projects and 18
  industrial areas have the official name, number, sector, location and active
  status only. Their province centroids are excluded from the map so they are not
  mistaken for site locations. They remain searchable and downloadable, and the
  ledger labels them separately.
- **No recently completed toll roads.** The four `recently_completed` rows are
  Benoa Port and three factories; see Current coverage.
- **Trans Sulawesi and Trans Kalimantan have route totals but no progress
  series.** The atlas publishes 2,000 km and 3,901 km respectively and says so
  explicitly. No percentage is estimated: competing definitions include a 1,186 km
  travel route, a 1,920 km border-parallel road and a 2,100.8 km WPS figure for
  Kalimantan, and the 3,900 km figure for Sulawesi refers to the wider road
  network.
- **Incomplete reference set.** Construction-only and pre-construction BPJT rows are
  not returned by the API. The 45-corridor target now includes three planned
  0-km Trans Sumatra concessions, but the wider 0-km reference set is not enumerated.
- **Excluded for now:** the three planned strait bridges (Bali, Malacca, Sunda),
  non-toll PSN roads and bridges, and announced factories that lack a dated
  status-and-capacity source (for example GEM steel and Hailiang).
- **Wikipedia is secondary.** It is useful for discovery and cross-checking, not
  as the final authority on a status change.
- **Conflict coverage is not exhaustive.** The register has 19 rows and 8 open
  conflicts. The IPIP location conflict is resolved; Tembesi remains in the
  2024 audit ledger because the second side has no citable source row. Free-text
  `notes` still carries context that is not in a structured field.
- **Performance at 300 markers is untested.** The 228-project dataset has 139
  mapped markers and loads quickly, but the 300-marker 60 fps target still needs a
  dedicated measurement run and a larger mapped set.
- **Lighthouse is not run.** axe-core 4.10.3 with WCAG A/AA tags reports zero
  violations on Explore and Corridors at 1440 px and 390 px, and on the project
  drawer. The map is inert while the modal drawer is open; the list is the
  accessible equivalent. The Phase 3 browser smoke test checks keyboard basics
  and console errors, not a Lighthouse score.
- **Local release only.** There is no GitHub remote, no push and no Pages
  deployment. The site is verified from `file://` and a local HTTP server; that is
  the intended Phase 3 release. Do not publish without an explicit reversal from
  the repository owner.

## Roadmap

1. ~~Plan, decisions, toll-road batch, map page.~~ Done.
2. ~~Normalised data foundation, km fields, operating status, corridor tab.~~ Done.
3. ~~Phase 1: design foundation, four-view shell, search, filters, drawer, map v2,
   mobile sheet, data page, schema v3.~~ Done 7 November 2026.
4. ~~Phase 2: data completion.~~ Done 8 November 2026. Transport PSN (13 rail,
   7 airports, 15 seaports), the 27-plant factory reference set and the road/corridor
   batch are complete. Roads meet the 45-corridor target; five corridors carry 44
   segments and six exact-dated events. Estates: the 179 count is met, 20 of the
   40 largest are geocoded, eight PSN industrial areas have dated sources and 18
   more are register-only; seven named 2024 additions remain open and ten count
   placeholders are retired. Corridor geometry (R6) is deferred.
5. ~~Phase 3: trust and local release.~~ Done 8 November 2026. 479 atomic
   claims, 107/107 projects fully claimed, a 19-row conflict register, a 285-row
   freshness report, a 200-field dictionary, Data view v2, filtered downloads,
   local CI, a browser smoke test and hand-off. **No GitHub push, remote, Pages
   deployment or public release.**
6. **V4 foundation, flagships, PSN roads and programmes.** In progress, started
   9 November 2026. The Permenko 16/2025 register and reconciliation ledger are
   in place. The flagship batch adds IKN Phase 2, Nusantara airport, Masela, RDMP
   Balikpapan, 100 GWp solar, 13 Hilirisasi Stage II projects, five dams and the
   Java sea wall. The PSN-road batch closes the last 12 road entries, taking
   roads to 50/50. The programme layer adds all 24 active PSN programmes with
   bilingual names, summaries, lead agencies and 48 claims. The register-only
   batch closes the remaining 88 projects and 18 industrial areas at Tier C,
   taking PSN coverage to 226/226 and 44/44. The target remains 400+ projects,
   300 companies, 200+ estates and a bilingual shell.
7. **Monthly refresh.** Follow [`docs/operations/refresh-runbook.md`](docs/operations/refresh-runbook.md):
   re-fetch sources, review status changes, update `last_verified`, rebuild and
   verify locally.
8. **Publishing (deferred).** Only if the repository owner explicitly asks. Until
   then, the local `site/` build is the release.

## Where to pick up

- **Current plan:** [`docs/plan/plan.md`](docs/plan/plan.md). V3 is complete as
  of 8 November 2026; V4 has its foundation, PSN ledger, 2026 flagship batch,
  50-entry PSN road set, 24-programme layer, first PSN industrial-area batch and
  the register-only closure of PSN coverage and the bilingual shell. Project
  summaries, company-profile expansion and strategic non-PSN expansion are
  still open. Track 2B (estates) is complete by count and R6
  geometry is deferred; both are documented. Publishing is explicitly deferred.
- **Next action:** run `python scripts/build_all.py --check`, read
  [`docs/operations/refresh-runbook.md`](docs/operations/refresh-runbook.md),
  then continue the V4 immediate actions in `docs/plan/plan.md` (run the
  five-user UX audit, extend the schema with indicators and phases, and expand
  strategic non-PSN records). Do not push, add a remote or deploy.
- **Trust layer:** [`docs/phases/phase-3-trust.md`](docs/phases/phase-3-trust.md) records the
  claims audit, freshness report, conflict register, Data view v2, downloads,
  build CI and smoke-test evidence. The generated files are
  `data/derived/claims_audit.csv`, `data/derived/freshness_report.csv` and
  `data/derived/data_dictionary.csv`.
- **Phase 1 decisions:** [`docs/phases/phase-1-decisions.md`](docs/phases/phase-1-decisions.md).
- **Transport PSN batch:** complete. The checked 35-row extraction is
  `data/derived/transport_psn.csv`; the importer is
  `scripts/imports/build_transport.py`; the mapping and conflicts are in
  [`docs/phases/phase-2-transport.md`](docs/phases/phase-2-transport.md).
- **Factories:** Track 2C complete for the original 27-plant reference set and
  extended to 34 by Hilirisasi Stage II. The ledger is
  `data/derived/factories_2026.csv`, the importers are
  `scripts/imports/add_factories.py` and `scripts/imports/add_flagships.py`, and
  the inclusion log and conflicts are in
  [`docs/phases/phase-2-factories.md`](docs/phases/phase-2-factories.md). Next:
  plant geometry, milestone events and a dated status check for GEM steel,
  Hailiang and other announced plants.
- **Roads and corridors:** 45 of 45 target corridors. Track 2D added 15 PSN
  corridors and three planned Trans Sumatra concessions, defined five corridors,
  built 44 segments and recorded six events. The mapping, series definitions and
  conflicts are in [`docs/phases/phase-2-roads.md`](docs/phases/phase-2-roads.md). Next: R6
  simplified geometry, more exact-dated openings, and a refresh of the Trans
  Sulawesi and Trans Kalimantan series.
- **Estates:** 204 rows in `data/curated/estates.csv`; the 2024 audit ledger is
  `data/derived/estate_gap_2026.csv` and the coordinate work is documented in
  [`docs/phases/phase-2-estates.md`](docs/phases/phase-2-estates.md). Next: source
  the seven named 2024 additions, upgrade the 18 register-only PSN areas with
  area/developer/status, geocode the remaining 20 large estates, and verify
  attributes. Keep the map layer off until then.
- **Before changing schema:** read the Data architecture section in
  `docs/plan/plan.md`, `docs/phases/phase-1-decisions.md` and the schema section
  in `docs/plan/plan-v3.md`.
- **Before adding a status:** the allowed set is in `scripts/data_model.py` and
  enforced by `scripts/pipeline/validate.py`.
- **When in doubt:** record the conflict in `notes` and in
  `data/curated/conflicts.csv`, and cite both sources. Do not pick a winner
  silently.

## Publishing

The site is **not published**. Do not create a GitHub remote, push the
repository, deploy GitHub Pages or publish the site until the repository owner
asks for it explicitly. Phase 3 ends with a local release that works from
`file://` and a local HTTP server. The last commit and the screenshots in
`docs/evidence/phase-3/` are the release evidence.

## Requirements

- Python 3.10 or newer.
- `pip install -r requirements.txt` for the extraction and basemap scripts
  (BeautifulSoup, lxml, Shapely).
- No Node.js or build tooling is required to view the site.
- Optional: `pip install playwright` and an installed Microsoft Edge for
  `scripts/dev/smoke_site.py`. Playwright is not in `requirements.txt` and is not
  needed by the build or the released site.

## Licensing and credits

- **Code:** no licence has been chosen yet. Treat it as all rights reserved until
  one is added.
- **Wikipedia text:** CC BY-SA 4.0. Reuse requires attribution and share-alike.
  Facts still need a primary source.
- **Natural Earth:** public domain. Credited in the map attribution.
- **OpenStreetMap / Nominatim:** data © OpenStreetMap contributors, ODbL 1.0.
  Used for estate and factory coordinate checks; attribution is carried in the
  Data view and the source register.
- **Leaflet 1.9.4:** BSD-2-Clause. Licence file at
  `site/vendor/leaflet/LICENSE`.
- **Leaflet.markercluster 1.5.3:** MIT. Licence file at
  `site/vendor/markercluster/LICENSE`.
- **Inter:** SIL Open Font License 1.1. Licence at
  `site/assets/fonts/OFL-Inter.txt`.
- **Source Serif 4:** SIL Open Font License 1.1. Licence at
  `site/assets/fonts/OFL-Source-Serif.txt`.
- **Government data:** check each portal's terms before redistribution.

`docs/plan/plan.md` is the working document for the V4 scope, data model,
bilingual architecture and source evaluation. Read it before changing what
counts as in-scope.
