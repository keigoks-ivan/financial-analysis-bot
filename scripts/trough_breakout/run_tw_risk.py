"""「翻身突破」降回撤組合版主流程（docs/TroughBreakout_Risk_Prereg.md，commit 4e63690）。
輸出到 data/trough_breakout_risk_2010-2026/。

組別（登記第四節）：base＝基準線（第一份主規則 L1 且 L2）、combo＝組合版（R1＋R2＋R3＋R4，判定對象）、
r1／r2／r3／r4＝只加一條（附測，只報）。各 × 兩種出場（12m、200d）× 兩種設計（i 全部持有、ii 五席 1,000 種子）。
訊號、組合引擎、成本、現金、原出場沿用 signals.py／engine.py；四條手段的輸入在 risk.py。

用法（repo 根目錄）：
  python3 -m src.trough_breakout.run_tw_risk                          # 全部，含重現核對與獨立重算
  python3 -m src.trough_breakout.run_tw_risk --slice 2018-06 2020-03  # 只印閘門與各手段觸發檔數，不寫檔
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time

import numpy as np
import pandas as pd

from . import common as cm
from . import report_stats as rs
from . import risk as rk
from . import tw_data as td
from . import upgrade as up
from . import verify as vf
from .prep import prepare_tw

EXITS = ("12m", "200d")
PREV = cm.ROOT / "data" / "trough_breakout_2010-2026"
WINDOWS = list(cm.CRASH) + [rk.WIN_1820]
WKEY = {k: k for k, _, _ in cm.CRASH}
WKEY[rk.WIN_1820[0]] = "2018-06_2020-03"
REASON = {0: "—", 1: "原出場", 2: "離高點 20%", 3: "兩者同時"}
WHY = {0: "期末未平倉（以最後收盤計）", 1: "出場日開盤", 2: "出場日收盤（開盤缺）", 3: "停牌後補賣", 4: "下市（最後可得價）"}


def _scalar(d):
    return {k: (float(np.asarray(v).ravel()[0]) if np.ndim(v) else float(v)) for k, v in d.items()}


def mdd_dates(dates, nav):
    nav = np.asarray(nav)
    peak = np.maximum.accumulate(nav)
    dd = nav / peak - 1
    it = int(np.argmin(dd))
    ip = int(np.argmax(nav[:it + 1])) if it > 0 else 0
    return dict(peak=str(dates[ip].date()), trough=str(dates[it].date()), mdd=float(dd[it]))


def windows_of(run_dates, nav):
    """nav (P, T) → {窗名: (P,) 回撤}。"""
    return {WKEY[k]: cm.window_mdd(run_dates, nav, a, b) for k, a, b in WINDOWS}


def build_inputs(m, L):
    dd = m.dates[L.dec]
    g = rk.index_gate(dd)
    pi = rk.price_inputs(m, L.dec)
    ind, ind_names = rk.industry_codes(m.codes)
    return dict(gate=g["gate"], gate_info=g, r3=pi["r3"], r4=pi["r4"], ret126_bps=pi["ret126_bps"],
                hi250_bps=pi["hi250_bps"], ind=ind, ind_names=ind_names)


def slice_check(m, L, inp, a, b):
    dd = m.dates[L.dec]
    g = inp["gate_info"]
    for w, d in enumerate(dd):
        if pd.Timestamp(a) <= d <= pd.Timestamp(b) + pd.offsets.MonthEnd(0):
            mn = L.main[w]
            print(d.date(), f"指數 {g['close'][w]:,.2f} 200 日均 {g['ma'][w]:,.2f} 差 {g['gap_bps'][w]:+d} bps",
                  "閘門" if g["gate"][w] else "    ", "主規則", int(mn.sum()), "過熱", int((mn & inp["r3"][w]).sum()),
                  "產業缺值", int((mn & (inp["ind"] < 0)).sum()), "| 母體中離高點 >20%", int((L.univ[w] & inp["r4"][w]).sum()))


def held_by_industry_ok(m, L, tr, ind, cap):
    """獨立核對 R2：用逐筆成交重建每個成交日收盤的持股，數每個產業的檔數，回傳超過上限的（月, 產業）數與最大檔數。"""
    t_in, t_out, why, j = (tr[k].astype(int) for k in ("t_in", "t_out", "why", "j"))
    bad, worst = 0, 0
    for d in L.dec:
        t = int(d) + 1
        if t >= len(m.dates):
            continue
        h = (t_in <= t) & ((t_out > t) | ((why == 0) & (t_out >= t)))
        g = ind[j[h]]
        g = g[g >= 0]
        if len(g):
            c = np.bincount(g)
            worst = max(worst, int(c.max()))
            bad += int((c > cap).sum())
    return dict(months_industry_over_cap=bad, max_same_industry=worst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slice", nargs=2, default=None)
    args = ap.parse_args()
    t_all = time.time()
    m, L, dg = prepare_tw()
    inp = build_inputs(m, L)
    if args.slice:
        slice_check(m, L, inp, *args.slice)
        return
    rk.OUT.mkdir(parents=True, exist_ok=True)
    N = len(m.codes)
    dd = m.dates[L.dec]
    W = len(L.dec)
    gate = inp["gate"]
    ind = inp["ind"]
    names = pd.read_parquet(td.PANEL / "names.parquet").set_index("code")["name"].to_dict()
    t0 = int(np.searchsorted(m.dates.values, np.datetime64(cm.NAV_START)))
    bench_nav = m.bench.values[t0:] / m.bench.values[t0]
    run_dates = m.dates[t0:]
    bm = _scalar(cm.path_metrics(run_dates, bench_nav))
    bm["mdd_dates"] = mdd_dates(run_dates, bench_nav)
    idx_win = {k: float(v[0]) for k, v in windows_of(run_dates, bench_nav[None, :]).items()}
    summary = dict(prereg=str(rk.PREREG.relative_to(cm.ROOT)), prereg_commit=rk.PREREG_COMMIT,
                   prereg_sha256=hashlib.sha256(rk.PREREG.read_bytes()).hexdigest(), base_results_commit=rk.BASE_RESULTS_COMMIT,
                   data=m.info,
                   period=dict(nav_start=str(run_dates[0].date()), end=str(run_dates[-1].date()), pre_end=str(cm.PRE_END.date()),
                               decisions=W, first_decision=str(dd[0].date()), last_decision=str(dd[-1].date())),
                   seeds=dict(design_ii="default_rng([20261103, 4, s]), s=1..1000",
                              reproduction_old="default_rng([20261103, s]), s=1..1000（只供基準線重現核對）"),
                   index=bm, index_windows=idx_win, configs={k: list(v) for k, v in rk.CONFIGS.items()}, groups={})
    nav_cols = {"date": run_dates, "taiex_tr": bench_nav}
    seed_rows, trade_frames = [], []
    yearly = {"index": {y: float(v[0]) for y, v in cm.yearly_returns(run_dates, bench_nav).items()}}
    crash = {"index": idx_win}
    keep_nav, keep_i = {}, {}
    blk_logs = {}
    for cfg in rk.CONFIGS:
        cand = rk.cand_for(cfg, L.main, gate)
        summary["groups"][cfg] = {}
        for ex in EXITS:
            t1 = time.time()
            r1 = rk.run(m, L, cand, cfg, ex, "i", inp)
            met1 = _scalar(cm.path_metrics(run_dates, r1["nav"]))
            ts1 = rs.trade_stats(r1["trades"], m.dates, 1).iloc[0].to_dict()
            tg1 = rk.trigger_stats(r1, 1).iloc[0].to_dict()
            met1.update(avg_held=float(r1["avg_held"][0]), avg_expo=float(r1["avg_expo"][0]), turnover=float(r1["turnover"][0]),
                        held_ok=rs.held_ok_from_sums(r1["nheld_sum"], r1["ndays"]), **ts1)
            met1["triggers"] = {k: float(v) for k, v in tg1.items()}
            met1["mdd_dates"] = mdd_dates(run_dates, r1["nav"][0])
            wi = {k: float(v[0]) for k, v in windows_of(run_dates, r1["nav"]).items()}
            met1["windows"] = wi
            nav_cols[f"{cfg}_i_{ex}"] = r1["nav"][0]
            keep_i[(cfg, ex)] = r1
            if r1["r2_block_log"] is not None:
                blk_logs[(cfg, ex)] = r1["r2_block_log"]
            yearly[f"{cfg}_i_{ex}"] = {y: float(v[0]) for y, v in cm.yearly_returns(run_dates, r1["nav"]).items()}
            crash[f"{cfg}_i_{ex}"] = wi
            tr = r1["trades"]
            jj = tr["j"].astype(int)
            trade_frames.append(pd.DataFrame(dict(
                config=cfg, exit=ex, code=[m.codes[j] for j in jj], name=[names.get(m.codes[j], "") for j in jj],
                industry=[inp["ind_names"][ind[j]] if ind[j] >= 0 else "" for j in jj],
                buy_date=m.dates.values[tr["t_in"].astype(int)], sell_date=m.dates.values[tr["t_out"].astype(int)],
                buy_px_adj=tr["px_in"], sell_px_adj=tr["px_out"], ret_net=tr["ret"], coef=tr["k"],
                exit_reason=pd.Series(tr["rule"].astype(int)).map(REASON).values,
                why=pd.Series(tr["why"].astype(int)).map(WHY).values)))
            # 設計 (ii)
            r2 = rk.run(m, L, cand, cfg, ex, "ii", inp)
            mt2 = cm.path_metrics(run_dates, r2["nav"])
            df2 = pd.DataFrame({k: np.asarray(v) for k, v in mt2.items() if k != "years"})
            df2["avg_held"], df2["avg_expo"], df2["turnover"] = r2["avg_held"], r2["avg_expo"], r2["turnover"]
            df2["fill_rate"] = r2["avg_held"] / cm.N_SEATS
            df2 = pd.concat([df2, rs.trade_stats(r2["trades"], m.dates, cm.N_SEEDS), rk.trigger_stats(r2, cm.N_SEEDS)], axis=1)
            w2 = windows_of(run_dates, r2["nav"])
            for k, v in w2.items():
                df2[f"mdd_{k}"] = v
            df2.insert(0, "seed", np.arange(1, cm.N_SEEDS + 1))
            df2.insert(0, "exit", ex)
            df2.insert(0, "config", cfg)
            seed_rows.append(df2)
            med = {k: float(df2[k].median()) for k in df2.columns if k not in ("config", "exit", "seed")}
            med["fill_ok"] = up.median_ge(r2["nheld_sum"], r2["ndays"], rk.FILL_MIN_SEATS)
            med["held_ok"] = rs.held_ok_from_sums(r2["nheld_sum"], r2["ndays"])
            med["cagr_p10"], med["cagr_p90"] = float(df2["cagr"].quantile(0.1)), float(df2["cagr"].quantile(0.9))
            med["mdd_p10"], med["mdd_p90"] = float(df2["mdd"].quantile(0.1)), float(df2["mdd"].quantile(0.9))
            med["calmar_p10"], med["calmar_p90"] = float(df2["calmar"].quantile(0.1)), float(df2["calmar"].quantile(0.9))
            med["windows"] = {k: float(np.median(v)) for k, v in w2.items()}
            nav_cols[f"{cfg}_ii_{ex}_median"] = np.median(r2["nav"], axis=0)
            if cfg in ("combo", "base"):
                keep_nav[(cfg, ex)] = r2["nav"][:5].copy()
            yy = cm.yearly_returns(run_dates, r2["nav"])
            yearly[f"{cfg}_ii_{ex}_median"] = {y: float(np.median(v)) for y, v in yy.items()}
            crash[f"{cfg}_ii_{ex}_median"] = med["windows"]
            summary["groups"][cfg][ex] = dict(i=met1, ii_median=med)
            del r2
            print(f"{rk.CNAME[cfg]} {ex}：(i) 年化 {met1['cagr']:.2%} 回撤 {met1['mdd']:.1%} Calmar {met1['calmar']:.2f} "
                  f"持股 {met1['avg_held']:.1f}｜(ii) 年化 {med['cagr']:.2%} 回撤 {med['mdd']:.1%} Calmar {med['calmar']:.2f} "
                  f"滿席率 {med['fill_rate']:.1%}  {time.time() - t1:.0f}s", flush=True)
    # ---------------- 判準（組合版）
    checks = {}
    for ex in EXITS:
        checks[ex] = {}
        for des in ("i", "ii"):
            sk = "i" if des == "i" else "ii_median"
            s = summary["groups"]["combo"][ex][sk]
            base = summary["groups"]["base"][ex][sk]
            cw = {k: s["windows"][WKEY[k]] for k, _, _ in cm.CRASH}
            bw = {k: idx_win[WKEY[k]] for k, _, _ in cm.CRASH}
            enough = s["held_ok"] if des == "i" else s["fill_ok"]
            c = rk.judge(s, bm, base, cw, bw, enough)
            c["values"].update(avg_held=s["avg_held"], fill_rate=s.get("fill_rate"), base_calmar=base["calmar"],
                               base_cagr=base["cagr"])
            checks[ex][des] = c
        checks[ex]["established"] = bool(checks[ex]["i"]["all_pass"] and checks[ex]["ii"]["all_pass"])
        checks[ex]["established_alt_inclusive"] = bool(checks[ex]["i"]["alt_inclusive"]["all_pass"]
                                                       and checks[ex]["ii"]["alt_inclusive"]["all_pass"])
    print(json.dumps({ex: {d: {k: v for k, v in checks[ex][d].items() if k[:1] in "12345" or k == "all_pass"}
                           for d in ("i", "ii")} for ex in EXITS}, ensure_ascii=False), flush=True)
    # ---------------- 基準線重現核對
    t1 = time.time()
    prev = json.loads((PREV / "summary.json").read_text())
    prev_nav = pd.read_csv(PREV / "nav_daily.csv", parse_dates=["date"])
    prev_seed = pd.read_csv(PREV / "seed_metrics.csv")
    repro = dict(note="基準線＝第一份主規則（L1 且 L2，無手段）。設計 (i) 無亂數，應逐位相同；設計 (ii) 用第一份種子 "
                      "default_rng([20261103, 種子]) 重跑應一致，正式結果用新種子 default_rng([20261103, 4, 種子])。")
    keys_i = ["cagr", "mdd", "calmar", "pre_cagr", "post_cagr", "total", "avg_held", "avg_expo", "turnover",
              "n_trades", "win_rate", "med_ret", "avg_hold_days", "q20", "q40", "q60", "q80"]
    keys_ii = ["cagr", "mdd", "calmar", "pre_cagr", "post_cagr", "avg_held", "avg_expo", "turnover", "n_trades", "win_rate",
               "med_ret", "avg_hold_days"]
    for ex in EXITS:
        now_i = summary["groups"]["base"][ex]["i"]
        pi = prev["groups"]["main"][ex]["i"]
        e = dict(design_i_equal={k: bool(now_i[k] == pi[k]) for k in keys_i},
                 design_i_max_abs_diff=max(abs(now_i[k] - pi[k]) for k in keys_i))
        assert np.array_equal(prev_nav["date"].values, run_dates.values)
        e["design_i_nav_csv_max_abs_diff"] = float(np.max(np.abs(prev_nav[f"main_i_{ex}"].values - nav_cols[f"base_i_{ex}"])))
        ro = rk.run(m, L, L.main, "base", ex, "ii", inp, key=None)
        mo = cm.path_metrics(run_dates, ro["nav"])
        dfo = pd.DataFrame({k: np.asarray(v) for k, v in mo.items() if k != "years"})
        dfo["avg_held"], dfo["avg_expo"], dfo["turnover"] = ro["avg_held"], ro["avg_expo"], ro["turnover"]
        dfo = pd.concat([dfo, rs.trade_stats(ro["trades"], m.dates, cm.N_SEEDS)], axis=1)
        old_med = {k: float(dfo[k].median()) for k in keys_ii}
        pii = prev["groups"]["main"][ex]["ii_median"]
        e["design_ii_old_seeds_equal"] = {k: bool(old_med[k] == pii[k]) for k in keys_ii}
        e["design_ii_old_seeds_max_abs_diff"] = max(abs(old_med[k] - pii[k]) for k in keys_ii)
        ps = prev_seed[(prev_seed["group"] == "main") & (prev_seed["exit"] == ex)].sort_values("seed")
        e["design_ii_old_seeds_per_seed_cagr_max_abs_diff_vs_csv"] = float(np.max(np.abs(ps["cagr"].values - dfo["cagr"].values)))
        e["design_ii_old_seeds_median"] = {k: old_med[k] for k in ("cagr", "mdd", "calmar", "avg_held")}
        e["design_ii_new_seeds_median"] = {k: summary["groups"]["base"][ex]["ii_median"][k] for k in ("cagr", "mdd", "calmar", "avg_held")}
        repro[ex] = e
        print("重現核對", ex, e["design_i_max_abs_diff"], e["design_i_nav_csv_max_abs_diff"], e["design_ii_old_seeds_max_abs_diff"],
              e["design_ii_old_seeds_per_seed_cagr_max_abs_diff_vs_csv"], flush=True)
        del ro
    repro["all_design_i_bit_identical"] = bool(all(all(repro[ex]["design_i_equal"].values()) for ex in EXITS))
    repro["all_design_ii_old_seeds_identical"] = bool(all(all(repro[ex]["design_ii_old_seeds_equal"].values()) for ex in EXITS))
    print("重現核對完成", f"{time.time() - t1:.0f}s", flush=True)
    # ---------------- 手段觸發統計
    mainc = L.main
    trig = {}
    gm = np.where(gate)[0]
    runs, w = [], 0
    while w < W:                                                 # 連續閘門月：[起, 迄, 月數]
        if gate[w]:
            s0 = w
            while w + 1 < W and gate[w + 1]:
                w += 1
            runs.append([str(dd[s0].date())[:7], str(dd[w].date())[:7], int(w - s0 + 1)])
        w += 1
    assert sum(r[2] for r in runs) == int(gate.sum())
    trig["r1"] = dict(gate_months=int(gate.sum()), decisions=W, gate_share=float(gate.mean()), gate_runs=runs,
                      gate_months_with_main=int((mainc[gate].sum(1) > 0).sum()),
                      main_stock_months_in_gate=int(mainc[gate].sum()), main_stock_months_total=int(mainc.sum()),
                      gate_months_by_year={int(y): int(v) for y, v in pd.Series(gate, index=dd.year).groupby(level=0).sum().items()})
    miss_codes = float((ind < 0).mean())
    miss_main = float((mainc & (ind[None, :] < 0)).sum() / mainc.sum())
    pre_mask = (dd <= cm.PRE_END)[:, None]
    trig["r2_industry_map"] = dict(
        n_codes=N, codes_missing_share=miss_codes, main_stock_months_missing_share=miss_main,
        main_stock_months_missing_share_pre=float((mainc & pre_mask & (ind[None, :] < 0)).sum() / (mainc & pre_mask).sum()),
        main_stock_months_missing_share_post=float((mainc & ~pre_mask & (ind[None, :] < 0)).sum() / (mainc & ~pre_mask).sum()),
        delisted_codes_missing_share=float((ind[m.last < len(m.dates) - 1] < 0).mean()),
        n_industries=len(inp["ind_names"]))
    trig["r3_candidate_level"] = dict(main_stock_months_hot=int((mainc & inp["r3"]).sum()),
                                      share=float((mainc & inp["r3"]).sum() / mainc.sum()))
    trig["by_run"] = {}
    for cfg in rk.CONFIGS:
        for ex in EXITS:
            gi = summary["groups"][cfg][ex]["i"]["triggers"]
            gii = summary["groups"][cfg][ex]["ii_median"]
            trig["by_run"][f"{cfg}_{ex}"] = dict(
                i=gi, ii_median={k: gii[k] for k in ("n_avail", "n_buys", "n_half", "half_share", "r2_blocked", "n_r4_exits", "n_r4_only_exits",
                                                     "r4_exit_mean_ret", "n_orig_exits")})
    summary["triggers"] = trig
    # ---------------- 敏感度：R1 另一讀法（閘門月設計 (i) 不再平衡、賣出留現金）
    t1 = time.time()
    sens = dict(note="R1 另一讀法：閘門月設計 (i) 既不買新股、也不把在席股票拉回等權，賣出的錢留現金。"
                     "設計 (ii) 原本就不再平衡，兩種讀法相同。只報，不改判定。", runs={})
    for cfg in ("combo", "r1"):
        cand = rk.cand_for(cfg, L.main, gate)
        for ex in EXITS:
            r = rk.run(m, L, cand, cfg, ex, "i", inp, freeze=gate)
            mt = _scalar(cm.path_metrics(run_dates, r["nav"]))
            mt.update(avg_held=float(r["avg_held"][0]), avg_expo=float(r["avg_expo"][0]),
                      held_ok=rs.held_ok_from_sums(r["nheld_sum"], r["ndays"]))
            mt["windows"] = {k: float(v[0]) for k, v in windows_of(run_dates, r["nav"]).items()}
            if cfg == "combo":
                cw = {k: mt["windows"][WKEY[k]] for k, _, _ in cm.CRASH}
                bw = {k: idx_win[WKEY[k]] for k, _, _ in cm.CRASH}
                mt["checks_design_i"] = rk.judge(mt, bm, summary["groups"]["base"][ex]["i"], cw, bw, mt["held_ok"])
            sens["runs"][f"{cfg}_i_{ex}"] = mt
    print("敏感度完成", f"{time.time() - t1:.0f}s", flush=True)
    # ---------------- 驗證
    t1 = time.time()
    ver = {}
    # R1：浮點均線重算
    tr_idx = rk.load_index()
    ma_f = tr_idx.rolling(rk.R1_MA).mean()
    q = (tr_idx / ma_f).reindex(dd).values
    f_gate = q < 1.0
    near = np.abs(q - 1.0) < 1e-9
    ver["r1_gate"] = dict(diff_far=int(((f_gate != gate) & ~near).sum()), diff_near=int(((f_gate != gate) & near).sum()),
                          near=int(near.sum()), min_abs_gap_bps=float(np.min(np.abs(q - 1.0)) * 1e4))
    # R3／R4：pandas rolling／shift 浮點重算（整數 bps 四捨五入，所以離門檻 0.5 bp 以內的格子允許不同）
    Cdf = pd.DataFrame(m.C, index=m.dates)
    hi = Cdf.rolling(cm.HI_WIN, min_periods=1).max().values[L.dec]
    lag = Cdf.shift(cm.RET_LAG).values[L.dec]
    c = m.C[L.dec]
    with np.errstate(invalid="ignore", divide="ignore"):
        q4, q3 = c / hi, c / lag
    f4 = np.isfinite(q4) & (q4 < 0.8)
    f3 = np.isfinite(q3) & (q3 - 1 > 1.5)
    n4 = np.abs(np.nan_to_num(q4, nan=9.0) - 0.8) < 0.5e-4
    n3 = np.abs(np.nan_to_num(q3, nan=9.0) - 2.5) < 0.5e-4
    ver["r4_far_from_high"] = dict(diff_far=int(((f4 != inp["r4"]) & ~n4 & L.univ).sum()),
                                   diff_near=int(((f4 != inp["r4"]) & n4 & L.univ).sum()), near=int((n4 & L.univ).sum()))
    ver["r3_hot"] = dict(diff_far=int(((f3 != inp["r3"]) & ~n3 & L.univ).sum()),
                         diff_near=int(((f3 != inp["r3"]) & n3 & L.univ).sum()), near=int((n3 & L.univ).sum()))
    # R2：由逐筆成交重建持股，每月每產業 ≤ 2
    ver["r2_rebuilt_holdings"] = {f"{cfg}_i_{ex}": held_by_industry_ok(m, L, keep_i[(cfg, ex)]["trades"], ind, rk.IND_CAP)
                                  for cfg in ("r2", "combo") for ex in EXITS}
    ver["r2_rebuilt_holdings_base_reference"] = {f"base_i_{ex}": held_by_industry_ok(m, L, keep_i[("base", ex)]["trades"], ind, rk.IND_CAP)
                                                 for ex in EXITS}
    # 引擎對逐檔迴圈版
    eng = {}
    for cfg in ("combo", "r2", "r3", "r4"):
        cand = rk.cand_for(cfg, L.main, gate)
        kw = rk.sim_kwargs(cfg, inp)
        for ex in EXITS:
            a = vf.nav_loop(m, L.dec, cand, "i", ex, L.below200, extra_exit=kw["extra_exit"], half=kw["half"], ind=kw["ind"],
                            ind_cap=rk.IND_CAP, order_i=inp["ret126_bps"] if kw["ind"] is not None else None)
            eng[f"{cfg}_i_{ex}"] = float(np.max(np.abs(a / keep_i[(cfg, ex)]["nav"][0] - 1)))
            if cfg == "combo":
                worst = 0.0
                for s in range(1, 6):
                    keys = np.random.default_rng([*rk.SEED_KEY_II, s]).random((W, N))
                    b = vf.nav_loop(m, L.dec, cand, "ii", ex, L.below200, order_keys=keys, extra_exit=kw["extra_exit"],
                                    half=kw["half"], ind=kw["ind"], ind_cap=rk.IND_CAP)
                    worst = max(worst, float(np.max(np.abs(b / keep_nav[(cfg, ex)][s - 1] - 1))))
                eng[f"{cfg}_ii_{ex}_seeds1to5"] = worst
            print("迴圈版", cfg, ex, eng, f"{time.time() - t1:.0f}s", flush=True)
    ver["engine_max_rel_err"] = eng
    summary["verify"] = ver
    print("驗證：", json.dumps(ver, ensure_ascii=False), f"{time.time() - t1:.0f}s", flush=True)
    # ---------------- 每月檔數與名單
    cnt = pd.DataFrame(dict(decision=dd.date, index_close=inp["gate_info"]["close"], index_ma200=inp["gate_info"]["ma"],
                            index_gap_bps=inp["gate_info"]["gap_bps"], gate=gate, n_univ=L.univ.sum(1), n_main=mainc.sum(1),
                            n_main_missing_industry=(mainc & (ind[None, :] < 0)).sum(1), n_main_hot=(mainc & inp["r3"]).sum(1),
                            n_univ_far_from_high=(L.univ & inp["r4"]).sum(1)))
    for cfg in ("base", "combo", "r2"):
        for ex in EXITS:
            nh = keep_i[(cfg, ex)]["nheld_daily"][0]
            cnt[f"held_{cfg}_i_{ex}"] = [int(nh[int(d) + 1 - t0]) for d in L.dec]
    blocked = {}
    for (cfg, ex), lg in blk_logs.items():
        cols = np.where(rk.cand_for(cfg, L.main, gate).any(0))[0]
        z = np.zeros((W, N), dtype=bool)
        for w, js in lg:
            z[w, cols[js]] = True
        blocked[(cfg, ex)] = z
        cnt[f"r2_blocked_{cfg}_i_{ex}"] = z.sum(1)
    cnt.to_csv(rk.OUT / "monthly_counts.csv", index=False)
    lst = []
    for w in range(W):
        for j in np.where(mainc[w])[0]:
            row = dict(decision=dd[w].date(), code=m.codes[j], name=names.get(m.codes[j], ""),
                       industry=inp["ind_names"][ind[j]] if ind[j] >= 0 else "", gate=bool(gate[w]),
                       ret_126d_bps=int(inp["ret126_bps"][w, j]), pct_of_250d_high_bps=int(inp["hi250_bps"][w, j]),
                       r3_hot=bool(inp["r3"][w, j]))
            for (cfg, ex), z in blocked.items():
                row[f"r2_blocked_{cfg}_i_{ex}"] = bool(z[w, j])
            lst.append(row)
    pd.DataFrame(lst).to_csv(rk.OUT / "monthly_lists.csv", index=False)
    # ---------------- 寫檔
    pd.DataFrame(nav_cols).to_csv(rk.OUT / "nav_daily.csv", index=False, float_format="%.8f")
    pd.concat(seed_rows).to_csv(rk.OUT / "seed_metrics.csv", index=False, float_format="%.8f")
    pd.concat(trade_frames).to_csv(rk.OUT / "trades_design_i.csv", index=False, float_format="%.6f")
    pd.DataFrame(yearly).to_csv(rk.OUT / "yearly_returns.csv", float_format="%.6f")
    pd.DataFrame(crash).to_csv(rk.OUT / "crash_windows_mdd.csv", float_format="%.6f")
    (rk.OUT / "reproduction.json").write_text(json.dumps(repro, ensure_ascii=False, indent=1, default=str))
    (rk.OUT / "sensitivity.json").write_text(json.dumps(sens, ensure_ascii=False, indent=1, default=str))
    summary["runtime_sec"] = round(time.time() - t_all, 1)
    (rk.OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1, default=str))
    (rk.OUT / "checks.json").write_text(json.dumps(checks, ensure_ascii=False, indent=1, default=str))
    print(f"完成 {time.time() - t_all:.0f}s")


if __name__ == "__main__":
    main()
