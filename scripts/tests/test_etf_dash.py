"""Unit tests for scripts/etf_dash/build_etf_dash.py — VanEck holdings xlsx
parsing and the yfinance rate-limit detector.

The parser is the riskiest bit of the pipeline (VanEck's US and IE fund pages
export slightly different column layouts/counts for "Download All Holdings",
see build_etf_dash.py::parse_holdings_xlsx docstring reasoning), so this
builds small synthetic xlsx files in-memory (openpyxl) that mirror both real
layouts observed on 2026-09-24, rather than depending on a fixture file or
network access. No network, no dependency on docs/dd-screener/latest.json.
"""
from __future__ import annotations

import io
import shutil
from datetime import datetime
from pathlib import Path
import sys

import openpyxl
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "etf_dash"))

import build_etf_dash as m  # noqa: E402
import dd_eps_history as ddh  # noqa: E402


def _xlsx_bytes(rows: list[list]) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── US-layout sheet: Number, Ticker, Holding Name, Identifier (FIGI), Shares,
#    Asset Class, Market Value (US$), Notional Value, % of Net Assets ────────

def test_parse_holdings_xlsx_us_layout():
    raw = _xlsx_bytes([
        # 2026-09-24 實測：VanEck 匯出的 xlsx 標題＋日期是同一個儲存格裡的組合字串
        # （"Daily Holdings (%)  09/22/2026"），不是分開兩欄。
        ["Daily Holdings (%)  09/22/2026", None, None, None, None, None, None, None, None],
        [None] * 9,
        ["Number", "Ticker", "Holding Name", "Identifier (FIGI)", "Shares", "Asset Class",
         "Market Value (US$)", "Notional Value", "% of Net Assets"],
        [1, "NVDA", "Nvidia Corp", "BBG000BBJQV0", 1000, "Stock", "$100.00", "--", "19.43%"],
        [2, "TSM", "Taiwan Semiconductor Manufacturing Co L", "BBG000BD8ZK0", 2000, "Stock",
         "$50.00", "--", "9.17%"],
        [3, "-USD CASH-", None, None, 500, "Cash Bal", "$5.00", "--", "0.00%"],
        [4, "--", "Other/Cash", "--", "--", "Cash", "$1.00", "--", "0.06%"],
        ["These are not recommendations to buy or to sell any security."],
    ])
    as_of, rows = m.parse_holdings_xlsx(raw)
    assert as_of == "2026-09-22"
    # cash lines (ticker "-USD CASH-" and name "Other/Cash") both excluded
    assert [r["ticker"] for r in rows] == ["NVDA", "TSM"]
    assert rows[0]["weight_pct"] == pytest.approx(19.43)
    assert rows[1]["name"] == "Taiwan Semiconductor Manufacturing Co L"


# ── IE-layout sheet: Number, Holding Name, Ticker, ISIN, Shares, Market
#    Value, % of Net Assets — note Ticker has a " US" suffix here ───────────

def test_parse_holdings_xlsx_ie_layout_strips_exchange_suffix():
    raw = _xlsx_bytes([
        ["All Holdings  09/23/2026", None, None, None, None, None, None],
        [None] * 7,
        ["Number", "Holding Name", "Ticker", "ISIN", "Shares", "Market Value", "% of Net Assets"],
        [1, "Advanced Micro Devices Inc", "AMD US", "US0079031078", 500, "$ 10.00", "11.15%"],
        [2, "Entegris Inc", "ENTG US", "US29362U1043", 300, "$ 5.00", "0.19%"],
        [3, "Other/Cash", "--", "--", "--", "$ 0.10", "0.06%"],
    ])
    as_of, rows = m.parse_holdings_xlsx(raw)
    assert as_of == "2026-09-23"
    assert [r["ticker"] for r in rows] == ["AMD", "ENTG"]  # " US" suffix stripped
    assert rows[0]["raw_ticker_field"] == "AMD US"
    assert rows[1]["weight_pct"] == pytest.approx(0.19)


def test_parse_holdings_xlsx_missing_header_raises():
    raw = _xlsx_bytes([["not", "a", "holdings", "sheet"]])
    with pytest.raises(RuntimeError, match="header row"):
        m.parse_holdings_xlsx(raw)


def test_parse_holdings_xlsx_no_data_rows_raises():
    raw = _xlsx_bytes([
        ["All Holdings  09/23/2026"],
        [None],
        ["Number", "Holding Name", "Ticker", "ISIN", "Shares", "Market Value", "% of Net Assets"],
        ["These are not recommendations to buy or to sell any security."],
    ])
    with pytest.raises(RuntimeError, match="parsed 0 holdings"):
        m.parse_holdings_xlsx(raw)


# ── SPY (SSGA) holdings xlsx — 2026-09-24 real layout: Name/Ticker/Identifier/
#    SEDOL/Weight/Sector/Shares Held/Local Currency, Weight is numeric (not a
#    "19.43%" string), "As of DD-Mon-YYYY" sits in a Fund Name/Ticker/Holdings
#    header block before the column header row. Dot-tickers (BRK.B), a cash
#    line (ticker "-"), and a CVR line (numeric-looking ticker) all appear in
#    the real file (see build_etf_dash.py's TICKER_ALIAS / EQUITY_TICKER_RE
#    comments) ────────────────────────────────────────────────────────────

def test_parse_ssga_holdings_xlsx_basic():
    raw = _xlsx_bytes([
        ["Fund Name:", "State Street® SPDR® S&P 500® ETF Trust", None, None, None, None, None, None],
        ["Ticker Symbol:", "SPY", None, None, None, None, None, None],
        ["Holdings:", "As of 23-Sep-2026", None, None, None, None, None, None],
        [None] * 8,
        ["Name", "Ticker", "Identifier", "SEDOL", "Weight", "Sector", "Shares Held", "Local Currency"],
        ["NVIDIA CORP", "NVDA", "67066G104", "2379504", 8.217272, "-", 298385133, "USD"],
        ["BERKSHIRE HATHAWAY INC CL B", "BRK.B", "084670702", "2073390", 1.422268, "-", 22963774, "USD"],
        ["US DOLLAR", "-", "999USDZ92", None, 0.210631, "-", 1724799064.7, "USD"],
        ["TPG INC", "2602335D", "436CVR021", None, 0.000003, "-", 2578626, "USD"],
        [None] * 8,  # 實測：資料列與免責聲明段落之間有一列全空
        ["Before investing in a fund, consider its investment objectives...", None, None, None, None, None, None, None],
    ])
    as_of, rows, non_equity = m.parse_ssga_holdings_xlsx(raw)
    assert as_of == "2026-09-23"
    assert [r["ticker"] for r in rows] == ["NVDA", "BRK.B"]
    assert rows[1]["weight_pct"] == pytest.approx(1.422268)
    # cash line + CVR line both excluded as non-equity, weight preserved
    assert {e["ticker"] for e in non_equity} == {None, "2602335D"}
    weights = {e["ticker"]: e["weight_pct"] for e in non_equity}
    assert weights[None] == pytest.approx(0.210631)
    assert weights["2602335D"] == pytest.approx(0.000003)
    assert "CVR" in non_equity[1]["reason"] or "特殊" in non_equity[1]["reason"]


def test_parse_ssga_holdings_xlsx_missing_header_raises():
    raw = _xlsx_bytes([["not", "a", "holdings", "sheet"]])
    with pytest.raises(RuntimeError, match="header row"):
        m.parse_ssga_holdings_xlsx(raw)


