"""Unit + case tests for scripts/eps_fy_shift.py (fiscal-year rollover between
EPS snapshots, 2026-10-08) and its wiring in build_dd_screener.py.

Hand-made / real-number inputs only — no network (reporting currency is
pre-seeded in the cache as USD; fx cache untouched).
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402
from eps_fy_shift import (  # noqa: E402
    SHIFTED_BASELINE_KEY,
    check_numbers_agree,
    fy_shift,
    roll_fye_forward,
)
from datetime import date  # noqa: E402


# ── fy_shift(): every branch ────────────────────────────────────────────────

def test_unknown_when_earnings_missing():
    assert fy_shift("2026-09-03", None, "2026-09-26", "2026-10-08") == (0, "unknown")


def test_unknown_when_fye_missing():
    assert fy_shift(None, "2026-09-30", "2026-09-26", "2026-10-08") == (0, "unknown")


def test_unknown_when_dates_unparseable():
    assert fy_shift("2026-09-03", "2026-09-30", None, "2026-10-08") == (0, "unknown")
    assert fy_shift("garbage", "2026-09-30", "2026-09-26", "2026-10-08") == (0, "unknown")


def test_annual_report_inside_window_shifts_when_baseline_before_it():
    assert fy_shift("2026-09-03", "2026-09-30", "2026-09-26", "2026-10-08") == (1, "shifted_heuristic")


def test_baseline_on_report_day_counts_as_before_report():
    # snapshot taken ~09:30 Taipei, before a same-day US report
    assert fy_shift("2026-09-03", "2026-09-30", "2026-09-30", "2026-10-08") == (1, "shifted_heuristic")


def test_baseline_after_report_not_shifted():
    assert fy_shift("2026-09-03", "2026-09-30", "2026-10-03", "2026-10-08") == (0, "no_shift_heuristic")


def test_report_not_before_current_not_shifted():
    # current snapshot taken the same day as the report: not yet rolled
    assert fy_shift("2026-09-03", "2026-09-30", "2026-09-26", "2026-09-30") == (0, "no_shift_heuristic")


def test_implausibly_old_last_earnings_is_unknown():
    # e.g. GAMUDA's yfinance calendar returning 2011-09-29
    assert fy_shift("2026-07-31", "2011-09-29", "2026-06-23", "2026-10-08") == (0, "unknown")


def test_last_earnings_before_fye_is_no_shift():
    # annual report for that fiscal year isn't out yet
    assert fy_shift("2026-09-03", "2026-08-01", "2026-06-23", "2026-10-08") == (0, "no_shift_heuristic")


def test_last_earnings_equal_fye_is_no_shift():
    assert fy_shift("2026-09-03", "2026-09-03", "2026-06-23", "2026-10-08") == (0, "no_shift_heuristic")


def test_late_quarterly_report_baseline_after_window_no_shift():
    # NVDA: FYE 2026-01-25, last report 2026-08-26 (a Q2) > fye+105d
    assert fy_shift("2026-01-25", "2026-08-26", "2026-08-28", "2026-10-08") == (0, "no_shift_heuristic")


def test_late_report_baseline_before_fye_is_shifted():
    assert fy_shift("2026-01-25", "2026-08-26", "2026-01-10", "2026-10-08") == (1, "shifted_heuristic")


def test_late_report_baseline_inside_window_is_ambiguous():
    assert fy_shift("2026-01-25", "2026-08-26", "2026-03-01", "2026-10-08") == (0, "ambiguous_heuristic")


def test_late_report_current_inside_window_cannot_be_shifted():
    # baseline before FYE but current snapshot itself still inside the window
    assert fy_shift("2026-01-25", "2026-08-26", "2026-01-10", "2026-03-01") == (0, "ambiguous_heuristic")


def test_late_report_current_before_fye_is_no_shift():
    assert fy_shift("2026-01-25", "2026-08-26", "2025-11-01", "2026-01-10") == (0, "no_shift_heuristic")


def test_stale_fye_rolled_forward():
    # cache still says FYE 2025-09-03; true last FYE is 2026-09-03 -> same answer
    assert roll_fye_forward(date(2025, 9, 3), date(2026, 10, 8)) == date(2026, 9, 3)
    assert fy_shift("2025-09-03", "2026-09-30", "2026-09-26", "2026-10-08") == (1, "shifted_heuristic")


def test_roll_forward_leaves_current_fye_alone():
    assert roll_fye_forward(date(2026, 9, 3), date(2026, 10, 8)) == date(2026, 9, 3)
    assert roll_fye_forward(date(2024, 2, 29), date(2025, 3, 5)) == date(2025, 2, 28)


def test_check_numbers_agree():
    assert check_numbers_agree(176.15, 73.60, 159.49) is True
    assert check_numbers_agree(76.0, 73.60, 159.49) is False
    assert check_numbers_agree(None, 1.0, 2.0) is True


def test_shifted_baseline_key_map():
    assert SHIFTED_BASELINE_KEY == {"eps_fy_curr": "eps_fy_next",
                                    "eps_fy_next": "eps_fy3", "eps_fy3": None}


# ── real-number cases through _compute_fy_eps_revision ──────────────────────

def _rev(ticker, cur, base, base_date, cur_date, fye, le):
    snap = {"snapshot_date": base_date,
            "tickers": {ticker: {"eps_fy_curr": base[0], "eps_fy_next": base[1],
                                 "eps_fy3": base[2]}}}
    ccy = {ticker: {"currency": "USD", "checked": "2026-10-08"}}
    return bds._compute_fy_eps_revision(
        ticker, ticker, cur[0], cur[1], cur[2], snap, cur_date, ccy, {},
        last_fye=fye, last_earnings_date=le)


def test_mu_fy_rolled():
    r = _rev("MU", (176.15, 206.33, 203.15), (73.60, 159.49, 179.51),
             "2026-09-26", "2026-10-08", "2026-09-03", "2026-09-30")
    assert r["eps_revision_fy_shift"] == 1
    assert r["eps_revision_fy_shift_status"] == "shifted_heuristic"
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(10.45, abs=0.05)   # 176.15/159.49
    assert r["eps_fy_next_revision_pct"] == pytest.approx(206.33 / 179.51 * 100 - 100, abs=0.05)
    assert r["eps_fy3_revision_pct"] is None
    # folded value re-weights over FY1/FY2 only (0.2/0.3)
    folded = bds._fold_eps_rev_fy_weighted(r)
    assert 10 < folded < 15


def test_jbl_fy_rolled():
    r = _rev("JBL", (17.69, 22.17, 25.93), (12.77, 16.88, 20.57),
             "2026-09-26", "2026-10-08", "2026-08-31", "2026-09-30")
    assert r["eps_revision_fy_shift"] == 1
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(17.69 / 16.88 * 100 - 100, abs=0.05)
    assert r["eps_fy_curr_revision_pct"] < 6          # not the fake +38%


def test_msft_since_earnings_baseline_before_report_shifts():
    r = _rev("MSFT", (19.76, 22.5, 25.0), (16.84, 19.35, 22.0),
             "2026-06-23", "2026-10-08", "2026-06-30", "2026-07-29")
    assert r["eps_revision_fy_shift"] == 1
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(19.76 / 19.35 * 100 - 100, abs=0.05)


def test_msft_baseline_after_roll_does_not_shift():
    # 2026-07-30 snapshot already shows the new FY1 (19.18)
    r = _rev("MSFT", (19.76, 22.5, 25.0), (19.18, 22.0, 24.5),
             "2026-07-30", "2026-10-08", "2026-06-30", "2026-07-29")
    assert r["eps_revision_fy_shift"] == 0
    assert r["eps_revision_fy_shift_status"] == "no_shift_heuristic"
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(19.76 / 19.18 * 100 - 100, abs=0.05)


def test_nvda_quarterly_report_does_not_shift():
    r = _rev("NVDA", (8.0, 11.0, 13.0), (7.5, 10.4, 12.5),
             "2026-08-28", "2026-10-08", "2026-01-25", "2026-08-26")
    assert r["eps_revision_fy_shift"] == 0
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(8.0 / 7.5 * 100 - 100, abs=0.05)
    assert r["eps_fy3_revision_pct"] is not None


def test_amzn_dec_fye_does_not_shift():
    r = _rev("AMZN", (7.0, 8.5, 10.0), (6.8, 8.2, 9.7),
             "2026-08-28", "2026-10-08", "2025-12-31", "2026-07-30")
    assert r["eps_revision_fy_shift"] == 0
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(7.0 / 6.8 * 100 - 100, abs=0.05)


def test_midyear_big_real_upgrade_at_quarterly_report_does_not_shift():
    # Dec-FYE company, Q2 report late July, FY1 +50% real upgrade
    r = _rev("XYZ", (15.0, 18.0, 21.0), (10.0, 14.0, 17.0),
             "2026-06-23", "2026-10-08", "2025-12-31", "2026-07-29")
    assert r["eps_revision_fy_shift"] == 0
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(50.0, abs=0.01)
    assert r["eps_fy3_revision_pct"] == pytest.approx(21 / 17 * 100 - 100, abs=0.05)


def test_numbers_disagree_still_follows_date_but_flagged(capsys):
    # Date rule says rolled, but FY1 barely moved vs old FY1
    r = _rev("ABC", (10.1, 12.0, 14.0), (10.0, 11.5, 13.0),
             "2026-09-26", "2026-10-08", "2026-09-03", "2026-09-30")
    assert r["eps_revision_fy_shift"] == 1
    assert r["eps_revision_fy_shift_status"] == "shifted_numbers_disagree_heuristic"
    assert "fy-shift" in capsys.readouterr().out


def test_no_last_fye_falls_back_to_positional_compare():
    r = _rev("MU", (176.15, 206.33, 203.15), (73.60, 159.49, 179.51),
             "2026-09-26", "2026-10-08", None, "2026-09-30")
    assert r["eps_revision_fy_shift"] == 0
    assert r["eps_revision_fy_shift_status"] == "unknown"
    assert r["eps_fy_curr_revision_pct"] > 100   # legacy behaviour preserved


# ── consecutive-down flag across a rollover ─────────────────────────────────

def test_consec_down_uses_next_fy_across_rollover():
    def snap(d, fy1, fy2):
        return {"snapshot_date": d, "tickers": {"MU": {"eps_fy_curr": fy1, "eps_fy_next": fy2}}}
    base = {"2026-06": snap("2026-06-23", 100.0, 150.0),
            "2026-07": snap("2026-07-30", 99.0, 149.0),
            "2026-08": snap("2026-08-28", 98.0, 148.0)}
    ccy = {"MU": {"currency": "USD", "checked": "2026-10-08"}}
    # Rollover between 08-28 and now: new FY1 = old FY2 (148 -> 147 is a genuine
    # small cut), not 98 -> 147 (+50% fake raise).
    args = ("MU", "MU", 147.0, "2026-10-08", ccy, {})
    kw = dict(baselines=base, last_fye="2026-09-03", last_earnings_date="2026-09-30")
    assert bds.compute_eps_fy1_consec_down(*args, **kw) == "fail"
    assert bds.compute_eps_fy1_consec_down(*args, baselines=base) == "pass"   # legacy


# ── real reported-earnings dates (preferred path) ───────────────────────────

ORCL_DATES = ["2026-03-10", "2026-06-11", "2026-09-10"]   # Q3, annual (FYE 05-31), Q1


def test_dates_orcl_q1_report_is_not_the_annual_report():
    # since-earnings baseline 08-28; FY rolled at the 06-11 annual report, long before
    assert fy_shift("2026-05-31", "2026-09-10", "2026-08-28", "2026-10-08", ORCL_DATES) == (0, "no_shift")


def test_dates_orcl_baseline_before_annual_report_shifts():
    assert fy_shift("2026-05-31", "2026-09-10", "2026-06-05", "2026-10-08", ORCL_DATES) == (1, "shifted")


def test_dates_nke_type_annual_late_june_3m_baseline_0623_shifts():
    nke = ["2026-03-19", "2026-06-25", "2026-09-30"]    # FYE 05-31; annual late June; Q1 late Sep
    assert fy_shift("2026-05-31", "2026-09-30", "2026-06-23", "2026-10-08", nke) == (1, "shifted")
    # a baseline taken after the annual report is already rolled
    assert fy_shift("2026-05-31", "2026-09-30", "2026-07-30", "2026-10-08", nke) == (0, "no_shift")


def test_dates_no_report_after_fye_yet():
    assert fy_shift("2026-09-03", "2026-06-25", "2026-06-23", "2026-10-08",
                    ["2026-03-20", "2026-06-25"]) == (0, "no_annual_report")


def test_dates_junk_old_entries_ignored():
    # GAMUDA-style junk 2011 date in the list: first date after FYE still wins
    assert fy_shift("2026-07-31", "2026-09-29", "2026-09-26", "2026-10-08",
                    ["2011-09-29", "2026-06-01", "2026-09-29"]) == (1, "shifted")


def test_dates_nvda_quarterly_only():
    assert fy_shift("2026-01-25", "2026-08-26", "2026-08-28", "2026-10-08",
                    ["2026-02-25", "2026-05-27", "2026-08-26"]) == (0, "no_shift")


def test_empty_or_missing_list_falls_back_to_heuristic_suffix():
    for lst in (None, []):
        assert fy_shift("2026-09-03", "2026-09-30", "2026-09-26", "2026-10-08", lst) == (1, "shifted_heuristic")
    assert fy_shift("2026-09-03", None, "2026-09-26", "2026-10-08", []) == (0, "unknown")


def test_orcl_case_through_compute_with_dates_does_not_shift():
    snap = {"snapshot_date": "2026-08-28",
            "tickers": {"ORCL": {"eps_fy_curr": 7.0, "eps_fy_next": 8.4, "eps_fy3": 10.0}}}
    ccy = {"ORCL": {"currency": "USD", "checked": "2026-10-08"}}
    r = bds._compute_fy_eps_revision("ORCL", "ORCL", 7.02, 8.4, 10.1, snap, "2026-10-08", ccy, {},
                                     last_fye="2026-05-31", last_earnings_date="2026-09-10",
                                     past_earnings_dates=ORCL_DATES)
    assert r["eps_revision_fy_shift"] == 0
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(0.29, abs=0.01)


# ── source-aware (yfinance rolls at FYE, Koyfin after the annual report) ────

ACN_DATES = ["2026-03-20", "2026-06-25", "2026-10-01"]   # FYE 08-31, annual 10-01


def test_acn_yfinance_baseline_after_fye_vs_xlsx_current_after_report_no_shift():
    # both sides already point at FY27: yfinance since 08-31, Koyfin since 10-01
    assert fy_shift("2026-08-31", "2026-10-01", "2026-09-26", "2026-10-08", ACN_DATES,
                    "yfinance", "xlsx") == (0, "no_shift")


def test_spcx_first_report_after_fye_is_too_late_to_be_annual():
    d = ["2026-08-04"]   # FYE 2025-12-31, first report 7 months later (new listing, quarterly)
    for base in ("2026-06-23", "2026-07-30"):
        assert fy_shift("2025-12-31", "2026-08-04", base, "2026-10-08", d,
                        "xlsx", "xlsx") == (0, "assumed_rolled")


def test_shift_back_yfinance_baseline_after_fye_vs_xlsx_current_before_report():
    # FYE 08-31, annual report not out yet (last report is a quarter)
    assert fy_shift("2026-08-31", "2026-06-25", "2026-09-26", "2026-10-08",
                    ["2026-03-20", "2026-06-25"], "yfinance", "xlsx") == (-1, "shifted_back")
    # annual report exists but comes after the current snapshot
    assert fy_shift("2026-08-31", "2026-10-20", "2026-09-26", "2026-10-08",
                    ["2026-06-25", "2026-10-20"], "yfinance", "xlsx") == (-1, "shifted_back")


def test_yfinance_both_sides_needs_no_dates():
    assert fy_shift("2026-08-31", None, "2026-08-20", "2026-09-26", None,
                    "yfinance", "yfinance") == (1, "shifted")
    assert fy_shift("2026-08-31", None, "2026-09-10", "2026-09-26", None,
                    "yfinance", "yfinance") == (0, "no_shift")


def test_xlsx_to_yfinance_current_rolls_at_fye():
    # Koyfin baseline before the annual report, yfinance current after FYE -> shift
    assert fy_shift("2026-08-31", "2026-10-01", "2026-09-26", "2026-10-08", ACN_DATES,
                    "xlsx", "yfinance") == (1, "shifted")


def test_mixed_sources_without_dates_use_last_earnings_heuristic():
    assert fy_shift("2026-08-31", "2026-10-01", "2026-09-26", "2026-10-08", None,
                    "yfinance", "xlsx") == (0, "no_shift_heuristic")
    assert fy_shift("2026-08-31", "2026-10-01", "2026-09-26", "2026-10-08", None,
                    "xlsx", "xlsx") == (1, "shifted_heuristic")


def test_sndk_raw_koyfin_row_shifts():
    # raw Koyfin baseline (07-30) 66.68/212.95/255.63, FYE 07-03, annual report 08-05
    snap = {"snapshot_date": "2026-07-30", "tickers": {"SNDK": {
        "eps_fy_curr": 66.68, "eps_fy_next": 212.95, "eps_fy3": 255.63, "source": "xlsx"}}}
    ccy = {"SNDK": {"currency": "USD", "checked": "2026-10-08"}}
    r = bds._compute_fy_eps_revision("SNDK", "SNDK", 214.38, 265.24, 253.23, snap, "2026-10-08",
                                     ccy, {}, last_fye="2026-07-03", last_earnings_date="2026-08-05",
                                     past_earnings_dates=["2026-05-01", "2026-08-05"],
                                     current_source="xlsx")
    assert r["eps_revision_fy_shift"] == 1
    assert r["eps_revision_fy_shift_status"] == "shifted"
    assert r["eps_fy_curr_revision_pct"] == pytest.approx(214.38 / 212.95 * 100 - 100, abs=0.01)
    assert r["eps_fy3_revision_pct"] is None


def test_shift_back_through_compute_pairs_cur_fy2_with_base_fy1():
    snap = {"snapshot_date": "2026-09-26", "tickers": {"ACN": {
        "eps_fy_curr": 15.0, "eps_fy_next": 16.0, "eps_fy3": 17.0, "source": "yfinance"}}}
    ccy = {"ACN": {"currency": "USD", "checked": "2026-10-08"}}
    r = bds._compute_fy_eps_revision("ACN", "ACN", 14.0, 15.3, 16.5, snap, "2026-10-08", ccy, {},
                                     last_fye="2026-08-31", last_earnings_date="2026-06-25",
                                     past_earnings_dates=["2026-06-25"], current_source="xlsx")
    assert r["eps_revision_fy_shift"] == -1
    assert r["eps_fy_curr_revision_pct"] is None
    assert r["eps_fy_next_revision_pct"] == pytest.approx(15.3 / 15.0 * 100 - 100, abs=0.01)
    assert r["eps_fy3_revision_pct"] == pytest.approx(16.5 / 16.0 * 100 - 100, abs=0.01)


def test_hona_yfinance_baseline_vs_xlsx_current_past_window_no_shift():
    # spin-off: FYE 2025-12-31, first report 08-05 (>120d) is not annual; Koyfin assumed rolled
    assert fy_shift("2025-12-31", "2026-08-05", "2026-09-26", "2026-10-08", ["2026-08-05"],
                    "yfinance", "xlsx") == (0, "assumed_rolled")


def test_inside_window_without_report_stays_not_rolled():
    assert fy_shift("2026-08-31", "2026-06-25", "2026-09-26", "2026-10-08", ["2026-06-25"],
                    "yfinance", "xlsx") == (-1, "shifted_back")
    assert fy_shift("2026-08-31", "2026-06-25", "2026-09-10", "2026-10-08", ["2026-06-25"],
                    "xlsx", "xlsx") == (0, "no_annual_report")


def test_spcx_type_both_sides_past_window_no_shift():
    assert fy_shift("2025-12-31", "2026-08-04", "2026-06-23", "2026-10-08", ["2026-08-04"],
                    "xlsx", "xlsx") == (0, "assumed_rolled")
