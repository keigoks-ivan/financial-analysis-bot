#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistical Properties Panel（統計性質面板）— daily data pipeline.

回答「什麼統計性質現在處於什麼狀態」——相關性、VIX 期限結構、COT 部位極端
統計三個獨立描述器模組，禁方向結論、禁買賣指令。設計依據：
notes/site-internal/root/_flowmap_forecast_ledger_design_20260901.md §G
（判斷已在設計稿凍結：窗長／門檻／onset 定義一律不得自行調整，改動需回設計
稿另過校準）。**本檔不含 producers**（vix-model／cot-model 是另一包，見設計
稿 §G5；settle_forecasts.py 與任何 generate_*_forecasts.py 都不在本檔範圍）。

三個模組
--------
  相關性（§G2）      ：SPY–TLT 63 交易日滾動相關；11 檔 SPDR sector 兩兩 63
                        交易日滾動相關的等權平均。各附 3 年分位＋近 90 日走勢。
  VIX 期限結構（§G3） ：slope = ^VIX3M − ^VIX（收盤差）。3 年分位；倒掛事件表
                        （onset＝連續 ≥5 日 slope>0 後首個 <0；記回正天數）。
  COT 極端統計（§G4） ：消費 data/cot_history.json（唯讀，crowding pipeline
                        維護）——15 市場滾動 3 年（156 週）分位，極端燈
                        ≥95／≤5。只對權益三指數（S&P/NDX/RTY e-mini，價格代
                        理 SPY/QQQ/IWM 讀 data/flowmap_prices.json 唯讀）算
                        「極端後 4 週價格反向」base rate，分市場＋pooled，樣
                        本數必列；2021 起樣本天生薄，一律標低信心。其餘 12
                        市場只渲染極端狀態，不算 base rate。

資料層
------
  data/statlab_prices.json          — SPY/TLT/11 SPDR sector/^VIX/^VIX3M 日線
                                       close，rolling ~830 個交易日（~3 年 3
                                       個月，多出的緩衝是為了讓「63 日滾動相
                                       關」這個衍生序列本身也能算出完整 3 年
                                       分位，不是放寬 3 年這個凍結窗長）。
                                       yfinance -> stooq fallback，incremental。
  data/cot_history.json             — 唯讀，本檔不寫入。
  data/flowmap_prices.json          — 唯讀，本檔不寫入；只取 SPY/QQQ/IWM 供
                                       COT base rate 對帳用。
  docs/statlab/data/latest.json     — 契約 JSON（schema="statlab-v1"）。

CLI
---
  python scripts/build_statlab.py                 完整每日刷新（預設）
  python scripts/build_statlab.py --skip-fetch     離線：只用既有快取重算

Design contracts（比照 build_flowmap.py / build_crowding.py）
--------------------------------------------------------------
  * Zero churn：latest.json 與價格快取皆先比對現值再寫，內容不變則不落盤
    （易變欄位 generated_at/built_at/fetched_at 比對前先剝除）。
  * Fault tolerance：三模組互相獨立、warn-and-continue；任一模組資料不足就
    整模組輸出 null 並記錄到 gaps，不用舊值或估值填充。
  * PREREG 凍結：CORR_WINDOW／PCTILE_WINDOW_3Y／COT_PCTILE_WINDOW_WEEKS／
    COT_EXTREME_HI／COT_EXTREME_LO／VIX_INVERSION_ONSET_STREAK／
    COT_BASE_RATE_LOOKAHEAD_* 皆為設計稿凍結值，不得依單一案例調參（見設計
    稿 §G7／校準輪流程）。
