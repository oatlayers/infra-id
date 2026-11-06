"""Validate data/projects.csv.

Checks required fields, allowed values, coordinates, dates, duplicate ids and
placeholder rows. Exits non-zero on any error.

Run: python scripts/validate.py
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "projects.csv"

REQUIRED = [
    "id",
    "name",
    "sector",
    "status",
    "status_basis",
    "province",
    "route",
    "length_km",
    "operator",
    "lat",
    "lon",
    "precision",
    "source_url",
    "source_type",
    "retrieved_on",
    "last_verified",
    "notes",
]
SECTORS = {"road", "airport", "seaport", "factory"}
STATUSES = {"planned", "under_construction", "recently_completed", "stalled"}
PRECISIONS = {"exact", "approximate", "regency", "province"}
SOURCE_TYPES = {"official", "secondary"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> None:
    errors: list[str] = []
    with CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    if not rows:
        errors.append("CSV is empty")

    seen: set[str] = set()
    for line, row in enumerate(rows, start=2):
        where = f"line {line} ({row.get('id', '?')})"

        for field in REQUIRED:
            if field not in row or row[field].strip() == "":
                errors.append(f"{where}: missing {field}")

        if row["id"] in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(row["id"])

        if not ID.match(row["id"]):
            errors.append(f"{where}: id must be lowercase-hyphenated")
        if row["sector"] not in SECTORS:
            errors.append(f"{where}: bad sector {row['sector']!r}")
        if row["status"] not in STATUSES:
            errors.append(f"{where}: bad status {row['status']!r}")
        if row["precision"] not in PRECISIONS:
            errors.append(f"{where}: bad precision {row['precision']!r}")
        if row["source_type"] not in SOURCE_TYPES:
            errors.append(f"{where}: bad source_type {row['source_type']!r}")
        if not row["source_url"].startswith(("http://", "https://")):
            errors.append(f"{where}: source_url is not a URL")

        for field in ("retrieved_on", "last_verified"):
            if not DATE.match(row[field]):
                errors.append(f"{where}: {field} is not YYYY-MM-DD")
            else:
                try:
                    date.fromisoformat(row[field])
                except ValueError:
                    errors.append(f"{where}: {field} is not a real date")

        try:
            lat = float(row["lat"])
            lon = float(row["lon"])
        except ValueError:
            errors.append(f"{where}: lat/lon are not numbers")
        else:
            if not (-11.0 <= lat <= 6.0 and 95.0 <= lon <= 141.0):
                errors.append(f"{where}: coordinates outside Indonesia ({lat}, {lon})")

        try:
            length = float(row["length_km"])
        except ValueError:
            errors.append(f"{where}: length_km is not a number")
        else:
            if length <= 0:
                errors.append(f"{where}: length_km must be positive")

        haystack = " ".join(row.values()).upper()
        if "TEST" in haystack or "PENTEST" in haystack:
            errors.append(f"{where}: placeholder or test entry")

    if errors:
        print(f"{len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        sys.exit(1)

    print(f"OK: {len(rows)} rows validated")


if __name__ == "__main__":
    main()
