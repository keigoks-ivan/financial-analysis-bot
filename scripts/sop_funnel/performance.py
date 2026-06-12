#!/usr/bin/env python3
"""SOP 漏斗績效層 — 從 start_date 起、起始資金固定的策略淨值 vs SPY。

設計（遵守所有交易設定）：
- 每筆 entered/closed trade 的日 MTM 直接由 simulate_trade 寫下的 legs 重建
  （態③減1/3 / 態④減碼+回補 / 態⑤全出 都已記在 legs），不重寫狀態機邏輯 →
  與 §3/§4 的 sim 經濟學完全一致。
- 部位金額 = 進場時建議部位% × 當下個股部淨值（running NAV，循環以時序解開：
  trade 進場當日自身 P&L=0，故進場日 NAV 只含先前 trade + 現金）。
- 未投入現金照 IBKR 閒置資金利率計息（USD 3.12% p.a.，2026-06-05；NAV>$100k 級距、
  $10,000 以上計息），逐日 Actual/360 累計（含週末日曆日）。
- NAV(t) = 現金(t, 含利息) + Σ 持倉市值(t)。基準 SPY 同起始資金、start_date 為基期。
  x 軸取 SPY 交易日（兩端對齊）。
"""
from __future__ import annotations

from collections import defaultdict

import pandas as pd

# IBKR USD 閒置資金利率（2026-06-05；NAV>$100k 享全額 BM-0.5%），餘額 > $10,000 計息
CASH_APR_DEFAULT = 0.0312
CASH_FLOOR_DEFAULT = 10_000.0


def _leg_schedule(legs: list[dict]) -> dict[str, list[dict]]:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for lg in legs or []:
        by_date[lg["date"]].append(lg)
    return by_date


def compute(events: list[dict], closes: pd.DataFrame, spy: pd.Series,
            start_date: str, capital: float = 1_000_000.0,
            cash_apr: float = CASH_APR_DEFAULT,
            cash_floor: float = CASH_FLOOR_DEFAULT) -> dict | None:
    """產出策略 NAV vs SPY 日序列 + 摘要（含現金利息）。資料不足回 None。"""
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

    def px_at(ticker: str, d: pd.Timestamp) -> float | None:
        sub = closes[ticker][closes[ticker].index <= d].dropna()
        return float(sub.iloc[-1]) if len(sub) else None

    # 每筆 trade 的可變帳：fraction（1.0=初始部位）+ 美元投入/賣出
    st = []
    for ev in trades:
        st.append({
            "ev": ev, "p0": float(ev["sim"]["entry_close"]),
            "entry": pd.Timestamp(ev["entry_date"]),
            "sched": _leg_schedule(ev["sim"].get("legs")),
            "opened": False, "frac": 0.0, "shares_unit": 0.0,
            "invested": 0.0, "proceeds": 0.0, "alloc": 0.0,
            "pos_pct": float(ev["sim"].get("suggested_position_pct") or 0.0),
        })

    cash = capital
    interest_total = 0.0
    prev = None
    series = []
    for d in axis:
        # 1) 閒置現金計息（日曆日，Actual/360，$10k 以上）
        if prev is not None and cash_apr > 0:
            days = (d - prev).days
            earn = max(0.0, cash - cash_floor) * cash_apr * days / 360.0
            cash += earn
            interest_total += earn
        # 2) 當日進場：部位 = pos% × 當下個股部淨值
        for s in st:
            if not s["opened"] and s["entry"] == d:
                held_others = sum(
                    o["frac"] * o["shares_unit"] * (px_at(o["ev"]["ticker"], d) or o["p0"])
                    for o in st if o["opened"])
                nav_now = cash + held_others
                s["alloc"] = s["pos_pct"] / 100.0 * nav_now
                s["shares_unit"] = s["alloc"] / s["p0"] if s["p0"] else 0.0
                s["frac"], s["opened"], s["invested"] = 1.0, True, s["alloc"]
                cash -= s["alloc"]
        # 3) 當日 legs（態③/④減碼、態④回補、態⑤全出）→ 現金流
        for s in st:
            if not s["opened"] or s["frac"] <= 1e-9:
                continue
            for lg in s["sched"].get(str(d.date()), []):
                f, pr, reason = lg["fraction"], lg["price"], lg["reason"]
                if "回補" in reason:                       # 買回 → 現金出
                    amt = f * s["shares_unit"] * pr
                    cash -= amt
                    s["frac"] += f
                    s["invested"] += amt
                elif "全出" in reason:                      # 賣光 → 現金入
                    amt = s["frac"] * s["shares_unit"] * pr
                    cash += amt
                    s["proceeds"] += amt
                    s["frac"] = 0.0
                else:                                        # 減碼 qty → 現金入
                    amt = f * s["shares_unit"] * pr
                    cash += amt
                    s["frac"] -= f
                    s["proceeds"] += amt
        # 4) NAV = 現金 + 持倉市值
        held = sum(s["frac"] * s["shares_unit"] * (px_at(s["ev"]["ticker"], d) or s["p0"])
                   for s in st if s["opened"] and s["frac"] > 1e-9)
        nav = cash + held
        series.append({"date": str(d.date()),
                       "nav": round(nav, 2),
                       "spy": round(capital * float(spy.loc[d]) / spy0, 2)})
        prev = d

    end_held = 0.0
    positions = []
    for s in st:
        p = px_at(s["ev"]["ticker"], axis[-1]) or s["p0"]
        hv = s["frac"] * s["shares_unit"] * p
        end_held += hv
        positions.append({
            "ticker": s["ev"]["ticker"], "name": s["ev"].get("name"),
            "entry_type": s["ev"]["entry_type"], "entry_date": s["ev"]["entry_date"],
            "weight_pct": round(s["pos_pct"], 2), "alloc_usd": round(s["alloc"], 0),
            "ret_pct": s["ev"]["sim"].get("ret_pct"),
            "pnl_usd": round(s["proceeds"] + hv - s["invested"], 0),
            "state": s["ev"]["sim"].get("current_state"),
            "status": s["ev"]["status"],
            "exit_date": s["ev"]["sim"].get("exit_date"),
        })

    end_nav = series[-1]["nav"]
    end_spy = series[-1]["spy"]
    end_cash = end_nav - end_held
    summary = {
        "strategy_value": round(end_nav, 0),
        "strategy_ret_pct": round((end_nav / capital - 1) * 100, 2),
        "spy_value": round(end_spy, 0),
        "spy_ret_pct": round((end_spy / capital - 1) * 100, 2),
        "excess_pp": round((end_nav - end_spy) / capital * 100, 2),
        "invested_pct": round(end_held / end_nav * 100, 2),
        "cash_pct": round(end_cash / end_nav * 100, 2),
        "interest_usd": round(interest_total, 0),
        "cash_apr_pct": round(cash_apr * 100, 2),
        "n_positions": len(positions),
    }
    return {
        "start": start_date,
        "capital": capital,
        "benchmark": "SPY",
        "cash_apr_pct": round(cash_apr * 100, 2),
        "as_of": series[-1]["date"],
        "series": series,
        "summary": summary,
        "positions": positions,
    }
