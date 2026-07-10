#!/usr/bin/env python3
"""
build_monitor.py — 全資產市場監測（/monitor/）資料層＋異常引擎。

每日美股收盤後由 .github/workflows/monitor-daily.yml 執行：
  1. yfinance 抓 ~70 條市場 series（450d 日線，算一年統計）
  2. FRED CSV 抓利率曲線／信用 OAS／流動性（免 API key）
  3. CNN Fear & Greed
  4. 每條 series 算：現值／日變動／變動 z-score／一年分位／52 週高低／連漲跌
  5. 異常引擎：z-score 閘、水位分位閘、結構事件（曲線翻轉／VIX 期限倒掛／
     股漲信用背離）、Fear & Greed 極端 → 當日 alerts
  6. 寫 docs/monitor/data/latest.json（整頁資料）＋ alerts.json（滾動 60 天留痕）

定位＝描述器（describer）非擇時訊號：所有 flag 都是「這條 series 今天落在
統計異常區」的描述，不是買賣指令。閾值見 RULES 常數（頁面方法論段同步顯示）。

零 churn 協議（同 build_rotation_radar.py）：內容不變即不重寫檔案，
週末／美國假日跑到的舊 bar 產生空 diff、workflow 不 commit。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "docs", "monitor", "data")
LATEST_PATH = os.path.join(OUT_DIR, "latest.json")
ALERTS_PATH = os.path.join(OUT_DIR, "alerts.json")

YF_PERIOD = "450d"      # ≈ 300 個交易日，足夠 252d 統計窗
STAT_WINDOW = 252       # 一年統計窗（交易日）
MIN_OBS = 60            # 統計窗最低樣本數，不足則不出 z/分位
ALERTS_RETENTION_DAYS = 60
STALE_DAYS = 5          # series 最新 bar 落後 as_of 超過此天數 → 標 stale、不進異常

# 異常規則閾值（頁面方法論段同步顯示；改這裡要同步改 docs/monitor/index.html 方法論）
RULES = {
    "z_yellow": 2.0,        # |日變動 z| ≥ 2 → 黃色
    "z_red": 3.0,           # |日變動 z| ≥ 3 → 紅色
    "pctile_hi": 98.0,      # 壓力型 series 水位分位 ≥ 98 → 黃色
    "pctile_lo": 2.0,       # 低水位警示型 series 分位 ≤ 2 → 黃色
    "streak": 5,            # 連漲跌 ≥ 5 日 → 黃色
    "fg_low": 10,           # Fear & Greed ≤ 10 → 黃色（極端恐懼）
    "fg_high": 90,          # Fear & Greed ≥ 90 → 黃色（極端貪婪）
    "div_credit_z": -2.0,   # 股漲但 HYG/LQD z ≤ -2 → 黃色（信用背離）
}


def warn(msg: str) -> None:
    print(f"[monitor][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[monitor] {msg}")


# ───────────────────────────────────────────────────────────────────────────
# Universe 定義
#
# 欄位：
#   label      顯示名（中文全形標點規範）
#   cat        分類 key（CATEGORIES 順序）
#   src        yf / fred / ratio / cnn
#   ticker     yf ticker 或 FRED series id；ratio 為 (分子 key, 分母 key)
#   unit       pct（價格類，日變動 %）/ bps（殖利率與利差，日變動 bps）
#              / abs（指數值，如 NFCI）/ usd_b（十億美元，FRED 流動性）
#   dp         現值顯示小數位
#   prefix     現值前綴（$ / NT$ …）
#   invert     True＝上漲是壞事（VIX、OAS、NFCI …），控制紅綠色
#   pct_alert  "high"/"low"/None — 水位分位異常方向（壓力型 series 才設）
#   lo52_alert True＝52 週新低要進異常（主要股指）
# ───────────────────────────────────────────────────────────────────────────

CATEGORIES = [
    ("alerts", "今日異常"),          # 虛擬分類，前端用
    ("indices", "全球指數"),
    ("sectors", "美股產業"),
    ("factors", "因子與風險胃納"),
    ("rates", "利率／通膨／期限溢價"),
    ("vol", "波動與情緒"),
    ("credit", "信用"),
    ("fx", "外匯"),
    ("commodities", "商品"),
    ("crypto", "加密資產"),
    ("liquidity", "流動性與資金管路（FRED）"),
]

S = {}  # key -> spec


def _d(key, label, cat, src, ticker, unit="pct", dp=2, prefix="", invert=False,
       pct_alert=None, lo52_alert=False, scale=1.0, freq="d"):
    S[key] = {"key": key, "label": label, "cat": cat, "src": src, "ticker": ticker,
              "unit": unit, "dp": dp, "prefix": prefix, "invert": invert,
              "pct_alert": pct_alert, "lo52_alert": lo52_alert,
              "scale": scale, "freq": freq}


# 全球指數
_d("sp500", "S&P 500", "indices", "yf", "^GSPC", lo52_alert=True)
_d("ndx", "Nasdaq 100", "indices", "yf", "^NDX", lo52_alert=True)
_d("djia", "道瓊工業", "indices", "yf", "^DJI", lo52_alert=True)
_d("rut", "Russell 2000", "indices", "yf", "^RUT", lo52_alert=True)
_d("sox", "費城半導體", "indices", "yf", "^SOX", lo52_alert=True)
_d("twii", "台灣加權", "indices", "yf", "^TWII", lo52_alert=True)
_d("n225", "日經 225", "indices", "yf", "^N225", lo52_alert=True)
_d("kospi", "韓國 KOSPI", "indices", "yf", "^KS11")
_d("hsi", "香港恆生", "indices", "yf", "^HSI")
_d("dax", "德國 DAX", "indices", "yf", "^GDAXI")
_d("stoxx", "歐洲 STOXX 50", "indices", "yf", "^STOXX50E")
_d("ftse", "英國 FTSE 100", "indices", "yf", "^FTSE")
_d("vt", "VT 全球股票", "indices", "yf", "VT", prefix="$")
_d("eem", "EEM 新興市場", "indices", "yf", "EEM", prefix="$")

# 美股產業（11 SPDR ＋ XBI）
for sym, zh in [("XLK", "科技"), ("XLF", "金融"), ("XLE", "能源"), ("XLV", "醫療"),
                ("XLI", "工業"), ("XLY", "非必需消費"), ("XLP", "必需消費"),
                ("XLU", "公用事業"), ("XLB", "材料"), ("XLRE", "房地產"),
                ("XLC", "通訊"), ("XBI", "生技")]:
    _d(sym.lower(), f"{sym} {zh}", "sectors", "yf", sym, prefix="$")

# 因子與風險胃納（ratio 系列的異常由自身 z-score 承擔跨資產背離偵測；
# 冷門但關鍵組：道氏運輸背離／區域銀行金絲雀／早週期營建／高 beta 胃納）
_d("mtum", "MTUM 動能", "factors", "yf", "MTUM", prefix="$")
_d("fngs", "FNGS 大型科技", "factors", "yf", "FNGS", prefix="$")
_d("arkk", "ARKK 投機胃納", "factors", "yf", "ARKK", prefix="$")
_d("rsp_spy", "RSP/SPY 等權比", "factors", "ratio", ("rsp_raw", "spy_raw"), dp=4)
_d("iwm_spy", "IWM/SPY 小型股比", "factors", "ratio", ("iwm_raw", "spy_raw"), dp=4)
_d("vtv_vug", "VTV/VUG 價值成長比", "factors", "ratio", ("vtv_raw", "vug_raw"), dp=4)
_d("sox_ndx", "SOX/NDX 半導體比", "factors", "ratio", ("sox", "ndx"), dp=4)
_d("djt_dji", "DJT/DJIA 道氏運輸比", "factors", "ratio", ("djt_raw", "djia"), dp=5,
   pct_alert="low")
_d("kre_xlf", "KRE/XLF 區域銀行比", "factors", "ratio", ("kre_raw", "xlf"), dp=4,
   pct_alert="low")
_d("itb_spy", "ITB/SPY 住宅營建比", "factors", "ratio", ("itb_raw", "spy_raw"), dp=4,
   pct_alert="low")
_d("xly_xlp", "XLY/XLP 消費風險胃納", "factors", "ratio", ("xly", "xlp"), dp=4,
   pct_alert="low")
_d("sphb_splv", "SPHB/SPLV 高低波比", "factors", "ratio", ("sphb_raw", "splv_raw"),
   dp=4, pct_alert="low")

# ratio 用的原始腳（不上表）
for k, t in [("rsp_raw", "RSP"), ("spy_raw", "SPY"), ("iwm_raw", "IWM"),
             ("vtv_raw", "VTV"), ("vug_raw", "VUG"), ("djt_raw", "^DJT"),
             ("kre_raw", "KRE"), ("itb_raw", "ITB"), ("sphb_raw", "SPHB"),
             ("splv_raw", "SPLV")]:
    _d(k, k, "_hidden", "yf", t)

# 利率／通膨／期限溢價（曲線走 FRED 日更，比 ^TNX 家族齊全；落後一個交易日
# 屬預期。冷門但關鍵組：TIPS 實質利率（壓成長股估值的真兇）、5y5y forward
# 通膨（Fed 錨定指標）、ACM 期限溢價（2023/10 與 2025 長端拋售的核心變數））
_d("dgs3mo", "美 3M", "rates", "fred", "DGS3MO", unit="bps")
_d("dgs2", "美 2Y", "rates", "fred", "DGS2", unit="bps")
_d("dgs5", "美 5Y", "rates", "fred", "DGS5", unit="bps")
_d("dgs10", "美 10Y", "rates", "fred", "DGS10", unit="bps")
_d("dgs30", "美 30Y", "rates", "fred", "DGS30", unit="bps")
_d("t10y2y", "10Y−2Y 利差", "rates", "fred", "T10Y2Y", unit="bps")
_d("t10y3m", "10Y−3M 利差", "rates", "fred", "T10Y3M", unit="bps")
_d("real10y", "10Y TIPS 實質利率", "rates", "fred", "DFII10", unit="bps",
   invert=True, pct_alert="high")
_d("bei5y", "5Y 通膨預期", "rates", "fred", "T5YIE", unit="bps", pct_alert="both")
_d("bei5y5y", "5y5y Forward 通膨", "rates", "fred", "T5YIFR", unit="bps",
   pct_alert="both")
_d("tp10y", "10Y 期限溢價（ACM）", "rates", "fred", "THREEFYTP10", unit="bps",
   invert=True, pct_alert="high", freq="w")  # 日頻 series 但 NY Fed 發布有數日 lag
_d("tlt", "TLT 長債 ETF", "rates", "yf", "TLT", prefix="$")

# 波動與情緒
_d("vix", "VIX", "vol", "yf", "^VIX", invert=True, pct_alert="high")
_d("vix9d", "VIX9D", "vol", "yf", "^VIX9D", invert=True, pct_alert="high")
_d("vvix", "VVIX", "vol", "yf", "^VVIX", invert=True, pct_alert="high")
_d("skew", "SKEW", "vol", "yf", "^SKEW", pct_alert="high")
_d("move", "MOVE 債市波動", "vol", "yf", "^MOVE", invert=True, pct_alert="high")
_d("vix_ts", "VIX9D/VIX 期限比", "vol", "ratio", ("vix9d", "vix"), dp=3, invert=True)

# 信用
_d("hyg", "HYG 高收益", "credit", "yf", "HYG", prefix="$")
_d("lqd", "LQD 投資級", "credit", "yf", "LQD", prefix="$")
_d("bkln", "BKLN 槓桿貸款", "credit", "yf", "BKLN", prefix="$")
_d("hyg_lqd", "HYG/LQD 信用比", "credit", "ratio", ("hyg", "lqd"), dp=4, pct_alert="low")
_d("emb", "EMB 新興美元債", "credit", "yf", "EMB", prefix="$")
_d("hy_oas", "HY OAS 高收益利差", "credit", "fred", "BAMLH0A0HYM2", unit="bps",
   invert=True, pct_alert="high")
_d("ig_oas", "IG OAS 投資級利差", "credit", "fred", "BAMLC0A0CM", unit="bps",
   invert=True, pct_alert="high")
# CCC 級 OAS＝信用市場最深處的金絲雀——HY OAS 平靜時 CCC 先走寬是典型前兆
_d("ccc_oas", "CCC OAS 最低評級利差", "credit", "fred", "BAMLH0A3HYC", unit="bps",
   invert=True, pct_alert="high")

# 外匯
_d("dxy", "DXY 美元指數", "fx", "yf", "DX-Y.NYB")
_d("usdjpy", "USD/JPY", "fx", "yf", "JPY=X", dp=2)
_d("usdtwd", "USD/TWD", "fx", "yf", "TWD=X", dp=3)
_d("eurusd", "EUR/USD", "fx", "yf", "EURUSD=X", dp=4)
_d("gbpusd", "GBP/USD", "fx", "yf", "GBPUSD=X", dp=4)
_d("usdcny", "USD/CNY", "fx", "yf", "CNY=X", dp=4)
_d("usdkrw", "USD/KRW", "fx", "yf", "KRW=X", dp=1)
_d("audusd", "AUD/USD", "fx", "yf", "AUD=X", dp=4)

# 商品
_d("wti", "WTI 原油", "commodities", "yf", "CL=F", prefix="$")
_d("brent", "Brent 原油", "commodities", "yf", "BZ=F", prefix="$")
_d("natgas", "天然氣", "commodities", "yf", "NG=F", prefix="$", dp=3)
_d("gold", "黃金", "commodities", "yf", "GC=F", prefix="$")
_d("silver", "白銀", "commodities", "yf", "SI=F", prefix="$")
_d("copper", "銅", "commodities", "yf", "HG=F", prefix="$", dp=4)
_d("alum", "鋁", "commodities", "yf", "ALI=F", prefix="$")
_d("platinum", "鉑金", "commodities", "yf", "PL=F", prefix="$")
_d("palladium", "鈀金", "commodities", "yf", "PA=F", prefix="$")
_d("wheat", "小麥", "commodities", "yf", "ZW=F", prefix="$")
_d("corn", "玉米", "commodities", "yf", "ZC=F", prefix="$")
_d("soybean", "黃豆", "commodities", "yf", "ZS=F", prefix="$")
_d("copper_gold", "銅金比", "commodities", "ratio", ("copper", "gold"), dp=6)
_d("gold_silver", "金銀比", "commodities", "ratio", ("gold", "silver"), dp=2,
   invert=True, pct_alert="high")

# 加密資產
_d("btc", "Bitcoin", "crypto", "yf", "BTC-USD", prefix="$", dp=0)
_d("eth", "Ethereum", "crypto", "yf", "ETH-USD", prefix="$", dp=0)

# 流動性與資金管路（FRED）— dir 慣例沿用早報：RRP↓／TGA↓＝流動性釋放＝pos。
# WTREGEN／WRESBAL／WALCL 原始單位是百萬美元，scale 到十億；RRPONTSYD 是十億。
# 冷門但關鍵組：SOFR−IORB（repo 管路壓力，2019-09 repo 危機的那條線）、
# STLFSI（聖路易 Fed 金融壓力合成）、WALCL（QT 進度）、ICSA（勞動市場金絲雀）。
_d("rrp", "RRP 隔夜逆回購", "liquidity", "fred", "RRPONTSYD", unit="usd_b", invert=True)
_d("tga", "TGA 財政部帳戶", "liquidity", "fred", "WTREGEN", unit="usd_b",
   invert=True, scale=1e-3, freq="w")
_d("reserves", "銀行準備金", "liquidity", "fred", "WRESBAL", unit="usd_b",
   scale=1e-3, freq="w")
_d("nfci", "NFCI 金融條件", "liquidity", "fred", "NFCI", unit="abs", dp=3,
   invert=True, pct_alert="high", freq="w")
_d("sofr_iorb", "SOFR−IORB 資金利差", "liquidity", "spread", ("sofr_raw", "iorb_raw"),
   unit="bps_lvl", invert=True, pct_alert="high")
_d("stlfsi", "STLFSI 金融壓力指數", "liquidity", "fred", "STLFSI4", unit="abs",
   dp=3, invert=True, pct_alert="high", freq="w")
_d("walcl", "Fed 資產負債表", "liquidity", "fred", "WALCL", unit="usd_b",
   scale=1e-3, freq="w")
_d("claims", "初領失業金", "liquidity", "fred", "ICSA", unit="k",
   scale=1e-3, invert=True, pct_alert="high", freq="w")

# spread 用的原始腳（不上表）
_d("sofr_raw", "sofr_raw", "_hidden", "fred", "SOFR", unit="bps")
_d("iorb_raw", "iorb_raw", "_hidden", "fred", "IORB", unit="bps")


# ───────────────────────────────────────────────────────────────────────────
# Zero-churn IO（協議同 build_rotation_radar.py）
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
# 資料抓取
# ───────────────────────────────────────────────────────────────────────────

def fetch_yf(tickers: list[str]) -> dict:
    """回傳 {ticker: [(date_iso, close), ...]}；抓不到的 ticker 缺 key。"""
    import pandas as pd
    import yfinance as yf
    out = {}
    df = yf.download(tickers, period=YF_PERIOD, interval="1d", auto_adjust=True,
                     progress=False, threads=True, group_by="column")
    if df is None or len(df) == 0:
        return out
    close = df["Close"] if isinstance(df.columns, pd.MultiIndex) else df[["Close"]].rename(
        columns={"Close": tickers[0]})
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
            out[str(tk)] = pts
    return out


def fetch_fred(series_id: str) -> list | None:
    """FRED CSV endpoint（免 key），回傳 [(date_iso, val), ...] 或 None。"""
    import requests
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        # 不帶自訂 UA——FRED 會 stall「Mozilla/5.0 …」型偽瀏覽器字串（實測 read
        # timeout），requests 預設 UA 反而正常回應。
        r = requests.get(url, timeout=30)
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
    return pts[-400:] or None


def fetch_fear_greed() -> dict | None:
    import requests
    try:
        r = requests.get(
            "https://production.dataviz.cnn.io/index/fearandgreed/graphdata",
            headers={"User-Agent": "Mozilla/5.0 (compatible; imq-monitor/1.0)"},
            timeout=15)
        r.raise_for_status()
        fg = r.json().get("fear_and_greed", {})
        score = fg.get("score")
        if score is None:
            return None
        return {"score": int(round(float(score))), "rating": fg.get("rating", ""),
                "prev": int(round(float(fg.get("previous_close", 0))))}
    except Exception as e:
        warn(f"Fear & Greed: {e}")
        return None


# ───────────────────────────────────────────────────────────────────────────
# 統計
# ───────────────────────────────────────────────────────────────────────────

def compute_stats(pts: list, unit: str, freq: str = "d") -> dict | None:
    """pts = [(date, val), ...] 升冪。回傳統計 dict；樣本不足回 None。
    統計窗按頻率換算成「一年」：日頻 252 筆、週頻 52 筆。"""
    if not pts or len(pts) < 2:
        return None
    win = STAT_WINDOW if freq == "d" else 52
    min_obs = MIN_OBS if freq == "d" else 30
    vals = [v for _, v in pts]
    dates = [d for d, _ in pts]
    last, prev = vals[-1], vals[-2]

    # 日變動：pct 類用報酬率，bps/abs/usd_b 類用差值
    if unit == "pct":
        changes = [(vals[i] - vals[i - 1]) / vals[i - 1] * 100
                   for i in range(1, len(vals)) if vals[i - 1] != 0]
        chg = (last - prev) / prev * 100 if prev else None
    else:
        changes = [vals[i] - vals[i - 1] for i in range(1, len(vals))]
        chg = last - prev

    # z-score：今日變動 vs 過去一年變動分布（不含今日）
    z = None
    base = changes[-(win + 1):-1]
    if chg is not None and len(base) >= min_obs:
        mean = sum(base) / len(base)
        var = sum((c - mean) ** 2 for c in base) / len(base)
        std = var ** 0.5
        if std > 1e-12:
            z = round((changes[-1] - mean) / std, 2)

    # 一年水位分位／52 週高低
    window = vals[-win:]
    pctile = hi52 = lo52 = None
    if len(window) >= min_obs:
        pctile = round(sum(1 for v in window if v <= last) / len(window) * 100, 1)
        eps = abs(last) * 1e-9
        hi52 = last >= max(window) - eps
        lo52 = last <= min(window) + eps

    # 連漲跌（同號連續日數；正數＝連漲）
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
            "hi52": hi52, "lo52": lo52, "streak": streak,
            "spark": spark, "date": dates[-1]}


def fmt_val(v, spec) -> str:
    if v is None:
        return "—"
    u = spec["unit"]
    if u == "bps":
        return f"{v:.2f}%"
    if u == "bps_lvl":
        return f"{v * 100:.0f}bps"
    if u == "usd_b":
        return f"${v:,.0f}B"
    if u == "k":
        return f"{v:,.0f}K"
    return f"{spec['prefix']}{v:,.{spec['dp']}f}"


def fmt_chg(chg, unit, dp=2) -> str:
    if chg is None:
        return "—"
    arrow = "▲" if chg > 0 else ("▼" if chg < 0 else "＝")
    if unit == "pct":
        return f"{arrow} {abs(chg):.2f}%"
    if unit in ("bps", "bps_lvl"):
        return f"{arrow} {abs(chg) * 100:.0f}bps"
    if unit == "usd_b":
        return f"{arrow} {abs(chg):.0f}B"
    if unit == "k":
        return f"{arrow} {abs(chg):.0f}K"
    return f"{arrow} {abs(chg):.3f}"


# ───────────────────────────────────────────────────────────────────────────
# 異常引擎
# ───────────────────────────────────────────────────────────────────────────

def series_alerts(item: dict, spec: dict) -> list[dict]:
    """單一 series 的規則：z 閘／水位分位閘／52 週新低／連漲跌。"""
    out = []
    key, label, cat = spec["key"], spec["label"], spec["cat"]
    z, pctile = item.get("z"), item.get("pctile")

    if z is not None and abs(z) >= RULES["z_yellow"]:
        sev = "red" if abs(z) >= RULES["z_red"] else "yellow"
        period = "單日" if spec["freq"] == "d" else "單期"
        vol = "日波動" if spec["freq"] == "d" else "週波動"
        out.append({"sev": sev, "cat": cat, "key": key, "rule": "move_z",
                    "msg": f"{label} {period}{'漲' if item['chg'] > 0 else '跌'}"
                           f"幅 {item['chg_fmt']}，為一年{vol}的 {abs(z):.2f} 倍標準差"})
    pa = spec["pct_alert"]
    if pctile is not None and pa in ("high", "both") and pctile >= RULES["pctile_hi"]:
        out.append({"sev": "yellow", "cat": cat, "key": key, "rule": "pctile",
                    "msg": f"{label} 現值 {item['val_fmt']} 進入一年水位前 "
                           f"{100 - pctile:.0f}%（分位 {pctile:.0f}）"})
    if pctile is not None and pa in ("low", "both") and pctile <= RULES["pctile_lo"]:
        out.append({"sev": "yellow", "cat": cat, "key": key, "rule": "pctile",
                    "msg": f"{label} 現值 {item['val_fmt']} 落到一年水位後 "
                           f"{pctile:.0f}%（低分位警示）"})
    if spec["lo52_alert"] and item.get("lo52"):
        out.append({"sev": "red", "cat": cat, "key": key, "rule": "lo52",
                    "msg": f"{label} 觸及 52 週新低（{item['val_fmt']}）"})
    st = item.get("streak") or 0
    if abs(st) >= RULES["streak"] and spec["freq"] == "d":
        out.append({"sev": "yellow", "cat": cat, "key": key, "rule": "streak",
                    "msg": f"{label} 連續 {abs(st)} 日{'上漲' if st > 0 else '下跌'}"})
    return out


def structural_alerts(items: dict, fear_greed: dict | None) -> tuple[list[dict], dict]:
    """跨 series 結構規則。回傳 (alerts, status)。"""
    alerts = []
    status = {}

    # 1) 殖利率曲線翻轉（10Y−2Y 正負號 vs 前一日）
    t = items.get("t10y2y")
    if t and t.get("last") is not None and t.get("chg") is not None:
        prev = t["last"] - t["chg"]
        status["curve_10y2y"] = {"val": round(t["last"], 2),
                                 "state": "inverted" if t["last"] < 0 else "normal"}
        if (t["last"] < 0) != (prev < 0):
            alerts.append({"sev": "red", "cat": "rates", "key": "t10y2y", "rule": "curve_flip",
                           "msg": f"10Y−2Y 利差正負翻轉：{prev:+.2f}% → {t['last']:+.2f}%"})

    # 2) VIX 期限結構（VIX9D > VIX ＝倒掛＝短期恐慌訂價高於中期）
    ts = items.get("vix_ts")
    if ts and ts.get("last") is not None:
        inverted = ts["last"] > 1.0
        status["vix_term"] = {"val": round(ts["last"], 3),
                              "state": "backwardation" if inverted else "contango"}
        if inverted:
            prev_ratio = None
            if ts.get("chg") is not None:
                prev_ratio = ts["last"] / (1 + ts["chg"] / 100)
            newly = prev_ratio is not None and prev_ratio <= 1.0
            alerts.append({"sev": "red" if newly else "yellow", "cat": "vol",
                           "key": "vix_ts", "rule": "vix_inversion",
                           "msg": f"VIX 期限結構倒掛{'（今日新轉倒掛）' if newly else '中'}："
                                  f"VIX9D/VIX = {ts['last']:.3f} > 1"})

    # 3) 股漲信用背離：S&P 500 上漲但 HYG/LQD 大幅走弱
    spx, hl = items.get("sp500"), items.get("hyg_lqd")
    if (spx and hl and spx.get("chg") is not None and hl.get("z") is not None
            and spx["chg"] > 0 and hl["z"] <= RULES["div_credit_z"]):
        alerts.append({"sev": "yellow", "cat": "credit", "key": "hyg_lqd", "rule": "divergence",
                       "msg": f"股漲信用背離：S&P 500 {spx['chg_fmt']} 上漲，"
                              f"但 HYG/LQD 信用比 z = {hl['z']:.1f} 大幅走弱"})

    # 4) Fear & Greed 極端
    if fear_greed:
        sc = fear_greed["score"]
        if sc <= RULES["fg_low"] or sc >= RULES["fg_high"]:
            side = "極端恐懼" if sc <= RULES["fg_low"] else "極端貪婪"
            alerts.append({"sev": "yellow", "cat": "vol", "key": "fear_greed",
                           "rule": "fg_extreme",
                           "msg": f"CNN Fear & Greed 進入{side}區：{sc}"})

    # 5) 流動性四訊號合成（沿用早報 assess_liquidity 慣例）
    score = 0
    for k, good_dir in [("rrp", "down"), ("tga", "down"), ("reserves", "up"), ("nfci", "down")]:
        it = items.get(k)
        if not it or it.get("chg") is None:
            continue
        up = it["chg"] > 0
        score += 1 if (up and good_dir == "up") or (not up and good_dir == "down") else -1
    status["liquidity"] = {"score": score,
                           "label": "流動性寬鬆" if score >= 2 else
                                    ("流動性收縮" if score <= -2 else "流動性中性")}
    return alerts, status


# ───────────────────────────────────────────────────────────────────────────
# main
# ───────────────────────────────────────────────────────────────────────────

def main() -> int:
    yf_tickers = sorted({sp["ticker"] for sp in S.values() if sp["src"] == "yf"})
    info(f"fetching {len(yf_tickers)} yfinance tickers …")
    yf_data = fetch_yf(yf_tickers)
    missing_yf = [t for t in yf_tickers if t not in yf_data]
    if missing_yf:
        warn(f"yfinance missing: {', '.join(missing_yf)}")

    fred_data = {}
    for sp in S.values():
        if sp["src"] == "fred":
            pts = fetch_fred(sp["ticker"])
            if pts:
                fred_data[sp["ticker"]] = pts
    info(f"FRED ok: {len(fred_data)} series")

    fear_greed = fetch_fear_greed()

    # 原始點位 → per-series 統計
    raw = {}
    for key, sp in S.items():
        if sp["src"] == "yf":
            raw[key] = yf_data.get(sp["ticker"])
        elif sp["src"] == "fred":
            pts = fred_data.get(sp["ticker"])
            if pts and sp["scale"] != 1.0:
                pts = [(d, v * sp["scale"]) for d, v in pts]
            raw[key] = pts
    for key, sp in S.items():
        if sp["src"] in ("ratio", "spread"):
            nk, dk = sp["ticker"]
            a, b = raw.get(nk), raw.get(dk)
            if not a or not b:
                raw[key] = None
                continue
            bm = dict(b)
            if sp["src"] == "ratio":
                raw[key] = [(d, round(v / bm[d], 8)) for d, v in a if d in bm and bm[d]]
            else:
                raw[key] = [(d, round(v - bm[d], 8)) for d, v in a if d in bm]

    items, gaps = {}, []
    for key, sp in S.items():
        st = compute_stats(raw.get(key) or [], sp["unit"], sp["freq"])
        if st is None:
            if sp["cat"] != "_hidden":
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

    if "sp500" not in items:
        warn("no S&P 500 data — aborting without write")
        return 1
    as_of = items["sp500"]["date"]

    # stale 標記（落後 as_of 太多的 series 不進異常；週頻 series 門檻放寬）
    as_of_dt = datetime.strptime(as_of, "%Y-%m-%d")
    for key, it in items.items():
        limit = STALE_DAYS if S[key]["freq"] == "d" else 12
        it["stale"] = (as_of_dt - datetime.strptime(it["date"], "%Y-%m-%d")).days > limit

    # 異常
    alerts = []
    for key, it in items.items():
        sp = S[key]
        if sp["cat"] == "_hidden" or it["stale"]:
            continue
        alerts.extend(series_alerts(it, sp))
    st_alerts, status = structural_alerts(items, fear_greed)
    alerts.extend(st_alerts)
    alerts.sort(key=lambda a: (a["sev"] != "red", a["cat"]))
    info(f"as_of {as_of}: {len(alerts)} alerts "
         f"({sum(1 for a in alerts if a['sev'] == 'red')} red)")

    # 組 latest.json
    categories = []
    for cat_key, cat_label in CATEGORIES:
        if cat_key == "alerts":
            continue
        rows = []
        for key, sp in S.items():
            if sp["cat"] != cat_key or key not in items:
                continue
            it = items[key]
            rows.append({"key": key, "label": sp["label"], "unit": sp["unit"],
                         "val": it["val_fmt"], "chg": it["chg_fmt"], "dir": it["dir"],
                         "z": it["z"], "pctile": it["pctile"],
                         "hi52": it["hi52"], "lo52": it["lo52"],
                         "streak": it["streak"], "spark": it["spark"],
                         "date": it["date"], "stale": it["stale"]})
        categories.append({"key": cat_key, "label": cat_label, "items": rows})

    latest = {
        "schema": "monitor-v1",
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rules": RULES,
        "categories": categories,
        "alerts_today": alerts,
        "status": status,
        "fear_greed": fear_greed,
        "gaps": gaps,
    }

    # 滾動 60 天異常留痕（同日重跑覆蓋當日 entry，idempotent）
    log = load_json(ALERTS_PATH, {"schema": "monitor-alerts-v1", "days": {}})
    log["days"][as_of] = alerts
    cutoff = (as_of_dt - timedelta(days=ALERTS_RETENTION_DAYS)).strftime("%Y-%m-%d")
    log["days"] = {d: a for d, a in log["days"].items() if d >= cutoff}

    ch1 = write_json_if_changed(LATEST_PATH, latest)
    ch2 = write_json_if_changed(ALERTS_PATH, log)
    info(f"latest.json {'written' if ch1 else 'unchanged'}; "
         f"alerts.json {'written' if ch2 else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
