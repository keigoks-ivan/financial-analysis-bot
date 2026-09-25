"""Unit tests for scripts/active_etf/analytics.py's five analysis modules —
all synthetic in-memory data, no network access.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR / "etf_dash"))
sys.path.insert(0, str(SCRIPTS_DIR / "active_etf"))

import analytics as an  # noqa: E402
import build_active_etf as bae  # noqa: E402 — compute_manager_moves() 傳給 analytics 的 post_trade_performance()


def _snap(as_of, holdings, units=None, nav_per_unit=None, scale=None):
    """holdings: {ticker: (shares, weight_pct)} -> compact jsonl-shaped snapshot."""
    nav = {}
    if units is not None:
        nav["units"] = units
    if nav_per_unit is not None:
        nav["nav_per_unit"] = nav_per_unit
    if scale is not None:
        nav["scale"] = scale
    return {"as_of": as_of, "holdings": [[t, s, w] for t, (s, w) in holdings.items()], "other": [], "nav": nav}


def _price_history(rows):
    """rows: {date: {ticker: close}} -> price_history shape (volume all 1000)."""
    return {d: {"close": dict(closes), "volume": {t: 1000 for t in closes}} for d, closes in rows.items()}


# ── M1a: active_return_attribution ─────────────────────────────────────────
def test_active_return_attribution_basic_overweight_positive_return():
    snaps = [_snap("2026-01-01", {"AAA.TW": (1000, 50.0), "BBB.TW": (1000, 50.0)})]
    bench = {"AAA.TW": 20.0, "BBB.TW": 20.0}
    ph = _price_history({
        "2026-01-01": {"AAA.TW": 100.0, "BBB.TW": 100.0, "FUND.TW": 10.0, "0050.TW": 10.0},
        "2026-01-02": {"AAA.TW": 110.0, "BBB.TW": 100.0, "FUND.TW": 10.5, "0050.TW": 10.2},
    })
    out = an.active_return_attribution(snaps, ph, bench, "2026-01-02", 30, "FUND.TW")
    assert out["status"] == "ok"
    # AAA active weight = 30pp, return 10% -> contribution ~3.0pp; BBB active weight 30pp, return 0 -> 0
    assert out["total_active_return_pct"] > 2.5
    assert out["top_positive"][0]["ticker"] == "AAA.TW"
    assert out["actual_fund_return_pct"] == 5.0
    assert out["bench_return_pct"] == 2.0


def test_active_return_attribution_insufficient_data():
    out = an.active_return_attribution([], {}, {}, "2026-01-02", 30, "FUND.TW")
    assert out["status"] == "no_price_data"


def test_manager_skill_return_attribution_has_three_windows():
    snaps = [_snap("2026-01-01", {"AAA.TW": (1000, 50.0)})]
    bench = {"AAA.TW": 20.0}
    ph = _price_history({
        "2026-01-01": {"AAA.TW": 100.0, "FUND.TW": 10.0, "0050.TW": 10.0},
        "2026-01-02": {"AAA.TW": 105.0, "FUND.TW": 10.2, "0050.TW": 10.1},
    })
    out = an.manager_skill_return_attribution(snaps, ph, bench, "FUND.TW")
    assert set(out) == {"1m", "3m", "since_available"}


# ── M1b: post-trade performance ────────────────────────────────────────────
def test_forward_excess_return_full_window_required():
    series = {"AAA.TW": [("2026-01-0{}".format(i), 100.0 + i, 1000) for i in range(1, 9)]}
    dates = an._dates_of(series["AAA.TW"])
    taiex = [("2026-01-0{}".format(i), 1000.0 + i * 2, None) for i in range(1, 9)]
    taiex_dates = an._dates_of(taiex)
    # horizon 60 far exceeds the 8 available points -> None (incomplete window)
    assert an._forward_excess_return(series, taiex, taiex_dates, "AAA.TW", "2026-01-02", 60) is None
    r = an._forward_excess_return(series, taiex, taiex_dates, "AAA.TW", "2026-01-02", 3)
    assert r is not None and "excess_return_pct" in r


def test_post_trade_performance_counts_buy_and_sell_events():
    snaps = [
        _snap("2026-01-01", {"AAA.TW": (1000, 10.0)}, units=1_000_000),
        _snap("2026-01-08", {"AAA.TW": (2000, 20.0), "BBB.TW": (500, 5.0)}, units=1_000_000),
        _snap("2026-01-15", {"BBB.TW": (500, 5.0)}, units=1_000_000),  # AAA exited
    ]
    # give each ticker a long enough price series to satisfy 20d windows from the earliest event
    dates = ["2026-01-{:02d}".format(d) for d in range(1, 29)]
    series = {"AAA.TW": [(d, 100.0 + i, 1000) for i, d in enumerate(dates)],
              "BBB.TW": [(d, 50.0 + i, 1000) for i, d in enumerate(dates)]}
    taiex = [(d, 1000.0 + i, None) for i, d in enumerate(dates)]
    taiex_dates = an._dates_of(taiex)
    out = an.post_trade_performance("TESTF", snaps, series, taiex, taiex_dates, bae.compute_manager_moves)
    assert out["n_events_total"] >= 2  # at least the AAA increase + AAA exit
    assert 20 in out["buys"] and 20 in out["sells"]


# ── M2: crowding ────────────────────────────────────────────────────────────
def test_compute_crowding_overlap_and_top_lists():
    fund_results = [
        {"code": "F1", "holdings": [{"ticker": "AAA.TW", "shares": 1000, "weight_pct": 40.0},
                                     {"ticker": "BBB.TW", "shares": 500, "weight_pct": 10.0}]},
        {"code": "F2", "holdings": [{"ticker": "AAA.TW", "shares": 2000, "weight_pct": 30.0}]},
    ]
    security_meta = {"AAA.TW": {"name": "A公司", "shares_outstanding": 30000, "market": "TWSE"},
                      "BBB.TW": {"name": "B公司", "shares_outstanding": 100000, "market": "TWSE"}}
    ticker_series = {"AAA.TW": [("2026-01-0{}".format(i), 100.0, 100 * i) for i in range(1, 6)]}
    out = an.compute_crowding(fund_results, security_meta, ticker_series)
    aaa = next(r for r in out["top_by_pct_shares_outstanding"] if r["ticker"] == "AAA.TW")
    assert aaa["total_shares_held"] == 3000
    assert aaa["n_funds_holding"] == 2
    assert round(aaa["pct_of_shares_outstanding"], 2) == 10.0
    m = out["overlap_matrix"]
    i1, i2 = m["codes"].index("F1"), m["codes"].index("F2")
    # overlap F1 vs F2 = min(40,30) on AAA + min(10,0) on BBB = 30
    assert m["matrix"][i1][i2] == 30.0
    assert m["matrix"][i1][i1] == 50.0  # self-overlap = own total weight


# ── M3: fund flows ──────────────────────────────────────────────────────────
def test_compute_fund_flows_price_effect_and_net_flow():
    snaps = [
        _snap("2026-01-01", {"AAA.TW": (1000, 10.0)}, units=1_000_000, nav_per_unit=10.0),
        _snap("2026-01-08", {"AAA.TW": (1000, 10.0)}, units=1_100_000, nav_per_unit=11.0),
    ]
    out = an.compute_fund_flows(snaps)
    assert out["n_events_with_units"] == 1
    ev = out["events"][0]
    # price_effect = 1_000_000 * (11-10) = 1,000,000 TWD = 0.01 億元
    assert ev["price_effect_100m"] == 0.01
    # net_flow = (1,100,000-1,000,000)*11 = 1,100,000 TWD = 0.011 億元
    assert ev["net_flow_100m"] == 0.011


def test_compute_fund_flows_skips_missing_units():
    snaps = [_snap("2026-01-01", {}), _snap("2026-01-08", {}, units=1_000_000, nav_per_unit=10.0)]
    out = an.compute_fund_flows(snaps)
    assert out["n_events_with_units"] == 0
    assert out["cumulative_net_flow_100m"] is None


def test_compute_overview_flows_aggregates_weekly():
    flows_by_code = {
        "F1": {"events": [{"date": "2026-01-05", "net_flow_100m": 1.0, "price_effect_100m": 0.5}],
               "cumulative_net_flow_100m": 1.0, "n_events_with_units": 1},
        "F2": {"events": [{"date": "2026-01-06", "net_flow_100m": -0.5, "price_effect_100m": 0.2}],
               "cumulative_net_flow_100m": -0.5, "n_events_with_units": 1},
    }
    out = an.compute_overview_flows(flows_by_code, {"F1": "Fund 1", "F2": "Fund 2"})
    assert len(out["weekly_net_flow_100m"]) == 1
    assert out["weekly_net_flow_100m"][0]["net_flow_100m"] == 0.5
    assert out["by_fund"][0]["code"] == "F1"  # sorted by cumulative desc


# ── M4: style tilts ──────────────────────────────────────────────────────────
def test_compute_style_tilts_industry_and_size():
    fund_holdings = [{"ticker": "AAA.TW", "weight_pct": 60.0}, {"ticker": "BBB.TW", "weight_pct": 40.0}]
    bench_weights = {"AAA.TW": 20.0, "CCC.TW": 80.0}
    security_meta = {
        "AAA.TW": {"industry_name": "半導體", "shares_outstanding": 1000},
        "BBB.TW": {"industry_name": "食品", "shares_outstanding": 2000},
        "CCC.TW": {"industry_name": "金融保險", "shares_outstanding": 3000},
    }
    latest_close = {"AAA.TW": 100.0, "BBB.TW": 50.0, "CCC.TW": 10.0}
    out = an.compute_style_tilts(fund_holdings, bench_weights, security_meta, latest_close,
                                  fund_periods_90d=5.0, bench_periods_90d=2.0,
                                  fund_fwd_pe=20.0, bench_fwd_pe=18.0,
                                  held_universe_tickers=["AAA.TW", "BBB.TW", "CCC.TW"])
    semis = next(r for r in out["industry_diffs_all"] if r["industry"] == "半導體")
    assert semis["diff_pp"] == 40.0  # 60 - 20
    assert out["fwd_pe_diff"] == 2.0
    assert out["eps_revision_90d_tilt_pp"] == 3.0


# ── M5: operations ───────────────────────────────────────────────────────────
def test_monthly_turnover_computes_trade_value_over_aum():
    snaps = [
        _snap("2026-01-01", {"AAA.TW": (1000, 50.0)}, scale=100000.0),
        _snap("2026-01-08", {"AAA.TW": (1500, 60.0)}, scale=120000.0),
    ]
    ph = _price_history({"2026-01-08": {"AAA.TW": 100.0}})
    out = an.monthly_turnover(snaps, ph)
    assert len(out) == 1
    # trade_value = |1500-1000|*100 = 50000; /2 /120000 *100 = 20.83%
    assert round(out[0]["turnover_pct"], 2) == 20.83


def test_avg_holding_period_days_only_counts_closed_positions():
    # BBB confirmed held on both 01-01 and 01-11 (span = 10 days), gone by 01-21 -> closed.
    # AAA held on all three snapshots -> still open, excluded from the average.
    snaps = [
        _snap("2026-01-01", {"AAA.TW": (1000, 10.0), "BBB.TW": (1000, 10.0)}),
        _snap("2026-01-11", {"AAA.TW": (1000, 10.0), "BBB.TW": (1000, 10.0)}),
        _snap("2026-01-21", {"AAA.TW": (1000, 10.0)}),  # AAA still held (open position)
    ]
    out = an.avg_holding_period_days(snaps)
    assert out["n_closed_positions"] == 1
    assert out["closed"][0]["ticker"] == "BBB.TW"
    assert out["closed"][0]["days"] == 10


def test_compute_operations_flags_low_equity():
    snaps = [_snap("2026-01-01", {"AAA.TW": (1000, 70.0)})]  # 70% < default band min 90%
    ph = _price_history({})
    out = an.compute_operations("00980A", snaps, ph)  # 00980A has a custom low band (80-101)
    assert out["stock_weight_over_time"][0]["low_equity"] is True
    assert out["n_holdings_over_time"][0]["n_holdings"] == 1
