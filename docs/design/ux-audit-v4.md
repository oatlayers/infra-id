# UX audit — V4 baseline

**Date:** 9 November 2026
**Scope:** English and Indonesian editions at desktop, laptop and mobile widths.
**Evidence:** `docs/evidence/phase-3/` screenshots and `ux-rehearsal.json`;
`scripts/dev/smoke_site.py`; `scripts/dev/ux_rehearsal.py`;
`scripts/dev/check_contrast.py`.

## 1. Method and honesty

Two passes were run:

1. **Expert heuristic walkthrough.** The four primary tasks were exercised in
   both locales on `file://` and a local HTTP server, with keyboard and
   touch-sized viewports. Findings below are from that walkthrough.
2. **Automated five-profile rehearsal.** The same four tasks ran through five
   viewport/locale/input profiles. This catches layout and interaction
   regressions and gives a time baseline.

The build is local-only. No analytics, account, cookie or remote request is
involved.

## 2. Profiles

| Profile | Viewport | Locale | Input | Why |
|---|---|---|---|---|
| Desk researcher | 1440 × 900 | EN | Mouse | Default international reading case |
| Policy analyst | 1280 × 800 | ID | Mouse | Indonesian-first user on a smaller desktop |
| Laptop journalist | 1024 × 768 | EN | Mouse | Constrained width, checking a fact quickly |
| Field user | 390 × 844 | ID | Touch | One-handed mobile use |
| Keyboard user | 1440 × 900 | EN | Keyboard search | Non-pointer path |

## 3. Tasks and results

| # | Task | Success criterion | Result | Median time |
|---|---|---|---|---|
| 1 | Find a named project and verify its status and source | Drawer opens with title, status pill and at least one source link | 5/5 profiles | 0.54 s |
| 2 | Read the PSN project coverage row in Data | Coverage table shows 226 current / 226 target | 5/5 profiles | 0.15 s |
| 3 | Filter to East Java and open the first project | 23 rows, drawer opens | 5/5 profiles | 1.00 s |
| 4 | Switch language and keep the current view | `lang` changes, `#/data` preserved | 5/5 profiles | 0.92 s |

The mobile profile needed two taps on the sheet handle before the filter tools
were visible. That was a real finding; the handle now cycles
peek → half → full → peek on tap, and the rehearsal follows that path.

The search task exposed a relevance issue rather than a failure: searching
“Trans Sumatra” returned project rows from that corridor before the corridor
itself, because the corridor name is in every project's search text. Grouped
counts now show `Projects 18 · Corridors 1 · Companies 1`, and clicking the
corridor group opens the matching corridor. Fuzzy ranking is still open.

## 4. Findings

### Fixed in this build

| Finding | Fix | Evidence |
|---|---|---|
| Data, Programmes, Corridors and Estates were squeezed into the 400 px rail beside an unrelated map | Full-width register pages, max 1180 px; map hidden on those views; two-column programme and corridor grids | `04-data-desktop.png`, `03b-programmes-desktop.png`, `02-corridors-desktop.png` |
| No Indonesian edition, no language switch, English-only chrome | `site/en/`, `site/id/`, chooser, 635-key catalogues, `translations.csv`, language switch preserving the hash | `00-language-chooser.png`, `08-explore-id-desktop.png`, `08d-data-id-desktop.png` |
| 140 project names fell back to the source name; no project summaries | 163 reviewed Indonesian names plus 88 official PSN aliases; a factual one-sentence summary in both locales, labelled generated | `08-explore-id-desktop.png`, `08f-project-drawer-id.png` |
| English-only status, sector, filter, sort and Data prose | All chrome and the Data methods are translated; `Intl` number/date/coordinate formatting | `08d-data-id-desktop.png` |
| English prose in the Indonesian edition could look like a translation failure | `lang="en"` on sourced text and a visible `EN` tag; a quiet note at the top of the project drawer | `05-project-drawer.png` |
| Mobile filters were unreachable at peek height | Tapping the sheet handle cycles to half and full; filters are then reachable | `ux-rehearsal.json`, field-id profile |
| Small `EN`/`ID` programme badge used muted-2 at 2.91:1 | Badge now uses muted at 4.73:1 | `check_contrast.py` |
| Unknown status had no pill treatment | Added `.status-pill.s-unknown` with a grey border, soft fill and text label | style tile |
| No companies or agencies view despite 101 organisation profiles | Full-width Companies view with type filter, role search, expandable project and estate roles, filtered CSV and two downloads | `03d-companies-desktop.png` |
| The atlas had one IKN Phase 2 row against a 25-package target | Added 23 named IKN package and project rows with status, location and source claims; the census reached 28/28 with the 10 November private-investment batch | `09-ikn-search-desktop.png`, `09b-ikn-toll-drawer.png` |
| Data had no charts | Native sector, status and freshness charts from the existing stats | `04b-data-charts.png` |
| Data headers did not sort | The four coverage headers now sort by layer, current count, target and gap, with `aria-sort`, a visible arrow and focus retention. The curated order is unchanged until a header is activated. | `11-data-sort-desktop.png` |
| The indicator layer was thin | Added 21 delivery-report indicators and 14 dated values; programme cards now show education, health, housing, infrastructure and energy measures | `10-education-pkpn-card.png`, `10c-data-indicators.png` |
| Leaflet scale and attribution leaked above the full-height mobile sheet on register views | The map is hidden for wide views on mobile, matching the existing desktop rule | `10e-education-mobile.png` |
| The 2027 PKPN were absent from the programme register | Eight PKPN cards with bilingual summaries, targets, budgets and indicators, in speech order | `03b-programmes-desktop.png` |

