#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_breadth_base_rates.py — 市場廣度（sector-ETF breadth）base rate（forecast ledger
P2 package G2 機械餵料）。

一次性／季度手動重建（`--if-due` 供 cron 掛「季度自動重建」，慣例照抄
scripts/build_vrp_base_rates.py）。獨立自建 raw cache
`data/breadth_base_rates_raw_cache.json`（SPY＋11 檔 SPDR 類股 ETF，yfinance
period="max" 日線；與 data/statlab_prices.json 解耦，理由同 build_vrp_base_rates.py：
statlab 只 rolling ~850 個交易日，不夠建 20＋年 base rate）。

定義（設計稿 `notes/site-internal/root/_forecast_p2_design_20260902.md` §2 PREREG 凍結）
--------------------------------------------------------------------------------
  b_t = 100 × (收盤 > 自身 50 日簡單均線 的類股 ETF 檔數) ÷ (當日有 ≥ 50 根 bar 的類股 ETF 檔數)
    母體（11 檔 SPDR）：XLK XLF XLE XLV XLI XLY XLP XLU XLB XLRE XLC
    「有 ≥ 50 根 bar」＝該 ETF 自身歷史（含當日）累計根數 ≥ 50（能算出 50 日 SMA）；
    XLRE（2015 上市）／XLC（2018 上市）在各自上市初期會暫時被排除分母，屬預期行為。
    可用檔數（分母）< 9 的日子整天不取樣。

取樣點：SPY 每月首個交易日 t。結果＝SPY 收盤(t＋21／63 個「SPY 自身交易日」) > 收盤(t)，
21d／63d 各自獨立計數（尾端不足 t＋63 但 t＋21 仍可算時，21d 桶收、63d 桶不收——結構同
scripts/build_credit_base_rates.py／設計稿 §1）。

桶＝**固定門檻（PREREG，非資料推算切點）**：low b<30／mid 30≤b≤80／high b>80。
每桶 {n_21d, n_63d, freq_up_21d, freq_up_63d}；pooled＝全部取樣點合併（不分桶）的同組統計；
p_clim = {"breadth_spy_up_21d": pooled.freq_up_21d, "breadth_spy_up_63d": pooled.freq_up_63d}
（同一取樣點、同一窗口下的無條件頻率）。cell n < 30 → producer 用 pooled 代替。

誠實註記
--------
* **重疊樣本，非獨立樣本**：月頻取樣降低但未消除 21／63 交易日前瞻視窗的跨月重疊，本表只報告
  經驗頻率與樣本數，不做假設檢定。
* **固定門檻非資料切點**：與 vrp/rv 的 in-sample 分位不同，low/mid/high 是設計稿明文凍結的
  絕對數字，不隨資料重跑而變動；因此 low／high 桶的樣本量取決於歷史上廣度觸及極端值的頻率，
  可能明顯薄於 mid 桶（甚至 n<30 觸發 pooled 退回），此為預期現象，非資料錯誤。
* 無 stooq fallback（yfinance 失敗時直接沿用既有本地快取並 warn，不新增資料源——理由同
  scripts/build_credit_base_rates.py 檔頭：ETF 還原股利口徑跨源不一致）。

用法
----
  python scripts/build_breadth_base_rates.py                 完整重抓 + 重算（預設）
  python scripts/build_breadth_base_rates.py --skip-fetch     離線：只用既有本地快取重算
  python scripts/build_breadth_base_rates.py --if-due         現有輸出 built_at <85 天則跳過
                                                                （cron 用，慣例照抄 vrp/rv）
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_CACHE = DATA / "breadth_base_rates_raw_cache.json"  # 本檔專用，與 data/statlab_prices.json 解耦
OUT_JSON = DATA / "breadth_base_rates.json"

SCHEMA = "breadth-base-rates-v1"
SPY_TICKER = "SPY"
SECTOR_TICKERS = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
TICKERS = [SPY_TICKER] + SECTOR_TICKERS
FETCH_PERIOD = "max"  # yfinance 無 "25y" 選項；period="max" 取得全歷史（慣例同
                       # build_monitor_score.py／build_risk_gauge.py），恰好涵蓋設計稿要求的
                       # 「25 年」（多數 SPDR 自 1998-12 起、XLRE 2015、XLC 2018）。
