# Indonesia Infrastructure Map

A simple map of major infrastructure in Indonesia: roads, airports, seaports and factories that are under construction, planned, or recently completed.

**Status:** building. Started 2026-11-06. Decisions agreed 2026-11-06. First toll-road batch is in `data/projects.csv` (27 rows, validation passing). The Leaflet page is built and working at `site/index.html`. Not deployed yet.

## Goal

- One page with a map of Indonesia. Projects are coloured by status and can be filtered by sector.
- Clicking a project shows its details, its sources, and when it was last verified.
- The site says it is "major, curated, not exhaustive".

## Scope

**Sectors**

- **Roads:** toll roads that are under construction, planned, or recently opened. PSN national roads and bridges come later.
- **Airports and seaports:** new builds and major expansions that are designated (PSN or KPBU), or have an investment of at least Rp 1T (about US$55–60M).
- **Factories:** industrial estates as a background layer. Single plants with an investment of at least Rp 1T. Steel plants from GEM's tracker.

**Statuses**

| Status | Meaning |
|---|---|
| `planned` | Designated (PSN or KPBU) or tender announced. No groundbreaking yet. |
| `under_construction` | Contract signed or groundbreaking held (*peletakan batu pertama*). Latest evidence is under 12 months old. |
| `recently_completed` | Opened in the last 2 years, on or after 2024-11-06. |
| `stalled` | Officially delayed or reported stalled (*mangkrak*). |

## Decisions

**Made** (all agreed 2026-11-06)

- Folder: `D:\Workspace\infra-id`.
- First batch: toll roads from the English Wikipedia article "Indonesian Toll Road System". Keep only planned, under-construction and recently built ones (2026-11-06).
- Every row needs a source URL and a retrieved date.
- "Recently built" means opened in the last 2 years, so on or after 2024-11-06.
- Airports, seaports and factories qualify if designated (PSN or KPBU) or if the investment is at least Rp 1T.
- Include `stalled` projects.
- v1 covers toll roads only. PSN roads and bridges, airports, ports and factories come after.
- Leave out the three planned strait bridges (Bali, Malacca, Sunda) for now.
- Language: English with Indonesian names. Stack: Python scripts, plain HTML with Leaflet, GitHub Pages.
- Run `git init` in this folder.

## Sources

| Layer | Source | Used for | Caveat |
|---|---|---|---|
| Toll roads (first batch) | English Wikipedia, "Indonesian Toll Road System" (revision 1329385293, last edited 2025-12-25) | Route names, km, operators, status markers | Secondary. No opening years or coordinates. Cites BPJT's BUJT page. Stale for some rows (for example Pandaan–Malang is marked italic but is fully open) |
| Toll roads (official status) | BPJT `toll-road-list` API: `https://itrams-api.bpjt.pu.go.id/v1/reference/api/toll-road-list` | Status (`Operasi` / `Operasi Sebagian`), total and operating km, construction km, operator, endpoint coordinates, PSN flag | 77 operating or partly operating rows. Construction-only and pre-construction rows are not returned. Endpoint coordinates are sometimes misplaced (for example Bogor Ring Road) |
| Toll roads (cross-check) | Indonesian Wikipedia, "Daftar jalan tol di Indonesia" (oldid 30025554, 3 October 2026) | Full list including 0-km concessions, operating km, operators | Secondary. Lengths and operating km often differ from BPJT. Includes rows with a concession but no construction |
| Basemap | Natural Earth 1:50m admin-0 countries and populated places (`ne_50m_admin_0_countries`, `ne_50m_populated_places`) | Land outlines for the map, major city labels | Public domain. Clipped to 92–144°E, 14°S–9°N and simplified to about 500 m. Stored in `site/data/basemap.js` so no tile server is called |
| Built | BIG Satu Peta, SARANA_PRASARANA: airports (layer 4), public ports (layer 1), national toll roads (layer 14), national non-toll roads (layer 13) | Airport coordinates and ICAO/IATA codes; port build year and operating status; road lines | Service dated 2024. Responses capped at 1,000 records. An explicit field list gave a 400 error on the airport layer; `outFields=*` worked |
| Built | BIG Satu Peta, KAWASAN_KHUSUS_DAN_TRANSMIGRASI layer 4 | Industrial estate polygons | Existing estates only |
| Built | data.go.id and data.pu.go.id toll-road datasets | Operating toll roads with opening year; GeoJSON | Newest resource I found is for 2023. Recent openings need a news or BPJT check |
| Built | Kemenperin 2025 industrial estate map (satudata.kemenperin.go.id) | About 150 estates with operator and area (ha) | Existing only |
| Designated | PSN list: Permenko 7/2021 and its amendments; latest is Permenko 4/2026, in force 24 Feb 2026 | Official designation, sector, province | Province level only. Amended nine times |
| Pipeline | PPP Book 2026 (76 KPBU projects, US$63.45B, Oct 2026); KPBU portal (kpbu.kemenkeu.go.id) | Stage, capex, responsible agency | Sources disagree (see Risks) |
| About to start | INAPROC and LPSE tenders (inaproc.id, spse.inaproc.id) | Tender packages, budget ceilings (HPS), closing dates | Named by work. No coordinates |
| Factories | GEM Iron & Steel Tracker (Global Energy Monitor) | Plants of 0.5 Mt/yr or more, with status and coordinates | Iron and steel only. Some locations approximate or unknown |
| Finance | World Bank Projects API | Indonesian WB projects with status and closing dates | No coordinates |
| Geometry | OpenStreetMap: `highway=construction` with `construction=motorway` | Lines for roads under construction | Crowdsourced. Cross-check |
| Chinese-financed | AidData GeoGCDF v3 | Project footprints | Commitments only to 2021 |

