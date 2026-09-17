"""Unit tests for scripts/build_dd_screener.py's compute_funnel_rank() —
the 2026-09-17 (owner pattern-approved) wiring of compute_fundamental_gates()'s
quality_veto_level / decline_signal_light into FunnelRank (see
compute_funnel_rank()'s docstring "four processes").

Hand-made inputs only — no network / no cache files. Same style as
scripts/tests/test_fundamental_gates.py / scripts/tests/test_eps_fx_normalize.py.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402


def _clean_quality():
    """A synthetic quality dict that passes all 4 SCORED_CRITERIA (FCF/ROIC/
    EPS CAGR/PEG) — pass5 → quality_gate = 1.00."""
    return {"fcf": 50.0, "roic": 50.0, "eps2y": 50.0, "peg": 0.5, "de": 0.3}


def test_veto_decline_signal_forces_zero():
    """(a) decline_signal_light == '⛔' → funnel_rank forced to 0, regardless
    of an otherwise-clean quality/moat/revision profile."""
    out = bds.compute_funnel_rank(
        _clean_quality(), pass_count=4, moat_score=10, moat_trend="→",
        rev_fy1=None, rev_fy2=None, rev_fy3=None,
        quality_veto_level="維持", decline_signal_light="⛔",
    )
    assert out["funnel_rank"] == 0.0
    assert out["veto_decline_signal"] is True
    assert out["veto_all_downgrade"] is False
    # Soft caps are skipped once a hard veto fires (max-severity wins).
    assert out["funnel_cap_quality"] is False
    assert out["funnel_cap_quality_level"] is None


def test_quality_veto_reject_caps_at_030():
    """(b) quality_veto_level == '拒絕' → cap 0.30. No revision baseline, so
    the (c) override never engages."""
    out = bds.compute_funnel_rank(
        _clean_quality(), pass_count=4, moat_score=10, moat_trend="→",
        rev_fy1=None, rev_fy2=None, rev_fy3=None,
        quality_veto_level="拒絕", decline_signal_light="🟢",
    )
    # Pre-cap weighted funnel would be 0.40*1.00 + 0.30*1.00 + 0.30*0.50 = 0.85
    # (revision_no_baseline → neutral 0.50) — well above the 0.30 cap.
    assert out["funnel_rank"] == 0.30
    assert out["funnel_cap_quality"] is True
    assert out["funnel_cap_quality_level"] == "拒絕"
    assert out["quality_cap_overridden_by_revision"] is False
    assert out["veto_decline_signal"] is False


def test_quality_veto_downgrade_caps_at_060():
    """(b) quality_veto_level == '降一級' → cap 0.60."""
    out = bds.compute_funnel_rank(
        _clean_quality(), pass_count=4, moat_score=10, moat_trend="→",
        rev_fy1=None, rev_fy2=None, rev_fy3=None,
        quality_veto_level="降一級", decline_signal_light="🟢",
    )
    assert out["funnel_rank"] == 0.60
    assert out["funnel_cap_quality"] is True
    assert out["funnel_cap_quality_level"] == "降一級"
    assert out["quality_cap_overridden_by_revision"] is False


def test_quality_veto_reject_overridden_by_all_three_revisions_up():
    """(c) Leading-overrides-lagging: quality_veto_level == '拒絕' but all
    three FY revisions are >= +1% (well above the +0.5% threshold) → the cap
    in (b) does NOT apply; funnel_rank falls through to the plain weighted
    formula instead."""
    out = bds.compute_funnel_rank(
        _clean_quality(), pass_count=4, moat_score=10, moat_trend="→",
        rev_fy1=1.0, rev_fy2=1.0, rev_fy3=1.0,
        quality_veto_level="拒絕", decline_signal_light="🟢",
    )
    assert out["quality_cap_overridden_by_revision"] is True
    assert out["funnel_cap_quality"] is False
    assert out["funnel_cap_quality_level"] is None
    # revision_score = 1.0 (all three upgraded, no steepening bonus since
    # fy3 == fy1) → funnel = 0.40*1.00 + 0.30*1.00 + 0.30*1.00 = 1.00, uncapped.
    assert out["funnel_rank"] == pytest.approx(1.00, abs=1e-6)
