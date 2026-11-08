"""Build the browser payload from the curated and flat tables.

Runtime payload (site/data/):
  projects.js       window.PROJECTS, same collection plus per-project sources
  corridors.js      window.CORRIDORS
  estates.js        window.INFRA_ESTATES (loaded lazily by the Estates view)
  stats.js          window.INFRA_STATS: counts, coverage, sources, downloads
  search.js         window.INFRA_SEARCH: build-time search index

Downloads (site/downloads/):
  projects.geojson, projects.csv, corridors.json, estates.json, estates.csv,
  estate-gap.csv, corridors-segments.csv, events.csv, sources.csv, claims.csv,
  conflicts.csv, freshness.csv, dictionary.csv, basemap.geojson

Run: python scripts/pipeline/build_site_data.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CORRIDOR_FIELDS,
    CURATED,
    DERIVED,
    DERIVED_FIELDS,
    EVENT_FIELDS,
    EXPORTS,
    ROOT,
    SEGMENT_FIELDS,
    SITE_DATA,
    SITE_DOWNLOADS,
    SOURCE_FIELDS,
    read_csv,
    write_csv,
)

PROJECTS_CSV = EXPORTS / "projects.csv"
CHANGELOG = ROOT / "CHANGELOG.md"

CLAIM_DOWNLOAD_FIELDS = [
    "project_id", "project_name", "sector", "claim", "claim_value", "claim_date",
    "source_id", "publisher", "source_title", "source_type", "source_url",
    "retrieved_on", "notes",
]


def source_record(source: dict[str, str], claim: str = "") -> dict[str, str]:
    record = {
        "id": source["id"],
        "publisher": source["publisher"],
        "title": source["title"],
        "url": source["url"],
        "published_on": source["published_on"],
        "retrieved_on": source["retrieved_on"],
        "source_type": source["source_type"],
        "language": source["language"],
        "archive_path": source["archive_path"],
        "notes": source["notes"],
    }
    if claim:
        record["claim"] = claim
    return record


def split_provinces(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def write_download_json(name: str, value: object, *, indent: int | None = None) -> None:
    separators = (",", ":") if indent is None else None
    text = json.dumps(value, ensure_ascii=False, indent=indent, separators=separators)
    (SITE_DOWNLOADS / name).write_text(text + "\n", encoding="utf-8")


def write_global(name: str, global_name: str, value: object) -> None:
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    (SITE_DATA / name).write_text(
        f"window.{global_name} = {text};\n", encoding="utf-8"
    )


def read_changelog() -> list[dict[str, object]]:
    """Parse ``## YYYY-MM-DD`` sections and their bullet lists."""
    if not CHANGELOG.exists():
        return []
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in CHANGELOG.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(\d{4}-\d{2}-\d{2})\s*[-—:]?\s*(.*)$", line)
        if heading:
            current = {
                "date": heading.group(1),
                "title": heading.group(2).strip(),
                "items": [],
            }
            entries.append(current)
            continue
        if current is not None and line.startswith(("- ", "* ")):
            current["items"].append(line[2:].strip())
    return entries


