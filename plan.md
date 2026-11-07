# Indonesia Infrastructure Map

A curated static atlas of major infrastructure in Indonesia: roads, airports, seaports, railways and factories that are operating, under construction, planned or stalled.

**Current execution plan:** [`plan-v3.md`](plan-v3.md) (7 November 2026). This
file records scope, decisions, architecture and history; `plan-v3.md` is the
phase-by-phase backlog for the site overhaul and the data-completeness work.
Phase 1 decisions and budgets are recorded in
[`docs/phase-1-decisions.md`](docs/phase-1-decisions.md).

**Status:** Phase 1 of the v3 overhaul is complete (2026-11-07). Phase 2 Track 2A (transport PSN) is also complete: 35 projects — 13 railways, 7 airports and 15 seaports — are in the curated tables, for 62 projects total. The site has four views, search, filters, a detail drawer, a new basemap, a mobile bottom sheet and a generated Data page. Schema v3 is frozen. 27 toll roads and 178 estates/SEZs are also in the curated tables. **Not published:** there is no GitHub remote or Pages deployment, and publishing is explicitly deferred.

**Publishing constraint:** do not create a GitHub remote, push the repository, deploy GitHub Pages or publish the site until the repository owner asks for it explicitly. The release target is a local build that works from `file://` and a local HTTP server.

## Goal

- A static atlas of Indonesia with four views: Explore, Corridors, Estates and Data.
- Projects are coloured by status and filterable by sector, status, island, province, PSN, corridor, precision and verification age.
- Clicking a project shows its details, every source, the evidence behind the status and when it was last verified.
- The site says it is "major, curated, not exhaustive" and reports its coverage honestly.

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
- Language: English with Indonesian names. Stack: Python scripts, plain HTML with Leaflet, offline static site. Publishing is deferred; do not push to GitHub.
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
| Built | Kemenperin 2025 industrial estate map (satudata.kemenperin.go.id) | About 150 estates with operator and area (ha) | Existing only. The subdomain did not resolve on 2026-11-06, so the BAJRA mirror below was used |
| Estates/SEZ | KEK National Council profiles: `https://kek.go.id/id/investment/distribution/<slug>` | SEZ name, address, coordinates, area, developer, legal basis, category | Official. 25 zones. Operational maturity is not stated |
| Estates | BAJRA, "Daftar Kawasan Industri Indonesia" (17 Aug 2024) | Industrial estate name, developer, regency, province, area | Secondary mirror of Kemenperin data. 160 rows; Kemenperin reported 179 estates in 2026 |
| Estates (coverage) | ANTARA, Kemenperin estate count (2026) | Benchmark: 179 estates, 101,351.45 ha, 57.20% occupancy | Secondary; not a row source |
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

## Data architecture (proposed 2026-11-06)

A single `projects.csv` is fine for 27 flat rows. It will not carry companies,
investment rounds, investor countries, laws and claim-level sources without
turning into a wide table full of duplicated values. The problem is not CSV as a
format; it is storing every entity in one table.

**Recommendation:** keep text-based CSVs as the editable source of truth, split
the data into normalised tables with stable ids, and generate the site JSON at
build time. Revisit SQLite only when the data or the editing workflow outgrows
this.

### Target tables

| File | One row per | Key fields |
|---|---|---|
| `projects.csv` | project | `id`, `name`, `sector`, `status`, `corridor_id`, `island`, `province`, `route`, km fields, `investment_idr_t`, `psn`, `status_as_of`, `verification`, `precision`, `last_verified` |
| `organizations.csv` | company or agency | `id`, `name`, `short_name`, `org_type`, `country_code`, `parent_id`, `website` |
| `project_organizations.csv` | project–organisation role | `project_id`, `org_id`, `role` (sponsor, operator, contractor, lender, off-taker), `share_pct`, `start_year`, `end_year`, `source_id` |
| `investments.csv` | commitment or tranche | `id`, `project_id`, `investor_org_id`, `amount`, `currency`, `amount_idr_t`, `fx_date`, `year`, `stage`, `instrument`, `share_pct`, `source_id` |
| `sources.csv` | source document | `id`, `publisher`, `title`, `url`, `published_on`, `retrieved_on`, `source_type`, `language`, `snapshot_hash`, `accessed_via`, `archive_path`, `licence`, `notes` |
| `project_sources.csv` | project–source claim | `project_id`, `source_id`, `claim` (status, length, investment, opening), `claim_value`, `claim_date` |
| `project_aliases.csv` | project alias | `project_id`, `alias`, `source_id` |
| `project_events.csv` | dated event | `project_id`, `event_date`, `event_type`, `description`, `source_id` |
| `project_geometry.csv` | project geometry | `project_id`, `kind` (point, line, polygon), GeoJSON `geometry`, `precision`, `source_id` |
| `laws.csv` | regulation | `id`, `title`, `number`, `year`, `level`, `url`, `status` |
| `project_laws.csv` | project–law relation | `project_id`, `law_id`, `relation` |
| `corridors.csv` | Trans corridor | `id`, `name`, `definition`, `total_km`, `operational_km`, `construction_km`, `planned_km`, `metric`, `as_of`, `source_id` |
| `corridor_segments.csv` | corridor segment | `segment_type`, km fields, progress, status, opening year, geometry link |
| `estates.csv` | industrial estate or SEZ | `id`, `name`, `type`, `province`, `regency`, `island`, `area_ha`, `developer`, `status`, `coordinate_source`, `sector_focus`, `legal_basis`, external ids, `source_id` |
| `estate_sources.csv` | estate–source claim | `estate_id`, `source_id`, `claim`, `claim_value`, `claim_date` |
| `coverage_targets.csv` | coverage layer | `layer`, `label`, `unit`, `target_count`, `universe`, `source_id` |

