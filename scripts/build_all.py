"""Run the local build pipeline in the correct order.

Steps: validate -> flat export -> dictionary -> freshness -> claims audit ->
site payload -> factory ledger -> site check.

``--check`` hashes the generated files before and after the run and fails if a
rebuild changes bytes. This is the local CI drift check; it never touches git,
a remote or a deployment.

Run: python scripts/build_all.py [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

from data_model import DERIVED, EXPORTS, ROOT, SITE_DATA, SITE_DOWNLOADS

STEPS = [
    ("validate curated tables", "pipeline/validate.py"),
    ("build PSN reconciliation", "pipeline/build_psn_ledger.py"),
    ("build flat project export", "pipeline/build_projects.py"),
    ("build data dictionary", "pipeline/build_dictionary.py"),
    ("build freshness report", "pipeline/freshness.py"),
    ("audit per-fact claims", "pipeline/audit_claims.py"),
    ("build i18n payload", "pipeline/build_i18n.py"),
    ("build site payload", "pipeline/build_site_data.py"),
    ("build locale entry points", "pipeline/build_locales.py"),
    ("build factory ledger", "pipeline/build_factories_ledger.py"),
    ("check site payload", "pipeline/check_site.py"),
]

SITE = ROOT / "site"

GENERATED = [
    EXPORTS / "projects.csv",
    DERIVED / "psn_reconciliation.csv",
    DERIVED / "factories_2026.csv",
    DERIVED / "freshness_report.csv",
    DERIVED / "claims_audit.csv",
    DERIVED / "data_dictionary.csv",
    DERIVED / "i18n_report.csv",
    SITE / "index.html",
    SITE / "en" / "index.html",
    SITE / "id" / "index.html",
]


def generated_files() -> list[Path]:
    files = list(GENERATED)
    for directory in (SITE_DATA, SITE_DOWNLOADS):
        if directory.exists():
            files.extend(sorted(directory.glob("*")))
    return [path for path in files if path.is_file()]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot() -> dict[str, str]:
    return {str(path.relative_to(ROOT)): digest(path) for path in generated_files()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if a rebuild changes bytes")
    args = parser.parse_args()

    before = snapshot() if args.check else {}

    for label, script in STEPS:
        print(f"==> {label}")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script)],
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            raise SystemExit(f"{script} failed with exit code {result.returncode}")

    if not args.check:
        print("OK: local build complete")
        return

    after = snapshot()
    changed = sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )
    if changed:
        print(f"DRIFT: {len(changed)} generated file(s) changed on rebuild")
        for path in changed:
            print(" -", path)
        raise SystemExit(1)
    print(f"OK: deterministic rebuild, {len(after)} generated files unchanged")


if __name__ == "__main__":
    main()
