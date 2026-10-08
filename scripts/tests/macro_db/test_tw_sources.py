"""台灣 fetcher 解析測試：全部離線，用截短的真實檔當 fixture，網路請求一律被攔截。"""
from __future__ import annotations

import io
import json
import zipfile
from datetime import date
from pathlib import Path

import pytest

from macro_db.sources import tw_common as C
from macro_db.sources import (tw_cbc, tw_dgbas, tw_energy, tw_jcic, tw_moea, tw_mof, tw_moi, tw_ndc, tw_tpex,
                              tw_twse)

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "tw"


def fx(name: str) -> bytes:
    return (FIX / name).read_bytes()


@pytest.fixture
def net(monkeypatch):
    """回傳可註冊「網址片段 -> bytes（或例外）」的路由器；沒註冊的網址視為失敗。"""
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
    fake_get.routes = routes
    fake_get.calls = calls
    return fake_get


def obs_of(res, sid):
    assert "obs" in res[sid], res[sid]
    return dict(res[sid]["obs"])


# ---------- 共用工具 ----------

def test_to_float_missing_values():
    assert C.to_float("1,234.5") == 1234.5
    for bad in ("-", "…", "", "  ", "NaN", None, "x"):
        assert C.to_float(bad) is None


def test_period_and_roc_dates():
    assert C.period_to_date("2026M08") == "2026-08-01"
    assert C.period_to_date("2026Q2") == "2026-04-01"
    assert C.period_to_date("202607Ⓟ") == "2026-07-01"
    assert C.period_to_date("20260831") == "2026-08-31"
    assert C.period_to_date("2025") == "2025-01-01"
    assert C.roc_ym_to_date("11507") == "2026-07-01"
    assert C.roc_ym_to_date("08501") == "1996-01-01"
    assert C.roc_label_to_date("115年 8月") == "2026-08-01"
    assert C.roc_label_to_date("90年") is None
    assert C.roc_date_to_iso(" 115/09/01") == "2026-09-01"
    assert C.roc_date_to_iso("1150901") == "2026-09-01"


def test_clean_obs_sorted_dedup_skips_missing():
    out = C.clean_obs([("2026-02-01", "2"), ("2026-01-01", "1"), ("2026-03-01", "-"), ("2026-02-01", "2.5")])
    assert out == [("2026-01-01", 1.0), ("2026-02-01", 2.5)]


# ---------- 主計總處 ----------

def test_dgbas_long_quarter_and_annual_skipped(net):
    net.routes["data.gov.tw/api/v2/rest/dataset/6801"] = json.dumps(
        {"result": {"distribution": [{"resourceDownloadUrl": "https://ws.dgbas.gov.tw/x/NEW/na8102a6q.xml"}]}}).encode()
    net.routes["NEW/na8102a6q.xml"] = fx("dgbas_long_na8102a6q.xml")
    spec = {"sid": "tw.gdp_real", "fetcher": "tw_dgbas", "params": {
        "kind": "long", "dataset": 6801, "file": "na8102a6q", "url": "https://old/na8102a6q.xml",
        "item": "連鎖實質值(2021為參考年_新臺幣百萬元)、8.GDP"}}
    res = tw_dgbas.fetch([spec])
    o = obs_of(res, "tw.gdp_real")
    assert "2026-04-01" in o and "2025-01-01" in o     # 2026Q2、2025Q1
    assert o["2026-04-01"] > 7_000_000                    # 7,066,942 百萬元
    assert all(len(d) == 10 for d in o)
    assert list(o) == sorted(o)
    # 年列（TIME_PERIOD=2025）不得被當成季資料混進來：2025-01-01 只能是 2025Q1 的值
    assert len([d for d in o if d.startswith("2025")]) == 4
    assert not any("old/" in u for u in net.calls)        # 先用 data.gov.tw 解析的新網址


def test_dgbas_long_falls_back_to_hardcoded_url(net):
    net.routes["data.gov.tw"] = C.FetchError("API 掛了")
    net.routes["old/pr0101a1m.xml"] = fx("dgbas_long_pr0101a1m.xml")
    spec = {"sid": "tw.cpi_all", "fetcher": "tw_dgbas", "params": {
        "kind": "long", "dataset": 6019, "file": "pr0101a1m", "url": "https://old/pr0101a1m.xml", "item": "總指數("}}
    res = tw_dgbas.fetch([spec])
    o = obs_of(res, "tw.cpi_all")
    assert "2026-08-01" in o and 90 < o["2026-08-01"] < 130


