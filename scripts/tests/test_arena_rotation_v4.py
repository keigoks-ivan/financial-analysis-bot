"""Unit tests for scripts/engine/build_arena.py's v4 monthly-rotation engine
(2026-09-17 席位引擎 v4 — see knowledge/rule_ledger.md "v4 席位引擎" row):
rotate_roster() / select_fresh_roster() / hard_veto_v4().

Pure-function level only — hand-made row fixtures, no disk/network reads
(no dd-screener latest.json, no arena-ledger.json). Same style as
scripts/tests/test_fundamental_gates.py.
"""
from __future__ import annotations

from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from engine.build_arena import (  # noqa: E402
    hard_veto_v4, rotate_roster, select_fresh_roster,
)


def _row(ticker, score, core_candidate=True, veto=False, cap_ok=True):
    return {
        "ticker": ticker, "score": score, "core_candidate": core_candidate,
        "grp": {"veto_dd_avoid": veto, "veto_quality_reject": False,
                "veto_decline": False, "veto_revision": False},
        "cap_ok": cap_ok,
    }


def _ranked_fixture():
    # Sorted by score desc, as apply_own_score_v4() would produce.
    return [
        _row("A", 90), _row("B", 80), _row("C", 70),
        _row("D", 60, core_candidate=False), _row("E", 50, core_candidate=False),
        _row("F", 40), _row("G", 30, core_candidate=False), _row("H", 20, core_candidate=False),
    ]


# ── select_fresh_roster() ─────────────────────────────────────────────────

def test_select_fresh_roster_core_from_candidates_sat_from_remainder():
    ranked = _ranked_fixture()
    fresh = select_fresh_roster(ranked, core_slots=2, sat_slots=2)
    # Core: top 2 core_candidate=True names by score -> A, B (C is 3rd candidate, misses out)
    assert fresh["core"] == ["A", "B"]
    # Sat: top 2 of *everyone else* by score, including non-core-candidates -> C, D
    assert fresh["sat"] == ["C", "D"]


# ── hard_veto_v4() ────────────────────────────────────────────────────────

def test_hard_veto_v4_six_conditions():
    assert hard_veto_v4({"grp": {"veto_dd_avoid": True}}) == "DD 迴避"
    assert hard_veto_v4({"grp": {"veto_quality_reject": True}}) == "體質拒絕"
    assert hard_veto_v4({"grp": {"veto_decline": True}}) == "衰退 ⛔"
    assert hard_veto_v4({"grp": {"veto_revision": True}}) == "三月上修 ≤ −5"
    assert hard_veto_v4({"grp": {}, "cap_ok": False}) == "市值不足"
    assert hard_veto_v4({"grp": {}}, w52_fail_streak=2) == "連續兩週跌破 52 週線"


def test_hard_veto_v4_none_when_clean():
    assert hard_veto_v4({"grp": {}, "cap_ok": True}, w52_fail_streak=0) is None
    assert hard_veto_v4({"grp": {}, "cap_ok": True}, w52_fail_streak=1) is None, (
        "一週跌破 52 週線不夠，門檻是連續 2 次"
    )


# ── rotate_roster(): monthly cadence ─────────────────────────────────────

def test_rotate_roster_bootstrap_does_full_reselect():
    ranked = _ranked_fixture()
    r = rotate_roster("2026-09", None, None, ranked, {}, core_slots=2, sat_slots=2)
    assert r["rotated"] is True
    assert r["core"] == ["A", "B"]
    assert r["sat"] == ["C", "D"]
    assert r["removed"] == [] and r["filled"] == []


def test_rotate_roster_same_month_carries_forward_unchanged():
    ranked = _ranked_fixture()
    prev = {"core": ["A", "B"], "sat": ["C", "D"]}
    r = rotate_roster("2026-09", "2026-09", prev, ranked, {}, core_slots=2, sat_slots=2)
    assert r["rotated"] is False
    assert r["core"] == ["A", "B"]
    assert r["sat"] == ["C", "D"]
    assert r["removed"] == []


