#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_credit_base_rates.py — 信用領先（HYG／LQD 比值 21 日動能）三分位 base rate
（forecast ledger P2 package G1 機械餵料）。

一次性／季度手動重建（`--if-due` 供 cron 掛「季度自動重建」，慣例照抄
scripts/build_vrp_base_rates.py）。獨立自建 raw cache
`data/credit_base_rates_raw_cache.json`（HYG／LQD／SPY 各抓 ~20 年日收盤，
yfinance `auto_adjust=True`；失敗沿用既有快取並 warn，**不做 stooq fallback**——
stooq 未還原股利，口徑與 auto_adjust=True 不同）。

定義（設計稿 `notes/site-internal/root/_forecast_p2_design_20260902.md` §1 PREREG 凍結）
--------------------------------------------------------------------------------
  R_t ＝ HYG 收盤 ÷ LQD 收盤（同日，口徑同 docs/monitor/data/latest.json 的 hyg_lqd item）
  x_t ＝ 100 × ln(R_t ／ R_{t−21})（21 個交易日對數變化，%；t 為 HYG／LQD／SPY 三序列
         共同交易日索引，非日曆日）。x 為負＝HYG 相對 LQD 下跌＝高收益利差走闊；
         x 為正＝利差收斂。

取樣點：HYG／LQD／SPY 三序列共同交易日中每月首個「x 已可算」的交易日 t（需 t−21 存在）。
21d 結果另需 t＋21 存在、63d 結果另需 t＋63 存在，**各自獨立計數**（尾端不足者不計入該
窗口，但仍計入取樣點與分桶，故 n_21d／n_63d 可能不同）。

三分位切點：取樣點 in-sample 的 x 分布的 33.3／66.7 百分位（做法照抄
build_vrp_base_rates.py「切點用同一個可判斷樣本算」的既有慣例；33.3／66.7 為沿用該檔
既有常數選擇，非精確 1/3、2/3）。

輸出 data/credit_base_rates.json：
  {built_at, data_start, data_end, n_samples, cuts:{q33,q67},
   buckets:{low,mid,high}（各含 n/n_21d/n_63d/freq_up_21d/freq_up_63d/x_range/description），
   pooled:{n_21d,n_63d,freq_up_21d,freq_up_63d},
   p_clim:{credit_spy_up_21d: pooled freq_up_21d, credit_spy_up_63d: pooled freq_up_63d},
   definition, note}
cell n（n_21d／n_63d）< 30 時，由 producer（generate_credit_forecasts.py）改用 pooled，
本表不做該 fallback（如實記錄各桶樣本數）。

誠實註記
--------
* **重疊樣本，非獨立樣本**：相鄰月份取樣點的 21／63 日前瞻視窗高度重疊，本表只報告經驗
  頻率與樣本數，不做假設檢定。
* **三分位切點 in-sample**：見上，不能宣稱樣本外預測力——本表定位是 base rate 參照表，
  不是模型。
* **信用利差代理**：本表用 HYG／LQD 價格比值近似信用利差方向，非 ICE BofA OAS（FRED 對
  OAS 只給約 3 年史，見設計稿 §0），與 docs/monitor 顯示口徑一致。
* HYG 於 2007 年才掛牌，故三序列共同交易日的實際起點晚於名目 20 年抓取窗口。

用法
----
  python scripts/build_credit_base_rates.py                 完整重抓 + 重算（預設）
  python scripts/build_credit_base_rates.py --skip-fetch     離線：只用既有本地快取重算
  python scripts/build_credit_base_rates.py --if-due         現有輸出 built_at <85 天則跳過
                                                                （cron 用，慣例照抄 vrp）
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "credit_base_rates_raw_cache.json"
OUT_JSON = DATA / "credit_base_rates.json"

