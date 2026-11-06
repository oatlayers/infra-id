"""Build the browser payload from the flat project export and corridors.

Outputs:
  site/data/projects.geojson  standard GeoJSON FeatureCollection
  site/data/projects.js       same collection as window.PROJECTS (works from file://)
  site/data/projects.csv      downloadable copy
  site/data/corridors.json    Trans corridor summary
  site/data/corridors.js      same summary as window.CORRIDORS

Run: python scripts/build_site_data.py
"""

from __future__ import annotations

import json

from data_model import (
    CORRIDOR_FIELDS,
    CURATED,
    DERIVED_FIELDS,
    ROOT,
    SITE_DATA,
    read_csv,
    write_csv,
)

PROJECTS_CSV = ROOT / "data" / "projects.csv"


def main() -> None:
    rows = read_csv(PROJECTS_CSV)
    sources = {row["id"]: row for row in read_csv(CURATED / "sources.csv")}

    features = []
    for row in rows:
        properties = {field: row[field] for field in DERIVED_FIELDS if field not in {"lat", "lon"}}
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

    corridors = []
    for row in read_csv(CURATED / "corridors.csv"):
        source = sources.get(row["source_id"])
        corridors.append(
            {
                **{field: row[field] for field in CORRIDOR_FIELDS if field != "source_id"},
                "source_url": source["url"] if source else "",
                "source_type": source["source_type"] if source else "",
                "retrieved_on": source["retrieved_on"] if source else "",
            }
        )

    SITE_DATA.mkdir(parents=True, exist_ok=True)
    (SITE_DATA / "projects.geojson").write_text(
        json.dumps(collection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (SITE_DATA / "projects.js").write_text(
        "window.PROJECTS = " + json.dumps(collection, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    (SITE_DATA / "corridors.json").write_text(
        json.dumps(corridors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (SITE_DATA / "corridors.js").write_text(
        "window.CORRIDORS = " + json.dumps(corridors, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    write_csv(SITE_DATA / "projects.csv", DERIVED_FIELDS, rows)

    print(f"wrote {len(features)} features and {len(corridors)} corridors to {SITE_DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
