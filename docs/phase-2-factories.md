# Phase 2 — Factory and Smelter Batch

**Date:** 8 November 2026
**Status:** Track 2C complete for the frozen 27-plant universe.
**Importer:** `scripts/add_factories.py`
**Ledger:** `data/derived/factories_2026.csv`
**Coordinate cache:** `data/derived/nominatim_factories.json`

## Scope and universe

The factory layer covers **PSN manufacturing plants** plus **private plants with
investment of at least Rp 1 trillion**, where the plant is operating, under
construction, recently completed or stalled. Industrial estates are a separate
table; pure mining pits are excluded. The universe was frozen at **27 plants**
against the plan’s 20–30 target.

Each row has a status source, a verification date, a capacity figure and an
approximate plant or industrial-park point. Eighteen rows also have an
investment figure. The batch adds 43 source rows, 26 organisations and 18
investment rows.

## What was added

| Plant | Subsector | Status | Province | Capacity | Investment (Rp T) | Opened / target | Verification |
|---|---|---|---|---:|---:|---:|---|
| Amman Mineral Copper Smelter | smelter | recently_completed | West Nusa Tenggara | 220 ktpa copper cathode | 23.1 | 2025 | dual |
| Borneo Alumina SGAR Mempawah | alumina | recently_completed | West Kalimantan | 1,000 ktpa alumina | 14.85 | 2025 | official |
| CATL–CBL Indonesia Battery Cell Plant | battery | under_construction | West Java | 6.9 GWh/y cells | 99.0 | 2027 | official |
| Chandra Asri Cilegon Petrochemical Complex | petrochemical | operating | Banten | 860 ktpa ethylene | – | 1995 | official |
| Freeport Indonesia Manyar Copper Smelter | smelter | operating | East Java | 1,700 ktpa concentrate | 61.05 | 2024 | dual |
| Inalum Kuala Tanjung Aluminium Smelter | aluminium | operating | North Sumatra | 250 ktpa aluminium | – | 1982 | official |
| Krakatau Steel Cilegon | steel | operating | Banten | 3,000 ktpa steel slab | – | 1970 | official |
| Lotte Chemical Indonesia New Ethylene (LINE) | petrochemical | recently_completed | Banten | 1,000 ktpa ethylene | 65.175 | 2025 | dual |
| PT Angel Nickel Industry | smelter | operating | North Maluku | 66 ktpa Ni in ferronickel | – | 2022 | official |
| PT Dexin Steel Indonesia | steel | operating | Central Sulawesi | 7,000 ktpa crude steel | 36.3 | 2020 | single |
| PT Gunbuster Nickel Industry (GNI) | smelter | stalled | Central Sulawesi | 1,800 ktpa NPI | 49.5 | 2021 | dual |
| PT Gunung Raja Paksi | steel | operating | West Java | 2,200 ktpa steel | – | 1991 | official |
| PT Halmahera Persada Lygend HPAL (Obi) | smelter | operating | North Maluku | 55 ktpa Ni+Co in MHP | 16.5 | 2021 | official |
| PT Huadi Nickel-Alloy Indonesia | smelter | operating | South Sulawesi | 200 ktpa NPI | 6.5 | 2020 | single |
| PT Huafei Nickel Cobalt HPAL (IWIP) | smelter | operating | North Maluku | 120 ktpa Ni in MHP | 34.32 | 2023 | dual |
| PT Indonesia BTR New Energy Material | battery | operating | Central Java | 80 ktpa anode material | 7.887 | 2024 | official |
| PT Indonesia Tsingshan Stainless Steel (ITSS) | steel | operating | Central Sulawesi | 1,000 ktpa stainless steel | – | 2017 | dual |
| PT Obi Nickel Cobalt (ONC) | smelter | operating | North Maluku | 65 ktpa MHP | 18.15 | 2024 | official |
| PT Obsidian Stainless Steel (OSS) | steel | operating | Southeast Sulawesi | 2,500 ktpa stainless steel | – | 2021 | official |
| PT OKI Pulp & Paper Mills | pulp | operating | South Sumatra | 2,800 ktpa pulp | 42.9 | 2016 | dual |
| PT Smelting Gresik Copper Smelter | smelter | operating | East Java | 342 ktpa copper cathode | – | 1998 | official |
| PT Virtue Dragon Nickel Industry (VDNI) | smelter | operating | Southeast Sulawesi | 120 ktpa Ni in NPI | 23.1 | 2019 | official |
| PT Well Harvest Winning Alumina Refinery | alumina | operating | West Kalimantan | 2,000 ktpa alumina | 21.45 | 2016 | official |
| Pupuk Kaltim Bontang | fertiliser | operating | East Kalimantan | 2,980 ktpa urea | – | 1977 | dual |
| Vale Bahodopi HPAL Project | smelter | under_construction | Central Sulawesi | 60 ktpa MHP | 23.1 | 2026 | official |
| Vale Pomalaa HPAL Project | smelter | under_construction | Southeast Sulawesi | 120 ktpa MHP | 44.55 | 2027 | official |
| Vale Sorowako HPAL Project | smelter | under_construction | South Sulawesi | 60 ktpa MHP | 33.0 | 2027 | official |

