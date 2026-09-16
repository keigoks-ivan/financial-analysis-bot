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

DOWNLOAD RESILIENCE (2026-09-08 fix — plumbing only, no judgment change)
--------------------------------------------------------------------------
This script's own ~490-ticker yf.download burst runs earlier in the same
weekly-market-update job than build_price_momentum.py's ~512-ticker burst
(see that script's 2026-09-07 fix, commit 71cd044e4, for the incident this
mirrors: two big yf.download bursts back-to-back in one job can trip
Yahoo's 429 rate limit). To make THIS script survivable the same way,
without touching any threshold, price value, or download parameter:
  - tickers + ['SPY'] is downloaded in ~100-ticker batches (identical
    download kwargs per batch, byte-identical to the old single call),
    concatenated into one DataFrame with the exact same
    px[ticker]['Close'] access shape the rest of the file already relies
    on.
  - The whole batched download is retried up to 4 attempts total, with
    exponential backoff + jitter (~20s / 60s / 150s) between attempts,
    whenever SPY comes back empty OR price coverage on that attempt is
    below the coverage floor. The floor reused for this gate is the
    file's OWN existing fail-safe number, MIN_EPS_COVERAGE (300) — not a
    new number invented for this fix.
  - Only after all attempts fail does this escalate to the existing
    fail-safe path (print a warning, exit 0, data.json/raw_factors.json
    untouched) — same fail-safe semantics, just given more chances to
    succeed first before giving up.
  - When running under GitHub Actions (GITHUB_ACTIONS env var set), any
    fail-safe exit (download-retry exhaustion, low eps_trend coverage, or
    any other uncaught exception) also emits a
    `::warning title=Momentum-5 build skipped::...` annotation (and a
    GITHUB_STEP_SUMMARY line when available) naming the reason and the
    stale as_of date left in data.json, so a skipped run is visible in the
    Actions run summary instead of silently no-op'ing green.

Runs in the weekly-market-update GitHub Actions workflow (wired by maintainer).
"""

import io
import json
import os
import random
import sys
import time
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
# spec v2 (2026-09-16, owner-approved): 20->5 human convergence layer flips
# preference to "already running". This seat-level informational flag mirrors
# one of that rule's two necessary conditions (the other, rev30_avg<=0, reuses
# the existing rev30_avg computed below). Does NOT touch composite/veto/top20
# — see portfolio.json's rules.convergence_v2 for the full spec.
STALLED_PX52WH_MIN = 0.90               # seat px_over_52wh < 0.90 (>10% off 52wk high) -> flag

# spec v3 (2026-09-16, owner-approved): main-line governance goes fully
# mechanical — see apply_mechanical_rotation() below and portfolio.json's
# rules.governance_v3 for the full spec. The 2026-07-02–2026-09-16 human
# judgment period is preserved in changelog, not erased or rewritten.
EXIT_RANK_MAX = 40                      # seat composite rank > 40 -> evict (entry gate stays top-20)
SECTOR_CAP = 2                          # same GICS sector, incumbents included, max 2 seats

# Chinese sector labels (own copy — kept identical to docs/research/momentum-5/
# index.html's SECTOR_ZH table; used only to render theme/thesis text for
# mechanically-filled seats, does not feed any judgment logic).
SECTOR_ZH = {
    'Information Technology': '資訊科技', 'Industrials': '工業', 'Energy': '能源',
    'Health Care': '醫療保健', 'Materials': '原物料', 'Financials': '金融',
    'Consumer Discretionary': '非必需消費', 'Consumer Staples': '必需消費',
    'Utilities': '公用事業', 'Real Estate': '不動產', 'Communication Services': '通訊服務',
}

# 2026-08-20: raw-dump-only constants feeding shadow lines R (residual momentum)
# and H (52-week high) — NOT part of the frozen composite/veto logic above.
RESMOM_REG_WINDOW = 252                # line R: OLS regression window (trading days)
RESMOM_SKIP_DAYS = 21                  # line R: skip most-recent N days from sum/std (short-term reversal)
RESMOM_MIN_OBS = RESMOM_REG_WINDOW + RESMOM_SKIP_DAYS  # 273 — data-sufficiency gate, else null
PX_52WH_WINDOW = 252                   # line H: 52-week-high lookback window (trading days)


# ── download resilience (2026-09-08 fix, plumbing only — see docstring
#    "DOWNLOAD RESILIENCE" section, mirrors build_price_momentum.py's
#    2026-09-07 fix, commit 71cd044e4). Not FROZEN SCREEN SPEC — these only
#    govern how the SAME yf.download call is chunked and retried. Coverage
#    floor reused verbatim from MIN_EPS_COVERAGE below (no new number). ──
DOWNLOAD_BATCH_SIZE = 100
MAX_DOWNLOAD_ATTEMPTS = 4
RETRY_BACKOFF_SECONDS = (20.0, 60.0, 150.0)  # before attempts 2, 3, 4 respectively


def _count_price_sufficient(px, tickers):
    """How many of `tickers` have >=260 dropna'd closes in `px` (mirrors
    run_screen()'s own per-ticker sufficiency check `if len(c) < 260:
    continue` below). Used only by the download-retry gate — does not
    touch or replace that downstream loop."""
    n = 0
    for t in tickers:
        try:
            c = px[t]['Close'].dropna()
        except Exception:
            continue
        if len(c) >= 260:
            n += 1
    return n


def _download_prices_once(all_tickers):
    """One attempt: download all_tickers (already includes 'SPY') in
    DOWNLOAD_BATCH_SIZE-sized chunks with the SAME yf.download kwargs the
    old single-shot call used, then concat into one DataFrame with the
    same px[ticker]['Close'] column shape. A chunk that raises is skipped
    (not fatal by itself) — the resulting SPY/coverage check in the caller
    decides whether this whole attempt counts as a failure."""
    frames = []
    n_chunks = (len(all_tickers) + DOWNLOAD_BATCH_SIZE - 1) // DOWNLOAD_BATCH_SIZE
    for i in range(0, len(all_tickers), DOWNLOAD_BATCH_SIZE):
        chunk = all_tickers[i:i + DOWNLOAD_BATCH_SIZE]
        chunk_no = i // DOWNLOAD_BATCH_SIZE + 1
        try:
            frames.append(yf.download(chunk, period='2y', interval='1d', auto_adjust=True,
                                       group_by='ticker', progress=False, threads=True))
        except Exception as e:
            print(f"      ! batch {chunk_no}/{n_chunks} ({len(chunk)} tickers) raised "
                  f"{type(e).__name__}: {e} — skipped this batch")
        if chunk_no < n_chunks:
            time.sleep(3)
    if not frames:
        raise RuntimeError("all download batches failed")
    return pd.concat(frames, axis=1)


def download_prices_with_retry(tickers):
    """Retry the whole batched price download up to MAX_DOWNLOAD_ATTEMPTS
    times with exponential backoff + jitter whenever SPY comes back empty
    or price coverage is short. Returns (px, spy) on success; raises
    RuntimeError after the retry budget is exhausted (caught by main()'s
    existing top-level except Exception -> fail-safe exit 0, same
    semantics as before)."""
    all_tickers = tickers + ['SPY']
    last_reason = None
    for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
        print(f"  · price download attempt {attempt}/{MAX_DOWNLOAD_ATTEMPTS} "
              f"({len(all_tickers)} tickers incl. SPY, batches of {DOWNLOAD_BATCH_SIZE})")
        try:
            px = _download_prices_once(all_tickers)
            spy = px['SPY']['Close'].dropna()
        except Exception as e:
            last_reason = f"attempt {attempt} raised {type(e).__name__}: {e}"
            print(f"    ! {last_reason}")
        else:
            if spy.empty:
                last_reason = f"attempt {attempt}: SPY price series empty after download"
                print(f"    ! {last_reason}")
            else:
                n_sufficient = _count_price_sufficient(px, tickers)
                if n_sufficient < MIN_EPS_COVERAGE:
                    last_reason = (f"attempt {attempt}: price coverage {n_sufficient} "
                                    f"< {MIN_EPS_COVERAGE}")
                    print(f"    ! {last_reason}")
                else:
                    print(f"    ✓ attempt {attempt} succeeded: SPY ok, "
                          f"price coverage {n_sufficient} >= {MIN_EPS_COVERAGE}")
                    return px, spy
        if attempt < MAX_DOWNLOAD_ATTEMPTS:
            backoff = RETRY_BACKOFF_SECONDS[attempt - 1] + random.uniform(0, 5)
            print(f"    … retrying in {backoff:.0f}s")
            time.sleep(backoff)
    raise RuntimeError(
        f"price download failed after {MAX_DOWNLOAD_ATTEMPTS} attempts (last: {last_reason})")


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

    # ── prices (batch, 2y adjusted daily; batched download + retry, 2026-09-08
    #    fix — see download_prices_with_retry docstring) ──
    px, spy = download_prices_with_retry(tickers)
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
            tk = yf.Ticker(t)
            eh = tk.earnings_history
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
            result = dict(surprise_pct=float(sp) * 100.0, surprise_date=date_iso, report_date=None)
            # report_date (2026-09-16 addition): the ACTUAL announcement date,
            # from the same yf.Ticker(t) object's get_earnings_dates() call —
            # distinct from surprise_date above (fiscal-period END date). Feeds
            # build_momentum5_short.py's PEAD freshness window, which needs the
            # real announcement date, not the quarter-end. Raw-dump passthrough
            # only — does not touch surprise_pct/surprise_date or anything in
            # the frozen composite/veto logic. Best-effort: any failure here
            # just leaves report_date=None.
            try:
                ed = tk.get_earnings_dates(limit=8)
                if ed is not None and not ed.empty and 'Reported EPS' in ed.columns:
                    ed_idx = ed.index
                    if getattr(ed_idx, 'tz', None) is not None:
                        ed_idx = ed_idx.tz_localize(None)
                    today = pd.Timestamp(datetime.now(timezone.utc).date())
                    mask = (ed_idx <= today) & ed['Reported EPS'].notna().to_numpy()
                    reported = ed_idx[mask]
                    if len(reported):
                        result['report_date'] = reported.max().date().isoformat()
            except Exception:
                pass
            return t, result
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


def _fmt_pct_zh(v, decimals=1):
    """'+x.x%' / '-x.x%' / '—' — used only for mechanical-rotation changelog
    and auto-generated thesis text, not for any judgment logic."""
    if v is None:
        return '—'
    return f"{'+' if v > 0 else ''}{v:.{decimals}f}%"


def apply_mechanical_rotation(portfolio, univ, as_of, sector_map):
    """v3 (2026-09-16, owner-approved) — Momentum-5 main line goes fully
    mechanical. Mutates `portfolio` in place (seats/rules/changelog/
    last_rotation_month) and persists it to PORTFOLIO_JSON; also returns
    `portfolio` for convenience/testability. Pure w.r.t. inputs otherwise —
    no other global state read, so it can be imported and unit-tested with a
    synthetic `portfolio` dict + a synthetic `univ` DataFrame (must carry
    columns: eligible, rev30_fy1, rev30_fy2, px_over_52wh, rank, price,
    sector). The 2026-07-02–2026-09-16 human-curated period is untouched
    history in changelog — this function only ever appends.

    CADENCE: runs only when as_of's calendar month != portfolio's
    last_rotation_month (mirrors the shadow track's "first successful weekly
    update of the month" convention). A same-month call is a total no-op —
    it does not even read/write portfolio.json again. On a new month it
    ALWAYS updates last_rotation_month and writes the file, even if zero
    seats actually turn over (so the gate correctly advances either way).

    EVICT (any one of, checked only for seats holding a ticker):
      - ticker not present in this week's univ (delisted / dropped from the
        index) — checked first, short-circuits the other checks below;
      - eligible is False (failed one of the three frozen vetoes);
      - rev30_avg (mean of rev30_fy1/rev30_fy2, missing counts as failing)
        <= 0;
      - px_over_52wh < STALLED_PX52WH_MIN (0.90, i.e. >10% off the 52-week
        high) — same threshold as the seat-card 'stalled' flag;
      - (only checked when eligible, since rank is only defined for the
        eligible universe) composite rank > EXIT_RANK_MAX (40) — the entry
        gate stays the top-20 pool, exit is deliberately looser (top-40) to
        cut back-and-forth churn.
    A seat's sleeve settles at eviction: sleeve_at_entry * close/entry_price
    (or unchanged if this week's close is unavailable) becomes that seat's
    new sleeve_at_entry, i.e. it goes to cash and stays there — mirrors
    build_momentum5_short.py's sleeve settlement.

    FILL: empty seats (freshly evicted this run, or already empty from a
    prior month) are filled, in score order, from this week's eligible
    top-20 pool, excluding: current holders (post-eviction), any candidate
    with rev30_avg <= 0 or px_over_52wh < 0.90, and any candidate whose GICS
    sector already holds SECTOR_CAP (2) seats (incumbents counted). Filling
    stops when seats run out OR the top-20 pool is exhausted — an unfillable
    seat is deliberately left empty (cash), never force-filled. A filled
    seat gets ticker/entry_date=as_of/entry_price=this week's close/
    weight_pct(unchanged, 20)/theme(GICS sector, Chinese)/an auto-generated
    thesis string; sleeve_at_entry is whatever cash value the seat already
    holds (untouched by the fill step itself).
    """
    current_month = as_of[:7]
    if portfolio.get('last_rotation_month') == current_month:
        return portfolio  # not this month's rotation window yet — total no-op

    seats = portfolio['seats']
    rules = portfolio.setdefault('rules', {})
    changelog = portfolio.setdefault('changelog', [])

    def g(t, col, default=None):
        if t is not None and t in univ.index and col in univ.columns:
            v = univ.at[t, col]
            if pd.notna(v):
                return float(v) if isinstance(v, (int, float, np.floating, np.integer)) else v
        return default

    def rev30_avg_of(t):
        vals = [v for v in (g(t, 'rev30_fy1'), g(t, 'rev30_fy2')) if v is not None]
        return sum(vals) / len(vals) if vals else None

    # ── evict ──
    evicted = []
    kept_seats = []
    for seat in seats:
        t = seat.get('ticker')
        if t is None:
            kept_seats.append(seat)  # already empty; fill step below may fill it
            continue
        reasons = []
        if t not in univ.index:
            reasons.append('下市／剔除指數')
        else:
            eligible = bool(univ.at[t, 'eligible']) if pd.notna(univ.at[t, 'eligible']) else False
            if not eligible:
                reasons.append('三否決未過')
            rev30_avg = rev30_avg_of(t)
            if rev30_avg is None or rev30_avg <= 0:
                reasons.append('30D 修正≤0')
            px52 = g(t, 'px_over_52wh')
            if px52 is None or px52 < STALLED_PX52WH_MIN:
                reasons.append('距 52 週高點>10%')
            if eligible:
                rank = g(t, 'rank')
                if rank is None or rank > EXIT_RANK_MAX:
                    reasons.append('排名>40')
        if not reasons:
            kept_seats.append(seat)
            continue
        close = g(t, 'price')
        entry = float(seat['entry_price'])
        sleeve_at_entry = float(seat.get('sleeve_at_entry', 100.0 / len(seats)))
        settled = round(sleeve_at_entry * (close / entry), 2) if close is not None else round(sleeve_at_entry, 2)
        ret_pct = round((close / entry - 1) * 100, 1) if close is not None else None
        evicted.append({'ticker': t, 'reasons': reasons, 'entry_price': entry,
                         'close': close, 'ret_pct': ret_pct, 'settled': settled})
        kept_seats.append({
            'ticker': None, 'entry_date': None, 'entry_price': None,
            'weight_pct': seat.get('weight_pct', 20), 'theme': None, 'thesis': None,
            'sleeve_at_entry': settled,
        })

    # ── fill ──
    current_tickers = {s['ticker'] for s in kept_seats if s['ticker']}
    sector_counts = {}
    for s in kept_seats:
        if s['ticker']:
            sec = sector_map.get(s['ticker'])
            if sec:
                sector_counts[sec] = sector_counts.get(sec, 0) + 1

    elig_sorted = univ[univ['eligible']].sort_values('score', ascending=False)
    top20 = elig_sorted.head(20)

    filled = []
    for seat in kept_seats:
        if seat['ticker'] is not None:
            continue
        chosen = None
        for t in top20.index:
            if t in current_tickers:
                continue
            rev30_avg = rev30_avg_of(t)
            if rev30_avg is None or rev30_avg <= 0:
                continue
            px52 = g(t, 'px_over_52wh')
            if px52 is None or px52 < STALLED_PX52WH_MIN:
                continue
            sec = sector_map.get(t)
            if sec and sector_counts.get(sec, 0) >= SECTOR_CAP:
                continue
            chosen = t
            break
        if chosen is None:
            continue  # no qualifying candidate left — leave this seat empty (cash)
        close = g(chosen, 'price')
        rank = g(chosen, 'rank')
        rev_fy1, rev_fy2 = g(chosen, 'rev_fy1'), g(chosen, 'rev_fy2')
        rev30_avg = rev30_avg_of(chosen)
        px52 = g(chosen, 'px_over_52wh')
        px52_diff_pct = (px52 - 1) * 100 if px52 is not None else None
        sec_en = sector_map.get(chosen)
        sec_zh = SECTOR_ZH.get(sec_en, sec_en or '')
        thesis = (f"機械進場：composite 第 {int(rank) if rank is not None else '—'} 名，"
                  f"FY1／FY2 90 天上修 {_fmt_pct_zh(rev_fy1)}／{_fmt_pct_zh(rev_fy2)}，"
                  f"30 天 {_fmt_pct_zh(rev30_avg)}，距 52 週高點 {_fmt_pct_zh(px52_diff_pct)}")
        seat['ticker'] = chosen
        seat['entry_date'] = as_of
        seat['entry_price'] = round(close, 2) if close is not None else None
        seat['weight_pct'] = seat.get('weight_pct', 20)
        seat['theme'] = sec_zh
        seat['thesis'] = thesis
        # sleeve_at_entry already holds the correct cash figure (settled at
        # eviction, or carried over from an earlier empty month) — untouched.
        sector_counts[sec_en] = sector_counts.get(sec_en, 0) + 1
        current_tickers.add(chosen)
        filled.append({'ticker': chosen, 'sector_zh': sec_zh})

    portfolio['seats'] = kept_seats
    portfolio['last_rotation_month'] = current_month
    rules['governance_v3'] = (
        "2026-09-16 起全機械：每月第一個成功週更由程式依 v2 條件踢出／補位，"
        "人工不再介入；2026-07-02 至 2026-09-16 為人工裁決期，紀錄保留"
    )

    n_empty = sum(1 for s in kept_seats if s['ticker'] is None)
    if evicted or filled:
        evict_desc = '、'.join(
            f"{e['ticker']}（{_fmt_pct_zh(e['ret_pct'])}，{'／'.join(e['reasons'])}）" for e in evicted
        ) or '無'
        fill_desc = '、'.join(f"{f['ticker']}（{f['sector_zh']}）" for f in filled) or '無'
        changelog.append({
            'date': as_of,
            'event': f"月度機械換席：踢出 {evict_desc}；補入 {fill_desc}；留空 {n_empty} 席。",
        })
    else:
        changelog.append({
            'date': as_of,
            'event': '月度機械檢查：五席全數維持（否決／30D 修正／距高點／排名皆過關），無異動。',
        })

    # Persisted by main() AFTER data.json / raw_factors.json are written, so a
    # crash mid-build can't leave portfolio.json rotated while data.json lags.
    print(f"  ✓ mechanical rotation ({current_month}): "
          f"evicted={[e['ticker'] for e in evicted]} filled={[f['ticker'] for f in filled]} "
          f"empty_seats={n_empty}")
    return portfolio


def build():
    now = datetime.now(timezone.utc)
    as_of = now.strftime('%Y-%m-%d')
    print(f"=== Momentum-5 Build: {as_of} ===")

    portfolio = json.loads(PORTFOLIO_JSON.read_text(encoding='utf-8'))
    bench_cfg = portfolio.get('bench', [])
    spy_entry = float(portfolio['benchmark']['entry_price'])

    univ, spy_close, spy6, coverage = run_screen()

    # ── fail-safe: insufficient coverage -> leave data.json untouched ──
    if coverage['eps_trend'] < MIN_EPS_COVERAGE:
        print(f"  ✗ eps_trend coverage {coverage['eps_trend']} < {MIN_EPS_COVERAGE} "
              f"— aborting, data.json left unchanged")
        _emit_gh_skip_warning(
            f"eps_trend coverage {coverage['eps_trend']} < {MIN_EPS_COVERAGE}")
        return None

    # ── mechanical rotation (v3, 2026-09-16): monthly, fully automatic —
    #    mutates + persists portfolio.json in place; re-bind seats_cfg after. ──
    sector_map = univ['sector'].to_dict()
    rotated = portfolio.get('last_rotation_month') != as_of[:7]
    apply_mechanical_rotation(portfolio, univ, as_of, sector_map)
    seats_cfg = portfolio['seats']

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
        # 2026-09-16: sleeve accounting. Each seat is a 20-unit sleeve at
        # inception; when a seat is swapped, portfolio.json records the sleeve
        # value the outgoing name settled to as the incoming name's
        # sleeve_at_entry, so realised P&L stays in the headline return instead
        # of vanishing with the swapped-out ticker. Missing key = 20 (untouched).
        sleeve = float(s.get('sleeve_at_entry', 100.0 / len(seats_cfg)))
        if t is None:
            # v3 (2026-09-16): empty seat left by apply_mechanical_rotation()
            # (no qualifying candidate) — held as cash, contributes its sleeve
            # value unchanged to port_ret, no metrics/flags to compute.
            seat_rets.append(sleeve)
            seats_out.append({
                'ticker': None, 'close': None, 'ret_since_entry_pct': None,
                'rev_fy1': None, 'rev_fy2': None, 'rev30_avg': None,
                'px_over_52wh': None, 'score': None, 'rank': None, 'flags': [],
            })
            continue
        close = g(t, 'price')
        entry = float(s['entry_price'])
        ret_since = round((close / entry - 1) * 100, 1) if close is not None else None
        seat_rets.append(sleeve * (close / entry) if close is not None else sleeve)

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

        # v2 收斂規則（2026-09-16）「已在跑優先」的兩個必要條件——30D 修正轉負
        # 或已遠離 52 週高點 10% 以上——任一不成立就亮 stalled，供人工複審參考。
        px_over_52wh = g(t, 'px_over_52wh')
        if (rev30_avg is not None and rev30_avg <= 0) or \
           (px_over_52wh is not None and px_over_52wh < STALLED_PX52WH_MIN):
            flags.append('stalled')

        seats_out.append({
            'ticker': t,
            'close': round(close, 2) if close is not None else None,
            'ret_since_entry_pct': ret_since,
            'rev_fy1': round(rev_fy1, 1) if rev_fy1 is not None else None,
            'rev_fy2': round(rev_fy2, 1) if rev_fy2 is not None else None,
            'rev30_avg': round(rev30_avg, 1) if rev30_avg is not None else None,
            'px_over_52wh': round(px_over_52wh, 4) if px_over_52wh is not None else None,
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
    port_ret = round((sum(seat_rets) / 100.0 - 1) * 100, 1) if seat_rets else None
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
            'report_date': gv_str(t, 'report_date'),
            'resmom': gv(t, 'resmom'),
            'px_over_52wh': gv(t, 'px_over_52wh'),
            'sector': gv_str(t, 'sector'),  # 2026-09-16: raw-dump passthrough, feeds Fast line's sector cap
        })
    surprise_coverage = sum(1 for r in raw_universe if r['surprise_pct'] is not None)
    resmom_coverage = sum(1 for r in raw_universe if r['resmom'] is not None)
    px52wh_coverage = sum(1 for r in raw_universe if r['px_over_52wh'] is not None)
    # report_date (2026-09-16 addition): the actual announcement date, distinct
    # from surprise_date's fiscal-period-end date — see surprise_info()'s
    # docstring comment above. Feeds build_momentum5_short.py's PEAD freshness
    # window; raw-dump passthrough only.
    report_date_coverage = sum(1 for r in raw_universe if r['report_date'] is not None)
    raw_payload = {
        'as_of': as_of,
        'spy_close': round(spy_close, 2),
        'spy6': float(spy6),  # SPY's own 6M return — needed to rebuild relmom6 = mom6 - spy6
        'surprise_coverage': surprise_coverage,
        'report_date_coverage': report_date_coverage,
        'resmom_coverage': resmom_coverage,
        'px52wh_coverage': px52wh_coverage,
        'universe': raw_universe,
    }

    return payload, raw_payload, (portfolio if rotated else None)


def _existing_data_json_as_of():
    """Best-effort read of the current data.json's as_of, for the GH Actions
    warning annotation below. Must never raise — a missing or corrupt file
    just reads as unknown."""
    try:
        if DATA_JSON.exists():
            return json.loads(DATA_JSON.read_text(encoding='utf-8')).get('as_of')
    except Exception:
        pass
    return None


def _emit_gh_skip_warning(reason):
    """Failure-visibility fix (2026-09-08, mirrors build_price_momentum.py's
    2026-09-07 fix, commit 71cd044e4): a fail-safe abort or uncaught
    exception used to be a silent exit 0 (green workflow run, no trace).
    When running under GitHub Actions, also emit a `::warning::` workflow
    command so it shows up in the run summary, plus a GITHUB_STEP_SUMMARY
    line when available. No-op on a local run (keeps local output clean)."""
    if not os.environ.get('GITHUB_ACTIONS'):
        return
    stale_as_of = _existing_data_json_as_of() or '（無既有 data.json）'
    msg = f"{reason}；data.json 未更新，本週資料停在 {stale_as_of}"
    print(f"::warning title=Momentum-5 build skipped::{msg}")
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_path:
        try:
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write(f"- ⚠️ **Momentum-5 build skipped** — {msg}\n")
        except Exception:
            pass


def main():
    try:
        result = build()
    except Exception as e:
        # any screen/scrape failure -> keep last good data.json
        print(f"  ✗ screen failed ({type(e).__name__}: {e}) — data.json left unchanged")
        _emit_gh_skip_warning(f"screen failed ({type(e).__name__}: {e})")
        sys.exit(0)

    if result is None:
        # coverage fail-safe already logged (warning already emitted in build())
        sys.exit(0)

    payload, raw_payload, rotated_portfolio = result

    DATA_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + '\n',
                         encoding='utf-8')
    print(f"  ✓ wrote {DATA_JSON.relative_to(ROOT)}")
    print(f"    coverage: {payload['coverage']}")
    print(f"    portfolio: {payload['portfolio']}")
    print("    seats:")
    for s in payload['seats']:
        flags = ('  [' + ','.join(s['flags']) + ']') if s['flags'] else ''
        print(f"      {(s['ticker'] or '(空席)'):<5} close={s['close']}  ret={s['ret_since_entry_pct']}%  "
              f"revFY1={s['rev_fy1']}  revFY2={s['rev_fy2']}  score={s['score']}  "
              f"rank={s['rank']}{flags}")

    RAW_FACTORS_JSON.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=1) + '\n',
                                encoding='utf-8')
    print(f"  ✓ wrote {RAW_FACTORS_JSON.relative_to(ROOT)} "
          f"({len(raw_payload['universe'])} tickers, "
          f"surprise_coverage={raw_payload['surprise_coverage']}, "
          f"report_date_coverage={raw_payload['report_date_coverage']}, "
          f"resmom_coverage={raw_payload['resmom_coverage']}, "
          f"px52wh_coverage={raw_payload['px52wh_coverage']})")

    if rotated_portfolio is not None:
        # v3 mechanical rotation ran this month — persist portfolio.json last,
        # after data.json / raw_factors.json, so the three files move together.
        PORTFOLIO_JSON.write_text(json.dumps(rotated_portfolio, ensure_ascii=False, indent=1) + '\n',
                                  encoding='utf-8')
        print(f"  ✓ wrote {PORTFOLIO_JSON.relative_to(ROOT)} (mechanical rotation persisted)")


if __name__ == '__main__':
    main()
