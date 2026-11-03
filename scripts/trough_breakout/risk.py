"""「翻身突破」降回撤組合版：四條手段的輸入、組別設定、判準。
規格：docs/TroughBreakout_Risk_Prereg.md（2026-11-03，commit 4e63690）。

訊號（L1／L2）、組合引擎、成本、現金、原出場都沿用 signals.py／engine.py；四條手段以 engine.simulate 的
選用參數接上（extra_exit＝R4、half＝R3、ind＝R2），R1 在候選名單層把閘門月清空。
離散門檻一律在整數空間比：R1 用指數「分」為單位的整數和，R2～R4 用整數 bps（萬分之一）。
Python 3.9 相容（系統 python3 跑回測）。
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

from . import common as cm
from . import engine as en

OUT = cm.ROOT / "data" / "trough_breakout_risk_2010-2026"
PREREG = cm.ROOT / "docs" / "TroughBreakout_Risk_Prereg.md"
PREREG_COMMIT = "4e63690"
BASE_RESULTS_COMMIT = "27566ae"
INDEX_PARQUET = cm.ROOT / "data" / "revmom" / "index_tr.parquet"
INDUSTRY_CSV = cm.ROOT / "docs" / "QueueOrder_IndustryMap_tw.csv"
INDUSTRY_FALLBACK = Path(__file__).resolve().parent / "QueueOrder_IndustryMap_tw.csv"   # 網站 repo 副本放在程式旁

SEED_KEY_II = (20261103, 4)          # 設計 (ii)：default_rng([20261103, 4, 種子])，種子 1..1000
R1_MA = 200                          # 加權報酬指數 200 日簡單均線
IND_CAP = 2                          # R2：同產業最多 2 檔
R3_RET_BPS = 15000                   # R3：126 日報酬 > 150%（> 15000 bps）
R4_HI_BPS = 8000                     # R4：收盤 < 250 日最高收盤 × 80%（< 8000 bps）
FILL_MIN_SEATS = 3                   # 判準 5 設計 (ii)：滿席率 ≥ 60% ＝ 逐日平均在席 ≥ 3 檔
MDD_GAP_BPS = 500                    # 判準 2、4：5 個百分點
WIN_1820 = ("2018-06", "2018-06-01", "2020-03-31")

MEASURES = ("r1", "r2", "r3", "r4")
CONFIGS = {"base": (), "combo": MEASURES, "r1": ("r1",), "r2": ("r2",), "r3": ("r3",), "r4": ("r4",)}
CNAME = dict(base="基準線", combo="組合版", r1="只加大盤閘門", r2="只加產業上限", r3="只加過熱減半", r4="只加離高點出場")


# ---------------------------------------------------------------- 整數 bps
def bps_units(a, b):
    """a ÷ b 以萬分之一（bps）為單位四捨五入成 int64；任一為 NaN 或 b ≤ 0 時回傳 -1（呼叫端視為無效）。"""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b) & (b > 0)
    out = np.full(np.broadcast(a, b).shape, -1, dtype=np.int64)
    with np.errstate(divide="ignore", invalid="ignore"):
        q = np.rint(np.where(ok, a / np.where(ok, b, 1.0), 0.0) * 10000.0)
    out[ok] = q[ok].astype(np.int64)
    return out


def mdd_bps(x) -> int:
    """回撤（負小數）→ 整數 bps。"""
    return int(np.rint(float(x) * 10000.0))


# ---------------------------------------------------------------- R1 大盤閘門
def load_index() -> pd.Series:
    t = pd.read_parquet(INDEX_PARQUET).set_index("date")["taiex_tr"].sort_index()
    return t


def index_gate(dec_dates, tr: pd.Series = None) -> dict:
    """決策日加權報酬指數收盤 < 其 200 日簡單均線 → 閘門（True＝當月不買新股）。
    均線用指數自己的交易日；指數值以「分」（× 100）轉整數，比較 200 × 收盤 < 近 200 日收盤合計，恰好相等不觸發。"""
    tr = load_index() if tr is None else tr
    cents = np.rint(tr.values * 100.0).astype(np.int64)
    if np.max(np.abs(tr.values * 100.0 - cents)) > 1e-6:
        raise ValueError("指數不是兩位小數，不能用分為單位")
    cs = np.concatenate([[0], np.cumsum(cents)])
    pos = pd.Series(np.arange(len(tr)), index=tr.index)
    W = len(dec_dates)
    gate = np.zeros(W, dtype=bool)
    close = np.full(W, np.nan)
    ma = np.full(W, np.nan)
    gap_bps = np.zeros(W, dtype=np.int64)
    for w, d in enumerate(pd.DatetimeIndex(dec_dates)):
        if d not in pos.index:
            raise ValueError(f"決策日 {d.date()} 沒有指數收盤")
        i = int(pos[d])
        if i < R1_MA - 1:
            raise ValueError(f"決策日 {d.date()} 指數不足 200 日")
        s = int(cs[i + 1] - cs[i + 1 - R1_MA])
        gate[w] = R1_MA * int(cents[i]) < s
        close[w] = cents[i] / 100.0
        ma[w] = s / R1_MA / 100.0
        gap_bps[w] = int(bps_units(R1_MA * cents[i], s)) - 10000
    return dict(gate=gate, close=close, ma=ma, gap_bps=gap_bps)


# ---------------------------------------------------------------- R2 產業
def industry_csv() -> Path:
    """產業對照表：環境變數 TB_INDUSTRY_CSV 指定者優先；否則 INDUSTRY_CSV，不存在再用 INDUSTRY_FALLBACK；都沒有就報錯。"""
    env = os.environ.get("TB_INDUSTRY_CSV")
    if env:
        return Path(env)
    for p in (INDUSTRY_CSV, INDUSTRY_FALLBACK):
        if p.exists():
            return p
    raise FileNotFoundError(f"找不到產業對照表：{INDUSTRY_CSV}、{INDUSTRY_FALLBACK}（可用 TB_INDUSTRY_CSV 指定）")


def industry_codes(codes) -> tuple:
    """回傳 (ind (N,) int，-1＝缺值；產業名稱串列，依名稱排序)。代號不在對照表或 industry 欄空白者為缺值。"""
    t = pd.read_csv(industry_csv(), dtype=str)
    t = t[t["industry"].notna() & (t["industry"].str.strip() != "")]
    mp = dict(zip(t["code"].str.strip(), t["industry"].str.strip()))
    names = sorted(set(mp.get(c) for c in codes if c in mp))
    gi = {g: k for k, g in enumerate(names)}
    ind = np.array([gi[mp[c]] if c in mp else -1 for c in codes], dtype=np.int64)
    return ind, names


# ---------------------------------------------------------------- R3、R4 與 R2 排序用的價格值
def price_inputs(m, dec) -> dict:
    """(W, N)：ret126_bps＝決策日收盤 ÷ 126 個交易日前收盤 − 1（整數 bps，無效為 None 遮罩外）、
    hi250_bps＝決策日收盤 ÷ 近 250 個交易日（含）最高收盤（整數 bps）。
    r3＝ret126_bps > 15000；r4＝0 ≤ hi250_bps < 8000。"""
    C = m.C
    W, N = len(dec), C.shape[1]
    ret = np.full((W, N), -10 ** 9, dtype=np.int64)
    ret_ok = np.zeros((W, N), dtype=bool)
    hib = np.full((W, N), -1, dtype=np.int64)
    for w, d in enumerate(dec):
        d = int(d)
        c = C[d]
        lo = max(d - cm.HI_WIN + 1, 0)
        win = C[lo:d + 1]
        with np.errstate(invalid="ignore", all="ignore"):
            hi = np.max(np.where(np.isnan(win), -np.inf, win), axis=0)
        hi = np.where(np.isfinite(hi), hi, np.nan)
        hib[w] = bps_units(c, hi)
        if d - cm.RET_LAG >= 0:
            b = bps_units(c, C[d - cm.RET_LAG])
            ok = b >= 0
            ret[w] = np.where(ok, b - 10000, ret[w])
            ret_ok[w] = ok
    r3 = ret_ok & (ret > R3_RET_BPS)
    r4 = (hib >= 0) & (hib < R4_HI_BPS)
    return dict(ret126_bps=ret, ret126_ok=ret_ok, hi250_bps=hib, r3=r3, r4=r4)


# ---------------------------------------------------------------- 名單與參數
def cand_for(cfg: str, main: np.ndarray, gate: np.ndarray) -> np.ndarray:
    """R1：閘門月清空候選（當月不買新股；已持有者照出場規則）。"""
    c = main.copy()
    if "r1" in CONFIGS[cfg]:
        c[gate] = False
    return c


def sim_kwargs(cfg: str, inp: dict) -> dict:
    ms = CONFIGS[cfg]
    return dict(extra_exit=inp["r4"] if "r4" in ms else None,
                half=inp["r3"] if "r3" in ms else None,
                ind=inp["ind"] if "r2" in ms else None, ind_cap=IND_CAP)


def lists_fixed_ordered(cand: np.ndarray, pos: np.ndarray, ret_bps: np.ndarray):
    """設計 (i) 有 R2 時的遞補順序：近 126 日報酬（整數 bps）由低到高，同分取代號小者（代號字串排序＝欄位序）。"""
    out = []
    for w in range(cand.shape[0]):
        js = np.where(cand[w])[0]
        if len(js) == 0:
            out.append(None)
            continue
        o = np.lexsort((js, ret_bps[w, js]))
        out.append(pos[js[o]][None, :])
    return out


def run(m, L, cand, cfg, ex, design, inp, key=SEED_KEY_II, record=True, freeze=None, seeds=None):
    """跑一組。design 'i'：單一路徑；'ii'：種子 1..1000（key＝None 時用第一份的舊種子 default_rng([20261103, 種子])）。"""
    from . import upgrade as up
    N = len(m.codes)
    cols = np.where(cand.any(0))[0]
    pos = en.col_lookup(cols, N)
    kw = sim_kwargs(cfg, inp)
    if design == "i":
        sl = lists_fixed_ordered(cand, pos, inp["ret126_bps"]) if kw["ind"] is not None else en.lists_fixed(cand, pos)
        return en.simulate(m, L.dec, cols, sl, "i", ex, L.below200, 1, record=record, freeze=freeze, **kw)
    seeds = list(range(1, cm.N_SEEDS + 1)) if seeds is None else list(seeds)
    sl = en.lists_seeded(cand, pos, seeds) if key is None else up.lists_seeded_key(cand, pos, seeds, key)
    return en.simulate(m, L.dec, cols, sl, "ii", ex, L.below200, len(seeds), record=record, freeze=freeze, **kw)


# ---------------------------------------------------------------- 手段觸發統計（逐路徑）
def trigger_stats(r, P) -> pd.DataFrame:
    """每條路徑：當時未持有的候選數（n_avail）、成交買進筆數、R3 減半筆數與比例、R2 被擋候選數、R4 出場筆數（含與原出場同時觸發）與其平均報酬、
    只因 R4 出場的筆數。R4 出場＝出場原因碼 2 或 3（期末未平倉與下市不算）。"""
    tr = r.get("trades")
    rows = dict(n_avail=r["n_avail"], n_buys=r["n_buys"], n_half=r["n_half"], r2_blocked=r["r2_blocked"])
    df = pd.DataFrame(rows)
    df["half_share"] = np.where(df["n_buys"] > 0, df["n_half"] / df["n_buys"].where(df["n_buys"] > 0, 1), np.nan)
    if tr is not None and len(tr["p"]):
        p = tr["p"].astype(int)
        rule = tr["rule"].astype(int)
        why = tr["why"].astype(int)
        is4 = ((rule == 2) | (rule == 3)) & (why != 0)
        only4 = (rule == 2) & (why != 0)
        df["n_r4_exits"] = np.bincount(p[is4], minlength=P)
        df["n_r4_only_exits"] = np.bincount(p[only4], minlength=P)
        s = np.bincount(p[is4], weights=tr["ret"][is4], minlength=P)
        df["r4_exit_mean_ret"] = np.where(df["n_r4_exits"] > 0, s / np.maximum(df["n_r4_exits"], 1), np.nan)
        orig = (rule == 1) & (why != 0)
        df["n_orig_exits"] = np.bincount(p[orig], minlength=P)
    else:
        for k in ("n_r4_exits", "n_r4_only_exits", "n_orig_exits"):
            df[k] = 0
        df["r4_exit_mean_ret"] = np.nan
    return df


# ---------------------------------------------------------------- 判準（登記第五節）
def judge(s: dict, b: dict, base: dict, crash_s: dict, crash_b: dict, enough: bool) -> dict:
    """s：組合版指標（設計 (ii) 為中位數）；b：指數；base：基準線（同出場、同設計）；crash_*：四個崩盤窗回撤。
    比較一律嚴格大於、相等算沒過；回撤比較在整數 bps 上。判準 2 括號寫「≥ −500 bps」、判準 4 寫「至少 5 個百分點」，
    與開頭「嚴格大於」衝突，正式判定取較嚴的嚴格大於，另列含等號讀法（alt_inclusive）。"""
    gaps = {k: mdd_bps(crash_s[k]) - mdd_bps(crash_b[k]) for k in crash_b}
    d4 = mdd_bps(s["mdd"]) - mdd_bps(base["mdd"])
    c = {
        "1_calmar_gt_index": bool(s["calmar"] > b["calmar"]),
        "2_crash_windows_within_5pp": bool(all(v > -MDD_GAP_BPS for v in gaps.values())),
        "3_cagr_gt_index": bool(s["cagr"] > b["cagr"]),
        "4_mdd_shallower_than_base_by_5pp": bool(d4 > MDD_GAP_BPS),
        "5_enough_names": bool(enough),
    }
    c["all_pass"] = bool(all(c.values()))
    c["no_signal"] = not enough
    alt2 = all(v >= -MDD_GAP_BPS for v in gaps.values())
    alt4 = d4 >= MDD_GAP_BPS
    c["alt_inclusive"] = dict(c2=bool(alt2), c4=bool(alt4),
                              all_pass=bool(c["1_calmar_gt_index"] and alt2 and c["3_cagr_gt_index"] and alt4 and enough))
    c["values"] = dict(calmar=s["calmar"], index_calmar=b["calmar"], cagr=s["cagr"], index_cagr=b["cagr"],
                       mdd_bps=mdd_bps(s["mdd"]), base_mdd_bps=mdd_bps(base["mdd"]), mdd_improve_vs_base_bps=d4,
                       crash_gap_vs_index_bps=gaps,
                       crash_bps={k: mdd_bps(v) for k, v in crash_s.items()},
                       index_crash_bps={k: mdd_bps(v) for k, v in crash_b.items()})
    return c
