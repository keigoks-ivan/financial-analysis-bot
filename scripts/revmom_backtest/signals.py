"""Monthly selection (docs/RevMom_Backtest_Spec.md §2). Everything uses data known at the signal day's close."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_PICK = 10
VALUE_MIN = 10_000_000.0


def signal_days(dates: pd.DatetimeIndex, start, end, day: int | None = None) -> list:
    """Signal day of each month.

    day=None (the rule, spec §3 as amended 2026-10-01): the trading day AFTER the revenue deadline. Revenue for the
    prior month is due by the 10th; when the 10th is a market holiday the deadline moves to the next business day,
    taken here as the first trading day on/after the 10th. Signalling on the deadline day itself would use revenue
    that some companies file only that evening.
    day=N (sensitivity checks only): the first trading day on/after the N-th.
    """
    s = pd.Series(dates, index=dates)
    if day is not None:
        s = s[(s.index >= pd.Timestamp(start)) & (s.index <= pd.Timestamp(end)) & (s.index.day >= day)]
        return list(s.groupby([s.index.year, s.index.month]).min())
    out = []
    for (y, m), g in s.groupby([s.index.year, s.index.month]):
        after10 = g[g.index.day >= 10]
        if len(after10) < 2:
            continue                                    # deadline or the day after it not reached yet
        d = after10.index[1]
        if pd.Timestamp(start) <= d <= pd.Timestamp(end):
            out.append(d)
    return out


def precompute(pn) -> dict:
    fac = (pn.mark / pn.ref).where(pn.listed).fillna(1.0)
    tri = fac.cumprod().where(pn.listed)                          # total-return index per stock
    return {"tri": tri, "ma": {n: tri.rolling(n, min_periods=n).mean() for n in (20, 60, 120)},
            "ret5": tri / tri.shift(5) - 1, "ret60": tri / tri.shift(60) - 1,
            "val20": pn.value.where(pn.listed).rolling(20).mean()}


def revenue_ratio(rev: pd.DataFrame, d: pd.Timestamp) -> pd.Series:
    """Mean of the last 3 months / mean of the last 12 months, months up to the one before d's month."""
    last = pd.Period(d, "M") - 1
    r = rev.loc[:last]
    if len(r) < 12 or r.index[-1] != last:
        return pd.Series(dtype=float)
    r12 = r.iloc[-12:]
    a3, a12 = r12.iloc[-3:].mean(skipna=False), r12.mean(skipna=False)
    out = a3 / a12
    out[a12 == 0] = np.nan
    return out


def revenue_growth3(rev: pd.DataFrame, d: pd.Timestamp) -> pd.Series:
    last = pd.Period(d, "M") - 1
    cur = rev.reindex([last - 2, last - 1, last]).sum(min_count=3)
    prev = rev.reindex([last - 14, last - 13, last - 12]).sum(min_count=3)
    return (cur / prev - 1).where((cur > 0) & (prev > 0))


def select(pn, pre: dict, d: pd.Timestamp, variant: str = "V1a", n_pick: int = N_PICK,
           value_min: float = VALUE_MIN, tech: bool = True, innovation: bool = False) -> tuple:
    """innovation=False drops stocks on the Taiwan Innovation Board that day (spec §3, 2026-10-01 amendment)."""
    codes = pd.Index([c for c in pn.close.columns if len(c) == 4 and c.isdigit()])
    listed = pn.listed.loc[d].reindex(codes).fillna(False).astype(bool)
    if not innovation:
        listed &= ~pn.innov.loc[d].reindex(codes).fillna(False).astype(bool)
    base = listed & (pre["val20"].loc[d].reindex(codes) >= value_min).fillna(False)
    if variant in ("V1a", "V1b"):
        rr = revenue_ratio(pn.rev, d).reindex(codes)
        cond = base & (rr > 1).fillna(False)
        if tech:
            tri = pre["tri"].loc[d].reindex(codes)
            cond &= (pre["ret5"].loc[d].reindex(codes) > 0).fillna(False)
            for n in (20, 60, 120):
                cond &= (tri > pre["ma"][n].loc[d].reindex(codes)).fillna(False)
        score = rr if variant == "V1a" else pre["ret60"].loc[d].reindex(codes)
    else:
        score = revenue_growth3(pn.rev, d).reindex(codes)
        cond = base & score.notna()
    cand = score[cond].dropna().sort_index().sort_values(ascending=False, kind="mergesort")
    picks = list(cand.index[:n_pick])
    return picks, {"date": str(d.date()), "n_universe": int(base.sum()), "n_pass": int(cond.sum()), "picks": picks}


def selections(pn, pre: dict, start, end, variant: str = "V1a", day: int | None = None, **kw) -> tuple:
    sels, diags = {}, []
    for d in signal_days(pn.dates, start, end, day):
        p, g = select(pn, pre, d, variant, **kw)
        sels[d] = p
        diags.append(g)
    return sels, diags
