# Indonesia Infrastructure Atlas — V4 Plan

**Status:** V4 foundation, the 2026 flagship batch, the PSN road backlog, the
24-programme layer, the first PSN industrial-area batch and the register-only
closure of PSN coverage landed on 9 November 2026. The released site is still the
v3 build: 107 projects, 178 estates and SEZs, 5 corridors, 44 segments, 479 atomic
claims and 91 sources. The repository now has 251 projects, 24 programmes, 204
estates and SEZs, 5 corridors, 44 segments, 917 project claims plus 115 estate
claims and 48 programme claims, 8 PKPN programmes with 27 claims, 14 indicators,
4 indicator values, 9 project phases, 138 sources and 34 events, with a
deterministic local build and a browser smoke test. It includes the official Permenko 16/2025
register (226 active projects and 24 active programmes) and a reconciliation
ledger showing **226 of 226** project or estate records represented: 94 to 88
reviewed project rows, 26 to reviewed estates, 88 new register-only project rows
and 18 new register-only industrial areas, with all 24 programmes matched, 24
flagship records and all 50 PSN road entries. Every PSN sector is complete.
Eighty-eight projects and 18 estates are Tier C register-only records. The
bilingual shell is implemented: `site/en/`, `site/id/`, a chooser, 635 UI keys
per locale, a language switch that preserves the current view, and full-width
register pages. The schema v4 translation, indicator and phase layers are in.
Map v3, project pages, company-profile expansion to 300 and editorial review of
the generated summaries are still open.

**Supersedes:** the roadmap, scope and "where to pick up" sections of
[`plan-v3.md`](plan-v3.md). The v1–v3 history, phase records and decisions stay
in this repository and in git history.

**Release constraint:** do **not** push this repository to GitHub, add a remote,
deploy GitHub Pages or publish the site until the repository owner asks for it
explicitly. V4 remains a local release that works from `file://` and a local
HTTP server.

**Research date:** 8 November 2026. Figures in this plan come from official
Indonesian government releases, the KPPIP project pages, the KEK Secretariat,
the 2026 and 2027 budget speeches, Wikipedia (as a discovery index only) and
the current build's own data. Every imported fact still needs its own source
and verification date; the numbers below are planning evidence, not atlas rows.

---

## Contents