### Why this shape

- **Companies are not a project column.** A project has sponsors, an operator, contractors and lenders, often several of each, with shares and dates. A join table handles that; an `operator` string does not.
- **Investments are events, not a total.** Store each commitment or tranche separately, with its original currency. Derive the project total and the investor-country mix. This is what makes "joint venture", "domestic vs foreign" and "which country" answerable later.
- **Sources are first-class.** One source can support many projects; one project needs several claims. A `source_url` column cannot express which claim a link supports.
- **Laws are not news.** A regulation and a news article are different objects. Keep `laws` separate from `sources`.
- **No semicolon lists.** Multi-valued facts become rows in a join table.
- **Derived data is disposable.** `data/projects.csv` and `site/data/*` are build outputs. Curated inputs live in `data/curated/`; raw snapshots stay in `data/raw/`.

### Migration order

1. Move the curated project list out of `scripts/build_projects.py` into `data/curated/projects.csv`. The script should read, validate, merge and build, not hold the data.
2. Add `sources.csv` and `project_sources.csv`; replace the free-text `source_url` with references. Keep a generated display URL for the site.
3. Add `organizations.csv` and `project_organizations.csv`; replace `operator`. Seed with the 20 operators already in batch 1.
4. Add `investments.csv`, `laws.csv` and `project_laws.csv` before the factories batch, where investor, amount and legal basis are central.
5. Add `corridors.csv` (and later `corridor_segments.csv`) for the Trans Sumatra, Sulawesi, Papua and Kalimantan progress section.
6. Keep `data/derived/` and `site/data/` generated. Do not edit them by hand.
7. Revisit SQLite when any of these is true: more than about 1,000 projects, several concurrent editors, or queries that genuinely need SQL. If that happens, the build script should still export CSV/JSON for review.

**Why not SQLite now?** It adds a binary file to git, a migration tool and a query layer, while the dataset is small and the main need is reviewable diffs. **Why not JSON per project?** It duplicates schema handling and makes cross-project checks and joins harder. CSV plus validation gives most of the relational discipline with none of the infrastructure.

**Decided 2026-11-06:** adopt the normalised CSV model. `data/curated/` is the
editable source of truth; `data/projects.csv` and `site/data/` are generated.
Revisit SQLite only when the triggers above are met.

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
- No toll-road corridor was fully opened between 2024-11-06 and 2026-11-06. Several sections opened in that window (for example Binjai-Langsa Section 3 in March 2025, Padang-Sicincin in May 2025, Solo-Yogyakarta Klaten-Prambanan in July 2025, Probolinggo-Banyuwangi Sections 1-2 in 2026). They are recorded in the `notes` of their corridor, which stays `under_construction`. The `recently_completed` status is now used by the Benoa Port expansion (2025).
- Inclusion rule: the italic rows in the English table, with two corrections. Pandaan–Malang is dropped because BPJT shows it fully open and past the 2-year window. Yogyakarta–Solo and Yogyakarta–Sleman–YIA are merged into the single BPJT corridor Solo–Yogyakarta–NYIA Kulonprogo.
- Two under-construction rows from Indonesian Wikipedia were added because they are large Trans-Sumatra sections missing from the English table: Kuala Tanjung–Tebing Tinggi–Parapat and Betung–Tempino–Jambi.
- JORR 3 is kept as one `planned` master-plan row. Its active sections (Kamal–Teluknaga–Rajeg, Serpong–Balaraja) are noted there rather than mapped separately.
- Not yet included: 0-km concession roads such as Lhokseumawe–Sigli, Langsa–Lhokseumawe, Rengat–Pekanbaru, Jambi–Rengat, Muara Enim–Lubuk Linggau, Palembang–Tanjung Api-api, Bogor–Serpong, Sentul–Jonggol–Karawang, Balikpapan–Penajam, the IKN toll road and the Patimban access road. Add them with the road batch in Phase 2 of `plan-v3.md`.
- Coordinates are midpoints of BPJT start/end points, so `precision` is `approximate` for every row. Bogor Ring Road uses Bogor city centre because the BPJT endpoints are misplaced.

