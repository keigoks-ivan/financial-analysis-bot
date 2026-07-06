#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cross-Asset Regime Dashboard — weekly data pipeline.

Sibling of build_crowding.py / build_rotation.py.  Refreshes the *mechanical*
layers of the regime dashboard while PRESERVING the *editorial* layer.

Mechanical (recomputed every run)
---------------------------------
  * COT positioning extremes — 5y inclusive percentile / net direction /
    stretched flags, derived from data/cot_history.json (read-only, maintained
    by build_crowding.py).  No CFTC download here; we consume the shared cache.
  * Three growth-vs-defence ratios — copper/gold (HG=F / GC=F), HY/IG
    (HYG / LQD), small/large (IWM / SPY): current value, 12m change, and 2y
    inclusive percentile.  Prices via yfinance -> stooq fallback, cached
    incrementally in data/regime_prices.json.

Editorial (carried from the Vol.1 pilot; NEVER overwritten by mechanical)
------------------------------------------------------------------------
  * Six-axis regime scorecard marker positions + one-line reads + pills.
  * Composite (qualitative) read.
  * Trigger / monitoring table.
  * USD July turn correction (COT stops 2026-06-23, spot already rolled over —
    labelled as-of, not overwritten by the raw COT percentile).
  NB: the small/large and HY/IG axis markers are editorial (set from 12m
  relative return / OAS percentile), NOT the raw ratio 2y percentile.  The
  mechanical ratio metrics are stored alongside as a separate sub-object so the
  two layers stay distinct.

Outputs
-------
  docs/regime/data/latest.json  — contract JSON (zero-churn).
  docs/regime/index.html        — compact scorecard dashboard injected between
                                  the REGIME_AUTO_DASH_START / _END markers.
  (The Vol.1 snapshot REGIME_20260706.html is frozen; this script never
  regenerates it.)

CLI
---
  python scripts/build_regime.py            full weekly refresh (default)
  python scripts/build_regime.py --skip-fetch   offline: recompute from caches

Design contracts (identical to build_crowding.py / build_rotation.py)
---------------------------------------------------------------------
  * Zero churn: JSON emitted sorted-keys + fixed decimals; volatile timestamp
    fields stripped before the on-disk compare, so a no-op run writes nothing.
  * data/cot_history.json and data/weekly_cache are read-only here.
  * Fault tolerance: price fetch is warn-and-continue with cache fallback; the
    process exits non-zero only if it can produce neither COT nor ratio layer.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
COT_HISTORY = os.path.join(DATA, "cot_history.json")
PRICE_CACHE = os.path.join(DATA, "regime_prices.json")
OUT_DIR = os.path.join(ROOT, "docs", "regime")
OUT_JSON = os.path.join(OUT_DIR, "data", "latest.json")
INDEX_HTML = os.path.join(OUT_DIR, "index.html")
SNAPSHOT_LATEST = "REGIME_20260706.html"
DASH_START = "<!-- REGIME_AUTO_DASH_START -->"
DASH_END = "<!-- REGIME_AUTO_DASH_END -->"


def warn(msg: str) -> None:
    print(f"[regime][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[regime] {msg}")


# ───────────────────────────────────────────────────────────────────────────
# Zero-churn IO (identical protocol to the sibling builders)
# ───────────────────────────────────────────────────────────────────────────

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


def write_json_if_changed(path, obj, volatile=("generated_at", "built_at")) -> bool:
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


def pctile_incl(values, x):
    """Inclusive percentile rank (fraction of values <= x), 0..100."""
    v = [z for z in values if z is not None]
    n = len(v)
    if n == 0 or x is None:
        return None
    return round(100.0 * sum(1 for z in v if z <= x) / n, 1)


def rnd(v, d):
    if v is None:
        return None
    try:
        return round(float(v), d)
    except (TypeError, ValueError):
        return None


# ═══════════════════════════════════════════════════════════════════════════
# EDITORIAL LAYER — carried verbatim from the Vol.1 pilot.  A human refreshes
# these; the mechanical layers below MUST NOT overwrite them.
# ═══════════════════════════════════════════════════════════════════════════

