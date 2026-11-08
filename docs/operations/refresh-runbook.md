# Monthly refresh runbook

**Cadence:** once a month, in the first week. **Owner:** whoever holds the
repository; no remote or deployment is involved. The atlas is a local, curated
release, not a live tracker.

**Why monthly:** a row is treated as fresh for 183 days after `last_verified`
and due soon in the final 30 days. The 9 November 2026 build has 318 fresh rows;
the first record falls due on **11 May 2027**. A monthly pass keeps the whole
dataset ahead of that cliff instead of refreshing everything at once.

**Never do in this runbook:** push to GitHub, add a remote, deploy GitHub Pages,
publish the site, backdate `last_verified`, or change a status on one secondary
source. Fetching a page is not verification.

---

## 1. Prepare

```bash
git status --short          # must be clean before refreshing
git log --oneline -3        # note the starting commit
python scripts/build_all.py --check
```

`build_all.py --check` must end with `deterministic rebuild`. If it reports
drift, fix the build before changing data: a refresh on top of an unstable build
cannot be reviewed.

Create the raw snapshot folder with the real date:

```text
data/raw/YYYY-MM-DD/
```

Raw snapshots are never edited. If a source returns a different page or PDF,
save it under the new date rather than overwriting the old one.

## 2. Fetch, newest first

Work in this order. Official sources first; secondary sources only to cross-check
or to discover a change.

| Order | Source | What to fetch | Watch for |
|---:|---|---|---|
| 1 | BPJT toll-road API | `https://itrams-api.bpjt.pu.go.id/v1/reference/api/toll-road-list` | Status labels, operating/construction km, operator, endpoint coordinates |
| 2 | Kemenhub transport PSN deck | `https://ppid.kemenhub.go.id/fileupload/informasi-berkala/20260406102830.R1_19022026_Update_PSN_Kemenhub_compressed.pdf` | A newer deck; opening dates, progress, targets |
| 3 | KPPIP PSN pages | `https://kppip.go.id/proyek-strategis-nasional/` | Airport, seaport and industrial-area list changes |
| 4 | KEK National Council | `https://kek.go.id/id/investment/distribution` | New zones, changed coordinates, area or developer |
| 5 | Kemenperin / BAJRA estate list | The 2024 BAJRA mirror; retry `kemenperin.go.id` and `satudata.kemenperin.go.id` | The 179-vs-160 gap; any 2025/2026 additions |
| 6 | BPJT Trans Java section list and Trans corridor pages | The dated article and the Wikipedia revisions already in `sources.csv` | Section openings, total vs operating km, definition changes |
| 7 | Factory company and official pages | Each factory's source rows in `sources.csv` | Status, capacity, investment, restart or halt |
| 8 | Hutama Karya, Bina Marga and Katadata corridor items | The rows already in `sources.csv` | Operational km, connected/paved metrics, target changes |

Useful fetch pattern:

```powershell
$date = Get-Date -Format 'yyyy-MM-dd'
New-Item -ItemType Directory -Force "data/raw/$date" | Out-Null
Invoke-WebRequest -Uri '<url>' -OutFile "data/raw/$date/<name>"
```

For an API, save the JSON unchanged. For HTML, save the page or a dated print to
PDF. Record the retrieval date and a hash in `sources.csv`.

If a source is unreachable, write that down; do not substitute an undated
search-result snippet. The 8 November 2026 run recorded Kemenperin HTTP 502 and
`satudata.kemenperin.go.id` DNS failure, which is why the estate gap remains.

## 3. Diff and triage

Compare the new snapshot with the previous one before editing curated data.

```powershell
Get-ChildItem "data/raw/YYYY-MM-DD" -File | ForEach-Object {
  $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.Substring(0, 16)
  "$hash  $($_.Name)"
}
```

For each changed source, answer three questions:

1. **What fact changed?** Status, km, capacity, investment, operator, opening
   date, target year, area, coordinates or legal basis.
2. **Is the change dated?** An exact date is required for an event. A month-end
   approximation is not enough.
3. **Is the claim strong enough?** A status change needs an official source or
   two independent sources. A numeric change needs a source that states the
   number; do not derive one from a chart.

