#!/usr/bin/env python3
"""
QQQ + SMH 長線 × 波動率目標 — 前瞻 OOS 追蹤（paper tracking）訊號頁產生器
========================================================================
每交易日抓 QQQ、SMH 日線（auto-adjust），逐標的算：
  1. 週線長軌閘門（W-FRI；進場 score5＝週收 > W52/W104/W250 且 W104/W250 四週
     斜率 > 0；出場一根週收 < W52；長多 only）→ 0/1。
  2. 波動率套袖 w = min(1, σ目標／RV20)，RV20＝20 日對數報酬年化波動。
  3. 最終目標權重 = 0.5 × 閘門 × 套袖（兩標的各自計算，合成即等權每日再平衡）。

正式追蹤版規則（2026-07-17 定案後不再調整）：σ目標 QQQ 20%、SMH 25%；成本 7 bps／邊；
t 收盤訊號、t+1 收盤生效。定位＝前瞻 OOS 追蹤，非實盤採用。

閘門定義逐位元對齊回測授權（v7-backtest
src/vol_target_backtest/run_ext_ltrack_smh.longtrack_weight 與 run_vol_target.
vt_weight）；規則若變更，兩處一起改。回測數字見 BACKTEST 常數（由
results/vol_targeting/combo_qs.json 轉錄）。

CANONICAL COPY：本檔在 v7-backtest（src/vol_target_backtest/）與
financial-analysis-bot（scripts/）兩處逐位元相同——nav 匯入以 try/except 兼容
兩 repo，輸出路徑自動解析為 <repo_root>/docs/long-track-qs-vt/。CI 由 fab 執行。

排程：每交易日美股收盤後（套袖 RV20 為日頻量，閘門為週頻，故日更）。

圖像化（Chart.js）：合成曝險量表＋每腿乘法鏈 bar（閘門×套袖→最終權重）、近三年
權重時間軸（兩腿最終權重＋合成曝險）＋ RV20 vs σ 目標、回測縮圖（對數淨值＋
回撤，BT_NAV 靜態快照）。時間軸資料存於 state.json 的 history 陣列：首次生成以
build_backfill 規則回放近 756 交易日＝約三年（source='replay'），此後 CI 逐日以 _daily_record
追加當日實錄（source='live'）；merge_history 以日期為 key 冪等（同日重跑不重複、實錄
不被回放覆蓋），上限 HISTORY_CAP。回放與實錄在圖上以虛線／實線區隔（誠實紀律，回放
不偽裝成實錄）。回放計算與每日腳本完全一致（共用 _gate_core 與同式 RV20）。
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# ---- nav import (byte-identical file across two repos) ---------------------
HERE = Path(__file__).resolve().parent
for _p in (HERE, HERE.parents[2] if len(HERE.parents) >= 3 else HERE):
    sys.path.insert(0, str(_p))
try:                                       # fab: scripts/site_nav.py
    from site_nav import full_nav_block
except ImportError:                        # v7-backtest: repo-root snippet
    from site_nav_snippet import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "ltqsvt")

# ---- output dir: <repo_root>/docs/long-track-qs-vt/ ------------------------
_cand = [HERE.parent / "docs", HERE.parents[2] / "docs" if len(HERE.parents) >= 3 else HERE / "docs"]
DOCS = next((c for c in _cand if c.exists()), _cand[0])
OUTPUT = DOCS / "long-track-qs-vt" / "index.html"
STATE_JSON = DOCS / "long-track-qs-vt" / "state.json"
ALERT_FILE = DOCS.parent / "lt_qs_vt_alert.txt"

TICKERS = ["QQQ", "SMH"]
WEIGHTS = {"QQQ": 0.5, "SMH": 0.5}
SIGMA = {"QQQ": 0.20, "SMH": 0.25}         # 規則 2026-07-17 定案，此後不再調整
FREEZE_DATE = "2026-07-17"

# 回測（results/vol_targeting/combo_qs.json，window 2005-01-03 起）— 轉錄
BACKTEST = {
    "window": "2005-01 – 2026-07",
    "rows": [                              # (label, cagr, mdd, calmar, ui, martin)
        ("正式追蹤版 σ Q20/S25（本頁追蹤）", 11.90, -21.8, 0.547, 8.21, 1.45),
        ("50/50 買進持有", 17.65, -56.9, 0.310, 13.99, 1.26),
        ("純長軌（無套袖）", 12.36, -34.0, 0.363, 9.77, 1.27),
        ("參數對照 σ Q15/S30（僅敏感度用）", 12.13, -21.3, 0.569, 7.78, 1.56),
    ],
    "grid": [                              # (qσ, sσ, calmar, cagr, mdd, martin)
        (15, 25, 0.549, 11.66, -21.3, 1.54), (15, 30, 0.569, 12.13, -21.3, 1.56),
        (15, 35, 0.582, 12.41, -21.3, 1.57), (20, 25, 0.547, 11.90, -21.8, 1.45),
        (20, 30, 0.566, 12.36, -21.8, 1.46), (20, 35, 0.552, 12.64, -22.9, 1.47),
        (25, 25, 0.542, 11.96, -22.1, 1.38), (25, 30, 0.551, 12.42, -22.5, 1.40),
        (25, 35, 0.529, 12.70, -24.0, 1.40),
    ],
    "eras": [                              # (label, ΔCAGR vs 純長軌, ΔMDD pp)
        ("2005-08 GFC", -0.1, +0.0), ("2009-13 QE", +0.8, +2.0),
        ("2014-18 低波", -1.0, +0.5), ("2019-23 COVID", +1.3, +14.5),
        ("2024- AI 牛", -7.1, +4.8),
    ],
}

# 回測月度淨值（回測快照，與 /backtest/vol_targeting/ 深度版同源、靜態轉錄；
# 用於本頁「回測縮圖」對數淨值＋回撤。深度分析請點連結過去）。
BT_NAV = {
    "labels": ["2005-01","2005-02","2005-03","2005-04","2005-05","2005-06","2005-07","2005-08","2005-09","2005-10","2005-11","2005-12","2006-01","2006-02","2006-03","2006-04","2006-05","2006-06","2006-07","2006-08","2006-09","2006-10","2006-11","2006-12","2007-01","2007-02","2007-03","2007-04","2007-05","2007-06","2007-07","2007-08","2007-09","2007-10","2007-11","2007-12","2008-01","2008-02","2008-03","2008-04","2008-05","2008-06","2008-07","2008-08","2008-09","2008-10","2008-11","2008-12","2009-01","2009-02","2009-03","2009-04","2009-05","2009-06","2009-07","2009-08","2009-09","2009-10","2009-11","2009-12","2010-01","2010-02","2010-03","2010-04","2010-05","2010-06","2010-07","2010-08","2010-09","2010-10","2010-11","2010-12","2011-01","2011-02","2011-03","2011-04","2011-05","2011-06","2011-07","2011-08","2011-09","2011-10","2011-11","2011-12","2012-01","2012-02","2012-03","2012-04","2012-05","2012-06","2012-07","2012-08","2012-09","2012-10","2012-11","2012-12","2013-01","2013-02","2013-03","2013-04","2013-05","2013-06","2013-07","2013-08","2013-09","2013-10","2013-11","2013-12","2014-01","2014-02","2014-03","2014-04","2014-05","2014-06","2014-07","2014-08","2014-09","2014-10","2014-11","2014-12","2015-01","2015-02","2015-03","2015-04","2015-05","2015-06","2015-07","2015-08","2015-09","2015-10","2015-11","2015-12","2016-01","2016-02","2016-03","2016-04","2016-05","2016-06","2016-07","2016-08","2016-09","2016-10","2016-11","2016-12","2017-01","2017-02","2017-03","2017-04","2017-05","2017-06","2017-07","2017-08","2017-09","2017-10","2017-11","2017-12","2018-01","2018-02","2018-03","2018-04","2018-05","2018-06","2018-07","2018-08","2018-09","2018-10","2018-11","2018-12","2019-01","2019-02","2019-03","2019-04","2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12","2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12","2021-01","2021-02","2021-03","2021-04","2021-05","2021-06","2021-07","2021-08","2021-09","2021-10","2021-11","2021-12","2022-01","2022-02","2022-03","2022-04","2022-05","2022-06","2022-07","2022-08","2022-09","2022-10","2022-11","2022-12","2023-01","2023-02","2023-03","2023-04","2023-05","2023-06","2023-07","2023-08","2023-09","2023-10","2023-11","2023-12","2024-01","2024-02","2024-03","2024-04","2024-05","2024-06","2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12","2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07"],
    "combo": [1.0,1.0019,1.0043,1.0066,1.009,1.0116,1.0141,1.0173,1.0202,1.0233,1.0266,1.0299,1.0238,1.0147,1.0275,1.0285,0.9949,0.999,1.0029,1.0075,1.0159,1.0485,1.0687,1.0608,1.0742,1.0675,1.0733,1.114,1.1332,1.1567,1.1517,1.1666,1.2023,1.2067,1.167,1.1656,1.1319,1.1338,1.1349,1.1362,1.1514,1.1196,1.1212,1.1097,1.1107,1.1113,1.1115,1.1115,1.1116,1.1118,1.112,1.1122,1.1123,1.1125,1.1126,1.1128,1.1129,1.113,1.113,1.113,1.1131,1.1131,1.1468,1.1599,1.1233,1.0976,1.0904,1.0637,1.0851,1.1193,1.1187,1.1452,1.1616,1.1801,1.1791,1.232,1.2112,1.1684,1.1432,1.0749,1.0614,1.0658,1.0395,1.0172,1.0519,1.0852,1.1124,1.1063,1.0671,1.0847,1.091,1.1192,1.1137,1.0841,1.079,1.0763,1.0962,1.1112,1.1346,1.1734,1.2141,1.1901,1.2415,1.216,1.2903,1.3433,1.3672,1.4192,1.3846,1.4621,1.4741,1.4552,1.5151,1.5901,1.588,1.6754,1.6596,1.6567,1.7577,1.7335,1.6856,1.8144,1.7677,1.7875,1.8772,1.771,1.7903,1.6793,1.6514,1.6873,1.7031,1.6505,1.5279,1.5283,1.5702,1.5082,1.5375,1.515,1.6265,1.6696,1.7293,1.7019,1.7403,1.7631,1.8432,1.9078,1.9685,1.9952,2.1127,2.0375,2.1285,2.1846,2.2392,2.39,2.3978,2.3927,2.6044,2.5381,2.4287,2.3735,2.549,2.5092,2.5842,2.6962,2.662,2.4594,2.4323,2.4366,2.4414,2.4555,2.5398,2.7269,2.417,2.4531,2.5545,2.4814,2.5221,2.6652,2.7763,2.941,2.9454,2.8461,2.6237,2.6603,2.7653,2.9203,3.1275,3.3712,3.2574,3.1981,3.6042,3.7693,3.8549,3.9339,3.9459,4.0031,3.9923,4.2244,4.2932,4.4471,4.2017,4.5063,4.8091,4.8552,4.4041,4.3582,4.251,4.1415,4.1447,4.1496,4.1566,4.1663,4.1769,4.1895,4.2038,4.2186,4.2337,4.2155,4.3983,4.2834,4.6502,4.8857,5.1123,5.0011,4.7061,4.559,5.1335,5.5238,5.7465,6.2822,6.4723,6.1623,6.6427,7.1324,6.9287,6.8727,6.9994,6.896,7.0955,7.127,7.1927,6.94,6.6718,6.6951,6.8585,7.3595,7.581,7.6381,8.3154,8.8922,8.6849,8.7064,9.2352,9.1369,8.6005,9.963,11.1782,11.3818,11.2104],
    "bh": [1.0,1.0414,1.01,0.9616,1.0601,1.0313,1.1272,1.113,1.1194,1.0591,1.1518,1.1302,1.1628,1.1462,1.1475,1.1674,1.0691,1.0511,1.0066,1.0717,1.0997,1.121,1.1495,1.1238,1.1388,1.1393,1.1251,1.2109,1.2318,1.2573,1.2519,1.2716,1.3118,1.2911,1.205,1.2072,1.056,1.0382,1.0512,1.1274,1.1993,1.0867,1.0584,1.0775,0.9222,0.7779,0.6561,0.6836,0.6631,0.6372,0.7134,0.7941,0.8194,0.8388,0.9423,0.9588,0.9891,0.9466,1.0016,1.076,0.9803,1.035,1.1044,1.1393,1.0665,1.0056,1.0708,0.9819,1.1165,1.1883,1.2182,1.2761,1.331,1.3786,1.3527,1.4134,1.3895,1.3404,1.3111,1.2186,1.1763,1.3061,1.2668,1.2582,1.3753,1.4394,1.5031,1.4691,1.3425,1.3921,1.3995,1.4517,1.4286,1.3784,1.4086,1.427,1.4897,1.5101,1.5418,1.5945,1.6499,1.6173,1.6871,1.6525,1.7534,1.8254,1.8579,1.9285,1.8815,1.9867,2.0031,1.9794,2.0609,2.163,2.1601,2.279,2.2575,2.2957,2.44,2.4063,2.3398,2.5187,2.4529,2.4804,2.6049,2.4574,2.4571,2.3125,2.2947,2.5257,2.5709,2.5192,2.3487,2.3471,2.5358,2.4356,2.5918,2.5649,2.8029,2.8771,2.9799,2.9327,2.999,3.0412,3.1794,3.2907,3.3955,3.4416,3.6442,3.5144,3.6714,3.7682,3.8625,4.1225,4.1359,4.1271,4.4923,4.4644,4.326,4.1876,4.5221,4.4514,4.5849,4.7836,4.723,4.232,4.3019,3.943,4.3337,4.5498,4.7059,5.0555,4.4535,4.8943,5.1055,4.9993,5.125,5.4177,5.6436,5.9784,5.9874,5.6856,5.163,5.9185,6.278,6.7384,7.2841,7.8826,7.627,7.5272,8.6707,9.1203,9.3084,9.5976,9.7388,10.0145,10.0819,10.6627,10.8364,11.2248,10.6055,11.3826,12.1386,12.3221,11.1225,10.7297,11.0155,9.4532,9.6756,8.4303,9.6542,8.9471,7.8619,8.1089,9.1435,8.281,9.4178,9.4492,10.3702,10.0788,11.3194,11.9891,12.5526,12.2899,11.5362,11.178,12.6477,13.6092,14.1612,15.5222,16.1017,15.3645,16.7829,18.0381,17.4251,17.4084,17.7183,17.5133,17.9963,18.083,18.3491,17.698,16.2215,16.3392,18.191,20.2405,20.8494,21.0066,22.8691,24.6987,24.1468,24.3765,25.973,25.7687,24.43,30.221,34.5695,36.2044,34.699],
}

BACKFILL_DAYS = 756                        # 回放窗（近三年交易日；2026-07-17 自 252 擴）
HISTORY_CAP = 820                          # state.json history 陣列上限（>756 留實錄餘裕），防肥大


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def fetch_close(ticker: str) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 13)   # 13y: W250 (~4.8y) warmup + state history
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    return c.dropna()


# ---------------------------------------------------------------------------
# Gate — verbatim port of run_ext_ltrack_smh.longtrack_weight (weekly, long-only)
# ---------------------------------------------------------------------------
def _gate_core(px: pd.Series):
    """Weekly long-track state machine. Returns (wk, pos, w52, w104, w250,
    s104, s250). Shared by gate_state (live card) and build_backfill (rule
    replay) so both compute the gate byte-identically."""
    wk = px.resample("W-FRI").last().dropna()
    w52 = wk.rolling(52).mean()
    w104 = wk.rolling(104).mean()
    w250 = wk.rolling(250).mean()
    s104 = w104 - w104.shift(4)
    s250 = w250 - w250.shift(4)
    pos, state = [], 0
    for i in range(len(wk)):
        if pd.isna(w250.iloc[i]) or pd.isna(s250.iloc[i]):
            pos.append(0)
            continue
        c = wk.iloc[i]
        if (state == 0 and c > w52.iloc[i] and c > w104.iloc[i] and c > w250.iloc[i]
                and s104.iloc[i] > 0 and s250.iloc[i] > 0):
            state = 1
        elif state == 1 and c < w52.iloc[i]:
            state = 0
        pos.append(state)
    pos = pd.Series(pos, index=wk.index, dtype=int)
    return wk, pos, w52, w104, w250, s104, s250


def gate_state(px: pd.Series) -> dict:
    wk, pos, w52, w104, w250, s104, s250 = _gate_core(px)

    recent = []
    for i in range(-8, 0):
        recent.append({
            "date": wk.index[i].strftime("%Y-%m-%d"),
            "close": float(wk.iloc[i]),
            "w52": float(w52.iloc[i]) if not pd.isna(w52.iloc[i]) else None,
            "w104": float(w104.iloc[i]) if not pd.isna(w104.iloc[i]) else None,
            "w250": float(w250.iloc[i]) if not pd.isna(w250.iloc[i]) else None,
            "s104_pos": bool(s104.iloc[i] > 0) if not pd.isna(s104.iloc[i]) else None,
            "s250_pos": bool(s250.iloc[i] > 0) if not pd.isna(s250.iloc[i]) else None,
            "in": bool(pos.iloc[i]),
        })
    return {
        "gate": bool(pos.iloc[-1]),
        "wk_date": wk.index[-1].strftime("%Y-%m-%d"),
        "wk_close": float(wk.iloc[-1]),
        "w52": float(w52.iloc[-1]), "w104": float(w104.iloc[-1]), "w250": float(w250.iloc[-1]),
        "s104_pos": bool(s104.iloc[-1] > 0), "s250_pos": bool(s250.iloc[-1] > 0),
        "recent": recent,
    }


# ---------------------------------------------------------------------------
# Sleeve — verbatim port of run_vol_target.vt_weight
# ---------------------------------------------------------------------------
def sleeve_state(px: pd.Series, sigma: float, win: int = 20) -> dict:
    lr = np.log(px / px.shift(1))
    rv = lr.rolling(win).std() * np.sqrt(252)
    rv_now = float(rv.iloc[-1])
    w = min(1.0, sigma / rv_now) if rv_now > 0 else 1.0
    return {"rv20": rv_now, "sleeve": w}


def compute_ticker(t: str, px: pd.Series) -> dict:
    g = gate_state(px)
    s = sleeve_state(px, SIGMA[t])
    fill = (1 if g["gate"] else 0) * s["sleeve"]        # 0..1 fill of the 0.5 slot
    final = WEIGHTS[t] * fill
    return {**g, **s, "sigma": SIGMA[t], "fill": fill, "final": final}


# ---------------------------------------------------------------------------
# History — rule-replay backfill (誠實紀律：回放 ≠ 實錄，欄位 source 標記區分)
# ---------------------------------------------------------------------------
def _daily_record(px_map: dict, d: pd.Timestamp, source: str) -> dict:
    """One day's target weights, computed byte-identically to the live path:
    gate = _gate_core(px[:d]).pos.iloc[-1] (含當週部分週線，與每日腳本一致)；
    sleeve = min(1, σ/RV20) on px[:d]. source ∈ {'replay','live'}."""
    rec = {"date": d.strftime("%Y-%m-%d"), "source": source, "tickers": {}}
    combined = 0.0
    for t in TICKERS:
        pxd = px_map[t].loc[:d]
        _, pos, *_ = _gate_core(pxd)
        gate = bool(pos.iloc[-1])
        lr = np.log(pxd / pxd.shift(1))
        rv_now = float((lr.rolling(20).std() * np.sqrt(252)).iloc[-1])
        sleeve = min(1.0, SIGMA[t] / rv_now) if rv_now > 0 else 1.0
        final = WEIGHTS[t] * ((1 if gate else 0) * sleeve)
        combined += final
        rec["tickers"][t] = {
            "gate": gate,
            "rv20_pct": round(rv_now * 100, 2),
            "sleeve": round(sleeve, 4),
            "final_pct": round(final * 100, 1),
        }
    rec["combined_pct"] = round(combined * 100, 1)
    return rec


def build_backfill(px_map: dict, n_days: int = BACKFILL_DAYS) -> list:
    """Replay the exact daily rule over the last n_days common trading days.
    Every record is marked source='replay' (誠實：非當日實錄)."""
    common = None
    for t in TICKERS:
        common = px_map[t].index if common is None else common.intersection(px_map[t].index)
    dates = common.sort_values()[-n_days:]
    return [_daily_record(px_map, d, "replay") for d in dates]


def merge_history(prev_history: list, backfill: list, today_rec: dict,
                  cap: int = HISTORY_CAP) -> list:
    """Idempotent, date-keyed merge. Backfill only fills dates absent from
    prior history (never overwrites a recorded 'live' point with a 'replay').
    Today's live record always wins its date. Kept sorted, capped at `cap`."""
    by_date = {r["date"]: r for r in (prev_history or [])}
    for r in backfill:
        by_date.setdefault(r["date"], r)
    by_date[today_rec["date"]] = today_rec       # live wins
    out = [by_date[k] for k in sorted(by_date)]
    return out[-cap:]


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
def fmt_pct(v, dp=2):
    return f"{'+' if v >= 0 else ''}{v:.{dp}f}%"


