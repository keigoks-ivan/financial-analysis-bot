"""台股階段燈 (scripts/build_stages_tw.py) — owner decisions 2026-10-09.

Checks the three TW-specific inputs: universe = radar ∪ TW pool, liquidity floor
US$5M converted to TWD, 0050 as benchmark; and that the US PARAMS come back
unchanged after a TW build. Synthetic prices, no network.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime as real_datetime
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_rs_turn  # noqa: E402
import build_stages  # noqa: E402
import build_stages_tw as tw  # noqa: E402

FX = 32.0
N_DAYS = 300


def _frames():
    idx = pd.bdate_range('2025-06-02', periods=N_DAYS)
    up = np.linspace(100.0, 300.0, N_DAYS)
    closes = pd.DataFrame({
        'A.TW': up,                         # strong uptrend
        'B.TW': np.full(N_DAYS, 100.0),     # flat, thin trading
        '0050.TW': np.full(N_DAYS, 100.0),  # flat benchmark
    }, index=idx)
    # A: ~NT$6 億/day at the end ≈ US$18.75M — passes US$5M, would fail the US US$20M floor.
    # B: NT$1 億 flat ≈ US$3.1M — fails US$5M, would pass an unconverted 5,000,000.
    volumes = pd.DataFrame({
        'A.TW': np.full(N_DAYS, 2_000_000.0),
        'B.TW': np.full(N_DAYS, 1_000_000.0),
        '0050.TW': np.full(N_DAYS, 1e7),
    }, index=idx)
    return closes, volumes


def _patch(monkeypatch, tmp_path):
    closes, volumes = _frames()
    pool = tmp_path / 'tw_latest.json'
    pool.write_text(json.dumps({'stocks': [{'ticker': 'B.TW'}, {'ticker': 'C.TWO'}]}))
    out = tmp_path / 'lamp_tw.json'
    monkeypatch.setattr(tw.screener_tw, 'build_watchlist',
                        lambda: {'A.TW': {}, 'B.TW': {}})
    monkeypatch.setattr(tw, 'TW_POOL_JSON', pool)
    monkeypatch.setattr(tw, 'LAMP_TW_JSON', out)
    monkeypatch.setattr(tw, 'latest_twd_per_usd', lambda: FX)
    monkeypatch.setattr(tw, 'drop_unfinished_bar', lambda *f: f)

    seen = {}

    def fake_download(tickers, extra):
        seen['tickers'], seen['extra'] = list(tickers), list(extra)
        cols = ['A.TW', 'B.TW', '0050.TW']  # C.TWO has no prices
        return (closes[cols], closes[cols] * 1.01, closes[cols] * 0.99, closes[cols], volumes[cols])

    monkeypatch.setattr(build_stages, 'download_ohlcv_with_retry', fake_download)
    return out, seen


def test_universe_is_radar_plus_pool(monkeypatch, tmp_path):
    _patch(monkeypatch, tmp_path)
    tickers, sizes = tw.build_universe()
    assert tickers == ['A.TW', 'B.TW', 'C.TWO']
    assert sizes == {'radar': 2, 'pool': 2, 'total': 3}


def test_lamp_uses_tw_benchmark_and_converted_floor(monkeypatch, tmp_path):
    out, seen = _patch(monkeypatch, tmp_path)
    us_params = build_rs_turn.PARAMS
    lamp = tw.build()

    assert seen['extra'] == ['0050.TW']
    assert lamp == {'A.TW': 'S4', 'B.TW': 'S9'}
    doc = json.loads(out.read_text())
    assert doc['benchmark'] == '0050.TW'
    assert doc['adv_min_usd'] == 5_000_000
    assert doc['universe'] == {'radar': 2, 'pool': 2, 'total': 3, 'priced': 2, 'eligible': 1}
    # US settings are back in place after the build
    assert build_rs_turn.PARAMS is us_params
    assert build_rs_turn.PARAMS['adv_min_usd'] == 20_000_000


def test_drop_unfinished_bar_before_taipei_close(monkeypatch):
    idx = pd.to_datetime(['2026-10-07', '2026-10-08'])
    frame = pd.DataFrame({'X': [1.0, 2.0]}, index=idx)

    class At(real_datetime):
        hm = (10, 0)

        @classmethod
        def now(cls, tz=None):
            return real_datetime(2026, 10, 8, *cls.hm, tzinfo=tz)

    monkeypatch.setattr(tw, 'datetime', At)
    (kept,) = tw.drop_unfinished_bar(frame)
    assert list(kept.index) == [idx[0]]

    At.hm = (14, 30)
    (kept,) = tw.drop_unfinished_bar(frame)
    assert list(kept.index) == list(idx)
