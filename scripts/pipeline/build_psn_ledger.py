"""Build the PSN reconciliation ledger.

The register is the official Permenko 16/2025 annex: 226 active projects and
24 active programmes, with the deleted slots retained. This script matches each
active record to the current atlas project or estate where a match exists and
records what is missing. The matches are deliberately explicit rather than
fuzzy: a wrong match is worse than a visible gap.

Run: python scripts/pipeline/build_psn_ledger.py
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import CURATED, DERIVED, read_csv, write_csv

FIELDS = [
    "record_id", "kind", "psn_no", "sector_code", "sector", "name_id", "location",
    "status", "atlas_layer", "atlas_id", "atlas_status", "match_status",
    "match_confidence", "missing_fields", "owner", "next_action", "release",
    "source_id", "notes",
]

# Explicit matches for the 85 transport entries. Values are
# (atlas project id, match status, confidence, note).
TRANSPORT_MATCH = {
    1: ("tol-serang-panimbang", "matched_project", "high", ""),
    2: ("tol-pandaan-malang", "matched_project", "high", ""),
    3: ("tol-manado-bitung", "matched_project", "high", ""),
    4: ("tol-balikpapan-samarinda", "matched_project", "high", ""),
    5: ("tol-medan-binjai", "matched_project", "high", ""),
    6: ("tol-pekanbaru-kandis-dumai", "matched_project", "high", ""),
    8: ("tol-sigli-banda-aceh", "matched_project", "high", ""),
    9: ("tol-binjai-langsa", "matched_project", "high", ""),
    13: ("tol-betung-tempino-jambi", "matched_project", "high", ""),
    16: ("tol-simpang-indralaya-muara-enim", "matched_project", "high", ""),
    17: ("tol-bengkulu-lubuk-linggau", "matched_project", "high", ""),
    18: ("tol-kayu-agung-palembang-betung", "matched_project", "high", ""),
    19: ("tol-cileunyi-sumedang-dawuan", "matched_project", "high", ""),
    20: (
        "tol-ciawi-sukabumi",
        "matched_partial",
        "medium",
        "Atlas row covers Ciawi–Sukabumi; the PSN extends to Ciranjang–Padalarang.",
    ),
    21: ("tol-cengkareng-batu-ceper-kunciran", "matched_project", "high", ""),
    23: ("tol-cinere-jagorawi", "matched_project", "high", ""),
    25: ("tol-cibitung-cilincing", "matched_project", "high", ""),
    26: ("tol-bekasi-cawang-kampung-melayu", "matched_project", "high", ""),
    27: ("tol-serpong-balaraja", "matched_project", "high", ""),
    28: (
        "tol-jakarta-inner-ring-road-2",
        "matched_aggregate",
        "high",
        "Aggregated in the atlas as the six inner-city toll roads.",
    ),
    29: (
        "tol-jakarta-inner-ring-road-2",
        "matched_aggregate",
        "high",
        "Aggregated in the atlas as the six inner-city toll roads.",
    ),
    30: (
        "tol-jakarta-inner-ring-road-2",
        "matched_aggregate",
        "high",
        "Aggregated in the atlas as the six inner-city toll roads.",
    ),
    31: (
        "tol-jakarta-inner-ring-road-2",
        "matched_aggregate",
        "high",
        "Aggregated in the atlas as the six inner-city toll roads.",
    ),
    32: (
        "tol-jakarta-inner-ring-road-2",
        "matched_aggregate",
        "high",
        "Aggregated in the atlas as the six inner-city toll roads.",
    ),
    33: (
        "tol-jakarta-inner-ring-road-2",
        "matched_aggregate",
        "high",
        "Aggregated in the atlas as the six inner-city toll roads.",
    ),
    34: ("tol-pasuruan-probolinggo", "matched_project", "high", ""),
    35: ("tol-probolinggo-banyuwangi", "matched_project", "high", ""),
    36: ("tol-krian-legundi-bunder-manyar", "matched_project", "high", ""),
    37: ("tol-jakarta-cikampek-2-south", "matched_project", "high", ""),
    38: ("tol-semarang-demak", "matched_project", "high", ""),
    39: ("tol-yogyakarta-bawen", "matched_project", "high", ""),
    41: ("tol-ngawi-kertosono-kediri", "matched_project", "high", ""),
    42: ("tol-depok-antasari", "matched_project", "high", ""),
    43: ("tol-solo-yogyakarta-nyia", "matched_project", "high", ""),
    44: ("tol-bogor-ring-road", "matched_project", "high", ""),
    45: ("tol-gedebage-tasikmalaya-cilacap", "matched_project", "high", ""),
    47: (
        "tol-gilimanuk-mengwi",
        "matched_partial",
        "medium",
        "Atlas row is Gilimanuk–Mengwi; the PSN lists the full Negara–Pekutatan–Soka alignment.",
    ),
    49: ("tol-jakarta-harbour-road-2", "matched_project", "high", ""),
    51: ("port-kek-maloy", "matched_project", "high", ""),
    52: (
        "port-sanur",
        "matched_partial",
        "medium",
        "Atlas row is Sanur Port; the PSN includes the Nusa Ceningan/Lembongan link.",
    ),
    53: ("port-likupang", "matched_project", "high", ""),
    54: ("port-makassar-new-port", "matched_project", "high", ""),
    55: ("port-labuan-bajo-multipurpose", "matched_project", "high", ""),
    56: ("port-patimban", "matched_project", "high", ""),
    57: ("port-kijing", "matched_project", "high", ""),
    58: ("port-kupang", "matched_project", "high", ""),
    59: ("port-sorong", "matched_project", "high", ""),
    60: ("port-teluk-palu", "matched_project", "high", ""),
    61: ("port-kuala-tanjung", "matched_project", "high", ""),
    62: ("port-bitung", "matched_project", "high", ""),
    63: ("port-benoa", "matched_project", "high", ""),
    64: ("port-palembang-baru", "matched_project", "high", ""),
    65: ("port-muaro-jambi", "matched_project", "high", ""),
    66: ("air-yogyakarta-international", "matched_project", "high", ""),
    67: ("air-kediri", "matched_project", "high", ""),
    68: ("air-komodo-labuan-bajo", "matched_project", "high", ""),
    69: ("air-lombok-praya", "matched_project", "high", ""),
    70: ("air-nabire", "matched_project", "high", ""),
    71: ("air-siboru-fakfak", "matched_project", "high", ""),
    72: ("air-raja-haji-abdullah-karimun", "matched_project", "high", ""),
    73: ("rail-makassar-parepare", "matched_project", "high", ""),
    74: ("rail-tebing-tinggi-kuala-tanjung", "matched_project", "high", ""),
    75: ("rail-rantau-prapat-kota-pinang", "matched_project", "high", ""),
    76: ("rail-yogyakarta-airport", "matched_project", "high", ""),
    77: ("rail-double-track-java-south", "matched_project", "high", ""),
    78: ("rail-kcj-jakarta-bandung", "matched_project", "high", ""),
    79: ("rail-lrt-jabodebek", "matched_project", "high", ""),
    80: ("rail-lahat-kertapati", "matched_project", "high", ""),
    81: ("rail-kaltim-logistics", "matched_project", "high", ""),
    82: ("rail-lrt-sumsel", "matched_project", "high", ""),
    83: ("rail-lrt-jakarta-velodrome-manggarai", "matched_project", "high", ""),
    84: ("rail-mrt-jakarta-north-south", "matched_project", "high", ""),
    85: ("rail-mrt-jakarta-east-west", "matched_project", "high", ""),
}

# Explicit matches for non-transport projects added in the V4 flagship
# increment. Values are (atlas project id, match status, confidence, note).
PROJECT_MATCH = {
    141: ("dam-keureuto", "matched_project", "high", ""),
    147: ("dam-rukoh", "matched_project", "high", ""),
    161: ("dam-sidan", "matched_project", "high", ""),
    170: ("dam-meninting", "matched_project", "high", ""),
    175: ("dam-jlantah", "matched_project", "high", ""),
    199: (
        "coastal-java-sea-wall",
        "matched_partial",
        "medium",
        "Register No. 199 covers the Jakarta/West Java coastal dyke; the atlas row covers the 15-segment national programme.",
    ),
    200: ("energy-masela-abadi-lng", "matched_project", "high", ""),
    207: (
        "energy-rdmp-balikpapan",
        "matched_partial",
        "medium",
        "Register No. 207 aggregates the RDMP programme; this atlas row is the Balikpapan component.",
    ),
    215: (
        "energy-hilirisasi-2-06-tanjung-enim-dme",
        "matched_partial",
        "medium",
        "Register No. 215 lists coal gasification at Tanjung Enim; the atlas row is the 1.4 Mtpa DME project announced in stage II.",
    ),
}

# Explicit matches for the 44 industrial-area entries.
ESTATE_MATCH = {
    87: ("ki-kawasan-industri-landak", "high", ""),
    88: (
        "ki-ketapang-ecology-and-agriculture-forestery-industrial-park",
        "medium",
        "Atlas name differs; the location matches Ketapang, West Kalimantan.",
    ),
    89: ("ki-kawasan-industri-jorong", "high", ""),
    91: ("ki-kawasan-industri-morowali", "high", ""),
    92: ("ki-kawasan-industri-konawe", "high", ""),
    95: ("ki-kawasan-industri-terpadu-wilmar", "high", ""),
    96: ("ki-kawasan-industri-pulau-obi", "high", ""),
    97: (
        "ki-kawasan-industri-teluk-weda",
        "medium",
        "Atlas name is Teluk Weda; this is the Weda Bay industrial area.",
    ),
    98: ("ki-ki-takalar", "high", ""),
    99: ("ki-kawasan-industri-tanjung-enim", "high", ""),
    101: (
        "ki-batang-industrial-park",
        "medium",
        "Verify that Batang Industrial Park is the same KIT Batang project.",
    ),
    102: ("ki-indonesia-konawe-industrial-park", "high", ""),
    103: ("sez-tanjung-sauh", "high", ""),
    105: ("ki-kawasan-industri-motui", "high", ""),
    109: ("ki-indonesia-huabao-industrial-park-ihip", "high", ""),
    114: ("ki-neo-energy-parimo-industrial-estate", "high", ""),
}

MISSING_FIELDS = {
    "project": "name_en, summary_id, summary_en, sector_detail, status, status_as_of, coordinates, source, claim, programme_id, organization_roles",
    "estate": "name_en, summary_id, summary_en, area_ha, occupancy_pct, developer, coordinates, source",
    "programme": "name_en, summary_id, summary_en, indicators, budget, lead_org, sources",
    "matched_project": "name_id, summary_id, summary_en, programme_id, pkpn_id, translation_status",
    "matched_estate": "name_en, summary_id, summary_en, translation_status",
    "matched_partial": "review_match, name_id, summary_id, summary_en, programme_id",
    "matched_aggregate": "review_match, name_id, summary_id, summary_en, programme_id",
    "deleted": "",
}

RELEASE_BY_SECTOR = {
    "roads_and_bridges": "4.1",
    "ports": "4.1",
    "airports": "4.1",
    "railways": "4.1",
    "industrial_areas": "4.2",
    "housing": "4.1",
    "dams_and_irrigation": "4.1",
    "water_and_sanitation": "4.1",
    "coastal_defence": "4.1",
    "energy": "4.1",
    "technology": "4.2",
    "education": "4.2",
    "tourism": "4.2",
    "agriculture": "4.1",
    "programme": "4.1",
}


def release_for(row: dict[str, str]) -> str:
    if row["kind"] == "programme" and int(row["psn_no"]) >= 17:
        return "4.2"
    return RELEASE_BY_SECTOR[row["sector"]]


def main() -> None:
    register = read_csv(CURATED / "psn_register.csv")
    projects = {row["id"]: row for row in read_csv(CURATED / "projects.csv")}
    estates = {row["id"]: row for row in read_csv(CURATED / "estates.csv")}

    if len(register) != 253:
        raise SystemExit(f"PSN register should have 253 rows, found {len(register)}")
    active_projects = [r for r in register if r["kind"] == "project" and r["status"] == "active"]
    active_programmes = [r for r in register if r["kind"] == "programme" and r["status"] == "active"]
    deleted = [r for r in register if r["status"] == "deleted"]
    if len(active_projects) != 226:
        raise SystemExit(f"PSN register should have 226 active projects, found {len(active_projects)}")
    if len(active_programmes) != 24:
        raise SystemExit(f"PSN register should have 24 active programmes, found {len(active_programmes)}")
    if len(deleted) != 3:
        raise SystemExit(f"PSN register should have 3 deleted slots, found {len(deleted)}")

    for number, (project_id, _, _, _) in TRANSPORT_MATCH.items():
        if project_id not in projects:
            raise SystemExit(f"PSN {number} maps to unknown project {project_id}")
    for number, (project_id, _, _, _) in PROJECT_MATCH.items():
        if project_id not in projects:
            raise SystemExit(f"PSN {number} maps to unknown project {project_id}")
    for number, (estate_id, _, _) in ESTATE_MATCH.items():
        if estate_id not in estates:
            raise SystemExit(f"PSN {number} maps to unknown estate {estate_id}")

    out = []
    for row in register:
        item = {
            "record_id": row["id"],
            "kind": row["kind"],
            "psn_no": row["psn_no"],
            "sector_code": row["sector_code"],
            "sector": row["sector"],
            "name_id": row["name_id"],
            "location": row["location"],
            "status": row["status"],
            "atlas_layer": "",
            "atlas_id": "",
            "atlas_status": "",
            "match_status": "",
            "match_confidence": "",
            "missing_fields": "",
            "owner": "",
            "next_action": "",
            "release": "",
            "source_id": row["source_id"],
            "notes": "",
        }

        if row["status"] == "deleted":
            item.update(
                match_status="deleted",
                next_action="none",
                notes="Deleted slot; retained for audit against the official numbering.",
            )
            out.append(item)
            continue

        if row["kind"] == "programme":
            item.update(
                match_status="missing_programme",
                missing_fields=MISSING_FIELDS["programme"],
                owner="data",
                next_action="add_programme",
                release=release_for(row),
                notes="Programme-level record; the atlas has no programme layer yet.",
            )
            out.append(item)
            continue

        number = int(row["psn_no"])
        if number in PROJECT_MATCH:
            atlas_id, status, confidence, note = PROJECT_MATCH[number]
            item.update(
                atlas_layer="project",
                atlas_id=atlas_id,
                atlas_status=projects[atlas_id]["status"],
                match_status=status,
                match_confidence=confidence,
                missing_fields=MISSING_FIELDS.get(status, MISSING_FIELDS["matched_project"]),
                owner="translation" if status == "matched_project" else "data",
                next_action="add_translation" if status == "matched_project" else "review_match",
                release=release_for(row),
                notes=note,
            )
        elif number in TRANSPORT_MATCH:
            atlas_id, status, confidence, note = TRANSPORT_MATCH[number]
            item.update(
                atlas_layer="project",
                atlas_id=atlas_id,
                atlas_status=projects[atlas_id]["status"],
                match_status=status,
                match_confidence=confidence,
                missing_fields=MISSING_FIELDS.get(status, MISSING_FIELDS["matched_project"]),
                owner="translation" if status == "matched_project" else "data",
                next_action="add_translation" if status == "matched_project" else "review_match",
                release=release_for(row),
                notes=note,
            )
        elif number in ESTATE_MATCH:
            atlas_id, confidence, note = ESTATE_MATCH[number]
            item.update(
                atlas_layer="estate",
                atlas_id=atlas_id,
                atlas_status=estates[atlas_id]["status"],
                match_status="matched_estate",
                match_confidence=confidence,
                missing_fields=MISSING_FIELDS["matched_estate"],
                owner="translation",
                next_action="add_translation",
                release=release_for(row),
                notes=note,
            )
        elif row["sector"] == "industrial_areas":
            item.update(
                match_status="missing_estate",
                missing_fields=MISSING_FIELDS["estate"],
                owner="data",
                next_action="add_estate",
                release=release_for(row),
                notes="No matching atlas estate row as of 2026-11-09.",
            )
        else:
            item.update(
                match_status="missing_project",
                missing_fields=MISSING_FIELDS["project"],
                owner="data",
                next_action="add_project",
                release=release_for(row),
                notes="No matching atlas project row as of 2026-11-09.",
            )
        out.append(item)

    write_csv(DERIVED / "psn_reconciliation.csv", FIELDS, out)

    counts = Counter(item["match_status"] for item in out if item["status"] == "active")
    print("PSN reconciliation: 226 active projects + 24 active programmes")
    for status in [
        "matched_project", "matched_aggregate", "matched_partial", "matched_estate",
        "missing_project", "missing_estate", "missing_programme",
    ]:
        print(f"  {status:18} {counts.get(status, 0):3}")

    linked = {item["atlas_id"] for item in out if item["atlas_layer"] == "project"}
    print(f"  atlas projects linked {len(linked):3} of {len(projects)}")
    linked_estates = {item["atlas_id"] for item in out if item["atlas_layer"] == "estate"}
    print(f"  atlas estates linked  {len(linked_estates):3} of {len(estates)}")

    by_sector = defaultdict(lambda: [0, 0, 0])
    for item in out:
        if item["status"] != "active" or item["kind"] != "project":
            continue
        bucket = by_sector[item["sector"]]
        bucket[0] += 1
        if item["match_status"].startswith("matched"):
            bucket[1] += 1
        else:
            bucket[2] += 1
    print("  by sector (total / matched / missing):")
    for sector in sorted(by_sector):
        total, matched, missing = by_sector[sector]
        print(f"    {sector:22} {total:3} / {matched:3} / {missing:3}")


if __name__ == "__main__":
    main()
