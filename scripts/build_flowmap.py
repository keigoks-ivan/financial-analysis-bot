#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conditional Flow Map（條件流量地圖）— Phase 1 daily data pipeline.

回答「未來 1–10 個交易日，機械型參與者（CTA／vol-control／庫藏股）在什麼價格
與波動條件下，會被迫買或賣、量級多少」——不預測指數方向、不出買賣指令、不落
任何聚合名單。設計依據：notes/site-internal/root/_flowmap_forecast_ledger_design_20260901.md
§A（判斷已在設計稿凍結：模型選型／窗長／門檻／AUM 錨／kill conditions 一律不得
自行調整，改動需回設計稿另過校準）。

三個 Phase 1 模組
-----------------
  CTA 趨勢觸發位   ：SPX／NDX／RTY（以 SPY／QQQ／IWM 為代理）各算 20／60／120 交易
                     日動能，反解翻多／翻空的價格位（flip_level）與距現價 %。
  Vol-control 曝險 ：SPY 日報酬算 21d／63d 年化已實現波動，目標波動曝險模型
                     （target_vol=10%、cap=100%）換算隱含曝險 %，並給 RV 階梯表。
  庫藏股靜默期日曆 ：S&P 市值前 100 檔（CONFIG 硬表）下次財報日 → 財報前 35 曆日
                     至財報後 1 曆日視為 blackout，算未來 8 週等權覆蓋率。

Phase 2（dealer gamma）本檔不做——資料源不足，一律進 gaps 不捏造。

Phase 1.5（2026-09-01 持有人核准增補，設計依據同檔 §E1／§E2）
-----------------------------------------------------------
  槓桿ETF每日再平衡（模組 4）：SPX／NDX／SOX 三複合體 CONFIG 硬表，尾盤再平衡
                     名目 =（L²−L）× AUM × 當日標的報酬；AUM 走 yfinance
                     totalAssets（獨立快取，7 天內不重抓）。confidence: med。
  月末／季末再平衡壓力（模組 5）：分岔 = SPY MTD 報酬 − AGG MTD 報酬，量級桶為
                     外部研究粗錨，confidence: lo。生效窗＝當月最後 3 個交易日。
  兩模組函式獨立、latest.json 各占獨立 key（lev_etf／month_end），拆除互不影響。

輸出
----
  data/flowmap_prices.json          — SPY/QQQ/IWM/AGG 日線 close，rolling ~500 個
                                       交易日（yfinance -> stooq fallback，incremental）。
  data/flowmap_earnings_cache.json  — 100 檔次次財報日快取（7 天內不重抓）。
  data/flowmap_etf_aum_cache.json   — 槓桿／反向 ETF 複合體 AUM 快取（7 天內不重抓；
                                       單檔失敗沿用上次快取值並標 stale）。
  docs/flowmap/data/latest.json     — 契約 JSON（schema="flowmap-v1.1"）。
  docs/flowmap/data/forecast_history.jsonl
                                     — 每日凍結預測逐行 append（同日重跑覆蓋當日
                                       那行，不重複 append）。

CLI
---
  python scripts/build_flowmap.py                 完整每日刷新（預設）
  python scripts/build_flowmap.py --skip-fetch     離線：只用既有快取重算

Design contracts（比照 build_regime.py / build_crowding.py）
--------------------------------------------------------------
  * Zero churn：latest.json 與價格/財報快取皆先比對現值再寫，內容不變則不落盤
    （易變欄位 generated_at/built_at/fetched_at 比對前先剝除）。
  * Fault tolerance：CTA／vol-control／buyback 三模組互相獨立、warn-and-continue；
    任一模組資料不足就整模組輸出 null 並記錄到 gaps，不用舊值或估值填充。
  * PREREG 凍結：CONFIG 區的窗長／門檻／AUM 錨數字皆為設計稿凍結值，不得依單一
    案例調參（見設計稿 §A6）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PRICE_CACHE = os.path.join(DATA, "flowmap_prices.json")
EARNINGS_CACHE = os.path.join(DATA, "flowmap_earnings_cache.json")
LEV_ETF_AUM_CACHE = os.path.join(DATA, "flowmap_etf_aum_cache.json")
OUT_DIR = os.path.join(ROOT, "docs", "flowmap", "data")
OUT_JSON = os.path.join(OUT_DIR, "latest.json")
FORECAST_HISTORY = os.path.join(OUT_DIR, "forecast_history.jsonl")

SCHEMA = "flowmap-v1.1"


