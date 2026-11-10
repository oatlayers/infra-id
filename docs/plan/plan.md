# Indonesia Infrastructure Atlas — Remaining Work

**Status:** V4 in progress. Local-only build; nothing is published.
**Baseline data:** 10 November 2026 build.
**Scope of this file:** remaining work only. Completed work is recorded in
[`CHANGELOG.md`](../../CHANGELOG.md), the phase records in
[`docs/phases/`](../phases/), and git history.

## 1. Definition of done

V4 is complete when:

1. The reference set reaches **400 records**: 226 active PSN project or estate
   records plus 174 strategic and private records.
2. The atlas has **300 company profiles**, **250 archived sources** and
   **300 sourced indicators**.
3. IKN package coverage reaches **25 of 25** and every other coverage target in
   `data/curated/coverage_targets.csv` is met or explicitly marked blocked.
4. Every project has a status source and an atomic claim for each populated
   numeric fact. Register-only rows remain visibly labelled.
5. English and Indonesian editions have full UI parity, reviewed entity names,
   and no untranslated chrome.
6. The UX backlog in section 5 is complete and the five-user study has been run.
7. `build_all.py`, `build_all.py --check`, the browser smoke test, the
   five-profile rehearsal, the contrast check and the Markdown link check pass.
8. The build remains offline: no remote, push, Pages deployment or published URL.

## 2. Current baseline

| Measure | Current |
|---|---:|
| Project rows | 252 |
| PSN project/estate records represented | 226 / 226 |
| PSN programmes represented | 24 / 24 |
| PKPN programmes | 8 / 8 |
| Estates | 204 |
| Companies and agencies | 112 |
| Sources | 140 |
| Indicators / dated values / phases | 45 / 28 / 9 |
| IKN package rows | 25 / 25 |
| Project claims / estate claims | 921 / 115 |
| Programme claims / PKPN claims | 48 / 27 |
| Events | 35 |
| Data dictionary | 286 fields across 28 tables |
| Initial / data / total payload | 1,225 / 1,795 / 3,937 KB |

### Reference-set accounting

The 226 active PSN records are fully represented: 182 matches sit on 174
project rows (86 reviewed rows and 88 register-only rows) and 44 records are
estate rows. Fifteen PSN records are aggregate or partial matches to an existing
row, so the number of matches is higher than the number of rows.

The 400-record target is therefore **226 PSN records + 174 strategic/private
records**, not 400 project-table rows. The atlas currently has 78 strategic
records, so **96 strategic records remain**. The project table will grow to
about 348 rows when those records are added; 44 PSN records live in the estate
layer and eight PSN records share an existing project row, so 400 reference
records correspond to about 392 rows.

## 3. Coverage gaps

| Layer | Current | Target | Remaining |
|---|---:|---:|---:|
| PSN project/estate records | 226 | 226 | 0 |
| PSN programmes | 24 | 24 | 0 |
| Strategic/private records | 78 | 174 | **96** |
| Companies and agencies | 112 | 300 | **188** |
| Sources | 140 | 250 | **110** |
| Indicators | 45 | 300 | **255** |
| IKN package rows | 25 | 25 | 0 |
| Factories | 34 | 34 | 0 |
| Industrial estates | 204 | 197 | 0 |
| Roads | 56 | 54 | 0 |
| Railways, airports, seaports, transport PSN | 13 / 8 / 15 / 35 | met | 0 |

The Data view renders these numbers from `site/data/stats.js`. Update
`coverage_targets.csv` only when a target is genuinely met.

## 4. Data workstreams

### 4.1 Strategic and private records — 97 records

Add sourced records outside the PSN list. Search `projects.csv`,
`psn_register.csv` and `estates.csv` first; upgrade an existing row instead of
creating a duplicate.

Candidate areas, in rough priority order:

- **Roads and bridges:** JORR 3, Demak–Tuban, Pejagan/Tegal–Cilacap,
  Cilacap–Yogyakarta, Gilimanuk–Mengwi, Semarang Harbour, strategic regional
  roads and bridges.
- **Rail:** MRT Jakarta Phase 2A and 2B, MRT East–West, LRT Jakarta Phase 1B,
  Jakarta–Bandung high-speed rail extension study, Trans Sulawesi rail,
  Kalimantan logistics rail, Yogyakarta airport rail, station revitalisation.
- **Airports:** North Bali, Kertajati, Soekarno–Hatta expansion, Komodo, Lombok
  Praya, Yogyakarta International, Kediri/Dhoho, Nabire, Siboru Fakfak, Karimun.
- **Seaports and ferries:** remaining Patimban phases, Makassar New Port,
  Kijing, Sorong, Kupang, Teluk Palu, Likupang, Sanur, Maloy, New Palembang,
  Muaro Jambi, fishing ports and RoRo links.