def test_ticker_alias_dot_to_dash():
    assert m.TICKER_ALIAS["BRK.B"] == "BRK-B"
    assert m.TICKER_ALIAS["BF.B"] == "BF-B"


# ── QQQ (Invesco) holdings JSON — 2026-09-24 real shape from
#    dng-api.invesco.com .../holdings/fund: {"effectiveDate","holdings":[...]}
#    with COM/ADR/DRNY as real equities and CURR/CURRCOL/IFUT/SYN as
#    cash/futures/synthetic offset lines (SYN often carries a negative
#    weight); one row (USDPDV) has percentageOfTotalNetAssets: null ─────────

def _invesco_fixture():
    return {
        "cusip": "QQQ", "effectiveDate": "2026-09-23", "effectiveBusinessDate": "2026-09-23",
        "totalNumberOfHoldings": 6,
        "holdings": [
            {"ticker": "NVDA", "issuerName": "NVIDIA Corp", "units": 1, "percentageOfTotalNetAssets": 8.22,
             "securityTypeName": "Common Stock", "securityTypeCode": "COM", "currency": "USD"},
            {"ticker": "ASML", "issuerName": "ASML Holding NV", "units": 1, "percentageOfTotalNetAssets": 0.68,
             "securityTypeName": "NY Registry Shares", "securityTypeCode": "DRNY", "currency": "USD"},
            {"ticker": "USD", "issuerName": "CASH & EQUIVALENTS", "units": 1, "percentageOfTotalNetAssets": 0.20,
             "securityTypeName": "Currency", "securityTypeCode": "CURR", "currency": "USD"},
            {"ticker": "NQZ6", "issuerName": "CME E-Mini NASDAQ 100 Index Future", "units": 1,
             "percentageOfTotalNetAssets": 0.14, "securityTypeName": "Index Future", "securityTypeCode": "IFUT",
             "currency": "USD"},
            {"ticker": None, "issuerName": "CONTRA FUTURE NASDAQ 100 E-MINI DEC26NQZ6", "units": 1,
             "percentageOfTotalNetAssets": -0.14, "securityTypeName": "Synthetic", "securityTypeCode": "SYN",
             "currency": "USD"},
            {"ticker": "USDPDV", "issuerName": "USD Pending Dividends", "units": 0,
             "percentageOfTotalNetAssets": None, "securityTypeName": "Currency", "securityTypeCode": "CURR",
             "currency": "USD"},
        ],
    }


def test_parse_invesco_holdings_json_basic():
    as_of, rows, non_equity = m.parse_invesco_holdings_json(_invesco_fixture())
    assert as_of == "2026-09-23"
    assert [r["ticker"] for r in rows] == ["NVDA", "ASML"]
    assert len(non_equity) == 4
    ne_tickers = {e["ticker"] for e in non_equity}
    assert ne_tickers == {"USD", "NQZ6", None, "USDPDV"}
    # negative-weight synthetic offset line's weight is preserved, not dropped or clamped
    syn = next(e for e in non_equity if e["name"].startswith("CONTRA FUTURE"))
    assert syn["weight_pct"] == pytest.approx(-0.14)


def test_parse_invesco_holdings_json_missing_holdings_raises():
    with pytest.raises(RuntimeError, match="missing effectiveDate or holdings"):
        m.parse_invesco_holdings_json({"effectiveDate": "2026-09-23", "holdings": []})


def test_parse_invesco_holdings_json_all_non_equity_raises():
    data = {"effectiveDate": "2026-09-23", "holdings": [
        {"ticker": "USD", "issuerName": "CASH", "percentageOfTotalNetAssets": 100.0,
         "securityTypeCode": "CURR"},
    ]}
    with pytest.raises(RuntimeError, match="0 equity holdings"):
        m.parse_invesco_holdings_json(data)


# ── yfinance rate-limit detector ─────────────────────────────────────────────

class _FakeYFRateLimitError(Exception):
    pass


def test_is_rate_limited_matches_by_class_name():
    assert m._is_rate_limited(_FakeYFRateLimitError("slow down")) is True


def test_is_rate_limited_matches_429_message():
    assert m._is_rate_limited(RuntimeError("HTTP 429 Too Many Requests")) is True


def test_is_rate_limited_false_for_unrelated_error():
    assert m._is_rate_limited(ValueError("bad ticker")) is False


# ── classify_revision() — per-constituent-period EPS revision% validity/cap ──
# 2026-09-24: persisted holdings backed out these real base EPS values from the
# QQQ/SPY build that shipped -17.1%/absurd numbers (coordinator caught it
# before it went live):
#   - ECHO (SPY) 60d/90d: current=22.73, base≈-0.114 (negative) -> raw ≈ -20039%
#     — a genuine sign-flip/near-zero base, not a real revision. Must exclude.
#   - SPCX (QQQ) 90d: current=1.8627, base≈-0.236 (negative) -> raw ≈ -889%
#     — same negative-base pattern. Must exclude.
#   - SPCX (QQQ) 60d: current=1.8627, base≈0.653 -> raw ≈ +185%. Base is
#     positive and not "tiny" by the 0.2× ratio (0.653/1.8627≈0.35 ≥ 0.2), so
#     rule 1 does NOT exclude it — it's rule 2's job to cap it to +50%.
#   - HON (QQQ) 90d: current=9.939, base≈22.891 -> raw ≈ -56.58%. Base is
#     larger than current (a real, large EPS-estimate drop, from Honeywell's
#     spin-off restating the "next FY" number) — not caught by the tiny-base
#     rule either, so it's also rule 2's job: capped to -50%, not excluded.

def test_classify_revision_no_base_is_not_an_error():
    assert m.classify_revision(None, 10.0) == ("no_base", None, None, None)
    assert m.classify_revision(0.0, 10.0) == ("no_base", None, None, None)


def test_classify_revision_excludes_negative_base_echo_style():
    status, reason, raw_pct, capped_pct = m.classify_revision(-0.114, 22.73)
    assert status == "invalid_base"
    assert reason is not None
    assert raw_pct is None and capped_pct is None


def test_classify_revision_excludes_negative_base_spcx_90d_style():
    status, reason, raw_pct, capped_pct = m.classify_revision(-0.236, 1.8627)
    assert status == "invalid_base"
    assert raw_pct is None and capped_pct is None


def test_classify_revision_excludes_tiny_positive_base():
    # base is positive but far below the 0.2x(current) floor -> still unstable
    status, reason, raw_pct, capped_pct = m.classify_revision(0.05, 2.0)
    assert status == "invalid_base"
    assert "過小" in reason
    assert raw_pct is None and capped_pct is None


def test_classify_revision_excludes_current_le_zero():
    status, reason, raw_pct, capped_pct = m.classify_revision(10.0, 0.0)
    assert status == "invalid_base"
    assert raw_pct is None and capped_pct is None


def test_classify_revision_caps_large_positive_spcx_60d_style():
    # base=0.653 is NOT "tiny" relative to current=1.8627 (ratio ≈0.35 ≥ 0.2)
    # -> not excluded, but the +185% raw move gets capped to +50%.
    status, reason, raw_pct, capped_pct = m.classify_revision(0.65307, 1.8627)
    assert status == "capped"
    assert raw_pct == pytest.approx(185.2, abs=0.5)
    assert capped_pct == 50.0


