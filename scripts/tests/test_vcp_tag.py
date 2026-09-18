"""Tests for VCP depth 1 (2026-09-18 — see notes/site-internal/root/
_seat_engine_v5_1_20260918.md §3 / knowledge/rule_ledger.md「VCP 深度 1」列):
tag-and-sort only, timing_lamp()/grp_score()/LAMP_ACTION untouched.

Three areas, matching the spec:
  (a) scripts/build_dd_screener.py::compute_vcp_tag() scope logic — far from
      ATH -> "far_from_ath" (skipped), too few/missing bars ->
      "insufficient_bars", enough bars -> "computed" (calls
      vcp_core.calc_vcp() and maps its fields straight through).
  (b) scripts/engine/build_arena.py::_group_waiting_pool_by_timing() — the
      🟡 group sorts vcp_tight=True first, ties keep the incoming
      (revision-desc) order; 🔴 group order is untouched.
  (c) scripts/engine/build_arena.py's 底部 cell text (_vcp_kind() /
      _bottom_ascii_cell() / _bottom_cell_html()) for each scope/gate case.

No network anywhere — all OHLCV data here is synthetic pandas Series.
"""
from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as dd_screener  # noqa: E402
import vcp_core  # noqa: E402
from engine import build_arena  # noqa: E402
from engine.grp import ATH_RED_DIST  # noqa: E402


def _synthetic_ohlcv(n=300, seed=0):
    """A deterministic, network-free daily OHLCV series long enough to clear
    VCP_MIN_BARS. Shape doesn't matter for the scope tests below (they only
    care about bar count and that calc_vcp()'s fields get mapped through
    verbatim, not about which vcp_gate the pattern happens to earn) — a mild
    random walk is enough."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-01-01", periods=n, freq="B")
    steps = rng.normal(0.05, 1.0, n)
    close = pd.Series(100 + np.cumsum(steps), index=idx)
    high = close + rng.uniform(0.1, 1.0, n)
    low = close - rng.uniform(0.1, 1.0, n)
    volume = pd.Series(rng.uniform(1e6, 2e6, n), index=idx)
    return {"close": close, "high": high, "low": low, "volume": volume}


# ── (a) compute_vcp_tag() scope logic ───────────────────────────────────

def test_ath_scope_min_is_the_same_cutoff_timing_lamp_uses():
    """VCP_ATH_SCOPE_MIN must be a single-source-of-truth reuse of
    grp.ATH_RED_DIST, not a re-hardcoded -10.0 — otherwise the VCP base-high
    window and the board's ATH trigger could silently drift apart."""
    assert dd_screener.VCP_ATH_SCOPE_MIN == ATH_RED_DIST == -10.0


def test_far_from_ath_is_skipped():
    ohlcv = _synthetic_ohlcv(300)
    tag = dd_screener.compute_vcp_tag(-15.0, ohlcv)
    assert tag["vcp_scope"] == "far_from_ath"
    assert tag["vcp_gate"] is None
    assert tag["vcp_score"] is None
    assert tag["vcp_tight"] is False


def test_missing_dist_ath_pct_gets_scope_none():
    """No ATH data at all (e.g. skip_ma build) -> vcp_scope stays None, not
    "far_from_ath" (those are different reasons for not computing)."""
    tag = dd_screener.compute_vcp_tag(None, _synthetic_ohlcv(300))
    assert tag["vcp_scope"] is None
    assert tag["vcp_gate"] is None
    assert tag["vcp_tight"] is False


def test_scope_boundary_at_exactly_minus_10_is_in_scope():
    """Spec: "within 10% of ATH (ma.dist_ath_pct >= -10)" — the boundary
    itself is in scope, not excluded."""
    tag = dd_screener.compute_vcp_tag(-10.0, _synthetic_ohlcv(300))
    assert tag["vcp_scope"] == "computed"


def test_scope_just_past_minus_10_is_far_from_ath():
    tag = dd_screener.compute_vcp_tag(-10.01, _synthetic_ohlcv(300))
    assert tag["vcp_scope"] == "far_from_ath"


def test_too_few_bars_is_insufficient():
    short = _synthetic_ohlcv(100)  # < VCP_MIN_BARS (221)
    assert len(short["close"]) < vcp_core.VCP_MIN_BARS
    tag = dd_screener.compute_vcp_tag(-2.0, short)
    assert tag["vcp_scope"] == "insufficient_bars"
    assert tag["vcp_gate"] is None
    assert tag["vcp_tight"] is False


def test_missing_ohlcv_entry_is_insufficient():
    """Ticker within scope by distance, but its 5y daily fetch failed
    entirely (not in vcp_ohlcv_map) — same "insufficient_bars" bucket as a
    too-short series, not treated as an error."""
    tag = dd_screener.compute_vcp_tag(-2.0, None)
    assert tag["vcp_scope"] == "insufficient_bars"


