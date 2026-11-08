"""Check the generated site payload and its local-only guarantees.

Asserts that payload counts match the curated tables, every project has the
required properties, the search index covers every project and estate, the
downloads exist, and the shell loads no remote resource.

Run: python scripts/check_site.py
Exits non-zero on any failure.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from data_model import CURATED, ROOT, SITE_DATA, read_csv

SITE = ROOT / "site"
INDEX = SITE / "index.html"
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
    html = INDEX.read_text(encoding="utf-8")
    for match in re.finditer(r'(?:src|href)="([^"]+)"', html):
        target = match.group(1)
        if target.startswith(("#", "data:", "http://", "https://", "//", "mailto:")):
            continue
        path = (SITE / target.split("?")[0]).resolve()
        if not path.exists():
            err(f"index.html: missing local asset {target}")

    for name in ("app.js", "map.js", "constants.js"):
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


def main() -> None:
    projects = read_csv(CURATED / "projects.csv")
    estates = read_csv(CURATED / "estates.csv")
    corridors = read_csv(CURATED / "corridors.csv")
    segments = read_csv(CURATED / "corridor_segments.csv")
    events = read_csv(CURATED / "project_events.csv")
    conflicts = read_csv(CURATED / "conflicts.csv")
    claims = read_csv(CURATED / "project_sources.csv")

    payload = load_global(SITE_DATA / "projects.js", "PROJECTS")
    features = payload.get("features", [])
    estate_payload = load_global(SITE_DATA / "estates.js", "INFRA_ESTATES")
    corridor_payload = load_global(SITE_DATA / "corridors.js", "CORRIDORS")
    stats = load_global(SITE_DATA / "stats.js", "INFRA_STATS")
    search = load_global(SITE_DATA / "search.js", "INFRA_SEARCH")

    if len(features) != len(projects):
        err(f"projects.js: {len(features)} features, expected {len(projects)}")
    if len(estate_payload) != len(estates):
        err(f"estates.js: {len(estate_payload)} rows, expected {len(estates)}")
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
    if search_projects != project_ids:
        err("search.js: project coverage does not match projects.js")
    if search_estates != estate_ids:
        err("search.js: estate coverage does not match estates.js")

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

    with (SITE_DATA / "claims.csv").open(encoding="utf-8", newline="") as fh:
        claim_rows = list(csv.DictReader(fh))
    if len(claim_rows) != len(claims):
        err("claims.csv: row count does not match the curated claims")
    if any(row["project_id"] not in project_ids for row in claim_rows):
        err("claims.csv: unknown project id")

    check_local_assets()

    if errors:
        print(f"{len(errors)} site error(s):")
        for message in errors:
            print(" -", message)
        raise SystemExit(1)

    size = sum(path.stat().st_size for path in SITE_DATA.glob("*") if path.is_file())
    print(
        f"OK: {len(features)} projects, {len(estate_payload)} estates, "
        f"{len(corridor_payload)} corridors, {len(claim_rows)} claims, "
        f"{len(conflicts)} conflicts; site payload {size / 1024:.0f} KB"
    )


if __name__ == "__main__":
    main()
