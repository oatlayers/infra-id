"""Import the 35 transport PSN rows into the curated tables.

Reads data/derived/transport_psn.csv (the checked extraction from the Kemenhub
review) and upserts projects, source claims, organisation links and aliases.
Idempotent: transport rows are replaced, road and estate rows are untouched.

Run after extract_transport_psn.py:

    python scripts/imports/extract_transport_psn.py
    python scripts/imports/build_transport.py
    python scripts/pipeline/validate.py
    python scripts/pipeline/build_projects.py
    python scripts/pipeline/build_site_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CURATED,
    DERIVED,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    ALIAS_FIELDS,
    ORG_FIELDS,
    read_csv,
    write_csv,
)

STAGING = DERIVED / "transport_psn.csv"
SOURCE_ID = "src-kemenhub-psn-progress-2026-02-19"
STATUS_AS_OF = "2026-02-19"
LAST_VERIFIED = "2026-11-07"

ORGANIZATIONS = [
    {
        "id": "org-kemenhub",
        "name": "Ministry of Transportation",
        "short_name": "Kemenhub",
        "org_type": "government",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://www.kemenhub.go.id",
        "notes": "National transport ministry; sponsor of the 35 transport PSNs.",
    },
    {
        "id": "org-ditjen-perkeretaapian",
        "name": "Directorate General of Railways",
        "short_name": "DJKA",
        "org_type": "government",
        "country_code": "ID",
        "parent_id": "org-kemenhub",
        "website": "",
        "notes": "Owner of the railway PSNs.",
    },
    {
        "id": "org-ditjen-perhubungan-laut",
        "name": "Directorate General of Sea Transportation",
        "short_name": "Hubla",
        "org_type": "government",
        "country_code": "ID",
        "parent_id": "org-kemenhub",
        "website": "",
        "notes": "Owner of the seaport PSNs.",
    },
    {
        "id": "org-ditjen-perhubungan-udara",
        "name": "Directorate General of Civil Aviation",
        "short_name": "Hubud",
        "org_type": "government",
        "country_code": "ID",
        "parent_id": "org-kemenhub",
        "website": "",
        "notes": "Owner of the airport PSNs.",
    },
    {
        "id": "org-kai",
        "name": "PT Kereta Api Indonesia (Persero)",
        "short_name": "KAI",
        "org_type": "soe",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://www.kai.id",
        "notes": "State railway operator.",
    },
    {
        "id": "org-kcic",
        "name": "PT Kereta Cepat Indonesia China",
        "short_name": "KCIC",
        "org_type": "consortium",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://whoosh.co.id",
        "notes": "Jakarta–Bandung high-speed rail consortium.",
    },
    {
        "id": "org-mrt-jakarta",
        "name": "PT MRT Jakarta (Persero)",
        "short_name": "MRT Jakarta",
        "org_type": "soe",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://www.mrtjakarta.co.id",
        "notes": "Jakarta metro operator and developer.",
    },
    {
        "id": "org-lrt-jakarta",
        "name": "PT LRT Jakarta",
        "short_name": "LRT Jakarta",
        "org_type": "soe",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://www.lrtjakarta.co.id",
        "notes": "Jakarta LRT operator.",
    },
    {
        "id": "org-lrt-sumsel",
        "name": "PT LRT Sumatera Selatan",
        "short_name": "LRT Sumsel",
        "org_type": "soe",
        "country_code": "ID",
        "parent_id": "",
        "website": "",
        "notes": "South Sumatra LRT operator.",
    },
    {
        "id": "org-bayan-laju-trans-kalimantan",
        "name": "PT Bayan Laju Trans Kalimantan",
        "short_name": "BLTK",
        "org_type": "private",
        "country_code": "ID",
        "parent_id": "",
        "website": "",
        "notes": "Developer of the East Kalimantan logistics railway.",
    },
    {
        "id": "org-angakasa-pura-i",
        "name": "PT Angkasa Pura I (Persero)",
        "short_name": "AP I",
        "org_type": "soe",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://www.angkasapura1.co.id",
        "notes": "Airport operator for central and eastern Indonesia.",
    },
    {
        "id": "org-angakasa-pura-ii",
        "name": "PT Angkasa Pura II (Persero)",
        "short_name": "AP II",
        "org_type": "soe",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://www.angkasapura2.co.id",
        "notes": "Airport operator for western Indonesia.",
    },
    {
        "id": "org-pelindo",
        "name": "PT Pelabuhan Indonesia (Persero)",
        "short_name": "Pelindo",
        "org_type": "soe",
        "country_code": "ID",
        "parent_id": "",
        "website": "https://www.pelindo.co.id",
        "notes": "State port operator formed by the 2021 merger of Pelindo I–IV.",
    },
]

SECTOR_OWNER = {
    "railway": "org-ditjen-perkeretaapian",
    "seaport": "org-ditjen-perhubungan-laut",
    "airport": "org-ditjen-perhubungan-udara",
}


def upsert(rows: list[dict[str, str]], key: str, incoming: dict[str, str]) -> None:
    for index, row in enumerate(rows):
        if row[key] == incoming[key]:
            rows[index] = {**row, **incoming}
            return
    rows.append(incoming)


def main() -> None:
    staging = read_csv(STAGING)
    if len(staging) != 35:
        raise SystemExit(f"expected 35 staging rows, got {len(staging)}")

    projects = read_csv(CURATED / "projects.csv")
    organizations = read_csv(CURATED / "organizations.csv")
    claims = read_csv(CURATED / "project_sources.csv")
    links = read_csv(CURATED / "project_organizations.csv")
    aliases = read_csv(CURATED / "project_aliases.csv")
    sources = {row["id"] for row in read_csv(CURATED / "sources.csv")}

    if SOURCE_ID not in sources:
        raise SystemExit(f"missing source {SOURCE_ID}")

    for org in ORGANIZATIONS:
        upsert(organizations, "id", org)

    ids = {row["id"] for row in staging}

    # Drop previous transport rows, claims, links and aliases so the import is
    # idempotent. Road, estate and factory rows are untouched.
    projects = [row for row in projects if row["id"] not in ids]
    claims = [row for row in claims if row["project_id"] not in ids]
    links = [row for row in links if row["project_id"] not in ids]
    aliases = [row for row in aliases if row["project_id"] not in ids]

    for item in staging:
        project = {
            "id": item["id"],
            "name": item["name"],
            "sector": item["sector"],
            "subsector": item["subsector"],
            "status": item["status"],
            "status_basis": item["status_basis"],
            "corridor_id": "",
            "island": item["island"],
            "province": item["province"],
            "route": item["route"],
            "length_km": "",
            "operational_km": "",
            "construction_km": "",
            "progress_pct": item["progress_pct"],
            "investment_idr_t": item["investment_idr_t"],
            "capacity": "",
            "capacity_unit": "",
            "psn": "yes",
            "opened_year": item["opened_year"],
            "opened_date": "",
            "expected_open_year": item["expected_open_year"],
            "status_as_of": STATUS_AS_OF,
            "verification": "official",
            "lat": item["lat"],
            "lon": item["lon"],
            "precision": "approximate",
            "last_verified": LAST_VERIFIED,
            "notes": item["notes"],
        }
        projects.append(project)

        def claim(kind: str, value: str) -> dict[str, str]:
            return {
                "project_id": item["id"],
                "source_id": SOURCE_ID,
                "claim": kind,
                "claim_value": value,
                "claim_date": STATUS_AS_OF,
                "notes": f"Kemenhub deck {item['page_ref']}.",
            }

        claims.append(claim("status", item["status"]))
        claims.append(claim("location", f"{item['province']} — {item['route']}"))
        if item["opened_year"]:
            claims.append(claim("opening", item["opened_year"]))
        if item["expected_open_year"]:
            claims.append(claim("target", item["expected_open_year"]))
        if item["investment_idr_t"]:
            claims.append(claim("investment", f"Rp {item['investment_idr_t']} T"))
        if item["progress_pct"]:
            claims.append(claim("progress", f"{item['progress_pct']}%"))

        def link(org_id: str, role: str) -> dict[str, str]:
            return {
                "project_id": item["id"],
                "org_id": org_id,
                "role": role,
                "share_pct": "",
                "start_year": "",
                "end_year": "",
                "source_id": SOURCE_ID,
                "notes": "",
            }

        links.append(link("org-kemenhub", "sponsor"))
        links.append(link(SECTOR_OWNER[item["sector"]], "owner"))
        if item["operator_org_id"]:
            links.append(link(item["operator_org_id"], "operator"))

        for alias in [part.strip() for part in item["aliases"].split(";") if part.strip()]:
            aliases.append(
                {
                    "project_id": item["id"],
                    "alias": alias,
                    "source_id": "",
                    "notes": "Common alternate name.",
                }
            )

    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, organizations)
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, links)
    write_csv(CURATED / "project_aliases.csv", ALIAS_FIELDS, aliases)

    print(
        f"imported {len(staging)} transport projects; "
        f"{len(projects)} projects, {len(organizations)} organisations, "
        f"{len(claims)} claims, {len(links)} links, {len(aliases)} aliases"
    )


if __name__ == "__main__":
    main()
