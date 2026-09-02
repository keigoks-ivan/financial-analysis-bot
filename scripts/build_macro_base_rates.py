#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_macro_base_rates.py — macro 證偽表 producer 的 FRED 歷史快取與 climatology 引擎
（forecast ledger v2 §5.5 M 套件；設計稿 notes/site-internal/root/_forecast_v2_design_20260902.md）。

維護 data/macro_base_rates_raw_cache.json：FRED 全史（不切筆數，抓法照 scripts/build_monitor.py
的 fetch_fred——不帶自訂 UA，FRED 對「Mozilla/5.0 …」型偽瀏覽器字串會 stall；requests 預設 UA
反而正常回應）：

  DGS10（10Y 殖利率，%）、DGS30（30Y 殖利率，%）、BAMLH0A0HYM2（ICE BofA HY OAS，%）、
  THREEFYTP10（Kim–Wright 10Y term premium，%——注意這不是 NY Fed ACM，monitor 頁面把
  tp10y 標成「ACM」是既有標籤誤植，本檔與 harvest_macro_falsifiers.py 皆不修正 monitor 標籤，
  只在 harvest 的 note 註記，見設計稿 §9）、SOFR（%）、IORB（%）、DEXCHUS（USD/CNY 匯率）、
  T10YIE（10Y breakeven 通膨預期，%）。

另衍生一條非 FRED 直抓序列 sofr_iorb：(SOFR − IORB) × 100，單位＝bp，只取兩序列共同交易日
且 ≥ 2021-07-29（IORB 序列本身從這天開始，這也是設計稿 §5.5／§0 指定的起點）——這個 bp 尺度
刻意對齊 docs/monitor/data/latest.json 的 sofr_iorb 顯示值格式（"3bps" 這類字串），讓
harvest_macro_falsifiers.py 算 delta 時不必再做一次尺度換算。

另兩條衍生序列 core_pce_yoy／payems_3m（forecast v2 P2 設計稿 §6 item4，G4 包新增）：抓
PCEPILFE（核心 PCE 平減指數，月頻）與 PAYEMS（非農就業人數，月頻）全史後，衍生
core_pce_yoy＝(PCEPILFE_t／PCEPILFE_{t−12} − 1) × 100（12 期 YoY，%）、payems_3m＝最近 3 個月
ΔPAYEMS 平均（千人）——公式與 scripts/build_monitor_internals.py 的 yoy_series()／
mom_3mavg_series() 逐字一致（見 derive_core_pce_yoy()／derive_payems_3m()）。

另有一條非 FRED 序列 DXY（美元指數）：yfinance `DX-Y.NYB` 日收盤 ~20 年，stooq `dx.f`
連續期貨為 fallback（2026-09-02 實測：本機網路環境下 stooq CSV endpoint 一律回傳 JS
challenge 頁、非 CSV，即使對已知有效代碼如 spy.us 亦然——推測 stooq 現在全站擋爬蟲，此
fallback 保留供日後 stooq 恢復時使用，非本次驗證路徑）；兩者皆失敗時**不中止整個 raw cache
重建**，記錄缺口（series 缺失或沿用舊快取）即可——DXY 不是原本 6 條 FRED 序列之一，不應讓
它的抓取失敗拖垮 DGS10 等既有序列（見 fetch_dxy_series()）。

輸出 data/macro_base_rates.json：只存 meta（各序列起訖、n、built_at、視窗說明）——不預先算
好機率表，climatology() 由 harvest_macro_falsifiers.py 在 dry-run 時對 raw cache 即時呼叫
（設計稿原文：「climatology 由 harvest 即時呼叫」）。

