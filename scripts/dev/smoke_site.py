"""Browser smoke test for the local release. Development-only.

Requires Playwright and an installed Microsoft Edge (``channel="msedge"``).
Playwright is deliberately not in ``requirements.txt``: the build pipeline never
needs a browser, and the release is usable without one.

Checks the four views, a project drawer, keyboard basics, filtered CSV/GeoJSON
downloads, a static CSV download, ``file://`` and a local HTTP server, and
asserts that the page makes no external request and logs no console error.

Writes screenshots and a JSON report to ``docs/evidence/phase-3/``.

Run: python scripts/dev/smoke_site.py
"""

from __future__ import annotations

import csv
import io
import json
import re
import threading
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
EVIDENCE = ROOT / "docs" / "evidence" / "phase-3"
FILE_URL = (SITE / "en" / "index.html").as_uri()
ID_FILE_URL = (SITE / "id" / "index.html").as_uri()
CHOOSER_URL = (SITE / "index.html").as_uri()

STATS_TEXT = (SITE / "data" / "stats.js").read_text(encoding="utf-8")
STATS = json.loads(re.search(r"window\.INFRA_STATS\s*=\s*(\{.*\});?", STATS_TEXT, re.S).group(1))
TOTAL = str(STATS["projects"]["total"])
RAIL = str(STATS["projects"]["by_sector"].get("railway", 0))
ESTATES = str(STATS["estates"]["total"])
PROGRAMMES = str(STATS["programmes"]["total"])
COMPANIES = str(STATS["organizations"]["total"])

failures: list[str] = []
report: dict[str, object] = {
    "checked_at": date.today().isoformat(),
    "views": {},
    "downloads": {},
    "keyboard": {},
    "protocols": {},
    "screenshots": [],
}


def check(condition: bool, label: str) -> None:
    print(("PASS " if condition else "FAIL ") + label)
    if not condition:
        failures.append(label)


def watch(page: Page, external: list[str], console: list[str], page_errors: list[str]) -> None:
    def on_request(request):
        url = request.url
        if url.startswith(("file:", "data:", "blob:")):
            return
        if url.startswith("http://127.0.0.1:"):
            return
        external.append(url)

    page.on("request", on_request)
    page.on(
        "console",
        lambda message: console.append(message.text) if message.type == "error" else None,
    )
    page.on("pageerror", lambda error: page_errors.append(str(error)))