**Endpoints**

- Satu Peta, SARANA_PRASARANA: `https://kspservices.big.go.id/satupeta/rest/services/PUBLIK/SARANA_PRASARANA/MapServer`
- Satu Peta, industrial estates: `https://kspservices.big.go.id/satupeta/rest/services/PUBLIK/KAWASAN_KHUSUS_DAN_TRANSMIGRASI/MapServer`
- World Bank: `https://search.worldbank.org/api/v2/projects?format=json&countrycode_exact=ID`

## Data

**Folder layout**

```
infra-id/
  plan.md
  data/
    projects.csv        # curated, one row per project (source of truth)
    raw/YYYY-MM-DD/     # each source as fetched, never edited
  scripts/              # fetch, validate, build
  site/                 # index.html (Leaflet) and data/projects.geojson
```

**Columns (v1)**

```
id,name,sector,status,status_basis,province,route,length_km,operator,opened_year,lat,lon,precision,source_url,source_type,retrieved_on,last_verified,notes
```

- `sector`: road | airport | seaport | factory
- `status`: planned | under_construction | recently_completed | stalled
- `status_basis`: the evidence behind the status, for example "Wikipedia: (under construction)"
- `precision`: exact | approximate | regency | province
- `source_type`: official | secondary
- `retrieved_on`: when we fetched the source. `last_verified`: when someone last checked the row.

**Mapping the Wikipedia article**

- "(under construction)" → `under_construction`.
- "(in preparation)" → `planned`.
- Plain (non-italic) entries are fully open. Keep one only if it opened in the last 2 years, using the year from BPJT data.
- Italic entries that are partly open, or have no status marker: check BPJT before classifying.

**Rules**

- A status change needs an official source, or two independent sources.
- Conflicts go in `notes`. Don't resolve them silently.
- Drop test or placeholder entries (for example names containing "TEST" or "PENTEST").
- Coordinates must fall roughly within 95–141°E and 11°S–6°N.
- Rows not re-checked in 6 months show as "unverified" on the map.

**Batch 1 status (2026-11-06)**

- 27 toll-road rows: 20 `under_construction`, 7 `planned`, 0 `recently_completed`.
- No toll-road corridor was fully opened between 2024-11-06 and 2026-11-06. Several sections opened in that window (for example Binjai–Langsa Section 3 in March 2025, Padang–Sicincin in May 2025, Solo–Yogyakarta Klaten–Prambanan in July 2025, Probolinggo–Banyuwangi Sections 1–2 in 2026). They are recorded in the `notes` of their corridor, which stays `under_construction`. `recently_completed` will be populated by airports, ports and factories in phase 3.
- Inclusion rule: the italic rows in the English table, with two corrections. Pandaan–Malang is dropped because BPJT shows it fully open and past the 2-year window. Yogyakarta–Solo and Yogyakarta–Sleman–YIA are merged into the single BPJT corridor Solo–Yogyakarta–NYIA Kulonprogo.
- Two under-construction rows from Indonesian Wikipedia were added because they are large Trans-Sumatra sections missing from the English table: Kuala Tanjung–Tebing Tinggi–Parapat and Betung–Tempino–Jambi.
- JORR 3 is kept as one `planned` master-plan row. Its active sections (Kamal–Teluknaga–Rajeg, Serpong–Balaraja) are noted there rather than mapped separately.
- Not yet included: 0-km concession roads such as Lhokseumawe–Sigli, Langsa–Lhokseumawe, Rengat–Pekanbaru, Jambi–Rengat, Muara Enim–Lubuk Linggau, Palembang–Tanjung Api-api, Bogor–Serpong, Sentul–Jonggol–Karawang, Balikpapan–Penajam, the IKN toll road and the Patimban access road. Add them in phase 2 when the PSN list is in place.
- Coordinates are midpoints of BPJT start/end points, so `precision` is `approximate` for every row. Bogor Ring Road uses Bogor city centre because the BPJT endpoints are misplaced.

