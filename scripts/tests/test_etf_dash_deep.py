"""Unit tests for the 2026-09-26 additions to scripts/etf_dash/build_etf_dash.py
(EPS 修正廣度／報酬貢獻／資金流／風格快照) and their two new helper modules
scripts/etf_dash/price_history.py and scripts/etf_dash/flows.py.

Pure-function coverage only — no network, mirrors the existing
test_etf_dash.py convention (synthetic in-memory fixtures, monkeypatch for
any disk paths).
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "etf_dash"))

import build_etf_dash as m  # noqa: E402
import price_history as ph  # noqa: E402
import flows  # noqa: E402


# ── compute_eps_breadth() ────────────────────────────────────────────────────

def _c(ticker, weight, rev30=None, rev60=None, rev90=None):
    return {"ticker": ticker, "name": ticker, "weight_pct": weight,
            "revisions_pct": {"30d": rev30, "60d": rev60, "90d": rev90}}


def test_compute_eps_breadth_classifies_up_flat_down_by_dead_band():
    constituents = [
        _c("A", 40, rev90=5.0),     # up
        _c("B", 30, rev90=-3.0),    # down
        _c("C", 20, rev90=0.2),     # flat (|0.2| < 0.5 dead band)
        _c("D", 10, rev90=None),    # no data this period -> excluded from n_covered
    ]
    out = m.compute_eps_breadth(constituents)
    b90 = out["90d"]
    assert b90["n_up"] == 1 and b90["n_down"] == 1 and b90["n_flat"] == 1
    assert b90["n_covered"] == 3 and b90["n_total"] == 4
    # covered weight = 40+30+20 = 90 -> renormalized shares (rounded to 2dp by the function)
    assert b90["up_weight_pct"] == pytest.approx(40 / 90 * 100, abs=0.01)
    assert b90["down_weight_pct"] == pytest.approx(30 / 90 * 100, abs=0.01)
    assert b90["flat_weight_pct"] == pytest.approx(20 / 90 * 100, abs=0.01)
    # three buckets sum to ~100 (each independently rounded to 2dp, so allow tiny rounding drift)
    assert b90["up_weight_pct"] + b90["down_weight_pct"] + b90["flat_weight_pct"] == pytest.approx(100.0, abs=0.05)


def test_compute_eps_breadth_weighted_median_revision():
    # weight-sorted: B(-3, w30) < C(0.2, w20) < A(5, w40) — cumulative weight
    # crosses half (45) inside A's bucket (30+20=50 >= 45) -> median falls on C? verify formula directly.
    constituents = [_c("A", 40, rev90=5.0), _c("B", 30, rev90=-3.0), _c("C", 20, rev90=0.2)]
    out = m.compute_eps_breadth(constituents)
    med = out["90d"]["weighted_median_revision_pct"]
    assert med is not None
    # sorted by value: B(-3,30) C(0.2,20) A(5,40); total=90, half=45;
    # cumulative after B=30 (<45), after C=50 (>=45) -> median = C's value = 0.2
    assert med == pytest.approx(0.2)


def test_compute_eps_breadth_no_covered_data_returns_none_stats():
    constituents = [_c("A", 40, rev90=None), _c("B", 60, rev90=None)]
    out = m.compute_eps_breadth(constituents)
    b90 = out["90d"]
    assert b90["n_covered"] == 0
    assert b90["up_weight_pct"] is None and b90["weighted_median_revision_pct"] is None


def test_compute_eps_breadth_covers_all_period_defs_keys():
    out = m.compute_eps_breadth([_c("A", 100, rev30=1, rev60=1, rev90=1)])
    assert set(out.keys()) == {k for k, *_ in m.PERIOD_DEFS}


# ── _weighted_median() / _weighted_quantile() ────────────────────────────────

def test_weighted_median_simple_majority():
    assert m._weighted_median([(1.0, 90), (100.0, 10)]) == pytest.approx(1.0)


def test_weighted_median_empty_returns_none():
    assert m._weighted_median([]) is None
    assert m._weighted_median([(5.0, 0)]) is None  # zero weight filtered out


def test_weighted_quantile_median_of_uniform_weights():
    pairs = [(v, 1.0) for v in [10, 20, 30, 40, 50]]
    assert m._weighted_quantile(pairs, 0.5) == pytest.approx(30, abs=5)


def test_weighted_quantile_empty_returns_none():
    assert m._weighted_quantile([], 0.5) is None


# ── resolve_sector() ─────────────────────────────────────────────────────────

def test_resolve_sector_prefers_raw_sector_field():
    assert m.resolve_sector("8306.T", "銀行業", {}, {}) == "銀行業"


def test_resolve_sector_tw_ticker_uses_industry_map():
    tw_map = {"2330": "半導體"}
    assert m.resolve_sector("2330.TW", None, {}, tw_map) == "半導體"
    assert m.resolve_sector("5880.TWO", None, {}, {"5880": "金融保險"}) == "金融保險"


def test_resolve_sector_us_ticker_uses_sector_lookup():
    us = {"NVDA": "科技"}
    assert m.resolve_sector("NVDA", None, us, {}) == "科技"


def test_resolve_sector_unresolvable_returns_none():
    assert m.resolve_sector("ZZZZ", None, {}, {}) is None


# ── compute_price_contribution() ─────────────────────────────────────────────

def _cc(ticker, weight, price_local, sector=None):
    return {"ticker": ticker, "name": ticker, "weight_pct": weight, "price_local": price_local,
            "sector": sector}


def test_compute_price_contribution_basic_return_and_contribution():
    today = "2026-09-26"
    base_1m = "2026-08-27"  # 30 days before
    price_days = {base_1m: {"AAA": 100.0, "BBB": 50.0}}
    constituents = [_cc("AAA", 60, 110.0), _cc("BBB", 40, 45.0)]
    out = m.compute_price_contribution("SPY", constituents, 100.0, price_days, today, {}, {})
    p1m = out["1M"]
    assert p1m["n_covered"] == 2
    aaa = next(r for r in p1m["top10"] + p1m["bottom10"] if r["ticker"] == "AAA")
    assert aaa["return_pct"] == pytest.approx(10.0)
    assert aaa["contribution_pct"] == pytest.approx(60 / 100 * 10.0)
    bbb = next(r for r in p1m["top10"] + p1m["bottom10"] if r["ticker"] == "BBB")
    assert bbb["return_pct"] == pytest.approx(-10.0)
    assert bbb["contribution_pct"] == pytest.approx(40 / 100 * -10.0)


def test_compute_price_contribution_missing_history_gives_zero_coverage():
    constituents = [_cc("AAA", 100, 110.0)]
    out = m.compute_price_contribution("SPY", constituents, 100.0, {}, "2026-09-26", {}, {})
    assert out["1M"]["n_covered"] == 0
    assert out["1M"]["coverage_pct"] == 0.0
    assert out["1M"]["top10"] == []


def test_compute_price_contribution_sector_aggregation_for_eligible_fund():
    today = "2026-09-26"
    base = "2026-08-27"
    price_days = {base: {"AAA": 100.0, "BBB": 100.0}}
    constituents = [_cc("AAA", 50, 120.0, sector="科技"), _cc("BBB", 50, 90.0, sector="金融")]
    out = m.compute_price_contribution("QQQ", constituents, 100.0, price_days, today, {}, {})
    sc = {r["sector"]: r["contribution_pct"] for r in out["1M"]["sector_contribution"]}
    assert sc["科技"] == pytest.approx(50 / 100 * 20.0)
    assert sc["金融"] == pytest.approx(50 / 100 * -10.0)


def test_compute_price_contribution_no_sector_for_ineligible_fund():
    constituents = [_cc("AAA", 100, 110.0, sector="科技")]
    out = m.compute_price_contribution("SMH", constituents, 100.0, {}, "2026-09-26", {}, {})
    assert out["1M"]["sector_contribution"] is None


# ── compute_style_snapshot() ─────────────────────────────────────────────────

def _sc(ticker, weight, mcap=None, eps_usd=None, price_usd=None, sector=None):
    return {"ticker": ticker, "name": ticker, "weight_pct": weight, "market_cap_local": mcap,
            "eps_fy_next_usd": eps_usd, "price_usd": price_usd, "sector": sector}


def test_compute_style_snapshot_size_quantiles():
    constituents = [_sc("A", 50, mcap=1000), _sc("B", 50, mcap=3000)]
    out = m.compute_style_snapshot("SPY", constituents, 100.0, {}, {})
    size = out["size"]
    assert size["n_covered"] == 2
    assert size["weighted_median_market_cap"] is not None


def test_compute_style_snapshot_pe_dispersion_excludes_outliers():
    # PGR-style outlier: price_usd/eps_fy_next_usd way outside [3x,300x]
    constituents = [
        _sc("A", 50, eps_usd=10, price_usd=200),   # pe=20x, kept
        _sc("B", 50, eps_usd=1000, price_usd=200),  # pe=0.2x, excluded
    ]
    out = m.compute_style_snapshot("SPY", constituents, 100.0, {}, {})
    pe = out["pe_dispersion"]
    assert pe["n_covered"] == 1
    assert pe["weighted_median"] == pytest.approx(20.0)


def test_compute_style_snapshot_sector_weights_only_for_eligible_funds():
    constituents = [_sc("A", 100, sector="科技")]
    out_qqq = m.compute_style_snapshot("QQQ", constituents, 100.0, {}, {})
    assert out_qqq["sector_weights"] == [{"sector": "科技", "weight_pct": 100.0}]
    out_smh = m.compute_style_snapshot("SMH", constituents, 100.0, {}, {})
    assert out_smh["sector_weights"] is None


# ── build_us_sector_lookup() ─────────────────────────────────────────────────

def test_build_us_sector_lookup_reads_sector_fund_caches(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_CACHE_DIR", tmp_path)
    (tmp_path / "XLK.json").write_text(json.dumps({
        "holdings": [{"ticker": "AAPL", "name": "Apple", "weight_pct": 10}]
    }), encoding="utf-8")
    lookup = m.build_us_sector_lookup()
    assert lookup["AAPL"] == "科技"


def test_build_us_sector_lookup_missing_cache_files_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_CACHE_DIR", tmp_path)
    assert m.build_us_sector_lookup() == {}


# ── price_history.py ─────────────────────────────────────────────────────────

def test_price_history_append_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(ph, "PRICES_JSONL_PATH", tmp_path / "prices.jsonl")
    ph.append_today("2026-09-24", {"AAA": 100.0})
    ph.append_today("2026-09-25", {"AAA": 101.0, "BBB": 50.0})
    days = ph.load_days()
    assert days["2026-09-24"] == {"AAA": 100.0}
    assert days["2026-09-25"] == {"AAA": 101.0, "BBB": 50.0}


def test_price_history_same_day_rerun_merges_not_duplicates(tmp_path, monkeypatch):
    monkeypatch.setattr(ph, "PRICES_JSONL_PATH", tmp_path / "prices.jsonl")
    ph.append_today("2026-09-25", {"AAA": 100.0})
    ph.append_today("2026-09-25", {"BBB": 50.0})  # same day, different ticker
    days = ph.load_days()
    assert len(days) == 1
    assert days["2026-09-25"] == {"AAA": 100.0, "BBB": 50.0}


def test_price_history_prunes_to_max_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(ph, "PRICES_JSONL_PATH", tmp_path / "prices.jsonl")
    monkeypatch.setattr(ph, "MAX_ROWS", 3)
    for i in range(5):
        ph.append_today(f"2026-09-{20+i:02d}", {"AAA": float(i)})
    days = ph.load_days()
    assert len(days) == 3
    assert sorted(days.keys()) == ["2026-09-22", "2026-09-23", "2026-09-24"]


def test_price_history_closest_close_on_or_before_finds_nearest_earlier_day():
    days = {"2026-09-01": {"AAA": 10.0}, "2026-09-10": {"AAA": 12.0}}
    found = ph.closest_close_on_or_before(days, "AAA", "2026-09-15")
    assert found == ("2026-09-10", 12.0)


def test_price_history_closest_close_on_or_before_no_data_before_target_returns_none():
    days = {"2026-09-10": {"AAA": 12.0}}
    assert ph.closest_close_on_or_before(days, "AAA", "2026-09-01") is None


def test_price_history_closest_close_on_or_before_missing_ticker_returns_none():
    days = {"2026-09-10": {"BBB": 12.0}}
    assert ph.closest_close_on_or_before(days, "AAA", "2026-09-15") is None


# ── flows.py ─────────────────────────────────────────────────────────────────

def test_flows_append_today_idempotent_same_day(tmp_path, monkeypatch):
    monkeypatch.setattr(flows, "FLOWS_DIR", tmp_path)
    flows.append_today("SPY", {"date": "2026-09-25", "shares_outstanding": 100, "nav": 10.0})
    flows.append_today("SPY", {"date": "2026-09-25", "shares_outstanding": 101, "nav": 10.1})
    rows = flows.load_rows("SPY")
    assert len(rows) == 1
    assert rows[0]["shares_outstanding"] == 101


def test_flows_compute_flow_series_basic_delta_and_weekly_and_cumulative():
    rows = [
        {"date": "2026-09-22", "shares_outstanding": 1000, "nav": 10.0},  # Tuesday
        {"date": "2026-09-23", "shares_outstanding": 1010, "nav": 10.0},  # +10 shares
        {"date": "2026-09-24", "shares_outstanding": 1005, "nav": 10.0},  # -5 shares
    ]
    out = flows.compute_flow_series(rows)
    assert out["n_snapshots"] == 3
    assert len(out["daily"]) == 2
    assert out["daily"][0]["flow_shares"] == 10
    assert out["daily"][0]["flow_amount"] == pytest.approx(100.0)
    assert out["daily"][1]["flow_shares"] == -5
    # same ISO week (all in the same Tue-Wed-Thu) -> one weekly row
    assert len(out["weekly"]) == 1
    assert out["weekly"][0]["flow_shares"] == 5
    assert out["cumulative_since_start"] == pytest.approx((10 * 10.0) + (-5 * 10.0))


def test_flows_compute_flow_series_skips_rows_missing_data():
    rows = [
        {"date": "2026-09-22", "shares_outstanding": 1000, "nav": 10.0},
        {"date": "2026-09-23", "shares_outstanding": None, "nav": None, "source": None},
        {"date": "2026-09-24", "shares_outstanding": 1010, "nav": 10.0},
    ]
    out = flows.compute_flow_series(rows)
    # only 2 valid snapshots -> 1 daily delta, spanning the gap day correctly
    assert out["n_snapshots"] == 2
    assert len(out["daily"]) == 1
    assert out["daily"][0]["flow_shares"] == 10


def test_flows_compute_flow_series_empty_input():
    out = flows.compute_flow_series([])
    assert out["n_snapshots"] == 0
    assert out["daily"] == [] and out["weekly"] == []
    assert out["cumulative_since_start"] is None


def test_flows_fetch_shares_snapshot_direct_source(monkeypatch):
    class FakeTicker:
        def get_info(self):
            return {"sharesOutstanding": 1000, "navPrice": 20.0, "totalAssets": 25000, "currency": "USD"}

    class FakeYF:
        def Ticker(self, tk):
            return FakeTicker()

    out = flows.fetch_shares_snapshot(FakeYF(), "SPY")
    assert out["source"] == "direct"
    assert out["shares_outstanding"] == 1000
    assert out["nav"] == 20.0


def test_flows_fetch_shares_snapshot_derives_from_aum_nav_when_shares_missing(monkeypatch):
    class FakeTicker:
        def get_info(self):
            return {"sharesOutstanding": None, "navPrice": 10.0, "totalAssets": 5000, "currency": "JPY"}

    class FakeYF:
        def Ticker(self, tk):
            return FakeTicker()

    out = flows.fetch_shares_snapshot(FakeYF(), "1475.T")
    assert out["source"] == "derived"
    assert out["shares_outstanding"] == 500


def test_flows_fetch_shares_snapshot_no_usable_data(monkeypatch):
    class FakeTicker:
        def get_info(self):
            return {"sharesOutstanding": None, "navPrice": None, "totalAssets": None}

    class FakeYF:
        def Ticker(self, tk):
            return FakeTicker()

    out = flows.fetch_shares_snapshot(FakeYF(), "XXX")
    assert out["source"] is None
    assert out["shares_outstanding"] is None


def test_flows_fetch_shares_snapshot_get_info_raises_is_caught(monkeypatch):
    class FakeTicker:
        def get_info(self):
            raise RuntimeError("boom")

    class FakeYF:
        def Ticker(self, tk):
            return FakeTicker()

    out = flows.fetch_shares_snapshot(FakeYF(), "XXX")
    assert out["source"] is None
    assert "boom" in out["reason"]


# ── TWSE industry map (fetch_tw_industry_map parsing logic, no network) ────

def test_fetch_tw_industry_map_parses_company_list(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        class R:
            def raise_for_status(self):
                pass

            def json(self):
                return [
                    {"公司代號": "2330", "產業別": "24"},
                    {"公司代號": "2882", "產業別": "17"},
                    {"公司代號": "BADCODE", "產業別": "99"},  # not 4-digit -> skipped
                ]
        return R()
    monkeypatch.setattr(m.requests, "get", fake_get)
    out = m.fetch_tw_industry_map()
    assert out["2330"] == "半導體"
    assert out["2882"] == "金融保險"
    assert "BADCODE" not in out


def test_get_tw_industry_map_falls_back_to_cache_on_fetch_failure(tmp_path, monkeypatch):
    cache_path = tmp_path / "tw_industry_map.json"
    cache_path.write_text(json.dumps({"2330": "半導體"}), encoding="utf-8")
    monkeypatch.setattr(m, "TW_INDUSTRY_MAP_CACHE", cache_path)

    def _boom():
        raise RuntimeError("network down")
    monkeypatch.setattr(m, "fetch_tw_industry_map", _boom)
    out = m.get_tw_industry_map()
    assert out == {"2330": "半導體"}


# ── parse_ishares_jp_holdings_csv sector capture (additive field) ──────────

def test_parse_ishares_jp_holdings_csv_captures_sector_field():
    # Mirrors test_etf_dash.py's fixture shape (Sector column present).
    raw = (
        '基準日,"2026年9月23日"\n\xa0\n'
        'Ticker,Name,Sector,Asset Class,Weight (%)\n'
        '"8306","MUFG","銀行業","株式","3.93"\n'
    ).encode("utf-8-sig")
    as_of, rows, non_equity = m.parse_ishares_jp_holdings_csv(raw)
    assert rows[0]["sector"] == "銀行業"


def test_parse_ishares_jp_holdings_csv_missing_sector_column_is_none():
    raw = (
        '基準日,"2026年9月23日"\n\xa0\n'
        'Ticker,Name,Asset Class,Weight (%)\n'
        '"8306","MUFG","株式","3.93"\n'
    ).encode("utf-8-sig")
    as_of, rows, non_equity = m.parse_ishares_jp_holdings_csv(raw)
    assert rows[0]["sector"] is None
