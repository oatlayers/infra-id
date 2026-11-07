# Phase 2 — Transport PSN Batch

**Date:** 7 November 2026
**Status:** Track 2A complete (T1–T8).
**Source:** Kementerian Perhubungan, *Capaian Progres Proyek Strategis Nasional
(PSN) Sektor Transportasi*, Jakarta, 19 February 2026.
**Snapshot:** `data/raw/2026-11-06/kemenhub_psn_progress_2026.pdf`
**Extraction:** `data/derived/transport_psn.csv` (35 checked rows, page references)
**Importer:** `scripts/build_transport.py`

## What was added

35 curated projects: 13 railways, 7 airports and 15 seaports. Every row has:

- a stable ID, name, sector and subsector;
- an island, province, route, approximate coordinates and `precision=approximate`;
- a `status_basis` quoting the Kemenhub evidence;
- `psn=yes`, `verification=official`, `status_as_of=2026-02-19` and
  `last_verified=2026-11-07`;
- at least one source claim, plus opening, target, investment or progress claims
  where the deck states a figure;
- sponsor, owner and operator links where they can be named;
- common aliases for search.

The flat export now has 62 projects: 27 roads, 13 railways, 7 airports and 15
seaports.

## Status mapping

The deck's summary says 29 projects are complete/operating and 6 are under
construction. The atlas uses its own definitions and the deck's project pages.
The result is:

| Status | Count | Projects |
|---|---:|---|
| `operating` | 24 | 7 airports, 11 seaports, 6 railways |
| `recently_completed` | 1 | Benoa Port expansion (2025) |
| `under_construction` | 6 | Patimban, Double Track Java South, Rantau Prapat–Kota Pinang, Lahat–Kertapati, MRT Jakarta North–South, LRT Jakarta Velodrome–Manggarai |
| `planned` | 4 | New Palembang Port, Muaro Jambi Container Terminal, East Kalimantan Logistics Railway, MRT Jakarta East–West |

Why this differs from the deck's summary:

- **Patimban** is listed among the 29 completed projects, but the project page
  reports Phase I-2 packages 5 and 6 at 95.48% and 93.02% in late 2025.
- **Double Track Java South** is reported at 100%, but the same page describes
  the work as partly complete and the Sepanjang–Wonokromo continuation as still
  in technical planning and land acquisition.
- **Rantau Prapat–Kota Pinang** is listed among the completed projects, but the
  project page says construction stops at Pondok S5 and 52 land parcels remain.
- **Lahat–Kertapati** is listed among the completed projects, but the Coal
  Terminal Unloading System is 33.65% complete.
- **East Kalimantan Logistics Railway, MRT East–West, New Palembang Port and
  Muaro Jambi** are in the deck's construction group but had no physical
  construction at the review date. The atlas calls them `planned` because that
  is the definition in use.

**Makassar–Parepare** stays `operating` (the PSN summary and the plan's table
both treat it as operating) with a recorded conflict: the Mandai–Palanro section
is reported at 95.91% and the Tonasa overpass land issue continued into 2025.

## Conflicts recorded

| Project | Conflict | Treatment |
|---|---|---|
| Double Track Java South | 100% in the summary; "partly complete" on the project page; Rp 86T investment line is copied from KCJB | `under_construction`; investment left blank |
| Rantau Prapat–Kota Pinang | Listed as complete; Pondok S5–Kota Pinang remains; Rp 86T investment line copied from KCJB | `under_construction`; investment left blank |
| Lahat–Kertapati | Listed as complete; coal terminal 33.65% | `under_construction` |
| Patimban | Listed as complete; Phase I-2 at 93–95% | `under_construction`; total investment 18.189T from two JICA loans |
| Makassar–Parepare | Listed as complete; Mandai–Palanro 95.91% | `operating` with a conflict note |
| East Kalimantan Logistics Railway | Target 2028 on page 5, 2027 on page 6 | Uses 2028; both targets in the note |
| New Palembang Port | 2025 target; no physical work at the February 2026 review | `planned`; target kept but flagged as stale |
| Benoa Port | Expansion reported 100% in 2025; original port long operating | `recently_completed` for the 2025 expansion, with a note |
| Airports and ports | Kemenhub gives inauguration years, not exact opening dates | `opened_year` only; `opened_date` blank |

## Data gaps

- **No rail lengths.** The deck does not state km for any railway PSN. The atlas
  leaves `length_km` blank rather than importing an unsourced figure.
- **No asset capacity.** The deck does not state airport passenger capacity or
  port TEU/tonnage. `capacity` is blank; T5 allows capacity only when stated.
- **Approximate coordinates.** All 35 points are airport, port or city
  reference points, not surveyed boundaries.
- **Investment coverage.** 14 projects have a figure. The deck gives none for
  most airports and ports.
- **Status date.** The evidence is from 19 February 2026. `last_verified` is the
  curation date (7 November 2026), not a claim that the asset was re-surveyed.

## Validation changes

Two validation rules were adjusted for this batch:

1. `length_km` is required for roads. A railway may omit it when the official
   source gives no km figure; if a railway supplies `operational_km` or
   `construction_km`, `length_km` is still required.
2. Target years may run to 2040, because MRT Jakarta East–West has a 2032 target.

Both changes are documented in `scripts/validate.py` and the README.

## Accessibility and map

- The detail drawer is modal. The map is now `inert` while the drawer is open,
  so its overlapping approximate markers are not competing focus targets. The
  project list remains the accessible equivalent, and the drawer has
  previous/next controls.
- Cluster radius was raised from 44 px to 60 px. This removes the last
  mobile `target-size` failure where a lone port marker sat under a cluster.
- axe-core 4.10.3 with WCAG A/AA tags: **0 violations** on Explore (desktop and
  mobile) and on a transport detail view. The Phase 1 marker exception is
  closed.

## Build results

- `python scripts/validate.py` → `OK: 62 projects, 178 estates, 32
  organisations, 38 sources, 4 corridors, 0 segments, 0 events, 0 geometry, 0
  investments`.
- Coverage: railways 13/13, airports 7/7, seaports 15/15, transport PSN 35/35.
- Payloads: shell 85.3 KB gz, initial data 98.8 KB gz, basemap 75.2 KB gz,
  estates 10.8 KB gz, total including fonts 350.7 KB gz.
- The site still works from `file://` and makes no external request.

## Next

Track 2B (estates), Track 2C (factories), Track 2D (roads and corridors), then
the Phase 2 exit check. Do not publish.
