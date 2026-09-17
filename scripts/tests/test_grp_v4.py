"""Unit tests for scripts/engine/grp.py's v4 additions (2026-09-17 席位引擎 v4 overhaul
— see knowledge/rule_ledger.md "v4 席位引擎" row):

  - timing_lamp(): pure timing-lamp truth table (out/red/hot/green/yellow, missing stage)
  - own_score_v4(): cross-sectional percentile math on a 5-row fixture, incl. the
    FCF/NI exemption when incremental_roic_pct >= 15
  - grp_score(): eligibility gates, incl. the 10% durable-growth relaxation and the
    v4 revision veto (eps_rev_3m_pct <= -5, falling back to the old FY+1 <= -10 rule
    only when eps_rev_3m_pct is missing)

Hand-made inputs only — no network, no disk reads of real dd-screener/lamp data.
Same style as scripts/tests/test_fundamental_gates.py.
"""
from __future__ import annotations

from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from engine import grp  # noqa: E402


# ── timing_lamp() truth table ────────────────────────────────────────────────

def _lamp_input(above_w52=True, vs200=5.0, rs=60.0, dist_hi=-5.0, stage="S1", overheated=False):
    return {
        "ma": {"above_w52": above_w52},
        "timing": {"vs_200ma_pct": vs200, "rs_score": rs, "dist_52w_high_pct": dist_hi},
        "_stage_code": stage,
        "_overheated": overheated,
    }


def test_timing_lamp_out_when_below_w52():
    lamp = grp.timing_lamp(_lamp_input(above_w52=False))
    assert lamp["code"] == "out"
    assert lamp["size"] == 0.0


def test_timing_lamp_red_vs200_negative():
    lamp = grp.timing_lamp(_lamp_input(vs200=-1.0))
    assert lamp["code"] == "red"
    assert lamp["trigger"] == "站回 200 日線且 RS ≥ 50"


def test_timing_lamp_red_rs_weak():
    lamp = grp.timing_lamp(_lamp_input(rs=30.0))
    assert lamp["code"] == "red"
    assert lamp["trigger"] == "RS 回到 50 以上"


def test_timing_lamp_red_far_from_high():
    lamp = grp.timing_lamp(_lamp_input(dist_hi=-30.0))
    assert lamp["code"] == "red"
    assert lamp["trigger"] == "回到高點 25% 內"


def test_timing_lamp_red_stage_s0():
    lamp = grp.timing_lamp(_lamp_input(stage="S0"))
    assert lamp["code"] == "red"


def test_timing_lamp_hot_overheated_overrides_green_setup():
    lamp = grp.timing_lamp(_lamp_input(overheated=True))
    assert lamp["code"] == "hot"
    assert lamp["size"] == 0.5


def test_timing_lamp_green_all_conditions_met():
    lamp = grp.timing_lamp(_lamp_input())
    assert lamp["code"] == "green"
    assert lamp["size"] == 1.0


def test_timing_lamp_green_missing_stage_does_not_block():
    lamp = grp.timing_lamp(_lamp_input(stage=None))
    assert lamp["code"] == "green", "缺 stage 應視為中性，不擋 green"


def test_timing_lamp_yellow_stage_not_in_green_set():
    lamp = grp.timing_lamp(_lamp_input(stage="S2"))
    assert lamp["code"] == "yellow"
    assert lamp["size"] == 0.5


def test_timing_lamp_yellow_when_numeric_inputs_missing():
    lamp = grp.timing_lamp(_lamp_input(vs200=None, rs=None, dist_hi=None, stage=None))
    assert lamp["code"] == "yellow", "above_w52 但關鍵數字缺 → 無法確認 green，落 yellow"


def test_lamp_action_mapping():
    assert grp.LAMP_ACTION["green"] == "正常倉"
    assert grp.LAMP_ACTION["yellow"] == "半倉"
    assert grp.LAMP_ACTION["hot"] == "半倉"
    assert grp.LAMP_ACTION["red"] == "零倉・等板機"
    assert grp.LAMP_ACTION["out"] == "—"