def fill_color(fill):
    if fill >= 0.99:
        return "green"
    if fill >= 0.66:
        return "blue"
    if fill >= 0.33:
        return "amber"
    return "red"


def ticker_card(t: str, d: dict) -> str:
    col = fill_color(d["fill"])
    gate_on = d["gate"]
    d52 = (d["wk_close"] / d["w52"] - 1) * 100
    d104 = (d["wk_close"] / d["w104"] - 1) * 100
    d250 = (d["wk_close"] / d["w250"] - 1) * 100
    near_exit = gate_on and abs(d52) < 2.0
    warn = (' <span style="color:var(--amber);font-weight:700;font-size:.72rem">'
            '⚠ 接近出場（近 W52）</span>') if near_exit else ""
    return f"""<div class="tcard">
  <div class="tcard-hdr">
    <span class="tname">{t}</span>
    <span class="pos-badge pos-{col}">最終權重 {d['final']*100:.0f}%</span>
  </div>
  <div class="tcard-sub">閘門 {'在場' if gate_on else '出場'} × 套袖 {d['sleeve']*100:.0f}%
    → 佔本標的 50% 額度的 {d['fill']*100:.0f}% · 目標權重 0.5 × {1 if gate_on else 0} × {d['sleeve']:.2f} = {d['final']*100:.0f}%{warn}</div>
  <div class="sig-row">
    <div class="sig {'on' if gate_on else 'off'}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">週線長軌閘門</span><span class="sig-mark">{'✓ 在場' if gate_on else '✕ 出場'}</span></div>
      <div class="sig-detail">週收 {d['wk_close']:.2f}｜W52 {d['w52']:.2f} <b style="color:var(--{'green' if d52>=0 else 'red'})">{fmt_pct(d52,1)}</b>
        ｜W104 {d['w104']:.2f} <b style="color:var(--{'green' if d104>=0 else 'red'})">{fmt_pct(d104,1)}</b>
        ｜W250 {d['w250']:.2f} <b style="color:var(--{'green' if d250>=0 else 'red'})">{fmt_pct(d250,1)}</b>
        ｜W104斜率 {'↑' if d['s104_pos'] else '↓'}｜W250斜率 {'↑' if d['s250_pos'] else '↓'}
        <br><span style="font-size:.72rem">進場 score5＝週收在三線上且 W104/W250 四週斜率為正；出場＝一根週收 &lt; W52。</span></div>
    </div>
    <div class="sig {'on' if d['sleeve']>=0.999 else 'off'}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">波動率套袖 σ目標 {d['sigma']*100:.0f}%</span><span class="sig-mark">{d['sleeve']*100:.0f}%</span></div>
      <div class="sig-detail">RV20（20日年化波動）<b>{d['rv20']*100:.1f}%</b> vs σ目標 {d['sigma']*100:.0f}%
        → w = min(1, {d['sigma']*100:.0f}%／{d['rv20']*100:.1f}%) = <b>{d['sleeve']:.2f}</b>
        <br><span style="font-size:.72rem">{'波動 ≤ σ目標，滿載。' if d['sleeve']>=0.999 else '波動高於 σ目標，按比例減碼（只降不加）。'}</span></div>
    </div>
  </div>
</div>"""