def test_classify_revision_caps_large_negative_hon_90d_style():
    # base=22.891 is LARGER than current=9.939 (ratio well above 0.2) -> not
    # excluded by the tiny-base rule, but -56.6% still gets capped to -50%.
    status, reason, raw_pct, capped_pct = m.classify_revision(22.891, 9.939)
    assert status == "capped"
    assert raw_pct == pytest.approx(-56.6, abs=0.5)
    assert capped_pct == -50.0


def test_classify_revision_ok_normal_move_not_capped():
    status, reason, raw_pct, capped_pct = m.classify_revision(10.0, 10.5)
    assert status == "ok"
    assert raw_pct == capped_pct == 5.0


def test_classify_revision_boundary_exactly_50_not_capped():
    status, _, raw_pct, capped_pct = m.classify_revision(10.0, 15.0)  # exactly +50%
    assert status == "ok"
    assert raw_pct == capped_pct == 50.0


def test_classify_revision_boundary_ratio_exactly_0_2_not_excluded():
    # |base| == 0.2 * |current| is the boundary — spec says "< 0.2x" excludes,
    # so exactly-equal must NOT be excluded (still subject to capping if large).
    status, _, raw_pct, capped_pct = m.classify_revision(2.0, 10.0)
    assert status in ("ok", "capped")  # not "invalid_base"


# ── classify_eps_step() — long-history EPS index rollover/anomaly detector ──
# Real fixtures pulled from data/etf_dash/dd_eps_history.jsonl during the
# 2026-09-24 build (see build_etf_dash.py's classify_eps_step docstring and
# KNOWN_ANOMALY_EXPLANATIONS): KLAC did a real 10:1 split on 2026-06-12 that
# Koyfin's eps_fy_next/eps_fy3 fields didn't reflect until 07-16 (both drop
# ~9.7x together that day); TSM's dd-screener pipeline started applying the
# ADR share ratio on 09-16 (both fields jump ~4.9x together); and this
# synthetic case has a jump large enough to be an anomaly but not close
# enough to either specific pattern — it must not silently fall through to
# "normal".

def test_classify_eps_step_normal_small_move():
    assert m.classify_eps_step(10.0, 15.0, 10.3, 15.0) == ("normal", 10.0)


def test_classify_eps_step_rollover_fy3_continuity():
    # cur_nxt (15.1) is within 3% of p_fy3 (15.0) -> fiscal-year rollover
    step_type, baseline = m.classify_eps_step(10.0, 15.0, 15.1, None)
    assert step_type == "rollover"
    assert baseline == 15.0


def test_classify_eps_step_scale_anomaly_klac_style():
    # KLAC 2026-07-15 -> 2026-07-16: both eps_fy_next and eps_fy3 drop ~9.7x together
    step_type, baseline = m.classify_eps_step(49.85, 59.14, 5.12, 6.24)
    assert step_type == "scale_anomaly"
    assert baseline is None


def test_classify_eps_step_scale_anomaly_tsm_style():
    # TSM 2026-09-15 -> 2026-09-16: both jump ~4.9x together (the reverse direction)
    step_type, baseline = m.classify_eps_step(4.51, 5.73, 22.3, 28.3)
    assert step_type == "scale_anomaly"


def test_classify_eps_step_unconfirmed_anomaly_no_fy3():
    # TSM 2026-05-19 -> 2026-05-20: -80% single step, eps_fy3 not populated yet
    step_type, baseline = m.classify_eps_step(19.29, None, 3.86, None)
    assert step_type == "unconfirmed_anomaly"
    assert baseline is None


def test_classify_eps_step_large_jump_not_matching_either_pattern_is_not_normal():
    # A 6x jump where fy3 also moved (~5.4x) but not tightly enough to match the
    # scale-anomaly ratio tolerance, and not close enough to fy3 for rollover —
    # must still be rejected, not silently accepted as a genuine revision.
    step_type, baseline = m.classify_eps_step(10.0, 12.0, 60.0, 65.0)
    assert step_type == "unconfirmed_anomaly"
    assert baseline is None


def test_classify_eps_step_missing_or_nonpositive_inputs_is_normal_noop():
    assert m.classify_eps_step(None, 10.0, 12.0, 13.0) == ("normal", None)
    assert m.classify_eps_step(10.0, 10.0, 0.0, 10.0) == ("normal", 10.0)


# ── dd_eps_history.py — append-only JSONL cache ──────────────────────────────
# 2026-09-24: converted from a single dict-of-dict JSON (rewritten whole on
# every run) to append-only JSONL, since the repo is public and a multi-MB
# file rewritten daily bloats git history. Tests point JSONL_PATH at a tmp
# file so they never touch the real data/etf_dash/dd_eps_history.jsonl.

@pytest.fixture()
def tmp_jsonl(tmp_path, monkeypatch):
    p = tmp_path / "dd_eps_history.jsonl"
    monkeypatch.setattr(ddh, "JSONL_PATH", p)
    return p


def _fake_latest_json(tmp_path, stocks):
    p = tmp_path / "latest.json"
    p.write_text(__import__("json").dumps({"stocks": stocks}), encoding="utf-8")
    return p


def test_append_today_writes_one_line_and_drops_nulls_only_tickers(tmp_path, tmp_jsonl):
    stocks = [
        {"ticker": "NVDA", "eps_fy_next": 15.68, "eps_fy3": 21.06, "eps_display_currency": "USD"},
        {"ticker": "NODATA"},  # all six FIELDS are None -> dropped
    ]
    latest = _fake_latest_json(tmp_path, stocks)
    ok = ddh.append_today(latest_json_path=latest, date_str="2026-05-19")
    assert ok is True
    lines = tmp_jsonl.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    days = ddh.load_days()
    assert set(days.keys()) == {"2026-05-19"}
    assert set(days["2026-05-19"]["tickers"].keys()) == {"NVDA"}
    assert days["2026-05-19"]["tickers"]["NVDA"]["eps_fy_next"] == 15.68
    assert days["2026-05-19"]["tickers"]["NVDA"]["eps_fy3"] == 21.06


def test_append_today_same_day_rewrites_last_line_only(tmp_path, tmp_jsonl):
    latest1 = _fake_latest_json(tmp_path, [{"ticker": "NVDA", "eps_fy_next": 15.0}])
    ddh.append_today(latest_json_path=latest1, date_str="2026-05-20")
    latest_prior_day = _fake_latest_json(tmp_path, [{"ticker": "NVDA", "eps_fy_next": 14.0}])
    ddh.append_today(latest_json_path=latest_prior_day, date_str="2026-05-19")
    # 2026-05-19 got appended AFTER 2026-05-20 here (out-of-order on purpose) —
    # append_today only special-cases "same date as the LAST line", so this
    # becomes a genuine second line, not a rewrite. Now rerun 2026-05-19 with
    # different data while it's still the last line -> must rewrite in place.
    latest2 = _fake_latest_json(tmp_path, [{"ticker": "NVDA", "eps_fy_next": 16.0}])
    ddh.append_today(latest_json_path=latest2, date_str="2026-05-19")
    lines = tmp_jsonl.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2  # still 2 lines, not 3 — last line was replaced in place
    days = ddh.load_days()
    assert days["2026-05-19"]["tickers"]["NVDA"]["eps_fy_next"] == 16.0
    assert days["2026-05-20"]["tickers"]["NVDA"]["eps_fy_next"] == 15.0


def test_append_today_missing_latest_json_is_noop(tmp_path, tmp_jsonl):
    ok = ddh.append_today(latest_json_path=tmp_path / "does-not-exist.json", date_str="2026-05-19")
    assert ok is False
    assert not tmp_jsonl.exists()