def test_rotate_roster_new_month_triggers_fresh_reselect_even_with_prev_roster():
    ranked = _ranked_fixture()
    prev = {"core": ["A", "B"], "sat": ["C", "D"]}
    r = rotate_roster("2026-10", "2026-09", prev, ranked, {}, core_slots=2, sat_slots=2)
    assert r["rotated"] is True


# ── rotate_roster(): the core grace-period behavior ──────────────────────

def test_rotate_roster_soft_gate_failure_is_carried_forward_not_evicted():
    """v4's whole point: mid-month, only the six enumerated hard vetoes evict a
    seat. A name that simply falls out of the ELIGIBLE/ranked pool this run
    (e.g. growth or quality gate slipped) but has NO hard veto must still be
    carried forward — this is what "只有硬否決能換人" means in the spec."""
    ranked = _ranked_fixture()
    prev = {"core": ["A", "B"], "sat": ["C", "D"]}
    all_by_ticker = {r["ticker"]: r for r in ranked}
    # B drops out of `ranked` (e.g. failed growth gate this week) but carries no veto.
    all_by_ticker["B"] = _row("B", 80, veto=False)
    ranked_without_b = [r for r in ranked if r["ticker"] != "B"]
    r = rotate_roster("2026-09", "2026-09", prev, ranked_without_b, {},
                      core_slots=2, sat_slots=2, all_by_ticker=all_by_ticker)
    assert r["core"] == ["A", "B"], "B 沒有硬否決，即使跌出 ranked 也該沿用"
    assert r["removed"] == []


def test_rotate_roster_hard_veto_evicts_and_backfills_from_eligible_pool():
    ranked = _ranked_fixture()
    prev = {"core": ["A", "B"], "sat": ["C", "D"]}
    all_by_ticker = {r["ticker"]: r for r in ranked}
    all_by_ticker["B"] = _row("B", 80, veto=True)   # hard veto this time
    ranked_without_b = [r for r in ranked if r["ticker"] != "B"]
    r = rotate_roster("2026-09", "2026-09", prev, ranked_without_b, {},
                      core_slots=2, sat_slots=2, all_by_ticker=all_by_ticker)
    assert ("B", "DD 迴避") in r["removed"]
    # C is already seated as a satellite -> can't double-fill; next core_candidate is F.
    assert r["core"] == ["A", "F"]
    assert r["sat"] == ["C", "D"]
    assert ("core", "F") in r["filled"]


def test_rotate_roster_ticker_delisted_entirely_is_removed():
    ranked = _ranked_fixture()
    prev = {"core": ["A", "Z"], "sat": ["C", "D"]}   # Z was seated but no longer exists anywhere
    all_by_ticker = {r["ticker"]: r for r in ranked}
    r = rotate_roster("2026-09", "2026-09", prev, ranked, {}, core_slots=2, sat_slots=2,
                      all_by_ticker=all_by_ticker)
    assert any(t == "Z" for t, _why in r["removed"])
    assert "Z" not in r["core"]


def test_rotate_roster_w52_streak_evicts_after_two_consecutive_runs():
    ranked = _ranked_fixture()
    prev = {"core": ["A", "B"], "sat": ["C", "D"]}
    all_by_ticker = {r["ticker"]: r for r in ranked}
    r1 = rotate_roster("2026-09", "2026-09", prev, ranked, {"B": 1},
                       core_slots=2, sat_slots=2, all_by_ticker=all_by_ticker)
    assert r1["core"] == ["A", "B"], "streak=1 還不夠，先容忍一週"
    r2 = rotate_roster("2026-09", "2026-09", prev, ranked, {"B": 2},
                       core_slots=2, sat_slots=2, all_by_ticker=all_by_ticker)
    assert "B" not in r2["core"]
    assert ("B", "連續兩週跌破 52 週線") in r2["removed"]
