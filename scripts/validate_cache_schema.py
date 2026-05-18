#!/usr/bin/env python3
"""Validate docs/cache/{fundamentals,prices}-{us,tw}.json schemas.

Run as:
  python3 scripts/validate_cache_schema.py            # check all 4 if present
  python3 scripts/validate_cache_schema.py --staged   # only validate files in git stage
  python3 scripts/validate_cache_schema.py --file path/to/cache.json  # one file

Pre-commit hook usage (added to .git/hooks/pre-commit):
  if git diff --cached --name-only | grep -q "^docs/cache/.*\\.json"; then
      python3 scripts/validate_cache_schema.py --staged || exit 1
  fi

Exit non-zero on validation failure.
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "docs" / "cache"

EXPECTED_SCHEMA_VERSION = "1.0"

# Top-level keys every cache file must have
TOP_LEVEL_KEYS = {
    "schema_version", "region", "as_of", "run_timestamp",
    "universe_size", "source_breakdown", "health",
    "failed_tickers", "tickers",
}

# Per-ticker required nested keys
FUNDAMENTALS_REQUIRED_KEYS = {
    "currency", "quality", "eps_estimate", "info", "growth", "margins",
    "trends", "quarterly", "quality_source", "fetched_at",
}
PRICES_REQUIRED_KEYS = {"currency", "source"}

FUNDAMENTALS_QUALITY_FIELDS = {"fcf", "roic", "eps2y", "peg", "de"}
FUNDAMENTALS_EPS_FIELDS = {"fy0", "fy1"}


def _staged_cache_files() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, check=True,
        )
    except Exception:
        return []
    return [ROOT / line for line in out.stdout.splitlines()
            if line.startswith("docs/cache/") and line.endswith(".json")]


def _validate_top_level(data: dict, path: Path) -> list[str]:
    errs = []
    missing = TOP_LEVEL_KEYS - set(data.keys())
    if missing:
        errs.append(f"top-level missing keys: {sorted(missing)}")
    if data.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        errs.append(f"schema_version={data.get('schema_version')!r} ≠ "
                    f"expected {EXPECTED_SCHEMA_VERSION!r}")
    if data.get("region") not in ("us", "tw", "jp"):
        errs.append(f"region={data.get('region')!r} not in (us, tw, jp)")
    if not isinstance(data.get("tickers"), dict):
        errs.append(f"tickers must be dict, got {type(data.get('tickers')).__name__}")
    return errs


def _validate_fundamentals(data: dict, path: Path) -> list[str]:
    errs = _validate_top_level(data, path)
    tickers = data.get("tickers", {})
    if not isinstance(tickers, dict):
        return errs

    # Sample 10 tickers
    sample_keys = random.sample(list(tickers.keys()), min(10, len(tickers)))
    for t in sample_keys:
        row = tickers[t]
        if not isinstance(row, dict):
            errs.append(f"  {t}: not a dict")
            continue
        missing = FUNDAMENTALS_REQUIRED_KEYS - set(row.keys())
        if missing:
            errs.append(f"  {t}: missing keys {sorted(missing)}")
        # Quality should be 5-field dict
        q = row.get("quality") or {}
        q_missing = FUNDAMENTALS_QUALITY_FIELDS - set(q.keys())
        if q_missing:
            errs.append(f"  {t}.quality: missing {sorted(q_missing)}")
        # EPS estimate
        eps = row.get("eps_estimate") or {}
        eps_missing = FUNDAMENTALS_EPS_FIELDS - set(eps.keys())
        if eps_missing:
            errs.append(f"  {t}.eps_estimate: missing {sorted(eps_missing)}")
        # Currency
        ccy = row.get("currency")
        if ccy not in ("USD", "TWD", "EUR", "JPY", "GBP", "HKD", "CNY"):
            errs.append(f"  {t}: currency={ccy!r} not in supported set")
    return errs


def _validate_prices(data: dict, path: Path) -> list[str]:
    errs = _validate_top_level(data, path)
    tickers = data.get("tickers", {})
    if not isinstance(tickers, dict):
        return errs

    # Prices files have an indices block (not in TOP_LEVEL_KEYS spec)
    if "indices" not in data:
        errs.append("prices file missing 'indices' top-level key")

    sample_keys = random.sample(list(tickers.keys()), min(10, len(tickers)))
    for t in sample_keys:
        row = tickers[t]
        if not isinstance(row, dict):
            errs.append(f"  {t}: not a dict")
            continue
        missing = PRICES_REQUIRED_KEYS - set(row.keys())
        if missing:
            errs.append(f"  {t}: missing keys {sorted(missing)}")
        # price must be numeric (or null)
        p = row.get("price")
        if p is not None and not isinstance(p, (int, float)):
            errs.append(f"  {t}: price has type {type(p).__name__}, expected float/int/null")
    return errs


def validate_file(path: Path) -> bool:
    if not path.exists():
        print(f"  SKIP {path}: file not found", file=sys.stderr)
        return True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"  FAIL {path}: cannot parse JSON: {e}", file=sys.stderr)
        return False

    name = path.name
    if name.startswith("fundamentals-"):
        errs = _validate_fundamentals(data, path)
    elif name.startswith("prices-"):
        errs = _validate_prices(data, path)
    else:
        print(f"  SKIP {path}: unknown cache type", file=sys.stderr)
        return True

    if errs:
        print(f"  FAIL {path}:", file=sys.stderr)
        for e in errs:
            print(f"    {e}", file=sys.stderr)
        return False
    print(f"  ✓ {path.name}: {len(data.get('tickers', {}))} tickers, "
          f"schema_version={data['schema_version']}, region={data['region']}, "
          f"health={data['health']['status']}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--staged", action="store_true",
                    help="Only validate cache files currently staged in git")
    ap.add_argument("--file", type=Path, action="append", default=[],
                    help="Validate specific file(s)")
    args = ap.parse_args()

    if args.staged:
        files = _staged_cache_files()
        if not files:
            print("  No staged cache files — nothing to validate")
            return 0
    elif args.file:
        files = args.file
    else:
        files = sorted(CACHE_DIR.glob("*.json"))

    if not files:
        print("  No cache files found")
        return 0

    print(f"Validating {len(files)} cache file(s)...")
    all_ok = True
    for p in files:
        if not validate_file(p):
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