def read_csv_download(download) -> list[dict[str, str]]:
    path = download.path()
    if path is None:
        raise AssertionError("download has no local path")
    text = Path(path).read_text(encoding="utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def screenshot(page: Page, name: str) -> None:
    target = EVIDENCE / name
    page.screenshot(path=str(target), animations="disabled")
    report["screenshots"].append(name)  # type: ignore[union-attr]
    print(f"SHOT docs/evidence/phase-3/{name}")


def tab(page: Page, view: str) -> None:
    page.click(f'[data-view="{view}"]')
    page.wait_for_timeout(250)


def locale_shell(page: Page) -> None:
    page.goto(CHOOSER_URL)
    page.wait_for_selector(".choice")
    check(page.locator(".choice").count() == 2, "Language chooser offers two editions")
    check(page.locator('a[href="en/index.html"]').count() == 1, "Chooser links to English")
    check(page.locator('a[href="id/index.html"]').count() == 1, "Chooser links to Indonesian")
    screenshot(page, "00-language-chooser.png")

    page.click('a[href="id/index.html"]')
    page.wait_for_selector(".project-row")
    page.wait_for_timeout(900)
    check(page.evaluate("document.documentElement.lang") == "id",
          "Indonesian edition sets html lang=id")
    check("Jelajahi" in page.locator(".tabs").inner_text(),
          "Indonesian edition translates the navigation")
    check("Perusahaan" in page.locator(".tabs").inner_text(),
          "Indonesian edition translates the Companies tab")
    check(page.locator("#stat-projects").inner_text() == TOTAL,
          f"Indonesian edition loads {TOTAL} projects")
    check(page.locator(".project-row").count() == int(TOTAL),
          f"Indonesian edition lists {TOTAL} project rows")
    check("proyek" in page.locator("#result-count").inner_text().lower(),
          "Indonesian edition translates the result count")
    check(page.locator("#search").get_attribute("placeholder").startswith("Cari"),
          "Indonesian edition translates the search placeholder")
    screenshot(page, "08-explore-id-desktop.png")

    page.goto(ID_FILE_URL + "#/programmes")
    page.wait_for_selector(".programme-card")
    page.wait_for_timeout(400)
    check(page.locator(".programme-card").count() == int(PROGRAMMES),
          f"Indonesian edition renders {PROGRAMMES} programme cards")
    check(page.locator(".pkpn-card").count() == 8,
          "Indonesian edition renders eight PKPN cards")
    check("Delapan PKPN" in page.locator(".programme-view").inner_text(),
          "Indonesian edition translates the PKPN section")
    screenshot(page, "08b-programmes-id-desktop.png")

    page.goto(ID_FILE_URL + "#/estates")
    page.wait_for_selector(".estate-row")
    page.wait_for_timeout(400)
    check(page.locator(".estate-row").count() == int(ESTATES),
          f"Indonesian edition renders {ESTATES} estate rows")
    screenshot(page, "08c-estates-id-desktop.png")

    page.goto(ID_FILE_URL + "#/data")
    page.wait_for_selector(".data-view")
    page.wait_for_timeout(400)
    check("Data dan metode" in page.locator(".data-view").inner_text(),
          "Indonesian edition translates the Data view")
    check(page.locator(".dictionary details").count() == 28,
          "Indonesian edition renders 28 dictionary tables")
    screenshot(page, "08d-data-id-desktop.png")
    page.click('[data-lang-target="en"]')
    page.wait_for_selector(".data-view")
    page.wait_for_timeout(500)
    check(page.evaluate("document.documentElement.lang") == "en",
          "Language switch returns to English")
    check("#/data" in page.url, "Language switch preserves the current view")
    report["locales"] = {"chooser": True, "en": True, "id": True}  # type: ignore[index]


def desktop_views(page: Page) -> None:
    page.goto(FILE_URL + "#/explore")
    page.wait_for_selector(".project-row")
    page.wait_for_timeout(900)

    check(page.locator(".project-row").count() == int(TOTAL), f"Explore lists {TOTAL} projects")
    check(page.locator("#foot-total").inner_text() == TOTAL, f"Explore total is {TOTAL}")
    check(page.locator("#stat-projects").inner_text() == TOTAL, f"Header project count is {TOTAL}")
    check(page.locator("#stat-corridors").inner_text() == "5", "Header corridor count is 5")
    check(page.locator("#stat-estates").inner_text() == ESTATES, f"Header estate count is {ESTATES}")
    report["views"]["explore"] = {"rows": int(TOTAL)}  # type: ignore[index]
    screenshot(page, "01-explore-desktop.png")

    page.click('[data-sector="railway"]')
    page.wait_for_timeout(200)
    check(page.locator("#foot-count").inner_text() == RAIL, f"Railway filter narrows to {RAIL}")
    check(page.locator(".project-row").count() == int(RAIL), f"Railway rows are {RAIL}")
    page.click("#clear-filters")
    page.wait_for_timeout(200)
    check(page.locator("#foot-count").inner_text() == TOTAL, f"Clearing filters restores {TOTAL}")

    tab(page, "corridors")
    check(page.locator(".corridor-card").count() == 5, "Corridors view has five corridors")
    report["views"]["corridors"] = {"cards": 5}  # type: ignore[index]
    screenshot(page, "02-corridors-desktop.png")
    page.click('[data-corridor="trans-sumatera"]')
    page.wait_for_selector("#drawer:not([hidden]) .segment-table")
    page.wait_for_timeout(300)
    check(page.locator("#drawer .segment-table tbody tr").count() == 13,
          "Trans Sumatra drawer lists 13 segments")
    screenshot(page, "02b-corridor-segments-desktop.png")
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)

    tab(page, "estates")
    page.wait_for_selector(".estate-row")
    page.wait_for_timeout(400)
    check(page.locator(".estate-row").count() == int(ESTATES), f"Estates view lists {ESTATES} zones")
    check(ESTATES in page.locator(".corridor-meta").first.inner_text(), f"Estate count text is {ESTATES}")
    report["views"]["estates"] = {"rows": int(ESTATES)}  # type: ignore[index]
    screenshot(page, "03-estates-desktop.png")

    tab(page, "companies")
    page.wait_for_selector(".company-row")
    page.wait_for_timeout(400)
    check(page.locator(".company-row").count() == int(COMPANIES),
          f"Companies view lists {COMPANIES} organisations")
    check("PT Jasa Marga" in page.locator(".estate-list").inner_text(),
          "Companies view shows a named organisation")
    page.click('[data-company="org-hutama-karya"]')
    page.wait_for_timeout(250)
    check(page.locator(".company-role-list li").count() >= 1,
          "Company detail lists at least one project role")
    page.click('[data-company-type="government"]')
    page.wait_for_timeout(250)
    check(page.locator(".company-row").count() < int(COMPANIES),
          "Company type filter narrows the organisation list")
    page.click('[data-company-type="all"]')
    page.wait_for_timeout(250)
    report["views"]["companies"] = {"rows": int(COMPANIES)}  # type: ignore[index]
    screenshot(page, "03d-companies-desktop.png")

    tab(page, "programmes")
    page.wait_for_selector(".programme-card")
    page.wait_for_timeout(400)
    check(page.locator(".pkpn-card").count() == 8, "Programme view lists eight PKPN priorities")
    check("Kedaulatan Pangan" in page.locator(".programme-view").inner_text(),
          "PKPN cards show the official Indonesian priority name")
    check("820.9" in page.locator(".programme-view").inner_text(),
          "The education PKPN budget is visible")
    check("10,000" in page.locator(".programme-view").inner_text(),
          "The health PKPN target is visible")
    check(page.locator(".programme-card").count() == int(PROGRAMMES),
          f"Programmes view lists {PROGRAMMES} PSN programmes")
    check("Program Ketenagalistrikan" in page.locator(".programme-view").inner_text(),
          "Programme cards show the official Indonesian name")
    check("Mencakup kebijakan" in page.locator(".programme-view").inner_text(),
          "Programme cards show the Indonesian summary")
    check(page.locator('.programme-card a[href="#/project/energy-plts-100gw-phase-1"]').count() == 1,
          "Programme cards link to a curated project")
    check(page.locator(".programme-indicators").count() >= 1,
          "Programme cards show a target-versus-current indicator")
    programme_text = page.locator(".programme-view").inner_text().lower()
    check("target vs current" in programme_text and "100 gwp" in programme_text,
          "The 100 GWp target is visible on the programme card")
    page.click('[data-programme-theme="food"]')
    page.wait_for_timeout(200)
    check(page.locator(".programme-card").count() == 4, "Food theme narrows to four programmes")
    page.click('[data-programme-theme="all"]')
    page.wait_for_timeout(200)
    report["views"]["programmes"] = {"cards": int(PROGRAMMES)}  # type: ignore[index]
    screenshot(page, "03b-programmes-desktop.png")

    tab(page, "data")
    check(page.locator(".chart").count() == 2, "Data view renders two chart panels")
    check(page.locator(".bar-row").count() == 14, "Sector chart lists all 14 sectors")
    check(page.locator(".chart-legend-item").count() >= 6,
          "Status and freshness charts have a legend")
    check("projects by sector" in page.locator(".data-view").inner_text().lower(),
          "Data view labels the sector chart")
    check(page.locator(".conflict-table tbody tr").count() == 19, "Conflict register has 19 rows")
    check(page.locator(".dictionary details").count() == 28, "Data dictionary has 28 tables")
    check(page.locator('a.download[href]').count() == 23, "Data view has 23 static downloads")
    check("programme register" in page.locator(".data-view").inner_text().lower(),
          "Data view has a programme register section")
    check(page.locator('.download[data-export="projects-csv"]').count() == 1,
          "Data view offers the filtered project CSV")
    check(page.locator('.download[data-export="projects-geojson"]').count() == 1,
          "Data view offers the filtered GeoJSON")
    check(page.locator('.download[data-export="estates-csv"]').count() == 1,
          "Loaded estates add the filtered estate CSV")
    check(page.locator('.download[data-export="companies-csv"]').count() == 1,
          "Loaded companies add the filtered company CSV")
    check(f"{TOTAL} / {TOTAL}" in page.locator(".data-view").inner_text(), f"Claims coverage is {TOTAL} / {TOTAL}")
    report["views"]["data"] = {  # type: ignore[index]
        "conflicts": 19,
        "dictionary_tables": 28,
        "download_controls": 26,
        "charts": 2,
    }
    screenshot(page, "04-data-desktop.png")