## Pipeline

1. Fetch each source into `data/raw/YYYY-MM-DD/`.
2. Extract candidates into `data/projects.csv`, checking rows by hand where needed.
3. Validate: required fields, source URL, coordinates in bounds, no duplicates, no test entries.
4. Build `site/data/projects.geojson` from the CSV.
5. Site: one HTML page with Leaflet. Colour by status. Filter by sector and status. Detail panel with sources and dates.

**Built so far**

- `scripts/extract_wikipedia_toll_roads.py` parses the Wikipedia table into `data/raw/2026-11-06/enwiki_toll_roads_parsed.csv`.
- `data/curated/` holds the editable tables: projects, organisations, roles, sources, claims, external ids, investments, laws, corridors and segments.
- `scripts/build_projects.py` reads the curated tables, joins operator and source, fills gaps from BPJT and writes the flat `data/projects.csv`.
- `scripts/validate.py` checks schemas, enums, dates, coordinates, ranges and foreign keys across the curated tables.
- `scripts/build_site_data.py` writes project and corridor payloads to `site/data/`.
- `scripts/build_basemap.py` clips Natural Earth to the map region and writes `site/data/basemap.geojson` / `basemap.js`.
- `site/index.html` loads `projects.js` with a normal script tag, so it also works from `file://`. It has status and sector filters, a list, a detail panel, and `#project-id` deep links.
- The basemap is bundled vector geometry, not raster tiles. OpenStreetMap's tile servers reject `file://` requests, so the page never calls them. Leaflet 1.9.4 is vendored in `site/vendor/leaflet/`; the page needs no network at all.
- Local preview: `python -m http.server 8765 --directory site`.

## Scope v2 (proposed 2026-11-06)

The next version adds kilometres, railways, airports, seaports, factories and a
Trans-corridor progress section. The data model changes first (see Data
architecture).

**Km and progress.** Linear projects get `length_km` (total), `operational_km`,
`construction_km` and an optional reported `progress_pct`. The site shows a bar
and the raw figures. Non-linear assets (airports, ports, factories) use
`investment_idr_t`, `capacity` and `capacity_unit`; km stays blank.

**New sectors.** road, railway, airport, seaport, factory. Industrial estates are
a factory subtype until there are enough to separate.

**Status.** The strict two-year window excludes almost every airport and port.
The Kemenhub PSN review of 19 February 2026 counts 35 transport PSNs: 29 are
complete or operating, 18 are proposed for removal from the PSN list, and only 6
are still in construction. All seven PSN airports opened between 2020 and 2023.
Proposal: add an `operating` status for major assets opened before 2024-11-06,
kept distinct from `recently_completed`. Without it the airports section would
contain only Bali Utara, which is planned.

**Transport baseline (Kemenhub, 19 February 2026).**

| Mode | PSNs | Status |
|---|---:|---|
| Airports | 7 | all operating (2020–2023); no PSN airport under construction |
| Seaports | 15 | 13 operating (11 completed, plus Patimban and Benoa); Patimban Phase I-2 under construction; New Palembang and Muaro Jambi planned |
| Railways | 13 | 9 operating; MRT N-S 48.14% (Phase 2A 55.89%); LRT Velodrome–Manggarai 89.22%; MRT E-W and KA logistik Kaltim planned |

**Trans corridor section.** A separate `corridors.csv` and a panel showing total,
operational, under-construction and planned km, with an as-of date and metric.
The four corridors are not comparable as published:

| Corridor | Definition | Figures found | Treatment |
|---|---|---|---|
| Trans Sumatra | Toll backbone (JTTS) | 2,854 km ultimate; 1,161 km built; 982 km operational (Hutama Karya, Aug 2026) | aggregate bar; Bina Marga's 1,051.84 km Phase I figure conflicts, note it |
| Trans Papua | National road, Sorong–Merauke | 4,330 km total; 3,446 km connected (Jul 2025); 2,235 km paved (Nov 2025) | two metrics: connected and paved |
| Trans Sulawesi | National road corridor plus planned toll | no single official total; a JICA corridor study and a 1,300+ km toll plan use different scopes | segment view, no aggregate until defined |
| Trans Kalimantan | National road corridor | 1,186 km travel route, 1,920 km border-parallel road and 2,100.8 km WPS figure are different things | segment view, no aggregate until defined |

