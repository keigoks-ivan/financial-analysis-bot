#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兩檔配法比較器（/etf-dash/compare.html）的資料檔。

輸出 docs/etf-dash/data/compare_series.json（schema compare-series-v1）：
  - 21 檔每日「美元含息還原指數」（各檔第一個有資料日＝1），日期對齊到美國交易日（SPY 的交易日）。
    台幣、日圓計價的 0050、TAIEX、TOPIX 用同一天的匯率（TWD=X、JPY=X，1 美元兌當地貨幣）換成美元，
    再順延到美國交易日。TAIEX 是價格指數，不含息，不能買，只當對照。
  - 基準 SPY 回檔 ≥10% 的區段（峰、谷、回前高日）。
  - 持股重疊矩陣，讀 data/etf_dash/picks_candidates.json 的 overlap。
資料格式為「日期陣列＋各檔 {i0, v}」：i0 是該檔第一個值對應 dates 的位置，v 是從 i0 起的指數值。

候選清單（鍵與 yf_ticker）沿用 scripts/etf_dash/picks_candidates.py 的同一套：從
data/etf_dash/picks_candidates.json 的 funds[] 讀（key、yf_ticker、currency、label_zh）。

價格來源：
  --source yfinance     預設，雲端 CI 用（Yahoo 的 Adj Close＝含息還原）。
  --source price_store  本機開發與驗證用，讀 ~/v7-backtest/src/price_store.py 的共用正本，缺的才下載。

已知壞資料處理見 compare_common.py（1475.T 兩個壞 K 棒、2024-08-09 壞配息係數）。
0050.TW 若在美股交易日沒有 bar（例如 2026-10-26），以前一日順延。

用法：python3 scripts/etf_dash/build_compare_data.py [--source price_store] [--out PATH]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare_common as cc  # noqa: E402

REPO_ROOT = cc.REPO_ROOT
CAND_PATH = REPO_ROOT / "data" / "etf_dash" / "picks_candidates.json"
OUT_PATH = REPO_ROOT / "docs" / "etf-dash" / "data" / "compare_series.json"
BENCH = "SPY"
FX_TICKER = {"TWD": "TWD=X", "JPY": "JPY=X"}
HISTORY_START = "1999-01-01"
FETCH_START = "1998-01-01"


def last_closed_date(now: datetime.datetime | None = None) -> datetime.date:
    """美股最後一個已收盤的交易日上界：紐約時間 16:30 前，今天的 K 棒算盤中，不用。"""
    from zoneinfo import ZoneInfo
    now = (now or datetime.datetime.now(datetime.timezone.utc)).astimezone(ZoneInfo("America/New_York"))
    d = now.date()
    if now.hour < 16 or (now.hour == 16 and now.minute < 30):
        d -= datetime.timedelta(days=1)
    return d


def short_label(key: str, label_zh: str) -> str:
    name = label_zh.split("（")[0].strip()
    return name if name.startswith(key) or key in name else f"{key}｜{name}"


def build(source: str) -> dict:
    cand = json.loads(CAND_PATH.read_text(encoding="utf-8"))
    funds = cand["funds"]
    notes: list[str] = []
    fx: dict[str, pd.Series] = {}
    for cur, tk in FX_TICKER.items():
        fx[cur] = cc.load_bars(tk, source, FETCH_START)["close"]

    bars: dict[str, pd.DataFrame] = {}
    for f in funds:
        b = cc.load_bars(f["yf_ticker"], source, FETCH_START)
        if f["yf_ticker"] == "1475.T":
            b = cc.fix_topix(b, notes)
        bars[f["key"]] = b

    spy = bars[BENCH]
    cutoff = pd.Timestamp(last_closed_date())
    cal = spy.index[(spy.index >= pd.Timestamp(HISTORY_START)) & (spy.index <= cutoff)]

    series = {}
    meta = {}
    floats: dict[str, pd.Series] = {}
    for f in funds:
        key, cur = f["key"], f["currency"]
        b = bars[key]
        adj = b["adj_close"]
        if cur in fx:
            rate = fx[cur].reindex(fx[cur].index.union(adj.index)).ffill().reindex(adj.index)
            adj = adj / rate
        usd = adj.reindex(adj.index.union(cal)).ffill().reindex(cal)
        usd = usd.where(usd.index >= adj.index[0])
        comp, norm = cc.to_compact(usd, cal)
        floats[key] = norm
        last_real = adj.index[adj.index <= cal[-1]][-1]
        comp["last_real"] = last_real.strftime("%Y-%m-%d")
        series[key] = comp
        meta[key] = {"label": short_label(key, f["label_zh"]), "ticker": f["yf_ticker"], "currency": cur,
                     "total_return": key != "TAIEX"}

    for key, m in meta.items():
        series[key].update(m)
    notes.append("0050、TAIEX、TOPIX 以當地交易日的收盤與同日匯率換成美元，再順延到美國交易日；"
                 "當地沒有 bar 的美國交易日以前一日順延。")
    notes.append("TAIEX 是價格指數，不含息，也不能買，只當對照。")
    stale = [f"{k}（最後資料 {s['last_real']}）" for k, s in series.items()
             if (cal[-1] - pd.Timestamp(s["last_real"])).days > 3]
    if stale:
        notes.append("以下基金的最後一根 bar 比最新日早超過 3 天，之後以持平處理：" + "、".join(stale) + "。")

    episodes = cc.drawdown_episodes(floats[BENCH])
    return {
        "schema": cc.SCHEMA,
        "market": "etf-dash",
        "generated_at": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec="seconds"),
        "source": source,
        "currency": "USD",
        "scale": cc.SCALE,
        "benchmark": BENCH,
        "as_of": cal[-1].strftime("%Y-%m-%d"),
        "dates": [d.strftime("%Y-%m-%d") for d in cal],
        "funds": series,
        "episodes": episodes,
        "overlap": cand.get("overlap") or {},
        "overlap_as_of": cand.get("as_of"),
        "notes": notes,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["price_store", "yfinance"], default="yfinance")
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()
    payload = build(args.source)
    n = cc.write_json(Path(args.out), payload)
    print(f"wrote {args.out}  {n / 1024:.0f} KB  funds={len(payload['funds'])} days={len(payload['dates'])} "
          f"as_of={payload['as_of']} episodes={len(payload['episodes'])}")


if __name__ == "__main__":
    main()
