"""「趨勢上修」升級回測的新增部分：有預估母體、新種子規則、滿席率、成交金額五分位。
規格：docs/TroughBreakout_Upgrade_Prereg.md（2026-11-03，commit 8bc46ab）。

訊號（L1／L2／L3）、組合引擎、成本、現金、出場都沿用本套件既有程式（signals.py、engine.py），這裡不重寫。
Python 3.9 相容（系統 python3 跑回測）。
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import common as cm

OUT = cm.ROOT / "data" / "trough_breakout_upgrade_2010-2026"
PREREG = cm.ROOT / "docs" / "TroughBreakout_Upgrade_Prereg.md"
PREREG_COMMIT = "8bc46ab"
SEED_KEY_II = (20261103, 2)          # 設計 (ii)：default_rng([20261103, 2, 種子])，種子 1..1000
SEED_KEY_RAND = (20261103, 3)        # 隨機對照：default_rng([20261103, 3, 次數])，次數 1..1000
FILL_NUM, FILL_DEN = 4, 5            # 滿席率 ≥ 80%＝4/5：逐日平均在席數 ≥ 4/5 × 5 席＝4 檔（整數比較）


# ---------------------------------------------------------------- 有預估母體（登記第三節）
def estimate_mask(eps_ff: pd.DataFrame, codes, dec_dates) -> np.ndarray:
    """(W, N) bool：決策日當天（含）以前有 NTM EPS 值、91 天前（含）以前也有值、且 91 天前的值 > 0。
    eps_ff：tw_data.load_eps 回傳的已向前補寬表（查某日即得當天含以前最近一筆，不限新舊，沿用上一份第七節第 4 條）。
    查值方式與 signals.eps_layer 相同（searchsorted side=right − 1）。母體條件（代號、流動性）由呼叫端另外 AND。"""
    W, N = len(dec_dates), len(codes)
    out = np.zeros((W, N), dtype=bool)
    col = {c: j for j, c in enumerate(codes)}
    js = np.array([col[c] for c in eps_ff.columns], dtype=int)
    idx = eps_ff.index.values
    E = eps_ff.values
    for w, d in enumerate(dec_dates):
        i1 = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(d)), side="right")) - 1
        i0 = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(d) - pd.Timedelta(days=cm.EPS_LAG_DAYS)), side="right")) - 1
        if i1 < 0 or i0 < 0:
            continue
        now, then = E[i1], E[i0]
        with np.errstate(invalid="ignore"):
            out[w, js] = np.isfinite(now) & np.isfinite(then) & (then > 0)
    return out


def last_obs_age_days(eps_raw: pd.DataFrame, codes, dec_dates) -> np.ndarray:
    """(W, N)：決策日當天（含）以前最近一筆「原始」NTM EPS 觀測距決策日的日曆天數；從未有值為 NaN。
    eps_raw：未向前補的原檔寬表。只供疑點節（序列已停的股票）用，不進判定。"""
    W, N = len(dec_dates), len(codes)
    out = np.full((W, N), np.nan)
    col = {c: j for j, c in enumerate(codes)}
    keep = [c for c in eps_raw.columns if c in col]
    R = eps_raw[keep]
    idx = R.index.values
    pos = np.where(R.notna().values, np.arange(len(R))[:, None], -1)
    lastpos = np.maximum.accumulate(pos, axis=0)
    js = np.array([col[c] for c in keep], dtype=int)
    for w, d in enumerate(dec_dates):
        i = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(d)), side="right")) - 1
        if i < 0:
            continue
        lp = lastpos[i]
        ok = lp >= 0
        age = (np.datetime64(pd.Timestamp(d)) - idx[np.where(ok, lp, 0)]) / np.timedelta64(1, "D")
        out[w, js] = np.where(ok, age, np.nan)
    return out


# ---------------------------------------------------------------- 種子（登記第二、五節）
def lists_seeded_key(cand: np.ndarray, pos: np.ndarray, seeds, key=SEED_KEY_II):
    """設計 (ii) 遞補順序：種子 s 用 default_rng([*key, s]).random((W, M)) 由小到大（M＝代號數，代號字串排序）。
    與 engine.lists_seeded 相同，只把種子序列改成登記的三段式。"""
    W, M = cand.shape
    seeds = list(seeds)
    P = len(seeds)
    js_w = [np.where(cand[w])[0] for w in range(W)]
    out = [np.full((P, len(js)), -1, dtype=np.int64) if len(js) else None for js in js_w]
    for p, s in enumerate(seeds):
        k = np.random.default_rng([*key, int(s)]).random((W, M))
        for w, js in enumerate(js_w):
            if len(js):
                out[w][p] = pos[js[np.argsort(k[w, js], kind="stable")]]
    return out


def lists_random_key(pool: np.ndarray, n_draw: np.ndarray, pos: np.ndarray, reps=cm.N_RANDOM, key=SEED_KEY_RAND):
    """隨機對照：第 r 次（r＝1..reps）用自己的產生器 default_rng([*key, r])，月份依序；
    第 w 月從 pool[w]（代號字串排序）抽 rng.random(|pool_w|) 最小的 n_draw[w] 檔，不放回，抽出順序即設計 (ii) 遞補順序。
    抽 0 檔或 pool 為空的月份不消耗亂數（主規則 0 檔的月份不抽新股）。"""
    W = pool.shape[0]
    js_w = [np.where(pool[w])[0] for w in range(W)]
    ns = [min(int(n_draw[w]), len(js_w[w])) for w in range(W)]
    out = [np.full((reps, n), -1, dtype=np.int64) if n > 0 else None for n in ns]
    for r in range(reps):
        g = np.random.default_rng([*key, r + 1])
        for w in range(W):
            n = ns[w]
            if n == 0:
                continue
            k = g.random(len(js_w[w]))
            out[w][r] = pos[js_w[w][np.argsort(k, kind="stable")[:n]]]
    return out


# ---------------------------------------------------------------- 判準 6（登記第六節）
def median_ge(nheld_sum: np.ndarray, ndays: int, num: int, den: int = 1) -> bool:
    """各路徑「逐日平均持有檔數」的中位數 ≥ num/den，整數比較（偶數條路徑時中位數＝中間兩者平均）。"""
    v = np.sort(np.rint(np.asarray(nheld_sum)).astype(np.int64))
    n = len(v)
    if n % 2:
        return bool(den * v[n // 2] >= num * ndays)
    return bool(den * (v[n // 2 - 1] + v[n // 2]) >= 2 * num * ndays)


def fill_rate_ok(nheld_sum: np.ndarray, ndays: int) -> bool:
    """設計 (ii)：全期逐日平均在席數 ÷ 5 ≥ 80%（各種子中位數）。等價於逐日平均在席數 ≥ 4 檔。"""
    return median_ge(nheld_sum, ndays, FILL_NUM * cm.N_SEATS, FILL_DEN)


def judge(s: dict, b: dict, p90: float, hit: dict, enough: bool) -> dict:
    """s：組合指標（設計 (ii) 為中位數）；b：指數；p90：對應設計的趨勢組（有預估）隨機對照第 90 百分位；
    hit：report_stats.hit_summary（有預估母體基準率）；enough：判準 6。全部嚴格大於。
    判準 6 不過時其餘判準記 None（不比），整組不成立。"""
    c = {"6_enough_names": bool(enough)}
    raw = {
        "1_cagr_gt_index": bool(s["cagr"] > b["cagr"]),
        "2_calmar_gt_index": bool(s["calmar"] > b["calmar"]),
        "3_pre_post_gt_index": bool(s["pre_cagr"] > b["pre_cagr"] and s["post_cagr"] > b["post_cagr"]),
        "4_cagr_gt_trend_est_random_p90": bool(s["cagr"] > p90),
        "5_hit_2x_est_base_pre_post": bool(hit["pre"]["pass_2x"] and hit["post"]["pass_2x"]),
    }
    for k, v in raw.items():
        c[k] = v if enough else None
    c["raw_if_compared"] = raw
    c["all_pass"] = bool(enough and all(raw.values()))
    c["no_signal"] = not enough
    return c


def pct_rank(dist: np.ndarray, x: float) -> float:
    """x 在分布中的百分位：低於 x 的比例 ＋ 相等者的一半，× 100。"""
    d = np.asarray(dist, dtype=float)
    return float(100.0 * ((d < x).sum() + 0.5 * (d == x).sum()) / len(d))


# ---------------------------------------------------------------- 成交金額（市值代理，登記第七節）
def amount20_at(m, dec: np.ndarray, start="2007-01-01") -> np.ndarray:
    """(W, N) int64：決策日近 20 個交易日（含）成交金額合計（元），口徑同 tw_data.load_prices 的流動性。
    重讀面板 value 欄；呼叫端核對 ≥ 2 億元的格子與 m.liq 完全一致。"""
    from .tw_data import PANEL, code_ok
    p = pd.read_parquet(PANEL / "prices.parquet", columns=["date", "code", "value"])
    p = p[(p["date"] >= pd.Timestamp(start)) & p["code"].map(code_ok)]
    di = pd.Series(np.arange(len(m.dates)), index=m.dates)
    ci = pd.Series(np.arange(len(m.codes)), index=m.codes)
    V = np.zeros((len(m.dates), len(m.codes)))
    V[di.loc[p["date"]].values, ci.loc[p["code"]].values] = p["value"].fillna(0.0).values
    cs = np.cumsum(V, axis=0)
    out = np.zeros((len(dec), len(m.codes)), dtype=np.int64)
    for w, d in enumerate(dec):
        d = int(d)
        s = cs[d] - (cs[d - cm.LIQ_WIN] if d - cm.LIQ_WIN >= 0 else 0.0)
        out[w] = np.rint(s).astype(np.int64) if d >= cm.LIQ_WIN - 1 else 0
    return out


def quintile_of(amount: np.ndarray, base: np.ndarray) -> np.ndarray:
    """(W, N) int8：在 base[w] 內依成交金額由小到大的五分位 1..5（同值依代號順序），base 以外為 0。
    名次 r＝1..n，五分位＝(5r − 1) // n + 1（整數）。"""
    W, N = amount.shape
    q = np.zeros((W, N), dtype=np.int8)
    for w in range(W):
        js = np.where(base[w])[0]
        n = len(js)
        if n == 0:
            continue
        order = js[np.argsort(amount[w, js], kind="stable")]
        r = np.arange(1, n + 1)
        q[w, order] = ((5 * r - 1) // n + 1).astype(np.int8)
    return q
