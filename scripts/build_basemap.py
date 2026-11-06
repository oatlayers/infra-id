"""Build the bundled vector basemap from Natural Earth.

Input : data/raw/2026-11-06/ne_50m_admin_0_countries.geojson
        data/raw/2026-11-06/ne_50m_populated_places.geojson
Output: site/data/basemap.geojson
        site/data/basemap.js   (window.BASEMAP, works from file://)

Natural Earth is public domain. The geometry is clipped to the map region and
simplified so the file stays small enough to ship with the page.

Run: python scripts/build_basemap.py
"""

from __future__ import annotations

import json
from pathlib import Path

from shapely.geometry import box, mapping, shape

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "2026-11-06"
OUT_DIR = ROOT / "site" / "data"

# A little wider than Indonesia so neighbouring coasts give context.
REGION = box(92.0, -14.0, 144.0, 9.0)
TOLERANCE = 0.005  # degrees, roughly 500 m

COUNTRY_NAMES = {
    "IDN": "Indonesia",
    "MYS": "Malaysia",
    "SGP": "Singapore",
    "BRN": "Brunei",
    "TLS": "Timor-Leste",
    "PNG": "Papua New Guinea",
    "PHL": "Philippines",
    "AUS": "Australia",
    "THA": "Thailand",
    "VNM": "Vietnam",
    "KHM": "Cambodia",
    "MMR": "Myanmar",
    "IND": "India",
    "PLW": "Palau",
}

LABEL_COUNTRIES = {"Indonesia", "Malaysia", "Singapore", "Brunei", "East Timor",
                   "Timor-Leste", "Papua New Guinea", "Philippines"}


def round_coords(value: object) -> object:
    if isinstance(value, float):
        return round(value, 4)
    if isinstance(value, list):
        return [round_coords(item) for item in value]
    if isinstance(value, dict):
        return {key: round_coords(item) for key, item in value.items()}
    return value


def main() -> None:
    countries_src = json.loads(
        (RAW / "ne_50m_admin_0_countries.geojson").read_text(encoding="utf-8")
    )
    features = []
    for feature in countries_src["features"]:
        props = feature["properties"]
        iso = props.get("ADM0_A3") or ""
        geometry = shape(feature["geometry"])
        if not geometry.intersects(REGION):
            continue
        clipped = geometry.intersection(REGION).simplify(TOLERANCE, preserve_topology=True)
        if clipped.is_empty:
            continue
        features.append(
            {
                "type": "Feature",
                "properties": {"name": COUNTRY_NAMES.get(iso, props.get("NAME") or iso)},
                "geometry": round_coords(mapping(clipped)),
            }
        )

    countries = {
        "type": "FeatureCollection",
        # Draw Indonesia last so its outline sits above enclaves.
        "features": sorted(features, key=lambda f: f["properties"]["name"] == "Indonesia"),
    }

    places_src = json.loads(
        (RAW / "ne_50m_populated_places.geojson").read_text(encoding="utf-8")
    )
    places = []
    for feature in places_src["features"]:
        props = feature["properties"]
        country = props.get("ADM0NAME")
        if country not in LABEL_COUNTRIES:
            continue
        population = props.get("POP_MAX") or 0
        if not (props.get("ADM0CAP") == 1 or population >= 1_000_000):
            continue
        lon, lat = feature["geometry"]["coordinates"][:2]
        if not (REGION.bounds[0] <= lon <= REGION.bounds[2]):
            continue
        if not (REGION.bounds[1] <= lat <= REGION.bounds[3]):
            continue
        places.append(
            {
                "name": props.get("NAME"),
                "country": country,
                "capital": props.get("ADM0CAP") == 1,
                "lat": round(lat, 4),
                "lon": round(lon, 4),
            }
        )

    basemap = {"countries": countries, "places": places}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = json.dumps(basemap, ensure_ascii=False, separators=(",", ":"))
    (OUT_DIR / "basemap.geojson").write_text(text + "\n", encoding="utf-8")
    (OUT_DIR / "basemap.js").write_text("window.BASEMAP = " + text + ";\n", encoding="utf-8")

    print(f"countries: {len(countries['features'])}, places: {len(places)}")
    print(f"basemap.js: {(OUT_DIR / 'basemap.js').stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
