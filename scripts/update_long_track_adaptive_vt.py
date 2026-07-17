#!/usr/bin/env python3
"""自適應 σ 長線 × 波動率目標（美股 QQQ+SMH ＋ 台股 0050+2330）— 前瞻 OOS 追蹤產生器
================================================================================
固定 σ 版（update_long_track_qs_vt.py／update_long_track_tw_vt.py）的自適應 σ 姊妹頁。
每交易日抓四腿日線（美股 QQQ、SMH auto-adjust；台股 0050.TW、2330.TW auto-adjust
＋幻影分割修復），兩市場各自獨立追蹤（各 100%），逐腿算：
  1. 週線長軌閘門（W-FRI；進場 score5＝週收 > W52/W104/W250 且 W104/W250 四週
     斜率 > 0；出場一根週收 < W52；長多 only）→ 0/1。
  2. 自適應波動率套袖（本頁唯一與固定 σ 版不同處，凍結 2026-07-17）：
       σ_t ＝ RV20 的 rolling(756, min_periods=252).median()（近三年 RV20 中位數，
       首年 expanding）；w = min(1, σ_t／RV20)。RV20＝20 日對數報酬年化波動。
       語義＝「相對自身 regime 的尖峰偵測器」，不是固定的絕對風險預算。
  3. 最終目標權重 = 0.5 × 閘門 × 套袖（每市場兩腿各自計算，合成即等權每日再平衡）。

正式追蹤版規則（2026-07-17 定案後不再調整）：機制＝滾動中位數 3 年（756/252），視窗
鎖死；成本 7 bps／邊；t 收盤訊號、t+1 收盤生效。定位＝前瞻 OOS 追蹤，非實盤採用。

這是「固定 vs 自適應」並行 OOS 對照實驗——與 /long-track-qs-vt/（固定 σ 美股）、
/long-track-tw-vt/（固定 σ 台股）並跑。研究判定（見 results/vol_targeting/
adaptive_sigma.json）：台股過關（自適應中位數 3y/5y 兩窗同向、Calmar 0.863 → 0.948、
Martin 2.05 → 2.16）；美股雜訊級平手（Calmar 0.547 → 0.540、Martin 1.45 → 1.45，
FAIL＝無證據值得替換固定 σ，非更差）。2027-01 或滿 120 交易日複審，與兩固定 σ 版並讀。

閘門定義逐位元對齊回測授權（v7-backtest src/vol_target_backtest/run_ext_ltrack_smh.
longtrack_weight）；套袖對齊 run_adaptive_sigma.vt_weight_adaptive_median(n_days=756)。
規則若變更，各處一起改。回測數字見 BT_US／BT_TW／APPENDIX_2330 常數（由
results/vol_targeting/adaptive_sigma.json 轉錄）。

CANONICAL COPY：本檔在 v7-backtest（src/vol_target_backtest/）與 financial-analysis-bot
（scripts/）兩處逐位元相同——nav 匯入以 try/except 兼容兩 repo，輸出路徑自動解析為
<repo_root>/docs/long-track-adaptive-vt/。CI 由 fab 執行（台股收盤後、美股收盤後各跑
一次，date-keyed merge 冪等所以安全）。

執行層（與規則同日凍結 2026-07-17）：|目標 − 現持| ≥ 10pp 才調整、調整取整至 5% 格；
兩市場各自以 band_exec_replay 從 history_us／history_tw 確定性重放，供時間軸粗階梯線、
事件表、通知與 state 的 executed_pct 用（回測主數字亦含此執行層，見 BT_US／BT_TW 常數）。

圖像化（Chart.js）：兩市場各一個合成曝險量表＋每腿乘法鏈 bar、近三年權重時間軸（粗階梯
＝執行層持股率＋細線＝每日理論目標）＋ RV20 vs σ_t（σ_t 本頁是動態線，非水平虛線）、
執行層變化事件表、回測縮圖（對數淨值＋回撤，BT_* 靜態快照＝執行版月度 NAV）。
時間軸資料存於 state.json 的 history_us／history_tw 陣列（各自市場交易日曆）：首次生成以
build_backfill 規則回放近 756 交易日＝約三年（source='replay'），此後 CI 逐日以
_daily_record 追加當日實錄（source='live'）；merge_history 以日期為 key 冪等，上限
HISTORY_CAP。回放與實錄在圖上以虛線／實線區隔（誠實紀律，回放不偽裝成實錄）。
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

NAV_BLOCK = full_nav_block("system", "ltadvt")

# ---- output dir: <repo_root>/docs/long-track-adaptive-vt/ ------------------
_cand = [HERE.parent / "docs", HERE.parents[2] / "docs" if len(HERE.parents) >= 3 else HERE / "docs"]
DOCS = next((c for c in _cand if c.exists()), _cand[0])
OUTPUT = DOCS / "long-track-adaptive-vt" / "index.html"
STATE_JSON = DOCS / "long-track-adaptive-vt" / "state.json"
ALERT_FILE = DOCS.parent / "lt_adaptive_vt_alert.txt"

US_TICKERS = ["QQQ", "SMH"]
TW_TICKERS = ["0050", "2330"]
ALL_TICKERS = US_TICKERS + TW_TICKERS
YF_SYMBOL = {"QQQ": "QQQ", "SMH": "SMH", "0050": "0050.TW", "2330": "2330.TW"}
IS_TW = {"QQQ": False, "SMH": False, "0050": True, "2330": True}
TICKER_MARKET = {"QQQ": "美股", "SMH": "美股", "0050": "台股", "2330": "台股"}
WEIGHTS = {t: 0.5 for t in ALL_TICKERS}    # 每市場內兩腿各 50%，兩組合各自 100%
SIGMA_BASE = {"QQQ": 0.20, "SMH": 0.25,    # 固定 σ 版的 σ；本頁僅供對照顯示，套袖不使用
              "0050": 0.15, "2330": 0.25}
MED_WIN = 756                              # 自適應中位數視窗（3 年），凍結不再調整
MIN_PERIODS = 252                          # 首年 expanding
FREEZE_DATE = "2026-07-17"

BACKFILL_DAYS = 756                        # 回放窗（近三年交易日）
HISTORY_CAP = 820                          # state.json history 陣列上限（>756 留實錄餘裕）

# ---------------------------------------------------------------------------
# 回測摘要（results/vol_targeting/adaptive_sigma.json，2026-07-17 版）— 轉錄
# 每列：(label, cagr%, mdd%, calmar, ui, martin)
# ---------------------------------------------------------------------------
BT_US = {
    "window": "2005-01 – 2026-07",
    "verdict_pass": False,
    "rows": [
        ("自適應中位數 3y・含 10pp＋5% 取整執行層（本頁追蹤）", 11.59, -22.1, 0.5242, 7.87, 1.472),
        ("每日照調（理論・對照）", 11.51, -21.3, 0.5399, 7.95, 1.447),
        ("固定 σ 正式版・含執行層（對照）", 11.78, -21.9, 0.5384, 8.24, 1.431),
        ("純長軌（無套袖）", 12.36, -34.0, 0.3632, 9.77, 1.265),
        ("50/50 買進持有", 17.65, -56.9, 0.3100, 13.99, 1.262),
    ],
    "eras": [                              # (label, ΔCAGR vs 固定 σ, ΔMDD pp)
        ("2005-08 GFC", +0.3, +0.6), ("2009-13 QE", -0.1, +0.3),
        ("2014-18 低波", -2.3, +0.4), ("2019-23 COVID", -0.3, +3.8),
        ("2024- AI 牛", +1.8, -1.4),
    ],
}
BT_TW = {
    "window": "2014-01 – 2026-07",
    "verdict_pass": True,
    "rows": [
        ("自適應中位數 3y・含 10pp＋5% 取整執行層（本頁追蹤）", 18.53, -18.6, 0.9948, 8.41, 2.203),
        ("每日照調（理論・對照）", 18.53, -19.6, 0.9475, 8.60, 2.155),
        ("固定 σ 正式版・含執行層（對照）", 18.90, -20.9, 0.9036, 8.59, 2.201),
        ("純長軌（無套袖）", 21.40, -23.5, 0.9126, 9.38, 2.282),
        ("50/50 買進持有", 26.38, -39.5, 0.6683, 9.85, 2.677),
    ],
    "eras": [
        ("2014-16 陸股貶值/整理", -1.0, +1.2), ("2017-19 平順多頭", +0.4, +1.8),
        ("2020-22 COVID/升息", -0.0, +2.5), ("2023- AI 台積電牛", +0.8, -1.3),
    ],
}

# 單腿 2330 長窗（含 2008 GFC）附錄（adaptive_sigma.json leg_2330_long_window_appendix）
# 每列：(label, full_cagr%, full_mdd%, calmar, martin, gfc_mdd%, gfc_cagr%)
APPENDIX_2330 = {
    "window": "2005-06 – 2026-07",
    "rows": [
        ("固定 σ 正式版", 16.09, -34.8, 0.463, 1.151, -34.8, 2.09),
        ("自適應中位數 3y（本頁）", 15.94, -35.4, 0.451, 1.153, -35.4, 0.90),
        ("自適應中位數 5y", 15.51, -36.0, 0.431, 1.098, -36.0, 0.15),
        ("純長軌（無套袖）", 17.02, -38.6, 0.441, 1.097, -38.6, -0.86),
    ],
}

# 回測月度淨值（自適應中位數 3y 合成 vs 50/50 B&H，正規化 1.0；由 run_adaptive_sigma
# 的 build_market 的 configs 月度 NAV dump，靜態轉錄。美股 2005-01 起、台股 2014-01 起）。
BT_NAV_US = {
    "labels": ["2005-01","2005-02","2005-03","2005-04","2005-05","2005-06","2005-07","2005-08","2005-09","2005-10","2005-11","2005-12","2006-01","2006-02","2006-03","2006-04","2006-05","2006-06","2006-07","2006-08","2006-09","2006-10","2006-11","2006-12","2007-01","2007-02","2007-03","2007-04","2007-05","2007-06","2007-07","2007-08","2007-09","2007-10","2007-11","2007-12","2008-01","2008-02","2008-03","2008-04","2008-05","2008-06","2008-07","2008-08","2008-09","2008-10","2008-11","2008-12","2009-01","2009-02","2009-03","2009-04","2009-05","2009-06","2009-07","2009-08","2009-09","2009-10","2009-11","2009-12","2010-01","2010-02","2010-03","2010-04","2010-05","2010-06","2010-07","2010-08","2010-09","2010-10","2010-11","2010-12","2011-01","2011-02","2011-03","2011-04","2011-05","2011-06","2011-07","2011-08","2011-09","2011-10","2011-11","2011-12","2012-01","2012-02","2012-03","2012-04","2012-05","2012-06","2012-07","2012-08","2012-09","2012-10","2012-11","2012-12","2013-01","2013-02","2013-03","2013-04","2013-05","2013-06","2013-07","2013-08","2013-09","2013-10","2013-11","2013-12","2014-01","2014-02","2014-03","2014-04","2014-05","2014-06","2014-07","2014-08","2014-09","2014-10","2014-11","2014-12","2015-01","2015-02","2015-03","2015-04","2015-05","2015-06","2015-07","2015-08","2015-09","2015-10","2015-11","2015-12","2016-01","2016-02","2016-03","2016-04","2016-05","2016-06","2016-07","2016-08","2016-09","2016-10","2016-11","2016-12","2017-01","2017-02","2017-03","2017-04","2017-05","2017-06","2017-07","2017-08","2017-09","2017-10","2017-11","2017-12","2018-01","2018-02","2018-03","2018-04","2018-05","2018-06","2018-07","2018-08","2018-09","2018-10","2018-11","2018-12","2019-01","2019-02","2019-03","2019-04","2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12","2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12","2021-01","2021-02","2021-03","2021-04","2021-05","2021-06","2021-07","2021-08","2021-09","2021-10","2021-11","2021-12","2022-01","2022-02","2022-03","2022-04","2022-05","2022-06","2022-07","2022-08","2022-09","2022-10","2022-11","2022-12","2023-01","2023-02","2023-03","2023-04","2023-05","2023-06","2023-07","2023-08","2023-09","2023-10","2023-11","2023-12","2024-01","2024-02","2024-03","2024-04","2024-05","2024-06","2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12","2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07"],
    "combo": [1.0,1.0019,1.0043,1.0066,1.009,1.0116,1.0141,1.0173,1.0202,1.0233,1.0266,1.0299,1.0238,1.0147,1.0275,1.0285,0.9949,0.999,1.0029,1.0075,1.0159,1.0485,1.0687,1.0608,1.0742,1.0675,1.0726,1.1113,1.1305,1.1539,1.1489,1.1639,1.1893,1.1879,1.161,1.1631,1.1462,1.1482,1.1493,1.1506,1.1621,1.1358,1.1374,1.129,1.13,1.1307,1.1309,1.1309,1.131,1.1312,1.1314,1.1315,1.1317,1.1319,1.132,1.1322,1.1323,1.1323,1.1324,1.1324,1.1325,1.1325,1.1667,1.1801,1.1447,1.1149,1.1062,1.0821,1.1039,1.1387,1.138,1.165,1.1817,1.2005,1.2,1.2538,1.2327,1.1891,1.1631,1.0933,1.0806,1.085,1.0611,1.0392,1.0727,1.1067,1.1346,1.1283,1.0883,1.1085,1.1143,1.1431,1.1375,1.1073,1.102,1.0993,1.1195,1.1346,1.1568,1.1949,1.2343,1.2115,1.26,1.2345,1.3069,1.3573,1.3791,1.4296,1.3961,1.4705,1.4847,1.4618,1.5197,1.595,1.5928,1.6805,1.6647,1.6319,1.7199,1.6978,1.6548,1.7681,1.714,1.7296,1.8165,1.7136,1.7298,1.6231,1.6085,1.6317,1.642,1.5899,1.4872,1.4875,1.5175,1.4575,1.4796,1.4494,1.5405,1.5767,1.6275,1.6042,1.637,1.6581,1.7259,1.7804,1.8316,1.8541,1.9524,1.8901,1.9662,2.013,2.0586,2.1835,2.1903,2.1865,2.3607,2.3112,2.218,2.1772,2.2869,2.2566,2.3209,2.4187,2.3909,2.214,2.2043,2.2082,2.2126,2.2179,2.2867,2.44,2.2145,2.2324,2.2958,2.2284,2.2665,2.3809,2.4659,2.6122,2.6161,2.5502,2.3434,2.3599,2.4317,2.5442,2.7065,2.899,2.8092,2.765,3.1085,3.2515,3.3131,3.3945,3.4054,3.4365,3.4582,3.6374,3.6907,3.8107,3.6214,3.8602,4.0912,4.1224,3.7795,3.7377,3.6353,3.5498,3.5525,3.5567,3.5627,3.5711,3.5802,3.591,3.6032,3.6159,3.6288,3.5975,3.7833,3.675,3.9734,4.2087,4.4066,4.3143,4.0496,3.9237,4.4399,4.7777,4.9716,5.4496,5.662,5.4024,5.9012,6.3427,6.1496,6.0995,6.2556,6.1811,6.3367,6.3679,6.4435,6.2272,5.9707,5.9916,6.119,6.5773,6.7753,6.8264,7.4319,8.0267,7.8702,7.9344,8.4541,8.3897,7.8707,9.2681,10.4584,10.8036,10.5682],
    "bh": [1.0,1.0414,1.01,0.9616,1.0601,1.0313,1.1272,1.113,1.1194,1.0591,1.1518,1.1302,1.1628,1.1462,1.1475,1.1674,1.0691,1.0511,1.0066,1.0717,1.0997,1.121,1.1495,1.1238,1.1388,1.1393,1.1251,1.2109,1.2318,1.2573,1.2519,1.2716,1.3118,1.2911,1.205,1.2072,1.056,1.0382,1.0512,1.1274,1.1993,1.0867,1.0584,1.0775,0.9222,0.7779,0.6561,0.6836,0.6631,0.6372,0.7134,0.7941,0.8194,0.8388,0.9423,0.9588,0.9891,0.9466,1.0016,1.076,0.9803,1.035,1.1044,1.1393,1.0665,1.0056,1.0708,0.9819,1.1165,1.1883,1.2182,1.2761,1.331,1.3786,1.3527,1.4134,1.3895,1.3404,1.3111,1.2186,1.1763,1.3061,1.2668,1.2582,1.3753,1.4394,1.5031,1.4691,1.3425,1.3921,1.3995,1.4517,1.4286,1.3784,1.4086,1.427,1.4897,1.5101,1.5418,1.5945,1.6499,1.6173,1.6871,1.6525,1.7534,1.8254,1.8579,1.9285,1.8815,1.9867,2.0031,1.9794,2.0609,2.163,2.1601,2.279,2.2575,2.2957,2.44,2.4063,2.3398,2.5187,2.4529,2.4804,2.6049,2.4574,2.4571,2.3125,2.2947,2.5257,2.5709,2.5192,2.3487,2.3471,2.5358,2.4356,2.5918,2.5649,2.8029,2.8771,2.9799,2.9327,2.999,3.0412,3.1794,3.2907,3.3955,3.4416,3.6442,3.5144,3.6714,3.7682,3.8625,4.1225,4.1359,4.1271,4.4923,4.4644,4.326,4.1876,4.5221,4.4514,4.5849,4.7836,4.723,4.232,4.3019,3.943,4.3337,4.5498,4.7059,5.0555,4.4535,4.8943,5.1055,4.9993,5.125,5.4177,5.6436,5.9784,5.9874,5.6856,5.163,5.9185,6.278,6.7384,7.2841,7.8826,7.627,7.5272,8.6707,9.1203,9.3084,9.5976,9.7388,10.0145,10.0819,10.6627,10.8364,11.2248,10.6055,11.3826,12.1386,12.3221,11.1225,10.7297,11.0155,9.4532,9.6756,8.4303,9.6542,8.9471,7.8619,8.1089,9.1435,8.281,9.4178,9.4492,10.3702,10.0788,11.3194,11.9891,12.5526,12.2899,11.5362,11.178,12.6477,13.6092,14.1612,15.5222,16.1017,15.3645,16.7829,18.0381,17.4251,17.4084,17.7183,17.5133,17.9963,18.083,18.3491,17.698,16.2215,16.3392,18.191,20.2405,20.8494,21.0066,22.8691,24.6987,24.1468,24.3765,25.973,25.7687,24.43,30.221,34.5695,36.2044,34.699],
}
BT_NAV_TW = {
    "labels": ["2014-01","2014-02","2014-03","2014-04","2014-05","2014-06","2014-07","2014-08","2014-09","2014-10","2014-11","2014-12","2015-01","2015-02","2015-03","2015-04","2015-05","2015-06","2015-07","2015-08","2015-09","2015-10","2015-11","2015-12","2016-01","2016-02","2016-03","2016-04","2016-05","2016-06","2016-07","2016-08","2016-09","2016-10","2016-11","2016-12","2017-01","2017-02","2017-03","2017-04","2017-05","2017-06","2017-07","2017-08","2017-09","2017-10","2017-11","2017-12","2018-01","2018-02","2018-03","2018-04","2018-05","2018-06","2018-07","2018-08","2018-09","2018-10","2018-11","2018-12","2019-01","2019-02","2019-03","2019-04","2019-05","2019-06","2019-07","2019-08","2019-09","2019-10","2019-11","2019-12","2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12","2021-01","2021-02","2021-03","2021-04","2021-05","2021-06","2021-07","2021-08","2021-09","2021-10","2021-11","2021-12","2022-01","2022-02","2022-03","2022-04","2022-05","2022-06","2022-07","2022-08","2022-09","2022-10","2022-11","2022-12","2023-01","2023-02","2023-03","2023-04","2023-05","2023-06","2023-07","2023-08","2023-09","2023-10","2023-11","2023-12","2024-01","2024-02","2024-03","2024-04","2024-05","2024-06","2024-07","2024-08","2024-09","2024-10","2024-11","2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12","2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07"],
    "combo": [1.0,1.0157,1.0741,1.0823,1.1055,1.1631,1.1577,1.19,1.1374,1.2186,1.2784,1.2682,1.2713,1.3255,1.2967,1.3264,1.32,1.2998,1.2676,1.2136,1.2146,1.2112,1.1978,1.2143,1.1889,1.2118,1.2591,1.181,1.1966,1.2556,1.3184,1.3406,1.3814,1.4073,1.3754,1.3687,1.3952,1.4208,1.4259,1.4521,1.498,1.5741,1.6092,1.6306,1.6103,1.7392,1.6572,1.6681,1.7943,1.7328,1.7284,1.6328,1.6086,1.618,1.7307,1.7838,1.8031,1.6208,1.6155,1.6168,1.6182,1.6215,1.6198,1.702,1.5618,1.5819,1.6586,1.6486,1.7215,1.8558,1.8893,2.0298,1.9649,1.949,1.7155,1.7521,1.7298,1.837,2.2674,2.2532,2.2814,2.2746,2.5196,2.7471,3.0556,3.1225,3.0925,3.1867,3.0927,3.1046,3.0376,3.1749,3.0564,3.0688,3.1071,3.2407,3.2876,3.1899,3.1114,3.0339,3.0364,3.039,3.0415,3.0443,3.0468,3.0492,3.0519,3.0546,3.0561,3.0583,3.0611,3.0632,3.0659,3.0238,3.0164,2.9421,2.851,2.8483,3.0847,3.179,3.2874,3.5304,3.8036,3.7884,3.8665,4.399,4.2756,4.2435,4.3288,4.5157,4.3834,4.6663,4.8897,4.6248,4.1237,4.127,4.1103,4.2845,4.6447,4.6884,5.2296,5.9354,5.6683,6.0194,6.7874,7.5679,6.8691,7.9495,8.6647,8.8373,8.5563],
    "bh": [1.0,1.0205,1.0854,1.0937,1.1172,1.1753,1.1699,1.206,1.1527,1.2653,1.3398,1.3313,1.3434,1.4115,1.376,1.4074,1.3993,1.3779,1.3408,1.2522,1.2587,1.3183,1.3094,1.3234,1.3046,1.3571,1.454,1.3659,1.4127,1.4942,1.5854,1.614,1.6664,1.7063,1.6709,1.6654,1.7013,1.7358,1.7425,1.778,1.8402,1.9437,1.9918,2.0208,1.9927,2.1702,2.0567,2.0717,2.2457,2.1758,2.1827,2.061,2.0572,2.0682,2.2694,2.3346,2.3639,2.1092,2.0602,2.0436,2.039,2.1672,2.2179,2.3303,2.1633,2.2502,2.3827,2.3669,2.4755,2.6766,2.7267,2.9351,2.8249,2.787,2.4175,2.7011,2.6291,2.8199,3.5482,3.5185,3.5761,3.5722,3.9517,4.3221,4.7258,4.882,4.8395,4.9986,4.9241,4.9597,4.8528,5.072,4.8828,4.9028,4.9678,5.1944,5.2682,5.0789,5.0551,4.634,4.7476,4.1458,4.3629,4.343,3.7348,3.5149,4.272,3.9892,4.5102,4.4725,4.6343,4.4195,4.8308,4.9772,4.9602,4.8306,4.6709,4.6692,5.0781,5.2415,5.4353,5.8851,6.5663,6.636,6.9295,7.9825,7.7514,7.8048,7.933,8.4057,8.1683,8.6954,9.1242,8.5425,7.5887,7.4903,7.9832,8.6929,9.423,9.5117,10.609,12.04,11.5783,12.3438,13.9957,15.6888,13.9375,17.1716,19.4701,19.9497,18.9252],
}

# 市場定義（渲染與資料處理共用）
MARKETS = [
    {"key": "us", "name": "美股 QQQ + SMH", "short": "QQQ+SMH",
     "legs": US_TICKERS, "hist_key": "history_us", "bt": BT_US, "bt_nav": BT_NAV_US},
    {"key": "tw", "name": "台股 0050 + 2330", "short": "0050+2330",
     "legs": TW_TICKERS, "hist_key": "history_tw", "bt": BT_TW, "bt_nav": BT_NAV_TW},
]
MKT = {m["key"]: m for m in MARKETS}


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
    return repair_phantom_splits(c) if IS_TW[ticker] else c


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
# Sleeve — adaptive median (verbatim port of
#          run_adaptive_sigma.vt_weight_adaptive_median with n_days=756)
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


def sleeve_state(px: pd.Series) -> dict:
    rv_now, sig_now, w = _sleeve_from(px)
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
def _daily_record(px_map: dict, legs: list, d: pd.Timestamp, source: str) -> dict:
    """One market's one-day target weights, computed byte-identically to the
    live path: gate = _gate_core(px[:d]).pos.iloc[-1]；sleeve = adaptive median
    on px[:d]. source ∈ {'replay','live'}. Records sigma_t_pct per leg."""
    rec = {"date": d.strftime("%Y-%m-%d"), "source": source, "tickers": {}}
    combined = 0.0
    for t in legs:
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


def build_backfill(px_map: dict, legs: list, n_days: int = BACKFILL_DAYS) -> list:
    """Replay the exact daily rule over the last n_days common trading days of
    this market's legs. Every record is marked source='replay'."""
    common = None
    for t in legs:
        common = px_map[t].index if common is None else common.intersection(px_map[t].index)
    dates = common.sort_values()[-n_days:]
    return [_daily_record(px_map, legs, d, "replay") for d in dates]


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
# 每市場各自從 history 確定性重放（history_us／history_tw），冪等可重現。
# band／grid 以組合 pp 為單位（每腿滿載＝50 pp）。
# ---------------------------------------------------------------------------
def band_exec_replay(history: list, legs: list) -> dict:
    """對每腿的最終權重（組合 pp）重放執行層：executed 初始 0，逐日若
    |target − executed| ≥ 10pp 則 executed = round(target/5)×5，否則不變。
    回傳每腿每日 executed、組合合計、事件清單（日期、腿、from→to、原因＝該日
    閘門翻轉則「閘門翻轉」否則「波動調整」、當日組合執行曝險）與各腿當前值。"""
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