AXES = [
    dict(key="rates", name="利率／久期", sub="Rates / Duration", pos=0.56,
         trail=None, pill="中性偏暖", pillcls="warm", short="升息路徑降溫，久期逆風轉緩",
         reading="10Y 4.47%（7/2），弱非農後由 4.53% 回落；9 月升息機率 64%→55%。COT 公債各天期仍淨空（10Y 5y 第 24.6、30Y 20.8 百分位），升息路徑降溫、久期逆風轉緩。",
         src="10Y CNBC/dshort 2026-07-02 · CFTC COT 2026-06-23 · TLT/IEF yfinance 2026-07-05"),
    dict(key="usd", name="美元", sub="US Dollar", pos=0.62, trail=0.38,
         pill="轉暖／翻向", pillcls="turn", short="擁擠做多，翻向回落",
         reading="COT 美元淨多 4 週暴增 +21.5pp 至 6/23（擁擠做多），7/2 弱非農後 DXY 由 101.5 跌破 101（100.8）翻向回落。UUP 2y 動能第 98 百分位為全資產最延伸——極端多頭遇催化劑正在鬆動，對非美／EM／商品由逆風轉順風。",
         src="COT DX 2026-06-23（Δ4w +21.53）· DXY tradingeconomics 2026-07-03 · UUP yfinance 2026-07-05"),
    dict(key="credit", name="信用", sub="Credit (HY vs IG)", pos=0.78,
         trail=None, pill="偏暖", pillcls="warm", short="HY spread 偏緊，胃納完好",
         reading="HY OAS 2.78%（6/25），落在 10 年區間第 17 百分位（歷史性偏緊）；IG OAS ~80bp。HYG 站上 52 週均線 +1.9%，信用胃納完好——本表最明確的 risk-on 軸；惟 spread 已現微幅走闊的早警。",
         src="ICE BofA HY OAS FRED 2026-06-25 · HYG/LQD yfinance 2026-07-05"),
    dict(key="growth", name="成長 vs 恐慌", sub="Growth vs Fear", pos=0.64,
         trail=None, pill="偏暖", pillcls="warm", short="循環／小型領先，中段偏暖",
         reading="銅金比 2y 第 56 百分位、近 13 週上行（成長訊號回溫）；小型股領先大型（IWM +34.8% vs SPY +20.4%，12m）。但黃金 COT 第 86 百分位同步偏多——再通脹與避險同時被買，屬「什麼都漲」的晚週期形狀。",
         src="銅金比 yfinance 2y 週線 2026-07-06 · IWM/SPY yfinance 2026-07-05 · Gold COT 2026-06-23"),
    dict(key="equity", name="股票風險胃納", sub="Equity Risk Appetite", pos=0.50,
         trail=None, pill="中性", pillcls="mid", short="皮平靜、骨防禦",
         reading="表面平靜——VIX 偏低、VIX 期貨淨空（5y 第 29.6 百分位）；但水面下偏防禦：Nasdaq-100 COT 淨空落在 5y 第 8.1 百分位（極端偏空），IBIT 12m −43.9% 高 β 投機軌已斷。平靜的皮、防禦的骨。",
         src="Nasdaq/VIX COT 2026-06-23 · IBIT yfinance 2026-07-05"),
    dict(key="commod", name="商品", sub="Commodities", pos=0.70,
         trail=None, pill="偏暖但擁擠", pillcls="warmx", short="金屬買盤沉重但擁擠",
         reading="金屬買盤沉重但擁擠：銅 COT 5y 第 96.9 百分位（極端做多、觸旗）、黃金 86.2、白銀 48.5；WTI 原油僅第 10.4 百分位（能源被落下）。再通脹由金屬與 AI 電氣化主導，非廣度能源——多頭已高度擁擠，去化風險升。",
         src="Copper/Gold/Silver/WTI COT 2026-06-23 · USO yfinance 2026-07-05"),
]