Status mix: **19 operating, 3 recently completed, 4 under construction and 1
stalled**. The three recently completed rows are Amman, SGAR Mempawah and Lotte
LINE. GNI is the only stalled row.

## Inclusion and exclusion decisions

| Candidate | Decision | Reason |
|---|---|---|
| KIPI Bulungan | Excluded from the factory table | A green industrial park, not a single plant. It is not in the 2024 Kemenperin estate snapshot and needs its own area/coordinate source before it can be added to the estate table. |
| IMIP, IWIP, Konawe/Morosi, Bantaeng, JIIPE | Not rows; their plants are | Industrial estates belong in `estates.csv`. The factories inside them are represented where a named operator and capacity source exist (ITSS, Dexin, Huafei, Angel, VDNI, OSS, Huadi, Freeport Manyar, PT Smelting). |
| Weda Bay Nickel mine, Grasberg, Sorowako mine | Excluded | Pure mining pits and mines, not processing plants. The related HPAL or smelter rows are included separately. |
| GEM steel, Kendal | Excluded | The plan flagged a large steel investment, but no dated official or dual source confirmed operating/construction status, capacity and location. Revisit in the next research pass. |
| Hailiang copper foil / battery announcements | Excluded | Announcements did not meet the status-and-capacity evidence rule at the cut-off date. |
| New capital (IKN) construction projects | Out of scope | The atlas covers sector infrastructure, not the full IKN build programme. |
| The Bali, Malacca and Sunda strait bridges | Out of scope | Excluded by the road scope; they are not factories. |

## Status and conflict register

These conflicts are recorded in each row’s `notes`; they are not silently
resolved.

- **Freeport Manyar design.** PTFI describes a 2 Mtpa concentrate design, while
  the EPC scope and later reporting use 1.7 Mtpa. Cathode output is reported as
  480 ktpa by one source and 600–650 ktpa elsewhere. The row uses 1.7 Mtpa feed.
- **Amman investment.** The plan carried US$2.1B; the current company figure is
  about US$1.4B. The row uses US$1.4B.
- **HPL capacity.** The atlas uses 55 ktpa Ni+Co in MHP; the first phase is also
  reported as 37,260 t Ni plus 4,577 t Co contained in 96,000 t MHP.
- **GNI.** The 2026 PKPU is a court-supervised restructuring stay, not
  liquidation. Management said operations continued in June 2026, but most of the
  20 NPI lines had stopped by July. The row is `stalled`, not `operating`.
