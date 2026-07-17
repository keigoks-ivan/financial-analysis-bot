#!/usr/bin/env python3
"""
台股 0050 + 2330 長線 × 波動率目標（自適應 σ 版）— 前瞻 OOS 追蹤訊號頁產生器
==========================================================================
/long-track-tw-vt/（固定 σ 版）的自適應 σ 姊妹子頁，輸出 adaptive.html；亦是美股
自適應子頁（update_long_track_qs_vt_adaptive.py）的台股同形移植。每交易日抓
0050.TW、2330.TW 日線（auto-adjust ＋ 幻影分割修復），逐標的算：
  1. 週線長軌閘門（W-FRI；進場 score5＝週收 > W52/W104/W250 且 W104/W250 四週
     斜率 > 0；出場一根週收 < W52；長多 only）→ 0/1。
  2. 自適應波動率套袖（本頁唯一與固定 σ 版不同處，凍結 2026-07-17）：
     σ_t＝RV20 的 rolling(756, min_periods=252).median()（近 3 年 RV20 中位數，首年
     expanding）；w = min(1, σ_t／RV20)。RV20＝20 日對數報酬年化波動。
  3. 最終目標權重 = 0.5 × 閘門 × 套袖（兩標的各自計算，合成即等權每日再平衡）。

規格完全比照固定 σ 主頁（閘門／執行層 10pp＋5% 取整／權重／窗／成本 7 bps 邊、t+1／
現金 1%／同凍結日 2026-07-17），唯套袖 σ 改滾動中位數。研究判定＝台股自適應過關
（Calmar 0.904→0.995），但 0.995 含 5% 取整的路徑運氣、且台股 2014 窗無深熊樣本，
須節制解讀；美股自適應為雜訊級平手（FAIL）。兩市場並跑供 2027-01 複審。

台股資料地雷（全部揭露）：0050.TW 2014-01-02 有 Yahoo 幻影分割壞 bar（~4:1），
內嵌 repair_phantom_splits 自動修復（單日 |報酬|>40% 且無登記分割 → 回溯縮放；
台股漲跌停 ±10%，真行情不可能觸發）；0050 免費歷史約 2009 起。集中度：2330 佔
0050 約五成，50/50 組合等效台積電曝險 ≈75%，非分散組合。

閘門逐位元對齊 run_ext_ltrack_smh.longtrack_weight；套袖對齊 run_adaptive_sigma.
vt_weight_adaptive_median(n_days=756)。回測數字見 BACKTEST 常數（band_exec.json
tw/adaptive/band10_round5 主列、tw_combo.json σ 階梯、live_engine_compare.json 實倉列）。

無 email／alert 檔：可行動變化通知由 /long-track-adaptive-vt/ 的既有排程涵蓋，本頁不
另發（頁面註明此點，避免雙重通知）。

CANONICAL COPY：本檔在 v7-backtest（src/vol_target_backtest/）與
financial-analysis-bot（scripts/）兩處逐位元相同——nav 匯入以 try/except 兼容
兩 repo，輸出路徑自動解析為 <repo_root>/docs/long-track-tw-vt/adaptive.html。CI 由 fab 執行。

排程：每交易日台股收盤（13:30 台北）後數小時（套袖 RV20／σ_t 為日頻量，閘門為週頻，
故日更）。

執行層（與規則同日凍結 2026-07-17）：|目標 − 現持| ≥ 10pp 才調整、調整取整至 5% 格；
band_exec_replay 從 history 確定性重放，供時間軸粗階梯線、事件表、通知與 state 的
executed_pct 用（回測主數字亦含此執行層，見 BACKTEST 常數）。

圖像化（Chart.js）：合成曝險量表＋每腿乘法鏈 bar（閘門×套袖→最終權重）、近三年
權重時間軸（粗階梯＝執行層持股率＋細線＝每日理論目標）＋ RV20 vs σ_t（動態）、執行層
變化事件表、回測縮圖（對數淨值＋回撤，BT_NAV 靜態快照＝執行版月度 NAV）。時間軸
資料存於 state.json 的 history 陣列：首次生成以
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

NAV_BLOCK = full_nav_block("system", "lttwvt")

# ---- output dir: <repo_root>/docs/long-track-tw-vt/ ------------------------
_cand = [HERE.parent / "docs", HERE.parents[2] / "docs" if len(HERE.parents) >= 3 else HERE / "docs"]
DOCS = next((c for c in _cand if c.exists()), _cand[0])
OUTPUT = DOCS / "long-track-tw-vt" / "adaptive.html"
STATE_JSON = DOCS / "long-track-tw-vt" / "adaptive_state.json"
# 無 email／alert 檔：可行動變化通知由 /long-track-adaptive-vt/ 的既有 email 涵蓋，
# 本頁不另發，避免雙重通知（頁面亦註明此點）。

TICKERS = ["0050", "2330"]
YF_SYMBOL = {"0050": "0050.TW", "2330": "2330.TW"}
WEIGHTS = {"0050": 0.5, "2330": 0.5}
SIGMA_BASE = {"0050": 0.15, "2330": 0.25}  # 固定 σ 版對照值；本頁套袖不使用（僅卡片顯示）
MED_WIN = 756                              # 自適應中位數視窗（3 年），凍結不再調整
MIN_PERIODS = 252                          # 首年 expanding
FREEZE_DATE = "2026-07-17"

# 回測（band_exec.json tw/adaptive、tw_combo.json σ 網格、live_engine_compare.json）— 轉錄
BACKTEST = {
    "window": "2014-01 – 2026-07",
    "rows": [                              # (label, cagr, mdd, calmar, ui, martin)
        ("自適應中位數 3y・含 10pp＋5% 取整執行層（本頁追蹤）", 18.53, -18.6, 0.995, 8.41, 2.20),
        ("每日照調（理論・對照）", 18.53, -19.6, 0.948, 8.60, 2.16),
        ("固定 σ 正式版・含執行層（對照）", 18.90, -20.9, 0.904, 8.59, 2.20),
        ("純長軌（無套袖）", 21.40, -23.5, 0.913, 9.38, 2.28),
        ("50/50 買進持有", 26.38, -39.5, 0.668, 9.85, 2.68),
        ("實倉引擎對照 50/50 E3（0050+2330）", 22.33, -25.0, 0.895, 8.76, 2.55),
    ],
    "sigma_ladder": [                      # (2330 σ, Calmar) — 0050 15% 固定、每日照調（tw_combo 網格）
        (20, 0.884), (25, 0.863), (30, 0.874),
    ],
    "eras": [                              # (label, ΔCAGR vs 固定 σ, ΔMDD pp) — 自適應每日照調 vs 固定 σ
        ("2014-16 陸股貶值/整理", -1.0, +1.2), ("2017-19 平順多頭", +0.4, +1.8),
        ("2020-22 COVID/升息", -0.0, +2.5), ("2023- AI 台積電牛", +0.8, -1.3),
    ],
}

# 回測月度淨值（回測快照，與 results/vol_targeting/tw_combo.json 同源、靜態轉錄；
# 用於本頁「回測縮圖」對數淨值＋回撤）。
BT_NAV = {
    "labels": ["2014-01","2014-02","2014-03","2014-04","2014-05","2014-06","2014-07","2014-08","2014-09","2014-10","2014-11","2014-12","2015-01","2015-02","2015-03","2015-04","2015-05","2015-06","2015-07","2015-08","2015-09","2015-10","2015-11","2015-12","2016-01","2016-02","2016-03","2016-04","2016-05","2016-06","2016-07","2016-08","2016-09","2016-10","2016-11","2016-12","2017-01","2017-02","2017-03","2017-04","2017-05","2017-06","2017-07","2017-08","2017-09","2017-10","2017-11","2017-12","2018-01","2018-02","2018-03","2018-04","2018-05","2018-06","2018-07","2018-08","2018-09","2018-10","2018-11","2018-12","2019-01","2019-02","2019-03","2019-04","2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12","2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12","2021-01","2021-02","2021-03","2021-04","2021-05","2021-06","2021-07","2021-08","2021-09","2021-10","2021-11","2021-12","2022-01","2022-02","2022-03","2022-04","2022-05","2022-06","2022-07","2022-08","2022-09","2022-10","2022-11","2022-12","2023-01","2023-02","2023-03","2023-04","2023-05","2023-06","2023-07","2023-08","2023-09","2023-10","2023-11","2023-12","2024-01","2024-02","2024-03","2024-04","2024-05","2024-06","2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12","2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07"],
    "combo": [1.0,1.0157,1.0741,1.0823,1.1055,1.1631,1.1577,1.19,1.1374,1.2186,1.2784,1.2682,1.2713,1.3255,1.2967,1.3264,1.32,1.2998,1.2676,1.2136,1.2146,1.2112,1.1978,1.2143,1.1889,1.2118,1.2591,1.181,1.1966,1.2556,1.3184,1.3406,1.3814,1.4073,1.3754,1.3687,1.3952,1.4208,1.4259,1.4521,1.498,1.5741,1.6092,1.6306,1.6103,1.7392,1.6572,1.6681,1.7943,1.7328,1.7284,1.6328,1.6086,1.618,1.7307,1.7838,1.8031,1.6208,1.6155,1.6168,1.6182,1.6215,1.6198,1.702,1.5618,1.5819,1.6586,1.6486,1.7215,1.8558,1.8893,2.0298,1.9649,1.949,1.7155,1.7521,1.7298,1.837,2.2674,2.2532,2.2814,2.2746,2.5196,2.7471,3.0556,3.1225,3.0925,3.1867,3.0927,3.1046,3.0376,3.1749,3.0564,3.0688,3.1071,3.2407,3.2876,3.1899,3.1114,3.0339,3.0364,3.039,3.0415,3.0443,3.0468,3.0492,3.0519,3.0546,3.0561,3.0583,3.0611,3.0632,3.0659,3.0238,3.0164,2.9421,2.851,2.8483,3.0847,3.179,3.2874,3.5304,3.8036,3.7884,3.8665,4.399,4.2756,4.2435,4.3288,4.5157,4.3834,4.6663,4.8897,4.6248,4.1237,4.127,4.1103,4.2845,4.6447,4.6884,5.2296,5.9354,5.6683,6.0194,6.7874,7.5679,6.8691,7.9495,8.6647,8.8373,8.5563],
    "bh": [1.0,1.0205,1.0854,1.0937,1.1172,1.1753,1.1699,1.206,1.1527,1.2653,1.3398,1.3313,1.3434,1.4115,1.376,1.4074,1.3993,1.3779,1.3408,1.2522,1.2587,1.3183,1.3094,1.3234,1.3046,1.3571,1.454,1.3659,1.4127,1.4942,1.5854,1.614,1.6664,1.7063,1.6709,1.6654,1.7013,1.7358,1.7425,1.778,1.8402,1.9437,1.9918,2.0208,1.9927,2.1702,2.0567,2.0717,2.2457,2.1758,2.1827,2.061,2.0572,2.0682,2.2694,2.3346,2.3639,2.1092,2.0602,2.0436,2.039,2.1672,2.2179,2.3303,2.1633,2.2502,2.3827,2.3669,2.4755,2.6766,2.7267,2.9351,2.8249,2.787,2.4175,2.7011,2.6291,2.8199,3.5482,3.5185,3.5761,3.5722,3.9517,4.3221,4.7258,4.882,4.8395,4.9986,4.9241,4.9597,4.8528,5.072,4.8828,4.9028,4.9678,5.1944,5.2682,5.0789,5.0551,4.634,4.7476,4.1458,4.3629,4.343,3.7348,3.5149,4.272,3.9892,4.5102,4.4725,4.6343,4.4195,4.8308,4.9772,4.9602,4.8306,4.6709,4.6692,5.0781,5.2415,5.4353,5.8851,6.5663,6.636,6.9295,7.9825,7.7514,7.8048,7.933,8.4057,8.1683,8.6954,9.1242,8.5425,7.5887,7.4903,7.9832,8.6929,9.423,9.5117,10.609,12.04,11.5783,12.3438,13.9957,15.6888,13.9375,17.1716,19.4701,19.9497,18.9252],
    "live": [1.0,1.0115,1.076,1.0842,1.1075,1.1651,1.1597,1.1956,1.1426,1.2544,1.3282,1.3197,1.3318,1.3993,1.3641,1.3952,1.3872,1.366,1.3179,1.2612,1.2626,1.2731,1.2602,1.2794,1.2637,1.2906,1.3517,1.2773,1.2992,1.3664,1.4362,1.4593,1.5068,1.5428,1.5108,1.5058,1.5383,1.5695,1.5756,1.6076,1.6639,1.7575,1.801,1.8273,1.8019,1.9624,1.8597,1.8732,2.0307,1.9562,1.9625,1.8514,1.8312,1.8385,1.9617,2.018,2.0433,1.8056,1.8021,1.7912,1.787,1.7991,1.7963,1.8734,1.721,1.7572,1.8607,1.8503,1.9249,2.0757,2.1146,2.2762,2.1908,2.1614,1.8424,1.9047,1.8714,1.958,2.4638,2.4431,2.4832,2.4804,2.744,3.0012,3.2816,3.3901,3.3606,3.471,3.4193,3.444,3.3698,3.4604,3.3312,3.3158,3.3364,3.4886,3.5382,3.411,3.3524,3.1934,3.1844,3.1871,3.1897,3.1927,3.1953,3.1979,3.2007,3.2034,3.2365,3.2109,3.2895,3.1884,3.3857,3.4996,3.4876,3.3965,3.2859,3.2694,3.5068,3.6197,3.7535,4.0642,4.5348,4.5829,4.7856,5.5129,5.3533,5.3902,5.4787,5.8052,5.6412,6.0053,6.3015,5.8997,5.3808,5.377,5.4895,5.7848,6.2709,6.3299,7.0604,8.013,7.7056,8.2152,9.3149,10.442,9.2761,11.4291,12.9592,13.2785,12.5964]
}

BACKFILL_DAYS = 756                        # 回放窗（近三年交易日；2026-07-17 自 252 擴）
HISTORY_CAP = 820                          # state.json history 陣列上限（>756 留實錄餘裕），防肥大


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def repair_phantom_splits(c: pd.Series, thresh: float = 0.4) -> pd.Series:
    """Yahoo phantom-split repair (port of tw_0050_backtest.backtest_tw):
    single-bar |return| > thresh with no recorded split -> rescale the PRIOR
    segment so the return series is continuous. TW price limit is ±10%, so a
    genuine move can never trip this. Known case: 0050.TW 2014-01-02 (~4:1)."""
    c = c.copy()
    r = c.pct_change()
    for d in r[r.abs() > thresh].index:
        i = c.index.get_loc(d)
        factor = float(c.iloc[i] / c.iloc[i - 1])
        c.iloc[:i] *= factor
        print(f"  phantom split repaired at {d.date()} (factor {factor:.5f})")
    return c


def fetch_close(ticker: str) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 13)   # 13y: W250 (~4.8y) warmup + state history
    df = yf.download(YF_SYMBOL[ticker], start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    c = c.dropna()
    if getattr(c.index, "tz", None) is not None:
        c.index = c.index.tz_localize(None)
    return repair_phantom_splits(c)


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
# Sleeve — adaptive median (逐位元對齊 run_adaptive_sigma.vt_weight_adaptive_median，n_days=756)
# ---------------------------------------------------------------------------
def _sleeve_from(px: pd.Series, win: int = 20):
    """Returns (rv20_now, sigma_t_now, sleeve). σ_t ＝ RV20 的 rolling(756,
    min_periods=252).median()；w = min(1, σ_t/RV20)，NaN → 1（滿載）。因果、無前視。"""
    lr = np.log(px / px.shift(1))
    rv = lr.rolling(win).std() * np.sqrt(252)
    sigma = rv.rolling(MED_WIN, min_periods=MIN_PERIODS).median()
    rv_now = float(rv.iloc[-1])
    sig_now = float(sigma.iloc[-1])
    if rv_now > 0 and not np.isnan(sig_now):
        w = min(1.0, sig_now / rv_now)
    else:
        w = 1.0
        if np.isnan(sig_now):
            sig_now = rv_now
    return rv_now, sig_now, w


def sleeve_state(px: pd.Series, win: int = 20) -> dict:
    rv_now, sig_now, w = _sleeve_from(px, win)
    return {"rv20": rv_now, "sigma_t": sig_now, "sleeve": w}


def compute_ticker(t: str, px: pd.Series) -> dict:
    g = gate_state(px)
    s = sleeve_state(px)
    fill = (1 if g["gate"] else 0) * s["sleeve"]        # 0..1 fill of the 0.5 slot
    final = WEIGHTS[t] * fill
    return {**g, **s, "sigma_base": SIGMA_BASE[t], "fill": fill, "final": final}


# ---------------------------------------------------------------------------
# History — rule-replay backfill (誠實紀律：回放 ≠ 實錄，欄位 source 標記區分)
# ---------------------------------------------------------------------------
def _daily_record(px_map: dict, d: pd.Timestamp, source: str) -> dict:
    """One day's target weights, computed byte-identically to the live path:
    gate = _gate_core(px[:d]).pos.iloc[-1] (含當週部分週線，與每日腳本一致)；
    sleeve = min(1, σ_t/RV20)（σ_t＝近 3 年 RV20 中位數）on px[:d]，每腿記 sigma_t_pct。
    source ∈ {'replay','live'}."""
    rec = {"date": d.strftime("%Y-%m-%d"), "source": source, "tickers": {}}
    combined = 0.0
    for t in TICKERS:
        pxd = px_map[t].loc[:d]
        _, pos, *_ = _gate_core(pxd)
        gate = bool(pos.iloc[-1])
        rv_now, sig_now, sleeve = _sleeve_from(pxd)
        final = WEIGHTS[t] * ((1 if gate else 0) * sleeve)
        combined += final
        rec["tickers"][t] = {
            "gate": gate,
            "rv20_pct": round(rv_now * 100, 2),
            "sigma_t_pct": round(sig_now * 100, 2),
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
# Execution layer — 10pp 門檻＋5% 取整（與規則同日凍結 2026-07-17）
# 從 history 確定性重放，冪等可重現。band／grid 以組合 pp 為單位（每腿滿載＝50 pp）。
# ---------------------------------------------------------------------------
def band_exec_replay(history: list, legs: list | None = None) -> dict:
    """對每腿的最終權重（組合 pp）重放執行層：executed 初始 0，逐日若
    |target − executed| ≥ 10pp 則 executed = round(target/5)×5，否則不變。
    回傳每腿每日 executed、組合合計、事件清單（日期、腿、from→to、原因＝該日
    閘門翻轉則「閘門翻轉」否則「波動調整」、當日組合執行曝險）與各腿當前值。"""
    legs = legs or TICKERS
    executed = {t: [] for t in legs}
    combined, events = [], []
    cur = {t: 0.0 for t in legs}
    prev_gate = {t: None for t in legs}
    for r in history:
        for t in legs:
            tk = r["tickers"][t]
            target = tk["final_pct"]
            gate = bool(tk["gate"])
            if abs(target - cur[t]) >= 10.0:
                new = round(target / 5.0) * 5.0
                if new != cur[t]:
                    flipped = prev_gate[t] is not None and gate != prev_gate[t]
                    events.append({"date": r["date"], "leg": t,
                                   "from": cur[t], "to": new,
                                   "reason": "閘門翻轉" if flipped else "波動調整"})
                    cur[t] = new
            executed[t].append(cur[t])
            prev_gate[t] = gate
        combined.append(round(sum(cur[t] for t in legs), 1))
    date_idx = {r["date"]: i for i, r in enumerate(history)}
    for ev in events:
        ev["combined_exec_pct"] = combined[date_idx[ev["date"]]]
    last = {t: (executed[t][-1] if executed[t] else 0.0) for t in legs}
    return {"executed": executed, "combined": combined, "events": events, "last": last}


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
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">自適應波動率套袖（動態 σ_t）</span><span class="sig-mark">{d['sleeve']*100:.0f}%</span></div>
      <div class="sig-detail">RV20（20日年化波動）<b>{d['rv20']*100:.1f}%</b> vs σ_t <b>{d['sigma_t']*100:.1f}%</b>（σ目標＝近 3 年 RV20 中位數（動態））
        → w = min(1, {d['sigma_t']*100:.1f}%／{d['rv20']*100:.1f}%) = <b>{d['sleeve']:.2f}</b>
        <br><span style="font-size:.72rem">{'波動 ≤ 近 3 年中位，滿載。' if d['sleeve']>=0.999 else '波動高於自身近 3 年中位，按比例減碼（只降不加）。'} 固定 σ 版對照 σ＝{d['sigma_base']*100:.0f}%。</span></div>
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
        hl = "rowhl" if "本頁追蹤" in lab else ("rowbh" if "買進持有" in lab else "")
        rows += (f'<tr class="{hl}"><td>{lab}</td><td class="num">{cagr:.2f}%</td>'
                 f'<td class="num">{mdd:.1f}%</td><td class="num">{calmar:.3f}</td>'
                 f'<td class="num">{ui:.2f}</td><td class="num">{martin:.2f}</td></tr>\n')
    ladder = ""
    for ss, calmar in BACKTEST["sigma_ladder"]:
        ladder += (f'<tr><td>0050 15% / 2330 {ss}%</td>'
                   f'<td class="num">{calmar:.3f}</td></tr>\n')
    eras = ""
    for lab, dc, dm in BACKTEST["eras"]:
        cc = "pos" if dc >= 0 else "neg"
        cm = "pos" if dm >= 0 else "neg"
        eras += (f'<tr><td>{lab}</td><td class="num {cc}">{dc:+.1f}pp</td>'
                 f'<td class="num {cm}">{dm:+.1f}pp</td></tr>\n')
    return f"""<div class="card">
