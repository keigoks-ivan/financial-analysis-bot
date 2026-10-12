#!/usr/bin/env python3
"""期望報酬漂移歸因由程式拆量（先換情境、股價不動；再換股價、情境不動），2026-10-12 GFS／AMAT。
以及證據 findings 來源字串的 CJK 後半形標點轉全形（dd_evidence.finalize）。"""
import json
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dd2"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402
import dd_evidence  # noqa: E402

GFS = {"ticker": "GFS", "date": "2026-10-12", "price": 48.24,
       "start": {"eps": 1.96, "pe": 24.61, "basis": "x"},
       "yield_pct": {"dividend": 0.498, "net_buyback": 0.0}, "terminal_label": "FY2030E",
       "scenarios": {
           "bull": {"eps_path": [2.0, 2.85, 3.9, 4.8, 5.6], "terminal_pe": 21, "p": 25},
           "base": {"eps_path": [1.96, 2.55, 3.25, 3.75, 4.2], "terminal_pe": 16, "p": 45},
           "bear": {"eps_path": [1.9, 2.05, 1.75, 2.05, 2.4], "terminal_pe": 12, "p": 30}},
       "consensus": {"fy1": 1.96, "fy2": 2.63, "fy3": 3.56},
       "second_stage": {"bull_cagr_pct": 12, "base_cagr_pct": 7}, "endo_ceiling_exceeded": True}
AMAT = {"ticker": "AMAT", "date": "2026-10-12", "price": 507.03,
        "start": {"eps": 12.79, "pe": 39.64, "basis": "x"},
        "yield_pct": {"dividend": 0.391, "net_buyback": 0.4}, "terminal_label": "FY2031E",
        "scenarios": {
            "bull": {"eps_path": [20.5, 27.0, 31.5, 36.0, 40.0], "terminal_pe": 26, "p": 25},
            "base": {"eps_path": [18.3, 22.0, 22.0, 24.5, 27.0], "terminal_pe": 22, "p": 45},
            "bear": {"eps_path": [16.5, 13.5, 12.0, 14.0, 16.0], "terminal_pe": 17, "p": 30}},
        "consensus": {"fy1": 12.79, "fy2": 18.47, "fy3": 23.6},
        "second_stage": {"bull_cagr_pct": 12, "base_cagr_pct": 8}, "endo_ceiling_exceeded": True}

PM_GFS = {"price_at_dd": 69.71, "ev5y_pct": 31.0, "irr_base_pct": 6.3, "asym_ratio": 2.3,
          "bull_5y_price": 143.0, "bear_5y_price": 43.0}
PM_AMAT = {"price_at_dd": 668.0, "ev5y_pct": 5.0, "irr_base_pct": 2.5, "asym_ratio": None,
           "bull_5y_price": 955.24, "bear_5y_price": 307.28}


def _ctx(tmp_path, scen, ticker):
    (tmp_path / "scenario.json").write_text(json.dumps(scen), encoding="utf-8")
    return types.SimpleNamespace(run_dir=tmp_path, ticker=ticker, date="20261012", manifest={})


def _split(tmp_path, scen, pm, ticker):
    ents, fields = run.return_split_entries(_ctx(tmp_path, scen, ticker), pm, {})
    return {e["cause"]: e for e in ents}, fields


def test_gfs_known_answer(tmp_path):
    ents, fields = _split(tmp_path, GFS, PM_GFS, "GFS")
    assert fields == set(run.RETURN_SPLIT_ALL)
    m, p = ents["方法變動"], ents["價格變動"]
    assert m["axis"].startswith("[程式歸因]期望報酬拆解")
    assert "69.71" in m["axis"]
    assert "+31.0%" in m["side_a"] and "6.3%" in m["side_a"] and "不對稱比 2.3" in m["side_a"]
    assert "−2.1%" in m["side_b"] and "−0.7%" in m["side_b"] and "不對稱比 0.98" in m["side_b"]
    assert "−2.1%" in p["side_a"] and "+41.5%" in p["side_b"] and "6.9%" in p["side_b"]
    assert "不對稱比 0.98" in p["side_a"] and "不對稱比 2.97" in p["side_b"]
    assert "拆解順序為先情境後股價" in p["ruling"] and "先換情境、股價不動" in m["ruling"]
    assert m["prior_field"] == list(run.RETURN_SPLIT_ALL)
    assert p["prior_field"] == list(run.RETURN_SPLIT_FIELDS)  # bull／bear 價與現價無關，不進價格條
    assert m["evidence_level"] == "程式計算" and m["if_then"] == []


