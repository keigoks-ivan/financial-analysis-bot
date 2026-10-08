"""美國第二次擴充：新 fetcher 的離線解析測試，加目錄結構檢查。"""
import datetime as dt
import json
from pathlib import Path

import pandas as pd
import pytest

from macro_db.sources import (REGISTRY, fiscaldata, nyfed, nyfed_markets, us_atlfed_wage, us_eia_weekly,
                              us_finra_margin, us_kcfed_mfg, us_ofr_fsi, us_philly_fed, us_tic, us_tsa)

CAT = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "us.json"


# ---------- 費城聯儲 ----------
def test_philly_ads_and_spf_and_nbos():
    ads = pd.DataFrame({"Date": ["1960:03:01", "1960:03:02", "1960:03:03"], "ADS_Index": [-0.5, "x", 0.2]})
    assert us_philly_fed.parse_ads(ads) == [("1960-03-01", -0.5), ("1960-03-03", 0.2)]
    spf = pd.DataFrame({"YEAR": [2026, 2026], "QUARTER": [2, 3], "CPI10": [2.4, None]})
    assert us_philly_fed.parse_spf(spf, "CPI10") == [("2026-04-01", 2.4)]
    nb = pd.DataFrame({"date": [pd.Timestamp("2026-09-30"), pd.Timestamp("2026-08-31")], "gabndif_sa": [0.3, -8.2]})
    assert us_philly_fed.parse_nbos(nb, "gabndif_sa") == [("2026-09-01", 0.3), ("2026-08-01", -8.2)]


def test_philly_anxious_shifts_target_quarter_to_survey_quarter():
    df = pd.DataFrame([[None, None, None], ["Obs Year", "Obs Quarter", "Anxious Index"], [2026, 1, 14.9], [2026, 4, 19.9], [2027, None, None]])
    # 檔內 2026Q1（預測目標季）＝2025Q4 調查；2026Q4＝2026Q3 調查
    assert us_philly_fed.parse_anxious(df) == [("2025-10-01", 14.9), ("2026-07-01", 19.9)]
    assert us_philly_fed.parse_anxious(df, 0)[0][0] == "2026-01-01"


# ---------- 亞特蘭大聯儲 ----------
def test_atlanta_wage_finds_column_by_header_text():
    df = pd.DataFrame([["note", None, None], [None, "16-24", "25-54"],
                       [pd.Timestamp("1997-01-01"), 9.0, 4.2], [pd.Timestamp("1997-02-01"), None, 4.3]])
    assert us_atlfed_wage.parse_sheet(df, "25-54") == [("1997-01-01", 4.2), ("1997-02-01", 4.3)]
    assert us_atlfed_wage.parse_sheet(df, "16-24") == [("1997-01-01", 9.0)]
    with pytest.raises(ValueError):
        us_atlfed_wage.parse_sheet(df, "不存在")


# ---------- 堪薩斯市聯儲 ----------
def _kc_df():
    rows = [["Table2", None, None], ["Historical Manufacturing Survey Indexes", None, None],
            [None, pd.Timestamp("2001-07-31"), pd.Timestamp("2001-08-31")],
            ["Versus a Month Ago", None, None], ["(seasonally adjusted)", None, None],
            ["Composite Index", -16, 0], ["Production", -18, 19],
            ["Versus a Month Ago", None, None], ["(not seasonally adjusted)", None, None],
            ["Composite Index", 99, 99]]
    return pd.DataFrame(rows)


def test_kc_link_from_page_and_block_lookup():
    html = '<a href="/documents/12345/2026Sept24historicalmfg.xlsx">Historical</a>'
    assert us_kcfed_mfg.find_link(html, "https://www.kansascityfed.org/surveys/manufacturing-survey/") == \
        "https://www.kansascityfed.org/documents/12345/2026Sept24historicalmfg.xlsx"
    with pytest.raises(ValueError):
        us_kcfed_mfg.find_link("<html>沒有連結</html>")
    assert us_kcfed_mfg.parse_block(_kc_df(), "Versus a Month Ago", "(seasonally adjusted)", "Composite Index") == \
        [("2001-07-01", -16.0), ("2001-08-01", 0.0)]      # 取季調那一塊，不是 99
    with pytest.raises(ValueError):
        us_kcfed_mfg.parse_block(_kc_df(), "Versus a Month Ago", "(seasonally adjusted)", "Backlog of orders")


def test_kc_fetch_returns_error_when_link_missing(monkeypatch):
    from macro_db.sources import us_common
    monkeypatch.setattr(us_common.Cache, "text", lambda self, url, **kw: "<html></html>")
    spec = {"sid": "us.kc_comp", "params": {"block": "Versus a Month Ago", "note": "(seasonally adjusted)", "label": "Composite Index"}}
    r = us_kcfed_mfg.fetch([spec])
    assert "error" in r["us.kc_comp"] and "連結" in r["us.kc_comp"]["error"]


