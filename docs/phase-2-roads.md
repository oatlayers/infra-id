# Phase 2 — BPJT PSN Road Batch

**Date:** 8 November 2026
**Status:** Track 2D partial. R1 done for PSN toll roads; R2–R6 not started.
**Source:** BPJT toll-road list API, snapshot 6 November 2026
(`data/raw/2026-11-06/bpjt_toll_road_list.json`).
**Importer:** `scripts/add_bpjt_psn_roads.py`.

## What was added

The curated batch had 27 toll corridors. The BPJT snapshot has 15 more PSN
corridors in scope, so the atlas now has **42 road corridors** against a target
of 45. The flat export has **77 projects**.

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

The three Trans Sumatra rows link to `trans-sumatera`: Simpang
Indralaya–Muara Enim, Pekanbaru–Kandis–Dumai and Medan–Binjai.

## Status mapping

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

## Coordinates

Coordinates are the midpoint of the BPJT start and end points and carry
`precision=approximate`. BPJT returns UTM coordinates for
Ngawi–Kertosono–Kediri, so that row uses a manual corridor midpoint
(-7.55, 111.65) with a note; validation rejects the raw UTM values.

## Operators

Twelve concession operators were added to `organizations.csv`, including
Trans Bumi Serbaraja, Citra Karya Jabar Tol, Cibitung Tanjung Priok Port
Tollways, Jasamarga Kunciran Cengkareng, Jasamarga Manado Bitung, Jasamarga
Balikpapan Samarinda, Marga Trans Nusantara, Trans Jawa Paspro Jalan Tol,
Jasamarga Pandaan Malang, Jasamarga Ngawi Kertosono Kediri, Medan Binjai Tol and
Translingkar Kita Jaya. Hutama Karya already existed.

## Coverage and gaps

- Roads: **42 / 45** target corridors (partial, 93%).
- The three-road gap to the 45 target is not a PSN toll-road gap. The next
  candidates are non-toll PSN roads, 0-km concessions and access roads listed in
  `plan.md`.
- Corridor segments, events and geometry are still empty. R2–R6 remain.
- Total projects: 77 (42 roads, 13 railways, 7 airports, 15 seaports).
- Sources: 39 (32 official, 7 secondary).

## Validation and accessibility

- `python scripts/validate.py` → `OK: 77 projects, 178 estates, 44
  organisations, 39 sources, 4 corridors, 0 segments, 0 events, 0 geometry, 0
  investments`.
- axe-core 4.10.3 with WCAG A/AA tags: 0 violations on Explore at 1440 px and
  390 px with the 77-project dataset.
- The site still works from `file://` and makes no external request.

## Next

1. R2: add Trans Java and open Trans Sumatra operating context.
2. R3: corridor segments for five corridors.
3. R4: recent openings and stalled/resumed events.
4. R5–R6: corridor UI v2 and simplified lines.
5. Do not push or publish.
