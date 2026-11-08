"""Build the field-level data dictionary.

The dictionary is generated from the schema in ``data_model.py`` plus the
descriptions below, so it cannot drift from the CSV headers. It is written to
``data/derived/data_dictionary.csv`` and copied to ``site/data/dictionary.csv``
for download.

Run: python scripts/build_dictionary.py
"""

from __future__ import annotations

from data_model import CURATED, DERIVED, SITE_DATA, TABLES, read_csv, write_csv

TABLE_META = {
    "projects.csv": ("Projects", "One row per curated infrastructure project, with status, location and key figures."),
    "organizations.csv": ("Organisations", "Companies and agencies that sponsor, own or operate projects."),
    "project_organizations.csv": ("Project organisations", "Role links between projects and organisations."),
    "sources.csv": ("Sources", "Documents used as evidence, with retrieval dates and local snapshots."),
    "project_sources.csv": ("Project claims", "One atomic fact per project-source link."),
    "project_external_ids.csv": ("External IDs", "Project keys in BPJT and other external systems."),
    "project_aliases.csv": ("Project aliases", "Alternative names used by search."),
    "investments.csv": ("Investments", "Commitment or tranche figures with their own source."),
    "laws.csv": ("Laws", "Legal instruments used as a basis for a project or zone."),
    "project_laws.csv": ("Project laws", "Links between projects and legal instruments."),
    "project_events.csv": ("Project events", "Exact-dated events used by timelines."),
    "project_geometry.csv": ("Project geometry", "Line, point or polygon geometry; currently empty."),
    "corridors.csv": ("Corridors", "Trans corridor definitions and published kilometre totals."),
    "corridor_segments.csv": ("Corridor segments", "Section, phase or package rows behind a corridor table."),
    "estates.csv": ("Estates and SEZs", "Industrial estates and special economic zones."),
    "estate_sources.csv": ("Estate claims", "One atomic fact per estate-source link."),
    "coverage_targets.csv": ("Coverage targets", "The universe and target count for every data layer."),
    "conflicts.csv": ("Conflict register", "Known disagreements between sources, with both values and resolutions."),
}

