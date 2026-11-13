"""Build the locale payloads and the translation coverage report.

Sources:

* ``data/i18n/ui.en.json`` and ``ui.id.json`` — the UI string catalogues. The
  build fails unless both files carry exactly the same non-empty keys.
* ``data/curated/translations.csv`` — reviewed entity text.
* Bilingual curated fields — programmes already carry ``name_id``/``name_en``
  and summaries; project aliases carry official Indonesian names; corridor
  definitions come from the curated table plus translations.csv.

Outputs:

* ``site/data/i18n.en.js`` and ``site/data/i18n.id.js`` — classic scripts so
  ``file://`` works without fetch.
* ``data/derived/i18n_report.csv`` — one row per required entity field with its
  state: ``translated``, ``official``, ``fallback`` or ``missing``.

Run: python scripts/pipeline/build_i18n.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (
    CURATED,
    DERIVED,
    ROOT,
    SITE_DATA,
    read_csv,
)

I18N = ROOT / "data" / "i18n"
LOCALES = ("en", "id")
REQUIRED = {
    "programme": ("name", "summary"),
    "corridor": ("name", "definition"),
    "project": ("name",),
}
FIELD_SOURCE = {
    ("programme", "name"): ("name_id", "name_en"),
    ("programme", "summary"): ("summary_id", "summary_en"),
    ("programme", "target_summary"): ("target_summary_id", "target_summary_en"),
    ("corridor", "name"): ("name", "name"),
    ("corridor", "definition"): ("definition", "definition"),
}

PROVINCES_ID = {
    "Aceh": "Aceh", "North Sumatra": "Sumatera Utara", "West Sumatra": "Sumatera Barat",
    "Riau": "Riau", "Riau Islands": "Kepulauan Riau", "Jambi": "Jambi",
    "Bengkulu": "Bengkulu", "South Sumatra": "Sumatera Selatan", "Lampung": "Lampung",
    "Bangka Belitung": "Kepulauan Bangka Belitung", "Banten": "Banten",
    "DKI Jakarta": "DKI Jakarta", "West Java": "Jawa Barat",
    "Central Java": "Jawa Tengah", "DI Yogyakarta": "DI Yogyakarta",
    "East Java": "Jawa Timur", "Bali": "Bali",
    "West Nusa Tenggara": "Nusa Tenggara Barat",
    "East Nusa Tenggara": "Nusa Tenggara Timur",
    "West Kalimantan": "Kalimantan Barat", "Central Kalimantan": "Kalimantan Tengah",
    "South Kalimantan": "Kalimantan Selatan", "East Kalimantan": "Kalimantan Timur",
    "North Kalimantan": "Kalimantan Utara", "North Sulawesi": "Sulawesi Utara",
    "Gorontalo": "Gorontalo", "Central Sulawesi": "Sulawesi Tengah",
    "West Sulawesi": "Sulawesi Barat", "South Sulawesi": "Sulawesi Selatan",
    "Southeast Sulawesi": "Sulawesi Tenggara", "Maluku": "Maluku",
    "North Maluku": "Maluku Utara", "Papua": "Papua", "West Papua": "Papua Barat",
    "Southwest Papua": "Papua Barat Daya", "Central Papua": "Papua Tengah",
    "South Papua": "Papua Selatan", "Highland Papua": "Papua Pegunungan",
    "Indonesia": "Indonesia", "Eastern Indonesia": "Indonesia Timur",
}

STATUS_EN = {
    "under_construction": "under construction", "planned": "planned",
    "operating": "operating", "recently_completed": "recently completed",
    "stalled": "stalled", "unknown": "status not sourced",
}
STATUS_ID = {
    "under_construction": "dalam konstruksi", "planned": "direncanakan",
    "operating": "beroperasi", "recently_completed": "baru selesai",
    "stalled": "terhenti", "unknown": "status belum bersumber",
}
SECTOR_EN = {
    "road": "road", "railway": "railway", "airport": "airport",
    "seaport": "seaport", "factory": "industrial plant", "energy": "energy project",
    "water": "water project", "urban": "urban project", "coastal": "coastal project",
    "housing": "housing project", "technology": "technology project",
    "education": "education project", "tourism": "tourism project",
    "agriculture": "agriculture project",
}
SECTOR_ID = {
    "road": "jalan", "railway": "kereta api", "airport": "bandar udara",
    "seaport": "pelabuhan", "factory": "pabrik industri", "energy": "proyek energi",
    "water": "proyek air", "urban": "proyek perkotaan", "coastal": "proyek pesisir",
    "housing": "proyek perumahan", "technology": "proyek teknologi",
    "education": "proyek pendidikan", "tourism": "proyek pariwisata",
    "agriculture": "proyek pertanian",
}


MONTHS_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
    "Agustus", "September", "Oktober", "November", "Desember",
]
MONTHS_EN = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]
UNIT_ID = {
    "million m3": "juta m³",
    "ktpa copper cathode": "ktpa katoda tembaga",
    "ktpa stainless steel": "ktpa baja nirkarat",
    "ktpa ethylene": "ktpa etilena",
    "ktpa concentrate": "ktpa konsentrat",
    "ktpa crude steel": "ktpa baja mentah",
    "ktpa Ni in MHP": "ktpa Ni dalam MHP",
    "ktpa Ni in ferronickel": "ktpa Ni dalam feronikel",
    "ktpa Ni+Co in MHP": "ktpa Ni+Co dalam MHP",
    "ktpa Ni in NPI": "ktpa Ni dalam NPI",
    "ktpa steel slab": "ktpa slab baja",
    "ktpa steel": "ktpa baja",
    "ktpa anode material": "ktpa bahan anoda",
    "GWh/y cells": "GWh/tahun sel",
    "m runway": "m landasan pacu",
    "kbd crude": "kbd minyak mentah",
    "MWp launched": "MWp terpasang",
}


def number(value: str, locale: str = "en") -> str:
    try:
        number_value = float(value)
    except (TypeError, ValueError):
        return ""
    text = f"{number_value:,.1f}".rstrip("0").rstrip(".")
    if locale == "id":
        text = text.replace(",", "\u0000").replace(".", ",").replace("\u0000", ".")
    return text


def investment_text(value: str, locale: str = "en") -> str:
    """Render a trillion-rupiah value, switching to billions when small."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return ""
    if amount and amount < 0.1:
        amount_text = number(str(amount * 1000), locale)
        return (
            f"Rp {amount_text} billion" if locale == "en"
            else f"Rp {amount_text} miliar"
        )
    amount_text = number(value, locale)
    return (
        f"Rp {amount_text} trillion" if locale == "en"
        else f"Rp {amount_text} triliun"
    )


