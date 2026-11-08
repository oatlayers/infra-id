"""Add the remaining PSN road entries to the curated tables.

The PSN register has 12 road entries without an atlas row. Two are the
Bukittinggi-Padang and Pekanbaru-Bukittinggi components of the already-curated
Padang-Pekanbaru corridor, and one is the Tebing Tinggi-Parapat-Sibolga corridor
already partly represented by the Kuala Tanjung-Tebing Tinggi-Parapat row. The
other nine are new rows.

This script adds the nine rows, updates the existing Kuala Tanjung row's PSN
flag, and records dated claims, operators and investments. It does not try to
force a match where only a component exists; the ledger records that choice.

Run: python scripts/imports/add_psn_backlog_roads.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_psn_ledger.py
      python scripts/build_all.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CURATED,
    EVENT_FIELDS,
    INVESTMENT_FIELDS,
    ORG_FIELDS,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    SOURCE_FIELDS,
    read_csv,
    write_csv,
)

RETRIEVED = "2026-11-09"
LAST_VERIFIED = "2026-11-09"

SOURCES = [
    {
        "id": "src-cnbc-trans-sumatra-remaining-2026-06-14",
        "publisher": "CNBC Indonesia",
        "title": "Prabowo Kebut Tol Trans Sumatra Lampung Tembus Aceh, Ini Rute Tersisa",
        "url": "https://www.cnbcindonesia.com/news/20260614124832-4-742692/prabowo-kebut-tol-trans-sumatra-lampung-tembus-aceh-ini-rute-tersisa",
        "published_on": "2026-06-14",
        "source_type": "secondary",
        "language": "id",
        "notes": "Lists the Trans Sumatra PSN routes still to be built, including Kisaran-Tebing Tinggi, Jambi-Rengat and Rengat-Pekanbaru.",
    },
    {
        "id": "src-binamarga-kisaran-tebing-tinggi",
        "publisher": "Direktorat Jenderal Bina Marga",
        "title": "The Trans Sumatra Toll Road can reduce traffic burden and road maintenance costs in Sumatra",
        "url": "https://binamarga.pu.go.id/index.php/berita/the-trans-sumatra-toll-road-can-reduce-traffic-burden-and-road-maintenance-costs-in-sumatra",
        "published_on": "",
        "source_type": "official",
        "language": "en",
        "notes": "Records the Kisaran-Tebing Tinggi Phase I length of 39.68 km.",
    },
    {
        "id": "src-antara-jambi-rengat-2026-09-29",
        "publisher": "ANTARA News",
        "title": "Pemprov Jambi telah menuntaskan penetapan lokasi Tol Jambi-Rengat",
        "url": "https://www.antaranews.com/berita/5763044/pemprov-jambi-telah-menuntaskan-penetapan-lokasi-tol-jambi-rengat",
        "published_on": "2026-09-29",
        "source_type": "secondary",
        "language": "id",
        "notes": "Location determination complete; land acquisition targeted December 2026 and construction from 2027.",
    },
    {
        "id": "src-simpul-kpbu-jambi-rengat",
        "publisher": "Direktorat Jenderal Pembiayaan Infrastruktur, Kementerian Pekerjaan Umum",
        "title": "Jalan Tol Jambi-Rengat",
        "url": "https://simpulkpbu.pu.go.id/proyek/jalan-tol-jambi-rengat-2-1",
        "published_on": "",
        "source_type": "official",
        "language": "id",
        "notes": "198.13 km, Rp49.60T and three phases; phase 1 Sp. Ness-Merlung is 67.45 km.",
    },
    {
        "id": "src-antara-pekanbaru-ring-road-2026-07-08",
        "publisher": "ANTARA News",
        "title": "HKI: Progres pembangunan Proyek Tol Lingkar Pekanbaru capai 77 persen",
        "url": "https://m.antaranews.com/berita/5640339/hki-progres-pembangunan-proyek-tol-lingkar-pekanbaru-capai-77-persen",
        "published_on": "2026-07-08",
        "source_type": "secondary",
        "language": "id",
        "notes": "Pekanbaru ring-road section 77% complete at end-June 2026; completion target February 2027.",
    },
    {
        "id": "src-simpul-kpbu-rengat-pekanbaru",
        "publisher": "Direktorat Jenderal Pembiayaan Infrastruktur, Kementerian Pekerjaan Umum",
        "title": "Jalan Tol Rengat-Pekanbaru",
        "url": "https://simpulkpbu.pu.go.id/proyek/jalan-tol-rengat-pekanbaru-2-1",
        "published_on": "",
        "source_type": "official",
        "language": "id",
        "notes": "206.67 km and Rp41.36T.",
    },
    {
        "id": "src-jasamarga-serpong-cinere",
        "publisher": "PT Jasa Marga (Persero) Tbk",
        "title": "Tol Serpong-Cinere",
        "url": "https://www.jasamarga.com/jalan-tol/jasa-marga-metropolitan/ruas-tol/c83c724a-28af-4f90-8827-6c306d02edeb",
        "published_on": "",
        "source_type": "company",
        "language": "id",
        "notes": "10.14 km across two sections; both sections operate and are managed by PT Cinere Serpong Jaya.",
    },
    {
        "id": "src-cnbc-serpong-cinere-2024-01-09",
        "publisher": "CNBC Indonesia",
        "title": "Akhirnya Bentar Lagi Tersambung Penuh, Ini Dia 6 Ruas Tol JORR 2",
        "url": "https://www.cnbcindonesia.com/news/20240109165500-4-504207/akhirnya-bentar-lagi-tersambung-penuh-ini-dia-6-ruas-tol-jorr-2",
        "published_on": "2024-01-09",
        "source_type": "secondary",
        "language": "id",
        "notes": "Serpong-Cinere Section II Pamulang-Cinere opened on 8 January 2024.",
    },
    {
        "id": "src-bpjt-cimanggis-cibitung-2024-07-11",
        "publisher": "Badan Pengatur Jalan Tol",
        "title": "Sederet Fakta tentang Jalan Tol Cimanggis-Cibitung yang Sudah Beroperasi Penuh",
        "url": "https://bpjt.pu.go.id/sederet-fakta-tentang-jalan-tol-cimanggis-cibitung-yang-sudah-beroperasi-penuh",
        "published_on": "2024-07-11",
        "source_type": "official",
        "language": "id",
        "notes": "Full 26.18 km open after Section 2B Cikeas-Cibitung was completed.",
    },
    {
        "id": "src-voiceofasia-teluk-lamong-2026-06-29",
        "publisher": "Voice of Asia",
        "title": "Fisik Rampung 100%, Pelindo Sinergi Lokaseva Group Kawal Persiapan Pra-Operasi Fly Over Teluk Lamong",
        "url": "https://voiceofasean.com/newsroom/fisik-rampung-100-pelindo-sinergi-lokaseva-group-kawal-persiapan-pra-operasi-fly-over-teluk-lamong-untuk-kelancaran-logistik-jawa-timur/",
        "published_on": "2026-06-29",
        "source_type": "secondary",
        "language": "id",
        "notes": "Physical works 100% complete; pre-operational preparation continues.",
    },
    {
        "id": "src-sinfra-teluk-lamong",
        "publisher": "Sistem Informasi Infrastruktur Provinsi Jawa Timur",
        "title": "Pembangunan Fly Over dari dan Menuju Terminal Teluk Lamong",
        "url": "https://sinfra.jatimprov.go.id/proyek/pembangunan-fly-over-dari-dan-menuju-terminal-teluk-lamong-443",
        "published_on": "",
        "source_type": "official",
        "language": "id",
        "notes": "2.4 km with 0.45 km elevated; status complete; coordinates 112.674159, -7.198103.",
    },
    {
        "id": "src-binamarga-patimban-2026-06-09",
        "publisher": "Balai Besar Pelaksanaan Jalan Nasional DKI Jakarta - Jawa Barat",
        "title": "Tol Akses Patimban Capai 68 Persen, Pemerintah Percepat Konektivitas Logistik Nasional",
        "url": "https://binamarga.pu.go.id/balai-dki-jabar/berita/tol-akses-patimban-capai-68-persen-pemerintah-percepat-konektivitas-logistik-nasional",
        "published_on": "2026-06-09",
        "source_type": "official",
        "language": "id",
        "notes": "68% physical progress on the 22.94 km government section; package progress 58-74%.",
    },
    {
        "id": "src-bisnis-patimban-2026-09-08",
        "publisher": "Bisnis Indonesia",
        "title": "Tol Akses Patimban Jadi Katalis SSIA Kerek Nilai Lahan Subang Smartpolitan",
        "url": "https://market.bisnis.com/read/20260908/192/2002479/tol-akses-patimban-jadi-katalis-ssia-kerek-nilai-lahan-subang-smartpolitan",
        "published_on": "2026-09-08",
        "source_type": "secondary",
        "language": "id",
        "notes": "37.05 km total: 22.94 km government and 14.11 km BUJT; target completion 2027.",
    },
    {
        "id": "src-cnbc-npea-2026-06-27",
        "publisher": "CNBC Indonesia",
        "title": "Tanjung Priok Bakal Dilewati 2 Tol Baru, Ini Rutenya",
        "url": "https://www.cnbcindonesia.com/news/20260627132427-4-746194/tanjung-priok-bakal-dilewati-2-tol-baru-ini-rutenya",
        "published_on": "2026-06-27",
        "source_type": "secondary",
        "language": "id",
        "notes": "NPEA Section I 2.78 km; six-lane cross-section; links Kalibaru to Cibitung-Cilincing.",
    },
    {
        "id": "src-wikabeton-npea-2026-07-03",
        "publisher": "PT Wijaya Karya Beton Tbk",
        "title": "Konektivitas Logistik Makin Lancar, WIKA Beton Suplai Material Proyek NPEA",
        "url": "https://www.wika-beton.co.id/berita/konektivitas-logistik-makin-lancar-wika-beton-suplai-material-proyek-npea",
        "published_on": "2026-07-03",
        "source_type": "company",
        "language": "id",
        "notes": "Construction started in 2025; operation targeted for 2027.",
    },
    {
        "id": "src-tribunjabar-bandung-toll-2026-06-18",
        "publisher": "Tribun Jabar",
        "title": "13 Tol di Jabar Masuk Skala Prioritas PSN, Proyek Getaci hingga Tol Dalam Kota Bandung Dikebut",
        "url": "https://jabar.tribunnews.com/metro-bandung/1176082/daftar-13-jalan-tol-baru-di-jabar-yang-bakal-dikebut-era-prabowo-jawa-barat-jadi-primadona-psn",
        "published_on": "2026-06-18",
        "source_type": "secondary",
        "language": "id",
        "notes": "No physical construction yet for the North-South Link or Bandung Inter Urban Toll Road.",
    },
    {
        "id": "src-cnbc-bandung-toll-2025-08-10",
        "publisher": "CNBC Indonesia",
        "title": "Bandung Macet Minta Ampun, Nasib Proyek Tol Dalam Kota Begini",
        "url": "https://www.cnbcindonesia.com/news/20250730202647-4-653716/bandung-macet-minta-ampun-nasib-proyek-tol-dalam-kota-begini",
        "published_on": "2025-08-10",
        "source_type": "secondary",
        "language": "id",
        "notes": "27.3 km and Rp7.83T; Pasteur-Pasupati-Gasibu-Cileunyi route still under review.",
    },
]


def project(**row: str) -> dict[str, str]:
    record = {field: "" for field in PROJECT_FIELDS}
    record.update(row)
    return record


PROJECTS = [
    project(
        id="tol-kisaran-tebing-tinggi",
        name="Kisaran–Tebing Tinggi Toll Road",
        sector="road",
        subsector="toll",
        status="planned",
        status_basis="Listed among the Trans Sumatra routes still to be built in June 2026; Phase I is 39.68 km and land acquisition is still being prepared.",
        corridor_id="trans-sumatera",
        island="Sumatra",
        province="North Sumatra",
        route="Kisaran–Tebing Tinggi",
        length_km="39.68",
        psn="yes",
        status_as_of="2026-06-14",
        verification="dual",
        lat="3.15",
        lon="99.40",
        precision="regency",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 7. The missing link between the operating Indrapura–Kisaran section and the Kuala Tanjung–Tebing Tinggi corridor. The 39.68 km figure is the Phase I length.",
    ),
    project(
        id="tol-jambi-rengat",
        name="Jambi–Rengat Toll Road",
        sector="road",
        subsector="toll",
        status="planned",
        status_basis="Location determination completed in 2026; land acquisition targeted for December 2026 and physical construction from 2027.",
        corridor_id="trans-sumatera",
        island="Sumatra",
        province="Jambi; Riau",
        route="Jambi–Rengat",
        length_km="198.13",
        investment_idr_t="49.6",
        psn="yes",
        status_as_of="2026-09-29",
        verification="dual",
        lat="-1.00",
        lon="103.00",
        precision="regency",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 14. Three phases; phase 1 Sp. Ness–Merlung is 67.45 km. The PU KPBU page gives Rp49.60T and 198.13 km. AIIB and IsDB are indicated financiers.",
    ),
    project(
        id="tol-rengat-pekanbaru",
        name="Rengat–Pekanbaru Toll Road",
        sector="road",
        subsector="toll",
        status="under_construction",
        status_basis="Pekanbaru ring-road section 77% complete in June 2026 and targeted for February 2027; the Rengat–Kampar and Kampar–Pekanbaru sections remain in planning and land acquisition.",
        corridor_id="trans-sumatera",
        island="Sumatra",
        province="Riau",
        route="Rengat–Pekanbaru",
        length_km="206.67",
        construction_km="30.5",
        investment_idr_t="41.36",
        psn="yes",
        status_as_of="2026-07-08",
        verification="dual",
        lat="0.05",
        lon="101.98",
        precision="regency",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 15. 206.67 km per the PU KPBU page; other plans give 175 km. The 30.5 km Pekanbaru ring-road section is part of the corridor and was 77% complete in June 2026.",
    ),
    project(
        id="tol-serpong-cinere",
        name="Serpong–Cinere Toll Road",
        sector="road",
        subsector="toll",
        status="operating",
        status_basis="Fully open since 8 January 2024; 10.14 km across two sections.",
        island="Java",
        province="Banten; West Java",
        route="Serpong–Pamulang–Cinere",
        length_km="10.14",
        operational_km="10.14",
        psn="yes",
        opened_year="2024",
        opened_date="2024-01-08",
        status_as_of="2026-11-09",
        verification="dual",
        lat="-6.35",
        lon="106.75",
        precision="approximate",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 22. JORR 2 link: Section I Serpong–Pamulang 6.5 km and Section II Pamulang–Cinere 3.64 km. Operated by PT Cinere Serpong Jaya.",
    ),
    project(
        id="tol-cimanggis-cibitung",
        name="Cimanggis–Cibitung Toll Road",
        sector="road",
        subsector="toll",
        status="operating",
        status_basis="Fully open since July 2024; 26.18 km.",
        island="Java",
        province="West Java",
        route="Cimanggis–Cikeas–Cibitung",
        length_km="26.18",
        operational_km="26.18",
        psn="yes",
        opened_year="2024",
        opened_date="2024-07-11",
        status_as_of="2024-07-11",
        verification="official",
        lat="-6.37",
        lon="106.95",
        precision="approximate",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 24. Final JORR 2 link, connecting Jagorawi and the Jakarta–Cikampek corridor. Operated by PT Cimanggis Cibitung Tollways.",
    ),
    project(
        id="flyover-teluk-lamong",
        name="Teluk Lamong Flyover",
        sector="road",
        subsector="flyover",
        status="under_construction",
        status_basis="Physical works 100% complete by June 2026; operational handover still in preparation.",
        island="Java",
        province="East Java",
        route="Tambak Osowilangun and Romokalisari, Surabaya",
        length_km="2.4",
        psn="yes",
        status_as_of="2026-06-29",
        verification="dual",
        lat="-7.198103",
        lon="112.674160",
        precision="exact",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 40. 2.4 km including 0.45 km elevated; connects Terminal Teluk Lamong to the Surabaya–Gresik toll road, the GBT access road and the west outer ring road.",
    ),
    project(
        id="tol-akses-patimban",
        name="Patimban Port Access Toll Road",
        sector="road",
        subsector="port_access",
        status="under_construction",
        status_basis="68% physical progress in June 2026; government packages 58–74% and the 14.11 km BUJT section 14%.",
        island="Java",
        province="West Java",
        route="Cikopo–Palimanan to Patimban Port",
        length_km="37.05",
        investment_idr_t="5.02",
        psn="yes",
        status_as_of="2026-06-09",
        verification="dual",
        lat="-6.35",
        lon="107.75",
        precision="approximate",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 46. 37.05 km total: 22.94 km government packages and 14.11 km BUJT. Target operation 2027; connects Cipali at Junction Cipeundeuy to Patimban.",
    ),
    project(
        id="tol-new-priok-eastern-access",
        name="New Priok Eastern Access (NPEA)",
        sector="road",
        subsector="port_access",
        status="under_construction",
        status_basis="Construction started in 2025; Section I 2.78 km and Section II 3.4 km under way, with operation targeted for 2027.",
        island="Java",
        province="DKI Jakarta",
        route="Kalibaru/New Priok to Cibitung–Cilincing",
        length_km="6.6",
        psn="yes",
        status_as_of="2026-07-03",
        verification="dual",
        lat="-6.10",
        lon="106.95",
        precision="approximate",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 48. Connects the Kalibaru container terminal to the Cibitung–Cilincing toll road. Section I is 2.78 km; Section II is about 3.4 km.",
    ),
    project(
        id="tol-bandung-inner-city",
        name="Bandung Inner City Toll Road",
        sector="road",
        subsector="urban_toll",
        status="planned",
        status_basis="No physical construction as of June 2026; route and financing are still under review.",
        island="Java",
        province="West Java",
        route="Pasteur–Pasupati–Gasibu–Cileunyi",
        length_km="27.3",
        investment_idr_t="7.83",
        psn="yes",
        status_as_of="2026-06-18",
        verification="dual",
        lat="-6.90",
        lon="107.62",
        precision="approximate",
        last_verified=LAST_VERIFIED,
        notes="PSN No. 50. Two components, the North–South Link and the Bandung Inter Urban Toll Road; Rp7.83T. The Pasteur–Pasupati–Gasibu–Cileunyi route is still being finalised.",
    ),
]

ORG_ROWS = [
    ("org-cinere-serpong-jaya", "PT Cinere Serpong Jaya", "CSJ", "private", "ID",
     "https://www.jasamarga.com", "Operator of the Serpong–Cinere toll road."),
    ("org-cimanggis-cibitung-tollways", "PT Cimanggis Cibitung Tollways", "CCT", "private", "ID",
     "", "Operator of the Cimanggis–Cibitung toll road."),
]

CLAIMS = [
    ("tol-kisaran-tebing-tinggi", "src-cnbc-trans-sumatra-remaining-2026-06-14", "status"),
    ("tol-kisaran-tebing-tinggi", "src-binamarga-kisaran-tebing-tinggi", "length"),
    ("tol-kisaran-tebing-tinggi", "src-cnbc-trans-sumatra-remaining-2026-06-14", "location"),
    ("tol-kisaran-tebing-tinggi", "src-binamarga-kisaran-tebing-tinggi", "operator"),
    ("tol-jambi-rengat", "src-antara-jambi-rengat-2026-09-29", "status"),
    ("tol-jambi-rengat", "src-simpul-kpbu-jambi-rengat", "length"),
    ("tol-jambi-rengat", "src-simpul-kpbu-jambi-rengat", "investment"),
    ("tol-jambi-rengat", "src-antara-jambi-rengat-2026-09-29", "location"),
    ("tol-jambi-rengat", "src-simpul-kpbu-jambi-rengat", "operator"),
    ("tol-rengat-pekanbaru", "src-antara-pekanbaru-ring-road-2026-07-08", "status"),
    ("tol-rengat-pekanbaru", "src-simpul-kpbu-rengat-pekanbaru", "length"),
    ("tol-rengat-pekanbaru", "src-simpul-kpbu-rengat-pekanbaru", "investment"),
    ("tol-rengat-pekanbaru", "src-antara-pekanbaru-ring-road-2026-07-08", "location"),
    ("tol-rengat-pekanbaru", "src-simpul-kpbu-rengat-pekanbaru", "operator"),
    ("tol-serpong-cinere", "src-jasamarga-serpong-cinere", "status"),
    ("tol-serpong-cinere", "src-jasamarga-serpong-cinere", "length"),
    ("tol-serpong-cinere", "src-jasamarga-serpong-cinere", "operational"),
    ("tol-serpong-cinere", "src-cnbc-serpong-cinere-2024-01-09", "opening"),
    ("tol-serpong-cinere", "src-jasamarga-serpong-cinere", "location"),
    ("tol-serpong-cinere", "src-jasamarga-serpong-cinere", "operator"),
    ("tol-cimanggis-cibitung", "src-bpjt-cimanggis-cibitung-2024-07-11", "status"),
    ("tol-cimanggis-cibitung", "src-bpjt-cimanggis-cibitung-2024-07-11", "length"),
    ("tol-cimanggis-cibitung", "src-bpjt-cimanggis-cibitung-2024-07-11", "operational"),
    ("tol-cimanggis-cibitung", "src-bpjt-cimanggis-cibitung-2024-07-11", "opening"),
    ("tol-cimanggis-cibitung", "src-bpjt-cimanggis-cibitung-2024-07-11", "location"),
    ("tol-cimanggis-cibitung", "src-bpjt-cimanggis-cibitung-2024-07-11", "operator"),
    ("flyover-teluk-lamong", "src-voiceofasia-teluk-lamong-2026-06-29", "status"),
    ("flyover-teluk-lamong", "src-sinfra-teluk-lamong", "length"),
    ("flyover-teluk-lamong", "src-sinfra-teluk-lamong", "location"),
    ("flyover-teluk-lamong", "src-sinfra-teluk-lamong", "operator"),
    ("tol-akses-patimban", "src-binamarga-patimban-2026-06-09", "status"),
    ("tol-akses-patimban", "src-bisnis-patimban-2026-09-08", "length"),
    ("tol-akses-patimban", "src-binamarga-patimban-2026-06-09", "investment"),
    ("tol-akses-patimban", "src-binamarga-patimban-2026-06-09", "location"),
    ("tol-new-priok-eastern-access", "src-cnbc-npea-2026-06-27", "status"),
    ("tol-new-priok-eastern-access", "src-cnbc-npea-2026-06-27", "length"),
    ("tol-new-priok-eastern-access", "src-wikabeton-npea-2026-07-03", "location"),
    ("tol-new-priok-eastern-access", "src-cnbc-npea-2026-06-27", "operator"),
    ("tol-bandung-inner-city", "src-tribunjabar-bandung-toll-2026-06-18", "status"),
    ("tol-bandung-inner-city", "src-cnbc-bandung-toll-2025-08-10", "length"),
    ("tol-bandung-inner-city", "src-cnbc-bandung-toll-2025-08-10", "investment"),
    ("tol-bandung-inner-city", "src-cnbc-bandung-toll-2025-08-10", "location"),
]

LINKS = [
    ("tol-kisaran-tebing-tinggi", "org-hutama-karya", "operator", "src-binamarga-kisaran-tebing-tinggi"),
    ("tol-jambi-rengat", "org-hutama-karya", "operator", "src-simpul-kpbu-jambi-rengat"),
    ("tol-rengat-pekanbaru", "org-hutama-karya", "operator", "src-simpul-kpbu-rengat-pekanbaru"),
    ("tol-serpong-cinere", "org-cinere-serpong-jaya", "operator", "src-jasamarga-serpong-cinere"),
    ("tol-cimanggis-cibitung", "org-cimanggis-cibitung-tollways", "operator", "src-bpjt-cimanggis-cibitung-2024-07-11"),
    ("flyover-teluk-lamong", "org-pelindo", "sponsor", "src-voiceofasia-teluk-lamong-2026-06-29"),
    ("flyover-teluk-lamong", "org-wijaya-karya", "contractor", "src-sinfra-teluk-lamong"),
    ("tol-akses-patimban", "org-kementerian-pu", "sponsor", "src-binamarga-patimban-2026-06-09"),
    ("tol-new-priok-eastern-access", "org-pelindo", "sponsor", "src-cnbc-npea-2026-06-27"),
    ("tol-new-priok-eastern-access", "org-hutama-karya", "contractor", "src-cnbc-npea-2026-06-27"),
    ("tol-new-priok-eastern-access", "org-pp", "contractor", "src-wikabeton-npea-2026-07-03"),
    ("tol-bandung-inner-city", "org-kementerian-pu", "sponsor", "src-tribunjabar-bandung-toll-2026-06-18"),
]

INVESTMENTS = [
    ("inv-jambi-rengat", "tol-jambi-rengat", "org-hutama-karya", "49.6", "IDR", "49.6", "2026", "announced", "mixed", "src-simpul-kpbu-jambi-rengat", "Project cost on the PU KPBU page; construction targeted from 2027."),
    ("inv-rengat-pekanbaru", "tol-rengat-pekanbaru", "org-hutama-karya", "41.36", "IDR", "41.36", "2026", "announced", "mixed", "src-simpul-kpbu-rengat-pekanbaru", "Project cost on the PU KPBU page."),
    ("inv-patimban-access", "tol-akses-patimban", "org-kementerian-pu", "5.02", "IDR", "5.02", "2026", "committed", "mixed", "src-binamarga-patimban-2026-06-09", "Government package cost; the 14.11 km BUJT section is financed separately."),
    ("inv-bandung-inner-toll", "tol-bandung-inner-city", "org-kementerian-pu", "7.83", "IDR", "7.83", "2026", "announced", "mixed", "src-cnbc-bandung-toll-2025-08-10", "Indicative project cost."),
]

EVENTS = [
    ("evt-serpong-cinere-opened", "tol-serpong-cinere", "2024-01-08", "opened",
     "Section II Pamulang–Cinere opened, completing the 10.14 km Serpong–Cinere link.",
     "src-cnbc-serpong-cinere-2024-01-09"),
    ("evt-cimanggis-cibitung-opened", "tol-cimanggis-cibitung", "2024-07-11", "opened",
     "Section 2B Cikeas–Cibitung completed, opening the full 26.18 km Cimanggis–Cibitung toll road.",
     "src-bpjt-cimanggis-cibitung-2024-07-11"),
]


def upsert(rows: list[dict[str, str]], incoming: dict[str, str], key: str = "id") -> None:
    for index, row in enumerate(rows):
        if row[key] == incoming[key]:
            rows[index] = incoming
            return
    rows.append(incoming)


def main() -> None:
    sources = read_csv(CURATED / "sources.csv")
    organizations = read_csv(CURATED / "organizations.csv")
    projects = read_csv(CURATED / "projects.csv")
    links = read_csv(CURATED / "project_organizations.csv")
    claims = read_csv(CURATED / "project_sources.csv")
    investments = read_csv(CURATED / "investments.csv")
    events = read_csv(CURATED / "project_events.csv")

    for source in SOURCES:
        row = {field: "" for field in SOURCE_FIELDS}
        row.update(source)
        row["retrieved_on"] = RETRIEVED
        upsert(sources, row)

    for org_id, name, short_name, org_type, country_code, website, notes in ORG_ROWS:
        upsert(
            organizations,
            {
                "id": org_id,
                "name": name,
                "short_name": short_name,
                "org_type": org_type,
                "country_code": country_code,
                "parent_id": "",
                "website": website,
                "notes": notes,
            },
        )

    new_ids = {row["id"] for row in PROJECTS}
    for row in PROJECTS:
        upsert(projects, row)

    # The Kuala Tanjung-Tebing Tinggi-Parapat row is the northern component of
    # PSN 12; mark it as a PSN row and keep the existing content.
    for row in projects:
        if row["id"] == "tol-kuala-tanjung-tebing-tinggi-parapat":
            row["psn"] = "yes"
            break

    links[:] = [row for row in links if row["project_id"] not in new_ids]
    claims[:] = [row for row in claims if row["project_id"] not in new_ids]
    investments[:] = [row for row in investments if row["project_id"] not in new_ids]
    events[:] = [row for row in events if row["project_id"] not in new_ids]

    for project_id, org_id, role, source_id in LINKS:
        links.append(
            {
                "project_id": project_id,
                "org_id": org_id,
                "role": role,
                "share_pct": "",
                "start_year": "",
                "end_year": "",
                "source_id": source_id,
                "notes": "",
            }
        )

    for project_id, source_id, claim in CLAIMS:
        claims.append(
            {
                "project_id": project_id,
                "source_id": source_id,
                "claim": claim,
                "claim_value": "",
                "claim_date": "",
                "notes": "",
            }
        )

    # Document the PSN flag change on the existing row.
    key = ("tol-kuala-tanjung-tebing-tinggi-parapat", "src-permenko-16-2025", "psn")
    if not any(
        (row["project_id"], row["source_id"], row["claim"]) == key for row in claims
    ):
        claims.append(
            {
                "project_id": key[0],
                "source_id": key[1],
                "claim": key[2],
                "claim_value": "",
                "claim_date": "",
                "notes": "The row covers the northern component of PSN 12.",
            }
        )

    for inv_id, project_id, org_id, amount, currency, amount_idr_t, year, stage, instrument, source_id, notes in INVESTMENTS:
        investments.append(
            {
                "id": inv_id,
                "project_id": project_id,
                "investor_org_id": org_id,
                "amount": amount,
                "currency": currency,
                "amount_idr_t": amount_idr_t,
                "fx_date": LAST_VERIFIED,
                "year": year,
                "stage": stage,
                "instrument": instrument,
                "share_pct": "",
                "source_id": source_id,
                "notes": notes,
            }
        )

    for event_id, project_id, event_date, event_type, description, source_id in EVENTS:
        events.append(
            {
                "id": event_id,
                "project_id": project_id,
                "event_date": event_date,
                "event_type": event_type,
                "description": description,
                "source_id": source_id,
                "notes": "",
            }
        )

    write_csv(CURATED / "sources.csv", SOURCE_FIELDS, sources)
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, organizations)
    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, links)
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)
    write_csv(CURATED / "investments.csv", INVESTMENT_FIELDS, investments)
    write_csv(CURATED / "project_events.csv", EVENT_FIELDS, events)

    print(
        f"OK: {len(PROJECTS)} PSN road rows, {len(SOURCES)} sources, "
        f"{len(ORG_ROWS)} organisations, {len(LINKS)} links, "
        f"{len(CLAIMS) + 1} claims, {len(INVESTMENTS)} investments, "
        f"{len(EVENTS)} events"
    )


if __name__ == "__main__":
    main()
