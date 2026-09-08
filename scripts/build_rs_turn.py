"""
RS Turn ("轉強觀察") — zero-LLM daily builder for docs/rs-turn/.

WHAT THIS IS
------------
A pure-technical discovery-layer screener that sits next to scripts/screener.py
(RS+VCP): that one finds names that are ALREADY leading and coiling; this one
finds names that pulled back hard and whose relative strength (vs QQQ) just
turned up again — "從弱轉強", not "貼高". It is NOT a convergence surface
(2026-07-07 policy): output never feeds picks/GRP/dd-screener/cockpit rankings,
only two plain links (docs/screeners.html card, docs/cockpit disc-link).

Also produces a breadth line — how many names pass the full screen each day,
recomputed over a fixed trailing window (see BREADTH section) — as a
mechanism-only descriptor ("a batch of names turning strong together"), never
a timing call. See notes/site-internal/root/_rs_turn_design_20260908.md.

All thresholds live in PARAMS below + DEFINITION_VERSION; both are written
into every output JSON so a future parameter change is auditable per-date via
version_by_date in history.json (definitions are frozen per date, not
silently rewritten).

UNIVERSE
--------
data/engine/universe.json (S&P 500 ∪ Nasdaq-100 ∪ S&P 400 ∪ DD-pool US, month-
updated, committed) UNION a Russell 1000 proxy — Nasdaq's own full-market
screener ranked by market cap, top ~1,000 kept (Russell 1000 is itself the
top ~1,000 US-listed stocks by market cap, reconstituted every June, so this
is a reasonable stand-in for actual index membership; Wikipedia's R1000 page
no longer carries a constituents table at all, so that source was dropped —
see fetch_r1000_proxy() below), iShares IWB holdings CSV as a second fallback,
30-day local cache at data/rs_turn/universe.json since none of these external
sources are committed to the repo. This is the only path that reaches very-
recent-IPO / not-yet-indexed names (CRCL, BLSH, NBIS, GLXY, IREN, ALM, SNDK-
style names) which is exactly the population this screen wants to catch
turning early.

DOWNLOAD RESILIENCE (2026-09-08, copied from scripts/build_momentum5.py's
"DOWNLOAD RESILIENCE (2026-09-08 fix)" section verbatim in shape — batch/
backoff/coverage-floor/fail-safe — because this screen's universe (~1,000-
1,080 tickers) is comparable in size and yfinance 429s are the same failure
mode)
--------------------------------------------------------------------------
  - tickers + [benchmark] downloaded in ~100-ticker batches (identical
    yf.download kwargs per batch), concatenated into one DataFrame with the
    same px.xs('Close', axis=1, level=1) / px.xs('Volume', ...) column shape.
  - Whole batched download retried up to 4 attempts total, exponential
    backoff + jitter (~20s / 60s / 150s) between attempts, whenever the
    benchmark comes back empty OR the fraction of tickers with >= MIN_BARS
    (260) daily bars is below PARAMS['coverage_floor_pct'] (0.85 — this
    script's OWN existing fail-safe number, not invented for the retry gate).
  - Only after all attempts fail does this escalate to the fail-safe path:
    print a warning, exit 0, latest.json/history.json left untouched.
  - This build step runs LAST in the daily-us-close.yml band (after
    "[monitor] Build home pulse"), deliberately as far from screener.py's own
    ~510-ticker burst as the band allows, per the design spec §3.

METRICS + SIX CONDITIONS
-------------------------
See PARAMS + compute_metrics()/compute_breadth() below; §4/§5 of the design
spec is the authority for every formula. Everything is vectorized over wide
DataFrames (date × ticker) — no per-ticker/per-day Python loop for the metric
math; the only per-ticker loops are over the small "passed today" subset when
assembling the JSON rows (a few dozen names, not the ~1,000-ticker universe).

Runs in .github/workflows/daily-us-close.yml (US close band), wired by the
maintainer as the last build step before "Commit and push".
"""

import io
import json
import os
import random
import re
import sys
import time
import warnings
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
ENGINE_UNIVERSE_JSON = ROOT / 'data' / 'engine' / 'universe.json'
RS_TURN_UNIVERSE_JSON = ROOT / 'data' / 'rs_turn' / 'universe.json'
DATA_DIR = ROOT / 'docs' / 'rs-turn' / 'data'
LATEST_JSON = DATA_DIR / 'latest.json'
HISTORY_JSON = DATA_DIR / 'history.json'
DOCS_T_DIR = ROOT / 'docs' / 't'

BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
NASDAQ_SCREENER_URL = (
    'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=5000&offset=0&download=true'
)
ISHARES_IWB_URL = (
    'https://www.ishares.com/us/products/239707/ishares-russell-1000-etf/'
    '1467271812596.ajax?fileType=csv&fileName=IWB_holdings&dataType=fund'
)

DEFINITION_VERSION = "v2"

# ── PARAMS (LOCKED — all thresholds live here + DEFINITION_VERSION; a change
#    requires bumping DEFINITION_VERSION, see design spec §0 "參數凍結") ──
PARAMS = {
    # six-condition thresholds (design spec §4)
    "rs_accel_min": 20,           # pt — condition 1 (v2, 2026-09-08: tightened 10->20, owner
                                  # feedback that the v1 list (~50 names) was far broader than the
                                  # ~15-name reference post; grid-searched, see design spec §4 note)
    "rs21_min": 0,                # pt — condition 1
    "pullback_min_pct": -25,      # % — condition 2 (pullback_pct <= this; v2: tightened -15->-25, same sweep)
    "dist_high_max_pct": -8,      # % — condition 5 (dist_high_pct <= this)
    "range_pos_min": 0.7,         # 0-1 — condition 4 (range_pos >= this)
    "adv_min_usd": 20000000,      # condition 6
    "price_min": 5,               # condition 6
    "accel_label_min": 25,        # pt — "偏加速中" status label threshold (v2: raised 20->25 in lockstep
                                  # with rs_accel_min's 10->20 so the label still marks a tier ABOVE the
                                  # entry gate, not merely "cleared the gate")
    "deep_pullback_tag_min_pct": -25,  # tag rule: pullback_pct <= this
    # scope / data-quality thresholds
    "benchmark": "QQQ",
    "breadth_window": 250,        # trading days recomputed each run (§5)
    "min_bars": 260,              # per-ticker sufficiency floor (§3)
    "coverage_floor_pct": 0.85,   # universe fraction with >= min_bars (§3)
    "universe_min": 700,          # union floor below which the build aborts (§2.4)
    "universe_cache_days": 30,    # data/rs_turn/universe.json cache TTL (§2.4)
    "r1000_proxy_n": 1300,        # Nasdaq list includes ADRs/foreign names Russell excludes, so top-1000 there cuts off ~$8B vs the real R1000 breakpoint ~$4-5B; 1300 corrects for that
}

# ── download resilience (2026-09-08, mirrors build_momentum5.py's own
#    2026-09-08 fix — see module docstring) ──
DOWNLOAD_BATCH_SIZE = 100
MAX_DOWNLOAD_ATTEMPTS = 4
RETRY_BACKOFF_SECONDS = (20.0, 60.0, 150.0)  # before attempts 2, 3, 4 respectively

TICKER_RE = re.compile(r'^[A-Z0-9-]{1,10}$')
# Class-share tickers with a single-letter suffix after a dot (BRK.B, BF.B,
# MOG.A) -> dash form (BRK-B, BF-B, MOG-A) so yfinance resolves them. Any
# OTHER dotted/suffixed symbol is left alone here and gets excluded by
# TICKER_RE downstream (unchanged behavior) rather than guessed at.
CLASS_SHARE_DOT_RE = re.compile(r'^[A-Z]+\.[A-Z]$')
# Nasdaq screener proxy: only keep plain 1-5 letter common-stock symbols —
# drops units/warrants/preferreds/class shares which the API represents with
# ^ / . etc. (design spec §2).
NASDAQ_SYMBOL_RE = re.compile(r'^[A-Z]{1,5}$')
NASDAQ_BAD_NAME_SUBSTRINGS = (
    'Warrant', 'Warrants', ' Unit', 'Units', 'Preferred',
    'Depositary Shares', 'Depositary Receipt', ' ETF', 'Fund', 'Notes', 'Debentures', 'Subordinated',
)


def _normalize_ticker(sym):
    """Apply the class-share dot->dash fix (see CLASS_SHARE_DOT_RE above);
    otherwise return the symbol unchanged."""
    return sym.replace('.', '-') if CLASS_SHARE_DOT_RE.match(sym) else sym