def recent_table(t: str, d: dict) -> str:
    rows = ""
    for r in d["recent"]:
        if r["w52"] is None:
            continue
        d52 = (r["close"] / r["w52"] - 1) * 100
        c52 = "var(--green)" if d52 >= 0 else "var(--red)"
        incell = (f'<span class="tag" style="background:var(--green-bg);color:var(--green-text)">在場</span>'
                  if r["in"] else
                  f'<span class="tag" style="background:var(--red-bg);color:var(--red-text)">出場</span>')
        rows += f"""<tr>
  <td>{r['date']}</td><td>{r['close']:.2f}</td>
  <td>{r['w52']:.2f}</td><td style="color:{c52}">{fmt_pct(d52,1)}</td>
  <td>{r['w104']:.2f}</td><td>{r['w250']:.2f}</td>
  <td>{'↑' if r['s104_pos'] else '↓'} / {'↑' if r['s250_pos'] else '↓'}</td>
  <td>{incell}</td>
</tr>\n"""
    return f"""<div class="card">
<h3>{t} — 近 8 週閘門軌跡（週線 W-FRI）</h3>
<table><thead><tr><th>週五</th><th>週收</th><th>W52</th><th>距 W52</th><th>W104</th><th>W250</th><th>W104/W250 斜率</th><th>閘門</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>"""


