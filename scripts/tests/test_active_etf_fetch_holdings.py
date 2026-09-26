"""Unit tests for scripts/active_etf/fetch_holdings.py — one parser test per
issuer, using small fixtures modeled on each issuer's real PCF/holdings
response (captured 2026-09-24/25 from the official endpoints themselves,
then trimmed to ~5 holdings). No network access; no dependency on any
third-party aggregator's data or code.
"""
from __future__ import annotations

import datetime
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


# ── HTTP 共用層(headers / 403 重試 / 雙向掃描)───────────────────────────
def test_get_session_sends_browser_like_headers(monkeypatch):
    monkeypatch.setattr(m, "_session", None)
    s = m._get_session()
    assert s.headers["User-Agent"] == m.UA
    assert "zh-TW" in s.headers["Accept-Language"]


class _FakeResp:
    def __init__(self, status_code=200, json_data=None, content=b"{}"):
        self.status_code = status_code
        self._json = json_data
        self.content = content

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise m.requests.HTTPError("HTTP {}".format(self.status_code))


class _FakeSession:
    """依序回傳 responses 清單,每呼叫一次 request() 吐一個。"""
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def request(self, method, url, **kw):
        r = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        return r


def test_request_retries_403_then_succeeds(monkeypatch):
    # 403 常見於暫時性 WAF 擋一次,值得退避重試(而非像其他 4xx 立即當「這天真的
    # 沒資料」放棄)——見 _request() 對 403 的特別處理。
    fake = _FakeSession([_FakeResp(403), _FakeResp(200, json_data={"ok": True})])
    monkeypatch.setattr(m, "_get_session", lambda: fake)
    monkeypatch.setattr(m.time, "sleep", lambda *_a, **_k: None)
    r = m.http_get("https://example.test/x")
    assert r.json() == {"ok": True}
    assert fake.calls == 2


def test_request_403_exhausted_raises_fetch_error(monkeypatch):
    fake = _FakeSession([_FakeResp(403)] * 4)
    monkeypatch.setattr(m, "_get_session", lambda: fake)
    monkeypatch.setattr(m.time, "sleep", lambda *_a, **_k: None)
    with pytest.raises(m.FetchError, match="403"):
        m.http_get("https://example.test/x")


def test_request_404_fails_immediately_without_retry(monkeypatch):
    # 其他 4xx(如摩根對查不到的歷史日期回 404)維持原行為:立即拋錯、不重試——
    # 這代表「這個查詢真的沒有」,不是暫時性擋一次,重試只會拖慢 backfill。
    fake = _FakeSession([_FakeResp(404)] * 4)
    monkeypatch.setattr(m, "_get_session", lambda: fake)
    monkeypatch.setattr(m.time, "sleep", lambda *_a, **_k: None)
    with pytest.raises(m.FetchError, match="404"):
        m.http_get("https://example.test/x")
    assert fake.calls == 1


# ── _scan_latest(雙向掃描,取基準日最新一筆)────────────────────────────
def test_scan_latest_finds_freshest_across_holiday_gap():
    """2026-09-26(週六,中秋+教師節連假中)實測:野村/安聯只往回找只能拿到基準
    日 09-23,但下一個有效交易日(09-29)這個 key 已經提前生成好基準日 09-24 的
    資料——只往回掃會漏掉這筆更新的,兩個方向都要掃才拿得到真正最新的。"""
    data = {
        "2026-09-23": {"as_of": "2026-09-22"},
        "2026-09-24": {"as_of": "2026-09-23"},
        "2026-09-29": {"as_of": "2026-09-24"},
    }
    best = m._scan_latest(lambda q: data.get(q), today=datetime.date(2026, 9, 26))
    assert best["as_of"] == "2026-09-24"


def test_scan_latest_normal_day_no_gap():
    data = {"2026-09-22": {"as_of": "2026-09-21"}}
    best = m._scan_latest(lambda q: data.get(q), today=datetime.date(2026, 9, 22))
    assert best["as_of"] == "2026-09-21"


def test_scan_latest_no_hits_returns_none():
    assert m._scan_latest(lambda q: None, today=datetime.date(2026, 9, 26)) is None


def test_scan_latest_prefers_already_published_next_key_over_stale_today():
    """深夜重跑的情境:「今天」這個 key 昨晚就已經生成(基準日=前一天),但如果
    今天收盤後、當下已經過了公告時間,「下一個有效交易日」這個 key 可能也已經
    生成(基準日=今天)——比「今天」這個 key 還新,不能只取掃描到的第一筆。"""
    data = {
        "2026-09-22": {"as_of": "2026-09-21"},  # 今天:昨晚已生成,基準日=昨天
        "2026-09-23": {"as_of": "2026-09-22"},  # 明天:今晚已生成,基準日=今天(更新)
    }
    best = m._scan_latest(lambda q: data.get(q), today=datetime.date(2026, 9, 22))
    assert best["as_of"] == "2026-09-22"