Put every disagreement in `data/curated/conflicts.csv` with both values and both
source ids, even when the atlas resolves it. If a conflict is resolved, say what
the atlas publishes and why. Open conflicts are visible in the Data view.

## 4. Update the curated tables

Edit `data/curated/` only; generated files are rebuilt in step 5.

### 4.1 Sources

Add a row to `sources.csv` for every new document, with `retrieved_on`,
`source_type`, `language`, `archive_path` and `snapshot_hash` where available.
Never point at a raw snapshot that does not exist.

### 4.2 Projects and claims

For a changed project:

- update `status`, `status_basis`, `status_as_of` and `last_verified` together;
- update the numeric field on `projects.csv` and add **one atomic claim row per
  fact** in `project_sources.csv` (`status`, `length`, `operational`, `opening`,
  `investment`, `capacity`, `location`, `coordinates`, `operator`, `target`,
  `progress`, ...);
- never use a comma-separated `claim`; validation rejects it;
- record the value in `claim_value` when it is short enough to transcribe, and
  the fact's date in `claim_date` when the source states one;
- set `verification` to `official`, `dual` or `single` honestly. `single` is
  allowed only when the row already says so in its notes.

### 4.3 Corridors and events

Update `corridors.csv` only when the source gives a dated total or operational
series. A partial section table does not create a corridor percentage. Add a
`corridor_segments.csv` row when a dated section length or status is published.
Add `project_events.csv` only for an exact date; attach it to a project and cite
the source.

### 4.4 Estates and factories

- Estates: update area, developer, legal basis, status or coordinates only with a
  source per row. Keep the map layer off while `precision=regency` dominates.
- Factories: update capacity, investment, status, restart or halt. Capacity is
  nameplate or design output, not verified production. Investment is project
  capex where stated; the rupiah figure is a ranking conversion at
  Rp 16,500/USD, not a transaction-date rate.

### 4.5 Conflict register

Add or update the row in `conflicts.csv`:

```text
id,scope,subject,project_id,estate_id,corridor_id,field,
value_a,source_a,value_b,source_b,status,resolution,notes
```

`scope` is `project`, `corridor`, `estate`, `dataset` or `method`; `status` is
`open` or `resolved`. Both source ids must exist. Do not delete a conflict just
because the atlas has chosen a value.

### 4.6 PSN register and reconciliation

When a new Permenko changes the PSN list, snapshot the PDF under
`data/raw/YYYY-MM-DD/`, add the source row with its SHA-256 hash, and update
`data/curated/psn_register.csv`. Keep deleted slots in the register with
`status=deleted` so the official numbering stays auditable. Then run:

```bash
python scripts/pipeline/build_psn_ledger.py
```

The script refuses to run unless the register has exactly 226 active projects,
24 active programmes and 3 deleted slots. Update the explicit match maps in
`scripts/pipeline/build_psn_ledger.py` when a new atlas row resolves a gap; do
not replace them with fuzzy matching. The generated ledger is
`data/derived/psn_reconciliation.csv`.

## 5. Rebuild

Run the whole pipeline, not a subset:

```bash
python scripts/build_all.py
```

This runs, in order:

1. `scripts/pipeline/validate.py`
2. `scripts/pipeline/build_projects.py`
3. `scripts/pipeline/build_dictionary.py`
4. `scripts/pipeline/freshness.py`
5. `scripts/pipeline/audit_claims.py`
6. `scripts/pipeline/build_site_data.py`
7. `scripts/pipeline/build_factories_ledger.py`
8. `scripts/pipeline/check_site.py`

A successful run prints the current counts and ends with the site payload size.
For a report-only check, use an explicit as-of date:

```bash
python scripts/pipeline/freshness.py --as-of 2026-12-08
```

For a **rebuilt site**, set `INFRAA_AS_OF` so `scripts/pipeline/freshness.py` and
`scripts/pipeline/build_site_data.py` use the same date:

```powershell
$env:INFRAA_AS_OF = '2026-12-08'
python scripts/build_all.py
$env:INFRAA_AS_OF = $null
```

