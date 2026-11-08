# Phase 2 — Roads and Corridors

**Date:** 8 November 2026
**Status:** Track 2D complete except R6 geometry, which is deferred and recorded
as a gap. Roads meet the 45-corridor target; five corridors publish totals and
three publish a progress series.
**Primary source:** BPJT toll-road list API, snapshot 6 November 2026
(`data/raw/2026-11-06/bpjt_toll_road_list.json`).
**Importer:** `scripts/imports/add_bpjt_psn_roads.py` for the 15 PSN corridors; the
three planned 0-km concessions and the corridor tables are curated directly.

## 1. Road coverage

The curated batch had 27 toll corridors. Track 2D added:

- **15 PSN toll corridors** from the BPJT snapshot (`scripts/imports/add_bpjt_psn_roads.py`);
- **3 planned Trans Sumatra 0-km concessions** from the Indonesian Wikipedia
  section list (3 October 2026): Lhokseumawe–Sigli 157 km, Langsa–Lhokseumawe
  135 km and Muara Enim–Lubuk Linggau 114.5 km.

The result is **45 road corridors** against a target of 45: 10 operating, 25
under construction and 10 planned. The flat export has **107 projects** in total.

The 15 BPJT additions and their status mapping are unchanged from the first
Track 2D pass:

| Corridor | Status | Operational / length | Opened |
|---|---|---:|---:|
| Cileunyi–Sumedang–Dawuan | operating | 61.665 / 60.1 km | 2022 |
| Cibitung–Cilincing | operating | 34.76 / 34.76 km | 2021 |
| Cengkareng–Batu Ceper–Kunciran | operating | 14.19 / 14.19 km | 2021 |
| Manado–Bitung | operating | 39.775 / 39.9 km | 2020 |
| Kunciran–Serpong | operating | 11.135 / 11.19 km | 2019 |
| Pasuruan–Probolinggo | operating | 40.375 / 39.875 km | 2019 |
| Pandaan–Malang | operating | 38.46 / 38.48 km | 2019 |
| Medan–Binjai | operating | 17.42 / 17.32 km | 2017 |
| Akses Tanjung Priok | operating | 11.4 / 11.4 km | 2017 |
| Cinere–Jagorawi | operating | 14.886 / 14.64 km | 2014 |
| Simpang Indralaya–Muara Enim | under construction | 63.5 / 119 km | — |
| Serpong–Balaraja | under construction | 9.335 / 30 km | — |
| Pekanbaru–Kandis–Dumai | under construction | 131.69 / 143.092 km | — |
| Balikpapan–Samarinda | under construction | 97.27 / 97.27 km | — |
| Ngawi–Kertosono–Kediri | under construction | 87.05 / 87.02 km | — |

## 2. Status mapping

The BPJT `status_ruas` values are not the atlas statuses. The mapping is:

- `Operasi` with at least 95% of the recorded length operational → `operating`;
- `Operasi` with a material unopened length → `under_construction`;
- `Operasi Sebagian` → `under_construction`.

This is why Pekanbaru–Kandis–Dumai is `under_construction` despite the `Operasi`
label (131.69 of 143.092 km, 92.0%), and why Balikpapan–Samarinda and
Ngawi–Kertosono–Kediri are `under_construction` despite operational figures that
match the recorded length. The conflicts are in each row's `notes`.

`opened_year` is the year of the BPJT operation decree (`sk_operasi`) for
operating rows. It is not presented as an exact opening date.

The three 0-km concessions use `status=planned`, `psn=unknown`,
`verification=single` and an approximate midpoint coordinate. They are in the
Trans Sumatra plan and are linked to `trans-sumatera`; no construction is
recorded.

## 3. The five corridors

`data/curated/corridors.csv` has five rows. The definitions and metrics are not
interchangeable, so each card shows the metric and an as-of date.

| Corridor | Definition | Metric | Total | Operational / connected | Construction | As of |
|---|---|---|---:|---:|---:|---|
| Trans Sumatra | JTTS toll backbone, Lampung–Aceh | toll operational km | 2,854 | 982 | — | 2026-08-31 |
| Trans Java | BPJT toll network, Merak–Banyuwangi, including MBZ and Gempol–Pandaan | toll operational km | 1,232.80 | 1,079.895 | 152.905 | 2026-09-07 |
| Trans Sulawesi | National road (Lintas Sulawesi), Manado–Makassar | route length; no progress series | 2,000 | — | — | 2026-11-07 |
| Trans Kalimantan | Southern national route (Poros Selatan), Aruk–Malinau | route length; no current progress series | 3,901 | — | — | 2026-07-14 |
| Trans Papua | National road, Sorong–Merauke | national road connected km | 4,330 | 3,446 | — | 2025-07-21 |

Trans Sumatra publishes 1,618 km of planned length as well as the operational
figure, leaving 254 km unallocated against the total. The note records that
Hutama Karya reports about 1,161 km built, of which 982 km is operational, and
that Bina Marga's Phase I figure is 1,051.84 km. These are different scopes and
dates; the atlas does not collapse them.

**Trans Java composite series.** 1,056.38 km across 20 sections operating by
January 2025, taken from a BPJT-attributed section list, plus 23.515 km
Gending–Paiton opened on 7 September 2026. That gives 1,079.895 km operating
against 1,232.80 km total. The remaining 152.905 km is Paiton–Besuki (26.185 km)
and Besuki–Banyuwangi (126.72 km). Paiton–Besuki is derived as 49.70 − 23.515,
while the section list prints 25.60 km; the 0.585 km discrepancy is recorded in
the corridor notes. The January 2025 article prints a 1,232.78 km total; the
section sum used here is 1,232.80 km. Older PU/Wikipedia figures of 1,167 km and
the July 2024 Kontan figure of 1,065.50 km operating use different scopes.

