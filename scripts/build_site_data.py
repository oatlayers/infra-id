"""Build the site data files from data/projects.csv.

Outputs:
  site/data/projects.geojson  standard GeoJSON FeatureCollection
  site/data/projects.js       same collection as window.PROJECTS (works from file://)
  site/data/projects.csv      downloadable copy

Run: python scripts/build_site_data.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "projects.csv"
OUT_DIR = ROOT / "site" / "data"

FIELDS = [
    "id",
    "name",
    "sector",
    "status",
    "status_basis",
    "province",
    "route",
    "length_km",
    "operator",
    "opened_year",
    "lat",
    "lon",
    "precision",
    "source_url",
    "source_type",
    "retrieved_on",
    "last_verified",
    "notes",
]


def main() -> None:
    with CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    features = []
    for row in rows:
        properties = {field: row[field] for field in FIELDS if field not in {"lat", "lon"}}
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

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "projects.geojson").write_text(
        json.dumps(collection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "projects.js").write_text(
        "window.PROJECTS = " + json.dumps(collection, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    # Downloadable copy of the curated table.
    with (OUT_DIR / "projects.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(features)} features to {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
