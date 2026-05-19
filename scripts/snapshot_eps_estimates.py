#!/usr/bin/env python3
"""Monthly EPS Estimates Snapshot Writer.

Reads the DD Screener universe from docs/dd-screener/latest.json and fetches
yfinance earnings_estimate (0y / +1y rows) + info.trailingEps for every ticker,
computing:
  - eps_0y:       current FY consensus EPS avg (kept for audit, not used in CAGR)
  - eps_1y:       next FY consensus EPS avg
  - trailing_eps: info.trailingEps — base for proper 2Y CAGR
  - eps_cagr_2y:  ((eps_1y / trailing_eps) ** 0.5 - 1) * 100  (% annual growth rate)

CAGR caveat (v1.7.1 fix): yfinance's 0y and +1y rows are 1 year apart, not 2.
Using ((eps_1y / eps_0y)**0.5 - 1) is mathematically wrong (halves a 1yr
growth). Proper 2Y CAGR uses trailingEps as base — matches QGM's
eps_cagr_2y_fwd convention (NVDA validated: 52.89% computed vs QGM 52.73%).

Output: docs/dd-screener/eps-estimates-snapshots/{YYYY-MM}.json

Idempotent: re-running in the same calendar month (Taipei timezone) overwrites
the existing monthly file.

Usage:
  python3 scripts/snapshot_eps_estimates.py              # full universe
  python3 scripts/snapshot_eps_estimates.py --dry-run    # no file write
  python3 scripts/snapshot_eps_estimates.py --max-workers 8
  python3 scripts/snapshot_eps_estimates.py --top 10     # smoke-test

Pattern:
  ThreadPoolExecutor(max_workers=4) mirrors build_fundamentals_cache.py:487.
  EU suffix resolution mirrors build_dd_screener.py _yf_ticker_for_ma().
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "-q"])
    import yfinance as yf

logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("peewee").setLevel(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

# Import EU suffix map from the quality module (single source of truth)
try:
    from dd_screener_quality import EU_SUFFIX_MAP
except ImportError:
    EU_SUFFIX_MAP: dict[str, str] = {}

OUTPUT_DIR = ROOT / "docs" / "dd-screener" / "eps-estimates-snapshots"
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"

TAIPEI_TZ = timezone(timedelta(hours=8))


def _yf_ticker_for(dd_ticker: str) -> str:
    """Resolve DD ticker → yfinance ticker (adds EU suffix when needed)."""
    return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}" if dd_ticker in EU_SUFFIX_MAP else dd_ticker


def _fetch_one(dd_ticker: str) -> dict | None:
    """Fetch earnings_estimate + trailingEps for one ticker.

    Returns dict with eps_0y / eps_1y / trailing_eps / eps_cagr_2y, or None on
    total failure. Partial success returns dict with available fields set and
    eps_cagr_2y = None (CAGR requires both trailing_eps + eps_1y).
    """
    yf_ticker = _yf_ticker_for(dd_ticker)
    out: dict = {
        "eps_0y": None,
        "eps_1y": None,
        "trailing_eps": None,
        "eps_cagr_2y": None,
        "yf_fy_label": None,  # for audit
    }
    try:
        tk = yf.Ticker(yf_ticker)
        ee = tk.earnings_estimate
        if ee is None or getattr(ee, "empty", True):
            return None

        for row_label, field in (("0y", "eps_0y"), ("+1y", "eps_1y")):
            try:
                if row_label not in ee.index:
                    continue
                val = ee.loc[row_label].get("avg")
                if val is not None and float(val) > 0:
                    out[field] = round(float(val), 4)
            except Exception:
                continue

        # v1.7.1: fetch trailingEps only if we have eps_1y (saves rate-limit
        # pressure when earnings_estimate already failed).
        if out["eps_1y"] is not None:
            try:
                trailing = tk.info.get("trailingEps")
                if trailing is not None and float(trailing) > 0:
                    out["trailing_eps"] = round(float(trailing), 4)
            except Exception:
                pass

        eps_1y = out["eps_1y"]
        trailing = out["trailing_eps"]

        # v1.7.1: proper 2Y CAGR uses trailingEps as base (1yr forward → +1y
        # estimate; 2yr period; annualized). Wrong formula (eps_1y/eps_0y)^0.5
        # halves the actual growth rate.
        if eps_1y is not None and trailing is not None and trailing > 0:
            cagr = ((eps_1y / trailing) ** 0.5 - 1) * 100
            out["eps_cagr_2y"] = round(cagr, 2)

        # Only return None if we got nothing useful at all
        if out["eps_0y"] is None and out["eps_1y"] is None:
            return None

        return out

    except Exception as exc:
        # Log but don't raise — caller continues with remaining tickers
        print(f"    [snapshot] WARN {dd_ticker}: {exc}", file=sys.stderr)
        return None


def load_universe() -> list[str]:
    """Read ticker list from docs/dd-screener/latest.json."""
    if not LATEST_JSON.exists():
        raise SystemExit(f"ERROR: {LATEST_JSON} not found — run build_dd_screener.py first")
    data = json.loads(LATEST_JSON.read_text(encoding="utf-8"))
    stocks = data.get("stocks") or []
    tickers = [s["ticker"] for s in stocks if s.get("ticker")]
    if not tickers:
        raise SystemExit("ERROR: no tickers found in latest.json")
    return tickers


def snapshot(
    tickers: list[str],
    max_workers: int,
    dry_run: bool,
) -> dict:
    """Run the snapshot for all tickers.

    Returns the full snapshot document (for inspection/testing).
    """
    now = datetime.now(TAIPEI_TZ)
    month_key = now.strftime("%Y-%m")  # e.g. "2026-05"
    captured_at = now.isoformat(timespec="seconds")

    print(f"  Universe: {len(tickers)} tickers")
    print(f"  Month key: {month_key} (Taipei TZ)")
    print(f"  Workers: {max_workers}")
    print(f"  Output: {OUTPUT_DIR / (month_key + '.json')}")
    print()

    t0 = time.time()
    results: dict[str, dict] = {}
    failed: list[str] = []

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_fetch_one, t): t for t in tickers}
        for i, fut in enumerate(as_completed(futs), 1):
            t = futs[fut]
            try:
                row = fut.result(timeout=30)
                if row is not None:
                    results[t] = row
                else:
                    failed.append(t)
            except Exception as exc:
                print(f"    ERR {t}: {exc}", file=sys.stderr)
                failed.append(t)
            if i % 20 == 0 or i == len(futs):
                elapsed = time.time() - t0
                print(f"    [{i:>3}/{len(futs)}] {elapsed:.0f}s — succeeded so far: {len(results)}")

    succeeded = len(results)
    print()
    print(f"  Succeeded: {succeeded}/{len(tickers)}")
    if failed:
        print(f"  Failed ({len(failed)}): {', '.join(failed[:20])}"
              + ("..." if len(failed) > 20 else ""))

    doc = {
        "captured_at": captured_at,
        "for_month": month_key,
        "universe_size": len(tickers),
        "succeeded": succeeded,
        "failed": failed,
        "tickers": results,
    }

    if dry_run:
        print(f"\n  (dry-run) skipping write to {OUTPUT_DIR / (month_key + '.json')}")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / f"{month_key}.json"
        out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Wrote {out_path} ({out_path.stat().st_size:,} bytes)")

    return doc


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true",
                   help="Fetch and compute but don't write file")
    p.add_argument("--max-workers", type=int, default=4,
                   help="Concurrent yfinance fetchers (default 4)")
    p.add_argument("--top", type=int, default=None,
                   help="Limit to first N tickers (smoke test)")
    args = p.parse_args()

    print(f"=== EPS Estimates Snapshot · {datetime.now(TAIPEI_TZ).isoformat(timespec='seconds')} ===\n")

    tickers = load_universe()
    if args.top:
        print(f"  (--top {args.top}: limiting to first {args.top} tickers)")
        tickers = tickers[:args.top]

    if args.dry_run:
        print("  (--dry-run: will fetch but not write)\n")

    doc = snapshot(tickers, max_workers=args.max_workers, dry_run=args.dry_run)

    # Print sample for verification
    sample_tickers = ["JNJ", "NVDA", "V", "TSM"]
    print("\n  Sample output:")
    for t in sample_tickers:
        row = doc["tickers"].get(t)
        if row:
            print(f"    {t}: trailing={row.get('trailing_eps')} eps_0y={row['eps_0y']} "
                  f"eps_1y={row['eps_1y']} eps_cagr_2y={row['eps_cagr_2y']}")
        else:
            print(f"    {t}: (not in results)")


if __name__ == "__main__":
    main()
