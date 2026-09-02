#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_calendar_base_rates.py — 日曆效應（月末四日窗 TOM／假日前一日）base rate builder
（forecast ledger P2 package G3 機械餵料）。

設計凍結稿 notes/site-internal/root/_forecast_p2_design_20260902.md §3。

一次性／季度手動重建（`--if-due` 供 cron 掛「季度自動重建」，慣例照抄
scripts/build_vrp_base_rates.py）。獨立自建 raw cache `data/calendar_base_rates_raw_cache.json`
（SPY 25 年日線，yfinance auto_adjust Close；yfinance 無「25y」period 選項，改用
period="max"——SPY 自 1993 年起有資料，天然 ≥ 25 年）。

定義（§3 逐字）
--------------
TOM（月末四日窗）：
  L ＝月最後交易日；命中＝close(L＋3)／close(L−1) − 1 > 0（L−1／L＋3 皆用 SPY 自身交易日
  索引位移，L＋3 即「次月第三個交易日」，見 generate_calendar_forecasts.py）；需 L−1 與 L＋3
  皆存在（歷史不足/尾端不足者不計入 n）。
  p_clim(tom_spy_up_4d) ＝全部交易日 t 的 close(t＋4)／close(t) − 1 > 0 頻率（無條件，非月末
  取樣點限定）。

Pre-holiday（假日前一日）：
  假日＝資料期間內（首尾各去 5 個交易日，避免抓取窗邊界的假訊號）不在交易日序列中的週一至
  週五；連續缺口（如週末＋週一假日相連）只算一次；P＝缺口前最後交易日；命中＝
  close(P)／close(P−1) − 1 > 0。
  p_clim(preholiday_spy_up_1d) ＝全部交易日 t 的單日上漲頻率（close(t) > close(t−1)，全樣本
  無條件）。

注意：本 builder 對「假日」的判定是純資料驅動（交易日序列裡的缺口），不區分官方假日與其他
市場關閉事件（如 9/11、颶風 Sandy 等）——與 forward-looking 的 generator 端用逐字寫死的
NYSE_HOLIDAYS 表刻意不同源，理由見 generate_calendar_forecasts.py 檔頭。

輸出 data/calendar_base_rates.json：
  {built_at, data_start, data_end, tom:{p, n}, preholiday:{p, n},
   p_clim:{tom_spy_up_4d, preholiday_spy_up_1d}, definitions}

用法
----
  python scripts/build_calendar_base_rates.py                 完整重抓 + 重算（預設）
  python scripts/build_calendar_base_rates.py --skip-fetch     離線：只用既有本地快取重算
  python scripts/build_calendar_base_rates.py --if-due         現有輸出 built_at <85 天則跳過
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "calendar_base_rates_raw_cache.json"
OUT_JSON = DATA / "calendar_base_rates.json"

SCHEMA = "calendar-base-rates-v1"
TICKER = "SPY"
FETCH_PERIOD = "max"        # yfinance 無 "25y" 選項；SPY 全歷史（1993 起）天然 ≥ 25 年
TOM_LAG_TRADING_DAYS = 3    # L+3（PREREG 凍結，設計稿 §3；即「次月第三個交易日」）
TOM_WINDOW_SPAN_TRADING_DAYS = 4  # p_clim 用（設計稿 §3：「close(t+4)/close(t)」；與
                                  # TOM 命中窗同義但錨點不同——L-1→L+3 距離恰為 4，
                                  # p_clim 改用任意 t→t+4，同一 4 交易日窗、不同起點）
EDGE_TRIM_TRADING_DAYS = 5  # pre-holiday 缺口掃描首尾各去 5 個交易日（設計稿 §3）
IF_DUE_MAX_AGE_DAYS = 85


