"""五條訊號：分位數（整數空間）、同一波只算一次、止穩日。"""
from __future__ import annotations

from bisect import bisect_left, bisect_right, insort

import numpy as np
import pandas as pd

BURN = 1260
PS = (500, 250, 100)          # 基點：5%、2.5%、1%
SCALE = 1_000_000
SIGNALS = ("vol", "rsi", "accel1", "accel2", "multi")


def to_int(x):
    return int(round(float(x) * SCALE))


def rsi14(close: pd.Series) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0.0)
    dn = (-d).clip(lower=0.0)
    au = up.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    ad = dn.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    rs = au / ad.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    out[(ad == 0) & au.notna()] = 100.0
    return out


def z3_and_flags(df: pd.DataFrame):
    c = df["close"]
    r = c / c.shift(1) - 1.0
    ret3 = c / c.shift(3) - 1.0
    sd20 = r.shift(3).rolling(20).std(ddof=0)
    z3 = ret3 / (sd20 * np.sqrt(3.0))
    z3 = z3.where(sd20 > 0)
    rb = (r * 1e4).round()
    a1 = (rb.shift(2) < 0) & (rb.shift(1) < rb.shift(2)) & (rb < rb.shift(1))
    v = df["volume"] if "volume" in df else pd.Series(np.nan, index=df.index)
    va = (v.shift(1) > v.shift(2)) & (v > v.shift(1)) & v.notna() & v.shift(1).notna() & v.shift(2).notna()
    a1 = a1.fillna(False)
    a2 = (a1 & va).fillna(False)
    return z3, a1.to_numpy(bool), a2.to_numpy(bool)


class Track:
    """一個指標的逐日極端判斷。high=True：越大越極端。"""

    def __init__(self, values: np.ndarray, high: bool):
        n = len(values)
        self.val = [None] * n
        self.med = [None] * n
        self.lit = {p: np.zeros(n, bool) for p in PS}
        lst = []
        for i in range(n):
            x = values[i]
            if x != x:
                continue
            xi = to_int(x)
            self.val[i] = xi
            k = len(lst)
            if k >= BURN:
                c = (k - bisect_left(lst, xi)) if high else bisect_right(lst, xi)
                for p in PS:
                    if c * 10_000 <= p * k:
                        self.lit[p][i] = True
                self.med[i] = lst[(k - 1) // 2]
            insort(lst, xi)
        self.first_valid = next((i for i in range(n) if self.med[i] is not None), None)


def build(df: pd.DataFrame) -> dict:
    n = len(df)
    nan = np.full(n, np.nan)
    T = {}
    T["vol"] = Track(df["vol"].to_numpy(float) if "vol" in df else nan, True)
    T["rsi"] = Track(rsi14(df["close"]).to_numpy(float), False)
    z3, a1, a2 = z3_and_flags(df)
    T["z3"] = Track(z3.to_numpy(float), False)
    T["ratio"] = Track(df["ratio"].to_numpy(float) if "ratio" in df else nan, True)
    T["a1"], T["a2"] = a1, a2
    # 原始三日跌幅（不除波動；登記檔「另列當描述」）：只在 raw3 訊號用到
    T["ret3"] = Track((df["close"] / df["close"].shift(3) - 1.0).to_numpy(float), False)
    return T


def lit_series(T: dict, sig: str, p: int) -> np.ndarray:
    if sig == "vol":
        return T["vol"].lit[p]
    if sig == "rsi":
        return T["rsi"].lit[p]
    if sig == "accel1":
        return T["a1"] & T["z3"].lit[p]
    if sig == "accel2":
        return T["a2"] & T["z3"].lit[p]
    if sig == "raw3":
        return T["a1"] & T["ret3"].lit[p]
    b = T["a1"] & T["z3"].lit[p]
    return (T["vol"].lit[p].astype(int) + b.astype(int) + T["ratio"].lit[p].astype(int)) >= 2


def rearm_ok(T: dict, sig: str, i: int) -> bool:
    if sig in ("vol", "multi"):
        t = T["vol"]
        return t.val[i] is not None and t.med[i] is not None and t.val[i] <= t.med[i]
    t = T["rsi"] if sig == "rsi" else (T["ret3"] if sig == "raw3" else T["z3"])
    return t.val[i] is not None and t.med[i] is not None and t.val[i] >= t.med[i]


def events(T: dict, sig: str, p: int, n: int) -> list:
    lit = lit_series(T, sig, p)
    armed, out = True, []
    for i in range(n):
        if armed:
            if lit[i]:
                out.append(i)
                armed = False
        elif rearm_ok(T, sig, i):
            armed = True
    return out


def stab_day(close: np.ndarray, vol: np.ndarray, s: int, last: int):
    """訊號日 s 之後 1~20 個交易日內第一個止穩日；沒有回 None。"""
    if vol[s] != vol[s]:
        return None
    peak = to_int(vol[s])
    for j in range(s + 1, min(s + 20, last) + 1):
        if j >= 3 and vol[j] == vol[j]:
            vj = to_int(vol[j])
            cj = to_int(close[j])
            if cj > max(to_int(close[j - 3]), to_int(close[j - 2]), to_int(close[j - 1])) and vj < peak:
                return j
        if vol[j] == vol[j]:
            peak = max(peak, to_int(vol[j]))
    return None
