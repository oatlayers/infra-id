"""Add the 37 strategic electricity projects inaugurated on 20 January 2025.

Sources archived in ``data/raw/2026-11-13/``:

* ESDM, 20 January 2025, press release 005.Pers/04/SJI/2025. Lists the 26
  generating plants and the 11 transmission and substation projects, and gives
  the bundle totals: 3,222.75 MW, 739.71 kms and 1,740 MVA.
* ESDM, 20 January 2025, detail release. Gives the Jatigede, Asahan III and
  PLTS IKN capacity, household, CO2, worker, storage and output figures.
* GNFI, 26 January 2025. Groups the 26 plants by island: Sumatra 7 (259 MW),
  Kalimantan 3, Java 9 and Sulawesi 7.
* Listrik Indonesia, 23 January 2025. Gives the five Sumenep plant capacities,
  the Tanamalala capacity and benefits, and the 40 MW PLTMG Luwuk.

No capacity is invented. The archived releases state per-project capacity only
for Jatigede, Asahan III, PLTS IKN, the five Sumenep plants and Tanamalala, so
the other project rows leave ``capacity`` blank. The ESDM project list names
the IKN entry "PLTS IKN 10 MW" while the same ministry's detail release gives
50 MWac / 72 MWp; the list entry appears to be phase 1. The row records the
detail-release capacity and documents the discrepancy in ``notes``.

The script is idempotent: existing ids are never replaced and existing claims,
aliases, translations, links and values are never duplicated.

Run: python scripts/imports/add_37_electricity_projects.py
Then: python scripts/pipeline/validate.py
      python scripts/build_all.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    ALIAS_FIELDS,
    COVERAGE_FIELDS,
    CURATED,
    INDICATOR_FIELDS,
    INDICATOR_VALUE_FIELDS,
    PROGRAMME_PROJECT_FIELDS,
    PROGRAMME_SOURCE_FIELDS,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    SOURCE_FIELDS,
    TRANSLATION_FIELDS,
    read_csv,
    write_csv,
)

REVIEWED = "2026-11-13"
SOURCE_ESDM = "src-esdm-37-projects-2025-01-20"
SOURCE_ESDM_DETAILS = "src-esdm-37-projects-details-2025-01-20"
SOURCE_GNFI = "src-gnfi-26-plants-2025-01-26"
SOURCE_LISTRIK = "src-listrikindonesia-6-plts-2025-01-23"

PROGRAMME_ID = "prog-electricity"
ORG_PLN = "org-pln"

STATUS_GEN = (
    "Inaugurated by President Prabowo on 20 January 2025 as one of the 26 "
    "generating plants in the 37 strategic electricity projects; ESDM lists it "
    "as a completed plant."
)
STATUS_GRID = (
    "Inaugurated by President Prabowo on 20 January 2025 as one of the 11 "
    "transmission and substation projects in the 37 strategic electricity "
    "projects; ESDM lists it as completed."
)

NEW_SOURCES = [
    {
        "id": SOURCE_ESDM,
        "publisher": "Kementerian Energi dan Sumber Daya Mineral (ESDM)",
        "title": (
            "Menuju Kemandirian Energi, Presiden Prabowo Resmikan 37 Proyek "
            "Strategis Ketenagalistrikan 3,2 Gigawatt"
        ),
        "url": (
            "https://www.esdm.go.id/id/media-center/arsip-berita/"
            "menuju-kemandirian-energi-presiden-prabowo-resmikan-37-proyek-"
            "strategis-ketenagalistrikan-32-gigawatt"
        ),
        "published_on": "2025-01-20",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "109035eabe207da06172d462039aa1ed38f54a9dc64bed3b259af675c7673df1"
        ),
        "accessed_via": "",
        "archive_path": "data/raw/2026-11-13/esdm_37_projects_2025-01-20.html",
        "licence": "",
        "notes": (
            "Press release 005.Pers/04/SJI/2025. Lists the 26 generating plants "
            "and 11 transmission and substation projects; states 3,222.75 MW, "
            "739.71 kms and 1,740 MVA for the bundle."
        ),
    },
    {
        "id": SOURCE_ESDM_DETAILS,
        "publisher": "Kementerian Energi dan Sumber Daya Mineral (ESDM)",
        "title": (
            "Proyek Ketenagalistrikan 3,2 GW Diresmikan, Presiden Prabowo: "
            "Hasil Kerja Putra-Putri Bangsa"
        ),
        "url": (
            "https://www.esdm.go.id/id/media-center/arsip-berita/"
            "proyek-ketenagalistrikan-32-gw-diresmikan-presiden-prabowo-hasil-"
            "kerja-putra-putri-bangsa"
        ),
        "published_on": "2025-01-20",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "342fde27015b4275146a9ce06eb56ed7681d471b03a5cfc23765d0308fca49b6"
        ),
        "accessed_via": "",
        "archive_path": (
            "data/raw/2026-11-13/esdm_37_projects_details_2025-01-20.html"
        ),
        "licence": "",
        "notes": (
            "Detail release on the same inauguration. Gives Jatigede, Asahan III "
            "and PLTS IKN capacity, households, CO2, workers, BESS and output."
        ),
    },
    {
        "id": SOURCE_GNFI,
        "publisher": "Good News From Indonesia (GNFI)",
        "title": (
            "Ini Sebaran 26 Pembangkit Listrik yang Baru Diresmikan, Ada 6 di "
            "Wilayah 3T!"
        ),
        "url": (
            "https://www.goodnewsfromindonesia.id/indonesiana/nasional/"
            "ini-sebaran-26-pembangkit-listrik-yang-baru-diresmikan-ada-6-di-"
            "wilayah-3t"
        ),
        "published_on": "2025-01-26",
        "retrieved_on": REVIEWED,
        "source_type": "secondary",
        "language": "id",
        "snapshot_hash": (
            "99d016181ac52103d75d8659ed443ae72fa1bb48fb996b2ec43670c6a109468d"
        ),
        "accessed_via": "",
        "archive_path": "data/raw/2026-11-13/gnfi_26_plants_2025-01-26.html",
        "licence": "",
        "notes": (
            "Groups the 26 plants by island: Sumatra 7 (259 MW), Kalimantan 3, "
            "Java 9 and Sulawesi 7. Spells Duminanga and Sedulang Kecil "
            "differently from ESDM."
        ),
    },
    {
        "id": SOURCE_LISTRIK,
        "publisher": "Listrik Indonesia",
        "title": "6 PLTS di Wilayah 3T Resmi Beroperasi",
        "url": (
            "https://listrikindonesia.com/detail/15459/"
            "6-plts-di-wilayah-3t-resmi-beroperasi"
        ),
        "published_on": "2025-01-23",
        "retrieved_on": REVIEWED,
        "source_type": "secondary",
        "language": "id",
        "snapshot_hash": (
            "0ba75e4be7e86db30b2c9bb96a26dbb7e65cc33273bb3ef3a878f29000c5f643"
        ),
        "accessed_via": "",
        "archive_path": (
            "data/raw/2026-11-13/listrikindonesia_6_plts_3t_2025-01-23.html"
        ),
        "licence": "",
        "notes": (
            "Gives the five Sumenep plant capacities, the Tanamalala capacity "
            "and benefits, and the 40 MW PLTMG Luwuk that the Luwuk line "
            "connects."
        ),
    },
]

# id, English name, Indonesian name, subsector, island, province, route,
# capacity, capacity unit, lat, lon, precision, ESDM list alias, notes,
# extra claims. A claim tuple is (source, claim, value, date, notes).
GEN = [
    {
        "id": "power-asahan-3-unit-1",
        "name": "Asahan 3 Hydropower Unit 1",
        "name_id": "PLTA Asahan 3 Unit 1",
        "subsector": "hydro",
        "island": "Sumatra",
        "province": "North Sumatra",
        "route": "Upper Asahan River, Toba Samosir Regency, North Sumatra",
        "capacity": "87",
        "capacity_unit": "MW",
        "lat": "2.40",
        "lon": "99.15",
        "precision": "approximate",
        "alias": "PLTA Asahan 3 #1",
        "notes": (
            "Unit 1 of the 174 MW (2x87 MW) Asahan III hydropower plant on the "
            "upper Asahan River. ESDM reports 113,769 households, 688,610 t "
            "CO2/yr avoided and 1,952 local workers for the plant."
        ),
        "extra": [
            (
                SOURCE_ESDM_DETAILS,
                "capacity",
                "87 MW (unit of the 174 MW plant)",
                "2025-01-20",
                "",
            )
        ],
    },
    {
        "id": "power-asahan-3-unit-2",
        "name": "Asahan 3 Hydropower Unit 2",
        "name_id": "PLTA Asahan 3 Unit 2",
        "subsector": "hydro",
        "island": "Sumatra",
        "province": "North Sumatra",
        "route": "Upper Asahan River, Toba Samosir Regency, North Sumatra",
        "capacity": "87",
        "capacity_unit": "MW",
        "lat": "2.40",
        "lon": "99.15",
        "precision": "approximate",
        "alias": "PLTA Asahan 3 #2",
        "notes": (
            "Unit 2 of the 174 MW (2x87 MW) Asahan III hydropower plant on the "
            "upper Asahan River. ESDM reports 113,769 households, 688,610 t "
            "CO2/yr avoided and 1,952 local workers for the plant."
        ),
        "extra": [
            (
                SOURCE_ESDM_DETAILS,
                "capacity",
                "87 MW (unit of the 174 MW plant)",
                "2025-01-20",
                "",
            )
        ],
    },
    {
        "id": "power-sorik-marapi-2",
        "name": "Sorik Marapi Geothermal Unit 2",
        "name_id": "PLTP Sorik Marapi Unit 2",
        "subsector": "geothermal",
        "island": "Sumatra",
        "province": "North Sumatra",
        "route": "Sorik Marapi, Mandailing Natal Regency, North Sumatra",
        "capacity": "",
        "capacity_unit": "",
        "lat": "0.68",
        "lon": "99.54",
        "precision": "approximate",
        "alias": "PLTP Sorik Marapi #2",
        "notes": (
            "Unit 2 of the Sorik Marapi geothermal plant in Mandailing Natal. "
            "ESDM lists it among the 26 plants but the archived releases do not "
            "state its unit capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-jatigede",
        "name": "Jatigede Hydropower Plant",
        "name_id": "PLTA Jatigede",
        "subsector": "hydro",
        "island": "Java",
        "province": "West Java",
        "route": "Jatigede Dam, Sumedang Regency, West Java",
        "capacity": "110",
        "capacity_unit": "MW",
        "lat": "-6.8586",
        "lon": "108.0636",
        "precision": "approximate",
        "alias": "PLTA Jatigede",
        "notes": (
            "110 MW (2x55 MW) at Jatigede Dam, Sumedang. ESDM reports 71,923 "
            "households, 415,800 t CO2/yr avoided and 485 local workers. The "
            "inauguration ceremony was held at this plant."
        ),
        "extra": [
            (
                SOURCE_ESDM_DETAILS,
                "capacity",
                "110 MW (2x55 MW)",
                "2025-01-20",
                "",
            )
        ],
    },
    {
        "id": "power-jawa-1",
        "name": "Jawa 1 Gas and Steam Power Plant",
        "name_id": "PLTGU Jawa 1",
        "subsector": "gas",
        "island": "Java",
        "province": "West Java",
        "route": "Cilamaya Wetan, Karawang Regency, West Java",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-6.236",
        "lon": "107.578",
        "precision": "approximate",
        "alias": "PLTGU Jawa 1",
        "notes": (
            "Combined-cycle gas plant in Cilamaya, Karawang. ESDM lists it "
            "among the 26 plants but the archived releases do not state its "
            "capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-muara-tawar-add-on-2-3-4",
        "name": "Muara Tawar Add-On Blocks 2-4 Gas and Steam Power Plant",
        "name_id": "PLTGU Muara Tawar Add-On Blok 2-4",
        "subsector": "gas",
        "island": "Java",
        "province": "West Java",
        "route": "Muara Tawar, Bekasi Regency, West Java",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-6.096",
        "lon": "107.045",
        "precision": "approximate",
        "alias": "PLTGU Muara Tawar Add On Blok 2,3,4",
        "notes": (
            "Add-on blocks 2-4 at the Muara Tawar combined-cycle plant in "
            "Bekasi. ESDM lists it among the 26 plants but the archived releases "
            "do not state its capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-tambak-lorok-block-3",
        "name": "Tambak Lorok Block 3 Gas and Steam Power Plant",
        "name_id": "PLTGU Tambak Lorok Blok 3",
        "subsector": "gas",
        "island": "Java",
        "province": "Central Java",
        "route": "Tambak Lorok, Semarang, Central Java",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-6.944",
        "lon": "110.423",
        "precision": "approximate",
        "alias": "PLTGU Jawa Bali 1 Tambak Look",
        "alias_notes": (
            "ESDM list spelling; the plant is commonly written Tambak Lorok."
        ),
        "notes": (
            "Block 3 of the Tambak Lorok combined-cycle plant in Semarang. ESDM "
            "spells the project 'Tambak Look' in the 37-project list. The "
            "archived releases do not state its capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-plts-ikn",
        "name": "IKN Solar Power Plant",
        "name_id": "PLTS IKN",
        "subsector": "solar",
        "island": "Kalimantan",
        "province": "East Kalimantan",
        "route": "KIPP Nusantara, Penajam Paser Utara Regency, East Kalimantan",
        "capacity": "50",
        "capacity_unit": "MWac",
        "lat": "-0.975",
        "lon": "116.708",
        "precision": "approximate",
        "alias": "PLTS IKN 10 MW",
        "alias_notes": (
            "ESDM project-list name; the same ministry's detail release gives "
            "50 MWac / 72 MWp."
        ),
        "notes": (
            "50 MWac / 72 MWp with a 10.32 MWh battery storage system. ESDM's "
            "project list names the entry 'PLTS IKN 10 MW' while its detail "
            "release gives 50 MWac / 72 MWp; the list entry appears to be phase "
            "1. ESDM reports 92.8 GWh/yr, 44,000 t CO2/yr avoided and 502 local "
            "workers."
        ),
        "extra": [
            (
                SOURCE_ESDM_DETAILS,
                "design capacity",
                "50 MWac / 72 MWp",
                "2025-01-20",
                "The ESDM project list names the 10 MW entry.",
            ),
            (
                SOURCE_ESDM_DETAILS,
                "capacity",
                "10.32 MWh battery storage",
                "2025-01-20",
                "",
            ),
            (
                SOURCE_ESDM_DETAILS,
                "output",
                "92.8 GWh/yr",
                "2025-01-20",
                "",
            ),
        ],
    },
    {
        "id": "power-kalselteng-2-unit-1",
        "name": "Kalselteng-2 Coal Power Plant Unit 1",
        "name_id": "PLTU Kalselteng-2 Unit 1",
        "subsector": "coal",
        "island": "Kalimantan",
        "province": "South Kalimantan",
        "route": "Kalselteng-2 project, South Kalimantan",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-2.76531",
        "lon": "115.43637",
        "precision": "province",
        "alias": "PLTU Kalselteng - 2 #1",
        "notes": (
            "Unit 1 of the two Kalselteng-2 coal units. GNFI groups both under "
            "Kalimantan and the project name covers South and Central "
            "Kalimantan; the archived releases do not give the regency or "
            "capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-kalselteng-2-unit-2",
        "name": "Kalselteng-2 Coal Power Plant Unit 2",
        "name_id": "PLTU Kalselteng-2 Unit 2",
        "subsector": "coal",
        "island": "Kalimantan",
        "province": "South Kalimantan",
        "route": "Kalselteng-2 project, South Kalimantan",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-2.76531",
        "lon": "115.43637",
        "precision": "province",
        "alias": "PLTU Kalselteng - 2 #2",
        "notes": (
            "Unit 2 of the two Kalselteng-2 coal units. GNFI groups both under "
            "Kalimantan and the project name covers South and Central "
            "Kalimantan; the archived releases do not give the regency or "
            "capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-mpp-sulselbar",
        "name": "Sulselbar Mobile Power Plant (BMPP Nusantara 1)",
        "name_id": "MPP Sulselbar (BMPP Nusantara 1)",
        "subsector": "mobile_gas",
        "island": "Sulawesi",
        "province": "West Sulawesi; South Sulawesi",
        "route": "Sulawesi Barat-Sulawesi Selatan (Sulselbar) area",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-3.0",
        "lon": "119.5",
        "precision": "approximate",
        "alias": "MPP Sulselbar (BMPP Nusantara #1)",
        "notes": (
            "Barge-mounted mobile power plant (BMPP Nusantara 1) for the "
            "Sulawesi Barat-Sulawesi Selatan area. ESDM lists it among the 26 "
            "plants but the archived releases do not state its capacity or "
            "exact berth."
        ),
        "extra": [],
    },
    {
        "id": "power-palu-3-unit-1",
        "name": "Palu-3 Coal Power Plant Unit 1",
        "name_id": "PLTU Palu-3 Unit 1",
        "subsector": "coal",
        "island": "Sulawesi",
        "province": "Central Sulawesi",
        "route": "Palu-3 project, Central Sulawesi",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-2.32901",
        "lon": "121.60611",
        "precision": "province",
        "alias": "PLTU Palu - 3 #1",
        "notes": (
            "Unit 1 of the Palu-3 coal plant. ESDM lists two units but the "
            "archived releases do not state their capacity or regency."
        ),
        "extra": [],
    },
    {
        "id": "power-palu-3-unit-2",
        "name": "Palu-3 Coal Power Plant Unit 2",
        "name_id": "PLTU Palu-3 Unit 2",
        "subsector": "coal",
        "island": "Sulawesi",
        "province": "Central Sulawesi",
        "route": "Palu-3 project, Central Sulawesi",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-2.32901",
        "lon": "121.60611",
        "precision": "province",
        "alias": "PLTU Palu - 3 #2",
        "notes": (
            "Unit 2 of the Palu-3 coal plant. ESDM lists two units but the "
            "archived releases do not state their capacity or regency."
        ),
        "extra": [],
    },
    {
        "id": "power-sulut-1-unit-1",
        "name": "Sulut-1 Coal Power Plant Unit 1",
        "name_id": "PLTU Sulut-1 Unit 1",
        "subsector": "coal",
        "island": "Sulawesi",
        "province": "North Sulawesi",
        "route": "Sulut-1 project, North Sulawesi",
        "capacity": "",
        "capacity_unit": "",
        "lat": "1.52254",
        "lon": "125.07818",
        "precision": "province",
        "alias": "PLTU Sulut -1 #1",
        "notes": (
            "Unit 1 of the Sulut-1 coal plant. ESDM lists only unit 1 among the "
            "37 projects; the archived releases do not state its capacity or "
            "regency."
        ),
        "extra": [],
    },
    {
        "id": "power-pltm-aceh-tersebar",
        "name": "Aceh Distributed Mini-Hydropower Plants",
        "name_id": "PLTM Minihidro Aceh Tersebar",
        "subsector": "hydro",
        "island": "Sumatra",
        "province": "Aceh",
        "route": "Scattered sites across Aceh",
        "capacity": "",
        "capacity_unit": "",
        "lat": "5.08414",
        "lon": "96.71107",
        "precision": "province",
        "alias": "PLTM Minihidro Aceh Tersebar",
        "notes": (
            "A bundled entry for distributed mini-hydropower plants across "
            "Aceh. ESDM lists it as one project but the archived releases do not "
            "name the sites or state the capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-pltbm-sadai",
        "name": "Sadai Biomass Power Plant",
        "name_id": "PLTBm Sadai Bangka Selatan",
        "subsector": "biomass",
        "island": "Sumatra",
        "province": "Bangka Belitung",
        "route": "Sadai, Bangka Selatan Regency, Bangka Belitung",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-2.90",
        "lon": "106.10",
        "precision": "approximate",
        "alias": "PLTBm Sadai Bangka Selatan",
        "notes": (
            "Biomass plant at Sadai, Bangka Selatan. ESDM lists it among the 26 "
            "plants but the archived releases do not state its capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-pltm-ordi-hulu",
        "name": "Ordi Hulu Mini-Hydropower Plant",
        "name_id": "PLTM Ordi Hulu",
        "subsector": "hydro",
        "island": "Sumatra",
        "province": "North Sumatra",
        "route": "Ordi Hulu, North Sumatra",
        "capacity": "",
        "capacity_unit": "",
        "lat": "3.23365",
        "lon": "99.21523",
        "precision": "province",
        "alias": "PLTM Ordi Hulu",
        "notes": (
            "Mini-hydropower plant in North Sumatra. ESDM lists it among the 26 "
            "plants but the archived releases do not state its site or capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-pltbm-deli-serdang",
        "name": "Deli Serdang Biomass Power Plant",
        "name_id": "PLTBm Deli Serdang",
        "subsector": "biomass",
        "island": "Sumatra",
        "province": "North Sumatra",
        "route": "Deli Serdang Regency, North Sumatra",
        "capacity": "",
        "capacity_unit": "",
        "lat": "3.55",
        "lon": "98.70",
        "precision": "approximate",
        "alias": "PLTBm Deli Serdang",
        "notes": (
            "Biomass plant in Deli Serdang. ESDM lists it among the 26 plants "
            "but the archived releases do not state its capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-plts-pajangan",
        "name": "Pajangan Village Solar Power Plant",
        "name_id": "PLTS Lisdes Pajangan",
        "subsector": "solar",
        "island": "Java",
        "province": "East Java",
        "route": "Pajangan, Sumenep Regency, East Java",
        "capacity": "25",
        "capacity_unit": "kWp",
        "lat": "-7.01",
        "lon": "113.86",
        "precision": "regency",
        "alias": "PLTS Lisdes Pajangan",
        "notes": (
            "Village solar plant in Sumenep with 25 kWp. Part of the five-plant "
            "Sumenep cluster; Listrik Indonesia reports the cluster avoids 6,078 "
            "L of diesel and produces 22,000 kWh/yr for 597 households."
        ),
        "extra": [
            (
                SOURCE_LISTRIK,
                "capacity",
                "25 kWp",
                "2025-01-23",
                "",
            )
        ],
    },
    {
        "id": "power-plts-sadulang-kecil",
        "name": "Sadulang Kecil Village Solar Power Plant",
        "name_id": "PLTS Lisdes Sadulang Kecil",
        "subsector": "solar",
        "island": "Java",
        "province": "East Java",
        "route": "Sadulang Kecil, Sumenep Regency, East Java",
        "capacity": "50",
        "capacity_unit": "kWp",
        "lat": "-7.01",
        "lon": "113.86",
        "precision": "regency",
        "alias": "PLTS Lisdes Sadulang Kecil",
        "alias2": "PLTS Lisdes Sedulang Kecil",
        "alias2_source": SOURCE_GNFI,
        "alias2_notes": "GNFI spelling variant.",
        "notes": (
            "Village solar plant in Sumenep with 50 kWp. Part of the five-plant "
            "Sumenep cluster; Listrik Indonesia reports the cluster avoids 6,078 "
            "L of diesel and produces 22,000 kWh/yr for 597 households."
        ),
        "extra": [
            (
                SOURCE_LISTRIK,
                "capacity",
                "50 kWp",
                "2025-01-23",
                "",
            )
        ],
    },
    {
        "id": "power-plts-sapapan",
        "name": "Sapapan Village Solar Power Plant",
        "name_id": "PLTS Lisdes Sapapan",
        "subsector": "solar",
        "island": "Java",
        "province": "East Java",
        "route": "Sapapan, Sumenep Regency, East Java",
        "capacity": "50",
        "capacity_unit": "kWp",
        "lat": "-7.01",
        "lon": "113.86",
        "precision": "regency",
        "alias": "PLTS Lisdes Sapapan",
        "notes": (
            "Village solar plant in Sumenep with 50 kWp. Part of the five-plant "
            "Sumenep cluster; Listrik Indonesia reports the cluster avoids 6,078 "
            "L of diesel and produces 22,000 kWh/yr for 597 households."
        ),
        "extra": [
            (
                SOURCE_LISTRIK,
                "capacity",
                "50 kWp",
                "2025-01-23",
                "",
            )
        ],
    },
    {
        "id": "power-plts-sapangkur-kecil",
        "name": "Sapangkur Kecil Village Solar Power Plant",
        "name_id": "PLTS Lisdes Sapangkur Kecil",
        "subsector": "solar",
        "island": "Java",
        "province": "East Java",
        "route": "Sapangkur Kecil, Sumenep Regency, East Java",
        "capacity": "50",
        "capacity_unit": "kWp",
        "lat": "-7.01",
        "lon": "113.86",
        "precision": "regency",
        "alias": "PLTS Lisdes Sapangkur Kecil",
        "alias2": "PLTS Sepangkur Kecil",
        "alias2_source": SOURCE_LISTRIK,
        "alias2_notes": "Listrik Indonesia spelling variant.",
        "notes": (
            "Village solar plant in Sumenep with 50 kWp. Part of the five-plant "
            "Sumenep cluster; Listrik Indonesia reports the cluster avoids 6,078 "
            "L of diesel and produces 22,000 kWh/yr for 597 households."
        ),
        "extra": [
            (
                SOURCE_LISTRIK,
                "capacity",
                "50 kWp",
                "2025-01-23",
                "",
            )
        ],
    },
    {
        "id": "power-plts-saur",
        "name": "Saur Village Solar Power Plant",
        "name_id": "PLTS Lisdes Saur",
        "subsector": "solar",
        "island": "Java",
        "province": "East Java",
        "route": "Saur, Sumenep Regency, East Java",
        "capacity": "150",
        "capacity_unit": "kWp",
        "lat": "-7.01",
        "lon": "113.86",
        "precision": "regency",
        "alias": "PLTS Lisdes Saur",
        "notes": (
            "Village solar plant in Sumenep with 150 kWp. Part of the five-plant "
            "Sumenep cluster; Listrik Indonesia reports the cluster avoids 6,078 "
            "L of diesel and produces 22,000 kWh/yr for 597 households."
        ),
        "extra": [
            (
                SOURCE_LISTRIK,
                "capacity",
                "150 kWp",
                "2025-01-23",
                "",
            )
        ],
    },
    {
        "id": "power-pltm-koro-yaentu",
        "name": "Koro Yaentu Mini-Hydropower Plant",
        "name_id": "PLTM Koro Yaentu",
        "subsector": "hydro",
        "island": "Sulawesi",
        "province": "Central Sulawesi",
        "route": "Koro Yaentu, Central Sulawesi",
        "capacity": "",
        "capacity_unit": "",
        "lat": "-2.32901",
        "lon": "121.60611",
        "precision": "province",
        "alias": "PLTM Koro Yaentu",
        "notes": (
            "Mini-hydropower plant in Central Sulawesi. ESDM lists it among the "
            "26 plants but the archived releases do not state its site or "
            "capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-pltm-dominanga",
        "name": "Dominanga Mini-Hydropower Plant",
        "name_id": "PLTM Dominanga",
        "subsector": "hydro",
        "island": "Sulawesi",
        "province": "North Sulawesi",
        "route": "Dominanga, North Sulawesi",
        "capacity": "",
        "capacity_unit": "",
        "lat": "1.52254",
        "lon": "125.07818",
        "precision": "province",
        "alias": "PLTM Dominanga",
        "alias2": "PLTM Duminanga",
        "alias2_source": SOURCE_GNFI,
        "alias2_notes": "GNFI spelling variant.",
        "notes": (
            "Mini-hydropower plant in North Sulawesi. ESDM spells it 'PLTM "
            "Dominanga'; GNFI spells it 'PLTM Duminanga'. The archived releases "
            "do not state its site or capacity."
        ),
        "extra": [],
    },
    {
        "id": "power-plts-tanamalala",
        "name": "Tanamalala Village Solar Power Plant",
        "name_id": "PLTS Lisdes Tanamalala",
        "subsector": "solar",
        "island": "Sulawesi",
        "province": "South Sulawesi",
        "route": "Tanamalala, Selayar Islands Regency, South Sulawesi",
        "capacity": "189.6",
        "capacity_unit": "kWp",
        "lat": "-6.10",
        "lon": "120.50",
        "precision": "regency",
        "alias": "PLTS Lisdes Tanamalala",
        "notes": (
            "189.6 kWp village solar plant on Selayar. Listrik Indonesia reports "
            "185 households, 197,000 kWh/yr, 29,000 L of diesel avoided and 415 "
            "t CO2/yr avoided."
        ),
        "extra": [
            (
                SOURCE_LISTRIK,
                "capacity",
                "189.6 kWp",
                "2025-01-23",
                "",
            )
        ],
    },
]

GRID = [
    {
        "id": "grid-muara-enim-gumawang",
        "name": "Muara Enim-Gumawang 275 kV Transmission and Lampung 1 Substation",
        "name_id": (
            "SUTET 275 kV Muara Enim-Gumawang dan GI 150 kV Lampung 1"
        ),
        "island": "Sumatra",
        "province": "South Sumatra; Lampung",
        "route": (
            "Muara Enim-Gumawang, South Sumatra, and Lampung 1 substation, "
            "Lampung"
        ),
        "lat": "-3.10534",
        "lon": "104.1996",
        "precision": "province",
        "alias": (
            "SUTET 275 kV Muara Enim - Gumawang dan GI 150 kV Lampung 1"
        ),
        "notes": (
            "275 kV transmission line and 150 kV Lampung 1 substation. Part of "
            "the 11 transmission and substation projects; ESDM reports 739.71 "
            "kms and 1,740 MVA across the bundle but no per-project length."
        ),
        "extra": [],
    },
    {
        "id": "grid-kendawangan-marau-sukamara",
        "name": (
            "Kendawangan-Marau-Sukamara 150 kV Transmission and Sukamara "
            "Substation"
        ),
        "name_id": (
            "SUTT 150 kV Kendawangan-Marau-Sukamara dan GI 150 kV Sukamara "
            "Ext 2LB"
        ),
        "island": "Kalimantan",
        "province": "West Kalimantan",
        "route": "Kendawangan-Marau-Sukamara, West Kalimantan",
        "lat": "-0.5706",
        "lon": "109.35566",
        "precision": "province",
        "alias": (
            "SUTT 150 kV Kendawangan - Marau - Sukamara dan GI 150 kV "
            "Sukamara Ext 2LB"
        ),
        "notes": (
            "150 kV line and Sukamara extension substation. Part of the 11 "
            "transmission and substation projects; no per-project length is "
            "stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-kariangau-kipp",
        "name": "Kariangau-KIPP GIS 4 150 kV Transmission and Substation",
        "name_id": (
            "GI 150 kV Kariangau arah GIS 4 KIPP dan SUTT 150 kV Kariangau-"
            "Landing Point GIS 4 KIPP"
        ),
        "island": "Kalimantan",
        "province": "East Kalimantan",
        "route": "Kariangau-Landing Point GIS 4 KIPP, East Kalimantan",
        "lat": "-0.66745",
        "lon": "117.04239",
        "precision": "province",
        "alias": (
            "GI 150 kV Kariangau arah GIS 4 KIPP dan SUTT 150 kV Kariangau - "
            "Landing Point GIS 4 KIPP GIS 4 KIPP 150 kV"
        ),
        "alias_notes": "ESDM list wording.",
        "notes": (
            "150 kV substation at Kariangau toward GIS 4 KIPP and the "
            "connecting line. Part of the 11 transmission and substation "
            "projects; no per-project length is stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-kolaka-pomala",
        "name": "Kolaka-Pomala 150 kV Transmission and Kolaka Substation",
        "name_id": (
            "SUTT 150 kV GI Kolaka-PT Antam Pomala dan GI 150 kV Kolaka Ext"
        ),
        "island": "Sulawesi",
        "province": "Southeast Sulawesi",
        "route": "Kolaka-PT Antam Pomala, Southeast Sulawesi",
        "lat": "-3.95366",
        "lon": "122.1222",
        "precision": "province",
        "alias": (
            "SUTT 150 kV GI Kolaka - PT Antam Pomala dan GI 150 kV Kolaka Ext"
        ),
        "notes": (
            "150 kV line from Kolaka substation to PT Antam Pomala and the "
            "Kolaka extension substation. Part of the 11 transmission and "
            "substation projects; no per-project length is stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-luwuk",
        "name": "Luwuk 150 kV Transmission and Substation",
        "name_id": "SUTT 150 kV PLTMG Luwuk-GI Luwuk dan GI 150 kV Luwuk",
        "island": "Sulawesi",
        "province": "Central Sulawesi",
        "route": "PLTMG Luwuk-GI Luwuk, Banggai Regency, Central Sulawesi",
        "lat": "-0.95",
        "lon": "122.79",
        "precision": "approximate",
        "alias": (
            "SUTT 150 kV PLTMG Luwuk -Gl Luwuk danGI 150 kV Luwuk"
        ),
        "notes": (
            "150 kV line from the 40 MW PLTMG Luwuk to the Luwuk substation. "
            "Listrik Indonesia says the gas plant replaces a rented 40 MW diesel "
            "plant and can save 500,000 L of fuel per year. Part of the 11 "
            "transmission and substation projects."
        ),
        "extra": [
            (
                SOURCE_LISTRIK,
                "output",
                "connects the 40 MW PLTMG Luwuk",
                "2025-01-23",
                (
                    "The gas plant replaces a rented 40 MW diesel plant and can "
                    "save 500,000 L of fuel per year."
                ),
            )
        ],
    },
    {
        "id": "grid-flores-labuan-bajo",
        "name": "Flores-Labuan Bajo 70 kV Transmission and Substations",
        "name_id": (
            "SUTT 70 kV GI PLTMG Flores-GI Labuan Bajo dan GI 66 kV Labuan "
            "Bajo (2 LB) dan GI 66 kV PLTMG Flores"
        ),
        "island": "Bali-Nusa Tenggara",
        "province": "East Nusa Tenggara",
        "route": "PLTMG Flores-Labuan Bajo, East Nusa Tenggara",
        "lat": "-8.9465",
        "lon": "121.38823",
        "precision": "province",
        "alias": (
            "SUTT 70 kV GI PLTMG Flores - GI Labuan Bajo dan GI 66 kV Labuan "
            "Bajo (2 LB) dan GI 66 KV PLTMG Flores"
        ),
        "notes": (
            "70 kV line from PLTMG Flores to Labuan Bajo and the 66 kV Labuan "
            "Bajo and PLTMG Flores substations. Part of the 11 transmission and "
            "substation projects; no per-project length is stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-muara-karang-durikosambi",
        "name": "Muara Karang Baru-Durikosambi 500 kV Transmission",
        "name_id": "SUTET 500 kV Muara Karang Baru-Durikosambi",
        "island": "Java",
        "province": "DKI Jakarta",
        "route": "Muara Karang Baru-Durikosambi, DKI Jakarta",
        "lat": "-6.23886",
        "lon": "106.91435",
        "precision": "province",
        "alias": "SUTET 500 kV Muara Karang Baru - Durikosambi",
        "notes": (
            "500 kV transmission link between Muara Karang Baru and Durikosambi "
            "in Jakarta. Part of the 11 transmission and substation projects; no "
            "per-project length is stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-ampel-boyolali-500",
        "name": "Ampel Boyolali 500 kV Substation and Incomer",
        "name_id": (
            "GITET 500 kV Ampel Boyolali (2x500 MVA), SUTET 500 kV Ampel "
            "New/Boyolali Incomer Arah Ungaran dan Pedan Sirkit 1"
        ),
        "island": "Java",
        "province": "Central Java",
        "route": "Ampel New/Boyolali, Central Java",
        "lat": "-7.28449",
        "lon": "109.92084",
        "precision": "province",
        "alias": (
            "GITET 500 kV Ampel Boyolali (2x500 MVA), SUTET 500 kV Ampel "
            "New/Boyolali Incomer Arah Ungaran dan Pedan Sirkit 1"
        ),
        "notes": (
            "500 kV substation (2x500 MVA), the Ampel New/Boyolali incomer "
            "toward Ungaran and the Pedan circuit 1. Part of the 11 transmission "
            "and substation projects; no per-project length is stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-ampel-bringin-mojosongo",
        "name": "Ampel-Bringin-Mojosongo 150 kV Transmission",
        "name_id": (
            "SUTT 150 kV Ampel New/Boyolali Incomer arah Bringin dan Mojosongo "
            "Sirkit 1 dan 2"
        ),
        "island": "Java",
        "province": "Central Java",
        "route": "Ampel New/Boyolali-Bringin-Mojosongo, Central Java",
        "lat": "-7.28449",
        "lon": "109.92084",
        "precision": "province",
        "alias": (
            "SUTT 150 kV Ampel New/Boyolali Incomer arah Bringin dan Mojosongo "
            "Sirkit 1 dan 2"
        ),
        "notes": (
            "150 kV incomer from Ampel New/Boyolali toward Bringin and the "
            "Mojosongo circuits 1 and 2. Part of the 11 transmission and "
            "substation projects; no per-project length is stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-duren-tiga-depok",
        "name": "Duren Tiga-Depok II 150 kV Transmission",
        "name_id": (
            "SUTT 150 kV Duren Tiga II/Ragunan (GIS)-Depok II Sirkit 1"
        ),
        "island": "Java",
        "province": "DKI Jakarta; West Java",
        "route": "Duren Tiga II/Ragunan (GIS)-Depok II, DKI Jakarta-West Java",
        "lat": "-6.30",
        "lon": "106.80",
        "precision": "approximate",
        "alias": (
            "SUTT 150 kV Duren Tiga II / Ragunan (GIS) - Depok II Sirkit 1"
        ),
        "notes": (
            "150 kV circuit from Duren Tiga II/Ragunan GIS to Depok II. Part of "
            "the 11 transmission and substation projects; no per-project length "
            "is stated."
        ),
        "extra": [],
    },
    {
        "id": "grid-cilegon-ibt-4",
        "name": "Cilegon 500 kV IBT 4 Extension",
        "name_id": "Extension IBT 4 GITET 500 kV Cilegon",
        "island": "Java",
        "province": "Banten",
        "route": "Cilegon, Banten",
        "lat": "-6.00",
        "lon": "106.05",
        "precision": "approximate",
        "alias": "Extension IBT 4 GITET 500 kV Cilegon",
        "notes": (
            "Extension of the 500 kV Cilegon interconnection (IBT 4). Part of "
            "the 11 transmission and substation projects; no per-project length "
            "is stated."
        ),
        "extra": [],
    },
]

# id, project_id, programme_id, name_en, name_id, unit, direction, value,
# as_of, source, notes.
INDICATORS = [
    (
        "ind-jatigede-capacity", "power-jatigede", "",
        "Jatigede installed capacity", "Kapasitas terpasang Jatigede",
        "MW", "increase", "110", "2025-01-20", SOURCE_ESDM_DETAILS,
        "110 MW (2x55 MW).",
    ),
    (
        "ind-jatigede-households", "power-jatigede", "",
        "Households served by Jatigede", "Rumah tangga terlayani Jatigede",
        "households", "increase", "71923", "2025-01-20", SOURCE_ESDM_DETAILS,
        "ESDM says more than 71,923 households.",
    ),
    (
        "ind-jatigede-co2", "power-jatigede", "",
        "CO2 emissions avoided by Jatigede", "Emisi CO2 dihindari Jatigede",
        "t CO2/yr", "increase", "415800", "2025-01-20", SOURCE_ESDM_DETAILS,
        "415,800 t CO2 per year.",
    ),
    (
        "ind-jatigede-workers", "power-jatigede", "",
        "Local workers at Jatigede", "Tenaga kerja lokal Jatigede",
        "workers", "increase", "485", "2025-01-20", SOURCE_ESDM_DETAILS,
        "485 local workers.",
    ),
    (
        "ind-asahan-3-capacity", "power-asahan-3-unit-1", "",
        "Asahan 3 installed capacity", "Kapasitas terpasang Asahan 3",
        "MW", "increase", "174", "2025-01-20", SOURCE_ESDM_DETAILS,
        "174 MW (2x87 MW); the atlas has one row per unit.",
    ),
    (
        "ind-asahan-3-households", "power-asahan-3-unit-1", "",
        "Households served by Asahan 3", "Rumah tangga terlayani Asahan 3",
        "households", "increase", "113769", "2025-01-20", SOURCE_ESDM_DETAILS,
        "ESDM says more than 113,769 households.",
    ),
    (
        "ind-asahan-3-co2", "power-asahan-3-unit-1", "",
        "CO2 emissions avoided by Asahan 3", "Emisi CO2 dihindari Asahan 3",
        "t CO2/yr", "increase", "688610", "2025-01-20", SOURCE_ESDM_DETAILS,
        "688,610 t CO2 per year.",
    ),
    (
        "ind-asahan-3-workers", "power-asahan-3-unit-1", "",
        "Local workers at Asahan 3", "Tenaga kerja lokal Asahan 3",
        "workers", "increase", "1952", "2025-01-20", SOURCE_ESDM_DETAILS,
        "1,952 local workers.",
    ),
    (
        "ind-plts-ikn-capacity-ac", "power-plts-ikn", "",
        "PLTS IKN installed capacity (AC)", "Kapasitas terpasang PLTS IKN (AC)",
        "MWac", "increase", "50", "2025-01-20", SOURCE_ESDM_DETAILS,
        "50 MWac; the ESDM project list names the 10 MW entry.",
    ),
    (
        "ind-plts-ikn-capacity-dc", "power-plts-ikn", "",
        "PLTS IKN installed capacity (DC)", "Kapasitas terpasang PLTS IKN (DC)",
        "MWp", "increase", "72", "2025-01-20", SOURCE_ESDM_DETAILS,
        "72 MWp.",
    ),
    (
        "ind-plts-ikn-bess", "power-plts-ikn", "",
        "PLTS IKN battery storage", "Penyimpanan baterai PLTS IKN",
        "MWh", "increase", "10.32", "2025-01-20", SOURCE_ESDM_DETAILS,
        "10.32 MWh battery energy storage system.",
    ),
    (
        "ind-plts-ikn-output", "power-plts-ikn", "",
        "PLTS IKN annual output", "Keluaran tahunan PLTS IKN",
        "GWh/yr", "increase", "92.8", "2025-01-20", SOURCE_ESDM_DETAILS,
        "92.8 GWh of green energy per year.",
    ),
    (
        "ind-plts-ikn-co2", "power-plts-ikn", "",
        "CO2 emissions avoided by PLTS IKN", "Emisi CO2 dihindari PLTS IKN",
        "t CO2/yr", "increase", "44000", "2025-01-20", SOURCE_ESDM_DETAILS,
        "Up to 44,000 t CO2 per year.",
    ),
    (
        "ind-plts-ikn-workers", "power-plts-ikn", "",
        "Local workers at PLTS IKN", "Tenaga kerja lokal PLTS IKN",
        "workers", "increase", "502", "2025-01-20", SOURCE_ESDM_DETAILS,
        "502 local workers.",
    ),
    (
        "ind-plts-saur-capacity", "power-plts-saur", "",
        "Saur village solar capacity", "Kapasitas PLTS Lisdes Saur",
        "kWp", "increase", "150", "2025-01-23", SOURCE_LISTRIK,
        "150 kWp.",
    ),
    (
        "ind-plts-sepangkur-kecil-capacity", "power-plts-sapangkur-kecil", "",
        "Sapangkur Kecil village solar capacity",
        "Kapasitas PLTS Lisdes Sapangkur Kecil",
        "kWp", "increase", "50", "2025-01-23", SOURCE_LISTRIK,
        "Listrik Indonesia spells the plant Sepangkur Kecil; 50 kWp.",
    ),
    (
        "ind-plts-pajangan-capacity", "power-plts-pajangan", "",
        "Pajangan village solar capacity", "Kapasitas PLTS Lisdes Pajangan",
        "kWp", "increase", "25", "2025-01-23", SOURCE_LISTRIK,
        "25 kWp.",
    ),
    (
        "ind-plts-sapapan-capacity", "power-plts-sapapan", "",
        "Sapapan village solar capacity", "Kapasitas PLTS Lisdes Sapapan",
        "kWp", "increase", "50", "2025-01-23", SOURCE_LISTRIK,
        "50 kWp.",
    ),
    (
        "ind-plts-sadulang-kecil-capacity", "power-plts-sadulang-kecil", "",
        "Sadulang Kecil village solar capacity",
        "Kapasitas PLTS Lisdes Sadulang Kecil",
        "kWp", "increase", "50", "2025-01-23", SOURCE_LISTRIK,
        "50 kWp.",
    ),
    (
        "ind-sumenep-plts-output", "", PROGRAMME_ID,
        "Sumenep village solar annual output",
        "Keluaran tahunan PLTS Lisdes Sumenep",
        "kWh/yr", "increase", "22000", "2025-01-23", SOURCE_LISTRIK,
        "22,000 kWh per year across the five Sumenep plants.",
    ),
    (
        "ind-sumenep-plts-diesel", "", PROGRAMME_ID,
        "Diesel avoided by Sumenep village solar plants",
        "BBM dihindari PLTS Lisdes Sumenep",
        "L/yr", "increase", "6078", "2025-01-23", SOURCE_LISTRIK,
        "6,078 L of generator fuel avoided per year across the five plants.",
    ),
    (
        "ind-sumenep-plts-households", "", PROGRAMME_ID,
        "Households served by Sumenep village solar plants",
        "Rumah tangga terlayani PLTS Lisdes Sumenep",
        "households", "increase", "597", "2025-01-23", SOURCE_LISTRIK,
        "More than 597 households across the five plants.",
    ),
    (
        "ind-plts-tanamalala-capacity", "power-plts-tanamalala", "",
        "Tanamalala village solar capacity",
        "Kapasitas PLTS Lisdes Tanamalala",
        "kWp", "increase", "189.6", "2025-01-23", SOURCE_LISTRIK,
        "189.6 kWp.",
    ),
    (
        "ind-plts-tanamalala-households", "power-plts-tanamalala", "",
        "Households served by Tanamalala",
        "Rumah tangga terlayani Tanamalala",
        "households", "increase", "185", "2025-01-23", SOURCE_LISTRIK,
        "More than 185 households.",
    ),
    (
        "ind-plts-tanamalala-output", "power-plts-tanamalala", "",
        "Tanamalala annual output", "Keluaran tahunan Tanamalala",
        "kWh/yr", "increase", "197000", "2025-01-23", SOURCE_LISTRIK,
        "197,000 kWh per year.",
    ),
    (
        "ind-plts-tanamalala-diesel", "power-plts-tanamalala", "",
        "Diesel avoided by Tanamalala", "BBM dihindari Tanamalala",
        "L/yr", "increase", "29000", "2025-01-23", SOURCE_LISTRIK,
        "29,000 L of generator fuel avoided per year.",
    ),
    (
        "ind-plts-tanamalala-co2", "power-plts-tanamalala", "",
        "CO2 emissions avoided by Tanamalala", "Emisi CO2 dihindari Tanamalala",
        "t CO2/yr", "increase", "415", "2025-01-23", SOURCE_LISTRIK,
        "415 t CO2 per year.",
    ),
]

# programme, source, claim, value, date, notes
PROGRAMME_CLAIMS = [
    (
        PROGRAMME_ID, SOURCE_ESDM, "capacity", "3,222.75 MW", "2025-01-20",
        "Total capacity of the 26 generating plants.",
    ),
    (
        PROGRAMME_ID, SOURCE_ESDM, "output", "89% clean energy", "2025-01-20",
        "Share of the 3.2 GW total from gas and renewable energy.",
    ),
    (
        PROGRAMME_ID, SOURCE_ESDM, "length", "739.71 kms", "2025-01-20",
        "Total transmission line length across the 11 projects.",
    ),
    (
        PROGRAMME_ID, SOURCE_ESDM, "design capacity", "1,740 MVA", "2025-01-20",
        "Total substation capacity across the 11 projects.",
    ),
]


def project_row(item: dict, grid: bool) -> dict:
    return {
        "id": item["id"],
        "name": item["name"],
        "sector": "energy",
        "subsector": "transmission" if grid else item["subsector"],
        "status": "recently_completed",
        "status_basis": STATUS_GRID if grid else STATUS_GEN,
        "corridor_id": "",
        "island": item["island"],
        "province": item["province"],
        "route": item["route"],
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "",
        "capacity": "" if grid else item.get("capacity", ""),
        "capacity_unit": "" if grid else item.get("capacity_unit", ""),
        "psn": "unknown",
        "opened_year": "2025",
        "opened_date": "2025-01-20",
        "expected_open_year": "",
        "status_as_of": "2025-01-20",
        "verification": "official",
        "lat": item["lat"],
        "lon": item["lon"],
        "precision": item["precision"],
        "last_verified": REVIEWED,
        "notes": item["notes"],
    }


def main() -> None:
    sources = read_csv(CURATED / "sources.csv")
    existing_sources = {row["id"] for row in sources}
    for source in NEW_SOURCES:
        if source["id"] not in existing_sources:
            sources.append(dict(source))
            existing_sources.add(source["id"])
    sources.sort(key=lambda row: row["id"])
    write_csv(CURATED / "sources.csv", SOURCE_FIELDS, sources)

    projects = read_csv(CURATED / "projects.csv")
    existing_projects = {row["id"] for row in projects}
    new_rows = []
    for item in GEN:
        if item["id"] not in existing_projects:
            new_rows.append(project_row(item, grid=False))
            existing_projects.add(item["id"])
    for item in GRID:
        if item["id"] not in existing_projects:
            new_rows.append(project_row(item, grid=True))
            existing_projects.add(item["id"])
    projects.extend(new_rows)
    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)

    claims = read_csv(CURATED / "project_sources.csv")
    claim_keys = {
        (row["project_id"], row["source_id"], row["claim"]) for row in claims
    }

    def add_claim(project_id: str, source: str, claim: str, value: str,
                  date: str, notes: str) -> None:
        key = (project_id, source, claim)
        if key in claim_keys:
            return
        claims.append(
            {
                "project_id": project_id,
                "source_id": source,
                "claim": claim,
                "claim_value": value,
                "claim_date": date,
                "notes": notes,
            }
        )
        claim_keys.add(key)

    for item in GEN:
        add_claim(
            item["id"], SOURCE_ESDM, "status", "recently_completed",
            "2025-01-20", "Inaugurated on 20 January 2025.",
        )
        add_claim(
            item["id"], SOURCE_ESDM, "location", item["route"],
            "2025-01-20", "",
        )
        add_claim(
            item["id"], SOURCE_ESDM, "opening", "2025-01-20",
            "2025-01-20", "Inauguration date.",
        )
        add_claim(
            item["id"], SOURCE_GNFI, "location", item["island"],
            "2025-01-26", "GNFI island grouping for the 26 plants.",
        )
        for source, claim, value, date, notes in item["extra"]:
            add_claim(item["id"], source, claim, value, date, notes)

    for item in GRID:
        add_claim(
            item["id"], SOURCE_ESDM, "status", "recently_completed",
            "2025-01-20", "Inaugurated on 20 January 2025.",
        )
        add_claim(
            item["id"], SOURCE_ESDM, "location", item["route"],
            "2025-01-20", "",
        )
        add_claim(
            item["id"], SOURCE_ESDM, "opening", "2025-01-20",
            "2025-01-20", "Inauguration date.",
        )
        add_claim(
            item["id"], SOURCE_ESDM, "operator", "PT PLN (Persero)",
            "2025-01-20",
            "PLN operates the transmission and substation network named in "
            "the ESDM list.",
        )
        for source, claim, value, date, notes in item["extra"]:
            add_claim(item["id"], source, claim, value, date, notes)

    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)

    programme_links = read_csv(CURATED / "programme_projects.csv")
    link_keys = {
        (row["programme_id"], row["project_id"], row["role"])
        for row in programme_links
    }
    for item in GEN + GRID:
        key = (PROGRAMME_ID, item["id"], "component")
        if key in link_keys:
            continue
        programme_links.append(
            {
                "programme_id": PROGRAMME_ID,
                "project_id": item["id"],
                "role": "component",
                "source_id": SOURCE_ESDM,
                "notes": (
                    "One of the 37 strategic electricity projects inaugurated "
                    "on 20 January 2025."
                ),
            }
        )
        link_keys.add(key)
    write_csv(CURATED / "programme_projects.csv", PROGRAMME_PROJECT_FIELDS,
              programme_links)

    org_links = read_csv(CURATED / "project_organizations.csv")
    org_keys = {
        (row["project_id"], row["org_id"], row["role"]) for row in org_links
    }
    for item in GRID:
        key = (item["id"], ORG_PLN, "operator")
        if key in org_keys:
            continue
        org_links.append(
            {
                "project_id": item["id"],
                "org_id": ORG_PLN,
                "role": "operator",
                "share_pct": "",
                "start_year": "",
                "end_year": "",
                "source_id": SOURCE_ESDM,
                "notes": (
                    "PLN operates the transmission and substation network; "
                    "ESDM quotes PLN's commitment to manage the electricity "
                    "infrastructure."
                ),
            }
        )
        org_keys.add(key)
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS,
              org_links)

    aliases = read_csv(CURATED / "project_aliases.csv")
    alias_keys = {(row["project_id"], row["alias"]) for row in aliases}
    for item in GEN + GRID:
        key = (item["id"], item["alias"])
        if key not in alias_keys:
            aliases.append(
                {
                    "project_id": item["id"],
                    "alias": item["alias"],
                    "source_id": SOURCE_ESDM,
                    "notes": item.get("alias_notes", "Official ESDM list name."),
                }
            )
            alias_keys.add(key)
        if item.get("alias2"):
            key = (item["id"], item["alias2"])
            if key not in alias_keys:
                aliases.append(
                    {
                        "project_id": item["id"],
                        "alias": item["alias2"],
                        "source_id": item.get("alias2_source", ""),
                        "notes": item.get("alias2_notes", ""),
                    }
                )
                alias_keys.add(key)
    write_csv(CURATED / "project_aliases.csv", ALIAS_FIELDS, aliases)

    translations = read_csv(CURATED / "translations.csv")
    translation_keys = {
        (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        for row in translations
    }
    for item in GEN + GRID:
        key = ("project", item["id"], "name", "id")
        if key in translation_keys:
            continue
        translations.append(
            {
                "entity_type": "project",
                "entity_id": item["id"],
                "field": "name",
                "locale": "id",
                "text": item["name_id"],
                "status": "reviewed",
                "translator": "atlas-editor",
                "reviewed_on": REVIEWED,
                "source_id": SOURCE_ESDM,
            }
        )
        translation_keys.add(key)
    write_csv(CURATED / "translations.csv", TRANSLATION_FIELDS, translations)

    indicators = read_csv(CURATED / "indicators.csv")
    existing_indicators = {row["id"] for row in indicators}
    values = read_csv(CURATED / "indicator_values.csv")
    value_keys = {
        (row["indicator_id"], row["as_of"], row["source_id"]) for row in values
    }
    for (
        indicator_id, project_id, programme_id, name_en, name_id, unit,
        direction, value, as_of, source_id, notes,
    ) in INDICATORS:
        if indicator_id not in existing_indicators:
            indicators.append(
                {
                    "id": indicator_id,
                    "programme_id": programme_id,
                    "project_id": project_id,
                    "name_en": name_en,
                    "name_id": name_id,
                    "unit": unit,
                    "direction": direction,
                    "baseline_value": "",
                    "baseline_date": "",
                    "target_value": "",
                    "target_date": "",
                    "source_id": source_id,
                    "notes": notes,
                }
            )
            existing_indicators.add(indicator_id)
        key = (indicator_id, as_of, source_id)
        if key not in value_keys:
            values.append(
                {
                    "indicator_id": indicator_id,
                    "value": value,
                    "as_of": as_of,
                    "source_id": source_id,
                    "notes": "",
                }
            )
            value_keys.add(key)
    write_csv(CURATED / "indicators.csv", INDICATOR_FIELDS, indicators)
    write_csv(CURATED / "indicator_values.csv", INDICATOR_VALUE_FIELDS, values)

    programme_claims = read_csv(CURATED / "programme_sources.csv")
    programme_keys = {
        (row["programme_id"], row["source_id"], row["claim"])
        for row in programme_claims
    }
    for programme_id, source_id, claim, value, date, notes in PROGRAMME_CLAIMS:
        key = (programme_id, source_id, claim)
        if key in programme_keys:
            continue
        programme_claims.append(
            {
                "programme_id": programme_id,
                "source_id": source_id,
                "claim": claim,
                "claim_value": value,
                "claim_date": date,
                "notes": notes,
            }
        )
        programme_keys.add(key)
    write_csv(CURATED / "programme_sources.csv", PROGRAMME_SOURCE_FIELDS,
              programme_claims)

    coverage = read_csv(CURATED / "coverage_targets.csv")
    if not any(row["layer"] == "strategic_records" for row in coverage):
        row = {
            "layer": "strategic_records",
            "label": "Strategic and private records",
            "unit": "records",
            "target_count": "174",
            "reference_set": (
                "226 PSN records plus 174 strategic/private records = 400"
            ),
            "source_id": "",
            "notes": (
                "157 project rows outside the PSN list at 13 November 2026; 17 "
                "remain. The layer counts project rows with psn=no or "
                "psn=unknown, including 84 psn=no and 73 psn=unknown rows."
            ),
        }
        index = next(
            (
                i + 1 for i, target in enumerate(coverage)
                if target["layer"] == "psn_industrial_areas"
            ),
            len(coverage),
        )
        coverage.insert(index, row)
        write_csv(CURATED / "coverage_targets.csv", COVERAGE_FIELDS, coverage)

    print(
        f"Added {len(GEN) + len(GRID)} electricity projects, "
        f"{len(NEW_SOURCES)} sources, {len(INDICATORS)} indicators and "
        f"{len(PROGRAMME_CLAIMS)} programme claims (idempotent)."
    )


if __name__ == "__main__":
    main()
