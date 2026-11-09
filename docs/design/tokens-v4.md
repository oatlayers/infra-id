# Design tokens — V4 baseline

**Date:** 9 November 2026
**Source of truth:** [`site/assets/tokens.css`](../../site/assets/tokens.css)
**Visual specimen:** [`style-tile.html`](style-tile.html)
**Contrast test:** `python scripts/dev/check_contrast.py`

The atlas is an editorial reference book that happens to be interactive. The
palette is cream paper, deep navy and one burnt-orange accent. The map is the
hero in Explore; the register views are full-width reading pages. No view may
introduce a second accent or a decorative colour.

## Colour

| Token | Value | Use |
|---|---|---|
| `--paper` | `#fbf9f4` | Page ground |
| `--surface` | `#ffffff` | Cards, drawers, tables |
| `--surface-warm` | `#f7f4ec` | Notes and quiet panels |
| `--ink` | `#101828` | Body text |
| `--navy` | `#0b1f33` | Header and brand |
| `--muted` | `#667085` | Captions, secondary text |
| `--muted-2` | `#8a94a6` | Decorative chevrons and icons only |
| `--line` | `#e4e7ec` | Hairlines |
| `--line-strong` | `#cfd4dc` | Hover borders |
| `--accent` | `#b54708` | Links, focus ring, active tab |
| `--uc` | `#c2410c` | Under construction |
| `--planned` | `#1d4ed8` | Planned |
| `--operating` | `#0f766e` | Operating |
| `--done` | `#15803d` | Recently completed |
| `--stalled` | `#b42318` | Stalled |
| unknown | `#667085` | Status not sourced; uses the muted grey with a dashed/no-colour cue |

Each status also has a soft background and border token (`--uc-soft`,
`--uc-line`, and so on). Status is always colour + dot + text label; colour
alone is never the message.

## Type

| Role | Family | Size / line height |
|---|---|---|
| Display | Source Serif 4 | 48 / 1.05 |
| Page title | Source Serif 4 | 36 / 1.1 |
| Section title | Source Serif 4 | 28 / 1.15 |
| Card title | Source Serif 4 | 22 / 1.2 |
| Body | Inter | 16 / 1.6 |
| Interface | Inter | 14 / 1.5 |
| Caption | Inter | 12 / 1.4 |

The target body scale is 14–16 px with 12–13 px captions. The current Explore
rail still uses 9.5–12.5 px for density; this is the main open typography item
in Release 4.3. Full-width Data, Programmes and Corridors already use the
larger scale.

Maximum line length is 70 characters. Numbers in tables use tabular figures.

## Spacing, shape and motion

- **Spacing:** 4, 8, 12, 16, 24, 32, 48, 64.
- **Radius:** `--r-sm` 8, `--r-md` 12, `--r-lg` 16, `--r-pill` 999.
- **Shadow:** `--shadow` for overlays, `--shadow-soft` for cards.
- **Motion:** 120 ms hover, 180 ms drawer, 240 ms map fit. Respect
  `prefers-reduced-motion`; no autoplay.

## Layout

- Header: 64 px; brand, search, three counts, Data link, EN/ID switch.
- Explore: 400 px rail at ≥ 1200 px, map fills the rest; drawer overlays.
- Data, Programmes, Corridors and Estates: full-width register pages, centred
  at a maximum of 1180 px; the map is hidden rather than left as an unrelated
  background.
- Mobile: map behind a three-snap sheet; header keeps the search and language
  switch; no horizontal overflow at 390 px.

## Bilingual surface

- The language switch is a two-item segmented control in the header: `EN` and
  `ID`. The active item uses a raised white-on-navy treatment; the other is
  muted. Both labels are proper language names, not translated.
- `<html lang>` is set per page. Sourced text that remains English inside the
  Indonesian edition carries `lang="en"` and a small `EN` tag.
- `Belum diterjemahkan` is the visible fallback label for a missing translation;
  it is never silently replaced with English.
- The Indonesian edition is not a theme. It keeps the same palette, spacing and
  status colours.

## Contrast

`scripts/dev/check_contrast.py` reads the live tokens and asserts:

| Pair | Ratio | Need |
|---|---:|---:|
| Ink on paper | 16.87 | 4.5 |
| Muted on paper | 4.73 | 4.5 |
| Muted on warm surface | 4.53 | 4.5 |
| Accent on paper | 5.16 | 4.5 |
| White on navy | 16.69 | 4.5 |
| Under construction on its soft background | 4.63 | 4.5 |
| Accent focus ring on navy | 3.08 | 3.0 |

The decorative chevron (`--muted-2` on paper, 2.91:1) is not relied on for
meaning. Focus rings are 2 px accent with a 2 px offset.

## Change control

1. Change `tokens.css`, not a copy.
2. Run `python scripts/dev/check_contrast.py`.
3. Open `docs/design/style-tile.html` and check the specimen.
4. If a status or sector is added, add its colour, soft background, border and
   text label together.
5. Run `python scripts/build_all.py --check` and the browser smoke test.
