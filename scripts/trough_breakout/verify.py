"""獨立重算：條件層用 pandas rolling／shift 浮點重寫，組合用逐日、逐檔字典（股數）重寫，與主程式比對。

條件層：浮點與整數空間結果不同的格子，只允許出現在離門檻 1e-9 以內（浮點誤差）；否則報錯。
組合：設計 (i) 全期淨值、設計 (ii) 種子 1～5 淨值，最大相對誤差須 < 1e-9。
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import common as cm


def signals_check(m, L, rev):
    """回傳 dict：各層與主程式不一致的格子數（排除離門檻 1e-9 以內者）與邊界格子數。"""
    C = pd.DataFrame(m.C, index=m.dates)
    d = L.dec
    hi = C.rolling(cm.HI_WIN, min_periods=cm.HI_WIN).max().values[d]
    ma = C.rolling(cm.MA_WIN, min_periods=cm.MA_WIN).mean().values[d]
    lag = C.shift(cm.RET_LAG).values[d]
    c = m.C[d]
    ok = np.isfinite(hi) & np.isfinite(lag)
    with np.errstate(invalid="ignore", divide="ignore"):
        q1, q2, q3 = c / hi, c / lag, c / ma
    f1a = ok & (q1 >= 0.9)
    f1b = ok & (q2 >= 1.5)
    f1c = ok & (q3 > 1.0)
    res = {}
    for name, f, mine, q, thr in (("l1a", f1a, L.l1a, q1, 0.9), ("l1b", f1b, L.l1b, q2, 1.5), ("l1c", f1c, L.l1c, q3, 1.0)):
        diff = (f != mine) & L.univ
        near = np.abs(np.nan_to_num(q, nan=9.0) - thr) < 1e-9
        res[name] = dict(diff_far=int((diff & ~near).sum()), diff_near=int((diff & near).sum()), near=int((near & ok & L.univ).sum()))
    # L2：營收寬表 shift 浮點
    r = rev.copy()
    yo = r / r.shift(12) - 1
    yo = yo.where(r.shift(12) > 0)
    W, N = len(d), len(m.codes)
    f2 = np.zeros((W, N), dtype=bool)
    q2a = np.full((W, N), np.nan)
    q2b = np.full((W, N), np.nan)
    for w, di in enumerate(d):
        dt = m.dates[di]
        p = pd.Period(dt, freq="M") - (1 if dt.day >= 10 else 2)
        if p not in yo.index or (p - 3) not in yo.index:
            continue
        a, b = yo.loc[p].values, yo.loc[p - 3].values
        f2[w] = np.isfinite(a) & np.isfinite(b) & (a >= 0.15) & (a > b)
        q2a[w], q2b[w] = a, a - b
    diff = (f2 != L.l2)
    near = (np.abs(np.nan_to_num(q2a, nan=9.0) - 0.15) < 1e-9) | (np.abs(np.nan_to_num(q2b, nan=9.0)) < 1e-12)
    res["l2"] = dict(diff_far=int((diff & ~near).sum()), diff_near=int((diff & near).sum()), near=int(near.sum()))
    return res


def _px_open(m, t, j):
    o = m.O[t, j]
    return o if np.isfinite(o) else None


def nav_loop(m, dec, cand, design, exit_rule, below200, order_keys=None, start=cm.NAV_START,
             extra_exit=None, half=None, ind=None, ind_cap=2, order_i=None, freeze=None):
    """逐日逐檔：pos[j]＝股數（以還原價計）。order_keys：(W, N) 設計 (ii) 遞補順序（越小越先）。回傳淨值 ndarray。

    降回撤組合版（docs/TroughBreakout_Risk_Prereg.md）的四條手段另以字典逐檔寫一次，不呼叫 engine：
    extra_exit (W, N)＝R4 並行出場；half (W, N)＝R3 買進時係數 0.5；ind (N,)＝R2 產業（-1 缺值），
    在席＋新進同產業最多 ind_cap 檔、依順序跳過超限者；order_i (W, N)＝設計 (i) 遞補順序鍵（同值依欄位序）；
    freeze (W,)＝該月設計 (i) 不買不再平衡。全部為 None 時與原本相同。"""
    T = len(m.dates)
    t0 = int(np.searchsorted(m.dates.values, np.datetime64(pd.Timestamp(start))))
    cb, cs = m.cost_buy, m.cost_sell
    ex_day = {int(dd) + 1: w for w, dd in enumerate(dec) if int(dd) + 1 < T and int(dd) >= t0}
    cash = 1.0
    pos, ent, pend = {}, {}, set()
    kk = {}                                              # 買進時定的係數
    out = [1.0]

    def px(t, j):                               # 收盤（停牌日沿用前值）
        return m.C[t, j]

    for t in range(t0 + 1, T):
        r = m.rate[t - 1]
        if np.isfinite(r):
            cash *= 1 + r / 100 / 252
        w = ex_day.get(t)
        close_sells = []
        if w is not None or pend:
            busy = set(pos)                                  # 決策日當時持有者（含本次要賣的）不重複買
            sells = set(pend)
            if w is not None:
                for j in list(pos):
                    if exit_rule == "12m" and w - ent[j] >= cm.HOLD_MONTHS:
                        sells.add(j)
                    if exit_rule == "200d" and w > ent[j] and below200[w, j]:
                        sells.add(j)
                    if extra_exit is not None and extra_exit[w, j]:
                        sells.add(j)
            for j in sorted(sells):
                po = _px_open(m, t, j)
                if po is not None:
                    cash += pos.pop(j) * po * (1 - cs)
                    ent.pop(j)
                    kk.pop(j, None)
                    pend.discard(j)
                elif m.row[t, j]:
                    close_sells.append(j)
                else:
                    pend.add(j)
            if w is not None and not (freeze is not None and freeze[w]):
                stay = [j for j in pos if j not in sells]
                new = [j for j in np.where(cand[w])[0] if j not in busy]
                if ind is None:
                    if design == "ii":
                        new = sorted(new, key=lambda j: order_keys[w, j])[:max(cm.N_SEATS - len(stay), 0)]
                else:
                    if design == "ii":
                        new = sorted(new, key=lambda j: order_keys[w, j])
                    elif order_i is not None:
                        new = sorted(new, key=lambda j: (order_i[w, j], j))
                    cnt = {}
                    for j in stay:
                        if ind[j] >= 0:
                            cnt[ind[j]] = cnt.get(ind[j], 0) + 1
                    acc = []
                    for j in new:
                        if design == "ii" and len(acc) >= cm.N_SEATS - len(stay):
                            break
                        g = ind[j]
                        if g >= 0 and cnt.get(g, 0) >= ind_cap:
                            continue
                        acc.append(j)
                        if g >= 0:
                            cnt[g] = cnt.get(g, 0) + 1
                    new = acc
                kn = {j: (0.5 if (half is not None and half[w, j]) else 1.0) for j in new}
                if design == "i":
                    trad = [j for j in stay if _px_open(m, t, j) is not None]
                    nb = [j for j in new if _px_open(m, t, j) is not None]
                    tg = trad + nb
                    if tg and half is None:
                        I = cash + sum(pos[j] * m.O[t, j] for j in trad)
                        cur = {j: pos[j] * m.O[t, j] for j in trad}

                        def resid(x):
                            cost = sum(cb * max(x - cur.get(j, 0.0), 0) + cs * max(cur.get(j, 0.0) - x, 0) for j in tg)
                            return len(tg) * x + cost - I
                        lo, hi = 0.0, I / len(tg)
                        for _ in range(200):                      # 二分法求 x（與主程式的不動點法不同）
                            mid = (lo + hi) / 2
                            if resid(mid) > 0:
                                hi = mid
                            else:
                                lo = mid
                        x = (lo + hi) / 2
                        cost = sum(cb * max(x - cur.get(j, 0.0), 0) + cs * max(cur.get(j, 0.0) - x, 0) for j in tg)
                        for j in tg:
                            pos[j] = x / m.O[t, j]
                        for j in nb:
                            ent[j] = w
                            kk[j] = 1.0
                        cash = I - len(tg) * x - cost
                    elif tg:                                       # R3：每檔目標＝x × 係數，差額留現金
                        kf = {j: kk[j] for j in trad}
                        kf.update({j: kn[j] for j in nb})
                        I = cash + sum(pos[j] * m.O[t, j] for j in trad)
                        cur = {j: pos[j] * m.O[t, j] for j in trad}

                        def cost_k(x):
                            return sum(cb * max(kf[j] * x - cur.get(j, 0.0), 0) + cs * max(cur.get(j, 0.0) - kf[j] * x, 0)
                                       for j in tg)
                        lo, hi = 0.0, I / len(tg)
                        for _ in range(200):
                            mid = (lo + hi) / 2
                            if len(tg) * mid + cost_k(mid) - I > 0:
                                hi = mid
                            else:
                                lo = mid
                        x = (lo + hi) / 2
                        cost = cost_k(x)
                        for j in tg:
                            pos[j] = kf[j] * x / m.O[t, j]
                        for j in nb:
                            ent[j] = w
                            kk[j] = kn[j]
                        cash = I - sum(kf[j] * x for j in tg) - cost
                else:
                    navo = cash + sum(q * (m.O[t, j] if _px_open(m, t, j) is not None else m.C[t - 1, j]) for j, q in pos.items())
                    if new:
                        amt = min(navo / cm.N_SEATS, cash / len(new))
                        for j in new:
                            po = _px_open(m, t, j)
                            if po is None:
                                continue
                            a = amt * kn[j]
                            pos[j] = a / (po * (1 + cb))
                            ent[j] = w
                            kk[j] = kn[j]
                            cash -= a
        for j in close_sells:
            cash += pos.pop(j) * px(t, j) * (1 - cs)
            ent.pop(j)
            kk.pop(j, None)
            pend.discard(j)
        for j in list(pos):
            if m.last[j] == t and t < T - 1:
                cash += pos.pop(j) * px(t, j) * (1 - cs)
                ent.pop(j)
                kk.pop(j, None)
                pend.discard(j)
        out.append(cash + sum(q * px(t, j) for j, q in pos.items()))
    return np.array(out)


def engine_check(m, L, cand, results_i, results_ii, seeds=(1, 2, 3, 4, 5)):
    """results_i[exit]：主程式設計 (i) 淨值 (T,)；results_ii[exit]：主程式設計 (ii) 淨值 (P, T)，列 = 種子 1..P。"""
    out = {}
    for ex in ("12m", "200d"):
        a = nav_loop(m, L.dec, cand, "i", ex, L.below200)
        out[f"i_{ex}"] = float(np.max(np.abs(a / results_i[ex] - 1)))
        worst = 0.0
        for s in seeds:
            keys = np.random.default_rng([cm.SEED, s]).random((len(L.dec), len(m.codes)))
            b = nav_loop(m, L.dec, cand, "ii", ex, L.below200, order_keys=keys)
            worst = max(worst, float(np.max(np.abs(b / results_ii[ex][s - 1] - 1))))
        out[f"ii_{ex}"] = worst
    return out
