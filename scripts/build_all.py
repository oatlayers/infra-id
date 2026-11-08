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

from data_model import DERIVED, ROOT, SITE_DATA

STEPS = [
    ("validate curated tables", "validate.py"),
    ("build flat project export", "build_projects.py"),
    ("build data dictionary", "build_dictionary.py"),
    ("build freshness report", "freshness.py"),
    ("audit per-fact claims", "audit_claims.py"),
    ("build site payload", "build_site_data.py"),
    ("build factory ledger", "build_factories_ledger.py"),
    ("check site payload", "check_site.py"),
]

GENERATED = [
    ROOT / "data" / "projects.csv",
    DERIVED / "factories_2026.csv",
    DERIVED / "freshness_report.csv",
    DERIVED / "claims_audit.csv",
    DERIVED / "data_dictionary.csv",
]


def generated_files() -> list[Path]:
    files = list(GENERATED)
    if SITE_DATA.exists():
        files.extend(sorted(SITE_DATA.glob("*")))
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
