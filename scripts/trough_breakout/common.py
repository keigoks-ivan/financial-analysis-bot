"""路徑、常數、整數空間比較、績效指標。規格：docs/TroughBreakout_Prereg.md（2026-11-03，commit ccfc98d）。

Python 3.9 相容（系統 python3 跑回測）。
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

# 資料根目錄：預設是本 repo；網站 repo 的副本在本機跑時，用環境變數 TB_ROOT 指到 v7-backtest 或解開的 Release 資料。
ROOT = Path(os.environ["TB_ROOT"]) if os.environ.get("TB_ROOT") else Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "trough_breakout_2010-2026"

# ---------------------------------------------------------------- 時序（登記第三節）
NAV_START = pd.Timestamp("2009-12-31")       # 淨值起點收盤＝1.0
PRE_END = pd.Timestamp("2017-12-29")         # 前段 2010-01～2017-12 的最後一個交易日（台股）
CRASH = [("2011-07", "2011-07-01", "2011-10-31"), ("2015-06", "2015-06-01", "2015-08-31"),
         ("2020-02", "2020-02-01", "2020-03-31"), ("2022-01", "2022-01-01", "2022-10-31")]

# ---------------------------------------------------------------- 成本（登記第三節）
TW_COST_BUY = 0.000855                       # 手續費 0.1425% 六折
TW_COST_SELL = 0.000855 + 0.003              # 手續費＋證交稅 30 bps
US_COST = 0.0007                             # 美股單邊 7 bps（第十節）

# ---------------------------------------------------------------- 母體與條件（第三、四節）
LIQ_WIN = 20
LIQ_MIN_TWD = 10_000_000                     # 近 20 日平均成交金額門檻（元）
HI_WIN, RET_LAG, MA_WIN = 250, 126, 200
EPS_LAG_DAYS = 91
HOLD_MONTHS = 12
N_SEATS = 5
SEED = 20261103
N_SEEDS = 1000
N_RANDOM = 1000

# 整數空間：價格比值以 1e-8 為一個單位四捨五入成整數再比（避免浮點把恰好等於門檻的情形算錯）。
UNIT = 100_000_000
U_HI = 90_000_000            # 收盤 ≥ 250 日最高 × 90%
U_RET = 150_000_000          # 收盤 ÷ 126 日前 ≥ 1.5（+50%）
U_MA = 100_000_000           # 收盤 > 200 日均線（嚴格）
U_EPS = 110_000_000          # EPS 比值 ≥ 1.10
U_DOUBLE = 200_000_000       # 12 個月內最高收盤 ≥ 買進價 × 2


def ratio_units(a, b):
    """a ÷ b 轉成 1e-8 單位的整數（int64）；任一為 NaN 或 b ≤ 0 時回傳 -1（視為不成立）。"""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b) & (b > 0)
    out = np.full(np.broadcast(a, b).shape, -1, dtype=np.int64)
    with np.errstate(divide="ignore", invalid="ignore"):
        q = np.rint(np.where(ok, a / np.where(ok, b, 1.0), 0.0) * UNIT)
    out[ok] = q[ok].astype(np.int64)
    return out


def latest_revenue_month(decision_date) -> pd.Period:
    """月營收可得日：m 月營收視為 m+1 月 10 日公布，決策日 ≥ 公布日才能用。回傳決策日可用的最新月份。"""
    d = pd.Timestamp(decision_date)
    cur = pd.Period(d, freq="M")
    return cur - 1 if d.day >= 10 else cur - 2


# ---------------------------------------------------------------- 指標
def years_between(d0, d1) -> float:
    return (pd.Timestamp(d1) - pd.Timestamp(d0)).days / 365.25


def mdd_of(nav: np.ndarray) -> np.ndarray:
    """nav：(..., T)。回傳最後一軸的最大回撤（負數）。"""
    peak = np.maximum.accumulate(nav, axis=-1)
    return (nav / peak - 1.0).min(axis=-1)


def cagr_of(total, years):
    return np.power(total, 1.0 / years) - 1.0


def path_metrics(dates: pd.DatetimeIndex, nav: np.ndarray) -> dict:
    """nav：(P, T) 或 (T,)，dates 長度 T，第一天為起點。回傳各指標陣列（P,）或純量。"""
    nav = np.atleast_2d(nav)
    yrs = years_between(dates[0], dates[-1])
    total = nav[:, -1] / nav[:, 0]
    cagr = cagr_of(total, yrs)
    mdd = mdd_of(nav)
    calmar = np.where(mdd < 0, cagr / np.abs(np.where(mdd < 0, mdd, -1.0)), np.nan)
    ipre = int(np.searchsorted(dates.values, np.datetime64(PRE_END), side="right")) - 1
    y1 = years_between(dates[0], dates[ipre])
    y2 = years_between(dates[ipre], dates[-1])
    pre = cagr_of(nav[:, ipre] / nav[:, 0], y1)
    post = cagr_of(nav[:, -1] / nav[:, ipre], y2)
    return dict(cagr=cagr, mdd=mdd, calmar=calmar, pre_cagr=pre, post_cagr=post, total=total - 1.0, years=yrs)


def window_mdd(dates: pd.DatetimeIndex, nav: np.ndarray, a, b) -> np.ndarray:
    """區間內（含前一日收盤作為起點）的最大回撤。"""
    nav = np.atleast_2d(nav)
    i0 = max(int(np.searchsorted(dates.values, np.datetime64(pd.Timestamp(a)), side="left")) - 1, 0)
    i1 = int(np.searchsorted(dates.values, np.datetime64(pd.Timestamp(b)), side="right"))
    return mdd_of(nav[:, i0:i1])


def yearly_returns(dates: pd.DatetimeIndex, nav: np.ndarray) -> dict:
    """每個日曆年：該年最後一個交易日收盤 ÷ 前一年最後一個交易日收盤（第一年從起點算）。"""
    nav = np.atleast_2d(nav)
    s = pd.Series(np.arange(len(dates)), index=dates)
    ends = s.groupby(dates.year).max()
    out, prev = {}, 0
    for y, i in ends.items():
        if i == 0:
            continue
        out[int(y)] = nav[:, i] / nav[:, prev] - 1.0
        prev = i
    return out
