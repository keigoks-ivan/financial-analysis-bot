"""台股核心席 v5.8（2026-10-21 持有人破例決定）：每月依波動分配每席大小（SeatRebal R2）。

規則照 v7-backtest docs/SeatRebal_Prereg.md（f6d7dfd）第三節：每月第一個決策週，在席者的基本權重＝
（有 σ 檔數 ÷ 席位數）×（1/σ）÷ Σ（1/σ），σ＝近 60 個交易日日報酬的樣本標準差，缺 σ 的拿 1/席位數；
當週與月中新進席用 1/席位數，到下個調倉日才一起調。合成資料，不連網（fetch_closes 一律換掉）。
"""
from __future__ import annotations

import math
import statistics
import sys
from datetime import date
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_seats_tw as tw  # noqa: E402
from test_build_seats_tw import _rev, _stock  # noqa: E402
from test_seats_tw_x1 import BULL_CLOSES, env  # noqa: E402,F401


def _closes(daily, n=61, start=100.0):
    """n 個收盤：日報酬在 +daily 與 −daily 之間交替。"""
    out = [start]
    for k in range(n - 1):
        out.append(out[-1] * (1 + (daily if k % 2 == 0 else -daily)))
    return out


# ── 純函式 ──────────────────────────────────────────────────────────────

def test_sigma_is_the_sample_std_of_60_daily_returns():
    c = _closes(0.02)
    rets = [c[k + 1] / c[k] - 1 for k in range(60)]
    assert math.isclose(tw.sigma_from_closes(c), statistics.stdev(rets), rel_tol=1e-12)


def test_sigma_missing_cases():
    assert tw.sigma_from_closes(_closes(0.02, n=60)) is None            # 收盤不足 61 個
    c = _closes(0.02)
    assert tw.sigma_from_closes(c[:30] + [float('nan')] + c[31:]) is None
    assert tw.sigma_from_closes(c[:30] + [0.0] + c[31:]) is None
    assert tw.sigma_from_closes([100.0] * 61) is None                    # σ 為 0
    assert tw.sigma_from_closes(_closes(0.12)) is None                   # 超過漲跌幅上限＝資料錯誤
    assert tw.sigma_from_closes(_closes(0.099)) is not None


def test_vol_base_keeps_the_equal_weight_total_and_splits_by_inverse_sigma():
    b = tw.vol_base(['A', 'B', 'C'], {'A': 0.01, 'B': 0.02, 'C': None})
    assert math.isclose(sum(b.values()), 3 / 5)
    assert b['C'] == 0.2                                                 # 缺 σ 拿 1/席位數
    assert math.isclose(b['A'] + b['B'], 2 / 5) and math.isclose(b['A'], 2 * b['B'])
    assert tw.vol_base(['A'], {'A': 0.03}) == {'A': 0.2}
    assert tw.vol_base([], {}) == {}


def test_rebal_day_is_the_first_saturday_decision_of_a_month():
    snaps = [{'date': '2026-10-30'}]
    assert tw.is_rebal_day(True, snaps, '2026-11-06')
    assert not tw.is_rebal_day(True, snaps, '2026-10-31')
    assert not tw.is_rebal_day(False, snaps, '2026-11-06')                # 平日只刷燈號
    assert not tw.is_rebal_day(True, [], '2026-11-06')                   # 第一次跑不算


def test_update_vol_rebal_paths(monkeypatch):
    sig = {'A.TW': 0.01, 'B.TW': 0.03}
    monkeypatch.setattr(tw, 'fetch_closes', lambda ts, d: {t: _closes(sig[t]) for t in ts})
    prior = [{'date': '2026-10-30', 'core': ['A.TW', 'B.TW']}]
    rb, now = tw.update_vol_rebal({}, True, prior, '2026-11-06', ['A.TW', 'B.TW', 'N.TW'], ['A.TW', 'B.TW'],
                                  log=lambda m: None)
    assert now and rb['decision_date'] == '2026-11-06'
    assert set(rb['base']) == {'A.TW', 'B.TW'}                           # 新進者不調
    assert rb['base']['A.TW'] > 0.2 > rb['base']['B.TW']
    assert rb['prev_base'] == {'A.TW': 0.2, 'B.TW': 0.2}
    # 同一決策日重跑：沿用、不再通知
    rb2, now2 = tw.update_vol_rebal(rb, True, prior, '2026-11-06', ['A.TW', 'B.TW'], ['A.TW', 'B.TW'])
    assert rb2 == rb and not now2
    # 平日：不動
    assert tw.update_vol_rebal(rb, False, [], '2026-11-09', ['A.TW'], ['A.TW', 'B.TW']) == (rb, False)
    # 下個週六（同月）：離席的丟掉
    rb3, now3 = tw.update_vol_rebal(rb, True, [{'date': '2026-11-06'}], '2026-11-13', ['A.TW'], ['A.TW', 'B.TW'])
    assert not now3 and set(rb3['base']) == {'A.TW'} and set(rb3['sigma']) == {'A.TW'}


