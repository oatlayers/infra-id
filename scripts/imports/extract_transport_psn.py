"""Extract the 35 transport PSN rows from the Kemenhub review into staging.

The source is the Kemenhub deck "Capaian Progres Proyek Strategis Nasional
(PSN) Sektor Transportasi", Jakarta, 19 February 2026. The deck is a PDF; this
script encodes a checked manual transcription rather than re-parsing the PDF.
Every row carries a page reference so the claim can be traced back.

Status mapping follows the atlas definitions, not the deck's summary counts:

* operating: complete and in service.
* under_construction: material construction active, even if part of the asset
  is already open.
* recently_completed: fully open on or after 2024-11-06.
* planned: designated or contracted, but no physical construction.

The deck's summary says 29 complete and 6 under construction. The deck's own
project pages show that Patimban, the Java south double track, Rantau Prapat and
Lahat still have active work, while Kaltim, MRT East-West, New Palembang and
Muaro Jambi had no physical work. Those conflicts are recorded in `notes`.

Run: python scripts/imports/extract_transport_psn.py
Writes: data/derived/transport_psn.csv
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "derived" / "transport_psn.csv"

FIELDS = [
    "id", "name", "sector", "subsector", "status", "province", "island",
    "route", "lat", "lon", "opened_year", "expected_open_year", "progress_pct",
    "investment_idr_t", "operator_org_id", "page_ref", "status_basis", "notes",
    "aliases",
]

SOURCE = "Kemenhub PSN review (19 Feb 2026)"


def row(
    id: str,
    name: str,
    sector: str,
    subsector: str,
    status: str,
    province: str,
    island: str,
    route: str,
    lat: float,
    lon: float,
    page_ref: str,
    status_basis: str,
    notes: str,
    aliases: str,
    *,
    opened_year: str = "",
    expected_open_year: str = "",
    progress_pct: str = "",
    investment_idr_t: str = "",
    operator_org_id: str = "",
) -> dict[str, str]:
    return {
        "id": id,
        "name": name,
        "sector": sector,
        "subsector": subsector,
        "status": status,
        "province": province,
        "island": island,
        "route": route,
        "lat": f"{lat:.5f}",
        "lon": f"{lon:.5f}",
        "opened_year": opened_year,
        "expected_open_year": expected_open_year,
        "progress_pct": progress_pct,
        "investment_idr_t": investment_idr_t,
        "operator_org_id": operator_org_id,
        "page_ref": page_ref,
        "status_basis": status_basis,
        "notes": notes,
        "aliases": aliases,
    }


ROWS = [
    # ------------------------------------------------------------------
    # Airports (7). All were inaugurated between 2020 and 2023.
    # ------------------------------------------------------------------
    row(
        "air-yogyakarta-international",
        "Yogyakarta International Airport (YIA)",
        "airport", "international airport", "operating",
        "DI Yogyakarta", "Java", "Kulon Progo, DI Yogyakarta",
        -7.9006, 110.0575, "p.7",
        f"{SOURCE}: inaugurated in 2020 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are the airport reference point, approximate. No capacity figure is stated in the PSN review.",
        "YIA;Bandar Udara Internasional Yogyakarta",
        opened_year="2020", operator_org_id="org-angakasa-pura-i",
    ),
    row(
        "air-komodo-labuan-bajo",
        "Komodo Airport – Labuan Bajo",
        "airport", "international airport", "operating",
        "East Nusa Tenggara", "Bali-Nusa Tenggara", "Manggarai, East Nusa Tenggara",
        -8.4867, 119.8892, "p.7",
        f"{SOURCE}: inaugurated in 2022 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are the airport reference point, approximate. No capacity figure is stated in the PSN review.",
        "LBJ;Bandar Udara Komodo",
        opened_year="2022", operator_org_id="org-angakasa-pura-i",
    ),
    row(
        "air-lombok-praya",
        "Lombok Praya Airport",
        "airport", "international airport", "operating",
        "West Nusa Tenggara", "Bali-Nusa Tenggara", "Lombok Tengah, West Nusa Tenggara",
        -8.7573, 116.2767, "p.7",
        f"{SOURCE}: inaugurated in 2020 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are the airport reference point, approximate. No capacity figure is stated in the PSN review.",
        "LOP;Bandar Udara Lombok",
        opened_year="2020", operator_org_id="org-angakasa-pura-i",
    ),
    row(
        "air-nabire",
        "Nabire New Airport",
        "airport", "domestic airport", "operating",
        "Central Papua", "Papua", "Nabire, Central Papua",
        -3.3682, 135.4967, "p.7",
        f"{SOURCE}: inaugurated in 2022 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are the airport reference point, approximate. No capacity figure is stated in the PSN review.",
        "Nabire Baru;Bandar Udara Nabire",
        opened_year="2022", operator_org_id="org-angakasa-pura-i",
    ),
    row(
        "air-siboru-fakfak",
        "Siboru Fakfak Airport",
        "airport", "domestic airport", "operating",
        "West Papua", "Papua", "Fakfak, West Papua",
        -2.9220, 132.2670, "p.7",
        f"{SOURCE}: inaugurated in 2023 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are the airport reference point, approximate. No capacity figure is stated in the PSN review.",
        "Siboru;Bandar Udara Siboru Fakfak",
        opened_year="2023", operator_org_id="org-angakasa-pura-i",
    ),
    row(
        "air-kediri",
        "Kediri Airport (Dhoho)",
        "airport", "domestic airport", "operating",
        "East Java", "Java", "Kediri, East Java",
        -7.7486, 111.9479, "p.7",
        f"{SOURCE}: inaugurated in 2023 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are the airport reference point, approximate. No capacity figure is stated in the PSN review.",
        "Dhoho;Bandar Udara Kediri",
        opened_year="2023", operator_org_id="org-angakasa-pura-i",
    ),
    row(
        "air-raja-haji-abdullah-karimun",
        "Raja Haji Abdullah Airport – Karimun",
        "airport", "domestic airport", "operating",
        "Riau Islands", "Sumatra", "Karimun, Riau Islands",
        0.9167, 103.3833, "p.7",
        f"{SOURCE}: inaugurated in 2023 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are the airport reference point, approximate. No capacity figure is stated in the PSN review.",
        "Karimun;Bandar Udara Raja Haji Abdullah",
        opened_year="2023", operator_org_id="org-angakasa-pura-ii",
    ),

    # ------------------------------------------------------------------
    # Seaports (15). Eleven operating, Patimban under construction, Benoa
    # expansion recently completed, two planned.
    # ------------------------------------------------------------------
    row(
        "port-kek-maloy",
        "KEK Maloy Port",
        "seaport", "multipurpose port", "operating",
        "East Kalimantan", "Kalimantan", "Kutai Timur, East Kalimantan",
        0.5833, 117.5000, "p.7",
        f"{SOURCE}: inaugurated in 2020 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Serves the Maloy Batuta Trans Kalimantan SEZ. Coordinates are approximate.",
        "Pelabuhan Maloy;Maloy Batuta Port",
        opened_year="2020", operator_org_id="org-pelindo",
    ),
    row(
        "port-labuan-bajo-multipurpose",
        "Labuan Bajo Multipurpose Terminal",
        "seaport", "multipurpose port", "operating",
        "East Nusa Tenggara", "Bali-Nusa Tenggara", "Manggarai Barat, East Nusa Tenggara",
        -8.4960, 119.8870, "p.7",
        f"{SOURCE}: inaugurated in 2021 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are approximate.",
        "Terminal Multipurpose Labuan Bajo;Pelabuhan Labuan Bajo",
        opened_year="2021", operator_org_id="org-pelindo",
    ),
    row(
        "port-bitung",
        "Bitung International Hub Port",
        "seaport", "hub port", "operating",
        "North Sulawesi", "Sulawesi", "Bitung, North Sulawesi",
        1.4400, 125.1230, "p.7",
        f"{SOURCE}: inaugurated in 2018 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Supporting hub works continue after the inauguration. Coordinates are approximate.",
        "Pelabuhan Bitung;Bitung Hub Port",
        opened_year="2018", operator_org_id="org-pelindo",
    ),
    row(
        "port-kupang",
        "Kupang Port",
        "seaport", "multipurpose port", "operating",
        "East Nusa Tenggara", "Bali-Nusa Tenggara", "Kupang, East Nusa Tenggara",
        -10.1833, 123.5667, "p.7",
        f"{SOURCE}: inaugurated in 2018 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Tenau–Kupang port. Inauguration year per Kemenhub. Coordinates are approximate.",
        "Pelabuhan Kupang;Tenau Kupang",
        opened_year="2018", operator_org_id="org-pelindo",
    ),
    row(
        "port-kuala-tanjung",
        "Kuala Tanjung International Hub Port",
        "seaport", "hub port", "operating",
        "North Sumatra", "Sumatra", "Batu Bara, North Sumatra",
        3.3500, 99.4500, "p.7",
        f"{SOURCE}: inaugurated in 2018 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are approximate.",
        "Pelabuhan Kuala Tanjung;Kuala Tanjung Hub",
        opened_year="2018", operator_org_id="org-pelindo",
    ),
    row(
        "port-kijing",
        "Kijing Terminal",
        "seaport", "multipurpose port", "operating",
        "West Kalimantan", "Kalimantan", "Mempawah, West Kalimantan",
        0.2833, 108.9500, "p.7",
        f"{SOURCE}: inaugurated in 2022 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are approximate.",
        "Terminal Kijing;Pelabuhan Kijing",
        opened_year="2022", operator_org_id="org-pelindo",
    ),
    row(
        "port-sanur",
        "Sanur Port",
        "seaport", "ferry port", "operating",
        "Bali", "Bali-Nusa Tenggara", "Denpasar, Bali",
        -8.7000, 115.2670, "p.7",
        f"{SOURCE}: inaugurated in 2022 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Sanur–Nusa Ceningan crossing. Inauguration year per Kemenhub. Coordinates are approximate.",
        "Pelabuhan Sanur;Sanur–Nusa Ceningan",
        opened_year="2022", operator_org_id="org-pelindo",
    ),
    row(
        "port-likupang",
        "Likupang Port",
        "seaport", "ferry port", "operating",
        "North Sulawesi", "Sulawesi", "Minahasa Utara, North Sulawesi",
        1.6670, 125.0670, "p.7",
        f"{SOURCE}: inaugurated in 2022 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are approximate.",
        "Pelabuhan Likupang",
        opened_year="2022", operator_org_id="org-pelindo",
    ),
    row(
        "port-makassar-new-port",
        "Makassar New Port",
        "seaport", "container port", "operating",
        "South Sulawesi", "Sulawesi", "Makassar, South Sulawesi",
        -5.1000, 119.3830, "p.7",
        f"{SOURCE}: inaugurated in 2023 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are approximate.",
        "Makassar New Port;MNP",
        opened_year="2023", operator_org_id="org-pelindo",
    ),
    row(
        "port-teluk-palu",
        "Teluk Palu Port",
        "seaport", "multipurpose port", "operating",
        "Central Sulawesi", "Sulawesi", "Palu, Central Sulawesi",
        -0.8830, 119.7330, "p.7",
        f"{SOURCE}: inaugurated in 2023 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are approximate.",
        "Pelabuhan Teluk Palu;Pelabuhan Palu",
        opened_year="2023", operator_org_id="org-pelindo",
    ),
    row(
        "port-sorong",
        "Sorong Port",
        "seaport", "multipurpose port", "operating",
        "Southwest Papua", "Papua", "Sorong, Southwest Papua",
        -0.8830, 131.2670, "p.7",
        f"{SOURCE}: inaugurated in 2023 and operating; one of 18 completed projects proposed for removal from the PSN list.",
        "Inauguration year per Kemenhub. Coordinates are approximate.",
        "Pelabuhan Sorong",
        opened_year="2023", operator_org_id="org-pelindo",
    ),
    row(
        "port-patimban",
        "Patimban Port",
        "seaport", "container port", "under_construction",
        "West Java", "Java", "Subang, West Java",
        -6.2330, 107.8670, "p.11",
        f"{SOURCE}: Phase I complete and operating; Phase I-2 packages 5 and 6 at 95.48% and 93.02% in late 2025; project still under construction.",
        "The summary lists Patimban among 29 completed projects, but the project page reports Phase I-2 still under construction. Two JICA loans: Rp 8.979T (IP-577) and Rp 9.210T (IP-577 and IP-588); total 18.189T. Phase I opened in 2021; the full project is not complete. Coordinates approximate.",
        "Pelabuhan Patimban;Patimban",
        investment_idr_t="18.189", operator_org_id="org-pelindo",
    ),
    row(
        "port-benoa",
        "Benoa Port (BMTH)",
        "seaport", "multipurpose port", "recently_completed",
        "Bali", "Bali-Nusa Tenggara", "Denpasar, Bali",
        -8.7500, 115.2170, "p.10",
        f"{SOURCE}: all listed BMTH development works reported 100% in 2025, including the cruise terminal, international passenger terminal expansion, revetments and dredging.",
        "The status refers to the BMTH expansion completed in 2025, not the original port, which has operated for decades. Coordinates are approximate.",
        "Pelabuhan Benoa;BMTH",
        opened_year="2025", progress_pct="100", investment_idr_t="6.06",
        operator_org_id="org-pelindo",
    ),
    row(
        "port-palembang-baru",
        "New Palembang Port",
        "seaport", "multipurpose port", "planned",
        "South Sumatra", "Sumatra", "Banyuasin, South Sumatra",
        -2.3830, 104.9000, "p.13",
        f"{SOURCE}: no physical construction; 599,500 m2 of land was granted by the South Sumatra government on 31 October 2025.",
        "The deck's 2025 target has already passed and no physical work had started at the review date. Location is the Tanjung Carat/Sungsang area; coordinates approximate.",
        "Pelabuhan Palembang Baru;New Palembang Port",
        expected_open_year="2025", investment_idr_t="1.450",
    ),
    row(
        "port-muaro-jambi",
        "Muaro Jambi Container Terminal",
        "seaport", "container port", "planned",
        "Jambi", "Sumatra", "Muaro Jambi, Jambi",
        -1.5000, 103.6170, "p.13",
        f"{SOURCE}: construction contract signed on 17 December 2025; no physical construction at the review date.",
        "Contract awarded to PT Nusa Konstruksi Enjiniring for the WSI terminal. Coordinates are approximate.",
        "Terminal Peti Kemas Muaro Jambi;Muaro Jambi Container Terminal",
        expected_open_year="2028", investment_idr_t="3.948",
    ),

    # ------------------------------------------------------------------
    # Railways (13). Six operating, five under construction, two planned.
    # ------------------------------------------------------------------
    row(
        "rail-lrt-sumsel",
        "LRT South Sumatra",
        "railway", "urban rail", "operating",
        "South Sumatra", "Sumatra", "Palembang, South Sumatra",
        -2.9830, 104.7500, "p.8",
        f"{SOURCE}: construction 100% and operating since 2018; asset regularisation at the depot remains open.",
        "Length is not stated in the PSN review. Coordinates are approximate. The depot land certificate is still being resolved.",
        "LRT Palembang;Light Rail Transit Sumatera Selatan",
        opened_year="2018", investment_idr_t="12.13",
        operator_org_id="org-lrt-sumsel",
    ),
    row(
        "rail-double-track-java-south",
        "Double Track Java South",
        "railway", "intercity rail", "under_construction",
        "West Java; Central Java; DI Yogyakarta; East Java", "Java",
        "Cirebon–Sepanjang–Wonokromo, Java",
        -6.7170, 108.5670, "p.8",
        f"{SOURCE}: the summary reports 100% but describes the work as partly complete; the Sepanjang–Wonokromo continuation is still in technical planning and land acquisition.",
        "The deck repeats 'Rp 86 T private investment, excluding cost overrun' from the KCJB row; treated as a copy error and not used. No single length is stated because the programme covers multiple segments. Coordinates mark Cirebon, approximate.",
        "Double-Double Track Java;Jalur Ganda Jawa Selatan",
        operator_org_id="org-kai",
    ),
    row(
        "rail-tebing-tinggi-kuala-tanjung",
        "Tebing Tinggi–Kuala Tanjung Railway",
        "railway", "freight rail", "operating",
        "North Sumatra", "Sumatra", "Tebing Tinggi–Kuala Tanjung, North Sumatra",
        3.3400, 99.3000, "p.8",
        f"{SOURCE}: construction 100% in 2020 and operating since 2022; utility and land completion works continue.",
        "Length is not stated in the PSN review. Coordinates are the midpoint, approximate.",
        "KA Tebing Tinggi–Kuala Tanjung",
        opened_year="2022", investment_idr_t="0.874",
        operator_org_id="org-kai",
    ),
    row(
        "rail-yogyakarta-airport",
        "Yogyakarta Airport Rail Link",
        "railway", "airport rail", "operating",
        "DI Yogyakarta", "Java", "Yogyakarta–Yogyakarta International Airport",
        -7.8000, 110.3700, "p.8",
        f"{SOURCE}: construction 100% in 2021 and commercial operation since September 2021.",
        "Investment: APBN Rp 6T plus KPBU Rp 1T. Length is not stated in the PSN review. Coordinates are approximate.",
        "KA Bandara YIA;Yogyakarta International Airport Rail Link",
        opened_year="2021", investment_idr_t="7",
        operator_org_id="org-kai",
    ),
    row(
        "rail-makassar-parepare",
        "Makassar–Parepare Railway",
        "railway", "intercity rail", "operating",
        "South Sulawesi", "Sulawesi", "Makassar–Parepare, South Sulawesi",
        -4.5800, 119.5300, "p.9",
        f"{SOURCE}: construction 100% and operating since 2023; the Mandai–Palanro section is reported at 95.91%.",
        "Conflict: the summary calls the project complete, but the project page reports Mandai–Palanro at 95.91% with the Tonasa overpass land issue continuing in 2025. Investment: APBN Rp 6T plus KPBU Rp 1T. Length is not stated in the PSN review. Coordinates approximate.",
        "KA Trans Sulawesi;Makassar–Parepare",
        opened_year="2023", investment_idr_t="7",
        operator_org_id="org-kai",
    ),
    row(
        "rail-lrt-jabodebek",
        "Jabodebek LRT",
        "railway", "urban rail", "operating",
        "DKI Jakarta; West Java", "Java", "Jakarta–Bogor–Depok–Bekasi",
        -6.3500, 106.8700, "p.9",
        f"{SOURCE}: construction 100% and operating since 2023.",
        "Investment figure is BUMN investment for stage I. Length is not stated in the PSN review. Coordinates are approximate.",
        "LRT Jabodetabek;LRT Jabodebek",
        opened_year="2023", investment_idr_t="29.9",
        operator_org_id="org-kai",
    ),
    row(
        "rail-kcj-jakarta-bandung",
        "Jakarta–Bandung High-Speed Rail",
        "railway", "high-speed rail", "operating",
        "DKI Jakarta; West Java", "Java", "Jakarta–Bandung",
        -6.5500, 107.6500, "p.9",
        f"{SOURCE}: construction 100% and operating since 2023.",
        "Deck figure Rp 86T excludes cost overrun. Also known as Whoosh. Length is not stated in the PSN review. Coordinates are approximate.",
        "KCJB;Whoosh;Kereta Cepat Jakarta–Bandung",
        opened_year="2023", investment_idr_t="86",
        operator_org_id="org-kcic",
    ),
    row(
        "rail-rantau-prapat-kota-pinang",
        "Rantau Prapat–Kota Pinang Railway",
        "railway", "freight rail", "under_construction",
        "North Sumatra", "Sumatra", "Rantau Prapat–Kota Pinang, North Sumatra",
        2.0000, 99.9400, "p.9",
        f"{SOURCE}: construction reached Pondok S5 in 2024; the Pondok S5–Kota Pinang section remains, with 93.3% of land acquired.",
        "The summary lists the project among 29 completed, but the project page says the line stops at Pondok S5 and 52 land parcels are still unresolved. The deck repeats the KCJB Rp 86T investment line; treated as a copy error and not used. Length is not stated. Coordinates are approximate.",
        "KA Rantau Prapat–Kota Pinang",
        operator_org_id="org-kai",
    ),
    row(
        "rail-lahat-kertapati",
        "Lahat–Kertapati Logistics Railway",
        "railway", "freight rail", "under_construction",
        "South Sumatra", "Sumatra", "Lahat–Kertapati, South Sumatra",
        -3.3800, 104.1400, "p.9",
        f"{SOURCE}: the double track is complete and operating; the Coal Terminal Unloading System is 33.65% complete and was targeted for end-2025.",
        "The summary lists the project among 29 completed, but the coal terminal is still under construction. Length is not stated in the PSN review. Coordinates are the midpoint, approximate.",
        "KA Logistik Lahat–Kertapati;Lahat–Kertapati",
        investment_idr_t="11.52",
        operator_org_id="org-kai",
    ),
    row(
        "rail-kaltim-logistics",
        "East Kalimantan Logistics Railway",
        "railway", "freight rail", "planned",
        "East Kalimantan", "Kalimantan", "Balikpapan, East Kalimantan",
        -1.2700, 116.8300, "p.5-6",
        f"{SOURCE}: no physical construction; PT Bayan Laju Trans Kalimantan is still preparing the feasibility study and planning documents.",
        "Conflict: page 5 gives a 2028 target, page 6 gives 2027. The deck says investment is not yet stated. Coordinates mark Balikpapan, approximate.",
        "KA Logistik Kalimantan Timur;Bayan Rail",
        expected_open_year="2028",
        operator_org_id="org-bayan-laju-trans-kalimantan",
    ),
    row(
        "rail-mrt-jakarta-north-south",
        "MRT Jakarta North–South",
        "railway", "urban rail", "under_construction",
        "DKI Jakarta", "Java", "Lebak Bulus–Kota, Jakarta",
        -6.2000, 106.8200, "p.12",
        f"{SOURCE}: 48.14% overall; Phase 2A at 55.89% (Segment 1 77.03%, Segment 2 45.73%); commercial operation targeted for March 2028 and full operation for 2030.",
        "Length is not stated in the PSN review. Coordinates are approximate.",
        "MRT Jakarta;MRT North–South",
        expected_open_year="2030", progress_pct="48.14",
        investment_idr_t="11.48", operator_org_id="org-mrt-jakarta",
    ),
    row(
        "rail-mrt-jakarta-east-west",
        "MRT Jakarta East–West",
        "railway", "urban rail", "planned",
        "DKI Jakarta", "Java", "Jakarta East–West",
        -6.2000, 106.8000, "p.12",
        f"{SOURCE}: no physical construction; DPPT verification and re-baseline are ongoing, with land acquisition and contractor procurement still ahead.",
        "Length is not stated in the PSN review. Coordinates are approximate.",
        "MRT East–West;MRT Timur–Barat",
        expected_open_year="2032", investment_idr_t="34",
        operator_org_id="org-mrt-jakarta",
    ),
    row(
        "rail-lrt-jakarta-velodrome-manggarai",
        "LRT Jakarta Velodrome–Manggarai",
        "railway", "urban rail", "under_construction",
        "DKI Jakarta", "Java", "Velodrome–Manggarai, Jakarta",
        -6.2000, 106.8700, "p.12",
        f"{SOURCE}: 89.22% physical progress; track trials with the maintenance rail vehicle completed; target 2026.",
        "Groundbreaking 30 October 2023. Length is not stated in the PSN review. Coordinates are approximate.",
        "LRT Jakarta Fase 1B;LRT Velodrome–Manggarai",
        expected_open_year="2026", progress_pct="89.22",
        investment_idr_t="7", operator_org_id="org-lrt-jakarta",
    ),
]


def main() -> None:
    ids = [item["id"] for item in ROWS]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate staging id")
    counts = {sector: sum(1 for item in ROWS if item["sector"] == sector)
              for sector in ("railway", "airport", "seaport")}
    if counts != {"railway": 13, "airport": 7, "seaport": 15}:
        raise SystemExit(f"unexpected sector counts: {counts}")
    if len(ROWS) != 35:
        raise SystemExit(f"expected 35 rows, got {len(ROWS)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ROWS)

    statuses = {}
    for item in ROWS:
        statuses[item["status"]] = statuses.get(item["status"], 0) + 1
    print(f"wrote {len(ROWS)} rows to {OUT.relative_to(ROOT)}")
    print("sectors:", counts)
    print("statuses:", statuses)


if __name__ == "__main__":
    main()