"""
from __future__ import annotations

import argparse
import bisect
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PRICE_CACHE = os.path.join(DATA, "statlab_prices.json")
COT_HISTORY = os.path.join(DATA, "cot_history.json")
FLOWMAP_PRICE_CACHE = os.path.join(DATA, "flowmap_prices.json")
OUT_DIR = os.path.join(ROOT, "docs", "statlab", "data")
OUT_JSON = os.path.join(OUT_DIR, "latest.json")

SCHEMA = "statlab-v1"


def warn(msg: str) -> None:
    print(f"[statlab][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[statlab] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（設計稿 §G2／§G3／§G4）。不得因單一案例調參。
# ═══════════════════════════════════════════════════════════════════════════

SECTOR_SYMBOLS = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
STATLAB_SYMBOLS = ["SPY", "TLT"] + SECTOR_SYMBOLS + ["^VIX", "^VIX3M"]
# ~3 年（756 個交易日）＋63 日相關滾動窗緩衝＋假期緩衝，見檔頭說明。
ROLLING_TRADING_DAYS = 850
BOOTSTRAP_PERIOD = "4y"

# ── 相關性模組（§G2）──
CORR_WINDOW = 63          # 滾動相關窗長（交易日）
PCTILE_WINDOW_3Y = 756    # 3 年分位視窗（交易日，252×3）

# ── VIX 期限結構模組（§G3）──
VIX_INVERSION_ONSET_STREAK = 5  # onset＝連續 ≥5 日 slope>0 後首個 <0

# ── COT 極端統計模組（§G4，重設計——與 crowding 5y/90-10 刻意不同）──
COT_PCTILE_WINDOW_WEEKS = 156   # 3 年分位視窗（週，52×3）
COT_EXTREME_HI = 95
COT_EXTREME_LO = 5
# CFTC 契約代碼 -> 顯示序（沿用 build_crowding.py COT_MARKETS 的碼與序，資料
# 與 label 一律讀 cot_history.json，本檔不重複硬編數字）。
COT_DISPLAY_ORDER = [
    "13874A", "209742", "239742", "1170E1", "042601", "044601", "043602",
    "020601", "098662", "099741", "097741", "088691", "084691", "085692", "067651",
]
# 權益三指數：CFTC 碼 -> (顯示標籤 fallback, 價格代理 ticker，走 flowmap 快取)。
EQUITY_THREE_PROXY = {"13874A": "SPY", "209742": "QQQ", "239742": "IWM"}
COT_BASE_RATE_LOOKAHEAD_WEEKS = 4
COT_BASE_RATE_LOOKAHEAD_DAYS = 28  # 4 週的曆日近似值，用來在日線價格快取上找比較點


# ═══════════════════════════════════════════════════════════════════════════
# Zero-churn IO（同 build_flowmap.py / build_crowding.py 協議）
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


def pctile_incl(values, x):
    """Inclusive percentile rank (fraction of values <= x), 0..100.

    同 build_crowding.py pctile_incl 的定義（本檔獨立複製一份，比照
    build_flowmap.py 對 build_crowding.py 小工具函式各自獨立複製的既有慣例）。
    """
    v = [z for z in values if z is not None]
    n = len(v)
    if n == 0 or x is None:
        return None
    return round(100.0 * sum(1 for z in v if z <= x) / n, 1)


def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 statlab"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 statlab"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


# ═══════════════════════════════════════════════════════════════════════════
# 價格快取（daily close, yfinance -> stooq fallback, incremental）
# ═══════════════════════════════════════════════════════════════════════════

def _yf_daily(tickers, period="4y"):
    """Batch daily close download -> {ticker: [(date, close), ...]}."""
    import yfinance as yf
    out = {}
    if not tickers:
        return out
    df = yf.download(tickers, period=period, interval="1d", auto_adjust=True,
                     group_by="ticker", threads=True, progress=False)
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
    if sym.startswith("^"):
        # 指數代碼（^VIX／^VIX3M）在 stooq 不吃 .us 後綴（那只用於美股個股/ETF）。
        pass
    elif "." not in sym:
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
    """Incrementally refresh data/statlab_prices.json.  Returns
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
        missing = [t for t in STATLAB_SYMBOLS if not series.get(t)]
        existing = [t for t in STATLAB_SYMBOLS if series.get(t)]
        for label, batch, period in (("bootstrap", missing, BOOTSTRAP_PERIOD),
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
        for t in STATLAB_SYMBOLS:
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
        "symbols": STATLAB_SYMBOLS,
        "note": "daily close cache for statlab correlation / VIX term-structure "
                "modules (SPY/TLT/11 SPDR sector ETFs/^VIX/^VIX3M); yfinance->"
                "stooq fallback; incremental, rolling ~850 trading days "
                "(~3y + 63d correlation-window bootstrap buffer).",
    }
    wrote = write_json_if_changed(PRICE_CACHE, cache)
    n = {t: len(series.get(t, [])) for t in STATLAB_SYMBOLS}
    info(f"price cache: {n}, {'written' if wrote else 'no change'}")
    return {t: [(d, c) for d, c in series.get(t, [])] for t in STATLAB_SYMBOLS}


