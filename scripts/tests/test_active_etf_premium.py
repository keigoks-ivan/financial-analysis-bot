"""Unit tests for scripts/active_etf/premium.py — synthetic data, no network."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR / "active_etf"))

import premium as pm  # noqa: E402


def _codes(n):
    return [f"0098{i:02d}A" for i in range(n)]


def _pcf(codes, d, base=10.0):
    return {c: {d: base + i} for i, c in enumerate(codes)}


def test_match_picks_previous_day_when_h_is_prior_nav():
    codes = _codes(12)
    pcf = {c: {"2026-10-28": 10.0 + i, "2026-10-29": 20.0 + i} for i, c in enumerate(codes)}
    h = {c: 10.0 + i for i, c in enumerate(codes)}          # h＝10-28 的淨值
    d, counts = pm.match_nav_date(h, pcf, ["2026-10-29", "2026-10-28"])
    assert d == "2026-10-28"
    assert counts == {"2026-10-29": 0, "2026-10-28": 12}


def test_match_picks_snapshot_day_when_h_is_same_day_nav():
    codes = _codes(12)
    pcf = {c: {"2026-10-28": 10.0 + i, "2026-10-29": 20.0 + i} for i, c in enumerate(codes)}
    h = {c: 20.004 + i for i, c in enumerate(codes)}         # 四捨五入到 2 位後相符
    d, _ = pm.match_nav_date(h, pcf, ["2026-10-29", "2026-10-28"])
    assert d == "2026-10-29"


def test_match_refuses_below_minimum():
    codes = _codes(12)
    pcf = {c: {"2026-10-28": 10.0 + i} for i, c in enumerate(codes)}
    h = {c: 10.0 + i for i, c in enumerate(codes[:9])}       # 只有 9 檔
    d, counts = pm.match_nav_date(h, pcf, ["2026-10-29", "2026-10-28"])
    assert d is None and counts["2026-10-28"] == 9


def test_match_refuses_on_tie():
    codes = _codes(10)
    pcf = {c: {"2026-10-28": 10.0 + i, "2026-10-29": 10.0 + i} for i, c in enumerate(codes)}
    h = {c: 10.0 + i for i, c in enumerate(codes)}
    d, _ = pm.match_nav_date(h, pcf, ["2026-10-29", "2026-10-28"])
    assert d is None


def test_match_ignores_unreliable_fund():
    codes = _codes(9)
    pcf = {c: {"2026-10-28": 10.0 + i} for i, c in enumerate(codes)}
    pcf["00401A"] = {"2026-10-28": 13.75}                    # 即使相符也不算
    h = {c: 10.0 + i for i, c in enumerate(codes)}
    h["00401A"] = 13.75
    d, counts = pm.match_nav_date(h, pcf, ["2026-10-28"])
    assert d is None and counts["2026-10-28"] == 9


def test_premium_calc_and_source_priority():
    close = {"2026-10-27": {"00981A": 28.65}, "2026-10-28": {"00981A": 28.65}}
    twse = {"2026-10-28": {"nav": {"00981A": 28.50}}}
    pcf = {"00981A": {"2026-10-27": 28.60, "2026-10-28": 28.61}}
    r = pm.compute_premium(close, twse, pcf)["00981A"]
    assert r["series"][0] == ("2026-10-27", 0.17, 28.65, 28.60, "pcf")
    assert r["series"][1] == ("2026-10-28", 0.53, 28.65, 28.50, "twse")   # 證交所優先
    assert r["suspect"] == []


def test_00401A_pcf_never_used():
    assert "00401A" in pm.PCF_NAV_UNRELIABLE
    # load_pcf_nav 不載 00401A，所以只有證交所快照有值的日子才算得出
    close = {"2026-10-27": {"00401A": 13.0}, "2026-10-28": {"00401A": 13.76}}
    twse = {"2026-10-28": {"nav": {"00401A": 13.75}}}
    r = pm.compute_premium(close, twse, {})["00401A"]
    assert [x[0] for x in r["series"]] == ["2026-10-28"]
    assert r["series"][0][1] == 0.07 and r["series"][0][4] == "twse"


def test_suspect_filtered_out_of_series_and_stats():
    close = {f"2026-10-{d}": {"00999A": 10.0} for d in (26, 27, 28)}
    pcf = {"00999A": {"2026-10-26": 10.0, "2026-10-27": 10.8, "2026-10-28": 9.99}}
    res = pm.compute_premium(close, {}, pcf)["00999A"]
    assert [x[0] for x in res["series"]] == ["2026-10-26", "2026-10-28"]
    assert len(res["suspect"]) == 1 and res["suspect"][0]["date"] == "2026-10-27"
    s = pm.summarize("00999A", res)
    assert s["n"] == 2 and s["max_pct"]["pct"] == 0.1 and "suspect" in s
    assert s["days_over_1pct"] == 0


def test_summarize_stats():
    series = [(f"d{i:02d}", p, 1, 1, "pcf") for i, p in enumerate([1.5, -1.2, 0.0] + [0.1] * 20)]
    s = pm.summarize("00981A", {"series": series, "suspect": []})
    assert s["days_over_1pct"] == 1 and s["days_under_minus1pct"] == 1
    assert s["avg20_pct"] == 0.1 and s["latest"]["pct"] == 0.1
    assert s["max_pct"] == {"date": "d00", "pct": 1.5}


def test_parse_close_table():
    payload = {"tables": [
        {"title": "大盤統計資訊", "fields": ["a"], "data": []},
        {"title": "115年10月28日 每日收盤行情(ETF)",
         "fields": ["證券代號", "證券名稱", "成交股數", "成交筆數", "成交金額", "開盤價", "最高價", "最低價", "收盤價"],
         "data": [["00981A", "x", "1", "1", "1", "1", "1", "1", "28.65"],
                  ["0050", "y", "1", "1", "1", "1", "1", "1", "1,108.65"],
                  ["00999A", "z", "1", "1", "1", "1", "1", "1", "--"]]}]}
    assert pm.parse_close_table(payload) == {"00981A": 28.65, "0050": 1108.65}
    assert pm.parse_close_table({"tables": []}) == {}
