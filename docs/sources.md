# Sources and provenance

The source register is [`data/curated/sources.csv`](../data/curated/sources.csv).
Each row records publisher, title, URL, publication date, retrieval date, source
type, language, snapshot hash, archive path and notes. Raw snapshots live under
`data/raw/<YYYY-MM-DD>/` and are never edited.

Current register: **140 sources** — 58 official, 55 secondary and 27 company.

## Source types

| Type | Use |
|---|---|
| `official` | Ministry, agency, presidential or regional government publication |
| `secondary` | Reputable reporting, Wikipedia or a research organisation |
| `company` | Company release, annual report, profile or project page |
| `multilateral` | Multilateral development bank or international organisation |

A status change needs an official source or two independent sources. Secondary
sources are used for discovery and cross-checks, never as the sole authority for
a status change when an official source exists.

## Main sources

| Source | URL / access | Used for | Caveats |
|---|---|---|---|
| BPJT toll-road API | <https://itrams-api.bpjt.pu.go.id/v1/reference/api/toll-road-list> | Official status, operating/construction km, operator, endpoint coordinates | 77 operating or partly operating rows; construction-only rows absent; status labels inconsistent |
| English Wikipedia, "Indonesian Toll Road System", revision 1329385293 (2025-12-25) | <https://en.wikipedia.org/w/index.php?oldid=1329385293> | Route names, lengths, operators, status markers | Secondary and stale in places; no coordinates or opening years |
| Indonesian Wikipedia, "Daftar jalan tol di Indonesia", oldid 30025554 (2026-10-03) | <https://id.wikipedia.org/w/index.php?oldid=30025554> | Cross-check of lengths, operating km and concessions | Secondary; figures often differ from BPJT |
| Kemenhub, "Capaian Progres PSN Sektor Transportasi" (19 Feb 2026) | <https://ppid.kemenhub.go.id/fileupload/informasi-berkala/20260406102830.R1_19022026_Update_PSN_Kemenhub_compressed.pdf> | Transport PSN status, opening years, progress, investment | 35 transport PSNs; 29 complete or operating, 6 in construction |
| KPPIP PSN pages | <https://kppip.go.id/proyek-strategis-nasional/> | Airport, seaport and industrial-area PSN lists | Names and provinces only; status must come from elsewhere |
| Hutama Karya via Palpres (4 Oct 2026) | <https://palpres.disway.id/news/read/780474/hutama-karya-buka-bukaan-soal-jtts-di-hadapan-bakn-dpr-ri-ini-progresnya> | Trans Sumatra km | Secondary; figures differ by scope and date |
| BPJT section list via detikFinance (26 Jan 2025) | <https://finance.detik.com/infrastruktur/d-7750531/tol-trans-jawa-belum-tersambung-penuh-masih-ada-sisa-ruas-ini> | Trans Java 20-section operating series | Secondary reporting of BPJT data; article prints 1,232.78 km, section sum is 1,232.80 km |
| Kementerian Sekretariat Negara (20 Dec 2018) | <https://setneg.go.id/baca/index/presiden_resmikan_4_ruas_jalan_tol_trans_jawa_di_jawa_timur> | East Java section-opening event | Official; one event covers four sections and is attached to the Ngawi–Kertosono–Kediri row |
| Katadata (21 Jul 2025) | <https://katadata.co.id/berita/industri/687e4748a975f/tni-targetkan-proyek-trans-papua-rampung-di-era-prabowo> | Trans Papua km | Secondary; connected vs paved metrics differ |
| Wikipedia Trans corridor revisions (2026) | <https://en.wikipedia.org/wiki/Trans-Papua_Highway> | Trans Java, Sulawesi, Kalimantan and Papua definitions, section lengths and opening years | Secondary; used for discovery and cross-checks, never for a status change |
| KEK National Council profiles (25 pages) | <https://kek.go.id/id/investment/distribution> | SEZ name, address, coordinates, area, developer, legal basis, category | Official; one page per zone. Operational maturity is not stated |
| Kemenperin estate directory (2026) | <https://kemenperin.go.id/kawasan> | Industrial estate name, manager, regency/province and land area | Official; 181 rows. It does not state operational status or coordinates |
| BAJRA, "Daftar Kawasan Industri Indonesia" (17 Aug 2024) | <https://www.bajra.id/2024/08/daftar-kawasan-industri-indonesia.html> | Industrial estate name, developer, regency, province, area | Secondary mirror of Kemenperin data; 159 estates, not the 179 reported in 2026 |
| PSN industrial-area batch (2024–2026) | Pelindo, Waspada, DPN, Rebana, Indonesiana, Luwu Timur, Neo Energy, ANTARA, GEM and OSM/Nominatim | Area, manager, status and place points for Kuala Tanjung, Bantaeng, Pomalaa, Huali, Patimban, NEMIE, Pulau Penebang and Alumina Toba | Each row names its own dated source; developer master-plan areas can exceed the licensed Kemenperin area |
| ANTARA, Kemenperin estate count (2026) | <https://www.antaranews.com/berita/5627392/kemenperin-catat-kawasan-industri-serap-235-juta-pekerja> | Coverage benchmark: 179 estates, 101,351.45 ha, 57.20% occupancy | Secondary; used only as a benchmark, not as a row source |
| Permenko 16/2025 | <https://www.peraturan.go.id/files/permenko-perekonomian-no-16-tahun-2025.pdf> | Official PSN list: 226 active projects, 24 active programmes | The annex does not state budgets, targets or status |
| Permenko 4/2026 | <https://peraturan.bpk.go.id/Download/418980/2026PermenkoEkon004.pdf> | Amendment to the smelter programme | Does not change the 226-project list |
| 2027 budget speech (14 Aug 2026) | <https://www.setneg.go.id/baca/index/pidato_presiden_pada_penyampaian_keterangan_pemerintah_atas_ruu_tentang_apbn_tahun_anggaran_2027_beserta_nota_keuangannya_di_depan_rapat_paripurna_dpr_ri> | Eight PKPN, health, education and energy targets | Targets are annual or programme-level; no project splits |
| Finance Ministry PKPN breakdown (16 Sep 2026) | <https://mediakeuangan.kemenkeu.go.id/article/show/ini-rincian-8-program-kerja-prioritas-nasional-pkpn-dalam-rapbn-2027> | PKPN budgets and delivery targets | Secondary official explainer; use the speech for the legal text |
| Two-year delivery report (20 Oct 2026) | <https://setkab.go.id/seskab-teddy-bagikan-sekilas-cuplikan-hasil-nyata-2-tahun-pemerintahan/> | Education, health, housing, irrigation, bridges, roads, boreholes, fishing villages and downstreaming delivery figures | Headline achievements; no targets for most measures |
| Kemendikdasmen two-year release (27 Oct 2026) | <https://www.kemendikdasmen.go.id/siaran-pers/16362-dua-tahun-pemerintahan-prabowogibran-kemendikdasmen-perluas-akses-dan-perkuat-mutu-pendidikan> | School digitalisation, electricity, internet and SNT figures | Some figures are 2025 or 2026; read each note |
| Natural Earth 1:50m countries, provinces, lakes, rivers, urban areas and populated places | <https://www.naturalearthdata.com/> | Basemap layers and city labels | Public domain; clipped and simplified |
| OpenStreetMap / Nominatim | <https://nominatim.openstreetmap.org/> | Point coordinates for estates and factories | © OpenStreetMap contributors, ODbL 1.0. Points are not boundaries |

