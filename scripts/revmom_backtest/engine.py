"""Weights engine (docs/RevMom_Backtest_Spec.md §3): no capital, fractional positions, NAV starts at 1.0.

- A signal on day d trades at the next trading day's open. Target = equal weight, at most 10% per name,
  cash for empty slots. Existing names are resized to target, dropped names are sold.
- Total return: each day a position moves by mark / ref (dividends reinvested in the same name).
- Costs per side on traded value: fee (both sides) + slippage (both sides) + transaction tax (sells).
- lock=True: an order cannot fill on a day with no trade, or when the open is locked at the limit
  (high == low == open at limit-up for buys, limit-down for sells). It retries at later opens until
  the next signal replaces it. The daily limit was 7% before 2015-06-01 and 10% after.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

LIMIT_10PCT_FROM = pd.Timestamp("2015-06-01")


@dataclass
class Cost:
    fee: float = 0.001425 * 0.3
    tax: float = 0.003
    slip: float = 0.001          # 10 bp per side


def tick_size(p: float) -> float:
    return 0.01 if p < 10 else 0.05 if p < 50 else 0.1 if p < 100 else 0.5 if p < 500 else 1.0 if p < 1000 else 5.0


def limit_prices(ref: float, t: pd.Timestamp) -> tuple:
    rate = 0.10 if t >= LIMIT_10PCT_FROM else 0.07
    up_raw, dn_raw = ref * (1 + rate), ref * (1 - rate)
    tu, td = tick_size(up_raw), tick_size(dn_raw)
    return np.floor(up_raw / tu + 1e-9) * tu, np.ceil(dn_raw / td - 1e-9) * td


def run(pn, sels: dict, start, end, cost: Cost = Cost(), lock: bool = True, single: str | None = None,
        track: bool = False):
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    dates = pn.dates[(pn.dates >= start) & (pn.dates <= end)]
    exec_map = {}
    for d, picks in sels.items():
        i = pn.dates.searchsorted(d, side="right")
        if i < len(pn.dates) and start <= pn.dates[i] <= end:
            exec_map[pn.dates[i]] = picks
    if single is not None:
        exec_map = {dates[0]: [single]}
    val, cash, target, pending = {}, 1.0, {}, set()
    rows, trades = [], []
    for t in dates:
        mt, rt = pn.mark.loc[t], pn.ref.loc[t]
        if t in exec_map or pending:
            om, hm, lm, vm = pn.open.loc[t], pn.high.loc[t], pn.low.loc[t], pn.value.loc[t]

            def px_open(c):
                o, r = om.get(c, np.nan), rt.get(c, np.nan)
                return o if o == o else r

            for c in val:                                   # previous close -> today's open
                o, r = px_open(c), rt.get(c, np.nan)
                if o == o and r == r and r > 0:
                    val[c] *= o / r
            if t in exec_map:
                picks = exec_map[t]
                w = 1.0 if single is not None else (min(1.0 / len(picks), 0.10) if picks else 0.0)
                target = {c: w for c in picks}
                pending = set(val) | set(picks)
            E = cash + sum(val.values())

            def blocked(c, side):
                if not lock:
                    return False
                o, h, lo_, v, r = om.get(c, np.nan), hm.get(c, np.nan), lm.get(c, np.nan), vm.get(c, np.nan), rt.get(c, np.nan)
                if not (o == o and v == v and v > 0):
                    return True                             # no trade today
                if r == r and h == lo_ == o:
                    up, dn = limit_prices(r, t)
                    return (side == "buy" and o >= up - 1e-9) or (side == "sell" and o <= dn + 1e-9)
                return False

            still = set()
            for c in sorted(pending):                       # sells first
                amt = val.get(c, 0.0) - target.get(c, 0.0) * E
                if amt > 1e-12:
                    if blocked(c, "sell"):
                        still.add(c)
                        continue
                    cash += amt * (1 - cost.fee - cost.tax - cost.slip)
                    val[c] -= amt
                    trades.append((t, c, "sell", amt / E))
            for c in sorted(pending):
                amt = target.get(c, 0.0) * E - val.get(c, 0.0)
                if amt > 1e-12:
                    if blocked(c, "buy"):
                        still.add(c)
                        continue
                    amt = min(amt, cash / (1 + cost.fee + cost.slip))
                    if amt <= 1e-12:
                        continue
                    cash -= amt * (1 + cost.fee + cost.slip)
                    val[c] = val.get(c, 0.0) + amt
                    trades.append((t, c, "buy", amt / E))
            pending = still
            val = {c: v for c, v in val.items() if v > 1e-12}
            for c in val:                                   # today's open -> close
                o, m = px_open(c), mt.get(c, np.nan)
                if o == o and m == m and o > 0:
                    val[c] *= m / o
        else:
            for c in val:
                m, r = mt.get(c, np.nan), rt.get(c, np.nan)
                if m == m and r == r and r > 0:
                    val[c] *= m / r
        nav = cash + sum(val.values())
        rows.append((t, nav, sum(val.values()) / nav if nav > 0 else 0.0, len(val), len(pending))
                    + ((",".join(sorted(val)),) if track else ()))
    cols = ["date", "nav", "exposure", "n_hold", "n_pending"] + (["held"] if track else [])
    daily = pd.DataFrame(rows, columns=cols).set_index("date")
    tr = pd.DataFrame(trades, columns=["date", "code", "side", "weight"])
    return daily, tr
