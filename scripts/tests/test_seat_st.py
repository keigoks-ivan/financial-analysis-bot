"""席位出場折衷組（2026-11-05，scripts/engine/seat_st.py）：盤整突破 8 週、停損線高過買進價、切換後不切回、
已切換者不吃紅燈與 200 日線、出池仍會賣、沒切換的照舊、切換永遠不成立時與現行逐位相同。合成資料，不連網。"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_seats_tw as tw  # noqa: E402
from engine import build_arena as ba  # noqa: E402
from engine import seat_st as st  # noqa: E402
from engine import seat_tm  # noqa: E402
from test_build_seats_tw import _rev, _stock  # noqa: E402
from test_seats_tw_x1 import BEAR, BULL, _inc, _rows  # noqa: E402


# ── 合成日線：每週 5 個平日，週內價格相同 ──────────────────────────────────

def daily_from_weekly(closes, start="2024-01-01"):
    idx = pd.bdate_range(start, periods=len(closes) * 5)
    c = np.repeat(np.asarray(closes, float), 5)
    return pd.DataFrame({"high": c * 1.01, "low": c * 0.99, "close": c}, index=idx)


def weekly_label(daily, k):
    return daily.resample("W-FRI").close.last().index[k]


RISING = [100 + 2 * i for i in range(60)]                      # 一路創高，每週都是新高，離上次新高只差 1 週
DECISION = "2099-01-01"                                         # 遠在未來：所有週都算已收完


# ── 盤整突破：離上次創新高至少 8 週 ────────────────────────────────────────

def test_breakout_exactly_eight_weeks_is_true_and_seven_is_false():
    eight = [1, 2, 3] + [2.5] * 7 + [3.1]
    assert st.breakout_weeks(eight)[10]
    seven = [1, 2, 3] + [2.5] * 6 + [3.1]
    assert not st.breakout_weeks(seven)[9]


def test_breakout_needs_to_exceed_all_prior_closes_and_a_prior_high():
    c = [5, 4, 3, 3, 3, 3, 3, 3, 3, 4.9]                         # 沒超過 5
    assert not st.breakout_weeks(c).any()
    assert not st.breakout_weeks([1.0]).any()                    # 剛上市沒有上一次新高
    # 連續創高（gap=1）不算盤整突破
    assert not st.breakout_weeks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]).any()


def test_entry_week_label():
    f = lambda d: str(st.entry_week_label(d).date())  # noqa: E731
    assert f("2026-10-31") == "2026-10-30"                       # 週六 → 剛過去的週五
    assert f("2026-10-30") == "2026-10-30"
    assert f("2026-10-28") == "2026-10-30"                       # 週三 → 當週五
    assert f("2026-11-01") == "2026-10-30"


# ── 停損線條件 (b)、盤整突破 (a)、一旦切換不切回 ─────────────────────────────

def test_stop_line_above_entry_price_switches_the_week_after_entry():
    d = daily_from_weekly(RISING)
    entry_date = weekly_label(d, 30)
    r = st.evaluate_holding(d, entry_date, DECISION, entry_price=50.0)   # 買進價遠低於停損線
    assert r["data_ok"] and r["switched"] and r["reason"] == "b"
    assert r["switch_week"] == str(weekly_label(d, 31).date())          # (b) 只從買進之後的週算
    assert r["st_dir"] == "bull" and r["st_line"] is not None


def test_stop_line_below_entry_price_does_not_switch():
    d = daily_from_weekly(RISING)
    r = st.evaluate_holding(d, weekly_label(d, 30), DECISION, entry_price=10_000.0)
    assert r["data_ok"] and not r["switched"]


def test_default_entry_price_is_adjusted_close_on_entry_day():
    d = daily_from_weekly(RISING)
    ed = weekly_label(d, 30)
    r = st.evaluate_holding(d, ed, DECISION)
    assert r["entry_price"] == pytest.approx(RISING[30])


def test_breakout_week_switches_and_entry_week_counts():
    closes = list(range(100, 120)) + [105] * 12 + [125] + [126]  # 週 19 創高，其後 12 週整理，週 32 盤整突破
    d = daily_from_weekly(closes + [127] * 20)
    ed = weekly_label(d, 32)                                    # 進場那週就是突破週：含進場週
    r = st.evaluate_holding(d, ed, DECISION, entry_price=1e9)   # 停損線條件不可能成立，只看 (a)
    assert r["switched"] and r["reason"] == "a"
    assert r["switch_week"] == str(weekly_label(d, 32).date())
    after = st.evaluate_holding(d, weekly_label(d, 33), DECISION, entry_price=1e9)   # 突破發生在進場之前：不算
    assert not after["switched"]


def test_once_switched_never_switches_back():
    comp = {"data_ok": True, "switched": False, "switch_week": None, "reason": None, "st_dir": "bull",
            "st_line": 90.0, "entry_price": 100.0}
    prev = {"switched": True, "switch_week": "2026-11-06", "switch_reason": "a", "entry_price": 99.0}
    out = st.merge_sticky(comp, prev)
    assert out["switched"] and out["switch_week"] == "2026-11-06" and out["reason"] == "a"
    assert not st.merge_sticky(comp, {"switched": False})["switched"]


def test_force_no_switch_flag_blocks_every_switch(monkeypatch):
    monkeypatch.setattr(st, "FORCE_NO_SWITCH", True)
    d = daily_from_weekly(RISING)
    assert not st.evaluate_holding(d, weekly_label(d, 30), DECISION, entry_price=50.0)["switched"]


def test_only_completed_weeks_are_used():
    d = daily_from_weekly(RISING)
    wk = weekly_label(d, 40)
    wb = st.weekly_bars(d, wk - pd.Timedelta(days=2))            # 決策日在週三：該週還沒收完
    assert wb.index[-1] < wk


# ── 帳本快照 → 買進日 ───────────────────────────────────────────────────────

def test_entry_dates_from_contiguous_snapshot_run():
    snaps = [{"date": "2026-10-03", "core": ["A", "B"]}, {"date": "2026-10-10", "core": ["B"]},
             {"date": "2026-10-17", "core": ["A", "B"]}, {"date": "2026-10-24", "core": ["A", "B"]}]
    out = st.entry_dates(["A", "B", "C"], snaps, {"B": {"entry_date": "2026-09-01"}}, "2026-10-31")
    assert out["A"][0] == "2026-10-17"                           # 10-10 掉出後 10-17 重新進席
    assert out["B"][0] == "2026-09-01"                           # 狀態檔優先
    assert out["C"][0] == "2026-10-31"                           # 本次新進席


# ── 選席：美股看板 ───────────────────────────────────────────────────────────

def _row(t, code="green", size=1.0):
    return {"ticker": t, "lamp": {"code": code, "size": size, "label": code, "why": ""}}


def _status(**kw):
    base = {"switched": True, "st_dir": "bull", "switch_week": "2026-11-06", "reason": "a"}
    base.update(kw)
    return base


def _roster(pool, prev, status, market):
    pool2, prev2, removed = st.apply_overlay(pool, prev, status)
    rot = seat_tm.select_roster(pool2, prev2, market, ba.select_hold_roster)
    rot["removed"] = list(rot["removed"]) + removed
    return rot


BEAR_US = {"mode": "e1", "status": "bear"}
BULL_US = {"mode": "tm", "status": "bull"}


def test_switched_incumbent_ignores_red_lamp_even_in_bear_market():
    pool = [_row("A", "red"), _row("B", "green")]
    rot = _roster(pool, ["A", "B"], {"A": _status()}, BEAR_US)
    assert rot["core"] == ["A", "B"] and rot["removed"] == []


def test_unswitched_incumbent_keeps_current_rule_in_bear_market():
    pool = [_row("A", "red"), _row("B", "green")]
    rot = _roster(pool, ["A", "B"], {"A": _status(switched=False)}, BEAR_US)
    assert rot["core"] == ["B"]
    assert rot["removed"] == [("A", "時機燈轉紅（距新高 <−10% 或跌破 200 日線）")]


def test_supertrend_bear_sells_switched_incumbent_and_is_not_refilled_this_week():
    pool = [_row("A", "green"), _row("B", "green")]
    rot = _roster(pool, ["A"], {"A": _status(st_dir="bear")}, BULL_US)
    assert "A" not in rot["core"]
    assert ("A", "週線 Supertrend 翻空") in rot["removed"]
    assert rot["filled"] == [("core", "B")]


def test_switched_incumbent_out_of_pool_is_sold_as_out_of_pool():
    pool = [_row("B", "green")]                                  # A 不在池內
    rot = _roster(pool, ["A", "B"], {"A": _status()}, BULL_US)
    assert rot["core"] == ["B"] and rot["removed"] == [("A", "出池（資格不成立）")]
    both = _roster(pool, ["A", "B"], {"A": _status(st_dir="bear")}, BULL_US)   # 翻空又出池：記為出池
    assert both["removed"] == [("A", "出池（資格不成立）")]


def test_all_unswitched_is_identical_to_current_rule():
    pool = [_row("A", "red"), _row("B", "green"), _row("C", "yellow"), _row("D", "green")]
    status = {t: _status(switched=False) for t in ("A", "B", "C")}
    for market in (BEAR_US, BULL_US, None):
        new = _roster(pool, ["A", "B", "C"], status, market)
        old = seat_tm.select_roster(pool, ["A", "B", "C"], market, ba.select_hold_roster)
        assert new == old
    pool2, prev2, removed = st.apply_overlay(pool, ["A", "B", "C"], status)
    assert pool2 is pool and prev2 == ["A", "B", "C"] and removed == []


def test_mark_core_rows_forces_full_size_only_for_switched():
    sw, plain = _row("A", "red", 0.0), _row("B", "yellow", 0.5)
    sw["seat_note"] = "現任・週中轉紅，週六複判"
    stat = {"A": dict(_status(), entry_date="2026-10-24", entry_price=10.0, st_line=9.0),
            "B": dict(_status(switched=False), entry_date="2026-10-24", entry_price=10.0, st_line=9.0)}
    st.mark_core_rows([sw, plain], stat)
    assert sw["lamp"]["size"] == 1.0 and sw["action"].startswith("正常倉") and "Supertrend 持有" in sw["seat_note"]
    assert plain["lamp"]["size"] == 0.5 and "action" not in plain
    assert sw["st"]["switched"] and not plain["st"]["switched"]


def test_exit_label_texts():
    sw = st.public_view(dict(_status(), entry_date="2026-10-24", entry_price=10.0, st_line=9.0, data_ok=True))
    short, full = st.exit_label(sw)
    assert short == "Supertrend 或出池" and "2026-11-06" in full and "9.00" in full
    assert st.exit_label(dict(sw, switched=False))[0] == "跌 10% 紅燈"


# ── 選席：台股席位 ───────────────────────────────────────────────────────────

def test_tw_switched_incumbent_below_200_line_stays_in_bull_market():
    stocks = [_inc(vs200=-2.0)]                                  # 現行：大盤多頭、跌破自己的 200 日線 → 下席
    assert _sel_tw(stocks, BULL, None)["core"] == []
    sel = _sel_tw(stocks, BULL, {"1000.TW": _status()})
    assert [r["ticker"] for r in sel["core"]] == ["1000.TW"]
    assert sel["core"][0]["x1_hold"] is False and "Supertrend 持有" in sel["core"][0]["seat_note"]


def test_tw_switched_incumbent_ignores_bear_market_red():
    sel = _sel_tw([_inc()], BEAR, {"1000.TW": _status()})
    assert [r["ticker"] for r in sel["core"]] == ["1000.TW"]


def test_tw_supertrend_bear_removed_with_reason_and_unswitched_unchanged():
    sel = _sel_tw([_inc(), _stock("2000.TW", **_rev(10))], BULL,
                  {"1000.TW": _status(st_dir="bear"), "2000.TW": _status(switched=False)},
                  prev=("1000.TW", "2000.TW"))
    assert [r["ticker"] for r in sel["core"]] == ["2000.TW"]
    assert ("1000.TW", "週線 Supertrend 翻空") in sel["rotation"]["removed"]


def test_tw_switch_never_true_is_identical_to_current_rule():
    stocks = lambda: [_inc("1000.TW"), _stock("2000.TW", **_rev(30)), _inc("3000.TW", rev=25, vs200=-3.0)]  # noqa: E731
    prev = ("1000.TW", "3000.TW")
    status = {t: _status(switched=False) for t in prev}
    for market in (BULL, BEAR, None):
        a = tw.select(_rows(stocks()), list(prev), True, market=market)
        b = tw.select(_rows(stocks()), list(prev), True, market=market, st_status=status)
        assert [r["ticker"] for r in a["core"]] == [r["ticker"] for r in b["core"]]
        assert a["rotation"] == b["rotation"]


def _sel_tw(stocks, market, status, prev=("1000.TW",)):
    return tw.select(_rows(stocks), list(prev), True, market=market, st_status=status)


# ── 生效日 ───────────────────────────────────────────────────────────────────

def test_cutover_date_gate():
    assert not st.active("2026-10-31")
    assert st.active(st.CUTOVER_DATE)


# ── 席位進出通知：下席原因 ───────────────────────────────────────────────────

def test_roster_alert_shows_supertrend_bear_reason():
    import check_seat_roster_alerts as al
    prev = {"seats": [{"t": "AAA", "n": "甲"}, {"t": "BBB", "n": "乙"}], "queue": []}
    cur = {"seats": [{"t": "BBB", "n": "乙"}], "queue": [], "why": al._why_map([{"ticker": "AAA", "why": "週線 Supertrend 翻空"}])}
    text = al._describe(al.diff_segment(prev, cur))
    assert "出席 AAA 甲（週線 Supertrend 翻空）" in text
    assert al.compute(None, {"us": cur}, "2026-11-07")["new_state"]["segments"]["us"].get("why") is None