def test_computed_calls_calc_vcp_and_maps_every_field(monkeypatch):
    """Deterministic field-mapping check: stub calc_vcp() and verify
    compute_vcp_tag() passes its four Series through positionally and maps
    every key straight into the vcp_* row fields, with vcp_tight derived
    from vcp_gate == "pass"."""
    ohlcv = _synthetic_ohlcv(300)
    captured = {}

    def _stub_calc_vcp(closes, highs, lows, volumes):
        captured["args"] = (closes, highs, lows, volumes)
        return {
            "score": 77, "pullback_count": 3, "last_pullback_pct": 4.2,
            "vol_dryup_ratio": 0.55, "base_age_days": 42, "vcp_gate": "pass",
        }

    monkeypatch.setattr(dd_screener, "calc_vcp", _stub_calc_vcp)
    tag = dd_screener.compute_vcp_tag(-2.0, ohlcv)

    assert captured["args"] == (ohlcv["close"], ohlcv["high"], ohlcv["low"], ohlcv["volume"])
    assert tag == {
        "vcp_scope": "computed", "vcp_gate": "pass", "vcp_score": 77,
        "vcp_pullback_count": 3, "vcp_last_pullback_pct": 4.2,
        "vcp_vol_dryup_ratio": 0.55, "vcp_base_age_days": 42, "vcp_tight": True,
    }


def test_computed_not_tight_when_gate_is_contraction_or_trend(monkeypatch):
    ohlcv = _synthetic_ohlcv(300)
    monkeypatch.setattr(dd_screener, "calc_vcp", lambda c, h, l, v: {
        "score": 30, "pullback_count": 1, "last_pullback_pct": 9.0,
        "vol_dryup_ratio": 1.1, "base_age_days": 10, "vcp_gate": "contraction",
    })
    tag = dd_screener.compute_vcp_tag(-2.0, ohlcv)
    assert tag["vcp_scope"] == "computed"
    assert tag["vcp_gate"] == "contraction"
    assert tag["vcp_tight"] is False


def test_computed_end_to_end_against_real_calc_vcp():
    """Not monkeypatched — proves compute_vcp_tag() really does call the real
    vcp_core.calc_vcp() (not a stand-in) end to end and that its output is
    self-consistent with calling calc_vcp() directly on the same series."""
    ohlcv = _synthetic_ohlcv(300, seed=7)
    tag = dd_screener.compute_vcp_tag(-1.0, ohlcv)
    assert tag["vcp_scope"] == "computed"
    expected = vcp_core.calc_vcp(ohlcv["close"], ohlcv["high"], ohlcv["low"], ohlcv["volume"])
    assert tag["vcp_gate"] == expected["vcp_gate"]
    assert tag["vcp_score"] == expected["score"]
    assert tag["vcp_pullback_count"] == expected["pullback_count"]
    assert tag["vcp_last_pullback_pct"] == expected["last_pullback_pct"]
    assert tag["vcp_vol_dryup_ratio"] == expected["vol_dryup_ratio"]
    assert tag["vcp_base_age_days"] == expected["base_age_days"]
    assert tag["vcp_tight"] == (expected["vcp_gate"] == "pass")


# ── (b) ③ 等待池 🟡 group sort ────────────────────────────────────────────

def _waiting_row(ticker, dist_ath, lamp_code, vcp_tight=None):
    return {"ticker": ticker, "dist_ath_pct": dist_ath, "lamp": {"code": lamp_code},
            "vcp_tight": vcp_tight}


def test_yellow_group_sorts_tight_first_ties_keep_revision_order():
    # Input order is assumed to already be grp.pool_sort_key() order (revision
    # descending) — that's what build_arena.main() hands to this function.
    # A (rev 20, loose), B (rev 15, tight), C (rev 10, loose), D (rev 5, tight).
    rows = [
        _waiting_row("A", -5.0, "yellow", vcp_tight=False),
        _waiting_row("B", -6.0, "yellow", vcp_tight=True),
        _waiting_row("C", -7.0, "yellow", vcp_tight=False),
        _waiting_row("D", -8.0, "yellow", vcp_tight=True),
    ]
    yellow, red, gray = build_arena._group_waiting_pool_by_timing(rows)
    # Tight (B, D) first, each subgroup keeps its incoming revision-desc order.
    assert [r["ticker"] for r in yellow] == ["B", "D", "A", "C"]
    assert red == [] and gray == []


def test_yellow_group_all_tight_or_all_loose_keeps_revision_order():
    rows = [_waiting_row(t, -5.0 - i, "yellow", vcp_tight=True) for i, t in enumerate("ABC")]
    yellow, _, _ = build_arena._group_waiting_pool_by_timing(rows)
    assert [r["ticker"] for r in yellow] == ["A", "B", "C"]


