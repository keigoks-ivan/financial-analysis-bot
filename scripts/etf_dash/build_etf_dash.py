#!/usr/bin/env python3
"""build_etf_dash.py — ETF 股價 vs 成分股 EPS 預估修正儀表板。

四檔基金：SMH 兩個版本比較（美國掛牌 VanEck Semiconductor ETF vs 愛爾蘭
UCITS 版，ISIN IE00BMC38736；持股／權重不同，UCITS 有集中度上限，這是這兩
檔要呈現的重點）＋ 2026-09-24 加的 QQQ（Invesco QQQ Trust，那斯達克 100）與
SPY（SPDR S&P 500 ETF Trust，標普 500，規模上到 ~500 檔成分股）。

Pipeline：
  1. 抓各基金發行商官方完整持股下載，三種來源、一套 fallback（見 FUND_REGISTRY
     的 "source" 與 HOLDINGS_SOURCES 分派）：
       - VanEck（SMH／SMH_UCITS）：fund 頁 "Download All Holdings" 連結，純
         GET + 一組 disclaimer cookie，回傳 .xlsx（fetch_holdings_xlsx()／
         parse_holdings_xlsx()）。
       - SSGA（SPY）：State Street 每日持股 xlsx，直接可下載，不需要 cookie
         （fetch_ssga_holdings_xlsx()／parse_ssga_holdings_xlsx()）。
       - Invesco（QQQ）：基金頁「All QQQ holdings」表格背後的 JSON API，純
         requests.get() 不需要 cookie，但實測偶爾回 406（短暫的 WAF／節流，
         非永久需要瀏覽器），已加重試（fetch_invesco_holdings_json()／
         parse_invesco_holdings_json()，見 INVESCO_406_RETRY_BACKOFFS_S）。
     任何一種失敗（格式改版、被擋、需要瀏覽器）都退回上次成功抓到的快取
     （data/etf_dash/holdings_cache/{ETF}.json），絕不用空資料覆蓋好資料。
     現金／期貨／CVR 等特殊有價證券三種來源都會被各自的 parse_* 識別出來，
     不進 EPS 計算但權重會回報（見 non_equity／non_equity_weight_pct）。
  2. 每檔成分股用 yfinance Ticker.eps_trend 抓 0y／+1y 的 current／7d／30d／
     60d／90d 前 EPS 估計（見該欄位自帶的 currency：多數 ADR 是 USD，但
     ASML 這類「美股掛牌、歐洲報表」的名字 eps_trend 是 EUR——這是
     scripts/eps_fx_normalize.py 修過的同一類 bug，這裡重用該模組的
     get_fx_rate() 只在算「加權遠期本益比」這條需要美元 EPS 的地方做 FX
     轉換；EPS 修正 % 本身是同幣別比較，不需要）。四檔基金共用同一份
     ticker_cache（見 main()），同一檔股票（如 NVDA 同時在 SMH／QQQ／SPY）
     一次 run 只抓一次；新 ticker 之間留 TICKER_FETCH_PACING_S 秒節流，SPY
     規模上到 ~500 檔後這條線變成整支 pipeline最花時間的部分。
  3. ETF 本身的股價走勢用 yfinance 直接抓。
  4. 算出：分期間（7d／30d／60d／90d 對齊 eps_trend 的四個錨點）的成分股
     加權 EPS 修正、ETF 股價漲跌、隱含本益比變動；當期加權遠期本益比
     （harmonic mean）；上修 Top 10／下修 Bottom 10 貢獻者；覆蓋率。
  5. 寫每日快照 data/etf_dash/snapshots/{ETF}/{YYYY-MM-DD}.json（同日重跑
     覆寫同一檔，冪等），供圖表隨時間自然長出歷史線（見
     build_eps_index_series()）。
  6. 輸出 docs/etf-dash/data/{ETF}.json（正式頁讀取）＋一份自含資料的
     preview HTML。

Usage:
    python3.12 scripts/etf_dash/build_etf_dash.py --etf SMH --etf SMH_UCITS --etf QQQ --etf SPY
    python3.12 scripts/etf_dash/build_etf_dash.py --etf SMH --preview-only

Exit code non-zero only if ALL requested funds failed outright (holdings
fetch failed AND no cache to fall back on); a single fund failing that way
only skips that fund and keeps going (see main()).
"""
from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import shutil
import subprocess
import sys
import os
import time
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

warnings.filterwarnings("ignore")

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from eps_fx_normalize import (  # noqa: E402
    load_fx_daily_cache, save_fx_daily_cache, get_fx_rate,
    load_reporting_currency_cache, save_reporting_currency_cache, get_reporting_currency,
    compute_fx_normalized_revision,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))  # scripts/etf_dash/ itself, for dd_eps_history
import dd_eps_history  # noqa: E402
import anchor_history  # noqa: E402
import price_history  # noqa: E402
import flows  # noqa: E402

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance>=0.2.40", "-q"])
    import yfinance as yf

SNAP_DIR = ROOT / "data" / "etf_dash" / "snapshots"
HOLDINGS_CACHE_DIR = ROOT / "data" / "etf_dash" / "holdings_cache"
EPS_CACHE_DIR = ROOT / "data" / "etf_dash" / "eps_cache"
OUT_DIR = ROOT / "docs" / "etf-dash" / "data"
PREVIEW_DIR = Path("/private/tmp/claude-501/-Users-ivanchang/etf_dash_preview")
DD_SCREENER_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"

TAIPEI_TZ = ZoneInfo("Asia/Taipei")
EPS_CACHE_MAX_AGE_DAYS = 7  # 超過這麼多天沒更新，即使不是週六也強制 FULL（"weekly" 基金）
# 2026-09-25 持有人拍板：TOPIX（日股持股／EPS 預估變動慢）FULL 改成每月一次
# （見 FUND_REGISTRY["TOPIX"]["full_refresh"]="monthly"），過期保護門檻同步
# 拉長——見 decide_mode() 的 full_refresh 分支。
EPS_CACHE_MAX_AGE_DAYS_MONTHLY = 35


def load_stock_dash_universe() -> set[str]:
    """/stock-dash/ 只給 docs/dd-screener/latest.json stocks[] 裡的 ticker 建頁
    （見 scripts/build_stock_dash_all.py docstring）。用這份集合判斷成分股列
    要不要連到 /stock-dash/?t=，讀不到就回空集合（頁面全部退化成純文字，不連結，
    不當掉）。"""
    try:
        d = json.loads(DD_SCREENER_LATEST.read_text(encoding="utf-8"))
        return {s["ticker"] for s in d.get("stocks", []) if s.get("ticker")}
    except Exception as e:  # noqa: BLE001
        print(f"[etf_dash] WARNING could not load {DD_SCREENER_LATEST} for stock-dash link check: {e}",
              file=sys.stderr)
        return set()

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

# 2026-09-24 實測：VanEck fund 頁本身要投資人類型/國家 disclaimer 才會顯示
# holdings 表（JS 渲染的 <ve-holdingsblock> custom element），但「Download
# All Holdings」連結背後的 XHR 端點本身只認一個 disclaimer cookie（伺服器
# 302 重導向到 ...?cken=true 時已經在 Set-Cookie 裡示範了這個 cookie 的完整
# 格式——見 CI 測試 notes），純 requests.get() 帶這組 cookie 就能拿到 .xlsx，
# 不需要瀏覽器/JS。
# 每檔基金的持股來源——"source" 對應下面 HOLDINGS_SOURCES 的 (fetch_fn,
# parse_fn) 一組，2026-09-24 新增 QQQ／SPY 時拆出來，讓 get_holdings_with_fallback()
# 不用管每家發行商的下載格式差異（VanEck 是 xlsx＋cookie 閘門、SSGA(SPY) 是
# 直接可下載的 xlsx、Invesco(QQQ) 是 JSON API——見各自 fetch_*／parse_* 函式）。
FUND_REGISTRY = {
    "SMH": {
        "label_zh": "VanEck 半導體 ETF（SMH，那斯達克，美國掛牌）",
        "label_en": "VanEck Semiconductor ETF (SMH, NASDAQ)",
        "yf_ticker": "SMH",
        "isin": None,
        "source": "vaneck",
        "holdings_issuer_zh": "VanEck 官方持股下載",
        "holdings_url": "https://www.vaneck.com/us/en/investments/semiconductor-etf-smh/downloads/holdings/",
        "holdings_page_url": "https://www.vaneck.com/us/en/investments/semiconductor-etf-smh/holdings/",
        "holdings_cookies": {
            "ve-country-us": "iso%3Dus%26investortype%3Dretail%26language%3Den%26disclaimer%3Dtrue"
                              "%26foreigntax%3Dfalse%26foreigntaxdisclaimer%3Dfalse",
            "visitortype": "user",
            "sitelanguage": "en",
            "ve-country": "current%3Dus%26previous%3D",
        },
        "other_listings": [],
    },
    "SMH_UCITS": {
        "label_zh": "VanEck 半導體 UCITS ETF（愛爾蘭掛牌，ISIN IE00BMC38736；LSE 美元計價 ticker 同名 SMH）",
        "label_en": "VanEck Semiconductor UCITS ETF (IE00BMC38736; LSE SMH, USD)",
        "yf_ticker": "SMH.L",
        "isin": "IE00BMC38736",
        "source": "vaneck",
        "holdings_issuer_zh": "VanEck 官方持股下載",
        "holdings_url": "https://www.vaneck.com/ie/en/investments/semiconductor-etf/downloads/holdings/",
        "holdings_page_url": "https://www.vaneck.com/ie/en/investments/semiconductor-etf/holdings/",
        "holdings_cookies": {
            "ve-country-ie": "iso%3Die%26investortype%3Dretail%26language%3Den%26disclaimer%3Dtrue"
                              "%26foreigntax%3Dfalse%26foreigntaxdisclaimer%3Dfalse",
            "visitortype": "user",
            "sitelanguage": "en",
            "ve-country": "current%3Die%26previous%3D",
        },
        # 同一檔基金的其他掛牌／計價幣別——本頁不抓這些，只記錄供讀者對照。
        "other_listings": [
            {"exchange": "LSE", "ticker": "SMGB.L", "currency": "GBP"},
            {"exchange": "Xetra", "ticker": "VVSM.DE", "currency": "EUR"},
        ],
    },
    "QQQ": {
        "label_zh": "Invesco QQQ 信託（QQQ，那斯達克 100，美國掛牌）",
        "label_en": "Invesco QQQ Trust (QQQ, Nasdaq-100)",
        "yf_ticker": "QQQ",
        "isin": None,
        "source": "invesco",
        "holdings_issuer_zh": "Invesco 官方持股 API",
        # 2026-09-24 實測：QQQ 基金頁「All QQQ holdings」表格背後的 XHR 端點
        # （table 的 data-holding-api）是一個乾淨的 JSON API，純 requests.get()
        # 不帶任何 cookie／session 就能拿到（見 fetch_invesco_holdings_json()）；
        # 頁面上另一個 data-holdings-api（多了 loadType=initial 參數）反而會被
        # WAF 擋 406，這裡刻意不用那個。
        "holdings_url": "https://dng-api.invesco.com/cache/v1/accounts/en_US/shareclasses/QQQ/holdings/fund",
        "holdings_page_url": "https://www.invesco.com/qqq-etf/en/about.html",
        "holdings_params": {"idType": "ticker", "interval": "monthly", "productType": "ETF"},
        "other_listings": [],
    },
    "SPY": {
        "label_zh": "SPDR 標普 500 ETF 信託（SPY，紐約證交所，美國掛牌）",
        "label_en": "SPDR S&P 500 ETF Trust (SPY, NYSE Arca)",
        "yf_ticker": "SPY",
        "isin": None,
        "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        # 2026-09-24 實測：State Street 每日持股 xlsx 直接可下載（301 重導向到
        # 同網域的另一個路徑，requests 預設就會跟），不需要 cookie／disclaimer
        # 閘門——跟 VanEck 那組不同。
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy",
        "other_listings": [],
    },
    # 2026-09-25 加的 9 檔 SPDR 產業 ETF（SPDR Select Sector Fund 系列，State
    # Street 發行）——跟 SPY 同一個發行商、同一套持股 xlsx 格式，只是網址裡的
    # ticker 換成小寫（holdings-daily-us-en-{ticker}.xlsx），source 沿用既有的
    # "ssga"（fetch_ssga_holdings_xlsx／parse_ssga_holdings_xlsx，不需要另外
    # 寫 parser）——9 檔網址都已個別 curl 實測回 200＋正確 content-type。成分股
    # 全部是 SPY 500 檔的子集合，跟 SPY 同一個 run 共用 ticker_cache 幾乎不會
    # 產生新的 eps_trend 呼叫（見 main() 的共用快取設計）。只加 9 個（略過
    # XLRE 房地產／XLU 公用事業，持有人拍板不需要）。
    "XLK": {
        "label_zh": "科技類股 SPDR 基金（XLK，S&P 科技產業，美國掛牌）",
        "label_en": "Technology Select Sector SPDR Fund (XLK)",
        "yf_ticker": "XLK", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlk.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/technology-select-sector-spdr-fund-xlk",
        "other_listings": [],
    },
    "XLF": {
        "label_zh": "金融類股 SPDR 基金（XLF，S&P 金融產業，美國掛牌）",
        "label_en": "Financial Select Sector SPDR Fund (XLF)",
        "yf_ticker": "XLF", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlf.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/financial-select-sector-spdr-fund-xlf",
        "other_listings": [],
    },
    "XLE": {
        "label_zh": "能源類股 SPDR 基金（XLE，S&P 能源產業，美國掛牌）",
        "label_en": "Energy Select Sector SPDR Fund (XLE)",
        "yf_ticker": "XLE", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xle.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/energy-select-sector-spdr-fund-xle",
        "other_listings": [],
    },
    "XLV": {
        "label_zh": "醫療保健類股 SPDR 基金（XLV，S&P 醫療保健產業，美國掛牌）",
        "label_en": "Health Care Select Sector SPDR Fund (XLV)",
        "yf_ticker": "XLV", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlv.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/health-care-select-sector-spdr-fund-xlv",
        "other_listings": [],
    },
    "XLI": {
        "label_zh": "工業類股 SPDR 基金（XLI，S&P 工業產業，美國掛牌）",
        "label_en": "Industrial Select Sector SPDR Fund (XLI)",
        "yf_ticker": "XLI", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xli.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/industrial-select-sector-spdr-fund-xli",
        "other_listings": [],
    },
    "XLY": {
        "label_zh": "非必需消費類股 SPDR 基金（XLY，S&P 非必需消費產業，美國掛牌）",
        "label_en": "Consumer Discretionary Select Sector SPDR Fund (XLY)",
        "yf_ticker": "XLY", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xly.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/consumer-discretionary-select-sector-spdr-fund-xly",
        "other_listings": [],
    },
    "XLP": {
        "label_zh": "必需消費類股 SPDR 基金（XLP，S&P 必需消費產業，美國掛牌）",
        "label_en": "Consumer Staples Select Sector SPDR Fund (XLP)",
        "yf_ticker": "XLP", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlp.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/consumer-staples-select-sector-spdr-fund-xlp",
        "other_listings": [],
    },
    "XLC": {
        "label_zh": "通訊服務類股 SPDR 基金（XLC，S&P 通訊服務產業，美國掛牌）",
        "label_en": "Communication Services Select Sector SPDR Fund (XLC)",
        "yf_ticker": "XLC", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlc.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/communication-services-select-sector-spdr-fund-xlc",
        "other_listings": [],
    },
    "XLB": {
        "label_zh": "原物料類股 SPDR 基金（XLB，S&P 原物料產業，美國掛牌）",
        "label_en": "Materials Select Sector SPDR Fund (XLB)",
        "yf_ticker": "XLB", "isin": None, "source": "ssga",
        "holdings_issuer_zh": "State Street (SSGA) 官方每日持股下載",
        "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlb.xlsx",
        "holdings_page_url": "https://www.ssga.com/us/en/intermediary/etfs/materials-select-sector-spdr-fund-xlb",
        "other_listings": [],
    },
    # 2026-09-25 加的 RSP（Invesco S&P 500 等權重 ETF）——跟 QQQ 同一個發行商、
    # 同一套 JSON API 格式，source 沿用既有的 "invesco"（fetch_invesco_holdings_json／
    # parse_invesco_holdings_json）。這檔的特別之處是它有第三層 fallback：
    # Invesco API 若失敗、且本地也沒有 RSP 自己的 holdings_cache（例如上線第一次
    # 就撞到 406），改用同一次 run 裡 SPY 的成分股清單做等權重近似（見
    # get_holdings_with_fallback() 裡的 etf_key == "RSP" 分支與
    # build_rsp_equal_weight_fallback()）——RSP 本身定義就是「S&P 500 成分股
    # 等權重」，這是失去官方持股時最貼近實際持股結構的近似，清楚標記
    # holdings_approximation_zh 不是真實持股。
    "RSP": {
        "label_zh": "Invesco 標普 500 等權重 ETF（RSP，紐約證交所，美國掛牌）",
        "label_en": "Invesco S&P 500 Equal Weight ETF (RSP)",
        "yf_ticker": "RSP", "isin": None, "source": "invesco",
        "holdings_issuer_zh": "Invesco 官方持股 API",
        "holdings_url": "https://dng-api.invesco.com/cache/v1/accounts/en_US/shareclasses/RSP/holdings/fund",
        "holdings_page_url": "https://www.invesco.com/us/financial-products/etfs/product-detail?audienceType=Investor&ticker=RSP",
        "holdings_params": {"idType": "ticker", "interval": "monthly", "productType": "ETF"},
        "other_listings": [],
    },
    # 2026-09-24 加的兩檔台股基金——見本檔下方「TAIEX (台灣加權指數)」與
    # 「0050 (元大台灣卓越50基金)」兩段的 fetch/parse 函式與其上的方法論註解。
    # 兩者都用 pe_basis_currency="TWD"：本益比／股價換算的基準幣別不是預設的
    # USD（見 convert_to_basis_currency()），避免把 TWD 數字當 USD 用（過去在
    # 別的頁面出現過的那種 bug）。
    "TAIEX": {
        "label_zh": "台灣加權股價指數（TAIEX，近似持股，非追蹤型 ETF）",
        "label_en": "Taiwan Capitalization Weighted Stock Index (TAIEX)",
        "yf_ticker": "^TWII",
        "isin": None,
        "source": "twse",
        "pe_basis_currency": "TWD",
        "holdings_issuer_zh": "TWSE 公開資料（上市公司基本資料＋個股日成交資訊）機械估算近似持股",
        # 純文件用途（JSON 的 holdings_source_url／citation 連結）——實際抓取
        # 用的兩個端點見下方 fetch_twse_taiex_universe()／TWSE_COMPANY_LIST_URL
        # 與 TWSE_STOCK_DAY_ALL_URL 常數，這裡列的是後者（收盤價，讀者比較
        # 常需要對照的那個）。
        "holdings_url": "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",
        "holdings_page_url": "https://openapi.twse.com.tw/",
        "other_listings": [],
    },
    "0050": {
        "label_zh": "元大台灣卓越50基金（0050）",
        "label_en": "Yuanta/P-shares Taiwan Top 50 ETF (0050)",
        "yf_ticker": "0050.TW",
        "isin": "TW0000050004",
        "source": "yuanta",
        "pe_basis_currency": "TWD",
        "holdings_issuer_zh": "元大投信官方持股頁（SSR 內嵌資料）",
        "holdings_url": "https://www.yuantaetfs.com/product/detail/0050/ratio",
        "holdings_page_url": "https://www.yuantaetfs.com/product/detail/0050/ratio",
        "other_listings": [],
    },
    # 2026-09-25 加的日股基金——iShares Core TOPIX ETF（1475，東京證交所，
    # BlackRock Japan）。選它而非 NEXT FUNDS TOPIX（1306，野村）或 MAXIS
    # TOPIX（1348）：三檔的完整持股（~1,700 檔）都能純 requests.get() 拿到
    # （1475 是 .ajax CSV 端點、1306 是野村官網一支 .xlsx，都不需要 cookie／
    # 瀏覽器——見 fetch_ishares_jp_holdings_csv() 上方註解），但 1475 成分股數
    # 與 as-of 日期直接寫在檔案第一列（"基準日","YYYY年M月D日"），格式最好
    # 機械解析、且是三檔裡規模最大最具代表性的一檔，故選 1475。TOPIX 本身不
    # 是可交易標的，只能用追蹤它的 ETF 當持股與價格代理。
    "TOPIX": {
        "label_zh": "TOPIX（1475，iシェアーズ・コア TOPIX ETF，東京證交所）",
        "label_en": "iShares Core TOPIX ETF (1475, TSE, tracking TOPIX)",
        "yf_ticker": "1475.T",
        "isin": None,
        "source": "ishares_jp",
        "pe_basis_currency": "JPY",
        # 2026-09-25 持有人拍板：TOPIX 只有這一檔用 "monthly"——日股持股與
        # EPS 預估變動慢，不需要每週整套重抓（見 decide_mode() full_refresh
        # 分支）；股價（ETF／成分股／加權遠期本益比／圖表股價線）仍是每天
        # PRICE 模式更新，不受影響。其餘六檔沒有這個鍵，decide_mode() 用
        # cfg.get("full_refresh", "weekly") 取預設值，行為完全不變。
        "full_refresh": "monthly",
        # 2026-09-25 實測：完整持股 ~1,635 檔股票，逐檔抓 yfinance eps_trend
        # 在時間（見 TICKER_FETCH_PACING_S）與限速風險上都不現實——只對依權重
        # 排序、累計達此門檻的最大權重成分股抓 EPS（見
        # select_eps_scope_tickers()／build_eps_scope_note_zh()），其餘成分股
        # 仍列在完整持股明細，但 excluded 标记為「EPS 涵蓋門檻外」，不計入任何
        # EPS 相關計算。實測 90% 門檻約需 370 檔（見本次 run 的
        # methods_note_zh 記錄實際數字）；如果全部 7 檔基金 FULL 總時間超出
        # ~35 分鐘，改低到 85%（約 248 檔）。
        "eps_scope_cutoff_pct": 90.0,
        "holdings_issuer_zh": "iShares（BlackRock Japan）官方持股下載",
        "holdings_url": "https://www.blackrock.com/jp/individual/ja/products/279438/fund/1480664184455.ajax"
                        "?fileType=csv&fileName=1475_holdings&dataType=fund",
        "holdings_page_url": "https://www.blackrock.com/jp/individual/ja/products/279438/ishares-core-topix-etf",
        "other_listings": [],
    },
}

# 2026-09-24 持有人拍板：SK Hynix 在 VanEck 持股欄位裡標的 ticker「SKHYV」是
# 境外 Reg-S ADR，yfinance 查無報價（Quote not found）——原本整檔排除，但它是
# 兩檔基金裡數一數二大的權重（UCITS 9.16%／US 4.67%），排除會讓 ETF 加權 EPS
# 變動有偏誤（它很可能是修正幅度最大的名字之一）。改用一個顯式別名表，把
# 「VanEck 持股欄位的 ticker」映射到「yfinance 實際查得到報價與 EPS 的 ticker」
# ——SK Hynix 用南韓交易所掛牌股 000660.KS（KRW 計價）。eps_trend／fast_info
# 抓到的 EPS 與股價都是這檔韓股本身的（同一份股票、同一個股數基礎），不是
# ADR 換股比例調整過的數字，兩者一起用不會有股數比例造成的單位不一致
# （revisions_pct／price_usd 都用同一檔 000660.KS 的原始 KRW 數字算，FX 換算
# 只在需要美元基準的地方做——見 build_fund() 裡對 eps_fy_next_usd／price_usd
# 兩處的 FX 轉換，兩者都走同一個 get_fx_rate() 快取）。未來遇到類似查無報價
# 的成分股，往這裡加一行 alias 即可，不需要改其他邏輯。
TICKER_ALIAS = {
    "SKHYV": "000660.KS",
    # 2026-09-24 QQQ/SPY 上線：S&P 500 官方持股欄位裡的雙類股用點號分隔
    # （"BRK.B"／"BF.B"），yfinance 一律用連字號（"BRK-B"／"BF-B"）——實測
    # SPY 505 檔持股裡只有這兩檔是這個格式（見 build_etf_dash.py 的
    # parse_ssga_holdings_xlsx 與其測試）。
    "BRK.B": "BRK-B",
    "BF.B": "BF-B",
}

# 2026-09-24 持有人對帳確認的兩個 build_long_eps_index() anomaly_events 根因
# （見該函式與 classify_eps_step()）：
#   - KLAC 07-16：KLAC 於 2026-06-12 執行 10:1 股票分割，Koyfin 延遲到 07-16
#     才在預估欄位反映，eps_fy_next／eps_fy3 才會同步除以約 9.7-10。
#   - TSM 09-16：dd-screener 管線當天開始對 TSM 套用 ADR 換股比例，讓
#     eps_fy_next／eps_fy3 同步乘以約 4.9（此前呈現的是換算前的基礎）。
# 只註記已經對過帳、有明確根因的事件；沒對過帳的（例如 05-20 那筆，當時
# eps_fy3 欄位還沒上線）維持不猜測根因，只留「排除」的事實。
KNOWN_ANOMALY_EXPLANATIONS = {
    ("KLAC", "2026-07-16"): "KLAC 於 2026-06-12 執行 10:1 股票分割，Koyfin 延遲到 07-16 才反映在預估欄位，"
                             "eps_fy_next／eps_fy3 同步除以約 9.7-10，不是分析師修正。",
    ("TSM", "2026-09-16"): "dd-screener 管線當天開始對 TSM 套用 ADR 換股比例，eps_fy_next／eps_fy3 同步"
                            "乘以約 4.9（此前呈現的是換算前的基礎），不是分析師修正。",
}

PERIOD_DEFS = [  # (key, yfinance eps_trend 欄名, 中文標籤, 概略天數)
    # 2026-09-24 拿掉「近 7 天」列——tiered update 上線後 Exhibit 1 整份表格
    # 錨定在 eps_as_of（週頻），7 天窗口太短、又跟「EPS 預估更新於...」那行
    # daily 資訊重疊，容易讓人誤讀成每天在動。
    ("30d", "30daysAgo", "近一個月", 30),
    ("60d", "60daysAgo", "近二個月", 60),
    ("90d", "90daysAgo", "近三個月", 90),
]

# 2026-09-25 加的 anchor-line fallback（見 scripts/etf_dash/anchor_history.py
# 模組開頭 docstring）用的錨點集合——跟 PERIOD_DEFS 分開的獨立常數：Exhibit 1
# 的期間表格 2026-09-24 故意拿掉「近 7 天」（太短、跟 daily 更新資訊重疊，見
# PERIOD_DEFS 上方註解），但 anchor line 需要完整 5 個 yfinance eps_trend 錨點
# （含 7 天前）才能在覆蓋率不足 dd-screener 長線的基金上補一條線——兩者用途不
# 同，合併會讓「7d 要不要進 Exhibit 1」跟「anchor line 用幾個錨點」被綁在一起。
# fetch_ticker_eps_and_price() 的 anchors_local 改抓這份（是 PERIOD_DEFS 的
# superset，同樣的欄名），PERIOD_DEFS 驅動的 revisions_pct 計算不受影響（它
# 只迭代 PERIOD_DEFS 的三個 key，anchors_local 多出的 "7d" 不會被用到那裡）。
ANCHOR_LINE_DEFS = [  # (key, yfinance eps_trend 欄名, 概略天數)
    ("7d", "7daysAgo", 7),
    ("30d", "30daysAgo", 30),
    ("60d", "60daysAgo", 60),
    ("90d", "90daysAgo", 90),
]

