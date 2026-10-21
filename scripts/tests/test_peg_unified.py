"""全站 PEG 統一算法（2026-10-21，持有人指示「PEG 口徑統一處理」）。無網路。"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402
from engine import grp  # noqa: E402
from peg_unified import compute_peg_unified, price_currency  # noqa: E402
from sop_funnel import engine as sop  # noqa: E402


def test_basic_usd():
    r = compute_peg_unified("NVDA", 216.47, 15.91, 51.3988)
    assert r["fpe_next"] == round(216.47 / 15.91, 2)
    assert r["live_peg"] == round(216.47 / 15.91 / 51.3988, 2)


def test_eps_nonpositive_or_missing_gives_none():
    for e in (0, -1.0, None):
        assert compute_peg_unified("X", 100, e, 20) == {"fpe_next": None, "live_peg": None}


def test_growth_nonpositive_or_missing_keeps_fpe_but_no_peg():
    for g in (0, -5.0, None):
        r = compute_peg_unified("X", 100, 5.0, g)
        assert r["fpe_next"] == 20.0 and r["live_peg"] is None


def test_missing_price_gives_none():
    assert compute_peg_unified("X", None, 5.0, 20)["fpe_next"] is None


def test_tw_twd_both_sides_direct():
    r = compute_peg_unified("2330.TW", 2420.0, 148.9, 31.2209, eps_ccy="TWD")
    assert r["live_peg"] == round(2420 / 148.9 / 31.2209, 2)


def test_tw_usd_eps_converted_with_fx():
    # tw 池建構中 EPS 還是 Koyfin 美元、股價是新台幣：換成新台幣再除。
    r = compute_peg_unified("2330.TW", 2420.0, 4.56, 31.22, eps_ccy="USD", fx_per_usd=32.65)
    assert r["fpe_next"] == round(2420 / (4.56 * 32.65), 2)
    assert compute_peg_unified("2330.TW", 2420.0, 4.56, 31.22, eps_ccy="USD")["fpe_next"] is None, "沒匯率不猜"


def test_kl_usd_eps_myr_price_pinned():
    # 已知地雷：主名單 .KL 的 eps_fy_next 是美元、股價是馬幣，直接相除會放大約 4 倍。
    assert price_currency("5326.KL") == "MYR"
    naive = 3.09 / 0.02
    r = compute_peg_unified("5326.KL", 3.09, 0.02, 22.4745, eps_ccy="USD", fx_per_usd=4.2)
    assert r["fpe_next"] == round(3.09 / (0.02 * 4.2), 2)
    assert abs(naive / r["fpe_next"] - 4.2) < 0.01
    assert compute_peg_unified("5326.KL", 3.09, 0.02, 22.4745, eps_ccy="USD")["live_peg"] is None
    assert compute_peg_unified("5326.KL", 3.09, 0.02, 22.4745, eps_ccy="USD", fx_per_usd=None)["fpe_next"] is None


def test_unknown_suffix_or_foreign_eps_ccy_or_unreliable_gives_none():
    assert compute_peg_unified("XYZ.L", 100, 5, 20, fx_per_usd=0.8)["fpe_next"] is None     # 英國便士不認
    assert compute_peg_unified("ASML", 100, 5, 20, eps_ccy="EUR")["fpe_next"] is None        # 美元股價配歐元 EPS
    assert compute_peg_unified("JPM", 100, 5, 20, eps_reliable=False)["fpe_next"] is None    # yfinance 備援列幣別不明


def test_compute_live_peg_wrapper_uses_fx_only_when_needed():
    lfy = {"eps_1y_raw": 0.02, "cagr_fy1_fy3_pct": 22.4745, "eps_source": "xlsx"}
    r = bds._compute_live_peg("5326.KL", {"price": 3.09}, lfy, fx_for=lambda c: 4.2 if c == "MYR" else None)
    assert r["fpe_next"] == round(3.09 / 0.084, 2)
    r2 = bds._compute_live_peg("5326.KL", {"price": 3.09}, lfy, fx_for=lambda c: None)
    assert r2 == {"fpe_next": None, "live_peg": None}
    r3 = bds._compute_live_peg("NVDA", {"price": 216.47}, {"eps_1y_raw": 15.91, "cagr_fy1_fy3_pct": 51.4, "eps_source": "xlsx"},
                               fx_for=lambda c: (_ for _ in ()).throw(AssertionError("美元不該查匯率")))
    assert r3["live_peg"] == round(216.47 / 15.91 / 51.4, 2)


def test_evaluate_criteria_reads_live_peg_missing_fails():
    q = {"fcf": 20, "roic": 30, "eps2y": 20, "peg": 0.5, "live_peg": 1.9}
    assert bds.evaluate_criteria(q) == (4, [])
    q2 = dict(q, live_peg=2.1)
    assert bds.evaluate_criteria(q2) == (3, ["peg"])
    q3 = dict(q, live_peg=None)                       # 舊 peg 0.5 不能救
    assert bds.evaluate_criteria(q3) == (3, ["peg"])
    assert bds.FUNNEL_FORGIVABLE_FAILS == {"peg"}


def test_grp_valuation_gate_missing_peg_looks_only_at_multiple():
    g = grp.valuation_gate({"pe_vs_5y_x": 1.2, "peg": 9.9})
    assert g["light"] == "🟢" and g["peg"] is None
    g = grp.valuation_gate({"pe_vs_5y_x": 2.0})
    assert g["light"] == "🔴" and g["red_by"] == ["pe_vs_5y"]
    assert grp.valuation_gate({})["light"] == "⚪"


def test_grp_cycle_guard_and_own_penalty_ignore_old_peg():
    s = {"eps_fy1_fy3_cagr_pct": 20, "live_fpe_est": 10.0, "peg": 0.1, "roic": 10,
         "fund": {"gm_ltm_pct": 10, "gm_fy1_pct": 40, "gm_fy2_pct": 20}, "ma": {}}
    assert grp.own_raw(s)["cycle_guard"] is False
    s2 = dict(s, live_peg=0.1)
    assert grp.own_raw(s2)["cycle_guard"] is True
    assert grp.own_score(dict(s, peg=3.0))["peg_penalty"] is False
    assert grp.own_score(dict(s, live_peg=3.0))["peg_penalty"] is True


def test_sop_quality_check_missing_live_peg_is_missing_data():
    row = {"eps_fy1_fy3_cagr_pct": 25, "roic": 30, "fcf": 20, "peg": 0.4, "moat_grade": "S", "moat_trend": "→"}
    ok, fails, used = sop.quality_check(row)
    assert ok is None and fails == ["缺資料"] and used["peg_used"] is None
