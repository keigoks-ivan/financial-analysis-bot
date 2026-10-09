"""台股池 OCF 現金流條件（2026-10-09，build_dd_screener.py TW_OCF_CRITERION；
knowledge/rule_ledger.md「台股池現金流條件改看營業現金流」列）。

1. _tw_cash_fields()：OCF 利潤率＝FCF 利潤率＋|Capex|／Sales；資本支出缺值時
   退回 FCF 利潤率；ocf_ni_ratio 只在淨利率 > 0 時算。
2. _apply_tw_cash_criteria()：只換 fcf 一條、門檻不變、presets 補 ocf、
   FunnelRank v2 quality 層換成 ocf／ocf_ni_ratio。沒呼叫時（美股預設）一律是 FCF。
3. evaluate_criteria()：擴產股（FCF 低、OCF 高）在台股模式過現金流條件，
   在預設模式照舊不過。

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
