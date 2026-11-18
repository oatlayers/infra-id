"""Add 17 sourced strategic and private records.

Sources archived in ``data/raw/2026-11-13/``:

* Eight undated KPPIP priority-project pages captured on 13 November 2026:
  SHIA Express, Bontang refinery, Sumatra 500 kV, Central-West Java 500 kV,
  PLTU Indramayu, PLTU Batang, CBL inland waterway and North Bali airport.
* ESDM, 10 October 2026: Batang Toru reservoir impounding.
* PU, 1 August 2023: Sodetan Ciliwung inauguration.
* PU, 21 February 2023: Ciliwung normalisation progress.
* KKP, 29 September 2026: PPN Pengambengan groundbreaking.
* KKP, 18 September 2026: PPN Kejawanan groundbreaking.
* Kemenhub, 1 November 2023: Kertajati full operation.
* ANTARA, 21 August 2026: CATIB Karawang construction complete.
* BPI, 6 September 2022: PLTU Batang commercial operation.
* Kemenhub, 5 April 2023: Trans Sulawesi railway.
* Kemenhub, 12 June 2026: national rail network progress.
* ESDM, 10 July 2026: B50 biodiesel launch.

No status, cost, capacity, target or date is invented. KPPIP priority-project
pages are undated and do not form the current 226-row PSN register, so the
KPPIP records use ``psn=unknown`` and say so in ``notes``. The current register
also omits Kertajati and CATIB, which are recorded from separate official or
news sources.

The script is idempotent: existing ids are never replaced and existing claims,
aliases, translations, links and values are never duplicated.

Run: python scripts/imports/add_17_strategic_records.py
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

SRC_SHIA = "src-kppip-shia-express-2026-11-13"
SRC_BONTANG = "src-kppip-bontang-refinery-2026-11-13"
SRC_SUMATRA = "src-kppip-sumatra-500kv-2026-11-13"
SRC_CENTRAL_WEST_JAVA = "src-kppip-central-west-java-500kv-2026-11-13"
SRC_INDRAMAYU = "src-kppip-pltu-indramayu-2026-11-13"
SRC_BATANG = "src-kppip-pltu-batang-2026-11-13"
SRC_CBL = "src-kppip-cbl-2026-11-13"
SRC_NORTH_BALI = "src-kppip-north-bali-airport-2026-11-13"
SRC_BATANG_TORU = "src-esdm-batang-toru-2026-10-10"
SRC_SODETAN = "src-pu-sodetan-ciliwung-2023-08-01"
SRC_CILIWUNG = "src-pu-ciliwung-normalisation-2023-02-21"
SRC_PENGAMBENGAN = "src-kkp-ppn-pengambengan-2026-09-29"
SRC_KEJAWANAN = "src-kkp-ppn-kejawanan-2026-09-18"
SRC_KERTAJATI = "src-kemenhub-kertajati-2023-11-01"
SRC_CATIB = "src-antara-catib-karawang-2026-08-21"
SRC_BPI = "src-bpi-pltu-batang-cod-2022-09-06"
SRC_TRANS_SULAWESI = "src-kemenhub-trans-sulawesi-2023-04-05"
SRC_RAIL_NETWORK = "src-kemenhub-rail-network-2026-06-12"
SRC_B50 = "src-esdm-b50-2026-07-10"

PROGRAMME_ELECTRICITY = "prog-electricity"
PROGRAMME_JAKARTA_FLOOD = "prog-jakarta-flood-control"
PROGRAMME_AVIATION = "prog-tourism-aviation"
PROGRAMME_SUPERHUB = "prog-superhub"
PROGRAMME_FOOD = "prog-food-supply"
PROGRAMME_PALM = "prog-sugar-palm-downstreaming"

ORG_PLN = "org-pln"
ORG_PERTAMINA = "org-pertamina"
ORG_PELINDO = "org-pelindo"
ORG_KEMENTERIAN_PU = "org-kementerian-pu"
ORG_KEMENTERIAN_KKP = "org-kementerian-kkp"
ORG_KEMENTERIAN_ESDM = "org-kementerian-esdm"

KPPIP_LICENCE = "Government public data; check portal terms"
PRESS_LICENCE = "Government press release; quoted in short excerpts"
NEWS_LICENCE = "News article; quoted in short excerpts"
COMPANY_LICENCE = "Company release; quoted in short excerpts"

NEW_SOURCES = [
    {
        "id": SRC_SHIA,
        "publisher": "KPPIP",
        "title": "Kereta Api Ekspres SHIA",
        "url": (
            "https://kppip.go.id/proyek-prioritas/kereta-api/"
            "kereta-api-ekspres-shia/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "b88dfa42fb10bdcc31b17c62e1a0141f55289cadfafbd8da7a3f16e1db9b4de0"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/kppip_shia_express_2026.html",
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "Rp24.5T, KPBU and BUMN funding, DKI Jakarta-Banten, Kemenhub as "
            "responsible party, planned construction 2015 and operation 2017, "
            "status Selesai, and operation since the end of 2018."
        ),
    },
    {
        "id": SRC_BONTANG,
        "publisher": "KPPIP",
        "title": "Kilang Minyak Bontang",
        "url": (
            "https://kppip.go.id/proyek-prioritas/minyak-gas/"
            "kilang-minyak-bontang/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "f34f3cefef9b61ff50d50c106059a07f21b79ec86d719c1378e2d543babb90f8"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/kppip_bontang_refinery_2026.html",
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "Rp197.586T, BUMN assignment, Bontang in East Kalimantan, "
            "Pertamina as responsible party, planned operation 2027, "
            "transaction stage and a minimum capacity of 300,000 bpd."
        ),
    },
    {
        "id": SRC_SUMATRA,
        "publisher": "KPPIP",
        "title": "Transmisi Sumatera 500 kV",
        "url": (
            "https://kppip.go.id/proyek-prioritas/ketenaga-listrikan/"
            "transmisi-sumatera-500-kv/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "e4cf5b95b7587f4255f8c7751c77b1215489093486680d7a7f4abd8ca5b0c8e2"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/kppip_sumatra_500kv_2026.html",
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "Rp24.4T, BUMN assignment, PLN as responsible party, 1,330 km "
            "from Muara Enim to Langsa, construction stage, planned "
            "construction 2016 and operation 2019."
        ),
    },
    {
        "id": SRC_CENTRAL_WEST_JAVA,
        "publisher": "KPPIP",
        "title": "Central - West Java Transmission Line 500 kV",
        "url": (
            "https://kppip.go.id/proyek-prioritas/ketenaga-listrikan/"
            "central-west-java-transmission-line-500-kv/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "fd1756b47c6ff1c93ee9447e2cba8110471f69da306439625b2b2137162e2759"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/kppip_central_west_java_500kv_2026.html"
        ),
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "Rp7.64T, PLN budget, West Java-Central Java, partially operating "
            "status, and four sections of 144, 397, 180 and 260 km."
        ),
    },
    {
        "id": SRC_INDRAMAYU,
        "publisher": "KPPIP",
        "title": "PLTU Indramayu",
        "url": (
            "https://kppip.go.id/proyek-prioritas/ketenaga-listrikan/"
            "pltu-indramayu/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "7c59e819e5a4c61c2c982f0912cd0273ca990bf5cc3ac163b7120fbbc2559871"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/kppip_pltu_indramayu_2026.html",
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "Rp29.5T, APBN with a foreign loan, Indramayu in West Java, PLN as "
            "responsible party, 1,000 MW, preparation stage, planned "
            "construction 2022 and operation 2026."
        ),
    },
    {
        "id": SRC_BATANG,
        "publisher": "KPPIP",
        "title": "PLTU Batang / Central Java Power Plant",
        "url": (
            "https://kppip.go.id/proyek-prioritas/ketenaga-listrikan/"
            "pltu-batang/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "5dabd08c3d0e64b313c67d1e78657fc763271432d9dd8760a9fddd893d1f002e"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/kppip_pltu_batang_2026.html",
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "Rp56.7T, KPBU with PT Bhimasena Power Indonesia, Batang in "
            "Central Java, PLN as responsible party, 2x1,000 MW USC, and a "
            "construction-stage status that the BPI COD release supersedes."
        ),
    },
    {
        "id": SRC_CBL,
        "publisher": "KPPIP",
        "title": "Inland Waterways / Cikarang-Bekasi-Laut Jawa (CBL)",
        "url": (
            "https://kppip.go.id/proyek-prioritas/pelabuhan/"
            "inland-waterways-cikarang-bekasi-laut-jawa-cbl/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "1c234f2af31ba6b2b96845d4354e5c2537fe8c2d8ae186cfdf48d7c7c74232e0"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/kppip_cbl_2026.html",
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "Rp3.41T, potential BUMN assignment, DKI Jakarta-West Java, "
            "Pelindo II as responsible party, preparation stage, planned "
            "construction 2019 and operation 2021."
        ),
    },
    {
        "id": SRC_NORTH_BALI,
        "publisher": "KPPIP",
        "title": "Pembangunan Bandar Udara Bali Utara",
        "url": (
            "https://kppip.go.id/proyek-strategis-nasional/"
            "f-proyek-pembangunan-bandar-udara-baru/"
            "pembangunan-bandar-udara-bali-utara/"
        ),
        "published_on": "",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "0ff59c72bdd5bb7a2d270d5d0da90329eff41f034ddfb6084ed1f9f5f2f90db4"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/kppip_north_bali_airport_2026.html"
        ),
        "licence": KPPIP_LICENCE,
        "notes": (
            "Undated priority-project page captured 13 November 2026. Gives "
            "APBN funding, Bali, preparation stage, and no investment total, "
            "responsible party, construction date or operation date."
        ),
    },
    {
        "id": SRC_BATANG_TORU,
        "publisher": "Kementerian Energi dan Sumber Daya Mineral (ESDM)",
        "title": (
            "Waduk PLTA Batang Toru Mulai Digenangi, Pasokan Listrik Sumatera "
            "Utara Kian Andal Jelang Nataru"
        ),
        "url": (
            "https://www.esdm.go.id/id/media-center/arsip-berita/"
            "waduk-plta-batang-toru-mulai-digenangi-pasokan-listrik-sumatera-"
            "utara-kian-andal-jelang-nataru"
        ),
        "published_on": "2026-10-10",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "de8b2314ed22223eb2ef98cf466f58d2862a5233c3074cb50813fb323a0f2d2d"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/esdm_batang_toru_2026-10-10.html",
        "licence": PRESS_LICENCE,
        "notes": (
            "Reservoir impounding began on 9 October 2026. Gives 510 MW "
            "(4x127.5 MW), Rp21.6T, NSHE as developer, a 160 MW second-phase "
            "study, and a target to operate for the 2026 Christmas-New Year "
            "period."
        ),
    },
    {
        "id": SRC_SODETAN,
        "publisher": "Kementerian Pekerjaan Umum (PU)",
        "title": (
            "Presiden Jokowi Resmikan Sodetan Ciliwung 1.2 Km, Bagian dari "
            "Penanganan dari Hulu ke Hilir untuk Kendalikan Banjir Jakarta"
        ),
        "url": (
            "https://pu.go.id/berita/"
            "presiden-jokowi-resmikan-sodetan-ciliwung-12-km-bagian-dari-"
            "penanganan-dari-hulu-ke-hilir-untuk-kendalikan-banjir-jakarta"
        ),
        "published_on": "2023-08-01",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "4b831631cbff1d8ecbcd48981015d53214b355c84d59aa45934c7c753b55b58b"
        ),
        "accessed_via": "Direct HTTP fetch",
        "archive_path": (
            "data/raw/2026-11-13/pu_sodetan_ciliwung_2023-08-01.html"
        ),
        "licence": PRESS_LICENCE,
        "notes": (
            "Inaugurated on 31 July 2023. Gives a 1,268 m tunnel with two "
            "3.5 m pipes, 60 m3/s, about Rp1.2T, the WIKA-Jaya Konstruksi KSO "
            "contractor, and a 107 ha reduction in flood-affected area."
        ),
    },
    {
        "id": SRC_CILIWUNG,
        "publisher": "Kementerian Pekerjaan Umum (PU)",
        "title": (
            "Normalisasi Sungai Ciliwung untuk Pengendalian Banjir Jakarta, "
            "Ditargetkan Rampung Tahun 2024. Presiden Jokowi Tinjau Langsung "
            "Lokasi Pekerjaan."
        ),
        "url": (
            "https://sda.pu.go.id/balai/bwsbalipenida/berita/detail/"
            "396-normalisasi-sungai-ciliwung-untuk-pengendalian-banjir-"
            "jakarta-ditargetkan-rampung-tahun-2024-presi"
        ),
        "published_on": "2023-02-21",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "d54e7618f1d9bba4eaa1becb7756a70ec72e81b3820067a5840c6747e8574c4f"
        ),
        "accessed_via": "Direct HTTP fetch",
        "archive_path": (
            "data/raw/2026-11-13/pu_ciliwung_normalisation_2023-02-21.html"
        ),
        "licence": PRESS_LICENCE,
        "notes": (
            "Gives a 35-50 m normalised width, capacity rising from 200 to "
            "570 m3/s, 16.19 km completed of 33 km, and the remaining 17 km "
            "targeted for the end of 2024."
        ),
    },
    {
        "id": SRC_PENGAMBENGAN,
        "publisher": "Kementerian Kelautan dan Perikanan (KKP)",
        "title": (
            "Menteri Trenggono Siapkan PPN Pengambengan Jadi Pelabuhan "
            "Perikanan Kelas Dunia"
        ),
        "url": (
            "https://kkp.go.id/news/news-detail/"
            "menteri-trenggono-siapkan-ppn-pengambengan-jadi-pelabuhan-"
            "perikanan-kelas-dunia-wKBM.html"
        ),
        "published_on": "2026-09-29",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "0c5c489c22b69bf4f63aeab2c199246b5d6a176f4cdaf5b9a275128ab5b087ee"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/kkp_ppn_pengambengan_2026-09-29.html"
        ),
        "licence": PRESS_LICENCE,
        "notes": (
            "Groundbreaking on 29 September 2026. Gives 13.5 to 49.3 ha, a "
            "harbour basin of 24 to 88.3 ha, 1,273 to 1,600 vessels, 61,300 "
            "to 124,000 t/yr landings, Rp48bn to Rp104bn PNBP, about 25,000 "
            "workers, a Rp1.27T contract with IsDB support and an end-2029 "
            "completion target."
        ),
    },
    {
        "id": SRC_KEJAWANAN,
        "publisher": "Kementerian Kelautan dan Perikanan (KKP)",
        "title": "KKP Modernisasi Pelabuhan Perikanan, PPN Kejawanan Jadi Langkah Awal",
        "url": (
            "https://www.kkp.go.id/news/news-detail/"
            "kkp-modernisasi-pelabuhan-perikanan-ppn-kejawanan-jadi-langkah-"
            "awal-6BEV.html"
        ),
        "published_on": "2026-09-18",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "c340fc8734210a21bb3f582ca86ae8fb6102cee9a23824e38d2ce45ed6001960"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/kkp_ppn_kejawanan_2026-09-18.html"
        ),
        "licence": PRESS_LICENCE,
        "notes": (
            "Groundbreaking on 17 September 2026. Gives 241 to 500 vessels, "
            "5,600 to 32,000 t/yr landings, 2,900 to 8,000 workers and "
            "Rp15bn to Rp53bn annual PNBP. No investment or completion date "
            "is stated."
        ),
    },
    {
        "id": SRC_KERTAJATI,
        "publisher": "Kementerian Perhubungan (Kemenhub)",
        "title": (
            "Bandara Kertajati Resmi Beroperasi Penuh, Menhub Targetkan "
            "Layani 12 Juta Penumpang Hingga Tahun 2024"
        ),
        "url": (
            "https://www.kemenhub.go.id/post/read/"
            "%E2%80%8Bbandara-kertajati-resmi-beroperasi-penuh,-menhub-"
            "targetkan-layani-12-juta-penumpang-hingga-tahun-2024"
        ),
        "published_on": "2023-11-01",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "eadc1d54fcdfaba7029d9e3bc4da8a877268e7fbb79f9f01f035c19e54b17a9a"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/kemenhub_kertajati_2023-11-01.html"
        ),
        "licence": PRESS_LICENCE,
        "notes": (
            "Full operation from 29 October 2023. Gives 1,800 ha, a 121,000 "
            "m2 passenger terminal, a 90,000 m2 cargo terminal, a 3,000x60 m "
            "runway, 5.6-12 million passengers/yr to 2024, 29.3 million by "
            "2032, and 16 daily flights at the time."
        ),
    },
    {
        "id": SRC_CATIB,
        "publisher": "ANTARA News",
        "title": "ESDM sebut pembangunan pabrik baterai EV di Karawang sudah rampung",
        "url": (
            "https://www.antaranews.com/berita/5705060/"
            "esdm-sebut-pembangunan-pabrik-baterai-ev-di-karawang-sudah-rampung"
        ),
        "published_on": "2026-08-21",
        "retrieved_on": REVIEWED,
        "source_type": "secondary",
        "language": "id",
        "snapshot_hash": (
            "150b0121aad2c3397c6d1ab553d9433dd274aed031e430885f9b14b25b135052"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/antara_catib_karawang_2026-08-21.html"
        ),
        "licence": NEWS_LICENCE,
        "notes": (
            "Quotes the ESDM Secretary General and a CATIB director. Gives a "
            "completed 6.9 GWh/yr plant, gradual operation, about Rp7T, an 18 "
            "MWh PLTS and about 3,000 workers; the inauguration was awaiting "
            "a presidential schedule."
        ),
    },
    {
        "id": SRC_BPI,
        "publisher": "PT Bhimasena Power Indonesia (BPI)",
        "title": "Batang Power Plant 2 x 1.000 MW Project Achieves Commercial Operation",
        "url": (
            "https://www.bhimasenapower.co.id/content/3050/"
            "proyek-pltu-batang-2-x-1.000-mw-mencapai-operasi-komersial-penuh"
        ),
        "published_on": "2022-09-06",
        "retrieved_on": REVIEWED,
        "source_type": "company",
        "language": "en",
        "snapshot_hash": (
            "446ff621f65effe834f7074f27ac9e110ca6000e51c36c711ca3ed4d340337a3"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/bpi_pltu_batang_cod_2022-09-06.html"
        ),
        "licence": COMPANY_LICENCE,
        "notes": (
            "Unit 1 reached commercial operation on 15 August 2022 and Unit 2 "
            "on 31 August 2022. Gives 2x1,000 MW USC, the J-Power, Adaro and "
            "Itochu sponsors, and a 25-year supply contract with PLN."
        ),
    },
    {
        "id": SRC_TRANS_SULAWESI,
        "publisher": "Kementerian Perhubungan (Kemenhub)",
        "title": "Kereta Api dan Mimpi Rakyat Sulawesi",
        "url": "https://kemenhub.go.id/post/read/kereta-api-dan-mimpi-rakyat-sulawesi",
        "published_on": "2023-04-05",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "29e4fe7d7e622037f166037fc0cab71b9b1bb865611c80e3e891bfc7bfc44bdb"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/kemenhub_trans_sulawesi_2023-04-05.html"
        ),
        "licence": PRESS_LICENCE,
        "notes": (
            "Describes the Makassar-Manado Trans Sulawesi railway, the 150 km "
            "Makassar-Parepare section, 118 km built, 90 km of Maros-Barru "
            "operating, and a 157.7 km Makassar-Parepare alignment including "
            "15.7 km of siding track."
        ),
    },
    {
        "id": SRC_RAIL_NETWORK,
        "publisher": "Kementerian Perhubungan (Kemenhub)",
        "title": "Kemenhub Terus Percepat Pembangunan Jaringan Kereta Api Nasional",
        "url": (
            "https://www.kemenhub.go.id/index.php/post/read/"
            "kemenhub-terus-percepat-pembangunan-jaringan-kereta-api-nasional"
        ),
        "published_on": "2026-06-12",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "81070a8e632fd190fe4b8141606270e811413232f600cf5fec16959d264f08f2"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": (
            "data/raw/2026-11-13/kemenhub_rail_network_2026-06-12.html"
        ),
        "licence": PRESS_LICENCE,
        "notes": (
            "Confirms that completion of Makassar-Parepare operations remains "
            "a priority. Gives a 6,927 km active national network and a "
            "10,524 km target."
        ),
    },
    {
        "id": SRC_B50,
        "publisher": "Kementerian Energi dan Sumber Daya Mineral (ESDM)",
        "title": (
            "B50 Diluncurkan, Pemerintah Targetkan Hemat Devisa Rp170 Triliun "
            "dan Stop Impor Solar"
        ),
        "url": (
            "https://www.esdm.go.id/id/media-center/arsip-berita/"
            "b50-diluncurkan-pemerintah-targetkan-hemat-devisa-rp170-triliun-"
            "dan-stop-impor-solar"
        ),
        "published_on": "2026-07-10",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "snapshot_hash": (
            "6b4d40c9961f35ba1f2977b916bf13b356b267dd7c874ec0e2d309c67c6a47c7"
        ),
        "accessed_via": "r.jina.ai HTML proxy",
        "archive_path": "data/raw/2026-11-13/esdm_b50_2026-07-10.html",
        "licence": PRESS_LICENCE,
        "notes": (
            "Launch on 9 July 2026. Gives a 50% blend, Rp170T foreign-exchange "
            "saving, CPO demand of 15.2 to 16.3 Mt, value added of Rp20.92T "
            "to Rp23.49T, 1.8 to 2.1 million workers, 39.66 to 44.46 Mt CO2, "
            "and 38-40 million kL/yr diesel consumption."
        ),
    },
]

RECORDS = [
    {
        "id": "rail-shia-express",
        "name": "SHIA Airport Express Railway",
        "name_id": "Kereta Api Ekspres SHIA",
        "sector": "railway",
        "subsector": "airport rail",
        "status": "operating",
        "status_basis": (
            "KPPIP lists the project as completed and says the airport train "
            "from SHIA to central Jakarta has operated since the end of 2018."
        ),
        "island": "Java",
        "province": "DKI Jakarta",
        "route": (
            "Soekarno-Hatta International Airport-central Jakarta, "
            "DKI Jakarta-Banten"
        ),
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "24.5",
        "capacity": "",
        "capacity_unit": "",
        "psn": "unknown",
        "opened_year": "2018",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": REVIEWED,
        "verification": "official",
        "lat": "-6.20",
        "lon": "106.80",
        "precision": "province",
        "notes": (
            "KPPIP priority-project page (undated; captured 13 November 2026) "
            "gives Rp24.5T, KPBU and BUMN funding, Kementerian Perhubungan as "
            "responsible party, planned construction in 2015 and planned "
            "operation in 2017. The page says the airport train has operated "
            "since the end of 2018. It names the 2013 alignment via "
            "Halim-Manggarai-Dukuh Atas-Tanah Abang-Pluit-SHIA and a 2015 "
            "proposal to reroute via Gambir. The current 226-row PSN register "
            "does not list the project, so psn=unknown."
        ),
        "source": SRC_SHIA,
        "aliases": [
            (
                "KA Bandara SHIA",
                SRC_SHIA,
                "KPPIP calls it the KA Bandara from SHIA to central Jakarta.",
            ),
        ],
        "claims": [
            (
                SRC_SHIA,
                "status",
                "operating",
                REVIEWED,
                "Page says the airport train has operated since the end of 2018.",
            ),
            (
                SRC_SHIA,
                "location",
                "Soekarno-Hatta International Airport-central Jakarta, "
                "DKI Jakarta-Banten",
                REVIEWED,
                "",
            ),
            (
                SRC_SHIA,
                "opening",
                "end of 2018",
                REVIEWED,
                "The page says the airport train has operated since the end of "
                "2018; no exact date is stated.",
            ),
            (SRC_SHIA, "investment", "Rp24.5T", REVIEWED, ""),
        ],
    },
    {
        "id": "factory-bontang-refinery",
        "name": "Bontang Refinery",
        "name_id": "Kilang Minyak Bontang",
        "sector": "energy",
        "subsector": "refinery",
        "status": "planned",
        "status_basis": (
            "KPPIP lists the refinery at the transaction stage, with planned "
            "operation in 2027."
        ),
        "island": "Kalimantan",
        "province": "East Kalimantan",
        "route": "Bontang, East Kalimantan",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "197.586",
        "capacity": "300000",
        "capacity_unit": "bpd (minimum)",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "2027",
        "status_as_of": REVIEWED,
        "verification": "official",
        "lat": "-0.13",
        "lon": "117.50",
        "precision": "approximate",
        "notes": (
            "KPPIP priority-project page (undated; captured 13 November 2026) "
            "gives Rp197.586T, BUMN assignment, Pertamina as responsible "
            "party, a minimum capacity of 300,000 barrels per day, planned "
            "operation in 2027 and the transaction stage. The page says the "
            "configuration will consider petrochemicals. The current 226-row "
            "PSN register does not list the project, so psn=unknown."
        ),
        "source": SRC_BONTANG,
        "aliases": [
            (
                "Kilang Bontang",
                SRC_BONTANG,
                "Short form of Kilang Minyak Bontang.",
            ),
        ],
        "claims": [
            (
                SRC_BONTANG,
                "status",
                "planned",
                REVIEWED,
                "Page status is Tahap Transaksi.",
            ),
            (SRC_BONTANG, "location", "Bontang, East Kalimantan", REVIEWED, ""),
            (SRC_BONTANG, "investment", "Rp197.586T", REVIEWED, ""),
            (
                SRC_BONTANG,
                "capacity",
                "at least 300,000 bpd",
                REVIEWED,
                "The page says a minimum of 300,000 barrels per day.",
            ),
            (
                SRC_BONTANG,
                "target",
                "2027",
                REVIEWED,
                "Planned start of operation.",
            ),
        ],
    },
    {
        "id": "grid-sumatra-500kv",
        "name": "Sumatra 500 kV Transmission",
        "name_id": "Transmisi Sumatera 500 kV",
        "sector": "energy",
        "subsector": "transmission",
        "status": "under_construction",
        "status_basis": (
            "KPPIP lists the 1,330 km Muara Enim-Langsa line at the "
            "construction stage."
        ),
        "island": "Sumatra",
        "province": "South Sumatra",
        "route": "Muara Enim, South Sumatra-Langsa, Aceh",
        "length_km": "1330",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "24.4",
        "capacity": "",
        "capacity_unit": "",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": REVIEWED,
        "verification": "official",
        "lat": "-3.65",
        "lon": "103.77",
        "precision": "approximate",
        "notes": (
            "KPPIP priority-project page (undated; captured 13 November 2026) "
            "gives Rp24.4T, BUMN assignment, PLN as responsible party, a "
            "1,330 km line from Muara Enim in South Sumatra to Langsa in "
            "Aceh, and the construction stage. It still gives a planned start "
            "of operation in 2019, which has passed; no newer completion date "
            "is stated. The map point is the Muara Enim end of the corridor. "
            "The current 226-row PSN register does not list the project, so "
            "psn=unknown."
        ),
        "source": SRC_SUMATRA,
        "aliases": [
            (
                "Transmisi Sumatera 500 kV",
                SRC_SUMATRA,
                "Official KPPIP page title.",
            ),
        ],
        "claims": [
            (
                SRC_SUMATRA,
                "status",
                "under_construction",
                REVIEWED,
                "Page status is Tahap Konstruksi.",
            ),
            (
                SRC_SUMATRA,
                "location",
                "Muara Enim, South Sumatra-Langsa, Aceh",
                REVIEWED,
                "",
            ),
            (SRC_SUMATRA, "length", "1,330 km", REVIEWED, ""),
            (SRC_SUMATRA, "investment", "Rp24.4T", REVIEWED, ""),
            (
                SRC_SUMATRA,
                "operator",
                "PT PLN (Persero)",
                REVIEWED,
                "PLN is the responsible party named on the page.",
            ),
        ],
    },
    {
        "id": "grid-central-west-java-500kv",
        "name": "Central-West Java 500 kV Transmission",
        "name_id": "Transmisi Jawa Tengah-Jawa Barat 500 kV",
        "sector": "energy",
        "subsector": "transmission",
        "status": "operating",
        "status_basis": (
            "KPPIP lists the project as partially operating (beroperasi "
            "sebagian)."
        ),
        "island": "Java",
        "province": "West Java",
        "route": (
            "Tanjung Jati-Ungaran/Pedan-Mandirancan-Indramayu-Cibatu, "
            "Central Java-West Java"
        ),
        "length_km": "981",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "7.64",
        "capacity": "",
        "capacity_unit": "",
        "psn": "unknown",
        "opened_year": "2019",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": REVIEWED,
        "verification": "official",
        "lat": "-6.35",
        "lon": "107.30",
        "precision": "province",
        "notes": (
            "KPPIP priority-project page (undated; captured 13 November 2026) "
            "gives Rp7.64T, a PLN budget, West Java-Central Java, and a "
            "partially operating status. The four sections are 144 km "
            "(Tanjung Jati-Ungaran/Pedan), 397 km (Ungaran/Pedan-Mandirancan), "
            "180 km (Mandirancan-Indramayu) and 260 km (Indramayu-Cibatu), "
            "totalling 981 km. The page does not say which sections are "
            "energised, so operational_km is blank. It gives a planned start "
            "of operation in 2019, which has passed. The current 226-row PSN "
            "register does not list the project, so psn=unknown."
        ),
        "source": SRC_CENTRAL_WEST_JAVA,
        "aliases": [
            (
                "Transmisi Jawa Tengah-Jawa Barat 500 kV",
                SRC_CENTRAL_WEST_JAVA,
                "Official KPPIP page title.",
            ),
        ],
        "claims": [
            (
                SRC_CENTRAL_WEST_JAVA,
                "status",
                "operating (partially)",
                REVIEWED,
                "Page status is Beroperasi Sebagian; the page does not say "
                "which sections are energised.",
            ),
            (
                SRC_CENTRAL_WEST_JAVA,
                "location",
                "Tanjung Jati-Ungaran/Pedan-Mandirancan-Indramayu-Cibatu, "
                "Central Java-West Java",
                REVIEWED,
                "",
            ),
            (
                SRC_CENTRAL_WEST_JAVA,
                "length",
                "981 km across four sections",
                REVIEWED,
                "144 + 397 + 180 + 260 km.",
            ),
            (
                SRC_CENTRAL_WEST_JAVA,
                "investment",
                "Rp7.64T",
                REVIEWED,
                "",
            ),
            (
                SRC_CENTRAL_WEST_JAVA,
                "opening",
                "2019 (planned start of operation)",
                REVIEWED,
                "The page says the project is partially operating and gives a "
                "planned start of operation in 2019; it does not say which "
                "sections are energised.",
            ),
            (
                SRC_CENTRAL_WEST_JAVA,
                "operator",
                "PT PLN (Persero)",
                REVIEWED,
                "PLN is the responsible party named on the page.",
            ),
        ],
    },
    {
        "id": "power-pltu-indramayu",
        "name": "Indramayu Coal-Fired Power Plant (1,000 MW)",
        "name_id": "PLTU Indramayu 1.000 MW",
        "sector": "energy",
        "subsector": "coal",
        "status": "planned",
        "status_basis": (
            "KPPIP lists the 1,000 MW plant at the preparation stage, with "
            "planned operation in 2026."
        ),
        "island": "Java",
        "province": "West Java",
        "route": "Indramayu, West Java",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "29.5",
        "capacity": "1000",
        "capacity_unit": "MW",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "2026",
        "status_as_of": REVIEWED,
        "verification": "official",
        "lat": "-6.33",
        "lon": "108.32",
        "precision": "approximate",
        "notes": (
            "KPPIP priority-project page (undated; captured 13 November 2026) "
            "gives Rp29.5T, APBN funding with a foreign loan, PLN as "
            "responsible party, 1,000 MW, the preparation stage, planned "
            "construction in 2022 and planned operation in 2026. The page "
            "still shows preparation, so the 2026 date is a plan and not an "
            "opening. The current 226-row PSN register does not list the "
            "project, so psn=unknown."
        ),
        "source": SRC_INDRAMAYU,
        "aliases": [
            ("PLTU Indramayu", SRC_INDRAMAYU, "Official KPPIP page title."),
        ],
        "claims": [
            (
                SRC_INDRAMAYU,
                "status",
                "planned",
                REVIEWED,
                "Page status is Tahap Penyiapan.",
            ),
            (SRC_INDRAMAYU, "location", "Indramayu, West Java", REVIEWED, ""),
            (SRC_INDRAMAYU, "capacity", "1,000 MW", REVIEWED, ""),
            (SRC_INDRAMAYU, "investment", "Rp29.5T", REVIEWED, ""),
            (
                SRC_INDRAMAYU,
                "target",
                "2026",
                REVIEWED,
                "Planned start of operation; the page still shows preparation.",
            ),
            (
                SRC_INDRAMAYU,
                "operator",
                "PT PLN (Persero)",
                REVIEWED,
                "PLN is the responsible party named on the page.",
            ),
        ],
    },
    {
        "id": "power-pltu-batang",
        "name": "Batang Coal-Fired Power Plant (2x1,000 MW)",
        "name_id": "PLTU Batang (2x1.000 MW)",
        "sector": "energy",
        "subsector": "coal",
        "status": "operating",
        "status_basis": (
            "BPI announced commercial operation of Unit 1 on 15 August 2022 "
            "and Unit 2 on 31 August 2022."
        ),
        "island": "Java",
        "province": "Central Java",
        "route": "Batang, Central Java",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "56.7",
        "capacity": "2000",
        "capacity_unit": "MW",
        "psn": "unknown",
        "opened_year": "2022",
        "opened_date": "2022-08-31",
        "expected_open_year": "",
        "status_as_of": "2022-09-06",
        "verification": "dual",
        "lat": "-6.91",
        "lon": "109.73",
        "precision": "approximate",
        "notes": (
            "BPI, the IPP, says Unit 1 reached commercial operation on 15 "
            "August 2022 and Unit 2 on 31 August 2022, so the 2x1,000 MW USC "
            "plant is fully operational. The KPPIP priority-project page "
            "(undated; captured 13 November 2026) still says construction and "
            "is treated as stale. KPPIP gives Rp56.7T, KPBU with BPI, PLN as "
            "responsible party, and the J-Power (34%), Adaro (34%) and Itochu "
            "(32%) sponsors. The current 226-row PSN register does not list "
            "the project, so psn=unknown."
        ),
        "source": SRC_BATANG,
        "aliases": [
            ("PLTU Batang", SRC_BATANG, "Official KPPIP page title."),
            (
                "Central Java Power Plant",
                SRC_BATANG,
                "Alternative name used in the KPPIP page title.",
            ),
            (
                "Central Java Coal-Fired Power Plant",
                SRC_BPI,
                "BPI says this was the former project name, renamed Batang "
                "Power Plant.",
            ),
        ],
        "claims": [
            (
                SRC_BPI,
                "status",
                "operating",
                "2022-09-06",
                "Both units are in commercial operation.",
            ),
            (
                SRC_BPI,
                "capacity",
                "2 x 1,000 MW",
                "2022-09-06",
                "Ultra Super Critical technology.",
            ),
            (
                SRC_BPI,
                "opening",
                "2022-08-31",
                "2022-09-06",
                "Unit 1 on 15 August 2022; Unit 2 on 31 August 2022.",
            ),
            (
                SRC_BPI,
                "operator",
                "PT Bhimasena Power Indonesia",
                "2022-09-06",
                "BPI operates the plant and sells electricity to PLN for 25 "
                "years.",
            ),
            (
                SRC_BATANG,
                "investment",
                "Rp56.7T",
                REVIEWED,
                "",
            ),
            (
                SRC_BATANG,
                "capacity",
                "2 x 1,000 MW",
                REVIEWED,
                "",
            ),
            (
                SRC_BATANG,
                "location",
                "Batang, Central Java",
                REVIEWED,
                "",
            ),
        ],
    },
    {
        "id": "port-cbl-inland-waterway",
        "name": "Cikarang-Bekasi-Laut (CBL) Inland Waterway",
        "name_id": "Inland Waterways Cikarang-Bekasi-Laut (CBL)",
        "sector": "seaport",
        "subsector": "inland waterway",
        "status": "planned",
        "status_basis": (
            "KPPIP lists the inland waterway at the preparation stage."
        ),
        "island": "Java",
        "province": "DKI Jakarta",
        "route": "Cikarang-Bekasi-Marunda, DKI Jakarta-West Java",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "3.41",
        "capacity": "",
        "capacity_unit": "",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": REVIEWED,
        "verification": "official",
        "lat": "-6.20",
        "lon": "107.00",
        "precision": "province",
        "notes": (
            "KPPIP priority-project page (undated; captured 13 November 2026) "
            "gives Rp3.41T, a potential BUMN assignment, Pelindo II as "
            "responsible party, and the preparation stage. Phase 1 uses the "
            "existing Cikarang-Bekasi-Laut canal via Marunda; phase 2 would "
            "extend from Tanjung Priok to Cikampek. Planned construction in "
            "2019 and operation in 2021 have passed without a completion "
            "source. The current 226-row PSN register does not list the "
            "project, so psn=unknown."
        ),
        "source": SRC_CBL,
        "aliases": [
            (
                "CBL",
                SRC_CBL,
                "Short form used in the KPPIP page title.",
            ),
        ],
        "claims": [
            (
                SRC_CBL,
                "status",
                "planned",
                REVIEWED,
                "Page status is Tahap Penyiapan.",
            ),
            (
                SRC_CBL,
                "location",
                "Cikarang-Bekasi-Marunda, DKI Jakarta-West Java",
                REVIEWED,
                "",
            ),
            (SRC_CBL, "investment", "Rp3.41T", REVIEWED, ""),
            (
                SRC_CBL,
                "operator",
                "PT Pelabuhan Indonesia II",
                REVIEWED,
                "Pelindo II is the responsible party named on the page.",
            ),
        ],
    },
    {
        "id": "airport-north-bali",
        "name": "North Bali Airport",
        "name_id": "Bandar Udara Bali Utara",
        "sector": "airport",
        "subsector": "international airport",
        "status": "planned",
        "status_basis": (
            "KPPIP lists the new airport at the preparation stage under an "
            "APBN scheme."
        ),
        "island": "Bali-Nusa Tenggara",
        "province": "Bali",
        "route": "North Bali",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "",
        "capacity": "",
        "capacity_unit": "",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": REVIEWED,
        "verification": "official",
        "lat": "-8.15",
        "lon": "114.95",
        "precision": "province",
        "notes": (
            "KPPIP priority-project page (undated; captured 13 November 2026) "
            "gives APBN funding, Bali, and the preparation stage. It states no "
            "investment total, responsible party, construction date or "
            "operation date. The map point is northern Bali, not a surveyed "
            "site. The current 226-row PSN register does not list the "
            "project, so psn=unknown."
        ),
        "source": SRC_NORTH_BALI,
        "aliases": [
            (
                "Bandara Bali Utara",
                SRC_NORTH_BALI,
                "Short form of Pembangunan Bandar Udara Bali Utara.",
            ),
        ],
        "claims": [
            (
                SRC_NORTH_BALI,
                "status",
                "planned",
                REVIEWED,
                "Page status is Penyiapan.",
            ),
            (SRC_NORTH_BALI, "location", "North Bali", REVIEWED, ""),
        ],
    },
    {
        "id": "airport-kertajati",
        "name": "Kertajati International Airport",
        "name_id": "Bandar Udara Internasional Kertajati",
        "sector": "airport",
        "subsector": "international airport",
        "status": "operating",
        "status_basis": (
            "Kemenhub reports that the airport was fully operated on 29 "
            "October 2023."
        ),
        "island": "Java",
        "province": "West Java",
        "route": "Kertajati, West Java",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "",
        "capacity": "12000000",
        "capacity_unit": "passengers/year (upper bound)",
        "psn": "unknown",
        "opened_year": "2023",
        "opened_date": "2023-10-29",
        "expected_open_year": "",
        "status_as_of": "2023-11-01",
        "verification": "official",
        "lat": "-6.65",
        "lon": "108.17",
        "precision": "approximate",
        "notes": (
            "Kemenhub reports full operation from 29 October 2023. It gives "
            "1,800 ha, a 121,000 m2 passenger terminal, a 90,000 m2 cargo "
            "terminal, a 3,000x60 m runway, a projected 5.6-12 million "
            "passengers per year to 2024, 29.3 million by 2032, and 16 daily "
            "flights with 32,760 seats per week at the time. The capacity "
            "field records the upper bound of the 5.6-12 million range. The "
            "current 226-row PSN register does not list the airport, so "
            "psn=unknown."
        ),
        "source": SRC_KERTAJATI,
        "aliases": [
            (
                "BIJB Kertajati",
                SRC_KERTAJATI,
                "Kemenhub uses BIJB for Bandara Internasional Jawa Barat.",
            ),
            (
                "Bandara Internasional Jawa Barat",
                SRC_KERTAJATI,
                "Full name of the BIJB airport.",
            ),
        ],
        "claims": [
            (
                SRC_KERTAJATI,
                "status",
                "operating",
                "2023-11-01",
                "Fully operated from 29 October 2023.",
            ),
            (
                SRC_KERTAJATI,
                "opening",
                "2023-10-29",
                "2023-11-01",
                "Full operation date.",
            ),
            (
                SRC_KERTAJATI,
                "capacity",
                "5.6-12 million passengers/year",
                "2023-11-01",
                "Projected range to 2024; the project row records the upper "
                "bound.",
            ),
            (
                SRC_KERTAJATI,
                "location",
                "Kertajati, West Java",
                "2023-11-01",
                "",
            ),
            (
                SRC_KERTAJATI,
                "length",
                "3,000 m x 60 m runway",
                "2023-11-01",
                "The terminal areas are recorded as an indicator.",
            ),
        ],
    },
    {
        "id": "power-batang-toru",
        "name": "Batang Toru Hydropower Plant",
        "name_id": "PLTA Batang Toru",
        "sector": "energy",
        "subsector": "hydro",
        "status": "under_construction",
        "status_basis": (
            "ESDM reports the reservoir began impounding on 9 October 2026 "
            "and targets operation around the Christmas-New Year period; the "
            "plant is not yet commercially operating."
        ),
        "island": "Sumatra",
        "province": "North Sumatra",
        "route": "Batang Toru River, Tapanuli Selatan, North Sumatra",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "21.6",
        "capacity": "510",
        "capacity_unit": "MW",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "2026",
        "status_as_of": "2026-10-10",
        "verification": "official",
        "lat": "1.50",
        "lon": "99.07",
        "precision": "approximate",
        "notes": (
            "ESDM reports the 510 MW (4x127.5 MW) plant at Batang Toru in "
            "Tapanuli Selatan, North Sumatra, with a Rp21.6T investment and "
            "PT North Sumatera Hydro Energy (NSHE) as developer. Reservoir "
            "impounding began on 9 October 2026, and the plant is targeted to "
            "operate for the 2026 Christmas-New Year period; it was not yet "
            "commercially operating. NSHE has prepared a 160 MW second-phase "
            "study. ESDM calls it a PSN, but it is absent from the current "
            "226-row register, so psn=unknown."
        ),
        "source": SRC_BATANG_TORU,
        "aliases": [
            (
                "PLTA Batang Toru",
                SRC_BATANG_TORU,
                "Official ESDM name.",
            ),
        ],
        "claims": [
            (
                SRC_BATANG_TORU,
                "status",
                "under_construction",
                "2026-10-10",
                "Reservoir impounding began on 9 October 2026; not yet "
                "commercially operating.",
            ),
            (
                SRC_BATANG_TORU,
                "location",
                "Batang Toru River, Tapanuli Selatan, North Sumatra",
                "2026-10-10",
                "",
            ),
            (
                SRC_BATANG_TORU,
                "capacity",
                "510 MW (4x127.5 MW)",
                "2026-10-10",
                "",
            ),
            (
                SRC_BATANG_TORU,
                "investment",
                "Rp21.6T",
                "2026-10-10",
                "",
            ),
            (
                SRC_BATANG_TORU,
                "target",
                "operation around the 2026 Christmas-New Year period",
                "2026-10-10",
                "No exact date is stated.",
            ),
            (
                SRC_BATANG_TORU,
                "operator",
                "PT North Sumatera Hydro Energy (NSHE)",
                "2026-10-10",
                "ESDM calls NSHE the developer; the claim is recorded as the "
                "operating company because 'developer' is not a claim type.",
            ),
            (
                SRC_BATANG_TORU,
                "design capacity",
                "160 MW second phase under study",
                "2026-10-10",
                "",
            ),
        ],
    },
    {
        "id": "flood-sodetan-ciliwung",
        "name": "Ciliwung Diversion Tunnel (Sodetan Ciliwung)",
        "name_id": "Sodetan Ciliwung",
        "sector": "water",
        "subsector": "flood control",
        "status": "operating",
        "status_basis": (
            "President Joko Widodo inaugurated the diversion on 31 July 2023; "
            "PU reports the tunnel is complete."
        ),
        "island": "Java",
        "province": "DKI Jakarta",
        "route": "Ciliwung River-Kanal Banjir Timur/Kali Cipinang, Jakarta",
        "length_km": "1.268",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "1.2",
        "capacity": "60",
        "capacity_unit": "m3/s",
        "psn": "unknown",
        "opened_year": "2023",
        "opened_date": "2023-07-31",
        "expected_open_year": "",
        "status_as_of": "2023-08-01",
        "verification": "official",
        "lat": "-6.23",
        "lon": "106.87",
        "precision": "approximate",
        "notes": (
            "PU reports a 1,268 m tunnel with two 3.5 m pipes, a 60 m3/s "
            "capacity, an about Rp1.2T budget, the WIKA-Jaya Konstruksi KSO "
            "contractor, and inauguration on 31 July 2023. The diversion "
            "reduces the flood-affected area by 107 ha. Work started in 2013, "
            "650 m was completed by 2015, and the remaining 580 m resumed in "
            "2021. The current 226-row PSN register does not list the project, "
            "so psn=unknown."
        ),
        "source": SRC_SODETAN,
        "aliases": [
            (
                "Sodetan Ciliwung 1,2 km",
                SRC_SODETAN,
                "PU headline name.",
            ),
        ],
        "claims": [
            (
                SRC_SODETAN,
                "status",
                "operating",
                "2023-08-01",
                "Inaugurated on 31 July 2023.",
            ),
            (
                SRC_SODETAN,
                "opening",
                "2023-07-31",
                "2023-08-01",
                "Inauguration date.",
            ),
            (SRC_SODETAN, "length", "1,268 m", "2023-08-01", ""),
            (
                SRC_SODETAN,
                "capacity",
                "60 m3/s",
                "2023-08-01",
                "Two 3.5 m pipes.",
            ),
            (
                SRC_SODETAN,
                "investment",
                "about Rp1.2T",
                "2023-08-01",
                "",
            ),
            (
                SRC_SODETAN,
                "location",
                "Ciliwung River-Kanal Banjir Timur/Kali Cipinang, Jakarta",
                "2023-08-01",
                "",
            ),
        ],
    },
    {
        "id": "flood-ciliwung-normalisation",
        "name": "Ciliwung River Normalisation",
        "name_id": "Normalisasi Sungai Ciliwung",
        "sector": "water",
        "subsector": "flood control",
        "status": "under_construction",
        "status_basis": (
            "PU reported 16.19 km of the 33 km normalisation completed and "
            "the remaining 17 km targeted for completion by the end of 2024; "
            "no later status source was found."
        ),
        "island": "Java",
        "province": "DKI Jakarta",
        "route": "Ciliwung River, Jakarta",
        "length_km": "33",
        "operational_km": "16.19",
        "construction_km": "17",
        "progress_pct": "",
        "investment_idr_t": "",
        "capacity": "570",
        "capacity_unit": "m3/s",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "2024",
        "status_as_of": "2023-02-21",
        "verification": "official",
        "lat": "-6.25",
        "lon": "106.85",
        "precision": "province",
        "notes": (
            "PU reports normalising the river to a 35-50 m width, raising "
            "capacity from 200 to 570 m3/s, 16.19 km completed of 33 km, and "
            "the remaining 17 km targeted for the end of 2024. No later "
            "official status was found, so the row remains under construction "
            "as of 21 February 2023. The completed and remaining lengths add "
            "to 33.19 km because the source rounds the remaining 17 km. The "
            "current 226-row PSN register does not list the project, so "
            "psn=unknown."
        ),
        "source": SRC_CILIWUNG,
        "aliases": [
            (
                "Normalisasi Ciliwung",
                SRC_CILIWUNG,
                "Short form of Normalisasi Sungai Ciliwung.",
            ),
        ],
        "claims": [
            (
                SRC_CILIWUNG,
                "status",
                "under_construction",
                "2023-02-21",
                "16.19 km of 33 km completed; the remaining 17 km were "
                "targeted for the end of 2024.",
            ),
            (SRC_CILIWUNG, "location", "Ciliwung River, Jakarta", "2023-02-21", ""),
            (SRC_CILIWUNG, "length", "33 km", "2023-02-21", ""),
            (
                SRC_CILIWUNG,
                "operational",
                "16.19 km completed",
                "2023-02-21",
                "",
            ),
            (
                SRC_CILIWUNG,
                "capacity",
                "570 m3/s after normalisation",
                "2023-02-21",
                "Up from 200 m3/s.",
            ),
            (
                SRC_CILIWUNG,
                "progress",
                "16.19 km of 33 km",
                "2023-02-21",
                "",
            ),
        ],
    },
    {
        "id": "port-ppn-pengambengan",
        "name": "Pengambengan National Fishing Port",
        "name_id": "Pelabuhan Perikanan Nusantara Pengambengan",
        "sector": "seaport",
        "subsector": "fishing port",
        "status": "under_construction",
        "status_basis": (
            "KKP held the groundbreaking on 29 September 2026 and targets "
            "completion by the end of 2029."
        ),
        "island": "Bali-Nusa Tenggara",
        "province": "Bali",
        "route": "Jembrana, Bali",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "1.27",
        "capacity": "1600",
        "capacity_unit": "vessels",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "2029",
        "status_as_of": "2026-09-29",
        "verification": "official",
        "lat": "-8.37",
        "lon": "114.57",
        "precision": "approximate",
        "notes": (
            "KKP held the groundbreaking for the Integrated Fishing Ports and "
            "International Fish Market Phase I on 29 September 2026. It gives "
            "a port area of 13.5 to 49.3 ha, a harbour basin of 24 to 88.3 ha, "
            "vessel capacity of 1,273 to 1,600, landings of 61,300 to 124,000 "
            "t/yr, PNBP of Rp48bn to Rp104bn/yr, about 25,000 workers, a "
            "Rp1.27T contract with Islamic Development Bank support, and an "
            "end-2029 completion target. The current 226-row PSN register does "
            "not list the project, so psn=unknown."
        ),
        "source": SRC_PENGAMBENGAN,
        "aliases": [
            (
                "PPN Pengambengan",
                SRC_PENGAMBENGAN,
                "Short form of Pelabuhan Perikanan Nusantara Pengambengan.",
            ),
        ],
        "claims": [
            (
                SRC_PENGAMBENGAN,
                "status",
                "under_construction",
                "2026-09-29",
                "Groundbreaking on 29 September 2026.",
            ),
            (
                SRC_PENGAMBENGAN,
                "location",
                "Jembrana, Bali",
                "2026-09-29",
                "",
            ),
            (
                SRC_PENGAMBENGAN,
                "investment",
                "Rp1.27T contract",
                "2026-09-29",
                "Islamic Development Bank support.",
            ),
            (
                SRC_PENGAMBENGAN,
                "capacity",
                "1,600 vessels",
                "2026-09-29",
                "Up from 1,273 vessels.",
            ),
            (
                SRC_PENGAMBENGAN,
                "target",
                "end-2029",
                "2026-09-29",
                "Projected completion.",
            ),
            (
                SRC_PENGAMBENGAN,
                "output",
                "124,000 t/yr landings",
                "2026-09-29",
                "Up from 61,300 t/yr; the port area and workforce are "
                "recorded as indicators.",
            ),
        ],
    },
    {
        "id": "port-ppn-kejawanan",
        "name": "Kejawanan National Fishing Port",
        "name_id": "Pelabuhan Perikanan Nusantara Kejawanan",
        "sector": "seaport",
        "subsector": "fishing port",
        "status": "under_construction",
        "status_basis": "KKP held the groundbreaking on 17 September 2026.",
        "island": "Java",
        "province": "West Java",
        "route": "Cirebon, West Java",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "",
        "capacity": "500",
        "capacity_unit": "vessels",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": "2026-09-18",
        "verification": "official",
        "lat": "-6.73",
        "lon": "108.56",
        "precision": "approximate",
        "notes": (
            "KKP held the groundbreaking on 17 September 2026. It gives vessel "
            "capacity of 241 to 500, landings of 5,600 to 32,000 t/yr, workers "
            "of 2,900 to 8,000, and annual PNBP of Rp15bn to Rp53bn. No "
            "investment or completion date is stated. The current 226-row PSN "
            "register does not list the project, so psn=unknown."
        ),
        "source": SRC_KEJAWANAN,
        "aliases": [
            (
                "PPN Kejawanan",
                SRC_KEJAWANAN,
                "Short form of Pelabuhan Perikanan Nusantara Kejawanan.",
            ),
        ],
        "claims": [
            (
                SRC_KEJAWANAN,
                "status",
                "under_construction",
                "2026-09-18",
                "Groundbreaking on 17 September 2026.",
            ),
            (SRC_KEJAWANAN, "location", "Cirebon, West Java", "2026-09-18", ""),
            (
                SRC_KEJAWANAN,
                "capacity",
                "500 vessels",
                "2026-09-18",
                "Up from 241 vessels.",
            ),
            (
                SRC_KEJAWANAN,
                "output",
                "32,000 t/yr landings",
                "2026-09-18",
                "Up from 5,600 t/yr; the workforce is recorded as an "
                "indicator.",
            ),
        ],
    },
    {
        "id": "factory-catib-karawang",
        "name": "CATIB EV Battery Cell Plant, Karawang",
        "name_id": "Pabrik Sel Baterai EV CATIB Karawang",
        "sector": "factory",
        "subsector": "battery",
        "status": "operating",
        "status_basis": (
            "ESDM reports construction is complete and the plant has started "
            "gradual operation; the official inauguration was awaiting a "
            "presidential schedule."
        ),
        "island": "Java",
        "province": "West Java",
        "route": "Artha Industrial Hills, Karawang, West Java",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "7",
        "capacity": "6.9",
        "capacity_unit": "GWh/yr",
        "psn": "unknown",
        "opened_year": "2026",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": "2026-08-21",
        "verification": "single",
        "lat": "-6.30",
        "lon": "107.30",
        "precision": "approximate",
        "notes": (
            "ANTARA quotes the ESDM Secretary General and a CATIB director: "
            "construction of the 6.9 GWh/yr plant is complete, gradual "
            "operation has started, and the inauguration was awaiting a "
            "presidential schedule. It gives an investment of about Rp7T, an "
            "18 MWh PLTS and about 3,000 workers. PT CATIB is a joint venture "
            "of Indonesia Battery Corporation and the CATL-Brunp-Lygend "
            "consortium. The plant is part of the integrated EV battery "
            "ecosystem whose groundbreaking was on 29 June 2025; the ecosystem "
            "is described as a PSN but CATIB is absent from the current "
            "226-row register, so psn=unknown."
        ),
        "source": SRC_CATIB,
        "aliases": [
            (
                "Pabrik Baterai EV Karawang",
                SRC_CATIB,
                "ANTARA headline name.",
            ),
            (
                "PT CATIB",
                SRC_CATIB,
                "Project company.",
            ),
        ],
        "claims": [
            (
                SRC_CATIB,
                "status",
                "operating (gradual)",
                "2026-08-21",
                "Construction complete; gradual operation started; "
                "inauguration awaiting a presidential schedule.",
            ),
            (
                SRC_CATIB,
                "location",
                "Artha Industrial Hills, Karawang, West Java",
                "2026-08-21",
                "",
            ),
            (
                SRC_CATIB,
                "capacity",
                "6.9 GWh/yr",
                "2026-08-21",
                "",
            ),
            (
                SRC_CATIB,
                "investment",
                "about Rp7T",
                "2026-08-21",
                "",
            ),
            (
                SRC_CATIB,
                "opening",
                "2026 (gradual operation)",
                "2026-08-21",
                "Construction is complete and gradual operation has started; "
                "no exact date is stated and the inauguration was awaiting a "
                "presidential schedule.",
            ),
            (
                SRC_CATIB,
                "operator",
                "PT Contemporary Amperex Technology Indonesia Battery (CATIB)",
                "2026-08-21",
                "The project company operates the plant; the workforce is "
                "recorded as an indicator.",
            ),
            (
                SRC_CATIB,
                "output",
                "18 MWh PLTS",
                "2026-08-21",
                "On-site solar plant for operations.",
            ),
        ],
    },
    {
        "id": "energy-b50-biodiesel",
        "name": "B50 Biodiesel Programme",
        "name_id": "Program Mandatori Biodiesel B50",
        "sector": "energy",
        "subsector": "biofuel",
        "status": "operating",
        "status_basis": (
            "ESDM launched B50 on 9 July 2026 and the 50% blend mandate is in "
            "force."
        ),
        "island": "National",
        "province": "Indonesia",
        "route": "National",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "",
        "capacity": "",
        "capacity_unit": "",
        "psn": "no",
        "opened_year": "2026",
        "opened_date": "2026-07-09",
        "expected_open_year": "",
        "status_as_of": "2026-07-10",
        "verification": "official",
        "lat": "-2.50",
        "lon": "118.09",
        "precision": "province",
        "notes": (
            "ESDM launched B50 on 9 July 2026. The programme blends 50% "
            "biodiesel into diesel and is projected to save Rp170T of foreign "
            "exchange, raise CPO demand from 15.2 to 16.3 Mt, lift CPO value "
            "added from Rp20.92T to Rp23.49T, raise workers from 1.8 to 2.1 "
            "million, and cut emissions from 39.66 to 44.46 Mt CO2. National "
            "diesel consumption is 38-40 million kL/yr, with 3-4 million kL "
            "previously imported. This is a national programme-level record, "
            "not a single facility. The map point is a national centroid, not "
            "a site."
        ),
        "source": SRC_B50,
        "aliases": [
            ("B50", SRC_B50, "Programme short name."),
            (
                "Biodiesel B50",
                SRC_B50,
                "Common programme name.",
            ),
        ],
        "claims": [
            (
                SRC_B50,
                "status",
                "operating",
                "2026-07-10",
                "Launched on 9 July 2026.",
            ),
            (
                SRC_B50,
                "opening",
                "2026-07-09",
                "2026-07-10",
                "Launch date.",
            ),
            (SRC_B50, "location", "Indonesia", "2026-07-10", ""),
            (
                SRC_B50,
                "design capacity",
                "50% biodiesel blend",
                "2026-07-10",
                "",
            ),
            (
                SRC_B50,
                "target",
                "Rp170T foreign-exchange saving",
                "2026-07-10",
                "",
            ),
            (
                SRC_B50,
                "output",
                "44.46 Mt CO2 reduction",
                "2026-07-10",
                "Up from 39.66 Mt under B40; the workforce is recorded as an "
                "indicator.",
            ),
        ],
    },
    {
        "id": "rail-trans-sulawesi",
        "name": "Trans Sulawesi Railway",
        "name_id": "Kereta Api Trans Sulawesi",
        "sector": "railway",
        "subsector": "intercity rail",
        "status": "under_construction",
        "status_basis": (
            "Kemenhub describes the Makassar-Manado Trans Sulawesi railway as "
            "a mega-project; the 90 km Maros-Barru section is operating while "
            "the wider corridor remains under construction."
        ),
        "island": "Sulawesi",
        "province": "South Sulawesi",
        "route": "Makassar-Parepare-Manado, Sulawesi",
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "",
        "capacity": "",
        "capacity_unit": "",
        "psn": "unknown",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": "2026-06-12",
        "verification": "official",
        "lat": "-4.58",
        "lon": "119.53",
        "precision": "approximate",
        "notes": (
            "Kemenhub describes the Makassar-Manado Trans Sulawesi railway as "
            "a mega-project and the 150 km Makassar-Parepare section as its "
            "first part. By April 2023, 118 km of the 157.7 km "
            "Makassar-Parepare alignment had been built and 90 km of the "
            "Maros-Barru section was operating. Kemenhub still listed "
            "completion of Makassar-Parepare operations as a priority in June "
            "2026. This umbrella record covers the operating segment and "
            "planned extensions. The PSN register lists only the "
            "Makassar-Parepare stage (No. 73), so psn=unknown. The map point is "
            "Makassar, the southern terminus."
        ),
        "source": SRC_TRANS_SULAWESI,
        "aliases": [
            (
                "Jalan Baja Trans Sulawesi",
                SRC_TRANS_SULAWESI,
                "Kemenhub calls it the trans Sulawesi rail mega-project.",
            ),
            (
                "KA Trans Sulawesi",
                SRC_TRANS_SULAWESI,
                "Short form.",
            ),
        ],
        "claims": [
            (
                SRC_RAIL_NETWORK,
                "status",
                "under_construction",
                "2026-06-12",
                "Kemenhub still lists completion of Makassar-Parepare "
                "operations as a priority.",
            ),
            (
                SRC_TRANS_SULAWESI,
                "status",
                "under_construction",
                "2023-04-05",
                "Umbrella over the operating Maros-Barru segment and planned "
                "extensions.",
            ),
            (
                SRC_TRANS_SULAWESI,
                "location",
                "Makassar-Parepare-Manado, Sulawesi",
                "2023-04-05",
                "",
            ),
            (
                SRC_TRANS_SULAWESI,
                "operational",
                "90 km Maros-Barru operating",
                "2023-04-05",
                "",
            ),
            (
                SRC_TRANS_SULAWESI,
                "progress",
                "118 km built of the 157.7 km Makassar-Parepare section",
                "2023-04-05",
                "",
            ),
            (
                SRC_TRANS_SULAWESI,
                "length",
                "150 km Makassar-Parepare section",
                "2023-04-05",
                "",
            ),
        ],
    },
]

# id, project_id, programme_id, name_en, name_id, unit, direction, value,
# as_of, source, notes.
INDICATORS = [
    (
        "ind-bontang-refinery-capacity", "factory-bontang-refinery", "",
        "Bontang refinery capacity", "Kapasitas Kilang Bontang",
        "bpd", "increase", "300000", REVIEWED, SRC_BONTANG,
        "Minimum 300,000 barrels per day.",
    ),
    (
        "ind-sumatra-500kv-length", "grid-sumatra-500kv", "",
        "Sumatra 500 kV line length", "Panjang Transmisi Sumatera 500 kV",
        "km", "increase", "1330", REVIEWED, SRC_SUMATRA,
        "1,330 km from Muara Enim to Langsa.",
    ),
    (
        "ind-central-west-java-500kv-length", "grid-central-west-java-500kv", "",
        "Central-West Java 500 kV line length",
        "Panjang Transmisi Jawa Tengah-Jawa Barat 500 kV",
        "km", "increase", "981", REVIEWED, SRC_CENTRAL_WEST_JAVA,
        "Four sections of 144, 397, 180 and 260 km.",
    ),
    (
        "ind-indramayu-capacity", "power-pltu-indramayu", "",
        "Indramayu planned capacity", "Kapasitas rencana PLTU Indramayu",
        "MW", "increase", "1000", REVIEWED, SRC_INDRAMAYU,
        "1,000 MW at the preparation stage.",
    ),
    (
        "ind-batang-capacity", "power-pltu-batang", "",
        "Batang installed capacity", "Kapasitas terpasang PLTU Batang",
        "MW", "increase", "2000", "2022-09-06", SRC_BPI,
        "2 x 1,000 MW in commercial operation.",
    ),
    (
        "ind-kertajati-capacity", "airport-kertajati", "",
        "Kertajati passenger capacity", "Kapasitas penumpang Kertajati",
        "passengers/yr", "increase", "12000000", "2023-11-01", SRC_KERTAJATI,
        "Upper bound of the 5.6-12 million passengers/yr range to 2024.",
    ),
    (
        "ind-kertajati-terminal-area", "airport-kertajati", "",
        "Kertajati passenger terminal area", "Luas terminal penumpang Kertajati",
        "m2", "increase", "121000", "2023-11-01", SRC_KERTAJATI,
        "Passenger terminal; the cargo terminal is 90,000 m2.",
    ),
    (
        "ind-batang-toru-capacity", "power-batang-toru", "",
        "Batang Toru installed capacity", "Kapasitas terpasang PLTA Batang Toru",
        "MW", "increase", "510", "2026-10-10", SRC_BATANG_TORU,
        "510 MW from four 127.5 MW units.",
    ),
    (
        "ind-batang-toru-phase-2", "power-batang-toru", "",
        "Batang Toru second-phase capacity",
        "Kapasitas tahap kedua PLTA Batang Toru",
        "MW", "target", "160", "2026-10-10", SRC_BATANG_TORU,
        "Second-phase study prepared by NSHE.",
    ),
    (
        "ind-sodetan-length", "flood-sodetan-ciliwung", "",
        "Sodetan Ciliwung tunnel length", "Panjang terowongan Sodetan Ciliwung",
        "km", "increase", "1.268", "2023-08-01", SRC_SODETAN,
        "1,268 m tunnel.",
    ),
    (
        "ind-sodetan-capacity", "flood-sodetan-ciliwung", "",
        "Sodetan Ciliwung flow capacity", "Kapasitas aliran Sodetan Ciliwung",
        "m3/s", "increase", "60", "2023-08-01", SRC_SODETAN,
        "Two 3.5 m pipes.",
    ),
    (
        "ind-sodetan-flood-area", "flood-sodetan-ciliwung", "",
        "Flood area removed by Sodetan Ciliwung",
        "Luas banjir yang dikurangi Sodetan Ciliwung",
        "ha", "increase", "107", "2023-08-01", SRC_SODETAN,
        "107 ha reduction in flood-affected area.",
    ),
    (
        "ind-ciliwung-length", "flood-ciliwung-normalisation", "",
        "Ciliwung normalisation scope", "Lingkup normalisasi Ciliwung",
        "km", "increase", "33", "2023-02-21", SRC_CILIWUNG,
        "33 km total scope.",
    ),
    (
        "ind-ciliwung-completed", "flood-ciliwung-normalisation", "",
        "Ciliwung normalisation completed length",
        "Panjang normalisasi Ciliwung selesai",
        "km", "increase", "16.19", "2023-02-21", SRC_CILIWUNG,
        "16.19 km completed; the remaining 17 km were targeted for end-2024.",
    ),
    (
        "ind-ciliwung-capacity", "flood-ciliwung-normalisation", "",
        "Ciliwung normalised flow capacity",
        "Kapasitas aliran normalisasi Ciliwung",
        "m3/s", "increase", "570", "2023-02-21", SRC_CILIWUNG,
        "Up from 200 m3/s.",
    ),
    (
        "ind-pengambengan-vessels", "port-ppn-pengambengan", "",
        "Pengambengan vessel capacity", "Kapasitas kapal Pengambengan",
        "vessels", "increase", "1600", "2026-09-29", SRC_PENGAMBENGAN,
        "Up from 1,273 vessels.",
    ),
    (
        "ind-pengambengan-landings", "port-ppn-pengambengan", "",
        "Pengambengan fish landings", "Pendaratan ikan Pengambengan",
        "t/yr", "increase", "124000", "2026-09-29", SRC_PENGAMBENGAN,
        "Up from 61,300 t/yr.",
    ),
    (
        "ind-pengambengan-area", "port-ppn-pengambengan", "",
        "Pengambengan port area", "Luas pelabuhan Pengambengan",
        "ha", "increase", "49.3", "2026-09-29", SRC_PENGAMBENGAN,
        "Up from 13.5 ha.",
    ),
    (
        "ind-pengambengan-workers", "port-ppn-pengambengan", "",
        "Pengambengan workers", "Tenaga kerja Pengambengan",
        "workers", "increase", "25000", "2026-09-29", SRC_PENGAMBENGAN,
        "About 25,000 workers, nearly three times the current workforce.",
    ),
    (
        "ind-pengambengan-pnbp", "port-ppn-pengambengan", "",
        "Pengambengan annual PNBP", "PNBP tahunan Pengambengan",
        "IDR bn/yr", "increase", "104", "2026-09-29", SRC_PENGAMBENGAN,
        "Up from Rp48bn/yr.",
    ),
    (
        "ind-kejawanan-vessels", "port-ppn-kejawanan", "",
        "Kejawanan vessel capacity", "Kapasitas kapal Kejawanan",
        "vessels", "increase", "500", "2026-09-18", SRC_KEJAWANAN,
        "Up from 241 vessels.",
    ),
    (
        "ind-kejawanan-landings", "port-ppn-kejawanan", "",
        "Kejawanan fish landings", "Pendaratan ikan Kejawanan",
        "t/yr", "increase", "32000", "2026-09-18", SRC_KEJAWANAN,
        "Up from 5,600 t/yr.",
    ),
    (
        "ind-kejawanan-workers", "port-ppn-kejawanan", "",
        "Kejawanan workers", "Tenaga kerja Kejawanan",
        "workers", "increase", "8000", "2026-09-18", SRC_KEJAWANAN,
        "Up from about 2,900.",
    ),
    (
        "ind-kejawanan-pnbp", "port-ppn-kejawanan", "",
        "Kejawanan annual PNBP", "PNBP tahunan Kejawanan",
        "IDR bn/yr", "increase", "53", "2026-09-18", SRC_KEJAWANAN,
        "Up from Rp15bn/yr.",
    ),
    (
        "ind-catib-capacity", "factory-catib-karawang", "",
        "CATIB phase 1 capacity", "Kapasitas tahap 1 CATIB",
        "GWh/yr", "increase", "6.9", "2026-08-21", SRC_CATIB,
        "Phase 1 battery cell capacity.",
    ),
    (
        "ind-catib-workers", "factory-catib-karawang", "",
        "CATIB workers", "Tenaga kerja CATIB",
        "workers", "increase", "3000", "2026-08-21", SRC_CATIB,
        "About 3,000 workers at full operation.",
    ),
    (
        "ind-catib-solar", "factory-catib-karawang", "",
        "CATIB on-site solar capacity", "Kapasitas PLTS CATIB",
        "MWh", "increase", "18", "2026-08-21", SRC_CATIB,
        "18 MWh PLTS for operations.",
    ),
    (
        "ind-b50-fx-saving", "energy-b50-biodiesel", "",
        "B50 foreign-exchange saving", "Penghematan devisa B50",
        "IDR T/yr", "increase", "170", "2026-07-10", SRC_B50,
        "Projected saving from ending diesel imports.",
    ),
    (
        "ind-b50-workers", "energy-b50-biodiesel", "",
        "B50 workers", "Tenaga kerja B50",
        "million workers", "increase", "2.1", "2026-07-10", SRC_B50,
        "Up from 1.8 million under B40.",
    ),
    (
        "ind-b50-emissions", "energy-b50-biodiesel", "",
        "B50 emissions reduction", "Penurunan emisi B50",
        "Mt CO2/yr", "increase", "44.46", "2026-07-10", SRC_B50,
        "Up from 39.66 Mt under B40.",
    ),
    (
        "ind-trans-sulawesi-operating", "rail-trans-sulawesi", "",
        "Trans Sulawesi operating length", "Panjang Trans Sulawesi beroperasi",
        "km", "increase", "90", "2023-04-05", SRC_TRANS_SULAWESI,
        "90 km of the Maros-Barru section operating.",
    ),
    (
        "ind-trans-sulawesi-built", "rail-trans-sulawesi", "",
        "Trans Sulawesi built length", "Panjang Trans Sulawesi terbangun",
        "km", "increase", "118", "2023-04-05", SRC_TRANS_SULAWESI,
        "118 km built of the 157.7 km Makassar-Parepare alignment.",
    ),
    (
        "ind-trans-sulawesi-segment", "rail-trans-sulawesi", "",
        "Makassar-Parepare segment length",
        "Panjang ruas Makassar-Parepare",
        "km", "increase", "150", "2023-04-05", SRC_TRANS_SULAWESI,
        "150 km Makassar-Parepare section.",
    ),
]

# programme, project, role, source, notes
PROGRAMME_LINKS = [
    (
        PROGRAMME_ELECTRICITY, "grid-sumatra-500kv", "component", SRC_SUMATRA,
        "500 kV transmission project listed on the KPPIP priority page.",
    ),
    (
        PROGRAMME_ELECTRICITY, "grid-central-west-java-500kv", "component",
        SRC_CENTRAL_WEST_JAVA,
        "500 kV transmission project listed on the KPPIP priority page.",
    ),
    (
        PROGRAMME_ELECTRICITY, "power-pltu-indramayu", "component",
        SRC_INDRAMAYU,
        "1,000 MW coal plant listed on the KPPIP priority page.",
    ),
    (
        PROGRAMME_ELECTRICITY, "power-pltu-batang", "component", SRC_BATANG,
        "2x1,000 MW coal plant listed on the KPPIP priority page.",
    ),
    (
        PROGRAMME_ELECTRICITY, "power-batang-toru", "component",
        SRC_BATANG_TORU,
        "510 MW hydropower plant under construction.",
    ),
    (
        PROGRAMME_JAKARTA_FLOOD, "flood-sodetan-ciliwung", "component",
        SRC_SODETAN,
        "Ciliwung diversion tunnel inaugurated in 2023.",
    ),
    (
        PROGRAMME_JAKARTA_FLOOD, "flood-ciliwung-normalisation", "component",
        SRC_CILIWUNG,
        "Ciliwung normalisation under construction.",
    ),
    (
        PROGRAMME_AVIATION, "rail-shia-express", "component", SRC_SHIA,
        "Airport rail access to Soekarno-Hatta.",
    ),
    (
        PROGRAMME_AVIATION, "airport-north-bali", "component", SRC_NORTH_BALI,
        "New airport at the preparation stage.",
    ),
    (
        PROGRAMME_AVIATION, "airport-kertajati", "component", SRC_KERTAJATI,
        "Kertajati airport in full operation since 2023.",
    ),
    (
        PROGRAMME_SUPERHUB, "port-cbl-inland-waterway", "component", SRC_CBL,
        "Inland waterway link to Tanjung Priok.",
    ),
    (
        PROGRAMME_FOOD, "port-ppn-pengambengan", "component", SRC_PENGAMBENGAN,
        "Fishing port modernisation.",
    ),
    (
        PROGRAMME_FOOD, "port-ppn-kejawanan", "component", SRC_KEJAWANAN,
        "Fishing port modernisation.",
    ),
    (
        PROGRAMME_PALM, "energy-b50-biodiesel", "component", SRC_B50,
        "National B50 biodiesel mandate.",
    ),
]

# programme, source, claim, value, date, notes
PROGRAMME_CLAIMS = [
    (
        PROGRAMME_ELECTRICITY, SRC_BATANG, "capacity", "2,000 MW", REVIEWED,
        "Batang plant capacity.",
    ),
    (
        PROGRAMME_ELECTRICITY, SRC_BATANG_TORU, "capacity", "510 MW",
        "2026-10-10", "Batang Toru capacity under construction.",
    ),
    (
        PROGRAMME_JAKARTA_FLOOD, SRC_SODETAN, "capacity", "60 m3/s",
        "2023-08-01", "Sodetan Ciliwung diversion capacity.",
    ),
    (
        PROGRAMME_JAKARTA_FLOOD, SRC_CILIWUNG, "capacity", "570 m3/s",
        "2023-02-21", "Ciliwung normalisation target capacity.",
    ),
    (
        PROGRAMME_AVIATION, SRC_KERTAJATI, "capacity",
        "12 million passengers/yr (upper bound)", "2023-11-01",
        "Kertajati upper bound of the 5.6-12 million range to 2024.",
    ),
    (
        PROGRAMME_FOOD, SRC_PENGAMBENGAN, "capacity", "1,600 vessels",
        "2026-09-29", "Pengambengan vessel capacity after expansion.",
    ),
    (
        PROGRAMME_FOOD, SRC_KEJAWANAN, "capacity", "500 vessels",
        "2026-09-18", "Kejawanan vessel capacity after expansion.",
    ),
    (
        PROGRAMME_PALM, SRC_B50, "design capacity", "50% biodiesel blend",
        "2026-07-10", "National B50 mandate.",
    ),
    (
        PROGRAMME_SUPERHUB, SRC_CBL, "investment", "Rp3.41T", REVIEWED,
        "CBL inland waterway investment.",
    ),
]

# project, organisation, role, source, notes
ORG_LINKS = [
    (
        "factory-bontang-refinery", ORG_PERTAMINA, "owner", SRC_BONTANG,
        "Pertamina is the responsible party named on the KPPIP page.",
    ),
    (
        "grid-sumatra-500kv", ORG_PLN, "operator", SRC_SUMATRA,
        "PLN is the responsible party named on the KPPIP page.",
    ),
    (
        "grid-central-west-java-500kv", ORG_PLN, "operator",
        SRC_CENTRAL_WEST_JAVA,
        "PLN is the responsible party named on the KPPIP page.",
    ),
    (
        "power-pltu-indramayu", ORG_PLN, "owner", SRC_INDRAMAYU,
        "PLN is the responsible party named on the KPPIP page.",
    ),
    (
        "power-pltu-batang", ORG_PLN, "off_taker", SRC_BPI,
        "BPI sells the plant's output to PLN under a 25-year contract.",
    ),
    (
        "port-cbl-inland-waterway", ORG_PELINDO, "owner", SRC_CBL,
        "Pelindo II is the responsible party named on the KPPIP page; it is "
        "now part of PT Pelabuhan Indonesia (Persero).",
    ),
    (
        "flood-sodetan-ciliwung", ORG_KEMENTERIAN_PU, "sponsor", SRC_SODETAN,
        "PU built and inaugurated the diversion.",
    ),
    (
        "flood-ciliwung-normalisation", ORG_KEMENTERIAN_PU, "sponsor",
        SRC_CILIWUNG,
        "PU is normalising the river.",
    ),
    (
        "port-ppn-pengambengan", ORG_KEMENTERIAN_KKP, "sponsor",
        SRC_PENGAMBENGAN,
        "KKP is developing the fishing port.",
    ),
    (
        "port-ppn-kejawanan", ORG_KEMENTERIAN_KKP, "sponsor", SRC_KEJAWANAN,
        "KKP is developing the fishing port.",
    ),
    (
        "energy-b50-biodiesel", ORG_KEMENTERIAN_ESDM, "sponsor", SRC_B50,
        "ESDM launched the B50 mandate.",
    ),
]


def project_row(item: dict) -> dict:
    return {
        "id": item["id"],
        "name": item["name"],
        "sector": item["sector"],
        "subsector": item["subsector"],
        "status": item["status"],
        "status_basis": item["status_basis"],
        "corridor_id": "",
        "island": item["island"],
        "province": item["province"],
        "route": item["route"],
        "length_km": item["length_km"],
        "operational_km": item["operational_km"],
        "construction_km": item["construction_km"],
        "progress_pct": item["progress_pct"],
        "investment_idr_t": item["investment_idr_t"],
        "capacity": item["capacity"],
        "capacity_unit": item["capacity_unit"],
        "psn": item["psn"],
        "opened_year": item["opened_year"],
        "opened_date": item["opened_date"],
        "expected_open_year": item["expected_open_year"],
        "status_as_of": item["status_as_of"],
        "verification": item["verification"],
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
    for item in RECORDS:
        if item["id"] not in existing_projects:
            projects.append(project_row(item))
            existing_projects.add(item["id"])
    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)

    claims = read_csv(CURATED / "project_sources.csv")
    claim_keys = {
        (row["project_id"], row["source_id"], row["claim"]) for row in claims
    }
    for item in RECORDS:
        for source_id, claim, value, date, notes in item["claims"]:
            key = (item["id"], source_id, claim)
            if key in claim_keys:
                continue
            claims.append(
                {
                    "project_id": item["id"],
                    "source_id": source_id,
                    "claim": claim,
                    "claim_value": value,
                    "claim_date": date,
                    "notes": notes,
                }
            )
            claim_keys.add(key)
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)

    programme_links = read_csv(CURATED / "programme_projects.csv")
    link_keys = {
        (row["programme_id"], row["project_id"], row["role"])
        for row in programme_links
    }
    for programme_id, project_id, role, source_id, notes in PROGRAMME_LINKS:
        key = (programme_id, project_id, role)
        if key in link_keys:
            continue
        programme_links.append(
            {
                "programme_id": programme_id,
                "project_id": project_id,
                "role": role,
                "source_id": source_id,
                "notes": notes,
            }
        )
        link_keys.add(key)
    write_csv(
        CURATED / "programme_projects.csv",
        PROGRAMME_PROJECT_FIELDS,
        programme_links,
    )

    org_links = read_csv(CURATED / "project_organizations.csv")
    org_keys = {
        (row["project_id"], row["org_id"], row["role"]) for row in org_links
    }
    for project_id, org_id, role, source_id, notes in ORG_LINKS:
        key = (project_id, org_id, role)
        if key in org_keys:
            continue
        org_links.append(
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
        org_keys.add(key)
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, org_links)

    aliases = read_csv(CURATED / "project_aliases.csv")
    alias_keys = {(row["project_id"], row["alias"]) for row in aliases}
    for item in RECORDS:
        for alias, source_id, notes in item["aliases"]:
            key = (item["id"], alias)
            if key in alias_keys:
                continue
            aliases.append(
                {
                    "project_id": item["id"],
                    "alias": alias,
                    "source_id": source_id,
                    "notes": notes,
                }
            )
            alias_keys.add(key)
    write_csv(CURATED / "project_aliases.csv", ALIAS_FIELDS, aliases)

    translations = read_csv(CURATED / "translations.csv")
    translation_keys = {
        (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        for row in translations
    }
    for item in RECORDS:
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
                "source_id": item["source"],
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
        if key in value_keys:
            continue
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
    write_csv(
        CURATED / "programme_sources.csv",
        PROGRAMME_SOURCE_FIELDS,
        programme_claims,
    )

    coverage = read_csv(CURATED / "coverage_targets.csv")
    strategic = [row for row in projects if row["psn"] != "yes"]
    no_count = sum(1 for row in strategic if row["psn"] == "no")
    unknown_count = sum(1 for row in strategic if row["psn"] == "unknown")
    for row in coverage:
        if row["layer"] != "strategic_records":
            continue
        row["notes"] = (
            f"{len(strategic)} project rows outside the PSN list at 13 November "
            f"2026; target met. The layer counts project rows with psn=no or "
            f"psn=unknown, including {no_count} psn=no and {unknown_count} "
            "psn=unknown rows."
        )
    write_csv(CURATED / "coverage_targets.csv", COVERAGE_FIELDS, coverage)

    print(
        f"Added {len(RECORDS)} strategic records, {len(NEW_SOURCES)} sources, "
        f"{len(INDICATORS)} indicators, {len(PROGRAMME_LINKS)} programme links "
        f"and {len(ORG_LINKS)} organisation links (idempotent)."
    )


if __name__ == "__main__":
    main()

