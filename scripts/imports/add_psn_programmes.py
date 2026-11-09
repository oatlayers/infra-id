"""Add the 24 active PSN programmes and their first delivery links.

The programme layer is the first part of schema v4. Each row is keyed to the
official programme number in Permenko 16/2025, and the script reads the official
Indonesian name from ``psn_register.csv`` instead of retyping it. A mismatch in
the register stops the import.

The annex does not state budgets, targets or indicators, so those fields stay
blank rather than being filled from unrelated reporting. Programme claims record
only the two facts the annex supports: that the record is a PSN programme and
that it is active. Project links are structural examples where the programme
clearly names the activity; they are not a complete membership list.

Run: python scripts/imports/add_psn_programmes.py
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
    ORG_FIELDS,
    PROGRAMME_FIELDS,
    PROGRAMME_PROJECT_FIELDS,
    PROGRAMME_SOURCE_FIELDS,
    read_csv,
    write_csv,
)

RETRIEVED = "2026-11-09"
LAST_VERIFIED = "2026-11-09"
REGULATION_DATE = "2025-09-24"
SOURCE_ID = "src-permenko-16-2025"

NOTE = (
    "Official programme name and active status from Permenko 16/2025. The annex "
    "does not state a budget, target or indicator, so those fields stay blank "
    "until a dated official source is added."
)

# psn_no, id, English name, theme, PKPN, lead organisation, English summary,
# Indonesian summary.
PROGRAMMES = [
    (1, "prog-electricity", "Electricity Programme", "energy", "pkpn-energy-water",
     "org-kementerian-esdm",
     "Covers national electricity generation, transmission and distribution policy and projects.",
     "Mencakup kebijakan dan proyek pembangkit, transmisi, serta distribusi tenaga listrik nasional."),
    (2, "prog-economic-equity", "Economic Equity Programme", "economy", "",
     "",
     "Groups measures to broaden economic participation and reduce regional inequality.",
     "Mengelompokkan langkah untuk memperluas partisipasi ekonomi dan mengurangi ketimpangan wilayah."),
    (3, "prog-border-areas", "Border Area Development Programme", "border",
     "pkpn-infrastructure", "org-bnpp",
     "Covers infrastructure and economic development in national border areas.",
     "Mencakup pembangunan infrastruktur dan ekonomi di kawasan perbatasan negara."),
    (4, "prog-toll-exit-access", "Toll Exit Access Road Development Programme",
     "transport", "pkpn-infrastructure", "org-kementerian-pu",
     "Builds and improves access roads at toll exits to connect toll corridors with surrounding areas.",
     "Membangun dan meningkatkan jalan akses di simpang susun tol agar terhubung dengan kawasan sekitarnya."),
    (5, "prog-national-tourism-areas",
     "National Strategic Tourism Area Development Programme", "tourism", "",
     "org-kementerian-pariwisata",
     "Develops national strategic tourism areas and their supporting infrastructure.",
     "Mengembangkan kawasan strategis pariwisata nasional beserta infrastruktur pendukungnya."),
    (7, "prog-smelters", "Smelter Development Programme", "industry",
     "pkpn-downstreaming", "",
     "Supports the construction of mineral and metal smelters and refining capacity.",
     "Mendukung pembangunan smelter dan kapasitas pemurnian mineral serta logam."),
    (8, "prog-food-supply", "National Food Supply Improvement Programme", "food",
     "pkpn-food", "org-kementerian-pertanian",
     "Groups programmes to raise national food production and supply.",
     "Mengelompokkan program untuk meningkatkan produksi dan penyediaan pangan nasional."),
    (9, "prog-superhub", "Superhub Development Programme", "transport",
     "pkpn-infrastructure", "org-kemenhub",
     "Develops multimodal superhub nodes linking sea, air and land transport.",
     "Mengembangkan simpul superhub multimoda yang menghubungkan transportasi laut, udara, dan darat."),
    (10, "prog-accelerated-regions", "Accelerated Regional Development Programme",
     "urban", "pkpn-infrastructure", "",
     "Accelerates development in regions designated for economic acceleration and in the national capital.",
     "Mempercepat pembangunan wilayah yang ditetapkan untuk percepatan ekonomi dan ibu kota negara."),
    (11, "prog-special-economic-zones", "Special Economic Zone Development Programme",
     "industry", "pkpn-downstreaming", "org-kemenko-perekonomian",
     "Develops and promotes special economic zones.",
     "Mengembangkan dan mempromosikan kawasan ekonomi khusus."),
    (12, "prog-sugar-palm-downstreaming",
     "National Sugar Industry Revitalisation and Palm Oil Downstreaming Programme",
     "industry", "pkpn-downstreaming", "",
     "Revitalises the national sugar industry and expands palm-oil downstreaming.",
     "Merevitalisasi industri gula nasional dan memperluas hilirisasi industri kelapa sawit."),
    (13, "prog-eco-city", "Eco-City Area Development Programme", "urban", "",
     "",
     "Develops eco-city areas with sustainable urban infrastructure.",
     "Mengembangkan kawasan eco-city dengan infrastruktur perkotaan yang berkelanjutan."),
    (14, "prog-tourism-aviation", "Tourism and Aviation Industry Growth Programme",
     "tourism", "", "",
     "Supports growth in the tourism and aviation industries.",
     "Mendukung pertumbuhan industri pariwisata dan penerbangan."),
    (15, "prog-toll-operation", "Toll Road Operation and Modernisation Programme",
     "transport", "pkpn-infrastructure", "org-kementerian-pu",
     "Covers the operation, maintenance and modernisation of toll roads.",
     "Mencakup pengoperasian, pemeliharaan, dan modernisasi jalan tol."),
    (16, "prog-jakarta-flood-control",
     "Jakarta Flood Control, Congestion and Liveability Programme", "water",
     "pkpn-infrastructure", "org-kementerian-pu",
     "Coordinates flood control, congestion management and liveability works in Jakarta.",
     "Mengoordinasikan pengendalian banjir, penanganan kemacetan, dan peningkatan kelayakhunian di Jakarta."),
    (17, "prog-free-nutritious-meals", "Free Nutritious Meals Programme", "health",
     "pkpn-health", "org-badan-gizi-nasional",
     "Delivers free nutritious meals through the national nutrition programme.",
     "Menyediakan makanan bergizi gratis melalui program gizi nasional."),
    (18, "prog-peoples-schools", "People's School Programme", "education",
     "pkpn-education", "org-kementerian-sosial",
     "Runs People's Schools for students from low-income families.",
     "Menyelenggarakan Sekolah Rakyat bagi siswa dari keluarga berpenghasilan rendah."),
    (19, "prog-village-cooperatives",
     "Red and White Village and Neighbourhood Cooperative Programme", "economy",
     "pkpn-resilience", "org-kementerian-koperasi",
     "Establishes village and neighbourhood cooperatives across Indonesia.",
     "Membentuk koperasi desa dan kelurahan di seluruh Indonesia."),
    (20, "prog-education-digitalisation", "Education Digitalisation Programme",
     "education", "pkpn-education", "org-kemendikdasmen",
     "Supports digital tools and connectivity in education.",
     "Mendukung pemanfaatan perangkat digital dan konektivitas dalam pendidikan."),
    (21, "prog-poverty-reduction", "Poverty Reduction Programme", "social",
     "pkpn-resilience", "",
     "Coordinates national measures to reduce poverty.",
     "Mengoordinasikan langkah nasional untuk pengentasan kemiskinan."),
    (22, "prog-integrated-waste", "Integrated Waste Management Programme",
     "environment", "pkpn-resilience", "org-kementerian-lingkungan-hidup",
     "Builds integrated waste management infrastructure and services.",
     "Membangun infrastruktur dan layanan pengelolaan sampah terpadu."),
    (23, "prog-merauke-food-energy-water",
     "Merauke Food, Energy and Water Self-Sufficiency Programme", "food",
     "pkpn-food", "",
     "Develops food, energy and water production in Merauke, Mappi, Asmat and Boven Digoel, including rice fields, palm oil, livestock and supporting facilities.",
     "Mengembangkan produksi pangan, energi, dan air di Merauke, Mappi, Asmat, dan Boven Digoel, termasuk cetak sawah, sawit, peternakan, dan sarana pendukung."),
    (24, "prog-pantura-ponds", "Pantura Pond Revitalisation Programme", "food",
     "pkpn-food", "org-kementerian-kkp",
     "Revitalises coastal ponds in Bekasi, Karawang, Subang and Indramayu.",
     "Merevitalisasi tambak pesisir di Bekasi, Karawang, Subang, dan Indramayu."),
    (25, "prog-east-sumba-shrimp", "East Sumba Integrated Shrimp Farming Programme",
     "food", "pkpn-food", "org-kementerian-kkp",
     "Develops integrated shrimp farming in East Sumba.",
     "Mengembangkan budi daya udang terintegrasi di Sumba Timur."),
]

ORG_ROWS = [
    ("org-bnpp", "Badan Nasional Pengelola Perbatasan", "BNPP", "government", "ID",
     "https://bnpp.go.id", "National border management agency."),
    ("org-kementerian-pariwisata", "Kementerian Pariwisata", "Kemenpar",
     "government", "ID", "https://kemenpar.go.id", "Ministry of Tourism."),
    ("org-kementerian-pertanian", "Kementerian Pertanian", "Kementan",
     "government", "ID", "https://pertanian.go.id", "Ministry of Agriculture."),
    ("org-kemenko-perekonomian",
     "Kementerian Koordinator Bidang Perekonomian", "Kemenko Perekonomian",
     "government", "ID", "https://ekon.go.id",
     "Coordinating Ministry for Economic Affairs; publishes the PSN register."),
    ("org-badan-gizi-nasional", "Badan Gizi Nasional", "BGN", "government", "ID",
     "", "National Nutrition Agency."),
    ("org-kementerian-sosial", "Kementerian Sosial", "Kemensos", "government",
     "ID", "https://kemensos.go.id", "Ministry of Social Affairs."),
    ("org-kementerian-koperasi", "Kementerian Koperasi", "Kemenkop",
     "government", "ID", "", "Ministry of Cooperatives."),
    ("org-kemendikdasmen", "Kementerian Pendidikan Dasar dan Menengah",
     "Kemendikdasmen", "government", "ID", "",
     "Ministry of Primary and Secondary Education."),
    ("org-kementerian-lingkungan-hidup", "Kementerian Lingkungan Hidup", "KLH",
     "government", "ID", "https://menlhk.go.id", "Ministry of Environment."),
    ("org-kementerian-kkp", "Kementerian Kelautan dan Perikanan", "KKP",
     "government", "ID", "https://kkp.go.id",
     "Ministry of Marine Affairs and Fisheries."),
]

# programme id, project id, role, source id, note.
LINKS = [
    ("prog-electricity", "energy-plts-100gw-phase-1", "component",
     "src-setneg-plts-100gw-2026-08-25",
     "The 100 GWp solar phase is an electricity programme component; this link is structural."),
    ("prog-smelters", "factory-hilirisasi-2-07-imip-stainless-steel", "component",
     "src-setkab-hilirisasi-stage-ii-2026-04-29",
     "Hilirisasi Stage II smelter project; the annex does not name individual plants under the programme."),
    ("prog-smelters", "factory-hilirisasi-2-08-cilegon-carbon-steel", "component",
     "src-setkab-hilirisasi-stage-ii-2026-04-29",
     "Hilirisasi Stage II smelter project; the annex does not name individual plants under the programme."),
    ("prog-smelters", "factory-hilirisasi-2-10-gresik-copper-gold", "component",
     "src-setkab-hilirisasi-stage-ii-2026-04-29",
     "Hilirisasi Stage II smelter project; the annex does not name individual plants under the programme."),
    ("prog-sugar-palm-downstreaming", "factory-hilirisasi-2-11-sei-mangkei-oleofood",
     "component", "src-setkab-hilirisasi-stage-ii-2026-04-29",
     "Palm-oil downstreaming component; this link is structural."),
    ("prog-accelerated-regions", "urban-ikn-phase-2", "component",
     "src-bisnis-ikn-phase-2-2026-09-28",
     "IKN is named in the programme scope; this row covers Phase 2."),
    ("prog-jakarta-flood-control", "coastal-java-sea-wall", "related",
     "src-antara-sea-wall-2026-09-16",
     "The sea wall is a coastal-defence asset related to Jakarta flood control, not a direct programme component."),
]


def upsert(rows: list[dict[str, str]], incoming: dict[str, str], key: str = "id") -> None:
    for index, row in enumerate(rows):
        if row[key] == incoming[key]:
            rows[index] = incoming
            return
    rows.append(incoming)


def main() -> None:
    register = read_csv(CURATED / "psn_register.csv")
    official = {
        int(row["psn_no"]): row
        for row in register
        if row["kind"] == "programme" and row["status"] == "active"
    }
    if len(official) != 24:
        raise SystemExit(f"expected 24 active programmes in the register, found {len(official)}")

    numbers = {entry[0] for entry in PROGRAMMES}
    if numbers != set(official):
        raise SystemExit(
            f"programme numbers do not match the register: {sorted(numbers ^ set(official))}"
        )

    sources = {row["id"] for row in read_csv(CURATED / "sources.csv")}
    if SOURCE_ID not in sources:
        raise SystemExit(f"missing source {SOURCE_ID}")

    organizations = read_csv(CURATED / "organizations.csv")
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
    org_ids = {row["id"] for row in organizations}

    programmes_path = CURATED / "programmes.csv"
    programmes = read_csv(programmes_path) if programmes_path.exists() else []
    links_path = CURATED / "programme_projects.csv"
    links = read_csv(links_path) if links_path.exists() else []
    claims_path = CURATED / "programme_sources.csv"
    claims = read_csv(claims_path) if claims_path.exists() else []

    managed_ids = {entry[1] for entry in PROGRAMMES}

    for number, programme_id, name_en, theme, pkpn_id, lead_org_id, summary_en, summary_id in PROGRAMMES:
        row = official[number]
        if lead_org_id and lead_org_id not in org_ids:
            raise SystemExit(f"{programme_id}: unknown lead organisation {lead_org_id}")
        upsert(
            programmes,
            {
                "id": programme_id,
                "name_id": row["name_id"],
                "name_en": name_en,
                "theme": theme,
                "psn_no": str(number),
                "pkpn_id": pkpn_id,
                "lead_org_id": lead_org_id,
                "summary_id": summary_id,
                "summary_en": summary_en,
                "target_summary_id": "",
                "target_summary_en": "",
                "start_year": "",
                "target_year": "",
                "status": "active",
                "budget_idr_t": "",
                "source_id": SOURCE_ID,
                "last_verified": LAST_VERIFIED,
                "notes": NOTE,
            },
        )

    # Drop stale managed rows so reruns are idempotent.
    links[:] = [row for row in links if row["programme_id"] not in managed_ids]
    claims[:] = [row for row in claims if row["programme_id"] not in managed_ids]

    project_ids = {row["id"] for row in read_csv(CURATED / "projects.csv")}
    for programme_id, project_id, role, source_id, note in LINKS:
        if programme_id not in managed_ids:
            raise SystemExit(f"link has unknown programme {programme_id}")
        if project_id not in project_ids:
            raise SystemExit(f"link has unknown project {project_id}")
        if source_id not in sources:
            raise SystemExit(f"link has unknown source {source_id}")
        links.append(
            {
                "programme_id": programme_id,
                "project_id": project_id,
                "role": role,
                "source_id": source_id,
                "notes": note,
            }
        )

    for number, programme_id, *_ in PROGRAMMES:
        for claim, value in (("psn", f"PSN programme {number}"), ("status", "active")):
            claims.append(
                {
                    "programme_id": programme_id,
                    "source_id": SOURCE_ID,
                    "claim": claim,
                    "claim_value": value,
                    "claim_date": REGULATION_DATE,
                    "notes": "Permenko 16/2025 annex, programme section.",
                }
            )

    write_csv(CURATED / "organizations.csv", ORG_FIELDS, organizations)
    write_csv(programmes_path, PROGRAMME_FIELDS, programmes)
    write_csv(links_path, PROGRAMME_PROJECT_FIELDS, links)
    write_csv(claims_path, PROGRAMME_SOURCE_FIELDS, claims)

    print(
        f"OK: {len(PROGRAMMES)} PSN programmes, {len(ORG_ROWS)} organisations, "
        f"{len(LINKS)} project links, {len(PROGRAMMES) * 2} claims"
    )


if __name__ == "__main__":
    main()
