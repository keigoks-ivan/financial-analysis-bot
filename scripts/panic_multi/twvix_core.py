"""自動產生，勿手改：src/twvix_proxy/build.py 的逐字副本（third_wednesday、term_variance、vix_one_day）。

產生方式：v7-backtest `python3 -m src.panic_call.ci_copy`。
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

ROLL_TD = 2  # 近月到期前 2 個交易日（含到期日）起，近月改用次近月


def third_wednesday(yyyymm: str) -> pd.Timestamp:
    y, m = int(yyyymm[:4]), int(yyyymm[4:])
    d = pd.Timestamp(y, m, 1)
    first_wed = d + pd.Timedelta(days=(2 - d.weekday()) % 7)
    return first_wed + pd.Timedelta(days=14)


def term_variance(c: pd.Series, p: pd.Series):
    """c、p：index＝履約價的買權與賣權價格（Series，可含 NaN）。
    回傳 (sigma2_annualized_without_T, F, K0, n_used) 的元組；不成立回 None。
    sigma2 這裡先回傳 (sum_term, F, K0, n)；T 由呼叫端處理。"""
    both = pd.concat([c.rename("c"), p.rename("p")], axis=1)
    bb = both.dropna()
    bb = bb[(bb.c > 0) & (bb.p > 0)]
    if bb.empty:
        return None
    diff = (bb.c - bb.p).abs()
    mn = diff.min()
    ties = bb.index[diff.values == mn]
    # CBOE：|C−P| 最小的履約價 F＝K+e^{RT}(C−P)，R＝0；同分取平均
    F = float(np.mean([k + (bb.c[k] - bb.p[k]) for k in ties]))
    ks = bb.index[bb.index <= F]
    if len(ks) == 0:
        return None
    K0 = float(ks.max())
    q0 = (bb.c[K0] + bb.p[K0]) / 2.0
    # 價外序列：連續兩個零價就停
    puts = []
    z = 0
    for k in sorted([k for k in p.index if k < K0], reverse=True):
        v = p[k]
        if not (v > 0):
            z += 1
            if z >= 2:
                break
            continue
        z = 0
        puts.append((float(k), float(v)))
    calls = []
    z = 0
    for k in sorted([k for k in c.index if k > K0]):
        v = c[k]
        if not (v > 0):
            z += 1
            if z >= 2:
                break
            continue
        z = 0
        calls.append((float(k), float(v)))
    if not puts or not calls:
        return None
    seq = sorted(puts + [(K0, q0)] + calls)
    ks_ = [s[0] for s in seq]
    tot = 0.0
    for i, (k, q) in enumerate(seq):
        if i == 0:
            dk = ks_[1] - ks_[0]
        elif i == len(seq) - 1:
            dk = ks_[-1] - ks_[-2]
        else:
            dk = (ks_[i + 1] - ks_[i - 1]) / 2.0
        tot += dk / (k * k) * q
    return tot, F, K0, len(seq)


def vix_one_day(g: pd.DataFrame, date: pd.Timestamp, near: str, nxt: str, exp_map: dict, col: str):
    """g：當天資料；col＝價格欄位（'px_settle' 或 'px_mid'）。回傳 dict 或 None。"""
    res = {}
    for tag, e in (("near", near), ("next", nxt)):
        ge = g[g.expiry == e]
        c = ge[ge.cp == "C"].set_index("strike")[col]
        p = ge[ge.cp == "P"].set_index("strike")[col]
        c = c[~c.index.duplicated()]
        p = p[~p.index.duplicated()]
        r = term_variance(c, p)
        if r is None:
            return None
        tot, F, K0, n = r
        days = (exp_map[e] - date).days
        T = days * 86400.0 / (86400.0 * (366 if date.is_leap_year else 365))
        var = 2.0 / T * tot - (1.0 / T) * (F / K0 - 1.0) ** 2
        res[tag] = dict(var=var, T=T, days=days, F=F, K0=K0, n=n)
    a, b = res["near"], res["next"]
    n1, n2, n30 = a["days"] * 86400.0, b["days"] * 86400.0, 30 * 86400.0
    ny = (366 if date.is_leap_year else 365) * 86400.0
    w1 = (n2 - n30) / (n2 - n1)
    w2 = (n30 - n1) / (n2 - n1)
    if w1 > 1.0:       # 30 天落在近月之前：期交所規定直接用近月
        sig2 = a["var"]
    elif w2 > 1.0:     # 30 天落在次近月之後：直接用次近月
        sig2 = b["var"]
    else:
        v = a["T"] * a["var"] * w1 + b["T"] * b["var"] * w2
        sig2 = v * ny / n30
    if not (sig2 > 0):
        return None
    return dict(vix=100.0 * math.sqrt(sig2), near=a, next=b)