**Factories.** Single plants or estates with investment of at least Rp 1T,
operating or under construction. Start with PSN smelters, GEM steel plants and
the large nickel, aluminium, copper and battery projects. Investment rows,
investor organisations and claim-level sources are prerequisites, so factories
come after the schema migration.

**Industrial estates and SEZs (data only).** `data/curated/estates.csv` holds 178
records: 25 SEZs from the official KEK profiles, 153 industrial estates from a
2024 Kemenperin-derived table, and 7 zones marked `both`. SEZ rows carry official
zone coordinates, area, developer, legal basis and category. Industrial-estate
rows carry developer, regency/province and area, with regency-centroid
coordinates (`precision=regency`). The list is close to, but not the same as, the
179 estates Kemenperin reported in 2026: 2025 additions and exact boundaries are
still missing. The data is validated, read by the site build and shown in the
Estates table; the map layer remains off.

**Known gap.** Nine estates announced in 2025 are not in the table: IPIP (listed
by Kemenperin under Central Sulawesi, though Pomalaa is in Southeast Sulawesi),
I-Sentra Lamongan, Huadi Bantaeng, Cikembar II, Losarang, Purwakarta Integrated
Industrial Park, Pulau Penebang, Seafer and Tembesi. Add them with individual
sources for area, developer and coordinates.

**Site changes.** Done in v3 Phase 1: four views, sector/status/island filters,
search, km and operational-share bars, investment or capacity in the drawer, a
corridor section, generated coverage in the header and Data view, and the
offline basemap. Railway, airport and seaport rows arrived in Phase 2; factory rows are still to come.

**Decided 2026-11-06.**

1. Adopt the normalised CSV model. Done.
2. Add an `operating` status, distinct from `recently_completed`. Done.
3. Publish segment-level progress with a data-gap note for Trans Sulawesi and
   Trans Kalimantan until a single official series exists. The site currently
   shows the data-gap note only.

**Implementation order.** ~~Schema migration~~ → ~~km fields and corridor
data/UI~~ → ~~industrial estates and SEZs (data only)~~ → Kemenhub transport batch
(rail, ports, airports) → factories pilot → docs.

## Phases

0. **Plan and decisions.** Done. This file and `plan-v3.md`.
1. **Toll roads.** Done for batch 1: 27 curated rows in `data/projects.csv`, checked against BPJT. Remaining gaps listed under Batch 1 status.
2. **Official pipeline.** Kemenhub transport PSN deck and KPPIP pages snapshotted; the full PSN/KPBU/INAPROC pass is still open.
3. **Industrial estates and SEZs.** First pass done: 178 records in `data/curated/estates.csv`, validated and shown as a table. Remaining: 2025 additions, exact boundaries and better coordinates. Map layer still off.
4. **v3 Phase 1 — foundation and experience.** Done 2026-11-07: design tokens, bundled fonts, four-view shell, search, filters, detail drawer, map v2, mobile sheet, Data view and schema v3. See `docs/phase-1-decisions.md`.
5. **v3 Phase 2 - data completion.** Transport PSN (35/35) is done. Next: estate reconciliation and coordinates, factories, roads and corridor segments. ← in progress
6. **v3 Phase 3 — trust and local release.** Claims, freshness, Data view v2, downloads, conflicts, local CI and hand-off. **Do not push to GitHub or publish.**
7. **Monthly refresh.** Re-fetch sources, review status changes, update `last_verified`, rebuild and verify locally.

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
- **Leaflet.markercluster 1.5.3:** MIT, vendored in `site/vendor/markercluster/`.
- **Inter and Source Serif 4:** SIL OFL 1.1, bundled under `site/assets/fonts/` with their licence files.
- **Government data:** check each dataset's licence on its portal.

## Next steps

1. ~~Answer the open decisions.~~ Done 2026-11-06.
2. ~~Save the Wikipedia snapshot to `data/raw/2026-11-06/`.~~ Done.
3. ~~Extract the toll roads into `data/projects.csv`.~~ Done: 27 rows, validation passing.
4. ~~Build the Leaflet page from `data/projects.csv`.~~ Done and superseded by the v3 shell.
5. ~~Normalise the data model and add km/corridor support.~~ Done.
6. ~~Gather the industrial estate and SEZ first pass.~~ Done: 178 rows, validated.
7. ~~v3 Phase 1: shell, experience, map v2, schema v3.~~ Done 2026-11-07.
8. Add the Kemenhub transport batch (rail, ports, airports). ← next
9. Add the factories batch.
10. Complete Phase 2, then Phase 3. Do **not** publish or push to GitHub.
