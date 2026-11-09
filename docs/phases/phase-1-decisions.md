# Phase 1 Decisions and Guardrails

**Date:** 7 November 2026
**Status:** confirmed. This file closes D1-D5 in the completed v3 plan, which is
retained in git history.
**Publishing:** no GitHub remote, push, Pages deployment or public release. Phase 1
ends with a local, offline-capable preview. Publishing is deferred until the
repository owner asks for it explicitly.

## D1 — Design direction

An **editorial atlas**, not a dashboard.

- Warm paper (`#FBF9F4`), ink (`#101828`) and navy (`#0B1F33`).
- One accent (`#B54708`) for active states, links and focus.
- Source Serif 4 for display type and figures; Inter for UI text.
- Hairlines instead of shadows on panels; one shadow token for floating
  elements only.
- Restrained status colour; every status also has a text label and, on the map,
  a sector glyph.
- No gradients, glassmorphism, emoji, flag motifs or dark mode in v3.

Reference points: Our World in Data, Financial Times visual journalism, Reuters
Graphics, and Indonesian government annual reports.

## D2 — Universe and coverage targets

`data/curated/coverage_targets.csv` records the target for every layer:

| Layer | Target | Universe |
|---|---:|---|
| Toll and major PSN roads | 45 | Major toll corridors plus PSN national roads |
| PSN railways | 13 | Kemenhub transport PSN list, 19 Feb 2026 |
| PSN airports | 7 | Kemenhub transport PSN list |
| PSN seaports | 15 | Kemenhub transport PSN list |
| Factories and smelters | 25 | PSN manufacturing plus private investment ≥ Rp 1T |
| Industrial estates | 179 | Kemenperin 2026 count |
| Special economic zones | 25 | KEK National Council |
| Unique estates and SEZs | 197 | 179 + 25 − 7 overlaps |
| Trans corridors with a km series | 5 | Sumatra, Java, Sulawesi, Kalimantan, Papua |
| Sources | 90 | Official and secondary documents with snapshots |

Excluded by scope: the Bali, Malacca and Sunda strait bridges. Estates remain a
table view until their coordinates are verified.

## D3 — Schema v3

Schema v3 is frozen in `scripts/data_model.py` and enforced by
`scripts/pipeline/validate.py`.

**New project fields:** `island`, `opened_date`, `expected_open_year`,
`status_as_of`, `verification`.

**New estate fields:** `island`, `coordinate_source`, `developer_org_id`,
`occupancy_pct`, `kemenperin_id`, `sez_id`.

**New source and claim fields:** `language`, `snapshot_hash`, `accessed_via`,
`claim_value`, `claim_date`.

**New tables:** `project_events.csv`, `project_geometry.csv`,
`project_aliases.csv`, `estate_sources.csv`, `coverage_targets.csv`.

**Expanded tables:** `corridor_segments.csv` gains segment type, operational and
construction km, progress, expected opening year and a geometry link.
`estates.csv` carries the new fields above.

A one-off schema v3 migration script performed the change; the script is retained
in git history. Existing values were
preserved; `island`, `status_as_of`, `verification` and `coordinate_source`
were backfilled from existing rows. No status or numeric claim was guessed.

## D4 — Budgets

| Budget | Target | Measured 7 Nov 2026 |
|---|---|---|
| Shell HTML + CSS + JS | ≤ 120 KB gzipped | 85.3 KB |
| Initial data payloads | ≤ 200 KB gzipped | 101.7 KB |
| Basemap | ≤ 150 KB gzipped | 75.2 KB |
| Estate layer (lazy) | ≤ 80 KB gzipped | 11.0 KB |
| Total initial including fonts | — | 354 KB gzipped |
| Time to interactive, local file, mid-range phone | ≤ 1.5 s | 0.71 s load and 0.60 s first contentful paint in headless Edge from `file://`; physical-phone test pending |
| Map pan/zoom with 300 markers | 60 fps | pending 300-row test |
| Console errors | zero | zero observed |
| Accessibility | WCAG 2.2 AA | axe-core WCAG A/AA tags: 0 violations on Explore, Corridors, Estates and Data at 1440 px and 390 px. The Phase 1 map-marker target-size exception was fixed in Phase 2 (modal map is inert and cluster radius is 60 px) |

The shell budget excludes data payloads and fonts. Fonts are two bundled WOFF2
files (Inter and Source Serif 4, 166.6 KB together), inside the 150–250 KB
target.

## D5 — Tracking

The completed v3 plan is the work-status record in git history. Phase 1 is marked
complete with a completion log. Phase 2 and Phase 3 remain open.

## Phase 1 deviations from the original plan

- **Estates table shipped in Phase 1, not Phase 2.** The data already existed
  and is clearly marked as a table-only view with coarse coordinates. This does
  not change the map-layer gate.
- **No preview deployment.** A local file preview was signed off instead, per
  the publishing constraint.
- **No 300-marker performance test yet.** The current 27-row dataset is
  clustered; the 300-marker test moves to Phase 2 when transport data lands.
- **Accessibility audit is partial.** axe-core 4.10.3 with WCAG A/AA tags found
  zero violations on Explore, Corridors, Estates and Data. The Phase 1 project
  drawer had one `target-size` exception from overlapping approximate markers.
  Phase 2 closed it by making the map inert while the modal drawer is open and
  raising the cluster radius to 60 px. Lighthouse was not run.
