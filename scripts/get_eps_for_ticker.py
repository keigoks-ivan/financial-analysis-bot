#!/usr/bin/env python3
"""Lookup EPS estimates from the monthly Excel for a single ticker.

Designed for stock-analyst (DD) and deep-conviction-analyst (DCA) skills to
call BEFORE doing valuation modeling — pulls the buy-side standard Koyfin /
Excel consensus FY1 / FY2 / FY3 + growth + CAGR + snapshot date, so the
analyst can anchor §13 (DD) / Phase C (DCA) on the same numbers the dd-screener
uses.

Alias-aware: 2330.TW → looks up '2330' in Excel; ASML → 'ASML'.

Usage:
  python3 scripts/get_eps_for_ticker.py AAPL
  python3 scripts/get_eps_for_ticker.py 2330.TW
  python3 scripts/get_eps_for_ticker.py NVDA --json   # machine-readable

Exit codes:
  0 — ticker found, EPS printed
  1 — ticker not in Excel (caller should fall back to WebSearch / yfinance)
  2 — Excel file not found (data/eps-estimates/ empty)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from load_eps_estimates_xlsx import load_latest_excel


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ticker", help="Ticker to look up (US/ADR or 2330.TW / 6857.T)")
    ap.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = ap.parse_args()

    snap = load_latest_excel()
    if snap is None:
        print("ERROR: No Excel found in data/eps-estimates/. "
              "Run: cp ~/Downloads/DD_universe_EPS_estimates_YYYYMMDD.xlsx data/eps-estimates/",
              file=sys.stderr)
        return 2

    rec = snap.get(args.ticker)
    if rec is None:
        if args.json:
            print(json.dumps({"ticker": args.ticker, "covered": False,
                              "snapshot_date": snap.snapshot_date,
                              "source_file": snap.source_file}, ensure_ascii=False))
        else:
            print(f"{args.ticker}: NOT in Excel (snapshot {snap.snapshot_date}, "
                  f"source {snap.source_file})")
            print("  → fall back to WebSearch / yfinance for EPS estimates.")
        return 1

    if args.json:
        payload = {
            "ticker": args.ticker,
            "covered": True,
            "snapshot_date": snap.snapshot_date,
            "source_file": snap.source_file,
            **rec,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    # v1.8.5: for foreign listings (.TW/.T/.HK/.KS/.SS/.SZ), surface the
    # native-currency values (TWD/JPY/etc.) so DD/DCA analysts see local-currency
    # numbers directly. PRIMARY source = latest.json's stored eps_fx_rate
    # (computed during each build_dd_screener run — stable, no live API call).
    # FALLBACK = live yfinance fetch (used when latest.json absent or stale).
    _FOREIGN_SUFFIXES = (".TW", ".T", ".HK", ".KS", ".KQ", ".SS", ".SZ", ".JP")
    local_ccy = None
    fx = None
    fx_source = None
    if any(args.ticker.endswith(s) for s in _FOREIGN_SUFFIXES):
        # Primary: read from latest.json (no API call, immune to rate limits)
        latest_json = ROOT / "docs" / "dd-screener" / "latest.json"
        if latest_json.exists():
            try:
                latest = json.loads(latest_json.read_text(encoding="utf-8"))
                row = next((x for x in latest.get("stocks", []) if x.get("ticker") == args.ticker), None)
                if row and row.get("eps_fx_rate") and row.get("eps_display_currency"):
                    fx = row["eps_fx_rate"]
                    local_ccy = row["eps_display_currency"]
                    fx_source = f"latest.json (build {latest.get('as_of', '?')})"
            except Exception:
                pass
        # Fallback: live yfinance fetch
        if fx is None:
            try:
                import warnings
                warnings.filterwarnings("ignore")
                import yfinance as yf
                tk = yf.Ticker(args.ticker)
                ee = tk.earnings_estimate
                yf_0y_avg = None
                if ee is not None and not getattr(ee, "empty", True) and "0y" in ee.index:
                    v = ee.loc["0y"].get("avg")
                    if v is not None and float(v) > 0:
                        yf_0y_avg = float(v)
                xlsx_fy1 = rec.get("fy1")
                if yf_0y_avg and xlsx_fy1 and xlsx_fy1 > 0:
                    fx = yf_0y_avg / xlsx_fy1
                    fx_source = "yfinance live"
                try:
                    local_ccy = tk.info.get("financialCurrency")
                except Exception:
                    local_ccy = None
                if not local_ccy:
                    local_ccy = {
                        ".TW": "TWD", ".T": "JPY", ".JP": "JPY",
                        ".HK": "HKD", ".KS": "KRW", ".KQ": "KRW",
                        ".SS": "CNY", ".SZ": "CNY",
                    }.get(next(s for s in _FOREIGN_SUFFIXES if args.ticker.endswith(s)), None)
            except Exception:
                pass

    # Human-readable text format (default — easy for DD/DCA skill to paste-quote)
    def _fmt(v, unit=""):
        return f"{v:.2f}{unit}" if isinstance(v, (int, float)) else "—"

    print(f"=== EPS Estimates · {args.ticker} ===")
    print(f"  Source: {snap.source_file}  (snapshot {snap.snapshot_date})")
    if fx and local_ccy and local_ccy != "USD":
        print(f"  Currency: {local_ccy} (Excel reports USD; FX {fx:.2f} from {fx_source or 'unknown'})")
        print()
        print(f"  FY+1 EPS:  {_fmt(rec.get('fy1') * fx if rec.get('fy1') else None)} {local_ccy}  (USD orig {_fmt(rec.get('fy1'))})")
        print(f"  FY+2 EPS:  {_fmt(rec.get('fy2') * fx if rec.get('fy2') else None)} {local_ccy}  (USD orig {_fmt(rec.get('fy2'))})")
        print(f"  FY+3 EPS:  {_fmt(rec.get('fy3') * fx if rec.get('fy3') else None)} {local_ccy}  (USD orig {_fmt(rec.get('fy3'))})")
    else:
        print(f"  Currency: USD (Excel convention — applies to ADRs / TW listings too)")
        print()
        print(f"  FY+1 EPS:  {_fmt(rec.get('fy1'))}")
        print(f"  FY+2 EPS:  {_fmt(rec.get('fy2'))}")
        print(f"  FY+3 EPS:  {_fmt(rec.get('fy3'))}")
    print()
    print(f"  FY+1 → FY+2 growth:  {_fmt(rec.get('growth_fy1_fy2_pct'), '%')}")
    print(f"  FY+2 → FY+3 growth:  {_fmt(rec.get('growth_fy2_fy3_pct'), '%')}")
    print(f"  FY+1 → FY+3 CAGR:    {_fmt(rec.get('cagr_fy1_fy3_pct'), '%')}")
    print()
    print("  Caveats:")
    if rec.get("fy3") is None:
        print("    - FY+3 missing (some tickers have <3 analysts covering FY+3)")
    if rec.get("fy1") is not None and rec.get("fy1") < 0:
        print("    - FY+1 negative — CAGR undefined (only YoY growth meaningful)")
    print("    - These are normalized consensus means (non-GAAP basis for SaaS).")
    print("    - Updated monthly. Re-run this CLI after each Excel refresh.")
    if fx and local_ccy and local_ccy != "USD":
        print(f"    - {local_ccy} values back-computed from yfinance (financialCurrency)/Excel(USD). FX = {fx:.4f}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