def test_dgbas_price_list_csv_resolver(net):
    net.routes["dataset/44211"] = json.dumps({"result": {"distribution": [
        {"resourceDownloadUrl": "https://ws.dgbas.gov.tw/list/pricestatisticsxmlurl.csv"}]}}).encode()
    net.routes["pricestatisticsxmlurl.csv"] = (
        "序號,機關代碼,產製機關,統計表,網址連結\n"
        "1,A57,主計總處,CPI,https://ws.dgbas.gov.tw/NEW/pr0101a1m.xml\n").encode("utf-8-sig")
    net.routes["NEW/pr0101a1m.xml"] = fx("dgbas_long_pr0101a1m.xml")
    spec = {"sid": "tw.cpi_all", "fetcher": "tw_dgbas", "params": {
        "kind": "long", "dataset": 44211, "file": "pr0101a1m", "url": "https://old/pr0101a1m.xml", "item": "總指數("}}
    res = tw_dgbas.fetch([spec])
    assert "obs" in res["tw.cpi_all"]
    assert any("NEW/pr0101a1m.xml" in u for u in net.calls)


def test_dgbas_wide_unemployment_and_wages(net):
    net.routes["data.gov.tw"] = C.FetchError("x")
    net.routes["u/mp0101a07.xml"] = fx("dgbas_wide_mp0101a07.xml")
    net.routes["u/mp05002.xml"] = fx("dgbas_wide_mp05002.xml")
    specs = [
        {"sid": "tw.unemp_rate", "params": {"kind": "wide", "dataset": 6637, "file": "mp0101a07", "col": 1, "url": "https://u/mp0101a07.xml"}},
        {"sid": "tw.wage_regular", "params": {"kind": "wide", "dataset": 9663, "file": "mp05002", "col": 1, "url": "https://u/mp05002.xml"}},
    ]
    res = tw_dgbas.fetch(specs)
    u = obs_of(res, "tw.unemp_rate")
    assert "2026-08-01" in u and 2 < u["2026-08-01"] < 6
    assert set(u) == {"2026-06-01", "2026-07-01", "2026-08-01"}   # fixture 內的年列「1978」不得被當成月資料
    w = obs_of(res, "tw.wage_regular")
    assert all(d.endswith("-01") for d in w)    # 全是月資料；年列 '1980' 與 'Ⓟ' 後綴都已處理
    assert "2026-07-01" in w and w["2026-07-01"] > 40000


def test_dgbas_wide_skips_annual_rows():
    recs = [["1978", "1.67"], ["1978M01", "2.01"], ["202607Ⓟ", "5"], ["202606Ⓡ", "4"]]
    out = dict(tw_dgbas.wide_obs(recs, 1))
    assert out == {"1978-01-01": 2.01, "2026-07-01": 5.0, "2026-06-01": 4.0}


# ---------- 央行 ----------

def test_cbc_cpx_monthly_with_col_name_guard(net):
    net.routes["FileName=EF17M01"] = fx("cbc_EF17M01.json")
    d = json.loads(fx("cbc_EF17M01.json"))
    names = tw_cbc.column_names(d)
    good = {"sid": "tw.m1a", "params": {"file": "EF17M01", "col": 25, "col_name": names[24]}}
    bad = {"sid": "tw.m1b", "params": {"file": "EF17M01", "col": 27, "col_name": "不是這一欄"}}
    res = tw_cbc.fetch([good, bad])
    o = obs_of(res, "tw.m1a")
    assert "2026-08-01" in o
    assert "error" in res["tw.m1b"] and "欄位順序已變" in res["tw.m1b"]["error"]


def test_cbc_cpx_skips_dash_and_handles_daily(net):
    net.routes["FileName=BP01D01"] = fx("cbc_BP01D01.json")
    res = tw_cbc.fetch([{"sid": "tw.usdtwd_d", "params": {"file": "BP01D01", "col": 1}}])
    o = obs_of(res, "tw.usdtwd_d")
    assert "2026-09-30" in o and 25 < o["2026-09-30"] < 40


def test_cbc_fsi_csv_roc_year(net):
    net.routes["fsi.csv"] = fx("cbc_fsi_realestate.csv")
    res = tw_cbc.fetch([{"sid": "tw.cbc_fsi_realestate", "params": {"kind": "fsi_csv", "url": "https://x/fsi.csv", "col": 3}}])
    o = obs_of(res, "tw.cbc_fsi_realestate")
    assert o["2025-01-01"] == 34.27 and o["2022-01-01"] == 31.79


# ---------- 國發會 ----------

def _zip_with(member: str, data: bytes) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr(member, data)
    return b.getvalue()