def warn(msg: str) -> None:
    print(f"[flowmap][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[flowmap] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（設計稿 §A2／§A6）。不得因單一案例調參。
# ═══════════════════════════════════════════════════════════════════════════

# ── 價格快取 ──
FLOWMAP_SYMBOLS = ["SPY", "QQQ", "IWM", "AGG"]  # AGG：模組 5 月末再平衡需股債分岔
ROLLING_TRADING_DAYS = 520  # ~500 個交易日 + 緩衝

# ── 模組 1：CTA 趨勢觸發位 ──
CTA_WINDOWS = [20, 60, 120]
# (yfinance symbol, 顯示市場代號, 全翻轉時預估名目流量區間 $bn — 外部研究粗錨，
#  lo 信心，非本檔機械計算；設計稿 §A2 明文「掛 lo 信心」)
CTA_MARKETS = [
    ("SPY", "SPX", [20, 40]),
    ("QQQ", "NDX", [8, 15]),
    ("IWM", "RTY", [3, 8]),
]
CTA_FLOW_NOTE = "外部研究粗錨（CTA 趨勢跟隨資金規模量級），非機械計算，lo 信心"

# ── 模組 2：Vol-control 曝險 ──
VOL_TARGET = 0.10          # target_vol = 10%
VOL_CAP = 1.00              # 曝險上限 100%
VOL_AUM_USD_BN = 250.0      # AUM 錨 ~$250bn，外部研究值，lo 信心
VOL_LADDER_STEP_PTS = 2.0   # 階梯：RV 每 +2 vol 點一階
VOL_LADDER_RUNGS = 4
VOL_SHOCK_PCT = 0.02        # 假想「明日 ±2% 日」情境

# ── 模組 3：庫藏股靜默期日曆 ──
BUYBACK_BLACKOUT_BEFORE_DAYS = 35  # 財報前 35 曆日起
BUYBACK_BLACKOUT_AFTER_DAYS = 1    # 財報後 1 曆日止
BUYBACK_WEEKS_AHEAD = 8
BUYBACK_CACHE_MAX_AGE_DAYS = 7
BUYBACK_MIN_COVERAGE_FRAC = 0.5  # 抓不到 >= 一半名單就整模組輸出 null

# S&P 500 市值前 100（約，寫死名單，來源＝知識中的當前大市值成分，非即時排序）
SP100_TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "AVGO", "BRK-B", "TSLA", "LLY",
    "JPM", "V", "XOM", "UNH", "MA", "COST", "HD", "PG", "JNJ", "NFLX",
    "ABBV", "CRM", "BAC", "KO", "ORCL", "MRK", "CVX", "AMD", "PEP", "TMO",
    "WMT", "ADBE", "LIN", "ACN", "MCD", "CSCO", "ABT", "DIS", "WFC", "TXN",
    "DHR", "PM", "GE", "INTU", "NOW", "IBM", "CAT", "VZ", "AMAT", "QCOM",
    "CMCSA", "UBER", "SPGI", "UNP", "AXP", "LOW", "T", "BKNG", "PFE", "NEE",
    "ISRG", "HON", "AMGN", "RTX", "ETN", "GS", "LMT", "SYK", "PLD", "MS",
    "ELV", "BLK", "TJX", "MDT", "DE", "ADI", "VRTX", "C", "BA", "SBUX",
    "MU", "GILD", "BX", "ADP", "LRCX", "PANW", "REGN", "SCHW", "MMC", "KLAC",
    "CB", "PGR", "SO", "ZTS", "CI", "BSX", "FI", "MO", "DUK", "CME",
]

# ── 模組 4：槓桿 ETF 每日再平衡（設計稿 §E1，PREREG 凍結，逐字照抄不得調整）──
# 係數 = L² − L（L 含正負）：+2x→2／−2x→6／+3x→6／−3x→12。
LEV_ETF_AUM_MAX_AGE_DAYS = 7
LEV_ETF_SHOCK_PCTS = [-3, -2, -1, 1, 2, 3]
LEV_ETF_CONFIDENCE = "med"
LEV_ETF_COMPLEXES = [
    {
        "complex": "SPX",
        # SPX 複合體標的報酬直接讀既有價格快取的 SPY（非槓桿代理）。
        "underlying_proxy": "SPY",
        "legs": [
            ("SSO", 2), ("UPRO", 3), ("SPXL", 3),
            ("SDS", -2), ("SPXU", -3), ("SPXS", -3),
        ],
    },
    {
        "complex": "NDX",
        "underlying_proxy": "QQQ",
        "legs": [("QLD", 2), ("TQQQ", 3), ("QID", -2), ("SQQQ", -3)],
    },
    {
        "complex": "SOX",
        # 半導體複合體在既有價格快取（SPY/QQQ/IWM/AGG）中無現成非槓桿代理；
        # 設計稿未另外指定新增指數代理，改用 SOXL（失敗則 SOXS）自身當日報酬
        # ÷ 槓桿反推標的報酬——屬本檔的實作選擇，非設計稿逐字條文，供持有人複審。
        "underlying_proxy": None,
        "legs": [("SOXL", 3), ("SOXS", -3)],
    },
]


def _lev_coef(lev: int) -> int:
    return lev * lev - lev


def _all_lev_etf_tickers():
    out = []
    for cx in LEV_ETF_COMPLEXES:
        for t, _ in cx["legs"]:
            out.append(t)
    return out


# ── 模組 5：月末／季末再平衡壓力（設計稿 §E2，PREREG 凍結）──
MONTH_END_WINDOW_DAYS = 3
MONTH_END_CONFIDENCE = "lo"
QUARTER_END_MONTHS = {3, 6, 9, 12}
QUARTER_END_NOTE = "本月為季末月，疊加季度再平衡，量級傾向桶內偏上緣"


# ═══════════════════════════════════════════════════════════════════════════
# Zero-churn IO（同 build_regime.py / build_crowding.py 協議）
# ═══════════════════════════════════════════════════════════════════════════