def warn(msg: str) -> None:
    print(f"[calendar-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[calendar-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance；失敗沿用既有快取並 warn，不做 stooq fallback——同批 G1/G2 慣例）
# ═══════════════════════════════════════════════════════════════════════════

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


def fetch_spy(skip_fetch, cache_path=RAW_CACHE):
    """回傳升冪 [(date, close), ...]。skip_fetch=True 時只讀本地 cache_path。"""
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read {cache_path.name}: {e}")
            cache = {}
    series = cache.get("series", {})

    if skip_fetch:
        rows = series.get(TICKER)
        if not rows:
            raise SystemExit(f"--skip-fetch 但 {cache_path} 無 {TICKER} 快取，無法離線重算")
        return [(d, c) for d, c in rows]

    bars = None
    try:
        bars = _yf_daily(TICKER)
    except Exception as e:
        warn(f"yfinance fetch failed for {TICKER}: {e}")

    if not bars:
        rows = series.get(TICKER)
        if rows:
            warn(f"{TICKER} 抓取失敗，沿用既有快取（{len(rows)} 筆）")
            return [(d, c) for d, c in rows]
        raise SystemExit(f"{TICKER} 日線抓取失敗且無既有快取，中止")

    info(f"{TICKER}: fetched {len(bars)} daily bars via yfinance ({bars[0][0]} .. {bars[-1][0]})")
    series[TICKER] = bars
    cache["series"] = series
    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ticker": TICKER,
        "note": "build_calendar_base_rates.py 專用日線快取，季度手動重建，非 incremental cron。",
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return bars


# ═══════════════════════════════════════════════════════════════════════════
# TOM（月末四日窗）
# ═══════════════════════════════════════════════════════════════════════════

def find_month_end_indices(dates):
    """回傳 [(YYYY-MM, idx), ...]：每個「有後續月份接續」的月份之最後交易日 index
    （資料裡最後一個、尚未走完的月份不計入——其「最後交易日」還會再變動）。"""
    out = []
    for i in range(len(dates) - 1):
        if dates[i][:7] != dates[i + 1][:7]:
            out.append((dates[i][:7], i))
    return out


def build_tom_sample(dates, closes, month_ends, lag=TOM_LAG_TRADING_DAYS):
    n = len(dates)
    rows = []
    for month_str, lidx in month_ends:
        if lidx - 1 < 0 or lidx + lag >= n:
            continue  # 歷史不足 L-1，或尾端不足 L+lag，兩者皆不計入樣本
        base_close = closes[lidx - 1]
        end_close = closes[lidx + lag]
        hit = (end_close / base_close - 1) > 0
        rows.append({
            "month": month_str, "L": dates[lidx],
            "base_date": dates[lidx - 1], "end_date": dates[lidx + lag],
            "hit": hit,
        })
    return rows


def compute_tom_p_clim(closes, lag=TOM_WINDOW_SPAN_TRADING_DAYS):
    n = len(closes)
    hits = [(closes[t + lag] / closes[t] - 1) > 0 for t in range(n - lag)]
    if not hits:
        return None, 0
    return round(sum(hits) / len(hits), 4), len(hits)


# ═══════════════════════════════════════════════════════════════════════════
# Pre-holiday（缺口偵測；連續缺口只算一次；首尾各去 5 個交易日）
# ═══════════════════════════════════════════════════════════════════════════

def detect_holiday_gaps(dates, edge_trim=EDGE_TRIM_TRADING_DAYS):
    """回傳升冪 [{"P", "P_minus1"}, ...]。掃描範圍限縮在
    dates[edge_trim .. n-1-edge_trim]（含）之間——首尾各去 edge_trim 個交易日，避免抓取窗
    邊界（資料起訖點附近）誤判為假日缺口。"""
    n = len(dates)
    events = []
    if n < 2 * edge_trim + 2:
        return events
    date_objs = [date.fromisoformat(d) for d in dates]
    for i in range(edge_trim, n - 1 - edge_trim):
        d_cur = date_objs[i]
        d_next = date_objs[i + 1]
        delta = (d_next - d_cur).days
        if delta <= 1:
            continue
        gap_start = next((d_cur + timedelta(days=k) for k in range(1, delta)
                          if (d_cur + timedelta(days=k)).weekday() < 5), None)
        if gap_start is None:
            continue  # 純週末缺口（如 Fri→Mon），不是假日
        events.append({"P": dates[i], "P_minus1": dates[i - 1],
                       "gap_start": gap_start.isoformat(), "next_trading_day": dates[i + 1]})
    return events


def build_preholiday_sample(dates, closes, events):
    idx_of = {d: i for i, d in enumerate(dates)}
    rows = []
    for e in events:
        p_idx = idx_of[e["P"]]
        pm1_idx = idx_of[e["P_minus1"]]
        hit = (closes[p_idx] / closes[pm1_idx] - 1) > 0
        rows.append({"P": e["P"], "P_minus1": e["P_minus1"], "gap_start": e["gap_start"], "hit": hit})
    return rows


def compute_preholiday_p_clim(closes):
    hits = [closes[t] > closes[t - 1] for t in range(1, len(closes))]
    if not hits:
        return None, 0
    return round(sum(hits) / len(hits), 4), len(hits)


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="日曆效應（TOM／假日前一日）base rate builder"
                                              "（forecast ledger P2 package G3）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/calendar_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過")
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

    bars = fetch_spy(args.skip_fetch)
    dates = [d for d, _ in bars]
    closes = [c for _, c in bars]
    if len(dates) < 260:
        raise SystemExit(f"SPY 可用樣本僅 {len(dates)} 筆日線，過少，中止")

    # TOM
    month_ends = find_month_end_indices(dates)
    tom_rows = build_tom_sample(dates, closes, month_ends)
    if not tom_rows:
        raise SystemExit("TOM 可驗證樣本為 0，中止")
    tom_n = len(tom_rows)
    tom_p = round(sum(1 for r in tom_rows if r["hit"]) / tom_n, 4)
    tom_p_clim, tom_p_clim_n = compute_tom_p_clim(closes)

    # Pre-holiday
    gap_events = detect_holiday_gaps(dates)
    preholiday_rows = build_preholiday_sample(dates, closes, gap_events)
    if not preholiday_rows:
        raise SystemExit("Pre-holiday 可驗證樣本為 0，中止")
    ph_n = len(preholiday_rows)
    ph_p = round(sum(1 for r in preholiday_rows if r["hit"]) / ph_n, 4)
    ph_p_clim, ph_p_clim_n = compute_preholiday_p_clim(closes)

    recent_gaps = [
        {"gap_start": r["gap_start"], "P": r["P"], "P_minus1": r["P_minus1"], "hit": r["hit"]}
        for r in preholiday_rows[-10:]
    ]

    payload = {
        "schema": SCHEMA,
        "ticker": TICKER,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_start": dates[0],
        "data_end": dates[-1],
        "n_price_days": len(dates),
        "tom": {"p": tom_p, "n": tom_n},
        "preholiday": {"p": ph_p, "n": ph_n},
        "p_clim": {
            "tom_spy_up_4d": tom_p_clim,
            "preholiday_spy_up_1d": ph_p_clim,
        },
        "definitions": {
            "tom": (f"L=月最後交易日；命中=close(L+{TOM_LAG_TRADING_DAYS})/close(L-1)-1>0；"
                    f"p_clim=全部交易日 t 的 close(t+{TOM_WINDOW_SPAN_TRADING_DAYS})/close(t)-1>0 "
                    f"無條件頻率（同一 4 交易日窗、不同起點，n={tom_p_clim_n}）"),
            "preholiday": (f"假日=資料期間（首尾各去 {EDGE_TRIM_TRADING_DAYS} 個交易日）內不在交易日"
                           f"序列中的週一至週五，連續缺口只算一次；P=缺口前最後交易日；"
                           f"命中=close(P)/close(P-1)-1>0；p_clim=全部交易日單日上漲無條件頻率"
                           f"（n={ph_p_clim_n}）"),
            "tom_lag_trading_days": TOM_LAG_TRADING_DAYS,
            "edge_trim_trading_days": EDGE_TRIM_TRADING_DAYS,
        },
        "recent_holiday_gaps_sample": recent_gaps,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path} — SPY {dates[0]}..{dates[-1]}（{len(dates)} 筆）")
    info(f"  tom: p={tom_p} n={tom_n}  p_clim={tom_p_clim}（n={tom_p_clim_n}）")
    info(f"  preholiday: p={ph_p} n={ph_n}  p_clim={ph_p_clim}（n={ph_p_clim_n}）")
    info("  5 most recent detected holiday gaps (gap_start): " +
         ", ".join(g["gap_start"] for g in recent_gaps[-5:][::-1]))


if __name__ == "__main__":
    main()