def _warn(msg):
    """Always print a ::warning:: line (GitHub Actions parses this from plain
    stdout regardless of GITHUB_ACTIONS env; harmless plain text locally)."""
    print(f"::warning::rs-turn: {msg}")


# ── universe: engine ∪ Russell 1000 (§2) ────────────────────────────────────
def load_engine_universe():
    return [_normalize_ticker(str(r['ticker']).strip().upper())
            for r in json.loads(ENGINE_UNIVERSE_JSON.read_text(encoding='utf-8')).get('tickers', [])]


def _clean_tickers(raw):
    out = set()
    for s in raw:
        if s is None:
            continue
        s = str(s).strip().upper()
        if not s or s in ('NAN', 'NONE'):
            continue
        s = re.sub(r'\[[^\]]*\]', '', s).strip()  # strip stray footnote-style markers
        s = _normalize_ticker(s)                   # BRK.B -> BRK-B; other dots stay excluded below
        if TICKER_RE.match(s):
            out.add(s)
    return sorted(out)


# Wikipedia's Russell 1000 page (tried here through 2026-09-08) no longer
# carries a constituents table at all (verified: 71 <tr> total, only summary/
# return tables) — dead source, removed rather than left as a permanent
# guaranteed-fail network call. Nasdaq's own full-market screener (below) is
# used as a market-cap-ranked proxy for the index instead: Russell 1000 is,
# by construction, the top ~1,000 US-listed stocks by market cap
# (reconstituted every June), so a fresh full-market screen ranked the same
# way is a reasonable stand-in for the actual membership list.
def fetch_r1000_proxy():
    headers = {'User-Agent': BROWSER_UA, 'Accept': 'application/json'}
    rows = None
    last_err = None
    for attempt in (1, 2):
        try:
            r = requests.get(NASDAQ_SCREENER_URL, headers=headers, timeout=30)
            rows = (r.json().get('data') or {}).get('rows') or []
            break
        except Exception as e:
            last_err = e
            if attempt == 1:
                print(f"    Nasdaq screener fetch failed (attempt 1): "
                      f"{type(e).__name__}: {e} — retrying in 10s")
                time.sleep(10)
    if not rows:
        print(f"    Nasdaq screener fetch failed: "
              f"{type(last_err).__name__ if last_err else 'empty response'}: {last_err or ''}")
        return None

    candidates = []
    for row in rows:
        sym = str(row.get('symbol', '') or '').strip().upper()
        name = str(row.get('name', '') or '')
        if not NASDAQ_SYMBOL_RE.match(sym):
            continue
        if any(bad in name for bad in NASDAQ_BAD_NAME_SUBSTRINGS):
            continue
        try:
            mc = float(str(row.get('marketCap', '')).replace(',', '').strip())
        except (TypeError, ValueError):
            continue
        if mc <= 0:
            continue
        candidates.append((sym, mc))

    if len(candidates) < 500:
        print(f"    Nasdaq screener parsed but only {len(candidates)} usable rows "
              f"(< 500) — treating as failure")
        return None

    candidates.sort(key=lambda x: x[1], reverse=True)
    return sorted({sym for sym, _ in candidates[:PARAMS['r1000_proxy_n']]})


def scrape_r1000_ishares():
    try:
        r = requests.get(ISHARES_IWB_URL, headers={'User-Agent': BROWSER_UA}, timeout=30)
        text = r.text
    except Exception as e:
        print(f"    iShares IWB fetch failed: {type(e).__name__}: {e}")
        return None
    lines = text.splitlines()
    header_idx = None
    for i, ln in enumerate(lines):
        cells = [c.strip().strip('"') for c in ln.split(',')]
        if 'Ticker' in cells and 'Asset Class' in cells:
            header_idx = i
            break
    if header_idx is None:
        print("    iShares IWB CSV: no 'Ticker'/'Asset Class' header row found "
              "(blocked, interstitial page, or format changed)")
        return None
    try:
        df = pd.read_csv(io.StringIO('\n'.join(lines[header_idx:])), thousands=',')
    except Exception as e:
        print(f"    iShares IWB CSV parse failed: {type(e).__name__}: {e}")
        return None
    if 'Asset Class' in df.columns:
        df = df[df['Asset Class'] == 'Equity']
    cleaned = _clean_tickers(df.get('Ticker', pd.Series(dtype=str)).tolist())
    if len(cleaned) >= 500:
        return cleaned
    print(f"    iShares IWB CSV parsed but only {len(cleaned)} usable tickers (< 500) "
          f"— treating as failure")
    return None


