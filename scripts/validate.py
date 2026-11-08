"""Validate the curated CSV tables and their foreign keys.

Run: python scripts/validate.py
Exits non-zero on any error.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

from data_model import (
    CLAIM_TYPES,
    CONFLICT_SCOPES,
    CONFLICT_STATUSES,
    COORDINATE_SOURCES,
    CURATED,
    ESTATE_STATUSES,
    ESTATE_TYPES,
    EVENT_TYPES,
    GEOMETRY_KINDS,
    INSTRUMENTS,
    ISLANDS,
    LANGUAGES,
    LAW_LEVELS,
    ORG_TYPES,
    PRECISIONS,
    PSN_VALUES,
    ROOT,
    ROLES,
    SECTORS,
    SEGMENT_TYPES,
    SOURCE_TYPES,
    STAGES,
    STATUSES,
    TABLES,
    VERIFICATIONS,
    as_int,
    is_blank,
    read_csv,
)

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COUNTRY_RE = re.compile(r"^[A-Z]{2}$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")

errors: list[str] = []


def err(message: str) -> None:
    errors.append(message)


def columns(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as fh:
        return next(csv.reader(fh))


def check_columns() -> None:
    for name, expected in TABLES.items():
        path = CURATED / name
        if not path.exists():
            err(f"{name}: file is missing")
            continue
        actual = columns(path)
        if actual != expected:
            err(f"{name}: header mismatch; expected {expected}, got {actual}")


def check_id(value: str, where: str) -> None:
    if not ID_RE.match(value):
        err(f"{where}: id must be lowercase-hyphenated")


def check_date(value: str, where: str) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        err(f"{where}: not a real YYYY-MM-DD date")


def check_enum(value: str, allowed: set[str], field: str, where: str) -> None:
    if value not in allowed:
        err(f"{where}: {field} has bad value {value!r}")


def check_url(value: str, where: str) -> None:
    if not value.startswith(("http://", "https://")):
        err(f"{where}: URL does not start with http(s)://")


def check_number(value: str, field: str, where: str, minimum: float = 0.0) -> float | None:
    if is_blank(value):
        return None
    try:
        number = float(value)
    except ValueError:
        err(f"{where}: {field} is not a number")
        return None
    if number < minimum:
        err(f"{where}: {field} must be >= {minimum}")
    return number


def check_year(value: str, field: str, where: str) -> int | None:
    year = as_int(value)
    # Targets can sit beyond 2030 (MRT Jakarta East-West is 2032).
    if year is None or not 1900 <= year <= 2040:
        err(f"{where}: {field} is not a plausible year")
        return None
    return year


def main() -> None:
    check_columns()
    if errors:
        print(f"{len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        sys.exit(1)

    projects = read_csv(CURATED / "projects.csv")
    organizations = read_csv(CURATED / "organizations.csv")
    project_orgs = read_csv(CURATED / "project_organizations.csv")
    sources = read_csv(CURATED / "sources.csv")
    project_sources = read_csv(CURATED / "project_sources.csv")
    external_ids = read_csv(CURATED / "project_external_ids.csv")
    aliases = read_csv(CURATED / "project_aliases.csv")
    investments = read_csv(CURATED / "investments.csv")
    laws = read_csv(CURATED / "laws.csv")
    project_laws = read_csv(CURATED / "project_laws.csv")
    events = read_csv(CURATED / "project_events.csv")
    geometry = read_csv(CURATED / "project_geometry.csv")
    corridors = read_csv(CURATED / "corridors.csv")
    segments = read_csv(CURATED / "corridor_segments.csv")
    estates = read_csv(CURATED / "estates.csv")
    estate_sources = read_csv(CURATED / "estate_sources.csv")
    coverage = read_csv(CURATED / "coverage_targets.csv")
    conflicts = read_csv(CURATED / "conflicts.csv")

    project_ids = {row["id"] for row in projects}
    org_ids = {row["id"] for row in organizations}
    source_ids = {row["id"] for row in sources}
    corridor_ids = {row["id"] for row in corridors}
    law_ids = {row["id"] for row in laws}
    estate_ids = {row["id"] for row in estates}
    geometry_ids = {row["id"] for row in geometry}

    seen: set[str] = set()
    for row in projects:
        where = f"projects {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)

        for field in ("name", "status_basis", "island", "province", "route", "lat",
                      "lon", "precision", "psn", "status_as_of", "verification",
                      "last_verified", "notes"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")

        check_enum(row["sector"], SECTORS, "sector", where)
        check_enum(row["status"], STATUSES, "status", where)
        check_enum(row["precision"], PRECISIONS, "precision", where)
        check_enum(row["psn"], PSN_VALUES, "psn", where)
        check_enum(row["island"], ISLANDS, "island", where)
        check_enum(row["verification"], VERIFICATIONS, "verification", where)
        check_date(row["last_verified"], f"{where} last_verified")
        check_date(row["status_as_of"], f"{where} status_as_of")

        if row["corridor_id"] and row["corridor_id"] not in corridor_ids:
            err(f"{where}: unknown corridor_id {row['corridor_id']!r}")

        length = check_number(row["length_km"], "length_km", where)
        operational = check_number(row["operational_km"], "operational_km", where)
        construction = check_number(row["construction_km"], "construction_km", where)
        check_number(row["progress_pct"], "progress_pct", where)
        check_number(row["investment_idr_t"], "investment_idr_t", where)

        # Road corridors are defined by length. Some transport PSNs are
        # programmes or single assets whose official source gives no km figure
        # (the Kemenhub deck does not), so railway length is required only when
        # a km breakdown is supplied.
        if row["sector"] == "road" and length is None:
            err(f"{where}: road projects need length_km")
        if row["sector"] == "railway" and length is None and (operational is not None or construction is not None):
            err(f"{where}: railway km breakdown needs length_km")
        if length is not None:
            used = (operational or 0) + (construction or 0)
            if used > length * 1.05:
                err(f"{where}: operational + construction exceeds length ({used:g} > {length:g})")

        if not is_blank(row["progress_pct"]):
            progress = float(row["progress_pct"])
            if not 0 <= progress <= 100:
                err(f"{where}: progress_pct must be 0-100")

        opened = as_int(row["opened_year"])
        if not is_blank(row["opened_year"]):
            if opened is None or not 1900 <= opened <= 2030:
                err(f"{where}: opened_year is not a plausible year")
        if row["status"] in {"operating", "recently_completed"} and opened is None:
            err(f"{where}: {row['status']} requires opened_year")
        if row["status"] == "recently_completed" and opened is not None and opened < 2024:
            err(f"{where}: recently_completed must have opened_year >= 2024")
        if row["opened_date"]:
            check_date(row["opened_date"], f"{where} opened_date")
        if row["expected_open_year"]:
            check_year(row["expected_open_year"], "expected_open_year", where)

        if bool(row["capacity"]) != bool(row["capacity_unit"]):
            err(f"{where}: capacity and capacity_unit must be set together")

        try:
            lat = float(row["lat"])
            lon = float(row["lon"])
        except ValueError:
            err(f"{where}: lat/lon are not numbers")
        else:
            if not (-11.0 <= lat <= 6.0 and 95.0 <= lon <= 141.0):
                err(f"{where}: coordinates outside Indonesia ({lat}, {lon})")

    seen = set()
    for row in organizations:
        where = f"organizations {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        if not row["name"]:
            err(f"{where}: missing name")
        check_enum(row["org_type"], ORG_TYPES, "org_type", where)
        if not COUNTRY_RE.match(row["country_code"]):
            err(f"{where}: country_code must be ISO alpha-2")
        if row["parent_id"] and row["parent_id"] not in org_ids:
            err(f"{where}: unknown parent_id {row['parent_id']!r}")
        if row["parent_id"] == row["id"]:
            err(f"{where}: parent_id cannot point to itself")
        if row["website"]:
            check_url(row["website"], where)

    seen = set()
    for row in project_orgs:
        where = f"project_organizations {row['project_id']}/{row['org_id']}/{row['role']}"
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if row["org_id"] not in org_ids:
            err(f"{where}: unknown organisation")
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        check_enum(row["role"], ROLES, "role", where)
        if row["share_pct"]:
            share = check_number(row["share_pct"], "share_pct", where)
            if share is not None and share > 100:
                err(f"{where}: share_pct must be <= 100")
        key = (row["project_id"], row["org_id"], row["role"])
        if key in seen:
            err(f"{where}: duplicate link")
        seen.add(key)

    seen = set()
    for row in sources:
        where = f"sources {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        for field in ("publisher", "title", "url", "retrieved_on", "source_type", "language"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        check_url(row["url"], where)
        check_date(row["retrieved_on"], f"{where} retrieved_on")
        if row["published_on"]:
            check_date(row["published_on"], f"{where} published_on")
        check_enum(row["source_type"], SOURCE_TYPES, "source_type", where)
        check_enum(row["language"], LANGUAGES, "language", where)
        if row["archive_path"] and not (ROOT / row["archive_path"]).exists():
            err(f"{where}: archive_path does not exist: {row['archive_path']}")

    projects_with_source: set[str] = set()
    seen = set()
    for row in project_sources:
        where = f"project_sources {row['project_id']}/{row['source_id']}"
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        if not row["claim"]:
            err(f"{where}: missing claim")
        elif "," in row["claim"]:
            err(f"{where}: claim must be one atomic type, got {row['claim']!r}")
        elif row["claim"] not in CLAIM_TYPES:
            err(f"{where}: unknown claim type {row['claim']!r}")
        if row["claim_date"]:
            check_date(row["claim_date"], f"{where} claim_date")
        projects_with_source.add(row["project_id"])
        key = (row["project_id"], row["source_id"], row["claim"])
        if key in seen:
            err(f"{where}: duplicate claim")
        seen.add(key)
    for project_id in project_ids - projects_with_source:
        err(f"projects {project_id}: no source linked")

    seen = set()
    for row in external_ids:
        where = f"project_external_ids {row['project_id']}/{row['system']}"
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if not row["system"] or not row["external_id"]:
            err(f"{where}: missing system or external_id")
        key = (row["project_id"], row["system"])
        if key in seen:
            err(f"{where}: duplicate external id")
        seen.add(key)

    seen = set()
    for row in aliases:
        where = f"project_aliases {row['project_id']}/{row['alias']}"
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if not row["alias"]:
            err(f"{where}: missing alias")
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        key = (row["project_id"], row["alias"])
        if key in seen:
            err(f"{where}: duplicate alias")
        seen.add(key)

    seen = set()
    for row in investments:
        where = f"investments {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if row["investor_org_id"] not in org_ids:
            err(f"{where}: unknown investor")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        amount = check_number(row["amount"], "amount", where)
        if amount is None or amount <= 0:
            err(f"{where}: amount must be positive")
        if not CURRENCY_RE.match(row["currency"]):
            err(f"{where}: currency must be ISO alpha-3")
        check_number(row["amount_idr_t"], "amount_idr_t", where)
        if row["fx_date"]:
            check_date(row["fx_date"], f"{where} fx_date")
        check_enum(row["stage"], STAGES, "stage", where)
        check_enum(row["instrument"], INSTRUMENTS, "instrument", where)
        if row["share_pct"]:
            share = check_number(row["share_pct"], "share_pct", where)
            if share is not None and share > 100:
                err(f"{where}: share_pct must be <= 100")

    seen = set()
    for row in laws:
        where = f"laws {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        for field in ("title", "number", "year", "level", "url", "status"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        check_enum(row["level"], LAW_LEVELS, "level", where)
        check_url(row["url"], where)
        year = as_int(row["year"])
        if year is None or not 1945 <= year <= 2030:
            err(f"{where}: implausible year")

    for row in project_laws:
        where = f"project_laws {row['project_id']}/{row['law_id']}"
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if row["law_id"] not in law_ids:
            err(f"{where}: unknown law")
        if not row["relation"]:
            err(f"{where}: missing relation")

    seen = set()
    for row in events:
        where = f"project_events {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        if is_blank(row["event_date"]):
            err(f"{where}: missing event_date")
        else:
            check_date(row["event_date"], f"{where} event_date")
        check_enum(row["event_type"], EVENT_TYPES, "event_type", where)
        if not row["description"]:
            err(f"{where}: missing description")

    seen = set()
    for row in geometry:
        where = f"project_geometry {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        check_enum(row["kind"], GEOMETRY_KINDS, "kind", where)
        check_enum(row["precision"], PRECISIONS, "precision", where)
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        if not row["geometry"]:
            err(f"{where}: missing geometry")
        else:
            try:
                json.loads(row["geometry"])
            except json.JSONDecodeError:
                err(f"{where}: geometry is not valid JSON")

    seen = set()
    for row in corridors:
        where = f"corridors {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        for field in ("name", "island", "definition", "metric", "notes"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        total = check_number(row["total_km"], "total_km", where)
        operational = check_number(row["operational_km"], "operational_km", where)
        construction = check_number(row["construction_km"], "construction_km", where)
        planned = check_number(row["planned_km"], "planned_km", where)
        if total is not None:
            used = (operational or 0) + (construction or 0) + (planned or 0)
            if used > total * 1.05:
                err(f"{where}: operational + construction + planned exceeds total")
        if not is_blank(row["progress_pct"]):
            progress = float(row["progress_pct"])
            if not 0 <= progress <= 100:
                err(f"{where}: progress_pct must be 0-100")
        if row["as_of"]:
            check_date(row["as_of"], f"{where} as_of")
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")

    for row in segments:
        where = f"corridor_segments {row['id']}"
        if row["corridor_id"] not in corridor_ids:
            err(f"{where}: unknown corridor")
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        if row["geometry_id"] and row["geometry_id"] not in geometry_ids:
            err(f"{where}: unknown geometry")
        check_number(row["length_km"], "length_km", where, minimum=0.000001)
        if row["segment_type"]:
            check_enum(row["segment_type"], SEGMENT_TYPES, "segment_type", where)
        check_enum(row["status"], STATUSES, "status", where)
        if row["opened_year"]:
            check_year(row["opened_year"], "opened_year", where)
        if row["expected_open_year"]:
            check_year(row["expected_open_year"], "expected_open_year", where)
        check_number(row["operational_km"], "operational_km", where)
        check_number(row["construction_km"], "construction_km", where)
        if row["progress_pct"]:
            progress = check_number(row["progress_pct"], "progress_pct", where)
            if progress is not None and not 0 <= progress <= 100:
                err(f"{where}: progress_pct must be 0-100")

    seen = set()
    for row in estates:
        where = f"estates {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        for field in ("name", "type", "province", "regency", "island", "lat", "lon",
                      "precision", "coordinate_source", "area_ha", "developer",
                      "status", "source_id", "last_verified", "notes"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        check_enum(row["type"], ESTATE_TYPES, "type", where)
        check_enum(row["status"], ESTATE_STATUSES, "status", where)
        check_enum(row["precision"], PRECISIONS, "precision", where)
        check_enum(row["island"], ISLANDS, "island", where)
        check_enum(row["coordinate_source"], COORDINATE_SOURCES, "coordinate_source", where)
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        if row["developer_org_id"] and row["developer_org_id"] not in org_ids:
            err(f"{where}: unknown developer_org_id")
        check_date(row["last_verified"], f"{where} last_verified")
        area = check_number(row["area_ha"], "area_ha", where, minimum=0.0001)
        if area is None:
            err(f"{where}: area_ha must be positive")
        if row["occupancy_pct"]:
            occupancy = check_number(row["occupancy_pct"], "occupancy_pct", where)
            if occupancy is not None and occupancy > 100:
                err(f"{where}: occupancy_pct must be <= 100")
        try:
            lat = float(row["lat"])
            lon = float(row["lon"])
        except ValueError:
            err(f"{where}: lat/lon are not numbers")
        else:
            if not (-11.0 <= lat <= 6.0 and 95.0 <= lon <= 141.0):
                err(f"{where}: coordinates outside Indonesia ({lat}, {lon})")
        if row["established_year"]:
            year = as_int(row["established_year"])
            if year is None or not 1945 <= year <= 2030:
                err(f"{where}: implausible established_year")
        if row["website"]:
            check_url(row["website"], where)

    seen = set()
    for row in estate_sources:
        where = f"estate_sources {row['estate_id']}/{row['source_id']}"
        if row["estate_id"] not in estate_ids:
            err(f"{where}: unknown estate")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        if not row["claim"]:
            err(f"{where}: missing claim")
        elif "," in row["claim"]:
            err(f"{where}: claim must be one atomic type, got {row['claim']!r}")
        elif row["claim"] not in CLAIM_TYPES:
            err(f"{where}: unknown claim type {row['claim']!r}")
        if row["claim_date"]:
            check_date(row["claim_date"], f"{where} claim_date")
        key = (row["estate_id"], row["source_id"], row["claim"])
        if key in seen:
            err(f"{where}: duplicate claim")
        seen.add(key)

    seen = set()
    for row in conflicts:
        where = f"conflicts {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        check_enum(row["scope"], CONFLICT_SCOPES, "scope", where)
        check_enum(row["status"], CONFLICT_STATUSES, "status", where)
        for field in ("subject", "field", "value_a", "value_b", "resolution"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        for field in ("source_a", "source_b"):
            if row[field] not in source_ids:
                err(f"{where}: unknown {field} {row[field]!r}")
        if row["project_id"] and row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if row["estate_id"] and row["estate_id"] not in estate_ids:
            err(f"{where}: unknown estate")
        if row["corridor_id"] and row["corridor_id"] not in corridor_ids:
            err(f"{where}: unknown corridor")
        if row["scope"] == "project" and not row["project_id"]:
            err(f"{where}: project scope needs project_id")
        if row["scope"] == "corridor" and not row["corridor_id"]:
            err(f"{where}: corridor scope needs corridor_id")
        if row["scope"] == "estate" and not row["estate_id"]:
            err(f"{where}: estate scope needs estate_id")

    seen = set()
    for row in coverage:
        where = f"coverage_targets {row['layer'] or '?'}"
        if not row["layer"]:
            err(f"{where}: missing layer")
        if row["layer"] in seen:
            err(f"{where}: duplicate layer")
        seen.add(row["layer"])
        for field in ("label", "unit", "universe"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        target = as_int(row["target_count"])
        if target is None or target <= 0:
            err(f"{where}: target_count must be a positive integer")
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")

    if errors:
        print(f"{len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        sys.exit(1)

    print(
        f"OK: {len(projects)} projects, {len(estates)} estates, "
        f"{len(organizations)} organisations, {len(sources)} sources, "
        f"{len(corridors)} corridors, {len(segments)} segments, "
        f"{len(events)} events, {len(geometry)} geometry, {len(investments)} investments, "
        f"{len(conflicts)} conflicts"
    )


if __name__ == "__main__":
    main()
