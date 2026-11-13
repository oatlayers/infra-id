"""Build the field-level data dictionary.

The dictionary is generated from the schema in ``data_model.py`` plus the
descriptions below, so it cannot drift from the CSV headers. Indonesian
descriptions come from ``data/i18n/dictionary.id.json``. It is written to
``data/derived/data_dictionary.csv`` and copied to ``site/downloads/dictionary.csv``
for download.

Run: python scripts/pipeline/build_dictionary.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import CURATED, DERIVED, ROOT, SITE_DOWNLOADS, TABLES, read_csv, write_csv

DICTIONARY_I18N = ROOT / "data" / "i18n" / "dictionary.id.json"

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
    "coverage_targets.csv": ("Coverage targets", "The reference set and target count for every data layer."),
    "conflicts.csv": ("Conflict register", "Known disagreements between sources, with both values and resolutions."),
    "psn_register.csv": ("PSN register", "The 226 active projects and 24 active programmes in Permenko 16/2025, with deleted slots retained for audit."),
    "programmes.csv": ("Programmes", "The 24 active PSN programmes, with bilingual names, summaries, lead agency and source."),
    "programme_projects.csv": ("Programme projects", "Structural links between a programme and the atlas projects that illustrate it."),
    "programme_sources.csv": ("Programme claims", "One atomic fact per programme-source link."),
    "translations.csv": ("Translations", "Reviewed English and Indonesian text for entity names, summaries and definitions that are not carried in a bilingual curated field."),
    "indicators.csv": ("Indicators", "Programme or project targets, baselines and units, with their own source."),
    "indicator_values.csv": ("Indicator values", "Dated observations for an indicator, each with its own source."),
    "project_phases.csv": ("Project phases", "Sourced stages of a project, with status, dates, cost and progress where stated."),
    "pkpn_programmes.csv": ("PKPN programmes", "The eight 2027 Program Kerja Prioritas Nasional, with bilingual summaries, targets, budget and source."),
    "pkpn_sources.csv": ("PKPN claims", "One atomic fact per PKPN-source link."),
}

FIELD = {
    "id": ("id", "yes", "Stable lowercase-hyphenated identifier used in deep links and joins."),
    "entity_type": ("enum", "yes", "Entity family being translated: project, programme, corridor, estate, company, indicator or source."),
    "entity_id": ("id", "yes", "Foreign key to the entity in its own table."),
    "field": ("enum", "yes", "Translated field: name, summary, target_summary, definition, unit_label or title."),
    "locale": ("enum", "yes", "Locale code: en or id."),
    "text": ("text", "yes", "Display text in the stated locale."),
    "translator": ("text", "conditional", "Translator or editor for a reviewed or official translation."),
    "reviewed_on": ("date", "conditional", "Review date for a reviewed or official translation."),
    "direction": ("enum", "yes", "Whether the indicator should increase, decrease, hold or reach a target."),
    "unit": ("text", "yes", "Unit of the indicator, such as GWp, km, % or million m3."),
    "baseline_value": ("decimal", "no", "Starting value for the indicator."),
    "baseline_date": ("date", "no", "Date of the baseline value."),
    "target_value": ("decimal", "no", "Target value for the indicator."),
    "target_date": ("date", "no", "Date by which the target is to be reached."),
    "indicator_id": ("id", "yes", "Foreign key to indicators.csv."),
    "value": ("decimal", "yes", "Observed value at as_of."),
    "as_of": ("date", "yes", "Date of the observed value."),
    "phase": ("text", "yes", "Stable phase key, such as phase_1 or operation."),
    "cost_idr_t": ("decimal", "no", "Phase cost in trillion rupiah, only when the source splits it."),
    "start_date": ("date", "no", "Phase start date when the source states one."),
    "end_date": ("date", "no", "Phase end or opening date when the source states one."),
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
    "target_count": ("integer", "yes", "Target number of rows for the layer."),
    "reference_set": ("text", "yes", "Definition of the target reference set."),
    "definition": ("text", "yes", "What the corridor includes and excludes."),
    "metric": ("text", "yes", "Metric used for the corridor figure."),
    "total_km": ("decimal", "yes", "Published corridor total in kilometres."),
    "scope": ("enum", "yes", "Conflict scope: project, corridor, estate, dataset or method."),
    "value_a": ("text", "yes", "First value, with its date or scope when needed."),
    "value_b": ("text", "yes", "Second value, with its date or scope when needed."),
    "resolution": ("text", "yes", "What the atlas does with the conflict."),
    "psn_no": ("integer", "yes", "Official number in the Permenko 16/2025 annex; project and programme numbers are separate sequences."),
    "sector_code": ("text", "yes", "Official annex letter A-N for projects, or programme for the programme section."),
    "name_id": ("text", "yes", "Official Indonesian name as printed in the regulation."),
    "location": ("text", "no", "Official location text as printed in the regulation."),
    "name_en": ("text", "yes", "Display name in English."),
    "theme": ("enum", "yes", "Programme theme used for filtering and display."),
    "pkpn_id": ("enum", "no", "Optional link to one of the eight national priority programmes (PKPN)."),
    "lead_org_id": ("id", "conditional", "Foreign key to the organisation leading the programme."),
    "summary_id": ("text", "yes", "Short Indonesian summary of the programme scope."),
    "summary_en": ("text", "yes", "Short English summary of the programme scope."),
    "target_summary_id": ("text", "no", "Indonesian summary of the published target; blank when the source states none."),
    "target_summary_en": ("text", "no", "English summary of the published target; blank when the source states none."),
    "target_year": ("year", "no", "Target completion year when a source states one."),
    "budget_idr_t": ("decimal", "no", "Programme budget in trillion rupiah when a source states one."),
    "programme_id": ("id", "yes", "Foreign key to programmes.csv."),
}

# Context-specific overrides where a field means different things by table.
OVERRIDES = {
    ("projects.csv", "status"): ("enum", "yes", "planned, under_construction, operating, recently_completed, stalled or unknown. Unknown marks a register-only record whose implementation status is not yet sourced.", "planned; under_construction; operating; recently_completed; stalled; unknown"),
    ("estates.csv", "status"): ("enum", "yes", "Designation-level operating, under_construction, planned or unknown; not independently verified for most estates.", "operating; under_construction; planned; unknown"),
    ("corridor_segments.csv", "status"): ("enum", "yes", "Segment status using the project status vocabulary.", "planned; under_construction; operating; recently_completed; stalled"),
    ("conflicts.csv", "status"): ("enum", "yes", "Whether the conflict remains open or has a recorded resolution.", "open; resolved"),
    ("estates.csv", "type"): ("enum", "yes", "industrial_estate, sez or both.", "industrial_estate; sez; both"),
    ("projects.csv", "sector"): ("enum", "yes", "road, railway, airport, seaport, factory, energy, water, urban, coastal, housing, technology, education, tourism or agriculture.", "road; railway; airport; seaport; factory; energy; water; urban; coastal; housing; technology; education; tourism; agriculture"),
    ("projects.csv", "island"): ("enum", "yes", "Sumatra, Java, Kalimantan, Sulawesi, Papua, Bali-Nusa Tenggara, Maluku or National.", "Sumatra; Java; Kalimantan; Sulawesi; Papua; Bali-Nusa Tenggara; Maluku; National"),
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
    ("conflicts.csv", "field"): ("text", "yes", "Field or fact in dispute.", ""),
    ("corridors.csv", "as_of"): ("date", "yes", "Date of the corridor figures.", ""),
    ("coverage_targets.csv", "unit"): ("text", "yes", "Unit counted by the coverage target.", ""),
    ("project_sources.csv", "claim"): ("enum", "yes", "One atomic fact type; commas are not allowed.", ""),
    ("estate_sources.csv", "claim"): ("enum", "yes", "One atomic fact type; commas are not allowed.", ""),
    ("project_organizations.csv", "role"): ("enum", "yes", "sponsor, operator, contractor, lender, off_taker, developer or owner.", "sponsor; operator; contractor; lender; off_taker; developer; owner"),
    ("psn_register.csv", "kind"): ("enum", "yes", "project or programme.", "project; programme"),
    ("psn_register.csv", "status"): ("enum", "yes", "active or deleted in the current annex.", "active; deleted"),
    ("psn_register.csv", "sector"): ("enum", "yes", "Normalised sector key used by the reconciliation ledger.", "roads_and_bridges; ports; airports; railways; industrial_areas; housing; dams_and_irrigation; water_and_sanitation; coastal_defence; energy; technology; education; tourism; agriculture; programme"),
    ("psn_register.csv", "description"): ("text", "no", "Programme description from the annex; blank for projects.", ""),
    ("programmes.csv", "status"): ("enum", "yes", "active, paused or completed.", "active; paused; completed"),
    ("programmes.csv", "theme"): ("enum", "yes", "Programme theme used for filtering.", "energy; economy; border; transport; tourism; industry; food; urban; water; health; education; social; environment"),
    ("programmes.csv", "pkpn_id"): ("enum", "no", "Optional PKPN link.", "pkpn-food; pkpn-energy-water; pkpn-education; pkpn-health; pkpn-downstreaming; pkpn-infrastructure; pkpn-housing; pkpn-resilience"),
    ("programme_projects.csv", "role"): ("enum", "yes", "primary, component or related.", "primary; component; related"),
    ("programme_sources.csv", "claim"): ("enum", "yes", "One atomic fact type; commas are not allowed.", ""),
    ("translations.csv", "entity_type"): ("enum", "yes", "project, programme, corridor, estate, company, indicator or source.", "project; programme; corridor; estate; company; indicator; source"),
    ("translations.csv", "field"): ("enum", "yes", "name, summary, target_summary, definition, unit_label or title.", "name; summary; target_summary; definition; unit_label; title"),
    ("translations.csv", "locale"): ("enum", "yes", "en or id.", "en; id"),
    ("translations.csv", "status"): ("enum", "yes", "official, reviewed, draft, machine or missing.", "official; reviewed; draft; machine; missing"),
    ("translations.csv", "text"): ("text", "yes", "Display text in the stated locale.", ""),
    ("translations.csv", "translator"): ("text", "conditional", "Translator or editor for a reviewed or official translation.", ""),
    ("translations.csv", "reviewed_on"): ("date", "conditional", "Review date for a reviewed or official translation.", ""),
    ("indicators.csv", "direction"): ("enum", "yes", "increase, decrease, target or maintain.", "increase; decrease; target; maintain"),
    ("indicators.csv", "programme_id"): ("id", "conditional", "Foreign key to programmes.csv; at least one of programme_id or project_id is required.", ""),
    ("indicators.csv", "project_id"): ("id", "conditional", "Foreign key to projects.csv; at least one of programme_id or project_id is required.", ""),
    ("indicators.csv", "notes"): ("text", "no", "Caveats, target-year convention and source context.", ""),
    ("indicator_values.csv", "notes"): ("text", "no", "Observation context and source caveats.", ""),
    ("project_phases.csv", "status"): ("enum", "yes", "planned, under_construction, operating, recently_completed, stalled or unknown.", "planned; under_construction; operating; recently_completed; stalled; unknown"),
    ("project_phases.csv", "notes"): ("text", "no", "Scope, package context and caveats.", ""),
    ("project_phases.csv", "cost_idr_t"): ("decimal", "no", "Phase cost in trillion rupiah, only when the source splits it.", ""),
    ("project_phases.csv", "start_date"): ("date", "no", "Phase start date when the source states one.", ""),
    ("project_phases.csv", "end_date"): ("date", "no", "Phase end or opening date when the source states one.", ""),
    ("project_phases.csv", "progress_pct"): ("decimal", "no", "Reported phase progress, 0-100.", ""),
    ("pkpn_sources.csv", "claim"): ("enum", "yes", "One atomic fact type; commas are not allowed.", ""),
    ("pkpn_programmes.csv", "theme"): ("enum", "yes", "Programme theme used for filtering.", "energy; economy; border; transport; infrastructure; tourism; industry; food; urban; water; health; education; social; environment"),
}

CONDITIONAL = {
    ("projects.csv", "length_km"), ("projects.csv", "capacity"),
    ("projects.csv", "capacity_unit"), ("projects.csv", "opened_year"),
    ("projects.csv", "corridor_id"), ("estates.csv", "regency"),
    ("corridors.csv", "source_id"), ("corridor_segments.csv", "source_id"),
    ("translations.csv", "translator"), ("translations.csv", "reviewed_on"),
    ("indicators.csv", "programme_id"), ("indicators.csv", "project_id"),
    ("project_phases.csv", "cost_idr_t"), ("project_phases.csv", "start_date"),
    ("project_phases.csv", "end_date"), ("project_phases.csv", "progress_pct"),
}


def main() -> None:
    i18n = json.loads(DICTIONARY_I18N.read_text(encoding="utf-8"))
    table_id = i18n.get("table", {})
    field_id = i18n.get("field", {})

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
                    "table_description_id": table_id.get(description, ""),
                    "field": field,
                    "type": kind,
                    "required": required,
                    "description": text,
                    "description_id": field_id.get(text, ""),
                    "allowed_values": allowed,
                    "example": examples.get(name, {}).get(field, ""),
                }
            )

    if missing:
        raise SystemExit(f"dictionary has no description for: {', '.join(missing)}")

    missing_id = [
        f"{row['table']}.{row['field']}"
        for row in out
        if not row["description_id"] or not row["table_description_id"]
    ]
    if missing_id:
        raise SystemExit(
            f"dictionary has no Indonesian description for: {', '.join(missing_id[:20])}"
        )

    fields = [
        "table", "table_label", "table_description", "table_description_id", "field",
        "type", "required", "description", "description_id", "allowed_values", "example",
    ]
    DERIVED.mkdir(parents=True, exist_ok=True)
    write_csv(DERIVED / "data_dictionary.csv", fields, out)
    write_csv(SITE_DOWNLOADS / "dictionary.csv", fields, out)
    print(f"OK: {len(out)} field definitions across {len(TABLES)} tables")


if __name__ == "__main__":
    main()