SCHEMA = "credit-base-rates-v1"
TICKERS = ["HYG", "LQD", "SPY"]
FETCH_PERIOD = "20y"
X_LOOKBACK_TRADING_DAYS = 21    # PREREG 凍結（設計稿 §1；須與 generate_credit_forecasts.py 一致）
UP_21D_TRADING_DAYS = 21        # PREREG 凍結
UP_63D_TRADING_DAYS = 63        # PREREG 凍結
BUCKET_PCTS = (33.3, 66.7)      # PREREG 凍結（沿用 build_vrp_base_rates.py 既有常數選擇）
MIN_CELL_N = 30                 # 僅供文件記錄；pooled fallback 在 producer 端執行
IF_DUE_MAX_AGE_DAYS = 85        # --if-due 門檻（慣例照抄 vrp）


def warn(msg: str) -> None:
    print(f"[credit-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[credit-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance only；不做 stooq fallback——stooq 未還原股利，口徑不同）
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


def fetch_daily_bars(ticker, skip_fetch, cache_path=RAW_CACHE):
    """回傳升冪 [(date, close), ...]。skip_fetch=True 時只讀本地 cache_path。
    多個 ticker 共用同一 cache_path，累積寫入 cache["series"][ticker]。
    抓取失敗（非 --skip-fetch）時沿用既有快取並 warn；快取也沒有才中止
    （本檔不做 stooq fallback）。"""
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read {cache_path.name}: {e}")
            cache = {}
    series = cache.get("series", {})

    if skip_fetch:
        rows = series.get(ticker)
        if not rows:
            raise SystemExit(f"--skip-fetch 但 {cache_path} 無 {ticker} 快取，無法離線重算")
        return [(d, c) for d, c in rows]

    bars = None
    for attempt in range(3):
        try:
            bars = _yf_daily(ticker)
            if bars:
                break
        except Exception as e:
            warn(f"yfinance attempt {attempt + 1} failed for {ticker}: {e}")

    if not bars:
        cached_rows = series.get(ticker)
        if cached_rows:
            warn(f"{ticker} yfinance 抓取失敗，沿用既有快取（{len(cached_rows)} 筆，"
                 f"{cached_rows[0][0]}..{cached_rows[-1][0]}）——不做 stooq fallback"
                 f"（stooq 未還原股利，口徑與 auto_adjust=True 不同，設計稿 §1 明文排除）。")
            return [(d, c) for d, c in cached_rows]
        raise SystemExit(f"{ticker} 日線抓取失敗（yfinance），且無既有快取可沿用，中止"
                          f"（本 builder 不做 stooq fallback）")

    info(f"{ticker}: fetched {len(bars)} daily bars via yfinance ({bars[0][0]} .. {bars[-1][0]})")

    series[ticker] = bars
    cache["series"] = series
    cache["meta"] = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tickers": TICKERS,
        "note": "build_credit_base_rates.py 專用日線快取，季度手動重建，不做 stooq fallback。",
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return bars


def fetch_all(skip_fetch, cache_path=RAW_CACHE):
    return {t: fetch_daily_bars(t, skip_fetch, cache_path) for t in TICKERS}


# ═══════════════════════════════════════════════════════════════════════════
# R_t／x_t 序列（HYG／LQD／SPY 三序列共同交易日）
# ═══════════════════════════════════════════════════════════════════════════

def build_signal_series(hyg_bars, lqd_bars, spy_bars, lookback=X_LOOKBACK_TRADING_DAYS):
    """回傳 (common_dates, x_vals, spy_closes)：三序列共同交易日升冪排序；x_vals[i] 為
    100*ln(R_i/R_{i-lookback})（i<lookback 或分母非正時為 None）；spy_closes[i] 對齊
    common_dates[i]。"""
    hyg_map = dict(hyg_bars)
    lqd_map = dict(lqd_bars)
    spy_map = dict(spy_bars)
    common = sorted(set(hyg_map) & set(lqd_map) & set(spy_map))

    r_vals = [hyg_map[d] / lqd_map[d] for d in common]
    n = len(common)
    x_vals = [None] * n
    for i in range(lookback, n):
        r_then = r_vals[i - lookback]
        if r_then <= 0 or r_vals[i] <= 0:
            continue
        x_vals[i] = round(100 * math.log(r_vals[i] / r_then), 4)

    spy_closes = [spy_map[d] for d in common]
    return common, x_vals, spy_closes


def month_of(d):
    return d[:7]  # "YYYY-MM-DD" -> "YYYY-MM"


def sample_first_trading_day_of_month(common_dates, x_vals):
    """每個 YYYY-MM 的第一個「x 已可算」交易日。回傳 [(idx, date, x), ...]。"""
    seen = set()
    out = []
    for i, d in enumerate(common_dates):
        if x_vals[i] is None:
            continue
        m = month_of(d)
        if m in seen:
            continue
        seen.add(m)
        out.append((i, d, x_vals[i]))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 前瞻結果（三序列共同交易日索引前瞻位移，21d／63d 各自獨立計數）
# ═══════════════════════════════════════════════════════════════════════════

def build_transition_sample(monthly_samples, spy_closes,
                             up21=UP_21D_TRADING_DAYS, up63=UP_63D_TRADING_DAYS):
    n = len(spy_closes)
    rows = []
    for idx, d, x in monthly_samples:
        base_close = spy_closes[idx]
        row = {"date": d, "x": x, "up_21d": None, "up_63d": None}
        if idx + up21 < n:
            row["up_21d"] = spy_closes[idx + up21] > base_close
        if idx + up63 < n:
            row["up_63d"] = spy_closes[idx + up63] > base_close
        rows.append(row)
    return rows


def _percentile(sorted_vals, q):
    """線性內插百分位（同 numpy 預設 'linear' method），q ∈ [0,100]。"""
    n = len(sorted_vals)
    if n == 0:
        return None
    if n == 1:
        return sorted_vals[0]
    idx = q / 100.0 * (n - 1)
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return sorted_vals[lo]
    frac = idx - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


def compute_cuts(rows):
    xs = sorted(r["x"] for r in rows)
    q33_pct, q67_pct = BUCKET_PCTS
    return {"q33": round(_percentile(xs, q33_pct), 4), "q67": round(_percentile(xs, q67_pct), 4)}


def bucket_label(x, cuts):
    if x <= cuts["q33"]:
        return "low"
    if x <= cuts["q67"]:
        return "mid"
    return "high"


BUCKET_DESC = {
    "low": "高收益利差走闊快（HYG／LQD 比值 21 日下跌最多的一組）",
    "mid": "利差變化居中的一組",
    "high": "高收益利差收斂快（HYG／LQD 比值 21 日上漲最多的一組）",
}


def _freq(rows, key):
    valid = [r for r in rows if r[key] is not None]
    n = len(valid)
    if n == 0:
        return None, 0
    return round(sum(1 for r in valid if r[key]) / n, 3), n


def build_bucket_table(rows, cuts):
    buckets = {k: [] for k in ("low", "mid", "high")}
    for r in rows:
        buckets[bucket_label(r["x"], cuts)].append(r)

    out = {}
    for k in ("low", "mid", "high"):
        brows = buckets[k]
        freq21, n21 = _freq(brows, "up_21d")
        freq63, n63 = _freq(brows, "up_63d")
        xs = [r["x"] for r in brows]
        out[k] = {
            "n": len(brows),
            "n_21d": n21,
            "n_63d": n63,
            "freq_up_21d": freq21,
            "freq_up_63d": freq63,
            "x_range": [round(min(xs), 2), round(max(xs), 2)] if xs else None,
            "description": BUCKET_DESC[k],
        }
    return out


def compute_pooled(rows):
    freq21, n21 = _freq(rows, "up_21d")
    freq63, n63 = _freq(rows, "up_63d")
    return {"n_21d": n21, "n_63d": n63, "freq_up_21d": freq21, "freq_up_63d": freq63}


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="信用領先（HYG/LQD 比值）三分位 base rate builder"
                                              "（forecast ledger P2 package G1）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/credit_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建"
                          "（exit 0，印 not due）；供 cron 掛「季度自動重建」用")
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

    bars = fetch_all(args.skip_fetch)
    hyg_bars, lqd_bars, spy_bars = bars["HYG"], bars["LQD"], bars["SPY"]

    common_dates, x_vals, spy_closes = build_signal_series(hyg_bars, lqd_bars, spy_bars)
    if len(common_dates) < 260:
        raise SystemExit(f"HYG/LQD/SPY 共同交易日僅 {len(common_dates)} 筆，過少，中止")

    monthly_samples = sample_first_trading_day_of_month(common_dates, x_vals)
    if len(monthly_samples) < 60:
        raise SystemExit(f"可用月度取樣點僅 {len(monthly_samples)} 筆，過少，中止")

    sample_rows = build_transition_sample(monthly_samples, spy_closes)
    cuts = compute_cuts(sample_rows)
    buckets = build_bucket_table(sample_rows, cuts)
    pooled = compute_pooled(sample_rows)
    p_clim = {
        "credit_spy_up_21d": pooled["freq_up_21d"],
        "credit_spy_up_63d": pooled["freq_up_63d"],
    }

    payload = {
        "schema": SCHEMA,
        "tickers": TICKERS,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_start": common_dates[0],
        "data_end": common_dates[-1],
        "n_price_days": {t: len(bars[t]) for t in TICKERS},
        "n_common_days": len(common_dates),
        "n_samples": len(sample_rows),
        "x_lookback_trading_days": X_LOOKBACK_TRADING_DAYS,
        "up_21d_trading_days": UP_21D_TRADING_DAYS,
        "up_63d_trading_days": UP_63D_TRADING_DAYS,
        "cuts": cuts,
        "buckets": buckets,
        "pooled": pooled,
        "p_clim": p_clim,
        "definition": (
            "R_t ＝ HYG 收盤 ÷ LQD 收盤（同日，yfinance auto_adjust=True，口徑同 "
            "docs/monitor/data/latest.json 的 hyg_lqd item）；x_t ＝ 100 × ln(R_t ／ R_{t−21})"
            "（21 個交易日對數變化，%；t 為 HYG／LQD／SPY 三序列共同交易日索引，非日曆日）。"
            "x 為負＝HYG 相對 LQD 下跌＝高收益利差走闊；x 為正＝利差收斂。"
        ),
        "note": (
            "取樣點＝HYG／LQD／SPY 三序列共同交易日中每月首個「x 可算」交易日；三分位切點"
            "（q33/q67）為 in-sample（用同一組取樣點的 x 分布算出，非滾動窗口即時分位），"
            "不宣稱樣本外預測力，本表定位是 base rate 參照表。up_21d／up_63d 用三序列共同"
            "交易日索引前瞻位移，21d／63d 各自獨立計數（尾端不足者不計入該窗口，但仍計入"
            "取樣點與分桶，故 n_21d／n_63d 可能不同）。頻率為重疊樣本估計，不做假設檢定。"
            "本表用 HYG／LQD 價格比值近似信用利差方向，非 ICE BofA OAS（FRED 對 OAS 只給"
            "約 3 年史，見設計稿 §0）；builder 不做 stooq fallback（stooq 未還原股利，"
            "口徑與 auto_adjust=True 不同）。cell n（n_21d／n_63d）< 30 時由 producer 端"
            "改用 pooled，本表如實記錄各桶樣本數，不在此層做 fallback。"
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path} — {len(sample_rows)} 筆月度取樣點，"
         f"共同交易日 {common_dates[0]}..{common_dates[-1]}（{len(common_dates)} 筆）")
    info(f"  cuts(q33/q67)={cuts}")
    for k in ("low", "mid", "high"):
        b = buckets[k]
        info(f"  {k}: n={b['n']:<4} x_range={b['x_range']}  "
             f"n_21d={b['n_21d']:<4} freq_up_21d={b['freq_up_21d']}  "
             f"n_63d={b['n_63d']:<4} freq_up_63d={b['freq_up_63d']}")
    info(f"  pooled={pooled}")
    info(f"  p_clim={p_clim}")


if __name__ == "__main__":
    main()
