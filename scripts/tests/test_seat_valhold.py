"""估值偏貴現任續抱、不加碼（2026-11-05 持有人拍板，scripts/engine/seat_valhold.py）。
驗：估值紅的現任留席、估值紅的非現任不補席、倉位取較小值、大盤空頭紅燈照樣下席（多頭紅燈續抱照舊）、
已切換持股不受影響、生效日前逐位不變、美股看板／台股席位的三條線（實際新規則、舊規則對照、假設線）都套用。合成資料，不連網。"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_seats_tw as tw  # noqa: E402
from engine import build_arena as ba  # noqa: E402
from engine import seat_st as st  # noqa: E402
from engine import seat_tm  # noqa: E402
from engine import seat_valhold as vh  # noqa: E402
from test_build_seats_tw import _rev, _stock  # noqa: E402
from test_seat_st import daily_from_weekly  # noqa: E402
from test_seats_tw_x1 import BEAR, BULL, _inc, _rows, env  # noqa: E402,F401  (env＝端到端用的路徑沙盒)

US_BULL = {"mode": "tm", "status": "bull"}
US_BEAR = {"mode": "e1", "status": "bear"}


# ── 美股看板：合成列 ─────────────────────────────────────────────────────────

def _urow(t, code="green", size=1.0, *, ok_pass=True, val_red=False, cap_ok=True):
    """ok_pass＝除估值外的資格；val_red＝估值閘紅燈。pass＝ok_pass 且不是 val_red。"""
    g = {"pass": bool(ok_pass and not val_red), "pass_ex_valuation": bool(ok_pass), "veto_valuation": bool(val_red),
         "fundamental_pass": bool(ok_pass)}
    return {"ticker": t, "lamp": {"code": code, "size": size, "label": code, "why": ""}, "grp": g, "cap_ok": cap_ok}


def _us_pool(rows):
    return [r for r in rows if r["grp"]["pass"]]


def _us_rotation(rows, prev, market, *, on=True, status=None):
    """美股看板一次選席（與 build_arena.main 同一組函式：augment_pool → new_rule_rotation → select_roster）。"""
    pool = vh.augment_pool(_us_pool(rows), prev, rows, status, on)
    return st.new_rule_rotation(pool, prev, status or {}, rows,
                                lambda p, pv: seat_tm.select_roster(p, pv, market, ba.select_hold_roster))


def test_us_val_red_incumbent_keeps_the_seat():
    rows = [_urow("A"), _urow("B", val_red=True)]
    rot = _us_rotation(rows, ["A", "B"], US_BULL)
    assert rot["core"] == ["A", "B"] and rot["removed"] == []
    off = _us_rotation(rows, ["A", "B"], US_BULL, on=False)          # 生效日前：照舊，B 在週六被當成出池賣掉
    assert off["core"] == ["A"] and off["removed"] == [("B", "出池（資格不成立）")]


def test_us_val_red_non_incumbent_is_not_filled_into_an_empty_seat():
    rows = [_urow("A"), _urow("C", val_red=True), _urow("D")]
    rot = _us_rotation(rows, ["A"], US_BULL)
    assert "C" not in rot["core"] and rot["core"] == ["A", "D"]
    assert [t for _, t in rot["filled"]] == ["D"]


def test_us_other_failures_still_leave_the_pool():
    rows = [_urow("A"), _urow("B", ok_pass=False, val_red=True)]      # 估值紅，但品質／成長等也沒過
    rot = _us_rotation(rows, ["A", "B"], US_BULL)
    assert rot["core"] == ["A"] and rot["removed"] == [("B", "出池（資格不成立）")]
    capped_out = [_urow("A"), _urow("B", val_red=True, cap_ok=False)]  # 市值帶沒過也算資格不成立
    assert _us_rotation(capped_out, ["A", "B"], US_BULL)["core"] == ["A"]


def test_us_bear_market_red_lamp_still_drops_the_val_red_incumbent():
    rows = [_urow("A"), _urow("B", code="red", size=0.0, val_red=True)]
    rot = _us_rotation(rows, ["A", "B"], US_BEAR)
    assert rot["core"] == ["A"]
    assert rot["removed"][0][0] == "B" and "時機燈轉紅" in rot["removed"][0][1] and "出池" not in rot["removed"][0][1]


def test_us_bull_market_red_lamp_hold_exception_unchanged():
    rows = [_urow("B", code="red", size=0.0, val_red=True)]
    rot = _us_rotation(rows, ["B"], US_BULL)
    assert rot["core"] == ["B"] and rot["removed"] == []
    held = vh.held_set(rows, set(), {}, True)
    assert held == {"B"}
    # 大盤多頭續抱的顯示判定要把估值偏貴的現任算進池內，否則紅燈續抱的倉位不會沿用最近非紅燈倉位
    assert seat_tm.held_tickers(rows, held, US_BULL, ba.LIT_LAMP_CODES) == {"B"}
    assert seat_tm.held_tickers(rows, set(), US_BULL, ba.LIT_LAMP_CODES) == set()


def test_us_switched_holding_is_untouched_by_valhold():
    rows = [_urow("A"), _urow("B", val_red=True)]
    status = {"B": {"switched": True, "st_dir": "bull", "switch_week": "2026-11-06", "reason": "a"}}
    assert vh.augment_pool(_us_pool(rows), ["A", "B"], rows, status, True) == _us_pool(rows)   # 不補：已切換者另有路徑
    assert vh.held_set(rows, {"A"}, status, True) == set()
    on = _us_rotation(rows, ["A", "B"], US_BULL, status=status)
    off = _us_rotation(rows, ["A", "B"], US_BULL, on=False, status=status)
    assert on == off and on["core"] == ["A", "B"]                      # 折衷組本來就讓 B（基本面過）留席
    # 已切換者倉位不被 cap_rows 動到
    core = [dict(rows[1], lamp=dict(rows[1]["lamp"]))]
    vh.cap_rows(core, vh.held_set(rows, {"A"}, status, True), {"B": {"size": 0.5}})
    assert core[0]["lamp"]["size"] == 1.0 and "val_hold" not in core[0]


def test_us_before_cutover_is_bit_for_bit_the_same():
    rows = [_urow("A"), _urow("B", val_red=True), _urow("C", code="red", size=0.0)]
    pool = _us_pool(rows)
    assert vh.augment_pool(pool, ["A", "B"], rows, {}, vh.active("2026-11-06")) is pool
    assert vh.held_set(rows, {"A"}, {}, vh.active("2026-11-06")) == set()
    assert vh.active("2026-11-07") and not vh.active("2026-11-06") and not vh.active("—") and not vh.active(None)


# ── 倉位：取較小值、狀態檔 ───────────────────────────────────────────────────

def test_cap_rows_takes_the_smaller_size_and_labels_it():
    rows = [_urow("B", size=1.0, val_red=True), _urow("C", size=0.5, val_red=True), _urow("D", size=1.0, val_red=True)]
    logs = []
    vh.cap_rows(rows, {"B", "C", "D"}, {"B": {"size": 0.5}, "C": {"size": 1.0}}, log=logs.append)
    b, c, d = rows
    assert b["lamp"]["size"] == 0.5 and b["action"] == "半倉・不加碼" and b["val_hold"] and b["val_pre_size"] == 0.5
    assert c["lamp"]["size"] == 0.5 and "action" not in c              # 現行倉位本來就較小：不動，也不能因此加碼到 1.0
    assert d["lamp"]["size"] == 1.0 and d["val_hold"] and len(logs) == 1 and "D" in logs[0]   # 沒紀錄：本週不設上限
    assert vh.capped(0.5, {"size": 1.0}) == 0.5 and vh.capped(1.0, None) == 1.0 and vh.capped(None, {"size": 1.0}) is None


def test_next_pre_records_in_pool_names_keeps_red_ones_and_drops_leavers():
    prev = {"B": {"size": 0.5, "date": "2026-11-07"}, "Z": {"size": 1.0, "date": "2026-11-07"}}
    size = {"A": 1.0, "B": 1.0, "C": 0.5}
    new = vh.next_pre(prev, ["A", "B", "C"], {"B", "C"}, size.get, "2026-11-14")
    assert new["A"] == {"size": 1.0, "date": "2026-11-14"}
    assert new["B"] == prev["B"]                                        # 估值紅：保留轉紅前最後一次
    assert new["C"] == {"size": 0.5, "date": "2026-11-14", "fallback": True}   # 生效週就已紅：當週倉位當 fallback
    assert "Z" not in new


def test_state_file_round_trip(tmp_path):
    p = tmp_path / "s.json"
    assert vh.load_pre(p) == {"new": {}, "legacy": {}, "hypo": {}}
    vh.save_pre(p, {"new": {"A": {"size": 0.5, "date": "2026-11-14"}}}, "2026-11-14")
    assert vh.load_pre(p)["new"]["A"]["size"] == 0.5 and vh.load_pre(p)["hypo"] == {}


# ── 台股席位：select（實際新規則、舊規則對照、假設線都呼叫同一個 select） ────────────

def _tsel(stocks, market, prev, **kw):
    return tw.select(_rows(stocks), list(prev), True, market=market, **kw)


def _val(t='1000.TW', **kw):
    return _inc(t, dist=-1.0, vs200=5.0, rev=20, live_peg=3.0, **kw)


def test_tw_val_red_incumbent_keeps_the_seat_but_off_stays_the_old_rule():
    sel = _tsel([_val()], BULL, ['1000.TW'], valhold=True)
    assert [r['ticker'] for r in sel['core']] == ['1000.TW'] and sel['rotation']['removed'] == []
    assert [r['ticker'] for r in sel['too_expensive']] == ['1000.TW']
    off = _tsel([_val()], BULL, ['1000.TW'])
    assert off['core'] == [] and off['rotation']['removed'][0] == ('1000.TW', '出池（資格不成立）')


def test_tw_val_red_non_incumbent_is_not_filled():
    sel = _tsel([_val('2000.TW'), _inc('3000.TW', dist=-1.0, rev=15)], BULL, [], valhold=True)
    assert [r['ticker'] for r in sel['core']] == ['3000.TW']
    assert [t for _, t in sel['rotation']['filled']] == ['3000.TW']


def test_tw_bear_week_red_lamp_drops_it_and_bear_never_buys_new_names():
    red = _inc('1000.TW', dist=-15.0, vs200=5.0, rev=20, live_peg=3.0)
    sel = _tsel([red], BEAR, ['1000.TW'], valhold=True)
    assert sel['core'] == [] and sel['rotation']['removed'][0][0] == '1000.TW'
    assert '出池' not in sel['rotation']['removed'][0][1]
    lit = _tsel([_val(), _val('2000.TW')], BEAR, ['1000.TW'], valhold=True)   # 空頭：現任亮燈續抱，估值紅的非現任不補
    assert [r['ticker'] for r in lit['core']] == ['1000.TW']


def test_tw_bull_week_distance_red_hold_exception_still_applies():
    red = _inc('1000.TW', dist=-15.0, vs200=5.0, rev=20, live_peg=3.0)
    sel = _tsel([red], BULL, ['1000.TW'], valhold=True)
    assert [r['ticker'] for r in sel['core']] == ['1000.TW'] and sel['core'][0]['x1_hold'] is True


def test_tw_switched_incumbent_not_double_handled():
    status = {'1000.TW': {'switched': True, 'st_dir': 'bull', 'switch_week': '2026-11-06', 'reason': 'a'}}
    a = _tsel([_val()], BULL, ['1000.TW'], st_status=status, valhold=True)
    b = _tsel([_val()], BULL, ['1000.TW'], st_status=status)
    assert a['rotation'] == b['rotation'] and [r['ticker'] for r in a['core']] == ['1000.TW']


# ── 台股席位：端到端 build()，三條線都套用 ───────────────────────────────────────

def _hypo_seed():
    return {'schema': st.HYPO_SCHEMA, 'start': st.HYPO_START, 'roster': [], 'holdings': {}, 'events': [],
            'nav': {'series': [{'week': '2026-11-06', 'nav': 1.0}], 'asof': '2026-11-06', 'positions': {}},
            'decision_date': '2026-11-06', 'as_of': '2026-11-06'}


@pytest.fixture
def venv(env, tmp_path, monkeypatch):
    out = env.out_dir
    monkeypatch.setattr(tw, 'ST_NAV_JSON', out / 'seat_st_nav_tw.json')
    monkeypatch.setattr(tw, 'ST_STATE_JSON', out / 'seat_st_state_tw.json')
    monkeypatch.setattr(tw, 'ST_HYPO_JSON', out / 'seat_st_hypo_tw.json')
    monkeypatch.setattr(tw, 'ST_HYPO_SEED_JSON', tmp_path / 'seed.json')
    monkeypatch.setattr(tw, 'VALHOLD_JSON', out / 'seat_valhold_state_tw.json')
    (tmp_path / 'seed.json').write_text(json.dumps(_hypo_seed()), encoding='utf-8')
    flat = daily_from_weekly([100.0] * 80, start='2025-06-02')
    monkeypatch.setattr(tw.seat_st, 'make_loader', lambda: (lambda t: flat))   # 不連網：平盤價格，沒有持股會切換
    return env


def test_end_to_end_three_lines_all_apply_and_size_is_the_smaller_one(venv):
    env, out = venv, venv.out_dir
    closes = [100.0] * 259 + [110.0]
    # 週 1（11-13 資料）：1000 過熱橘燈 0.5，估值正常，入席；三條線都記下 0.5
    env.market(closes, date(2026, 11, 12))
    hot = _stock('1000.TW', dist_ath=-1.0, **_rev(20), ma={'above_w52': True, 'dist_ath_pct': -1.0, 'vs_200ma_pct': 5.0,
                                                          'price': 100, 'mom_12_1_pct': 200.0})
    env.pool_json([hot], '2026-11-13')
    tw.build(True, today=date(2026, 11, 14))
    pre = json.loads((out / 'seat_valhold_state_tw.json').read_text(encoding='utf-8'))['lines']
    assert pre['new']['1000.TW']['size'] == pre['legacy']['1000.TW']['size'] == pre['hypo']['1000.TW']['size'] == 0.5

    # 週 2（11-20 資料）：估值轉紅、燈號變綠（現行倉位 1.0）；另一檔估值紅的 2000 不是現任
    env.market(closes, date(2026, 11, 19))
    env.pool_json([_stock('1000.TW', dist_ath=-1.0, **_rev(20), live_peg=3.0),
                   _stock('2000.TW', dist_ath=-1.0, **_rev(20), live_peg=3.0)], '2026-11-20')
    tw.build(True, today=date(2026, 11, 21))
    d = json.loads((out / 'seats_tw.json').read_text(encoding='utf-8'))
    seat = d['core_seats'][0]
    assert [c['ticker'] for c in d['core_seats']] == ['1000.TW']                  # 實際新規則線：留席，2000 不補
    assert seat['lamp']['size'] == 0.5 and seat['val_hold'] is True and '估值偏貴・不加碼' in seat['seat_note']
    assert seat['action'] == '半倉・不加碼' and d['rotation']['removed'] == []
    ledger = json.loads((out / 'seats_tw_ledger.json').read_text(encoding='utf-8'))
    assert ledger['roster_legacy']['core'] == ['1000.TW']                          # 舊規則對照線也留席
    hypo = json.loads((out / 'seat_st_hypo_tw.json').read_text(encoding='utf-8'))
    assert hypo['roster'] == ['1000.TW']                                           # 假設線也留席、2000 不補
    assert hypo['nav']['positions']['1000.TW'] == 0.5                              # 假設線的倉位同樣取較小值
    nav = json.loads((out / 'seat_st_nav_tw.json').read_text(encoding='utf-8'))
    assert nav['holdings']['new']['1000.TW'] == 0.5 and nav['holdings']['legacy']['1000.TW'] == 0.5
    pre = json.loads((out / 'seat_valhold_state_tw.json').read_text(encoding='utf-8'))['lines']
    assert all(pre[k]['1000.TW']['size'] == 0.5 and 'fallback' not in pre[k]['1000.TW'] for k in ('new', 'legacy', 'hypo'))
    html = (out / '_seats_tw_body.html').read_text(encoding='utf-8')
    assert '估值偏貴・不加碼' in html and '已在席的不賣、不加碼，沒在席的不補' in html

    # 週 3：大盤翻空，現任又紅燈 → 照樣下席，三條線都下
    env.market([100.0] * 259 + [90.0], date(2026, 11, 26))
    env.pool_json([_stock('1000.TW', dist_ath=-15.0, **_rev(20), live_peg=3.0)], '2026-11-27')
    tw.build(True, today=date(2026, 11, 28))
    d = json.loads((out / 'seats_tw.json').read_text(encoding='utf-8'))
    assert d['core_seats'] == [] and d['rotation']['removed'][0]['ticker'] == '1000.TW'
    assert json.loads((out / 'seats_tw_ledger.json').read_text(encoding='utf-8'))['roster_legacy']['core'] == []
    assert json.loads((out / 'seat_st_hypo_tw.json').read_text(encoding='utf-8'))['roster'] == []


def test_end_to_end_before_cutover_nothing_changes(venv, monkeypatch):
    monkeypatch.setattr(vh, 'CUTOVER_DATE', '2099-01-01')
    env, out = venv, venv.out_dir
    env.market([100.0] * 259 + [110.0], date(2026, 11, 12))
    env.pool_json([_stock('1000.TW', dist_ath=-1.0, **_rev(20), live_peg=3.0)], '2026-11-13')
    tw.build(True, today=date(2026, 11, 14))
    d = json.loads((out / 'seats_tw.json').read_text(encoding='utf-8'))
    assert d['core_seats'] == []
    assert not (out / 'seat_valhold_state_tw.json').exists()


# ── 事後覆寫 pass 的兩處（實作漏接修正）：市值不足、yfinance 保守否決 ──────────────────

def test_cross_check_yfinance_veto_clears_pass_ex_valuation_and_fundamental_pass():
    g = {"pass": True, "pass_ex_valuation": True, "fundamental_pass": True, "veto": False, "why": [],
         "r_fy1": 5.0}
    r = ba.cross_check_r({"ticker": "A", "grp": g}, -12.0)
    assert r["grp"]["pass"] is False and r["grp"]["veto"] is True
    assert r["grp"]["pass_ex_valuation"] is False and r["grp"]["fundamental_pass"] is False
    assert g["pass_ex_valuation"] is True                              # 不改原 dict
    assert vh.is_val_hold(dict(r, cap_ok=True, grp=dict(r["grp"], veto_valuation=True))) is False


def _us_env(monkeypatch, tmp_path, stocks, caps=None, pre=None, spy=None):
    from test_arena_lamp_only import _patch_paths, _write_fixtures  # noqa: E402
    from test_arena_tm_v57 import _ledger, _spy_file  # noqa: E402
    paths = _patch_paths(monkeypatch, tmp_path)
    monkeypatch.setattr(ba, 'VALHOLD_JSON', tmp_path / 'seat_valhold_state.json')
    monkeypatch.setattr(vh, 'CUTOVER_DATE', '2026-09-01')
    if caps is not None:
        monkeypatch.setattr(ba, 'fetch_caps', lambda tickers, caps_=None: {t: caps.get(t, 5e10) for t in (tickers or [])})
    _write_fixtures(paths, stocks, as_of='2026-09-18', ledger=_ledger())
    _spy_file(paths['SPY_PRICES_JSON'], spy or ([100.0] * 199 + [101.0]))
    if pre is not None:
        (tmp_path / 'seat_valhold_state.json').write_text(
            json.dumps({'schema': vh.SCHEMA, 'lines': {'new': pre}}), encoding='utf-8')
    monkeypatch.setattr(sys, 'argv', ['build_arena.py', '--ledger'])
    assert ba.main() == 0
    return paths, json.loads(paths['ARENA_JSON'].read_text(encoding='utf-8'))


def _stocks_us(a_extra):
    from test_arena_lamp_only import _CORE5, _v5_stock  # noqa: E402
    return [_v5_stock(_CORE5[0], 20.0, **a_extra)] + [_v5_stock(t, 20.0) for t in _CORE5[1:]]


def test_us_end_to_end_val_red_incumbent_stays_with_capped_size(tmp_path, monkeypatch):
    paths, out = _us_env(monkeypatch, tmp_path, _stocks_us({'live_peg': 3.0}), pre={'PQRSA': {'size': 0.5, 'date': '2026-09-11'}})
    core = {r['ticker']: r for r in out['core_seats']}
    a = core['PQRSA']
    assert len(core) == 5 and a['val_hold'] is True and a['lamp']['size'] == 0.5
    assert '估值偏貴・不加碼' in a['seat_note'] and '出池' not in json.dumps(out['rotation'], ensure_ascii=False)
    assert 'val_hold' not in core['PQRSB']
    assert json.loads((tmp_path / 'seat_valhold_state.json').read_text(encoding='utf-8'))['lines']['new']['PQRSA']['size'] == 0.5


def test_us_end_to_end_cap_failed_incumbent_leaves_even_if_valuation_red_and_is_not_in_3b(tmp_path, monkeypatch):
    # 市值不足＋估值紅：下席（出池）；市值不足＋估值綠（OSCR 型）：不列 ③b
    paths, out = _us_env(monkeypatch, tmp_path, _stocks_us({'live_peg': 3.0}), caps={'PQRSA': 1e9})
    assert 'PQRSA' not in {r['ticker'] for r in out['core_seats']}
    assert any(x['ticker'] == 'PQRSA' for x in out['rotation']['removed'])
    board = paths['BOARD_TXT'].read_text(encoding='utf-8')
    assert '③b 太貴不入池（共 0 檔' in board
