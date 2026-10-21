"""2026-10-21 早報用台股寬名單 build_tw_wide_eps.py：換匯、CAGR、year-ago 沿用、輸出能被
morning-briefing dd_numbers.facts() 的欄位讀法吃下。純函式，不碰網路。"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_dd_screener as bds  # noqa: E402
import build_tw_wide_eps as bw  # noqa: E402

REC = {"fy1": 3.38, "fy2": 4.56, "fy3": 5.82, "roic_pct": 30.34, "cagr_fy1_fy3_pct": None}
LISTING = {"ticker": "2330.TW", "name": "台積電", "market": "TWSE", "industry": "半導體業"}


def facts_like_dd_numbers(s: dict):
    """morning-briefing/briefing/dd_numbers.facts() 讀的欄位（該檔只在 morning-briefing repo）。"""
    seq = [s.get("eps_year_ago"), s.get("eps_fy_curr"), s.get("eps_fy_next"), s.get("eps_fy3")]
    return seq, s.get("roic"), s.get("eps_fy1_fy3_cagr_pct"), s.get("eps_display_currency")


def test_usd_to_local():
    assert bw.usd_to_local(3.38, 32.456) == 109.7
    assert bw.usd_to_local(None, 32.456) is None
    assert bw.usd_to_local(3.38, None) is None


def test_cagr_uses_main_definition():
    assert bds._koyfin_eps_growth(REC, "fy1_fy3") == 31.22
    assert bds._koyfin_eps_growth({"fy1": -1.0, "fy3": 2.0}, "fy1_fy3") is None   # FY1<=0 -> None（金融／虧損股）


def test_build_row_fields_and_usd_orig():
    ya = {"eps_year_ago": 66.25, "eps_year_ago_fye": "2025-12-31", "eps_year_ago_source": "yfinance"}
    row = bw.build_row("2330", REC, LISTING, 32.456, ya, "2025-12-31", bds._koyfin_eps_growth)
    assert row["ticker"] == "2330.TW" and row["name"] == "台積電"
    assert (row["eps_fy_curr"], row["eps_fy_next"], row["eps_fy3"]) == (109.7, 148.0, 188.89)
    assert (row["eps_fy_curr_usd_orig"], row["eps_fy3_usd_orig"]) == (3.38, 5.82)
    assert row["eps_display_currency"] == "TWD" and row["eps_fx_rate"] == 32.456
    assert row["roic"] == 30.34 and row["eps_fy1_fy3_cagr_pct"] == 31.22
    seq, roic, cagr, ccy = facts_like_dd_numbers(row)
    assert seq == [66.25, 109.7, 148.0, 188.89] and roic == 30.34 and cagr == 31.22 and ccy == "TWD"


def test_build_row_unresolved_keeps_bare_code():
    row = bw.build_row("9999", {"fy1": None, "fy2": None, "fy3": None, "roic_pct": None}, None, 32.0,
                       {}, None, bds._koyfin_eps_growth)
    assert row["ticker"] == "9999" and row["name"] == "9999"
    assert row["eps_fy_curr"] is None and row["eps_fy1_fy3_cagr_pct"] is None and row["eps_year_ago"] is None


def test_year_ago_carry_before_fetch_and_fye_roll():
    prev_wide = {"2330.TW": {"eps_year_ago": 66.25, "eps_year_ago_fye": "2025-12-31"}}
    prev_main = {"2881.TW": {"eps_year_ago": 5.0, "eps_year_ago_fye": "2025-12-31"}}
    rows = [("carried", prev_wide), ("carried_main", prev_main)]
    calls = []

    def fetch(t):
        calls.append(t)
        return {"eps_year_ago": 1.23}

    a = bw.pick_year_ago("2330", "2330.TW", "2025-12-31", rows, fetch, bds.decide_year_ago_carry)
    b = bw.pick_year_ago("2881", "2881.TW", "2025-12-31", rows, fetch, bds.decide_year_ago_carry)
    c = bw.pick_year_ago("2330", "2330.TW", "2026-12-31", rows, fetch, bds.decide_year_ago_carry)  # 財年換了
    assert (a["eps_year_ago"], a["eps_year_ago_source"]) == (66.25, "carried")
    assert (b["eps_year_ago"], b["eps_year_ago_source"]) == (5.0, "carried_main")
    assert (c["eps_year_ago"], c["eps_year_ago_source"]) == (1.23, "yfinance")
    assert calls == ["2330.TW"]


def test_year_ago_missing_gives_none_source():
    r = bw.pick_year_ago("1", "1.TW", "2025-12-31", [], lambda t: {}, bds.decide_year_ago_carry)
    assert r == {"eps_year_ago": None, "eps_year_ago_fye": "2025-12-31", "eps_year_ago_source": None}


def test_seed_fye_cache_prefers_shared_then_latest_json():
    shared = {"2330.TW": {"last_fye": "2025-12-31", "checked": "2026-10-01"}}
    wide = {"as_of": "2026-10-21", "stocks": [{"ticker": "2330.TW", "fiscal_year_end": "2024-12-31"},
                                              {"ticker": "2881.TW", "fiscal_year_end": "2025-12-31"}]}
    c = bw.seed_fye_cache(shared, wide, {})
    assert c["2330.TW"]["last_fye"] == "2025-12-31"
    assert c["2881.TW"] == {"last_fye": "2025-12-31", "checked": "2026-10-21"}
