"""Build data/curated/estates.csv from the KEK profiles and the estate table.

Sources:
  * 25 official KEK profile pages (data/raw/2026-11-06/kek_*.html), parsed directly.
  * The 2024 Kemenperin-derived industrial estate table (BAJRA mirror).

Coordinates:
  * SEZs: official zone point from the KEK profile.
  * Industrial estates: regency/city centroid from data/derived/regency_coords.json,
    precision=regency. Refine major estates later.

Run: python scripts/imports/build_estates.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import csv
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

from data_model import ESTATE_FIELDS, SOURCE_FIELDS, island_for

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "2026-11-06"
CURATED = ROOT / "data" / "curated"
DERIVED = ROOT / "data" / "derived"

SEZ_LOCATION = {
    "batam-tourism-and-international-healthcare": ("Kepulauan Riau", "Kota Batam"),
    "bumi-serpong-damai": ("Banten", "Kabupaten Tangerang"),
    "industropolis-batang": ("Jawa Tengah", "Kabupaten Batang"),
    "kek-arun-lhokseumawe": ("Aceh", "Kota Lhokseumawe"),
    "kek-batam-aero-technic": ("Kepulauan Riau", "Kota Batam"),
    "kek-bitung": ("Sulawesi Utara", "Kota Bitung"),
    "kek-galang-batang": ("Kepulauan Riau", "Kabupaten Bintan"),
    "kek-gresik": ("Jawa Timur", "Kabupaten Gresik"),
    "kek-kendal": ("Jawa Tengah", "Kabupaten Kendal"),
    "kek-kura-kura": ("Bali", "Kota Denpasar"),
    "kek-lido": ("Jawa Barat", "Kabupaten Bogor"),
    "kek-likupang": ("Sulawesi Utara", "Kabupaten Minahasa Utara"),
    "kek-maloy-batuta": ("Kalimantan Timur", "Kabupaten Kutai Timur"),
    "kek-mandalika": ("Nusa Tenggara Barat", "Kabupaten Lombok Tengah"),
    "kek-morotai": ("Maluku Utara", "Kabupaten Pulau Morotai"),
    "kek-nongsa": ("Kepulauan Riau", "Kota Batam"),
    "kek-palu": ("Sulawesi Tengah", "Kota Palu"),
    "kek-sanur": ("Bali", "Kota Denpasar"),
    "kek-sei-mangkei": ("Sumatera Utara", "Kabupaten Simalungun"),
    "kek-singhasari": ("Jawa Timur", "Kabupaten Malang"),
    "kek-sorong": ("Papua Barat Daya", "Kabupaten Sorong"),
    "kek-tanjung-kelayang": ("Kepulauan Bangka Belitung", "Kabupaten Belitung"),
    "kek-tanjung-lesung": ("Banten", "Kabupaten Pandeglang"),
    "setangga": ("Kalimantan Selatan", "Kabupaten Tanah Bumbu"),
    "tanjung-sauh": ("Kepulauan Riau", "Kota Batam"),
}

# SEZ slug -> exact industrial-estate name in the 2024 table. Those rows are
# merged into the SEZ record as type=both instead of being duplicated.
SEZ_INDUSTRIAL_OVERLAP = {
    "kek-galang-batang": "KEK Galang Batang",
    "kek-kendal": "Kawasan Industri Kendal",
    "kek-gresik": "Kawasan Industri Gresik",
    "kek-sei-mangkei": "Kawasan Industri Sei Mangkei (KEK)",
    "kek-palu": "Kawasan Industri Palu",
    "tanjung-sauh": "Kawasan Industri Tanjung Sauh",
    "industropolis-batang": "Kawasan Industri Terpadu Batang",
}

PROVINCE_FIX = {
    "Nangroe Aceh Darussalam": "Aceh",
    "Nanggroe Aceh Darussalam": "Aceh",
}
REGENCY_FIX = {
    "Kabupaten SIAK": "Kabupaten Siak",
    "Kabupaten Kota Baru": "Kabupaten Kotabaru",
}


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def parse_area(raw: str) -> float:
    text = raw.strip().lower()
    factor = 1.0
    if "m2" in text or "m²" in text:
        factor = 0.0001
    text = text.replace("ha", "").replace("m²", "").replace("m2", "").strip()
    text = text.replace(" ", "")
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    elif text.count(".") == 1 and len(text.split(".")[1]) == 3:
        text = text.replace(".", "")
    return round(float(text) * factor, 2)


def parse_year(raw: str) -> str:
    matches = re.findall(r"\b((?:19|20)\d{2})\b", raw)
    return matches[-1] if matches else ""


def fmt_num(value: float) -> str:
    return str(int(value)) if value.is_integer() else f"{value:g}"


def load_estate_table() -> list[dict[str, str]]:
    soup = BeautifulSoup((RAW / "bajra_kawasan_industri.html").read_text(encoding="utf-8"), "lxml")
    table = None
    for candidate in soup.find_all("table"):
        heads = [th.get_text(" ", strip=True) for th in candidate.find_all("th")]
        if "Nama Kawasan" in heads:
            table = candidate
            break
    if table is None:
        raise SystemExit("industrial estate table not found")
    rows: list[dict[str, str]] = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cells) < 5:
            continue
        location = cells[3]
        parts = [part.strip() for part in location.split(",", 1)]
        rows.append(
            {
                "developer": cells[1],
                "name": cells[2],
                "regency": REGENCY_FIX.get(parts[0], parts[0]),
                "province": PROVINCE_FIX.get(parts[1] if len(parts) > 1 else "", parts[1] if len(parts) > 1 else ""),
                "area": cells[4],
            }
        )
    return rows


def load_sez_details() -> list[dict[str, object]]:
    slugs = [
        line.strip()
        for line in (RAW / "kek_slugs.txt").read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    details: list[dict[str, object]] = []
    for slug in slugs:
        soup = BeautifulSoup((RAW / f"kek_{slug}.html").read_text(encoding="utf-8"), "lxml")
        tag = soup.find("script", id="__NEXT_DATA__")
        if tag is None:
            raise SystemExit(f"{slug}: __NEXT_DATA__ not found")
        data = json.loads(tag.string)
        queries = data["props"]["pageProps"]["initialState"]["sez-regions"]["queries"]
        record = None
        for key, value in queries.items():
            if key.startswith("getDetailSezRegions"):
                record = value.get("data", {}).get("data")
        if not record:
            raise SystemExit(f"{slug}: SEZ detail not found")
        details.append(
            {
                "slug": slug,
                "title": record["title"],
                "latitude": record["latitude"],
                "longitude": record["longitude"],
                "category": record["category"],
                "developer": record["developer"],
                "area": record["area"],
                "legalBasis": record["legalBasis"],
            }
        )
    return details


def main() -> None:
    details = load_sez_details()
    coords = json.loads((DERIVED / "regency_coords.json").read_text(encoding="utf-8"))
    industrial = load_estate_table()

    estates: list[dict[str, str]] = []
    new_sources: list[dict[str, str]] = []

    # --- SEZs -------------------------------------------------------------
    for detail in details:
        slug = detail["slug"]
        province, regency = SEZ_LOCATION[slug]
        area = parse_area(detail["area"])
        title = detail["title"]
        name = title if title.upper().startswith("KEK") else f"KEK {title}"
        overlap = SEZ_INDUSTRIAL_OVERLAP.get(slug)
        notes = "Designated SEZ. Operational maturity varies and is not independently verified."
        if overlap:
            notes += " Also listed as an industrial estate in the 2024 Kemenperin-derived table."

        source_id = f"src-kek-{slug.removeprefix('kek-')}-2026-11-06"
        estates.append(
            {
                "id": f"sez-{slug.removeprefix('kek-')}",
                "name": name,
                "type": "both" if overlap else "sez",
                "province": province,
                "regency": regency,
                "island": island_for(province),
                "lat": f"{detail['latitude']:.5f}",
                "lon": f"{detail['longitude']:.5f}",
                "precision": "approximate",
                "coordinate_source": "official",
                "area_ha": fmt_num(area),
                "developer": detail["developer"],
                "developer_org_id": "",
                "status": "operating",
                "sector_focus": detail["category"],
                "legal_basis": detail["legalBasis"],
                "established_year": parse_year(detail["legalBasis"]),
                "website": "",
                "occupancy_pct": "",
                "kemenperin_id": "",
                "sez_id": slug,
                "source_id": source_id,
                "last_verified": "2026-11-06",
                "notes": notes,
            }
        )
        new_sources.append(
            {
                "id": source_id,
                "publisher": "Sekretariat Dewan Nasional Kawasan Ekonomi Khusus",
                "title": f"{name} profile",
                "url": f"https://kek.go.id/id/investment/distribution/{slug}",
                "published_on": "",
                "retrieved_on": "2026-11-06",
                "source_type": "official",
                "language": "id",
                "snapshot_hash": "",
                "accessed_via": "",
                "archive_path": f"data/raw/2026-11-06/kek_{slug}.html",
                "licence": "Government public data; check portal terms",
                "notes": "Area, developer, legal basis and coordinates parsed from the page payload.",
            }
        )

    # --- Industrial estates ----------------------------------------------
    seen_names: set[str] = set()
    used_ids: set[str] = set()
    skipped = 0
    duplicates = 0
    for row in industrial:
        if row["name"] in SEZ_INDUSTRIAL_OVERLAP.values():
            skipped += 1
            continue
        duplicate = row["name"] in seen_names
        seen_names.add(row["name"])
        key = f'{row["regency"]}, {row["province"]}'
        coord = coords.get(key)
        if not coord or coord.get("lat") is None:
            raise SystemExit(f"no coordinates for {key} ({row['name']})")
        base_id = f'ki-{slugify(row["name"])}'
        estate_id = base_id
        suffix = 2
        while estate_id in used_ids:
            estate_id = f"{base_id}-{suffix}"
            suffix += 1
        used_ids.add(estate_id)
        note = "Listed in the 2024 Kemenperin-derived industrial estate table. Coordinates are the regency/city centroid; refine with the estate boundary."
        if duplicate:
            duplicates += 1
            note += " Duplicate name in the source table; this may be a separate plot."
        estates.append(
            {
                "id": estate_id,
                "name": row["name"],
                "type": "industrial_estate",
                "province": row["province"],
                "regency": row["regency"],
                "island": island_for(row["province"]),
                "lat": f'{coord["lat"]:.5f}',
                "lon": f'{coord["lon"]:.5f}',
                "precision": "regency",
                "coordinate_source": "regency",
                "area_ha": fmt_num(parse_area(row["area"])),
                "developer": row["developer"],
                "developer_org_id": "",
                "status": "operating",
                "sector_focus": "",
                "legal_basis": "",
                "established_year": "",
                "website": "",
                "occupancy_pct": "",
                "kemenperin_id": "",
                "sez_id": "",
                "source_id": "src-bajra-kawasan-industri-2024",
                "last_verified": "2026-11-06",
                "notes": note,
            }
        )

    new_sources.append(
        {
            "id": "src-bajra-kawasan-industri-2024",
            "publisher": "BAJRA (reproducing Kemenperin data)",
            "title": "Daftar Kawasan Industri Indonesia",
            "url": "https://www.bajra.id/2024/08/daftar-kawasan-industri-indonesia.html",
            "published_on": "2024-08-17",
            "retrieved_on": "2026-11-06",
            "source_type": "secondary",
            "language": "id",
            "snapshot_hash": "",
            "accessed_via": "",
            "archive_path": "data/raw/2026-11-06/bajra_kawasan_industri.html",
            "licence": "Article; data attributed to Kemenperin",
            "notes": "159 estates. Kemenperin reported 179 estates in 2026, so this is a partial snapshot.",
        }
    )

    # --- Write ------------------------------------------------------------
    estates.sort(key=lambda row: (row["type"] != "sez", row["name"].lower()))
    with (CURATED / "estates.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=ESTATE_FIELDS)
        writer.writeheader()
        writer.writerows(estates)

    sources_path = CURATED / "sources.csv"
    with sources_path.open(encoding="utf-8", newline="") as fh:
        sources = list(csv.DictReader(fh))
    existing = {row["id"] for row in sources}
    added = 0
    for source in new_sources:
        if source["id"] not in existing:
            sources.append(source)
            existing.add(source["id"])
            added += 1
    with sources_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=SOURCE_FIELDS)
        writer.writeheader()
        writer.writerows(sources)

    print(f"wrote {len(estates)} estates ({sum(1 for e in estates if e['type'] != 'industrial_estate')} SEZ/both)")
    print(f"skipped {skipped} industrial rows already represented as SEZs; kept {duplicates} duplicate-name rows")
    print(f"sources: {added} added, {len(sources)} total")


if __name__ == "__main__":
    main()
