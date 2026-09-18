"""Unit tests for scripts/engine/grp.py's v5 additions (2026-09-17 席位引擎 v5 overhaul
— "品質派 ∩ 獲利上修 ∩ 突破還原權息歷史新高", see knowledge/rule_ledger.md "v5 席位
引擎" row and grp.py 檔頭 v5 段):

  - durable_5y_v5(): the consistency-not-average durable rule (QGM stability >=75,
    OR Koyfin 5y-avg AND 3y-avg AND current ROIC all >=15)
  - in_pool() / pool_sort_key(): the pool condition (revision >= +5%) and the
    revision-only ranking with implied_growth_pct / EY tie-breaks
  - timing_lamp(): the v5 ATH-distance truth table, incl. hot-requires-green-level-
    proximity (the fuller table lives in test_grp_v4.py alongside the v4 tests it
    replaced; this file adds the durable/pool-shaped cases that don't fit there)
  - grp_score(): durable-as-eligibility-gate and high-short-interest-as-full-
    exclusion (the veto_high_short_interest field consumed by
    build_arena.hard_veto_v5())
  - valuation_gate() (v5.1, 2026-09-18 owner decision — see knowledge/rule_ledger.md
    "v5.1 估值閘" row and grp.py 檔頭 v5.1 段): PEG >2.0 OR PE-NTM-vs-5Y-avg >1.5 →
    red → not eligible; both missing is NOT a veto (⚪); one missing is judged on
    the other alone. This is an eligibility/pool gate, not a mid-month hard veto —
    it deliberately has no test here asserting it's excluded from
    build_arena.hard_veto_v5()'s seven conditions (that's covered by
    test_arena_rotation_v4.py's exhaustive hard_veto_v5 test + the build_arena.py
    comment at that function).

v4 own_score_v4()/own_raw() (percentile ranking, base-effect, cyclical guard) are
unchanged in v5 — see test_grp_v4.py, not duplicated here.

Hand-made inputs only — no network, no disk reads of real dd-screener/lamp data.
"""
from __future__ import annotations

from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from engine import grp  # noqa: E402


# ── durable_5y_v5(): consistency, not average ────────────────────────────────

def test_durable_v5_qgm_path_alone():
    assert grp.durable_5y_v5({"qgm_roic_5y_stability_pct": 80.0}) == (True, "qgm")


def test_durable_v5_qgm_path_below_threshold():
    assert grp.durable_5y_v5({"qgm_roic_5y_stability_pct": 74.9}) == (False, "qgm")


def test_durable_v5_koyfin_path_requires_all_three_above_15():
    s = {"roic_5y_avg_pct": 20.0, "roic_3y_avg_pct": 18.0, "roic": 16.0}
    assert grp.durable_5y_v5(s) == (True, "koyfin-xlsx")


def test_durable_v5_koyfin_path_fails_when_5y_avg_masks_faded_3y_or_current():
    """v4 only looked at the 5y average — a one-off profit spike could push it
    over 15% while the 3y average / current ROIC had already faded. v5's whole
    point is to catch this."""
    s = {"roic_5y_avg_pct": 20.0, "roic_3y_avg_pct": 12.0, "roic": 16.0}
    assert grp.durable_5y_v5(s) == (False, "koyfin-xlsx"), "三年平均 12% < 15% → 不耐久"
    s2 = {"roic_5y_avg_pct": 20.0, "roic_3y_avg_pct": 18.0, "roic": 10.0}
    assert grp.durable_5y_v5(s2) == (False, "koyfin-xlsx"), "現值 10% < 15% → 不耐久"


def test_durable_v5_koyfin_path_incomplete_data_is_none_not_false():
    s = {"roic_5y_avg_pct": 20.0, "roic_3y_avg_pct": 18.0}   # missing current roic
    assert grp.durable_5y_v5(s) == (None, None), "三者缺一無法判定該路徑，兩路徑皆缺才是 (None, None)"


