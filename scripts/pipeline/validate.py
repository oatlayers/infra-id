"""Validate the curated CSV tables and their foreign keys.

Run: python scripts/pipeline/validate.py
Exits non-zero on any error.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
    INDICATOR_DIRECTIONS,
    INSTRUMENTS,
    ISLANDS,
    LANGUAGES,
    LAW_LEVELS,
    ORG_TYPES,
    PKPN_IDS,
    PRECISIONS,
    PROGRAMME_ROLES,
    PROGRAMME_STATUSES,
    PROGRAMME_THEMES,
    PSN_VALUES,
    ROLES,
    ROOT,
    SECTORS,
    SEGMENT_TYPES,
    SOURCE_TYPES,
    STAGES,
    STATUSES,
    TABLES,
    TRANSLATION_ENTITY_TYPES,
    TRANSLATION_FIELDS_BY_ENTITY,
    TRANSLATION_STATUSES,
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
    programmes = read_csv(CURATED / "programmes.csv")
    programme_projects = read_csv(CURATED / "programme_projects.csv")
    programme_sources = read_csv(CURATED / "programme_sources.csv")
    translations = read_csv(CURATED / "translations.csv")
    pkpn_programmes = read_csv(CURATED / "pkpn_programmes.csv")
    pkpn_sources = read_csv(CURATED / "pkpn_sources.csv")
    indicators = read_csv(CURATED / "indicators.csv")
    indicator_values = read_csv(CURATED / "indicator_values.csv")
    phases = read_csv(CURATED / "project_phases.csv")
    register = read_csv(CURATED / "psn_register.csv")

    project_ids = {row["id"] for row in projects}
    org_ids = {row["id"] for row in organizations}
    source_ids = {row["id"] for row in sources}
    corridor_ids = {row["id"] for row in corridors}
    law_ids = {row["id"] for row in laws}
    estate_ids = {row["id"] for row in estates}
    geometry_ids = {row["id"] for row in geometry}
    programme_ids = {row["id"] for row in programmes}

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
        if not is_blank(row["opened_year"]) and (
            opened is None or not 1900 <= opened <= 2030
        ):
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
        register_only = (
            row["status"] == "unknown" and row["coordinate_source"] == "unknown"
        )
        required = [
            "name", "type", "province", "island", "lat", "lon", "precision",
            "coordinate_source", "status", "source_id", "last_verified", "notes",
        ]
        if not register_only:
            required += ["regency", "area_ha", "developer"]
        for field in required:
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        if register_only and row["precision"] != "province":
            err(f"{where}: register-only estates need province precision")
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
        if area is None and not register_only:
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

    register_names = {
        (row["kind"], int(row["psn_no"])): row["name_id"]
        for row in register
        if row["status"] == "active"
    }
    active_programme_numbers = {
        number for (kind, number) in register_names if kind == "programme"
    }

    seen_ids: set[str] = set()
    seen_numbers: set[int] = set()
    for row in programmes:
        where = f"programmes {row['id'] or '?'}"
        if row["id"] in seen_ids:
            err(f"{where}: duplicate id")
        seen_ids.add(row["id"])
        check_id(row["id"], where)
        for field in (
            "name_id", "name_en", "theme", "psn_no", "summary_id", "summary_en",
            "status", "source_id", "last_verified", "notes",
        ):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        check_enum(row["theme"], PROGRAMME_THEMES, "theme", where)
        check_enum(row["status"], PROGRAMME_STATUSES, "status", where)
        number = as_int(row["psn_no"])
        if number is None or not 1 <= number <= 25:
            err(f"{where}: psn_no must be 1-25")
        elif number in seen_numbers:
            err(f"{where}: duplicate psn_no {number}")
        else:
            seen_numbers.add(number)
        if row["psn_no"] and number is not None:
            expected = register_names.get(("programme", number))
            if expected is None:
                err(f"{where}: psn_no {number} is not an active register programme")
            elif row["name_id"] != expected:
                err(f"{where}: name_id does not match the register")
        if row["pkpn_id"]:
            check_enum(row["pkpn_id"], PKPN_IDS, "pkpn_id", where)
        if row["lead_org_id"] and row["lead_org_id"] not in org_ids:
            err(f"{where}: unknown lead_org_id {row['lead_org_id']!r}")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        check_date(row["last_verified"], f"{where} last_verified")
        start = check_year(row["start_year"], "start_year", where) if row["start_year"] else None
        target = check_year(row["target_year"], "target_year", where) if row["target_year"] else None
        if start is not None and target is not None and target < start:
            err(f"{where}: target_year is before start_year")
        check_number(row["budget_idr_t"], "budget_idr_t", where)

    if seen_numbers != active_programme_numbers:
        missing = sorted(active_programme_numbers - seen_numbers)
        extra = sorted(seen_numbers - active_programme_numbers)
        err(f"programmes: register coverage mismatch; missing {missing}, extra {extra}")

    seen = set()
    for row in programme_projects:
        where = f"programme_projects {row['programme_id']}/{row['project_id']}"
        if row["programme_id"] not in programme_ids:
            err(f"{where}: unknown programme")
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        check_enum(row["role"], PROGRAMME_ROLES, "role", where)
        key = (row["programme_id"], row["project_id"])
        if key in seen:
            err(f"{where}: duplicate link")
        seen.add(key)

    seen = set()
    for row in programme_sources:
        where = f"programme_sources {row['programme_id']}/{row['source_id']}"
        if row["programme_id"] not in programme_ids:
            err(f"{where}: unknown programme")
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
        key = (row["programme_id"], row["source_id"], row["claim"])
        if key in seen:
            err(f"{where}: duplicate claim")
        seen.add(key)

    translation_entities = {
        "project": project_ids,
        "programme": programme_ids,
        "corridor": corridor_ids,
        "estate": estate_ids,
    }
    seen = set()
    for row in translations:
        where = "translations {}/{}/{}".format(
            row["entity_type"] or "?", row["entity_id"] or "?", row["field"] or "?"
        )
        check_enum(row["entity_type"], TRANSLATION_ENTITY_TYPES, "entity_type", where)
        check_enum(row["locale"], {"en", "id"}, "locale", where)
        check_enum(row["status"], TRANSLATION_STATUSES, "status", where)
        allowed_fields = TRANSLATION_FIELDS_BY_ENTITY.get(row["entity_type"], set())
        if row["field"] not in allowed_fields:
            err(f"{where}: field is not valid for {row['entity_type'] or '?'}")
        if row["entity_id"] not in translation_entities.get(row["entity_type"], set()):
            err(f"{where}: unknown {row['entity_type'] or '?'} id")
        if row["status"] == "missing":
            if row["text"]:
                err(f"{where}: a missing row must not carry text")
        elif is_blank(row["text"]):
            err(f"{where}: missing text")
        if row["status"] in {"official", "reviewed"}:
            if not row["translator"]:
                err(f"{where}: reviewed translations need a translator")
            if not row["reviewed_on"]:
                err(f"{where}: reviewed translations need reviewed_on")
        if row["reviewed_on"]:
            check_date(row["reviewed_on"], f"{where} reviewed_on")
        if row["source_id"] and row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        key = (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        if key in seen:
            err(f"{where}: duplicate translation")
        seen.add(key)

    seen = set()
    pkpn_ids = set()
    for row in pkpn_programmes:
        where = f"pkpn_programmes {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        pkpn_ids.add(row["id"])
        check_id(row["id"], where)
        for field in ("name_en", "name_id", "summary_en", "summary_id"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        check_enum(row["theme"], PROGRAMME_THEMES, "theme", where)
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        check_date(row["last_verified"], f"{where} last_verified")
        check_number(row["budget_idr_t"], "budget_idr_t", where)
    if pkpn_ids != PKPN_IDS:
        missing = sorted(PKPN_IDS - pkpn_ids)
        extra = sorted(pkpn_ids - PKPN_IDS)
        err(f"pkpn_programmes: id mismatch; missing {missing}, extra {extra}")

    seen = set()
    for row in pkpn_sources:
        where = f"pkpn_sources {row['programme_id']}/{row['source_id']}"
        if row["programme_id"] not in pkpn_ids:
            err(f"{where}: unknown programme")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        if not row["claim"]:
            err(f"{where}: missing claim")
        elif "," in row["claim"]:
            err(f"{where}: claim must be one atomic type")
        elif row["claim"] not in CLAIM_TYPES:
            err(f"{where}: unknown claim type {row['claim']!r}")
        if row["claim_date"]:
            check_date(row["claim_date"], f"{where} claim_date")
        key = (row["programme_id"], row["source_id"], row["claim"])
        if key in seen:
            err(f"{where}: duplicate claim")
        seen.add(key)

    all_programme_ids = programme_ids | pkpn_ids
    seen = set()
    represented_indicators = set()
    for row in indicators:
        where = f"indicators {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        if not row["programme_id"] and not row["project_id"]:
            err(f"{where}: needs programme_id or project_id")
        if row["programme_id"] and row["programme_id"] not in all_programme_ids:
            err(f"{where}: unknown programme_id")
        if row["project_id"] and row["project_id"] not in project_ids:
            err(f"{where}: unknown project_id")
        for field in ("name_en", "name_id", "unit"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        check_enum(row["direction"], INDICATOR_DIRECTIONS, "direction", where)
        check_number(row["baseline_value"], "baseline_value", where)
        check_number(row["target_value"], "target_value", where)
        if row["baseline_date"]:
            check_date(row["baseline_date"], f"{where} baseline_date")
        if row["target_date"]:
            check_date(row["target_date"], f"{where} target_date")
        if row["baseline_date"] and row["target_date"] and row["target_date"] < row["baseline_date"]:
            err(f"{where}: target_date is before baseline_date")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")

    seen_values = set()
    for row in indicator_values:
        where = f"indicator_values {row['indicator_id'] or '?'}/{row['as_of'] or '?'}"
        if row["indicator_id"] not in seen:
            err(f"{where}: unknown indicator_id")
        represented_indicators.add(row["indicator_id"])
        value = check_number(row["value"], "value", where)
        if value is None:
            err(f"{where}: value is required")
        if not row["as_of"]:
            err(f"{where}: missing as_of")
        else:
            check_date(row["as_of"], f"{where} as_of")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")
        key = (row["indicator_id"], row["as_of"], row["source_id"])
        if key in seen_values:
            err(f"{where}: duplicate value")
        seen_values.add(key)

    for row in indicators:
        if row["baseline_value"] or row["target_value"]:
            represented_indicators.add(row["id"])
    missing_values = sorted(set(row["id"] for row in indicators) - represented_indicators)
    if missing_values:
        err(f"indicators: no baseline, target or value for {missing_values}")

    seen = set()
    for row in phases:
        where = f"project_phases {row['id'] or '?'}"
        if row["id"] in seen:
            err(f"{where}: duplicate id")
        seen.add(row["id"])
        check_id(row["id"], where)
        if row["project_id"] not in project_ids:
            err(f"{where}: unknown project_id")
        for field in ("phase", "name_en", "name_id"):
            if is_blank(row[field]):
                err(f"{where}: missing {field}")
        check_enum(row["status"], STATUSES, "status", where)
        check_number(row["cost_idr_t"], "cost_idr_t", where)
        progress = check_number(row["progress_pct"], "progress_pct", where)
        if progress is not None and progress > 100:
            err(f"{where}: progress_pct must be <= 100")
        if row["start_date"]:
            check_date(row["start_date"], f"{where} start_date")
        if row["end_date"]:
            check_date(row["end_date"], f"{where} end_date")
        if row["start_date"] and row["end_date"] and row["end_date"] < row["start_date"]:
            err(f"{where}: end_date is before start_date")
        if row["source_id"] not in source_ids:
            err(f"{where}: unknown source")

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
        for field in ("label", "unit", "reference_set"):
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
        f"{len(conflicts)} conflicts, {len(programmes)} programmes, "
        f"{len(pkpn_programmes)} PKPN programmes, {len(indicators)} indicators, "
        f"{len(indicator_values)} indicator values, {len(phases)} phases"
    )


if __name__ == "__main__":
    main()