FIELD = {
    "id": ("id", "yes", "Stable lowercase-hyphenated identifier used in deep links and joins."),
    "name": ("text", "yes", "Display name in English with Indonesian proper names."),
    "short_name": ("text", "no", "Short display name or acronym."),
    "subject": ("text", "yes", "Short human-readable label for the conflicted subject."),
    "sector": ("enum", "yes", "Project sector."),
    "subsector": ("text", "no", "Sector-specific type, such as toll, urban_rail, smelter or alumina."),
    "status": ("enum", "yes", "Current atlas status."),
    "status_basis": ("text", "yes", "The evidence behind the status, with figures and dates where possible."),
    "status_as_of": ("date", "yes", "Date of the evidence behind the current status."),
    "verification": ("enum", "yes", "Official, dual-source or single-source verification level."),
    "corridor_id": ("id", "conditional", "Foreign key to corridors.csv."),
    "island": ("enum", "yes", "Island group."),
    "province": ("text", "yes", "Province or provinces, semicolon-separated."),
    "regency": ("text", "conditional", "Regency or city for an estate."),
    "route": ("text", "yes", "Route, corridor or location description."),
    "lat": ("decimal", "yes", "Latitude in decimal degrees."),
    "lon": ("decimal", "yes", "Longitude in decimal degrees."),
    "precision": ("enum", "yes", "Coordinate precision: exact, approximate, regency or province."),
    "length_km": ("decimal", "conditional", "Total route or corridor length in kilometres."),
    "operational_km": ("decimal", "no", "Length in service in kilometres."),
    "construction_km": ("decimal", "no", "Length under construction in kilometres."),
    "planned_km": ("decimal", "no", "Length planned but not started in kilometres."),
    "progress_pct": ("decimal", "no", "Reported construction or completion progress, 0-100."),
    "investment_idr_t": ("decimal", "no", "Investment in trillion rupiah."),
    "capacity": ("decimal", "no", "Nameplate capacity or design output."),
    "capacity_unit": ("text", "conditional", "Unit for capacity, such as ktpa, Mtpa or mppa."),
    "psn": ("enum", "yes", "Whether the asset is a National Strategic Project."),
    "opened_year": ("year", "conditional", "Year the asset opened to service."),
    "opened_date": ("date", "no", "Exact opening date when the source states one."),
    "expected_open_year": ("year", "no", "Target opening year for planned or under-construction rows."),
    "last_verified": ("date", "yes", "Date the row was last checked against a source."),
    "notes": ("text", "yes", "Conflicts, caveats, section openings and coordinate overrides."),
    "org_type": ("enum", "yes", "Government, state-owned, private, consortium, multilateral or other."),
    "country_code": ("text", "yes", "ISO alpha-2 country code."),
    "parent_id": ("id", "no", "Foreign key to a parent organisation."),
    "website": ("url", "no", "Official website."),
    "project_id": ("id", "yes", "Foreign key to projects.csv."),
    "org_id": ("id", "yes", "Foreign key to organizations.csv."),
    "estate_id": ("id", "yes", "Foreign key to estates.csv."),
    "role": ("enum", "yes", "Organisation role on the project."),
    "share_pct": ("decimal", "no", "Ownership or participation share, 0-100."),
    "start_year": ("year", "no", "First year of the role or investment."),
    "end_year": ("year", "no", "Last year of the role or investment."),
    "source_id": ("id", "yes", "Foreign key to sources.csv."),
    "source_a": ("id", "yes", "Foreign key to the first source in a conflict."),
    "source_b": ("id", "yes", "Foreign key to the second source in a conflict."),
    "publisher": ("text", "yes", "Publisher or institution."),
    "title": ("text", "yes", "Document title."),
    "url": ("url", "yes", "Public URL for the document."),
    "published_on": ("date", "no", "Publication date when known."),
    "retrieved_on": ("date", "yes", "Date the snapshot was retrieved."),
    "source_type": ("enum", "yes", "Official, secondary, company or multilateral."),
    "language": ("enum", "yes", "Document language: en, id or other."),
    "snapshot_hash": ("text", "no", "Hash of the saved snapshot when available."),
    "accessed_via": ("text", "no", "API, page fetch, PDF download or manual transcription."),
    "archive_path": ("text", "no", "Repository-relative path to the raw snapshot."),
    "licence": ("text", "no", "Licence or reuse terms stated by the source."),
    "claim": ("enum", "yes", "One atomic fact type supported by the source."),
    "claim_value": ("text", "no", "The value stated by the source, when transcribed."),
    "claim_date": ("date", "no", "Date the source states the fact."),
    "system": ("text", "yes", "External system name, such as bpjt-ruas."),
    "external_id": ("text", "yes", "Identifier in the external system."),
    "alias": ("text", "yes", "Alternative project name."),
    "investor_org_id": ("id", "yes", "Foreign key to the investing organisation."),
    "amount": ("decimal", "yes", "Amount in the stated currency."),
    "currency": ("text", "yes", "ISO alpha-3 currency code."),
    "amount_idr_t": ("decimal", "no", "Rupiah trillion equivalent used for ranking."),
    "fx_date": ("date", "no", "Date of the exchange rate used for conversion."),
    "year": ("year", "no", "Year of the commitment or law."),
    "stage": ("enum", "yes", "Announced, committed, financial close or disbursed."),
    "instrument": ("enum", "yes", "Equity, debt, grant, guarantee, mixed or other."),
    "number": ("text", "yes", "Law or regulation number."),
    "level": ("enum", "yes", "Law, presidential regulation, ministerial regulation or other."),
    "law_id": ("id", "yes", "Foreign key to laws.csv."),
    "relation": ("text", "yes", "How the law relates to the project."),
    "event_date": ("date", "yes", "Exact date of the event."),
    "event_type": ("enum", "yes", "Announced, groundbreaking, contract, financial close, section opened, opened, stalled, resumed, target changed or other."),
    "description": ("text", "yes", "What happened."),
    "kind": ("enum", "yes", "Geometry kind: line, point or polygon."),
    "geometry": ("json", "yes", "GeoJSON geometry object."),
    "geometry_id": ("id", "no", "Foreign key to project_geometry.csv."),
    "segment_type": ("enum", "yes", "Section, phase, package or other."),
    "coordinate_source": ("enum", "yes", "Official, OSM, regency, manual or unknown."),
    "area_ha": ("decimal", "yes", "Zone area in hectares."),
    "developer": ("text", "yes", "Developer display name from the source."),
    "developer_org_id": ("id", "no", "Foreign key to organizations.csv."),
    "sector_focus": ("text", "no", "Estate or SEZ sector focus."),
    "legal_basis": ("text", "no", "Legal instrument establishing the zone."),
    "established_year": ("year", "no", "Year the zone was established."),
    "occupancy_pct": ("decimal", "no", "Reported occupancy, 0-100."),
    "kemenperin_id": ("text", "no", "Kemenperin estate identifier when known."),
    "sez_id": ("text", "no", "KEK National Council identifier when known."),
    "layer": ("text", "yes", "Coverage layer key used by the build."),
    "label": ("text", "yes", "Human-readable layer label."),
    "unit": ("text", "yes", "Unit counted by the coverage target."),
    "target_count": ("integer", "yes", "Target number of rows for the layer."),
    "universe": ("text", "yes", "Definition of the target universe."),
    "definition": ("text", "yes", "What the corridor includes and excludes."),
    "metric": ("text", "yes", "Metric used for the corridor figure."),
    "total_km": ("decimal", "yes", "Published corridor total in kilometres."),
    "as_of": ("date", "yes", "Date of the corridor figures."),
    "scope": ("enum", "yes", "Conflict scope: project, corridor, estate, dataset or method."),
    "field": ("text", "yes", "Field or fact in dispute."),
    "value_a": ("text", "yes", "First value, with its date or scope when needed."),
    "value_b": ("text", "yes", "Second value, with its date or scope when needed."),
    "resolution": ("text", "yes", "What the atlas does with the conflict."),
}

