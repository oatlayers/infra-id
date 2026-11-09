"""Add the first PSN industrial-area batch to the estate layer.

Eight active PSN industrial areas now have enough public information to enter
the atlas as estate records: Kuala Tanjung, Bantaeng, Pomalaa, Huali, Patimban,
NEMIE, Pulau Penebang and Alumina Toba. Six are in the official Kemenperin
industrial-estate directory with manager, regency and land area. Kuala Tanjung
and Bantaeng are added from official/company reporting because Kemenperin does
not list them.

The importer is deliberately explicit. It does not guess a missing area or
status: every row names the source that states its area, and status claims are
added only where a dated source supports them. Where a developer or regional
source gives a larger planning area than the Kemenperin licence, the difference
is recorded in the row notes rather than blended into one number.

Run: python scripts/imports/add_psn_industrial_estates.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_psn_ledger.py
      python scripts/build_all.py
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CURATED,
    ESTATE_FIELDS,
    ESTATE_SOURCE_FIELDS,
    ORG_FIELDS,
    ROOT,
    SOURCE_FIELDS,
    island_for,
    read_csv,
    write_csv,
)

RAW = ROOT / "data" / "raw" / "2026-11-09"
RETRIEVED = "2026-11-09"
LAST_VERIFIED = "2026-11-09"

SOURCES = [
    {
        "id": "src-kemenperin-kawasan-2026-11-09",
        "publisher": "Kementerian Perindustrian",
        "title": "Daftar Kawasan Industri",
        "url": "https://kemenperin.go.id/kawasan",
        "published_on": "",
        "retrieved_on": RETRIEVED,
        "source_type": "official",
        "language": "id",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/kemenperin_kawasan.html",
        "licence": "Government public data; check portal terms",
        "notes": "181 estates with manager, location and land area; used for six PSN industrial areas.",
    },
    {
        "id": "src-waspada-kikt-2024-12-19",
        "publisher": "Waspada",
        "title": "Sambut Tahun Baru, PLN UID Sumut Jalin Kerja Sama Optimalisasi Kelistrikan Di KIKT",
        "url": "https://www.waspada.id/artikel/sambut-tahun-baru-pln-uid-sumut-jalin-kerja-sama-optimalisasi-kelistrikan-di-kikt",
        "published_on": "2024-12-19",
        "retrieved_on": RETRIEVED,
        "source_type": "secondary",
        "language": "id",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/waspada_kuala_tanjung_2024.html",
        "licence": "News article; quoted in short excerpts",
        "notes": "KIKT covers 3,400 ha; PT Prima Pengembangan Kawasan; early phase land clearing, gate and basic infrastructure.",
    },
    {
        "id": "src-pelindo-kikt-2024-02-01",
        "publisher": "PT Pelabuhan Indonesia (Persero)",
        "title": "Pelindo Mulai Membangun Kawasan Industri Terintegrasi Pelabuhan di Kuala Tanjung",
        "url": "https://pelindo.co.id/media/download/559/pelindo-mulai-membangun-kawasan-industri-terintegrasi-pelabuhan-di-kuala-tanjung",
        "published_on": "2024-02-01",
        "retrieved_on": RETRIEVED,
        "source_type": "company",
        "language": "id",
        "accessed_via": "PDF download",
        "archive_path": "data/raw/2026-11-09/pelindo_kuala_tanjung_2024.pdf",
        "licence": "Company press release",
        "notes": "PT Prima Pengembangan Kawasan manages KIKT; 57 ha acquired; phase 1 land clearing and maturation.",
    },
    {
        "id": "src-dpn-patimban-2026-04-07",
        "publisher": "Dewan Pertahanan Nasional RI",
        "title": "DPN Tinjau Pengembangan Pelabuhan dan Kawasan Industri Patimban, Subang, Jawa Barat",
        "url": "https://www.dpn.go.id/dpn-tinjau-pengembangan-pelabuhan-dan-kawasan-industri-patimban-subang-jawa-barat",
        "published_on": "2026-04-07",
        "retrieved_on": RETRIEVED,
        "source_type": "official",
        "language": "id",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/dpn_patimban_2026.html",
        "licence": "Government public data; check portal terms",
        "notes": "PT Wahana Mitra Semesta manages the estate; land maturation, 1.2 km internal road and basic facilities.",
    },
    {
        "id": "src-rebana-patimban-2026",
        "publisher": "BP Rebana Metropolitan",
        "title": "Kawasan Industri Patimban Industrial Estate",
        "url": "https://www.rebana.id/en/ki/kawasan-industri-patimban-industrial-estate",
        "published_on": "",
        "retrieved_on": RETRIEVED,
        "source_type": "official",
        "language": "en",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/rebana_patimban_2026.html",
        "licence": "Government public data; check portal terms",
        "notes": "627.77 ha total area, land maturation and a proposed SEZ; used to record the wider planning-area figure.",
    },
    {
        "id": "src-indonesiana-bantaeng-2020-09-30",
        "publisher": "Indonesiana",
        "title": "Pesisir Bantaeng yang Diluluhlantakkan Industri Nikel",
        "url": "https://www.indonesiana.id/read/164450/pesisir-bantaeng-yang-diluluhlantakkan-industri-nikel",
        "published_on": "2020-09-30",
        "retrieved_on": RETRIEVED,
        "source_type": "secondary",
        "language": "id",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/indonesiana_bantaeng_2020.html",
        "licence": "Article; quoted in short excerpts",
        "notes": "KIBA covers 3,128 ha in Pa'jukukang; PT Bantaeng Sinergi Cemerlang manages it; 13 firms recorded by 2017.",
    },
    {
        "id": "src-warta-lutim-huali-2025-09-25",
        "publisher": "Pemerintah Kabupaten Luwu Timur",
        "title": "Pemkab Luwu Timur dan PT IHIP Teken Kerja Sama Pembangunan Kawasan Industri Terintegrasi",
        "url": "https://warta.luwutimurkab.go.id/2025/09/25/pemkab-luwu-timur-dan-pt-ihip-teken-kerja-sama-pembangunan-kawasan-industri-terintegrasi",
        "published_on": "2025-09-25",
        "retrieved_on": RETRIEVED,
        "source_type": "official",
        "language": "id",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/warta_lutim_huali_2025.html",
        "licence": "Government public data; check portal terms",
        "notes": "Construction to start after permits; nickel HPAL and pyrometallurgy; Malili, Luwu Timur.",
    },
    {
        "id": "src-neo-energy-nemie-2026",
        "publisher": "Neo Energy",
        "title": "NEMIE",
        "url": "https://neoenergy.co.id/nemie",
        "published_on": "",
        "retrieved_on": RETRIEVED,
        "source_type": "company",
        "language": "en",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/neo_energy_nemie_2026.html",
        "licence": "Company website",
        "notes": "4,758 ha green industrial park at the TAS mine mouth; two operational jetties; infrastructure target 2026.",
    },
    {
        "id": "src-antara-penebang-2026-08-20",
        "publisher": "ANTARA News Kalimantan Barat",
        "title": "Dua perusahaan di KIPP raih penghargaan dari Pemprov Kalbar",
        "url": "https://kalbar.antaranews.com/berita/710037/dua-perusahaan-di-kipp-raih-penghargaan-dari-pemprov-kalbar",
        "published_on": "2026-08-20",
        "retrieved_on": RETRIEVED,
        "source_type": "secondary",
        "language": "id",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/antara_penebang_2026-08-20.html",
        "licence": "News article; quoted in short excerpts",
        "notes": "KIPP expected to reach commercial production in 2027; PT Dharma Inti Bersama.",
    },
    {
        "id": "src-gem-alumina-toba-2026",
        "publisher": "Global Energy Monitor",
        "title": "PT Kalimantan Alumina Nusantara power station",
        "url": "https://www.gem.wiki/PT_Kalimantan_Alumina_Nusantara_power_station",
        "published_on": "",
        "retrieved_on": RETRIEVED,
        "source_type": "secondary",
        "language": "en",
        "accessed_via": "HTML page",
        "archive_path": "data/raw/2026-11-09/gem_alumina_toba_2026.html",
        "licence": "CC BY-SA; attribution required",
        "notes": "Captive power station under construction at Toba, Sanggau; coordinates -0.1238386, 109.9713147.",
    },
    {
        "id": "src-osm-nominatim-2026-11-09",
        "publisher": "OpenStreetMap contributors",
        "title": "Nominatim search results for PSN industrial areas",
        "url": "https://nominatim.openstreetmap.org/",
        "published_on": "",
        "retrieved_on": RETRIEVED,
        "source_type": "secondary",
        "language": "en",
        "accessed_via": "Nominatim API, one request per second",
        "archive_path": "data/derived/nominatim_psn_estates.json",
        "licence": "ODbL 1.0",
        "notes": "Approximate place or island points for seven PSN industrial areas; not estate boundaries.",
    },
]

ORGS = [
    ("org-prima-pengembangan-kawasan", "PT Prima Pengembangan Kawasan", "PPK", "soe", "https://pelindo.co.id", "Pelindo subsidiary managing Kawasan Industri Kuala Tanjung."),
    ("org-bantaeng-sinergi-cemerlang", "PT Bantaeng Sinergi Cemerlang (Perseroda)", "BSC", "soe", "", "Regional enterprise managing Kawasan Industri Bantaeng."),
    ("org-indonesia-pomalaa-industry-park", "PT Indonesia Pomalaa Industry Park", "IPIP", "consortium", "", "Joint-venture estate company at Pomalaa, Kolaka."),
    ("org-indonesia-huali-industry-park", "PT Indonesia Huali Industry Park", "IHIP", "private", "", "Developer of the Huali nickel industrial park in Luwu Timur."),
    ("org-wahana-mitra-semesta", "PT Wahana Mitra Semesta", "WMS", "private", "", "Manager of Patimban Industrial Estate."),
    ("org-morowali-industri-sejahtera", "PT Morowali Industri Sejahtera", "MIS", "private", "https://neoenergy.co.id", "Neo Energy subsidiary managing NEMIE."),
    ("org-dharma-inti-bersama", "PT Dharma Inti Bersama", "DIB", "private", "", "Harita Group company developing Pulau Penebang."),
    ("org-westerfield-alumina-indonesia", "PT Westerfield Alumina Indonesia", "WAI", "private", "", "Developer of the Alumina Toba industrial area."),
]

# id, PSN number, official name, source id, province, regency, lat, lon,
# precision, coordinate source, area_ha, developer org id, status, sector focus,
# website, notes.
ESTATES = [
    (
        "ki-kawasan-industri-kuala-tanjung",
        86,
        "Kawasan Industri Kuala Tanjung",
        "src-waspada-kikt-2024-12-19",
        "Sumatera Utara",
        "Kabupaten Batubara",
        "3.35960",
        "99.44993",
        "approximate",
        "osm",
        "3400",
        "org-prima-pengembangan-kawasan",
        "under_construction",
        "Port-linked industry; aluminium, palm oil, logistics",
        "",
        "PSN 86. KIKT is a port-linked estate managed by PT Prima Pengembangan Kawasan. "
        "The 3,400 ha figure is the planned area; 57 ha had been acquired by early 2024 "
        "and phase 1 was land clearing and basic infrastructure. The point is the Kuala "
        "Tanjung place, not the estate boundary.",
    ),
    (
        "ki-kawasan-industri-bantaeng",
        90,
        "Kawasan Industri Bantaeng",
        "src-indonesiana-bantaeng-2020-09-30",
        "Sulawesi Selatan",
        "Kabupaten Bantaeng",
        "-5.54841",
        "120.03105",
        "approximate",
        "osm",
        "3128",
        "org-bantaeng-sinergi-cemerlang",
        "operating",
        "Nickel smelting and metal processing",
        "",
        "PSN 90. KIBA covers 3,128 ha in Pa'jukukang and Gantarang Keke. "
        "PT Bantaeng Sinergi Cemerlang manages the estate; 13 firms and a Huadi "
        "nickel smelter were recorded by 2020. Current occupancy is not verified. "
        "The point is the Pa'jukukang district, not the estate boundary.",
    ),
    (
        "ki-indonesia-pomalaa-industry-park",
        104,
        "Kawasan Industri Indonesia Pomalaa Industry Park",
        "src-kemenperin-kawasan-2026-11-09",
        "Sulawesi Tenggara",
        "Kabupaten Kolaka",
        "-4.05000",
        "121.60000",
        "approximate",
        "osm",
        "686.00",
        "org-indonesia-pomalaa-industry-park",
        "under_construction",
        "Nickel HPAL and battery materials",
        "",
        "PSN 104. Kemenperin lists 686.00 ha in Kabupaten Kolaka. The estate hosts "
        "Vale's Pomalaa HPAL project, which was under construction at the end of 2025. "
        "The point is the Pomalaa village, not the estate boundary.",
    ),
    (
        "ki-indonesia-huali-industry-park",
        111,
        "Kawasan Industri Indonesia Huali Industry Park (IHIP)",
        "src-kemenperin-kawasan-2026-11-09",
        "Sulawesi Selatan",
        "Kabupaten Luwu Timur",
        "-2.61907",
        "121.11634",
        "approximate",
        "osm",
        "394.50",
        "org-indonesia-huali-industry-park",
        "under_construction",
        "Nickel HPAL and pyrometallurgy",
        "",
        "PSN 111. Kemenperin lists 394.50 ha in Kabupaten Luwu Timur. The developer "
        "was completing permits in September 2025 before construction; land clearing "
        "was reported in 2026. The point is Malili town, not the estate boundary.",
    ),
    (
        "ki-kawasan-industri-patimban-industrial-estate",
        115,
        "Kawasan Industri Patimban Industrial Estate",
        "src-kemenperin-kawasan-2026-11-09",
        "Jawa Barat",
        "Kabupaten Subang",
        "-6.25158",
        "107.87838",
        "approximate",
        "osm",
        "298.30",
        "org-wahana-mitra-semesta",
        "under_construction",
        "Automotive, electronics, petrochemicals and logistics",
        "",
        "PSN 115. Kemenperin lists 298.30 ha; the Rebana Metropolitan profile gives "
        "627.77 ha and the developer markets about 1,200 ha across the wider plan. "
        "The estate was still in land maturation in April 2026. The point is the "
        "Patimban port access road, not the estate boundary.",
    ),
    (
        "ki-neo-energy-morowali-industrial-estate",
        119,
        "Kawasan Industri Neo Energy Morowali Industrial Estate (NEMIE)",
        "src-kemenperin-kawasan-2026-11-09",
        "Sulawesi Tengah",
        "Kabupaten Morowali",
        "-3.01462",
        "122.22482",
        "approximate",
        "osm",
        "283.82",
        "org-morowali-industri-sejahtera",
        "under_construction",
        "Nickel HPAL and battery materials",
        "https://neoenergy.co.id/nemie",
        "PSN 119. Kemenperin lists 283.82 ha; Neo Energy describes a 4,758 ha green "
        "industrial park at the TAS mine mouth. Groundbreaking took place in 2024 and "
        "the first infrastructure was targeted for 2026. The point is Buleleng village, "
        "not the estate boundary.",
    ),
    (
        "ki-kawasan-industri-pulau-penebang",
        125,
        "Kawasan Industri Pulau Penebang",
        "src-kemenperin-kawasan-2026-11-09",
        "Kalimantan Barat",
        "Kabupaten Kayong Utara",
        "-1.21286",
        "109.24885",
        "approximate",
        "osm",
        "1476.30",
        "org-dharma-inti-bersama",
        "under_construction",
        "Bauxite, alumina and aluminium",
        "",
        "PSN 125. Kemenperin lists 1,476.30 ha on Penebang Island, Kayong Utara. "
        "Commercial production is targeted for 2027-2028 and the project was still "
        "under construction in 2026. The point is Penebang Island, not the estate boundary.",
    ),
    (
        "ki-kawasan-industri-alumina-toba",
        127,
        "Kawasan Industri Alumina Toba",
        "src-kemenperin-kawasan-2026-11-09",
        "Kalimantan Barat",
        "Kabupaten Sanggau",
        "-0.12384",
        "109.97131",
        "approximate",
        "manual",
        "724.70",
        "org-westerfield-alumina-indonesia",
        "under_construction",
        "Alumina refining",
        "",
        "PSN 127. Kemenperin lists 724.70 ha in Kabupaten Sanggau. The associated "
        "captive power station is under construction; the estate's own construction "
        "status is not separately stated. The point is the power-station site, not the "
        "estate boundary.",
    ),
]

# One atomic claim per source link. The area itself is carried by the estate's
# source_id; the claim register records the other dated facts.
CLAIMS = [
    # Kuala Tanjung
    ("ki-kawasan-industri-kuala-tanjung", "src-permenko-16-2025", "psn", "PSN 86", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-kawasan-industri-kuala-tanjung", "src-pelindo-kikt-2024-02-01", "location", "Kabupaten Batubara, Sumatera Utara", "2024-02-01", ""),
    ("ki-kawasan-industri-kuala-tanjung", "src-pelindo-kikt-2024-02-01", "operator", "PT Prima Pengembangan Kawasan", "2024-02-01", ""),
    ("ki-kawasan-industri-kuala-tanjung", "src-waspada-kikt-2024-12-19", "status", "under_construction", "2024-12-19", "Early phase land clearing, gate and basic infrastructure."),
    ("ki-kawasan-industri-kuala-tanjung", "src-osm-nominatim-2026-11-09", "coordinates", "3.35960, 99.44993", "2026-11-09", "Kuala Tanjung place point; approximate."),
    # Bantaeng
    ("ki-kawasan-industri-bantaeng", "src-permenko-16-2025", "psn", "PSN 90", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-kawasan-industri-bantaeng", "src-indonesiana-bantaeng-2020-09-30", "location", "Kecamatan Pa'jukukang, Kabupaten Bantaeng, Sulawesi Selatan", "2020-09-30", ""),
    ("ki-kawasan-industri-bantaeng", "src-indonesiana-bantaeng-2020-09-30", "operator", "PT Bantaeng Sinergi Cemerlang", "2020-09-30", ""),
    ("ki-kawasan-industri-bantaeng", "src-indonesiana-bantaeng-2020-09-30", "status", "operating", "2020-09-30", "13 firms and a Huadi nickel smelter recorded."),
    ("ki-kawasan-industri-bantaeng", "src-osm-nominatim-2026-11-09", "coordinates", "-5.54841, 120.03105", "2026-11-09", "Pa'jukukang district point; approximate."),
    # Pomalaa
    ("ki-indonesia-pomalaa-industry-park", "src-permenko-16-2025", "psn", "PSN 104", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-indonesia-pomalaa-industry-park", "src-kemenperin-kawasan-2026-11-09", "location", "Kabupaten Kolaka, Sulawesi Tenggara", "2026-11-09", ""),
    ("ki-indonesia-pomalaa-industry-park", "src-kemenperin-kawasan-2026-11-09", "operator", "PT Indonesia Pomalaa Industry Park", "2026-11-09", ""),
    ("ki-indonesia-pomalaa-industry-park", "src-vale-pomalaa-2025-12-13", "status", "under_construction", "2025-12-13", "Pomalaa HPAL project; first autoclaves received."),
    ("ki-indonesia-pomalaa-industry-park", "src-osm-nominatim-2026-11-09", "coordinates", "-4.05000, 121.60000", "2026-11-09", "Pomalaa village point; approximate."),
    # Huali
    ("ki-indonesia-huali-industry-park", "src-permenko-16-2025", "psn", "PSN 111", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-indonesia-huali-industry-park", "src-kemenperin-kawasan-2026-11-09", "location", "Kabupaten Luwu Timur, Sulawesi Selatan", "2026-11-09", ""),
    ("ki-indonesia-huali-industry-park", "src-kemenperin-kawasan-2026-11-09", "operator", "PT Indonesia Huali Industry Park", "2026-11-09", ""),
    ("ki-indonesia-huali-industry-park", "src-warta-lutim-huali-2025-09-25", "status", "under_construction", "2025-09-25", "Permits being completed before construction."),
    ("ki-indonesia-huali-industry-park", "src-osm-nominatim-2026-11-09", "coordinates", "-2.61907, 121.11634", "2026-11-09", "Malili town point; approximate."),
    # Patimban
    ("ki-kawasan-industri-patimban-industrial-estate", "src-permenko-16-2025", "psn", "PSN 115", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-kawasan-industri-patimban-industrial-estate", "src-kemenperin-kawasan-2026-11-09", "location", "Kabupaten Subang, Jawa Barat", "2026-11-09", ""),
    ("ki-kawasan-industri-patimban-industrial-estate", "src-kemenperin-kawasan-2026-11-09", "operator", "PT Wahana Mitra Semesta", "2026-11-09", ""),
    ("ki-kawasan-industri-patimban-industrial-estate", "src-dpn-patimban-2026-04-07", "status", "under_construction", "2026-04-07", "Land maturation, 1.2 km internal road and basic facilities."),
    ("ki-kawasan-industri-patimban-industrial-estate", "src-rebana-patimban-2026", "status", "under_construction", "2026-11-09", "Land maturation and proposed SEZ."),
    ("ki-kawasan-industri-patimban-industrial-estate", "src-osm-nominatim-2026-11-09", "coordinates", "-6.25158, 107.87838", "2026-11-09", "Patimban port access road point; approximate."),
    # NEMIE
    ("ki-neo-energy-morowali-industrial-estate", "src-permenko-16-2025", "psn", "PSN 119", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-neo-energy-morowali-industrial-estate", "src-kemenperin-kawasan-2026-11-09", "location", "Kabupaten Morowali, Sulawesi Tengah", "2026-11-09", ""),
    ("ki-neo-energy-morowali-industrial-estate", "src-kemenperin-kawasan-2026-11-09", "operator", "PT Morowali Industri Sejahtera", "2026-11-09", ""),
    ("ki-neo-energy-morowali-industrial-estate", "src-neo-energy-nemie-2026", "status", "under_construction", "2026-11-09", "Groundbreaking 2024; infrastructure target 2026."),
    ("ki-neo-energy-morowali-industrial-estate", "src-osm-nominatim-2026-11-09", "coordinates", "-3.01462, 122.22482", "2026-11-09", "Buleleng village point; approximate."),
    # Pulau Penebang
    ("ki-kawasan-industri-pulau-penebang", "src-permenko-16-2025", "psn", "PSN 125", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-kawasan-industri-pulau-penebang", "src-kemenperin-kawasan-2026-11-09", "location", "Kabupaten Kayong Utara, Kalimantan Barat", "2026-11-09", ""),
    ("ki-kawasan-industri-pulau-penebang", "src-kemenperin-kawasan-2026-11-09", "operator", "PT Dharma Inti Bersama", "2026-11-09", ""),
    ("ki-kawasan-industri-pulau-penebang", "src-antara-penebang-2026-08-20", "status", "under_construction", "2026-08-20", "Commercial production targeted for 2027."),
    ("ki-kawasan-industri-pulau-penebang", "src-osm-nominatim-2026-11-09", "coordinates", "-1.21286, 109.24885", "2026-11-09", "Penebang Island point; approximate."),
    # Alumina Toba
    ("ki-kawasan-industri-alumina-toba", "src-permenko-16-2025", "psn", "PSN 127", "2025-09-24", "Permenko 16/2025 annex."),
    ("ki-kawasan-industri-alumina-toba", "src-kemenperin-kawasan-2026-11-09", "location", "Kabupaten Sanggau, Kalimantan Barat", "2026-11-09", ""),
    ("ki-kawasan-industri-alumina-toba", "src-kemenperin-kawasan-2026-11-09", "operator", "PT Westerfield Alumina Indonesia", "2026-11-09", ""),
    ("ki-kawasan-industri-alumina-toba", "src-gem-alumina-toba-2026", "status", "under_construction", "2026-10-31", "Associated captive power station under construction."),
    ("ki-kawasan-industri-alumina-toba", "src-gem-alumina-toba-2026", "coordinates", "-0.12384, 109.97131", "2026-10-31", "Power-station point; approximate for the estate."),
]


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upsert(rows: list[dict[str, str]], key: str, incoming: dict[str, str]) -> None:
    for index, row in enumerate(rows):
        if row[key] == incoming[key]:
            rows[index] = incoming
            return
    rows.append(incoming)


def main() -> None:
    sources = read_csv(CURATED / "sources.csv")
    organizations = read_csv(CURATED / "organizations.csv")
    estates = read_csv(CURATED / "estates.csv")
    claims = read_csv(CURATED / "estate_sources.csv")

    source_ids = {row["id"] for row in sources}
    for partial in SOURCES:
        row = {field: "" for field in SOURCE_FIELDS}
        row.update(partial)
        archive = ROOT / row["archive_path"] if row["archive_path"] else None
        if archive and archive.exists():
            row["snapshot_hash"] = file_hash(archive)
        upsert(sources, "id", row)
        source_ids.add(row["id"])

    org_ids = {row["id"] for row in organizations}
    for org_id, name, short_name, org_type, website, notes in ORGS:
        row = {field: "" for field in ORG_FIELDS}
        row.update(
            {
                "id": org_id,
                "name": name,
                "short_name": short_name,
                "org_type": org_type,
                "country_code": "ID",
                "parent_id": "",
                "website": website,
                "notes": notes,
            }
        )
        upsert(organizations, "id", row)
        org_ids.add(org_id)

    managed_ids = set()
    for (
        estate_id,
        psn_no,
        official_name,
        source_id,
        province,
        regency,
        lat,
        lon,
        precision,
        coordinate_source,
        area_ha,
        developer_org_id,
        status,
        sector_focus,
        website,
        notes,
    ) in ESTATES:
        if source_id not in source_ids:
            raise SystemExit(f"{estate_id}: unknown source {source_id}")
        if developer_org_id not in org_ids:
            raise SystemExit(f"{estate_id}: unknown developer organisation {developer_org_id}")
        managed_ids.add(estate_id)
        row = {field: "" for field in ESTATE_FIELDS}
        row.update(
            {
                "id": estate_id,
                "name": official_name,
                "type": "industrial_estate",
                "province": province,
                "regency": regency,
                "island": island_for(province),
                "lat": lat,
                "lon": lon,
                "precision": precision,
                "coordinate_source": coordinate_source,
                "area_ha": area_ha,
                "developer": next(
                    org["name"] for org in organizations if org["id"] == developer_org_id
                ),
                "developer_org_id": developer_org_id,
                "status": status,
                "sector_focus": sector_focus,
                "legal_basis": "",
                "established_year": "",
                "website": website,
                "occupancy_pct": "",
                "kemenperin_id": "",
                "sez_id": "",
                "source_id": source_id,
                "last_verified": LAST_VERIFIED,
                "notes": notes,
            }
        )
        upsert(estates, "id", row)

    claims[:] = [row for row in claims if row["estate_id"] not in managed_ids]
    for estate_id, source_id, claim, claim_value, claim_date, note in CLAIMS:
        if estate_id not in managed_ids:
            raise SystemExit(f"claim has unknown estate {estate_id}")
        if source_id not in source_ids:
            raise SystemExit(f"claim has unknown source {source_id}")
        claims.append(
            {
                "estate_id": estate_id,
                "source_id": source_id,
                "claim": claim,
                "claim_value": claim_value,
                "claim_date": claim_date,
                "notes": note,
            }
        )

    write_csv(CURATED / "sources.csv", SOURCE_FIELDS, sources)
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, organizations)
    write_csv(CURATED / "estates.csv", ESTATE_FIELDS, estates)
    write_csv(CURATED / "estate_sources.csv", ESTATE_SOURCE_FIELDS, claims)

    print(
        f"OK: {len(ESTATES)} PSN industrial areas, {len(SOURCES)} sources, "
        f"{len(ORGS)} organisations, {len(CLAIMS)} claims"
    )
    print(f"estates: {len(estates)}; claims: {len(claims)}; sources: {len(sources)}")


if __name__ == "__main__":
    main()
