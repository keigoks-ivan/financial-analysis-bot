"""
Momentum-5 weekly data builder — feeds docs/research/momentum-5/data.json.

WHAT THIS IS
------------
The site owner runs a 5-seat S&P 500 "12-month upside" research portfolio
("Momentum-5"). Seats are chosen by a frozen EPS-revision-momentum screen PLUS
human catalyst / expectation-gap judgment. This script refreshes the *data* the
page renders every week; it NEVER changes the seats. Seat governance lives in
docs/research/momentum-5/portfolio.json (hand-edited, source of truth). This
script only raises informational FLAGS ("this seat's consensus turned negative",
"a bench name now out-scores your weakest seat", "this seat is up >250%") so the
human can decide. Swaps are always a manual edit of portfolio.json.

FROZEN SCREEN SPEC (LOCKED — changes go through the owner)
----------------------------------------------------------
Universe   : S&P 500 constituents scraped from Wikipedia (browser User-Agent).
composite  = 0.5 * z(rev_avg)                 # main factor: 3M EPS revision, FY1/FY2 avg
           + 0.3 * z(relmom6 vs SPY)          # confirmation: 6M relative momentum
           + 0.2 * z(FY1->FY2 growth)         # false-positive filter: forward growth
z(.)       : winsorized at the 2% / 98% quantiles, then (x-mean)/std.
Vetoes     : price below 200DMA  |  rev_avg <= 0  |  12M return > +250%.
eps_trend  : yfinance .eps_trend, 3-month ("90daysAgo") revision snapshot,
             fetched threaded with 8 workers.
These thresholds (0.5/0.3/0.2 weights, 2/98 clip, 200DMA / 0 / +250% vetoes,
challenger 0.5 z-margin, review rev_avg <= -2, heat +250%) are LOCKED. Do not
tune them here — they are the portfolio's pre-registered rules.

FAIL-SAFE (mirrors scripts/build_risk_gauge.py culture)
-------------------------------------------------------
If eps_trend coverage < 300, or the screen throws for any reason, we print a
warning and EXIT 0 WITHOUT touching data.json, so the page keeps its last good
data instead of rendering a broken/empty week.

Runs in the weekly-market-update GitHub Actions workflow (wired by maintainer).
"""

import io
import json
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

import requests

ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'portfolio.json'
DATA_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'data.json'

WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'

# ── frozen thresholds (LOCKED) ──
CLIP_LO, CLIP_HI = 0.02, 0.98          # winsorize quantiles for z-score
W_REV, W_MOM, W_GROWTH = 0.5, 0.3, 0.2  # composite factor weights
VETO_RET12 = 2.5                        # 12M return > +250% -> veto
CHALLENGER_MARGIN_Z = 0.5              # bench beats weakest seat by >= 0.5 z -> flag
REVIEW_REV_AVG = -2.0                  # seat rev_avg <= -2 -> flag
HEAT_RET12 = 2.5                       # seat 12M return > +250% -> flag
MIN_EPS_COVERAGE = 300                 # fail-safe floor


