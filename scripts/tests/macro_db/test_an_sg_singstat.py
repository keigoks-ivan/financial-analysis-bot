"""an_singstat 分頁、同名列（series_no）與單列查詢的離線測試。"""
from __future__ import annotations

import json

import pytest

from macro_db.sources import an_singstat as S


def row(sn, text, keys, start=0):
    return {"seriesNo": sn, "rowText": text, "columns": [{"key": k, "value": str(i + start)} for i, k in enumerate(keys)]}


def resp(rows):
    return json.dumps({"StatusCode": 200, "Message": "", "Data": {"row": rows}})


Q = ["2025 1Q", "2025 2Q", "2025 3Q", "2025 4Q"]


@pytest.fixture(autouse=True)
def fast(monkeypatch):
    monkeypatch.setattr(S, "PAUSE", 0)
    monkeypatch.setattr(S, "LIMIT", 6)


def install(monkeypatch, pages, seen):
    def get(url, **kw):
        p = kw["params"]
        seen.append(dict(p))
        if "search" in p:
            return resp([r for r in pages["all"] if p["search"].lower() in r["rowText"].lower()])
        if "seriesNoORrowNo" in p:
            return resp([r for r in pages["all"] if r["seriesNo"] == p["seriesNoORrowNo"]])
        return resp(pages[p["offset"]])
    monkeypatch.setattr(S._http, "get", get)


def test_pagination_joins_split_row(monkeypatch):
    # 6 格一頁：A(4) + B 前 2 格；第二頁 B 後 2 格 + C(4)（B 的續段同 seriesNo）
    pages = {0: [row("1", "A", Q), row("2", "B", Q[:2])],
             6: [row("2", "B", Q[2:], 2), row("3", "C", Q)],
             12: []}
    seen = []
    install(monkeypatch, pages, seen)
    r = S.fetch([{"sid": "b", "params": {"table_id": "T", "row": "B"}}, {"sid": "c", "params": {"table_id": "T", "row": "C"}}])
    assert [v for _, v in r["b"]["obs"]] == [0, 1, 2, 3]
    assert r["b"]["obs"][0][0] == "2025-01-01" and r["c"]["obs"][-1] == ("2025-10-01", 3.0)
    assert [p["offset"] for p in seen] == [0, 6, 12]


def test_same_table_fetched_once_and_early_stop(monkeypatch):
    pages = {0: [row("1", "A", Q), row("2", "B", Q[:2])], 6: [row("2", "B", Q[2:], 2), row("3", "C", Q)], 12: []}
    seen = []
    install(monkeypatch, pages, seen)
    r = S.fetch([{"sid": "a", "params": {"table_id": "T", "row": "A"}}, {"sid": "a2", "params": {"table_id": "T", "row": "A", "scale": 2}}])
    assert len(seen) == 1 and r["a2"]["obs"][-1][1] == 6.0


def test_duplicate_name_needs_series_no(monkeypatch):
    pages = {0: [row("1", "Sector", Q[:1]), row("2.1", "Elec", Q[:1]), row("3.1", "Elec", Q[:1], 5)]}
    install(monkeypatch, pages, [])
    r = S.fetch([{"sid": "x", "params": {"table_id": "T", "row": "Elec"}},
                 {"sid": "y", "params": {"table_id": "T", "row": "Elec", "series_no": "3.1"}},
                 {"sid": "z", "params": {"table_id": "T", "row": "Wrong", "series_no": "3.1"}}])
    assert "同名列" in r["x"]["error"] and "series_no" in r["x"]["error"]
    assert r["y"]["obs"] == [("2025-01-01", 5.0)]
    assert "不是" in r["z"]["error"]


def test_deep_row_uses_search(monkeypatch):
    monkeypatch.setattr(S, "FULL_PAGES", 1)
    allrows = [row(str(i), "R%d" % i, Q) for i in range(1, 6)]
    pages = {0: [allrows[0], allrows[1][:1]] if False else [allrows[0], row("2", "R2", Q[:2])], 6: [row("2", "R2", Q[2:], 2), row("3", "R3", Q)], "all": allrows}
    seen = []
    install(monkeypatch, pages, seen)
    r = S.fetch([{"sid": "d", "params": {"table_id": "T", "row": "R4"}}])
    assert len(r["d"]["obs"]) == 4 and any("search" in p for p in seen)


def test_search_term_strips_ampersand():
    assert S._search_term("Housing & Utilities") == "Utilities"
    assert S._search_term("Total") == "Total"