def desktop_drawer(page: Page) -> None:
    page.goto(FILE_URL + "#/explore")
    page.wait_for_selector(".project-row")
    page.click(".project-row")
    page.wait_for_selector("#drawer:not([hidden])")
    page.wait_for_timeout(400)
    title = page.locator("#drawer-title").inner_text()
    check(bool(title), "Project drawer opens with a title")
    check(page.locator(".freshness-line").count() == 1, "Drawer shows the freshness line")
    check(page.locator("#drawer-body a[href]").count() >= 1, "Drawer lists at least one source link")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    page.fill("#search", "100 GWp")
    page.wait_for_timeout(250)
    page.locator(".project-row").first.click()
    page.wait_for_selector("#drawer:not([hidden])")
    page.wait_for_timeout(300)
    drawer_text = page.locator("#drawer-body").inner_text().lower()
    check("indicators" in drawer_text and "5.3" in drawer_text,
          "Drawer shows the 100 GWp indicator and current value")
    check("phases" in drawer_text and "phase 1" in drawer_text,
          "Drawer shows the sourced project phase")
    report["views"]["drawer"] = {"title": title}  # type: ignore[index]
    screenshot(page, "05-project-drawer.png")
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    check(page.locator("#drawer").is_hidden(), "Escape closes the project drawer")