climatology(key, op, delta, horizon_days) -> {"p": float|None, "n": int, "window": str, "series": str}
────────────────────────────────────────────────────────────────────────────────────────────
PREREG 凍結（設計稿 §5.5，sonnet 不得改）：
  * key ∈ {dgs10, dgs30, hy_oas, tp10y, sofr_iorb} → 對應快取序列（見 MONITOR_KEY_SERIES）。
    2026-09-02 F3（設計稿 §9 row F3／`_market_cockpit_design_20260902.md`）序列擴充新增
    key ∈ {dxy, usdcny, bei10y, t10yie}——沿用同一 climatology() 實作與 20 年窗／H_td／
    op 規則，不是新公式，只是 MONITOR_KEY_SERIES 多 4 個條目。
  * 樣本窗＝近 20 年（不足取全部）。
  * H_td = round(horizon_days × 252 / 365)（曆日轉交易日筆數，非交易日曆——與
    build_tsmom_base_rates.py／build_vrp_base_rates.py 的 t+N 筆處理方式一致：直接數序列筆數
    而非查真實交易日曆）。
  * op ">"（含 ">="）：對每個有完整未來 H_td 筆視窗的起點 t，命中＝max(x[t+1..t+H_td]) − x[t] ≥ delta。
  * op "<"（含 "<="）：命中＝min(x[t+1..t+H_td]) − x[t] ≤ delta。
  * p = hits / n（n＝可判斷起點數，非全樣本筆數）。
  * **MONTHLY_SERIES = {core_pce_yoy, payems_3m}**（2026-09-02 G4 新增，設計稿 P2 §6 item4）：
    這兩個 key 是月頻序列（非交易日），H 改為 max(1, round(horizon_days / 30.44)) 個觀測
    （曆日轉「月」筆數，30.44＝365.25/12）；樣本窗改為最近 240 個觀測（20 年×12 個月，不足取
    全部），取代日頻的「近 20 年」日期窗；op／命中規則不變（同上，只是視窗單位是觀測筆數而非
    交易日）。climatology() 回傳 dict 新增 `freq`："monthly"（MONTHLY_SERIES 成員）或
    "daily"（其餘 key）。

用法
----
  python scripts/build_macro_base_rates.py                 完整重抓 + 重建 raw cache + meta（預設）
  python scripts/build_macro_base_rates.py --skip-fetch     離線：只用既有本地 raw cache 重建 meta
  python scripts/build_macro_base_rates.py --if-due         data/macro_base_rates.json built_at
                                                              距今 <85 天則跳過（cron 用）
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from datetime import date as date_cls
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "macro_base_rates_raw_cache.json"
OUT_JSON = DATA / "macro_base_rates.json"

SCHEMA_RAW = "macro-base-rates-raw-v1"
SCHEMA_META = "macro-base-rates-v1"

FRED_SERIES = ["DGS10", "DGS30", "BAMLH0A0HYM2", "THREEFYTP10", "SOFR", "IORB",
               "DEXCHUS", "T10YIE", "PCEPILFE", "PAYEMS"]
                                               # DEXCHUS／T10YIE：2026-09-02 F3 新增，走既有
                                               # FRED 抓取／全數失敗即中止整批重建的既有行為
                                               # （不享受 DXY 的「record gap」特例，見檔頭）。
                                               # PCEPILFE／PAYEMS：2026-09-02 G4 新增（設計稿 P2
                                               # §6 item4），月頻，衍生 core_pce_yoy／payems_3m
                                               # （見 derive_core_pce_yoy()／derive_payems_3m()）。
SOFR_IORB_START = "2021-07-29"     # PREREG（設計稿 §5.5／§0）：IORB 序列本身從這天開始
LOOKBACK_YEARS = 20                # PREREG（設計稿 §5.5）：climatology 樣本窗（日頻 key）
MONTHLY_SERIES = {"core_pce_yoy", "payems_3m"}  # PREREG（設計稿 P2 §6 item4，G4 新增）：月頻
                                                 # climatology key 清單
MONTHLY_LOOKBACK_OBS = 240         # PREREG：月頻樣本窗＝240 個觀測（20 年×12 個月，不足取全部）
IF_DUE_MAX_AGE_DAYS = 85           # --if-due 門檻（比照 build_rv_base_rates.py 慣例）

DXY_YF_TICKER = "DX-Y.NYB"         # 2026-09-02 F3 新增：美元指數，非 FRED 序列
DXY_STOOQ_SYMBOL = "dx.f"          # stooq 連續期貨代碼（best-effort fallback，未驗證可用，見檔頭）
DXY_FETCH_PERIOD = "20y"           # 對齊 LOOKBACK_YEARS

