# Data model

The atlas is a normalised set of curated CSV tables. One entity or relationship
per row. `data/curated/` is the source of truth; exports and browser payloads are
generated.

## Curated tables

| Table | One row per | Key fields |
|---|---|---|
| `projects.csv` | project | `id`, `name`, `sector`, `status`, `corridor_id`, `island`, km, investment, location, `status_as_of`, `verification` |
| `organizations.csv` | company or agency | `id`, `name`, `org_type`, `country_code`, `parent_id`, `website` |
| `project_organizations.csv` | project–organisation role | `project_id`, `org_id`, `role`, `share_pct`, `source_id` |
| `investments.csv` | commitment or tranche | `project_id`, `investor_org_id`, `amount`, `currency`, `amount_idr_t`, `stage`, `instrument` |
| `sources.csv` | source document | `id`, `publisher`, `title`, `url`, `published_on`, `retrieved_on`, `source_type`, `language`, `archive_path` |
| `project_sources.csv` | project–source claim | `project_id`, `source_id`, one atomic `claim`, `claim_value`, `claim_date` |
| `project_external_ids.csv` | external key | `project_id`, `system`, `external_id` |
| `project_aliases.csv` | project alias | `project_id`, `alias`, `source_id` |
| `project_events.csv` | dated event | `project_id`, `event_date`, `event_type`, `description`, `source_id` |
| `project_geometry.csv` | geometry | `project_id`, `kind`, GeoJSON `geometry`, `precision`, `source_id` |
| `laws.csv` / `project_laws.csv` | regulation / relation | legal basis, kept separate from news |
| `corridors.csv` | Trans corridor | `total_km`, `operational_km`, `construction_km`, `planned_km`, `metric`, `as_of` |
| `corridor_segments.csv` | corridor segment | `segment_type`, section-level km, progress, status, opening year, geometry |
| `estates.csv` | industrial estate or SEZ | `id`, `name`, `type`, `province`, `regency`, `island`, `area_ha`, `developer`, `status`, `coordinate_source`, `source_id` |
| `estate_sources.csv` | estate–source claim | `estate_id`, `source_id`, one atomic `claim`, `claim_value`, `claim_date` |
| `coverage_targets.csv` | coverage layer | `layer`, `label`, `unit`, `target_count`, `reference_set`, `source_id` |
| `conflicts.csv` | source disagreement | `id`, `scope`, `subject`, `field`, `value_a`, `source_a`, `value_b`, `source_b`, `status`, `resolution` |
| `psn_register.csv` | official PSN project or programme | `id`, `kind`, `psn_no`, `sector`, official `name_id`, `location`, `status`, `source_id` |
| `programmes.csv` | PSN programme | `id`, `psn_no`, `name_id`, `name_en`, `theme`, `pkpn_id`, `lead_org_id`, bilingual summaries, `source_id` |
| `programme_projects.csv` | programme–project link | `programme_id`, `project_id`, `role`, `source_id`, `notes` |
| `programme_sources.csv` | programme–source claim | `programme_id`, `source_id`, one atomic `claim`, `claim_value`, `claim_date` |
| `pkpn_programmes.csv` | 2027 PKPN priority | bilingual name, summary, target, budget, `source_id` |
| `pkpn_sources.csv` | PKPN–source claim | `programme_id`, `source_id`, one atomic `claim`, `claim_value`, `claim_date` |
| `translations.csv` | reviewed locale text | `entity_type`, `entity_id`, `field`, `locale`, `text`, `status`, `translator`, `reviewed_on`, `source_id` |
| `indicators.csv` | measurable target | `id`, `programme_id`, `project_id`, bilingual name, `unit`, `direction`, baseline, target, `source_id` |
| `indicator_values.csv` | dated observation | `indicator_id`, `value`, `as_of`, `source_id` |
| `project_phases.csv` | project phase or package | `project_id`, phase name, status, dates, cost and source where stated |

## Project columns

