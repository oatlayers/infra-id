"""Automated five-profile UX rehearsal. Development-only.

This is not a substitute for five human participants. It runs the same four
tasks through five viewport/locale/input profiles to catch layout, locale and
interaction regressions, and records a time baseline that a human study can be
compared against.

Profiles:
  desk-en        1440x900, English, mouse
  analyst-id     1280x800, Indonesian, mouse
  laptop-en      1024x768, English, mouse
  field-id        390x844, Indonesian, touch
  keyboard-en    1440x900, English, keyboard search

Tasks:
  1. Find a named project and open its drawer.
  2. Read the PSN project coverage row in Data.
  3. Filter to East Java and open the first project.
  4. Switch language and keep the current Data view.

Writes ``%TEMP%/opencode/atlas-evidence/ux-rehearsal.json``.

Run: python scripts/dev/ux_rehearsal.py
"""

from __future__ import annotations

import json
import tempfile
import time
from functools import partial
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
EVIDENCE = Path(tempfile.gettempdir()) / "opencode" / "atlas-evidence"
EN = (SITE / "en" / "index.html").as_uri()
ID = (SITE / "id" / "index.html").as_uri()

PROFILES = [
    {"name": "desk-en", "locale": "en", "width": 1440, "height": 900, "mobile": False, "keyboard": False},
    {"name": "analyst-id", "locale": "id", "width": 1280, "height": 800, "mobile": False, "keyboard": False},
    {"name": "laptop-en", "locale": "en", "width": 1024, "height": 768, "mobile": False, "keyboard": False},
    {"name": "field-id", "locale": "id", "width": 390, "height": 844, "mobile": True, "keyboard": False},
    {"name": "keyboard-en", "locale": "en", "width": 1440, "height": 900, "mobile": False, "keyboard": True},
]


def base(locale: str) -> str:
    return EN if locale == "en" else ID


def timed(task) -> tuple[bool, float, str]:
    started = time.perf_counter()
    try:
        note = task()
        elapsed = time.perf_counter() - started
        return True, round(elapsed, 3), note or "ok"
    except Exception as error:
        elapsed = time.perf_counter() - started
        return False, round(elapsed, 3), str(error).splitlines()[0][:160]


def task_project(page: Page, profile: dict) -> str:
    page.goto(base(profile["locale"]) + "#/explore")
    page.wait_for_selector(".project-row")
    if profile["keyboard"]:
        page.keyboard.press("Control+k")
        page.fill("#search", "Trans Sumatra")
        page.wait_for_timeout(250)
        page.locator(".project-row").first.focus()
        page.keyboard.press("Enter")
    else:
        page.fill("#search", "Trans Sumatra")
        page.wait_for_timeout(250)
        page.locator(".project-row").first.click()
    page.wait_for_selector("#drawer:not([hidden])")
    title = page.locator("#drawer-title").inner_text().strip()
    if not title:
        raise AssertionError("empty drawer title")
    return title


def task_coverage(page: Page, profile: dict) -> str:
    page.goto(base(profile["locale"]) + "#/data")
    page.wait_for_selector(".coverage-table")
    row = page.locator(".coverage-table tbody tr").filter(has_text="226")
    if row.count() == 0:
        raise AssertionError("PSN projects coverage row not found")
    text = row.first.inner_text()
    if "226" not in text:
        raise AssertionError("coverage row does not show 226")
    return text.replace("\n", " ")[:90]


def task_province(page: Page, profile: dict) -> str:
    page.goto(base(profile["locale"]) + "#/explore")
    page.wait_for_selector(".project-row")
    if profile["mobile"]:
        # Tap the handle twice: peek -> half -> full. This is the one-handed
        # path a user needs before the filter tools are visible.
        page.click("#sheet-handle")
        page.wait_for_timeout(250)
        page.click("#sheet-handle")
        page.wait_for_timeout(250)
    page.click("#more-filters")
    page.wait_for_selector("#filter-popover:not([hidden])")
    page.select_option("#f-province", "East Java")
    page.wait_for_timeout(350)
    page.click("#popover-close")
    page.wait_for_timeout(200)
    rows = page.locator(".project-row")
    count = rows.count()
    if count == 0:
        raise AssertionError("East Java filter returned no rows")
    rows.first.click()
    page.wait_for_selector("#drawer:not([hidden])")
    title = page.locator("#drawer-title").inner_text().strip()
    if not title:
        raise AssertionError("empty drawer title after province filter")
    return f"{count} rows; {title}"


def task_language(page: Page, profile: dict) -> str:
    page.goto(ID + "#/data")
    page.wait_for_selector(".data-view")
    page.click('[data-lang-target="en"]')
    page.wait_for_selector('html[lang="en"]')
    page.wait_for_timeout(300)
    if "#/data" not in page.url:
        raise AssertionError("view was not preserved")
    return "EN + #/data preserved"


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    results = []
    failures = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        for profile in PROFILES:
            context = browser.new_context(
                viewport={"width": profile["width"], "height": profile["height"]},
                is_mobile=profile["mobile"],
                has_touch=profile["mobile"],
            )
            page = context.new_page()
            page.goto(base(profile["locale"]) + "#/explore")
            row = {"profile": profile["name"], "tasks": {}}
            for name, task in (
                ("project", task_project),
                ("coverage", task_coverage),
                ("province", task_province),
                ("language", task_language),
            ):
                ok, seconds, note = timed(partial(task, page, profile))
                row["tasks"][name] = {"ok": ok, "seconds": seconds, "note": note}
                if not ok:
                    failures += 1
                print(
                    f"{profile['name']:14s} {name:9s} "
                    f"{'PASS' if ok else 'FAIL':4s} {seconds:5.2f}s  {note}"
                )
            results.append(row)
            context.close()
        browser.close()

    (EVIDENCE / "ux-rehearsal.json").write_text(
        json.dumps({"profiles": results, "failures": failures}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if failures:
        print(f"\n{failures} rehearsal step(s) failed")
        raise SystemExit(1)
    print("\nOK: five-profile UX rehearsal passed")


if __name__ == "__main__":
    main()