def _serialize(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


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


def write_json_if_changed(path, obj, volatile=("generated_at", "built_at", "fetched_at")) -> bool:
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


def rnd(v, d):
    if v is None:
        return None
    try:
        return round(float(v), d)
    except (TypeError, ValueError):
        return None


def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0 flowmap"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 flowmap"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


# ═══════════════════════════════════════════════════════════════════════════
# 價格快取（daily close, yfinance -> stooq fallback, incremental）
# ═══════════════════════════════════════════════════════════════════════════

def _yf_daily(tickers, period="2y"):
    """Batch daily close download -> {ticker: [(date, close), ...]}."""
    import yfinance as yf
    out = {}
    if not tickers:
        return out
    df = yf.download(tickers, period=period, interval="1d", auto_adjust=True,
                     group_by="ticker", threads=True, progress=False)
    # yfinance 回傳 MultiIndex 欄位（Ticker, Price）不論單檔或多檔（實測 1.2.0），
    # 用欄位層數判斷而非 ticker 數，修正單檔 bootstrap（如新增 AGG）誤判為扁平欄位。
    is_multi = hasattr(df.columns, "nlevels") and df.columns.nlevels > 1
    for tk in tickers:
        try:
            sub = df[tk] if is_multi else df
            close = sub["Close"]
            rows = []
            for idx, val in close.items():
                try:
                    c = float(val)
                except (TypeError, ValueError):
                    continue
                if c != c:  # NaN
                    continue
                rows.append((idx.date().isoformat(), round(c, 4)))
            if rows:
                out[tk] = rows
        except (KeyError, AttributeError, ValueError, TypeError):
            continue
    return out


def _stooq_daily(ticker):
    sym = ticker.lower()
    if "." not in sym:
        sym = sym + ".us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
    try:
        raw = _http_get(url, timeout=30).decode("utf-8", "replace")
    except Exception:
        return None
    lines = raw.strip().splitlines()
    if len(lines) < 2 or not lines[0].lower().startswith("date"):
        return None
    rows = []
    for ln in lines[1:]:
        parts = ln.split(",")
        if len(parts) < 5:
            continue
        try:
            rows.append((parts[0], round(float(parts[4]), 4)))
        except ValueError:
            continue
    return rows or None


def build_price_cache(skip_fetch):
    """Incrementally refresh data/flowmap_prices.json.  Returns
    {symbol: [(date, close), ...]} (possibly from cache alone)."""
    cache = load_json(PRICE_CACHE, {"meta": {}, "series": {}})
    series = cache.setdefault("series", {})
    fetched = {}
    if not skip_fetch:
        try:
            import yfinance  # noqa: F401
        except ImportError:
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", "-q",
                             "yfinance>=0.2.40", "pandas"])
        missing = [t for t in FLOWMAP_SYMBOLS if not series.get(t)]
        existing = [t for t in FLOWMAP_SYMBOLS if series.get(t)]
        for label, batch, period in (("bootstrap", missing, "2y"),
                                     ("topup", existing, "10d")):
            if not batch:
                continue
            got = None
            for attempt in range(3):
                try:
                    got = _yf_daily(batch, period=period)
                    if got:
                        break
                except Exception as e:
                    warn(f"yfinance {label} attempt {attempt+1} failed: {e}")
            if got:
                fetched.update(got)
            info(f"prices {label}: requested {len(batch)}, got "
                 f"{sum(1 for t in batch if t in fetched)}")
        for t in FLOWMAP_SYMBOLS:
            if t in fetched or series.get(t):
                continue
            s = _stooq_daily(t)
            if s:
                fetched[t] = s
                info(f"prices stooq fallback: {t} ({len(s)} days)")

    for t, rows in fetched.items():
        merged = {d: c for d, c in series.get(t, [])}
        for d, c in rows:
            merged[d] = c
        merged_sorted = sorted(merged.items())
        if len(merged_sorted) > ROLLING_TRADING_DAYS:
            merged_sorted = merged_sorted[-ROLLING_TRADING_DAYS:]
        series[t] = merged_sorted

    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "symbols": FLOWMAP_SYMBOLS,
        "note": "daily close cache for flowmap CTA / vol-control modules "
                "(SPY/QQQ/IWM as SPX/NDX/RTY proxies); yfinance->stooq "
                "fallback; incremental, rolling ~500 trading days.",
    }
    wrote = write_json_if_changed(PRICE_CACHE, cache)
    n = {t: len(series.get(t, [])) for t in FLOWMAP_SYMBOLS}
    info(f"price cache: {n}, {'written' if wrote else 'no change'}")
    return {t: [(d, c) for d, c in series.get(t, [])] for t in FLOWMAP_SYMBOLS}


# ═══════════════════════════════════════════════════════════════════════════
# 模組 1：CTA 趨勢觸發位
# ═══════════════════════════════════════════════════════════════════════════

def cta_module(price_series, gaps):
    out = []
    need = max(CTA_WINDOWS) + 1
    for symbol, label, flow_range in CTA_MARKETS:
        pts = price_series.get(symbol) or []
        if len(pts) < need:
            gaps.append(f"CTA {label}（{symbol}）：價格歷史僅 {len(pts)} 筆，"
                        f"不足 {need} 筆，模組跳過")
            continue
        dates = [d for d, _ in pts]
        closes = [c for _, c in pts]
        cur_date, cur_close = dates[-1], closes[-1]
        windows_out = []
        pos_count = 0
        for w in CTA_WINDOWS:
            flip_level = closes[-1 - w]
            if flip_level == 0:
                continue
            signal = 1 if cur_close > flip_level else (-1 if cur_close < flip_level else 0)
            if signal > 0:
                pos_count += 1
            dist_pct = rnd((cur_close - flip_level) / flip_level * 100, 2)
            windows_out.append({
                "len": w, "signal": signal,
                "flip_level": rnd(flip_level, 2), "dist_pct": dist_pct,
            })
        if not windows_out:
            gaps.append(f"CTA {label}（{symbol}）：無有效窗口，模組跳過")
            continue
        out.append({
            "market": label,
            "proxy": symbol,
            "as_of": cur_date,
            "windows": windows_out,
            "composite_signal": f"+{pos_count}/{len(windows_out)}",
            "est_flow_on_full_flip_usd_bn": list(flow_range),
            "est_flow_note": CTA_FLOW_NOTE,
            "confidence": "lo",
        })
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 模組 2：Vol-control 曝險
# ═══════════════════════════════════════════════════════════════════════════

