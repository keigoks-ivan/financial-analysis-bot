#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_tsmom_base_rates.py — TSMOM（時間序列動能）12-1 訊號經驗轉移表
（forecast ledger v2 §5.2 tsmom producer 的機械餵料）。

一次性／季度手動重建（`--if-due` 供 cron 掛「季度自動重建」，慣例照抄
scripts/build_rv_base_rates.py／scripts/build_cot_base_rates.py）。**自建**
data/tsmom_base_rates_raw_cache.json（9 檔 trend-track 資產類別代理＋PDBC 共 10 檔，
各抓 ~20 年日線，yfinance -> stooq fallback）——與 data/trend_track_prices.json
解耦，理由同 build_cot_base_rates.py 檔頭：trend_track_prices.json 只 rolling
~420 個交易日（供 scripts/build_trend_track.py 的「當前訊號」用），深度不足以
回測 20 年的月度取樣點，故本檔自抓長歷史。

訊號與結果定義（與 scripts/build_trend_track.py 的 12-1 動能定義逐字一致，
不得另立標準——見設計稿 notes/site-internal/root/_forecast_v2_design_20260902.md
§5.2）：

  ret_12_1 = close[i-21] / close[i-252] - 1     （t-252 至 t-21 交易日總報酬，
                                                    對齊 build_trend_track.py
                                                    的 FAR_IDX=-253/NEAR_IDX=-22
                                                    相對末筆的定義：在任一取樣
                                                    索引 i 上，near=i-21、
                                                    far=i-252，需 i>=252，即
                                                    該資產至少要有 253 筆收盤
                                                    才可算）
  state    = "in_trend"（ret_12_1 > 0）或 "not_in_trend"（ret_12_1 <= 0）
  outcome  = close[i+21] > close[i]             （t 後第 21 個交易日收盤
                                                    是否高於 t 收盤；i+21 需
                                                    在資料範圍內）

取樣點＝每月首個交易日（依各 ticker 自身收盤序列切月分組取第一筆，非套用
統一交易日曆——不同 ETF 上市日不同，各自認自己的第一筆）。

輸出 data/tsmom_base_rates.json：
  - 每檔（10 檔，含 DBC 與 PDBC 兩列）× state(in_trend/not_in_trend) 的
    {n, freq_up}
  - `p_clim[ticker]` = 該 ticker 全部取樣點（不分 state）的無條件 freq_up
  - pooled：9 個「canonical slot」（8 核心資產 + 大宗商品格＝DBC 自身歷史）
    合併統計，**不含 PDBC**——PDBC 列只供 generate_tsmom_forecasts.py 在
    DBC 資料不足需要 fallback 時查表用，若併入 pooled 會讓大宗商品格的
    觀測被兩次計入（DBC 與 PDBC 2006–2026／2014–2026 高度重疊），故排除。

誠實註記（務必讀）
------------------
* **quintile-free**：state 只有二分（in_trend／not_in_trend），門檻是訊號本身
  的正負號，不是樣本內百分位切點——不像 scripts/build_rv_base_rates.py 的五
  分位表需要「用同一組可判斷樣本算切點」那種 in-sample 顧慮，這裡沒有切點
  可算，故無對應顧慮。
* **月頻取樣、結果視窗近乎不重疊**：取樣點間隔約 21 個交易日（一個月），
  outcome 視窗（t 到 t+21 交易日）長度也是 21 個交易日，故相鄰取樣點的
  outcome 視窗大致首尾相接、重疊極少（差異僅來自每月實際交易日數不是恆定
  21天的誤差）——這與 build_rv_base_rates.py 的「相鄰交易日重疊 21 日視窗」
  是不同性質：那裡是逐日取樣、這裡是逐月取樣，統計獨立性明顯較佳，但仍非
  嚴格獨立樣本（12-1 訊號本身用的 t-252~t-21 這段 231 個交易日的窗，相鄰
  月份之間高度重疊——這是「訊號」的重疊，不是「outcome」的重疊，本表報告
  的頻率是以 outcome 是否重疊為準的近似獨立估計，仍不做假設檢定）。
* **cell n < 30 的 fallback 由 producer 端處理**（generate_tsmom_forecasts.py
  查表時若 own-ticker × state 的 n < 30，改用 pooled 同 state 的格），本檔
  只誠實列出每格的 n，不在此處做任何替換或隱藏樣本薄的格。
* PDBC 上市於 2014-11，歷史僅約 12 年，取樣點數天生少於其餘 9 檔（20 年）；
  這是資料本身限制，非本腳本 bug。