# monitor key → (快取序列名, 顯示單位)。sofr_iorb 是本檔衍生序列（非 FRED 原始 id），
# 單位刻意用 bp 對齊 monitor latest.json 的 "3bps" 顯示格式。dxy/usdcny/bei10y/t10yie 為
# 2026-09-02 F3 新增（設計稿 §9 row F3）：dxy 對應非 FRED 的 DXY 快取序列（美元指數，無 %／bp
# 單位，直接是指數點數）；usdcny 對應 FRED DEXCHUS（USD/CNY 匯率，直接是匯率數字）；bei10y
# 與 t10yie 是同一條 FRED T10YIE（10Y breakeven 通膨預期，%）的兩個別名——kill_watch.json 對
# 這條門檻的 data_source.key 目前記作 macro/bei10y，未來若改用 t10yie 兩個 key 都能命中。
# core_pce_yoy／payems_3m 為 2026-09-02 G4 新增（設計稿 P2 §6 item4）：對應本檔衍生的月頻序列
# （非 FRED 原始 id，同 sofr_iorb 慣例），亦登記於 MONTHLY_SERIES（climatology() 走月頻分支）。
MONITOR_KEY_SERIES = {
    "dgs10": ("DGS10", "%"),
    "dgs30": ("DGS30", "%"),
    "hy_oas": ("BAMLH0A0HYM2", "%"),
    "tp10y": ("THREEFYTP10", "%"),
    "sofr_iorb": ("sofr_iorb", "bp"),
    "dxy": ("DXY", ""),
    "usdcny": ("DEXCHUS", "USD/CNY"),
    "bei10y": ("T10YIE", "%"),
    "t10yie": ("T10YIE", "%"),
    "core_pce_yoy": ("core_pce_yoy", "%"),
    "payems_3m": ("payems_3m", "K"),
}


