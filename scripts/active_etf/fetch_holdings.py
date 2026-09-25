#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日抓取台股掛牌主動式 ETF 的官方持股清單(PCF 申購買回清單 / 每日持股)。

範圍:22 檔台股主動式 ETF(00xxxA,第 6 碼 A=股票型主動式),涵蓋 15 家投信。
**不依賴任何第三方彙整站**——每家 fetcher 直接打投信官網/官方 API。各投信端點
是用 Chrome 網路檢視器 + 直接 curl/requests 探勘出來的(見各 fetch_* 函式開頭
說明);只在探勘階段讀過 github.com/nctuwanglin/active-etf 的原始碼以確認「這家
投信官方到底有哪個端點」,沒有引用或依賴它的程式或資料。

各投信「資料日」取自哪個欄位——這張表最容易踩坑,改 fetcher 前先看:
    野村/安聯    CNavDtStr / CNavDt          基準日(CPcfdate 是公告日,勿用)
    統一        pcf[0].TranDate             基準日
    群益        data.pcf.date2              基準日(date1 是公告日,勿用)
    中信        FundAssets[0].資料日期        基準日
    復華        result[0].dDate             基準日
    國泰        BuySale.preDateC            基準日(date 是公告生效日 T+1,勿用)
    兆豐        查詢日期之後那個日期          基準日(查詢日期本身是公告生效日)
    第一金      sdate                       基準日
    聯博        holdings 的 asOfDate        基準日(先取 basket.asOfDate 再帶入查詢)
    摩根        xlsx 表頭 (YYYY-MM-DD)       公告日;無獨立基準日欄位
    台新        NAV_DATE                    基準日(PUB_DATE 是公告生效日 T+1,勿用)
    富邦/永豐/凱基  頁面「資料日期/持股比重(日期)」  基準日

輸出正規化 schema(每檔一份):
    {code, name, issuer, as_of,
     holdings: [{ticker, name, shares, weight_pct}],   # ticker = "{代號}.TW"/".TWO"
     other: [{type, name, weight_pct}],                # 現金/期貨/其他,能拆出來的才拆
     nav: {scale, units, nav_per_unit, holders},        # 缺漏給 None
     source_url, fetched_at}

儲存:data/active_etf/holdings/{as_of}/{code}.json——以 PCF 自己的基準日為目錄,
同一天重跑內容不變就不改寫(idempotent)。