SMA_WINDOW = 50                 # PREREG 凍結
UP_21D_TRADING_DAYS = 21        # PREREG 凍結
UP_63D_TRADING_DAYS = 63        # PREREG 凍結
MIN_AVAILABLE_SECTORS = 9       # PREREG 凍結：可用檔數 < 9 的日子不取樣
BUCKET_LOW_MAX = 30             # PREREG 凍結：low b < 30
BUCKET_HIGH_MIN = 80            # PREREG 凍結：high b > 80（30 ≤ b ≤ 80 為 mid）
MIN_CELL_N = 30                 # cell n < 30 → 用 pooled
IF_DUE_MAX_AGE_DAYS = 85        # --if-due 門檻（慣例照抄 vrp/rv）


def warn(msg: str) -> None:
    print(f"[breadth-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[breadth-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 日線抓取（yfinance only，失敗沿用既有快取；無 stooq fallback，理由見檔頭）
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


def fetch_daily_bars(ticker, skip_fetch, cache_path=RAW_CACHE, cache=None):
    """回傳升冪 [(date, close), ...]。skip_fetch=True 時只讀本地 cache_path。
    多個 ticker 共用同一份 cache dict（呼叫端傳入、就地累積），最後統一寫檔。"""
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
        cached = series.get(ticker)
        if cached:
            warn(f"{ticker} yfinance 抓取失敗，沿用既有快取（{len(cached)} 筆，"
                 f"{cached[0][0]}..{cached[-1][0]}）")
            return [(d, c) for d, c in cached]
        raise SystemExit(f"{ticker} yfinance 抓取失敗且無既有快取可沿用，中止")

    info(f"{ticker}: fetched {len(bars)} daily bars via yfinance ({bars[0][0]} .. {bars[-1][0]})")
    series[ticker] = bars
    cache["series"] = series
    return bars


def fetch_all(skip_fetch, cache_path=RAW_CACHE):
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"could not read {cache_path.name}: {e}")
            cache = {}

    out = {}
    for t in TICKERS:
        out[t] = fetch_daily_bars(t, skip_fetch, cache_path, cache=cache)

    if not skip_fetch:
        cache["meta"] = {
            "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tickers": TICKERS,
            "note": "build_breadth_base_rates.py 專用日線快取（獨立於 data/statlab_prices.json），"
                    "季度手動重建，非 incremental cron。無 stooq fallback。",
        }
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                              encoding="utf-8")
    return out


# ═══════════════════════════════════════════════════════════════════════════
# b_t 序列：每個類股 ETF 自身 50 日 SMA、是否站上
# ═══════════════════════════════════════════════════════════════════════════

def sector_above_sma_by_date(bars, window=SMA_WINDOW):
    """bars: 升冪 [(date, close), ...]。回傳 {date: is_above}，只含「自身累計根數 ≥ window」
    的日期（不足 window 根的早期歷史整段不出現在回傳 dict 中，代表該日對此 ETF 不可用）。"""
    dates = [d for d, _ in bars]
    closes = [c for _, c in bars]
    out = {}
    for i in range(window - 1, len(closes)):
        window_vals = closes[i - window + 1: i + 1]
        sma = sum(window_vals) / window
        out[dates[i]] = closes[i] > sma
    return out


def build_breadth_series(sector_bars_by_ticker):
    """回傳升冪 [(date, b, n_available), ...]：對 SPY 交易日曆之外獨立算——這裡先算出
    「每個類股 ETF 各自的 above-sma 日期集合」，再對所有出現過的日期聯集逐日算 b_t／
    可用檔數，可用檔數 < MIN_AVAILABLE_SECTORS 的日子整天不列入（回傳序列中不出現）。"""
    above_by_ticker = {t: sector_above_sma_by_date(bars) for t, bars in sector_bars_by_ticker.items()}

    all_dates = sorted(set().union(*(set(d.keys()) for d in above_by_ticker.values())))
    out = []
    for d in all_dates:
        flags = [above_by_ticker[t][d] for t in SECTOR_TICKERS if d in above_by_ticker[t]]
        n_avail = len(flags)
        if n_avail < MIN_AVAILABLE_SECTORS:
            continue
        n_above = sum(1 for f in flags if f)
        b = round(100.0 * n_above / n_avail, 4)
        out.append((d, b, n_avail))
    return out


def month_of(d):
    return d[:7]  # "YYYY-MM-DD" -> "YYYY-MM"