def warn(msg: str) -> None:
    print(f"[macro-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[macro-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# FRED 抓取（抓法照 scripts/build_monitor.py 的 fetch_fred，但不切 400 筆）
# ═══════════════════════════════════════════════════════════════════════════

def fetch_fred_full(series_id: str) -> list | None:
    """FRED CSV endpoint（免 key），回傳升冪 [(date_iso, val), ...] 或 None。

    刻意不帶自訂 User-Agent——build_monitor.py 已實測「Mozilla/5.0 …」型偽瀏覽器字串會讓
    FRED stall（read timeout），requests 預設 UA 反而正常回應；本檔沿用同一慣例。
    與 build_monitor.fetch_fred 的唯一差異：這裡不做 `[-400:]` 截斷，要全史。
    """
    import requests
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
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
    return pts or None


def fetch_all_series(skip_fetch: bool) -> dict:
    """回傳 {series_id: [(date, val), ...]}（升冪）。skip_fetch=True 時只讀既有 raw cache。"""
    cache = {}
    if RAW_CACHE.exists():
        try:
            cache = json.loads(RAW_CACHE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read {RAW_CACHE.name}: {e}")
            cache = {}
    series = cache.get("series", {})

    if skip_fetch:
        missing = [sid for sid in FRED_SERIES if not series.get(sid)]
        if missing:
            raise SystemExit(f"--skip-fetch 但 {RAW_CACHE} 缺 {missing}，無法離線重建")
        return {sid: [(d, v) for d, v in series[sid]] for sid in FRED_SERIES}

    out = {}
    failed = []
    for sid in FRED_SERIES:
        bars = None
        for attempt in range(3):
            bars = fetch_fred_full(sid)
            if bars:
                break
        if not bars:
            # 抓不到就退回既有快取（若有），不整批中止——單一序列上游故障不該擋掉其餘序列
            existing = series.get(sid)
            if existing:
                warn(f"{sid}: 全部重試失敗，沿用既有快取（{len(existing)} 筆，可能過期）")
                out[sid] = [(d, v) for d, v in existing]
                continue
            failed.append(sid)
            continue
        info(f"{sid}: fetched {len(bars)} obs ({bars[0][0]} .. {bars[-1][0]})")
        out[sid] = bars

    if failed:
        raise SystemExit(f"以下序列抓取全數失敗且無既有快取可退回，中止：{failed}")

    return out


def derive_sofr_iorb(series: dict) -> list:
    """(SOFR − IORB) × 100，單位 bp，只取兩序列共同交易日且 ≥ SOFR_IORB_START。"""
    sofr = dict(series.get("SOFR", []))
    iorb = dict(series.get("IORB", []))
    common_dates = sorted(d for d in (set(sofr) & set(iorb)) if d >= SOFR_IORB_START)
    return [(d, round((sofr[d] - iorb[d]) * 100, 4)) for d in common_dates]


def derive_core_pce_yoy(series: dict) -> list:
    """PCEPILFE 12 期 YoY（%）＝(PCEPILFE_t／PCEPILFE_{t−12} − 1) × 100。公式與
    scripts/build_monitor_internals.py::yoy_series() 逐字一致（2026-09-02 G4 新增，設計稿 P2
    §6 item4）。"""
    pts = series.get("PCEPILFE", [])
    out = []
    for i in range(12, len(pts)):
        d, v = pts[i]
        _, v12 = pts[i - 12]
        if v12:
            out.append((d, round((v / v12 - 1) * 100, 4)))
    return out


def derive_payems_3m(series: dict) -> list:
    """PAYEMS 月增的 3 個月移動平均（單位千人）。公式與
    scripts/build_monitor_internals.py::mom_3mavg_series() 逐字一致（2026-09-02 G4 新增，
    設計稿 P2 §6 item4）。"""
    pts = series.get("PAYEMS", [])
    diffs = [(pts[i][0], pts[i][1] - pts[i - 1][1]) for i in range(1, len(pts))]
    out = []
    for i in range(2, len(diffs)):
        w = [diffs[i - 2][1], diffs[i - 1][1], diffs[i][1]]
        out.append((diffs[i][0], round(sum(w) / 3, 2)))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# DXY 抓取（yfinance -> stooq fallback；非 FRED，獨立實作，照抄
# scripts/build_dd_verdict_base_rates.py 的 _yf_daily／_stooq_daily 慣例。2026-09-02 F3 新增，
# 見檔頭「另有一條非 FRED 序列 DXY」說明：兩者皆敗時記錄缺口，不中止整批 raw cache 重建）
# ═══════════════════════════════════════════════════════════════════════════

def _yf_daily_close(ticker: str, period: str) -> list | None:
    import yfinance as yf
    df = yf.download(ticker, period=period, interval="1d", auto_adjust=True,
                      progress=False, threads=False)
    if df is None or df.empty:
        return None
    close = df["Close"]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
    rows = []
    for idx, val in close.items():
        try:
            c = float(val)
        except (TypeError, ValueError):
            continue
        if c != c:  # NaN
            continue
        rows.append((idx.date().isoformat(), round(c, 4)))
    return rows or None


def _stooq_daily(symbol: str) -> list | None:
    """symbol 須已是 stooq 慣用代碼（如 'dx.f'），呼叫端不補 .us 綴。"""
    import requests
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0 macro-base-rates"})
        r.raise_for_status()
        raw = r.text
    except Exception as e:
        warn(f"stooq fetch failed for {symbol}: {e}")
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


def fetch_dxy_series(skip_fetch: bool, existing_cache_series: dict) -> list:
    """DXY：yfinance → stooq fallback → 兩者皆敗記錄缺口（回傳既有快取或空 list，絕不
    SystemExit——DXY 不在原 6 條 FRED 序列之列，見檔頭）。"""
    existing = existing_cache_series.get("DXY") or []
    if skip_fetch:
        if not existing:
            warn("--skip-fetch 且 raw cache 無既有 DXY 快取——climatology(key='dxy', ...) 之後會 n=0")
        return [(d, v) for d, v in existing]

    got, src = None, None
    for attempt in range(3):
        try:
            got = _yf_daily_close(DXY_YF_TICKER, period=DXY_FETCH_PERIOD)
            if got:
                src = "yfinance"
                break
        except Exception as e:
            warn(f"DXY yfinance attempt {attempt + 1} failed: {e}")
    if not got:
        got = _stooq_daily(DXY_STOOQ_SYMBOL)
        if got:
            src = "stooq"
    if not got:
        if existing:
            warn(f"DXY 抓取全數失敗（yfinance + stooq），沿用既有快取（{len(existing)} 筆，"
                 f"至 {existing[-1][0]}）")
            return [(d, v) for d, v in existing]
        warn("DXY 抓取全數失敗（yfinance + stooq）且無既有快取——記錄缺口（series 留空），"
             "climatology(key='dxy', ...) 之後會 n=0，不中止整批 raw cache 重建")
        return []

    info(f"DXY: fetched {len(got)} obs via {src} ({got[0][0]} .. {got[-1][0]})")
    merged = {d: v for d, v in existing}
    for d, v in got:
        merged[d] = v
    return sorted(merged.items())


def build_raw_cache(skip_fetch: bool) -> dict:
    existing_cache_series = {}
    if RAW_CACHE.exists():
        try:
            existing_cache_series = json.loads(RAW_CACHE.read_text(encoding="utf-8")).get("series", {})
        except (OSError, json.JSONDecodeError):
            existing_cache_series = {}

    series = fetch_all_series(skip_fetch)
    series["sofr_iorb"] = derive_sofr_iorb(series)
    if not series["sofr_iorb"]:
        warn("sofr_iorb 衍生序列為空（SOFR／IORB 無共同交易日 ≥ "
             f"{SOFR_IORB_START}）——climatology(key='sofr_iorb', ...) 之後會回傳 n=0")
    series["core_pce_yoy"] = derive_core_pce_yoy(series)
    if not series["core_pce_yoy"]:
        warn("core_pce_yoy 衍生序列為空（PCEPILFE 筆數不足 12 期）——"
             "climatology(key='core_pce_yoy', ...) 之後會回傳 n=0")
    series["payems_3m"] = derive_payems_3m(series)
    if not series["payems_3m"]:
        warn("payems_3m 衍生序列為空（PAYEMS 筆數不足）——"
             "climatology(key='payems_3m', ...) 之後會回傳 n=0")
    series["DXY"] = fetch_dxy_series(skip_fetch, existing_cache_series)

    cache = {
        "schema": SCHEMA_RAW,
        "series": {sid: [[d, v] for d, v in pts] for sid, pts in series.items()},
        "meta": {
            "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "note": ("build_macro_base_rates.py 專用 FRED 快取（DGS10/DGS30/"
                     "BAMLH0A0HYM2/THREEFYTP10/SOFR/IORB/DEXCHUS/T10YIE/PCEPILFE/PAYEMS 全史 + "
                     "衍生 sofr_iorb bp 序列 + 衍生 core_pce_yoy／payems_3m 月頻序列 + 非 FRED 的 "
                     "DXY 美元指數序列），手動／--if-due 重建，非逐日 cron。"),
        },
    }
    RAW_CACHE.parent.mkdir(parents=True, exist_ok=True)
    RAW_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                         encoding="utf-8")
    return cache