def backtest_section() -> str:
    rows = ""
    for lab, cagr, mdd, calmar, ui, martin in BACKTEST["rows"]:
        hl = "rowhl" if "正式追蹤" in lab else ("rowbh" if "買進持有" in lab else "")
        rows += (f'<tr class="{hl}"><td>{lab}</td><td class="num">{cagr:.2f}%</td>'
                 f'<td class="num">{mdd:.1f}%</td><td class="num">{calmar:.3f}</td>'
                 f'<td class="num">{ui:.2f}</td><td class="num">{martin:.2f}</td></tr>\n')
    grid = ""
    for qs, ss, calmar, cagr, mdd, martin in BACKTEST["grid"]:
        hl = ' class="rowhl"' if (qs == 20 and ss == 25) else ""
        grid += (f'<tr{hl}><td>Q{qs}% / S{ss}%</td><td class="num">{calmar:.3f}</td>'
                 f'<td class="num">{cagr:.2f}%</td><td class="num">{mdd:.1f}%</td>'
                 f'<td class="num">{martin:.2f}</td></tr>\n')
    eras = ""
    for lab, dc, dm in BACKTEST["eras"]:
        cc = "pos" if dc >= 0 else "neg"
        cm = "pos" if dm >= 0 else "neg"
        eras += (f'<tr><td>{lab}</td><td class="num {cc}">{dc:+.1f}pp</td>'
                 f'<td class="num {cm}">{dm:+.1f}pp</td></tr>\n')
    return f"""<div class="card">
<h3>回測摘要（正式追蹤版 vs 三基準・共同窗 {BACKTEST['window']}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
兩標的日報酬 50/50 加權合成（等效每日再平衡，如實揭露）。判準基準＝<b>純長軌組合</b>（非買進持有）。</p>
<table><thead><tr><th>配置</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Calmar</th><th class="num">Ulcer</th><th class="num">Martin</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="takeaway">套袖把純長軌的 Calmar 0.363 → <b>0.547</b>、MDD −34.0% → <b>−21.8%</b>，CAGR 只付 0.46pp；
對 50/50 買進持有則是「風險調整支配、CAGR 讓步」（B&amp;H 17.65%／−56.9%）。正式追蹤版 σ（0.547）貼近參數對照最佳（Q15/S30 0.569），
不靠選中特定 σ 才成立。<b>唯一系統性代價集中在 AI 牛（單期 CAGR −7.1pp，高波急彈仍減碼、漏接反彈）。</b></div>
</div>

<div class="card">
<h3>σ 目標敏感度對照（僅回測參考，不追蹤）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
QQQ σ × SMH σ 網格的組合 Calmar。正式追蹤版格 Q20/S25 高亮；參數對照最佳 Q15/S35（0.582）與正式追蹤版差距小，故採原則法 σ（各自長期 RV 中位取整）。此格僅敏感度用、不追蹤。</p>
<table><thead><tr><th>σ 組合</th><th class="num">Calmar</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Martin</th></tr></thead>
<tbody>{grid}</tbody></table>
</div>

<div class="card">
<h3>分期（正式追蹤版 vs 純長軌；ΔCAGR／ΔMDD，正＝套袖較優）</h3>
<table><thead><tr><th>期間</th><th class="num">Δ CAGR</th><th class="num">Δ MDD</th></tr></thead>
<tbody>{eras}</tbody></table>
<div style="font-size:.75rem;color:var(--muted);margin-top:.5rem">五期 MDD 全數改善（+0.0～+14.5pp）；CAGR 代價集中在 AI 牛（−7.1pp）。</div>
</div>"""


