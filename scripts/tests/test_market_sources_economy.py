#!/usr/bin/env python3
"""2026-09-13：官方總經來源 adapter 的離線 schema／日期／版本測試。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
import market_sources_economy as sources  # noqa: E402


class FakeClient:
    def __init__(self, env=None, get_json=None, post_json=None):
        self.env = env or {}
        self.get_json_payload = get_json
        self.post_json_payload = post_json
        self.get_calls = []
        self.post_calls = []

    def get_env(self, name):
        return self.env.get(name)

    def get_json(self, url, params=None, headers=None):
        self.get_calls.append((url, params, headers))
        if isinstance(self.get_json_payload, list):
            return self.get_json_payload.pop(0)
        return self.get_json_payload

    def post_json(self, url, payload, headers=None):
        self.post_calls.append((url, payload, headers))
        return self.post_json_payload


def _spec(provider, series="SERIES", unit="USD", frequency="monthly", **params):
    return {
        "id": "test." + provider,
        "provider": provider,
        "series": series,
        "unit": unit,
        "frequency": frequency,
        "params": params,
    }


def test_bls_v1_maps_months_and_excludes_annual_average_m13():
    client = FakeClient(
        post_json={
            "status": "REQUEST_SUCCEEDED",
            "Results": {
                "series": [{
                    "seriesID": "SERIES",
                    "data": [
                        {"year": "2024", "period": "M13", "value": "999"},
                        {"year": "2024", "period": "M02", "value": "123.4"},
                        {"year": "2024", "period": "M01", "value": "..."},
                    ],
                }]
            },
        }
    )

    result = sources.fetch_series(_spec("bls"), client, "2024-01-01", "2024-12-31")

    assert result == [{"date": "2024-02-01", "value": 123.4, "published_at": None, "vintage": None}]
    assert client.post_calls[0][0] == sources.BLS_V1_URL
    assert "registrationkey" not in client.post_calls[0][1]


def test_bls_key_selects_v2_without_exposing_key_in_error_or_payload_metadata():
    client = FakeClient(
        env={"BLS_API_KEY": "bls-secret"},
        post_json={"status": "REQUEST_SUCCEEDED", "Results": {"series": []}},
    )

    sources.fetch_series(_spec("bls"), client, "2024-01-01", "2024-12-31")

    assert client.post_calls[0][0] == sources.BLS_V2_URL
    assert client.post_calls[0][1]["registrationkey"] == "bls-secret"


def test_bls_public_requests_are_batched_to_ten_year_windows():
    client = FakeClient(post_json={"status": "REQUEST_SUCCEEDED", "Results": {"series": []}})

    sources.fetch_series(_spec("bls"), client, "2000-01-01", "2024-12-31")

    assert len(client.post_calls) == 3
    assert [(call[1]["startyear"], call[1]["endyear"]) for call in client.post_calls] == [
        ("2000", "2009"), ("2010", "2019"), ("2020", "2024")
    ]


@pytest.mark.parametrize(
    "provider,key",
    [("bea", "BEA_API_KEY"), ("eia", "EIA_API_KEY"), ("sec", "SEC_USER_AGENT")],
)
def test_keyed_sources_fail_cleanly_when_key_is_missing(provider, key):
    client = FakeClient()
    with pytest.raises(sources.EconomySourceError, match=r"requires " + key):
        sources.fetch_series(_spec(provider, series="us-gaap:Revenues", cik="123"), client, "2024-01-01", "2024-12-31")


def test_bea_maps_quarter_to_period_start_and_filters_line():
    # 2026-09-13：季度觀測日＝期間首日（與 FRED GDPC1 同口徑），不再用季底。
    client = FakeClient(
        env={"BEA_API_KEY": "bea-secret"},
        get_json={
            "BEAAPI": {"Results": {"Data": [
                {"LineNumber": "1", "TimePeriod": "2024Q1", "DataValue": "1,234.5", "CL_UNIT": "Millions"},
                {"LineNumber": "2", "TimePeriod": "2024Q1", "DataValue": "999"},
                {"LineNumber": "1", "TimePeriod": "2024Q2", "DataValue": "(D)"},
            ]}}
        },
    )

    result = sources.fetch_series(
        _spec("bea", series="T10101:1", frequency="quarterly", tablename="T10101"),
        client,
        "2024-01-01",
        "2024-06-30",
    )

    assert result[0]["date"] == "2024-01-01"
    assert result[0]["value"] == 1234.5
    assert result[0]["dimensions"]["LineNumber"] == "1"
    assert client.get_calls[0][1]["UserID"] == "bea-secret"
    assert client.get_calls[0][1]["TableName"] == "T10101"


def test_eia_v2_maps_period_and_preserves_finite_values():
    client = FakeClient(
        env={"EIA_API_KEY": "eia-secret"},
        get_json={"response": {"data": [
            {"period": "2024-01", "value": "10.5"},
            {"period": "2024-02-01", "value": "NaN"},
        ]}},
    )

    result = sources.fetch_series(
        _spec("eia", frequency="monthly", route="petroleum/stoc/wstk"),
        client,
        "2024-01-01",
        "2024-02-29",
    )

    assert result == [{"date": "2024-01-01", "value": 10.5, "published_at": None, "vintage": None}]
    assert client.get_calls[0][0].endswith("/petroleum/stoc/wstk/data/")
    assert client.get_calls[0][1]["data[]"] == "value"
    assert client.get_calls[0][1]["api_key"] == "eia-secret"


def test_eia_paginates_and_sends_monthly_bounds_as_year_month():
    client = FakeClient(
        env={"EIA_API_KEY": "eia-secret"},
        get_json=[
            {"response": {"total": 3, "data": [
                {"period": "2024-01", "value": "10"},
                {"period": "2024-02", "value": "11"},
            ]}},
            {"response": {"total": 3, "data": [{"period": "2024-03", "value": "12"}]}},
        ],
    )

    result = sources.fetch_series(
        _spec("eia", frequency="monthly", route="petroleum/stoc/wstk"),
        client,
        "2024-01-01",
        "2024-03-15",
    )

    assert [row["date"] for row in result] == ["2024-01-01", "2024-02-01", "2024-03-01"]
    assert [call[1]["offset"] for call in client.get_calls] == [0, 2]
    assert client.get_calls[0][1]["start"] == "2024-01"
    assert client.get_calls[0][1]["end"] == "2024-03"


def test_sec_uses_filed_date_and_keeps_restatement_versions():
    client = FakeClient(
        env={"SEC_USER_AGENT": "ResearchBot/1.0 (contact@example.test)"},
        get_json={"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
            {"start": "2023-01-01", "end": "2023-12-31", "val": 100, "filed": "2024-02-01", "accn": "0001", "form": "10-K", "fy": 2023},
            {"start": "2023-01-01", "end": "2023-12-31", "val": 120, "filed": "2024-08-01", "accn": "0002", "form": "10-K/A", "fy": 2023},
        ]}}}}},
    )

    result = sources.fetch_series(
        _spec("sec", series="us-gaap:Revenues", frequency="annual", cik="320193"),
        client,
        "2023-01-01",
        "2023-12-31",
    )

    assert [row["value"] for row in result] == [100.0, 120.0]
    assert [row["published_at"] for row in result] == ["2024-02-01", "2024-08-01"]
    assert [row["vintage"] for row in result] == ["0001", "0002"]
    assert client.get_calls[0][0].endswith("CIK0000320193.json")
    assert client.get_calls[0][2]["User-Agent"].startswith("ResearchBot/")


def test_sec_requires_start_for_flow_and_separates_annual_quarter_and_ytd():
    facts = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        {"end": "2023-12-31", "val": 100, "filed": "2024-02-01", "accn": "a", "start": "2023-01-01"},
        {"end": "2023-03-31", "val": 20, "filed": "2023-05-01", "accn": "b", "start": "2023-01-01"},
        {"end": "2023-06-30", "val": 40, "filed": "2023-08-01", "accn": "c", "start": "2023-01-01"},
        {"end": "2023-06-30", "val": 20, "filed": "2023-08-01", "accn": "d", "start": "2023-04-01"},
        {"end": "2023-09-30", "val": 60, "filed": "2023-11-01", "accn": "e"},
    ]}}}}}

    annual = FakeClient(env={"SEC_USER_AGENT": "Bot (contact@example.test)"}, get_json=facts)
    quarterly = FakeClient(env={"SEC_USER_AGENT": "Bot (contact@example.test)"}, get_json=facts)
    ytd = FakeClient(env={"SEC_USER_AGENT": "Bot (contact@example.test)"}, get_json=facts)
    base = dict(cik="123")
    concept = "us-gaap:Revenues"
    assert [row["value"] for row in sources.fetch_series(_spec("sec", series=concept, frequency="annual", **base), annual, "2023-01-01", "2023-12-31")] == [100.0]
    assert [row["value"] for row in sources.fetch_series(_spec("sec", series=concept, frequency="quarterly", **base), quarterly, "2023-01-01", "2023-12-31")] == [20.0, 20.0]
    assert [row["value"] for row in sources.fetch_series(_spec("sec", series=concept, frequency="quarterly", period_kind="ytd", **base), ytd, "2023-01-01", "2023-12-31")] == [20.0, 40.0]


def test_sec_wrong_unit_fails_instead_of_silently_using_another_unit():
    client = FakeClient(
        env={"SEC_USER_AGENT": "Bot (contact@example.test)"},
        get_json={"facts": {"us-gaap": {"Revenues": {"units": {"USD": []}}}}},
    )
    with pytest.raises(sources.EconomySourceError, match="requested unit is unavailable"):
        sources.fetch_series(_spec("sec", cik="123", unit="shares"), client, "2023-01-01", "2023-12-31")


def test_fiscaldata_uses_verified_field_filter_and_total_pages_pagination():
    client = FakeClient(
        get_json=[
            {
                "data": [
                    {"record_date": "2024-01-02", "debt_held_public_amt": "100.25"},
                    {"record_date": "2024-01-01", "debt_held_public_amt": "99"},
                ],
                "meta": {"total-pages": 2, "total-count": 3},
            },
            {
                "data": [{"record_date": "2024-01-03", "debt_held_public_amt": "101"}],
                "meta": {"total-pages": 2, "total-count": 3},
            },
        ]
    )

    result = sources.fetch_series(
        _spec("fiscaldata", series="debt_held_public_amt", frequency="daily", date_field="record_date", page_size=2),
        client,
        "2024-01-01",
        "2024-01-03",
    )

    assert [row["date"] for row in result] == ["2024-01-01", "2024-01-02", "2024-01-03"]
    assert [row["value"] for row in result] == [99.0, 100.25, 101.0]
    assert all(row["published_at"] is None for row in result)
    assert client.get_calls[0][0] == sources.FISCALDATA_URL
    assert client.get_calls[0][1]["filter"] == "record_date:gte:2024-01-01,record_date:lte:2024-01-03"
    assert [call[1]["page[number]"] for call in client.get_calls] == [1, 2]
    assert all("api_key" not in call[1] for call in client.get_calls)


def test_sample_specs_are_independent_and_include_verified_fiscaldata_series():
    specs = sources.sample_specs()
    specs[0]["params"]["changed"] = True
    assert "changed" not in sources.SAMPLE_SPECS[0]["params"]
    assert "fiscaldata" in sources.SUPPORTED_PROVIDERS
    fiscal = next(spec for spec in specs if spec["provider"] == "fiscaldata")
    assert fiscal["series"] == "debt_held_public_amt"