def sample_first_trading_day_of_month(breadth_series):
    """breadth_series: 升冪 [(date, b, n_avail), ...]。回傳每個 YYYY-MM 的第一筆
    （SPY 每月首個交易日的定義照抄 build_vrp_base_rates.py，但取樣母體換成 breadth_series
    自身涵蓋的日期——breadth_series 已限定在可用檔數 ≥9 的日子）。"""
    seen = set()
    out = []
    for d, b, n_avail in breadth_series:
        m = month_of(d)
        if m in seen:
            continue
        seen.add(m)
        out.append((d, b, n_avail))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 前瞻視窗（用 SPY 自身交易日序列；21d／63d 各自獨立計數，尾端不足者不計——
# 結構同設計稿 §1 credit-lead，非 vrp 的「兩窗聯合可驗證」寫法）
# ═══════════════════════════════════════════════════════════════════════════

def build_transition_sample(monthly_samples, spy_bars,
                             up21_days=UP_21D_TRADING_DAYS, up63_days=UP_63D_TRADING_DAYS):
    """對每個月度取樣點 (date, b, n_avail)，各自獨立判斷 21d／63d 前瞻視窗是否可驗證。
    回傳 [{"date","b","n_avail","up_21d": bool|None,"up_63d": bool|None}, ...]
    （None 表示該視窗在此點不可驗證，尾端截斷）。"""
    spy_dates = [d for d, _ in spy_bars]
    spy_closes = [c for _, c in spy_bars]
    n = len(spy_dates)

    rows = []
    for d, b, n_avail in monthly_samples:
        pos = bisect.bisect_left(spy_dates, d)
        if pos >= n or spy_dates[pos] != d:
            # 取樣點日期理論上必為 SPY 自身交易日（breadth_series 只用 SPY 有均線的類股日期
            # 交集，而類股與 SPY 同屬美股交易日曆），此為防禦性檢查。
            continue
        base_close = spy_closes[pos]
        idx21 = pos + up21_days
        idx63 = pos + up63_days
        up_21d = (spy_closes[idx21] > base_close) if idx21 < n else None
        up_63d = (spy_closes[idx63] > base_close) if idx63 < n else None
        rows.append({"date": d, "b": b, "n_avail": n_avail, "up_21d": up_21d, "up_63d": up_63d})
    return rows


def bucket_label(b):
    if b < BUCKET_LOW_MAX:
        return "low"
    if b > BUCKET_HIGH_MIN:
        return "high"
    return "mid"


BUCKET_DESC = {
    "low": f"廣度低：b < {BUCKET_LOW_MAX}（參與度低，洗盤區）",
    "mid": f"廣度中性：{BUCKET_LOW_MAX} ≤ b ≤ {BUCKET_HIGH_MIN}",
    "high": f"廣度高：b > {BUCKET_HIGH_MIN}（參與度高，廣度強）",
}


def _cell_stats(rows, key):
    """rows 中 key（"up_21d"／"up_63d"）非 None 的子集算 n／freq。"""
    vals = [r[key] for r in rows if r[key] is not None]
    n = len(vals)
    if n == 0:
        return {"n": 0, "freq": None}
    return {"n": n, "freq": round(sum(1 for v in vals if v) / n, 3)}


def build_bucket_table(sample_rows):
    buckets = {k: [] for k in ("low", "mid", "high")}
    for r in sample_rows:
        buckets[bucket_label(r["b"])].append(r)

    table = {}
    for k in ("low", "mid", "high"):
        rows = buckets[k]
        s21 = _cell_stats(rows, "up_21d")
        s63 = _cell_stats(rows, "up_63d")
        b_vals = [r["b"] for r in rows]
        table[k] = {
            "n_21d": s21["n"],
            "n_63d": s63["n"],
            "freq_up_21d": s21["freq"],
            "freq_up_63d": s63["freq"],
            "b_range": [round(min(b_vals), 2), round(max(b_vals), 2)] if b_vals else None,
            "description": BUCKET_DESC[k],
        }
    return table


