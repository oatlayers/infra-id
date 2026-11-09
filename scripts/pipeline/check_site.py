"""Check the generated site payload and its local-only guarantees.

Asserts that payload counts match the curated tables, every project has the
required properties, the search index covers every project and estate, the
downloads exist, and the shell loads no remote resource.

Run: python scripts/pipeline/check_site.py
Exits non-zero on any failure.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import CURATED, ROOT, SITE_DATA, SITE_DOWNLOADS, read_csv

SITE = ROOT / "site"
CHOOSER = SITE / "index.html"
LOCALES = ("en", "id")
errors: list[str] = []


def err(message: str) -> None:
    errors.append(message)


def load_global(path: Path, name: str):
    text = path.read_text(encoding="utf-8").strip()
    prefix = f"window.{name} = "
    if not text.startswith(prefix):
        raise SystemExit(f"{path}: expected {prefix!r}")
    payload = text[len(prefix) :].rstrip().rstrip(";")
    return json.loads(payload)


def check_local_assets() -> None:
    pages = [SITE / locale / "index.html" for locale in LOCALES] + [CHOOSER]
    for page in pages:
        if not page.exists():
            err(f"{page.relative_to(SITE)}: page is missing")
            continue
        html = page.read_text(encoding="utf-8")
        for match in re.finditer(r'(?:src|href)="([^"]+)"', html):
            target = match.group(1)
            if target.startswith(("#", "data:", "http://", "https://", "//", "mailto:")):
                continue
            path = (page.parent / target.split("?")[0]).resolve()
            if not path.exists():
                err(f"{page.relative_to(SITE)}: missing local asset {target}")

    for name in ("app.js", "map.js", "constants.js", "i18n.js"):
        text = (SITE / "assets" / name).read_text(encoding="utf-8")
        if re.search(r"\bfetch\s*\(", text):
            err(f"assets/{name}: uses fetch(), which file:// blocks")
        if "XMLHttpRequest" in text:
            err(f"assets/{name}: uses XMLHttpRequest")
        if re.search(r"https?://(?:tile|unpkg|cdn|fonts\.googleapis)", text):
            err(f"assets/{name}: references a remote host")

    css = (SITE / "assets" / "app.css").read_text(encoding="utf-8")
    if re.search(r"url\(\s*['\"]?https?://", css):
        err("assets/app.css: loads a remote URL")


def check_i18n() -> None:
    payloads = {}
    for locale in LOCALES:
        path = SITE_DATA / f"i18n.{locale}.js"
        if not path.exists():
            err(f"i18n.{locale}.js: missing")
            continue
        payload = load_global(path, "INFRA_I18N")
        payloads[locale] = payload
        if payload.get("locale") != locale:
            err(f"i18n.{locale}.js: locale is {payload.get('locale')!r}")
        messages = payload.get("messages") or {}
        if not messages:
            err(f"i18n.{locale}.js: empty message catalogue")
        blank = [key for key, value in messages.items() if not str(value).strip()]
        if blank:
            err(f"i18n.{locale}.js: blank messages {blank[:5]}")
        entities = payload.get("entities") or {}
        if not entities:
            err(f"i18n.{locale}.js: empty entity map")

    if len(payloads) == len(LOCALES):
        en_keys = set(payloads["en"].get("messages", {}))
        id_keys = set(payloads["id"].get("messages", {}))
        if en_keys != id_keys:
            err(
                "i18n: catalogue key mismatch; "
                f"missing id {sorted(en_keys - id_keys)[:5]}, missing en {sorted(id_keys - en_keys)[:5]}"
            )
        project_total = len(read_csv(CURATED / "projects.csv"))
        for locale in LOCALES:
            project_entities = [
                key for key in payloads[locale].get("entities", {}) if key.startswith("project:")
            ]
            if len(project_entities) != project_total:
                err(
                    f"i18n.{locale}.js: {len(project_entities)} project entities, "
                    f"expected {project_total}"
                )
            programme_entities = [
                key for key in payloads[locale].get("entities", {}) if key.startswith("programme:")
            ]
            if len(programme_entities) != 24:
                err(f"i18n.{locale}.js: {len(programme_entities)} programme entities, expected 24")

    for locale in LOCALES:
        page = (SITE / locale / "index.html").read_text(encoding="utf-8")
        for needle in (
            f'<html lang="{locale}"',
            f'data/i18n.{locale}.js',
            'window.ATLAS_BASE = "../"',
            'data-lang-target="en"',
            'data-lang-target="id"',
            'hreflang="en"',
            'hreflang="id"',
        ):
            if needle not in page:
                err(f"site/{locale}/index.html: missing {needle!r}")
        if re.search(r'(?:src|href)="(?:assets|vendor|data)/', page):
            err(f"site/{locale}/index.html: a root-relative asset path is still present")

    chooser = CHOOSER.read_text(encoding="utf-8")
    for needle in ('href="en/index.html"', 'href="id/index.html"', 'hreflang="en"', 'hreflang="id"'):
        if needle not in chooser:
            err(f"site/index.html: missing {needle!r}")
    if re.search(r'(?:src|href)="(?:https?:)?//', chooser):
        err("site/index.html: chooser references a remote host")


def main() -> None:
    projects = read_csv(CURATED / "projects.csv")
    estates = read_csv(CURATED / "estates.csv")
    corridors = read_csv(CURATED / "corridors.csv")
    segments = read_csv(CURATED / "corridor_segments.csv")
    events = read_csv(CURATED / "project_events.csv")
    conflicts = read_csv(CURATED / "conflicts.csv")
    claims = read_csv(CURATED / "project_sources.csv")
    organizations = read_csv(CURATED / "organizations.csv")
    project_orgs = read_csv(CURATED / "project_organizations.csv")
    programmes = read_csv(CURATED / "programmes.csv")
    programme_projects = read_csv(CURATED / "programme_projects.csv")
    programme_claims = read_csv(CURATED / "programme_sources.csv")
    pkpn_programmes = read_csv(CURATED / "pkpn_programmes.csv")
    pkpn_claims = read_csv(CURATED / "pkpn_sources.csv")
    indicators = read_csv(CURATED / "indicators.csv")
    indicator_values = read_csv(CURATED / "indicator_values.csv")
    phases = read_csv(CURATED / "project_phases.csv")

    payload = load_global(SITE_DATA / "projects.js", "PROJECTS")
    features = payload.get("features", [])
    estate_payload = load_global(SITE_DATA / "estates.js", "INFRA_ESTATES")
    company_payload = load_global(SITE_DATA / "companies.js", "INFRA_COMPANIES")
    programme_payload = load_global(SITE_DATA / "programmes.js", "INFRA_PROGRAMMES")
    pkpn_payload = load_global(SITE_DATA / "pkpn.js", "INFRA_PKPN")
    corridor_payload = load_global(SITE_DATA / "corridors.js", "CORRIDORS")
    stats = load_global(SITE_DATA / "stats.js", "INFRA_STATS")
    search = load_global(SITE_DATA / "search.js", "INFRA_SEARCH")

    if len(features) != len(projects):
        err(f"projects.js: {len(features)} features, expected {len(projects)}")
    if len(estate_payload) != len(estates):
        err(f"estates.js: {len(estate_payload)} rows, expected {len(estates)}")
    if len(company_payload) != len(organizations):
        err(f"companies.js: {len(company_payload)} rows, expected {len(organizations)}")
    if len(programme_payload) != len(programmes):
        err(f"programmes.js: {len(programme_payload)} rows, expected {len(programmes)}")
    if len(pkpn_payload) != len(pkpn_programmes):
        err(f"pkpn.js: {len(pkpn_payload)} rows, expected {len(pkpn_programmes)}")
    if len(corridor_payload) != len(corridors):
        err(f"corridors.js: {len(corridor_payload)} rows, expected {len(corridors)}")

    project_ids = set()
    required = {
        "id", "name", "sector", "status", "province", "island", "precision",
        "psn", "verification", "status_as_of", "last_verified", "status_basis",
        "sources", "freshness_state", "freshness_due",
    }
    for feature in features:
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        project_id = props.get("id", "")
        if project_id in project_ids:
            err(f"projects.js: duplicate id {project_id!r}")
        project_ids.add(project_id)
        missing = sorted(required - set(props))
        if missing:
            err(f"projects.js {project_id}: missing {missing}")
        if len(geometry.get("coordinates", [])) != 2:
            err(f"projects.js {project_id}: point geometry missing")
        if not props.get("sources"):
            err(f"projects.js {project_id}: no source attached")
        if props.get("freshness_state") not in {"fresh", "due_soon", "stale", "unknown"}:
            err(f"projects.js {project_id}: bad freshness state")
        for indicator in props.get("indicators", []):
            if indicator.get("project_id") != project_id:
                err(f"projects.js {project_id}: indicator does not point back to the project")
            if not indicator.get("source_id"):
                err(f"projects.js {project_id}: indicator has no source")
        for phase in props.get("phases", []):
            if phase.get("project_id") != project_id:
                err(f"projects.js {project_id}: phase does not point back to the project")
            if not phase.get("source_id"):
                err(f"projects.js {project_id}: phase has no source")

    estate_ids = set()
    for estate in estate_payload:
        estate_id = estate.get("id", "")
        if estate_id in estate_ids or estate_id in project_ids:
            err(f"estates.js: duplicate or colliding id {estate_id!r}")
        estate_ids.add(estate_id)
        for field in ("name", "type", "province", "status", "source_id", "freshness_state"):
            if not estate.get(field):
                err(f"estates.js {estate_id}: missing {field}")

    search_projects = {row["id"] for row in search if row.get("type") == "project"}
    search_estates = {row["id"] for row in search if row.get("type") == "estate"}
    search_companies = {row["id"] for row in search if row.get("type") == "company"}
    search_programmes = {row["id"] for row in search if row.get("type") == "programme"}
    search_corridors = {row["id"] for row in search if row.get("type") == "corridor"}
    if search_projects != project_ids:
        err("search.js: project coverage does not match projects.js")
    if search_estates != estate_ids:
        err("search.js: estate coverage does not match estates.js")
    company_ids = {row["id"] for row in organizations}
    if search_companies != company_ids:
        err("search.js: company coverage does not match organizations.csv")
    if search_programmes != ({row["id"] for row in programmes} | {row["id"] for row in pkpn_programmes}):
        err("search.js: programme coverage does not match the programme tables")
    if search_corridors != {row["id"] for row in corridors}:
        err("search.js: corridor coverage does not match corridors.csv")
    for company in company_payload:
        for role in company.get("roles", []):
            if role.get("project_id") not in project_ids:
                err(f"companies.js {company.get('id')}: unknown project role {role.get('project_id')}")

    programme_ids = set()
    programme_numbers = set()
    for programme in programme_payload:
        programme_id = programme.get("id", "")
        if programme_id in programme_ids or programme_id in project_ids or programme_id in estate_ids:
            err(f"programmes.js: duplicate or colliding id {programme_id!r}")
        programme_ids.add(programme_id)
        number = str(programme.get("psn_no", ""))
        if number in programme_numbers:
            err(f"programmes.js: duplicate PSN number {number!r}")
        programme_numbers.add(number)
        for field in (
            "name_id", "name_en", "theme", "summary_id", "summary_en", "status",
            "source_id", "last_verified", "claims",
        ):
            if not programme.get(field):
                err(f"programmes.js {programme_id}: missing {field}")
        if len(programme.get("claims", [])) < 2:
            err(f"programmes.js {programme_id}: fewer than two programme claims")
        linked = programme.get("projects", [])
        if any(link.get("id") not in project_ids for link in linked):
            err(f"programmes.js {programme_id}: unknown linked project")
        for indicator in programme.get("indicators", []):
            if indicator.get("programme_id") != programme_id:
                err(f"programmes.js {programme_id}: indicator does not point back to the programme")
    if programme_ids != {row["id"] for row in programmes}:
        err("programmes.js: ids do not match the curated programme table")
    if len(programme_numbers) != 24:
        err(f"programmes.js: {len(programme_numbers)} PSN numbers, expected 24")

    pkpn_ids = set()
    for pkpn in pkpn_payload:
        pkpn_id = pkpn.get("id", "")
        if pkpn_id in pkpn_ids or pkpn_id in programme_ids or pkpn_id in project_ids:
            err(f"pkpn.js: duplicate or colliding id {pkpn_id!r}")
        pkpn_ids.add(pkpn_id)
        for field in (
            "name_id", "name_en", "theme", "summary_id", "summary_en",
            "source_id", "last_verified", "claims",
        ):
            if not pkpn.get(field):
                err(f"pkpn.js {pkpn_id}: missing {field}")
        if len(pkpn.get("claims", [])) < 2:
            err(f"pkpn.js {pkpn_id}: fewer than two claims")
        for indicator in pkpn.get("indicators", []):
            if indicator.get("programme_id") != pkpn_id:
                err(f"pkpn.js {pkpn_id}: indicator does not point back to the programme")
    if pkpn_ids != {row["id"] for row in pkpn_programmes}:
        err("pkpn.js: ids do not match the curated PKPN table")

    project_stats = stats.get("projects", {})
    if project_stats.get("total") != len(projects):
        err("stats.js: project total does not match the curated table")
    if sum(project_stats.get("by_status", {}).values()) != len(projects):
        err("stats.js: status counts do not sum to the project total")
    if sum(project_stats.get("by_sector", {}).values()) != len(projects):
        err("stats.js: sector counts do not sum to the project total")
    if stats.get("corridors", {}).get("segments") != len(segments):
        err("stats.js: segment count does not match the curated table")
    if stats.get("corridors", {}).get("events") != len(events):
        err("stats.js: event count does not match the curated table")
    if stats.get("conflicts", {}).get("total") != len(conflicts):
        err("stats.js: conflict count does not match the curated table")
    if stats.get("claims", {}).get("total") != len(claims):
        err("stats.js: claim count does not match the curated table")
    if stats.get("claims", {}).get("projects_fully_claimed") != len(projects):
        err("stats.js: not every project is fully claimed")
    if stats.get("organizations", {}).get("total") != len(organizations):
        err("stats.js: organisation total does not match the curated table")
    if stats.get("organizations", {}).get("links") != len(project_orgs):
        err("stats.js: organisation link count does not match the curated table")
    if stats.get("programmes", {}).get("total") != len(programmes):
        err("stats.js: programme total does not match the curated table")
    if stats.get("pkpn", {}).get("total") != len(pkpn_programmes):
        err("stats.js: PKPN total does not match the curated table")
    if stats.get("pkpn", {}).get("claims") != len(pkpn_claims):
        err("stats.js: PKPN claim count does not match the curated table")
    if stats.get("programmes", {}).get("claims") != len(programme_claims):
        err("stats.js: programme claim count does not match the curated table")
    if stats.get("programmes", {}).get("links") != len(programme_projects):
        err("stats.js: programme link count does not match the curated table")
    if stats.get("indicators", {}).get("total") != len(indicators):
        err("stats.js: indicator total does not match the curated table")
    if stats.get("indicators", {}).get("values") != len(indicator_values):
        err("stats.js: indicator value count does not match the curated table")
    if stats.get("phases", {}).get("total") != len(phases):
        err("stats.js: phase total does not match the curated table")
    if stats.get("freshness", {}).get("records") != len(projects) + len(estates):
        err("stats.js: freshness report does not cover every project and estate")
    if not stats.get("freshness", {}).get("next_due"):
        err("stats.js: freshness next_due is missing")
    if not stats.get("changelog"):
        err("stats.js: changelog is empty")
    if len(stats.get("dictionary", [])) < 100:
        err("stats.js: data dictionary looks incomplete")

    for download in stats.get("downloads", []):
        path = SITE / download["file"]
        if not path.exists():
            err(f"downloads: missing {download['file']}")

    with (SITE_DOWNLOADS / "claims.csv").open(encoding="utf-8", newline="") as fh:
        claim_rows = list(csv.DictReader(fh))
    if len(claim_rows) != len(claims):
        err("claims.csv: row count does not match the curated claims")
    if any(row["project_id"] not in project_ids for row in claim_rows):
        err("claims.csv: unknown project id")

    with (SITE_DOWNLOADS / "programme-claims.csv").open(encoding="utf-8", newline="") as fh:
        programme_claim_rows = list(csv.DictReader(fh))
    if len(programme_claim_rows) != len(programme_claims):
        err("programme-claims.csv: row count does not match the curated claims")
    if any(row["programme_id"] not in programme_ids for row in programme_claim_rows):
        err("programme-claims.csv: unknown programme id")

    check_local_assets()
    check_i18n()

    # The initial payload is the shell for one locale and the Explore view:
    # basemap, projects, corridors, stats, search and one i18n payload.
    # Estates and programmes are lazy view bundles; the other locale is never
    # loaded. The total includes every data file and every download.
    core_names = ("basemap.js", "projects.js", "corridors.js", "stats.js", "search.js")
    initial_files = [SITE_DATA / name for name in core_names if (SITE_DATA / name).exists()]
    locale_payloads = sorted(
        SITE_DATA.glob("i18n.*.js"), key=lambda path: path.stat().st_size
    )
    if locale_payloads:
        initial_files.append(locale_payloads[-1])
    initial_bytes = sum(path.stat().st_size for path in initial_files)
    data_bytes = sum(path.stat().st_size for path in SITE_DATA.glob("*") if path.is_file())
    download_bytes = sum(
        path.stat().st_size for path in SITE_DOWNLOADS.glob("*") if path.is_file()
    )
    if initial_bytes > 1_500_000:
        err(f"payload: initial {initial_bytes / 1024:.0f} KB exceeds the 1.5 MB budget")
    if data_bytes + download_bytes > 5_000_000:
        err(
            f"payload: total {(data_bytes + download_bytes) / 1024:.0f} KB "
            "exceeds the 5 MB budget"
        )

    if errors:
        print(f"{len(errors)} site error(s):")
        for message in errors:
            print(" -", message)
        raise SystemExit(1)

    size = sum(
        path.stat().st_size
        for directory in (SITE_DATA, SITE_DOWNLOADS)
        for path in directory.glob("*")
        if path.is_file()
    )
    print(
        f"OK: {len(features)} projects, {len(estate_payload)} estates, "
        f"{len(company_payload)} companies, {len(pkpn_payload)} PKPN programmes, "
        f"{len(corridor_payload)} corridors, {len(claim_rows)} claims, "
        f"{len(conflicts)} conflicts, {len(indicators)} indicators, "
        f"{len(phases)} phases; initial {initial_bytes / 1024:.0f} KB, "
        f"data {data_bytes / 1024:.0f} KB, total {(data_bytes + download_bytes) / 1024:.0f} KB"
    )


if __name__ == "__main__":
    main()