# ═══════════════════════════════════════════════════════════════════════════
# 共用數學工具
# ═══════════════════════════════════════════════════════════════════════════

def _align_dates(series_list):
    """series_list: list of list[(date, val)].  Returns (dates, [vals...])
    restricted to dates common to every series (raw price series, not returns
    — correlation is computed on returns derived from this common calendar so
    each symbol's own occasional missing bar can't desync the pair)."""
    if not series_list:
        return [], []
    maps = [dict(s) for s in series_list]
    common = set(maps[0].keys())
    for m in maps[1:]:
        common &= set(m.keys())
    dates = sorted(common)
    aligned = [[m[d] for d in dates] for m in maps]
    return dates, aligned


def _simple_returns(dates, closes):
    """(dates, closes) aligned lists -> (return_dates, returns) for t>=1."""
    rets = [closes[i] / closes[i - 1] - 1.0 for i in range(1, len(closes))]
    return dates[1:], rets


def pearson_corr(xs, ys):
    n = len(xs)
    if n < 5:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return None
    return cov / ((vx * vy) ** 0.5)


def rolling_corr_series(dates, xs, ys, window):
    """Returns list of (date, corr) for each i where a full trailing `window`
    exists (i.e. i >= window-1)."""
    out = []
    for i in range(window - 1, len(dates)):
        c = pearson_corr(xs[i - window + 1:i + 1], ys[i - window + 1:i + 1])
        if c is not None:
            out.append((dates[i], c))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 模組一：相關性（設計稿 §G2）
# ═══════════════════════════════════════════════════════════════════════════

def _corr_summary(corr_ts, gaps, label, n_pairs=None):
    if not corr_ts:
        gaps.append(f"相關性模組：{label} 無法計算（價格樣本或共同交易日不足）")
        return None
    corr_ts = sorted(corr_ts)
    vals = [v for _, v in corr_ts]
    cur_date, cur_val = corr_ts[-1]
    window_n = min(len(vals), PCTILE_WINDOW_3Y)
    pctile = pctile_incl(vals[-window_n:], cur_val)
    spark = corr_ts[-90:]
    if window_n < PCTILE_WINDOW_3Y:
        gaps.append(f"相關性模組：{label} 3 年分位樣本僅 {window_n} 個交易日"
                    f"（<{PCTILE_WINDOW_3Y}），分位可信度隨快取累積提升")
    result = {
        "window_days": CORR_WINDOW,
        "current": rnd(cur_val, 3),
        "pctile_3y": pctile,
        "pctile_window_n": window_n,
        "as_of": cur_date,
        "spark_90d": [[d, rnd(v, 3)] for d, v in spark],
        "confidence": "hi" if window_n >= PCTILE_WINDOW_3Y else "med",
    }
    if n_pairs is not None:
        result["n_pairs"] = n_pairs
    return result