def events_card(mkt: dict, events: list) -> str:
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
<h3>{mkt['short']} 近三年執行層訊號變化事件（10pp 門檻＋5% 取整）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
只有當某腿目標與現持差 ≥ 10pp 才調整（取整到 5% 格），故事件遠少於每日微調。倒序全列；「變化」為該腿最終權重（組合 pp，滿載 50%）；原因＝當日閘門翻轉則「閘門翻轉」否則「波動調整」。</p>
<table><thead><tr><th>日期</th><th>腿</th><th>變化</th><th>原因</th><th class="num">當日組合執行曝險</th></tr></thead>
<tbody>{body}</tbody></table>
</div>"""


# ---------------------------------------------------------------------------
# HTML helpers
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
    rv = d["rv20"] * 100
    sig = d["sigma_t"] * 100
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
      <div class="sig-detail">RV20（20日年化波動）<b>{rv:.1f}%</b> vs σ_t <b>{sig:.1f}%</b>（σ目標＝近 3 年 RV20 中位數，動態）
        → w = min(1, {sig:.1f}%／{rv:.1f}%) = <b>{d['sleeve']:.2f}</b>
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


def backtest_section(mkt: dict) -> str:
    bt = mkt["bt"]
    rows = ""
    for lab, cagr, mdd, calmar, ui, martin in bt["rows"]:
        hl = ("rowhl" if "自適應中位數 3y" in lab else
              ("rowbh" if "買進持有" in lab else ""))
        rows += (f'<tr class="{hl}"><td>{lab}</td><td class="num">{cagr:.2f}%</td>'
                 f'<td class="num">{mdd:.1f}%</td><td class="num">{calmar:.3f}</td>'
                 f'<td class="num">{ui:.2f}</td><td class="num">{martin:.2f}</td></tr>\n')
    eras = ""
    for lab, dc, dm in bt["eras"]:
        cc = "pos" if dc >= 0 else "neg"
        cm = "pos" if dm >= 0 else "neg"
        eras += (f'<tr><td>{lab}</td><td class="num {cc}">{dc:+.1f}pp</td>'
                 f'<td class="num {cm}">{dm:+.1f}pp</td></tr>\n')
    if mkt["key"] == "tw":
        take = ('<b>台股版判定＝過關</b>：主列（含執行層）vs 固定 σ 正式版（同含執行層）'
                'Calmar 0.904 → <b>0.995</b>、Martin 2.20 ≈ 2.20，MDD −20.9% → <b>−18.6%</b>，'
                'CAGR 幾乎不變。每日照調理論版 Calmar 0.948，執行層對台股自適應再加值（0.948 → 0.995）。'
                '每日照調基準的四分期 MDD 三期改善、AI 台積電牛僅微惡化（−1.3pp）。regime 中位數隨波動抬升，'
                '讓結構性高波的 2330 在多頭段少欠載，同時保留深回撤時的減碼。')
    else:
        take = ('<b>美股版判定＝雜訊級平手（FAIL）</b>：主列（含執行層）vs 固定 σ 正式版（同含執行層）'
                'Calmar 0.538 → 0.524、Martin 1.43 → 1.47，差距在四捨五入級、互有高低——'
                '<b>FAIL 的意思是「無證據值得替換固定 σ」，不是「更差」</b>。每日照調理論版 Calmar 0.540，'
                '執行層對美股自適應略有折損（0.540 → 0.524）。每日照調基準的五分期 MDD 四期改善、'
                '低波段 CAGR 代價 −2.3pp（regime 中位數在長期低波時被壓低、減碼偏保守）。'
                '與台股過關並置＝同一機制、兩市場、兩個相反判定，正是本頁前瞻追蹤要檢驗的。')
    return f"""<div class="card">
