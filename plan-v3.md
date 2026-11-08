# V3 Overhaul Plan — Site Experience and Data Completeness

**Status:** Phase 1 complete, 7 November 2026. Phase 2 complete except the
partial estate layer and deferred corridor geometry, 8 November 2026. Phase 3
complete, 8 November 2026: 107 projects, 479 atomic project claims, 19 conflicts,
285 freshness rows and 189 dictionary fields, with a deterministic local build
and a browser smoke test. The release is **local only**.
**Evidence:** [`docs/phase-3-trust.md`](docs/phase-3-trust.md),
[`docs/refresh-runbook.md`](docs/refresh-runbook.md) and
[`docs/evidence/phase-3/`](docs/evidence/phase-3/).
**Supersedes:** the roadmap and "Where to pick up" sections of `plan.md`.
**Scope:** the site (`site/`) and the curated dataset (`data/curated/`).
**Hard constraints that do not change:** English UI with Indonesian proper names;
plain HTML, CSS and classic JavaScript; Leaflet; works offline and from `file://`;
no tile server, CDN or `fetch`; every row has a source and a verification date.

**Publishing constraint (7 November 2026):** do **not** push this repository to
GitHub, add a remote, publish the site or deploy GitHub Pages. Phase 3 ends with
a local release that works from `file://` and a local HTTP server. Publishing is
deferred until the repository owner asks for it explicitly.

This is an execution backlog, not a vision deck. Work top to bottom. Each item
has an ID, a concrete outcome, acceptance criteria and a size. Do not start an
item before its dependencies are done.

---

## 1. Why this plan exists

### 1.1 What the site audit found

The current page reads as a prototype, not a published atlas.

| Area | Today | Problem |
|---|---|---|
| Shell | 390 px sidebar, map fills the rest | At 861 px viewport height only three project rows are visible; filters, tab strip and the coverage paragraph consume most of the panel |
| Visual language | System font, dark top bar, pale beige map | Flat hierarchy, low contrast, no editorial identity, nothing signals quality or trust |
| Map | 27 identical coloured circles | Java markers overlap heavily; no clustering, sector encoding or labels; hover is a name-only tooltip; zoom capped at 9 |
| Filters | Nine always-visible checkboxes | Three status filters have zero rows; legend duplicates the filter list; no province, PSN, corridor or verification filter |
| Search | None | The only way to find a project is to scroll a short list |
| List | Name, province, status, km | No sector icon, progress bar, investment, sort control or grouping; long names wrap badly |
| Detail | One panel, one source, one text block | No timeline, phase history, confidence level, related assets or previous/next navigation |
| Mobile | 46 dvh map strip above a 2,604 px page | The list starts below the fold; filters push it further down; the map scrolls away; detail is a separate overlay |
| Copy | "Toll roads" in the meta description; "railways... being added" in the footer | Stale and contradicts the data model |
| Trust | Hardcoded "Last verified" date; one footer paragraph | No methodology, coverage matrix, source register, changelog or data download |
| Accessibility | Colour-only status, small targets, no focus management | Fails the basic WCAG 2.2 AA expectations for a public information site |
| Performance | 27 individual markers | Fine today; will collapse at 300+ projects and 197 estates |

The underlying cause is structural: the interface was designed for one sector
and 27 rows, then the data model was generalised without redesigning the
interface around it.

### 1.2 What the data audit found

| Layer | Current | Reality |
|---|---:|---|
| Projects | 27 | All roads. 20 under construction, 7 planned. Zero operating, recently completed or stalled |
| Railways | 0 | 13 PSN railway projects already listed in the official Kemenhub deck |
| Airports | 0 | 7 PSN airports, all opened 2020–2023 |
| Seaports | 0 | 15 PSN seaports, 11 opened 2018–2023, 4 with later or partial status |
| Factories | 0 | No PSN smelters, steel, aluminium, copper or battery plants |
| Industrial estates | 160 | Kemenperin reports 179 in 2026; 19 missing, including nine named 2025 additions |
| SEZs | 25 | Official profiles complete for name, area, developer, legal basis and coordinates |
| Estate unique rows | 178 | Target is about 197 after reconciling 179 industrial estates and 25 SEZs with 7 overlaps |
| Corridors | 4 | Only Trans Sumatra and Trans Papua have kilometre series; Trans Sulawesi and Trans Kalimantan are data-gap notes; `corridor_segments.csv` is empty |
| Sources | 38 | 32 official, 6 secondary; one claim per project on average |

Other concrete gaps:

- 10 of 27 road rows have `psn=unknown`; 0 have an investment figure; 0 have a
  progress percentage; 0 have an `opened_year`.
- All 27 road rows are `precision=approximate`. Estate coordinates are regency
  centroids except for the 25 SEZs.
- No estate has a website; only the 25 SEZs have `sector_focus`, `legal_basis`
  and `established_year`.
- All 178 estates are marked `operating`; operational maturity is unverified.
- There is no status history, no per-fact claim trail, no geometry table and no
  freshness report.
- The 2025 estate additions are documented as a gap but not researched:
  IPIP, I-Sentra Lamongan, Huadi Bantaeng, Cikembar II, Losarang, Purwakarta
  Integrated Industrial Park, Pulau Penebang, Seafer and Tembesi.

### 1.3 Root causes

1. The product was never defined beyond "major, curated, not exhaustive". There
   is no universe to measure completeness against.
2. The interface was built for a toll-road batch and never redesigned when the
   schema gained sectors, corridors and estates.
3. The pipeline is excellent at validating rows but has no extraction path for
   the next sectors, so data work is manual and slow.
4. There is no trust layer: no coverage report, no methodology page, no
   freshness signal and no source register in the UI.

---

## 2. Target product

**One sentence:** an offline-capable, source-linked atlas of Indonesia's major
infrastructure, where anyone can see what is operating, what is being built,
what is planned and what has stalled — and check the evidence.

**Principles**

1. **Map first, evidence always.** The map is the entry point; the detail panel
   is the proof.
2. **Curated, not exhaustive — but measured.** Every layer has a defined
   universe and a coverage number against it.
3. **Status is a dated claim.** No status without a source, a date and a basis.
4. **Calm, editorial design.** Data-dense but not cluttered. No dashboard
   ornament, no gradients, no glassmorphism.
5. **Offline is a feature.** The page must work from `file://` and a static host
   with no network.
6. **Mobile is a first-class view.** The map and the list must not fight for
   the same scroll.

**What "done" looks like**

- 35/35 transport PSN projects, 179 industrial estates, 25 SEZs, 20–30 major
  factories and 40–50 major road corridors are in the curated tables.
- Every row has a source, a verification date and coordinates with a precision.
- Every status change has an official source or two independent sources.
- The site has four views (Explore, Corridors, Estates, Data), search, filters,
  URL state, a detail timeline and a source register.
- The page passes a WCAG 2.2 AA audit and loads in under 1.5 s on a mid-range
  phone from a local file.
- CI validates and builds; publishing is explicitly deferred until requested.

**Non-goals**

- Live tracking, real-time traffic, routing or navigation.
- An exhaustive list of every infrastructure project in Indonesia.
- User accounts, comments, favourites or editing in the browser.
- 3D, satellite imagery or an online tile dependency.
- Property listings or investment advice.

---

## 3. Experience design

### 3.1 Design language

**Direction:** an editorial atlas, not a startup dashboard. Think a well-made
annual report or a financial-press graphics desk: warm paper, ink, hairlines,
one accent, strong typography, generous whitespace, restrained colour.

Reference points: Our World in Data (clarity, source discipline), Financial Times
visual journalism (typographic hierarchy, maps), Reuters Graphics (annotation),
Indonesian government annual reports (authority, not decoration).

**Avoid:** gradients, glassmorphism, drop shadows on everything, emoji, flag
motifs, cartoon icons, rounded cards inside rounded cards, dark mode as a
default.

**Design tokens**

| Token | Value | Use |
|---|---|---|
| `--ink` | `#101828` | Body text, headings |
| `--navy` | `#0B1F33` | Top bar, map chrome |
| `--paper` | `#FBF9F4` | Page background |
| `--surface` | `#FFFFFF` | Cards, panels |
| `--muted` | `#667085` | Secondary text |
| `--line` | `#E4E7EC` | Hairlines, dividers |
| `--accent` | `#B54708` | Links, focus, active states |
| `--uc` | `#C2410C` | Under construction |
| `--planned` | `#1D4ED8` | Planned |
| `--operating` | `#0F766E` | Operating |
| `--done` | `#15803D` | Recently completed |
| `--stalled` | `#B42318` | Stalled |

