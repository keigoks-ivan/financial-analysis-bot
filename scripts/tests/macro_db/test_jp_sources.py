"""日本 fetcher 解析測試：全部離線，用手工縮小的檔案內容當 fixture，網路請求一律被攔截。"""
from __future__ import annotations

import datetime as dt
import io

import pytest

from macro_db.sources import jp_boj, jp_common as C, jp_customs, jp_esri, jp_estat_file, jp_misc, jp_mof, jp_stat


def cp932(text: str) -> bytes:
    return text.encode("cp932")


def make_xlsx(rows, name="Sheet1") -> bytes:
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = name
    for r in rows:
        ws.append(list(r))
    b = io.BytesIO()
    wb.save(b)
    return b.getvalue()


# ---------- 共用 ----------

def test_wareki_dot():
    assert C.wareki_dot("S49.9.24") == (1974, 9, 24)
    assert C.wareki_dot("H31.4.30") == (2019, 4, 30)
    assert C.wareki_dot("R8.9.30") == (2026, 9, 30)
    assert C.wareki_dot("R元.5.1") == (2019, 5, 1)
    assert C.wareki_dot("abc") is None


def test_wareki_year_text_and_month():
    assert C.wareki_year_text("昭和28年") == 1953
    assert C.wareki_year_text("令和元年") == 2019
    assert C.wareki_year_text(1953.0) == 1953
    assert C.wareki_year_text("") is None
    assert C.month_of("１月") == 1 and C.month_of("12月") == 12 and C.month_of("13月") is None


def test_num_skips_missing_never_zero():
    assert C.num("1,234.5") == 1234.5
    assert C.num("－") is None and C.num("***") is None and C.num("") is None
    assert C.num("１２") == 12.0


def test_check_header_detects_layout_change():
    rows = [["", "完全失業率"], ["", ""]]
    C.check_header(rows, 1, [0, 1], "完全失業率", "t")
    with pytest.raises(ValueError, match="改版"):
        C.check_header(rows, 1, [0, 1], "就業者", "t")


def test_find_link_absolute():
    html = '<a href="/a/b/0910ci.xlsx">x</a>'
    assert C.find_link(html, r"\d{4}ci\.xlsx", "https://e.go.jp/jp/stat/di.html") == "https://e.go.jp/a/b/0910ci.xlsx"
    with pytest.raises(ValueError):
        C.find_link(html, r"nomatch", "https://e.go.jp/")


# ---------- BOJ ----------

BOJ_HEAD = "STATUS,200\nMESSAGEID,M181000I\nMESSAGE,ok\nDATE,2026-10-08\nNEXTPOSITION,\n"
BOJ_COLS = "SERIES_CODE,NAME_OF_TIME_SERIES,UNIT,FREQUENCY,CATEGORY,LAST_UPDATE,SURVEY_DATES,VALUES\n"


def test_boj_quarterly_tankan_dates_and_null():
    text = BOJ_HEAD + BOJ_COLS + (
        "TK1,x,DI,QUARTERLY,c,20261001,202601,20\n"
        "TK1,x,DI,QUARTERLY,c,20261001,202602,21\n"
        "TK1,x,DI,QUARTERLY,c,20261001,202603,null\n"
        "TK1,x,DI,QUARTERLY,c,20261001,202604,24\n")
    res, nxt = jp_boj.parse(text)
    assert nxt is None
    assert res["TK1"] == [("2026-01-01", 20.0), ("2026-04-01", 21.0), ("2026-10-01", 24.0)]


def test_boj_daily_monthly_and_bad_status():
    text = BOJ_HEAD + BOJ_COLS + "A,x,%,DAILY,c,1,20260930,0.5\nB,x,%,MONTHLY,c,1,202608,1.5\n"
    res, _ = jp_boj.parse(text)
    assert res["A"] == [("2026-09-30", 0.5)] and res["B"] == [("2026-08-01", 1.5)]
    with pytest.raises(ValueError, match="STATUS=400"):
        jp_boj.parse("STATUS,400\nMESSAGE,bad\n")
    with pytest.raises(ValueError, match="不支援"):
        jp_boj.to_date("ANNUAL", "2026")


