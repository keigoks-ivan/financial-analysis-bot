"""Unit tests for scripts/etf_dash/long_pe.py — Exhibit 4 長期本益比。No network."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "etf_dash"))

import long_pe as lp  # noqa: E402


def _raw_index(forward, own):
    return {"forward": [{"date": d, "value": v} for d, v in forward],
            "forwardOwn": [{"date": d, "value": v} for d, v in own]}


def test_extract_appends_own_line_after_last_terminal_week_only():
    raw = _raw_index([("2026-07-24", 20.0), ("2026-07-31", 20.5)],
                     [("2026-07-28", 99.0),                       # 終端機還在的期間 → 不用
                      ("2026-08-03", 20.1), ("2026-08-05", 20.2),  # 同一週 → 只留 08-05
                      ("2026-08-12", 19.8)])
    rows = lp.extract_hom_series(raw, None)
    assert [(r["date"], r["pe"], r["src"]) for r in rows] == [
        ("2026-07-24", 20.0, "terminal"), ("2026-07-31", 20.5, "terminal"),
        ("2026-08-05", 20.2, "own"), ("2026-08-12", 19.8, "own")]


def test_extract_sector_uses_series_key():
    raw = {"sectors": {"cons": {"series": [{"date": "2026-09-04", "value": 21.33}], "forwardOwn": []}}}
    rows = lp.extract_hom_series(raw, "cons")
    assert rows == [{"date": "2026-09-04", "pe": 21.33, "src": "terminal"}]


def test_merge_keeps_older_cached_rows_and_prefers_fresh():
    cached = [{"date": "2000-01-07", "pe": 25.0, "src": "terminal"},
              {"date": "2026-08-07", "pe": 18.0, "src": "own"}]
    fresh = [{"date": "2001-01-05", "pe": 22.0, "src": "terminal"},
             {"date": "2026-08-07", "pe": 18.5, "src": "own"}]
    assert lp.merge_rows(cached, fresh) == [cached[0]] + fresh
    assert lp.merge_rows(cached, []) == cached


def test_summarize_median_and_share_of_cheaper_weeks():
    rows = [{"date": f"2026-01-0{i}", "pe": v, "src": "terminal"} for i, v in enumerate([10, 20, 30, 40, 25], 1)]
    s = lp.summarize(rows)
    assert s == {"median": 25.0, "current": 25.0, "pct_below": 40.0}


def test_build_long_pe_unmapped_fund_is_unavailable():
    out = lp.build_long_pe("XLE", {})
    assert out["available"] is False and out["note_zh"]


def test_build_long_pe_proxy_note_and_own_from():
    rows = [{"date": "2026-07-31", "pe": 20.0, "src": "terminal"},
            {"date": "2026-08-07", "pe": 19.0, "src": "own"}]
    out = lp.build_long_pe("SMH", {"sox": rows})
    assert out["available"] and out["series_key"] == "sox"
    assert "費城半導體" in out["proxy_note_zh"]
    assert out["own_note_zh"].startswith("2026-08-07 起")
    assert out["stats"]["current"] == 19.0
    assert out["kind"] == "forward_ntm" and out["period_unit_zh"] == "週"


def test_refresh_hom_fetch_failure_uses_cached_csv(tmp_path, monkeypatch):
    monkeypatch.setattr(lp, "LONG_PE_DIR", tmp_path)
    lp.write_csv("sp500", [{"date": "2026-08-07", "pe": 19.0, "src": "own"}])

    def fail(url):
        raise RuntimeError("down")
    monkeypatch.setattr(lp, "_get_json", fail)
    out = lp.refresh_hom({"sp500"})
    assert out["sp500"] == [{"date": "2026-08-07", "pe": 19.0, "src": "own"}]


def test_build_long_pe_taiex_is_trailing_monthly():
    rows = [{"date": "1999-01-31", "pe": 24.5, "src": "twse"}, {"date": "2026-09-30", "pe": 26.68, "src": "twse"}]
    out = lp.build_long_pe("TAIEX", {"twse": rows})
    assert out["kind"] == "trailing" and out["period_unit_zh"] == "月"
    assert "1999 年起" in out["sub_zh"] and out["own_note_zh"] is None
    assert "前 50 大" in lp.build_long_pe("0050", {"twse": rows})["proxy_note_zh"]  # 0050 用大盤代替並註明


def _fake_twse(monkeypatch, tmp_path, published: dict[str, dict]):
    """published: {YYYYMM: {月底日期: pe}}；沒列的月份當作還沒發布。回傳被請求的月份清單。"""
    monkeypatch.setattr(lp, "LONG_PE_DIR", tmp_path)
    asked = []

    def fake_zip(ym, raw_dir=None, sleep=0):
        asked.append(ym)
        return ym.encode() if ym in published else None
    monkeypatch.setattr(lp, "_twse_zip", fake_zip)
    monkeypatch.setattr(lp, "parse_twse_c02001", lambda blob: published[blob.decode()])
    return asked


def test_refresh_twse_backfills_december_files_then_latest(monkeypatch, tmp_path):
    from datetime import date
    pub = {f"{y}12": {f"{y}-12-31": 10.0 + y - 1999} for y in range(1999, 2026)}
    pub["1999" + "12"]["1998-12-31"] = 99.0  # 1999 以前的年度列要丟掉
    pub["202609"] = {"2026-08-31": 25.0, "2026-09-30": 26.68}
    asked = _fake_twse(monkeypatch, tmp_path, pub)
    rows = lp.refresh_twse(today=date(2026, 10, 19))
    assert asked[0] == "199912" and asked[-1] == "202609"
    assert rows[0]["date"] == "1999-12-31" and rows[-1] == {"date": "2026-09-30", "pe": 26.68, "src": "twse"}
    assert lp.read_csv("twse") == rows


def test_refresh_twse_incremental_skips_when_last_month_present(monkeypatch, tmp_path):
    from datetime import date
    asked = _fake_twse(monkeypatch, tmp_path, {})
    lp.write_csv("twse", [{"date": "2026-09-30", "pe": 26.68, "src": "twse"}])
    lp.refresh_twse(today=date(2026, 10, 19))
    assert asked == []


def test_refresh_twse_new_file_revises_preliminary_month(monkeypatch, tmp_path):
    from datetime import date
    asked = _fake_twse(monkeypatch, tmp_path, {"202610": {"2026-09-30": 26.9, "2026-10-31": 27.5}})
    lp.write_csv("twse", [{"date": "2026-09-30", "pe": 26.68, "src": "twse"}])
    rows = lp.refresh_twse(today=date(2026, 11, 20))
    assert asked == ["202610"]
    assert [(r["date"], r["pe"]) for r in rows] == [("2026-09-30", 26.9), ("2026-10-31", 27.5)]


def test_refresh_twse_unpublished_month_tries_one_earlier_then_stops(monkeypatch, tmp_path):
    from datetime import date
    asked = _fake_twse(monkeypatch, tmp_path, {})
    lp.write_csv("twse", [{"date": "2026-08-31", "pe": 25.0, "src": "twse"}])
    rows = lp.refresh_twse(today=date(2026, 10, 3))
    assert asked == ["202609"]  # 202608 已有，不再往前試
    assert rows == lp.read_csv("twse")


def _jpx_xlsx(old_group="市場第一部　　1ｓｔ　Ｓｅｃｔｉｏｎ", new_group="プライム市場　　Prime Section") -> bytes:
    """仿 JPX longrange-perpbr.xlsx 兩張加權表的版面（標題、市場組、欄名、單位四列後接資料）。"""
    import io
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for sheet, group, data in (("Consolidated(WT AVG)～202203", old_group, [(2022, 2, 2160, 20.1), (2022, 3, 2159, 19.7)]),
                               ("Consolidated(Weighted avg.)", new_group, [(2022, 4, 1821, 19.2), (2022, 5, 1822, "-")])):
        ws = wb.create_sheet(sheet)
        ws.append(["連結総合 （加重）"])
        ws.append([None, None, group, None, None])
        ws.append(["年月末", None, "会社数", "PER", "PBR"])
        ws.append([None, None, None, "倍　times", "倍　times"])
        for y, m, n, pe in data:
            ws.append([y, m, n, pe, 1.2])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_parse_jpx_reads_per_column_and_skips_dash():
    out = lp.parse_jpx_perpbr(_jpx_xlsx())
    assert out == {"2022-02-28": 20.1, "2022-03-31": 19.7, "2022-04-30": 19.2}


def test_parse_jpx_layout_change_raises():
    with pytest.raises(RuntimeError):
        lp.parse_jpx_perpbr(_jpx_xlsx(new_group="スタンダード市場　　Standard Section"))


def test_refresh_jpx_no_network_when_last_month_present(tmp_path, monkeypatch):
    from datetime import date
    monkeypatch.setattr(lp, "LONG_PE_DIR", tmp_path)
    lp.write_csv("jpx", [{"date": "2026-09-30", "pe": 20.6, "src": "jpx"}])

    def boom(*a, **k):
        raise AssertionError("should not hit network")
    monkeypatch.setattr(lp.urllib.request, "urlopen", boom)
    assert lp.refresh_jpx(today=date(2026, 10, 19))[-1]["pe"] == 20.6


def test_refresh_jpx_fetch_failure_falls_back_via_refresh(tmp_path, monkeypatch):
    from datetime import date
    monkeypatch.setattr(lp, "LONG_PE_DIR", tmp_path)
    lp.write_csv("jpx", [{"date": "2026-08-31", "pe": 20.8, "src": "jpx"}])

    def down(*a, **k):
        raise OSError("blocked")
    monkeypatch.setattr(lp.urllib.request, "urlopen", down)
    assert lp.refresh({"jpx"})["jpx"] == [{"date": "2026-08-31", "pe": 20.8, "src": "jpx"}]


def test_build_long_pe_topix_trailing_with_june_and_break_notes():
    rows = [{"date": "2013-01-31", "pe": 23.6, "src": "jpx"}, {"date": "2026-09-30", "pe": 20.6, "src": "jpx"}]
    out = lp.build_long_pe("TOPIX", {"jpx": rows})
    assert out["kind"] == "trailing" and out["period_unit_zh"] == "月"
    assert "6 月" in out["compare_note_zh"] and "2022-04" in out["proxy_note_zh"]
    assert "JPX" in out["source_zh"] and "2013 年起" in out["sub_zh"]