用法
----
  python scripts/build_tsmom_base_rates.py                完整重抓 + 重算（預設）
  python scripts/build_tsmom_base_rates.py --skip-fetch    離線：只用既有本地快取重算
  python scripts/build_tsmom_base_rates.py --if-due        現有輸出 built_at <85 天則跳過
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "tsmom_base_rates_raw_cache.json"  # 本檔專用，與 data/trend_track_prices.json 解耦
OUT_JSON = DATA / "tsmom_base_rates.json"

SCHEMA = "tsmom-base-rates-v1"
FETCH_PERIOD = "20y"
IF_DUE_MAX_AGE_DAYS = 85    # --if-due 門檻（設計稿 §F3 慣例，照抄 rv/cot/vixts builder）

# PREREG 凍結：12-1 訊號定義與 scripts/build_trend_track.py 逐字一致（不得調參）。
MIN_CLOSES = 253            # 需 i>=252（0-based），即至少 253 筆收盤才可算訊號（§G6 資料充足門檻）
FAR_OFFSET = 252            # far index = i - 252（~12 個月前）
NEAR_OFFSET = 21            # near index = i - 21（~1 個月前，跳過最近 21 個交易日）
OUTCOME_OFFSET = 21         # outcome index = i + 21（~1 個月後）

MIN_CELL_N = 30             # producer 端 own-cell < 此門檻 → fallback 用 pooled（本檔僅標註，不替換）

# 資產類別代理（與 build_trend_track.py CORE_ROLES 逐字一致）
CORE_ROLES = [
    ("SPY", "美股大盤（S&P 500）"),
    ("QQQ", "美股科技（Nasdaq 100）"),
    ("IWM", "美股小型股（Russell 2000）"),
    ("EFA", "成熟市場（歐澳遠東）"),
    ("EEM", "新興市場"),
    ("TLT", "長天期美債（20 年以上）"),
    ("IEF", "中天期美債（7–10 年）"),
    ("GLD", "黃金"),
]
CORE_SYMBOLS = [t for t, _ in CORE_ROLES]
COMMODITY_ROLE = "大宗商品"
COMMODITY_PRIMARY = "DBC"
COMMODITY_FALLBACK = "PDBC"
ROLE_MAP = dict(CORE_ROLES)
ROLE_MAP[COMMODITY_PRIMARY] = COMMODITY_ROLE
ROLE_MAP[COMMODITY_FALLBACK] = COMMODITY_ROLE

FETCH_UNIVERSE = CORE_SYMBOLS + [COMMODITY_PRIMARY, COMMODITY_FALLBACK]  # 10 檔
POOLED_SLOTS = CORE_SYMBOLS + [COMMODITY_PRIMARY]  # 9 個 canonical slot（大宗商品格用 DBC 自身歷史）


def warn(msg: str) -> None:
    print(f"[tsmom-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[tsmom-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance -> stooq fallback；獨立實作，理由同 build_cot_base_rates.py
# 檔頭：避免耦合到並行開發中的其他 pipeline）
# ═══════════════════════════════════════════════════════════════════════════

def _http_get(url, timeout=45):
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 tsmom-base-rates"})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 tsmom-base-rates"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


def _yf_daily(ticker, period=FETCH_PERIOD):
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


def _stooq_daily(ticker):
    sym = ticker.lower()
    if "." not in sym:
        sym = sym + ".us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
    try:
        raw = _http_get(url, timeout=30).decode("utf-8", "replace")
    except Exception as e:
        warn(f"stooq fetch failed for {ticker}: {e}")
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


def fetch_daily_bars(ticker, skip_fetch, cache):
    """回傳升冪 [(date, close), ...]。skip_fetch=True 時只讀 cache 現有內容。
    cache: 整份快取 dict（含 "series"），本函式就地更新 cache["series"][ticker]。"""
    series = cache.setdefault("series", {})

    if skip_fetch:
        rows = series.get(ticker)
        if not rows:
            raise SystemExit(f"--skip-fetch 但 {RAW_CACHE} 無 {ticker} 快取，無法離線重算")
        return [(d, c) for d, c in rows]

    bars = None
    src = None
    for attempt in range(3):
        try:
            bars = _yf_daily(ticker)
            if bars:
                src = "yfinance"
                break
        except Exception as e:
            warn(f"yfinance attempt {attempt + 1} failed for {ticker}: {e}")
    if not bars:
        bars = _stooq_daily(ticker)
        if bars:
            src = "stooq"
    if not bars:
        raise SystemExit(f"{ticker} 日線抓取全數失敗（yfinance + stooq），中止")

    info(f"{ticker}: fetched {len(bars)} daily bars via {src} ({bars[0][0]} .. {bars[-1][0]})")
    series[ticker] = bars
    return bars


def fetch_all(skip_fetch, cache_path=RAW_CACHE):
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read {cache_path.name}: {e}")
            cache = {}
    cache.setdefault("series", {})

    out = {}
    gaps = []
    for t in FETCH_UNIVERSE:
        try:
            out[t] = fetch_daily_bars(t, skip_fetch, cache)
        except SystemExit as e:
            warn(str(e))
            gaps.append({"ticker": t, "reason": str(e)})
            out[t] = []

    if not skip_fetch:
        cache["meta"] = {
            "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tickers": FETCH_UNIVERSE,
            "note": "build_tsmom_base_rates.py 專用日線快取（獨立於 data/trend_track_prices.json），"
                    "季度手動重建，非 incremental cron。",
        }
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                              encoding="utf-8")
    return out, gaps


