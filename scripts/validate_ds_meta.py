#!/usr/bin/env python3
"""Validate <script id="ds-meta"> JSON blocks in industry DS HTML files.

Mirror of validate_id_meta.py for the industry-ds skill output. The DS schema
shares all sector-taxonomy / enum / ticker-depth validation with ID, but adds
DS-specific fields:

  - ds_version (replaces id_version)
  - history_window_years (int, 1-200): how far back §1 reviews
  - forecast_horizon_years (int, 1-30): how far §6 projects
  - related_ids: optional list of ID stems (e.g., "ID_HBMSupplyDemand_20260419")

We import TAXONOMY / ENUM_FIELDS / NUMERIC_RANGES / TICKER_DEPTH_ALLOWED /
regex patterns directly from validate_id_meta to ensure a single source of
truth — DS uses the same mega × sub_group whitelist as ID by design.

Usage:
  python scripts/validate_ds_meta.py            # strict: exit 1 on any issue
  python scripts/validate_ds_meta.py --report   # exit 0 always
  python scripts/validate_ds_meta.py FILE...    # specific files
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Single source of truth: share taxonomy + enum constants with ID validator.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_id_meta import (  # noqa: E402
    TAXONOMY,
    ENUM_FIELDS as ID_ENUM_FIELDS,
    NUMERIC_RANGES as ID_NUMERIC_RANGES,
    TICKER_DEPTH_ALLOWED,
    DATE_RE,
    SKILL_VERSION_RE,
    ONELINER_HARD_CAP,
)

ROOT = Path(__file__).resolve().parent.parent
DS_DIR = ROOT / "docs" / "ds"

DS_META_RE = re.compile(
    r'<script\s+id="ds-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
DS_VERSION_TAG_RE = re.compile(
    r'<meta\s+name="ds-skill-version"\s+content="([^"]+)"', re.IGNORECASE
)
DS_VERSION_RE = re.compile(r"^v\d+\.\d+(?:\.\d+)?$")

# DS-specific required fields (ds_version replaces id_version).
REQUIRED_FIELDS = {
    "theme": str,
    "skill_version": str,
    "ds_version": str,
    "publish_date": str,
    "thesis_type": str,
    "ai_exposure": str,
    "oneliner": str,
    "related_tickers": list,
}

# Reuse ID enum whitelist (thesis_type / ai_exposure / quality_tier / etc).
ENUM_FIELDS = dict(ID_ENUM_FIELDS)

# DS-specific numeric ranges (windows / horizons).
NUMERIC_RANGES = dict(ID_NUMERIC_RANGES)
NUMERIC_RANGES["history_window_years"] = (1, 200)
NUMERIC_RANGES["forecast_horizon_years"] = (1, 30)

# Related ID stems should match the canonical ID filename pattern.
RELATED_ID_RE = re.compile(r"^ID_[A-Za-z0-9]+_\d{8}$")


def validate_meta(meta: dict) -> list:
    """Return a list of error strings; empty list means valid."""
    errs: list = []

    # Required fields + type check
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in meta:
            errs.append(f"missing required field: {field}")
            continue
        v = meta[field]
        if v is None:
            errs.append(f"{field}: must not be null")
            continue
        if not isinstance(v, expected_type):
            errs.append(
                f"{field}: expected {expected_type.__name__}, got {type(v).__name__}"
            )

    # Enum fields
    for field, allowed in ENUM_FIELDS.items():
        v = meta.get(field)
        if v is not None and v not in allowed:
            errs.append(
                f"{field}: invalid value {v!r}; allowed {sorted(allowed)}"
            )

    # Format checks
    if "publish_date" in meta and not DATE_RE.match(str(meta["publish_date"])):
        errs.append(f"publish_date: must be YYYY-MM-DD, got {meta['publish_date']!r}")
    if "skill_version" in meta and not SKILL_VERSION_RE.match(str(meta["skill_version"])):
        errs.append(f"skill_version: must match vN.N, got {meta['skill_version']!r}")
    if "ds_version" in meta and not DS_VERSION_RE.match(str(meta["ds_version"])):
        errs.append(f"ds_version: must match vN.N, got {meta['ds_version']!r}")

    # Numeric ranges
    for field, (lo, hi) in NUMERIC_RANGES.items():
        v = meta.get(field)
        if isinstance(v, (int, float)) and not (lo <= v <= hi):
            errs.append(f"{field}: {v} out of range [{lo}, {hi}]")

    # Integer-only check on the new horizon fields
    for field in ("history_window_years", "forecast_horizon_years"):
        v = meta.get(field)
        if v is not None and not isinstance(v, int):
            errs.append(
                f"{field}: must be int (years), got {type(v).__name__}"
            )

    # Oneliner cap
    one = meta.get("oneliner")
    if isinstance(one, str) and len(one) > ONELINER_HARD_CAP:
        errs.append(f"oneliner: {len(one)} chars exceeds hard cap {ONELINER_HARD_CAP}")

    # related_tickers entries (same shape as ID)
    rt = meta.get("related_tickers")
    if isinstance(rt, list):
        if len(rt) == 0:
            errs.append(
                "related_tickers: must contain ≥ 1 entry "
                "(use empty array only for cross-cutting themes)"
            )
        for i, t in enumerate(rt):
            if not isinstance(t, dict):
                errs.append(
                    f"related_tickers[{i}]: must be object, "
                    f"got {type(t).__name__}"
                )
                continue
            for key in ("ticker", "role", "depth", "beneficiary"):
                if key not in t:
                    errs.append(f"related_tickers[{i}].{key}: required key missing")
            if "depth" in t and t["depth"] not in TICKER_DEPTH_ALLOWED:
                errs.append(
                    f"related_tickers[{i}].depth: invalid {t['depth']!r}, "
                    f"allowed {sorted(TICKER_DEPTH_ALLOWED)}"
                )
            if "beneficiary" in t and not isinstance(t["beneficiary"], bool):
                errs.append(
                    f"related_tickers[{i}].beneficiary: must be bool, "
                    f"got {type(t['beneficiary']).__name__}"
                )

    # related_ids (DS-specific): optional list of "ID_{Theme}_{YYYYMMDD}" stems
    ri = meta.get("related_ids")
    if ri is not None:
        if not isinstance(ri, list):
            errs.append(
                f"related_ids: must be list of ID stems, got {type(ri).__name__}"
            )
        else:
            for i, s in enumerate(ri):
                if not isinstance(s, str) or not RELATED_ID_RE.match(s):
                    errs.append(
                        f"related_ids[{i}]: must match 'ID_<Theme>_<YYYYMMDD>', "
                        f"got {s!r}"
                    )

    # sections_refreshed (optional, DS uses different freshness buckets than ID)
    sr = meta.get("sections_refreshed")
    if isinstance(sr, dict):
        allowed_buckets = {"history", "supply_demand", "forecast"}
        for k in sr:
            if k not in allowed_buckets:
                errs.append(
                    f"sections_refreshed: unknown key {k!r}; "
                    f"allowed {sorted(allowed_buckets)}"
                )
            if not DATE_RE.match(str(sr[k])):
                errs.append(f"sections_refreshed.{k}: must be YYYY-MM-DD")

    # mega + sub_group taxonomy (shared with ID; required for DS — no soft warning)
    mega = meta.get("mega")
    sub_group = meta.get("sub_group")
    if mega is None and sub_group is None:
        errs.append(
            "mega + sub_group: both required for DS "
            "(use the same whitelist as ID — see docs/id/taxonomy.md)"
        )
    else:
        if not isinstance(mega, str) or mega not in TAXONOMY:
            errs.append(
                f"mega: invalid value {mega!r}; "
                f"must be one of {sorted(TAXONOMY.keys())}"
            )
        elif not isinstance(sub_group, str) or sub_group not in TAXONOMY[mega]:
            errs.append(
                f"sub_group: invalid value {sub_group!r} for mega={mega!r}; "
                f"must be one of {sorted(TAXONOMY[mega])}"
            )

    return errs


def validate_file(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {"status": "read_error", "errors": [str(e)]}

    has_skill_meta = bool(DS_VERSION_TAG_RE.search(text))
    if not has_skill_meta:
        return {"status": "non_ds"}  # not an industry-ds output

    meta_m = DS_META_RE.search(text)
    if not meta_m:
        return {
            "status": "missing_block",
            "errors": ['no <script id="ds-meta"> found in <head>'],
        }

    raw = meta_m.group(1).strip()
    try:
        meta = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"status": "parse_error", "errors": [f"JSON parse error: {e}"]}

    errs = validate_meta(meta)
    if errs:
        return {"status": "invalid", "errors": errs, "theme": meta.get("theme")}
    return {"status": "ok", "theme": meta.get("theme")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--json", dest="json_out", action="store_true")
    args = parser.parse_args()

    targets = [Path(p) for p in args.files] if args.files else sorted(
        DS_DIR.glob("DS_*.html")
    )

    results = [{"file": p.name, **validate_file(p)} for p in targets]

    if args.json_out:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        bad = any(r["status"] not in ("ok", "non_ds") for r in results)
        sys.exit(0 if (args.report or not bad) else 1)

    counts: dict = {"ok": 0, "non_ds": 0, "missing_block": 0, "parse_error": 0, "invalid": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    print(f"Scanned {len(results)} DS file(s):")
    print(f"  ✅ ok                : {counts['ok']}")
    print(f"  ⚠  missing ds-meta  : {counts.get('missing_block', 0)}")
    print(f"  ❌ JSON parse error : {counts.get('parse_error', 0)}")
    print(f"  ❌ validation error : {counts.get('invalid', 0)}")
    print(f"  ↪  non-DS (skipped) : {counts.get('non_ds', 0)}")

    bad = [r for r in results if r["status"] in ("missing_block", "parse_error", "invalid")]
    if bad:
        print()
        for r in bad:
            theme = r.get("theme", "?")
            print(f"\n[{r['status'].upper()}] {r['file']} (theme={theme})")
            for e in r.get("errors", []):
                print(f"    - {e}")

    if bad and not args.report:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
