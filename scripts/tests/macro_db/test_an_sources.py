"""東南亞（an）與跨國共用 fetcher 解析測試：全部離線，用截短的真實回應當 fixture。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from macro_db.sources import an_opendosm, an_singstat, intl_bis, intl_common, intl_imf, intl_worldbank

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "an"


def fx(name):
    return (FIX / name).read_text(encoding="utf-8")


def test_period_to_date():
    f = intl_common.period_to_date
    assert f("2026-M06") == "2026-06-01" and f("2026-Q2") == "2026-04-01"
    assert f("2026-08") == "2026-08-01" and f("2026-09-29") == "2026-09-29" and f("2025") == "2025-01-01"
    assert f("junk") is None


def test_imf_parse_and_scale(monkeypatch):
    obs = intl_imf.parse(fx("imf_irfcl_sgp.json"))
    assert len(obs) == 4 and obs[0][0].startswith("20")
    monkeypatch.setattr(intl_imf._http, "get", lambda url, **kw: fx("imf_irfcl_sgp.json"))
    spec = {"sid": "x", "params": {"dataflow": "IRFCL", "key": "SGP.X", "scale": 1e-6}}
    res = intl_imf.fetch([spec])["x"]["obs"]
    assert res[-1][0] == "2026-08-01" or res[-1][0].endswith("-01")
    assert abs(res[-1][1] - float(obs[-1][1]) * 1e-6) < 1e-6
    assert "attributes=none" in intl_imf.build_url(spec["params"])


def test_imf_rejects_multi_series():
    bad = json.dumps({"data": {"structures": [{"dimensions": {"observation": [{"values": [{"value": "2026-M01"}]}]}}],
                               "dataSets": [{"series": {"0": {"observations": {}}, "1": {"observations": {}}}}]}})
    with pytest.raises(ValueError):
        intl_imf.parse(bad)


def test_bis_parse_skips_nan(monkeypatch):
    text = fx("bis_cbpol_th.csv")
    rows = intl_bis.parse(text)
    assert rows and rows[0][0].startswith("20")
    nan = text.rstrip("\n") + "\n" + text.splitlines()[1].replace("2026-0", "2030-0").rsplit(",", 5)[0] + ",NaN,A,F,\n"
    monkeypatch.setattr(intl_bis._http, "get", lambda url, **kw: nan)
    out = intl_bis.fetch([{"sid": "y", "params": {"dataflow": "WS_CBPOL", "key": "M.TH"}}])["y"]["obs"]
    assert all(not d.startswith("2030") for d, _ in out)


def test_worldbank(monkeypatch):
    monkeypatch.setattr(intl_worldbank._http, "get", lambda url, **kw: fx("wb_vnm.json"))
    out = intl_worldbank.fetch([{"sid": "z", "params": {"indicator": "NY.GDP.MKTP.KD.ZG", "country": "VNM"}}])["z"]["obs"]
    assert out and out[0][0].endswith("-01-01") and out == sorted(out)


def test_singstat(monkeypatch):
    monkeypatch.setattr(an_singstat._http, "get", lambda url, **kw: fx("singstat_unemp.json"))
    r = an_singstat.fetch([{"sid": "a", "params": {"table_id": "M182341", "row": "Total Unemployment Rate"}},
                           {"sid": "b", "params": {"table_id": "M182341", "row": "不存在的列"}}])
    assert r["a"]["obs"][-1] == ("2026-04-01", 2.3)
    assert "找不到列" in r["b"]["error"]
    assert an_singstat.key_to_date("2026 Aug") == "2026-08-01" and an_singstat.key_to_date("2026 2Q") == "2026-04-01"


def test_dosm_scale_and_filter(monkeypatch):
    seen = []
    monkeypatch.setattr(an_opendosm._http, "get", lambda url, **kw: seen.append(url) or fx("dosm_trade.json"))
    spec = {"sid": "d", "params": {"id": "trade_headline", "field": "exports", "filter": "abs@series", "scale": 1e-6}}
    r = an_opendosm.fetch([spec])["d"]["obs"]
    assert r[-1][0] == "2026-08-01" and abs(r[-1][1] - 191049.044049) < 1e-3
    assert "/data-catalogue/?id=trade_headline" in seen[0] and "filter=abs@series" in seen[0]