# ── own_score_v4() percentile math ───────────────────────────────────────────

def _five_row_fixture():
    return [
        {"rev": 10, "mom": 20, "g": 25, "ey": 4, "fcf_ni": 1.2, "dilution": 1.0,
         "incremental_roic_pct": None},
        {"rev": 5, "mom": 10, "g": 15, "ey": 3, "fcf_ni": 0.8, "dilution": 2.0,
         "incremental_roic_pct": 20.0},   # exempt: incremental ROIC >= 15
        {"rev": -2, "mom": -5, "g": 10, "ey": 2, "fcf_ni": 0.5, "dilution": 3.0,
         "incremental_roic_pct": None},
        {"rev": 20, "mom": 30, "g": 30, "ey": 5, "fcf_ni": None, "dilution": 0.5,
         "incremental_roic_pct": None},
        {"rev": 0, "mom": 0, "g": None, "ey": None, "fcf_ni": 1.0, "dilution": 1.5,
         "incremental_roic_pct": None},   # only 3/5 present -> score must be None
    ]


def test_own_score_v4_percentile_ranks():
    out = grp.own_score_v4(_five_row_fixture())
    # row 3 (index 3) has the best value on every axis -> percentile 100 on all, score 100
    assert out[3]["p_rev"] == 100.0
    assert out[3]["p_mom"] == 100.0
    assert out[3]["p_g"] == 100.0
    assert out[3]["p_ey"] == 100.0
    assert out[3]["score"] == 100.0
    # row 2 (index 2) has the worst rev/mom/ey -> lowest percentiles among the 4 with growth
    assert out[2]["p_rev"] == 20.0
    assert out[2]["p_mom"] == 20.0


def test_own_score_v4_needs_at_least_four_of_five():
    out = grp.own_score_v4(_five_row_fixture())
    assert out[4]["score"] is None, "只有 3/5 百分位有值，score 必須是 None"


def test_own_score_v4_fcf_ni_exemption_when_incremental_roic_high():
    out = grp.own_score_v4(_five_row_fixture())
    row1 = out[1]
    assert row1["q_fcf_ni_exempt"] is True
    # exempt -> p_q must equal the dilution-only percentile, not the fcf_ni/dilution average
    dilution_only_pct = row1["p_q"]
    # recompute what the *non*-exempt average would have been, to prove they differ
    non_exempt_rows = _five_row_fixture()
    non_exempt_rows[1]["incremental_roic_pct"] = 10.0   # below the 15 threshold -> not exempt
    out_non_exempt = grp.own_score_v4(non_exempt_rows)
    assert out_non_exempt[1]["q_fcf_ni_exempt"] is False
    assert out_non_exempt[1]["p_q"] != dilution_only_pct, (
        "免計 FCF/淨利時 p_q 應只看稀釋率分位，非豁免時應是兩者平均——兩者必須不同"
    )


def test_own_score_v4_accepts_full_stock_dicts_via_own_raw():
    """own_score_v4() 也接受完整 stock dict（非 own_raw() 形狀），自動套一次 own_raw()。"""
    stocks = [
        {"eps_fy1_fy3_cagr_pct": 20.0, "eps_rev_3m_pct": 5.0,
         "live_fpe_est": 20.0, "ma": {"mom_12_1_pct": 10.0}},
        {"eps_fy1_fy3_cagr_pct": 10.0, "eps_rev_3m_pct": 1.0,
         "live_fpe_est": 25.0, "ma": {"mom_12_1_pct": 5.0}},
    ]
    out = grp.own_score_v4(stocks)
    assert len(out) == 2
    assert out[0]["raw"]["g"] == 20.0


# ── grp_score() eligibility gates ────────────────────────────────────────────

