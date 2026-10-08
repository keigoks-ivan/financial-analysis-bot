"""an_vn_nso 離線解析測試（fixture 是仿 NSO 附表版面的小檔）。"""
from __future__ import annotations

from pathlib import Path

from macro_db.sources import an_vn_nso as N

FX = Path(__file__).resolve().parents[1] / "fixtures" / "macro_db" / "an" / "vn"


def grids(name):
    return N.load_grids((FX / name).read_bytes(), name)


def ext(g, table, ym, rows):
    return N.extract(g, table, ym, {r: True for r in rows})


def test_report_period_new_layout():
    assert N.report_ym(grids("nso_monthly_aug2026.xlsx"), "x/02-Tables-Aug-2026-EN.xlsx") == (2026, 8)


def test_cpi_and_core():
    g = grids("nso_monthly_aug2026.xlsx")
    r = ext(g, "cpi", (2026, 8), ["total", "core", "transport", "comm", "educ", "food", "housing"])
    assert abs(r["total"]["2026-08-01"] - 4.888) < 1e-6
    assert abs(r["transport"]["2026-08-01"] - 8.022) < 1e-6
    assert abs(r["core"]["2026-08-01"] - 4.548) < 1e-6
    assert abs(r["educ"]["2026-08-01"] - 3.901) < 1e-6


def test_iip_levels_never_used_only_yoy():
    g = grids("nso_monthly_aug2026.xlsx")
    r = ext(g, "iip", (2026, 8), ["whole", "mfg", "mining"])
    assert abs(r["whole"]["2026-08-01"] - 14.41) < 1e-6
    assert abs(r["mfg"]["2026-08-01"] - 14.59) < 1e-6
    assert abs(r["mining"]["2026-08-01"] - 18.49) < 1e-6


def test_retail_visitors_state_investment_fdi():
    g = grids("nso_monthly_aug2026.xlsx")
    r = ext(g, "retail", (2026, 8), ["total", "goods", "food", "travel"])
    assert abs(r["total"]["2026-08-01"] - 679814.082) < 1e-3
    assert abs(r["goods"]["2026-08-01"] - 507417.982) < 1e-3
    assert abs(ext(g, "visitors", (2026, 8), ["total"])["total"]["2026-08-01"] - 1994469) < 1e-6
    assert abs(ext(g, "stateinv", (2026, 8), ["total"])["total"]["2026-08-01"] - 105749.188) < 1e-3
    assert abs(ext(g, "fdi", (2026, 8), ["total"])["total"]["2026-08-01"] - 21714.179) < 1e-3
    assert abs(ext(g, "newent", (2026, 8), ["total"])["total"]["2026-08-01"] - 138097) < 1e-6


def test_quarterly_tables():
    g = grids("nso_quarterly_q2_2026.xlsx")
    r = ext(g, "gdp_real", (2026, 6), ["total", "agri", "ind", "serv", "mfg"])
    assert abs(r["total"]["2026-04-01"] - 8.392) < 1e-6
    assert abs(r["total"]["2026-01-01"] - 7.94) < 1e-6
    assert abs(r["mfg"]["2026-04-01"] - 10.561) < 1e-6
    assert abs(ext(g, "gdp_nom", (2026, 6), ["total"])["total"]["2026-04-01"] - 3479487.231) < 1e-3
    assert abs(ext(g, "ppi", (2026, 6), ["industry"])["industry"]["2026-04-01"] - 5.403) < 1e-6
    assert abs(ext(g, "tot", (2026, 6), ["general"])["general"]["2026-04-01"] - 98.29) < 1e-6
    lab = ext(g, "labour", (2026, 6), ["lf", "emp", "agri", "ind", "serv"])
    assert abs(lab["lf"]["2026-04-01"] - 53787.55) < 1e-6
    assert abs(lab["agri"]["2026-04-01"] - 13294.52) < 1e-6
    assert abs(lab["serv"]["2026-01-01"] - 21589.53) < 1e-6
    un = ext(g, "unemp", (2026, 6), ["general", "youth", "under"])
    assert abs(un["general"]["2026-04-01"] - 2.232) < 1e-6
    assert abs(un["youth"]["2026-01-01"] - 8.87) < 1e-6
    assert abs(un["under"]["2026-04-01"] - 1.62) < 1e-6