**Typography**

- Display: a bundled OFL serif for `h1`, `h2` and large figures. Recommended:
  Source Serif 4, subset to Latin plus the Indonesian characters needed.
- UI: a bundled OFL sans. Recommended: Inter, variable or three weights.
- Both are local WOFF2 files under `site/assets/fonts/`; `@font-face` must work
  from `file://`. Fallbacks: Georgia and the system UI stack.
- Scale: 12, 13, 14, 16, 20, 28, 40 px. Line height 1.2 for display, 1.5 for
  body. Numbers use tabular figures.

**Shape and depth**

- Radius 8 px for controls, 12 px for cards, 16 px for sheets.
- One shadow token for floating elements only:
  `0 12px 32px rgba(16, 24, 40, .12)`.
- Hairline borders instead of shadows for panels.

**Icons**

- One inline SVG sprite, 16 px stroke, 1.5 px weight: road, railway, airport,
  seaport, factory, search, filter, close, chevron, external link, download,
  share, check.
- Sector icons appear in list rows, map markers and detail headers.

### 3.2 Desktop layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  INDONESIA INFRASTRUCTURE ATLAS   [search........]   35 PSN · 197 estates  Data │
├───────────────────────┬──────────────────────────────────────────────────────┤
│ Explore Corridors     │                                                      │
│ Estates Data          │                                                      │
│                       │                                                      │
│ [All] [Road] [Rail]   │                     MAP                              │
│ [Air] [Sea] [Factory] │                                                      │
│                       │                                                      │
│ Status: chips         │                                                      │
│ Sort: status ▾        │                                                      │
│ ─────────────────     │                                                      │
│ ● Name       [status] │                                                      │
│   Province · sector   │                                                      │
│   ▓▓▓▓░░ 65%          │                                                      │
│ ─────────────────     │                                                      │
│ ● Name       [status] │                                                      │
│ ...                   │                                                      │
│                       │                                                      │
│ 27 of 321             │                                                      │
└───────────────────────┴──────────────────────────────────────────────────────┘
                                                ┌──────────────────────────────┐
                                                │ Detail drawer (400 px)       │
                                                └──────────────────────────────┘
```

- Top bar: 64 px, navy, brand at left, global search in the centre-left,
  live coverage summary and a **Data** link at right.
- Sidebar: 380 px, white, independently scrollable. Tabs at the top; filters
  in a compact row; list below; result count pinned at the bottom.
- Map: fills the remaining space. Detail drawer slides from the right over the
  map; the list stays visible. The map pans so the selected marker is not
  covered.
- Attribution is a small bottom-right line, not a banner.

### 3.3 Mobile layout

```
┌──────────────────────────────┐
│ ☰  Atlas        [search]  ⚙  │  app bar
├──────────────────────────────┤
│                              │
│           MAP                │  fills viewport
│                              │
│                              │
├──────────────────────────────┤
│ ────                         │  bottom sheet handle
│ 27 projects · 6 sectors      │  peek state
│ ● Sigli–Banda Aceh   65%     │
│ ● Binjai–Langsa      42%     │
└──────────────────────────────┘
```

- The map is full-viewport (`100dvh`) behind a persistent app bar.
- A draggable bottom sheet has three snap points: **peek** (count + two rows),
  **half** (scrollable list), **full** (filters or detail).
- Tapping a row expands the sheet to detail; tapping the map collapses it.
- Filters open as a full-screen sheet with **Apply** and **Clear all**. The
  result count updates live.
- No page-level scroll. Each region scrolls internally.
- Touch targets are at least 44 px. The sheet respects safe-area insets.

### 3.4 Information architecture

| Tab | Purpose | Primary content |
|---|---|---|
| **Explore** | Find and inspect a project | Search, filters, list, map, detail |
| **Corridors** | Understand network progress | Five Trans corridor cards, segment tables, definitions, data gaps |
| **Estates** | Browse the zone inventory | Summary strip, table of 197 estates and SEZs, filters, CSV download |
| **Data** | Trust and reuse | Coverage matrix, methodology, status definitions, source register, downloads, changelog, known gaps |

The current two-tab switch becomes four tabs. Estates remain a **table view**
until their data is refined in Phase 2; the map layer is added only after
coordinates are verified and is off by default.

### 3.5 Explore view

**Search**

- One input searches project name, province, regency, operator/developer,
  corridor, estate name and aliases.
- Results are ranked: exact prefix, word prefix, substring.
- `Ctrl/Cmd+K` focuses search; `Esc` clears it.
- The index is built at build time into `site/data/search.js`; no network.

**Filters**

- Sector chips with icons and counts: All, Road, Railway, Airport, Seaport,
  Factory. Multi-select.
- Status chips with coloured dots and counts. Multi-select. Zero-count chips
  are muted but still visible.
- **More filters** popover: island, province, PSN status, corridor, verification
  age (fresh under 6 months, stale), coordinate precision.
- Active filters render as removable chips under the bar, plus **Clear all**.
- Filter state is encoded in the URL hash (see 3.12).

**Sort**

- Default: status order (under construction, recently completed, planned,
  operating, stalled), then name.
- Alternatives: name A–Z, recently verified, largest investment, longest
  length, progress.

**List rows**

```
●  [icon]  Sigli–Banda Aceh Toll Road              [Under construction]
           Aceh · Road · PSN                      65% · 48.6 / 74.2 km
           ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░
```

- Left status dot; sector icon; name; status pill; province, sector and PSN
  tags; one key figure; optional mini progress bar.
- Selected row gets a 3 px accent left border and a tinted background.
- Rows are 64–72 px tall, so 9–11 fit in the panel at 900 px height.
- Hover shows a subtle tint; focus ring is visible.
- Keyboard: `↑`/`↓` move, `Enter` opens, `Esc` closes detail.

**Result summary**

- "27 of 321 projects" updates live.
- When filters return zero: an empty state with **Clear filters** and a short
  explanation, not a blank list.

### 3.6 Map

**Basemap v2**

- Natural Earth 1:50m or 1:10m, clipped to 92–144°E, 14°S–9°N.
- Layers: land, country borders, province boundaries, lakes, major rivers,
  urban areas, 30 city labels.
- Muted palette: `#F4F1E8` land, `#DCE9F2` water, `#C9CDD4` borders,
  `#6B7280` labels. No satellite, no hillshade.
- Labels avoid the marker layer; city labels are small caps, 10–11 px.
- Build with Shapely simplification to keep the payload under 150 KB gzipped.

**Markers**

- 28 px circle, filled by status, white sector glyph inside, 2 px white ring.
- Selected: 40 px, accent ring, name label to the right with a white halo.
- Hover: tooltip with name, status, province and one key figure.
- Cluster below zoom 7: a donut showing the status mix with a total in the
  centre; click zooms in.
- At zoom 5–6 show clusters; at 7–8 individual markers; at 9+ optional labels.

**Layers**

- Projects on by default.
- Estates off by default, toggled from the Estates tab or the layer control.
- Corridor geometry on when the Corridors tab is active.
- Layer control is a small floating card, not a permanent legend.

**Controls**

- Zoom bottom-right, scale bar bottom-left, layer control top-right,
  "Fit Indonesia" reset.
- Legend is collapsible and explains status colours and sector glyphs.
- No default Leaflet attribution box competing with the footer; attribution
  becomes one compact line.

**Behaviour**

- Filtering updates existing layer groups; it does not rebuild the map.
- Selecting a marker opens the drawer and pans with an offset so the marker
  stays visible beside the drawer.
- Closing the drawer clears the URL state.
- `prefers-reduced-motion` disables fly-to animations.

### 3.7 Detail drawer

