# Phase 2 — Estate Reconciliation and Coordinates

**Date:** 8 November 2026
**Status:** Track 2B partial. E1 done, E2 blocked, E3 partial, E4 not
started, E5 shipped in Phase 1, E6 deferred.

## E1 — The 179-vs-160 gap

Kemenperin reports **179 industrial estates** in 2026. The curated table carries
**160 industrial-estate designations** from the 2024 BAJRA mirror of Kemenperin
data. The difference is **19**.

The Kemenperin source itself was not reachable on 8 November 2026:

- `https://kemenperin.go.id/` → HTTP 502;
- `satudata.kemenperin.go.id` → DNS failure;
- the Kemenperin search page → HTTP 502.

The 179 count is sourced to ANTARA's report of the Kemenperin briefing on
29 June 2026 (`src-antara-kemenperin-179-2026`). That article gives the total,
area (101,351.45 ha), occupancy (57.20%) and Java/non-Java split, but no names.

`data/derived/estate_gap_2026.csv` is a 19-row ledger:

| Disposition | Rows | Meaning |
|---|---:|---|
| `unresolved-location-conflict` | 2 | IPIP (Central vs Southeast Sulawesi) and Tembesi (West Kalimantan vs Batam) |
| `unresolved-no-source` | 7 | I-Sentra Lamongan, Huadi Bantaeng, Cikembar II, Losarang, Purwakarta Integrated Industrial Park, Pulau Penebang, Seafer |
| `unresolved-not-named` | 10 | The remaining gap; no reachable source names them |

The ledger is downloadable from the Data view. It is deliberately not a list of
invented rows: a name alone is not enough for a curated row, which needs an area,
a developer, a location and a source.

### Named additions

| Name | Province / regency | Disposition | Why it is not a row yet |
|---|---|---|---|
| IPIP (Indonesia Pomalaa Industry Park) | Central Sulawesi (Kemenperin) / Pomalaa, Southeast Sulawesi | location conflict | The official careers site confirms the company, but gives no area or boundary |
| I-Sentra Lamongan | East Java / Lamongan | no source | No reachable official page, area or coordinate |
| Huadi Bantaeng | South Sulawesi / Bantaeng | no source | The operator is known; no reachable estate area or boundary |
| Cikembar II | West Java / Sukabumi | no source | Cikembar I is in the table; Cikembar II is a separate 2025 designation |
| Losarang | West Java / Indramayu | no source | No reachable official page or area |
| Purwakarta Integrated Industrial Park | West Java / Purwakarta | no source | Several Purwakarta estates are in the table, but not this one |
| Pulau Penebang | Riau Islands / Bintan | no source | Island location known; no developer page or area |
| Seafer | Riau Islands / Batam | no source | No reachable developer page or area |
| Tembesi | Riau Islands / Batam | location conflict | Kemenperin is reported to list it under West Kalimantan; the well-known Tembesi area is in Batam |

## E2 — Adding the nine

**Blocked.** The nine named additions cannot be added without an area, a
developer, a location and a source. The Kemenperin list is unavailable and the
developer pages that resolve do not publish those fields. Adding estimates would
break the source rule. Revisit when the Kemenperin list or a dated provincial
announcement is reachable.

## E3 — Coordinates

Current estate coordinate provenance:

| Source | Rows | Notes |
|---|---:|---|
| `official` | 25 | KEK profile points for the 25 SEZs, including the 7 shared zones |
| `osm` | 20 | Largest industrial estates, industrial-landuse points from Nominatim |
| `regency` | 133 | Regency/city centroid fallback |

The 20 OSM matches are cached in `data/derived/nominatim_estates.json` and
sourced to `src-osm-nominatim-2026-11-08` (OpenStreetMap contributors, ODbL
1.0). The script is `scripts/geocode_estates.py`; it queries one request per
second, accepts only `type=industrial` results that match the estate name and
regency/province, and requires numbered estates to match their number (so
GIIC 2 does not inherit GIIC 1's point).

The matched set includes Java Integrated Industrial and Port Estate, GIIC, Kota
Bukit Indah, Jatiluhur, Millenium, Dumai, Pertiwi Lestari, Modern Cikande,
MM2100, Wilmar, Medan, Indotaisei, Krakatau Cilegon, Karawang International
Industrial City (two source rows), Kawasan Berikat Nusantara, Pasuruan,
Pulogadung, Maspion and Suryacipta. Batamindo is below the top-40 cutoff and
keeps its regency point.

**Not done:** 20 of the 40 largest still use regency centroids because Nominatim
has no industrial-landuse match. The remaining 133 also stay regency. The map
layer remains off.

## E4 — Attributes and status

**Not started.** The 160 industrial-estate rows still carry `status=operating`
from the 2024 table, and most have blank `sector_focus`, `website`,
`legal_basis` and `established_year`. Changing status needs a dated source for
each estate; the 2024 list is not enough. This remains a documented gap.

## E5 — Estates table

Shipped in Phase 1. Now shows 178 rows, coordinate provenance in the inline
detail, the 19-row gap ledger as a download, and coordinate values to 4–5
decimal places.

## E6 — Optional map layer

**Deferred.** Only 25 of 178 estate coordinates are official and 20 more are
OSM points. The table stays the only estate view, as required.

## Site changes

- Data view: estate coverage now names the 19-row ledger, the nine named
  additions and the coordinate-source split.
- Downloads: `data/estate-gap.csv`.
- Estate detail: coordinates show 4–5 decimals and the OSM/BAJRA provenance.
- Sources: 39 (32 official, 7 secondary).

## Next

1. Resolve the Kemenperin list or a dated 2025 provincial announcement; add the
   nine named estates with area, developer, location, coordinates and source.
2. Geocode the remaining 20 of the top 40; keep the acceptance and numbered-
   estate checks.
3. Add sector focus, website, legal basis and verified status for the top 100
   estates.
4. Keep the estate map layer off until coverage is materially complete.
