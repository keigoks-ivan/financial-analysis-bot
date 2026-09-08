"""
tech_core.py — shared price-data download + same-run on-disk cache.

Extracted 2026-09-08 from scripts/screener.py's download-resilience commit
(batch download + backoff/jitter, moved here verbatim in shape) so
scripts/screener.py, scripts/build_rs_turn.py and scripts/build_stages.py
stop downloading the same tickers three times a day. See design spec
notes/site-internal/root/_stages_radar_design_20260908.md §2.

WHAT THIS PROVIDES
-------------------
download_prices(tickers, period, auto_adjust) -> DataFrame, shaped exactly
like `yf.download(tickers, group_by='ticker', ...)` (columns = MultiIndex
(ticker, field)), covering exactly the requested `tickers`.

CACHING
-------
Every fresh network fetch pulls CACHE_PERIOD (currently '2y') of history —
the broadest width any current consumer needs — REGARDLESS of the `period`
a caller asks for, then trims the returned frame down to that caller's
`period` before handing it back. This means:
  - a caller's own row-count/shape (and therefore anything downstream that
    slices by `.iloc[-N:]`) is unaffected by the refactor: trimming a 2y
    cache entry to '15mo' reproduces the same set of trading days a direct
    `yf.download(period='15mo')` call would (verified empirically —
    residual differences are ~1e-5-level auto_adjust floating-point noise,
    invisible after this codebase's rounding).
  - a SECOND caller asking for a WIDER period (e.g. build_rs_turn.py's
    '2y') over an overlapping ticker set is served entirely from cache,
    because the cache already holds the full 2y width regardless of which
    caller triggered the original download. This is the "只補下載差集"
    behavior build_rs_turn.py / build_stages.py rely on when they run
    after screener.py in the same daily-us-close.yml run.

Cache is on disk at data/tech_core/cache/{YYYY-MM-DD}_{adj|raw}.pkl — one
pickle per (UTC date, auto_adjust) holding a {ticker: OHLCV DataFrame}
dict, so it survives across separate script invocations within the same
day (CI runners are always fresh, so this never crosses a day boundary in
practice) but not across days (old files are pruned — see
CACHE_KEEP_DAYS). A ticker whose fetch comes back empty/near-empty is
simply NOT cached (no "known-bad" sentinel), so the next call in the same
run retries it over the network — this is what gives each caller's own
outer coverage-floor retry loop (screener.py / build_rs_turn.py keep their
own floor + fail-safe logic, unchanged by this refactor) real teeth.
"""

import pickle
import random
import re
import sys
import time
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

import pandas as pd

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance', '-q'])
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / 'data' / 'tech_core' / 'cache'

DOWNLOAD_BATCH_SIZE = 100
BATCH_SLEEP_SECONDS = 3
MAX_BATCH_RETRIES = 2       # transient per-batch retry (network blip only) — the
                             # "did coverage meet the floor" retry stays with each
                             # caller, which now retries by calling download_prices()
                             # again (cheap: already-cached tickers are a no-op).
CACHE_PERIOD = '2y'         # canonical fetch width — must stay >= the longest
                             # period any consumer requests (currently rs-turn's
                             # '2y'; screener's '15mo' and build_stages' own use
                             # are both narrower).
MIN_TICKER_BARS = 5         # a per-ticker download with fewer valid Close bars than
                             # this is treated as empty/failed and NOT cached — kept
                             # low so genuinely short-history recent IPOs still get
                             # cached (nothing gained by re-fetching them every call).
CACHE_KEEP_DAYS = 2          # local cache files older than "today or yesterday" are
                             # deleted on the next call (design spec §2: "保留最近 2
                             # 天，其餘刪"); CI runners are always fresh so this only
                             # matters for repeated local runs.


def _today_str():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


def _cache_path(date_str, auto_adjust):
    return CACHE_DIR / f"{date_str}_{'adj' if auto_adjust else 'raw'}.pkl"


def _cleanup_old_cache(keep_date_strs):
    if not CACHE_DIR.exists():
        return
    pat = re.compile(r'^(\d{4}-\d{2}-\d{2})_(adj|raw)\.pkl$')
    for f in CACHE_DIR.glob('*.pkl'):
        m = pat.match(f.name)
        if not m or m.group(1) not in keep_date_strs:
            try:
                f.unlink()
            except OSError:
                pass