# ---------- TIC ----------
def test_tic_recent_and_history_merge():
    recent = "Country\t2026-06\t2026-07\nJapan\t1,116.7\t1103.9\nChina, Mainland\t633.4\t618.0\n".replace("1,116.7", "1116.7")
    assert us_tic.parse_recent(recent, "Japan") == {"2026-06-01": 1116.7, "2026-07-01": 1103.9}
    hist = "\tDec\tNov\nCountry\t2025\t2025\nJapan\t1000.1\t990.2\n\tJan\tFeb\nCountry\t2024\t2024\nJapan\t1\t2\n"
    h = us_tic.parse_history(hist, "Japan")
    assert h["2025-12-01"] == 1000.1 and h["2025-11-01"] == 990.2 and h["2024-02-01"] == 2.0


# ---------- OFR／FINRA／EIA／TSA ----------
def test_ofr_finra_eia_tsa():
    csv_text = "Date,OFR FSI,Credit\n2026-10-05,-2.109,-0.96\n2026-10-06,,-1.014\n"
    assert us_ofr_fsi.parse(csv_text, "OFR FSI") == [("2026-10-05", -2.109)]
    assert us_ofr_fsi.parse(csv_text, "Credit")[-1] == ("2026-10-06", -1.014)
    df = pd.DataFrame([["2026-08", 1453832], ["2026-07", 1417225], ["說明", 1]])
    assert us_finra_margin.parse(df) == [("2026-07-01", 1417225.0), ("2026-08-01", 1453832.0)]
    eia = pd.DataFrame([["Sourcekey", "x"], ["Date", "y"], ["Units", "z"], [pd.Timestamp("2026-10-02"), 424134], [pd.Timestamp("2026-09-25"), None]])
    assert us_eia_weekly.parse(eia) == [("2026-10-02", 424134.0)]
    html = "<td>10/7/2026</td><td> 2,377,978 </td><tr><td>10/6/2026 </td> <td>2,089,407</td>"
    assert us_tsa.parse(html) == {"2026-10-07": 2377978.0, "2026-10-06": 2089407.0}


# ---------- NY Fed ----------
def test_nyfed_sce_hhdc_acm_parsers():
    sce = pd.DataFrame([[None, None], [None, None], [None, None], [None, "Median one-year ahead expected inflation"],
                        ["201306", 3.09], ["202609", 3.9027]])
    assert nyfed.parse_sce(sce, "Median one-year ahead expected inflation") == [("2013-06-01", 3.09), ("2026-09-01", 3.9027)]
    hh = pd.DataFrame([[None, "Mortgage", "HE Revolving"], ["03:Q1", 4.942, 0.242], ["26:Q2", 13.117, 0.4585], ["* 註", None, None]])
    assert nyfed.parse_hhdc(hh, "mortgage") == [("2003-01-01", 4.942), ("2026-04-01", 13.117)]
    assert nyfed.parse_hhdc(hh, "HE Revolving")[-1] == ("2026-04-01", 0.4585)
    acm = pd.DataFrame({"DATE": ["05-Oct-2026", "06-Oct-2026"], "ACMTP10": [0.9, 0.946]})
    assert nyfed.parse_acm(acm, "ACMTP10") == [("2026-10-05", 0.9), ("2026-10-06", 0.946)]
    c = nyfed.hhdc_candidates("x/{YYYY}Q{q}.xlsx", dt.date(2026, 10, 8), 3)
    assert c == ["x/2026Q4.xlsx", "x/2026Q3.xlsx", "x/2026Q2.xlsx"]
    assert nyfed.hhdc_candidates("{YYYY}Q{q}", dt.date(2026, 2, 1), 2) == ["2026Q1", "2025Q4"]


def test_soma_summary_skips_blank_and_scales():
    txt = json.dumps({"soma": {"summary": [{"asOfDate": "2003-07-09", "frn": "", "bills": "239304992000"},
                                          {"asOfDate": "2026-09-30", "frn": "20046000000", "bills": "560211000000"}]}})
    assert nyfed_markets.parse_soma(txt, "frn") == [("2026-09-30", 0.020046)]
    assert nyfed_markets.parse_soma(txt, "bills")[0] == ("2003-07-09", 0.239304992)


