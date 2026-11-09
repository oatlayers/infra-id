"""Seed reviewed Indonesian names for the curated project rows.

The official PSN names for the 88 register-only rows already live in
``project_aliases.csv``. This script adds a reviewed Indonesian display name for
every other project. Where the name is a proper name, the Indonesian text is the
same as the source name; that is a reviewed decision, not a missing translation.
Where the source name uses a generic English descriptor (Toll Road, Airport,
Port, Railway, Dam, Smelter, Phase), the Indonesian form uses the standard
generic term while keeping the proper name.

This is a seed, not a translator. Later edits belong in ``translations.csv``.
The script is idempotent: it never replaces an existing row.

Run: python scripts/imports/add_project_name_translations.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_i18n.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import CURATED, TRANSLATION_FIELDS, read_csv, write_csv  # noqa: E402

REVIEWED = "2026-11-09"

NAMES = {
    # Roads and bridges
    "tol-sigli-banda-aceh": "Jalan Tol Sigli–Banda Aceh",
    "tol-binjai-langsa": "Jalan Tol Binjai–Langsa",
    "tol-padang-pekanbaru": "Jalan Tol Padang–Pekanbaru",
    "tol-bengkulu-lubuk-linggau": "Jalan Tol Bengkulu–Lubuk Linggau",
    "tol-kayu-agung-palembang-betung": "Jalan Tol Kayu Agung–Palembang–Betung",
    "tol-kuala-tanjung-tebing-tinggi-parapat": "Jalan Tol Kuala Tanjung–Tebing Tinggi–Parapat",
    "tol-betung-tempino-jambi": "Jalan Tol Betung–Tempino–Jambi",
    "tol-depok-antasari": "Jalan Tol Depok–Antasari",
    "tol-jakarta-inner-ring-road-2": "Jalan Tol Lingkar Dalam Jakarta 2 (6 Jalan Tol Dalam Kota)",
    "tol-bekasi-cawang-kampung-melayu": "Jalan Tol Bekasi–Cawang–Kampung Melayu",
    "tol-jakarta-harbour-road-2": "Jalan Tol Pelabuhan Jakarta 2",
    "tol-jakarta-cikampek-2-south": "Jalan Tol Jakarta–Cikampek II Selatan",
    "tol-bogor-ring-road": "Jalan Tol Lingkar Bogor",
    "tol-serang-panimbang": "Jalan Tol Serang–Panimbang",
    "tol-ciawi-sukabumi": "Jalan Tol Ciawi–Sukabumi",
    "tol-semarang-demak": "Jalan Tol Semarang–Demak",
    "tol-solo-yogyakarta-nyia": "Jalan Tol Solo–Yogyakarta–NYIA Kulon Progo",
    "tol-yogyakarta-bawen": "Jalan Tol Yogyakarta–Bawen",
    "tol-krian-legundi-bunder-manyar": "Jalan Tol Krian–Legundi–Bunder–Manyar",
    "tol-probolinggo-banyuwangi": "Jalan Tol Probolinggo–Banyuwangi",
    "tol-jorr-3": "Jalan Tol Lingkar Luar Jakarta 3",
    "tol-gedebage-tasikmalaya-cilacap": "Jalan Tol Gedebage–Tasikmalaya–Cilacap",
    "tol-demak-tuban": "Jalan Tol Demak–Tuban",
    "tol-semarang-kendal": "Jalan Tol Pelabuhan Semarang (Semarang–Kendal)",
    "tol-pejagan-tegal-cilacap": "Jalan Tol Pejagan/Tegal–Cilacap",
    "tol-cilacap-yogyakarta": "Jalan Tol Cilacap–Yogyakarta",
    "tol-gilimanuk-mengwi": "Jalan Tol Gilimanuk–Mengwi",
    "tol-simpang-indralaya-muara-enim": "Jalan Tol Simpang Indralaya–Muara Enim",
    "tol-serpong-balaraja": "Jalan Tol Serpong–Balaraja",
    "tol-cileunyi-sumedang-dawuan": "Jalan Tol Cileunyi–Sumedang–Dawuan",
    "tol-cibitung-cilincing": "Jalan Tol Cibitung–Cilincing",
    "tol-cengkareng-batu-ceper-kunciran": "Jalan Tol Cengkareng–Batu Ceper–Kunciran",
    "tol-pekanbaru-kandis-dumai": "Jalan Tol Pekanbaru–Kandis–Dumai",
    "tol-manado-bitung": "Jalan Tol Manado–Bitung",
    "tol-balikpapan-samarinda": "Jalan Tol Balikpapan–Samarinda",
    "tol-kunciran-serpong": "Jalan Tol Kunciran–Serpong",
    "tol-pasuruan-probolinggo": "Jalan Tol Pasuruan–Probolinggo",
    "tol-pandaan-malang": "Jalan Tol Pandaan–Malang",
    "tol-ngawi-kertosono-kediri": "Jalan Tol Ngawi–Kertosono–Kediri",
    "tol-medan-binjai": "Jalan Tol Medan–Binjai",
    "tol-akses-tanjung-priok": "Jalan Tol Akses Tanjung Priok",
    "tol-cinere-jagorawi": "Jalan Tol Cinere–Jagorawi",
    "tol-lhokseumawe-sigli": "Jalan Tol Lhokseumawe–Sigli",
    "tol-langsa-lhokseumawe": "Jalan Tol Langsa–Lhokseumawe",
    "tol-muara-enim-lubuk-linggau": "Jalan Tol Muara Enim–Lubuk Linggau",
    "tol-kisaran-tebing-tinggi": "Jalan Tol Kisaran–Tebing Tinggi",
    "tol-jambi-rengat": "Jalan Tol Jambi–Rengat",
    "tol-rengat-pekanbaru": "Jalan Tol Rengat–Pekanbaru",
    "tol-serpong-cinere": "Jalan Tol Serpong–Cinere",
    "tol-cimanggis-cibitung": "Jalan Tol Cimanggis–Cibitung",
    "flyover-teluk-lamong": "Flyover Teluk Lamong",
    "tol-akses-patimban": "Jalan Tol Akses Pelabuhan Patimban",
    "tol-new-priok-eastern-access": "Akses Timur Priok Baru (NPEA)",
    "tol-bandung-inner-city": "Jalan Tol Dalam Kota Bandung",
    # Airports
    "air-yogyakarta-international": "Bandar Udara Internasional Yogyakarta (YIA)",
    "air-komodo-labuan-bajo": "Bandar Udara Komodo – Labuan Bajo",
    "air-lombok-praya": "Bandar Udara Lombok Praya",
    "air-nabire": "Bandar Udara Baru Nabire",
    "air-siboru-fakfak": "Bandar Udara Siboru Fakfak",
    "air-kediri": "Bandar Udara Kediri (Dhoho)",
    "air-raja-haji-abdullah-karimun": "Bandar Udara Raja Haji Abdullah – Karimun",
    "air-nusantara-ikn": "Bandar Udara Internasional Nusantara (IVD)",
    # Seaports
    "port-kek-maloy": "Pelabuhan KEK Maloy",
    "port-labuan-bajo-multipurpose": "Terminal Multipurpose Labuan Bajo",
    "port-bitung": "Pelabuhan Hub Internasional Bitung",
    "port-kupang": "Pelabuhan Kupang",
    "port-kuala-tanjung": "Pelabuhan Hub Internasional Kuala Tanjung",
    "port-kijing": "Terminal Kijing",
    "port-sanur": "Pelabuhan Sanur",
    "port-likupang": "Pelabuhan Likupang",
    "port-makassar-new-port": "Pelabuhan Baru Makassar",
    "port-teluk-palu": "Pelabuhan Teluk Palu",
    "port-sorong": "Pelabuhan Sorong",
    "port-patimban": "Pelabuhan Patimban",
    "port-benoa": "Pelabuhan Benoa (BMTH)",
    "port-palembang-baru": "Pelabuhan Baru Palembang",
    "port-muaro-jambi": "Terminal Peti Kemas Muaro Jambi",
    # Railways
    "rail-lrt-sumsel": "LRT Sumatera Selatan",
    "rail-double-track-java-south": "Jalur Ganda Jawa Selatan",
    "rail-tebing-tinggi-kuala-tanjung": "Kereta Api Tebing Tinggi–Kuala Tanjung",
    "rail-yogyakarta-airport": "Kereta Api Bandara Yogyakarta",
    "rail-makassar-parepare": "Kereta Api Makassar–Parepare",
    "rail-lrt-jabodebek": "LRT Jabodebek",
    "rail-kcj-jakarta-bandung": "Kereta Cepat Jakarta–Bandung",
    "rail-rantau-prapat-kota-pinang": "Kereta Api Rantau Prapat–Kota Pinang",
    "rail-lahat-kertapati": "Kereta Api Logistik Lahat–Kertapati",
    "rail-kaltim-logistics": "Kereta Api Logistik Kalimantan Timur",
    "rail-mrt-jakarta-north-south": "MRT Jakarta Utara–Selatan",
    "rail-mrt-jakarta-east-west": "MRT Jakarta Timur–Barat",
    "rail-lrt-jakarta-velodrome-manggarai": "LRT Jakarta Velodrome–Manggarai",
    # Dams
    "dam-meninting": "Bendungan Meninting",
    "dam-keureuto": "Bendungan Keureuto",
    "dam-rukoh": "Bendungan Rukoh",
    "dam-jlantah": "Bendungan Jlantah",
    "dam-sidan": "Bendungan Sidan",
    # Energy
    "energy-masela-abadi-lng": "LNG Abadi Masela",
    "energy-plts-100gw-phase-1": "Program Surya 100 GWp – Tahap 1",
    "energy-hilirisasi-2-01-dumai-gasoline": "Hilirisasi Tahap II – Kilang Bensin Dumai",
    "energy-hilirisasi-2-02-cilacap-gasoline": "Hilirisasi Tahap II – Kilang Bensin Cilacap",
    "energy-hilirisasi-2-03-palaran-fuel-terminal": "Hilirisasi Tahap II – Terminal BBM Palaran",
    "energy-hilirisasi-2-04-biak-fuel-terminal": "Hilirisasi Tahap II – Terminal BBM Biak",
    "energy-hilirisasi-2-05-maumere-fuel-terminal": "Hilirisasi Tahap II – Terminal BBM Maumere",
    "energy-hilirisasi-2-06-tanjung-enim-dme": "Hilirisasi Tahap II – DME Tanjung Enim",
    # Factories and smelters
    "factory-freeport-manyar-smelter": "Smelter Tembaga Freeport Indonesia Manyar",
    "factory-pt-smelting-gresik": "Smelter Tembaga PT Smelting Gresik",
    "factory-amman-copper-smelter": "Smelter Tembaga Amman Mineral",
    "factory-vale-pomalaa-hpal": "Proyek HPAL Vale Pomalaa",
    "factory-vale-bahodopi-hpal": "Proyek HPAL Vale Bahodopi",
    "factory-vale-sorowako-hpal": "Proyek HPAL Vale Sorowako",
    "factory-sgar-mempawah": "SGAR Mempawah Borneo Alumina",
    "factory-inalum-kuala-tanjung": "Smelter Aluminium Inalum Kuala Tanjung",
    "factory-catl-cbl-karawang": "Pabrik Sel Baterai CATL-CBL Indonesia",
    "factory-lotte-line-cilegon": "Pabrik Etilena Baru Lotte Chemical Indonesia (LINE)",
    "factory-chandra-asri-cilegon": "Kompleks Petrokimia Chandra Asri Cilegon",
    "factory-hilirisasi-2-07-imip-stainless-steel": "Hilirisasi Tahap II – Baja Nirkarat IMIP",
    "factory-hilirisasi-2-08-cilegon-carbon-steel": "Hilirisasi Tahap II – Slab Baja Karbon Cilegon",
    "factory-hilirisasi-2-09-karawang-buton-asphalt": "Hilirisasi Tahap II – Aspal Buton Karawang",
    "factory-hilirisasi-2-10-gresik-copper-gold": "Hilirisasi Tahap II – Tembaga dan Emas Gresik",
    "factory-hilirisasi-2-11-sei-mangkei-oleofood": "Hilirisasi Tahap II – Oleofood dan Biodiesel Sei Mangkei",
    "factory-hilirisasi-2-12-central-maluku-nutmeg": "Hilirisasi Tahap II – Oleoresin Pala Maluku Tengah",
    "factory-hilirisasi-2-13-central-maluku-coconut": "Hilirisasi Tahap II – Kelapa Terpadu Maluku Tengah",
    # Urban and coastal
    "urban-ikn-phase-2": "IKN Tahap 2",
    "coastal-java-sea-wall": "Tanggul Laut Raksasa Jawa (Pantura)",
}


def main() -> None:
    projects = read_csv(CURATED / "projects.csv")
    translations = read_csv(CURATED / "translations.csv")
    existing = {
        (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        for row in translations
    }
    added = 0
    for project in projects:
        if project["verification"] == "unverified" and project["status"] == "unknown":
            continue
        key = ("project", project["id"], "name", "id")
        if key in existing:
            continue
        translations.append(
            {
                "entity_type": "project",
                "entity_id": project["id"],
                "field": "name",
                "locale": "id",
                "text": NAMES.get(project["id"], project["name"]),
                "status": "reviewed",
                "translator": "atlas-editor",
                "reviewed_on": REVIEWED,
                "source_id": "",
            }
        )
        existing.add(key)
        added += 1

    translations.sort(
        key=lambda row: (
            row["entity_type"], row["entity_id"], row["field"], row["locale"]
        )
    )
    write_csv(CURATED / "translations.csv", TRANSLATION_FIELDS, translations)
    print(f"OK: added {added} reviewed project names; {len(translations)} translation rows")


if __name__ == "__main__":
    main()
