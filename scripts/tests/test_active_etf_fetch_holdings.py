"""Unit tests for scripts/active_etf/fetch_holdings.py — one parser test per
issuer, using small fixtures modeled on each issuer's real PCF/holdings
response (captured 2026-09-24/25 from the official endpoints themselves,
then trimmed to ~5 holdings). No network access; no dependency on any
third-party aggregator's data or code.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import openpyxl
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "active_etf"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "active_etf"))

import fetch_holdings as m  # noqa: E402


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def load_text(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


# ── 共用工具 ──────────────────────────────────────────────────────────────
def test_to_num():
    assert m.to_num("30,372,771,968") == 30372771968.0
    assert m.to_num("NT$8.10") == 8.10
    assert m.to_num(8.1) == 8.1
    assert m.to_num(None) is None
    assert m.to_num("-") is None


def test_parse_dotnet_date():
    assert m.parse_dotnet_date("2026-08-04T00:00:00") == "2026-08-04"
    # ms epoch for 2026-08-04 00:00 台北時間(+8)
    assert m.parse_dotnet_date("/Date(1785772800000)/") == "2026-08-04"


def test_ticker_for_twse_vs_tpex():
    twse, tpex = {"2330", "2454"}, {"6223", "5274"}
    assert m.ticker_for("2330", twse, tpex) == "2330.TW"
    assert m.ticker_for("6223", twse, tpex) == "6223.TWO"
    # 兩邊都查不到 → fallback 上市(.TW),不讓查表失敗擋住整批
    assert m.ticker_for("9999", twse, tpex) == "9999.TW"


def test_isin_for_matches_known_values():
    # 參考值來自聯博/摩根官網產品頁網址本身(公開資訊,可獨立核對算法正確)
    assert m.isin_for("00404A") == "TW00000404A5"


# ── validate_holdings ────────────────────────────────────────────────────
def _h(code, weight, shares=1000):
    return {"code": code, "name": "測試", "shares": shares, "weight_pct": weight}


def test_validate_holdings_ok():
    holdings = [_h(str(1000 + i), 5.0) for i in range(19)] + [_h("9999", 5.0)]
    m.validate_holdings("TEST", holdings, [])  # 20*5=100%,不拋錯


def test_validate_holdings_too_few():
    with pytest.raises(m.FetchError, match="少於下限"):
        m.validate_holdings("TEST", [_h("1000", 50.0)], [])


def test_validate_holdings_weight_out_of_range():
    # 股票權重合計 40% < 90% 下限
    holdings = [_h(str(1000 + i), 4.0) for i in range(10)]
    with pytest.raises(m.FetchError, match="超出"):
        m.validate_holdings("TEST", holdings, [])


def test_validate_holdings_ignores_other_overlay():
    """期貨/選擇權 overlay(other)不計入權重合計驗證——實測 00404A 聯博股票 90.22%
    + 期貨 overlay 15.43% 合計會到 105%,若把 other 併入驗證會誤殺合法槓桿曝險。"""
    holdings = [_h(str(1000 + i), 9.0) for i in range(10)]  # 90%
    other = [{"type": "futures", "name": "台股期貨", "weight_pct": 20.0}]
    m.validate_holdings("TEST", holdings, other)  # 不拋錯


def test_validate_holdings_duplicate_code():
    holdings = [_h(str(1000 + i), 5.0) for i in range(9)] + [_h("2330", 5.0)] * 2
    with pytest.raises(m.FetchError, match="重複"):
        m.validate_holdings("TEST", holdings, [])


# ── 野村 ─────────────────────────────────────────────────────────────────
def test_parse_nomura():
    d = load_json("nomura_tradeinfo.json")
    parsed = m.parse_nomura_entries(d["Entries"], "00980A")
    assert parsed["as_of"] == d["Entries"]["CNavDtStr"].replace("/", "-")
    assert len(parsed["holdings"]) == 5
    h0 = parsed["holdings"][0]
    assert h0["code"] and h0["shares"] > 0 and 0 < h0["weight_pct"] < 100
    assert parsed["nav"]["scale"] is not None


def test_parse_nomura_no_entries_returns_none():
    assert m.parse_nomura_entries(None, "00980A") is None
    assert m.parse_nomura_entries({}, "00980A") is None


# ── 安聯 ─────────────────────────────────────────────────────────────────
def test_parse_allianz():
    d = load_json("allianz_tradeinfo.json")
    parsed = m.parse_allianz_entries(d["Entries"], "00984A")
    assert parsed["as_of"] == d["Entries"]["CNavDt"][:10]
    assert len(parsed["holdings"]) == 4
    for h in parsed["holdings"]:
        assert h["shares"] > 0 and 0 < h["weight_pct"] < 100


# ── 統一 ─────────────────────────────────────────────────────────────────
def test_parse_president_fund_map():
    fm = m.parse_president_fund_map(load_text("president_pcf_page.html"))
    assert "00981A" in fm and fm["00981A"]


def test_parse_president_pcf():
    d = load_json("president_getpcf.json")
    parsed = m.parse_president_pcf(d, "00981A")
    assert parsed["as_of"] == m.parse_dotnet_date(d["pcf"][0]["TranDate"])
    assert len(parsed["holdings"]) == 4  # 修剪過的 fixture
    # 期貨(GD)分段要拆進 other,不能混進 holdings
    assert any(o["type"] == "futures" for o in parsed["other"])
    assert parsed["nav"]["holders"] is not None


# ── 群益 ─────────────────────────────────────────────────────────────────
def test_parse_capital_buyback():
    d = load_json("capital_buyback.json")
    parsed = m.parse_capital_buyback(d, "00982A")
    assert parsed["as_of"] == d["data"]["pcf"]["date2"]
    assert len(parsed["holdings"]) == 5
    assert parsed["nav"]["holders"] == d["data"]["pcf"]["numberPeople"]


# ── 台新 ─────────────────────────────────────────────────────────────────
def test_parse_taishin_detail():
    parsed = m.parse_taishin_detail(load_text("taishin_detail.html"), "00987A")
    assert parsed["as_of"] == "2026-09-23"
    assert len(parsed["holdings"]) == 5
    # Bloomberg 式 "2330 TT" → 剝掉 " TT" 還原成 "2330"
    assert parsed["holdings"][0]["code"] == "2330"


def test_taishin_normalize_code_keeps_foreign_suffix():
    assert m._taishin_normalize_code("2330 TT") == "2330"
    assert m._taishin_normalize_code("MU US") == "MU US"


# ── 復華 ─────────────────────────────────────────────────────────────────
def test_parse_fuhhwa_assets():
    d = load_json("fuhhwa_assets.json")
    parsed = m.parse_fuhhwa_assets(d, "00991A")
    assert parsed["as_of"] == d["result"][0]["dDate"].replace("/", "-")
    assert len(parsed["holdings"]) >= 1
    for h in parsed["holdings"]:
        assert h["shares"] > 0


def test_parse_fuhhwa_assets_empty_result_returns_none():
    assert m.parse_fuhhwa_assets({"result": []}, "00991A") is None


# ── 中信 ─────────────────────────────────────────────────────────────────
def test_parse_ctbc_holding():
    d = load_json("ctbc_holdingweight.json")
    parsed = m.parse_ctbc_holding(d, "00995A")
    assert parsed["as_of"] == d["Data"]["FundAssets"][0]["資料日期"].replace("/", "-")
    assert len(parsed["holdings"]) == 5
    # MARGIN/CASH 分段要拆進 other
    kinds = {o["type"] for o in parsed["other"]}
    assert "cash" in kinds and "futures" in kinds


def test_parse_ctbc_holding_bad_result_code_returns_none():
    assert m.parse_ctbc_holding({"ResultCode": 1}, "00995A") is None


# ── 兆豐 ─────────────────────────────────────────────────────────────────
def test_parse_megafunds_fund_map():
    fm = m.parse_megafunds_fund_map(load_text("megafunds_fundlist.html"))
    assert fm.get("兆豐台灣豐收主動式ETF基金") == "23"


def test_parse_megafunds_result():
    parsed = m.parse_megafunds_result(load_text("megafunds_result.html"), "00996A")
    # 查詢日期(2026/09/29)是公告生效日,其後第一個日期(2026/09/24)才是持股基準日
    assert parsed["as_of"] == "2026-09-24"
    assert len(parsed["holdings"]) == 5


# ── 國泰 ─────────────────────────────────────────────────────────────────
def test_build_cathay_holdings():
    stocks = load_json("cathay_stockslist.json")["result"]
    weights = load_json("cathay_weights.json")["result"]["stockWeights"]
    bs = load_json("cathay_buysale.json")["result"]
    baskets = float(bs["totUnit"].replace(",", "")) / float(bs["basketUnit"].replace(",", ""))
    holdings = m.build_cathay_holdings(stocks, weights, baskets, "00400A")
    # 兩邊(成分股表/權重表)在這份 fixture 裡代號完全對齊(參考真實抓取的行為)
    assert {h["code"] for h in holdings} == {"1215", "1303", "2059", "2303", "2308"}
    for h in holdings:
        assert h["shares"] > 0
    kaohu = next(h for h in holdings if h["code"] == "1303")
    assert kaohu["shares"] == round(976 * baskets)


def test_build_cathay_holdings_no_overlap_raises():
    with pytest.raises(m.FetchError, match="無交集"):
        m.build_cathay_holdings([{"prod": "1234", "prodName": "x", "basketShares": "10"}], [], 100, "00400A")


# ── 聯博 ─────────────────────────────────────────────────────────────────
def test_parse_ab_holdings():
    d = load_json("ab_holdings.json")
    as_of, holdings, other = m.parse_ab_holdings(d, "00404A")
    assert as_of == "2026-09-24"
    assert len(holdings) == 4
    # 期貨/選擇權分段要拆進 other,不能混進權重合計
    kinds = {o["type"] for o in other}
    assert "futures" in kinds


def test_parse_ab_holdings_no_equity_section_raises():
    with pytest.raises(m.FetchError, match="equity"):
        m.parse_ab_holdings({"domesticHoldings": []}, "00404A")


# ── 摩根(xlsx)──────────────────────────────────────────────────────────
def _xlsx_bytes(sheets: dict[str, list[list]]) -> bytes:
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, rows in sheets.items():
        ws = wb.create_sheet(name)
        for row in rows:
            ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_jpmorgan_read_and_parse_xlsx():
    holding_sheet = [
        ["基金資產 - 股票 (2026-09-24)"],
        ["股票代碼", "股票名稱", "股數", "金額", "權重(%)"],
        ["2330", "台積電", "90000", "223200000", "8.05"],
        ["2454", "聯發科", "32000", "40960000", "3.5"],
    ]
    sheets = _xlsx_bytes({"holding": holding_sheet})
    parsed_sheets = m.read_xlsx(sheets)
    as_of, holdings = m.parse_jpmorgan_holdings_xlsx(parsed_sheets, "00401A")
    assert as_of == "2026-09-24"
    assert len(holdings) == 2
    assert holdings[0] == {"code": "2330", "name": "台積電", "shares": 90000, "weight_pct": 8.05}


def test_jpmorgan_parse_meta_xlsx():
    meta_sheet = [
        ["現金申購買回清單公告(2026-09-24)", ""],
        ["基金淨資產價值(元)", "1234567890"],
        ["已發行受益權單位總數", "100000000"],
        ["每受益權單位淨資產價值(元)", "12.35"],
    ]
    sheets = m.read_xlsx(_xlsx_bytes({"m12": meta_sheet}))
    meta = m.parse_jpmorgan_meta_xlsx(sheets)
    assert meta["scale"] == 1234567890.0
    assert meta["units"] == 100000000.0
    assert meta["holders"] is None  # 摩根檔案不揭露受益人數


def test_jpmorgan_bad_zip_raises():
    with pytest.raises(m.FetchError, match="不是 xlsx"):
        m.read_xlsx(b"not a zip file")


# ── 富邦 ─────────────────────────────────────────────────────────────────
def test_parse_fubon_assets():
    as_of, holdings = m.parse_fubon_assets(load_text("fubon_assets.html"), "00405A")
    assert as_of == "2026-09-24"
    assert len(holdings) == 5


def test_fubon_pcf_value():
    t = load_text("fubon_pcf.html")
    assert m._fubon_pcf_value(t, "受益人人數") == 160457.0


# ── 凱基 ─────────────────────────────────────────────────────────────────
def test_parse_kgi_detail():
    parsed = m.parse_kgi_detail(load_text("kgi_detail.html"), "00407A")
    assert parsed["as_of"] == "2026-09-24"
    assert len(parsed["holdings"]) == 5


def test_kgi_fund_map_from_dropdown():
    t = load_text("kgi_redemption.html").replace("<html><body>", "").replace("</body></html>", "")
    # 直接沿用模組內的 unescape+regex 邏輯(html.unescape 對純 ASCII 選單無影響)
    import html as html_mod
    fm = {name.strip(): fid for fid, name in m.KGI_OPTION_RE.findall(html_mod.unescape(load_text("kgi_redemption.html")))}
    assert fm.get("主動凱基台灣") == "J024"


# ── 第一金 ───────────────────────────────────────────────────────────────
def test_parse_firstsec_hd():
    rows = load_json("firstsec_get_hd.json")
    as_of, holdings, other = m.parse_firstsec_hd(rows, "00408A")
    assert as_of == "2026-09-24"
    assert len(holdings) == 5
    assert other and other[0]["type"] == "cash"


def test_parse_firstsec_meta():
    rows = load_json("firstsec_get_buysella.json")
    meta = m.parse_firstsec_meta(rows)
    assert meta["scale"] == 1485542179.0
    assert meta["units"] == 140134000.0


# ── 永豐 ─────────────────────────────────────────────────────────────────
def test_parse_sinopac_single_pcf():
    parsed = m.parse_sinopac_single_pcf(load_text("sinopac_singlepcf.html"), "00410A")
    assert parsed["as_of"] == "2026-09-24"
    assert len(parsed["holdings"]) == 5


# ── TWSE AUM/NAV/受益人數 ────────────────────────────────────────────────
def test_parse_twse_etf_info():
    row = m.parse_twse_etf_info(load_text("twse_etf_info.html"), "00980A")
    assert row["aum_100m_twd"] == 201.93
    assert row["holders_10k_people"] == 7.03
    assert row["as_of"] == "2026-09-24"


def test_parse_twse_etf_info_missing_raises():
    with pytest.raises(m.FetchError):
        m.parse_twse_etf_info("<html>no data here</html>", "00980A")


# ── normalize_fund + save_snapshot(端到端,無網路)───────────────────────
def test_normalize_fund_and_implied_other():
    m.FUND_REGISTRY.setdefault("00980A", {"name": "主動野村臺灣優選", "issuer": "野村", "adapter": "nomura"})
    raw = {
        "as_of": "2026-09-24",
        "holdings": [{"code": "2330", "name": "台積電", "shares": 90000, "weight_pct": 92.0},
                     {"code": "6223", "name": "旺矽", "shares": 1000, "weight_pct": 3.0}]
                    + [{"code": str(3000 + i), "name": "x", "shares": 100, "weight_pct": 0.1} for i in range(10)],
        "other": [],  # 端點未拆現金/期貨 → normalize_fund 應補一筆 implied unclassified
        "nav": {"scale": 1.0, "units": 1.0, "nav_per_unit": 1.0, "holders": 1.0},
        "source_url": "https://example.test/x",
    }
    twse, tpex = {"2330"}, {"6223"}
    normalized = m.normalize_fund("00980A", raw, twse, tpex)
    assert normalized["holdings"][0]["ticker"] == "2330.TW"
    assert normalized["holdings"][1]["ticker"] == "6223.TWO"
    assert normalized["other"][0]["type"] == "unclassified"
    stock_sum = sum(h["weight_pct"] for h in normalized["holdings"])
    assert abs(normalized["other"][0]["weight_pct"] - (100.0 - stock_sum)) < 1e-6


def test_normalize_fund_rejects_too_few_holdings():
    raw = {"as_of": "2026-09-24",
           "holdings": [{"code": "2330", "name": "台積電", "shares": 1, "weight_pct": 95.0}],
           "other": [], "nav": {}, "source_url": "x"}
    with pytest.raises(m.FetchError):
        m.normalize_fund("00980A", raw, set(), set())


def test_save_snapshot_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_DIR", tmp_path / "holdings")
    normalized = {"code": "00980A", "name": "x", "issuer": "野村", "as_of": "2026-09-24",
                  "holdings": [{"ticker": "2330.TW", "name": "台積電", "shares": 1, "weight_pct": 1.0}],
                  "other": [], "nav": {}, "source_url": "u", "fetched_at": "2026-09-24T09:00:00+08:00"}
    status1, path1 = m.save_snapshot(normalized)
    assert status1 == "written"
    assert path1.exists()
    # 同內容、不同 fetched_at(模擬同日重跑)→ 應判定 unchanged,不改寫檔案
    normalized2 = dict(normalized, fetched_at="2026-09-24T18:00:00+08:00")
    status2, path2 = m.save_snapshot(normalized2)
    assert status2 == "unchanged"
    assert path2 == path1
    # 內容真的變了(新增一檔持股)→ 應改寫
    normalized3 = dict(normalized, holdings=normalized["holdings"] + [
        {"ticker": "2454.TW", "name": "聯發科", "shares": 1, "weight_pct": 1.0}])
    status3, _ = m.save_snapshot(normalized3)
    assert status3 == "written"