# ═══════════════════════════════════════════════════════════════════════════
# climatology()（PREREG 凍結；harvest_macro_falsifiers.py 即時呼叫）
# ═══════════════════════════════════════════════════════════════════════════

def _shift_years(iso_date: str, years_delta: int) -> str:
    d = date_cls.fromisoformat(iso_date)
    try:
        return d.replace(year=d.year + years_delta).isoformat()
    except ValueError:
        # 2/29 落在非閏年目標年份 —— 退回 2/28
        return d.replace(year=d.year + years_delta, day=28).isoformat()


def _load_raw_series(cache_path: Path = RAW_CACHE) -> dict:
    if not cache_path.exists():
        return {}
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return cache.get("series", {})


def climatology(key: str, op: str, delta: float, horizon_days: int,
                 cache_path: Path = RAW_CACHE) -> dict:
    """PREREG 凍結公式，見檔頭。key 為 monitor 域 key（dgs10/dgs30/hy_oas/tp10y/sofr_iorb 等），
    非 FRED series id。op ∈ {">", ">=", "<", "<="}；delta 帶號＝門檻 − 現值，單位與快取序列
    一致（dgs10/dgs30/hy_oas/tp10y 為 %，sofr_iorb 為 bp）。key ∈ MONTHLY_SERIES（core_pce_yoy／
    payems_3m）走月頻分支（見檔頭 PREREG 段），回傳 dict 多一個 `freq` 欄位。"""
    mapped = MONITOR_KEY_SERIES.get(key)
    if mapped is None:
        raise ValueError(f"climatology: 未知 monitor key={key!r}（僅支援 {sorted(MONITOR_KEY_SERIES)}）")
    series_name, unit = mapped
    freq = "monthly" if key in MONTHLY_SERIES else "daily"

    all_series = _load_raw_series(cache_path)
    rows = all_series.get(series_name)
    if not rows:
        return {"p": None, "n": 0, "window": f"{series_name}：raw cache 無資料（未 build 或序列為空）",
                "series": series_name, "freq": freq}

    dates = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    n_total = len(vals)
    if n_total < 2:
        return {"p": None, "n": 0, "window": f"{series_name}：樣本不足（僅 {n_total} 筆）",
                "series": series_name, "freq": freq}

    op_eff = ">" if op in (">", ">=") else "<"
    if freq == "monthly":
        start_i = max(0, n_total - MONTHLY_LOOKBACK_OBS)
        H_td = max(1, round(horizon_days / 30.44))
    else:
        cutoff = _shift_years(dates[-1], -LOOKBACK_YEARS)
        start_i = bisect.bisect_left(dates, cutoff)
        H_td = max(1, round(horizon_days * 252 / 365))

    hits = 0
    count = 0
    for t in range(start_i, n_total):
        end = t + H_td
        if end >= n_total:
            break
        window_vals = vals[t + 1:t + H_td + 1]
        if len(window_vals) != H_td:
            continue
        if op_eff == ">":
            hit = (max(window_vals) - vals[t]) >= delta
        else:
            hit = (min(window_vals) - vals[t]) <= delta
        count += 1
        if hit:
            hits += 1

    p = (hits / count) if count else None
    if freq == "monthly":
        window_desc = (f"{series_name} 最近 {n_total - start_i} 個觀測（月頻，不足取全部，"
                        f"實際取樣 {dates[start_i]}..{dates[-1]}）、"
                        f"H={H_td} 個月觀測視窗（horizon_days={horizon_days}÷30.44 四捨五入）、"
                        f"op={op_eff}、delta={delta}{unit}")
    else:
        window_desc = (f"{series_name} 近{LOOKBACK_YEARS}年（不足取全部，實際取樣 "
                        f"{dates[start_i]}..{dates[-1] if start_i < n_total else dates[-1]}）、"
                        f"H_td={H_td} 交易日視窗（horizon_days={horizon_days}×252/365 四捨五入）、"
                        f"op={op_eff}、delta={delta}{unit}")
    return {"p": p, "n": count, "window": window_desc, "series": series_name, "freq": freq}


