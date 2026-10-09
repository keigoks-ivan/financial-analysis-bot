"""
台股階段燈 — docs/stages/data/lamp_tw.json (2026-10-09).

Same lifecycle stages as the US 個股階段雷達 (scripts/build_stages.py):
compute_stage_frame() and build_rs_turn.compute_metrics() are imported, not
copied, so every stage threshold stays identical to the US lamp. Only the three
market-bound inputs change (owner decisions 2026-10-09, knowledge/rule_ledger.md
「台股階段燈」):

  1. Benchmark: 0050.TW dividend-adjusted (US: QQQ for S1/S0 relative strength,
     SPY for rs_line_high). Both slots get 0050 — adjusted vs adjusted, so the
     dividend yield does not tilt relative strength the way ^TWII (price index)
     would.
  2. Liquidity: 20-day average traded value >= US$5M (US: US$20M). Prices and
     volumes stay in TWD; the USD floor is converted once at the latest TWD=X
     rate. Only today's lamp is written, so one rate is enough.
  3. RS percentile population (S4 needs rs_ibd_pct >= 80): 0050 + 0051 + 00714
     constituents (screener_tw.build_watchlist(), the TW RS radar universe)
     plus the TW DD pool (docs/dd-screener/tw/latest.json).

PARAMS['price_min'] (5) is read as NT$5. No name in this universe trades that
low, so the price floor has no effect here.

Writes the lamp only ({ticker: stage code}). No history.json / transitions /
latest.json: the US /stages/ page and its base rates stay US-only.

Usage:
  python3 scripts/build_stages_tw.py
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_rs_turn
import build_stages
import screener_tw

ROOT = Path(__file__).resolve().parent.parent
TW_POOL_JSON = ROOT / 'docs' / 'dd-screener' / 'tw' / 'latest.json'
LAMP_TW_JSON = build_stages.DATA_DIR / 'lamp_tw.json'

BENCHMARK_TW = '0050.TW'
ADV_MIN_USD_TW = 5_000_000
TW_CLOSE_CUTOFF = (14, 30)  # Taipei; before this the day's bar is still forming


def _warn(msg):
    print(f"::warning::stages-tw: {msg}")


def build_universe():
    """0050/0051/00714 constituents ∪ TW DD pool, radar order first."""
    tickers = list(screener_tw.build_watchlist().keys())
    n_radar = len(tickers)
    pool = [s['ticker'] for s in json.loads(TW_POOL_JSON.read_text(encoding='utf-8'))['stocks']]
    tickers += [t for t in pool if t not in tickers]
    return tickers, {'radar': n_radar, 'pool': len(pool), 'total': len(tickers)}


def latest_twd_per_usd():
    fx = yf.download('TWD=X', period='1mo', auto_adjust=True, progress=False)['Close'].dropna()
    if isinstance(fx, pd.DataFrame):
        fx = fx.iloc[:, 0]
    if fx.empty:
        raise RuntimeError('TWD=X returned no data')
    return float(fx.iloc[-1])


def drop_unfinished_bar(*frames):
    """Before 14:30 Taipei, today's bar (if present) is intraday — drop it."""
    now_tpe = datetime.now(timezone(timedelta(hours=8)))
    if (now_tpe.hour, now_tpe.minute) >= TW_CLOSE_CUTOFF:
        return frames
    today = pd.Timestamp(now_tpe.date())
    return tuple(f[f.index.normalize() < today] for f in frames)


def build():
    run_started = datetime.now(timezone.utc)
    print(f"=== Stages TW Build ({build_stages.DEFINITION_VERSION}) — {run_started.isoformat()} ===")

    tickers, sizes = build_universe()
    print(f"  universe: {sizes}")

    twd_per_usd = latest_twd_per_usd()
    print(f"  TWD/USD {twd_per_usd:.2f} → liquidity floor NT${ADV_MIN_USD_TW * twd_per_usd / 1e8:.2f} 億/日")
    # compute_metrics() and compute_stage_frame() read the module-level PARAMS at
    # call time. Swap in the TW values for this build only and put the US values
    # back afterwards, so nothing else in the process sees them.
    us_params = build_rs_turn.PARAMS
    build_rs_turn.PARAMS = {**us_params,
                            'benchmark': BENCHMARK_TW,
                            'adv_min_usd': ADV_MIN_USD_TW * twd_per_usd}
    try:
        return _build_with_tw_params(tickers, sizes, twd_per_usd)
    finally:
        build_rs_turn.PARAMS = us_params


def _build_with_tw_params(tickers, sizes, twd_per_usd):
    try:
        _o, highs, lows, closes, volumes = build_stages.download_ohlcv_with_retry(tickers, [BENCHMARK_TW])
    except RuntimeError as e:
        _warn(f"{e} — abort, lamp_tw.json untouched")
        return None
    highs, lows, closes, volumes = drop_unfinished_bar(highs, lows, closes, volumes)

    bench = closes[BENCHMARK_TW].dropna() if BENCHMARK_TW in closes.columns else pd.Series(dtype=float)
    if bench.empty:
        _warn(f"benchmark {BENCHMARK_TW} missing — abort, lamp_tw.json untouched")
        return None
    cols = [t for t in tickers if t in closes.columns]
    C, H, L, V = closes[cols], highs[cols], lows[cols], volumes[cols]

    stage, fields = build_stages.compute_stage_frame(H, L, C, V, bench, bench)
    as_of_idx = C.index[-1]
    stage_today = stage.loc[as_of_idx]
    lamp = {t: stage_today[t] for t in cols}
    counts = {code: int((stage_today == code).sum())
              for code in ('S0', 'S1', 'S2', 'S5', 'S3', 'S4', 'S9')}
    n_eligible = int(fields['eligible'].loc[as_of_idx].sum())

    LAMP_TW_JSON.write_text(json.dumps({
        'as_of': as_of_idx.strftime('%Y-%m-%d'),
        'definition_version': build_stages.DEFINITION_VERSION,
        'benchmark': BENCHMARK_TW,
        'adv_min_usd': ADV_MIN_USD_TW,
        'twd_per_usd': round(twd_per_usd, 4),
        'universe': {**sizes, 'priced': len(cols), 'eligible': n_eligible},
        'lamp': lamp,
    }, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {LAMP_TW_JSON}: {len(lamp)} tickers, "
          f"eligible {n_eligible}, counts {counts}")
    return lamp


def main():
    try:
        result = build()
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — lamp_tw.json left unchanged")
        _warn(f"build failed ({type(e).__name__}: {e})")
        sys.exit(0)
    if result is None:
        sys.exit(0)


if __name__ == '__main__':
    main()
