"""Build the bundled vector basemap from Natural Earth.

Inputs : data/raw/2026-11-06/ne_50m_*.geojson
Outputs: site/data/basemap.geojson
         site/data/basemap.js   (window.BASEMAP, works from file://)

Layers: countries, Indonesian provinces, lakes, rivers, urban areas and city
labels. Natural Earth is public domain. Geometry is clipped to the map region
and simplified so the whole payload stays small enough to ship offline.

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

LABEL_COUNTRIES = {
    "Indonesia", "Malaysia", "Singapore", "Brunei", "East Timor",
    "Timor-Leste", "Papua New Guinea", "Philippines",
}


def round_coords(value: object) -> object:
    if isinstance(value, float):
        return round(value, 4)
    if isinstance(value, list):
        return [round_coords(item) for item in value]
    if isinstance(value, dict):
        return {key: round_coords(item) for key, item in value.items()}
    return value


def load(name: str) -> dict:
    return json.loads((RAW / name).read_text(encoding="utf-8"))


def clip_features(
    source: dict,
    *,
    tolerance: float,
    properties,
    predicate=None,
) -> list[dict]:
    features = []
    for feature in source["features"]:
        if predicate and not predicate(feature):
            continue
        geometry = shape(feature["geometry"])
        if geometry.is_empty or not geometry.intersects(REGION):
            continue
        clipped = geometry.intersection(REGION).simplify(tolerance, preserve_topology=True)
        if clipped.is_empty:
            continue
        features.append(
            {
                "type": "Feature",
                "properties": properties(feature),
                "geometry": round_coords(mapping(clipped)),
            }
        )
    return features


def main() -> None:
    countries_src = load("ne_50m_admin_0_countries.geojson")
    country_features = []
    for feature in countries_src["features"]:
        props = feature["properties"]
        iso = props.get("ADM0_A3") or ""
        name = COUNTRY_NAMES.get(iso, props.get("NAME") or iso)
        if not name:
            continue
        geometry = shape(feature["geometry"])
        if not geometry.intersects(REGION):
            continue
        clipped = geometry.intersection(REGION).simplify(0.005, preserve_topology=True)
        if clipped.is_empty:
            continue
        country_features.append(
            {
                "type": "Feature",
                "properties": {"name": name},
                "geometry": round_coords(mapping(clipped)),
            }
        )
    countries = {
        "type": "FeatureCollection",
        # Draw Indonesia last so its outline sits above enclaves.
        "features": sorted(
            country_features, key=lambda f: f["properties"]["name"] == "Indonesia"
        ),
    }

    provinces_src = load("ne_50m_admin_1_states_provinces.geojson")
    provinces = {
        "type": "FeatureCollection",
        "features": clip_features(
            provinces_src,
            tolerance=0.008,
            predicate=lambda f: f["properties"].get("admin") == "Indonesia",
            properties=lambda f: {
                "name": f["properties"].get("name") or "",
                "iso": f["properties"].get("iso_3166_2") or "",
            },
        ),
    }

    lakes_src = load("ne_50m_lakes.geojson")
    lakes = {
        "type": "FeatureCollection",
        "features": clip_features(
            lakes_src,
            tolerance=0.005,
            properties=lambda f: {
                "name": f["properties"].get("name") or "",
                "rank": f["properties"].get("scalerank") or 9,
            },
        ),
    }

    rivers_src = load("ne_50m_rivers_lake_centerlines.geojson")
    rivers = {
        "type": "FeatureCollection",
        "features": clip_features(
            rivers_src,
            tolerance=0.008,
            properties=lambda f: {
                "name": f["properties"].get("name") or "",
                "rank": f["properties"].get("scalerank") or 9,
            },
        ),
    }

    urban_src = load("ne_50m_urban_areas.geojson")
    urban = {
        "type": "FeatureCollection",
        "features": clip_features(
            urban_src,
            tolerance=0.01,
            properties=lambda f: {
                "area_sqkm": round(f["properties"].get("area_sqkm") or 0, 1)
            },
        ),
    }

    places_src = load("ne_50m_populated_places.geojson")
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
                "population": population,
                "lat": round(lat, 4),
                "lon": round(lon, 4),
            }
        )
    places.sort(key=lambda place: (-place["population"], place["name"]))

    basemap = {
        "countries": countries,
        "provinces": provinces,
        "lakes": lakes,
        "rivers": rivers,
        "urban": urban,
        "places": places,
        "meta": {
            "source": "Natural Earth 1:50m, public domain",
            "region": [92.0, -14.0, 144.0, 9.0],
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = json.dumps(basemap, ensure_ascii=False, separators=(",", ":"))
    (OUT_DIR / "basemap.geojson").write_text(text + "\n", encoding="utf-8")
    (OUT_DIR / "basemap.js").write_text("window.BASEMAP = " + text + ";\n", encoding="utf-8")

    print(
        "countries: {countries}, provinces: {provinces}, lakes: {lakes}, "
        "rivers: {rivers}, urban: {urban}, places: {places}".format(
            countries=len(countries["features"]),
            provinces=len(provinces["features"]),
            lakes=len(lakes["features"]),
            rivers=len(rivers["features"]),
            urban=len(urban["features"]),
            places=len(places),
        )
    )
    print(f"basemap.js: {(OUT_DIR / 'basemap.js').stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
