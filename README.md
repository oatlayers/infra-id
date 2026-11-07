# Indonesia Infrastructure Map

A curated, source-linked map of major Indonesian infrastructure. Every project
carries a source and a verification date. The map is deliberately **major and
curated, not exhaustive**.

- **Live data:** 27 toll-road corridors — 20 under construction, 7 planned —
  plus 4 Trans corridor summaries.
- **Estate dataset:** 178 industrial estates and SEZs, shown as a table; the map
  layer is deliberately off until coordinates are verified.
- **Last verification:** 6 November 2026.
- **Status:** Phase 1 of the v3 overhaul is complete (7 November 2026): new
  shell, four views, search, filters, detail drawer, map v2, mobile sheet and a
  generated data page. The site is **not published** and has no GitHub remote.
- **Overhaul plan:** [`plan-v3.md`](plan-v3.md) is the execution backlog. Phase 2
  is data completion; Phase 3 is the trust layer and a local release. Publishing
  is explicitly deferred. Phase 1 decisions are recorded in
  [`docs/phase-1-decisions.md`](docs/phase-1-decisions.md).

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
| Toll roads | 27 | 20 under construction, 7 planned | Sumatra, Java and Bali corridors |
| Trans corridor summaries | 4 | 2 with km data, 2 data gaps | Sumatra and Papua have figures; Sulawesi and Kalimantan need segment definitions |
| Railways | 0 | — | Phase 2: 13 PSN railways |
| Airports | 0 | — | Phase 2: 7 PSN airports |
| Seaports | 0 | — | Phase 2: 15 PSN seaports |
| Factories | 0 | — | Phase 2: 20–30 plants |
| Industrial estates / SEZs | 178 | 160 industrial-estate designations (153 industrial-only + 7 shared), 25 SEZs | table view only; map layer waits for verified coordinates |
| Sources | 38 | 32 official, 6 secondary | 25 individual SEZ profiles plus the national source register |

**Why zero recently completed?** No full toll corridor opened between
2024-11-06 and 2026-11-06. Sections did open in that window (for example
Binjai–Langsa Section 3 in March 2025, Padang–Sicincin in May 2025,
Solo–Yogyakarta Klaten–Prambanan in July 2025, Probolinggo–Banyuwangi Sections
1–2 in 2026), but their corridors remain under construction. Those openings are
recorded in each row's `notes`.

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
├─ plan.md                  scope, decisions, architecture, phase status
├─ plan-v3.md               three-phase execution backlog
├─ README.md
├─ docs/
│  └─ phase-1-decisions.md  confirmed design, scope, schema and budgets
├─ requirements.txt         Python dependencies for the data scripts
├─ data/
│  ├─ curated/              editable source of truth
│  │  ├─ projects.csv
│  │  ├─ organizations.csv
│  │  ├─ project_organizations.csv
│  │  ├─ sources.csv
│  │  ├─ project_sources.csv
│  │  ├─ project_external_ids.csv
│  │  ├─ project_aliases.csv
│  │  ├─ project_events.csv
│  │  ├─ project_geometry.csv
│  │  ├─ investments.csv
│  │  ├─ laws.csv
│  │  ├─ project_laws.csv
│  │  ├─ corridors.csv
│  │  ├─ corridor_segments.csv
│  │  ├─ estates.csv
│  │  ├─ estate_sources.csv
│  │  └─ coverage_targets.csv
│  ├─ projects.csv          generated flat export for the site and downloads
│  ├─ derived/              extracted text and build-time intermediates
│  └─ raw/YYYY-MM-DD/       sources as fetched, never edited
├─ scripts/
│  ├─ data_model.py         paths, field lists, enums and CSV helpers
│  ├─ migrate_schema_v3.py  one-off schema migration
│  ├─ extract_wikipedia_toll_roads.py
│  ├─ build_projects.py
│  ├─ build_estates.py
│  ├─ validate.py
│  ├─ build_site_data.py
│  └─ build_basemap.py
└─ site/
   ├─ index.html            shell, inline SVG sprite and mount points
   ├─ assets/
   │  ├─ fonts.css          local @font-face rules
   │  ├─ fonts/             bundled OFL WOFF2 files
   │  ├─ tokens.css         design tokens
   │  ├─ app.css            layout and components
   │  ├─ constants.js       shared status and sector vocabulary
   │  ├─ app.js             boot, routing, views and drawer
   │  └─ map.js             Leaflet basemap, markers and clusters
   ├─ data/                 generated payloads and downloads
   │  ├─ projects.js/.geojson/.csv
   │  ├─ estates.js/.json/.csv
   │  ├─ corridors.js/.json
   │  ├─ stats.js
   │  ├─ search.js
   │  ├─ sources.csv
   │  ├─ basemap.js/.geojson
   └─ vendor/
      ├─ leaflet/           Leaflet 1.9.4, BSD licence
      └─ markercluster/     Leaflet.markercluster 1.5.3, MIT licence