def test_durable_v5_or_logic_qgm_rescues_failed_koyfin():
    s = {"roic_5y_avg_pct": 20.0, "roic_3y_avg_pct": 12.0, "roic": 16.0,
         "qgm_roic_5y_stability_pct": 90.0}
    assert grp.durable_5y_v5(s) == (True, "qgm"), "Koyfin 路徑不過但 QGM 路徑過 → OR 邏輯仍耐久"


def test_durable_v5_both_missing_is_none():
    assert grp.durable_5y_v5({}) == (None, None)


# ── in_pool() / pool_sort_key(): pool condition + revision-only ranking ──────

def test_in_pool_threshold():
    assert grp.in_pool(5.0) is True, "剛好 +5% 應進池（>= 邊界）"
    assert grp.in_pool(4.9) is False
    assert grp.in_pool(None) is False
    assert grp.in_pool(-3.0) is False


def test_pool_sort_key_ranks_by_revision_desc():
    rows = [{"rev": 10.0}, {"rev": 30.0}, {"rev": 20.0}]
    ranked = sorted(rows, key=lambda r: grp.pool_sort_key(r["rev"]))
    assert [r["rev"] for r in ranked] == [30.0, 20.0, 10.0]


def test_pool_sort_key_tie_break_implied_growth_then_ey():
    a = {"rev": 10.0, "ig": 25.0, "ey": 3.0}
    b = {"rev": 10.0, "ig": 30.0, "ey": 1.0}   # same rev, higher implied_growth wins
    c = {"rev": 10.0, "ig": 30.0, "ey": 5.0}   # same rev+ig, higher EY wins
    rows = [a, b, c]
    ranked = sorted(rows, key=lambda r: grp.pool_sort_key(r["rev"], r["ig"], r["ey"]))
    assert ranked[0] is c, "同上修、同 implied_growth → EY 高者優先"
    assert ranked[1] is b
    assert ranked[2] is a, "implied_growth 25 < 30 → 排最後"


def test_pool_sort_key_none_values_sort_last():
    rows = [{"rev": None}, {"rev": 5.0}, {"rev": -2.0}]
    ranked = sorted(rows, key=lambda r: grp.pool_sort_key(r["rev"]))
    assert [r["rev"] for r in ranked] == [5.0, -2.0, None], "上修缺值排最後，不是排最前"


# ── grp_score(): durable-as-eligibility-gate + full SI exclusion (v5) ───────

def _v5_stock(**kw):
    base = {
        "eps_fy1_fy3_cagr_pct": 25.0, "eps_rev_3m_pct": 8.0,
        "roic": 20.0, "fcf": 15.0, "live_fpe_est": 20.0,
        "ma": {"above_w52": True, "price": 100.0, "mom_12_1_pct": 10.0,
               "dist_ath_pct": -2.0},
        # dist_52w_high_pct feeds the (unchanged in v5) P-gate/p_label — a
        # separate concept from ma.dist_ath_pct, which only feeds timing_lamp().
        "timing": {"vs_200ma_pct": 5.0, "dist_52w_high_pct": -2.0},
        "durable_5y": True,
    }
    base.update(kw)
    return base


def test_durable_required_for_eligibility_false():
    g = grp.grp_score(_v5_stock(durable_5y=False))
    assert not g["pass"], "v5：不耐久整體排除，沒有衛星軌可以退"


def test_durable_required_for_eligibility_none():
    g = grp.grp_score(_v5_stock(durable_5y=None))
    assert not g["pass"], "v5：耐久資料缺，資格從嚴不通過"


def test_durable_true_with_everything_else_clean_passes():
    g = grp.grp_score(_v5_stock())
    assert g["pass"]


