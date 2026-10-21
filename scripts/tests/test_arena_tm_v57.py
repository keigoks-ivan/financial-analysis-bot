"""美股看板 v5.7（2026-10-21 持有人破例決定）：大盤空頭才看紅燈（SPY 還原收盤 vs 200 日線）。

規則見 scripts/engine/seat_tm.py 檔頭（回測定義：紅燈 ∧ 大盤空頭，不是看大盤切換）。這裡驗：大盤狀態判定（含恰好相等、均線不足、不偷看決策日之後、資料過舊）、
大盤多頭週所有紅燈（含跌破 200 日線）都不下席／出池仍下席、大盤空頭週紅燈下席、資料過舊退回現行賣法、
續抱倉位沿用最近一次非紅燈的倉位（狀態檔）、十倍股頁與台股不受影響。合成資料，不連網。
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from engine import build_arena, grp, seat_tm  # noqa: E402
from test_arena_lamp_only import _CORE5, _patch_paths, _v5_stock, _write_fixtures  # noqa: E402

AS_OF = "2026-09-18"        # 週五


def _series(closes, end=date(2026, 9, 18)):
    n = len(closes)
    days = [end - timedelta(days=n - 1 - i) for i in range(n)]
    return list(zip(days, closes))


# ── 大盤狀態 ──────────────────────────────────────────────────────────────

def test_state_bear_bull_and_exactly_equal_is_bull():
    bear = seat_tm.market_state(_series([100.0] * 199 + [99.0]), date(2026, 9, 18))
    assert (bear["status"], bear["mode"]) == ("bear", "e1")
    # 恰好相等＝多頭：200 列平均 = 100，收盤 100
    eq = seat_tm.market_state(_series([100.0] * 200), date(2026, 9, 18))
    assert (eq["status"], eq["mode"]) == ("bull", "tm") and eq["ma200"] == 100.0


def test_fewer_than_200_rows_counts_as_bull():
    st = seat_tm.market_state(_series([100.0] * 150 + [1.0]), date(2026, 9, 18))
    assert st["ma200"] is None and st["mode"] == "tm"


def test_average_uses_exactly_the_last_200_rows():
    st = seat_tm.market_state(_series([1000.0] * 50 + [100.0] * 200), date(2026, 9, 18))
    assert st["ma200"] == 100.0 and st["status"] == "bull"


def test_never_peeks_past_the_decision_day():
    s = _series([100.0] * 199 + [110.0, 50.0])          # 最後一列暴跌，決策日是前一天
    assert seat_tm.market_state(s, date(2026, 9, 17))["status"] == "bull"
    assert seat_tm.market_state(s, date(2026, 9, 18))["status"] == "bear"


def test_stale_or_missing_data_falls_back_to_current_exit():
    s = _series([100.0] * 200, end=date(2026, 9, 10))
    st = seat_tm.market_state(s, date(2026, 9, 18))     # 8 天前
    assert (st["status"], st["mode"]) == ("stale", "e1")
    assert seat_tm.market_state(s, date(2026, 9, 17))["status"] == "bull"   # 7 天內不算舊
    assert seat_tm.market_state([], date(2026, 9, 18))["status"] == "missing"
    assert seat_tm.market_state(s, date(2020, 1, 1))["status"] == "missing"  # 決策日前沒有任何資料


def test_load_close_series_reads_flowmap_format_and_survives_bad_file(tmp_path):
    p = tmp_path / "f.json"
    p.write_text(json.dumps({"series": {"SPY": [["2026-09-17", 500.0], ["2026-09-16", 499.5], ["x", 1]]}}))
    assert seat_tm.load_close_series(p) == [(date(2026, 9, 16), 499.5), (date(2026, 9, 17), 500.0)]
    assert seat_tm.load_close_series(tmp_path / "nope.json") == []
    p.write_text("{bad")
    assert seat_tm.load_close_series(p) == []


# ── 純函式：選席 ──────────────────────────────────────────────────────────

def _row(t, code="green", size=1.0):
    return {"ticker": t, "lamp": {"code": code, "size": size, "label": code, "why": ""},
            "dist_ath_pct": -1.0}


def _selector(pool, prev, core_slots=5):
    return build_arena.select_lit_roster_v52(pool, prev, core_slots=core_slots)


BULL = {"mode": "tm", "status": "bull"}
BEAR = {"mode": "e1", "status": "bear"}


def test_bull_week_every_red_incumbent_stays():
    # 紅燈不論原因（距新高 <−10% 或跌破 200 日線）都續抱
    pool = [_row("A", "red"), _row("B", "red"), _row("C")]
    rot = seat_tm.select_roster(pool, ["A", "B"], BULL, _selector)
    assert rot["core"] == ["A", "B", "C"] and rot["removed"] == []


def test_bear_week_and_stale_week_red_incumbent_leaves_like_before():
    pool = [_row("A", "red"), _row("C")]
    for market in (BEAR, {"mode": "e1", "status": "stale"}, None):
        rot = seat_tm.select_roster(pool, ["A"], market, _selector)
        assert rot["core"] == ["C"] and [t for t, _ in rot["removed"]] == ["A"]


def test_bull_week_new_red_name_is_not_bought():
    rot = seat_tm.select_roster([_row("A", "red"), _row("C")], [], BULL, _selector)
    assert rot["core"] == ["C"]            # 非現任的紅燈不當亮燈


def test_bull_week_incumbent_out_of_pool_leaves():
    rot = seat_tm.select_roster([_row("C")], ["A"], BULL, _selector)      # A 不在池內（資格不成立）
    assert rot["core"] == ["C"] and [t for t, _ in rot["removed"]] == ["A"]


def test_input_rows_are_not_mutated_and_no_market_equals_selector():
    pool = [_row("A", "red")]
    seat_tm.select_roster(pool, ["A"], BULL, _selector)
    assert pool[0]["lamp"]["code"] == "red"
    pool2 = [_row("A"), _row("B", "red")]
    assert seat_tm.select_roster(pool2, ["B"], None, _selector) == _selector(pool2, ["B"])


def test_hold_uses_last_nonred_size_default_and_state_update():
    rows = [_row("A", "red", size=0.0), _row("B", "red", size=0.0), _row("C", "hot", size=0.5)]
    held = seat_tm.held_tickers(rows, {"A", "B", "C"}, BULL, build_arena.LIT_LAMP_CODES)
    assert held == {"A", "B"}
    logs = []
    seat_tm.apply_hold(rows, held, {"A": {"size": 0.5}}, log=logs.append)
    assert rows[0]["lamp"]["size"] == 0.5 and rows[0]["action"] == "半倉・續抱" and rows[0]["lamp"]["code"] == "red"
    assert rows[1]["lamp"]["size"] == 1.0 and rows[1]["action"] == "正常倉・續抱" and len(logs) == 1
    assert "lamp" in rows[2] and rows[2]["lamp"]["label"] == "hot"
    new = seat_tm.update_state({"A": {"size": 0.5}, "Z": {"size": 1.0}}, rows, "2026-09-18", build_arena.LIT_LAMP_CODES)
    assert set(new) == {"A", "C"} and new["C"]["size"] == 0.5          # 紅燈保留舊值；離席的 Z 丟掉
    assert seat_tm.held_tickers(rows, {"A"}, BEAR, build_arena.LIT_LAMP_CODES) == set()


def test_us_and_tenbagger_pool_threshold_untouched():
    assert grp.POOL_REV_MIN == 5.0 and grp.in_pool(4.9) is False


# ── 端到端：build_arena.main() --ledger / --daily ─────────────────────────

def _spy_file(path, closes, end=date(2026, 9, 18)):
    path.write_text(json.dumps({"series": {"SPY": [[d.isoformat(), c] for d, c in _series(closes, end)]}}))


def _stocks(a_extra=None):
    a = _v5_stock("PQRSA", 20.0, dist_ath=-15.0, **(a_extra or {}))   # 距新高 −15%：紅燈（站上 200 日線）
    return [a] + [_v5_stock(t, 20.0) for t in _CORE5[1:]] + [_v5_stock("PQRSF", 8.0)]


def _ledger():
    return {"schema_version": "5.0", "last_rotation_month": "2026-09", "w52_fail_streak": {},
            "roster": {"core": list(_CORE5)}, "snapshots": [{"date": "2026-09-11", "core": list(_CORE5), "sat": []}]}


def _run(monkeypatch, tmp_path, stocks, spy, flag="--ledger", state=None, ledger=None, as_of=AS_OF):
    paths = _patch_paths(monkeypatch, tmp_path)
    _write_fixtures(paths, stocks, as_of=as_of, ledger=ledger or _ledger())
    if spy is not None:
        _spy_file(paths["SPY_PRICES_JSON"], spy)
    if state is not None:
        paths["STATE_JSON"].write_text(json.dumps({"last_nonred": state}), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["build_arena.py", flag])
    assert build_arena.main() == 0
    return paths, json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))


BULL_SPY = [100.0] * 199 + [101.0]
BEAR_SPY = [100.0] * 199 + [90.0]


def test_e2e_bull_week_red_incumbent_stays_with_last_nonred_size(tmp_path, monkeypatch):
    paths, out = _run(monkeypatch, tmp_path, _stocks(), BULL_SPY, state={"PQRSA": {"size": 0.5}})
    core = {r["ticker"]: r for r in out["core_seats"]}
    assert sorted(core) == sorted(_CORE5)
    a = core["PQRSA"]
    assert a["lamp"]["code"] == "red" and a["lamp"]["label"] == "🔴 續抱" and a["lamp"]["size"] == 0.5
    assert a["action"] == "半倉・續抱" and "大盤多頭續抱" in a["seat_note"]
    assert out["market_tm"]["status"] == "bull"
    ledger = json.loads(paths["LEDGER_JSON"].read_text(encoding="utf-8"))
    assert ledger["roster"]["core"] == _CORE5 and ledger["last_decision_date"] == AS_OF
    state = json.loads(paths["STATE_JSON"].read_text(encoding="utf-8"))["last_nonred"]
    assert state["PQRSA"]["size"] == 0.5 and state["PQRSB"]["size"] == 1.0     # 紅燈者保留舊值，亮燈者更新
    html = paths["BOARD_HTML"].read_text(encoding="utf-8")
    assert "v5.7 變更" in html and "/cockpit/#seats-grid" in html and "多頭" in html


def test_e2e_bull_week_missing_state_uses_one_and_logs(tmp_path, monkeypatch, capsys):
    _, out = _run(monkeypatch, tmp_path, _stocks(), BULL_SPY)
    a = next(r for r in out["core_seats"] if r["ticker"] == "PQRSA")
    assert a["lamp"]["size"] == 1.0 and a["action"] == "正常倉・續抱"
    assert "狀態檔沒有最近非紅燈倉位" in capsys.readouterr().out


def test_e2e_bear_week_red_incumbent_leaves_and_next_name_fills(tmp_path, monkeypatch):
    _, out = _run(monkeypatch, tmp_path, _stocks(), BEAR_SPY)
    assert sorted(r["ticker"] for r in out["core_seats"]) == sorted(_CORE5[1:] + ["PQRSF"])
    assert any(x["ticker"] == "PQRSA" for x in out["rotation"]["removed"])
    assert out["market_tm"]["status"] == "bear"


@pytest.mark.parametrize("spy", [None, [100.0] * 200], ids=["no-file", "stale"])
def test_e2e_missing_or_stale_market_data_keeps_current_exit(tmp_path, monkeypatch, spy):
    paths = _patch_paths(monkeypatch, tmp_path)
    _write_fixtures(paths, _stocks(), as_of=AS_OF, ledger=_ledger())
    if spy is not None:
        _spy_file(paths["SPY_PRICES_JSON"], spy, end=date(2026, 9, 1))
    monkeypatch.setattr(sys, "argv", ["build_arena.py", "--ledger"])
    assert build_arena.main() == 0
    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    assert "PQRSA" not in [r["ticker"] for r in out["core_seats"]]
    assert out["market_tm"]["status"] in ("missing", "stale")


def test_e2e_bull_week_below_200_red_incumbent_stays(tmp_path, monkeypatch):
    stocks = _stocks()
    stocks[0]["timing"] = {"vs_200ma_pct": -3.0, "dist_52w_high_pct": -15.0}
    _, out = _run(monkeypatch, tmp_path, stocks, BULL_SPY)
    assert "PQRSA" in [r["ticker"] for r in out["core_seats"]]        # 跌破 200 日線也是紅燈：多頭週續抱


def test_e2e_bull_week_ineligible_incumbent_leaves(tmp_path, monkeypatch):
    stocks = _stocks()
    stocks[0]["ma"]["above_w52"] = False           # 位置閘不過＝資格不成立
    _, out = _run(monkeypatch, tmp_path, stocks, BULL_SPY)
    assert "PQRSA" not in [r["ticker"] for r in out["core_seats"]]


def test_e2e_daily_run_uses_last_decision_days_market_and_never_writes_ledger(tmp_path, monkeypatch):
    ledger = _ledger()
    ledger["last_decision_date"] = "2026-09-11"
    paths = _patch_paths(monkeypatch, tmp_path)
    _write_fixtures(paths, _stocks(), as_of="2026-09-16", ledger=ledger)
    # 決策日（9-11）前是多頭；之後兩天暴跌，今天的大盤已是空頭，但平日刷燈沿用決策日狀態
    closes = [100.0] * 195 + [101.0] * 3 + [60.0] * 2
    _spy_file(paths["SPY_PRICES_JSON"], closes, end=date(2026, 9, 16))
    before = paths["LEDGER_JSON"].read_text(encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["build_arena.py", "--daily"])
    assert build_arena.main() == 0
    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    assert out["market_tm"]["decision_date"] == "2026-09-11" and out["market_tm"]["status"] == "bull"
    assert paths["LEDGER_JSON"].read_text(encoding="utf-8") == before


# ── v5.7 第四項：池不看上修門檻 ────────────────────────────────────────────

def test_e2e_pool_has_no_revision_threshold_valuation_red_still_out_and_order_by_revision(tmp_path, monkeypatch):
    stocks = [_v5_stock("PQRSA", 20.0), _v5_stock("LOWREV", 1.0), _v5_stock("NEGREV", -2.0),
              _v5_stock("PRICEY", 30.0, live_peg=3.0)]          # 估值閘紅燈：太貴不入池
    paths = _patch_paths(monkeypatch, tmp_path)
    _write_fixtures(paths, stocks, as_of=AS_OF, ledger={"schema_version": "5.0", "snapshots": []})
    monkeypatch.setattr(sys, "argv", ["build_arena.py", "--ledger"])
    assert build_arena.main() == 0
    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    seated = [r["ticker"] for r in out["core_seats"]]
    assert seated == ["PQRSA", "LOWREV", "NEGREV"]          # 池序＝上修降冪，含 +1% 與 −2%
    assert out["pool_size"] == 3 and out["not_in_pool"] == []
    assert "PRICEY" not in seated
