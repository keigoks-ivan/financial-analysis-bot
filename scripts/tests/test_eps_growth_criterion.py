"""EPS 成長條件改由 Koyfin EPS 直接算（2026-10-09，build_dd_screener.py
EPS_GROWTH_SPAN；knowledge/rule_ledger.md「EPS 成長條件」兩列）。

1. _koyfin_eps_growth()：Koyfin 預算欄空白（2026-06-23 起的匯出）時由 FY1／FY2／FY3
   自己算；有預算欄時照用。
2. _apply_tw_growth_criterion()：台股池改看 FY+1→FY+2、只換 label 與 span，
   門檻與 SCORED_CRITERIA 的 key 不變。沒呼叫時（美股預設）一律 FY+1→FY+3。

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

# 2330 on 2026-10-09 (Koyfin USD): FY1 3.38, FY2 4.52, FY3 5.76, precomputed columns blank.
TSMC = {"fy1": 3.38, "fy2": 4.52, "fy3": 5.76,
        "growth_fy1_fy2_pct": None, "growth_fy2_fy3_pct": None, "cagr_fy1_fy3_pct": None}


@pytest.fixture
def tw_mode(monkeypatch):
    """Apply the TW growth swap, then restore every module global it touches."""
    monkeypatch.setattr(bds, "CRITERIA", bds.CRITERIA)
    monkeypatch.setattr(bds, "SCORED_CRITERIA", bds.SCORED_CRITERIA)
    monkeypatch.setattr(bds, "EPS_GROWTH_SPAN", bds.EPS_GROWTH_SPAN)
    bds._apply_tw_growth_criterion()
    yield


def test_fy1_fy3_derived_when_column_blank():
    assert bds._koyfin_eps_growth(TSMC, "fy1_fy3") == 30.54


def test_fy1_fy2_derived_when_column_blank():
    assert bds._koyfin_eps_growth(TSMC, "fy1_fy2") == 33.73


def test_precomputed_column_wins():
    rec = dict(TSMC, cagr_fy1_fy3_pct=25.0, growth_fy1_fy2_pct=20.0)
    assert bds._koyfin_eps_growth(rec, "fy1_fy3") == 25.0
    assert bds._koyfin_eps_growth(rec, "fy1_fy2") == 20.0


def test_missing_or_non_positive_inputs():
    # No FY3: no FY1→FY3 figure (US then keeps the yfinance fallback).
    assert bds._koyfin_eps_growth(dict(TSMC, fy3=None), "fy1_fy3") is None
    # Loss in FY1: growth undefined either way.
    assert bds._koyfin_eps_growth(dict(TSMC, fy1=-0.5), "fy1_fy2") is None
    assert bds._koyfin_eps_growth(dict(TSMC, fy1=-0.5), "fy1_fy3") is None
    # FY2 drop to a loss is still a valid (negative) one-year growth.
    assert bds._koyfin_eps_growth(dict(TSMC, fy2=-1.0), "fy1_fy2") == round((-1.0 / 3.38 - 1) * 100, 2)


def test_default_mode_is_fy1_fy3():
    assert bds.EPS_GROWTH_SPAN == "fy1_fy3"
    eps = next(c for c in bds.CRITERIA if c["key"] == "eps2y")
    assert eps["label"] == "FY+1→FY+3 CAGR≥15%"


def test_tw_page_generator_uses_same_label():
    import build_dd_screener_tw_page as page
    assert page.TW_GROWTH_LABEL == bds.TW_EPS_GROWTH_LABEL


def test_tw_mode_swaps_label_and_span_only(tw_mode):
    assert bds.EPS_GROWTH_SPAN == "fy1_fy2"
    eps = next(c for c in bds.CRITERIA if c["key"] == "eps2y")
    assert eps["label"] == bds.TW_EPS_GROWTH_LABEL
    assert eps["threshold"] == 15.0 and eps["invert"] is False
    assert [c["key"] for c in bds.SCORED_CRITERIA] == ["fcf", "roic", "eps2y", "peg"]
