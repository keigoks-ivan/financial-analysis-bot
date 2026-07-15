#!/usr/bin/env python3
"""
build_monitor_internals.py — 市場偵測器 v2 Phase 1：內部結構／選擇權波動面／
宏觀 kill 級／部位情緒，共 38 條 series 的資料層＋異常引擎。

與 scripts/build_monitor.py（96 條機械層）平行、互不干涉：協議（series 定義
dict／compute_stats／zero-churn IO／fetch 慣例）自母版複製後擴充，不 import、
不改動母版一行。每日由 .github/workflows/monitor-daily.yml 在 stress score
之後執行，失敗不擋 monitor 核心。

四個面向：
  1. 市場內部結構（12 條，日頻）——docs/cache/prices-us.json 快照聚合（零新
     抓取，歷史自累積）＋產業／全球 breadth（yfinance 450d 自算可全回填）＋
     QQEW/QQQ 等權比＋SPY/QQQ 美元成交額。
  2. 選擇權與波動面（15 條，日頻）——CBOE 日檔 put/call 分項＋SPX 選擇權總量
     （0DTE 活動代理）逐日累積（--backfill-cboe 一次性回填）；VIX 家族與
     derived（VIX/VIX3M、VIX1D−VIX、VXN−VIX、VRP）全回填。
  3. 宏觀事件日曆＋宏觀 kill 級（7 條）——FRED 月頻（Sahm／核心 PCE YoY／CPI
     YoY／NFP 3 月均）＋日頻 10Y BEI；TreasuryDirect 10Y/30Y 標售 bid-to-cover
     與 primary dealer takedown。另讀 docs/monitor/data/macro_calendar.json
     輸出未來 14 天事件、為事件日前後的 alert 附 event 標籤。
  4. 加碼（4 條）——NAAIM 曝險指數（xlsx 全史重建）／FINRA 全市場空單量比
     （逐日累積，--backfill-finra）／IPO/SPY／DD universe EPS 上修寬度（月頻）。

統計協議沿用母版：日頻 252 窗／週頻 52 窗，新增月頻 12 窗（min_obs 8）。
樣本不足（obs < min_obs）的 series 標 warming_up、z 與分位輸出 null、不進
異常。落後 as_of 超過 5 天（週頻 12 天、月頻 45 天）標 stale、不進異常。

異常規則走新命名空間 RULES_V2（不動母版 RULES）；所有警報文案為描述句
（陳述數字與分位），禁擇時與買賣語，中文全形標點。定位＝描述器非擇時訊號。

輸出三檔（zero-churn，volatile＝generated_at）：
  docs/monitor/data/internals.json          當日整頁資料（monitor-internals-v1）
  docs/monitor/data/internals_history.json  每 key 滾動 450 筆時間序列
  docs/monitor/data/internals_alerts.json   滾動 60 天異常留痕

容錯：任一資料源掛掉→該面向進 gaps、不 abort；只有 prices cache 與 yfinance
全部失敗才 exit 1。FRED 一律用 requests 預設 UA（偽瀏覽器 UA 會 stall，見母版
註記）；其餘外部源帶 imq-monitor UA。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "docs", "monitor", "data")
INTERNALS_PATH = os.path.join(OUT_DIR, "internals.json")
HISTORY_PATH = os.path.join(OUT_DIR, "internals_history.json")
ALERTS_PATH = os.path.join(OUT_DIR, "internals_alerts.json")
CALENDAR_PATH = os.path.join(OUT_DIR, "macro_calendar.json")
MONITOR_LATEST_PATH = os.path.join(OUT_DIR, "latest.json")  # 母版輸出，唯讀
PRICES_US_PATH = os.path.join(ROOT, "docs", "cache", "prices-us.json")
DD_SCREENER_PATH = os.path.join(ROOT, "docs", "dd-screener", "latest.json")

YF_PERIOD = "450d"
STAT_WINDOW = 252            # 日頻一年統計窗
MIN_OBS = 60                 # 日頻最低樣本
HISTORY_CAP = 450            # internals_history.json 每 key 滾動上限
ALERTS_RETENTION_DAYS = 60
STALE_DAYS = {"d": 5, "w": 12, "m": 45}
REQ_TIMEOUT = 30
REQ_RETRIES = 2
THROTTLE_S = 0.2             # backfill 逐日請求間隔
GAPFILL_BDAYS = 7            # 日常 run 對 CBOE／FINRA 缺日往回補的商業日數
UA = {"User-Agent": "Mozilla/5.0 (compatible; imq-monitor/1.0)"}  # FRED 絕不帶

# 異常規則閾值（新命名空間，不動母版 RULES；文案一律描述句）
RULES_V2 = {
    "z_yellow": 2.0,            # |變動 z| ≥ 2 → 黃
    "z_red": 3.0,               # |變動 z| ≥ 3 → 紅
    "pctile_hi": 98.0,          # 水位分位 ≥ 98 → 黃（pct_alert 設定的 series）
    "pctile_lo": 2.0,           # 水位分位 ≤ 2 → 黃
    "streak": 5,                # 連漲跌 ≥ 5 日 → 黃（僅日頻）
    "thrust_hi": 90.0,          # brd_adv_dec ≥ 90 → 黃（廣度衝刺）
    "thrust_lo": 10.0,          # brd_adv_dec ≤ 10 → 黃
    "div_sp500_pctile": 95.0,   # 指數分位 ≥ 95（讀母版 latest.json sp500）
    "div_above50": 60.0,        # 且 brd_above50 < 60 → 黃
    "div_above200_pctile": 50.0,  # 同時 brd_above200 分位 ≤ 50 → 升紅
    "eqw_pctile_lo": 2.0,       # qqew_qqq 分位 ≤ 2 → 黃
    "vol_term_ratio": 1.0,      # vix_vix3m > 1.0 倒掛：新翻轉紅、持續黃
    "zdte_pctile": 98.0,        # vix1d_vix 分位 ≥ 98 且 spx_opt_vol z ≥ 2 → 黃
    "zdte_z": 2.0,
    "vrp_floor": 0.0,           # vrp_20d < 0 → 黃
    "pc_eq_hi": 98.0,           # pc_equity 分位 ≥ 98 或 ≤ 2 → 黃
    "pc_eq_lo": 2.0,
    "sv_hi": 98.0,              # short_vol_ratio 分位 ≥ 98 或 ≤ 2 → 黃
    "sv_lo": 2.0,
    "naaim_pctile": 98.0,       # naaim 分位 ≥ 98 或值 > 100 或 < 10 → 黃
    "naaim_hi": 100.0,
    "naaim_lo": 10.0,
    "sahm_trigger": 0.50,       # sahm ≥ 0.50 → 紅
    "auct_dealer_hi": 20.0,     # dealer > 20% 且 b2c < 2.3 → 黃；連兩場 → 紅
    "auct_b2c_lo": 2.3,
    "eps_rev_floor": 40.0,      # 上修比 < 40% 或月變 z ≤ −2 → 黃
    "eps_rev_z": -2.0,
}


def warn(msg: str) -> None:
    print(f"[internals][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[internals] {msg}")


# ───────────────────────────────────────────────────────────────────────────
# Universe 定義（協議同母版 _d，簡化 lo52_alert／scale，新增 note）
#
#   unit：pct（價格類，日變動 %）/ pp（百分比水位，變動＝差值 pt）
#         / abs（比率或指數水位，變動＝差值）/ bps（殖利率型，%.2f%%）
#         / k（千人）
# ───────────────────────────────────────────────────────────────────────────

CATEGORIES_V2 = [
    ("breadth", "市場內部結構"),
    ("options_vol", "選擇權與波動面"),
    ("macro", "宏觀 kill 級與事件"),
    ("positioning", "部位與情緒"),
]

# build_monitor.py sectors 類實際的 12 支（XBI 非 SMH，照母版清單）
SECTOR_ETFS = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU",
               "XLB", "XLRE", "XLC", "XBI"]
# build_monitor.py indices 類的 14 支全球指數
GLOBAL_IDX = ["^GSPC", "^NDX", "^DJI", "^RUT", "^SOX", "^TWII", "^N225",
              "^KS11", "^HSI", "^GDAXI", "^STOXX50E", "^FTSE", "VT", "EEM"]

S = {}  # key -> spec


def _d(key, label, cat, unit="pct", dp=2, prefix="", invert=False,
       pct_alert=None, freq="d", note=None, stale_days=None):
    """stale_days：個別覆寫 stale 門檻。FRED 月頻以「期別起始日」標日期（5 月
    PCE 標 05-01、6 月下旬才發布），發布 lag 使通用 45 天門檻不可達──期別標日
    的月頻 series 用 75 天（≈ 期別→發布 lag 上界＋餘裕），否則 kill 級指標會
    永久或週期性誤標 stale、無法進異常。"""
    S[key] = {"key": key, "label": label, "cat": cat, "unit": unit, "dp": dp,
              "prefix": prefix, "invert": invert, "pct_alert": pct_alert,
              "freq": freq, "note": note, "stale_days": stale_days}


# 面向 1｜市場內部結構（12 條，日頻）
_d("brd_above200", "站上 200 日線占比", "breadth", unit="pp", dp=1,
   note="docs/cache/prices-us.json 598 檔美股 universe，vs_200ma_pct > 0 占比；歷史自累積")
_d("brd_above50", "站上 50 日線占比", "breadth", unit="pp", dp=1,
   note="同 universe，ma50_pct > 0 占比")
_d("brd_adv_dec", "上漲家數占比", "breadth", unit="pp", dp=1,
   note="close_change_pct > 0 家數／（上漲＋下跌家數），平盤不計")
_d("brd_new_hi", "接近 52 週高占比", "breadth", unit="pp", dp=1,
   note="dist_52w_high_pct > −5%（距 52 週高 5% 內）占比")
_d("brd_new_lo", "接近 52 週低占比", "breadth", unit="pp", dp=1, invert=True,
   note="cache 中僅約 89/598 檔帶 low_52w 欄位，分母縮限為該子集；定義＝price ≤ low_52w × 1.05（近 52 週低 5% 內），與 new_hi 的 −5% 對稱")
_d("brd_rsi_hot", "RSI14 ≥ 70 占比", "breadth", unit="pp", dp=1)
_d("brd_rsi_cold", "RSI14 ≤ 30 占比", "breadth", unit="pp", dp=1, invert=True)
_d("brd_sec_above50", "產業 ETF 站上 50 日線占比", "breadth", unit="pp", dp=1,
   note="12 支美股產業 ETF（11 SPDR＋XBI，同 monitor 母版 sectors 清單）之 % above 50DMA，yfinance 450d 自算全回填")
_d("brd_glb_above200", "全球指數站上 200 日線占比", "breadth", unit="pp", dp=1,
   note="14 支全球指數（同 monitor 母版 indices 清單）之 % above 200DMA，全回填")
_d("qqew_qqq", "QQEW/QQQ 等權比", "breadth", unit="pct", dp=4)
_d("spy_dvol_z", "SPY 美元成交額（十億）", "breadth", unit="pct", dp=1, prefix="$",
   note="Close × Volume／1e9；z＝日變動百分比的 z-score（與其餘 series 同一統計機制）")
_d("qqq_dvol_z", "QQQ 美元成交額（十億）", "breadth", unit="pct", dp=1, prefix="$",
   note="同 spy_dvol_z 定義")

# 面向 2｜選擇權與波動面（15 條，日頻）
_d("pc_total", "Put/Call 總比", "options_vol", unit="abs", dp=2,
   note="CBOE 全產品 put/call ratio，日檔逐日累積")
_d("pc_index", "Put/Call 指數選擇權", "options_vol", unit="abs", dp=2)
_d("pc_equity", "Put/Call 個股選擇權", "options_vol", unit="abs", dp=2)
_d("pc_vix", "Put/Call VIX 選擇權", "options_vol", unit="abs", dp=2)
_d("spx_opt_vol", "SPX＋SPXW 選擇權總量（百萬口）", "options_vol", unit="pct", dp=2,
   note="0DTE 活動代理——SPX＋SPXW 全部到期日總量，非 0DTE 分項（CBOE 免費日檔無到期日拆分）")
_d("vix1d", "VIX1D", "options_vol", invert=True, pct_alert="high")
_d("vix3m", "VIX3M", "options_vol", invert=True, pct_alert="high")
_d("vix6m", "VIX6M", "options_vol", invert=True, pct_alert="high")
_d("vxn", "VXN 那斯達克波動", "options_vol", invert=True, pct_alert="high")
_d("ovx", "OVX 原油波動", "options_vol", invert=True, pct_alert="high")
_d("gvz", "GVZ 黃金波動", "options_vol", invert=True, pct_alert="high")
_d("vix_vix3m", "VIX/VIX3M 期限比", "options_vol", unit="pct", dp=3, invert=True,
   note="> 1.0＝三個月期限結構倒掛")
_d("vix1d_vix", "VIX1D−VIX 利差", "options_vol", unit="abs", dp=2, invert=True)
_d("vxn_vix", "VXN−VIX 利差", "options_vol", unit="abs", dp=2)
_d("vrp_20d", "波動風險溢價（20 日）", "options_vol", unit="abs", dp=2,
   note="VIX − SPX 20 交易日已實現波動年化；< 0＝隱含低於已實現")

# 面向 3｜宏觀 kill 級（7 條）
_d("sahm", "Sahm Rule 失業率指標", "macro", unit="abs", dp=2, invert=True, freq="m",
   note="≥ 0.50 為歷史衰退觸發水位（SAHMREALTIME）", stale_days=75)
_d("core_pce_yoy", "核心 PCE 年增率", "macro", unit="pp", dp=2, invert=True, freq="m",
   stale_days=75)
_d("cpi_yoy", "CPI 年增率", "macro", unit="pp", dp=2, invert=True, freq="m",
   stale_days=75)
_d("payems_3m", "非農月增（3 月均）", "macro", unit="k", dp=0, freq="m",
   note="PAYEMS 月增的 3 個月移動平均，單位千人", stale_days=75)
_d("bei10y", "10Y 通膨預期", "macro", unit="bps", pct_alert="both")
_d("auct_b2c", "10Y/30Y 標售 bid-to-cover", "macro", unit="abs", dp=2, freq="w",
   note="TreasuryDirect 10Y／30Y（term 含 reopening）標售，每場一點，週頻語意")
_d("auct_dealer", "標售 primary dealer 承接比", "macro", unit="pp", dp=1,
   invert=True, freq="w",
   note="primary dealer accepted／total accepted；dealer 承接高＝終端需求弱")

# 面向 4｜加碼（4 條）
_d("naaim", "NAAIM 主動經理人曝險指數", "positioning", unit="abs", dp=1, freq="w",
   note="官方 xlsx 全史每次重建；> 100＝槓桿做多、< 10＝接近空倉")
_d("short_vol_ratio", "全市場空單量比", "positioning", unit="abs", dp=3,
   note="FINRA regsho 日檔 ΣShortVolume／ΣTotalVolume，逐日累積")
_d("ipo_spy", "IPO/SPY 比", "positioning", unit="pct", dp=4)
_d("eps_rev_breadth", "EPS 上修家數占比", "positioning", unit="pp", dp=1, freq="m",
   note="DD universe（docs/dd-screener，約 241 檔）eps_revision_pct > 0 占比，非全市場；月頻 upsert")

MONTHLY_UPSERT_KEYS = {"eps_rev_breadth"}


# ───────────────────────────────────────────────────────────────────────────
# Zero-churn IO（逐字沿用母版協議）
# ───────────────────────────────────────────────────────────────────────────

def _serialize(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {os.path.basename(path)}: {e}")
        return default


def write_json_if_changed(path, obj, volatile=("generated_at",)) -> bool:
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


# ───────────────────────────────────────────────────────────────────────────
# HTTP helpers
# ───────────────────────────────────────────────────────────────────────────

def http_get(url, headers=None, timeout=REQ_TIMEOUT, retries=REQ_RETRIES,
             ok_missing=False):
    """帶重試的 GET。ok_missing=True 時 404／403 直接回 None 不重試——CBOE 與
    FINRA 的日檔對「不存在的日期」（假日／尚未發布）實測回 403 而非 404。"""
    import requests
    last_err = None
    for i in range(retries + 1):
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            if r.status_code in (403, 404) and ok_missing:
                return None
            r.raise_for_status()
            return r
        except Exception as e:
            last_err = e
            if i < retries:
                time.sleep(1.0 + i)
    warn(f"GET {url}: {last_err}")
    return None


# ───────────────────────────────────────────────────────────────────────────
# 資料抓取
# ───────────────────────────────────────────────────────────────────────────

def fetch_yf_ext(tickers: list[str], vol_tickers: tuple = ()) -> tuple[dict, dict]:
    """批量抓 450d：回傳 ({ticker: [(date, close)]}, {ticker: [(date, 美元成交額十億)]})。
    Volume 只對 vol_tickers 白名單取（母版 fetch_yf 的擴充版本）。"""
    import pandas as pd
    import yfinance as yf
    out_close, out_dvol = {}, {}
    df = yf.download(tickers, period=YF_PERIOD, interval="1d", auto_adjust=True,
                     progress=False, threads=True, group_by="column")
    if df is None or len(df) == 0:
        return out_close, out_dvol
    if isinstance(df.columns, pd.MultiIndex):
        close = df["Close"]
        vol = df["Volume"] if "Volume" in set(df.columns.get_level_values(0)) else None
    else:
        close = df[["Close"]].rename(columns={"Close": tickers[0]})
        vol = df[["Volume"]].rename(columns={"Volume": tickers[0]}) \
            if "Volume" in df.columns else None
    for tk in close.columns:
        pts = []
        for idx, val in close[tk].items():
            try:
                c = float(val)
            except (TypeError, ValueError):
                continue
            if c != c or c <= 0:
                continue
            pts.append((idx.date().isoformat(), round(c, 6)))
        if pts:
            out_close[str(tk)] = pts
    if vol is not None:
        for tk in vol_tickers:
            if tk not in close.columns or tk not in vol.columns:
                continue
            pts = []
            for idx in close.index:
                try:
                    c = float(close[tk].loc[idx])
                    v = float(vol[tk].loc[idx])
                except (TypeError, ValueError, KeyError):
                    continue
                if c != c or v != v or c <= 0 or v <= 0:
                    continue
                pts.append((idx.date().isoformat(), round(c * v / 1e9, 4)))
            if pts:
                out_dvol[str(tk)] = pts
    return out_close, out_dvol


def fetch_fred(series_id: str, last_n: int | None = 600) -> list | None:
    """FRED CSV endpoint（免 key）。不帶自訂 UA——FRED 會 stall 偽瀏覽器字串
    （實測 read timeout），requests 預設 UA 正常（母版註記）。"""
    import requests
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        r = requests.get(url, timeout=REQ_TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        warn(f"FRED {series_id}: {e}")
        return None
    pts = []
    for line in r.text.strip().split("\n")[1:]:
        parts = line.split(",")
        if len(parts) < 2 or parts[1] in ("", "."):
            continue
        try:
            pts.append((parts[0], float(parts[1])))
        except ValueError:
            continue
    if last_n:
        pts = pts[-last_n:]
    return pts or None


def fetch_cboe_day(date_iso: str) -> dict | None:
    """CBOE 日檔 → {pc_total, pc_index, pc_equity, pc_vix, spx_opt_vol}。
    404（假日／尚未發布）→ None。ratios 用 name 比對，不假設固定順序。"""
    url = ("https://cdn.cboe.com/data/us/options/market_statistics/daily/"
           f"{date_iso}_daily_options")
    r = http_get(url, headers=UA, ok_missing=True)
    if r is None:
        return None
    try:
        j = r.json()
    except ValueError:
        warn(f"CBOE {date_iso}: 非 JSON 回應")
        return None
    out = {}
    for row in j.get("ratios", []):
        name = str(row.get("name", "")).upper()
        if "PUT/CALL" not in name:
            continue
        try:
            v = float(row.get("value"))
        except (TypeError, ValueError):
            continue
        if name.startswith("TOTAL"):
            out["pc_total"] = v
        elif name.startswith("INDEX"):
            out["pc_index"] = v
        elif name.startswith("EQUITY"):
            out["pc_equity"] = v
        elif name.startswith("VIX") or "VOLATILITY" in name:
            out["pc_vix"] = v
    spx = j.get("SPX + SPXW")
    if isinstance(spx, list) and spx:
        row = next((x for x in spx
                    if str(x.get("name", "")).upper() == "VOLUME"), spx[0])
        tot = row.get("total")
        if isinstance(tot, (int, float)) and tot > 0:
            out["spx_opt_vol"] = round(tot / 1e6, 4)
    return out or None


def fetch_finra_day(date_iso: str) -> float | None:
    """FINRA regsho CNMS 日檔 → 全市場 ΣShortVolume／ΣTotalVolume。404 → None。"""
    ymd = date_iso.replace("-", "")
    url = f"https://cdn.finra.org/equity/regsho/daily/CNMSshvol{ymd}.txt"
    r = http_get(url, headers=UA, ok_missing=True)
    if r is None:
        return None
    short_sum = total_sum = 0.0
    for line in r.text.strip().split("\n"):
        parts = line.split("|")
        if len(parts) < 5 or parts[0] == "Date":
            continue
        try:
            short_sum += float(parts[2])
            total_sum += float(parts[4])
        except ValueError:
            continue
    if total_sum <= 0:
        return None
    return round(short_sum / total_sum, 6)


def fetch_treasury_auctions() -> tuple[list, list]:
    """TreasuryDirect 10Y（Note）＋30Y（Bond）標售 → (b2c_pts, dealer_pts)。
    term 欄位對 reopening 也保留原始期限（實測 '10-Year'），直接以 term 篩。
    同日多場（罕見）取平均。每場一點＝週頻語意。"""
    recs = []
    for typ in ("Note", "Bond"):
        url = ("https://www.treasurydirect.gov/TA_WS/securities/auctioned"
               f"?format=json&type={typ}")
        r = http_get(url, headers=UA, timeout=45)
        if r is None:
            continue
        try:
            data = r.json()
        except ValueError:
            warn(f"TreasuryDirect {typ}: 非 JSON 回應")
            continue
        for x in data:
            if x.get("term") not in ("10-Year", "30-Year"):
                continue
            d = str(x.get("auctionDate", ""))[:10]
            if not d:
                continue
            try:
                b2c = float(x.get("bidToCoverRatio") or 0)
                dealer = float(x.get("primaryDealerAccepted") or 0)
                total = float(x.get("totalAccepted") or 0)
            except (TypeError, ValueError):
                continue
            if b2c <= 0 or total <= 0:
                continue
            recs.append((d, b2c, dealer / total * 100.0))
    if not recs:
        return [], []
    by_date_b2c, by_date_dealer = {}, {}
    for d, b2c, dl in recs:
        by_date_b2c.setdefault(d, []).append(b2c)
        by_date_dealer.setdefault(d, []).append(dl)
    b2c_pts = [(d, round(sum(v) / len(v), 4)) for d, v in sorted(by_date_b2c.items())]
    dl_pts = [(d, round(sum(v) / len(v), 4)) for d, v in sorted(by_date_dealer.items())]
    return b2c_pts, dl_pts


def fetch_naaim() -> list | None:
    """NAAIM 頁面 → regex xlsx 連結 → openpyxl 解析全史。任何一步失敗 → None
    （fail-soft 進 gaps）。欄位偵測：header 列找 Date 欄＋含 NAAIM/Mean 的值欄。"""
    page = http_get("https://naaim.org/programs/naaim-exposure-index/", headers=UA)
    if page is None:
        return None
    m = re.search(r'href="([^"]*USE_Data[^"]*\.xlsx)"', page.text)
    if not m:
        m = re.search(r'href="([^"]*\.xlsx)"', page.text)
    if not m:
        warn("NAAIM: 頁面找不到 xlsx 連結")
        return None
    xurl = m.group(1)
    if xurl.startswith("/"):
        xurl = "https://naaim.org" + xurl
    info(f"NAAIM xlsx: {xurl}")
    xr = http_get(xurl, headers=UA, timeout=60)
    if xr is None:
        return None
    try:
        import io
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(xr.content), read_only=True,
                                    data_only=True)
        ws = wb.worksheets[0]
        rows = list(ws.iter_rows(values_only=True))
    except Exception as e:
        warn(f"NAAIM: xlsx 解析失敗：{e}")
        return None
    # 找 header 列與欄位 index
    hdr_i = date_col = val_col = None
    for i, row in enumerate(rows[:10]):
        cells = [str(c).strip().lower() if c is not None else "" for c in row]
        if any(c == "date" or c.startswith("date") for c in cells):
            hdr_i = i
            for j, c in enumerate(cells):
                if date_col is None and c.startswith("date"):
                    date_col = j
                if val_col is None and ("naaim" in c and "number" in c):
                    val_col = j
            if val_col is None:
                for j, c in enumerate(cells):
                    if "mean" in c or "average" in c or "naaim" in c:
                        val_col = j
                        break
            break
    if hdr_i is None or date_col is None or val_col is None:
        warn(f"NAAIM: 偵測不到 Date／值欄（hdr={hdr_i}, date={date_col}, val={val_col}）")
        return None
    pts = []
    for row in rows[hdr_i + 1:]:
        if row is None or len(row) <= max(date_col, val_col):
            continue
        d, v = row[date_col], row[val_col]
        if d is None or v is None:
            continue
        if isinstance(d, datetime):
            d_iso = d.date().isoformat()
        elif isinstance(d, date):
            d_iso = d.isoformat()
        else:
            try:
                d_iso = datetime.strptime(str(d)[:10], "%Y-%m-%d").date().isoformat()
            except ValueError:
                continue
        try:
            pts.append((d_iso, round(float(v), 4)))
        except (TypeError, ValueError):
            continue
    pts.sort()
    return pts or None


# ───────────────────────────────────────────────────────────────────────────
# 序列 derive helpers
# ───────────────────────────────────────────────────────────────────────────

def pct_above_ma(close_map: dict, tickers: list[str], n: int,
                 min_members: int) -> list:
    """多 ticker 的 % above n 日均線序列。各 ticker 在自身日曆上算 SMA，按日期
    聚合；當日成員數 < min_members 的日期不出點（跨時區假日錯位防呆）。"""
    per = {}
    for tk in tickers:
        pts = close_map.get(tk)
        if not pts or len(pts) < n:
            continue
        dates = [d for d, _ in pts]
        vals = [v for _, v in pts]
        csum = [0.0]
        for v in vals:
            csum.append(csum[-1] + v)
        for i in range(n - 1, len(vals)):
            sma = (csum[i + 1] - csum[i + 1 - n]) / n
            per.setdefault(dates[i], []).append(1.0 if vals[i] > sma else 0.0)
    return [(d, round(sum(a) / len(a) * 100, 2))
            for d, a in sorted(per.items()) if len(a) >= min_members]


def ratio_series(a: list, b: list, dp: int = 6) -> list:
    bm = dict(b)
    return [(d, round(v / bm[d], dp)) for d, v in a if d in bm and bm[d]]


def spread_series(a: list, b: list, dp: int = 6) -> list:
    bm = dict(b)
    return [(d, round(v - bm[d], dp)) for d, v in a if d in bm]


def realized_vol_20d(pts: list) -> list:
    """SPX 20 交易日已實現波動年化（%）。回傳與 pts 同日曆（自第 21 筆起）。"""
    if len(pts) < 22:
        return []
    dates = [d for d, _ in pts]
    vals = [v for _, v in pts]
    rets = [math.log(vals[i] / vals[i - 1]) for i in range(1, len(vals))]
    out = []
    for i in range(20, len(rets) + 1):
        w = rets[i - 20:i]
        m = sum(w) / 20
        var = sum((x - m) ** 2 for x in w) / 20
        out.append((dates[i], round(math.sqrt(var) * math.sqrt(252) * 100, 4)))
    return out


def yoy_series(pts: list) -> list:
    """月頻 series 的 12 期 YoY（%）。"""
    out = []
    for i in range(12, len(pts)):
        d, v = pts[i]
        _, v12 = pts[i - 12]
        if v12:
            out.append((d, round((v / v12 - 1) * 100, 4)))
    return out


def mom_3mavg_series(pts: list) -> list:
    """月增的 3 個月移動平均（PAYEMS 用，單位保持千人）。"""
    diffs = [(pts[i][0], pts[i][1] - pts[i - 1][1]) for i in range(1, len(pts))]
    out = []
    for i in range(2, len(diffs)):
        w = [diffs[i - 2][1], diffs[i - 1][1], diffs[i][1]]
        out.append((diffs[i][0], round(sum(w) / 3, 2)))
    return out


def business_days_back(end_iso: str, n_cal_days: int) -> list[str]:
    """end（含）往回 n_cal_days 日曆天內的商業日（一~五）清單，升冪。"""
    end_d = datetime.strptime(end_iso, "%Y-%m-%d").date()
    out = []
    for i in range(n_cal_days, -1, -1):
        d = end_d - timedelta(days=i)
        if d.weekday() < 5:
            out.append(d.isoformat())
    return out


# ───────────────────────────────────────────────────────────────────────────
# 面向 collectors（每個回傳 {key: [(date, val), ...]}；失敗回 {} 由 caller 記 gaps）
# ───────────────────────────────────────────────────────────────────────────

def collect_prices_us_breadth() -> tuple[dict, str | None]:
    """讀 prices-us.json 快照 → 7 條 brd_* 當日單點。回傳 (raw, cache_as_of)。"""
    cache = load_json(PRICES_US_PATH)
    if not cache or not cache.get("tickers"):
        return {}, None
    as_of = cache.get("as_of")
    tk = cache["tickers"]
    n_200 = n_50 = adv = dec = n_hi = n_hot = n_cold = 0
    total = 0
    lo_hit = lo_total = 0
    for sym, row in tk.items():
        v200 = row.get("vs_200ma_pct")
        v50 = row.get("ma50_pct")
        chg = row.get("close_change_pct")
        dhi = row.get("dist_52w_high_pct")
        rsi = row.get("rsi14")
        if v200 is None or v50 is None:
            continue
        total += 1
        if v200 > 0:
            n_200 += 1
        if v50 > 0:
            n_50 += 1
        if chg is not None:
            if chg > 0:
                adv += 1
            elif chg < 0:
                dec += 1
        if dhi is not None and dhi > -5:
            n_hi += 1
        if rsi is not None:
            if rsi >= 70:
                n_hot += 1
            if rsi <= 30:
                n_cold += 1
        lo52 = row.get("low_52w")
        px = row.get("price")
        if lo52 and px:
            lo_total += 1
            if px <= lo52 * 1.05:
                lo_hit += 1
    if not total or not as_of:
        return {}, as_of
    raw = {
        "brd_above200": [(as_of, round(n_200 / total * 100, 2))],
        "brd_above50": [(as_of, round(n_50 / total * 100, 2))],
        "brd_new_hi": [(as_of, round(n_hi / total * 100, 2))],
        "brd_rsi_hot": [(as_of, round(n_hot / total * 100, 2))],
        "brd_rsi_cold": [(as_of, round(n_cold / total * 100, 2))],
    }
    if adv + dec > 0:
        raw["brd_adv_dec"] = [(as_of, round(adv / (adv + dec) * 100, 2))]
    if lo_total >= 30:  # 子集太小就不出點（誠實缺席，不硬湊）
        raw["brd_new_lo"] = [(as_of, round(lo_hit / lo_total * 100, 2))]
    else:
        warn(f"brd_new_lo：low_52w 子集僅 {lo_total} 檔（< 30），本日不出點")
    return raw, as_of


def collect_yf_facets() -> tuple[dict, str | None]:
    """一次批次抓所有 yfinance 腳，derive 面向 1B／2／4 的可回填 series。
    回傳 (raw, gspc_last_date)。"""
    tickers = sorted(set(
        SECTOR_ETFS + GLOBAL_IDX +
        ["QQEW", "QQQ", "SPY", "IPO",
         "^VIX", "^VIX1D", "^VIX3M", "^VIX6M", "^VXN", "^OVX", "^GVZ"]))
    info(f"fetching {len(tickers)} yfinance tickers …")
    close_map, dvol_map = fetch_yf_ext(tickers, vol_tickers=("SPY", "QQQ"))
    missing = [t for t in tickers if t not in close_map]
    if missing:
        warn(f"yfinance missing: {', '.join(missing)}")
    raw = {}
    gspc = close_map.get("^GSPC")
    gspc_last = gspc[-1][0] if gspc else None

    # 面向 1B
    sec = pct_above_ma(close_map, SECTOR_ETFS, 50, min_members=10)
    if sec:
        raw["brd_sec_above50"] = sec
    glb = pct_above_ma(close_map, GLOBAL_IDX, 200, min_members=10)
    if glb:
        raw["brd_glb_above200"] = glb
    if close_map.get("QQEW") and close_map.get("QQQ"):
        raw["qqew_qqq"] = ratio_series(close_map["QQEW"], close_map["QQQ"], dp=6)
    if dvol_map.get("SPY"):
        raw["spy_dvol_z"] = dvol_map["SPY"]
    if dvol_map.get("QQQ"):
        raw["qqq_dvol_z"] = dvol_map["QQQ"]

    # 面向 2（yf 家族）
    for key, tk in [("vix1d", "^VIX1D"), ("vix3m", "^VIX3M"), ("vix6m", "^VIX6M"),
                    ("vxn", "^VXN"), ("ovx", "^OVX"), ("gvz", "^GVZ")]:
        if close_map.get(tk):
            raw[key] = close_map[tk]
    vix = close_map.get("^VIX")
    if vix and close_map.get("^VIX3M"):
        raw["vix_vix3m"] = ratio_series(vix, close_map["^VIX3M"], dp=6)
    if close_map.get("^VIX1D") and vix:
        raw["vix1d_vix"] = spread_series(close_map["^VIX1D"], vix, dp=4)
    if close_map.get("^VXN") and vix:
        raw["vxn_vix"] = spread_series(close_map["^VXN"], vix, dp=4)
    if vix and gspc:
        rv = realized_vol_20d(gspc)
        if rv:
            raw["vrp_20d"] = spread_series(vix, rv, dp=4)

    # 面向 4
    if close_map.get("IPO") and close_map.get("SPY"):
        raw["ipo_spy"] = ratio_series(close_map["IPO"], close_map["SPY"], dp=6)
    return raw, gspc_last


def collect_fred() -> dict:
    """FRED 月頻 kill 級＋日頻 BEI。個別失敗個別缺席。"""
    raw = {}
    sahm = fetch_fred("SAHMREALTIME")
    if sahm:
        raw["sahm"] = sahm
    pce = fetch_fred("PCEPILFE")
    if pce:
        y = yoy_series(pce)
        if y:
            raw["core_pce_yoy"] = y
    cpi = fetch_fred("CPIAUCSL")
    if cpi:
        y = yoy_series(cpi)
        if y:
            raw["cpi_yoy"] = y
    pay = fetch_fred("PAYEMS")
    if pay:
        m = mom_3mavg_series(pay)
        if m:
            raw["payems_3m"] = m
    bei = fetch_fred("T10YIE")
    if bei:
        raw["bei10y"] = bei
    return raw


def collect_cboe(history: dict, as_of: str, backfill_days: int) -> tuple[dict, int]:
    """CBOE 逐日累積＋缺日 gap-fill＋可選 backfill。回傳 (raw, 抓到的天數)。"""
    keys = ["pc_total", "pc_index", "pc_equity", "pc_vix", "spx_opt_vol"]
    existing = {d for k in keys for d, _ in history.get(k, [])}
    if backfill_days > 0:
        days = business_days_back(as_of, backfill_days)
    else:
        days = [d for d in business_days_back(as_of, GAPFILL_BDAYS + 3)
                if d not in existing][-(GAPFILL_BDAYS + 1):]
        # 當日一定重試（idempotent upsert，同日重跑覆蓋）
        if as_of not in days:
            days.append(as_of)
    raw = {k: [] for k in keys}
    got = 0
    for d in days:
        if backfill_days > 0 and d in existing:
            continue
        day = fetch_cboe_day(d)
        time.sleep(THROTTLE_S)
        if not day:
            continue
        got += 1
        for k in keys:
            if k in day:
                raw[k].append((d, day[k]))
    return {k: v for k, v in raw.items() if v}, got


def collect_finra(history: dict, as_of: str, backfill_days: int) -> tuple[dict, int]:
    """FINRA 逐日累積＋缺日 gap-fill＋可選 backfill。"""
    existing = {d for d, _ in history.get("short_vol_ratio", [])}
    if backfill_days > 0:
        days = business_days_back(as_of, backfill_days)
    else:
        days = [d for d in business_days_back(as_of, GAPFILL_BDAYS + 3)
                if d not in existing][-(GAPFILL_BDAYS + 1):]
        if as_of not in days:
            days.append(as_of)
    pts = []
    got = 0
    for d in days:
        if backfill_days > 0 and d in existing:
            continue
        v = fetch_finra_day(d)
        time.sleep(THROTTLE_S)
        if v is None:
            continue
        got += 1
        pts.append((d, v))
    return ({"short_vol_ratio": pts} if pts else {}), got


def collect_eps_breadth() -> dict:
    """DD screener EPS 上修寬度（月頻，按月 upsert 由 merge 處理）。"""
    scr = load_json(DD_SCREENER_PATH)
    if not scr or not scr.get("stocks"):
        return {}
    as_of = scr.get("as_of")
    vals = [s.get("eps_revision_pct") for s in scr["stocks"]
            if s.get("eps_revision_pct") is not None]
    if not as_of or len(vals) < 50:
        return {}
    pos = sum(1 for v in vals if v > 0)
    return {"eps_rev_breadth": [(as_of, round(pos / len(vals) * 100, 2))]}


# ───────────────────────────────────────────────────────────────────────────
# history merge
# ───────────────────────────────────────────────────────────────────────────

def merge_history(history: dict, raw_new: dict) -> dict:
    """按日期 union merge（新值覆蓋同日舊值），月頻 upsert keys 以 YYYY-MM 去重
    （同月新點覆蓋舊點，維持每月一點的窗口語意），每 key 截為最後 HISTORY_CAP 筆。"""
    for key, new_pts in raw_new.items():
        if not new_pts:
            continue
        cur = {d: v for d, v in history.get(key, [])}
        if key in MONTHLY_UPSERT_KEYS:
            new_months = {d[:7] for d, _ in new_pts}
            cur = {d: v for d, v in cur.items() if d[:7] not in new_months}
        for d, v in new_pts:
            cur[d] = v
        history[key] = sorted(cur.items())[-HISTORY_CAP:]
    return history


# ───────────────────────────────────────────────────────────────────────────
# 統計（母版 compute_stats ＋ freq="m" 支援 ＋ n_obs）
# ───────────────────────────────────────────────────────────────────────────

def compute_stats(pts: list, unit: str, freq: str = "d") -> dict | None:
    """pts = [(date, val), ...] 升冪。統計窗按頻率換算成「一年」：日頻 252 筆、
    週頻 52 筆、月頻 12 筆（min_obs 8）。樣本不足 → z／分位 None＋warming_up；
    自累積 series 首日僅 1 點也要出 item（warming_up），不進 gaps。"""
    if not pts:
        return None
    if freq == "d":
        win, min_obs = STAT_WINDOW, MIN_OBS
    elif freq == "w":
        win, min_obs = 52, 30
    else:  # "m"
        win, min_obs = 12, 8
    vals = [v for _, v in pts]
    dates = [d for d, _ in pts]
    if len(pts) == 1:
        return {"last": vals[0], "chg": None, "z": None, "pctile": None,
                "p20": None, "p60": None, "hi52": None, "lo52": None,
                "streak": 0, "spark": [round(vals[0], 6)], "date": dates[0],
                "n_obs": 1, "warming_up": True}
    last, prev = vals[-1], vals[-2]

    if unit == "pct":
        changes = [(vals[i] - vals[i - 1]) / vals[i - 1] * 100
                   for i in range(1, len(vals)) if vals[i - 1] != 0]
        chg = (last - prev) / prev * 100 if prev else None
    else:
        changes = [vals[i] - vals[i - 1] for i in range(1, len(vals))]
        chg = last - prev

    z = None
    base = changes[-(win + 1):-1]
    if chg is not None and len(base) >= min_obs:
        mean = sum(base) / len(base)
        var = sum((c - mean) ** 2 for c in base) / len(base)
        std = var ** 0.5
        if std > 1e-12:
            z = round((changes[-1] - mean) / std, 2)

    def pct_at(idx_from_end):
        pos = len(vals) - 1 - idx_from_end
        if pos < 0:
            return None
        w = vals[max(0, pos - win + 1):pos + 1]
        if len(w) < min_obs:
            return None
        return round(sum(1 for v in w if v <= vals[pos]) / len(w) * 100, 1)

    window = vals[-win:]
    pctile = hi52 = lo52 = None
    if len(window) >= min_obs:
        pctile = round(sum(1 for v in window if v <= last) / len(window) * 100, 1)
        eps = abs(last) * 1e-9
        hi52 = last >= max(window) - eps
        lo52 = last <= min(window) + eps
    if freq == "d":
        off20, off60 = 20, 60
    elif freq == "w":
        off20, off60 = 4, 12
    else:
        off20, off60 = 1, 3
    p20, p60 = pct_at(off20), pct_at(off60)

    streak = 0
    for c in reversed(changes):
        if c > 0 and streak >= 0:
            streak += 1
        elif c < 0 and streak <= 0:
            streak -= 1
        else:
            break

    spark = [round(v, 6) for v in vals[-30:]]
    return {"last": last, "chg": chg, "z": z, "pctile": pctile,
            "p20": p20, "p60": p60,
            "hi52": hi52, "lo52": lo52, "streak": streak,
            "spark": spark, "date": dates[-1],
            "n_obs": len(window), "warming_up": len(window) < min_obs}


def fmt_val(v, spec) -> str:
    if v is None:
        return "—"
    u = spec["unit"]
    if u == "bps":
        return f"{v:.2f}%"
    if u == "pp":
        return f"{v:.{spec['dp']}f}%"
    if u == "k":
        return f"{v:,.0f}K"
    return f"{spec['prefix']}{v:,.{spec['dp']}f}"


def fmt_chg(chg, unit, dp=2) -> str:
    if chg is None:
        return "—"
    arrow = "▲" if chg > 0 else ("▼" if chg < 0 else "＝")
    if unit == "pct":
        return f"{arrow} {abs(chg):.2f}%"
    if unit == "bps":
        return f"{arrow} {abs(chg) * 100:.0f}bps"
    if unit == "pp":
        return f"{arrow} {abs(chg):.2f}pt"
    if unit == "k":
        return f"{arrow} {abs(chg):.0f}K"
    return f"{arrow} {abs(chg):.3f}"


# ───────────────────────────────────────────────────────────────────────────
# 異常引擎（RULES_V2）
# ───────────────────────────────────────────────────────────────────────────

FREQ_LABEL = {"d": ("單日", "日波動"), "w": ("單期", "期波動"), "m": ("單月", "月波動")}


def series_alerts_v2(item: dict, spec: dict) -> list[dict]:
    """通用閘（沿用母版語意）：z 閘／水位分位閘（pct_alert）／連漲跌（日頻）。
    caller 已排除 stale 與 warming_up。"""
    out = []
    key, label, cat = spec["key"], spec["label"], spec["cat"]
    z, pctile = item.get("z"), item.get("pctile")

    if z is not None and abs(z) >= RULES_V2["z_yellow"]:
        sev = "red" if abs(z) >= RULES_V2["z_red"] else "yellow"
        period, vol = FREQ_LABEL[spec["freq"]]
        out.append({"sev": sev, "cat": cat, "key": key, "rule": "move_z",
                    "msg": f"{label} {period}{'漲' if item['chg'] > 0 else '跌'}"
                           f"幅 {item['chg_fmt']}，為一年{vol}的 {abs(z):.2f} 倍標準差"})
    pa = spec["pct_alert"]
    if pctile is not None and pa in ("high", "both") and pctile >= RULES_V2["pctile_hi"]:
        out.append({"sev": "yellow", "cat": cat, "key": key, "rule": "pctile",
                    "msg": f"{label} 現值 {item['val_fmt']} 進入一年水位前 "
                           f"{100 - pctile:.0f}%（分位 {pctile:.0f}）"})
    if pctile is not None and pa in ("low", "both") and pctile <= RULES_V2["pctile_lo"]:
        out.append({"sev": "yellow", "cat": cat, "key": key, "rule": "pctile",
                    "msg": f"{label} 現值 {item['val_fmt']} 落到一年水位後 "
                           f"{pctile:.0f}%（低分位警示）"})
    st = item.get("streak") or 0
    if abs(st) >= RULES_V2["streak"] and spec["freq"] == "d":
        out.append({"sev": "yellow", "cat": cat, "key": key, "rule": "streak",
                    "msg": f"{label} 連續 {abs(st)} 日{'上漲' if st > 0 else '下跌'}"})
    return out


def _live(items, key):
    """非 stale／非 warming 的 item，否則 None（結構規則共用防呆）。"""
    it = items.get(key)
    if not it or it.get("stale") or it.get("warming_up"):
        return None
    return it


def structural_alerts_v2(items: dict, history: dict) -> list[dict]:
    """面向特有跨 series 結構規則。警報全部描述句。"""
    alerts = []

    # brd_thrust：單日漲跌家數比極端（廣度衝刺／崩落）
    ad = _live(items, "brd_adv_dec")
    if ad and ad.get("last") is not None:
        if ad["last"] >= RULES_V2["thrust_hi"]:
            alerts.append({"sev": "yellow", "cat": "breadth", "key": "brd_adv_dec",
                           "rule": "brd_thrust",
                           "msg": f"上漲家數占比達 {ad['last']:.0f}%，"
                                  f"單日廣度衝刺（≥ {RULES_V2['thrust_hi']:.0f}%）"})
        elif ad["last"] <= RULES_V2["thrust_lo"]:
            alerts.append({"sev": "yellow", "cat": "breadth", "key": "brd_adv_dec",
                           "rule": "brd_thrust",
                           "msg": f"上漲家數占比僅 {ad['last']:.0f}%，"
                                  f"單日廣度崩落（≤ {RULES_V2['thrust_lo']:.0f}%）"})

    # brd_divergence：母版 latest.json 的 sp500 分位 ≥ 95 且 above50 < 60 → 黃；
    # brd_above200 分位 ≤ 50 同時成立 → 升紅。讀不到母版資料整條 skip（不猜）。
    b50 = _live(items, "brd_above50")
    mother = load_json(MONITOR_LATEST_PATH)
    sp500_pct = None
    if mother:
        for cat in mother.get("categories", []):
            for row in cat.get("items", []):
                if row.get("key") == "sp500":
                    sp500_pct = row.get("pctile")
                    break
    if (b50 and sp500_pct is not None
            and sp500_pct >= RULES_V2["div_sp500_pctile"]
            and b50.get("last") is not None
            and b50["last"] < RULES_V2["div_above50"]):
        sev = "yellow"
        extra = ""
        b200 = _live(items, "brd_above200")
        if (b200 and b200.get("pctile") is not None
                and b200["pctile"] <= RULES_V2["div_above200_pctile"]):
            sev = "red"
            extra = f"，且站上 200 日線占比分位僅 {b200['pctile']:.0f}"
        alerts.append({"sev": sev, "cat": "breadth", "key": "brd_above50",
                       "rule": "brd_divergence",
                       "msg": f"指數與廣度背離：S&P 500 一年分位 {sp500_pct:.0f}，"
                              f"但站上 50 日線占比僅 {b50['last']:.0f}%{extra}"})

    # eqw_div：等權／市值權比落到一年低分位
    eq = _live(items, "qqew_qqq")
    if (eq and eq.get("pctile") is not None
            and eq["pctile"] <= RULES_V2["eqw_pctile_lo"]):
        alerts.append({"sev": "yellow", "cat": "breadth", "key": "qqew_qqq",
                       "rule": "eqw_div",
                       "msg": f"QQEW/QQQ 等權比 {eq['val_fmt']} 落到一年水位後 "
                              f"{eq['pctile']:.0f}%，等權腳明顯落後市值權"})

    # vol_term_3m：VIX/VIX3M > 1.0 倒掛——新翻轉紅、持續黃
    vt = _live(items, "vix_vix3m")
    if vt and vt.get("last") is not None and vt["last"] > RULES_V2["vol_term_ratio"]:
        prev_ratio = None
        if vt.get("chg") is not None:
            prev_ratio = vt["last"] / (1 + vt["chg"] / 100)
        newly = prev_ratio is not None and prev_ratio <= RULES_V2["vol_term_ratio"]
        alerts.append({"sev": "red" if newly else "yellow", "cat": "options_vol",
                       "key": "vix_vix3m", "rule": "vol_term_3m",
                       "msg": f"VIX 三個月期限結構倒掛{'（今日新轉倒掛）' if newly else '中'}："
                              f"VIX/VIX3M = {vt['last']:.3f} > 1"})

    # zero_dte_stress：極端短波動水位＋SPX 選擇權量異常同日出現
    v1 = _live(items, "vix1d_vix")
    sv = _live(items, "spx_opt_vol")
    if (v1 and sv and v1.get("pctile") is not None and sv.get("z") is not None
            and v1["pctile"] >= RULES_V2["zdte_pctile"]
            and sv["z"] >= RULES_V2["zdte_z"]):
        alerts.append({"sev": "yellow", "cat": "options_vol", "key": "vix1d_vix",
                       "rule": "zero_dte_stress",
                       "msg": f"VIX1D−VIX 利差分位 {v1['pctile']:.0f} 且 SPX 選擇權"
                              f"總量 z = {sv['z']:.1f}，超短天期活動與定價同步偏熱"})

    # vrp_negative：隱含波動低於已實現
    vrp = _live(items, "vrp_20d")
    if vrp and vrp.get("last") is not None and vrp["last"] < RULES_V2["vrp_floor"]:
        alerts.append({"sev": "yellow", "cat": "options_vol", "key": "vrp_20d",
                       "rule": "vrp_negative",
                       "msg": f"波動風險溢價轉負：VIX 低於 SPX 20 日已實現波動 "
                              f"{abs(vrp['last']):.2f} 個波動點"})

    # pc_extreme：pc_equity 水位分位極端 → 黃。
    # （pc_total z ≥ 3 紅由通用 move_z 閘以同一門檻承接，不重複發。）
    pe = _live(items, "pc_equity")
    if pe and pe.get("pctile") is not None:
        if pe["pctile"] >= RULES_V2["pc_eq_hi"]:
            alerts.append({"sev": "yellow", "cat": "options_vol", "key": "pc_equity",
                           "rule": "pc_extreme",
                           "msg": f"個股 Put/Call 比 {pe['val_fmt']} 進入一年水位前 "
                                  f"{100 - pe['pctile']:.0f}%（避險需求偏高側極端）"})
        elif pe["pctile"] <= RULES_V2["pc_eq_lo"]:
            alerts.append({"sev": "yellow", "cat": "options_vol", "key": "pc_equity",
                           "rule": "pc_extreme",
                           "msg": f"個股 Put/Call 比 {pe['val_fmt']} 落到一年水位後 "
                                  f"{pe['pctile']:.0f}%（call 偏好側極端）"})

    # sv_extreme：全市場空單量比水位極端
    svr = _live(items, "short_vol_ratio")
    if svr and svr.get("pctile") is not None:
        if svr["pctile"] >= RULES_V2["sv_hi"]:
            alerts.append({"sev": "yellow", "cat": "positioning",
                           "key": "short_vol_ratio", "rule": "sv_extreme",
                           "msg": f"全市場空單量比 {svr['val_fmt']} 進入一年水位前 "
                                  f"{100 - svr['pctile']:.0f}%"})
        elif svr["pctile"] <= RULES_V2["sv_lo"]:
            alerts.append({"sev": "yellow", "cat": "positioning",
                           "key": "short_vol_ratio", "rule": "sv_extreme",
                           "msg": f"全市場空單量比 {svr['val_fmt']} 落到一年水位後 "
                                  f"{svr['pctile']:.0f}%"})

    # naaim_extreme：極端曝險水位（分位或絕對值）
    na = _live(items, "naaim")
    if na and na.get("last") is not None:
        hit = None
        if na["last"] > RULES_V2["naaim_hi"]:
            hit = f"現值 {na['last']:.1f} 高於 100（平均曝險超過全倉，含槓桿）"
        elif na["last"] < RULES_V2["naaim_lo"]:
            hit = f"現值 {na['last']:.1f} 低於 10（平均曝險接近空手）"
        elif (na.get("pctile") is not None
              and na["pctile"] >= RULES_V2["naaim_pctile"]):
            hit = f"現值 {na['last']:.1f} 進入一年水位前 {100 - na['pctile']:.0f}%"
        if hit:
            alerts.append({"sev": "yellow", "cat": "positioning", "key": "naaim",
                           "rule": "naaim_extreme",
                           "msg": f"NAAIM 主動經理人曝險指數{hit}"})

    # sahm_trigger：歷史衰退觸發水位
    sm = _live(items, "sahm")
    if (sm and sm.get("last") is not None
            and sm["last"] >= RULES_V2["sahm_trigger"]):
        alerts.append({"sev": "red", "cat": "macro", "key": "sahm",
                       "rule": "sahm_trigger",
                       "msg": f"Sahm Rule 指標達 {sm['last']:.2f}，觸及 0.50 的"
                              f"歷史衰退觸發水位"})

    # auction_weak：dealer 承接偏高＋b2c 偏弱；連兩場 → 紅
    b2c = _live(items, "auct_b2c")
    dlr = _live(items, "auct_dealer")
    if (b2c and dlr and b2c.get("last") is not None and dlr.get("last") is not None
            and dlr["last"] > RULES_V2["auct_dealer_hi"]
            and b2c["last"] < RULES_V2["auct_b2c_lo"]):
        sev = "yellow"
        b2c_h = history.get("auct_b2c", [])
        dlr_h = history.get("auct_dealer", [])
        if (len(b2c_h) >= 2 and len(dlr_h) >= 2
                and dlr_h[-2][1] > RULES_V2["auct_dealer_hi"]
                and b2c_h[-2][1] < RULES_V2["auct_b2c_lo"]):
            sev = "red"
        alerts.append({"sev": sev, "cat": "macro", "key": "auct_b2c",
                       "rule": "auction_weak",
                       "msg": f"公債標售偏弱{'（連續兩場）' if sev == 'red' else ''}："
                              f"primary dealer 承接 {dlr['last']:.1f}%（> 20%）、"
                              f"bid-to-cover {b2c['last']:.2f}（< 2.3）"})

    # eps_rev_deterioration：上修寬度惡化
    er = _live(items, "eps_rev_breadth")
    if er and er.get("last") is not None:
        hit = None
        if er["last"] < RULES_V2["eps_rev_floor"]:
            hit = f"上修家數占比 {er['last']:.0f}% 低於 40%"
        elif er.get("z") is not None and er["z"] <= RULES_V2["eps_rev_z"]:
            hit = f"月變動 z = {er['z']:.1f}，惡化速度為一年月波動的 {abs(er['z']):.1f} 倍標準差"
        if hit:
            alerts.append({"sev": "yellow", "cat": "positioning",
                           "key": "eps_rev_breadth", "rule": "eps_rev_deterioration",
                           "msg": f"DD universe EPS 修正寬度惡化：{hit}"})
    return alerts


# ───────────────────────────────────────────────────────────────────────────
# 宏觀事件日曆
# ───────────────────────────────────────────────────────────────────────────

def load_calendar_events() -> list[dict]:
    cal = load_json(CALENDAR_PATH)
    if not cal or cal.get("schema") != "macro-calendar-v1":
        return []
    return cal.get("events", [])


def upcoming_events(events: list[dict], as_of: str, horizon_days: int = 14) -> list[dict]:
    as_of_d = datetime.strptime(as_of, "%Y-%m-%d").date()
    out = []
    for ev in events:
        try:
            d = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            continue
        delta = (d - as_of_d).days
        if 0 <= delta <= horizon_days:
            out.append({"date": ev["date"], "type": ev.get("type", ""),
                        "label": ev.get("label", ""),
                        "confidence": ev.get("confidence", "estimated"),
                        "days_until": delta})
    out.sort(key=lambda e: e["date"])
    return out


def tag_event_alerts(alerts: list[dict], events: list[dict], as_of: str) -> None:
    """as_of 當日或前一日有宏觀事件時，為 macro／options_vol 面 alert 附 event 標籤。"""
    as_of_d = datetime.strptime(as_of, "%Y-%m-%d").date()
    window = {as_of_d.isoformat(), (as_of_d - timedelta(days=1)).isoformat()}
    hits = [ev for ev in events if ev.get("date") in window]
    if not hits:
        return
    tag = {"type": hits[0].get("type", ""), "label": hits[0].get("label", ""),
           "date": hits[0].get("date", "")}
    for a in alerts:
        if a["cat"] in ("macro", "options_vol"):
            a["event"] = tag


# ───────────────────────────────────────────────────────────────────────────
# main
# ───────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="市場偵測器 v2 Phase 1 internals collector")
    ap.add_argument("--backfill-cboe", type=int, default=0, metavar="N",
                    help="CBOE 日檔一次性回填 N 日曆天（throttle 0.2s/req）")
    ap.add_argument("--backfill-finra", type=int, default=0, metavar="N",
                    help="FINRA regsho 一次性回填 N 日曆天")
    args = ap.parse_args()

    hist_doc = load_json(HISTORY_PATH,
                         {"schema": "monitor-internals-history-v1", "series": {}})
    history = {k: [tuple(p) for p in v]
               for k, v in hist_doc.get("series", {}).items()}
    cal_events = load_calendar_events()
    if not cal_events:
        warn("macro_calendar.json 缺失或 schema 不符——事件層本輪缺席")

    gaps = []

    # 面向 1A：prices cache 快照
    cache_raw, cache_as_of = collect_prices_us_breadth()
    if not cache_raw:
        warn("prices-us.json 讀取失敗或空——面向 1A 缺席")

    # 面向 1B／2／4：yfinance 批次
    try:
        yf_raw, gspc_last = collect_yf_facets()
    except Exception as e:
        warn(f"yfinance batch failed: {e}")
        yf_raw, gspc_last = {}, None

    # 全掛防呆：prices cache 與 yf 都失敗才 abort
    if not cache_raw and not yf_raw:
        warn("prices cache 與 yfinance 全部失敗——aborting without write")
        return 1

    as_of = gspc_last or cache_as_of
    info(f"as_of = {as_of}")

    # 面向 3：FRED＋TreasuryDirect
    try:
        fred_raw = collect_fred()
    except Exception as e:
        warn(f"FRED failed: {e}")
        fred_raw = {}
    try:
        b2c_pts, dlr_pts = fetch_treasury_auctions()
    except Exception as e:
        warn(f"TreasuryDirect failed: {e}")
        b2c_pts, dlr_pts = [], []
    td_raw = {}
    if b2c_pts:
        td_raw["auct_b2c"] = b2c_pts
    if dlr_pts:
        td_raw["auct_dealer"] = dlr_pts

    # 面向 2：CBOE（累積型）
    try:
        cboe_raw, cboe_got = collect_cboe(history, as_of, args.backfill_cboe)
    except Exception as e:
        warn(f"CBOE failed: {e}")
        cboe_raw, cboe_got = {}, 0
    info(f"CBOE：本輪抓到 {cboe_got} 個交易日"
         + (f"（backfill {args.backfill_cboe} 日曆天）" if args.backfill_cboe else ""))

    # 面向 4：FINRA（累積型）＋NAAIM＋EPS breadth
    try:
        finra_raw, finra_got = collect_finra(history, as_of, args.backfill_finra)
    except Exception as e:
        warn(f"FINRA failed: {e}")
        finra_raw, finra_got = {}, 0
    info(f"FINRA：本輪抓到 {finra_got} 個交易日"
         + (f"（backfill {args.backfill_finra} 日曆天）" if args.backfill_finra else ""))
    try:
        naaim_pts = fetch_naaim()
    except Exception as e:
        warn(f"NAAIM failed: {e}")
        naaim_pts = None
    naaim_raw = {"naaim": naaim_pts} if naaim_pts else {}
    eps_raw = collect_eps_breadth()
    if not eps_raw:
        warn("dd-screener latest.json 讀取失敗或樣本不足——eps_rev_breadth 缺席")

    # merge 全部進 history
    for raw in (cache_raw, yf_raw, fred_raw, td_raw, cboe_raw, finra_raw,
                naaim_raw, eps_raw):
        merge_history(history, raw)

    # 統計
    items = {}
    for key, sp in S.items():
        pts = history.get(key) or []
        st = compute_stats(pts, sp["unit"], sp["freq"])
        if st is None:
            gaps.append({"key": key, "label": sp["label"],
                         "reason": "no data from source"})
            continue
        st["val_fmt"] = fmt_val(st["last"], sp)
        st["chg_fmt"] = fmt_chg(st["chg"], sp["unit"])
        if st["chg"] is None:
            st["dir"] = "neu"
        else:
            up = st["chg"] > 0
            st["dir"] = ("neg" if up else "pos") if sp["invert"] else ("pos" if up else "neg")
        items[key] = st

    if not items or not as_of:
        warn("no series computed — aborting without write")
        return 1

    # stale 標記（落後 as_of 超過頻率門檻 → 不進異常）
    as_of_dt = datetime.strptime(as_of, "%Y-%m-%d")
    for key, it in items.items():
        limit = S[key]["stale_days"] or STALE_DAYS[S[key]["freq"]]
        it["stale"] = (as_of_dt - datetime.strptime(it["date"], "%Y-%m-%d")).days > limit

    # 異常（stale 與 warming_up 皆不進）
    alerts = []
    for key, it in items.items():
        if it["stale"] or it["warming_up"]:
            continue
        alerts.extend(series_alerts_v2(it, S[key]))
    alerts.extend(structural_alerts_v2(items, history))
    tag_event_alerts(alerts, cal_events, as_of)
    alerts.sort(key=lambda a: (a["sev"] != "red", a["cat"]))
    n_warm = sum(1 for it in items.values() if it["warming_up"])
    info(f"as_of {as_of}: {len(items)}/{len(S)} series（warming_up {n_warm}），"
         f"{len(alerts)} alerts（{sum(1 for a in alerts if a['sev'] == 'red')} red），"
         f"gaps {len(gaps)}")
    for a in alerts:
        info(f"  [{a['sev']}] {a['rule']}: {a['msg']}")

    # 組 internals.json（item 欄位協議對齊母版 latest.json，加 warming_up／note）
    categories = []
    for cat_key, cat_label in CATEGORIES_V2:
        rows = []
        for key, sp in S.items():
            if sp["cat"] != cat_key or key not in items:
                continue
            it = items[key]
            rows.append({"key": key, "label": sp["label"], "unit": sp["unit"],
                         "val": it["val_fmt"], "chg": it["chg_fmt"], "dir": it["dir"],
                         "z": it["z"], "pctile": it["pctile"],
                         "p20": it["p20"], "p60": it["p60"],
                         "hi52": it["hi52"], "lo52": it["lo52"],
                         "streak": it["streak"], "spark": it["spark"],
                         "date": it["date"], "stale": it["stale"],
                         "warming_up": it["warming_up"], "note": sp["note"]})
        categories.append({"key": cat_key, "label": cat_label, "items": rows})

    internals = {
        "schema": "monitor-internals-v1",
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rules": RULES_V2,
        "categories": categories,
        "alerts_today": alerts,
        "upcoming_events": upcoming_events(cal_events, as_of),
        "gaps": gaps,
    }

    hist_out = {
        "schema": "monitor-internals-history-v1",
        "series": {k: [[d, v] for d, v in pts] for k, pts in sorted(history.items())},
    }

    log = load_json(ALERTS_PATH, {"schema": "monitor-internals-alerts-v1", "days": {}})
    log["days"][as_of] = alerts
    cutoff = (as_of_dt - timedelta(days=ALERTS_RETENTION_DAYS)).strftime("%Y-%m-%d")
    log["days"] = {d: a for d, a in log["days"].items() if d >= cutoff}

    ch1 = write_json_if_changed(INTERNALS_PATH, internals)
    ch2 = write_json_if_changed(HISTORY_PATH, hist_out)
    ch3 = write_json_if_changed(ALERTS_PATH, log)
    info(f"internals.json {'written' if ch1 else 'unchanged'}; "
         f"internals_history.json {'written' if ch2 else 'unchanged'}; "
         f"internals_alerts.json {'written' if ch3 else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