def display_date(value: str, locale: str) -> str:
    try:
        year, month, day = (int(part) for part in value.split("-"))
    except (TypeError, ValueError):
        return value
    months = MONTHS_ID if locale == "id" else MONTHS_EN
    if not 1 <= month <= 12:
        return value
    return f"{day} {months[month - 1]} {year}"


def cap_first(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def province_text(value: str, locale: str) -> str:
    parts = [part.strip() for part in value.split(";") if part.strip()]
    if locale == "id":
        parts = [PROVINCES_ID.get(part, part) for part in parts]
    if not parts:
        return "Indonesia"
    if len(parts) == 1:
        return parts[0]
    separator = ", "
    return separator.join(parts[:-1]) + (" and " if locale == "en" else " dan ") + parts[-1]


def generated_summary(project: dict[str, str], locale: str) -> str:
    if project["verification"] == "unverified" and project["status"] == "unknown":
        match = re.search(r"Register-only PSN (\d+)", project["notes"])
        number_text = match.group(1) if match else "?"
        if locale == "id":
            return (
                f"Tercantum sebagai PSN {number_text} dalam register resmi. "
                "Lampiran menyatakan nama, sektor, dan lokasi; status implementasi, "
                "biaya, kapasitas, dan jadwal belum bersumber."
            )
        return (
            f"Listed as PSN {number_text} in the official register. The annex states "
            "the name, sector and location; implementation status, cost, capacity and "
            "schedule are not yet sourced."
        )

    status = (STATUS_ID if locale == "id" else STATUS_EN).get(
        project["status"], project["status"]
    )
    if locale == "en" and status == "under construction":
        status = "under-construction"
    sector = (SECTOR_ID if locale == "id" else SECTOR_EN).get(
        project["sector"], project["sector"]
    )
    province = province_text(project["province"], locale)
    facts: list[str] = []
    if project["length_km"]:
        facts.append(
            f"{number(project['length_km'], locale)} km total" if locale == "en"
            else f"total {number(project['length_km'], locale)} km"
        )
    if project["operational_km"]:
        facts.append(
            f"{number(project['operational_km'], locale)} km operational" if locale == "en"
            else f"{number(project['operational_km'], locale)} km operasional"
        )
    if project["construction_km"]:
        facts.append(
            f"{number(project['construction_km'], locale)} km under construction" if locale == "en"
            else f"{number(project['construction_km'], locale)} km dalam konstruksi"
        )
    if project["investment_idr_t"]:
        facts.append(
            f"{investment_text(project['investment_idr_t'], locale)} investment" if locale == "en"
            else f"investasi {investment_text(project['investment_idr_t'], locale)}"
        )
    if project["capacity"]:
        unit = project["capacity_unit"]
        if locale == "id":
            unit = UNIT_ID.get(unit, unit)
        facts.append(
            f"capacity {number(project['capacity'], locale)} {unit}".strip() if locale == "en"
            else f"kapasitas {number(project['capacity'], locale)} {unit}".strip()
        )
    if project["opened_year"]:
        facts.append(
            f"opened {project['opened_year']}" if locale == "en"
            else f"dibuka {project['opened_year']}"
        )
    elif project["expected_open_year"]:
        facts.append(f"target {project['expected_open_year']}")

    if locale == "id":
        sentence = f"{sector.capitalize()} {status} di {province}."
    else:
        sentence = f"{status.capitalize()} {sector} in {province}."
    if facts:
        facts[0] = cap_first(facts[0])
        sentence += " " + ", ".join(facts) + "."
    if project["psn"] == "yes":
        sentence += " Proyek Strategis Nasional." if locale == "id" else " National Strategic Project."
    if project["last_verified"]:
        verified = display_date(project["last_verified"], locale)
        sentence += (
            f" Terakhir diverifikasi {verified}." if locale == "id"
            else f" Last verified {verified}."
        )
    return sentence


def load_catalogue(locale: str) -> dict[str, str]:
    path = I18N / f"ui.{locale}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def check_catalogues(en: dict[str, str], id_: dict[str, str]) -> None:
    problems: list[str] = []
    missing_id = sorted(set(en) - set(id_))
    missing_en = sorted(set(id_) - set(en))
    if missing_id:
        problems.append(f"ui.id.json is missing {len(missing_id)} keys: {missing_id[:8]}")
    if missing_en:
        problems.append(f"ui.en.json is missing {len(missing_en)} keys: {missing_en[:8]}")
    for locale, catalogue in (("en", en), ("id", id_)):
        blank = sorted(key for key, value in catalogue.items() if not str(value).strip())
        if blank:
            problems.append(f"ui.{locale}.json has blank values: {blank[:8]}")
    if problems:
        raise SystemExit("i18n catalogue error:\n - " + "\n - ".join(problems))


def official_alias_names() -> dict[str, tuple[str, str]]:
    names: dict[str, tuple[str, str]] = {}
    for row in read_csv(CURATED / "project_aliases.csv"):
        if not row["notes"].startswith("Official Indonesian name"):
            continue
        names.setdefault(row["project_id"], (row["alias"], row["source_id"]))
    return names


def add_field(
    report: list[dict[str, str]],
    entities: dict[str, dict[str, str]],
    *,
    entity_type: str,
    entity_id: str,
    field: str,
    locale: str,
    value: str,
    state: str,
    note: str = "",
) -> None:
    entities.setdefault(f"{entity_type}:{entity_id}", {})[field] = value
    report.append(
        {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "field": field,
            "locale": locale,
            "state": state,
            "note": note,
        }
    )


def main() -> None:
    en = load_catalogue("en")
    id_ = load_catalogue("id")
    check_catalogues(en, id_)

    projects = read_csv(CURATED / "projects.csv")
    programmes = read_csv(CURATED / "programmes.csv")
    corridors = read_csv(CURATED / "corridors.csv")
    estates = read_csv(CURATED / "estates.csv")
    translations = read_csv(CURATED / "translations.csv")
    aliases = official_alias_names()

    translation_map: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in translations:
        key = (row["entity_type"], row["entity_id"], row["field"], row["locale"])
        translation_map[key] = row

    # Programme and corridor fields already exist in the curated tables.
    bilingual: dict[str, dict[str, dict[str, tuple[str, str, str]]]] = {
        "programme": {},
        "corridor": {},
    }
    for programme in programmes:
        bilingual["programme"][programme["id"]] = {
            "name": (
                programme["name_en"],
                programme["name_id"],
                programme["source_id"],
            ),
            "summary": (
                programme["summary_en"],
                programme["summary_id"],
                programme["source_id"],
            ),
            "target_summary": (
                programme["target_summary_en"],
                programme["target_summary_id"],
                programme["source_id"],
            ),
        }
    for corridor in corridors:
        bilingual["corridor"][corridor["id"]] = {
            "name": (corridor["name"], corridor["name"], corridor["source_id"]),
            "definition": (
                corridor["definition"],
                "",
                corridor["source_id"],
            ),
        }

    errors: list[str] = []
    report: list[dict[str, str]] = []
    payloads: dict[str, dict[str, object]] = {}
    coverage: dict[str, dict[str, object]] = {}

    for locale in LOCALES:
        messages = en if locale == "en" else id_
        entities: dict[str, dict[str, str]] = {}
        counts: Counter[str] = Counter()
        warnings: list[str] = []

        # Programmes: required name and summary in both locales.
        for programme in programmes:
            fields = bilingual["programme"][programme["id"]]
            for field in ("name", "summary"):
                en_value, id_value, source_id = fields[field]
                value = en_value if locale == "en" else id_value
                if not value:
                    errors.append(
                        f"programme {programme['id']}: missing {field}_{locale}"
                    )
                    continue
                state = "translated" if locale == "id" else "source"
                add_field(
                    report, entities,
                    entity_type="programme", entity_id=programme["id"],
                    field=field, locale=locale, value=value, state=state,
                    note=source_id,
                )
                counts["programme_" + state] += 1
            # Target summaries are optional.
            target = fields["target_summary"][0 if locale == "en" else 1]
            if target:
                add_field(
                    report, entities,
                    entity_type="programme", entity_id=programme["id"],
                    field="target_summary", locale=locale, value=target,
                    state="translated" if locale == "id" else "source",
                )
            else:
                report.append(
                    {
                        "entity_type": "programme", "entity_id": programme["id"],
                        "field": "target_summary", "locale": locale,
                        "state": "not_published", "note": "No target in the annex.",
                    }
                )

        # Corridors: name is a proper name; definition must be translated.
        for corridor in corridors:
            fields = bilingual["corridor"][corridor["id"]]
            name = fields["name"][0 if locale == "en" else 1]
            add_field(
                report, entities,
                entity_type="corridor", entity_id=corridor["id"],
                field="name", locale=locale, value=name, state="source",
            )
            defined = fields["definition"][0 if locale == "en" else 1]
            translation = translation_map.get(
                ("corridor", corridor["id"], "definition", locale)
            )
            if translation and translation["text"]:
                add_field(
                    report, entities,
                    entity_type="corridor", entity_id=corridor["id"],
                    field="definition", locale=locale,
                    value=translation["text"], state="translated",
                    note=translation["source_id"],
                )
                counts["corridor_definition_translated"] += 1
            elif defined:
                add_field(
                    report, entities,
                    entity_type="corridor", entity_id=corridor["id"],
                    field="definition", locale=locale, value=defined,
                    state="source",
                )
                counts["corridor_definition_source"] += 1
            else:
                errors.append(
                    f"corridor {corridor['id']}: missing definition_{locale}"
                )

        # Projects: names are proper names in most rows. Prefer an explicit
        # translation, then the official Indonesian alias, then the source name.
        for project in projects:
            translation = translation_map.get(
                ("project", project["id"], "name", locale)
            )
            alias = aliases.get(project["id"])
            if translation and translation["text"]:
                add_field(
                    report, entities,
                    entity_type="project", entity_id=project["id"],
                    field="name", locale=locale,
                    value=translation["text"], state="translated",
                    note=translation["source_id"],
                )
                counts["project_name_translated"] += 1
            elif locale == "id" and alias:
                add_field(
                    report, entities,
                    entity_type="project", entity_id=project["id"],
                    field="name", locale=locale, value=alias[0],
                    state="official", note=alias[1],
                )
                counts["project_name_official"] += 1
            else:
                add_field(
                    report, entities,
                    entity_type="project", entity_id=project["id"],
                    field="name", locale=locale, value=project["name"],
                    state="source",
                )
                counts["project_name_source"] += 1
                if locale == "id":
                    warnings.append(project["id"])

            summary = translation_map.get(
                ("project", project["id"], "summary", locale)
            )
            if summary and summary["text"]:
                add_field(
                    report, entities,
                    entity_type="project", entity_id=project["id"],
                    field="summary", locale=locale,
                    value=summary["text"], state="translated",
                    note=summary["source_id"],
                )
                entities[f"project:{project['id']}"]["summary_state"] = "translated"
                counts["project_summary_translated"] += 1
            else:
                # A factual one-sentence summary built only from sourced fields.
                # It is labelled generated in the payload and in the drawer; it is
                # not an editorial claim and it never introduces a new fact.
                add_field(
                    report, entities,
                    entity_type="project", entity_id=project["id"],
                    field="summary", locale=locale,
                    value=generated_summary(project, locale), state="generated",
                    note="Generated from curated fields; not editorial.",
                )
                entities[f"project:{project['id']}"]["summary_state"] = "generated"
                counts["project_summary_generated"] += 1

        # Estate names are proper names, so the source name is the display name.
        # Include them so search and the API have one shape.
        for estate in estates:
            add_field(
                report, entities,
                entity_type="estate", entity_id=estate["id"],
                field="name", locale=locale, value=estate["name"],
                state="source",
            )

        payloads[locale] = {
            "locale": locale,
            "messages": messages,
            "entities": entities,
            "missing_label": id_["app.translation_pending"],
        }
        coverage[locale] = {
            "ui_keys": len(messages),
            "required_entity_fields": len(
                [row for row in report if row["locale"] == locale and row["field"] != "summary"]
            ),
            "translated": counts["project_name_translated"]
            + counts["project_name_official"]
            + counts["corridor_definition_translated"],
            "fallback": counts["project_name_source"],
            "project_summary_translated": counts["project_summary_translated"],
            "project_summary_generated": counts["project_summary_generated"],
            "warnings": len(warnings),
        }

    if errors:
        print(f"{len(errors)} i18n error(s):")
        for message in errors[:40]:
            print(" -", message)
        raise SystemExit(1)

    SITE_DATA.mkdir(parents=True, exist_ok=True)
    for locale in LOCALES:
        path = SITE_DATA / f"i18n.{locale}.js"
        text = json.dumps(payloads[locale], ensure_ascii=False, separators=(",", ":"))
        path.write_text(f"window.INFRA_I18N = {text};\n", encoding="utf-8")

    DERIVED.mkdir(parents=True, exist_ok=True)
    fields = ["entity_type", "entity_id", "field", "locale", "state", "note"]
    from data_model import write_csv  # local import to keep the header tidy

    write_csv(DERIVED / "i18n_report.csv", fields, report)

    print(
        f"OK: {len(en)} UI keys x {len(LOCALES)} locales; "
        f"{len(payloads['en']['entities'])} entity records; "
        f"{len(report)} coverage rows"
    )
    for locale in LOCALES:
        info = coverage[locale]
        print(
            f"  {locale}: translated {info['translated']}, "
            f"official/source fallback {info['fallback']}, "
            f"project summaries generated {info['project_summary_generated']}"
        )
    if coverage["id"]["warnings"]:
        print(
            f"  note: {coverage['id']['warnings']} project names use the source name "
            "because no Indonesian translation or official alias is recorded"
        )


if __name__ == "__main__":
    main()
