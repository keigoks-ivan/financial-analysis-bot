"""Unit tests for scripts/engine/build_arena.py's monthly-rotation engine.

v5 NOTE (2026-09-17, see knowledge/rule_ledger.md "v5 席位引擎" row and
engine/grp.py 檔頭 v5 段第 3 點): this file originally covered the v4 engine's
select_fresh_roster()/hard_veto_v4()/rotate_roster() (core AND satellite,
core_candidate-filtered). v5 removed the satellite track entirely — the
"waiting pool" (former satellites) is recomputed fresh every run from the
current pool ranking, with no persisted roster state, no eviction/backfill
machinery of its own, and no "core_candidate" concept (the pool itself IS the
full eligibility+durable filter, so pool rank is the only judgment left).
Only the core-seat rotation still needs stateful monthly-cadence logic, so
this file was rewritten (not deleted) to test the v5 shapes:
  - select_fresh_roster_v5(): top-N of an already-pool-sorted list, no filter
  - hard_veto_v5(): the v4 six conditions + high_short_interest as a 7th
    (v5 upgraded high SI from "core-candidacy exclusion" to "full eligibility
    exclusion", so an incumbent core seat that turns high-SI must now be
    evicted immediately too, not just quietly demoted to a satellite seat
    that no longer exists)
  - rotate_roster(): same monthly-cadence contract as v4 (bootstrap vs.
    same-month carry-forward-with-hard-veto-eviction-and-backfill), but
    signature/return shape dropped everything "sat" (single `prev_core_roster`
    param in, single `"core"` key out — `"filled"` entries still carry a
    "core" track label for backward format compat with the v4 ledger shape,
    but there is only one track now)

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
    hard_veto_v5, rotate_roster, select_fresh_roster_v5,
)


def _row(ticker, score, veto=False, cap_ok=True, high_si=False):
    return {
        "ticker": ticker, "score": score,
        "grp": {"veto_dd_avoid": veto, "veto_quality_reject": False,
                "veto_decline": False, "veto_revision": False,
                "veto_high_short_interest": high_si},
        "cap_ok": cap_ok,
    }


def _pool_fixture():
    # Sorted by (whatever pool key produced this order — grp.pool_sort_key()
    # in production), as build_arena.main() would hand it to rotate_roster().
    return [_row("A", 90), _row("B", 80), _row("C", 70), _row("D", 60),
            _row("E", 50), _row("F", 40), _row("G", 30), _row("H", 20)]


# ── select_fresh_roster_v5() ──────────────────────────────────────────────

def test_select_fresh_roster_v5_takes_top_n_of_pool_no_extra_filter():
    pool = _pool_fixture()
    assert select_fresh_roster_v5(pool, core_slots=2) == ["A", "B"]
    assert select_fresh_roster_v5(pool, core_slots=5) == ["A", "B", "C", "D", "E"]


# ── hard_veto_v5() ────────────────────────────────────────────────────────

def test_hard_veto_v5_seven_conditions():
    assert hard_veto_v5({"grp": {"veto_dd_avoid": True}}) == "DD 迴避"
    assert hard_veto_v5({"grp": {"veto_quality_reject": True}}) == "體質拒絕"
    assert hard_veto_v5({"grp": {"veto_decline": True}}) == "衰退 ⛔"
    assert hard_veto_v5({"grp": {"veto_revision": True}}) == "三月上修 ≤ −5"
    assert hard_veto_v5({"grp": {"veto_high_short_interest": True}}) == "融券占流通股比 >10%"
    assert hard_veto_v5({"grp": {}, "cap_ok": False}) == "市值不足"
    assert hard_veto_v5({"grp": {}}, w52_fail_streak=2) == "連續兩週跌破 52 週線"


def test_hard_veto_v5_none_when_clean():
    assert hard_veto_v5({"grp": {}, "cap_ok": True}, w52_fail_streak=0) is None
    assert hard_veto_v5({"grp": {}, "cap_ok": True}, w52_fail_streak=1) is None, (
        "一週跌破 52 週線不夠，門檻是連續 2 次"
    )


def test_hard_veto_v5_revision_label_uses_earnings_anchor_when_present():
    assert hard_veto_v5({"grp": {"veto_revision": True, "rev_anchor": "earnings"}}) == \
        "財報後上修 ≤ −5"


# ── rotate_roster(): monthly cadence, core-only ──────────────────────────

def test_rotate_roster_bootstrap_does_full_reselect():
    pool = _pool_fixture()
    r = rotate_roster("2026-09", None, None, pool, {}, core_slots=2)
    assert r["rotated"] is True
    assert r["core"] == ["A", "B"]
    assert r["removed"] == [] and r["filled"] == []


def test_rotate_roster_same_month_carries_forward_unchanged():
    pool = _pool_fixture()
    r = rotate_roster("2026-09", "2026-09", ["A", "B"], pool, {}, core_slots=2)
    assert r["rotated"] is False
    assert r["core"] == ["A", "B"]
    assert r["removed"] == []


def test_rotate_roster_new_month_triggers_fresh_reselect_even_with_prev_roster():
    pool = _pool_fixture()
    r = rotate_roster("2026-10", "2026-09", ["A", "B"], pool, {}, core_slots=2)
    assert r["rotated"] is True


# ── rotate_roster(): the core grace-period behavior ──────────────────────

def test_rotate_roster_soft_gate_failure_is_carried_forward_not_evicted():
    """v5's whole point (unchanged from v4): mid-month, only hard_veto_v5's
    enumerated conditions evict a seat. A name that simply falls out of the
    pool this run (e.g. growth or quality gate slipped, or revision dropped
    below the +5% pool threshold) but has NO hard veto must still be carried
    forward — this is what "只有硬否決能換人" means in the spec."""
    pool = _pool_fixture()
    all_by_ticker = {r["ticker"]: r for r in pool}
    # B drops out of the pool (e.g. revision fell below +5%, or failed growth
    # gate) but carries no hard veto.
    all_by_ticker["B"] = _row("B", 80, veto=False)
    pool_without_b = [r for r in pool if r["ticker"] != "B"]
    r = rotate_roster("2026-09", "2026-09", ["A", "B"], pool_without_b, {},
                      core_slots=2, all_by_ticker=all_by_ticker)
    assert r["core"] == ["A", "B"], "B 沒有硬否決，即使跌出池也該沿用"
    assert r["removed"] == []


def test_rotate_roster_hard_veto_evicts_and_backfills_from_pool():
    pool = _pool_fixture()
    all_by_ticker = {r["ticker"]: r for r in pool}
    all_by_ticker["B"] = _row("B", 80, veto=True)   # hard veto this time
    pool_without_b = [r for r in pool if r["ticker"] != "B"]
    r = rotate_roster("2026-09", "2026-09", ["A", "B"], pool_without_b, {},
                      core_slots=2, all_by_ticker=all_by_ticker)
    assert ("B", "DD 迴避") in r["removed"]
    assert r["core"] == ["A", "C"], "空位由池中下一名（C）遞補"
    assert ("core", "C") in r["filled"]


def test_rotate_roster_high_short_interest_evicts_incumbent_core_seat():
    """v5-specific: a core seat that turns high-short-interest must be evicted
    immediately (no satellite track left to quietly demote it to, unlike v4.1
    where high SI only barred NEW core candidacy but didn't evict an
    incumbent)."""
    pool = _pool_fixture()
    all_by_ticker = {r["ticker"]: r for r in pool}
    all_by_ticker["A"] = _row("A", 90, high_si=True)
    r = rotate_roster("2026-09", "2026-09", ["A", "B"], pool, {},
                      core_slots=2, all_by_ticker=all_by_ticker)
    assert ("A", "融券占流通股比 >10%") in r["removed"]
    assert "A" not in r["core"]


def test_rotate_roster_ticker_delisted_entirely_is_removed():
    pool = _pool_fixture()
    all_by_ticker = {r["ticker"]: r for r in pool}
    r = rotate_roster("2026-09", "2026-09", ["A", "Z"], pool, {},
                      core_slots=2, all_by_ticker=all_by_ticker)
    assert any(t == "Z" for t, _why in r["removed"])
    assert "Z" not in r["core"]


def test_rotate_roster_w52_streak_evicts_after_two_consecutive_runs():
    pool = _pool_fixture()
    all_by_ticker = {r["ticker"]: r for r in pool}
    r1 = rotate_roster("2026-09", "2026-09", ["A", "B"], pool, {"B": 1},
                       core_slots=2, all_by_ticker=all_by_ticker)
    assert r1["core"] == ["A", "B"], "streak=1 還不夠，先容忍一週"
    r2 = rotate_roster("2026-09", "2026-09", ["A", "B"], pool, {"B": 2},
                       core_slots=2, all_by_ticker=all_by_ticker)
    assert "B" not in r2["core"]
    assert ("B", "連續兩週跌破 52 週線") in r2["removed"]


def test_rotate_roster_daily_rerun_without_ledger_is_idempotent_pure_function():
    """The `--daily`/`--lamp-only` mode (see build_arena.py 檔頭 --daily 段) is
    just "call the same code path without persisting to the ledger" — there is
    no separate code path to test here. This test documents that guarantee at
    the pure-function level: calling rotate_roster() twice with the exact same
    inputs (as a --daily rerun would, since it never advances
    last_rotation_month/prev_core_roster) returns identical results both times."""
    pool = _pool_fixture()
    all_by_ticker = {r["ticker"]: r for r in pool}
    r1 = rotate_roster("2026-09", "2026-09", ["A", "B"], pool, {},
                       core_slots=2, all_by_ticker=all_by_ticker)
    r2 = rotate_roster("2026-09", "2026-09", ["A", "B"], pool, {},
                       core_slots=2, all_by_ticker=all_by_ticker)
    assert r1 == r2
