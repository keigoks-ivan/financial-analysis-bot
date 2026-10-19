#!/usr/bin/env python3
"""ishares_us.py — iShares 美國官網持股檔（EWY／EWM／EWZ／IEV）的下載、解析與代號轉換。

2026-10-19 加。端點：
  https://www.ishares.com/us/products/{id}/{slug}/latest-holdings.csv
純 requests.get＋一般 User-Agent，回 text/plain。注意：同一產品頁底下另一條
`...ajax?fileType=csv&...` 回的是 HTML 頁面（content-type 卻也標 csv），所以
驗證一律看檔頭文字與欄位，不看 content-type。

檔案格式：前幾行是基金資訊（第 2 行 `Fund Holdings as of,"Oct 15, 2026"`），
標題列含 Ticker／Name／Sector／Asset Class／Market Value／Weight (%)／…／
Location／Exchange／Currency／FX Rate／Market Currency。Asset Class 不是
Equity 的列（現金、期貨、匯率部位）歸 non_equity。

這份持股檔給的是各國交易所自己的代號（韓國 6 位數字、馬來西亞 Bursa 簡稱、
巴西 B3 代號、歐洲各所代號），不是 yfinance 代號。轉換規則集中在
to_yf_symbol()，純函式、可單獨測試。轉不出來的名字「不猜」：照樣留在 holdings，
但 ticker 前綴 UNMAPPED: ，build_etf_dash 不會去抓 EPS，會排除並在方法說明列出，
讓維護者補下面的表。
"""
from __future__ import annotations

import csv
import io
import re
from datetime import datetime

import requests

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

UNMAPPED_PREFIX = "UNMAPPED:"

# 交易所名稱（持股檔 Exchange 欄原文）→ yfinance 後綴。空字串＝美國掛牌，不加後綴。
EXCHANGE_SUFFIX = {
    "Korea Exchange (Stock Market)": ".KS",
    "Korea Exchange (Kosdaq)": ".KQ",
    "Bursa Malaysia": ".KL",
    "XBSP": ".SA",
    "London Stock Exchange": ".L",
    "SIX Swiss Exchange": ".SW",
    "Nyse Euronext - Euronext Paris": ".PA",
    "Xetra": ".DE",
    "Deutsche Boerse Xetra": ".DE",
    "Euronext Amsterdam": ".AS",
    "Bolsa De Madrid": ".MC",
    "Nasdaq Omx Nordic": ".ST",
    "Borsa Italiana": ".MI",
    "Omx Nordic Exchange Copenhagen A/S": ".CO",
    "Nyse Euronext - Euronext Brussels": ".BR",
    "Nasdaq Omx Helsinki Ltd.": ".HE",
    "Oslo Bors Asa": ".OL",
    "Wiener Boerse Ag": ".VI",
    "Irish Stock Exchange - All Market": ".IR",
    "Nyse Euronext - Euronext Lisbon": ".LS",
    "Athens Exchange S.A. Cash Market": ".AT",
    "NYSE": "",
    "NASDAQ": "",
}

# 馬來西亞：持股檔給 Bursa 簡稱，yfinance 要數字碼＋.KL。2026-10-19 對 EWM
# 21 檔逐一核對過公司名。表外的新簡稱不猜，由 to_yf_symbol() 回報無法對應。
MALAYSIA_CODE = {
    "PBBANK": "1295", "CIMB": "1023", "MAYBANK": "1155", "TENAGA": "5347",
    "PMETAL": "8869", "GAMUDA": "5398", "YTLPOWR": "6742", "AMBANK": "1015",
    "SDG": "5285", "PETGAS": "6033", "HLBANK": "5819", "IHH": "5225",
    "RHBBANK": "1066", "SWB": "5211", "MISC": "3816", "IOICORP": "1961",
    "PCHEM": "5183", "KLK": "2445", "TM": "4863", "MAXIS": "6012", "CDB": "6947",
}

# iShares 的 Sector 欄是英文 GICS 類別；轉成跟 9 檔 SPDR 產業 ETF 同一套中文標籤
# （見 build_etf_dash.SECTOR_ETF_LABEL_ZH），報酬貢獻的產業彙總才不會中英混用。
# 不在表內的類別保留原文。
SECTOR_ZH = {
    "Information Technology": "科技", "Financials": "金融", "Energy": "能源",
    "Health Care": "醫療保健", "Industrials": "工業", "Consumer Discretionary": "非必需消費",
    "Consumer Staples": "必需消費", "Communication": "通訊服務", "Materials": "原物料",
    "Utilities": "公用事業", "Real Estate": "不動產",
}

# 已知例外（清理規則套不出 yfinance 代號的）：(持股檔原始代號, 後綴) → yfinance 代號。
SYMBOL_EXCEPTIONS = {
    ("BT.A", ".L"): "BT-A.L",
}