def test_get_usd_value_prefers_usd_orig_field():
    rec = {"eps_fy_next": 87.7, "eps_fy_next_usd_orig": 17.54}  # TWD-displayed post-v1.8.5 style
    assert ddh.get_usd_value(rec, "eps_fy_next") == 17.54


def test_get_usd_value_falls_back_to_raw_field_pre_v185():
    rec = {"eps_fy_next": 21.9, "eps_fy_next_usd_orig": None}
    assert ddh.get_usd_value(rec, "eps_fy_next") == 21.9


# ── decide_mode() — tiered update FULL vs PRICE decision ────────────────────
# 2026-09-24：SPY 規模到 ~500 檔，每天整套重抓 eps_trend 沒必要（EPS 估計本
# 來就是月頻更新）。FULL（持股下載＋逐檔 eps_trend）只在週六（台北時區）、
# 或 EPS 快取遺失／過舊、或明示 --mode full 時才跑；其餘日子用 PRICE（只抓
# 股價，EPS 沿用快取）。

def test_decide_mode_explicit_cli_mode_wins_over_everything():
    # 就算是週六、快取也新鮮，--mode price 明示還是照做
    saturday = datetime(2026, 9, 26)  # 2026-09-26 是台北時區的週六
    fresh_cache = {"eps_as_of": "2026-09-26"}
    assert m.decide_mode("price", fresh_cache, saturday)[0] == "price"
    assert m.decide_mode("full", fresh_cache, datetime(2026, 9, 21))[0] == "full"


def test_decide_mode_saturday_forces_full():
    saturday = datetime(2026, 9, 26)
    assert saturday.weekday() == 5
    fresh_cache = {"eps_as_of": "2026-09-26"}
    mode, reason = m.decide_mode("auto", fresh_cache, saturday)
    assert mode == "full"
    assert "週六" in reason


def test_decide_mode_missing_cache_forces_full():
    sunday = datetime(2026, 9, 27)
    mode, reason = m.decide_mode("auto", None, sunday)
    assert mode == "full"
    assert "沒有 EPS 快取" in reason


def test_decide_mode_stale_cache_forces_full():
    sunday = datetime(2026, 9, 27)
    stale_cache = {"eps_as_of": "2026-09-12"}  # 15 天前，超過 7 天門檻
    mode, reason = m.decide_mode("auto", stale_cache, sunday)
    assert mode == "full"
    assert "天沒更新" in reason


def test_decide_mode_fresh_cache_non_saturday_is_price():
    sunday = datetime(2026, 9, 27)
    fresh_cache = {"eps_as_of": "2026-09-26"}  # 昨天，1 天前
    mode, reason = m.decide_mode("auto", fresh_cache, sunday)
    assert mode == "price"


def test_decide_mode_cache_exactly_at_boundary_still_price():
    # 恰好 7 天門檻本身不算超過（> 7，不是 >=7）
    day = datetime(2026, 9, 27)
    cache = {"eps_as_of": "2026-09-20"}  # 恰好 7 天前
    mode, _ = m.decide_mode("auto", cache, day)
    assert mode == "price"


def test_decide_mode_malformed_eps_as_of_forces_full():
    sunday = datetime(2026, 9, 27)
    bad_cache = {"eps_as_of": "not-a-date"}
    mode, reason = m.decide_mode("auto", bad_cache, sunday)
    assert mode == "full"
    assert "格式壞掉" in reason


# ── decide_mode() full_refresh="monthly" — 2026-09-25 持有人拍板：TOPIX（日股
#    持股與 EPS 預估變動慢）FULL 只需要每月第一個週六，不是每週六；其餘六檔
#    沒有 full_refresh 鍵，decide_mode() 預設 "weekly"，行為與上面既有測試
#    完全不變。────────────────────────────────────────────────────────────

def test_is_first_saturday_of_month():
    assert m.is_first_saturday_of_month(datetime(2026, 9, 5).date()) is True   # 2026-09 的第一個週六
    assert m.is_first_saturday_of_month(datetime(2026, 9, 12).date()) is False  # 第二個週六
    assert m.is_first_saturday_of_month(datetime(2026, 10, 3).date()) is True   # 2026-10 的第一個週六


def test_decide_mode_monthly_first_saturday_forces_full():
    first_saturday = datetime(2026, 9, 5)
    assert first_saturday.weekday() == 5
    fresh_cache = {"eps_as_of": "2026-08-01"}  # 也可以是完全過期，這裡確認「第一個週六」本身就足夠
    mode, reason = m.decide_mode("auto", fresh_cache, first_saturday, "monthly")
    assert mode == "full"
    assert "本月第一個週六" in reason


def test_decide_mode_monthly_non_first_saturday_is_price_if_fresh():
    second_saturday = datetime(2026, 9, 12)
    assert second_saturday.weekday() == 5
    fresh_cache = {"eps_as_of": "2026-09-05"}  # 7 天前，遠低於 35 天門檻
    mode, reason = m.decide_mode("auto", fresh_cache, second_saturday, "monthly")
    assert mode == "price"
    assert "非本月第一個週六" in reason


def test_decide_mode_monthly_non_saturday_weekday_is_price_if_fresh():
    wednesday = datetime(2026, 9, 16)
    assert wednesday.weekday() == 2
    fresh_cache = {"eps_as_of": "2026-09-05"}
    mode, _ = m.decide_mode("auto", fresh_cache, wednesday, "monthly")
    assert mode == "price"


def test_decide_mode_monthly_stale_over_35_days_forces_full():
    day = datetime(2026, 9, 16)  # 非週六
    stale_cache = {"eps_as_of": "2026-08-01"}  # 46 天前，超過 35 天門檻
    mode, reason = m.decide_mode("auto", stale_cache, day, "monthly")
    assert mode == "full"
    assert "35 天門檻" in reason


def test_decide_mode_monthly_exactly_35_days_still_price():
    day = datetime(2026, 9, 16)  # 非週六
    cache = {"eps_as_of": "2026-08-12"}  # 恰好 35 天前
    mode, _ = m.decide_mode("auto", cache, day, "monthly")
    assert mode == "price"


def test_decide_mode_monthly_missing_cache_forces_full_even_off_saturday():
    wednesday = datetime(2026, 9, 16)
    mode, reason = m.decide_mode("auto", None, wednesday, "monthly")
    assert mode == "full"
    assert "沒有 EPS 快取" in reason


def test_decide_mode_default_full_refresh_is_weekly():
    # 沒傳 full_refresh 參數（其餘六檔的呼叫方式）維持舊版每週六行為，跟明示
    # full_refresh="weekly" 結果一致。
    first_saturday = datetime(2026, 9, 5)
    fresh_cache = {"eps_as_of": "2026-09-05"}
    assert m.decide_mode("auto", fresh_cache, first_saturday) == \
        m.decide_mode("auto", fresh_cache, first_saturday, "weekly")
    second_saturday = datetime(2026, 9, 12)
    assert m.decide_mode("auto", fresh_cache, second_saturday)[0] == "full"  # 每週六都 full，不是只有第一個


# ── EPS cache round-trip — load_eps_cache()/save_eps_cache() ────────────────