<h3>回測摘要 — {mkt['short']}（自適應中位數 3y vs 固定 σ 正式版・共同窗 {bt['window']}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
兩標的日報酬 50/50 加權合成（等效每日再平衡，如實揭露）。判準基準＝<b>固定 σ 正式版</b>（本頁與固定 σ 版的差異只在套袖，閘門完全相同）。<b>主列與固定 σ 對照列皆含 10pp＋5% 取整執行層</b>（與追蹤操作同規則，apples-to-apples）；「每日照調」為理論對照。
含執行層數字轉錄自 results/vol_targeting/band_exec.json，每日照調數字自 adaptive_sigma.json。</p>
<table><thead><tr><th>配置</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Calmar</th><th class="num">Ulcer</th><th class="num">Martin</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="takeaway">{take}</div>
</div>

<div class="card">
<h3>分期（{mkt['short']} 自適應中位數 3y vs 固定 σ・每日照調；ΔCAGR／ΔMDD，正＝自適應較優）</h3>
<table><thead><tr><th>期間</th><th class="num">Δ CAGR</th><th class="num">Δ MDD</th></tr></thead>
<tbody>{eras}</tbody></table>
<div style="font-size:.75rem;color:var(--muted);margin-top:.5rem">ΔMDD 正值＝自適應回撤較淺；ΔCAGR 正值＝自適應報酬較高。與固定 σ 對照，非與買進持有對照。</div>
</div>"""


def appendix_2330_section() -> str:
    ap = APPENDIX_2330
    rows = ""
    for lab, fc, fm, cal, mar, gm, gc in ap["rows"]:
        hl = ' class="rowhl"' if "本頁" in lab else ""
        rows += (f'<tr{hl}><td>{lab}</td><td class="num">{fc:.2f}%</td>'
                 f'<td class="num">{fm:.1f}%</td><td class="num">{cal:.3f}</td>'
                 f'<td class="num">{mar:.2f}</td><td class="num">{gm:.1f}%</td>'
                 f'<td class="num">{gc:.2f}%</td></tr>\n')
    return f"""<div class="card">
