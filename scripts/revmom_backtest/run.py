"""Run every case in docs/RevMom_Backtest_Spec.md -> results/revmom/.

python3 -m src.revmom_backtest.run            # backtests + results.json
python3 -m src.revmom_backtest.run --log      # also append the trials to experiments/ledger.jsonl (once)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import data as D
from . import engine as E
from . import signals as S

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "revmom"
START, SIG0 = "2008-01-01", "2007-12-01"
PERIODS = {"oos_2008_2014": ("2008-01-01", "2014-12-31"), "is_2015_2025": ("2015-01-01", "2025-12-31"),
           "post_finlab": ("2026-01-12", None)}
COSTS = {"base": E.Cost(), "slip0": E.Cost(slip=0.0), "slip30": E.Cost(slip=0.003),
         "fullfee_slip30": E.Cost(fee=0.001425, slip=0.003), "zero": E.Cost(fee=0.0, tax=0.0, slip=0.0)}
# stress events: the deepest 0050 peak-to-trough drawdown inside each search window (dates found from the data)
STRESS = {"2008 金融海嘯": ("2008-01-01", "2008-12-31"), "2011 歐債": ("2011-01-01", "2011-12-31"),
          "2015 股災": ("2015-01-01", "2015-12-31"), "2018 第四季": ("2018-09-01", "2018-12-31"),
          "2020 疫情": ("2020-01-01", "2020-06-30"), "2022 空頭": ("2022-01-01", "2022-12-31"),
          "2025 關稅": ("2025-01-01", "2025-06-30")}


def dd_window(nav, a, b):
    s = nav[(nav.index >= pd.Timestamp(a)) & (nav.index <= pd.Timestamp(b))]
    dd = s / s.cummax() - 1
    trough = dd.idxmin()
    peak = s.loc[:trough].idxmax()
    return peak, trough
CASH_RATE = 0.01          # only for the excess returns logged to the experiment ledger


def stats(nav: pd.Series) -> dict:
    r = nav.pct_change().dropna()
    yrs = (nav.index[-1] - nav.index[0]).days / 365.25
    cagr = (nav.iloc[-1] / nav.iloc[0]) ** (1 / yrs) - 1
    dd = nav / nav.cummax() - 1
    m = nav.resample("ME").last().pct_change().dropna()
    dn = r[r < 0]
    return {"cagr": float(cagr), "mdd": float(dd.min()), "mdd_trough": str(dd.idxmin().date()),
            "vol": float(r.std() * np.sqrt(252)), "sharpe": float(r.mean() / r.std() * np.sqrt(252)),
            "sortino": float(r.mean() / dn.std() * np.sqrt(252)) if len(dn) > 1 else None,
            "calmar": float(cagr / abs(dd.min())) if dd.min() < 0 else None,
            "month_win": float((m > 0).mean()), "best_month": float(m.max()), "worst_month": float(m.min()),
            "worst_month_at": str(m.idxmin().date())[:7]}


def slice_nav(nav, a, b=None):
    s = nav[(nav.index >= pd.Timestamp(a)) & (nav.index <= (pd.Timestamp(b) if b else nav.index[-1]))]
    prev = nav[nav.index < pd.Timestamp(a)]
    base = prev.iloc[-1] if len(prev) else s.iloc[0]
    return pd.concat([pd.Series([base], index=[s.index[0] - pd.Timedelta(days=1)]), s])


def yearly(nav):
    y = nav.resample("YE").last()
    out = y.pct_change()
    out.iloc[0] = y.iloc[0] / nav.iloc[0] - 1
    return {str(k.year): float(v) for k, v in out.items()}


def summarize(daily, tr=None, windows=None):
    nav = daily.nav
    out = {"full": stats(nav), "yearly": yearly(nav),
           "periods": {k: stats(slice_nav(nav, a, b)) for k, (a, b) in PERIODS.items()},
           "stress": {k: float(nav.asof(t) / nav.asof(p) - 1)
                      for k, (p, t) in (windows or {}).items()},
           "avg_exposure": float(daily.exposure.mean()), "avg_names": float(daily.n_hold.mean())}
    if tr is not None and len(tr):
        yrs = (nav.index[-1] - nav.index[0]).days / 365.25
        out["turnover_ann"] = float(tr.weight.abs().sum() / yrs)     # buys + sells, fraction of NAV per year
    return out


def ledger_metrics(nav, a, b=None):
    from src.experiment_ledger import metrics_from_returns
    r = slice_nav(nav, a, b).pct_change().dropna() - CASH_RATE / 252
    return metrics_from_returns(r.tolist(), 252)


def main(log=False, log_innov=False):
    OUT.mkdir(parents=True, exist_ok=True)
    pn = D.load("2007-01-01")
    pre = S.precompute(pn)
    end = pn.dates[-1]
    res = {"end": str(end.date()), "cases": {}}
    navs = {}

    b0, _ = E.run(pn, {}, START, end, COSTS["base"], single="0050")
    windows = {k: dd_window(b0.nav, a, z) for k, (a, z) in STRESS.items()}
    res["stress_windows"] = {k: [str(p.date()), str(t.date())] for k, (p, t) in windows.items()}

    def case(name, sels, cost, save=False, **kw):
        daily, tr = E.run(pn, sels, START, end, cost, **kw)
        navs[name] = daily.nav
        res["cases"][name] = summarize(daily, tr, windows)
        if save:
            daily.to_csv(OUT / f"{name}_daily.csv.gz")
            tr.to_csv(OUT / f"{name}_trades.csv.gz", index=False)
        return daily

    variants = {}
    for v in ("V1a", "V1b", "V2"):
        sels, diags = S.selections(pn, pre, SIG0, end, v)
        variants[v] = sels
        pd.DataFrame(diags).to_csv(OUT / f"selections_{v}.csv", index=False)
        case(f"{v}_base", sels, COSTS["base"], save=(v == "V1a"))
        res["cases"][f"{v}_base"]["avg_pass"] = float(np.mean([g["n_pass"] for g in diags]))
    for cn, cost in COSTS.items():
        if cn != "base":
            case(f"V1a_{cn}", variants["V1a"], cost)
    sels_inn, _ = S.selections(pn, pre, SIG0, end, "V1a", innovation=True)   # before the 2026-10-01 amendment
    case("V1a_incl_innovation", sels_inn, COSTS["base"])
    res["innovation_picks_removed"] = sum(len(set(sels_inn[d]) - set(variants["V1a"][d])) for d in variants["V1a"])
    res["innovation_removed_list"] = [[str(d.date()), c] for d in variants["V1a"]
                                      for c in sorted(set(sels_inn[d]) - set(variants["V1a"][d]))]
    sens = {"n5": dict(n_pick=5), "n20": dict(n_pick=20), "liq5m": dict(value_min=5e6), "liq30m": dict(value_min=3e7),
            "day15": dict(day=15), "notech": dict(tech=False), "day12": dict(day=12), "day13": dict(day=13)}
    for name, kw in sens.items():
        sels, _ = S.selections(pn, pre, SIG0, end, "V1a", **kw)
        case(f"sens_{name}", sels, COSTS["base"])
    late = {}
    for d in S.signal_days(pn.dates, SIG0, end):
        i = pn.dates.searchsorted(d, side="right")
        if i < len(pn.dates):
            late[pn.dates[i]] = S.select(pn, pre, pn.dates[i], "V1a")[0]
    case("sens_delay1", late, COSTS["base"])
    b = case("bench_0050", {}, COSTS["base"], save=True, single="0050")
    tx = pn.taiex_tr
    res["cases"]["bench_taiex_tr_2009"] = {"full": stats(tx), "yearly": yearly(tx)}
    ix = navs["V1a_base"]
    res["slice_2009_2014"] = {"V1a": stats(slice_nav(ix, "2009-01-05", "2014-12-31")),
                              "0050": stats(slice_nav(b.nav, "2009-01-05", "2014-12-31")),
                              "taiex_tr": stats(slice_nav(tx, "2009-01-05", "2014-12-31"))}
    m1 = ix.resample("ME").last().pct_change().dropna()
    m2 = b.nav.resample("ME").last().pct_change().dropna()
    res["corr_0050_monthly"] = float(m1.corr(m2))
    (OUT / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    if log:
        log_trials(navs)
    if log_innov:
        log_innovation_amendment(navs)
    print(json.dumps({k: {"cagr": round(v["full"]["cagr"], 4), "mdd": round(v["full"]["mdd"], 4)}
                      for k, v in res["cases"].items()}, ensure_ascii=False))


TRIALS = [  # (case, params, reason, saw_oos_before_change)
    ("V1a_base", {"rank": "rev3/rev12", "n": 10, "liq": 1e7, "day": 11, "tech": True},
     "主要版本：FinLab 公開條件＋營收比值排序（排序在看結果前選定）", False),
    ("V1b_base", {"rank": "ret60", "n": 10, "liq": 1e7, "day": 11, "tech": True}, "排序改股價 60 日報酬（事前並列）", False),
    ("V2_base", {"rank": "rev3_yoy", "n": 10, "liq": 1e7, "day": 11, "tech": False}, "學術版：只看營收年增率（事前並列）", False),
    ("sens_n5", {"rank": "rev3/rev12", "n": 5, "liq": 1e7, "day": 11, "tech": True}, "事前敏感度：持股 5 檔", False),
    ("sens_n20", {"rank": "rev3/rev12", "n": 20, "liq": 1e7, "day": 11, "tech": True}, "事前敏感度：持股 20 檔", False),
    ("sens_liq5m", {"rank": "rev3/rev12", "n": 10, "liq": 5e6, "day": 11, "tech": True}, "事前敏感度：流動性 500 萬", False),
    ("sens_liq30m", {"rank": "rev3/rev12", "n": 10, "liq": 3e7, "day": 11, "tech": True}, "事前敏感度：流動性 3,000 萬", False),
    ("sens_day15", {"rank": "rev3/rev12", "n": 10, "liq": 1e7, "day": 15, "tech": True}, "事前敏感度：訊號日 >=15 日", False),
    ("sens_notech", {"rank": "rev3/rev12", "n": 10, "liq": 1e7, "day": 11, "tech": False}, "事前敏感度：拿掉價格條件", False),
    ("sens_delay1", {"rank": "rev3/rev12", "n": 10, "liq": 1e7, "day": "11+1td", "tech": True},
     "事後檢查：看到 15 日版本變差後，確認晚 1 個交易日的影響", True),
    ("sens_day12", {"rank": "rev3/rev12", "n": 10, "liq": 1e7, "day": 12, "tech": True}, "事後檢查：訊號日 >=12 日", True),
    ("sens_day13", {"rank": "rev3/rev12", "n": 10, "liq": 1e7, "day": 13, "tech": True}, "事後檢查：訊號日 >=13 日", True),
]


def log_trials(navs):
    from src import experiment_ledger as L
    L.open_family(
        "REVMOM",
        "台股月營收動能（FinLab 公開條件＋營收比值排序，前 10 檔、每月 11 日後換股）在 FinLab 沒用過的 2008～2014 年，"
        "扣成本後年化與年化÷最大回撤都高於 0050。",
        prereg_ref="docs/RevMom_Backtest_Spec.md",
        prior_untracked_trials=0,
        note="同一組 12 個設定先在研究資料夾以 500 萬整張帳戶跑過（結果已看）；網站版只改帳戶慣例，這裡記的是同一組設定，"
             "所以不另計帳本前試驗。IS＝2015-01～2025-12（FinLab 設計期間），OOS＝2008-01～2014-12。")
    for name, params, reason, saw in TRIALS:
        nav = navs[name]
        L.log_experiment("REVMOM", params, reason, "frontier", saw,
                         is_metrics=ledger_metrics(nav, "2015-01-01", "2025-12-31"),
                         oos_metrics=ledger_metrics(nav, "2008-01-01", "2014-12-31"),
                         prereg_ref="docs/RevMom_Backtest_Spec.md", note="網站版帳戶：零碎部位、滑價 10 bp、鎖漲跌停順延")


def log_innovation_amendment(navs):
    from src import experiment_ledger as L
    L.log_experiment("REVMOM", {"rank": "rev3/rev12", "n": 10, "liq": 1e7, "day": 11, "tech": True,
                                "exclude": "innovation_board"},
                     "用戶要求名單要買得到：母體排除創新板（依當日名稱是否以「-創」結尾判斷）", "human", True,
                     is_metrics=ledger_metrics(navs["V1a_base"], "2015-01-01", "2025-12-31"),
                     oos_metrics=ledger_metrics(navs["V1a_base"], "2008-01-01", "2014-12-31"),
                     changed="universe: drop Taiwan Innovation Board", prereg_ref="docs/RevMom_Backtest_Spec.md",
                     note="看過全部結果後由用戶提出；其餘版本一併改用新母體重跑，但不另記試驗")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", action="store_true")
    ap.add_argument("--log-innov", action="store_true")
    a = ap.parse_args()
    main(a.log, a.log_innov)