def test_eps_cache_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "EPS_CACHE_DIR", tmp_path)
    payload = {
        "eps_as_of": "2026-09-20",
        "holdings": [{"ticker": "AAA", "name": "Alpha", "weight_pct": 100.0}],
        "non_equity": [],
        "tickers": {"AAA": {"status": "ok", "eps_fy_next_local": 5.0,
                             "revisions_pct": {"30d": 1.0, "60d": 2.0, "90d": 3.0}}},
        "periods": [{"key": "30d", "eps_chg_pct": 1.0}],
        "contributions": {"30d": {"top": [], "bottom": []}},
    }
    m.save_eps_cache("FAKE", payload)
    loaded = m.load_eps_cache("FAKE")
    assert loaded == payload  # 逐層結構（含 nested revisions_pct）原封不動


def test_load_eps_cache_missing_file_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "EPS_CACHE_DIR", tmp_path)
    assert m.load_eps_cache("NOPE") is None


def test_load_eps_cache_corrupt_json_returns_none_not_raise(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "EPS_CACHE_DIR", tmp_path)
    (tmp_path / "BROKEN.json").write_text("{not valid json", encoding="utf-8")
    assert m.load_eps_cache("BROKEN") is None


# ── build_fund_price() — table window anchored at eps_as_of, not "today", ──
# and makes zero eps_trend calls (all EPS reused verbatim from eps_cache) ────

def _fake_eps_cache():
    return {
        "eps_as_of": "2026-09-20",
        "holdings_as_of": "2026-09-19",
        "holdings_source_url": "https://example.com/holdings.xlsx",
        "holdings": [
            {"ticker": "AAA", "name": "Alpha Corp", "weight_pct": 60.0},
            {"ticker": "BBB", "name": "Beta Corp", "weight_pct": 40.0},
        ],
        "non_equity": [],
        "tickers": {
            "AAA": {"status": "ok", "reason": None, "yf_ticker_used": "AAA", "eps_currency": "USD",
                    "eps_fy_next_local": 5.0, "price_currency": "USD", "has_stock_dash": False,
                    "revisions_pct": {"30d": 2.0, "60d": 3.0, "90d": 4.0}},
            "BBB": {"status": "ok", "reason": None, "yf_ticker_used": "BBB", "eps_currency": "USD",
                    "eps_fy_next_local": 2.0, "price_currency": "USD", "has_stock_dash": False,
                    "revisions_pct": {"30d": -1.0, "60d": -2.0, "90d": -3.0}},
        },
        # frozen table — anchored at eps_as_of (2026-09-20), NOT at "today" (2026-09-24)
        "periods": [
            {"key": "30d", "label": "近一個月", "days": 30, "base_date": "2026-08-21",
             "eps_chg_pct": 0.8, "price_chg_pct": 1.5, "implied_pe_chg_pct": 0.7,
             "coverage_pct": 100.0, "n_covered": 2, "n_total": 2,
             "period_exclusions": [], "period_capped": []},
        ],
        "contributions": {"30d": {"top": [], "bottom": []}},
    }


def _fake_cfg():
    return {
        "label_zh": "測試基金", "label_en": "Test Fund", "yf_ticker": "TESTETF",
        "isin": None, "other_listings": [], "holdings_issuer_zh": "測試官方持股下載",
    }


def test_build_fund_price_reuses_frozen_periods_and_makes_zero_eps_trend_calls(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "SNAP_DIR", tmp_path / "snapshots")
    eps_cache = _fake_eps_cache()
    fake_prices = {
        "TESTETF": [{"date": "2026-09-18", "close": 100.0}, {"date": "2026-09-20", "close": 102.0},
                    {"date": "2026-09-24", "close": 105.0}],
        "AAA": [{"date": "2026-09-24", "close": 50.0}],
        "BBB": [{"date": "2026-09-24", "close": 20.0}],
    }
    monkeypatch.setattr(m, "fetch_prices_batch", lambda tickers, **kw: fake_prices)

    calls_before = m.EPS_TREND_CALL_COUNT
    result = m.build_fund_price("TESTETF", _fake_cfg(), eps_cache, {}, {}, {},
                                 datetime(2026, 9, 24), "test forced price")

    # zero eps_trend calls — fetch_ticker_eps_and_price() (the only caller of
    # .eps_trend) is never on build_fund_price()'s call path.
    assert m.EPS_TREND_CALL_COUNT == calls_before

    assert result["mode"] == "price"
    assert result["eps_as_of"] == "2026-09-20"
    # the Exhibit 1 table is reused byte-for-byte from the FULL run, not
    # recomputed against "today" — this is what keeps the 近一個月/近二個月/
    # 近三個月 window anchored at eps_as_of all week.
    assert result["periods"] is eps_cache["periods"]
    assert result["contributions"] is eps_cache["contributions"]


def test_build_fund_price_computes_price_since_eps_as_of(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "SNAP_DIR", tmp_path / "snapshots")
    eps_cache = _fake_eps_cache()
    fake_prices = {
        "TESTETF": [{"date": "2026-09-20", "close": 102.0}, {"date": "2026-09-24", "close": 105.0}],
        "AAA": [{"date": "2026-09-24", "close": 50.0}],
        "BBB": [{"date": "2026-09-24", "close": 20.0}],
    }
    monkeypatch.setattr(m, "fetch_prices_batch", lambda tickers, **kw: fake_prices)
    result = m.build_fund_price("TESTETF", _fake_cfg(), eps_cache, {}, {}, {},
                                 datetime(2026, 9, 24), "test forced price")
    assert result["price_since_eps_as_of_pct"] == pytest.approx((105.0 / 102.0 - 1) * 100, abs=0.01)
    assert result["price"]["close"] == 105.0


def test_build_fund_price_weighted_fwd_pe_uses_todays_price_and_cached_eps(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "SNAP_DIR", tmp_path / "snapshots")
    eps_cache = _fake_eps_cache()
    # AAA: eps=5.0 price=50.0 -> yield 0.10 (weight 60%); BBB: eps=2.0 price=20.0 -> yield 0.10 (weight 40%)
    # both yields equal -> weighted harmonic mean P/E = 1/0.10 = 10.0
    fake_prices = {
        "TESTETF": [{"date": "2026-09-20", "close": 102.0}, {"date": "2026-09-24", "close": 105.0}],
        "AAA": [{"date": "2026-09-24", "close": 50.0}],
        "BBB": [{"date": "2026-09-24", "close": 20.0}],
    }
    monkeypatch.setattr(m, "fetch_prices_batch", lambda tickers, **kw: fake_prices)
    result = m.build_fund_price("TESTETF", _fake_cfg(), eps_cache, {}, {}, {},
                                 datetime(2026, 9, 24), "test forced price")
    assert result["weighted_forward_pe"]["value"] == pytest.approx(10.0, abs=0.01)
    assert result["weighted_forward_pe"]["coverage_pct"] == pytest.approx(100.0, abs=0.01)


def test_build_fund_price_ticker_missing_from_batch_gets_null_price(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "SNAP_DIR", tmp_path / "snapshots")
    eps_cache = _fake_eps_cache()
    fake_prices = {
        "TESTETF": [{"date": "2026-09-20", "close": 102.0}, {"date": "2026-09-24", "close": 105.0}],
        "AAA": [{"date": "2026-09-24", "close": 50.0}],
        # BBB deliberately missing — simulates a delisted/no-data ticker
    }
    monkeypatch.setattr(m, "fetch_prices_batch", lambda tickers, **kw: fake_prices)
    result = m.build_fund_price("TESTETF", _fake_cfg(), eps_cache, {}, {}, {},
                                 datetime(2026, 9, 24), "test forced price")
    bbb = next(c for c in result["constituents"] if c["ticker"] == "BBB")
    assert bbb["price_local"] is None
    assert bbb["price_usd"] is None
    # AAA still contributes to weighted_forward_pe alone
    aaa = next(c for c in result["constituents"] if c["ticker"] == "AAA")
    assert aaa["price_usd"] == 50.0


