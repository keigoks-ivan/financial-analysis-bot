"""中國區 fetcher 離線解析測試（fixture 為截短後的真實回應）。"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from macro_db.sources import cn_chinabond, cn_chinamoney, cn_common, cn_csindex, cn_nbs, cn_nbs_pmi, cn_pbc

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "cn"


def jload(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def tload(name):
    return (FIX / name).read_text(encoding="utf-8")


# ---------- 國統局 ----------
def test_nbs_code_to_date():
    assert cn_nbs.code_to_date("202608MM") == "2026-08-01"
    assert cn_nbs.code_to_date("202602SS") == "2026-04-01"   # 第 2 季＝4 月 1 日
    assert cn_nbs.code_to_date("202604SS") == "2026-10-01"
    assert cn_nbs.code_to_date("2025SS") == "2025-01-01"
    assert cn_nbs.code_to_date("garbage") is None


def test_nbs_match_indicator_ignores_whitespace_and_requires_unique():
    lst = jload("nbs_indicators.json")["data"]["list"]
    assert cn_nbs.match_indicator(lst, "居民消费价格指数 (上年同月=100)").startswith("53180")
    assert cn_nbs.match_indicator(lst, "居民消费价格指数(上年同月=100)").startswith("53180")   # 空白不拘
    assert cn_nbs.match_indicator(lst, "不存在") is None
    assert cn_nbs.match_indicator(lst + lst, "衣着类居民消费价格指数 (上年同月=100)") is None   # 重名不猜


def test_nbs_parse_rows_skips_empty_values():
    j = jload("nbs_esdata.json")
    ids = {"cpi": "53180dfb9c14411ba4b762307c85920c"}
    out = cn_nbs.parse_rows(j["data"], ids)
    assert out["53180dfb9c14411ba4b762307c85920c"] == [("2026-08-01", 100.8), ("2026-01-01", 100.2), ("2026-04-01", 104.3)]


def test_nbs_merge_parts_prefers_first():
    a = [("2026-01-01", 100.2)]
    b = [("2026-01-01", 99.0), ("2025-12-01", 100.8)]
    assert cn_nbs.merge_parts([a, b]) == [("2025-12-01", 100.8), ("2026-01-01", 100.2)]


class FakeNBS:
    """依網址回固定 JSON；records 之後的請求計次，用來驗證批次（同 cid 只 POST 一次）。"""
    def __init__(self, blocked=False):
        self.calls = []
        self.blocked = blocked

    def http_json(self, s, method, url, **kw):
        self.calls.append((method, url.split("/external/")[-1][:40]))
        if self.blocked:
            raise cn_common.Blocked("挑戰頁")
        if "queryIndexTreeAsync" in url:
            return {"data": [{"_id": "ROOT"}]}
        if "queryIndicatorsByCid" in url:
            return jload("nbs_indicators.json")
        if "esData" in url:
            return jload("nbs_esdata.json")
        raise AssertionError(url)


def specs_nbs():
    cid = "5c7452825c7c4dcba391db5ca7f335c5"
    return [
        {"sid": "t.cpi", "params": {"cid": cid, "name": "居民消费价格指数 (上年同月=100)"}},
        {"sid": "t.food", "params": {"cid": cid, "name": "食品烟酒及在外餐饮类居民消费价格指数(上年同月=100)", "scale": 2}},
        {"sid": "t.bad", "params": {"cid": cid, "name": "沒有這個指標"}},
    ]


def test_nbs_fetch_batches_and_reports_missing_name(monkeypatch):
    fake = FakeNBS()
    monkeypatch.setattr(cn_nbs.C, "http_json", fake.http_json)
    monkeypatch.setattr(cn_nbs.C, "session", lambda *a, **k: object())
    res = cn_nbs.fetch(specs_nbs())
    assert res["t.cpi"]["obs"][0] == ("2026-01-01", 100.2)
    assert res["t.food"]["obs"][-1][0] == "2026-08-01" and res["t.food"]["obs"][-1][1] == 99.3 * 2
    assert "找不到名稱" in res["t.bad"]["error"]
    assert [c for c in fake.calls if c[0] == "POST"].__len__() == 1       # 同一 cid 只 POST 一次
    assert [c for c in fake.calls if "queryIndicatorsByCid" in c[1]].__len__() == 1


def test_nbs_fetch_splices_parts(monkeypatch):
    fake = FakeNBS()

    def hj(s, method, url, **kw):
        if "esData" in url and kw["json"]["cid"].startswith("809d2"):
            return jload("nbs_esdata_old.json")
        if "queryIndicatorsByCid" in url and "cid=809d2" in url:
            return {"data": {"list": [{"_id": "4ae90aaaaaaaaaaaaaaaaaaaaaaaaaaa", "i_showname": "居民消费价格指数 (上年同月=100) "}]}}
        return fake.http_json(s, method, url, **kw)

    monkeypatch.setattr(cn_nbs.C, "http_json", hj)
    monkeypatch.setattr(cn_nbs.C, "session", lambda *a, **k: object())
    sp = [{"sid": "t.cpi", "params": {"parts": [
        {"cid": "5c7452825c7c4dcba391db5ca7f335c5", "name": "居民消费价格指数 (上年同月=100)"},
        {"cid": "809d2522b0fe4be89142650341b19083", "name": "居民消费价格指数 (上年同月=100)"}]}}]
    obs = cn_nbs.fetch(sp)["t.cpi"]["obs"]
    d = dict(obs)
    assert [k for k, _ in obs] == sorted(d)
    assert d["2021-01-01"] == 99.7 and d["2025-12-01"] == 100.8 and d["2026-01-01"] == 100.2 and d["2026-08-01"] == 100.8


def test_nbs_blocked_marks_whole_batch_error_without_retry(monkeypatch):
    fake = FakeNBS(blocked=True)
    monkeypatch.setattr(cn_nbs.C, "http_json", fake.http_json)
    monkeypatch.setattr(cn_nbs.C, "session", lambda *a, **k: object())
    res = cn_nbs.fetch(specs_nbs())
    assert all("error" in v and "擋" in v["error"] for v in res.values())
    assert len(fake.calls) == 1        # 第一次被擋就停，不再打其他請求


def test_nbs_overlay_only_appends_newer_months():
    obs = [("2026-06-01", 1.0), ("2026-07-01", 2.0)]

    class Fake:
        @staticmethod
        def latest(cfg, s, cache):
            return [("2026-06-01", 99.0), ("2026-07-01", 99.0), ("2026-08-01", 3.0)]

    import sys
    mod = sys.modules["macro_db.sources.cn_nbs_pmi"]
    orig = mod.latest
    mod.latest = Fake.latest
    try:
        got = cn_nbs.overlay(obs, {"nbs_pmi": {"sheet": "制造业", "col": "PMI"}}, None, {})
    finally:
        mod.latest = orig
    assert got == [("2026-06-01", 1.0), ("2026-07-01", 2.0), ("2026-08-01", 3.0)]   # 平台值不被覆蓋


# ---------- 統計局 PMI 新聞稿 ----------
def test_pmi_release_discovery_and_sheet():
    assert cn_nbs_pmi.find_release(tload("nbs_zxfb.html")) == "./202609/t20260930_1965449.html"
    assert cn_nbs_pmi.find_xls(tload("nbs_pmi_page.html")) == "./P020260930312638229472.xls"
    rows = [["中国制造业采购经理指数各指标情况（经季节调整）"], ["单位（%）"], [None, "PMI", "生产", "生产经营\n活动预期"],
            [46235.0, 49.8, 50.4, 53.8], [46266.0, 50.1, 51.7, 53.8]]
    assert cn_nbs_pmi.parse_sheet(rows, "PMI") == [("2026-08-01", 49.8), ("2026-09-01", 50.1)]
    assert cn_nbs_pmi.parse_sheet(rows, "生产经营活动预期")[-1] == ("2026-09-01", 53.8)
    with pytest.raises(ValueError):
        cn_nbs_pmi.parse_sheet(rows, "不存在")


# ---------- 人行 ----------
def test_pbc_parse_index_and_section():
    idx = cn_pbc.parse_index(tload("pbc_index.html"))
    assert sorted(idx) == [2025, 2026]
    assert idx[2026]["货币统计概览"].endswith("/2026ntjsj/hbtjgl/index.html") and idx[2026]["货币统计概览"].startswith("https://www.pbc.gov.cn/")
    assert idx[2025]["社会融资规模"].endswith("/5570903/5570885/index.html")
    sec = cn_pbc.parse_section(tload("pbc_section.html"))
    first = [l for t, l in sec if t.startswith("官方储备资产")][0]
    assert first == ["https://www.pbc.gov.cn/diaochatongjisi/attachDir/2026/10/a.xlsx"]
    assert [l for t, l in sec if t.startswith("货币供应量")][0][0].endswith("m.xls")
    assert [l for t, l in sec if t.startswith("地区")][0] == []


def test_pbc_month_of_handles_ambiguous_decimals():
    assert cn_pbc.month_of(2026.01) == "2026-01-01"
    assert cn_pbc.month_of("2026.10") == "2026-10-01"
    assert cn_pbc.month_of(2026.1, 1) == "2026-01-01"       # 2026.1 在第 1 個月份格＝1 月
    assert cn_pbc.month_of(2026.1, 10) == "2026-10-01"      # 在第 10 個月份格＝10 月
    assert cn_pbc.month_of("abc") is None and cn_pbc.month_of(None) is None


def test_pbc_parse_horiz_pairs_and_ordinal_months():
    hdr = ["项目 Item"] + [v for m in range(1, 7) for v in (2026 + m / 100, None)]
    usd = ["1.\xa0\xa0外汇储备\xa0\nForeign currency reserves"] + [x for m in range(6) for x in ("3%d.5\xa0" % m, "2000.1")]
    rows = [["官方储备资产"], hdr, [None, "亿美元", "亿SDR"], usd, ["2.\xa0\xa0基金组织储备头寸", "1.0"]]
    out = cn_pbc.parse_horiz(rows, "外汇储备")
    assert out[0] == ("2026-01-01", 30.5) and out[-1] == ("2026-06-01", 35.5) and len(out) == 6
    with pytest.raises(ValueError):
        cn_pbc.parse_horiz(rows, "不存在")


def test_pbc_parse_vert_by_column_name():
    rows = [["社会融资规模增量统计表"], ["项目\n月份 Month", None, "其中"], [None, "社会融资规模增量", "人民币贷款"],
            [None, "AFRE(flow)", "RMB loans"],
            ["2026.01", 72185.0, 49016.0], [2026.02, 23837.0, 8458.0], [2026.1, 10.0, 5.0], [None, None, None]]
    assert cn_pbc.parse_vert(rows, "人民币贷款") == [("2026-01-01", 49016.0), ("2026-02-01", 8458.0), ("2026-03-01", 5.0)]   # 2026.1 是第 3 列＝3 月
    assert cn_pbc.parse_vert(rows, "社会融资规模增量")[1] == ("2026-02-01", 23837.0)


def test_pbc_read_rows_xlsx(tmp_path):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["货币供应量"])
    ws.append(["项目", 2026.01, 2026.02, 2026.03, 2026.04, 2026.05, 2026.06])
    ws.append(["货币和准货币（M2）", 100.0, 101.0, 102.0, 103.0, 104.0, "105.5\xa0"])
    p = tmp_path / "m.xlsx"
    wb.save(p)
    rows = cn_pbc.read_rows(p.read_bytes(), "https://x/m.xlsx")
    out = cn_pbc.parse_horiz(rows, "^货币和准货币")
    assert out[0] == ("2026-01-01", 100.0) and out[-1] == ("2026-06-01", 105.5)


# ---------- 外匯交易中心 ----------
def test_chinamoney_parsers():
    assert cn_chinamoney.parse_lpr(jload("chinamoney_lpr.json"), "1Y") == [("2026-09-01", 3.0), ("2026-08-01", 3.0)]   # 2019-08-01 舊制不收
    assert cn_chinamoney.parse_lpr(jload("chinamoney_lpr.json"), "5Y") == [("2026-09-01", 3.5), ("2026-08-01", 3.5)]
    assert cn_chinamoney.parse_shibor(jload("chinamoney_shibor.json"), "ON") == [("2026-10-08", 1.3756), ("2026-09-30", 1.362)]
    assert cn_chinamoney.parse_shibor(jload("chinamoney_shibor.json"), "3M") == [("2026-10-08", 1.43)]        # 空值略過
    assert cn_chinamoney.parse_ccpr(jload("chinamoney_ccpr.json")) == [("2026-10-08", 6.7367), ("2026-09-30", 6.7351)]


def test_chinamoney_windows_cover_range_in_year_slices():
    w = cn_chinamoney.windows("2019-08-20", dt.date(2026, 10, 8))
    assert w[0][1] == "2026-10-08" and w[-1][0] == "2019-08-20"
    for a, b in w:
        assert (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days <= 359
    for (a1, _), (_, b2) in zip(w, w[1:]):
        assert dt.date.fromisoformat(a1) - dt.date.fromisoformat(b2) == dt.timedelta(days=1)   # 相鄰切片剛好銜接


def test_chinamoney_fetch_shares_one_shibor_query(monkeypatch):
    urls = []

    def hj(s, method, url, **kw):
        urls.append(url)
        return jload("chinamoney_shibor.json")

    monkeypatch.setattr(cn_chinamoney.C, "http_json", hj)
    monkeypatch.setattr(cn_chinamoney.C, "session", lambda *a, **k: object())
    monkeypatch.setattr(cn_chinamoney.C, "need_backfill", lambda sid, y: False)
    sp = [{"sid": "t.on", "params": {"kind": "shibor", "tenor": "ON"}}, {"sid": "t.3m", "params": {"kind": "shibor", "tenor": "3M"}}]
    res = cn_chinamoney.fetch(sp)
    assert res["t.on"]["obs"][-1] == ("2026-10-08", 1.3756) and res["t.3m"]["obs"] == [("2026-10-08", 1.43)]
    assert len(urls) == len(set(urls)) and len(urls) <= 2    # ON 與 3M 共用同一批請求


# ---------- 中債、中證 ----------
def test_chinabond_snapshot():
    assert cn_chinabond.parse(jload("chinabond.json"), 10.0) == ("2026-09-30", 1.6822)
    assert cn_chinabond.parse(jload("chinabond.json"), 1.0)[1] == 1.2197
    with pytest.raises(ValueError):
        cn_chinabond.parse(jload("chinabond.json"), 7.0)
    with pytest.raises(ValueError):
        cn_chinabond.parse([{"ycDefName": "别的曲线", "seriesData": []}], 10.0)


def test_csindex_parse():
    assert cn_csindex.parse(jload("csindex.json")) == [("2026-09-30", 4357.62), ("2026-09-29", 4350.1)]


# ---------- 共用 ----------
def test_common_clean_and_backfill(tmp_path):
    assert cn_common.clean(" 外汇 储备 \n") == "外汇储备"
    assert cn_common.need_backfill("cn.nothing", 2016, data_dir=tmp_path) is True
    d = tmp_path / "series"
    d.mkdir()
    (d / "cn.x.csv").write_text("date,value\n2016-01-01,1\n2026-01-01,2\n")
    assert cn_common.need_backfill("cn.x", 2016, data_dir=tmp_path) is False
    (d / "cn.y.csv").write_text("date,value\n2024-01-01,1\n")
    assert cn_common.need_backfill("cn.y", 2016, data_dir=tmp_path) is True


def test_http_json_raises_blocked_on_html(monkeypatch):
    class R:
        status_code = 200
        text = "<html>challenge</html>"

        def json(self):
            raise ValueError("no json")

    monkeypatch.setattr(cn_common, "http", lambda *a, **k: R())
    with pytest.raises(cn_common.Blocked):
        cn_common.http_json(None, "GET", "https://example.com/x")
