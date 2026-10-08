"""日本第二次擴充的新增解析測試：離線，手工縮小的內容當 fixture。"""
from __future__ import annotations

import datetime as dt

import pytest

from macro_db.sources import jp_boj, jp_esri, jp_estat_file, jp_misc, jp_mof


# ---------- jp_boj：年度頻率、(db, 頻率) 分組、reri ----------

def test_boj_annual_mar_maps_to_april_first():
    assert jp_boj.to_date("ANNUAL(MAR)", "2026") == "2026-04-01"
    assert jp_boj.to_date("ANNUAL(CY)", "2025") == "2025-01-01"
    with pytest.raises(ValueError, match="不支援"):
        jp_boj.to_date("SEMIANNUAL", "2026")


def test_boj_requests_split_by_db_and_freq(monkeypatch):
    calls = []

    def fake_request(db, codes):
        calls.append((db, list(codes)))
        return {c: [("2026-04-01", 1.0)] for c in codes}
    monkeypatch.setattr(jp_boj, "request", fake_request)
    specs = [{"sid": "q", "freq": "Q", "params": {"db": "CO", "code": "Q1"}},
             {"sid": "a", "freq": "A", "params": {"db": "CO", "code": "A1"}},
             {"sid": "q2", "freq": "Q", "params": {"db": "CO", "code": "Q2"}}]
    res = jp_boj.fetch(specs)
    assert sorted(calls) == [("CO", ["A1"]), ("CO", ["Q1", "Q2"])]
    assert all("obs" in v for v in res.values())


def test_reri_obs_checks_header_and_skips_blank():
    rows = [["", ""], ["", "Total exports"], ["", ""], ["", ""], ["", ""], ["", ""],
            [dt.datetime(2026, 7, 1), 120.0], [dt.datetime(2026, 8, 1), None], ["note", 1]]
    assert jp_boj.reri_obs(rows, 1, "Total exports") == [("2026-07-01", 120.0)]
    with pytest.raises(ValueError, match="表頭"):
        jp_boj.reri_obs(rows, 1, "Imports")


# ---------- jp_esri：watcher_sa、ci file ----------

def test_watcher_sa_obs_header_rows_3_4_and_year_col_1():
    rows = [[""] * 5, [""] * 5, [""] * 5,
            ["", "", "", "合計", "家計動向関連"], ["", "", "", "", ""], ["", "", "", "", ""],
            ["", "2026年", 8.0, 46.4, 45.5], ["", "", 9.0, 47.0, 46.8], ["", "", 10.0, "", ""]]
    assert jp_esri.watcher_sa_obs(rows, "合計") == [("2026-08-01", 46.4), ("2026-09-01", 47.0)]
    assert jp_esri.watcher_sa_obs(rows, "家計動向関連")[-1] == ("2026-09-01", 46.8)
    with pytest.raises(ValueError, match="找不到表頭"):
        jp_esri.watcher_sa_obs(rows, "不存在")


def test_fetch_ci_resolves_file_per_param(monkeypatch):
    page = '<a href="x/0809ci.xlsx">a</a><a href="x/0809ci1.xlsx">b</a><a href="x/0809ci2.xlsx">c</a>'
    fetched = []

    def fake_get_url(self, url, **kw):
        fetched.append(url.rsplit("/", 1)[1])
        return b"RAW"
    monkeypatch.setattr(jp_esri, "get", lambda *a, **k: page)
    monkeypatch.setattr(jp_esri.Cache, "get_url", fake_get_url)
    monkeypatch.setattr(jp_esri, "sheets_any", lambda raw: {"s": [["", "", "", "新規求人数"], ["", 2026, 8, 5.0]]})
    specs = [{"sid": "a", "params": {"col": 3, "file": "ci1", "col_check": "新規求人数"}},
             {"sid": "b", "params": {"col": 3, "file": "ci2", "col_check": "新規求人数"}},
             {"sid": "c", "params": {"col": 3, "col_check": "新規求人数"}}]
    res = jp_esri.fetch_ci(specs)
    assert sorted(fetched) == ["0809ci.xlsx", "0809ci1.xlsx", "0809ci2.xlsx"]
    assert all(v["obs"] == [("2026-08-01", 5.0)] for v in res.values())


# ---------- jp_estat_file：wage sheet 參數 ----------

def test_wage_sheet_param(monkeypatch):
    seen = []
    monkeypatch.setattr(jp_estat_file.Cache, "get_url", lambda self, url, **kw: b"RAW")
    monkeypatch.setattr(jp_estat_file, "sheets_any", lambda raw: {"TL": ["TL"], "D": ["D"]})
    monkeypatch.setattr(jp_estat_file, "wage_obs", lambda rows, expect: seen.append(rows) or [("2026-07-01", 1.0)])
    jp_estat_file.fetch_wage([{"sid": "x", "params": {"url": "u", "expect": ["e"], "sheet": "D"}},
                              {"sid": "y", "params": {"url": "u", "expect": ["e"]}}])
    assert seen == [["D"], ["TL"]]


# ---------- jp_misc：mlit anchor／季資料 ----------

def test_mlit_link_anchor_and_quarterly_obs():
    html = ('不動産価格指数（住宅）<a href="/a/resi.xlsx">Excel</a><br>'
            '不動産価格指数（商業用不動産）<a href="/a/cre.xlsx">Excel</a>')
    assert jp_misc.mlit_link_anchor(html, "不動産価格指数（商業用不動産）").endswith("/a/cre.xlsx")
    with pytest.raises(ValueError):
        jp_misc.mlit_link_anchor(html, "不存在")
    rows = [[""] * 3 for _ in range(3)] + [["", "", "総合"]] + [[""] * 3] + [[2025, 3, 146.9], [2025, 4, 146.6], ["注", "", 1]]
    assert jp_misc.mlit_q_obs(rows, 2, "総合", "m") == [("2025-07-01", 146.9), ("2025-10-01", 146.6)]


# ---------- jp_mof：securities／ssc_pct／ssc_level／tax ----------

def test_securities_obs_year_carries_down():
    csv_text = ('2026,１月,Jan,"1","2","3","4","5","6"\n'
                '(令和8年),２月,Feb,"1","2","1,234","4","5","6"\n'
                ',10月,Oct,,,,,,\n')
    assert jp_mof.securities_obs(csv_text.encode("cp932"), 5) == [("2026-01-01", 3.0), ("2026-02-01", 1234.0)]


def test_ssc_pct_level_and_tax_obs():
    pct = [["", "19854~6月", 1.5], ["", "20261~3月", -0.5], ["", "memo", 9]]
    assert jp_mof.ssc_pct_obs(pct, 2) == [("1985-04-01", 1.5), ("2026-01-01", -0.5)]
    lvl = [["平成21年4-6月", 100.0], ["令和8年4-6月", 200.0], ["x", 1]]
    assert jp_mof.ssc_level_obs(lvl, 1) == [("2009-04-01", 100.0), ("2026-04-01", 200.0)]
    tax = [["", "", 7.0, 2025.0, 842226.0], ["", "", "", "", ""]]
    assert jp_mof.tax_obs(tax, 4) == [("2025-04-01", 842226.0)]
