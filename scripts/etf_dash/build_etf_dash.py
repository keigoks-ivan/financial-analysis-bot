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
EPS_CACHE_MAX_AGE_DAYS = 7  # 超過這麼多天沒更新，即使不是週六也強制 FULL


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


def classify_revision(base: float | None, current: float | None) -> tuple[str, str | None, float | None, float | None]:
    """純函式（不碰快取／網路）：判斷一筆「N 天前 EPS → 今日 EPS」修正% 該怎麼用。
    回傳 (status, reason, raw_pct, capped_pct)：

      - "no_base"：base 缺值（那個時間點 yfinance 根本沒抓到資料）——不是異常，
        只是覆蓋率不足，raw_pct/capped_pct/reason 都是 None，沿用既有行為
        （這筆不進任何加總，也不進 period_exclusions——那份名單只記「有資料
        但資料壞掉」的情況，跟「沒資料」分開，語意才清楚）。
      - "invalid_base"：current<=0，或 base<=0，或 |base| 相對 current 過小
        （REVISION_BASE_MIN_RATIO 門檻——SPCX／ECHO／HON 這類基期趨近 0 或
        翻負號、企業行動造成分母跳動的案例）。整筆排除，不進任何加總
        （raw_pct/capped_pct 為 None），reason 說明原因，呼叫端要記進
        period_exclusions。
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
    raw_pct = (current / base - 1) * 100
    capped_pct = max(-REVISION_CAP_PCT, min(REVISION_CAP_PCT, raw_pct))
    status = "capped" if abs(raw_pct - capped_pct) > 1e-9 else "ok"
    return status, None, round(raw_pct, 4), round(capped_pct, 4)

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


def decide_mode(cli_mode: str, eps_cache: dict | None, now_taipei: datetime) -> tuple[str, str]:
    """純函式（不碰檔案／網路——是否讀得到快取由呼叫端先讀好傳進來)：決定這次
    要跑 FULL 還是 PRICE，回傳 (mode, reason)。

    規則（cli_mode 明示 full／price 時最優先；"auto" 才照以下順序判斷）：
      1. 台北時區今天是週六 -> full。
      2. 完全沒有 EPS 快取（第一次跑、或快取被清掉）-> full。
      3. 快取的 eps_as_of 超過 EPS_CACHE_MAX_AGE_DAYS 天沒更新（保護：萬一連
         續幾個週六都因為 Invesco 406／假期跳過，不能無限期沿用舊 EPS）-> full。
      4. 快取的 eps_as_of 格式壞掉、讀不出日期 -> full（保守，壞資料不硬撐）。
      5. 以上都不是 -> price。
    """
    if cli_mode in ("full", "price"):
        return cli_mode, f"--mode {cli_mode}（明示）"
    if now_taipei.weekday() == 5:  # Monday=0 .. Saturday=5 .. Sunday=6
        return "full", "台北時區今天是週六"
    if eps_cache is None:
        return "full", "沒有 EPS 快取（第一次跑或快取遺失）"
    eps_as_of = eps_cache.get("eps_as_of")
    try:
        age_days = (now_taipei.date() - datetime.strptime(eps_as_of, "%Y-%m-%d").date()).days
    except (TypeError, ValueError):
        return "full", f"EPS 快取的 eps_as_of 格式壞掉（{eps_as_of!r}）"
    if age_days > EPS_CACHE_MAX_AGE_DAYS:
        return "full", f"EPS 快取已 {age_days} 天沒更新（> {EPS_CACHE_MAX_AGE_DAYS} 天門檻）"
    return "price", f"EPS 快取新鮮（{age_days} 天前，as of {eps_as_of}）且非週六"


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


HOLDINGS_SOURCES = {
    "vaneck": (fetch_holdings_xlsx, lambda raw: (*parse_holdings_xlsx(raw), [])),
    "ssga": (fetch_ssga_holdings_xlsx, parse_ssga_holdings_xlsx),
    "invesco": (fetch_invesco_holdings_json, parse_invesco_holdings_json),
    "twse": (fetch_twse_taiex_universe, parse_twse_taiex_universe),
    "yuanta": (fetch_yuanta_holdings_page, parse_yuanta_0050_holdings),
}


def get_holdings_with_fallback(etf_key: str, cfg: dict) -> tuple[str, list[dict], list[dict], str, bool]:
    """回傳 (as_of, holdings, non_equity, source_url, used_stale_cache)。

    抓取失敗（含格式改版、被擋、需要瀏覽器）一律退回上次成功快取，並清楚
    標記 used_stale_cache=True——絕不用空資料覆蓋 data/etf_dash/holdings_cache/
    裡的好資料（快取檔只在成功解析時才寫入）。兩者都沒有才整檔失敗。"""
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
        return as_of, rows, non_equity, cfg["holdings_url"], False
    except Exception as e:  # noqa: BLE001
        print(f"[etf_dash] WARNING holdings fetch failed for {etf_key}: {e}", file=sys.stderr)
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            print(f"[etf_dash] WARNING falling back to cached holdings for {etf_key} "
                  f"(as_of={cached['as_of']}, fetched_at={cached.get('fetched_at')})", file=sys.stderr)
            return (cached["as_of"], cached["holdings"], cached.get("non_equity", []),
                    cached.get("source_url", cfg["holdings_url"]), True)
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

    anchors = {}
    for key, col, _label, _days in PERIOD_DEFS:
        v = row.get(col)
        anchors[key] = None if v is None or pd.isna(v) else float(v)

    price = None
    price_currency = None
    try:
        fi = yf_call_with_backoff(lambda: t.fast_info, label=f"{ticker}.fast_info")
        price = fi.get("lastPrice") if hasattr(fi, "get") else getattr(fi, "last_price", None)
        if price is not None:
            price = float(price)
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


def build_methods_note_zh(cfg: dict, constituents: list[dict], non_equity: list[dict],
                           long_eps: dict, dd_universe_size: int, periods: list[dict],
                           mode: str, eps_as_of: str, mode_reason: str,
                           weight_methodology_note_zh: str | None = None) -> str:
    """組 methods_note_zh——2026-09-24 加 QQQ／SPY 之前這段是寫死給 SMH／
    SMH_UCITS 看的（硬編「VanEck」「ASML」「SK Hynix」）。四檔基金共用同一個
    build_fund()，持股來源、非美元成分股、TICKER_ALIAS 用到哪些、長線指數
    覆蓋率與異常事件都因基金而異，所以這裡全部改成從當次算好的資料動態組，
    不對其他基金硬猜。"""
    mode_zh = "完整更新（FULL：重抓持股與每檔 EPS 估計）" if mode == "full" else "只更新股價（PRICE：EPS 沿用快取）"
    parts = [
        f"本頁分層更新：每週六（台北時區）完整重抓一次持股與每檔明年度 EPS 估計"
        f"（現在的 EPS 估計 as of {eps_as_of}），其餘六天只抓股價，跟週六存的 EPS "
        "快取重新配對算「今日加權遠期本益比」——Exhibit 1 的期間表格（EPS 修正％／"
        "股價漲跌／隱含本益比）因此整週不變，只有本益比跟「EPS 預估更新於...」那行"
        f"每天更新。這次是{mode_zh}（{mode_reason}）。",
    ]
    if weight_methodology_note_zh:
        parts.append(weight_methodology_note_zh)
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


def build_fund_full(etf_key: str, cfg: dict, ticker_cache: dict, fx_cache: dict, rc_cache: dict,
                     dd_days: dict, today: datetime, stock_dash_universe: set[str],
                     mode_reason: str) -> dict:
    """FULL 模式：持股下載＋每檔 eps_trend，這是 tiered update 之前唯一的路徑
    （見模組開頭「Tiered update」段落）。跑完會把這次算出來的東西存進
    data/etf_dash/eps_cache/{ETF}.json（見 save_eps_cache()），PRICE 模式
    （build_fund_price()）整週沿用，不重抓。"""
    today_str = today.strftime("%Y-%m-%d")
    as_of_holdings, holdings, non_equity, source_url, used_stale = get_holdings_with_fallback(etf_key, cfg)
    weight_methodology_note_zh = build_weight_methodology_note_zh(cfg, holdings)

    unique_tickers = sorted({h["ticker"] for h in holdings})
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
    for h in holdings:
        info = ticker_cache[h["ticker"]]
        rec = {
            "ticker": h["ticker"], "name": h["name"], "weight_pct": h["weight_pct"],
            "has_stock_dash": h["ticker"] in stock_dash_universe,
        }
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
        })
        constituents.append(rec)

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

    # ---- weighted forward P/E (harmonic mean): 1 / Σ w_i * (EPS_i/price_i)
    pe_covered = [c for c in constituents if c["eps_fy_next_usd"] and c["price_usd"]]
    pe_covered_weight = sum(c["weight_pct"] or 0 for c in pe_covered)
    weighted_fwd_pe = None
    if pe_covered_weight > 0:
        yield_sum = sum((c["weight_pct"] / pe_covered_weight) * (c["eps_fy_next_usd"] / c["price_usd"])
                         for c in pe_covered)
        weighted_fwd_pe = round(1 / yield_sum, 2) if yield_sum > 0 else None

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
    long_chart_series = []
    if long_eps["series"]:
        start_pt = _closest_close_on_or_before(price_series, long_eps["start_date"])
        start_price = start_pt["close"] if start_pt else None
        for pt in long_eps["series"]:
            price_pt = _closest_close_on_or_before(price_series, pt["date"])
            price_index = (round(price_pt["close"] / start_price * 100, 4)
                            if (price_pt and start_price) else None)
            long_chart_series.append({
                "date": pt["date"], "eps_index": pt["eps_index"],
                "price_index": price_index, "coverage_pct": pt["coverage_pct"],
            })

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
        "holdings": holdings,
        "non_equity": non_equity,
        "tickers": cached_tickers,
        "periods": periods,
        "contributions": contributions_by_period,
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
        "eps_as_of": today_str,
        "price_since_eps_as_of_pct": 0.0,  # FULL 跑當天，eps_as_of 就是今天，定義上還沒有變動
        "holdings_as_of": as_of_holdings,
        "holdings_source_url": source_url,
        "holdings_issuer_zh": cfg["holdings_issuer_zh"],
        "holdings_stale": used_stale,
        "n_holdings": len(constituents) + len(excluded),
        "n_holdings_covered": len(constituents),
        "price": {"close": today_price_pt["close"], "date": today_price_pt["date"], "currency": pe_basis_ccy},
        "periods": periods,
        "weighted_forward_pe": {
            "value": weighted_fwd_pe,
            "coverage_pct": round(pe_covered_weight / total_weight * 100, 2) if total_weight else None,
            "method": f"harmonic mean 1/Σw_i·(EPS_i/price_i)；基準幣別 {pe_basis_ccy}，非{pe_basis_ccy}報表"
                      f"(如 ASML)的成分股先用當日 FX 換算成{pe_basis_ccy}",
        },
        "constituents": constituents,
        "excluded": excluded,
        "excluded_weight_pct": round(excluded_weight, 2),
        "non_equity": non_equity,
        "non_equity_weight_pct": round(non_equity_weight, 2),
        "contributions": contributions_by_period,
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
                                                  weight_methodology_note_zh=weight_methodology_note_zh),
    }


def build_fund_price(etf_key: str, cfg: dict, eps_cache: dict, fx_cache: dict, rc_cache: dict,
                      dd_days: dict, today: datetime, mode_reason: str) -> dict:
    """PRICE 模式：不下載持股、不呼叫 eps_trend（fetch_prices_batch() 完全是
    另一條路徑，見該函式），只批次抓 ETF 加所有成分股「今天」的收盤價，跟
    eps_cache（上次 FULL 存的，見 build_fund_full()）重新配對算「今日加權
    遠期本益比」與「EPS 預估更新後股價變動了多少」。Exhibit 1 的期間表格
    （periods）／貢獻分解（contributions）整份沿用 eps_cache 裡凍結的版本，
    不重算——這樣「近一個月／近二個月／近三個月」的 EPS 修正％跟股價漲跌才是
    同一個窗口算出來的，不會因為每天都用「今天」當窗口終點而互相對不齊（見
    模組開頭「Tiered update」的說明）。"""
    today_str = today.strftime("%Y-%m-%d")
    eps_as_of = eps_cache["eps_as_of"]
    holdings = eps_cache["holdings"]
    non_equity = eps_cache.get("non_equity", [])
    cached_tickers = eps_cache["tickers"]
    total_weight = sum(h["weight_pct"] or 0 for h in holdings)
    weight_methodology_note_zh = build_weight_methodology_note_zh(cfg, holdings)

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

    # ---- 今日加權遠期本益比：今天的價格 × 快取的 EPS（跟 FULL 模式同一個調和平均公式）
    pe_covered = [c for c in constituents if c["eps_fy_next_usd"] and c["price_usd"]]
    pe_covered_weight = sum(c["weight_pct"] or 0 for c in pe_covered)
    weighted_fwd_pe = None
    if pe_covered_weight > 0:
        yield_sum = sum((c["weight_pct"] / pe_covered_weight) * (c["eps_fy_next_usd"] / c["price_usd"])
                         for c in pe_covered)
        weighted_fwd_pe = round(1 / yield_sum, 2) if yield_sum > 0 else None

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
    long_chart_series = []
    if long_eps["series"]:
        start_pt = _closest_close_on_or_before(etf_series, long_eps["start_date"])
        start_price = start_pt["close"] if start_pt else None
        for pt in long_eps["series"]:
            price_pt = _closest_close_on_or_before(etf_series, pt["date"])
            price_index = (round(price_pt["close"] / start_price * 100, 4)
                            if (price_pt and start_price) else None)
            long_chart_series.append({
                "date": pt["date"], "eps_index": pt["eps_index"],
                "price_index": price_index, "coverage_pct": pt["coverage_pct"],
            })

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
        "eps_as_of": eps_as_of,
        "price_since_eps_as_of_pct": price_since_eps_as_of_pct,
        "holdings_as_of": eps_cache.get("holdings_as_of"),
        "holdings_source_url": eps_cache.get("holdings_source_url"),
        "holdings_issuer_zh": cfg["holdings_issuer_zh"],
        "holdings_stale": False,  # 不是抓取失敗，是設計上這週沒重抓——見 mode／methods_note_zh
        "n_holdings": len(constituents) + len(excluded),
        "n_holdings_covered": len(constituents),
        "price": {"close": today_price_pt["close"], "date": today_price_pt["date"], "currency": pe_basis_ccy},
        "periods": periods,
        "weighted_forward_pe": {
            "value": weighted_fwd_pe,
            "coverage_pct": round(pe_covered_weight / total_weight * 100, 2) if total_weight else None,
            "method": f"harmonic mean 1/Σw_i·(EPS_i/price_i)；EPS 沿用 eps_as_of 快取，股價是今天批次抓的，"
                      f"兩者都用今天的匯率換算成{pe_basis_ccy}，非{pe_basis_ccy}報表(如 ASML)一樣先換算",
        },
        "constituents": constituents,
        "excluded": excluded,
        "excluded_weight_pct": round(excluded_weight, 2),
        "non_equity": non_equity,
        "non_equity_weight_pct": round(non_equity_weight, 2),
        "contributions": eps_cache["contributions"],  # 凍結，整週不變
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
                                                  weight_methodology_note_zh=weight_methodology_note_zh),
    }


def build_fund(etf_key: str, cfg: dict, ticker_cache: dict, fx_cache: dict, rc_cache: dict,
               dd_days: dict, today: datetime, stock_dash_universe: set[str], cli_mode: str) -> dict:
    """FULL／PRICE 分派——見模組開頭「Tiered update」說明。decide_mode() 在這裡
    評估一次（不是在 main() 裡對整個 run 評估一次）：每檔基金各自的 EPS 快取
    新鮮度不同（例如 QQQ／SPY 剛上線那週還沒有快取，即使不是週六也會被判定
    要 FULL——這正是我們要的：第一次跑一定要有真資料才能建立快取），比在
    main() 算一次全域 mode 更貼近實際狀態。"""
    eps_cache = load_eps_cache(etf_key)
    mode, mode_reason = decide_mode(cli_mode, eps_cache, taipei_now())
    print(f"[etf_dash] {etf_key}: mode={mode} ({mode_reason})", file=sys.stderr)
    if mode == "price":
        try:
            return build_fund_price(etf_key, cfg, eps_cache, fx_cache, rc_cache, dd_days, today, mode_reason)
        except Exception as e:  # noqa: BLE001
            # PRICE 模式本身失敗（批次下載掛了之類）不代表 FULL 模式也會失敗
            # ——退回 FULL 跑一次，好過整檔直接沒資料（跟 holdings fetch 的
            # cache-fallback 哲學一致：能有資料就不要沒資料）。
            print(f"[etf_dash] WARNING {etf_key}: PRICE mode failed ({e}), falling back to FULL", file=sys.stderr)
            mode_reason = f"PRICE 模式失敗退回 FULL（{e}）"
    return build_fund_full(etf_key, cfg, ticker_cache, fx_cache, rc_cache, dd_days, today,
                            stock_dash_universe, mode_reason)


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

    n_ok = 0
    n_fail = 0
    for etf_key in args.etf:
        cfg = FUND_REGISTRY[etf_key]
        print(f"[etf_dash] building {etf_key} ({cfg['label_en']}) ...")
        try:
            data = build_fund(etf_key, cfg, ticker_cache, fx_cache, rc_cache, dd_days, today,
                               stock_dash_universe, args.mode)
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
