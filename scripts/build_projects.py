"""Build the flat project export from the curated tables.

Reads data/curated/*.csv, fills gaps from the BPJT toll-road snapshot, joins the
primary operator and source, and writes data/projects.csv. The flat file is what
the site and external users consume; it is not the source of truth.

Run: python scripts/build_projects.py
"""

from __future__ import annotations

import json

from data_model import (
    CURATED,
    DERIVED_FIELDS,
    ROOT,
    is_blank,
    num,
    read_csv,
    write_csv,
)

BPJT_PATH = ROOT / "data" / "raw" / "2026-11-06" / "bpjt_toll_road_list.json"
OUT = ROOT / "data" / "projects.csv"

OPTIONAL_BLANK = {
    "subsector",
    "corridor_id",
    "length_km",
    "operational_km",
    "construction_km",
    "progress_pct",
    "investment_idr_t",
    "capacity",
    "capacity_unit",
    "opened_year",
}


def main() -> None:
    projects = read_csv(CURATED / "projects.csv")
    organizations = {row["id"]: row for row in read_csv(CURATED / "organizations.csv")}
    sources = {row["id"]: row for row in read_csv(CURATED / "sources.csv")}
    external = {
        row["project_id"]: row["external_id"]
        for row in read_csv(CURATED / "project_external_ids.csv")
        if row["system"] == "bpjt-ruas"
    }

    operators: dict[str, list[str]] = {}
    for link in read_csv(CURATED / "project_organizations.csv"):
        if link["role"] != "operator":
            continue
        org = organizations.get(link["org_id"])
        if org:
            operators.setdefault(link["project_id"], []).append(org["name"])

    links: dict[str, list[dict[str, str]]] = {}
    for link in read_csv(CURATED / "project_sources.csv"):
        source = sources.get(link["source_id"])
        if source:
            links.setdefault(link["project_id"], []).append(source)

    bpjt = {
        row["ruas_name"]: row
        for row in json.loads(BPJT_PATH.read_text(encoding="utf-8-sig"))["data"]
    }

    rows: list[dict[str, str]] = []
    for project in projects:
        row = dict(project)
        if not row["psn"]:
            row["psn"] = "unknown"

        bpjt_name = external.get(row["id"])
        if bpjt_name:
            if bpjt_name not in bpjt:
                raise SystemExit(f"{row['id']}: BPJT row not found: {bpjt_name}")
            official = bpjt[bpjt_name]
            if is_blank(row["length_km"]):
                row["length_km"] = num(official.get("length"))
            if is_blank(row["operational_km"]):
                row["operational_km"] = num(official.get("panjang_operasi_km"))
            if is_blank(row["construction_km"]):
                row["construction_km"] = num(official.get("panjang_konstruksi_km"))
            if row["psn"] == "unknown":
                row["psn"] = "yes" if official.get("psn_status") == "PSN" else "no"
            if is_blank(row["lat"]) or is_blank(row["lon"]):
                try:
                    row["lat"] = (
                        f"{(float(official['start_latitude']) + float(official['end_latitude'])) / 2:.5f}"
                    )
                    row["lon"] = (
                        f"{(float(official['start_longitude']) + float(official['end_longitude'])) / 2:.5f}"
                    )
                except (TypeError, ValueError):
                    pass

        row["operator"] = "; ".join(operators.get(row["id"], [])) or "tba"

        candidates = links.get(row["id"], [])
        official_sources = [s for s in candidates if s["source_type"] == "official"]
        chosen = official_sources or candidates
        if not chosen:
            raise SystemExit(f"{row['id']}: no source linked")
        source = chosen[0]
        row["source_url"] = source["url"]
        row["source_type"] = source["source_type"]
        row["retrieved_on"] = source["retrieved_on"]

        missing = [
            field
            for field in DERIVED_FIELDS
            if is_blank(row.get(field, "")) and field not in OPTIONAL_BLANK
        ]
        if missing:
            raise SystemExit(f"{row['id']}: missing {missing}")

        rows.append({field: row.get(field, "") for field in DERIVED_FIELDS})

    write_csv(OUT, DERIVED_FIELDS, rows)

    by_status: dict[str, int] = {}
    by_sector: dict[str, int] = {}
    for row in rows:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
        by_sector[row["sector"]] = by_sector.get(row["sector"], 0) + 1
    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")
    print("status:", by_status)
    print("sector:", by_sector)


if __name__ == "__main__":
    main()