# ---------- FiscalData ----------
def test_mts9_picks_section_by_summary_rows():
    rows = [
        {"record_date": "2026-08-31", "src_line_nbr": "2", "data_type_cd": "D", "classification_desc": "Customs Duties", "current_month_rcpt_outly_amt": "12835500000"},
        {"record_date": "2026-08-31", "src_line_nbr": "1", "data_type_cd": "S", "classification_desc": "Receipts", "current_month_rcpt_outly_amt": "null"},
        {"record_date": "2026-08-31", "src_line_nbr": "10", "data_type_cd": "S", "classification_desc": "Net Outlays", "current_month_rcpt_outly_amt": "null"},
        {"record_date": "2026-08-31", "src_line_nbr": "11", "data_type_cd": "D", "classification_desc": "Health", "current_month_rcpt_outly_amt": "80514500000"},
        {"record_date": "2026-08-31", "src_line_nbr": "5", "data_type_cd": "D", "classification_desc": "Health", "current_month_rcpt_outly_amt": "999"},   # 收入段同名，不取
    ]
    assert fiscaldata.parse_mts9(rows, "Receipts", "Customs Duties") == [("2026-08-01", 12.8355)]
    assert fiscaldata.parse_mts9(rows, "Net Outlays", "Health") == [("2026-08-01", 80.5145)]


def test_fiscaldata_mspd_avg_rate_int_exp_auction():
    assert fiscaldata.parse_mspd1([{"record_date": "2026-09-30", "debt_held_public_mil_amt": "7117937.0671"}]) == [("2026-09-01", 7.117937)]
    assert fiscaldata.parse_avg_rate([{"record_date": "2026-09-30", "avg_interest_rate_amt": "3.531"}, {"record_date": "2026-08-31", "avg_interest_rate_amt": "null"}]) == [("2026-09-01", 3.531)]
    ie = [{"record_date": "2026-09-30", "expense_catg_desc": "INTEREST EXPENSE ON PUBLIC ISSUES", "month_expense_amt": "80000000000"},
          {"record_date": "2026-09-30", "expense_catg_desc": "INTEREST EXPENSE ON PUBLIC ISSUES - OTHER", "month_expense_amt": "6655400000"},
          {"record_date": "2026-09-30", "expense_catg_desc": "INTEREST EXPENSE ON INTRAGOVERNMENTAL", "month_expense_amt": "1"}]
    assert fiscaldata.parse_int_exp(ie, "INTEREST EXPENSE ON PUBLIC") == [("2026-09-01", 86.6554)]
    au = [{"auction_date": "2026-09-22", "original_security_term": "2-Year", "bid_to_cover_ratio": "2.63", "inflation_index_security": "No", "floating_rate": "No"},
          {"auction_date": "2026-09-23", "original_security_term": "2-Year", "bid_to_cover_ratio": "2.1", "inflation_index_security": "No", "floating_rate": "Yes"},
          {"auction_date": "2026-09-24", "original_security_term": "5-Year", "bid_to_cover_ratio": "2.2", "inflation_index_security": "No", "floating_rate": "No"}]
    ex = {"inflation_index_security": "Yes", "floating_rate": "Yes"}
    assert fiscaldata.parse_auction(au, "2-Year", "bid_to_cover_ratio", ex) == [("2026-09-22", 2.63)]


# ---------- 目錄 ----------
def test_us_catalog_expand2_structure():
    cat = json.loads(CAT.read_text())
    keys = [c["key"] for c in cat["categories"]]
    assert {"energy", "credit", "fiscal"} <= set(keys)
    sids, chart_keys = {}, set()
    for c in cat["categories"]:
        assert len(c["charts"]) >= 3, c["key"]
        for ch in c["charts"]:
            assert ch["key"] not in chart_keys, ch["key"]
            chart_keys.add(ch["key"])
            for s in ch["series"]:
                if "fetcher" not in s:      # 自算（derived）序列
                    continue
                assert sids.setdefault(s["sid"], s["fetcher"]) == s["fetcher"], s["sid"]   # 同 sid 可跨圖重複，但 fetcher 要一致
                assert s["fetcher"] in REGISTRY, s["sid"]
                new_kind = s["params"].get("kind") in ("sce", "acm", "hhdc", "soma_summary", "mts9", "mspd1", "avg_rate", "int_exp", "auction")
                if s["fetcher"].startswith("us_") or new_kind:
                    urls = [v for v in s["params"].values() if isinstance(v, str) and v.startswith("http")]
                    assert urls, s["sid"]
                if s["display"] == "sum12m":
                    assert s["freq"] in ("M", "Q")
                lic = s.get("license", "")
                if s["sid"] == "us.finra_margin_debit":
                    assert lic == "copyright:FINRA"
    # 新 fetcher 一律 us_ 開頭
    for name in ("us_philly_fed", "us_atlfed_wage", "us_kcfed_mfg", "us_eia_weekly", "us_tic", "us_ofr_fsi", "us_finra_margin", "us_tsa"):
        assert name in REGISTRY