def test_yellow_group_missing_vcp_tight_treated_as_not_tight():
    """Rows with no vcp_scope/vcp_tight at all (legacy data, or vcp_scope
    wasn't "computed") must not crash the sort and sort after tight rows —
    `not None` is truthy, so they land in the "not tight" bucket."""
    rows = [
        _waiting_row("A", -5.0, "yellow"),   # vcp_tight=None
        _waiting_row("B", -6.0, "yellow", vcp_tight=True),
    ]
    yellow, _, _ = build_arena._group_waiting_pool_by_timing(rows)
    assert [r["ticker"] for r in yellow] == ["B", "A"]


def test_red_and_gray_groups_order_unchanged_by_vcp_tight():
    """🔴 拉回中 and ⚫ 資料缺 keep their incoming order regardless of
    vcp_tight — only 🟡 gets the tight-first resort."""
    rows = [
        _waiting_row("R1", -20.0, "red", vcp_tight=False),
        _waiting_row("R2", -12.0, "red", vcp_tight=True),   # tight, but red -> unaffected
        _waiting_row("G1", None, "yellow", vcp_tight=False),
        _waiting_row("G2", None, "yellow", vcp_tight=True),  # tight, but gray -> unaffected
    ]
    _, red, gray = build_arena._group_waiting_pool_by_timing(rows)
    assert [r["ticker"] for r in red] == ["R1", "R2"]
    assert [r["ticker"] for r in gray] == ["G1", "G2"]


# ── (c) 底部 cell text per scope/gate ────────────────────────────────────

def _v(scope, tight, lamp_code="yellow", n=3, last_pb=6.2, score=70, vol=0.6, age=40):
    return {"vcp_scope": scope, "vcp_tight": tight, "lamp": {"code": lamp_code},
            "vcp_pullback_count": n, "vcp_last_pullback_pct": last_pb,
            "vcp_score": score, "vcp_vol_dryup_ratio": vol, "vcp_base_age_days": age}


def test_bottom_cell_far_from_ath():
    v = _v("far_from_ath", False)
    assert build_arena._vcp_kind(v) == "far"
    assert build_arena._bottom_ascii_cell(v) == "-"
    assert "—" in build_arena._bottom_cell_html(v)


def test_bottom_cell_insufficient_bars():
    v = _v("insufficient_bars", False)
    assert build_arena._vcp_kind(v) == "insufficient"
    assert build_arena._bottom_ascii_cell(v) == "SHRT"
    assert "資料短" in build_arena._bottom_cell_html(v)


def test_bottom_cell_computed_tight_yellow():
    v = _v("computed", True, lamp_code="yellow")
    assert build_arena._vcp_kind(v) == "tight"
    assert build_arena._bottom_ascii_cell(v) == "T3/6.2"
    html = build_arena._bottom_cell_html(v)
    assert "緊 3段" in html and "−6.2%" in html


def test_bottom_cell_computed_loose_yellow():
    v = _v("computed", False, lamp_code="yellow", n=2, last_pb=15.0)
    assert build_arena._vcp_kind(v) == "loose"
    assert build_arena._bottom_ascii_cell(v) == "L2"
    html = build_arena._bottom_cell_html(v)
    assert "鬆 2段" in html
    assert "15.0" not in html.split("title=")[0]  # 鬆 not showing last-pullback in the visible text


def test_bottom_cell_breakout_tight_green():
    v = _v("computed", True, lamp_code="green")
    assert build_arena._vcp_kind(v) == "breakout_tight"
    assert build_arena._bottom_ascii_cell(v) == "BRKT"
    assert "緊縮後突破" in build_arena._bottom_cell_html(v)


def test_bottom_cell_breakout_loose_hot():
    v = _v("computed", False, lamp_code="hot")
    assert build_arena._vcp_kind(v) == "breakout_loose"
    assert build_arena._bottom_ascii_cell(v) == "BRKL"
    assert "鬆散突破" in build_arena._bottom_cell_html(v)


def test_bottom_cell_computed_not_breakout_for_red_or_yellow_lamp():
    """Only green/hot get the breakout wording — red (still in ③等待池,
    though _group_waiting_pool_by_timing would've routed it to 🔴) and
    yellow itself stay tight/loose."""
    v_red = _v("computed", True, lamp_code="red")
    assert build_arena._vcp_kind(v_red) == "tight"


def test_bottom_cell_missing_scope_is_none_kind():
    v = {}
    assert build_arena._vcp_kind(v) == "none"
    assert build_arena._bottom_ascii_cell(v) == "-"
    assert "—" in build_arena._bottom_cell_html(v)


def test_bottom_cell_tooltip_carries_raw_numbers():
    v = _v("computed", True, n=4, last_pb=3.5, score=88, vol=0.42, age=55)
    html = build_arena._bottom_cell_html(v)
    assert "88" in html and "4" in html and "3.5" in html and "0.42" in html and "55" in html
