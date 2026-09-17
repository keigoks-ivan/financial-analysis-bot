"""Unit tests for scripts/build_dd_screener.py's compute_fundamental_gates()
and compute_eps_fy1_consec_down() (2026-09-17 fundamental-gates screener
additions — see the 35 new Koyfin xlsx columns documented in
scripts/load_eps_estimates_xlsx.py's module docstring).

Hand-made inputs only — no network / no cache files, no reliance on any
real xlsx or docs/dd-screener/eps-estimates-snapshots/*.json content (the
AAPL-shaped case below is a synthetic record with AAPL's known 2026-09-17
values baked in, not a live read of the xlsx). Same style as
scripts/tests/test_eps_fx_normalize.py.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402


def _aapl_record():
    """Synthetic record shaped like AAPL's real 2026-09-17 xlsx row (see
    verification in the task report) — used to pin down a known-good full
    row without depending on the xlsx file's content staying fixed."""
    return {
        "fcf_margin_pct": 29.28,
        "rev_yoy_fq0_pct": 16.36, "rev_yoy_fq1_pct": 16.6,
        "rev_yoy_fq2_pct": 15.65, "rev_yoy_fq3_pct": 7.94,
        "gm_ltm_pct": 48.65, "gm_fy1_pct": 46.21, "gm_fy2_pct": 44.13, "gm_fy3_pct": 43.31,
        "sales_ltm": 466820.0, "ebit_ltm": 154860.0, "net_debt_ebitda_x": None,
        "sales_growth_fy_pct": 7.94, "ebit_growth_fy_pct": 9.58,
        "dil_shares_fy": 15000.0, "dil_shares_fy3": 16330.0,
        "sbc_ltm": 13710.0, "capex_ltm": -10040.0, "fcf_ltm": 136680.0,
        "net_debt_ltm": -62170.0, "buyback_ltm": -88930.0,
        "ccc_days": -49.49,
        "pe_ntm_x": 36.1, "pe_ntm_5y_avg_x": 28.7, "pb_x": 45.2, "pb_5y_avg_x": 45.5,
        "rsi14": 62.1, "price_chg_6m_pct": 31.48,
        "target_high": 405.0, "target_low": 215.0, "target_avg": 327.84,
        "last_price_local": 332.41,
        "ni_margin_ltm_pct": 27.62, "est_rev_cagr_3y_pct": 11.12,
        "est_eps_cagr_3y_pct": 13.23, "below_52w_high_pct": -3.45,
    }


def test_aapl_full_row():
    g = bds.compute_fundamental_gates(_aapl_record(), "HH", eps_fy1=8.83)

    # A. quality veto — all healthy, 0 fails.
    assert g["gm_3y_decline"] == "pass"
    assert g["fcf_ni"] == "pass"
    assert g["rev_4q_negative"] == "pass"
    assert g["leverage"] == "pass"  # net_debt_ebitda_x None but net_debt_ltm < 0 -> net cash pass
    assert g["quality_veto_fail_count"] == 0
    assert g["quality_veto_level"] == "維持"

    # D. capital allocation — dilution net negative (buybacks), buyback/FCF ~65% (<=80),
    # leverage pass -> all 3 known and passing -> grade A.
    assert g["sbc_dilution_pct_yr"] == pytest.approx(-2.79, abs=0.02)
    assert g["capalloc_mech_grade"] == "A"

    # E. capex intensity — light (<5% of sales).
    assert g["capex_intensity_label"] == "輕"

    # F. unprofitable gates — AAPL is profitable, both None.
    assert g["rule_of_40"] is None
    assert g["cash_runway_months"] is None

    # G. decline signals — clean name, 0 signals, green light.
    assert g["decline_signal_count"] == 0
    assert g["decline_signal_light"] == "🟢"

    # H/I/J/K spot checks.
    assert g["pe_vs_5y_x"] == pytest.approx(1.26, abs=0.01)
    assert g["pe_vs_5y_flag"] is False
    assert g["target_range_x"] == pytest.approx(1.88, abs=0.01)
    assert g["rsi_overheated"] is False
    assert g["return_6m_gate"] == "放行"
    assert g["rsi_usable"] is True  # |below_52w_high_pct|=3.45 > 3
    assert g["ccc_supplier_financed"] is True  # ccc_days < 0
    assert g["lh_ccc_note"] is None  # not an LH quadrant name

    # "fund" sub-object bundles all 35 raw inputs for FE hover.
    assert g["fund"]["sales_ltm"] == 466820.0
    assert g["fund"]["target_avg"] == 327.84