TRIGGERS = [
    dict(ax="利率／久期", off="10Y 收上 4.7% 或升息機率回升", on="10Y 跌破 4.2% 或轉降息預期",
         now="4.47%、升息機率 55%，路徑降溫（偏暖）"),
    dict(ax="美元", off="DXY 收復 102、COT 淨多續增", on="DXY 確認跌破 100、COT 淨多去化",
         now="100.8、COT 仍擁擠多頭，翻向初期（轉暖）"),
    dict(ax="信用", off="HY OAS 走闊上破 3.5%", on="HY OAS 維持 3% 以下",
         now="2.78%、第 17 百分位偏緊，微幅早警（偏暖）"),
    dict(ax="成長 vs 恐慌", off="銅金比轉跌、黃金獨強", on="銅金比上破前高、小型續領先",
         now="銅金比 56 百分位上行（偏暖）"),
    dict(ax="股票胃納", off="VIX 上破 20、Nasdaq 空頭回補失敗", on="Nasdaq 極端空頭軋空、VIX 續低",
         now="VIX 低但 Nasdaq 部位防禦（中性）"),
    dict(ax="商品", off="銅 COT 自 97 百分位擁擠去化", on="現貨續創高且部位不再增溫",
         now="銅第 96.9 百分位極端擁擠，脆（偏暖但擁擠）"),
]

COMPOSITE = {"pos": 0.63, "label_zh": "晚週期再通脹 · 美元見頂回落",
             "label_en": "Late-cycle reflation, dollar rolling over",
             "method": "qualitative weighted read across 6 axes; not a tradable index"}

# Editorial ratio markers (pos_0to1 set from 12m relative return / OAS
# percentile — NOT the raw 2y ratio percentile).  Mechanical value / 12m /
# 2y-pctile are attached separately at build time.
RATIOS_EDITORIAL = [
    dict(key="copper_gold", name="銅／金比", sub="Copper / Gold", pos=0.56,
         num="HG=F", den="GC=F",
         reading="2y 第 56 百分位，近 13 週上行 — 成長脈動回溫、中段偏成長",
         src="yfinance HG=F / GC=F 2y 週線"),
    dict(key="small_large", name="小型／大型", sub="Russell 2000 / S&P 500", pos=0.74,
         num="IWM", den="SPY",
         reading="小型明顯領先，IWM +34.8% vs SPY +20.4%（12m）— 循環／廣度領導，risk-on",
         src="IWM/SPY yfinance 2y 週線"),
    dict(key="hy_ig", name="高收益／投等", sub="HY / IG credit", pos=0.60,
         num="HYG", den="LQD",
         reading="HY OAS 2.78%（10y 第 17 百分位，偏緊）、HYG 站上均線 — 信用胃納存，惟動能百分位低",
         src="ICE BofA HY OAS · HYG/LQD yfinance 2y 週線"),
]

META_EDITORIAL = {
    "title": "Cross-Asset Regime Dashboard",
    "vol": 1,
    "publish_date": "2026-07-06",
    "macro_as_of": "2026-07-03",
    "etf_as_of": "2026-07-05",
    "note": "Describer, not a timing/allocation signal. Composite axis is qualitative, not a tradable index. Mechanical layers (COT percentiles, ratio metrics) refresh weekly; six-axis markers / composite / triggers are editorial.",
    "cot_note": "6/30 CFTC report delayed by US holiday; latest available 2026-06-23. USD/rates July turn confirmed on spot, not yet in COT.",
}

GAPS = [
    "COT 停在 2026-06-23（6/30 期因美國國慶假期順延未發布）；美元／利率軸的 7 月初翻向以現貨與殖利率確認，COT 尚未捕捉。",
    "無 prime-brokerage 實際曝險資料（GS/MS PB），positioning 僅以 CFTC 大額投機 ＋ ETF 動能三角，機構真實槓桿不可見。",
    "銅金比、HY/IG、小型/大型為現貨比率代理，非官方 regime 指數；六軸 marker 位置與合成軸為定性判讀，非量化模型。",
    "信用以 HY/IG OAS 與 HYG/LQD 代理，無 CDX／單一券種細部；spread 微幅走闊的早警訊號樣本短。",
]

# ═══════════════════════════════════════════════════════════════════════════
# MECHANICAL LAYER 1 — COT positioning extremes (from cot_history.json)
# ═══════════════════════════════════════════════════════════════════════════

