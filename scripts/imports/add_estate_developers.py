"""Link estate developers to sourced company profiles.

The 204 estate rows name 186 developers, but only eight carried a
``developer_org_id``. This script creates a company profile for every named
developer that has no profile yet and links each estate through
``developer_org_id``. One developer, PT Perkebunan Nusantara III, already has a
profile and is matched instead of duplicated.

The developer name comes from the estate row; its source is the estate's own
source (the Kemenperin/BAJRA directory or a KEK profile). No role is inferred:
the directory names the developer, so the role is ``developer``. Ownership type
follows the legal form in the source name; the profile note says so.

Run: python scripts/imports/add_estate_developers.py
Then: python scripts/pipeline/validate.py
      python scripts/build_all.py
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_model import (  # noqa: E402
    CURATED,
    ESTATE_FIELDS,
    ORG_FIELDS,
    read_csv,
    write_csv,
)

# Developers whose state ownership is not spelled out in the directory name.
# Keep this list short and explicit; everything else follows the legal form.
STATE_DEVELOPERS = {
    "PT. Bukit Asam",
    "PT. Jakarta Industrial Estate Pulogadung",
    "PT. Kawasan Berikat Nusantara",
    "PT. Kawasan Industri Makassar (KIMA)",
    "PT. Krakatau Sarana Infrastruktur",
    "PT. Pembangunan Aceh",
    "PT. Surabaya Industrial Estate Rungkut",
    "Perumda Manuntu Sukses",
}


def normalise(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = text.encode("ascii", "ignore").decode().lower()
    text = re.sub(r"\b(pt|persero|tbk|cv)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def slug(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = text.encode("ascii", "ignore").decode().lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\b(pt|persero|tbk|cv)\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def org_type(name: str) -> str:
    low = name.casefold()
    if name in STATE_DEVELOPERS:
        return "soe"
    if "(persero)" in low or low.startswith(("perum", "perusahaan umum")):
        return "soe"
    if "badan usaha" in low or "bupp" in low:
        return "other"
    return "private"


def short_name(name: str) -> str:
    text = re.sub(r"^(PT\.?|CV)\s+", "", name, flags=re.I)
    text = re.sub(r",?\s*Tbk\.?$", "", text, flags=re.I)
    text = re.sub(r"\s*\(Persero\)\s*$", "", text, flags=re.I)
    return text.strip() or name


def note_for(kind: str) -> str:
    if kind == "soe":
        return (
            "State-owned estate developer. The developer role comes from the "
            "atlas estate layer; ownership follows the legal form in the source "
            "name."
        )
    if kind == "other":
        return (
            "Estate development body. The developer role comes from the atlas "
            "estate layer; ownership follows the legal form in the source name."
        )
    return (
        "Estate developer. The developer role comes from the atlas estate "
        "layer; ownership follows the legal form in the source name."
    )


def main() -> None:
    estates = read_csv(CURATED / "estates.csv")
    organizations = read_csv(CURATED / "organizations.csv")

    by_name: dict[str, str] = {}
    for org in organizations:
        for field in ("name", "short_name"):
            if org[field]:
                by_name.setdefault(normalise(org[field]), org["id"])

    org_ids = {org["id"] for org in organizations}
    developer_ids: dict[str, str] = {}
    added_orgs = 0
    linked = 0

    for estate in estates:
        if estate["developer_org_id"]:
            continue
        developer = estate["developer"].strip()
        if not developer:
            continue
        key = normalise(developer)
        if key in developer_ids:
            estate["developer_org_id"] = developer_ids[key]
            linked += 1
            continue
        existing = by_name.get(key)
        if existing:
            developer_ids[key] = existing
            estate["developer_org_id"] = existing
            linked += 1
            continue

        base = "org-" + (slug(developer) or "estate-developer")
        org_id = base
        suffix = 2
        while org_id in org_ids:
            org_id = f"{base}-{suffix}"
            suffix += 1

        kind = org_type(developer)
        organizations.append(
            {
                "id": org_id,
                "name": developer,
                "short_name": short_name(developer),
                "org_type": kind,
                "country_code": "ID",
                "parent_id": "",
                "website": "",
                "notes": note_for(kind),
            }
        )
        org_ids.add(org_id)
        developer_ids[key] = org_id
        estate["developer_org_id"] = org_id
        added_orgs += 1
        linked += 1

    organizations.sort(key=lambda row: row["id"])
    write_csv(CURATED / "organizations.csv", ORG_FIELDS, organizations)
    write_csv(CURATED / "estates.csv", ESTATE_FIELDS, estates)

    print(
        f"OK: {added_orgs} new developer profiles, {linked} estates linked, "
        f"{len(organizations)} organisations in total"
    )


if __name__ == "__main__":
    main()