### Open

| Pri | Finding | Why it matters | Next action |
|---|---|---|---|
| Medium | 294 project summaries are generated from fields, not written by an editor | The text is factual but telegraphic and does not explain why a project matters | Review the flagship and high-traffic summaries; keep the generated text for the long tail |
| Medium | Explore now uses 13 px row titles and 10.5–12.5 px captions; the 14–16 px body scale is not complete | The plan targets a 14–16 px body and 12–13 px captions | Finish the body scale in Release 4.3 and re-test 320/390 px overflow |
| Medium | Search ranking is still token containment, with no edit distance or arrow-key result navigation | Grouped counts and synonyms fix discovery, but typo tolerance and keyboard result movement remain | Add fuzzy ranking and result-list arrow navigation |
| Medium | Data coverage `reference_set`, download labels/meta and dictionary descriptions remain English in the ID edition | These are methodological strings, not proper names | Move coverage labels and download labels into the catalogue; translate dictionary descriptions in Release 4.4 |
| Forty-five indicators and nine phases are sourced | The layer is structurally complete but still thin against the 300-indicator target | Add ministry baseline values and project-level output indicators as official reporting is filed |
| Low | The 300-company target is met at 314 profiles; 14 profiles remain reference-only and 100 projects have no organisation role | The Companies view now covers project and estate roles, but the network is not complete | Add sourced roles where a source names one; do not add bare profiles |
| Medium | No map-only mode or rail collapse | Explore still fixes 400 px for the rail | Add a collapse control and a map-only state |
| Medium | Mobile navigation is still a tab row inside the sheet | The plan calls for a five-item bottom bar with “More” | Add the bottom bar and a full-screen filter sheet |
| Medium | Drawer only; no shareable project, programme or company page | Deep links are hash-based and the drawer is not a page | Add detail routes and static printable pages |
| Medium | No list↔map hover linking | Users cannot connect a row to a marker | Add hover/focus highlighting in both directions |
| Medium | Corridor and estate geometry are still absent | The map is project-only | Add corridor lines and estate polygons once sourced |
| Low | Tables lack `<caption>`; some table headers are not scoped | WCAG 2.2 AA table semantics | Add captions and `scope` attributes |
| Low | No print stylesheet | Users cannot print a project or Data page cleanly | Add print CSS for detail and Data pages |

## 5. Baseline measurements

| Measure | Value |
|---|---|
| Projects / programmes / estates | 294 / 24 / 204 |
| Mapped project markers | 205 |
| Locales | 2, 635 UI keys each |
| Project names | 294 Indonesian display names (206 reviewed + 88 official) |
| Project summaries | 294 generated in both locales; 0 editorial |
| Indicators / values / phases | 45 / 28 / 9 |
| Sortable coverage headers | 4 |
| PKPN programmes | 8, with 27 claims |
| Companies / role links | 314 / 457 (271 project, 186 estate) |
| Sources / dictionary tables | 140 / 28 |
| Initial payload (one locale + core Explore) | 1,398 KB |
| Runtime data payload | 2,149 KB |
| Total payload including downloads | 4,600 KB |
| Mobile horizontal overflow | none at 390 px (EN and ID) |
| External requests | none |
| Console / page errors | none |
| Contrast pairs asserted | 19; all pass WCAG AA |
| Keyboard path | skip link, Ctrl+K, Escape, coverage sort buttons, arrow-row navigation, drawer Escape and focus trap |
| Automated task success | 20/20 steps across five profiles |

## 6. Recommended order

1. Review the generated project summaries and write editorial summaries for the
   flagships and high-traffic rows (Medium, Release 4.1/4.4).
2. Raise the Explore type scale (High, Release 4.3).
3. Search fuzzy ranking and result navigation (Medium, Release 4.3).
4. A general sortable table component and column chooser in Data (Medium, Release 4.3); the coverage table now sorts.
5. Mobile bottom navigation and full-screen filters (Medium, Release 4.3).
6. Detail pages and list↔map linking (Medium, Release 4.3).
7. Table semantics and print CSS (Low, Release 4.5).
