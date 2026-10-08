"""印尼 fetcher 離線解析測試：SEKI（用假工作表模擬兩種年份標籤位置、項次重複、舊表接續）與 OECD SDMX-CSV。"""
from __future__ import annotations

from pathlib import Path

import pytest

from macro_db.sources import an_id_seki, intl_oecd

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "an" / "id"


class Cell:
    def __init__(self, v):
        self.value = v


class FakeSheet:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid
        self.nrows = len(grid)
        self.ncols = max(len(r) for r in grid)

    def cell_value(self, r, c):
        row = self.grid[r]
        return row[c] if c < len(row) else ""

    def row(self, r):
        return [Cell(self.cell_value(r, c)) for c in range(self.ncols)]


class FakeBook:
    def __init__(self, sheets):
        self._s = sheets

    def sheets(self):
        return self._s


def pad(r, n):
    return r + [""] * (n - len(r))


# 版面 A：年份標籤在該年最後一欄（空白欄為年合計）；項次在最右欄
SHEET_A = FakeSheet("8.1", [
    pad(["", "", "", "", 2025.0, "", "", "", 2026.0], 10),
    pad(["", "", "Nov", "Dec", "", "Jan", "Feb*", "", ""], 10),
    ["Food", "Indeks", 100.0, 101.0, 101.5, 102.0, 103.0, "", 2.0, 2.0][:10],
])
# 版面 B：年份標籤在該年第一欄（像 I.4_3）；項次在最左與最右欄；項次 121 重複
SHEET_B = FakeSheet("I.4_3", [
    pad(["", "", "", 2025.0] + [""] * 12 + [2026.0], 20),
    pad(["", "", ""] + ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "", "Jan", "Feb"], 20),
    pad([121.0, "", "Others", 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, "", 13.0, 14.0, "Others", 121.0], 20),
    pad([121.0, "", "Housing", 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, "", 33.0, 34.0, "Housing", 121.0], 20),
    pad([142.0, "", "Housing", 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, "", 17.0, 18.0, "Housing", 142.0], 20),
])
SHEET_Q = FakeSheet("7.2", [
    pad(["", "", 2024.0, "", "", "", 2025.0], 9),
    pad(["", "", "Q1", "Q2", "Q3", "Q4", "Q1*", "Q2**"], 9),
    pad(["Agri", "", 10.0, 11.0, 12.0, 13.0, 14.0, 15.0], 9),
])


def test_cols_year_label_at_last_column():
    c = an_id_seki._sheet_cols(SHEET_A)
    assert c == {2: "2025-11-01", 3: "2025-12-01", 5: "2026-01-01", 6: "2026-02-01"}


def test_cols_year_label_at_first_column_and_skips_total_column():
    c = an_id_seki._sheet_cols(SHEET_B)
    assert c[3] == "2025-01-01" and c[14] == "2025-12-01" and c[16] == "2026-01-01" and c[17] == "2026-02-01"
    assert 15 not in c


def test_quarter_columns():
    c = an_id_seki._sheet_cols(SHEET_Q)
    assert c == {2: "2024-01-01", 3: "2024-04-01", 4: "2024-07-01", 5: "2024-10-01", 6: "2025-01-01", 7: "2025-04-01"}


def test_read_series_by_item_and_provisional_star():
    s = an_id_seki.read_sheet_series(SHEET_A, 2)
    assert s["2026-02-01"] == 103.0 and s["2025-11-01"] == 100.0 and len(s) == 4


def test_duplicate_item_needs_label():
    with pytest.raises(KeyError):
        an_id_seki.read_sheet_series(SHEET_B, 121)
    s = an_id_seki.read_sheet_series(SHEET_B, 121, "housing")
    assert s["2025-01-01"] == 21.0
    assert an_id_seki.read_sheet_series(SHEET_B, 142)["2026-02-01"] == 18.0


def test_missing_item_raises():
    with pytest.raises(KeyError):
        an_id_seki.read_sheet_series(SHEET_A, 99)


