"""Complete the BPJT toll-road register with the non-PSN sections.

The official BPJT toll-road list archived on 6 November 2026 names 77 sections.
The atlas already carried all 50 PSN road entries but only part of the non-PSN
register. This script adds the 39 non-PSN sections that had no curated row, so
that every section in the official register is represented.

Everything factual comes from that archived JSON:

* section name, concession operator (``bujt_name``), PSN status;
* operational status (``Operasi`` or ``Operasi Sebagian``);
* section length, operational and construction km;
* operation-decree date (``sk_operasi``);
* start and end coordinates, from which the marker point is derived.

Two source quirks are handled explicitly rather than silently:

* BPJT reports a zero ``length`` for three Jakarta and Makassar sections. The
  operational length is used instead and the row notes it.
* BPJT reports more operational km than the section length on nine sections
  (the operational figure appears to include ramps). Those figures stay in the
  claim, but the row omits ``operational_km`` because publishing both would
  contradict the row. One dataset conflict records the pattern.

The script also corrects ``tol-kuala-tanjung-tebing-tinggi-parapat``: its note
claimed the section was absent from the BPJT API, and its operator came from
Indonesian Wikipedia. The API does list the section and names PT Hutama Marga
Waskita as the concession operator, so the link moves to that company and two
resolved conflicts keep the Wikipedia values.

Run: python scripts/imports/add_bpjt_non_psn_toll_rows.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_i18n.py
      python scripts/build_all.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CONFLICT_FIELDS,
    CURATED,
    EVENT_FIELDS,
    ORG_FIELDS,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    RAW,
    TRANSLATION_FIELDS,
    read_csv,
    write_csv,
)

SOURCE = "src-bpjt-toll-road-list-2026-11-06"
WIKI = "src-idwiki-daftar-jalan-tol-30025554"
AS_OF = "2026-11-06"
REVIEWED = "2026-11-10"
ARCHIVE = RAW / "2026-11-06" / "bpjt_toll_road_list.json"

# ruas: exact name in the BPJT API. province, island and corridor are curated.
ROWS = [
    dict(ruas="Pemalang - Batang", id="tol-pemalang-batang",
         name="Pemalang–Batang Toll Road", name_id="Jalan Tol Pemalang–Batang",
         province="Central Java", island="Java", corridor="trans-java"),
    dict(ruas="Indrapura - Kisaran", id="tol-indrapura-kisaran",
         name="Indrapura–Kisaran Toll Road", name_id="Jalan Tol Indrapura–Kisaran",
         province="North Sumatra", island="Sumatra", corridor="trans-sumatera"),
    dict(ruas="Cikampek - Padalarang", id="tol-cikampek-padalarang",
         name="Cikampek–Padalarang Toll Road", name_id="Jalan Tol Cikampek–Padalarang",
         province="West Java", island="Java", corridor=""),
    dict(ruas="Jakarta - Cikampek II Elevated", id="tol-jakarta-cikampek-2-elevated",
         name="Jakarta–Cikampek II Elevated Toll Road",
         name_id="Jalan Tol Jakarta–Cikampek II Elevated",
         province="DKI Jakarta; West Java", island="Java", corridor="trans-java"),
    dict(ruas="Terbanggi Besar - Pematang Panggang - Kayu Agung",
         id="tol-terbanggi-besar-kayu-agung",
         name="Terbanggi Besar–Pematang Panggang–Kayu Agung Toll Road",
         name_id="Jalan Tol Terbanggi Besar–Pematang Panggang–Kayu Agung",
         province="Lampung; South Sumatra", island="Sumatra",
         corridor="trans-sumatera"),
    dict(ruas="Batang - Semarang", id="tol-batang-semarang",
         name="Batang–Semarang Toll Road", name_id="Jalan Tol Batang–Semarang",
         province="Central Java", island="Java", corridor="trans-java"),
    dict(ruas="Bakauheni - Terbanggi Besar", id="tol-bakauheni-terbanggi-besar",
         name="Bakauheni–Terbanggi Besar Toll Road",
         name_id="Jalan Tol Bakauheni–Terbanggi Besar",
         province="Lampung", island="Sumatra", corridor="trans-sumatera"),
    dict(ruas="Solo - Mantingan - Ngawi", id="tol-solo-mantingan-ngawi",
         name="Solo–Mantingan–Ngawi Toll Road", name_id="Jalan Tol Solo–Mantingan–Ngawi",
         province="Central Java; East Java", island="Java", corridor="trans-java"),
    dict(ruas="Soreang - Pasir koja", id="tol-soreang-pasirkoja",
         name="Soreang–Pasirkoja Toll Road", name_id="Jalan Tol Soreang–Pasirkoja",
         province="West Java", island="Java", corridor=""),
    dict(ruas="Palembang - Simpang Indralaya", id="tol-palembang-simpang-indralaya",
         name="Palembang–Simpang Indralaya Toll Road",
         name_id="Jalan Tol Palembang–Simpang Indralaya",
         province="South Sumatra", island="Sumatra", corridor="trans-sumatera"),
    dict(ruas="Medan - Kualanamu - Tebing Tinggi",
         id="tol-medan-kualanamu-tebing-tinggi",
         name="Medan–Kualanamu–Tebing Tinggi Toll Road",
         name_id="Jalan Tol Medan–Kualanamu–Tebing Tinggi",
         province="North Sumatra", island="Sumatra", corridor=""),
    dict(ruas="Pejagan - Pemalang", id="tol-pejagan-pemalang",
         name="Pejagan–Pemalang Toll Road", name_id="Jalan Tol Pejagan–Pemalang",
         province="Central Java", island="Java", corridor="trans-java"),
    dict(ruas="Gempol - Pandaan", id="tol-gempol-pandaan",
         name="Gempol–Pandaan Toll Road", name_id="Jalan Tol Gempol–Pandaan",
         province="East Java", island="Java", corridor="trans-java"),
    dict(ruas="Cikampek - Palimanan", id="tol-cikampek-palimanan",
         name="Cikampek–Palimanan Toll Road", name_id="Jalan Tol Cikampek–Palimanan",
         province="West Java", island="Java", corridor="trans-java"),
    dict(ruas="Kertosono - Mojokerto", id="tol-kertosono-mojokerto",
         name="Kertosono–Mojokerto Toll Road", name_id="Jalan Tol Kertosono–Mojokerto",
         province="East Java", island="Java", corridor="trans-java"),
    dict(ruas="JORR W2 Utara", id="tol-jorr-w2-utara",
         name="JORR W2 North Toll Road", name_id="Jalan Tol JORR W2 Utara",
         province="DKI Jakarta", island="Java", corridor=""),
    dict(ruas="Nusa Dua - Ngurah Rai - Benoa (Bali Mandara)",
         id="tol-bali-mandara",
         name="Bali Mandara Toll Road", name_id="Jalan Tol Bali Mandara",
         province="Bali", island="Bali-Nusa Tenggara", corridor=""),
    dict(ruas="Semarang - Solo", id="tol-semarang-solo",
         name="Semarang–Solo Toll Road", name_id="Jalan Tol Semarang–Solo",
         province="Central Java", island="Java", corridor="trans-java"),
    dict(ruas="Surabaya - Mojokerto", id="tol-surabaya-mojokerto",
         name="Surabaya–Mojokerto Toll Road", name_id="Jalan Tol Surabaya–Mojokerto",
         province="East Java", island="Java", corridor="trans-java"),
    dict(ruas="JORR W1 (Kebon Jeruk - Penjaringan)", id="tol-jorr-w1",
         name="JORR W1 Toll Road", name_id="Jalan Tol JORR W1",
         province="DKI Jakarta", island="Java", corridor=""),
    dict(ruas="Kanci - Pejagan", id="tol-kanci-pejagan",
         name="Kanci–Pejagan Toll Road", name_id="Jalan Tol Kanci–Pejagan",
         province="Central Java", island="Java", corridor="trans-java"),
    dict(ruas="Makassar Seksi IV", id="tol-makassar-section-4",
         name="Makassar Section IV Toll Road", name_id="Jalan Tol Makassar Seksi IV",
         province="South Sulawesi", island="Sulawesi", corridor=""),
    dict(ruas="SS Waru - Bandara Juanda", id="tol-waru-juanda",
         name="Waru–Juanda Airport Toll Road", name_id="Jalan Tol Waru–Bandara Juanda",
         province="East Java", island="Java", corridor=""),
    dict(ruas="JORR NON S", id="tol-jorr-non-s",
         name="JORR Non-S Toll Road", name_id="Jalan Tol JORR Non-S",
         province="DKI Jakarta", island="Java", corridor=""),
    dict(ruas="Gempol - Pasuruan", id="tol-gempol-pasuruan",
         name="Gempol–Pasuruan Toll Road", name_id="Jalan Tol Gempol–Pasuruan",
         province="East Java", island="Java", corridor="trans-java"),
    dict(ruas="Pondok Aren - Serpong", id="tol-pondok-aren-serpong",
         name="Pondok Aren–Serpong Toll Road", name_id="Jalan Tol Pondok Aren–Serpong",
         province="Banten", island="Java", corridor=""),
    dict(ruas="Pondok Aren - Bintaro Viaduct - Ulujami",
         id="tol-pondok-aren-bintaro-ulujami",
         name="Pondok Aren–Bintaro Viaduct–Ulujami Toll Road",
         name_id="Jalan Tol Pondok Aren–Bintaro Viaduct–Ulujami",
         province="Banten; DKI Jakarta", island="Java", corridor=""),
    dict(ruas="Ujung Pandang Seksi 1, 2 dan 3", id="tol-ujung-pandang-1-3",
         name="Ujung Pandang Sections 1–3 Toll Road",
         name_id="Jalan Tol Ujung Pandang Seksi 1, 2 dan 3",
         province="South Sulawesi", island="Sulawesi", corridor=""),
    dict(ruas="Palimanan - Plumbon - Kanci", id="tol-palimanan-plumbon-kanci",
         name="Palimanan–Plumbon–Kanci Toll Road",
         name_id="Jalan Tol Palimanan–Plumbon–Kanci",
         province="West Java", island="Java", corridor="trans-java"),
    dict(ruas="Cawang - Tomang - Pluit", id="tol-cawang-tomang-pluit",
         name="Cawang–Tomang–Pluit Toll Road", name_id="Jalan Tol Cawang–Tomang–Pluit",
         province="DKI Jakarta", island="Java", corridor=""),
    dict(ruas="JORR S (Pondok Pinang - TMII)", id="tol-jorr-s",
         name="JORR S Toll Road", name_id="Jalan Tol JORR S",
         province="DKI Jakarta", island="Java", corridor=""),
    dict(ruas="Surabaya - Gresik", id="tol-surabaya-gresik",
         name="Surabaya–Gresik Toll Road", name_id="Jalan Tol Surabaya–Gresik",
         province="East Java", island="Java", corridor=""),
    dict(ruas="Tangerang - Merak", id="tol-tangerang-merak",
         name="Tangerang–Merak Toll Road", name_id="Jalan Tol Tangerang–Merak",
         province="Banten", island="Java", corridor="trans-java"),
    dict(ruas="Padalarang - Cileunyi", id="tol-padalarang-cileunyi",
         name="Padalarang–Cileunyi Toll Road", name_id="Jalan Tol Padalarang–Cileunyi",
         province="West Java", island="Java", corridor=""),
    dict(ruas="Belawan - Medan - Tanjung Morawa",
         id="tol-belawan-medan-tanjung-morawa",
         name="Belawan–Medan–Tanjung Morawa Toll Road",
         name_id="Jalan Tol Belawan–Medan–Tanjung Morawa",
         province="North Sumatra", island="Sumatra", corridor=""),
    dict(ruas="Surabaya - Gempol", id="tol-surabaya-gempol",
         name="Surabaya–Gempol Toll Road", name_id="Jalan Tol Surabaya–Gempol",
         province="East Java", island="Java", corridor="trans-java"),
    dict(ruas="Prof.Dr.Ir.Soedijatmo", id="tol-soedijatmo",
         name="Prof. Dr. Ir. Soedijatmo Toll Road",
         name_id="Jalan Tol Prof. Dr. Ir. Soedijatmo",
         province="DKI Jakarta", island="Java", corridor=""),
    dict(ruas="Semarang Seksi ABC", id="tol-semarang-abc",
         name="Semarang ABC Sections Toll Road", name_id="Jalan Tol Semarang Seksi ABC",
         province="Central Java", island="Java", corridor=""),
    dict(ruas="Jakarta - Bogor - Ciawi", id="tol-jakarta-bogor-ciawi",
         name="Jakarta–Bogor–Ciawi Toll Road", name_id="Jalan Tol Jakarta–Bogor–Ciawi",
         province="DKI Jakarta; West Java", island="Java", corridor=""),
]

# BPJT operator string -> organization id for the companies that already exist.
# The rest are created from the same field below.
BUJT_ORG = {
    "PT Cibitung Tanjung Priok Port Tollways": "org-cibitung-tanjung-priok-port-tollways",
    "PT Cinere Serpong Jaya": "org-cinere-serpong-jaya",
    "PT Citra Karya Jabar Tol": "org-citra-karya-jabar-tol",
    "PT Citra Waspphutowa": "org-citra-waspphutowa",
    "PT Hutama Karya (Persero)": "org-hutama-karya",
    "PT Jakarta Tollroad Development": "org-jakarta-tollroad-development",
    "PT Jasamarga Jogja Solo": "org-jasamarga-jogja-solo",
    "PT Jasamarga Manado Bitung": "org-jasamarga-manado-bitung",
    "PT Jasamarga Ngawi Kertosono Kediri": "org-jasamarga-ngawi-kertosono-kediri",
    "PT Jasamarga Pandaan Malang": "org-jasamarga-pandaan-malang",
    "PT Jasamarga Probolinggo Banyuwangi": "org-jasamarga-probolinggo-banyuwangi",
    "PT Kresna Kusuma Dyandra Marga": "org-kresna-kusuma-dyandra-marga",
    "PT Pembangunan Perumahan Semarang Demak": "org-pp-semarang-demak",
    "PT Trans Bumi Serbaraja": "org-trans-bumi-serbaraja",
    "PT Trans Jabar Tol": "org-trans-jabar-tol",
    "PT Trans Jawa Paspro Jalan Tol": "org-trans-jawa-paspro-jalan-tol",
    "PT Translingkar Kita Jaya": "org-translingkar-kita-jaya",
    "PT Waskita Bumi Wira": "org-waskita-bumi-wira",
    "PT Wijaya Karya Serang Panimbang": "org-wijaya-karya-serang-panimbang",
    "PT. Cimanggis Cibitung Tollways": "org-cimanggis-cibitung-tollways",
    "PT. Citra Marga Nusaphala Persada Tbk.": "org-citra-marga-nusaphala-persada",
    "PT. Jasa Marga (Persero) Tbk": "org-jasa-marga",
    "PT. Jasamarga Balikpapan Samarinda": "org-jasamarga-balikpapan-samarinda",
    "PT. Jasamarga Kunciran Cengkareng": "org-jasamarga-kunciran-cengkareng",
    "PT. Marga Sarana Jabar": "org-marga-sarana-jabar",
    "PT. Marga Trans Nusantara": "org-marga-trans-nusantara",
    "PT. Medan Binjai Tol": "org-medan-binjai-tol",
    "PT. Waskita Sriwijaya Tol": "org-waskita-sriwijaya-tol",
}

# BPJT operator string -> new organization id.
NEW_BUJT = {
    "PT Bakauheni Terbanggi Besar Toll": "org-bakauheni-terbanggi-besar-toll",
    "PT Citra Margatama Surabaya": "org-citra-margatama-surabaya",
    "PT Duta Graha Karya": "org-duta-graha-karya",
    "PT Hutama Marga Waskita": "org-hutama-marga-waskita",
    "PT Jalan Tol Seksi Empat": "org-jalan-tol-seksi-empat",
    "PT Jasamarga Bali Tol": "org-jasamarga-bali-tol",
    "PT Jasamarga Gempol Pasuruan": "org-jasamarga-gempol-pasuruan",
    "PT Jasamarga Jalanlayang Cikampek": "org-jasamarga-jalanlayang-cikampek",
    "PT Jasamarga Kualanamu Tol": "org-jasamarga-kualanamu-tol",
    "PT Jasamarga Pandaan Tol": "org-jasamarga-pandaan-tol",
    "PT Jasamarga Solo Ngawi": "org-jasamarga-solo-ngawi",
    "PT Jasamarga Surabaya Mojokerto": "org-jasamarga-surabaya-mojokerto",
    "PT Jasamarga Transjawa Tol": "org-jasamarga-transjawa-tol",
    "PT Makassar Metro Network": "org-makassar-metro-network",
    "PT Marga Harjaya Infrastruktur": "org-marga-harjaya-infrastruktur",
    "PT Marga Lingkar Jakarta": "org-marga-lingkar-jakarta",
    "PT Marga Mandala Sakti": "org-marga-mandala-sakti",
    "PT Pemalang Batang Tol Road": "org-pemalang-batang-tol-road",
    "PT Semesta Marga Raya": "org-semesta-marga-raya",
    "PT. Bintaro Serpong Damai": "org-bintaro-serpong-damai",
    "PT. Citra Marga Lintas Jabar": "org-citra-marga-lintas-jabar",
    "PT. Jakarta Lingkar Baratsatu": "org-jakarta-lingkar-baratsatu",
    "PT. Jasamarga Semarang Batang": "org-jasamarga-semarang-batang",
    "PT. Lintas Marga Sedaya": "org-lintas-marga-sedaya",
    "PT. Margabumi Matraraya": "org-margabumi-matraraya",
    "PT. Pejagan Pemalang Tol Road": "org-pejagan-pemalang-tol-road",
    "PT. Trans Marga Jateng": "org-trans-marga-jateng",
}

MONTHS = [
    "", "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]

NUMBER_WORDS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve",
]


def count_word(value: int) -> str:
    return NUMBER_WORDS[value] if 0 <= value < len(NUMBER_WORDS) else str(value)


def fmt(value: float) -> str:
    text = f"{value:.3f}".rstrip("0").rstrip(".")
    return text or "0"


def long_date(value: str) -> str:
    year, month, day = (int(part) for part in value.split("-"))
    return f"{day} {MONTHS[month]} {year}"


def main() -> None:
    api = json.loads(ARCHIVE.read_text(encoding="utf-8"))["data"]
    by_ruas = {row["ruas_name"]: row for row in api}

    # Organisations -------------------------------------------------------
    orgs = read_csv(CURATED / "organizations.csv")
    org_ids = {row["id"] for row in orgs}
    added_orgs = 0
    for bujt, org_id in NEW_BUJT.items():
        if org_id in org_ids:
            continue
        orgs.append(
            {
                "id": org_id,
                "name": bujt,
                "short_name": bujt.replace("PT. ", "").replace("PT ", "")
                .replace(" (Persero)", "").replace(" Tbk", ""),
                "org_type": "private",
                "country_code": "ID",
                "parent_id": "",
                "website": "",
                "notes": "Toll-road concession operator from the BPJT list.",
            }
        )
        org_ids.add(org_id)
        added_orgs += 1
    orgs.sort(key=lambda row: row["id"])
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, orgs)

    # Projects ------------------------------------------------------------
    projects = read_csv(CURATED / "projects.csv")
    project_ids = {row["id"] for row in projects}
    added_projects = 0
    added_claims = 0
    added_events = 0
    added_links = 0
    added_translations = 0

    claims = read_csv(CURATED / "project_sources.csv")
    claim_keys = {
        (row["project_id"], row["source_id"], row["claim"]) for row in claims
    }
    events = read_csv(CURATED / "project_events.csv")
    event_ids = {row["id"] for row in events}
    links = read_csv(CURATED / "project_organizations.csv")
    link_keys = {(row["project_id"], row["org_id"], row["role"]) for row in links}
    translations = read_csv(CURATED / "translations.csv")
    translation_keys = {
        (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        for row in translations
    }

    zero_length = []
    op_over_length = []

    for spec in ROWS:
        api_row = by_ruas[spec["ruas"]]
        length = float(api_row["length"])
        operational = float(api_row["panjang_operasi_km"] or 0)
        construction = float(api_row["panjang_konstruksi_km"] or 0)
        partial = api_row["status_ruas"] != "Operasi"
        status = "under_construction" if partial else "operating"
        decree = api_row["sk_operasi"][:10]
        bujt = api_row["bujt_name"]

        notes = []
        if length <= 0:
            length = operational
            zero_length.append(spec["id"])
            notes.append(
                "BPJT reports a zero section length; the operational length is used."
            )
        publish_operational = ""
        if operational and operational <= length * 1.05:
            publish_operational = fmt(operational)
        elif operational:
            op_over_length.append(spec["id"])
            notes.append(
                f"BPJT reports {fmt(operational)} km in operation against a "
                f"section length of {fmt(length)} km. The operational figure is "
                "kept in the claim only, because publishing both would contradict "
                "the row."
            )

        route = f"{spec['name']}, {spec['province']}"

        def sane(lat: float, lon: float) -> bool:
            return -11.5 <= lat <= 6.5 and 94 <= lon <= 141.5

        start = (float(api_row["start_latitude"]), float(api_row["start_longitude"]))
        end = (float(api_row["end_latitude"]), float(api_row["end_longitude"]))
        if sane(*start) and sane(*end):
            point = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            notes.insert(
                0,
                "Coordinates are the midpoint of the BPJT start and end points, "
                "approximate.",
            )
        elif sane(*start):
            point = start
            notes.insert(
                0, "Coordinates are the BPJT start point, approximate."
            )
            notes.append(
                "The BPJT end point for this section is malformed, so the start "
                "point is used."
            )
        elif sane(*end):
            point = end
            notes.insert(0, "Coordinates are the BPJT end point, approximate.")
            notes.append(
                "The BPJT start point for this section is malformed, so the end "
                "point is used."
            )
        else:
            point = None
        if partial:
            basis = (
                f"BPJT toll-road list (6 Nov 2026): {api_row['status_ruas']}, "
                f"{fmt(operational)} of {fmt(length)} km operational."
            )
        elif publish_operational:
            basis = (
                f"BPJT toll-road list (6 Nov 2026): Operasi, "
                f"{fmt(operational)} of {fmt(length)} km operational; "
                f"operation decree {decree[:4]}."
            )
        else:
            basis = (
                f"BPJT toll-road list (6 Nov 2026): Operasi; operation decree "
                f"{decree[:4]}. The API's operational figure exceeds the section "
                "length and is recorded in the claim only."
            )

        row = {
            "id": spec["id"],
            "name": spec["name"],
            "sector": "road",
            "subsector": "toll",
            "status": status,
            "status_basis": basis,
            "corridor_id": spec["corridor"],
            "island": spec["island"],
            "province": spec["province"],
            "route": route,
            "length_km": fmt(length),
            "operational_km": publish_operational,
            "construction_km": fmt(construction) if construction else "",
            "progress_pct": "",
            "investment_idr_t": "",
            "capacity": "",
            "capacity_unit": "",
            "psn": "no",
            "opened_year": decree[:4] if status == "operating" else "",
            "opened_date": "",
            "expected_open_year": "",
            "status_as_of": AS_OF,
            "verification": "official",
            "lat": fmt(point[0]) if point else "",
            "lon": fmt(point[1]) if point else "",
            "precision": "approximate",
            "last_verified": REVIEWED,
            "notes": " ".join(notes),
        }
        if spec["id"] in project_ids:
            # Upsert so a rerun repairs a row written from an older rule.
            for index, existing in enumerate(projects):
                if existing["id"] == spec["id"]:
                    projects[index] = row
                    break
        else:
            projects.append(row)
            project_ids.add(spec["id"])
            added_projects += 1

        # Claims
        claim_rows = [
            ("status", status),
            ("length", f"{fmt(length)} km"),
            ("location", f"{spec['province']} — {route}"),
            ("operator", bujt),
        ]
        if operational:
            value = f"{fmt(operational)} km"
            note = ""
            if not publish_operational:
                note = (
                    f"Exceeds the {fmt(length)} km section length; see the project "
                    "notes."
                )
            claim_rows.append(("operational", value, note))
        if status == "operating":
            claim_rows.append(
                ("opening", decree, "BPJT operation decree (SK operasi).")
            )
        for claim in claim_rows:
            name, value = claim[0], claim[1]
            note = claim[2] if len(claim) > 2 else ""
            key = (spec["id"], SOURCE, name)
            if key in claim_keys:
                continue
            claims.append(
                {
                    "project_id": spec["id"],
                    "source_id": SOURCE,
                    "claim": name,
                    "claim_value": value,
                    "claim_date": AS_OF,
                    "notes": note,
                }
            )
            claim_keys.add(key)
            added_claims += 1

        # Event
        event_id = f"evt-{spec['id'][4:]}-{decree}"
        if event_id not in event_ids:
            if partial:
                description = (
                    f"{spec['name']}: BPJT partial-operation decree dated "
                    f"{long_date(decree)}; {fmt(operational)} km in operation of a "
                    f"{fmt(length)} km section."
                )
                event_type = "section_opened"
            else:
                description = (
                    f"{spec['name']}: BPJT operation decree dated "
                    f"{long_date(decree)}; {fmt(operational)} km in operation of a "
                    f"{fmt(length)} km section."
                )
                event_type = "opened"
            events.append(
                {
                    "id": event_id,
                    "project_id": spec["id"],
                    "event_date": decree,
                    "event_type": event_type,
                    "description": description,
                    "source_id": SOURCE,
                    "notes": "",
                }
            )
            event_ids.add(event_id)
            added_events += 1

        # Operator link
        org_id = BUJT_ORG.get(bujt) or NEW_BUJT[bujt]
        key = (spec["id"], org_id, "operator")
        if key not in link_keys:
            links.append(
                {
                    "project_id": spec["id"],
                    "org_id": org_id,
                    "role": "operator",
                    "share_pct": "",
                    "start_year": "",
                    "end_year": "",
                    "source_id": SOURCE,
                    "notes": "Concession operator named in the BPJT toll-road list.",
                }
            )
            link_keys.add(key)
            added_links += 1

        # Indonesian name
        key = ("project", spec["id"], "name", "id")
        if key not in translation_keys:
            translations.append(
                {
                    "entity_type": "project",
                    "entity_id": spec["id"],
                    "field": "name",
                    "locale": "id",
                    "text": spec["name_id"],
                    "status": "reviewed",
                    "translator": "atlas-editor",
                    "reviewed_on": REVIEWED,
                    "source_id": SOURCE,
                }
            )
            translation_keys.add(key)
            added_translations += 1

    # Kuala Tanjung correction -------------------------------------------
    for row in projects:
        if row["id"] != "tol-kuala-tanjung-tebing-tinggi-parapat":
            continue
        row["operational_km"] = "96.402"
        row["status_as_of"] = AS_OF
        row["verification"] = "official"
        row["last_verified"] = REVIEWED
        row["status_basis"] = (
            "BPJT toll-road list (6 Nov 2026): Operasi Sebagian, 96.402 of "
            "143.25 km operational; operation decree 2023."
        )
        row["notes"] = (
            "Coordinates are the midpoint of the BPJT start and end points, "
            "approximate. Indonesian Wikipedia reports 125.45 km operational and "
            "names PT Hutama Karya as operator; the BPJT list of 6 November 2026 "
            "reports 96.402 km and names PT Hutama Marga Waskita. The atlas "
            "publishes the BPJT values and keeps the Wikipedia figures in the "
            "conflict register."
        )

    for row in links:
        if (
            row["project_id"] == "tol-kuala-tanjung-tebing-tinggi-parapat"
            and row["role"] == "operator"
            and row["org_id"] == "org-hutama-karya"
        ):
            row["org_id"] = "org-hutama-marga-waskita"
            row["source_id"] = SOURCE
            row["notes"] = (
                "The BPJT list names PT Hutama Marga Waskita; Indonesian "
                "Wikipedia named PT Hutama Karya (conflict-kuala-tanjung-operator)."
            )

    for row in claims:
        if (
            row["project_id"] == "tol-kuala-tanjung-tebing-tinggi-parapat"
            and row["source_id"] == WIKI
            and row["claim"] == "operator"
        ):
            row["notes"] = (
                "Indonesian Wikipedia names PT Hutama Karya; the BPJT list names "
                "PT Hutama Marga Waskita. See conflict-kuala-tanjung-operator."
            )
    key = ("tol-kuala-tanjung-tebing-tinggi-parapat", SOURCE, "operator")
    if key not in claim_keys:
        claims.append(
            {
                "project_id": "tol-kuala-tanjung-tebing-tinggi-parapat",
                "source_id": SOURCE,
                "claim": "operator",
                "claim_value": "PT Hutama Marga Waskita",
                "claim_date": AS_OF,
                "notes": "",
            }
        )
        claim_keys.add(key)
        added_claims += 1
    key = ("tol-kuala-tanjung-tebing-tinggi-parapat", SOURCE, "operational")
    if key not in claim_keys:
        claims.append(
            {
                "project_id": "tol-kuala-tanjung-tebing-tinggi-parapat",
                "source_id": SOURCE,
                "claim": "operational",
                "claim_value": "96.402 km",
                "claim_date": AS_OF,
                "notes": "",
            }
        )
        claim_keys.add(key)
        added_claims += 1

    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)
    write_csv(CURATED / "project_events.csv", EVENT_FIELDS, events)
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, links)
    write_csv(CURATED / "translations.csv", TRANSLATION_FIELDS, translations)

    # Conflicts -----------------------------------------------------------
    conflicts = read_csv(CURATED / "conflicts.csv")
    existing = {row["id"] for row in conflicts}
    new_conflicts = [
        {
            "id": "conflict-kuala-tanjung-operator",
            "scope": "project",
            "subject": "Kuala Tanjung–Tebing Tinggi–Parapat operator",
            "project_id": "tol-kuala-tanjung-tebing-tinggi-parapat",
            "estate_id": "",
            "corridor_id": "",
            "field": "operator",
            "value_a": "PT Hutama Karya (Persero) (Indonesian Wikipedia)",
            "source_a": WIKI,
            "value_b": "PT Hutama Marga Waskita (BPJT toll-road list, 6 Nov 2026)",
            "source_b": SOURCE,
            "status": "resolved",
            "resolution": (
                "Atlas publishes PT Hutama Marga Waskita, the concession operator "
                "named in the official BPJT register, and keeps the Wikipedia "
                "operator in this note."
            ),
            "notes": (
                "The earlier row note said the section was absent from the BPJT "
                "API; it is listed there as Kuala Tanjung - Tebing Tinggi - Parapat."
            ),
        },
        {
            "id": "conflict-kuala-tanjung-operational",
            "scope": "project",
            "subject": "Kuala Tanjung–Tebing Tinggi–Parapat operational km",
            "project_id": "tol-kuala-tanjung-tebing-tinggi-parapat",
            "estate_id": "",
            "corridor_id": "",
            "field": "operational_km",
            "value_a": "125.45 km operational (Indonesian Wikipedia)",
            "source_a": WIKI,
            "value_b": "96.402 km operational (BPJT toll-road list, 6 Nov 2026)",
            "source_b": SOURCE,
            "status": "resolved",
            "resolution": (
                "Atlas publishes the BPJT figure, which is dated 6 November 2026 "
                "and comes from the official register, and keeps the Wikipedia "
                "figure here."
            ),
            "notes": "The two figures differ by 29 km and may reflect different dates.",
        },
        {
            "id": "conflict-bpjt-operational-above-length",
            "scope": "dataset",
            "subject": "BPJT operational km above section length",
            "project_id": "",
            "estate_id": "",
            "corridor_id": "",
            "field": "operational_km",
            "value_a": (
                count_word(len(op_over_length)).capitalize()
                + " sections report more operational km than their section "
                "length: " + ", ".join(op_over_length)
            ),
            "source_a": SOURCE,
            "value_b": "Operational km cannot exceed the section length",
            "source_b": SOURCE,
            "status": "open",
            "resolution": (
                "Atlas publishes the BPJT section length and keeps the reported "
                "operational figure in the claim, with a note on each row. The "
                "operational figure may include ramps or a different measurement."
            ),
            "notes": (
                "Affected rows: " + ", ".join(op_over_length) + "."
            ),
        },
    ]
    added_conflicts = 0
    for conflict in new_conflicts:
        if conflict["id"] in existing:
            continue
        conflicts.append(dict(conflict))
        existing.add(conflict["id"])
        added_conflicts += 1
    write_csv(CURATED / "conflicts.csv", CONFLICT_FIELDS, conflicts)

    print(
        f"Added {added_projects} projects, {added_orgs} organisations, "
        f"{added_links} role links, {added_claims} claims, {added_events} events, "
        f"{added_translations} translations and {added_conflicts} conflicts "
        "(idempotent)."
    )
    if zero_length:
        print("Zero-length sections using the operational length:",
              ", ".join(zero_length))


if __name__ == "__main__":
    main()