# ═══════════════════════════════════════════════════════════════════════════
# 12-1 訊號 + 月度取樣（與 build_trend_track.py 定義逐字一致）
# ═══════════════════════════════════════════════════════════════════════════

def month_first_indices(dates):
    """dates: 升冪 'YYYY-MM-DD' 字串列表。回傳 [(month_key, idx), ...]，
    idx = 該月在此序列中第一次出現的索引（依此 ticker 自身序列切月，
    不套用統一交易日曆）。"""
    out = []
    seen = set()
    for i, d in enumerate(dates):
        m = d[:7]
        if m not in seen:
            seen.add(m)
            out.append((m, i))
    return out


def build_sample_rows(dates, closes):
    """回傳每月首個交易日中「訊號與 outcome 皆可算」的觀測列：
    {"date","month","ret_12_1","state","outcome_up"}。
    需 idx >= FAR_OFFSET（訊號可算）且 idx + OUTCOME_OFFSET < len(closes)（outcome 可算）。"""
    n = len(closes)
    rows = []
    for month, idx in month_first_indices(dates):
        if idx < FAR_OFFSET or idx + OUTCOME_OFFSET >= n:
            continue
        far = closes[idx - FAR_OFFSET]
        near = closes[idx - NEAR_OFFSET]
        if not far:
            continue
        ret_12_1 = near / far - 1.0
        state = "in_trend" if ret_12_1 > 0 else "not_in_trend"
        outcome_up = closes[idx + OUTCOME_OFFSET] > closes[idx]
        rows.append({
            "date": dates[idx], "month": month,
            "ret_12_1": round(ret_12_1, 6),
            "state": state, "outcome_up": bool(outcome_up),
        })
    return rows