def correlation_module(price_series, gaps):
    out = {}

    spy = price_series.get("SPY") or []
    tlt = price_series.get("TLT") or []
    if len(spy) < CORR_WINDOW + 30 or len(tlt) < CORR_WINDOW + 30:
        gaps.append("相關性模組：SPY／TLT 價格樣本不足，SPY-TLT 相關性略過")
        out["spy_tlt"] = None
    else:
        dates, aligned = _align_dates([spy, tlt])
        if len(dates) < CORR_WINDOW + 31:
            gaps.append("相關性模組：SPY／TLT 共同交易日不足，SPY-TLT 相關性略過")
            out["spy_tlt"] = None
        else:
            rdates, rx = _simple_returns(dates, aligned[0])
            _, ry = _simple_returns(dates, aligned[1])
            corr_ts = rolling_corr_series(rdates, rx, ry, CORR_WINDOW)
            out["spy_tlt"] = _corr_summary(corr_ts, gaps, "SPY-TLT")

    avail = {}
    for t in SECTOR_SYMBOLS:
        pts = price_series.get(t) or []
        if len(pts) >= CORR_WINDOW + 30:
            avail[t] = pts
        else:
            gaps.append(f"相關性模組：sector {t} 價格樣本不足，未納入 sector 兩兩相關平均")
    tickers = sorted(avail.keys())
    if len(tickers) < 2:
        gaps.append("相關性模組：可用 sector ETF 不足 2 檔，sector 平均兩兩相關略過")
        out["sector_avg_pairwise"] = None
    else:
        pair_series = {}
        for ta, tb in combinations(tickers, 2):
            dates, aligned = _align_dates([avail[ta], avail[tb]])
            if len(dates) < 2:
                continue
            rdates_a, ra = _simple_returns(dates, aligned[0])
            _, rb = _simple_returns(dates, aligned[1])
            if len(rdates_a) < CORR_WINDOW + 30:
                continue
            cts = rolling_corr_series(rdates_a, ra, rb, CORR_WINDOW)
            if cts:
                pair_series[(ta, tb)] = dict(cts)
        if not pair_series:
            gaps.append("相關性模組：sector 兩兩相關全數無法計算，sector 平均兩兩相關略過")
            out["sector_avg_pairwise"] = None
        else:
            all_dates = sorted(set().union(*[set(v.keys()) for v in pair_series.values()]))
            avg_ts = []
            for d in all_dates:
                vals = [pair_series[p][d] for p in pair_series if d in pair_series[p]]
                if vals:
                    avg_ts.append((d, sum(vals) / len(vals)))
            out["sector_avg_pairwise"] = _corr_summary(
                avg_ts, gaps, "sector 平均兩兩相關", n_pairs=len(pair_series))

    return out


# ═══════════════════════════════════════════════════════════════════════════
# 模組二：VIX 期限結構（設計稿 §G3）
# ═══════════════════════════════════════════════════════════════════════════

VIX_GAP_THRESHOLD_DAYS = 10  # 見下方 vix_term_module 註解：偵測上游 feed 資料缺口用，非 PREREG 判斷門檻