def test_all_none_row_renders_safely():
    g = bds.compute_fundamental_gates(None, None, None, None)
    for key in ("gm_3y_decline", "fcf_ni", "rev_4q_negative", "leverage",
                "eps_fy1_consec_down", "ol_divergence_pp", "ol_divergence_label",
                "gm_trigger", "capalloc_mech_grade", "capex_pct_rev",
                "rule_of_40", "cash_runway_months", "pe_vs_5y_x", "target_upside_pct",
                "rsi_overheated", "return_6m_gate", "rsi_usable", "lh_ccc_note",
                "short_interest_pct_float", "short_squeeze_flag",
                "insider_net_buy_3m", "insider_signal"):
        assert g[key] is None
    assert g["quality_veto_fail_count"] == 0
    assert g["quality_veto_level"] is None  # no veto item known at all -> None, not a false "維持"
    assert g["quality_veto_fails"] == []
    assert g["decline_signal_count"] == 0
    assert g["decline_signal_light"] == "🟢"
    assert all(v is None for v in g["fund"].values())


def test_unprofitable_row_rule_of_40_and_runway():
    rec = {
        "ni_margin_ltm_pct": -12.0,
        "sales_growth_fy_pct": 30.0,
        "fcf_margin_pct": -15.0,   # rule_of_40 = 30 + (-15) = 15 < 20 -> flag
        "fcf_ltm": -50.0,          # burning cash
        "net_debt_ltm": -600.0,   # net cash pile
    }
    g = bds.compute_fundamental_gates(rec, None, eps_fy1=-1.5)
    assert g["rule_of_40"] == pytest.approx(15.0)
    assert g["rule_of_40_flag"] is True
    # cash_runway_months = 600 / (50/12) = 144
    assert g["cash_runway_months"] == pytest.approx(144.0)
    assert g["cash_runway_flag"] is False  # 144 >= 12


def test_net_cash_row_with_no_net_debt_ebitda_passes_leverage():
    rec = {"net_debt_ebitda_x": None, "net_debt_ltm": -200.0}
    g = bds.compute_fundamental_gates(rec, None, eps_fy1=None)
    assert g["leverage"] == "pass"

    rec_pos_unknown = {"net_debt_ebitda_x": None, "net_debt_ltm": 50.0}
    g2 = bds.compute_fundamental_gates(rec_pos_unknown, None, eps_fy1=None)
    assert g2["leverage"] is None  # net debt positive but no EBITDA multiple -> unknown


def test_short_interest_and_insider_signal_2026_09_17():
    # short_squeeze_flag: > 10 -> True, <= 10 -> False, missing -> None (untouched
    # by test_all_none_row_renders_safely above).
    hi = bds.compute_fundamental_gates({"short_interest_pct_float": 12.5}, None, None)
    assert hi["short_interest_pct_float"] == 12.5
    assert hi["short_squeeze_flag"] is True
    lo = bds.compute_fundamental_gates({"short_interest_pct_float": 3.2}, None, None)
    assert lo["short_squeeze_flag"] is False
    exactly_ten = bds.compute_fundamental_gates({"short_interest_pct_float": 10.0}, None, None)
    assert exactly_ten["short_squeeze_flag"] is False, "門檻是 > 10，不是 >= 10"

    # insider_signal: net buy > 0 -> 買, net sell < 0 -> 賣, 0 or missing -> None.
    buy = bds.compute_fundamental_gates({"insider_net_buy_3m": 15000.0}, None, None)
    assert buy["insider_net_buy_3m"] == 15000.0
    assert buy["insider_signal"] == "買"
    sell = bds.compute_fundamental_gates({"insider_net_buy_3m": -5000.0}, None, None)
    assert sell["insider_signal"] == "賣"
    flat = bds.compute_fundamental_gates({"insider_net_buy_3m": 0.0}, None, None)
    assert flat["insider_signal"] is None

    # both land inside the "fund" sub-object too (per _FUND_RAW_FIELDS).
    both = bds.compute_fundamental_gates(
        {"short_interest_pct_float": 22.0, "insider_net_buy_3m": -1000.0}, None, None)
    assert both["fund"]["short_interest_pct_float"] == 22.0
    assert both["fund"]["insider_net_buy_3m"] == -1000.0


