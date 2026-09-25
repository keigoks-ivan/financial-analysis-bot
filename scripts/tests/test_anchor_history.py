"""Unit tests for scripts/etf_dash/anchor_history.py — the "anchor line"
fallback for build_etf_dash.py's Exhibit 2 long EPS-index chart (used when a
fund's dd-screener coverage is too low, e.g. TOPIX — see
build_etf_dash.py::LONG_EPS_LINE_MIN_COVERAGE_PCT and
build_anchor_chart_series()).

Covers: splice_runs() chain-linking across overlapping FULL runs, the
>90-day-gap -> new-segment rule, build_display_points() rebasing, and the
append-only JSONL persistence (append_run()/load_runs()) idempotency
convention shared with dd_eps_history.py.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR / "etf_dash"))

import anchor_history as ah  # noqa: E402


# ── splice_runs() — single run seeds the series as-is ────────────────────────

def test_splice_runs_empty_input_returns_empty():
    points, notes = ah.splice_runs([])
    assert points == []
    assert notes == []


def test_splice_runs_single_run_seeds_points_unchanged():
    run1 = {
        "eps_as_of": "2026-09-25",
        "points": [
            {"date": "2026-06-27", "level": 92.3, "coverage_pct": 80.0},
            {"date": "2026-07-27", "level": 94.1, "coverage_pct": 82.0},
            {"date": "2026-08-26", "level": 97.0, "coverage_pct": 85.0},
            {"date": "2026-09-18", "level": 99.2, "coverage_pct": 88.0},
            {"date": "2026-09-25", "level": 100.0, "coverage_pct": 90.0},
        ],
    }
    points, notes = ah.splice_runs([run1])
    assert notes == []
    assert [p["segment_id"] for p in points] == [0] * 5
    assert [p["level"] for p in points] == [92.3, 94.1, 97.0, 99.2, 100.0]
    assert points[-1]["date"] == "2026-09-25"


# ── splice_runs() — chain-linking two overlapping (monthly-cadence) runs ────

def _monthly_run(eps_as_of: str, dates_days_ago: list[tuple[str, int]], levels: list[float],
                  coverage: float = 85.0) -> dict:
    points = [{"date": d, "level": lvl, "coverage_pct": coverage}
              for (d, _), lvl in zip(dates_days_ago, levels)]
    return {"eps_as_of": eps_as_of, "points": points}


def test_splice_runs_chain_links_second_run_when_anchor_matches_exactly():
    # run1: eps_as_of 2026-09-25, its own 100-basis levels.
    run1 = {
        "eps_as_of": "2026-09-25",
        "points": [
            {"date": "2026-06-27", "level": 90.0, "coverage_pct": 80.0},
            {"date": "2026-07-27", "level": 94.0, "coverage_pct": 82.0},
            {"date": "2026-08-26", "level": 97.0, "coverage_pct": 85.0},
            {"date": "2026-09-18", "level": 99.0, "coverage_pct": 88.0},
            {"date": "2026-09-25", "level": 100.0, "coverage_pct": 90.0},
        ],
    }
    # run2: eps_as_of 2026-10-25 (30 days later); its own -30d point lands
    # exactly on 2026-09-25 = run1's last stored date, so this exercises the
    # exact-date-match path of chain-linking.
    run2 = {
        "eps_as_of": "2026-10-25",
        "points": [
            {"date": "2026-07-27", "level": 88.0, "coverage_pct": 79.0},
            {"date": "2026-08-26", "level": 92.0, "coverage_pct": 81.0},
            {"date": "2026-09-25", "level": 98.0, "coverage_pct": 84.0},   # anchor point
            {"date": "2026-10-18", "level": 99.5, "coverage_pct": 87.0},  # new
            {"date": "2026-10-25", "level": 100.0, "coverage_pct": 90.0},  # new
        ],
    }
    points, notes = ah.splice_runs([run1, run2])
    assert notes == []  # no gap -> single segment throughout
    assert all(p["segment_id"] == 0 for p in points)
    # run1's 5 points unchanged, plus run2's 2 new points (dates after 2026-09-25),
    # scaled by scale = stored(2026-09-25)=100.0 / run2_anchor(2026-09-25)=98.0.
    assert [p["date"] for p in points] == [
        "2026-06-27", "2026-07-27", "2026-08-26", "2026-09-18", "2026-09-25",
        "2026-10-18", "2026-10-25",
    ]
    scale = 100.0 / 98.0
    got_1018 = next(p for p in points if p["date"] == "2026-10-18")
    got_1025 = next(p for p in points if p["date"] == "2026-10-25")
    assert got_1018["level"] == pytest.approx(round(99.5 * scale, 4))
    assert got_1025["level"] == pytest.approx(round(100.0 * scale, 4))
    assert got_1018["coverage_pct"] == 87.0  # coverage passes through unscaled
    # run1's original points are untouched.
    assert next(p for p in points if p["date"] == "2026-09-25")["level"] == 100.0


def test_splice_runs_chain_links_via_closest_not_after_when_dates_dont_match_exactly():
    # Same idea, but run2's dates are offset by a few days from run1's stored
    # dates, so the anchor is "closest to but not after" last_stored_date,
    # not an exact match — exercises _value_on_or_before().
    run1 = {
        "eps_as_of": "2026-09-20",
        "points": [
            {"date": "2026-06-22", "level": 91.0, "coverage_pct": 80.0},
            {"date": "2026-07-22", "level": 95.0, "coverage_pct": 82.0},
            {"date": "2026-08-21", "level": 98.0, "coverage_pct": 85.0},
            {"date": "2026-09-13", "level": 99.4, "coverage_pct": 88.0},
            {"date": "2026-09-20", "level": 100.0, "coverage_pct": 90.0},
        ],
    }
    run2 = {
        "eps_as_of": "2026-10-24",
        "points": [
            {"date": "2026-07-26", "level": 89.0, "coverage_pct": 79.0},
            {"date": "2026-08-25", "level": 93.0, "coverage_pct": 81.0},
            {"date": "2026-09-24", "level": 97.0, "coverage_pct": 84.0},  # > last_stored_date (2026-09-20)!
            {"date": "2026-10-17", "level": 99.0, "coverage_pct": 87.0},
            {"date": "2026-10-24", "level": 100.0, "coverage_pct": 90.0},
        ],
    }
    points, notes = ah.splice_runs([run1, run2])
    assert notes == []
    # anchor candidates in run2 with date <= 2026-09-20: only 2026-08-25 (97.0
    # is 2026-09-24, which is AFTER last_stored_date, so excluded).
    anchor_level = 93.0
    stored_ref = 98.0  # run1's value at (or before) 2026-08-25 -> 2026-08-21 = 98.0
    scale = stored_ref / anchor_level
    new_dates = ["2026-09-24", "2026-10-17", "2026-10-24"]
    assert [p["date"] for p in points][-3:] == new_dates
    expected = {"2026-09-24": 97.0, "2026-10-17": 99.0, "2026-10-24": 100.0}
    for d in new_dates:
        got = next(p for p in points if p["date"] == d)
        assert got["level"] == pytest.approx(round(expected[d] * scale, 4))


# ── splice_runs() — gap > 90 days starts a new segment ───────────────────────

def test_splice_runs_gap_over_90_days_starts_new_segment():
    run1 = {
        "eps_as_of": "2026-01-03",
        "points": [
            {"date": "2025-10-05", "level": 85.0, "coverage_pct": 80.0},
            {"date": "2025-11-04", "level": 90.0, "coverage_pct": 82.0},
            {"date": "2025-12-04", "level": 95.0, "coverage_pct": 85.0},
            {"date": "2025-12-27", "level": 98.0, "coverage_pct": 88.0},
            {"date": "2026-01-03", "level": 100.0, "coverage_pct": 90.0},
        ],
    }
    # Next FULL run isn't until almost 9 months later — gap from 2026-01-03 to
    # run2's earliest point (2026-06-27, -90d of 2026-09-25) is way over 90 days.
    run2 = {
        "eps_as_of": "2026-09-25",
        "points": [
            {"date": "2026-06-27", "level": 88.0, "coverage_pct": 79.0},
            {"date": "2026-07-27", "level": 92.0, "coverage_pct": 81.0},
            {"date": "2026-08-26", "level": 96.0, "coverage_pct": 84.0},
            {"date": "2026-09-18", "level": 99.0, "coverage_pct": 87.0},
            {"date": "2026-09-25", "level": 100.0, "coverage_pct": 90.0},
        ],
    }
    points, notes = ah.splice_runs([run1, run2])
    assert len(notes) == 1
    note = notes[0]
    assert note["segment_id"] == 1
    assert note["prev_date"] == "2026-01-03"
    assert note["new_eps_as_of"] == "2026-09-25"
    assert note["gap_days"] > 90
    seg0 = [p for p in points if p["segment_id"] == 0]
    seg1 = [p for p in points if p["segment_id"] == 1]
    assert len(seg0) == 5 and len(seg1) == 5
    # segment 1's points keep run2's OWN levels — not scaled/chained to segment 0.
    assert [p["level"] for p in seg1] == [88.0, 92.0, 96.0, 99.0, 100.0]


# ── build_display_points() — only the latest segment, rebased to 100 ────────

def test_build_display_points_empty_input():
    assert ah.build_display_points([]) == []


def test_build_display_points_single_segment_rebases_first_point_to_100():
    points = [
        {"date": "2026-06-27", "level": 92.3, "coverage_pct": 80.0, "segment_id": 0},
        {"date": "2026-09-25", "level": 100.0, "coverage_pct": 90.0, "segment_id": 0},
    ]
    out = ah.build_display_points(points)
    assert out[0]["level"] == 100.0
    assert out[0]["date"] == "2026-06-27"
    assert out[1]["level"] == pytest.approx(round(100.0 / 92.3 * 100, 4))
    assert "segment_id" not in out[0]  # display points drop the internal bookkeeping field


def test_build_display_points_only_uses_latest_segment_after_a_gap():
    points = [
        {"date": "2025-10-05", "level": 85.0, "coverage_pct": 80.0, "segment_id": 0},
        {"date": "2026-01-03", "level": 100.0, "coverage_pct": 90.0, "segment_id": 0},
        {"date": "2026-06-27", "level": 88.0, "coverage_pct": 79.0, "segment_id": 1},
        {"date": "2026-09-25", "level": 100.0, "coverage_pct": 90.0, "segment_id": 1},
    ]
    out = ah.build_display_points(points)
    assert [p["date"] for p in out] == ["2026-06-27", "2026-09-25"]
    assert out[0]["level"] == 100.0  # rebased to segment 1's own first point
    assert out[1]["level"] == pytest.approx(round(100.0 / 88.0 * 100, 4))


def test_build_display_points_missing_base_level_returns_empty():
    points = [{"date": "2026-06-27", "level": None, "coverage_pct": 80.0, "segment_id": 0}]
    assert ah.build_display_points(points) == []


# ── append_run()/load_runs() — append-only JSONL, same-eps_as_of idempotency ─

@pytest.fixture()
def tmp_anchor_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(ah, "ANCHOR_HISTORY_DIR", tmp_path)
    return tmp_path


def test_load_runs_missing_file_returns_empty(tmp_anchor_dir):
    assert ah.load_runs("TOPIX") == []


def test_append_run_then_load_round_trips(tmp_anchor_dir):
    run = {"eps_as_of": "2026-09-25", "points": [{"date": "2026-09-25", "level": 100.0, "coverage_pct": 90.0}]}
    ah.append_run("TOPIX", run)
    rows = ah.load_runs("TOPIX")
    assert rows == [run]
    assert (tmp_anchor_dir / "TOPIX.jsonl").exists()


def test_append_run_same_eps_as_of_rewrites_last_line_only(tmp_anchor_dir):
    run1 = {"eps_as_of": "2026-09-25", "points": [{"date": "2026-09-25", "level": 100.0, "coverage_pct": 50.0}]}
    ah.append_run("TOPIX", run1)
    run1_rerun = {"eps_as_of": "2026-09-25", "points": [{"date": "2026-09-25", "level": 100.0, "coverage_pct": 91.0}]}
    ah.append_run("TOPIX", run1_rerun)
    rows = ah.load_runs("TOPIX")
    assert len(rows) == 1
    assert rows[0]["points"][0]["coverage_pct"] == 91.0


def test_append_run_new_eps_as_of_appends_new_line(tmp_anchor_dir):
    run1 = {"eps_as_of": "2026-08-01", "points": [{"date": "2026-08-01", "level": 100.0, "coverage_pct": 50.0}]}
    run2 = {"eps_as_of": "2026-09-25", "points": [{"date": "2026-09-25", "level": 100.0, "coverage_pct": 90.0}]}
    ah.append_run("TOPIX", run1)
    ah.append_run("TOPIX", run2)
    rows = ah.load_runs("TOPIX")
    assert [r["eps_as_of"] for r in rows] == ["2026-08-01", "2026-09-25"]


def test_load_runs_skips_malformed_lines(tmp_anchor_dir):
    path = tmp_anchor_dir / "TOPIX.jsonl"
    path.write_text(
        '{"eps_as_of": "2026-09-25", "points": []}\n'
        "not json at all\n",
        encoding="utf-8",
    )
    rows = ah.load_runs("TOPIX")
    assert len(rows) == 1
    assert rows[0]["eps_as_of"] == "2026-09-25"


def test_load_runs_separate_etf_keys_are_independent_files(tmp_anchor_dir):
    ah.append_run("TOPIX", {"eps_as_of": "2026-09-25", "points": []})
    ah.append_run("SPY", {"eps_as_of": "2026-09-25", "points": []})
    assert (tmp_anchor_dir / "TOPIX.jsonl").exists()
    assert (tmp_anchor_dir / "SPY.jsonl").exists()
    assert len(ah.load_runs("TOPIX")) == 1
    assert len(ah.load_runs("SPY")) == 1
