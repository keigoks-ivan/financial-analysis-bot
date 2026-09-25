#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""22 檔主動式 ETF 分析模組共用的股價/成交量快取——所有曾被任一基金持有過的
個股 + 0050(元大台灣50,.TW)+ 台股加權指數(^TWII)的日收盤價與成交量。

儲存:單一 JSONL 檔 data/active_etf/prices.jsonl,每行一個交易日的橫斷面:
    {"date": "2026-09-24",
     "close":  {"2330.TW": 1230.0, ...},
     "volume": {"2330.TW": 12345678, ...}}
依日期升冪排序、append-only(FULL/backfill 補歷史時會重寫整檔以維持排序+去重,
PRICE 模式每日只在尾端新增一行)。選這個格式(而非每檔一個檔案)是因為 22 檔基金
持股高度重疊(354 檔個股 vs. 逐檔各開一檔會是 354 個小檔案),一行代表「這一天
全市場所有我們關心的股票收盤+量」,跟 data/active_etf/aum/{date}.json 的「一天
一份橫斷面」慣例一致,對 git diff 也友善(新的一天只多一行)。

重用 scripts/etf_dash/build_etf_dash.py 的 yf_call_with_backoff()(429 退避重試),
不重寫這段機械;批次下載邏輯是本檔自己的(需要 Volume,etf_dash 的
fetch_prices_batch() 只抓 Close)。
"""
from __future__ import annotations

import datetime
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "etf_dash"))
import build_etf_dash as etfdash  # noqa: E402 — 只借用 yf_call_with_backoff()

import pandas as pd  # noqa: E402
import yfinance as yf  # noqa: E402

PRICES_PATH = REPO_ROOT / "data" / "active_etf" / "prices.jsonl"

BENCH_0050 = "0050.TW"
BENCH_TAIEX = "^TWII"

BATCH_CHUNK_SIZE = 150
BATCH_PACING_S = 1.0


def load_price_history() -> dict:
    """回傳 {date: {"close": {...}, "volume": {...}}},依日期字串排序(dict 在
    Python 3.7+ 保留插入順序,寫入前已排序過)。檔案不存在回空 dict。"""
    if not PRICES_PATH.exists():
        return {}
    out = {}
    for line in PRICES_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        out[rec["date"]] = {"close": rec.get("close") or {}, "volume": rec.get("volume") or {}}
    return out


def save_price_history(history: dict) -> None:
    PRICES_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for date in sorted(history):
        rec = history[date]
        lines.append(json.dumps({"date": date, "close": rec["close"], "volume": rec["volume"]},
                                 ensure_ascii=False, sort_keys=True))
    PRICES_PATH.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def build_ticker_series(history: dict) -> dict:
    """把 {date: {close,volume}} 橫斷面轉置成 {ticker: [(date, close, volume), ...]}
    (依日期升冪),供逐檔取用(報酬率、20 日均量等)。"""
    series: dict = {}
    for date in sorted(history):
        rec = history[date]
        closes, vols = rec["close"], rec["volume"]
        for t, c in closes.items():
            if c is None:
                continue
            series.setdefault(t, []).append((date, c, vols.get(t)))
    return series


def _download_chunk(tickers, start):
    return etfdash.yf_call_with_backoff(
        lambda: yf.download(tickers, start=start, group_by="ticker", progress=False,
                             auto_adjust=False, threads=True),
        label="active-etf price batch ({} tickers)".format(len(tickers)))


def fetch_prices(tickers: list, start_date: str) -> dict:
    """批次下載 tickers(含 0050.TW/^TWII 若在清單內)從 start_date 起的日收盤/量,
    回傳 {date: {"close": {...}, "volume": {...}}}。沒抓到資料的 ticker 直接不
    出現(呼叫端合併時視為缺席,不是 0)。"""
    uniq = sorted(set(tickers))
    out: dict = {}
    chunks = [uniq[i:i + BATCH_CHUNK_SIZE] for i in range(0, len(uniq), BATCH_CHUNK_SIZE)]

    def _record(date_str, tk, close_v, vol_v):
        if pd.isna(close_v):
            return
        rec = out.setdefault(date_str, {"close": {}, "volume": {}})
        rec["close"][tk] = round(float(close_v), 4)
        if vol_v is not None and not pd.isna(vol_v):
            rec["volume"][tk] = int(vol_v)

    for i, chunk in enumerate(chunks):
        if i:
            time.sleep(BATCH_PACING_S)
        df = _download_chunk(chunk, start_date)
        if df is None or df.empty:
            continue
        if len(chunk) == 1 or not isinstance(df.columns, pd.MultiIndex):
            tk = chunk[0]
            if "Close" not in df.columns:
                continue
            vol = df["Volume"] if "Volume" in df.columns else None
            for idx, close_v in df["Close"].items():
                date_str = idx.strftime("%Y-%m-%d")
                _record(date_str, tk, close_v, vol.loc[idx] if vol is not None else None)
            continue
        top_level = set(df.columns.get_level_values(0))
        for tk in chunk:
            if tk not in top_level:
                continue
            sub = df[tk]
            if "Close" not in sub.columns:
                continue
            for idx, close_v in sub["Close"].items():
                date_str = idx.strftime("%Y-%m-%d")
                _record(date_str, tk, close_v, sub["Volume"].loc[idx] if "Volume" in sub.columns else None)
    return out


def merge_history(base: dict, new: dict) -> dict:
    """把 new 併入 base(同一天同一檔以 new 為準——重抓通常是同一天資料更完整
    或修正)。不改動 base,回傳新 dict。"""
    out = {d: {"close": dict(rec["close"]), "volume": dict(rec["volume"])} for d, rec in base.items()}
    for date, rec in new.items():
        cur = out.setdefault(date, {"close": {}, "volume": {}})
        cur["close"].update(rec["close"])
        cur["volume"].update(rec["volume"])
    return out


def update_prices(tickers: list, mode: str, earliest_needed: str | None = None) -> dict:
    """呼叫端入口:mode="full" 時從 earliest_needed(或現有快取最早日期往前推 70
    個交易日≈100 個日曆天,沒有既有快取則用 earliest_needed)重抓整段歷史並
    與既有快取合併;mode="price" 時只抓最近 10 個日曆天(涵蓋週末/假日補齊)
    append 到既有快取。回傳合併後完整的 history(已寫檔)。"""
    history = load_price_history()
    today = datetime.date.today()
    if mode == "full":
        if earliest_needed:
            start = (datetime.date.fromisoformat(earliest_needed) - datetime.timedelta(days=100)).isoformat()
        elif history:
            start = min(history)
        else:
            start = (today - datetime.timedelta(days=270)).isoformat()
        new = fetch_prices(tickers, start)
    else:
        start = (today - datetime.timedelta(days=10)).isoformat()
        new = fetch_prices(tickers, start)
    merged = merge_history(history, new)
    save_price_history(merged)
    return merged
