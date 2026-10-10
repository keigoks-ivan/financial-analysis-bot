"""台股全市場雷達 (scripts/build_radar_tw.py), 2026-10-10.

US radar shapes on the TW stage universe; 主題下沉 on 0051 members with hot
industries of >= HOT_MIN_MEMBERS names; fail-safe when too few names have
enough weekly bars. Synthetic weekly closes, no network.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_radar_tw as rt  # noqa: E402

IDX = pd.date_range('2024-09-02', periods=109, freq='W-MON')


def _series(values):
    return pd.Series(np.asarray(values, dtype=float), index=IDX[-len(values):])


def _flat_then_up(gain):
    """100 for most of the window, then a linear climb to 100*(1+gain) over the last 20 weeks."""
    v = [100.0] * 89 + list(np.linspace(100, 100 * (1 + gain), 20))
    return _series(v)


def test_structure_matches_the_us_formulas():
    s = _series([100.0] * 50 + [200.0] + [120.0] * 57 + [150.0])     # high 58 weeks ago
    rows, as_of = rt.structure({'A.TW': s, 'SHORT.TW': _series([100.0] * 40)})
    assert [r['ticker'] for r in rows] == ['A.TW']                     # < 56 bars dropped
    r = rows[0]
    assert as_of == str(IDX[-1].date())
    assert r['ret_12m'] == 25.0 and r['ret_13w'] == 25.0
    assert r['dist_ath'] == -25.0 and r['base_age_w'] == 58 and r['depth'] == -40.0
    assert r['above_40w'] is True and r['rs_pct'] == 0.0


def _row(t, ret_13w, sector, tier='0051', rs=80.0):
    return {'ticker': t, 'ret_12m': 50.0, 'ret_13w': ret_13w, 'dist_ath': -2.0, 'base_age_w': 1,
            'depth': -5.0, 'above_40w': True, 'rs_pct': rs, 'sector': sector, 'tier': tier}


def test_small_industry_cannot_be_hot_and_theme_needs_0051():
    rows = ([_row(f'S{i}.TW', 90.0, '小產業') for i in range(rt.HOT_MIN_MEMBERS - 1)]
            + [_row(f'B{i}.TW', 30.0, '半導體業') for i in range(rt.HOT_MIN_MEMBERS)]
            + [_row('P.TW', 30.0, '半導體業', tier='pool'),
               _row('LOW.TW', 30.0, '半導體業', rs=50.0)])
    shapes, hot = rt.tag(rows)
    assert '小產業' not in hot and hot[0] == '半導體業'
    theme = [r['ticker'] for r in shapes['theme_smallmid']]
    assert theme and all(t.startswith('B') for t in theme)            # pool tier / low RS left out
    assert set(shapes) == set(rt.SHAPE_TEXT)


def _patch(monkeypatch, tmp_path, tickers):
    monkeypatch.setattr(rt, 'OUT_DIR', tmp_path)
    monkeypatch.setattr(rt, 'RADAR_TW_JSON', tmp_path / 'radar_tw.json')
    monkeypatch.setattr(rt, 'RADAR_TW_HTML', tmp_path / '_radar_tw_body.html')
    pool = tmp_path / 'pool.json'
    pool.write_text(json.dumps({'stocks': [{'ticker': tickers[0], 'tw_industry': '半導體業'}]}),
                    encoding='utf-8')
    monkeypatch.setattr(rt, 'TW_POOL_JSON', pool)
    monkeypatch.setattr(rt.build_stages_tw, 'universe_with_names',
                        lambda: (tickers, {'radar': len(tickers) - 1, 'pool': 1, 'total': len(tickers)},
                                 {t: '名' + t[0] for t in tickers}))
    monkeypatch.setattr(rt.screener_tw, 'build_watchlist', lambda: {t: {'etf': '0050'} for t in tickers[1:]})
    monkeypatch.setattr(rt, 'industries', lambda ts, stocks: {t: '半導體業' for t in ts})


def test_build_writes_fragment_and_json(monkeypatch, tmp_path):
    tickers = [f'{1000 + i}.TW' for i in range(11)]                   # top of 11 → RS 90.9
    _patch(monkeypatch, tmp_path, tickers)
    closes = {t: _flat_then_up(0.1 * (i + 1)) for i, t in enumerate(tickers)}
    payload = rt.build(closes)
    assert payload['scored_n'] == 11 and payload['universe_n'] == 11
    data = json.loads((tmp_path / 'radar_tw.json').read_text(encoding='utf-8'))
    assert data['schema_version'] == 'radar-tw-1' and data['params']['theme_tier'] == '0051'
    html = (tmp_path / '_radar_tw_body.html').read_text(encoding='utf-8')
    assert html.startswith('<div class="board-wrap">') and '台股全市場雷達' in html
    for label, _ in rt.SHAPE_TEXT.values():
        assert label in html
    mom = data['shapes']['momentum_rerate']
    assert [r['ticker'] for r in mom] == ['1010.TW']
    assert mom[0]['tier'] == '0050' and mom[0]['in_pool'] is False
    assert data['shapes']['breakout_base'] == []                    # high is this week, base 0


def test_too_few_scored_names_leaves_files_alone(monkeypatch, tmp_path):
    tickers = ['A.TW', 'B.TW', 'C.TW']
    _patch(monkeypatch, tmp_path, tickers)
    closes = {'A.TW': _flat_then_up(0.1), 'B.TW': _series([100.0] * 30), 'C.TW': _series([100.0] * 30)}
    assert rt.build(closes) is None
    assert not (tmp_path / 'radar_tw.json').exists()


def test_financials_count_in_rs_but_are_not_listed(monkeypatch, tmp_path):
    tickers = [f'{1000 + i}.TW' for i in range(10)] + ['2881.TW']
    _patch(monkeypatch, tmp_path, tickers)
    monkeypatch.setattr(rt, 'industries', lambda ts, stocks: {
        t: ('金融保險業' if t == '2881.TW' else '半導體業') for t in ts})
    # 2881 rises least; the best name ranks 10th of 11 (RS 90.9) only because
    # 2881 is in the comparison group — out of 10 it would be 9th of 10 (90.0)
    closes = {t: _flat_then_up(0.1 * (i + 2)) for i, t in enumerate(tickers[:10])}
    closes['2881.TW'] = _flat_then_up(0.05)
    payload = rt.build(closes)
    assert payload['scored_n'] == 11 and payload['excluded_n'] == 1
    mom = payload['shapes']['momentum_rerate']
    assert [r['ticker'] for r in mom] == ['1009.TW'] and mom[0]['rs_pct'] == 90.9
    html = (tmp_path / '_radar_tw_body.html').read_text(encoding='utf-8')
    assert '金融保險業 1 檔算進 RS 的比較對象，但不列出' in html and '2881' not in html


def test_missing_industry_is_retried(monkeypatch, tmp_path):
    tickers = [f'{1000 + i}.TW' for i in range(11)]
    _patch(monkeypatch, tmp_path, tickers)
    monkeypatch.setattr(rt, 'RETRY_WAIT_S', 0)
    calls = []

    def flaky(ts, stocks):                     # first call: roster cut off, last name missing
        calls.append(list(ts))
        return {t: '半導體業' for t in (ts[:-1] if len(calls) == 1 else ts)}
    monkeypatch.setattr(rt, 'industries', flaky)
    closes = {t: _flat_then_up(0.1 * (i + 1)) for i, t in enumerate(tickers)}
    assert rt.build(closes) is not None
    assert len(calls) == 2 and calls[1] == ['1010.TW']        # only the missing name is retried
    assert (tmp_path / 'radar_tw.json').exists()


def test_industry_still_missing_leaves_files_alone(monkeypatch, tmp_path, capsys):
    tickers = [f'{1000 + i}.TW' for i in range(11)]
    _patch(monkeypatch, tmp_path, tickers)
    monkeypatch.setattr(rt, 'RETRY_WAIT_S', 0)
    monkeypatch.setattr(rt, 'industries', lambda ts, stocks: {t: '半導體業' for t in ts if t != '1003.TW'})
    closes = {t: _flat_then_up(0.1 * (i + 1)) for i, t in enumerate(tickers)}
    assert rt.build(closes) is None
    assert not (tmp_path / 'radar_tw.json').exists() and not (tmp_path / '_radar_tw_body.html').exists()
    assert '::warning::radar-tw: 1 name(s) still without an official industry' in capsys.readouterr().out