# (cftc_code, 中文顯示名, 群組).  Curated 13-market regime slate (drops EUR /
# Russell from the crowding 15).  Matched by stable CFTC contract code.
REGIME_COT_MARKETS = [
    ("085692", "銅 Copper", "商品"),
    ("088691", "黃金 Gold", "商品"),
    ("13874A", "S&P 500", "股指"),
    ("044601", "美國 5Y 公債", "利率"),
    ("084691", "白銀 Silver", "商品"),
    ("098662", "美元指數 DX", "外匯"),
    ("042601", "美國 2Y 公債", "利率"),
    ("097741", "日圓 JPY", "外匯"),
    ("1170E1", "VIX 期貨", "波動"),
    ("043602", "美國 10Y 公債", "利率"),
    ("020601", "美國 30Y 公債", "利率"),
    ("067651", "WTI 原油", "商品"),
    ("209742", "Nasdaq-100", "股指"),
]


def cot_compute(history):
    """Derive the current positioning table from the shared cot_history cache.
    Returns (rows_sorted_by_p5_desc, latest_as_of, gaps)."""
    if not history or "markets" not in history:
        return [], None, ["COT: data/cot_history.json 缺失或格式異常，部位層跳過"]
    rows, gaps, latest = [], [], None
    for code, zh, grp in REGIME_COT_MARKETS:
        m = history["markets"].get(code)
        if not m or not m.get("series"):
            gaps.append(f"COT {zh}（{code}）：無資料")
            continue
        s = sorted(m["series"])
        vals = [v for _, v in s]
        cur_date, cur_val = s[-1]
        if latest is None or cur_date > latest:
            latest = cur_date
        win5 = vals[-260:]
        p5 = pctile_incl(win5, cur_val)
        i4 = len(vals) - 1 - 4
        d4 = rnd(cur_val - vals[i4], 2) if i4 >= 0 else None
        net = "淨多" if cur_val > 0 else ("淨空" if cur_val < 0 else "中性")
        flag = None
        if p5 is not None:
            if p5 >= 90:
                flag = "極端做多"
            elif p5 <= 10:
                flag = "極端偏空"
        if len(win5) < 150:
            gaps.append(f"COT {zh}：5y 樣本僅 {len(win5)} 週（<150），百分位可信度打折")
        rows.append({"market": zh, "group": grp, "pctile_5y": p5, "net": net,
                     "extreme": flag, "delta_4w_pp_oi": d4})
    rows.sort(key=lambda r: (r["pctile_5y"] is not None, r["pctile_5y"]), reverse=True)
    return rows, latest, gaps


# ═══════════════════════════════════════════════════════════════════════════
# MECHANICAL LAYER 2 — growth-vs-defence ratio metrics (yfinance -> stooq)
# ═══════════════════════════════════════════════════════════════════════════

RATIO_SYMBOLS = ["HG=F", "GC=F", "HYG", "LQD", "IWM", "SPY"]
STOOQ_OK = {"HYG", "LQD", "IWM", "SPY"}  # futures don't serve cleanly on stooq


def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout,
                         headers={"User-Agent": "Mozilla/5.0 regime-monitor"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 regime-monitor"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


def _yf_weekly(tickers, period="3y"):
    """Batch weekly close download -> {ticker: [(week_end, close), ...]}."""
    import yfinance as yf
    import pandas as pd
    out = {}
    if not tickers:
        return out
    df = yf.download(tickers, period=period, interval="1wk", auto_adjust=True,
                     group_by="ticker", threads=True, progress=False)
    single = len(tickers) == 1
    for tk in tickers:
        try:
            sub = df if single else df[tk]
            close = sub["Close"] if not single else sub["Close"]
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


def _stooq_weekly(ticker):
    sym = ticker.lower()
    if "." not in sym:
        sym = sym + ".us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=w"
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
    """Incrementally refresh data/regime_prices.json.  Returns
    {symbol: [(week_end, close), ...]} (possibly from cache alone)."""
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
        missing = [t for t in RATIO_SYMBOLS if not series.get(t)]
        existing = [t for t in RATIO_SYMBOLS if series.get(t)]
        for label, batch, period in (("bootstrap", missing, "3y"),
                                     ("topup", existing, "3mo")):
            for i in range(0, len(batch), 6):
                chunk = batch[i:i + 6]
                got = None
                for attempt in range(3):
                    try:
                        got = _yf_weekly(chunk, period=period)
                        if got:
                            break
                    except Exception as e:
                        warn(f"yfinance {label} chunk {i//6} attempt {attempt+1} failed: {e}")
                if got:
                    fetched.update(got)
            info(f"prices {label}: requested {len(batch)}, got "
                 f"{sum(1 for t in batch if t in fetched)}")
        for t in RATIO_SYMBOLS:
            if t in fetched or series.get(t) or t not in STOOQ_OK:
                continue
            s = _stooq_weekly(t)
            if s:
                fetched[t] = s
                info(f"prices stooq fallback: {t} ({len(s)} wks)")

    for t, rows in fetched.items():
        merged = {d: c for d, c in series.get(t, [])}
        for d, c in rows:
            merged[d] = c
        series[t] = sorted(merged.items())

    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "symbols": RATIO_SYMBOLS,
        "note": "weekly close cache for regime growth/defence ratios; "
                "yfinance->stooq (ETFs only); incremental.",
    }
    wrote = write_json_if_changed(PRICE_CACHE, cache)
    n = {t: len(series.get(t, [])) for t in RATIO_SYMBOLS}
    info(f"price cache: {n}, {'written' if wrote else 'no change'}")
    return {t: [(d, c) for d, c in series.get(t, [])] for t in RATIO_SYMBOLS}


