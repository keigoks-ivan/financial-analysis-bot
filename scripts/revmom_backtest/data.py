"""Load the exported official panel into wide (date x code) frames."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "revmom"


@dataclass
class Panel:
    dates: pd.DatetimeIndex
    open: pd.DataFrame
    high: pd.DataFrame
    low: pd.DataFrame
    close: pd.DataFrame
    value: pd.DataFrame
    mark: pd.DataFrame      # close, or the reference price on a no-trade day
    ref: pd.DataFrame       # reference price after dividends / splits / capital changes
    listed: pd.DataFrame
    rev: pd.DataFrame       # monthly revenue, PeriodIndex x code
    taiex_tr: pd.Series     # TWSE total-return index (2009 on)
    innov: pd.DataFrame     # True where the stock traded on the Taiwan Innovation Board that day (name ends "-創")


def load(start: str = "2007-01-01") -> Panel:
    p = pd.read_parquet(DATA / "prices.parquet")
    p = p[p.date >= pd.Timestamp(start)]
    wide = {c: p.pivot(index="date", columns="code", values=c) for c in
            ("open", "high", "low", "close", "value", "mark", "ref")}
    dates = wide["mark"].index
    codes = wide["mark"].columns
    wide = {k: v.reindex(index=dates, columns=codes) for k, v in wide.items()}
    listed = p.assign(v=1.0).pivot(index="date", columns="code", values="v").reindex(index=dates, columns=codes).notna()
    rev = pd.read_parquet(DATA / "revenue.parquet").pivot(index="month", columns="code", values="revenue")
    rev.index = pd.PeriodIndex(rev.index, freq="M")
    tr = pd.read_parquet(DATA / "index_tr.parquet").set_index("date").taiex_tr
    ib = pd.read_parquet(DATA / "innovation_board.parquet")
    innov = ib.assign(v=1.0).pivot(index="date", columns="code", values="v").reindex(
        index=dates, columns=codes).notna()
    return Panel(dates, wide["open"], wide["high"], wide["low"], wide["close"], wide["value"], wide["mark"],
                 wide["ref"], listed, rev.sort_index(), tr, innov)
