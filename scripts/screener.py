"""
RS + VCP Screener (Mark Minervini Style)
Computes Relative Strength + Volatility Contraction Pattern scores
for ~200 US stocks. Outputs JSON for web display.

Usage:
  python scripts/screener.py          # full run
  python scripts/screener.py --quick  # skip fundamentals (faster)
"""

import csv, io, json, os, random, sys, math, time, warnings
from datetime import datetime, timezone, timedelta
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance', 'pandas', 'numpy', '-q'])
    import numpy as np
    import pandas as pd
    import yfinance as yf

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)): return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, (np.bool_,)): return bool(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super().default(obj)

ROOT = Path(__file__).resolve().parent.parent
SCREENER_DIR = ROOT / 'docs' / 'screener'
HISTORY_DIR = SCREENER_DIR / 'history'
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# ── Watchlist: S&P 500 + NQ100 extras ────────────────────────────────────

# NQ100 tickers NOT in S&P 500 (added to ensure full NQ100 coverage)
NQ100_EXTRAS = {
    'ARM':'Technology','MSTR':'Technology','SMCI':'Technology','APP':'Technology',
    'COIN':'Financials','DASH':'Consumer Disc','DDOG':'Technology','MNDY':'Technology',
    'TEAM':'Technology','TTD':'Technology','ZS':'Technology','RIVN':'Consumer Disc',
    'MELI':'Consumer Disc','GFS':'Technology','GEHC':'Health Care','WBD':'Communication',
    'LULU':'Consumer Disc','MRNA':'Health Care','CPRT':'Industrials','TTWO':'Communication',
    'WDAY':'Technology','ABNB':'Consumer Disc','PYPL':'Financials','PCAR':'Industrials',
}

def fetch_sp500_tickers():
    """Fetch S&P 500 components from GitHub CSV.

    Uses csv.reader so quoted fields with embedded commas (e.g.
    "Verisk Analytics, Inc.") parse correctly — naive split(',')
    previously misaligned columns and produced sector='Inc."'.
    """
    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
    try:
        import requests
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            raise Exception(f"HTTP {r.status_code}")
        tickers = {}
        reader = csv.reader(io.StringIO(r.text))
        next(reader, None)  # skip header row
        for row in reader:
            if len(row) >= 3:
                sym = row[0].replace('.', '-')  # BRK.B → BRK-B
                sector = row[2]
                sector = sector.replace('Information Technology', 'Technology')
                sector = sector.replace('Consumer Discretionary', 'Consumer Disc')
                sector = sector.replace('Consumer Staples', 'Consumer Staples')
                sector = sector.replace('Communication Services', 'Communication')
                tickers[sym] = sector
        print(f"  Fetched {len(tickers)} S&P 500 tickers from GitHub")
        return tickers
    except Exception as e:
        print(f"  ⚠ Failed to fetch S&P 500: {e}, using fallback")
        return None

# ── Universe source (2026-09-08): data/engine/universe.json, filtered to
# tier in {sp500, ndx100}, replaces the GitHub CSV + NQ100_EXTRAS as the
# PRIMARY watchlist source. The old CSV/NQ100_EXTRAS path above is kept as
# a fallback only (engine file missing, unreadable, or shorter than
# ENGINE_UNIVERSE_MIN rows). ──
ENGINE_UNIVERSE_PATH = ROOT / 'data' / 'engine' / 'universe.json'
ENGINE_UNIVERSE_MIN = 450

# Engine universe sector labels are GICS full names; map to the screener's
# existing short labels so sector_ranking / sector_strength_map keys stay
# unchanged. Sectors not listed here already match (Consumer Staples,
# Energy, Financials, Health Care, Industrials, Materials, Real Estate,
# Utilities).
ENGINE_SECTOR_LABEL_MAP = {
    'Information Technology': 'Technology',
    'Consumer Discretionary': 'Consumer Disc',
    'Communication Services': 'Communication',
}

# The 15 ndx100-only rows in data/engine/universe.json carry sector: ""
# (engine build doesn't backfill GICS sector for pure-NDX100 additions).
# Hand-mapped to the screener's short-label vocabulary so sector_ranking
# doesn't grow a bare "" bucket; 'Other' for names with no clean fit.
ENGINE_BLANK_SECTOR_FALLBACK = {
    'ALNY': 'Health Care', 'ARM': 'Technology', 'ASML': 'Technology',
    'ALAB': 'Technology', 'CCEP': 'Consumer Staples', 'CRWV': 'Technology',
    'FER': 'Industrials', 'MELI': 'Consumer Disc', 'MSTR': 'Technology',
    'NBIS': 'Technology', 'PDD': 'Consumer Disc', 'RKLB': 'Industrials',
    'SHOP': 'Technology', 'SPCX': 'Other', 'TRI': 'Industrials',
}


def _load_engine_universe():
    """S&P 500 + NDX100 watchlist from data/engine/universe.json. Returns
    None (triggers the CSV+NQ100_EXTRAS fallback below) if the file is
    missing, unreadable, or has fewer than ENGINE_UNIVERSE_MIN sp500/ndx100
    rows."""
    try:
        with open(ENGINE_UNIVERSE_PATH) as f:
            doc = json.load(f)
        rows = [t for t in doc.get('tickers', []) if t.get('tier') in ('sp500', 'ndx100')]
        if len(rows) < ENGINE_UNIVERSE_MIN:
            print(f"  ⚠ engine universe only {len(rows)} sp500/ndx100 rows (<{ENGINE_UNIVERSE_MIN}), falling back")
            return None
        watchlist = {}
        for row in rows:
            sym = row['ticker'].replace('.', '-')  # BRK.B -> BRK-B (yfinance symbol form)
            sector = row.get('sector') or ''
            sector = ENGINE_SECTOR_LABEL_MAP.get(sector, sector)
            if not sector:
                sector = ENGINE_BLANK_SECTOR_FALLBACK.get(sym, 'Other')
            watchlist[sym] = sector
        print(f"  Fetched {len(watchlist)} tickers from data/engine/universe.json (sp500+ndx100)")
        return watchlist
    except Exception as e:
        print(f"  ⚠ Failed to read engine universe: {e}, falling back")
        return None


def build_watchlist():
    """Build watchlist: data/engine/universe.json (sp500+ndx100) primary,
    falling back to the GitHub S&P 500 CSV + NQ100_EXTRAS."""
    watchlist = _load_engine_universe()
    if watchlist is not None:
        return watchlist
    sp500 = fetch_sp500_tickers()
    if sp500 is None:
        # Fallback: use a hardcoded subset
        print("  Using hardcoded fallback (~200 stocks)")
        return _FALLBACK_WATCHLIST
    # Merge with NQ100 extras
    watchlist = dict(sp500)
    for t, s in NQ100_EXTRAS.items():
        if t not in watchlist:
            watchlist[t] = s
    print(f"  Total watchlist: {len(watchlist)} stocks (SP500 + NQ100 extras)")
    return watchlist

# Hardcoded fallback if GitHub CSV is unavailable
_FALLBACK_WATCHLIST = {
    'AAPL':'Technology','MSFT':'Technology','NVDA':'Technology','GOOG':'Technology',
    'META':'Technology','AVGO':'Technology','ORCL':'Technology','CRM':'Technology',
    'AMD':'Technology','ADBE':'Technology','NOW':'Technology','INTU':'Technology',
    'AMAT':'Technology','KLAC':'Technology','LRCX':'Technology','MRVL':'Technology',
    'SNPS':'Technology','CDNS':'Technology','PANW':'Technology','CRWD':'Technology',
    'FTNT':'Technology','PLTR':'Technology','APP':'Technology','MSTR':'Technology',
    'DELL':'Technology','MU':'Technology','QCOM':'Technology','TXN':'Technology',
    'ARM':'Technology','JPM':'Financials','V':'Financials','MA':'Financials',
    'BAC':'Financials','GS':'Financials','BLK':'Financials','SPGI':'Financials',
    'PGR':'Financials','COIN':'Financials','LLY':'Health Care','UNH':'Health Care',
    'JNJ':'Health Care','ABBV':'Health Care','MRK':'Health Care','TMO':'Health Care',
    'ISRG':'Health Care','VRTX':'Health Care','AMZN':'Consumer Disc','TSLA':'Consumer Disc',
    'HD':'Consumer Disc','MCD':'Consumer Disc','LOW':'Consumer Disc','BKNG':'Consumer Disc',
    'CMG':'Consumer Disc','GE':'Industrials','CAT':'Industrials','RTX':'Industrials',
    'HON':'Industrials','UNP':'Industrials','LMT':'Industrials','ETN':'Industrials',
    'UBER':'Industrials','AXON':'Industrials','XOM':'Energy','CVX':'Energy',
    'COP':'Energy','SLB':'Energy','EOG':'Energy','MPC':'Energy',
    'NFLX':'Communication','DIS':'Communication','TMUS':'Communication','SPOT':'Communication',
    'PG':'Consumer Staples','KO':'Consumer Staples','COST':'Consumer Staples','WMT':'Consumer Staples',
    'NEE':'Utilities','CEG':'Utilities','VST':'Utilities','PLD':'Real Estate',
    'EQIX':'Real Estate','WELL':'Real Estate','LIN':'Materials','SHW':'Materials',
    'FCX':'Materials','NEM':'Materials',
}

BENCHMARK = 'SPY'
EMA_ALPHA = 0.2

# ── download resilience (2026-09-08 fix, plumbing only — code shape copied
# from scripts/build_momentum5.py's 2026-09-08 "DOWNLOAD RESILIENCE" fix,
# which itself mirrors build_price_momentum.py's 2026-09-07 fix,
# commit 71cd044e4): a single-shot yf.download burst for the whole watchlist
# can trip Yahoo's 429 rate limit. To survive that without changing any
# scoring logic:
#   - tickers + [BENCHMARK] is downloaded in DOWNLOAD_BATCH_SIZE-ticker
#     batches (identical download kwargs per batch to the old single-shot
#     call), concatenated into one DataFrame with the exact same
#     data[ticker]['Close'] access shape the rest of main() already relies
#     on.
#   - The whole batched download is retried up to MAX_DOWNLOAD_ATTEMPTS
#     times, with exponential backoff + jitter between attempts, whenever
#     the benchmark comes back empty OR price coverage on that attempt is
#     below the coverage floor (>= MIN_COVERAGE_BARS bars on
#     MIN_COVERAGE_PCT of the watchlist).
#   - Only after all attempts fail does this print a `::warning::` and
#     exit 0 WITHOUT writing latest.json / history (fail-safe — same
#     semantics as a stale-but-untouched output, just given more chances
#     to succeed first).
DOWNLOAD_BATCH_SIZE = 100
MAX_DOWNLOAD_ATTEMPTS = 4
RETRY_BACKOFF_SECONDS = (20.0, 60.0, 150.0)  # before attempts 2, 3, 4
MIN_COVERAGE_BARS = 252
MIN_COVERAGE_PCT = 0.85


def _count_price_sufficient(data, tickers):
    """How many of `tickers` have >= MIN_COVERAGE_BARS dropna'd closes in
    `data`. Used only by the download-retry coverage gate."""
    n = 0
    for t in tickers:
        try:
            c = data[t]['Close'].dropna()
        except Exception:
            continue
        if len(c) >= MIN_COVERAGE_BARS:
            n += 1
    return n


def _download_all_once(all_tickers, period):
    """One attempt: download all_tickers (already includes BENCHMARK) in
    DOWNLOAD_BATCH_SIZE-sized chunks with the SAME yf.download kwargs the
    old single-shot call used, then concat into one DataFrame with the same
    group_by='ticker' column shape. A chunk that raises is skipped (not
    fatal by itself) — the coverage check in the caller decides whether
    this whole attempt counts as a failure."""
    frames = []
    n_chunks = (len(all_tickers) + DOWNLOAD_BATCH_SIZE - 1) // DOWNLOAD_BATCH_SIZE
    for i in range(0, len(all_tickers), DOWNLOAD_BATCH_SIZE):
        chunk = all_tickers[i:i + DOWNLOAD_BATCH_SIZE]
        chunk_no = i // DOWNLOAD_BATCH_SIZE + 1
        try:
            frames.append(yf.download(chunk, period=period, interval='1d',
                                       group_by='ticker', progress=False, threads=True))
        except Exception as e:
            print(f"      ! batch {chunk_no}/{n_chunks} ({len(chunk)} tickers) raised "
                  f"{type(e).__name__}: {e} — skipped this batch")
        if chunk_no < n_chunks:
            time.sleep(3)
    if not frames:
        raise RuntimeError("all download batches failed")
    return pd.concat(frames, axis=1)


def _emit_gh_warning(reason):
    """Failure-visibility fix (2026-09-08, same shape as
    build_momentum5.py's _emit_gh_skip_warning): print a `::warning::`
    workflow command (and a GITHUB_STEP_SUMMARY line when available) so a
    fail-safe abort shows up in the Actions run summary instead of a
    silent green no-op. Prints regardless of environment so a local run
    also sees the reason."""
    print(f"::warning title=US RS+VCP screener skipped::{reason}")
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_path:
        try:
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write(f"- ⚠️ **US RS+VCP screener skipped** — {reason}\n")
        except Exception:
            pass


def fetch_all_data(tickers, period='15mo'):
    """Fetch price data for all tickers, batched + retried (see
    DOWNLOAD RESILIENCE note above). period='15mo' (~326 calendar days)
    so the 252-bar lookbacks used elsewhere in this file have headroom —
    the old '300d' (~206 bars) was too short for that.

    On coverage-floor failure after all retries: prints a `::warning::`
    and calls sys.exit(0) — this function is called before latest.json /
    history are written, so a floor failure never touches either file.
    """
    tickers = list(tickers)
    all_tickers = tickers + [BENCHMARK]
    min_required = math.ceil(len(tickers) * MIN_COVERAGE_PCT)
    last_reason = None
    for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
        print(f"  Fetching {len(tickers)} tickers (attempt {attempt}/{MAX_DOWNLOAD_ATTEMPTS}, "
              f"batches of {DOWNLOAD_BATCH_SIZE})...")
        try:
            data = _download_all_once(all_tickers, period)
        except Exception as e:
            last_reason = f"attempt {attempt} raised {type(e).__name__}: {e}"
            print(f"    ! {last_reason}")
        else:
            try:
                bench = data[BENCHMARK]['Close'].dropna()
            except Exception:
                bench = pd.Series(dtype=float)
            if bench.empty:
                last_reason = f"attempt {attempt}: {BENCHMARK} price series empty after download"
                print(f"    ! {last_reason}")
            else:
                n_sufficient = _count_price_sufficient(data, tickers)
                if n_sufficient < min_required:
                    last_reason = (f"attempt {attempt}: price coverage {n_sufficient}/{len(tickers)} "
                                    f"< floor {min_required} ({int(MIN_COVERAGE_PCT*100)}% w/ "
                                    f">={MIN_COVERAGE_BARS} bars)")
                    print(f"    ! {last_reason}")
                else:
                    print(f"    ✓ attempt {attempt} succeeded: {BENCHMARK} ok, "
                          f"price coverage {n_sufficient}/{len(tickers)} >= floor {min_required}")
                    return data
        if attempt < MAX_DOWNLOAD_ATTEMPTS:
            backoff = RETRY_BACKOFF_SECONDS[attempt - 1] + random.uniform(0, 5)
            print(f"    … retrying in {backoff:.0f}s")
            time.sleep(backoff)
    reason = f"price download failed after {MAX_DOWNLOAD_ATTEMPTS} attempts (last: {last_reason})"
    print(f"  ✗ {reason}")
    _emit_gh_warning(reason)
    sys.exit(0)


def calc_return(closes, days):
    """Calculate return over N trading days."""
    if len(closes) < days + 1:
        return None
    return (closes.iloc[-1] / closes.iloc[-(days+1)] - 1) * 100


def percentile_rank(values):
    """Compute percentile rank (0-100) for each value."""
    arr = np.array(values, dtype=float)
    valid = ~np.isnan(arr)
    ranks = np.full_like(arr, np.nan)
    if valid.sum() == 0:
        return ranks
    for i in range(len(arr)):
        if np.isnan(arr[i]):
            continue
        ranks[i] = np.nansum(arr[valid] <= arr[i]) / valid.sum() * 100
    return ranks


def load_previous_history():
    """Load most recent history JSON for EMA smoothing."""
    files = sorted(HISTORY_DIR.glob('*.json'))
    if not files:
        return {}
    try:
        with open(files[-1]) as f:
            data = json.load(f)
        return {r['ticker']: r for r in data.get('rankings', [])}
    except:
        return {}


def find_local_highs(highs, window=90):
    """Find local high points in the last `window` days."""
    if len(highs) < window:
        return []
    segment = highs.iloc[-window:]
    peaks = []
    for i in range(10, len(segment) - 5):
        left = max(0, i - 10)
        right = min(len(segment), i + 6)
        if segment.iloc[i] == segment.iloc[left:right].max():
            peaks.append((segment.index[i], segment.iloc[i], i))
    # Merge peaks within 10 days
    merged = []
    for p in peaks:
        if merged and (p[2] - merged[-1][2]) < 10:
            if p[1] > merged[-1][1]:
                merged[-1] = p
        else:
            merged.append(p)
    return merged


VCP_MIN_BARS = 221  # 200 (MA200) + 21 (MA200-21-bars-ago), the Trend Template's tightest need


def _vcp_empty_result(trend_ok=False, tt_fails=None):
    """Shared zero-score shape for insufficient-data / degenerate cases.
    Existing keys keep the same meaning/shape they had pre-2026-09-08;
    new keys (trend_template_pass/tt_fails/contraction_ok/vcp_gate/
    base_age_days/base_high/vol_dryup_ratio) default to the
    fails-everything state so a downstream `vcp_gate` read never KeyErrors."""
    return {
        'score': 0, 'pullback_count': 0, 'last_pullback_pct': 0,
        'dist_from_high_pct': 0, 'atr_ratio': 1.0, 'vol_ratio': 1.0,
        'trend_ok': bool(trend_ok),
        'trend_template_pass': False, 'tt_fails': tt_fails or ['insufficient_data'],
        'contraction_ok': False, 'vcp_gate': 'trend',
        'base_age_days': 0, 'base_high': 0.0, 'vol_dryup_ratio': 1.0,
    }


def calc_vcp(closes, highs, lows, volumes):
    """Calculate VCP score (2026-09-08 rewrite: VCP becomes gate + score).

    Same signature as before (superset of return keys — existing keys keep
    their meaning: score, pullback_count, last_pullback_pct,
    atr_ratio, vol_ratio, trend_ok; dist_from_high_pct now measured vs
    base_high instead of the old fixed 90-day high).

    Shape:
      - Window = last min(260, len) bars. base_high = max High in that
        window, base_high_idx its position. Contraction detection (reuses
        find_local_highs) runs only on the segment from base_high_idx to
        the end — the base_high itself seeds the pullback sequence as
        anchor #1 (find_local_highs' own edge margins can never flag a
        peak within its first ~10 bars, so it would otherwise be missed).
        Base age (bars since base_high) must be >= 15, else pullback_count
        is forced to 0 (no established base yet to measure contractions
        in).
      - Trend Template gate (trend_template_pass / tt_fails): price >
        MA150 > MA200; MA200 today > MA200 21 bars ago; MA50 > MA150;
        price >= 1.30x 52-week low close; price >= 0.75x 52-week high
        close. trend_ok (legacy) stays price > MA150 > MA200 only.
      - Contraction gate (contraction_ok): pullback_count >= 2 AND every
        pullback_pct smaller than the one before it.
      - Score table (component cap 100 before gates): trend template pass
        10; contraction count 2-4 -> 15 (1 -> 5, >4 -> 8); decreasing
        magnitudes 20; higher lows 15; volume dry-up 15 (<0.7x 50d avg) /
        8 (<0.9x); last pullback tightness 15/10/5 for <4/<6/<10%;
        distance from base_high 10/6/3 for <3/<5/<10%, -5 if >=10%;
        ATR10/ATR60 <0.5 -> 10, <0.7 -> 5.
      - Gates: trend template fail -> score capped at 30, vcp_gate="trend";
        else contraction gate fail -> score capped at 40,
        vcp_gate="contraction"; else vcp_gate="pass".
    """
    if len(closes) < VCP_MIN_BARS:
        return _vcp_empty_result()

    price = closes.iloc[-1]
    ma50 = closes.iloc[-50:].mean()
    ma150 = closes.iloc[-150:].mean()
    ma200 = closes.iloc[-200:].mean()
    ma200_21_ago = closes.iloc[-(200 + 21):-21].mean()
    trend_ok = bool(price > ma150 > ma200)  # legacy key, meaning unchanged

    window_52w = closes.iloc[-min(252, len(closes)):]
    low_52w = window_52w.min()
    high_52w = window_52w.max()

    tt_fails = []
    if not (price > ma150 > ma200):
        tt_fails.append('price>MA150>MA200')
    if not (ma200 > ma200_21_ago):
        tt_fails.append('MA200_rising')
    if not (ma50 > ma150):
        tt_fails.append('MA50>MA150')
    if not (low_52w > 0 and price >= 1.30 * low_52w):
        tt_fails.append('>=1.30x52wLow')
    if not (high_52w > 0 and price >= 0.75 * high_52w):
        tt_fails.append('>=0.75x52wHigh')
    trend_template_pass = len(tt_fails) == 0

    # ── Base + contraction detection ──────────────────────────────────
    window_n = min(260, len(closes))
    highs_w = highs.iloc[-window_n:]
    lows_w = lows.iloc[-window_n:]
    vols_w = volumes.iloc[-window_n:]

    base_high_idx = int(np.argmax(highs_w.values))
    base_high = float(highs_w.iloc[base_high_idx])
    base_age_days = (window_n - 1) - base_high_idx

    seg_highs = highs_w.iloc[base_high_idx:]
    seg_lows = lows_w.iloc[base_high_idx:]
    seg_vols = vols_w.iloc[base_high_idx:]

    if base_age_days >= 15:
        # find_local_highs' own left-margin (10 bars) means it can never
        # flag the segment's first point as a peak — seed base_high as
        # anchor #1 explicitly, then append any later local highs found
        # within the segment (dropping any duplicate right at position 0).
        later_peaks = [p for p in find_local_highs(seg_highs, window=len(seg_highs)) if p[2] >= 10]
        peaks = [(seg_highs.index[0], base_high, 0)] + later_peaks
    else:
        peaks = []

    pullbacks = []
    for i in range(1, len(peaks)):
        idx_start = peaks[i-1][2]
        idx_end = peaks[i][2]
        seg_low = seg_lows.iloc[idx_start:idx_end+1]
        seg_vol = seg_vols.iloc[idx_start:idx_end+1]
        if len(seg_low) == 0:
            continue
        low_val = seg_low.min()
        high_val = peaks[i-1][1]
        pullback_pct = (high_val - low_val) / high_val * 100
        if pullback_pct < 3:
            continue
        avg_vol = seg_vol.mean() if len(seg_vol) > 0 else 0
        pullbacks.append({
            'high': high_val, 'low': low_val,
            'pullback_pct': pullback_pct, 'avg_vol': avg_vol
        })

    n = len(pullbacks)

    decreasing_ok = n >= 2 and all(pullbacks[i]['pullback_pct'] < pullbacks[i-1]['pullback_pct'] for i in range(1, n))
    higher_lows_ok = n >= 2 and all(pullbacks[i]['low'] > pullbacks[i-1]['low'] for i in range(1, n))
    contraction_ok = decreasing_ok

    # ── Score table ──────────────────────────────────────────────────
    score = 10 if trend_template_pass else 0

    if 2 <= n <= 4:
        score += 15
    elif n == 1:
        score += 5
    elif n > 4:
        score += 8

    if decreasing_ok:
        score += 20

    if higher_lows_ok:
        score += 15

    # Volume dry-up: mean volume of the LAST contraction segment vs 50-day avg
    vol_50 = volumes.iloc[-50:].mean()
    if n >= 1 and vol_50 > 0:
        vol_dryup_ratio = pullbacks[-1]['avg_vol'] / vol_50
    else:
        vol_dryup_ratio = 1.0
    if vol_dryup_ratio < 0.7: score += 15
    elif vol_dryup_ratio < 0.9: score += 8

    # Last pullback magnitude (tightness)
    last_pb = pullbacks[-1]['pullback_pct'] if pullbacks else 0
    if last_pb > 0:
        if last_pb < 4: score += 15
        elif last_pb < 6: score += 10
        elif last_pb < 10: score += 5

    # Distance from base_high (was: 90-day high)
    dist_pct = (base_high - price) / base_high * 100 if base_high > 0 else 0
    if dist_pct < 3: score += 10
    elif dist_pct < 5: score += 6
    elif dist_pct < 10: score += 3
    elif dist_pct >= 10: score -= 5

    # ATR contraction
    def atr(h, l, c, n):
        tr = pd.concat([h-l, (h-c.shift(1)).abs(), (l-c.shift(1)).abs()], axis=1).max(axis=1)
        return tr.rolling(n).mean().iloc[-1]

    atr10 = atr(highs, lows, closes, 10)
    atr60 = atr(highs, lows, closes, 60)
    atr_ratio = atr10 / atr60 if atr60 > 0 else 1.0
    if atr_ratio < 0.5: score += 10
    elif atr_ratio < 0.7: score += 5

    score = max(0, min(100, score))

    # ── Gates ────────────────────────────────────────────────────────
    if not trend_template_pass:
        score = min(score, 30)
        vcp_gate = 'trend'
    elif not contraction_ok:
        score = min(score, 40)
        vcp_gate = 'contraction'
    else:
        vcp_gate = 'pass'

    # Volume ratio (legacy key, meaning unchanged: 10d avg vs 60d avg)
    vol_10 = volumes.iloc[-10:].mean()
    vol_60 = volumes.iloc[-60:].mean()
    vol_ratio = vol_10 / vol_60 if vol_60 > 0 else 1.0

    return {
        'score': score,
        'pullback_count': n,
        'last_pullback_pct': round(last_pb, 1),
        'dist_from_high_pct': round(dist_pct, 1),
        'atr_ratio': round(atr_ratio, 2),
        'vol_ratio': round(vol_ratio, 2),
        'trend_ok': trend_ok,
        'trend_template_pass': bool(trend_template_pass),
        'tt_fails': tt_fails,
        'contraction_ok': bool(contraction_ok),
        'vcp_gate': vcp_gate,
        'base_age_days': int(base_age_days),
        'base_high': round(base_high, 2),
        'vol_dryup_ratio': round(float(vol_dryup_ratio), 2),
    }


def calc_extra_indicators(closes, highs, lows, price):
    """MA21%/MA50%/52W high%/RSI14/ATR% on adjusted close. Returns dict with None for any insufficient-data field."""
    out = {'ma21_pct': None, 'ma50_pct': None, 'dist_52w_high_pct': None,
           'rsi14': None, 'atr_pct': None, 'close_change_pct': None}

    if len(closes) < 2 or price <= 0:
        return out

    # 1-day return (today close vs prior close) — surfaces single-day relative
    # weakness that EMA-smoothed rs_score dampens. Consumed by Flow ATH Hunter's
    # "1d vs SPY" column to flag stocks that under-performed SPY yesterday even
    # when their multi-week RS still looks healthy.
    prev_close = closes.iloc[-2]
    if prev_close > 0:
        out['close_change_pct'] = round((price / prev_close - 1) * 100, 2)

    if len(closes) >= 21:
        ma21 = closes.iloc[-21:].mean()
        if ma21 > 0:
            out['ma21_pct'] = round((price / ma21 - 1) * 100, 1)
    if len(closes) >= 50:
        ma50 = closes.iloc[-50:].mean()
        if ma50 > 0:
            out['ma50_pct'] = round((price / ma50 - 1) * 100, 1)

    window = min(252, len(closes))
    high_52w = closes.iloc[-window:].max()
    if high_52w > 0:
        out['dist_52w_high_pct'] = round((price / high_52w - 1) * 100, 1)

    if len(closes) >= 15:
        delta = closes.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = (-delta).where(delta < 0, 0.0)
        avg_gain = gain.ewm(alpha=1/14, adjust=False).mean().iloc[-1]
        avg_loss = loss.ewm(alpha=1/14, adjust=False).mean().iloc[-1]
        if avg_loss == 0:
            out['rsi14'] = 100.0
        else:
            rs = avg_gain / avg_loss
            out['rsi14'] = round(100 - (100 / (1 + rs)), 1)

    if len(closes) >= 15 and len(highs) >= 15 and len(lows) >= 15:
        prev_close = closes.shift(1)
        tr = pd.concat([highs - lows,
                        (highs - prev_close).abs(),
                        (lows - prev_close).abs()], axis=1).max(axis=1)
        atr14 = tr.ewm(alpha=1/14, adjust=False).mean().iloc[-1]
        if pd.notna(atr14):
            out['atr_pct'] = round((atr14 / price) * 100, 2)

    return out


def fetch_fundamentals(ticker):
    """Fetch basic fundamentals for a single ticker."""
    try:
        info = yf.Ticker(ticker).info
        return {
            'mktCap': round((info.get('marketCap') or 0) / 1e9, 1),
            'epsTTM': info.get('trailingEps'),
            'epsFwd': info.get('forwardEps'),
            'peRatio': info.get('forwardPE') or info.get('trailingPE'),
            'revGrowth': round((info.get('revenueGrowth') or 0) * 100, 1),
            'opMargin': round((info.get('operatingMargins') or 0) * 100, 1),
            'roe': round((info.get('returnOnEquity') or 0) * 100, 1),
        }
    except:
        return {}


def main():
    quick = '--quick' in sys.argv
    now = datetime.now(timezone.utc)
    today = now.strftime('%Y-%m-%d')
    print(f"=== RS+VCP Screener: {today} ===\n")

    # ── Build watchlist ────────────────────────────────────────────────
    WATCHLIST = build_watchlist()

    # ── Fetch data ──────────────────────────────────────────────────────
    data = fetch_all_data(WATCHLIST.keys())
    prev = load_previous_history()

    # ── Calculate RS for all stocks ─────────────────────────────────────
    print("  Calculating RS scores...")
    rs_raw = {}  # {ticker: {r1w, r4w, r13w}}
    for ticker in WATCHLIST:
        try:
            closes = data[ticker]['Close'].dropna()
            r1w = calc_return(closes, 5)
            r4w = calc_return(closes, 21)
            r13w = calc_return(closes, 63)
            if r1w is not None and r4w is not None and r13w is not None:
                rs_raw[ticker] = {'r1w': r1w, 'r4w': r4w, 'r13w': r13w}
        except:
            pass

    if not rs_raw:
        print("ERROR: No valid data")
        return

    # Percentile ranks
    tickers_list = list(rs_raw.keys())
    r1w_vals = [rs_raw[t]['r1w'] for t in tickers_list]
    r4w_vals = [rs_raw[t]['r4w'] for t in tickers_list]
    r13w_vals = [rs_raw[t]['r13w'] for t in tickers_list]

    pr1w = percentile_rank(r1w_vals)
    pr4w = percentile_rank(r4w_vals)
    pr13w = percentile_rank(r13w_vals)

    # ── EMA smooth + trend + final RS ───────────────────────────────────
    results = []
    for i, ticker in enumerate(tickers_list):
        raw_1w, raw_4w, raw_13w = pr1w[i], pr4w[i], pr13w[i]

        # EMA smoothing
        prev_data = prev.get(ticker, {})
        if prev_data:
            s1w = prev_data.get('rs_1w', raw_1w) * (1 - EMA_ALPHA) + raw_1w * EMA_ALPHA
            s4w = prev_data.get('rs_4w', raw_4w) * (1 - EMA_ALPHA) + raw_4w * EMA_ALPHA
            s13w = prev_data.get('rs_13w', raw_13w) * (1 - EMA_ALPHA) + raw_13w * EMA_ALPHA
        else:
            s1w, s4w, s13w = raw_1w, raw_4w, raw_13w

        # Persistence
        persistence = s1w * 0.2 + s4w * 0.3 + s13w * 0.5

        # Trend bonus
        if s1w > s4w > s13w:
            trend = 'accelerating'
            bonus = 5
        elif s1w >= s4w >= s13w:
            trend = 'steady'
            bonus = 2
        elif s1w < s4w < s13w:
            trend = 'fading'
            bonus = -5
        else:
            trend = 'choppy'
            bonus = 0

        rs_score = min(100, persistence + bonus)

        # ── VCP ─────────────────────────────────────────────────────────
        try:
            closes = data[ticker]['Close'].dropna()
            highs = data[ticker]['High'].dropna()
            lows = data[ticker]['Low'].dropna()
            volumes = data[ticker]['Volume'].dropna()
            price = float(closes.iloc[-1])
            ma200 = closes.iloc[-200:].mean() if len(closes) >= 200 else price
            vs_200ma = (price - ma200) / ma200 * 100

            vcp = calc_vcp(closes, highs, lows, volumes)
            extras = calc_extra_indicators(closes, highs, lows, price)

            # Price-action override for V-shape recovery: percentile-rank trend
            # lags after a sharp reversal because s1w/s4w/s13w ordering is noisy.
            # Upgrade fading/choppy → accelerating when price > 21DMA > 50DMA
            # AND RSI14 > 60 AND last-week raw return > 0. rs_score unchanged.
            if trend in ('fading', 'choppy') \
                    and extras.get('ma21_pct') is not None \
                    and extras.get('ma50_pct') is not None \
                    and extras.get('rsi14') is not None \
                    and extras['ma21_pct'] > 0 \
                    and extras['ma21_pct'] < extras['ma50_pct'] \
                    and extras['rsi14'] > 60 \
                    and rs_raw[ticker]['r1w'] > 0:
                trend = 'accelerating'
        except:
            price = 0
            vs_200ma = 0
            vcp = _vcp_empty_result()
            extras = {'ma21_pct': None, 'ma50_pct': None, 'dist_52w_high_pct': None,
                      'rsi14': None, 'atr_pct': None, 'close_change_pct': None}

        combined = round(rs_score * 0.6 + vcp['score'] * 0.4, 1)

        results.append({
            'ticker': ticker,
            'sector': WATCHLIST[ticker],
            'rs_score': round(rs_score, 1),
            'rs_trend': trend,
            'rs_1w': round(s1w, 1),
            'rs_4w': round(s4w, 1),
            'rs_13w': round(s13w, 1),
            'vcp_score': vcp['score'],
            'pullback_count': vcp['pullback_count'],
            'last_pullback_pct': vcp['last_pullback_pct'],
            'dist_from_high_pct': vcp['dist_from_high_pct'],
            'atr_ratio': vcp['atr_ratio'],
            'vol_ratio': vcp.get('vol_ratio', 1.0),
            'combined': combined,
            'price': round(price, 2),
            'vs_200ma_pct': round(vs_200ma, 1),
            'trend_ok': bool(vcp['trend_ok']),
            'vcp_gate': vcp.get('vcp_gate', 'trend'),
            'trend_template_pass': bool(vcp.get('trend_template_pass', False)),
            'tt_fails': vcp.get('tt_fails', []),
            'contraction_ok': bool(vcp.get('contraction_ok', False)),
            'base_age_days': vcp.get('base_age_days', 0),
            'base_high': vcp.get('base_high', 0.0),
            'vol_dryup_ratio': vcp.get('vol_dryup_ratio', 1.0),
            'ma21_pct': extras['ma21_pct'],
            'ma50_pct': extras['ma50_pct'],
            'dist_52w_high_pct': extras['dist_52w_high_pct'],
            'rsi14': extras['rsi14'],
            'atr_pct': extras['atr_pct'],
            'close_change_pct': extras['close_change_pct'],
        })

    # Sort by combined score
    results.sort(key=lambda x: x['combined'], reverse=True)

    # Assign ranks + rank change
    for i, r in enumerate(results):
        r['rank'] = i + 1
        prev_r = prev.get(r['ticker'], {})
        prev_rank = prev_r.get('rank')
        if prev_rank:
            diff = prev_rank - r['rank']
            if diff > 0: r['rank_change'] = f'+{diff}'
            elif diff < 0: r['rank_change'] = str(diff)
            else: r['rank_change'] = '—'
        else:
            r['rank_change'] = 'NEW'

    # ── Top Picks ───────────────────────────────────────────────────────
    print("  Selecting top picks...")
    picks = {}  # key → ticker
    used = set()

    def pick(key, candidates):
        for r in candidates:
            if r['ticker'] not in used:
                picks[key] = r['ticker']
                used.add(r['ticker'])
                return True
        return False

    # Minervini best × 3 (progressively relaxed within a strict floor — the
    # two loosest rungs, rs>=75&vcp>=65 and rs>=70&vcp>=55, were removed
    # 2026-09-08 so top_picks can legitimately come back empty on a day with
    # no real setup, instead of always forcing 3 mediocre names)
    for label in ['minervini_1', 'minervini_2', 'minervini_3']:
        for cond in [
            lambda r: r['rs_score']>=80 and r['vcp_score']>=75 and r['rs_trend']=='accelerating' and r['dist_from_high_pct']<5 and r['vol_ratio']<0.8,
            lambda r: r['rs_score']>=80 and r['vcp_score']>=75 and r['rs_trend']=='accelerating' and r['dist_from_high_pct']<8,
            lambda r: r['rs_score']>=78 and r['vcp_score']>=70 and r['rs_trend'] in ('accelerating','steady'),
        ]:
            found = [r for r in results if r['ticker'] not in used and cond(r)]
            if found:
                pick(label, found)
                break

    # Momentum × 1 (biggest rank improvement)
    try:
        momentum_candidates = [r for r in results if r['rs_score'] >= 65 and r['rank_change'] not in ('—', 'NEW') and int(r['rank_change'].replace('+','')) > 0]
        momentum_candidates.sort(key=lambda r: int(r['rank_change'].replace('+','')), reverse=True)
        pick('momentum', momentum_candidates)
    except:
        pass

    # VCP best × 3
    vcp_candidates = [r for r in results if r['vcp_score'] >= 65 and r['rs_score'] >= 60]
    vcp_candidates.sort(key=lambda r: r['vcp_score'] * 0.7 + r['rs_score'] * 0.3, reverse=True)
    pick('vcp_1', vcp_candidates)
    pick('vcp_2', [r for r in vcp_candidates if r['ticker'] not in used])
    pick('vcp_3', [r for r in vcp_candidates if r['ticker'] not in used])

    # ── Fundamentals for top 30 ─────────────────────────────────────────
    if not quick:
        print("  Fetching fundamentals for top 30...")
        for r in results[:30]:
            r['fundamentals'] = fetch_fundamentals(r['ticker'])
    else:
        print("  Skipping fundamentals (--quick mode)")

    # ── Sector ranking ──────────────────────────────────────────────────
    sector_scores = {}
    for r in results:
        sec = r['sector']
        if sec not in sector_scores:
            sector_scores[sec] = []
        sector_scores[sec].append(r['rs_score'])
    sector_ranking = [{'sector': s, 'avg_rs': round(np.mean(v), 1), 'count': len(v)}
                      for s, v in sector_scores.items()]
    sector_ranking.sort(key=lambda x: x['avg_rs'], reverse=True)

    # ── Sector strength (strong/neutral/weak) ───────────────────────────
    sector_counts = {}
    for r in results:
        sec = r['sector']
        c = sector_counts.setdefault(sec, {'strong': 0, 'total': 0})
        c['total'] += 1
        if r['rs_score'] >= 75 and r['rs_trend'] in ('accelerating', 'steady'):
            c['strong'] += 1
    sector_strength_map = {}
    for sec, c in sector_counts.items():
        ratio = c['strong'] / c['total'] if c['total'] > 0 else 0
        if ratio >= 0.30 and c['strong'] >= 5:
            sector_strength_map[sec] = 'strong'
        elif ratio >= 0.15:
            sector_strength_map[sec] = 'neutral'
        else:
            sector_strength_map[sec] = 'weak'
    for r in results:
        r['sector_strength'] = sector_strength_map.get(r['sector'], 'weak')

    # ── Output JSON ─────────────────────────────────────────────────────
    output = {
        'date': today,
        'total_stocks': len(results),
        'benchmark': BENCHMARK,
        'top_picks': picks,
        'top_sector': sector_ranking[0] if sector_ranking else {},
        'sector_ranking': sector_ranking,
        'rankings': results,
    }

    latest_path = SCREENER_DIR / 'latest.json'
    with open(latest_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NpEncoder)

    history_path = HISTORY_DIR / f'{today}.json'
    with open(history_path, 'w') as f:
        json.dump(output, f, cls=NpEncoder)

    print(f"\n  ✓ Output: {latest_path}")
    print(f"  ✓ History: {history_path}")
    print(f"  ✓ Top 5: {', '.join(r['ticker'] for r in results[:5])}")
    print(f"  ✓ Top picks: {picks}")
    print(f"  ✓ Top sector: {sector_ranking[0]['sector']} (avg RS {sector_ranking[0]['avg_rs']})")

    # GitHub Actions output
    gh_output = os.environ.get('GITHUB_OUTPUT')
    if gh_output:
        with open(gh_output, 'a') as f:
            f.write("has_changes=true\n")
            f.write(f"summary=screener {today} top={results[0]['ticker']}\n")


if __name__ == '__main__':
    main()