# ── convert_to_basis_currency() — 2026-09-25 加 TAIEX／0050：本益比／股價換算
#    的基準幣別不再寫死 USD（見 FUND_REGISTRY cfg["pe_basis_currency"]）。同
#    幣別（含 TWD==TWD）一定是 no-op，不查匯率——這條路徑是回歸測試的重點：
#    過去在別的頁面出現過「把 TWD 數字當 USD 用」的 bug，這裡確保同幣別時
#    connect_to_basis_currency 完全不碰 fx_cache／get_fx_rate。────────────────

def test_convert_to_basis_currency_same_currency_is_noop_no_fx_lookup(monkeypatch):
    def _boom(*a, **kw):
        raise AssertionError("get_fx_rate should not be called when local_ccy == basis_ccy")
    monkeypatch.setattr(m, "get_fx_rate", _boom)
    value, ok = m.convert_to_basis_currency(2475.0, "TWD", "TWD", "2026-09-24", {})
    assert value == 2475.0 and ok is True
    # also covers the existing USD==USD path unchanged
    value, ok = m.convert_to_basis_currency(50.0, "USD", "USD", "2026-09-24", {})
    assert value == 50.0 and ok is True


def test_convert_to_basis_currency_none_value_passthrough():
    assert m.convert_to_basis_currency(None, "TWD", "TWD", "2026-09-24", {}) == (None, True)


def test_convert_to_basis_currency_non_usd_basis_matches_usd_basis_logic():
    # basis_ccy="USD": local_ccy units per 1 USD (existing get_fx_rate() semantics)
    fx_cache = {"EUR": {"2026-09-24": {"rate": 0.92}}}
    value, ok = m.convert_to_basis_currency(92.0, "EUR", "USD", "2026-09-24", fx_cache)
    assert ok is True
    assert value == pytest.approx(100.0, abs=0.01)
    # basis_ccy="TWD", local_ccy="USD": basis_ccy units per 1 USD — multiply, not divide
    fx_cache2 = {"TWD": {"2026-09-24": {"rate": 31.0}}}
    value, ok = m.convert_to_basis_currency(10.0, "USD", "TWD", "2026-09-24", fx_cache2)
    assert ok is True
    assert value == pytest.approx(310.0, abs=0.01)


def test_convert_to_basis_currency_missing_rate_returns_not_ok(monkeypatch):
    monkeypatch.setattr(m, "get_fx_rate", lambda *a, **kw: None)
    value, ok = m.convert_to_basis_currency(100.0, "EUR", "USD", "2026-09-24", {})
    assert value is None and ok is False


def _fake_cfg_twd():
    return {
        "label_zh": "測試台股基金", "label_en": "Test TW Fund", "yf_ticker": "TESTTW",
        "isin": None, "other_listings": [], "holdings_issuer_zh": "測試 TWSE 機械估算",
        "source": "twse", "pe_basis_currency": "TWD",
    }


def test_build_fund_price_twd_basis_price_currency_and_no_us_fx_conversion(tmp_path, monkeypatch):
    """2026-09-25 加 TAIEX／0050 的回歸測試：pe_basis_currency="TWD" 的基金，
    成分股本身也是 TWD 報表時，price.currency 要標成 TWD（不是寫死 USD），
    且 eps_fy_next_usd／price_usd 兩個欄位（沿用既有欄位名稱，語意變成「本益
    比基準幣別下的值」）要等於原始 TWD 數字本身，不能被誤當 USD 再除一次
    匯率——這正是過去在別的頁面出現過的那種 bug。"""
    monkeypatch.setattr(m, "SNAP_DIR", tmp_path / "snapshots")

    def _boom(*a, **kw):
        raise AssertionError("get_fx_rate should not be called — constituents are already TWD, basis is TWD")
    monkeypatch.setattr(m, "get_fx_rate", _boom)

    eps_cache = {
        "eps_as_of": "2026-09-20", "holdings_as_of": "2026-09-19",
        "holdings_source_url": "https://openapi.twse.com.tw/",
        "holdings": [{"ticker": "2330.TW", "name": "台積電", "weight_pct": 100.0}],
        "non_equity": [],
        "tickers": {
            "2330.TW": {"status": "ok", "reason": None, "yf_ticker_used": "2330.TW", "eps_currency": "TWD",
                        "eps_fy_next_local": 142.96, "price_currency": "TWD", "has_stock_dash": False,
                        "revisions_pct": {"30d": 1.0, "60d": 2.0, "90d": 3.0}},
        },
        "periods": [{"key": "30d", "label": "近一個月", "days": 30, "base_date": "2026-08-21",
                     "eps_chg_pct": 1.0, "price_chg_pct": 1.0, "implied_pe_chg_pct": 0.0,
                     "coverage_pct": 100.0, "n_covered": 1, "n_total": 1,
                     "period_exclusions": [], "period_capped": []}],
        "contributions": {"30d": {"top": [], "bottom": []}},
    }
    fake_prices = {
        "TESTTW": [{"date": "2026-09-24", "close": 48024.6}],
        "2330.TW": [{"date": "2026-09-24", "close": 2475.0}],
    }
    monkeypatch.setattr(m, "fetch_prices_batch", lambda tickers, **kw: fake_prices)
    result = m.build_fund_price("TAIEX", _fake_cfg_twd(), eps_cache, {}, {}, {},
                                 datetime(2026, 9, 24), "test forced price")
    assert result["price"]["currency"] == "TWD"
    c = result["constituents"][0]
    assert c["eps_fy_next_usd"] == pytest.approx(142.96, abs=0.001)  # not divided by any FX rate
    assert c["price_usd"] == pytest.approx(2475.0, abs=0.001)
    assert "TWD" in result["weighted_forward_pe"]["method"]


# ── TWSE (TAIEX) universe — 2026-09-25: TAIEX 沒有官方持股清單可下載，改用
#    TWSE 公開資料（公司基本資料 t187ap03_L 的已發行普通股數 × STOCK_DAY_ALL
#    的收盤價）機械估算市值排序。用「公司代號」（4 位數字）比對兩份資料，
#    天然排除 ETF（如 "0050"／"00631L"，5-6 碼）、特別股（如 "2887B1"，非
#    純數字）、TDR（"9"開頭 6 碼）——這裡合成三種資料驗證這個排除行為。────

def _twse_fixture():
    companies = [
        {"公司代號": "2330", "公司簡稱": "台積電", "已發行普通股數或TDR原股發行股數": "25930380458"},
        {"公司代號": "2454", "公司簡稱": "聯發科", "已發行普通股數或TDR原股發行股數": "1595131238"},
        {"公司代號": "1101", "公司簡稱": "台泥", "已發行普通股數或TDR原股發行股數": "7523181742"},
    ]
    prices = [
        {"Date": "1150923", "Code": "2330", "ClosingPrice": "2475.0"},
        {"Date": "1150923", "Code": "2454", "ClosingPrice": "5285.0"},
        {"Date": "1150923", "Code": "1101", "ClosingPrice": "30.5"},
        # 不該出現在 holdings：ETF（5 碼，非公司清單裡的代號）、特別股
        # （非純數字）、TDR（9 開頭 6 碼）——都不在 comp_by_code，join 自然濾掉
        {"Date": "1150923", "Code": "0050", "ClosingPrice": "112.33"},
        {"Date": "1150923", "Code": "2887B1", "ClosingPrice": "50.0"},
        {"Date": "1150923", "Code": "910322", "ClosingPrice": "80.0"},
    ]
    return {"companies": companies, "prices": prices}


