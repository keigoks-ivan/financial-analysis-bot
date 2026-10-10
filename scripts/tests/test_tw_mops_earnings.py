"""MOPS 董事會通過財報日 as the TW earnings-date fallback (scripts/tw_mops_earnings.py).

Subjects below are real t05st01 主旨 strings (2026-10-10 pull); no network.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import tw_mops_earnings as tme  # noqa: E402

TODAY = date(2026, 10, 10)


def test_parse_wording_variants():
    rows = [
        ("115/03/24", "公告本公司董事會通過民國114年度合併財務報表"),
        ("115/05/12", "公告本公司董事會通過民國115年第一季合併財務報表"),
        ("115/08/13", "公告本公司董事會通過民國115年第二季合併財務報表"),
        ("114/11/03", "公告本公司114年第3季合併財務報告業經董事會決議通過"),
        ("115/03/04", "本公司董事會通過114年第四季合併財務報告。"),
        ("114/10/28", "公告本公司董事會通過114年上半年度合併財務報告"),
    ]
    assert tme.parse_approvals(rows) == {
        "2025Q2": "2025-10-28", "2025Q3": "2025-11-03", "2025Q4": "2026-03-04",
        "2026Q1": "2026-05-12", "2026Q2": "2026-08-13"}


def test_parse_less_common_wordings():
    rows = [
        ("115/02/26", "本公司董事會通過民國一一四年第四季合併財務報告"),               # 緯穎
        ("115/05/13", "公告本公司向董事會提報2026年第1季合併財務報告"),                # 亞德客
        ("115/04/30", "本公司發布115年第一季財務報告"),                               # 創意
        ("115/08/10", "公告本公司董事會通過115年合併財報"),                            # 萬潤（年報）
        ("115/08/12", "公告本公司民國115年第二季合併財務報告業經董事會決議"),           # 神基
        ("115/11/06", "本公司董事會通過115年第三季自結財務資訊"),                      # AES-KY
    ]
    # 115 年合併財報 posted 115/08/10 comes before its own year end: dropped.
    assert tme.parse_approvals(rows) == {
        "2025Q4": "2026-02-26", "2026Q1": "2026-04-30", "2026Q2": "2026-08-12",
        "2026Q3": "2026-11-06"}


def test_parse_skips_notices_corrections_and_subsidiaries():
    rows = [
        ("115/05/04", "公告本公司115年第1季財務報告董事會預計召開日期"),
        ("114/07/30", "公告本公司114年第2季合併財務報告董事會預計召開日期 為114年8月7日"),
        ("115/07/22", "公告本公司上櫃前初次現金增資員工認股之費用化金額及 對財務報表之影響"),
        ("115/05/25", "公告更正本公司112~114年度合併財務報告附註部份 資訊內容"),
        ("115/08/04", "公告本公司新增資金貸與金額達新臺幣一千萬元以上且 達本公司最近期財務報表淨值百分之二以上"),
        ("115/08/10", "代子公司公告董事會通過115年第二季財務報告"),
        ("115/04/10", "公告董事會決議114年第4季 及115年第1季盈餘分派之股利配發基準日"),
        ("115/03/17", "因本公司有價證券於集中市場達公布注意交易資訊標準， 故公布相關財務業務等重大訊息"),
        ("115/02/13", "公告本公司114年度財務報告董事會預計召開日期為 115年2月26日"),
    ]
    assert tme.parse_approvals(rows) == {}


def test_parse_drops_approval_far_from_period_end_and_keeps_earliest():
    rows = [("115/08/24", "公告董事會通過115年第一季合併財務報告"),        # 146 days: kept
            ("115/08/20", "公告董事會通過115年第一季合併財務報告"),        # earlier wins
            ("116/01/05", "董事會通過115年第一季合併財務報告")]          # 280 days: dropped
    assert tme.parse_approvals(rows) == {"2026Q1": "2026-08-20"}


def test_needs_fallback():
    assert tme.needs_fallback(None, TODAY)
    assert tme.needs_fallback("2019-05-10", TODAY)
    assert tme.needs_fallback("2026-05-12", TODAY)          # Q2 deadline 8/14 has passed
    assert not tme.needs_fallback("2026-08-11", TODAY)


def test_merge_keeps_a_current_yfinance_date():
    cal = {"last_earnings_date": "2026-07-16", "next_earnings_date": "2026-10-15",
           "past_earnings_dates": ["2026-04-16", "2026-07-16"]}
    out = tme.merge(cal, {"2026Q2": "2026-08-11"}, TODAY)
    assert out["last_earnings_date"] == "2026-07-16" and out["earnings_date_source"] == "yfinance"


def test_merge_fills_missing_and_replaces_stale():
    approvals = {"2025Q4": "2026-03-24", "2026Q1": "2026-05-12", "2026Q2": "2026-08-13"}
    empty = {"last_earnings_date": None, "next_earnings_date": None, "past_earnings_dates": []}
    out = tme.merge(empty, approvals, TODAY)
    assert out["last_earnings_date"] == "2026-08-13" and out["earnings_date_source"] == "mops_board"
    assert out["past_earnings_dates"] == ["2026-03-24", "2026-05-12", "2026-08-13"]
    stale = {"last_earnings_date": "2026-05-08", "next_earnings_date": None,
             "past_earnings_dates": ["2025-11-05", "2026-03-10", "2026-05-08"]}
    out = tme.merge(stale, approvals, TODAY)
    # yfinance dates on or after MOPS coverage are dropped: one date per quarter.
    assert out["past_earnings_dates"] == ["2025-11-05", "2026-03-24", "2026-05-12", "2026-08-13"]


def test_merge_without_mops_dates_leaves_calendar_alone():
    empty = {"last_earnings_date": None, "next_earnings_date": None, "past_earnings_dates": []}
    out = tme.merge(empty, None, TODAY)
    assert out["last_earnings_date"] is None and out["earnings_date_source"] is None
    future_only = tme.merge(empty, {"2026Q3": "2026-11-10"}, TODAY)
    assert future_only["last_earnings_date"] is None


def test_prefetch_uses_cache_then_stops_after_repeated_failures():
    calls = []

    def fetch(code, roc_year):
        calls.append((code, roc_year))
        if code == "1111":
            return [("115/08/11", "董事會通過115年第二季合併財務報告")]
        return None                                          # network down

    cache = {"0001": {"approvals": {"2026Q2": "2026-08-05"}, "checked": "2026-10-09"},   # fresh
             "2000": {"approvals": {"2026Q1": "2026-05-06"}, "checked": "2026-09-01"}}   # stale
    out = tme.prefetch(["0001", "1111", "2000", "3000", "4000", "5000"], cache, TODAY,
                       fetch=fetch, sleep=lambda s: None)
    assert out["0001"] == {"2026Q2": "2026-08-05"}           # served from cache, not refetched
    assert out["1111"] == {"2026Q2": "2026-08-11"}
    assert out["2000"] == {"2026Q1": "2026-05-06"}           # fetch failed: old cache served
    assert "3000" not in out and "5000" not in out
    assert cache["1111"]["checked"] == "2026-10-10"
    assert cache["2000"]["checked"] == "2026-09-01"
    queried = [c for c, _ in calls]
    assert "0001" not in queried and "5000" not in queried   # third failure stops the run
    assert queried.count("1111") == 2                        # previous + current ROC year