# ── validate_holdings ────────────────────────────────────────────────────
def _h(code, weight, shares=1000):
    return {"code": code, "name": "測試", "shares": shares, "weight_pct": weight}


def test_validate_holdings_ok():
    holdings = [_h(str(1000 + i), 5.0) for i in range(19)] + [_h("9999", 5.0)]
    stock_pct, low_equity = m.validate_holdings("TEST", holdings, [])  # 20*5=100%,不拋錯
    assert stock_pct == 100.0
    assert low_equity is False


def test_validate_holdings_too_few():
    with pytest.raises(m.FetchError, match="少於下限"):
        m.validate_holdings("TEST", [_h("1000", 50.0)], [])


def test_validate_holdings_weight_out_of_range():
    # 股票權重合計 40% < 90% 下限,strict=True(預設,daily run 用)一樣硬性失敗
    holdings = [_h(str(1000 + i), 4.0) for i in range(10)]
    with pytest.raises(m.FetchError, match="超出"):
        m.validate_holdings("TEST", holdings, [])


def test_validate_holdings_low_equity_warns_only_when_not_strict():
    """2026-09 回填時發現的真實現金緩衝低點(00980A/00984A/00991A/00993A/00981A
    Feb-Aug 2026,股票權重 82-89%)不該被 backfill 當成解析錯誤丟掉——strict=False
    (backfill_fund 專用)只回傳 low_equity=True,不拋錯;still 存檔。"""
    holdings = [_h(str(1000 + i), 4.0) for i in range(10)]  # 40%,遠低於任何合理下限
    stock_pct, low_equity = m.validate_holdings("TEST", holdings, [], strict=False)
    assert stock_pct == 40.0
    assert low_equity is True


def test_validate_holdings_ceiling_still_hard_fails_when_not_strict():
    # 上限(band_max)永遠是硬性失敗,不受 strict 影響——這代表資料真的壞了
    # (weights sum > 101%),不是合法的現金緩衝狀態。
    holdings = [_h(str(1000 + i), 15.0) for i in range(10)]  # 150%
    with pytest.raises(m.FetchError, match="上限"):
        m.validate_holdings("TEST", holdings, [], strict=False)


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
    assert parsed["pcf_date"] == d["Entries"]["CPcfdate"][:10]  # 公告生效日(T+1),僅供對照
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
    assert parsed["pcf_date"] == d["Entries"]["CPcfdate"][:10]  # 公告生效日(T+1),僅供對照
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
    assert parsed["pcf_date"] == d["data"]["pcf"]["date1"]  # 公告生效日,僅供對照
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


def test_parse_taishin_detail_extracts_pub_date_as_pcf_date():
    # fixture 本身沒有 PUB_DATE(2026-09-24/25 抓取時網頁上未必帶出這欄),用真實
    # 頁面會有的 hidden input 格式補一段驗證抽取邏輯——PUB_DATE 是公告生效日
    # (T+1),NAV_DATE 才是基準日,兩者不可互換(見模組頂 docstring 表格)。
    html_with_pub_date = load_text("taishin_detail.html").replace(
        'id="NAV_DATE" value="2026/9/23 上午 12:00:00"',
        'id="NAV_DATE" value="2026/9/23 上午 12:00:00" /><input type="hidden" '
        'id="PUB_DATE" value="2026-09-24"')
    parsed = m.parse_taishin_detail(html_with_pub_date, "00987A")
    assert parsed["as_of"] == "2026-09-23"
    assert parsed["pcf_date"] == "2026-09-24"


def test_parse_taishin_detail_pcf_date_none_when_pub_date_absent():
    parsed = m.parse_taishin_detail(load_text("taishin_detail.html"), "00987A")
    assert parsed["pcf_date"] is None


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
    assert parsed["pcf_date"] == "2026-09-29"
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
        "pcf_date": "2026-09-29",
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
    assert normalized["pcf_date"] == "2026-09-29"  # 公告生效日隨 raw 帶入,不影響 as_of(基準日)
    stock_sum = sum(h["weight_pct"] for h in normalized["holdings"])
    assert abs(normalized["other"][0]["weight_pct"] - (100.0 - stock_sum)) < 1e-6