```

**Do not edit `data/projects.csv`.** It is generated from `data/curated/` by
`scripts/build_projects.py`. Edit the curated tables and rebuild.

## How the data is built

```
data/curated/*.csv ──► validate.py ──► build_projects.py ──► data/projects.csv
                                                               │
                                                               ▼
                                              build_site_data.py ──► site/data/*
BPJT snapshot ─────────────► build_projects.py (fills gaps, official endpoints)
Natural Earth ─────────────► build_basemap.py ─────────────► site/data/basemap.*
```

Rebuild everything:

```bash
python scripts/build_estates.py      # only when the estate sources change
python scripts/validate.py
python scripts/build_projects.py
python scripts/build_site_data.py
python scripts/build_basemap.py
```

What each script does:

| Script | Input | Output | Purpose |
|---|---|---|---|
| `migrate_schema_v3.py` | Old curated tables | Schema-v3 headers and backfilled fields | One-off migration; idempotent enough to re-run |
| `extract_wikipedia_toll_roads.py` | English Wikipedia HTML snapshot | `enwiki_toll_roads_parsed.csv` | Parses the toll-road table; no status decisions |
| `validate.py` | `data/curated/*.csv` | exit code | Schema, enums, dates, coordinates, foreign keys, events, geometry, claims and coverage checks |
| `build_projects.py` | Curated tables + BPJT JSON | `data/projects.csv` | Joins operator and source, fills gaps from BPJT, writes the flat export |
| `build_estates.py` | KEK HTML + BAJRA table + regency cache | `data/curated/estates.csv` + source rows | Merges the 25 SEZs and 153 industrial estates, handles overlaps |
| `build_site_data.py` | Flat projects + curated corridors, estates, sources and coverage targets | GeoJSON, JS, CSV, stats and search payloads | Site-ready data; the search index and coverage matrix are generated here |
| `build_basemap.py` | Natural Earth countries, provinces, lakes, rivers, urban areas and places | `site/data/basemap.*` | Clipped, simplified offline basemap |

`build_projects.py` expects the BPJT snapshot in
`data/raw/2026-11-06/bpjt_toll_road_list.json`. If it is missing, re-fetch it
from the API listed below before rebuilding.

## Data model

The curated data is normalised. One fact per row; no semicolon-separated lists.
The full rationale and target schema are in `plan.md`.

| Table | One row per | Key fields |
|---|---|---|
| `projects.csv` | project | `id`, `name`, `sector`, `status`, `corridor_id`, `island`, km, investment, location, `status_as_of`, `verification` |
| `organizations.csv` | company or agency | `id`, `name`, `org_type`, `country_code`, `parent_id`, `website` |
| `project_organizations.csv` | project–organisation role | `project_id`, `org_id`, `role`, `share_pct`, `source_id` |
| `investments.csv` | commitment or tranche | `project_id`, `investor_org_id`, `amount`, `currency`, `amount_idr_t`, `stage`, `instrument` |
| `sources.csv` | source document | `id`, `publisher`, `title`, `url`, `published_on`, `retrieved_on`, `source_type`, `language`, `archive_path` |
| `project_sources.csv` | project–source claim | `project_id`, `source_id`, `claim`, `claim_value`, `claim_date` |
| `project_external_ids.csv` | external key | `project_id`, `system`, `external_id` |
| `project_aliases.csv` | project alias | `project_id`, `alias`, `source_id` |
| `project_events.csv` | dated event | `project_id`, `event_date`, `event_type`, `description`, `source_id` |
| `project_geometry.csv` | geometry | `project_id`, `kind`, GeoJSON `geometry`, `precision`, `source_id` |
| `laws.csv` / `project_laws.csv` | regulation / relation | legal basis, kept separate from news |
| `corridors.csv` | Trans corridor | `total_km`, `operational_km`, `construction_km`, `planned_km`, `metric`, `as_of` |
| `corridor_segments.csv` | corridor segment | `segment_type`, section-level km, progress, status, opening year, geometry |
| `estates.csv` | industrial estate or SEZ | `id`, `name`, `type`, `province`, `regency`, `island`, `area_ha`, `developer`, `status`, `coordinate_source`, `source_id` |
| `estate_sources.csv` | estate–source claim | `estate_id`, `source_id`, `claim`, `claim_value`, `claim_date` |
| `coverage_targets.csv` | coverage layer | `layer`, `label`, `unit`, `target_count`, `universe`, `source_id` |

Project columns (`data/curated/projects.csv`):

| Column | Required | Allowed values / meaning |
|---|---|---|
| `id` | yes | Lowercase, hyphenated, unique. Used in deep links |
| `name` | yes | Project name, English with Indonesian proper names |
| `sector` | yes | `road`, `railway`, `airport`, `seaport`, `factory` |
| `subsector` | no | For example `toll`, `urban_rail`, `new_build`, `expansion` |
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
| Katadata (21 Jul 2025) | <https://katadata.co.id/berita/industri/687e4748a975f/tni-targetkan-proyek-trans-papua-rampung-di-era-prabowo> | Trans Papua km | Secondary; connected vs paved metrics differ |
| KEK National Council profiles (25 pages) | <https://kek.go.id/id/investment/distribution> | SEZ name, address, coordinates, area, developer, legal basis, category | Official; one page per zone. Operational maturity is not stated |
| BAJRA, "Daftar Kawasan Industri Indonesia" (17 Aug 2024) | <https://www.bajra.id/2024/08/daftar-kawasan-industri-indonesia.html> | Industrial estate name, developer, regency, province, area | Secondary mirror of Kemenperin data; 159 estates, not the 179 reported in 2026 |
| ANTARA, Kemenperin estate count (2026) | <https://www.antaranews.com/berita/5627392/kemenperin-catat-kawasan-industri-serap-235-juta-pekerja> | Coverage benchmark: 179 estates, 101,351.45 ha, 57.20% occupancy | Secondary; used only as a benchmark, not as a row source |
| Natural Earth 1:50m countries, provinces, lakes, rivers, urban areas and populated places | <https://www.naturalearthdata.com/> | Basemap layers and city labels | Public domain; clipped and simplified |

Raw snapshots are never edited. Current contents include the Wikipedia
snapshots, the BPJT JSON, the Kemenhub PDF, the KPPIP HTML pages, the 25 KEK
profile pages, the BAJRA estate table and the Natural Earth GeoJSON under
`data/raw/2026-11-06/`.

The KPPIP pages and the Kemenhub PSN deck are saved for the transport batch and
are **not yet reflected** in `data/curated/projects.csv`.

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
4. Link the source in `data/curated/project_sources.csv` and set `claim`
   (`status`, `length`, `operator`, `investment`, `opening`, `location`).
5. Add the operator/sponsor to `organizations.csv` and link it in
   `project_organizations.csv`. Do not put company names in `projects.csv`.
6. Set `status_basis` to the actual evidence, not just the status word. Include
   figures (km operational, completion date, decree number) where possible.
7. Set `island`, `status_as_of` and `verification` (`official`, `dual`, `single`
   or `unverified`).
8. Put disagreements and caveats in `notes`. Do not resolve conflicts silently.
9. Run:

   ```bash
   python scripts/validate.py
   python scripts/build_projects.py
   python scripts/build_site_data.py
   ```

10. Reload the page and check the marker, the drawer, the filters, the Estates
    table and the Data view.
11. Update this README if the coverage, schema or behaviour changed.
12. Commit the curated rows, rebuilt exports and site data together. Do not push.

Rules that apply to every row:

- A status change needs an official source, or two independent sources.
- Coordinates must be plausible; prefer official or site-specific points over
  city centres.
- A row not re-checked within six months should be treated as unverified.
- Do not include test, placeholder or duplicate entries.
- Use only the status values above.
- Keep `data/projects.csv` and `site/data/` generated; never hand-edit them.

## The site

`site/index.html` is the shell; CSS and JavaScript live under `site/assets/`.
Features:

- **Explore:** search across name, province, corridor and operator; sector,
  status, island, province, PSN, corridor, precision and freshness filters;
  five sort modes; URL state; map/list selection; keyboard navigation.
- **Map:** Natural Earth provinces, lakes, rivers, urban areas and city labels;
  sector glyphs inside status-coloured markers; status-ring clusters below zoom
  7; selected marker label; drawer-aware panning.
- **Detail drawer:** key figures, operational share, why-this-status, evidence,
  every source with claim and retrieval date, notes, related corridor,
  previous/next and share.
- **Corridors:** Trans Sumatra, Trans Papua, Trans Sulawesi and Trans Kalimantan
  with km bars, as-of dates, sources and explicit data-gap states.
- **Estates:** 178-row table with type/province filters, sort, inline detail,
  area totals and a CSV download. No map layer yet.
- **Data:** generated coverage matrix, status definitions, inclusion rules,
  source register, downloads, known gaps and changelog.
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

`python scripts/validate.py` checks:

- every curated table has the expected header;
- required fields are present and enums are valid;
- dates are real `YYYY-MM-DD` values and years are plausible;
- ids are unique, lowercase and hyphenated;
- every foreign key resolves (project, organisation, source, corridor, law,
  estate, event, geometry);
- every project has at least one source claim;
- km figures are non-negative and do not exceed the total by more than 5%;
- coordinates fall inside Indonesia's rough bounding box;
- operating and recently completed rows have an `opened_year`;
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
`status_basis`, `notes` and source rows are what make a project trustworthy.

## Known limitations

- **Corridor-level, not section-level.** A corridor with one open section and one
  section under construction is `under_construction`; the open section is in
  `notes`.
- **Approximate coordinates.** Batch 1 uses the midpoint of each BPJT endpoint
  pair, so every road row is `precision=approximate`. Bogor Ring Road uses Bogor
  city centre because the BPJT endpoints are misplaced.
- **Mixed source quality.** 17 road rows are BPJT-backed (`official`); 10 rely on
  Wikipedia or a single secondary source.
- **BPJT labels are inconsistent.** Some rows marked `Operasi` still have
  unopened length or active construction. Conflicts are recorded, not hidden.
- **No geometry.** Projects are points, not lines or polygons. `project_geometry`
  exists but is empty.
- **Transport and factories are still empty.** The 35 transport PSN projects,
  20–30 factories and the expanded road/corridor batch are Phase 2.
- **PSN status is incomplete.** 10 of 27 road rows have `psn=unknown`.
- **Estate coordinates are coarse.** SEZ points are official zone coordinates but
  still approximate for an area; industrial-estate points are regency centroids,
  not estate boundaries.
- **Estate coverage is partial.** The industrial-estate table is a 2024 secondary
  mirror with 160 rows; Kemenperin reported 179 estates in 2026. New 2025 estates
  and exact boundaries still need to be added.
- **No recently completed toll roads.** See Current coverage.
- **Trans Sulawesi and Trans Kalimantan have no aggregate.** Published figures
  use different definitions; the site shows a data-gap note instead of inventing
  a total.
- **Incomplete universe.** Construction-only and pre-construction BPJT rows are
  not returned by the API; 0-km concessions are not yet included.
- **Excluded for now:** the three planned strait bridges (Bali, Malacca, Sunda)
  and non-toll PSN roads and bridges.
- **Wikipedia is secondary.** It is useful for discovery and cross-checking, not
  as the final authority on a status change.
- **Performance at 300 markers is untested.** The current 27-row dataset is
  clustered, but the 300-marker 60 fps target needs the Phase 2 dataset.
- **Formal accessibility audit pending.** Keyboard, focus, skip link, reduced
  motion and text status labels are in place; Lighthouse/axe results are not yet
  recorded.
- **Not published.** There is no GitHub remote or Pages deployment. The site is
  verified from `file://` only.

## Roadmap

1. ~~Plan, decisions, toll-road batch, map page.~~ Done.
2. ~~Normalised data foundation, km fields, operating status, corridor tab.~~ Done.
3. ~~Phase 1: design foundation, four-view shell, search, filters, drawer, map v2,
   mobile sheet, data page, schema v3.~~ Done 7 November 2026.
4. **Phase 2: data completion.** Transport PSN (13 rail, 7 airports, 15
   seaports), estate reconciliation and exact coordinates, factories, roads and
   corridor segments. *Next.*
5. **Phase 3: trust and local release.** Per-fact claims, freshness, Data view
   v2, downloads, conflicts, local CI, smoke tests and hand-off. **No GitHub push
   or Pages deployment.**
6. **Monthly refresh.** Re-fetch sources, review status changes, update
   `last_verified`, rebuild and verify locally.

## Where to pick up

- **Current plan:** [`plan-v3.md`](plan-v3.md). Phase 1 is complete. Phase 2 is
  data completion; Phase 3 is the trust layer and a local release. Publishing is
  explicitly deferred.
- **Phase 1 decisions:** [`docs/phase-1-decisions.md`](docs/phase-1-decisions.md).
- **Transport PSN batch:** the extracted 35-row baseline is in
  `data/derived/kemenhub_psn_progress_2026.txt` and the full table is in
  `plan-v3.md` section 5.2. This is the next data win.
- **Estates:** 178 rows in `data/curated/estates.csv`. Add the 2025 estates,
  replace regency centroids with estate boundaries or site coordinates, and
  verify SEZ operational status. Keep the map layer off until then.
- **Before changing schema:** read the Data architecture section in `plan.md`,
  `docs/phase-1-decisions.md` and the schema section in `plan-v3.md`.
- **Before adding a status:** the allowed set is in `scripts/data_model.py` and
  enforced by `validate.py`.
- **When in doubt:** record the conflict in `notes` and cite both sources.

## Publishing

The site is **not published**. Do not create a GitHub remote, push the
repository, deploy GitHub Pages or publish the site until the repository owner
asks for it explicitly. The current release target is a local build that works
from `file://` and a local HTTP server.

## Requirements

- Python 3.10 or newer.
- `pip install -r requirements.txt` for the extraction and basemap scripts
  (BeautifulSoup, lxml, Shapely).
- No Node.js or build tooling is required to view the site.

## Licensing and credits

- **Code:** no licence has been chosen yet. Treat it as all rights reserved until
  one is added.
- **Wikipedia text:** CC BY-SA 4.0. Reuse requires attribution and share-alike.
  Facts still need a primary source.
- **Natural Earth:** public domain. Credited in the map attribution.
- **Leaflet 1.9.4:** BSD-2-Clause. Licence file at
  `site/vendor/leaflet/LICENSE`.
- **Leaflet.markercluster 1.5.3:** MIT. Licence file at
  `site/vendor/markercluster/LICENSE`.
- **Inter:** SIL Open Font License 1.1. Licence at
  `site/assets/fonts/OFL-Inter.txt`.
- **Source Serif 4:** SIL Open Font License 1.1. Licence at
  `site/assets/fonts/OFL-Source-Serif.txt`.
- **Government data:** check each portal's terms before redistribution.

`plan.md` is the working document for scope, decisions, architecture and source
evaluation. Read it before changing what counts as in-scope.
