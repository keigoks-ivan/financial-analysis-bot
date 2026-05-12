"""
US Fundamentals fetcher.
Output: docs/screener/fundamentals.json

Universe: top N (default 30) tickers by `combined` from docs/screener/latest.json
(matches screener.py's existing fetch_fundamentals inline behavior).

4 fields per ticker:
  - eps_cagr   : Forward 2Y EPS CAGR. yfinance earnings_estimate has no +2y
                 row, so we span FY-1 actual (yearAgoEps in 0y row) → FY+1
                 consensus (avg in +1y row), exactly 2 fiscal years. Fallback
                 anchors on trailingEps (~1.5-2Y span, less precise).
  - rev_cagr   : Forward 2Y revenue CAGR (same FY-1 actual → FY+1 estimate).
  - roic       : NOPAT / Invested Capital (annual income_stmt + balance_sheet)
  - fcf_margin : TTM FCF / Revenue

Output schema (carries both keys for forward + backward compat):
  - `fundamentals`: new key consumed by docs/flow/ath-hunter.html
  - `data`        : legacy key consumed by docs/screener.html

Usage:
  python scripts/fundamentals_us.py            # top 100 (default)
  python scripts/fundamentals_us.py --top 30   # restrict to top 30
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
OUTPUT_PATH = SCREENER_DIR / 'fundamentals.json'


def _row(df, key_substring: str):
    if df is None or df.empty:
        return None
    for r in df.index:
        if key_substring.lower() in r.lower():
            v = df.loc[r].iloc[0]
            try:
                f = float(v)
                return f if pd.notna(f) else None
            except (TypeError, ValueError):
                return None
    return None


def _ic_from_balance_sheet(bs_df):
    ic = _row(bs_df, 'Invested Capital')
    if ic is None or ic <= 0:
        equity = _row(bs_df, 'Stockholders Equity') or _row(bs_df, 'Total Equity')
        debt = _row(bs_df, 'Total Debt')
        cash = _row(bs_df, 'Cash And Cash Equivalents') or _row(bs_df, 'Cash')
        if equity and debt is not None and cash is not None:
            ic = equity + debt - cash
    return ic if (ic and ic > 0) else None


def calc_fcf_margin(t, info=None):
    if info is None:
        info = t.info or {}
    rev = info.get('totalRevenue')
    fcf = info.get('freeCashflow')
    if fcf is None:
        try:
            cf_df = t.cashflow
            fcf = _row(cf_df, 'Free Cash Flow')
            if fcf is None:
                ocf = _row(cf_df, 'Operating Cash Flow')
                capex = _row(cf_df, 'Capital Expenditure')
                if ocf is not None and capex is not None:
                    fcf = ocf + capex
        except Exception:
            pass
    if not rev or rev <= 0:
        try:
            rev = _row(t.income_stmt, 'Total Revenue')
        except Exception:
            rev = None
    if fcf is None or not rev or rev <= 0:
        return None
    return float(fcf) / float(rev)


def calc_roic(t, info=None):
    """ROIC = NOPAT / Invested Capital. Skip Financial Services (ROIC not applicable)."""
    try:
        if info is None:
            info = t.info or {}
        if (info.get('sector') or '').strip() == 'Financial Services':
            return None
        bs_df = t.balance_sheet
        ic = _ic_from_balance_sheet(bs_df)
        if ic is None:
            return None
        is_df = t.income_stmt
        op_inc = _row(is_df, 'Operating Income')
        tax = _row(is_df, 'Tax Provision')
        pretax = _row(is_df, 'Pretax Income') or _row(is_df, 'Pre Tax Income')
        if op_inc is None or pretax is None or pretax <= 0:
            op_margin = info.get('operatingMargins')
            total_rev = info.get('totalRevenue')
            if op_margin is None or not total_rev or total_rev <= 0:
                return None
            op_inc = float(op_margin) * float(total_rev)
            eff_tax = 0.21  # US federal corporate rate
        else:
            eff_tax = (tax / pretax) if (tax is not None) else 0.21
            eff_tax = max(0.0, min(0.50, eff_tax))
        nopat = op_inc * (1 - eff_tax)
        return nopat / ic
    except Exception:
        return None


def _forward_2y_cagr(df, base_col, ttm_fallback):
    """Forward 2Y CAGR using yfinance estimate dataframe (earnings or revenue).

    Primary span: FY-1 actual (yearAgoEps/yearAgoRevenue in 0y row) →
                  FY+1 consensus (avg in +1y row). Exactly 2 fiscal years.
    Fallback anchor: ttm_fallback (trailingEps / totalRevenue). Less precise
                    (~1.5-2Y span depending on FY calendar position) but
                    usable when yearAgo column is missing or non-positive.
    Returns None when no valid base or forward value is found, or when the
    ratio is non-positive (e.g. negative-earnings recovery).
    """
    try:
        if df is None or getattr(df, 'empty', True):
            return None
        if '+1y' not in df.index or 'avg' not in df.columns:
            return None
        fwd = df.loc['+1y', 'avg']
        if not pd.notna(fwd) or fwd <= 0:
            return None
        base = None
        if '0y' in df.index and base_col in df.columns:
            v = df.loc['0y', base_col]
            if pd.notna(v) and float(v) > 0:
                base = float(v)
        if base is None and ttm_fallback is not None:
            try:
                v = float(ttm_fallback)
                if v > 0:
                    base = v
            except (TypeError, ValueError):
                pass
        if base is None or base <= 0:
            return None
        ratio = float(fwd) / base
        if ratio <= 0:
            return None
        return ratio ** 0.5 - 1
    except Exception:
        return None


def fetch_us_fundamentals(ticker: str) -> dict:
    out = {'ticker': ticker, 'rev_cagr': None, 'eps_cagr': None,
           'roic': None, 'fcf_margin': None}
    try:
        t = yf.Ticker(ticker)
        info = {}
        try:
            info = t.info or {}
        except Exception:
            pass
        try:
            out['eps_cagr'] = _forward_2y_cagr(
                t.earnings_estimate, 'yearAgoEps', info.get('trailingEps'))
        except Exception:
            pass
        try:
            out['rev_cagr'] = _forward_2y_cagr(
                t.revenue_estimate, 'yearAgoRevenue', info.get('totalRevenue'))
        except Exception:
            pass
        out['roic'] = calc_roic(t, info=info)
        out['fcf_margin'] = calc_fcf_margin(t, info=info)
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
    # Sort by combined desc (latest.json may already be sorted, but don't assume)
    rankings = sorted(rankings, key=lambda r: r.get('combined', 0), reverse=True)
    return [r['ticker'] for r in rankings[:top_n]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', type=int, default=100,
                        help='Number of top-combined tickers to fetch (default: 100)')
    args = parser.parse_args()

    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    generated_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"=== US Fundamentals fetcher: {today} (top {args.top}) ===\n")

    tickers = load_universe(args.top)
    print(f"  Universe: {len(tickers)} tickers from latest.json")

    data = {}
    t0 = time.time()
    for i, ticker in enumerate(tickers, 1):
        f = fetch_us_fundamentals(ticker)
        data[ticker] = f
        if i % 5 == 0 or i == len(tickers):
            elapsed = time.time() - t0
            print(f"  [{i:>3}/{len(tickers)}] {ticker:>6s} "
                  f"eps={f['eps_cagr']} rev={f['rev_cagr']} "
                  f"roic={f['roic']} fcf={f['fcf_margin']}  ({elapsed:.0f}s)")

    output = {
        'generated_at': generated_at,
        'date': today,
        'count': len(data),
        'fundamentals': data,  # consumed by docs/flow/ath-hunter.html
        'data': data,          # back-compat for docs/screener.html
    }

    SCREENER_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    have = {k: 0 for k in ('eps_cagr', 'rev_cagr', 'roic', 'fcf_margin')}
    for v in data.values():
        for k in have:
            if v.get(k) is not None:
                have[k] += 1
    print(f"\n  ✓ Output: {OUTPUT_PATH}")
    print(f"  ✓ Coverage: total={len(data)}")
    for k, n in have.items():
        pct = 100 * n / len(data) if data else 0
        print(f"    - {k:12s}: {n:>3}/{len(data)} ({pct:.0f}%)")
    print(f"  ✓ Elapsed: {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