def desktop_keyboard(page: Page) -> None:
    page.goto(FILE_URL + "#/explore")
    page.reload()
    page.wait_for_selector(".project-row")
    page.keyboard.press("Tab")
    focused = page.evaluate("document.activeElement && document.activeElement.className")
    check("skip-link" in (focused or ""), "First Tab reaches the skip link")

    page.keyboard.press("Control+k")
    check(page.evaluate("document.activeElement && document.activeElement.id") == "search",
          "Ctrl+K focuses search")
    page.fill("#search", "Papua")
    page.wait_for_timeout(300)
    narrowed = page.locator(".project-row").count()
    check(0 < narrowed < int(TOTAL), "Search narrows the project list")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    check(page.input_value("#search") == "", "Escape clears search")
    check(page.locator(".project-row").count() == int(TOTAL), "Clearing search restores the list")

    page.fill("#search", "Trans Sumatra")
    page.wait_for_timeout(300)
    check(page.locator("#search-groups").is_visible(), "Search shows grouped results")
    check(page.locator('[data-search-type="corridor"]').count() == 1,
          "Search groups include corridors")
    check("1" in page.locator('[data-search-type="corridor"]').inner_text(),
          "The Trans Sumatra corridor is in the group count")
    page.click('[data-search-type="corridor"]')
    page.wait_for_selector(".corridor-card")
    page.wait_for_timeout(300)
    check(page.locator(".corridor-card").count() == 1,
          "A corridor search opens the matching corridor view")
    page.fill("#search", "")
    page.wait_for_selector(".project-row")
    page.wait_for_timeout(300)

    page.locator(".project-row").first.focus()
    page.keyboard.press("ArrowDown")
    focused_row = page.evaluate("document.activeElement && document.activeElement.getAttribute('data-project')")
    check(bool(focused_row), "ArrowDown moves focus to the next project row")
    report["keyboard"] = {  # type: ignore[index]
        "skip_link": True, "ctrl_k": True, "arrow_nav": True, "grouped_search": True
    }


def desktop_downloads(page: Page) -> None:
    page.goto(FILE_URL + "#/data")
    page.wait_for_selector('.download[data-export="projects-csv"]')

    with page.expect_download() as csv_info:
        page.click('[data-export="projects-csv"]')
    csv_download = csv_info.value
    csv_rows = read_csv_download(csv_download)
    check(len(csv_rows) == int(TOTAL), f"Filtered project CSV has {TOTAL} rows")
    check(csv_download.suggested_filename.endswith(".csv"), "Filtered project CSV has a .csv name")
    check(csv_rows[0].get("id") is not None and "freshness_state" in csv_rows[0],
          "Filtered project CSV includes the freshness field")
    report["downloads"]["projects_csv"] = {  # type: ignore[index]
        "file": csv_download.suggested_filename,
        "rows": len(csv_rows),
    }

    with page.expect_download() as geojson_info:
        page.click('[data-export="projects-geojson"]')
    geojson_download = geojson_info.value
    geojson_path = geojson_download.path()
    payload = json.loads(Path(geojson_path).read_text(encoding="utf-8"))
    features = payload.get("features", [])
    check(len(features) == int(TOTAL), f"Filtered GeoJSON has {TOTAL} features")
    check(all(len(feature.get("geometry", {}).get("coordinates", [])) == 2 for feature in features),
          "Filtered GeoJSON features are points")
    report["downloads"]["projects_geojson"] = {  # type: ignore[index]
        "file": geojson_download.suggested_filename,
        "features": len(features),
    }

    page.click('[data-view="estates"]')
    page.wait_for_selector('.estate-row')
    with page.expect_download() as estate_info:
        page.click('[data-export="estates-csv"]')
    estate_download = estate_info.value
    estate_rows = read_csv_download(estate_download)
    check(len(estate_rows) == int(ESTATES), f"Filtered estate CSV has {ESTATES} rows")
    report["downloads"]["estates_csv"] = {  # type: ignore[index]
        "file": estate_download.suggested_filename,
        "rows": len(estate_rows),
    }

    page.goto(FILE_URL + "#/data")
    page.wait_for_selector('a[download][href="../downloads/claims.csv"]')
    with page.expect_download() as claims_info:
        page.click('a[download][href="../downloads/claims.csv"]')
    claims_download = claims_info.value
    claims_rows = read_csv_download(claims_download)
    check(len(claims_rows) == STATS["claims"]["total"], f"Static claims CSV has {STATS['claims']['total']} rows")
    report["downloads"]["claims_csv"] = {  # type: ignore[index]
        "file": claims_download.suggested_filename,
        "rows": len(claims_rows),
    }