def test_ndc_zip_signal_score_and_light(net):
    net.routes["data.gov.tw/api/v2/rest/dataset/6099"] = json.dumps(
        {"result": {"distribution": [{"resourceDownloadUrl": "https://ws.ndc.gov.tw/Download.ashx?u=GUID2"}]}}).encode()
    net.routes["GUID2"] = _zip_with("景氣指標與燈號.csv", fx("ndc_light.csv"))
    common = {"kind": "zip", "dataset": 6099, "url": "https://ws.ndc.gov.tw/Download.ashx?u=GUID1", "member": "景氣指標與燈號.csv"}
    specs = [
        {"sid": "tw.ndc_signal_score", "params": {**common, "col": "景氣對策信號綜合分數"}},
        {"sid": "tw.ndc_signal_light", "params": {**common, "col": "景氣對策信號",
                                                  "text_map": {"藍": "1", "黃藍": "2", "綠": "3", "黃紅": "4", "紅": "5"}}},
        {"sid": "tw.ndc_lead", "params": {**common, "col": "領先指標綜合指數"}},
    ]
    res = tw_ndc.fetch(specs)
    s = obs_of(res, "tw.ndc_signal_score")
    assert s["2026-08-01"] == 41.0
    assert "1982-03-01" not in s                 # 早期是「-」，略過、不填 0
    assert obs_of(res, "tw.ndc_signal_light")["2026-08-01"] == 5.0
    assert obs_of(res, "tw.ndc_lead")["1982-03-01"] == pytest.approx(12.38128475)
    assert not any("GUID1" in u for u in net.calls)


def test_ndc_pmi_csv_skips_dash(net):
    net.routes["data.gov.tw"] = C.FetchError("x")
    net.routes["GUIDP"] = fx("ndc_pmi.csv")
    base = {"kind": "csv", "dataset": 6100, "url": "https://ws.ndc.gov.tw/Download.ashx?u=GUIDP"}
    res = tw_ndc.fetch([{"sid": "tw.pmi", "params": {**base, "col": "PMI"}}, {"sid": "tw.nmi", "params": {**base, "col": "NMI"}}])
    assert obs_of(res, "tw.pmi")["2012-07-01"] == 47.1
    nmi = obs_of(res, "tw.nmi")
    assert "2012-07-01" not in nmi and nmi["2014-09-01"] == 55.2


# ---------- 財政部 ----------

def test_mof_njswww_skips_annual_row(net):
    net.routes["funid=i8102"] = fx("mof_i8102.csv")
    spec = {"sid": "tw.trade_exp_total", "params": {"kind": "njswww", "url": "https://web02.mof.gov.tw/x?funid=i8102", "col": "按美元計算/ 出口總計"}}
    o = obs_of(tw_mof.fetch([spec]), "tw.trade_exp_total")
    assert set(o) == {"2001-01-01", "2026-07-01", "2026-08-01"}      # 「90年」年合計列不在
    assert o["2026-08-01"] > 50000


def test_mof_u2010_big5(net):
    net.routes["u2010ex.csv"] = fx("mof_u2010ex.csv")
    specs = [{"sid": "tw.exp_c_us", "params": {"kind": "u2010", "url": "https://s/u2010ex.csv", "col": "美國"}},
             {"sid": "tw.exp_c_cn", "params": {"kind": "u2010", "url": "https://s/u2010ex.csv", "col": "中國大陸"}}]
    res = tw_mof.fetch(specs)
    us = obs_of(res, "tw.exp_c_us")
    assert us["2026-08-01"] == 23666999.0 and "2001-01-01" in us
    assert obs_of(res, "tw.exp_c_cn")["2026-07-01"] == 11165220.0


# ---------- 經濟部統計處 / 能源署 ----------

def test_moea_roc_period_and_strip(net):
    net.routes["d.csv"] = fx("moea_d.csv")
    specs = [{"sid": "tw.ip_all", "params": {"file": "d.csv", "where": {"行業代碼": "Z", "統計項目": "生產指數"}, "value": "統計值(指數)"}}]
    o = obs_of(tw_moea.fetch(specs), "tw.ip_all")
    assert o["1996-01-01"] == 29.62                 # 08501 -> 1996-01，行業代碼尾端空白已 strip
    assert "2026-07-01" in o


def test_moea_missing_column_is_error_not_crash(net):
    net.routes["d.csv"] = fx("moea_d.csv")
    specs = [{"sid": "a", "params": {"file": "d.csv", "where": {}, "value": "沒有這欄"}},
             {"sid": "b", "params": {"file": "d.csv", "where": {"行業代碼": "Z"}, "value": "統計值(指數)"}}]
    res = tw_moea.fetch(specs)
    assert "error" in res["a"] and "obs" in res["b"]