def generate_html(sigs: dict, changes: list | None, last_change_date: str | None,
                  history: list | None = None) -> str:
    changes = changes or []
    history = history or []
    combined = sum(sigs[t]["final"] for t in TICKERS) * 100
    ccol = fill_color(combined / 100)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards = "".join(ticker_card(t, sigs[t]) for t in TICKERS)
    tables = "".join(recent_table(t, sigs[t]) for t in TICKERS)

    # ---- timeline data (last ~3 years, replay + live) ----
    def _col(fn):
        return json.dumps([fn(r) for r in history], separators=(",", ":"))
    H_LABELS = _col(lambda r: r["date"])
    H_COMB = _col(lambda r: r["combined_pct"])
    H_QQQ = _col(lambda r: r["tickers"]["QQQ"]["final_pct"])
    H_SMH = _col(lambda r: r["tickers"]["SMH"]["final_pct"])
    H_QRV = _col(lambda r: r["tickers"]["QQQ"]["rv20_pct"])
    H_SRV = _col(lambda r: r["tickers"]["SMH"]["rv20_pct"])
    H_SRC = _col(lambda r: r["source"])
    n_replay = sum(1 for r in history if r["source"] == "replay")
    n_live = sum(1 for r in history if r["source"] == "live")
    span = (f"{history[0]['date']} → {history[-1]['date']}" if history else "—")

    # ---- current multiplication chain (per leg, out of the 50% slot) ----
    slot = {t: WEIGHTS[t] * 100 for t in TICKERS}
    finals = [round(sigs[t]["final"] * 100, 1) for t in TICKERS]
    gate_cut = [round(slot[t] if not sigs[t]["gate"] else 0.0, 1) for t in TICKERS]
    sleeve_cut = [round(slot[t] - finals[i] - gate_cut[i], 1) for i, t in enumerate(TICKERS)]
    C_FINALS = json.dumps(finals, separators=(",", ":"))
    C_SLEEVE = json.dumps(sleeve_cut, separators=(",", ":"))
    C_GATE = json.dumps(gate_cut, separators=(",", ":"))
    SIG_Q = SIGMA["QQQ"] * 100
    SIG_S = SIGMA["SMH"] * 100
    CCOL_HEX = {"green": "#16a34a", "blue": "#1d4ed8",
                "amber": "#a16207", "red": "#b91c1c"}[ccol]

    # ---- backtest thumbnail (static snapshot) ----
    BT_L = json.dumps(BT_NAV["labels"], separators=(",", ":"))
    BT_C = json.dumps(BT_NAV["combo"], separators=(",", ":"))
    BT_B = json.dumps(BT_NAV["bh"], separators=(",", ":"))

    change_html = (
        ('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;'
         'padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">'
         '可行動變化</b><br>' + "<br>".join(changes) +
         '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>')
        if changes else
        ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">'
         '無可行動變化（閘門未翻轉、且無標的最終權重變動 ≥ 10pp）' +
         (f'（上次變化：{last_change_date}）' if last_change_date else '') + '</div>'))

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>QQQ + SMH 長線 × 波動率目標｜前瞻 OOS 追蹤 | InvestMQuest Research</title>
  <meta name="description" content="QQQ 50% + SMH 50% · 週線長軌閘門 × 波動率目標套袖 · 前瞻 OOS 紙上追蹤（未採用）">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
  <style>