```
[Under construction]  [Road icon]                    [share] [close]
Sigli–Banda Aceh Toll Road
Aceh · PSN · 74.2 km

┌──────────────┬──────────────┬──────────────┐
│ 65%          │ 48.6 km      │ Rp 12.4 T    │
│ operational  │ operational  │ investment   │
└──────────────┴──────────────┴──────────────┘

Progress  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░  65%

WHY THIS STATUS
12 Aug 2026  Section 6 opened; 25.6 km remain.     [official]
04 Mar 2025  Section 3 opened.                      [official]

TIMELINE
2023  Groundbreaking
2025  Section 3 opened
2026  Section 6 opened
2027  Target completion

SOURCES
BPJT toll-road list · official · retrieved 6 Nov 2026   [open]
Hutama Karya statement · official · 12 Aug 2026          [open]

NOTES
BPJT labels the corridor "Operasi Sebagian"; the remaining
section is under construction.

Coordinate precision: approximate · Last verified: 6 Nov 2026
```

- Header: status pill, sector icon, name, location, share and close.
- Key figures: at most four, chosen by sector (length/progress/investment/
  capacity/opened).
- Progress bar for linear projects.
- **Why this status**: dated evidence entries, each with a source badge.
- **Timeline**: events from `project_events.csv`.
- **Sources**: every claim, publisher, type, retrieved date, link.
- **Notes**: conflicts and caveats in a tinted callout, never hidden.
- **Related**: corridor, nearby estates, operator.
- **Footer**: precision, last verified, project ID.
- Previous/next buttons walk the current filtered list.
- Mobile: the same content becomes a full-height sheet with a drag handle.

### 3.8 Corridors view

- Overview strip: five cards, each with definition, metric, progress bar,
  as-of date, source and a one-line gap note. Cards carry an explicit coverage
  state: complete series, partial segment table, route total only or no series.
- Selecting a corridor opens a detail panel:
  - total, operational, under construction and planned km;
  - stacked bar with a four-part legend, including unallocated length;
  - segment table: segment, length, status, opened year, source and notes;
  - grouped timeline of exact-dated openings;
  - "What this figure includes" definition and known conflicts.
- Trans Sulawesi and Trans Kalimantan publish route totals only: show the total
  and say that no operational-km series exists. Never invent an aggregate or a
  percentage.
- `corridor_segments.csv` powers the tables; the map can highlight segments
  once geometry exists.

### 3.9 Estates view

- Summary strip: total zones, total area, SEZ count, industrial-estate count,
  provinces covered.
- Filter by type (SEZ, industrial estate, both), province, island, sector focus,
  status and area range.
- Table columns: name, type, province/regency, area, developer, status, sector,
  source. Sortable.
- Row click expands an inline detail card: legal basis, established year,
  website, coordinates, notes, source.
- **Open on map** appears only after the map layer exists.
- CSV download of the current filtered set.
- The table is readable at 390 px: collapse to two lines per row, not a
  horizontal scroll.

### 3.10 Data view

Sections:

1. **What this is / is not** — one paragraph.
2. **Coverage matrix** — sector × status counts, target universe, gap, last
   verified. Generated at build time, never hand-typed.
3. **Status definitions** — the five statuses with examples.
4. **Inclusion rules** — PSN/KPBU, Rp 1T threshold, estate lists, exclusions
   (Bali, Malacca and Sunda strait bridges).
5. **Source register** — publisher, title, type, retrieved date, archive path,
   what it is used for.
6. **Known gaps** — the living list: 2025 estates, Trans Sulawesi/Kalimantan
   aggregates, SEZ operational maturity, geometry, factory coverage.
7. **Downloads** — projects CSV, estates CSV, sources CSV, GeoJSON.
8. **Changelog** — dated entries: added, changed, corrected.

### 3.11 Accessibility and performance

**Accessibility (WCAG 2.2 AA)**

- Status is never conveyed by colour alone: pill text, icon and label.
- Every control is keyboard reachable; focus ring is visible and not removed.
- The list is the accessible equivalent of the map; a "Skip map" link moves to
  it.
- Detail drawer traps focus while open and returns focus on close.
- Result counts use `aria-live="polite"`.
- Contrast: at least 4.5:1 for body text, 3:1 for large text and UI borders.
- Touch targets at least 44 × 44 px.
- `prefers-reduced-motion` disables transitions and fly-to.
- Map markers have accessible names; the selected marker is announced.
- Test with keyboard only, a screen reader (NVDA), and 200% zoom.

**Performance budgets**

| Budget | Target |
|---|---|
| Initial HTML + CSS + JS | under 120 KB gzipped |
| Initial data (projects + corridors + stats) | under 200 KB gzipped |
| Basemap | under 150 KB gzipped |
| Estate layer (lazy) | under 80 KB gzipped |
| Time to interactive, mid-range phone, local file | under 1.5 s |
| Map pan/zoom | 60 fps at 300 markers with clustering |
| Console errors | zero |

- Split heavy layers: load `estates.js` only when the Estates tab or estate
  layer is first opened.
- Cluster markers below zoom 7.
- Reuse layer groups on filter changes.
- Never load a font weight that is not used.

### 3.12 Routing and URL state

`file://` blocks the History API in some browsers and blocks ES modules and
`fetch`. Use a hash router with plain classic scripts.

Examples:

```
site/index.html#/explore
site/index.html#/explore?sector=railway&status=operating&q=jakarta
site/index.html#/project/tol-sigli-banda-aceh
site/index.html#/corridors/trans-sumatera
site/index.html#/estates?type=sez&province=Bali
site/index.html#/data
```

- Parse the hash on load and on `hashchange`.
- Filters, sort and search are serialised into the hash.
- Deep links remain stable because IDs are stable.
- Invalid hashes fall back to `#/explore` with a small toast.

---

## 4. Data model and pipeline

### 4.1 New tables

| Table | One row per | Key fields | Why |
|---|---|---|---|
| `project_events.csv` | dated event | `id`, `project_id`, `event_date`, `event_type`, `description`, `source_id` | Timeline, recent openings, stalled/resumed history |
| `project_geometry.csv` | geometry | `project_id`, `kind`, `geojson`, `precision`, `source_id` | Lines for roads and railways, polygons for zones later |
| `estate_sources.csv` | estate–source claim | `estate_id`, `source_id`, `claim`, `notes` | Multiple sources per estate, not one |
| `coverage_targets.csv` | layer target | `layer`, `target_count`, `universe`, `source_id`, `notes` | Makes completeness measurable |

`event_type` values: `announced`, `groundbreaking`, `contract`, `financial_close`,
`section_opened`, `opened`, `stalled`, `resumed`, `target_changed`.

### 4.2 Field additions

**`projects.csv`**

- `island` — Sumatra, Java, Kalimantan, Sulawesi, Papua, Bali-Nusa Tenggara,
  Maluku.
- `expected_open_year` — for planned and under-construction rows.
- `status_as_of` — date of the evidence behind the current status.
- `verification` — `official`, `dual`, `single` (or `unverified`).
- `aliases` — semicolon-free; use a separate `project_aliases.csv` if needed
  for search. Prefer a table over a list field.

**`estates.csv`**

- `island`
- `developer_org_id` — foreign key to `organizations.csv`; keep `developer` as
  the display string for legacy rows.
- `occupancy_pct` — only when a source reports it.
- `kemenperin_id`, `sez_id` — external identifiers.
- `coordinate_source` — `official`, `osm`, `regency`, `manual`.

**`corridor_segments.csv`**

- `operational_km`, `construction_km`, `progress_pct`, `expected_open_year`,
  `geometry_id`.
- `segment_type` — `section`, `phase`, `package`.

**`sources.csv`**

- `language`, `snapshot_hash`, `accessed_via`.

**`project_sources.csv`**

- Use the `claim` field consistently: `status`, `length`, `investment`,
  `capacity`, `operator`, `opening`, `location`, `legal_basis`, `cost`.
- Add `claim_value` so a numeric fact can be traced to the exact source value.
- Add `claim_date` for the date the source states the fact.

### 4.3 Pipeline changes

```
data/raw/YYYY-MM-DD/       immutable snapshots
        │
        ▼
data/derived/              extracted staging (never published)
        │
        ▼
data/curated/              human-reviewed source of truth
        │
        ├─ validate.py     schema, enums, FKs, ranges, freshness
        ├─ build_projects.py
        ├─ build_estates.py
        ├─ add_factories.py
        ├─ build_events.py
        └─ build_coverage.py
        │
        ▼
data/projects.csv          flat export
data/coverage.csv          generated coverage report
        │
        ▼
build_site_data.py         per-layer payloads, search index, stats
        │
        ▼
site/data/*.js             window.INFRA payloads
```