<h3>附錄 — 單腿 2330 長窗（含 2008 GFC）：深熊由誰扛？（窗 {ap['window']}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
台股正式窗自 2014 起（0050 免費歷史限制）不含深熊。2330 有 2005 起資料，單腿拉長把 2008 GFC 收進來，
檢驗含崩盤樣本時自適應 σ 相對固定 σ 的行為、以及深熊保護由 W52 閘門（純長軌）扛的比重。</p>
<table><thead><tr><th>配置</th><th class="num">全窗 CAGR</th><th class="num">全窗 MDD</th><th class="num">Calmar</th><th class="num">Martin</th><th class="num">GFC MDD</th><th class="num">GFC CAGR</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="takeaway">GFC 段三配置 MDD 都在 −35% 上下、自適應略深於固定 σ（−34.8% → −35.4%）——
深熊保護主要是 <b>W52 週線閘門（純長軌）</b>扛的（純長軌 GFC MDD −38.6%，套袖只再削 3～4pp），
套袖不論固定或自適應都不是深熊的主要防線。自適應 σ 在崩盤群聚期「regime 中位數升高 → 減碼比固定 σ 少」的
預期代價，在此如實顯現：GFC 段 CAGR 2.09% → 0.90%。</div>
</div>"""


# ---------------------------------------------------------------------------
# per-market render (html block + chart JS)
# ---------------------------------------------------------------------------
def _market_data(mkt: dict, sigs: dict, history: list, exec_replay: dict) -> dict:
    legs = mkt["legs"]
    a, b = legs[0], legs[1]

    def _col(fn):
        return json.dumps([fn(r) for r in history], separators=(",", ":"))
    H = {
        "labels": _col(lambda r: r["date"]),
        "comb": _col(lambda r: r["combined_pct"]),
        "a": _col(lambda r: r["tickers"][a]["final_pct"]),
        "b": _col(lambda r: r["tickers"][b]["final_pct"]),
        "arv": _col(lambda r: r["tickers"][a]["rv20_pct"]),
        "brv": _col(lambda r: r["tickers"][b]["rv20_pct"]),
        "asig": _col(lambda r: r["tickers"][a]["sigma_t_pct"]),
        "bsig": _col(lambda r: r["tickers"][b]["sigma_t_pct"]),
        "src": _col(lambda r: r["source"]),
        # executed layer (10pp band + 5% round) — deterministic replay
        "cexe": json.dumps(exec_replay["combined"], separators=(",", ":")),
        "aexe": json.dumps(exec_replay["executed"].get(a, []), separators=(",", ":")),
        "bexe": json.dumps(exec_replay["executed"].get(b, []), separators=(",", ":")),
    }
    combined = sum(sigs[t]["final"] for t in legs) * 100
    ccol = fill_color(combined / 100)
    slot = {t: WEIGHTS[t] * 100 for t in legs}
    finals = [round(sigs[t]["final"] * 100, 1) for t in legs]
    gate_cut = [round(slot[t] if not sigs[t]["gate"] else 0.0, 1) for t in legs]
    sleeve_cut = [round(slot[t] - finals[i] - gate_cut[i], 1) for i, t in enumerate(legs)]
    n_replay = sum(1 for r in history if r["source"] == "replay")
    n_live = sum(1 for r in history if r["source"] == "live")
    span = (f"{history[0]['date']} → {history[-1]['date']}" if history else "—")
    return {
        "legs": legs, "a": a, "b": b, "combined": combined, "ccol": ccol,
        "finals": finals,
        "C_FINALS": json.dumps(finals, separators=(",", ":")),
        "C_SLEEVE": json.dumps(sleeve_cut, separators=(",", ":")),
        "C_GATE": json.dumps(gate_cut, separators=(",", ":")),
        "H": H, "n_replay": n_replay, "n_live": n_live, "span": span,
        "nhist": len(history), "events": exec_replay["events"],
        "BT_L": json.dumps(mkt["bt_nav"]["labels"], separators=(",", ":")),
        "BT_C": json.dumps(mkt["bt_nav"]["combo"], separators=(",", ":")),
        "BT_B": json.dumps(mkt["bt_nav"]["bh"], separators=(",", ":")),
    }


def market_html(mkt: dict, sigs: dict, md: dict) -> str:
    legs = mkt["legs"]
    combined = md["combined"]
    ccol = md["ccol"]
    finals = md["finals"]
    suf = mkt["key"]
    cards = "".join(ticker_card(t, sigs[t]) for t in legs)
    return f"""<div class="mkt-hd"><span class="mkt-tag">{mkt['name']}</span></div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>{mkt['short']} 組合當前目標曝險</span></div>
  <div class="status-exposure">{combined:.0f}%</div>
  <div style="font-size:.8rem;color:var(--muted)">0.5 × 閘門 × 套袖，兩標的相加 · 閒置部分持現金 · 此組合獨立追蹤（100%）</div>
