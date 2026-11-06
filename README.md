# Indonesia Infrastructure Map

A curated, source-linked map of major Indonesian infrastructure: toll roads now,
with airports, seaports and factories planned. Every project carries a source URL
and a verification date. The map is deliberately **major and curated, not
exhaustive**.

- **Live data:** 27 toll-road corridors — 20 under construction, 7 planned.
- **Last verification:** 6 November 2026.
- **Status:** working v1. Not yet deployed; airports, seaports and factories are
  not included yet.

## What it is, and what it is not

It is a single static page with a map of Sumatra, Java and Bali. Projects are
coloured by status, can be filtered by status and sector, and open a detail panel
with the evidence behind the status, the operator, the length, the source and the
dates.

It is **not** a live project tracker, an official government dataset, or a
complete list of Indonesian infrastructure. Rows are included only when they are
planned, under construction, recently completed or stalled, and only when a
source supports that status.

## Current coverage

| Sector | Rows | Under construction | Planned | Recently completed | Notes |
|---|---:|---:|---:|---:|---|
| Toll roads | 27 | 20 | 7 | 0 | Sumatra, Java and Bali corridors |
| Airports | 0 | — | — | — | phase 3 |
| Seaports | 0 | — | — | — | phase 3 |
| Factories | 0 | — | — | — | phase 3 |

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
├─ plan.md                  scope, decisions, sources, rules and phase status
├─ README.md
├─ requirements.txt         Python dependencies for the data scripts
├─ data/
│  ├─ projects.csv          curated table, one row per project (source of truth)
│  ├─ derived/              extracted text and other build-time intermediates
│  └─ raw/YYYY-MM-DD/       sources as fetched, never edited
├─ scripts/
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
   │  ├─ basemap.geojson    generated
   │  └─ basemap.js         generated, window.BASEMAP
   └─ vendor/leaflet/       Leaflet 1.9.4, vendored with its BSD licence
```

`data/projects.csv` is **generated** from the curated list in
`scripts/build_projects.py`. Edit the script, not the CSV, or the next rebuild
will overwrite your changes.

## How the data is built

```
Wikipedia snapshot ──► extract_wikipedia_toll_roads.py ──► parsed CSV
                                                              │
BPJT toll-road API ───────────────────────────────────────────┤
                                                              ▼
                                    build_projects.py ──► data/projects.csv
                                                              │
                                         validate.py ◄────────┤
                                                              ▼
                                    build_site_data.py ──► site/data/projects.*
