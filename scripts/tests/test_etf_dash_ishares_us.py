"""Tests for 2026-10-19 additions to scripts/etf_dash/: iShares US holdings parser +
per-market ticker conversion (ishares_us.py), GBp (pence) price fix in
build_etf_dash.py, and the daily P/E record fallback for Exhibit 3 (pe_daily.py).
No network."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "etf_dash"))

import build_etf_dash as m  # noqa: E402
import ishares_us as iu  # noqa: E402
import pe_daily as pd_  # noqa: E402

HEADER = ('Ticker,Name,Sector,Asset Class,Market Value,Weight (%),Notional Value,Quantity,Price,'
          'Location,Exchange,Currency,FX Rate,Market Currency,Accrual Date')


def _csv(rows: list[str], title="iShares Test ETF", as_of="Oct 15, 2026") -> bytes:
    # 真實檔頭：基金名、as-of、成立日、股數、Stock/Bond/Cash/Other、空行、標題列
    head = [title, f'Fund Holdings as of,"{as_of}"', 'Inception Date,"Mar 12, 1996"',
            'Shares Outstanding,"9,000,000.00"', 'Stock,"-"', 'Bond,"-"', 'Cash,"-"', 'Other,"-"', '']
    return ("\n".join(head + [HEADER] + rows) + "\n").encode("utf-8")


def _row(t, n, sector, ac, w, exch, loc="X"):
    return (f'"{t}","{n}","{sector}","{ac}","1.00","{w}","1.00","1.00","1.00","{loc}","{exch}",'
            f'"USD","1.00","USD","-"')


# ── to_yf_symbol ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("ticker,exch,expect", [
    ("005930", "Korea Exchange (Stock Market)", "005930.KS"),
    ("247540", "Korea Exchange (Kosdaq)", "247540.KQ"),
    ("PBBANK", "Bursa Malaysia", "1295.KL"),
    ("TENAGA", "Bursa Malaysia", "5347.KL"),
    ("VALE3", "XBSP", "VALE3.SA"),
    ("NU", "NYSE", "NU"),
    ("XP", "NASDAQ", "XP"),
    ("RR.", "London Stock Exchange", "RR.L"),
    ("BT.A", "London Stock Exchange", "BT-A.L"),
    ("NOVO B", "Omx Nordic Exchange Copenhagen A/S", "NOVO-B.CO"),
    ("VOLV B", "Nasdaq Omx Nordic", "VOLV-B.ST"),
    ("ASML", "Euronext Amsterdam", "ASML.AS"),
    ("SAP", "Xetra", "SAP.DE"),
    ("NESN", "SIX Swiss Exchange", "NESN.SW"),
    ("MC", "Nyse Euronext - Euronext Paris", "MC.PA"),
    ("ENEL", "Borsa Italiana", "ENEL.MI"),
])
def test_to_yf_symbol_known(ticker, exch, expect):
    assert iu.to_yf_symbol(ticker, exch) == (expect, None)


def test_to_yf_symbol_unknown_exchange_not_guessed():
    sym, why = iu.to_yf_symbol("ABC", "Some New Bourse")
    assert sym is None and "Some New Bourse" in why


def test_to_yf_symbol_malaysia_unlisted_short_name_not_guessed():
    sym, why = iu.to_yf_symbol("NEWCO", "Bursa Malaysia")
    assert sym is None and "NEWCO" in why


def test_to_yf_symbol_korea_non_six_digit_rejected():
    sym, _ = iu.to_yf_symbol("ABC123", "Korea Exchange (Stock Market)")
    assert sym is None


def test_to_yf_symbol_empty_ticker():
    assert iu.to_yf_symbol("", "NYSE")[0] is None
    assert iu.to_yf_symbol(".", "London Stock Exchange")[0] is None


def test_exchange_table_covers_every_exchange_in_spec():
    for ex in ["London Stock Exchange", "SIX Swiss Exchange", "Nyse Euronext - Euronext Paris", "Xetra",
               "Euronext Amsterdam", "Bolsa De Madrid", "Nasdaq Omx Nordic", "Borsa Italiana",
               "Omx Nordic Exchange Copenhagen A/S", "Nyse Euronext - Euronext Brussels",
               "Nasdaq Omx Helsinki Ltd.", "Oslo Bors Asa", "Wiener Boerse Ag",
               "Irish Stock Exchange - All Market", "Nyse Euronext - Euronext Lisbon",
               "Athens Exchange S.A. Cash Market", "NYSE", "NASDAQ"]:
        assert ex in iu.EXCHANGE_SUFFIX


# ── parser ──────────────────────────────────────────────────────────────────

def test_parse_basic_equity_and_non_equity():
    raw = _csv([
        _row("PBBANK", "PUBLIC BANK", "Financials", "Equity", "15.97", "Bursa Malaysia", "Malaysia"),
        _row("TENAGA", "TENAGA NASIONAL", "Utilities", "Equity", "10.00", "Bursa Malaysia", "Malaysia"),
        _row("MYR", "MYR CASH", "Cash and/or Derivatives", "Cash", "2.10", "-"),
        _row("MESZ6", "MSCI EMER MKT INDEX DEC 26", "Cash and/or Derivatives", "Futures", "0.00", "Ice Futures U.S."),
    ])
    as_of, holdings, non_eq = iu.parse_ishares_us_holdings_csv(raw)
    assert as_of == "2026-10-15"
    assert [h["ticker"] for h in holdings] == ["1295.KL", "5347.KL"]
    assert holdings[0]["weight_pct"] == 15.97 and holdings[0]["sector"] == "金融"
    assert holdings[1]["sector"] == "公用事業"
    assert [n["ticker"] for n in non_eq] == ["MYR", "MESZ6"]
    assert "Cash" in non_eq[0]["reason"] and "Futures" in non_eq[1]["reason"]


def test_parse_unmapped_equity_kept_with_prefix_and_reason():
    raw = _csv([_row("NEWCO", "NEW CO BHD", "Financials", "Equity", "1.50", "Bursa Malaysia"),
                _row("ZZZ", "WEIRD", "Financials", "Equity", "1.00", "Some New Bourse")])
    _, holdings, _ = iu.parse_ishares_us_holdings_csv(raw)
    assert all(iu.is_unmapped(h["ticker"]) for h in holdings)
    assert holdings[0]["ticker"] == "UNMAPPED:NEWCO:Bursa Malaysia"
    assert holdings[0]["raw_ticker_field"] == "NEWCO" and "NEWCO" in holdings[0]["unmapped_reason"]


def test_parse_europe_symbol_cleaning():
    raw = _csv([_row("RR.", "ROLLS-ROYCE", "Industrials", "Equity", "10.5", "London Stock Exchange"),
                _row("NOVO B", "NOVO NORDISK", "Health Care", "Equity", "2.00", "Omx Nordic Exchange Copenhagen A/S")])
    _, holdings, _ = iu.parse_ishares_us_holdings_csv(raw)
    assert [h["ticker"] for h in holdings] == ["RR.L", "NOVO-B.CO"]
    assert holdings[1]["sector"] == "醫療保健"


def test_parse_html_page_rejected():
    html = b"<!DOCTYPE html><html><head></head><body>not csv</body></html>"
    with pytest.raises(RuntimeError):
        iu.parse_ishares_us_holdings_csv(html)


def test_parse_missing_header_raises():
    with pytest.raises(RuntimeError):
        iu.parse_ishares_us_holdings_csv(b'Fund,X\nFund Holdings as of,"Oct 15, 2026"\nfoo,bar\n')


def test_fetch_rejects_html_even_if_content_type_says_csv(monkeypatch):
    class R:
        content = b"<!DOCTYPE html><html>" + b"x" * 3000
        headers = {"content-type": "text/csv;charset=UTF-8"}
        def raise_for_status(self): pass
    monkeypatch.setattr(iu.requests, "get", lambda *a, **k: R())
    with pytest.raises(RuntimeError):
        iu.fetch_ishares_us_holdings_csv({"holdings_url": "http://x"})


def test_fetch_accepts_text_plain_csv(monkeypatch):
    body = _csv([_row("PBBANK", "PUBLIC BANK", "Financials", "Equity", "15.97", "Bursa Malaysia")])
    class R:
        content = body
        headers = {"content-type": "text/plain; charset=utf-8"}
        def raise_for_status(self): pass
    monkeypatch.setattr(iu.requests, "get", lambda *a, **k: R())
    assert iu.fetch_ishares_us_holdings_csv({"holdings_url": "http://x"}) == body


def test_registry_has_four_new_funds_wired():
    for k in ["EWY", "EWM", "EWZ", "IEV"]:
        cfg = m.FUND_REGISTRY[k]
        assert cfg["source"] == "ishares_us" and "ishares_us" in m.HOLDINGS_SOURCES
        assert cfg["yf_ticker"] == k and cfg["holdings_url"].endswith("/latest-holdings.csv")
        assert k in m.SECTOR_CONTRIB_ETF_KEYS
    assert m.FUND_REGISTRY["IEV"]["eps_scope_cutoff_pct"] == 90.0
    assert "eps_scope_cutoff_pct" not in m.FUND_REGISTRY["EWY"]


# ── GBp (pence) fix ─────────────────────────────────────────────────────────

def test_normalize_price_quote_pence():
    assert m.normalize_price_quote(1850.0, "GBp") == (18.5, "GBP", 100)
    assert m.normalize_price_quote(1850.0, "GBX") == (18.5, "GBP", 100)


def test_normalize_price_quote_pounds_and_others_unchanged():
    assert m.normalize_price_quote(18.5, "GBP") == (18.5, "GBP", 1)
    assert m.normalize_price_quote(100.0, "usd") == (100.0, "USD", 1)
    assert m.normalize_price_quote(None, None) == (None, "USD", 1)


def test_fetch_ticker_eps_and_price_converts_pence(monkeypatch):
    idx = ["0q", "+1q", "0y", "+1y"]
    cols = ["current", "7daysAgo", "30daysAgo", "60daysAgo", "90daysAgo", "currency"]
    df = pd.DataFrame([[1.0, 1, 1, 1, 1, "GBP"]] * 3 + [[1.2, 1.2, 1.2, 1.2, 1.2, "GBP"]], index=idx, columns=cols)

    class FI(dict):
        pass

    class T:
        def __init__(self, tk):
            self.eps_trend = df
            self.fast_info = FI(lastPrice=1850.0, marketCap=5e10, currency="GBp")
    monkeypatch.setattr(m.yf, "Ticker", T)
    out = m.fetch_ticker_eps_and_price("RR.L")
    assert out["status"] == "ok"
    assert out["price"] == pytest.approx(18.5) and out["price_currency"] == "GBP"
    assert out["price_quote_divisor"] == 100
    # 修正後個股本益比約 15.4x，在 2–300x 門檻內（修正前是 1541x，會被濾掉）
    assert 3 <= out["price"] / out["eps_fy_next_local"] <= 300


def test_no_existing_cache_uses_pence_path():
    """既有基金的 eps_cache 沒有 GBP 計價的持股（確認 GBp 修正不改變舊 17 檔數字）。"""
    import json
    cache_dir = SCRIPTS_DIR.parent / "data" / "etf_dash" / "eps_cache"
    for key in ["SPY", "RSP", "QQQ", "SMH", "SMH_UCITS", "TAIEX", "0050", "TOPIX",
                "XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLC", "XLB"]:
        p = cache_dir / f"{key}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        for tk, info in d.get("tickers", {}).items():
            assert info.get("price_currency") != "GBP", (key, tk)


# ── pe_daily ────────────────────────────────────────────────────────────────

def test_pe_daily_record_add_overwrite_and_sort(tmp_path):
    assert pd_.record("XLE", "2026-10-20", 15.123, 80.0, "price", tmp_path)
    assert pd_.record("XLE", "2026-10-19", 14.0, 79.0, "full", tmp_path)
    assert pd_.record("XLE", "2026-10-20", 16.0, 81.5, "full", tmp_path)  # 同日覆蓋
    rows = pd_.load("XLE", tmp_path)
    assert [r["date"] for r in rows] == ["2026-10-19", "2026-10-20"]
    assert rows[1]["pe"] == 16.0 and rows[1]["coverage_pct"] == 81.5 and rows[1]["mode"] == "full"
    text = (tmp_path / "XLE.csv").read_text()
    assert text.splitlines()[0] == "date,pe,coverage_pct,mode"
    assert text.count("2026-10-20") == 1


def test_pe_daily_record_ignores_bad_values(tmp_path):
    assert not pd_.record("XLE", "2026-10-20", None, 80.0, "price", tmp_path)
    assert not pd_.record("XLE", "2026-10-20", 0, 80.0, "price", tmp_path)
    assert not pd_.record("XLE", None, 12.0, 80.0, "price", tmp_path)
    assert pd_.load("XLE", tmp_path) == []


def _data(series, pe=15.0, date="2026-10-19", mode="price", full_refresh="weekly"):
    return {"mode": mode, "full_refresh": full_refresh, "price": {"date": date},
            "weighted_forward_pe": {"value": pe, "coverage_pct": 97.0},
            "chart": {"pe_history": {"series": series, "start_date": series[0]["date"] if series else None,
                                       "earnings_coverage_pct": 55.0 if series else None,
                                       "rollover_events": [],
                                       "suppressed_note": None if series else "dd 涵蓋 12%"}}}


def test_fallback_uses_record_when_suppressed(tmp_path):
    pd_.record("XLE", "2026-10-18", 14.5, 96.0, "full", tmp_path)
    ph = pd_.apply_fallback(_data([]), "XLE", tmp_path)
    assert ph["source"] == "daily_record"
    assert [p["date"] for p in ph["series"]] == ["2026-10-18", "2026-10-19"]
    assert ph["series"][-1]["pe"] == 15.0 and ph["start_date"] == "2026-10-18"
    assert "2026-10-18 起記錄" in ph["source_note_zh"] and "每週" in ph["source_note_zh"]


def test_fallback_monthly_wording_for_topix(tmp_path):
    ph = pd_.apply_fallback(_data([], full_refresh="monthly"), "TOPIX", tmp_path)
    assert "每月" in ph["source_note_zh"]


def test_fallback_does_not_touch_backcast_line(tmp_path):
    series = [{"date": "2026-10-01", "pe": 12.0, "coverage_pct": 60.0},
              {"date": "2026-10-19", "pe": 15.0, "coverage_pct": 60.0}]
    d = _data(series)
    ph = pd_.apply_fallback(d, "SPY", tmp_path)
    assert ph["source"] == "dd_backcast" and ph["series"] == series
    assert "source_note_zh" not in ph
    # 但今天的值仍記一列
    assert pd_.load("SPY", tmp_path)[0]["pe"] == 15.0


def test_fallback_single_point(tmp_path):
    ph = pd_.apply_fallback(_data([]), "EWY", tmp_path)
    assert ph["source"] == "daily_record" and len(ph["series"]) == 1
    assert ph["series"][0] == {"date": "2026-10-19", "pe": 15.0, "coverage_pct": 97.0}


def test_fallback_no_pe_no_record(tmp_path):
    d = _data([], pe=None)
    ph = pd_.apply_fallback(d, "EWY", tmp_path)
    assert ph["series"] == [] and ph["source"] == "none"


# ── 2026-10-29 加 28 檔：新交易所代號轉換與註冊 ────────────────────────────

@pytest.mark.parametrize("ticker,exchange,expected", [
    ("700", "Hong Kong Exchanges And Clearing Ltd", "0700.HK"),
    ("12345", "Hong Kong Exchanges And Clearing Ltd", "12345.HK"),
    ("J36", "Singapore Exchange", "J36.SI"),
    ("600519", "Shanghai Stock Exchange", "600519.SS"),
    ("300750", "Shenzhen Stock Exchange", "300750.SZ"),
    ("RELIANCE", "National Stock Exchange Of India", "RELIANCE.NS"),
    ("M&M", "National Stock Exchange Of India", "M&M.NS"),
    ("BAJAJ.AUTO", "National Stock Exchange Of India", "BAJAJ-AUTO.NS"),
    ("534091", "Bse Ltd", "534091.BO"),
    ("RY", "Toronto Stock Exchange", "RY.TO"),
    ("TECK.B", "Toronto Stock Exchange", "TECK-B.TO"),
    ("BHP", "Asx - All Markets", "BHP.AX"),
    ("BBCA", "Indonesia Stock Exchange", "BBCA.JK"),
    ("PTT.R", "Stock Exchange Of Thailand", "PTT.BK"),
    ("ICT", "Philippine Stock Exchange Inc.", "ICT.PS"),
    ("FPH", "New Zealand Exchange Ltd", "FPH.NZ"),
    ("WALMEX*", "Bolsa Mexicana De Valores", "WALMEX.MX"),
    ("GMEXICOB", "Bolsa Mexicana De Valores", "GMEXICOB.MX"),
    ("1120", "Saudi Stock Exchange", "1120.SR"),
    ("RR.", "London Stock Exchange", "RR.L"),
    ("HEI A", "NYSE", "HEI-A"),
])
def test_new_exchange_symbol_conversion(ticker, exchange, expected):
    assert iu.to_yf_symbol(ticker, exchange) == (expected, None)


def test_new_exchange_rejects_malformed_codes():
    assert iu.to_yf_symbol("ABC", "Hong Kong Exchanges And Clearing Ltd")[0] is None
    assert iu.to_yf_symbol("12", "Saudi Stock Exchange")[0] is None
    assert iu.to_yf_symbol("-", "NO MARKET (E.G. UNLISTED)")[0] is None


@pytest.mark.parametrize("raw,expected", [
    ("VIC VN", "VIC.VN"), ("AEM", "AEM"), ("NST AU", "NST.AX"), ("EDV LN", "EDV.L"),
    ("2259 HK", "2259.HK"), ("700 HK", "0700.HK"), ("LUG CN", "LUG.TO"),
    ("AMMN IJ", "AMMN.JK"), ("PE&OLES* MM", "PE&OLES.MX"),
])
def test_bloomberg_symbol_conversion(raw, expected):
    assert iu.bloomberg_to_yf_symbol(raw) == (expected, None)


def test_bloomberg_symbol_unknown_code_not_guessed():
    assert iu.bloomberg_to_yf_symbol("ABC ZZ")[0] is None
    assert iu.bloomberg_to_yf_symbol("2688492D")[0] is None


NEW_COUNTRY_KEYS = ["EWU", "EWG", "EWQ", "EWP", "EWN", "EWL", "EWI", "EWA", "EWS", "EWH", "MCHI", "INDA",
                    "THD", "VNM", "EIDO", "EPHE", "ENZL", "EWC", "EWW", "KSA"]
NEW_SUBSECTOR_KEYS = ["SOXX", "IGV", "ITA", "XBI", "XOP", "KRE", "XHB", "GDX"]


def test_28_new_funds_registered_with_valid_sources():
    for k in NEW_COUNTRY_KEYS + NEW_SUBSECTOR_KEYS:
        cfg = m.FUND_REGISTRY[k]
        assert cfg["yf_ticker"] == k and cfg["source"] in m.HOLDINGS_SOURCES
        assert cfg["holdings_url"].startswith("https://") and cfg["holdings_page_url"].startswith("https://")
    assert m.FUND_REGISTRY["VNM"]["source"] == m.FUND_REGISTRY["GDX"]["source"] == "vaneck_intl"
    assert {m.FUND_REGISTRY[k]["source"] for k in ["XBI", "XOP", "KRE", "XHB"]} == {"ssga"}
    for k in ["MCHI", "INDA", "KSA", "IGV", "KRE", "XBI"]:
        assert m.FUND_REGISTRY[k]["eps_scope_cutoff_pct"] == 90.0


def test_new_funds_in_workflow_and_page_groups():
    root = SCRIPTS_DIR.parent
    wf = (root / ".github" / "workflows" / "etf-dash-daily.yml").read_text(encoding="utf-8")
    html = (root / "docs" / "etf-dash" / "index.html").read_text(encoding="utf-8")
    for k in NEW_COUNTRY_KEYS + NEW_SUBSECTOR_KEYS:
        assert f"--etf {k} " in wf, k
        assert f"key:'{k}'" in html, k
    # 頁面分組與註冊表一一對應
    import re
    block = html[html.index("var FUND_GROUPS = ["):html.index("var FUND_LIST =")]
    assert set(re.findall(r"\{key:'([^']+)', label:", block)) == set(m.FUND_REGISTRY)


def test_research_universe_unchanged_by_new_funds():
    import compare_common as cc
    assert len(set(cc.RESEARCH_UNIVERSE)) == 21
    assert not (set(cc.RESEARCH_UNIVERSE) & set(NEW_COUNTRY_KEYS + NEW_SUBSECTOR_KEYS))


def test_vaneck_intl_parser_maps_suffix_and_flags_unmapped(monkeypatch):
    rows = [{"ticker": "VIC", "raw_ticker_field": "VIC VN", "name": "Vingroup", "weight_pct": 8.0},
            {"ticker": "AEM", "raw_ticker_field": "AEM", "name": "Agnico", "weight_pct": 5.0},
            {"ticker": "2688492D", "raw_ticker_field": "2688492D", "name": "junk", "weight_pct": 0.0}]
    monkeypatch.setattr(m, "parse_holdings_xlsx", lambda raw: ("2026-10-27", rows))
    as_of, hs, ne = m.parse_vaneck_intl_holdings(b"x")
    assert [h["ticker"] for h in hs[:2]] == ["VIC.VN", "AEM"]
    assert iu.is_unmapped(hs[2]["ticker"]) and ne == []