</div>

<div class="card">
<h3>{mkt['short']} 當前部位視覺 — 合成曝險量表 × 每腿乘法鏈</h3>
<div class="viz-split">
  <div>
    <div class="gauge-box">
      <canvas id="chart-gauge-{suf}"></canvas>
      <div class="gauge-center"><div class="g-num hero-{ccol}" style="color:var(--{ccol})">{combined:.0f}%</div><div class="g-lab">合成目標曝險（0～100%）</div></div>
    </div>
  </div>
  <div>
    <div class="chart-wrap-xs"><canvas id="chart-chain-{suf}"></canvas></div>
  </div>
</div>
<div style="font-size:.76rem;color:var(--muted);margin-top:.7rem">每腿 50% 額度＝<b style="color:var(--text)">最終持有</b> ＋ <b style="color:var(--amber-text)">套袖折減</b>（高波減碼）＋ <b>閘門關閉</b>（出場歸零）。{legs[0]} 最終 {finals[0]:.0f}%、{legs[1]} 最終 {finals[1]:.0f}%。</div>
</div>

<div class="card">
<h3>{mkt['short']} 近三年權重時間軸 — 執行層持股率 ＋ 每日理論目標</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
<b style="color:var(--text)">粗階梯線＝10pp 門檻＋5% 取整的實際執行持股率</b>（跨門檻才動、取整到 5% 格）；<b>細線＝每日理論目標</b>（未過門檻）。
線段<b>實線＝每日實錄</b>（CI 逐日追加），<b>虛線＝規則回放</b>（首次生成時以完全相同的規則往回重算，非當日實錄，誠實區隔）。
窗 {md['span']}，共 {md['nhist']} 個交易日（回放 {md['n_replay']}／實錄 {md['n_live']}）。</p>
<div class="chart-wrap"><canvas id="chart-weights-{suf}"></canvas></div>
<div class="legend-note">
  <span class="ln-item"><span class="ln-line" style="border-top-width:3px"></span>執行層（粗階梯）</span>
  <span class="ln-item"><span class="ln-line" style="border-top-color:rgba(120,120,120,.5)"></span>每日理論目標（細）</span>
  <span class="ln-item"><span class="ln-line"></span>每日實錄</span>
  <span class="ln-item"><span class="ln-line ln-dash"></span>規則回放</span>
</div>
<h3 style="margin-top:1.1rem">{mkt['short']} 套袖觸發脈絡 — RV20 vs σ_t（動態）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
本頁 σ_t 是<b>動態線</b>（近 3 年 RV20 滾動中位數），不是固定 σ 版的水平虛線。當 RV20（實線）升破自身 σ_t（虛線）時套袖按比例減碼；RV20 ≤ σ_t 時滿載。regime 抬升時 σ_t 跟著上移，是這頁與固定 σ 版的唯一機制差異。</p>
<div class="chart-wrap-sm"><canvas id="chart-rv-{suf}"></canvas></div>
</div>

{events_card(mkt, md['events'])}

<div class="tgrid">{cards}</div>

