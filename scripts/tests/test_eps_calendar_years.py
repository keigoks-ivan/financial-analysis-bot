"""Calendar-year basis helpers in eps_fy_shift.py (2026-10-08)."""
from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from eps_fy_shift import (  # noqa: E402
    calendar_year_columns,
    calendar_year_of_fy,
    condition_calendar_years,
    display_calendar_years,
    snapshot_fy1_end,
)


def test_calendar_year_of_fy():
    assert calendar_year_of_fy("2026-12-31") == 2026
    assert calendar_year_of_fy("2027-01-31") == 2026   # NVDA-style Jan FYE
    assert calendar_year_of_fy("2027-03-31") == 2026   # Japan March FYE
    assert calendar_year_of_fy("2027-05-31") == 2026
    assert calendar_year_of_fy("2027-06-30") == 2027   # 6/6 split -> end year
    assert calendar_year_of_fy("2027-07-03") == 2027   # SNDK
    assert calendar_year_of_fy("2027-09-02") == 2027   # MU
    assert calendar_year_of_fy(None) is None


def test_year_sets_switch_dates():
    assert display_calendar_years("2026-10-08") == (2026, 2027, 2028)
    assert display_calendar_years("2027-01-02") == (2027, 2028, 2029)
    assert condition_calendar_years("2026-10-08") == (2027, 2028)
    assert condition_calendar_years("2027-05-31") == (2027, 2028)
    assert condition_calendar_years("2027-06-01") == (2028, 2029)


MU_PAST = ["2025-09-23", "2025-12-17", "2026-03-18", "2026-06-25", "2026-09-30"]


def test_mu_rolled_now_and_pre_rollover_snapshot():
    # current (10-08, after the 09-30 annual report): FY1 = FY27 -> 2027 is column 1
    end = snapshot_fy1_end("2026-09-03", "2026-10-08", MU_PAST)
    assert end == date(2027, 9, 3)
    assert calendar_year_columns(end, (2027, 2028)) == {2027: 1, 2028: 2}
    # 06-23 snapshot (FY25 reported 2025-09-23): FY1 = FY26 -> 2027 is column 2
    end_b = snapshot_fy1_end("2026-09-03", "2026-06-23", MU_PAST)
    assert end_b == date(2026, 9, 3)
    assert calendar_year_columns(end_b, (2027, 2028)) == {2027: 2, 2028: 3}
    # 09-26 snapshot: FYE passed but annual report (09-30) not out -> still FY26
    assert snapshot_fy1_end("2026-09-03", "2026-09-26", MU_PAST) == date(2026, 9, 3)


def test_dec_fye_company():
    past = ["2026-02-10", "2026-04-28", "2026-07-28"]
    end = snapshot_fy1_end("2025-12-31", "2026-10-08", past)
    assert end == date(2026, 12, 31)
    assert calendar_year_columns(end, (2026, 2027, 2028)) == {2026: 1, 2027: 2, 2028: 3}
    # January, annual report not out yet: FY1 still 2026 -> 2029 unavailable
    end_jan = snapshot_fy1_end("2026-12-31", "2027-01-20", past + ["2026-10-27"])
    assert end_jan == date(2026, 12, 31)
    assert calendar_year_columns(end_jan, (2027, 2028, 2029)) == {2027: 2, 2028: 3, 2029: None}


def test_jan_fye_nvda_style():
    past = ["2026-02-25", "2026-05-27", "2026-08-26"]
    end = snapshot_fy1_end("2026-01-25", "2026-10-08", past)
    assert end == date(2027, 1, 25)                       # FY27 = calendar 2026
    assert calendar_year_columns(end, (2027, 2028)) == {2027: 2, 2028: 3}


def test_sep_fye_before_annual_report():
    # Apple-style: FYE 09-26, annual report 10-29 not yet out on 10-08
    past = ["2025-10-30", "2026-01-29", "2026-04-30", "2026-07-30"]
    end = snapshot_fy1_end("2026-09-26", "2026-10-08", past)
    assert end == date(2026, 9, 26)                       # FY26 -> 2026
    assert calendar_year_columns(end, (2027, 2028)) == {2027: 2, 2028: 3}


def test_yfinance_source_rolls_at_fye():
    assert snapshot_fy1_end("2026-09-03", "2026-09-10", MU_PAST, source="yfinance") == date(2027, 9, 3)


def test_no_dates_list():
    # no list, inside the window -> unknown; past the window -> assumed rolled
    assert snapshot_fy1_end("2026-07-03", "2026-08-20") is None
    assert snapshot_fy1_end("2026-07-03", "2026-12-01") == date(2027, 7, 3)
    # no list but a plausible last-earnings date
    assert snapshot_fy1_end("2026-07-03", "2026-08-20", last_earnings_date="2026-08-05") == date(2027, 7, 3)
    assert snapshot_fy1_end(None, "2026-10-08") is None
