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


def benchmark_ret_pct(spy: pd.Series, d0: pd.Timestamp, d1: pd.Timestamp) -> float | None:
    """SPY 在 [d0, d1] 的報酬%。兩端取 ≤ 該日的最近收盤；缺資料回 None。"""
    if spy is None or spy.empty:
        return None
    s0 = spy.loc[:d0]
    s1 = spy.loc[:d1]
    if s0.empty or s1.empty:
        return None
    return (float(s1.iloc[-1]) / float(s0.iloc[-1]) - 1.0) * 100.0