## Pipeline

1. Fetch each source into `data/raw/YYYY-MM-DD/`.
2. Extract candidates into `data/projects.csv`, checking rows by hand where needed.
3. Validate: required fields, source URL, coordinates in bounds, no duplicates, no test entries.
4. Build `site/data/projects.geojson` from the CSV.
5. Site: one HTML page with Leaflet. Colour by status. Filter by sector and status. Detail panel with sources and dates.

**Built so far**

- `scripts/extract_wikipedia_toll_roads.py` parses the Wikipedia table into `data/raw/2026-11-06/enwiki_toll_roads_parsed.csv`.
- `scripts/build_projects.py` holds the curated list and merges BPJT fields; run it to regenerate `data/projects.csv`.
- `scripts/validate.py` checks required fields, allowed values, date formats, coordinate bounds and duplicate ids.
- `scripts/build_site_data.py` writes `site/data/projects.geojson`, `projects.js` and a downloadable `projects.csv`.
- `scripts/build_basemap.py` clips Natural Earth to the map region and writes `site/data/basemap.geojson` / `basemap.js`.
- `site/index.html` loads `projects.js` with a normal script tag, so it also works from `file://`. It has status and sector filters, a list, a detail panel, and `#project-id` deep links.
- The basemap is bundled vector geometry, not raster tiles. OpenStreetMap's tile servers reject `file://` requests, so the page never calls them. Leaflet 1.9.4 is vendored in `site/vendor/leaflet/`; the page needs no network at all.
- Local preview: `python -m http.server 8765 --directory site`.

## Phases

0. **Plan and decisions.** Done. This file.
1. **Toll roads.** Done for batch 1: 27 curated rows in `data/projects.csv`, checked against BPJT. Remaining gaps listed under Batch 1 status.
2. **Official pipeline.** PSN list, KPBU portal and INAPROC tenders. ← next
3. **Airports, ports, factories.** Satu Peta airports and ports, Kemenperin estates, GEM steel plants.
4. **Geocoding.** Replace midpoint coordinates with better points or lines; set precision per row.
5. **Map page.** Done for v1: `site/index.html`. Revisit once there is more than one sector.
6. **Publish.** GitHub Pages workflow once the repo is pushed.
7. **Monthly refresh.** Re-fetch sources, review status changes, update `last_verified`.

**Done for v1:** toll roads on the map, each with a source and dates. Validation passes. The page states its coverage.

## Risks

- **Secondary source first.** The Wikipedia article was last edited 2025-12-25. Statuses may be out of date.
- **The article disagrees with itself.** The navbox omits Yogyakarta–Solo and Jakarta Harbour Road 2, which the table marks as under construction. It also omits planned routes such as Demak–Tuban. Use the table, not the navbox.
- **Official sources disagree.** The Patimban access toll road shows Rp 5.02T capex and "Konstruksi" on the KPBU portal, but Rp 24.18T and "Transaksi" on the PU list.
- **Official lists contain junk.** The PU KPBU list has test entries.
- **Status counters are wrong.** The BPJT homepage shows 0 km under construction.
- **Opening years may lag.** The newest BPJT toll-road resource I found is from 2023.
- **The PSN list changes.** PIK 2 was dropped in 2025.
- **Coordinates are hard.** PSN lists give provinces only. Expect manual geocoding.
- **Coverage is partial.** Private factories mostly show up in news and company disclosures.

## Licensing

- **Wikipedia text:** CC BY-SA 4.0. Credit it if we reuse text. Facts still need a primary source.
- **OpenStreetMap:** ODbL. Credit OSM. A derived dataset of OSM geometry must also be ODbL.
- **GEM:** CC BY 4.0 unless the file says otherwise.
- **AidData:** ODC-BY. Credit AidData.
- **Natural Earth:** public domain, no attribution required. The page credits it anyway.
- **Leaflet 1.9.4:** BSD-2-Clause, vendored in `site/vendor/leaflet/` with its licence file.
- **Government data:** check each dataset's licence on its portal.

## Next steps

1. ~~Answer the open decisions.~~ Done 2026-11-06.
2. ~~Save the Wikipedia snapshot to `data/raw/2026-11-06/`.~~ Done.
3. ~~Extract the toll roads into `data/projects.csv`.~~ Done: 27 rows, validation passing.
4. ~~Build the Leaflet page from `data/projects.csv`.~~ Done: `site/index.html`, checked at desktop and mobile widths.
5. ~~Initialise git and make the first commit.~~ Done.
6. Publish to GitHub Pages.
7. Start phase 2: PSN list, KPBU portal and INAPROC tenders.
