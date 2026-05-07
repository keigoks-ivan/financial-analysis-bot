"""
日股 Fundamentals fetcher
產出: docs/screener/jp_fundamentals.json (mirror US/TW schema)
觸發: 手動 (workflow_dispatch),fundamentals 一季變一次,不排 cron

4 個欄位:
  - eps_cagr: 1Y forward EPS growth (yfinance earnings_estimate +1y row)
  - rev_cagr: 1Y forward revenue growth (yfinance revenue_estimate +1y row)
  - roic    : NOPAT / Invested Capital (自算,IC 用 yfinance balance_sheet 直接給的 row)
  - fcf_margin: TTM freeCashflow / totalRevenue (yfinance .info)
"""

import json, sys, time, warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance', 'pandas', '-q'])
    import pandas as pd
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
SCREENER_DIR = ROOT / 'docs' / 'screener'
OUTPUT_PATH = SCREENER_DIR / 'jp_fundamentals.json'

# Universe from screener_jp (避免重複維護)
sys.path.insert(0, str(ROOT / 'scripts'))
from screener_jp import TOPIX_CORE30, NIKKEI_225


def _row(df, key_substring: str):
    """Find first row whose label contains substring (case-insensitive); return latest col value or None."""
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
    """Get Invested Capital from yfinance balance_sheet (direct row or fallback formula)."""
    ic = _row(bs_df, 'Invested Capital')
    if ic is None or ic <= 0:
        equity = _row(bs_df, 'Stockholders Equity') or _row(bs_df, 'Total Equity')
        debt = _row(bs_df, 'Total Debt')
        cash = _row(bs_df, 'Cash And Cash Equivalents') or _row(bs_df, 'Cash')
        if equity and debt is not None and cash is not None:
            ic = equity + debt - cash
    return ic if (ic and ic > 0) else None


def calc_fcf_margin(t, info=None):
    """FCF / Revenue (TTM-ish).

    Primary: info.freeCashflow / info.totalRevenue (when populated).
    Fallback 1: cashflow stmt 'Free Cash Flow' row (yfinance 直接給).
    Fallback 2: cashflow stmt OCF + CapEx (CapEx 為負所以加).
    Revenue fallback: info.totalRevenue → income_stmt 'Total Revenue' row.
    """
    if info is None: info = t.info or {}
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
                    fcf = ocf + capex  # capex usually negative
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
    """ROIC = NOPAT / Invested Capital.

    Primary: yfinance income_stmt (annual) + balance_sheet.
    Fallback: .info['operatingMargins'] × .info['totalRevenue'] when income_stmt is empty
              (common for some JP large-caps like Keyence/HOYA/Shin-Etsu/Hitachi).
    Skip:    Financial Services sector — traditional ROIC doesn't apply.
    """
    try:
        if info is None:
            info = t.info or {}

        # Skip banks / insurance / asset managers — ROIC 不適用
        if (info.get('sector') or '').strip() == 'Financial Services':
            return None

        bs_df = t.balance_sheet
        ic = _ic_from_balance_sheet(bs_df)
        if ic is None:
            return None

        # Primary path: annual income_stmt
        is_df = t.income_stmt
        op_inc = _row(is_df, 'Operating Income')
        tax = _row(is_df, 'Tax Provision')
        pretax = _row(is_df, 'Pretax Income') or _row(is_df, 'Pre Tax Income')

        # Fallback path: derive Op Income from .info trailing fields
        if op_inc is None or pretax is None or pretax <= 0:
            op_margin = info.get('operatingMargins')
            total_rev = info.get('totalRevenue')
            if op_margin is None or not total_rev or total_rev <= 0:
                return None
            op_inc = float(op_margin) * float(total_rev)
            eff_tax = 0.25  # JP corporate effective tax ~25-30%, use 25%
        else:
            eff_tax = (tax / pretax) if (tax is not None) else 0.25
            eff_tax = max(0.0, min(0.50, eff_tax))

        nopat = op_inc * (1 - eff_tax)
        return nopat / ic
    except Exception:
        return None


def fetch_jp_fundamentals(ticker: str) -> dict:
    out = {'ticker': ticker, 'rev_cagr': None, 'eps_cagr': None,
           'roic': None, 'fcf_margin': None}
    try:
        t = yf.Ticker(ticker)

        try:
            df = t.earnings_estimate
            if df is not None and '+1y' in df.index and 'growth' in df.columns:
                v = df.loc['+1y', 'growth']
                if pd.notna(v):
                    out['eps_cagr'] = float(v)
        except Exception:
            pass

        try:
            df = t.revenue_estimate
            if df is not None and '+1y' in df.index and 'growth' in df.columns:
                v = df.loc['+1y', 'growth']
                if pd.notna(v):
                    out['rev_cagr'] = float(v)
        except Exception:
            pass

        # 把 info 算一次給 calc_roic 與 fcf_margin 共用 (省一次 yfinance call)
        info = {}
        try:
            info = t.info or {}
        except Exception:
            pass

        out['roic'] = calc_roic(t, info=info)
        out['fcf_margin'] = calc_fcf_margin(t, info=info)
    except Exception:
        pass
    return out


def main():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    print(f"=== JP Fundamentals fetcher: {today} ===\n")

    # Build universe — Core30 first so dedup keeps Core30 as the canonical entry
    universe = {}
    for d in (TOPIX_CORE30, NIKKEI_225):
        for t in d:
            universe.setdefault(t, None)
    tickers = list(universe.keys())
    print(f"  Universe: {len(tickers)} tickers")

    data = {}
    t0 = time.time()
    for i, ticker in enumerate(tickers, 1):
        f = fetch_jp_fundamentals(ticker)
        data[ticker] = f
        if i % 25 == 0 or i == len(tickers):
            elapsed = time.time() - t0
            print(f"  [{i:>3}/{len(tickers)}] {ticker:>8s} eps={f['eps_cagr']} rev={f['rev_cagr']} roic={f['roic']} fcf={f['fcf_margin']}  ({elapsed:.0f}s)")

    output = {
        'date': today,
        'count': len(data),
        'data': data,
    }

    SCREENER_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Coverage report
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