def compute_pooled(sample_rows):
    s21 = _cell_stats(sample_rows, "up_21d")
    s63 = _cell_stats(sample_rows, "up_63d")
    return {"n_21d": s21["n"], "n_63d": s63["n"],
            "freq_up_21d": s21["freq"], "freq_up_63d": s63["freq"]}


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="市場廣度 base rate builder（forecast ledger P2 package G2 機械餵料）")
    ap.add_argument("--skip-fetch", action="store_true", help="離線：只用本地快取重算")
    ap.add_argument("--out", default=str(OUT_JSON), help="輸出路徑（測試用；預設 data/breadth_base_rates.json）")
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
    spy_bars = bars[SPY_TICKER]
    sector_bars = {t: bars[t] for t in SECTOR_TICKERS}

    breadth_series = build_breadth_series(sector_bars)
    if len(breadth_series) < 60:
        raise SystemExit(f"breadth 可算樣本僅 {len(breadth_series)} 筆（可用檔數 ≥{MIN_AVAILABLE_SECTORS} 的日子），過少，中止")

    monthly_samples = sample_first_trading_day_of_month(breadth_series)
    sample_rows = build_transition_sample(monthly_samples, spy_bars)
    if not sample_rows:
        raise SystemExit("可驗證的月度取樣點為 0，中止")

    bucket_table = build_bucket_table(sample_rows)
    pooled = compute_pooled(sample_rows)
    p_clim = {"breadth_spy_up_21d": pooled["freq_up_21d"], "breadth_spy_up_63d": pooled["freq_up_63d"]}

    n_samples = len(sample_rows)
    thin_buckets = [k for k in ("low", "high")
                    if bucket_table[k]["n_21d"] < MIN_CELL_N or bucket_table[k]["n_63d"] < MIN_CELL_N]

    payload = {
        "schema": SCHEMA,
        "tickers": TICKERS,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_start": {t: bars[t][0][0] for t in TICKERS},
        "data_end": {t: bars[t][-1][0] for t in TICKERS},
        "n_price_days": {t: len(bars[t]) for t in TICKERS},
        "n_breadth_series": len(breadth_series),
        "n_monthly_samples": len(monthly_samples),
        "n_samples": n_samples,
        "sma_window": SMA_WINDOW,
        "up_21d_trading_days": UP_21D_TRADING_DAYS,
        "up_63d_trading_days": UP_63D_TRADING_DAYS,
        "min_available_sectors": MIN_AVAILABLE_SECTORS,
        "min_cell_n": MIN_CELL_N,
        "cuts": {"low_max": BUCKET_LOW_MAX, "high_min": BUCKET_HIGH_MIN},
        "buckets": bucket_table,
        "pooled": pooled,
        "p_clim": p_clim,
        "definition": (
            f"b_t = 100 × (收盤 > 自身 {SMA_WINDOW} 日簡單均線 的類股 ETF 檔數) ÷ "
            f"(當日有 ≥ {SMA_WINDOW} 根 bar 的類股 ETF 檔數)；母體 11 檔 SPDR：{', '.join(SECTOR_TICKERS)}；"
            f"可用檔數 < {MIN_AVAILABLE_SECTORS} 的日子不取樣。取樣點＝SPY 每月首個交易日 t；"
            "結果＝SPY 收盤(t+21／63 個 SPY 自身交易日) > 收盤(t)，21d／63d 各自獨立計數"
            "（尾端不足者該窗不計，不影響另一窗）。桶為 PREREG 固定門檻（非資料推算切點）："
            f"low b<{BUCKET_LOW_MAX} ／ mid {BUCKET_LOW_MAX}≤b≤{BUCKET_HIGH_MIN} ／ high b>{BUCKET_HIGH_MIN}。"
        ),
        "note": (
            "重疊樣本，非獨立樣本：月頻取樣降低但未消除 21/63 交易日前瞻視窗的跨月重疊，本表只報告"
            "經驗頻率與樣本數，不做假設檢定。固定門檻非資料切點：low/high 桶樣本量取決於歷史上廣度"
            "觸及極端值的頻率，可能明顯薄於 mid 桶；cell n < "
            f"{MIN_CELL_N} 時 producer 以 pooled 取代（"
            f"{'本次重建薄桶：' + ', '.join(thin_buckets) if thin_buckets else '本次重建三桶皆達門檻，未觸發 pooled 退回'}"
            "）。XLRE（2015 上市）／XLC（2018 上市）在各自上市初期累計根數不足 50 時暫不計入分母，"
            "屬預期行為非資料缺陷。無 stooq fallback（yfinance 失敗時沿用既有本地快取並 warn）。"
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path} — {n_samples} 筆可驗證月度觀測，"
         f"breadth 序列 {breadth_series[0][0]}..{breadth_series[-1][0]}（{len(breadth_series)} 筆）")
    info(f"  cuts={payload['cuts']}")
    for k in ("low", "mid", "high"):
        t = bucket_table[k]
        info(f"  {k}: n_21d={t['n_21d']:<4} n_63d={t['n_63d']:<4} "
             f"freq_up_21d={t['freq_up_21d']} freq_up_63d={t['freq_up_63d']} range={t['b_range']}")
    info(f"  pooled={pooled}")
    info(f"  p_clim={p_clim}")


if __name__ == "__main__":
    main()