def fetch_r1000():
    r = fetch_r1000_proxy()
    if r:
        n = PARAMS['r1000_proxy_n']
        print(f"  R1000 via Nasdaq screener proxy (top {n} by market cap): "
              f"{len(r)} tickers")
        return r, f'nasdaq-screener-top{n}'
    print("  Nasdaq screener proxy fetch failed/unusable, trying iShares IWB holdings CSV...")
    r = scrape_r1000_ishares()
    if r:
        print(f"  R1000 via iShares: {len(r)} tickers")
        return r, 'ishares'
    print("  iShares IWB fetch also failed/unusable")
    return None, None


def _is_fresh(fetched_at_str, days):
    try:
        dt = datetime.fromisoformat(str(fetched_at_str).replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days < days
    except Exception:
        return False


def build_universe():
    """Returns (union_ticker_list, payload) or (None, None) on abort (union
    too small — exit 0, no output written, per design spec §2.4)."""
    engine_tickers = load_engine_universe()
    engine_set = set(engine_tickers)
    print(f"  engine universe: {len(engine_set)} tickers")

    cache = None
    if RS_TURN_UNIVERSE_JSON.exists():
        try:
            cache = json.loads(RS_TURN_UNIVERSE_JSON.read_text(encoding='utf-8'))
        except Exception:
            cache = None

    if (cache and _is_fresh(cache.get('fetched_at', ''), PARAMS['universe_cache_days'])
            and len(cache.get('tickers', [])) >= PARAMS['universe_min']):
        print(f"  universe cache fresh (fetched_at={cache['fetched_at']}) — using cached "
              f"{len(cache['tickers'])} tickers, no network fetch")
        return cache['tickers'], cache

    r1000, r1000_source = fetch_r1000()
    if r1000 is None and cache and cache.get('r1000_tickers'):
        r1000 = cache['r1000_tickers']
        r1000_source = f"stale-cache({cache.get('fetched_at', '?')})"
        print(f"  R1000 live fetch failed both sources; falling back to stale cache's "
              f"R1000 part ({len(r1000)} tickers, cached {cache.get('fetched_at')})")
    if r1000 is None:
        r1000 = []
        r1000_source = 'unavailable'
        _warn("R1000 fetch failed (Wikipedia + iShares) and no usable cache — "
              "falling back to engine-only universe")

    union = sorted(engine_set | set(r1000))
    payload = {
        'fetched_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'n': len(union),
        'sources': {'engine': len(engine_set), 'r1000': len(r1000), 'union': len(union)},
        'r1000_source': r1000_source,
        'r1000_tickers': sorted(set(r1000)),
        'tickers': union,
    }
    if len(union) < PARAMS['universe_min']:
        _warn(f"universe union {len(union)} < {PARAMS['universe_min']} — abort, "
              f"no universe cache or output written")
        return None, None

    RS_TURN_UNIVERSE_JSON.parent.mkdir(parents=True, exist_ok=True)
    RS_TURN_UNIVERSE_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  wrote {RS_TURN_UNIVERSE_JSON.relative_to(ROOT)}: engine={len(engine_set)} "
          f"r1000={len(r1000)} ({r1000_source}) union={len(union)}")
    return union, payload


# ── prices (§3) ──────────────────────────────────────────────────────────
def _count_sufficient(close_wide, tickers, min_bars):
    n = 0
    for t in tickers:
        try:
            c = close_wide[t].dropna()
        except Exception:
            continue
        if len(c) >= min_bars:
            n += 1
    return n