- **Vale Pomalaa.** About US$2.7B covers the HPAL plant; some sources include the
  mine and quote US$4.5B. The row uses US$2.7B and records the wider figure.
- **CATL/CBL.** The US$6B figure covers the full battery integration project
  (mine, materials, recycling and plant), not only the Karawang cell plant. The
  row records both the project total and the 6.9 GWh first phase.
- **ITSS.** The row covers ITSS’s 1 Mtpa stainless line. Wood Mackenzie puts the
  wider Morowali stainless complex at 2 Mtpa in 2017 and 3 Mtpa in 2018.
- **Inalum.** Expansion to 400–600 ktpa has been discussed but is not committed
  in a source used here; the row keeps the 250 ktpa reduction-plant capacity.
- **BTR.** Phase 2 (US$299M, 160 ktpa) is not confirmed complete. The row covers
  the 80 ktpa phase that started on 7 August 2024.
- **Chandra Asri.** The 860 ktpa ethylene row is the existing cracker; the
  CA-EDC plant under construction is a separate project and is not included.
- **Krakatau Steel.** The row covers the Cilegon slab plant, not the group’s
  larger rolling capacity.

## Verification and coordinate provenance

- **Status verification:** 17 rows are `official`, 8 are `dual`, and 2 are
  `single` (Dexin and Huadi). No row is `unverified`.
- **PSN status:** 6 rows are `psn=yes`, 9 are `psn=no` and 12 are
  `psn=unknown`; the unknown rows are private plants whose PSN designation is
  not stated in the sources used.
- **Coordinates:** 18 rows use an OSM/Nominatim point
  (`src-osm-nominatim-factories-2026-11-08`, cached in
  `data/derived/nominatim_factories.json`). Nine rows use a manual approximate
  plant/park point and either a company or location claim: ITSS, Dexin, Huafei,
  Angel, ONC, OSS, SGAR, GNI and OKI. All 27 are `precision=approximate`.
- **What the OSM points mean:** where Nominatim returned a village, estate or
  access point rather than a plant polygon, the row uses that point. It is a
  locator, not a surveyed boundary.
- **Investment:** 18 rows have a figure. USD amounts are converted at
  **Rp 16,500/USD** for ranking only, not at a transaction-date rate.
- **Capacity:** all 27 rows have a nameplate capacity. It is not verified output.
- **Status dates:** `status_as_of` varies from 2020 to 2026, reflecting the latest
  evidence for each row. `last_verified` is 2026-11-08 for every row.

## Rebuild and checks

```bash
python scripts/add_factories.py
python scripts/validate.py
python scripts/build_projects.py
python scripts/build_site_data.py
python scripts/build_factories_ledger.py
```

Expected output after the batch:

```text
OK: 27 factories, 43 sources, 26 organisations, 18 investments
OK: 104 projects, 178 estates, 70 organisations, 82 sources, 4 corridors, 0 segments, 0 events, 0 geometry, 18 investments
wrote 104 rows to data/projects.csv
wrote 104 projects, 4 corridors, 178 estates, 82 sources
```

Site checks performed on the generated payloads:

- `projects.geojson` has 27 factory features.
- `stats.js` reports `factory: 27` and the status mix above.
- The Explore sector filter and the factory glyph are wired through
  `constants.js`, `map.js` and `app.js`.
- The drawer shows capacity, investment, operator, status basis, every source
  with claim and retrieval date, and the row notes.

## Remaining gaps

- Plant-level geometry and boundaries are not available; all points are
  approximate.
- The events table is still empty, so factory milestones are not yet dated
  events. The status basis and notes carry the dates instead.
- `claim_value` is blank for factory claims; the numeric values live in the
  project and investment rows.
- GEM steel, Hailiang and other announced plants need a dated status/capacity
  source before inclusion.
- KIPI Bulungan needs an estate source before it can join the estate table.
- Capacity and investment figures need a periodic re-check; some are nameplate
  or planning figures rather than current output.