def _vix_inversion_events(slope_ts, gap_threshold_days=VIX_GAP_THRESHOLD_DAYS):
    """slope_ts: 依日期排序的 (date, slope) 序列。
    onset＝連續 ≥VIX_INVERSION_ONSET_STREAK 日 slope>0 後首個 <0（PREREG 凍
    結，設計稿 §G3）。回正天數＝onset 到下一個 slope>0 日的交易日差。

    若相鄰兩筆資料日曆日差超過 gap_threshold_days（上游 feed 出現長天期缺
    口，非正常週末／假日間隔），streak 在缺口處強制歸零重新起算——缺口期間
    實際發生過什麼無法得知，不允許 onset／回正判定跨過資料缺口去配對兩端，
    避免把「資料沒有」誤判成「連續站在正值」。回傳 (events, gaps_found)。"""
    events = []
    gaps_found = []
    consec_pos = 0
    n = len(slope_ts)
    for i in range(n):
        d, s = slope_ts[i]
        if i > 0:
            prev_d = slope_ts[i - 1][0]
            gap_days = (date.fromisoformat(d) - date.fromisoformat(prev_d)).days
            if gap_days > gap_threshold_days:
                consec_pos = 0
                gaps_found.append((prev_d, d, gap_days))
        if s > 0:
            consec_pos += 1
            continue
        if s < 0:
            if consec_pos >= VIX_INVERSION_ONSET_STREAK:
                recovery_idx = None
                for j in range(i + 1, n):
                    if slope_ts[j][1] > 0:
                        recovery_idx = j
                        break
                if recovery_idx is not None:
                    events.append({
                        "onset_date": d,
                        "onset_slope": rnd(s, 3),
                        "recovery_date": slope_ts[recovery_idx][0],
                        "recovery_trading_days": recovery_idx - i,
                        "status": "resolved",
                    })
                else:
                    events.append({
                        "onset_date": d,
                        "onset_slope": rnd(s, 3),
                        "recovery_date": None,
                        "recovery_trading_days": None,
                        "status": "ongoing",
                    })
            consec_pos = 0
        else:
            consec_pos = 0
    return events, gaps_found


def vix_term_module(price_series, gaps):
    vix = price_series.get("^VIX") or []
    vix3m = price_series.get("^VIX3M") or []
    if len(vix) < 30 or len(vix3m) < 30:
        gaps.append("VIX期限結構模組：^VIX／^VIX3M 樣本不足，模組略過")
        return None
    dates, aligned = _align_dates([vix, vix3m])
    if len(dates) < 30:
        gaps.append("VIX期限結構模組：^VIX 與 ^VIX3M 共同交易日不足，模組略過")
        return None
    v, v3 = aligned
    slope_ts = [(dates[i], v3[i] - v[i]) for i in range(len(dates))]
    cur_date, cur_slope = slope_ts[-1]
    cur_vix, cur_vix3m = v[-1], v3[-1]
    window_n = min(len(slope_ts), PCTILE_WINDOW_3Y)
    vals = [s for _, s in slope_ts]
    pctile = pctile_incl(vals[-window_n:], cur_slope)
    state = "contango" if cur_slope > 0 else ("inverted" if cur_slope < 0 else "flat")
    events, data_gaps = _vix_inversion_events(slope_ts)
    if window_n < PCTILE_WINDOW_3Y:
        gaps.append(f"VIX期限結構模組：3 年分位樣本僅 {window_n} 個交易日（<{PCTILE_WINDOW_3Y}）")
    if data_gaps:
        shown = "；".join(f"{g0}→{g1}（{d} 曆日）" for g0, g1, d in data_gaps[-3:])
        more = f"，另有 {len(data_gaps) - 3} 段" if len(data_gaps) > 3 else ""
        gaps.append(f"VIX期限結構模組：^VIX／^VIX3M 共同交易日序列偵測到長天期資料缺口"
                    f"（{shown}{more}），上游 feed 於缺口期間無資料，倒掛事件的連續天數計算"
                    f"已在缺口處重新起算、不跨缺口累計，缺口期間可能發生過的倒掛事件無法判定")

    # 兩序列各自的最新一筆若不同步（其中一檔上游 feed 落後），現值仍以兩者
    # 共同交易日為準，但要誠實揭露落後幅度——沿用全站既有 5 天 stale 慣例
    # （build_monitor.py／2.5 對照表），不是新發明的門檻。
    raw_vix_latest = vix[-1][0]
    raw_vix3m_latest = vix3m[-1][0]
    stale = False
    if raw_vix_latest != raw_vix3m_latest:
        lag_days = (date.fromisoformat(max(raw_vix_latest, raw_vix3m_latest)) -
                    date.fromisoformat(cur_date)).days
        if lag_days > 5:
            stale = True
            lagging = "^VIX3M" if raw_vix3m_latest < raw_vix_latest else "^VIX"
            lagging_latest = min(raw_vix_latest, raw_vix3m_latest) if raw_vix3m_latest < raw_vix_latest \
                else raw_vix3m_latest
            gaps.append(f"VIX期限結構模組：{lagging} 上游資料最新僅到 {lagging_latest}，"
                        f"期限結構現值以兩者共同交易日 {cur_date} 為準，落後另一序列 {lag_days} 個曆日")

    return {
        "vix": rnd(cur_vix, 2),
        "vix3m": rnd(cur_vix3m, 2),
        "slope": rnd(cur_slope, 3),
        "state": state,
        "pctile_3y": pctile,
        "pctile_window_n": window_n,
        "as_of": cur_date,
        "stale": stale,
        "data_gaps_n": len(data_gaps),
        "onset_streak_days": VIX_INVERSION_ONSET_STREAK,
        "events_3y": events,
        "n_events_3y": len(events),
        "confidence": "hi" if (window_n >= PCTILE_WINDOW_3Y and not stale and not data_gaps) else "med",
    }


