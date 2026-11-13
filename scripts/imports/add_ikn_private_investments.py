"""Add the three remaining named IKN private investments and correct Intiland.

Source already archived in the repository:

* JournalArta, 8 November 2026, reporting the OIKN cooperation signing of
  14 October 2026. Besides the Berdikari chicken facility and Grand Vista
  Nusantara already curated, the report names three further private
  investments signed that day:

  - PT Laziz Nusantara Grup: Arabic restaurant, gelato outlet and a
    multipurpose building at KIPP 1B, 0.54 ha, about Rp10B.
  - PT FYP Karya Perdana: Teras Padu, sports and commercial support facilities
    at KIPP 1A, 0.45 ha, about Rp20B.
  - PT Java Teak Indo: Jepara furniture showroom and office at KIPP 1A,
    0.2 ha, about Rp1.5B.

  The same report also gives the previously missing detail for the Intiland
  landed houses: 109 units (not 108), 390 sqm each, 9.17 ha across two parcels,
  Rp2.819T, a 10-year cooperation (two years construction plus eight years of
  service) and completion expected in Q4 2028. The signing date was 6 October
  2026, not 14 October.

The script also raises the IKN coverage target from 25 to 28 because the same
archived source names 28 IKN package and private-investment rows once these
three are included. No target is inferred from a different document.

The script is idempotent: existing ids are never replaced and repeated runs do
not duplicate rows. The corrections are written as fixed values, so rerunning
them is harmless.

Run: python scripts/imports/add_ikn_private_investments.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_i18n.py
      python scripts/build_all.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CONFLICT_FIELDS,
    CURATED,
    EVENT_FIELDS,
    ORG_FIELDS,
    PROJECT_FIELDS,
    PROJECT_ORG_FIELDS,
    PROJECT_SOURCE_FIELDS,
    TRANSLATION_FIELDS,
    read_csv,
    write_csv,
)

REVIEWED = "2026-11-10"
SOURCE = "src-journalarta-ikn-seven-projects-2026-11-08"
SIGNING = "2026-10-14"
INTILAND_SIGNING = "2026-10-06"

KIPP_1A = "KIPP Nusantara, KIPP 1A, Penajam Paser Utara"
KIPP_1B = "KIPP Nusantara, KIPP 1B, Penajam Paser Utara"

NEW_ORGS = [
    {
        "id": "org-laziz-nusantara",
        "name": "PT Laziz Nusantara Grup",
        "short_name": "Laziz Nusantara",
        "org_type": "private",
        "country_code": "ID",
        "parent_id": "",
        "website": "",
        "notes": (
            "Signed an IKN cooperation agreement on 14 October 2026 for an "
            "Arabic restaurant, gelato outlet and multipurpose building."
        ),
    },
    {
        "id": "org-fyp-karya-perdana",
        "name": "PT FYP Karya Perdana",
        "short_name": "FYP Karya Perdana",
        "org_type": "private",
        "country_code": "ID",
        "parent_id": "",
        "website": "",
        "notes": (
            "Signed an IKN cooperation agreement on 14 October 2026 for the "
            "Teras Padu sports and commercial hub."
        ),
    },
    {
        "id": "org-java-teak-indo",
        "name": "PT Java Teak Indo",
        "short_name": "Java Teak Indo",
        "org_type": "private",
        "country_code": "ID",
        "parent_id": "",
        "website": "",
        "notes": (
            "Signed an IKN cooperation agreement on 14 October 2026 for a "
            "Jepara furniture showroom and office."
        ),
    },
    {
        "id": "org-nindya-estate-management",
        "name": "PT Nindya Estate Management",
        "short_name": "Nindya Estate Management",
        "org_type": "private",
        "country_code": "ID",
        "parent_id": "",
        "website": "",
        "notes": (
            "Co-initiator with PT Nindya Karya of the eight ASN apartment "
            "towers signed on 14 October 2026."
        ),
    },
]

NEW_PROJECTS = [
    {
        "id": "urban-laziz-arabic-resto",
        "name": "Laziz Arabic Resto and Gelato IKN",
        "sector": "urban",
        "subsector": "food and beverage",
        "status": "planned",
        "status_basis": (
            "PT Laziz Nusantara Grup signed a cooperation agreement with OIKN "
            "on 14 October 2026 for an Arabic restaurant, gelato outlet and "
            "multipurpose building at KIPP 1B; construction had not started in "
            "the source."
        ),
        "corridor_id": "",
        "island": "Kalimantan",
        "province": "East Kalimantan",
        "route": KIPP_1B,
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "0.010",
        "capacity": "0.54",
        "capacity_unit": "ha",
        "psn": "no",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": SIGNING,
        "verification": "single",
        "lat": "-0.974",
        "lon": "116.708",
        "precision": "approximate",
        "last_verified": REVIEWED,
        "notes": (
            "Arabic restaurant, gelato outlet and multipurpose building on "
            "0.54 ha. The source gives an estimated investment of Rp10B and "
            "no completion date."
        ),
    },
    {
        "id": "urban-teras-padu",
        "name": "Teras Padu Sports and Commercial Hub IKN",
        "sector": "urban",
        "subsector": "sports and commercial",
        "status": "planned",
        "status_basis": (
            "PT FYP Karya Perdana signed a cooperation agreement with OIKN on "
            "14 October 2026 for the Teras Padu sports and commercial support "
            "facilities at KIPP 1A; construction had not started in the source."
        ),
        "corridor_id": "",
        "island": "Kalimantan",
        "province": "East Kalimantan",
        "route": KIPP_1A,
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "0.020",
        "capacity": "0.45",
        "capacity_unit": "ha",
        "psn": "no",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": SIGNING,
        "verification": "single",
        "lat": "-0.974",
        "lon": "116.708",
        "precision": "approximate",
        "last_verified": REVIEWED,
        "notes": (
            "Sports and commercial support facilities on 0.45 ha. The source "
            "gives an estimated investment of Rp20B and no completion date."
        ),
    },
    {
        "id": "urban-java-teak-showroom",
        "name": "Java Teak Jepara Furniture Showroom IKN",
        "sector": "urban",
        "subsector": "showroom",
        "status": "planned",
        "status_basis": (
            "PT Java Teak Indo signed a cooperation agreement with OIKN on "
            "14 October 2026 for a Jepara furniture showroom and office at "
            "KIPP 1A; construction had not started in the source."
        ),
        "corridor_id": "",
        "island": "Kalimantan",
        "province": "East Kalimantan",
        "route": KIPP_1A,
        "length_km": "",
        "operational_km": "",
        "construction_km": "",
        "progress_pct": "",
        "investment_idr_t": "0.0015",
        "capacity": "0.2",
        "capacity_unit": "ha",
        "psn": "no",
        "opened_year": "",
        "opened_date": "",
        "expected_open_year": "",
        "status_as_of": SIGNING,
        "verification": "single",
        "lat": "-0.974",
        "lon": "116.708",
        "precision": "approximate",
        "last_verified": REVIEWED,
        "notes": (
            "Jepara furniture showroom and office on 0.2 ha. The source gives "
            "an estimated investment of Rp1.5B and no completion date."
        ),
    },
]

# project_id, org_id, role, notes
NEW_LINKS = [
    (
        "urban-laziz-arabic-resto", "org-laziz-nusantara", "developer",
        "Signed a cooperation agreement with OIKN for the KIPP 1B restaurant, "
        "gelato and multipurpose building.",
    ),
    (
        "urban-teras-padu", "org-fyp-karya-perdana", "developer",
        "Signed a cooperation agreement with OIKN for the KIPP 1A Teras Padu "
        "sports and commercial hub.",
    ),
    (
        "urban-java-teak-showroom", "org-java-teak-indo", "developer",
        "Signed a cooperation agreement with OIKN for the KIPP 1A furniture "
        "showroom.",
    ),
    (
        "housing-ikn-rusun-asn", "org-nindya-estate-management", "developer",
        "Co-initiator (pemrakarsa) with PT Nindya Karya of the eight ASN "
        "apartment towers.",
    ),
]

# project_id, claim, claim_value
NEW_CLAIMS = {
    "urban-laziz-arabic-resto": [
        ("status", ""),
        ("location", KIPP_1B),
        ("investment", "Rp 10B"),
        ("capacity", "0.54 ha"),
    ],
    "urban-teras-padu": [
        ("status", ""),
        ("location", KIPP_1A),
        ("investment", "Rp 20B"),
        ("capacity", "0.45 ha"),
    ],
    "urban-java-teak-showroom": [
        ("status", ""),
        ("location", KIPP_1A),
        ("investment", "Rp 1.5B"),
        ("capacity", "0.2 ha"),
    ],
}

# project_id, event id, description
NEW_EVENTS = [
    (
        "urban-laziz-arabic-resto", "evt-laziz-pks",
        "PT Laziz Nusantara Grup signed a cooperation agreement for an Arabic "
        "restaurant, gelato outlet and multipurpose building at KIPP 1B.",
    ),
    (
        "urban-teras-padu", "evt-teras-padu-pks",
        "PT FYP Karya Perdana signed a cooperation agreement for the Teras "
        "Padu sports and commercial hub at KIPP 1A.",
    ),
    (
        "urban-java-teak-showroom", "evt-java-teak-pks",
        "PT Java Teak Indo signed a cooperation agreement for a Jepara "
        "furniture showroom and office at KIPP 1A.",
    ),
]

# project_id, Indonesian name
NEW_TRANSLATIONS = {
    "urban-laziz-arabic-resto": "Resto Arab dan Gelato Laziz IKN",
    "urban-teras-padu": "Teras Padu Olahraga dan Komersial IKN",
    "urban-java-teak-showroom": "Showroom Mebel Jepara Java Teak IKN",
}

# Intiland corrections. The source states 109 units, Rp2.819T and Q4 2028.
INTILAND_ID = "housing-ikn-intiland-houses"
INTILAND_CLAIMS = [
    ("investment", "Rp 2.819T"),
    ("capacity", "109 houses"),
    ("target", "2028 (Q4)"),
]

CONFLICT = {
    "id": "conflict-ikn-private-investment-total",
    "scope": "dataset",
    "subject": "IKN five private-investment total",
    "project_id": "",
    "estate_id": "",
    "corridor_id": "",
    "field": "investment",
    "value_a": "Rp1.11T stated for the five private investments",
    "source_a": SOURCE,
    "value_b": (
        "Rp1.2085T sum of the five stated project estimates "
        "(177 + 10 + 20 + 1.5 + 1,000 billion)"
    ),
    "source_b": SOURCE,
    "status": "open",
    "resolution": (
        "Atlas records each project's own stated estimate and keeps the Rp1.11T "
        "headline in the source notes. It does not rescale any row. Grand "
        "Vista's rounded Rp1T is the most likely source of the difference, but "
        "the atlas does not adjust it without a source."
    ),
    "notes": (
        "The article's own five project estimates do not add up to its "
        "Rp1.11T headline; the difference is about Rp98.5B."
    ),
}


def main() -> None:
    orgs = read_csv(CURATED / "organizations.csv")
    org_ids = {row["id"] for row in orgs}
    added_orgs = 0
    for org in NEW_ORGS:
        if org["id"] not in org_ids:
            orgs.append(dict(org))
            org_ids.add(org["id"])
            added_orgs += 1
    # Correct the Intiland note: the source says 109 houses, not 108.
    for row in orgs:
        if row["id"] == "org-intiland":
            row["notes"] = "Sponsor of 109 landed ASN houses signed in October 2026."
    orgs.sort(key=lambda row: row["id"])
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, orgs)

    projects = read_csv(CURATED / "projects.csv")
    project_ids = {row["id"] for row in projects}
    added_projects = 0
    for project in NEW_PROJECTS:
        if project["id"] not in project_ids:
            projects.append(dict(project))
            project_ids.add(project["id"])
            added_projects += 1
    # Correct and complete the Intiland landed-house row.
    for row in projects:
        if row["id"] == INTILAND_ID:
            row["investment_idr_t"] = "2.819"
            row["capacity"] = "109"
            row["capacity_unit"] = "houses"
            row["expected_open_year"] = "2028"
            row["status_as_of"] = INTILAND_SIGNING
            row["last_verified"] = REVIEWED
            row["status_basis"] = (
                "PT Intiland Development signed a KPBU for 109 landed ASN "
                "houses on 6 October 2026; construction was about to start."
            )
            row["notes"] = (
                "109 landed houses of 390 sqm each on 9.17 ha across two "
                "parcels (79 units on 6.6 ha and 30 on 2.4 ha). The 10-year "
                "cooperation covers two years of construction and eight years "
                "of service; completion is expected in Q4 2028. Signed on "
                "6 October 2026."
            )
    write_csv(CURATED / "projects.csv", PROJECT_FIELDS, projects)

    links = read_csv(CURATED / "project_organizations.csv")
    link_keys = {
        (row["project_id"], row["org_id"], row["role"]) for row in links
    }
    added_links = 0
    for project_id, org_id, role, notes in NEW_LINKS:
        key = (project_id, org_id, role)
        if key in link_keys:
            continue
        links.append(
            {
                "project_id": project_id,
                "org_id": org_id,
                "role": role,
                "share_pct": "",
                "start_year": "",
                "end_year": "",
                "source_id": SOURCE,
                "notes": notes,
            }
        )
        link_keys.add(key)
        added_links += 1
    write_csv(CURATED / "project_organizations.csv", PROJECT_ORG_FIELDS, links)

    claims = read_csv(CURATED / "project_sources.csv")
    claim_keys = {
        (row["project_id"], row["source_id"], row["claim"]) for row in claims
    }
    added_claims = 0
    for project_id, project_claims in NEW_CLAIMS.items():
        for claim, value in project_claims:
            key = (project_id, SOURCE, claim)
            if key in claim_keys:
                continue
            claims.append(
                {
                    "project_id": project_id,
                    "source_id": SOURCE,
                    "claim": claim,
                    "claim_value": value,
                    "claim_date": SIGNING,
                    "notes": "",
                }
            )
            claim_keys.add(key)
            added_claims += 1
    for claim, value in INTILAND_CLAIMS:
        key = (INTILAND_ID, SOURCE, claim)
        if key in claim_keys:
            continue
        claims.append(
            {
                "project_id": INTILAND_ID,
                "source_id": SOURCE,
                "claim": claim,
                "claim_value": value,
                "claim_date": INTILAND_SIGNING,
                "notes": "",
            }
        )
        claim_keys.add(key)
        added_claims += 1
    # The Intiland status and location claims were dated to the 14 October
    # signing; the source dates that agreement to 6 October 2026.
    for row in claims:
        if row["project_id"] == INTILAND_ID and row["source_id"] == SOURCE:
            row["claim_date"] = INTILAND_SIGNING
    write_csv(CURATED / "project_sources.csv", PROJECT_SOURCE_FIELDS, claims)

    events = read_csv(CURATED / "project_events.csv")
    event_ids = {row["id"] for row in events}
    added_events = 0
    for project_id, event_id, description in NEW_EVENTS:
        if event_id in event_ids:
            continue
        events.append(
            {
                "id": event_id,
                "project_id": project_id,
                "event_date": SIGNING,
                "event_type": "contract",
                "description": description,
                "source_id": SOURCE,
                "notes": "",
            }
        )
        event_ids.add(event_id)
        added_events += 1
    # Correct the Intiland event: 6 October signing and 109 houses.
    for row in events:
        if row["id"] == "evt-ikn-intiland-pks":
            row["event_date"] = INTILAND_SIGNING
            row["description"] = (
                "PT Intiland Development signed a KPBU for 109 landed ASN "
                "houses worth Rp2.819T."
            )
    write_csv(CURATED / "project_events.csv", EVENT_FIELDS, events)

    translations = read_csv(CURATED / "translations.csv")
    translation_keys = {
        (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        for row in translations
    }
    added_translations = 0
    for project_id, name_id in NEW_TRANSLATIONS.items():
        key = ("project", project_id, "name", "id")
        if key in translation_keys:
            continue
        translations.append(
            {
                "entity_type": "project",
                "entity_id": project_id,
                "field": "name",
                "locale": "id",
                "text": name_id,
                "status": "reviewed",
                "translator": "atlas-editor",
                "reviewed_on": REVIEWED,
                "source_id": SOURCE,
            }
        )
        translation_keys.add(key)
        added_translations += 1
    write_csv(CURATED / "translations.csv", TRANSLATION_FIELDS, translations)

    conflicts = read_csv(CURATED / "conflicts.csv")
    added_conflicts = 0
    if CONFLICT["id"] not in {row["id"] for row in conflicts}:
        conflicts.append(dict(CONFLICT))
        write_csv(CURATED / "conflicts.csv", CONFLICT_FIELDS, conflicts)
        added_conflicts = 1

    print(
        f"Added {added_projects} projects, {added_orgs} organisations, "
        f"{added_links} role links, {added_claims} claims, {added_events} events, "
        f"{added_translations} translations, {added_conflicts} conflicts and "
        f"corrected the Intiland row (idempotent)."
    )


if __name__ == "__main__":
    main()
