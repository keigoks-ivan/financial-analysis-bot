"""Unit tests for scripts/active_etf/build_active_etf.py's pure functions —
manager-moves classification, active-share vs 0050, and cross-fund consensus
aggregation. No network access; these are the parts of the analysis layer that
don't touch yfinance or the fetch_holdings.py storage layer directly.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR / "etf_dash"))
sys.path.insert(0, str(SCRIPTS_DIR / "active_etf"))

import build_active_etf as bae  # noqa: E402


def _snap(as_of, holdings, units=None):
    """holdings: {ticker: (shares, weight_pct)} -> compact jsonl-shaped snapshot."""
    return {
        "as_of": as_of,
        "holdings": [[t, s, w] for t, (s, w) in holdings.items()],
        "nav": {"units": units} if units is not None else {},
    }


# ── compute_manager_moves: shares/units ratio method ──────────────────────
def test_moves_shares_per_unit_method_used_when_units_present():
    past = _snap("2026-09-01", {"2330.TW": (100000, 10.0)}, units=1_000_000)
    cur = _snap("2026-09-08", {"2330.TW": (110000, 10.0)}, units=1_000_000)  # 純申購也會讓股數變,但這裡 units 沒變
    moves = bae.compute_manager_moves(cur, past)
    assert moves["method"] == "shares_per_unit"
    assert len(moves["increase"]) == 1
    assert moves["increase"][0]["ticker"] == "2330.TW"


def test_moves_ignores_pure_subscription_scaling():
    # 純申購:全部股數等比例放大(units 也等比例放大),股數/單位比值不變 —— 不該被當成加碼
    past = _snap("2026-09-01", {"2330.TW": (100000, 10.0), "2454.TW": (50000, 5.0)}, units=1_000_000)
    cur = _snap("2026-09-08", {"2330.TW": (150000, 10.0), "2454.TW": (75000, 5.0)}, units=1_500_000)
    moves = bae.compute_manager_moves(cur, past)
    assert moves["method"] == "shares_per_unit"
    assert moves["increase"] == [] and moves["decrease"] == []


def test_moves_detects_real_increase_despite_fund_growth():
    # 基金同時在成長(units 漲 20%),但 2330 的股數/單位比值真的漲了(加碼),
    # 2454 的比值沒變(只是跟著申購等比例放大,不算異動)。
    past = _snap("2026-09-01", {"2330.TW": (100000, 10.0), "2454.TW": (50000, 5.0)}, units=1_000_000)
    cur = _snap("2026-09-08", {"2330.TW": (150000, 12.0), "2454.TW": (60000, 5.0)}, units=1_200_000)
    moves = bae.compute_manager_moves(cur, past)
    tickers_increased = {r["ticker"] for r in moves["increase"]}
    assert "2330.TW" in tickers_increased
    assert "2454.TW" not in tickers_increased
    assert "2454.TW" not in {r["ticker"] for r in moves["decrease"]}


def test_moves_new_and_exit():
    past = _snap("2026-09-01", {"2330.TW": (100000, 10.0)}, units=1_000_000)
    cur = _snap("2026-09-08", {"2454.TW": (50000, 5.0)}, units=1_000_000)
    moves = bae.compute_manager_moves(cur, past)
    assert [r["ticker"] for r in moves["new"]] == ["2454.TW"]
    assert [r["ticker"] for r in moves["exit"]] == ["2330.TW"]
    assert moves["exit"][0]["weight_pct_before"] == 10.0


# ── compute_manager_moves: weight_pct fallback when units missing ─────────
def test_moves_falls_back_to_weight_delta_without_units():
    past = _snap("2026-09-01", {"2330.TW": (100000, 10.0)})  # 無 nav.units
    cur = _snap("2026-09-08", {"2330.TW": (100000, 10.5)})
    moves = bae.compute_manager_moves(cur, past)
    assert moves["method"] == "weight_pct_delta"
    assert len(moves["increase"]) == 1
    assert moves["increase"][0]["weight_pct_change_pp"] == 0.5


def test_moves_weight_delta_below_threshold_ignored():
    past = _snap("2026-09-01", {"2330.TW": (100000, 10.0)})
    cur = _snap("2026-09-08", {"2330.TW": (100000, 10.05)})  # < MOVE_WEIGHT_MIN_DELTA_PP (0.10)
    moves = bae.compute_manager_moves(cur, past)
    assert moves["increase"] == [] and moves["decrease"] == []


# ── snapshot_near ────────────────────────────────────────────────────────
def test_snapshot_near_picks_latest_on_or_before_target():
    snaps = [_snap(d, {}) for d in ("2026-08-01", "2026-08-15", "2026-09-01")]
    assert bae.snapshot_near(snaps, "2026-08-20")["as_of"] == "2026-08-15"
    assert bae.snapshot_near(snaps, "2026-07-01") is None
    assert bae.snapshot_near(snaps, "2026-09-01")["as_of"] == "2026-09-01"


# ── active_share vs benchmark ───────────────────────────────────────────
def test_active_share_identical_to_benchmark_is_zero():
    w = {"2330.TW": 50.0, "2454.TW": 50.0}
    assert bae.active_share(w, w) == 0.0


def test_active_share_full_union_math():
    fund = {"2330.TW": 40.0, "6223.TWO": 10.0}
    bench = {"2330.TW": 55.0, "2454.TW": 20.0}
    # union = {2330, 6223, 2454}; |40-55| + |10-0| + |0-20| = 15+10+20 = 45; /2 = 22.5
    assert bae.active_share(fund, bench) == 22.5


def test_active_share_none_when_no_benchmark():
    assert bae.active_share({"2330.TW": 100.0}, {}) is None


# ── cross-fund consensus (build_consensus) ─────────────────────────────
def _fund_result(code, aum, week_moves):
    return {"code": code, "twse_aum": {"aum_100m_twd": aum}, "moves": {"week": week_moves, "month": None}}


def test_build_consensus_counts_and_aum_weights():
    f1 = _fund_result("00980A", 200.0, {
        "new": [{"ticker": "2330.TW", "weight_pct": 5.0}], "increase": [], "decrease": [], "exit": [],
    })
    f2 = _fund_result("00985A", 100.0, {
        "new": [], "increase": [{"ticker": "2330.TW", "weight_pct": 6.0, "weight_pct_change_pp": 1.0}],
        "decrease": [], "exit": [],
    })
    out = bae.build_consensus([f1, f2], "week")
    assert len(out["bought"]) == 1
    row = out["bought"][0]
    assert row["ticker"] == "2330.TW"
    assert row["n_funds_buy"] == 2 and row["n_funds_sell"] == 0
    assert row["net_funds"] == 2
    # f1's "new" record has no weight_pct_before -> delta falls back to weight_pct - 0 = 5.0
    # f2's increase has weight_pct_change_pp = 1.0
    # aum_weighted_score = 5.0*200 + 1.0*100 = 1100
    assert row["aum_weighted_score"] == 1100.0


def test_build_consensus_sold_bucket_for_net_negative():
    f1 = _fund_result("00980A", 200.0, {
        "new": [], "increase": [], "decrease": [{"ticker": "2454.TW", "weight_pct": 3.0, "weight_pct_change_pp": -1.0}],
        "exit": [],
    })
    out = bae.build_consensus([f1], "week")
    assert out["bought"] == []
    assert len(out["sold"]) == 1
    assert out["sold"][0]["ticker"] == "2454.TW"
    assert out["sold"][0]["net_funds"] == -1


def test_build_consensus_skips_funds_with_no_moves_for_window():
    f1 = _fund_result("00980A", 200.0, None)
    out = bae.build_consensus([f1], "week")
    assert out == {"bought": [], "sold": [], "n_funds_with_history": 0, "n_funds_total": 1}


# ── load_0050_weights / benchmark rows: file-missing graceful behavior ────
def test_load_0050_weights_missing_file_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(bae, "ETF_DASH_DATA_DIR", tmp_path)
    weights, as_of = bae.load_0050_weights()
    assert weights == {} and as_of is None


def test_load_benchmark_rows_missing_files_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(bae, "ETF_DASH_DATA_DIR", tmp_path)
    assert bae.load_benchmark_rows() == []