def test_parse_twse_taiex_universe_excludes_etf_preferred_tdr(monkeypatch):
    monkeypatch.setattr(m, "TAIEX_TOP_N", 150)
    as_of, holdings, non_equity = m.parse_twse_taiex_universe(_twse_fixture())
    assert as_of == "2026-09-23"  # ROC 1150923 -> 西元 2026-09-23
    assert non_equity == []
    tickers = [h["ticker"] for h in holdings]
    assert tickers == ["2330.TW", "2454.TW", "1101.TW"]  # 依市值排序，且 ETF/特別股/TDR 都不在裡面
    # TSMC 市值最大，佔比最高
    assert holdings[0]["ticker"] == "2330.TW"
    assert holdings[0]["weight_pct"] > holdings[1]["weight_pct"] > holdings[2]["weight_pct"]
    # weight_pct 是佔全市場（這個 fixture 裡的三檔）比例，加總應為 100%
    assert sum(h["weight_pct"] for h in holdings) == pytest.approx(100.0, abs=0.01)
    assert holdings[0]["cum_weight_pct"] < holdings[1]["cum_weight_pct"] < holdings[2]["cum_weight_pct"]
    assert holdings[-1]["cum_weight_pct"] == pytest.approx(100.0, abs=0.01)


def test_parse_twse_taiex_universe_respects_top_n(monkeypatch):
    monkeypatch.setattr(m, "TAIEX_TOP_N", 2)
    as_of, holdings, non_equity = m.parse_twse_taiex_universe(_twse_fixture())
    assert len(holdings) == 2
    assert [h["ticker"] for h in holdings] == ["2330.TW", "2454.TW"]
    # weight_pct 仍是佔全市場（含被截掉的台泥）比例，因此加總 < 100%
    assert sum(h["weight_pct"] for h in holdings) < 100.0


def test_parse_twse_taiex_universe_sets_last_universe_stats(monkeypatch):
    monkeypatch.setattr(m, "TAIEX_TOP_N", 150)
    m.parse_twse_taiex_universe(_twse_fixture())
    stats = m.LAST_TAIEX_UNIVERSE_STATS
    assert stats["n_total"] == 3
    assert stats["n_for_90pct"] is not None


def test_parse_twse_taiex_universe_missing_data_raises():
    with pytest.raises(RuntimeError, match="TAIEX universe"):
        m.parse_twse_taiex_universe({"companies": [], "prices": []})


def test_roc_date_to_iso():
    assert m._roc_date_to_iso("1150923") == "2026-09-23"
    assert m._roc_date_to_iso("") is None
    assert m._roc_date_to_iso(None) is None


def test_yyyymmdd_to_iso():
    assert m._yyyymmdd_to_iso("20260924") == "2026-09-24"
    assert m._yyyymmdd_to_iso("bad") is None
    assert m._yyyymmdd_to_iso(None) is None


# ── Yuanta (0050) SSR payload parsing — 2026-09-25: 持股資料內嵌在頁面 HTML
#    的 window.__NUXT__=(function(a,b,...){...})(v1,v2,...) 這段 IIFE 裡，
#    要拿到真正資料等同於要「執行」這段 JS（見 fetch_yuanta_holdings_page()
#    上方註解）。這裡用一段跟真實 Nuxt 序列化格式同構、但只含 2 檔股票 + 1
#    檔期貨的最小合成 payload，驗證 parse 邏輯本身，不對外發任何請求。跳過
#    （而非失敗）如果這台機器沒有 node——這條解析路徑本來就設計成「找不到
#    node 就整體抓取失敗、退回 holdings_cache」，測試環境沒有 node 不代表
#    程式邏輯錯了。──────────────────────────────────────────────────────────

def _yuanta_nuxt_fixture_html() -> str:
    # 真實 Nuxt payload 是「函式體用短變數名，呼叫時把實際值當參數傳回代入」
    # 的去重複字串格式；這裡刻意保留同樣的殼（IIFE + 参数替换），但只填最小
    # 需要的欄位（PCF.trandate 與 FundWeights 三類），驗證
    # parse_yuanta_0050_holdings() 找得到 window.__NUXT__、送進 node eval、
    # 且能正確取出 weightData 區塊。
    payload = (
        "window.__NUXT__=(function(a,b,c,d,e,f){"
        "return {data:[{fundData:{}},"
        "{weightData:{PCF:{trandate:a},"
        "FundWeights:{"
        "StockWeights:[{code:b,name:c,weights:d},{code:'2454',name:'聯發科',weights:7.2}],"
        "FutureWeights:[{code:e,name:f,weights:0.26}],"
        "ETFWeights:[],BondWeights:[]"
        "}}}]}"
        "})('20260924','2330','台積電',56,'TX','臺股期貨');"
    )
    return ("<html><head></head><body>"
            "<script>" + payload + "</script>"
            "<script>other script not touched</script>"
            "</body></html>")


def _node_missing() -> bool:
    return shutil.which("node") is None


@pytest.mark.skipif(_node_missing(), reason="node not available in this environment")
def test_parse_yuanta_0050_holdings_basic():
    as_of, holdings, non_equity = m.parse_yuanta_0050_holdings(_yuanta_nuxt_fixture_html())
    assert as_of == "2026-09-24"
    assert [h["ticker"] for h in holdings] == ["2330.TW", "2454.TW"]
    assert holdings[0]["weight_pct"] == pytest.approx(56.0)
    assert len(non_equity) == 1
    assert non_equity[0]["ticker"] == "TX"
    assert non_equity[0]["reason"].startswith("期貨")


def test_parse_yuanta_0050_holdings_missing_nuxt_payload_raises():
    with pytest.raises(RuntimeError, match="__NUXT__"):
        m.parse_yuanta_0050_holdings("<html><body>no payload here</body></html>")


def test_parse_yuanta_0050_holdings_node_missing_raises(monkeypatch):
    monkeypatch.setattr(m.shutil, "which", lambda name: None)
    with pytest.raises(RuntimeError, match="node executable not found"):
        m.parse_yuanta_0050_holdings(_yuanta_nuxt_fixture_html())


# ── iShares Japan (TOPIX, 1475.T) holdings CSV — 2026-09-25: BlackRock Japan's
#    .ajax endpoint returns plain CSV (utf-8 BOM), first line "基準日,\"YYYY年
#    M月D日\"", second line a lone \xa0, real header on the third line. Asset
#    Class is "株式" for equity and anything else (cash/futures/collateral) is
#    excluded — mirrors the real 2026-09-25 response shape (see scratchpad
#    curl test), not a black-list of known non-equity labels. ─────────────────

def _ishares_jp_csv_bytes(as_of_zh: str, extra_rows: list[list[str]]) -> bytes:
    header = ["Ticker", "Name", "Sector", "Asset Class", "Market Value", "Weight (%)",
              "Notional Value", "Shares", "Price", "Location", "Exchange", "Currency", "FX Rate",
              "Market Currency"]
    lines = [f'基準日,"{as_of_zh}"', "\xa0", ",".join(header)]
    for row in extra_rows:
        lines.append(",".join(f'"{c}"' if isinstance(c, str) and "," not in c else str(c) for c in row))
    text = "\n".join(lines) + "\n"
    return text.encode("utf-8-sig")