# ═══════════════════════════════════════════════════════════════════════════
# meta 輸出（只存起訖／n，不存機率表）
# ═══════════════════════════════════════════════════════════════════════════

def build_meta(cache: dict, out_path: Path) -> dict:
    series = cache.get("series", {})
    series_meta = {}
    for sid, rows in series.items():
        if not rows:
            series_meta[sid] = {"start": None, "end": None, "n": 0}
            continue
        series_meta[sid] = {"start": rows[0][0], "end": rows[-1][0], "n": len(rows)}

    meta = {
        "schema": SCHEMA_META,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "raw_cache_built_at": cache.get("meta", {}).get("built_at"),
        "series_meta": series_meta,
        "monitor_key_series": {k: {"series": v[0], "unit": v[1]} for k, v in MONITOR_KEY_SERIES.items()},
        "climatology_window_note": (
            f"climatology(key, op, delta, horizon_days) 對每個 monitor key 對應的快取序列，"
            f"取近 {LOOKBACK_YEARS} 年（不足取全部）逐點為起點 t，H_td=round(horizon_days×252/365) "
            "為未來視窗交易筆數；op='>' 命中＝視窗內最大值−當前值≥delta，op='<' 命中＝視窗內"
            "最小值−當前值≤delta；p=命中數/可判斷起點數。本檔不預先算表——climatology() 由 "
            "scripts/harvest_macro_falsifiers.py 對 raw cache 即時呼叫，此 JSON 只存 meta 供人工核對。"
        ),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    return meta


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="macro 證偽表 producer：FRED 歷史快取 + climatology 引擎")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地 raw cache 重建 meta")
    ap.add_argument("--out", default=str(OUT_JSON), help="meta 輸出路徑（測試用；預設 data/macro_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有 --out 路徑 built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建（cron 用）")
    args = ap.parse_args()
    out_path = Path(args.out)

    if args.if_due:
        if out_path.exists():
            try:
                existing = json.loads(out_path.read_text(encoding="utf-8"))
                built_at = existing.get("built_at")
                if built_at:
                    built_dt = datetime.strptime(built_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    age_days = (datetime.now(timezone.utc) - built_dt).total_seconds() / 86400.0
                    if age_days < IF_DUE_MAX_AGE_DAYS:
                        info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）< "
                             f"{IF_DUE_MAX_AGE_DAYS} 天門檻，not due，本次不重建")
                        return
                    info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）≥ "
                         f"{IF_DUE_MAX_AGE_DAYS} 天門檻，due，繼續重建")
                else:
                    info(f"--if-due: {out_path} 無 built_at 欄位，視為需要重建")
            except (OSError, json.JSONDecodeError, ValueError) as e:
                warn(f"--if-due: 無法讀取/解析既有 {out_path}（{e}），視為需要重建")
        else:
            info(f"--if-due: {out_path} 不存在，視為需要重建")

    cache = build_raw_cache(args.skip_fetch)
    meta = build_meta(cache, out_path)

    info(f"wrote {RAW_CACHE}")
    info(f"wrote {out_path}")
    for sid, m in meta["series_meta"].items():
        info(f"  {sid:<14} n={m['n']:<6} {m['start']} .. {m['end']}")


if __name__ == "__main__":
    main()
