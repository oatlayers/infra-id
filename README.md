# Indonesia Infrastructure Map

A curated, source-linked map of major Indonesian infrastructure. Every project
carries a source and a verification date. The map is deliberately **major and
curated, not exhaustive**.

- **Live data:** 27 toll-road corridors — 20 under construction, 7 planned —
  plus 4 Trans corridor summaries.
- **Last verification:** 6 November 2026.
- **Status:** v2 data foundation in place. Not deployed. Airports, seaports,
  railways, factories, industrial estates and SEZs are not on the map yet.

## What it is, and what it is not

It is a single static page with a map of Indonesia. Projects are coloured by
status, can be filtered by status and sector, and open a detail panel with the
evidence behind the status, the operator, the length, the source and the dates.
A second tab summarises progress on the Trans Sumatra, Trans Papua, Trans
Sulawesi and Trans Kalimantan corridors.

It is **not** a live project tracker, an official government dataset, or a
complete list of Indonesian infrastructure. Rows are included only when they are
planned, under construction, recently completed, operating or stalled, and only
when a source supports that status.

## Current coverage

| Layer | Rows | Status | Notes |
|---|---:|---|---|
| Toll roads | 27 | 20 under construction, 7 planned | Sumatra, Java and Bali corridors |
| Trans corridor summaries | 4 | 2 with km data, 2 data gaps | Sumatra and Papua have figures; Sulawesi and Kalimantan need segment definitions |
| Railways | 0 | — | next transport batch |
| Airports | 0 | — | next transport batch |
| Seaports | 0 | — | next transport batch |
| Factories | 0 | — | after the estate/SEZ batch |
| Industrial estates / SEZs | 0 | — | data gathering in progress |

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

Deep links use the project id, for example:

```
site/index.html#tol-solo-yogyakarta-nyia
```

## Repository layout

```
infra-id/
├─ plan.md                  scope, decisions, architecture, phase status
├─ README.md
├─ requirements.txt         Python dependencies for the data scripts
├─ data/
│  ├─ curated/              editable source of truth
│  │  ├─ projects.csv
│  │  ├─ organizations.csv
│  │  ├─ project_organizations.csv
│  │  ├─ sources.csv
│  │  ├─ project_sources.csv
│  │  ├─ project_external_ids.csv
│  │  ├─ investments.csv
│  │  ├─ laws.csv
│  │  ├─ project_laws.csv
│  │  ├─ corridors.csv
│  │  └─ corridor_segments.csv
│  ├─ projects.csv          generated flat export for the site and downloads
│  ├─ derived/              extracted text and build-time intermediates
│  └─ raw/YYYY-MM-DD/       sources as fetched, never edited
├─ scripts/
│  ├─ data_model.py         paths, field lists, enums and CSV helpers
│  ├─ extract_wikipedia_toll_roads.py
│  ├─ build_projects.py
│  ├─ validate.py
│  ├─ build_site_data.py
│  └─ build_basemap.py
└─ site/
   ├─ index.html            Leaflet page (HTML, CSS, JS in one file)
   ├─ data/
   │  ├─ projects.geojson   generated
   │  ├─ projects.js        generated, window.PROJECTS
   │  ├─ projects.csv       generated download copy
   │  ├─ corridors.js       generated, window.CORRIDORS
   │  ├─ corridors.json     generated
   │  ├─ basemap.geojson    generated
   │  └─ basemap.js         generated, window.BASEMAP
   └─ vendor/leaflet/       Leaflet 1.9.4, vendored with its BSD licence
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
python scripts/validate.py
python scripts/build_projects.py
python scripts/build_site_data.py
python scripts/build_basemap.py
```

What each script does:

| Script | Input | Output | Purpose |
|---|---|---|---|
| `extract_wikipedia_toll_roads.py` | English Wikipedia HTML snapshot | `enwiki_toll_roads_parsed.csv` | Parses the toll-road table; no status decisions |
| `validate.py` | `data/curated/*.csv` | exit code | Schema, enums, dates, coordinates, foreign keys and range checks |
| `build_projects.py` | Curated tables + BPJT JSON | `data/projects.csv` | Joins operator and source, fills gaps from BPJT, writes the flat export |
| `build_site_data.py` | `data/projects.csv` + `corridors.csv` | GeoJSON, JS, CSV and corridor payloads | Site-ready data |
| `build_basemap.py` | Natural Earth GeoJSON | `site/data/basemap.*` | Clipped, simplified offline basemap |

`build_projects.py` expects the BPJT snapshot in
`data/raw/2026-11-06/bpjt_toll_road_list.json`. If it is missing, re-fetch it
from the API listed below before rebuilding.

## Data model

The curated data is normalised. One fact per row; no semicolon-separated lists.
The full rationale and target schema are in `plan.md`.