# ═══════════════════════════════════════════════════════════════════════════
# 模組三：COT 極端統計（設計稿 §G4，重設計；唯讀消費 cot_history.json）
# ═══════════════════════════════════════════════════════════════════════════

# 「最近一個 >= target 的交易日」查找的容忍窗——COT 事件週到下個交易日、或
# +28 曆日目標到下個交易日，正常應在數天內找到；超過這個容忍窗代表目標日期
# 根本落在價格快取覆蓋範圍之外（例如事件早於快取起點），此時必須視為「無可
# 用價格」略過，不能讓 bisect 硬牽到快取裡最近的日期、把一個時間上完全不相
# 干的價格點誤配成「事件發生後不久」，那會靜默產生語意錯誤的樣本。
PRICE_LOOKUP_TOLERANCE_DAYS = 10


def _nearest_date_on_or_after(sorted_dates, target, tolerance_days=PRICE_LOOKUP_TOLERANCE_DAYS):
    i = bisect.bisect_left(sorted_dates, target)
    if i >= len(sorted_dates):
        return None
    found = sorted_dates[i]
    lag = (date.fromisoformat(found) - date.fromisoformat(target)).days
    if lag > tolerance_days:
        return None
    return found


def _add_calendar_days(date_str, days):
    d = date.fromisoformat(date_str)
    return (d + timedelta(days=days)).isoformat()


