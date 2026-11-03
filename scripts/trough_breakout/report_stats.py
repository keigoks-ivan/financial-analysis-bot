"""逐筆統計、大漲命中率、判準。"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import common as cm


def trade_stats(tr, dates, P):
    """每條路徑：筆數、勝率、逐筆報酬中位數、平均持有日曆天數、五分位點。tr：engine 的 trades dict。"""
    p = tr["p"].astype(int) if len(tr["p"]) else np.array([], dtype=int)
    ret = tr["ret"]
    days = (dates.values[tr["t_out"].astype(int)] - dates.values[tr["t_in"].astype(int)]) / np.timedelta64(1, "D") \
        if len(p) else np.array([])
    rows = []
    for k in range(P):
        mk = p == k
        r = ret[mk]
        n = int(mk.sum())
        rows.append(dict(n_trades=n, win_rate=float((r > 0).mean()) if n else np.nan,
                         med_ret=float(np.median(r)) if n else np.nan,
                         avg_hold_days=float(days[mk].mean()) if n else np.nan,
                         q20=float(np.percentile(r, 20)) if n else np.nan, q40=float(np.percentile(r, 40)) if n else np.nan,
                         q60=float(np.percentile(r, 60)) if n else np.nan, q80=float(np.percentile(r, 80)) if n else np.nan))
    return pd.DataFrame(rows)


def hit_table(m, L, groups: dict) -> pd.DataFrame:
    """每個決策日：母體與各組「次一交易日開盤買進後、到 12 個月後決策日收盤為止的最高收盤 ≥ 買進價 2 倍」的檔數。
    12 個月窗不完整（第 w+12 個決策日不存在）的月份不列。買進日沒有開盤者不計。"""
    W = len(L.dec)
    C = np.where(np.isnan(m.C), -np.inf, m.C)
    rows = []
    for w in range(W - cm.HOLD_MONTHS):
        e, end = int(L.dec[w]) + 1, int(L.dec[w + cm.HOLD_MONTHS])
        o = m.O[e]
        ok = np.isfinite(o)
        mx = C[e:end + 1].max(axis=0)
        hit = cm.ratio_units(np.where(np.isfinite(mx), mx, np.nan), o) >= cm.U_DOUBLE
        r = dict(decision=m.dates[L.dec[w]].date(), exec=m.dates[e].date())
        base = L.univ[w] & ok
        r["n_univ"], r["hit_univ"] = int(base.sum()), int((hit & base).sum())
        for g, cand in groups.items():
            s = cand[w] & ok
            r[f"n_{g}"], r[f"hit_{g}"] = int(s.sum()), int((hit & s).sum())
        rows.append(r)
    return pd.DataFrame(rows)


def hit_summary(ht: pd.DataFrame, g: str) -> dict:
    """前段（買進日 ≤ 2017-12-31）／後段。判準 5：命中率 > 2 × 基準率（整數交叉相乘，相等不過）。"""
    out = {}
    ex = pd.to_datetime(ht["exec"])
    for name, mk in (("pre", ex <= pd.Timestamp("2017-12-31")), ("post", ex > pd.Timestamp("2017-12-31")), ("all", ex == ex)):
        s = ht[mk]
        nb, hb, nl, hl = int(s["n_univ"].sum()), int(s["hit_univ"].sum()), int(s[f"n_{g}"].sum()), int(s[f"hit_{g}"].sum())
        out[name] = dict(n_univ=nb, hit_univ=hb, base_rate=hb / nb if nb else np.nan, n_list=nl, hit_list=hl,
                         list_rate=hl / nl if nl else np.nan, months=int(len(s)),
                         pass_2x=bool(nl > 0 and hl * nb > 2 * hb * nl))
    return out


def judge(s: dict, b: dict, p90: float, hit: dict, held_ok: bool) -> dict:
    """s：組合指標（設計 (ii) 為中位數）；b：指數；p90：趨勢組隨機對照全期年化第 90 百分位；hit：hit_summary。"""
    c = {}
    c["6_avg_held_ge_5"] = bool(held_ok)
    c["1_cagr_gt_index"] = bool(s["cagr"] > b["cagr"])
    c["2_calmar_gt_index"] = bool(s["calmar"] > b["calmar"])
    c["3_pre_post_gt_index"] = bool(s["pre_cagr"] > b["pre_cagr"] and s["post_cagr"] > b["post_cagr"])
    c["4_cagr_gt_trend_random_p90"] = bool(s["cagr"] > p90)
    c["5_hit_2x_pre_post"] = bool(hit["pre"]["pass_2x"] and hit["post"]["pass_2x"])
    c["all_pass"] = bool(all(c.values()))
    c["no_signal"] = not held_ok
    return c


def held_ok_from_sums(nheld_sum: np.ndarray, ndays: int) -> bool:
    """月均持股 ≥ 5：設計 (i) 單一路徑；設計 (ii) 取各種子的中位數（偶數個時為中間兩者平均），整數比較。"""
    v = np.sort(np.rint(np.asarray(nheld_sum)).astype(np.int64))
    n = len(v)
    if n % 2:
        return bool(v[n // 2] >= 5 * ndays)
    return bool(v[n // 2 - 1] + v[n // 2] >= 10 * ndays)
