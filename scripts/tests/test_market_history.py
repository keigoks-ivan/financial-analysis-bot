"""2026-09-13：驗證官方歷史頻率、修訂界線與跨市場缺口降級。"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("market_history", ROOT / "scripts" / "market_history.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def _write(tmp_path, source_id, frequency, unit, observations, mode="latest_revised"):
    root = tmp_path / "market_sources"
    series = root / "series"
    series.mkdir(parents=True, exist_ok=True)
    (series / (source_id + ".json")).write_text(json.dumps({
        "schema": "market-observations-v1", "id": source_id, "frequency": frequency,
        "unit": unit, "data_mode": mode, "source_url": "https://example.test/" + source_id,
        "observations": observations,
    }), encoding="utf-8")
    (root / "latest.json").write_text('{"quotes":{}}', encoding="utf-8")
    (tmp_path / "market_source_registry.json").write_text(json.dumps({"sources": [{
        "id": source_id, "label": source_id, "region": "US", "frequency": frequency,
        "unit": unit, "data_mode": mode, "source_url": "https://example.test/" + source_id,
    }]}), encoding="utf-8")
    return series


def test_daily_windows_report_actual_dates_and_future_is_excluded(tmp_path):
    series = _write(tmp_path, "fred_treasury_10y", "daily", "percent", [
        {"date": "2026-08-01", "value": 4.0}, {"date": "2026-09-01", "value": 4.2},
        {"date": "2026-09-20", "value": 9.9},
    ])
    result = MOD.build_history_context({}, series, "2026-09-13")
    item = result["series"][0]
    assert item["latest"] == {"date": "2026-09-01", "value": 4.2}
    assert item["changes"]["30d"]["actual_start"] == "2026-08-01"
    assert item["changes"]["30d"]["bp"] == 20.0


def test_monthly_price_level_uses_yoy_and_never_fakes_weekly_change(tmp_path):
    observations = [{"date": "2025-%02d-01" % month, "value": 100 + month} for month in range(1, 13)]
    observations += [{"date": "2026-%02d-01" % month, "value": 103 + month} for month in range(1, 9)]
    series = _write(tmp_path, "fred_cpi", "monthly", "index_1982_84_100", observations)
    item = MOD.build_history_context({}, series, "2026-09-13")["series"][0]
    assert item["transform"] == "yoy"
    assert item["unit"] == "percent"
    assert item["changes"]["7d"]["status"] == "incompatible_frequency"
    assert item["changes"]["30d"]["comparison"] == "mom"
    assert item["changes"]["365d"]["comparison"] == "yoy"


def test_monthly_alignment_does_not_use_wrong_month_or_fake_yoy_across_gap(tmp_path):
    observations = [{"date": "2025-%02d-01" % month, "value": 100 + month} for month in range(1, 13)]
    observations += [{"date": "2026-01-01", "value": 110}, {"date": "2026-03-01", "value": 112}]
    series = _write(tmp_path, "some_monthly", "monthly", "index", observations)
    item = MOD.build_history_context({}, series, "2026-03-15")["series"][0]
    assert item["changes"]["30d"]["status"] == "insufficient_history"
    assert item["changes"]["365d"]["actual_start"] == "2025-03-01"


def test_daily_sparse_history_does_not_cross_large_gap(tmp_path):
    series = _write(tmp_path, "fred_dollar", "daily", "index", [
        {"date": "2025-09-01", "value": 90}, {"date": "2026-09-01", "value": 100},
    ])
    item = MOD.build_history_context({}, series, "2026-09-13")["series"][0]
    assert item["changes"]["7d"]["status"] == "insufficient_history"


def test_public_compare_observations_keeps_existing_value_keys():
    result = MOD.compare_observations([
        {"date": "2025-09-01", "value": 100}, {"date": "2026-09-01", "value": 105},
    ], "monthly", "index", 365)
    assert result["before"] == 100
    assert result["current"] == 105
    assert result["delta"] == 5
    assert result["comparison_label"] == "年增"


def test_latest_revised_is_not_replay_eligible_and_future_publication_is_hidden(tmp_path):
    series = _write(tmp_path, "fred_dollar", "daily", "index", [
        {"date": "2026-08-01", "value": 100},
        {"date": "2026-09-01", "value": 102, "published_at": "2026-09-20"},
    ])
    result = MOD.build_history_context({}, series, "2026-09-13")
    assert result["series"][0]["latest"]["date"] == "2026-08-01"
    assert result["series"][0]["replay_eligible"] is False
    assert "latest_revised" in result["replay"]["note"]


def test_regions_use_monitor_latest_and_disclose_no_long_history(tmp_path):
    series = _write(tmp_path, "fred_dollar", "daily", "index", [{"date": "2026-09-01", "value": 100}])
    state = {"evidence": {"quotes": {"monitor:n225": {
        "label": "日經 225", "num": 40000, "val": "40,000", "as_of": "2026-09-11", "chg30_pct": -1.2,
    }}}}
    result = MOD.build_history_context(state, series, "2026-09-13")
    japan = next(row for row in result["regions"] if row["id"] == "JP")
    assert japan["observations"][0]["chg30_pct"] == -1.2
    assert "缺少附日期的長期歷史" in japan["data_gaps"][0]


def test_undated_monitor_spark_does_not_claim_long_history(tmp_path):
    series = _write(tmp_path, "fred_dollar", "daily", "index", [{"date": "2026-09-01", "value": 100}])
    state = {"evidence": {"quotes": {"monitor:n225": {
        "label": "日經 225", "num": 40000, "as_of": "2026-09-11", "spark": [39000, 40000],
    }}}}
    japan = next(row for row in MOD.build_history_context(state, series, "2026-09-13")["regions"] if row["id"] == "JP")
    card = next(row for row in japan["observations"] if row["ref"] == "monitor:n225")
    assert card["history"] == [39000, 40000]
    assert card["long_history"] is False
    assert any("日經 225" in gap for gap in japan["data_gaps"])


def test_future_invalid_monitor_quotes_are_excluded_and_coverage_is_grouped(tmp_path):
    series = _write(tmp_path, "fred_dollar", "daily", "index", [{"date": "2026-09-01", "value": 100}])
    state = {"evidence": {"quotes": {
        "monitor:sp500": {"label": "S&P 500", "num": 1, "as_of": "2026-09-20"},
        "monitor:usdtwd": {"label": "USD/TWD", "num": float("inf"), "as_of": "2026-09-01"},
    }}}
    result = MOD.build_history_context(state, series, "2026-09-13")
    us = next(row for row in result["regions"] if row["id"] == "US")
    assert all(row["ref"] != "monitor:sp500" for row in us["observations"])
    assert us["coverage"]["available"] <= us["coverage"]["requested"]


def test_compact_preserves_first_and_last_points():
    rows = [{"date": "2026-01-%03d" % index, "value": index} for index in range(200)]
    compact = MOD._compact(rows, maximum=10)
    assert compact[0] == {"date": rows[0]["date"], "value": 0}
    assert compact[-1] == {"date": rows[-1]["date"], "value": 199}


def test_short_economic_history_remains_level(tmp_path):
    series = _write(tmp_path, "fred_cpi", "monthly", "index", [
        {"date": "2026-07-01", "value": 100}, {"date": "2026-08-01", "value": 101},
    ])
    item = MOD.build_history_context({}, series, "2026-09-13")["series"][0]
    assert item["transform"] == "level"
    assert item["unit"] == "index"


def test_economic_yoy_uses_same_month_when_history_has_a_missing_month(tmp_path):
    # 2026-09-13：缺一個月不可把第十二筆舊資料誤當去年同月。
    observations = [{"date": "2025-%02d-01" % month, "value": 100 + month}
                    for month in range(1, 13) if month != 2]
    observations += [{"date": "2026-01-01", "value": 110}, {"date": "2026-03-01", "value": 112}]
    series = _write(tmp_path, "fred_cpi", "monthly", "index", observations)
    item = MOD.build_history_context({}, series, "2026-03-15")["series"][0]
    assert item["latest"]["value"] == round((112 / 103 - 1) * 100, 6)


def test_weekly_series_does_not_offer_seven_day_comparison_even_with_baseline():
    result = MOD.compare_observations([
        {"date": "2026-09-01", "value": 100}, {"date": "2026-09-08", "value": 102},
    ], "weekly", "index", 7)
    assert result["status"] == "incompatible_frequency"


def test_missing_sources_explain_non_equivalent_substitutes(tmp_path):
    series = _write(tmp_path, "fred_real_gdp", "quarterly", "billion_USD", [
        {"date": "2025-01-01", "value": 100}, {"date": "2026-01-01", "value": 102},
    ])
    missing = {row["id"]: row for row in MOD.build_history_context({}, series, "2026-09-13")["missing_sources"]}
    assert missing["bea_real_gdp_growth"]["substitute_ref"] == "source:fred_real_gdp"
    assert "不能冒充庫存" in missing["eia_crude_stocks"]["substitute_limit"]
    assert "不能做" in missing["alfred_cpiaucsl"]["impact"]