def test_boj_fetch_merges_codes_and_scale(monkeypatch):
    calls = []

    def fake_request(db, codes):
        calls.append((db, list(codes)))
        return {"X": [("2026-08-01", 123456.0)], "Y": [("2026-08-01", 2.0)]}
    monkeypatch.setattr(jp_boj, "request", fake_request)
    specs = [{"sid": "a", "params": {"db": "BS01", "code": "X", "scale": 0.0001}},
             {"sid": "b", "params": {"db": "BS01", "code": "Y"}},
             {"sid": "c", "params": {"db": "BS01", "code": "Z"}}]
    res = jp_boj.fetch(specs)
    assert len(calls) == 1 and calls[0][1] == ["X", "Y", "Z"]
    assert res["a"]["obs"] == [("2026-08-01", 12.3456)]
    assert res["b"]["obs"] == [("2026-08-01", 2.0)]
    assert "error" in res["c"]


def test_boj_cpirev_newer_base_wins_and_header_guard():
    import datetime as dt
    hdr = [""] * 5
    hdr[1] = "刈込平均値"
    rows = [[], ["", "刈込平均値", "刈込平均値"], [], [], []]
    rows += [[dt.datetime(2026, 8, 1), 2.1, 9.9], [dt.datetime(2020, 1, 1), None, 0.5]]
    assert jp_boj.cpirev_obs(rows, [1, 2], "刈込平均値") == [("2026-08-01", 2.1), ("2020-01-01", 0.5)]
    with pytest.raises(ValueError, match="改版"):
        jp_boj.cpirev_obs(rows, [1, 2], "加重中央値")


# ---------- MOF ----------

JGB = ("国債金利情報 (令和8年10月),,,,\n基準日,2年,10年,30年\n"
       "S49.9.24,-,7.1,-\nR8.9.30,1.9,3.057,4.1\nR8.10.1,1.939,3.092,4.122\n,,,\n※註記,,,\n")


def test_jgb_wareki_and_missing():
    obs = dict(jp_mof.jgb_obs(cp932(JGB), "10年"))
    assert obs["1974-09-24"] == 7.1 and obs["2026-09-30"] == 3.057 and obs["2026-10-01"] == 3.092
    assert "1974-09-24" not in dict(jp_mof.jgb_obs(cp932(JGB), "2年"))   # "-" 不填 0
    with pytest.raises(ValueError):
        jp_mof.jgb_obs(cp932(JGB), "40年")


def test_jgb_fetch_merges_recent_file(monkeypatch):
    allf = "基準日,10年\nR8.9.30,3.057\n"
    now = "国債金利情報 (令和8年10月),\n基準日,10年\nR8.10.1,3.092\nR8.10.7,3.111\n"
    store = {"u/all": cp932(allf), "u/now": cp932(now)}
    monkeypatch.setattr(C.Cache, "get_url", lambda self, url, **kw: store[url])
    res = jp_mof.fetch([{"sid": "j", "params": {"kind": "jgb", "url": "u/all", "recent_url": "u/now", "tenor": "10年"}}])
    assert dict(res["j"]["obs"]) == {"2026-09-30": 3.057, "2026-10-01": 3.092, "2026-10-07": 3.111}


def test_reserves_scale_and_header_guard():
    rows = [[""] * 6 for _ in range(19)]
    rows[10] = ["", "", "", "", "外貨準備及びその他外貨資産", ""]
    rows += [["令和8年", "1月", "", "", "1,000,000", ""], ["", "2月", "", "", "1,010,000", ""]]
    out = "\n".join(",".join('"%s"' % c for c in r) for r in rows)
    obs = jp_mof.reserves_obs(cp932(out), 4, "外貨準備及びその他外貨資産", "r", 0.01)
    assert obs == [("2026-01-01", 10000.0), ("2026-02-01", 10100.0)]
    with pytest.raises(ValueError, match="改版"):
        jp_mof.reserves_obs(cp932(out), 4, "金", "r")


# ---------- 海關 ----------

CUSTOMS = ("Title\nunit,1000yen\nYears/Months,Exp-Total,Imp-Total\n"
           "2026/07,9000000,8000000\n2026/08,9100000,8200000\n2026/09,0,0\n")


