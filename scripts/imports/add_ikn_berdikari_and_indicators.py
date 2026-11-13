"""Add the 25th IKN package and ten delivery indicators.

Sources already archived in the repository:

* JournalArta, 8 November 2026, reporting the OIKN cooperation signing of
  14 October 2026. Names the five private investments alongside the ASN
  housing packages. PT Berdikari (Persero) plans an integrated chicken
  downstreaming facility in Wilayah Perencanaan 3: 17.27 ha, about Rp177B and
  a capacity of about 140,000 chickens. This is the named 25th IKN package.
* Sekretariat Kabinet, 20 October 2026, two-year delivery report. Food
  reserve, food self-sufficiency, free health checks and street children
  returning to school.
* Kementerian Pendidikan Dasar dan Menengah, 27 October 2026, two-year
  education release. Schools reached in 2025 and 2026, the 2025-2026 total,
  interactive digital panels, disaster-affected schools and new SNT pupils.

No source is invented and no target is inferred. Where the release gives only
a year, the value date uses the year-end convention already used by the
existing indicator layer. The 2026 education figures are observed on
20 October 2026, the cut-off stated in the release.

The script is idempotent: existing ids are never replaced and existing values
are never duplicated.

Run: python scripts/imports/add_ikn_berdikari_and_indicators.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_i18n.py
      python scripts/build_all.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CURATED,
    EVENT_FIELDS,
    INDICATOR_FIELDS,
    INDICATOR_VALUE_FIELDS,
    ORG_FIELDS,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    TRANSLATION_FIELDS,
    read_csv,
    write_csv,
)

REVIEWED = "2026-11-10"

SOURCE_IKN = "src-journalarta-ikn-seven-projects-2026-11-08"
SOURCE_SETKAB = "src-setkab-two-year-report-2026-10-20"
SOURCE_KEMDIKDASMEN = "src-kemendikdasmen-two-year-2026-10-27"

PROJECT_ID = "agri-ikn-berdikari-chicken"
ORG_ID = "org-berdikari"
ROUTE = "KIPP Nusantara, Wilayah Perencanaan 3, Penajam Paser Utara"
STATUS_AS_OF = "2026-10-14"

NEW_ORG = {
    "id": ORG_ID,
    "name": "PT Berdikari (Persero)",
    "short_name": "Berdikari",
    "org_type": "soe",
    "country_code": "ID",
    "parent_id": "",
    "website": "",
    "notes": (
        "State-owned food company. Signed the IKN integrated chicken "
        "downstreaming agreement on 14 October 2026."
    ),
}

NEW_PROJECT = {
    "id": PROJECT_ID,
    "name": "Berdikari Integrated Chicken Downstreaming (IKN)",
    "sector": "agriculture",
    "subsector": "downstreaming",
    "status": "planned",
    "status_basis": (
        "PT Berdikari (Persero) signed a cooperation agreement on 14 October "
        "2026 for an integrated chicken downstreaming facility in Wilayah "
        "Perencanaan 3; construction had not started in the source."
    ),
    "corridor_id": "",
    "island": "Kalimantan",
    "province": "East Kalimantan",
    "route": ROUTE,
    "length_km": "",
    "operational_km": "",
    "construction_km": "",
    "progress_pct": "",
    "investment_idr_t": "0.177",
    "capacity": "140000",
    "capacity_unit": "chickens",
    "psn": "no",
    "opened_year": "",
    "opened_date": "",
    "expected_open_year": "",
    "status_as_of": STATUS_AS_OF,
    "verification": "single",
    "lat": "-0.974",
    "lon": "116.708",
    "precision": "approximate",
    "last_verified": REVIEWED,
    "notes": (
        "Named among the five private investments signed on 14 October 2026. "
        "The source describes a parent-stock layer farm and hatchery on "
        "17.27 ha with an estimated Rp177B investment and a capacity of about "
        "140,000 chickens. No completion date is stated."
    ),
}

NEW_CLAIMS = [
    ("status", "", STATUS_AS_OF, ""),
    ("location", ROUTE, STATUS_AS_OF, ""),
    ("investment", "Rp 177B", STATUS_AS_OF, ""),
    ("capacity", "140,000 chickens", STATUS_AS_OF, ""),
]

NEW_EVENT = {
    "id": "evt-berdikari-pks",
    "project_id": PROJECT_ID,
    "event_date": STATUS_AS_OF,
    "event_type": "contract",
    "description": (
        "PT Berdikari signed a cooperation agreement for an integrated "
        "chicken downstreaming facility in IKN Wilayah Perencanaan 3."
    ),
    "source_id": SOURCE_IKN,
    "notes": "",
}

NEW_TRANSLATION = {
    "entity_type": "project",
    "entity_id": PROJECT_ID,
    "field": "name",
    "locale": "id",
    "text": "Hilirisasi Ayam Terintegrasi Berdikari (IKN)",
    "status": "reviewed",
    "translator": "atlas-editor",
    "reviewed_on": REVIEWED,
    "source_id": SOURCE_IKN,
}

# id, programme, name_en, name_id, unit, direction, target, target_date,
# source, notes
NEW_INDICATORS = [
    (
        "ind-pkpn-food-reserve", "pkpn-food",
        "National food reserve", "Cadangan pangan nasional",
        "tonnes", "increase", "", "", SOURCE_SETKAB,
        "5.2 million tonnes, described as the highest in history. The release "
        "states no target or baseline.",
    ),
    (
        "ind-pkpn-food-self-sufficiency", "pkpn-food",
        "Food commodities self-sufficient", "Komoditas pangan swasembada",
        "commodities", "increase", "", "", SOURCE_SETKAB,
        "Eight commodities reported as self-sufficient. The release does not "
        "name them or state a target.",
    ),
    (
        "ind-pkpn-health-free-checks", "pkpn-health",
        "Free health check services", "Layanan cek kesehatan gratis",
        "services", "increase", "", "", SOURCE_SETKAB,
        "108 million services under the Cek Kesehatan Gratis programme. No "
        "target is stated.",
    ),
    (
        "ind-pkpn-education-street-children", "pkpn-education",
        "Street children returned to school",
        "Anak jalanan kembali bersekolah",
        "children", "increase", "", "", SOURCE_SETKAB,
        "43,000 street children returned to school in the first two years. No "
        "target is stated.",
    ),
    (
        "ind-pkpn-education-schools-reached", "pkpn-education",
        "Schools reached by revitalisation and construction",
        "Sekolah terjangkau revitalisasi dan pembangunan",
        "schools", "increase", "", "", SOURCE_KEMDIKDASMEN,
        "55,451 schools reached in 2025-2026. This is a broader definition "
        "than the 30,000 renovated schools in the two-year report.",
    ),
    (
        "ind-pkpn-education-schools-2025", "pkpn-education",
        "Schools reached in 2025", "Sekolah terjangkau pada 2025",
        "schools", "increase", "10440", "2025-12-31", SOURCE_KEMDIKDASMEN,
        "16,167 schools reached against a 10,440 target; 99.96% of "
        "construction was complete. The release gives only the year.",
    ),
    (
        "ind-pkpn-education-schools-2026", "pkpn-education",
        "Schools reached in 2026", "Sekolah terjangkau pada 2026",
        "schools", "increase", "31744", "2026-12-31", SOURCE_KEMDIKDASMEN,
        "39,284 schools reached by 20 October 2026 against a 31,744 target "
        "(123.75%).",
    ),
    (
        "ind-pkpn-education-pid-2026", "pkpn-education",
        "Interactive digital panels installed in 2026",
        "Panel interaktif digital terpasang pada 2026",
        "units", "increase", "742536", "2026-12-31", SOURCE_KEMDIKDASMEN,
        "72,258 units installed against a 742,536 target by 20 October 2026. "
        "In 2025, 288,865 schools received panels and supporting devices; the "
        "units differ.",
    ),
    (
        "ind-pkpn-education-disaster-schools", "pkpn-education",
        "Disaster-affected schools revitalised",
        "Sekolah terdampak bencana direvitalisasi",
        "schools", "increase", "3178", "", SOURCE_KEMDIKDASMEN,
        "3,134 of 3,178 target schools in Aceh, North Sumatra and West "
        "Sumatra (98.62%) by 20 October 2026. A separate 747 of 749 schools "
        "were reached for other disasters.",
    ),
    (
        "ind-pkpn-education-snt-pupils", "pkpn-education",
        "New SNT pupils", "Murid baru SNT",
        "pupils", "increase", "", "", SOURCE_KEMDIKDASMEN,
        "1,360 new pupils across 17 operating SNT in 13 provinces in the "
        "2026/2027 school year. No target is stated.",
    ),
]

# id, value, as_of, source, notes
NEW_VALUES = [
    ("ind-pkpn-food-reserve", "5200000", "2026-10-20", SOURCE_SETKAB, ""),
    ("ind-pkpn-food-self-sufficiency", "8", "2026-10-20", SOURCE_SETKAB, ""),
    ("ind-pkpn-health-free-checks", "108000000", "2026-10-20", SOURCE_SETKAB, ""),
    ("ind-pkpn-education-street-children", "43000", "2026-10-20", SOURCE_SETKAB, "The release says 43 thousand."),
    ("ind-pkpn-education-schools-reached", "55451", "2026-10-20", SOURCE_KEMDIKDASMEN, ""),
    ("ind-pkpn-education-schools-2025", "16167", "2025-12-31", SOURCE_KEMDIKDASMEN, ""),
    ("ind-pkpn-education-schools-2026", "39284", "2026-10-20", SOURCE_KEMDIKDASMEN, ""),
    ("ind-pkpn-education-pid-2026", "72258", "2026-10-20", SOURCE_KEMDIKDASMEN, ""),
    ("ind-pkpn-education-disaster-schools", "3134", "2026-10-20", SOURCE_KEMDIKDASMEN, ""),
    ("ind-pkpn-education-snt-pupils", "1360", "2026-10-20", SOURCE_KEMDIKDASMEN, ""),
]


def main() -> None:
    orgs = read_csv(CURATED / "organizations.csv")
    if ORG_ID not in {row["id"] for row in orgs}:
        orgs.append(dict(NEW_ORG))
        orgs.sort(key=lambda row: row["id"])
        write_csv(CURATED / "organizations.csv", ORG_FIELDS, orgs)

    projects = read_csv(CURATED / "projects.csv")
    if PROJECT_ID not in {row["id"] for row in projects}:
        projects.append(dict(NEW_PROJECT))
        write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)

    links = read_csv(CURATED / "project_organizations.csv")
    link_key = (PROJECT_ID, ORG_ID, "developer")
    if not any(
        (row["project_id"], row["org_id"], row["role"]) == link_key
        for row in links
    ):
        links.append(
            {
                "project_id": PROJECT_ID,
                "org_id": ORG_ID,
                "role": "developer",
                "share_pct": "",
                "start_year": "",
                "end_year": "",
                "source_id": SOURCE_IKN,
                "notes": (
                    "Signed a cooperation agreement with OIKN for the WP3 "
                    "integrated chicken facility."
                ),
            }
        )
        write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, links)

    claims = read_csv(CURATED / "project_sources.csv")
    claim_keys = {
        (row["project_id"], row["source_id"], row["claim"]) for row in claims
    }
    for claim, value, date, notes in NEW_CLAIMS:
        key = (PROJECT_ID, SOURCE_IKN, claim)
        if key in claim_keys:
            continue
        claims.append(
            {
                "project_id": PROJECT_ID,
                "source_id": SOURCE_IKN,
                "claim": claim,
                "claim_value": value,
                "claim_date": date,
                "notes": notes,
            }
        )
        claim_keys.add(key)
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)

    events = read_csv(CURATED / "project_events.csv")
    if NEW_EVENT["id"] not in {row["id"] for row in events}:
        events.append(dict(NEW_EVENT))
        write_csv(CURATED / "project_events.csv", EVENT_FIELDS, events)

    translations = read_csv(CURATED / "translations.csv")
    translation_key = (
        NEW_TRANSLATION["entity_type"],
        NEW_TRANSLATION["entity_id"],
        NEW_TRANSLATION["field"],
        NEW_TRANSLATION["locale"],
    )
    if not any(
        (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        == translation_key
        for row in translations
    ):
        translations.append(dict(NEW_TRANSLATION))
        write_csv(CURATED / "translations.csv", TRANSLATION_FIELDS, translations)

    indicators = read_csv(CURATED / "indicators.csv")
    existing_indicators = {row["id"] for row in indicators}
    for (
        indicator_id, programme_id, name_en, name_id, unit, direction,
        target, target_date, source_id, notes,
    ) in NEW_INDICATORS:
        if indicator_id in existing_indicators:
            continue
        indicators.append(
            {
                "id": indicator_id,
                "programme_id": programme_id,
                "project_id": "",
                "name_en": name_en,
                "name_id": name_id,
                "unit": unit,
                "direction": direction,
                "baseline_value": "",
                "baseline_date": "",
                "target_value": target,
                "target_date": target_date,
                "source_id": source_id,
                "notes": notes,
            }
        )
        existing_indicators.add(indicator_id)
    write_csv(CURATED / "indicators.csv", INDICATOR_FIELDS, indicators)

    values = read_csv(CURATED / "indicator_values.csv")
    value_keys = {
        (row["indicator_id"], row["as_of"], row["source_id"]) for row in values
    }
    for indicator_id, value, as_of, source_id, notes in NEW_VALUES:
        key = (indicator_id, as_of, source_id)
        if key in value_keys:
            continue
        values.append(
            {
                "indicator_id": indicator_id,
                "value": value,
                "as_of": as_of,
                "source_id": source_id,
                "notes": notes,
            }
        )
        value_keys.add(key)
    write_csv(CURATED / "indicator_values.csv", INDICATOR_VALUE_FIELDS, values)

    print(
        f"Added {PROJECT_ID}, {ORG_ID}, {len(NEW_CLAIMS)} claims, "
        f"1 event, 1 translation, {len(NEW_INDICATORS)} indicators and "
        f"{len(NEW_VALUES)} values (idempotent)."
    )


if __name__ == "__main__":
    main()