:root{{--brand:#0d2244;--bg:#f7f3ea;--card:#ffffff;--text:#0c1521;--muted:#9aa7b8;--border:#e5dfd0;
  --green:#15803d;--green-bg:#eafaef;--green-border:var(--line);--green-text:#15803d;
  --red:#b91c1c;--red-bg:#fbeceb;--red-border:var(--line);--red-text:#b91c1c;
  --amber:#a16207;--amber-bg:#fbf3df;--amber-border:var(--line);--amber-text:#a16207;
  --blue:#1d4ed8;--blue-bg:#e8eef5;--blue-border:var(--line);--blue-text:#1d4ed8}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.65;font-size:14px}}
a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:1140px;margin:0 auto;padding:0 1.5rem}}
.page-hdr{{padding:1.5rem 0 1.2rem;background:var(--card);border-bottom:1px solid var(--border)}}
.page-hdr h1{{font-family:var(--serif);font-size:1.5rem;font-weight:700;letter-spacing:-.01em}}
.page-hdr .sub{{color:var(--muted);font-size:.85rem;margin-top:.2rem}}
.crumb{{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}}
.crumb a{{color:var(--muted)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;margin-bottom:1rem;box-shadow:var(--sh-1)}}
.card h3{{font-size:.95rem;font-weight:600;margin-bottom:.75rem}}
.card .takeaway{{font-size:.82rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:8px;background:#f6f8fb;border-left:3px solid var(--brand)}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th,td{{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}}
th{{background:transparent;font-family:var(--mono);font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}
td{{font-variant-numeric:tabular-nums}}
td.num,th.num{{text-align:right}}
.pos{{color:var(--green);font-weight:600}}.neg{{color:var(--red);font-weight:600}}
.rowhl td{{background:#eef3fb!important}}.rowbh td{{background:#faf7f0;color:var(--muted)}}
tbody tr:hover td{{background:#fbf8f1}}
.tag{{display:inline-block;padding:.12rem .5rem;border-radius:6px;font-size:.7rem;font-weight:600}}
footer{{background:var(--card);border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1rem 0;font-size:.75rem;margin-top:1rem}}
.status-hero{{padding:2rem 0 1rem;text-align:center}}
.status-badge{{display:inline-flex;align-items:center;gap:.75rem;padding:1rem 2.5rem;border-radius:var(--r);font-size:1.4rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.5rem}}
.status-badge .dot{{width:14px;height:14px;border-radius:50%;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.status-exposure{{font-size:2.6rem;font-weight:800;margin:.3rem 0}}
.status-date{{font-size:.8rem;color:var(--muted)}}
.hero-green .status-badge{{background:var(--green-bg);color:var(--green-text);border:2px solid var(--green-border)}}
.hero-green .dot{{background:var(--green)}}.hero-green .status-exposure{{color:var(--green)}}
.hero-blue .status-badge{{background:var(--blue-bg);color:var(--blue-text);border:2px solid var(--blue-border)}}
.hero-blue .dot{{background:var(--blue)}}.hero-blue .status-exposure{{color:var(--blue)}}
.hero-amber .status-badge{{background:var(--amber-bg);color:var(--amber-text);border:2px solid var(--amber-border)}}
.hero-amber .dot{{background:var(--amber)}}.hero-amber .status-exposure{{color:var(--amber)}}
.hero-red .status-badge{{background:var(--red-bg);color:var(--red-text);border:2px solid var(--red-border)}}
.hero-red .dot{{background:var(--red)}}.hero-red .status-exposure{{color:var(--red)}}
.tgrid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}}
.tcard{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem;box-shadow:var(--sh-1)}}
.tcard-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.2rem}}
.tname{{font-size:1.3rem;font-weight:800;letter-spacing:-.02em}}
.pos-badge{{font-size:.95rem;font-weight:700;padding:.25rem .7rem;border-radius:6px}}
.pos-green{{background:var(--green-bg);color:var(--green-text)}}.pos-blue{{background:var(--blue-bg);color:var(--blue-text)}}
.pos-amber{{background:var(--amber-bg);color:var(--amber-text)}}.pos-red{{background:var(--red-bg);color:var(--red-text)}}
.tcard-sub{{font-size:.75rem;color:var(--muted);margin-bottom:.75rem}}
.sig-row{{display:grid;grid-template-columns:1fr;gap:.5rem}}
.sig{{border:1px solid var(--border);border-radius:var(--r);padding:.55rem .7rem;background:var(--card)}}
.sig.on{{border-color:var(--green-border);background:var(--green-bg)}}
.sig.off{{border-color:var(--red-border);background:var(--red-bg)}}
.sig-top{{display:flex;align-items:center;gap:.5rem}}
.sig-dot{{width:11px;height:11px;border-radius:50%}}
.sig.on .sig-dot{{background:var(--green)}}.sig.off .sig-dot{{background:var(--red)}}
.sig-name{{font-weight:700;font-size:.85rem}}
.sig-mark{{margin-left:auto;font-weight:800}}
.sig.on .sig-mark{{color:var(--green)}}.sig.off .sig-mark{{color:var(--red)}}
.sig-detail{{font-size:.74rem;color:var(--muted);margin-top:.2rem;font-variant-numeric:tabular-nums}}
.oos-banner{{background:linear-gradient(135deg,#fdf6e3 0%,#faf0d7 100%);border:2px solid var(--amber);border-radius:12px;padding:1rem 1.3rem;margin:1rem 0}}
.oos-banner .tag-loud{{display:inline-block;background:var(--amber);color:#fff;font-size:.72rem;font-weight:800;letter-spacing:.06em;padding:.22rem .7rem;border-radius:99px;margin-bottom:.45rem}}
.oos-banner b{{color:var(--amber-text)}}
.rule-list{{font-size:.82rem;line-height:1.9}}.rule-list b{{color:var(--text)}}
.chart-wrap{{position:relative;width:100%;height:400px}}
.chart-wrap-sm{{position:relative;width:100%;height:300px}}
.chart-wrap-xs{{position:relative;width:100%;height:210px}}
.viz-split{{display:grid;grid-template-columns:260px 1fr;gap:1.25rem;align-items:center}}
.gauge-box{{position:relative;width:100%;max-width:240px;margin:0 auto;height:150px}}
.gauge-center{{position:absolute;left:0;right:0;bottom:6px;text-align:center}}
.gauge-center .g-num{{font-size:2.1rem;font-weight:800;line-height:1;letter-spacing:-.02em}}
.gauge-center .g-lab{{font-size:.7rem;color:var(--muted);margin-top:.15rem}}
.legend-note{{font-size:.74rem;color:var(--muted);margin-top:.6rem;display:flex;gap:1.2rem;flex-wrap:wrap;align-items:center}}
.legend-note .ln-item{{display:inline-flex;align-items:center;gap:.35rem}}
.legend-note .ln-line{{display:inline-block;width:22px;height:0;border-top:2.4px solid var(--muted)}}
.legend-note .ln-dash{{border-top-style:dashed}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
@media(max-width:768px){{.tgrid{{grid-template-columns:1fr}}.status-exposure{{font-size:2rem}}table{{font-size:.74rem}}th,td{{padding:.4rem .45rem}}
  .viz-split{{grid-template-columns:1fr}}.grid2{{grid-template-columns:1fr}}.chart-wrap{{height:320px}}}}
</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / QQQ + SMH 長線 × 波動率目標</div>
    <h1>QQQ + SMH 長線 × 波動率目標 — 前瞻 OOS 追蹤</h1>
    <div class="sub">50% QQQ + 50% SMH · 週線長軌閘門 × 波動率目標套袖（σ QQQ 20%／SMH 25%）· Long only · 紙上追蹤（未採用）</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem;flex-wrap:wrap">
      <a href="/long-track-qs-vt/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">QQQ+SMH 波動率</a>
      <a href="/long-track-smh/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">SMH/QQQ STX50（實倉）</a>
      <a href="/backtest/vol_targeting/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">波動率目標回測</a>
    </div>
  </div>
</div>
<div class="container">

<div class="oos-banner">
  <span class="tag-loud">前瞻 OOS 追蹤中・未採用（PAPER TRACKING）</span>
  <div style="font-size:.86rem">這<b>不是實盤系統</b>，是把一組<b>{FREEZE_DATE} 定案的正式規則</b>往前逐日記錄，看真實 OOS 表現是否與回測分布一致的紙上追蹤頁。
  規則定案後不再調整、不再調參（前瞻樣本外驗證的前提）。<b>複審條件：2027-01 或滿 120 個追蹤交易日</b>後，比對 OOS 與回測分布。
  實倉的長線攻擊位請見 <a href="/long-track-smh/">SMH/QQQ STX50 頁</a>；本頁的回測邏輯見 <a href="/backtest/vol_targeting/">波動率目標回測</a>。</div>
</div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>組合當前目標曝險</span></div>
  <div class="status-exposure">{combined:.0f}%</div>
  <div style="font-size:.8rem;color:var(--muted)">0.5 × 閘門 × 套袖，兩標的相加 · 閒置部分持現金</div>
  <div class="status-date">數據截至 {data_date}（週五收盤）· 頁面更新 {now}</div>
</div>

{change_html}

<div class="card">
<h3>當前部位視覺 — 合成曝險量表 × 每腿乘法鏈</h3>
<div class="viz-split">
  <div>
    <div class="gauge-box">
      <canvas id="chart-gauge"></canvas>
      <div class="gauge-center"><div class="g-num hero-{ccol}" style="color:var(--{ccol})">{combined:.0f}%</div><div class="g-lab">合成目標曝險（0～100%）</div></div>
    </div>
  </div>
  <div>
    <div class="chart-wrap-xs"><canvas id="chart-chain"></canvas></div>
  </div>
</div>
<div style="font-size:.76rem;color:var(--muted);margin-top:.7rem">每腿 50% 額度＝<b style="color:var(--text)">最終持有</b> ＋ <b style="color:var(--amber-text)">套袖折減</b>（高波減碼）＋ <b>閘門關閉</b>（出場歸零）。一眼看出「現在拿多少、被誰折了多少」：{TICKERS[0]} 最終 {finals[0]:.0f}%、{TICKERS[1]} 最終 {finals[1]:.0f}%。</div>
</div>

<div class="card">
<h3>近三年權重時間軸 — 兩腿最終權重 ＋ 合成曝險</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
逐日目標權重。<b style="color:var(--text)">實線＝每日實錄</b>（CI 逐日追加），<b>虛線＝規則回放</b>（首次生成時以完全相同的規則往回重算，非當日實錄，誠實區隔）。
窗 {span}，共 {len(history)} 個交易日（回放 {n_replay}／實錄 {n_live}）。</p>
<div class="chart-wrap"><canvas id="chart-weights"></canvas></div>
<div class="legend-note">
  <span class="ln-item"><span class="ln-line"></span>每日實錄</span>
  <span class="ln-item"><span class="ln-line ln-dash"></span>規則回放</span>
</div>
<h3 style="margin-top:1.1rem">套袖觸發脈絡 — RV20 vs σ 目標</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
當 RV20（實線）升破 σ 目標（水平虛線），套袖開始按比例減碼；RV20 ≤ σ 目標時滿載。對照上圖即可看出每次減碼的來源。</p>
<div class="chart-wrap-sm"><canvas id="chart-rv"></canvas></div>
</div>

<div class="tgrid">{cards}</div>

<div class="card">
<h3>正式追蹤版規則（{FREEZE_DATE} 定案，此後不再調整）</h3>
<div class="rule-list">
① <b>兩標的各 50%</b>，日報酬加權合成（<b>絕不直接相加 equity curve</b>；50/50 日報酬加權＝等效每日再平衡，如實揭露此假設）。<br>
② <b>週線長軌閘門</b>（W-FRI）：進場＝週收盤 &gt; W52／W104／W250 且 W104／W250 四週斜率 &gt; 0（score5）；出場＝一根週收盤 &lt; W52；<b>長多 only</b>，閘門輸出 0／1。<br>
③ <b>波動率套袖</b>：w = min(1, σ目標／RV20)，RV20＝20 日對數報酬年化波動；<b>只降不加</b>（上限 1.0）。<br>
④ <b>σ 定案（原則法）</b>：QQQ 20%、SMH 25%（各自長期 RV 中位數取整到 5%）。參數對照版 Q15/S30 只作敏感度用，<b>不追蹤</b>。<br>
⑤ <b>執行</b>：t 收盤訊號、t+1 收盤生效；成本 7 bps／邊。<br>
⑥ <b>最終權重</b> = 0.5 × 閘門(0/1) × 套袖權重，兩標的各自計算。<br>
<span style="color:var(--muted);font-size:.78rem">閘門為週頻（僅週五可能翻轉），套袖 RV20 為日頻（每日可能微調），故本頁每交易日更新。「可行動變化」＝閘門翻轉或任一標的最終權重變動 ≥ 10pp，觸發 email 通知。</span>
</div>
</div>

{tables}

<div class="card">
<h3>回測縮圖 — 正式追蹤版 vs 50/50 B&amp;H（對數淨值＋回撤）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
回測快照（{BT_NAV['labels'][0]} → {BT_NAV['labels'][-1]}，與 <a href="/backtest/vol_targeting/">波動率目標回測</a> 深度版同源、靜態轉錄）。
深度分析（純長軌對照、σ 敏感度、分期、年報酬）請點連結過去。</p>
<div class="grid2">
  <div class="chart-wrap-sm"><canvas id="chart-bt-nav"></canvas></div>
  <div class="chart-wrap-sm"><canvas id="chart-bt-dd"></canvas></div>
</div>
<div style="text-align:right;margin-top:.5rem"><a href="/backtest/vol_targeting/" style="font-size:.82rem;font-weight:600">看回測深度版 →</a></div>
</div>

{backtest_section()}

<div class="card">
<h3>複審條件</h3>
<div class="rule-list" style="font-size:.82rem">
於 <b>2027-01</b> 或滿 <b>120 個追蹤交易日</b>後，檢視前瞻 OOS 的 CAGR／MDD／Calmar 是否落在回測分布內。
若 OOS 顯著劣於回測（例如 Calmar 掉出回測分期區間、或 AI 牛型漏接反彈的代價超出回測所示），則記錄為「規則不穩健」；
若一致，才進入 charter 採用決策流程。<b>在此之前本頁純為研究追蹤，不構成任何倉位建議。</b>
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research · QQQ+SMH 長線 × 波動率目標（前瞻 OOS 追蹤・未採用）</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
<script>
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;
var GREEN="#16a34a",BLUE="#1565c0",AMBER="#d97706";

// ---- gauge: combined exposure 0..100 (semicircle) ----
new Chart(document.getElementById('chart-gauge'),{{
  type:'doughnut',
  data:{{labels:['曝險','現金'],datasets:[{{data:[{combined:.1f},{100-combined:.1f}],
    backgroundColor:['{CCOL_HEX}','#ece7db'],borderWidth:0}}]}},
  options:{{rotation:-90,circumference:180,cutout:'72%',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:function(c){{return c.label+': '+c.parsed.toFixed(1)+'%'}}}}}}}}}}
}});

// ---- multiplication chain: per leg out of the 50% slot ----
new Chart(document.getElementById('chart-chain'),{{
  type:'bar',
  data:{{labels:['{TICKERS[0]} 腿（50%）','{TICKERS[1]} 腿（50%）'],datasets:[
    {{label:'最終持有',data:{C_FINALS},backgroundColor:[GREEN,AMBER],borderWidth:0,stack:'s'}},
    {{label:'套袖折減',data:{C_SLEEVE},backgroundColor:'rgba(161,98,7,0.28)',borderWidth:0,stack:'s'}},
    {{label:'閘門關閉',data:{C_GATE},backgroundColor:'rgba(120,120,120,0.22)',borderWidth:0,stack:'s'}}
  ]}},
  options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:true,position:'bottom',labels:{{usePointStyle:true,pointStyle:'rect',padding:10,boxWidth:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.x.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{stacked:true,min:0,max:50,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}}}}}},
      y:{{stacked:true,grid:{{display:false}}}}}}
  }}
}});

