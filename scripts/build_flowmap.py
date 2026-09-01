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

輸出
----
  data/flowmap_prices.json          — SPY/QQQ/IWM 日線 close，rolling ~500 個交易日
                                       （yfinance -> stooq fallback，incremental）。
  data/flowmap_earnings_cache.json  — 100 檔次次財報日快取（7 天內不重抓）。
  docs/flowmap/data/latest.json     — 契約 JSON（schema="flowmap-v1"）。
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
OUT_DIR = os.path.join(ROOT, "docs", "flowmap", "data")
OUT_JSON = os.path.join(OUT_DIR, "latest.json")
FORECAST_HISTORY = os.path.join(OUT_DIR, "forecast_history.jsonl")

SCHEMA = "flowmap-v1"


def warn(msg: str) -> None:
    print(f"[flowmap][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[flowmap] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（設計稿 §A2／§A6）。不得因單一案例調參。
# ═══════════════════════════════════════════════════════════════════════════

# ── 價格快取 ──
FLOWMAP_SYMBOLS = ["SPY", "QQQ", "IWM"]
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
    single = len(tickers) == 1
    for tk in tickers:
        try:
            sub = df if single else df[tk]
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
# 每日凍結預測（設計稿 §A6 自我證偽機制）
# ═══════════════════════════════════════════════════════════════════════════

def build_frozen_forecast(cta_out, vol_control_out, as_of):
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

    return {"as_of": as_of, "cta": cta_fc, "vol_control": vc_fc}


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

    frozen_forecast = build_frozen_forecast(cta_out, vol_control_out, as_of)

    payload = {
        "schema": SCHEMA,
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cta": cta_out,
        "vol_control": vol_control_out,
        "buyback": buyback_out,
        "gamma": None,
        "gaps": gaps,
        "frozen_forecast": frozen_forecast,
    }

    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"latest.json: {'written' if wrote else 'no change'} (as_of={as_of}, "
         f"cta_markets={len(cta_out)}, vol_control={'ok' if vol_control_out else 'null'}, "
         f"buyback={'ok' if buyback_out else 'null'})")

    append_forecast_history(as_of, frozen_forecast)
    info(f"forecast_history.jsonl: appended/overwritten row for {as_of}")

    if not cta_out and not vol_control_out and not buyback_out:
        warn("all three Phase-1 modules failed — exiting non-zero")
        sys.exit(1)
    info("done.")


if __name__ == "__main__":
    main()
