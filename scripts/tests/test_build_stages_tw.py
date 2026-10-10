"""台股階段燈 (scripts/build_stages_tw.py) — owner decisions 2026-10-09.

Checks the three TW-specific inputs: universe = radar ∪ TW pool, liquidity floor
US$5M converted to TWD, 0050 as benchmark; that the US PARAMS come back
unchanged after a TW build; and (2026-10-10) the history_tw / latest_tw files
for the /stages/tw/ page. Synthetic prices, no network.
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
                        lambda: {'A.TW': {'name': '甲'}, 'B.TW': {'name': '乙'}})
    monkeypatch.setattr(tw, 'TW_POOL_JSON', pool)
    monkeypatch.setattr(tw, 'LAMP_TW_JSON', out)
    monkeypatch.setattr(tw, 'HISTORY_TW_JSON', tmp_path / 'history_tw.json')
    monkeypatch.setattr(tw, 'LATEST_TW_JSON', tmp_path / 'latest_tw.json')
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


def test_drop_sparse_dates_removes_a_whole_market_hole():
    idx = pd.bdate_range('2025-07-30', periods=4)
    closes = pd.DataFrame({'A.TW': [1.0, np.nan, 3.0, 4.0], 'B.TW': [1.0, np.nan, np.nan, 4.0],
                           '0050.TW': [1.0, 2.0, 3.0, 4.0]}, index=idx)
    h, l, c, v = tw.drop_sparse_dates(['A.TW', 'B.TW'], closes, closes, closes, closes)
    # day 2: no stock priced (0050 alone) → dropped; day 3: half priced → kept
    assert list(c.index) == [idx[0], idx[2], idx[3]]
    assert list(h.index) == list(v.index) == list(c.index)


def test_one_hole_day_does_not_turn_the_window_into_transition(monkeypatch, tmp_path):
    def non_transition_days():
        tw.build()
        hist = json.loads((tmp_path / 'history_tw.json').read_text())
        (tmp_path / 'history_tw.json').unlink()
        return sum(c != '9' for c in hist['stages']['A.TW'])

    _patch(monkeypatch, tmp_path)
    clean = non_transition_days()

    closes, volumes = _frames()
    closes.iloc[10, :2] = np.nan        # stocks blank on one day, 0050 still priced
    cols = ['A.TW', 'B.TW', '0050.TW']
    monkeypatch.setattr(build_stages, 'download_ohlcv_with_retry', lambda t, e: (
        closes[cols], closes[cols] * 1.01, closes[cols] * 0.99, closes[cols], volumes[cols]))
    assert clean > 0 and non_transition_days() >= clean - 1


def test_history_and_latest_for_the_tw_page(monkeypatch, tmp_path):
    _patch(monkeypatch, tmp_path)
    tw.build()

    hist = json.loads((tmp_path / 'history_tw.json').read_text())
    assert hist['schema'] == 'stages-history-v2' and hist['benchmark'] == '0050.TW'
    # 300 rows: the data check first passes on row 251 and the 252-day return
    # that 領先 needs exists from row 252, so the window is the last 48 rows,
    # not the last 250 (which would start in the warm-up)
    win = N_DAYS - 252
    assert len(hist['dates']) == win and hist['dates'][0] == str(_frames()[0].index[252].date())
    assert set(hist['stages']) == {'A.TW', 'B.TW'}
    assert hist['stages']['A.TW'][0] != '9'                            # no warm-up days
    assert hist['stages']['B.TW'] == '9' * win                          # never liquid enough
    assert hist['qqq'][-1] == 100.0                                    # the 0050 close

    latest = json.loads((tmp_path / 'latest_tw.json').read_text())
    assert latest['market'] == 'tw' and latest['benchmark'] == '0050.TW'
    assert latest['counts_today']['S4'] == 1 and latest['counts_today']['S9'] == 1
    assert {'rows', 'baseline', 'control_deep_pullback'} <= set(latest['transitions'])
    s1p = latest['params']['s1_params']
    assert s1p['benchmark'] == '0050.TW' and s1p['adv_min_usd'] == 5_000_000 * FX
    assert latest['params']['window_days'] == win
    (row,) = latest['rows']
    assert row['ticker'] == 'A.TW' and row['name'] == '甲' and row['stage'] == 'S4'
    # prices are TWD: 300 x 2,000,000 shares ≈ NT$6 億 → US$ at 32
    assert abs(row['adv20_twd'] / row['adv20_usd'] - FX) < 0.01


def test_history_merge_keeps_dates_before_the_window(monkeypatch, tmp_path):
    _patch(monkeypatch, tmp_path)
    old = {'dates': ['2020-01-02'], 'counts': {c: [0] for c in ('S0', 'S1', 'S2', 'S5', 'S3', 'S4')},
           'qqq': [50.0], 'stages': {'Z.TW': '4'}, 'deep': {'Z.TW': '0'}}
    (tmp_path / 'history_tw.json').write_text(json.dumps(old))
    tw.build()
    hist = json.loads((tmp_path / 'history_tw.json').read_text())
    assert hist['dates'][0] == '2020-01-02' and len(hist['dates']) == N_DAYS - 252 + 1
    assert hist['stages']['Z.TW'][0] == '4'
    assert hist['stages']['A.TW'][0] == '9'      # no data on the old date
