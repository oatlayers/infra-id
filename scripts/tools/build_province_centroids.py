"""Build province-level centroids for register-only atlas records.

The official PSN register gives a province (or ``Nasional``), not a site
coordinate. Register-only rows therefore use a province centroid and are
excluded from the map. This script records where each centroid comes from:

* the mean of at least two curated atlas points in the province, when available;
* otherwise the bounding-box centre of the province polygon in the bundled
  Natural Earth basemap;
* otherwise the parent region for the five provinces created after the basemap
  was cut (North Kalimantan and the four new Papua provinces);
* otherwise the national centre.

No network request is made. The output is a build input, not a source of
project facts.

Run: python scripts/tools/build_province_centroids.py
Writes: data/derived/province_centroids.json
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import CURATED, DERIVED, read_csv

ROOT = Path(__file__).resolve().parents[2]
BASEMAP = ROOT / "site" / "data" / "basemap.js"

# Natural Earth province names in the bundled basemap -> atlas province names.
BASEMAP_TO_ATLAS = {
    "Aceh": "Aceh",
    "Kalimantan Timur": "East Kalimantan",
    "Jawa Barat": "West Java",
    "Jawa Tengah": "Central Java",
    "Bengkulu": "Bengkulu",
    "Banten": "Banten",
    "Jakarta Raya": "DKI Jakarta",
    "Kalimantan Barat": "West Kalimantan",
    "Lampung": "Lampung",
    "Sumatera Selatan": "South Sumatra",
    "Bangka-Belitung": "Bangka Belitung",
    "Bali": "Bali",
    "Jawa Timur": "East Java",
    "Kalimantan Selatan": "South Kalimantan",
    "Nusa Tenggara Timur": "East Nusa Tenggara",
    "Sulawesi Selatan": "South Sulawesi",
    "Sulawesi Barat": "West Sulawesi",
    "Kepulauan Riau": "Riau Islands",
    "Gorontalo": "Gorontalo",
    "Jambi": "Jambi",
    "Kalimantan Tengah": "Central Kalimantan",
    "Papua Barat": "West Papua",
    "Sumatera Utara": "North Sumatra",
    "Riau": "Riau",
    "Sulawesi Utara": "North Sulawesi",
    "Maluku Utara": "North Maluku",
    "Sumatera Barat": "West Sumatra",
    "Yogyakarta": "DI Yogyakarta",
    "Maluku": "Maluku",
    "Nusa Tenggara Barat": "West Nusa Tenggara",
    "Sulawesi Tenggara": "Southeast Sulawesi",
    "Sulawesi Tengah": "Central Sulawesi",
    "Papua": "Papua",
}

# Provinces created after the basemap edition. Their centroid falls back to the
# parent region unless curated points exist.
PARENT = {
    "North Kalimantan": "East Kalimantan",
    "Southwest Papua": "West Papua",
    "Central Papua": "Papua",
    "South Papua": "Papua",
    "Highland Papua": "Papua",
}

ATLAS_PROVINCES = sorted(
    set(BASEMAP_TO_ATLAS.values())
    | set(PARENT)
    | {"Indonesia", "Eastern Indonesia"}
)


def load_basemap() -> dict:
    text = BASEMAP.read_text(encoding="utf-8")
    match = re.search(r"window\.BASEMAP\s*=\s*(\{.*\});?\s*$", text, re.S)
    if not match:
        raise SystemExit("basemap.js does not contain window.BASEMAP")
    return json.loads(match.group(1))


def collect_points(geometry: dict) -> list[tuple[float, float]]:
    kind = geometry.get("type")
    coords = geometry.get("coordinates") or []
    points: list[tuple[float, float]] = []
    if kind == "Point":
        points.append((float(coords[0]), float(coords[1])))
    elif kind in {"LineString", "MultiPoint"}:
        points.extend((float(pair[0]), float(pair[1])) for pair in coords)
    elif kind in {"Polygon", "MultiLineString"}:
        for ring in coords:
            points.extend((float(pair[0]), float(pair[1])) for pair in ring)
    elif kind == "MultiPolygon":
        for polygon in coords:
            for ring in polygon:
                points.extend((float(pair[0]), float(pair[1])) for pair in ring)
    return points


def bbox_centre(points: list[tuple[float, float]]) -> tuple[float, float]:
    lons = [pair[0] for pair in points]
    lats = [pair[1] for pair in points]
    return ((min(lats) + max(lats)) / 2, (min(lons) + max(lons)) / 2)


def curated_means() -> tuple[dict[str, list[tuple[float, float]]], tuple[float, float] | None]:
    grouped: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for filename in ("projects.csv", "estates.csv"):
        for row in read_csv(CURATED / filename):
            try:
                lat = float(row["lat"])
                lon = float(row["lon"])
            except (TypeError, ValueError):
                continue
            for province in (part.strip() for part in row["province"].split(";")):
                if province:
                    grouped[province].append((lat, lon))
    return grouped, None


def main() -> None:
    basemap = load_basemap()
    curated, _ = curated_means()

    basemap_centres: dict[str, tuple[float, float]] = {}
    for feature in basemap.get("provinces", {}).get("features", []):
        name = feature.get("properties", {}).get("name", "")
        atlas_name = BASEMAP_TO_ATLAS.get(name)
        if not atlas_name:
            continue
        points = collect_points(feature.get("geometry") or {})
        if points:
            basemap_centres[atlas_name] = bbox_centre(points)

    national = None
    for feature in basemap.get("countries", {}).get("features", []):
        if feature.get("properties", {}).get("name") != "Indonesia":
            continue
        points = collect_points(feature.get("geometry") or {})
        if points:
            national = bbox_centre(points)
            break
    if national is None:
        raise SystemExit("Indonesia polygon not found in the basemap")

    out: dict[str, dict[str, object]] = {}
    for province in ATLAS_PROVINCES:
        if province == "Indonesia":
            out[province] = {
                "lat": round(national[0], 5),
                "lon": round(national[1], 5),
                "method": "national bbox centre",
                "source": "Natural Earth Indonesia polygon in site/data/basemap.js",
                "points": 0,
            }
            continue
        if province == "Eastern Indonesia":
            out[province] = {
                "lat": round(national[0], 5),
                "lon": round(national[1], 5),
                "method": "national fallback",
                "source": "Natural Earth Indonesia polygon; register location is a region, not a province",
                "points": 0,
            }
            continue

        points = curated.get(province, [])
        if len(points) >= 2:
            lat = sum(point[0] for point in points) / len(points)
            lon = sum(point[1] for point in points) / len(points)
            out[province] = {
                "lat": round(lat, 5),
                "lon": round(lon, 5),
                "method": "curated mean",
                "source": f"Mean of {len(points)} curated atlas points in {province}",
                "points": len(points),
            }
        elif province in basemap_centres:
            lat, lon = basemap_centres[province]
            out[province] = {
                "lat": round(lat, 5),
                "lon": round(lon, 5),
                "method": "basemap bbox centre",
                "source": "Natural Earth province polygon in site/data/basemap.js",
                "points": len(points),
            }
        elif province in PARENT:
            parent_name = PARENT[province]
            if parent_name in out:
                parent = out[parent_name]
                lat, lon = parent["lat"], parent["lon"]
                method = f"parent fallback ({parent_name})"
                source = parent["source"]
            elif parent_name in basemap_centres:
                lat, lon = basemap_centres[parent_name]
                method = f"parent fallback ({parent_name})"
                source = "Natural Earth parent province polygon in site/data/basemap.js"
            else:
                lat, lon = national
                method = "national fallback"
                source = "Natural Earth Indonesia polygon; parent province not matched"
            out[province] = {
                "lat": round(lat, 5),
                "lon": round(lon, 5),
                "method": method,
                "source": source,
                "points": len(points),
            }
        else:
            out[province] = {
                "lat": round(national[0], 5),
                "lon": round(national[1], 5),
                "method": "national fallback",
                "source": "Natural Earth Indonesia polygon; no province polygon matched",
                "points": len(points),
            }

    DERIVED.mkdir(parents=True, exist_ok=True)
    (DERIVED / "province_centroids.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"OK: {len(out)} province centroids written")
    for key in ("Indonesia", "DKI Jakarta", "West Java", "Papua", "Southwest Papua", "North Kalimantan"):
        if key in out:
            print(f"  {key}: {out[key]['lat']}, {out[key]['lon']} ({out[key]['method']})")


if __name__ == "__main__":
    main()