def test_monotonic_gm_decline_fails():
    rec = {"gm_ltm_pct": 40.0, "gm_fy1_pct": 42.0, "gm_fy2_pct": 44.0, "gm_fy3_pct": 46.0}
    g = bds.compute_fundamental_gates(rec, None, eps_fy1=None)
    assert g["gm_3y_decline"] == "fail"
    assert "毛利連降" in g["quality_veto_fails"]
    assert g["quality_veto_fail_count"] == 1
    assert g["quality_veto_level"] == "維持"  # 1 fail is still in the 0-2 band

    # Decline < 2.0pp over the 3 steps should NOT fail despite being monotonic.
    rec_small = {"gm_ltm_pct": 40.0, "gm_fy1_pct": 40.5, "gm_fy2_pct": 41.0, "gm_fy3_pct": 41.5}
    g_small = bds.compute_fundamental_gates(rec_small, None, eps_fy1=None)
    assert g_small["gm_3y_decline"] == "pass"


def test_leverage_fail_pushes_toward_reject():
    rec = {
        "gm_ltm_pct": 40.0, "gm_fy1_pct": 42.0, "gm_fy2_pct": 44.0, "gm_fy3_pct": 46.0,
        "net_debt_ebitda_x": 4.5,
        "rev_yoy_fq0_pct": -1, "rev_yoy_fq1_pct": -2, "rev_yoy_fq2_pct": -3, "rev_yoy_fq3_pct": -4,
    }
    g = bds.compute_fundamental_gates(rec, None, eps_fy1=None)
    assert g["gm_3y_decline"] == "fail"
    assert g["leverage"] == "fail"
    assert g["rev_4q_negative"] == "fail"
    assert g["quality_veto_fail_count"] == 3
    assert g["quality_veto_level"] == "降一級"


# ---------------------------------------------------------------------------
# compute_eps_fy1_consec_down — hand-made baselines, USD ticker (no FX lookup
# needed) so the reporting-currency cache can be pre-populated and no
# network call happens.
# ---------------------------------------------------------------------------

def _baselines(fy1_06, fy1_07, fy1_08):
    def snap(date, val):
        return {"snapshot_date": date, "tickers": {"FAKE": {"eps_fy_curr": val}}}
    return {
        "2026-06": snap("2026-06-30", fy1_06),
        "2026-07": snap("2026-07-31", fy1_07),
        "2026-08": snap("2026-08-31", fy1_08),
    }


def test_eps_fy1_consec_down_fail_when_all_three_steps_down():
    baselines = _baselines(10.0, 9.9, 9.5)   # -1.0%, -4.04%
    ccy_cache = {"FAKE": {"currency": "USD"}}
    result = bds.compute_eps_fy1_consec_down(
        "FAKE", "FAKE", 9.0, "2026-09-17", ccy_cache, {}, baselines=baselines,
    )  # last step 9.5 -> 9.0 = -5.26%
    assert result == "fail"


def test_eps_fy1_consec_down_pass_when_one_step_not_down():
    baselines = _baselines(10.0, 9.9, 9.95)  # -1.0%, then +0.51% (not down)
    ccy_cache = {"FAKE": {"currency": "USD"}}
    result = bds.compute_eps_fy1_consec_down(
        "FAKE", "FAKE", 9.0, "2026-09-17", ccy_cache, {}, baselines=baselines,
    )
    assert result == "pass"


def test_eps_fy1_consec_down_none_when_baseline_missing():
    baselines = {
        "2026-06": {"snapshot_date": "2026-06-30", "tickers": {}},  # ticker absent
        "2026-07": {"snapshot_date": "2026-07-31", "tickers": {"FAKE": {"eps_fy_curr": 9.9}}},
        "2026-08": {"snapshot_date": "2026-08-31", "tickers": {"FAKE": {"eps_fy_curr": 9.5}}},
    }
    ccy_cache = {"FAKE": {"currency": "USD"}}
    result = bds.compute_eps_fy1_consec_down(
        "FAKE", "FAKE", 9.0, "2026-09-17", ccy_cache, {}, baselines=baselines,
    )
    assert result is None