def _download_prices_once(all_tickers):
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
    """Returns (closes, volumes, benchmark_close) — all wide DataFrames/Series
    keyed by date, `closes`/`volumes` columns = tickers (benchmark excluded).
    Raises RuntimeError after MAX_DOWNLOAD_ATTEMPTS (caller -> fail-safe)."""
    benchmark = PARAMS['benchmark']
    req = list(dict.fromkeys(tickers))  # de-dup, preserve order
    all_tickers = req + [benchmark] if benchmark not in req else req
    last_reason = None
    for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
        print(f"  price download attempt {attempt}/{MAX_DOWNLOAD_ATTEMPTS} "
              f"({len(all_tickers)} tickers incl. {benchmark}, batches of {DOWNLOAD_BATCH_SIZE})")
        close_all = None
        bench = pd.Series(dtype=float)
        try:
            px = _download_prices_once(all_tickers)
            close_all = px.xs('Close', axis=1, level=1)
            vol_all = px.xs('Volume', axis=1, level=1)
            if benchmark in close_all.columns:
                bench = close_all[benchmark].dropna()
        except Exception as e:
            last_reason = f"attempt {attempt} raised {type(e).__name__}: {e}"
            print(f"    ! {last_reason}")

        if close_all is not None and not bench.empty:
            n_sufficient = _count_sufficient(close_all, req, PARAMS['min_bars'])
            frac = n_sufficient / len(req) if req else 0.0
            if frac >= PARAMS['coverage_floor_pct']:
                print(f"    ✓ attempt {attempt} succeeded: {benchmark} ok, "
                      f"coverage {n_sufficient}/{len(req)} ({frac:.1%}) >= floor "
                      f"{PARAMS['coverage_floor_pct']:.0%}")
                closes = close_all.drop(columns=[benchmark], errors='ignore')
                volumes = vol_all.drop(columns=[benchmark], errors='ignore')
                return closes, volumes, bench
            last_reason = (f"attempt {attempt}: coverage {n_sufficient}/{len(req)} "
                            f"({frac:.1%}) < floor {PARAMS['coverage_floor_pct']:.0%}")
            print(f"    ! {last_reason}")
        elif bench.empty and close_all is not None:
            last_reason = f"attempt {attempt}: {benchmark} price series empty after download"
            print(f"    ! {last_reason}")

        if attempt < MAX_DOWNLOAD_ATTEMPTS:
            backoff = RETRY_BACKOFF_SECONDS[attempt - 1] + random.uniform(0, 5)
            print(f"    … retrying in {backoff:.0f}s")
            time.sleep(backoff)
    raise RuntimeError(
        f"price download failed after {MAX_DOWNLOAD_ATTEMPTS} attempts (last: {last_reason})")


