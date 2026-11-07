"""Improve coordinates for the largest industrial estates with OpenStreetMap.

The 2024 Kemenperin-derived table only gives regency centroids for industrial
estates. This script queries Nominatim (one request per second) for the 40
largest industrial-only estates, accepts a result only when it is tagged as an
industrial landuse and matches the estate name and regency/province, and stores
every response in a cache.

SEZ and shared SEZ/estate rows keep their official KEK coordinates. Estates
without a reliable match keep the regency centroid.

Attribution: OpenStreetMap contributors, ODbL 1.0.

Run: python scripts/geocode_estates.py
Writes: data/derived/nominatim_estates.json
Updates: data/curated/estates.csv, data/curated/sources.csv,
         data/curated/estate_sources.csv
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from data_model import (
    CURATED,
    DERIVED,
    ESTATE_FIELDS,
    ESTATE_SOURCE_FIELDS,
    SOURCE_FIELDS,
    read_csv,
    write_csv,
)

CACHE = DERIVED / "nominatim_estates.json"
SOURCE_ID = "src-osm-nominatim-2026-11-08"
CHECK_DATE = "2026-11-08"
TOP_N = 40
USER_AGENT = "infra-id-atlas/0.1 (local research; contact: repository owner)"

STOP = {
    "kawasan", "industri", "industrial", "estate", "park", "city", "town",
    "terpadu", "kota", "kabupaten", "the", "and", "of", "pt", "tbk", "ie",
    "ki", "kawasan", "indonesia",
}


def tokens(value: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", value.lower())
    return [word for word in words if len(word) >= 4 and word not in STOP]


def search(query: str, limit: int = 5) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "format": "jsonv2",
            "limit": limit,
            "countrycodes": "id",
            "addressdetails": 1,
            "accept-language": "en",
        }
    )
    request = urllib.request.Request(
        "https://nominatim.openstreetmap.org/search?" + params,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def acceptable(estate: dict, results: list[dict]) -> dict | None:
    name_tokens = tokens(estate["name"])
    place_tokens = tokens(estate["regency"]) + tokens(estate["province"])
    digits = re.findall(r"\d+", estate["name"])
    for result in results:
        if result.get("type") != "industrial":
            continue
        display = (result.get("display_name") or "").lower()
        if not any(token in display for token in name_tokens):
            continue
        if not any(token in display for token in place_tokens):
            continue
        # A numbered estate (GIIC 2, Puri Industrial Park 2000) must match its
        # number; otherwise the search can silently return the first estate.
        if any(number not in display for number in digits):
            continue
        return result
    return None


def main() -> None:
    estates = read_csv(CURATED / "estates.csv")
    sources = read_csv(CURATED / "sources.csv")
    claims = read_csv(CURATED / "estate_sources.csv")

    industrial = [
        row for row in estates
        if row["type"] == "industrial_estate" and row["area_ha"]
    ]
    industrial.sort(key=lambda row: float(row["area_ha"]), reverse=True)
    targets = industrial[:TOP_N]

    cache: dict[str, dict] = {}
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))

    matched = 0
    for index, estate in enumerate(targets, start=1):
        name = estate["name"]
        regency = estate["regency"]
        province = estate["province"]
        base = name.split("(")[0].strip()
        short = re.sub(r"\s+(MMID|IE|SPIKE|BCIP|KIMONG)$", "", base, flags=re.I).strip()
        if short.lower().startswith("suryacipta"):
            short = "Kawasan Industri " + short
        queries = list(
            dict.fromkeys(
                [
                    f"{name}, {regency}, {province}, Indonesia",
                    f"{base}, {regency}, Indonesia",
                    f"{short}, {regency}, Indonesia",
                ]
            )
        )
        entry = cache.get(estate["id"])
        if entry and entry.get("accepted") is None:
            # Retry misses so improved query variants can find them.
            entry = None
        if entry and entry.get("accepted"):
            cached_results = [
                result
                for query in entry.get("queries", [])
                for result in query.get("results", [])
            ]
            if acceptable(estate, cached_results) is None:
                entry = None
        if not entry or entry.get("check_date") != CHECK_DATE:
            entry = {"check_date": CHECK_DATE, "queries": []}
            for query in queries:
                try:
                    results = search(query)
                except Exception as error:  # keep the batch going
                    print(f"  ! {name}: {query}: {error}")
                    results = []
                entry["queries"].append({"query": query, "results": results})
                accepted = acceptable(estate, results)
                if accepted:
                    entry["accepted"] = accepted
                    break
                time.sleep(1.2)
            cache[estate["id"]] = entry
            CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            time.sleep(1.2)

        accepted = entry.get("accepted")
        if not accepted:
            print(f"{index:2}/{len(targets)}  no match  {name}")
            continue

        matched += 1
        estate["lat"] = f"{float(accepted['lat']):.5f}"
        estate["lon"] = f"{float(accepted['lon']):.5f}"
        estate["precision"] = "approximate"
        estate["coordinate_source"] = "osm"
        estate["notes"] = estate["notes"].replace(
            "Coordinates are the regency/city centroid; refine with the estate boundary.", ""
        ).strip()
        note = "Coordinates from OpenStreetMap/Nominatim (ODbL), approximate."
        if note not in estate["notes"]:
            estate["notes"] = (estate["notes"] + " " + note).strip()
        print(f"{index:2}/{len(targets)}  matched    {name}  -> {estate['lat']}, {estate['lon']}")

    if SOURCE_ID not in {row["id"] for row in sources}:
        sources.append(
            {
                "id": SOURCE_ID,
                "publisher": "OpenStreetMap contributors",
                "title": "Nominatim search results for industrial estates",
                "url": "https://nominatim.openstreetmap.org/",
                "published_on": "",
                "retrieved_on": CHECK_DATE,
                "source_type": "secondary",
                "language": "en",
                "snapshot_hash": "",
                "accessed_via": "Nominatim API, one request per second",
                "archive_path": str(CACHE.relative_to(CURATED.parents[1])).replace("\\", "/"),
                "licence": "ODbL 1.0",
                "notes": "Point coordinates for the 40 largest industrial estates. Attribution required.",
            }
        )

    target_ids = {row["id"] for row in targets}
    claims = [row for row in claims if row["source_id"] != SOURCE_ID or row["estate_id"] not in target_ids]
    for estate in targets:
        if estate["coordinate_source"] != "osm":
            continue
        claims.append(
            {
                "estate_id": estate["id"],
                "source_id": SOURCE_ID,
                "claim": "coordinates",
                "claim_value": f"{estate['lat']}, {estate['lon']}",
                "claim_date": CHECK_DATE,
                "notes": "Industrial landuse point from OpenStreetMap/Nominatim; approximate.",
            }
        )

    write_csv(CURATED / "estates.csv", ESTATE_FIELDS, estates)
    write_csv(CURATED / "sources.csv", SOURCE_FIELDS, sources)
    write_csv(CURATED / "estate_sources.csv", ESTATE_SOURCE_FIELDS, claims)

    print(f"\nmatched {matched} of {len(targets)} target estates; cache {CACHE.relative_to(CURATED.parents[1])}")


if __name__ == "__main__":
    main()
