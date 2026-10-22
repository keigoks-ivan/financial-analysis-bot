"""tech_core.download_prices：Yahoo 最新一根日線 Close 為 NaN（只有 Volume）時，
不能讓 rs-turn / stages 的合格數崩掉（2026-10-19~21 事故）。"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tech_core  # noqa: E402
import build_rs_turn  # noqa: E402


def _frame(idx, n_nan_tail, rng):
    close = 100 + np.cumsum(rng.normal(0, 0.5, len(idx)))
    df = pd.DataFrame({'Open': close, 'High': close, 'Low': close,
                       'Close': close, 'Volume': 5_000_000.0}, index=idx)
    if n_nan_tail:
        df.iloc[-n_nan_tail:, df.columns.get_indexer(['Open', 'High', 'Low', 'Close'])] = np.nan
    return df


def _patched_download(monkeypatch, cache):
    monkeypatch.setattr(tech_core, '_cleanup_old_cache', lambda keep: None)
    monkeypatch.setattr(tech_core, '_load_cache', lambda d, a: dict(cache))
    return tech_core.download_prices(list(cache), period='2y')


def _eligible_today(px):
    closes = px.xs('Close', axis=1, level=1)
    vols = px.xs('Volume', axis=1, level=1)
    qqq = closes['QQQ'].dropna()
    m = build_rs_turn.compute_metrics(closes.drop(columns=['QQQ']), vols.drop(columns=['QQQ']), qqq)
    return int(m['eligible'].iloc[-1].sum()), closes.index[-1]


def _make_cache(last_row_valid_tickers):
    rng = np.random.default_rng(0)
    end = pd.Timestamp.now("UTC").tz_localize(None).normalize()
    idx = pd.bdate_range(end=end, periods=300)
    cache = {}
    names = ['QQQ'] + [f'T{i}' for i in range(40)]
    for i, t in enumerate(names):
        df = _frame(idx, 1, rng)           # 最後一根 OHLC 全 NaN、Volume 有值
        if i < last_row_valid_tickers:      # 少數幾檔最後一根已定稿
            df.iloc[-1, df.columns.get_indexer(['Open', 'High', 'Low', 'Close'])] = 100.0
        cache[t] = df
    return cache, idx


def test_mostly_nan_last_row_is_dropped(monkeypatch):
    cache, idx = _make_cache(last_row_valid_tickers=2)   # 41 檔只有 2 檔有最後一根
    px = _patched_download(monkeypatch, cache)
    n_elig, last = _eligible_today(px)
    assert last == idx[-2]                  # 未定稿的最後一天被丟掉
    assert n_elig == 40                     # 合格數回到全部（不是 0~4）


def test_fully_settled_last_row_is_kept(monkeypatch):
    cache, idx = _make_cache(last_row_valid_tickers=41)
    px = _patched_download(monkeypatch, cache)
    n_elig, last = _eligible_today(px)
    assert last == idx[-1]
    assert n_elig == 40