def test_history_splice_new_wins_and_old_fills_before():
    old = FakeSheet("Th 2010-2024", [
        pad(["", "", "", "", 2024.0, "", "", 2025.0], 10),
        pad(["", "", "Nov", "Dec", "", "Jan", "Feb", ""], 10),
        ["Food", "Indeks", 90.0, 91.0, "", 92.0, 93.5, "", 2.0, 2.0],
    ])
    book = FakeBook([old, SHEET_A])
    obs = an_id_seki.read_spec(book, {"item": 2, "history": [{"sheet": "Th 2010-2024", "item": 2}]})
    d = dict(obs)
    assert d["2024-11-01"] == 90.0 and d["2024-12-01"] == 91.0   # 舊表只補新表第一期之前
    assert d["2025-11-01"] == 100.0                                # 新表不被覆蓋
    assert d["2025-01-01"] == 92.0 and d["2025-02-01"] == 93.5   # 舊表日期早於新表第一期（2025-11）才補
    assert [x[0] for x in obs] == sorted(x[0] for x in obs)


def test_scale_and_start():
    book = FakeBook([SHEET_A])
    obs = dict(an_id_seki.read_spec(book, {"item": 2, "scale": 0.5, "start": "2025-12"}))
    assert "2025-11-01" not in obs and obs["2025-12-01"] == 50.5


def test_fetch_downloads_each_table_once(monkeypatch):
    calls = []
    monkeypatch.setattr(an_id_seki._http, "get", lambda url, **kw: calls.append((url, kw)) or b"x")
    import xlrd
    monkeypatch.setattr(xlrd, "open_workbook", lambda file_contents=None, **k: FakeBook([SHEET_A]))
    monkeypatch.setattr(an_id_seki.time, "sleep", lambda s: None)
    specs = [{"sid": "a", "params": {"table": "TABEL8_1", "item": 2}},
             {"sid": "b", "params": {"table": "TABEL8_1", "item": 2, "scale": 2}},
             {"sid": "c", "params": {"table": "TABEL9_9", "item": 2}}]
    res = an_id_seki.fetch(specs)
    assert len(calls) == 2 and calls[0][0].endswith("TABEL8_1.xls")
    assert "ua" not in calls[0][1]                       # 預設 NAMED_UA，不偽裝瀏覽器
    assert res["b"]["obs"][-1][1] == 206.0 and "obs" in res["c"]


def test_fetch_failure_isolated(monkeypatch):
    def boom(url, **kw):
        raise RuntimeError("HTTP 500")
    monkeypatch.setattr(an_id_seki._http, "get", boom)
    res = an_id_seki.fetch([{"sid": "a", "params": {"table": "T", "item": 1}}])
    assert "HTTP 500" in res["a"]["error"]


def test_oecd_parse_and_fetch(monkeypatch):
    text = (FIX / "oecd_kei_cpi_yoy.csv").read_text(encoding="utf-8")
    rows = intl_oecd.parse(text)
    assert len(rows) == 5
    calls = []
    monkeypatch.setattr(intl_oecd._http, "get", lambda url, **kw: calls.append((url, kw)) or text)
    monkeypatch.setattr(intl_oecd.time, "sleep", lambda s: None)
    p = {"dataflow": "OECD.SDD.STES,DSD_KEI@DF_KEI", "key": "IDN.M.CP.GR._Z._Z.GY"}
    res = intl_oecd.fetch([{"sid": "x", "params": p}, {"sid": "y", "params": dict(p, scale=2)}])
    assert len(calls) == 1 and calls[0][1]["headers"]["Accept"] == "application/vnd.sdmx.data+csv"
    assert calls[0][0] == "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_KEI@DF_KEI/IDN.M.CP.GR._Z._Z.GY"
    assert res["x"]["obs"] == [("2026-05-01", 3.08), ("2026-06-01", 3.34), ("2026-07-01", 2.88), ("2026-08-01", 3.19), ("2026-09-01", 3.28)]
    assert res["y"]["obs"][-1][1] == 6.56


def test_oecd_rejects_multiple_series():
    bad = "TIME_PERIOD,OBS_VALUE\n2026-01,1.0\n2026-01,2.0\n"
    with pytest.raises(ValueError):
        intl_oecd.parse(bad)


def test_oecd_skips_missing_values():
    obs = intl_oecd.C.clean_obs(intl_oecd.parse("TIME_PERIOD,OBS_VALUE\n2026-01,\n2026-02,NaN\n2026-03,4.5\n2026-Q2,1\n"))
    assert obs == [("2026-03-01", 4.5), ("2026-04-01", 1.0)]