def test_seat_weights_multiply_the_lamp_size_and_default_to_equal():
    rows = [{'ticker': 'A.TW', 'lamp': {'size': 0.5}}, {'ticker': 'N.TW', 'lamp': {'size': 1.0}},
            {'ticker': 'R.TW', 'lamp': {'size': 0}}]
    w = tw.seat_weights(rows, {'base': {'A.TW': 0.3}, 'sigma': {'A.TW': 0.01}})
    assert (w['A.TW']['target'], w['A.TW']['src']) == (0.15, 'vol')
    assert (w['N.TW']['target'], w['N.TW']['src']) == (0.2, 'equal')
    assert w['R.TW']['target'] == 0.0


def test_next_rebal_month():
    assert tw.next_rebal_month('2026-10-30') == 11
    assert tw.next_rebal_month('2026-12-04') == 1


# ── build()：端到端 ─────────────────────────────────────────────────────

def test_end_to_end_month_turn_rebalances_incumbents_and_writes_the_alert(env, monkeypatch, tmp_path):
    alert = tmp_path / 'alert.txt'
    monkeypatch.setattr(tw, 'REBAL_ALERT_TXT', alert)
    sig = {'1000.TW': 0.01, '3000.TW': 0.02}
    calls = []

    def fake_fetch(ts, d):
        calls.append((list(ts), d))
        return {t: _closes(sig[t]) for t in ts}
    monkeypatch.setattr(tw, 'fetch_closes', fake_fetch)

    # 週 0（10-30）：兩檔入席，月中，等權
    env.market(BULL_CLOSES, date(2026, 10, 30))
    env.pool_json([_stock('1000.TW', **_rev(20)), _stock('3000.TW', **_rev(10))], '2026-10-23')
    tw.build(True, today=date(2026, 10, 24))
    env.pool_json([_stock('1000.TW', **_rev(20)), _stock('3000.TW', **_rev(10))], '2026-10-30')
    tw.build(True, today=date(2026, 10, 31))
    d = env.seats()
    assert [c['ticker'] for c in d['core_seats']] == ['1000.TW', '3000.TW']
    assert [c['seat_target_pct'] for c in d['core_seats']] == [20.0, 20.0]
    assert calls == [] and not alert.exists()
    assert d['vol_rebal'] == {'decision_date': None, 'next_month': 11, 'stock_total_pct': 40.0}
    assert '本月占比' in env.html() and '還沒調整過' in env.html()

    # 週 1（11-06）：換月，兩檔在席者依波動調、新進 2000.TW 用等權
    env.market(BULL_CLOSES, date(2026, 11, 6))
    stocks = [_stock('1000.TW', **_rev(20)), _stock('3000.TW', **_rev(10)), _stock('2000.TW', **_rev(5))]
    env.pool_json(stocks, '2026-11-06')
    tw.build(True, today=date(2026, 11, 7))
    d = env.seats()
    by = {c['ticker']: c for c in d['core_seats']}
    assert calls == [(['1000.TW', '3000.TW'], '2026-11-06')]
    assert math.isclose(by['1000.TW']['seat_base_pct'] + by['3000.TW']['seat_base_pct'], 40.0)
    assert by['1000.TW']['seat_base_pct'] > 20 > by['3000.TW']['seat_base_pct']
    assert by['2000.TW']['seat_target_pct'] == 20.0 and by['2000.TW']['seat_weight_src'] == 'equal'
    assert d['vol_rebal']['decision_date'] == '2026-11-06' and d['vol_rebal']['next_month'] == 12
    text = alert.read_text(encoding='utf-8')
    assert '依 2026-11-06 收盤' in text and '（上月 20.0%）' in text and '本週新進，先用等權' in text
    assert '空席 2：放現金 40%' in text and '下次調整：12 月第一個週六' in text
    html = env.html()
    assert html.count('>本月占比</th>') == 1 and '上次調整依 2026-11-06 收盤' in html
    head = html[html.index('① 核心席'):]
    row = head[head.index('<tr><td class="bw-l">C1</td>'):]
    row = row[:row.index('</tr>')]
    empty = head[head.index('<td class="bw-l">C4</td>'):]
    empty = empty[:empty.index('</tr>')]
    assert row.count('<td') == empty.count('<td')                       # 空席列也多一格

    # 同一天重跑（workflow retry）：不重抓、不再寫通知
    tw.build(True, today=date(2026, 11, 7))
    assert len(calls) == 1 and not alert.exists()

    # 平日：沿用、不寫通知
    alert.write_text('x', encoding='utf-8')
    tw.build(False, today=date(2026, 11, 9))
    assert len(calls) == 1 and alert.read_text(encoding='utf-8') == 'x'
