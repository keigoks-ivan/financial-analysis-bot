"""馬來西亞 fetcher（an_my_bnm、an_opendosm 的限流與季資料收斂）離線解析測試。"""
from __future__ import annotations

from pathlib import Path

from macro_db.sources import an_my_bnm, an_opendosm

FX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "an" / "my"


def rows(name):
    return an_my_bnm.sheet_rows((FX / name).read_bytes())


def test_parse_ym_skips_year_rows_and_dashes():
    r = an_my_bnm.parse_ym(rows("bnm_ym.xlsx"), 7)
    assert r == [("2025-01-01", 3.45), ("2026-01-01", 3.6)]   # 年度列（B 欄空白）略過，'-' 缺值略過
    assert an_my_bnm.parse_ym(rows("bnm_ym.xlsx"), 8)[-1] == ("2026-01-01", 3.87)


def test_parse_yq_footnote_year():
    r = an_my_bnm.parse_yq(rows("bnm_yq.xlsx"), 2)
    assert r == [("2025-01-01", 900.5), ("2025-04-01", 950.0), ("2026-01-01", 1050.25)]   # '2026 4' 取前四碼；空值略過


def test_parse_daily():
    r = an_my_bnm.parse_daily(rows("bnm_daily.xlsx"), 8)
    assert r == [("2026-06-01", 2.75), ("2026-06-03", 2.76), ("2026-07-01", 2.74)]


def test_discovery_parsing():
    home = (FX / "bnm_home.html").read_text()
    assert an_my_bnm.find_edition(home) == "/-/monthly-highlights-statistics-in-august-2026-1"
    links = an_my_bnm.table_links((FX / "bnm_edition.html").read_text())
    assert links == {"2.5": "https://www.bnm.gov.my/documents/20124/23200938/2.5.xlsx",
                     "3.1.4": "https://www.bnm.gov.my/documents/20124/23200938/3.1.4.xlsx"}


def test_fetch_uses_discovered_url_then_fallback(monkeypatch):
    got = []
    xl = (FX / "bnm_ym.xlsx").read_bytes()

    def fake_get(url, **kw):
        got.append(url)
        if url == an_my_bnm.HOME:
            return (FX / "bnm_home.html").read_text()
        if url.endswith("august-2026-1"):
            return (FX / "bnm_edition.html").read_text()
        if "23200938/2.5.xlsx" in url:
            return xl
        raise RuntimeError("HTTP 404")

    monkeypatch.setattr(an_my_bnm._http, "get", fake_get)
    monkeypatch.setattr(an_my_bnm.time, "sleep", lambda s: None)
    sp = lambda sid, col, url: {"sid": sid, "params": {"table": "2.5", "layout": "ym", "col": col, "url": url}}
    r = an_my_bnm.fetch([sp("a", 7, "https://x/old.xlsx"), sp("b", 8, "https://x/old.xlsx"),
                         {"sid": "c", "params": {"table": "9.9", "layout": "ym", "col": 3, "url": "https://x/none.xlsx"}}])
    assert r["a"]["obs"][-1] == ("2026-01-01", 3.6) and r["b"]["obs"][-1] == ("2026-01-01", 3.87)
    assert "error" in r["c"]
    assert got.count("https://www.bnm.gov.my/documents/20124/23200938/2.5.xlsx") == 1   # 同一張表只下載一次


def test_fetch_falls_back_when_discovery_fails(monkeypatch):
    xl = (FX / "bnm_ym.xlsx").read_bytes()

    def fake_get(url, **kw):
        if url == "https://x/fixed.xlsx":
            return xl
        raise RuntimeError("HTTP 403")

    monkeypatch.setattr(an_my_bnm._http, "get", fake_get)
    monkeypatch.setattr(an_my_bnm.time, "sleep", lambda s: None)
    r = an_my_bnm.fetch([{"sid": "a", "params": {"table": "2.5", "layout": "ym", "col": 7, "url": "https://x/fixed.xlsx"}}])
    assert r["a"]["obs"][0] == ("2025-01-01", 3.45)


def test_dosm_to_quarterly(monkeypatch):
    monkeypatch.setattr(an_opendosm._http, "get", lambda url, **kw: (FX / "dosm_wage.json").read_text())
    monkeypatch.setattr(an_opendosm.time, "sleep", lambda s: None)
    sp = {"sid": "w", "params": {"id": "x", "field": "salary", "filter": "Malaysia@state", "to_quarterly": True}}
    assert an_opendosm.fetch([sp])["w"]["obs"] == [("2025-10-01", 2882.0), ("2026-01-01", 3072.72)]


def test_dosm_retries_429_and_fetches_once(monkeypatch):
    calls = []

    def fake_get(url, **kw):
        calls.append(url)
        if len(calls) == 1:
            raise RuntimeError("u：HTTP 429")
        return (FX / "dosm_wage.json").read_text()

    monkeypatch.setattr(an_opendosm._http, "get", fake_get)
    monkeypatch.setattr(an_opendosm.time, "sleep", lambda s: None)
    sp = lambda sid, f: {"sid": sid, "params": {"id": "x", "field": f, "filter": "Malaysia@state"}}
    r = an_opendosm.fetch([sp("a", "salary"), sp("b", "salary")])
    assert "obs" in r["a"] and "obs" in r["b"]
    assert len(calls) == 2   # 第一次 429、重試一次成功；兩條序列共用同一個網址


def test_dosm_gives_up_on_404(monkeypatch):
    calls = []
    monkeypatch.setattr(an_opendosm._http, "get", lambda url, **kw: calls.append(1) or (_ for _ in ()).throw(RuntimeError("u：HTTP 404")))
    monkeypatch.setattr(an_opendosm.time, "sleep", lambda s: None)
    r = an_opendosm.fetch([{"sid": "a", "params": {"id": "x", "field": "v"}}])
    assert "error" in r["a"] and len(calls) == 1