New scripts:

| Script | Purpose |
|---|---|
| `scripts/build_all.py` | Run validate → build → site in the correct order; used by CI |
| `scripts/build_transport.py` | Extract the 35 PSN transport rows from the Kemenhub deck and KPPIP snapshots into staging |
| `scripts/add_factories.py` | Import the frozen factory universe, organisations, investments and claims |
| `scripts/geocode_factories.py` | Refresh the cached Nominatim checks for factory coordinates (provenance only) |
| `scripts/build_factories_ledger.py` | Write the reviewable 27-row factory ledger to `data/derived/` |
| `scripts/build_events.py` | Build `project_events.csv` from curated event rows and status transitions |
| `scripts/build_coverage.py` | Compare curated counts with `coverage_targets.csv`; write `data/coverage.csv` and site stats |
| `scripts/freshness.py` | List rows older than six months; write a stale report |
| `scripts/check_site.py` | Assert payload counts, required fields, no duplicate IDs, no console-breaking data |

Existing scripts:

- `validate.py` gains estate-source FKs, event FKs, geometry FKs, duplicate
  names, claim-value checks, freshness warnings and coverage checks.
- `build_estates.py` reads `kek_slugs.txt` and the BAJRA table; add a curated
  overrides file so manual fixes survive a rebuild.
- `build_site_data.py` emits separate `projects.js`, `estates.js`,
  `corridors.js`, `search.js` and `stats.js`.

**Curated overrides.** `build_estates.py` currently overwrites the whole table.
Add `data/curated/estate_overrides.csv` keyed by estate ID for manual fixes
(coordinates, status, sector, website). The build applies overrides after the
source parse. Same pattern for transport rows if extraction is re-run.

### 4.4 Verification rules

1. A status change needs an official source, or two independent sources.
2. Every row has at least one source and a `last_verified` date.
3. Every status row has a `status_basis` that states the evidence, not the
   status word.
4. Every numeric claim (length, investment, capacity, progress) has a
   `project_sources` claim or a note explaining why it is missing.
5. Conflicting figures go in `notes` with both values and both sources. Never
   silently choose one.
6. A row not re-checked within six months is flagged `stale` in the Data view.
7. Coordinates use the best available precision; `regency` is a fallback, not a
   default.
8. Operating and recently completed rows have an `opened_year`, and an
   `opened_date` when the source gives one.
9. One map entity per asset. Phase 2 of a port is an event on the asset, not a
   duplicate row, unless it has a separate legal project and status.
10. Do not add a row just to increase coverage. An honest gap is better than a
    guessed row.

**Status rule for phased assets**

- `operating`: fully open, no material construction active.
- `recently_completed`: fully open on or after 2024-11-06.
- `under_construction`: any material construction active, even if another
  phase is open. Note the open phase and its length/capacity.
- `planned`: designated or contracted, no physical construction.
- `stalled`: officially delayed or reported stalled.

---

## 5. Data backlog

### 5.1 Coverage targets

| Layer | Now | Target | Gap | Source of truth |
|---|---:|---:|---:|---|
| Roads | 45 | 45 target (40–50 range) | 0 | BPJT + PSN + three planned Trans Sumatra concessions |
| Railways | 13 | 13 PSN | 0 | Kemenhub deck |
| Airports | 7 | 7 PSN | 0 | Kemenhub deck |
| Seaports | 15 | 15 PSN | 0 | Kemenhub deck |
| Transport PSN (all modes) | 35 | 35 | 0 | Kemenhub deck |
| Factories | 27 | 25 target (20–30 range) | 0 | PSN + Rp 1T; frozen universe in `data/derived/factories_2026.csv` |
| Industrial estates | 160 | 179 | 19 | Kemenperin 2026; gap ledger in `data/derived/estate_gap_2026.csv` |
| SEZs | 25 | 25 | 0 | KEK National Council |
| Unique estates | 178 | ~197 | ~19 | Dedupe 179 + 25 − 7 |
| Estate coordinates | 45 official/OSM of 178 | 178 verified | 133 regency | KEK profiles, OpenStreetMap/Nominatim |
| Corridors | 5 | 5 with totals | 0 | Hutama Karya, BPJT, Bina Marga, Wikipedia revisions |
| Corridor progress series | 3 | 5 | 2 | Sumatra, Java and Papua only; Sulawesi and Kalimantan are route-total-only |
| Corridor segments | 44 | 5 corridors | 2 corridors | 13 Sumatra, 23 Java, 8 Papua; no section list for Sulawesi or Kalimantan |
| Sources | 89 | 80–100 | 0 | In range; 35 official, 31 secondary, 23 company |

### 5.2 Transport PSN: the 35 projects

The Kemenhub deck (19 Feb 2026) is the authoritative list: 7 airports, 15
seaports, 13 railway projects. The deck's summary says 29 are complete/operating
and 6 are under construction. The curated batch uses the atlas definitions and
the deck's project pages: 24 operating, 1 recently completed (Benoa expansion),
6 under construction and 4 planned. The differences are itemised in
`docs/phase-2-transport.md`. This is the single biggest data win and is now in
the curated tables.

**Airports (7)**

| Project | Location | Status | Opened |
|---|---|---|---|
| Yogyakarta International Airport | Kulon Progo, DI Yogyakarta | operating | 2020 |
| Komodo Airport, Labuan Bajo | Manggarai, NTT | operating | 2022 |
| Lombok Praya Airport | Lombok Tengah, NTB | operating | 2020 |
| Nabire New Airport | Nabire, Central Papua | operating | 2022 |
| Siboru Fakfak Airport | Fakfak, West Papua | operating | 2023 |
| Kediri Airport | Kediri, East Java | operating | 2023 |
| Raja Haji Abdullah Airport | Karimun, Riau Islands | operating | 2023 |

**Seaports (15)**

| Project | Location | Status | Opened/notes |
|---|---|---|---|
| KEK Maloy Port | Kutai Timur, East Kalimantan | operating | 2020 |
| Labuan Bajo Multipurpose Terminal | Manggarai Barat, NTT | operating | 2021 |
| Bitung International Hub Port | Bitung, North Sulawesi | operating | 2018 |
| Kupang Port | Kupang, NTT | operating | 2018 |
| Kuala Tanjung International Hub Port | Batu Bara, North Sumatra | operating | 2018 |
| Kijing Terminal | Mempawah, West Kalimantan | operating | 2022 |
| Sanur Port | Denpasar, Bali | operating | 2022 |
| Likupang Port | Minahasa Utara, North Sulawesi | operating | 2022 |
| Makassar New Port | Makassar, South Sulawesi | operating | 2023 |
| Teluk Palu Port | Palu, Central Sulawesi | operating | 2023 |
| Sorong Port | Sorong, Southwest Papua | operating | 2023 |
| Patimban Port | Subang, West Java | under_construction | Phase 1 operating; phase 2 packages 5–6 at 93–95% in late 2025 |
| Benoa Port (BMTH) | Denpasar, Bali | recently_completed | Expansion reported 100% in 2025; verify opening date |
| New Palembang Port | Banyuasin, South Sumatra | planned | Land grant 31 Oct 2025; no physical work |
| Muaro Jambi Container Terminal | Muaro Jambi, Jambi | planned | Contract 17 Dec 2025; no physical work |

**Railways (13)**

| Project | Location | Status | Opened/target |
|---|---|---|---|
| LRT South Sumatra | Palembang, South Sumatra | operating | 2018 |
| Double Track Java South | West/Central/East Java, DIY | under_construction | Segments open; Sepanjang–Wonokromo and land remaining |
| Tebing Tinggi–Kuala Tanjung Railway | North Sumatra | operating | 2022 |
| Yogyakarta Airport Rail | DI Yogyakarta | operating | 2021 |
| Makassar–Parepare Railway | South Sulawesi | operating | 2023; Mandai–Palanro reported 95.91% |
| Jabodebek LRT | Jabodetabek | operating | 2023 |
| Jakarta–Bandung High-Speed Rail | DKI Jakarta, West Java | operating | 2023 |
| Rantau Prapat–Kota Pinang Railway | North Sumatra | under_construction | Pondok S5 reached 2024; Kota Pinang remaining |
| Lahat–Kertapati Logistics Railway | South Sumatra | under_construction | Double track operating; coal terminal 33.65% |
| East Kalimantan Logistics Railway | Balikpapan, East Kalimantan | planned | 2028 target; feasibility study |
| MRT Jakarta North–South | DKI Jakarta | under_construction | Phase 2A 55.89%; 2028/2030 target |
| MRT Jakarta East–West | DKI Jakarta | planned | 2032 target; no physical work |
| LRT Jakarta Velodrome–Manggarai | DKI Jakarta | under_construction | 89.22% physical; 2026 target |