# Context-specific overrides: status and type mean different things by table.
OVERRIDES = {
    ("projects.csv", "status"): ("enum", "yes", "planned, under_construction, operating, recently_completed or stalled.", "planned; under_construction; operating; recently_completed; stalled"),
    ("estates.csv", "status"): ("enum", "yes", "Designation-level operating, under_construction or planned; not independently verified for most estates.", "operating; under_construction; planned"),
    ("corridor_segments.csv", "status"): ("enum", "yes", "Segment status using the project status vocabulary.", "planned; under_construction; operating; recently_completed; stalled"),
    ("conflicts.csv", "status"): ("enum", "yes", "Whether the conflict remains open or has a recorded resolution.", "open; resolved"),
    ("estates.csv", "type"): ("enum", "yes", "industrial_estate, sez or both.", "industrial_estate; sez; both"),
    ("projects.csv", "sector"): ("enum", "yes", "road, railway, airport, seaport or factory.", "road; railway; airport; seaport; factory"),
    ("projects.csv", "island"): ("enum", "yes", "Sumatra, Java, Kalimantan, Sulawesi, Papua, Bali-Nusa Tenggara or Maluku.", "Sumatra; Java; Kalimantan; Sulawesi; Papua; Bali-Nusa Tenggara; Maluku"),
    ("projects.csv", "psn"): ("enum", "yes", "yes, no or unknown.", "yes; no; unknown"),
    ("projects.csv", "precision"): ("enum", "yes", "exact, approximate, regency or province.", "exact; approximate; regency; province"),
    ("projects.csv", "verification"): ("enum", "yes", "official, dual, single or unverified.", "official; dual; single; unverified"),
    ("sources.csv", "source_type"): ("enum", "yes", "official, secondary, company or multilateral.", "official; secondary; company; multilateral"),
    ("sources.csv", "language"): ("enum", "yes", "en, id or other.", "en; id; other"),
    ("investments.csv", "stage"): ("enum", "yes", "announced, committed, financial_close or disbursed.", "announced; committed; financial_close; disbursed"),
    ("investments.csv", "instrument"): ("enum", "yes", "equity, debt, grant, guarantee, mixed or other.", "equity; debt; grant; guarantee; mixed; other"),
    ("project_events.csv", "event_type"): ("enum", "yes", "Dated event type.", "announced; groundbreaking; contract; financial_close; section_opened; opened; stalled; resumed; target_changed; other"),
    ("project_geometry.csv", "kind"): ("enum", "yes", "line, point or polygon.", "line; point; polygon"),
    ("corridor_segments.csv", "segment_type"): ("enum", "yes", "section, phase, package or other.", "section; phase; package; other"),
    ("estates.csv", "coordinate_source"): ("enum", "yes", "official, osm, regency, manual or unknown.", "official; osm; regency; manual; unknown"),
    ("conflicts.csv", "scope"): ("enum", "yes", "project, corridor, estate, dataset or method.", "project; corridor; estate; dataset; method"),
    ("project_sources.csv", "claim"): ("enum", "yes", "One atomic fact type; commas are not allowed.", ""),
    ("estate_sources.csv", "claim"): ("enum", "yes", "One atomic fact type; commas are not allowed.", ""),
    ("project_organizations.csv", "role"): ("enum", "yes", "sponsor, operator, contractor, lender, off_taker, developer or owner.", "sponsor; operator; contractor; lender; off_taker; developer; owner"),
}

