"""Shared paths, field lists and helpers for the curated data pipeline.

The field lists define the on-disk CSV schema. Changing a list here without a
migration leaves the table headers out of sync, and validate.py will fail.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CURATED = DATA / "curated"
DERIVED = DATA / "derived"
RAW = DATA / "raw"
SITE_DATA = ROOT / "site" / "data"

# Schema v3 (7 November 2026). New project fields: island, opened_date,
# expected_open_year, status_as_of, verification. New estate fields: island,
# coordinate_source, developer_org_id, occupancy_pct, kemenperin_id, sez_id.
PROJECT_FIELDS = [
    "id", "name", "sector", "subsector", "status", "status_basis", "corridor_id",
    "island", "province", "route", "length_km", "operational_km", "construction_km",
    "progress_pct", "investment_idr_t", "capacity", "capacity_unit", "psn",
    "opened_year", "opened_date", "expected_open_year", "status_as_of",
    "verification", "lat", "lon", "precision", "last_verified", "notes",
]

DERIVED_FIELDS = [
    "id", "name", "sector", "subsector", "status", "status_basis", "corridor_id",
    "island", "province", "route", "length_km", "operational_km", "construction_km",
    "progress_pct", "investment_idr_t", "capacity", "capacity_unit", "psn",
    "opened_year", "opened_date", "expected_open_year", "status_as_of",
    "verification", "lat", "lon", "precision", "operator", "source_url",
    "source_type", "retrieved_on", "last_verified", "notes",
]

ORG_FIELDS = [
    "id", "name", "short_name", "org_type", "country_code", "parent_id",
    "website", "notes",
]

PROJECT_ORG_FIELDS = [
    "project_id", "org_id", "role", "share_pct", "start_year", "end_year",
    "source_id", "notes",
]

SOURCE_FIELDS = [
    "id", "publisher", "title", "url", "published_on", "retrieved_on",
    "source_type", "language", "snapshot_hash", "accessed_via", "archive_path",
    "licence", "notes",
]

PROJECT_SOURCE_FIELDS = [
    "project_id", "source_id", "claim", "claim_value", "claim_date", "notes",
]

EXTERNAL_FIELDS = ["project_id", "system", "external_id", "url", "notes"]

ALIAS_FIELDS = ["project_id", "alias", "source_id", "notes"]

INVESTMENT_FIELDS = [
    "id", "project_id", "investor_org_id", "amount", "currency", "amount_idr_t",
    "fx_date", "year", "stage", "instrument", "share_pct", "source_id", "notes",
]

LAW_FIELDS = ["id", "title", "number", "year", "level", "url", "status", "notes"]

PROJECT_LAW_FIELDS = ["project_id", "law_id", "relation", "notes"]

EVENT_FIELDS = [
    "id", "project_id", "event_date", "event_type", "description", "source_id",
    "notes",
]

GEOMETRY_FIELDS = [
    "id", "project_id", "kind", "geometry", "precision", "source_id", "notes",
]

CORRIDOR_FIELDS = [
    "id", "name", "island", "definition", "metric", "total_km", "operational_km",
    "construction_km", "planned_km", "progress_pct", "as_of", "source_id", "notes",
]

SEGMENT_FIELDS = [
    "id", "corridor_id", "name", "segment_type", "length_km", "operational_km",
    "construction_km", "progress_pct", "status", "opened_year",
    "expected_open_year", "geometry_id", "source_id", "notes",
]

ESTATE_FIELDS = [
    "id", "name", "type", "province", "regency", "island", "lat", "lon",
    "precision", "coordinate_source", "area_ha", "developer", "developer_org_id",
    "status", "sector_focus", "legal_basis", "established_year", "website",
    "occupancy_pct", "kemenperin_id", "sez_id", "source_id", "last_verified",
    "notes",
]

ESTATE_SOURCE_FIELDS = [
    "estate_id", "source_id", "claim", "claim_value", "claim_date", "notes",
]

COVERAGE_FIELDS = [
    "layer", "label", "unit", "target_count", "universe", "source_id", "notes",
]

SECTORS = {"road", "railway", "airport", "seaport", "factory"}
STATUSES = {"planned", "under_construction", "recently_completed", "operating", "stalled"}
PSN_VALUES = {"yes", "no", "unknown"}
PRECISIONS = {"exact", "approximate", "regency", "province"}
ISLANDS = {"Sumatra", "Java", "Kalimantan", "Sulawesi", "Papua", "Bali-Nusa Tenggara", "Maluku"}
VERIFICATIONS = {"official", "dual", "single", "unverified"}
ORG_TYPES = {"government", "soe", "private", "consortium", "multilateral", "other"}
ROLES = {"sponsor", "operator", "contractor", "lender", "off_taker", "developer", "owner"}
SOURCE_TYPES = {"official", "secondary", "company", "multilateral"}
LANGUAGES = {"en", "id", "other"}
STAGES = {"announced", "committed", "financial_close", "disbursed"}
INSTRUMENTS = {"equity", "debt", "grant", "guarantee", "mixed", "other"}
LAW_LEVELS = {"law", "presidential_regulation", "ministerial_regulation", "other"}
EVENT_TYPES = {
    "announced", "groundbreaking", "contract", "financial_close", "section_opened",
    "opened", "stalled", "resumed", "target_changed", "other",
}
GEOMETRY_KINDS = {"line", "point", "polygon"}
SEGMENT_TYPES = {"section", "phase", "package", "other"}
ESTATE_TYPES = {"industrial_estate", "sez", "both"}
ESTATE_STATUSES = {"operating", "under_construction", "planned"}
COORDINATE_SOURCES = {"official", "osm", "regency", "manual", "unknown"}

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


def island_for(province: str) -> str:
    first = (province or "").split(";")[0].strip()
    if first not in PROVINCE_ISLAND:
        raise ValueError(f"no island mapping for province {first!r}")
    return PROVINCE_ISLAND[first]


TABLES = {
    "projects.csv": PROJECT_FIELDS,
    "organizations.csv": ORG_FIELDS,
    "project_organizations.csv": PROJECT_ORG_FIELDS,
    "sources.csv": SOURCE_FIELDS,
    "project_sources.csv": PROJECT_SOURCE_FIELDS,
    "project_external_ids.csv": EXTERNAL_FIELDS,
    "project_aliases.csv": ALIAS_FIELDS,
    "investments.csv": INVESTMENT_FIELDS,
    "laws.csv": LAW_FIELDS,
    "project_laws.csv": PROJECT_LAW_FIELDS,
    "project_events.csv": EVENT_FIELDS,
    "project_geometry.csv": GEOMETRY_FIELDS,
    "corridors.csv": CORRIDOR_FIELDS,
    "corridor_segments.csv": SEGMENT_FIELDS,
    "estates.csv": ESTATE_FIELDS,
    "estate_sources.csv": ESTATE_SOURCE_FIELDS,
    "coverage_targets.csv": COVERAGE_FIELDS,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(fh)
        ]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def is_blank(value: str) -> bool:
    return value is None or str(value).strip() == ""


def as_float(value: str) -> float | None:
    if is_blank(value):
        return None
    return float(value)


def as_int(value: str) -> int | None:
    if is_blank(value):
        return None
    return int(float(value))


def num(value: object) -> str:
    if value in (None, ""):
        return ""
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:g}"