def _annualized_std(rets):
    n = len(rets)
    if n < 2:
        return None
    mean = sum(rets) / n
    var = sum((r - mean) ** 2 for r in rets) / (n - 1)
    return (var ** 0.5) * (252 ** 0.5)


def _exposure_for_rv(rv):
    if rv is None or rv <= 0:
        return VOL_CAP
    return min(VOL_CAP, VOL_TARGET / rv)


def vol_control_module(price_series, gaps):
    pts = price_series.get("SPY") or []
    if len(pts) < 64:
        gaps.append(f"vol-control：SPY 價格歷史僅 {len(pts)} 筆，不足 64 筆，模組跳過")
        return None
    dates = [d for d, _ in pts]
    closes = [c for _, c in pts]
    rets = [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes)) if closes[i - 1]]
    if len(rets) < 63:
        gaps.append("vol-control：日報酬序列不足 63 筆，模組跳過")
        return None

    rv21 = _annualized_std(rets[-21:])
    rv63 = _annualized_std(rets[-63:])
    if rv21 is None or rv63 is None:
        gaps.append("vol-control：RV21/RV63 計算失敗，模組跳過")
        return None

    cur_rv = max(rv21, rv63)
    implied_exposure = _exposure_for_rv(cur_rv)
    implied_exposure_pct = rnd(implied_exposure * 100, 1)

    base_rv_pct = cur_rv * 100
    ladder = []
    for i in range(1, VOL_LADDER_RUNGS + 1):
        rv_rung_pct = base_rv_pct + i * VOL_LADDER_STEP_PTS
        exp_rung = _exposure_for_rv(rv_rung_pct / 100)
        exp_rung_pct = rnd(exp_rung * 100, 1)
        flow_bn = rnd((exp_rung - implied_exposure) * VOL_AUM_USD_BN, 1)
        ladder.append({
            "rv": rnd(rv_rung_pct, 1),
            "exposure_pct": exp_rung_pct,
            "flow_usd_bn": flow_bn,
        })

    def scenario(shock):
        new_window = rets[-20:] + [shock]  # 丟最舊一天、補一天假想報酬
        new_rv21 = _annualized_std(new_window)
        new_rv = max(new_rv21, rv63) if new_rv21 is not None else cur_rv
        new_exposure = _exposure_for_rv(new_rv)
        new_exposure_pct = rnd(new_exposure * 100, 1)
        if new_exposure_pct is None or implied_exposure_pct is None:
            direction = None
        elif new_exposure_pct > implied_exposure_pct + 0.05:
            direction = "up"
        elif new_exposure_pct < implied_exposure_pct - 0.05:
            direction = "down"
        else:
            direction = "flat"
        return {
            "rv21_new_pct": rnd(new_rv21 * 100, 2) if new_rv21 is not None else None,
            "implied_exposure_pct_new": new_exposure_pct,
            "exposure_change_dir": direction,
        }

    return {
        "as_of": dates[-1],
        "rv_1m": rnd(rv21 * 100, 2),
        "rv_3m": rnd(rv63 * 100, 2),
        "implied_exposure_pct": implied_exposure_pct,
        "ladder": ladder,
        "next_day_scenario": {
            "plus_2pct": scenario(VOL_SHOCK_PCT),
            "minus_2pct": scenario(-VOL_SHOCK_PCT),
        },
        "aum_usd_bn": VOL_AUM_USD_BN,
        "confidence": "lo",
    }


# ═══════════════════════════════════════════════════════════════════════════
# 模組 3：庫藏股靜默期日曆
# ═══════════════════════════════════════════════════════════════════════════

def _fetch_next_earnings_date(ticker):
    """單檔下次財報日，失敗回傳 None（呼叫端須 warn-and-continue）。"""
    import yfinance as yf
    c = yf.Ticker(ticker).calendar
    raw = None
    if isinstance(c, dict):
        raw = c.get("Earnings Date")
    elif c is not None and hasattr(c, "loc"):
        try:
            raw = list(c.loc["Earnings Date"])
        except Exception:
            raw = None
    d0 = raw[0] if isinstance(raw, (list, tuple)) and raw else raw
    if d0 is None:
        return None
    if isinstance(d0, datetime):
        return d0.date().isoformat()
    if isinstance(d0, date):
        return d0.isoformat()
    try:
        import pandas as pd
        return pd.Timestamp(d0).date().isoformat()
    except Exception:
        return None


