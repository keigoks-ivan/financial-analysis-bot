#!/usr/bin/env python3
"""Monthly EPS Estimates Snapshot Writer (v2: Excel-first).

Builds a monthly snapshot from the EPS estimates Excel export (data/eps-estimates/)
as the primary source. For DD tickers NOT covered by Excel (e.g. .TW / .T),
falls back to yfinance earnings_estimate + trailingEps.

Snapshot schema (one row per ticker):
  - eps_fy_curr:  FY1 EPS estimate     (Excel FY1E or yfinance 0y)
  - eps_fy_next:  FY2 EPS estimate     (Excel FY2E or yfinance +1y)
  - eps_fy3:      FY3 EPS estimate     (Excel FY3E; null for yfinance fallback)
  - trailing_eps: yfinance trailingEps (always from yfinance — Excel has no TTM)
  - eps_cagr_2y:  ((eps_fy_next / trailing_eps) ** 0.5 - 1) × 100
  - source:       "xlsx" or "yfinance"
  - eps_0y:       legacy alias = eps_fy_curr (kept for back-compat)
  - eps_1y:       legacy alias = eps_fy_next
  - yf_fy_label:  null for xlsx; "+1y" or "+2y" for yfinance (audit)

Top-level keys:
  for_month, snapshot_date, captured_at, source ("xlsx"/"yfinance"/"mixed"),
  source_file, universe_size, xlsx_covered, yfinance_fetched, failed.

Output: docs/dd-screener/eps-estimates-snapshots/{YYYY-MM}.json
  Month key is derived from the Excel snapshot_date (NOT wall-clock), so re-
  running with the same Excel always overwrites the same monthly file.

Usage:
  python3 scripts/snapshot_eps_estimates.py              # use latest Excel
  python3 scripts/snapshot_eps_estimates.py --month 2026-04   # specific month
  python3 scripts/snapshot_eps_estimates.py --dry-run
  python3 scripts/snapshot_eps_estimates.py --max-workers 8

Pattern:
  ThreadPoolExecutor(max_workers=4) mirrors build_fundamentals_cache.py.
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

try:
    from dd_screener_quality import EU_SUFFIX_MAP
except ImportError:
    EU_SUFFIX_MAP: dict[str, str] = {}

from load_eps_estimates_xlsx import (
    ExcelSnapshot,
    find_excel_for_month,
    find_latest_excel,
    load_excel,
)

OUTPUT_DIR = ROOT / "docs" / "dd-screener" / "eps-estimates-snapshots"
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"

TAIPEI_TZ = timezone(timedelta(hours=8))


def _yf_ticker_for(dd_ticker: str) -> str:
    return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}" if dd_ticker in EU_SUFFIX_MAP else dd_ticker


def _fetch_yf_one(dd_ticker: str) -> dict | None:
    """Fetch yfinance fallback: 0y / +1y / +2y rows + trailingEps."""
    yf_ticker = _yf_ticker_for(dd_ticker)
    out: dict = {
        "eps_fy_curr": None,
        "eps_fy_next": None,
        "eps_fy3": None,
        "trailing_eps": None,
        "eps_cagr_2y": None,
        "source": "yfinance",
        "yf_fy_label": None,
    }
    try:
        tk = yf.Ticker(yf_ticker)
        ee = tk.earnings_estimate
        if ee is None or getattr(ee, "empty", True):
            return None

        for row_label, field in (("0y", "eps_fy_curr"),
                                  ("+1y", "eps_fy_next"),
                                  ("+2y", "eps_fy3")):
            try:
                if row_label not in ee.index:
                    continue
                val = ee.loc[row_label].get("avg")
                if val is not None and float(val) > 0:
                    out[field] = round(float(val), 4)
            except Exception:
                continue

        if out["eps_fy_next"] is not None:
            try:
                trailing = tk.info.get("trailingEps")
                if trailing is not None and float(trailing) > 0:
                    out["trailing_eps"] = round(float(trailing), 4)
            except Exception:
                pass

        if out["eps_fy_next"] is not None and out["trailing_eps"]:
            cagr = ((out["eps_fy_next"] / out["trailing_eps"]) ** 0.5 - 1) * 100
            out["eps_cagr_2y"] = round(cagr, 2)

        if out["eps_fy_curr"] is None and out["eps_fy_next"] is None:
            return None
        return out
    except Exception as exc:
        print(f"    [snapshot] WARN {dd_ticker}: {exc}", file=sys.stderr)
        return None


def _fetch_trailing_only(dd_ticker: str) -> float | None:
    """For Excel-covered tickers we still need trailing_eps from yfinance to
    compute eps_cagr_2y (Excel has no TTM)."""
    yf_ticker = _yf_ticker_for(dd_ticker)
    try:
        tk = yf.Ticker(yf_ticker)
        trailing = tk.info.get("trailingEps")
        if trailing is not None and float(trailing) > 0:
            return round(float(trailing), 4)
    except Exception:
        pass
    return None


def load_universe() -> list[str]:
    if not LATEST_JSON.exists():
        raise SystemExit(f"ERROR: {LATEST_JSON} not found — run build_dd_screener.py first")
    data = json.loads(LATEST_JSON.read_text(encoding="utf-8"))
    stocks = data.get("stocks") or []
    tickers = [s["ticker"] for s in stocks if s.get("ticker")]
    if not tickers:
        raise SystemExit("ERROR: no tickers found in latest.json")
    return tickers


def snapshot_from_excel(
    excel: ExcelSnapshot,
    universe: list[str],
    max_workers: int,
    dry_run: bool,
) -> dict:
    """Build monthly snapshot, Excel-first."""
    # Month key from Excel snapshot_date (YYYY-MM-DD → YYYY-MM)
    month_key = excel.snapshot_date[:7] if len(excel.snapshot_date) >= 7 else "unknown"
    captured_at = datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")

    xlsx_tickers = [t for t in universe if excel.has(t)]
    yf_tickers = [t for t in universe if not excel.has(t)]

    print(f"  Excel snapshot date: {excel.snapshot_date} → month_key={month_key}")
    print(f"  Universe: {len(universe)} (Excel covers {len(xlsx_tickers)}, yfinance fallback {len(yf_tickers)})")
    print(f"  Source file: {excel.source_file}")
    print()

    results: dict[str, dict] = {}
    failed: list[str] = []

    # Excel rows: build records + fetch trailing_eps from yfinance for CAGR
    t0 = time.time()
    print(f"  Fetching trailingEps from yfinance for {len(xlsx_tickers)} Excel tickers...")
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_fetch_trailing_only, t): t for t in xlsx_tickers}
        trailing_map: dict[str, float | None] = {}
        for i, fut in enumerate(as_completed(futs), 1):
            t = futs[fut]
            try:
                trailing_map[t] = fut.result(timeout=20)
            except Exception:
                trailing_map[t] = None
            if i % 30 == 0 or i == len(futs):
                elapsed = time.time() - t0
                print(f"    [{i:>3}/{len(futs)}] {elapsed:.0f}s")

    for t in xlsx_tickers:
        rec = excel.get(t) or {}
        fy1 = rec.get("fy1")
        fy2 = rec.get("fy2")
        fy3 = rec.get("fy3")
        trailing = trailing_map.get(t)
        cagr = None
        if fy2 is not None and trailing and trailing > 0:
            cagr = round(((fy2 / trailing) ** 0.5 - 1) * 100, 2)
        results[t] = {
            "eps_fy_curr": fy1,
            "eps_fy_next": fy2,
            "eps_fy3": fy3,
            "trailing_eps": trailing,
            "eps_cagr_2y": cagr,
            "source": "xlsx",
            "yf_fy_label": None,
            # legacy aliases for back-compat with build_dd_screener's
            # _compute_eps_revision which reads eps_cagr_2y
            "eps_0y": fy1,
            "eps_1y": fy2,
        }

    # yfinance fallback for non-Excel tickers
    if yf_tickers:
        print(f"\n  yfinance fallback for {len(yf_tickers)} tickers...")
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futs = {ex.submit(_fetch_yf_one, t): t for t in yf_tickers}
            for i, fut in enumerate(as_completed(futs), 1):
                t = futs[fut]
                try:
                    row = fut.result(timeout=30)
                    if row is not None:
                        # legacy aliases
                        row["eps_0y"] = row["eps_fy_curr"]
                        row["eps_1y"] = row["eps_fy_next"]
                        results[t] = row
                    else:
                        failed.append(t)
                except Exception as exc:
                    print(f"    ERR {t}: {exc}", file=sys.stderr)
                    failed.append(t)
                if i % 5 == 0 or i == len(futs):
                    elapsed = time.time() - t0
                    print(f"    [{i:>3}/{len(futs)}] {elapsed:.0f}s")

    print()
    print(f"  Succeeded: {len(results)}/{len(universe)}")
    print(f"  xlsx rows: {len(xlsx_tickers)}, yfinance rows: {len(results) - len(xlsx_tickers)}, failed: {len(failed)}")
    if failed:
        print(f"  Failed: {', '.join(failed[:20])}" + ("..." if len(failed) > 20 else ""))

    doc = {
        "captured_at": captured_at,
        "for_month": month_key,
        "snapshot_date": excel.snapshot_date,
        "source": "mixed" if (xlsx_tickers and yf_tickers) else ("xlsx" if xlsx_tickers else "yfinance"),
        "source_file": excel.source_file,
        "universe_size": len(universe),
        "xlsx_covered": len(xlsx_tickers),
        "yfinance_fetched": len(results) - len(xlsx_tickers),
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
    p.add_argument("--month", help="YYYY-MM — pin to specific Excel; default = latest")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--max-workers", type=int, default=4)
    p.add_argument("--skip-trailing", action="store_true",
                   help="Skip yfinance trailingEps fetch (eps_cagr_2y will be null)")
    args = p.parse_args()

    print(f"=== EPS Estimates Snapshot · {datetime.now(TAIPEI_TZ).isoformat(timespec='seconds')} ===\n")

    if args.month:
        path = find_excel_for_month(args.month)
        if path is None:
            raise SystemExit(f"ERROR: no Excel found for month {args.month} in data/eps-estimates/")
    else:
        path = find_latest_excel()
        if path is None:
            raise SystemExit("ERROR: no Excel found in data/eps-estimates/ — "
                             "place DD_universe_EPS_estimates_YYYYMMDD.xlsx there first")

    excel = load_excel(path)
    universe = load_universe()

    if args.skip_trailing:
        # Force trailing-fetch to skip (testing): patch the function
        global _fetch_trailing_only
        _fetch_trailing_only = lambda t: None

    snapshot_from_excel(excel, universe, max_workers=args.max_workers, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