def _ratio_series(num_pts, den_pts):
    """Align two weekly close series on common week_end and return
    [(date, num/den), ...] sorted."""
    dn = dict(num_pts)
    dd = dict(den_pts)
    common = sorted(set(dn) & set(dd))
    out = []
    for d in common:
        den = dd[d]
        if den:
            out.append((d, dn[d] / den))
    return out


def ratio_compute(price_series):
    """Attach mechanical {value, chg_12m_pct, pctile_2y, as_of} to each
    editorial ratio.  Returns (ratios_out, gaps)."""
    ratios, gaps = [], []
    for r in RATIOS_EDITORIAL:
        entry = {k: r[k] for k in ("key", "name", "sub", "reading", "src")}
        entry["pos_0to1"] = r["pos"]
        num_pts = price_series.get(r["num"]) or []
        den_pts = price_series.get(r["den"]) or []
        rs = _ratio_series(num_pts, den_pts)
        mech = {"value": None, "chg_12m_pct": None, "pctile_2y": None, "as_of": None}
        if len(rs) >= 53:
            vals = [v for _, v in rs]
            mech["as_of"] = rs[-1][0]
            mech["value"] = rnd(vals[-1], 4)
            if vals[-53]:
                mech["chg_12m_pct"] = rnd((vals[-1] / vals[-53] - 1) * 100, 1)
            mech["pctile_2y"] = pctile_incl(vals[-104:], vals[-1])
        else:
            gaps.append(f"比率 {r['name']}：對齊週數僅 {len(rs)}（<53），機械指標不足")
        entry["mechanical"] = mech
        ratios.append(entry)
    return ratios, gaps


# ═══════════════════════════════════════════════════════════════════════════
# DASHBOARD — self-contained dark scorecard thumbnail (mirrors rotation card)
# ═══════════════════════════════════════════════════════════════════════════

# dark-card palette (self-contained; independent of page theme vars)
_C = dict(bg="#12161f", border="#2a3242", ink1="#e6e9ef", ink2="#9aa4b5",
          ink3="#6b7484", roff="#5b9bff", rmid="#3a4351", ron="#e0a256")
_PILL = {"warm": "#c78a2c", "warmx": "#b3801f", "turn": "#9085e9",
         "mid": "#6b7280", "cool": "#5b9bff"}


def _esc(s):
    import html
    return html.escape(str(s))


def _pillw(s):
    return 16 + len(s) * 12.0