def _ishares_jp_fixture_bytes() -> bytes:
    return _ishares_jp_csv_bytes("2026年9月23日", [
        ["8306", "三菱UFJﾌｨﾅﾝｼｬﾙG", "銀行業", "株式", "116649432000.00", "3.93",
         "116649432000.00", "32223600.00", "3620.00", "日本", "東京証券取引所", "JPY", "1.00", "JPY"],
        ["285A", "SOME NEW LISTING", "サービス業", "株式", "5640000.00", "0.01",
         "5640000.00", "18800.00", "300.00", "日本", "東京証券取引所", "JPY", "1.00", "JPY"],
        ["JPY", "JPY CASH", "その他", "キャッシュ", "6910209525.00", "0.23",
         "6910209525.00", "6910209525.00", "100.00", "日本", "-", "JPY", "1.00", "JPY"],
        ["MARGIN_JPY", "FUTURES JPY MARGIN BALANCE", "その他", "Cash Collateral and Margins",
         "3677468.00", "0.00", "3677468.00", "3677468.00", "100.00", "日本", "-", "JPY", "1.00", "JPY"],
        ["TPZ6", "TOPIX INDEX DEC 26", "その他", "Futures", "0.00", "0.00",
         "7267740000.00", "178.00", "4083.00", "-", "Osaka Securities Exchange", "JPY", "1.00", "JPY"],
    ])


def test_parse_ishares_jp_holdings_csv_basic():
    as_of, rows, non_equity = m.parse_ishares_jp_holdings_csv(_ishares_jp_fixture_bytes())
    assert as_of == "2026-09-23"
    assert [r["ticker"] for r in rows] == ["8306.T", "285A.T"]  # 4-digit and post-2024 alphanumeric codes both -> {code}.T
    assert rows[0]["weight_pct"] == pytest.approx(3.93)
    assert rows[0]["raw_ticker_field"] == "8306"
    assert len(non_equity) == 3
    reasons = {e["ticker"]: e["reason"] for e in non_equity}
    assert "キャッシュ" in reasons["JPY"]
    assert "Cash Collateral and Margins" in reasons["MARGIN_JPY"]
    assert "Futures" in reasons["TPZ6"]


def test_parse_ishares_jp_holdings_csv_tolerates_blank_nbsp_line():
    # 真實檔案第 2 列是單獨一個 \xa0（見 _ishares_jp_csv_bytes 固定寫死那一
    # 行）——確認 csv.reader 對這種短列不會撞 IndexError，而是被當空白列跳過。
    as_of, rows, non_equity = m.parse_ishares_jp_holdings_csv(_ishares_jp_fixture_bytes())
    assert as_of is not None
    assert len(rows) == 2


def test_parse_ishares_jp_holdings_csv_missing_header_raises():
    bad = 'not,a,holdings,csv\n"no ticker column here"\n'.encode("utf-8-sig")
    with pytest.raises(RuntimeError, match="as-of date or header row"):
        m.parse_ishares_jp_holdings_csv(bad)


def test_parse_ishares_jp_holdings_csv_no_equity_rows_raises():
    raw = _ishares_jp_csv_bytes("2026年9月23日", [
        ["JPY", "JPY CASH", "その他", "キャッシュ", "100.00", "0.23", "100.00", "100.00", "100.00",
         "日本", "-", "JPY", "1.00", "JPY"],
    ])
    with pytest.raises(RuntimeError, match="parsed 0 equity holdings"):
        m.parse_ishares_jp_holdings_csv(raw)


# ── EPS scope cutoff (TOPIX ~1,700 holdings — only fetch eps_trend for the
#    largest names reaching the configured cumulative weight) ───────────────

def test_select_eps_scope_tickers_stops_once_cutoff_reached():
    holdings = [
        {"ticker": "A", "weight_pct": 50.0},
        {"ticker": "B", "weight_pct": 30.0},
        {"ticker": "C", "weight_pct": 15.0},
        {"ticker": "D", "weight_pct": 5.0},
    ]
    assert m.select_eps_scope_tickers(holdings, 80.0) == {"A", "B"}
    assert m.select_eps_scope_tickers(holdings, 95.0) == {"A", "B", "C"}
    assert m.select_eps_scope_tickers(holdings, 100.0) == {"A", "B", "C", "D"}


def test_select_eps_scope_tickers_aggregates_duplicate_tickers():
    holdings = [{"ticker": "A", "weight_pct": 40.0}, {"ticker": "A", "weight_pct": 40.0},
                {"ticker": "B", "weight_pct": 20.0}]
    assert m.select_eps_scope_tickers(holdings, 70.0) == {"A"}


def test_build_eps_scope_note_zh_none_when_cutoff_not_configured():
    assert m.build_eps_scope_note_zh({"label_zh": "x"}, [], None) is None


def test_build_eps_scope_note_zh_reports_n_and_weight():
    cfg = {"label_zh": "TOPIX（1475）", "eps_scope_cutoff_pct": 90.0}
    holdings = [{"ticker": "A", "weight_pct": 60.0}, {"ticker": "B", "weight_pct": 30.0},
                {"ticker": "C", "weight_pct": 10.0}]
    scoped = {"A", "B"}
    note = m.build_eps_scope_note_zh(cfg, holdings, scoped)
    assert "3 檔" in note
    assert "90%" in note
    assert "前 2 檔" in note
    assert "90.00%" in note  # 實際累計權重 A+B=90.00


# ── Long EPS-index line suppression when dd-screener coverage is too low
#    (2026-09-25, TOPIX: dd-screener universe is overwhelmingly US names, so
#    Japan coverage is expected to be near-zero — don't draw a near-empty
#    line, show a note instead) ───────────────────────────────────────────

def test_build_long_chart_series_no_data_returns_empty_no_note():
    long_eps = {"series": [], "coverage_weight_pct": 0.0, "start_date": None}
    series, note = m.build_long_chart_series(long_eps, [{"date": "2026-09-20", "close": 100.0}])
    assert series == []
    assert note is None


def test_build_long_chart_series_below_threshold_suppressed_with_note():
    long_eps = {
        "series": [{"date": "2026-09-01", "eps_index": 100.0, "coverage_pct": 5.0},
                   {"date": "2026-09-20", "eps_index": 101.0, "coverage_pct": 5.0}],
        "coverage_weight_pct": 5.0,
        "start_date": "2026-09-01",
    }
    price_series = [{"date": "2026-09-01", "close": 100.0}, {"date": "2026-09-20", "close": 105.0}]
    series, note = m.build_long_chart_series(long_eps, price_series)
    assert series == []
    assert note is not None
    assert "5.0%" in note


def test_build_long_chart_series_at_or_above_threshold_is_drawn():
    long_eps = {
        "series": [{"date": "2026-09-01", "eps_index": 100.0, "coverage_pct": 40.0},
                   {"date": "2026-09-20", "eps_index": 101.0, "coverage_pct": 40.0}],
        "coverage_weight_pct": 40.0,
        "start_date": "2026-09-01",
    }
    price_series = [{"date": "2026-09-01", "close": 100.0}, {"date": "2026-09-20", "close": 105.0}]
    series, note = m.build_long_chart_series(long_eps, price_series)
    assert note is None
    assert len(series) == 2
    assert series[0]["price_index"] == pytest.approx(100.0)
    assert series[1]["price_index"] == pytest.approx(105.0)