## Raw snapshots

| Directory | Contents |
|---|---|
| `data/raw/2026-11-06/` | Wikipedia snapshots, BPJT JSON, Kemenhub PDF, KPPIP HTML, 25 KEK profiles, BAJRA estate table and Natural Earth GeoJSON |
| `data/raw/2026-11-09/` | Permenko 16/2025 and 4/2026, Kemenperin directory, PSN industrial-area sources, 2027 budget speech, Finance Ministry PKPN breakdown, two-year delivery report, Kemendikdasmen release and IKN Stage II sources |

Each snapshot directory has a `manifest.json` with URLs, byte sizes and SHA-256
hashes where applicable, plus a `README.md` describing the batch.

## Archive rules

1. Save the page or PDF before parsing it.
2. Hash the file with SHA-256 and record the hash in `sources.csv`.
3. Record the retrieval date, not just the publication date.
4. If a page cannot be archived, record why in `notes`.
5. Do not edit a raw snapshot to fix a parse. Add a corrected extraction as a new
   derived file and document the transformation.
6. When two sources disagree, add a `conflicts.csv` row with both values and both
   source IDs. Do not resolve it silently.

## Known coverage gaps

- RPJMN 2025–2029 and the current Bappenas planning documents are not yet
  archived.
- Some KPPIP sector pages are not archived.
- Budget speeches beyond the two PKPN snapshots are not yet archived.
- Some flagship and road sources are registered by URL but lack a local snapshot.
- IKN Authority returns HTTP 403 to some clients; the archived Top Konstruksi
  report reproduces the same OIKN evaluation.
- The Dishub Sanggau page for Alumina Toba returns HTTP 500; GEM and Kemenperin
  sources are archived instead.

The remaining source work is tracked in
[`docs/plan/plan.md`](plan/plan.md#43-sources--110-documents).