驗證:validate_holdings() 檔股數 ≥10、(持股+其他)權重合計落在 90-101%,任何一檔
失敗只讓該檔標記 failed,不中斷其他 21 檔(see main())。
"""
from __future__ import annotations

import argparse
import csv
import datetime
import html
import io
import json
import math
import re
import sys
import time
import zipfile
from pathlib import Path

import requests

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

REPO_ROOT = Path(__file__).resolve().parents[2]
HOLDINGS_DIR = REPO_ROOT / "data" / "active_etf" / "holdings"
AUM_DIR = REPO_ROOT / "data" / "active_etf" / "aum"

WEIGHT_SUM_MIN = 90.0
WEIGHT_SUM_MAX = 101.0
MIN_HOLDINGS = 10


class FetchError(Exception):
    """單檔 ETF 抓取/解析/驗證失敗。main() 捕捉後標 failed,不中斷整批。"""


# ── 22 檔標的 registry(代號→投信/官方全名,2026-09-25 由 TWSE STOCK_DAY_ALL 核對) ──
FUND_REGISTRY = {
    "00980A": {"name": "主動野村臺灣優選", "issuer": "野村", "adapter": "nomura"},
    "00981A": {"name": "主動統一台股增長", "issuer": "統一", "adapter": "president"},
    "00982A": {"name": "主動群益台灣強棒", "issuer": "群益", "adapter": "capital"},
    "00984A": {"name": "主動安聯台灣高息", "issuer": "安聯", "adapter": "allianz"},
    "00985A": {"name": "主動野村台灣50", "issuer": "野村", "adapter": "nomura"},
    "00987A": {"name": "主動台新優勢成長", "issuer": "台新", "adapter": "taishin"},
    "00991A": {"name": "主動復華未來50", "issuer": "復華", "adapter": "fuhhwa"},
    "00992A": {"name": "主動群益科技創新", "issuer": "群益", "adapter": "capital"},
    "00993A": {"name": "主動安聯台灣", "issuer": "安聯", "adapter": "allianz"},
    "00994A": {"name": "主動第一金台股優", "issuer": "第一金", "adapter": "firstsec"},
    "00995A": {"name": "主動中信台灣卓越", "issuer": "中信", "adapter": "ctbc"},
    "00996A": {"name": "主動兆豐台灣豐收", "issuer": "兆豐", "adapter": "megafunds"},
    "00999A": {"name": "主動野村臺灣高息", "issuer": "野村", "adapter": "nomura"},
    "00400A": {"name": "主動國泰動能高息", "issuer": "國泰", "adapter": "cathay"},
    "00401A": {"name": "主動摩根台灣鑫收", "issuer": "摩根", "adapter": "jpmorgan"},
    "00403A": {"name": "主動統一升級50", "issuer": "統一", "adapter": "president"},
    "00404A": {"name": "主動聯博動能50", "issuer": "聯博", "adapter": "ab"},
    "00405A": {"name": "主動富邦台灣龍耀", "issuer": "富邦", "adapter": "fubon"},
    "00406A": {"name": "主動中信台灣收益", "issuer": "中信", "adapter": "ctbc"},
    "00407A": {"name": "主動凱基台灣", "issuer": "凱基", "adapter": "kgi"},
    "00408A": {"name": "主動第一金優股息", "issuer": "第一金", "adapter": "firstsec"},
    "00410A": {"name": "主動永豐科技趨勢", "issuer": "永豐", "adapter": "sinopac"},
}


# ── HTTP 共用層 ──────────────────────────────────────────────────────────────
_session = None
_IMAGE_MAGIC = (b"\x89PNG", b"\xff\xd8\xff", b"GIF8")


def _get_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({"User-Agent": UA})
    return _session


def http_get(url, **kw):
    return _request("GET", url, **kw)


def http_post(url, **kw):
    return _request("POST", url, **kw)


def _request(method, url, **kw):
    s = _get_session()
    kw.setdefault("timeout", 30)
    last = None
    for attempt in range(3):
        try:
            r = s.request(method, url, **kw)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise FetchError("{} 抓取失敗: {}".format(url, last))


def is_bot_challenge(resp):
    """回應是圖片(而非預期的 JSON/HTML 資料)→ 站方的機器人驗證挑戰。"""
    body = resp.content[:8]
    return any(body.startswith(m) for m in _IMAGE_MAGIC)


def to_num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(",", "").replace("NT$", "").replace("TWD", "").replace("$", "").strip()
    if not s or s in ("-", "—", ""):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_dotnet_date(s):
    """'2026-08-04T00:00:00' 或 '/Date(1785772800000)/' → 'YYYY-MM-DD'(以台北時區解 ms epoch)。"""
    m = re.match(r"/Date\((\d+)\)/", s or "")
    if m:
        tz = datetime.timezone(datetime.timedelta(hours=8))
        dt = datetime.datetime.fromtimestamp(int(m.group(1)) / 1000, tz)
        return dt.strftime("%Y-%m-%d")
    return (s or "")[:10]


def roc_date(dt):
    return "{}/{:02d}/{:02d}".format(dt.year - 1911, dt.month, dt.day)


# ── 台股代號 → 上市(.TW)/上櫃(.TWO)分類 ──────────────────────────────────────
_market_codes_cache = None


def load_market_codes():
    """回傳 (twse_codes, tpex_codes) 兩個 set,供 ticker suffix 判斷用。

    來源:TWSE exchangeReport/STOCK_DAY_ALL(上市全部證券)、
    TPEx openapi/v1/tpex_mainboard_daily_close_quotes(上櫃股票)。皆為官方端點。
    """
    global _market_codes_cache
    if _market_codes_cache is not None:
        return _market_codes_cache
    twse_codes, tpex_codes = set(), set()
    try:
        r = http_get("https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL", timeout=30)
        rdr = csv.reader(io.StringIO(r.text))
        next(rdr, None)
        for row in rdr:
            if len(row) > 1 and row[1].strip():
                twse_codes.add(row[1].strip())
    except FetchError as e:
        print("警告: TWSE STOCK_DAY_ALL 抓取失敗,上市/上櫃判斷將 fallback 為 .TW ({})".format(e),
              file=sys.stderr)
    try:
        r = http_get("https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes", timeout=30)
        for row in r.json():
            code = (row.get("SecuritiesCompanyCode") or "").strip()
            if code:
                tpex_codes.add(code)
    except (FetchError, ValueError) as e:
        print("警告: TPEx 上櫃清單抓取失敗,上市/上櫃判斷將 fallback 為 .TW ({})".format(e),
              file=sys.stderr)
    _market_codes_cache = (twse_codes, tpex_codes)
    return _market_codes_cache


def ticker_for(code, twse_codes, tpex_codes):
    code = code.strip()
    if code in tpex_codes and code not in twse_codes:
        return code + ".TWO"
    return code + ".TW"  # 預設上市;查無資料時也 fallback 到 .TW


# ── 驗證 ─────────────────────────────────────────────────────────────────────
# 權重合計只驗「持股(股票)」這張表,**不含** other(現金/期貨/選擇權)。理由:
# 主動式 ETF 常見期貨/選擇權 overlay 是名目本金曝險,不是切分自 100% NAV 的一塊
# (實測 00404A 聯博:股票 90.22% + 台股期貨 overlay 15.43% + 選擇權 -0.24% =
# 105.41%,期貨部位讓合計「超過」100% 是正常的,不是解析錯誤)。若把 other 併入
# 合計驗證,90-101% 這個窄範圍會誤殺這種合法的槓桿 overlay,所以驗證範圍只套用在
# 股票持股本身——這與 nctuwanglin/active-etf 參考碼的驗證設計(只驗 holdings,
# 不含 other)一致,只是我們把範圍收更窄(90-101 vs 對方的 50-105)。
def validate_holdings(code, holdings, other):
    if len(holdings) < MIN_HOLDINGS:
        raise FetchError("{}: 持股僅 {} 檔,少於下限 {}".format(code, len(holdings), MIN_HOLDINGS))
    seen = set()
    for h in holdings:
        if not h["name"] or h["code"] in seen:
            raise FetchError("{}: 持股代號重複或空白 {}".format(code, h["code"]))
        seen.add(h["code"])
        if h["shares"] < 0 or h["weight_pct"] < 0 or h["weight_pct"] > 100:
            raise FetchError("{}: {} 股數/權重超出合理範圍".format(code, h["code"]))
        if not (math.isfinite(h["shares"]) and math.isfinite(h["weight_pct"])):
            raise FetchError("{}: {} 股數/權重非有限數值".format(code, h["code"]))
    total = sum(h["weight_pct"] for h in holdings)
    if not (WEIGHT_SUM_MIN <= total <= WEIGHT_SUM_MAX):
        raise FetchError("{}: 股票持股權重合計 {:.2f}% 超出 {}-{}% 範圍"
                          .format(code, total, WEIGHT_SUM_MIN, WEIGHT_SUM_MAX))


# ═════════════════════════════════════════════════════════════════════════════
# 野村(nomurafunds.com.tw)/ 安聯(etf.allianzgi.com.tw)—同一套 ETF 網站供應商,
# 端點名 GetFundTradeInfo 相同,差異見各自函式說明。
# ═════════════════════════════════════════════════════════════════════════════
NOMURA_TRADEINFO = "https://www.nomurafunds.com.tw/API/ETFAPI/api/Fund/GetFundTradeInfo"


def parse_nomura_entries(entries, code):
    """GetFundTradeInfo 的 Entries → dict,或 None(查無此日資料,供逐日往回試)。"""
    if not entries:
        return None
    rows = entries.get("Stocks") or []
    if not rows or not entries.get("CNavDtStr"):
        return None
    holdings = [{"code": str(r["CStockCode"]).strip(), "name": str(r["CStockName"]).strip(),
                 "shares": int(r["CQuantity"]), "weight_pct": float(r["CWeightsPct"])}
                for r in rows]
    return {
        "as_of": entries["CNavDtStr"].replace("/", "-"),
        "holdings": holdings,
        "other": [],  # 端點未拆出現金/期貨,見 normalize_fund() 的 implied-other 補算
        "nav": {"scale": to_num(entries.get("CAnceTotalAv")),
                "units": to_num(entries.get("CAnceTotalIssues")),
                "nav_per_unit": to_num(entries.get("CAnceNav")),
                "holders": to_num(entries.get("CBeneficiariesCount"))},
    }


def fetch_nomura(code):
    day = datetime.date.today()
    for back in range(8):
        q = (day - datetime.timedelta(days=back)).strftime("%Y-%m-%d")
        r = http_post(NOMURA_TRADEINFO, json={"Type": 1, "Keyword": "", "FundNo": code, "Date": q},
                      headers={"Content-Type": "application/json"})
        if is_bot_challenge(r):
            raise FetchError("nomura: {} 網站回機器人驗證圖,暫時無法取得".format(code))
        try:
            d = r.json()
        except ValueError:
            raise FetchError("nomura: {} 回非 JSON(改版?)".format(code))
        parsed = parse_nomura_entries(d.get("Entries"), code)
        if parsed:
            parsed["source_url"] = NOMURA_TRADEINFO
            return parsed
    raise FetchError("nomura: {} 連續 8 日無持股資料".format(code))


# ── 安聯:同野村供應商,但 base path 不同、需 anti-forgery token、持股在
#    DynamicTableData 通用表格,且有「股票」以外的表(現金/期貨),可拆出 other。
ALLIANZ_BASE = "https://etf.allianzgi.com.tw"
ALLIANZ_PAGE = ALLIANZ_BASE + "/list-trade"
ALLIANZ_TOKEN_URL = ALLIANZ_BASE + "/webapi/api/AntiForgery/GetAntiForgeryToken"
ALLIANZ_FUNDTYPES = ALLIANZ_BASE + "/webapi/api/Category/GetFundTypeDropdownOptions"
ALLIANZ_FUNDLIST = ALLIANZ_BASE + "/webapi/api/Category/GetFundDropdownOptions"
ALLIANZ_TRADEINFO = ALLIANZ_BASE + "/webapi/api/Fund/GetFundTradeInfo"

_allianz_token = None
_allianz_fund_map = None


def _allianz_headers():
    global _allianz_token
    if _allianz_token is None:
        http_get(ALLIANZ_PAGE)  # 建立 session cookie,token 與其綁定
        _allianz_token = http_get(ALLIANZ_TOKEN_URL).json()["token"]
    return {"Content-Type": "application/json", "X-XSRF-TOKEN": _allianz_token, "Referer": ALLIANZ_PAGE}


def _allianz_fund_map_load():
    global _allianz_fund_map
    if _allianz_fund_map is not None:
        return _allianz_fund_map
    hdr = _allianz_headers()
    types = http_post(ALLIANZ_FUNDTYPES, json={}, headers=hdr).json()
    type_id = None
    for e in types.get("Entries") or []:
        if "主動" in (e.get("Name") or ""):
            type_id = e["Id"]
    if type_id is None:
        raise FetchError("allianz: 基金類別找不到「主動式」(改版?)")
    funds = http_post(ALLIANZ_FUNDLIST, json={"TypeId": type_id}, headers=hdr).json()
    _allianz_fund_map = {(e.get("SecuritiesCode") or "").strip(): e["FundNo"]
                          for e in funds.get("Entries") or [] if (e.get("SecuritiesCode") or "").strip()}
    return _allianz_fund_map


def parse_allianz_entries(entries, code):
    if not entries:
        return None
    tables = entries.get("DynamicTableData") or []
    stock_tables = [t for t in tables if (t.get("TableTitle") or "").startswith("股票")]
    if not stock_tables or not entries.get("CNavDt"):
        return None
    holdings, other = [], []
    for t in tables:
        title = t.get("TableTitle") or ""
        is_stock = title.startswith("股票")
        for row in t.get("Rows") or []:
            if len(row) < 5:
                continue
            _, rcode, name, shares_s, weight_s = row[:5]
            weight = float(str(weight_s).rstrip("%"))
            if is_stock:
                holdings.append({"code": str(rcode).strip(), "name": str(name).strip(),
                                  "shares": int(str(shares_s).replace(",", "")), "weight_pct": weight})
            else:
                kind = "futures" if "期貨" in title else ("cash" if "現金" in title else "other")
                other.append({"type": kind, "name": str(name).strip(), "weight_pct": weight})
    if not holdings:
        return None
    return {
        "as_of": entries["CNavDt"][:10],
        "holdings": holdings,
        "other": other,
        "nav": {"scale": to_num(entries.get("CAnceTotalAv")),
                "units": to_num(entries.get("CAnceTotalIssues")),
                "nav_per_unit": to_num(entries.get("CAnceNav")),
                "holders": to_num(entries.get("CBeneficiariesCount"))},
    }


def fetch_allianz(code):
    fund_map = _allianz_fund_map_load()
    fund_no = fund_map.get(code)
    if not fund_no:
        raise FetchError("allianz: {} 不在基金清單".format(code))
    day = datetime.date.today()
    for back in range(8):
        q = (day - datetime.timedelta(days=back)).strftime("%Y-%m-%d")
        r = http_post(ALLIANZ_TRADEINFO, headers=_allianz_headers(),
                      json={"Type": 1, "Keyword": "", "FundNo": fund_no, "Date": q})
        try:
            d = r.json()
        except ValueError:
            raise FetchError("allianz: {} 回非 JSON(改版?)".format(code))
        parsed = parse_allianz_entries(d.get("Entries"), code)
        if parsed:
            parsed["source_url"] = ALLIANZ_TRADEINFO
            return parsed
    raise FetchError("allianz: {} 連續 8 日無持股資料".format(code))


# ═════════════════════════════════════════════════════════════════════════════
# 統一(ezmoney.com.tw)
# ═════════════════════════════════════════════════════════════════════════════
PRESIDENT_PCF_PAGE = "https://www.ezmoney.com.tw/ETF/Transaction/PCF"
PRESIDENT_GETPCF = "https://www.ezmoney.com.tw/ETF/Transaction/GetPCF"
_president_fund_map = None


def parse_president_fund_map(page_html):
    m = re.search(r"id=['\"]DataFundList['\"][^>]*data-content=['\"](.*?)['\"]", page_html, re.S)
    if not m:
        raise FetchError("president: PCF 頁找不到 DataFundList(改版?)")
    funds = json.loads(html.unescape(m.group(1)))
    return {(f.get("sStockNo") or "").strip(): f["sFundCode"] for f in funds if f.get("sStockNo")}


def parse_president_pcf(d, code):
    stock_assets = [a for a in d.get("asset", []) if a.get("AssetCode") == "ST"]
    if not stock_assets or not stock_assets[0].get("Details"):
        raise FetchError("{}: GetPCF 無股票明細".format(code))
    holdings = [{"code": str(r["DetailCode"]), "name": str(r["DetailName"]),
                 "shares": int(r["Share"]), "weight_pct": float(r["NavRate"])}
                for r in stock_assets[0]["Details"]]
    other = []
    for a in d.get("asset", []):
        if a.get("AssetCode") == "ST":
            continue
        kind = "futures" if "期貨" in (a.get("AssetName") or "") else "other"
        for r in a.get("Details") or []:
            other.append({"type": kind, "name": str(r.get("DetailName") or a.get("AssetName") or "").strip(),
                           "weight_pct": float(r.get("NavRate") or 0)})
    pcf = d.get("pcf") or []
    if not pcf:
        raise FetchError("{}: GetPCF 無 pcf 摘要(資料日不明)".format(code))
    amt = {r.get("PCFCode"): r.get("Amount") for r in pcf}
    return {
        "as_of": parse_dotnet_date(pcf[0]["TranDate"]),
        "holdings": holdings,
        "other": other,
        "nav": {"scale": to_num(amt.get("NAV")), "units": to_num(amt.get("OUT_UNIT")),
                "nav_per_unit": to_num(amt.get("P_UNIT")), "holders": to_num(amt.get("NAV_PEOPLE"))},
    }


def fetch_president(code):
    global _president_fund_map
    if _president_fund_map is None:
        _president_fund_map = parse_president_fund_map(http_get(PRESIDENT_PCF_PAGE).text)
    if code not in _president_fund_map:
        raise FetchError("president: {} 不在 fundList".format(code))
    query_date = roc_date(datetime.date.today() + datetime.timedelta(days=3))
    r = http_post(PRESIDENT_GETPCF, json={"fundCode": _president_fund_map[code], "date": query_date,
                                           "specificDate": False},
                  headers={"Referer": PRESIDENT_PCF_PAGE})
    try:
        d = r.json()
    except ValueError:
        raise FetchError("president: {} GetPCF 回非 JSON".format(code))
    parsed = parse_president_pcf(d, code)
    parsed["source_url"] = PRESIDENT_GETPCF
    return parsed


# ═════════════════════════════════════════════════════════════════════════════
# 群益(capitalfund.com.tw)
# ═════════════════════════════════════════════════════════════════════════════
CAPITAL_ITEMS = "https://www.capitalfund.com.tw/CFWeb/api/etf/items"
CAPITAL_BUYBACK = "https://www.capitalfund.com.tw/CFWeb/api/etf/buyback"
_capital_fund_map = None


def parse_capital_buyback(d, code):
    data = d.get("data") or {}
    stocks = data.get("stocks") or []
    pcf = data.get("pcf") or {}
    if not stocks or not pcf.get("date2"):
        raise FetchError("{}: buyback 無持股/資料日".format(code))
    holdings = [{"code": str(x["stocNo"]), "name": str(x["stocName"]).strip(),
                 "shares": int(x["share"]), "weight_pct": float(x["weight"])}
                for x in stocks]
    return {
        "as_of": pcf["date2"],
        "holdings": holdings,
        "other": [],
        "nav": {"scale": to_num(pcf.get("nav")), "units": to_num(pcf.get("totUnit")),
                "nav_per_unit": to_num(pcf.get("pUnit")), "holders": to_num(pcf.get("numberPeople"))},
    }


def fetch_capital(code):
    global _capital_fund_map
    if _capital_fund_map is None:
        r = http_post(CAPITAL_ITEMS, json={}, headers={"Content-Type": "application/json"})
        try:
            d = r.json()
        except ValueError:
            raise FetchError("capital: items 回非 JSON")
        _capital_fund_map = {(f.get("stockNo") or "").strip(): f["fundNo"]
                              for f in d.get("data", []) if f.get("stockNo")}
    if code not in _capital_fund_map:
        raise FetchError("capital: {} 不在 items".format(code))
    r = http_post(CAPITAL_BUYBACK, json={"fundId": _capital_fund_map[code]},
                  headers={"Content-Type": "application/json"})
    try:
        d = r.json()
    except ValueError:
        raise FetchError("capital: {} buyback 回非 JSON".format(code))
    parsed = parse_capital_buyback(d, code)
    parsed["source_url"] = CAPITAL_BUYBACK
    return parsed


# ═════════════════════════════════════════════════════════════════════════════
# 台新(tsit.com.tw)—server-rendered HTML,ETF 代號即網址參數。
# ═════════════════════════════════════════════════════════════════════════════
TAISHIN_DETAIL = "https://www.tsit.com.tw/ETF/Home/ETFSeriesDetail/{}"
TAISHIN_ROW_RE = re.compile(
    r"<tr>\s*<td>\s*([0-9A-Z]{1,8}(?:\s+[A-Z]{2})?)\s*</td>\s*<td>\s*([^<]+?)\s*</td>"
    r"\s*<td>\s*([\d,]+)\s*</td>\s*<td>\s*([\d.]+)%\s*</td>")
TAISHIN_NAV_DATE_RE = re.compile(r'id="NAV_DATE"[^>]*value="([^"]+)"')


def _taishin_normalize_code(raw):
    raw = raw.strip()
    return raw[:-3].strip() if raw.endswith(" TT") else raw


def _taishin_meta_value(plain, label):
    m = re.search(re.escape(label) + r"\s*(?:TWD)?\s*([\d,]+(?:\.\d+)?)", plain)
    return to_num(m.group(1)) if m else None


def parse_taishin_detail(page_html, code):
    t = html.unescape(page_html)
    m = TAISHIN_NAV_DATE_RE.search(t)
    if not m:
        raise FetchError("{}: 台新頁面找不到 NAV_DATE(改版?)".format(code))
    dm = re.match(r"\s*(\d{4})/(\d{1,2})/(\d{1,2})", m.group(1))
    if not dm:
        raise FetchError("{}: 台新 NAV_DATE 格式非預期".format(code))
    y, mo, d = dm.groups()
    as_of = "{}-{:02d}-{:02d}".format(y, int(mo), int(d))
    i = t.find("股數")  # 股票表表頭;其前為期貨表(欄位是「口數」,結構不同,不併入)
    seg = t[i:] if i >= 0 else t
    holdings = [{"code": _taishin_normalize_code(c), "name": n,
                 "shares": int(s.replace(",", "")), "weight_pct": float(w)}
                for c, n, s, w in TAISHIN_ROW_RE.findall(seg)]
    plain = re.sub(r"<[^>]+>", " ", t)
    return {
        "as_of": as_of,
        "holdings": holdings,
        "other": [],  # 期貨表格式與股票表不同(口數非股數),暫不併入,詳見上方註解
        "nav": {"scale": _taishin_meta_value(plain, "基金淨資產價值(元)"),
                "units": _taishin_meta_value(plain, "已發行受益權單位總數"),
                "nav_per_unit": _taishin_meta_value(plain, "每受益權單位淨資產價值(元)"),
                "holders": None},
    }


def fetch_taishin(code):
    r = http_get(TAISHIN_DETAIL.format(code))
    parsed = parse_taishin_detail(r.text, code)
    parsed["source_url"] = TAISHIN_DETAIL.format(code)
    return parsed


# ═════════════════════════════════════════════════════════════════════════════
# 復華(fhtrust.com.tw)
# ═════════════════════════════════════════════════════════════════════════════
FUHHWA_FUNDLIST = "https://www.fhtrust.com.tw/api/fundList?ec001=3"
FUHHWA_ASSETS = "https://www.fhtrust.com.tw/api/assets"
_fuhhwa_fund_map = None


def parse_fuhhwa_assets(d, code):
    results = d.get("result") or []
    if not results:
        return None
    r = results[0]
    detail = r.get("detail") or []
    stock_rows = [x for x in detail if x.get("ftype") == "股票" and (x.get("stockid") or "").strip()]
    if not stock_rows or not r.get("dDate"):
        return None
    holdings = [{"code": x["stockid"], "name": x["stockname"],
                 "shares": int(x["qshare"].replace(",", "")), "weight_pct": float(x["prate_addaccint"].rstrip("%"))}
                for x in stock_rows]
    other = []
    for x in detail:
        if x.get("ftype") != "股票":
            kind = "futures" if "期貨" in (x.get("ftype") or "") else "cash" if "現金" in (x.get("ftype") or "") else "other"
            w = to_num(str(x.get("prate_addaccint", "")).rstrip("%"))
            if w is not None:
                other.append({"type": kind, "name": str(x.get("stockname") or x.get("ftype")).strip(), "weight_pct": w})
    return {
        "as_of": r["dDate"].replace("/", "-"),
        "holdings": holdings,
        "other": other,
        "nav": {"scale": to_num(r.get("pcf_FundNav")), "units": to_num(r.get("pcf_FundQissue")),
                "nav_per_unit": to_num(r.get("pcf_Fundpnav")), "holders": None},
    }


def fetch_fuhhwa(code):
    global _fuhhwa_fund_map
    if _fuhhwa_fund_map is None:
        _fuhhwa_fund_map = {(f.get("etf002") or "").strip(): f["fundID"]
                             for f in http_get(FUHHWA_FUNDLIST).json().get("result", []) if f.get("etf002")}
    if code not in _fuhhwa_fund_map:
        raise FetchError("fuhhwa: {} 不在 fundList".format(code))
    fund_id = _fuhhwa_fund_map[code]
    day = datetime.date.today()
    for back in range(8):
        q = (day - datetime.timedelta(days=back)).strftime("%Y/%m/%d")
        d = http_get(FUHHWA_ASSETS, params={"fundID": fund_id, "qDate": q}).json()
        parsed = parse_fuhhwa_assets(d, code)
        if parsed:
            parsed["source_url"] = FUHHWA_ASSETS
            return parsed
    raise FetchError("fuhhwa: {} 連續 8 日無持股資料".format(code))


# ═════════════════════════════════════════════════════════════════════════════
# 中信(ctbcinvestments.com.tw)
# ═════════════════════════════════════════════════════════════════════════════
CTBC_AUTH = "https://www.ctbcinvestments.com.tw/API/home/AuthToken"
CTBC_ETFLIST = "https://www.ctbcinvestments.com.tw/API/etf/ETFList"
CTBC_HOLDING = "https://www.ctbcinvestments.com.tw/API/etf/ETFHoldingWeight"
_ctbc_token = None
_ctbc_fund_map = None


def _ctbc_decode(resp):
    d = resp.json()
    return json.loads(d) if isinstance(d, str) else d


def fetch_ctbc(code):
    global _ctbc_token, _ctbc_fund_map
    if _ctbc_token is None:
        d = _ctbc_decode(http_post(CTBC_AUTH, params={"token": "www.ctbcinvestments.com"}, json={}))
        _ctbc_token = d["Data"]["token"]
    if _ctbc_fund_map is None:
        d = _ctbc_decode(http_post(CTBC_ETFLIST, params={"token": _ctbc_token}, json={}))
        rows = d["Data"]["Data"] if isinstance(d.get("Data"), dict) else d.get("Data", [])
        _ctbc_fund_map = {r["ETF_ID"]: r["FID"] for r in rows if r.get("ETF_ID")}
    if code not in _ctbc_fund_map:
        raise FetchError("ctbc: {} 不在 ETFList".format(code))
    fid = _ctbc_fund_map[code]
    day = datetime.date.today()
    for back in range(8):
        q = (day - datetime.timedelta(days=back)).strftime("%Y/%m/%d")
        d = _ctbc_decode(http_post(CTBC_HOLDING, params={"token": _ctbc_token}, json={"FID": fid, "StartDate": q}))
        parsed = parse_ctbc_holding(d, code)
        if parsed:
            parsed["source_url"] = CTBC_HOLDING
            return parsed
    raise FetchError("ctbc: {} 連續 8 日無持股資料".format(code))


def parse_ctbc_holding(d, code):
    if d.get("ResultCode") != 0:
        return None
    data = d.get("Data") or {}
    assets = data.get("FundAssets") or []
    groups = data.get("FundAssetsDetail") or []
    stock_group = next((g for g in groups if g.get("Code") == "STOCK"), None)
    rows = stock_group.get("Data") or [] if stock_group else []
    if not assets or not rows:
        return None
    holdings = [{"code": str(r["code_"]).strip(), "name": str(r["name_"]).strip(),
                 "shares": int(float(r["qty_"].replace(",", ""))), "weight_pct": float(r["weights_"])}
                for r in rows]
    other = []
    for g in groups:
        if g.get("Code") == "STOCK":
            continue
        kind = "cash" if g.get("Code") == "CASH" else "futures" if g.get("Code") in ("MARGIN", "FUTURES") else "other"
        for r in g.get("Data") or []:
            w = to_num(r.get("weights_"))
            if w is not None:
                other.append({"type": kind, "name": str(r.get("name_") or g.get("Code")).strip(), "weight_pct": w})
    a = assets[0]
    return {
        "as_of": a["資料日期"].replace("/", "-"),
        "holdings": holdings,
        "other": other,
        "nav": {"scale": to_num(a.get("基金淨資產")), "units": to_num(a.get("基金在外流通單位數")),
                "nav_per_unit": to_num(a.get("基金每單位淨值")), "holders": None},
    }


# ═════════════════════════════════════════════════════════════════════════════
# 兆豐(megafunds.com.tw)—ASP.NET WebForms,基金切換是 POST 回原頁(viewstate)。
# ═════════════════════════════════════════════════════════════════════════════
MEGAFUNDS_URL = "https://www.megafunds.com.tw/MEGA/etf/trade_pcf.aspx"
MEGAFUNDS_PREFIX = "ctl00$ContentPlaceHolder1$"
MEGAFUNDS_HIDDEN_RE = re.compile(r'<input[^>]*type="hidden"[^>]*name="([^"]+)"[^>]*value="([^"]*)"')
MEGAFUNDS_OPTION_BLOCK_RE = re.compile(
    r'name="' + re.escape(MEGAFUNDS_PREFIX) + r'fund_id"[^>]*>(.*?)</select>', re.S)
MEGAFUNDS_ROW_RE = re.compile(
    r'<tr class="tr-stock">\s*<td[^>]*>\s*([0-9A-Z]{4,6})\s*</td>\s*'
    r'<td[^>]*>\s*([^<]+?)\s*</td>\s*<td[^>]*>\s*([\d,]+)\s*</td>\s*'
    r'<td[^>]*>\s*([\d.]+)%\s*</td>')
MEGAFUNDS_QUERY_DATE_RE = re.compile(r"查詢日期[^0-9]{0,40}(\d{4}/\d{2}/\d{2})")
MEGAFUNDS_DATE_RE = re.compile(r"\d{4}/\d{2}/\d{2}")


def parse_megafunds_fund_map(page_html):
    t = html.unescape(page_html)
    m = MEGAFUNDS_OPTION_BLOCK_RE.search(t)
    if not m:
        raise FetchError("megafunds: 找不到基金下拉(改版?)")
    return {name.strip(): val for val, name in
            re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)</option>', m.group(1)) if name.strip()}


def parse_megafunds_result(page_html, code):
    t = html.unescape(page_html)
    if code not in t:
        raise FetchError("{}: 兆豐結果頁不含此代號(基金對照錯誤?)".format(code))
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
    m = MEGAFUNDS_QUERY_DATE_RE.search(plain)
    if not m:
        raise FetchError("{}: 找不到查詢日期(改版?)".format(code))
    after = MEGAFUNDS_DATE_RE.findall(plain[m.end():m.end() + 1200])
    as_of = (after[0] if after else m.group(1)).replace("/", "-")
    holdings = [{"code": c, "name": n, "shares": int(s.replace(",", "")), "weight_pct": float(w)}
                for c, n, s, w in MEGAFUNDS_ROW_RE.findall(t)]

    def val(label):
        mm = re.search(re.escape(label) + r"\s*(?:TWD\$)?\s*([\d,]+(?:\.\d+)?)", plain)
        return to_num(mm.group(1)) if mm else None

    return {
        "as_of": as_of,
        "holdings": holdings,
        "other": [],
        "nav": {"scale": val("基金淨資產價值(元)"), "units": val("已發行受益權單位總數"),
                "nav_per_unit": val("每受益權單位淨資產價值(元)"), "holders": None},
    }


def fetch_megafunds(code):
    name = FUND_REGISTRY[code]["name"]
    page = http_get(MEGAFUNDS_URL).text
    fund_map = parse_megafunds_fund_map(page)
    base = name[2:] if name.startswith("主動") else name
    fund_id = next((fid for opt_name, fid in fund_map.items() if opt_name.startswith(base)), None)
    if not fund_id:
        raise FetchError("megafunds: {}「{}」不在基金下拉".format(code, name))
    data = dict(MEGAFUNDS_HIDDEN_RE.findall(page))
    data[MEGAFUNDS_PREFIX + "category_id"] = ""
    data[MEGAFUNDS_PREFIX + "fund_id"] = fund_id
    data[MEGAFUNDS_PREFIX + "button1"] = "查 詢"
    r = http_post(MEGAFUNDS_URL, data=data, headers={"Referer": MEGAFUNDS_URL})
    parsed = parse_megafunds_result(r.text, code)
    parsed["source_url"] = MEGAFUNDS_URL
    return parsed


# ═════════════════════════════════════════════════════════════════════════════
# 國泰(cathaysite.com.tw)—股數是由「每基數股數 × 流通基數」還原,兩個數字都是
# 官方公告值,見模組內 fetch_cathay 說明。
# ═════════════════════════════════════════════════════════════════════════════
CATHAY_BASE = "https://cwapi.cathaysite.com.tw/api/"
CATHAY_ETF_LIST = CATHAY_BASE + "ETF/GetETFList"
CATHAY_BUYSALE = CATHAY_BASE + "BuySale/GetBuySale"
CATHAY_STOCKS = CATHAY_BASE + "BuySale/GetStocksList"
CATHAY_WEIGHTS = CATHAY_BASE + "ETF/GetIndexStockWeights"
_cathay_fund_map = None


def _cathay_result(resp, what):
    try:
        d = resp.json()
    except ValueError:
        raise FetchError("cathay: {} 回非 JSON".format(what))
    if not d.get("success"):
        raise FetchError("cathay: {} 失敗 {}".format(what, d.get("returnMessage")))
    return d.get("result")


def build_cathay_holdings(stocks, weight_rows, baskets, code):
    """basketShares(每基數股數,官方公告值) × baskets(流通基數) → 總股數,併上官方權重。

    國泰只公告「每基數股數」,不是總持股;總股數 = basketShares × (totUnit /
    basketUnit) 是 PCF 的標準還原方式,不是估計——兩個輸入都是官方公告值。"""
    wmap = {r["stockCode"]: to_num(r["weights"]) for r in weight_rows}
    holdings = []
    for r in stocks:
        stock_code = str(r["prod"]).strip()
        if stock_code not in wmap:
            continue
        basket_shares = to_num(r["basketShares"])
        if basket_shares is None:
            continue
        holdings.append({"code": stock_code, "name": str(r["prodName"]).strip(),
                          "shares": int(round(basket_shares * baskets)), "weight_pct": wmap[stock_code]})
    if not holdings:
        raise FetchError("{}: 國泰 PCF 與權重表無交集(參數或改版?)".format(code))
    return holdings


def fetch_cathay(code):
    global _cathay_fund_map
    if _cathay_fund_map is None:
        rows = _cathay_result(http_get(CATHAY_ETF_LIST, params={"FundType": "", "PerPageCount": 9999, "status": 1}),
                               "GetETFList")
        rows = rows if isinstance(rows, list) else (rows or {}).get("list") or []
        _cathay_fund_map = {(r.get("stockCode") or "").strip(): r["fundCode"]
                             for r in rows if r.get("stockCode") and r.get("fundCode")}
    fund_code = _cathay_fund_map.get(code)
    if not fund_code:
        raise FetchError("cathay: {} 不在 GetETFList".format(code))
    bs = _cathay_result(http_get(CATHAY_BUYSALE, params={"FundCode": fund_code, "IsTest": "false", "status": 1}),
                         "GetBuySale")
    tot, basket = to_num(bs.get("totUnit")), to_num(bs.get("basketUnit"))
    if not (tot and basket):
        raise FetchError("{}: 國泰 PCF 缺流通單位數/基數,無法還原股數".format(code))
    stocks = _cathay_result(http_get(CATHAY_STOCKS, params={"FundCode": fund_code, "SearchDate": bs["date"],
                                                              "IsTest": "false", "status": 1}), "GetStocksList") or []
    w = _cathay_result(http_get(CATHAY_WEIGHTS, params={"fundCode": fund_code, "status": 1}),
                        "GetIndexStockWeights") or {}
    weight_rows = w.get("stockWeights") or []
    if not stocks or not weight_rows:
        raise FetchError("{}: 國泰 PCF 成分股或權重表為空".format(code))
    holdings = build_cathay_holdings(stocks, weight_rows, tot / basket, code)
    as_of = (bs.get("preDateC") or w.get("date") or "").replace("/", "-")
    if not as_of:
        raise FetchError("{}: 國泰取不到基準日".format(code))
    return {
        "as_of": as_of,
        "holdings": holdings,
        "other": [],
        "nav": {"scale": to_num(bs.get("aum")), "units": tot, "nav_per_unit": to_num(bs.get("nav")),
                "holders": to_num(bs.get("benefiCount"))},
        "source_url": CATHAY_BUYSALE,
    }


# ═════════════════════════════════════════════════════════════════════════════
# 聯博(webapi.alliancebernstein.com)—以 ISIN 當基金識別,ISIN 由代號直接算出。
# ═════════════════════════════════════════════════════════════════════════════
AB_BASE = "https://webapi.alliancebernstein.com/v2/funds/tw/zh-tw/investor/{}"
AB_EQUITY = "holdings-section-equity"


def isin_check_digit(body):
    digits = "".join(str(int(c, 36)) for c in body)
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return str((10 - total % 10) % 10)


def isin_for(code):
    body = "TW000" + code
    return body + isin_check_digit(body)


def parse_ab_holdings(payload, code):
    sections = [s for s in (payload.get("domesticHoldings") or []) if s.get("holdingCategory") == AB_EQUITY]
    if not sections:
        raise FetchError("{}: 聯博 holdings 無 equity 分段".format(code))
    sec = sections[0]
    holdings = []
    for r in sec.get("holdings") or []:
        stock_code = str(r.get("holdingCode") or "").strip()
        shares, weight = to_num(r.get("holdingShares")), to_num(r.get("holdingPerc"))
        if not stock_code or shares is None or weight is None:
            continue
        holdings.append({"code": stock_code, "name": str(r.get("holding") or "").strip(),
                          "shares": int(shares), "weight_pct": weight})
    d = (sec.get("asOfDate") or "").strip()  # 'MM/DD/YYYY'
    parts = d.split("/")
    if len(parts) != 3:
        raise FetchError("{}: 聯博 holdings 日期格式非預期 {!r}".format(code, d))
    as_of = "{}-{}-{}".format(parts[2], parts[0], parts[1])
    other = []
    for s in (payload.get("domesticHoldings") or []):
        if s.get("holdingCategory") == AB_EQUITY:
            continue
        kind = "futures" if "futures" in (s.get("holdingCategory") or "") else "other"
        for r in s.get("holdings") or []:
            w = to_num(r.get("holdingPerc"))
            if w is not None:
                other.append({"type": kind, "name": str(r.get("holding") or s.get("holdingCategory")).strip(),
                              "weight_pct": w})
    return as_of, holdings, other


def fetch_ab(code):
    isin = isin_for(code)
    base = AB_BASE.format(isin)
    try:
        basket = http_get(base + "/basket").json()
    except ValueError:
        raise FetchError("ab: {} basket 回非 JSON".format(code))
    as_of_q = (basket.get("asOfDate") or "").strip()
    params = {"date": as_of_q} if as_of_q else None
    try:
        payload = http_get(base + "/holdings", params=params).json()
    except ValueError:
        raise FetchError("ab: {} holdings 回非 JSON".format(code))
    as_of, holdings, other = parse_ab_holdings(payload, code)
    return {
        "as_of": as_of, "holdings": holdings, "other": other,
        "nav": {"scale": to_num(basket.get("aum")), "units": to_num(basket.get("shares")),
                "nav_per_unit": to_num(basket.get("nav")), "holders": None},
        "source_url": base + "/holdings",
    }


# ═════════════════════════════════════════════════════════════════════════════
# 摩根(am.jpmorgan.com)—唯一只給 xlsx 下載的投信;xlsx 以 zipfile+regex 直解
# (xlsx 本質是 zip 包 XML),不為一家投信多裝 openpyxl 相依。
# ═════════════════════════════════════════════════════════════════════════════
JPMORGAN_EXCEL = "https://am.jpmorgan.com/FundsMarketingHandler/excel"
JPMORGAN_REFERER = "https://am.jpmorgan.com/tw/zh/asset-management/twetf/"

_JP_ROW_RE = re.compile(r"<row[^>]*>(.*?)</row>", re.S)
_JP_CELL_RE = re.compile(r'<c\b([^>]*?)(?:/>|>(.*?)</c>)', re.S)
_JP_VAL_RE = re.compile(r"<v>(.*?)</v>", re.S)
_JP_SI_RE = re.compile(r"<si>(.*?)</si>", re.S)
_JP_T_RE = re.compile(r"<t[^>]*>(.*?)</t>", re.S)
_JP_TITLE_DATE_RE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")
_JP_STOCK_CODE_RE = re.compile(r"^[0-9A-Z]{4,6}$")


def read_xlsx(blob):
    try:
        z = zipfile.ZipFile(io.BytesIO(blob))
    except zipfile.BadZipFile:
        raise FetchError("jpmorgan: 回應不是 xlsx(參數不全時會回錯誤頁)")
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        xml = z.read("xl/sharedStrings.xml").decode("utf-8", "replace")
        shared = [html.unescape("".join(_JP_T_RE.findall(si))) for si in _JP_SI_RE.findall(xml)]
    sheets = {}
    for name in sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet")):
        rows = []
        for row in _JP_ROW_RE.findall(z.read(name).decode("utf-8", "replace")):
            cells = []
            for attrs, inner in _JP_CELL_RE.findall(row):
                if 't="inlineStr"' in attrs:
                    # 部分 xlsx 產生器(如 openpyxl 預設)用行內字串而非 sharedStrings
                    val = html.unescape("".join(_JP_T_RE.findall(inner or "")))
                else:
                    v = _JP_VAL_RE.search(inner or "")
                    val = v.group(1) if v else ""
                    if 't="s"' in attrs and val.isdigit() and int(val) < len(shared):
                        val = shared[int(val)]
                cells.append(val)
            rows.append(cells)
        sheets[name] = rows
    return sheets


def parse_jpmorgan_holdings_xlsx(sheets, code):
    for rows in sheets.values():
        title = rows[0][0] if rows and rows[0] else ""
        if "股票" not in title:
            continue
        m = _JP_TITLE_DATE_RE.search(title)
        if not m:
            continue
        hdr = next((i for i, r in enumerate(rows) if r and r[0] == "股票代碼"), None)
        if hdr is None:
            continue
        holdings = []
        for r in rows[hdr + 1:]:
            if len(r) < 5 or not _JP_STOCK_CODE_RE.match((r[0] or "").strip()):
                continue
            shares, weight = to_num(r[2]), to_num(str(r[4]).replace("%", ""))
            if shares is None or weight is None:
                continue
            holdings.append({"code": r[0].strip(), "name": (r[1] or "").strip(),
                              "shares": int(shares), "weight_pct": weight})
        if holdings:
            return m.group(1), holdings
    raise FetchError("{}: 摩根 xlsx 找不到股票表(改版?)".format(code))


def parse_jpmorgan_meta_xlsx(sheets):
    kv = {}
    for rows in sheets.values():
        for r in rows:
            if len(r) >= 2 and r[0] and r[1]:
                kv[str(r[0])] = r[1]

    def pick(label):
        for k, v in kv.items():
            if label in k:
                return to_num(v)
        return None

    return {"scale": pick("基金淨資產價值"), "units": pick("已發行受益權單位總數"),
            "nav_per_unit": pick("每受益權單位淨資產價值"), "holders": None}


def _jpmorgan_download(isin, kind, date):
    r = http_get(JPMORGAN_EXCEL, params={"type": kind, "cusip": isin, "country": "tw", "role": "twetf",
                                          "locale": "zh-TW", "date": date}, headers={"Referer": JPMORGAN_REFERER})
    return r.content


def fetch_jpmorgan(code):
    isin = isin_for(code)
    today = datetime.date.today()
    holdings = as_of = None
    for back in range(8):
        d = (today - datetime.timedelta(days=back)).strftime("%Y-%m-%d")
        try:
            as_of, holdings = parse_jpmorgan_holdings_xlsx(read_xlsx(_jpmorgan_download(isin, "holding_pcf", d)), code)
            break
        except FetchError:
            continue
    if not holdings:
        raise FetchError("jpmorgan: {} 連續 8 日取不到 holding_pcf".format(code))
    meta = None
    for fwd in range(6):
        d = (today + datetime.timedelta(days=fwd)).strftime("%Y-%m-%d")
        try:
            meta = parse_jpmorgan_meta_xlsx(read_xlsx(_jpmorgan_download(isin, "m12_pcf", d)))
            if meta.get("scale"):
                break
        except FetchError:
            continue
    return {"as_of": as_of, "holdings": holdings, "other": [], "nav": meta or {},
            "source_url": JPMORGAN_EXCEL}


# ═════════════════════════════════════════════════════════════════════════════
# 富邦(websys.fsit.com.tw)
# ═════════════════════════════════════════════════════════════════════════════
FUBON_ASSETS_URL = "https://websys.fsit.com.tw/FubonETF/Trade/Assets.aspx"
FUBON_PCF_URL = "https://websys.fsit.com.tw/FubonETF/Trade/Pcf.aspx"
FUBON_ROW_RE = re.compile(
    r'<tr>\s*<td class="tac">([0-9A-Z]{4,6})</td>\s*<td>([^<]+)</td>'
    r'\s*<td class="tar">([\d,]+)</td>\s*<td class="tar">[\d,.-]+</td>'
    r'\s*<td class="tar">([\d.]+)</td>')
FUBON_DATE_RE = re.compile(r"資料日期：(\d{4}/\d{2}/\d{2})")


def parse_fubon_assets(page_html, code):
    m = FUBON_DATE_RE.search(page_html)
    if not m:
        raise FetchError("{}: 富邦資產頁找不到資料日期(改版?)".format(code))
    holdings = [{"code": c, "name": n, "shares": int(s.replace(",", "")), "weight_pct": float(w)}
                for c, n, s, w in FUBON_ROW_RE.findall(page_html)]
    return m.group(1).replace("/", "-"), holdings


def _fubon_pcf_value(page_html, label):
    m = re.search(re.escape(label) + r"[^<]*</p>\s*<p>([^<]+)</p>", page_html)
    return to_num(m.group(1)) if m else None


def fetch_fubon(code):
    r = http_get(FUBON_ASSETS_URL, params={"stkId": code, "lan": "TW"})
    as_of, holdings = parse_fubon_assets(r.text, code)
    try:
        pcf_html = http_get(FUBON_PCF_URL, params={"stkId": code, "lan": "TW"}).text
        nav = {"scale": _fubon_pcf_value(pcf_html, "基金淨資產價值"),
               "units": _fubon_pcf_value(pcf_html, "已發行受益權單位總數"),
               "nav_per_unit": _fubon_pcf_value(pcf_html, "每受益權單位淨資產價值"),
               "holders": _fubon_pcf_value(pcf_html, "受益人人數")}
    except FetchError:
        nav = {}
    return {"as_of": as_of, "holdings": holdings, "other": [], "nav": nav, "source_url": FUBON_ASSETS_URL}


# ═════════════════════════════════════════════════════════════════════════════
# 凱基(kgifund.com.tw)—純 server-rendered HTML,不需 session/token。
# ═════════════════════════════════════════════════════════════════════════════
KGI_REDEMPTION = "https://www.kgifund.com.tw/Fund/RedemptionList"
KGI_DETAIL = "https://www.kgifund.com.tw/Fund/Detail"
KGI_ROW_RE = re.compile(
    r'<tr name="content"[^>]*>\s*<td[^>]*>\s*([0-9A-Z]{4,6})\s*</td>\s*'
    r'<td[^>]*>\s*([^<]+?)\s*</td>\s*<td[^>]*>\s*([\d,]+)\s*</td>\s*'
    r'<td[^>]*>\s*([\d.]+)\s*</td>')
KGI_DATE_RE = re.compile(r"持股比重(?:<[^>]*>|\s)*\((\d{4}/\d{2}/\d{2})\)")
KGI_OPTION_RE = re.compile(r'<option[^>]*value="([A-Z0-9]+)"[^>]*>([^<]+)</option>')
_kgi_fund_map = None


def _kgi_meta_value(plain, label):
    m = re.search(re.escape(label) + r"\s*(?:TWD\$)?\s*([\d,]+(?:\.\d+)?)", plain)
    return to_num(m.group(1)) if m else None


def parse_kgi_detail(page_html, code):
    t = html.unescape(page_html)
    m = KGI_DATE_RE.search(t)
    if not m:
        raise FetchError("{}: 凱基頁面找不到「持股比重 (日期)」(改版?)".format(code))
    as_of = m.group(1).replace("/", "-")
    first = t.find("股票代號")
    second = t.find("股票代號", first + 1)
    seg = t[first:second] if second > 0 else t[first:]  # 頁面有桌機/行動兩份相同表,只取第一份
    holdings = [{"code": c, "name": n, "shares": int(s.replace(",", "")), "weight_pct": float(w)}
                for c, n, s, w in KGI_ROW_RE.findall(seg)]
    plain = re.sub(r"<[^>]+>", " ", t)
    return {
        "as_of": as_of, "holdings": holdings, "other": [],
        "nav": {"scale": _kgi_meta_value(plain, "基金淨值資產價值"), "units": _kgi_meta_value(plain, "基金在外流通單位數"),
                "nav_per_unit": _kgi_meta_value(plain, "基金每單位淨值"), "holders": None},
    }


def fetch_kgi(code):
    global _kgi_fund_map
    if _kgi_fund_map is None:
        t = html.unescape(http_get(KGI_REDEMPTION).text)
        _kgi_fund_map = {name.strip(): fid for fid, name in KGI_OPTION_RE.findall(t) if name.strip()}
    name = FUND_REGISTRY[code]["name"]
    fund_id = _kgi_fund_map.get(name)
    if not fund_id:
        raise FetchError("kgi: {} 名稱「{}」不在基金下拉清單".format(code, name))
    r = http_get(KGI_DETAIL, params={"fundID": fund_id})
    parsed = parse_kgi_detail(r.text, code)
    parsed["source_url"] = KGI_DETAIL + "?fundID=" + fund_id
    return parsed


# ═════════════════════════════════════════════════════════════════════════════
# 第一金(fsitc.com.tw)—ASP.NET WebForms + jQuery WebMethod,雙層 JSON 編碼。
# fund_id 已知(2026-09-25 查證):00408A=183、00994A=182,寫死避免每次反查掃描。
# ═════════════════════════════════════════════════════════════════════════════
FIRSTSEC_WEBAPI = "https://www.fsitc.com.tw/WebAPI.aspx/"
FIRSTSEC_DETAIL = "https://www.fsitc.com.tw/FundDetail.aspx"
FIRSTSEC_FUND_IDS = {"00408A": "183", "00994A": "182"}


def _firstsec_call(method, fund_id, date=""):
    r = http_post(FIRSTSEC_WEBAPI + method, json={"pStrFundID": str(fund_id), "pStrDate": date},
                  headers={"Content-Type": "application/json; charset=utf-8",
                           "Referer": "{}?ID={}".format(FIRSTSEC_DETAIL, fund_id)})
    try:
        d = r.json()
        return json.loads(d["d"])
    except (ValueError, KeyError, TypeError):
        raise FetchError("firstsec: {} 回應非預期格式".format(method))


def parse_firstsec_hd(rows, code):
    stocks = [r for r in rows if str(r.get("group")) == "1" and (r.get("A") or "").strip()]
    if not stocks:
        raise FetchError("{}: 第一金 Get_hd 無股票明細".format(code))
    holdings = []
    for r in stocks:
        shares, weight = to_num(r.get("D")), to_num(r.get("C"))
        if shares is None or weight is None:
            continue
        holdings.append({"code": str(r["A"]).strip(), "name": str(r["B"]).strip(),
                          "shares": int(shares), "weight_pct": weight})
    other = []
    for r in rows:
        if str(r.get("group")) == "4":  # 現金/存款
            w = to_num(r.get("C"))
            if w is not None:
                other.append({"type": "cash", "name": str(r.get("A") or "現金").strip(), "weight_pct": w})
    as_of = (stocks[0].get("sdate") or "").strip()
    if not as_of:
        raise FetchError("{}: 第一金 Get_hd 無資料日".format(code))
    return as_of[:10], holdings, other


def parse_firstsec_meta(rows):
    kv = {(r.get("A") or "").strip(): r.get("B") for r in rows}

    def pick(*labels):
        for k, v in kv.items():
            if any(k.startswith(l) for l in labels):
                return to_num(v)
        return None

    return {"scale": pick("基金淨資產價值"), "units": pick("已發行受益權單位總數"),
            "nav_per_unit": pick("每受益權單位淨資產價值"), "holders": None}


def fetch_firstsec(code):
    fund_id = FIRSTSEC_FUND_IDS.get(code)
    if not fund_id:
        raise FetchError("firstsec: {} 無已知 fund_id(需到 FundDetail.aspx 查出並補進 FIRSTSEC_FUND_IDS)".format(code))
    as_of, holdings, other = parse_firstsec_hd(_firstsec_call("Get_hd", fund_id), code)
    try:
        meta = parse_firstsec_meta(_firstsec_call("Get_BuySellA", fund_id))
    except FetchError:
        meta = {}
    return {"as_of": as_of, "holdings": holdings, "other": other, "nav": meta,
            "source_url": FIRSTSEC_DETAIL + "?ID=" + fund_id}


# ═════════════════════════════════════════════════════════════════════════════
# 永豐(sitc.sinopac.com)—server-rendered HTML,ETF 代號即網址參數。
# ═════════════════════════════════════════════════════════════════════════════
SINOPAC_SINGLE_PCF = "https://sitc.sinopac.com/SinopacEtfs/Etfs/SinglePcf/{}"
SINOPAC_ROW_RE = re.compile(
    r"<tr>\s*<td>\s*([0-9A-Z]{4,6})\s*</td>\s*<td>\s*([^<]+?)\s*</td>\s*"
    r"<td>\s*([\d,]+)\s*</td>\s*<td>\s*([\d.]+)\s*</td>")
SINOPAC_DATE_RE = re.compile(r"資料日期：\s*(\d{4}/\d{2}/\d{2})")


def _sinopac_all_values(plain, label):
    return [to_num(v) for v in re.findall(re.escape(label) + r"\s*(?:NT\$)?\s*([\d,]+(?:\.\d+)?)", plain)]


def _sinopac_pick_scale(candidates, units, nav):
    candidates = [c for c in candidates if c]
    if not candidates:
        return None
    if not (units and nav):
        return candidates[0]
    expected = units * nav
    return min(candidates, key=lambda c: abs(c - expected))


def parse_sinopac_single_pcf(page_html, code):
    t = html.unescape(page_html)
    m = SINOPAC_DATE_RE.search(t)
    if not m:
        raise FetchError("{}: 永豐頁面找不到「資料日期」(改版?)".format(code))
    as_of = m.group(1).replace("/", "-")
    heads = [x.start() for x in re.finditer("證券代碼", t)]
    if not heads:
        raise FetchError("{}: 永豐頁面找不到持股表(改版?)".format(code))
    seg = t[heads[0]:heads[1]] if len(heads) > 1 else t[heads[0]:]
    holdings = [{"code": c, "name": n, "shares": int(s.replace(",", "")), "weight_pct": float(w)}
                for c, n, s, w in SINOPAC_ROW_RE.findall(seg)]
    plain = re.sub(r"<[^>]+>", " ", t)
    units = (_sinopac_all_values(plain, "已發行受益權單位總數") or [None])[0]
    nav = (_sinopac_all_values(plain, "每受益權單位淨資產價值(元)") or [None])[0]
    return {
        "as_of": as_of, "holdings": holdings, "other": [],
        "nav": {"scale": _sinopac_pick_scale(_sinopac_all_values(plain, "基金淨資產價值(元)"), units, nav),
                "units": units, "nav_per_unit": nav, "holders": None},
    }


def fetch_sinopac(code):
    r = http_get(SINOPAC_SINGLE_PCF.format(code))
    parsed = parse_sinopac_single_pcf(r.text, code)
    parsed["source_url"] = SINOPAC_SINGLE_PCF.format(code)
    return parsed


# ═════════════════════════════════════════════════════════════════════════════
ADAPTERS = {
    "nomura": fetch_nomura, "allianz": fetch_allianz, "president": fetch_president,
    "capital": fetch_capital, "taishin": fetch_taishin, "fuhhwa": fetch_fuhhwa,
    "ctbc": fetch_ctbc, "megafunds": fetch_megafunds, "cathay": fetch_cathay,
    "ab": fetch_ab, "jpmorgan": fetch_jpmorgan, "fubon": fetch_fubon, "kgi": fetch_kgi,
    "firstsec": fetch_firstsec, "sinopac": fetch_sinopac,
}


# ── 正規化 + 儲存 ─────────────────────────────────────────────────────────────
def normalize_fund(code, raw, twse_codes, tpex_codes):
    """raw(各 fetch_* 回傳)→ 任務規格的正規化 schema,並驗證。"""
    info = FUND_REGISTRY[code]
    holdings = [{"ticker": ticker_for(h["code"], twse_codes, tpex_codes), "name": h["name"],
                 "shares": h["shares"], "weight_pct": round(h["weight_pct"], 4)}
                for h in raw["holdings"]]
    other = [{"type": o["type"], "name": o["name"], "weight_pct": round(o["weight_pct"], 4)}
             for o in raw.get("other", [])]
    validate_holdings(code, raw["holdings"], raw.get("other", []))
    # 來源沒拆出現金/期貨的(other 為空)且股票權重合計未滿 99.5%,補一筆「implied
    # unclassified」讓 100% 分解一致;不是官方公告的細項,只是「還沒被拆出來的那塊」。
    stock_sum = sum(h["weight_pct"] for h in holdings)
    if not other and stock_sum < 99.5:
        other = [{"type": "unclassified", "name": "現金/期貨/其他(來源未逐項揭露)",
                   "weight_pct": round(100.0 - stock_sum, 4)}]
    return {
        "code": code, "name": info["name"], "issuer": info["issuer"],
        "as_of": raw["as_of"], "holdings": holdings, "other": other,
        "nav": raw.get("nav") or {}, "source_url": raw.get("source_url"),
        "fetched_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }


def save_snapshot(normalized):
    """存到 data/active_etf/holdings/{as_of}/{code}.json;內容與已存檔案相同就跳過(idempotent)。"""
    day_dir = HOLDINGS_DIR / normalized["as_of"]
    day_dir.mkdir(parents=True, exist_ok=True)
    path = day_dir / "{}.json".format(normalized["code"])
    comparable = {k: v for k, v in normalized.items() if k != "fetched_at"}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            existing_comparable = {k: v for k, v in existing.items() if k != "fetched_at"}
            if existing_comparable == comparable:
                return "unchanged", path
        except (json.JSONDecodeError, OSError):
            pass
    path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return "written", path


# ── TWSE AUM / NAV / 受益人數(ETF e添富) ────────────────────────────────────
TWSE_ETF_INFO = "https://www.twse.com.tw/zh/ETFortune/etfInfo/{}"


def parse_twse_etf_info(page_html, code):
    t = page_html
    m_aum = re.search(r"資產規模\(億元\)\s*</p>\s*<span>([\d.,]+)</span>", t)
    m_holders = re.search(r"受益人次\(萬人\)\s*</p>\s*<span>([\d.,]+)</span>", t)
    m_date = re.search(r"資料日期：(\d{4}-\d{2}-\d{2})", t)
    if not (m_aum or m_holders):
        raise FetchError("{}: TWSE ETF e添富頁找不到資產規模/受益人次(改版?)".format(code))
    return {
        "code": code,
        "aum_100m_twd": to_num(m_aum.group(1)) if m_aum else None,
        "holders_10k_people": to_num(m_holders.group(1)) if m_holders else None,
        "as_of": m_date.group(1) if m_date else None,
        "source_url": TWSE_ETF_INFO.format(code),
    }


def fetch_twse_aum(code):
    r = http_get(TWSE_ETF_INFO.format(code))
    return parse_twse_etf_info(r.text, code)


# ── main ─────────────────────────────────────────────────────────────────────
def run(codes=None, skip_aum=False, pace_sec=1.5):
    codes = codes or list(FUND_REGISTRY)
    twse_codes, tpex_codes = load_market_codes()
    results = []
    for code in codes:
        info = FUND_REGISTRY[code]
        adapter = ADAPTERS[info["adapter"]]
        try:
            raw = adapter(code)
            normalized = normalize_fund(code, raw, twse_codes, tpex_codes)
            status, path = save_snapshot(normalized)
            stock_sum = sum(h["weight_pct"] for h in normalized["holdings"])
            other_sum = sum(o["weight_pct"] for o in normalized["other"])
            results.append({
                "code": code, "issuer": info["issuer"], "adapter": info["adapter"],
                "status": status, "as_of": normalized["as_of"], "n_holdings": len(normalized["holdings"]),
                "stock_weight_pct": round(stock_sum, 2), "other_weight_pct": round(other_sum, 2),
                "path": str(path.relative_to(REPO_ROOT)), "error": None,
            })
            print("OK   {} ({} {}): as_of={} n={} stock_wt={:.2f}% other_wt={:.2f}% [{}]".format(
                code, info["issuer"], info["adapter"], normalized["as_of"], len(normalized["holdings"]),
                stock_sum, other_sum, status))
        except FetchError as e:
            results.append({"code": code, "issuer": info["issuer"], "adapter": info["adapter"],
                             "status": "failed", "error": str(e)})
            print("FAIL {} ({} {}): {}".format(code, info["issuer"], info["adapter"], e), file=sys.stderr)

    if not skip_aum:
        aum_rows = []
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        for i, code in enumerate(FUND_REGISTRY):
            try:
                aum_rows.append(fetch_twse_aum(code))
                print("AUM  {}: {}".format(code, aum_rows[-1]))
            except FetchError as e:
                print("AUM FAIL {}: {}".format(code, e), file=sys.stderr)
            if i < len(FUND_REGISTRY) - 1:
                time.sleep(pace_sec)
        AUM_DIR.mkdir(parents=True, exist_ok=True)
        (AUM_DIR / "{}.json".format(today_str)).write_text(
            json.dumps(aum_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", help="逗號分隔的代號子集,如 00980A,00981A")
    ap.add_argument("--skip-aum", action="store_true", help="跳過 TWSE AUM/受益人數抓取")
    args = ap.parse_args()
    codes = [c.strip() for c in args.only.split(",")] if args.only else None
    if codes:
        for c in codes:
            if c not in FUND_REGISTRY:
                ap.error("未知代號: {}".format(c))
    results = run(codes=codes, skip_aum=args.skip_aum)
    n_ok = sum(1 for r in results if r["status"] in ("written", "unchanged"))
    n_fail = sum(1 for r in results if r["status"] == "failed")
    print("\n完成: {} 成功, {} 失敗".format(n_ok, n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
