"""Parse the toll-road table from the English Wikipedia article.

Input : data/raw/2026-11-06/wikipedia_indonesian_toll_road_system.html
Output: data/raw/2026-11-06/enwiki_toll_roads_parsed.csv

This only extracts what the article says. It does not decide status or curate rows.
"""

from __future__ import annotations

import csv
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "2026-11-06"
SRC = RAW / "wikipedia_indonesian_toll_road_system.html"
OUT = RAW / "enwiki_toll_roads_parsed.csv"


def main() -> None:
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "lxml")

    table = None
    for candidate in soup.find_all("table"):
        heads = [th.get_text(" ", strip=True) for th in candidate.find_all("th")]
        if "Toll Road name" in heads:
            table = candidate
            break
    if table is None:
        raise SystemExit("Toll-road table not found")

    rows: list[dict[str, object]] = []
    island = ""
    province = ""

    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        texts = [c.get_text(" ", strip=True) for c in cells]
        if texts[0] == "Island" or len(cells) < 3:
            continue

        if cells[0].get("rowspan"):
            island = texts[0].split("\n")[0].strip()
        if len(cells) >= 4 and cells[1].get("rowspan"):
            province = texts[1].strip()

        # 5 cells = island + province; 4 = province; 3 = neither.
        name_i = 2 if len(cells) == 5 else 1 if len(cells) == 4 else 0
        name_cell = cells[name_i]
        name = name_cell.get_text(" ", strip=True)
        if not name:
            continue

        length = texts[name_i + 1] if len(texts) > name_i + 1 else ""
        operator = texts[name_i + 2] if len(texts) > name_i + 2 else ""
        haystack = f"{name} {length}".lower()

        rows.append(
            {
                "island": island,
                "province": province,
                "name": name,
                "length_raw": length,
                "operator": operator,
                "italic": name_cell.find("i") is not None,
                "under_construction": "under construction" in haystack,
                "in_preparation": "preparation" in haystack,
            }
        )

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
