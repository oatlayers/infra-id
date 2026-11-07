"""Build the browser payload from the curated and flat tables.

Outputs, all under site/data/:
  projects.geojson  standard GeoJSON FeatureCollection
  projects.js       window.PROJECTS, same collection plus per-project sources
  projects.csv      downloadable copy of the flat export
  corridors.json    Trans corridor summary with source metadata and segments
  corridors.js      window.CORRIDORS
  estates.json      estate and SEZ table payload
  estates.js        window.INFRA_ESTATES (loaded lazily by the Estates view)
  estates.csv       downloadable estate table
  sources.csv       downloadable source register
  stats.js          window.INFRA_STATS: counts, coverage, sources, downloads
  search.js         window.INFRA_SEARCH: build-time search index

Run: python scripts/build_site_data.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

from data_model import (
    CORRIDOR_FIELDS,
    CURATED,
    DERIVED_FIELDS,
    ROOT,
    SITE_DATA,
    SOURCE_FIELDS,
    read_csv,
    write_csv,
)

PROJECTS_CSV = ROOT / "data" / "projects.csv"


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


def write_json(name: str, value: object, *, indent: int | None = None) -> None:
    separators = (",", ":") if indent is None else None
    text = json.dumps(value, ensure_ascii=False, indent=indent, separators=separators)
    (SITE_DATA / name).write_text(text + "\n", encoding="utf-8")


def write_global(name: str, global_name: str, value: object) -> None:
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    (SITE_DATA / name).write_text(
        f"window.{global_name} = {text};\n", encoding="utf-8"
    )


def main() -> None:
    rows = read_csv(PROJECTS_CSV)
    sources = {row["id"]: row for row in read_csv(CURATED / "sources.csv")}
    claims = read_csv(CURATED / "project_sources.csv")
    estates = read_csv(CURATED / "estates.csv")
    corridors = read_csv(CURATED / "corridors.csv")
    segments = read_csv(CURATED / "corridor_segments.csv")
    targets = read_csv(CURATED / "coverage_targets.csv")

    # One source entry per project, with all of its claims joined. A row may
    # have several claims against the same document (status, location, opening,
    # investment), and the drawer should not repeat the document four times.
    claims_by_project: dict[str, dict[str, list[str]]] = {}
    for claim in claims:
        if claim["source_id"] in sources:
            claims_by_project.setdefault(claim["project_id"], {}).setdefault(
                claim["source_id"], []
            ).append(claim["claim"])

    corridor_names = {row["id"]: row["name"] for row in corridors}

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
        corridor_segments = [
            {
                "id": segment["id"],
                "name": segment["name"],
                "length_km": segment["length_km"],
                "status": segment["status"],
                "opened_year": segment["opened_year"],
                "notes": segment["notes"],
            }
            for segment in segments
            if segment["corridor_id"] == row["id"]
        ]
        corridor_payload.append(
            {
                **{field: row[field] for field in CORRIDOR_FIELDS if field != "source_id"},
                "source_id": row["source_id"],
                "source_publisher": source["publisher"] if source else "",
                "source_title": source["title"] if source else "",
                "source_url": source["url"] if source else "",
                "source_type": source["source_type"] if source else "",
                "retrieved_on": source["retrieved_on"] if source else "",
                "segments": corridor_segments,
            }
        )

    estate_payload = []
    for row in estates:
        source = sources.get(row["source_id"])
        estate_payload.append(
            {
                **row,
                "source_publisher": source["publisher"] if source else "",
                "source_title": source["title"] if source else "",
                "source_url": source["url"] if source else "",
                "source_type": source["source_type"] if source else "",
                "retrieved_on": source["retrieved_on"] if source else "",
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

    last_verified_projects = max((row["last_verified"] for row in rows), default="")
    last_verified_estates = max((row["last_verified"] for row in estates), default="")
    last_verified = max(last_verified_projects, last_verified_estates)

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
        "industrial_estates": estate_types.get("industrial_estate", 0)
        + estate_types.get("both", 0),
        "sezs": estate_types.get("sez", 0) + estate_types.get("both", 0),
        "unique_estates": len(estates),
        "corridors_with_series": sum(1 for row in corridors if row["total_km"]),
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
                "universe": target["universe"],
                "notes": target["notes"],
            }
        )

    stats = {
        "generated_on": date.today().isoformat(),
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
            "with_series": current_counts["corridors_with_series"],
            "segments": len(segments),
        },
        "estates": {
            "total": len(estates),
            "industrial": current_counts["industrial_estates"],
            "sez": current_counts["sezs"],
            "both": estate_types.get("both", 0),
            "area_ha": round(estate_area, 1),
            "provinces": len(estate_provinces),
            "last_verified": last_verified_estates,
        },
        "coverage": coverage,
        "sources": [
            source_record(source)
            for source in sorted(sources.values(), key=lambda row: row["publisher"])
        ],
        "downloads": [
            {
                "label": "Projects",
                "file": "data/projects.csv",
                "meta": f"{len(rows)} rows · flat export",
            },
            {
                "label": "Projects (GeoJSON)",
                "file": "data/projects.geojson",
                "meta": f"{len(rows)} point features",
            },
            {
                "label": "Estates and SEZs",
                "file": "data/estates.csv",
                "meta": f"{len(estates)} rows · table only",
            },
            {
                "label": "Corridors",
                "file": "data/corridors.json",
                "meta": f"{len(corridors)} corridor summaries",
            },
            {
                "label": "Sources",
                "file": "data/sources.csv",
                "meta": f"{len(sources)} documents",
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

    write_json("projects.geojson", collection, indent=2)
    write_global("projects.js", "PROJECTS", collection)
    write_csv(SITE_DATA / "projects.csv", DERIVED_FIELDS, rows)

    write_json("corridors.json", corridor_payload, indent=2)
    write_global("corridors.js", "CORRIDORS", corridor_payload)

    write_json("estates.json", estate_payload, indent=2)
    write_global("estates.js", "INFRA_ESTATES", estate_payload)
    write_csv(
        SITE_DATA / "estates.csv",
        list(estates[0].keys()) if estates else [],
        estate_payload,
    )

    write_csv(SITE_DATA / "sources.csv", SOURCE_FIELDS, list(sources.values()))

    write_global("stats.js", "INFRA_STATS", stats)
    write_global("search.js", "INFRA_SEARCH", search)

    print(
        f"wrote {len(features)} projects, {len(corridor_payload)} corridors, "
        f"{len(estate_payload)} estates, {len(sources)} sources"
    )
    print(f"site/data size: {sum(p.stat().st_size for p in SITE_DATA.iterdir()) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
