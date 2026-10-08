"""歐洲 fetcher 解析測試：全部離線，用截短的真實檔當 fixture，網路請求一律被攔截。"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from macro_db.sources import _http, eu_common, eu_ecb, eu_eurostat, eu_smard

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "eu"


def fx(name):
    return (FIX / name).read_text(encoding="utf-8")


@pytest.fixture
def net(monkeypatch):
    """路由器：網址片段 -> 文字（或例外）；沒註冊的網址視為失敗。"""
    routes, calls = {}, []

    def fake_get(url, **kw):
        calls.append((url, kw.get("params")))
        for frag, body in routes.items():
            if frag in url:
                if isinstance(body, Exception):
                    raise body
                return body
        raise RuntimeError("測試沒有註冊這個網址：" + url)

    for m in (eu_eurostat, eu_ecb, eu_smard):
        monkeypatch.setattr(m._http, "get", fake_get)
    fake_get.routes, fake_get.calls = routes, calls
    return fake_get


def spec(sid, fetcher_params):
    return {"sid": sid, "params": fetcher_params}


# ---------- 共用工具 ----------

def test_period_to_date():
    p = eu_common.period_to_date
    assert p("2026-Q2") == "2026-04-01" and p("2026Q4") == "2026-10-01"
    assert p("2026-09") == "2026-09-01" and p("2026") == "2026-01-01"
    assert p("2026-10-07") == "2026-10-07"
    # ISO 週 -> 該週星期五：2026-W40 的星期五是 10 月 2 日
    assert p("2026-W40") == "2026-10-02"
    assert dt.date.fromisoformat(p("2026-W40")).weekday() == 4
    assert p("2020-W53") == "2021-01-01"
    with pytest.raises(ValueError):
        p("九月")


def test_plan_requests_merges_small_and_splits_scattered():
    items = [("Q.CLV10_MEUR.SCA.B1GQ.EA21", "a"), ("Q.CLV10_MEUR.SCA.B1GQ.DE", "b"),
             ("Q.CLV10_MEUR.SCA.P3_S13.EA21", "c")]
    plan = eu_common.plan_requests(items)
    assert len(plan) == 1 and plan[0][0] == "Q.CLV10_MEUR.SCA.B1GQ+P3_S13.EA21+DE"
    # 18 個分項 × 6 個地區只要其中 23 條：聯集 108 > 4 倍，必須拆開
    geos = ["EA21", "DE", "FR", "IT", "ES", "NL"]
    big = [("M.I25.CP%02d.EA21" % i, "x%d" % i) for i in range(1, 14)] + [("M.I25.TOTAL.%s" % g, g) for g in geos]
    plan = eu_common.plan_requests(big)
    assert len(plan) > 1
    assert sorted(k for _, ms in plan for k, _ in ms) == sorted(k for k, _ in big)
    for union, members in plan:
        assert len(members) >= 1


def test_plan_requests_single_and_empty():
    assert eu_common.plan_requests([]) == []
    assert eu_common.plan_requests([("A.B", 1)]) == [("A.B", [("A.B", 1)])]


# ---------- Eurostat ----------

def test_eurostat_parse_multi_series_and_missing():
    wanted = {"Q.CLV10_MEUR.SCA.B1GQ.EA21": ["eu.gdp_real"], "Q.CLV10_MEUR.SCA.P3_S13.DE": ["eu.de_gdp_gov"]}
    got = eu_eurostat.parse_csv(fx("estat_gdp.csv"), wanted)
    assert "eu.gdp_real" in got and "eu.de_gdp_gov" in got
    d = dict(got["eu.gdp_real"])
    assert d["2026-04-01"] == 2943716.9 and d["2025-10-01"] == 2925489.0
    assert list(d) == sorted(d)
    # 沒被點名的組合（B1GQ.DE 等）不會混進來
    assert set(got) == {"eu.gdp_real", "eu.de_gdp_gov"}


def test_eurostat_flash_flag_kept_and_blank_skipped():
    txt = fx("estat_hicp.csv") + "ESTAT:PRC_HICP_MINR(1.0),02/10/26 11:00:00,M,I25,TOTAL,EA21,2026-10,,,\n"
    got = eu_eurostat.parse_csv(txt, {"M.I25.TOTAL.EA21": ["eu.hicp"]})
    d = dict(got["eu.hicp"])
    assert d["2026-09-01"] == 104.31      # OBS_FLAG=e 的快報值照收
    assert "2026-10-01" not in d          # 空值略過，不填 0


def test_eurostat_fetch_one_request_per_dataset(net):
    net.routes["namq_10_gdp"] = fx("estat_gdp.csv")
    specs = [spec("eu.gdp_real", {"dataset": "namq_10_gdp", "key": "Q.CLV10_MEUR.SCA.B1GQ.EA21"}),
             spec("eu.de_gdp_gov", {"dataset": "namq_10_gdp", "key": "Q.CLV10_MEUR.SCA.P3_S13.DE"}),
             spec("eu.gdp_nothing", {"dataset": "namq_10_gdp", "key": "Q.CLV10_MEUR.SCA.B1GQ.FR"})]
    res = eu_eurostat.fetch(specs)
    assert len(net.calls) == 1
    assert "B1GQ+P3_S13" in net.calls[0][0] and "EA21+DE+FR" in net.calls[0][0]
    assert res["eu.gdp_real"]["obs"][-1] == ("2026-04-01", 2943716.9)
    assert "error" in res["eu.gdp_nothing"]        # 該序列沒資料：只標這一條失敗


def test_eurostat_failure_isolated_per_dataset(net):
    net.routes["namq_10_gdp"] = fx("estat_gdp.csv")
    net.routes["une_rt_m"] = RuntimeError("HTTP 500")
    res = eu_eurostat.fetch([
        spec("eu.gdp_real", {"dataset": "namq_10_gdp", "key": "Q.CLV10_MEUR.SCA.B1GQ.EA21"}),
        spec("eu.unemp_ea", {"dataset": "une_rt_m", "key": "M.SA.TOTAL.PC_ACT.T.EA21"})])
    assert "obs" in res["eu.gdp_real"] and "HTTP 500" in res["eu.unemp_ea"]["error"]


def test_eurostat_unemployment_monthly():
    got = eu_eurostat.parse_csv(fx("estat_unemp.csv"), {"M.SA.TOTAL.PC_ACT.T.EA21": ["u"]})
    assert got["u"][-1] == ("2026-08-01", 6.4)


# ---------- ECB ----------

def test_ecb_daily_policy_rates_match_by_key():
    wanted = {"FM.D.U2.EUR.4F.KR.DFR.LEV": ["eu.ecb_dfr"], "FM.D.U2.EUR.4F.KR.MRR_FR.LEV": ["eu.ecb_mro"]}
    got = eu_ecb.parse_csv(fx("ecb_fm.csv"), wanted)
    assert got["eu.ecb_dfr"][0] == ("2026-09-14", 2.25)
    assert "eu.ecb_mro" not in got or all(v > 0 for _, v in got["eu.ecb_mro"])


def test_ecb_weekly_iso_week_becomes_friday():
    got = eu_ecb.parse_csv(fx("ecb_ilm.csv"), {"ILM.W.U2.C.T000000.Z5.Z01": ["eu.ecb_assets"]})
    obs = got["eu.ecb_assets"]
    assert obs[-1][0] == "2026-10-02" and obs[-1][1] == 5947826.0
    assert all(dt.date.fromisoformat(d).weekday() == 4 for d, _ in obs)


def test_ecb_monthly_and_quarterly():
    m = eu_ecb.parse_csv(fx("ecb_bsi.csv"), {"BSI.M.U2.Y.V.M30.X.I.U2.2300.Z01.A": ["m3"]})
    assert m["m3"][-1][0] == "2026-08-01"
    q = eu_ecb.parse_csv(fx("ecb_bls.csv"), {"BLS.Q.U2.ALL.O.E.Z.B3.ST.S.WFNET": ["bls"]})
    assert q["bls"][0][0].endswith("-01-01") and all(d[5:7] in ("01", "04", "07", "10") for d, _ in q["bls"])


def test_ecb_fetch_uses_dataset_prefix_in_key(net):
    net.routes["data-api.ecb.europa.eu/service/data/FM/"] = fx("ecb_fm.csv")
    res = eu_ecb.fetch([spec("eu.ecb_dfr", {"dataset": "FM", "key": "D.U2.EUR.4F.KR.DFR.LEV"}),
                        spec("eu.ecb_mro", {"dataset": "FM", "key": "D.U2.EUR.4F.KR.MRR_FR.LEV"})])
    assert len(net.calls) == 1 and "DFR+MRR_FR" in net.calls[0][0]
    assert net.calls[0][1] == {"format": "csvdata", "detail": "dataonly"}
    assert "obs" in res["eu.ecb_dfr"]


def test_ecb_error_on_empty_series(net):
    net.routes["service/data/FM/"] = "KEY,FREQ,TIME_PERIOD,OBS_VALUE\n"
    res = eu_ecb.fetch([spec("eu.x", {"dataset": "FM", "key": "D.A"})])
    assert "error" in res["eu.x"]


# ---------- SMARD ----------

def test_smard_timestamps_are_german_local_midnight():
    # 1767222000000 ＝ 2025-12-31 23:00 UTC ＝ 德國 2026-01-01 00:00（冬令）
    assert eu_smard.ms_to_date(1767222000000) == "2026-01-01"
    # 夏令：2025-07-01 00:00 CEST ＝ 2025-06-30 22:00 UTC
    assert eu_smard.ms_to_date(1751320800000) == "2025-07-01"


def test_smard_fetch_all_years_skips_null(net):
    net.routes["index_day.json"] = fx("smard_index_day.json")
    net.routes["410_DE_day_1735686000000.json"] = fx("smard_day_2025.json")
    net.routes["410_DE_day_1767222000000.json"] = fx("smard_day_2026.json")
    res = eu_smard.fetch([spec("eu.de_power_load", {"filter": 410, "region": "DE", "resolution": "day"})])
    obs = dict(res["eu.de_power_load"]["obs"])
    assert obs["2026-01-01"] == 1170188.55 and obs["2026-01-02"] == 1328457.98
    assert "2026-01-03" not in obs                     # null 尚未結算
    assert "2025-01-01" in obs
    assert list(obs) == sorted(obs)


def test_smard_failure_reports_error(net):
    res = eu_smard.fetch([spec("eu.de_power_load", {"filter": 410, "region": "DE", "resolution": "day"})])
    assert "error" in res["eu.de_power_load"]


def test_named_ua_has_no_email():
    assert "@" not in _http.NAMED_UA