1. [Executive summary](#1-executive-summary)
2. [What the research found](#2-what-the-research-found)
3. [Product vision and principles](#3-product-vision-and-principles)
4. [Information architecture](#4-information-architecture)
5. [Data expansion plan](#5-data-expansion-plan)
6. [Bilingual architecture](#6-bilingual-architecture)
7. [Design and UX plan](#7-design-and-ux-plan)
8. [Delivery plan](#8-delivery-plan)
9. [Metrics](#9-metrics)
10. [Risks and mitigations](#10-risks-and-mitigations)
11. [Immediate next actions](#11-immediate-next-actions)

Appendices: [A](#appendix-a--current-data-model-v3) ·
[B](#appendix-b--source-register-v4-starter) ·
[C](#appendix-c--research-notes) ·
[D](#appendix-d--named-backlog-starter) ·
[E](#appendix-e--v1v3-history) ·
[F](#appendix-f--open-decisions) ·
[G](#appendix-g--execution-log)

---

## 1. Executive summary

V4 turns the atlas from a **PSN project map** into a **bilingual national
delivery atlas**. It does five things:

1. **Completes the project reference set.** Reconcile the full PSN list, the eight
   national priority programmes (PKPN), IKN, the 2024–2029 flagship portfolio
   and the largest private projects, then add the missing sectors: dams and
   irrigation, water and sanitation, power generation and transmission, housing,
   health, education, digital, tourism, food and fisheries, and the sea wall.
2. **Adds the delivery layer.** New Programme, Company and Timeline views that
   answer "what is the current administration building, through whom, with what
   money, and how far along is it?" rather than only "where is this project?"
3. **Rebuilds the experience around the map.** A stronger cartographic base,
   linked list–map interaction, semantic zoom, corridor and estate layers, a
   full-width Data dashboard, and readable type and spacing.
4. **Makes English and Indonesian equal citizens.** A locale-first data model,
   externalised UI strings, two static entry points, locale-aware number, date
   and currency formatting, translation status on every field, and a build that
   fails when a UI key or required data translation is missing.
5. **Scales the editorial pipeline.** A repeatable intake process for any new
   project, factory, estate, company or programme, with source snapshots,
   atomic claims, coverage tiers and a monthly refresh.

### Headline targets

| Dimension | Today | V4 target |
|---|---:|---:|
| Project records | 251 (88 register-only) | **400+** (226 PSN + 174 strategic/private records) |
| Programmes | 24 PSN + 8 PKPN | **8 PKPN + 24 PSN programmes** plus 40–60 sub-programmes |
| Companies / organisations | 111 | **300** (top 100 complete) |
| Estates and SEZs | 204 (18 register-only) | **200+** unique records (25 KEK + 179 industrial estates + 2026 additions) |
| Corridors / segments | 5 / 44 | 5 / **100+** |
| Atomic claims | 1,107 (917 project + 115 estate + 48 programme + 27 PKPN) | **1,500+** |
| Indicators | 14 | **300+** |
| Sources | 135 | **250+** |
| UI languages | 2 (English + Indonesian) | **2** (English + Indonesian) |
| Data translation coverage | UI 100%; programmes and corridors 100%; 251 project names; 251 generated summaries; editorial summaries 0% | **100%** of names, summaries and programmes, with editorial review of generated summaries |
| Initial site payload | 1,217 KB initial / 1,753 KB data / 3,876 KB total | **< 1.5 MB initial**, < 5 MB total |

### Release shape

| Release | Theme | Main outcome |
|---|---|---|
| **4.0** | Foundation | IA, tokens, bilingual shell, schema v4, audit |
| **4.1** | PSN complete | 226 projects and 24 programmes reconciled; missing roads, dams, energy, IKN |
| **4.2** | Industry and companies | 300 organisations, 200 estates, hilirisasi, social infrastructure |
| **4.3** | Experience rebuild | New navigation, map v3, Programme/Company/Timeline views |
| **4.4** | Bilingual complete | Full Indonesian UI and data, formatting, QA |
| **4.5** | Trust and release | Claims, conflicts, freshness, accessibility, performance, docs |

Estimated effort: **19–24 person-weeks** for one experienced editor/developer,
or about 4–5 months calendar time with a second translator/reviewer. Releases
4.1 and 4.2 are data-heavy and can run in parallel with 4.3 design work.

---

## 2. What the research found

### 2.1 The current atlas is strong but narrow

At the research date (8 November 2026), the v3 build was a credible,
source-linked PSN atlas. Its strengths were real:

- 107 projects across roads, railways, airports, seaports and factories.
- 479 atomic claims, 107/107 fully claimed, 19 recorded conflicts.
- 178 estates and SEZs, 5 corridor summaries, 44 segments.
- 89 dated sources, bundled basemap, no external requests.
- A local release that works from `file://`.

But the distribution was skewed to projects that were already visible by 2024:

- 53 operating, 35 under construction, 14 planned, 4 recently completed,
  1 stalled.
- 45 roads, 13 railways, 7 airports, 15 seaports, 27 factories.
- **No dams, irrigation, water supply, sanitation, power generation,
  transmission, housing, health, education, digital, tourism, fisheries or
  programme layer.**
- **No companies view**, even though sponsors, contractors and lenders are the
  real delivery network.
- **No Indonesian UI**, and most entity names and notes are English-only.

The first V4 data increment has since added 24 projects and four new sector
classes (energy, water, urban and coastal). The programme layer now records all
24 active PSN programmes; the map, company and bilingual layers are still to
come.

### 2.2 The current administration's portfolio is much larger

The government's own reporting gives the scale V4 has to cover:

- **Permenko 16/2025** sets **226 active PSN projects and 24 active PSN
  programmes** (228 project slots with 2 deleted, 25 programme slots with 1
  deleted). The KEK Secretariat lists **25 SEZ detail pages**. The bilingual
  shell and full-width register pages are in place; map v3 and company profiles
  are not. The atlas now
  has 228 project records, represents **all 226 active PSN project or estate
  records** (88 projects and 18 industrial areas are register-only), and records
  **all 24 active programmes**; no PSN project record remains.
- The **2027 budget speech (14 August 2026)** frames eight **PKPN**: food
  sovereignty; energy and water independence; education; health; downstreaming
  and industrialisation; infrastructure; housing; and disaster resilience,
  people's economy, village development and poverty reduction.
- The **two-year delivery report (20 October 2026)** records, among other
  things: 8 commodities self-sufficient, a 5.2 million-tonne food reserve,
  62 million free-meal beneficiaries, 108 million free health checks, 265
  Sekolah Rakyat, 30,000 renovated schools, 288,180 interactive screens,
  400,000 repaired houses, 100 fishing villages, 9,000 km of irrigation,
  3,500 bridges, 2,228 km of Inpres roads, 3,000 boreholes, 26 downstreaming
  groundbreakings, Rp 3,923 trillion of investment and 5.49 million jobs.
- The **2026–2027 pipeline** is visible in specific, dated events: IKN Phase 2,
  the Nusantara airport, Masela LNG, RDMP Balikpapan, 100 GW of solar, the
  13-project downstreaming stage II, the 11-project nickel ecosystem at IWIP,
  the giant Java sea wall, five dams in July 2026, 1,151 km of regional roads,
  1,386 fishing villages, 30,000 village co-operatives, 441 RSUD, 10,000
  puskesmas, 265 Sekolah Rakyat, three million houses and the national
  car/motor programme.

**Method and limits.** The research combined (a) a code and screenshot audit of
the current site, (b) 98 Setkab releases from 2026 collected by keyword, (c) the
KPPIP PSN and road pages, (d) the KEK Secretariat sitemap and detail pages,
(e) the 2026 and 2027 budget speeches, and (f) the current curated data. KPPIP
intermittently timed out, Bappenas and the IKN Authority returned 403 to some
clients, and live web search was unavailable, so a few figures are leads rather
than confirmed rows. Every figure in the flagship table still needs a direct
source check before import.

### 2.3 Flagship inventory (planning evidence)

The table is deliberately selective. It is the seed for the V4 data backlog,
not a final dataset. "Covered" means the atlas had a related row at the research
date; "partial" means only a component was present; "missing" means no record.
The 2026 flagship batch has since added rows 1–6, 8 and 9, so the column
records the 8 November baseline, not the current state.

| # | Programme / project | Status, late 2026 | Scale | Atlas today |
|---:|---|---|---|---|
| 1 | IKN Phase 2 (core government area, legislature, judiciary, ASN housing) | Under construction | Rp 48.8T 2025–2029; 1,700–4,100 ASN moving in 2026 | Missing |
| 2 | Nusantara International Airport (IVD) | Operating / expansion | Gateway to IKN | Missing |
| 3 | Masela Abadi LNG | Under construction, groundbreaking 16 Jul 2026 | US$20.9B; 9.5 Mtpa LNG; 35,000 bpd condensate | Missing |
| 4 | RDMP Balikpapan | Inaugurated 12 Jan 2026 | Refinery upgrade; import substitution | Missing |
| 5 | 100 GW PLTS programme | Under construction; phase 1 17 GWp | 30 GW in 2026; 13 GW diesel retired; Rp 73.9T annual saving | Missing |
| 6 | Downstreaming stage II | Groundbreaking 29 Apr 2026 | Rp 116T; 5 energy, 5 mineral, 3 agriculture projects | Missing |
| 7 | IWIP nickel ecosystem | 4 commercial, 7 new | US$10.2B / Rp 180T; EV battery export | Partial (factories) |
| 8 | Giant Java sea wall | Planned; master plan | 15 segments, Banten–East Java; 15–20 years | Missing |
| 9 | Five dams | Inaugurated 10 Jul 2026 | Meninting (NTB) plus four others | Missing |
| 10 | 1,151 km regional roads | Inaugurated 2026 | National/regional road programme | Missing |
| 11 | 1,386 fishing villages | 100 built; target end-2026 | 5,000 by 2029; 1,582 modern boats from 2027 | Missing |
| 12 | 30,000 village co-operatives | 10,000 established; 3,300 optimal | Target 30,000 by end-2026 | Missing |
| 13 | 441 RSUD | Planned / construction | One capable hospital per kabupaten/kota | Missing |
| 14 | 10,000 puskesmas + 514 labs | Planned from 2027 | Rp 4B per puskesmas; finish by 2030 | Missing |
| 15 | 265 Sekolah Rakyat | 93 permanent, 182 pilot | Boarding schools for poorest deciles | Missing |
| 16 | School renovation + 288,180 IFPs | Operating | All schools by 2029 | Missing |
| 17 | Three million houses | Programme | 62,000 KPR; 400,000 repaired | Missing |
| 18 | 37 electricity projects | Inaugurated 20 Jan 2025 | 26 generators, 3.2 GW; 11 transmission packages, 18 provinces | Missing |
| 19 | Patimban Port Phase 2 | Operating / expansion | 3.75M TEU phase 1; car export gateway | Partial |
| 20 | MRT Jakarta N–S Phase 2A/2B | Under construction | Bundaran HI–Ancol; extension | Partial |
| 21 | LRT Jakarta Velodrome–Manggarai | Under construction | 6.4 km, 5 stations | Partial |
| 22 | Jakarta–Bandung HSR / Whoosh | Operating; Surabaya extension studied | 142.3 km; extension pipeline | Partial |
| 23 | North Bali International Airport | Planned | New international gateway | Missing |
| 24 | Trans Sumatra toll | Under construction | 2,854 km ultimate; 982 km operational | Partial |
| 25 | Trans Java toll | Operating | 1,232.8 km; 1,079.9 km operating | Partial |
| 26 | Trans Sulawesi / Trans Kalimantan / Trans Papua | Mixed | National road and rail corridors | Partial |
| 27 | 25 KEKs | Operating / development | 25 official SEZs | Covered |
| 28 | 179 industrial estates | Operating | 101,351 ha; 57.2% occupancy (2026) | Covered by count (204 estates; 186 industrial, 18 register-only) |
| 29 | National car / motor EV ecosystem | Construction / launch | Mass production target 2028 | Missing |
| 30 | Danantara DDMF | Operating fund | Long-term strategic projects | Missing |
| 31 | Indonesia Financial Center (PFII) | Planned | Jakarta and Bali | Missing |
| 32 | Mineral and commodity exchange | Planned 1 Jan 2027 | Indonesia Reference Price | Missing |
| 33 | Free Nutritious Meals (MBG) | Operating | 62M beneficiaries; Rp 335T 2026 | Missing (programme) |
| 34 | B50 biodiesel | Operating | Energy self-sufficiency | Missing |

### 2.4 What the current site does well

- A distinctive editorial identity: cream paper, navy header, Source Serif
  headlines and Inter interface text. It does not look like a generic admin
  dashboard.
- Honest coverage language and a Data view that exposes gaps rather than
  hiding them.
- Keyboard support: skip link, Ctrl+K search, Escape to close, focus return
  from the drawer, roving list navigation.
- A real offline build: vendored Leaflet, bundled Natural Earth basemap, no
  tile server or CDN.
- Source-linked claims and a conflict register, which most infrastructure maps
  do not have.

### 2.5 What the current site gets wrong

These findings come from the v3 screenshots and a read of
`site/index.html`, `site/assets/app.css` and `site/assets/app.js`.

| # | Finding | Severity | Evidence |
|---:|---|---|---|
| 1 | **The map is visually passive.** Land and water are both pale, there are no province boundaries, city labels or transport context, and clusters are hard to decode. | High | Screenshot 01: a beige island silhouette on a pale blue field; clusters show mixed status rings but no names. |
| 2 | **The map does not respond to the view.** Corridors and Estates keep the same national project clusters; selecting a corridor does not draw its line or fit its bounds. | High | Screenshots 02 and 03. |
| 3 | **Type is too small.** Many labels are 8.5–11.5 px; the project list, Data view and drawer are dense. | High | `app.css` font sizes; screenshot 04. |
| 4 | **The Data view is squeezed into a 400 px rail** while 70% of the screen shows an unrelated map. | High | Screenshot 04. |
| 5 | **Navigation hides the product.** Four tabs in a rail; no Programmes, Companies, About or Methods entry point. | Medium | `index.html` tabs. |
| 6 | **No page title.** There is no `<h1>`; headings start at the drawer `<h2>`. | High | `index.html`. |
| 7 | **Language is hardcoded.** `<html lang="en">`, every string is inline in HTML or JS, and number/date formats are US-style. | High | `index.html`, `app.js`. |
| 8 | **Search is a substring filter**, with no ranking, aliases, result grouping or keyboard result navigation. | Medium | `app.js` search handler. |
| 9 | **No dark mode, print stylesheet or installable offline mode.** | Low | `app.css`. |
| 10 | **No compare, saved views, timeline or "what changed" surface.** | Medium | Product gap. |
| 11 | **Payload will not scale.** 1.9 MB for 107 projects; 400+ projects with rich text and two languages will exceed a comfortable `file://` load unless split. | High | Build output. |
| 12 | **Accessibility depends on the list.** The map has a region label but no text alternative for spatial relationships; cluster counts are not announced. | Medium | `index.html`, `app.js`. |

### 2.6 Bilingual audit

- No locale layer, no string catalogue, no language switcher.
- Entity names are English translations of Indonesian names; there is no
  canonical Indonesian name field.
- Notes and status explanations are English prose.
- Number and date formatting is implicit and US-centric: `1,161 km`,
  `8 Nov 2026`, `Rp 116T`.
- `lang="en"` is never updated; mixed Indonesian names are not marked with
  `lang="id"`.
- Downloads, dictionary descriptions and error messages are English-only.
- The build has no translation coverage check, so a new project can ship
  without an Indonesian name or summary.

---

## 3. Product vision and principles

**Vision:** a living, bilingual, source-linked atlas of what Indonesia is
building — every major project, the programme it belongs to, the companies
delivering it, the money behind it, and the evidence for its status.

**Audiences and jobs**

| Audience | Job to be done |
|---|---|
| Policy analyst | Which projects are behind, by province and programme? |
| Investor / lender | Who sponsors this, what is the capex, who is contracted, what is the status? |
| Journalist / researcher | What is the source for this claim, and when was it last checked? |
| Student / citizen | What is being built near me, and when will it open? |
| Delivery agency | What is in my portfolio and what changed since last month? |

**Principles**

1. **Map first, but not map only.** The map is the entry point; the list,
   programme cards, tables and detail pages carry the analysis.
2. **Evidence forward.** Status, cost, progress and completion are claims with
   a source and a date. A row without a claim is visibly incomplete.
3. **Editorial calm.** One accent, generous spacing, a readable type scale,
   and no dashboard chrome that competes with the data.
4. **Bilingual parity.** English and Indonesian are built together, not
   translated afterwards. A missing translation is a build defect.
5. **Progressive disclosure.** National overview → programme → project →
   claim. Do not show every field at every zoom.
6. **Offline first.** No network request at runtime; everything is bundled and
   works from `file://`.
7. **Honest coverage.** Show what is missing, estimated, stale or contested.
8. **Comparable.** Same fields, same definitions, same date semantics across
   roads, dams, hospitals and factories.

**Non-goals for V4**

- A real-time project management system or a replacement for ministry
  dashboards.
- A prediction or ranking of project success.
- A tile-server or CDN-dependent map.
- Publishing, remote hosting or GitHub Pages.
- A full financial database for every company; V4 adds profile-level financials
  only where a public source exists.

---

## 4. Information architecture

### 4.1 Top-level navigation

| Item | Purpose | Primary content |
|---|---|---|
| **Overview** | The national picture | KPI strip, map, programme cards, latest changes |
| **Explore** | Find a project | Filters, list, map, detail drawer |
| **Programmes** | The eight PKPN | Target vs current, project lists, indicators |
| **Corridors** | Network progress | Corridor cards, segments, map geometry |
| **Estates** | Industrial geography | KEK and industrial estate map/table |
| **Companies** | Who delivers | Sponsors, operators, contractors, lenders |
| **Data** | Trust and downloads | Coverage, freshness, claims, conflicts, dictionary, changelog |
| **About** | Methods and scope | Inclusion rules, status definitions, corrections |

On desktop the top navigation sits under the brand header. On mobile it
collapses into a bottom bar with five items: Overview, Explore, Programmes,
Data, More.

### 4.2 URL model

```
site/
  index.html            # language chooser / redirect
  en/
    index.html          # English app shell
  id/
    index.html          # Indonesian app shell
  assets/               # shared CSS, JS, fonts
  data/                 # shared data bundles + locale bundles
  downloads/            # static CSV / GeoJSON / JSON
```

Inside a locale, views use hash routes so `file://` works:

```
#/overview
#/explore?view=map&sector=road&status=under_construction
#/project/tol-trans-sumatera
#/programme/energy
#/corridor/trans-sumatra
#/estate/kek-morowali
#/company/pt-hutama-karya
#/data?tab=freshness
#/about
```

The language toggle preserves the current hash and swaps only the locale
prefix. Deep links from v3 (`#project-id`, `#/explore`) redirect to the new
route.

### 4.3 Page templates

1. **Overview:** headline, national map, 8 programme cards, "what changed"
   feed, coverage band.
2. **Explore:** filter rail + map + list; drawer on desktop, full-screen sheet
   on mobile.
3. **Project detail:** title, status, location, hero map, key facts, timeline,
   companies, investment, sources, conflicts, related projects, share/export.
4. **Programme detail:** narrative, target/current indicators, project map,
   project table, timeline, sources.
5. **Corridor detail:** route definition, progress bar, segment table, map with
   line geometry, sources.
6. **Estate detail:** area, occupancy, developer, legal basis, incentives,
   tenants, map, sources.
7. **Company detail:** profile, ownership, portfolio, roles, project map,
   financials (where public), sources.
8. **Data:** full-width dashboard with tabs for Overview, Coverage, Freshness,
   Claims, Conflicts, Programmes, Dictionary, Changelog, Downloads, Methods.
9. **About:** what the atlas is and is not, inclusion rules, status
   definitions, correction policy, licences.

---

## 5. Data expansion plan

### 5.1 Entity model

| Entity | One row per | Why it exists |
|---|---|---|
| `programmes` | national programme or sub-programme | Aggregates projects and indicators under a PKPN |
| `projects` | discrete intervention or asset | The core atlas record |
| `project_phases` | phase or package of a project | IKN, Patimban, MRT, 100 GW, etc. |
| `organizations` | company or agency | Sponsors, operators, contractors, lenders |
| `project_organizations` | project–organisation role | Who does what, with share and dates |
| `investments` | commitment or tranche | Original currency, instrument, status |
| `sources` | document or dataset | First-class provenance |
| `claims` | atomic fact | One fact, one source, one date |
| `conflicts` | contested fact | Both values and both sources |
| `events` | dated event | Groundbreaking, contract, opening, delay |
| `indicators` | measurable target | 100 GW, 441 RSUD, 1,386 villages |
| `indicator_values` | dated measurement | Current vs target over time |
| `corridors` | network summary | Trans Sumatra, Java, Sulawesi, etc. |
| `corridor_segments` | segment | Progress and geometry |
| `estates` | KEK or industrial estate | Industrial geography |
| `geometry` | point, line or polygon | Map layer with precision and source |
| `translations` | translated field | Locale, text, status, reviewer |
| `coverage_targets` | expected reference set | Coverage dashboard |
| `laws` | regulation | Legal basis |
| `project_laws` | project–law relation | Designation and incentives |

### 5.2 Target reference set

The counts are coverage targets, not a promise that every row is complete on
day one. A record can enter at Tier C and be upgraded.

| Layer | Today | V4 target | Source of the reference set |
|---|---:|---:|---|
| PSN projects | 176 project rows linked; 226 records represented (88 register-only projects + 18 register-only estates) | **226 active** (228 slots, 2 deleted) | Permenko 16/2025; Permenko 4/2026 |
| PSN programmes | 24 programme records; 24/24 represented | **24 active** (25 slots, 1 deleted) | Permenko 16/2025 |
| Strategic non-PSN projects | 3 | **174+** | Ministries, Danantara, private announcements |
| National programmes (PKPN) | 8 | **8** | 2027 budget speech; Finance Ministry breakdown |
| Sub-programmes | 0 | **40–60** | Ministry work plans |
| IKN packages | 24 | **25** | IKN Authority; Setkab releases |
| Energy projects | 24 (15 register-only) | **60** | ESDM, PLN, Danantara |
| Transport projects | 90 | **150** | Kemenhub, PU, BPJT |
| Water and sanitation | 66 (61 register-only) | **60** | PU, PDAM, KPPIP |
| Industry and downstreaming | 34 | **80** | Kemenperin, BKPM, company disclosures |
| Social infrastructure | 4 (2 housing, 1 education, 1 tourism) | **30** | Kemenkes, Kemendikbud, PKP |
| Estates and SEZs | 204 (18 register-only) | **200+** | KEK Secretariat, Kemenperin |
| Companies | 111 | **300** | BUMN, Danantara, private, foreign |
| Corridor segments | 44 | **100+** | KPPIP, PU, BPJT |
| Claims | 708 | **1,500+** | Every project, company and indicator |
| Indicators | 14 | **300+** | PKPN targets and ministry reporting |
| Sources | 135 | **250+** | Official, company, multilateral, news |

### 5.3 Inclusion rules

A project enters the atlas if it meets **at least one** of these:

- Designated PSN, PKPN or KPBU.
- Investment of at least **Rp 1 trillion** (about US$60–65M at 2026 rates).
- A national or regional network node (toll corridor, railway, hub port,
  international airport, transmission line, dam, industrial estate).
- At least **100,000 beneficiaries** or a national programme target.
- A named sponsor, contract or groundbreaking and a public source.

A project is excluded if it is:

- A slogan, aspiration or unnamed proposal with no sponsor, budget or date.
- A duplicate of another record (use aliases and phases instead).
- A routine maintenance or procurement package below the threshold.
- A private project with no public source and no named sponsor.

**Status vocabulary**

| Status | Meaning |
|---|---|
| `planned` | Designated, studied or announced; no construction contract |
| `tendered` | Procurement or tender open |
| `financed` | Financial close or funding secured; construction not started |
| `under_construction` | Contract signed or groundbreaking held |
| `testing` | Commissioning or trial operation |
| `operating` | In commercial or public operation |
| `recently_completed` | Opened within the last 24 months |
| `stalled` | Officially delayed or reported stalled |
| `suspended` | Temporarily halted |
| `cancelled` | Removed or terminated |

`status_as_of` is mandatory. A status older than 12 months is flagged.

### 5.4 Sector playbooks

#### Roads and bridges

- **Reference set:** 54 KPPIP road entries plus the national road programme,
  1,151 km of regional roads, strategic bridges and flyovers.
- **Gap:** the ledger matches 38 of 50 PSN road entries to 33 unique atlas
  road rows. Twelve PSN roads are missing: Kisaran–Tebing Tinggi;
  Bukittinggi–Padang Panjang–Lubuk Alung–Padang; Pekanbaru–Bangkinang–
  Payakumbuh–Bukittinggi; Tebing Tinggi–Pematang Siantar–Parapat–Tarutung–
  Sibolga; Jambi–Rengat; Rengat–Pekanbaru; Serpong–Cinere;
  Cimanggis–Cibitung; the Teluk Lamong flyover; the Patimban access road;
  the New Priok Eastern Access; and the Bandung inner-city toll roads. Six
  Jakarta inner-city entries map to one aggregate atlas row, and two
  corridors (Ciawi–Sukabumi and Gilimanuk–Mengwi) are partial matches.
- **Fields:** length, operational/construction km, progress, concession,
  operator, status, opening date, geometry.
- **Sources:** BPJT API, KPPIP, PU, Hutama Karya, Jasa Marga, concession
  announcements.

#### Railways

- **Reference set:** MRT Jakarta N–S and E–W, LRT Jakarta/Jabodebek/Palembang,
  Whoosh and the Surabaya extension, Trans Sulawesi, Kalimantan logistics
  rail, station revitalisation, airport rail links, freight.
- **Gap:** no station-level assets, no phase-level progress, no Jakarta
  integrated rail map.
- **Fields:** line, phase, stations, length, gauge, electrification, operator,
  rolling stock, progress, opening.
- **Sources:** Kemenhub, KAI, MRT Jakarta, LRT Jakarta, KCIC, KPPIP.

#### Airports

- **Reference set:** 7 PSN airports plus IKN, North Bali, Kertajati, Soekarno–Hatta
  expansion, major regional upgrades.
- **Gap:** IKN and North Bali are missing; airport capacity and terminal
  expansion are not modelled.
- **Fields:** IATA/ICAO, terminal capacity, runway, passengers, status,
  operator, investment.
- **Sources:** Kemenhub, Angkasa Pura, InJourney, IKN Authority.

#### Seaports and ferries

- **Reference set:** 15 PSN ports plus Patimban phases, Kuala Tanjung, Bitung,
  Makassar, Benoa, Kijing, fishing ports, RoRo and sea toll.
- **Gap:** terminals and phases are collapsed into one row; fishing ports are
  missing.
- **Fields:** port type, terminal, draft, capacity (TEU/tonnes/passengers),
  operator, status, investment, hinterland.
- **Sources:** Pelindo, Kemenhub, KPPIP, KEK Secretariat.

#### Energy

- **Reference set:** 100 GW solar programme, 37 electricity projects (3.2 GW +
  11 transmission packages), geothermal, hydro, gas, LNG (Masela, Tangguh),
  RDMP/GRR, waste-to-energy, storage, transmission, rural electrification.
- **Gap:** zero energy generation or transmission records today.
- **Fields:** technology, capacity (MW/MWp), storage, fuel, grid connection,
  COD, PPA, owner, EPC, status.
- **Sources:** ESDM, PLN, Pertamina, Danantara, RUPTL, company disclosures.

#### Water, sanitation and flood control

- **Reference set:** PSN dams, irrigation schemes, SPAM, Jakarta sewerage, flood
  control, the 15-segment Java sea wall, 9,000 km of irrigation, 3,000
  boreholes.
- **Gap:** zero water records today; the current atlas has no dams despite
  dams being one of the largest PSN sectors.
- **Fields:** type, capacity (m³, ha, MW), service area, beneficiaries,
  progress, operator, status.
- **Sources:** PU, KPPIP, Perum Jasa Tirta, provincial water utilities.

#### Industry and downstreaming

- **Reference set:** 13 downstreaming stage II projects, 11 IWIP projects, existing
  smelters, petrochemicals, steel, aluminium, battery/EV, pulp/paper,
  fertiliser, food processing, data centres.
- **Gap:** 34 factories today. Stage II is now project-level, but the 11 IWIP
  packages, the remaining PSN industrial areas and company roles are missing.
- **Fields:** commodity, capacity, feedstock, offtake, investment, owner,
  EPC, status, location, environmental notes.
- **Sources:** Kemenperin, BKPM, Danantara, company disclosures, AMDAL.

#### Estates and SEZs

- **Reference set:** 25 KEKs plus 179 industrial estates; 2025 additions and exact
  boundaries.
- **Gap:** 204 rows and 186 industrial-estate designations, so the 179 count is
  met. Only 20/40 large estates are geocoded, 18 PSN areas are register-only and
  seven named 2024 additions still need an individual source; map layer off.
- **Fields:** type, area, occupancy, developer, legal basis, incentives,
  sector focus, tenants, coordinates/polygon, sources.
- **Sources:** KEK Secretariat, Kemenperin, Satu Peta, developers.

#### Housing, health, education and social infrastructure

- **Reference set:** three million houses, 441 RSUD, 10,000 puskesmas, 514 labs,
  265 Sekolah Rakyat, school renovation, 288,180 IFPs, universities, sports.
- **Gap:** zero records; these are national programmes with site-level
  examples, not individual procurements.
- **Approach:** one programme record plus representative site records and
  indicators; do not attempt 10,000 puskesmas rows.
- **Sources:** PKP, Kemenkes, Kemendikbud, National Nutrition Agency, Setkab.

#### Digital, tourism and fisheries

- **Digital:** Palapa Ring, Satria, data centres, 5G, government cloud, AI.
- **Tourism:** five super-priority destinations, KEK tourism, access works.
- **Fisheries:** 1,386 fishing villages, BUBK, cold chain, fish ports,
  1,582 boats.
- **Sources:** Komdigi, Kemenpar, KKP, Setkab.

### 5.5 The delivery layer

Every project and programme should answer:

- **What is the target?** A number, a unit and a date.
- **What is the current value?** A number, a date and a source.
- **Who is delivering it?** Sponsor, owner, operator, contractor, lender.
- **What is the money?** Original currency, IDR equivalent, instrument,
  status.
- **What changed?** The latest event and the previous status.
- **How confident are we?** Tier A/B/C, last verified, conflicts.

This is implemented through `programmes`, `indicators`, `indicator_values`,
`project_organizations`, `investments`, `events` and `claims`. The Programme
view is the primary surface; the Explore filters can also filter by programme.

### 5.6 Companies

V4 adds a Company view and a richer organisation model:

- **Types:** BUMN, BUMN subsidiary, Danantara portfolio, private Indonesian,
  foreign, state agency, multilateral, SPV.
- **Roles:** sponsor, owner, operator, contractor, EPC, lender, investor,
  off-taker, consultant, regulator.
- **Fields:** legal name, short name, ticker, ownership, parent, country, HQ,
  website, sector, summary, total project exposure, sources.
- **Coverage:** 300 organisations; top 100 by project count or investment
  complete; every project has at least one sponsor/owner and, where known,
  an operator and contractor.
- **Key clusters:** Danantara seven (Bank Mandiri, BNI, BRI, MIND ID,
  Pertamina, PLN, Telkom), infrastructure SOEs (Hutama Karya, Jasa Marga,
  Pelindo, Angkasa Pura, KAI, MRT Jakarta, KCIC, Waskita, Wijaya Karya, PP,
  Adhi, Brantas Abipraya), industrial SOEs (Krakatau Steel, Pupuk Indonesia,
  Semen Indonesia, Inalum, Antam, Vale Indonesia, Freeport), and private
  sponsors (Salim, Sinar Mas, Djarum, Lippo, Agung Sedayu, Astra, Adaro,
  Harita, Merdeka Copper Gold, Amman, Tsingshan, CATL, Lotte, Chandra Asri).

### 5.7 Estates

- Keep the 25 official KEKs; add the 2025–2026 additions and verify the
  current list against the KEK Secretariat.
- Reconcile 204 rows against the 179-estate Kemenperin count; the count is met.
  Resolve the seven named 2024 additions and upgrade the 18 register-only PSN
  industrial areas with area, developer, status and boundary.
- Geocode the remaining large estates; use Satu Peta polygons where available.
- Add occupancy, tenants, incentives and sector focus where sourced.
- Turn the estate map layer on once at least 80% of rows have better than
  regency-centroid precision.

### 5.8 Sources and verification

**Source hierarchy**

| Tier | Source | Use |
|---|---|---|
| A1 | Law, regulation, presidential instruction, RPJMN | Designation, legal basis |
| A2 | Official project page or ministry release naming the project, cost, status | Core facts |
| A3 | Official dataset or portal (BPJT, Satu Peta, Kemenperin, KEK) | Coordinates, counts, status |
| B1 | Company annual report, prospectus, disclosure | Sponsor, capex, capacity |
| B2 | Multilateral project document (World Bank, ADB, AIIB, JICA) | Financing, safeguards |
| C1 | Reputable news with a named official or company statement | Status changes, events |
| C2 | Wikipedia, OSM | Discovery and geometry only |
| D | Social media, unattributed blogs | Do not use for claims |

**Rules**

- Every project needs at least one A2/A3 or B1 source and one dated claim.
- A status change needs an A2/A3 source or two independent C1 sources.
- Costs keep the original currency and the exchange-rate date.
- Coordinates must fall inside 95–141°E and 11°S–6°N; precision is explicit.
- Conflicts are recorded in `conflicts.csv`, not silently resolved.
- Snapshots go to `data/raw/YYYY-MM-DD/`; the source row records the path and
  hash.
- A row not re-checked in six months is `due_soon`; after twelve months it is
  `stale` and is flagged in the UI.

### 5.9 Schema changes

Add to `projects.csv`:

```
name_id, name_en, summary_id, summary_en, programme_id, pkpn_id,
asset_type, implementation_type, cost_idr_t, cost_usd_b,
beneficiaries, start_date, target_date, actual_end_date,
progress_as_of, geometry_id, coverage_tier, translation_status
```

Add to `organizations.csv`:

```
name_id, name_en, ticker, ownership, company_type, hq_city, hq_province,
founded_year, employees, assets_idr_t, revenue_idr_t,
danantara_portfolio, summary_id, summary_en, translation_status
```

Add to `estates.csv`:

```
name_id, name_en, summary_id, summary_en, tenants_count, incentives,
polygon_id, translation_status
```

Add to `sources.csv`:

```
title_id, title_en, language, publisher_type, archive_path, snapshot_hash,
accessed_via, licence
```

New tables:

- `programmes.csv` — id, name_en/id, pkpn_id, lead_org_id, summary_en/id,
  target_summary_en/id, start_year, target_year, status, budget_idr_t,
  source_id, last_verified.
- `indicators.csv` — id, programme_id, project_id, name_en/id, unit,
  direction, baseline_value, baseline_date, target_value, target_date,
  source_id.
- `indicator_values.csv` — indicator_id, value, as_of, source_id, notes.
- `translations.csv` — **implemented 9 November 2026**: entity_type, entity_id,
  field, locale, text, status, translator, reviewed_on, source_id. Validated by
  `validate.py` and consumed by `build_i18n.py`.
- `project_phases.csv` — project_id, phase, name_en/id, status, cost,
  start_date, end_date, progress, source_id.
- `geometry.csv` — id, entity_type, entity_id, kind, geojson, precision,
  source_id.

`project_events.csv` gets a controlled `event_type` vocabulary and a
`significance` field. `conflicts.csv` gets both source ids, a resolution and a
`resolved_on` date.

### 5.10 Data quality and coverage

**Coverage tiers**

| Tier | Minimum |
|---|---|
| A | Official source, 2+ claims, coordinates, geometry, EN/ID name and summary |
| B | Official source, 1 claim, coordinates, EN/ID name |
| C | Secondary source, 1 claim, province centroid, EN name; ID pending |

The Data view reports the tier mix. The target is 60% Tier A, 30% Tier B and
10% Tier C at Release 4.5, with no Tier C row older than six months.

**Project intake checklist**

1. Name in Indonesian and English.
2. Sector, subsector, programme and PKPN.
3. Status, status basis and status date.
4. Province, regency, island, coordinates and precision.
5. Cost, currency, capacity and beneficiaries (where known).
6. Sponsor, owner, operator, contractor and lender (where known).
7. At least one source and one atomic claim.
8. Geometry (point, line or polygon) or an explicit "no geometry" note.
9. Indonesian and English summary.
10. Coverage tier and last verified date.

---

## 6. Bilingual architecture

### 6.1 Principles

- **Locale is a first-class dimension**, not a translation layer applied at the
  end.
- **Indonesian is the source language for official names and facts**; English
  is the primary interface language for the international edition. Both are
  maintained.
- **Proper names are not translated.** `Danantara`, `PSN`, `KEK`, `IKN`,
  `MBG`, `RSUD`, `Puskesmas`, `Bendungan Meninting` and similar names stay in
  Indonesian; an English gloss may follow in parentheses on first use.
- **Numbers, dates and currency follow the locale**, not the source language.
- **Missing translations are visible, not silent.** A field with no Indonesian
  text shows the original with a small "Belum diterjemahkan" label.

### 6.2 Locale routing

Two static entry points share one application and one data bundle:

```
site/en/index.html   <html lang="en">
site/id/index.html   <html lang="id">
```

- All asset and data URLs are relative (`../assets/...`, `../data/...`), so
  both work from `file://`.
- `site/index.html` is a tiny language chooser. It reads
  `navigator.language` and offers English and Indonesian; it never blocks the
  app if JavaScript is unavailable.
- The header language control swaps the path prefix and preserves the hash,
  filters, selected project and scroll position.
- When the atlas is eventually published, `/en/` and `/id/` are clean URLs,
  each with `hreflang` links and a localized `<title>` and description.
- `document.documentElement.lang` is set by the shell and updated on switch;
  mixed-language content uses `<span lang="id">` or `<span lang="en">`.

### 6.3 String catalogue and data translations

**UI strings** live in:

```
data/i18n/ui.en.json
data/i18n/ui.id.json
```

Keys are semantic, not English sentences:

```json
{
  "nav.explore": "Explore",
  "status.under_construction": "Under construction",
  "action.download": "Download",
  "label.last_verified": "Last verified"
}
```

The build generates `site/data/i18n.en.js` and `site/data/i18n.id.js` as
classic scripts so `file://` works without `fetch`.

**Entity translations** live in `data/curated/translations.csv`:

```
entity_type,entity_id,field,locale,text,status,translator,reviewed_on,source_id
project,tol-sigli-banda-aceh,name,id,Jalan Tol Sigli–Banda Aceh,official,,,
project,tol-sigli-banda-aceh,summary,en,The toll road links...,reviewed,editor,2026-11-08,src-001
```

`status` is one of `official`, `reviewed`, `draft`, `machine`, `missing`.
Machine translations may be used for discovery but are never shown as reviewed.

```
source text (ID / EN)
        │
        ▼
data/curated/translations.csv ──┐
data/i18n/ui.<locale>.json ─────┤
                                ▼
                    scripts/pipeline/build_i18n.py
                                │
                                ▼
                  site/data/i18n.<locale>.js
                                │
                                ▼
                  views read t(key) and localized fields
```

**Required translation fields by entity**

| Entity | Required in both locales |
|---|---|
| Project | name, summary |
| Programme | name, summary, target summary |
| Corridor | name, definition |
| Estate | name, summary |
| Company | name, summary |
| Indicator | name, unit label |
| Source | title (original language is allowed; translated title optional) |
| UI | every key |

### 6.4 Formatting

Use the platform `Intl` APIs, not hand-rolled separators:

- Numbers: `new Intl.NumberFormat(locale)`; English `1,151`, Indonesian
  `1.151`.
- Percentages: `72.6%` / `72,6%`.
- Currency: keep the original currency and add an IDR or USD equivalent with
  the conversion date. English: `Rp 116 trillion (US$7.2B)`; Indonesian:
  `Rp 116 triliun (US$7,2 miliar)`.
- Dates: `8 Nov 2026` / `8 Nov 2026`; long form `8 November 2026`.
- Relative time: `3 months ago` / `3 bulan lalu`.
- Lists: `Intl.ListFormat` for "roads, railways and ports" / "jalan, kereta
  api, dan pelabuhan".

The formatter is a single module used by every view, drawer, download note and
chart axis. No view may call `toLocaleString()` without an explicit locale.

### 6.5 Search

- Build one index per locale plus a shared alias index.
- Fields: Indonesian name, English name, aliases, province, regency, corridor,
  programme, company, estate.
- Ranking: exact match, prefix, token match, fuzzy (edit distance ≤ 2).
- Synonyms: `tol`/`toll`, `bandara`/`airport`, `pelabuhan`/`port`,
  `kawasan industri`/`industrial estate`, `KEK`/`SEZ`.
- Searching in English still finds Indonesian names, and vice versa.
- Results are grouped by type (Projects, Programmes, Estates, Companies) and
  navigable with arrow keys.

### 6.6 Translation workflow and QA

1. **Extract.** The build lists every missing key and every entity field without
   an Indonesian or English value.
2. **Translate.** A translator edits `ui.id.json` and `translations.csv`.
3. **Review.** A second reviewer marks `reviewed`; official names use
   `official`.
4. **Validate.** `build_i18n.py` fails on missing UI keys and on missing
   required entity fields; it warns on Tier C rows with no translation.
5. **Pseudo-localize.** A test locale (`en-XA`) expands strings by 30% and
   brackets them to catch overflow.
6. **Screenshot diff.** Smoke test captures EN and ID desktop/mobile views and
   compares layout, not pixels.
7. **Glossary check.** A script flags forbidden translations (for example
   "toll road" rendered as "jalan bebas hambatan" where the atlas uses
   "jalan tol").

### 6.7 English–Indonesian glossary

| English | Indonesian | Note |
|---|---|---|
| toll road | jalan tol | Not "jalan bebas hambatan" |
| railway | kereta api | |
| airport | bandar udara | "bandara" in UI labels |
| seaport | pelabuhan | |
| industrial estate | kawasan industri | |
| special economic zone (SEZ) | kawasan ekonomi khusus (KEK) | Keep the abbreviation |
| under construction | dalam konstruksi | |
| operating | beroperasi | |
| planned | direncanakan | |
| recently completed | baru selesai | |
| stalled | terhenti | |
| downstreaming | hilirisasi | Keep |
| investment | investasi | |
| source | sumber | |
| claim | klaim | |
| last verified | terakhir diverifikasi | |
| coverage | cakupan | |
| freshness | keterbaruan | |
| conflict | konflik | |
| programme | program | |
| company | perusahaan | |
| estate | kawasan | Context-dependent |
| dam | bendungan | |
| irrigation | irigasi | |
| water supply | penyediaan air minum | |
| transmission | transmisi | |
| power plant | pembangkit listrik | |
| solar power plant | PLTS | Keep the abbreviation |
| hydropower plant | PLTA | Keep |
| geothermal | panas bumi | |
| sea wall | tanggul laut | |
| fishing village | kampung nelayan | |
| co-operative | koperasi | |
| public health centre | puskesmas | Keep |
| regional hospital | RSUD | Keep |
| school | sekolah | |
| housing | perumahan | |
| village | desa/kelurahan | Context-dependent |
| budget | anggaran | |
| target | target | |
| progress | progres | |
| capacity | kapasitas | |
| beneficiaries | penerima manfaat | |

### 6.8 Future languages

The locale registry is a list, not a binary switch. Adding a language means:

1. Add `data/i18n/ui.<locale>.json`.
2. Add translation rows for required entity fields.
3. Add a glossary file.
4. Add the locale to the build, the language chooser and the smoke test.
5. If the script is right-to-left, add `dir="rtl"` support and mirror the
   layout; the current CSS uses logical properties where possible.

No view may hardcode a language name, date format or currency label.

---

## 7. Design and UX plan

### 7.1 Visual direction

**Editorial atlas, not SaaS dashboard.** Keep the cream paper, deep navy and
single burnt-orange accent. Make the map the hero; use serif headlines for
place and programme names, and Inter for interface and data. The page should
feel like a well-made reference book that happens to be interactive.

Specific moves:

- **Stronger map contrast.** Land `#f2eee3`, water `#cfe0ea`, province lines
  `#c9c2b2`, labels `#4b5563`. Add a subtle hillshade only if it does not
  compete with the data layer.
- **More whitespace.** Replace the 8.5–11.5 px density with a 14–16 px body
  and 12–13 px captions. Let the data breathe.
- **One accent, one alert.** Keep burnt orange for action and under
  construction; reserve red for stalled/cancelled. Do not use accent colour
  for decoration.
- **Editorial numbers.** Large serif numerals for headline stats (226 PSN,
  24 programmes, 100 GW, 441 RSUD), with a small unit label and a source line.
- **Status as a system.** Colour + icon + text label, never colour alone.

**What changes, screen by screen**

| Screen | Today | V4 |
|---|---|---|
| Header | Brand, search, three stats, Data link | Brand, primary nav, search, EN/ID, theme |
| Explore | 400 px rail, map, drawer | 380 px rail, linked map highlight, overlay drawer, map-only mode |
| Corridors | Cards beside an unchanged project map | Cards plus corridor geometry, segment progress, fit bounds |
| Estates | Table only; map layer off | Map polygons/centroids, filters, estate profile |
| Data | Cramped rail beside an unrelated map | Full-width dashboard with coverage, freshness, claims, conflicts, downloads, methods |
| Project | Drawer only | Drawer plus a shareable project page with timeline and companies |
| Programmes | None | Eight PKPN cards, target vs current, project lists, indicators |
| Companies | 111 profiles, 227 roles | 300 profiles, roles, portfolio, project map |
| Mobile | Map + sheet | Map + three-snap sheet + bottom navigation + full-screen detail |
| Type | 8.5–12 px in many places | 13–16 px body/caption scale, 1.5 line height |

### 7.2 Design tokens

| Token | Value |
|---|---|
| Paper | `#fbf9f4` |
| Surface | `#ffffff` |
| Ink | `#101828` |
| Navy | `#0b1f33` |
| Muted | `#667085` |
| Line | `#e4e7ec` |
| Accent | `#b54708` |
| Under construction | `#c2410c` |
| Planned | `#1d4ed8` |
| Operating | `#0f766e` |
| Recently completed | `#15803d` |
| Stalled | `#b42318` |
| Cancelled | `#7f1d1d` |

**Type scale:** 12, 14, 16, 18, 22, 28, 36, 48. Body 16/1.6; captions 13/1.4;
headline 36–48/1.1. Maximum line length 70 characters.

**Spacing:** 4, 8, 12, 16, 24, 32, 48, 64.

**Radius:** 4 (chips), 8 (cards), 12 (panels), 16 (sheets).

**Motion:** 120 ms for hover, 180 ms for drawer, 240 ms for map fit; respect
`prefers-reduced-motion`.

### 7.3 Layout

**Desktop (≥ 1200 px)**

```
┌──────────────────────────────────────────────────────────────┐
│ Header: brand · nav · search · EN/ID · theme                 │
├───────────────┬──────────────────────────────────────────────┤
│ Filter rail   │ Map                                          │
│ 380 px        │ flex                                         │
│ list / cards  │                                              │
│               │                                              │
└───────────────┴──────────────────────────────────────────────┘
                                  Drawer 440 px (overlay)
```

- The rail is collapsible; a "map only" mode expands the map.
- The drawer is an overlay, not a third column, so the map does not shrink.
- Data, Programmes, Companies and About are full-width pages with a max width
  of 1280 px; the map is an embedded component, not the page background.

**Tablet (860–1199 px):** rail 320 px; drawer full-height overlay; map
controls compact.

**Mobile (< 860 px):**

```
┌──────────────────────────┐
│ Header: menu · search    │
├──────────────────────────┤
│ Map 55vh                 │
│  (legend, layers, scale) │
├──────────────────────────┤
│ ═══ sheet handle         │
│ Explore · Programmes ·…  │
│ result count · sort      │
│ project rows             │
├──────────────────────────┤
│ Overview Explore … More  │
└──────────────────────────┘
```

The sheet has three snap points (peek, half, full); the handle is a real
button; filters open as a full-screen sheet; detail opens as a full-screen page
with a back button.

### 7.4 Map v3

**Base layers**

- Land, water, province boundaries, regency boundaries at zoom 7+, city labels,
  major roads and railways at zoom 8+, scale bar, attribution.
- Natural Earth + BIG boundaries, simplified to keep the payload small.

**Data layers**

| Layer | Low zoom | High zoom |
|---|---|---|
| Projects | Donut clusters by status | Sector-shaped markers with status fill |
| Corridors | Coloured lines, dashed for planned | Segment points and progress labels |
| Estates | Centroid dots by type | Polygons by type, labels at zoom 10+ |
| Companies | Hidden | HQ markers when toggled |
| Investment | Optional choropleth by province | Province tooltip with total |
| Freshness | Optional heatmap | Project-level stale markers |

**Interaction**

- Hover a list row → highlight the matching marker; hover a marker → highlight
  the row.
- Click a row → fit the map to the project and open the drawer.
- Click a cluster → zoom to its bounds; at max zoom, spiderfy.
- Select a corridor → draw its line, fit bounds, show segment progress.
- Select an estate → zoom to its polygon or centroid.
- Filter changes animate the map and update the legend counts.
- "Fit Indonesia" and "locate me" controls; full-screen mode.

**Accessibility**

- A "View as table" control exposes the same data in a sortable table.
- Map controls have visible labels and keyboard focus.
- Cluster counts are announced through an `aria-live` region.
- Status is never conveyed by colour alone; markers carry a shape or letter.
- A text summary above the map states the number of projects, the current
  filter and the visible extent.

### 7.5 Components

- **Header:** brand, primary nav, search, language, theme.
- **Filter bar:** sector, status, province, island, programme, PSN, precision,
  freshness; chips with counts; "More filters" sheet.
- **Project row/card:** name, status, sector, location, progress, last
  verified, source count.
- **Stat tile:** label, value, unit, delta, source.
- **Programme card:** PKPN icon, target vs current, progress bar, project count,
  investment.
- **Company card:** name, type, country, roles, project count.
- **Detail drawer/page:** title, status, location, key facts, map, timeline,
  companies, investment, sources, conflicts, related.
- **Timeline:** event type icon, date, description, source.
- **Data table:** sticky header, sortable columns, column chooser, CSV export.
- **Chart:** bar, stacked bar, sparkline, donut; SVG, no library.
- **Feedback:** empty state, loading skeleton, error state, toast, tooltip.

### 7.6 Content design

**Project page order**

1. Title, status badge, sector and location.
2. One-sentence summary: what it is and why it matters.
3. Key facts: cost, capacity, length, beneficiaries, start and target dates.
4. Map with the project highlighted and related projects nearby.
5. Progress and timeline (groundbreaking, milestones, expected opening).
6. Companies and roles (sponsor, owner, operator, contractor, lender).
7. Investment table with original currency and IDR/USD equivalents.
8. Sources and claims, with dates and source-language badges.
9. Conflicts and caveats.
10. Related projects, programme link, share and export.

- Write short, factual summaries: what it is, where it is, why it matters,
  what is happening now.
- Put the number first: "982 of 2,854 km operational", not "The Trans Sumatra
  toll road has a total length of...".
- Use the same status vocabulary everywhere.
- Every claim links to a source and a date.
- Show the source language when it is Indonesian: a small `ID` badge.
- Use "not yet verified" and "estimated" explicitly; never imply precision
  that the source does not support.

### 7.7 Accessibility

Target **WCAG 2.2 AA**. Priority checks:

- One `<h1>` per page; logical heading order.
- Skip link; visible focus; no keyboard trap; Escape closes overlays.
- Contrast: 4.5:1 for text, 3:1 for UI components and graphics.
- Status not conveyed by colour alone.
- Target size at least 24×24 px.
- Text resize to 200% without loss; reflow at 320 px.
- `lang` on the page and on mixed-language spans.
- Accessible names for icon buttons; `aria-live` for result counts and map
  updates.
- Reduced motion; no autoplay.
- Tables with `<caption>`, `<th scope>` and a meaningful reading order.

### 7.8 Performance

- **Initial payload:** < 1.5 MB raw for the shell, core data and one view.
- **Total payload:** < 5 MB including both locales and downloads.
- Split bundles by view: core, explore, programmes, companies, estates, data.
- Load detail records on demand from a compact index.
- Use compact arrays for map points; avoid repeating text in every bundle.
- Canvas renderer and clustering for 400+ markers.
- Simplify geometry; drop province polygons below zoom 6.
- Keep fonts; subset if the payload grows.
- Build check fails if a budget is exceeded.

### 7.9 Responsive and mobile

- Map-first, but the sheet must be usable with one hand.
- Three snap points; the handle is a real button; keyboard arrows resize.
- Bottom navigation with five items; "More" opens a sheet with Companies,
  Estates, About and language.
- Filters apply immediately and show the result count.
- Detail pages are full-screen with a sticky back button and share action.
- Downloads work on mobile; CSV opens in the device's default app.

### 7.10 Print and export

- A print stylesheet for project, programme and data pages: white background,
  no map controls, source list included.
- Filtered CSV, GeoJSON and JSON exports for every view.
- A "download this page" action for the current project or programme.
- A static `atlas-<date>.zip` is out of scope for V4; the downloads folder is
  the export surface.

---

## 8. Delivery plan

### Release 4.0 — Foundation (2 weeks)

**Scope**

- Freeze V4 scope and the target list.
- UX audit with five users; task success baseline. **Partial:** expert heuristic
  audit and an automated five-profile rehearsal exist; five external users are
  still open.
- Design tokens v2 and a static style tile. **Done:** `tokens-v4.md`,
  `style-tile.html` and `check_contrast.py`.
- Schema v4 migration plan and validation rules. **Partial:** the translation
  layer is in; indicators and phases remain.
- Bilingual shell: `site/en/`, `site/id/`, UI catalogues, language toggle.
  **Done.**
- Build checks: missing UI keys, payload budget, link check. **Done.**

**Acceptance**

- Both locales load from `file://` and HTTP. **Met:** smoke-tested on both.
- The language toggle preserves the current view. **Met.**
- `build_all.py --check` passes. **Met.**
- A written UX audit and design token sheet exist. **Met for the expert audit
  and token sheet; the five-user baseline is not claimed.**

### Release 4.1 — PSN complete (4 weeks)

**Scope**

- Reconcile the 226 active PSN projects and 24 programmes against the current
  228 project records. **Done 9 November 2026: 226/226 represented.**
- Add the missing road entries and all PSN dams, irrigation, water and
  sanitation, energy and housing records. **Done at Tier C:** 88 register-only
  project rows, plus 18 register-only industrial areas.
- Add IKN Phase 2 and the Nusantara airport. **Done.**
- Add the 37 electricity projects, Masela, RDMP Balikpapan, 100 GW solar,
  the 13 stage II projects and the 11 IWIP projects. **Partly done:** Masela,
  RDMP, solar and stage II are in; the 37 electricity and 11 IWIP packages are
  not yet separate rows.
- Add the 8 PKPN programmes and their headline indicators. **Done (9 Nov
  2026):** `pkpn_programmes.csv` (8 rows, bilingual summaries and targets, 27
  claims, 2 sourced budgets) and 11 PKPN indicators. Current values are shown
  only where sourced; the rest say "No observation yet".
- Seed 20–30 company records for the new projects. **Open.**

**Acceptance**

- 100% of the PSN list has a record or a documented exclusion. **Met.**
- Every new record has a source, a claim and a status date. **Met for Tier C**
  through the PSN, location and active-designation claims; full EN/ID names and
  implementation facts remain to be upgraded.
- The Programme view shows target vs current for 8 programmes. **Met for target
  visibility:** all eight PKPN cards show the sourced target and budget where
  stated; current values appear only where a source states one.
- Coverage report shows the PSN gap at zero. **Met.**

### Release 4.2 — Industry, companies and estates (4 weeks)

**Scope**

- Expand to 300 organisations and 200 estates. **Partial:** 111 organisations
  and 204 estates; the Companies view is in.
- Add hilirisasi, petrochemical, steel, battery, EV, data centre and food
  processing projects. **Partial:** 34 factories and the 13 Hilirisasi Stage II
  rows are in; data centre, EV and food processing remain.
- Add social infrastructure programmes: 441 RSUD, 10,000 puskesmas, 265
  Sekolah Rakyat, school renovation, housing. **Open.**
- Add fisheries, tourism and digital projects. **Partial:** tourism and
  technology PSN rows are in; fisheries remain.
- Add company profiles and roles for the top 100. **Partial:** 111 profiles,
  227 roles, 89 with links; 22 are reference-only.
- Geocode the remaining large estates; enable the estate map layer for rows
  with better than regency precision. **Open.**

**Acceptance**

- Every project has at least one organisation role. **Open:** 151 of 251.
- Top 100 companies have a profile, a source and a project list. **Partial:**
  111 profiles exist; 89 have at least one sourced role and 22 do not.
- Estate map layer is on for at least 80% of rows with point/polygon geometry.
  **Open.**
- The Company and Estate views pass the smoke test on both locales. **Partial:**
  the Companies view passes in English; the Indonesian smoke check covers the
  tab label, not the full view.

### Release 4.3 — Experience rebuild (4 weeks)

**Scope**

- New top navigation and mobile bottom bar.
- Map v3 with province boundaries, labels, linked highlighting and corridor
  and estate layers.
- Project, programme, corridor, estate and company detail pages.
- Full-width Data dashboard with charts and downloads.
- Search v2 with ranking, aliases and grouped results. **Partial:** grouped
  counts, corridor results and Indonesian–English synonyms are in; fuzzy
  ranking and arrow-key result navigation remain.
- Compare, saved views and "what changed" feed.

**Acceptance**

- A user can go from national view to a project in two interactions.
- Selecting a corridor draws its geometry and fits bounds.
- Data view uses the full content width.
- Task success improves by at least 30% over the 4.0 baseline.
- Keyboard-only path covers every primary task.

### Release 4.4 — Bilingual complete (3 weeks)

**Scope**

- Translate 100% of UI keys, names, summaries, programmes, indicators and
  dictionary descriptions.
- Add `Intl` formatting everywhere.
- Review the 100 highest-traffic strings and all programme names.
- Add pseudo-localization and screenshot diff to the smoke test.
- Publish the glossary and translation status in the Data view.

**Acceptance**

- Zero missing UI keys; zero missing required entity translations.
- EN and ID screenshots pass layout checks at 1440, 768 and 390 px.
- Numbers, dates and currency render correctly in both locales.
- A native Indonesian reviewer signs off the glossary and programme names.

### Release 4.5 — Trust and release (2 weeks)

**Scope**

- Claims coverage at 1,500+; conflicts reviewed; freshness under control.
- Accessibility audit and fixes; performance budget.
- Smoke test on `file://` and HTTP for both locales.
- Documentation: README, plan, runbook, changelog, data dictionary.
- Local release only; no remote, push or Pages.

**Acceptance**

- `build_all.py` and `--check` pass.
- `smoke_site.py` passes EN and ID, desktop and mobile.
- Zero critical accessibility issues; zero external requests.
- Payload within budget; 0 broken Markdown links.
- Release notes and hand-off are complete.

### Work breakdown

| Workstream | Releases | Estimate |
|---|---|---:|
| Data reconciliation and imports | 4.1, 4.2, 4.5 | 8–10 weeks |
| Translation and review | 4.0, 4.4 | 3–4 weeks |
| Design system and UX | 4.0, 4.3 | 4–5 weeks |
| Front-end build | 4.0, 4.3, 4.4 | 6–8 weeks |
| QA, accessibility, performance | 4.3, 4.5 | 2–3 weeks |

### Definition of done

A record is done when:

- It has EN/ID names and summaries.
- It has a status, status date and status basis.
- It has coordinates or an explicit no-geometry note.
- It has at least one claim and one source.
- It has a programme and at least one organisation role.
- It passes validation and appears in the search index.
- It has a coverage tier and a last-verified date.

---

## 9. Metrics

### Data

- PSN coverage: 226/226 active projects and 24/24 programmes, or documented
  exclusions.
- Project count: 400+.
- Claims: 1,500+, with 90% of projects at 2+ claims.
- Sources: 250+; 80% Tier A/B.
- Freshness: 90% of rows verified in the last six months.
- Conflicts: 100% with both sources; open conflicts visible.
- Estates: 200+; 80% better than regency precision.

### Experience

- Task success for "find a project", "compare two projects", "export filtered
  data" and "find the source for a claim".
- Time on task; error rate; SUS or UMUX-Lite.
- Search zero-result rate.
- Mobile task success.

### Accessibility

- WCAG 2.2 AA audit: zero critical issues.
- Keyboard-only completion of primary tasks.
- Contrast and target-size checks.
- Screen-reader spot check on Explore, project detail and Data.

### Performance

- Initial payload < 1.5 MB; total < 5 MB.
- First contentful paint < 1.5 s on a local server.
- Map interaction < 100 ms for filter changes.
- No external requests; works from `file://`.

### Bilingual

- 100% UI key coverage.
- 100% required entity translation coverage.
- Zero fallback keys in production.
- Native review of the glossary and programme names.
- EN/ID layout parity at three widths.

### Trust

- Every project has a source and a date.
- Every status change has an official source or two independent sources.
- Conflicts are recorded, not hidden.
- The Data view states what is missing.

---

## 10. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data collection is larger than expected | High | High | Tiered records; PSN first; 226 target, not 1,000 |
| Official sources are blocked or change | Medium | High | Snapshot to `data/raw/`; use archives; multiple sources |
| Translation drift and poor quality | High | Medium | Glossary, build checks, native review, status field |
| Payload growth breaks `file://` | High | High | Per-view bundles, compact arrays, payload budget |
| Map performance at 400+ markers | Medium | Medium | Canvas, clustering, simplification, lazy details |
| Duplicate or conflicting records | High | Medium | Stable IDs, aliases, phases, reconciliation ledger |
| Scope creep into real-time tracking | Medium | High | Non-goals; monthly refresh, not live |
| Political sensitivity | Medium | Medium | Neutral language, source every claim, no predictions |
| Licensing and copyright | Medium | Medium | Record licences; link, do not republish; credit |
| Translation of proper names | Medium | Low | Keep Indonesian names; gloss only on first use |

---

## 11. Immediate next actions

1. **Freeze scope.** **Done (9 Nov 2026).** The target is 226 active PSN
   projects plus 24 active programmes, inside the 400-record cap. The counts
   are in `coverage_targets.csv` and this plan.
2. **Snapshot the sources.** **Partly done (9 Nov 2026).** Permenko 16/2025 and
   Permenko 4/2026 are in `data/raw/2026-11-09/` with SHA-256 hashes in
   `sources.csv`. The RPJMN, KPPIP sector pages, budget speeches and KEK list
   still need filing.
3. **Build the PSN reconciliation ledger.** **Done (9 Nov 2026).**
   `data/curated/psn_register.csv` holds 253 rows (226 active projects, 24
   active programmes, 3 deleted slots). `data/derived/psn_reconciliation.csv`
   records 79 direct project matches, 8 aggregate matches, 7 partial matches,
   26 estate matches, 24 programme matches, 88 missing projects and 18 missing
   estates. The build fails if the register loses its official count.
4. **Pilot IKN and the 2026 flagships.** **Done (9 Nov 2026).** Added 24
   records: IKN Phase 2, Nusantara airport, Masela, RDMP Balikpapan, 100 GWp
   phase 1, the 13 stage II projects, five dams and the Giant Java Sea Wall, with
   14 sources, 77 claims and 22 events. See Appendix G.
5. **Complete the PSN road set.** **Done (9 Nov 2026).** Added nine rows for the
   remaining PSN road entries and matched three more to existing rows. Roads are
   now 50/50. See Appendix G.
6. **Add the programme layer.** **Done (9 Nov 2026).** Added `programmes.csv`,
   `programme_projects.csv` and `programme_sources.csv`, all 24 active
   programmes with bilingual names and summaries, 10 lead organisations, 7
   structural project links and 48 claims. The programme view, Data section,
   downloads and ledger all use the new layer. See Appendix G.
7. **Add the first PSN industrial-area batch.** **Done (9 Nov 2026).** Added
   eight estates (Kuala Tanjung, Bantaeng, Pomalaa, Huali, Patimban, NEMIE,
   Pulau Penebang and Alumina Toba) with 11 sources, 8 organisations and 41
   claims. Industrial coverage rose to 26/44. See Appendix G.
8. **Close the remaining PSN records at Tier C.** **Done (9 Nov 2026).** Added
   88 register-only projects and 18 register-only industrial areas with PSN,
   location and active-designation claims. PSN coverage is 226/226 and 44/44;
   no PSN record remains. See Appendix G.
9. **Prototype the bilingual shell.** **Done (9 Nov 2026).** `site/index.html`
   chooser, `site/en/`, `site/id/`, 635 UI keys per locale, `translations.csv`,
   `build_i18n.py`, `build_locales.py`, `Intl` formatting, language switch and
   `hreflang`. The smoke test covers EN and ID on `file://` and HTTP.
10. **Run the UX audit.** **Partial (9 Nov 2026).** Expert heuristic walkthrough
    and an automated five-profile rehearsal are documented; five external users
    and the time baseline are still open.
11. **Design the map palette and tokens.** **Done (9 Nov 2026).**
    `docs/design/style-tile.html`, `docs/design/tokens-v4.md` and
    `scripts/dev/check_contrast.py`.
12. **Extend the schema.** **Done (9 Nov 2026).** Programmes, translations,
    indicators, indicator values and project phases are in with validation and
    dictionary entries. Geometry remains an empty table until a sourced line or
    polygon is added; the migration note is in the changelog and runbook.
13. **Build the Data dashboard prototype.** **Partial (9 Nov 2026).** Full-width
    coverage, native sector/status/freshness charts, freshness, claims,
    conflicts, sources, downloads and methods are in. A sortable table component
    remains.
14. **Write the acceptance tests.** **Done (9 Nov 2026).** Payload budget, i18n
    coverage, catalogue parity, both locales, keyboard path, `file://` and HTTP
    are in the build or the browser smoke test.

---

## Appendix A — Current data model (v4 programme layer)

The current curated tables are:

```
projects.csv                 organizations.csv
project_organizations.csv    investments.csv
sources.csv                  project_sources.csv
project_aliases.csv          project_events.csv
project_geometry.csv         laws.csv
project_laws.csv             corridors.csv
corridor_segments.csv        estates.csv
estate_sources.csv           coverage_targets.csv
conflicts.csv                psn_register.csv
programmes.csv               programme_projects.csv
programme_sources.csv        translations.csv
pkpn_programmes.csv          pkpn_sources.csv
indicators.csv               indicator_values.csv
project_phases.csv
```

Generated outputs:

```
data/exports/projects.csv
data/derived/factories_2026.csv
data/derived/freshness_report.csv
data/derived/i18n_report.csv
data/derived/claims_audit.csv
data/derived/data_dictionary.csv
data/derived/psn_reconciliation.csv
site/data/basemap.js
site/data/corridors.js
site/data/estates.js
site/data/programmes.js
site/data/projects.js
site/data/search.js
site/data/stats.js
site/downloads/*.csv, *.json, *.geojson
```

The v4 build passes with 251 projects, 24 programmes, 204 estates, 111
organisations, 138 sources, 5 corridors, 44 segments, 34 events, 26 investments,
19 conflicts, 917 project claims, 115 estate claims, 48 programme claims, 8
PKPN programmes with 27 claims, 14 indicators, 4 indicator values, 9 project
phases and 286 dictionary fields across 28 tables. The initial payload is
1,217 KB, the data payload is 1,753 KB and the total including downloads is
3,876 KB. The two locale pages, the chooser
and both i18n payloads are generated and checked by the build.

## Appendix B — Source register (V4 starter)

| Source | URL / access | Use | Caveat |
|---|---|---|---|
| KPPIP PSN pages | `kppip.go.id/proyek-strategis-nasional/` | PSN project lists by sector | Site intermittently unreachable; use archive |
| Permenko 16/2025 | `peraturan.go.id/files/permenko-perekonomian-no-16-tahun-2025.pdf` | 226 active projects and 24 active programmes; full annex | Snapshot in `data/raw/2026-11-09/`; 2 project slots and 1 programme slot are deleted |
| Permenko 4/2026 | `peraturan.bpk.go.id/Download/418980/2026PermenkoEkon004.pdf` | Ninth amendment to the PSN list | Amends the smelter programme only; it does not change the 226-project list |
| RPJMN 2025–2029 | Bappenas | National targets and PKPN | Bappenas blocks some requests; use archive |
| Setkab releases | `setkab.go.id` | Groundbreakings, inaugurations, delivery stats | Official but political framing |
| PU | `pu.go.id` | Roads, dams, irrigation, water | Project pages vary |
| BPJT | `bpjt.pu.go.id` | Toll road status, km, operator | API and page data disagree |
| Kemenhub | `kemenhub.go.id` | Rail, ports, airports | PDFs and decks |
| ESDM | `esdm.go.id` | Energy projects, RUPTL | Capacity and COD change |
| KEK Secretariat | `kek.go.id` | 25 SEZs, incentives | Some pages are JS-rendered |
| Kemenperin | `kemenperin.go.id` | Industrial estates | Reachable on 9 November 2026; earlier runs saw 502 errors |
| Danantara | `danantaraindonesia.co.id` | Portfolio, DDMF | Limited project detail |
| IKN Authority | `ikn.go.id` | IKN packages | 403 to some clients |
| Company reports | IDX, annual reports | Capex, capacity, sponsors | Self-reported |
| World Bank / ADB / AIIB / JICA | Project documents | Financing, safeguards | Lagging |
| Wikipedia | `en.wikipedia.org` / `id.wikipedia.org` | Discovery only | Not a primary source |
| OpenStreetMap | Overpass / extracts | Geometry | ODbL; cross-check |
| Natural Earth | `naturalearthdata.com` | Basemap | Public domain |
| BIG Satu Peta | `kspservices.big.go.id` | Boundaries, infrastructure | Service limits |

## Appendix C — Research notes

- Permenko 16/2025 sets **226 active projects and 24 active programmes**. The
  annex keeps 228 project numbers and 25 programme numbers; project 112
  (Kawasan Industri), project 226 (Sektor Pariwisata) and programme 6 are
  marked deleted. Total investment is reported at Rp 6,491 trillion.
- The reconciliation ledger represents **226 of 226 active PSN project or estate
  records**: 94 records map to 88 reviewed project rows, 26 map to reviewed
  estates, 88 are register-only project rows and 18 are register-only industrial
  areas, and **all 24 programmes** are recorded. **No PSN record remains.**
  Roads (50/50), airports (7/7), ports (15/15), railways (13/13), coastal defence
  (1/1), industrial areas (44/44), dams and irrigation (57/57), water and
  sanitation (9/9), energy (18/18), technology (6/6), housing (2/2), agriculture
  (2/2), education (1/1) and tourism (1/1) are complete.
- The register-only layer is deliberately Tier C. Permenko 16/2025 supports the
  official name, PSN number, sector, location and active status only. The atlas
  does not infer implementation status, cost, capacity, developer, area or
  boundary. Province centroids are used for the record layer and those points are
  excluded from the map.
- KPPIP's road page lists **54 entries**; the atlas now has **54 road rows** and
  matches all **50 PSN road entries** in the Permenko 16/2025 annex. The 12
  entries initially missing are resolved: nine new rows (Kisaran–Tebing Tinggi,
  Jambi–Rengat, Rengat–Pekanbaru, Serpong–Cinere, Cimanggis–Cibitung, Teluk
  Lamong, Patimban access, New Priok Eastern Access and the Bandung inner-city
  toll roads) plus three aggregate or partial matches to existing rows.
- The 2027 budget speech lists eight PKPN: food sovereignty; energy and water
  independence; education; health; downstreaming and industrialisation;
  infrastructure, housing and disaster resilience; people's economy and village
  development; and poverty reduction. The Finance Ministry breakdown adds the
  Rp820.9T education and Rp244.9T health allocations, the Rp549.9T social
  protection allocation, 10 million local entrepreneurs and the 15-segment
  Giant Sea Wall. The atlas records these as a separate PKPN layer with 27
  claims; it does not infer a full budget or target where the source is silent.
- The 100 GW solar programme was launched at Gilimanuk on 25 August 2026; the
  first phase is 17 GWp, with 30 GW targeted in 2026 and 13 GW of diesel
  retired.
- Masela LNG started on 16 July 2026: US$20.9B, 9.5 Mtpa, 35,000 bpd
  condensate, at least 60% domestic gas.
- Downstreaming stage II started on 29 April 2026: Rp 116T, 13 projects
  (5 energy, 5 mineral, 3 agriculture), including Dumai/Cilacap gasoline,
  Palaran/Biak/Maumere fuel tanks, Tanjung Enim DME, Morowali stainless steel,
  Cilegon carbon steel, Karawang Buton asphalt, Gresik copper/gold, Sei
  Mangkei oleofood/biodiesel, and two Maluku coconut/pala projects.
- IWIP started 11 nickel downstreaming projects on 8 October 2026: US$10.2B,
  4 commercial and 7 new, plus the first EV battery export.
- Five dams were inaugurated on 10 July 2026, centred on Meninting (NTB); the
  other four names still need a source check.
- The two-year delivery report (20 October 2026) is the best single source for
  outcome indicators; use it as a lead, then verify each number against the
  responsible ministry.

## Appendix D — Named backlog (starter)

This is a working list, not a claim that every item is a separate atlas row.
Some are projects, some are packages, and some are programme-level records.
Each item still needs a source, a status date and a decision about its record
type.

**Status at 9 November 2026:** all 226 active PSN project or estate records,
all 24 active programmes, all 35 transport PSN entries and all 50 PSN road
entries are represented. The remaining items below are strategic non-PSN
records, Tier C upgrades or programme-level gaps.

**Roads and bridges**

- PSN roads: all 50 entries are represented. The 12 that were initially missing
  were added or matched: Kisaran-Tebing Tinggi; Bukittinggi-Padang Panjang-
  Lubuk Alung-Padang; Pekanbaru-Bangkinang-Payakumbuh-Bukittinggi;
  Tebing Tinggi-Pematang Siantar-Parapat-Tarutung-Sibolga; Jambi-Rengat;
  Rengat-Pekanbaru; Serpong-Cinere; Cimanggis-Cibitung; Teluk Lamong
  flyover; Patimban access; New Priok Eastern Access; Bandung inner-city
  toll roads.
- Strategic pipeline: JORR 3, Demak–Tuban, Pejagan/Tegal–Cilacap,
  Cilacap–Yogyakarta, Gilimanuk–Mengwi, Semarang Harbour.
- National road programme: 1,151 km of regional roads, 2,228 km of Inpres
  roads, 3,500 bridges.

**Rail**

- MRT Jakarta N–S Phase 2A (Bundaran HI–Ancol) and Phase 2B; MRT East–West.
- LRT Jakarta Phase 1B (Velodrome–Manggarai); LRT Jabodebek; LRT Palembang.
- Jakarta–Bandung high-speed rail (Whoosh) and the Surabaya extension study.
- Trans Sulawesi rail (Makassar–Parepare and extensions); Kalimantan logistics
  rail; Rantau Prapat–Kota Pinang; Lahat–Kertapati; Tebing Tinggi–Kuala
  Tanjung; Yogyakarta airport rail.
- Station revitalisation: Semarang Tawang, Gambir, and level-crossing works.

**Airports**

- Nusantara International Airport (IKN); North Bali International Airport;
  Kertajati; Soekarno–Hatta expansion; Komodo; Lombok Praya; Yogyakarta
  International Airport; Kediri/Dhoho; Nabire; Siboru Fakfak; Karimun.

**Seaports and ferries**

- Patimban phases; Kuala Tanjung; Bitung; Makassar New Port; Benoa; Kijing;
  Sorong; Kupang; Teluk Palu; Likupang; Sanur; Maloy; New Palembang; Muaro
  Jambi; fishing ports and RoRo links.

**Energy**

- Masela Abadi LNG; Tangguh Train 3; Jambaran–Tiung Biru; IDD; RDMP
  Balikpapan, Cilacap, Dumai and Balongan; GRR Tuban and Bontang.
- 100 GW PLTS phase 1 (17 GWp) and the 30 GW 2026 build; 13 GW diesel
  retirement; village 1 MW solar.
- 37 electricity projects (26 generators, 3.2 GW; 11 transmission packages).
- Sumatra 500 kV; Central–West Java 500 kV; geothermal (Hululais, Rajabasa);
  Batang Toru hydro; waste-to-energy in eight cities; gas plants in 18
  provinces; B50 biodiesel.

**Water, sanitation and flood control**

- Five dams inaugurated in July 2026 (Meninting plus four to verify); the PSN
  dam portfolio; 9,000 km of irrigation; 3,000 boreholes.
- Jakarta sewerage; SPAM Jatiluhur, Lampung and Semarang Barat; regional water
  supply; the 15-segment Java sea wall; Jakarta flood control.

**Industry and downstreaming**

- Stage II: Dumai and Cilacap gasoline; Palaran, Biak and Maumere fuel tanks;
  Tanjung Enim DME; Morowali stainless steel; Cilegon carbon steel; Karawang
  Buton asphalt; Gresik copper/gold; Sei Mangkei oleofood/biodiesel; Maluku
  pala oleoresin; Maluku integrated coconut.
- IWIP: nickel battery materials, precursor, EV battery, separator,
  electrolyte, aluminium, electric heavy equipment, photovoltaic glass.
- Existing and pipeline: Freeport Manyar, Amman, Vale HPAL, CATL-CBL, Lotte
  LINE, Chandra Asri, OKI pulp, Pupuk Kaltim, Inalum, Krakatau Steel, SGAR
  Mempawah, BTR Kendal; national car and motor ecosystem.

**Social infrastructure**

- 441 RSUD; 10,000 puskesmas; 514 Labkesmas; 66 hospitals in 3T regions.
- 265 Sekolah Rakyat; school renovation; 288,180 interactive screens; SMA
  Taruna Nusantara campuses.
- Three million houses; 62,000 KPR; 400,000 repaired houses.
- Free Nutritious Meals (MBG) kitchens and programme indicators.

**Digital, tourism and fisheries**

- Palapa Ring; Satria; data centres; 5G; government cloud and AI.
- Five super-priority tourism destinations and KEK tourism.
- 1,386 fishing villages; BUBK; cold chain; 1,582 modern boats; fish ports.

**Companies to model first**

- Danantara: Bank Mandiri, BNI, BRI, MIND ID, Pertamina, PLN, Telkom.
- Infrastructure: Hutama Karya, Jasa Marga, Pelindo, Angkasa Pura, KAI, MRT
  Jakarta, KCIC, Waskita, Wijaya Karya, PP, Adhi, Brantas Abipraya.
- Industry: Krakatau Steel, Pupuk Indonesia, Semen Indonesia, Inalum, Antam,
  Vale Indonesia, Freeport Indonesia.
- Private and foreign: Salim, Sinar Mas, Djarum, Lippo, Agung Sedayu, Astra,
  Adaro, Harita, Merdeka Copper Gold, Amman, Tsingshan, CATL, Lotte, Chandra
  Asri.

## Appendix E — V1–V3 history

The v1–v3 work is recorded in:

- [`plan-v3.md`](plan-v3.md) — the three-phase overhaul backlog.
- [`../phases/phase-1-decisions.md`](../phases/phase-1-decisions.md) — design,
  scope, schema and payload budgets.
- [`../phases/phase-2-transport.md`](../phases/phase-2-transport.md),
  [`../phases/phase-2-estates.md`](../phases/phase-2-estates.md),
  [`../phases/phase-2-factories.md`](../phases/phase-2-factories.md),
  [`../phases/phase-2-roads.md`](../phases/phase-2-roads.md) — data batches.
- [`../phases/phase-3-trust.md`](../phases/phase-3-trust.md) — claims,
  freshness, conflicts and the local release.
- [`../operations/refresh-runbook.md`](../operations/refresh-runbook.md) —
  monthly refresh procedure.

V4 does not invalidate that work. It reuses the curated tables, the claim
model, the deterministic build and the offline constraints. It adds the
programme, company, estate and bilingual layers on top.

## Appendix F — Open decisions

1. **English or Indonesian default at the root?** Recommendation: a chooser
   with browser-language detection, English fallback.
2. **226 PSN projects or 400 total?** Recommendation: both, in separate
   coverage targets; 226 active projects plus 24 programmes is the PSN
   reference set, 400 is the atlas cap.
3. **How much company financial data?** Recommendation: profile-level only in
   V4; no full financial statements.
4. **How many social infrastructure sites?** Recommendation: programme-level
   records plus 10–20 representative sites, not 10,000 rows.
5. **When to enable the estate map layer?** Recommendation: when 80% of rows
   have better than regency-centroid precision.
6. **When to publish?** Only when the repository owner asks. V4 remains local.

## Appendix G — Execution log

| Date | Increment | Evidence |
|---|---|---|
| 2026-11-09 | Official PSN register and reconciliation | `data/raw/2026-11-09/permenko_16_2025.pdf`, `permenko_4_2026.pdf` and the parsed text; `data/curated/psn_register.csv` (253 rows); `data/derived/psn_reconciliation.csv` (253 rows); new `scripts/pipeline/build_psn_ledger.py` step in `build_all.py`; 200-field dictionary across 19 tables. |
| 2026-11-09 | 2026 flagship batch | 24 new project rows in `projects.csv`, 14 sources, 11 organisations, 77 claims, 4 investments and 22 events. New sectors: energy, water, urban and coastal. `scripts/imports/add_flagships.py` is idempotent. |
| 2026-11-09 | PSN road completion | 9 new project rows in `projects.csv`, 17 sources, 2 organisations, 43 claims, 4 investments and 2 events. Three existing rows absorb PSN 10, 11 and 12 as aggregate or partial matches. `scripts/imports/add_psn_backlog_roads.py` is idempotent. |
| 2026-11-09 | PSN programme layer | `programmes.csv` (24 rows), `programme_projects.csv` (7 links) and `programme_sources.csv` (48 claims); 10 lead organisations. Bilingual names and summaries; programme view, Data section and three downloads. Dictionary grows to 229 fields across 22 tables. `scripts/imports/add_psn_programmes.py` is idempotent. |
| 2026-11-09 | PSN industrial-area batch | 8 estate rows (Kuala Tanjung, Bantaeng, Pomalaa, Huali, Patimban, NEMIE, Pulau Penebang, Alumina Toba), 11 sources, 8 organisations and 41 claims. `estates.csv` grows to 186 rows; `sources.csv` to 133. PSN industrial coverage rises from 18/44 to 26/44. `scripts/imports/add_psn_industrial_estates.py` is idempotent. |
| 2026-11-09 | PSN register-only closure | 88 project rows and 18 industrial-area rows, 264 project claims and 54 estate claims, 88 official-name aliases, 5 new sectors and an `unknown` status. `projects.csv` grows to 228 rows, `estates.csv` to 204, project claims to 863 and estate claims to 115. PSN coverage is 226/226 and 44/44. `scripts/imports/add_psn_register_records.py` is idempotent; `scripts/tools/build_province_centroids.py` supplies province centroids. |
| 2026-11-09 | Bilingual shell | `site/en/index.html`, `site/id/index.html` and `site/index.html`; 634 UI keys per locale; `data/curated/translations.csv`; `build_i18n.py`, `build_locales.py`, `assets/i18n.js`; 24 programme and 5 corridor translations; 228 project names (140 reviewed + 88 official); 228 generated summaries; both locales smoke-tested on `file://` and HTTP. |
| 2026-11-09 | Full-width registers and UX baseline | Data, Programmes, Corridors and Estates use the full content width; tap-to-expand mobile sheet; `docs/design/tokens-v4.md`, `style-tile.html`, `ux-audit-v4.md`; 19 contrast pairs pass; 20/20 automated task steps across five profiles; 238-field dictionary across 23 tables. |
| 2026-11-09 | PKPN layer | `pkpn_programmes.csv` (8 rows with bilingual summaries, targets, budgets and sources), `pkpn_sources.csv` (27 claims), 11 PKPN indicators and one value. Source snapshots `setneg_rapbn_2027.html` and `kemenkeu_pkpn_2027.html`. Programme view adds eight PKPN cards in speech order; Data adds two downloads. Sources 135; dictionary 286 fields across 28 tables; initial payload 1,150 KB, total 3,677 KB. |
| 2026-11-09 | Data charts | Native sector, status and freshness charts on the full-width Data view. Sector bars cover all 14 sectors; the status and freshness stacks reuse the existing status colours. No chart library; 634 UI keys per locale. |
| 2026-11-09 | Companies view | `companies.js` from 101 organisations and 203 project-role links; full-width Companies view with type filter, role search, expandable role list, filtered CSV, two downloads and a coverage row (101/300). 79 organisations have a link; 22 are reference-only. Initial payload 1,150 KB, data 1,667 KB, total 3,634 KB. |
| 2026-11-09 | Indicators, values and phases | `indicators.csv` (3), `indicator_values.csv` (3) and `project_phases.csv` (9), with validation, dictionary entries, project/programme payloads, three downloads and a Programme target-vs-current view. The 100 GWp programme target is 100 GWp against 5.3 GWp current; Phase 1 targets 17 GWp; Nusantara's runway is 3,000 m. Dictionary 268 fields across 26 tables; initial payload 1,099 KB, total 3,428 KB. |

**Reconciliation result at 9 November 2026:** 226 of 226 active PSN project or
estate records represented: 94 records map to 88 reviewed project rows, 26 map to
reviewed estates, 88 are register-only project rows and 18 are register-only
industrial areas; all 24 programmes are recorded. No PSN record remains. Every
sector is complete. The build now fails if the register does not contain exactly
226 active projects, 24 active programmes and 3 deleted slots.
