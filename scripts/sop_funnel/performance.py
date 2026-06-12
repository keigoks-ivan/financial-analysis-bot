#!/usr/bin/env python3
"""SOP 漏斗績效層 — 從 start_date 起、起始資金固定的策略淨值 vs SPY。

設計（遵守所有交易設定）：
- 每筆 entered/closed trade 的日 MTM 直接由 simulate_trade 寫下的 legs 重建
  （態③減1/3 / 態④減碼+回補 / 態⑤全出 都已記在 legs），不重寫狀態機邏輯 →
  與 §3/§4 的 sim 經濟學完全一致。
- 部位金額 = 進場時建議部位% × 當下個股部淨值（running NAV，循環以時序解開：
  trade 進場當日自身 P&L=0，故進場日 NAV 只含先前 trade）。
- 其餘為現金（0% 報酬）。NAV(t) = 起始資金 + Σ 各 trade 到 t 的美元損益。
- 基準 SPY 以同起始資金、start_date 為基期。x 軸取 SPY 交易日（兩端對齊）。
"""
from __future__ import annotations

from collections import defaultdict

import pandas as pd


def _leg_schedule(legs: list[dict]) -> dict[str, list[dict]]:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for lg in legs or []:
        by_date[lg["date"]].append(lg)
    return by_date


def _trade_unit_pnl_series(ev: dict, col: pd.Series, axis: pd.DatetimeIndex) -> dict:
    """回傳 {date: 每股單位損益}（fraction 1.0 = 1 股 @ p0）。重建自 legs。"""
    sim = ev["sim"]
    p0 = float(sim["entry_close"])
    entry = pd.Timestamp(ev["entry_date"])
    sched = _leg_schedule(sim.get("legs"))
    fraction, invested, proceeds = 1.0, p0, 0.0
    out: dict[pd.Timestamp, float] = {}
    for d in axis:
        if d < entry:
            out[d] = 0.0
            continue
        for lg in sched.get(str(d.date()), []):
            qty, price, reason = lg["fraction"], lg["price"], lg["reason"]
            if "回補" in reason:                     # 態④回補：買回
                invested += qty * price
                fraction += qty
            elif "全出" in reason:                   # 態⑤全出：賣光
                proceeds += fraction * price
                fraction = 0.0
            else:                                     # 態③/態④減碼：賣 qty
                proceeds += qty * price
                fraction -= qty
        sub = col[col.index <= d].dropna()
        px = float(sub.iloc[-1]) if len(sub) else p0
        out[d] = (proceeds + fraction * px) - invested   # 每股單位損益
    return out


def compute(events: list[dict], closes: pd.DataFrame, spy: pd.Series,
            start_date: str, capital: float = 1_000_000.0) -> dict | None:
    """產出策略 NAV vs SPY 日序列 + 摘要。資料不足回 None。"""
    start = pd.Timestamp(start_date)
    if spy is None or spy.empty:
        return None
    axis = spy.index[(spy.index >= start) & (spy.index <= closes.index.max())]
    if len(axis) < 2:
        return None
    spy0 = float(spy.loc[axis[0]])

    trades = [e for e in events
              if e.get("status") in ("entered", "closed") and e.get("sim")
              and e.get("entry_date") and e["ticker"] in closes.columns]
    trades.sort(key=lambda e: e["entry_date"])

    # 每筆 trade：單位損益日序列 + 美元 scale（部位金額 ÷ p0）
    unit_series: dict[int, dict] = {}
    dollar_pnl: dict[int, dict] = {}
    positions = []
    for idx, ev in enumerate(trades):
        col = closes[ev["ticker"]]
        unit_series[idx] = _trade_unit_pnl_series(ev, col, axis)
        ed = pd.Timestamp(ev["entry_date"])
        # 進場日個股部淨值（只含先前已配置 trade 的當日損益）
        nav_at_entry = capital + sum(dollar_pnl[j].get(ed, 0.0) for j in dollar_pnl)
        pos_pct = float(ev["sim"].get("suggested_position_pct") or 0.0)
        alloc = pos_pct / 100.0 * nav_at_entry
        p0 = float(ev["sim"]["entry_close"])
        scale = alloc / p0 if p0 else 0.0
        dollar_pnl[idx] = {d: unit_series[idx][d] * scale for d in axis}
        last_pnl = dollar_pnl[idx][axis[-1]]
        positions.append({
            "ticker": ev["ticker"], "name": ev.get("name"),
            "entry_type": ev["entry_type"], "entry_date": ev["entry_date"],
            "weight_pct": round(pos_pct, 2), "alloc_usd": round(alloc, 0),
            "ret_pct": ev["sim"].get("ret_pct"),
            "pnl_usd": round(last_pnl, 0),
            "state": ev["sim"].get("current_state"),
            "status": ev["status"],
            "exit_date": ev["sim"].get("exit_date"),
        })

    series = []
    for d in axis:
        nav = capital + sum(dollar_pnl[j][d] for j in dollar_pnl)
        spv = capital * float(spy.loc[d]) / spy0
        series.append({"date": str(d.date()),
                       "nav": round(nav, 2), "spy": round(spv, 2)})

    invested_pct = sum(p["weight_pct"] for p in positions)
    end_nav = series[-1]["nav"]
    end_spy = series[-1]["spy"]
    summary = {
        "strategy_value": round(end_nav, 0),
        "strategy_ret_pct": round((end_nav / capital - 1) * 100, 2),
        "spy_value": round(end_spy, 0),
        "spy_ret_pct": round((end_spy / capital - 1) * 100, 2),
        "excess_pp": round((end_nav - end_spy) / capital * 100, 2),
        "invested_pct": round(invested_pct, 2),
        "cash_pct": round(100 - invested_pct, 2),
        "n_positions": len(positions),
    }
    return {
        "start": start_date,
        "capital": capital,
        "benchmark": "SPY",
        "as_of": series[-1]["date"],
        "series": series,
        "summary": summary,
        "positions": positions,
    }