def test_energy_monthly_and_annual(net):
    net.routes["set_id=171"] = fx("energy_171.csv")
    net.routes["set_id=69"] = fx("energy_69.csv")
    specs = [{"sid": "tw.gen_total", "params": {"set_id": 171, "col": "全國發電量_總計(數值)"}},
             {"sid": "tw.cap_total", "params": {"set_id": 69, "col": "總發電裝置容量_全國(統計數值)"}}]
    res = tw_energy.fetch(specs)
    g = obs_of(res, "tw.gen_total")
    assert "2007-01-01" in g and "2026-08-01" in g
    c = obs_of(res, "tw.cap_total")
    assert all(d.endswith("-01-01") for d in c) and "2025-01-01" in c


# ---------- 內政部 / 聯徵 ----------

def test_moi_statis_label_match_skips_annual_and_dash(net):
    net.routes["funid=c0510302"] = fx("moi_c0510302.csv")
    url = "https://statis.moi.gov.tw/micst/webMain.aspx?funid=c0510302"
    specs = [{"sid": "tw.moi_bldg_transfer_sale_tw", "params": {"kind": "statis", "url": url, "label": "區域別總計/ 買賣", "col": 1}},
             {"sid": "tw.moi_bldg_transfer_auction_tw", "params": {"kind": "statis", "url": url, "label": "區域別總計/ 拍賣", "col": 1}}]
    res = tw_moi.fetch(specs)
    sale = obs_of(res, "tw.moi_bldg_transfer_sale_tw")
    assert sale == {"1999-01-01": 36437.0, "2026-08-01": 20270.0}     # 「88年/」年度列略過；新北市列不混入
    auc = obs_of(res, "tw.moi_bldg_transfer_auction_tw")
    assert auc == {"2026-08-01": 279.0}                               # 1999-01 為「-」，略過


def test_moi_hpi_text_parse():
    text = fx("moi_hpi.txt").decode("utf-8")
    nat = dict(tw_moi.parse_hpi_text(text, 1))
    tpe = dict(tw_moi.parse_hpi_text(text, 3))
    assert nat["2026-01-01"] == 143.85 and nat["2012-07-01"] == 78.96
    assert tpe["2026-01-01"] == 125.88
    with pytest.raises(ValueError):
        tw_moi.parse_hpi_text(text.replace("臺北市", "台北市"), 1)    # 表頭改版要報錯，不能悄悄抓錯欄


def test_jcic_group_strip(net):
    net.routes["Mortgage_Institution.CSV"] = fx("jcic_Mortgage_Institution.csv")
    base = {"url": "https://j/Mortgage_Institution.CSV", "group": "A全體銀行"}
    specs = [{"sid": "bal", "params": {**base, "value": "授信餘額[仟元]"}}, {"sid": "rate", "params": {**base, "value": "平均利率[%]"}},
             {"sid": "h", "params": {"url": base["url"], "group": "H信用合作社", "value": "授信餘額[仟元]"}}]
    res = tw_jcic.fetch(specs)
    assert obs_of(res, "bal")["2012-01-01"] == 5779582112.0
    assert 1 < obs_of(res, "rate")["2012-01-01"] < 4
    assert obs_of(res, "h")["2012-01-01"] == 115975220.0       # 分類字串尾端有全形空白也要比得上


# ---------- TWSE / TPEx ----------

@pytest.fixture
def market_day(monkeypatch):
    monkeypatch.setattr(C, "today_taipei", lambda: date(2026, 10, 8))
    monkeypatch.setattr(tw_twse, "GAP", 0)
    monkeypatch.setattr(tw_tpex, "GAP", 0)


