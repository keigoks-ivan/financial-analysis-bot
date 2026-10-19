"""Unit tests for build_etf_dash.compute_forward_summary（2026-10-19 財務預估摘要）。No network."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "etf_dash"))

import build_etf_dash as b  # noqa: E402


def _c(w, price, e1, e0=None, em1=None, e0_90d=None, ticker="X"):
    return {"ticker": ticker, "weight_pct": w, "price_usd": price, "eps_fy_next_usd": e1,
            "eps_fy_next_local": e1, "eps_fy_curr_local": e0, "eps_fy_prev_actual_local": em1,
            "eps_fy_curr_90d_local": e0_90d}


def _periods(rev=3.0, cov=90.0):
    return [{"key": "90d", "eps_chg_pct": rev, "coverage_pct": cov}]


def two_stocks():
    # A: PE1=10, PE0=12.5, PEm1=20；B: PE1=20, PE0=25, PEm1=25
    return [_c(60, 100, 10, 8, 5, 7.6, "A"), _c(40, 100, 5, 4, 4, 4.0, "B")]


def test_hand_computed_case():
    r = b.compute_forward_summary(two_stocks(), 100.0, _periods())
    # Σw/PE1=.08, Σw/PE0=.064, Σw/PEm1=.046（w 以比例計）
    assert r["fy1"]["pe"] == 12.5                       # 沿用頭條 1/.08
    assert r["fy1"]["eps_growth_pct"] == pytest.approx(25.0)
    assert r["fy1"]["peg"] == pytest.approx(0.5)
    assert r["fy0"]["pe"] == pytest.approx(15.62, abs=0.01)   # 1/.064=15.625
    assert r["fy0"]["eps_growth_pct"] == pytest.approx(39.13, abs=0.01)
    assert r["fy0"]["peg"] == pytest.approx(0.40, abs=0.01)
    assert r["fy1"]["rev_3m_pct"] == 3.0                # 沿用 Exhibit 1
    assert r["fy0"]["coverage_pct"] == 100.0
    # 今年度 3 個月修正：A 8/7.6-1=5.263%、B 0% → 加權 .6×5.263=3.158
    assert r["fy0"]["rev_3m_pct"] == pytest.approx(3.16, abs=0.01)


def test_pe_band_excludes_year_specific():
    # B 的今年度 EPS 極小 → PE0 = 20×5/0.1 = 1000 倍 > 300，不進 S0，fy1 成長只看 A
    cs = [_c(60, 100, 10, 8, 5), _c(40, 100, 5, 0.1, 4)]
    r = b.compute_forward_summary(cs, 100.0, _periods())
    assert r["fy0"]["coverage_pct"] == 60.0
    assert r["fy0"]["pe"] == 12.5
    assert r["fy1"]["eps_growth_pct"] == pytest.approx(25.0)   # A：PE0 12.5 → PE1 10
    assert r["fy1"]["pe"] == pytest.approx(12.5)               # 頭條仍含 B（PE1=20 在帶內）：1/.08


def test_missing_and_negative_values():
    cs = [_c(50, 100, 10, 8, None), _c(50, 100, 10, -1.0, 5), _c(10, 100, 10, None, None)]
    r = b.compute_forward_summary(cs, 110.0, _periods())
    # 只有第一檔有可用今年度 EPS；去年度實際缺 → fy0 成長 None、PEG None
    assert r["fy0"]["eps_growth_pct"] is None and r["fy0"]["peg"] is None
    assert r["fy0"]["coverage_pct"] == pytest.approx(50 / 110 * 100, abs=0.01)
    assert r["fy1"]["eps_growth_pct"] == pytest.approx(25.0)


def test_negative_growth_gives_null_peg():
    cs = [_c(100, 100, 8, 10, 8)]    # PE1=12.5 PE0=10 PEm1=12.5 → fy1 成長 -20%、fy0 成長 +25%
    r = b.compute_forward_summary(cs, 100.0, _periods())
    assert r["fy1"]["eps_growth_pct"] == pytest.approx(-20.0)
    assert r["fy1"]["peg"] is None
    assert r["fy0"]["eps_growth_pct"] == pytest.approx(25.0)
    assert r["fy0"]["peg"] == pytest.approx(0.4)


def test_old_cache_without_new_fields():
    cs = [{"ticker": "A", "weight_pct": 100, "price_usd": 100, "eps_fy_next_usd": 10, "eps_fy_next_local": 10}]
    r = b.compute_forward_summary(cs, 100.0, _periods(rev=2.0))
    assert r["fy0"] == {"pe": None, "eps_growth_pct": None, "peg": None, "rev_3m_pct": None,
                         "coverage_pct": None, "pe_coverage_pct": None, "growth_coverage_pct": None,
                         "rev_coverage_pct": None}
    assert r["fy1"]["pe"] == 10.0 and r["fy1"]["rev_3m_pct"] == 2.0
    assert r["fy1"]["eps_growth_pct"] is None
    assert b.compute_forward_summary([], 0.0, None)["fy1"]["pe"] is None


def test_foreign_currency_uses_local_eps_ratio():
    # 當地幣別 EPS 比值與匯率無關：price_usd／eps_usd 已換匯，E1/E0 用當地值
    cs = [{"ticker": "T", "weight_pct": 100, "price_usd": 100, "eps_fy_next_usd": 10,
           "eps_fy_next_local": 300.0, "eps_fy_curr_local": 240.0, "eps_fy_prev_actual_local": 200.0}]
    r = b.compute_forward_summary(cs, 100.0, _periods())
    assert r["fy0"]["pe"] == pytest.approx(12.5)      # 10 × 300/240
    assert r["fy1"]["eps_growth_pct"] == pytest.approx(25.0)
    assert r["fy0"]["eps_growth_pct"] == pytest.approx(20.0)
