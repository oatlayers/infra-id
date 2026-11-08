"""Audit per-fact claim coverage.

For every project, check that the status and each populated numeric fact has a
matching atomic claim. Investment rows in ``investments.csv`` satisfy the
investment check even when no duplicate claim exists.

Run: python scripts/pipeline/audit_claims.py
Writes: data/derived/claims_audit.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import CURATED, DERIVED, read_csv, write_csv

FIELDS = [
    "project_id", "name", "sector", "verification", "claim_count", "source_count",
    "status_claim", "length_claim", "operational_claim", "progress_claim",
    "investment_claim", "capacity_claim", "opening_claim", "location_claim",
    "missing", "status_basis",
]

CAPACITY_CLAIMS = {"capacity", "design capacity", "current capacity"}


def main() -> None:
    projects = read_csv(CURATED / "projects.csv")
    claims = read_csv(CURATED / "project_sources.csv")
    investments = read_csv(CURATED / "investments.csv")

    by_project: dict[str, list[dict[str, str]]] = {}
    for claim in claims:
        by_project.setdefault(claim["project_id"], []).append(claim)

    invested = {row["project_id"] for row in investments}

    rows = []
    totals: dict[str, int] = {}
    missing_total = 0
    for project in projects:
        project_claims = by_project.get(project["id"], [])
        kinds = {row["claim"] for row in project_claims}
        sources = {row["source_id"] for row in project_claims}
        checks = {
            "status_claim": "status" in kinds,
            "length_claim": "length" in kinds or not project["length_km"],
            "operational_claim": "operational" in kinds or not project["operational_km"],
            "progress_claim": "progress" in kinds or not project["progress_pct"],
            "investment_claim": (
                "investment" in kinds
                or project["id"] in invested
                or not project["investment_idr_t"]
            ),
            "capacity_claim": bool(kinds & CAPACITY_CLAIMS) or not project["capacity"],
            "opening_claim": "opening" in kinds or not project["opened_year"],
            "location_claim": bool(kinds & {"location", "coordinates"}),
        }
        missing = [key.removesuffix("_claim") for key, ok in checks.items() if not ok]
        missing_total += len(missing)
        for key, ok in checks.items():
            if not ok:
                totals[key] = totals.get(key, 0) + 1
        rows.append(
            {
                "project_id": project["id"],
                "name": project["name"],
                "sector": project["sector"],
                "verification": project["verification"],
                "claim_count": str(len(project_claims)),
                "source_count": str(len(sources)),
                "status_claim": "yes" if checks["status_claim"] else "no",
                "length_claim": "yes" if checks["length_claim"] else "no",
                "operational_claim": "yes" if checks["operational_claim"] else "no",
                "progress_claim": "yes" if checks["progress_claim"] else "no",
                "investment_claim": "yes" if checks["investment_claim"] else "no",
                "capacity_claim": "yes" if checks["capacity_claim"] else "no",
                "opening_claim": "yes" if checks["opening_claim"] else "no",
                "location_claim": "yes" if checks["location_claim"] else "no",
                "missing": ";".join(missing) if missing else "none",
                "status_basis": project["status_basis"],
            }
        )

    write_csv(DERIVED / "claims_audit.csv", FIELDS, rows)

    complete = sum(1 for row in rows if row["missing"] == "none")
    print(
        f"OK: {len(rows)} projects, {len(claims)} claims; "
        f"{complete}/{len(rows)} fully claimed; missing: {totals or 'none'}"
    )


if __name__ == "__main__":
    main()