def test_twse_daily_kinds(net, market_day):
    net.routes["FMTQIK?date=20260901"] = fx("twse_fmtqik.json")
    net.routes["FMTQIK?date=20261001"] = fx("twse_fmtqik.json")
    net.routes["dayDate=20261007"] = fx("twse_bfi82u.json")
    net.routes["dayDate="] = fx("twse_bfi82u_holiday.json")          # 其他日子：查無資料
    net.routes["MI_MARGN?date=20261007"] = fx("twse_margn.json")
    net.routes["MI_MARGN"] = fx("twse_bfi82u_holiday.json")
    specs = [
        {"sid": "tw.mk.taiex_close", "params": {"kind": "fmtqik", "col": 4}},
        {"sid": "tw.mk.twse_turnover", "params": {"kind": "fmtqik", "col": 2}},
        {"sid": "tw.mk.twse_inst_net", "params": {"kind": "bfi82u", "row": "合計", "col": 3}},
        {"sid": "tw.mk.twse_inst_foreign_net", "params": {"kind": "bfi82u", "row": "外資及陸資(不含外資自營商)", "col": 3}},
        {"sid": "tw.mk.twse_margin_balance", "params": {"kind": "margn", "row": "融資金額", "col": 5}},
        {"sid": "tw.mk.twse_short_balance", "params": {"kind": "margn", "row": "融券(", "col": 5}},
    ]
    res = tw_twse.fetch(specs)
    close = obs_of(res, "tw.mk.taiex_close")
    assert close["2026-09-01"] == 46948.72 and close["2026-09-30"] == 47940.13     # 民國 115/09/01 -> 2026-09-01
    assert obs_of(res, "tw.mk.twse_turnover")["2026-09-30"] == 921492702613.0
    assert obs_of(res, "tw.mk.twse_inst_net") == {"2026-10-07": -24163727068.0}
    assert obs_of(res, "tw.mk.twse_inst_foreign_net") == {"2026-10-07": -13043886365.0}
    assert obs_of(res, "tw.mk.twse_margin_balance") == {"2026-10-07": 640000774.0}
    assert obs_of(res, "tw.mk.twse_short_balance") == {"2026-10-07": 215104.0}
    # 同一請求只打一次（融資與融券共用）
    assert len([u for u in net.calls if "MI_MARGN?date=20261007" in u]) == 1


def test_twse_empty_everywhere_is_error(net, market_day):
    net.routes["BFI82U"] = fx("twse_bfi82u_holiday.json")
    res = tw_twse.fetch([{"sid": "x", "params": {"kind": "bfi82u", "row": "合計", "col": 3}}])
    assert "error" in res["x"]


def test_tpex_kinds(net, market_day):
    net.routes["inx?date=2026%2F09%2F01"] = fx("tpex_inx.json")
    net.routes["inx?date=2026%2F10%2F01"] = fx("tpex_inx.json")
    net.routes["tradingIndex"] = fx("tpex_trading.json")
    net.routes["insti/summary?type=Daily&date=2026%2F10%2F07"] = fx("tpex_insti.json")
    net.routes["insti/summary"] = json.dumps({"stat": "ok", "tables": [{"data": []}]}).encode()
    net.routes["margin/balance?date=2026%2F10%2F07"] = fx("tpex_margin.json")
    net.routes["margin/balance"] = json.dumps({"stat": "ok", "tables": [{"data": [], "summary": []}]}).encode()
    specs = [
        {"sid": "tw.mk.tpex_close", "params": {"kind": "inx", "col": 4}},
        {"sid": "tw.mk.tpex_turnover", "params": {"kind": "trading", "col": 2}},
        {"sid": "tw.mk.tpex_inst_net", "params": {"kind": "insti", "row": "三大法人合計", "col": 3}},
        {"sid": "tw.mk.tpex_inst_foreign_net", "params": {"kind": "insti", "row": "外資及陸資合計", "col": 3}},
        {"sid": "tw.mk.tpex_margin_balance", "params": {"kind": "margin", "row": "融資金", "col": 6}},
        {"sid": "tw.mk.tpex_short_balance", "params": {"kind": "margin", "row": "合計(張)", "col": 14}},
    ]
    res = tw_tpex.fetch(specs)
    assert obs_of(res, "tw.mk.tpex_close")["2026-09-30"] == 417.07
    assert obs_of(res, "tw.mk.tpex_turnover")["2026-09-30"] == 232219046.0     # 民國日期、金額仟元
    assert obs_of(res, "tw.mk.tpex_inst_net") == {"2026-10-07": 4282780748.0}
    assert obs_of(res, "tw.mk.tpex_inst_foreign_net") == {"2026-10-07": 9098094285.0}
    assert obs_of(res, "tw.mk.tpex_margin_balance") == {"2026-10-07": 228958200.0}
    assert obs_of(res, "tw.mk.tpex_short_balance") == {"2026-10-07": 40410.0}


# ---------- 重試 ----------

def test_http_get_retries_then_raises(monkeypatch):
    calls = []

    class R:
        status_code = 500
        content = b""

    monkeypatch.setattr(C.requests, "request", lambda *a, **k: (calls.append(1), R())[1])
    monkeypatch.setattr(C.time, "sleep", lambda s: None)
    with pytest.raises(C.FetchError):
        C.http_get("https://example.invalid/x")
    assert len(calls) == 3          # 1 次 + 重試 2 次
