"""Add the two-year delivery-report indicators and the 2026 energy targets.

Sources:

* Sekretariat Kabinet, 20 October 2026, *Seskab Teddy Bagikan Sekilas Cuplikan
  Hasil Nyata 2 Tahun Pemerintahan*. Headline delivery figures for education,
  health, housing, irrigation, bridges, Inpres roads, boreholes, fishing
  villages and downstreaming.
* Kementerian Pendidikan Dasar dan Menengah, 27 October 2026, *Dua Tahun
  Pemerintahan Prabowo-Gibran, Kemendikdasmen Perluas Akses dan Perkuat Mutu
  Pendidikan*. Education delivery detail and the 2027 SNT target.
* Kementerian Sekretariat Negara, 14 August 2026, 2027 budget speech. The
  2026 solar and diesel targets, the per-Puskesmas budget, the 7,280-kecamatan
  coverage target and the three-screens-per-school target.

The script also removes the unsupported 2030 completion date from
``ind-pkpn-health-rsud``: the speech's 2030 deadline applies to the Puskesmas
and Labkesmas renovation, not to the 441 RSUD.

Indicators are national programme measures, not project facts. Values are
recorded exactly as stated; "more than 9,000 km" is stored as 9,000 and marked
as a lower bound. No target is invented where the source is silent.

The script is idempotent: existing indicator ids are never replaced and
existing values are never duplicated.

Run: python scripts/imports/add_two_year_indicators.py
Then: python scripts/pipeline/validate.py
      python scripts/pipeline/build_i18n.py
      python scripts/build_all.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CURATED,
    INDICATOR_FIELDS,
    INDICATOR_VALUE_FIELDS,
    SOURCE_FIELDS,
    read_csv,
    write_csv,
)

RAW = Path(__file__).resolve().parents[2] / "data" / "raw" / "2026-11-09"
REVIEWED = "2026-11-09"

SOURCE_SETKAB = "src-setkab-two-year-report-2026-10-20"
SOURCE_KEMDIKDASMEN = "src-kemendikdasmen-two-year-2026-10-27"
SOURCE_SPEECH = "src-setneg-rapbn-2027-2026-08-14"

NEW_SOURCES = [
    {
        "id": SOURCE_SETKAB,
        "publisher": "Sekretariat Kabinet Republik Indonesia",
        "title": "Seskab Teddy Bagikan Sekilas Cuplikan Hasil Nyata 2 Tahun Pemerintahan",
        "url": "https://setkab.go.id/seskab-teddy-bagikan-sekilas-cuplikan-hasil-nyata-2-tahun-pemerintahan/",
        "published_on": "2026-10-20",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "archive_path": "data/raw/2026-11-09/setkab_two_year_report_2026-10-20.html",
        "notes": (
            "Two-year delivery report: 265 Sekolah Rakyat, 30,000 renovated "
            "schools, 288,180 interactive screens, 400,000 repaired houses, 22 "
            "new hospitals, 100 fishing villages, more than 9,000 km of "
            "irrigation, 3,500 bridges, 2,228 km of Inpres roads, 3,000 "
            "boreholes and 26 downstreaming groundbreakings."
        ),
    },
    {
        "id": SOURCE_KEMDIKDASMEN,
        "publisher": "Kementerian Pendidikan Dasar dan Menengah",
        "title": (
            "Dua Tahun Pemerintahan Prabowo-Gibran, Kemendikdasmen Perluas "
            "Akses dan Perkuat Mutu Pendidikan"
        ),
        "url": (
            "https://www.kemendikdasmen.go.id/siaran-pers/16362-dua-tahun-"
            "pemerintahan-prabowogibran-kemendikdasmen-perluas-akses-dan-"
            "perkuat-mutu-pendidikan"
        ),
        "published_on": "2026-10-27",
        "retrieved_on": REVIEWED,
        "source_type": "official",
        "language": "id",
        "archive_path": "data/raw/2026-11-09/kemendikdasmen_two_year_2026-10-27.html",
        "notes": (
            "55,451 schools reached in 2025-2026; 39,284 against a 31,744 "
            "target in 2026; 72,258 of 742,536 planned interactive panels; "
            "2,389 schools with electricity, 8,152 with internet; 17 SNT "
            "operating and 100 schools planned for 2027."
        ),
    },
]

# id, programme, name_en, name_id, unit, direction, target, target_date,
# source, notes
NEW_INDICATORS = [
    (
        "ind-pkpn-education-sekolah-rakyat", "pkpn-education",
        "Sekolah Rakyat built", "Sekolah Rakyat terbangun",
        "schools", "increase", "", "", SOURCE_SETKAB,
        "265 Sekolah Rakyat had opened by 20 October 2026. The release says "
        "43,000 street children returned to school; no target is stated.",
    ),
    (
        "ind-pkpn-education-schools-renovated", "pkpn-education",
        "Schools renovated", "Sekolah direnovasi",
        "schools", "increase", "", "", SOURCE_SETKAB,
        "Two-year figure of 30,000 renovated schools. Kemendikdasmen reports "
        "55,451 schools reached by revitalisation and construction in "
        "2025-2026, a broader definition.",
    ),
    (
        "ind-pkpn-education-screens", "pkpn-education",
        "Interactive screens distributed", "Layar interaktif terdistribusi",
        "screens", "increase", "", "", SOURCE_SETKAB,
        "288,180 interactive screens distributed in the first two years. "
        "Kemendikdasmen separately reports 288,865 schools receiving "
        "interactive panels in 2025, a different unit.",
    ),
    (
        "ind-pkpn-education-schools-electricity", "pkpn-education",
        "Schools given electricity access", "Sekolah mendapat akses listrik",
        "schools", "increase", "", "", SOURCE_KEMDIKDASMEN,
        "Reported with the 2026 digitalisation figures; the release does not "
        "give a separate year.",
    ),
    (
        "ind-pkpn-education-schools-internet", "pkpn-education",
        "Schools given internet access", "Sekolah mendapat akses internet",
        "schools", "increase", "", "", SOURCE_KEMDIKDASMEN,
        "Reported with the 2026 digitalisation figures; the release does not "
        "give a separate year.",
    ),
    (
        "ind-pkpn-education-snt", "pkpn-education",
        "Sekolah Nasional Terintegrasi operating",
        "Sekolah Nasional Terintegrasi beroperasi",
        "schools", "increase", "", "", SOURCE_KEMDIKDASMEN,
        "17 SNT operating in the 2026/2027 school year, with 1,360 new pupils "
        "in 13 provinces.",
    ),
    (
        "ind-pkpn-education-snt-2027", "pkpn-education",
        "SNT schools to be built in 2027", "Sekolah SNT dibangun pada 2027",
        "schools", "target", "100", "2027-12-31", SOURCE_KEMDIKDASMEN,
        "Construction continues in 2027 with 100 schools after 20 further "
        "kabupaten/kota enter the plan. The date uses the year-end convention; "
        "the release gives only the year.",
    ),
    (
        "ind-pkpn-education-screens-per-school", "pkpn-education",
        "Additional screens per school", "Tambahan layar per sekolah",
        "screens per school", "target", "3", "2026-12-31", SOURCE_SPEECH,
        "Every school is to receive an additional three screens by "
        "end-December 2026. The speech states no total number of screens.",
    ),
    (
        "ind-pkpn-health-new-hospitals", "pkpn-health",
        "New hospitals operational", "Rumah sakit baru beroperasi",
        "hospitals", "increase", "", "", SOURCE_SETKAB,
        "22 new hospitals reported in the first two years. The 2027 budget "
        "speech says 66 hospitals were built in disadvantaged, frontier and "
        "outermost regions and 22 were operational.",
    ),
    (
        "ind-pkpn-health-puskesmas-budget", "pkpn-health",
        "Renovation budget per Puskesmas", "Anggaran renovasi per Puskesmas",
        "Rp B per facility", "target", "4", "2030-12-31", SOURCE_SPEECH,
        "About Rp4B per Puskesmas. The 2030 date is the completion deadline "
        "for the Puskesmas and Labkesmas renovation programme.",
    ),
    (
        "ind-pkpn-health-kecamatan", "pkpn-health",
        "Kecamatan covered by Puskesmas renovation",
        "Kecamatan terjangkau renovasi Puskesmas",
        "kecamatan", "target", "7280", "2030-12-31", SOURCE_SPEECH,
        "The speech says 10,000 Puskesmas across 7,280 kecamatan will be "
        "renovated by 2030.",
    ),
    (
        "ind-pkpn-housing-repaired", "pkpn-infrastructure",
        "Houses repaired", "Rumah diperbaiki",
        "houses", "increase", "", "", SOURCE_SETKAB,
        "400,000 houses repaired in the first two years. The release states "
        "no target.",
    ),
    (
        "ind-pkpn-infrastructure-irrigation", "pkpn-infrastructure",
        "Irrigation built", "Irigasi terbangun",
        "km", "increase", "", "", SOURCE_SETKAB,
        "More than 9,000 km of irrigation; the value is a lower bound.",
    ),
    (
        "ind-pkpn-infrastructure-bridges", "pkpn-infrastructure",
        "Bridges built", "Jembatan terbangun",
        "bridges", "increase", "", "", SOURCE_SETKAB,
        "3,500 bridges reported in the first two years.",
    ),
    (
        "ind-pkpn-infrastructure-inpres-roads", "pkpn-infrastructure",
        "Inpres roads built", "Jalan Inpres terbangun",
        "km", "increase", "", "", SOURCE_SETKAB,
        "2,228 km of Inpres roads reported in the first two years.",
    ),
    (
        "ind-pkpn-energy-water-boreholes", "pkpn-energy-water",
        "Borehole water points built", "Titik air bor terbangun",
        "points", "increase", "", "", SOURCE_SETKAB,
        "3,000 new borehole water points reported in the first two years.",
    ),
    (
        "ind-pkpn-food-fishing-villages", "pkpn-food",
        "Kampung Nelayan Merah Putih developed",
        "Kampung Nelayan Merah Putih terbangun",
        "villages", "increase", "", "", SOURCE_SETKAB,
        "100 fishing villages developed in the first two years. The plan's "
        "1,386-village pipeline target is not stated in this release.",
    ),
    (
        "ind-pkpn-downstreaming-groundbreakings", "pkpn-downstreaming",
        "Downstreaming groundbreakings", "Peletakan batu pertama hilirisasi",
        "projects", "increase", "", "", SOURCE_SETKAB,
        "26 downstreaming projects broke ground in the first two years, "
        "including the electric-vehicle battery project described as the "
        "largest in Southeast Asia.",
    ),
    (
        "ind-pkpn-energy-solar-2026", "pkpn-energy-water",
        "Solar capacity built in 2026", "Kapasitas surya terbangun pada 2026",
        "GW", "increase", "30", "2026-12-31", SOURCE_SPEECH,
        "The speech says 30 GW of solar will be built in 2026. The 100 GW "
        "programme target is separate; 5.3 GWp had been launched by 25 August "
        "2026.",
    ),
    (
        "ind-pkpn-energy-diesel-retired", "pkpn-energy-water",
        "Diesel capacity retired in 2026",
        "Kapasitas diesel dipensiunkan pada 2026",
        "GW", "increase", "13", "2026-12-31", SOURCE_SPEECH,
        "The speech says 13 GW of diesel generation will be retired as 30 GW "
        "of solar is built in 2026.",
    ),
    (
        "ind-pkpn-energy-solar-savings", "pkpn-energy-water",
        "Annual generation-cost saving at 100 GW",
        "Penghematan biaya pembangkitan per tahun pada 100 GW",
        "Rp T", "target", "73.9", "", SOURCE_SPEECH,
        "At least Rp73.9T per year from lower generation cost at 100 GW. The "
        "speech gives no date for the full saving.",
    ),
]

# indicator_id, value, as_of, source, notes
NEW_VALUES = [
    ("ind-pkpn-education-sekolah-rakyat", "265", "2026-10-20", SOURCE_SETKAB,
     "265 Sekolah Rakyat opened by 20 October 2026."),
    ("ind-pkpn-education-schools-renovated", "30000", "2026-10-20", SOURCE_SETKAB,
     "30,000 schools renovated in the first two years."),
    ("ind-pkpn-education-screens", "288180", "2026-10-20", SOURCE_SETKAB,
     "288,180 interactive screens distributed in the first two years."),
    ("ind-pkpn-education-schools-electricity", "2389", "2026-10-27", SOURCE_KEMDIKDASMEN,
     "2,389 schools given electricity access; the release does not state a "
     "separate year."),
    ("ind-pkpn-education-schools-internet", "8152", "2026-10-27", SOURCE_KEMDIKDASMEN,
     "8,152 schools given internet access; the release does not state a "
     "separate year."),
    ("ind-pkpn-education-snt", "17", "2026-10-27", SOURCE_KEMDIKDASMEN,
     "17 SNT operating in the 2026/2027 school year."),
    ("ind-pkpn-health-new-hospitals", "22", "2026-10-20", SOURCE_SETKAB,
     "22 new hospitals reported in the first two years."),
    ("ind-pkpn-housing-repaired", "400000", "2026-10-20", SOURCE_SETKAB,
     "400,000 houses repaired in the first two years."),
    ("ind-pkpn-infrastructure-irrigation", "9000", "2026-10-20", SOURCE_SETKAB,
     "More than 9,000 km; recorded as a lower bound."),
    ("ind-pkpn-infrastructure-bridges", "3500", "2026-10-20", SOURCE_SETKAB,
     "3,500 bridges reported in the first two years."),
    ("ind-pkpn-infrastructure-inpres-roads", "2228", "2026-10-20", SOURCE_SETKAB,
     "2,228 km of Inpres roads reported in the first two years."),
    ("ind-pkpn-energy-water-boreholes", "3000", "2026-10-20", SOURCE_SETKAB,
     "3,000 new borehole water points reported in the first two years."),
    ("ind-pkpn-food-fishing-villages", "100", "2026-10-20", SOURCE_SETKAB,
     "100 fishing villages developed in the first two years."),
    ("ind-pkpn-downstreaming-groundbreakings", "26", "2026-10-20", SOURCE_SETKAB,
     "26 downstreaming projects broke ground in the first two years."),
]


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def update_manifest() -> None:
    path = RAW / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for name in (
        "setkab_two_year_report_2026-10-20.html",
        "kemendikdasmen_two_year_2026-10-27.html",
    ):
        file_path = RAW / name
        urls = {
            "setkab_two_year_report_2026-10-20.html":
                "https://setkab.go.id/seskab-teddy-bagikan-sekilas-cuplikan-hasil-nyata-2-tahun-pemerintahan/",
            "kemendikdasmen_two_year_2026-10-27.html":
                "https://www.kemendikdasmen.go.id/siaran-pers/16362-dua-tahun-pemerintahan-prabowogibran-kemendikdasmen-perluas-akses-dan-perkuat-mutu-pendidikan",
        }
        manifest[name] = {
            "url": urls[name],
            "bytes": file_path.stat().st_size,
            "sha256": hash_file(file_path),
        }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    sources = read_csv(CURATED / "sources.csv")
    existing_sources = {row["id"] for row in sources}
    added_sources = 0
    for row in NEW_SOURCES:
        if row["id"] in existing_sources:
            continue
        row = dict(row)
        row["snapshot_hash"] = hash_file(RAW / Path(row["archive_path"]).name)
        row["accessed_via"] = row["url"].split("/")[2]
        row["licence"] = ""
        sources.append(row)
        existing_sources.add(row["id"])
        added_sources += 1
    sources.sort(key=lambda row: row["id"])
    write_csv(CURATED / "sources.csv", SOURCE_FIELDS, sources)

    indicators = read_csv(CURATED / "indicators.csv")
    existing_indicators = {row["id"]: row for row in indicators}
    added_indicators = 0
    for (
        indicator_id, programme_id, name_en, name_id, unit, direction,
        target_value, target_date, source_id, notes,
    ) in NEW_INDICATORS:
        if indicator_id in existing_indicators:
            continue
        indicators.append(
            {
                "id": indicator_id,
                "programme_id": programme_id,
                "project_id": "",
                "name_en": name_en,
                "name_id": name_id,
                "unit": unit,
                "direction": direction,
                "baseline_value": "",
                "baseline_date": "",
                "target_value": target_value,
                "target_date": target_date,
                "source_id": source_id,
                "notes": notes,
            }
        )
        added_indicators += 1

    # The speech's 2030 deadline applies to Puskesmas and Labkesmas only.
    rsud = existing_indicators.get("ind-pkpn-health-rsud")
    if rsud is not None:
        rsud["target_date"] = ""
        rsud["notes"] = (
            "441 regional public hospitals. The 2027 budget speech gives no "
            "completion year; the 2030 deadline in the same passage applies to "
            "the Puskesmas and Labkesmas renovation."
        )

    indicators.sort(key=lambda row: row["id"])
    write_csv(CURATED / "indicators.csv", INDICATOR_FIELDS, indicators)

    values = read_csv(CURATED / "indicator_values.csv")
    existing_keys = {
        (row["indicator_id"], row["as_of"], row["source_id"]) for row in values
    }
    added_values = 0
    for indicator_id, value, as_of, source_id, notes in NEW_VALUES:
        key = (indicator_id, as_of, source_id)
        if key in existing_keys:
            continue
        values.append(
            {
                "indicator_id": indicator_id,
                "value": value,
                "as_of": as_of,
                "source_id": source_id,
                "notes": notes,
            }
        )
        existing_keys.add(key)
        added_values += 1
    values.sort(key=lambda row: (row["indicator_id"], row["as_of"], row["source_id"]))
    write_csv(CURATED / "indicator_values.csv", INDICATOR_VALUE_FIELDS, values)

    update_manifest()

    print(
        f"OK: {added_indicators} indicators, {added_values} values, "
        f"{added_sources} sources; RSUD target date cleared"
    )


if __name__ == "__main__":
    main()