**Tasks**

| ID | Task | Acceptance |
|---|---|---|
| T1 | Extract the 35 rows into `data/derived/transport_psn.csv` with a parser or a checked manual table | 35 rows, sector counts 13/7/15, every row has a Kemenhub source and page reference |
| T2 | Curate the 13 railway rows | Each has status, location, coordinates, operator, opened/target year, length where applicable, at least one claim |
| T3 | Curate the 7 airport rows | Each has IATA/ICAO if available, capacity, opened year, operator, coordinates |
| T4 | Curate the 15 seaport rows | Each has port type, capacity (TEU or tonnes), opened year, operator, coordinates |
| T5 | Enrich investment, capacity, operators and aliases | Investment from the deck or an official source; capacity only when stated; operators added to `organizations.csv` |
| T6 | Add sources and claims | Every row has a `project_sources` claim for status and for each numeric figure; conflicts in notes |
| T7 | Validate and rebuild | `validate.py` passes; site payload contains every curated project; filters return correct counts |
| T8 | Coverage check | 35/35 represented; any exclusion documented in the Data view |

### 5.3 Factories

Universe: PSN industrial projects plus private plants with investment of at
least Rp 1T, operating or under construction. Exclude estates (they are a
separate table) and pure mining pits.

Candidate list to research:

| Candidate | Location | Why |
|---|---|---|
| Freeport Indonesia copper smelter, Manyar | Gresik, East Java | PSN, about US$3B, 1.7 Mtpa concentrate |
| Amman Mineral copper smelter | Sumbawa, NTB | PSN, about US$2.1B, cathode capacity |
| Huadi nickel-alloy smelter | Bantaeng, South Sulawesi | Operating nickel chain |
| Weda Bay Nickel | Central Halmahera, North Maluku | Large nickel estate and smelter |
| Obi Island nickel | South Halmahera, North Maluku | Operating nickel chain |
| IMIP Morowali | Morowali, Central Sulawesi | Estate plus multiple smelters |
| Konawe Industrial Park | Konawe, Southeast Sulawesi | Operating nickel chain |
| IWIP Teluk Weda | Central Halmahera, North Maluku | Estate plus smelters |
| KIPI Bulungan | Bulungan, North Kalimantan | Under construction, green industrial park |
| Mempawah alumina refinery | Mempawah, West Kalimantan | Under construction, bauxite/alumina |
| Inalum aluminium smelter expansion | Kuala Tanjung, North Sumatra | State aluminium expansion |
| GEM steel plant | Kendal, Central Java | Large steel investment |
| Battery-chain plants | Karawang and others | CATL/Hailiang announcements; verify status |

Tasks:

| ID | Task | Acceptance |
|---|---|---|
| F1 | Freeze the factory universe and candidate list | 20–30 named plants with a source for inclusion; exclusions documented |
| F2 | Curate factory rows | Sector `factory`, subsector (`smelter`, `steel`, `alumina`, `battery`, `cement`, `petrochemical`), capacity, investment, status, coordinates |
| F3 | Add organisations and investments | Operator/parent/sponsor rows; investment rows with amount, currency, `amount_idr_t`, stage and source |
| F4 | Site integration | Factory filter and markers work; detail shows capacity and investment |
| F5 | Coverage check | 20–30 rows; every row has investment or capacity; every status has a source |

### 5.4 Industrial estates and SEZs

Tasks:

| ID | Task | Acceptance |
|---|---|---|
| E1 | Reconcile 179 vs 160 | A gap list of 19 names, each marked added, duplicate, out of scope or unresolved with a reason |
| E2 | Add the nine 2025 estates | IPIP, I-Sentra Lamongan, Huadi Bantaeng, Cikembar II, Losarang, Purwakarta Integrated Industrial Park, Pulau Penebang, Seafer, Tembesi — each with area, developer, province/regency, coordinates and a source |
| E3 | Exact coordinates | All 25 SEZs plus the 40 largest industrial estates get official/OSM points or boundaries; `precision=exact` or `approximate`; regency remains the fallback |
| E4 | Attributes and status | Sector focus, website, legal basis, established year and verified status for the top 100 estates; status no longer a blanket `operating` |
| E5 | Estates table view | Summary, filters, sortable table, row detail, CSV download; works at 390 px |
| E6 | Optional map layer | Toggle off by default; clusters; estate detail links to nearby projects; only after E3 |

**Known conflicts to resolve**

- Kemenperin lists IPIP under Central Sulawesi; PT IPIP's Pomalaa project is in
  Southeast Sulawesi. There may be two different projects.
- Tembesi is listed under West Kalimantan, but the well-known Tembesi estate is
  in Batam. Verify before adding.
- Kemenperin's 179 count and the 160-row table may use different definitions
  (operational vs permitted, or include new 2025 estates).

### 5.5 Roads and corridors

Tasks:

| ID | Task | Acceptance |
|---|---|---|
| R1 | Audit PSN toll roads against the current 27 | Missing PSN corridors added; every PSN row has `psn=yes` and a legal basis |
| R2 | Add operating context rows | Trans Java and major open Trans Sumatra sections added as operating context without duplicating under-construction corridors |
| R3 | Build `corridor_segments.csv` | Section tables where a published list exists: 13 Sumatra, 23 Java, 8 Papua (44 rows); Sulawesi and Kalimantan documented as route-total-only |
| R4 | Recent openings and stalled rows | Six exact-dated events recorded; month-end approximations rejected; remaining openings stay in project notes |
| R5 | Corridor UI v2 | Segment table, four-part stacked bar, grouped timeline, coverage states and definitions |
| R6 | Geometry for major corridors | Simplified lines for 10 major corridors from OSM or official maps; `project_geometry.csv`; attribution recorded — **deferred, documented gap** |

**Track 2D outcome**

- Roads: **45 / 45** target corridors. 42 earlier corridors plus three planned
  0-km Trans Sumatra concessions: Lhokseumawe–Sigli (157 km), Langsa–Lhokseumawe
  (135 km) and Muara Enim–Lubuk Linggau (114.5 km).
- Corridors: **5 / 5** with a kilometre total. Trans Java joins Sumatra, Papua,
  Sulawesi and Kalimantan.
- Segments: **44** rows. Trans Java reconciles exactly to 1,232.80 km; Trans
  Sumatra covers 1,667.31 km of 2,854 km and Trans Papua 2,345.40 km of 4,330 km.
- Events: **6** exact-dated rows, from the 2018 East Java openings to the
  2026 Gending–Paiton opening and the GNI PKPU.
- Data pages: corridor segments and events CSVs are downloadable; coverage layer
  renamed `corridors_with_total` and met 5/5.
- R6 geometry remains empty. The atlas still shows points, not lines.

**Known recent openings**

Four candidate openings from the earlier backlog did not meet the exact-date
rule and were not added as events: Binjai–Langsa Section 3 (March 2025),
Padang–Sicincin (May 2025), Solo–Yogyakarta Klaten–Prambanan (July 2025) and
Probolinggo–Banyuwangi Sections 1–2 (2026). The 7 September 2026 Gending–Paiton
opening is recorded because the BPJT decree gives an exact date. Add the others
when an exact date is found.

### 5.6 Coverage and reconciliation

- `data/curated/coverage_targets.csv` records the universe and target for every
  layer.
- `scripts/build_coverage.py` writes `data/coverage.csv` and site stats.
- The Data view shows current/target/gap and the last verified date.
- Any layer below 80% of target is labelled **partial** in the UI.
- A monthly refresh checks the gap list first, then freshness.

