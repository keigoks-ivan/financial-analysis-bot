"""十倍股頁 v5.7（2026-10-21 持有人破例決定）：做成真的 10 席。

規則見 scripts/build_tenbagger.py 檔頭「v5.7 十席」：每週重選；在席者紅燈或出池就下席；空席從池中亮燈者照池序補，
最多 10 席；在席者不被排名更高的新名字擠掉；倉位綠 1.0／黃 1.0／橘 0.5，空席放現金；第一次跑沒有狀態檔就直接補。
合成資料，不連網。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_tenbagger as bt  # noqa: E402
from test_picks_v5 import _patch_tenbagger_paths, _v5_stock, _write_latest, _write_picks, _write_universe  # noqa: E402


def _pool(*specs):
    """specs＝(ticker, lamp_code)，依池序。"""
    return [{"ticker": t, "lamp": {"code": c}} for t, c in specs]


def test_first_run_fills_from_empty_in_pool_order_and_skips_unlit():
    pool = _pool(("A", "green"), ("B", "red"), ("C", "yellow"), ("D", "hot"))
    sel = bt.select_seats(pool, [])
    assert sel["roster"] == ["A", "C", "D"] and sel["filled"] == ["A", "C", "D"] and sel["removed"] == []


def test_fills_at_most_ten_seats():
    pool = _pool(*[(f"T{i:02d}", "green") for i in range(15)])
    sel = bt.select_seats(pool, [])
    assert sel["roster"] == [f"T{i:02d}" for i in range(10)]


def test_red_incumbent_leaves_and_out_of_pool_incumbent_leaves():
    pool = _pool(("A", "red"), ("B", "green"), ("N", "green"))
    sel = bt.select_seats(pool, ["A", "B", "GONE"])
    assert sel["roster"] == ["B", "N"]
    why = dict(sel["removed"])
    assert "轉紅" in why["A"] and "出池" in why["GONE"]
    assert sel["filled"] == ["N"]


def test_incumbent_is_never_pushed_out_by_a_higher_ranked_new_name():
    new_names = [(f"N{i}", "green") for i in range(12)]            # 12 個排名都比現任高的新名字
    pool = _pool(*new_names, ("OLD", "yellow"))
    sel = bt.select_seats(pool, ["OLD"])
    assert "OLD" in sel["roster"] and len(sel["roster"]) == 10
    assert sel["roster"] == [f"N{i}" for i in range(9)] + ["OLD"]   # 補 9 席，依池序排列
    assert sel["removed"] == []


def test_vacant_seats_stay_empty_when_nothing_is_lit():
    sel = bt.select_seats(_pool(("A", "red"), ("B", "red")), ["A"])
    assert sel["roster"] == [] and [t for t, _ in sel["removed"]] == ["A"]


def test_veto_reason_is_labelled():
    sel = bt.select_seats(_pool(("B", "green")), ["V"], vetoed=["V"])
    assert dict(sel["removed"])["V"] == "持有人否決"


# ── 端到端：build_tenbagger.main() ────────────────────────────────────────

def _setup(monkeypatch, tmp_path, stocks, as_of="2026-10-16"):
    paths = _patch_tenbagger_paths(monkeypatch, tmp_path)
    _write_universe(paths["universe"], [s["ticker"] for s in stocks])
    _write_latest(paths["latest"], stocks, as_of=as_of)
    _write_picks(paths["picks"])
    paths["seats"] = tmp_path / "tenbagger_seats.json"
    return paths


def _stocks(n=12, **over):
    out = []
    for i in range(n):
        s = _v5_stock(f"TB{i:02d}", rev_pct=30.0 - i, cap_b=5.0)
        out.append(s)
    return out


def _out(paths):
    return json.loads(paths["out"].read_text(encoding="utf-8"))


def test_e2e_first_run_without_state_file_fills_ten_seats_and_writes_state(tmp_path, monkeypatch):
    paths = _setup(monkeypatch, tmp_path, _stocks())
    assert not paths["seats"].exists()
    assert bt.main([]) == 0                                   # 沒帶 --ledger、也沒有狀態檔：照規則從空席補
    seats = _out(paths)["seats"]
    assert seats["n_seated"] == 10 and seats["vacant"] == 0 and seats["slots"] == 10
    assert [r["ticker"] for r in seats["roster"]] == [f"TB{i:02d}" for i in range(10)]
    assert seats["invested_seats"] == 10.0 and seats["cash_seats"] == 0.0     # 都是綠燈 1.0
    assert all(r["seat_note"] == "新席" for r in seats["roster"])
    state = json.loads(paths["seats"].read_text(encoding="utf-8"))
    assert state["roster"] == [f"TB{i:02d}" for i in range(10)] and state["last_rotation_date"] == "2026-10-16"
    assert [r["seat"] for r in _out(paths)["official"][:2]] == ["T1", "T2"]


def test_e2e_daily_run_keeps_roster_and_only_refreshes_lamps(tmp_path, monkeypatch):
    paths = _setup(monkeypatch, tmp_path, _stocks())
    bt.main([])
    before = paths["seats"].read_text(encoding="utf-8")
    stocks = _stocks()
    stocks[0]["ma"]["dist_ath_pct"] = -15.0                    # TB00 週中轉紅
    stocks.append(_v5_stock("NEWHI", rev_pct=99.0, cap_b=5.0))  # 上修最高的新名字、燈亮著
    _write_universe(paths["universe"], [s["ticker"] for s in stocks])
    _write_latest(paths["latest"], stocks, as_of="2026-10-19")
    bt.main([])                                                # 平日：不重選
    assert paths["seats"].read_text(encoding="utf-8") == before
    seats = _out(paths)["seats"]
    assert "NEWHI" not in [r["ticker"] for r in seats["roster"]] and seats["n_seated"] == 10
    tb0 = next(r for r in seats["roster"] if r["ticker"] == "TB00")
    assert tb0["seat_note"] == "新席・週中轉紅，週六複判" and tb0["lamp"]["code"] == "red"


def test_e2e_saturday_reselect_sells_red_fills_vacancy_without_displacing(tmp_path, monkeypatch):
    paths = _setup(monkeypatch, tmp_path, _stocks())
    bt.main([])
    stocks = _stocks()
    stocks[0]["ma"]["dist_ath_pct"] = -15.0                    # TB00 紅燈
    stocks[3]["ma"]["above_w52"] = False                       # TB03 資格不成立
    stocks.append(_v5_stock("NEWHI", rev_pct=99.0, cap_b=5.0))
    _write_universe(paths["universe"], [s["ticker"] for s in stocks])
    _write_latest(paths["latest"], stocks, as_of="2026-10-23")
    bt.main(["--ledger"])
    seats = _out(paths)["seats"]
    roster = [r["ticker"] for r in seats["roster"]]
    assert "TB00" not in roster and "TB03" not in roster
    assert {t["ticker"] for t in seats["removed"]} == {"TB00", "TB03"}
    # 空出 2 席：池序補亮燈者；NEWHI 排第一先補，再補 TB10（TB11 排後面沒有席）
    assert set(seats["filled"]) == {"NEWHI", "TB10"} and len(roster) == 10
    assert all(t in roster for t in ("TB01", "TB02", "TB04", "TB09"))     # 現任全留
    snaps = json.loads(paths["seats"].read_text(encoding="utf-8"))["snapshots"]
    assert [s["date"] for s in snaps] == ["2026-10-16", "2026-10-23"]


def test_e2e_orange_is_half_size_and_empty_seats_are_cash(tmp_path, monkeypatch):
    stocks = _stocks(n=3)
    stocks[1]["ma"]["mom_12_1_pct"] = 200.0                    # 過熱：橘燈、半倉
    paths = _setup(monkeypatch, tmp_path, stocks)
    bt.main([])
    seats = _out(paths)["seats"]
    assert seats["n_seated"] == 3 and seats["vacant"] == 7
    assert seats["invested_seats"] == 2.5 and seats["cash_seats"] == 7.5
    assert sorted((r["lamp"]["code"], r["lamp"]["size"]) for r in seats["roster"]) == [
        ("green", 1.0), ("green", 1.0), ("hot", 0.5)]


def test_e2e_retry_on_same_price_date_is_idempotent(tmp_path, monkeypatch):
    paths = _setup(monkeypatch, tmp_path, _stocks())
    bt.main([])
    stocks = _stocks()
    stocks[0]["ma"]["dist_ath_pct"] = -15.0
    _write_latest(paths["latest"], stocks, as_of="2026-10-23")
    bt.main(["--ledger"])
    first = paths["seats"].read_text(encoding="utf-8")
    bt.main(["--ledger"])
    assert paths["seats"].read_text(encoding="utf-8") == first


def test_e2e_pool_threshold_still_five_percent(tmp_path, monkeypatch):
    stocks = [_v5_stock("LOW", rev_pct=3.0, cap_b=5.0), _v5_stock("OK", rev_pct=8.0, cap_b=5.0)]
    paths = _setup(monkeypatch, tmp_path, stocks)
    bt.main([])
    assert [r["ticker"] for r in _out(paths)["seats"]["roster"]] == ["OK"]