| Table | One row per | Key fields |
|---|---|---|
| `projects.csv` | project | `id`, `name`, `sector`, `status`, `corridor_id`, km, investment, location |
| `organizations.csv` | company or agency | `id`, `name`, `org_type`, `country_code`, `parent_id`, `website` |
| `project_organizations.csv` | project–organisation role | `project_id`, `org_id`, `role`, `share_pct`, `source_id` |
| `investments.csv` | commitment or tranche | `project_id`, `investor_org_id`, `amount`, `currency`, `amount_idr_t`, `stage`, `instrument` |
| `sources.csv` | source document | `id`, `publisher`, `title`, `url`, `published_on`, `retrieved_on`, `source_type`, `archive_path` |
| `project_sources.csv` | project–source claim | `project_id`, `source_id`, `claim` |
| `project_external_ids.csv` | external key | `project_id`, `system`, `external_id` |
| `laws.csv` / `project_laws.csv` | regulation / relation | legal basis, kept separate from news |
| `corridors.csv` | Trans corridor | `total_km`, `operational_km`, `construction_km`, `planned_km`, `metric`, `as_of` |
| `corridor_segments.csv` | corridor segment | section-level km, status and opening year |

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
| Natural Earth 1:50m countries and populated places | <https://www.naturalearthdata.com/> | Land outlines and city labels | Public domain; clipped and simplified |

Raw snapshots are never edited. Current contents include the Wikipedia
snapshots, the BPJT JSON, the Kemenhub PDF, the KPPIP HTML pages and the Natural
Earth GeoJSON under `data/raw/2026-11-06/`.

The KPPIP pages and the Kemenhub PSN deck are saved for the transport batch and
are **not yet reflected** in `data/curated/projects.csv`.

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
7. Put disagreements and caveats in `notes`. Do not resolve conflicts silently.
8. Run:

   ```bash
   python scripts/validate.py
   python scripts/build_projects.py
   python scripts/build_site_data.py
   ```

9. Reload the page and check the marker, the detail panel, the filters and the
   corridor tab.
10. Update this README if the coverage, schema or behaviour changed.
11. Commit the curated rows, rebuilt exports and site data together.

Rules that apply to every row:

- A status change needs an official source, or two independent sources.
- Coordinates must be plausible; prefer official or site-specific points over
  city centres.
- A row not re-checked within six months should be treated as unverified.
- Do not include test, placeholder or duplicate entries.
- Use only the status values above.
- Keep `data/projects.csv` and `site/data/` generated; never hand-edit them.

## The site

`site/index.html` is a single page with inline CSS and JavaScript. Features:

- Colour-coded markers by status, with status and sector filters.
- A **Projects / Trans corridors** switch in the list panel.
- Trans corridor cards with km bars, as-of dates, sources and data-gap notes.
- A scrollable project list, sorted by status then name.
- A detail panel with route, km breakdown (operational vs under construction),
  investment or capacity, operator, status basis, notes, source, retrieval and
  verification dates, and coordinate precision.
- Deep links via `#project-id`; closing the panel clears the hash.
- Responsive layout: side panel on desktop, stacked map and filters on mobile,
  bottom sheet for details.
- A compact layout for short desktop windows.
- Offline-capable: no tile server, no CDN, no `fetch`.

The basemap is Natural Earth geometry clipped to 92–144°E, 14°S–9°N and
simplified to roughly 500 m. It shows land, borders and 13 major cities — not
roads, terrain or small settlements. This is a deliberate trade for reliability:
OpenStreetMap's tile servers block `file://` pages, which previously filled the
map with 403 images.

## Validation and quality rules

`python scripts/validate.py` checks:

- every curated table has the expected header;
- required fields are present and enums are valid;
- dates are real `YYYY-MM-DD` values and years are plausible;
- ids are unique, lowercase and hyphenated;
- every foreign key resolves (project, organisation, source, corridor, law);
- every project has at least one source claim;
- km figures are non-negative and do not exceed the total by more than 5%;
- coordinates fall inside Indonesia's rough bounding box;
- operating and recently completed rows have an `opened_year`;
- archive paths exist when they point into the repo;
- no duplicate project–organisation roles or external ids.

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
- **No geometry.** Projects are points, not lines or polygons.
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

## Roadmap

1. ~~Plan, decisions, toll-road batch, map page.~~ Done.
2. ~~Normalised data foundation, km fields, operating status, corridor tab.~~ Done.
3. **Industrial estates and SEZs.** Gather all Kawasan Industri and KEK records
   with location, area, developer, status, key sectors and sources. Data only;
   no new map layer yet. *In progress.*
4. **Transport PSN batch.** Railways, airports and seaports from the Kemenhub
   deck and KPPIP lists. Enable the sector filters with real data.
5. **Factories.** PSN smelters, GEM steel plants, large nickel/aluminium/copper
   and battery projects. Requires `organizations` and `investments` rows.
6. **Better geometry.** Replace midpoints with lines or exact points; set
   precision per row.
7. **Publish.** GitHub Pages workflow for `site/`.
8. **Monthly refresh.** Re-fetch sources, review status changes, update
   `last_verified`.

## Where to pick up

- **Current task:** gather industrial estate and SEZ data into a new curated
  table, then extend `validate.py` and `build_projects.py` for it. Do not add it
  to the map yet.
- **Next task:** the transport PSN batch (rail, ports, airports). Start from
  `data/derived/kemenhub_psn_progress_2026.txt` and the KPPIP HTML snapshots.
- **Before changing schema:** read the Data architecture section in `plan.md`.
- **Before adding a status:** the allowed set is in `scripts/data_model.py` and
  enforced by `validate.py`.
- **When in doubt:** record the conflict in `notes` and cite both sources.

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
- **Government data:** check each portal's terms before redistribution.

`plan.md` is the working document for scope, decisions, architecture and source
evaluation. Read it before changing what counts as in-scope.