---

## 6. Engineering workstream

### 6.1 Front-end structure

The site must keep working from `file://`. That rules out ES modules and
`fetch`. Use classic scripts and a single global namespace.

```
site/
├─ index.html                 shell, SVG sprite and mount points
├─ assets/
│  ├─ fonts.css               local @font-face rules
│  ├─ fonts/                  Inter and Source Serif 4 WOFF2 files
│  ├─ tokens.css              design tokens
│  ├─ app.css                 layout and components
│  ├─ constants.js            status, sector and vocabulary data
│  ├─ app.js                  boot, routing, state, views and drawer
│  └─ map.js                  Leaflet setup, basemap, markers, clusters
├─ data/
│  ├─ projects.js             window.PROJECTS, with per-row sources
│  ├─ estates.js              window.INFRA_ESTATES (lazy)
│  ├─ corridors.js            window.CORRIDORS
│  ├─ stats.js                window.INFRA_STATS: counts, coverage, sources
│  ├─ search.js               window.INFRA_SEARCH
│  └─ basemap.js              window.BASEMAP
└─ vendor/
   ├─ leaflet/                Leaflet 1.9.4
   └─ markercluster/          vendored Leaflet.markercluster 1.5.3
```

- `index.html` loads tokens, app CSS, Leaflet, markercluster, data scripts and
  then the app scripts in order. No bundler, no build step to view.
- Data files write one global each: `window.PROJECTS`, `window.CORRIDORS`,
  `window.INFRA_STATS`, `window.INFRA_SEARCH`, and lazily
  `window.INFRA_ESTATES`.
- Estate data loads by injecting a `<script src="data/estates.js">` when the
  Estates tab is first opened. Works from `file://`.
- The SVG sprite is inline in `index.html` so `<use href="#i-road">` works from
  `file://` without an external SVG fetch.
- Vendor markercluster with its licence.

### 6.2 Build and validation

- `scripts/build_all.py` runs: validate → build projects → build estates →
  build factories → build events → build coverage → build site data → check
  site. CI uses it.
- `scripts/validate.py` v3 checks:
  - all existing checks;
  - estate source FKs and event FKs;
  - duplicate estate names with different IDs (warn, do not fail);
  - `opened_year` required for operating/recently completed;
  - `expected_open_year` for planned/under construction (warn if missing);
  - coordinates inside the province's rough bounding box (best effort);
  - claims exist for status and for each numeric field;
  - stale rows (> 6 months) reported, not failed;
  - coverage targets present for every layer.
- `scripts/check_site.py` asserts:
  - payload counts match the flat exports;
  - every project has an ID, name, sector, status, coordinates, source;
  - no duplicate IDs across projects and estates;
  - the search index has an entry per project and estate;
  - stats counts sum to the payload counts.
- Unit tests for parsers (area, dates, slugs, status mapping) with `unittest`.
  No heavy test framework needed.

### 6.4 Documentation

- `README.md` stays the front door: current counts, how to run, schema, sources,
  limitations, where to pick up.
- `plan-v3.md` is the backlog.
- `CHANGELOG.md` records dated additions and corrections.
- `docs/sources.md`? Keep the source register in `data/curated/sources.csv` and
  render it on the Data page; do not duplicate it in prose.
- Every phase updates README counts and the Data view.
- Every schema change updates `scripts/data_model.py`, `validate.py` and the
  README data-model table in the same commit.

---

## 7. Three-phase execution plan

The work is grouped into **three phases**. Each phase has parallel tracks; the
phase is the unit of delivery. Finish the exit criteria before starting the next
phase. Sizes: **S** = one focused session, **M** = 2–3 sessions, **L** = 4–6
sessions.

### Phase 1 — Foundation and experience

**Status: complete, 7 November 2026.** See the completion log after the exit
criteria.

**Goal:** the current 27 rows look and behave like a published product. The
shell, four views, search, filters, detail drawer, map and mobile sheet are
ready. No new data rows in this phase.

**Track 1A — Decisions and guardrails**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| D1 | Confirm the design direction | One-page decision: editorial atlas, tokens, typography, reference set | S | — |
| D2 | Freeze the universe | `coverage_targets.csv` with every layer, target and source; exclusions written down | S | — |
| D3 | Freeze schema v3 | New tables and fields agreed; `data_model.py` updated; migration notes | S | D2 |
| D4 | Set budgets | Accessibility, performance and payload budgets written into this plan | S | D1 |
| D5 | Set up tracking | This file's checklist becomes the single source of work status | S | — |

**Track 1B — Shell and design**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| U1 | Tokens, fonts, icons | `tokens.css`, local WOFF2 fonts, SVG sprite; a style specimen page or section | M | D1 |
| U2 | App shell | Top bar, 380 px sidebar, map region, tab strip, responsive grid; no data changes | M | U1 |
| U3 | Tabs and routing | Explore/Corridors/Estates/Data; hash router; deep links work from `file://` | M | U2 |
| U4 | Filters and URL state | Sector/status chips, more-filters popover, active chips, clear all, hash sync | M | U3 |
| U5 | Search, sort and list | Search index, ranked results, sort control, new row anatomy, keyboard navigation | L | U4 |
| U6 | Detail drawer | New anatomy, key figures, why-this-status, sources, notes, prev/next, share | L | U5 |
| U7 | Mobile bottom sheet | Full-viewport map, three snap points, filter sheet, detail sheet | L | U6 |
| U8 | States and accessibility | Empty/loading/error states, focus trap, skip link, contrast, reduced motion | M | U7 |
| U9 | Data view skeleton | Coverage, definitions, sources, downloads, changelog; generated counts | M | U3 |
| U10 | Copy pass | Remove stale toll-road copy; data-driven dates and counts; metadata | S | U9 |

**Track 1C — Map experience**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| M1 | Basemap v2 | Province boundaries, lakes, rivers, urban areas, 30 cities; under 150 KB gzipped | M | U2 |
| M2 | Marker system | Sector glyphs, status fill, selected ring and label, hover tooltip | M | M1 |
| M3 | Clustering | Clusters below zoom 7 with status donut; expands smoothly | M | M2 |
| M4 | Interaction sync | List ↔ map selection, drawer offset, keyboard, reduced motion | M | M3 |
| M5 | Controls and legend | Zoom, scale, reset, layer control, collapsible legend, compact attribution | S | M2 |
| M6 | Layer manager | Projects on; estates off; corridor geometry; lazy estate load | M | M3 |
| M7 | Performance and offline QA | 300 markers at 60 fps; `file://` and localhost; no network requests | M | M6 |

**Exit criteria**

- Decisions recorded; `coverage_targets.csv` exists; schema v3 agreed.
- Four views exist and hash routing works from `file://`.
- Search, filters, sort and URL state work with the 27 existing rows.
- The detail drawer shows evidence, sources and notes; the mobile sheet works.
- The map has the new basemap, sector markers and clusters; no network requests.
- Keyboard, focus, contrast and reduced-motion checks pass; no console errors;
  works from `file://`.
- A local preview was signed off with desktop and mobile screenshots.

**Phase 1 completion log — 7 November 2026**

| Item | Evidence |
|---|---|
| D1–D5 | `docs/phase-1-decisions.md`; `data/curated/coverage_targets.csv`; schema v3 in `data_model.py`; migration in `migrate_schema_v3.py` |
| U1 | `site/assets/tokens.css`, `fonts.css`, bundled WOFF2 files, inline SVG sprite |
| U2–U4 | Four-tab shell, hash router, sector/status chips, island/province/PSN/corridor/precision/freshness filters, URL state |
| U5 | Search, five sort modes, compact list rows, empty state, arrow-key navigation |
| U6 | Detail drawer with metrics, open share, why-this-status, evidence, every source, notes, related corridor, previous/next, share |
| U7 | Full-viewport mobile map and draggable three-snap bottom sheet; peek shows two rows |
| U8 | Focus trap, skip link, `aria-live` counts, text status labels, reduced motion, loading/error/empty states; axe-core 0 violations on four views. The Phase 1 map-marker target-size exception was fixed in Phase 2 |
| U9–U10 | Data view with coverage matrix, definitions, inclusion rules, source register, downloads, gaps, changelog; stale toll-road copy removed |
| M1–M3 | Natural Earth provinces, lakes, rivers, urban areas and city labels; sector markers; status-ring clusters |
| M4–M6 | List ↔ map selection, drawer offset, zoom/scale controls, collapsible legend, layer control, lazy estates |
| M7 | `file://` verified; no external resource hosts; shell 84.7 KB gz, initial data 93.0 KB gz, basemap 75.2 KB gz, estates 10.8 KB gz; 0.71 s load from `file://` in headless Edge |