def refresh_earnings_cache(skip_fetch):
    """回傳 (cache_dict, known_dates: {ticker: date}, fetched_n, failed_n)。"""
    cache = load_json(EARNINGS_CACHE, {"meta": {}, "tickers": {}})
    entries = cache.setdefault("tickers", {})
    now = datetime.now(timezone.utc)
    fetched_n = 0
    failed_n = 0
    skipped_n = 0

    if not skip_fetch:
        try:
            import yfinance  # noqa: F401
        except ImportError:
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", "-q",
                             "yfinance>=0.2.40", "pandas"])
        for t in SP100_TICKERS:
            e = entries.get(t)
            fresh = False
            if e and e.get("fetched_at"):
                try:
                    fetched_dt = datetime.strptime(e["fetched_at"], "%Y-%m-%dT%H:%M:%SZ")
                    fetched_dt = fetched_dt.replace(tzinfo=timezone.utc)
                    age_days = (now - fetched_dt).total_seconds() / 86400.0
                    fresh = age_days < BUYBACK_CACHE_MAX_AGE_DAYS
                except Exception:
                    fresh = False
            if fresh:
                skipped_n += 1
                continue
            try:
                iso = _fetch_next_earnings_date(t)
                entries[t] = {
                    "next_earnings_date": iso,
                    "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
                if iso:
                    fetched_n += 1
                else:
                    failed_n += 1
            except Exception as exc:
                failed_n += 1
                warn(f"earnings calendar fetch failed for {t}: {str(exc)[:80]}")
                # 單檔失敗跳過，保留舊快取（若有），不覆寫成 null
                if t not in entries:
                    entries[t] = {"next_earnings_date": None,
                                  "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ")}
            time.sleep(0.15)

    cache["meta"] = {
        "built_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "universe_n": len(SP100_TICKERS),
        "cache_max_age_days": BUYBACK_CACHE_MAX_AGE_DAYS,
        "note": "S&P 500 市值前 100 檔次次財報日快取（yfinance .calendar），"
                "7 天內不重抓；單檔失敗跳過不 abort。",
    }
    write_json_if_changed(EARNINGS_CACHE, cache)
    info(f"earnings cache: fetched={fetched_n} skipped_fresh={skipped_n} failed={failed_n}")

    known = {}
    for t in SP100_TICKERS:
        e = entries.get(t)
        if not e or not e.get("next_earnings_date"):
            continue
        try:
            known[t] = date.fromisoformat(e["next_earnings_date"])
        except ValueError:
            continue
    return known


def buyback_module(known_dates, as_of_date, gaps):
    n_total = len(SP100_TICKERS)
    n_known = len(known_dates)
    if n_known < n_total * BUYBACK_MIN_COVERAGE_FRAC:
        gaps.append(f"庫藏股靜默期：僅取得 {n_known}/{n_total} 檔財報日"
                    f"（<{int(BUYBACK_MIN_COVERAGE_FRAC*100)}%），依規則不產出覆蓋率，模組輸出 null")
        return None

    weeks = []
    for i in range(BUYBACK_WEEKS_AHEAD):
        week_start = as_of_date + timedelta(days=7 * i)
        weekdays = [week_start + timedelta(days=d) for d in range(5)]  # Mon-Fri 代理，週線粒度
        total_frac = 0.0
        for ed in known_dates.values():
            blackout_start = ed - timedelta(days=BUYBACK_BLACKOUT_BEFORE_DAYS)
            blackout_end = ed + timedelta(days=BUYBACK_BLACKOUT_AFTER_DAYS)
            in_days = sum(1 for wd in weekdays if blackout_start <= wd <= blackout_end)
            total_frac += in_days / 5.0
        cov_pct = rnd(100.0 * total_frac / n_known, 1)
        weeks.append({"week_start": week_start.isoformat(), "coverage_pct": cov_pct})

    peak = max(weeks, key=lambda w: w["coverage_pct"])
    return {
        "as_of": as_of_date.isoformat(),
        "universe_n": n_known,
        "universe_total": n_total,
        "weighting_note": "等權（equal-weight），非市值加權",
        "blackout_window_note": f"財報前 {BUYBACK_BLACKOUT_BEFORE_DAYS} 曆日 至 "
                                f"財報後 {BUYBACK_BLACKOUT_AFTER_DAYS} 曆日",
        "blackout_cov_pct_by_week": weeks,
        "peak_week": peak["week_start"],
    }


# ═══════════════════════════════════════════════════════════════════════════
# 模組 4：槓桿 ETF 每日再平衡（設計稿 §E1）
# ═══════════════════════════════════════════════════════════════════════════