def test_customs_scale_and_trailing_zero_dropped():
    obs = jp_customs.customs_obs(cp932(CUSTOMS), "Exp-Total", 1e-05)
    assert obs == [("2026-07-01", 90.0), ("2026-08-01", 91.0)]
    with pytest.raises(ValueError, match="改版"):
        jp_customs.customs_obs(cp932(CUSTOMS), "Exp-999")


# ---------- CPI ----------

def cpi_csv(base, vals):
    head = ["", "", "", "", "", ""]
    rows = [["類・品目", "総合", "生鮮食品を除く総合"]] + [[""] * 3 for _ in range(5)]
    rows += [[ym, v, v] for ym, v in vals]
    return cp932("\n".join(",".join(map(str, r)) for r in rows))


def test_cpi_yoy_within_file_and_newer_base_priority():
    new = cpi_csv("2025", [("202508", 100.0), ("202608", 102.0)])
    old = cpi_csv("2020", [("202408", 110.0), ("202508", 112.0), ("202608", 999.0), ("202608", 999.0)])
    names, data = jp_stat.parse_index(new)
    assert jp_stat.yoy_in_file(names, data, "総合") == {"2026-08-01": pytest.approx(2.0)}
    assert jp_stat.yoy_in_file(names, data, "存在しない") == {}


def test_cpi_fetch_fails_when_newest_base_missing(monkeypatch):
    old = cpi_csv("2020", [("202408", 110.0), ("202508", 112.2)])

    def fake(url, **kw):
        if "2025" in url:
            raise RuntimeError("404")
        return old
    monkeypatch.setattr(jp_stat, "get", fake)
    res = jp_stat.fetch([{"sid": "c", "params": {"item": "総合", "files": ["x/2025.csv", "x/2020.csv"]}}])
    assert "error" in res["c"]            # 最新基準檔抓不到就整條失敗，不拿舊基準檔充數


# ---------- ESRI ----------

def test_gdp_base_and_obs():
    top = '<a href="data/data_list/sokuhou/files/2026/qe262_2/gdemenuja.html">x</a>'
    base, code = jp_esri.gdp_base(top)
    assert base.endswith("/files/2026/qe262_2/tables/") and code == "2622"
    with pytest.raises(ValueError):
        jp_esri.gdp_base("<html></html>")
    csv_ = ("title,\n,GDP(Expenditure Approach),PrivateConsumption\n"
            "2026/ 1- 3.,0.5,0.2\n 4- 6.,0.4,\n,,\n注,x,y\n")
    assert jp_esri.gdp_obs(cp932(csv_), 1, "GDP(Expenditure Approach)", "g") == [("2026-01-01", 0.5), ("2026-04-01", 0.4)]
    with pytest.raises(ValueError, match="改版"):
        jp_esri.gdp_obs(cp932(csv_), 1, "PrivateConsumption", "g")


def test_ci_obs_with_guard():
    rows = [("", "", "", "先行指数", "一致指数", "遅行指数"), ("", 2026, 7, 117.6, 120.6, 113.0), ("", 2026, 8, 118.0, 118.7, 112.1)]
    assert jp_esri.ci_obs(rows, 3, "先行指数", "ci") == [("2026-07-01", 117.6), ("2026-08-01", 118.0)]
    with pytest.raises(ValueError, match="改版"):
        jp_esri.ci_obs(rows, 3, "一致指数", "ci")


def test_watcher_obs_year_forward_fill():
    rows = [[""] * 6 for _ in range(7)]
    rows[5] = ["", "", "", "", "合計", "家計動向関連"]
    rows += [["", "", "2026年", 8, 46.2, 45.5], ["", "", "", 9, 46.4, 45.9]]
    assert jp_esri.watcher_obs(rows, "合計") == [("2026-08-01", 46.2), ("2026-09-01", 46.4)]
    with pytest.raises(ValueError):
        jp_esri.watcher_obs(rows, "存在しない")


def test_machinery_obs():
    rows = [[""] * 6 for _ in range(4)] + [["", "", "", "受注額合計", "", "外需"], ["", 2026, 8, 100.0, "", 30.0]]
    assert jp_esri.machinery_obs(rows, 5, "外需", "m") == [("2026-08-01", 30.0)]
    with pytest.raises(ValueError, match="改版"):
        jp_esri.machinery_obs(rows, 3, "外需", "m")


