# Indonesia Infrastructure Map

A curated, source-linked map of major Indonesian infrastructure. Every project
carries a source and a verification date. The map is deliberately **major and
curated, not exhaustive**.

- **Live data:** 107 projects — 45 toll-road corridors, 13 railways, 7 airports,
  15 seaports and 27 factories — plus 5 Trans corridor summaries, 44 dated
  corridor segments and 6 project events.
- **Transport PSN:** 35 of 35 represented. Status is as of 19 February 2026, the
  date of the Kemenhub review.
- **Factories:** 27 plants and smelters: 19 operating, 3 recently completed,
  4 under construction and 1 stalled. All have capacity, 18 have investment.
- **Estate dataset:** 178 industrial estates and SEZs, shown as a table; the map
  layer is deliberately off until coordinates are verified.
- **Trust layer:** 479 atomic project claims and 20 estate claims; 107 of 107
  projects have a claim for the status and every populated numeric fact. 19
  conflicts are recorded with both values and both sources (11 resolved, 8 open).
  A 285-row freshness report marks each project and estate fresh, due soon or
  stale. A 189-field data dictionary covers all 18 curated tables.
- **Last verification:** 8 November 2026 (road, estate and factory batches); the
  transport batch was verified on 7 November 2026; earlier rows on 6 November.
  The 285-row freshness report is fresh as of 8 November 2026; the first record
  falls due on 8 May 2027.
- **Status:** Phase 1, Phase 2 and Phase 3 of the v3 overhaul are complete as of
  8 November 2026. Track 2B (estates) is partial and corridor geometry (R6) is
  deferred, but both are documented gaps. The 45-corridor road target is met.
  Phase 3 ends with a **local release only**: the site is verified from `file://`
  and a local HTTP server. There is **no GitHub remote, push, Pages deployment or
  published URL**.
- **V4 plan:** [`docs/plan/plan.md`](docs/plan/plan.md) is the current plan: a
  bilingual national delivery atlas with 400+ projects, 8 PKPN programmes,
  300 companies, 200 estates and a rebuilt map and Data view. It is a plan, not
  a released build. The completed v3 backlog stays in
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
| Toll roads | 45 | 10 operating, 25 under construction, 10 planned | 42 toll-road corridors plus 3 planned Trans Sumatra 0-km concessions |
| Railways | 13 | 6 operating, 5 under construction, 2 planned | 13/13 PSN railways; no rail length or capacity in the source deck |
| Airports | 7 | 7 operating | 7/7 PSN airports; inaugurated 2020–2023 |
| Seaports | 15 | 11 operating, 1 under construction, 1 recently completed, 2 planned | 15/15 PSN seaports; Patimban Phase I-2 still building, Benoa expansion completed 2025 |
| Transport PSN total | 35 | 24 operating, 1 recently completed, 6 under construction, 4 planned | 35/35; status as of 19 February 2026 |
| All projects | 107 | 53 operating, 4 recently completed, 35 under construction, 14 planned, 1 stalled | 45 roads, 13 railways, 7 airports, 15 seaports and 27 factories |
| Trans corridor summaries | 5 | 5 with km totals; 3 with progress series | Sumatra, Java and Papua have a series; Sulawesi and Kalimantan publish route totals only |
| Corridor segments | 44 | 13 Sumatra, 23 Java, 8 Papua | Section tables only where a published list exists; Sulawesi and Kalimantan are route-total-only |
| Dated events | 6 | 2018–2026 | Exact dates only; month-end approximations are not used |
| Factories | 27 | 19 operating, 3 recently completed, 4 under construction, 1 stalled | 27 capacity figures, 18 investment figures; 17 official, 8 dual, 2 single-source |
| Industrial estates / SEZs | 178 | 160 industrial-estate designations (153 industrial-only + 7 shared), 25 SEZs | table view only; 25 official SEZ points, 20 OSM points, 133 regency centroids; 19-name gap ledger |
| Sources | 89 | 35 official, 31 secondary, 23 company | 43 factory-batch sources, 25 individual SEZ profiles, the national register, OSM/Nominatim and the corridor series; target range 80–100, lower bound met |
| Project claims | 479 | 107/107 projects fully claimed | one atomic fact per row; 20 separate estate claims; 264 carry a transcribed value and 199 a source-stated fact date |
| Conflicts | 19 | 11 resolved, 8 open | both values and both sources, with a recorded resolution; downloadable register |
| Freshness | 285 | 285 fresh as of 2026-11-08 | 107 projects + 178 estates; 183-day threshold; next due 2027-05-08 |
| Data dictionary | 189 | 18 tables | generated from the schema; field type, required flag, description, allowed values and example |