def _age_days(fetched_at, now):
    if not fetched_at:
        return None
    try:
        dt = datetime.strptime(fetched_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return (now - dt).total_seconds() / 86400.0
    except Exception:
        return None


def refresh_etf_aum_cache(skip_fetch):
    """槓桿／反向 ETF 複合體 AUM 快取（yfinance totalAssets），7 天內不重抓。

    回傳 {ticker: {"aum_usd_bn": float, "stale": bool}}——單檔失敗沿用上次快取值
    並標 stale=True；從未成功抓過的 ticker 不出現在回傳值中（呼叫端須跳過）。
    """
    cache = load_json(LEV_ETF_AUM_CACHE, {"meta": {}, "tickers": {}})
    entries = cache.setdefault("tickers", {})
    now = datetime.now(timezone.utc)
    tickers = _all_lev_etf_tickers()
    fetched_n = 0
    failed_n = 0
    skipped_n = 0
    failed_this_run = set()

    if not skip_fetch:
        try:
            import yfinance as yf  # noqa: F401
        except ImportError:
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", "-q",
                             "yfinance>=0.2.40", "pandas"])
            import yfinance as yf
        for t in tickers:
            e = entries.get(t)
            age = _age_days(e.get("fetched_at") if e else None, now)
            fresh = (e is not None and e.get("aum_usd_bn") is not None
                    and age is not None and age < LEV_ETF_AUM_MAX_AGE_DAYS)
            if fresh:
                skipped_n += 1
                continue
            try:
                etf_info = yf.Ticker(t).info or {}
                ta = etf_info.get("totalAssets")
                if not ta:
                    raise ValueError("totalAssets missing/zero in yfinance .info")
                entries[t] = {
                    "aum_usd_bn": round(float(ta) / 1e9, 4),
                    "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
                fetched_n += 1
            except Exception as exc:
                failed_n += 1
                failed_this_run.add(t)
                warn(f"lev-etf AUM fetch failed for {t}: {str(exc)[:80]}")
                # 保留舊快取值（若有）當 fallback，不覆寫成 null
            time.sleep(0.15)

    cache["meta"] = {
        "built_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "universe_n": len(tickers),
        "cache_max_age_days": LEV_ETF_AUM_MAX_AGE_DAYS,
        "note": "槓桿／反向 ETF 複合體 AUM 快取（yfinance .info totalAssets），"
                "7 天內不重抓；單檔失敗沿用上次快取值並標 stale，不覆寫成 null。",
    }
    write_json_if_changed(LEV_ETF_AUM_CACHE, cache)
    info(f"lev-etf AUM cache: fetched={fetched_n} skipped_fresh={skipped_n} failed={failed_n}")

    out = {}
    for t in tickers:
        e = entries.get(t)
        if not e or e.get("aum_usd_bn") is None:
            continue
        age = _age_days(e.get("fetched_at"), now)
        stale = (t in failed_this_run) or (age is None) or (age >= LEV_ETF_AUM_MAX_AGE_DAYS)
        out[t] = {"aum_usd_bn": e["aum_usd_bn"], "stale": bool(stale)}
    return out


def _daily_return_from_series(pts):
    """pts: [(date, close), ...] 升冪排序。回傳最新一筆對前一筆的報酬（小數），
    資料不足回傳 None。"""
    if not pts or len(pts) < 2:
        return None
    prev = pts[-2][1]
    cur = pts[-1][1]
    if not prev:
        return None
    return cur / prev - 1.0


def _sox_underlying_return(skip_fetch, gaps):
    """SOX 複合體標的報酬：既有價格快取無非槓桿半導體代理，改用 SOXL（失敗則
    SOXS）自身當日報酬 ÷ 槓桿反推。--skip-fetch 模式不重抓（該資料不落盤快取），
    直接跳過並記錄 gap。"""
    if skip_fetch:
        gaps.append("SOX 複合體標的報酬：--skip-fetch 模式不重抓 SOXL／SOXS，本次跳過")
        return None
    for ticker, lev in (("SOXL", 3), ("SOXS", -3)):
        try:
            rows = _yf_daily([ticker], period="5d").get(ticker)
            if rows and len(rows) >= 2:
                c_prev, c_cur = rows[-2][1], rows[-1][1]
                if c_prev:
                    return (c_cur / c_prev - 1.0) / lev
        except Exception as e:
            warn(f"SOX underlying return via {ticker} failed: {e}")
    gaps.append("SOX 複合體標的報酬：SOXL／SOXS 皆抓取失敗，SOX 複合體本次跳過")
    return None


def lev_etf_module(price_series, aum_map, skip_fetch, gaps):
    spy_pts = price_series.get("SPY") or []
    as_of = spy_pts[-1][0] if spy_pts else None

    complexes_out = []
    for cx in LEV_ETF_COMPLEXES:
        label = cx["complex"]
        proxy = cx.get("underlying_proxy")
        if proxy:
            r = _daily_return_from_series(price_series.get(proxy) or [])
            if r is None:
                gaps.append(f"槓桿ETF {label} 複合體：{proxy} 報酬資料不足，複合體跳過")
                continue
            proxy_label = proxy
        else:
            r = _sox_underlying_return(skip_fetch, gaps)
            if r is None:
                continue  # gap 已在 _sox_underlying_return 內記錄
            proxy_label = "SOXL/SOXS（自身報酬÷槓桿反推，無現成非槓桿代理）"

        legs_out = []
        k_complex = 0.0
        for ticker, lev in cx["legs"]:
            a = aum_map.get(ticker)
            if not a:
                gaps.append(f"槓桿ETF {label}／{ticker}：AUM 無可用資料（含快取），該檔跳過")
                continue
            coef = _lev_coef(lev)
            aum_bn = a["aum_usd_bn"]
            flow_bn = coef * aum_bn * r
            legs_out.append({
                "ticker": ticker,
                "leverage": lev,
                "coef": coef,
                "aum_usd_bn": rnd(aum_bn, 3),
                "aum_stale": bool(a["stale"]),
                "today_flow_usd_bn": rnd(flow_bn, 3),
            })
            k_complex += coef * aum_bn

        if not legs_out:
            gaps.append(f"槓桿ETF {label} 複合體：所有成分 AUM 皆無可用資料，複合體跳過")
            continue

        shock_table = [
            {"shock_pct": s, "flow_usd_bn": rnd(k_complex * (s / 100.0), 3)}
            for s in LEV_ETF_SHOCK_PCTS
        ]
        complexes_out.append({
            "complex": label,
            "underlying_proxy": proxy_label,
            "underlying_return_pct": rnd(r * 100, 3),
            "legs": legs_out,
            "today_realized_flow_usd_bn": rnd(k_complex * r, 3),
            "shock_table": shock_table,
            "confidence": LEV_ETF_CONFIDENCE,
        })

    if not complexes_out:
        gaps.append("槓桿ETF再平衡：三個複合體皆無可用資料，模組輸出 null")
        return None

    return {"as_of": as_of, "complexes": complexes_out}


# ═══════════════════════════════════════════════════════════════════════════
# 模組 5：月末／季末再平衡壓力（設計稿 §E2）
# ═══════════════════════════════════════════════════════════════════════════

def _weekdays_of_month(year, month):
    import calendar as _cal
    days_in_month = _cal.monthrange(year, month)[1]
    return [date(year, month, d) for d in range(1, days_in_month + 1)
            if date(year, month, d).weekday() < 5]


def _mtd_return_pct(pts, as_of_date):
    """pts: [(date_str, close), ...] 升冪排序。MTD% = 今日收盤 / 上月底收盤 − 1。
    資料不足（無上月底收盤或無今日收盤）回傳 None。"""
    if not pts:
        return None
    month_start_str = as_of_date.replace(day=1).isoformat()
    as_of_str = as_of_date.isoformat()
    prior_close = None
    asof_close = None
    for d, c in pts:
        if d < month_start_str:
            prior_close = c
        if d == as_of_str:
            asof_close = c
    if prior_close is None or asof_close is None or not prior_close:
        return None
    return (asof_close / prior_close - 1.0) * 100.0


def _magnitude_bucket(abs_div_pp):
    """量級桶（設計稿 §E2，外部研究粗錨，lo 信心）：
    <2pp→小[0,10]；2–5pp→中[10,30]；>5pp→大[30,60]（單位：億美元 usd_bn）。"""
    if abs_div_pp < 2.0:
        return "小", [0, 10]
    if abs_div_pp <= 5.0:
        return "中", [10, 30]
    return "大", [30, 60]


def month_end_module(price_series, gaps):
    spy_pts = price_series.get("SPY") or []
    agg_pts = price_series.get("AGG") or []
    if not spy_pts:
        gaps.append("月末再平衡：SPY 價格快取為空，模組跳過")
        return None
    if not agg_pts:
        gaps.append("月末再平衡：AGG 價格快取為空，模組跳過")
        return None

    as_of_str = spy_pts[-1][0]
    as_of_date = date.fromisoformat(as_of_str)

    spy_mtd = _mtd_return_pct(spy_pts, as_of_date)
    agg_mtd = _mtd_return_pct(agg_pts, as_of_date)
    if spy_mtd is None or agg_mtd is None:
        gaps.append("月末再平衡：本月或上月底收盤資料不足，無法算 MTD 報酬，模組跳過")
        return None

    divergence = spy_mtd - agg_mtd
    if divergence > 1e-9:
        direction = "sell_equity_buy_bond"
    elif divergence < -1e-9:
        direction = "buy_equity_sell_bond"
    else:
        direction = "flat"

    bucket_label, bucket_range = _magnitude_bucket(abs(divergence))

    wds = _weekdays_of_month(as_of_date.year, as_of_date.month)
    last3 = wds[-MONTH_END_WINDOW_DAYS:] if len(wds) >= MONTH_END_WINDOW_DAYS else wds
    in_window = as_of_date in last3
    is_qtr = as_of_date.month in QUARTER_END_MONTHS

    return {
        "as_of": as_of_str,
        "month": as_of_date.strftime("%Y-%m"),
        "spy_mtd_return_pct": rnd(spy_mtd, 3),
        "agg_mtd_return_pct": rnd(agg_mtd, 3),
        "divergence_pct": rnd(divergence, 3),
        "direction": direction,
        "magnitude_bucket": {"label": bucket_label, "range_usd_bn": bucket_range},
        "effective_window": {
            "start": last3[0].isoformat() if last3 else None,
            "end": last3[-1].isoformat() if last3 else None,
        },
        "in_window": in_window,
        "is_quarter_end_month": is_qtr,
        "quarter_end_note": QUARTER_END_NOTE if is_qtr else None,
        "confidence": MONTH_END_CONFIDENCE,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 每日凍結預測（設計稿 §A6 自我證偽機制）
# ═══════════════════════════════════════════════════════════════════════════

def build_lev_etf_frozen(lev_etf_out):
    """槓桿ETF條件表快照——本模組無行為級 kill（純算術），凍結純為稽核留痕。"""
    if not lev_etf_out:
        return None
    out = []
    for c in lev_etf_out.get("complexes", []):
        out.append({
            "complex": c["complex"],
            "today_realized_flow_usd_bn": c["today_realized_flow_usd_bn"],
            "shock_table": c["shock_table"],
        })
    return out or None


def build_month_end_frozen(month_end_out):
    """月末生效窗首日凍結方向件（設計稿 §E2）：只在生效窗第一個交易日落帳，
    對帳定義＝生效窗 3 日 SPY−AGG 相對報酬方向（非本檔職責，留給後續結算腳本）。"""
    if not month_end_out or not month_end_out.get("in_window"):
        return None
    win = month_end_out.get("effective_window") or {}
    if month_end_out.get("as_of") != win.get("start"):
        return None
    return {
        "as_of": month_end_out["as_of"],
        "direction": month_end_out["direction"],
        "divergence_pct": month_end_out["divergence_pct"],
        "window_start": win.get("start"),
        "window_end": win.get("end"),
    }


def build_frozen_forecast(cta_out, vol_control_out, lev_etf_out, month_end_out, as_of):
    cta_fc = []
    for m in cta_out:
        windows = m["windows"]
        cand = min(windows, key=lambda w: abs(w["dist_pct"]) if w["dist_pct"] is not None else float("inf"))
        total = len(windows)
        pos_now = sum(1 for w in windows if w["signal"] > 0)
        pos_after = pos_now + (1 if cand["signal"] <= 0 else -1)
        pos_after = max(0, min(total, pos_after))
        cta_fc.append({
            "market": m["market"],
            "nearest_flip_window": cand["len"],
            "nearest_flip_level": cand["flip_level"],
            "dist_pct": cand["dist_pct"],
            "current_composite": m["composite_signal"],
            "if_breached_composite": f"+{pos_after}/{total}",
        })

    vc_fc = None
    if vol_control_out:
        nd = vol_control_out.get("next_day_scenario") or {}
        vc_fc = {
            "plus_2pct_exposure_change_dir": (nd.get("plus_2pct") or {}).get("exposure_change_dir"),
            "minus_2pct_exposure_change_dir": (nd.get("minus_2pct") or {}).get("exposure_change_dir"),
        }

    lev_etf_fc = build_lev_etf_frozen(lev_etf_out)
    month_end_fc = build_month_end_frozen(month_end_out)

    return {"as_of": as_of, "cta": cta_fc, "vol_control": vc_fc,
            "lev_etf": lev_etf_fc, "month_end": month_end_fc}


def append_forecast_history(as_of, frozen_forecast):
    """append-only jsonl；同日重跑覆蓋當日那行，不重複 append。"""
    line_obj = {"date": as_of, "frozen_forecast": frozen_forecast}
    records = []
    if os.path.exists(FORECAST_HISTORY):
        with open(FORECAST_HISTORY, encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    obj = json.loads(ln)
                except json.JSONDecodeError:
                    continue
                if obj.get("date") != as_of:
                    records.append(obj)
    records.append(line_obj)
    records.sort(key=lambda o: o.get("date") or "")
    os.makedirs(os.path.dirname(FORECAST_HISTORY), exist_ok=True)
    with open(FORECAST_HISTORY, "w", encoding="utf-8") as f:
        for obj in records:
            f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Conditional Flow Map — Phase 1 daily builder")
    ap.add_argument("--skip-fetch", action="store_true",
                    help="offline: skip yfinance/stooq fetch, recompute from caches only")
    args = ap.parse_args()

    gaps = ["dealer gamma：無 OI 級資料（CBOE/OCC），Phase 2 待解，本次不捏造"]

    # ── 價格快取 + 模組 1/2 ──
    price_series = build_price_cache(args.skip_fetch)
    cta_out = cta_module(price_series, gaps)
    vol_control_out = vol_control_module(price_series, gaps)

    as_of = None
    spy_pts = price_series.get("SPY") or []
    if spy_pts:
        as_of = spy_pts[-1][0]
    else:
        as_of = date.today().isoformat()
        gaps.append("as_of：SPY 價格快取為空，退回今日日期")

    # ── 模組 3：庫藏股靜默期 ──
    try:
        known_dates = refresh_earnings_cache(args.skip_fetch)
        buyback_out = buyback_module(known_dates, date.fromisoformat(as_of), gaps)
    except Exception as e:
        warn(f"buyback module failed: {e}")
        gaps.append(f"庫藏股靜默期：模組執行失敗（{str(e)[:120]}），輸出 null")
        buyback_out = None

    # ── 模組 4：槓桿 ETF 每日再平衡（Phase 1.5，§E1）──
    try:
        aum_map = refresh_etf_aum_cache(args.skip_fetch)
        lev_etf_out = lev_etf_module(price_series, aum_map, args.skip_fetch, gaps)
    except Exception as e:
        warn(f"lev-etf module failed: {e}")
        gaps.append(f"槓桿ETF再平衡：模組執行失敗（{str(e)[:120]}），輸出 null")
        lev_etf_out = None

    # ── 模組 5：月末／季末再平衡壓力（Phase 1.5，§E2）──
    try:
        month_end_out = month_end_module(price_series, gaps)
    except Exception as e:
        warn(f"month-end module failed: {e}")
        gaps.append(f"月末再平衡：模組執行失敗（{str(e)[:120]}），輸出 null")
        month_end_out = None

    frozen_forecast = build_frozen_forecast(cta_out, vol_control_out, lev_etf_out,
                                            month_end_out, as_of)

    payload = {
        "schema": SCHEMA,
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cta": cta_out,
        "vol_control": vol_control_out,
        "buyback": buyback_out,
        "gamma": None,
        "lev_etf": lev_etf_out,
        "month_end": month_end_out,
        "gaps": gaps,
        "frozen_forecast": frozen_forecast,
    }

    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"latest.json: {'written' if wrote else 'no change'} (as_of={as_of}, "
         f"cta_markets={len(cta_out)}, vol_control={'ok' if vol_control_out else 'null'}, "
         f"buyback={'ok' if buyback_out else 'null'}, "
         f"lev_etf_complexes={len(lev_etf_out['complexes']) if lev_etf_out else 0}, "
         f"month_end={'ok' if month_end_out else 'null'})")

    append_forecast_history(as_of, frozen_forecast)
    info(f"forecast_history.jsonl: appended/overwritten row for {as_of}")

    if not cta_out and not vol_control_out and not buyback_out:
        warn("all three Phase-1 modules failed — exiting non-zero")
        sys.exit(1)
    info("done.")


if __name__ == "__main__":
    main()