def _load_cache(date_str, auto_adjust):
    p = _cache_path(date_str, auto_adjust)
    if not p.exists():
        return {}
    try:
        with open(p, 'rb') as fh:
            obj = pickle.load(fh)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _save_cache(date_str, auto_adjust, cache):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    p = _cache_path(date_str, auto_adjust)
    tmp = p.with_suffix('.pkl.tmp')
    with open(tmp, 'wb') as fh:
        pickle.dump(cache, fh, protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(p)


_PERIOD_RE = re.compile(r'^(\d+)(d|wk|mo|y)$')
_UNIT_DAYS = {'d': 1.0, 'wk': 7.0, 'mo': 30.44, 'y': 365.25}


def _period_to_start(period, end):
    """Approximate calendar start date for a yfinance-style period string
    ('15mo', '2y', ...) so a broader cached range can be trimmed down to
    reproduce what a direct `yf.download(period=period)` call would return.
    Falls back to a 15-month lookback for an unrecognized string (only
    '15mo'/'2y' are ever passed by this repo's callers)."""
    m = _PERIOD_RE.match(period)
    if not m:
        return end - timedelta(days=456)
    n, unit = int(m.group(1)), m.group(2)
    return end - timedelta(days=n * _UNIT_DAYS[unit])


def _fetch_missing(missing, auto_adjust):
    """Download `missing` tickers at CACHE_PERIOD in DOWNLOAD_BATCH_SIZE
    batches (each batch retried up to MAX_BATCH_RETRIES times on exception).
    Returns {ticker: per-ticker OHLCV DataFrame} — only for tickers that
    cleared MIN_TICKER_BARS; tickers that came back empty/short are simply
    absent (left for a later call to retry over the network)."""
    out = {}
    n_chunks = (len(missing) + DOWNLOAD_BATCH_SIZE - 1) // DOWNLOAD_BATCH_SIZE
    for i in range(0, len(missing), DOWNLOAD_BATCH_SIZE):
        chunk = missing[i:i + DOWNLOAD_BATCH_SIZE]
        chunk_no = i // DOWNLOAD_BATCH_SIZE + 1
        px = None
        for batch_attempt in range(1, MAX_BATCH_RETRIES + 1):
            try:
                px = yf.download(chunk, period=CACHE_PERIOD, interval='1d',
                                  auto_adjust=auto_adjust, group_by='ticker',
                                  progress=False, threads=True)
                break
            except Exception as e:
                print(f"      ! tech_core: batch {chunk_no}/{n_chunks} ({len(chunk)} tickers) "
                      f"attempt {batch_attempt}/{MAX_BATCH_RETRIES} raised {type(e).__name__}: {e}")
                if batch_attempt < MAX_BATCH_RETRIES:
                    time.sleep(5 + random.uniform(0, 3))
        if px is None or px.empty:
            if chunk_no < n_chunks:
                time.sleep(BATCH_SLEEP_SECONDS)
            continue
        for t in chunk:
            try:
                df = px[t]
            except Exception:
                continue
            if df is None or 'Close' not in df.columns:
                continue
            if df['Close'].dropna().shape[0] >= MIN_TICKER_BARS:
                out[t] = df
        if chunk_no < n_chunks:
            time.sleep(BATCH_SLEEP_SECONDS)
    return out


def download_prices(tickers, period='15mo', auto_adjust=True):
    """Return a yf.download(group_by='ticker')-shaped DataFrame covering
    exactly `tickers`, trimmed to `period`. See module docstring for the
    caching contract."""
    tickers = list(dict.fromkeys(tickers))  # de-dup, preserve order
    today = _today_str()
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y-%m-%d')
    _cleanup_old_cache({today, yesterday})

    cache = _load_cache(today, auto_adjust)
    missing = [t for t in tickers if t not in cache]

    if missing:
        print(f"  tech_core: {len(tickers)} requested, {len(tickers) - len(missing)} cache hit(s), "
              f"downloading {len(missing)} missing ticker(s) at period={CACHE_PERIOD} "
              f"auto_adjust={auto_adjust}...")
        fetched = _fetch_missing(missing, auto_adjust)
        if fetched:
            cache.update(fetched)
            _save_cache(today, auto_adjust, cache)
        still_missing = len(missing) - len(fetched)
        if still_missing:
            print(f"  tech_core: {still_missing} ticker(s) still missing after this fetch "
                  f"(empty/short-history or download failure)")
    else:
        print(f"  tech_core: {len(tickers)} requested, all {len(tickers)} served from cache "
              f"(0 downloaded)")

    end = datetime.now(timezone.utc).replace(tzinfo=None)
    start = _period_to_start(period, end)

    frames = {}
    for t in tickers:
        df = cache.get(t)
        if df is None:
            continue
        trimmed = df[df.index >= start]
        if not trimmed.empty:
            frames[t] = trimmed

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, axis=1)
