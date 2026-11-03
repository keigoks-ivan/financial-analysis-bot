"""逐日組合模擬，向量化跑多條路徑（設計 (ii) 的 1,000 個種子、隨機對照的 1,000 次）。登記第五、六節。

時序：決策日 d 收盤判；次一交易日 t 開盤成交。開盤缺（沒有成交）時買進當日不買、賣出改用當日收盤；
當日根本沒有報價列（停牌）時賣單保留，到下一個有列的日子再賣（有開盤用開盤，否則收盤）。
下市（最後一列早於面板終點）在最後一列收盤以最後可得價賣出。

設計 (i)：每個成交日，留下的持股與新進者重設等權（成交日開盤無法成交的留任者不動，其餘等分可投入資金）。
設計 (ii)：最多 5 席，空位依路徑自己的順序從當月名單遞補；新席金額＝min(開盤淨值 ÷ 5, 現金 ÷ 本次遞補檔數)，
持股不做再平衡（與 src/seat_exit_backtest 等席位引擎同口徑）。

出場：'12m' 買進後第 12 個決策日賣；'200d' 買進後下一個決策日起，決策日收盤 < 200 日均線就賣。
持有期間（含已決定賣出但尚未成交）同一檔不重複買。
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import common as cm


def simulate(m, dec, cols, sel_lists, design, exit_rule, below200, n_paths, start=cm.NAV_START, record=True,
             rebuy_on_exit=False, extra_exit=None, half=None, ind=None, ind_cap=2, freeze=None):
    """
    m：Mkt；dec：(W,) 決策日位置；cols：(K,) 這次模擬用到的代號欄位（m 的欄位位置）。
    sel_lists：長度 W 的串列，第 w 個為 int 陣列 (P 或 1, n_w)，值為 cols 內的位置（0..K-1），依遞補優先順序排列，-1 為空。
    below200：(W, N) bool。回傳 dict。
    rebuy_on_exit：True 時，出場決策日當天已在開盤賣出的股票可以在同一決策日再買（另一種讀法，只供疑點節敏感度）。

    以下參數供降回撤組合版（docs/TroughBreakout_Risk_Prereg.md）用；全部為 None 時與原本逐位相同。
    extra_exit：(W, N) bool，決策日收盤為 True 的持股與原出場並行賣出（R4 離高點 20%）。
    half：(W, N) bool，買進當月為 True 者倉位係數 0.5（R3），只在買進時定、持有期間不變。
          設計 (i)：目標金額＝基準權重（可投入資金扣成本後 ÷ 成交檔數）× 係數，差額留現金；設計 (ii)：該席金額 × 0.5。
    ind：(N,) int 產業編號（-1＝缺值，不受上限）。每月「在席（本月不賣者）＋本月新進」同產業最多 ind_cap 檔（R2），
         依 sel_lists 的順序遞補、超限者跳過（設計 (ii) 繼續往下抽）。選中但次日沒有開盤者照樣占名額（同空席規則）。
    freeze：(W,) bool，該月設計 (i) 不買也不再平衡、賣出的錢留現金（只供 R1 另一讀法的敏感度）。
    """
    assert design in ("i", "ii") and exit_rule in ("12m", "200d")
    T = len(m.dates)
    t0 = int(np.searchsorted(m.dates.values, np.datetime64(pd.Timestamp(start)), side="left"))
    cols = np.asarray(cols, dtype=int)
    K, P = len(cols), int(n_paths)
    C = m.C[:, cols]
    O = m.O[:, cols]
    ROW = m.row[:, cols]
    last = m.last[cols]
    B200 = below200[:, cols]
    X4 = None if extra_exit is None else np.asarray(extra_exit)[:, cols]
    HF = None if half is None else np.asarray(half)[:, cols]
    IND = None if ind is None else np.asarray(ind, dtype=np.int64)[cols]
    OH = None
    if IND is not None and (IND >= 0).any():
        OH = (IND[:, None] == np.arange(int(IND.max()) + 1)[None, :]).astype(float)     # (K, G) 產業 one-hot
    cb, cs = m.cost_buy, m.cost_sell
    exec_of = {int(d) + 1: w for w, d in enumerate(dec) if int(d) + 1 < T and int(d) >= t0}
    delist_at = {}
    for j in np.where(last < T - 1)[0]:
        delist_at.setdefault(int(last[j]), []).append(j)
    delist_at = {k: np.array(v, dtype=int) for k, v in delist_at.items()}

    val = np.zeros((P, K))
    held = np.zeros((P, K), dtype=bool)
    pend = np.zeros((P, K), dtype=bool)
    entry_w = np.full((P, K), -10 ** 6, dtype=np.int64)
    entry_t = np.zeros((P, K), dtype=np.int64)
    entry_px = np.zeros((P, K))
    cash = np.ones(P)
    n_run = T - t0
    nav = np.empty((P, n_run))
    nav[:, 0] = 1.0
    nheld_sum = np.zeros(P)
    expo_sum = np.zeros(P)
    buy_frac = np.zeros(P)
    sell_frac = np.zeros(P)
    nheld_daily = np.zeros((P, n_run), dtype=np.int32) if P == 1 else None
    tr = {k: [] for k in ("p", "j", "t_in", "t_out", "px_in", "px_out", "why", "rule", "k")}
    kco = np.ones((P, K))                       # 買進時定的倉位係數（R3）
    xr = np.zeros((P, K), dtype=np.int8)        # 出場原因：1＝原出場、2＝R4、3＝兩者；0＝未決定（下市、期末）
    n_buys = np.zeros(P)
    n_half = np.zeros(P)
    r2_blk = np.zeros(P)
    n_avail = np.zeros(P)                       # 決策日名單中當時未持有的候選數（統計用）
    blk_log = [] if (P == 1 and IND is not None) else None

    def log_exit(mask, px_out, t, why):
        if not record:
            return
        pi, ji = np.nonzero(mask)
        if len(pi) == 0:
            return
        tr["p"].append(pi); tr["j"].append(ji); tr["t_in"].append(entry_t[pi, ji]); tr["t_out"].append(np.full(len(pi), t))
        tr["px_in"].append(entry_px[pi, ji]); tr["px_out"].append(np.broadcast_to(px_out, mask.shape)[pi, ji])
        tr["why"].append(np.full(len(pi), why))
        tr["rule"].append(xr[pi, ji].copy()); tr["k"].append(kco[pi, ji].copy())

    nav_prev = np.ones(P)
    for t in range(t0 + 1, T):
        r = m.rate[t - 1]
        if np.isfinite(r):
            cash *= 1.0 + r / 100.0 / 252.0
        cp, cn, on = C[t - 1], C[t], O[t]
        with np.errstate(invalid="ignore", divide="ignore"):
            gC = cn / cp
            gO = on / cp
            gOC = cn / on
        gC = np.where(np.isfinite(gC), gC, 1.0)
        okO = np.isfinite(on) & np.isfinite(gO)
        gO = np.where(okO, gO, 1.0)
        gOC = np.where(okO & np.isfinite(gOC), gOC, gC)
        w = exec_of.get(t)
        if w is None and not pend.any():
            val *= gC
        else:
            val = np.where(okO[None, :], val * gO[None, :], val)            # 開盤無法成交者停在前一日收盤
            held_dec = held.copy()                                           # 決策日當時的持有（含本次要賣的）
            if w is not None:
                if exit_rule == "12m":
                    ex = held & (w - entry_w >= cm.HOLD_MONTHS)
                else:
                    ex = held & (w > entry_w) & B200[w][None, :]
                code = ex.astype(np.int8)
                if X4 is not None:
                    e4 = held & X4[w][None, :]
                    code = code + 2 * e4.astype(np.int8)
                    ex = ex | e4
                xr = np.where(ex & ~pend, code, xr)
                sell = ex | pend
            else:
                sell = pend.copy()
            s_open = sell & okO[None, :]
            if s_open.any():
                proceeds = (val * s_open).sum(1)
                cash += proceeds * (1 - cs)
                sell_frac += proceeds / nav_prev
                log_exit(s_open, np.where(okO, on, np.nan)[None, :], t, 1 if w is not None else 3)
                val[s_open] = 0.0
                held[s_open] = False
                pend[s_open] = False
            s_close = sell & ~okO[None, :] & ROW[t][None, :]
            pend |= sell & ~ROW[t][None, :]
            if w is not None and not (freeze is not None and freeze[w]):
                keep = held & ~sell
                buy = np.zeros((P, K), dtype=bool)
                S = sel_lists[w]
                norder = np.zeros(P)
                if S is not None and S.size:
                    S = np.broadcast_to(S, (P, S.shape[1]))
                    valid = S >= 0
                    Sc = np.where(valid, S, 0)
                    avail = valid & ~np.take_along_axis(held if rebuy_on_exit else held_dec, Sc, axis=1)    # 持有期間不重複買
                    n_avail += avail.sum(1)
                    feas = avail
                    if IND is not None:
                        okg = industry_room(Sc, avail, keep, IND, OH, ind_cap)
                        feas = avail & okg
                    if design == "ii":
                        vac = cm.N_SEATS - keep.sum(1)
                        pick = feas & (np.cumsum(feas, axis=1) <= vac[:, None])
                        if IND is not None:                                      # 抽到時座位還沒滿、因產業超限跳過者
                            blk = avail & ~okg & ((np.cumsum(feas, axis=1) - feas) < vac[:, None])
                    else:
                        pick = feas
                        if IND is not None:
                            blk = avail & ~okg
                    if IND is not None:
                        r2_blk += blk.sum(1)
                        if blk_log is not None and blk[0].any():
                            blk_log.append((w, Sc[0][blk[0]].copy()))
                    pi, ri = np.nonzero(pick)
                    buy[pi, Sc[pi, ri]] = True
                    norder = pick.sum(1).astype(float)
                newb = buy & okO[None, :]
                if design == "i":
                    kt = keep & okO[None, :]
                    nT = kt.sum(1) + newb.sum(1)
                    I = cash + (val * kt).sum(1)
                    cur = np.where(kt, val, 0.0)
                    den = np.maximum(nT, 1)
                    if HF is None:
                        x = I / den
                        for _ in range(5):
                            up = (np.clip(x[:, None] - cur, 0, None) * kt).sum(1)
                            dn = (np.clip(cur - x[:, None], 0, None) * kt).sum(1)
                            cost = cb * (up + x * newb.sum(1)) + cs * dn
                            x = (I - cost) / den
                        up = (np.clip(x[:, None] - cur, 0, None) * kt).sum(1)
                        dn = (np.clip(cur - x[:, None], 0, None) * kt).sum(1)
                        cost = cb * (up + x * newb.sum(1)) + cs * dn
                        has = nT > 0
                        tgt = (kt | newb) & has[:, None]
                        val = np.where(tgt, x[:, None], val)
                        cash = np.where(has, I - nT * x - cost, cash)
                        buy_frac += np.where(has, up + x * newb.sum(1), 0.0) / nav_prev
                    else:                                                        # R3：目標＝x × 係數，差額留現金
                        kw = np.where(newb, np.where(HF[w], 0.5, 1.0)[None, :], kco)
                        nk = (kw * newb).sum(1)
                        x = I / den
                        for _ in range(5):
                            tx = x[:, None] * kw
                            up = (np.clip(tx - cur, 0, None) * kt).sum(1)
                            dn = (np.clip(cur - tx, 0, None) * kt).sum(1)
                            cost = cb * (up + x * nk) + cs * dn
                            x = (I - cost) / den
                        tx = x[:, None] * kw
                        up = (np.clip(tx - cur, 0, None) * kt).sum(1)
                        dn = (np.clip(cur - tx, 0, None) * kt).sum(1)
                        cost = cb * (up + x * nk) + cs * dn
                        has = nT > 0
                        tgt = (kt | newb) & has[:, None]
                        val = np.where(tgt, tx, val)
                        cash = np.where(has, I - (tx * tgt).sum(1) - cost, cash)
                        buy_frac += np.where(has, up + x * nk, 0.0) / nav_prev
                    sell_frac += np.where(has, dn, 0.0) / nav_prev
                    px_new = np.broadcast_to(on, (P, K))
                else:
                    navo = cash + (val * held).sum(1)
                    amt = np.minimum(navo / cm.N_SEATS, cash / np.maximum(norder, 1.0))
                    amt = np.where(norder > 0, amt, 0.0)
                    nb = newb.sum(1)
                    if HF is None:
                        val = np.where(newb, (amt / (1 + cb))[:, None], val)
                        cash = cash - amt * nb
                        buy_frac += amt * nb / nav_prev
                    else:                                                        # R3：該席金額 × 0.5，其餘留現金
                        aj = np.where(newb, amt[:, None] * np.where(HF[w], 0.5, 1.0)[None, :], 0.0)
                        val = np.where(newb, aj / (1 + cb), val)
                        cash = cash - aj.sum(1)
                        buy_frac += aj.sum(1) / nav_prev
                    px_new = np.broadcast_to(on, (P, K))
                held |= newb
                entry_w[newb] = w
                entry_t[newb] = t
                entry_px[newb] = px_new[newb]
                xr[newb] = 0
                n_buys += newb.sum(1)
                if HF is not None:
                    kco = np.where(newb, np.where(HF[w], 0.5, 1.0)[None, :], kco)
                    n_half += (newb & HF[w][None, :]).sum(1)
            val = np.where(okO[None, :], val * gOC[None, :], val * gC[None, :])
            if s_close.any():
                proceeds = (val * s_close).sum(1)
                cash += proceeds * (1 - cs)
                sell_frac += proceeds / nav_prev
                log_exit(s_close, cn[None, :], t, 2 if w is not None else 3)
                val[s_close] = 0.0
                held[s_close] = False
                pend[s_close] = False
        js = delist_at.get(t)
        if js is not None:
            mk = held[:, js]
            if mk.any():
                sub = val[:, js] * mk
                cash += sub.sum(1) * (1 - cs)
                sell_frac += sub.sum(1) / nav_prev
                full = np.zeros((P, K), dtype=bool)
                full[:, js] = mk
                log_exit(full, cn[None, :], t, 4)
                val[full] = 0.0
                held[full] = False
                pend[full] = False
        nv = cash + val.sum(1)
        nav[:, t - t0] = nv
        nheld_sum += held.sum(1)
        expo_sum += 1.0 - cash / nv
        if nheld_daily is not None:
            nheld_daily[:, t - t0] = held.sum(1)
        nav_prev = nv
    # 期末未平倉：以最後收盤、扣賣出成本計逐筆報酬（淨值不受影響）
    if record and held.any():
        log_exit(held, C[T - 1][None, :], T - 1, 0)
    ndays = n_run - 1
    dates = m.dates[t0:]
    yrs = cm.years_between(dates[0], dates[-1])
    out = dict(dates=dates, nav=nav, avg_held=nheld_sum / ndays, nheld_sum=nheld_sum, ndays=ndays, avg_expo=expo_sum / ndays,
               turnover=(buy_frac + sell_frac) / 2.0 / yrs, nheld_daily=nheld_daily, cols=cols,
               n_buys=n_buys, n_half=n_half, r2_blocked=r2_blk, r2_block_log=blk_log, n_avail=n_avail)
    if record:
        tt = {k: (np.concatenate(v) if v else np.array([], dtype=float)) for k, v in tr.items()}
        tt["ret"] = tt["px_out"] / tt["px_in"] * (1 - cs) / (1 + cb) - 1.0 if len(tt["p"]) else np.array([])
        tt["j"] = cols[tt["j"].astype(int)] if len(tt["j"]) else tt["j"]
        out["trades"] = tt
    return out


def industry_room(Sc, avail, keep, IND, OH, cap):
    """R2：(P, n) bool。候選依 Sc 的順序遞補時，該檔所屬產業「在席數＋本月排在它前面（含）的可買同產業檔數」≤ cap 才可買；
    產業缺值（-1）一律可買。keep：(P, K) 本月不賣的持股；OH：(K, G) 產業 one-hot（這裡只用到 G）。
    同產業前面的候選若因座位已滿沒買到，後面的也不會買到（座位仍滿），所以排名只需在可買者（avail）之間數。"""
    g = IND[Sc]
    ok = g < 0
    if OH is None:
        return ok
    present = np.unique(g[avail & (g >= 0)])
    if len(present) == 0:
        return ok
    lut = np.full(OH.shape[1], -1, dtype=np.int64)
    lut[present] = np.arange(len(present))
    pi, ki = np.nonzero(keep)
    gk = IND[ki]
    ga = np.where(gk >= 0, lut[np.maximum(gk, 0)], -1)
    KC = np.zeros((keep.shape[0], len(present)), dtype=np.int64)                  # (P, |present|) 在席數（整數計數）
    np.add.at(KC, (pi[ga >= 0], ga[ga >= 0]), 1)
    for a, gi in enumerate(present):
        ing = avail & (g == gi)
        ok = ok | (ing & (np.cumsum(ing, axis=1) + KC[:, a:a + 1] <= cap))
    return ok


# ---------------------------------------------------------------- 遞補順序
def col_lookup(cols, N):
    """全欄位位置 → 模擬欄位位置（不在 cols 內為 -1）。"""
    pos = np.full(N, -1, dtype=np.int64)
    pos[np.asarray(cols, dtype=int)] = np.arange(len(cols))
    return pos


def lists_fixed(cand: np.ndarray, pos: np.ndarray):
    """設計 (i)：每月名單全買（順序無關）。cand：(W, N) bool。回傳 sel_lists（每項 (1, n)）。"""
    out = []
    for w in range(cand.shape[0]):
        js = np.where(cand[w])[0]
        out.append(pos[js][None, :] if len(js) else None)
    return out


def lists_seeded(cand: np.ndarray, pos: np.ndarray, seeds, base=cm.SEED):
    """設計 (ii)：種子 s 的遞補順序＝default_rng([base, s]).random((W, M)) 由小到大（M＝母體代號數，代號字串排序）。"""
    W, M = cand.shape
    seeds = list(seeds)
    P = len(seeds)
    js_w = [np.where(cand[w])[0] for w in range(W)]
    out = [np.full((P, len(js)), -1, dtype=np.int64) if len(js) else None for js in js_w]
    for p, s in enumerate(seeds):
        k = np.random.default_rng([base, int(s)]).random((W, M))
        for w, js in enumerate(js_w):
            if len(js):
                out[w][p] = pos[js[np.argsort(k[w, js], kind="stable")]]
    return out


def lists_random(pool: np.ndarray, n_draw: np.ndarray, pos: np.ndarray, reps=cm.N_RANDOM, seed=cm.SEED):
    """隨機對照：每月從 pool[w] 抽 n_draw[w] 檔（不放回），reps 次共用一個產生器 default_rng(seed)，月份依序。
    第 r 次第 w 月：rng.random((reps, |pool_w|)) 的第 r 列由小到大取前 n 檔（代號字串排序對應欄），
    該順序也是設計 (ii) 的遞補順序。抽 0 檔的月份不消耗亂數。"""
    rng = np.random.default_rng(seed)
    out = []
    for w in range(pool.shape[0]):
        js = np.where(pool[w])[0]
        n = int(n_draw[w])
        if n == 0 or len(js) == 0:
            out.append(None)
            continue
        n = min(n, len(js))
        k = rng.random((reps, len(js)))
        if n < len(js):
            part = np.argpartition(k, n - 1, axis=1)[:, :n]
        else:
            part = np.broadcast_to(np.arange(len(js)), (reps, n)).copy()
        o = np.argsort(np.take_along_axis(k, part, axis=1), axis=1, kind="stable")
        sel = np.take_along_axis(part, o, axis=1)
        out.append(pos[js][sel])
    return out