def test_pool_membership_is_separate_from_eligibility():
    """grp_score()['pass'] is eligibility only — the +5% pool threshold is an
    additional filter the caller (build_arena.main()) applies via grp.in_pool()
    on top of `pass`, not baked into `pass` itself."""
    g = grp.grp_score(_v5_stock(eps_rev_3m_pct=2.0))   # positive revision, but < 5%
    assert g["pass"], "低於 5% 的正向上修仍是 ELIGIBLE（只是不進池）"
    assert not grp.in_pool(g["rev_used_pct"]), "但不滿足池門檻"


# ── valuation_gate() (v5.1, 2026-09-18 owner decision — see knowledge/rule_ledger.md
# "v5.1 估值閘" row and grp.py 檔頭 v5.1 段): PEG >2.0 OR PE-NTM-vs-5Y-avg >1.5 → red;
# both missing is NOT a veto (⚪); one missing is judged on the other alone ────────────

def test_valuation_gate_red_by_peg():
    g = grp.valuation_gate({"live_peg": 2.5})
    assert g["light"] == "🔴"
    assert g["red_by"] == ["peg"]
    assert g["peg"] == 2.5 and g["peg_source"] == "live"
    assert g["why"] == "估值閘紅燈（PEG 2.5 > 2.0）"


def test_valuation_gate_red_by_multiple():
    g = grp.valuation_gate({"pe_vs_5y_x": 1.9})
    assert g["light"] == "🔴"
    assert g["red_by"] == ["pe_vs_5y"]
    assert g["pe_vs_5y_x"] == 1.9
    assert g["why"] == "估值閘紅燈（PE 相對五年均倍數 1.90x > 1.75x）"


def test_valuation_gate_both_missing_is_gray_not_a_veto():
    g = grp.valuation_gate({})
    assert g["light"] == "⚪"
    assert g["red_by"] == []
    assert g["peg"] is None and g["pe_vs_5y_x"] is None
    assert g["why"] is not None, "缺值仍要記錄一句話（why），只是不當否決"


def test_valuation_gate_live_peg_takes_precedence_over_peg():
    g = grp.valuation_gate({"live_peg": 1.0, "peg": 5.0})
    assert g["peg"] == 1.0 and g["peg_source"] == "live", "live_peg 優先，即使 peg（Koyfin）本身會紅"
    assert g["light"] == "🟢"


def test_valuation_gate_one_missing_judged_on_the_other_alone():
    # PEG 缺（live_peg／peg 皆無），只剩 multiple——用 multiple 單獨判定，不因缺一個
    # 就補灰燈。這裡刻意選一個「過關」的 multiple，跟「red by multiple」測試（PEG
    # 缺、multiple 紅）互補，證明「缺一個」本身不影響另一個的判定方向。
    g = grp.valuation_gate({"pe_vs_5y_x": 1.2})
    assert g["light"] == "🟢"
    assert g["peg"] is None and g["pe_vs_5y_x"] == 1.2

    # multiple 缺，只剩 PEG——同理用 PEG 單獨判定。
    g2 = grp.valuation_gate({"peg": 1.5})
    assert g2["light"] == "🟢"
    assert g2["peg"] == 1.5 and g2["pe_vs_5y_x"] is None


def test_grp_score_pass_flips_false_on_valuation_red_with_all_other_gates_clean():
    """重用 _v5_stock()（其餘四道資格閘：成長／位置／上修否決／耐久皆過）——只加
    估值閘紅燈，pass 應整體翻為 False，veto_valuation=True，why 帶新句型。"""
    g = grp.grp_score(_v5_stock())
    assert g["pass"], "sanity：不動估值欄位時，既有 fixture 仍應過閘（missing→⚪ 不否決）"

    g_red = grp.grp_score(_v5_stock(live_peg=2.5))
    assert not g_red["pass"], "估值閘紅燈應讓整體資格翻為 False"
    assert g_red["veto_valuation"] is True
    assert g_red["valuation"]["light"] == "🔴"
    assert "估值閘紅燈（PEG 2.5 > 2.0）" in g_red["why"]
