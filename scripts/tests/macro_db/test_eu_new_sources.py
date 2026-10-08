"""歐洲新增三支 fetcher（Comext、INSEE、INE）的離線解析測試：fixture 是截短的真實回應。"""
from __future__ import annotations

from pathlib import Path

import pytest

from macro_db.sources import _http, eu_comext, eu_ine, eu_insee

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "eu"


def fx(name):
    return (FIX / name).read_text(encoding="utf-8")


def test_comext_parse():
    obs = eu_comext.parse_csv(fx("comext_de_us_exp.csv"))
    assert obs[0] == ("2026-04-01", 11394424446.0)
    assert obs[-1] == ("2026-07-01", 15547032272.0) and len(obs) == 4


def test_comext_fetch_builds_key_and_retries(monkeypatch):
    urls, sleeps = [], []
    monkeypatch.setattr(eu_comext.time, "sleep", lambda s: sleeps.append(s))

    def fake_get(url, **kw):
        urls.append(url)
        if len(urls) == 1:
            raise RuntimeError("x：HTTP 429")
        return fx("comext_de_us_exp.csv")

    monkeypatch.setattr(_http, "get", fake_get)
    specs = [{"sid": "eu.a", "params": {"reporter": "DE", "partner": "US", "flow": "2", "product": "TOTAL"}},
             {"sid": "eu.b", "params": {"reporter": "DE", "partner": "US", "flow": "2", "product": "TOTAL"}}]
    res = eu_comext.fetch(specs)
    assert urls[0].endswith("DS-045409/M.DE.US.TOTAL.2.VALUE_IN_EUROS")
    assert res["eu.a"]["obs"][-1][1] == 15547032272.0 and res["eu.b"]["obs"]
    assert eu_comext.BACKOFF[0] in sleeps and eu_comext.GAP in sleeps


def test_comext_non_retryable_error_reported(monkeypatch):
    monkeypatch.setattr(eu_comext.time, "sleep", lambda s: None)
    calls = []

    def fake_get(url, **kw):
        calls.append(url)
        raise RuntimeError("x：HTTP 404")

    monkeypatch.setattr(_http, "get", fake_get)
    res = eu_comext.fetch([{"sid": "eu.a", "params": {"reporter": "DE", "partner": "ZZ", "flow": "1"}}])
    assert "error" in res["eu.a"] and len(calls) == 1


def test_insee_parse_and_fetch(monkeypatch):
    got = eu_insee.parse_xml(fx("insee_bdm.xml"))
    assert got["001565530"][0] == ("1977-01-01", 98.7) and len(got["001565530"]) == 3
    monkeypatch.setattr(_http, "get", lambda url, **kw: fx("insee_bdm.xml"))
    res = eu_insee.fetch([{"sid": "eu.fr_climate", "params": {"idbank": "001565530"}},
                          {"sid": "eu.fr_none", "params": {"idbank": "000000001"}}])
    assert res["eu.fr_climate"]["obs"][-1] == ("1977-03-01", 98.3)
    assert "error" in res["eu.fr_none"]


def test_ine_dates_and_fetch(monkeypatch):
    obs = eu_ine.parse(fx("ine_serie.json"))
    assert obs == [("2026-05-01", 56462.0), ("2026-06-01", 59288.0), ("2026-07-01", 61417.0)]
    seen = {}

    def fake_get(url, **kw):
        seen["url"], seen["params"] = url, kw.get("params")
        return fx("ine_serie.json")

    monkeypatch.setattr(_http, "get", fake_get)
    res = eu_ine.fetch([{"sid": "eu.es_x", "params": {"cod": "ETDP1826"}}])
    assert seen["params"] == {"nult": 2000} and res["eu.es_x"]["obs"][-1][1] == 61417.0
