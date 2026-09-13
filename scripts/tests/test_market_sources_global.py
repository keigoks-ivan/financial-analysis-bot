#!/usr/bin/env python3
"""2026-09-13：全球官方來源 adapter 的離線回應契約測試。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import market_sources_global as sources  # noqa: E402


class Client:
    def __init__(self, text=None, payload=None):
        self.text, self.payload, self.calls = text, payload, []

    def get_text(self, url, params=None, headers=None):
        self.calls.append((url, params, headers))
        return self.text

    def get_json(self, url, params=None, headers=None):
        self.calls.append((url, params, headers))
        return self.payload

    def post_json(self, url, payload, headers=None):
        raise AssertionError("not used")

    def get_env(self, name):
        return None


class HistoryClient(Client):
    def __init__(self, payloads):
        super().__init__()
        self.payloads, self.receipts = payloads, []

    def get_json(self, url, params=None, headers=None):
        self.calls.append((url, params, headers))
        request_date = params["date"]
        self.receipts.append({"raw_hash": "hash-" + request_date})
        return self.payloads[request_date]


def _spec(provider, series, frequency="daily", **extra):
    item = {"id": "test-source", "provider": provider, "series": series,
            "unit": "points", "frequency": frequency}
    item.update(extra)
    return item


def test_ecb_csv_uses_bounded_sdmx_url_and_normalizes_rows():
    client = Client("TIME_PERIOD,OBS_VALUE,CURRENCY\n2026-08-31,1.1,USD\n2026-09-10,1.1723,USD\n2026-09-11,,USD\n")
    rows = sources.fetch_series(_spec("ecb", "EXR/D.USD.EUR.SP00.A"), client, "2026-09-01", "2026-09-12")
    assert rows == [{"date": "2026-09-10", "value": 1.1723, "published_at": None, "vintage": None,
                     "dimensions": {"CURRENCY": "USD"}}]
    assert client.calls[0][0] == sources.ECB_URL + "EXR/D.USD.EUR.SP00.A"
    assert client.calls[0][1]["startPeriod"] == "2026-09-01"


def test_boj_json_request_has_official_month_bounded_parameters():
    payload = {"RESULTSET": [{
        "SERIES_CODE": "TK99F1000601GCQ01000",
        "NAME_OF_TIME_SERIES": "D.I./Business Conditions/Large Enterprises/Manufacturing/Actual result",
        "UNIT": "% points", "FREQUENCY": "QUARTERLY", "CATEGORY": "TANKAN/Judgement Survey",
        "LAST_UPDATE": 20260702,
        "VALUES": {"SURVEY_DATES": [202601, 202602, 202603], "VALUES": [12.5, 13, None]},
    }]}
    client = Client(payload=payload)
    rows = sources.fetch_series(_spec("boj", "TK99F1000601GCQ01000", "quarterly", params={"db": "CO"}),
                                client, "2026-01-01", "2026-06-30")
    assert rows[0]["date"] == "2026-01-01"
    assert rows[0]["value"] == 12.5
    assert len(rows) == 2
    assert client.calls[0][0] == sources.BOJ_URL
    assert client.calls[0][1]["db"] == "CO"
    assert client.calls[0][1]["startDate"] == "202601"
    assert client.calls[0][1]["endDate"] == "202602"


@pytest.mark.parametrize("provider", ["twse", "tpex"])
def test_taiwan_current_only_preserves_roc_date_commas_and_negative_values(provider):
    client = Client(payload=[{"日期": "114/09/12", "名稱": "臺指", "收盤價": "(1,234.50)"}])
    rows = sources.fetch_series(_spec(provider, "daily_quote", params={"row_name": "臺指", "name_field": "名稱", "value_field": "收盤價"}),
                                client, "2020-01-01", "2026-09-13")
    assert rows[0]["date"] == "2025-09-12"
    assert rows[0]["value"] == -1234.5
    assert rows[0]["dimensions"]["data_mode"] == "latest_only"


def test_taifex_keeps_rolling_history_mode_and_filters_the_requested_range():
    client = Client(payload=[{"Date": "20260911", "PutCallOIRatio%": "87.70"},
                             {"Date": "20260801", "PutCallOIRatio%": "99.00"}])
    rows = sources.fetch_series(_spec("taifex", "OptionsPutCallRatio",
                                      params={"value_field": "PutCallOIRatio%"}, data_mode="rolling_history"),
                                client, "2026-09-01", "2026-09-13")
    assert rows[0]["date"] == "2026-09-11"
    assert rows[0]["dimensions"]["data_mode"] == "rolling_history"


def _fmtqik(month, day, index="12,345.67", turnover="987,654,321"):
    return {"stat": "OK", "date": month, "fields": ["日期", "成交金額", "發行量加權股價指數"],
            "data": [[day, turnover, index]]}


def test_twse_fmtqik_fetches_each_month_and_binds_its_own_raw_hash():
    client = HistoryClient({
        "20260101": _fmtqik("20260101", "115/01/05"),
        "20260201": _fmtqik("20260201", "115/02/03", index="12,400.00"),
    })
    spec = _spec("twse", "FMTQIK", params={"field": "發行量加權股價指數"}, data_mode="rolling_history")
    rows = sources.fetch_series(spec, client, "2026-01-01", "2026-02-28")
    assert [row["date"] for row in rows] == ["2026-01-05", "2026-02-03"]
    assert [row["raw_hashes"] for row in rows] == [["hash-20260101"], ["hash-20260201"]]
    assert all(row["dimensions"]["data_mode"] == "rolling_history" for row in rows)


def test_twse_fmtqik_accepts_turnover_field_and_rejects_missing_month_data():
    spec = _spec("twse", "FMTQIK", params={"field": "成交金額"})
    rows = sources.fetch_series(spec, HistoryClient({"20260101": _fmtqik("20260101", "115/01/05")}),
                                "2026-01-01", "2026-01-31")
    assert rows[0]["value"] == 987654321.0
    with pytest.raises(ValueError, match="不能視為完整歷史"):
        sources.fetch_series(spec, HistoryClient({"20260101": {"stat": "OK", "date": "20260101", "fields": [], "data": []}}),
                             "2026-01-01", "2026-01-31")


def test_taiwan_requires_an_actual_public_date_instead_of_backfilling():
    client = Client(payload=[{"名稱": "臺指", "收盤價": "1,234"}])
    with pytest.raises(ValueError, match="沒有可驗證"):
        sources.fetch_series(_spec("twse", "daily_quote", params={"row_name": "臺指", "name_field": "名稱", "value_field": "收盤價"}),
                             client, "2020-01-01", "2026-09-13")


def test_bis_requires_confirmed_flow_and_key_not_a_guessed_label():
    with pytest.raises(ValueError, match="已確認"):
        sources.fetch_series(_spec("bis", "credit-growth"), Client(text=""), "2026-01-01", "2026-09-13")


def test_sdmx_rejects_multiple_dimension_series_in_one_response():
    text = "FREQ,CG_DTYPE,TIME_PERIOD,OBS_VALUE\nQ,A,2026-Q1,1\nQ,C,2026-Q1,2\n"
    with pytest.raises(ValueError, match="多個維度"):
        sources.fetch_series(_spec("bis", "WS_CG/Q.CN.P.A.A"), Client(text=text), "2026-01-01", "2026-09-13")


def test_sdmx_ignores_observation_annotations_when_identifying_the_series():
    text = "KEY,DECIMALS,OBS_COM,TIME_PERIOD,OBS_VALUE\nX.A,1,old,2026-09-10,1\nX.A,2,new,2026-09-11,2\n"
    rows = sources.fetch_series(_spec("ecb", "EXR/D.USD.EUR.SP00.A"), Client(text=text), "2026-09-01", "2026-09-13")
    assert [row["value"] for row in rows] == [1.0, 2.0]


def test_contract_rejects_bad_id_and_reversed_dates():
    with pytest.raises(ValueError, match="來源代碼"):
        sources.fetch_series(_spec("ecb", "EXR/D.USD.EUR.SP00.A", id="Bad id"), Client(text=""), "2026-01-01", "2026-09-13")
    with pytest.raises(ValueError, match="start"):
        sources.fetch_series(_spec("ecb", "EXR/D.USD.EUR.SP00.A"), Client(text=""), "2026-09-13", "2026-01-01")