def svg_scorecard():
    """Compact six-axis regime scorecard for the index dashboard (dark)."""
    W = 900
    rowH, top = 48, 56
    n = len(AXES)
    H = top + n * rowH + 62
    lx = 168          # label right edge
    tx0, tw = 186, 356
    rx0 = tx0 + tw + 24
    p = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="system-ui,-apple-system,sans-serif" role="img" '
         f'aria-label="六軸 regime 記分卡">']
    p.append('<defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{_C["roff"]}"/>'
             f'<stop offset="0.5" stop-color="{_C["rmid"]}"/>'
             f'<stop offset="1" stop-color="{_C["ron"]}"/></linearGradient>'
             '<marker id="ah" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">'
             f'<path d="M0,0 L6,3 L0,6 Z" fill="{_C["ron"]}"/></marker></defs>')
    # legend
    hy = 34
    p.append(f'<text x="{tx0}" y="{hy}" fill="{_C["ink3"]}" '
             f'font-size="10" font-family="ui-monospace,monospace" text-anchor="start">◄ RISK-OFF</text>')
    p.append(f'<text x="{tx0+tw/2:.0f}" y="{hy}" fill="{_C["ink3"]}" '
             f'font-size="10" font-family="ui-monospace,monospace" text-anchor="middle">中性</text>')
    p.append(f'<text x="{tx0+tw:.0f}" y="{hy}" fill="{_C["ink3"]}" '
             f'font-size="10" font-family="ui-monospace,monospace" text-anchor="end">RISK-ON ►</text>')
    p.append(f'<text x="0" y="{hy}" fill="{_C["ink2"]}" font-size="10" font-weight="700" '
             f'font-family="ui-monospace,monospace">REGIME 軸</text>')
    p.append(f'<text x="{rx0}" y="{hy}" fill="{_C["ink2"]}" font-size="10" font-weight="700" '
             f'font-family="ui-monospace,monospace">狀態 · 讀數</text>')
    p.append(f'<line x1="0" y1="{hy+10}" x2="{W}" y2="{hy+10}" stroke="{_C["border"]}" stroke-width="1"/>')
    for i, a in enumerate(AXES):
        cy = top + i * rowH + rowH / 2
        p.append(f'<text x="{lx}" y="{cy-3:.0f}" fill="{_C["ink1"]}" font-size="13" '
                 f'font-weight="700" text-anchor="end">{_esc(a["name"])}</text>')
        p.append(f'<text x="{lx}" y="{cy+12:.0f}" fill="{_C["ink3"]}" font-size="9" '
                 f'font-family="ui-monospace,monospace" text-anchor="end">{_esc(a["sub"])}</text>')
        p.append(f'<rect x="{tx0}" y="{cy-5:.0f}" width="{tw}" height="10" rx="5" '
                 f'fill="url(#rg)" opacity="0.85"/>')
        midx = tx0 + tw / 2
        p.append(f'<line x1="{midx:.0f}" y1="{cy-9:.0f}" x2="{midx:.0f}" y2="{cy+9:.0f}" '
                 f'stroke="{_C["ink3"]}" stroke-width="1.2" opacity="0.55"/>')
        mx = tx0 + a["pos"] * tw
        if a["trail"] is not None:
            trx = tx0 + a["trail"] * tw
            p.append(f'<line x1="{trx:.0f}" y1="{cy:.0f}" x2="{mx-9:.0f}" y2="{cy:.0f}" '
                     f'stroke="{_C["ron"]}" stroke-width="2" stroke-dasharray="2 2" '
                     f'marker-end="url(#ah)" opacity="0.85"/>')
        p.append(f'<circle cx="{mx:.0f}" cy="{cy:.0f}" r="7" fill="{_C["ink1"]}" '
                 f'stroke="{_C["bg"]}" stroke-width="2.5"/>')
        pc = _PILL[a["pillcls"]]
        pw = _pillw(a["pill"])
        p.append(f'<rect x="{rx0}" y="{cy-16:.0f}" width="{pw:.0f}" height="17" rx="8.5" fill="{pc}"/>')
        p.append(f'<text x="{rx0+pw/2:.0f}" y="{cy-4:.0f}" fill="#fff" font-size="9.5" '
                 f'font-weight="700" font-family="ui-monospace,monospace" text-anchor="middle">'
                 f'{_esc(a["pill"])}</text>')
        p.append(f'<text x="{rx0}" y="{cy+14:.0f}" fill="{_C["ink2"]}" font-size="10.5">'
                 f'{_esc(a["short"])}</text>')
        if i < n - 1:
            p.append(f'<line x1="0" y1="{top+(i+1)*rowH:.0f}" x2="{W}" y2="{top+(i+1)*rowH:.0f}" '
                     f'stroke="{_C["border"]}" stroke-width="1" opacity="0.55"/>')
    # composite band
    by = top + n * rowH + 18
    p.append(f'<line x1="0" y1="{by-8:.0f}" x2="{W}" y2="{by-8:.0f}" stroke="{_C["ink3"]}" stroke-width="1.4"/>')
    p.append(f'<text x="{lx}" y="{by+7:.0f}" fill="{_C["ink1"]}" font-size="13.5" '
             f'font-weight="800" text-anchor="end">綜合判讀</text>')
    p.append(f'<text x="{lx}" y="{by+22:.0f}" fill="{_C["ink3"]}" font-size="9" '
             f'font-family="ui-monospace,monospace" text-anchor="end">Composite（定性）</text>')
    p.append(f'<rect x="{tx0}" y="{by+2:.0f}" width="{tw}" height="12" rx="6" fill="url(#rg)"/>')
    p.append(f'<line x1="{tx0+tw/2:.0f}" y1="{by-3:.0f}" x2="{tx0+tw/2:.0f}" y2="{by+19:.0f}" '
             f'stroke="{_C["ink3"]}" stroke-width="1.2" opacity="0.55"/>')
    cmx = tx0 + COMPOSITE["pos"] * tw
    p.append(f'<circle cx="{cmx:.0f}" cy="{by+8:.0f}" r="8.5" fill="{_C["ron"]}" '
             f'stroke="{_C["bg"]}" stroke-width="2.5"/>')
    p.append(f'<text x="{rx0}" y="{by+2:.0f}" fill="{_C["ink1"]}" font-size="13" '
             f'font-weight="800">{_esc(COMPOSITE["label_zh"])}</text>')
    p.append(f'<text x="{rx0}" y="{by+18:.0f}" fill="{_C["ink3"]}" font-size="10" '
             f'font-family="ui-monospace,monospace">risk-on 傾斜 · late-cycle reflation</text>')
    p.append('</svg>')
    return "".join(p)


