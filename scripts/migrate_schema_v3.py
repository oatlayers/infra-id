"""One-off schema v3 migration.

Adds the new project, estate, source, claim, segment and estate-source fields,
and creates the new event, geometry, alias and estate-source tables. Existing
values are preserved; new fields are backfilled only where the value is
unambiguous.

Run once: python scripts/migrate_schema_v3.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from data_model import (
    ALIAS_FIELDS,
    COVERAGE_FIELDS,
    CURATED,
    ESTATE_FIELDS,
    ESTATE_SOURCE_FIELDS,
    EVENT_FIELDS,
    GEOMETRY_FIELDS,
    PROJECT_FIELDS,
    PROJECT_SOURCE_FIELDS,
    SEGMENT_FIELDS,
    SOURCE_FIELDS,
    write_csv,
)

PROVINCE_ISLAND = {
    # Sumatra
    "Aceh": "Sumatra", "North Sumatra": "Sumatra", "West Sumatra": "Sumatra",
    "Riau": "Sumatra", "Riau Islands": "Sumatra", "Jambi": "Sumatra",
    "Bengkulu": "Sumatra", "South Sumatra": "Sumatra", "Lampung": "Sumatra",
    "Bangka Belitung": "Sumatra", "Kepulauan Riau": "Sumatra",
    "Kepulauan Bangka Belitung": "Sumatra", "Sumatera Utara": "Sumatra",
    "Sumatera Barat": "Sumatra", "Sumatera Selatan": "Sumatra",
    # Java
    "Banten": "Java", "DKI Jakarta": "Java", "West Java": "Java",
    "Central Java": "Java", "DI Yogyakarta": "Java", "East Java": "Java",
    "Jawa Barat": "Java", "Jawa Tengah": "Java", "Jawa Timur": "Java",
    # Bali and Nusa Tenggara
    "Bali": "Bali-Nusa Tenggara", "West Nusa Tenggara": "Bali-Nusa Tenggara",
    "East Nusa Tenggara": "Bali-Nusa Tenggara",
    "Nusa Tenggara Barat": "Bali-Nusa Tenggara", "Nusa Tenggara Timur": "Bali-Nusa Tenggara",
    # Kalimantan
    "West Kalimantan": "Kalimantan", "Central Kalimantan": "Kalimantan",
    "South Kalimantan": "Kalimantan", "East Kalimantan": "Kalimantan",
    "North Kalimantan": "Kalimantan", "Kalimantan Barat": "Kalimantan",
    "Kalimantan Tengah": "Kalimantan", "Kalimantan Selatan": "Kalimantan",
    "Kalimantan Timur": "Kalimantan", "Kalimantan Utara": "Kalimantan",
    # Sulawesi
    "North Sulawesi": "Sulawesi", "Gorontalo": "Sulawesi",
    "Central Sulawesi": "Sulawesi", "West Sulawesi": "Sulawesi",
    "South Sulawesi": "Sulawesi", "Southeast Sulawesi": "Sulawesi",
    "Sulawesi Utara": "Sulawesi", "Sulawesi Tengah": "Sulawesi",
    "Sulawesi Barat": "Sulawesi", "Sulawesi Selatan": "Sulawesi",
    "Sulawesi Tenggara": "Sulawesi",
    # Maluku
    "Maluku": "Maluku", "North Maluku": "Maluku", "Maluku Utara": "Maluku",
    # Papua
    "Papua": "Papua", "West Papua": "Papua", "Southwest Papua": "Papua",
    "Central Papua": "Papua", "South Papua": "Papua", "Highland Papua": "Papua",
    "Papua Barat": "Papua", "Papua Barat Daya": "Papua", "Papua Selatan": "Papua",
    "Papua Tengah": "Papua", "Papua Pegunungan": "Papua",
}


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(fh)]


def island_for(province: str) -> str:
    first = (province or "").split(";")[0].strip()
    if first not in PROVINCE_ISLAND:
        raise SystemExit(f"no island mapping for province {first!r}")
    return PROVINCE_ISLAND[first]


def official_sources() -> dict[str, list[str]]:
    sources = {row["id"]: row for row in read(CURATED / "sources.csv")}
    result: dict[str, list[str]] = {}
    for claim in read(CURATED / "project_sources.csv"):
        source = sources.get(claim["source_id"])
        if source:
            result.setdefault(claim["project_id"], []).append(source["source_type"])
    return result


def verification_for(types: list[str]) -> str:
    if any(kind == "official" for kind in types):
        return "official"
    if len(types) >= 2:
        return "dual"
    if len(types) == 1:
        return "single"
    return "unverified"


def main() -> None:
    # Projects
    projects = read(CURATED / "projects.csv")
    types = official_sources()
    for row in projects:
        row["island"] = row.get("island") or island_for(row["province"])
        row["status_as_of"] = row.get("status_as_of") or row["last_verified"]
        row["verification"] = row.get("verification") or verification_for(types.get(row["id"], []))
        row["opened_date"] = row.get("opened_date", "")
        row["expected_open_year"] = row.get("expected_open_year", "")
    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)

    # Estates
    estates = read(CURATED / "estates.csv")
    for row in estates:
        row["island"] = row.get("island") or island_for(row["province"])
        row["coordinate_source"] = row.get("coordinate_source") or (
            "official" if row["type"] in {"sez", "both"} else "regency"
        )
        for field in ("developer_org_id", "occupancy_pct", "kemenperin_id", "sez_id"):
            row[field] = row.get(field, "")
    write_csv(CURATED / "estates.csv", ESTATE_FIELDS, estates)

    # Sources
    sources = read(CURATED / "sources.csv")
    for row in sources:
        row["language"] = row.get("language") or (
            "en" if row["publisher"] == "Wikipedia (English)" else "id"
        )
        row["snapshot_hash"] = row.get("snapshot_hash", "")
        row["accessed_via"] = row.get("accessed_via", "")
    write_csv(CURATED / "sources.csv", SOURCE_FIELDS, sources)

    # Claims
    claims = read(CURATED / "project_sources.csv")
    for row in claims:
        row["claim_value"] = row.get("claim_value", "")
        row["claim_date"] = row.get("claim_date", "")
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)

    # Corridor segments (header-only today)
    segments = read(CURATED / "corridor_segments.csv")
    for row in segments:
        for field in (
            "segment_type", "operational_km", "construction_km", "progress_pct",
            "expected_open_year", "geometry_id",
        ):
            row[field] = row.get(field, "")
    write_csv(CURATED / "corridor_segments.csv", SEGMENT_FIELDS, segments)

    # New tables: create with headers if they do not exist.
    for name, fields in {
        "project_aliases.csv": ALIAS_FIELDS,
        "project_events.csv": EVENT_FIELDS,
        "project_geometry.csv": GEOMETRY_FIELDS,
        "estate_sources.csv": ESTATE_SOURCE_FIELDS,
        "coverage_targets.csv": COVERAGE_FIELDS,
    }.items():
        path = CURATED / name
        if not path.exists():
            write_csv(path, fields, [])

    print(
        f"migrated {len(projects)} projects, {len(estates)} estates, "
        f"{len(sources)} sources, {len(claims)} claims, {len(segments)} segments"
    )


if __name__ == "__main__":
    main()