Natural Earth ──► build_basemap.py ─────────────────────► site/data/basemap.*
```

Rebuild everything:

```bash
python scripts/build_projects.py
python scripts/validate.py
python scripts/build_site_data.py
python scripts/build_basemap.py
```

What each script does:

| Script | Input | Output | Purpose |
|---|---|---|---|
| `extract_wikipedia_toll_roads.py` | English Wikipedia HTML snapshot | `enwiki_toll_roads_parsed.csv` | Parses the toll-road table; no status decisions |
| `build_projects.py` | Curated `PROJECTS` list + BPJT JSON | `data/projects.csv` | Applies inclusion decisions and merges official BPJT fields |
| `validate.py` | `data/projects.csv` | exit code | Required fields, enums, dates, coordinates, duplicates |
| `build_site_data.py` | `data/projects.csv` | GeoJSON, JS and CSV copies | Site-ready data |
| `build_basemap.py` | Natural Earth GeoJSON | `site/data/basemap.*` | Clipped, simplified offline basemap |

`build_projects.py` expects the BPJT snapshot in
`data/raw/2026-11-06/bpjt_toll_road_list.json`. If it is missing, re-fetch it
from the API listed below before rebuilding.

## Data model

One row per project in `data/projects.csv`:

| Column | Required | Allowed values / meaning |
|---|---|---|
| `id` | yes | Lowercase, hyphenated, unique. Used in deep links |
| `name` | yes | Project name, English with Indonesian proper names |
| `sector` | yes | `road`, `airport`, `seaport`, `factory` |
| `status` | yes | `planned`, `under_construction`, `recently_completed`, `stalled` |
| `status_basis` | yes | The evidence for the status, with figures where possible |
| `province` | yes | Province or provinces, semicolon-separated |
| `route` | yes | Route, corridor or location description |
| `length_km` | yes | Positive number; corridor length, not completed length |
| `operator` | yes | Concession holder, agency or `tba` |
| `opened_year` | no | Year of opening, when known (blank in batch 1) |
| `lat`, `lon` | yes | Decimal degrees, inside 95–141°E and 11°S–6°N |
| `precision` | yes | `exact`, `approximate`, `regency`, `province` |
| `source_url` | yes | Direct URL to the source used |
| `source_type` | yes | `official` or `secondary` |
| `retrieved_on` | yes | Date the source was fetched (`YYYY-MM-DD`) |
| `last_verified` | yes | Date the row was last checked (`YYYY-MM-DD`) |
| `notes` | yes | Conflicts, caveats, section openings, coordinate overrides |

Status definitions:

| Status | Meaning |
|---|---|
| `planned` | Designated (PSN or KPBU) or tender announced; no groundbreaking |
| `under_construction` | Contract signed or groundbreaking held; latest evidence under 12 months old |
| `recently_completed` | Opened on or after 2024-11-06 |
| `stalled` | Officially delayed or reported stalled (*mangkrak*) |

## Sources

Batch 1 uses three sources. Each has a dated snapshot in `data/raw/2026-11-06/`.

| Source | URL | Used for | Caveats |
|---|---|---|---|
| English Wikipedia, "Indonesian Toll Road System", revision 1329385293 (2025-12-25) | <https://en.wikipedia.org/w/index.php?oldid=1329385293> | Route names, lengths, operators, status markers | Secondary and stale in places; no coordinates or opening years |
| BPJT toll-road API | <https://itrams-api.bpjt.pu.go.id/v1/reference/api/toll-road-list> | Official status, operating/construction km, operator, endpoint coordinates | 77 operating or partly operating rows; construction-only rows absent; status labels inconsistent |
| Indonesian Wikipedia, "Daftar jalan tol di Indonesia", oldid 30025554 (2026-10-03) | <https://id.wikipedia.org/w/index.php?oldid=30025554> | Cross-check of lengths, operating km and concessions | Secondary; figures often differ from BPJT |
| Natural Earth 1:50m countries and populated places | <https://www.naturalearthdata.com/> | Land outlines and city labels | Public domain; clipped and simplified |

Raw snapshots are never edited. Current contents:

```
data/raw/2026-11-06/
├─ wikipedia_indonesian_toll_road_system.wikitext / .html / .meta.json
├─ idwiki_daftar_jalan_tol_di_indonesia.wikitext / .html
├─ enwiki_toll_roads_parsed.csv
├─ bpjt_toll_road_list.json
├─ bpjt_toll_road_information.json
├─ bpjt_daftar_ruas_konstruksi.html
├─ ne_50m_admin_0_countries.geojson
├─ ne_50m_populated_places.geojson
├─ kppip_bandar_udara.html
├─ kppip_pelabuhan.html
├─ kppip_kawasan.html
├─ kemenhub_psn_progress_2026.pdf
└─ (extracted text in data/derived/)
```

The KPPIP pages and the Kemenhub PSN progress deck are saved for phase 2 and
are **not yet reflected** in `projects.csv`.

## Adding or updating a project

1. Save the source snapshot to `data/raw/<YYYY-MM-DD>/` (raw, unedited).
2. Add or edit the project's dictionary in the `PROJECTS` list in
   `scripts/build_projects.py`.
3. Set `status_basis` to the actual evidence, not just the status word. Include
   figures (km operational, completion date, decree number) where possible.
4. Put disagreements and caveats in `notes`. Do not resolve conflicts silently.
5. Run:

   ```bash
   python scripts/build_projects.py
   python scripts/validate.py
   python scripts/build_site_data.py
   ```

6. Reload the page and check the marker, the detail panel and the filters.
7. Commit the script change, the rebuilt CSV and the site data together.

Rules that apply to every row:

- A status change needs an official source, or two independent sources.
- Coordinates must be plausible; prefer official endpoints over city centres.
- A row not re-checked within six months should be treated as unverified.
- Do not include test, placeholder or duplicate entries.
- Keep the status vocabulary to the four values above.

## The site

`site/index.html` is a single page with inline CSS and JavaScript. Features:

- Colour-coded markers by status, with a status and sector filter.
- A scrollable project list, sorted by status then name.
- A detail panel showing route, length, operator, status basis, notes, source,
  retrieval and verification dates, and coordinate precision.
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

- every required field is present;
- `sector`, `status`, `precision` and `source_type` are in the allowed sets;
- `source_url` looks like a URL;
- `retrieved_on` and `last_verified` are real `YYYY-MM-DD` dates;
- ids are unique, lowercase and hyphenated;
- `length_km` is a positive number;
- coordinates fall inside Indonesia's rough bounding box;
- no row contains placeholder text such as `TEST` or `PENTEST`.

Validating is not the same as verifying. Validation catches malformed rows; the
`status_basis`, `notes` and source fields are what make a row trustworthy.

## Known limitations

- **Corridor-level, not section-level.** A corridor with one open section and one
  section under construction is `under_construction`; the open section is in
  `notes`.
- **Approximate coordinates.** Batch 1 uses the midpoint of each BPJT endpoint
  pair, so every row is `precision=approximate`. Bogor Ring Road uses Bogor city
  centre because the BPJT endpoints are misplaced.
- **Mixed source quality.** 17 rows are BPJT-backed (`official`); 10 rely on
  Wikipedia or a single secondary source.
- **BPJT labels are inconsistent.** Some rows marked `Operasi` still have
  unopened length or active construction. Conflicts are recorded, not hidden.
- **No geometry.** Projects are points, not lines or polygons.
- **No recently completed toll roads.** See Current coverage.
- **Incomplete universe.** Construction-only and pre-construction BPJT rows are
  not returned by the API; 0-km concessions are not yet included.
- **Excluded for now:** the three planned strait bridges (Bali, Malacca, Sunda)
  and non-toll PSN roads and bridges.
- **Wikipedia is secondary.** It is useful for discovery and cross-checking, not
  as the final authority on a status change.

## Roadmap

1. ~~Plan, decisions, toll-road batch, map page.~~ Done.
2. **Official pipeline.** PSN list (Permenko 4/2026), KPBU portal and INAPROC
   tenders. Snapshot pages are already saved under `data/raw/2026-11-06/`.
3. **Airports, seaports, factories.** KPPIP PSN lists, Satu Peta layers,
   Kemenperin estates, GEM steel plants. Apply the PSN/KPBU or Rp 1T threshold.
4. **Better geometry.** Replace midpoints with lines or exact points; set
   precision per row.
5. **Publish.** GitHub Pages workflow for `site/`.
6. **Monthly refresh.** Re-fetch sources, review status changes, update
   `last_verified`.

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

`plan.md` is the working document for scope, decisions and source evaluation.
Read it before changing what counts as in-scope.