<h3>回測摘要（自適應中位數 3y vs 對照・共同窗 {BACKTEST['window']}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
兩標的日報酬 50/50 加權合成（等效每日再平衡，如實揭露）。判準基準＝<b>固定 σ 正式版</b>（本頁與固定 σ 版差異只在套袖，閘門完全相同）。<b>主列與固定 σ 對照列皆含 10pp 門檻＋5% 取整執行層</b>（apples-to-apples）；「每日照調」為理論對照。「實倉引擎對照」＝2330/0050 E3（0..1 分數倉），同權重 50/50、同窗、同成本，<b>非本頁 0/1 閘門機制</b>。含執行層數字自 band_exec.json、實倉引擎自 live_engine_compare.json。共同窗自 2014 起：0050 免費史 2009 起、W250 需約 250 週暖機。</p>
<table><thead><tr><th>配置</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Calmar</th><th class="num">Ulcer</th><th class="num">Martin</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="takeaway"><b>台股自適應判定＝過關（但須節制解讀）</b>：主列（含執行層）vs 固定 σ 正式版（同含執行層）Calmar 0.904 → <b>0.995</b>、Martin 2.20 ≈ 2.20、MDD −20.9% → <b>−18.6%</b>，CAGR 幾乎不變；每日照調理論版 0.948，執行層對台股自適應再加值（0.948 → 0.995）。
<b>誠實警語</b>：0.995 這個數字含 <b>5% 取整的路徑運氣成分</b>，與每日照調 0.948 的差距在<b>離散執行敏感度的量級內</b>（帶 5pp 連續版 0.958、帶 10pp 連續版 0.909），不得過度解讀為「自適應穩定勝出 0.05 Calmar」；<b>台股窗 2014 起無深熊崩盤樣本</b>，真正的深水保護未受檢驗（深熊證據見固定 σ 版的 2330 長窗附錄）。
與美股自適應（雜訊級平手 FAIL）並置＝同一機制、兩市場、兩個相反判定，正是與固定版並跑要檢驗的（見 <a href="/long-track-adaptive-vt/">自適應美台總覽</a>）。</div>
</div>