**Trans Sulawesi and Trans Kalimantan.** Both now publish a route total but no
current operational-km series. Trans Sulawesi uses the 2,000 km Manado–Makassar
national route from the Indonesian Wikipedia revision; the 3,900 km figure refers
to the wider Sulawesi network. Trans Kalimantan uses the 3,901 km Aruk–Malinau
southern route; competing definitions are 1,186 km (travel route), 1,920 km
(border-parallel road) and 2,100.8 km (WPS). The article says the route was
completed in 2016, but the Penajam–Balikpapan ferry crossing remains. No
percentage is estimated.

## 4. Segment tables

`data/curated/corridor_segments.csv` has **44 rows**:

| Corridor | Sections | Sum of section lengths | Share of corridor total | State |
|---|---:|---:|---:|---|
| Trans Sumatra | 13 | 1,667.306 km | 58.4% of 2,854 km | partial segment table |
| Trans Java | 23 | 1,232.80 km | 100% of 1,232.80 km | complete series |
| Trans Papua | 8 | 2,345.40 km | 54.2% of 4,330 km | partial segment table |
| Trans Sulawesi | 0 | — | — | route total only |
| Trans Kalimantan | 0 | — | — | route total only |

The Trans Java table reconciles exactly. Paiton–Besuki is 26.185 km so the
sections sum to the published total; the source's 25.60 km figure would leave a
0.585 km gap. The Trans Sumatra table covers the 13 curated sections only; the
corridor operational figure (982 km) is wider than the 516.39 km of operational
length recorded inside those section rows, because several operating sections are
not individually listed. The Trans Papua table covers the eight Papua-side
sections only; the four West Papua and Southwest Papua sections have no published
lengths.

Sections carry `segment_type`, length, status, operational/construction km,
progress, opening or target year, geometry ID and notes. No geometry is present
yet (R6).

## 5. Events

`data/curated/project_events.csv` has **six exact-dated events**:

| Date | Project | Type | Event |
|---|---|---|---|
| 2018-12-20 | Ngawi–Kertosono–Kediri | section_opened | Four East Java sections inaugurated: Ngawi–Kertosono, Jombang–Mojokerto, Gempol–Pasuruan and the Surabaya–Gempol relocation |
| 2023-10-30 | LRT Jakarta Velodrome–Manggarai | groundbreaking | Extension groundbreaking |
| 2024-10-16 | Betung–Tempino–Jambi | section_opened | 52.59 km of 170.73 km began operation |
| 2025-11-06 | Lotte LINE Cilegon | opened | Presidential inauguration; commercial operation from October 2025 |
| 2026-06-19 | GNI Morowali | stalled | Court-supervised PKPU debt suspension, not liquidation |
| 2026-09-07 | Probolinggo–Banyuwangi | section_opened | Gending–Paiton 23.515 km began operation |

Month-end approximations were rejected. Four earlier candidates are therefore
not events yet: Binjai–Langsa Section 3 (March 2025), Padang–Sicincin (May 2025),
Solo–Yogyakarta Klaten–Prambanan (July 2025) and Probolinggo–Banyuwangi Sections
1–2 (2026). Their openings remain in project notes until an exact date is found.

## 6. Site

Corridor UI v2 renders:

- five cards with metric, total, operating/connected share, as-of date, a
  four-part stacked bar (operating, construction, planned, unallocated/not
  connected) and a coverage-state badge;
- a detail drawer with metric cards, definition, series coverage, notes and
  conflicts, a sortable-by-source segment table and a grouped timeline;
- project drawers with a timeline when the project has dated events;
- downloads `data/corridors-segments.csv` and `data/events.csv` in the Data view.

Coverage state is explicit: **Complete series** (Trans Java), **Partial segment
table** (Sumatra, Papua), **Route total only** (Sulawesi, Kalimantan). Cards
without a progress series do not render a misleading bar or an “unallocated”
legend.

## 7. Validation and offline QA

```
OK: 107 projects, 178 estates, 70 organisations, 89 sources, 5 corridors,
44 segments, 6 events, 0 geometry, 18 investments
```

- `file://` loads five corridor cards; the Trans Java drawer has 23 segment rows
  and two timeline years; the project drawer shows the Gending–Paiton event; the
  Data view shows 5/5 corridors and the two new downloads.
- 19 local file requests, **0 external HTTP(S) requests**, 0 console errors.
- axe-core 4.10.3 with WCAG A/AA tags: **0 violations** on Explore and Corridors
  at 1440 px and 390 px, and on the project drawer.

## 8. Coverage and gaps

- Roads: **45 / 45** (met).
- Corridors with a total: **5 / 5** (met).
- Corridor progress series: **3 / 5**; Sulawesi and Kalimantan are documented
  as route-total-only.
- Corridor segments: **44** rows across three corridors; no published section
  list for Sulawesi or Kalimantan.
- PSN status on roads: 26 `yes`, 6 `no`, 13 `unknown`. The 13 unknown rows are
  not presented as PSN.
- R6 geometry: **deferred**. `project_geometry.csv` is empty; the atlas still
  shows points, not lines.
- Event coverage is thin: exact dates only, so most openings stay in notes.

## 9. Next

1. R6: simplified lines for major corridors, with OSM/ODbL attribution.
2. Add exact dates for the four deferred openings when an official decree or
   inauguration record is found.
3. Refresh Trans Sulawesi and Trans Kalimantan in the monthly run; publish a
   progress series only when a current, sourced kilometre breakdown exists.
4. Do not push or publish.