| Column | Required | Allowed values / meaning |
|---|---|---|
| `id` | yes | Lowercase, hyphenated, unique. Used in deep links |
| `name` | yes | Project name, English with Indonesian proper names |
| `sector` | yes | `road`, `railway`, `airport`, `seaport`, `factory`, `energy`, `water`, `housing`, `technology`, `education`, `tourism`, `agriculture`, `urban`, `coastal` |
| `subsector` | no | For example `toll`, `urban_rail`, `new_build`, `expansion`, `smelter`, `steel`, `alumina`, `battery`, `petrochemical`, `pulp`, `fertiliser` |
| `status` | yes | `planned`, `under_construction`, `operating`, `recently_completed`, `stalled`, `unknown` |
| `status_basis` | yes | The evidence for the status, with figures where possible |
| `corridor_id` | no | Links to `corridors.csv` |
| `island` | yes | `Sumatra`, `Java`, `Kalimantan`, `Sulawesi`, `Papua`, `Bali-Nusa Tenggara`, `Maluku`, `National` |
| `province` | yes | Province or provinces, semicolon-separated |
| `route` | yes | Route, corridor or location description |
| `length_km` | linear only | Total length; required for roads and railways |
| `operational_km` | no | Length in service |
| `construction_km` | no | Length under construction |
| `progress_pct` | no | Reported progress, 0–100; leave blank if not reported |
| `investment_idr_t` | no | Investment in trillion rupiah |
| `capacity` / `capacity_unit` | no | For airports, ports and factories; set both or neither |
| `psn` | yes | `yes`, `no`, `unknown` |
| `opened_year` | no | Required for `operating` and `recently_completed` |
| `opened_date` | no | Exact opening date when the source gives one |
| `expected_open_year` | no | Target year for planned or under-construction rows |
| `status_as_of` | yes | Date of the evidence behind the current status |
| `verification` | yes | `official`, `dual`, `single`, `unverified` |
| `lat`, `lon` | yes | Decimal degrees, inside 95–141°E and 11°S–6°N |
| `precision` | yes | `exact`, `approximate`, `regency`, `province` |
| `last_verified` | yes | Date the row was last checked (`YYYY-MM-DD`) |
| `notes` | yes | Conflicts, caveats, section openings, coordinate overrides |

The flat export adds `operator`, `source_url`, `source_type` and `retrieved_on`,
joined from the curated tables.

## Status definitions

| Status | Meaning |
|---|---|
| `planned` | Designated (PSN or KPBU) or tender announced; no groundbreaking |
| `under_construction` | Contract signed or groundbreaking held; latest evidence under 12 months old |
| `operating` | Major asset already in service, opened before 2024-11-06. Context, not a recent completion |
| `recently_completed` | Opened on or after 2024-11-06 |
| `stalled` | Officially delayed or reported stalled (*mangkrak*) |
| `unknown` | Register-only record; the source does not state implementation status |

## Claims and verification

Each populated status and numeric fact needs an atomic claim in
`project_sources.csv`, `estate_sources.csv`, `programme_sources.csv` or
`pkpn_sources.csv`. Allowed claim types include `status`, `length`,
`operational`, `opening`, `investment`, `capacity`, `location`, `coordinates`,
`operator`, `target` and `progress`.

- One fact per row. Validation rejects comma-separated claims.
- `verification=official` means one official source; `dual` means two independent
  sources; `single` means one secondary or company source; `unverified` means the
  record is register-only.
- A status change needs an official source or two independent sources.
- Put disagreements in `conflicts.csv` with both values and both sources.
- `data/derived/claims_audit.csv` must report no missing claims after a build.

## Generated outputs

```text
data/exports/projects.csv              flat export
data/derived/psn_reconciliation.csv    PSN match ledger
data/derived/freshness_report.csv      row-level freshness
data/derived/claims_audit.csv          per-fact claim audit
data/derived/data_dictionary.csv       field dictionary
data/derived/i18n_report.csv           translation coverage
data/derived/factories_2026.csv        frozen factory ledger
site/data/*.js                         browser runtime payload
site/downloads/*                       CSV, JSON and GeoJSON downloads
```

Never hand-edit these files. Edit `data/curated/` and rebuild.

## Identifier and formatting rules

- IDs are lowercase ASCII, hyphenated and stable. Do not reuse or renumber an ID.
- Dates use `YYYY-MM-DD`. Years are four digits.
- Numeric fields use a dot decimal separator and no thousands separator.
- Lists are semicolon-separated; do not embed a list in a claim.
- Coordinates are WGS84 decimal degrees.
- Every table header is defined in `scripts/data_model.py`; the dictionary is
  generated from it.

## Estates

`estates.csv` holds 204 rows: 179 pure industrial-estate rows, 7 shared SEZ and
industrial-estate rows, and 18 SEZ-only rows. `type` is `industrial_estate`,
`sez` or `both`. `coordinate_source` is `official`, `osm`, `regency`, `manual`
or `unknown`. Map display is gated on verified coordinates; register-only rows
use province centroids and stay off the map.

## Programmes, PKPN and indicators

- `programmes.csv` holds the 24 active PSN programmes. The annex does not state
  budgets, targets or indicators, so those fields stay blank unless another
  source states them.
- `pkpn_programmes.csv` holds the eight 2027 PKPN priorities. Targets and budgets
  come only from the budget speech and the Finance Ministry breakdown.
- `indicators.csv` records an indicator only when a source states the name, unit
  and a baseline, target or dated observation. `indicator_values.csv` records
  dated observations. Do not infer a target from atlas fields.