<div class="card">
<h3>固定 σ 階梯對照（0050 15% 固定、2330 σ 掃描・每日照調）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
手動調 2330 σ 的增益有限（20→25→30 僅 0.884／0.863／0.874 來回，無單調趨勢）——<b>自適應機制以滾動中位數自動取代此手動選擇</b>：波動 regime 高時 σ_t 自動上移（少欠載）、低時下移（多減碼），不必人工釘死一個固定 σ。此階梯僅供理解「為何要自適應」，不追蹤。</p>
<table><thead><tr><th>σ 組合</th><th class="num">Calmar</th></tr></thead>
<tbody>{ladder}</tbody></table>
</div>

<div class="card">
<h3>分期（自適應每日照調 vs 固定 σ；ΔCAGR／ΔMDD，正＝自適應較優）</h3>
<table><thead><tr><th>期間</th><th class="num">Δ CAGR</th><th class="num">Δ MDD</th></tr></thead>
<tbody>{eras}</tbody></table>
<div style="font-size:.75rem;color:var(--muted);margin-top:.5rem">ΔMDD 正值＝自適應回撤較淺；ΔCAGR 正值＝自適應報酬較高。與固定 σ 對照（每日照調基準），非與買進持有對照。</div>
</div>"""


def events_card(exec_replay: dict) -> str:
    events = exec_replay.get("events", []) if exec_replay else []
    if not events:
        body = ('<tr><td colspan="5" style="text-align:center;color:var(--muted)">'
                '近三年窗內無執行層調整事件（皆未跨 10pp 門檻）</td></tr>')
    else:
        body = ""
        for ev in reversed(events):                 # 倒序（最新在上）
            rc = "var(--blue-text)" if ev["reason"] == "閘門翻轉" else "var(--amber-text)"
            body += (f'<tr><td>{ev["date"]}</td><td><b>{ev["leg"]}</b></td>'
                     f'<td>{ev["from"]:.0f}% → {ev["to"]:.0f}%</td>'
                     f'<td style="color:{rc}">{ev["reason"]}</td>'
                     f'<td class="num">{ev["combined_exec_pct"]:.0f}%</td></tr>\n')
    return f"""<div class="card">