# ---------- e-Stat 檔案 ----------

def test_lfs_obs_wareki_year_and_guard():
    rows = [[""] * 6 for _ in range(4)] + [["", "", "", "", "完全失業率", ""]] + [[""] * 6 for _ in range(4)]
    rows += [["令和8年", "7月", "", "", "", 2.4], ["", "8月", "", "", "", 2.5]]
    obs = jp_estat_file.lfs_obs(rows, 5, None)
    assert obs == [("2026-07-01", 2.4), ("2026-08-01", 2.5)]
    rows[4][5] = "完全失業率"
    assert jp_estat_file.lfs_obs(rows, 5, "完全失業率", "u")
    with pytest.raises(ValueError, match="改版"):
        jp_estat_file.lfs_obs(rows, 5, "就業者", "u")


def make_wage_rows(top_title):
    rows = [[""] * 20 for _ in range(14)]
    rows[0][5] = "賃金指数 現金給与総額 ５人以上 就業形態計 調査産業計"
    rows[2][8:20] = [float(i) for i in range(1, 13)]
    rows[3][0] = "指数"
    rows[4][0] = 2025.0
    rows[4][8:10] = [100.0, 100.0]
    rows[8][0] = "前年比"
    rows[9][0] = 2026.0
    rows[9][8:11] = [2.5, "", 3.1]
    return rows


def test_wage_takes_yoy_section_not_index():
    obs = jp_estat_file.wage_obs(make_wage_rows(None), ["賃金指数", "現金給与総額", "５人以上"])
    assert obs == [("2026-01-01", 2.5), ("2026-03-01", 3.1)]          # 指數段的 100.0 不能混進來
    with pytest.raises(ValueError, match="statInfId"):
        jp_estat_file.wage_obs(make_wage_rows(None), ["実質賃金指数"])


def test_iip_obs_by_item_and_yyyymm_header():
    rows = [["品目番号", "品目", "202607", "p 202608"], ["1000000000", "鉱工業", 100.0, 101.5], ["2000000000", "x", 1, 2]]
    assert jp_estat_file.iip_obs(rows, "1000000000") == [("2026-07-01", 100.0), ("2026-08-01", 101.5)]
    with pytest.raises(ValueError):
        jp_estat_file.iip_obs(rows, "9")


# ---------- JNTO / MLIT ----------

def test_jnto_obs_year_sheets():
    rows = [["", *[("%d月" % m) for m in range(1, 13)]], ["総数", 3000000, 2900000, 3100000]]
    obs = jp_misc.jnto_obs({"2026": rows, "メモ": [["x"]]})
    assert obs == [("2026-01-01", 3000000.0), ("2026-02-01", 2900000.0), ("2026-03-01", 3100000.0)]


def test_mlit_link_picks_residential_xlsx():
    html = ('<a href="/a/other.xlsx">商業用</a> 不動産価格指数（商業用）'
            '<a href="/a/resi.xlsx">x</a>').replace('<a href="/a/other.xlsx">商業用</a>', '')
    html = '不動産価格指数（商業用）<a href="/a/com.xlsx">Excel</a><br>不動産価格指数（住宅）<a href="/a/resi.xlsx">Excel</a>'
    assert jp_misc.mlit_link(html).endswith("/a/resi.xlsx")
    with pytest.raises(ValueError):
        jp_misc.mlit_link("<html></html>")


def test_mlit_obs_datetime_rows():
    rows = [[""] * 3 for _ in range(4)] + [["", "住宅総合", ""]] + [[""] * 3 for _ in range(4)]
    rows += [[dt.datetime(2026, 5, 1), 130.5, ""], [dt.datetime(2026, 6, 1), 131.0, ""]]
    assert jp_misc.mlit_obs(rows, 1, "住宅総合", "m") == [("2026-05-01", 130.5), ("2026-06-01", 131.0)]


def test_xlsx_roundtrip_reader():
    raw = make_xlsx([["a", 1], ["b", 2]], "S")
    assert C.sheets_any(raw)["S"][1] == ("b", 2)
