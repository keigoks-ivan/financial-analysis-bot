#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兩檔配法比較器（/active-etf/compare.html）的資料檔。

輸出 docs/active-etf/data/compare_series.json（schema compare-series-v1，與 etf-dash 同格式）：
  - 22 檔主動式 ETF＋0050 每日「台幣含息還原指數」（各檔第一個有資料日＝1，不換匯），
    日期用 0050 的台股交易日。基準 0050。
  - 基準 0050 回檔 ≥10% 的區段（峰、谷、回前高日）。
  - 持股重疊矩陣，讀 data/active_etf/picks_candidates.json 的 overlap（0050 沒有持股資料，重疊顯示空白）。

價格來源：
  --source yfinance     預設，雲端 CI 用（Yahoo 的 Adj Close＝含息還原）。
  --source price_store  本機開發與驗證用，讀 ~/v7-backtest/src/price_store.py 的共用正本。

資料處理：
  1. 成交量為 0 的 bar 整天剔除（Yahoo 在台股休市日補一根與前一日相同的 bar）；
     各檔第一筆有成交量以前的上市初期 bar 保留，起日＝第一根 bar（與站上上市日口徑一致）。
  2. data/active_etf/prices.jsonl 是站上自己抓的每日收盤。同一天同一檔，兩邊收盤差超過 0.3% 時，
     以 prices.jsonl 為準（價格庫最新一天可能是盤中價）；還原價用當日 Adj Close ÷ Close 的係數換算。
  3. picks_dividends.json 的配息只用來核對 Yahoo 還原係數，不另外加進價格。
  4. 起日是 Yahoo 第一根 bar，可能晚於實際掛牌日。

用法：python3 scripts/active_etf/build_compare_data.py [--source price_store] [--out PATH]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "etf_dash"))
import compare_common as cc  # noqa: E402

CAND_PATH = REPO_ROOT / "data" / "active_etf" / "picks_candidates.json"
PRICES_PATH = REPO_ROOT / "data" / "active_etf" / "prices.jsonl"
DIV_PATH = REPO_ROOT / "data" / "active_etf" / "picks_dividends.json"
OUT_PATH = REPO_ROOT / "docs" / "active-etf" / "data" / "compare_series.json"
BENCH_CODE = "0050"
FETCH_START = "2025-01-01"
OVERRIDE_TOL = 0.003


def load_official_close() -> dict[str, dict[str, float]]:
    """prices.jsonl → {ticker: {date: close}}。"""
    out: dict[str, dict[str, float]] = {}
    if not PRICES_PATH.exists():
        return out
    for line in PRICES_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        for tk, c in (r.get("close") or {}).items():
            if c:
                out.setdefault(tk, {})[r["date"]] = float(c)
    return out


def clean_bars(tk: str, bars: pd.DataFrame, official: dict, overrides: dict[str, list[str]]) -> pd.DataFrame:
    b = bars.copy()
    # 休市日的補 bar（成交量 0）整天剔除；但各檔上市初期、第一筆有成交量以前的 bar 保留，
    # 與站上「自上市日起算」的口徑一致
    pos = b.index[b["volume"] > 0]
    first_trade = pos[0] if len(pos) else b.index[0]
    b = b[~((b["volume"] == 0) & (b.index > first_trade))]
    over = []
    for ds, oc in (official.get(tk) or {}).items():
        d = pd.Timestamp(ds)
        if d in b.index:
            c = float(b.loc[d, "close"])
            if c > 0 and abs(oc / c - 1) > OVERRIDE_TOL:
                factor = float(b.loc[d, "adj_close"]) / c
                b.loc[d, "close"] = oc
                b.loc[d, "adj_close"] = oc * factor
                over.append(ds)
    for ds in over:
        overrides.setdefault(ds, []).append(tk.replace(".TW", ""))
    return b


