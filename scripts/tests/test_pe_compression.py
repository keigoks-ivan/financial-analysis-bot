"""EPS 上修 × 本益比壓縮（dd-screener pe_compression，日曆年基準）單元測試。"""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_dd_screener as b  # noqa: E402

AS_OF = "2026-10-08"
IDX = pd.to_datetime(["2026-07-01", "2026-10-07"])


def close(end):
    return pd.Series([100.0, end], index=IDX)


def row(fye, fy_se, fy_3m, shift=0, status="no_shift", src="xlsx", past=None,
        last_earn="2026-09-01"):
    return {
        "fiscal_year_end": fye, "eps_source": src, "past_earnings_dates": past,
        "last_earnings_date": last_earn,
        "_eps_rev_since_earnings_fy": fy_se, "_eps_rev_3m_fy": fy_3m,
        "eps_rev_since_earnings_fy_shift": shift, "eps_rev_since_earnings_fy_shift_status": status,
        "eps_rev_since_earnings_baseline_date": "2026-07-01",
        "eps_rev_3m_fy_shift": shift, "eps_rev_3m_fy_shift_status": status,
        "eps_rev_3m_baseline_date": "2026-07-01",
        "fund": {"pe_ntm_x": 20, "pe_ntm_5y_avg_x": 20},
    }


def test_dec_fye_maps_columns_1_2_3():
    r = row("2025-12-31", [3, 8, 12], [1, 6, 9], past=["2026-02-20", "2026-09-01"])
    pc = b.compute_pe_compression(r, close(70.0), AS_OF)
    assert pc["display_years"] == [2026, 2027, 2028] and pc["condition_years"] == [2027, 2028]
    assert pc["fy_codes"] == {"2026": "FY26", "2027": "FY27", "2028": "FY28"}
    assert pc["since_earnings"]["revs"] == {"2026": 3, "2027": 8, "2028": 12}
    assert pc["since_earnings"]["eps_cond1_chg"] == 8
    assert pc["since_earnings"]["pe_chg_pct"] == pytest.approx(-35.19, abs=0.01)
    assert pc["match"] and pc["match_windows"] == ["since_earnings", "3m"]
    assert "_eps_rev_3m_fy" not in r


def test_mu_type_rolled_row_maps_none_1_2():
    # Aug FYE, FY26 reported in Sep: snapshot FY1 = FY27 (ends 2027-08) -> 2026 has no column
    r = row("2026-08-31", [20, 25, None], [10, 15, None], shift=1, status="shifted",
            past=["2026-09-24"])
    pc = b.compute_pe_compression(r, close(80.0), AS_OF)
    assert pc["fy_codes"] == {"2026": None, "2027": "FY27", "2028": "FY28"}
    assert pc["since_earnings"]["revs"] == {"2026": None, "2027": 20, "2028": 25}
    assert pc["since_earnings"]["pass"] is True
    assert pc["3m"]["pass"] is True  # 10/15 >= 5, pe -(1-0.8/1.1)


def test_jan_fye_counts_toward_prior_calendar_year():
    # FYE Jan 2026 -> calendar 2025; snapshot FY1 ends 2027-01 -> calendar 2026 (col 1)
    r = row("2026-01-31", [5, 6, 7], [5, 6, 7], past=["2026-03-10"])
    pc = b.compute_pe_compression(r, close(60.0), AS_OF)
    assert pc["since_earnings"]["revs"] == {"2026": 5, "2027": 6, "2028": 7}
    assert pc["fy_codes"] == {"2026": "FY27", "2027": "FY28", "2028": "FY29"}


def test_unknown_status_window_not_judged_other_window_ok():
    r = row("2025-12-31", [9, 9, 9], [9, 9, 9], past=["2026-02-20", "2026-09-01"])
    r["eps_rev_since_earnings_fy_shift_status"] = "unknown"
    pc = b.compute_pe_compression(r, close(50.0), AS_OF)
    se = pc["since_earnings"]
    assert se["revs"] == {"2026": None, "2027": None, "2028": None}
    assert se["pass"] is False and se["pe_chg_pct"] is None
    assert pc["3m"]["pass"] is True and pc["match_windows"] == ["3m"]


def test_shift_minus1_not_judged():
    r = row("2025-12-31", [9, 9, 9], [9, 9, 9], shift=-1, status="shifted_back",
            past=["2026-02-20", "2026-09-01"])
    pc = b.compute_pe_compression(r, close(50.0), AS_OF)
    assert not pc["match"]


def test_pe_chg_and_guard():
    assert b.pe_compress_pe_chg(0.0, 25.0) == pytest.approx(-20.0)
    assert b.pe_compress_pe_chg(0.0, -99.9) is None
    assert b.pe_compress_pe_chg(None, 10) is None


def test_price_uses_first_close_on_or_after_base():
    c = pd.Series([50.0, 100.0, 80.0], index=pd.to_datetime(["2026-06-30", "2026-07-02", "2026-10-07"]))
    assert b.pe_compress_price_chg(c, "2026-07-01") == pytest.approx(-20.0)


def test_pass_thresholds_boundary():
    cols = {2026: 1, 2027: 2, 2028: 3}
    dy, cy = (2026, 2027, 2028), (2027, 2028)
    ok = b.pe_compress_window([0, 5, 5], 0, "no_shift", "2026-07-01", close(94.5), cols, dy, cy)
    assert ok["pe_chg_pct"] <= -10 and ok["pass"]
    no = b.pe_compress_window([0, 5, 5], 0, "no_shift", "2026-07-01", close(95.0), cols, dy, cy)
    assert no["pe_chg_pct"] > -10 and not no["pass"]
    low = b.pe_compress_window([0, 4.9, 20], 0, "no_shift", "2026-07-01", close(50.0), cols, dy, cy)
    assert not low["pass"]
    # only first condition year available -> cannot pass
    part = b.pe_compress_window([20, 20, 20], 1, "shifted", "2026-07-01", close(50.0),
                                {2026: None, 2027: 1, 2028: None}, dy, cy)
    assert part["revs"]["2028"] is None and not part["pass"]


def test_flags():
    t = date(2026, 10, 8)
    w = {"since_earnings": {"revs": {"2026": 150, "2027": 5, "2028": 5}}, "3m": {"revs": {}}}
    assert b.pe_compress_flags(w, "2026-09-01", 1.0, t, {2027, 2028}) == []   # 2026 not a condition year
    assert b.pe_compress_flags(w, "2026-09-01", 1.0, t, {2026, 2027}) == ["big_move"]
    w2 = {"a": {"revs": {"2027": 99.9, "2028": 5}}}
    assert b.pe_compress_flags(w2, None, 0.29, t, {2027, 2028}) == ["earnings_date_odd", "pe5y_gap"]
    assert b.pe_compress_flags({}, "2026-03-01", 3.01, t) == ["earnings_date_odd", "pe5y_gap"]
    assert b.pe_compress_flags({}, "2026-03-22", 3.0, t) == []