<div class="card">
<h3>{mkt['short']} 回測縮圖 — 自適應中位數 3y（含執行層）vs 50/50 B&amp;H（對數淨值＋回撤）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
回測快照（{mkt['bt_nav']['labels'][0]} → {mkt['bt_nav']['labels'][-1]}）。淨值線＝<b>自適應中位數 3y（含 10pp 門檻＋5% 取整執行層，與追蹤操作同規則）</b>，由 run_band_exec_ablation 月度 NAV 靜態轉錄；B&amp;H 線不變。</p>
<div class="grid2">
  <div class="chart-wrap-sm"><canvas id="chart-bt-nav-{suf}"></canvas></div>
  <div class="chart-wrap-sm"><canvas id="chart-bt-dd-{suf}"></canvas></div>
</div>
</div>

{"".join(recent_table(t, sigs[t]) for t in legs)}

{backtest_section(mkt)}
"""


def market_js(mkt: dict, md: dict) -> str:
    suf = mkt["key"]
    legs = mkt["legs"]
    combined = md["combined"]
    ccol = md["ccol"]
    CCOL_HEX = {"green": "#16a34a", "blue": "#1d4ed8",
                "amber": "#a16207", "red": "#b91c1c"}[ccol]
    H = md["H"]
    return f"""
// ===== market: {suf} =====
new Chart(document.getElementById('chart-gauge-{suf}'),{{
  type:'doughnut',
  data:{{labels:['曝險','現金'],datasets:[{{data:[{combined:.1f},{100-combined:.1f}],
    backgroundColor:['{CCOL_HEX}','#ece7db'],borderWidth:0}}]}},
  options:{{rotation:-90,circumference:180,cutout:'72%',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:function(c){{return c.label+': '+c.parsed.toFixed(1)+'%'}}}}}}}}}}
}});

new Chart(document.getElementById('chart-chain-{suf}'),{{
  type:'bar',
  data:{{labels:['{legs[0]} 腿（50%）','{legs[1]} 腿（50%）'],datasets:[
    {{label:'最終持有',data:{md['C_FINALS']},backgroundColor:[GREEN,AMBER],borderWidth:0,stack:'s'}},
    {{label:'套袖折減',data:{md['C_SLEEVE']},backgroundColor:'rgba(161,98,7,0.28)',borderWidth:0,stack:'s'}},
    {{label:'閘門關閉',data:{md['C_GATE']},backgroundColor:'rgba(120,120,120,0.22)',borderWidth:0,stack:'s'}}
  ]}},
  options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:true,position:'bottom',labels:{{usePointStyle:true,pointStyle:'rect',padding:10,boxWidth:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.x.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{stacked:true,min:0,max:50,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}}}}}},
      y:{{stacked:true,grid:{{display:false}}}}}}
  }}
}});

