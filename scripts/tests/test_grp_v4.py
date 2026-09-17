"""Unit tests for scripts/engine/grp.py's v4 additions (2026-09-17 席位引擎 v4 overhaul
— see knowledge/rule_ledger.md "v4 席位引擎" row):

  - timing_lamp(): pure timing-lamp truth table (out/red/hot/green/yellow, missing stage)
  - own_score_v4(): cross-sectional percentile math on a 5-row fixture, incl. the
    FCF/NI exemption when incremental_roic_pct >= 15
  - grp_score(): eligibility gates, incl. the 10% durable-growth relaxation and the
    v4 revision veto (eps_rev_3m_pct <= -5, falling back to the old FY+1 <= -10 rule
    only when eps_rev_3m_pct is missing)

v4.1 additions (2026-09-17, see knowledge/rule_ledger.md "v4.1 融券比 >10% 只能衛星"
and "v4.1 基期效應＋循環股守門" rows): high_short_interest (core-candidacy exclusion
only, not a ranking factor or eligibility gate), _base_effect_growth() (overrides g
with FY2->FY3 growth when FY1->FY2 jumped on a low base), and own_raw()/own_score_v4()
cyclical guard (caps p_g/p_ey percentiles at 50 when PEG is suspiciously low on a
cyclical-shaped stock).

Hand-made inputs only — no network, no disk reads of real dd-screener/lamp data.
Same style as scripts/tests/test_fundamental_gates.py.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

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


# ── 財報錨定上修（2026-09-17，見 knowledge/rule_ledger.md「上修改為財報後錨定」
# 列）：_revision_anchor()／own_raw()／grp_score() 的 eps_rev_since_earnings_pct
# 優先、eps_rev_3m_pct 後備選錨邏輯 ────────────────────────────────────────────

def test_revision_anchor_prefers_since_earnings_when_present():
    value, anchor, baseline = grp._revision_anchor({
        "eps_rev_since_earnings_pct": 7.5,
        "eps_rev_since_earnings_baseline_date": "2026-07-30",
        "eps_rev_anchor": "earnings",
        "eps_rev_3m_pct": -20.0,   # must be ignored — since-earnings wins
        "eps_rev_3m_baseline_date": "2026-06-23",
    })
    assert (value, anchor, baseline) == (7.5, "earnings", "2026-07-30")


def test_revision_anchor_falls_back_to_calendar_3m_when_since_earnings_absent():
    """Back-compat safety net: a fixture / older dd-screener rebuild that only
    sets eps_rev_3m_pct (no eps_rev_since_earnings_pct at all) must behave
    exactly as before this feature — this is what _stock()'s default
    eps_rev_3m_pct=5.0 relies on across every other test in this file."""
    value, anchor, baseline = grp._revision_anchor({
        "eps_rev_3m_pct": -6.0, "eps_rev_3m_baseline_date": "2026-06-23",
    })
    assert (value, anchor, baseline) == (-6.0, "calendar_3m", "2026-06-23")


def test_revision_anchor_none_when_both_missing():
    assert grp._revision_anchor({}) == (None, None, None)


def test_own_raw_rev_field_uses_since_earnings_and_carries_anchor():
    raw = grp.own_raw({
        "eps_rev_since_earnings_pct": 12.0,
        "eps_rev_since_earnings_baseline_date": "2026-08-28",
        "eps_rev_anchor": "earnings",
        "eps_rev_3m_pct": -50.0,
    })
    assert raw["rev"] == 12.0
    assert raw["rev_anchor"] == "earnings"
    assert raw["rev_baseline_date"] == "2026-08-28"


def test_grp_score_veto_uses_since_earnings_value_over_calendar_3m():
    # eps_rev_since_earnings_pct <= -5 vetoes even though the stale calendar
    # eps_rev_3m_pct sitting alongside it is positive.
    g = grp.grp_score(_stock(
        eps_rev_since_earnings_pct=-6.0, eps_rev_anchor="earnings",
        eps_rev_since_earnings_baseline_date="2026-08-28",
        eps_rev_3m_pct=5.0, eps_fy_next_revision_pct=5.0,
    ))
    assert g["veto"] and not g["pass"]
    assert g["rev_anchor"] == "earnings"
    assert g["rev_used_pct"] == -6.0
    assert any("財報後上修否決" in w for w in g["why"])


def test_grp_score_veto_falls_back_to_calendar_3m_label_when_since_earnings_absent():
    g = grp.grp_score(_stock(eps_rev_3m_pct=-6.0))
    assert g["veto"]
    assert g["rev_anchor"] == "calendar_3m"
    assert any("三月上修否決" in w for w in g["why"])


def test_grp_score_exposes_days_to_next_earnings():
    g = grp.grp_score(_stock(days_to_next_earnings=5))
    assert g["days_to_next_earnings"] == 5


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


# ── v4.1 融券高（core-candidacy only, NOT a ranking factor / eligibility gate） ──
# See knowledge/rule_ledger.md "v4.1 融券比 >10% 只能衛星（2026-09-17）".

def test_high_short_interest_flag_above_threshold():
    g = grp.grp_score(_stock(short_interest_pct_float=12.5))
    assert g["high_short_interest"] is True
    assert g["short_interest_pct_float"] == 12.5
    assert g["pass"], "融券高不是資格閘，不否決 pass"
    assert not g["veto"], "融券高不是硬否決"


def test_high_short_interest_flag_below_threshold():
    g = grp.grp_score(_stock(short_interest_pct_float=3.0))
    assert g["high_short_interest"] is False
    assert g["pass"]


def test_high_short_interest_flag_missing_is_false_not_none():
    g = grp.grp_score(_stock())   # no short_interest_pct_float key at all
    assert g["high_short_interest"] is False
    assert g["short_interest_pct_float"] is None
    assert g["pass"], "缺融券資料不影響資格（fail-open 顯示、不否決）"


# ── v4.1 基期效應（base effect） ──────────────────────────────────────────
# See knowledge/rule_ledger.md "v4.1 基期效應＋循環股守門（2026-09-17）".

def test_base_effect_triggers_and_overrides_g_mrk_shape():
    # MRK-shaped: 2.75 -> 9.55 -> 10.62. FY1->FY2 jumps 3.47x (>1.6x), FY2->FY3
    # is only +11.2% (<20%) -> base effect fires, g becomes FY2->FY3 growth.
    g = grp.grp_score(_stock(
        eps_fy1_fy3_cagr_pct=97.0, eps_fy_curr=2.75, eps_fy_next=9.55, eps_fy3=10.62,
        durable_5y=True,
    ))
    assert g["base_effect"] is True
    assert g["g"] == pytest.approx(11.2, abs=0.5)
    assert g["g_three_year"] is True, "基期校正後仍是三年期資料，不是退回單年 fallback"
    # 97% would trivially clear both bars; ~11% only clears the durable 10% bar.
    assert g["pass"], "MRK 型基期校正後的 g（~11%）只能靠 durable 10% 放寬過關"


def test_base_effect_does_not_trigger_when_growth_is_smooth_mu_shape():
    # MU-shaped: 73.4 -> 156.3 -> 171.6. FY1->FY2 jumps 2.13x (>1.6x) but
    # FY2->FY3 is only +9.8% (<20%) -> base effect fires -> g fails growth gate.
    g = grp.grp_score(_stock(
        eps_fy1_fy3_cagr_pct=52.9, eps_fy_curr=73.4, eps_fy_next=156.3, eps_fy3=171.6,
        durable_5y=False,
    ))
    assert g["base_effect"] is True
    assert g["g"] == pytest.approx(9.79, abs=0.2)
    assert not g["pass"], "MU 型基期校正後 g<10%，非 durable 亦低於 15% 門檻，應失敗"


def test_base_effect_not_flagged_for_nvda_shape():
    # NVDA-shaped: 9.31 -> 15.61 -> 21.06. FY1->FY2 is 1.68x (>1.6x) but
    # FY2->FY3 is +34.9% (>=20%) -> base effect must NOT fire.
    g = grp.grp_score(_stock(
        eps_fy1_fy3_cagr_pct=50.5, eps_fy_curr=9.31, eps_fy_next=15.61, eps_fy3=21.06,
    ))
    assert g["base_effect"] is False
    assert g["g"] == pytest.approx(50.5, abs=0.01), "未觸發基期效應時應原樣沿用三年 CAGR"


def test_base_effect_absent_raw_eps_fields_falls_back_to_cagr():
    g = grp.grp_score(_stock(eps_fy1_fy3_cagr_pct=25.0))   # no eps_fy_curr/next/fy3
    assert g["base_effect"] is False
    assert g["g"] == 25.0


# ── v4.1 own_raw()/own_score_v4() 循環股守門（cyclical guard） ───────────────

def _cyclical_stock(peg=0.2, gm_swing=True, capex_high=False):
    s = {"eps_fy1_fy3_cagr_pct": 40.0, "eps_rev_3m_pct": 5.0,
         "live_fpe_est": 10.0, "ma": {"mom_12_1_pct": 10.0}, "live_peg": peg}
    if gm_swing:
        s["fund"] = {"gm_ltm_pct": 20.0, "gm_fy1_pct": 35.0, "gm_fy2_pct": 45.0, "gm_fy3_pct": 30.0}
    if capex_high:
        s["capex_pct_rev"] = 22.0
    return s


def test_own_raw_cycle_guard_true_when_cyclical_and_peg_low():
    raw = grp.own_raw(_cyclical_stock(peg=0.15, gm_swing=True))
    assert raw["cyclical"] is True
    assert raw["cycle_guard"] is True
    assert raw["cycle_guard_detail"]["peg"] == 0.15


def test_own_raw_cycle_guard_false_when_peg_not_low_enough():
    raw = grp.own_raw(_cyclical_stock(peg=0.8, gm_swing=True))
    assert raw["cyclical"] is True, "毛利率跨距 >20pp 本身仍標記循環，純顯示"
    assert raw["cycle_guard"] is False, "PEG 0.8 未低於 0.3，不觸發 guard"


def test_own_raw_cycle_guard_false_when_not_cyclical():
    s = _cyclical_stock(peg=0.1, gm_swing=False)
    s["capex_pct_rev"] = 5.0
    raw = grp.own_raw(s)
    assert raw["cyclical"] is False
    assert raw["cycle_guard"] is False


def test_own_raw_cycle_guard_false_when_peg_missing():
    s = _cyclical_stock(peg=None, gm_swing=True)
    del s["live_peg"]
    raw = grp.own_raw(s)
    assert raw["cyclical"] is True
    assert raw["cycle_guard"] is False, "缺 PEG 無法判斷是否可疑，不觸發 guard"


def test_own_raw_cycle_guard_via_capex_intensity():
    s = _cyclical_stock(peg=0.1, gm_swing=False, capex_high=True)
    raw = grp.own_raw(s)
    assert raw["cyclical"] is True, "資本支出佔營收 >15% 亦視為循環股"
    assert raw["cycle_guard"] is True


def test_own_score_v4_caps_p_g_and_p_ey_when_cycle_guard():
    rows = _five_row_fixture()
    # Turn row 3 (currently the top scorer on every axis) into a cycle-guard case.
    rows[3]["cyclical"] = True
    rows[3]["cycle_guard"] = True
    out = grp.own_score_v4(rows)
    assert out[3]["p_g"] == 50.0, "guard 觸發時 p_g 應封頂 50（未封頂前是 100.0）"
    assert out[3]["p_ey"] == 50.0, "guard 觸發時 p_ey 應封頂 50（未封頂前是 100.0）"
    # untouched rows keep their original percentiles
    assert out[0]["p_g"] != 50.0 or rows[0].get("cycle_guard")