def to_yf_symbol(ticker: str, exchange: str) -> tuple[str | None, str | None]:
    """持股檔的 (Ticker, Exchange) → (yfinance 代號, None)；轉不出來回
    (None, 中文原因)。不猜：交易所不在表內、馬來西亞簡稱不在表內、韓國代號
    不是 6 位數字、代號清理後是空字串，一律回 None。"""
    t = (ticker or "").strip()
    ex = (exchange or "").strip()
    if not t:
        return None, "代號為空"
    if ex not in EXCHANGE_SUFFIX:
        return None, f"交易所「{ex or '空白'}」不在對照表內"
    suffix = EXCHANGE_SUFFIX[ex]
    if suffix == ".KL":
        code = MALAYSIA_CODE.get(t.upper())
        if code is None:
            return None, f"馬來西亞簡稱「{t}」不在對照表內（MALAYSIA_CODE 待補）"
        return f"{code}.KL", None
    if suffix in (".KS", ".KQ"):
        if not re.fullmatch(r"\d{6}", t):
            return None, f"韓國代號「{t}」不是 6 位數字"
        return f"{t}{suffix}", None
    if (t, suffix) in SYMBOL_EXCEPTIONS:
        return SYMBOL_EXCEPTIONS[(t, suffix)], None
    cleaned = t.rstrip(".").strip().replace(" ", "-")
    if not cleaned:
        return None, f"代號「{t}」清理後為空"
    return cleaned + suffix, None


def fetch_ishares_us_holdings_csv(cfg: dict) -> bytes:
    r = requests.get(cfg["holdings_url"], headers={"User-Agent": UA}, timeout=60, allow_redirects=True)
    r.raise_for_status()
    head = r.content[:2000].decode("utf-8-sig", errors="replace")
    # 用檔頭文字判斷是不是持股檔：HTML 頁面（含 content-type 標 csv 的那種）
    # 一律不收。
    if "<html" in head.lower() or "Fund Holdings as of" not in head:
        raise RuntimeError(f"not an iShares holdings CSV (content-type={r.headers.get('content-type')!r}, "
                           f"len={len(r.content)}, head={head[:60]!r}) from {cfg['holdings_url']}")
    return r.content


def _parse_as_of(lines: list[str]) -> str | None:
    for line in lines[:8]:
        if line.startswith("Fund Holdings as of"):
            row = next(csv.reader([line]))
            if len(row) >= 2:
                try:
                    return datetime.strptime(row[1].strip(), "%b %d, %Y").strftime("%Y-%m-%d")
                except ValueError:
                    return None
    return None


def parse_ishares_us_holdings_csv(raw: bytes) -> tuple[str, list[dict], list[dict]]:
    """回傳 (as_of, holdings, non_equity)——跟其他 source 的 parse 函式同一個
    形狀。holdings 每列：ticker（yfinance 代號，或 UNMAPPED:原代號:交易所）、
    raw_ticker_field、name、weight_pct、sector、exchange、unmapped_reason
    （只有轉不出來的才有）。"""
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    as_of = _parse_as_of(lines)
    header_idx = None
    for i in range(min(15, len(lines))):
        try:
            probe = next(csv.reader([lines[i]]))
        except StopIteration:
            continue
        if "Ticker" in probe and "Weight (%)" in probe and "Asset Class" in probe:
            header_idx = i
            break
    if as_of is None or header_idx is None:
        raise RuntimeError(f"could not locate as-of date or header row in iShares US holdings CSV "
                           f"(as_of={as_of!r})")
    rows_raw = list(csv.reader(io.StringIO("\n".join(lines[header_idx:]))))
    cols = rows_raw[0]
    try:
        ti, ni = cols.index("Ticker"), cols.index("Name")
        ai, wi = cols.index("Asset Class"), cols.index("Weight (%)")
    except ValueError as e:
        raise RuntimeError(f"iShares US holdings CSV missing expected columns; got {cols!r}") from e
    si = cols.index("Sector") if "Sector" in cols else None
    ei = cols.index("Exchange") if "Exchange" in cols else None
    need = max(ti, ni, ai, wi)

    holdings, non_equity = [], []
    for r in rows_raw[1:]:
        if len(r) <= need:
            continue
        ticker_raw, name = r[ti].strip(), r[ni].strip()
        if not ticker_raw or not name:
            continue
        asset_class = r[ai].strip()
        try:
            weight = float(r[wi].replace(",", ""))
        except (TypeError, ValueError):
            weight = None
        if asset_class != "Equity":
            non_equity.append({"ticker": ticker_raw, "name": name, "weight_pct": weight,
                               "reason": f"非普通股（Asset Class「{asset_class}」），不計入 EPS"})
            continue
        exchange = r[ei].strip() if ei is not None and len(r) > ei else ""
        sector = r[si].strip() if si is not None and len(r) > si and r[si].strip() else None
        sym, why = to_yf_symbol(ticker_raw, exchange)
        rec = {"ticker": sym if sym else f"{UNMAPPED_PREFIX}{ticker_raw}:{exchange}",
               "raw_ticker_field": ticker_raw, "name": name, "weight_pct": weight,
               "sector": SECTOR_ZH.get(sector, sector) if sector else None, "exchange": exchange}
        if not sym:
            rec["unmapped_reason"] = why
        holdings.append(rec)
    if not holdings:
        raise RuntimeError(f"parsed 0 equity holdings from iShares US holdings CSV (as_of={as_of!r})")
    return as_of, holdings, non_equity


def is_unmapped(ticker: str) -> bool:
    return ticker.startswith(UNMAPPED_PREFIX)