def test_normalize_fund_pcf_date_defaults_none_when_source_lacks_it():
    """摩根等來源只有一個日期欄位(見模組頂 docstring 表格)——raw 沒帶 pcf_date
    時 normalize_fund 不應報錯,留 None(不是缺漏,是該來源本來就沒有這欄)。"""
    m.FUND_REGISTRY.setdefault("00980A", {"name": "主動野村臺灣優選", "issuer": "野村", "adapter": "nomura"})
    raw = {"as_of": "2026-09-24",
           "holdings": [{"code": str(1000 + i), "name": "x", "shares": 1, "weight_pct": 9.0} for i in range(11)],
           "other": [], "nav": {}, "source_url": "u"}
    normalized = m.normalize_fund("00980A", raw, set(), set())
    assert normalized["pcf_date"] is None


def test_normalize_fund_rejects_too_few_holdings():
    raw = {"as_of": "2026-09-24",
           "holdings": [{"code": "2330", "name": "台積電", "shares": 1, "weight_pct": 95.0}],
           "other": [], "nav": {}, "source_url": "x"}
    with pytest.raises(m.FetchError):
        m.normalize_fund("00980A", raw, set(), set())


def test_append_snapshot_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_DIR", tmp_path / "holdings")
    monkeypatch.setattr(m, "NAMES_PATH", tmp_path / "ticker_names.json")
    normalized = {"code": "00980A", "name": "x", "issuer": "野村", "as_of": "2026-09-24",
                  "holdings": [{"ticker": "2330.TW", "name": "台積電", "shares": 1, "weight_pct": 1.0}],
                  "other": [], "nav": {}, "source_url": "u", "weight_band_note": None,
                  "fetched_at": "2026-09-24T09:00:00+08:00"}
    status1, path1 = m.append_snapshot(normalized)
    assert status1 == "written"
    assert path1.exists()
    assert path1.name == "00980A.jsonl"
    # normalized 沒帶 pcf_date(舊呼叫端/來源沒有這欄)→ 存檔應是 None,不報錯,
    # 向下相容(見 append_snapshot 對 normalized.get("pcf_date") 的處理)。
    first_line = json.loads(path1.read_text(encoding="utf-8").splitlines()[0])
    assert first_line["pcf_date"] is None
    # 同內容、不同 fetched_at(模擬同日重跑)→ 應判定 unchanged,不新增行
    normalized2 = dict(normalized, fetched_at="2026-09-24T18:00:00+08:00")
    status2, path2 = m.append_snapshot(normalized2)
    assert status2 == "unchanged"
    assert path2 == path1
    assert len(path1.read_text(encoding="utf-8").splitlines()) == 1
    # 內容真的變了(新增一檔持股,as_of 也是新的一天)→ 應新增一行
    normalized3 = dict(normalized, as_of="2026-09-25", holdings=normalized["holdings"] + [
        {"ticker": "2454.TW", "name": "聯發科", "shares": 1, "weight_pct": 1.0}])
    status3, _ = m.append_snapshot(normalized3)
    assert status3 == "written"
    assert len(path1.read_text(encoding="utf-8").splitlines()) == 2


# ── 個別基金權重容許帶 ───────────────────────────────────────────────────
def test_weight_band_for_special_funds():
    assert m.weight_band_for("00985A")[:2] == (80.0, 101.0)
    assert m.weight_band_for("00406A")[:2] == (60.0, 101.0)
    assert m.weight_band_for("00980A")[:2] == (75.0, 101.0)
    assert m.weight_band_for("00999A")[:2] == (75.0, 101.0)
    assert m.weight_band_for("00985A")[2] is not None  # note 有值
    # 00981A 不在特例表中 → 用全域預設
    assert m.weight_band_for("00981A") == (m.WEIGHT_SUM_MIN, m.WEIGHT_SUM_MAX, None)


def test_validate_holdings_uses_per_fund_band():
    # 00406A 帶下限 60%,89.74% 的 00985A 若套用它自己的帶(80%)應通過
    holdings = [_h(str(1000 + i), 8.974) for i in range(10)]  # 合計 89.74%
    m.validate_holdings("00985A", holdings, [])  # 不拋錯(80-101 範圍內)
    with pytest.raises(m.FetchError):
        m.validate_holdings("00981A", holdings, [])  # 全域帶 90-101,89.74% 應失敗


# ── compact/expand 往返 ──────────────────────────────────────────────────
def test_compact_expand_holdings_roundtrip():
    holdings = [{"ticker": "2330.TW", "name": "台積電", "shares": 90000, "weight_pct": 8.05}]
    rows = m.compact_holdings(holdings)
    assert rows == [["2330.TW", 90000, 8.05]]
    expanded = m.expand_holdings(rows, {"2330.TW": "台積電"})
    assert expanded == holdings


def test_compact_expand_other_roundtrip():
    other = [{"type": "cash", "name": "現金", "weight_pct": 1.2}]
    rows = m.compact_other(other)
    assert rows == [["cash", "現金", 1.2]]
    assert m.expand_other(rows) == other