def main() -> None:
    rows = read_csv(PROJECTS_CSV)
    sources = {row["id"]: row for row in read_csv(CURATED / "sources.csv")}
    claims = read_csv(CURATED / "project_sources.csv")
    estates = read_csv(CURATED / "estates.csv")
    estate_gap = read_csv(DERIVED / "estate_gap_2026.csv")
    corridors = read_csv(CURATED / "corridors.csv")
    segments = read_csv(CURATED / "corridor_segments.csv")
    events = read_csv(CURATED / "project_events.csv")
    targets = read_csv(CURATED / "coverage_targets.csv")
    psn_ledger = read_csv(DERIVED / "psn_reconciliation.csv")
    conflicts = read_csv(CURATED / "conflicts.csv")
    freshness = read_csv(DERIVED / "freshness_report.csv")
    dictionary = read_csv(DERIVED / "data_dictionary.csv")
    claims_audit = read_csv(DERIVED / "claims_audit.csv")
    changelog = read_changelog()

    freshness_by_entity = {
        (row["entity_type"], row["entity_id"]): row for row in freshness
    }

    # One source entry per project, with all of its claims joined. A row may
    # have several claims against the same document (status, location, opening,
    # investment), and the drawer should not repeat the document four times.
    claims_by_project: dict[str, dict[str, list[str]]] = {}
    for claim in claims:
        if claim["source_id"] in sources:
            claims_by_project.setdefault(claim["project_id"], {}).setdefault(
                claim["source_id"], []
            ).append(claim["claim"])

    projects_by_id = {row["id"]: row for row in rows}
    claim_payload = []
    for claim in claims:
        source = sources.get(claim["source_id"], {})
        project = projects_by_id.get(claim["project_id"], {})
        claim_payload.append(
            {
                "project_id": claim["project_id"],
                "project_name": project.get("name", ""),
                "sector": project.get("sector", ""),
                "claim": claim["claim"],
                "claim_value": claim["claim_value"],
                "claim_date": claim["claim_date"],
                "source_id": claim["source_id"],
                "publisher": source.get("publisher", ""),
                "source_title": source.get("title", ""),
                "source_type": source.get("source_type", ""),
                "source_url": source.get("url", ""),
                "retrieved_on": source.get("retrieved_on", ""),
                "notes": claim["notes"],
            }
        )

    corridor_names = {row["id"]: row["name"] for row in corridors}

    events_by_project: dict[str, list[dict[str, str]]] = {}
    for event in events:
        source = sources.get(event["source_id"])
        events_by_project.setdefault(event["project_id"], []).append(
            {
                "id": event["id"],
                "event_date": event["event_date"],
                "event_type": event["event_type"],
                "description": event["description"],
                "source_id": event["source_id"],
                "source_title": source["title"] if source else "",
                "source_url": source["url"] if source else "",
                "notes": event["notes"],
            }
        )
    for records in events_by_project.values():
        records.sort(key=lambda record: record["event_date"])

    features = []
    for row in rows:
        properties = {
            field: row[field] for field in DERIVED_FIELDS if field not in {"lat", "lon"}
        }
        properties["corridor_name"] = corridor_names.get(row["corridor_id"], "")
        properties["sources"] = [
            source_record(sources[source_id], "; ".join(dict.fromkeys(kinds)))
            for source_id, kinds in claims_by_project.get(row["id"], {}).items()
        ]
        properties["events"] = events_by_project.get(row["id"], [])
        freshness_row = freshness_by_entity.get(("project", row["id"]), {})
        properties["freshness_state"] = freshness_row.get("state", "unknown")
        properties["freshness_age_days"] = freshness_row.get("age_days", "")
        properties["freshness_due"] = freshness_row.get("refresh_due", "")
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row["lon"]), float(row["lat"])],
                },
                "properties": properties,
            }
        )

    collection = {"type": "FeatureCollection", "features": features}

    corridor_payload = []
    for row in corridors:
        source = sources.get(row["source_id"])
        corridor_segments = []
        for segment in segments:
            if segment["corridor_id"] != row["id"]:
                continue
            segment_source = sources.get(segment["source_id"])
            corridor_segments.append(
                {
                    **{
                        field: segment[field]
                        for field in SEGMENT_FIELDS
                        if field != "source_id"
                    },
                    "source_id": segment["source_id"],
                    "source_title": segment_source["title"] if segment_source else "",
                    "source_url": segment_source["url"] if segment_source else "",
                }
            )
        segment_km = sum(float(segment["length_km"]) for segment in corridor_segments)
        segment_operational = sum(
            float(segment["operational_km"])
            for segment in corridor_segments
            if segment["operational_km"]
        )
        corridor_events = []
        for project_row in rows:
            if project_row["corridor_id"] != row["id"]:
                continue
            for event in events_by_project.get(project_row["id"], []):
                corridor_events.append(
                    {
                        **event,
                        "project_id": project_row["id"],
                        "project_name": project_row["name"],
                    }
                )
        corridor_events.sort(key=lambda event: event["event_date"])
        corridor_payload.append(
            {
                **{field: row[field] for field in CORRIDOR_FIELDS if field != "source_id"},
                "source_id": row["source_id"],
                "source_publisher": source["publisher"] if source else "",
                "source_title": source["title"] if source else "",
                "source_url": source["url"] if source else "",
                "source_type": source["source_type"] if source else "",
                "retrieved_on": source["retrieved_on"] if source else "",
                "segment_km": round(segment_km, 3),
                "segment_operational_km": round(segment_operational, 3),
                "segment_share": (
                    round(segment_km / float(row["total_km"]) * 100, 1)
                    if row["total_km"] and segment_km
                    else None
                ),
                "segments": corridor_segments,
                "events": corridor_events,
            }
        )

    estate_payload = []
    for row in estates:
        source = sources.get(row["source_id"])
        freshness_row = freshness_by_entity.get(("estate", row["id"]), {})
        estate_payload.append(
            {
                **row,
                "source_publisher": source["publisher"] if source else "",
                "source_title": source["title"] if source else "",
                "source_url": source["url"] if source else "",
                "source_type": source["source_type"] if source else "",
                "retrieved_on": source["retrieved_on"] if source else "",
                "freshness_state": freshness_row.get("state", "unknown"),
                "freshness_age_days": freshness_row.get("age_days", ""),
                "freshness_due": freshness_row.get("refresh_due", ""),
            }
        )
    estate_payload.sort(key=lambda row: row["name"].casefold())

    by_status = Counter(row["status"] for row in rows)
    by_sector = Counter(row["sector"] for row in rows)
    by_province: Counter[str] = Counter()
    for row in rows:
        by_province.update(split_provinces(row["province"]))
    psn = Counter(row["psn"] for row in rows)
    precision = Counter(row["precision"] for row in rows)
    by_island = Counter(row["island"] for row in rows)
    verification = Counter(row["verification"] for row in rows)

    estate_types = Counter(row["type"] for row in estates)
    estate_provinces = {row["province"] for row in estates if row["province"]}
    estate_area = sum(float(row["area_ha"]) for row in estates if row["area_ha"])
    estate_coord_sources = Counter(row["coordinate_source"] for row in estates)

    last_verified_projects = max((row["last_verified"] for row in rows), default="")
    last_verified_estates = max((row["last_verified"] for row in estates), default="")
    last_verified = max(last_verified_projects, last_verified_estates)

    freshness_counts = Counter(
        (row["entity_type"], row["state"]) for row in freshness
    )
    next_due = min((row["refresh_due"] for row in freshness if row["refresh_due"]), default="")
    attention = [
        row for row in freshness if row["state"] in {"due_soon", "stale", "unknown"}
    ]

    claims_missing = Counter()
    for row in claims_audit:
        if row["missing"] and row["missing"] != "none":
            for item in row["missing"].split(";"):
                claims_missing[item] += 1
    fully_claimed = sum(1 for row in claims_audit if row["missing"] == "none")

    conflict_payload = []
    for row in conflicts:
        source_a = sources.get(row["source_a"])
        source_b = sources.get(row["source_b"])
        conflict_payload.append(
            {
                **row,
                "source_a_publisher": source_a["publisher"] if source_a else "",
                "source_a_title": source_a["title"] if source_a else "",
                "source_a_url": source_a["url"] if source_a else "",
                "source_b_publisher": source_b["publisher"] if source_b else "",
                "source_b_title": source_b["title"] if source_b else "",
                "source_b_url": source_b["url"] if source_b else "",
            }
        )
    conflict_payload.sort(key=lambda row: (row["status"] != "open", row["subject"].casefold()))

    current_counts = {
        "roads": by_sector.get("road", 0),
        "railways": by_sector.get("railway", 0),
        "airports": by_sector.get("airport", 0),
        "seaports": by_sector.get("seaport", 0),
        "factories": by_sector.get("factory", 0),
        "transport_psn": sum(
            1 for row in rows
            if row["sector"] in {"railway", "airport", "seaport"} and row["psn"] == "yes"
        ),
        "psn_projects": sum(
            1 for row in psn_ledger
            if row["status"] == "active" and row["kind"] == "project"
            and row["match_status"].startswith("matched")
        ),
        "psn_programmes": sum(
            1 for row in psn_ledger
            if row["status"] == "active" and row["kind"] == "programme"
            and row["match_status"].startswith("matched")
        ),
        "psn_industrial_areas": sum(
            1 for row in psn_ledger
            if row["status"] == "active" and row["sector"] == "industrial_areas"
            and row["match_status"].startswith("matched")
        ),
        "industrial_estates": estate_types.get("industrial_estate", 0)
        + estate_types.get("both", 0),
        "sezs": estate_types.get("sez", 0) + estate_types.get("both", 0),
        "unique_estates": len(estates),
        "corridors_with_total": sum(1 for row in corridors if row["total_km"]),
        "sources": len(sources),
    }

    coverage = []
    for target in targets:
        layer = target["layer"]
        current = current_counts.get(layer, 0)
        target_count = int(target["target_count"])
        gap = max(target_count - current, 0)
        share = (current / target_count) if target_count else 1
        status = "met" if current >= target_count else ("partial" if share >= 0.8 else "gap")
        coverage.append(
            {
                "layer": layer,
                "label": target["label"],
                "unit": target["unit"],
                "current": current,
                "target": target_count,
                "gap": gap,
                "share": round(share * 100, 1),
                "status": status,
                "reference_set": target["reference_set"],
                "notes": target["notes"],
            }
        )

    stats = {
        # Deterministic by default: the build date is the newest verification
        # date unless the refresh run sets INFRAA_BUILD_DATE.
        "generated_on": os.environ.get("INFRAA_BUILD_DATE", "") or last_verified,
        "data_as_of": last_verified,
        "projects": {
            "total": len(rows),
            "by_sector": dict(sorted(by_sector.items())),
            "by_status": dict(sorted(by_status.items())),
            "by_province": dict(by_province.most_common()),
            "psn": dict(sorted(psn.items())),
            "precision": dict(sorted(precision.items())),
            "island": dict(sorted(by_island.items())),
            "verification": dict(sorted(verification.items())),
            "with_investment": sum(1 for row in rows if row["investment_idr_t"]),
            "with_progress": sum(1 for row in rows if row["progress_pct"]),
            "with_opened_year": sum(1 for row in rows if row["opened_year"]),
            "with_length": sum(1 for row in rows if row["length_km"]),
            "claim_count": len(claims),
            "source_count": len(sources),
            "last_verified": last_verified_projects,
        },
        "corridors": {
            "total": len(corridors),
            "with_total": current_counts["corridors_with_total"],
            "segments": len(segments),
            "events": len(events),
        },
        "estates": {
            "total": len(estates),
            "industrial": current_counts["industrial_estates"],
            "sez": current_counts["sezs"],
            "both": estate_types.get("both", 0),
            "area_ha": round(estate_area, 1),
            "provinces": len(estate_provinces),
            "coordinate_sources": dict(sorted(estate_coord_sources.items())),
            "gap_rows": len(estate_gap),
            "last_verified": last_verified_estates,
        },
        "freshness": {
            "as_of": os.environ.get("INFRAA_AS_OF", "") or last_verified,
            "stale_after_days": 183,
            "records": len(freshness),
            "counts": {
                "project": {
                    state: freshness_counts.get(("project", state), 0)
                    for state in ("fresh", "due_soon", "stale", "unknown")
                },
                "estate": {
                    state: freshness_counts.get(("estate", state), 0)
                    for state in ("fresh", "due_soon", "stale", "unknown")
                },
            },
            "next_due": next_due,
            "attention": attention,
        },
        "claims": {
            "total": len(claims),
            "projects_fully_claimed": fully_claimed,
            "projects_total": len(rows),
            "missing": dict(sorted(claims_missing.items())),
        },
        "conflicts": {
            "total": len(conflict_payload),
            "open": sum(1 for row in conflict_payload if row["status"] == "open"),
            "resolved": sum(1 for row in conflict_payload if row["status"] == "resolved"),
            "rows": conflict_payload,
        },
        "dictionary": [
            {
                "table": row["table"],
                "table_label": row["table_label"],
                "field": row["field"],
                "type": row["type"],
                "required": row["required"],
                "description": row["description"],
                "allowed_values": row["allowed_values"],
            }
            for row in dictionary
        ],
        "changelog": changelog,
        "coverage": coverage,
        "sources": [
            source_record(source)
            for source in sorted(sources.values(), key=lambda row: row["publisher"])
        ],
        "downloads": [
            {
                "label": "Projects",
                "file": "downloads/projects.csv",
                "meta": f"{len(rows)} rows · flat export",
            },
            {
                "label": "Projects (GeoJSON)",
                "file": "downloads/projects.geojson",
                "meta": f"{len(rows)} point features",
            },
            {
                "label": "Estates and SEZs",
                "file": "downloads/estates.csv",
                "meta": f"{len(estates)} rows · table only",
            },
            {
                "label": "Estate gap ledger",
                "file": "downloads/estate-gap.csv",
                "meta": f"{len(estate_gap)} rows · 179-vs-160 reconciliation",
            },
            {
                "label": "Corridors",
                "file": "downloads/corridors.json",
                "meta": f"{len(corridors)} corridor summaries",
            },
            {
                "label": "Corridor segments",
                "file": "downloads/corridors-segments.csv",
                "meta": f"{len(segments)} sections · five corridors",
            },
            {
                "label": "Project events",
                "file": "downloads/events.csv",
                "meta": f"{len(events)} dated events",
            },
            {
                "label": "Sources",
                "file": "downloads/sources.csv",
                "meta": f"{len(sources)} documents",
            },
            {
                "label": "Project claims",
                "file": "downloads/claims.csv",
                "meta": f"{len(claims)} atomic claims",
            },
            {
                "label": "Conflict register",
                "file": "downloads/conflicts.csv",
                "meta": f"{len(conflicts)} conflicts · {sum(1 for row in conflicts if row['status'] == 'open')} open",
            },
            {
                "label": "Freshness report",
                "file": "downloads/freshness.csv",
                "meta": f"{len(freshness)} rows · as of {os.environ.get('INFRAA_AS_OF', '') or last_verified}",
            },
            {
                "label": "Data dictionary",
                "file": "downloads/dictionary.csv",
                "meta": f"{len(dictionary)} field definitions",
            },
            {
                "label": "Basemap",
                "file": "downloads/basemap.geojson",
                "meta": "Natural Earth-derived offline basemap",
            },
        ],
    }

    search = []
    for row in rows:
        search.append(
            {
                "type": "project",
                "id": row["id"],
                "name": row["name"],
                "sector": row["sector"],
                "status": row["status"],
                "province": row["province"],
                "text": " ".join(
                    filter(
                        None,
                        [
                            row["name"],
                            row["province"],
                            row["island"],
                            row["route"],
                            row["operator"],
                            row["subsector"],
                            row["corridor_id"].replace("-", " "),
                            corridor_names.get(row["corridor_id"], ""),
                            "PSN" if row["psn"] == "yes" else "",
                        ],
                    )
                ),
            }
        )
    for row in estates:
        search.append(
            {
                "type": "estate",
                "id": row["id"],
                "name": row["name"],
                "type_label": row["type"],
                "province": row["province"],
                "text": " ".join(
                    filter(
                        None,
                        [
                            row["name"],
                            row["province"],
                            row["regency"],
                            row["developer"],
                            row["sector_focus"],
                            row["type"].replace("_", " "),
                        ],
                    )
                ),
            }
        )

    SITE_DATA.mkdir(parents=True, exist_ok=True)
    SITE_DOWNLOADS.mkdir(parents=True, exist_ok=True)

    write_download_json("projects.geojson", collection, indent=2)
    write_global("projects.js", "PROJECTS", collection)
    write_csv(SITE_DOWNLOADS / "projects.csv", DERIVED_FIELDS, rows)

    write_download_json("corridors.json", corridor_payload, indent=2)
    write_global("corridors.js", "CORRIDORS", corridor_payload)

    write_download_json("estates.json", estate_payload, indent=2)
    write_global("estates.js", "INFRA_ESTATES", estate_payload)
    write_csv(
        SITE_DOWNLOADS / "estates.csv",
        list(estates[0].keys()) if estates else [],
        estate_payload,
    )
    write_csv(
        SITE_DOWNLOADS / "estate-gap.csv",
        list(estate_gap[0].keys()) if estate_gap else [],
        estate_gap,
    )

    write_csv(SITE_DOWNLOADS / "sources.csv", SOURCE_FIELDS, list(sources.values()))
    write_csv(SITE_DOWNLOADS / "corridors-segments.csv", SEGMENT_FIELDS, segments)
    write_csv(SITE_DOWNLOADS / "events.csv", EVENT_FIELDS, events)
    write_csv(SITE_DOWNLOADS / "claims.csv", CLAIM_DOWNLOAD_FIELDS, claim_payload)
    write_csv(
        SITE_DOWNLOADS / "conflicts.csv",
        list(conflicts[0].keys()) if conflicts else [],
        conflicts,
    )
    write_csv(
        SITE_DOWNLOADS / "freshness.csv",
        list(freshness[0].keys()) if freshness else [],
        freshness,
    )
    write_csv(
        SITE_DOWNLOADS / "dictionary.csv",
        list(dictionary[0].keys()) if dictionary else [],
        dictionary,
    )

    write_global("stats.js", "INFRA_STATS", stats)
    write_global("search.js", "INFRA_SEARCH", search)

    print(
        f"wrote {len(features)} projects, {len(corridor_payload)} corridors, "
        f"{len(estate_payload)} estates, {len(sources)} sources"
    )
    print(
        f"site payload: {sum(p.stat().st_size for p in SITE_DATA.iterdir()) / 1024:.0f} KB runtime, "
        f"{sum(p.stat().st_size for p in SITE_DOWNLOADS.iterdir()) / 1024:.0f} KB downloads"
    )


if __name__ == "__main__":
    main()
