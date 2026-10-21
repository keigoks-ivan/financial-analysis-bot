"""2026-10-21 每日 Koyfin 抓取：閘門逐檔處理、每日快照基準挑選、財報後第 k 天對位。

全部用手造資料，不碰網路、不碰真的 docs/ 與 data/（路徑都 monkeypatch 到 tmp_path）。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import eps_daily as ed  # noqa: E402
import market_sessions as ms  # noqa: E402
import koyfin_refresh_all as kra  # noqa: E402
from load_eps_estimates_xlsx import ExcelSnapshot  # noqa: E402


def utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# 交易日
# ---------------------------------------------------------------------------

def test_us_calendar_holidays_2026():
    assert not ms.is_us_session("2026-04-03")      # Good Friday
    assert not ms.is_us_session("2026-07-03")      # 7/4 落週六，週五休
    assert not ms.is_us_session("2026-11-26")      # Thanksgiving
    assert ms.is_us_session("2026-10-12")          # Columbus Day 股市照開
    assert ms.next_session("US", "2026-11-25") == date(2026, 11, 27)
    assert ms.next_session("US", "2026-10-16") == date(2026, 10, 19)   # 週五 -> 週一


def test_latest_closed_session_uses_exchange_close():
    # 台北 10/21 08:15 = 美東 10/20 20:15：10/20 已收盤
    assert ms.latest_closed_session("US", utc("2026-10-21T00:15:00Z")) == date(2026, 10, 20)
    # 美東 10/20 15:00 還沒收：最近收盤是 10/19
    assert ms.latest_closed_session("US", utc("2026-10-20T19:00:00Z")) == date(2026, 10, 19)
    # 台北週六早上：最近收盤的台股交易日是週五
    assert ms.latest_closed_session("TW", utc("2026-10-17T00:15:00Z")) == date(2026, 10, 16)


# ---------------------------------------------------------------------------
# 閘門 a：微小 EPS
# ---------------------------------------------------------------------------

def _snap(tickers: dict) -> ExcelSnapshot:
    return ExcelSnapshot(snapshot_date="2026-10-19", source_file="fake.xlsx", tickers=tickers)


def test_gate_a_tiny_eps_not_flagged_but_listed():
    prev = _snap({"MP": {"fy1": 0.02}, "SPCX": {"fy1": -0.09}, "BIG": {"fy1": 2.0}})
    gate = kra.run_anomaly_gate({"MP": 0.01, "SPCX": -0.01, "BIG": 0.5}, prev)
    assert [r["ticker"] for r in gate["flagged"]] == ["BIG"]
    assert [r["ticker"] for r in gate["tiny_eps_skipped"]] == ["MP", "SPCX"]


def test_gate_a_only_when_both_sides_are_tiny():
    # 0.02 -> 0.30：新值不小，照常標出
    gate = kra.run_anomaly_gate({"MP": 0.30}, _snap({"MP": {"fy1": 0.02}}))
    assert [r["ticker"] for r in gate["flagged"]] == ["MP"]
    # 負轉正但兩邊都小：不標
    gate = kra.run_anomaly_gate({"X": 0.05}, _snap({"X": {"fy1": -0.05}}))
    assert gate["flagged"] == [] and len(gate["tiny_eps_skipped"]) == 1


# ---------------------------------------------------------------------------
# 閘門 b、c：resolve_flagged
# ---------------------------------------------------------------------------

def _flag(t, prev, new):
    return {"ticker": t, "prev_fy1": prev, "new_fy1": new,
            "pct_move": abs(new - prev) / abs(prev) * 100, "sign_flip": prev * new < 0}


def _resolve(flagged, today, state=None, reports=None, family="screener", ref=None):
    reports = reports or {}
    return ed.resolve_flagged(
        flagged, family_key=family, today=today, state_before=state or {},
        report_dates_for=lambda t: reports.get(t, []),
        ref_session=ref or ms.latest_closed_session("TW" if family == "tw" else "US", utc(f"{today}T00:15:00Z")))


def test_gate_b_report_within_three_trading_days_is_accepted():
    # 週三 10/21 早上抓取，最近收盤 10/20。最近 3 個交易日是 10/16、10/19、10/20
    for rep in ("2026-10-20", "2026-10-19", "2026-10-16"):
        res = _resolve([_flag("A", 5.0, 1.0)], "2026-10-21", reports={"A": [date.fromisoformat(rep)]})
        assert len(res["accepted_after_earnings"]) == 1, rep
        assert res["held"] == []
        assert res["accepted_after_earnings"][0]["report_date"] == rep
    # 10/15 是第 4 個交易日：不算
    res = _resolve([_flag("A", 5.0, 1.0)], "2026-10-21", reports={"A": [date(2026, 10, 15)]})
    assert res["accepted_after_earnings"] == [] and len(res["held"]) == 1


def test_gate_b_tw_family_counts_taiwan_sessions():
    # 台北週一 10/19 08:15：最近收盤的台股交易日是週五 10/16，最近 3 個交易日是 10/14、10/15、10/16
    res = _resolve([_flag("2330", 5.0, 1.0)], "2026-10-19", family="tw", reports={"2330": [date(2026, 10, 14)]})
    assert len(res["accepted_after_earnings"]) == 1
    res = _resolve([_flag("2330", 5.0, 1.0)], "2026-10-19", family="tw", reports={"2330": [date(2026, 10, 13)]})
    assert len(res["held"]) == 1


def test_gate_b_future_or_unknown_report_dates_do_not_accept():
    res = _resolve([_flag("A", 5.0, 1.0)], "2026-10-21", reports={"A": [date(2026, 10, 22)]})
    assert len(res["held"]) == 1
    res = _resolve([_flag("A", 5.0, 1.0)], "2026-10-21")
    assert len(res["held"]) == 1


def test_gate_c_held_then_released_on_second_consecutive_scrape():
    day1 = _resolve([_flag("A", 5.0, 1.00)], "2026-10-20")
    assert [r["ticker"] for r in day1["held"]] == ["A"]
    state = day1["state_after"]
    assert state["A"]["history"][-1] == {"date": "2026-10-20", "new_fy1": 1.0}

    # 第二天同一個新值（差 0.5%）：放行
    day2 = _resolve([_flag("A", 5.0, 1.005)], "2026-10-21", state=state)
    assert day2["held"] == []
    assert [r["ticker"] for r in day2["released_after_2_days"]] == ["A"]
    assert day2["state_after"] == {}


def test_gate_c_not_released_when_second_value_differs_or_gap_too_long():
    state = _resolve([_flag("A", 5.0, 1.00)], "2026-10-20")["state_after"]
    # 差 5%：繼續扣，歷史保留前一次與今天
    day2 = _resolve([_flag("A", 5.0, 1.05)], "2026-10-21", state=state)
    assert len(day2["held"]) == 1
    assert [h["new_fy1"] for h in day2["state_after"]["A"]["history"]] == [1.0, 1.05]
    # 第三天回到 1.05（與第二天相同）：放行
    day3 = _resolve([_flag("A", 5.0, 1.052)], "2026-10-22", state=day2["state_after"])
    assert len(day3["released_after_2_days"]) == 1
    # 前一次距今 6 天以上：不算連續
    old = {"A": {"history": [{"date": "2026-10-10", "new_fy1": 1.0}]}}
    assert len(_resolve([_flag("A", 5.0, 1.0)], "2026-10-21", state=old)["held"]) == 1


def test_gate_c_same_day_state_entries_are_ignored():
    # 同一天的舊紀錄（重跑）不能自己放行自己
    state = {"A": {"history": [{"date": "2026-10-21", "new_fy1": 1.0}]}}
    res = _resolve([_flag("A", 5.0, 1.0)], "2026-10-21", state=state)
    assert len(res["held"]) == 1 and res["released_after_2_days"] == []


def test_gate_d_limit():
    assert ed.held_limit(86) == 10
    assert ed.held_limit(292) == pytest.approx(14.6)
    assert ed.held_limit(1000) == 50


def test_held_columns_are_the_six_estimate_columns():
    names = [n for _, _, n in ed.HELD_COLUMNS]
    assert names == ["FY1E EPS", "FY2E EPS", "FY3E EPS", "PE NTM x", "Est Rev CAGR 3Y %", "Est EPS CAGR 3Y %"]
    # 原始 txt 欄位位置對應 koyfin_xlsx_from_raw.build_row：f[1..3]=FY1..3 EPS，f[37]=PE NTM，
    # f[48]=Est Rev CAGR 3Y，f[49]=Est EPS CAGR 3Y
    assert [i for i, _, _ in ed.HELD_COLUMNS] == [1, 2, 3, 37, 48, 49]


def _raw_line(t, fy1, fy2=6.0, fy3=7.0, pe=20.0, price="100"):
    f = ["-"] * 54
    f[0], f[1], f[2], f[3] = t, str(fy1), str(fy2), str(fy3)
    f[37], f[48], f[49], f[51] = str(pe), "10", "11", price
    return "|".join(f)


def test_apply_held_to_raw_lines_replaces_only_estimate_columns():
    prev = _snap({"AAA": {"fy1": 5.0, "fy2": 6.5, "fy3": None, "pe_ntm_x": 18.5,
                          "est_rev_cagr_3y_pct": 9.0, "est_eps_cagr_3y_pct": 12.0}})
    lines = [_raw_line("AAA", 1.0, price="55"), _raw_line("BBB", 2.0)]
    out = ed.apply_held_to_raw_lines(lines, {"AAA"}, prev)
    a = out[0].split("|")
    assert [a[1], a[2], a[3], a[37], a[48], a[49]] == ["5.000000", "6.500000", "-", "18.500000", "9.000000", "12.000000"]
    assert a[51] == "55"           # 價格等其他欄位用新值
    assert out[1] == lines[1]      # 其他股票原樣


# ---------------------------------------------------------------------------
# process_family 串起來（假的 xlsx 與財報日查詢）
# ---------------------------------------------------------------------------

@pytest.fixture
def env(tmp_path, monkeypatch):
    data = tmp_path / "data" / "eps-estimates"
    (data / "raw").mkdir(parents=True)
    monkeypatch.setattr(kra, "DATA_DIR", data)
    monkeypatch.setattr(ed, "GATE_DIR", data / "gate")
    monkeypatch.setattr(ed, "HELD_STATE_PATH", data / "gate" / "held_state.json")
    prev = _snap({"AAA": {"fy1": 5.0, "fy2": 6.0, "fy3": 7.0, "pe_ntm_x": 20.0,
                          "est_rev_cagr_3y_pct": 10.0, "est_eps_cagr_3y_pct": 11.0},
                  "CCC": {"fy1": 3.0}})
    monkeypatch.setattr(kra, "find_previous_snapshot", lambda *a, **k: data / "DD_universe_EPS_estimates_prev.xlsx")
    monkeypatch.setattr(kra.leex, "load_excel", lambda p: prev)
    built = {}

    def fake_build(family_key, raw_path, out_path, snapshot_date):
        built[snapshot_date] = Path(raw_path).read_text(encoding="utf-8")
        return 0, len(built[snapshot_date].splitlines())
    monkeypatch.setattr(kra, "build_xlsx", fake_build)
    monkeypatch.setattr(kra, "make_report_lookup", lambda fam, as_of: (lambda t: []))

    def put_raw(date_str, lines):
        p = data / "raw" / f"koyfin_screener_raw_{date_str}.txt"
        p.write_text("\n".join(lines), encoding="utf-8")
        ts = datetime.strptime(date_str, "%Y%m%d").replace(hour=0, minute=15, tzinfo=timezone.utc).timestamp()
        os.utime(p, (ts, ts))
        return p
    return {"data": data, "put_raw": put_raw, "built": built, "monkeypatch": monkeypatch}


def test_process_family_hold_then_release_and_idempotent(env):
    put_raw, built = env["put_raw"], env["built"]
    others = [_raw_line("CCC", 3.1)]

    put_raw("20261020", [_raw_line("AAA", 1.0, pe=99.0, price="55")] + others)
    rc, info = kra.process_family("screener", "20261020", False, None)
    assert rc == 0
    rep = info["gate_report"]
    assert [r["ticker"] for r in rep["held"]] == ["AAA"]
    eff = built["2026-10-20"].splitlines()[0].split("|")
    assert eff[1] == "5.000000" and eff[37] == "20.000000" and eff[51] == "55"

    # 同一天重跑：結果相同（冪等）
    rc, info2 = kra.process_family("screener", "20261020", False, None)
    assert [r["ticker"] for r in info2["gate_report"]["held"]] == ["AAA"]

    # 隔天同一個新值：放行，用新值建 xlsx
    put_raw("20261021", [_raw_line("AAA", 1.004, pe=98.0)] + others)
    rc, info3 = kra.process_family("screener", "20261021", False, None)
    rep3 = info3["gate_report"]
    assert rep3["held"] == [] and [r["ticker"] for r in rep3["released_after_2_days"]] == ["AAA"]
    assert built["2026-10-21"].splitlines()[0].split("|")[1] == "1.004"

    # 放行那天重跑：還是放行
    rc, info4 = kra.process_family("screener", "20261021", False, None)
    assert [r["ticker"] for r in info4["gate_report"]["released_after_2_days"]] == ["AAA"]

    # 報告檔與狀態檔都寫了
    gate_dir = env["data"] / "gate"
    doc = json.loads((gate_dir / "gate_report_20261021.json").read_text(encoding="utf-8"))
    assert doc["families"]["screener"]["released_after_2_days"][0]["ticker"] == "AAA"
    assert (gate_dir / "gate_report_latest.json").exists()
    state = json.loads((gate_dir / "held_state.json").read_text(encoding="utf-8"))
    assert state["screener"]["as_of"] == "2026-10-21" and state["screener"]["after"] == {}


def test_process_family_accepts_after_earnings(env):
    env["monkeypatch"].setattr(kra, "make_report_lookup",
                               lambda fam, as_of: (lambda t: [date(2026, 10, 20)] if t == "AAA" else []))
    env["put_raw"]("20261021", [_raw_line("AAA", 1.0), _raw_line("CCC", 3.0)])
    rc, info = kra.process_family("screener", "20261021", False, None)
    rep = info["gate_report"]
    assert rc == 0 and rep["held"] == []
    assert rep["accepted_after_earnings"][0]["ticker"] == "AAA"
    assert rep["accepted_after_earnings"][0]["report_date"] == "2026-10-20"
    assert env["built"]["2026-10-21"].splitlines()[0].split("|")[1] == "1.0"   # 新值


def test_process_family_too_many_held_exits_6(env):
    prev = _snap({f"T{i}": {"fy1": 5.0} for i in range(12)})
    env["monkeypatch"].setattr(kra.leex, "load_excel", lambda p: prev)
    env["put_raw"]("20261021", [_raw_line(f"T{i}", 1.0) for i in range(12)])
    rc, info = kra.process_family("screener", "20261021", False, None)
    assert rc == 6
    doc = json.loads((env["data"] / "gate" / "gate_report_20261021.json").read_text(encoding="utf-8"))
    assert doc["families"]["screener"]["status"] == "blocked_too_many_held"
    assert env["built"] == {}      # nothing built


# ---------------------------------------------------------------------------
# 基準挑選
# ---------------------------------------------------------------------------

def _daily(snapshot_date, scraped, **tickers):
    return {"kind": "daily", "snapshot_date": snapshot_date, "scraped_at_utc": scraped, "tickers": tickers}


def test_baseline_cutoff_10_utc_boundary_us():
    snaps = {
        "a": _daily("2026-10-19", "2026-10-19T00:15:00+00:00"),
        "b": _daily("2026-10-20", "2026-10-20T09:59:59+00:00"),
        "c": _daily("2026-10-20", "2026-10-20T10:00:00+00:00"),     # 剛好 10:00：不算「早於」
    }
    assert ed.pick_daily_baseline(snaps, "2026-10-20", "US") is snaps["b"]
    del snaps["b"]
    assert ed.pick_daily_baseline(snaps, "2026-10-20", "US") is snaps["a"]


def test_baseline_tw_cutoff_is_1330_taipei():
    snaps = {
        "a": _daily("2026-10-16", "2026-10-16T00:15:00+00:00"),
        "b": _daily("2026-10-16", "2026-10-16T05:29:00+00:00"),
        "c": _daily("2026-10-16", "2026-10-16T05:30:00+00:00"),
    }
    assert ed.pick_daily_baseline(snaps, "2026-10-16", "TW") is snaps["b"]
    # 同樣三份對美股（10:00 UTC）則是 c 以外最晚的 c? 05:30 < 10:00 -> c 合格
    assert ed.pick_daily_baseline(snaps, "2026-10-16", "US") is snaps["c"]


def test_baseline_must_be_within_10_days_else_none():
    snaps = {"a": _daily("2026-10-09", "2026-10-09T00:15:00+00:00")}
    assert ed.pick_daily_baseline(snaps, "2026-10-19", "US") is snaps["a"]      # 剛好 10 天
    assert ed.pick_daily_baseline(snaps, "2026-10-20", "US") is None            # 11 天
    assert ed.pick_daily_baseline({}, "2026-10-20", "US") is None
    assert ed.pick_daily_baseline(snaps, None, "US") is None


def _bds():
    import build_dd_screener as bds
    return bds


def test_since_earnings_uses_daily_baseline_and_flags_kind():
    bds = _bds()
    daily = {"2026-10-20": _daily("2026-10-20", "2026-10-20T00:15:00+00:00",
                                  FAKE={"eps_fy_curr": 10.0, "eps_fy_next": 12.0, "eps_fy3": 15.0, "source": "xlsx"})}
    monthly = {"2026-09": {"snapshot_date": "2026-09-26",
                           "tickers": {"FAKE": {"eps_fy_curr": 8.0, "eps_fy_next": 9.0, "eps_fy3": 10.0}}}}
    out = bds._compute_eps_rev_since_earnings(
        "FAKE", "FAKE", 11.0, 13.2, 16.5, last_earnings_date="2026-10-20", current_snapshot_date="2026-10-22",
        reporting_ccy_cache={"FAKE": {"currency": "USD", "checked": "2026-01-01"}}, fx_cache={},
        eps_rev_3m_result={"eps_rev_3m_pct": -99.0, "eps_rev_3m_baseline_date": "2026-07-01"},
        monthly_snapshots=monthly, daily_snapshots=daily, market="US")
    assert out["eps_rev_anchor"] == "earnings"
    assert out["eps_rev_since_earnings_baseline_date"] == "2026-10-20"
    assert out["eps_rev_since_earnings_baseline"] == {"date": "2026-10-20", "kind": "daily"}
    assert out["eps_rev_since_earnings_baseline_kind"] == "daily"
    assert out["eps_rev_since_earnings_pct"] == pytest.approx(10.0)    # 三個財年都 +10%


def test_since_earnings_falls_back_to_monthly_without_daily_history():
    bds = _bds()
    monthly = {"2026-09": {"snapshot_date": "2026-09-26",
                           "tickers": {"FAKE": {"eps_fy_curr": 10.0, "eps_fy_next": 12.0, "eps_fy3": 15.0}}}}
    kw = dict(last_earnings_date="2026-10-20", current_snapshot_date="2026-10-22",
              reporting_ccy_cache={"FAKE": {"currency": "USD", "checked": "2026-01-01"}}, fx_cache={},
              eps_rev_3m_result={"eps_rev_3m_pct": -99.0, "eps_rev_3m_baseline_date": "2026-07-01"},
              monthly_snapshots=monthly, market="US")
    none_daily = bds._compute_eps_rev_since_earnings("FAKE", "FAKE", 11.0, 13.2, 16.5, daily_snapshots={}, **kw)
    assert none_daily["eps_rev_since_earnings_baseline"] == {"date": "2026-09-26", "kind": "monthly"}
    # 每日快照太舊（離財報日超過 10 天）也退回月快照
    stale = {"2026-10-05": _daily("2026-10-05", "2026-10-05T00:15:00+00:00", FAKE={"eps_fy_curr": 1.0})}
    out = bds._compute_eps_rev_since_earnings("FAKE", "FAKE", 11.0, 13.2, 16.5, daily_snapshots=stale, **kw)
    assert out["eps_rev_since_earnings_baseline"]["kind"] == "monthly"
    # 沒有財報日：calendar_3m，kind 仍標 monthly
    kw2 = dict(kw, last_earnings_date=None)
    out = bds._compute_eps_rev_since_earnings("FAKE", "FAKE", 11.0, 13.2, 16.5, daily_snapshots=stale, **kw2)
    assert out["eps_rev_anchor"] == "calendar_3m" and out["eps_rev_since_earnings_baseline_kind"] == "monthly"


def test_since_earnings_daily_baseline_handles_fiscal_year_rollover():
    bds = _bds()
    # 年報（財年 9/30 結束）11/05 發布：基準（11/05 凌晨）還沒滾動，現在（11/06）已滾動
    daily = {"2026-11-05": _daily("2026-11-05", "2026-11-05T00:15:00+00:00",
                                  FAKE={"eps_fy_curr": 10.0, "eps_fy_next": 12.0, "eps_fy3": 14.0, "source": "xlsx"})}
    out = bds._compute_eps_rev_since_earnings(
        "FAKE", "FAKE", 12.6, 14.7, 17.0, last_earnings_date="2026-11-05", current_snapshot_date="2026-11-06",
        reporting_ccy_cache={"FAKE": {"currency": "USD", "checked": "2026-01-01"}}, fx_cache={},
        eps_rev_3m_result={"eps_rev_3m_pct": None, "eps_rev_3m_baseline_date": None},
        monthly_snapshots={}, daily_snapshots=daily, market="US",
        last_fye="2026-09-30", past_earnings_dates=["2026-08-05", "2026-11-05"])
    assert out["eps_rev_since_earnings_fy_shift"] == 1
    # 新 FY1 12.6 對舊 FY2 12.0 = +5%，新 FY2 14.7 對舊 FY3 14.0 = +5%，FY3 無基準
    assert out["eps_rev_since_earnings_pct"] == pytest.approx(5.0)
    assert out["_eps_rev_since_earnings_fy"][2] is None


# ---------------------------------------------------------------------------
# 財報後第 k 天
# ---------------------------------------------------------------------------

S_BEFORE_ET = "2026-10-20T00:15:00+00:00"   # 台北 10/20 08:15


def _chain(*pairs):
    """[(snapshot_date, scraped_utc)] -> {date: snapshot}"""
    return {d: _daily(d, s, X={"eps_fy_curr": 1.0}) for d, s in pairs}


def test_day_k_bmo_reports_before_open():
    snaps = _chain(("2026-10-20", "2026-10-20T00:15:00+00:00"),    # 財報日台北早上：財報前
                   ("2026-10-21", "2026-10-21T00:15:00+00:00"),    # 美東 10/20 20:15：10/20 收盤後
                   ("2026-10-22", "2026-10-22T00:15:00+00:00"))
    got = ed.post_earnings_snapshots(snaps, "US", "2026-10-20", "BMO")
    assert got["reaction_day"] == date(2026, 10, 20)
    assert got["before"]["snapshot_date"] == "2026-10-20"
    assert got["day1"]["snapshot_date"] == "2026-10-21"
    assert got["day2"]["snapshot_date"] == "2026-10-22"


def test_day_k_amc_reaction_is_next_session():
    snaps = _chain(("2026-10-20", "2026-10-20T00:15:00+00:00"),
                   ("2026-10-21", "2026-10-21T00:15:00+00:00"),    # 10/20 盤後剛發布，這份是財報當天收盤後
                   ("2026-10-22", "2026-10-22T00:15:00+00:00"),
                   ("2026-10-23", "2026-10-23T00:15:00+00:00"))
    got = ed.post_earnings_snapshots(snaps, "US", "2026-10-20", "AMC")
    assert got["reaction_day"] == date(2026, 10, 21)
    assert got["day1"]["snapshot_date"] == "2026-10-22"     # R=10/21 收盤之後
    assert got["day2"]["snapshot_date"] == "2026-10-23"


def test_day_k_friday_amc_crosses_weekend():
    snaps = _chain(("2026-10-16", "2026-10-16T00:15:00+00:00"),    # 週五早上（財報前）
                   ("2026-10-17", "2026-10-17T00:15:00+00:00"),    # 週六早上：含週五收盤，仍不算第 1 天
                   ("2026-10-20", "2026-10-20T00:15:00+00:00"),    # 週二早上：含週一收盤 -> 第 1 天
                   ("2026-10-21", "2026-10-21T00:15:00+00:00"))
    got = ed.post_earnings_snapshots(snaps, "US", "2026-10-16", "AMC")
    assert got["reaction_day"] == date(2026, 10, 19)
    assert got["before"]["snapshot_date"] == "2026-10-16"
    assert got["day1"]["snapshot_date"] == "2026-10-20"
    assert got["day2"]["snapshot_date"] == "2026-10-21"


def test_day_k_missing_is_none():
    snaps = _chain(("2026-10-20", "2026-10-20T00:15:00+00:00"), ("2026-10-21", "2026-10-21T00:15:00+00:00"))
    got = ed.post_earnings_snapshots(snaps, "US", "2026-10-20", "AMC")
    assert got["day1"] is None and got["day2"] is None


def test_day_k_unknown_time_is_treated_as_after_close():
    assert ed.reaction_day("US", "2026-10-20", None) == date(2026, 10, 21)
    assert ed.timing_label("US", None) == "時間不明（當盤後）"


def test_day_k_taiwan_uses_1330_taipei_close():
    snaps = _chain(("2026-10-15", "2026-10-15T00:15:00+00:00"),    # 週四早上（財報前）
                   ("2026-10-16", "2026-10-16T00:15:00+00:00"),    # 週五早上：週四收盤，還是 R 之前
                   ("2026-10-17", "2026-10-17T00:15:00+00:00"),    # 週六早上：含週五（R）收盤 -> 第 1 天
                   ("2026-10-20", "2026-10-20T00:15:00+00:00"))    # 週二早上：含週一收盤 -> 第 2 天
    got = ed.post_earnings_snapshots(snaps, "TW", "2026-10-15", None)
    assert got["reaction_day"] == date(2026, 10, 16)
    assert got["before"]["snapshot_date"] == "2026-10-15"
    assert got["day1"]["snapshot_date"] == "2026-10-17"
    assert got["day2"]["snapshot_date"] == "2026-10-20"


def test_recent_window_membership():
    now = utc("2026-10-21T00:15:00Z")          # 最近收盤 10/20
    assert ed.reaction_in_recent_window("US", date(2026, 10, 20), now)
    assert ed.reaction_in_recent_window("US", date(2026, 10, 14), now)       # 5 個交易日：14,15,16,19,20
    assert not ed.reaction_in_recent_window("US", date(2026, 10, 13), now)
    assert ed.reaction_in_recent_window("US", date(2026, 10, 21), now)       # 剛發完，等第 1 天
    assert not ed.reaction_in_recent_window("US", date(2026, 10, 22), now)


def test_compute_post_earnings_tracks_end_to_end_with_calendar_years():
    # FAKE：財年 12/31，今年 2026 條件年 (2027, 2028)。財報 10/20 盤後，R = 10/21
    def snap(d, scraped, fy1, fy2, fy3):
        return _daily(d, scraped, FAKE={"eps_fy_curr": fy1, "eps_fy_next": fy2, "eps_fy3": fy3, "source": "xlsx"})
    daily = {
        "2026-10-20": snap("2026-10-20", "2026-10-20T00:15:00+00:00", 5.0, 6.0, 7.0),
        "2026-10-22": snap("2026-10-22", "2026-10-22T00:15:00+00:00", 5.1, 6.6, 7.7),
        "2026-10-23": snap("2026-10-23", "2026-10-23T00:15:00+00:00", 5.2, 6.9, 7.7),
    }
    row = {"ticker": "FAKE", "name": "Fake Inc", "last_earnings_date": "2026-10-20", "last_earnings_time": "AMC",
           "fiscal_year_end": "2025-12-31", "past_earnings_dates": ["2026-02-10", "2026-10-20"]}
    out = ed.compute_post_earnings_tracks(
        [row], daily_snapshots=daily, years=(2027, 2028), now_utc=utc("2026-10-23T00:15:00Z"),
        market_for=lambda r: "US", adr_fn=lambda t, rec: rec)
    assert out["no_baseline"] == []
    tr = out["tracks"]["FAKE"]
    assert tr["reaction_day"] == "2026-10-21" and tr["timing"] == "盤後"
    # FY 12/31 結束；2026 年報在 2027 年初才發，所以 FY1 = 2026，2027 年是第 2 欄，2028 年是第 3 欄
    y27, y28 = tr["years"]
    assert (y27["year"], y27["before"], y27["day1"], y27["day2"]) == (2027, 6.0, 6.6, 6.9)
    assert y27["change_pct"] == pytest.approx(15.0) and y27["change_day"] == 2
    assert (y28["before"], y28["day1"], y28["day2"]) == (7.0, 7.7, 7.7)
    assert [r["ticker"] for r in out["recent"]] == ["FAKE"]


def test_compute_post_earnings_tracks_skips_without_baseline_and_reports_missing_days():
    daily = {"2026-10-22": _daily("2026-10-22", "2026-10-22T00:15:00+00:00",
                                  FAKE={"eps_fy_curr": 5.0, "eps_fy_next": 6.0, "eps_fy3": 7.0, "source": "xlsx"})}
    row = {"ticker": "FAKE", "last_earnings_date": "2026-10-20", "last_earnings_time": "AMC",
           "fiscal_year_end": "2025-12-31", "past_earnings_dates": ["2026-10-20"]}
    out = ed.compute_post_earnings_tracks(
        [row], daily_snapshots=daily, years=(2027, 2028), now_utc=utc("2026-10-23T00:15:00Z"),
        market_for=lambda r: "US", adr_fn=lambda t, rec: rec)
    assert out["recent"] == [] and out["no_baseline"] == ["FAKE"]

    # 有基準、第 2 天還沒抓到：day2 是 None，變動用第 1 天
    daily["2026-10-20"] = _daily("2026-10-20", "2026-10-20T00:15:00+00:00",
                                 FAKE={"eps_fy_curr": 5.0, "eps_fy_next": 5.0, "eps_fy3": 7.0, "source": "xlsx"})
    out = ed.compute_post_earnings_tracks(
        [row], daily_snapshots=daily, years=(2027, 2028), now_utc=utc("2026-10-22T00:15:00Z"),
        market_for=lambda r: "US", adr_fn=lambda t, rec: rec)
    y27 = out["tracks"]["FAKE"]["years"][0]
    assert y27["day2"] is None and y27["change_day"] == 1 and y27["change_pct"] == pytest.approx(20.0)


def test_daily_snapshot_roundtrip_and_same_day_overwrite(tmp_path):
    ex = ExcelSnapshot(snapshot_date="2026-10-21", source_file="a.xlsx",
                       tickers={"AAA": {"fy1": 5.0, "fy2": 6.0, "fy3": 7.0}})
    doc = ed.build_daily_snapshot("smallcap", [ex], scraped_at_utc="2026-10-21T00:20:00+00:00",
                                  source_files=["a.xlsx"], docs_dir=tmp_path)
    path = ed.daily_dir("smallcap", tmp_path) / "2026-10-21.json"
    ed.write_daily_snapshot(path, doc)
    ed.write_daily_snapshot(path, doc)          # 重跑覆蓋，不重複
    loaded = ed.load_daily_snapshots(path.parent)
    assert list(loaded) == ["2026-10-21"]
    assert loaded["2026-10-21"]["tickers"]["AAA"]["eps_fy_next"] == 6.0
    assert loaded["2026-10-21"]["kind"] == "daily"
    # 月快照載入器看不到 daily 子目錄
    assert not list(path.parent.parent.glob("????-??.json"))
