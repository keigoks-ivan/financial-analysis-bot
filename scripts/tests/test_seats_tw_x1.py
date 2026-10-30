"""台股核心席 v5.4（2026-10-18 持有人破例決定）：看大盤切換出場（X1）。

規則照 v7-backtest docs/SeatExitSwitch_Prereg.md（e26888d）：決策日加權報酬指數收盤 < 自己的 200 日簡單均線
＝大盤空頭，其餘（含恰好相等）＝多頭。多頭時在席者只在「跌破自己的 200 日線」或資格不成立時下席，距新高
跌超過 10% 不下席；空頭時照現行紅燈下席。入場、排序不變。紅燈在席者的倉位沿用最近一次非紅燈的倉位（狀態檔）。
合成資料，不連網。
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_seats_tw as tw  # noqa: E402
from test_build_seats_tw import _rev, _stock  # noqa: E402

BULL = {'mode': 'x1', 'status': 'bull'}
BEAR = {'mode': 'e1', 'status': 'bear'}


# ── 大盤狀態判定 ──────────────────────────────────────────────────────────

def _series(closes, end=date(2026, 10, 16)):
    """closes 依序是最近 len(closes) 個平日（含 end）的收盤。"""
    days, d = [], end
    while len(days) < len(closes):
        if d.weekday() < 5:
            days.append(d)
        d -= timedelta(days=1)
    return list(zip(reversed(days), closes))


def test_exactly_equal_to_the_average_is_bull():
    st = tw.market_state(_series([100.0] * 200), date(2026, 10, 17))
    assert st['close'] == st['ma200'] == 100.0
    assert (st['status'], st['mode']) == ('bull', 'x1')


def test_strictly_below_the_average_is_bear_and_above_is_bull():
    below = tw.market_state(_series([100.0] * 199 + [99.0]), date(2026, 10, 17))
    assert (below['status'], below['mode']) == ('bear', 'e1')
    assert below['ma200'] == pytest.approx((199 * 100.0 + 99.0) / 200)
    above = tw.market_state(_series([100.0] * 199 + [101.0]), date(2026, 10, 17))
    assert (above['status'], above['mode']) == ('bull', 'x1')


def test_average_uses_exactly_the_last_200_rows():
    # 前面 50 列很大，第 51 列起才是 200 列：若誤用 250 列平均，收盤 100 會低於均線而判空頭
    series = _series([1000.0] * 50 + [100.0] * 200)
    st = tw.market_state(series, date(2026, 10, 17))
    assert st['ma200'] == 100.0 and st['status'] == 'bull'


def test_fewer_than_200_rows_counts_as_bull():
    st = tw.market_state(_series([100.0] * 150 + [1.0]), date(2026, 10, 17))
    assert st['ma200'] is None and (st['status'], st['mode']) == ('bull', 'x1')


def test_state_never_peeks_past_the_decision_day():
    series = _series([100.0] * 199 + [110.0, 50.0])         # 最後一列（10-16）暴跌，決策日 10-15
    st = tw.market_state(series, date(2026, 10, 15))
    assert st['data_date'] == '2026-10-15' and st['close'] == 110.0 and st['status'] == 'bull'
    assert tw.market_state(series, date(2026, 10, 16))['status'] == 'bear'


def test_decision_day_on_a_saturday_uses_friday_close():
    st = tw.market_state(_series([100.0] * 200), date(2026, 10, 17))
    assert st['data_date'] == '2026-10-16' and st['decision_date'] == '2026-10-17'


def test_stale_data_falls_back_to_current_exit():
    series = _series([100.0] * 200, end=date(2026, 10, 9))
    ok = tw.market_state(series, date(2026, 10, 16))        # 剛好 7 天，不算舊
    assert ok['status'] == 'bull' and ok['mode'] == 'x1'
    old = tw.market_state(series, date(2026, 10, 17))       # 8 天
    assert (old['status'], old['mode']) == ('stale', 'e1') and old['data_date'] == '2026-10-09'


def test_no_data_before_the_decision_day_is_missing():
    assert tw.market_state([], date(2026, 10, 17))['status'] == 'missing'
    series = _series([100.0] * 200, end=date(2026, 10, 16))
    assert tw.market_state(series, date(2020, 1, 1))['mode'] == 'e1'


def test_load_market_series_reads_and_skips_bad_rows(tmp_path):
    f = tmp_path / 'tri.csv'
    f.write_text('date,value\n2026-10-15,100.5\nbad,1\n2026-10-14,99.5\n2026-10-16,\n', encoding='utf-8')
    assert tw.load_market_series(f) == [(date(2026, 10, 14), 99.5), (date(2026, 10, 15), 100.5)]
    assert tw.load_market_series(tmp_path / 'nope.csv') == []


def test_matches_pandas_rolling_mean_on_the_real_series():
    """與回測的算法（pandas rolling(200).mean()，收盤 < 均線）在真實資料上逐日一致。"""
    pd = pytest.importorskip('pandas')
    series = tw.load_market_series()
    if len(series) < 400:
        pytest.skip('tw.twse_tri.csv not available')
    s = pd.Series([v for _, v in series], index=[d for d, _ in series])
    ma = s.rolling(200, min_periods=200).mean()
    for i in range(250, len(series), 37):
        d = series[i][0]
        st = tw.market_state(series, d)
        assert st['data_date'] == d.isoformat()
        assert st['ma200'] == pytest.approx(ma.iloc[i], rel=1e-12)
        assert (st['status'] == 'bear') == bool(s.iloc[i] < ma.iloc[i])


def test_real_series_decision_day_2026_10_17_is_bull():
    series = tw.load_market_series()
    if not series or series[-1][0] < date(2026, 10, 16):
        pytest.skip('tw.twse_tri.csv not available')
    st = tw.market_state(series, date(2026, 10, 17))
    assert (st['data_date'], st['status']) == ('2026-10-16', 'bull')
    assert st['close'] == 108938.83 and round(st['ma200'], 2) == 91579.51


# ── 選席：大盤多頭時距新高跌超過 10% 不下席 ─────────────────────────────────

def _rows(stocks):
    return [tw.tw_row(s) for s in stocks]


def _inc(ticker='1000.TW', dist=-15.0, vs200=5.0, rev=20, **extra):
    # grp.timing_lamp 讀 timing.vs_200ma_pct（_stock 的 vs200 只放進 ma），所以 timing 明確帶進去
    return _stock(ticker, dist_ath=dist, vs200=vs200, timing={'dist_52w_high_pct': dist, 'vs_200ma_pct': vs200},
                  **_rev(rev), **extra)


def _sel(stocks, market, prev=('1000.TW',)):
    return tw.select(_rows(stocks), list(prev), True, market=market)


def test_bull_keeps_incumbent_that_is_red_only_by_distance():
    sel = _sel([_inc()], BULL)
    assert [r['ticker'] for r in sel['core']] == ['1000.TW']
    r = sel['core'][0]
    assert r['x1_hold'] is True and r['seat_note'] == '現任・大盤多頭續抱'
    assert sel['rotation']['removed'] == []


def test_bull_removes_incumbent_below_its_own_200_day_line():
    sel = _sel([_inc(vs200=-2.0)], BULL)
    assert sel['core'] == []
    assert [t for t, _ in sel['rotation']['removed']] == ['1000.TW']


def test_bear_removes_the_same_incumbent_like_the_current_rule():
    sel = _sel([_inc()], BEAR)
    assert sel['core'] == []
    assert sel['rotation']['removed'] == [('1000.TW', '時機燈轉紅（距新高 <−10% 或跌破 200 日線）')]


def test_flip_week_bull_to_bear_drops_all_distance_reds_together():
    stocks = lambda: [_inc('1000.TW'), _inc('2000.TW', rev=15), _stock('3000.TW', **_rev(10))]  # noqa: E731
    prev = ('1000.TW', '2000.TW', '3000.TW')
    bull = _sel(stocks(), BULL, prev)
    assert {r['ticker'] for r in bull['core']} == {'1000.TW', '2000.TW', '3000.TW'}
    bear = _sel(stocks(), BEAR, prev)
    assert [r['ticker'] for r in bear['core']] == ['3000.TW']
    assert {t for t, _ in bear['rotation']['removed']} == {'1000.TW', '2000.TW'}


def test_bull_does_not_let_a_non_incumbent_red_name_in():
    sel = _sel([_inc('1000.TW'), _inc('2000.TW', rev=30)], BULL, prev=('1000.TW',))
    assert [r['ticker'] for r in sel['core']] == ['1000.TW']            # 2000 紅燈、沒坐席：不入席
    assert [r['ticker'] for r in sel['waiting_rest']] == ['2000.TW']


def test_bull_incumbent_out_of_the_pool_still_leaves():
    sel = _sel([_inc(cagr=5.0)], BULL)                                  # 三年成長掉到 15% 以下＝資格不成立（v5.7 起上修不再是門檻）
    assert sel['core'] == []
    assert [t for t, _ in sel['rotation']['removed']] == ['1000.TW']


def test_held_incumbent_is_not_displaced_by_better_ranked_names():
    # v5.11（2026-10-30）：現任抱著，池內有 5 檔上修更高的亮燈名字也不擠掉現任
    lit = [_stock(f'{2000 + i}.TW', **_rev(40 - i)) for i in range(5)]
    sel = _sel([_inc(rev=10)] + lit, BULL)
    assert '1000.TW' in [r['ticker'] for r in sel['core']]
    assert sel['rotation']['removed'] == []


def test_no_market_or_stale_market_is_identical_to_v53():
    # v5.6 起大盤空頭週不補新席（見 test_seats_tw_bear_no_buy.py）；資料太舊退回現行賣法、照常補位，與 v5.3 相同
    stocks = lambda: [_inc('1000.TW'), _stock('2000.TW', **_rev(30)), _inc('3000.TW', rev=25, vs200=-3.0)]  # noqa: E731
    prev = ('1000.TW', '3000.TW')
    a = tw.select(_rows(stocks()), list(prev), True)
    b = tw.select(_rows(stocks()), list(prev), True, market={'mode': 'e1', 'status': 'stale'})
    assert [r['ticker'] for r in a['core']] == [r['ticker'] for r in b['core']] == ['2000.TW']
    assert a['rotation'] == b['rotation']


def test_daily_run_marks_distance_red_seat_as_held_in_bull_only():
    last = {'date': '2026-10-16', 'core': ['1000.TW', '2000.TW'], 'removed': [], 'filled': []}
    stocks = [_inc('1000.TW'), _inc('2000.TW', rev=15, vs200=-1.0)]
    sel = tw.select(_rows(stocks), ['1000.TW', '2000.TW'], False, last_snap=last, market=BULL)
    notes = {r['ticker']: (r['x1_hold'], r['seat_note']) for r in sel['core']}
    assert notes == {'1000.TW': (True, '現任・大盤多頭續抱'), '2000.TW': (False, '現任・週中轉紅，週六複判')}
    sel = tw.select(_rows(stocks), ['1000.TW', '2000.TW'], False, last_snap=last, market=BEAR)
    assert all(not r['x1_hold'] and '週中轉紅' in r['seat_note'] for r in sel['core'])


# ── 倉位：沿用最近一次非紅燈的倉位 ─────────────────────────────────────────

def test_update_state_records_only_lit_names_with_distance_data():
    rows = _rows([_stock('1000.TW'), _stock('2000.TW', dist_ath=-15.0), _stock('3000.TW', dist_ath=None)])
    for r in rows:
        r['x1_hold'] = False
    old = {'2000.TW': {'size': 0.5, 'code': 'hot', 'date': '2026-10-09'},
           '9999.TW': {'size': 1.0, 'code': 'green', 'date': '2026-10-09'}}
    new = tw.update_state(old, rows, '2026-10-16')
    assert new['1000.TW'] == {'size': 1.0, 'code': 'green', 'date': '2026-10-16'}
    assert new['2000.TW'] == old['2000.TW']                              # 紅燈：保留舊值
    assert '3000.TW' not in new                                          # 距新高缺：不更新、也沒有舊值
    assert '9999.TW' not in new                                          # 已離席：丟掉


def test_apply_x1_hold_uses_state_size_and_defaults_to_one_with_a_log_line():
    sel = _sel([_inc('1000.TW'), _inc('2000.TW', rev=15)], BULL, prev=('1000.TW', '2000.TW'))
    logs = []
    tw.apply_x1_hold(sel, {'1000.TW': {'size': 0.5}}, log=logs.append)
    by = {r['ticker']: r for r in sel['core']}
    assert (by['1000.TW']['lamp']['size'], by['1000.TW']['action']) == (0.5, '半倉・續抱')
    assert (by['2000.TW']['lamp']['size'], by['2000.TW']['action']) == (1.0, '正常倉・續抱')
    assert by['1000.TW']['lamp']['code'] == 'red' and by['1000.TW']['lamp']['label'] == '🔴 續抱'
    assert len(logs) == 1 and '2000.TW' in logs[0] and '1.0' in logs[0]


# ── build()：端到端 ─────────────────────────────────────────────────────

@pytest.fixture
def env(tmp_path, monkeypatch):
    out = tmp_path / 'out'
    monkeypatch.setattr(tw, 'TW_POOL_JSON', tmp_path / 'latest.json')
    monkeypatch.setattr(tw, 'LAMP_TW_JSON', tmp_path / 'lamp_tw.json')
    monkeypatch.setattr(tw, 'OUT_DIR', out)
    monkeypatch.setattr(tw, 'BODY_HTML', out / '_seats_tw_body.html')
    monkeypatch.setattr(tw, 'SEATS_JSON', out / 'seats_tw.json')
    monkeypatch.setattr(tw, 'LEDGER_JSON', out / 'seats_tw_ledger.json')
    monkeypatch.setattr(tw, 'MARKET_CSV', tmp_path / 'tri.csv')

    class E:
        pool, csv, out_dir = tmp_path / 'latest.json', tmp_path / 'tri.csv', out

        @staticmethod
        def pool_json(stocks, as_of):
            E.pool.write_text(json.dumps({'as_of': as_of, 'stocks': stocks}), encoding='utf-8')

        @staticmethod
        def market(closes, end):
            rows = ['date,value'] + [f'{d.isoformat()},{v}' for d, v in _series(closes, end=end)]
            E.csv.write_text('\n'.join(rows) + '\n', encoding='utf-8')

        @staticmethod
        def seats():
            return json.loads((out / 'seats_tw.json').read_text(encoding='utf-8'))

        @staticmethod
        def state():
            p = out / tw.STATE_NAME
            return json.loads(p.read_text(encoding='utf-8'))['last_nonred'] if p.exists() else None

        @staticmethod
        def html():
            return (out / '_seats_tw_body.html').read_text(encoding='utf-8')
    return E


BULL_CLOSES = [100.0] * 259 + [110.0]
BEAR_CLOSES = [100.0] * 259 + [90.0]


def test_end_to_end_hold_through_distance_red_then_bear_week_drops_it(env):
    # 週 0（10-09）：亮燈過熱（橘，0.5）入席，狀態檔記 0.5
    env.market(BULL_CLOSES, date(2026, 10, 8))
    env.pool_json([_stock('1000.TW', dist_ath=-1.0, **_rev(20), **{'ma': {
        'above_w52': True, 'dist_ath_pct': -1.0, 'vs_200ma_pct': 5.0, 'price': 100, 'mom_12_1_pct': 200.0}})],
        '2026-10-09')
    tw.build(True, today=date(2026, 10, 10))
    assert [c['ticker'] for c in env.seats()['core_seats']] == ['1000.TW']
    assert env.state()['1000.TW']['size'] == 0.5 and env.state()['1000.TW']['code'] == 'hot'

    # 週 1（10-16）：大盤多頭、距新高 −15% 但站上 200 日線 → 留任、續抱、倉位沿用 0.5
    env.market(BULL_CLOSES, date(2026, 10, 15))
    env.pool_json([_inc('1000.TW', dist=-15.0)], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    d = env.seats()
    seat = d['core_seats'][0]
    assert d['market']['status'] == 'bull' and d['market']['data_date'] == '2026-10-15'
    assert seat['ticker'] == '1000.TW' and seat['x1_hold'] is True
    assert seat['lamp']['size'] == 0.5 and seat['action'] == '半倉・續抱'
    assert env.state()['1000.TW']['size'] == 0.5                         # 紅燈日不改狀態
    assert '大盤多頭續抱' in env.html() and '本週用「跌破自己的 200 日線才賣」' in env.html()

    # 週 2（10-23）：大盤翻空 → 同一檔照現行紅燈下席
    env.market(BEAR_CLOSES, date(2026, 10, 22))
    env.pool_json([_inc('1000.TW', dist=-15.0)], '2026-10-23')
    tw.build(True, today=date(2026, 10, 24))
    d = env.seats()
    assert d['market']['status'] == 'bear' and d['core_seats'] == []
    snap = json.loads((env.out_dir / 'seats_tw_ledger.json').read_text(encoding='utf-8'))['snapshots'][-1]
    assert snap['core'] == [] and snap['removed'][0][0] == '1000.TW'
    assert env.state() == {}                                             # 離席者的紀錄丟掉
    assert '本週用「時機燈轉紅就賣」' in env.html()


def _seat_one(env, hot=False):
    env.market(BULL_CLOSES, date(2026, 10, 8))
    s = _stock('1000.TW', dist_ath=-1.0, **_rev(20))
    env.pool_json([s], '2026-10-09')
    tw.build(True, today=date(2026, 10, 10))


def test_daily_run_keeps_the_roster_and_uses_the_last_saturday_decision_state(env):
    _seat_one(env)
    # 週六 10-16：多頭，席位紅燈續抱
    env.market(BULL_CLOSES, date(2026, 10, 15))
    env.pool_json([_inc('1000.TW', dist=-15.0)], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    # 週二 10-20 的日跑：指數 10-19 已經暴跌到 200 日線下，但賣法仍看上週六的決策日（10-15 收盤，多頭）
    rows = ['date,value'] + [f'{d.isoformat()},{v}' for d, v in _series(BULL_CLOSES, end=date(2026, 10, 15))]
    rows.append('2026-10-19,50')
    env.csv.write_text('\n'.join(rows) + '\n', encoding='utf-8')
    env.pool_json([_inc('1000.TW', dist=-16.0)], '2026-10-20')
    tw.build(False, today=date(2026, 10, 20))
    d = env.seats()
    assert d['market']['status'] == 'bull' and d['market']['data_date'] == '2026-10-15'
    assert d['core_seats'][0]['x1_hold'] is True and d['core_seats'][0]['lamp']['size'] == 1.0


def test_missing_state_entry_defaults_to_one_and_logs(env, capsys):
    _seat_one(env)
    (env.out_dir / tw.STATE_NAME).unlink()
    env.market(BULL_CLOSES, date(2026, 10, 15))
    env.pool_json([_inc('1000.TW', dist=-15.0)], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    assert env.seats()['core_seats'][0]['lamp']['size'] == 1.0
    assert '1000.TW 狀態檔沒有最近非紅燈倉位' in capsys.readouterr().out


def test_stale_market_data_falls_back_to_current_exit_and_says_so(env):
    _seat_one(env)
    env.market(BULL_CLOSES, date(2026, 10, 1))                           # 最近一筆 10-01，比決策日 10-16 早 15 天
    env.pool_json([_inc('1000.TW', dist=-15.0)], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    d = env.seats()
    assert d['market']['status'] == 'stale' and d['core_seats'] == []
    assert '大盤資料未更新，本週照空頭處理' in env.html()
    assert env.state() == {}


def test_missing_market_file_also_falls_back(env):
    _seat_one(env)
    env.csv.unlink()
    env.pool_json([_inc('1000.TW', dist=-15.0)], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    assert env.seats()['market']['status'] == 'missing' and env.seats()['core_seats'] == []
    assert '大盤資料未更新，本週照空頭處理' in env.html()


def test_reselect_retry_is_idempotent_with_x1(env):
    _seat_one(env)
    env.market(BULL_CLOSES, date(2026, 10, 15))
    env.pool_json([_inc('1000.TW', dist=-15.0)], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    ledger1 = (env.out_dir / 'seats_tw_ledger.json').read_text(encoding='utf-8')
    state1, seats1 = env.state(), env.seats()['core_seats']
    tw.build(True, today=date(2026, 10, 17))
    assert (env.out_dir / 'seats_tw_ledger.json').read_text(encoding='utf-8') == ledger1
    assert env.state() == state1 and env.seats()['core_seats'] == seats1


def test_daily_run_does_not_write_the_ledger_but_does_write_state(env):
    env.market(BULL_CLOSES, date(2026, 10, 15))
    env.pool_json([_stock('1000.TW', **_rev(20))], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    ledger = (env.out_dir / 'seats_tw_ledger.json').read_text(encoding='utf-8')
    env.pool_json([_stock('1000.TW', dist_ath=-7.0, **_rev(20))], '2026-10-20')   # 黃燈 1.0
    tw.build(False, today=date(2026, 10, 20))
    assert (env.out_dir / 'seats_tw_ledger.json').read_text(encoding='utf-8') == ledger
    assert env.state()['1000.TW'] == {'size': 1.0, 'code': 'yellow', 'date': '2026-10-20'}


# ── 頁面文字 ─────────────────────────────────────────────────────────────

def test_page_shows_rule_and_state_line_without_changelog(env):
    env.market(BULL_CLOSES, date(2026, 10, 15))
    env.pool_json([_stock('1111.TW')], '2026-10-16')
    tw.build(False, today=date(2026, 10, 17))
    html = env.html()
    assert ('大盤多頭（加權報酬指數在 200 日線之上）時，在席者離歷史新高再遠也續抱，跌破自己的 200 日線才賣；'
            '大盤空頭時，時機燈轉紅就賣（距歷史新高超過 10% 或跌破 200 日線）。') in html
    assert '大盤狀態（2026-10-15 收盤）：加權報酬指數 110.00，200 日線 100.05，<b>多頭</b>' in html
    assert '大盤多頭續抱' in html and '倉位沿用最近一次非紅燈的倉位' in html
    assert '變更紀錄' not in html and '現行賣法' not in html
    assert '台股核心席 · 資料日' in html and '台股核心席 v5' not in html


def test_page_bear_and_stale_lines():
    bull = tw._market_html({'status': 'bull', 'data_date': '2026-10-16', 'close': 108938.83, 'ma200': 91579.5071})
    assert '加權報酬指數 108,938.83，200 日線 91,579.51，<b>多頭</b>' in bull
    bear = tw._market_html({'status': 'bear', 'data_date': '2026-10-16', 'close': 90.0, 'ma200': 100.0})
    assert '<b>空頭</b>' in bear and '本週用「時機燈轉紅就賣」' in bear
    stale = tw._market_html({'status': 'stale', 'data_date': '2026-10-01', 'close': 1.0, 'ma200': None})
    assert '大盤資料未更新，本週照空頭處理，用「時機燈轉紅就賣」' in stale and '2026-10-01' in stale
    assert '大盤資料未更新，本週照空頭處理' in tw._market_html({'status': 'missing', 'data_date': None})


def test_new_page_text_uses_fullwidth_punctuation_after_chinese():
    legend = tw._legend()
    for text in (legend, tw.RULE_LINE, tw._market_html({'status': 'bull', 'data_date': '2026-10-16',
                                                         'close': 1.0, 'ma200': 1.0})):
        assert not re.search(r'[一-鿿][,.:;]', text), text
