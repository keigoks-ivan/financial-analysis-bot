#!/usr/bin/env python3
"""Validate <script id="dd-meta"> JSON blocks across all v12+ DD HTML files.

Purpose: enforce a stable contract between stock-analyst skill output and
downstream consumers (research index, portfolio-manager skill,
morning-briefing). Run in CI / pre-commit to fail PRs that introduce broken
or incomplete dd-meta blocks.

Usage:
  python scripts/validate_dd_meta.py            # strict: exit 1 on any issue
  python scripts/validate_dd_meta.py --report   # exit 0 always; print issues
  python scripts/validate_dd_meta.py --json     # machine-readable output
  python scripts/validate_dd_meta.py FILE...    # validate specific files only
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DD_DIR = ROOT / "docs" / "dd"

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
META_VERSION_RE = re.compile(
    r'<meta\s+name="dd-schema-version"\s+content="([^"]+)"', re.IGNORECASE
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SCHEMA_RE = re.compile(r"^v12\.\d+$")

# Required fields with their expected Python types (after json.loads).
# Keys present here MUST appear in every v12 dd-meta block.
REQUIRED_FIELDS = {
    "ticker": str,
    "schema": str,
    "date": str,
    "price_at_dd": (int, float),
    "signal": str,
    "trap": str,
    "trap_label": str,
    "moat": str,
    "val": str,
    "ma": str,
    "fpe_fy2": (int, float),
    "pct_5y": (int, float),
    "peg_fy2": (int, float),
    "upside_short_pct": (int, float),
    "upside_mid_pct": (int, float),
    "stress": dict,
    "moat_score": (int, float),
    "growth_durability": (int, float),
    "quality_score": (int, float),
    "ai_risk": str,
    "long_term_confidence": str,
    "verdict": str,
    "oneliner": str,
}

ENUM_FIELDS = {
    "signal": {"A+", "A", "B", "C", "X"},
    "trap": {"🟢", "🟡", "🔴"},
    "moat": {"S", "A", "B", "C", "X"},
    "val": {"🟢", "🟡", "🟠", "🔴"},
    "ma": {"🟢", "✅", "🟡", "🟠", "❌", "-"},
    "ai_risk": {"🟢", "🟡", "🔴"},
    "long_term_confidence": {"高", "中", "低"},
}

NUMERIC_RANGES = {
    "moat_score": (1, 10),
    "growth_durability": (1, 10),
    "quality_score": (1, 10),
    "pct_5y": (0, 100),
}

ONELINER_HARD_CAP = 200  # hard cap; ≤ 120 is the soft target per skill spec


def validate_meta(meta: dict) -> list:
    """Return list of error strings; empty list = valid."""
    errs = []

    # Required fields: presence + type
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in meta:
            errs.append(f"missing required field: {field}")
            continue
        v = meta[field]
        if v is None:
            errs.append(f"{field}: must not be null (omit field instead)")
            continue
        if not isinstance(v, expected_type):
            type_name = (
                expected_type.__name__
                if isinstance(expected_type, type)
                else " or ".join(t.__name__ for t in expected_type)
            )
            errs.append(
                f"{field}: expected {type_name}, got {type(v).__name__} ({v!r})"
            )

    # Enum: allowed values only
    for field, allowed in ENUM_FIELDS.items():
        v = meta.get(field)
        if v is not None and v not in allowed:
            errs.append(
                f"{field}: invalid value {v!r}; allowed: {sorted(allowed)}"
            )

    # Date format
    date_v = meta.get("date")
    if isinstance(date_v, str) and not DATE_RE.match(date_v):
        errs.append(f"date: format must be YYYY-MM-DD, got {date_v!r}")

    # Schema format
    schema_v = meta.get("schema")
    if isinstance(schema_v, str) and not SCHEMA_RE.match(schema_v):
        errs.append(f"schema: must match v12.X (e.g. v12.0), got {schema_v!r}")

    # Numeric ranges
    for field, (lo, hi) in NUMERIC_RANGES.items():
        v = meta.get(field)
        if isinstance(v, (int, float)) and not (lo <= v <= hi):
            errs.append(f"{field}: {v} out of range [{lo}, {hi}]")

    # Stress object structure
    stress = meta.get("stress")
    if isinstance(stress, dict):
        for k in ("pass", "total"):
            if k not in stress:
                errs.append(f"stress.{k}: required key missing")
            elif not isinstance(stress[k], int):
                errs.append(
                    f"stress.{k}: must be int, got {type(stress[k]).__name__}"
                )
        if "pass" in stress and "total" in stress:
            if stress["total"] <= 0:
                errs.append(f"stress.total: must be > 0, got {stress['total']}")
            if stress["pass"] < 0 or (
                stress["total"] > 0 and stress["pass"] > stress["total"]
            ):
                errs.append(
                    f"stress: pass {stress['pass']} > total {stress['total']}"
                )

    # Oneliner hard cap (soft cap 120 is documented in skill, hard cap here)
    one = meta.get("oneliner")
    if isinstance(one, str) and len(one) > ONELINER_HARD_CAP:
        errs.append(
            f"oneliner: {len(one)} chars exceeds hard cap {ONELINER_HARD_CAP}"
        )

    return errs


def validate_file(path: Path) -> dict:
    """Inspect one DD HTML; return {status, errors[, meta_keys]}.

    status:
      - "non_v12": meta tag missing or not v12 (skipped from CI)
      - "missing_block": v12 DD without <script id="dd-meta">
      - "parse_error": JSON could not be parsed
      - "invalid": JSON parsed but failed validation
      - "ok": fully valid
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {"status": "read_error", "errors": [f"OSError: {e}"]}

    version_m = META_VERSION_RE.search(text)
    version = version_m.group(1) if version_m else ""
    if not version.startswith("v12"):
        return {"status": "non_v12", "version": version}

    meta_m = DD_META_RE.search(text)
    if not meta_m:
        return {
            "status": "missing_block",
            "errors": ["no <script id=\"dd-meta\"> found in <head>"],
        }

    raw = meta_m.group(1).strip()
    try:
        meta = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"status": "parse_error", "errors": [f"JSON parse error: {e}"]}

    errs = validate_meta(meta)
    if errs:
        return {"status": "invalid", "errors": errs, "ticker": meta.get("ticker")}
    return {"status": "ok", "ticker": meta.get("ticker")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files", nargs="*", help="Specific DD HTML files (default: all in docs/dd/)"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Always exit 0; just report issues (for diagnostic / backfill flow).",
    )
    parser.add_argument(
        "--json", dest="json_out", action="store_true", help="JSON output."
    )
    args = parser.parse_args()

    if args.files:
        targets = [Path(p) for p in args.files]
    else:
        targets = sorted(DD_DIR.glob("DD_*.html"))

    results = []
    for p in targets:
        r = validate_file(p)
        r["file"] = p.name
        results.append(r)

    if args.json_out:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        bad = any(r["status"] not in ("ok", "non_v12") for r in results)
        sys.exit(0 if (args.report or not bad) else 1)

    # Plain-text summary
    counts = {"ok": 0, "non_v12": 0, "missing_block": 0, "parse_error": 0, "invalid": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    print(f"Scanned {len(results)} DD file(s):")
    print(f"  ✅ ok                : {counts['ok']}")
    print(f"  ⚠  missing dd-meta  : {counts.get('missing_block', 0)}")
    print(f"  ❌ JSON parse error : {counts.get('parse_error', 0)}")
    print(f"  ❌ validation error : {counts.get('invalid', 0)}")
    print(f"  ↪  non-v12 (skipped): {counts.get('non_v12', 0)}")

    # Detailed report
    bad_statuses = ("missing_block", "parse_error", "invalid")
    bad = [r for r in results if r["status"] in bad_statuses]
    if bad:
        print()
        print("=" * 70)
        for r in bad:
            ticker = r.get("ticker", "?")
            print(f"\n[{r['status'].upper()}] {r['file']} (ticker={ticker})")
            for e in r.get("errors", []):
                print(f"    - {e}")

    if bad and not args.report:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
