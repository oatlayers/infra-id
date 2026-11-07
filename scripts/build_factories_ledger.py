"""Write the frozen 27-plant factory ledger for the 8 November 2026 build.

The ledger is derived from the curated tables after the factory import. It is a
reviewable snapshot, not a new source of truth: edit `data/curated/` and rerun
the import and this script.

Run: python scripts/build_factories_ledger.py
Writes: data/derived/factories_2026.csv
"""

from __future__ import annotations

from data_model import CURATED, DERIVED, read_csv, write_csv

FIELDS = [
    "id", "name", "subsector", "status", "province", "island", "route",
    "capacity", "capacity_unit", "investment_idr_t", "psn", "opened_year",
    "expected_open_year", "operator_org_id", "operator_name", "source_ids",
    "claim_count", "verification", "status_as_of", "last_verified",
    "status_basis", "notes",
]


def main() -> None:
    projects = read_csv(CURATED / "projects.csv")
    organizations = {row["id"]: row for row in read_csv(CURATED / "organizations.csv")}
    links = read_csv(CURATED / "project_organizations.csv")
    claims = read_csv(CURATED / "project_sources.csv")

    operator = {}
    for link in links:
        if link["role"] == "operator":
            operator.setdefault(link["project_id"], link["org_id"])

    sources_by_project: dict[str, list[str]] = {}
    counts: dict[str, int] = {}
    for claim in claims:
        sources_by_project.setdefault(claim["project_id"], [])
        if claim["source_id"] not in sources_by_project[claim["project_id"]]:
            sources_by_project[claim["project_id"]].append(claim["source_id"])
        counts[claim["project_id"]] = counts.get(claim["project_id"], 0) + 1

    rows = []
    for project in projects:
        if project["sector"] != "factory":
            continue
        org_id = operator.get(project["id"], "")
        rows.append(
            {
                "id": project["id"],
                "name": project["name"],
                "subsector": project["subsector"],
                "status": project["status"],
                "province": project["province"],
                "island": project["island"],
                "route": project["route"],
                "capacity": project["capacity"],
                "capacity_unit": project["capacity_unit"],
                "investment_idr_t": project["investment_idr_t"],
                "psn": project["psn"],
                "opened_year": project["opened_year"],
                "expected_open_year": project["expected_open_year"],
                "operator_org_id": org_id,
                "operator_name": organizations.get(org_id, {}).get("name", ""),
                "source_ids": ";".join(sources_by_project.get(project["id"], [])),
                "claim_count": str(counts.get(project["id"], 0)),
                "verification": project["verification"],
                "status_as_of": project["status_as_of"],
                "last_verified": project["last_verified"],
                "status_basis": project["status_basis"],
                "notes": project["notes"],
            }
        )

    rows.sort(key=lambda row: row["name"].casefold())
    write_csv(DERIVED / "factories_2026.csv", FIELDS, rows)
    print(f"OK: {len(rows)} factory rows -> data/derived/factories_2026.csv")


if __name__ == "__main__":
    main()
