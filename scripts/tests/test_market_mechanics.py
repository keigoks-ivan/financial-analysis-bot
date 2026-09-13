"""2026-09-13：市況主控台機械方向、來源與新鮮度契約。"""
from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_market_state as market
import build_monitor as monitor
import build_monitor_internals as internals


def _read(flows):
    return market.build_read_zh(
        {}, flows, None, {"fresh": False}, {"modules": {}, "ledger_sources": {}},
        [{"key": k, "tone": "good", "value": "正常"}
         for k in ("regime", "macro_clock", "detective", "monitor")],
        {}, [],
    )


def test_cta_signed_distance_controls_pressure_language_and_trigger_direction():
    above = {"cta": [{"market": "SPX", "levels": [{"dist_pct": 1.78}]}],
             "vol_control": {}, "lev_etf": {}}
    below = {"cta": [{"market": "SPX", "levels": [{"dist_pct": -1.78}]}],
             "vol_control": {}, "lev_etf": {}}
    assert "上方 1.8% 有機械追價買盤" in _read(above)["headline"]
    assert "下方 1.8% 有機械賣壓" in _read(below)["headline"]

    ff = {"frozen_forecast": {"cta": [{"market": "SPX", "nearest_flip_level": 777.88,
          "nearest_flip_window": 20, "current_composite": "+2/3",
          "if_breached_composite": "+3/3"}]}}
    trigger = market.build_triggers(ff, [], [])[0]
    assert trigger["label"] == "SPY 收盤站上"
    assert "翻多" in trigger["why"]


def test_matched_fuse_uses_monitor_value_and_keeps_intel_snapshot():
    intel = {"date": "2026-09-01", "flags": [{"theme": "Rates", "metric": "yield",
             "value": 4.0, "threshold": 5.0, "distance_pct": 25.0}]}
    rows = [{"id": "x", "source": "macro-falsifier", "status": "open",
             "episode_id": "macro:Rates:yield", "resolver": {"series": "monitor:dgs10",
             "value": 5.0, "unit": "%"}, "p": 0.5}]
    mon = {"categories": [{"items": [{"key": "dgs10", "val": "4.50%",
                                       "date": "2026-09-11"}]}]}
    fuse = market.build_fuses(intel, rows, mon, [])[0]
    assert fuse["now"] == "4.5%" and fuse["dist_pct"] == 11.1
    assert fuse["as_of"] == "2026-09-11" and fuse["source_id"] == "monitor:dgs10"
    assert fuse["historical"]["value"] == 4.0


def test_cpi_yoy_is_repaired_from_official_365_day_period():
    evidence = {"quotes": {"internals:cpi_yoy": {"num": 99.0, "val": "99%",
                "pctile": 100.0, "z": 8.0, "chg30_pct": 50.0}},
                "labor_inflation": {"cpi_yoy": 99.0}}
    source = {"sources": [{"id": "fred_cpi", "status": "ok",
               "latest": {"date": "2026-08-01"}, "periods": [{"days": 365,
               "status": "ok", "before": 100.0, "current": 103.0,
               "actual_start": "2025-08-01", "current_date": "2026-08-01"}]}]}
    market.repair_cpi_yoy_from_official(evidence, source, [])
    assert evidence["quotes"]["internals:cpi_yoy"]["num"] == 3.0
    assert evidence["quotes"]["internals:cpi_yoy"]["pctile"] is None
    assert evidence["quotes"]["internals:cpi_yoy"]["z"] is None
    assert evidence["labor_inflation"]["cpi_yoy"] == 3.0


def test_future_date_is_stale_and_frequency_windows_are_explicit():
    assert market.classify_stale("2026-09-14", date(2026, 9, 13), "daily") == (True, "stale")
    assert market.classify_stale("2026-09-07", date(2026, 9, 13), "weekly") == (False, "ok")
    assert market.classify_stale("2026-08-01", date(2026, 9, 13), "monthly") == (False, "ok")
    assert internals.yoy_series([(f"2025-{m:02d}-01", 100.0) for m in range(1, 13)] +
                                [("2026-01-01", 103.0)])[-1][1] == 3.0
    assert monitor.S["tp10y"]["ticker"] == "THREEFYTP10"
    assert "Kim–Wright" in monitor.S["tp10y"]["label"]


