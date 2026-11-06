"""Build data/projects.csv from curated toll-road rows plus BPJT data.

The curated list decides which projects are in scope and what status they have.
BPJT's toll-road-list API supplies official length, operator, operating km and
endpoint coordinates where a row exists.

Run: python scripts/build_projects.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "2026-11-06"
BPJT = RAW / "bpjt_toll_road_list.json"
OUT = ROOT / "data" / "projects.csv"

BPJT_URL = "https://itrams-api.bpjt.pu.go.id/v1/reference/api/toll-road-list"
ENWIKI_URL = "https://en.wikipedia.org/w/index.php?oldid=1329385293"
IDWIKI_URL = "https://id.wikipedia.org/w/index.php?oldid=30025554"

FIELDS = [
    "id",
    "name",
    "sector",
    "status",
    "status_basis",
    "province",
    "route",
    "length_km",
    "operator",
    "opened_year",
    "lat",
    "lon",
    "precision",
    "source_url",
    "source_type",
    "retrieved_on",
    "last_verified",
    "notes",
]

# Each entry is a curated decision. bpjt_name must match the API exactly.
PROJECTS = [
    {
        "id": "tol-sigli-banda-aceh",
        "name": "Sigli–Banda Aceh Toll Road",
        "status": "under_construction",
        "province": "Aceh",
        "route": "Banda Aceh–Sigli",
        "bpjt_name": "Sigli - Banda Aceh",
        "status_basis": "BPJT: Operasi Sebagian, 48.58 of 74.21 km operational, 24.67 km under construction; Section 6 Kuto Baro–Baitussalam (5 km) was complete in June 2025.",
        "notes": "English Wikipedia says 49.8 km operational of 74 km. BPJT gives no full-corridor opening date. Section 1 Padang Tiji–Seulimeum (24.67 km) was targeted for 2026.",
    },
    {
        "id": "tol-binjai-langsa",
        "name": "Binjai–Langsa Toll Road",
        "status": "under_construction",
        "province": "Aceh; North Sumatra",
        "route": "Binjai–Langsa",
        "bpjt_name": "Binjai - Langsa",
        "status_basis": "BPJT: Operasi, 57.23 of 130.9 km operational; remaining sections under construction. Section 3 Tanjung Pura–Pangkalan Brandan (18.9 km) opened 11 March 2025.",
        "notes": "BPJT status says Operasi although 73.7 km is not open; idwiki marks the corridor as partly open. Conflict recorded.",
    },
    {
        "id": "tol-padang-pekanbaru",
        "name": "Padang–Pekanbaru Toll Road",
        "status": "under_construction",
        "province": "West Sumatra; Riau",
        "route": "Padang–Pekanbaru",
        "bpjt_name": "Pekanbaru - Bangkinang - Payakumbuh - Bukit Tinggi - Padang Panjang - Lubuk Alung - Padang",
        "status_basis": "BPJT: Operasi Sebagian, 91.04 of 254.8 km operational, 9.11 km under construction. Padang–Sicincin (36 km) opened 28 May 2025.",
        "notes": "English Wikipedia says 38 km of 255 km operational (stale). The BPJT row covers the full Padang–Pekanbaru corridor via Bangkinang, Payakumbuh, Bukittinggi and Padang Panjang.",
    },
    {
        "id": "tol-bengkulu-lubuk-linggau",
        "name": "Bengkulu–Lubuk Linggau Toll Road",
        "status": "under_construction",
        "province": "Bengkulu; South Sumatra",
        "route": "Bengkulu–Lubuk Linggau",
        "bpjt_name": "Lubuk Linggau - Curup - Bengkulu",
        "status_basis": "BPJT: Operasi Sebagian, 16.73 of 95.8 km operational; no active construction km recorded.",
        "notes": "English Wikipedia says 18 km of 95 km operational. BPJT shows no active construction despite the partial status; verify before treating the remaining sections as active.",
    },
    {
        "id": "tol-kayu-agung-palembang-betung",
        "name": "Kayu Agung–Palembang–Betung Toll Road",
        "status": "under_construction",
        "province": "South Sumatra",
        "route": "Kayu Agung–Palembang–Betung",
        "bpjt_name": "Kayuagung - Palembang",
        "length_km": 111.7,
        "status_basis": "English Wikipedia: 42.5 of 111.7 km operational. BPJT lists only Kayuagung–Palembang (37.62 of 42.5 km operational); the Palembang–Betung link is covered by the Betung–Tempino–Jambi row.",
        "notes": "The corridor is split across two BPJT rows. Length and operating figures conflict. Palembang–Betung sections were targeted for 2026.",
    },
    {
        "id": "tol-kuala-tanjung-tebing-tinggi-parapat",
        "name": "Kuala Tanjung–Tebing Tinggi–Parapat Toll Road",
        "status": "under_construction",
        "province": "North Sumatra",
        "route": "Kuala Tanjung–Tebing Tinggi–Parapat",
        "lat": 3.01,
        "lon": 99.20,
        "operator": "PT Hutama Karya (Persero)",
        "length_km": 143.25,
        "source_url": IDWIKI_URL,
        "source_type": "secondary",
        "status_basis": "idwiki: 125.45 of 143.25 km operational; remaining sections under construction. Kuala Tanjung–Indrapura (10.15 km) opened in 2025.",
        "notes": "Not in the BPJT toll-road-list API. English Wikipedia omits this corridor. Source is Indonesian Wikipedia, so treat the status as secondary.",
    },
    {
        "id": "tol-betung-tempino-jambi",
        "name": "Betung–Tempino–Jambi Toll Road",
        "status": "under_construction",
        "province": "South Sumatra; Jambi",
        "route": "Betung–Tempino–Jambi",
        "bpjt_name": "Betung (Sp. Sekayu) - Tempino - Jambi",
        "status_basis": "BPJT: Operasi Sebagian, 52.59 of 170.73 km operational, 118.14 km under construction.",
        "notes": "Section 4 Tempino–Interchange Ness (18.49 km) was in ULFO in September 2025. Section 2 Tungkal Jaya–Bayung Lencir (54.3 km) was targeted for 2026.",
    },
    {
        "id": "tol-depok-antasari",
        "name": "Depok–Antasari Toll Road",
        "status": "under_construction",
        "province": "DKI Jakarta; West Java",
        "route": "Depok–Antasari",
        "bpjt_name": "Depok - Antasari",
        "status_basis": "BPJT: Operasi Sebagian, 12.1 of 27.94 km operational; no active construction km recorded.",
        "notes": "English Wikipedia says 15.7 of 23 km (stale). BPJT lists no active construction; the remaining section may be delayed. Verify.",
    },
    {
        "id": "tol-jakarta-inner-ring-road-2",
        "name": "Jakarta Inner Ring Road 2 (6 Inner City Toll Roads)",
        "status": "under_construction",
        "province": "DKI Jakarta",
        "route": "Jakarta inner ring, six sections",
        "bpjt_name": "6 Ruas Tol DKI (Semanan - Sunter dan Sunter - Pulogebang)",
        "length_km": 69.77,
        "status_basis": "BPJT: 6 Ruas Tol DKI, Operasi Sebagian, 9.287 of 29.67 km operational; no active construction km recorded.",
        "notes": "English Wikipedia gives 69.77 km for six inner-city toll roads. Only Sunter–Pulogebang is open; the other five sections have no construction recorded by BPJT. Status may be planned or stalled.",
    },
    {
        "id": "tol-bekasi-cawang-kampung-melayu",
        "name": "Bekasi–Cawang–Kampung Melayu Toll Road",
        "status": "under_construction",
        "province": "DKI Jakarta; West Java",
        "route": "Bekasi–Cawang–Kampung Melayu",
        "bpjt_name": "Bekasi - Cawang - Kampung Melayu",
        "status_basis": "BPJT: Operasi, 15.28 of 21.04 km operational; no active construction km recorded.",
        "notes": "English Wikipedia says 21.49 of 33.89 km; idwiki says 11.54 of 21.04 km. The three sources disagree on scope. BPJT status says Operasi despite the shortfall.",
    },
    {
        "id": "tol-jakarta-harbour-road-2",
        "name": "Jakarta Harbour Road 2 Toll Road",
        "status": "under_construction",
        "province": "DKI Jakarta",
        "route": "Tanjung Priok–Ancol Timur–Pluit",
        "bpjt_name": "Cawang - Tj. Priok - Ancol Timur - Jembatan Tiga/Pluit",
        "length_km": 9.6,
        "status_basis": "BPJT: Cawang–Tanjung Priok–Ancol Timur–Jembatan Tiga/Pluit, Operasi Sebagian, 27.05 of 36 km operational, 8.95 km under construction. BPJT (Sept 2026): Harbour Road II 47.41% complete, functional target Q1 2028.",
        "notes": "English Wikipedia lists 9.6 km under construction. The BPJT row covers a wider 36 km set of sections; 9.6 km is the Harbour Road II component.",
    },
    {
        "id": "tol-jakarta-cikampek-2-south",
        "name": "Jakarta–Cikampek II South Toll Road",
        "status": "under_construction",
        "province": "DKI Jakarta; West Java",
        "route": "Jakarta–Cikampek (southern route)",
        "lat": -6.40,
        "lon": 107.21,
        "operator": "PT Jasamarga Japek Selatan",
        "length_km": 62.0,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 62 km under construction. idwiki: 7.3 of 64 km operational.",
        "notes": "The BPJT toll-road-list API has no row for this project. 54.75 km was targeted for 2026. Coordinates are an approximate midpoint of the Setu–Sadang alignment.",
    },
    {
        "id": "tol-bogor-ring-road",
        "name": "Bogor Ring Road",
        "status": "under_construction",
        "province": "West Java",
        "route": "Bogor outer ring",
        "bpjt_name": "Bogor Ring Road",
        "lat": -6.58,
        "lon": 106.79,
        "status_basis": "BPJT: Operasi Sebagian, 11.3 of 11.95 km operational; no active construction km recorded.",
        "notes": "English Wikipedia says 8.5 of 13 km (stale). Only the BORR 3B section remains. BPJT endpoint coordinates for this row fall west of Bogor city, so the marker uses Bogor city centre.",
    },
    {
        "id": "tol-serang-panimbang",
        "name": "Serang–Panimbang Toll Road",
        "status": "under_construction",
        "province": "Banten",
        "route": "Serang–Panimbang",
        "bpjt_name": "Serang - Panimbang",
        "status_basis": "BPJT: Operasi Sebagian, 26.495 of 83.67 km operational, 57.17 km under construction.",
        "notes": "Section 1 Serang–Rangkasbitung (26.5 km) opened in 2021. Sections 2 and 3 were targeted for 2026.",
    },
    {
        "id": "tol-ciawi-sukabumi",
        "name": "Ciawi–Sukabumi Toll Road",
        "status": "under_construction",
        "province": "West Java",
        "route": "Ciawi–Sukabumi",
        "bpjt_name": "Ciawi - Sukabumi",
        "status_basis": "BPJT: Operasi Sebagian, 26.4 of 54 km operational, 13.7 km under construction.",
        "notes": "English Wikipedia says 27.3 of 53.6 km. Section 3 Cibadak–Cisaat (13.7 km) was targeted for 2026.",
    },
    {
        "id": "tol-semarang-demak",
        "name": "Semarang–Demak Toll Road",
        "status": "under_construction",
        "province": "Central Java",
        "route": "Semarang–Demak",
        "bpjt_name": "Semarang - Demak",
        "status_basis": "BPJT: Operasi Sebagian, 16.01 of 27 km operational, 10.64 km under construction.",
        "notes": "English Wikipedia says 16.01 of 24.74 km. Section 1A/1C (3.66 km) was targeted for 2026.",
    },
    {
        "id": "tol-solo-yogyakarta-nyia",
        "name": "Solo–Yogyakarta–NYIA Kulon Progo Toll Road",
        "status": "under_construction",
        "province": "DI Yogyakarta; Central Java",
        "route": "Solo–Yogyakarta–YIA Kulon Progo",
        "bpjt_name": "Solo - Yogyakarta - NYIA Kulonprogo",
        "status_basis": "BPJT: Operasi Sebagian, 30.15 of 96.57 km operational, 19.11 km under construction. Klaten–Prambanan (7.85 km) opened 2 July 2025; Kartasura–Klaten (22.3 km) opened September 2024.",
        "notes": "English Wikipedia splits the corridor into Yogyakarta–Solo (58.01 km, under construction) and Yogyakarta–Sleman–YIA (35.74 km, in preparation). BPJT treats it as one 96.57 km corridor.",
    },
    {
        "id": "tol-yogyakarta-bawen",
        "name": "Yogyakarta–Bawen Toll Road",
        "status": "under_construction",
        "province": "DI Yogyakarta; Central Java",
        "route": "Yogyakarta–Bawen",
        "lat": -7.52,
        "lon": 110.39,
        "operator": "PT Jasa Marga Jogja Bawen",
        "length_km": 75.82,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 75.82 km under construction. Seksi 6 Ambarawa–Bawen (4.98 km) targeted November 2026; Seksi 1 Sleman–Banyurejo near completion.",
        "notes": "idwiki lists 0 km operational. The BPJT toll-road-list API has no row. Coordinates are an approximate midpoint of the alignment.",
    },
    {
        "id": "tol-krian-legundi-bunder-manyar",
        "name": "Krian–Legundi–Bunder–Manyar Toll Road",
        "status": "under_construction",
        "province": "East Java",
        "route": "Krian–Legundi–Bunder–Manyar",
        "bpjt_name": "Krian - Legundi - Bunder - Manyar",
        "status_basis": "BPJT: Operasi, 29 of 38.29 km operational, 9.29 km under construction.",
        "notes": "BPJT status says Operasi despite 9.29 km under construction. English Wikipedia says 29 of 38 km.",
    },
    {
        "id": "tol-probolinggo-banyuwangi",
        "name": "Probolinggo–Banyuwangi Toll Road",
        "status": "under_construction",
        "province": "East Java",
        "route": "Probolinggo–Banyuwangi",
        "bpjt_name": "Probolinggo - Banyuwangi",
        "status_basis": "BPJT: Operasi Sebagian, 23.515 of 172.9 km operational, 25.6 km under construction. Sections 1–2 Gending–Paiton (24 km) were complete in 2026 and awaiting ULFO.",
        "notes": "English Wikipedia says 176.4 km. idwiki says 173 km and 23.515 km operational.",
    },
    {
        "id": "tol-jorr-3",
        "name": "Jakarta Outer Ring Road 3",
        "status": "planned",
        "province": "DKI Jakarta; Banten; West Java",
        "route": "Jakarta outer ring 3",
        "lat": -6.25,
        "lon": 106.65,
        "operator": "Various (see notes)",
        "length_km": 283.71,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: italic, 283.71 km estimated, no operational sections.",
        "notes": "Master-plan ring road with sections at different stages. Kamal–Teluknaga–Rajeg (4.7 of 38.6 km open) and Serpong–Balaraja (9.3 of 30 km open) are under construction; others are planned. BPJT API has no JORR 3 row.",
    },
    {
        "id": "tol-gedebage-tasikmalaya-cilacap",
        "name": "Gedebage–Tasikmalaya–Cilacap Toll Road",
        "status": "planned",
        "province": "West Java; Central Java",
        "route": "Gedebage–Tasikmalaya–Cilacap",
        "lat": -7.34,
        "lon": 108.35,
        "operator": "tba",
        "length_km": 206.65,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 206.65 km in preparation.",
        "notes": "idwiki: 206.65 km, 0 operational. Not in the BPJT toll-road-list API. Also called Getaci. A 2026 report says it is still at the potential/tender stage.",
    },
    {
        "id": "tol-demak-tuban",
        "name": "Demak–Tuban Toll Road",
        "status": "planned",
        "province": "Central Java; East Java",
        "route": "Demak–Tuban",
        "lat": -6.90,
        "lon": 111.35,
        "operator": "PT HM Sampoerna (idwiki); tba (enwiki)",
        "length_km": 176.99,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 176.99 km in preparation.",
        "notes": "idwiki: 171.93 km, 0 operational. Not in the BPJT toll-road-list API. Operators conflict between the two Wikipedia articles.",
    },
    {
        "id": "tol-semarang-kendal",
        "name": "Harbour Toll Road Semarang (Semarang–Kendal)",
        "status": "planned",
        "province": "Central Java",
        "route": "Semarang–Kendal",
        "lat": -6.95,
        "lon": 110.31,
        "operator": "tba",
        "length_km": 20.86,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 20.86 km in preparation.",
        "notes": "Not in the BPJT toll-road-list API.",
    },
    {
        "id": "tol-pejagan-tegal-cilacap",
        "name": "Pejagan/Tegal–Cilacap Toll Road",
        "status": "planned",
        "province": "Central Java",
        "route": "Pejagan/Tegal–Cilacap",
        "lat": -7.30,
        "lon": 109.08,
        "operator": "tba",
        "length_km": 141.0,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 141 km in preparation.",
        "notes": "Not in the BPJT toll-road-list API.",
    },
    {
        "id": "tol-cilacap-yogyakarta",
        "name": "Cilacap–Yogyakarta Toll Road",
        "status": "planned",
        "province": "Central Java; DI Yogyakarta",
        "route": "Cilacap–Yogyakarta",
        "lat": -7.77,
        "lon": 109.69,
        "operator": "PT Putera Jaya Sakti Perkasa (idwiki); tba (enwiki)",
        "length_km": 167.07,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 167.07 km in preparation.",
        "notes": "idwiki: 121.75 km, 0 operational. Not in the BPJT toll-road-list API. Length and operator conflict between the two Wikipedia articles.",
    },
    {
        "id": "tol-gilimanuk-mengwi",
        "name": "Gilimanuk–Mengwi Toll Road",
        "status": "planned",
        "province": "Bali",
        "route": "Gilimanuk–Mengwi",
        "lat": -8.30,
        "lon": 114.81,
        "operator": "Tol Jagat Kerthi Bali (idwiki); tba (enwiki)",
        "length_km": 96.84,
        "source_url": ENWIKI_URL,
        "source_type": "secondary",
        "status_basis": "English Wikipedia: 96.84 km in preparation.",
        "notes": "idwiki: 95.51 km, 0 operational. Not in the BPJT toll-road-list API. Also called Tol Bali Barat.",
    },
]


def num(value: object, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def main() -> None:
    records = {row["ruas_name"]: row for row in json.loads(BPJT.read_text(encoding="utf-8-sig"))["data"]}
    out_rows: list[dict[str, object]] = []

    for project in PROJECTS:
        row = dict(project)
        bpjt_name = row.pop("bpjt_name", None)

        if bpjt_name:
            if bpjt_name not in records:
                raise SystemExit(f"BPJT row not found: {bpjt_name}")
            source = records[bpjt_name]
            lat = (float(source["start_latitude"]) + float(source["end_latitude"])) / 2
            lon = (float(source["start_longitude"]) + float(source["end_longitude"])) / 2
            row.setdefault("lat", round(lat, 5))
            row.setdefault("lon", round(lon, 5))
            row.setdefault("length_km", num(source["length"]))
            row.setdefault("operator", (source["bujt_name"] or "").strip())
            row.setdefault("source_url", BPJT_URL)
            row.setdefault("source_type", "official")

        row.setdefault("sector", "road")
        row.setdefault("opened_year", "")
        row.setdefault("precision", "approximate")
        row.setdefault("retrieved_on", "2026-11-06")
        row.setdefault("last_verified", "2026-11-06")

        optional_empty = {"opened_year"}
        missing = [
            f
            for f in FIELDS
            if f not in row or (row[f] in (None, "") and f not in optional_empty)
        ]
        if missing:
            raise SystemExit(f"{row.get('id')}: missing {missing}")

        out_rows.append({f: row[f] for f in FIELDS})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out_rows)

    by_status: dict[str, int] = {}
    for row in out_rows:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
    print(f"wrote {len(out_rows)} rows to {OUT.relative_to(ROOT)}")
    print("status counts:", by_status)


if __name__ == "__main__":
    main()