def render_dashboard(payload):
    cot = payload["cot_percentile_5y"]
    ratios = payload["growth_defense_ratios"]
    hot = [c for c in cot if c["extreme"] == "極端做多"]
    cold = [c for c in cot if c["extreme"] == "極端偏空"]

    st = ("font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
          f"background:{_C['bg']};border:1px solid {_C['border']};border-radius:12px;"
          f"padding:18px 20px;color:{_C['ink1']};line-height:1.6;font-size:14px")
    pill = ("display:inline-block;font-family:ui-monospace,monospace;font-size:11px;"
            "padding:2px 8px;border-radius:5px;margin:2px 3px 2px 0")

    def chips(items, bg, fg):
        return "".join(f'<span style="{pill};background:{bg};color:{fg}">{_esc(i)}</span>'
                       for i in items) or f'<span style="color:{_C["ink3"]}">—</span>'

    cot_hot = chips([f'{c["market"]} {c["pctile_5y"]:.0f}' for c in hot], "#7f1d1d", "#fecaca")
    cot_cold = chips([f'{c["market"]} {c["pctile_5y"]:.0f}' for c in cold], "#0c4a6e", "#bae6fd")

    rchips = []
    for r in ratios:
        m = r.get("mechanical") or {}
        v = m.get("value")
        pv = m.get("pctile_2y")
        txt = r["name"]
        if v is not None:
            txt += f' {v:.3f}'
        if pv is not None:
            txt += f'（2y {pv:.0f}）'
        rchips.append(txt)
    ratio_chips = chips(rchips, "#1e2a3a", "#a9c7f0")

    return (
        f'{DASH_START}\n'
        f'<div style="{st}">'
        f'<div style="font-family:ui-monospace,monospace;font-size:11px;letter-spacing:.14em;'
        f'text-transform:uppercase;color:#5b9bff;margin-bottom:12px">'
        f'大類資產 Regime · 自動儀表</div>'
        f'<div style="overflow-x:auto;margin-bottom:14px">{svg_scorecard()}</div>'
        f'<div style="margin-bottom:8px"><b>COT 極端偏多（5y ≥ 90）：</b><br>{cot_hot}</div>'
        f'<div style="margin-bottom:8px"><b>COT 極端偏空（5y ≤ 10）：</b><br>{cot_cold}</div>'
        f'<div style="margin:10px 0 6px"><b>成長 vs 防禦比率</b>（機械 value · 2y 百分位）</div>{ratio_chips}'
        f'<div style="margin-top:12px;font-family:ui-monospace,monospace;font-size:11px;'
        f'color:{_C["ink3"]}">COT as-of {_esc(payload["meta"].get("cot_as_of") or "—")} · '
        f'比率 as-of {_esc(payload["meta"].get("ratio_as_of") or "—")} · '
        f'更新 {payload["generated_at"][:10]} · 描述器非擇時</div>'
        f'</div>\n{DASH_END}'
    )