def run_screen():
    """Run the frozen S&P 500 12M-upside screen.

    Returns (df, spy_close, spy6, coverage) where df is indexed by yfinance
    ticker and carries the full metric set + composite score for every name
    that cleared price coverage; `elig` masking (vetoes) is applied by callers.
    Raises on hard failure (caught by main() -> fail-safe exit 0).
    """
    # ── constituents (Wikipedia, browser UA) ──
    html = requests.get(WIKI_URL, headers={'User-Agent': BROWSER_UA}, timeout=60).text
    tables = pd.read_html(io.StringIO(html))
    cons = tables[0]
    cons['yf'] = cons['Symbol'].str.replace('.', '-', regex=False)
    sector = dict(zip(cons['yf'], cons['GICS Sector']))
    subind = dict(zip(cons['yf'], cons['GICS Sub-Industry']))
    tickers = cons['yf'].tolist()
    print(f"constituents: {len(tickers)}")

    # ── prices (batch, 2y adjusted daily) ──
    px = yf.download(tickers + ['SPY'], period='2y', interval='1d', auto_adjust=True,
                     group_by='ticker', progress=False, threads=True)
    spy = px['SPY']['Close'].dropna()
    spy_close = float(spy.iloc[-1])
    spy6 = spy.iloc[-1] / spy.iloc[-127] - 1

    rows = {}
    for t in tickers:
        try:
            c = px[t]['Close'].dropna()
            if len(c) < 260:
                continue
            ma200 = c.rolling(200).mean().iloc[-1]
            rows[t] = dict(
                price=float(c.iloc[-1]),
                above200=bool(c.iloc[-1] > ma200),
                mom6=float(c.iloc[-1] / c.iloc[-127] - 1),
                ret12=float(c.iloc[-1] / c.iloc[-253] - 1),
            )
        except Exception:
            pass
    print(f"price coverage: {len(rows)}")

    # ── eps trend (threaded per-ticker, 8 workers) ──
    def trend(t):
        try:
            tdf = yf.Ticker(t).eps_trend
            if tdf is None or tdf.empty:
                return t, None
            cy, ny = tdf.loc['0y'], tdf.loc['+1y']

            def rev(r):
                cur, old = r.get('current'), r.get('90daysAgo')
                if cur is None or old is None or pd.isna(cur) or pd.isna(old) or old == 0:
                    return None
                return (cur / old - 1) * 100 * (1 if old > 0 else -1)

            g = None
            if cy.get('current') and ny.get('current') and cy['current'] > 0:
                g = (ny['current'] / cy['current'] - 1) * 100
            return t, dict(rev_fy1=rev(cy), rev_fy2=rev(ny), growth=g,
                           eps_fy1=float(cy['current']) if pd.notna(cy.get('current')) else None)
        except Exception:
            return t, None

    got = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(trend, t) for t in rows]
        for f in as_completed(futs):
            t, d = f.result()
            if d:
                rows[t].update(d)
                got += 1
    print(f"eps_trend coverage: {got}")

    # ── composite (frozen 0.5/0.3/0.2, winsorized z) ──
    df = pd.DataFrame(rows).T
    df['sector'] = pd.Series(sector)
    df['subind'] = pd.Series(subind)
    df['rev_avg'] = df[['rev_fy1', 'rev_fy2']].astype(float).mean(axis=1)
    df['relmom6'] = df['mom6'].astype(float) - spy6

    univ = df.dropna(subset=['rev_avg', 'growth', 'relmom6']).copy()

    def z(s):
        s = s.astype(float).clip(s.quantile(CLIP_LO), s.quantile(CLIP_HI))
        return (s - s.mean()) / s.std()

    univ['score'] = (W_REV * z(univ['rev_avg'])
                     + W_MOM * z(univ['relmom6'])
                     + W_GROWTH * z(univ['growth']))

    # eligible after vetoes: above 200DMA & positive revision & not up >250%
    univ['eligible'] = (univ['above200']
                        & (univ['rev_avg'] > 0)
                        & (univ['ret12'] < VETO_RET12))

    # rank among the eligible universe (1 = best), by composite desc
    elig = univ[univ['eligible']].sort_values('score', ascending=False)
    univ['rank'] = pd.Series({t: i + 1 for i, t in enumerate(elig.index)})

    coverage = dict(constituents=len(tickers), priced=len(rows),
                    eps_trend=got, eligible=int(univ['eligible'].sum()))
    return univ, spy_close, float(spy6), coverage