# 2026-09-24 持有人擋下第一版 QQQ/SPY 上線：QQQ「近三個月」EPS 加權變動
# -17.1% 是異常值拉出來的，不是真實修正——SPCX（2.66% 權重）90d 修正 -889%
# （60d 卻是 +185%），根因是基期（N 天前）估計值趨近 0 甚至翻負號，除出來的
# 比值本身就不穩定；HON -56.6% 是拆分／企業行動造成分母跳動，不是分析師
# 調升調降；SPY 更誇張，ECHO 單筆 -20038%。這三檔都不是「EPS 真的變了
# 這麼多」，是分母壞掉。REVISION_BASE_MIN_RATIO／REVISION_CAP_PCT 兩道閘：
# 先剔除分母壞掉的（見 classify_revision()「invalid_base」），剩下的合理但
# 單筆仍可能是極端值（真實的巨幅修正，如虧轉盈附近的成長股）——這種不剔除
# （會漏掉真實訊號），改封頂在 ±50%，兩份名單都進 JSON／頁面讓人查核，不是
# 悄悄改數字。
REVISION_BASE_MIN_RATIO = 0.2   # |base(N天前 EPS)| < 此比例 × |current(今日 EPS)| → 比值不穩定，整筆排除
REVISION_CAP_PCT = 50.0         # 排除異常基期後，單筆修正 % 仍封頂在 ±50%（保留原始值供稽核，不丟棄）

# 2026-09-25 持有人擋下 XLF／RSP／SPY 的加權遠期本益比：PGR 的 yfinance
# eps_fy_next=1012.0（實際 Progressive FY EPS 量級應在 $15-20，這是 Yahoo
# 資料異常，不是單位換算——見下方 PE_EXCLUDE_MIN_X／PE_EXCLUDE_MAX_X 修
# weighted_forward_pe 那條腿）。這裡另外補一道 EPS 修正% 那條腿的檢查：
# REVISION_BASE_MIN_RATIO 只抓「base 相對 current 過小」（current/base 過大，
# 即巨幅上修）的情況，沒有對稱抓「current 相對 base 過小」（巨幅下修，
# current/base 過小）的情況——例如 base 本身就是異常值時，比值可能小於
# 0.1x。REVISION_UNIT_GLITCH_MIN_RATIO／MAX_RATIO 補這個對稱檢查，抓 10 倍
# 量級的比值跳動（常見的單位/資料異常特徵），跟 REVISION_BASE_MIN_RATIO
# 分開判斷、不互相取代。經查核：PGR 這次 run 的 30d/60d/90d 三個錨點
# （eps_trend 的 "30daysAgo"/"60daysAgo"/"90daysAgo" 欄）全部是 None（yfinance
# 沒有回傳歷史值，不是異常值），落在既有 "no_base" 分支，不受這裡影響——
# PGR 對加權遠期本益比的拖累完全是本益比那條腿的問題，這個新檢查目前對
# PGR 本身沒有作用，是為了未來出現「有 base 但比值跳 10 倍」的案例補的閘。
REVISION_UNIT_GLITCH_MAX_RATIO = 10.0   # current/base > 此值 → 疑似單位或資料異常，整筆排除
REVISION_UNIT_GLITCH_MIN_RATIO = 0.1    # current/base < 此值 → 同上


def classify_revision(base: float | None, current: float | None) -> tuple[str, str | None, float | None, float | None]:
    """純函式（不碰快取／網路）：判斷一筆「N 天前 EPS → 今日 EPS」修正% 該怎麼用。
    回傳 (status, reason, raw_pct, capped_pct)：

      - "no_base"：base 缺值（那個時間點 yfinance 根本沒抓到資料）——不是異常，
        只是覆蓋率不足，raw_pct/capped_pct/reason 都是 None，沿用既有行為
        （這筆不進任何加總，也不進 period_exclusions——那份名單只記「有資料
        但資料壞掉」的情況，跟「沒資料」分開，語意才清楚）。
      - "invalid_base"：current<=0，或 base<=0，或 |base| 相對 current 過小
        （REVISION_BASE_MIN_RATIO 門檻——SPCX／ECHO／HON 這類基期趨近 0 或
        翻負號、企業行動造成分母跳動的案例），或 current/base 比值超出
        [REVISION_UNIT_GLITCH_MIN_RATIO, REVISION_UNIT_GLITCH_MAX_RATIO]
        區間（疑似單位或資料異常）。整筆排除，不進任何加總（raw_pct/
        capped_pct 為 None），reason 說明原因，呼叫端要記進 period_exclusions。
      - "capped"：比值本身站得住腳，但單筆修正 % 超過 ±REVISION_CAP_PCT，
        封頂後才拿去加權——raw_pct 保留原始值供稽核，capped_pct 是實際加權
        用的值，呼叫端要記進 period_capped。
      - "ok"：正常，raw_pct == capped_pct。
    """
    if base is None or base == 0:
        return "no_base", None, None, None
    if current is None or current <= 0:
        return "invalid_base", "明年度 EPS 現值 ≤ 0", None, None
    if base <= 0:
        return "invalid_base", f"基期 EPS 估計 ≤ 0（{base:.4f}）", None, None
    if abs(base) < REVISION_BASE_MIN_RATIO * abs(current):
        return ("invalid_base",
                f"基期 EPS 估計相對現值過小（|{base:.4f}| < {REVISION_BASE_MIN_RATIO}×|{current:.4f}|），比值不穩定",
                None, None)
    ratio = current / base
    if ratio > REVISION_UNIT_GLITCH_MAX_RATIO or ratio < REVISION_UNIT_GLITCH_MIN_RATIO:
        return ("invalid_base",
                f"現值／基期比值 {ratio:.2f}x 超出合理區間 [{REVISION_UNIT_GLITCH_MIN_RATIO}x, "
                f"{REVISION_UNIT_GLITCH_MAX_RATIO}x]，疑似單位或資料異常",
                None, None)
    raw_pct = (current / base - 1) * 100
    capped_pct = max(-REVISION_CAP_PCT, min(REVISION_CAP_PCT, raw_pct))
    status = "capped" if abs(raw_pct - capped_pct) > 1e-9 else "ok"
    return status, None, round(raw_pct, 4), round(capped_pct, 4)


# ---------------------------------------------------------------------------
# EPS 修正廣度 (breadth) — 2026-09-26 加。純粹從已經算好的 constituents（每檔
# 都帶 revisions_pct，FULL／PRICE 兩種模式回傳的形狀完全一樣，見
# build_fund_full()／build_fund_price()）分類，不呼叫任何額外的 yfinance——
# 跟 classify_revision() 算出來的 revisions_pct 是同一份資料，只是換一種
# 彙總角度（「修正了多少」→「有幾檔、多少權重朝哪個方向修正」）。
# ---------------------------------------------------------------------------

BREADTH_DEAD_BAND_PCT = 0.5  # |revision_pct| < 此值 -> 算「持平」，見 compute_eps_breadth()


def _weighted_median(pairs: list[tuple[float, float]]) -> float | None:
    """pairs = [(value, weight), ...]，weight 需為正數。標準加權中位數：依
    value 排序後找「累積權重跨過總權重一半」的那個 value。"""
    items = [(v, w) for v, w in pairs if w and w > 0]
    if not items:
        return None
    items.sort(key=lambda x: x[0])
    total = sum(w for _, w in items)
    half = total / 2
    acc = 0.0
    for v, w in items:
        acc += w
        if acc >= half:
            return v
    return items[-1][0]


def compute_eps_breadth(constituents: list[dict]) -> dict:
    """回傳 {period_key: {...}}——每個 PERIOD_DEFS 期間各自算一份「修正廣度」：
    有 revisions_pct 值的成分股依 BREADTH_DEAD_BAND_PCT 死區分成上修／持平／
    下修三類，各自算檔數與（相對於「有值那些」的覆蓋權重重新正規化的）權重
    佔比，外加加權中位數修正%（用原始 revisions_pct，不是三分類後的標籤）。
    跟 periods[].eps_chg_pct 用同一個「相對覆蓋權重重新正規化」慣例
    （見 build_fund_full() 的 covered_weight 那段），這樣「上修/持平/下修
    權重佔比」三者才會剛好加總 100%。"""
    out = {}
    for key, _col, label, _days in PERIOD_DEFS:
        up, flat, down = [], [], []
        for c in constituents:
            rev = (c.get("revisions_pct") or {}).get(key)
            if rev is None:
                continue
            w = c.get("weight_pct") or 0
            item = {"ticker": c["ticker"], "name": c.get("name"), "weight_pct": w, "revision_pct": rev}
            if abs(rev) < BREADTH_DEAD_BAND_PCT:
                flat.append(item)
            elif rev > 0:
                up.append(item)
            else:
                down.append(item)
        n_covered = len(up) + len(flat) + len(down)
        covered_weight = sum(i["weight_pct"] for i in (up + flat + down))
        med = _weighted_median([(i["revision_pct"], i["weight_pct"]) for i in (up + flat + down)])

        def _wpct(bucket):
            return round(sum(i["weight_pct"] for i in bucket) / covered_weight * 100, 2) if covered_weight else None

        out[key] = {
            "key": key, "label": label,
            "n_up": len(up), "n_flat": len(flat), "n_down": len(down), "n_covered": n_covered,
            "n_total": len(constituents),
            "up_weight_pct": _wpct(up), "flat_weight_pct": _wpct(flat), "down_weight_pct": _wpct(down),
            "weighted_median_revision_pct": round(med, 4) if med is not None else None,
            "dead_band_pct": BREADTH_DEAD_BAND_PCT,
        }
    return out


RATE_LIMIT_BACKOFFS_S = [20, 45, 90]  # yfinance YFRateLimitError 重試等待秒數
TICKER_FETCH_PACING_S = 0.4  # 每檔新 ticker（快取沒有才算）之間的固定間隔秒數，見 build_fund()


def _is_rate_limited(exc: Exception) -> bool:
    name = type(exc).__name__
    msg = str(exc)
    return "YFRateLimitError" in name or ("rate" in msg.lower() and "limit" in msg.lower()) or "429" in msg


def yf_call_with_backoff(fn, *, label: str = ""):
    """跑一個 yfinance 存取（lambda），YFRateLimitError 時照 RATE_LIMIT_BACKOFFS_S
    等待重試；其他例外直接往外拋（呼叫端決定是整檔跳過還是整體失敗）。"""
    last_exc = None
    for attempt, wait_s in enumerate([0] + RATE_LIMIT_BACKOFFS_S):
        if wait_s:
            print(f"[etf_dash] rate-limited on {label}; sleeping {wait_s}s before retry "
                  f"{attempt}/{len(RATE_LIMIT_BACKOFFS_S)}", file=sys.stderr)
            time.sleep(wait_s)
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            last_exc = e
            if not _is_rate_limited(e):
                raise
    raise last_exc


# ---------------------------------------------------------------------------
# Tiered update — FULL（持股下載＋逐檔 eps_trend）vs PRICE（只抓股價，EPS 沿用
# 上次 FULL 存的快取）。2026-09-24 持有人拍板：SPY 規模到 ~500 檔，每天都整套
# 重抓 eps_trend 一來耗時（~10-15 分鐘）二來持續增加 yfinance 限速／Invesco
# 406 的風險，但成分股「明年度 EPS」預估本來就是月頻更新的資料（見
# dd_eps_history.py 同樣的觀察），沒必要每天重抓。改成：
#   - FULL：週六（台北時區）、或 EPS 快取遺失／超過 EPS_CACHE_MAX_AGE_DAYS 天沒
#     更新、或 --mode full 明示——完整跑一次（持股下載＋每檔 eps_trend），
#     跑完把「這次算出來的東西」存進 data/etf_dash/eps_cache/{ETF}.json（見
#     save_eps_cache()）：持股、非個股清單、每檔的 EPS 現值與幣別、已經算好
#     且凍結的 periods／contributions 表格。
#   - PRICE：其他日子——完全不下載持股、不呼叫 eps_trend，只用一次（視規模
#     chunk 幾次）batched yf.download 抓 ETF 加所有成分股「今天」的收盤價
#     （見 fetch_prices_batch()），拿去跟快取的 EPS 重新配對算「今日加權遠期
#     本益比」；Exhibit 1 的期間表格（EPS 修正％／股價漲跌／隱含本益比）整份
#     沿用快取，不重算——這樣才符合「同一個 N 天窗口內，EPS 變動跟股價變動要
#     配對」的要求（都是以 eps_as_of 為錨點，不是以「今天」為錨點，否則兩者
#     窗口對不齊、隱含本益比會是假訊號）。
# 兩種模式輸出的 JSON 仍是同一個 "etf-dash-v1" schema，只是多了 mode／
# eps_as_of／price_since_eps_as_of_pct 幾個欄位（見 build_fund_full()／
# build_fund_price() 尾端）——頁面／下游都不需要分兩套邏輯。
# ---------------------------------------------------------------------------


def taipei_now() -> datetime:
    return datetime.now(TAIPEI_TZ)


def load_eps_cache(etf_key: str) -> dict | None:
    """讀 data/etf_dash/eps_cache/{ETF}.json；不存在或壞掉都回 None（呼叫端
    決定要不要因此強制 FULL），不拋例外——EPS 快取只是加速用，壞了不該讓整個
    build 掛掉。"""
    path = EPS_CACHE_DIR / f"{etf_key}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"[etf_dash] WARNING could not read EPS cache {path}: {e}", file=sys.stderr)
        return None


def save_eps_cache(etf_key: str, data: dict) -> None:
    EPS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = EPS_CACHE_DIR / f"{etf_key}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def is_first_saturday_of_month(d) -> bool:
    """d 是 date（或 datetime）——每月只有一個週六的 day <= 7（週六彼此間隔 7
    天，同月第二個週六 day 必定 >= 8），不需要另外算「這個月第一天是星期
    幾」。呼叫端要自己先確認 d 是週六（這裡不重複檢查 weekday，見 decide_mode
    的呼叫方式），單獨呼叫這個函式對非週六的日期沒有意義但不會噴錯。"""
    return d.day <= 7


def decide_mode(cli_mode: str, eps_cache: dict | None, now_taipei: datetime,
                 full_refresh: str = "weekly") -> tuple[str, str]:
    """純函式（不碰檔案／網路——是否讀得到快取由呼叫端先讀好傳進來)：決定這次
    要跑 FULL 還是 PRICE，回傳 (mode, reason)。

    full_refresh（見 FUND_REGISTRY cfg["full_refresh"]，預設 "weekly"）：
      - "weekly"（多數基金）：規則同舊版——
          1. 台北時區今天是週六 -> full。
          2. 完全沒有 EPS 快取（第一次跑、或快取被清掉）-> full。
          3. 快取的 eps_as_of 超過 EPS_CACHE_MAX_AGE_DAYS 天沒更新（保護：萬一
             連續幾個週六都因為 Invesco 406／假期跳過，不能無限期沿用舊
             EPS）-> full。
          4. 快取的 eps_as_of 格式壞掉、讀不出日期 -> full（保守，壞資料不硬撐）。
          5. 以上都不是 -> price。
      - "monthly"（2026-09-25 起 TOPIX：日股持股與 EPS 預估變動慢，不需要
        每週整套重抓）：規則同上，但條件 1 改成「台北時區今天是本月第一個
        週六」（is_first_saturday_of_month()），條件 3 的過期門檻改用
        EPS_CACHE_MAX_AGE_DAYS_MONTHLY（35 天，涵蓋月與月之間偶爾錯過第一個
        週六——例如那天剛好撞到 Invesco 式的暫時性抓取失敗——的緩衝）。
        兩種 full_refresh 的股價（ETF 本身、成分股、加權遠期本益比、圖表股價
        線）都不受影響，PRICE 模式每天照跑，只有「整套重抓」的頻率不同。
    """
    if cli_mode in ("full", "price"):
        return cli_mode, f"--mode {cli_mode}（明示）"
    is_saturday = now_taipei.weekday() == 5  # Monday=0 .. Saturday=5 .. Sunday=6
    if full_refresh == "monthly":
        if is_saturday and is_first_saturday_of_month(now_taipei.date()):
            return "full", "台北時區今天是本月第一個週六（TOPIX 每月更新一次）"
        max_age_days = EPS_CACHE_MAX_AGE_DAYS_MONTHLY
        freshness_suffix = "且非本月第一個週六"
    else:
        if is_saturday:
            return "full", "台北時區今天是週六"
        max_age_days = EPS_CACHE_MAX_AGE_DAYS
        freshness_suffix = "且非週六"
    if eps_cache is None:
        return "full", "沒有 EPS 快取（第一次跑或快取遺失）"
    eps_as_of = eps_cache.get("eps_as_of")
    try:
        age_days = (now_taipei.date() - datetime.strptime(eps_as_of, "%Y-%m-%d").date()).days
    except (TypeError, ValueError):
        return "full", f"EPS 快取的 eps_as_of 格式壞掉（{eps_as_of!r}）"
    if age_days > max_age_days:
        return "full", f"EPS 快取已 {age_days} 天沒更新（> {max_age_days} 天門檻）"
    return "price", f"EPS 快取新鮮（{age_days} 天前，as of {eps_as_of}）{freshness_suffix}"


# ---------------------------------------------------------------------------
# Holdings — fetch + parse + cache fallback, three issuers (VanEck xlsx／
# SSGA xlsx／Invesco JSON), one shared fallback wrapper (get_holdings_with_fallback
# below). Every parse_* function returns (as_of, holdings, non_equity):
#   holdings    — list of {"ticker","raw_ticker_field","name","weight_pct"}，
#                 只放看起來像股票的列（yfinance 抓不抓得到是後面的事）。
#   non_equity  — list of {"ticker","name","weight_pct","reason"}，現金／期貨／
#                 CVR 等特殊有價證券／SEC 短倉抵銷列——不進 EPS 計算，但權重
#                 要讓讀者看得到（見 build_fund() 的 non_equity_weight_pct）。
# ---------------------------------------------------------------------------

EQUITY_TICKER_RE = re.compile(r"^[A-Z]{1,6}(\.[A-Z])?$")  # "NVDA"／"BRK.B"；數字或符號一律不算股票代碼


def fetch_holdings_xlsx(cfg: dict) -> bytes:
    r = requests.get(cfg["holdings_url"], headers={"User-Agent": UA}, cookies=cfg["holdings_cookies"],
                      timeout=30, allow_redirects=True)
    r.raise_for_status()
    ct = r.headers.get("content-type", "")
    if "spreadsheet" not in ct and "excel" not in ct and "octet-stream" not in ct:
        raise RuntimeError(f"unexpected content-type {ct!r} (body len={len(r.content)}) from "
                            f"{cfg['holdings_url']} — VanEck page format may have changed, or this "
                            f"now needs a browser session (disclaimer gate cookie stopped working)")
    if len(r.content) < 500:
        raise RuntimeError(f"suspiciously small response ({len(r.content)} bytes) from {cfg['holdings_url']}")
    return r.content


def parse_holdings_xlsx(raw: bytes) -> tuple[str, list[dict]]:
    df = pd.read_excel(io.BytesIO(raw), header=None)
    header_row_idx = None
    for i in range(min(6, len(df))):
        row_vals = [str(v).strip() for v in df.iloc[i].tolist()]
        if "Number" in row_vals:
            header_row_idx = i
            break
    if header_row_idx is None:
        raise RuntimeError("could not locate header row ('Number' column) in holdings sheet")

    title = str(df.iloc[0, 0]) if len(df) else ""
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", title)
    as_of = f"{m.group(3)}-{m.group(1)}-{m.group(2)}" if m else None

    cols = [str(c).strip() for c in df.iloc[header_row_idx].tolist()]
    body = df.iloc[header_row_idx + 1:].copy()
    body.columns = cols

    def _find_col(*needles):
        for c in cols:
            if all(n.lower() in c.lower() for n in needles):
                return c
        return None

    number_col = _find_col("Number")
    ticker_col = _find_col("Ticker")
    name_col = _find_col("Holding Name")
    weight_col = _find_col("% of Net Assets")
    if not all([number_col, ticker_col, name_col, weight_col]):
        raise RuntimeError(f"holdings sheet missing expected columns; got {cols!r}")

    rows = []
    for _, row in body.iterrows():
        n = row[number_col]
        try:
            int(n)
        except (TypeError, ValueError):
            break  # 撞到 footer 免責聲明列，資料列結束
        ticker_raw = str(row[ticker_col]).strip() if pd.notna(row[ticker_col]) else ""
        name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
        w_raw = row[weight_col]
        try:
            weight_pct = float(str(w_raw).replace("%", "").strip())
        except (TypeError, ValueError):
            weight_pct = None
        if not ticker_raw or ticker_raw in ("--", "nan") or name in ("Other/Cash",) or "CASH" in ticker_raw.upper():
            continue  # 現金／餘額列，不是個股
        yf_ticker = ticker_raw.split()[0]  # "AMD US" -> "AMD"；"NVDA" -> "NVDA"
        rows.append({"ticker": yf_ticker, "raw_ticker_field": ticker_raw, "name": name, "weight_pct": weight_pct})

    if as_of is None or not rows:
        raise RuntimeError(f"parsed 0 holdings or missing as-of date (as_of={as_of!r}, n_rows={len(rows)})")
    return as_of, rows  # VanEck 現金列在上面已經濾掉、沒有另外回報權重——沿用既有行為，不動它的呼叫端／測試


# ---------------------------------------------------------------------------
# SPY (State Street SPDR) — daily holdings xlsx，直接可下載，不需要 cookie／
# disclaimer 閘門（跟 VanEck 不同）。2026-09-24 實測欄位：Name／Ticker／
# Identifier／SEDOL／Weight／Sector／Shares Held／Local Currency，權重欄本身
# 就是數字（不是「19.43%」這種字串），"As of DD-Mon-YYYY" 在第 3 列。
# ---------------------------------------------------------------------------


def fetch_ssga_holdings_xlsx(cfg: dict) -> bytes:
    r = requests.get(cfg["holdings_url"], headers={"User-Agent": UA}, timeout=30, allow_redirects=True)
    r.raise_for_status()
    ct = r.headers.get("content-type", "")
    if "spreadsheet" not in ct and "excel" not in ct and "octet-stream" not in ct:
        raise RuntimeError(f"unexpected content-type {ct!r} (body len={len(r.content)}) from "
                            f"{cfg['holdings_url']} — SSGA page format may have changed")
    if len(r.content) < 500:
        raise RuntimeError(f"suspiciously small response ({len(r.content)} bytes) from {cfg['holdings_url']}")
    return r.content


