"""自動產生，勿手改：src/tw_panic_limitdown/run.py 的逐字副本（tick_cents、limit_down_cents、breadth）。

產生方式：v7-backtest `python3 -m src.panic_call.ci_copy`。
"""
from __future__ import annotations

import numpy as np
import pandas as pd

LIMIT_CHANGE = pd.Timestamp("2015-06-01")


def tick_cents(raw_cents: np.ndarray) -> np.ndarray:
    """升降單位（分），依價位決定。raw_cents 可為小數。"""
    t = np.full(raw_cents.shape, 500, dtype=np.int64)
    t[raw_cents < 100_000] = 100
    t[raw_cents < 50_000] = 50
    t[raw_cents < 10_000] = 10
    t[raw_cents < 5_000] = 5
    t[raw_cents < 1_000] = 1
    return t


def limit_down_cents(ref: pd.DataFrame, dates) -> np.ndarray:
    """跌停價（整數分）：參考價 ×（1−L），向上取到升降單位。L＝7（2015-06-01 前）或 10。整數運算。"""
    r = np.rint(ref.to_numpy() * 100)
    ok = np.isfinite(r) & (r > 0)
    rc = np.where(ok, r, 0).astype(np.int64)
    lim = np.where(np.asarray(dates) < np.datetime64(LIMIT_CHANGE), 7, 10).astype(np.int64)[:, None]
    num = rc * (100 - lim)                      # 單位：0.01 分
    tick = tick_cents(num / 100.0)
    out = -((-num) // (100 * tick)) * tick      # 向上取整到 tick
    return np.where(ok, out, -1)


def breadth(dates, codes, w, listed):
    first = listed.idxmax()                     # 每檔第一個有參考價的日子
    pos = pd.Series(np.arange(len(dates)), index=dates)
    first_pos = pos.reindex(first.values).to_numpy()
    new_listing = first.values > dates[0]
    rows = np.arange(len(dates))[:, None]
    in_first5 = new_listing[None, :] & (rows >= first_pos[None, :]) & (rows < first_pos[None, :] + 5)
    uni = listed.to_numpy() & ~in_first5
    ld = limit_down_cents(w["ref"], dates)
    c = np.rint(w["close"].to_numpy() * 100)
    traded = np.isfinite(c) & (np.nan_to_num(w["value"].to_numpy()) > 0)
    locked = uni & traded & (np.where(np.isfinite(c), c, 1e12) <= ld) & (ld > 0)
    notrade = uni & ~traded
    df = pd.DataFrame({"n_universe": uni.sum(1), "n_locked_down": locked.sum(1), "n_no_trade": notrade.sum(1)},
                      index=dates)
    df["ratio"] = df.n_locked_down / df.n_universe
    return df, pd.DataFrame(locked, index=dates, columns=codes), uni