var W_LAB_{suf}={H['labels']},W_SRC_{suf}={H['src']};
function segDash_{suf}(ctx){{return W_SRC_{suf}[ctx.p1DataIndex]==='live'?undefined:[3,3];}}
new Chart(document.getElementById('chart-weights-{suf}'),{{
  type:'line',
  data:{{labels:W_LAB_{suf},datasets:[
    {{label:'合成執行',data:{H['cexe']},borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.09)',
     borderWidth:2.8,stepped:true,pointRadius:0,pointHoverRadius:3,fill:'origin',segment:{{borderDash:segDash_{suf}}}}},
    {{label:'{legs[0]} 執行',data:{H['aexe']},borderColor:BLUE,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash_{suf}}}}},
    {{label:'{legs[1]} 執行',data:{H['bexe']},borderColor:AMBER,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash_{suf}}}}},
    {{label:'合成目標（理論）',data:{H['comb']},borderColor:'rgba(22,163,74,0.40)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}},
    {{label:'{legs[0]} 目標',data:{H['a']},borderColor:'rgba(21,101,192,0.35)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}},
    {{label:'{legs[1]} 目標',data:{H['b']},borderColor:'rgba(217,119,6,0.35)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{title:function(c){{return c[0].label+' · '+(W_SRC_{suf}[c[0].dataIndex]==='live'?'每日實錄':'規則回放')}},
        label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{min:0,max:100,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});

new Chart(document.getElementById('chart-rv-{suf}'),{{
  type:'line',
  data:{{labels:W_LAB_{suf},datasets:[
    {{label:'{legs[0]} RV20',data:{H['arv']},borderColor:BLUE,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{legs[1]} RV20',data:{H['brv']},borderColor:AMBER,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{legs[0]} σ_t（動態）',data:{H['asig']},borderColor:'rgba(21,101,192,0.55)',borderWidth:1.4,borderDash:[6,4],pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{legs[1]} σ_t（動態）',data:{H['bsig']},borderColor:'rgba(217,119,6,0.55)',borderWidth:1.4,borderDash:[6,4],pointRadius:0,pointHoverRadius:3,tension:0.15}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{beginAtZero:true,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});

var BT_LAB_{suf}={md['BT_L']},BT_C_{suf}={md['BT_C']},BT_B_{suf}={md['BT_B']};
new Chart(document.getElementById('chart-bt-nav-{suf}'),{{
  type:'line',
  data:{{labels:BT_LAB_{suf},datasets:[
    {{label:'自適應中位數 3y（含執行層）',data:BT_C_{suf},borderColor:GREEN,borderWidth:2,pointRadius:0,pointHoverRadius:3,tension:0.1}},
    {{label:'50/50 B&H',data:BT_B_{suf},borderColor:BLUE,borderWidth:1.3,borderDash:[6,3],pointRadius:0,pointHoverRadius:3,tension:0.1}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(2)+'×'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:8,font:{{size:9}},maxRotation:0,autoSkip:true}}}},
      y:{{type:'logarithmic',grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'×'}},font:{{size:9}}}}}}}}
  }}
}});
new Chart(document.getElementById('chart-bt-dd-{suf}'),{{
  type:'line',
  data:{{labels:BT_LAB_{suf},datasets:[
    {{label:'自適應中位數 3y（含執行層）',data:_dd(BT_C_{suf}),borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.12)',borderWidth:1.4,fill:'origin',pointRadius:0,tension:0.1}},
    {{label:'50/50 B&H',data:_dd(BT_B_{suf}),borderColor:BLUE,backgroundColor:'rgba(21,101,192,0.06)',borderWidth:1.1,fill:'origin',pointRadius:0,tension:0.1}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:8,font:{{size:9}},maxRotation:0,autoSkip:true}}}},
      y:{{grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:9}}}}}}}}
  }}
}});
"""


# ---------------------------------------------------------------------------
# Full HTML
# ---------------------------------------------------------------------------
def generate_html(sigs: dict, changes: list | None, last_change_date: str | None,
                  hist_map: dict, exec_map: dict) -> str:
    changes = changes or []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    data_date = max(sigs[t]["wk_date"] for t in ALL_TICKERS)

    md_map = {m["key"]: _market_data(m, sigs, hist_map.get(m["key"], []), exec_map[m["key"]]) for m in MARKETS}
    exp_us = md_map["us"]["combined"]
    exp_tw = md_map["tw"]["combined"]

    change_html = (
        ('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;'
         'padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">'
         '可行動變化</b><br>' + "<br>".join(changes) +
         '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>')
        if changes else
        ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">'
         '無可行動變化（四腿閘門未翻轉、且無標的目標與現持差 ≥ 10pp）' +
         (f'（上次變化：{last_change_date}）' if last_change_date else '') + '</div>'))

    markets_html = "\n".join(market_html(m, sigs, md_map[m["key"]]) for m in MARKETS)
    markets_js = "\n".join(market_js(m, md_map[m["key"]]) for m in MARKETS)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>自適應 σ 長線 × 波動率目標（美+台）｜前瞻 OOS 追蹤 | InvestMQuest Research</title>
  <meta name="description" content="美股 QQQ+SMH ＋ 台股 0050+2330 · 週線長軌閘門 × 自適應 σ 波動率套袖（近 3 年 RV20 中位數）· 固定 vs 自適應 前瞻 OOS 對照（未採用）">
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
.mkt-hd{{margin:1.6rem 0 .8rem;border-bottom:2px solid var(--brand);padding-bottom:.4rem}}
.mkt-tag{{font-family:var(--serif);font-size:1.15rem;font-weight:700;color:var(--brand)}}
.status-hero{{padding:1.4rem 0 1rem;text-align:center}}
.status-badge{{display:inline-flex;align-items:center;gap:.75rem;padding:.8rem 2rem;border-radius:var(--r);font-size:1.15rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.5rem}}
.status-badge .dot{{width:14px;height:14px;border-radius:50%;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.status-exposure{{font-size:2.4rem;font-weight:800;margin:.3rem 0}}
.status-date{{font-size:.8rem;color:var(--muted)}}
.hero-green .status-badge{{background:var(--green-bg);color:var(--green-text);border:2px solid var(--green-border)}}
.hero-green .dot{{background:var(--green)}}.hero-green .status-exposure{{color:var(--green)}}
.hero-blue .status-badge{{background:var(--blue-bg);color:var(--blue-text);border:2px solid var(--blue-border)}}
.hero-blue .dot{{background:var(--blue)}}.hero-blue .status-exposure{{color:var(--blue)}}
.hero-amber .status-badge{{background:var(--amber-bg);color:var(--amber-text);border:2px solid var(--amber-border)}}
.hero-amber .dot{{background:var(--amber)}}.hero-amber .status-exposure{{color:var(--amber)}}
.hero-red .status-badge{{background:var(--red-bg);color:var(--red-text);border:2px solid var(--red-border)}}
.hero-red .dot{{background:var(--red)}}.hero-red .status-exposure{{color:var(--red)}}
.dual-stat{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}}
.dual-stat .ds{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1rem 1.2rem;text-align:center;box-shadow:var(--sh-1)}}
.dual-stat .ds .dsn{{font-size:1.9rem;font-weight:800;letter-spacing:-.02em}}
.dual-stat .ds .dsl{{font-size:.76rem;color:var(--muted);margin-top:.2rem}}
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
  .viz-split{{grid-template-columns:1fr}}.grid2{{grid-template-columns:1fr}}.dual-stat{{grid-template-columns:1fr}}.chart-wrap{{height:320px}}}}
</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / 自適應 σ 長線 × 波動率目標（美+台）</div>
    <h1>自適應 σ 長線 × 波動率目標 — 前瞻 OOS 追蹤</h1>
    <div class="sub">美股 QQQ+SMH ＋ 台股 0050+2330 · 週線長軌閘門 × 自適應 σ 套袖（σ_t＝近 3 年 RV20 中位數）· Long only · 固定 vs 自適應 對照（未採用）</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem;flex-wrap:wrap">
      <a href="/long-track-adaptive-vt/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">自適應美台總覽（本頁）</a>
      <a href="/long-track-qs-vt/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">QQQ+SMH 波動率（固定 σ）</a>
      <a href="/long-track-qs-vt/adaptive.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">自適應 σ 版美股子頁</a>
      <a href="/long-track-tw-vt/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">0050+2330 波動率（固定 σ）</a>
      <a href="/backtest/vol_targeting/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">波動率目標回測</a>
    </div>
  </div>
</div>
<div class="container">

<div class="oos-banner">
  <span class="tag-loud">固定 vs 自適應・並行 OOS 對照實驗・未採用（PAPER TRACKING）</span>
  <div style="font-size:.86rem">這<b>不是實盤系統</b>，是把一組<b>{FREEZE_DATE} 定案的自適應 σ 規則</b>往前逐日記錄，與兩個<b>固定 σ</b> 追蹤頁（<a href="/long-track-qs-vt/">QQQ+SMH</a>／<a href="/long-track-tw-vt/">0050+2330</a>）並跑，
  在 2027-01 複審時拿到「固定 vs 自適應」真實 OOS 對照。與固定 σ 版的<b>唯一差異</b>是套袖：σ_t＝近 3 年 RV20 滾動中位數（動態），閘門與其他一切照舊。規則定案後不再調整、不再調參。
  <br><br><b>研究判定（回測，非採用理由）：台股過關</b>（自適應中位數 3y／5y 兩窗同向、Calmar 0.863 → 0.948、Martin 2.05 → 2.16）；<b>美股雜訊級平手（FAIL）</b>（Calmar 0.547 → 0.540、Martin 1.45 → 1.45，<b>FAIL＝無證據值得替換固定 σ，不是更差</b>）。
  同一機制、兩市場、兩個相反判定，正是本頁要在樣本外檢驗的。<b>複審條件：2027-01 或滿 120 個追蹤交易日</b>後，與 <a href="/long-track-qs-vt/">/long-track-qs-vt/</a>、<a href="/long-track-tw-vt/">/long-track-tw-vt/</a> 並讀。</div>
</div>

<div class="dual-stat">
  <div class="ds"><div class="dsn hero-{md_map['us']['ccol']}" style="color:var(--{md_map['us']['ccol']})">{exp_us:.0f}%</div><div class="dsl">美股 QQQ+SMH 組合目標曝險</div></div>
  <div class="ds"><div class="dsn hero-{md_map['tw']['ccol']}" style="color:var(--{md_map['tw']['ccol']})">{exp_tw:.0f}%</div><div class="dsl">台股 0050+2330 組合目標曝險</div></div>
</div>
<div class="status-date" style="text-align:center;margin-bottom:.5rem">數據截至 {data_date}（週五收盤）· 頁面更新 {now} · 兩組合各自獨立追蹤（各 100%）</div>

{change_html}

{markets_html}

<div class="card">
<h3>正式追蹤版規則（{FREEZE_DATE} 定案，此後不再調整）</h3>
<div class="rule-list">
① <b>四腿、兩市場</b>：美股 {{QQQ, SMH}} 各 50%、台股 {{0050, 2330}} 各 50%（.TW，內嵌幻影分割修復）。兩組合各自獨立追蹤（各 100%），日報酬 50/50 加權合成（<b>絕不直接相加 equity curve</b>）。<br>
② <b>週線長軌閘門</b>（W-FRI）：進場＝週收盤 &gt; W52／W104／W250 且 W104／W250 四週斜率 &gt; 0（score5）；出場＝一根週收盤 &lt; W52；<b>長多 only</b>，閘門輸出 0／1。<b>與固定 σ 版完全相同。</b><br>
③ <b>自適應波動率套袖（本頁唯一與固定 σ 版不同處，凍結 {FREEZE_DATE}）</b>：σ_t＝RV20 的 <b>rolling(756, min_periods=252).median()</b>（近 3 年 RV20 中位數，首年 expanding）；w = min(1, σ_t／RV20)，RV20＝20 日對數報酬年化波動；<b>只降不加</b>（上限 1.0）。語義＝相對自身 regime 的尖峰偵測器，非固定的絕對風險預算。<br>
④ <b>機制與視窗凍結</b>：滾動中位數 3 年（756／252）鎖死，<b>此後不再調整</b>；不掃 N 擇優、不改機制形狀。固定 σ 對照值（QQQ 20%／SMH 25%／0050 15%／2330 25%）僅供卡片顯示，套袖不使用。<br>
⑤ <b>執行</b>：t 收盤訊號、t+1 收盤生效；成本 7 bps／邊。<br>
⑥ <b>最終權重</b> = 0.5 × 閘門(0/1) × 套袖權重，每市場兩腿各自計算。<br>
⑦ <b>資料揭露</b>：yfinance auto-adjust（還原股價）；0050.TW 2014-01-02 幻影分割壞 bar 由腳本自動修復（回溯縮放，門檻單日 ±40%，台股漲跌停 ±10% 不可能誤觸）；0050 免費歷史約 2009 起。台股 2330 佔 0050 約五成，50/50 組合等效台積電曝險 ≈ 75%，非分散組合。<br>
⑧ <b>執行層（{FREEZE_DATE} 與規則同日凍結）</b>：|目標 − 現持| ≥ 10pp 才調整，調整取整至 5% 格；<b>回測主數字含此執行層</b>，與追蹤操作同規則（兩市場各自獨立重放）。<br>
<span style="color:var(--muted);font-size:.78rem">閘門為週頻（僅週五可能翻轉），套袖 RV20／σ_t 為日頻（每日可能微調），故本頁每交易日更新（台股收盤後、美股收盤後各一次，date-keyed 冪等）。「可行動變化」＝任一腿閘門翻轉，或今日目標與現持（執行層 executed）差 ≥ 10pp，觸發 email 通知（訊息標市場前綴、顯示取整後的建議動作）。</span>
</div>
</div>

{appendix_2330_section()}

<div class="card">
<h3>複審條件</h3>
<div class="rule-list" style="font-size:.82rem">
於 <b>2027-01</b> 或滿 <b>120 個追蹤交易日</b>後，把本頁前瞻 OOS 的 CAGR／MDD／Calmar 與兩個固定 σ 版（<a href="/long-track-qs-vt/">QQQ+SMH</a>／<a href="/long-track-tw-vt/">0050+2330</a>）逐市場對照：<br>
• <b>台股</b>：回測判定自適應過關。若 OOS 也顯示自適應 Calmar／Martin 不劣於固定 σ，則「自適應值得」獲得樣本外支持，進入 charter 採用討論；若 OOS 反轉（自適應反而較差），則記錄為「回測過關但樣本外不穩健」。<br>
• <b>美股</b>：回測判定雜訊級平手（FAIL＝無證據值得替換）。前瞻若持續平手，維持固定 σ；若自適應在真實 OOS 明顯勝出，才重新檢視。<br>
<b>在此之前本頁純為研究追蹤，不構成任何倉位建議。</b>兩固定 σ 版與本頁三頁並讀，才是「固定 vs 自適應」的完整對照。
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research · 自適應 σ 長線 × 波動率目標（美+台，前瞻 OOS 對照・未採用）</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
<script>
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;
var GREEN="#16a34a",BLUE="#1565c0",AMBER="#d97706";
function _dd(nav){{var dd=[],pk=0;for(var i=0;i<nav.length;i++){{if(nav[i]>pk)pk=nav[i];dd.push((nav[i]/pk-1)*100);}}return dd;}}
{markets_js}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# change detection
# ---------------------------------------------------------------------------
def detect_changes(prev: dict, sigs: dict) -> list:
    """可行動變化＝任一腿閘門翻轉，或 |今日目標 − 現持（執行層 executed_pct）| ≥ 10pp。
    改為與現持比（非與前一日目標比），才不會漏掉緩慢累積的漂移；alert 顯示取整後的
    建議動作（現持 → round(目標/5)×5）。訊息標市場前綴（美股／台股）。"""
    if not prev or "tickers" not in prev:
        return []
    out = []
    for t in ALL_TICKERS:
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
            out.append(f"<b>{TICKER_MARKET[t]} {t}</b>：{'、'.join(parts) + ' → ' if parts else ''}{arrow}")
    return out


def main():
    prev_state = {}
    if STATE_JSON.exists():
        try:
            prev_state = json.loads(STATE_JSON.read_text())
        except Exception:
            prev_state = {}

    px_map, sigs = {}, {}
    for t in ALL_TICKERS:
        print(f"Fetching {YF_SYMBOL[t]}...")
        px_map[t] = fetch_close(t)
        d = compute_ticker(t, px_map[t])
        sigs[t] = d
        print(f"  {t}: gate={'IN' if d['gate'] else 'OUT'} RV20={d['rv20']*100:.1f}% "
              f"σ_t={d['sigma_t']*100:.1f}% sleeve={d['sleeve']:.2f} -> final {d['final']*100:.0f}%")

    exp = {}
    for m in MARKETS:
        exp[m["key"]] = sum(sigs[t]["final"] for t in m["legs"]) * 100
        print(f"{m['short']} combined target exposure: {exp[m['key']]:.0f}%")

    changes = detect_changes(prev_state, sigs)
    data_date = max(sigs[t]["wk_date"] for t in ALL_TICKERS)

    # ---- per-market history: rule-replay backfill (once) + daily live append ----
    hist_map = {}
    for m in MARKETS:
        legs = m["legs"]
        prev_history = prev_state.get(m["hist_key"], [])
        backfill = build_backfill(px_map, legs) if len(prev_history) < BACKFILL_DAYS else []
        daily_date = max(px_map[t].index[-1] for t in legs)
        today_rec = _daily_record(px_map, legs, daily_date, "live")
        history = merge_history(prev_history, backfill, today_rec)
        hist_map[m["key"]] = history
        print(f"{m['short']} history: {len(history)} days (backfill {len(backfill)}, "
              f"span {history[0]['date']}→{history[-1]['date']})")

    # ---- per-market execution layer replay (deterministic from history) ----
    exec_map = {m["key"]: band_exec_replay(hist_map[m["key"]], m["legs"]) for m in MARKETS}
    exec_last = {}
    for m in MARKETS:
        er = exec_map[m["key"]]
        exec_last.update(er["last"])
        print(f"{m['short']} exec layer: {len(er['events'])} events, current executed " +
              ", ".join(f"{t} {er['last'][t]:.0f}%" for t in m["legs"]))

    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES: {last_change_desc}")
        lines = [f"自適應 σ 長線 × 波動率目標（美+台）— 可行動變化（數據截至 {data_date}）", ""]
        for c in changes:
            lines.append("• " + c.replace("<b>", "").replace("</b>", ""))
        lines += ["", "當前目標權重："]
        for t in ALL_TICKERS:
            d = sigs[t]
            lines.append(f"  {TICKER_MARKET[t]} {t}: {d['final']*100:.0f}%  "
                         f"(閘門{'在場' if d['gate'] else '出場'}, RV20 {d['rv20']*100:.1f}%, "
                         f"σ_t {d['sigma_t']*100:.1f}%, 套袖 {d['sleeve']:.2f})")
        lines += ["", f"美股組合曝險 {exp['us']:.0f}% · 台股組合曝險 {exp['tw']:.0f}% · 下一個交易日調整至上列目標。", "",
                  "固定 vs 自適應 前瞻 OOS 對照（未採用）。詳細： https://research.investmquest.com/long-track-adaptive-vt/"]
        ALERT_FILE.write_text("\n".join(lines), encoding="utf-8")
        print(f"Alert file: {ALERT_FILE}")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()
        print("No actionable change vs last run.")

    html = generate_html(sigs, changes, last_change_date, hist_map, exec_map)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "ruleset_locked_date": FREEZE_DATE,
        "mechanism": "adaptive median σ_t = rolling(756, min_periods=252).median(RV20); w=min(1, σ_t/RV20)",
        "status": "forward OOS paper tracking, not adopted (fixed-vs-adaptive parallel; verdict: TW pass, US noise-level tie)",
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
        "weights": WEIGHTS,
        "combined_exposure_us_pct": round(exp["us"], 1),
        "combined_exposure_tw_pct": round(exp["tw"], 1),
        "tickers": {
            t: {
                "market": TICKER_MARKET[t],
                "gate": sigs[t]["gate"],
                "sigma_base_pct": round(SIGMA_BASE[t] * 100, 1),
                "sigma_t_pct": round(sigs[t]["sigma_t"] * 100, 2),
                "rv20_pct": round(sigs[t]["rv20"] * 100, 2),
                "sleeve_weight": round(sigs[t]["sleeve"], 4),
                "final_weight_pct": round(sigs[t]["final"] * 100, 1),
                "executed_pct": exec_last[t],
                "wk_date": sigs[t]["wk_date"],
                "wk_close": round(sigs[t]["wk_close"], 2),
                "w52": round(sigs[t]["w52"], 2),
                "w104": round(sigs[t]["w104"], 2),
                "w250": round(sigs[t]["w250"], 2),
                "s104_pos": sigs[t]["s104_pos"],
                "s250_pos": sigs[t]["s250_pos"],
            } for t in ALL_TICKERS
        },
        "history_us": hist_map["us"],
        "history_tw": hist_map["tw"],
    }
    STATE_JSON.write_text(json.dumps(state_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