def test_amat_known_answer(tmp_path):
    ents, _ = _split(tmp_path, AMAT, PM_AMAT, "AMAT")
    m, p = ents["方法變動"], ents["價格變動"]
    assert "Bull 價 955.24、Bear 價 307.28" in m["side_a"]
    assert "前份未列不對稱比" in m["side_a"]
    assert "Bull 價 1,040、Bear 價 272" in m["side_b"]
    assert "−8.8%" in m["side_b"] and "−2.3%" in m["side_b"] and "不對稱比 0.78" in m["side_b"]
    assert "前份未列不對稱比，本次為 0.78" in m["ruling"]
    assert "−8.8%" in p["side_a"] and "+20.1%" in p["side_b"] and "3.2%" in p["side_b"]
    assert "不對稱比 1.89" in p["side_b"]
    assert "Bull" not in p["side_a"] and "Bull" not in p["side_b"]


def test_numbers_match_dd_scenario_directly():
    m = run._return_metrics(GFS, 69.71)
    assert m["ev5y_pct"] == pytest.approx(-2.1, abs=0.05)
    assert m["irr_base_pct"] == pytest.approx(-0.7, abs=0.05)
    assert m["asym_ratio"] == pytest.approx(0.98, abs=0.005)
    m = run._return_metrics(AMAT, 668.0)
    assert m["bull_5y_price"] == pytest.approx(1040, abs=1) and m["bear_5y_price"] == pytest.approx(272, abs=1)


def test_missing_prior_price_no_entries(tmp_path):
    pm = dict(PM_GFS, price_at_dd=None)
    assert run.return_split_entries(_ctx(tmp_path, GFS, "GFS"), pm, {}) == ([], set())


def test_missing_scenario_no_entries(tmp_path):
    ctx = types.SimpleNamespace(run_dir=tmp_path, ticker="GFS", date="20261012", manifest={})
    assert run.return_split_entries(ctx, PM_GFS, {}) == ([], set())


def test_nothing_changed_no_entries(tmp_path):
    # 前份值就是本次情境在本次股價下的結果，股價也相同
    cur = run._return_metrics(GFS, 48.24)
    pm = {"price_at_dd": 48.24, "ev5y_pct": round(cur["ev5y_pct"], 1), "irr_base_pct": round(cur["irr_base_pct"], 1),
          "asym_ratio": round(cur["asym_ratio"], 1), "bull_5y_price": round(cur["bull_5y_price"], 1),
          "bear_5y_price": round(cur["bear_5y_price"], 1)}
    assert run.return_split_entries(_ctx(tmp_path, GFS, "GFS"), pm, {}) == ([], set())


def test_only_price_changed_makes_only_price_entry(tmp_path):
    cf = run._return_metrics(GFS, 69.71)
    pm = {"price_at_dd": 69.71, "ev5y_pct": round(cf["ev5y_pct"], 1), "irr_base_pct": round(cf["irr_base_pct"], 1),
          "asym_ratio": round(cf["asym_ratio"], 1), "bull_5y_price": round(cf["bull_5y_price"], 1),
          "bear_5y_price": round(cf["bear_5y_price"], 1)}
    ents, fields = _split(tmp_path, GFS, pm, "GFS")
    assert set(ents) == {"價格變動"} and fields == set(run.RETURN_SPLIT_FIELDS)


def _prior(tmp_path, pm):
    (tmp_path / "parts").mkdir(exist_ok=True)
    (tmp_path / "parts" / "prior.json").write_text(json.dumps({"prior_dd": {
        "price_at_dd": pm["price_at_dd"], "prior_meta": pm}}), encoding="utf-8")


