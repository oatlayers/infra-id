"""Cache Nominatim responses used to check factory coordinates.

This script does not change any curated row. It records what the geocoder
returned so the coordinate claims in the factory batch can be audited. The
curated points are approximate plant or industrial-park locations; a result is
not a survey boundary.

Attribution: OpenStreetMap contributors, ODbL 1.0.

Run: python scripts/geocode_factories.py
Writes: data/derived/nominatim_factories.json
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

from data_model import DERIVED

CACHE = DERIVED / "nominatim_factories.json"
USER_AGENT = "infra-id-atlas/0.1 (local research; contact: repository owner)"

QUERIES = [
    "Java Integrated Industrial and Port Estate Gresik",
    "PT Smelting Gresik",
    "Benete Sumbawa Barat",
    "Indonesia Morowali Industrial Park",
    "IMIP Morowali",
    "Dexin Steel Morowali",
    "Weda Bay Industrial Park",
    "Lelilef Sawai",
    "Tanjung Kawasi",
    "Morosi Konawe",
    "Pajukukang Bantaeng",
    "Pomalaa Kolaka",
    "Bahodopi Morowali",
    "Sorowako",
    "Kendawangan Ketapang",
    "Well Harvest Winning Kendawangan",
    "SGAR Mempawah",
    "Sungai Kunyit Mempawah",
    "Kuala Tanjung Batu Bara",
    "Inalum Kuala Tanjung",
    "Krakatau Steel Cilegon",
    "Gunung Raja Paksi",
    "Kendal Industrial Park",
    "Karawang New Industry City",
    "Lotte Chemical Cilegon",
    "Chandra Asri Cilegon",
    "OKI Pulp Ogan Komering Ilir",
    "Air Sugihan",
    "Pupuk Kaltim Bontang",
    "Bunta Morowali Utara",
    "Gunbuster Nickel",
    "Bantaeng Industrial Park",
]


def search(query: str) -> list[dict[str, str]]:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "format": "jsonv2",
            "limit": 3,
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
        results = json.load(response)
    return [
        {
            "name": item.get("name", ""),
            "display": item.get("display_name", ""),
            "lat": item.get("lat", ""),
            "lon": item.get("lon", ""),
            "type": item.get("type", ""),
        }
        for item in results
    ]


def main() -> None:
    cache: dict[str, object] = {}
    for query in QUERIES:
        try:
            cache[query] = search(query)
        except Exception as error:  # keep going when one query fails
            cache[query] = {"error": str(error)}
        time.sleep(1)

    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(cache)} queries -> data/derived/nominatim_factories.json")


if __name__ == "__main__":
    main()
