"""Unit tests for the 財報錨定上修 (earnings-anchored EPS revision) baseline
picker in scripts/build_dd_screener.py — 2026-09-17 owner decision fixing the
fixed ~90-CALENDAR-day-back baseline (eps_rev_3m_pct) being unfair across
reporting calendars (an early reporter's post-earnings upgrade ages out of
the window a month later for purely calendar reasons, while a name that
hasn't reported yet sits near zero). See knowledge/rule_ledger.md「上修改為
財報後錨定」row and build_dd_screener.py's
pick_strictly_before_baseline()/_compute_eps_rev_since_earnings() docstrings.

Hand-made inputs only — no network, no reliance on real
docs/dd-screener/eps-estimates-snapshots/*.json content (monthly_snapshots
is injected). Same style as scripts/tests/test_eps_fx_normalize.py and
scripts/tests/test_fundamental_gates.py.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402


# ── pick_strictly_before_baseline() — pure function ─────────────────────────

def _snap(snapshot_date, **tickers):
    return {"snapshot_date": snapshot_date, "tickers": tickers}


def test_picks_latest_snapshot_strictly_before_target():
    snapshots = {
        "2026-06": _snap("2026-06-23"),
        "2026-07": _snap("2026-07-30"),
        "2026-08": _snap("2026-08-28"),
    }
    # Ticker reported 2026-09-05 — latest snapshot strictly before that is 08-28.
    picked = bds.pick_strictly_before_baseline(snapshots, "2026-09-05")
    assert picked["snapshot_date"] == "2026-08-28"


def test_picks_july_when_august_snapshot_postdates_earnings():
    snapshots = {
        "2026-06": _snap("2026-06-23"),
        "2026-07": _snap("2026-07-30"),
        "2026-08": _snap("2026-08-28"),
    }
    # Ticker reported 2026-08-15 — the 08-28 snapshot is AFTER the earnings
    # date (would already contain the post-earnings revision), so it must be
    # excluded; 07-30 is the correct pick.
    picked = bds.pick_strictly_before_baseline(snapshots, "2026-08-15")
    assert picked["snapshot_date"] == "2026-07-30"


def test_none_when_target_date_is_falsy():
    snapshots = {"2026-08": _snap("2026-08-28")}
    assert bds.pick_strictly_before_baseline(snapshots, None) is None
    assert bds.pick_strictly_before_baseline(snapshots, "") is None


def test_none_when_no_snapshot_predates_target():
    # Ticker hasn't reported yet this cycle relative to what's on disk — every
    # available snapshot postdates (or equals) the "target" (e.g. a bogus/very
    # early earnings date, or an empty snapshot set).
    snapshots = {"2026-08": _snap("2026-08-28")}
    assert bds.pick_strictly_before_baseline(snapshots, "2026-01-01") is None
    assert bds.pick_strictly_before_baseline({}, "2026-09-05") is None


def test_strictly_before_excludes_snapshot_dated_exactly_on_target():
    # A snapshot taken ON the earnings date itself must NOT be picked (could
    # already contain the post-earnings revision being measured) — this is
    # the "strictly before", not "on or before", rule.
    snapshots = {"2026-08": _snap("2026-08-28")}
    assert bds.pick_strictly_before_baseline(snapshots, "2026-08-28") is None
    # One day later, it becomes eligible.
    assert bds.pick_strictly_before_baseline(snapshots, "2026-08-29") is not None


def test_handles_dirty_snapshot_date_suffix():
    # Real snapshot on disk (docs/dd-screener/eps-estimates-snapshots/2026-05.json)
    # carries a descriptive suffix, e.g. "2026-05-26 (incremental updates over
    # 2026-05-25 base)" — only the first 10 chars (YYYY-MM-DD) must be parsed.
    snapshots = {
        "2026-05": _snap("2026-05-26 (incremental updates over 2026-05-25 base)"),
        "2026-06": _snap("2026-06-23"),
    }
    picked = bds.pick_strictly_before_baseline(snapshots, "2026-06-01")
    assert picked["snapshot_date"].startswith("2026-05-26")


def test_unparseable_snapshot_dates_are_skipped_not_fatal():
    snapshots = {
        "bad": {"snapshot_date": "not-a-date", "tickers": {}},
        "2026-06": _snap("2026-06-23"),
    }
    picked = bds.pick_strictly_before_baseline(snapshots, "2026-07-01")
    assert picked["snapshot_date"] == "2026-06-23"


def test_unparseable_target_date_returns_none():
    snapshots = {"2026-06": _snap("2026-06-23")}
    assert bds.pick_strictly_before_baseline(snapshots, "not-a-date") is None


# ── _compute_eps_rev_since_earnings() — integration over the pure picker ───
# reporting_ccy_cache pre-seeded with "USD" so get_reporting_currency() never
# hits the network (see eps_fx_normalize.get_reporting_currency: a cache hit
# short-circuits before any yfinance call).

def _usd_cache(ticker="FAKE"):
    return {ticker: {"currency": "USD", "checked": "2026-01-01"}}


def test_uses_earnings_anchor_when_a_qualifying_snapshot_exists():
    monthly = {
        "2026-06": _snap("2026-06-23", FAKE={"eps_fy_curr": 10.0, "eps_fy_next": 12.0, "eps_fy3": 15.0}),
        "2026-07": _snap("2026-07-30", FAKE={"eps_fy_curr": 10.5, "eps_fy_next": 12.5, "eps_fy3": 16.0}),
    }
    eps_rev_3m_result = {"eps_rev_3m_pct": -99.0, "eps_rev_3m_baseline_date": "2026-06-23"}
    out = bds._compute_eps_rev_since_earnings(
        "FAKE", "FAKE", 11.0, 13.0, 17.0,
        last_earnings_date="2026-08-01",
        current_snapshot_date="2026-09-17",
        reporting_ccy_cache=_usd_cache(), fx_cache={},
        eps_rev_3m_result=eps_rev_3m_result,
        monthly_snapshots=monthly,
    )
    assert out["eps_rev_anchor"] == "earnings"
    # Baseline picked must be the latest one strictly before 2026-08-01 -> 07-30.
    assert out["eps_rev_since_earnings_baseline_date"] == "2026-07-30"
    assert out["eps_rev_since_earnings_pct"] is not None
    # Must NOT silently reuse the calendar-3m fallback value.
    assert out["eps_rev_since_earnings_pct"] != eps_rev_3m_result["eps_rev_3m_pct"]
    assert out["eps_rev_since_earnings_days"] is not None and out["eps_rev_since_earnings_days"] >= 0


def test_falls_back_to_calendar_3m_when_last_earnings_date_unknown():
    monthly = {"2026-07": _snap("2026-07-30", FAKE={"eps_fy_curr": 10.5})}
    eps_rev_3m_result = {"eps_rev_3m_pct": 4.2, "eps_rev_3m_baseline_date": "2026-06-23"}
    out = bds._compute_eps_rev_since_earnings(
        "FAKE", "FAKE", 11.0, 13.0, 17.0,
        last_earnings_date=None,
        current_snapshot_date="2026-09-17",
        reporting_ccy_cache=_usd_cache(), fx_cache={},
        eps_rev_3m_result=eps_rev_3m_result,
        monthly_snapshots=monthly,
    )
    assert out["eps_rev_anchor"] == "calendar_3m"
    assert out["eps_rev_since_earnings_pct"] == eps_rev_3m_result["eps_rev_3m_pct"]
    assert out["eps_rev_since_earnings_baseline_date"] == "2026-06-23"


def test_falls_back_to_calendar_3m_when_no_snapshot_predates_earnings():
    # Ticker hasn't reported yet this cycle relative to what's on disk — the
    # only snapshot postdates the (bogus, very early) last_earnings_date.
    monthly = {"2026-08": _snap("2026-08-28", FAKE={"eps_fy_curr": 10.5})}
    eps_rev_3m_result = {"eps_rev_3m_pct": 1.1, "eps_rev_3m_baseline_date": "2026-06-23"}
    out = bds._compute_eps_rev_since_earnings(
        "FAKE", "FAKE", 11.0, 13.0, 17.0,
        last_earnings_date="2026-01-01",
        current_snapshot_date="2026-09-17",
        reporting_ccy_cache=_usd_cache(), fx_cache={},
        eps_rev_3m_result=eps_rev_3m_result,
        monthly_snapshots=monthly,
    )
    assert out["eps_rev_anchor"] == "calendar_3m"
    assert out["eps_rev_since_earnings_pct"] == eps_rev_3m_result["eps_rev_3m_pct"]


def test_fold_eps_rev_fy_weighted_matches_manual_calculation():
    rev = {"eps_fy_curr_revision_pct": 10.0, "eps_fy_next_revision_pct": 20.0,
           "eps_fy3_revision_pct": 30.0}
    # 0.2*10 + 0.3*20 + 0.5*30 = 2 + 6 + 15 = 23
    assert bds._fold_eps_rev_fy_weighted(rev) == pytest.approx(23.0)


def test_fold_eps_rev_fy_weighted_renormalizes_over_available_fys():
    # FY3 missing -> renormalize over FY1 (0.2) / FY2 (0.3) only.
    rev = {"eps_fy_curr_revision_pct": 10.0, "eps_fy_next_revision_pct": 20.0,
           "eps_fy3_revision_pct": None}
    expected = (10.0 * 0.2 + 20.0 * 0.3) / (0.2 + 0.3)
    assert bds._fold_eps_rev_fy_weighted(rev) == pytest.approx(round(expected, 2))


def test_fold_eps_rev_fy_weighted_none_when_all_missing():
    rev = {"eps_fy_curr_revision_pct": None, "eps_fy_next_revision_pct": None,
           "eps_fy3_revision_pct": None}
    assert bds._fold_eps_rev_fy_weighted(rev) is None