def check_dividends(raw: dict[str, pd.DataFrame], notes: list[str]) -> None:
    if not DIV_PATH.exists():
        return
    divs = json.loads(DIV_PATH.read_text(encoding="utf-8"))
    for tk, m in divs.items():
        b = raw.get(tk)
        if b is None:
            continue
        for ds, amt in m.items():
            d = pd.Timestamp(ds)
            if d not in b.index:
                continue
            i = b.index.get_loc(d)
            if i == 0:
                continue
            r = b["adj_close"] / b["close"]
            prev_close = float(b["close"].iloc[i - 1])
            exp = 1 / (1 - amt / prev_close)  # 除息日 Adj Close ÷ Close 相對前一日的跳動
            got = float(r.iloc[i] / r.iloc[i - 1])
            if abs(got / exp - 1) > 0.005:
                notes.append(f"{tk} {ds} 的配息 {amt} 與 Yahoo 還原係數對不上（預期 {exp:.4f}，實際 {got:.4f}）。")


def build(source: str) -> dict:
    cand = json.loads(CAND_PATH.read_text(encoding="utf-8"))
    names = {f["code"]: f.get("name") or f["code"] for f in cand["funds"]}
    names[BENCH_CODE] = (cand.get("benchmark_row") or {}).get("name") or "元大台灣50"
    codes = sorted(c for c in names if c != BENCH_CODE) + [BENCH_CODE]
    notes: list[str] = []
    official = load_official_close()
    overrides: dict[str, list[str]] = {}

    raw: dict[str, pd.DataFrame] = {}
    bars: dict[str, pd.DataFrame] = {}
    for c in codes:
        tk = c + ".TW"
        raw[tk] = cc.load_bars(tk, source, FETCH_START)
        bars[c] = clean_bars(tk, raw[tk], official, overrides)
    check_dividends(raw, notes)
    for ds in sorted(overrides):
        notes.append(f"{ds}：{len(overrides[ds])} 檔的價格庫收盤與站上 prices.jsonl 差超過 0.3%，以 prices.jsonl 為準。")

    bench = bars[BENCH_CODE]
    # 今天的 bar 若在台北 14:00 前產生，視為盤中，不用
    now_tpe = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    cal_idx = bench.index
    if now_tpe.hour < 14:
        cal_idx = cal_idx[cal_idx < pd.Timestamp(now_tpe.date())]
    first_fund = min(b.index[0] for k, b in bars.items() if k != BENCH_CODE)
    cal = cal_idx[cal_idx >= first_fund]

    series: dict = {}
    floats: dict[str, pd.Series] = {}
    for c in codes:
        adj = bars[c]["adj_close"]
        full = adj.reindex(adj.index.union(cal)).ffill().reindex(cal)
        full = full.where(full.index >= adj.index[0])
        comp, norm = cc.to_compact(full, cal)
        floats[c] = norm
        comp["last_real"] = adj.index[adj.index <= cal[-1]][-1].strftime("%Y-%m-%d")
        comp["label"] = f"{c}｜{names[c]}"
        comp["ticker"] = c + ".TW"
        comp["currency"] = "TWD"
        comp["total_return"] = True
        series[c] = comp

    notes.append("台幣計價，不換匯；日期用 0050 的台股交易日。起日是 Yahoo 第一根 bar，可能晚於實際掛牌日。")
    notes.append("各檔上市後約 6～12 個交易日成交量為 0（Yahoo 只有掛牌參考價），這段保留；之後成交量為 0 的 bar（休市日補值）整天剔除；站上 prices.jsonl 與價格庫收盤差超過 0.3% 的日子以 prices.jsonl 為準。")
    notes.append("0050 沒有持股快照，持股重疊欄顯示空白。")
    stale = [f"{k}（最後資料 {s['last_real']}）" for k, s in series.items()
             if (cal[-1] - pd.Timestamp(s["last_real"])).days > 3]
    if stale:
        notes.append("以下基金的最後一根 bar 比最新日早超過 3 天，之後以持平處理：" + "、".join(stale) + "。")

    return {
        "schema": cc.SCHEMA,
        "market": "active-etf",
        "generated_at": now_tpe.isoformat(timespec="seconds"),
        "source": source,
        "currency": "TWD",
        "scale": cc.SCALE,
        "benchmark": BENCH_CODE,
        "as_of": cal[-1].strftime("%Y-%m-%d"),
        "dates": [d.strftime("%Y-%m-%d") for d in cal],
        "funds": series,
        "episodes": cc.drawdown_episodes(floats[BENCH_CODE]),
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
    for n_ in payload["notes"]:
        print(" -", n_)


if __name__ == "__main__":
    main()