// ---- 3-year weight timeline (replay=dashed, live=solid) ----
var W_LAB={H_LABELS},W_SRC={H_SRC};
function segDash(ctx){{return W_SRC[ctx.p1DataIndex]==='live'?undefined:[3,3];}}
new Chart(document.getElementById('chart-weights'),{{
  type:'line',
  data:{{labels:W_LAB,datasets:[
    {{label:'合成曝險',data:{H_COMB},borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.07)',
     borderWidth:2.4,pointRadius:0,pointHoverRadius:3,tension:0.15,fill:'origin',segment:{{borderDash:segDash}}}},
    {{label:'{TICKERS[0]} 腿',data:{H_QQQ},borderColor:BLUE,borderWidth:1.5,pointRadius:0,pointHoverRadius:3,tension:0.15,segment:{{borderDash:segDash}}}},
    {{label:'{TICKERS[1]} 腿',data:{H_SMH},borderColor:AMBER,borderWidth:1.5,pointRadius:0,pointHoverRadius:3,tension:0.15,segment:{{borderDash:segDash}}}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{title:function(c){{return c[0].label+' · '+(W_SRC[c[0].dataIndex]==='live'?'每日實錄':'規則回放')}},
        label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{min:0,max:100,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});

// ---- RV20 vs sigma target ----
new Chart(document.getElementById('chart-rv'),{{
  type:'line',
  data:{{labels:W_LAB,datasets:[
    {{label:'{TICKERS[0]} RV20',data:{H_QRV},borderColor:BLUE,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{TICKERS[1]} RV20',data:{H_SRV},borderColor:AMBER,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{TICKERS[0]} σ 目標 {SIG_Q:.0f}%',data:W_LAB.map(function(){{return {SIG_Q:.0f};}}),borderColor:'rgba(21,101,192,0.55)',borderWidth:1.3,borderDash:[6,4],pointRadius:0}},
    {{label:'{TICKERS[1]} σ 目標 {SIG_S:.0f}%',data:W_LAB.map(function(){{return {SIG_S:.0f};}}),borderColor:'rgba(217,119,6,0.55)',borderWidth:1.3,borderDash:[6,4],pointRadius:0}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{beginAtZero:true,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});

// ---- backtest thumbnail: log nav + drawdown ----
var BT_LAB={BT_L},BT_C={BT_C},BT_B={BT_B};
function _dd(nav){{var dd=[],pk=0;for(var i=0;i<nav.length;i++){{if(nav[i]>pk)pk=nav[i];dd.push((nav[i]/pk-1)*100);}}return dd;}}
new Chart(document.getElementById('chart-bt-nav'),{{
  type:'line',
  data:{{labels:BT_LAB,datasets:[
    {{label:'正式追蹤版',data:BT_C,borderColor:GREEN,borderWidth:2,pointRadius:0,pointHoverRadius:3,tension:0.1}},
    {{label:'50/50 B&H',data:BT_B,borderColor:BLUE,borderWidth:1.3,borderDash:[6,3],pointRadius:0,pointHoverRadius:3,tension:0.1}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(2)+'×'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:8,font:{{size:9}},maxRotation:0,autoSkip:true}}}},
      y:{{type:'logarithmic',grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'×'}},font:{{size:9}}}}}}}}
  }}
}});
new Chart(document.getElementById('chart-bt-dd'),{{
  type:'line',
  data:{{labels:BT_LAB,datasets:[
    {{label:'正式追蹤版',data:_dd(BT_C),borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.12)',borderWidth:1.4,fill:'origin',pointRadius:0,tension:0.1}},
    {{label:'50/50 B&H',data:_dd(BT_B),borderColor:BLUE,backgroundColor:'rgba(21,101,192,0.06)',borderWidth:1.1,fill:'origin',pointRadius:0,tension:0.1}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:8,font:{{size:9}},maxRotation:0,autoSkip:true}}}},
      y:{{grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:9}}}}}}}}
  }}
}});
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# change detection
# ---------------------------------------------------------------------------
def detect_changes(prev: dict, sigs: dict) -> list:
    """可行動變化＝閘門翻轉，或任一標的最終權重變動 ≥ 10pp（vs 前一日 state）。"""
    if not prev or "tickers" not in prev:
        return []
    out = []
    for t in TICKERS:
        pt = prev["tickers"].get(t)
        if not pt:
            continue
        gate_flip = bool(pt.get("gate")) != bool(sigs[t]["gate"])
        new_final = round(sigs[t]["final"] * 100, 1)
        old_final = pt.get("final_weight_pct")
        big_move = old_final is not None and abs(old_final - new_final) >= 10.0
        if gate_flip or big_move:
            parts = []
            if gate_flip:
                parts.append("閘門 " + ("出場→在場" if sigs[t]["gate"] else "在場→出場"))
            arrow = (f"最終權重 {old_final:.0f}% → {new_final:.0f}%"
                     if old_final is not None else f"最終權重 {new_final:.0f}%")
            out.append(f"<b>{t}</b>：{'、'.join(parts) + ' → ' if parts else ''}{arrow}")
    return out