def test_old_monitor_cache_gets_registry_metadata_and_canonical_tp_label():
    old = {"categories": [{"items": [{"key": "tp10y", "label": "期限溢價（ACM）",
            "val": "0.50%", "date": "2026-09-08", "pctile": 40.0, "stale": False},
           {"key": "vix9d", "label": "VIX9D", "val": "14.0", "date": "2026-07-01",
            "stale": True}]}]}
    quotes = market.build_quotes(old, None, None, None, None, {}, [])
    tp = quotes["monitor:tp10y"]
    assert tp["label"] == "10Y 期限溢價（Kim–Wright）"
    assert (tp["source_id"], tp["frequency"], tp["pctile_window"], tp["unit"]) == (
        "FRED:THREEFYTP10", "weekly", "52_observations", "pct")
    assert tp["source_label"] == "Kim–Wright／FRED" and tp["status"] == "ok"
    assert quotes["monitor:vix9d"]["status"] == "stale"


def test_level_units_are_not_change_algorithm_units():
    old = {"categories": [{"items": [
        {"key": "sp500", "val": "7,656.98", "date": "2026-09-11"},
        {"key": "n225", "val": "64,011.34", "date": "2026-09-11"},
        {"key": "usdjpy", "val": "153.55", "date": "2026-09-11"},
        {"key": "wti", "val": "$97.26", "date": "2026-09-11"},
        {"key": "sofr_iorb", "val": "-3bps", "date": "2026-09-11"},
    ]}]}
    q = market.build_quotes(old, None, None, None, None, {}, [])
    assert q["monitor:sp500"]["unit"] == "index"
    assert q["monitor:n225"]["unit"] == "index"
    assert q["monitor:usdjpy"]["unit"] == "JPY_per_USD"
    assert q["monitor:wti"]["unit"] == "USD"
    assert q["monitor:sofr_iorb"]["unit"] == "bp"


def test_fuse_resolver_prefers_evidence_namespace_and_unmatched_exact_map():
    intel = {"date": "2026-08-21", "flags": [
        {"theme": "USEconomy", "metric": "核心 PCE 年增", "value": 3.29,
         "threshold": 3.5, "distance_pct": 6.0},
        {"theme": "GlobalLiquidity", "metric": "DXY／美元 COT", "value": 98.8,
         "threshold": 102.0, "distance_pct": 3.1}]}
    rows = [{"id": "pce", "source": "macro-falsifier", "status": "open",
             "episode_id": "macro:USEconomy:核心 PCE 年增",
             "resolver": {"series": "internals:core_pce_yoy", "value": 3.5, "unit": "%"}}]
    evidence = {"internals:core_pce_yoy": {"num": 3.34, "as_of": "2026-07-01"},
                "monitor:dxy": {"num": 99.12, "as_of": "2026-09-11"}}
    fuses = market.build_fuses(intel, rows, {}, [], evidence)
    assert fuses[0]["now"] == "3.34%" and fuses[0]["source_id"] == "internals:core_pce_yoy"
    assert fuses[1]["now"] == "99.12" and fuses[1]["source_id"] == "monitor:dxy"


def test_zero_current_fuse_keeps_absolute_rate_distance():
    intel = {"date": "2026-09-01", "flags": [{"theme": "Rates", "metric": "yield",
             "value": 1.0, "threshold": 5.0, "distance_pct": 400.0}]}
    rows = [{"id": "x", "source": "macro-falsifier", "status": "open",
             "episode_id": "macro:Rates:yield", "resolver": {"series": "monitor:dgs10",
             "value": 5.0, "unit": "%"}}]
    mon = {"categories": [{"items": [{"key": "dgs10", "val": "0.00%",
                                       "date": "2026-09-11"}]}]}
    fuse = market.build_fuses(intel, rows, mon, [])[0]
    assert fuse["dist_pct"] is None
    assert fuse["distance_abs"] == 500.0 and fuse["change_unit"] == "bp"
