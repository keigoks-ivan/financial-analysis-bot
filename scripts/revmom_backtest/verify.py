"""Checks for the site version -> results/revmom/verify.json.  Run: python3 -m src.revmom_backtest.verify"""
from __future__ import annotations

import dataclasses
import json

import numpy as np
import pandas as pd

from . import data as D
from . import engine as E
from . import signals as S
from .run import OUT, SIG0, START

RESEARCH_FAITHFUL = {"cagr": 0.3670, "mdd": -0.4010}    # research folder V1a faithful_full (weights, author cost)
TRUNC = ["2009-03-11", "2011-08-11", "2013-05-13", "2016-08-11", "2020-05-11", "2024-06-11"]


def truncate(pn, x):
    kw = {}
    for f in dataclasses.fields(pn):
        v = getattr(pn, f.name)
        if f.name == "dates":
            kw[f.name] = v[v <= x]
        elif f.name == "rev":
            kw[f.name] = v.loc[:pd.Period(x, "M") - 1]
        elif isinstance(v, (pd.DataFrame, pd.Series)):
            kw[f.name] = v.loc[:x]
        else:
            kw[f.name] = v
    return dataclasses.replace(pn, **kw)


def main():
    pn = D.load("2007-01-01")
    pre = S.precompute(pn)
    end = pn.dates[-1]
    res = {}
    sels, _ = S.selections(pn, pre, SIG0, end, "V1a")
    # 1. same accounting, universe and end date as the research weights engine -> same numbers
    x_end = pd.Timestamp("2026-09-29")
    sx, _ = S.selections(pn, pre, SIG0, x_end, "V1a", innovation=True)
    d, _ = E.run(pn, sx, START, x_end, E.Cost(fee=0.001425, tax=0.003, slip=0.0), lock=False)
    yrs = (d.index[-1] - d.index[0]).days / 365.25
    res["research_crosscheck"] = {"site_engine": {"cagr": float(d.nav.iloc[-1] ** (1 / yrs) - 1),
                                                  "mdd": float((d.nav / d.nav.cummax() - 1).min())},
                                  "research": RESEARCH_FAITHFUL}
    # 2. truncation: deleting everything after the signal day leaves the picks unchanged
    res["truncation_identical"] = {}
    for x in TRUNC:
        x = pd.Timestamp(x)
        t = truncate(pn, x)
        res["truncation_identical"][str(x.date())] = {
            v: S.select(pn, pre, x, v)[0] == S.select(t, S.precompute(t), x, v)[0] for v in ("V1a", "V1b", "V2")}
    # 3. main run: blocked orders, holdings that stopped trading, beyond-limit moves while held
    daily, _ = E.run(pn, sels, START, end, E.Cost(), track=True)
    res["pending_order_days"] = int((daily.n_pending > 0).sum())
    held_sets = daily.held.fillna("").str.split(",")
    last_listed = pn.listed[::-1].idxmax()
    res["held_at_end_not_trading"] = [c for c in held_sets.iloc[-1] if c and last_listed[c] < end - pd.Timedelta(days=10)]
    moves = []
    prev = set()
    for t, h in held_sets.items():
        for c in prev:
            m, r = pn.mark.at[t, c], pn.ref.at[t, c]
            lim = 0.10 if t >= E.LIMIT_10PCT_FROM else 0.07
            if m == m and r == r and r > 0 and abs(m / r - 1) > lim + 0.015:
                moves.append((str(t.date()), c, round(float(m / r - 1), 4)))
        prev = {c for c in h if c}
    res["beyond_limit_moves_while_held"] = moves
    # 4. capacity: portfolio size at which 90% of orders stay under 10% of that day's traded value
    vals = []
    for d0, picks in sels.items():
        i = pn.dates.searchsorted(d0, side="right")
        if i < len(pn.dates):
            vals += [pn.value.iat[i, pn.value.columns.get_loc(c)] for c in picks]
    vals = np.array([v for v in vals if v == v and v > 0])
    res["capacity_ntd_10pct_rule_p10"] = float(np.quantile(vals, 0.10) * 0.10 * 10)
    res["exec_day_value_median"] = float(np.median(vals))
    (OUT / "verify.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
