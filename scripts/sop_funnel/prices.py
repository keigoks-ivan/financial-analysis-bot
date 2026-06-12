#!/usr/bin/env python3
"""SOP 漏斗價格層 — 寬表 + CI 每日切片 in-memory stitch + SPY benchmark cache。

價格基底：data/state_machine_cache/study_closes_wide_latest.csv.gz（態④研究維護的
226 檔日收盤寬表，yfinance auto_adjust=True 含息調整）+ docs/.../study/closes_daily/
forward 切片（CI Tue-Sat commit）。本模組只讀不寫寬表（寬表歸 run_study.py 管）。

含息調整 caveat：股息使歷史價下移 → ATH / 52週線訊號可能比看盤圖表早觸發；
美股成長股影響可忽略，TW 高息股偏移 ~1-2%/年。頁面 caveat 區明標。

SPY benchmark：docs/dd-screener/sop-funnel/benchmark.json。首跑 yfinance 抓全史，
之後增量；抓取失敗沿用舊 cache 並標 stale（alpha 只用兩端皆有 SPY 收盤的日期）。
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WIDE_PATH = REPO_ROOT / "data" / "state_machine_cache" / "study_closes_wide_latest.csv.gz"
SLICES_DIR = REPO_ROOT / "docs" / "dd-screener" / "state-machine" / "data" / "study" / "closes_daily"
OUT_DIR = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel"
BENCHMARK_PATH = OUT_DIR / "benchmark.json"
BENCHMARK_TICKER = "SPY"

# IBKR USD 閒置資金利率 = BM − 0.5%（NAV>$100k 級距）。BM 以 ^IRX（13週國庫券殖利率）
# 為基準自動帶 — 與 SPY 同走 yfinance（CI 已驗證可達）；^IRX−0.5 現值 ≈ IBKR 公告 3.12%。
CASH_RATE_PATH = OUT_DIR / "cash_rate.json"
CASH_BM_TICKER = "^IRX"
CASH_SPREAD_PCT = 0.5
CASH_APR_FALLBACK_PCT = 3.12   # 取不到時保底（IBKR 2026-06-05 公告 USD 值）


def load_closes() -> pd.DataFrame:
    """寬表 + 切片 → 最新日收盤寬表（in-memory，不落地）。

    Stitch 邏輯參照 run_study.rebuild_from_slices()：切片日期已在寬表內則覆寫同值。
    """
    if not WIDE_PATH.exists():
        raise SystemExit(f"找不到寬表 {WIDE_PATH}；先跑 run_study.py --refresh-only 建 base。")
    closes = pd.read_csv(WIDE_PATH, index_col=0, parse_dates=True)
    files = sorted(SLICES_DIR.glob("*.json")) if SLICES_DIR.exists() else []
    for f in files:
        try:
            rec = json.loads(f.read_text(encoding="utf-8")).get("closes", {})
        except Exception as exc:  # 壞切片不擋全局
            print(f"  WARN: 略過壞切片 {f.name}: {exc}", file=sys.stderr)
            continue
        for tk, cell in rec.items():
            ts = pd.Timestamp(cell["date"])
            if tk not in closes.columns:
                closes[tk] = pd.NA
            closes.loc[ts, tk] = cell["close"]
    closes = closes.apply(pd.to_numeric, errors="coerce").sort_index()
    return closes


def load_benchmark(refresh: bool = True) -> tuple[pd.Series, bool]:
    """回傳 (SPY 日收盤 Series, is_stale)。refresh=False 時純讀 cache（測試用）。"""
    cache: dict = {}
    if BENCHMARK_PATH.exists():
        try:
            cache = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
        except Exception:
            cache = {}
    closes: dict[str, float] = dict(cache.get("closes", {}))
    stale = False

    if refresh:
        try:
            import yfinance as yf
            period = "1mo" if closes else "max"
            hist = yf.Ticker(BENCHMARK_TICKER).history(period=period, auto_adjust=True)
            if hist is None or hist.empty:
                raise RuntimeError("yfinance 回傳空資料")
            for d, row in hist["Close"].items():
                v = float(row)
                if v == v and v > 0:   # 排除 nan / 空 bar（曾汙染 cache 造成 α=nan）
                    closes[pd.Timestamp(d).strftime("%Y-%m-%d")] = round(v, 4)
            BENCHMARK_PATH.parent.mkdir(parents=True, exist_ok=True)
            BENCHMARK_PATH.write_text(json.dumps({
                "ticker": BENCHMARK_TICKER,
                "source": "yfinance auto_adjust=True",
                "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "closes": dict(sorted(closes.items())),
            }, ensure_ascii=False), encoding="utf-8")
        except Exception as exc:
            print(f"  WARN: SPY benchmark 更新失敗（沿用舊 cache）: {exc}", file=sys.stderr)
            stale = True

    if not closes:
        return pd.Series(dtype=float), True
    ser = pd.Series({pd.Timestamp(k): v for k, v in closes.items()}).sort_index()
    ser = ser[ser.notna() & (ser > 0)]
    return ser, stale


def load_cash_rate(refresh: bool = True) -> dict:
    """IBKR USD 閒置資金利率（%）— BM(^IRX) − 0.5%，自動跟基準。

    refresh=True 時抓 ^IRX 最新殖利率重算並寫 cache；失敗或 refresh=False 沿用 cache；
    無 cache 用 CASH_APR_FALLBACK_PCT 保底。回傳 dict 含 apr/bm/spread/source/stale。
    """
    cache: dict = {}
    if CASH_RATE_PATH.exists():
        try:
            cache = json.loads(CASH_RATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            cache = {}
    bm = cache.get("bm")
    apr = cache.get("ibkr_apr_pct")
    asof = cache.get("bm_asof")
    stale = bool(cache)

    if refresh:
        try:
            import yfinance as yf
            hist = yf.Ticker(CASH_BM_TICKER).history(period="5d")["Close"].dropna()
            if hist is None or hist.empty:
                raise RuntimeError("yfinance 回傳空資料")
            bm = round(float(hist.iloc[-1]), 3)
            apr = round(max(0.0, bm - CASH_SPREAD_PCT), 3)
            asof = pd.Timestamp(hist.index[-1]).strftime("%Y-%m-%d")
            CASH_RATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            CASH_RATE_PATH.write_text(json.dumps({
                "ibkr_apr_pct": apr, "bm": bm, "bm_ticker": CASH_BM_TICKER,
                "bm_asof": asof, "spread_pct": CASH_SPREAD_PCT,
                "source": f"{CASH_BM_TICKER} − {CASH_SPREAD_PCT}%（IBKR USD BM-0.5%）",
                "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }, ensure_ascii=False), encoding="utf-8")
            stale = False
        except Exception as exc:
            print(f"  WARN: 現金利率 {CASH_BM_TICKER} 更新失敗（沿用 cache/保底）: {exc}",
                  file=sys.stderr)
            stale = True

    if apr is None:
        return {"ibkr_apr_pct": CASH_APR_FALLBACK_PCT, "bm": None,
                "bm_ticker": CASH_BM_TICKER, "spread_pct": CASH_SPREAD_PCT,
                "source": "fallback（IBKR 公告值）", "bm_asof": None, "stale": True}
    return {"ibkr_apr_pct": apr, "bm": bm, "bm_ticker": CASH_BM_TICKER,
            "spread_pct": CASH_SPREAD_PCT,
            "source": f"{CASH_BM_TICKER} − {CASH_SPREAD_PCT}%", "bm_asof": asof,
            "stale": stale}


def benchmark_ret_pct(spy: pd.Series, d0: pd.Timestamp, d1: pd.Timestamp) -> float | None:
    """SPY 在 [d0, d1] 的報酬%。兩端取 ≤ 該日的最近收盤；缺資料回 None。"""
    if spy is None or spy.empty:
        return None
    s0 = spy.loc[:d0]
    s1 = spy.loc[:d1]
    if s0.empty or s1.empty:
        return None
    return (float(s1.iloc[-1]) / float(s0.iloc[-1]) - 1.0) * 100.0
