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
RAW_FACTORS_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'raw_factors.json'

WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'

# ── frozen thresholds (LOCKED) ──
CLIP_LO, CLIP_HI = 0.02, 0.98          # winsorize quantiles for z-score
W_REV, W_MOM, W_GROWTH = 0.5, 0.3, 0.2  # composite factor weights
VETO_RET12 = 2.5                        # 12M return > +250% -> veto
CHALLENGER_MARGIN_Z = 0.5              # bench beats weakest seat by >= 0.5 z -> flag
REVIEW_REV_AVG = -2.0                  # seat rev_avg (90D) <= -2 -> flag
# spec v1.1 (2026-07-05, owner-approved): 30D window joins the DECISION RULES
# (composite stays frozen on 90D — 30D has an earnings-calendar artifact and
#  re-weighting is untestable without point-in-time data):
REVIEW_REV30 = -2.0                    # seat rev30_avg <= -2 (fresh downgrade) -> early review flag
                                       # threshold mirrors the 90D rule's -2, same convention, not tuned
HEAT_RET12 = 2.5                       # seat 12M return > +250% -> flag
MIN_EPS_COVERAGE = 300                 # fail-safe floor

# 2026-08-20: raw-dump-only constants feeding shadow lines R (residual momentum)
# and H (52-week high) — NOT part of the frozen composite/veto logic above.
RESMOM_REG_WINDOW = 252                # line R: OLS regression window (trading days)
RESMOM_SKIP_DAYS = 21                  # line R: skip most-recent N days from sum/std (short-term reversal)
RESMOM_MIN_OBS = RESMOM_REG_WINDOW + RESMOM_SKIP_DAYS  # 273 — data-sufficiency gate, else null
PX_52WH_WINDOW = 252                   # line H: 52-week-high lookback window (trading days)


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
    # SPY daily returns — feeds shadow line R's market-residual OLS (below).
    spy_ret = spy.pct_change().dropna()

    rows = {}
    for t in tickers:
        try:
            c = px[t]['Close'].dropna()
            if len(c) < 260:
                continue
            ma200 = c.rolling(200).mean().iloc[-1]
            # up-day ratio, trailing 126 trading days — feeds shadow line Q
            # (path-quality / "frog in the pan" smoothness proxy). Not part of
            # the frozen composite/veto logic; purely a raw-dump passthrough.
            up_diffs = c.diff().dropna().tail(126)
            pct_up_126 = float((up_diffs > 0).sum() / len(up_diffs)) if len(up_diffs) else None

            # px_over_52wh — feeds shadow line H (52-week-high line). Raw-dump
            # passthrough only; not part of the frozen composite/veto logic.
            px_over_52wh = (float(c.iloc[-1] / c.tail(PX_52WH_WINDOW).max())
                            if len(c) >= PX_52WH_WINDOW else None)

            # resmom — feeds shadow line R (residual-momentum line). Raw-dump
            # passthrough only; not part of the frozen composite/veto logic.
            # Definition (PREREG'd 2026-08-20): OLS-regress the ticker's daily
            # return on SPY's same-day daily return (with intercept) over the
            # trailing RESMOM_REG_WINDOW (252) trading days on the common
            # date index; take the resulting daily residuals; skip the most
            # recent RESMOM_SKIP_DAYS (21) of them (short-term-reversal
            # avoidance); signal = sum(remaining residuals) / std(remaining
            # residuals, ddof=1). Requires >= RESMOM_MIN_OBS (273) common
            # trading days of ticker+SPY returns, else null (excluded).
            t_ret = c.pct_change().dropna()
            common = pd.concat({'r': t_ret, 's': spy_ret}, axis=1, join='inner').dropna()
            if len(common) >= RESMOM_MIN_OBS:
                win = common.tail(RESMOM_REG_WINDOW)
                X = np.column_stack([np.ones(len(win)), win['s'].to_numpy()])
                beta, *_ = np.linalg.lstsq(X, win['r'].to_numpy(), rcond=None)
                resid = win['r'].to_numpy() - X @ beta
                sig_resid = resid[:-RESMOM_SKIP_DAYS]  # drop most-recent 21
                sig_std = float(np.std(sig_resid, ddof=1)) if len(sig_resid) > 1 else 0.0
                resmom = float(np.sum(sig_resid) / sig_std) if sig_std > 0 else None
            else:
                resmom = None

            rows[t] = dict(
                price=float(c.iloc[-1]),
                above200=bool(c.iloc[-1] > ma200),
                mom6=float(c.iloc[-1] / c.iloc[-127] - 1),
                ret12=float(c.iloc[-1] / c.iloc[-253] - 1),
                pct_up_126=pct_up_126,
                resmom=resmom,
                px_over_52wh=px_over_52wh,
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

            def rev(r, col='90daysAgo'):
                cur, old = r.get('current'), r.get(col)
                if cur is None or old is None or pd.isna(cur) or pd.isna(old) or old == 0:
                    return None
                return (cur / old - 1) * 100 * (1 if old > 0 else -1)

            g = None
            if cy.get('current') and ny.get('current') and cy['current'] > 0:
                g = (ny['current'] / cy['current'] - 1) * 100
            # rev30_*: 30-day "freshness" companion metric — informational only,
            # NOT part of the frozen composite (which stays on the 90-day window)
            return t, dict(rev_fy1=rev(cy), rev_fy2=rev(ny),
                           rev30_fy1=rev(cy, '30daysAgo'), rev30_fy2=rev(ny, '30daysAgo'),
                           growth=g,
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

    # ── earnings surprise (threaded per-ticker, 8 workers) ──
    # Feeds shadow line P (PEAD / financial-report-surprise line). Raw-dump
    # passthrough ONLY — does not touch the frozen composite/veto logic above.
    def surprise_info(t):
        try:
            eh = yf.Ticker(t).earnings_history
            if eh is None or eh.empty:
                return t, None
            eh = eh[eh['epsActual'].notna()]
            if eh.empty:
                return t, None
            idx = eh.index[-1]
            row = eh.iloc[-1]
            sp = row.get('surprisePercent')
            if sp is None or pd.isna(sp):
                return t, None
            date_iso = pd.Timestamp(idx).date().isoformat()
            # yfinance's earnings_history.surprisePercent is a FRACTION
            # (e.g. 0.0452 == +4.52%); scale to percent-point units to match
            # this script's other percent fields (rev_fy1/rev_fy2/growth).
            # Note: the 'quarter' index is the fiscal-period END date, not the
            # actual report/announcement date (which yfinance keeps only in
            # the separate get_earnings_dates() call) — it typically lags the
            # real report date by ~3-6 weeks, so using it as the "report
            # date" for freshness gating is slightly conservative (marks
            # things stale a bit sooner than the true announcement date
            # would), not lenient.
            return t, dict(surprise_pct=float(sp) * 100.0, surprise_date=date_iso)
        except Exception:
            return t, None

    surprise_got = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(surprise_info, t) for t in rows]
        for f in as_completed(futs):
            t, d = f.result()
            if d:
                rows[t].update(d)
                surprise_got += 1
    print(f"surprise coverage: {surprise_got}")

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
        # v1.1 "review_fresh": 30D consensus turned negative — earlier warning
        # than the 90D window (fires independently so the human sees WHICH window)
        rev30_pre = g(t, 'rev30_fy1'), g(t, 'rev30_fy2')
        rev30_vals_pre = [v for v in rev30_pre if v is not None]
        if rev30_vals_pre and sum(rev30_vals_pre) / len(rev30_vals_pre) <= REVIEW_REV30:
            flags.append('review_fresh')
        # "heat": 12M return blew past +250%
        if ret12 is not None and ret12 > HEAT_RET12:
            flags.append('heat')

        rev30_fy1 = g(t, 'rev30_fy1')
        rev30_fy2 = g(t, 'rev30_fy2')
        rev30_vals = [v for v in (rev30_fy1, rev30_fy2) if v is not None]
        rev30_avg = sum(rev30_vals) / len(rev30_vals) if rev30_vals else None

        seats_out.append({
            'ticker': t,
            'close': round(close, 2) if close is not None else None,
            'ret_since_entry_pct': ret_since,
            'rev_fy1': round(rev_fy1, 1) if rev_fy1 is not None else None,
            'rev_fy2': round(rev_fy2, 1) if rev_fy2 is not None else None,
            'rev30_avg': round(rev30_avg, 1) if rev30_avg is not None else None,
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
        # v1.1: challenger must ALSO have live 30D momentum (> 0) — a high score
        # built on a stale 90D revision does not qualify to challenge a seat
        b30 = [v for v in (g(bt, 'rev30_fy1'), g(bt, 'rev30_fy2')) if v is not None]
        b30_avg = sum(b30) / len(b30) if b30 else None
        if (bs is not None and weakest_seat_score is not None
                and bs - weakest_seat_score >= CHALLENGER_MARGIN_Z
                and b30_avg is not None and b30_avg > 0):
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
            'rev30_avg': round(float(univ[['rev30_fy1', 'rev30_fy2']].astype(float).mean(axis=1).at[t]), 1)
                         if pd.notna(univ[['rev30_fy1', 'rev30_fy2']].astype(float).mean(axis=1).at[t]) else None,
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

    # ── raw factor dump for the shadow-track experiment (build_momentum5_shadow.py) ──
    # Full univ (post-dropna, pre-veto) so the shadow script can recompute its own
    # composite variants; does NOT feed the frozen composite/veto logic above.
    # 2026-08-20: added pct_up_126 (feeds shadow line Q), surprise_pct/
    # surprise_date (feeds shadow line P), and resmom/px_over_52wh (feed
    # shadow lines R and H respectively) — all raw-dump passthrough only.
    def gv(t, col):
        v = univ.at[t, col] if col in univ.columns else None
        if v is None or pd.isna(v):
            return None
        return float(v)

    def gv_str(t, col):
        if col not in univ.columns:
            return None
        v = univ.at[t, col]
        return None if v is None or pd.isna(v) else str(v)

    raw_universe = []
    for t in univ.index:
        raw_universe.append({
            'ticker': t,
            'price': gv(t, 'price'),
            'above200': bool(univ.at[t, 'above200']) if pd.notna(univ.at[t, 'above200']) else None,
            'mom6': gv(t, 'mom6'),
            'ret12': gv(t, 'ret12'),
            'rev_fy1': gv(t, 'rev_fy1'),
            'rev_fy2': gv(t, 'rev_fy2'),
            'rev30_fy1': gv(t, 'rev30_fy1'),
            'rev30_fy2': gv(t, 'rev30_fy2'),
            'growth': gv(t, 'growth'),
            'pct_up_126': gv(t, 'pct_up_126'),
            'surprise_pct': gv(t, 'surprise_pct'),
            'surprise_date': gv_str(t, 'surprise_date'),
            'resmom': gv(t, 'resmom'),
            'px_over_52wh': gv(t, 'px_over_52wh'),
        })
    surprise_coverage = sum(1 for r in raw_universe if r['surprise_pct'] is not None)
    resmom_coverage = sum(1 for r in raw_universe if r['resmom'] is not None)
    px52wh_coverage = sum(1 for r in raw_universe if r['px_over_52wh'] is not None)
    raw_payload = {
        'as_of': as_of,
        'spy_close': round(spy_close, 2),
        'spy6': float(spy6),  # SPY's own 6M return — needed to rebuild relmom6 = mom6 - spy6
        'surprise_coverage': surprise_coverage,
        'resmom_coverage': resmom_coverage,
        'px52wh_coverage': px52wh_coverage,
        'universe': raw_universe,
    }

    return payload, raw_payload


def main():
    try:
        result = build()
    except Exception as e:
        # any screen/scrape failure -> keep last good data.json
        print(f"  ✗ screen failed ({type(e).__name__}: {e}) — data.json left unchanged")
        sys.exit(0)

    if result is None:
        # coverage fail-safe already logged
        sys.exit(0)

    payload, raw_payload = result

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

    RAW_FACTORS_JSON.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=1) + '\n',
                                encoding='utf-8')
    print(f"  ✓ wrote {RAW_FACTORS_JSON.relative_to(ROOT)} "
          f"({len(raw_payload['universe'])} tickers, "
          f"surprise_coverage={raw_payload['surprise_coverage']}, "
          f"resmom_coverage={raw_payload['resmom_coverage']}, "
          f"px52wh_coverage={raw_payload['px52wh_coverage']})")


if __name__ == '__main__':
    main()