def summarize_rows(rows):
    """回傳 {"n_samples","states":{"in_trend":{"n","freq_up"},"not_in_trend":{...}},"p_clim"}。"""
    states = {}
    for key in ("in_trend", "not_in_trend"):
        sub = [r for r in rows if r["state"] == key]
        n = len(sub)
        if n == 0:
            states[key] = {"n": 0, "freq_up": None, "lo_sample": True}
            continue
        freq_up = sum(1 for r in sub if r["outcome_up"]) / n
        states[key] = {"n": n, "freq_up": round(freq_up, 4), "lo_sample": n < MIN_CELL_N}
    n_total = len(rows)
    p_clim = round(sum(1 for r in rows if r["outcome_up"]) / n_total, 4) if n_total else None
    return {"n_samples": n_total, "states": states, "p_clim": p_clim}


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="TSMOM 12-1 訊號 base rate builder（forecast ledger v2 tsmom producer 機械餵料）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/tsmom_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建")
    args = ap.parse_args()

    if args.if_due:
        out_path_check = Path(args.out)
        if out_path_check.exists():
            try:
                existing = json.loads(out_path_check.read_text(encoding="utf-8"))
                built_at = existing.get("built_at")
                if built_at:
                    built_dt = datetime.strptime(built_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    age_days = (datetime.now(timezone.utc) - built_dt).total_seconds() / 86400.0
                    if age_days < IF_DUE_MAX_AGE_DAYS:
                        info(f"--if-due: {out_path_check} built_at={built_at}（{age_days:.1f} 天前）< "
                             f"{IF_DUE_MAX_AGE_DAYS} 天門檻，not due，本次不重建")
                        return
                    info(f"--if-due: {out_path_check} built_at={built_at}（{age_days:.1f} 天前）≥ "
                         f"{IF_DUE_MAX_AGE_DAYS} 天門檻，due，繼續重建")
                else:
                    info(f"--if-due: {out_path_check} 無 built_at 欄位，視為需要重建")
            except (OSError, json.JSONDecodeError, ValueError) as e:
                warn(f"--if-due: 無法讀取/解析既有 {out_path_check}（{e}），視為需要重建")
        else:
            info(f"--if-due: {out_path_check} 不存在，視為需要重建")

    price_series, fetch_gaps = fetch_all(args.skip_fetch)

    tickers_out = {}
    rows_by_ticker = {}
    for t in FETCH_UNIVERSE:
        bars = price_series.get(t) or []
        if not bars:
            tickers_out[t] = {"role": ROLE_MAP.get(t), "n_price_days": 0, "n_samples": 0,
                               "states": {}, "p_clim": None, "note": "無價格資料"}
            rows_by_ticker[t] = []
            continue
        bars = sorted(bars, key=lambda b: b[0])
        dates = [d for d, _ in bars]
        closes = [c for _, c in bars]
        rows = build_sample_rows(dates, closes)
        rows_by_ticker[t] = rows
        summary = summarize_rows(rows)
        tickers_out[t] = {
            "role": ROLE_MAP.get(t),
            "data_start": dates[0], "data_end": dates[-1],
            "n_price_days": len(closes),
            **summary,
        }
        if not rows:
            warn(f"{t}：{len(closes)} 筆收盤，但可驗證月度取樣點為 0（歷史不足以同時算訊號 + "
                 f"{OUTCOME_OFFSET} 交易日後 outcome）")

    # pooled：9 個 canonical slot（8 核心 + DBC 代表大宗商品格，不含 PDBC——見檔頭誠實註記）
    pooled_rows = []
    for t in POOLED_SLOTS:
        pooled_rows.extend(rows_by_ticker.get(t, []))
    pooled_summary = summarize_rows(pooled_rows)

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "signal_definition": (
            "12-1 動能：ret_12_1 = close[i-21] / close[i-252] - 1（t-252 至 t-21 交易日"
            "總報酬），與 scripts/build_trend_track.py 定義逐字一致；state='in_trend' 若 "
            "ret_12_1 > 0，否則 'not_in_trend'。取樣點＝每月首個交易日（依各 ticker 自身"
            "收盤序列切月，非統一交易日曆）；需該取樣點 index >= 252（至少 253 筆收盤）"
            "才可算訊號。"
        ),
        "outcome_definition": "outcome_up = close[i+21] > close[i]（t 後第 21 個交易日收盤是否高於 t 收盤）。",
        "min_closes_floor": MIN_CLOSES,
        "far_offset_trading_days": FAR_OFFSET,
        "near_offset_trading_days": NEAR_OFFSET,
        "outcome_offset_trading_days": OUTCOME_OFFSET,
        "min_cell_n_for_own_table": MIN_CELL_N,
        "fetch_period": FETCH_PERIOD,
        "commodity_primary": COMMODITY_PRIMARY,
        "commodity_fallback": COMMODITY_FALLBACK,
        "tickers": tickers_out,
        "pooled": {
            "slots_used": POOLED_SLOTS,
            "note": "9 個 canonical slot 合併（8 核心資產 + DBC 代表大宗商品格）；PDBC 不併入"
                    "pooled，避免大宗商品格觀測因 DBC/PDBC 高度重疊而被重複計入。",
            **pooled_summary,
        },
        "fetch_gaps": fetch_gaps,
        "methodology_note": (
            "quintile-free：state 為訊號正負號二分，非樣本內百分位切點，無 in-sample 切點"
            "顧慮。月頻取樣、outcome 視窗（21 交易日）與取樣間隔（約 21 交易日／月）大致"
            "首尾相接、重疊極少，但訊號本身的 t-252~t-21 視窗在相鄰月份間高度重疊——本表"
            "只報告經驗頻率與樣本數 n，不做假設檢定。cell n < 30 的樣本薄格已標 lo_sample，"
            "由 generate_tsmom_forecasts.py 查表時 fallback 用 pooled 同 state 的格（見設計稿 "
            "notes/site-internal/root/_forecast_v2_design_20260902.md §5.2），本檔不預先替換。"
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")

    info(f"wrote {out_path}")
    info(f"{'ticker':<6} {'n_days':>7} {'n_samp':>7} {'in_trend(n,freq)':>20} {'not_in_trend(n,freq)':>22} {'p_clim':>8}")
    for t in FETCH_UNIVERSE:
        row = tickers_out[t]
        st = row.get("states", {})
        it = st.get("in_trend", {})
        nt = st.get("not_in_trend", {})
        info(f"{t:<6} {row.get('n_price_days', 0):>7} {row.get('n_samples', 0):>7} "
             f"({it.get('n')},{it.get('freq_up')}){'':>4} ({nt.get('n')},{nt.get('freq_up')}){'':>4} "
             f"{row.get('p_clim')}")
    p = pooled_summary
    info(f"pooled  n_samples={p['n_samples']}  in_trend={p['states']['in_trend']}  "
         f"not_in_trend={p['states']['not_in_trend']}  p_clim={p['p_clim']}")


if __name__ == "__main__":
    main()
