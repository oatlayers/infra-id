"""Build the 179-vs-160 industrial-estate reconciliation ledger.

Kemenperin reports 179 industrial estates in 2026. The 2024 BAJRA mirror carried
160 industrial-estate designations, a difference of 19. This ledger records what
happened to those 19 names.

By 9 November 2026 the atlas had 179 pure industrial-estate rows plus 7 shared
SEZ/estate rows, so the 179 target is met by count. The count was closed mainly
through the 18 register-only PSN industrial areas, not by finding every 2025
name. Two of the original 19 names are now resolved (IPIP and Pulau Penebang).
Seven named 2025 additions remain open. The ten unnamed rows are retained for
audit but marked as no longer required for the count.

The Kemenperin site returned HTTP 502 and satudata.kemenperin.go.id did not
resolve on 8 November 2026. The 179 count is sourced to ANTARA's report of the
Kemenperin briefing on 29 June 2026; the directory was reachable on 9 November
2026 and is filed as data/raw/2026-11-09/kemenperin_kawasan.html.

Run: python scripts/imports/extract_estate_gap.py
Writes: data/derived/estate_gap_2026.csv
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "derived" / "estate_gap_2026.csv"

FIELDS = ["name", "province", "regency", "disposition", "source_id", "notes"]

SOURCE_ID = "src-antara-kemenperin-179-2026"
COUNT_NOTE = (
    "Kemenperin reports 179 industrial estates in 2026 (ANTARA, 29 June 2026); "
    "the 2024 BAJRA mirror carried 160 industrial-estate designations. The atlas "
    "now has 179 pure industrial-estate rows plus 7 shared SEZ/estate rows, so "
    "the count target is met. This ledger is retained for name-level audit."
)

RESOLVED = [
    (
        "IPIP (Indonesia Pomalaa Industry Park)",
        "Southeast Sulawesi",
        "Kolaka",
        "resolved",
        "Resolved as ki-indonesia-pomalaa-industry-park. The Kemenperin directory "
        "lists 686.00 ha in Kabupaten Kolaka, Sulawesi Tenggara; the earlier "
        "Central Sulawesi location in the 2024 gap note was a directory conflict.",
    ),
    (
        "Pulau Penebang",
        "West Kalimantan",
        "Kayong Utara",
        "resolved",
        "Resolved as ki-kawasan-industri-pulau-penebang. The Kemenperin directory "
        "lists 1,476.30 ha in Kabupaten Kayong Utara, Kalimantan Barat; the earlier "
        "Riau Islands/Bintan location in the 2024 gap note was wrong.",
    ),
]

NAMED = [
    (
        "I-Sentra Lamongan",
        "East Java",
        "Lamongan",
        "unresolved-no-source",
        "Named as a 2025 addition in the v3 research backlog. No reachable "
        "official page, area figure or coordinate on 8 November 2026.",
    ),
    (
        "Huadi Bantaeng",
        "South Sulawesi",
        "Bantaeng",
        "unresolved-no-source",
        "Named as a 2025 addition. PT Huadi Nickel-Alloy Indonesia operates in "
        "Bantaeng, but no reachable estate page gives an area or boundary.",
    ),
    (
        "Cikembar II",
        "West Java",
        "Sukabumi",
        "unresolved-no-source",
        "Cikembar I is already in the table (220 ha). Cikembar II is a separate "
        "2025 designation; no reachable area or coordinate source.",
    ),
    (
        "Losarang",
        "West Java",
        "Indramayu",
        "unresolved-no-source",
        "Named as a 2025 addition. No reachable official page or area figure.",
    ),
    (
        "Purwakarta Integrated Industrial Park",
        "West Java",
        "Purwakarta",
        "unresolved-no-source",
        "Named as a 2025 addition. Purwakarta already has several estates in the "
        "table (Jatiluhur, Kota Bukit Indah, Cikaopark, Lion, SKI), but this "
        "specific park has no reachable area or coordinate source.",
    ),
    (
        "Seafer",
        "Riau Islands",
        "Batam",
        "unresolved-no-source",
        "Named as a 2025 addition. No reachable developer page or area figure.",
    ),
    (
        "Tembesi",
        "Riau Islands",
        "Batam",
        "unresolved-location-conflict",
        "Kemenperin is reported to list Tembesi under West Kalimantan, but the "
        "well-known Tembesi industrial area is in Batam. No reachable area or "
        "boundary source.",
    ),
]

UNIDENTIFIED = [
    (
        f"Unidentified 2025 addition {index}",
        "",
        "",
        "not-required-for-count",
        "The 179 count is now met by the 179 pure industrial-estate rows plus 7 "
        "shared SEZ/estate rows. This name remains unidentified but is no longer a "
        "count gap; it is retained so the original 19-row reconciliation is auditable.",
    )
    for index in range(1, 11)
]


def main() -> None:
    rows = [
        {
            "name": name,
            "province": province,
            "regency": regency,
            "disposition": disposition,
            "source_id": SOURCE_ID,
            "notes": f"{COUNT_NOTE} {notes}",
        }
        for name, province, regency, disposition, notes in RESOLVED + NAMED + UNIDENTIFIED
    ]
    if len(rows) != 19:
        raise SystemExit(f"expected 19 gap rows, got {len(rows)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} gap rows to {OUT.relative_to(ROOT)}")
    print(
        "resolved:", len(RESOLVED), "named open:", len(NAMED),
        "not required for count:", len(UNIDENTIFIED),
    )


if __name__ == "__main__":
    main()