# ── metrics (§4) — vectorized wide DataFrames, no per-ticker/day loop ──────
def _num(v, ndigits=None):
    """float()/round() that degrades NaN/inf -> None (valid JSON null,
    never a literal NaN token)."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(f):
        return None
    return round(f, ndigits) if ndigits is not None else f


def compute_metrics(closes, volumes, qqq):
    P = PARAMS
    C = closes
    V = volumes
    Q = qqq.reindex(C.index).ffill()

    e21 = C.ewm(span=21, adjust=False).mean()
    e50 = C.ewm(span=50, adjust=False).mean()

    ret21 = C / C.shift(21) - 1.0
    ret63 = C / C.shift(63) - 1.0
    qret21 = Q / Q.shift(21) - 1.0
    qret63 = Q / Q.shift(63) - 1.0

    rs21 = ret21.sub(qret21, axis=0) * 100.0
    rs63 = ret63.sub(qret63, axis=0) * 100.0
    rs_accel = rs21 - rs63

    roll_max_252 = C.rolling(252, min_periods=1).max()
    roll_min_63 = C.rolling(63, min_periods=1).min()
    dist_high_pct = (C / roll_max_252 - 1.0) * 100.0
    pullback_pct = (roll_min_63 / roll_max_252 - 1.0) * 100.0

    above_e21 = C > e21
    e21_up = e21 > e21.shift(5)
    below21 = C < e21
    had_below21_recent = below21.shift(1).rolling(10, min_periods=1).sum() > 0
    reclaimed_e21 = above_e21 & had_below21_recent

    above_e50 = C > e50
    below50 = C < e50
    had_below50_recent = below50.shift(1).rolling(10, min_periods=1).sum() > 0
    crossed_e50 = above_e50 & had_below50_recent
    near_e50 = (C / e50 - 1.0).abs() <= 0.03

    recent_low_10 = C.rolling(10, min_periods=1).min()
    prior_low_20 = C.rolling(20, min_periods=1).min().shift(10)
    higher_low = recent_low_10 > prior_low_20

    min63 = C.rolling(63, min_periods=1).min()
    max63 = C.rolling(63, min_periods=1).max()
    range_pos = (C - min63) / (max63 - min63)

    adv20_usd = (C * V).rolling(20, min_periods=1).mean()

    # data sufficiency: >=252 valid closes in the trailing 252-row window —
    # required for BOTH the breadth denominator (§5 n_eligible) and as an
    # implicit prerequisite for "passed"/"soft" (dist_high_pct/pullback_pct
    # are meaningless over a short/partial lookback for a recent IPO).
    valid_count_252 = C.notna().rolling(252, min_periods=1).sum()
    data_sufficient = valid_count_252 >= 252

    cond1 = (rs21 > P['rs21_min']) & (rs_accel >= P['rs_accel_min'])
    cond2 = pullback_pct <= P['pullback_min_pct']
    cond3 = above_e21 & (reclaimed_e21 | e21_up)
    cond4 = higher_low | (range_pos >= P['range_pos_min'])
    cond5 = dist_high_pct <= P['dist_high_max_pct']
    cond6 = (adv20_usd >= P['adv_min_usd']) & (C >= P['price_min'])

    liquidity_pass = cond6.fillna(False)
    eligible = (data_sufficient & liquidity_pass).fillna(False)

    passed = (cond1 & cond2 & cond3 & cond4 & cond5 & cond6 & data_sufficient).fillna(False)
    soft = ((rs_accel > 0) & above_e21 & data_sufficient).fillna(False)

    return {
        'C': C, 'e21': e21, 'e50': e50,
        'rs21': rs21, 'rs63': rs63, 'rs_accel': rs_accel,
        'dist_high_pct': dist_high_pct, 'pullback_pct': pullback_pct,
        'above_e21': above_e21, 'e21_up': e21_up, 'reclaimed_e21': reclaimed_e21,
        'crossed_e50': crossed_e50, 'near_e50': near_e50, 'higher_low': higher_low,
        'range_pos': range_pos, 'adv20_usd': adv20_usd,
        'passed': passed, 'soft': soft, 'eligible': eligible, 'qqq': Q,
    }


# ── breadth (§5) ────────────────────────────────────────────────────────
def compute_breadth(metrics, closes):
    window = PARAMS['breadth_window']
    dates = closes.index[-window:]
    passed = metrics['passed'].reindex(dates)
    soft = metrics['soft'].reindex(dates)
    eligible = metrics['eligible'].reindex(dates)
    qqq = metrics['qqq'].reindex(dates)

    n_full = passed.sum(axis=1)
    n_soft = soft.sum(axis=1)
    n_eligible = eligible.sum(axis=1)
    pct_full = (n_full / n_eligible.replace(0, np.nan) * 100).fillna(0.0)

    date_strs = [d.strftime('%Y-%m-%d') for d in dates]
    series = {
        'n_full': [[ds, int(n_full.iloc[i])] for i, ds in enumerate(date_strs)],
        'n_soft': [[ds, int(n_soft.iloc[i])] for i, ds in enumerate(date_strs)],
        'n_eligible': [[ds, int(n_eligible.iloc[i])] for i, ds in enumerate(date_strs)],
        'pct_full': [[ds, _num(pct_full.iloc[i], 2)] for i, ds in enumerate(date_strs)],
        'qqq': [[ds, _num(qqq.iloc[i], 2)] for i, ds in enumerate(date_strs)
                if pd.notna(qqq.iloc[i])],
    }
    version_by_date = {ds: DEFINITION_VERSION for ds in date_strs}
    members = {}
    for i, ds in enumerate(date_strs):
        row = passed.iloc[i]
        members[ds] = sorted(row[row].index.tolist())

    return {
        'series': series, 'version_by_date': version_by_date, 'members': members,
        'n_full': n_full, 'n_soft': n_soft, 'n_eligible': n_eligible, 'pct_full': pct_full,
    }


def load_existing_history():
    if not HISTORY_JSON.exists():
        return None
    try:
        return json.loads(HISTORY_JSON.read_text(encoding='utf-8'))
    except Exception:
        return None


def merge_history(existing, series, version_by_date, members, as_of):
    """Whole-window recompute merge: dates inside the freshly-recomputed
    window overwrite; dates outside it (older than the window) are kept
    as-is from the existing file. Deterministic key ordering (sorted by
    date) so a same-day rerun with unchanged inputs is byte-identical."""
    merged_series = {}
    for key, pairs in series.items():
        old = dict(existing.get('series', {}).get(key, [])) if existing else {}
        old.update({d: v for d, v in pairs})
        merged_series[key] = [[d, old[d]] for d in sorted(old.keys())]

    merged_vbd = dict(existing.get('version_by_date', {})) if existing else {}
    merged_vbd.update(version_by_date)
    merged_vbd = {d: merged_vbd[d] for d in sorted(merged_vbd.keys())}

    merged_members = dict(existing.get('members', {})) if existing else {}
    merged_members.update(members)
    merged_members = {d: merged_members[d] for d in sorted(merged_members.keys())}

    return {
        'schema': 'rs-turn-history-v1',
        'benchmark': PARAMS['benchmark'],
        'updated': as_of,
        'definition_version': DEFINITION_VERSION,
        'series': merged_series,
        'version_by_date': merged_vbd,
        'members': merged_members,
    }


def compute_days_on_list(ticker, dates_desc, members_sets):
    streak = 0
    for d in dates_desc:
        if ticker in members_sets.get(d, ()):
            streak += 1
        else:
            break
    return streak


# ── tags (§4 "入選原因") ────────────────────────────────────────────────
def build_tags(pullback_v, reclaimed_v, e21_up_v, crossed_v, near_v, higher_v, range_pos_v):
    tags = []
    tags.append('深回檔後相對強度急拉' if (pullback_v is not None
                and pullback_v <= PARAMS['deep_pullback_tag_min_pct'])
                else '回檔後相對強度改善')
    if reclaimed_v:
        tags.append('剛站回 21 日線')
    elif e21_up_v:
        tags.append('21 日線拐頭向上')
    if crossed_v:
        tags.append('剛穿 50 日線')
    elif near_v:
        tags.append('貼近 50 日線')
    if higher_v:
        tags.append('低點抬高')
    elif range_pos_v is not None and range_pos_v >= PARAMS['range_pos_min']:
        tags.append('靠近整理區上沿')
    return tags[:4]


# ── build ───────────────────────────────────────────────────────────────
def build():
    run_started = datetime.now(timezone.utc)
    print(f"=== RS Turn Build ({DEFINITION_VERSION}) — {run_started.isoformat()} ===")

    tickers, univ_payload = build_universe()
    if tickers is None:
        return None
    print(f"  universe total: {len(tickers)} (sources={univ_payload['sources']})")

    closes, volumes, qqq = download_prices_with_retry(tickers)

    n_covered = int((closes.notna().sum() >= PARAMS['min_bars']).sum())
    coverage_frac = (n_covered / len(tickers)) if tickers else 0.0
    print(f"  price coverage: {n_covered}/{len(tickers)} tickers with >= "
          f"{PARAMS['min_bars']} bars ({coverage_frac:.1%})")
    if coverage_frac < PARAMS['coverage_floor_pct']:
        _warn(f"coverage {coverage_frac:.1%} < floor "
              f"{PARAMS['coverage_floor_pct']:.0%} — abort, latest/history untouched")
        return None

    metrics = compute_metrics(closes, volumes, qqq)
    breadth = compute_breadth(metrics, closes)

    as_of_idx = closes.index[-1]
    as_of = as_of_idx.strftime('%Y-%m-%d')

    existing_history = load_existing_history()
    merged_history = merge_history(existing_history, breadth['series'],
                                    breadth['version_by_date'], breadth['members'], as_of)

    members_sets = {d: set(v) for d, v in merged_history['members'].items()}
    dates_desc = sorted(members_sets.keys(), reverse=True)

    today_passed = metrics['passed'].loc[as_of_idx]
    today_tickers = today_passed[today_passed].index.tolist()
    rs_accel_today = metrics['rs_accel'].loc[as_of_idx]
    today_tickers_sorted = sorted(
        today_tickers,
        key=lambda t: rs_accel_today[t] if pd.notna(rs_accel_today[t]) else -1e12,
        reverse=True,
    )

    rows = []
    for rank, t in enumerate(today_tickers_sorted, start=1):
        streak = compute_days_on_list(t, dates_desc, members_sets)
        is_new = streak == 1

        accel_v = _num(rs_accel_today[t], 1)
        e21_up_v = bool(metrics['e21_up'].at[as_of_idx, t])
        status = ('偏加速中' if (accel_v is not None and accel_v >= PARAMS['accel_label_min']
                                and e21_up_v) else '逐漸轉強')

        pullback_v = _num(metrics['pullback_pct'].at[as_of_idx, t], 1)
        reclaimed_v = bool(metrics['reclaimed_e21'].at[as_of_idx, t])
        crossed_v = bool(metrics['crossed_e50'].at[as_of_idx, t])
        near_v = bool(metrics['near_e50'].at[as_of_idx, t])
        higher_v = bool(metrics['higher_low'].at[as_of_idx, t])
        range_pos_v = _num(metrics['range_pos'].at[as_of_idx, t], 2)

        tags = build_tags(pullback_v, reclaimed_v, e21_up_v, crossed_v, near_v,
                           higher_v, range_pos_v)

        hub = f"/t/{t}.html" if (DOCS_T_DIR / f"{t}.html").exists() else None

        rows.append({
            'rank': rank, 'ticker': t, 'status': status, 'tags': tags,
            'rs_accel': accel_v,
            'rs21': _num(metrics['rs21'].at[as_of_idx, t], 1),
            'rs63': _num(metrics['rs63'].at[as_of_idx, t], 1),
            'dist_high_pct': _num(metrics['dist_high_pct'].at[as_of_idx, t], 1),
            'pullback_pct': pullback_v,
            'range_pos': range_pos_v,
            'adv20_usd': (int(round(metrics['adv20_usd'].at[as_of_idx, t]))
                          if pd.notna(metrics['adv20_usd'].at[as_of_idx, t]) else None),
            'price': _num(metrics['C'].at[as_of_idx, t], 2),
            'days_on_list': streak,
            'is_new': is_new,
            'hub': hub,
        })

    new_list = sorted(r['ticker'] for r in rows if r['is_new'])
    yesterday_date = dates_desc[1] if len(dates_desc) > 1 else None
    yesterday_set = members_sets.get(yesterday_date, set()) if yesterday_date else set()
    today_set = set(today_tickers_sorted)
    dropped_list = sorted(yesterday_set - today_set)

    n_full_today = int(breadth['n_full'].loc[as_of_idx])
    n_soft_today = int(breadth['n_soft'].loc[as_of_idx])
    n_eligible_today = int(breadth['n_eligible'].loc[as_of_idx])
    pct_full_today = _num(breadth['pct_full'].loc[as_of_idx], 1)

    n_full_hist_vals = [v for _, v in merged_history['series']['n_full']]
    last20 = n_full_hist_vals[-20:]
    n_full_ma20 = _num(sum(last20) / len(last20), 1) if last20 else None
    last250 = n_full_hist_vals[-250:]
    n_full_pctile = (_num(100.0 * sum(1 for v in last250 if v <= n_full_today) / len(last250), 1)
                      if last250 else None)

    latest_payload = {
        'schema': 'rs-turn-v1',
        'definition_version': DEFINITION_VERSION,
        'as_of': as_of,
        'run_timestamp': run_started.isoformat(),
        'benchmark': PARAMS['benchmark'],
        'params': PARAMS,
        'universe': {
            'total': len(tickers),
            'covered': n_covered,
            'eligible': n_eligible_today,
            'sources': univ_payload['sources'],
        },
        'breadth_today': {
            'n_full': n_full_today,
            'n_soft': n_soft_today,
            'n_eligible': n_eligible_today,
            'pct_full': pct_full_today,
            'n_full_ma20': n_full_ma20,
            'n_full_pctile_250d': n_full_pctile,
        },
        'changes': {'new': new_list, 'dropped': dropped_list},
        'rows': rows,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON.write_text(json.dumps(latest_payload, ensure_ascii=False, indent=1) + '\n',
                           encoding='utf-8')
    HISTORY_JSON.write_text(json.dumps(merged_history, ensure_ascii=False, indent=1) + '\n',
                            encoding='utf-8')

    print(f"  ✓ wrote {LATEST_JSON.relative_to(ROOT)}: n_full={n_full_today} "
          f"n_soft={n_soft_today} n_eligible={n_eligible_today} rows={len(rows)}")
    print(f"  ✓ wrote {HISTORY_JSON.relative_to(ROOT)}: "
          f"{len(merged_history['series']['n_full'])} dates")
    top15 = sorted(rows, key=lambda r: (r['rs_accel'] if r['rs_accel'] is not None else -1e12),
                   reverse=True)[:15]
    print("  top15 by rs_accel: " + ", ".join(f"{r['ticker']}({r['rs_accel']})" for r in top15))
    return latest_payload


def main():
    try:
        result = build()
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — outputs left unchanged")
        _warn(f"build failed ({type(e).__name__}: {e})")
        sys.exit(0)
    if result is None:
        sys.exit(0)  # fail-safe already logged inside build()


if __name__ == '__main__':
    main()
