"""Add named IKN Stage II packages and projects.

Sources:

* OIKN Stage II evaluation, 14 July 2026, reported by Top Konstruksi on
  21 July 2026. The IKN Authority page returned HTTP 403 to this client; the
  report reproduces the package counts and the named projects.
* OIKN seven-project investment signing, 14 October 2026, reported by
  JournalArta on 8 November 2026.
* Ministry of Public Works Nataru statement, 9 December 2025, for the 50.227 km
  functional IKN toll-road length.

The rows are project/package level. They do not invent a budget, length or
boundary where the source is silent. All coordinates use the KIPP point already
used by ``urban-ikn-phase-2`` and are marked approximate.

The script is idempotent: existing ids are never replaced.

Run: python scripts/imports/add_ikn_packages.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_i18n.py
      python scripts/build_all.py
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (  # noqa: E402
    CURATED,
    EVENT_FIELDS,
    ORG_FIELDS,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    SOURCE_FIELDS,
    TRANSLATION_FIELDS,
    read_csv,
    write_csv,
)

RAW = Path(__file__).resolve().parents[2] / "data" / "raw" / "2026-11-09"
REVIEWED = "2026-11-09"

SOURCE_TOP = "src-topkonstruksi-ikn-stage-ii-2026-07-21"
SOURCE_SEVEN = "src-journalarta-ikn-seven-projects-2026-11-08"
SOURCE_PU = "src-kemenpu-nataru-2025-12-09"

NEW_SOURCES = [
    {
        "id": SOURCE_TOP,
        "publisher": "Top Konstruksi",
        "title": "Otorita IKN Percepat Pembangunan Tahap II, Wujudkan IKN Sebagai Ibu Kota Politik pada Tahun 2028",
        "url": "https://topkonstruksi.com/otorita-ikn-percepat-pembangunan-tahap-ii-wujudkan-ikn-sebagai-ibu-kota-politik-pada-tahun-2028",
        "published_on": "2026-07-21",
        "retrieved_on": REVIEWED,
        "source_type": "secondary",
        "language": "id",
        "archive_path": "data/raw/2026-11-09/topkonstruksi_ikn_stage_ii_2026.html",
        "notes": (
            "Reproduces the OIKN Stage II evaluation of 14 July 2026: 40 OIKN "
            "APBN packages (9 complete, 15 under construction, 16 in tender), "
            "90 Public Works packages (78 complete, 12 under construction), "
            "12 housing packages (11 complete, 1 under construction), 67 private "
            "agreements and 13 KPBU initiatives. The IKN Authority page returned "
            "HTTP 403 to the local client."
        ),
    },
    {
        "id": SOURCE_SEVEN,
        "publisher": "JournalArta",
        "title": "Investasi IKN Rp3,739 Triliun: Tujuh Proyek Baru",
        "url": "https://journalarta.com/news/2026/11/08/investasi-ikn-tujuh-proyek-rp3739-triliun/",
        "published_on": "2026-11-08",
        "retrieved_on": REVIEWED,
        "source_type": "secondary",
        "language": "id",
        "archive_path": "data/raw/2026-11-09/journalarta_ikn_seven_projects_2026.html",
        "notes": (
            "Seven projects signed on 14 October 2026 worth Rp3.739T: eight ASN "
            "apartment towers at Rp2.629T and five private investments at "
            "Rp1.11T, including Grand Vista Nusantara (3.57 ha, Rp1T)."
        ),
    },
    {
        "id": SOURCE_PU,
        "publisher": "Kementerian Pekerjaan Umum",
        "title": "Kementerian PU Pastikan Jaringan Jalan Nasional dan Tol Siap Layani Arus Nataru 2025/2026",
        "url": "https://sahabat.pu.go.id/eppid/berita/detail/kementerian-pu-pastikan-jaringan-jalan-nasional-dan-tol-siap-layani-arus-nataru-20252026",
        "published_on": "2025-12-09",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "archive_path": "data/raw/2026-11-09/kemenpu_nataru_2025.html",
        "notes": (
            "States that IKN toll sections 3A, 3A2, 3B, 3B2, 5A, 5B, 6A and the "
            "Pulau Balang bridge, 50.227 km, would be functional for Nataru "
            "2025/2026."
        ),
    },
]

NEW_ORGS = [
    ("org-kementerian-pkp", "Kementerian Perumahan dan Kawasan Permukiman", "Kementerian PKP", "government", "Ministry responsible for the IKN housing packages."),
    ("org-nindya-karya", "PT Nindya Karya (Persero)", "Nindya Karya", "soe", "Sponsor of the eight ASN apartment towers signed in October 2026."),
    ("org-intiland", "PT Intiland Development Tbk", "Intiland", "private", "Sponsor of 108 landed ASN houses signed in October 2026."),
    ("org-gunadarma", "Universitas Gunadarma", "Gunadarma", "private", "Developer of the Nusantara campus under construction."),
    ("org-abdi-waluyo", "Rumah Sakit Abdi Waluyo", "Abdi Waluyo", "private", "Developer of the IKN hospital under construction."),
    ("org-plataran", "PT Plataran Indonesia", "Plataran", "private", "Developer of Teras by Plataran."),
    ("org-star-bright", "PT Star Bright International Investment", "Star Bright", "private", "Developer of the IKN apartment project under construction."),
    ("org-fajar-maju", "PT Fajar Maju Karya Gemilang", "Fajar Maju", "private", "Developer of the IKN mixed-use area under construction."),
    ("org-dian-jaya", "PT Dian Jaya Indonesia", "Dian Jaya", "private", "Developer of the IKN apartment project under construction."),
    ("org-indonesia-belt-road", "PT Indonesia Belt Road High Tech Development Park", "Indonesia Belt Road", "private", "Developer of Grand Vista Nusantara, signed in October 2026."),
]

KIPP = {"lat": "-0.974", "lon": "116.708"}
ROUTE = "KIPP Nusantara, Penajam Paser Utara"


def project(
    project_id: str,
    name: str,
    sector: str,
    subsector: str,
    status: str,
    basis: str,
    *,
    status_as_of: str = "2026-07-15",
    verification: str = "single",
    length: str = "",
    operational: str = "",
    progress: str = "",
    investment: str = "",
    capacity: str = "",
    capacity_unit: str = "",
    opened_year: str = "",
    opened_date: str = "",
    notes: str,
) -> dict[str, str]:
    return {
        "id": project_id,
        "name": name,
        "sector": sector,
        "subsector": subsector,
        "status": status,
        "status_basis": basis,
        "corridor_id": "",
        "island": "Kalimantan",
        "province": "East Kalimantan",
        "route": ROUTE,
        "length_km": length,
        "operational_km": operational,
        "construction_km": "",
        "progress_pct": progress,
        "investment_idr_t": investment,
        "capacity": capacity,
        "capacity_unit": capacity_unit,
        "psn": "no",
        "opened_year": opened_year,
        "opened_date": opened_date,
        "expected_open_year": "",
        "status_as_of": status_as_of,
        "verification": verification,
        "lat": KIPP["lat"],
        "lon": KIPP["lon"],
        "precision": "approximate",
        "last_verified": REVIEWED,
        "notes": notes,
    }


NEW_PROJECTS = [
    project(
        "urban-ikn-government-offices", "IKN Government Office Buildings", "urban",
        "government offices", "under_construction",
        "The OIKN Stage II evaluation lists government office buildings among the 15 APBN packages under construction as of 14 July 2026.",
        notes="One of 40 physical packages managed by OIKN under APBN. The source states no cost or floor area.",
    ),
    project(
        "urban-ikn-legislative-complex", "IKN Legislative Complex", "urban",
        "legislative complex", "under_construction",
        "The OIKN Stage II evaluation lists the legislative complex among the packages under construction as of 14 July 2026.",
        notes="Construction of the legislative complex. The separate 2026-2027 access-road package is recorded as its own row.",
    ),
    project(
        "urban-ikn-judicial-complex", "IKN Judicial Complex", "urban",
        "judicial complex", "under_construction",
        "The OIKN Stage II evaluation lists the judicial complex among the packages under construction as of 14 July 2026.",
        notes="Construction of the judicial complex. Hutama Karya reported the judicial access road at 22.20% in June 2026; the complex itself is a separate package.",
    ),
    project(
        "urban-ikn-road-network", "IKN Internal Road Network", "urban",
        "road network", "under_construction",
        "The OIKN Stage II evaluation lists road-network packages among the 15 APBN packages under construction as of 14 July 2026.",
        notes="OIKN-managed internal roads. Ministry of Public Works road packages are recorded separately.",
    ),
    project(
        "urban-ikn-retention-ponds", "IKN Embankments and Retention Ponds", "water",
        "urban drainage", "under_construction",
        "The OIKN Stage II evaluation lists embankments and retention ponds among the packages under construction as of 14 July 2026.",
        notes="Part of the IKN urban water-management system. The source states no storage volume.",
    ),
    project(
        "urban-ikn-water-piping", "IKN Drinking-Water Piping Network", "water",
        "water supply", "under_construction",
        "The OIKN Stage II evaluation lists drinking-water piping among the packages under construction as of 14 July 2026.",
        notes="Part of the IKN basic urban-service system. The source states no network length or capacity.",
    ),
    project(
        "road-ikn-toll", "IKN Toll Road", "road", "toll road", "under_construction",
        "The Ministry of Public Works lists the IKN toll road among 12 packages still under construction in July 2026; 50.227 km of sections were functional for Nataru 2025/2026.",
        verification="dual", length="50.227",
        notes="50.227 km is the combined functional length of sections 3A, 3A2, 3B, 3B2, 5A, 5B, 6A and the Pulau Balang bridge, not the full design length. Functional opening is not full operation.",
    ),
    project(
        "urban-pulau-balang-bridge-duplication", "Pulau Balang Short-Span Bridge Duplication", "urban",
        "bridge", "under_construction",
        "The Ministry of Public Works lists the Pulau Balang short-span bridge duplication among the 12 IKN packages still under construction in July 2026.",
        notes="A second short-span bridge beside the existing Pulau Balang bridge. The source gives no length or cost.",
    ),
    project(
        "urban-ikn-supporting-roads", "IKN Supporting Road Packages", "urban",
        "road package", "under_construction",
        "The Ministry of Public Works lists supporting road packages among the 12 IKN packages still under construction in July 2026.",
        notes="Public Works road packages supporting the KIPP and airport access. Individual package lengths are not stated.",
    ),
    project(
        "road-kipp-1b-1c-upgrade", "KIPP 1B-1C Road Upgrade", "road", "urban road",
        "recently_completed",
        "Seven road-upgrade packages covering 12.9 km were 100% complete and handed over to OIKN on 17 September 2026.",
        status_as_of="2026-09-17", length="12.9", operational="12.9", progress="100",
        opened_year="2026", opened_date="2026-09-17",
        notes="Package lengths: A 1.3 km, B-C 3.7 km, D-E 4.4 km, F-G 3.5 km. The 12.9 km total is the sum of the published package lengths.",
    ),
    project(
        "urban-ikn-judicial-access", "IKN Judicial Complex Access Road", "urban",
        "road package", "planned",
        "A 2026-2027 road package for the judicial complex received PPS approval in September 2026; construction had not started in the source.",
        status_as_of="2026-09-17", verification="single",
        notes="One of three road packages totalling about Rp3.986T approved for 2026-2027. The source states no length.",
    ),
    project(
        "urban-ikn-legislative-access", "IKN Legislative Complex Access Road", "urban",
        "road package", "planned",
        "A 2026-2027 road package for the legislative complex received PPS approval in September 2026; construction had not started in the source.",
        status_as_of="2026-09-17", verification="single",
        notes="One of three road packages totalling about Rp3.986T approved for 2026-2027. The source states no length.",
    ),
    project(
        "urban-kipp-1a-access", "KIPP 1A Supporting-Area Road", "urban",
        "road package", "planned",
        "A 2026-2027 road package for the KIPP 1A supporting area received PPS approval in September 2026; construction had not started in the source.",
        status_as_of="2026-09-17", verification="single",
        notes="One of three road packages totalling about Rp3.986T approved for 2026-2027. The source states no length.",
    ),
    project(
        "housing-ikn-rusun-mbr", "IKN Relocated Low-Income Housing", "housing",
        "public housing", "under_construction",
        "The Ministry of Housing and Residential Areas lists the relocated low-income apartment block as the one package still under construction among its 12 IKN packages in July 2026.",
        notes="Part of the resettlement programme for residents affected by IKN land preparation. The source states no unit count or cost.",
    ),
    project(
        "housing-ikn-rusun-asn", "IKN Civil-Servant Apartment Towers", "housing",
        "civil-servant housing", "planned",
        "Eight apartment towers worth Rp2.629T were signed under the KPBU scheme on 14 October 2026 and were about to enter construction.",
        status_as_of="2026-10-14", investment="2.629",
        notes="KPBU housing package sponsored by PT Nindya Karya. The Rp2.629T covers eight towers and is part of the Rp3.739T seven-project package signed on 14 October 2026.",
    ),
    project(
        "housing-ikn-intiland-houses", "IKN Intiland Landed Civil-Servant Houses", "housing",
        "civil-servant housing", "planned",
        "PT Intiland Development signed a KPBU for 108 landed ASN houses on 14 October 2026; construction was about to start.",
        status_as_of="2026-10-14",
        notes="KPBU housing package. The source does not state the contract value separately.",
    ),
    project(
        "education-gunadarma-nusantara", "Gunadarma University Nusantara Campus", "education",
        "university campus", "under_construction",
        "The OIKN Stage II evaluation lists the Gunadarma Nusantara campus among six private projects under construction as of 14 July 2026.",
        notes="Private investment project under a cooperation agreement with OIKN.",
    ),
    project(
        "urban-abdi-waluyo-hospital", "Abdi Waluyo Hospital IKN", "urban",
        "hospital", "under_construction",
        "The OIKN Stage II evaluation lists Abdi Waluyo Hospital among six private projects under construction as of 14 July 2026.",
        notes="Private hospital project under a cooperation agreement with OIKN.",
    ),
    project(
        "urban-teras-by-plataran", "Teras by Plataran IKN", "urban",
        "hospitality", "under_construction",
        "The OIKN Stage II evaluation lists Teras by Plataran among six private projects under construction as of 14 July 2026.",
        notes="Private hospitality project under a cooperation agreement with OIKN.",
    ),
    project(
        "housing-star-bright-apartment", "Star Bright Apartments IKN", "housing",
        "apartment", "under_construction",
        "The OIKN Stage II evaluation lists the Star Bright apartment project among six private projects under construction as of 14 July 2026.",
        notes="Private apartment project under a cooperation agreement with OIKN.",
    ),
    project(
        "urban-fajar-maju-mixed-use", "Fajar Maju Karya Gemilang Mixed-Use Area", "urban",
        "mixed-use", "under_construction",
        "The OIKN Stage II evaluation lists the Fajar Maju Karya Gemilang mixed-use area among six private projects under construction as of 14 July 2026.",
        notes="Private mixed-use project under a cooperation agreement with OIKN.",
    ),
    project(
        "housing-dian-jaya-apartment", "Dian Jaya Apartments IKN", "housing",
        "apartment", "under_construction",
        "The OIKN Stage II evaluation lists the Dian Jaya apartment project among six private projects under construction as of 14 July 2026.",
        notes="Private apartment project under a cooperation agreement with OIKN.",
    ),
    project(
        "urban-grand-vista-nusantara", "Grand Vista Nusantara", "urban",
        "mixed-use", "planned",
        "A cooperation agreement for the 3.57 ha Grand Vista Nusantara mixed-use area was signed on 14 October 2026; construction had not started.",
        status_as_of="2026-10-14", investment="1.0", capacity="3.57", capacity_unit="ha",
        notes="Commercial area, apartments and offices in KIPP 1B. Developer: PT Indonesia Belt Road High Tech Development Park.",
    ),
]

ID_NAMES = {
    "urban-ikn-government-offices": "Gedung Perkantoran Pemerintahan IKN",
    "urban-ikn-legislative-complex": "Kawasan Legislatif IKN",
    "urban-ikn-judicial-complex": "Kawasan Yudikatif IKN",
    "urban-ikn-road-network": "Jaringan Jalan Internal IKN",
    "urban-ikn-retention-ponds": "Embung dan Kolam Retensi IKN",
    "urban-ikn-water-piping": "Jaringan Perpipaan Air Minum IKN",
    "road-ikn-toll": "Jalan Tol IKN",
    "urban-pulau-balang-bridge-duplication": "Duplikasi Jembatan Pulau Balang Bentang Pendek",
    "urban-ikn-supporting-roads": "Paket Jalan Pendukung IKN",
    "road-kipp-1b-1c-upgrade": "Peningkatan Jalan KIPP 1B-1C",
    "urban-ikn-judicial-access": "Jalan Akses Kompleks Yudikatif IKN",
    "urban-ikn-legislative-access": "Jalan Akses Kompleks Legislatif IKN",
    "urban-kipp-1a-access": "Jalan Kawasan Pendukung KIPP 1A",
    "housing-ikn-rusun-mbr": "Rusun MBR Relokasi IKN",
    "housing-ikn-rusun-asn": "Menara Rusun ASN IKN",
    "housing-ikn-intiland-houses": "Rumah Tapak ASN Intiland IKN",
    "education-gunadarma-nusantara": "Kampus Universitas Gunadarma Nusantara",
    "urban-abdi-waluyo-hospital": "Rumah Sakit Abdi Waluyo IKN",
    "urban-teras-by-plataran": "Teras by Plataran IKN",
    "housing-star-bright-apartment": "Apartemen Star Bright IKN",
    "urban-fajar-maju-mixed-use": "Kawasan Mixed-Use Fajar Maju Karya Gemilang",
    "housing-dian-jaya-apartment": "Apartemen Dian Jaya Indonesia",
    "urban-grand-vista-nusantara": "Grand Vista Nusantara",
}

OIKN_PROJECTS = {
    "urban-ikn-government-offices", "urban-ikn-legislative-complex",
    "urban-ikn-judicial-complex", "urban-ikn-road-network",
    "urban-ikn-retention-ponds", "urban-ikn-water-piping",
}
PU_PROJECTS = {
    "road-ikn-toll", "urban-pulau-balang-bridge-duplication",
    "urban-ikn-supporting-roads", "road-kipp-1b-1c-upgrade",
    "urban-ikn-judicial-access", "urban-ikn-legislative-access",
    "urban-kipp-1a-access",
}
PRIVATE_DEVELOPERS = {
    "education-gunadarma-nusantara": "org-gunadarma",
    "urban-abdi-waluyo-hospital": "org-abdi-waluyo",
    "urban-teras-by-plataran": "org-plataran",
    "housing-star-bright-apartment": "org-star-bright",
    "urban-fajar-maju-mixed-use": "org-fajar-maju",
    "housing-dian-jaya-apartment": "org-dian-jaya",
    "urban-grand-vista-nusantara": "org-indonesia-belt-road",
}

NEW_EVENTS = [
    {
        "id": "evt-kipp-1b-1c-handover",
        "project_id": "road-kipp-1b-1c-upgrade",
        "event_date": "2026-09-17",
        "event_type": "section_opened",
        "description": "Seven KIPP 1B-1C road-upgrade packages were handed over to OIKN after reaching 100%.",
        "source_id": SOURCE_TOP,
        "notes": "",
    },
    {
        "id": "evt-ikn-asn-pks",
        "project_id": "housing-ikn-rusun-asn",
        "event_date": "2026-10-14",
        "event_type": "contract",
        "description": "Eight ASN apartment towers worth Rp2.629T were signed under the KPBU scheme.",
        "source_id": SOURCE_SEVEN,
        "notes": "",
    },
    {
        "id": "evt-ikn-intiland-pks",
        "project_id": "housing-ikn-intiland-houses",
        "event_date": "2026-10-14",
        "event_type": "contract",
        "description": "PT Intiland Development signed a KPBU for 108 landed ASN houses.",
        "source_id": SOURCE_SEVEN,
        "notes": "",
    },
    {
        "id": "evt-grand-vista-pks",
        "project_id": "urban-grand-vista-nusantara",
        "event_date": "2026-10-14",
        "event_type": "contract",
        "description": "Grand Vista Nusantara signed a cooperation agreement for a 3.57 ha mixed-use area worth Rp1T.",
        "source_id": SOURCE_SEVEN,
        "notes": "",
    },
]


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    sources = read_csv(CURATED / "sources.csv")
    existing_sources = {row["id"] for row in sources}
    for row in NEW_SOURCES:
        if row["id"] in existing_sources:
            continue
        row = dict(row)
        row["snapshot_hash"] = hash_file(RAW / Path(row["archive_path"]).name)
        row["accessed_via"] = row["url"].split("/")[2]
        row["licence"] = ""
        sources.append(row)
    sources.sort(key=lambda row: row["id"])
    write_csv(CURATED / "sources.csv", SOURCE_FIELDS, sources)

    orgs = read_csv(CURATED / "organizations.csv")
    existing_orgs = {row["id"] for row in orgs}
    for org_id, name, short, org_type, notes in NEW_ORGS:
        if org_id in existing_orgs:
            continue
        orgs.append(
            {
                "id": org_id,
                "name": name,
                "short_name": short,
                "org_type": org_type,
                "country_code": "ID",
                "parent_id": "",
                "website": "",
                "notes": notes,
            }
        )
    orgs.sort(key=lambda row: row["id"])
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, orgs)

    projects = read_csv(CURATED / "projects.csv")
    existing_projects = {row["id"] for row in projects}
    for row in NEW_PROJECTS:
        if row["id"] not in existing_projects:
            projects.append(row)
    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)

    claims = read_csv(CURATED / "project_sources.csv")
    claim_keys = {
        (row["project_id"], row["source_id"], row["claim"]) for row in claims
    }

    def add_claim(project_id: str, source_id: str, claim: str, value: str, date: str, notes: str = "") -> None:
        key = (project_id, source_id, claim)
        if key in claim_keys:
            return
        claims.append(
            {
                "project_id": project_id,
                "source_id": source_id,
                "claim": claim,
                "claim_value": value,
                "claim_date": date,
                "notes": notes,
            }
        )
        claim_keys.add(key)

    for row in NEW_PROJECTS:
        project_id = row["id"]
        source = SOURCE_SEVEN if row["status_as_of"] in {"2026-10-14"} else SOURCE_TOP
        if project_id == "road-kipp-1b-1c-upgrade":
            source = SOURCE_TOP
        add_claim(project_id, source, "status", "", row["status_as_of"])
        add_claim(project_id, source, "location", ROUTE, row["status_as_of"])
        if row["length_km"]:
            add_claim(project_id, SOURCE_PU if project_id == "road-ikn-toll" else SOURCE_TOP,
                      "length", row["length_km"] + " km", row["status_as_of"])
        if row["operational_km"]:
            add_claim(project_id, SOURCE_TOP, "operational", row["operational_km"] + " km", row["status_as_of"])
        if row["progress_pct"]:
            add_claim(project_id, SOURCE_TOP, "progress", row["progress_pct"] + "%", row["status_as_of"])
        if row["investment_idr_t"]:
            add_claim(project_id, SOURCE_SEVEN, "investment", "Rp " + row["investment_idr_t"] + "T", row["status_as_of"])
        if row["capacity"]:
            add_claim(project_id, SOURCE_SEVEN, "capacity", row["capacity"] + " " + row["capacity_unit"], row["status_as_of"])
        if row["opened_year"]:
            add_claim(project_id, SOURCE_TOP, "opening", row["opened_date"], row["status_as_of"])
        if project_id == "road-ikn-toll":
            add_claim(project_id, SOURCE_PU, "length", "50.227 km", "2025-12-09")
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)

    links = read_csv(CURATED / "project_organizations.csv")
    link_keys = {(row["project_id"], row["org_id"], row["role"]) for row in links}

    def add_link(project_id: str, org_id: str, role: str, source_id: str, notes: str = "") -> None:
        key = (project_id, org_id, role)
        if key in link_keys:
            return
        links.append(
            {
                "project_id": project_id,
                "org_id": org_id,
                "role": role,
                "share_pct": "",
                "start_year": "",
                "end_year": "",
                "source_id": source_id,
                "notes": notes,
            }
        )
        link_keys.add(key)

    for row in NEW_PROJECTS:
        project_id = row["id"]
        if project_id in OIKN_PROJECTS:
            add_link(project_id, "org-otorita-ikn", "sponsor", SOURCE_TOP)
        if project_id in PU_PROJECTS:
            add_link(project_id, "org-kementerian-pu", "sponsor", SOURCE_TOP)
        if project_id == "housing-ikn-rusun-mbr":
            add_link(project_id, "org-kementerian-pkp", "owner", SOURCE_TOP)
        if project_id == "housing-ikn-rusun-asn":
            add_link(project_id, "org-kementerian-pkp", "owner", SOURCE_SEVEN)
            add_link(project_id, "org-nindya-karya", "contractor", SOURCE_SEVEN)
        if project_id == "housing-ikn-intiland-houses":
            add_link(project_id, "org-intiland", "developer", SOURCE_SEVEN)
        if project_id in PRIVATE_DEVELOPERS:
            add_link(project_id, PRIVATE_DEVELOPERS[project_id], "developer", SOURCE_TOP)
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, links)

    events = read_csv(CURATED / "project_events.csv")
    existing_events = {row["id"] for row in events}
    for row in NEW_EVENTS:
        if row["id"] not in existing_events:
            events.append(row)
    events.sort(key=lambda row: (row["event_date"], row["id"]))
    write_csv(CURATED / "project_events.csv", EVENT_FIELDS, events)

    translations = read_csv(CURATED / "translations.csv")
    translation_keys = {
        (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        for row in translations
    }
    for row in NEW_PROJECTS:
        key = ("project", row["id"], "name", "id")
        if key in translation_keys:
            continue
        translations.append(
            {
                "entity_type": "project",
                "entity_id": row["id"],
                "field": "name",
                "locale": "id",
                "text": ID_NAMES[row["id"]],
                "status": "reviewed",
                "translator": "atlas-editor",
                "reviewed_on": REVIEWED,
                "source_id": "",
            }
        )
        translation_keys.add(key)
    translations.sort(key=lambda row: (row["entity_type"], row["entity_id"], row["field"], row["locale"]))
    write_csv(CURATED / "translations.csv", TRANSLATION_FIELDS, translations)

    print(
        f"OK: {len(NEW_PROJECTS)} IKN rows, {len(NEW_ORGS)} organisations, "
        f"{len(NEW_SOURCES)} sources, {len(NEW_EVENTS)} events"
    )


if __name__ == "__main__":
    main()