def _cot_base_rate(equity_events, equity_label, flowmap_series, gaps):
    """equity_events: {code: [(event_date, 'long'|'short'), ...]}.
    極端偏多（long）事件預測「4 週後價格下跌」為命中；極端偏空（short）事件
    預測「4 週後價格上漲」為命中——契約反轉／均值回歸方向的最小定義，見設計
    稿 §G4「極端後 4 週價格反向」。"""
    if not flowmap_series:
        gaps.append("COT模組：data/flowmap_prices.json 無法讀取，權益三指數 base rate 略過")
        return None

    by_market = []
    pooled_n = pooled_hit = pooled_skipped = 0
    for code, events in equity_events.items():
        proxy = EQUITY_THREE_PROXY[code]
        label = equity_label.get(code, code)
        price_pts = flowmap_series.get(proxy) or []
        if not price_pts:
            gaps.append(f"COT base rate：flowmap 快取缺 {proxy}，{label} 略過")
            by_market.append({"market": label, "proxy": proxy, "n_events": 0,
                              "n_hit": 0, "hit_rate_pct": None,
                              "n_skipped_no_price": len(events)})
            continue
        price_sorted = sorted(price_pts)
        price_dates = [d for d, _ in price_sorted]
        price_map = dict(price_sorted)

        n_events = n_hit = n_skipped = 0
        for ev_date, direction in events:
            entry_date = _nearest_date_on_or_after(price_dates, ev_date)
            if entry_date is None:
                n_skipped += 1
                continue
            target_date = _add_calendar_days(ev_date, COT_BASE_RATE_LOOKAHEAD_DAYS)
            exit_date = _nearest_date_on_or_after(price_dates, target_date)
            if exit_date is None:
                n_skipped += 1
                continue
            entry_price, exit_price = price_map[entry_date], price_map[exit_date]
            if not entry_price:
                n_skipped += 1
                continue
            ret = exit_price / entry_price - 1.0
            hit = (ret < 0) if direction == "long" else (ret > 0)
            n_events += 1
            if hit:
                n_hit += 1
        hit_rate = round(100.0 * n_hit / n_events, 1) if n_events else None
        by_market.append({"market": label, "proxy": proxy, "n_events": n_events,
                          "n_hit": n_hit, "hit_rate_pct": hit_rate,
                          "n_skipped_no_price": n_skipped})
        pooled_n += n_events
        pooled_hit += n_hit
        pooled_skipped += n_skipped

    pooled_hit_rate = round(100.0 * pooled_hit / pooled_n, 1) if pooled_n else None
    return {
        "lookahead_weeks": COT_BASE_RATE_LOOKAHEAD_WEEKS,
        "lookahead_calendar_days": COT_BASE_RATE_LOOKAHEAD_DAYS,
        "definition": "COT 報告週淨部位 3 年滾動分位觸及 ≥95（極端偏多）或 ≤5"
                      "（極端偏空）時記一筆事件；偏多事件以「4 週後價格下跌」"
                      "為命中，偏空事件以「4 週後價格上漲」為命中——以事件週最"
                      "近可得交易日收盤為基準、+28 曆日後最近可得交易日收盤為"
                      "比較點。",
        "by_market": by_market,
        "pooled": {"n_events": pooled_n, "n_hit": pooled_hit,
                   "hit_rate_pct": pooled_hit_rate,
                   "n_skipped_no_price": pooled_skipped},
        "confidence": "lo",
        "caveat": "COT 資料自 2021 年起僅約 5 年，3 年滾動分位需滿 156 週才成"
                  "立，可用事件樣本集中在近 1–2 年（且受限於 flowmap 價格快取"
                  "回看範圍，更早的事件缺對應價格點會被跳過），樣本數天生偏"
                  "少，一律標低信心；同一市場連續數週維持極端時，每週皆各記"
                  "一筆事件，事件之間並非互相獨立樣本。",
    }


