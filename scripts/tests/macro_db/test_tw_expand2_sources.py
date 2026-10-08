"""台灣第二波擴充的新 fetcher 解析測試：tw_cbc fsi_csv_ym、tw_twse 新 kind、tw_taifex。全部離線。"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from macro_db.sources import tw_cbc, tw_taifex, tw_twse
from macro_db.sources import tw_common as C

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "tw"


def fx(name: str) -> bytes:
    return (FIX / name).read_bytes()


@pytest.fixture
def net(monkeypatch):
    routes: dict = {}
    calls: list = []

    def fake_get(url, **kw):
        calls.append(url)
        for frag, body in routes.items():
            if frag in url:
                if isinstance(body, Exception):
                    raise body
                return body
        raise C.FetchError("測試沒有註冊這個網址：" + url)

    monkeypatch.setattr(C, "http_get", fake_get)
    monkeypatch.setattr(C.time, "sleep", lambda s: None)
    monkeypatch.setattr(C, "today_taipei", lambda: date(2026, 10, 8))
    monkeypatch.setattr(tw_twse, "GAP_FAST", 0)
    monkeypatch.setattr(tw_taifex, "GAP", 0)
    monkeypatch.delenv("MACRO_DB_BACKFILL", raising=False)
    fake_get.routes = routes
    fake_get.calls = calls
    return fake_get


def obs_of(res, sid):
    assert "obs" in res[sid], res[sid]
    return dict(res[sid]["obs"])


# ---------- tw_cbc fsi_csv_ym ----------

def test_cbc_fsi_ym_roc_year_month_to_quarter_start(net):
    net.routes["fsi.csv"] = fx("cbc_fsi_bank.csv")
    res = tw_cbc.fetch([{"sid": "npl", "params": {"kind": "fsi_csv_ym", "url": "https://x/fsi.csv", "col": 11}},
                        {"sid": "dash", "params": {"kind": "fsi_csv_ym", "url": "https://x/fsi.csv", "col": 1}}])
    o = obs_of(res, "npl")
    assert o["2002-01-01"] == 8.04          # 9103＝民國 91 年 3 月（不是 1991 年）→ 2002 年第 1 季
    assert o["2002-04-01"] == 7.48
    assert o["2026-01-01"] == 0.15          # 11503 → 2026 Q1
    assert "2026-03-01" not in o
    assert "2002-01-01" not in obs_of(res, "dash")   # 空值「-」略過，不填 0
    assert len(net.calls) == 1               # 同一個檔共用一次下載


# ---------- tw_twse 新 kind ----------

def test_twse_mi_index_ind_picks_price_table_by_name(net):
    net.routes["MI_INDEX?date=20261007"] = fx("twse_mi_index_ind.json")
    net.routes["MI_INDEX"] = json.dumps({"stat": "很抱歉，沒有符合條件的資料!"}).encode()
    specs = [{"sid": "semi", "params": {"kind": "mi_index_ind", "row": "半導體類指數"}},
             {"sid": "ship", "params": {"kind": "mi_index_ind", "row": "航運類指數"}},
             {"sid": "nope", "params": {"kind": "mi_index_ind", "row": "不存在類指數"}}]
    res = tw_twse.fetch(specs)
    assert obs_of(res, "semi") == {"2026-10-07": 1677.95}
    assert obs_of(res, "ship") == {"2026-10-07": 207.93}
    assert "error" in res["nope"] and "不存在類指數" in res["nope"]["error"]
    # 5 個指數共用同一天的請求
    assert len([u for u in net.calls if "MI_INDEX?date=20261007" in u]) == 1


def test_twse_mfi94u_month_page(net):
    net.routes["MFI94U"] = fx("twse_mfi94u.json")
    res = tw_twse.fetch([{"sid": "tri", "params": {"kind": "mfi94u"}}])
    o = obs_of(res, "tri")
    assert o["2026-09-01"] == 108395.72 and len(o) == 5
    assert len(net.calls) == 2              # 上個月＋本月


def test_twse_twtb4u_columns(net):
    net.routes["TWTB4U?date=20261007"] = fx("twse_twtb4u.json")
    net.routes["TWTB4U"] = json.dumps({"stat": "很抱歉，沒有符合條件的資料!"}).encode()
    res = tw_twse.fetch([{"sid": "v", "params": {"kind": "twtb4u", "col": 1}},
                         {"sid": "a", "params": {"kind": "twtb4u", "col": 3}}])
    assert obs_of(res, "v") == {"2026-10-07": 19.78}
    assert obs_of(res, "a") == {"2026-10-07": 40.01}


def test_twse_new_daily_kinds_all_days_fail_is_error(net):
    net.routes["MI_INDEX"] = C.FetchError("HTTP 500")
    res = tw_twse.fetch([{"sid": "x", "params": {"kind": "mi_index_ind", "row": "半導體類指數"}}])
    assert "error" in res["x"]


def test_twse_one_bad_day_does_not_sink_series(net):
    net.routes["MI_INDEX?date=20261006"] = C.FetchError("HTTP 500")
    net.routes["MI_INDEX?date=20261007"] = fx("twse_mi_index_ind.json")
    net.routes["MI_INDEX"] = json.dumps({"stat": "x"}).encode()
    res = tw_twse.fetch([{"sid": "x", "params": {"kind": "mi_index_ind", "row": "半導體類指數"}}])
    assert obs_of(res, "x") == {"2026-10-07": 1677.95}


def test_twse_backfill_goes_back_to_since_and_stops_on_time_budget(net, monkeypatch):
    monkeypatch.setenv("MACRO_DB_BACKFILL", "1")
    monkeypatch.setitem(tw_twse.BACKFILL_SINCE, "twtb4u", "2026-09-28")
    net.routes["TWTB4U?date=20261007"] = fx("twse_twtb4u.json")
    net.routes["TWTB4U"] = json.dumps({"stat": "x"}).encode()
    res = tw_twse.fetch([{"sid": "v", "params": {"kind": "twtb4u", "col": 1}}])
    assert obs_of(res, "v") == {"2026-10-07": 19.78}
    days = {u.split("date=")[1][:8] for u in net.calls}
    assert "20260928" in days and "20260925" not in days     # 回補範圍：起日當天起（平日）
    # 時間用完：未快取的日子不再請求
    tw_twse._T0[:] = [0.0]
    net.calls.clear()
    res = tw_twse.fetch([{"sid": "v", "params": {"kind": "twtb4u", "col": 1}}])
    assert net.calls == [] and "error" in res["v"]
    tw_twse._T0.clear()


def test_twse_backfill_months_for_mfi94u(monkeypatch):
    monkeypatch.setenv("MACRO_DB_BACKFILL", "1")
    ms = tw_twse.mfi94u_months(date(2026, 10, 8))
    assert ms[0] == "20261001" and ms[-1] == "20030101" and len(ms) == 286


# ---------- tw_taifex ----------

def test_taifex_inst_futures_and_pcr(net):
    base = "https://openapi.taifex.com.tw/v1/"
    net.routes["ByTheDate"] = fx("taifex_inst_futures.json")
    net.routes["PutCallRatio"] = fx("taifex_pcr.json")
    specs = [
        {"sid": "fx", "params": {"kind": "inst_futures", "contract": "臺股期貨", "item": "外資及陸資",
                                 "field": "OpenInterest(Net)", "url": base + "Foo/ByTheDate"}},
        {"sid": "pcr", "params": {"kind": "pcr", "field": "PutCallOIRatio%", "url": base + "PutCallRatio"}},
        {"sid": "bad", "params": {"kind": "pcr", "field": "沒有這欄", "url": base + "PutCallRatio"}},
    ]
    res = tw_taifex.fetch(specs)
    assert obs_of(res, "fx") == {"2026-10-07": -79101.0}
    assert obs_of(res, "pcr") == {"2026-10-07": 82.25, "2026-10-06": 95.47, "2026-10-05": 91.95}
    assert "error" in res["bad"]