Deviations: the estates table shipped early (it was already in the curated
tables); no preview deployment was made; the formal Lighthouse/axe audit and the
300-marker performance test move to Phase 2. See
`docs/phase-1-decisions.md`.

### Phase 2 — Data completion

**Status: complete except Track 2B (estates) and R6 geometry, 8 November 2026.
Track 2A complete; Track 2B partial; Track 2C complete; Track 2D complete except
R6.** See
`docs/phase-2-transport.md` for the extraction, status mapping and conflicts,
`docs/phase-2-estates.md` for the 19-name gap ledger and coordinate work,
`docs/phase-2-factories.md` for the factory universe, and
`docs/phase-2-roads.md` for the BPJT additions.

**Goal:** every layer meets its coverage target or has a documented gap. This
phase adds the views that consume the new data: the corridor segment view and
the refined estate attributes. The estate table itself shipped in Phase 1.

**Track 2A — Transport PSN**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| T1 | Extraction | 35 staging rows with page references | M | D3 |
| T2 | Railways | 13 curated rows with status, location, coordinates, operators, years | L | T1 |
| T3 | Airports | 7 curated rows with capacity, opened year, operator, coordinates | M | T1 |
| T4 | Seaports | 15 curated rows with port type, capacity, opened year, operator | L | T1 |
| T5 | Enrichment | Investment, capacity, aliases, organisations | M | T2–T4 |
| T6 | Sources and claims | Every row has status and numeric claims; conflicts recorded | M | T5 |
| T7 | Build and QA | Validation passes; every curated project in the payload; filters and map correct | M | T6 |
| T8 | Coverage check | 35/35 represented; exclusions documented | S | T7 |

**Track 2A completion log — 7 November 2026**

| Item | Evidence |
|---|---|
| T1 | `scripts/extract_transport_psn.py` → `data/derived/transport_psn.csv`, 35 checked rows with page references |
| T2–T4 | 13 railways, 7 airports and 15 seaports in `data/curated/projects.csv`; status, location, coordinates, operators and years |
| T5 | 13 new organisations, sponsor/owner/operator links, 67 aliases, investment for 14 rows |
| T6 | 145 project claims; conflicts recorded in `notes` and `docs/phase-2-transport.md` |
| T7 | `validate.py` passes; site rebuilt; filters show 13 rail, 7 air, 15 sea |
| T8 | Coverage 35/35; transport PSN row added to `coverage_targets.csv`; gaps for rail length, capacity and approximate coordinates documented |

**Track 2B — Estates**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| E1 | Reconcile 179 | 19-name gap list with a disposition per name | M | D2 |
| E2 | Add 2025 estates | Nine rows with area, developer, location, coordinates, source | L | E1 |
| E3 | Exact coordinates | 25 SEZs + 40 largest estates at exact/approximate precision | L | E2 |
| E4 | Attributes and status | Top 100 estates have sector, website, legal basis, verified status | L | E3 |
| E5 | Estates table | Summary, filters, sortable table, row detail, CSV, mobile layout — **shipped in Phase 1** | M | E4 |
| E6 | Optional map layer | Off by default; clusters; nearby projects; works offline | M | E5 |

**Track 2B status — 8 November 2026**

| Item | Status | Evidence |
|---|---|---|
| E1 | Done | `data/derived/estate_gap_2026.csv`: 9 named + 10 unidentified, with dispositions |
| E2 | Blocked | Kemenperin list HTTP 502 and `satudata` DNS failure; nine named additions lack area/location sources |
| E3 | Partial | 25 SEZs official, 20 of the 40 largest industrial estates OSM/Nominatim, 133 regency centroids |
| E4 | Not started | 160 industrial estates still `operating` from the 2024 table; attributes mostly blank |
| E5 | Shipped | Table with 178 rows, detail, filters, CSV, gap-ledger download |
| E6 | Deferred | Coordinate coverage is not enough to justify a map layer |

See `docs/phase-2-estates.md`.

**Track 2C — Factories**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| F1 | Universe | 20–30 candidates with inclusion sources | M | D2 |
| F2 | Rows | Status, capacity, investment, operator, coordinates, sources | L | F1 |
| F3 | Organisations and investments | Normalised org and investment rows | M | F2 |
| F4 | Site integration | Factory filter, markers, detail figures | M | F2 |
| F5 | Coverage check | 20–30 rows; every row has investment or capacity | S | F4 |

**Track 2C status — 8 November 2026**

| Item | Status | Evidence |
|---|---|---|
| F1 | Done | 27 plants frozen against the 20–30 target; inclusion/exclusion log in `docs/phase-2-factories.md` |
| F2 | Done | 27 rows with status, capacity, approximate coordinates, status basis and notes; 18 with investment |
| F3 | Done | 26 organisations and 18 investment rows; USD converted at Rp 16,500/USD for ranking |
| F4 | Done | Factory sector filter, map glyph, clustering and drawer metrics; Data view copy updated |
| F5 | Met | 27/25 coverage; all 27 have capacity; 17 official, 8 dual, 2 single-source |

See `docs/phase-2-factories.md` and the frozen ledger
`data/derived/factories_2026.csv`.

**Track 2D — Roads and corridors**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| R1 | PSN road audit | Missing PSN toll corridors added or documented | M | D2 |
| R2 | Operating context | Trans Java and major open Trans Sumatra sections | M | R1 |
| R3 | Segment table | Section tables for corridors with a published list; route totals only for the rest | L | R2 |
| R4 | Events | Exact-dated openings and stalled events recorded; no month-end approximations | M | R3 |
| R5 | Corridor UI v2 | Segment table, timeline, stacked bar, gap states | M | R3 |
| R6 | Geometry | Simplified lines for 10 major corridors with attribution | L | R5 |

**Track 2D status — 8 November 2026**

| Item | Status | Evidence |
|---|---|---|
| R1 | Done for PSN toll roads | 15 missing PSN corridors added from the BPJT snapshot; three planned Trans Sumatra concessions added; roads 45/45 |
| R2 | Done | Trans Java defined as the fifth corridor; Sumatra, Java and the 15 PSN corridors linked; planned 0-km concessions linked to Trans Sumatra |
| R3 | Done, partial by source | `corridor_segments.csv` has 44 rows: 13 Sumatra, 23 Java, 8 Papua; Java sums to 1,232.80 km; Sulawesi and Kalimantan have no published section list |
| R4 | Done, thin | Six exact-dated events: 2018 East Java openings, 2024 Betung–Jambi, 2025 Lotte LINE, 2026 GNI PKPU, 2026 Gending–Paiton, 2023 LRT Jakarta groundbreaking |
| R5 | Done | Corridor cards v2 with four-part bar, legend, coverage state, segment table, grouped timeline and series-coverage section; project drawer timeline |
| R6 | Deferred | `project_geometry.csv` still empty; recorded as a Phase 3/refresh gap, not a blocker |

See `docs/phase-2-roads.md`.

**Track 2D completion log — 8 November 2026**

| Item | Evidence |
|---|---|
| Roads | 45/45 target corridors; 10 operating, 25 under construction, 10 planned |
| Corridors | 5 rows: Trans Sumatra, Trans Java, Trans Sulawesi, Trans Kalimantan, Trans Papua |
| Segments | 44 rows: 13 Sumatra, 23 Java, 8 Papua; Java reconciles to 1,232.80 km |
| Events | 6 exact-dated rows in `project_events.csv` |
| Site | `corridors-segments.csv` and `events.csv` downloads; corridor cards v2; project and corridor timelines |
| Validation | `OK: 107 projects, 178 estates, 70 organisations, 89 sources, 5 corridors, 44 segments, 6 events, 0 geometry, 18 investments` |
| Offline QA | `file://` loads 5 cards, 23 Java segment rows, 2 timeline years and 8 downloads; 0 external requests; 0 console errors |
| Accessibility | axe-core 4.10.3, WCAG A/AA: 0 violations on Explore and Corridors at 1440 px and 390 px |
| Deferred | R6 geometry; the atlas still shows points, not lines |