def build():
    now = datetime.now(timezone.utc)
    as_of = now.strftime('%Y-%m-%d')
    print(f"=== Momentum-5 Build: {as_of} ===")

    portfolio = json.loads(PORTFOLIO_JSON.read_text(encoding='utf-8'))
    seats_cfg = portfolio['seats']
    bench_cfg = portfolio.get('bench', [])
    spy_entry = float(portfolio['benchmark']['entry_price'])

    univ, spy_close, spy6, coverage = run_screen()

    # ── fail-safe: insufficient coverage -> leave data.json untouched ──
    if coverage['eps_trend'] < MIN_EPS_COVERAGE:
        print(f"  ✗ eps_trend coverage {coverage['eps_trend']} < {MIN_EPS_COVERAGE} "
              f"— aborting, data.json left unchanged")
        return None

    def g(t, col, default=None):
        """Safe scalar lookup from the screen frame."""
        if t in univ.index and col in univ.columns:
            v = univ.at[t, col]
            if pd.notna(v):
                return float(v) if isinstance(v, (int, float, np.floating, np.integer)) else v
        return default

    # weakest seat score (for the challenger comparison)
    seat_scores = [g(s['ticker'], 'score') for s in seats_cfg]
    seat_scores = [x for x in seat_scores if x is not None]
    weakest_seat_score = min(seat_scores) if seat_scores else None

    # ── per-seat metrics + flags ──
    seats_out = []
    seat_rets = []
    for s in seats_cfg:
        t = s['ticker']
        close = g(t, 'price')
        entry = float(s['entry_price'])
        ret_since = round((close / entry - 1) * 100, 1) if close is not None else None
        if ret_since is not None:
            seat_rets.append(ret_since / 100.0)

        rev_fy1 = g(t, 'rev_fy1')
        rev_fy2 = g(t, 'rev_fy2')
        rev_avg = g(t, 'rev_avg')
        score = g(t, 'score')
        rank = g(t, 'rank')
        ret12 = g(t, 'ret12')

        flags = []
        # "review": 3M consensus turned meaningfully negative
        if rev_avg is not None and rev_avg <= REVIEW_REV_AVG:
            flags.append('review')
        # "heat": 12M return blew past +250%
        if ret12 is not None and ret12 > HEAT_RET12:
            flags.append('heat')

        seats_out.append({
            'ticker': t,
            'close': round(close, 2) if close is not None else None,
            'ret_since_entry_pct': ret_since,
            'rev_fy1': round(rev_fy1, 1) if rev_fy1 is not None else None,
            'rev_fy2': round(rev_fy2, 1) if rev_fy2 is not None else None,
            'score': round(score, 2) if score is not None else None,
            'rank': int(rank) if rank is not None else None,
            'flags': flags,
        })

    # "challenger": any bench name out-scoring the weakest seat by >= 0.5 z.
    # (informational, portfolio-level — attach to the weakest seat so the human
    #  sees where the pressure is; also expose bench_scores for the table.)
    bench_scores = {}
    challenger_present = False
    for b in bench_cfg:
        bt = b['ticker']
        bs = g(bt, 'score')
        bench_scores[bt] = round(bs, 2) if bs is not None else None
        if (bs is not None and weakest_seat_score is not None
                and bs - weakest_seat_score >= CHALLENGER_MARGIN_Z):
            challenger_present = True
    if challenger_present and weakest_seat_score is not None:
        for so in seats_out:
            if so['score'] == round(weakest_seat_score, 2):
                so['flags'].append('challenger')
                break

    # ── portfolio equal-weight return vs SPY over same window ──
    port_ret = round(sum(seat_rets) / len(seat_rets) * 100, 1) if seat_rets else None
    spy_ret = round((spy_close / spy_entry - 1) * 100, 1)
    alpha = round(port_ret - spy_ret, 1) if port_ret is not None else None

    # ── this week's screen top 20 ──
    elig = univ[univ['eligible']].sort_values('score', ascending=False).head(20)
    top20 = []
    for t in elig.index:
        top20.append({
            'ticker': t,
            'sector': univ.at[t, 'sector'],
            'rev_fy1': round(float(univ.at[t, 'rev_fy1']), 1) if pd.notna(univ.at[t, 'rev_fy1']) else None,
            'rev_fy2': round(float(univ.at[t, 'rev_fy2']), 1) if pd.notna(univ.at[t, 'rev_fy2']) else None,
            'growth': round(float(univ.at[t, 'growth']), 1) if pd.notna(univ.at[t, 'growth']) else None,
            'relmom6_pct': round(float(univ.at[t, 'relmom6']) * 100, 1),
            'ret12_pct': round(float(univ.at[t, 'ret12']) * 100, 1),
            'score': round(float(univ.at[t, 'score']), 2),
        })

    payload = {
        'as_of': as_of,
        'spy_close': round(spy_close, 2),
        'seats': seats_out,
        'portfolio': {'ret_pct': port_ret, 'spy_ret_pct': spy_ret, 'alpha_pp': alpha},
        'top20': top20,
        'bench_scores': bench_scores,
        'coverage': coverage,
    }
    return payload


def main():
    try:
        payload = build()
    except Exception as e:
        # any screen/scrape failure -> keep last good data.json
        print(f"  ✗ screen failed ({type(e).__name__}: {e}) — data.json left unchanged")
        sys.exit(0)

    if payload is None:
        # coverage fail-safe already logged
        sys.exit(0)

    DATA_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + '\n',
                         encoding='utf-8')
    print(f"  ✓ wrote {DATA_JSON.relative_to(ROOT)}")
    print(f"    coverage: {payload['coverage']}")
    print(f"    portfolio: {payload['portfolio']}")
    print("    seats:")
    for s in payload['seats']:
        flags = ('  [' + ','.join(s['flags']) + ']') if s['flags'] else ''
        print(f"      {s['ticker']:<5} close={s['close']}  ret={s['ret_since_entry_pct']}%  "
              f"revFY1={s['rev_fy1']}  revFY2={s['rev_fy2']}  score={s['score']}  "
              f"rank={s['rank']}{flags}")


if __name__ == '__main__':
    main()
