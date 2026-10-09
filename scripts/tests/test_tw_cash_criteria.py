"""台股池 OCF 現金流條件（2026-10-09，build_dd_screener.py TW_OCF_CRITERION；
knowledge/rule_ledger.md「台股池現金流條件改看營業現金流」列）。

1. _tw_cash_fields()：OCF 利潤率＝FCF 利潤率＋|Capex|／Sales；資本支出缺值時
   退回 FCF 利潤率；ocf_ni_ratio 只在淨利率 > 0 時算。
2. _apply_tw_cash_criteria()：只換 fcf 一條、門檻不變、presets 補 ocf、
   FunnelRank v2 quality 層換成 ocf／ocf_ni_ratio。沒呼叫時（美股預設）一律是 FCF。
3. evaluate_criteria()：擴產股（FCF 低、OCF 高）在台股模式過現金流條件，
   在預設模式照舊不過。
4. compute_fundamental_gates()：體質 veto 的現金對淨利一項與衰退訊號「FCF 遜於淨利」
   在台股模式改看營業現金流（CASH_BASIS），fcf_ni_ratio 輸出欄仍是 FCF／淨利。

No network, no xlsx.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402

# 聯亞 3081 on 2026-10-09: FCF margin 2.6%, capex 24.8% of sales, ROIC 20.8%.
CAPEX_HEAVY = {"fcf": 2.6, "ocf": 27.4, "roic": 20.8, "eps2y": 20.0, "peg": 1.5, "de": 0.1}


@pytest.fixture
def tw_mode(monkeypatch):
    """Apply the TW swap, then restore every module global it touches."""
    monkeypatch.setattr(bds, "CRITERIA", bds.CRITERIA)
    monkeypatch.setattr(bds, "SCORED_CRITERIA", bds.SCORED_CRITERIA)
    monkeypatch.setattr(bds, "PRESETS", bds.PRESETS)
    monkeypatch.setattr(bds, "CASH_BASIS", bds.CASH_BASIS)
    monkeypatch.setattr(bds, "QUALITY_VETO_LABELS", bds.QUALITY_VETO_LABELS)
    monkeypatch.setitem(bds.FUNNEL_V2_LAYER_FIELDS, "quality",
                        list(bds.FUNNEL_V2_LAYER_FIELDS["quality"]))
    bds._apply_tw_cash_criteria()
    yield


def _quality_layer_names():
    return [name for name, _, _ in bds.FUNNEL_V2_LAYER_FIELDS["quality"]]


def test_default_mode_scores_fcf():
    assert [c["key"] for c in bds.SCORED_CRITERIA] == ["fcf", "roic", "eps2y", "peg"]
    assert "ocf" not in bds.PRESETS["MLB"]
    assert _quality_layer_names() == ["roic_5y_avg_pct", "fcf", "fcf_ni_ratio", "ni_margin_ltm_pct"]
    assert bds.evaluate_criteria(dict(CAPEX_HEAVY)) == (3, ["fcf"])


def test_tw_mode_swaps_only_the_cash_criterion(tw_mode):
    assert [c["key"] for c in bds.SCORED_CRITERIA] == ["ocf", "roic", "eps2y", "peg"]
    ocf = next(c for c in bds.CRITERIA if c["key"] == "ocf")
    assert ocf["threshold"] == 10.0 and ocf["invert"] is False
    assert any(c["key"] == "de" and c.get("advisory") for c in bds.CRITERIA)
    assert bds.PRESETS["MLB"]["ocf"] == bds.PRESETS["MLB"]["fcf"] == 10.0
    assert _quality_layer_names() == ["roic_5y_avg_pct", "ocf", "ocf_ni_ratio", "ni_margin_ltm_pct"]


def test_tw_mode_capex_heavy_name_passes_cash(tw_mode):
    assert bds.evaluate_criteria(dict(CAPEX_HEAVY)) == (4, [])
    # Weak operating cash flow still fails (智邦-type working-capital drag).
    weak = dict(CAPEX_HEAVY, fcf=2.0, ocf=4.2)
    assert bds.evaluate_criteria(weak) == (3, ["ocf"])


def test_cash_fields_ocf_is_fcf_plus_capex_share():
    rec = {"capex_ltm": -24.8, "sales_ltm": 100.0, "ni_margin_ltm_pct": 20.0}
    out = bds._tw_cash_fields(rec, 2.6)
    assert out == {"ocf": 27.4, "ocf_basis": "fcf+capex", "capex_pct_sales": 24.8,
                   "ocf_ni_ratio": 1.37}


def test_cash_fields_missing_inputs():
    # Capex unknown: fall back to the FCF margin (OCF >= FCF, so never too lenient).
    assert bds._tw_cash_fields({"sales_ltm": 100.0}, 12.0)["ocf"] == 12.0
    assert bds._tw_cash_fields({"sales_ltm": 100.0}, 12.0)["ocf_basis"] == "fcf"
    # No FCF margin: no OCF either.
    assert bds._tw_cash_fields({"capex_ltm": -5.0, "sales_ltm": 100.0}, None)["ocf"] is None
    # Loss-making: no OCF/NI ratio.
    rec = {"capex_ltm": -5.0, "sales_ltm": 100.0, "ni_margin_ltm_pct": -3.0}
    assert bds._tw_cash_fields(rec, 1.0)["ocf_ni_ratio"] is None


def test_ocf_ni_ratio_capped_like_fcf_ni():
    assert bds._funnel_v2_ocf_ni_capped({"ocf_ni_ratio": 1.5}) == bds.FUNNEL_V2_FCF_NI_CAP
    assert bds._funnel_v2_ocf_ni_capped({"ocf_ni_ratio": 0.5}) == 0.5
    assert bds._funnel_v2_ocf_ni_capped({}) is None


# Capex-heavy record (USD m): FCF margin 2.6%, capex 24.8% of sales, NI margin 15%.
# FCF/NI 0.17 fails both cash checks; OCF/NI (2.6+24.8)/15 = 1.83 passes both.
GATES_CAPEX_HEAVY = {"fcf_margin_pct": 2.6, "ni_margin_ltm_pct": 15.0,
                     "capex_ltm": -248.0, "sales_ltm": 1000.0}
# Weak conversion even before capex: OCF 3.0% vs NI 15% fails in either mode.
GATES_WEAK_CASH = {"fcf_margin_pct": 2.0, "ni_margin_ltm_pct": 15.0,
                   "capex_ltm": -10.0, "sales_ltm": 1000.0}


def test_gates_default_mode_uses_fcf():
    out = bds.compute_fundamental_gates(GATES_CAPEX_HEAVY, None, None)
    assert out["fcf_ni"] == "fail"
    assert "FCF/淨利" in out["quality_veto_fails"]
    assert "FCF 遜於淨利" in out["decline_signals"]
    assert out["fcf_ni_ratio"] == 0.17


def test_gates_tw_mode_uses_ocf(tw_mode):
    out = bds.compute_fundamental_gates(GATES_CAPEX_HEAVY, None, None)
    assert out["fcf_ni"] == "pass"
    assert out["quality_veto_fails"] == []
    assert not any("淨利" in s for s in out["decline_signals"])
    assert out["fcf_ni_ratio"] == 0.17  # output field stays FCF/NI


def test_gates_tw_mode_still_flags_weak_cash(tw_mode):
    out = bds.compute_fundamental_gates(GATES_WEAK_CASH, None, None)
    assert out["fcf_ni"] == "fail"
    assert "OCF/淨利" in out["quality_veto_fails"]
    assert bds.TW_DECLINE_CASH_LABEL in out["decline_signals"]


def test_gates_tw_mode_capex_missing_falls_back_to_fcf(tw_mode):
    rec = {"fcf_margin_pct": 2.6, "ni_margin_ltm_pct": 15.0, "sales_ltm": 1000.0}
    assert bds.compute_fundamental_gates(rec, None, None)["fcf_ni"] == "fail"
