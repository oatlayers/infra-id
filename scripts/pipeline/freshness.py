"""Report row-level verification age.

The atlas treats a row as stale after 183 days (six months). This script writes
one row per project and estate, with the refresh date and a fresh / due_soon /
stale state.

The default as-of date is the newest ``last_verified`` in the curated tables, so
a rebuild is deterministic. Pass ``--as-of YYYY-MM-DD`` (or set INFRAA_AS_OF)
for a real monthly check.

Run: python scripts/pipeline/freshness.py [--as-of YYYY-MM-DD]
Writes: data/derived/freshness_report.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import os
from datetime import date, timedelta

from data_model import CURATED, DERIVED, read_csv, write_csv

STALE_DAYS = 183
DUE_SOON_DAYS = 153
FIELDS = [
    "entity_type", "entity_id", "name", "layer", "status", "last_verified",
    "age_days", "state", "refresh_due", "notes",
]


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def state_for(age: int | None) -> str:
    if age is None:
        return "unknown"
    if age > STALE_DAYS:
        return "stale"
    if age > DUE_SOON_DAYS:
        return "due_soon"
    return "fresh"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default="", help="report date, YYYY-MM-DD")
    args = parser.parse_args()

    projects = read_csv(CURATED / "projects.csv")
    estates = read_csv(CURATED / "estates.csv")
    dates = [row["last_verified"] for row in projects + estates if row["last_verified"]]
    default_as_of = max(dates) if dates else date.today().isoformat()
    as_of_text = args.as_of or os.environ.get("INFRAA_AS_OF", "") or default_as_of
    as_of = parse_date(as_of_text)
    if as_of is None:
        raise SystemExit(f"invalid --as-of date: {as_of_text!r}")

    rows = []
    for entity_type, records, layer_field in (
        ("project", projects, "sector"),
        ("estate", estates, "type"),
    ):
        for record in records:
            verified = parse_date(record["last_verified"])
            age = (as_of - verified).days if verified else None
            rows.append(
                {
                    "entity_type": entity_type,
                    "entity_id": record["id"],
                    "name": record["name"],
                    "layer": record[layer_field],
                    "status": record["status"],
                    "last_verified": record["last_verified"],
                    "age_days": str(age) if age is not None else "",
                    "state": state_for(age),
                    "refresh_due": (
                        (verified + timedelta(days=STALE_DAYS)).isoformat()
                        if verified
                        else ""
                    ),
                    "notes": record["notes"][:160],
                }
            )

    rows.sort(key=lambda row: (row["last_verified"], row["entity_type"], row["entity_id"]))
    write_csv(DERIVED / "freshness_report.csv", FIELDS, rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["state"]] = counts.get(row["state"], 0) + 1
    print(f"OK: {len(rows)} rows as of {as_of.isoformat()}: {counts}")


if __name__ == "__main__":
    main()
