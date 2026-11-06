# Indonesia Infrastructure Map

A curated map of major Indonesian infrastructure: toll roads now, airports,
seaports and factories next. Every project has a source and a verification date.
It is deliberately not exhaustive.

## What is here

```
plan.md                 scope, decisions, sources, rules, phase status
data/projects.csv       curated source of truth, one row per project
data/raw/YYYY-MM-DD/    snapshots of each source, never edited
scripts/                extract, build, validate, build site data
site/                   static Leaflet page and generated data
```

## Run it

```
python scripts/build_projects.py     # rebuild data/projects.csv
python scripts/validate.py           # check the CSV
python scripts/build_site_data.py    # write site/data/*
python -m http.server 8765 --directory site
```

Then open <http://localhost:8765/>. The page also opens directly from
`site/index.html`, because it loads `data/projects.js` with a script tag rather
than `fetch`.

## Data rules

- Only projects that are planned, under construction, recently completed (opened
  on or after 2024-11-06) or stalled.
- A status change needs an official source, or two independent sources.
- Conflicts are recorded in `notes`, not silently resolved.
- `retrieved_on` is when the source was fetched; `last_verified` is when the row
  was last checked.

## Sources

See the Sources table in `plan.md`. Batch 1 uses the English Wikipedia article
"Indonesian Toll Road System" (revision 1329385293) crossed with the BPJT
toll-road API (`itrams-api.bpjt.pu.go.id`) and the Indonesian Wikipedia list.

## Licence

Code is unlicensed for now. Wikipedia text is CC BY-SA 4.0; OpenStreetMap data
is ODbL. See `plan.md` before reusing source text.