def _stock(**kw):
    base = {
        "eps_fy1_fy3_cagr_pct": 25.0, "eps_rev_3m_pct": 5.0,
        "roic": 20.0, "fcf": 15.0, "live_fpe_est": 20.0,
        "ma": {"above_w52": True, "price": 100.0, "mom_12_1_pct": 10.0},
        "timing": {"dist_52w_high_pct": -10.0},
    }
    base.update(kw)
    return base


def test_growth_gate_durable_relaxation_to_10_pct():
    # 12% growth: fails the flat 15% bar when not durable...
    g = grp.grp_score(_stock(eps_fy1_fy3_cagr_pct=12.0, durable_5y=False))
    assert not g["pass"]
    assert g["g_min"] == grp.G_MIN_CAGR
    # ...but passes at the relaxed 10% bar when durable_5y=True
    g2 = grp.grp_score(_stock(eps_fy1_fy3_cagr_pct=12.0, durable_5y=True))
    assert g2["pass"]
    assert g2["g_min"] == grp.G_MIN_CAGR_DURABLE


def test_growth_gate_requires_true_three_year_cagr():
    # Single-year fallback (QGM supply rows) never satisfies the v4 growth gate,
    # even if the fallback number itself clears the bar.
    g = grp.grp_score(_stock(eps_fy1_fy3_cagr_pct=None, eps2y=40.0, durable_5y=True))
    assert not g["pass"]
    assert g["g_three_year"] is False or g["g_three_year"] is None


def test_revision_veto_uses_3m_primary_threshold():
    g = grp.grp_score(_stock(eps_rev_3m_pct=-6.0, eps_fy_next_revision_pct=5.0))
    assert g["veto"] and not g["pass"], "三月上修 <=-5% 必須否決，即使 FY+1 單月是正的"


def test_revision_veto_fy1_fallback_only_when_3m_missing():
    vetoed = grp.grp_score(_stock(eps_rev_3m_pct=None, eps_fy_next_revision_pct=-12.0))
    assert vetoed["veto"]
    not_vetoed = grp.grp_score(_stock(eps_rev_3m_pct=None, eps_fy_next_revision_pct=-8.0))
    assert not not_vetoed["veto"], "FY+1 fallback 否決線是 -10%，-8% 不該否決"
    # when eps_rev_3m_pct IS present, the FY+1 fallback must NOT be consulted at all
    ignored_fy1 = grp.grp_score(_stock(eps_rev_3m_pct=1.0, eps_fy_next_revision_pct=-50.0))
    assert not ignored_fy1["veto"], "3m 上修存在時，FY+1 fallback 不該被拿來否決"


def test_new_hard_vetoes():
    assert grp.grp_score(_stock(quality_veto_level="拒絕"))["veto"]
    assert grp.grp_score(_stock(decline_signal_light="⛔"))["veto"]
    fresh_avoid = grp.grp_score(_stock(dca_verdict="迴避", dd_age_days=30))
    assert fresh_avoid["veto"]
    stale_avoid = grp.grp_score(_stock(dca_verdict="迴避", dd_age_days=200))
    assert not stale_avoid["veto"], "超過 180 天的舊迴避裁決不否決"


def test_overheated_and_peak_are_not_eligibility_gates():
    overheated = grp.grp_score(_stock(ma={"above_w52": True, "price": 100.0, "mom_12_1_pct": 200.0},
                                       timing={"dist_52w_high_pct": -10.0}))
    assert overheated["overheated"] is True
    assert overheated["pass"], "過熱不擋資格，只排除核心候選（由呼叫端的 core_candidate 判斷）"

    peak = grp.grp_score(_stock(roic_vs_5y_x=2.0))
    assert peak["peak"] is True
    assert peak["pass"], "頂點純顯示，不擋資格"


def test_overheat_fallback_to_r26_when_mom_missing():
    hot = grp.grp_score(_stock(ma={"above_w52": True, "price": 100.0, "mom_12_1_pct": None}, _r26=90.0))
    assert hot["overheated"] is True
    cool = grp.grp_score(_stock(ma={"above_w52": True, "price": 100.0, "mom_12_1_pct": None}, _r26=50.0))
    assert cool["overheated"] is False
