"""Add the missing PSN toll corridors from the BPJT snapshot.

The curated road batch covers 27 corridors. The BPJT list has 15 more PSN
corridors that meet the atlas scope. This script upserts them with BPJT as the
official source, links the operator and external BPJT key, and records the
partial-opening conflicts in notes.

Status mapping:
* BPJT `Operasi` with at least 95% operational -> operating.
* BPJT `Operasi` with a material unopened length -> under_construction.
* BPJT `Operasi Sebagian` -> under_construction.

Run: python scripts/imports/add_bpjt_psn_roads.py
Then rebuild: validate.py, build_projects.py, build_site_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
from datetime import date

from data_model import (
    CURATED,
    EXTERNAL_FIELDS,
    ORG_FIELDS,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    ROOT,
    is_blank,
    read_csv,
    write_csv,
)

BPJT_PATH = ROOT / "data" / "raw" / "2026-11-06" / "bpjt_toll_road_list.json"
SOURCE_ID = "src-bpjt-toll-road-list-2026-11-06"
LAST_VERIFIED = "2026-11-08"
STATUS_AS_OF = "2026-11-06"

# Fields BPJT does not carry: id, province, island, route, corridor and the
# operator organisation. Everything numeric comes from the snapshot.
META = {
    "Simpang Indralaya - Muara Enim": {
        "id": "tol-simpang-indralaya-muara-enim",
        "name": "Simpang Indralaya–Muara Enim Toll Road",
        "province": "South Sumatra",
        "island": "Sumatra",
        "route": "Indralaya–Muara Enim, South Sumatra",
        "corridor_id": "trans-sumatera",
        "org_id": "org-hutama-karya",
    },
    "Serpong - Balaraja": {
        "id": "tol-serpong-balaraja",
        "name": "Serpong–Balaraja Toll Road",
        "province": "Banten",
        "island": "Java",
        "route": "Serpong–Balaraja, Banten",
        "corridor_id": "",
        "org_id": "org-trans-bumi-serbaraja",
    },
    "Cileunyi - Sumedang - Dawuan": {
        "id": "tol-cileunyi-sumedang-dawuan",
        "name": "Cileunyi–Sumedang–Dawuan Toll Road",
        "province": "West Java",
        "island": "Java",
        "route": "Cileunyi–Sumedang–Dawuan, West Java",
        "corridor_id": "",
        "org_id": "org-citra-karya-jabar-tol",
    },
    "Cibitung - Cilincing": {
        "id": "tol-cibitung-cilincing",
        "name": "Cibitung–Cilincing Toll Road",
        "province": "West Java; DKI Jakarta",
        "island": "Java",
        "route": "Cibitung–Cilincing, Bekasi–Jakarta",
        "corridor_id": "",
        "org_id": "org-cibitung-tanjung-priok-port-tollways",
    },
    "Cengkareng - Batu Ceper - Kunciran": {
        "id": "tol-cengkareng-batu-ceper-kunciran",
        "name": "Cengkareng–Batu Ceper–Kunciran Toll Road",
        "province": "DKI Jakarta; Banten",
        "island": "Java",
        "route": "Cengkareng–Kunciran, Jakarta–Tangerang",
        "corridor_id": "",
        "org_id": "org-jasamarga-kunciran-cengkareng",
    },
    "Pekanbaru - Kandis - Dumai": {
        "id": "tol-pekanbaru-kandis-dumai",
        "name": "Pekanbaru–Kandis–Dumai Toll Road",
        "province": "Riau",
        "island": "Sumatra",
        "route": "Pekanbaru–Dumai, Riau",
        "corridor_id": "trans-sumatera",
        "org_id": "org-hutama-karya",
    },
    "Manado - Bitung": {
        "id": "tol-manado-bitung",
        "name": "Manado–Bitung Toll Road",
        "province": "North Sulawesi",
        "island": "Sulawesi",
        "route": "Manado–Bitung, North Sulawesi",
        "corridor_id": "",
        "org_id": "org-jasamarga-manado-bitung",
    },
    "Balikpapan - Samarinda": {
        "id": "tol-balikpapan-samarinda",
        "name": "Balikpapan–Samarinda Toll Road",
        "province": "East Kalimantan",
        "island": "Kalimantan",
        "route": "Balikpapan–Samarinda, East Kalimantan",
        "corridor_id": "",
        "org_id": "org-jasamarga-balikpapan-samarinda",
    },
    "Kunciran - Serpong": {
        "id": "tol-kunciran-serpong",
        "name": "Kunciran–Serpong Toll Road",
        "province": "Banten",
        "island": "Java",
        "route": "Kunciran–Serpong, Banten",
        "corridor_id": "",
        "org_id": "org-marga-trans-nusantara",
    },
    "Pasuruan - Probolinggo": {
        "id": "tol-pasuruan-probolinggo",
        "name": "Pasuruan–Probolinggo Toll Road",
        "province": "East Java",
        "island": "Java",
        "route": "Pasuruan–Probolinggo, East Java",
        "corridor_id": "",
        "org_id": "org-trans-jawa-paspro-jalan-tol",
    },
    "Pandaan - Malang": {
        "id": "tol-pandaan-malang",
        "name": "Pandaan–Malang Toll Road",
        "province": "East Java",
        "island": "Java",
        "route": "Pandaan–Malang, East Java",
        "corridor_id": "",
        "org_id": "org-jasamarga-pandaan-malang",
    },
    "Ngawi - Kertosono - Kediri": {
        "id": "tol-ngawi-kertosono-kediri",
        "name": "Ngawi–Kertosono–Kediri Toll Road",
        "province": "East Java",
        "island": "Java",
        "route": "Ngawi–Kertosono–Kediri, East Java",
        "corridor_id": "",
        "org_id": "org-jasamarga-ngawi-kertosono-kediri",
        # BPJT returns UTM coordinates for this row, so use the corridor midpoint.
        "lat": "-7.55000",
        "lon": "111.65000",
    },
    "Medan - Binjai": {
        "id": "tol-medan-binjai",
        "name": "Medan–Binjai Toll Road",
        "province": "North Sumatra",
        "island": "Sumatra",
        "route": "Medan–Binjai, North Sumatra",
        "corridor_id": "trans-sumatera",
        "org_id": "org-medan-binjai-tol",
    },
    "Akses Tanjung Priok": {
        "id": "tol-akses-tanjung-priok",
        "name": "Akses Tanjung Priok Toll Road",
        "province": "DKI Jakarta",
        "island": "Java",
        "route": "Tanjung Priok access, Jakarta",
        "corridor_id": "",
        "org_id": "org-hutama-karya",
    },
    "Cinere - Jagorawi": {
        "id": "tol-cinere-jagorawi",
        "name": "Cinere–Jagorawi Toll Road",
        "province": "West Java; DKI Jakarta",
        "island": "Java",
        "route": "Cinere–Jagorawi, Depok–Jakarta",
        "corridor_id": "",
        "org_id": "org-translingkar-kita-jaya",
    },
}

NEW_ORGS = {
    "org-trans-bumi-serbaraja": ("PT Trans Bumi Serbaraja", "private"),
    "org-citra-karya-jabar-tol": ("PT Citra Karya Jabar Tol", "private"),
    "org-cibitung-tanjung-priok-port-tollways": ("PT Cibitung Tanjung Priok Port Tollways", "private"),
    "org-jasamarga-kunciran-cengkareng": ("PT Jasamarga Kunciran Cengkareng", "private"),
    "org-jasamarga-manado-bitung": ("PT Jasamarga Manado Bitung", "private"),
    "org-jasamarga-balikpapan-samarinda": ("PT Jasamarga Balikpapan Samarinda", "private"),
    "org-marga-trans-nusantara": ("PT Marga Trans Nusantara", "private"),
    "org-trans-jawa-paspro-jalan-tol": ("PT Trans Jawa Paspro Jalan Tol", "private"),
    "org-jasamarga-pandaan-malang": ("PT Jasamarga Pandaan Malang", "private"),
    "org-jasamarga-ngawi-kertosono-kediri": ("PT Jasamarga Ngawi Kertosono Kediri", "private"),
    "org-medan-binjai-tol": ("PT Medan Binjai Tol", "private"),
    "org-translingkar-kita-jaya": ("PT Translingkar Kita Jaya", "private"),
}


def year_of(value: str) -> str:
    return value[:4] if value and value[:4].isdigit() else ""


def main() -> None:
    bpjt = json.loads(BPJT_PATH.read_text(encoding="utf-8-sig"))["data"]
    projects = read_csv(CURATED / "projects.csv")
    organizations = read_csv(CURATED / "organizations.csv")
    links = read_csv(CURATED / "project_organizations.csv")
    claims = read_csv(CURATED / "project_sources.csv")
    external = read_csv(CURATED / "project_external_ids.csv")
    sources = {row["id"] for row in read_csv(CURATED / "sources.csv")}
    if SOURCE_ID not in sources:
        raise SystemExit(f"missing source {SOURCE_ID}")

    for org_id, (name, org_type) in NEW_ORGS.items():
        if not any(row["id"] == org_id for row in organizations):
            organizations.append(
                {
                    "id": org_id,
                    "name": name,
                    "short_name": "",
                    "org_type": org_type,
                    "country_code": "ID",
                    "parent_id": "",
                    "website": "",
                    "notes": "Toll-road concession operator from the BPJT list.",
                }
            )

    added = 0
    for record in bpjt:
        if record["psn_status"] != "PSN" or record["ruas_name"] not in META:
            continue
        meta = META[record["ruas_name"]]
        length = float(record["length"])
        operational = float(record["panjang_operasi_km"]) if record["panjang_operasi_km"] else 0.0
        share = operational / length if length else 0
        if record["status_ruas"] == "Operasi Sebagian":
            status = "under_construction"
        elif record["status_ruas"] == "Operasi" and share >= 0.95:
            status = "operating"
        else:
            status = "under_construction"

        opened_year = year_of(record.get("sk_operasi", "")) if status == "operating" else ""
        basis = (
            f"BPJT toll-road list (6 Nov 2026): {record['status_ruas']}, "
            f"{operational:g} of {length:g} km operational"
            + (f"; operation decree {year_of(record.get('sk_operasi', ''))}" if opened_year else "")
            + "."
        )
        note_bits = [
            "Coordinates are the midpoint of the BPJT start and end points, approximate.",
        ]
        if record["status_ruas"] == "Operasi Sebagian":
            note_bits.append(
                "BPJT labels the corridor Operasi Sebagian; the recorded operational length "
                "does not mean the whole corridor is open."
            )
        if status == "under_construction" and record["status_ruas"] == "Operasi":
            note_bits.append(
                "BPJT labels the corridor Operasi, but only part of the recorded length is "
                "open; the remainder is not recorded as operational."
            )
        if 0 < share < 0.95 and status == "operating":
            note_bits.append(
                f"The BPJT operational figure is {share * 100:.1f}% of the recorded length."
            )

        project = {
            "id": meta["id"],
            "name": meta["name"],
            "sector": "road",
            "subsector": "toll",
            "status": status,
            "status_basis": basis,
            "corridor_id": meta["corridor_id"],
            "island": meta["island"],
            "province": meta["province"],
            "route": meta["route"],
            "length_km": f"{length:g}",
            "operational_km": f"{operational:g}" if operational else "",
            "construction_km": "",
            "progress_pct": "",
            "investment_idr_t": "",
            "capacity": "",
            "capacity_unit": "",
            "psn": "yes",
            "opened_year": opened_year,
            "opened_date": "",
            "expected_open_year": "",
            "status_as_of": STATUS_AS_OF,
            "verification": "official",
            "lat": meta.get(
                "lat",
                f"{(float(record['start_latitude']) + float(record['end_latitude'])) / 2:.5f}",
            ),
            "lon": meta.get(
                "lon",
                f"{(float(record['start_longitude']) + float(record['end_longitude'])) / 2:.5f}",
            ),
            "precision": "approximate",
            "last_verified": LAST_VERIFIED,
            "notes": " ".join(note_bits),
        }

        existing = next((row for row in projects if row["id"] == meta["id"]), None)
        if existing:
            existing.update(project)
        else:
            projects.append(project)
            added += 1

        external = [row for row in external if row["project_id"] != meta["id"]]
        external.append(
            {
                "project_id": meta["id"],
                "system": "bpjt-ruas",
                "external_id": record["ruas_name"],
                "url": "",
                "notes": "BPJT toll-road list key.",
            }
        )

        claims = [row for row in claims if row["project_id"] != meta["id"]]
        for kind, value in (
            ("status", status),
            ("length", f"{length:g} km"),
            ("operational", f"{operational:g} km"),
            ("operator", record["bujt_name"]),
            ("location", f"{meta['province']} — {meta['route']}"),
        ):
            claims.append(
                {
                    "project_id": meta["id"],
                    "source_id": SOURCE_ID,
                    "claim": kind,
                    "claim_value": value,
                    "claim_date": STATUS_AS_OF,
                    "notes": "BPJT toll-road list.",
                }
            )

        links = [
            row for row in links
            if not (row["project_id"] == meta["id"] and row["role"] in {"operator", "owner"})
        ]
        links.append(
            {
                "project_id": meta["id"],
                "org_id": meta["org_id"],
                "role": "operator",
                "share_pct": "",
                "start_year": "",
                "end_year": "",
                "source_id": SOURCE_ID,
                "notes": "",
            }
        )

    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, organizations)
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, links)
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)
    write_csv(CURATED / "project_external_ids.csv", EXTERNAL_FIELDS, external)

    print(
        f"added {added} PSN toll corridors; "
        f"{len(projects)} projects, {len(organizations)} organisations, "
        f"{len(claims)} claims, {len(links)} links"
    )


if __name__ == "__main__":
    main()
