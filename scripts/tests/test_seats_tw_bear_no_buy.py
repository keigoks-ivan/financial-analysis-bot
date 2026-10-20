"""台股核心席 v5.6（2026-10-21 持有人破例決定）：大盤跌破 200 日線不買新股（SeatEntryGate N）。

規則照 v7-backtest docs/SeatEntryGate_Prereg.md（fafc772）第三節：大盤空頭的決策週不買任何新股票，空席留空放現金；
已持有的照原出場規則賣（空頭週＝時機燈轉紅就賣），不因大盤空頭強制賣；大盤回到多頭的下一個決策週恢復遞補。
即時頁的排序擠出要買新名字，所以空頭週在席者不會被擠出。資料太舊或缺的週不擋買進。合成資料，不連網。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_seats_tw as tw  # noqa: E402
from test_build_seats_tw import _rev, _stock  # noqa: E402
from test_seats_tw_x1 import BEAR, BULL, _inc, _rows  # noqa: E402

STALE = {'mode': 'e1', 'status': 'stale'}


def _core(sel):
    return [r['ticker'] for r in sel['core']]


def test_bear_week_adds_no_new_name_and_leaves_the_seat_empty():
    stocks = [_stock('1000.TW', **_rev(10)), _stock('2000.TW', **_rev(30))]
    sel = tw.select(_rows(stocks), ['1000.TW'], True, market=BEAR)
    assert _core(sel) == ['1000.TW']
    assert sel['rotation']['filled'] == [] and sel['rotation']['blocked'] == ['2000.TW']
    assert [r['ticker'] for r in sel['buyable']] == ['2000.TW']          # 仍列在可買，只是本週不補


def test_bull_week_fills_the_same_name():
    stocks = [_stock('1000.TW', **_rev(10)), _stock('2000.TW', **_rev(30))]
    sel = tw.select(_rows(stocks), ['1000.TW'], True, market=BULL)
    assert _core(sel) == ['2000.TW', '1000.TW'] and sel['rotation']['filled'] == [('core', '2000.TW')]
    assert not sel['rotation'].get('blocked')


def test_bear_week_red_incumbent_still_leaves_and_its_seat_stays_empty():
    stocks = [_inc('1000.TW'), _stock('2000.TW', **_rev(30))]           # 1000 距新高 −15%：紅燈
    sel = tw.select(_rows(stocks), ['1000.TW'], True, market=BEAR)
    assert sel['core'] == []
    assert sel['rotation']['removed'] == [('1000.TW', '時機燈轉紅（距新高 <−10% 或跌破 200 日線）')]
    assert sel['rotation']['blocked'] == ['2000.TW']


def test_bear_week_incumbent_is_not_pushed_out_by_rank():
    lit = [_stock(f'{2000 + i}.TW', **_rev(40 - i)) for i in range(5)]  # 5 檔亮燈、上修都比 1000 高
    sel = tw.select(_rows([_stock('1000.TW', **_rev(10))] + lit), ['1000.TW'], True, market=BEAR)
    assert _core(sel) == ['1000.TW'] and sel['rotation']['removed'] == []
    assert sel['rotation']['blocked'] == ['2000.TW', '2001.TW', '2002.TW', '2003.TW', '2004.TW']


def test_bear_week_incumbent_out_of_the_pool_still_leaves():
    sel = tw.select(_rows([_stock('1000.TW', **_rev(3.0))]), ['1000.TW'], True, market=BEAR)
    assert sel['core'] == [] and [t for t, _ in sel['rotation']['removed']] == ['1000.TW']


def test_stale_or_missing_market_data_does_not_block_buying():
    stocks = lambda: [_stock('1000.TW', **_rev(10)), _stock('2000.TW', **_rev(30))]  # noqa: E731
    for m in (STALE, {'mode': 'e1', 'status': 'missing'}, None):
        sel = tw.select(_rows(stocks()), ['1000.TW'], True, market=m)
        assert _core(sel) == ['2000.TW', '1000.TW'], m


def test_daily_run_carries_the_blocked_names_from_the_saturday_snapshot():
    last = {'date': '2026-10-16', 'core': ['1000.TW'], 'removed': [], 'filled': [], 'blocked': ['2000.TW']}
    stocks = [_stock('1000.TW', **_rev(10)), _stock('2000.TW', **_rev(30))]
    sel = tw.select(_rows(stocks), ['1000.TW'], False, last_snap=last, market=BEAR)
    assert _core(sel) == ['1000.TW'] and sel['rotation']['blocked'] == ['2000.TW']


def test_page_lines_for_bear_week():
    bear = tw._market_html({'status': 'bear', 'data_date': '2026-10-16', 'close': 90.0, 'ma200': 100.0})
    assert '<b>補位</b>：大盤空頭的週六不補新席，空席放現金；大盤回到多頭的下一個週六照常補。' in bear
    assert '本週用「時機燈轉紅就賣」，不補新席。' in bear
    stale = tw._market_html({'status': 'stale', 'data_date': '2026-10-01', 'close': 1.0, 'ma200': None})
    assert '新席照常補' in stale
    for text in (tw.BUY_LINE, bear, stale):
        assert not re.search(r'[一-鿿][,.:;]', text), text