- **Energy:** Tangguh Train 3, Jambaran–Tiung Biru, IDD, RDMP Cilacap, Dumai and
  Balongan, GRR Tuban and Bontang, the 37 electricity projects, Sumatra 500 kV,
  Central–West Java 500 kV, geothermal, Batang Toru, waste-to-energy, gas plants
  and B50 biodiesel.
- **Water and flood control:** Jakarta sewerage, SPAM Jatiluhur, Lampung and
  Semarang Barat, regional water supply and Jakarta flood control.
- **Industry and downstreaming:** remaining Hilirisasi Stage II projects, IWIP
  battery-material packages, CATL-CBL and the national car and motor ecosystem.
- **Social infrastructure:** representative schools, hospitals, housing and
  free-meal kitchens at programme level; do not create 10,000 facility rows.
- **Digital, tourism and fisheries:** Palapa Ring, Satria, data centres, 5G,
  government cloud and AI, the five super-priority destinations, fishing
  villages, cold chain and fish ports.

Acceptance for each record:

- a stable lowercase hyphenated `id`;
- source row with a dated snapshot or an explicit URL-only note;
- status, location and at least one atomic claim;
- bilingual display name and generated summary;
- no duplicate of a PSN, estate or existing project record;
- updated coverage count and changelog entry.

### 4.2 Companies and agencies — 189 profiles

Add profiles from existing project sources before adding new projects. Priorities:

- **Danantara holdings:** Bank Mandiri, BNI, BRI, MIND ID, Pertamina, PLN, Telkom.
- **Infrastructure SOEs:** Hutama Karya, Jasa Marga, Pelindo, Angkasa Pura, KAI,
  MRT Jakarta, KCIC, Waskita, Wijaya Karya, PP, Adhi, Brantas Abipraya.
- **Industry SOEs:** Krakatau Steel, Pupuk Indonesia, Semen Indonesia, Inalum,
  Antam, Vale Indonesia, Freeport Indonesia.
- **Private and foreign groups:** Salim, Sinar Mas, Djarum, Lippo, Agung Sedayu,
  Astra, Adaro, Harita, Merdeka Copper Gold, Amman, Tsingshan, CATL, Lotte,
  Chandra Asri.

Acceptance:

- `organizations.csv` row with `org_type`, country and website where sourced;
- at least one `project_organizations.csv` role where the source names a role;
- no duplicate organisation names or aliases;
- 22 reference-only profiles gain a sourced role where possible;
- 100 projects that currently have no organisation role are reviewed.

### 4.3 Sources — 110 documents

Priority order:

1. RPJMN 2025–2029 and the current Bappenas planning documents.
2. KPPIP sector pages for transport, energy, water and industry.
3. Budget speeches and Finance Ministry breakdowns beyond the two PKPN
   snapshots already archived.
4. Official delivery reports for education, health, housing, energy and water.
5. Company annual reports and project disclosures for the strategic records.
6. Missing archives for flagship and road sources currently registered by URL.

Every new source needs publisher, title, URL, publication date, retrieval date,
source type, language, snapshot hash and archive path. If a page cannot be
archived, record why in `notes`.

### 4.4 Indicators — 265 indicators

Add an indicator only when the source states the name, unit and at least one of:
a baseline, a target or a dated observation. Never infer a target from the
atlas's own fields.

Priority order:

1. Project-level output indicators for IKN, flagships, transport and industry.
2. Ministry baselines and delivery values for education, health, housing, water
   and energy.
3. PKPN delivery values where a dated official release exists.
4. Programme targets only where the source states them.

Rules:

- Record a range as the stated bound and name the bound in `notes`.
- Record "more than X" as X and mark it as a lower bound.
- Do not copy a completion year from a different measure.
- Link every indicator to a programme, a project, or both.
- Add dated observations to `indicator_values.csv` with their own source.

### 4.5 IKN package 25 of 25 — complete

The 25th row is PT Berdikari (Persero)'s integrated chicken downstreaming
facility in Wilayah Perencanaan 3, named in the 14 October 2026 OIKN signing
and reported by JournalArta on 8 November 2026. It is a private investment,
not an OIKN construction package; the row is labelled accordingly. No package
total is split across rows. The IKN Authority site still returns HTTP 403 to
some clients, so the archived secondary report remains the available source.

## 5. UX workstream

