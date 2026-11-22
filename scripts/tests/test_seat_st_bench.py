"""看板席位淨值的 QQQ 對照線（seat_st.update_nav 的 bench 參數）：報酬、最大跌幅、merge_to_index；
台股不傳 bench 時輸出與原本逐位相同。合成資料，不連網。"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from engine import seat_st as st  # noqa: E402
from test_seat_st import daily_from_weekly, weekly_label  # noqa: E402

REPO = SCRIPTS_DIR.parent


def _setup(stock, qqq):
    ds, dq = daily_from_weekly(stock), daily_from_weekly(qqq)
    lab = [weekly_label(ds, k).date().isoformat() for k in range(len(stock))]
    return (lambda t: dq if t == "QQQ" else ds), lab


def _run(loader, lab, bench):
    doc = st.update_nav({}, lab[0], {"A": 1.0}, {"A": 1.0}, loader, bench=bench)
    for w in lab[1:]:
        doc = st.update_nav(doc, w, {"A": 1.0}, {"A": 1.0}, loader, bench=bench)
    return doc


def test_bench_return_mdd_and_merge_flag():
    # 席位：100→101→100（滿倉占 1/5 資金，報酬小、跌幅小）；QQQ：100→120→90（報酬 -10%、跌幅 -25%）
    loader, lab = _setup([100, 101, 100], [100, 120, 90])
    s = st.nav_summary(_run(loader, lab, "QQQ"))
    assert s["qqq"]["cum"] == pytest.approx(-0.10)
    assert s["qqq"]["mdd"] == pytest.approx(-0.25)
    assert s["new"]["cum"] > s["qqq"]["cum"] and s["merge_to_index"] is False
    # 席位大賠、QQQ 小賠小跌：報酬輸、跌幅更深才併回
    loader, lab = _setup([100, 50, 40], [100, 102, 99])
    s = st.nav_summary(_run(loader, lab, "QQQ"))
    assert s["new"]["cum"] < s["qqq"]["cum"] and s["new"]["mdd"] < s["qqq"]["mdd"]
    assert s["merge_to_index"] is True
    # 報酬輸但跌幅較淺：不併回
    loader, lab = _setup([100, 100, 100], [100, 110, 112])
    s = st.nav_summary(_run(loader, lab, "QQQ"))
    assert s["new"]["cum"] < s["qqq"]["cum"] and s["new"]["mdd"] >= s["qqq"]["mdd"]
    assert s["merge_to_index"] is False


def test_bench_rerun_same_week_and_backfill_old_rows():
    loader, lab = _setup([100, 110, 121], [100, 105, 110])
    plain = _run(loader, lab, None)
    assert "qqq" not in plain["series"][0] and "bench" not in plain
    back = st.update_nav(plain, lab[-1], {"A": 1.0}, {"A": 1.0}, loader, bench="QQQ")   # 舊 doc 缺 qqq → 整條重算
    assert [r["qqq"] for r in back["series"]] == pytest.approx([1.0, 1.05, 1.10])
    assert back["bench"] == "QQQ" and len(back["series"]) == 3
    again = st.update_nav(back, lab[-1], {"A": 1.0}, {"A": 1.0}, loader, bench="QQQ")   # 同週重跑不重複
    assert again == back
    for a, b in zip(plain["series"], back["series"]):                                    # 只加欄位
        assert all(b[k] == v for k, v in a.items())


def test_no_bench_output_unchanged_for_tw():
    loader, lab = _setup([100, 110, 121], [100, 105, 110])
    doc = _run(loader, lab, None)
    assert set(doc) == {"schema", "start", "review_date", "slots", "series", "holdings"}
    assert all("qqq" not in r for r in doc["series"])
    s = st.nav_summary(doc)
    assert "qqq" not in s and "merge_to_index" not in s and "retreat" in s
    assert "QQQ" not in st._nav_line(s)


def test_real_nav_json_one_more_week_does_not_break():
    doc = json.loads((REPO / "docs/engine/seat_st_nav.json").read_text(encoding="utf-8"))
    assert all("qqq" in r for r in doc["series"]) and doc["bench"] == "QQQ"
    last = doc["series"][-1]["week"]
    nxt = (st.pd.Timestamp(last) + st.pd.Timedelta(days=7)).date().isoformat()
    ds = daily_from_weekly([100] * 400, start="2026-01-02")
    loader = lambda t: ds   # noqa: E731
    before = copy.deepcopy(doc)
    out = st.update_nav(doc, nxt, doc["holdings"]["new"], doc["holdings"]["legacy"], loader, bench="QQQ")
    assert doc == before                                   # 不改輸入
    assert len(out["series"]) == len(before["series"]) + 1
    assert out["series"][-1]["week"] == nxt and "qqq" in out["series"][-1]
    s = st.nav_summary(out)
    assert s["weeks"] == 3 and "merge_to_index" in s
    assert "QQQ" in st._nav_line(s)
