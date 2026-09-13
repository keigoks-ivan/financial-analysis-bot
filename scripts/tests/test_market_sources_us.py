#!/usr/bin/env python3
"""2026-09-13：驗證官方來源 adapter 的 bounded 請求與原始值解析。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
import market_sources_us as sources  # noqa: E402


class FakeClient:
    """測試 client：保留 adapter 提出的請求，但不接觸網路或憑證。"""

    def __init__(self, json_response=None, text_response=None, env=None):
        self.json_response = json_response
        self.text_response = text_response
        self.env = env or {}
        self.calls = []

    def get_env(self, name):
        return self.env.get(name)

    def get_json(self, url, params=None, headers=None):
        self.calls.append(("json", url, params, headers))
        return self.json_response

    def get_text(self, url, params=None, headers=None):
        self.calls.append(("text", url, params, headers))
        return self.text_response

    def post_json(self, url, payload, headers=None):
        self.calls.append(("post", url, payload, headers))
        raise AssertionError("adapter must not POST")


def spec(provider, series, **extra):
    result = {"id": "test", "provider": provider, "series": series,
              "unit": "percent", "frequency": "daily"}
    result.update(extra)
    return result


def test_fred_fallback_marks_latest_revised_and_filters_csv_range():
    item = spec("fred", "SOFR")
    client = FakeClient(text_response="observation_date,SOFR\n2024-01-01,5.30\n2024-01-02,.\n2024-01-03,5.31\n")

    rows = sources.fetch_series(item, client, "2024-01-02", "2024-01-03")

    assert rows == [{"date": "2024-01-03", "value": 5.31, "published_at": None, "vintage": None}]
    assert "data_mode" not in item
    assert client.calls == [("text", sources.FRED_GRAPH, {"id": "SOFR", "cosd": "2024-01-02", "coed": "2024-01-03"}, None)]


def test_fred_keyed_vintage_uses_official_observations_api_and_never_sets_publication_time():
    item = spec("fred", "GDP", vintage="2024-02-01")
    client = FakeClient(env={"FRED_API_KEY": "test-key"}, json_response={"observations": [
        {"date": "2024-01-01", "value": "100.1", "realtime_start": "2024-02-01"},
    ]})

    rows = sources.fetch_series(item, client, "2024-01-01", "2024-02-01")

    assert rows == [{"date": "2024-01-01", "value": 100.1, "published_at": None, "vintage": "2024-02-01"}]
    assert "data_mode" not in item
    assert client.calls[0][1] == sources.FRED_OBSERVATIONS
    assert client.calls[0][2]["vintage_dates"] == "2024-02-01"
    assert client.calls[0][2]["api_key"] == "test-key"


def test_fred_vintage_without_key_is_explicitly_unavailable():
    with pytest.raises(RuntimeError, match="requires FRED_API_KEY"):
        sources.fetch_series(spec("fred", "GDP", vintage="2024-02-01"), FakeClient(),
                             "2024-01-01", "2024-02-01")


def test_fred_rejects_wrong_series_and_future_vintage():
    with pytest.raises(ValueError, match="requested series"):
        sources.fetch_series(spec("fred", "GDP"), FakeClient(text_response="DATE,OTHER\n2024-01-01,1\n"), "2024-01-01", "2024-02-01")
    with pytest.raises(ValueError, match="vintage"):
        sources.fetch_series(spec("fred", "GDP", vintage="2024-03-01"), FakeClient(), "2024-01-01", "2024-02-01")


def test_alfred_preserves_realtime_versions_and_requires_key():
    item = spec("fred", "GDP", data_mode="point_in_time")
    client = FakeClient(env={"FRED_API_KEY": "test-key"}, json_response={"count": 2, "observations": [
        {"date": "2024-01-01", "value": "100", "realtime_start": "2024-02-01"},
        {"date": "2024-01-01", "value": "101", "realtime_start": "2024-03-01"}]})
    rows = sources.fetch_series(item, client, "2024-01-01", "2024-04-01")
    assert [r["vintage"] for r in rows] == ["2024-02-01", "2024-03-01"]
    assert all(r["published_at"] is None for r in rows)
    assert client.calls[0][2]["realtime_end"] == "2024-04-01"
    with pytest.raises(RuntimeError, match="requires FRED_API_KEY"):
        sources.fetch_series(item, FakeClient(), "2024-01-01", "2024-04-01")


def test_ofr_stfm_uses_documented_tuple_schema_and_drops_nulls():
    client = FakeClient(json_response=[["2024-01-02", 5.31], ["2024-01-03", None]])

    rows = sources.fetch_series(spec("ofr_stfm", "REPO-DVP_AR_G30-P"), client,
                                "2024-01-01", "2024-01-03")

    assert rows == [{"date": "2024-01-02", "value": 5.31, "published_at": None, "vintage": None}]
    assert client.calls[0][1] == sources.OFR_TIMESERIES
    assert client.calls[0][2] == {"mnemonic": "REPO-DVP_AR_G30-P", "start_date": "2024-01-01", "end_date": "2024-01-03"}


def test_cboe_history_parses_selected_csv_column_without_invented_dates():
    client = FakeClient(text_response="DATE,OPEN,HIGH,LOW,CLOSE\n01/02/2024,13,14,12,13.4\n2024-01-03,14,15,13,14.2\n")

    rows = sources.fetch_series(spec("cboe", "VIX"), client, "2024-01-01", "2024-01-03")

    assert rows == [
        {"date": "2024-01-02", "value": 13.4, "published_at": None, "vintage": None},
        {"date": "2024-01-03", "value": 14.2, "published_at": None, "vintage": None},
    ]
    assert client.calls[0][1] == sources.CBOE_HISTORY.format("VIX")


def test_cftc_pre_selects_specified_field_and_keeps_publication_unknown():
    client = FakeClient(json_response=[{
        "report_date_as_yyyy_mm_dd": "2024-01-02T00:00:00.000",
        "lev_money_positions_long_all": "12000",
        "cftc_contract_market_code": "13874A",
        "market_and_exchange_names": "E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE",
    }])
    item = spec("cftc_pre", "tff_futures_only", field="lev_money_positions_long_all",
                params={"market_code": "13874A"})

    rows = sources.fetch_series(item, client, "2024-01-02", "2024-01-02")

    assert rows == [{
        "date": "2024-01-02", "value": 12000.0, "published_at": None, "vintage": None,
        "dimensions": {"contract_market_code": "13874A",
                       "market_and_exchange_name": "E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE"},
    }]
    call = client.calls[0]
    assert call[1].endswith("/gpe5-46if.json")
    assert "report_date_as_yyyy_mm_dd >= '2024-01-02T00:00:00.000'" in call[2]["$where"]
    assert "cftc_contract_market_code = '13874A'" in call[2]["$where"]


def test_nyfed_sofr_reads_percent_rate_from_reference_rates():
    client = FakeClient(json_response={"refRates": [
        {"effectiveDate": "2024-01-02", "percentRate": 5.31},
    ]})

    rows = sources.fetch_series(spec("nyfed_sofr", "SOFR"), client, "2024-01-01", "2024-01-03")

    assert rows == [{"date": "2024-01-02", "value": 5.31, "published_at": None, "vintage": None}]
    assert client.calls[0][1] == sources.NYFED_SOFR
    assert client.calls[0][2] == {"startDate": "2024-01-01", "endDate": "2024-01-03", "type": "rate"}


def test_invalid_or_empty_responses_are_rejected():
    with pytest.raises(ValueError, match="no valid observations"):
        sources.fetch_series(spec("ofr", "X"), FakeClient(json_response=[]), "2024-01-01", "2024-01-02")
    with pytest.raises(ValueError, match="spec.field"):
        sources.fetch_series(spec("cftc", "tff"), FakeClient(json_response=[]), "2024-01-01", "2024-01-02")
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        sources.fetch_series(spec("fred", "SOFR"), FakeClient(), "2024/01/01", "2024-01-02")