def cot_module(cot_history, flowmap_series, gaps):
    if not cot_history or not isinstance(cot_history.get("markets"), dict):
        gaps.append("COT模組：data/cot_history.json 無法讀取或格式異常，模組略過")
        return None

    markets_map = cot_history["markets"]
    methodology = (cot_history.get("meta") or {}).get("methodology", "")

    markets_out = []
    equity_events = {code: [] for code in EQUITY_THREE_PROXY}
    equity_label = {}
    cot_as_of = None

    codes = list(COT_DISPLAY_ORDER) + [c for c in markets_map if c not in COT_DISPLAY_ORDER]
    for code in codes:
        m = markets_map.get(code)
        if not m or not m.get("series"):
            gaps.append(f"COT模組：{code} 無資料")
            continue
        label = m.get("label", code)
        if code in EQUITY_THREE_PROXY:
            equity_label[code] = label
        s = sorted(tuple(pt) for pt in m["series"])
        dates = [d for d, _ in s]
        vals = [v for _, v in s]
        cur_date, cur_val = s[-1]
        if cot_as_of is None or cur_date > cot_as_of:
            cot_as_of = cur_date
        if len(vals) < COT_PCTILE_WINDOW_WEEKS:
            gaps.append(f"COT模組：{label} 3 年分位樣本僅 {len(vals)} 週"
                        f"（<{COT_PCTILE_WINDOW_WEEKS}），可信度隨資料累積提升")
        win = vals[-COT_PCTILE_WINDOW_WEEKS:]
        pct = pctile_incl(win, cur_val)
        extreme = None
        if pct is not None:
            if pct >= COT_EXTREME_HI:
                extreme = "stretched_long"
            elif pct <= COT_EXTREME_LO:
                extreme = "stretched_short"
        is_eq3 = code in EQUITY_THREE_PROXY
        markets_out.append({
            "code": code,
            "label": label,
            "net_pct_oi": rnd(cur_val, 2),
            "pctile_3y": pct,
            "pctile_window_n": len(win),
            "as_of": cur_date,
            "extreme": extreme,
            "is_equity_three": is_eq3,
            "proxy": EQUITY_THREE_PROXY.get(code),
        })

        if is_eq3:
            for i in range(COT_PCTILE_WINDOW_WEEKS - 1, len(vals)):
                w = vals[i - COT_PCTILE_WINDOW_WEEKS + 1:i + 1]
                p = pctile_incl(w, vals[i])
                if p is None:
                    continue
                if p >= COT_EXTREME_HI:
                    equity_events[code].append((dates[i], "long"))
                elif p <= COT_EXTREME_LO:
                    equity_events[code].append((dates[i], "short"))

    base_rate = _cot_base_rate(equity_events, equity_label, flowmap_series, gaps)

    return {
        "as_of": cot_as_of,
        "methodology": methodology,
        "pctile_window_weeks": COT_PCTILE_WINDOW_WEEKS,
        "extreme_thresholds": {"hi": COT_EXTREME_HI, "lo": COT_EXTREME_LO},
        "markets": markets_out,
        "base_rate": base_rate,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Statistical Properties Panel (statlab) daily builder")
    ap.add_argument("--skip-fetch", action="store_true",
                    help="offline: skip yfinance/stooq fetch, recompute from caches only")
    args = ap.parse_args()

    gaps = []

    price_series = build_price_cache(args.skip_fetch)

    spy_pts = price_series.get("SPY") or []
    if spy_pts:
        as_of = spy_pts[-1][0]
    else:
        as_of = date.today().isoformat()
        gaps.append("as_of：SPY 價格快取為空，退回今日日期")

    try:
        corr_out = correlation_module(price_series, gaps)
    except Exception as e:
        warn(f"correlation module failed: {e}")
        gaps.append(f"相關性模組：執行失敗（{str(e)[:120]}），輸出 null")
        corr_out = {"spy_tlt": None, "sector_avg_pairwise": None}

    try:
        vix_out = vix_term_module(price_series, gaps)
    except Exception as e:
        warn(f"vix term module failed: {e}")
        gaps.append(f"VIX期限結構模組：執行失敗（{str(e)[:120]}），輸出 null")
        vix_out = None

    cot_history = load_json(COT_HISTORY)
    flowmap_cache = load_json(FLOWMAP_PRICE_CACHE)
    flowmap_series = {}
    if flowmap_cache and isinstance(flowmap_cache.get("series"), dict):
        flowmap_series = {k: [tuple(pt) for pt in v] for k, v in flowmap_cache["series"].items()}
    else:
        gaps.append("COT模組：data/flowmap_prices.json 無法讀取，權益三指數 base rate 略過")

    try:
        cot_out = cot_module(cot_history, flowmap_series, gaps)
    except Exception as e:
        warn(f"cot module failed: {e}")
        gaps.append(f"COT模組：執行失敗（{str(e)[:120]}），輸出 null")
        cot_out = None

    payload = {
        "schema": SCHEMA,
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "correlation": corr_out,
        "vix_term": vix_out,
        "cot": cot_out,
        "gaps": gaps,
    }
    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"statlab latest.json {'written' if wrote else 'no change'}; gaps={len(gaps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