def inject_dashboard(payload):
    if not os.path.exists(INDEX_HTML):
        warn(f"index.html not found ({INDEX_HTML}); skipping dashboard injection")
        return
    with open(INDEX_HTML, encoding="utf-8") as f:
        html = f.read()
    if DASH_START not in html or DASH_END not in html:
        warn("dashboard markers not found in index.html; skipping injection")
        return
    pre = html.split(DASH_START)[0]
    post = html.split(DASH_END, 1)[1]
    new = pre + render_dashboard(payload) + post
    if new == html:
        info("dashboard: no change")
        return
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(new)
    info("dashboard: injected into index.html")


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="Cross-asset regime weekly builder")
    ap.add_argument("--skip-fetch", action="store_true",
                    help="offline: skip price fetch, recompute from caches only")
    args = ap.parse_args()

    gaps = list(GAPS)
    cot_ok = ratio_ok = False

    # ── COT layer (mechanical, from shared cot_history.json) ────────────────
    cot_rows, cot_as_of = [], None
    try:
        history = load_json(COT_HISTORY)
        cot_rows, cot_as_of, cg = cot_compute(history)
        gaps += cg
        cot_ok = bool(cot_rows)
    except Exception as e:
        warn(f"COT layer failed: {e}")

    # ── Ratio layer (mechanical, yfinance->stooq cache) ─────────────────────
    ratios_out, ratio_as_of = [], None
    try:
        price_series = build_price_cache(args.skip_fetch)
        ratios_out, rg = ratio_compute(price_series)
        gaps += rg
        asofs = [r["mechanical"]["as_of"] for r in ratios_out
                 if r.get("mechanical", {}).get("as_of")]
        ratio_as_of = max(asofs) if asofs else None
        ratio_ok = any(r["mechanical"]["value"] is not None for r in ratios_out)
    except Exception as e:
        warn(f"ratio layer failed: {e}")
        ratios_out = [dict({k: r[k] for k in ("key", "name", "sub", "reading", "src")},
                           pos_0to1=r["pos"],
                           mechanical={"value": None, "chg_12m_pct": None,
                                       "pctile_2y": None, "as_of": None})
                      for r in RATIOS_EDITORIAL]

    # ── Assemble contract ────────────────────────────────────────────────────
    meta = dict(META_EDITORIAL)
    meta["cot_as_of"] = cot_as_of
    meta["ratio_as_of"] = ratio_as_of

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "meta": meta,
        "composite": {"pos_0to1": COMPOSITE["pos"], "label_zh": COMPOSITE["label_zh"],
                      "label_en": COMPOSITE["label_en"], "method": COMPOSITE["method"]},
        "axes": [{k: a[k] for k in ("key", "name", "sub", "pos", "pill", "reading", "src")}
                 for a in AXES],
        "triggers": [dict(t) for t in TRIGGERS],
        "cot_percentile_5y": cot_rows,
        "growth_defense_ratios": ratios_out,
        "gaps": gaps,
    }

    wrote = write_json_if_changed(OUT_JSON, payload)
    info(f"latest.json: {'written' if wrote else 'no change'} "
         f"(cot {len(cot_rows)} rows @ {cot_as_of}, ratios @ {ratio_as_of})")

    inject_dashboard(payload)

    if not cot_ok and not ratio_ok:
        warn("both COT and ratio layers failed — exiting non-zero")
        sys.exit(1)
    info("done.")


if __name__ == "__main__":
    main()
