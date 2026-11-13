"""Generate the English, Indonesian and chooser entry points.

One application template (``site/templates/app.html``) produces two static pages:

* ``site/en/index.html`` — ``<html lang="en">``
* ``site/id/index.html`` — ``<html lang="id">``

All asset and data URLs become ``../`` relative so both pages work from
``file://``. The chooser at ``site/index.html`` is a plain bilingual page with
no JavaScript dependency; it reads ``navigator.language`` only to highlight the
likely choice.

Run: python scripts/pipeline/build_locales.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import ROOT

SITE = ROOT / "site"
TEMPLATES = SITE / "templates"
TEMPLATE = TEMPLATES / "app.html"
CHOOSER = TEMPLATES / "chooser.html"
I18N = ROOT / "data" / "i18n"
LOCALES = ("en", "id")
LOCALE_NAMES = {"en": "English", "id": "Bahasa Indonesia"}

PLACEHOLDER_RE = re.compile(r"__[A-Z_]+__")
ASSET_RE = re.compile(r'(\b(?:src|href)=")(assets|vendor|data)/')


def catalogue(locale: str) -> dict[str, str]:
    return json.loads((I18N / f"ui.{locale}.json").read_text(encoding="utf-8"))


def render_locale(template: str, locale: str) -> str:
    strings = catalogue(locale)
    html = template

    html = html.replace('<html lang="en">', f'<html lang="{locale}" data-locale="{locale}">')
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{strings['app.title']}</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="' + strings["app.description"].replace('"', "&quot;") + '">',
        html,
        count=1,
    )
    html = html.replace(
        "<!--HREFLANG-->",
        '<link rel="alternate" hreflang="en" href="../en/">\n'
        '<link rel="alternate" hreflang="id" href="../id/">\n'
        '<link rel="alternate" hreflang="x-default" href="../">',
    )
    html = html.replace("__BASE__", "../").replace("__LOCALE__", locale)

    # The current locale links to itself; the other locale keeps ../<code>/.
    if locale == "en":
        html = html.replace('href="../en/index.html"', 'href="./index.html"')
    else:
        html = html.replace('href="../id/index.html"', 'href="./index.html"')

    html = ASSET_RE.sub(r"\1../\2/", html)

    leftovers = PLACEHOLDER_RE.findall(html)
    if leftovers:
        raise SystemExit(f"{locale}: unresolved placeholders {sorted(set(leftovers))}")

    required = (
        f'lang="{locale}"',
        f'data/i18n.{locale}.js',
        'window.ATLAS_BASE = "../"',
        'assets/i18n.js',
        'data-lang-target="en"',
        'data-lang-target="id"',
        'href="./index.html"',
    )
    for needle in required:
        if needle not in html:
            raise SystemExit(f"{locale}: generated page is missing {needle!r}")
    return html


def main() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    for locale in LOCALES:
        out = SITE / locale
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(render_locale(template, locale), encoding="utf-8")
        print(f"wrote site/{locale}/index.html")

    chooser = CHOOSER.read_text(encoding="utf-8")
    if "__" in chooser:
        raise SystemExit("templates/chooser.html contains an unresolved placeholder")
    (SITE / "index.html").write_text(chooser, encoding="utf-8")
    print("wrote site/index.html")


if __name__ == "__main__":
    main()