def test_read_fund_jsonl_missing_file_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_DIR", tmp_path / "holdings")
    assert m.read_fund_jsonl("00980A") == []


def test_read_fund_jsonl_backward_compatible_with_old_lines_missing_pcf_date(tmp_path, monkeypatch):
    """既有 jsonl(在加 pcf_date 欄位之前寫的)沒有這個 key,讀取不該報錯——
    只是額外一個 key,舊行沒有就是沒有,呼叫端用 .get("pcf_date") 拿 None。"""
    monkeypatch.setattr(m, "HOLDINGS_DIR", tmp_path / "holdings")
    path = m._fund_jsonl_path("00980A")
    path.parent.mkdir(parents=True, exist_ok=True)
    old_line = {"as_of": "2026-08-01", "holdings": [["2330.TW", 1, 1.0]], "other": [],
                "nav": {}, "source_url": "u", "fetched_at": "2026-08-01T09:00:00+08:00"}
    path.write_text(json.dumps(old_line, ensure_ascii=False) + "\n", encoding="utf-8")
    rows = m.read_fund_jsonl("00980A")
    assert len(rows) == 1
    assert rows[0].get("pcf_date") is None


def test_update_ticker_names_merges_and_persists(tmp_path, monkeypatch):
    names_path = tmp_path / "ticker_names.json"
    monkeypatch.setattr(m, "NAMES_PATH", names_path)
    m.update_ticker_names([{"ticker": "2330.TW", "name": "台積電"}])
    assert json.loads(names_path.read_text(encoding="utf-8")) == {"2330.TW": "台積電"}
    m.update_ticker_names([{"ticker": "2454.TW", "name": "聯發科"}])
    d = json.loads(names_path.read_text(encoding="utf-8"))
    assert d == {"2330.TW": "台積電", "2454.TW": "聯發科"}  # 舊值保留,新值併入


# ── 遷移(migrate_legacy_holdings)──────────────────────────────────────────
def test_migrate_legacy_holdings(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_DIR", tmp_path / "holdings")
    monkeypatch.setattr(m, "NAMES_PATH", tmp_path / "ticker_names.json")
    day_dir = tmp_path / "holdings" / "2026-09-24"
    day_dir.mkdir(parents=True)
    old = {"code": "00980A", "name": "主動野村臺灣優選", "issuer": "野村", "as_of": "2026-09-24",
           "holdings": [{"ticker": "2330.TW", "name": "台積電", "shares": 1, "weight_pct": 95.0}],
           "other": [], "nav": {}, "source_url": "u", "fetched_at": "2026-09-24T09:00:00+08:00"}
    (day_dir / "00980A.json").write_text(json.dumps(old, ensure_ascii=False), encoding="utf-8")
    migrated = m.migrate_legacy_holdings()
    assert migrated == [("00980A", "2026-09-24")]
    assert not day_dir.exists()  # 舊目錄遷移完應被刪除
    rows = m.read_fund_jsonl("00980A")
    assert len(rows) == 1 and rows[0]["as_of"] == "2026-09-24"


# ── 回補歷史(backfill_fund)──────────────────────────────────────────────
def test_backfill_fund_unsupported_adapter_is_noop(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_DIR", tmp_path / "holdings")
    n, earliest = m.backfill_fund("00982A", pace_sec=0)  # capital,不在 BACKFILL_SUPPORTED
    assert (n, earliest) == (0, None)


def test_backfill_fund_walks_back_until_miss(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "HOLDINGS_DIR", tmp_path / "holdings")
    monkeypatch.setattr(m, "NAMES_PATH", tmp_path / "ticker_names.json")
    monkeypatch.setattr(m, "load_market_codes", lambda: ({"2330"}, set()))
    today = datetime.date.today()
    good_dates = {(today - datetime.timedelta(days=d)).isoformat() for d in range(1, 4)}

    def fake_fetch(code, target_date=None):
        if target_date not in good_dates:
            return None
        # 每天權重故意不同,確保 3 天的內容互不相同(才會各自 append 成一行——
        # backfill_fund 跟 append_snapshot 用同一套「內容不變就不重複寫」邏輯)。
        base = list(good_dates).index(target_date) * 0.01
        holdings = [{"code": str(1000 + i), "name": "x", "shares": 1, "weight_pct": 9.5 + base} for i in range(10)]
        return {"as_of": target_date, "holdings": holdings, "other": [], "nav": {}, "source_url": "u"}

    monkeypatch.setitem(m.ADAPTERS, "nomura", fake_fetch)
    n, earliest = m.backfill_fund("00980A", pace_sec=0, max_consecutive_miss=2)
    assert n == 3
    rows = m.read_fund_jsonl("00980A")
    assert len(rows) == 3
    assert earliest == min(good_dates)