def main():
    prev_state = {}
    if STATE_JSON.exists():
        try:
            prev_state = json.loads(STATE_JSON.read_text())
        except Exception:
            prev_state = {}

    px_map, sigs = {}, {}
    for t in TICKERS:
        print(f"Fetching {t}...")
        px_map[t] = fetch_close(t)
        d = compute_ticker(t, px_map[t])
        sigs[t] = d
        print(f"  {t}: gate={'IN' if d['gate'] else 'OUT'} RV20={d['rv20']*100:.1f}% "
              f"sleeve={d['sleeve']:.2f} -> final {d['final']*100:.0f}%")

    combined = sum(sigs[t]["final"] for t in TICKERS) * 100
    print(f"Combined target exposure: {combined:.0f}%")

    changes = detect_changes(prev_state, sigs)
    data_date = max(sigs[t]["wk_date"] for t in TICKERS)

    # ---- history: rule-replay backfill (once) + idempotent daily live append ----
    prev_history = prev_state.get("history", [])
    backfill = build_backfill(px_map) if len(prev_history) < BACKFILL_DAYS else []
    daily_date = max(px_map[t].index[-1] for t in TICKERS)
    today_rec = _daily_record(px_map, daily_date, "live")
    history = merge_history(prev_history, backfill, today_rec)
    print(f"History: {len(history)} days (backfill {len(backfill)}, "
          f"span {history[0]['date']}→{history[-1]['date']})")

    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES: {last_change_desc}")
        lines = [f"QQQ+SMH 長線 × 波動率目標 — 可行動變化（數據截至 {data_date}）", ""]
        for c in changes:
            lines.append("• " + c.replace("<b>", "").replace("</b>", ""))
        lines += ["", "當前目標權重："]
        for t in TICKERS:
            d = sigs[t]
            lines.append(f"  {t}: {d['final']*100:.0f}%  "
                         f"(閘門{'在場' if d['gate'] else '出場'}, RV20 {d['rv20']*100:.1f}%, 套袖 {d['sleeve']:.2f})")
        lines += ["", f"組合目標曝險 {combined:.0f}% · 下一個交易日調整至上列目標。", "",
                  "前瞻 OOS 追蹤（未採用）。詳細： https://research.investmquest.com/long-track-qs-vt/"]
        ALERT_FILE.write_text("\n".join(lines), encoding="utf-8")
        print(f"Alert file: {ALERT_FILE}")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()
        print("No actionable change vs last run.")

    html = generate_html(sigs, changes, last_change_date, history)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "ruleset_locked_date": FREEZE_DATE,
        "status": "forward OOS paper tracking, not adopted",
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
        "weights": WEIGHTS,
        "combined_exposure_pct": round(combined, 1),
        "tickers": {
            t: {
                "gate": sigs[t]["gate"],
                "sigma_target_pct": round(SIGMA[t] * 100, 1),
                "rv20_pct": round(sigs[t]["rv20"] * 100, 2),
                "sleeve_weight": round(sigs[t]["sleeve"], 4),
                "final_weight_pct": round(sigs[t]["final"] * 100, 1),
                "wk_date": sigs[t]["wk_date"],
                "wk_close": round(sigs[t]["wk_close"], 2),
                "w52": round(sigs[t]["w52"], 2),
                "w104": round(sigs[t]["w104"], 2),
                "w250": round(sigs[t]["w250"], 2),
                "s104_pos": sigs[t]["s104_pos"],
                "s250_pos": sigs[t]["s250_pos"],
            } for t in TICKERS
        },
        "history": history,
    }
    STATE_JSON.write_text(json.dumps(state_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