| Pri | Item | Acceptance |
|---|---|---|
| P0 | Bilingual gaps | Coverage `reference_set`, download labels and metadata, dictionary descriptions and any new entity text are translated. Proper names and sourced English stay tagged `EN`. |
| P1 | Editorial summaries | Replace the generated `AUTO` / `OTOMATIS` text for flagships and high-traffic rows with reviewed bilingual summaries; keep the generated text for the long tail. |
| P1 | Mobile bottom navigation | Five-item bottom bar with a `More` item; full-screen filter sheet; 320 px and 390 px with no horizontal overflow. |
| P1 | Project and entity detail pages | Shareable hash routes for projects, programmes and companies, printable and keyboard accessible; the drawer remains the quick view. |
| P1 | Map v3 | Clustering or canvas rendering for 400+ markers, layer toggles, list↔map hover/focus linking, map-only mode and a collapsible rail. Measure frame rate at 300+ markers. |
| P2 | Data table | A general sortable table component and column chooser across Data tables; keep the coverage table's `aria-sort` behaviour. |
| P2 | Search | Fuzzy ranking and arrow-key navigation through grouped results. |
| P2 | Type scale | Complete the 14–16 px body and 12–13 px caption scale across every register view. |
| P2 | Table semantics and print | Captions, scoped headers and a print stylesheet for project and Data pages. |
| P3 | Geometry | Source corridor lines and estate polygons; keep unsourced geometry empty. |

## 6. Trust and evidence

- Run the five-user study in
  [`docs/design/ux-audit-v4.md`](../design/ux-audit-v4.md#6-five-user-protocol-open).
  Record task success, time on task, SEQ and verbatim notes without personal
  data. This is blocked until five external participants are available.
- Resolve or document the eight open conflicts. Do not pick a winner silently.
- Complete the missing official snapshots listed in section 4.3.
- Refresh rows through the monthly procedure in
  [`docs/operations/refresh-runbook.md`](../operations/refresh-runbook.md).
- Add the seven named 2024 estate additions and upgrade the 18 register-only PSN
  industrial areas with a sourced area, developer, status and boundary where
  possible.
- Geocode the remaining large estates and review the 12 PSN road rows with
  `psn=unknown`.

## 7. Priority order

1. **P0 — measurable coverage:** strategic records, companies, sources and
   indicators. IKN package coverage is complete at 25/25.
2. **P0 — bilingual completion and five-user study.**
3. **P1 — UX rebuild:** bottom navigation, detail pages, map v3, editorial
   summaries.
4. **P2 — Data and search polish:** column chooser, fuzzy ranking, type scale,
   table semantics, print.
5. **P3 — optional geometry and estate verification.**

## 8. Blockers and source gaps

| Blocker | Effect | Workaround |
|---|---|---|
| Five external UX participants unavailable | Human task-success baseline cannot be claimed | Keep the automated five-profile rehearsal as current evidence |
| IKN Authority returns HTTP 403 | Cannot cite the primary page directly | Use the archived Top Konstruksi and JournalArta reports of the same OIKN evaluations |
| KPPIP and Bappenas access intermittent | Some sector pages are unarchived | Retry, or use an official ministry mirror and record the substitution |
| RPJMN 2025–2029 not archived | Planning baseline is incomplete | Fetch and hash the official Bappenas document |
| Dishub Sanggau page returns HTTP 500 | Alumina Toba lacks that source | Use GEM and Kemenperin archives already filed |
| Some flagship and road sources are URL-only | Weaker provenance | Archive the page or record why it cannot be archived |

## 9. Invariants

- `data/curated/` is the source of truth. Never hand-edit `data/exports/`,
  `site/data/` or `site/downloads/`.
- Raw snapshots in `data/raw/` are never edited.
- One atomic fact per source claim. Comma-separated claims are rejected.
- No invented status, cost, capacity, target or date.
- PSN matching stays explicit in `data/derived/psn_reconciliation.csv`.
  Register-only records stay visible and labelled.
- Use "reference set", not "universe".
- Every new record needs a source, a status date and a verification level.
- Both locales must be updated together.
- The build is deterministic and offline. No `fetch`, CDN or remote tile server.
- The release is local only. Do not create a remote, push, deploy or publish.

## 10. Verification

Run from the repository root:

```bash
python scripts/build_all.py
python scripts/build_all.py --check
python scripts/pipeline/check_site.py
python scripts/dev/smoke_site.py
python scripts/dev/ux_rehearsal.py
python scripts/dev/check_contrast.py
```

Also run the Markdown link check described in the repository README. A change is
complete only when the build is deterministic, the smoke tests pass in both
locales, and the coverage table, dictionary and changelog reflect the change.

## 11. Out of scope

- A live, real-time project tracker.
- An exhaustive list of every Indonesian infrastructure asset.
- Full financial statements for companies.
- Ten-thousand-row facility lists; social infrastructure stays at programme
  level plus representative sites.
- Publishing or deployment.
- Additional interface languages beyond English and Indonesian.
