"""Add the remaining active PSN records as register-only rows.

Permenko 16/2025 names 226 active projects and 24 active programmes. The atlas
already had full or partial records for the transport set, several dams, a few
energy projects and 26 industrial areas. This importer adds the remaining 88
projects and 18 industrial areas at the only level the annex supports:

* official Indonesian name, PSN number, sector and location;
* an atlas English working name;
* a province centroid, clearly marked ``precision=province``;
* ``status=unknown`` and ``verification=unverified``.

It does not invent cost, capacity, status, developer, area or geometry. Every
new row has a ``psn`` claim, a ``location`` claim and a ``status`` claim that
says only "active in register". The ledger treats these as
``matched_register_project`` / ``matched_register_estate`` so coverage is
complete without pretending the record is complete.

The importer is idempotent: it removes and rewrites the claims, aliases and
rows it manages.

Run: python scripts/imports/add_psn_register_records.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_psn_ledger.py
      python scripts/build_all.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))

from build_psn_ledger import ESTATE_MATCH, PROJECT_MATCH, TRANSPORT_MATCH
from data_model import (
    ALIAS_FIELDS,
    CURATED,
    DERIVED,
    ESTATE_FIELDS,
    ESTATE_SOURCE_FIELDS,
    PROJECT_FIELDS,
    PROJECT_SOURCE_FIELDS,
    island_for,
    read_csv,
    write_csv,
)

RETRIEVED = "2026-11-09"
LAST_VERIFIED = "2026-11-09"
REGISTER_DATE = "2025-09-24"
REGISTER_SOURCE = "src-permenko-16-2025"

SECTOR_BY_REGISTER = {
    "housing": "housing",
    "dams_and_irrigation": "water",
    "water_and_sanitation": "water",
    "energy": "energy",
    "technology": "technology",
    "education": "education",
    "tourism": "tourism",
    "agriculture": "agriculture",
}

# English working names. The Indonesian name stays in the register, the row
# alias and the notes. These are translations, not official English titles.
PROJECT_NAMES = {
    131: "Rumah Susun Public Housing Construction",
    132: "Self-Help Housing Assistance Programme",
    133: "Marangkayu Dam",
    134: "Kuningan Dam",
    135: "Bendo Dam",
    136: "Gongseng Dam",
    137: "Tukul Dam",
    138: "Pidekso Dam",
    139: "Tugu Dam",
    140: "Karalloe Dam",
    142: "Tapin Dam",
    143: "Passeloreng Dam",
    144: "Lolak Dam",
    145: "Bintang Bano Dam",
    146: "Karian Dam",
    148: "Way Sekampung Dam",
    149: "Kuwil Kawangkoan Dam",
    150: "Ladongi Dam",
    151: "Ciawi Dam",
    152: "Sukamahi Dam",
    153: "Leuwikeris Dam",
    154: "Cipanas Dam",
    155: "Tiga Dihaji Dam",
    156: "Semantok Dam",
    157: "Pamukkulu Dam",
    158: "Bener Dam",
    159: "Sadawarna Dam",
    160: "Lausimeme Dam",
    162: "Marga Tiga Dam",
    163: "Bagong Dam",
    164: "Randugunting Dam",
    165: "Mbay Dam",
    166: "Bulango Ulu Dam",
    167: "Napun Gete Dam",
    168: "Temef Dam",
    169: "Way Apu Dam",
    171: "Tamblang Dam",
    172: "Beringin Sila Dam",
    173: "Tiu Suntuk Dam",
    174: "Manikin Dam",
    176: "Jragung Dam",
    177: "Sepaku Semoi Dam",
    178: "Budong-Budong Dam",
    179: "Ameroro Dam",
    180: "Karangnongko Dam",
    181: "Lhok Guci Irrigation Network",
    182: "Jambo Aye Kanan Irrigation Network",
    183: "Lematang Irrigation Network",
    184: "Baliase Irrigation Dam and Network",
    185: "Gumbasa Irrigation Network Rehabilitation",
    186: "Rentang Irrigation Network Rehabilitation",
    187: "Glapan Irrigation Network Rehabilitation",
    188: "Komering Irrigation Network Development and Management",
    189: "Bintan Bay Estuary Dam and Drinking Water Supply System",
    190: "Semarang West Drinking Water Supply System (SPAM)",
    191: "Umbulan Drinking Water Supply System (SPAM)",
    192: "Bandar Lampung Drinking Water Supply System (SPAM)",
    193: "Jatiluhur Regional Drinking Water Supply System (SPAM)",
    194: "Wosusokas Regional Drinking Water Supply System (SPAM)",
    195: "Karian-Serpong Regional Drinking Water Supply System (SPAM)",
    196: "Benteng-Kobema Regional Drinking Water Supply System (SPAM)",
    197: "Karian Raw Water Infrastructure",
    198: "Jakarta Sewerage System (JSS)",
    201: "Gendalo, Gandang, Gehem and Bangka Field Development (IDD)",
    202: "Tangguh LNG Train 3",
    203: "Jambaran-Tiung Biru Gas Field Unitisation",
    204: "Ubadari Field Development, CCUS and Compression (UCC), Teluk Bintuni",
    205: "Asap, Kido and Merah Gas Field Development (AKM)",
    206: "Tuban Oil Refinery Expansion",
    208: "Balongan Refinery Upgrade (RDMP) and Petrochemical Industry",
    209: "Fuel Storage Tank Construction",
    210: "LPG Storage Tank Construction",
    211: "City Gas Network Construction",
    212: "Cirebon-Semarang and Sei Mangkei-Dumai Gas Transmission Pipeline",
    213: "Green Fuel Development (Cilacap, Plaju and Pupuk Kujang)",
    214: "Methanol- and Ethanol-Based Biofuel Development, Bojonegoro",
    216: "Coal Gasification, Kutai Timur",
    217: "North Hub Development Project, Makassar Strait",
    218: "Accelerated Technopark Development",
    219: "Multifunction Satellite Project",
    220: "Male Combat Drone Development",
    221: "IVO and Palm Petrol Production Technology with Merah Putih Catalyst",
    222: "Salt Industry Development",
    223: "Palapa Ring Integration",
    224: "Indonesia International Islamic University Campus",
    225: "Thousand Islands Tourism Project, Kepulauan Seribu",
    227: "Coconut Development and Downstream Industry",
    228: "Tidal and Lebak Swamp Mineral Soil Rice Field Development",
}

SUBSECTOR = {
    "housing": "housing",
    "water": "water_supply",
    "technology": "technology",
    "education": "education",
    "tourism": "tourism",
    "agriculture": "agriculture",
}

PROVINCE_EN = {
    "Aceh": "Aceh",
    "Sumatera Utara": "North Sumatra",
    "Sumatera Barat": "West Sumatra",
    "Riau": "Riau",
    "Kepulauan Riau": "Riau Islands",
    "Jambi": "Jambi",
    "Bengkulu": "Bengkulu",
    "Sumatera Selatan": "South Sumatra",
    "Kepulauan Bangka Belitung": "Bangka Belitung",
    "Lampung": "Lampung",
    "Banten": "Banten",
    "Daerah Khusus Ibukota Jakarta": "DKI Jakarta",
    "Jawa Barat": "West Java",
    "Jawa Tengah": "Central Java",
    "DI Yogyakarta": "DI Yogyakarta",
    "Jawa Timur": "East Java",
    "Bali": "Bali",
    "Nusa Tenggara Barat": "West Nusa Tenggara",
    "Nusa Tenggara Timur": "East Nusa Tenggara",
    "Kalimantan Barat": "West Kalimantan",
    "Kalimantan Tengah": "Central Kalimantan",
    "Kalimantan Selatan": "South Kalimantan",
    "Kalimantan Timur": "East Kalimantan",
    "Kalimantan Utara": "North Kalimantan",
    "Sulawesi Utara": "North Sulawesi",
    "Gorontalo": "Gorontalo",
    "Sulawesi Tengah": "Central Sulawesi",
    "Sulawesi Barat": "West Sulawesi",
    "Sulawesi Selatan": "South Sulawesi",
    "Sulawesi Tenggara": "Southeast Sulawesi",
    "Maluku": "Maluku",
    "Maluku Utara": "North Maluku",
    "Papua": "Papua",
    "Papua Barat": "West Papua",
    "Papua Barat Daya": "Southwest Papua",
    "Papua Tengah": "Central Papua",
    "Papua Selatan": "South Papua",
    "Papua Pegunungan": "Highland Papua",
}


def slug(value: str, limit: int = 55) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:limit].rstrip("-")


def parse_location(location: str) -> tuple[list[str], str]:
    text = location.strip()
    if text == "Nasional":
        return ["Indonesia"], "National"
    if text == "Indonesia Bagian Timur":
        return ["Eastern Indonesia"], "National"

    text = text.replace("Provinsi ", "")
    text = text.replace(" dan ", ", ")
    text = re.sub(r"\s+-\s+", ", ", text)
    parts = [part.strip(" ,") for part in text.split(",") if part.strip(" ,")]
    provinces: list[str] = []
    for part in parts:
        if part not in PROVINCE_EN:
            raise SystemExit(f"unmapped province {part!r} in location {location!r}")
        english = PROVINCE_EN[part]
        if english not in provinces:
            provinces.append(english)
    if not provinces:
        raise SystemExit(f"empty location: {location!r}")
    return provinces, island_for(provinces[0])


def project_id(number: int, name: str) -> str:
    return f"psn-{number:03d}-{slug(name)}"


def estate_id(number: int, name: str) -> str:
    return f"psn-estate-{number:03d}-{slug(name)}"


def psn_claims(rows: list[dict[str, str]], key: str) -> set[int]:
    numbers: set[int] = set()
    for row in rows:
        if row["claim"] != "psn":
            continue
        match = re.fullmatch(r"PSN\s+(\d+)", row["claim_value"].strip())
        if match:
            numbers.add(int(match.group(1)))
    return numbers


def upsert(rows: list[dict[str, str]], key: str, incoming: dict[str, str]) -> None:
    for index, row in enumerate(rows):
        if row[key] == incoming[key]:
            rows[index] = incoming
            return
    rows.append(incoming)


def main() -> None:
    register = read_csv(CURATED / "psn_register.csv")
    projects = read_csv(CURATED / "projects.csv")
    estates = read_csv(CURATED / "estates.csv")
    project_claims = read_csv(CURATED / "project_sources.csv")
    estate_claims = read_csv(CURATED / "estate_sources.csv")
    aliases = read_csv(CURATED / "project_aliases.csv")
    sources = {row["id"] for row in read_csv(CURATED / "sources.csv")}

    if REGISTER_SOURCE not in sources:
        raise SystemExit(f"missing source {REGISTER_SOURCE}")

    centroids = json.loads((DERIVED / "province_centroids.json").read_text(encoding="utf-8"))

    represented_projects = (
        set(TRANSPORT_MATCH) | set(PROJECT_MATCH) | set(ESTATE_MATCH)
        | psn_claims(project_claims, "project_id")
    )
    represented_estates = set(ESTATE_MATCH) | psn_claims(estate_claims, "estate_id")

    # Existing register-only rows are updated in place on later runs. A plain
    # "missing" check would skip them once their PSN claim exists.
    existing_project_numbers: set[int] = set()
    for project in projects:
        if project["verification"] != "unverified" or project["status"] != "unknown":
            continue
        match = re.search(r"Register-only PSN (\d+)\.", project["notes"])
        if match:
            existing_project_numbers.add(int(match.group(1)))
    existing_estate_numbers: set[int] = set()
    for estate in estates:
        if estate["status"] != "unknown" or estate["coordinate_source"] != "unknown":
            continue
        match = re.search(r"Register-only PSN (\d+) industrial area", estate["notes"])
        if match:
            existing_estate_numbers.add(int(match.group(1)))

    active = [row for row in register if row["status"] == "active"]
    project_numbers = {
        int(row["psn_no"]) for row in active
        if row["kind"] == "project"
        and row["sector"] != "industrial_areas"
        and int(row["psn_no"]) not in represented_projects
    } | existing_project_numbers
    estate_numbers = {
        int(row["psn_no"]) for row in active
        if row["kind"] == "project"
        and row["sector"] == "industrial_areas"
        and int(row["psn_no"]) not in represented_estates
    } | existing_estate_numbers

    missing_projects = [
        row for row in active
        if row["kind"] == "project"
        and row["sector"] != "industrial_areas"
        and int(row["psn_no"]) in project_numbers
    ]
    missing_estates = [
        row for row in active
        if row["kind"] == "project"
        and row["sector"] == "industrial_areas"
        and int(row["psn_no"]) in estate_numbers
    ]

    unknown_names = [row["psn_no"] for row in missing_projects if int(row["psn_no"]) not in PROJECT_NAMES]
    if unknown_names:
        raise SystemExit(f"missing English working names for PSN {', '.join(unknown_names)}")

    managed_projects: set[str] = set()
    managed_estates: set[str] = set()

    for row in missing_projects:
        number = int(row["psn_no"])
        name_en = PROJECT_NAMES[number]
        identifier = project_id(number, name_en)
        if any(project["id"] == identifier for project in projects):
            managed_projects.add(identifier)
        provinces, island = parse_location(row["location"])
        centroid = centroids.get(provinces[0])
        if not centroid:
            raise SystemExit(f"no province centroid for {provinces[0]!r}")
        sector = SECTOR_BY_REGISTER[row["sector"]]
        subsector = SUBSECTOR.get(sector, "psn_register")
        if sector == "water":
            if "SPAM" in row["name_id"] or "Air Minum" in row["name_id"] or "Air Baku" in row["name_id"]:
                subsector = "water_supply"
            elif "Sewerage" in row["name_id"]:
                subsector = "sanitation"
            elif "Irigasi" in row["name_id"]:
                subsector = "irrigation"
            elif "Bendungan" in row["name_id"] or "Bendung" in row["name_id"]:
                subsector = "dam"
            else:
                subsector = "water_supply"
        elif sector == "energy":
            if number in {206, 208}:
                subsector = "refinery"
            elif number in {209, 210}:
                subsector = "storage"
            elif number in {211, 212}:
                subsector = "pipeline"
            elif number in {213, 214}:
                subsector = "biofuel"
            elif number == 216:
                subsector = "gasification"
            else:
                subsector = "oil_gas"

        managed_projects.add(identifier)
        project = {field: "" for field in PROJECT_FIELDS}
        project.update(
            {
                "id": identifier,
                "name": name_en,
                "sector": sector,
                "subsector": subsector,
                "status": "unknown",
                "status_basis": (
                    f"Permenko 16/2025 lists PSN {number} as active. The annex does not "
                    "state implementation status, cost, capacity, organisation or schedule."
                ),
                "corridor_id": "",
                "island": island,
                "province": "; ".join(provinces),
                "route": name_en,
                "length_km": "",
                "operational_km": "",
                "construction_km": "",
                "progress_pct": "",
                "investment_idr_t": "",
                "capacity": "",
                "capacity_unit": "",
                "psn": "yes",
                "opened_year": "",
                "opened_date": "",
                "expected_open_year": "",
                "status_as_of": REGISTER_DATE,
                "verification": "unverified",
                "lat": f"{centroid['lat']:.5f}",
                "lon": f"{centroid['lon']:.5f}",
                "precision": "province",
                "last_verified": LAST_VERIFIED,
                "notes": (
                    f"Register-only PSN {number}. Official name: {row['name_id']}. "
                    f"Location: {row['location']}. The annex supports the name, number, "
                    "sector, location and active status only. No implementation status, "
                    "cost, capacity, organisation or geometry has been sourced yet. The "
                    "coordinate is a province centroid; the row is not plotted on the map."
                ),
            }
        )
        upsert(projects, "id", project)

        aliases[:] = [alias for alias in aliases if alias["project_id"] != identifier]
        aliases.append(
            {
                "project_id": identifier,
                "alias": row["name_id"],
                "source_id": REGISTER_SOURCE,
                "notes": "Official Indonesian name from the PSN register; atlas English name is a working translation.",
            }
        )

        project_claims[:] = [
            claim for claim in project_claims if claim["project_id"] != identifier
        ]
        for claim, value, note in (
            ("psn", f"PSN {number}", "Permenko 16/2025 annex."),
            ("status", "active in register", "Active in the official PSN register; implementation status is not stated."),
            ("location", row["location"], ""),
        ):
            project_claims.append(
                {
                    "project_id": identifier,
                    "source_id": REGISTER_SOURCE,
                    "claim": claim,
                    "claim_value": value,
                    "claim_date": REGISTER_DATE,
                    "notes": note,
                }
            )

    for row in missing_estates:
        number = int(row["psn_no"])
        identifier = estate_id(number, row["name_id"])
        managed_estates.add(identifier)
        provinces, island = parse_location(row["location"])
        centroid = centroids.get(provinces[0])
        if not centroid:
            raise SystemExit(f"no province centroid for {provinces[0]!r}")
        estate = {field: "" for field in ESTATE_FIELDS}
        estate.update(
            {
                "id": identifier,
                "name": row["name_id"],
                "type": "industrial_estate",
                "province": "; ".join(provinces),
                "regency": "",
                "island": island,
                "lat": f"{centroid['lat']:.5f}",
                "lon": f"{centroid['lon']:.5f}",
                "precision": "province",
                "coordinate_source": "unknown",
                "area_ha": "",
                "developer": "",
                "developer_org_id": "",
                "status": "unknown",
                "sector_focus": "",
                "legal_basis": "",
                "established_year": "",
                "website": "",
                "occupancy_pct": "",
                "kemenperin_id": "",
                "sez_id": "",
                "source_id": REGISTER_SOURCE,
                "last_verified": LAST_VERIFIED,
                "notes": (
                    f"Register-only PSN {number} industrial area. The annex supports the "
                    "name, number, sector, location and active status only. Area, developer, "
                    "occupancy, implementation status and estate boundary are not yet "
                    "sourced. The coordinate is a province centroid; the estate map layer "
                    "is off."
                ),
            }
        )
        upsert(estates, "id", estate)

        estate_claims[:] = [
            claim for claim in estate_claims if claim["estate_id"] != identifier
        ]
        for claim, value, note in (
            ("psn", f"PSN {number}", "Permenko 16/2025 annex."),
            ("status", "active in register", "Active in the official PSN register; implementation status is not stated."),
            ("location", row["location"], ""),
        ):
            estate_claims.append(
                {
                    "estate_id": identifier,
                    "source_id": REGISTER_SOURCE,
                    "claim": claim,
                    "claim_value": value,
                    "claim_date": REGISTER_DATE,
                    "notes": note,
                }
            )

    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)
    write_csv(CURATED / "estates.csv", ESTATE_FIELDS, estates)
    write_csv(CURATED / "project_aliases.csv", ALIAS_FIELDS, aliases)
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, project_claims)
    write_csv(CURATED / "estate_sources.csv", ESTATE_SOURCE_FIELDS, estate_claims)

    print(
        f"OK: {len(missing_projects)} register-only projects and "
        f"{len(missing_estates)} register-only industrial areas"
    )
    print(
        f"projects: {len(projects)}; estates: {len(estates)}; "
        f"project claims: {len(project_claims)}; estate claims: {len(estate_claims)}"
    )


if __name__ == "__main__":
    main()
