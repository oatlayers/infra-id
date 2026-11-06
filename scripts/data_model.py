"""Shared paths, field lists and helpers for the curated data pipeline."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CURATED = DATA / "curated"
DERIVED = DATA / "derived"
RAW = DATA / "raw"
SITE_DATA = ROOT / "site" / "data"

PROJECT_FIELDS = [
    "id", "name", "sector", "subsector", "status", "status_basis", "corridor_id",
    "province", "route", "length_km", "operational_km", "construction_km",
    "progress_pct", "investment_idr_t", "capacity", "capacity_unit", "psn",
    "opened_year", "lat", "lon", "precision", "last_verified", "notes",
]

DERIVED_FIELDS = [
    "id", "name", "sector", "subsector", "status", "status_basis", "corridor_id",
    "province", "route", "length_km", "operational_km", "construction_km",
    "progress_pct", "investment_idr_t", "capacity", "capacity_unit", "psn",
    "opened_year", "lat", "lon", "precision", "operator", "source_url",
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
    "source_type", "archive_path", "licence", "notes",
]

PROJECT_SOURCE_FIELDS = ["project_id", "source_id", "claim", "notes"]

EXTERNAL_FIELDS = ["project_id", "system", "external_id", "url", "notes"]

INVESTMENT_FIELDS = [
    "id", "project_id", "investor_org_id", "amount", "currency", "amount_idr_t",
    "fx_date", "year", "stage", "instrument", "share_pct", "source_id", "notes",
]

LAW_FIELDS = ["id", "title", "number", "year", "level", "url", "status", "notes"]

PROJECT_LAW_FIELDS = ["project_id", "law_id", "relation", "notes"]

CORRIDOR_FIELDS = [
    "id", "name", "island", "definition", "metric", "total_km", "operational_km",
    "construction_km", "planned_km", "progress_pct", "as_of", "source_id", "notes",
]

SEGMENT_FIELDS = [
    "id", "corridor_id", "name", "length_km", "status", "opened_year",
    "source_id", "notes",
]

SECTORS = {"road", "railway", "airport", "seaport", "factory"}
STATUSES = {"planned", "under_construction", "recently_completed", "operating", "stalled"}
PSN_VALUES = {"yes", "no", "unknown"}
PRECISIONS = {"exact", "approximate", "regency", "province"}
ORG_TYPES = {"government", "soe", "private", "consortium", "multilateral", "other"}
ROLES = {"sponsor", "operator", "contractor", "lender", "off_taker", "developer", "owner"}
SOURCE_TYPES = {"official", "secondary", "company", "multilateral"}
STAGES = {"announced", "committed", "financial_close", "disbursed"}
INSTRUMENTS = {"equity", "debt", "grant", "guarantee", "mixed", "other"}
LAW_LEVELS = {"law", "presidential_regulation", "ministerial_regulation", "other"}

TABLES = {
    "projects.csv": PROJECT_FIELDS,
    "organizations.csv": ORG_FIELDS,
    "project_organizations.csv": PROJECT_ORG_FIELDS,
    "sources.csv": SOURCE_FIELDS,
    "project_sources.csv": PROJECT_SOURCE_FIELDS,
    "project_external_ids.csv": EXTERNAL_FIELDS,
    "investments.csv": INVESTMENT_FIELDS,
    "laws.csv": LAW_FIELDS,
    "project_laws.csv": PROJECT_LAW_FIELDS,
    "corridors.csv": CORRIDOR_FIELDS,
    "corridor_segments.csv": SEGMENT_FIELDS,
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