**Exit criteria**

- 35/35 transport PSN; 107 projects in the flat export.
- 178 unique estates: 25 SEZs, 160 industrial-estate designations and 7 shared
  zones. The 19-name gap list is resolved or explained; the blanket `operating`
  status is documented as unverified rather than presented as verified.
- 27 factories, each with capacity and at least one source; investment where a
  dated figure exists (18 of 27).
- 45 road corridors; five corridor totals; three progress series; 44 segments and
  six exact-dated events; Trans Sulawesi and Trans Kalimantan are explicitly
  route-total-only.
- Every row has coordinates, a source and a verification date; validation
  passes; the coverage report shows current/target/gap for every layer.
- R6 geometry is a documented gap, not a claimed feature.

### Phase 3 — Trust and local release

**Goal:** the site is verifiable, maintainable and locally releasable by another
agent. It is **not** pushed to GitHub or published in this phase.

**Status: complete, 8 November 2026.** The build has 107 projects, 178 estates,
479 atomic project claims (107/107 fully claimed), 19 conflicts (11 resolved, 8
open), 285 freshness rows and 189 dictionary fields. `build_all.py --check`
leaves 25 generated files unchanged; `smoke_site.py` passes on `file://` and a
local HTTP server with no external request and no console error. Evidence:
[`docs/phase-3-trust.md`](docs/phase-3-trust.md).

**Track 3A — Trust layer**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| Q1 | Per-fact claims | Status and numeric claims traced to sources | M | T6, F3 |
| Q2 | Freshness | Stale report, UI badge, monthly refresh list | M | Q1 |
| Q3 | Data page v2 | Coverage matrix, methodology, source register, gaps, changelog | M | U9, Q2 |
| Q4 | Downloads | Filtered CSV and GeoJSON, data dictionary | S | Q3 |
| Q5 | Conflict register | Known conflicts listed with both values and sources | S | Q3 |

**Track 3B — Local release and hand-off**

| ID | Item | Outcome / acceptance | Size | Depends |
|---|---|---|---|---|
| S1 | Build all + local CI | `build_all.py`, validation, deterministic rebuild and a diff check; no remote, no push | M | Q3 |
| S2 | Local release build | `site/` loads from `file://` and a local HTTP server; relative paths; no CDN or tile requests | S | S1 |
| S3 | Smoke tests | Desktop/mobile screenshots, keyboard, `file://`, no network requests | M | S2 |
| S4 | Refresh runbook | Monthly steps: fetch, diff, review, update, rebuild, verify locally | S | S2 |
| S5 | Hand-off | README, changelog and this plan current; open gaps listed | S | S4 |

**Exit criteria**

- Every status and numeric claim traces to a source.
- Stale rows are flagged and the monthly refresh runbook exists.
- The Data view has coverage, methodology, sources, downloads and conflicts.
- CI validates, rebuilds and checks for drift.
- Desktop, mobile, keyboard and offline smoke tests pass.
- **No GitHub remote, push, Pages deployment or public release is performed.**
- README, changelog and this plan agree with the data.

**Completion evidence:** Q1 `data/derived/claims_audit.csv` (107/107);
Q2 `data/derived/freshness_report.csv` (285 fresh, next due 2027-05-08); Q3 Data
view v2 and `docs/evidence/phase-3/04-data-desktop.png`; Q4 browser-tested
filtered CSV/GeoJSON and dictionary; Q5 `data/curated/conflicts.csv` (19 rows);
S1 `build_all.py --check` (25 files unchanged); S2 `file://` and local HTTP;
S3 `docs/evidence/phase-3/smoke-report.json` (0 external requests, 0 errors);
S4 `docs/refresh-runbook.md`; S5 README, `CHANGELOG.md`, `plan.md` and this plan.

---

## 8. Delivery order and milestones

**Milestone A — end of Phase 1: local preview (complete 7 Nov 2026)**

Order:

1. D1–D5 — decisions, coverage targets, schema, budgets.
2. U1 — tokens, fonts, icons.
3. U2–U3 — shell, tabs, hash routing.
4. U4–U5 — filters, search, sort, list.
5. U6 — detail drawer.
6. M1–M3 — basemap, markers, clustering.
7. U7–U8 — mobile and accessibility.
8. U9–U10 — Data view skeleton and copy pass.
9. M4–M7 — interaction, controls, layers, performance.

**Milestone B — end of Phase 2: dataset complete for the attainable scope
(8 Nov 2026)**

Order:

1. T1–T8 — transport PSN. This is the largest visible win and the data is
   already extracted.
2. E1–E5 — estate reconciliation, coordinates, table view. E2 is blocked and E4
   is partial; the gap ledger and the blanket-status caveat are documented.
3. F1–F5 — factory universe and rows.
4. R1–R5 — road audit, operating context, segments, events, corridor UI.
5. E6 and R6 — optional map layers and geometry. Both are deferred and recorded
   as gaps.

**Milestone C — end of Phase 3: local release (complete 8 Nov 2026)**

Order:

1. Q1–Q5 — claims, freshness, Data view, downloads, conflicts.
2. S1–S5 — local CI, release build, smoke tests, runbook and hand-off.
3. Stop. Do not push to GitHub, create a remote or publish the site.

---

## 9. Risks and constraints

| Risk | Impact | Mitigation |
|---|---|---|
| Kemenperin `satudata` does not resolve | Official estate list unavailable | Use the 2024 mirror, document the gap, retry monthly, ask for a snapshot |
| KPPIP and KEK pages change | Broken sources | Snapshot every fetch under `data/raw/YYYY-MM-DD/`; archive paths in `sources.csv` |
| Conflicting definitions (Trans Sulawesi, Trans Kalimantan) | False precision | Publish segment data and gap notes; never invent an aggregate |
| Estate coordinates are coarse | Misleading map | Keep estates off the map until E3; show `precision` in the table |
| Scope creep | Nothing ships | Freeze the universe in D2; add candidates to a backlog, not to the current batch |
| `file://` restrictions | Broken page | Classic scripts, hash routing, local JS payloads; test from `file://` every phase |
| Single-file site becomes unmaintainable | Slow changes | Split into local CSS/JS files in Phase 1 |
| Marker overload | Unusable map | Cluster below zoom 7; lazy estate layer; sector filters |
| Data verification is slower than extraction | Stale or wrong rows | Status rule: official or two independent sources; one batch at a time |
| Font licensing | Redistribution problem | Use OFL fonts, include licence files, subset to needed glyphs |
| OSM geometry licence | Attribution obligation | Record ODbL attribution in the Data view and map credits |
| A stray `six.py` in the shared temp directory breaks pandas | Build failures | Avoid the shared temp directory for scripts; use BeautifulSoup/csv or a clean venv |

---

## 10. Decisions confirmed

All Phase 1 decisions are closed in `docs/phase-1-decisions.md`.

1. **Design direction:** editorial atlas with bundled serif/sans. **Confirmed.**
2. **Fonts:** two OFL families bundled locally (Inter, Source Serif 4).
   **Confirmed.**
3. **Estates on the map:** table-only until E3, then an off-by-default layer.
   **Confirmed.**
4. **Factory scope:** PSN + private investment ≥ Rp 1T, 20–30 plants.
   **Confirmed.**
5. **Publishing:** no GitHub remote, push, Pages deployment or public release.
   **Deferred by the repository owner on 7 November 2026.**
6. **Dark mode:** skip for v3. **Confirmed.**

---

## 11. Definition of done

A row is done when it has:

- a stable ID, a name, a sector and a status;
- a `status_basis` with a date and a source;
- a province, a route/location and coordinates with a precision;
- at least one source claim, and a second source for any non-official status;
- the required numeric fields for its sector (length for linear assets,
  capacity or investment for nodes);
- notes for every conflict;
- `last_verified` within six months.

A view is done when:

- it has an empty state, a loading state and an error state;
- it works at 390 px and 1440 px;
- it is keyboard operable and screen-reader sensible;
- its counts are generated, not typed;
- it makes no network request;
- it has a screenshot in the phase log.
