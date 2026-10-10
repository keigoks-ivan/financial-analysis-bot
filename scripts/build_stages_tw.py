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
     rate (see the history caveat below).
  3. RS percentile population (S4 needs rs_ibd_pct >= 80): 0050 + 0051 + 006201
     constituents (screener_tw.build_watchlist(), the TW RS radar universe)
     plus the TW DD pool (docs/dd-screener/tw/latest.json).

PARAMS['price_min'] (5) is read as NT$5. No name in this universe trades that
low, so the price floor has no effect here.

Outputs (2026-10-10 adds the last two for the /stages/tw/ page):
  docs/stages/data/lamp_tw.json     today's stage per ticker (cockpit-tw, seats)
  docs/stages/data/history_tw.json  250-trading-day stage strings, same schema and
                                    merge as the US history.json
                                    (build_stages.merge_history); the "qqq" key
                                    holds the 0050 close so the page code is shared
  docs/stages/data/latest_tw.json   counts, transition base rates and the S1-S4
                                    rows, same schema as the US latest.json plus
                                    name / adv20_twd

History caveat: the liquidity floor is converted at today's TWD=X rate for the
whole 250-day window. A name near the floor can flip between eligible and S9 on
older dates if the rate moved; the stage thresholds themselves do not depend on
the rate.

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
HISTORY_TW_JSON = build_stages.DATA_DIR / 'history_tw.json'
LATEST_TW_JSON = build_stages.DATA_DIR / 'latest_tw.json'

BENCHMARK_TW = '0050.TW'
ADV_MIN_USD_TW = 5_000_000
TW_CLOSE_CUTOFF = (14, 30)  # Taipei; before this the day's bar is still forming
MIN_PRESENT_SHARE = 0.5     # a date where fewer stocks than this have a close is dropped


def _warn(msg):
    print(f"::warning::stages-tw: {msg}")


def build_universe():
    """0050/0051/006201 constituents ∪ TW DD pool, radar order first."""
    tickers, sizes, _names = universe_with_names()
    return tickers, sizes


def universe_with_names():
    """build_universe() plus {ticker: Chinese name} (constituent lists first,
    then the pool's names)."""
    wl = screener_tw.build_watchlist()
    pool = json.loads(TW_POOL_JSON.read_text(encoding='utf-8'))['stocks']
    tickers = list(wl.keys())
    tickers += [s['ticker'] for s in pool if s['ticker'] not in wl]
    names = {t: v.get('name') for t, v in wl.items()}
    for s in pool:
        if not names.get(s['ticker']) and s.get('name') and s['name'] != s['ticker']:
            names[s['ticker']] = s['name']
    return tickers, {'radar': len(wl), 'pool': len(pool), 'total': len(tickers)}, names


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


def drop_sparse_dates(tickers, highs, lows, closes, volumes):
    """yfinance has whole-market holes on some TW dates: 2025-08-01 was a
    normal session (0050 traded) but every individual stock is NaN, even on a
    fresh download. One such row keeps compute_metrics()'s "252 closes in the
    last 252 rows" check false for every stock for a year, so the whole
    history window turns 過渡. Drop dates where fewer than MIN_PRESENT_SHARE
    of the stocks have a close (benchmark included in the drop)."""
    cols = [t for t in tickers if t in closes.columns]
    if not cols:
        return highs, lows, closes, volumes
    share = closes[cols].notna().mean(axis=1)
    sparse = share.index[share < MIN_PRESENT_SHARE]
    if len(sparse):
        print(f"  dropped {len(sparse)} date(s) with < {MIN_PRESENT_SHARE:.0%} of stocks priced: "
              f"{', '.join(d.strftime('%Y-%m-%d') for d in sparse)}")
    keep = share.index[share >= MIN_PRESENT_SHARE]
    return tuple(f.loc[keep] for f in (highs, lows, closes, volumes))


def build():
    run_started = datetime.now(timezone.utc)
    print(f"=== Stages TW Build ({build_stages.DEFINITION_VERSION}) — {run_started.isoformat()} ===")

    tickers, sizes, names = universe_with_names()
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
        return _build_with_tw_params(tickers, sizes, twd_per_usd, names)
    finally:
        build_rs_turn.PARAMS = us_params