**Why the transport status counts differ from Kemenhub's summary.** The deck's
headline says 29 complete and 6 under construction. The atlas uses its own
definitions and the deck's project pages: Patimban, the Java south double track,
Rantau Prapat–Kota Pinang and Lahat–Kertapati still have active work, while the
East Kalimantan railway, MRT East–West, New Palembang Port and Muaro Jambi had no
physical construction. The result is 24 operating, 1 recently completed, 6 under
construction and 4 planned. The full mapping and conflicts are in
[`docs/phases/phase-2-transport.md`](docs/phases/phase-2-transport.md).

**Factory universe.** The 27 plants are PSN manufacturing projects plus private
plants with investment of at least Rp 1 trillion. The list covers copper, nickel,
steel, alumina, aluminium, battery, petrochemical, pulp and fertiliser plants.
Industrial estates and pure mining pits are excluded; KIPI Bulungan remains an
estate gap, while GEM steel and Hailiang announcements did not meet the dated
status-and-capacity rule. See
[`docs/phases/phase-2-factories.md`](docs/phases/phase-2-factories.md) for the full inclusion
log, conflicts and coordinate provenance.

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
│  ├─ curated/               editable source of truth (18 tables)
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
`pipeline/build_projects.py` → `pipeline/build_dictionary.py` →
`pipeline/freshness.py` → `pipeline/audit_claims.py` →
`pipeline/build_site_data.py` → `pipeline/build_factories_ledger.py` →
`pipeline/check_site.py`.

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
python scripts/tools/geocode_factories.py         # optional; coordinate cache
python scripts/imports/build_basemap.py           # only when Natural Earth changes
```

What each script does:

| Script | Input | Output | Purpose |
|---|---|---|---|
| `tools/migrate_schema_v3.py` | Old curated tables | Schema-v3 headers and backfilled fields | One-off migration; idempotent enough to re-run |
| `imports/extract_wikipedia_toll_roads.py` | English Wikipedia HTML snapshot | `enwiki_toll_roads_parsed.csv` | Parses the toll-road table; no status decisions |
| `imports/extract_transport_psn.py` | Kemenhub PSN deck, checked transcription | `data/derived/transport_psn.csv` | 35 transport rows with page references and conflict notes |
| `imports/extract_estate_gap.py` | Kemenperin 179 count + 2024 table | `data/derived/estate_gap_2026.csv` | 19-row reconciliation; names only where a source supports them |
| `tools/geocode_estates.py` | Top 40 industrial estates + Nominatim | `data/derived/nominatim_estates.json`, updated estate coordinates | One request per second; accepts only industrial-landuse matches |
| `imports/build_transport.py` | `transport_psn.csv` + curated tables | Project, claim, link and alias rows | Idempotent transport import; does not touch roads or estates |
| `imports/add_bpjt_psn_roads.py` | BPJT snapshot + curated tables | 15 new PSN road rows, operators, claims and external IDs | Idempotent; leaves the 27 batch-1 roads in place |
| `imports/add_factories.py` | Factory research + curated tables | 27 plant rows, 43 sources, 26 organisations and 18 investment rows | Idempotent; replaces each factory’s claims on rerun |
| `tools/geocode_factories.py` | Nominatim + factory queries | `data/derived/nominatim_factories.json` | Provenance cache only; does not change curated coordinates |
| `pipeline/build_factories_ledger.py` | Curated project, organisation, link and claim tables | `data/derived/factories_2026.csv` | Frozen review ledger for the 27 plants |
| `pipeline/validate.py` | `data/curated/*.csv` | exit code | Schema, enums, dates, coordinates, foreign keys, events, geometry, atomic claims, conflicts and coverage checks |
| `tools/normalize_claims.py` | Project and estate claim tables | Split claim rows | One atomic fact per row; backfills missing investment, operational, opening and location claims |
| `pipeline/build_projects.py` | Curated tables + BPJT JSON | `data/exports/projects.csv` | Joins operator and source, fills gaps from BPJT, writes the flat export |
| `imports/build_estates.py` | KEK HTML + BAJRA table + regency cache | `data/curated/estates.csv` + source rows | Merges the 25 SEZs and 153 industrial estates, handles overlaps |
| `pipeline/freshness.py` | Curated projects and estates | `data/derived/freshness_report.csv` | Fresh / due soon / stale by `last_verified`; deterministic as-of date |
| `pipeline/audit_claims.py` | Curated projects and claims | `data/derived/claims_audit.csv` | Checks that status and every populated numeric fact has an atomic claim |
| `pipeline/build_dictionary.py` | Schema field lists | `data/derived/data_dictionary.csv`, `site/downloads/dictionary.csv` | 189 field definitions across 18 tables |
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
| `coverage_targets.csv` | coverage layer | `layer`, `label`, `unit`, `target_count`, `universe`, `source_id` |
| `conflicts.csv` | source disagreement | `id`, `scope`, `subject`, `field`, `value_a`, `source_a`, `value_b`, `source_b`, `status`, `resolution` |

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
| BAJRA, "Daftar Kawasan Industri Indonesia" (17 Aug 2024) | <https://www.bajra.id/2024/08/daftar-kawasan-industri-indonesia.html> | Industrial estate name, developer, regency, province, area | Secondary mirror of Kemenperin data; 159 estates, not the 179 reported in 2026 |
| ANTARA, Kemenperin estate count (2026) | <https://www.antaranews.com/berita/5627392/kemenperin-catat-kawasan-industri-serap-235-juta-pekerja> | Coverage benchmark: 179 estates, 101,351.45 ha, 57.20% occupancy | Secondary; used only as a benchmark, not as a row source |
| Natural Earth 1:50m countries, provinces, lakes, rivers, urban areas and populated places | <https://www.naturalearthdata.com/> | Basemap layers and city labels | Public domain; clipped and simplified |

Raw snapshots are never edited. Current contents include the Wikipedia
snapshots, the BPJT JSON, the Kemenhub PDF, the KPPIP HTML pages, the 25 KEK
profile pages, the BAJRA estate table and the Natural Earth GeoJSON under
`data/raw/2026-11-06/`.

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

## Industrial estates and SEZs

`data/curated/estates.csv` holds 178 records, gathered but deliberately **not
visualised yet**:

- **25 SEZs** from the official KEK National Council profiles. Each has a name,
  address, province/regency, official zone coordinate, area in hectares,
  developer, legal basis, establishment year and category.
- **153 industrial estates** from the 2024 Kemenperin-derived list. Each has a
  developer, regency/province and area. Coordinates are regency/city centroids,
  so `precision=regency`. The centroids are cached in
  `data/derived/regency_coords.json`; the cache lets the build run without
  network access.
- **7 zones are both** a SEZ and an industrial estate; they are one row with
  `type=both`, not duplicates.

The industrial-estate source is a secondary mirror of Kemenperin data. Kemenperin
reported 179 estates in 2026; the 160-row source table is a 2024 snapshot, so the
list is close but not complete. The `notes` field says this on every row. SEZ
rows use `status=operating` as a designation-level default; operational maturity
is not independently verified.

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

**Known gap.** Kemenperin announced nine new estates in 2025. They are not in the
table yet because each needs its own source for area, developer and coordinates:
IPIP (Kemenperin lists it under Central Sulawesi; the Pomalaa project is in
Southeast Sulawesi), I-Sentra Lamongan, Huadi Bantaeng, Cikembar II, Losarang,
Purwakarta Integrated Industrial Park, Pulau Penebang, Seafer and Tembesi. Add
them with individual sources rather than copying the press release.

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
- **Factories:** 27 plants and smelters on the map with a factory glyph, capacity
  and investment figures, operators, status basis and every source claim.
- **Detail drawer:** key figures, operational share, why-this-status, evidence,
  every source with claim and retrieval date, a freshness badge with the next
  due date, notes, related corridor, a project timeline where a dated event
  exists, previous/next and share.
- **Corridors:** five Trans corridors with km bars, a four-part legend, segment
  tables, grouped timelines, as-of dates, sources and explicit coverage states:
  complete series, partial segment table, route total only and no series.
- **Estates:** 178-row table with type/province filters, sort, inline detail,
  area totals, coordinate provenance, a filtered CSV button and CSV downloads
  (including the 19-row gap ledger). No map layer yet.
- **Data:** generated coverage matrix; claims coverage; freshness; status
  definitions; inclusion rules; conflict register with both values and sources;
  source register; 13 static downloads plus filtered project CSV/GeoJSON and
  estate CSV; the 189-field data dictionary; known gaps; and the changelog parsed
  from `CHANGELOG.md`.
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
python scripts/build_all.py --check       # 25 generated files must be byte-identical
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
  city centre because the BPJT endpoints are misplaced. All 35 transport points
  are airport, port or city reference points, and all 27 factory points are
  plant or industrial-park locators, not surveyed boundaries.
- **Mixed source quality.** 32 road rows are BPJT-backed (`official`); 13 rely on
  Wikipedia or a single secondary source. All 35 transport rows are backed by the
  Kemenhub deck, but that deck does not give rail lengths or asset capacity. The
  factory batch draws on 43 source rows: 23 company, 18 secondary and 2 official;
  Dexin and Huadi are single-source.
- **Claim coverage is not claim correctness.** 107/107 projects have the required
  atomic claims, but 215 of 479 claims do not repeat the value and 280 do not
  state a fact date; they link to the source without duplicating the project row.
  Fifteen projects are single-source. The audit proves coverage, not that every
  source agrees.
- **Freshness is a date check, not a live re-verification.** All 285 rows are
  fresh as of 8 November 2026 because they were curated in the 6–8 November
  batches. The first record falls due on 8 May 2027; the monthly runbook is the
  real test.
- **BPJT labels are inconsistent.** Some rows marked `Operasi` still have
  unopened length or active construction. Conflicts are recorded, not hidden.
- **No geometry.** Projects are points, not lines or polygons. `project_geometry`
  exists but is empty.
- **Factory figures are nameplate or project-level.** Capacity is not verified
  output. Investment is total project capex where the source gives one; 9 of 27
  rows have no investment figure. USD values are converted at Rp 16,500/USD for
  ranking, not at a transaction-date rate.
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
- **Event coverage is thin.** Six exact-dated events are recorded. Month-end
  approximations were rejected, so most section openings remain in project notes
  rather than on a timeline.
- **Transport status is dated.** It reflects the Kemenhub review of 19 February
  2026, not a live check. `last_verified` is the curation date.
- **PSN status is incomplete for roads.** 13 of 45 road rows have `psn=unknown`.
- **Estate coordinates are mixed.** 25 SEZ/shared zones use official KEK points,
  20 large industrial estates use OSM/Nominatim industrial points, and 133 still
  use regency centroids, not estate boundaries. 20 of the 40 largest were
  geocoded; the rest had no reliable OSM match.
- **Estate coverage is partial.** The industrial-estate table is a 2024 secondary
  mirror with 160 rows; Kemenperin reported 179 estates in 2026. The 19-name gap
  ledger is downloadable: nine named 2025 additions and ten unidentified names.
  The Kemenperin list was unreachable on 8 November 2026 (HTTP 502 / DNS failure).
- **Estate status is still blanket `operating`.** The 160 industrial-estate rows
  come from the 2024 table and have not been individually re-verified. Their
  sector focus, website, legal basis and established year are mostly blank.
- **No recently completed toll roads.** The four `recently_completed` rows are
  Benoa Port and three factories; see Current coverage.
- **Trans Sulawesi and Trans Kalimantan have route totals but no progress
  series.** The atlas publishes 2,000 km and 3,901 km respectively and says so
  explicitly. No percentage is estimated: competing definitions include a 1,186 km
  travel route, a 1,920 km border-parallel road and a 2,100.8 km WPS figure for
  Kalimantan, and the 3,900 km figure for Sulawesi refers to the wider road
  network.
- **Incomplete universe.** Construction-only and pre-construction BPJT rows are
  not returned by the API. The 45-corridor target now includes three planned
  0-km Trans Sumatra concessions, but the wider 0-km universe is not enumerated.
- **Excluded for now:** the three planned strait bridges (Bali, Malacca, Sunda),
  non-toll PSN roads and bridges, and announced factories that lack a dated
  status-and-capacity source (for example GEM steel and Hailiang).
- **Wikipedia is secondary.** It is useful for discovery and cross-checking, not
  as the final authority on a status change.
- **Conflict coverage is not exhaustive.** The register has 19 rows and 8 open
  conflicts. Two estate *location* conflicts (IPIP and Tembesi) stay in the gap
  ledger because the second side has no citable source row. Free-text `notes`
  still carries context that is not in a structured field.
- **Performance at 300 markers is untested.** The 107-project dataset is clustered
  and loads quickly, but the 300-marker 60 fps target still needs a dedicated
  measurement run and a larger test set.
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
   7 airports, 15 seaports), the 27-plant factory universe and the road/corridor
   batch are complete. Roads meet the 45-corridor target; five corridors carry 44
   segments and six exact-dated events. Estates: the 19-name gap ledger is done
   and 20 of the 40 largest are geocoded; the nine 2025 additions remain blocked
   by the unavailable Kemenperin list. Corridor geometry (R6) is deferred.
5. ~~Phase 3: trust and local release.~~ Done 8 November 2026. 479 atomic
   claims, 107/107 projects fully claimed, a 19-row conflict register, a 285-row
   freshness report, a 189-field dictionary, Data view v2, filtered downloads,
   local CI, a browser smoke test and hand-off. **No GitHub push, remote, Pages
   deployment or public release.**
6. **Monthly refresh.** Follow [`docs/operations/refresh-runbook.md`](docs/operations/refresh-runbook.md):
   re-fetch sources, review status changes, update `last_verified`, rebuild and
   verify locally.
7. **Publishing (deferred).** Only if the repository owner explicitly asks. Until
   then, the local `site/` build is the release.

## Where to pick up

- **Current plan:** [`docs/plan/plan.md`](docs/plan/plan.md). V3 is complete as
  of 8 November 2026; V4 is planned but **not implemented**. Track 2B (estates)
  is partial and R6 geometry is deferred; both are documented. Publishing is
  explicitly deferred.
- **Next action:** run `python scripts/build_all.py --check`, read
  [`docs/operations/refresh-runbook.md`](docs/operations/refresh-runbook.md),
  then start the V4 immediate actions in `docs/plan/plan.md` (source snapshots,
  PSN reconciliation, bilingual shell). Do not push, add a remote or deploy.
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
- **Factories:** Track 2C complete for the frozen 27-plant universe. The ledger
  is `data/derived/factories_2026.csv`, the importer is
  `scripts/imports/add_factories.py`, and the inclusion log and conflicts are in
  [`docs/phases/phase-2-factories.md`](docs/phases/phase-2-factories.md). Next: plant geometry,
  milestone events and a dated status check for GEM steel, Hailiang and other
  announced plants.
- **Roads and corridors:** 45 of 45 target corridors. Track 2D added 15 PSN
  corridors and three planned Trans Sumatra concessions, defined five corridors,
  built 44 segments and recorded six events. The mapping, series definitions and
  conflicts are in [`docs/phases/phase-2-roads.md`](docs/phases/phase-2-roads.md). Next: R6
  simplified geometry, more exact-dated openings, and a refresh of the Trans
  Sulawesi and Trans Kalimantan series.
- **Estates:** 178 rows in `data/curated/estates.csv`; the 19-name gap ledger is
  `data/derived/estate_gap_2026.csv` and the coordinate work is documented in
  [`docs/phases/phase-2-estates.md`](docs/phases/phase-2-estates.md). Next: resolve the
  Kemenperin list or a dated 2025 provincial announcement, add the nine named
  estates, geocode the remaining 20 large estates, and verify status and
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
