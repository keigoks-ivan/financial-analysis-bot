#!/usr/bin/env python3
"""C1 影子對照：研究期回測曲線產生器（一次性、本機跑，輸出凍結檔）。

C1 ＝ 股票部分曝險上限 cap 1.0（不借錢；其餘照現行 W52 × 自適應 σ × A2 執行層、clamp 50）
      ＋ IEF 最多 20%、GLD 最多 20%，各用週線三條件 E3（週收 > 40 週均、> 52 週均、> 52 週前，
      每成立一條 ＋1/3）；訊號 t 收盤、t+2 計報酬；超額報酬（資產 − ^IRX）、roll 8bp/年、閘門變動 1bp/邊。
定義唯一依據：v7-backtest/src/pain_reduction/（README、PREREG_pain_robustness_20261017.md、
robust_test.build_candidate("C1")），本檔不改任何邏輯與參數，只 import 後轉出週頻曲線與統計。

為什麼是一次性腳本：研究期回測是凍結的歷史（2005-01-03～2026-10-16），不該每天被 yfinance
的還原價漂移重算；每日 CI 只更新「上線後追蹤」（update_long_track_w52_adaptive_c1.py）。
此檔需要 v7-backtest 在本機（/Users/ivanchang/v7-backtest）與網路（IEF／GLD／^IRX），
CI 不跑。重跑指令：
    cd /Users/ivanchang/v7-backtest && python3 <fab>/scripts/gen_c1_backtest_series.py

輸出：docs/long-track-w52-adaptive/c1_backtest.json（週五取樣的 NAV／曝險／條件數；
統計量由日頻序列算，不用週頻近似）。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

V7 = Path("/Users/ivanchang/v7-backtest")
os.chdir(V7)
sys.path.insert(0, str(V7 / "src" / "pain_reduction"))
sys.path.insert(0, str(V7))
sys.path.insert(0, str(V7 / "src"))

import robust_test as R  # noqa: E402  (module-level 載入面板與 IEF/GLD；不寫任何 v7 檔案)

OUT = Path(__file__).resolve().parent.parent / "docs" / "long-track-w52-adaptive" / "c1_backtest.json"


def weekly(s: pd.Series, nd: int = 4) -> list:
    return [round(float(x), nd) for x in s.resample("W-FRI").last().dropna().tolist()]


def main():
    nav = {}
    held, wdef = {}, {}
    for n in ("C0", "C1"):
        nav[n], held[n], wdef[n] = R.build_candidate(n, "W-FRI")
    idx = nav["C1"].index.intersection(nav["C0"].index).intersection(R.BH.index)
    bh = R.BH.reindex(idx)
    for n in nav:
        nav[n] = nav[n].reindex(idx)
        held[n] = held[n].reindex(idx)
        wdef[n] = wdef[n].reindex(idx).fillna(0.0)

    def norm(s):
        return 100.0 * s / s.iloc[0]

    stats = {}
    for name, s in (("C1", nav["C1"]), ("C0", nav["C0"])):
        stats[name] = R.metrics(s, held[name], wdef[name])
    from pain_compare import pain  # noqa: E402
    stats["BH"] = pain(bh, None, bh)

    # 五個錨點的中位數（PREREG 判準口徑），供頁面與研究結論對照
    anchors = {}
    for a in R.ANCHORS:
        anchors[a] = {}
        for n in ("C0", "C1"):
            nv, h, wd = R.build_candidate(n, a)
            anchors[a][n] = R.metrics(nv, h, wd)
    med = {n: {k: round(float(np.median([anchors[a][n][k] for a in R.ANCHORS])), 2)
               for k in ("cagr", "mdd", "ulcer", "uw10_frac")} for n in ("C0", "C1")}

    # 壓力期與分期（W-FRI；R.window_stats 為研究程式原函式）
    stress = {lab: {n: R.window_stats(nav[n], s0, e0) for n in ("C0", "C1")}
              for lab, (s0, e0) in R.STRESS.items()}
    bh_stress = {lab: R.window_stats(bh, s0, e0) for lab, (s0, e0) in R.STRESS.items()}
    eras = {lab: {n: R.window_stats(nav[n], s0, e0) for n in ("C0", "C1")}
            for (s0, e0), lab in zip(R.ERAS, R.ERA_LAB)}

    # 週線三條件（W-FRI 錨點），0..3；IEF／GLD 各一
    cnt = {}
    for k, key in (("ief", "ief"), ("gld", "gld")):
        g = R.gate_e3_anchor(R.DEF[key], "W-FRI")
        cnt[k] = (g * 3.0).round().reindex(idx).ffill().fillna(0.0)

    wk_idx = nav["C1"].resample("W-FRI").last().dropna().index
    wk_idx = pd.DatetimeIndex([d for d in wk_idx])
    # 週頻序列取每週最後一個交易日的值（與 weekly() 相同切法）
    out = {
        "generated": str(date.today()),
        "window": [str(idx[0].date()), str(idx[-1].date())],
        "definition": "C1＝cap 1.0＋IEF／GLD 各最多 20%（週線三條件 E3，每條 1/3）；定義依 v7-backtest/src/pain_reduction",
        "source": "v7-backtest src/pain_reduction robust_test.build_candidate（W-FRI 錨點）；價格＝v7 歷史檔＋yfinance 比值接續到 2026-10-16",
        "dates": [str(d.date()) for d in nav["C1"].resample("W-FRI").last().dropna().index],
        "nav_c1": weekly(norm(nav["C1"]), 3),
        "nav_c0": weekly(norm(nav["C0"]), 3),
        "nav_bh": weekly(norm(bh), 3),
        "stock_expo_c1_pct": [round(float(x) * 100, 1) for x in weekly(held["C1"], 4)],
        "stock_expo_c0_pct": [round(float(x) * 100, 1) for x in weekly(held["C0"], 4)],
        "overlay_w_pct": [round(float(x) * 100, 1) for x in weekly(wdef["C1"], 4)],
        "ief_cond": [int(x) for x in weekly(cnt["ief"], 0)],
        "gld_cond": [int(x) for x in weekly(cnt["gld"], 0)],
        "stats_daily_wfri": stats,
        "anchor_median": med,
        "by_anchor": anchors,
        "stress": stress,
        "stress_bh": bh_stress,
        "eras": eras,
        "research_reference": {"ulcer_median_c0": 10.7, "ulcer_median_c1": 7.6,
                               "cagr_median_c0": 13.9, "cagr_median_c1": 14.8,
                               "note": "交接單／README 所列研究結論，供對照"},
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("wrote", OUT, OUT.stat().st_size, "bytes")
    print("window", out["window"])
    print("W-FRI daily stats:")
    for k, v in stats.items():
        print(" ", k, {x: v[x] for x in ("cagr", "mdd", "ulcer", "uw10_frac") if x in v})
    print("anchor median:", med)


if __name__ == "__main__":
    main()