def _build_with_tw_params(tickers, sizes, twd_per_usd, names=None):
    try:
        _o, highs, lows, closes, volumes = build_stages.download_ohlcv_with_retry(tickers, [BENCHMARK_TW])
    except RuntimeError as e:
        _warn(f"{e} — abort, TW stage files untouched")
        return None
    highs, lows, closes, volumes = drop_unfinished_bar(highs, lows, closes, volumes)
    highs, lows, closes, volumes = drop_sparse_dates(tickers, highs, lows, closes, volumes)

    bench = closes[BENCHMARK_TW].dropna() if BENCHMARK_TW in closes.columns else pd.Series(dtype=float)
    if bench.empty:
        _warn(f"benchmark {BENCHMARK_TW} missing — abort, TW stage files untouched")
        return None
    cols = [t for t in tickers if t in closes.columns]
    C, H, L, V = closes[cols], highs[cols], lows[cols], volumes[cols]

    stage, fields = build_stages.compute_stage_frame(H, L, C, V, bench, bench)
    as_of_idx = C.index[-1]
    as_of = as_of_idx.strftime('%Y-%m-%d')
    stage_today = stage.loc[as_of_idx]
    lamp = {t: stage_today[t] for t in cols}
    counts = {code: int((stage_today == code).sum())
              for code in ('S0', 'S1', 'S2', 'S5', 'S3', 'S4', 'S9')}
    n_eligible = int(fields['eligible'].loc[as_of_idx].sum())
    n_covered = int((C.notna().sum() >= build_rs_turn.PARAMS['min_bars']).sum())
    universe = {**sizes, 'priced': len(cols), 'covered': n_covered, 'eligible': n_eligible}

    # History and base rates: the same merge and transition table as the US
    # build (build_stages.build()), on the TW frame. The window is the last
    # WINDOW_DAYS rows, but no earlier than the first day every stage can be
    # assigned: some stock passes compute_metrics()'s data check (252 closes in
    # the last 252 rows) AND has the 252-day return that 領先 (rs_ibd_pct) needs,
    # which arrives one row later. Two years of TW sessions is only ~484 rows,
    # so the last 250 would start ~17 days inside that warm-up: every stock
    # 過渡, then ~200 names "entering" a stage on the same day (and ~25 more
    # moving 高檔整理→領先 the day after), which the transition table counts
    # as events.
    ready = fields['eligible'] & fields['rs_ibd_pct'].notna()
    first_ok = int(ready.any(axis=1).values.argmax())
    window_idx = stage.index[max(len(stage.index) - build_stages.WINDOW_DAYS, first_ok):]
    stage_window = stage.loc[window_idx]
    window_dates = [d.strftime('%Y-%m-%d') for d in window_idx]
    bench_window = fields['qqq'].reindex(window_idx).values
    deep_window = fields['deep'].reindex(columns=stage_window.columns).loc[window_idx]
    existing = None
    if HISTORY_TW_JSON.exists():
        try:
            existing = json.loads(HISTORY_TW_JSON.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            existing = None
    history = build_stages.merge_history(existing, window_dates, stage_window, bench_window, deep_window)
    history['benchmark'] = BENCHMARK_TW
    transitions = build_stages.build_transitions_table(stage_window, deep_window)
    rows = detail_rows(cols, stage_today, fields, C, as_of_idx, history, names or {}, twd_per_usd)

    LATEST_TW_JSON.parent.mkdir(parents=True, exist_ok=True)
    LATEST_TW_JSON.write_text(json.dumps({
        'schema': 'stages-v1',
        'market': 'tw',
        'definition_version': build_stages.DEFINITION_VERSION,
        'transitions_version': build_stages.TRANSITIONS_VERSION,
        'as_of': as_of,
        'run_timestamp': datetime.now(timezone.utc).isoformat(),
        'benchmark': BENCHMARK_TW,
        'adv_min_usd': ADV_MIN_USD_TW,
        'twd_per_usd': round(twd_per_usd, 4),
        'params': page_params(len(window_idx)),
        'universe': universe,
        'counts_today': counts,
        'transitions': transitions,
        'rows': rows,
    }, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    HISTORY_TW_JSON.write_text(json.dumps(history, ensure_ascii=False, indent=1) + '\n',
                               encoding='utf-8')
    LAMP_TW_JSON.write_text(json.dumps({
        'as_of': as_of,
        'definition_version': build_stages.DEFINITION_VERSION,
        'benchmark': BENCHMARK_TW,
        'adv_min_usd': ADV_MIN_USD_TW,
        'twd_per_usd': round(twd_per_usd, 4),
        'universe': {k: v for k, v in universe.items() if k != 'covered'},
        'lamp': lamp,
    }, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {LAMP_TW_JSON}: {len(lamp)} tickers, "
          f"eligible {n_eligible}, counts {counts}")
    print(f"  ✓ wrote {HISTORY_TW_JSON.name}: {len(history['dates'])} dates; "
          f"{LATEST_TW_JSON.name}: {len(rows)} rows")
    return lamp


def page_params(window_days=build_stages.WINDOW_DAYS):
    """The US latest.json 'params' block, read from build_stages. s1_params is
    build_rs_turn.PARAMS as swapped in for this build (0050, TWD floor)."""
    bs = build_stages
    return {
        's4_rs_ibd_min': bs.S4_RS_IBD_MIN, 's4_dist_high_min_pct': bs.S4_DIST_HIGH_MIN_PCT,
        's3_dist_high_min_pct': bs.S3_DIST_HIGH_MIN_PCT, 's3_atr_ratio_max': bs.S3_ATR_RATIO_MAX,
        's3_vol_ratio_max': bs.S3_VOL_RATIO_MAX, 's5_dist_high_min_pct': bs.S5_DIST_HIGH_MIN_PCT,
        's2_dist_high_min_pct': bs.S2_DIST_HIGH_MIN_PCT,
        's2_dist_high_max_pct': bs.S2_DIST_HIGH_MAX_PCT, 's2_tt_min': bs.S2_TT_MIN,
        'extended_pct_above_e21': bs.EXTENDED_PCT_ABOVE_E21, 'extended_rsi_min': bs.EXTENDED_RSI_MIN,
        'window_days': window_days, 'forward_days': bs.FORWARD_DAYS,
        'recency_min_days': bs.RECENCY_MIN_DAYS,
        's1_params': dict(build_rs_turn.PARAMS),
        'control_not_s1_lookback_days': bs.CONTROL_NOT_S1_LOOKBACK_DAYS,
    }


def detail_rows(cols, stage_today, fields, C, as_of_idx, history, names, twd_per_usd):
    """S1/S2/S5/S3/S4 rows for latest_tw.json — the US build()'s row loop, plus
    the Chinese name and the 20-day traded value in TWD. adv20_usd is the TWD
    value at today's rate (prices are in TWD, so fields['adv20_usd'] is TWD)."""
    rows = []
    for t in cols:
        s = stage_today[t]
        if s not in ('S1', 'S2', 'S5', 'S3', 'S4'):
            continue
        info = build_stages.ticker_path_info(history['stages'].get(t, ''), history['dates'])
        if info is None:
            continue
        adv_twd = fields['adv20_usd'].at[as_of_idx, t]
        hub = f"/t/{t}.html" if (build_stages.DOCS_T_DIR / f"{t}.html").exists() else None
        rows.append({
            'ticker': t, 'name': names.get(t), 'stage': s, 'stage_name': build_stages.STAGE_NAMES[s],
            'days_in_stage': info['days_in_stage'], 'stage_since': info['stage_since'],
            'prev_stage': info['prev_stage'], 'prev_stage_ended': info['prev_stage_ended'],
            'path': info['path'],
            'rs_ibd_pct': build_stages._num(fields['rs_ibd_pct'].at[as_of_idx, t], 1),
            'rs21': build_stages._num(fields['rs21'].at[as_of_idx, t], 1),
            'rs63': build_stages._num(fields['rs63'].at[as_of_idx, t], 1),
            'dist_52w_high_pct': build_stages._num(fields['dist_high_pct'].at[as_of_idx, t], 1),
            'tt_pass_count': int(fields['tt_pass_count'].at[as_of_idx, t]),
            'atr_ratio': build_stages._num(fields['atr_ratio'].at[as_of_idx, t], 2),
            'vol_ratio': build_stages._num(fields['vol_ratio'].at[as_of_idx, t], 2),
            'extended': bool(fields['extended'].at[as_of_idx, t]),
            'rs_line_high': bool(fields['rs_line_high'].at[as_of_idx, t]),
            'adv20_twd': int(round(adv_twd)) if pd.notna(adv_twd) else None,
            'adv20_usd': int(round(adv_twd / twd_per_usd)) if pd.notna(adv_twd) else None,
            'price': build_stages._num(C.at[as_of_idx, t], 2),
            'hub': hub,
        })
    stage_order = {'S1': 0, 'S2': 1, 'S5': 2, 'S3': 3, 'S4': 4}
    rows.sort(key=lambda r: (stage_order.get(r['stage'], 9), r['days_in_stage']))
    return rows


def main():
    try:
        result = build()
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — TW stage files left unchanged")
        _warn(f"build failed ({type(e).__name__}: {e})")
        sys.exit(0)
    if result is None:
        sys.exit(0)


if __name__ == '__main__':
    main()
