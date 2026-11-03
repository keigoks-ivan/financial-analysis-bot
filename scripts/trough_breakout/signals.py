"""決策日條件層（登記第四節）與母體（第三節）。全部在決策日收盤判，離散門檻在整數空間比。

輸出矩陣形狀 (W, N)：W＝決策日數，N＝代號數。
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import common as cm


def decision_days(dates: pd.DatetimeIndex, start=cm.NAV_START) -> np.ndarray:
    """每月最後一個交易日（且其後還有交易日可成交）的位置，從 start 所在月起。"""
    s = pd.Series(np.arange(len(dates)), index=dates)
    last = s.groupby([dates.year, dates.month]).max().values
    last = last[(dates[last] >= pd.Timestamp(start)) & (last < len(dates) - 1)]
    return last.astype(int)


@dataclass
class Layers:
    dec: np.ndarray          # (W,) 決策日位置
    univ: np.ndarray         # (W, N) 母體（代號規則＋當日有列＋流動性）
    hist: np.ndarray         # (W, N) 有 250 個交易日歷史
    l1a: np.ndarray          # 收盤 ≥ 250 日最高 × 90%
    l1b: np.ndarray          # 6 個月 ≥ +50%
    l1c: np.ndarray          # 收盤 > 200 日均
    below200: np.ndarray     # 收盤 < 200 日均（出場用；有均線者才可能 True）
    l2: np.ndarray
    l3: np.ndarray
    ath: np.ndarray          # 收盤 ≥ 起算以來還原最高收盤 × 90%
    u_hi: np.ndarray         # 診斷用整數值
    u_ret: np.ndarray
    u_ma: np.ndarray
    u_ath: np.ndarray

    @property
    def L1(self):
        return self.univ & self.hist & self.l1a & self.l1b & self.l1c

    @property
    def main(self):
        return self.L1 & self.l2

    @property
    def rev(self):
        return self.main & self.l3

    @property
    def newhigh(self):
        return self.main & self.ath


def price_layers(m, dec: np.ndarray):
    """L1 三條件、200 日均線下、起算最高 90%。回傳 dict of (W, N)。"""
    C = m.C
    W, N = len(dec), C.shape[1]
    out = {k: np.zeros((W, N), dtype=bool) for k in ("hist", "l1a", "l1b", "l1c", "below200", "ath")}
    for k in ("u_hi", "u_ret", "u_ma", "u_ath"):
        out[k] = np.full((W, N), -1, dtype=np.int64)
    runmax = np.fmax.accumulate(np.where(np.isnan(C), -np.inf, C), axis=0)
    for w, d in enumerate(dec):
        c = C[d]
        hist = (d - m.first >= cm.HI_WIN - 1) & np.isfinite(c)
        lo = d - cm.HI_WIN + 1
        if lo < 0:
            continue
        win = C[lo:d + 1]
        with np.errstate(invalid="ignore", all="ignore"):
            hi = np.nanmax(np.where(np.isnan(win), -np.inf, win), axis=0)
            ma = win[-cm.MA_WIN:].mean(axis=0)            # 窗口內任一 NaN → NaN（hist 已保證完整）
        c126 = C[d - cm.RET_LAG] if d - cm.RET_LAG >= 0 else np.full(N, np.nan)
        u_hi = cm.ratio_units(c, np.where(hist, hi, np.nan))
        u_ret = cm.ratio_units(c, np.where(hist, c126, np.nan))
        u_ma_all = cm.ratio_units(c, ma)
        u_ma = np.where(hist, u_ma_all, -1)
        u_ath = cm.ratio_units(c, np.where(hist, runmax[d], np.nan))
        out["hist"][w] = hist
        out["l1a"][w] = hist & (u_hi >= cm.U_HI)
        out["l1b"][w] = hist & (u_ret >= cm.U_RET)
        out["l1c"][w] = hist & (u_ma > cm.U_MA)
        out["below200"][w] = (u_ma_all >= 0) & (u_ma_all < cm.U_MA)
        out["ath"][w] = hist & (u_ath >= cm.U_HI)                       # 90%
        out["u_hi"][w], out["u_ret"][w], out["u_ma"][w], out["u_ath"][w] = u_hi, u_ret, u_ma, u_ath
    return out


def revenue_layer(rev: pd.DataFrame, dec_dates) -> tuple:
    """L2：最新可得月營收年增 ≥ 15%，且高於三個月前那個月的年增。整數精確比較。
    rev：連續月 PeriodIndex × 代號（千元，缺 NaN）。回傳 (l2 (W,N) bool, yoy_now (W,N), yoy_3m (W,N)) 後兩者為浮點診斷值。"""
    vals = rev.values
    if np.nanmax(np.abs(vals)) >= 3e9:
        raise ValueError("營收數值過大，int64 乘積可能溢位")
    idx = {p: i for i, p in enumerate(rev.index)}
    W, N = len(dec_dates), vals.shape[1]
    l2 = np.zeros((W, N), dtype=bool)
    y0 = np.full((W, N), np.nan)
    y3 = np.full((W, N), np.nan)
    for w, d in enumerate(dec_dates):
        m0 = cm.latest_revenue_month(d)
        need = [m0, m0 - 12, m0 - 3, m0 - 15]
        if any(p not in idx for p in need):
            continue
        a, b, c, e = (vals[idx[p]] for p in need)          # a=最新, b=去年同月, c=三個月前那個月, e=其去年同月
        ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(c) & np.isfinite(e) & (b > 0) & (e > 0)
        ai = np.where(ok, a, 0).astype(np.int64)
        bi = np.where(ok, b, 1).astype(np.int64)
        ci = np.where(ok, c, 0).astype(np.int64)
        ei = np.where(ok, e, 1).astype(np.int64)
        grow = 100 * ai >= 115 * bi                        # a/b − 1 ≥ 15%
        accel = ai * ei > ci * bi                           # a/b > c/e（b, e > 0）
        l2[w] = ok & grow & accel
        with np.errstate(invalid="ignore", divide="ignore"):
            y0[w] = np.where(np.isfinite(b) & (b > 0), a / b - 1, np.nan)
            y3[w] = np.where(np.isfinite(e) & (e > 0), c / e - 1, np.nan)
    return l2, y0, y3


def eps_layer(eps_ff: pd.DataFrame, codes, dec_dates) -> tuple:
    """L3：NTM EPS 決策日（含）最近一筆 ÷ 91 天前（含）最近一筆 − 1 ≥ 10%；91 天前值 ≤ 0 或缺值不成立。
    回傳 (l3 (W,N), ratio (W,N) 浮點診斷, has_now (W,N) 有預估)。"""
    W, N = len(dec_dates), len(codes)
    l3 = np.zeros((W, N), dtype=bool)
    ratio = np.full((W, N), np.nan)
    have = np.zeros((W, N), dtype=bool)
    col = {c: j for j, c in enumerate(codes)}
    js = np.array([col[c] for c in eps_ff.columns], dtype=int)
    idx = eps_ff.index.values
    E = eps_ff.values
    for w, d in enumerate(dec_dates):
        i1 = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(d)), side="right")) - 1
        i0 = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(d) - pd.Timedelta(days=cm.EPS_LAG_DAYS)), side="right")) - 1
        if i1 < 0:
            continue
        now = E[i1]
        then = E[i0] if i0 >= 0 else np.full(len(js), np.nan)
        u = cm.ratio_units(now, then)                      # then ≤ 0 或 NaN → -1
        l3[w, js] = u >= cm.U_EPS
        have[w, js] = np.isfinite(now)
        with np.errstate(invalid="ignore", divide="ignore"):
            ratio[w, js] = np.where(np.isfinite(then) & (then > 0), now / then - 1, np.nan)
    return l3, ratio, have


def build_layers(m, rev_l2, eps_l3, dec=None) -> Layers:
    """rev_l2：(l2,) 已對齊 m.codes；eps_l3：(l3,) 已對齊。"""
    if dec is None:
        dec = decision_days(m.dates)
    pl = price_layers(m, dec)
    univ = m.row[dec] & m.liq[dec] & np.isfinite(m.C[dec])
    return Layers(dec, univ, pl["hist"], pl["l1a"], pl["l1b"], pl["l1c"], pl["below200"], rev_l2, eps_l3,
                  pl["ath"], pl["u_hi"], pl["u_ret"], pl["u_ma"], pl["u_ath"])