def parse_ssga_holdings_xlsx(raw: bytes) -> tuple[str, list[dict], list[dict]]:
    df = pd.read_excel(io.BytesIO(raw), header=None)
    header_row_idx = None
    for i in range(min(8, len(df))):
        row_vals = [str(v).strip() for v in df.iloc[i].tolist()]
        if "Name" in row_vals and "Ticker" in row_vals and "Weight" in row_vals:
            header_row_idx = i
            break
    if header_row_idx is None:
        raise RuntimeError("could not locate header row ('Name'/'Ticker'/'Weight' columns) in SSGA holdings sheet")

    as_of = None
    for i in range(header_row_idx):
        # "As of 23-Sep-2026" 這個值實測落在 "Holdings:" 那一列的第 2 欄（col 0
        # 是標籤），所以整列都要找，不能只看第 1 欄。
        row_text = " ".join(str(v) for v in df.iloc[i].tolist() if pd.notna(v))
        m = re.search(r"(\d{1,2})-([A-Za-z]{3})-(\d{4})", row_text)
        if m:
            try:
                as_of = datetime.strptime(m.group(0), "%d-%b-%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass
            break

    cols = [str(c).strip() for c in df.iloc[header_row_idx].tolist()]
    body = df.iloc[header_row_idx + 1:].copy()
    body.columns = cols

    def _find_col(name):
        for c in cols:
            if c.lower() == name.lower():
                return c
        return None

    name_col, ticker_col, weight_col = _find_col("Name"), _find_col("Ticker"), _find_col("Weight")
    identifier_col = _find_col("Identifier")
    if not all([name_col, ticker_col, weight_col]):
        raise RuntimeError(f"SSGA holdings sheet missing expected columns; got {cols!r}")

    rows, non_equity = [], []
    for _, row in body.iterrows():
        name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
        if not name:
            break  # 撞到資料列結束（後面是免責聲明的長文字段落）
        ticker_raw = str(row[ticker_col]).strip() if pd.notna(row[ticker_col]) else ""
        identifier = str(row[identifier_col]).strip() if identifier_col and pd.notna(row[identifier_col]) else ""
        w_raw = row[weight_col]
        try:
            weight_pct = float(w_raw)
        except (TypeError, ValueError):
            try:
                weight_pct = float(str(w_raw).replace("%", "").strip())
            except (TypeError, ValueError):
                weight_pct = None
        if not ticker_raw or ticker_raw in ("-", "--", "nan"):
            non_equity.append({"ticker": None, "name": name, "weight_pct": weight_pct,
                                "reason": "現金／餘額列（SSGA 持股表無 ticker）"})
            continue
        if not EQUITY_TICKER_RE.match(ticker_raw) or "CVR" in identifier.upper():
            # 例：2026-09-24 這份表裡的 TPG INC，ticker 是識別碼「2602335D」不是
            # 交易代碼，Identifier 帶 CVR（Contingent Value Right，併購後的或有價值權利
            # 憑證，不是普通股）——排除但保留權重可見。
            non_equity.append({"ticker": ticker_raw, "name": name, "weight_pct": weight_pct,
                                "reason": "非普通股（CVR／特殊有價證券），yfinance 無對應報價"})
            continue
        rows.append({"ticker": ticker_raw, "raw_ticker_field": ticker_raw, "name": name, "weight_pct": weight_pct})

    if as_of is None or not rows:
        raise RuntimeError(f"parsed 0 holdings or missing as-of date (as_of={as_of!r}, n_rows={len(rows)})")
    return as_of, rows, non_equity


# ---------------------------------------------------------------------------
# QQQ (Invesco) — 基金頁「All QQQ holdings」表格背後的 JSON API，見
# FUND_REGISTRY["QQQ"] 的註解；純 requests.get() 不需要 cookie。
# ---------------------------------------------------------------------------


# 2026-09-24 實測：這個端點偶爾會回 406（不是真的擋純 requests——同一組
# headers、隔幾秒重試就恢復 200），看起來是前面 Varnish／WAF 對短時間內連續
# request 的暫時性節流，不是永久需要瀏覽器。所以這裡跟 yfinance 一樣做「重試
# 幾次、間隔遞增」，406 仍失敗才真正報錯（往上交給 get_holdings_with_fallback
# 退回快取）。
INVESCO_406_RETRY_BACKOFFS_S = [10, 30, 60, 90]


def fetch_invesco_holdings_json(cfg: dict) -> dict:
    last_exc = None
    for attempt, wait_s in enumerate([0] + INVESCO_406_RETRY_BACKOFFS_S):
        if wait_s:
            print(f"[etf_dash] Invesco holdings API not returning JSON yet; retrying in {wait_s}s "
                  f"({attempt}/{len(INVESCO_406_RETRY_BACKOFFS_S)}): {last_exc}", file=sys.stderr)
            time.sleep(wait_s)
        try:
            r = requests.get(cfg["holdings_url"], params=cfg["holdings_params"],
                              headers={"User-Agent": UA, "Accept": "application/json, text/plain, */*",
                                        "Referer": cfg["holdings_page_url"], "Origin": "https://www.invesco.com"},
                              timeout=30)
            # 406／403／429／5xx 或 2xx 卻不是 json（實測還遇過 200 但
            # content-type text/plain 的過渡態）都當同一種暫時性節流處理，
            # 留到重試預算耗盡才真正報錯往上交給 get_holdings_with_fallback
            # 退回快取。
            if r.status_code >= 400:
                raise RuntimeError(f"{r.status_code} from {cfg['holdings_url']}")
            ct = r.headers.get("content-type", "")
            if "json" not in ct:
                raise RuntimeError(f"unexpected content-type {ct!r} (status {r.status_code}) "
                                    f"from {cfg['holdings_url']}")
            return r.json()
        except (RuntimeError, requests.RequestException) as e:
            last_exc = e
    raise RuntimeError(f"Invesco holdings API still not returning JSON after "
                        f"{len(INVESCO_406_RETRY_BACKOFFS_S) + 1} attempts — "
                        f"Invesco API format may have changed, or this now needs a browser session "
                        f"(last error: {last_exc})") from last_exc


# securityTypeCode 值見 2026-09-24 實測 QQQ 回應：COM（普通股）／ADR／DRNY（紐約
# 存託憑證，如 ASML）算股票；CURR（現金）／CURRCOL（現金擔保品）／IFUT（指數
# 期貨）／SYN（期貨對應的合成抵銷列，權重通常是負的）都不是個股。
INVESCO_EQUITY_SECURITY_TYPES = {"COM", "ADR", "DRNY"}


def parse_invesco_holdings_json(data: dict) -> tuple[str, list[dict], list[dict]]:
    as_of = data.get("effectiveDate")
    holdings = data.get("holdings") or []
    if not as_of or not holdings:
        raise RuntimeError(f"Invesco holdings JSON missing effectiveDate or holdings (as_of={as_of!r}, "
                            f"n={len(holdings)})")
    rows, non_equity = [], []
    for h in holdings:
        ticker_raw = (h.get("ticker") or "").strip()
        # 2026-09-24 實測：issuerName 偶爾帶 HTML 實體（如 "CASH &amp; EQUIVALENTS"），
        # 不轉回來的話畫面上會被 JS 的 esc() 再跳脫一次變成 "&amp;amp;"。
        name = html.unescape(h.get("issuerName") or "") or ticker_raw or "（無名稱）"
        weight_pct = h.get("percentageOfTotalNetAssets")
        sec_type = (h.get("securityTypeCode") or "").strip().upper()
        if not ticker_raw or sec_type not in INVESCO_EQUITY_SECURITY_TYPES or not EQUITY_TICKER_RE.match(ticker_raw):
            non_equity.append({"ticker": ticker_raw or None, "name": name, "weight_pct": weight_pct,
                                "reason": f"非個股（{h.get('securityTypeName') or sec_type or '無資料'}），"
                                          f"不計入 EPS"})
            continue
        rows.append({"ticker": ticker_raw, "raw_ticker_field": ticker_raw, "name": name, "weight_pct": weight_pct})

    if not rows:
        raise RuntimeError(f"parsed 0 equity holdings from Invesco JSON (as_of={as_of!r})")
    return as_of, rows, non_equity


# ---------------------------------------------------------------------------
# TAIEX (台灣加權指數) — 不是追蹤型 ETF，沒有發行商持股清單可下載。改用 TWSE
# 公開資料自行機械估算近似持股：
#   - 上市公司基本資料（t187ap03_L）：每家公司「已發行普通股數或TDR原股
#     發行股數」欄位——普通股在外流通股數，不含特別股。
#   - 個股日成交資訊（STOCK_DAY_ALL）：當天收盤價。
#   市值 = 股數 × 收盤價；用「公司代號」（4 位數字）比對兩份資料——TWSE 的
#   ETF／特別股／TDR 都不會出現在 t187ap03_L 這份「公司」清單裡（它們不是
#   公司本身，是公司或指數之上的證券包裝），這個 join 天然把它們濾掉，不需要
#   額外黑名單；「F-」開頭的外國企業註冊股（在台灣掛牌普通股者）視同一般
#   成分股（它們是公司清單裡的正常一列）。這是近似：真正 TAIEX 編製規則另有
#   股利／除權息與少數細節調整，這裡沒有重現，只用「普通股數 × 收盤價」排序
#   ——2026-09-24 實測 TSMC 權重約 41%，量級與市場認知相符，可接受為近似基礎。
#   只對市值前 TAIEX_TOP_N 檔抓 yfinance eps_trend（全市場上千檔逐檔抓不現實）
#   ——weight_pct 是「佔全市場總市值」的原始比例，不重新正規化到 100%，這樣
#   sum(weight_pct) 本身就是 Top-N 對全市場的涵蓋率（跟 excluded／non_equity
#   的權重概念一致，見 build_methods_note_zh 的 TAIEX 專屬段落）。
#   2026-09-24 實測：兩個 openapi.twse.com.tw 端點純 requests.get()、不需要
#   cookie／瀏覽器即可拿到完整 JSON——但這是從境外（非台灣）IP 測試的，
#   GitHub Actions runner 的實際可達性未另外驗證；擋掉的話 get_holdings_with_fallback()
#   一樣會退回上次成功的 holdings_cache，不會讓整檔失敗。
# ---------------------------------------------------------------------------

TWSE_COMPANY_LIST_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
TWSE_STOCK_DAY_ALL_URL = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
TAIEX_TOP_N = 150  # 2026-09-24 實測涵蓋全市場總市值約 92%；實際數字每次 FULL 動態算出，見 LAST_TAIEX_UNIVERSE_STATS

# ---------------------------------------------------------------------------
# 風格快照／報酬貢獻的產業分解 — 2026-09-26 加。台股（TAIEX／0050）用 TWSE
# 官方「產業別」代碼（跟 scripts/active_etf/security_meta.py 同一組 TWSE
# OpenAPI／同一套代碼表，但依本任務指示在 etf_dash 這邊重新實作、不 import
# active_etf——兩邊各自維護一份小小的靜態表，代碼表本身是 TWSE 官方標準，
# 不會因為兩邊分開放而產生分歧風險）。這份表就是
# scripts/build_price_momentum_tw.py::SECTOR_MAP 的內容（TWSE／證交所公告的
# 標準產業別代碼，公開穩定的對照表，不是需要另外驗證的私有資料）。
# ---------------------------------------------------------------------------

TWSE_SECTOR_MAP = {
    "01": "水泥", "02": "食品", "03": "塑膠", "04": "紡織纖維", "05": "電機機械",
    "06": "電器電纜", "08": "玻璃陶瓷", "09": "造紙", "10": "鋼鐵", "11": "橡膠",
    "12": "汽車", "14": "建材營造", "15": "航運", "16": "觀光餐旅", "17": "金融保險",
    "18": "貿易百貨", "19": "綜合", "20": "其他", "21": "化學", "22": "生技醫療",
    "23": "油電燃氣", "24": "半導體", "25": "電腦及週邊設備", "26": "光電",
    "27": "通信網路", "28": "電子零組件", "29": "電子通路", "30": "資訊服務",
    "31": "其他電子", "32": "文化創意", "33": "農業科技", "34": "電子商務",
    "35": "綠能環保", "36": "數位雲端", "37": "運動休閒", "38": "居家生活",
}

TW_INDUSTRY_MAP_CACHE = ROOT / "data" / "etf_dash" / "tw_industry_map.json"


def fetch_tw_industry_map() -> dict[str, str]:
    """單獨一次 requests.get()（跟 fetch_twse_taiex_universe() 抓的是同一個
    端點 t187ap03_L，但這裡獨立呼叫，不依賴 TAIEX 這次 run 有沒有一起跑）——
    回傳 {4 位數公司代號: 產業別中文名稱}。失敗時呼叫端（get_tw_industry_map()）
    會退回磁碟快取，跟其他持股來源同一套 fallback 哲學。"""
    r = requests.get(TWSE_COMPANY_LIST_URL, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    companies = r.json()
    if not isinstance(companies, list) or not companies:
        raise RuntimeError(f"unexpected/empty response from {TWSE_COMPANY_LIST_URL}")
    out = {}
    for c in companies:
        code = str(c.get("公司代號", "")).strip()
        if len(code) != 4 or not code.isdigit():
            continue
        ind_code = str(c.get("產業別", "")).strip()
        out[code] = TWSE_SECTOR_MAP.get(ind_code, "未分類")
    if not out:
        raise RuntimeError("parsed 0 rows from TWSE company list")
    return out


def get_tw_industry_map() -> dict[str, str]:
    """FULL 模式週期性重抓＋磁碟快取，跟 EPS 快取同一個「抓不到就用上次成功
    的」設計——這份資料（公司的 TWSE 產業別）本來就變動很慢，不需要每天都
    打這個端點。"""
    try:
        m = fetch_tw_industry_map()
        TW_INDUSTRY_MAP_CACHE.parent.mkdir(parents=True, exist_ok=True)
        TW_INDUSTRY_MAP_CACHE.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        return m
    except Exception as e:  # noqa: BLE001
        print(f"[etf_dash] WARNING fetch_tw_industry_map failed ({e}), falling back to cache", file=sys.stderr)
        if TW_INDUSTRY_MAP_CACHE.exists():
            try:
                return json.loads(TW_INDUSTRY_MAP_CACHE.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass
        return {}


# SPDR 9 檔美股產業 ETF 各自對應的中文短標籤——用它們各自的官方持股清單
# （data/etf_dash/holdings_cache/{ETF}.json，這 9 檔本身就是每週或更頻繁重抓
# 一次）當「這檔股票屬於哪個 GICS 類股」的免費副產品：SSGA 持股表本身的
# "Sector" 欄實測對 SPY／各產業 ETF 都是空值「-」（2026-09-26 實測，不是
# parser 沒抓到），沒有其他免費、可機械讀取的個股 GICS 分類來源，這 9 檔
# ETF 的持股清單本身就是「屬於這個類股的股票名單」，拿來反查最省成本
# （見 build_us_sector_lookup()）——SPY／RSP／QQQ 的風格快照／報酬貢獻產業
# 分解都靠這份反查表，覆蓋率受限於這 9 檔＋XLRE／XLU（2026-09-26 加，見下方
# SECTOR_LOOKUP_ONLY_LABEL_ZH——這兩檔本身不當顯示用基金，見 FUND_REGISTRY
# 上方 2026-09-25 註解，只為了反查表額外抓持股）的持股總和，非重疊的成分股
# 歸「未分類」。
SECTOR_ETF_LABEL_ZH = {
    "XLK": "科技", "XLF": "金融", "XLE": "能源", "XLV": "醫療保健", "XLI": "工業",
    "XLY": "非必需消費", "XLP": "必需消費", "XLC": "通訊服務", "XLB": "原物料",
}

# 2026-09-26 coordinator 回饋：XLRE（不動產）／XLU（公用事業）不當成顯示用的
# 基金（不進 FUND_REGISTRY、不出現在導覽／總覽，任務原本的 9 檔美股產業 ETF
# 拍板刻意跳過這兩檔），但只為了 ticker→sector 反查表而抓它們的持股，能讓
# SPY／RSP／QQQ 的 REITs／公用事業成分股不再全部落進「未分類」——跟 9 檔
# 顯示用的產業 ETF 同一套 SSGA 持股 xlsx 格式，直接重用
# fetch_ssga_holdings_xlsx()／parse_ssga_holdings_xlsx()，只是傳一個不在
# FUND_REGISTRY 裡的最小 cfg dict 進去；持股快取仍然寫進
# data/etf_dash/holdings_cache/{XLRE,XLU}.json（跟其他基金同一個目錄，同一套
# 「抓不到就退回上次快取」邏輯），但兩者永遠不會出現在 docs/etf-dash/data/
# 或總覽頁——build_fund()／main() 的主迴圈只處理 FUND_REGISTRY 裡的 key。
SECTOR_LOOKUP_ONLY_LABEL_ZH = {"XLRE": "不動產", "XLU": "公用事業"}
SECTOR_LOOKUP_ONLY_CFG = {
    "XLRE": {"source": "ssga",
             "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlre.xlsx"},
    "XLU": {"source": "ssga",
            "holdings_url": "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-xlu.xlsx"},
}


def refresh_sector_lookup_only_holdings() -> None:
    """每次 run 都嘗試重抓 XLRE／XLU 持股（純粹為了下面 build_us_sector_lookup()
    的反查表，見上方註解）——失敗（xlsx 格式改版、被擋）不拋例外，直接跳過
    那一檔，沿用上次寫進 holdings_cache 的版本（若有）；兩者都沒抓過也沒有
    快取，反查表就是少這兩檔的資料，不影響其他任何功能。"""
    for etf_key, cfg in SECTOR_LOOKUP_ONLY_CFG.items():
        try:
            raw = fetch_ssga_holdings_xlsx(cfg)
            as_of, rows, non_equity = parse_ssga_holdings_xlsx(raw)
            cache_path = HOLDINGS_CACHE_DIR / f"{etf_key}.json"
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps({
                "as_of": as_of, "holdings": rows, "non_equity": non_equity,
                "source_url": cfg["holdings_url"], "fetched_at": datetime.now(timezone.utc).isoformat(),
            }, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            print(f"[etf_dash] WARNING refresh_sector_lookup_only_holdings: {etf_key} failed ({e}), "
                  f"sector lookup falls back to any existing cache for it", file=sys.stderr)


def build_us_sector_lookup() -> dict[str, str]:
    """讀 9 檔 SPDR 產業 ETF ＋ XLRE／XLU（僅供反查，見上方註解）各自的
    holdings_cache，回傳 {ticker: 中文類股標籤}。某檔快取不存在／壞掉就跳過
    那一檔（不讓整個查找表失敗），這是「盡量湊」的查找表，不是權威資料源。"""
    lookup: dict[str, str] = {}
    all_labels = {**SECTOR_ETF_LABEL_ZH, **SECTOR_LOOKUP_ONLY_LABEL_ZH}
    for etf_key, label in all_labels.items():
        path = HOLDINGS_CACHE_DIR / f"{etf_key}.json"
        if not path.exists():
            continue
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for h in d.get("holdings") or []:
            tk = h.get("ticker")
            if tk:
                lookup[tk] = label
    return lookup


def resolve_sector(ticker: str, raw_sector_field: str | None, us_sector_lookup: dict[str, str],
                    tw_industry_map: dict[str, str]) -> str | None:
    """單一入口把一檔成分股歸類到一個產業標籤，供報酬貢獻的產業彙總／風格
    快照共用：
      1. holdings 列自帶的 sector（目前只有 TOPIX／iShares JP CSV 有，見
         parse_ishares_jp_holdings_csv()）——直接用，不重新分類。
      2. 台股（ticker 以 .TW／.TWO 結尾）：用 4 位數代碼查 tw_industry_map。
      3. 其餘：用 build_us_sector_lookup() 建的 9 檔 SPDR 產業 ETF 反查表。
      查不到都回 None（呼叫端把 None 歸進「未分類」，不是排除）。"""
    if raw_sector_field:
        return raw_sector_field
    if ticker and (ticker.endswith(".TW") or ticker.endswith(".TWO")):
        code = ticker.split(".")[0]
        return tw_industry_map.get(code)
    return us_sector_lookup.get(ticker)

# parse_twse_taiex_universe() 側寫的全市場統計（TAIEX 方法論段落用，見
# build_methods_note_zh）。只有這次 run 真的重抓（非 cache fallback）才有值；
# main() 對每檔基金依序（非併發）呼叫 build_fund，讀取的時序安全。
LAST_TAIEX_UNIVERSE_STATS: dict | None = None


def _roc_date_to_iso(s: str | None) -> str | None:
    """TWSE 開放資料常見的民國年日期（如 "1150923" = 民國115年09月23日），
    轉 "YYYY-MM-DD"（西元）。"""
    if not s or len(s) < 6:
        return None
    try:
        roc_year = int(s[:-4])
        month = int(s[-4:-2])
        day = int(s[-2:])
        return f"{roc_year + 1911:04d}-{month:02d}-{day:02d}"
    except ValueError:
        return None


def fetch_twse_taiex_universe(cfg: dict) -> dict:
    companies = requests.get(TWSE_COMPANY_LIST_URL, headers={"User-Agent": UA}, timeout=30)
    companies.raise_for_status()
    prices = requests.get(TWSE_STOCK_DAY_ALL_URL, headers={"User-Agent": UA}, timeout=30)
    prices.raise_for_status()
    companies_json = companies.json()
    prices_json = prices.json()
    if not isinstance(companies_json, list) or not companies_json:
        raise RuntimeError(f"unexpected/empty response from {TWSE_COMPANY_LIST_URL}")
    if not isinstance(prices_json, list) or not prices_json:
        raise RuntimeError(f"unexpected/empty response from {TWSE_STOCK_DAY_ALL_URL}")
    return {"companies": companies_json, "prices": prices_json}


def parse_twse_taiex_universe(raw: dict) -> tuple[str, list[dict], list[dict]]:
    """回傳 (as_of, holdings[:TAIEX_TOP_N], non_equity=[])——見上方方法論說明。
    副作用：把全市場統計（可比對市值的公司數、涵蓋 90% 需要幾檔）寫進模組層
    LAST_TAIEX_UNIVERSE_STATS，供 build_fund_full() 組 TAIEX 專屬方法論文字。"""
    global LAST_TAIEX_UNIVERSE_STATS
    companies = raw["companies"]
    prices = raw["prices"]
    comp_by_code = {c["公司代號"]: c for c in companies
                     if len(c.get("公司代號", "")) == 4 and c["公司代號"].isdigit()}
    price_by_code = {p["Code"]: p for p in prices}

    as_of = None
    for p in prices:
        as_of = _roc_date_to_iso(p.get("Date"))
        if as_of:
            break

    rows = []
    for code, c in comp_by_code.items():
        p = price_by_code.get(code)
        if not p:
            continue
        try:
            shares = float(c.get("已發行普通股數或TDR原股發行股數") or 0)
            close = float(p.get("ClosingPrice") or 0)
        except (TypeError, ValueError):
            continue
        if shares <= 0 or close <= 0:
            continue
        rows.append({"code": code, "name": (c.get("公司簡稱") or "").strip(), "mkt_cap": shares * close})

    if as_of is None or not rows:
        raise RuntimeError(f"parsed 0 TAIEX universe rows or missing as-of date "
                            f"(as_of={as_of!r}, n_companies={len(companies)}, n_prices={len(prices)})")

    rows.sort(key=lambda r: -r["mkt_cap"])
    total_mkt_cap = sum(r["mkt_cap"] for r in rows)

    n_for_90 = None
    cum90 = 0.0
    for i, r in enumerate(rows, start=1):
        cum90 += r["mkt_cap"]
        if n_for_90 is None and cum90 / total_mkt_cap >= 0.90:
            n_for_90 = i
    LAST_TAIEX_UNIVERSE_STATS = {
        "n_total": len(rows), "n_for_90pct": n_for_90, "total_mkt_cap_twd": round(total_mkt_cap, 0),
    }

    holdings = []
    cum = 0.0
    for r in rows[:TAIEX_TOP_N]:
        cum += r["mkt_cap"]
        holdings.append({
            "ticker": f"{r['code']}.TW", "raw_ticker_field": r["code"], "name": r["name"],
            "weight_pct": round(r["mkt_cap"] / total_mkt_cap * 100, 4),
            "cum_weight_pct": round(cum / total_mkt_cap * 100, 4),
        })
    return as_of, holdings, []


# ---------------------------------------------------------------------------
# 0050 (元大台灣卓越50基金) — 元大投信官方持股頁的 SSR 內嵌資料。2026-09-24
# 實測：/product/detail/0050/ratio 這頁的持股表格不是靠額外 XHR 拉的（猜測
# etfapi.yuantaetfs.com 底下幾個常見端點都 404，或被 ectranslation 代理擋
# 掉，且那個代理端點本身只回傳欄位schema，不是資料）——用 Chrome 實際看網路
# 請求才發現：資料其實是 Nuxt.js 的 SSR（伺服器端渲染），完整 50 檔持股（含
# 「展開全部」要用的那些）已經內嵌在首次載入的 HTML 裡的一段
# `window.__NUXT__=(function(a,b,...){ return {...} })(實際值, 實際值, ...)`
# script——這是 Nuxt 用來去重複字串的序列化格式（函式體用短變數名代表值，
# 呼叫時才把真正的字串/數字當參數傳回代入）。純 requests.get() 這個 URL
# （不需要 cookie、不需要瀏覽器）就能拿到完整 HTML；問題只在於「解析」這段
# IIFE——要拿到真正資料等同於要『執行』這段 JS。這裡用 Node.js 子行程在 vm 沙箱內執行
# 它（見同目錄 _yuanta_nuxt_extract.js），因為：(1) GitHub Actions
# ubuntu-latest runner 本身就內建 Node.js（Actions runner 自己是用 Node 跑
# 的，不需要額外 actions/setup-node 步驟）；(2) 這段 payload 是靜態資料（沒
# 有任何 DOM／瀏覽器 API 依賴，eval 過程不會發出任何網路請求），風險等同解析
# 任何一份需要『執行』才能還原的序列化格式，不是「這頁需要瀏覽器」。找不到
# node、eval 失敗、或解析不出預期的 weightData 結構都當整體抓取失敗，退回
# holdings_cache（跟其他來源同一套 fallback 邏輯）。
# ---------------------------------------------------------------------------

YUANTA_NUXT_EXTRACT_JS = Path(__file__).resolve().parent / "_yuanta_nuxt_extract.js"


def _yyyymmdd_to_iso(s: str | None) -> str | None:
    """西元年 8 位數字日期（如 "20260924"）轉 "YYYY-MM-DD"——注意這跟
    _roc_date_to_iso() 不同：Yuanta PCF.trandate 用的是西元年，不是民國年。"""
    if not s or len(s) != 8 or not s.isdigit():
        return None
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"


def fetch_yuanta_holdings_page(cfg: dict) -> str:
    r = requests.get(cfg["holdings_url"], headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    if len(r.text) < 10_000:
        raise RuntimeError(f"suspiciously small response ({len(r.text)} chars) from {cfg['holdings_url']} "
                            f"— Yuanta page format may have changed")
    return r.text


def parse_yuanta_0050_holdings(html_text: str) -> tuple[str, list[dict], list[dict]]:
    m = re.search(r"window\.__NUXT__=.*?(?=</script>)", html_text, re.S)
    if not m:
        raise RuntimeError("could not locate window.__NUXT__ SSR payload in Yuanta holdings page "
                            "(page layout may have changed, or this now needs a browser session)")
    payload_js = m.group(0)

    if shutil.which("node") is None:
        raise RuntimeError("node executable not found — cannot evaluate Yuanta's Nuxt SSR payload "
                            "(see module comment above fetch_yuanta_holdings_page)")

    # payload 是外部網站內容：由 stdin 餵給 vm 沙箱（見 _yuanta_nuxt_extract.js），
    # 子行程只給 PATH，不帶 GITHUB_TOKEN 等環境變數。
    proc = subprocess.run(
        ["node", str(YUANTA_NUXT_EXTRACT_JS)],
        input=payload_js, capture_output=True, text=True, timeout=30,
        env={"PATH": os.environ.get("PATH", "")},
    )
    if proc.returncode != 0:
        raise RuntimeError(f"node eval of Yuanta SSR payload failed: {(proc.stderr or '').strip()[:500]}")
    try:
        data_items = json.loads(proc.stdout)
    except ValueError as e:
        raise RuntimeError(f"node eval of Yuanta SSR payload returned non-JSON stdout: {e}") from e

    weight_block = next((item for item in data_items if isinstance(item, dict) and "weightData" in item), None)
    if not weight_block:
        raise RuntimeError("Yuanta SSR payload parsed but no 'weightData' block found "
                            "(page structure may have changed)")
    wd = weight_block["weightData"] or {}
    fw = wd.get("FundWeights") or {}
    stock_rows = fw.get("StockWeights") or []
    if not stock_rows:
        raise RuntimeError("Yuanta SSR payload parsed but StockWeights is empty")

    trandate = (wd.get("PCF") or {}).get("trandate")
    as_of = _yyyymmdd_to_iso(trandate)
    if not as_of:
        raise RuntimeError(f"could not determine as-of date from PCF.trandate={trandate!r}")

    holdings = []
    for r in stock_rows:
        code = str(r.get("code") or "").strip()
        w = r.get("weights")
        if not code or w is None:
            continue
        holdings.append({"ticker": f"{code}.TW", "raw_ticker_field": code,
                          "name": r.get("name") or code, "weight_pct": float(w)})
    if not holdings:
        raise RuntimeError("parsed 0 equity holdings from Yuanta SSR payload")

    non_equity = []
    for group_key, reason in (("FutureWeights", "期貨（非個股，不計入 EPS）"),
                               ("ETFWeights", "ETF（非個股，不計入 EPS）"),
                               ("BondWeights", "債券（非個股，不計入 EPS）")):
        for r in (fw.get(group_key) or []):
            w = r.get("weights")
            non_equity.append({"ticker": r.get("code"), "name": r.get("name") or r.get("code") or "（無名稱）",
                                "weight_pct": float(w) if w is not None else None, "reason": reason})

    return as_of, holdings, non_equity


# ---------------------------------------------------------------------------
# TOPIX (iShares Core TOPIX ETF, 1475.T) — BlackRock Japan 的 holdings .ajax
# 端點直接回傳 CSV（純 requests.get()，不需要 cookie／disclaimer 閘門，跟
# VanEck 的美國／愛爾蘭站不同；2026-09-25 實測見 FUND_REGISTRY["TOPIX"] 上方
# 註解）。檔案格式：第 1 列 `基準日,"YYYY年M月D日"`、第 2 列空白（一個
# \xa0）、第 3 列起才是真正表頭（Ticker,Name,Sector,Asset Class,Market
# Value,Weight (%),...）；股票代碼是 TSE 4 碼（多數是數字，少數 2024 年後新
# 上市股用「3 位數字+英文字母」如 "285A"，一律用 `{code}.T` 對應 yfinance）。
# Asset Class 只有普通股是「株式」，其餘（キャッシュ／Cash Collateral and
# Margins／Futures）都不是個股——這裡用白名單（只認「株式」為股票，其他一律
# 歸類 non_equity）而不是黑名單列舉，理由：新出現、目前沒看過的 Asset Class
# 值（例如未來若把 REIT 另立分類）預設也會被排除，不會被誤當成股票算進 EPS
# ——TOPIX 本身編製規則也不含 J-REIT（那是獨立的 REIT 指數，這份持股清單裡
# 「不動産業」Sector 底下的名字是一般不動產開發／仲介公司，不是 REIT 信託，
# 不需要另外排除）。
# ---------------------------------------------------------------------------

ISHARES_JP_EQUITY_ASSET_CLASS = "株式"


def fetch_ishares_jp_holdings_csv(cfg: dict) -> bytes:
    r = requests.get(cfg["holdings_url"], headers={"User-Agent": UA}, timeout=30, allow_redirects=True)
    r.raise_for_status()
    ct = r.headers.get("content-type", "")
    if "csv" not in ct.lower():
        raise RuntimeError(f"unexpected content-type {ct!r} (body len={len(r.content)}) from "
                            f"{cfg['holdings_url']} — iShares Japan page/API format may have changed, "
                            f"or this now needs a browser session")
    if len(r.content) < 500:
        raise RuntimeError(f"suspiciously small response ({len(r.content)} bytes) from {cfg['holdings_url']}")
    return r.content


def parse_ishares_jp_holdings_csv(raw: bytes) -> tuple[str, list[dict], list[dict]]:
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()

    as_of = None
    for line in lines[:6]:
        m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", line)
        if m:
            as_of = f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
            break

    header_row_idx = None
    for i in range(min(8, len(lines))):
        try:
            probe = next(csv.reader([lines[i]]))
        except StopIteration:
            continue
        if "Ticker" in probe and "Weight (%)" in probe and "Asset Class" in probe:
            header_row_idx = i
            break
    if as_of is None or header_row_idx is None:
        raise RuntimeError(f"could not locate as-of date or header row ('Ticker'/'Weight (%)'/'Asset Class' "
                            f"columns) in iShares Japan holdings CSV (as_of={as_of!r})")

    body_rows = list(csv.reader(lines[header_row_idx:]))
    cols = body_rows[0]
    try:
        ticker_i, name_i = cols.index("Ticker"), cols.index("Name")
        asset_class_i, weight_i = cols.index("Asset Class"), cols.index("Weight (%)")
    except ValueError as e:
        raise RuntimeError(f"iShares Japan holdings CSV missing expected columns; got {cols!r}") from e
    # 2026-09-26 加：風格快照／報酬貢獻的產業分解要用——這份 CSV 本來就有
    # "Sector" 欄（見本檔上方 2026-09-25 註解），只是先前沒有欄位需要它，
    # 之前沒有解析出來。缺這欄不當錯誤（沿用既有的「找不到就是 None」慣例），
    # 只是那批持股的產業分解會缺值。
    sector_i = cols.index("Sector") if "Sector" in cols else None

    rows, non_equity = [], []
    need = max(ticker_i, name_i, asset_class_i, weight_i)
    for r in body_rows[1:]:
        if len(r) <= need:
            continue  # 空白／過短列（例如檔案裡單獨一個 \xa0 的那一行），不是資料列
        ticker_raw = r[ticker_i].strip()
        name = r[name_i].strip()
        if not ticker_raw or not name:
            continue
        asset_class = r[asset_class_i].strip()
        try:
            weight_pct = float(r[weight_i])
        except (TypeError, ValueError):
            weight_pct = None
        if asset_class != ISHARES_JP_EQUITY_ASSET_CLASS:
            non_equity.append({"ticker": ticker_raw, "name": name, "weight_pct": weight_pct,
                                "reason": f"非普通股（Asset Class「{asset_class}」），不計入 EPS"})
            continue
        sector = r[sector_i].strip() if sector_i is not None and len(r) > sector_i and r[sector_i].strip() else None
        rows.append({"ticker": f"{ticker_raw}.T", "raw_ticker_field": ticker_raw, "name": name,
                     "weight_pct": weight_pct, "sector": sector})

    if not rows:
        raise RuntimeError(f"parsed 0 equity holdings from iShares Japan holdings CSV (as_of={as_of!r})")
    return as_of, rows, non_equity


HOLDINGS_SOURCES = {
    "vaneck": (fetch_holdings_xlsx, lambda raw: (*parse_holdings_xlsx(raw), [])),
    "ssga": (fetch_ssga_holdings_xlsx, parse_ssga_holdings_xlsx),
    "invesco": (fetch_invesco_holdings_json, parse_invesco_holdings_json),
    "twse": (fetch_twse_taiex_universe, parse_twse_taiex_universe),
    "yuanta": (fetch_yuanta_holdings_page, parse_yuanta_0050_holdings),
    "ishares_jp": (fetch_ishares_jp_holdings_csv, parse_ishares_jp_holdings_csv),
}


def build_rsp_equal_weight_fallback() -> tuple[str, list[dict], list[dict], str]:
    """RSP 的第三層 fallback（見 get_holdings_with_fallback() 的 etf_key=="RSP"
    分支）——Invesco API 抓取失敗、且本地沒有 RSP 自己的 holdings_cache 時，讀
    SPY 的 holdings_cache（data/etf_dash/holdings_cache/SPY.json；SPY 每次
    build 成功都會寫這個檔，且 SPY 本來就跟 RSP 同一個 run 一起跑，見 workflow）
    對 SPY 目前的成分股清單做等權重近似——RSP 本身定義就是「S&P 500 成分股
    等權重」，這是失去官方持股資料時最貼近實際持股結構的近似。回傳
    (as_of, holdings, non_equity=[], source_note)；SPY 快取也沒有就直接失敗，
    呼叫端負責標記這是近似值（不是真實持股）。"""
    spy_cache_path = HOLDINGS_CACHE_DIR / "SPY.json"
    if not spy_cache_path.exists():
        raise RuntimeError("no RSP holdings cache and no SPY holdings cache to build an equal-weight fallback from")
    spy_cached = json.loads(spy_cache_path.read_text(encoding="utf-8"))
    spy_holdings = spy_cached.get("holdings") or []
    if not spy_holdings:
        raise RuntimeError("SPY holdings cache exists but has no holdings")
    n = len(spy_holdings)
    w = 100.0 / n
    holdings = [{"ticker": h["ticker"], "raw_ticker_field": h.get("raw_ticker_field", h["ticker"]),
                 "name": h["name"], "weight_pct": round(w, 4)} for h in spy_holdings]
    as_of = spy_cached.get("as_of")
    if not as_of:
        raise RuntimeError("SPY holdings cache has no as_of date")
    return as_of, holdings, [], spy_cached.get("source_url") or "SPY holdings cache (equal-weight approximation)"


RSP_APPROXIMATION_NOTE_ZH = "近似：以 SPY 成分股等權重計算（Invesco RSP 持股 API 抓取失敗，且無 RSP 自身持股快取）"


def get_holdings_with_fallback(etf_key: str, cfg: dict) -> tuple[str, list[dict], list[dict], str, bool, str | None]:
    """回傳 (as_of, holdings, non_equity, source_url, used_stale_cache, approximation_note_zh)。

    抓取失敗（含格式改版、被擋、需要瀏覽器）一律退回上次成功快取，並清楚
    標記 used_stale_cache=True——絕不用空資料覆蓋 data/etf_dash/holdings_cache/
    裡的好資料（快取檔只在成功解析時才寫入）。兩者都沒有才整檔失敗——除了
    RSP：見 build_rsp_equal_weight_fallback()，RSP 在前兩層都失敗時還有第三層
    （SPY 成分股等權重近似），approximation_note_zh 非 None 時呼叫端要把這句話
    清楚標在 JSON／頁面上，不能讓讀者誤以為是官方持股。"""
    cache_path = HOLDINGS_CACHE_DIR / f"{etf_key}.json"
    fetch_fn, parse_fn = HOLDINGS_SOURCES[cfg["source"]]
    try:
        raw = fetch_fn(cfg)
        as_of, rows, non_equity = parse_fn(raw)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({
            "as_of": as_of, "holdings": rows, "non_equity": non_equity, "source_url": cfg["holdings_url"],
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return as_of, rows, non_equity, cfg["holdings_url"], False, None
    except Exception as e:  # noqa: BLE001
        print(f"[etf_dash] WARNING holdings fetch failed for {etf_key}: {e}", file=sys.stderr)
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            print(f"[etf_dash] WARNING falling back to cached holdings for {etf_key} "
                  f"(as_of={cached['as_of']}, fetched_at={cached.get('fetched_at')})", file=sys.stderr)
            return (cached["as_of"], cached["holdings"], cached.get("non_equity", []),
                    cached.get("source_url", cfg["holdings_url"]), True, cached.get("approximation_note_zh"))
        if etf_key == "RSP":
            try:
                as_of, rows, non_equity, spy_src = build_rsp_equal_weight_fallback()
            except Exception as e2:  # noqa: BLE001
                raise RuntimeError(f"RSP: holdings fetch failed ({e}) and SPY equal-weight fallback "
                                    f"also failed ({e2})") from e2
            print(f"[etf_dash] WARNING RSP: no cache, falling back to SPY equal-weight approximation "
                  f"(as_of={as_of}, n={len(rows)})", file=sys.stderr)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps({
                "as_of": as_of, "holdings": rows, "non_equity": non_equity, "source_url": spy_src,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "approximation_note_zh": RSP_APPROXIMATION_NOTE_ZH,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            return as_of, rows, non_equity, spy_src, False, RSP_APPROXIMATION_NOTE_ZH
        raise RuntimeError(f"{etf_key}: holdings fetch failed and no cached fallback exists ({e})") from e


# ---------------------------------------------------------------------------
# yfinance — per-ticker EPS trend + last price (cached once per run, shared
# across both funds so overlapping constituents — NVDA/TSM/AMD/... — are
# only fetched once).
# ---------------------------------------------------------------------------


EPS_TREND_CALL_COUNT = 0  # 只在 FULL 模式的 fetch_ticker_eps_and_price() 裡加一，main() 結束時印出來稽核


def fetch_ticker_eps_and_price(ticker: str) -> dict:
    global EPS_TREND_CALL_COUNT
    result = {"ticker": ticker, "status": "ok", "reason": None}
    try:
        t = yf.Ticker(ticker)
        EPS_TREND_CALL_COUNT += 1
        eps_trend = yf_call_with_backoff(lambda: t.eps_trend, label=f"{ticker}.eps_trend")
    except Exception as e:  # noqa: BLE001
        result["status"] = "no_eps_data"
        result["reason"] = f"eps_trend fetch failed: {e}"
        return result
    if eps_trend is None or eps_trend.empty or "+1y" not in eps_trend.index:
        result["status"] = "no_eps_data"
        result["reason"] = "no +1y row in eps_trend"
        return result
    row = eps_trend.loc["+1y"]
    currency = None
    if "currency" in eps_trend.columns:
        cur_val = row.get("currency")
        currency = str(cur_val).upper() if cur_val is not None and not pd.isna(cur_val) else None
    currency = currency or "USD"
    current = row.get("current")
    if current is None or pd.isna(current):
        result["status"] = "no_eps_data"
        result["reason"] = "+1y current estimate missing"
        return result
    current = float(current)
    if current <= 0:
        result["status"] = "negative_or_zero_eps"
        result["reason"] = f"+1y EPS estimate is {current:.4f} {currency} (<=0)"
        result["eps_fy_next_local"] = current
        result["eps_currency"] = currency
        return result

    # 抓 ANCHOR_LINE_DEFS（PERIOD_DEFS 的 superset，多一個 "7d"）而不是只抓
    # PERIOD_DEFS——這裡是唯一一個真的呼叫 eps_trend 的地方，anchor line
    # fallback（見 anchor_history.py）需要的 7 天前錨點要在這裡一次拿到，不
    # 能事後回頭再抓一次（PRICE 模式完全不呼叫 eps_trend）。
    anchors = {}
    for key, col, _days in ANCHOR_LINE_DEFS:
        v = row.get(col)
        anchors[key] = None if v is None or pd.isna(v) else float(v)

    price = None
    price_currency = None
    market_cap = None
    try:
        fi = yf_call_with_backoff(lambda: t.fast_info, label=f"{ticker}.fast_info")
        price = fi.get("lastPrice") if hasattr(fi, "get") else getattr(fi, "last_price", None)
        if price is not None:
            price = float(price)
        # 2026-09-26 加：風格快照的市值分位數要用——fast_info 本身已經帶
        # marketCap（不需要另一次 API 呼叫），這裡只是多存一個既有欄位。
        mc = fi.get("marketCap") if hasattr(fi, "get") else getattr(fi, "market_cap", None)
        if mc is not None:
            market_cap = float(mc)
        # fast_info.currency 是這檔股票自己掛牌的計價幣別——多數持股是美股/ADR
        # 所以是 USD，但像 000660.KS 這類非美元掛牌股（SK Hynix 別名指過去的
        # 那一檔）是 KRW。價格幣別跟 eps_currency 未必相同來源但通常一致（同一
        # 家公司同一個掛牌），這裡分開存是為了不假設兩者一定相等。
        pc = fi.get("currency") if hasattr(fi, "get") else getattr(fi, "currency", None)
        price_currency = str(pc).upper() if pc else None
    except Exception as e:  # noqa: BLE001
        print(f"[etf_dash] WARNING fast_info failed for {ticker}: {e}", file=sys.stderr)

    result.update({
        "eps_fy_next_local": current,
        "eps_currency": currency,
        "eps_fy_next_anchors_local": anchors,  # {7d,30d,60d,90d}: EPS N days ago (local currency)
        "price": price,
        "price_currency": price_currency or "USD",
        "market_cap": market_cap,  # local currency，units 未統一（多數 USD），風格快照只用它排序取中位數
    })
    return result


# ---------------------------------------------------------------------------
# ETF price history
# ---------------------------------------------------------------------------


def fetch_etf_price_history(yf_ticker: str, calendar_days: int = 200) -> list[dict]:
    t = yf.Ticker(yf_ticker)
    hist = yf_call_with_backoff(
        lambda: t.history(start=(datetime.now() - timedelta(days=calendar_days)).strftime("%Y-%m-%d")),
        label=f"{yf_ticker}.history",
    )
    if hist is None or hist.empty:
        raise RuntimeError(f"no price history returned for {yf_ticker}")
    out = []
    for idx, r in hist.iterrows():
        # 2026-09-25 實測：yfinance 對 0050.TW 2026-09-24 這天回傳 Close=NaN（有
        # Volume 但沒有收盤價，上游資料缺口，非本檔程式問題）——不篩掉的話
        # NaN 會原封不動寫進 JSON（json.dumps 預設輸出字面 NaN，不是合法
        # JSON，前端 JSON.parse 會直接丟例外整頁掛掉），且會污染所有下游算式
        # （price_chg_pct／implied_pe_chg_pct 全部變 NaN）。當成那天沒有收盤價
        # （不是 0），_closest_close_on_or_before() 本來就會退回前一個有資料的
        # 交易日，跟其他來源「缺資料當天」的既有語意一致。
        if pd.isna(r["Close"]):
            continue
        out.append({"date": idx.strftime("%Y-%m-%d"), "close": round(float(r["Close"]), 4)})
    return out


def _closest_close_on_or_before(price_series: list[dict], target_date: str):
    candidates = [p for p in price_series if p["date"] <= target_date]
    return candidates[-1] if candidates else None


PRICE_BATCH_CHUNK_SIZE = 150  # 「chunk if needed」——單次 yf.download 帶太多檔容易逾時／被限速
PRICE_BATCH_PACING_S = 1.0    # 批次之間的節流（跟逐檔的 TICKER_FETCH_PACING_S 分開）


def fetch_prices_batch(tickers: list[str], calendar_days: int = 200) -> dict[str, list[dict]]:
    """PRICE 模式專用：一次（規模大就分幾批）用 yf.download 抓多檔股票的股價
    歷史，取代 FULL 模式逐檔 fetch_ticker_eps_and_price() 裡的 fast_info 呼叫
    ——後者對幾百檔要打幾百次個別請求，這裡合併成幾次批次請求，不只快，也
    比較不會觸發 yfinance 限速。這個函式本身完全不呼叫 eps_trend（不產生任何
    EPS 相關的 yfinance 呼叫），呼叫端（build_fund_price()）會記錄實際呼叫
    次數＝0 以供稽核。

    回傳 {ticker: [{"date","close"}, ...]}（依日期升冪排序）——沒抓到資料的
    ticker 直接不在回傳的 dict 裡（呼叫端要自己判斷缺席＝沒資料，不是回傳
    None／空列表）。"""
    uniq = sorted(set(tickers))
    start = (datetime.now() - timedelta(days=calendar_days)).strftime("%Y-%m-%d")
    out: dict[str, list[dict]] = {}
    chunks = [uniq[i:i + PRICE_BATCH_CHUNK_SIZE] for i in range(0, len(uniq), PRICE_BATCH_CHUNK_SIZE)]
    for i, chunk in enumerate(chunks):
        if i:
            time.sleep(PRICE_BATCH_PACING_S)
        df = yf_call_with_backoff(
            lambda chunk=chunk: yf.download(chunk, start=start, group_by="ticker", progress=False,
                                             auto_adjust=False, threads=True),
            label=f"batch price download chunk {i + 1}/{len(chunks)} ({len(chunk)} tickers)",
        )
        if df is None or df.empty:
            continue
        if len(chunk) == 1 or not isinstance(df.columns, pd.MultiIndex):
            # yf.download 對單一 ticker（即使傳的是長度 1 的 list）有時仍回傳
            # 非 MultiIndex 欄位，這裡當成「這個 chunk 只有一檔」處理。
            tk = chunk[0]
            if "Close" in df.columns:
                pts = [{"date": idx.strftime("%Y-%m-%d"), "close": round(float(v), 4)}
                       for idx, v in df["Close"].items() if pd.notna(v)]
                if pts:
                    out[tk] = pts
            continue
        top_level = set(df.columns.get_level_values(0))
        for tk in chunk:
            if tk not in top_level:
                continue
            sub = df[tk]
            if "Close" not in sub.columns:
                continue
            pts = [{"date": idx.strftime("%Y-%m-%d"), "close": round(float(v), 4)}
                   for idx, v in sub["Close"].items() if pd.notna(v)]
            if pts:
                out[tk] = pts
    return out


def _all_known_constituent_tickers() -> set[str]:
    """回填用——蒐集「目前 eps_cache 裡已知的全部基金」的全部成分股 ticker
    （每檔基金讀 data/etf_dash/eps_cache/{ETF}.json 的 "tickers" 字典，取
    status=="ok" 的那些，即 constituents 實際會用到的 ticker），外加每檔
    基金自己的 ETF ticker（cfg["yf_ticker"]）。刻意讀「目前已知的全部 17 檔」
    而不是只看這次 run 的 --etf 參數——回填的目的是讓 prices.jsonl 一次涵蓋
    全站，不是只涵蓋今天剛好跑到的那幾檔（見 backfill_price_history_if_needed()
    docstring）。某檔基金還沒有 eps_cache（例如全新加入、從沒 FULL 過）就
    跳過它的成分股，不讓整個回填失敗。"""
    tickers: set[str] = set()
    for etf_key, cfg in FUND_REGISTRY.items():
        tickers.add(cfg["yf_ticker"])
        cache_path = EPS_CACHE_DIR / f"{etf_key}.json"
        if not cache_path.exists():
            continue
        try:
            eps_cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for tk, info in (eps_cache.get("tickers") or {}).items():
            if info.get("status") == "ok":
                tickers.add(info.get("yf_ticker_used") or tk)
    return tickers


def backfill_price_history_if_needed(price_days: dict) -> dict:
    """2026-09-26 self-heal（coordinator 回饋：報酬貢獻不該乾等 ~3 個月讓
    prices.jsonl 自然累積到有用的覆蓋率）——price_days 現有天數不足
    price_history.MIN_TRADING_DAYS 天，就用一次批次 yfinance 下載（重用
    fetch_prices_batch()，跟 PRICE 模式每天已經在用的同一支函式，不是新的
    抓取路徑）把全站（目前 eps_cache 已知的 17 檔基金＋各自成分股＋各基金
    自己的 ETF ticker，見 _all_known_constituent_tickers()）一次補進
    ~100 個曆日的收盤價，寫回 data/etf_dash/prices.jsonl。已經有足夠天數
    （例如日常累積到門檻之後）就直接回傳原本傳進來的 price_days，不做任何
    事——這個函式在 main() 迴圈開始前呼叫一次，回傳值取代呼叫端手上的
    price_days（讓這次 run 馬上就能用回填到的歷史算報酬貢獻，不用等明天）。
    批次下載本身失敗（網路問題等）不拋例外，印警告後原樣回傳 price_days，
    跟其他一次性抓取失敗時的既有哲學一致（缺資料就是缺資料，不讓整個
    build 掛掉）。"""
    if not price_history.needs_backfill(price_days):
        return price_days
    tickers = sorted(_all_known_constituent_tickers())
    print(f"[etf_dash] price_history: only {len(price_days)} day(s) on file "
          f"(< {price_history.MIN_TRADING_DAYS}) — backfilling ~100 calendar days for "
          f"{len(tickers)} ticker(s) in one batched download", file=sys.stderr)
    try:
        batch = fetch_prices_batch(tickers, calendar_days=100)
    except Exception as e:  # noqa: BLE001
        print(f"[etf_dash] WARNING price_history backfill failed ({e}); contribution stays at low "
              f"coverage until it accumulates day-by-day", file=sys.stderr)
        return price_days
    merged = price_history.merge_ticker_series(price_days, batch)
    price_history.save_days(merged)
    n_new_days = len(merged) - len(price_days)
    print(f"[etf_dash] price_history: backfill done — {len(merged)} day(s) on file now "
          f"(+{n_new_days}), {sum(len(v) for v in batch.values())} ticker-day close(s) fetched", file=sys.stderr)
    return merged


def build_weight_methodology_note_zh(cfg: dict, holdings: list[dict]) -> str | None:
    """TAIEX 近似持股／0050 官方持股的權重方法論說明——只有 cfg["source"] in
    ("twse","yuanta") 才回傳非 None，其他四檔基金（官方完整持股清單本身就是
    100% 精確）不需要這段。回傳字串會被 build_methods_note_zh() 接在動態組出
    的一般段落後面。"""
    if cfg.get("source") == "twse":
        cap_share = round(sum(h["weight_pct"] or 0 for h in holdings), 2)
        stats = LAST_TAIEX_UNIVERSE_STATS
        if stats:
            return (
                f"TAIEX 本身不是追蹤型 ETF、沒有發行商持股清單可下載，本頁改用 TWSE 公開資料"
                f"（上市公司基本資料 t187ap03_L 的「已發行普通股數」× 個股日成交資訊 "
                f"STOCK_DAY_ALL 的收盤價）機械估算持股與權重，是近似值，除權息與少數編製細節"
                f"未重現。市值以「公司代號」（4 位數字）比對兩份"
                f"資料，天然排除 ETF／特別股／TDR（它們不是公司本身，不會出現在公司基本資料"
                f"清單裡）；「F-」開頭的外國企業註冊股（在台灣掛牌普通股者）視同一般成分股。"
                f"全市場 {stats['n_total']} 檔可比對到市值與股數，本頁只取權重前 {len(holdings)} 檔"
                f"（合計 {cap_share:.1f}% 全市場總市值；全市場約需 {stats['n_for_90pct']} 檔即可涵蓋 90%"
                f"權重），只對這 {len(holdings)} 檔抓 yfinance eps_trend——落在這個子集合之外的"
                f"成分股不計入本頁任何 EPS 相關計算，也不在完整持股明細裡。"
            )
        return (
            f"TAIEX 近似持股與權重估算方式同上（TWSE 公開資料機械估算），本頁取權重前 "
            f"{len(holdings)} 檔（合計 {cap_share:.1f}% 全市場總市值），只對這些檔抓 yfinance "
            "eps_trend；今天沿用上次成功抓取的持股快取，全市場涵蓋率統計未重新計算。"
        )
    if cfg.get("source") == "yuanta":
        return (
            "0050 的持股是元大投信官方持股頁（0050/ratio）SSR 頁面內嵌的完整權重資料（非"
            "近似），含股票、期貨等各類資產的權重——期貨（台股期貨／台灣50ETF股票期貨）等"
            "非個股部位見完整持股明細表的「非個股」列，不計入 EPS。"
        )
    return None


# ---------------------------------------------------------------------------
# EPS scope cutoff — 2026-09-25 加 TOPIX：~1,700 檔持股逐檔抓 yfinance
# eps_trend 不現實（時間、限速兩者都撐不住），只對依權重排序、累計達
# cfg["eps_scope_cutoff_pct"] 的最大權重成分股抓 EPS，見 FUND_REGISTRY["TOPIX"]
# 上方註解。cfg 沒有這個鍵的基金（其餘六檔）不受影響——select_eps_scope_tickers
# 只在 build_fund_full() 判斷 cfg.get("eps_scope_cutoff_pct") 為真值時才呼叫。
# ---------------------------------------------------------------------------


def select_eps_scope_tickers(holdings: list[dict], cutoff_pct: float) -> set[str]:
    """純函式：holdings 依權重由大到小排序後累加，回傳累計達 cutoff_pct（百分比，
    例如 90.0）所需的最小 ticker 集合。同一 ticker 若出現多次先加總權重再排序
    （目前各資料源的 holdings 本身 ticker 已經不重複，這裡多做一層聚合純粹是
    防禦性寫法，不依賴呼叫端先去重）。"""
    by_ticker: dict[str, float] = {}
    for h in holdings:
        by_ticker[h["ticker"]] = by_ticker.get(h["ticker"], 0.0) + (h["weight_pct"] or 0.0)
    ordered = sorted(by_ticker.items(), key=lambda kv: -kv[1])
    scoped: set[str] = set()
    cum = 0.0
    for tk, w in ordered:
        if cum >= cutoff_pct:
            break
        scoped.add(tk)
        cum += w
    return scoped


def build_eps_scope_note_zh(cfg: dict, holdings: list[dict], eps_scope_tickers: set[str] | None) -> str | None:
    """cfg 沒有設 eps_scope_cutoff_pct 時回傳 None（其餘六檔基金不受影響）。"""
    cutoff_pct = cfg.get("eps_scope_cutoff_pct")
    if not cutoff_pct or eps_scope_tickers is None:
        return None
    unique_tickers = {h["ticker"] for h in holdings}
    n_total = len(unique_tickers)
    scoped_weight = sum(h["weight_pct"] or 0 for h in holdings if h["ticker"] in eps_scope_tickers)
    return (
        f"{cfg['label_zh']}成分股達 {n_total} 檔，逐檔抓 yfinance EPS 預估在時間與 API 限速上都不現實"
        f"——本頁只對依權重排序、累計達 {cutoff_pct:.0f}% 的前 {len(eps_scope_tickers)} 檔抓 EPS"
        f"（實際累計權重 {scoped_weight:.2f}%），其餘 {n_total - len(eps_scope_tickers)} 檔較小權重成分股"
        "不進任何 EPS 相關計算（加權 EPS 修正、加權遠期本益比都只用涵蓋範圍內的名字，"
        "權重照原比例重新正規化——沿用既有 revisions_pct 覆蓋率邏輯，不是額外一套）；完整持股明細仍"
        "列出全部成分股，這些名字在下表「備註」欄標示「EPS 涵蓋門檻外」，可查但不計入計算。"
    )


def build_methods_note_zh(cfg: dict, constituents: list[dict], non_equity: list[dict],
                           long_eps: dict, dd_universe_size: int, periods: list[dict],
                           mode: str, eps_as_of: str, mode_reason: str,
                           weight_methodology_note_zh: str | None = None,
                           eps_scope_note_zh: str | None = None,
                           anchor_label_zh: str | None = None,
                           holdings_approximation_zh: str | None = None,
                           pe_excluded: list[dict] | None = None) -> str:
    """組 methods_note_zh——2026-09-24 加 QQQ／SPY 之前這段是寫死給 SMH／
    SMH_UCITS 看的（硬編「VanEck」「ASML」「SK Hynix」）。四檔基金共用同一個
    build_fund()，持股來源、非美元成分股、TICKER_ALIAS 用到哪些、長線指數
    覆蓋率與異常事件都因基金而異，所以這裡全部改成從當次算好的資料動態組，
    不對其他基金硬猜。"""
    mode_zh = "完整更新（FULL：重抓持股與每檔 EPS 估計）" if mode == "full" else "只更新股價（PRICE：EPS 沿用快取）"
    full_refresh = cfg.get("full_refresh", "weekly")
    # 2026-09-25 持有人拍板：TOPIX 改成每月第一個週六才 FULL（其餘六檔仍是
    # 每週六）——見 decide_mode() full_refresh 分支；這裡的文字跟著 cfg 動態
    # 產生，不是寫死「每週六」。
    cadence_zh = "每月第一個週六" if full_refresh == "monthly" else "每週六"
    cadence_period_zh = "兩次 FULL 之間" if full_refresh == "monthly" else "整週"
    parts = [
        f"本頁分層更新：{cadence_zh}（台北時區）完整重抓一次持股與每檔明年度 EPS 估計"
        f"（現在的 EPS 估計 as of {eps_as_of}），其餘日子只抓股價，跟上次 FULL 存的 EPS "
        "快取重新配對算「今日加權遠期本益比」——Exhibit 1 的期間表格（EPS 修正％／"
        f"股價漲跌／隱含本益比）因此{cadence_period_zh}不變，只有本益比跟「EPS 預估更新於...」那行"
        f"每天更新。這次是{mode_zh}（{mode_reason}）。",
    ]
    if holdings_approximation_zh:
        parts.append(
            f"{holdings_approximation_zh}——不是官方持股，權重是把 SPY 目前成分股平均分配（1/N），"
            "只在 Invesco 持股 API 失敗且本地也沒有 RSP 自身快取時才會用到這條路徑，"
            "見 build_etf_dash.py::build_rsp_equal_weight_fallback()。"
        )
    if weight_methodology_note_zh:
        parts.append(weight_methodology_note_zh)
    if eps_scope_note_zh:
        parts.append(eps_scope_note_zh)
    parts += [
        f"成分股權重與明細來自{cfg['holdings_issuer_zh']}（見 holdings_source_url，"
        "as of holdings_as_of，非 yfinance 前十大）。每檔成分股的 EPS 修正取 "
        "yfinance Ticker.eps_trend 的「明年度」(+1y) 估計，比較目前值與 7／30／"
        "60／90 天前值的百分比變動；ETF 加權 EPS 變動＝當期有資料成分股的"
        "權重重新正規化後加權平均（無資料或 EPS≤0 者見 excluded 清單，不進分子分母）。"
        "股價變動用 ETF 自身 yfinance 收盤價，取最接近錨點日期（不晚於當日）的收盤。"
        "隱含本益比變動＝(1+股價變動)/(1+EPS變動)−1。加權遠期本益比用調和平均"
        "（1/Σw·(EPS/股價)）。"
    ]

    # 2026-09-24：持有人擋下第一版上線，因為某期間的加權 EPS 變動被異常值拉走
    # （基期估計翻負號或趨近 0，比值本身就不穩定；見 classify_revision() 上方
    # 的 SPCX／ECHO／HON 案例說明）。這裡把每個期間各自的排除／封頂名單彙總
    # 成一段話，跟 Exhibit 1 底下的 periodsQualityNote 是同一份資料（見
    # period_exclusions／period_capped），只是這裡是文字版。
    total_excl = sum(len(p.get("period_exclusions") or []) for p in periods)
    total_capped = sum(len(p.get("period_capped") or []) for p in periods)
    if total_excl or total_capped:
        bits = []
        if total_excl:
            excl_examples = sorted(
                {e["ticker"] or e["name"] for p in periods for e in (p.get("period_exclusions") or [])})
            bits.append(f"基期（N 天前 EPS 估計）為負或相對現值過小（<{REVISION_BASE_MIN_RATIO:.0%}）"
                        f"的整筆排除，各期間合計 {total_excl} 筆（{'、'.join(excl_examples[:10])}"
                        f"{'等' if len(excl_examples) > 10 else ''}），比值不穩定不代表真實修正這麼多")
        if total_capped:
            capped_examples = sorted(
                {e["ticker"] or e["name"] for p in periods for e in (p.get("period_capped") or [])})
            bits.append(f"排除後單筆修正仍超過 ±{REVISION_CAP_PCT:.0f}% 的封頂在 ±{REVISION_CAP_PCT:.0f}%"
                        f"才拿去加權（原始值不丟棄），各期間合計 {total_capped} 筆"
                        f"（{'、'.join(capped_examples[:10])}{'等' if len(capped_examples) > 10 else ''}）")
        parts.append(
            "各期間成分股加權 EPS 變動先過濾兩層資料品質問題才加總：" + "；".join(bits) +
            "。逐筆明細（ticker、原始值、處理後的值、原因）見各期間 periods[].period_exclusions／"
            "periods[].period_capped 欄位，頁面 Exhibit 1 下方也有同一份摘要。"
        )

    # 2026-09-25 加：加權遠期本益比那條腿獨立的資料品質過濾（見
    # compute_weighted_forward_pe() 上方模組註解的 PGR 案例——PGR 的
    # eps_fy_next=1012、price=202.17，個股本益比 0.2x，把 XLF／RSP／SPY 的
    # 加權遠期本益比拖到不合理的個位數）。跟上面 EPS 修正% 那段是兩件不同的
    # 事：這裡管「當下這個估值站不站得住」，不是「這次比上次變動多少」。
    if pe_excluded:
        pe_examples = sorted({e["ticker"] or e["name"] for e in pe_excluded})
        parts.append(
            f"加權遠期本益比只用個股本益比（股價／明年度 EPS）落在 [{PE_EXCLUDE_MIN_X:g}x, "
            f"{PE_EXCLUDE_MAX_X:g}x] 區間內的成分股，區間外整檔排除、權重重新正規化——本次排除 "
            f"{len(pe_excluded)} 檔（{'、'.join(pe_examples[:10])}{'等' if len(pe_examples) > 10 else ''}），"
            "多半是 yfinance eps_fy_next 資料異常（如個股 EPS 估計偏離實際量級一個數量級以上），"
            "不代表真實估值。逐筆明細見 weighted_forward_pe.pe_excluded 欄位。"
        )

    non_equity_w = round(sum(e["weight_pct"] or 0 for e in non_equity), 2)
    if non_equity:
        top = sorted(non_equity, key=lambda e: abs(e["weight_pct"] or 0), reverse=True)[:6]
        examples = "、".join(f"{e['name']}（{e['weight_pct']:.2f}%）" if e.get("weight_pct") is not None
                             else f"{e['name']}" for e in top)
        parts.append(
            f"{cfg['holdings_issuer_zh']}的持股清單裡另有現金／期貨／特殊有價證券共 {len(non_equity)} 筆、"
            f"合計權重 {non_equity_w:.2f}%（{examples}），不是普通股，不計入 EPS 與本益比計算的分子分母，"
            "完整清單見 JSON 的 non_equity 欄位。"
        )

    pe_basis_ccy = cfg.get("pe_basis_currency", "USD")
    if pe_basis_ccy != "USD":
        parts.append(
            f"本基金本益比／股價的基準幣別是 {pe_basis_ccy}，不是美元——JSON 裡的 eps_fy_next_usd／"
            f"price_usd 兩個欄位沿用既有命名（跟其餘四檔美元基金共用同一套 schema），但這裡實際"
            f"存的是換算到 {pe_basis_ccy} 後的值，不是美元金額，使用時請以 weighted_forward_pe."
            "method／本段為準，不要照字面把欄位名當成美元。"
        )
    fx_tickers = [c for c in constituents
                  if c["eps_currency"] != pe_basis_ccy or c["price_currency"] != pe_basis_ccy]
    if fx_tickers:
        fx_list = "、".join(f"{c['name']}〈{c['ticker']}，{c['eps_currency']} 報表〉" for c in fx_tickers)
        parts.append(
            f"本基金有 {len(fx_tickers)} 檔成分股的 EPS 或股價不是{pe_basis_ccy}報表／{pe_basis_ccy}掛牌：{fx_list}。"
            f"這些名字先用當日匯率把 EPS 與股價分別換算成{pe_basis_ccy}再算比值，EPS修正%本身"
            "不需要換算（同幣別比較）。"
        )

    alias_notation, alias_substitution = [], []
    for c in constituents:
        used = c.get("yf_ticker_used")
        if not used or used == c["ticker"]:
            continue
        if used.replace("-", ".") == c["ticker"]:
            alias_notation.append((c["ticker"], used))
        else:
            alias_substitution.append((c["ticker"], used, c["name"]))
    if alias_notation:
        pairs = "、".join(f"{a}→{b}" for a, b in alias_notation)
        parts.append(f"雙類股代碼在持股欄位用點號、yfinance 用連字號，代碼轉換：{pairs}（見 TICKER_ALIAS，同一檔股票，不影響股數基礎）。")
    if alias_substitution:
        for orig, used, name in alias_substitution:
            parts.append(
                f"{name}在持股欄位標的代碼「{orig}」yfinance 查無報價，改用「{used}」取代（見 TICKER_ALIAS）"
                "——EPS 與股價都是替代標的本身的原始數字，不是換股比例調整過的，避免股數基礎不一致。"
            )

    parts.append(
        "Exhibit 2 畫的 EPS 指數來自 docs/dd-screener/latest.json 的 git 歷史"
        "（scripts/etf_dash/dd_eps_history.py），從 2026-05-19 起、每個有資料"
        "的交易日一個點，比 yfinance eps_trend 只記得 90 天長得多。權重固定用"
        "今天的持股權重，指數在第一個資料日訂為 100；股價同一天也 rebase 成 "
        "100，兩條線才能疊在同一個座標軸上比誰漲得快。"
    )
    uncovered = long_eps.get("uncovered_tickers") or []
    if uncovered:
        parts.append(
            f"{'／'.join(uncovered[:12])}{'等' if len(uncovered) > 12 else ''}"
            f"不在 dd-screener 母體裡（母體現有 {dd_universe_size} 檔美股大型股，見 docs/dd-screener/latest.json），"
            f"長線覆蓋率因此低於 100%（見 coverage_weight_pct，本基金 "
            f"{long_eps.get('coverage_weight_pct', 0):.1f}%），缺的那部分不計入分子分母，不是當作沒漲跌。"
        )
    if anchor_label_zh:
        parts.append(
            f"本基金 dd-screener 覆蓋率低於 {LONG_EPS_LINE_MIN_COVERAGE_PCT:.0f}% 門檻，Exhibit 2 改畫"
            f"anchor line（見 scripts/etf_dash/anchor_history.py）：每次 FULL 完整更新（{cadence_zh}）"
            "都會用這次抓到的 yfinance eps_trend 90／60／30／7 天前紀錄，算出一個 ETF 級 EPS 相對水準的 5 點快照"
            "（不需要額外呼叫 API——Exhibit 1 本來就要抓這些資料）；多次 FULL run 的快照再串接（chain-link：找"
            "新一次 run 裡日期不晚於上次存檔日期、最接近的錨點，用比例對齊上次存的水準）成一條連續的線，兩次 "
            "run 相距超過 90 天銜接不上時另起一段，只顯示斷點之後最新一段。過去每個點的水準都是「當次 FULL run "
            "當下的持股權重」算出來的，不是今天的權重回頭套用——這是跟 dd-screener 長線（固定用今天權重）唯一"
            f"的方法論差異。{anchor_label_zh}"
        )
    parts.append(
        "Koyfin 的預估資料是月頻更新，兩次更新之間同一個數字連著好幾週不變，"
        "所以這條線本來就該長得像階梯，不是平滑曲線。"
        "串接每一步都要過濾兩種假訊號：一是財年輪替——公司的財年結束後，"
        "「明年度」這個標籤指的年份會往後挪一年，若不處理，eps_fy_next 會"
        "無端跳一大截；判斷方式是看這一步的 eps_fy_next 是否落在前一天 "
        "eps_fy3（後年度估計）的 3% 以內，是的話用 eps_fy3 接續，不是財年輪替"
        "才用前一天的 eps_fy_next 當基準（見 classify_eps_step()）。二是原始資料"
        "本身的異常——同步驟同步過濾，整步跳過不計入指數也不計入覆蓋率。"
    )
    n_rollover = len(long_eps.get("rollover_events") or [])
    n_anomaly = len(long_eps.get("anomaly_events") or [])
    if n_rollover or n_anomaly:
        bits = []
        if n_rollover:
            bits.append(f"{n_rollover} 次財年輪替")
        if n_anomaly:
            explained = [e for e in (long_eps.get("anomaly_events") or []) if e.get("explanation")]
            bits.append(f"{n_anomaly} 次資料異常（{len(explained)} 次已對過帳確認根因，"
                        f"逐筆記錄見 chart.long_eps_index.anomaly_events）")
        parts.append(f"本基金的長線串接歷史裡偵測到 {'、'.join(bits)}，都已整步排除，不計入指數。")
    else:
        parts.append("本基金的長線串接歷史裡目前沒有偵測到財年輪替或資料異常事件。")

    fx_chain_tickers = {tk: ccy for tk, ccy in (long_eps.get("currency_by_ticker") or {}).items() if ccy != "USD"}
    if fx_chain_tickers:
        chain_list = "、".join(f"{tk}（{ccy}）" for tk, ccy in sorted(fx_chain_tickers.items()))
        parts.append(
            f"非美元報表股票（{chain_list}）在串接每一步時都用當天匯率換算，避免匯率波動被算成 "
            "EPS 修正，做法與上一段相同，重用 scripts/eps_fx_normalize.py，沒有另外寫一套。"
        )
    parts.append(
        "舊版兩條 EPS 線（bootstrap／history，用 yfinance 資料）保留在 "
        "chart.eps_index_bootstrap／eps_index_history 供查核，但不畫進 "
        "Exhibit 2——同一張圖擺兩條定義不同的 EPS 線只會讓人看不懂哪條才是"
        "真的。"
    )
    return "".join(parts)


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------


def convert_to_basis_currency(value_local: float | None, local_ccy: str | None, basis_ccy: str,
                               date_str: str, fx_cache: dict) -> tuple[float | None, bool]:
    """把 value_local（幣別 local_ccy）換算成該基金算本益比用的基準幣別
    basis_ccy（見 FUND_REGISTRY cfg["pe_basis_currency"]，多數基金是 USD，
    2026-09-24 加的 TAIEX／0050 是 TWD）。local_ccy==basis_ccy 是最常見的
    no-op（USD 基金的美股成分股、TWD 基金的台股成分股都是這條路徑，不查
    匯率），這樣才不會把 TWD 數字當成 USD 用（過去在別的頁面出現過的那種
    bug）。跨幣別的兩段都借道 get_fx_rate()（USD 為軸心），不必為 TWD 基金
    另外寫一套匯率抓取。回傳 (converted_value, ok)——ok=False 時
    converted_value 一定是 None（其中一段匯率查不到）。"""
    if value_local is None:
        return None, True
    local_ccy = (local_ccy or "USD").upper()
    basis_ccy = (basis_ccy or "USD").upper()
    if local_ccy == basis_ccy:
        return value_local, True
    if basis_ccy == "USD":
        rate = get_fx_rate(local_ccy, date_str, fx_cache)  # local_ccy units per 1 USD
        return (value_local / rate, True) if rate else (None, False)
    if local_ccy == "USD":
        rate = get_fx_rate(basis_ccy, date_str, fx_cache)  # basis_ccy units per 1 USD
        return (value_local * rate, True) if rate else (None, False)
    rate_local = get_fx_rate(local_ccy, date_str, fx_cache)
    rate_basis = get_fx_rate(basis_ccy, date_str, fx_cache)
    if not rate_local or not rate_basis:
        return None, False
    return value_local / rate_local * rate_basis, True


# 2026-09-25 加 TOPIX：dd-screener 母體目前幾乎全是美股（近期才加台股大型
# 股），日股在裡面的覆蓋率天生就很低——長線 EPS 指數（Exhibit 2）如果覆蓋率
# 太低，畫出來的線其實是少數幾檔的雜訊，不是真正的成分股加權訊號，容易誤讀。
# 覆蓋率（權重）低於此門檻就不畫線，前端改顯示一則說明（見
# build_long_chart_series() 與 docs/etf-dash/index.html::renderChart()）——
# 這個門檻對所有基金一體適用，不是只有 TOPIX 特殊處理，只是目前只有 TOPIX 會
# 踩到。
LONG_EPS_LINE_MIN_COVERAGE_PCT = 30.0


def build_long_chart_series(long_eps: dict, price_series: list[dict]) -> tuple[list[dict], str | None]:
    """把 long_eps["series"]（純 EPS 指數點）配上同一天的 ETF 股價指數，回傳
    (chart_series, suppressed_note)。覆蓋率（權重）低於 LONG_EPS_LINE_MIN_COVERAGE_PCT
    時不畫線：回傳空列表＋一則可讀的說明字串，讓呼叫端放進 JSON／前端顯示，
    跟「完全沒有資料」（chart_series 空、suppressed_note 也是 None）區分開——
    後者前端維持既有的「無長線 EPS 指數資料」文字。"""
    if not long_eps["series"]:
        return [], None
    coverage = long_eps.get("coverage_weight_pct") or 0.0
    if coverage < LONG_EPS_LINE_MIN_COVERAGE_PCT:
        return [], (f"dd-screener 名單內符合本基金的成分股覆蓋率（權重）僅 {coverage:.1f}%，"
                     f"低於 {LONG_EPS_LINE_MIN_COVERAGE_PCT:.0f}% 門檻，不畫長線——覆蓋率太低時"
                     "這條線其實是少數幾檔的雜訊，不是真正的成分股加權訊號。")
    start_pt = _closest_close_on_or_before(price_series, long_eps["start_date"])
    start_price = start_pt["close"] if start_pt else None
    out = []
    for pt in long_eps["series"]:
        price_pt = _closest_close_on_or_before(price_series, pt["date"])
        price_index = (round(price_pt["close"] / start_price * 100, 4)
                        if (price_pt and start_price) else None)
        out.append({"date": pt["date"], "eps_index": pt["eps_index"],
                    "price_index": price_index, "coverage_pct": pt["coverage_pct"]})
    return out, None


# ---------------------------------------------------------------------------
# Anchor line — fallback long-EPS-line for funds whose dd-screener coverage
# is below LONG_EPS_LINE_MIN_COVERAGE_PCT (today: TOPIX). See
# scripts/etf_dash/anchor_history.py module docstring for the full design;
# the two functions below are build_etf_dash.py's half of it: computing one
# FULL run's 5-point snapshot (build_anchor_line_point(), uses data already
# fetched for Exhibit 1 — no extra API calls) and turning the spliced,
# multi-run history into a chart series paired with ETF price
# (build_anchor_chart_series(), called from both FULL and PRICE mode so the
# price side stays current daily even though the EPS side only grows on
# FULL runs).
# ---------------------------------------------------------------------------


def build_anchor_line_point(anchors_for_line: dict, total_weight: float, today: datetime) -> dict:
    """單次 FULL run 算出的 ETF 級 EPS 相對水準快照——5 個錨點（eps_as_of 本身
    ＋7／30／60／90 天前），以 eps_as_of＝100 為準。

    anchors_for_line：{ticker: {"current": eps_fy_next_local, "anchors":
    {"7d"/"30d"/"60d"/"90d": eps_N天前_local 或 None}, "weight_pct": ...}}
    ——只放這次 run 裡 EPS 狀態＝ok 的成分股（呼叫端在 build_fund_full() 的
    constituents 迴圈裡建，只用當地幣別：同一檔股票、同一個時間點比較用同一
    幣別，不需要 FX 轉換——跟 revisions_pct 的既有作法一致，見模組開頭
    docstring「EPS 修正 % 本身是同幣別比較，不需要」那段）。

    每個錨點：各成分股的 base/current 比值（= 1/(1+修正%/100)，修正% 套用跟
    Exhibit 1 完全一樣的 classify_revision() 離群值排除／封頂規則——基期 ≤0
    或相對現值過小整筆排除，封頂 ±REVISION_CAP_PCT%）先算出來，再用「這次
    run 的持股權重」加權平均，只在有效成分股集合內重新正規化（renormalize，
    跟 build_fund_full() 的 periods 計算同一個做法）。今天（0 天前）定義上是
    100，覆蓋率＝有算出 current 的成分股權重佔全部持股權重的比例。

    回傳 {"eps_as_of": "YYYY-MM-DD", "points": [{"date","level","coverage_pct"},
    ...]}（5 個點，依日期由舊到新）——直接餵給 anchor_history.append_run()。"""
    today_str = today.strftime("%Y-%m-%d")
    total_weight = total_weight or 1.0
    points = []
    for key, _col, days in ANCHOR_LINE_DEFS:
        acc = 0.0
        covered_w = 0.0
        for info in anchors_for_line.values():
            base = (info.get("anchors") or {}).get(key)
            current = info.get("current")
            status, _reason, _raw_pct, capped_pct = classify_revision(base, current)
            if status not in ("ok", "capped"):
                continue
            ratio = 1.0 / (1 + capped_pct / 100)  # base/current，同幣別故不需 FX
            w = info.get("weight_pct") or 0
            acc += w * ratio
            covered_w += w
        date_label = (today - timedelta(days=days)).strftime("%Y-%m-%d")
        level = round(acc / covered_w * 100, 4) if covered_w > 0 else None
        coverage_pct = round(covered_w / total_weight * 100, 2)
        points.append({"date": date_label, "level": level, "coverage_pct": coverage_pct})

    today_w = sum(info.get("weight_pct") or 0 for info in anchors_for_line.values()
                  if info.get("current") is not None)
    points.append({"date": today_str, "level": 100.0, "coverage_pct": round(today_w / total_weight * 100, 2)})
    points.sort(key=lambda p: p["date"])
    return {"eps_as_of": today_str, "points": points}


def build_anchor_chart_series(etf_key: str, price_series: list[dict]) -> tuple[list[dict], str | None]:
    """讀 data/etf_dash/anchor_history/{ETF}.jsonl（見 anchor_history.py），把
    所有已存的 FULL run 快照串接（anchor_history.splice_runs()）成一條連續的
    EPS 相對水準序列，只取最新一段（anchor_history.build_display_points()）
    配上同一天的 ETF 股價——兩者都在序列第一個點 rebase 成 100，跟
    build_long_chart_series() 的既有設計（EPS 線與股價線同一起點＝100）一致，
    畫在同一張圖上才能直接比較。

    只有 dd-screener 長線覆蓋率不足（呼叫端在 build_long_chart_series() 判定
    suppressed）時才會被呼叫並顯示——見 build_fund_full()／build_fund_price()
    尾端「anchor line fallback」段落。回傳 (chart_series, label_zh)：目前這檔
    基金還沒有任何 anchor_history 資料（例如還沒跑過一次 FULL）時回傳
    ([], None)，呼叫端維持既有的「不畫長線」訊息，不是靜默顯示空圖。"""
    runs = anchor_history.load_runs(etf_key)
    spliced, segment_notes = anchor_history.splice_runs(runs)
    display_points = anchor_history.build_display_points(spliced)
    if not display_points:
        return [], None
    start_date = display_points[0]["date"]
    start_pt = _closest_close_on_or_before(price_series, start_date)
    start_price = start_pt["close"] if start_pt else None
    out = []
    for pt in display_points:
        price_pt = _closest_close_on_or_before(price_series, pt["date"])
        price_index = (round(price_pt["close"] / start_price * 100, 4)
                        if (price_pt and start_price) else None)
        out.append({"date": pt["date"], "eps_index": pt["level"],
                    "price_index": price_index, "coverage_pct": pt["coverage_pct"]})
    label_zh = ("EPS 線來源：Yahoo 分析師預估的 90／60／30／7 天前紀錄（每次全面更新補一段；"
                "過去點位用當次權重）——dd-screener 名單內符合本基金的成分股覆蓋率太低，改用這條線。")
    if segment_notes:
        latest_note = segment_notes[-1]
        label_zh += (f"這條線在 {latest_note['prev_date']} 之前有一段斷點未接續（相距 "
                     f"{latest_note['gap_days']} 天，超過 {anchor_history.GAP_SEGMENT_THRESHOLD_DAYS} 天門檻），"
                     "只顯示斷點之後最新一段。")
    return out, label_zh


def apply_anchor_fallback(long_eps_suppressed_note: str | None, etf_key: str,
                           price_series: list[dict]) -> tuple[str | None, list[dict], str | None]:
    """Threshold switch，FULL／PRICE 兩個模式共用（見 build_fund_full()／
    build_fund_price() 呼叫處）：只有 dd-screener 長線被 build_long_chart_series()
    抑制（long_eps_suppressed_note 不是 None，也就是覆蓋率低於
    LONG_EPS_LINE_MIN_COVERAGE_PCT）才嘗試 anchor line fallback；找到資料就把
    suppressed_note 清成 None（改顯示 anchor line，不是兩則訊息一起顯示——見
    Exhibit 2「移除『不畫長線』說明」的既有要求），這檔基金還沒有任何
    anchor_history（例如還沒跑過一次 FULL）就維持原本的抑制說明，不是靜默
    顯示空圖。回傳 (更新後的 suppressed_note, anchor_chart_series, anchor_label_zh)。"""
    if long_eps_suppressed_note is None:
        return None, [], None
    anchor_chart_series, anchor_label_zh = build_anchor_chart_series(etf_key, price_series)
    if anchor_chart_series:
        return None, anchor_chart_series, anchor_label_zh
    return long_eps_suppressed_note, [], None


# 2026-09-25 持有人擋下上線：XLF 加權遠期本益比 6.82x 是 PGR 一檔拖出來的——
# PGR 的 yfinance eps_fy_next=1012.0、price=202.17，個股本益比 0.1998x，是
# Yahoo 資料異常（Progressive 實際 FY EPS 量級應在 $15-20），不是真的估值。
# 這條腿（加權遠期本益比）獨立做一層「個股本益比合理區間」檢查——跟 EPS
# 修正% 那條腿的 classify_revision() 完全分開（後者管「這次比上次」的比值，
# 這裡管「當下這個估值本身」站不站得住），任何一檔個股本益比 <PE_EXCLUDE_MIN_X
# 或 >PE_EXCLUDE_MAX_X 整筆排除、權重重新正規化，明細記進 pe_excluded 供稽核
# （不悄悄改數字）。FULL／PRICE 兩個模式共用同一個函式，避免兩處各寫一次
# 分岔（過去兩處各自 inline 算過一次，這次順手收斂）。
PE_EXCLUDE_MIN_X = 3.0     # 個股遠期本益比 < 此值 → 疑似資料異常，排除出加權遠期本益比分子分母
PE_EXCLUDE_MAX_X = 300.0   # 個股遠期本益比 > 此值 → 同上（多半是 EPS 趨近 0 造成的雜訊，不是真實估值）


def compute_weighted_forward_pe(constituents: list[dict], total_weight: float,
                                 pe_min: float = PE_EXCLUDE_MIN_X,
                                 pe_max: float = PE_EXCLUDE_MAX_X) -> tuple[float | None, float | None, list[dict]]:
    """純函式：harmonic-mean 加權遠期本益比 = 1 / Σ w_i·(EPS_i/price_i)，先過濾
    個股本益比不在 [pe_min, pe_max] 區間的成分股（見上方模組註解的 PGR 案例）。
    回傳 (weighted_fwd_pe, coverage_pct, pe_excluded)：coverage_pct 是「排除
    本益比異常值後」實際用進分子分母的權重佔 total_weight 的比例；pe_excluded
    依權重降冪排序，每筆含 ticker/name/weight_pct/eps_fy_next_usd/price_usd/
    pe/reason，供 JSON／頁面查核用（不是悄悄丟棄）。"""
    candidates = [c for c in constituents if c.get("eps_fy_next_usd") and c.get("price_usd")]
    pe_covered, pe_excluded = [], []
    for c in candidates:
        pe = c["price_usd"] / c["eps_fy_next_usd"]
        if pe < pe_min or pe > pe_max:
            pe_excluded.append({
                "ticker": c["ticker"], "name": c.get("name"), "weight_pct": c.get("weight_pct"),
                "eps_fy_next_usd": c["eps_fy_next_usd"], "price_usd": c["price_usd"],
                "pe": round(pe, 4),
                "reason": f"個股遠期本益比 {pe:.2f}x 超出合理區間 [{pe_min:g}x, {pe_max:g}x]"
                          "（EPS 或股價疑似資料異常，非真實估值）",
            })
            continue
        pe_covered.append(c)
    pe_covered_weight = sum(c["weight_pct"] or 0 for c in pe_covered)
    weighted_fwd_pe = None
    if pe_covered_weight > 0:
        yield_sum = sum((c["weight_pct"] / pe_covered_weight) * (c["eps_fy_next_usd"] / c["price_usd"])
                         for c in pe_covered)
        weighted_fwd_pe = round(1 / yield_sum, 2) if yield_sum > 0 else None
    coverage_pct = round(pe_covered_weight / total_weight * 100, 2) if total_weight else None
    pe_excluded.sort(key=lambda e: abs(e["weight_pct"] or 0), reverse=True)
    return weighted_fwd_pe, coverage_pct, pe_excluded


# ---------------------------------------------------------------------------
# 報酬貢獻 (price-return contribution) — 2026-09-26 加。contribution_pct =
# 目前權重 × 個股報酬%（見模組層 CONTRIB_PERIOD_DEFS）——用「目前權重」不是
# 期間起點的權重（那份資料我們沒有，見 price_history.py／本任務指示的
# 「use current weights, say so」），跨期間比較時要留意這點，methods_note_zh
# 會交代。個股報酬用同一個 ticker 自己的計價幣別前後比（不做 FX 轉換），
# 這樣才不會把「匯率變動」跟「股價變動」混在一起算成報酬（FX 對這個指標本來
# 就不是重點，是本任務容許的簡化）。
# ---------------------------------------------------------------------------

CONTRIB_PERIOD_DEFS = [("1M", 30, "近一個月"), ("3M", 90, "近三個月")]

# 有現貨產業分解資料的基金（見 resolve_sector()／build_us_sector_lookup()／
# get_tw_industry_map()）——task 指定的六檔：SPY／RSP／QQQ 靠 9 檔 SPDR
# 產業 ETF 持股反查，TAIEX／0050 靠 TWSE 產業別代碼，TOPIX 靠 iShares JP CSV
# 自帶的 Sector 欄。
SECTOR_CONTRIB_ETF_KEYS = {"SPY", "RSP", "QQQ", "TAIEX", "0050", "TOPIX"}


def compute_price_contribution(etf_key: str, constituents: list[dict], total_weight: float,
                                price_days: dict[str, dict[str, float]], today_date_str: str,
                                us_sector_lookup: dict[str, str], tw_industry_map: dict[str, str]) -> dict:
    """回傳 {period_key: {...}}——見模組上方註解。缺乏 30／90 天前收盤價的
    成分股（price_history.jsonl 累積不足，或該檔股票當時不在追蹤名單裡）
    直接跳過（不計入 n_covered／coverage），隨著 prices.jsonl 每天累積，
    覆蓋率會自然上升——上線第一週覆蓋率可能是 0（見 price_history.py 模組
    docstring 的 no-backfill 說明），這是設計上允許的，methods_note_zh 會
    交代。"""
    has_sector = etf_key in SECTOR_CONTRIB_ETF_KEYS
    out = {}
    for key, days, label in CONTRIB_PERIOD_DEFS:
        target_date = (datetime.strptime(today_date_str, "%Y-%m-%d") - timedelta(days=days)).strftime("%Y-%m-%d")
        rows = []
        for c in constituents:
            today_close = c.get("price_local")
            ticker = c.get("ticker")
            if today_close is None or not ticker:
                continue
            found = price_history.closest_close_on_or_before(price_days, ticker, target_date)
            if not found or not found[1]:
                continue
            base_date, base_close = found
            if base_close <= 0:
                continue
            return_pct = (today_close / base_close - 1) * 100
            w = c.get("weight_pct") or 0
            contribution_pct = w / 100 * return_pct
            rows.append({
                "ticker": ticker, "name": c.get("name"), "weight_pct": w,
                "return_pct": round(return_pct, 4), "contribution_pct": round(contribution_pct, 4),
                "base_date": base_date,
                "sector": resolve_sector(ticker, c.get("sector"), us_sector_lookup, tw_industry_map),
            })
        covered_weight = sum(r["weight_pct"] for r in rows)
        rows_sorted = sorted(rows, key=lambda r: r["contribution_pct"], reverse=True)

        sector_rows = None
        if has_sector:
            by_sector: dict[str, float] = {}
            sector_weight: dict[str, float] = {}
            for r in rows:
                s = r["sector"] or "未分類"
                by_sector[s] = by_sector.get(s, 0.0) + r["contribution_pct"]
                sector_weight[s] = sector_weight.get(s, 0.0) + r["weight_pct"]
            sector_rows = sorted(
                [{"sector": s, "contribution_pct": round(v, 4), "weight_pct": round(sector_weight[s], 4)}
                 for s, v in by_sector.items()],
                key=lambda r: r["contribution_pct"], reverse=True,
            )

        out[key] = {
            "key": key, "label": label, "target_date": target_date,
            "n_covered": len(rows), "n_total": len(constituents),
            "coverage_pct": round(covered_weight / total_weight * 100, 2) if total_weight else None,
            "top10": rows_sorted[:10],
            "bottom10": list(reversed(rows_sorted[-10:])) if rows_sorted else [],
            "sector_contribution": sector_rows,
        }
    return out


# ---------------------------------------------------------------------------
# 風格快照 (style snapshot) — 2026-09-26 加。Snapshot only（不補歷史，見任務
# 指示）——只在 FULL 模式算一次（見 build_fund_full() 呼叫處），PRICE 模式
# 沿用 eps_cache 裡存的上一份（跟 periods／contributions 同一個「凍結到下次
# FULL」慣例），不是每天重算（市值分位數／本益比四分位這類統計本來就不需要
# 每天更新，且市值分位數需要的 market_cap_local 只有 FULL 模式的
# fetch_ticker_eps_and_price() 才會抓，見該函式 2026-09-26 新增的欄位）。
# ---------------------------------------------------------------------------


def _weighted_quantile(pairs: list[tuple[float, float]], q: float) -> float | None:
    """加權分位數（linear interpolation between weighted-CDF steps）。
    pairs = [(value, weight), ...]，q in [0,1]。"""
    items = [(v, w) for v, w in pairs if w and w > 0 and v is not None]
    if not items:
        return None
    items.sort(key=lambda x: x[0])
    total = sum(w for _, w in items)
    if total <= 0:
        return None
    cum = 0.0
    target = q * total
    prev_v, prev_cum = items[0][0], 0.0
    for v, w in items:
        cum += w
        if cum >= target:
            if cum == prev_cum:
                return v
            # 線性內插：在這一步跨過 target 的地方，按累積權重比例內插數值。
            frac = (target - prev_cum) / (cum - prev_cum) if cum > prev_cum else 0.0
            return prev_v + frac * (v - prev_v)
        prev_v, prev_cum = v, cum
    return items[-1][0]


def compute_style_snapshot(etf_key: str, constituents: list[dict], total_weight: float,
                            us_sector_lookup: dict[str, str], tw_industry_map: dict[str, str]) -> dict:
    """回傳 {sector_weights, size, pe_dispersion}——見模組上方註解與各欄位。"""
    has_sector = etf_key in SECTOR_CONTRIB_ETF_KEYS
    sector_weights = None
    if has_sector:
        by_sector: dict[str, float] = {}
        for c in constituents:
            s = resolve_sector(c.get("ticker"), c.get("sector"), us_sector_lookup, tw_industry_map) or "未分類"
            by_sector[s] = by_sector.get(s, 0.0) + (c.get("weight_pct") or 0)
        sector_weights = sorted(
            [{"sector": s, "weight_pct": round(w, 4)} for s, w in by_sector.items()],
            key=lambda r: r["weight_pct"], reverse=True,
        )

    mc_pairs = [(c.get("market_cap_local"), c.get("weight_pct") or 0) for c in constituents
                if c.get("market_cap_local")]
    size = {
        "weighted_median_market_cap": _weighted_quantile(mc_pairs, 0.5),
        "weighted_p25_market_cap": _weighted_quantile(mc_pairs, 0.25),
        "weighted_p75_market_cap": _weighted_quantile(mc_pairs, 0.75),
        "n_covered": len(mc_pairs), "n_total": len(constituents),
        "note_zh": "市值為個股自身掛牌幣別（多數為 USD；未做 FX 統一換算——分位數本身是"
                    "「相對哪個量級」的排序統計，不是加總金額，混幣別對排序位置影響有限，"
                    "但跨基準幣別基金（如台股／日股基金）不宜直接跟美股基金的數字並列比較）。",
    }

    pe_pairs = [(c["price_usd"] / c["eps_fy_next_usd"], c.get("weight_pct") or 0) for c in constituents
                if c.get("eps_fy_next_usd") and c.get("price_usd")
                and PE_EXCLUDE_MIN_X <= c["price_usd"] / c["eps_fy_next_usd"] <= PE_EXCLUDE_MAX_X]
    pe_dispersion = {
        "weighted_p25": round(_weighted_quantile(pe_pairs, 0.25), 2) if pe_pairs else None,
        "weighted_median": round(_weighted_quantile(pe_pairs, 0.5), 2) if pe_pairs else None,
        "weighted_p75": round(_weighted_quantile(pe_pairs, 0.75), 2) if pe_pairs else None,
        "n_covered": len(pe_pairs), "n_total": len(constituents),
        "note_zh": f"個股遠期本益比先套用跟加權遠期本益比同一道 [{PE_EXCLUDE_MIN_X:g}x, "
                    f"{PE_EXCLUDE_MAX_X:g}x] 合理區間篩選（見 compute_weighted_forward_pe()），"
                    "四分位數以權重加權（大權重個股對分位數的影響大於小權重個股）。",
    }
    return {"sector_weights": sector_weights, "size": size, "pe_dispersion": pe_dispersion}


def build_fund_full(etf_key: str, cfg: dict, ticker_cache: dict, fx_cache: dict, rc_cache: dict,
                     dd_days: dict, today: datetime, stock_dash_universe: set[str],
                     mode_reason: str, price_days: dict | None = None, us_sector_lookup: dict | None = None,
                     tw_industry_map: dict | None = None, price_today_closes: dict | None = None) -> dict:
    """FULL 模式：持股下載＋每檔 eps_trend，這是 tiered update 之前唯一的路徑
    （見模組開頭「Tiered update」段落）。跑完會把這次算出來的東西存進
    data/etf_dash/eps_cache/{ETF}.json（見 save_eps_cache()），PRICE 模式
    （build_fund_price()）整週沿用，不重抓。

    2026-09-26 加的四個可選參數（皆有預設值，供既有呼叫端／測試不受影響）：
    price_days／us_sector_lookup／tw_industry_map 是報酬貢獻與風格快照要用
    的唯讀查找表（見 compute_price_contribution()／compute_style_snapshot()／
    resolve_sector()，main() 在跑迴圈前建好一次）；price_today_closes 是
    「這次 run 蒐集到的今日收盤價」累加用的輸出字典（呼叫端傳同一個 dict
    給所有基金，main() 最後統一寫進 price_history.jsonl，見該函式 docstring）
    ——都是 None 也能跑（報酬貢獻／風格快照的產業分解退化成沒有查找表可用）。"""
    today_str = today.strftime("%Y-%m-%d")
    price_days = price_days if price_days is not None else {}
    us_sector_lookup = us_sector_lookup if us_sector_lookup is not None else {}
    tw_industry_map = tw_industry_map if tw_industry_map is not None else {}
    as_of_holdings, holdings, non_equity, source_url, used_stale, holdings_approximation_zh = \
        get_holdings_with_fallback(etf_key, cfg)
    weight_methodology_note_zh = build_weight_methodology_note_zh(cfg, holdings)

    # 2026-09-25 加 TOPIX 的 EPS 涵蓋門檻——見 select_eps_scope_tickers() 與
    # FUND_REGISTRY["TOPIX"]["eps_scope_cutoff_pct"] 上方註解。cfg 沒有這個鍵
    # 的基金 eps_scope_tickers 是 None，下面兩處判斷都維持原行為（抓全部持股）。
    eps_scope_cutoff_pct = cfg.get("eps_scope_cutoff_pct")
    eps_scope_tickers = (select_eps_scope_tickers(holdings, eps_scope_cutoff_pct)
                         if eps_scope_cutoff_pct else None)
    eps_scope_note_zh = build_eps_scope_note_zh(cfg, holdings, eps_scope_tickers)

    unique_tickers = sorted(eps_scope_tickers if eps_scope_tickers is not None
                            else {h["ticker"] for h in holdings})
    n_new_fetches = 0
    for tk in unique_tickers:
        if tk not in ticker_cache:
            # 輕量節流：SPY／QQQ 規模到幾百檔，四檔基金共用同一份 ticker_cache
            # （見 main()），但單一 run 裡第一次遇到某檔還是要各抓一次
            # eps_trend＋fast_info——兩次 yfinance 呼叫之間留一點間隔，降低觸發
            # YFRateLimitError 的機率（GitHub runner 的 IP 已經在小規模的
            # SMH/SMH_UCITS 上撞過一次，見 RATE_LIMIT_BACKOFFS_S 的既有重試）。
            if n_new_fetches:
                time.sleep(TICKER_FETCH_PACING_S)
            n_new_fetches += 1
            yf_tk = TICKER_ALIAS.get(tk, tk)  # 例：SKHYV -> 000660.KS
            info = fetch_ticker_eps_and_price(yf_tk)
            info["yf_ticker_used"] = yf_tk
            ticker_cache[tk] = info

    constituents = []
    excluded = []
    total_weight = sum(h["weight_pct"] or 0 for h in holdings)
    # 2026-09-24 加 TAIEX／0050：本益比／股價換算的基準幣別不再寫死 USD——
    # 多數基金仍是 USD（下面兩段 FX 轉換照舊 no-op），台股基金是 TWD（見
    # FUND_REGISTRY cfg["pe_basis_currency"]），避免把 TWD 數字當美元用。
    pe_basis_ccy = cfg.get("pe_basis_currency", "USD")
    # 見 classify_revision() 上方 2026-09-24 的說明——按期間分開累積，兩份名單
    # 都會整份進 JSON（period_exclusions／period_capped，見 periods.append()
    # 下方），頁面也會顯示。
    period_exclusions = {key: [] for key, *_ in PERIOD_DEFS}
    period_capped = {key: [] for key, *_ in PERIOD_DEFS}
    # anchor line fallback（見 anchor_history.py）用——只存這次 run 的原始
    # anchors_local／current（當地幣別，不需要 FX，見 build_anchor_line_point()
    # docstring），跟 rec／constituents 分開，不進 eps_cache 也不進公開 JSON
    # （既有設計本來就不持久化每檔的 eps_trend anchors，見 build_fund_full()
    # 下方 eps_cache_payload 附近的既有註解——這裡沿用同一個原則，只是多算一份
    # 給 anchor_history 用，用完即丟）。
    anchors_for_line: dict[str, dict] = {}
    for h in holdings:
        rec = {
            "ticker": h["ticker"], "name": h["name"], "weight_pct": h["weight_pct"],
            "has_stock_dash": h["ticker"] in stock_dash_universe,
            "sector": h.get("sector"),  # 目前只有 TOPIX（iShares JP CSV）持股列自帶，見 resolve_sector()
        }
        if eps_scope_tickers is not None and h["ticker"] not in eps_scope_tickers:
            # 權重排在 EPS 涵蓋門檻之外，本來就沒抓（不在 unique_tickers 裡，
            # ticker_cache 沒有這一筆）——跟「抓了但沒資料」的 no_eps_data 分開，
            # 不查 ticker_cache（沒有這個 key）。
            rec["status"] = "out_of_eps_scope"
            rec["reason"] = f"權重排序在 EPS 涵蓋門檻（累計 {eps_scope_cutoff_pct:.0f}%）之外，未抓 EPS"
            excluded.append(rec)
            continue
        info = ticker_cache[h["ticker"]]
        if info["status"] != "ok":
            rec["status"] = info["status"]
            rec["reason"] = info.get("reason")
            excluded.append(rec)
            continue
        currency = info["eps_currency"]
        eps_local = info["eps_fy_next_local"]
        eps_usd, fx_normalized = convert_to_basis_currency(eps_local, currency, pe_basis_ccy, today_str, fx_cache)

        # 股價也要換成基準幣別——不能預設 info["price"] 就是基準幣別：多數
        # 成分股是美股/ADR（fast_info.currency=='USD'，USD 基金 no-op），但走
        # TICKER_ALIAS 查到的名字（目前只有 SK Hynix -> 000660.KS）本身用 KRW
        # 掛牌，台股基金的成分股則是 TWD（同樣是 no-op，因為基準幣別也是
        # TWD）。這裡用同一個 convert_to_basis_currency()／get_fx_rate() 快取
        # 換算，價格與 EPS 都換到同一個基準幣別後再算比率，就不會出現「基準
        # 幣別 EPS 除以另一種幣別股價」這種分子分母不同幣別的錯誤。
        price_local = info.get("price")
        price_currency = (info.get("price_currency") or "USD").upper()
        price_usd, price_fx_normalized = convert_to_basis_currency(
            price_local, price_currency, pe_basis_ccy, today_str, fx_cache)

        anchors_local = info["eps_fy_next_anchors_local"]
        anchors_for_line[h["ticker"]] = {"current": eps_local, "anchors": anchors_local,
                                          "weight_pct": h["weight_pct"]}
        revisions_pct = {}
        for key, _col, _label, _days in PERIOD_DEFS:
            base = anchors_local.get(key)
            status, reason, raw_pct, capped_pct = classify_revision(base, eps_local)
            if status == "no_base":
                revisions_pct[key] = None
            elif status == "invalid_base":
                revisions_pct[key] = None
                period_exclusions[key].append({
                    "ticker": h["ticker"], "name": h["name"], "weight_pct": h["weight_pct"],
                    "base_eps": round(base, 4) if base is not None else None,
                    "current_eps": round(eps_local, 4), "reason": reason,
                })
            else:  # "ok" or "capped"
                revisions_pct[key] = capped_pct
                if status == "capped":
                    period_capped[key].append({
                        "ticker": h["ticker"], "name": h["name"], "weight_pct": h["weight_pct"],
                        "raw_pct": raw_pct, "capped_pct": capped_pct,
                    })

        rec.update({
            "status": "ok",
            "yf_ticker_used": info.get("yf_ticker_used", h["ticker"]),
            "eps_currency": currency,
            "eps_fy_next_local": round(eps_local, 4),
            "eps_fy_next_usd": round(eps_usd, 4) if eps_usd is not None else None,
            "fx_normalized": fx_normalized,
            "revisions_pct": revisions_pct,
            "price_local": round(price_local, 4) if price_local is not None else None,
            "price_currency": price_currency,
            "price_usd": round(price_usd, 4) if price_usd is not None else None,
            "price_fx_normalized": price_fx_normalized,
            "market_cap_local": info.get("market_cap"),  # 風格快照市值分位數用，見 fetch_ticker_eps_and_price()
        })
        constituents.append(rec)

    # anchor line fallback：這次 FULL run 的 5 點快照，fund-agnostic——每檔
    # 基金每次 FULL 都算、都存（見 anchor_history.py 模組開頭 docstring），
    # 用不用得到（是否低於 LONG_EPS_LINE_MIN_COVERAGE_PCT 門檻）在下面拿到
    # long_eps 的覆蓋率之後才判斷，這裡先把資料存起來，不管這次用不用得到。
    anchor_run = build_anchor_line_point(anchors_for_line, total_weight, today)
    anchor_history.append_run(etf_key, anchor_run)

    # ---- periods: weighted EPS revision, ETF price change, implied P/E chg
    price_series = fetch_etf_price_history(cfg["yf_ticker"])
    price_series.sort(key=lambda p: p["date"])
    today_price_pt = price_series[-1]

    periods = []
    contributions_by_period = {}
    for key, _col, label, days in PERIOD_DEFS:
        covered = [c for c in constituents if c["revisions_pct"].get(key) is not None]
        covered_weight = sum(c["weight_pct"] or 0 for c in covered)
        eps_chg_pct = None
        contribs = []
        if covered_weight > 0:
            acc = 0.0
            for c in covered:
                w_renorm = (c["weight_pct"] or 0) / covered_weight
                contrib = w_renorm * c["revisions_pct"][key]
                acc += contrib
                contribs.append({"ticker": c["ticker"], "name": c["name"], "weight_pct": c["weight_pct"],
                                  "revision_pct": c["revisions_pct"][key],
                                  "contribution_pct": round(contrib, 4)})
            eps_chg_pct = round(acc, 4)
        # 2026-09-24 加 QQQ／SPY 之前這裡是「取貢獻度絕對值前 5 名」，適合
        # SMH 這種二十幾檔的組合；SPY 有 500 檔，同樣邏輯常常被單一方向洗版
        # （例如某期間九檔都上修，看不到下修的那一側）。改成分開列「上修貢獻
        # Top 10」與「下修貢獻 Bottom 10」，兩邊都能看到，檔數少的基金（如
        # SMH_UCITS）兩份清單容許重疊，不是 bug。
        contribs_sorted = sorted(contribs, key=lambda x: x["contribution_pct"], reverse=True)
        contributions_by_period[key] = {
            "top": contribs_sorted[:10],
            "bottom": list(reversed(contribs_sorted[-10:])) if contribs_sorted else [],
        }

        anchor_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
        anchor_pt = _closest_close_on_or_before(price_series, anchor_date)
        price_chg_pct = None
        if anchor_pt and anchor_pt["close"]:
            price_chg_pct = round((today_price_pt["close"] / anchor_pt["close"] - 1) * 100, 4)

        implied_pe_chg_pct = None
        if eps_chg_pct is not None and price_chg_pct is not None:
            eps_factor = 1 + eps_chg_pct / 100
            if eps_factor != 0:
                implied_pe_chg_pct = round(((1 + price_chg_pct / 100) / eps_factor - 1) * 100, 4)

        excl_sorted = sorted(period_exclusions[key], key=lambda x: x["weight_pct"] or 0, reverse=True)
        capped_sorted = sorted(period_capped[key], key=lambda x: abs(x["weight_pct"] or 0), reverse=True)
        periods.append({
            "key": key, "label": label, "days": days,
            "base_date": anchor_pt["date"] if anchor_pt else None,
            "eps_chg_pct": eps_chg_pct, "price_chg_pct": price_chg_pct,
            "implied_pe_chg_pct": implied_pe_chg_pct,
            "coverage_pct": round(covered_weight / total_weight * 100, 2) if total_weight else None,
            "n_covered": len(covered), "n_total": len(constituents),
            "period_exclusions": excl_sorted,
            "period_capped": capped_sorted,
        })

    # ---- weighted forward P/E (harmonic mean): 1 / Σ w_i * (EPS_i/price_i)，
    # 個股本益比不在合理區間的先排除（見 compute_weighted_forward_pe() 上方
    # 模組註解的 PGR 案例）。
    weighted_fwd_pe, pe_coverage_pct, pe_excluded = compute_weighted_forward_pe(constituents, total_weight)

    # ---- daily snapshot (idempotent per day)
    snap_dir = SNAP_DIR / etf_key
    snap_dir.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "date": today_str,
        "mode": "full",
        "eps_as_of": today_str,
        "holdings_as_of": as_of_holdings,
        "etf_price_close": today_price_pt["close"],
        "etf_price_date": today_price_pt["date"],
        "constituents": [
            {"ticker": c["ticker"], "weight_pct": c["weight_pct"], "eps_fy_next_local": c["eps_fy_next_local"],
             "eps_currency": c["eps_currency"], "eps_fy_next_usd": c["eps_fy_next_usd"]}
            for c in constituents
        ],
    }
    (snap_dir / f"{today_str}.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    eps_index_history = build_eps_index_series(snap_dir, constituents)
    eps_index_bootstrap = build_eps_index_bootstrap(constituents, today, today_price_pt)

    chart_price_series = price_series[-130:]

    # 長線 EPS 指數（2026-05-19 起，見 dd_eps_history.py／build_long_eps_index()
    # docstring）。用今天的持股權重固定，股價同步 rebase 到同一個起點＝100，
    # 兩條線才能疊在同一個座標軸上直接比「估計漲得比股價快還慢」。
    long_eps = build_long_eps_index(holdings, dd_days, fx_cache, rc_cache)
    long_chart_series, long_eps_suppressed_note = build_long_chart_series(long_eps, price_series)

    # anchor line fallback（見 apply_anchor_fallback()／anchor_history.py）——
    # fund-agnostic：用不用得到只看這次算出來的 suppressed_note 是不是
    # None，跟基金是誰無關（見 build_anchor_line_point() 上方註解）。
    long_eps_suppressed_note, anchor_chart_series, anchor_label_zh = apply_anchor_fallback(
        long_eps_suppressed_note, etf_key, price_series)

    excluded_weight = sum(e["weight_pct"] or 0 for e in excluded)
    non_equity_weight = sum(e["weight_pct"] or 0 for e in non_equity)

    # 對帳：長線指數的近 90 天變動，應該跟 Exhibit 1 用 yfinance 算出來的「近三個月」
    # 落在同一個量級——兩條線資料來源、期間定義都不同（長線是每天 as-of 的
    # dd-screener 快照鏈，Exhibit 1 是 yfinance eps_trend 記得的「90 天前」單點），
    # 對不上不代表錯，但差太多要交代原因（見回傳的 long_eps_index_summary）。
    long_full_period_pct = None
    long_last_90d_pct = None
    if long_chart_series:
        long_full_period_pct = round(long_chart_series[-1]["eps_index"] - 100, 4)
        cutoff_90d = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        base_pt = next((p for p in long_chart_series if p["date"] >= cutoff_90d), long_chart_series[0])
        if base_pt["eps_index"]:
            long_last_90d_pct = round(long_chart_series[-1]["eps_index"] / base_pt["eps_index"] * 100 - 100, 4)
    yfinance_90d_pct = next((p["eps_chg_pct"] for p in periods if p["key"] == "90d"), None)

    # 2026-09-26 加的三項——見各自函式上方模組註解。breadth／price_contribution
    # 每次 build（FULL／PRICE 都一樣）都重算，style_snapshot 只在 FULL 算一次
    # （凍結進 eps_cache，PRICE 模式沿用，見 build_fund_price()）。
    breadth = compute_eps_breadth(constituents)
    if price_today_closes is not None:
        for c in constituents:
            if c.get("price_local") is not None:
                price_today_closes[c["ticker"]] = c["price_local"]
    price_contribution = compute_price_contribution(etf_key, constituents, total_weight, price_days, today_str,
                                                      us_sector_lookup, tw_industry_map)
    style_snapshot = compute_style_snapshot(etf_key, constituents, total_weight, us_sector_lookup, tw_industry_map)

    # 2026-09-24 tiered update：這次算出來的東西存進 EPS 快取，PRICE 模式整週
    # 沿用，不重抓 eps_trend。快取只留「重建這份輸出所需的最小集合」——每檔
    # 的 eps_trend anchors 不用存（已經用掉、算進凍結的 periods/contributions
    # 裡了），存的是 status／幣別／現值 EPS 這些 PRICE 模式當天還要用的欄位。
    # tickers 字典從已經算好的 constituents／excluded 建，不是從 ticker_cache
    # 直接搬——constituents 裡的 rec 才有 revisions_pct（PRICE 模式的持股明細表
    # 要沿用這個，不能整週都空著）。
    cached_tickers = {}
    for c in constituents:
        cached_tickers[c["ticker"]] = {
            "status": "ok", "reason": None, "yf_ticker_used": c["yf_ticker_used"],
            "eps_currency": c["eps_currency"], "eps_fy_next_local": c["eps_fy_next_local"],
            "price_currency": c["price_currency"], "has_stock_dash": c["has_stock_dash"],
            "revisions_pct": c["revisions_pct"],
        }
    for e in excluded:
        cached_tickers[e["ticker"]] = {
            "status": e["status"], "reason": e.get("reason"), "yf_ticker_used": e["ticker"],
            "eps_currency": None, "eps_fy_next_local": None, "price_currency": None,
            "has_stock_dash": e["has_stock_dash"], "revisions_pct": None,
        }
    eps_cache_payload = {
        "eps_as_of": today_str,
        "holdings_as_of": as_of_holdings,
        "holdings_source_url": source_url,
        "holdings_approximation_zh": holdings_approximation_zh,
        "holdings": holdings,
        "non_equity": non_equity,
        "tickers": cached_tickers,
        "periods": periods,
        "contributions": contributions_by_period,
        "style_snapshot": style_snapshot,
    }
    save_eps_cache(etf_key, eps_cache_payload)

    return {
        "schema": "etf-dash-v1",
        "etf_key": etf_key,
        "label_zh": cfg["label_zh"],
        "label_en": cfg["label_en"],
        "yf_ticker": cfg["yf_ticker"],
        "isin": cfg["isin"],
        "other_listings": cfg["other_listings"],
        "as_of": today_str,
        "mode": "full",
        "mode_reason": mode_reason,
        "full_refresh": cfg.get("full_refresh", "weekly"),
        "eps_as_of": today_str,
        "price_since_eps_as_of_pct": 0.0,  # FULL 跑當天，eps_as_of 就是今天，定義上還沒有變動
        "holdings_as_of": as_of_holdings,
        "holdings_source_url": source_url,
        "holdings_issuer_zh": cfg["holdings_issuer_zh"],
        "holdings_stale": used_stale,
        "holdings_approximation_zh": holdings_approximation_zh,
        "n_holdings": len(constituents) + len(excluded),
        "n_holdings_covered": len(constituents),
        "price": {"close": today_price_pt["close"], "date": today_price_pt["date"], "currency": pe_basis_ccy},
        "periods": periods,
        "weighted_forward_pe": {
            "value": weighted_fwd_pe,
            "coverage_pct": pe_coverage_pct,
            "method": f"harmonic mean 1/Σw_i·(EPS_i/price_i)；基準幣別 {pe_basis_ccy}，非{pe_basis_ccy}報表"
                      f"(如 ASML)的成分股先用當日 FX 換算成{pe_basis_ccy}；個股本益比 <"
                      f"{PE_EXCLUDE_MIN_X:g}x 或 >{PE_EXCLUDE_MAX_X:g}x 視為資料異常，排除見 pe_excluded",
            "pe_excluded": pe_excluded,
        },
        "constituents": constituents,
        "excluded": excluded,
        "excluded_weight_pct": round(excluded_weight, 2),
        "non_equity": non_equity,
        "non_equity_weight_pct": round(non_equity_weight, 2),
        "contributions": contributions_by_period,
        "breadth": breadth,
        "price_contribution": price_contribution,
        "style_snapshot": style_snapshot,
        "chart": {
            "price_series": chart_price_series,
            "eps_index_bootstrap": eps_index_bootstrap,
            "eps_index_history": eps_index_history,
            "long_eps_index": {
                "start_date": long_eps["start_date"],
                "series": long_chart_series,
                "coverage_weight_pct": long_eps["coverage_weight_pct"],
                "covered_tickers": long_eps["covered_tickers"],
                "rollover_events": long_eps["rollover_events"],
                "anomaly_events": long_eps["anomaly_events"],
                "weight_basis": long_eps["weight_basis"],
                "suppressed_note": long_eps_suppressed_note,
            },
            "anchor_eps_index": {
                "series": anchor_chart_series,
                "label_zh": anchor_label_zh,
            },
        },
        "long_eps_index_summary": {
            "full_period_pct": long_full_period_pct,
            "last_90d_pct": long_last_90d_pct,
            "yfinance_90d_pct": yfinance_90d_pct,
            "note": "長線（dd-screener 快照鏈）與 yfinance 90 天單點理論上量級相近但不必相等"
                    "——資料源、取樣頻率、fiscal-year 對齊方式都不同。",
        },
        "methods_note_zh": build_methods_note_zh(cfg, constituents, non_equity, long_eps,
                                                  len(stock_dash_universe), periods,
                                                  "full", today_str, mode_reason,
                                                  weight_methodology_note_zh=weight_methodology_note_zh,
                                                  eps_scope_note_zh=eps_scope_note_zh,
                                                  anchor_label_zh=anchor_label_zh,
                                                  holdings_approximation_zh=holdings_approximation_zh,
                                                  pe_excluded=pe_excluded),
    }


def build_fund_price(etf_key: str, cfg: dict, eps_cache: dict, fx_cache: dict, rc_cache: dict,
                      dd_days: dict, today: datetime, mode_reason: str, price_days: dict | None = None,
                      us_sector_lookup: dict | None = None, tw_industry_map: dict | None = None,
                      price_today_closes: dict | None = None) -> dict:
    """PRICE 模式：不下載持股、不呼叫 eps_trend（fetch_prices_batch() 完全是
    另一條路徑，見該函式），只批次抓 ETF 加所有成分股「今天」的收盤價，跟
    eps_cache（上次 FULL 存的，見 build_fund_full()）重新配對算「今日加權
    遠期本益比」與「EPS 預估更新後股價變動了多少」。Exhibit 1 的期間表格
    （periods）／貢獻分解（contributions）整份沿用 eps_cache 裡凍結的版本，
    不重算——這樣「近一個月／近二個月／近三個月」的 EPS 修正％跟股價漲跌才是
    同一個窗口算出來的，不會因為每天都用「今天」當窗口終點而互相對不齊（見
    模組開頭「Tiered update」的說明）。

    2026-09-26 加的四個可選參數：跟 build_fund_full() 同一組（見該函式
    docstring）——breadth／price_contribution 這裡仍每天重算（用今天批次抓
    到的股價），style_snapshot 則直接沿用 eps_cache 裡凍結的那份（不重算，
    見 build_fund_full() 的 style_snapshot 只在 FULL 算一次的說明）。"""
    today_str = today.strftime("%Y-%m-%d")
    price_days = price_days if price_days is not None else {}
    us_sector_lookup = us_sector_lookup if us_sector_lookup is not None else {}
    tw_industry_map = tw_industry_map if tw_industry_map is not None else {}
    eps_as_of = eps_cache["eps_as_of"]
    holdings = eps_cache["holdings"]
    non_equity = eps_cache.get("non_equity", [])
    cached_tickers = eps_cache["tickers"]
    total_weight = sum(h["weight_pct"] or 0 for h in holdings)
    weight_methodology_note_zh = build_weight_methodology_note_zh(cfg, holdings)
    # PRICE 模式不重新選 EPS 涵蓋範圍（FULL 模式已經決定過、cached_tickers 裡
    # out_of_eps_scope 的狀態已經凍結），這裡只是純函式重算同一份門檻集合
    # 給方法論文字用（holdings／cutoff 都沒變，結果必然跟 FULL 那次相同）。
    eps_scope_cutoff_pct = cfg.get("eps_scope_cutoff_pct")
    eps_scope_tickers = (select_eps_scope_tickers(holdings, eps_scope_cutoff_pct)
                         if eps_scope_cutoff_pct else None)
    eps_scope_note_zh = build_eps_scope_note_zh(cfg, holdings, eps_scope_tickers)

    ok_yf_tickers = sorted({info.get("yf_ticker_used", tk) for tk, info in cached_tickers.items()
                             if info.get("status") == "ok"})
    batch = fetch_prices_batch([cfg["yf_ticker"]] + ok_yf_tickers)

    etf_series = batch.get(cfg["yf_ticker"])
    if not etf_series:
        raise RuntimeError(f"{etf_key}: batched price fetch returned no data for ETF ticker "
                            f"{cfg['yf_ticker']!r} (PRICE mode)")
    etf_series = sorted(etf_series, key=lambda p: p["date"])
    today_price_pt = etf_series[-1]
    eps_as_of_price_pt = _closest_close_on_or_before(etf_series, eps_as_of)
    price_since_eps_as_of_pct = None
    if eps_as_of_price_pt and eps_as_of_price_pt["close"]:
        price_since_eps_as_of_pct = round((today_price_pt["close"] / eps_as_of_price_pt["close"] - 1) * 100, 4)

    pe_basis_ccy = cfg.get("pe_basis_currency", "USD")
    constituents = []
    excluded = []
    for h in holdings:
        info = cached_tickers.get(h["ticker"])
        rec = {
            "ticker": h["ticker"], "name": h["name"], "weight_pct": h["weight_pct"],
            "has_stock_dash": bool(info.get("has_stock_dash")) if info else False,
            "sector": h.get("sector"),
        }
        if not info or info.get("status") != "ok":
            rec["status"] = (info or {}).get("status") or "no_eps_data"
            rec["reason"] = (info or {}).get("reason")
            excluded.append(rec)
            continue
        currency = info["eps_currency"]
        eps_local = info["eps_fy_next_local"]
        eps_usd, fx_normalized = convert_to_basis_currency(eps_local, currency, pe_basis_ccy, today_str, fx_cache)

        yf_tk = info.get("yf_ticker_used", h["ticker"])
        price_series_c = batch.get(yf_tk)
        price_local = price_series_c[-1]["close"] if price_series_c else None
        price_currency = (info.get("price_currency") or "USD").upper()
        price_usd, price_fx_normalized = convert_to_basis_currency(
            price_local, price_currency, pe_basis_ccy, today_str, fx_cache)

        rec.update({
            "status": "ok",
            "yf_ticker_used": yf_tk,
            "eps_currency": currency,
            "eps_fy_next_local": round(eps_local, 4) if eps_local is not None else None,
            "eps_fy_next_usd": round(eps_usd, 4) if eps_usd is not None else None,
            "fx_normalized": fx_normalized,
            "revisions_pct": info.get("revisions_pct"),  # 凍結（來自上次 FULL），PRICE 模式不重算
            "price_local": round(price_local, 4) if price_local is not None else None,
            "price_currency": price_currency,
            "price_usd": round(price_usd, 4) if price_usd is not None else None,
            "price_fx_normalized": price_fx_normalized,
        })
        constituents.append(rec)

    # ---- 今日加權遠期本益比：今天的價格 × 快取的 EPS（跟 FULL 模式同一個
    # compute_weighted_forward_pe()，含個股本益比合理區間過濾）
    weighted_fwd_pe, pe_coverage_pct, pe_excluded = compute_weighted_forward_pe(constituents, total_weight)

    # ---- daily snapshot（跟 FULL 模式同一個檔案序列，長線 EPS 指數的稽核／
    # legacy chart 都靠這個累積歷史——PRICE 模式的 constituents 裡的
    # eps_fy_next_usd 是「凍結的 EPS × 今天的 FX」，不是「凍結的 EPS × eps_as_of
    # 那天的 FX」，這樣才能跟同一天的 price_usd 用同一組匯率，避免分子分母
    # 匯率基準不一致）。
    snap_dir = SNAP_DIR / etf_key
    snap_dir.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "date": today_str,
        "mode": "price",
        "eps_as_of": eps_as_of,
        "holdings_as_of": eps_cache.get("holdings_as_of"),
        "etf_price_close": today_price_pt["close"],
        "etf_price_date": today_price_pt["date"],
        "constituents": [
            {"ticker": c["ticker"], "weight_pct": c["weight_pct"], "eps_fy_next_local": c["eps_fy_next_local"],
             "eps_currency": c["eps_currency"], "eps_fy_next_usd": c["eps_fy_next_usd"]}
            for c in constituents
        ],
    }
    (snap_dir / f"{today_str}.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    eps_index_history = build_eps_index_series(snap_dir, constituents)
    eps_index_bootstrap = build_eps_index_bootstrap(constituents, today, today_price_pt)
    chart_price_series = etf_series[-130:]

    long_eps = build_long_eps_index(holdings, dd_days, fx_cache, rc_cache)
    long_chart_series, long_eps_suppressed_note = build_long_chart_series(long_eps, etf_series)

    # anchor line fallback（見 apply_anchor_fallback()／build_fund_full() 同一
    # 段註解）——PRICE 模式不會有新的 FULL run 快照可存，只是把上次 FULL 存下來
    # 的 anchor_history 讀出來，配上今天批次抓到的最新股價，讓股價那一側每天
    # 都跟著更新（跟 long_eps_index 現有行為一致）。
    long_eps_suppressed_note, anchor_chart_series, anchor_label_zh = apply_anchor_fallback(
        long_eps_suppressed_note, etf_key, etf_series)

    excluded_weight = sum(e["weight_pct"] or 0 for e in excluded)
    non_equity_weight = sum(e["weight_pct"] or 0 for e in non_equity)

    long_full_period_pct = None
    long_last_90d_pct = None
    if long_chart_series:
        long_full_period_pct = round(long_chart_series[-1]["eps_index"] - 100, 4)
        cutoff_90d = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        base_pt = next((p for p in long_chart_series if p["date"] >= cutoff_90d), long_chart_series[0])
        if base_pt["eps_index"]:
            long_last_90d_pct = round(long_chart_series[-1]["eps_index"] / base_pt["eps_index"] * 100 - 100, 4)
    periods = eps_cache["periods"]  # 凍結，整週不變——見本函式 docstring
    yfinance_90d_pct = next((p["eps_chg_pct"] for p in periods if p["key"] == "90d"), None)

    breadth = compute_eps_breadth(constituents)
    if price_today_closes is not None:
        for c in constituents:
            if c.get("price_local") is not None:
                price_today_closes[c["ticker"]] = c["price_local"]
    price_contribution = compute_price_contribution(etf_key, constituents, total_weight, price_days, today_str,
                                                      us_sector_lookup, tw_industry_map)
    style_snapshot = eps_cache.get("style_snapshot")  # 凍結，沿用上次 FULL 算的——見本函式 docstring

    return {
        "schema": "etf-dash-v1",
        "etf_key": etf_key,
        "label_zh": cfg["label_zh"],
        "label_en": cfg["label_en"],
        "yf_ticker": cfg["yf_ticker"],
        "isin": cfg["isin"],
        "other_listings": cfg["other_listings"],
        "as_of": today_str,
        "mode": "price",
        "mode_reason": mode_reason,
        "full_refresh": cfg.get("full_refresh", "weekly"),
        "eps_as_of": eps_as_of,
        "price_since_eps_as_of_pct": price_since_eps_as_of_pct,
        "holdings_as_of": eps_cache.get("holdings_as_of"),
        "holdings_source_url": eps_cache.get("holdings_source_url"),
        "holdings_issuer_zh": cfg["holdings_issuer_zh"],
        "holdings_stale": False,  # 不是抓取失敗，是設計上這週沒重抓——見 mode／methods_note_zh
        "holdings_approximation_zh": eps_cache.get("holdings_approximation_zh"),
        "n_holdings": len(constituents) + len(excluded),
        "n_holdings_covered": len(constituents),
        "price": {"close": today_price_pt["close"], "date": today_price_pt["date"], "currency": pe_basis_ccy},
        "periods": periods,
        "weighted_forward_pe": {
            "value": weighted_fwd_pe,
            "coverage_pct": pe_coverage_pct,
            "method": f"harmonic mean 1/Σw_i·(EPS_i/price_i)；EPS 沿用 eps_as_of 快取，股價是今天批次抓的，"
                      f"兩者都用今天的匯率換算成{pe_basis_ccy}，非{pe_basis_ccy}報表(如 ASML)一樣先換算；"
                      f"個股本益比 <{PE_EXCLUDE_MIN_X:g}x 或 >{PE_EXCLUDE_MAX_X:g}x 視為資料異常，排除見 pe_excluded",
            "pe_excluded": pe_excluded,
        },
        "constituents": constituents,
        "excluded": excluded,
        "excluded_weight_pct": round(excluded_weight, 2),
        "non_equity": non_equity,
        "non_equity_weight_pct": round(non_equity_weight, 2),
        "contributions": eps_cache["contributions"],  # 凍結，整週不變
        "breadth": breadth,
        "price_contribution": price_contribution,
        "style_snapshot": style_snapshot,
        "chart": {
            "price_series": chart_price_series,
            "eps_index_bootstrap": eps_index_bootstrap,
            "eps_index_history": eps_index_history,
            "long_eps_index": {
                "start_date": long_eps["start_date"],
                "series": long_chart_series,
                "coverage_weight_pct": long_eps["coverage_weight_pct"],
                "covered_tickers": long_eps["covered_tickers"],
                "rollover_events": long_eps["rollover_events"],
                "anomaly_events": long_eps["anomaly_events"],
                "weight_basis": long_eps["weight_basis"],
                "suppressed_note": long_eps_suppressed_note,
            },
            "anchor_eps_index": {
                "series": anchor_chart_series,
                "label_zh": anchor_label_zh,
            },
        },
        "long_eps_index_summary": {
            "full_period_pct": long_full_period_pct,
            "last_90d_pct": long_last_90d_pct,
            "yfinance_90d_pct": yfinance_90d_pct,
            "note": "長線（dd-screener 快照鏈）與 yfinance 90 天單點理論上量級相近但不必相等"
                    "——資料源、取樣頻率、fiscal-year 對齊方式都不同。",
        },
        "methods_note_zh": build_methods_note_zh(cfg, constituents, non_equity, long_eps,
                                                  0, periods, "price", eps_as_of, mode_reason,
                                                  weight_methodology_note_zh=weight_methodology_note_zh,
                                                  eps_scope_note_zh=eps_scope_note_zh,
                                                  anchor_label_zh=anchor_label_zh,
                                                  holdings_approximation_zh=eps_cache.get("holdings_approximation_zh"),
                                                  pe_excluded=pe_excluded),
    }


# ---------------------------------------------------------------------------
# 資金流 (flows) — 2026-09-26 加。跟 FULL／PRICE 模式無關（每天都跑，見
# flows.py 模組 docstring），所以放在 build_fund() 這個分派層而不是
# build_fund_full()／build_fund_price() 內部——不管今天是哪種模式，都要記一筆
# 今天的 shares_outstanding／NAV 快照。TAIEX 是指數不是基金，沒有受益權
# 單位數／NAV 概念，整段跳過（不寫入 data/etf_dash/flows/TAIEX.jsonl）。
# ---------------------------------------------------------------------------

TAIEX_NO_FLOWS_NOTE_ZH = "TAIEX 是指數，不是可申購／贖回的基金，沒有受益權單位數或 NAV 概念——指數無資金流，不追蹤。"

# 2026-09-26 資金流來源分級（見 flows.py 模組開頭 docstring 的完整調查記錄）：
#   "ssga_navhist"          — SSGA 官方逐日 NAV／份額歷史（SPY＋9 檔產業 ETF）
#   "vaneck_navhist"        — VanEck 官方逐日 NAV／AUM 歷史，推算份額（僅美國
#                              掛牌 SMH；愛爾蘭 UCITS 版該檔沒有 AUM 欄，見
#                              flows.py 註解，維持 yfinance）
#   "invesco_direct"        — Invesco fundDetails API 單日快照（QQQ／RSP；
#                              RSP 實測不穩定，失敗會落到 yfinance）
#   "yfinance"（預設，未列在此表視同這個）— 其餘（SMH_UCITS／TOPIX／0050），
#                              以及上述來源這次 run 失敗時的 fallback。
FLOWS_SOURCE_TIER = {
    "SPY": "ssga_navhist", "XLK": "ssga_navhist", "XLF": "ssga_navhist", "XLE": "ssga_navhist",
    "XLV": "ssga_navhist", "XLI": "ssga_navhist", "XLY": "ssga_navhist", "XLP": "ssga_navhist",
    "XLC": "ssga_navhist", "XLB": "ssga_navhist",
    "SMH": "vaneck_navhist",
    "QQQ": "invesco_direct", "RSP": "invesco_direct",
}


def _attach_flows_tier1_history(etf_key: str, cfg: dict, tier: str) -> bool:
    """Tier 1（官方逐日歷史檔）——回傳 True 代表這次成功合併了一批歷史進
    data/etf_dash/flows/{ETF}.jsonl（見 flows.merge_history()），呼叫端接著
    照樣讀 flows.load_rows() 算 compute_flow_series()，不需要另外處理。"""
    if tier == "ssga_navhist":
        rows = flows.fetch_ssga_navhist_rows(cfg["yf_ticker"])
    elif tier == "vaneck_navhist":
        history_url = cfg["holdings_url"].replace("/downloads/holdings/", "/downloads/fundhistoprices/")
        rows = flows.fetch_vaneck_navhist_rows(history_url, cfg["holdings_cookies"])
    else:
        raise ValueError(f"unknown tier1 source {tier!r}")
    flows.merge_history(etf_key, rows)
    return True


def attach_flows(etf_key: str, cfg: dict, result: dict, today_str: str) -> None:
    """就地把 "flows" 鍵寫進 result（呼叫端傳進來的、build_fund_full／
    build_fund_price 剛回傳的那個 dict）。失敗不讓整個 build_fund() 失敗——
    資金流缺一天不該讓既有的 EPS／股價功能連坐失敗。依 FLOWS_SOURCE_TIER
    決定這檔基金的主要來源，官方來源這次 run 失敗（或這檔基金沒有官方來源）
    一律 fallback 到 yfinance（見 flows.fetch_shares_snapshot_yfinance()），
    不會因為官方來源失效就整天沒有資金流數字。"""
    if etf_key == "TAIEX":
        result["flows"] = {"skipped": True, "reason_zh": TAIEX_NO_FLOWS_NOTE_ZH}
        return
    tier = FLOWS_SOURCE_TIER.get(etf_key)
    used_tier1 = False
    if tier in ("ssga_navhist", "vaneck_navhist"):
        try:
            used_tier1 = _attach_flows_tier1_history(etf_key, cfg, tier)
        except Exception as e:  # noqa: BLE001
            print(f"[etf_dash] WARNING {etf_key}: flows tier1 ({tier}) fetch failed ({e}), "
                  f"falling back to yfinance for today", file=sys.stderr)
    snap = None
    if not used_tier1:
        if tier == "invesco_direct":
            snap = flows.fetch_shares_snapshot_invesco(cfg["yf_ticker"])
            if not snap.get("source"):
                print(f"[etf_dash] WARNING {etf_key}: Invesco fundDetails unusable today "
                      f"({snap.get('reason')}), falling back to yfinance", file=sys.stderr)
                snap = None
        if snap is None:
            snap = flows.fetch_shares_snapshot_yfinance(yf, cfg["yf_ticker"])
        if snap.get("source"):
            flows.append_today(etf_key, {"date": today_str, **snap})
        else:
            print(f"[etf_dash] WARNING {etf_key}: flows snapshot has no usable source today "
                  f"({snap.get('reason')})", file=sys.stderr)
    try:
        rows = flows.load_rows(etf_key)
        series = flows.compute_flow_series(rows)
        series["skipped"] = False
        series["today_snapshot"] = snap if snap is not None else (rows[-1] if rows and rows[-1].get("date") == today_str else None)
        result["flows"] = series
    except Exception as e:  # noqa: BLE001
        print(f"[etf_dash] WARNING {etf_key}: attach_flows failed ({e})", file=sys.stderr)
        result["flows"] = {"skipped": True, "reason_zh": f"這次 run 資金流快照失敗：{e}"}


def build_fund(etf_key: str, cfg: dict, ticker_cache: dict, fx_cache: dict, rc_cache: dict,
               dd_days: dict, today: datetime, stock_dash_universe: set[str], cli_mode: str,
               price_days: dict | None = None, us_sector_lookup: dict | None = None,
               tw_industry_map: dict | None = None, price_today_closes: dict | None = None) -> dict:
    """FULL／PRICE 分派——見模組開頭「Tiered update」說明。decide_mode() 在這裡
    評估一次（不是在 main() 裡對整個 run 評估一次）：每檔基金各自的 EPS 快取
    新鮮度不同（例如 QQQ／SPY 剛上線那週還沒有快取，即使不是週六也會被判定
    要 FULL——這正是我們要的：第一次跑一定要有真資料才能建立快取），比在
    main() 算一次全域 mode 更貼近實際狀態。"""
    eps_cache = load_eps_cache(etf_key)
    mode, mode_reason = decide_mode(cli_mode, eps_cache, taipei_now(), cfg.get("full_refresh", "weekly"))
    print(f"[etf_dash] {etf_key}: mode={mode} ({mode_reason})", file=sys.stderr)
    if mode == "price":
        try:
            result = build_fund_price(etf_key, cfg, eps_cache, fx_cache, rc_cache, dd_days, today, mode_reason,
                                       price_days, us_sector_lookup, tw_industry_map, price_today_closes)
            attach_flows(etf_key, cfg, result, today.strftime("%Y-%m-%d"))
            return result
        except Exception as e:  # noqa: BLE001
            # PRICE 模式本身失敗（批次下載掛了之類）不代表 FULL 模式也會失敗
            # ——退回 FULL 跑一次，好過整檔直接沒資料（跟 holdings fetch 的
            # cache-fallback 哲學一致：能有資料就不要沒資料）。
            print(f"[etf_dash] WARNING {etf_key}: PRICE mode failed ({e}), falling back to FULL", file=sys.stderr)
            mode_reason = f"PRICE 模式失敗退回 FULL（{e}）"
    result = build_fund_full(etf_key, cfg, ticker_cache, fx_cache, rc_cache, dd_days, today,
                              stock_dash_universe, mode_reason, price_days, us_sector_lookup,
                              tw_industry_map, price_today_closes)
    attach_flows(etf_key, cfg, result, today.strftime("%Y-%m-%d"))
    return result


def build_eps_index_series(snap_dir: Path, today_constituents: list[dict]) -> list[dict]:
    """用「今天的權重」＋「每天快照裡的 EPS」重建加權 EPS 指數時間序列。
    某天快照缺某檔（例如那天 yfinance 抓不到）就用當天有資料的成分股權重
    重新正規化——覆蓋率會隨之在 coverage_pct 欄位裡看得到。"""
    today_weights = {c["ticker"]: c["weight_pct"] for c in today_constituents}
    total_today_weight = sum(today_weights.values()) or 1.0
    series = []
    if not snap_dir.exists():
        return series
    for f in sorted(snap_dir.glob("*.json")):
        try:
            snap = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        acc = 0.0
        covered_w = 0.0
        for c in snap.get("constituents", []):
            tk = c.get("ticker")
            eps_usd = c.get("eps_fy_next_usd")
            if tk not in today_weights or eps_usd is None:
                continue
            w = today_weights[tk]
            acc += w * eps_usd
            covered_w += w
        if covered_w <= 0:
            continue
        # 用當天實際有資料的成分股權重正規化（覆蓋率不足 100% 時的加權平均 EPS，$/share）
        weighted_eps = acc / covered_w
        series.append({
            "date": snap.get("date"),
            "weighted_eps_usd": round(weighted_eps, 4),
            "coverage_pct": round(covered_w / total_today_weight * 100, 2),
            "etf_price_close": snap.get("etf_price_close"),
        })
    return series


def build_eps_index_bootstrap(constituents: list[dict], today: datetime, today_price_pt: dict) -> list[dict]:
    """用 eps_trend 自帶的 4 個歷史錨點（90/60/30/7 天前）＋今天，配「今天的
    權重」重建加權 EPS——只有第一次跑、還沒有每日快照歷史時才需要靠這個，
    之後 build_eps_index_series() 的每日快照序列會愈來愈長，蓋過這裡。"""
    total_weight = sum(c["weight_pct"] or 0 for c in constituents) or 1.0
    points = []
    anchor_specs = [("90d", 90), ("60d", 60), ("30d", 30)]  # 7d 已拿掉，見 PERIOD_DEFS 說明
    for key, days in anchor_specs:
        acc = 0.0
        covered_w = 0.0
        for c in constituents:
            anchors_local = None
            # 重新從 revisions_pct 反推需要原始 anchors；為避免重算 FX，這裡只用
            # 已經在 constituents 內算好的 eps_fy_next_usd 與 revisions_pct 還原：
            # anchor_usd = current_usd / (1 + revision%/100)
            rev = c["revisions_pct"].get(key)
            cur_usd = c.get("eps_fy_next_usd")
            if rev is None or cur_usd is None:
                continue
            anchor_usd = cur_usd / (1 + rev / 100)
            w = c["weight_pct"] or 0
            acc += w * anchor_usd
            covered_w += w
        if covered_w <= 0:
            continue
        date_label = (today - timedelta(days=days)).strftime("%Y-%m-%d")
        points.append({"date": date_label, "label": f"{days} 天前", "weighted_eps_usd": round(acc / covered_w, 4),
                        "coverage_pct": round(covered_w / total_weight * 100, 2)})
    # 今天
    acc = sum((c["weight_pct"] or 0) * c["eps_fy_next_usd"] for c in constituents if c.get("eps_fy_next_usd"))
    covered_w = sum((c["weight_pct"] or 0) for c in constituents if c.get("eps_fy_next_usd"))
    if covered_w > 0:
        points.append({"date": today.strftime("%Y-%m-%d"), "label": "今天",
                        "weighted_eps_usd": round(acc / covered_w, 4),
                        "coverage_pct": round(covered_w / total_weight * 100, 2)})
    return points


# ---------------------------------------------------------------------------
# Long-history EPS index — reconstructed from docs/dd-screener/latest.json's
# git history (2026-05-19 onward, ~105 distinct commit days as of 2026-09-24),
# via dd_eps_history.py's cache. Far longer than yfinance eps_trend's 90-day
# memory, but two things make the raw day-over-day series unsafe to chain
# blindly:
#   (1) fiscal-year rollover — a company's "eps_fy_next" means a different
#       fiscal year once that FY closes, so eps_fy_next can jump structurally
#       without any real analyst revision.
#   (2) upstream data artifacts found while building this (see report to
#       coordinator, 2026-09-24) — TSM's eps_fy_next flips between an
#       ADR-share basis and what looks like a /5 (per-local-share) basis at
#       least twice in this window, and KLAC shows a ~9.7x single-day drop in
#       BOTH eps_fy_next and eps_fy3 together on 2026-07-16 (a scale/rebase
#       artifact, not 25 companies each reporting a stock split that day).
#       eps_display_currency stays "USD" through all of this — it is NOT a
#       currency bug, so eps_fx_normalize alone would not catch it.
# classify_eps_step() below handles both. See its docstring for the exact
# decision rule and thresholds.
# ---------------------------------------------------------------------------

ROLLOVER_FY3_TOL = 0.03            # eps_fy_next(t) vs eps_fy3(t-1) 在 3% 以內 → 財年輪替
SCALE_ANOMALY_RATIO_TOL = 0.05     # eps_fy_next 與 eps_fy3 的單步變動比例要多接近才算「同步縮放」
SCALE_ANOMALY_BAND = (0.7, 1.43)   # 縮放比例落在此區間內視為正常（约±30%），區間外才觸發
UNCONFIRMED_JUMP_THRESHOLD = 0.45  # 沒有 eps_fy3 可佐證時，單步變動超過這個比例就保守排除
STEP_SCRUTINY_THRESHOLD = 0.08     # 單步變動小於這個比例，不值得跑下面的判定，直接當正常修正


def classify_eps_step(p_nxt: float | None, p_fy3: float | None,
                       cur_nxt: float | None, cur_fy3: float | None) -> tuple[str, float | None]:
    """判斷相鄰兩個 dd-screener 快照日之間，一檔股票的 eps_fy_next 這一步該
    怎麼用。純函式（不碰快取／網路），回傳 (step_type, baseline_for_revision)：

      - "normal"：一般分析師修正，用 cur_nxt 對 p_nxt 算修正%。
      - "rollover"：財年輪替——cur_nxt 實際上接的是 p_fy3（去年講的「後年度」
        變成今年的「明年度」），不是 p_nxt 的延續。用 p_fy3 當基準算修正%
        （殘差通常很小，因為判定門檻本身就是 3% 以內）。
      - "scale_anomaly"：eps_fy_next 與 eps_fy3 同一天同步跳了幾乎一樣的倍數
        （像股數基礎或單位換算被誤改，不是真實修正也不是財年輪替——兩個
        欄位不該同步移動一樣的比例）。整步排除，不計入指數也不計入覆蓋率。
      - "unconfirmed_anomaly"：單步變動超過 45%，但不符合上面兩種判定的條件
        （沒有 eps_fy3 可比對，或比對了也不像財年輪替／同步縮放），保守排除。

    2026-09-24 用本組合 105 天實測：命中 0 次 rollover、2 次 scale_anomaly
    （TSM 2026-09-16、KLAC 2026-07-16）、1 次 unconfirmed_anomaly（TSM
    2026-05-20，當時 eps_fy3 欄位還沒上線）。
    """
    if not p_nxt or not cur_nxt or p_nxt <= 0 or cur_nxt <= 0:
        return "normal", p_nxt
    ratio_next = cur_nxt / p_nxt
    if abs(ratio_next - 1) <= STEP_SCRUTINY_THRESHOLD:
        return "normal", p_nxt
    if p_fy3 and p_fy3 > 0 and abs(cur_nxt / p_fy3 - 1) <= ROLLOVER_FY3_TOL:
        return "rollover", p_fy3
    if p_fy3 and p_fy3 > 0 and cur_fy3 and cur_fy3 > 0:
        ratio_fy3 = cur_fy3 / p_fy3
        in_band = SCALE_ANOMALY_BAND[0] <= ratio_next <= SCALE_ANOMALY_BAND[1]
        if abs(ratio_next - ratio_fy3) <= SCALE_ANOMALY_RATIO_TOL and not in_band:
            return "scale_anomaly", None
    # 保底：不管有沒有 fy3，只要單步變動大到不像真實修正，又沒被上面兩種更
    # specific 的判定接住，一律保守排除——不要讓「兩個判定條件都差一點沒踩到」
    # 的邊界案例被默默當成正常修正吃進指數。
    if abs(ratio_next - 1) > UNCONFIRMED_JUMP_THRESHOLD:
        return "unconfirmed_anomaly", None
    return "normal", p_nxt


def build_long_eps_index(holdings: list[dict], dd_days: dict, fx_cache: dict, rc_cache: dict) -> dict:
    """把 dd_eps_history 快取（dd_days = {"date": {"tickers": {...}}}）鏈接成
    一條加權 EPS 指數，index=100 在第一個有資料的日期。權重固定用今天的持股
    權重（disclosed，見回傳的 weight_basis）；某天缺資料的成分股當天不計入
    covered weight、其餘成分股權重重新正規化——見各步驟內的 coverage_pct。"""
    weight_by_ticker = {h["ticker"]: (h["weight_pct"] or 0) for h in holdings}
    tickers = sorted(weight_by_ticker.keys())
    total_weight = sum(weight_by_ticker.values()) or 1.0
    dates = sorted(dd_days.keys())

    # 只有 dd-screener 母體裡的名字才有歷史可用；SKHYV／SNPS／MCHP／ENTG 這類
    # 不在母體的名字，下面 per_ticker_points 會是空列表，自然被排除、拉低
    # coverage_weight_pct，不特別報錯。
    currency_by_ticker: dict[str, str] = {}
    per_ticker_points: dict[str, list[tuple[str, float, float | None]]] = {}
    for tk in tickers:
        pts = []
        for d in dates:
            rec = dd_days[d]["tickers"].get(tk)
            if rec is None:
                continue
            nxt = dd_eps_history.get_usd_value(rec, "eps_fy_next")
            fy3 = dd_eps_history.get_usd_value(rec, "eps_fy3")
            if nxt is None or nxt <= 0:
                continue
            pts.append((d, nxt, fy3))
        if not pts:
            continue
        per_ticker_points[tk] = pts
        yf_tk = TICKER_ALIAS.get(tk, tk)
        ccy = get_reporting_currency(tk, yf_tk, rc_cache)
        currency_by_ticker[tk] = (ccy or "USD").upper()

    covered_tickers = sorted(per_ticker_points.keys())
    coverage_weight_pct = round(sum(weight_by_ticker[tk] for tk in covered_tickers) / total_weight * 100, 2)
    if not covered_tickers:
        return {"start_date": None, "series": [], "rollover_events": [], "anomaly_events": [],
                "covered_tickers": [], "coverage_weight_pct": 0.0, "weight_basis": "today",
                "currency_by_ticker": {}, "uncovered_tickers": sorted(tickers)}

    per_ticker_map = {tk: {d: (n, f) for d, n, f in per_ticker_points[tk]} for tk in covered_tickers}

    start_date = None
    for d in dates:
        if any(d in per_ticker_map[tk] for tk in covered_tickers):
            start_date = d
            break
    grid_dates = [d for d in dates if d >= start_date]

    rollover_events: list[dict] = []
    anomaly_events: list[dict] = []

    prev_vals: dict[str, tuple[str, float, float | None]] = {}
    for tk in covered_tickers:
        v = per_ticker_map[tk].get(start_date)
        if v:
            prev_vals[tk] = (start_date, v[0], v[1])

    cov0_w = sum(weight_by_ticker[tk] for tk in prev_vals)
    index = 100.0
    series = [{"date": start_date, "eps_index": 100.0,
               "coverage_pct": round(cov0_w / total_weight * 100, 2)}]

    for d in grid_dates[1:]:
        step_contribs = []  # (weight, step_pct)
        cov_today_w = 0.0
        for tk in covered_tickers:
            cur = per_ticker_map[tk].get(d)
            if cur is None:
                continue  # 這檔這天沒資料（暫時掉出 dd-screener 母體），跳過，prev_vals 不變
            cov_today_w += weight_by_ticker[tk]
            cur_nxt, cur_fy3 = cur
            if tk not in prev_vals:
                prev_vals[tk] = (d, cur_nxt, cur_fy3)  # 這檔第一次出現，這步不算修正
                continue
            p_date, p_nxt, p_fy3 = prev_vals[tk]
            if p_date == d:
                continue
            step_type, baseline = classify_eps_step(p_nxt, p_fy3, cur_nxt, cur_fy3)
            prev_vals[tk] = (d, cur_nxt, cur_fy3)
            if step_type == "rollover":
                rollover_events.append({"ticker": tk, "date": d, "prev_date": p_date,
                                         "prev_eps_fy3_usd": round(p_fy3, 4), "curr_eps_fy_next_usd": round(cur_nxt, 4)})
            elif step_type in ("scale_anomaly", "unconfirmed_anomaly"):
                anomaly_events.append({"ticker": tk, "date": d, "prev_date": p_date, "type": step_type,
                                        "prev_eps_fy_next_usd": round(p_nxt, 4) if p_nxt else None,
                                        "curr_eps_fy_next_usd": round(cur_nxt, 4),
                                        "explanation": KNOWN_ANOMALY_EXPLANATIONS.get((tk, d))})
                continue  # 不信任這一步：不進 index，也不計入 covered weight
            currency = currency_by_ticker[tk]
            fx_cur = 1.0 if currency == "USD" else get_fx_rate(currency, d, fx_cache)
            fx_base = 1.0 if currency == "USD" else get_fx_rate(currency, p_date, fx_cache)
            step_pct, _fx_ok = compute_fx_normalized_revision(cur_nxt, baseline, currency, fx_cur, fx_base)
            if step_pct is not None:
                step_contribs.append((weight_by_ticker[tk], step_pct))

        step_covered_w = sum(w for w, _ in step_contribs)
        weighted_step = (sum(w * r for w, r in step_contribs) / step_covered_w) if step_covered_w > 0 else 0.0
        index *= (1 + weighted_step / 100)
        series.append({"date": d, "eps_index": round(index, 4),
                        "coverage_pct": round(cov_today_w / total_weight * 100, 2)})

    return {
        "start_date": start_date,
        "series": series,
        "rollover_events": rollover_events,
        "anomaly_events": anomaly_events,
        "covered_tickers": covered_tickers,
        "coverage_weight_pct": coverage_weight_pct,
        "weight_basis": "today",
        "currency_by_ticker": currency_by_ticker,  # 只含非空值的 ticker；build_methods_note_zh() 用來組非美元報表段落
        "uncovered_tickers": sorted(set(tickers) - set(covered_tickers)),  # 有權重但不在 dd-screener 母體裡的名字
    }


# ---------------------------------------------------------------------------
# Preview HTML (self-contained, data inlined)
# ---------------------------------------------------------------------------


def render_preview_html(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    # 版面沿用 docs/etf-dash/index.html 的同一份 JS render()；preview 差別有二：
    # (1) 資料用 inline <script> 塞進去，不用 fetch，方便單檔打開檢視；
    # (2) imq-base.css 用絕對路徑 /assets/imq-base.css——正式站沒問題，但 preview
    #     是丟在 /private/tmp/ 底下單檔打開／或非站根 http server 測試，絕對路徑會
    #     404、整頁沒有 CSS token 變成沒樣式。這裡直接把該檔內容 inline 成
    #     <style>，讓 preview 真正自含（不依賴任何本機/線上路徑）。
    prod_template_path = ROOT / "docs" / "etf-dash" / "index.html"
    template = prod_template_path.read_text(encoding="utf-8")
    base_css_path = ROOT / "docs" / "assets" / "imq-base.css"
    base_css = base_css_path.read_text(encoding="utf-8") if base_css_path.exists() else ""
    template = template.replace(
        '<link rel="stylesheet" href="/assets/imq-base.css">',
        f"<style>{base_css}</style>",
    )
    marker = "/*__ETF_DASH_DATA__*/"
    inline = f"var ETF_DASH_INLINE_DATA = {payload};\n"
    if marker in template:
        template = template.replace(marker, inline)
    else:
        template = template.replace("<script>", f"<script>{inline}", 1)
    return template


# ---------------------------------------------------------------------------
# Overview — 2026-09-25 加 9 檔產業 ETF＋RSP 到 17 檔後，/etf-dash/?view=overview
# 一頁看全部基金（見 docs/etf-dash/index.html renderOverview()）。這裡把每檔
# 基金已經寫好的 docs/etf-dash/data/{ETF}.json 摘出幾個欄位彙總成一個小檔——
# 頁面只 fetch 這一個檔，不用對 17 檔各發一次 request。
# ---------------------------------------------------------------------------

SECTOR_ETF_KEYS = {"XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLC", "XLB"}


def _flow_amount_since(flows_data: dict | None, days: int, today_str: str) -> float | None:
    """把 flows.compute_flow_series() 存的逐日 flow_amount 加總「最近 N 天」
    （以最新一筆快照日期為基準，不是以「今天」為基準——資金流快照可能因為
    某天 attach_flows() 失敗而缺一天，見該函式）。沒有任何 daily 紀錄（剛
    上線、只有一天快照，還沒有 Δ 可算）回傳 None。"""
    if not flows_data or flows_data.get("skipped"):
        return None
    daily = flows_data.get("daily") or []
    if not daily:
        return None
    latest_date = flows_data.get("latest_date") or today_str
    cutoff = (datetime.strptime(latest_date, "%Y-%m-%d") - timedelta(days=days)).strftime("%Y-%m-%d")
    amt = sum(d["flow_amount"] for d in daily if d["date"] > cutoff)
    return round(amt, 2)


def build_overview_json() -> dict:
    """掃 docs/etf-dash/data/{ETF}.json（FUND_REGISTRY 目前已知的全部 key），
    不是只看這次 run 有沒有重建——單次 run 常常只更新一部分基金（例如只跑
    FULL 的那幾檔＋PRICE 的其他檔分開跑，或某檔基金這次抓取失敗被跳過），
    總覽頁要能看到「目前 docs/ 下最新的狀態」，不是「這次 run 動到的那幾檔」。
    分組（美股大盤／美股產業／半導體／亞洲）與短標籤是頁面呈現層的事，交給
    docs/etf-dash/index.html 的 FUND_GROUPS（唯一負責分組的地方）決定，這裡
    只給 flat 陣列＋etf_key。summary_sentence_zh 是純機械句（見下方，只挑最大值
    報數字，不下判斷字眼），9 檔美股產業 ETF 都有 90d 資料才會產生。"""
    funds = []
    for etf_key in FUND_REGISTRY:
        path = OUT_DIR / f"{etf_key}.json"
        if not path.exists():
            continue
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"[etf_dash] WARNING overview: could not read {path}: {e}", file=sys.stderr)
            continue
        periods_by_key = {p.get("key"): p for p in (d.get("periods") or [])}
        p30, p90 = periods_by_key.get("30d") or {}, periods_by_key.get("90d") or {}
        fpe = d.get("weighted_forward_pe") or {}
        breadth_90d = (d.get("breadth") or {}).get("90d") or {}
        flows_data = d.get("flows") or {}
        funds.append({
            "etf_key": etf_key,
            "label_zh": d.get("label_zh"),
            "yf_ticker": d.get("yf_ticker"),
            "eps_chg_pct_30d": p30.get("eps_chg_pct"),
            "eps_chg_pct_90d": p90.get("eps_chg_pct"),
            "price_chg_pct_30d": p30.get("price_chg_pct"),
            "price_chg_pct_90d": p90.get("price_chg_pct"),
            "implied_pe_chg_pct_30d": p30.get("implied_pe_chg_pct"),
            "implied_pe_chg_pct_90d": p90.get("implied_pe_chg_pct"),
            "weighted_forward_pe": fpe.get("value"),
            "eps_as_of": d.get("eps_as_of"),
            "as_of": d.get("as_of"),
            "mode": d.get("mode"),
            "holdings_stale": bool(d.get("holdings_stale")),
            "holdings_approximation_zh": d.get("holdings_approximation_zh"),
            # 2026-09-26 加：總覽表的修正廣度欄（stacked mini-bar）＋資金流欄。
            "breadth_90d": {
                "up_weight_pct": breadth_90d.get("up_weight_pct"),
                "flat_weight_pct": breadth_90d.get("flat_weight_pct"),
                "down_weight_pct": breadth_90d.get("down_weight_pct"),
                "n_covered": breadth_90d.get("n_covered"),
            },
            "flow_1m_net": _flow_amount_since(flows_data, 30, d.get("as_of") or ""),
            "flow_nav_currency": flows_data.get("nav_currency"),
            "flows_skipped": bool(flows_data.get("skipped")),
        })
    funds.sort(key=lambda f: f["etf_key"])

    # 產業資金流——9 檔 SPDR 產業 ETF 的最新一週／近一個月淨流量並排（見任務
    # 指示的 overview「產業資金流」圖），資料完全來自各基金已經寫好的 flows
    # 區塊，不重算。剛上線（daily 紀錄不足一週）某些基金這裡會是 None，頁面
    # 端要能處理（見 docs/etf-dash/index.html renderSectorFlows()）。
    sector_flows = []
    for etf_key in sorted(SECTOR_ETF_KEYS):
        path = OUT_DIR / f"{etf_key}.json"
        if not path.exists():
            continue
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        flows_data = d.get("flows") or {}
        weekly = flows_data.get("weekly") or []
        sector_flows.append({
            "etf_key": etf_key,
            "label_zh": SECTOR_ETF_LABEL_ZH.get(etf_key, etf_key),
            "latest_week_flow": weekly[-1]["flow_amount"] if weekly else None,
            "flow_1m_net": _flow_amount_since(flows_data, 30, d.get("as_of") or ""),
            "nav_currency": flows_data.get("nav_currency"),
            "skipped": bool(flows_data.get("skipped")),
        })

    sector_funds = [f for f in funds if f["etf_key"] in SECTOR_ETF_KEYS and f["eps_chg_pct_90d"] is not None]
    summary_sentence_zh = None
    if sector_funds:
        top = max(sector_funds, key=lambda f: f["eps_chg_pct_90d"])
        # label_zh 本身已經帶一層括號（如「科技類股 SPDR 基金（XLK，S&P 科技產業，
        # 美國掛牌）」），這句還要再接一層百分比括號——括號套括號可讀性差，這裡
        # 只取 label_zh 第一個括號前的短名＋ticker，不整段照搬。
        name = (top["label_zh"] or top["etf_key"]).split("（")[0].strip() + f"（{top['etf_key']}）"
        pe_chg = top.get("implied_pe_chg_pct_90d")
        summary_sentence_zh = (
            f"{len(sector_funds)} 檔美股產業 ETF 中，近三個月成分股加權明年度 EPS 預估上修幅度最大的是"
            f"{name}（{top['eps_chg_pct_90d']:+.2f}%）"
        )
        summary_sentence_zh += (f"，隱含本益比變動 {pe_chg:+.2f}%。" if pe_chg is not None else "。")

    return {
        "schema": "etf-dash-overview-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "as_of": taipei_now().strftime("%Y-%m-%d"),
        "funds": funds,
        "summary_sentence_zh": summary_sentence_zh,
        "sector_flows": sector_flows,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--etf", action="append", required=True, choices=list(FUND_REGISTRY.keys()),
                    help="可重複給多次；例：--etf SMH --etf SMH_UCITS")
    ap.add_argument("--preview-only", action="store_true", help="只重算 preview HTML，不重抓資料（需已有 docs/etf-dash/data/{ETF}.json）")
    ap.add_argument("--mode", choices=["auto", "full", "price"], default="auto",
                     help="auto（預設）＝每檔基金各自照 decide_mode() 規則判斷；"
                          "full／price＝對這次跑的每一檔基金強制指定，跳過判斷")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    HOLDINGS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    EPS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if args.preview_only:
        for etf_key in args.etf:
            out_path = OUT_DIR / f"{etf_key}.json"
            if not out_path.exists():
                print(f"[etf_dash] ERROR {out_path} missing, cannot do --preview-only", file=sys.stderr)
                return 1
            data = json.loads(out_path.read_text(encoding="utf-8"))
            (PREVIEW_DIR / f"{etf_key}.html").write_text(render_preview_html(data), encoding="utf-8")
            print(f"[etf_dash] wrote preview {PREVIEW_DIR / f'{etf_key}.html'}")
        return 0

    today = datetime.now()
    ticker_cache: dict = {}
    fx_cache = load_fx_daily_cache()
    rc_cache = load_reporting_currency_cache()
    stock_dash_universe = load_stock_dash_universe()

    # 長線 EPS 指數的資料源：先把「今天」併入 dd_eps_history.jsonl（append-only，
    # 只寫今天這一行；純讀 checkout 出來的 latest.json，不需要 git——shallow
    # clone 的 CI 也能跑），再讀出全部已知天數餵給 build_long_eps_index()。
    # 檔案本身的成長（git 完整歷史的一次性 backfill）另外用
    # `python3 scripts/etf_dash/dd_eps_history.py --backfill` 手動跑，見該檔
    # docstring；backfill 只需要跑一次，之後每次 build 都只是 append 一行。
    dd_eps_history.append_today(date_str=today.strftime("%Y-%m-%d"))
    dd_days = dd_eps_history.load_days()
    print(f"[etf_dash] dd_eps_history: {len(dd_days)} day(s) "
          f"({min(dd_days) if dd_days else '—'} .. {max(dd_days) if dd_days else '—'}), "
          f"{dd_eps_history.JSONL_PATH.stat().st_size if dd_eps_history.JSONL_PATH.exists() else 0} bytes")

    # 2026-09-26 加的三個唯讀查找表／一個輸出累加器——見各自模組
    # docstring／resolve_sector()／build_fund_full() 的參數說明。都在迴圈開始
    # 前建好一次（跟 dd_days／stock_dash_universe 同一個既有慣例），不是每檔
    # 基金各自重算一次。
    price_days = price_history.load_days()
    price_days = backfill_price_history_if_needed(price_days)  # self-heal — 見該函式 docstring
    refresh_sector_lookup_only_holdings()  # XLRE／XLU，僅供下一行的反查表用，見該函式註解
    us_sector_lookup = build_us_sector_lookup()
    tw_industry_map = get_tw_industry_map()
    price_today_closes: dict[str, float] = {}
    print(f"[etf_dash] price_history: {len(price_days)} day(s) on file; "
          f"us_sector_lookup covers {len(us_sector_lookup)} ticker(s); "
          f"tw_industry_map covers {len(tw_industry_map)} code(s)")

    n_ok = 0
    n_fail = 0
    for etf_key in args.etf:
        cfg = FUND_REGISTRY[etf_key]
        print(f"[etf_dash] building {etf_key} ({cfg['label_en']}) ...")
        try:
            data = build_fund(etf_key, cfg, ticker_cache, fx_cache, rc_cache, dd_days, today,
                               stock_dash_universe, args.mode, price_days, us_sector_lookup,
                               tw_industry_map, price_today_closes)
        except Exception as e:  # noqa: BLE001
            print(f"[etf_dash] ERROR {etf_key} failed: {e}", file=sys.stderr)
            n_fail += 1
            continue
        out_path = OUT_DIR / f"{etf_key}.json"
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[etf_dash] wrote {out_path} "
              f"(mode={data.get('mode')}, holdings {data['n_holdings']}, covered {data['n_holdings_covered']}, "
              f"stale_holdings={data['holdings_stale']})")
        preview_path = PREVIEW_DIR / f"{etf_key}.html"
        preview_path.write_text(render_preview_html(data), encoding="utf-8")
        print(f"[etf_dash] wrote preview {preview_path}")
        n_ok += 1

    save_fx_daily_cache(fx_cache)
    save_reporting_currency_cache(rc_cache)

    # 報酬貢獻的價格歷史——見 price_history.py 模組 docstring：這次 run 蒐集到
    # 的每檔 ticker「今天」收盤價（跨所有這次跑的基金聯集），併入既有序列，
    # 裁到最近 MAX_ROWS 天。今天完全沒有任何基金成功建置（price_today_closes
    # 是空的）就不寫這一行——不要用空字典覆蓋掉已有的資料。
    if price_today_closes:
        price_history.append_today(today.strftime("%Y-%m-%d"), price_today_closes)
        print(f"[etf_dash] price_history: recorded {len(price_today_closes)} ticker close(s) for today")

    # 總覽頁（/etf-dash/?view=overview）的小檔——見 build_overview_json()
    # docstring：一律重掃 OUT_DIR 目前已有的全部基金 JSON，不是只看這次 run
    # 動到的那幾檔，所以即使這次只跑一部分基金也要做（不需要 n_ok>0 才做，
    # 只要 OUT_DIR 裡有任何既有 JSON 就能生出一份有意義的總覽）。
    overview_path = OUT_DIR / "overview.json"
    overview_path.write_text(json.dumps(build_overview_json(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[etf_dash] wrote {overview_path}")

    # 稽核用：PRICE 模式這次 run 應該是 0——fetch_ticker_eps_and_price()（唯一
    # 會碰 eps_trend 的函式）只在 build_fund_full() 的逐檔迴圈裡被呼叫，
    # build_fund_price() 完全不會走到那條路徑。
    print(f"[etf_dash] eps_trend calls this run: {EPS_TREND_CALL_COUNT}")

    if n_ok == 0:
        print("[etf_dash] ERROR all requested funds failed", file=sys.stderr)
        return 1
    if n_fail:
        print(f"[etf_dash] WARNING {n_fail} fund(s) failed, {n_ok} succeeded", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
