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


# ── yfinance rate-limit detector ─────────────────────────────────────────────

class _FakeYFRateLimitError(Exception):
    pass


def test_is_rate_limited_matches_by_class_name():
    assert m._is_rate_limited(_FakeYFRateLimitError("slow down")) is True


def test_is_rate_limited_matches_429_message():
    assert m._is_rate_limited(RuntimeError("HTTP 429 Too Many Requests")) is True


def test_is_rate_limited_false_for_unrelated_error():
    assert m._is_rate_limited(ValueError("bad ticker")) is False


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
