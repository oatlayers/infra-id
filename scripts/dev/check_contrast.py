"""Check WCAG contrast for the design-token pairs used by the atlas.

Reads the real values from ``site/assets/tokens.css`` rather than a copy, so a
token change cannot silently pass this check. Text pairs need 4.5:1; focus
rings and graphical status marks need 3:1.

Run: python scripts/dev/check_contrast.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOKENS = ROOT / "site" / "assets" / "tokens.css"

PAIRS = [
    ("body text on paper", "ink", "paper", 4.5, "text"),
    ("body text on surface", "ink", "surface", 4.5, "text"),
    ("muted text on paper", "muted", "paper", 4.5, "text"),
    ("muted text on surface", "muted", "surface", 4.5, "text"),
    ("muted text on warm surface", "muted", "surface-warm", 4.5, "text"),
    ("white text on navy", "white", "navy", 4.5, "text"),
    ("accent on paper", "accent", "paper", 4.5, "text"),
    ("accent focus ring on paper", "accent", "paper", 3.0, "ui"),
    ("accent focus ring on navy", "accent", "navy", 3.0, "ui"),
    ("under construction on paper", "uc", "paper", 4.5, "text"),
    ("planned on paper", "planned", "paper", 4.5, "text"),
    ("operating on paper", "operating", "paper", 4.5, "text"),
    ("recently completed on paper", "done", "paper", 4.5, "text"),
    ("stalled on paper", "stalled", "paper", 4.5, "text"),
    ("under construction on soft", "uc", "uc-soft", 4.5, "text"),
    ("planned on soft", "planned", "planned-soft", 4.5, "text"),
    ("operating on soft", "operating", "operating-soft", 4.5, "text"),
    ("recently completed on soft", "done", "done-soft", 4.5, "text"),
    ("stalled on soft", "stalled", "stalled-soft", 4.5, "text"),
]


def read_tokens() -> dict[str, str]:
    text = TOKENS.read_text(encoding="utf-8")
    values = {}
    for name, value in re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})\s*;", text):
        values[name] = value
    # The atlas uses white in text pairs but does not need a token for it.
    values.setdefault("white", "#ffffff")
    return values


def luminance(value: str) -> float:
    value = value.lstrip("#")
    channels = [int(value[index : index + 2], 16) / 255 for index in (0, 2, 4)]

    def linear(channel: float) -> float:
        return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4

    red, green, blue = (linear(channel) for channel in channels)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def ratio(first: str, second: str) -> float:
    a, b = luminance(first), luminance(second)
    high, low = max(a, b), min(a, b)
    return (high + 0.05) / (low + 0.05)


def main() -> None:
    tokens = read_tokens()
    failures = []
    missing = sorted(
        {
            token
            for _, first, second, _, _ in PAIRS
            for token in (first, second)
            if token not in tokens
        }
    )
    if missing:
        raise SystemExit(f"tokens.css is missing: {', '.join(missing)}")

    print(f"{'Pair':38s} {'Ratio':>6s}  {'Need':>5s}  Result")
    for label, first, second, need, kind in PAIRS:
        value = ratio(tokens[first], tokens[second])
        passed = value >= need
        print(f"{label:38s} {value:6.2f}  {need:5.1f}  {'PASS' if passed else 'FAIL'} ({kind})")
        if not passed:
            failures.append((label, value, need))

    # Decorative-only pairs are reported but not asserted: chevrons and empty
    # state icons do not carry meaning by themselves.
    decorative = ratio(tokens["muted-2"], tokens["paper"])
    print(f"{'decorative chevron on paper':38s} {decorative:6.2f}  {'-':>5s}  note (non-text)")

    if failures:
        print(f"\n{len(failures)} contrast pair(s) failed")
        raise SystemExit(1)
    print("\nOK: all asserted token pairs meet WCAG AA")


if __name__ == "__main__":
    main()
