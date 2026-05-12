"""
US Quarterly fundamentals fetcher.
Output: docs/screener/quarterly.json

Universe: top N (default 100) tickers by `combined` from docs/screener/latest.json
(same convention as scripts/fundamentals_us.py).

Per ticker fetches up to 8 most-recent quarters of:
  - period       : "YYYYQX"
  - eps_diluted  : Diluted EPS for the quarter (fallback Basic EPS)
  - revenue      : Total Revenue
  - fcf_margin   : FCF (Operating CF + CapEx) / Revenue

Derived streak fields (consecutive most-recent quarters meeting the condition):
  - eps_yoy_neg_streak       : count of quarters where eps[i] < eps[i+4]
  - fcf_margin_decline_streak: count of quarters where fcf_margin[i] < fcf_margin[i+4]

Cockpit 證偽 condition「連 2 季負/降」maps to streak >= 2.

Usage:
  python scripts/quarterly_us.py             # top 100 (default)
  python scripts/quarterly_us.py --top 10    # restrict to top 10
"""

import argparse
import json
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           'yfinance>=0.2.40', 'pandas', '-q'])
    import pandas as pd
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
SCREENER_DIR = ROOT / 'docs' / 'screener'
LATEST_PATH = SCREENER_DIR / 'latest.json'
OUTPUT_PATH = SCREENER_DIR / 'quarterly.json'

MAX_QUARTERS = 8


def _cell(df, key_substring: str, col):
    """Return df cell at (row containing key_substring, col) as float or None."""
    if df is None or df.empty or col not in df.columns:
        return None
    for r in df.index:
        if key_substring.lower() in str(r).lower():
            v = df.loc[r, col]
            try:
                f = float(v)
                return f if pd.notna(f) else None
            except (TypeError, ValueError):
                return None
    return None


def _period_label(ts) -> str:
    try:
        t = pd.Timestamp(ts)
        return f"{t.year}Q{t.quarter}"
    except Exception:
        return str(ts)


def _fcf_for_quarter(cf_df, col):
    """Free Cash Flow for one quarter column. Prefer 'Free Cash Flow' row;
    else Operating Cash Flow + Capital Expenditure (capex is signed negative)."""
    if cf_df is None or cf_df.empty or col not in cf_df.columns:
        return None
    fcf = _cell(cf_df, 'Free Cash Flow', col)
    if fcf is not None:
        return fcf
    ocf = _cell(cf_df, 'Operating Cash Flow', col)
    capex = _cell(cf_df, 'Capital Expenditure', col)
    if ocf is not None and capex is not None:
        return ocf + capex
    return None


def _yoy_streak(quarters, field):
    """Count consecutive newest quarters where field[i] < field[i+4] (YoY decline).
    quarters[] must be sorted newest-first. Need both endpoints non-None to compare;
    a missing value breaks the streak. Returns 0 if insufficient data."""
    streak = 0
    for i in range(len(quarters)):
        j = i + 4
        if j >= len(quarters):
            break
        curr = quarters[i].get(field)
        prev = quarters[j].get(field)
        if curr is None or prev is None:
            break
        if curr < prev:
            streak += 1
        else:
            break
    return streak


def fetch_us_quarterly(ticker: str) -> dict:
    out = {
        'ticker': ticker,
        'quarters': [],
        'eps_yoy_neg_streak': None,
        'fcf_margin_decline_streak': None,
    }
    try:
        t = yf.Ticker(ticker)
        is_df = t.quarterly_income_stmt
        if is_df is None or getattr(is_df, 'empty', True):
            return out
        cf_df = t.quarterly_cashflow

        # yfinance returns columns as Timestamps; newest is leftmost by convention,
        # but sort explicitly to be safe.
        cols = sorted(is_df.columns, reverse=True)

        quarters = []
        for col in cols:
            rev = _cell(is_df, 'Total Revenue', col)
            eps = _cell(is_df, 'Diluted EPS', col)
            if eps is None:
                eps = _cell(is_df, 'Basic EPS', col)
            fcf = _fcf_for_quarter(cf_df, col)
            fcf_margin = (fcf / rev) if (fcf is not None and rev and rev > 0) else None
            quarters.append({
                'period': _period_label(col),
                'eps_diluted': eps,
                'revenue': rev,
                'fcf_margin': fcf_margin,
            })

        quarters = quarters[:MAX_QUARTERS]
        out['quarters'] = quarters
        out['eps_yoy_neg_streak'] = _yoy_streak(quarters, 'eps_diluted')
        out['fcf_margin_decline_streak'] = _yoy_streak(quarters, 'fcf_margin')
    except Exception:
        pass
    return out


def load_universe(top_n: int):
    if not LATEST_PATH.exists():
        raise SystemExit(f"latest.json not found at {LATEST_PATH}; run screener.py first.")
    with open(LATEST_PATH) as f:
        d = json.load(f)
    rankings = d.get('rankings') or []
    if not rankings:
        raise SystemExit("rankings is empty in latest.json")
    rankings = sorted(rankings, key=lambda r: r.get('combined', 0), reverse=True)
    return [r['ticker'] for r in rankings[:top_n]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', type=int, default=100,
                        help='Number of top-combined tickers to fetch (default: 100)')
    args = parser.parse_args()

    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    generated_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"=== US Quarterly fetcher: {today} (top {args.top}) ===\n")

    tickers = load_universe(args.top)
    print(f"  Universe: {len(tickers)} tickers from latest.json")

    data = {}
    t0 = time.time()
    for i, ticker in enumerate(tickers, 1):
        f = fetch_us_quarterly(ticker)
        data[ticker] = f
        if i % 5 == 0 or i == len(tickers):
            elapsed = time.time() - t0
            qn = len(f['quarters'])
            print(f"  [{i:>3}/{len(tickers)}] {ticker:>6s} "
                  f"q={qn} eps_neg={f['eps_yoy_neg_streak']} "
                  f"fcf_dec={f['fcf_margin_decline_streak']}  ({elapsed:.0f}s)")

    output = {
        'generated_at': generated_at,
        'date': today,
        'count': len(data),
        'tickers': data,
    }

    SCREENER_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    have_q = sum(1 for v in data.values() if v.get('quarters'))
    have_eps_streak = sum(1 for v in data.values() if v.get('eps_yoy_neg_streak') is not None)
    have_fcf_streak = sum(1 for v in data.values() if v.get('fcf_margin_decline_streak') is not None)
    triggered_eps = sum(1 for v in data.values() if (v.get('eps_yoy_neg_streak') or 0) >= 2)
    triggered_fcf = sum(1 for v in data.values() if (v.get('fcf_margin_decline_streak') or 0) >= 2)
    print(f"\n  ✓ Output: {OUTPUT_PATH}")
    print(f"  ✓ Coverage: total={len(data)}")
    print(f"    - quarters fetched     : {have_q}/{len(data)}")
    print(f"    - eps_yoy_neg_streak   : {have_eps_streak}/{len(data)} (triggered >=2: {triggered_eps})")
    print(f"    - fcf_decline_streak   : {have_fcf_streak}/{len(data)} (triggered >=2: {triggered_fcf})")
    print(f"  ✓ Elapsed: {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