CONDITIONAL = {
    ("projects.csv", "length_km"), ("projects.csv", "capacity"),
    ("projects.csv", "capacity_unit"), ("projects.csv", "opened_year"),
    ("projects.csv", "corridor_id"), ("estates.csv", "regency"),
    ("corridors.csv", "source_id"), ("corridor_segments.csv", "source_id"),
}


def main() -> None:
    examples: dict[str, dict[str, str]] = {}
    for name in TABLES:
        path = CURATED / name
        if not path.exists():
            continue
        rows = read_csv(path)
        examples[name] = {}
        for field in TABLES[name]:
            for row in rows:
                value = row.get(field, "")
                if value:
                    examples[name][field] = value[:120]
                    break

    out = []
    missing = []
    for name, fields in TABLES.items():
        label, description = TABLE_META[name]
        for field in fields:
            if (name, field) in OVERRIDES:
                kind, required, text, allowed = OVERRIDES[(name, field)]
            elif field in FIELD:
                kind, required, text = FIELD[field]
                allowed = ""
            else:
                missing.append(f"{name}.{field}")
                continue
            if (name, field) in CONDITIONAL:
                required = "conditional"
            out.append(
                {
                    "table": name,
                    "table_label": label,
                    "table_description": description,
                    "field": field,
                    "type": kind,
                    "required": required,
                    "description": text,
                    "allowed_values": allowed,
                    "example": examples.get(name, {}).get(field, ""),
                }
            )

    if missing:
        raise SystemExit(f"dictionary has no description for: {', '.join(missing)}")

    fields = [
        "table", "table_label", "table_description", "field", "type", "required",
        "description", "allowed_values", "example",
    ]
    DERIVED.mkdir(parents=True, exist_ok=True)
    write_csv(DERIVED / "data_dictionary.csv", fields, out)
    write_csv(SITE_DATA / "dictionary.csv", fields, out)
    print(f"OK: {len(out)} field definitions across {len(TABLES)} tables")


if __name__ == "__main__":
    main()