def test_old_layout_nov2023():
    g = grids("nso_monthly_nov2023.xlsx")
    assert N.report_ym(g, "x") == (2023, 11)
    c = ext(g, "cpi", (2023, 11), ["total", "transport", "comm", "core"])
    assert abs(c["total"]["2023-11-01"] - 3.448) < 1e-6
    assert abs(c["comm"]["2023-11-01"] - 0.1) < 1e-6
    i = ext(g, "iip", (2023, 11), ["whole", "mfg", "mining"])
    assert abs(i["whole"]["2023-11-01"] - 5.786) < 1e-6
    assert abs(i["mining"]["2023-11-01"] - (-3.82)) < 1e-6
    assert abs(ext(g, "retail", (2023, 11), ["total"])["total"]["2023-11-01"] - 552702.578) < 1e-3


def test_misaligned_cpi_rejected():
    g = grids("nso_cpi_misaligned.xlsx")
    assert ext(g, "cpi", (2023, 10), ["total", "food"]) in ({}, {"total": {}, "food": {}}) or not any(
        ext(g, "cpi", (2023, 10), ["total", "food"]).values())


def test_customs_extract_abbreviated_months_and_pairs():
    rows = grids("nso_E01_2026.xlsx")[0][1]
    t = N.customs_extract(rows, "E01", r"^total", None, 2026)
    assert len(t) == 8 and abs(t["2026-08-01"] - 54794764.26) < 1e-3
    assert abs(t["2026-01-01"] - 43302753.78) < 1e-3
    fdi = N.customs_extract(rows, "E01", r"^include crude", None, 2026)
    assert abs(fdi["2026-08-01"] - 44295914.19) < 1e-3
    assert abs(N.customs_extract(rows, "E01", r"^computers, electr", None, 2026)["2026-08-01"] - 15854382.19) < 1e-3
    assert len(N.customs_extract(rows, "E01", r"^textiles?(,| and) (sewing|garments)", None, 2026)) == 8


def test_customs_e03_export_import_columns():
    rows = grids("nso_E03_2026.xlsx")[0][1]
    us = N.customs_extract(rows, "E03", r"^united states", "export", 2026)
    assert abs(us["2026-01-01"] - 13897730.67) < 1e-3 and len(us) == 3
    cn_imp = N.customs_extract(rows, "E03", r"^china, pr", "import", 2026)
    assert abs(cn_imp["2026-03-01"] - 18229000.0) < 1e-3


def test_ytd_to_month():
    d = {"2026-01-01": 10.0, "2026-02-01": 25.0, "2026-04-01": 70.0}
    assert N.ytd_to_month(d) == {"2026-01-01": 10.0, "2026-02-01": 15.0}


def test_list_and_attachment_links(monkeypatch):
    pages = {N.LIST_URL % 1: (FX / "nso_list_p1.html").read_text(encoding="utf-8")}
    monkeypatch.setattr(N, "_get", lambda url, binary=False, ok404=False: pages.get(url))
    got = N.list_reports(1)
    assert len(got) == 3 and all("/data-and-statistics/2026/" in u for u in got)
    monkeypatch.setattr(N, "_get", lambda url, binary=False, ok404=False: (FX / "nso_report_page.html").read_text(encoding="utf-8"))
    assert N.attachment("https://x/y/").endswith("02-Tables-Aug-2026-EN.xlsx")


def test_fetch_report_end_to_end_offline(monkeypatch):
    xlsx = (FX / "nso_monthly_aug2026.xlsx").read_bytes()
    monkeypatch.setattr(N, "list_reports", lambda pages: ["https://www.nso.gov.vn/en/data-and-statistics/2026/09/r/"])
    monkeypatch.setattr(N, "attachment", lambda u: "https://www.nso.gov.vn/wp-content/uploads/2026/09/02-Tables-Aug-2026-EN.xlsx")
    monkeypatch.setattr(N, "_get", lambda url, binary=False, ok404=False: xlsx)
    monkeypatch.delenv("MACRO_DB_BACKFILL", raising=False)
    spec = {"sid": "vn.cpi_core_yoy", "params": {"kind": "report", "table": "cpi", "row": "core"}}
    out = N.fetch([spec])
    assert abs(out["vn.cpi_core_yoy"]["obs"][-1][1] - 4.548) < 1e-6
    bad = {"sid": "vn.x", "params": {"kind": "report", "table": "retail", "row": "nope"}}
    assert "error" in N.fetch([bad])["vn.x"]
