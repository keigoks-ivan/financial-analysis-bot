"""第三條對照線「假設折衷組從 2024-01-02 起一直在跑」（scripts/engine/seat_st.py 的 hypo_*、scripts/build_seat_hypo_seed.py）。
種子可重現、每週維護與實際新規則線用同一組函式、實際新規則線與舊規則對照線的輸出逐位不變。合成資料，不連網。"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_seat_hypo_seed as seed  # noqa: E402
from engine import seat_st as st  # noqa: E402
from test_seat_st import DECISION, RISING, daily_from_weekly, weekly_label  # noqa: E402

ROOT = SCRIPTS_DIR.parent


# ── 種子可重現 ────────────────────────────────────────────────────────────
def _raw():
    d = daily_from_weekly(RISING)
    d0 = weekly_label(d, 20).date().isoformat()
    wk = [{"date": weekly_label(d, k).date().isoformat(), "nav": 1.0 + 0.01 * k, "held": ["AAA"]} for k in range(20, 40)]
    return d, {
        "market": "large", "start": "2024-01-02", "price_end": "2026-11-04", "rev_matrix_end": "2026-10-30",
        "weeks": wk,
        "trades": [dict(t="AAA", d0=d0, p0=1.0, d1=None, p1=2.0, why="持有中", name="甲", ret=1.0, days=10,
                        sw_date=wk[5]["date"], sw_why="停損線高過買進價", held_at_ny=False)],
        "events": [[d0, "AAA", "買進", 1.0, 0.2, "係數1"]], "nav_last": 1.2, "mdd": -0.1}


def test_seed_is_reproducible_and_pure(monkeypatch):
    d, raw = _raw()
    monkeypatch.setattr(seed, "SEED_DECISION", "2099-01-01")
    a = seed.convert(json.loads(json.dumps(raw)), "us", lambda t: d)
    b = seed.convert(json.loads(json.dumps(raw)), "us", lambda t: d)
    assert json.dumps(a, ensure_ascii=False, sort_keys=True) == json.dumps(b, ensure_ascii=False, sort_keys=True)
    assert a["roster"] == ["AAA"] and a["holdings"]["AAA"]["switched"] is True
    assert a["nav"]["series"][0] == {"week": "2024-01-02", "nav": 1.0, "ret": 0.0, "missing": [], "source": "replay"}
    assert a["nav"]["positions"] == {"AAA": 1.0}                       # 已切換者滿倉
    assert a["seed"]["differences"]                                    # 差異清單一定要寫
    assert a["schema"] == st.HYPO_SCHEMA


def test_committed_seed_files_are_valid_and_match_working_copy():
    for seed_p, work_p in ((ROOT / "docs/engine/seat_st_hypo_seed.json", ROOT / "docs/engine/seat_st_hypo.json"),
                           (ROOT / "docs/cockpit-tw/data/seat_st_hypo_seed_tw.json",
                            ROOT / "docs/cockpit-tw/data/seat_st_hypo_tw.json")):
        a = st.load_hypo(seed_p)
        assert a and len(a["roster"]) == 5 and a["start"] == "2024-01-02" and a["decision_date"] == "2026-10-30"
        assert set(a["roster"]) == set(a["holdings"]) == set(a["nav"]["positions"])
        assert a["nav"]["series"][0]["week"] == "2024-01-02" and a["nav"]["asof"] == "2026-10-30"
        w = st.load_hypo(work_p)
        # 還沒有週六排程跑過時，工作檔就是種子的複本；之後工作檔會前進，這個條件才不再成立
        if w.get("step_week") is None:
            assert w == a


# ── 每週維護 ──────────────────────────────────────────────────────────────
def _doc(roster, holds, navs=1.0, asof="2026-10-30", positions=None):
    return {"schema": st.HYPO_SCHEMA, "start": "2024-01-02", "roster": roster, "holdings": holds, "events": [],
            "nav": {"series": [{"week": asof, "nav": navs, "ret": 0.0, "missing": [], "source": "replay"}],
                    "asof": asof, "positions": positions or {t: 1.0 for t in roster}},
            "seed": {"differences": ["x"], "decision_date": asof}}


def _hold(entry, switched=False, **kw):
    return dict({"entry_date": entry, "entry_price": None, "switched": switched, "switch_week": None,
                 "switch_reason": None, "st_dir": None, "st_line": None, "week": None, "data_ok": True}, **kw)


def _rot(core=None, removed=(), filled=()):
    def rotate(prev, st0):
        return {"core": list(core if core is not None else prev), "removed": list(removed), "filled": list(filled)}
    return rotate


def test_hypo_step_is_idempotent_within_a_week_and_extends_nav():
    d = daily_from_weekly(RISING)
    lab = [weekly_label(d, k).date().isoformat() for k in range(60)]
    doc = _doc(["A"], {"A": _hold(lab[30])}, asof=lab[40])
    loader = lambda t: d  # noqa: E731
    one = st.hypo_step(doc, lab[45], lab[45], _rot(), lambda t, sw: 1.0, loader)
    two = st.hypo_step(one, lab[45], lab[45], _rot(), lambda t, sw: 1.0, loader)       # 同一週重跑
    assert json.dumps(one, sort_keys=True) == json.dumps(two, sort_keys=True)
    assert len(one["nav"]["series"]) == 2 and one["nav"]["series"][-1]["week"] == lab[45]
    assert one["nav"]["series"][-1]["nav"] > 1.0 and one["nav"]["asof"] == lab[45]
    three = st.hypo_step(one, lab[46], lab[46], _rot(), lambda t, sw: 1.0, loader)     # 下一週再加一筆
    assert len(three["nav"]["series"]) == 3


def test_hypo_step_uses_same_switch_logic_as_actual_line():
    """切換狀態來自 build_status（與實際新規則線同一個函式）；已切換者資料之後不會被退回。"""
    d = daily_from_weekly(RISING)
    lab = [weekly_label(d, k).date().isoformat() for k in range(60)]
    doc = _doc(["A"], {"A": _hold(lab[30])}, asof=lab[40])
    out = st.hypo_step(doc, lab[45], lab[45], _rot(), lambda t, sw: 1.0 if sw else 0.5, lambda t: d)
    exp = st.build_status(["A"], {"A": (lab[30], None)}, lab[45], {}, lambda t: d)["A"]
    assert out["holdings"]["A"]["switched"] == exp["switched"] and out["holdings"]["A"]["switch_week"] == exp["switch_week"]
    assert out["nav"]["positions"]["A"] == (1.0 if exp["switched"] else 0.5)
    sticky = _doc(["A"], {"A": _hold(lab[30], True, switch_week=lab[31], switch_reason="b")}, asof=lab[40])
    out2 = st.hypo_step(sticky, lab[45], lab[45], _rot(), lambda t, sw: 1.0, lambda t: None)   # 抓不到資料也不退回
    assert out2["holdings"]["A"]["switched"] is True


def test_hypo_step_logs_events_and_handles_missing_universe_names():
    d = daily_from_weekly(RISING)
    lab = [weekly_label(d, k).date().isoformat() for k in range(60)]
    doc = _doc(["A", "OUT", "OUT2"], {"A": _hold(lab[30]), "OUT": _hold(lab[30], True, switch_week=lab[31], switch_reason="a"),
                                      "OUT2": _hold(lab[30])}, asof=lab[40])
    rot = _rot(core=["A", "N1", "N2"], removed=[("X", "出池")], filled=[("core", "N1"), ("core", "N2")])
    falling = daily_from_weekly([200 - i for i in range(60)])              # 一路下跌：不會切換
    out = st.hypo_step(doc, lab[45], lab[45], rot, lambda t, sw: 1.0, lambda t: falling if t == "OUT2" else d,
                       known={"A", "N1", "N2"})
    # OUT 已切換、週線沒翻空：續抱占一席；OUT2 未切換又不在母體：賣出
    assert out["roster"][0] == "OUT" and len(out["roster"]) <= 5
    assert "OUT2" not in out["roster"]
    ev = {(e["ticker"], e["kind"]): e["why"] for e in out["events"]}
    assert ev[("OUT2", "賣出")] == "不在網站母體" and ("N1", "買進") in ev and ("X", "賣出") in ev


# ── 實際新規則線與舊規則對照線逐位不變 ─────────────────────────────────────
def test_new_rule_rotation_equals_inline_overlay_plus_selector():
    """build_arena 改呼叫 new_rule_rotation，輸出必須和原本內嵌的三行逐位相同。"""
    pool = [{"ticker": t, "lamp": {"code": "yellow"}} for t in "ABCD"]
    status = {"A": {"switched": True, "st_dir": "bear"}, "B": {"switched": True, "st_dir": "bull"}}

    def selector(p, pv):
        return {"core": [r["ticker"] for r in p if r["ticker"] in pv] + ["Z"], "removed": [("Q", "紅燈")], "filled": [("core", "Z")],
                "rotated": False}
    a_pool, a_prev, a_rm = st.apply_overlay(pool, ["A", "B", "C"], status, pool)
    inline = selector(a_pool, a_prev)
    inline["removed"] = list(inline["removed"]) + a_rm
    assert st.new_rule_rotation(pool, ["A", "B", "C"], status, pool, selector) == inline


def _old_module():
    try:
        src = subprocess.run(["git", "show", "origin/main:scripts/engine/seat_st.py"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("沒有 origin/main 可比對")
    spec = importlib.util.spec_from_loader("seat_st_old", loader=None)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "engine"
    mod.__file__ = str(ROOT / "scripts/engine/seat_st_old.py")
    exec(compile(src, "seat_st_old", "exec"), mod.__dict__)
    return mod


def test_actual_and_legacy_nav_output_bit_for_bit_unchanged():
    old = _old_module()
    d = daily_from_weekly([100, 110, 121, 100, 90, 95, 120])
    lab = [weekly_label(d, k).date().isoformat() for k in range(7)]
    loader = lambda t: d  # noqa: E731
    a = b = {}
    for k in (0, 1, 1, 3, 6):
        a = old.update_nav(a, lab[k], {"A": 1.0, "B": 0.5}, {"A": 0.5}, loader)
        b = st.update_nav(b, lab[k], {"A": 1.0, "B": 0.5}, {"A": 0.5}, loader)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert old.nav_summary(a) == st.nav_summary(b)
    # 掛上假設線之後，新規則與舊規則的欄位不變，只多一個 hypo key
    hyp = _doc(["A"], {"A": _hold(lab[0])}, asof=lab[0])
    c = st.attach_hypo_to_nav(b, hyp)
    assert {k: v for k, v in c.items() if k != "hypo"} == b and "hypo" in c
    assert st.nav_summary(c) == st.nav_summary(b)
    assert old.legacy_html({"core": ["A"], "removed": [], "as_of": "x"}, "美股看板", nav=old.nav_summary(a)) == \
        st.legacy_html({"core": ["A"], "removed": [], "as_of": "x"}, "美股看板", nav=st.nav_summary(b))


def test_builders_call_the_shared_functions():
    arena = (SCRIPTS_DIR / "engine/build_arena.py").read_text(encoding="utf-8")
    twb = (SCRIPTS_DIR / "build_seats_tw.py").read_text(encoding="utf-8")
    assert arena.count("seat_st.new_rule_rotation(") == 2           # 實際新規則線與假設線各一
    assert "seat_st.hypo_step(" in arena and "seat_st.hypo_step(" in twb
    assert "hypo_step(" in arena[arena.index("if st_on and args.ledger"):]   # 只在週六 --ledger 才前進
    assert "select(copy.deepcopy(rows), prev, True" in twb and "st_status=st0" in twb


# ── 頁面區塊 ──────────────────────────────────────────────────────────────
def test_hypo_html_has_disclaimer_holdings_and_three_lines():
    doc = st.load_hypo(ROOT / "docs/engine/seat_st_hypo_seed.json")
    summ = st.hypo_summary(doc, None)
    html = st.hypo_html(doc, summ, None, "美股看板")
    for must in ("假設路徑", "2024-01-02", "不能照著買", "買進價", "目前停損線", "11-07"):
        assert must in html
    nav = {"new": {"cum": 0.01, "mdd": -0.02}, "legacy": {"cum": 0.0, "mdd": -0.03}}
    doc2 = json.loads(json.dumps(doc))
    doc2["nav"]["series"].append({"week": "2026-11-06", "nav": doc["nav"]["series"][-1]["nav"] * 1.01})
    navdoc = {"series": [{"week": "2026-11-06"}]}
    summ2 = st.hypo_summary(doc2, navdoc)
    assert summ2["window"]["from"] == "2026-11-06"
    assert "三條線同一起點比較" in st.hypo_html(doc2, summ2, nav, "美股看板")
