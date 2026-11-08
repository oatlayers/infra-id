"""Build the 179-vs-160 industrial-estate reconciliation ledger.

Kemenperin reports 179 industrial estates in 2026. The curated table carries 160
industrial-estate designations from a 2024 BAJRA mirror. The difference is 19.
Nine names are documented in the v3 research backlog; the other ten are not
named in any source that was reachable on 8 November 2026. This ledger records
that honestly instead of inventing rows.

The Kemenperin site returned HTTP 502 and satudata.kemenperin.go.id did not
resolve on 8 November 2026. The 179 count is sourced to ANTARA's report of the
Kemenperin briefing on 29 June 2026.

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
    "the curated table has 160 industrial-estate designations from the 2024 "
    "BAJRA mirror. Kemenperin's own list was unreachable on 8 November 2026 "
    "(HTTP 502 and DNS failure)."
)

NAMED = [
    (
        "IPIP (Indonesia Pomalaa Industry Park)",
        "Central Sulawesi",
        "",
        "unresolved-location-conflict",
        "Kemenperin lists IPIP under Central Sulawesi, but PT Indonesia Pomalaa "
        "Industry Park's project is at Pomalaa, Kolaka, Southeast Sulawesi. The "
        "official careers site confirms the company name but gives no area or "
        "estate boundary. Not added without an area and a location source.",
    ),
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
        "Pulau Penebang",
        "Riau Islands",
        "Bintan",
        "unresolved-no-source",
        "Named as a 2025 addition. The island location is known, but no reachable "
        "developer page gives an area or estate boundary.",
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
        "unresolved-not-named",
        "The 179 count exceeds the 160-row table by 19. Nine additions are named; "
        "this one is not named in any source reachable on 8 November 2026.",
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
        for name, province, regency, disposition, notes in NAMED + UNIDENTIFIED
    ]
    if len(rows) != 19:
        raise SystemExit(f"expected 19 gap rows, got {len(rows)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} gap rows to {OUT.relative_to(ROOT)}")
    print("named:", len(NAMED), "unidentified:", len(UNIDENTIFIED))


if __name__ == "__main__":
    main()
