"""Normalise source claims into one atomic fact per row.

Phase 2 imported several claims as a comma-separated string, for example
``status,length,operator,location``. That made a per-fact audit impossible.
This script splits every claim into one row per type, lower-cases ``PSN``, and
backfills numeric claims that were only recorded on the project row.

Idempotent: rerunning it leaves the tables unchanged.

Run: python scripts/normalize_claims.py
Writes: data/curated/project_sources.csv, data/curated/estate_sources.csv
"""

from __future__ import annotations

from data_model import CLAIM_TYPES, CURATED, read_csv, write_csv

PROJECT_SOURCE_FIELDS = [
    "project_id", "source_id", "claim", "claim_value", "claim_date", "notes",
]
ESTATE_SOURCE_FIELDS = [
    "estate_id", "source_id", "claim", "claim_value", "claim_date", "notes",
]


def normalise(rows: list[dict[str, str]], key: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        for raw in row["claim"].split(","):
            claim = raw.strip()
            if not claim:
                continue
            if claim.casefold() == "psn":
                claim = "psn"
            if claim not in CLAIM_TYPES:
                raise SystemExit(f"{row[key]}: unknown claim type {claim!r}")
            signature = (row[key], row["source_id"], claim)
            if signature in seen:
                # Merge notes rather than drop a distinct explanation.
                for existing in out:
                    if (existing[key], existing["source_id"], existing["claim"]) == signature:
                        if row["notes"] and row["notes"] not in existing["notes"]:
                            existing["notes"] = "; ".join(
                                part for part in (existing["notes"], row["notes"]) if part
                            )
                        break
                continue
            seen.add(signature)
            out.append({**row, "claim": claim})
    return out


def claim_source(rows: list[dict[str, str]], project_id: str, claims: set[str]) -> str:
    for row in rows:
        if row["project_id"] == project_id and row["claim"] in claims:
            return row["source_id"]
    return ""


def main() -> None:
    projects = read_csv(CURATED / "projects.csv")
    project_sources = normalise(read_csv(CURATED / "project_sources.csv"), "project_id")
    estate_sources = normalise(read_csv(CURATED / "estate_sources.csv"), "estate_id")
    investments = read_csv(CURATED / "investments.csv")

    by_project: dict[str, set[str]] = {}
    for row in project_sources:
        by_project.setdefault(row["project_id"], set()).add(row["claim"])

    added = {"investment": 0, "operational": 0, "opening": 0, "location": 0}

    # Investment figures already live in investments.csv with their own source.
    investment_source = {
        row["project_id"]: row for row in investments if row["project_id"]
    }
    for project in projects:
        project_id = project["id"]
        if project["investment_idr_t"] and "investment" not in by_project.get(project_id, set()):
            investment = investment_source.get(project_id)
            if not investment:
                continue
            project_sources.append(
                {
                    "project_id": project_id,
                    "source_id": investment["source_id"],
                    "claim": "investment",
                    "claim_value": f"{investment['amount']} {investment['currency']}",
                    "claim_date": "",
                    "notes": "Backfilled from investments.csv; amount_idr_t is a ranking conversion.",
                }
            )
            by_project.setdefault(project_id, set()).add("investment")
            added["investment"] += 1

    for project in projects:
        project_id = project["id"]
        claims = by_project.get(project_id, set())
        if project["operational_km"] and "operational" not in claims:
            source_id = claim_source(project_sources, project_id, {"length"}) or claim_source(
                project_sources, project_id, {"status"}
            )
            if source_id:
                project_sources.append(
                    {
                        "project_id": project_id,
                        "source_id": source_id,
                        "claim": "operational",
                        "claim_value": project["operational_km"],
                        "claim_date": "",
                        "notes": "Backfilled from the curated operational_km figure.",
                    }
                )
                claims.add("operational")
                added["operational"] += 1
        if project["opened_year"] and "opening" not in claims:
            source_id = claim_source(project_sources, project_id, {"status"})
            if source_id:
                project_sources.append(
                    {
                        "project_id": project_id,
                        "source_id": source_id,
                        "claim": "opening",
                        "claim_value": project["opened_year"],
                        "claim_date": "",
                        "notes": "Backfilled from the curated opened_year figure.",
                    }
                )
                claims.add("opening")
                added["opening"] += 1
        if not claims & {"location", "coordinates"}:
            source_id = claim_source(project_sources, project_id, {"status"})
            if source_id:
                project_sources.append(
                    {
                        "project_id": project_id,
                        "source_id": source_id,
                        "claim": "location",
                        "claim_value": f"{project['lat']}, {project['lon']}",
                        "claim_date": "",
                        "notes": "Backfilled from the curated point; precision is recorded on the project row.",
                    }
                )
                claims.add("location")
                added["location"] += 1

    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, project_sources)
    write_csv(CURATED / "estate_sources.csv", ESTATE_SOURCE_FIELDS, estate_sources)
    print(
        f"OK: {len(project_sources)} project claims, {len(estate_sources)} estate claims; "
        f"backfilled {added['investment']} investment, {added['operational']} operational, "
        f"{added['opening']} opening, {added['location']} location claims"
    )


if __name__ == "__main__":
    main()