<h3>近三年執行層訊號變化事件（10pp 門檻＋5% 取整）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
只有當某腿目標與現持差 ≥ 10pp 才調整（取整到 5% 格），故事件遠少於每日微調。倒序全列；「變化」為該腿最終權重（組合 pp，滿載 50%）；原因＝當日閘門翻轉則「閘門翻轉」否則「波動調整」。</p>
<table><thead><tr><th>日期</th><th>腿</th><th>變化</th><th>原因</th><th class="num">當日組合執行曝險</th></tr></thead>
<tbody>{body}</tbody></table>
</div>"""


def generate_html(sigs: dict, changes: list | None, last_change_date: str | None,
                  history: list | None = None, exec_replay: dict | None = None) -> str:
    changes = changes or []
    history = history or []
    exec_replay = exec_replay or {"executed": {t: [] for t in TICKERS}, "combined": [], "events": [], "last": {}}
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
    H_A = _col(lambda r: r["tickers"][TICKERS[0]]["final_pct"])
    H_B = _col(lambda r: r["tickers"][TICKERS[1]]["final_pct"])
    H_ARV = _col(lambda r: r["tickers"][TICKERS[0]]["rv20_pct"])
    H_BRV = _col(lambda r: r["tickers"][TICKERS[1]]["rv20_pct"])
    H_ASIG = _col(lambda r: r["tickers"][TICKERS[0]]["sigma_t_pct"])
    H_BSIG = _col(lambda r: r["tickers"][TICKERS[1]]["sigma_t_pct"])
    H_SRC = _col(lambda r: r["source"])
    # executed layer (10pp band + 5% round) — deterministic replay
    H_CEXE = json.dumps(exec_replay["combined"], separators=(",", ":"))
    H_AEXE = json.dumps(exec_replay["executed"].get(TICKERS[0], []), separators=(",", ":"))
    H_BEXE = json.dumps(exec_replay["executed"].get(TICKERS[1], []), separators=(",", ":"))
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
    CCOL_HEX = {"green": "#16a34a", "blue": "#1d4ed8",
                "amber": "#a16207", "red": "#b91c1c"}[ccol]

    # ---- backtest thumbnail (static snapshot) ----
    BT_L = json.dumps(BT_NAV["labels"], separators=(",", ":"))
    BT_C = json.dumps(BT_NAV["combo"], separators=(",", ":"))
    BT_B = json.dumps(BT_NAV["bh"], separators=(",", ":"))
    BT_V = json.dumps(BT_NAV["live"], separators=(",", ":"))

    change_html = (
        ('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;'
         'padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">'
         '可行動變化</b><br>' + "<br>".join(changes) +
         '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>')
        if changes else
        ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">'
         '無可行動變化（閘門未翻轉、且無標的目標與現持差 ≥ 10pp）' +
         (f'（上次變化：{last_change_date}）' if last_change_date else '') + '</div>'))

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>台股 0050 + 2330 長線 × 波動率目標（自適應 σ 版）｜前瞻 OOS 追蹤 | InvestMQuest Research</title>
  <meta name="description" content="0050 50% + 2330 50% · 週線長軌閘門 × 自適應波動率套袖（σ_t＝近 3 年 RV20 中位數）· 前瞻 OOS 紙上追蹤（未採用）">
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
    <div class="crumb"><a href="/">首頁</a> / 台股 0050 + 2330 長線 × 波動率目標（自適應 σ 版）</div>
    <h1>台股 0050 + 2330 長線 × 波動率目標（自適應 σ 版）— 前瞻 OOS 追蹤</h1>
    <div class="sub">50% 0050 + 50% 2330 · 週線長軌閘門 × 自適應波動率套袖（σ_t＝近 3 年 RV20 中位數，動態）· Long only · 紙上追蹤（未採用）</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem;flex-wrap:wrap">
      <a href="/long-track-tw-vt/adaptive.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">自適應 σ 版（本頁）</a>
      <a href="/long-track-tw-vt/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">固定 σ 版</a>
      <a href="/long-track-qs-vt/adaptive.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">QQQ+SMH 自適應子頁</a>
      <a href="/long-track-adaptive-vt/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">自適應美台總覽</a>
      <a href="/long-track-tw/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">台股長線 2330/0050（實倉）</a>
      <a href="/backtest/vol_targeting/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">波動率目標回測</a>
    </div>
  </div>
</div>
<div class="container">

<div class="oos-banner">
  <span class="tag-loud">前瞻 OOS 追蹤中・未採用（PAPER TRACKING）</span>
  <div style="font-size:.86rem">本頁＝<a href="/long-track-tw-vt/">固定 σ 版</a>的<b>自適應對照</b>：唯一差異是套袖 σ 改用<b>近 3 年 RV20 滾動中位數</b>（動態），閘門／執行層／權重／窗／成本全同，<b>同凍結日 {FREEZE_DATE}</b>。
  研究判定＝台股自適應<b>過關</b>（Calmar 0.904 → 0.995），但<b>0.995 含 5% 取整的路徑運氣、且台股 2014 窗無深熊樣本</b>，須節制解讀（見回測摘要警語）。與<a href="/long-track-qs-vt/adaptive.html">美股自適應（雜訊級平手）</a>並跑，供 <b>2027-01 或滿 120 個追蹤交易日</b>複審。
  <b>本頁不另發 email</b>——可行動變化通知由 <a href="/long-track-adaptive-vt/">自適應美台總覽</a> 涵蓋（避免雙重通知）。</div>
</div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>組合當前目標曝險</span></div>
  <div class="status-exposure">{combined:.0f}%</div>
  <div style="font-size:.8rem;color:var(--muted)">0.5 × 閘門 × 自適應套袖，兩標的相加 · 閒置部分持現金</div>
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
<h3>近三年權重時間軸 — 執行層持股率 ＋ 每日理論目標</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
<b style="color:var(--text)">粗階梯線＝10pp 門檻＋5% 取整的實際執行持股率</b>（跨門檻才動、取整到 5% 格）；<b>細線＝每日理論目標</b>（未過門檻）。
線段<b>實線＝每日實錄</b>（CI 逐日追加），<b>虛線＝規則回放</b>（首次生成時以完全相同的規則往回重算，非當日實錄，誠實區隔）。
窗 {span}，共 {len(history)} 個交易日（回放 {n_replay}／實錄 {n_live}）。</p>
<div class="chart-wrap"><canvas id="chart-weights"></canvas></div>
<div class="legend-note">
  <span class="ln-item"><span class="ln-line" style="border-top-width:3px"></span>執行層（粗階梯）</span>
  <span class="ln-item"><span class="ln-line" style="border-top-color:rgba(120,120,120,.5)"></span>每日理論目標（細）</span>
  <span class="ln-item"><span class="ln-line"></span>每日實錄</span>
  <span class="ln-item"><span class="ln-line ln-dash"></span>規則回放</span>
</div>
<h3 style="margin-top:1.1rem">套袖觸發脈絡 — RV20 vs σ_t（動態）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
本頁 σ_t 是<b>動態線</b>（近 3 年 RV20 滾動中位數），不是固定 σ 版的水平虛線。當 RV20（實線）升破自身 σ_t（虛線）時套袖按比例減碼；RV20 ≤ σ_t 時滿載。regime 抬升時 σ_t 跟著上移，是本頁與固定 σ 版的唯一機制差異。</p>
<div class="chart-wrap-sm"><canvas id="chart-rv"></canvas></div>
</div>

{events_card(exec_replay)}

<div class="tgrid">{cards}</div>

<div class="card">
<h3>追蹤版規則（自適應 σ；{FREEZE_DATE} 定案，此後不再調整）</h3>
<div class="rule-list">
① <b>兩標的各 50%</b>，日報酬加權合成（<b>絕不直接相加 equity curve</b>；50/50 日報酬加權＝等效每日再平衡，如實揭露此假設）。<br>
② <b>週線長軌閘門</b>（W-FRI）：進場＝週收盤 &gt; W52／W104／W250 且 W104／W250 四週斜率 &gt; 0（score5）；出場＝一根週收盤 &lt; W52；<b>長多 only</b>，閘門輸出 0／1。<br>
③ <b>自適應波動率套袖（本頁唯一與固定 σ 版不同處，凍結 {FREEZE_DATE}）</b>：σ_t＝RV20 的 <b>rolling(756, min_periods=252).median()</b>（近 3 年 RV20 中位數，首年 expanding）；w = min(1, σ_t／RV20)，<b>只降不加</b>（上限 1.0）。語義＝相對自身 regime 的尖峰偵測器，非固定的絕對風險預算。<br>
④ <b>機制與視窗凍結</b>：滾動中位數 3 年（756／252）鎖死，<b>此後不再調整</b>；不掃 N 擇優、不改機制形狀。固定 σ 對照值（0050 15%／2330 25%）僅供卡片顯示，套袖不使用。<br>
⑤ <b>執行</b>：t 收盤訊號、t+1 收盤生效；成本 7 bps／邊；閒置現金 1%／年（台幣短率假設）。<br>
⑥ <b>最終權重</b> = 0.5 × 閘門(0/1) × 套袖權重，兩標的各自計算。<br>
⑦ <b>資料揭露</b>：yfinance auto-adjust（還原股價）；0050.TW 2014-01-02 幻影分割壞 bar 由腳本自動修復（回溯縮放，門檻單日 ±40%，台股漲跌停 ±10% 不可能誤觸）；0050 免費歷史約 2009 起。<br>
⑧ <b>集中度揭露</b>：2330 佔 0050 權重約五成，50/50 組合等效台積電曝險 ≈ 0.5 ＋ 0.5×0.5 = 75%。<b>這不是分散組合</b>，是台積電 beta 的兩種包裝。<br>
⑨ <b>執行層（{FREEZE_DATE} 與規則同日凍結）</b>：|目標 − 現持| ≥ 10pp 才調整，調整取整至 5% 格；<b>回測主數字含此執行層</b>，與追蹤操作同規則。<br>
<span style="color:var(--muted);font-size:.78rem">閘門為週頻（僅週五可能翻轉），套袖 RV20／σ_t 為日頻（每日可能微調），故本頁每交易日更新。「可行動變化」＝閘門翻轉，或今日目標與現持（執行層 executed）差 ≥ 10pp。<b>本頁不另發 email</b>，通知由 <a href="/long-track-adaptive-vt/">自適應美台總覽</a> 涵蓋（避免雙重通知）。</span>
</div>
</div>

{tables}

<div class="card">
<h3>回測縮圖 — 自適應中位數 3y（含執行層）vs 50/50 B&amp;H（對數淨值＋回撤）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
回測快照（{BT_NAV['labels'][0]} → {BT_NAV['labels'][-1]}）。淨值線＝<b>自適應中位數 3y（含 10pp 門檻＋5% 取整執行層，與追蹤操作同規則）</b>，由 run_band_exec_ablation 月度 NAV 靜態轉錄；B&amp;H 線不變；<b style="color:var(--amber-text)">琥珀虛線＝實倉引擎（2330/0050 E3，同權重 50/50、同窗、同成本對照）</b>。
本頁系統（0/1 長軌閘門 × 自適應套袖 × 執行層）與實倉引擎（E3 分數倉 0..1）是不同機制；對照僅供「同一筆錢若改放實倉引擎規則」參考，<b>非替代關係</b>。固定 σ 版深度分析見 <a href="/backtest/vol_targeting/">波動率目標回測</a>。</p>
<div class="grid2">
  <div class="chart-wrap-sm"><canvas id="chart-bt-nav"></canvas></div>
  <div class="chart-wrap-sm"><canvas id="chart-bt-dd"></canvas></div>
</div>
<div style="text-align:right;margin-top:.5rem"><a href="/backtest/vol_targeting/" style="font-size:.82rem;font-weight:600">看美股版回測深度頁 →</a></div>
</div>

{backtest_section()}

<div class="card">
<h3>複審條件</h3>
<div class="rule-list" style="font-size:.82rem">
於 <b>2027-01</b> 或滿 <b>120 個追蹤交易日</b>後，檢視前瞻 OOS 的 CAGR／MDD／Calmar 是否落在回測分布內，
並與美股版並讀：若台股 OOS 也顯示套袖只付代價不給保護（如回測所示），則「不值得」判定獲得樣本外支持；
若台股遇到深回撤而套袖顯著護住（回測裡只在 2330 含 2008 崩盤的長窗出現過），則需重審統一定律的門檻。
<b>在此之前本頁純為研究追蹤，不構成任何倉位建議。</b>
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research · 台股 0050+2330 長線 × 波動率目標（自適應 σ 版・前瞻 OOS 追蹤・未採用）</div>
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

// ---- 3-year weight timeline: executed step lines (thick) + raw target (thin) ----
var W_LAB={H_LABELS},W_SRC={H_SRC};
function segDash(ctx){{return W_SRC[ctx.p1DataIndex]==='live'?undefined:[3,3];}}
new Chart(document.getElementById('chart-weights'),{{
  type:'line',
  data:{{labels:W_LAB,datasets:[
    {{label:'合成執行',data:{H_CEXE},borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.09)',
     borderWidth:2.8,stepped:true,pointRadius:0,pointHoverRadius:3,fill:'origin',segment:{{borderDash:segDash}}}},
    {{label:'{TICKERS[0]} 執行',data:{H_AEXE},borderColor:BLUE,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash}}}},
    {{label:'{TICKERS[1]} 執行',data:{H_BEXE},borderColor:AMBER,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash}}}},
    {{label:'合成目標（理論）',data:{H_COMB},borderColor:'rgba(22,163,74,0.40)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}},
    {{label:'{TICKERS[0]} 目標',data:{H_A},borderColor:'rgba(21,101,192,0.35)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}},
    {{label:'{TICKERS[1]} 目標',data:{H_B},borderColor:'rgba(217,119,6,0.35)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}}
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
    {{label:'{TICKERS[0]} RV20',data:{H_ARV},borderColor:BLUE,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{TICKERS[1]} RV20',data:{H_BRV},borderColor:AMBER,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{TICKERS[0]} σ_t（動態）',data:{H_ASIG},borderColor:'rgba(21,101,192,0.55)',borderWidth:1.4,borderDash:[6,4],pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{TICKERS[1]} σ_t（動態）',data:{H_BSIG},borderColor:'rgba(217,119,6,0.55)',borderWidth:1.4,borderDash:[6,4],pointRadius:0,pointHoverRadius:3,tension:0.15}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{beginAtZero:true,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});

// ---- backtest thumbnail: log nav + drawdown ----
var BT_LAB={BT_L},BT_C={BT_C},BT_B={BT_B},BT_V={BT_V};
function _dd(nav){{var dd=[],pk=0;for(var i=0;i<nav.length;i++){{if(nav[i]>pk)pk=nav[i];dd.push((nav[i]/pk-1)*100);}}return dd;}}
new Chart(document.getElementById('chart-bt-nav'),{{
  type:'line',
  data:{{labels:BT_LAB,datasets:[
    {{label:'自適應中位數 3y',data:BT_C,borderColor:GREEN,borderWidth:2,pointRadius:0,pointHoverRadius:3,tension:0.1}},
    {{label:'50/50 B&H',data:BT_B,borderColor:BLUE,borderWidth:1.3,borderDash:[6,3],pointRadius:0,pointHoverRadius:3,tension:0.1}},
    {{label:'實倉引擎（同權重對照）',data:BT_V,borderColor:AMBER,borderWidth:1.2,borderDash:[3,3],pointRadius:0,pointHoverRadius:3,tension:0.1}}
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
    {{label:'自適應中位數 3y',data:_dd(BT_C),borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.12)',borderWidth:1.4,fill:'origin',pointRadius:0,tension:0.1}},
    {{label:'50/50 B&H',data:_dd(BT_B),borderColor:BLUE,backgroundColor:'rgba(21,101,192,0.06)',borderWidth:1.1,fill:'origin',pointRadius:0,tension:0.1}},
    {{label:'實倉引擎（同權重對照）',data:_dd(BT_V),borderColor:AMBER,borderWidth:1.1,borderDash:[3,3],pointRadius:0,tension:0.1}}
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
    """可行動變化＝閘門翻轉，或 |今日目標 − 現持（執行層 executed_pct）| ≥ 10pp。
    改為與現持比（非與前一日目標比），才不會漏掉緩慢累積的漂移。alert 顯示取整後
    的建議動作（現持 → round(目標/5)×5）。"""
    if not prev or "tickers" not in prev:
        return []
    out = []
    for t in TICKERS:
        pt = prev["tickers"].get(t)
        if not pt:
            continue
        gate_flip = bool(pt.get("gate")) != bool(sigs[t]["gate"])
        target = round(sigs[t]["final"] * 100, 1)
        held = pt.get("executed_pct")
        drift = held is not None and abs(target - held) >= 10.0
        if gate_flip or drift:
            new_exec = round(target / 5.0) * 5.0
            parts = []
            if gate_flip:
                parts.append("閘門 " + ("出場→在場" if sigs[t]["gate"] else "在場→出場"))
            arrow = (f"最終權重 {held:.0f}% → {new_exec:.0f}%"
                     if held is not None else f"最終權重 → {new_exec:.0f}%")
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
        print(f"Fetching {YF_SYMBOL[t]}...")
        px_map[t] = fetch_close(t)
        d = compute_ticker(t, px_map[t])
        sigs[t] = d
        print(f"  {t}: gate={'IN' if d['gate'] else 'OUT'} RV20={d['rv20']*100:.1f}% "
              f"σ_t={d['sigma_t']*100:.1f}% sleeve={d['sleeve']:.2f} -> final {d['final']*100:.0f}%")

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

    # ---- execution layer replay (deterministic from history) ----
    exec_replay = band_exec_replay(history)
    print(f"Exec layer: {len(exec_replay['events'])} events, "
          f"current executed " + ", ".join(f"{t} {exec_replay['last'][t]:.0f}%" for t in TICKERS))

    # 無 email／alert 檔：可行動變化通知由 /long-track-adaptive-vt/ 涵蓋（避免雙重通知）。
    # 僅在 state 記錄 last_change 供頁面顯示。
    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES: {last_change_desc}（本頁不發 email；通知由 /long-track-adaptive-vt/ 涵蓋）")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        print("No actionable change vs last run.")

    html = generate_html(sigs, changes, last_change_date, history, exec_replay)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "ruleset_locked_date": FREEZE_DATE,
        "mechanism": "adaptive median σ_t = rolling(756, min_periods=252).median(RV20); w=min(1, σ_t/RV20)",
        "status": "forward OOS paper tracking, not adopted (adaptive-σ sibling of /long-track-tw-vt/; TW verdict: pass but path-luck caveat)",
        "no_email": "notifications covered by /long-track-adaptive-vt/ (avoid double-notify)",
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
        "weights": WEIGHTS,
        "combined_exposure_pct": round(combined, 1),
        "tickers": {
            t: {
                "gate": sigs[t]["gate"],
                "sigma_base_pct": round(SIGMA_BASE[t] * 100, 1),
                "sigma_t_pct": round(sigs[t]["sigma_t"] * 100, 2),
                "rv20_pct": round(sigs[t]["rv20"] * 100, 2),
                "sleeve_weight": round(sigs[t]["sleeve"], 4),
                "final_weight_pct": round(sigs[t]["final"] * 100, 1),
                "executed_pct": exec_replay["last"][t],
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