def test_judge_entry_fields_stripped_and_recorded(tmp_path, monkeypatch):
    ctx = _ctx(tmp_path, GFS, "GFS")
    _prior(tmp_path, PM_GFS)
    monkeypatch.setattr(run, "_ma_label", lambda c: None)
    monkeypatch.setattr(run, "_current_price", lambda c: None)
    obj = {"counter_evidence": {"contradictions": [
        {"axis": "判斷者：期望報酬", "cause": "價格變動", "prior_field": ["asym_ratio", "ev5y_pct", "irr_base_pct"],
         "ruling": "全是股價"},
        {"axis": "判斷者：毛利率", "cause": "新證據", "prior_field": ["moat_trend", "ev5y_pct"], "ruling": "x"}]}}
    obj, log = run.program_drift_entries(ctx, obj, decision_out=None)
    ents = obj["counter_evidence"]["contradictions"]
    assert [e["cause"] for e in ents[:2]] == ["方法變動", "價格變動"]
    judge = {e["axis"]: e for e in ents if not e["axis"].startswith("[程式歸因]")}
    assert judge["判斷者：期望報酬"]["prior_field"] == []          # 空陣列，文字保留
    assert judge["判斷者：期望報酬"]["ruling"] == "全是股價"
    assert judge["判斷者：毛利率"]["prior_field"] == ["moat_trend"]
    mo = ctx.manifest["mechanical_overrides"]
    assert {r["judge"] for r in mo} == {"asym_ratio", "ev5y_pct", "irr_base_pct"}
    # 重複呼叫（judged 第二階段、gate patch 後）冪等：程式條目不重複、紀錄不重複
    obj, _ = run.program_drift_entries(ctx, obj, decision_out=None)
    assert sum(e["axis"].startswith("[程式歸因]期望報酬拆解") for e in obj["counter_evidence"]["contradictions"]) == 2
    assert len(ctx.manifest["mechanical_overrides"]) == len(mo)


def test_judge_fields_kept_when_no_program_entry(tmp_path, monkeypatch):
    ctx = types.SimpleNamespace(run_dir=tmp_path, ticker="GFS", date="20261012", manifest={})  # 沒有 scenario.json
    _prior(tmp_path, PM_GFS)
    monkeypatch.setattr(run, "_ma_label", lambda c: None)
    monkeypatch.setattr(run, "_current_price", lambda c: None)
    obj = {"counter_evidence": {"contradictions": [
        {"axis": "判斷者", "cause": "價格變動", "prior_field": ["asym_ratio", "ev5y_pct"]}]}}
    obj, _ = run.program_drift_entries(ctx, obj, decision_out=None)
    assert obj["counter_evidence"]["contradictions"][0]["prior_field"] == ["asym_ratio", "ev5y_pct"]
    assert "mechanical_overrides" not in ctx.manifest


# ---- 任務 2：findings 來源字串半形標點轉全形 -------------------------------------

def test_findings_fullwidth_punct():
    base = {"coverage": {"ax": {"findings": [
        {"source": "Yahoo Finance／Reuters 摘要: Applied Materials 財測", "claim": "年增率, 優於預期",
         "url": "https://example.com/摘要:a,b", "href": "http://x/中:y", "link": "http://x/文.html",
         "note": "Note: x", "sources": ["Reuters 摘要: Applied"]}]}},
        "events": {"ev": {"findings": [{"claim": "營收3,000萬, 成長"}]}}}
    n = dd_evidence._fullwidth_findings(base)
    f = base["coverage"]["ax"]["findings"][0]
    assert f["source"] == "Yahoo Finance／Reuters 摘要：Applied Materials 財測"
    assert f["claim"] == "年增率，優於預期"
    assert f["note"] == "Note: x"
    assert f["url"] == "https://example.com/摘要:a,b" and f["href"] == "http://x/中:y" and f["link"] == "http://x/文.html"
    assert f["sources"] == ["Reuters 摘要：Applied"]
    assert base["events"]["ev"]["findings"][0]["claim"] == "營收3,000萬，成長"
    assert n == 4