`INFRAA_BUILD_DATE` overrides the deterministic `generated_on` date; leave it
unset for a normal rebuild. If you use `--as-of` on `scripts/pipeline/freshness.py` alone and then
rebuild, the Data view will still show the newest `last_verified` as its as-of
date. That is why the environment variable is the safer path.

If `scripts/pipeline/freshness.py` reports `due_soon`, `stale` or `unknown`, inspect
`data/derived/freshness_report.csv` before rebuilding. Do not edit that file;
refresh the underlying rows.

## 6. Verify locally

### 6.1 Deterministic rebuild

```bash
python scripts/build_all.py --check
```

The run must end with `deterministic rebuild, 26 generated files unchanged`.
This is the local CI gate. It does not touch git or the network.

### 6.2 Browser smoke test

If Playwright and Edge are installed:

```bash
python scripts/dev/smoke_site.py
```

It checks the four views, a project drawer, a corridor segment drawer, keyboard
access, filtered CSV/GeoJSON downloads, the static claims CSV, `file://`, a local
HTTP server, no external request and no console error. It writes screenshots and
`smoke-report.json` to `docs/evidence/phase-3/`. Playwright is a development
dependency and is not needed to view or ship the site.

### 6.3 Manual spot checks

- Open `site/index.html` from the filesystem. The map, fonts and data must load.
- Open the same page through `python -m http.server 8765 --directory site`.
- Check one changed project in the drawer: status basis, freshness badge, every
  source, and the claim values.
- Check the Data view: coverage, claims, freshness, conflicts, dictionary,
  changelog and the filtered CSV/GeoJSON buttons.
- Confirm the map legend, estates table and corridor segment tables still render.

### 6.4 Data-view spot checks

```bash
python scripts/pipeline/check_site.py
```

The output must show the expected project, estate, claim and conflict counts.
If a download is missing, the check fails before the browser does.

## 7. Commit and stop

Review the diff, then commit locally:

```bash
git status --short
git diff --stat
git add data/curated data/raw data/derived data/exports/projects.csv site scripts docs README.md CHANGELOG.md plan-v3.md plan.md
git commit -m "Refresh sources and verification dates for <month>"
```

**Do not** `git push`, add a remote, open a pull request, deploy Pages or publish
the site. The repository owner has deferred publishing explicitly.

## 8. If something fails

| Symptom | Action |
|---|---|
| `build_all.py --check` reports drift | Re-run without `--check`; inspect the changed generated file; fix the generator or commit the regenerated output. Never hand-edit a generated file. |
| `scripts/pipeline/validate.py` rejects a claim | A claim must name one type from `CLAIM_TYPES`; split the fact into separate rows. |
| A source is unreachable | Record the failure and date in the batch notes; keep the previous verified row. Do not lower verification quality to fill a gap. |
| An estate cannot be geocoded | Leave the regency centroid and `coordinate_source=regency`; keep the map layer off. Do not invent a point. |
| A corridor has a new total but no operating series | Update the total only; the site will keep publishing "no progress series". |
| A factory status is disputed | Record both values in `conflicts.csv`; keep the last verified status until the rule is met. |
| `scripts/dev/smoke_site.py` cannot launch Edge | Use the manual checks and record that the browser smoke test was skipped. Do not install or change the machine's browser without the owner's approval. |

## 9. Monthly checklist

- [ ] Working tree clean and `build_all.py --check` passes.
- [ ] New raw snapshots saved under `data/raw/YYYY-MM-DD/`.
- [ ] BPJT status and km diffed.
- [ ] Kemenhub transport deck checked for a newer version.
- [ ] KPPIP, KEK and Kemenperin/BAJRA estate sources retried.
- [ ] PSN regulation and `psn_register.csv` checked for a newer Permenko;
      reconciliation ledger regenerated.
- [ ] Trans corridor totals and sections checked.
- [ ] Factory statuses, capacity and investment checked.
- [ ] Changed rows updated with atomic claims and `last_verified`.
- [ ] Conflicts added or closed in `conflicts.csv`.
- [ ] `build_all.py` and `build_all.py --check` pass.
- [ ] Browser smoke test or documented manual checks pass.
- [ ] README, plan, changelog and this runbook updated if counts or behaviour
      changed.
- [ ] Local commit made; **nothing pushed or published**.