def mobile(page: Page) -> None:
    page.goto(FILE_URL + "#/explore")
    page.wait_for_selector(".project-row")
    page.wait_for_timeout(900)
    check(page.locator(".project-row").count() > 0, "Mobile Explore renders project rows")
    width = page.evaluate("document.documentElement.scrollWidth")
    check(width <= 391, f"Mobile layout has no horizontal overflow (width {width})")
    screenshot(page, "06-explore-mobile.png")

    page.goto(FILE_URL + "#/programmes")
    page.wait_for_selector(".programme-card")
    page.wait_for_timeout(400)
    check(page.locator(".programme-card").count() == int(PROGRAMMES),
          f"Mobile Programmes renders {PROGRAMMES} cards")
    width = page.evaluate("document.documentElement.scrollWidth")
    check(width <= 391, f"Mobile Programmes has no horizontal overflow (width {width})")
    screenshot(page, "06b-programmes-mobile.png")

    page.goto(FILE_URL + "#/data")
    page.wait_for_selector(".data-view")
    page.wait_for_timeout(400)
    check(page.locator(".conflict-table tbody tr").count() == 19, "Mobile Data view renders conflicts")
    screenshot(page, "07-data-mobile.png")

    page.goto(ID_FILE_URL + "#/explore")
    page.wait_for_selector(".project-row")
    page.wait_for_timeout(700)
    check("Jelajahi" in page.locator(".tabs").inner_text(),
          "Mobile Indonesian edition translates the navigation")
    width = page.evaluate("document.documentElement.scrollWidth")
    check(width <= 391, f"Mobile Indonesian layout has no horizontal overflow (width {width})")
    screenshot(page, "08e-explore-id-mobile.png")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):  # noqa: D401 - silence the test server
        return


def http_check(page: Page) -> None:
    handler = partial(QuietHandler, directory=str(SITE))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        page.goto(f"http://127.0.0.1:{port}/en/index.html#/data")
        page.wait_for_selector(".data-view")
        page.wait_for_timeout(500)
        check(page.locator("#stat-projects").inner_text() == TOTAL,
              f"Local HTTP server serves the {TOTAL}-project build")
        check(page.locator(".conflict-table tbody tr").count() == 19,
              "Local HTTP build renders 19 conflicts")
        page.goto(f"http://127.0.0.1:{port}/id/index.html#/explore")
        page.wait_for_selector(".project-row")
        page.wait_for_timeout(500)
        check("Jelajahi" in page.locator(".tabs").inner_text(),
              "Local HTTP server serves the Indonesian edition")
        check(page.locator("#stat-projects").inner_text() == TOTAL,
              f"Indonesian HTTP build loads {TOTAL} projects")
        report["protocols"]["http"] = {"port": port, "ok": True}  # type: ignore[index]
    finally:
        server.shutdown()
        server.server_close()


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)

        external: list[str] = []
        console: list[str] = []
        page_errors: list[str] = []
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        watch(page, external, console, page_errors)

        locale_shell(page)
        desktop_views(page)
        desktop_drawer(page)
        desktop_keyboard(page)
        desktop_downloads(page)
        http_check(page)

        mobile_external: list[str] = []
        mobile_console: list[str] = []
        mobile_errors: list[str] = []
        mobile_page = browser.new_page(viewport={"width": 390, "height": 844},
                                       is_mobile=True, has_touch=True)
        watch(mobile_page, mobile_external, mobile_console, mobile_errors)
        mobile(mobile_page)

        browser.close()

    all_external = external + mobile_external
    all_console = console + mobile_console
    all_page_errors = page_errors + mobile_errors
    check(not all_external, "No external page request")
    check(not all_console, "No console error")
    check(not all_page_errors, "No page error")
    report["protocols"]["file"] = {"ok": True}  # type: ignore[index]
    report["external_requests"] = all_external
    report["console_errors"] = all_console
    report["page_errors"] = all_page_errors
    report["failures"] = failures
    report["ok"] = not failures

    (EVIDENCE / "smoke-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if failures:
        print(f"\n{len(failures)} smoke check(s) failed")
        raise SystemExit(1)
    print("\nOK: local release smoke test passed")


if __name__ == "__main__":
    main()
