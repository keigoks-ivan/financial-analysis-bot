#!/usr/bin/env python3
"""W52 × 自適應 cap 1.5 ＋「日線均線長多確認」— 唯讀影子追蹤頁產生器
================================================================================
持有人 2026-09-15 提出的候選規則：實單主系統（update_long_track_w52_adaptive.py）只在平靜
regime（σ_t/RV20 > 1）借錢加碼到 150%；本頁在此之上多加一道<b>日線均線長多確認</b>——只有
均線也配合長多時才准許加碼到 cap 1.5，均線不配合就退回 cap 1.0。<b>本頁唯讀、不採用為實單、
無 email</b>；實單主系統的規則、程式碼、輸出檔（_body.html／state.json）完全不受本頁影響。

規則（凍結，照 2026-09-15 提案，不自行調參）：
  1. 週線 W52 單線閘門——與實單主系統逐位元相同（W-FRI；週收 > SMA52w 在場、< 出場）。
  2. 自適應波動率套袖分母——與實單主系統逐位元相同：σ_t ＝ RV20 的
     rolling(756, min_periods=252).median()；raw_ratio ＝ σ_t／RV20。
  3. <b>日線均線長多確認（score5，lag 20，本頁唯一新增條件）</b>：以 auto-adjust 收盤價算
     ma60/ma120/ma200；五條件——收盤 > MA60、收盤 > MA120、收盤 > MA200、MA120 今日 >
     MA120 20 個交易日前、MA200 今日 > MA200 20 個交易日前——全對 → ma5_on=True。
     cap_eff = 1.5 if ma5_on else 1.0；w = min(cap_eff, raw_ratio)（均線不配合時借錢加碼的
     上限退回 1.0，其餘與實單完全相同）。
  4. 執行層 A2（同實單）：20pp 門檻＋10% 取整＋取整後 clamp 於 50×1.5＝75pp（固定，
     不隨 cap_eff 變動）；最終目標權重 = 0.5 × 閘門 × 套袖（每市場兩腿各自計算）。

2026-09-15 同日修訂（缺陷 4）：三個價格條件（收盤 > MA60／MA120／MA200）加 1% 遲滯
（hysteresis，見 `_hyst`／`MA_BUF`）——理由＝收盤在 MA60 附近天天翻，造成執行層抖動。
條件目前關則收盤 > MA 才轉開；目前開則收盤 < MA×(1−1%) 才轉關；中間帶沿用前一日狀態。
兩條斜率條件（MA120／MA200 斜率向上）不變。回測依 v7-backtest
run_w52_adaptive_ma_confirm.py 的預註冊判準（兩市場同時滿足：年執行層變動次數不高於
buf=0、CAGR 不低於 buf=0 逾 0.2pp、MDD 不深於 buf=0 逾 0.5pp）驗證通過，採用 buf=0.01。
本頁 2026-09-15 才上線、無實錄可保留，故規則改動後 `ma_confirm_state.json` 重新
backfill（非累加式修訂）。

預註冊（2026-09-15）：本頁與實單並行 ≥ 60 交易日後、於 2026-10 回顧點比較三件事——
(a) 市場已從高點跌超過 5% 仍持有超過 100% 曝險的天數，(b) 執行層變動次數，(c) 兩條執行層
淨值差。本頁不自動採用；回測顯示美股 Calmar 持平（0.60→0.61、CAGR −0.3pp）、台股變差
（1.24→1.14、CAGR −1.5pp），這是用報酬買心理壓力，數字上沒有理由自動採用。（此段數字為
原提案、未計入同日遲滯修訂，判準卡片本身依規定保留不動；下方回測表已改採 buf=0.01 新數字。）

回測數字轉錄自 v7-backtest results/vol_targeting/w52_adaptive_ma_confirm_lag20_buf1.json
（run_w52_adaptive_ma_confirm.py --buf 0.01 產出；美股資料截至 2026-06-11、台股至
2026-09-08，斜率 lag 20、價格條件遲滯 buf=1%；lag 5/60 結論相同）。閘門、套袖分母、
執行層與實單主系統逐位元相同，僅 cap_eff 是否退回 1.0 這一件事不同——不掃參擇優、
不改機制形狀、不加濾網。

輸出：docs/long-track-w52-adaptive/ma-confirm.html ＋ ma_confirm_state.json（history_us／
history_tw 各 1260 回放＝近五年，date-keyed merge 冪等；_daily_record 每腿另記
ma5_on／cap_eff／ma_cond／sleeve_variant="ma_confirm_l20_h1"）。另唯讀讀取實單主系統的
docs/long-track-w52-adaptive/state.json（history_us／history_tw／tickers），供「本頁 vs
主系統」對照卡與雙線曝險時間軸使用（唯讀，不寫入、不影響主系統）。

CANONICAL COPY：本檔在 v7-backtest（src/vol_target_backtest/）與 financial-analysis-bot
（scripts/）兩處逐位元相同——nav 匯入以 try/except 兼容兩 repo，輸出路徑自動解析為
<repo_root>/docs/long-track-w52-adaptive/。CI 由 fab 執行（update_long_track_w52_adaptive.yml，
台股收盤後 + 美股收盤後各跑一次，date-keyed merge 冪等所以安全）。<b>本頁無 email／alert</b>。
"""
from __future__ import annotations   # 本機 python3（系統，3.9）相容 `X | None` 型別註記；不影響執行期行為

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

# 獨立完整頁（非 iframe 片段）：比照 tw-semivol.html／leverage.html，掛完整站 nav。
NAV_BLOCK = full_nav_block("system", "lthub")

# ---- output dir: <repo_root>/docs/long-track-w52-adaptive/ -----------------
_cand = [HERE.parent / "docs", HERE.parents[2] / "docs" if len(HERE.parents) >= 3 else HERE / "docs"]
DOCS = next((c for c in _cand if c.exists()), _cand[0])
OUTPUT = DOCS / "long-track-w52-adaptive" / "ma-confirm.html"
STATE_JSON = DOCS / "long-track-w52-adaptive" / "ma_confirm_state.json"
MAIN_STATE_JSON = DOCS / "long-track-w52-adaptive" / "state.json"   # 唯讀：實單主系統對照
# 無 email／alert：本頁為持有人 2026-09-15 提案的唯讀影子追蹤（不採用為實單），不觸發任何通知。

PROPOSAL_DATE = "2026-09-15"                # 持有人提案日
MA_LAG = 20                                 # 均線斜率比較日數（凍結；lag 5/60 結論相同）

US_TICKERS = ["QQQ", "SMH"]
TW_TICKERS = ["0050", "2330"]
ALL_TICKERS = US_TICKERS + TW_TICKERS
YF_SYMBOL = {"QQQ": "QQQ", "SMH": "SMH", "0050": "0050.TW", "2330": "2330.TW"}
IS_TW = {"QQQ": False, "SMH": False, "0050": True, "2330": True}
TICKER_MARKET = {"QQQ": "美股", "SMH": "美股", "0050": "台股", "2330": "台股"}
WEIGHTS = {t: 0.5 for t in ALL_TICKERS}    # 每市場內兩腿各 50%，兩組合各自 100%
MED_WIN = 756                              # 自適應中位數視窗（3 年），與實單主系統相同、凍結
MIN_PERIODS = 252                          # 首年 expanding
FREEZE_DATE = "2026-07-17"                 # 機制凍結日（W52 閘門／套袖分母／視窗，同實單主系統）

BACKFILL_DAYS = 1260                       # 回放窗（近五年交易日，同實單主系統）
HISTORY_CAP = 1320                         # state.json history 陣列上限（>1260 留實錄餘裕）

# ---------------------------------------------------------------------------
# 回測摘要（v7-backtest results/vol_targeting/w52_adaptive_ma_confirm_lag20_buf1.json，
# run_w52_adaptive_ma_confirm.build_market --buf 0.01 轉錄；美股窗至 2026-06-11、台股窗至
# 2026-09-08，斜率 lag 20、價格條件遲滯 buf=1%（缺陷 4，2026-09-15 同日修訂，判準通過採用）
# ——持有人凍結規則，不因報告日期落後而重跑調整；lag 5/60 結論相同）。
# 每列：(label, cagr%, mdd%, calmar, martin, avg_expo%, peak_expo%)。
# ---------------------------------------------------------------------------
BT_MA_US = {
    "window": ["2005-01-03", "2026-06-11"],
    "rows": [
        ("cap1.0 無槓桿對照", 12.68, -22.38, 0.5664, 1.437, 70, 100),
        ("cap1.5 實單主系統", 14.11, -23.68, 0.5957, 1.283, 85, 150),
        ("cap1.5＋均線確認（本頁追蹤）", 13.88, -22.95, 0.6046, 1.291, 83, 150),
        ("50/50 買進持有", 17.67, -56.93, 0.3103, 1.261, 100, 100),
    ],
}
BT_MA_TW = {
    "window": ["2014-01-01", "2026-09-08"],
    "rows": [
        ("cap1.0 無槓桿對照", 19.33, -19.13, 1.0108, 2.525, 70, 100),
        ("cap1.5 實單主系統", 23.32, -18.88, 1.2355, 2.593, 84, 145),
        ("cap1.5＋均線確認（本頁追蹤）", 22.72, -19.08, 1.1909, 2.510, 83, 150),
        ("50/50 買進持有", 26.81, -39.47, 0.6792, 2.731, 100, 100),
    ],
}

# 分期表（只列 實單 cap1.5 vs 本頁 cap1.5_ma；同一份 JSON 的 subperiods）。
# 每列：(label, live_cagr%, live_mdd%, live_calmar, shadow_cagr%, shadow_mdd%, shadow_calmar)
ERA_MA_US = [
    ("2005-08 GFC", -2.22, -22.28, -0.0994, -0.68, -18.34, -0.0372),
    ("2009-13 QE", 12.03, -22.13, 0.5435, 10.48, -22.95, 0.4565),
    ("2014-18 低波", 10.75, -23.68, 0.4541, 10.82, -22.57, 0.4796),
    ("2019-23 COVID", 22.21, -20.47, 1.0846, 20.72, -20.47, 1.0122),
    ("2024- AI 牛", 43.85, -18.19, 2.4111, 45.32, -18.90, 2.3980),
]
ERA_MA_TW = [
    ("2014-16 陸股貶值/整理", 12.87, -17.06, 0.7540, 12.76, -16.17, 0.7892),
    ("2017-19 平順多頭", 18.95, -18.67, 1.0147, 18.42, -19.08, 0.9656),
    ("2020-22 COVID/升息", 14.25, -18.88, 0.7549, 13.53, -18.88, 0.7166),
    ("2023- AI 台積電牛", 44.71, -18.67, 2.3949, 43.65, -18.66, 2.3396),
]

# 逐年表（只列 實單 cap1.5 vs 本頁 cap1.5_ma；同一份 JSON 的 annual，2026 為 YTD 部分年
# ——美股窗至 2026-06-11、台股窗至 2026-09-08）。每列：(年度, live%, shadow%, 差 pp, partial)
ANNUAL_MA_US = [
    (2005, -4.0, -2.6, 1.4, False), (2006, -4.8, -2.2, 2.6, False),
    (2007, 3.5, 5.7, 2.2, False), (2008, -3.3, -3.3, 0.0, False),
    (2009, 29.5, 28.0, -1.5, False), (2010, 8.8, 7.2, -1.6, False),
    (2011, -8.8, -10.8, -2.0, False), (2012, 0.1, 2.2, 2.1, False),
    (2013, 37.0, 31.5, -5.5, False), (2014, 18.2, 17.4, -0.8, False),
    (2015, -4.7, -4.7, 0.0, False), (2016, 1.2, 2.7, 1.5, False),
    (2017, 43.0, 42.7, -0.3, False), (2018, 0.9, 0.6, -0.3, False),
    (2019, 19.0, 16.2, -2.8, False), (2020, 22.2, 22.2, 0.0, False),
    (2021, 40.7, 37.9, -2.8, False), (2022, -13.8, -13.8, 0.0, False),
    (2023, 54.1, 51.5, -2.6, False), (2024, 33.2, 34.0, 0.8, False),
    (2025, 30.5, 32.3, 1.8, False), (2026, 34.9, 35.4, 0.5, True),
]
ANNUAL_MA_TW = [
    (2014, 32.0, 30.7, -1.3, False), (2015, -4.7, -4.0, 0.7, False),
    (2016, 14.2, 14.1, -0.1, False), (2017, 33.5, 31.9, -1.6, False),
    (2018, -2.0, -2.0, 0.0, False), (2019, 29.0, 28.9, -0.1, False),
    (2020, 35.7, 35.7, 0.0, False), (2021, 17.6, 16.9, -0.7, False),
    (2022, -5.3, -6.5, -1.2, False), (2023, 19.5, 15.8, -3.7, False),
    (2024, 55.2, 57.2, 2.0, False), (2025, 33.1, 31.9, -1.2, False),
    (2026, 57.9, 57.9, 0.0, True),
]

# 市場定義（渲染與資料處理共用）
MARKETS = [
    {"key": "us", "name": "美股 QQQ + SMH", "short": "QQQ+SMH",
     "legs": US_TICKERS, "hist_key": "history_us",
     "bt": BT_MA_US, "era": ERA_MA_US, "annual": ANNUAL_MA_US},
    {"key": "tw", "name": "台股 0050 + 2330", "short": "0050+2330",
     "legs": TW_TICKERS, "hist_key": "history_tw",
     "bt": BT_MA_TW, "era": ERA_MA_TW, "annual": ANNUAL_MA_TW},
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
    """W52 單線閘門（週收 > SMA52w 在場、< 出場，W-FRI，無滯後條件）。逐位元對齊
    run_w52_adaptive.gate_w52：閘門值＝「已收完的」W-FRI 週棒 ffill 到當日，未收完的
    當週（週五未到）之週棒不計入決策——只用於 recent[] 顯示背景。回傳
    (wk, pos, w52, w104, w250, s104, s250, pos_daily)——W104/W250 與斜率僅供頁面卡片
    作參考背景，<b>閘門決策只用 W52</b>；共用給 gate_state 與 build_backfill。"""
    wk = px.resample("W-FRI").last().dropna()
    w52 = wk.rolling(52).mean()
    w104 = wk.rolling(104).mean()
    w250 = wk.rolling(250).mean()
    s104 = w104 - w104.shift(4)
    s250 = w250 - w250.shift(4)
    pos = (wk > w52).astype(int)      # W52 單線：無 W104/W250 斜率滯後條件
    pos[w52.isna()] = 0
    pos = pos.astype(int)
    # 逐位元對齊 gate_w52：只有「已收完」的週棒才會透過 ffill 影響某日的閘門值——
    # 若 px 最後一天 < wk 最後一根的週五標籤（本週尚未收），該根不會被 ffill 選到，
    # 等同回測端 gate_w52 的行為（不需額外丟棄，reindex+ffill 本身就有此效果）。
    pos_daily = pos.reindex(px.index, method="ffill").fillna(0).astype(int)
    return wk, pos, w52, w104, w250, s104, s250, pos_daily


def gate_state(px: pd.Series) -> dict:
    wk, pos, w52, w104, w250, s104, s250, pos_daily = _gate_core(px)

    # recent[] 僅供頁面背景顯示；若最後一根週棒尚未收完（px 最後一天 < 週五標籤），
    # 該根不是決策依據，顯示時標記 incomplete 供人判讀，不影響 gate 本身。
    last_wk_complete = wk.index[-1] <= px.index[-1]

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
            **({"incomplete": True} if (i == -1 and not last_wk_complete) else {}),
        })
    return {
        "gate": bool(pos_daily.iloc[-1]),   # 已收完週棒 ffill 到今日，逐位元對齊 gate_w52
        "wk_date": wk.index[-1].strftime("%Y-%m-%d"),
        "wk_close": float(wk.iloc[-1]),
        "w52": float(w52.iloc[-1]), "w104": float(w104.iloc[-1]), "w250": float(w250.iloc[-1]),
        "s104_pos": bool(s104.iloc[-1] > 0), "s250_pos": bool(s250.iloc[-1] > 0),
        "recent": recent,
    }


# ---------------------------------------------------------------------------
# Sleeve — adaptive median (verbatim port of main system's _sleeve_from) ＋
# 日線均線長多確認（持有人 2026-09-15 提案，本頁唯一新增條件）
# ---------------------------------------------------------------------------
CAP = 1.5   # 均線配合時的曝險上限（同實單主系統）；均線不配合時 cap_eff 退回 1.0
MA_BUF = 0.01  # 缺陷 4（2026-09-15 同日修訂）：三個價格條件的遲滯緩衝＝1%，回測判準通過後採用

# 執行層常數（同實單主系統 A2：門檻 20pp／格 10%／取整後 clamp 於 50×CAP＝75pp，
# 固定不隨 cap_eff 變動）。band／grid／clamp 皆組合 pp；整數 pp 空間比較。
EXEC_BAND = 20.0
EXEC_GRID = 10.0
EXEC_CLAMP = 50.0 * CAP           # 固定 75pp（單腿滿載）；不隨 cap_eff 是否退回 1.0 而變
EXEC_UPGRADE_DATE = "2026-07-22"  # 執行層升格 A2 之日（同實單主系統，規則凍結日仍為 FREEZE_DATE）


def _hyst(close: pd.Series, ma: pd.Series, buf: float) -> pd.Series:
    """收盤 vs MA 的遲滯狀態機（缺陷 4，2026-09-15 同日修訂）：條件目前關→收盤>ma
    才轉開；目前開→收盤<ma×(1−buf) 才轉關；中間帶沿用前一日狀態，起始為 False。
    逐位元對齊 v7-backtest run_w52_adaptive_ma_confirm._hyst。buf=0 時 off=收盤<ma
    與 on 互補（相等時沿用前值）——與原本「收盤>ma」在收盤==ma 那一刻有微小差異，允許。"""
    on = close > ma
    off = close < ma * (1.0 - buf)
    st = pd.Series(np.nan, index=close.index)
    st[on] = 1.0
    st[off] = 0.0
    return st.ffill().fillna(0.0) > 0.5


def _ma_conditions(px: pd.Series, lag: int = MA_LAG) -> tuple:
    """日線均線長多 score5（持有人 2026-09-15 提案；同日修訂加 1% 遲滯，缺陷 4）。
    逐位元對齊 v7-backtest run_w52_adaptive_ma_confirm.ma_score5(lag=20, buf=MA_BUF)：
    五條件——收盤>MA60、收盤>MA120、收盤>MA200（三者皆用 `_hyst` 加 1% 遲滯，理由＝收盤
    在 MA60 附近天天翻會造成執行層抖動）、MA120 今日>MA120 lag 日前、MA200 今日>MA200
    lag 日前（斜率兩條件不加遲滯，維持原樣）——全對→ma5_on=True。因果、無前視。
    回傳 (cond_dict, ma5_on)。"""
    ma60 = px.rolling(60).mean()
    ma120 = px.rolling(120).mean()
    ma200 = px.rolling(200).mean()
    cond = {
        "gt60": bool(_hyst(px, ma60, MA_BUF).iloc[-1]),
        "gt120": bool(_hyst(px, ma120, MA_BUF).iloc[-1]),
        "gt200": bool(_hyst(px, ma200, MA_BUF).iloc[-1]),
        "s120_up": bool(ma120.iloc[-1] > ma120.shift(lag).iloc[-1]),
        "s200_up": bool(ma200.iloc[-1] > ma200.shift(lag).iloc[-1]),
    }
    ma5_on = all(cond.values())
    return cond, ma5_on


def _sleeve_from(px: pd.Series, win: int = 20):
    """Returns (rv20_now, sigma_t_now, sleeve, raw_ratio, ma5_on, cap_eff). RV20／σ_t／
    raw_ratio 與實單主系統 _sleeve_from 逐位元相同（σ_t ＝ RV20 的
    rolling(756, min_periods=252).median()；raw_ratio ＝ σ_t/RV20，未 clip）。
    cap_eff = 1.5 if ma5_on else 1.0（均線不配合時，借錢加碼的上限退回 1.0）；
    w = min(cap_eff, raw_ratio)——與 v7-backtest run_w52_adaptive_ma_confirm.leg_weight
    的 "cap1.5_ma" 分支數學等價（ratio<=cap 時取 ratio、ratio>cap 時取 cap，即
    ratio.clip(upper=cap)）。因果、無前視。"""
    lr = np.log(px / px.shift(1))
    rv = lr.rolling(win).std() * np.sqrt(252)
    sigma = rv.rolling(MED_WIN, min_periods=MIN_PERIODS).median()
    rv_now = float(rv.iloc[-1])
    sig_now = float(sigma.iloc[-1])
    _, ma5_on = _ma_conditions(px)
    cap_eff = 1.5 if ma5_on else 1.0
    if rv_now > 0 and not np.isnan(sig_now):
        raw = sig_now / rv_now
        w = min(cap_eff, raw)
    else:
        raw, w = 1.0, min(cap_eff, 1.0)
        if np.isnan(sig_now):
            sig_now = rv_now
    return rv_now, sig_now, w, raw, ma5_on, cap_eff


def sleeve_state(px: pd.Series) -> dict:
    rv_now, sig_now, w, raw, ma5_on, cap_eff = _sleeve_from(px)
    cond, _ = _ma_conditions(px)
    # 距離開槓桿：raw < 1 時波動還要降 (1-raw) 才到 1.0（開始借錢）；raw ≥ 1 已在借
    return {"rv20": rv_now, "sigma_t": sig_now, "sleeve": w, "raw_ratio": raw,
            "ma5_on": ma5_on, "cap_eff": cap_eff, "ma_cond": cond,
            "sleeve_variant": "ma_confirm_l20_h1",
            "levered": bool(raw > 1.0), "dist_to_lever": max(0.0, 1.0 - raw)}


def compute_ticker(t: str, px: pd.Series) -> dict:
    g = gate_state(px)
    s = sleeve_state(px)
    fill = (1 if g["gate"] else 0) * s["sleeve"]        # 0..1.5 fill of the 0.5 slot
    final = WEIGHTS[t] * fill
    return {**g, **s, "fill": fill, "final": final}


# ---------------------------------------------------------------------------
# History — rule-replay backfill (誠實紀律：回放 ≠ 實錄，欄位 source 標記區分)
# ---------------------------------------------------------------------------
def _daily_record(px_map: dict, legs: list, d: pd.Timestamp, source: str) -> dict:
    """One market's one-day target weights, computed byte-identically to the
    live path: gate = 已收完 W-FRI 週棒 ffill 到 d（_gate_core(px[:d]).pos_daily.iloc[-1]，
    逐位元對齊 run_w52_adaptive.gate_w52，與實單主系統相同）；sleeve = adaptive median
    × 均線 cap_eff on px[:d]（無前視：px_map[t].loc[:d] 截到當日）。
    source ∈ {'replay','live'}. Records sigma_t_pct／ma5_on／cap_eff／ma_cond per leg."""
    rec = {"date": d.strftime("%Y-%m-%d"), "source": source, "tickers": {}}
    combined = 0.0
    for t in legs:
        pxd = px_map[t].loc[:d]
        *_, pos_daily = _gate_core(pxd)
        gate = bool(pos_daily.iloc[-1])
        rv_now, sig_now, sleeve, raw, ma5_on, cap_eff = _sleeve_from(pxd)
        cond, _ = _ma_conditions(pxd)
        final = WEIGHTS[t] * ((1 if gate else 0) * sleeve)
        combined += final
        rec["tickers"][t] = {
            "gate": gate,
            "rv20_pct": round(rv_now * 100, 2),
            "sigma_t_pct": round(sig_now * 100, 2),
            "raw_ratio": round(raw, 4),
            "sleeve": round(sleeve, 4),
            "ma5_on": ma5_on,
            "cap_eff": cap_eff,
            "ma_cond": cond,
            "sleeve_variant": "ma_confirm_l20_h1",
            "final_pct": round(final * 100, 1),   # 組合 pp，0..75（每腿滿槓桿 75）
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
# Execution layer — A2：20pp 門檻＋10% 取整＋取整後 clamp 於 50×cap（升格 2026-07-22）
# 每市場各自從 history 確定性重放（history_us／history_tw），冪等可重現。
# band／grid／clamp 以組合 pp 為單位（每腿滿載＝50 pp；cap1.5 clamp＝75pp）。
# ---------------------------------------------------------------------------
def band_exec_replay(history: list, legs: list) -> dict:
    """對每腿的最終權重（組合 pp）重放執行層：executed 初始 0，逐日若
    |target − executed| ≥ 20pp 則 executed = min(round(target/10)×10, 50×cap)，否則不變。
    整數 pp 空間 ≥ 比較（不在 0..1 浮點空間重寫）。回傳每腿每日 executed、組合合計、
    事件清單（日期、腿、from→to、原因＝該日閘門翻轉則「閘門翻轉」否則「波動調整」、
    當日組合執行曝險）與各腿當前值。"""
    executed = {t: [] for t in legs}
    combined, events = [], []
    cur = {t: 0.0 for t in legs}
    prev_gate = {t: None for t in legs}
    for r in history:
        for t in legs:
            tk = r["tickers"][t]
            target = tk["final_pct"]
            gate = bool(tk["gate"])
            if abs(target - cur[t]) >= EXEC_BAND:
                new = min(round(target / EXEC_GRID) * EXEC_GRID, EXEC_CLAMP)
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
    # 2026-07-24：事件表由近三年窗改為過濾最近一年（365 個日曆天），標題同步；
    # band_exec_replay 本身仍對全史（現已近五年）重放以確保現持狀態正確，只有本表顯示過濾。
    cutoff = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    recent_events = [e for e in events if e["date"] >= cutoff]
    if not recent_events:
        body = ('<tr><td colspan="5" style="text-align:center;color:var(--muted)">'
                '最近一年窗內無執行層調整事件（皆未跨 20pp 門檻）</td></tr>')
    else:
        body = ""
        for ev in reversed(recent_events):          # 倒序（最新在上）
            rc = "var(--blue-text)" if ev["reason"] == "閘門翻轉" else "var(--amber-text)"
            body += (f'<tr><td>{ev["date"]}</td><td><b>{ev["leg"]}</b></td>'
                     f'<td>{ev["from"]:.0f}% → {ev["to"]:.0f}%</td>'
                     f'<td style="color:{rc}">{ev["reason"]}</td>'
                     f'<td class="num">{ev["combined_exec_pct"]:.0f}%</td></tr>\n')
    return f"""<div class="card">
<h3>{mkt['short']} 最近一年執行層訊號變化事件（A2：20pp 門檻＋10% 取整＋clamp 150%）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
只有當某腿目標與現持差 ≥ 20pp 才調整（取整到 10% 格、再 clamp 於 75%），故事件遠少於每日微調。倒序列出最近 365 天內全部事件；「變化」為該腿最終權重（組合 pp，滿載 50%）；原因＝當日閘門翻轉則「閘門翻轉」否則「波動調整」。</p>
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
    ma5_on = d["ma5_on"]
    cap_eff = d["cap_eff"]
    cond = d["ma_cond"]

    def _lamp(name, ok):
        bg = "var(--green-bg)" if ok else "var(--red-bg)"
        fg = "var(--green-text)" if ok else "var(--red-text)"
        mark = "✓" if ok else "✕"
        return f'<span class="tag" style="background:{bg};color:{fg};margin:0 .2rem .2rem 0">{mark} {name}</span>'

    lamps = "".join([
        _lamp("收盤&gt;MA60", cond["gt60"]),
        _lamp("收盤&gt;MA120", cond["gt120"]),
        _lamp("收盤&gt;MA200", cond["gt200"]),
        _lamp(f"MA120斜率↑(lag{MA_LAG})", cond["s120_up"]),
        _lamp(f"MA200斜率↑(lag{MA_LAG})", cond["s200_up"]),
    ])
    return f"""<div class="tcard">
  <div class="tcard-hdr">
    <span class="tname">{t}</span>
    <span class="pos-badge pos-{col}">最終權重 {d['final']*100:.0f}%</span>
  </div>
  <div class="tcard-sub">閘門 {'在場' if gate_on else '出場'} × 套袖 {d['sleeve']*100:.0f}%（cap_eff {cap_eff:.1f}）
    → 佔本標的 50% 額度的 {d['fill']*100:.0f}% · 目標權重 0.5 × {1 if gate_on else 0} × {d['sleeve']:.2f} = {d['final']*100:.0f}%{warn}</div>
  <div class="sig-row">
    <div class="sig {'on' if gate_on else 'off'}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">週線長軌閘門</span><span class="sig-mark">{'✓ 在場' if gate_on else '✕ 出場'}</span></div>
      <div class="sig-detail">週收 {d['wk_close']:.2f}｜W52 {d['w52']:.2f} <b style="color:var(--{'green' if d52>=0 else 'red'})">{fmt_pct(d52,1)}</b>
        ｜W104 {d['w104']:.2f} <b style="color:var(--{'green' if d104>=0 else 'red'})">{fmt_pct(d104,1)}</b>
        ｜W250 {d['w250']:.2f} <b style="color:var(--{'green' if d250>=0 else 'red'})">{fmt_pct(d250,1)}</b>
        ｜W104斜率 {'↑' if d['s104_pos'] else '↓'}｜W250斜率 {'↑' if d['s250_pos'] else '↓'}
        <br><span style="font-size:.72rem">W52 單線閘門：週收 &gt; W52 在場、&lt; W52 出場（與實單主系統逐位元相同，不受本頁均線條件影響）。</span></div>
    </div>
    <div class="sig {'on' if ma5_on else 'off'}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">日線均線長多確認（score5，持有人提案）</span><span class="sig-mark">{'✓ 五條全對' if ma5_on else '✕ 未全對'}</span></div>
      <div class="sig-detail">{lamps}
        <br><span style="font-size:.72rem">五條全對 → cap_eff = <b>1.5</b>（同實單）；任一條不對 → cap_eff 退回 <b>1.0</b>（凍結規則，不調參）。三個價格條件（收盤 vs MA60/120/200）加 1% 遲滯：關轉開要收盤 &gt; MA，開轉關要收盤 &lt; MA×99%，中間帶維持前一日狀態（2026-09-15 同日修訂，理由是收盤貼著 MA60 天天翻會讓執行層跟著抖動）。</span></div>
    </div>
    <div class="sig {'on' if d['levered'] else ('off' if d['sleeve']<0.999 else '')}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">自適應套袖 × cap_eff {cap_eff:.1f}</span><span class="sig-mark">{d['sleeve']*100:.0f}%</span></div>
      <div class="sig-detail">RV20 <b>{rv:.1f}%</b> vs σ_t <b>{sig:.1f}%</b> → σ_t/RV20 原始比率 <b>{d['raw_ratio']:.2f}</b>
        → w = min(cap_eff {cap_eff:.1f}, {d['raw_ratio']:.2f}) = <b>{d['sleeve']:.2f}</b>
        <br><span style="font-size:.72rem">{('<b style=color:var(--green)>已開槓桿</b>：波動低於自身近 3 年中位，加碼到 %.0f%%。' % (d['sleeve']*100)) if d['levered'] else ('未開槓桿（σ_t/RV &lt; cap_eff，減碼中）：波動<b>再降 %.0f%%</b>才會開始借錢。' % (d['dist_to_lever']*100))} RV20／σ_t 分母與實單主系統完全相同，差異只在上限 cap_eff。</span></div>
    </div>
  </div>
</div>"""


def recent_table(t: str, d: dict) -> str:
    recent = d.get("recent")
    if recent is None:
        # 安全網：recent 需要價格序列才能算（見 gate_state），本頁每次執行都重抓價，
        # 正常不會走到這裡；保留以防未來加上不重抓價的路徑。
        return f"""<div class="card">
<h3>{t} — 近 8 週閘門軌跡（週線 W-FRI）</h3>
<p style="font-size:.82rem;color:var(--muted)">近 8 週背景資料暫缺，下次正常執行（抓價）會自動補回。</p>
</div>"""
    rows = ""
    for r in recent:
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
    """回測主表（4 列：cap1.0／cap1.5 實單／cap1.5＋均線確認 本頁／50-50 買進持有），
    轉錄自 v7-backtest results/vol_targeting/w52_adaptive_ma_confirm_lag20_buf1.json（BT_MA_US/TW）。"""
    bt = mkt["bt"]
    rows = ""
    for lab, cagr, mdd, calmar, martin, avg, peak in bt["rows"]:
        hl = ("rowhl" if "本頁追蹤" in lab else ("rowbh" if "買進持有" in lab else ""))
        rows += (f'<tr class="{hl}"><td>{lab}</td><td class="num">{cagr:.2f}%</td>'
                 f'<td class="num">{mdd:.2f}%</td><td class="num">{calmar:.4f}</td>'
                 f'<td class="num">{martin:.3f}</td><td class="num">{avg:.0f}%</td>'
                 f'<td class="num">{peak:.0f}%</td></tr>\n')
    return f"""<div class="card">
<h3>回測摘要 — {mkt['short']}（均線確認候選 vs 實單主系統・窗 {bt['window'][0]} ～ {bt['window'][1]}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
主列（藍底）＝<b>cap1.5＋均線確認（本頁追蹤，持有人 2026-09-15 提案，價格條件已加 1% 遲滯）</b>；灰底列＝實單主系統對照（cap1.5，規則除均線條件外完全相同）。
數字轉錄自 v7-backtest <code>results/vol_targeting/w52_adaptive_ma_confirm_lag20_buf1.json</code>：<b>美股資料截至 2026-06-11、台股至 2026-09-08，斜率 lag 20、價格條件遲滯 buf=1%；lag 5/60 結論相同</b>。</p>
<table><thead><tr><th>配置</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Calmar</th><th class="num">Martin</th><th class="num">平均曝險</th><th class="num">峰值</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>"""


def era_section(mkt: dict) -> str:
    """分期表（只列 實單 cap1.5 vs 本頁 cap1.5＋均線確認，同一份 JSON 的 subperiods）。"""
    rows = ""
    for lab, lc, lm, lcal, sc, sm, scal in mkt["era"]:
        rows += (f'<tr><td>{lab}</td>'
                 f'<td class="num">{lc:+.2f}%</td><td class="num">{lm:.2f}%</td><td class="num">{lcal:.4f}</td>'
                 f'<td class="num">{sc:+.2f}%</td><td class="num">{sm:.2f}%</td><td class="num">{scal:.4f}</td></tr>\n')
    return f"""<div class="card">
<h3>{mkt['short']} 分期回測 — 實單（cap1.5）vs 本頁（cap1.5＋均線確認）</h3>
<table><thead><tr><th>期間</th><th class="num" colspan="3">實單 CAGR／MDD／Calmar</th><th class="num" colspan="3">本頁 CAGR／MDD／Calmar</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>"""


def annual_perf_section(mkt: dict) -> str:
    """逐年回測績效表：只列 實單（cap1.5）vs 本頁（cap1.5＋均線確認），轉錄自同一份
    JSON 的 annual。欄位＝年度、實單報酬%、本頁報酬%、差 pp。"""
    rows = mkt["annual"]
    win = mkt["bt"]["window"]
    body = ""
    for yr, live, shadow, diff, partial in rows:
        yl = (f'{yr} <span style="font-size:.68rem;color:var(--amber-text);font-weight:700">YTD</span>'
              if partial else str(yr))
        lc = "var(--green)" if live >= 0 else "var(--red)"
        sc = "var(--green)" if shadow >= 0 else "var(--red)"
        dc = "var(--green)" if diff >= 0 else "var(--red)"
        body += (f'<tr><td>{yl}</td>'
                 f'<td class="num" style="color:{lc}">{fmt_pct(live, 1)}</td>'
                 f'<td class="num" style="color:{sc}">{fmt_pct(shadow, 1)}</td>'
                 f'<td class="num" style="color:{dc}">{diff:+.1f}</td></tr>\n')
    return f"""<div class="card">
<h3>{mkt['short']} 逐年回測 — 實單（cap1.5）vs 本頁（cap1.5＋均線確認）（窗 {win[0]} ～ {win[1]}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
差＝本頁 − 實單（pp）。<b>末年為 YTD 部分年</b>（美股窗至 2026-06-11、台股窗至 2026-09-08）。<b>逐年數字為回測、非實盤</b>，兩者規則除均線確認外完全相同。</p>
<table><thead><tr><th>年度</th><th class="num">實單 cap1.5</th><th class="num">本頁 cap1.5＋均線</th><th class="num">差 (pp)</th></tr></thead>
<tbody>{body}</tbody></table>
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
        # 燃料表：組合 σ_t/RV 原始比率均值（clip 顯示 2.5）
        "fuel": _col(lambda r: round(min(2.5, 0.5 * (r["tickers"][a].get("raw_ratio", 1.0)
                                                     + r["tickers"][b].get("raw_ratio", 1.0))), 2)),
        # executed layer (A2: 20pp band + 10% round + clamp 50×cap) — deterministic replay
        "cexe": json.dumps(exec_replay["combined"], separators=(",", ":")),
        "aexe": json.dumps(exec_replay["executed"].get(a, []), separators=(",", ":")),
        "bexe": json.dumps(exec_replay["executed"].get(b, []), separators=(",", ":")),
    }
    combined = sum(sigs[t]["final"] for t in legs) * 100            # 今日目標（訊號）
    exec_combined = round(exec_replay["combined"][-1], 1) if exec_replay["combined"] else combined  # 現持（執行層）
    exec_finals = [round(exec_replay["last"].get(t, 0.0), 1) for t in legs]   # 每腿現持（執行層）
    ccol = fill_color(combined / 100)
    slot = {t: WEIGHTS[t] * 100 for t in legs}
    finals = [round(sigs[t]["final"] * 100, 1) for t in legs]        # 組合 pp（滿載 50×cap；A2 門檻／email 判斷用，不動）
    # 每腿乘法鏈圖（chart-chain）：2026-07-24 起改為「自身滿載＝100%」基準顯示（純顯示變換，
    # 不影響上面 finals／組合 pp 判斷）。fill_self：gate×sleeve 的自身結果，0~150%（cap1.5）。
    fill_self = [round(sigs[t]["fill"] * 100, 1) for t in legs]
    gate_cut = [round(100.0 if not sigs[t]["gate"] else 0.0, 1) for t in legs]
    sleeve_cut = [round(max(0.0, 100.0 - fill_self[i] - gate_cut[i]), 1) for i, t in enumerate(legs)]
    n_replay = sum(1 for r in history if r["source"] == "replay")
    n_live = sum(1 for r in history if r["source"] == "live")
    span = (f"{history[0]['date']} → {history[-1]['date']}" if history else "—")
    return {
        "legs": legs, "a": a, "b": b, "combined": combined, "exec_combined": exec_combined,
        "exec_finals": exec_finals, "ccol": ccol,
        "finals": finals, "fill_self": fill_self,
        "C_FINALS": json.dumps(fill_self, separators=(",", ":")),
        "C_SLEEVE": json.dumps(sleeve_cut, separators=(",", ":")),
        "C_GATE": json.dumps(gate_cut, separators=(",", ":")),
        "H": H, "n_replay": n_replay, "n_live": n_live, "span": span,
        "nhist": len(history), "events": exec_replay["events"],
    }


def _dual_breakdown(legs, finals, exec_finals):
    """組合層目標/現持並排＋每腿拆分。合計＝每腿顯示值（四捨五入後）之和，確保
    「腿＋腿＝合計」自洽。回傳 (html、目標合計、現持合計)。"""
    tf = [round(f) for f in finals]
    ef = [round(e) for e in exec_finals]
    td, ed = sum(tf), sum(ef)
    tgt = "＋".join(f"{legs[i]} {tf[i]}%" for i in range(len(legs)))
    exe = "＋".join(f"{legs[i]} {ef[i]}%" for i in range(len(legs)))
    html = (f"<b>目標 {td}%</b>＝{tgt}（訊號，每日隨波動微調）／"
            f"<b>現持 {ed}%</b>＝{exe}（執行層；"
            f"<b>|目標−現持| 未達 20pp 不調，故兩者常有幾 % 差、是設計非錯誤</b>）")
    return html, td, ed


# ---------------------------------------------------------------------------
# 本頁 vs 實單主系統對照（唯讀）：讀取主系統 state.json 的 history_us／history_tw／
# tickers，用同一套 band_exec_replay（cap1.5＋A2，主系統早已相同規則）重建其執行層
# 曝險序列，與本頁自身執行層曝險並排——只取兩邊日期的交集，不外推、不填補缺口。
# 借自 update_long_track_w52_adaptive_tw_semivol.py 的 main_vs_shadow_series 等，
# 本頁兩市場（美＋台）各自比照辦理。
# ---------------------------------------------------------------------------
def load_main_state() -> dict:
    if not MAIN_STATE_JSON.exists():
        return {}
    try:
        return json.loads(MAIN_STATE_JSON.read_text())
    except Exception:
        return {}


def main_vs_shadow_series(mkt_key: str, shadow_history: list, shadow_exec: dict,
                          main_state: dict) -> dict:
    """回傳 {available, labels, shadow, main, n, span} 供雙線曝險時間軸；main_state
    缺失或無對應 history 時 available=False（頁面誠實顯示「主系統尚無可比資料」，
    不偽造）。"""
    hist_key = "history_us" if mkt_key == "us" else "history_tw"
    main_hist = main_state.get(hist_key) or []
    if not main_hist:
        return {"available": False}
    legs = MKT[mkt_key]["legs"]
    main_exec = band_exec_replay(main_hist, legs)
    main_by_date = {r["date"]: v for r, v in zip(main_hist, main_exec["combined"])}
    shadow_by_date = {r["date"]: v for r, v in zip(shadow_history, shadow_exec["combined"])}
    common = sorted(set(main_by_date) & set(shadow_by_date))
    if not common:
        return {"available": False}
    return {
        "available": True,
        "labels": json.dumps(common, separators=(",", ":")),
        "shadow": json.dumps([shadow_by_date[d] for d in common], separators=(",", ":")),
        "main": json.dumps([main_by_date[d] for d in common], separators=(",", ":")),
        "n": len(common), "span": f"{common[0]} → {common[-1]}",
    }


def main_snapshot_card(mkt_key: str, main_state: dict) -> str:
    """本頁 vs 主系統：今日讀數並排（唯讀，讀主系統 state.json 的 tickers／
    combined_exposure_{mkt}_pct，不做任何寫入或推算超出既有欄位）。"""
    mkt = MKT[mkt_key]
    legs = mkt["legs"]
    tk = main_state.get("tickers") or {}
    if not tk or any(t not in tk for t in legs):
        return (f'<div class="card"><h3>{mkt["short"]} 本頁 vs 實單主系統（唯讀對照）</h3>'
                '<p style="font-size:.82rem;color:var(--muted)">主系統 state.json 尚無可讀資料，略過本次對照。</p></div>')
    main_data_date = main_state.get("data_date", "—")
    tgt_sum = round(sum(tk[t]["final_weight_pct"] for t in legs), 1)
    exe_sum = round(sum(tk[t]["executed_pct"] for t in legs), 1)
    rows = ""
    for t in legs:
        d = tk[t]
        rows += (f'<tr><td>{t}</td><td class="num">{"在場" if d["gate"] else "出場"}</td>'
                 f'<td class="num">{d["rv20_pct"]:.1f}%</td><td class="num">{d["sigma_t_pct"]:.1f}%</td>'
                 f'<td class="num">{d.get("raw_ratio", d["sleeve_weight"]):.2f}</td>'
                 f'<td class="num">{d["final_weight_pct"]:.1f}%</td>'
                 f'<td class="num">{d["executed_pct"]:.0f}%</td></tr>\n')
    return f"""<div class="card" style="border:2px solid var(--blue-border)">
<h3 style="color:var(--blue-text)">{mkt['short']} 本頁（cap1.5＋均線確認）vs 實單主系統（cap1.5，唯讀對照・主系統數據截至 {main_data_date}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
下表為<b>實單主系統</b>當前讀數，直接讀取 state.json，唯讀不寫入、不受本頁影響。差異只來自套袖上限——本頁均線不配合時 cap_eff 退回 1.0，主系統固定 1.5。
主系統組合目標 <b>{tgt_sum:.1f}%</b>、執行層現持 <b>{exe_sum:.0f}%</b>。</p>
<table><thead><tr><th>腿</th><th class="num">閘門</th><th class="num">RV20</th><th class="num">σ_t</th><th class="num">raw ratio</th><th class="num">目標</th><th class="num">現持</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>"""


def _cmp_chart_js(suf: str, cmp: dict) -> str:
    """本頁 vs 主系統雙線曝險比較圖的 Chart.js 區塊。cmp['available']=False 時不產生
    canvas 對應的 dataset（頁面端該卡片本身也會略過渲染），回傳空字串，不偽造資料。"""
    if not cmp or not cmp.get("available"):
        return ""
    return f"""
var CMP_LAB_{suf}={cmp['labels']},CMP_SHADOW_{suf}={cmp['shadow']},CMP_MAIN_{suf}={cmp['main']};
new Chart(document.getElementById('chart-cmp-{suf}'),{{
  type:'line',
  data:{{labels:CMP_LAB_{suf},datasets:[
    {{label:'本頁（均線確認）現持',data:CMP_SHADOW_{suf},borderColor:GREEN,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,tension:0}},
    {{label:'實單主系統現持',data:CMP_MAIN_{suf},borderColor:BLUE,borderWidth:2,borderDash:[5,3],stepped:true,pointRadius:0,pointHoverRadius:3,tension:0}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{min:0,max:150,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});
"""


def _cmp_card_html(suf: str, cmp: dict, mkt: dict) -> str:
    """本頁 vs 主系統執行層曝險雙線圖卡片。cmp 不可用時顯示誠實提示（不畫假圖）。"""
    if not cmp or not cmp.get("available"):
        return (f'<div class="card"><h3>{mkt["short"]} 本頁 vs 實單主系統 — 執行層曝險時間軸對照</h3>'
                '<p style="font-size:.82rem;color:var(--muted)">兩邊歷史尚無重疊日期，暫無法對照（本頁剛建立，需與主系統累積共同的實錄天數後才會出現對照線）。</p></div>')
    return f"""<div class="card">
<h3>{mkt['short']} 執行層曝險時間軸對照 — 本頁（均線確認）vs 實單主系統</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
兩條線都是<b>執行層現持</b>（A2 20pp 門檻＋10% 取整後的實際組合曝險，非每日理論目標），差異僅來自套袖上限（本頁均線不配合時 cap_eff 退回 1.0）。
交集窗 {cmp['span']}，共 {cmp['n']} 個交易日。</p>
<div class="chart-wrap"><canvas id="chart-cmp-{suf}"></canvas></div>
</div>"""


def market_html(mkt: dict, sigs: dict, md: dict) -> str:
    legs = mkt["legs"]
    exec_finals = md["exec_finals"]
    ccol = md["ccol"]
    finals = md["finals"]
    suf = mkt["key"]
    cards = "".join(ticker_card(t, sigs[t]) for t in legs)
    dual, combined, exec_combined = _dual_breakdown(legs, finals, exec_finals)
    return f"""<div class="mkt-section" id="mkt-{suf}" data-market="{suf}">
<div class="mkt-hd"><span class="mkt-tag">{mkt['name']}</span></div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>{mkt['short']} 組合曝險</span></div>
  <div class="status-exposure" style="display:flex;gap:1.4rem;justify-content:center;align-items:baseline;flex-wrap:wrap">
    <span>目標 {combined:.0f}%<span style="font-size:.4em;color:var(--muted);font-weight:600"> 訊號</span></span>
    <span style="opacity:.55;font-size:.7em">／</span>
    <span>現持 {exec_combined:.0f}%<span style="font-size:.4em;color:var(--muted);font-weight:600"> 執行層</span></span>
  </div>
  <div style="font-size:.8rem;color:var(--muted)">{dual}。</div>
</div>

<div class="card">
<h3>{mkt['short']} 當前部位視覺 — 合成曝險量表 × 每腿乘法鏈</h3>
<div class="viz-split">
  <div>
    <div class="gauge-box">
      <canvas id="chart-gauge-{suf}"></canvas>
      <div class="gauge-center"><div class="g-num hero-{ccol}" style="color:var(--{ccol})">{combined:.0f}%</div><div class="g-lab">目標曝險（訊號）· 現持 {exec_combined:.0f}%</div></div>
    </div>
  </div>
  <div>
    <div class="chart-wrap-xs"><canvas id="chart-chain-{suf}"></canvas></div>
  </div>
</div>
<div style="font-size:.76rem;color:var(--muted);margin-top:.7rem"><b>每腿以自身滿載＝100% 顯示</b>（cap 1.5 上限 150%；合成曝險量表仍為組合層 0~150%，不變）＝<b style="color:var(--text)">最終持有</b> ＋ <b style="color:var(--amber-text)">套袖折減</b>（高波減碼）＋ <b>閘門關閉</b>（出場歸零）。{legs[0]} 自身滿載 {md['fill_self'][0]:.0f}%（組合 pp {finals[0]:.0f}%）、{legs[1]} 自身滿載 {md['fill_self'][1]:.0f}%（組合 pp {finals[1]:.0f}%）。</div>
</div>

<div class="card">
<h3>{mkt['short']} 近五年權重時間軸 — 現持（執行層）vs 每日理論目標</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
<b style="color:var(--text)">粗階梯線＝現持（執行層）</b>＝A2 20pp 門檻＋10% 取整＋clamp 150% 的實際持股率（跨門檻才動）；<b>細線＝每日理論目標（訊號）</b>（未過門檻不調）。
末端值：{dual}。
線段<b>實線＝每日實錄</b>、<b>虛線＝規則回放</b>（首次生成往回重算，誠實區隔）。窗 {md['span']}，共 {md['nhist']} 個交易日（回放 {md['n_replay']}／實錄 {md['n_live']}）。</p>
<div class="chart-wrap"><canvas id="chart-weights-{suf}"></canvas></div>
<div class="legend-note">
  <span class="ln-item"><span class="ln-line" style="border-top-width:3px"></span>執行層（粗階梯）</span>
  <span class="ln-item"><span class="ln-line" style="border-top-color:rgba(120,120,120,.5)"></span>每日理論目標（細）</span>
  <span class="ln-item"><span class="ln-line"></span>每日實錄</span>
  <span class="ln-item"><span class="ln-line ln-dash"></span>規則回放</span>
</div>
<h3 style="margin-top:1.1rem">{mkt['short']} 近五年套袖觸發脈絡 — RV20 vs σ_t（動態）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
本頁 σ_t 是<b>動態線</b>（近 3 年 RV20 滾動中位數），不是固定 σ 版的水平虛線。當 RV20（實線）升破自身 σ_t（虛線）時套袖按比例減碼；RV20 ≤ σ_t 時滿載。regime 抬升時 σ_t 跟著上移，是這頁與固定 σ 版的唯一機制差異。</p>
<div class="chart-wrap-sm"><canvas id="chart-rv-{suf}"></canvas></div>
<h3 style="margin-top:1.1rem">{mkt['short']} 近五年槓桿燃料表 — σ_t/RV 原始比率</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
σ_t/RV &gt; <b>1.0</b>（下虛線）＝當下比自身近 3 年平靜、cap 1.5 開始借錢；&gt; <b>1.5</b>（上虛線）＝連 cap 1.5 也滿載 150%。崩盤時比率暴跌到 1 以下、槓桿自動關閉。上方時間軸的綠粗階梯＝本頁 cap 1.5 執行；比率超過 1.0 的部分就是「借的錢」。</p>
<div class="chart-wrap-sm"><canvas id="chart-fuel-{suf}"></canvas></div>
</div>

{events_card(mkt, md['events'])}

<div class="tgrid">{cards}</div>

{md.get('main_snapshot_html', '')}

{md.get('cmp_card_html', '')}

{"".join(recent_table(t, sigs[t]) for t in legs)}

{backtest_section(mkt)}

{era_section(mkt)}

{annual_perf_section(mkt)}
</div>
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
// 0~150 刻度：base（≤100）＋ 槓桿段（>100，紅）＋ 現金
new Chart(document.getElementById('chart-gauge-{suf}'),{{
  type:'doughnut',
  data:{{labels:['曝險','槓桿 (&gt;100%)','現金'],datasets:[{{data:[{min(100.0,combined):.1f},{max(0.0,combined-100):.1f},{max(0.0,150-combined):.1f}],
    backgroundColor:['{CCOL_HEX}','#dc2626','#ece7db'],borderWidth:0}}]}},
  options:{{rotation:-90,circumference:180,cutout:'72%',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:function(c){{return c.label+': '+c.parsed.toFixed(1)+'%'}}}}}}}}}}
}});

new Chart(document.getElementById('chart-chain-{suf}'),{{
  type:'bar',
  data:{{labels:['{legs[0]}','{legs[1]}'],datasets:[
    {{label:'最終持有',data:{md['C_FINALS']},backgroundColor:[GREEN,AMBER],borderWidth:0,stack:'s'}},
    {{label:'套袖折減',data:{md['C_SLEEVE']},backgroundColor:'rgba(161,98,7,0.28)',borderWidth:0,stack:'s'}},
    {{label:'閘門關閉',data:{md['C_GATE']},backgroundColor:'rgba(120,120,120,0.22)',borderWidth:0,stack:'s'}}
  ]}},
  options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:true,position:'bottom',labels:{{usePointStyle:true,pointStyle:'rect',padding:10,boxWidth:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.x.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{stacked:true,min:0,max:150,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}}}}}},
      y:{{stacked:true,grid:{{display:false}}}}}}
  }}
}});

var W_LAB_{suf}={H['labels']},W_SRC_{suf}={H['src']};
function segDash_{suf}(ctx){{return W_SRC_{suf}[ctx.p1DataIndex]==='live'?undefined:[3,3];}}
new Chart(document.getElementById('chart-weights-{suf}'),{{
  type:'line',
  data:{{labels:W_LAB_{suf},datasets:[
    {{label:'合成執行 cap 1.5',data:{H['cexe']},borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.09)',
     borderWidth:2.8,stepped:true,pointRadius:0,pointHoverRadius:3,fill:'origin',segment:{{borderDash:segDash_{suf}}}}},
    {{label:'{legs[0]} 執行',data:{H['aexe']},borderColor:BLUE,borderWidth:1.6,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash_{suf}}}}},
    {{label:'{legs[1]} 執行',data:{H['bexe']},borderColor:AMBER,borderWidth:1.6,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash_{suf}}}}},
    {{label:'100% 分界',data:W_LAB_{suf}.map(function(){{return 100;}}),borderColor:'rgba(120,120,120,0.55)',borderWidth:1,borderDash:[2,3],pointRadius:0}},
    {{label:'合成目標（理論）',data:{H['comb']},borderColor:'rgba(22,163,74,0.35)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{title:function(c){{return c[0].label+' · '+(W_SRC_{suf}[c[0].dataIndex]==='live'?'每日實錄':'規則回放')}},
        label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{min:0,max:155,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
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

// 槓桿燃料表：σ_t/RV 比率 vs 1.0/1.5 參考線
new Chart(document.getElementById('chart-fuel-{suf}'),{{
  type:'line',
  data:{{labels:W_LAB_{suf},datasets:[
    {{label:'σ_t/RV',data:{H['fuel']},borderColor:AMBER,borderWidth:1.5,pointRadius:0,pointHoverRadius:3,tension:0.1}},
    {{label:'1.0（開始借錢）',data:W_LAB_{suf}.map(function(){{return 1.0;}}),borderColor:'rgba(22,163,74,0.7)',borderWidth:1,borderDash:[5,4],pointRadius:0}},
    {{label:'1.5（滿載 150%）',data:W_LAB_{suf}.map(function(){{return 1.5;}}),borderColor:'rgba(220,38,38,0.7)',borderWidth:1,borderDash:[5,4],pointRadius:0}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(2)}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{beginAtZero:true,suggestedMax:2.5,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{font:{{size:10}}}}}}}}
  }}
}});

{_cmp_chart_js(suf, md.get('cmp'))}
"""


def market_switch_buttons() -> str:
    """一鍵切換美股／台股的 pill 按鈕列（沿用頁首既有 pill 視覺語言）。純前端切換
    ——兩市場區塊仍全部由伺服器端產生，JS 只負責顯示／隱藏＋localStorage 記憶；
    無 JS 時兩市場皆維持可見（降級安全）。預設美股（MARKETS[0]）為 active。"""
    btns = ""
    for i, m in enumerate(MARKETS):
        active = " active" if i == 0 else ""
        btns += (f'<button type="button" class="mkt-switch-btn{active}" data-mkt="{m["key"]}" '
                 f'onclick="switchMarket(\'{m["key"]}\')">{m["name"]}</button>\n')
    return btns


# ---------------------------------------------------------------------------
# 「今天結論」box（2026-09-10，頁面最上方三句白話）— 全部沿用既有已算好的值
# （sigs 的 gate/final/wk_close/w52、exp、last_change_date/desc），不新增任何指標。
# ---------------------------------------------------------------------------
def today_conclusion(sigs: dict, exp: dict, last_change_date: str | None,
                     last_change_desc: str | None) -> str:
    # 句 1：現在持有什麼（各腿權重＋帳戶曝險）
    leg_bits = []
    for m in MARKETS:
        parts = [f"{t} {sigs[t]['final']*100:.0f}%（{'在場' if sigs[t]['gate'] else '出場'}）"
                 for t in m["legs"]]
        leg_bits.append(f"{m['short']}＝{'＋'.join(parts)}，帳戶目標曝險 {exp[m['key']]:.0f}%")
    holding = "現在持有：" + "；".join(leg_bits) + "。"

    # 句 2：最近一次變動——哪天、發生了什麼（沿用 detect_changes 已寫入 state 的敘述）
    if last_change_date:
        changed = f"最近一次執行層變動：{last_change_date}，{last_change_desc or '（無敘述）'}。"
    else:
        changed = "最近一次執行層變動：尚無紀錄（近期沒有任何一腿的目標與現持差達到 20 個百分點的調整門檻）。"

    # 句 3：下一個可能觸發的條件——挑離 W52 閘門最近的一腿；在場＝還要跌多少才出場，
    # 出場＝還要漲多少才重新進場（距離＝既有 wk_close/w52 現算的百分比差，非新指標）。
    trig = []
    for t in ALL_TICKERS:
        d = sigs[t]
        d52 = (d["wk_close"] / d["w52"] - 1) * 100 if d["w52"] else 0.0
        trig.append((abs(d52), t, d52, d["gate"]))
    trig.sort(key=lambda x: x[0])
    _, tt, td52, tgate = trig[0]
    if tgate:
        nxt = (f"下一個可能觸發：{tt} 目前週收在 W52（過去 52 週收盤均線，本系統用它判斷長期趨勢方向"
               f"的閘門）之上 {abs(td52):.1f}%，若週收跌破 W52 即觸發出場（仍須配合執行層 A2——"
               f"目標與現持差要達到 20 個百分點門檻才會真的調整部位、且取整至 10% 一格）。")
    else:
        nxt = (f"下一個可能觸發：{tt} 目前已出場（週收在 W52 之下 {abs(td52):.1f}%），"
               f"需要週收漲回 W52 之上才會重新觸發進場。")

    return f"""<div class="card" style="border:2px solid var(--brand);background:#eef4ff">
<h3 style="color:var(--brand)">今天結論</h3>
<div class="rule-list" style="font-size:.88rem">
{holding}<br>
{changed}<br>
{nxt}
</div>
<div style="font-size:.72rem;color:var(--muted);margin-top:.6rem;line-height:1.7">
名詞：<b>W52</b>＝過去 52 週（約一年）收盤價的平均線，本系統用它當長期趨勢的進出場閘門（週收在上方視為多頭、在下方視為空頭）；
<b>套袖（自適應波動率）</b>＝波動低於自身近 3 年中位數時加碼、波動升高時自動減碼的機制；
<b>cap_eff</b>＝本頁的曝險上限，均線五條件全對時是 1.5（同實單）、任一條不對時退回 1.0（本頁與實單主系統唯一的差異）；
<b>執行層／A2</b>＝目標權重與現持部位差要達到 20 個百分點門檻才真的調整，避免天天微調。
</div>
</div>"""


# ---------------------------------------------------------------------------
# Full HTML
# ---------------------------------------------------------------------------
def generate_html(sigs: dict, changes: list | None, last_change_date: str | None,
                  hist_map: dict, exec_map: dict, main_state: dict | None = None,
                  last_change_desc: str | None = None) -> str:
    changes = changes or []
    main_state = main_state or {}
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    data_date = max(sigs[t]["wk_date"] for t in ALL_TICKERS)
    # 週線 bar 由 pandas 以「週結束的週五」為標籤，故週間跑時 data_date 會是本週五
    # （尚未到）。用日線最新交易日判斷本週是否已收：daily < 週五標記＝本週進行中，
    # 顯示須誠實標暫定，不可寫成「週五收盤」（見 2026-07-22 用戶回報）。
    daily_dates = [hist_map[m["key"]][-1]["date"] for m in MARKETS if hist_map.get(m["key"])]
    latest_daily = max(daily_dates) if daily_dates else data_date
    week_provisional = latest_daily < data_date
    data_asof_label = (
        f"數據截至 {latest_daily}（本週最新交易日｜週線 bar 進行中，週五 {data_date} 收盤前為暫定）"
        if week_provisional else
        f"數據截至 {data_date}（週五收盤）")

    md_map = {m["key"]: _market_data(m, sigs, hist_map.get(m["key"], []), exec_map[m["key"]]) for m in MARKETS}
    for m in MARKETS:
        md = md_map[m["key"]]
        cmp = main_vs_shadow_series(m["key"], hist_map.get(m["key"], []), exec_map[m["key"]], main_state)
        md["cmp"] = cmp
        md["cmp_card_html"] = _cmp_card_html(m["key"], cmp, m)
        md["main_snapshot_html"] = main_snapshot_card(m["key"], main_state)
    exp_us = md_map["us"]["combined"]
    exp_tw = md_map["tw"]["combined"]
    today_conclusion_html = today_conclusion(sigs, {"us": exp_us, "tw": exp_tw},
                                             last_change_date, last_change_desc)

    change_html = (
        ('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;'
         'padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">'
         '可行動變化（僅頁面顯示，本頁無 email）</b><br>' + "<br>".join(changes) +
         '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>')
        if changes else
        ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">'
         '無可行動變化（四腿目標與現持執行層差皆 < 20pp；閘門翻轉本身不觸發，須一併達 20pp 門檻；本頁無 email）' +
         (f'（上次變化：{last_change_date}）' if last_change_date else '') + '</div>'))

    markets_html = "\n".join(market_html(m, sigs, md_map[m["key"]]) for m in MARKETS)
    markets_js = "\n".join(market_js(m, md_map[m["key"]]) for m in MARKETS)
    mkt_keys_js = json.dumps([m["key"] for m in MARKETS])   # 切換白名單，順序即預設優先序

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>cap 1.5＋日線均線確認（美+台）｜唯讀影子追蹤 | InvestMQuest Research</title>
  <meta name="description" content="W52 × 自適應波動率 cap 1.5＋日線均線長多確認（持有人 2026-09-15 提案）· 美股 QQQ+SMH ＋ 台股 0050+2330 · 唯讀影子追蹤頁，不採用為實單、無 email · 均線不配合時 cap_eff 退回 1.0">
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
.mkt-switch-row{{display:flex;gap:.4rem;flex-wrap:wrap;align-items:center;margin-top:.6rem}}
.mkt-switch-label{{font-size:.78rem;color:var(--muted);margin-right:.1rem}}
.mkt-switch-btn{{font:inherit;font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;
  border:1px solid var(--border);background:transparent;color:var(--muted);cursor:pointer;line-height:1.3}}
.mkt-switch-btn.active{{background:var(--text);color:#fff;border-color:var(--text)}}
.mkt-switch-btn:hover{{border-color:var(--brand)}}
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
<div class="container" style="padding-top:1rem">
{today_conclusion_html}
</div>
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/long-track/#live">W52 × 自適應波動率（實單主系統）</a> / cap 1.5＋日線均線確認</div>
    <h1>cap 1.5＋日線均線確認 — 唯讀影子追蹤</h1>
    <div class="sub">美股 QQQ+SMH ＋ 台股 0050+2330 · 持有人 {PROPOSAL_DATE} 提案：均線五條件不全對時，借錢加碼的上限（cap_eff）退回 <b>1.0</b>；五條全對時同實單 <b>1.5</b>。閘門、套袖分母、執行層與<a href="/long-track/#live">實單主系統</a>逐位元相同。<b>本頁唯讀、不採用為實單、無 email</b>。</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem;flex-wrap:wrap">
      <a href="/long-track/#live" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">實單主系統 cap 1.5</a>
      <a href="/long-track-w52-adaptive/leverage.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">cap 1.0 影子對照</a>
      <a href="/long-track-w52-adaptive/tw-semivol.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">台股 B-ii 影子（唯讀）</a>
      <a href="/long-track-w52-adaptive/ma-confirm.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">cap 1.5＋均線確認（本頁）</a>
    </div>
    <div class="mkt-switch-row" role="group" aria-label="市場切換（美股／台股）">
      <span class="mkt-switch-label">看單一市場：</span>
      {market_switch_buttons()}
      <noscript><span style="font-size:.76rem;color:var(--muted)">（JS 關閉中：以下同時顯示美股與台股全部區塊）</span></noscript>
    </div>
  </div>
</div>
<div class="container">

<div class="oos-banner">
  <span class="tag-loud">唯讀影子追蹤・持有人 {PROPOSAL_DATE} 提案・無 email・不構成倉位建議</span>
  <div style="font-size:.86rem">本頁追蹤持有人 {PROPOSAL_DATE} 提出的候選規則：<b>實單主系統只在平靜 regime（σ_t/RV20 &gt; 1）借錢加碼到 150%；本頁多加一道「日線均線長多確認」——均線五條件（收盤 &gt; MA60／MA120／MA200、MA120／MA200 斜率向上，lag {MA_LAG}）全對時 cap_eff = 1.5（同實單），任一條不對時 cap_eff 退回 1.0</b>。W52 閘門、套袖分母（RV20、σ_t）、執行層 A2（20pp／10%／clamp 75pp）與<a href="/long-track/#live">實單主系統</a><b>逐位元相同</b>，唯一差異就是這道均線確認。
  <br><br><b>本頁不採用為實單、無獨立 email</b>——可行動變化只顯示在頁面上，任何通知一律由實單主系統覆蓋。凍結規則、不調參，見下方「追蹤規則」與回測表。</div>
</div>

<div class="dual-stat">
  <div class="ds"><div class="dsn hero-{md_map['us']['ccol']}" style="color:var(--{md_map['us']['ccol']})">{exp_us:.0f}%</div><div class="dsl">美股 QQQ+SMH 組合目標曝險（本頁）</div></div>
  <div class="ds"><div class="dsn hero-{md_map['tw']['ccol']}" style="color:var(--{md_map['tw']['ccol']})">{exp_tw:.0f}%</div><div class="dsl">台股 0050+2330 組合目標曝險（本頁）</div></div>
</div>
<div class="status-date" style="text-align:center;margin-bottom:.5rem">{data_asof_label} · 頁面更新 {now} 台北時間 · 兩組合各自獨立追蹤（各 100%）</div>

{change_html}

{markets_html}

<div class="card">
<h3>追蹤規則（cap 1.5＋日線均線確認；持有人 {PROPOSAL_DATE} 提案，凍結不調參）</h3>
<div class="rule-list">
① <b>四腿、兩市場</b>：美股 {{QQQ, SMH}} 各 50%、台股 {{0050, 2330}} 各 50%（.TW，內嵌幻影分割修復）。兩組合各自獨立追蹤（各 100%），日報酬 50/50 加權合成（<b>絕不直接相加 equity curve</b>）。<br>
② <b>週線 W52 單線閘門</b>（W-FRI）：<b>週收盤 &gt; SMA52w 在場、&lt; SMA52w 出場</b>；與實單主系統逐位元相同，不受本頁均線條件影響。<br>
③ <b>自適應波動率套袖分母</b>：σ_t＝RV20 的 <b>rolling(756, min_periods=252).median()</b>；raw_ratio＝σ_t／RV20；與實單主系統逐位元相同。<br>
④ <b>日線均線長多確認（本頁唯一新增條件）</b>：以 auto-adjust 收盤價算 <code>ma60/ma120/ma200</code>；五條件——收盤 &gt; MA60、收盤 &gt; MA120、收盤 &gt; MA200、MA120 今日 &gt; MA120 {MA_LAG} 個交易日前、MA200 今日 &gt; MA200 {MA_LAG} 個交易日前——<b>全對 → cap_eff = 1.5</b>（同實單）；<b>任一條不對 → cap_eff 退回 1.0</b>。<b>w = min(cap_eff, raw_ratio)</b>。三個價格條件（收盤 vs MA60/120/200）各加 <b>1% 遲滯</b>：條件目前關，收盤要漲過 MA 才轉開；目前開，收盤要跌破 MA×99% 才轉關；介於中間沿用前一日狀態。兩個斜率條件不受影響。<b>2026-09-15 同日修訂</b>：收盤貼著 MA60 天天翻，會讓執行層跟著抖動，加遲滯後年執行層變動次數下降，回測判準（兩市場同時：變動次數不高於無遲滯版、CAGR 不低於無遲滯版逾 0.2pp、MDD 不深於無遲滯版逾 0.5pp）通過，採用 1% 緩衝。<br>
⑤ <b>機制與視窗凍結</b>：W52 閘門、滾動中位數 3 年（756／252）、均線 lag {MA_LAG} 皆鎖死，<b>此後不再調整</b>；不掃參擇優、不改機制形狀、不加濾網後重跑（lag 5/60 結論相同，見回測表）。<br>
⑥ <b>執行</b>：t 收盤訊號、t+1 收盤生效；成本 7 bps／邊。<br>
⑦ <b>最終權重</b> = 0.5 × 閘門(0/1) × 套袖權重，每市場兩腿各自計算。<br>
⑧ <b>資料揭露</b>：yfinance auto-adjust（還原股價）；0050.TW 2014-01-02 幻影分割壞 bar 由腳本自動修復；0050 免費歷史約 2009 起。台股 2330 佔 0050 約五成，50/50 組合等效台積電曝險 ≈ 75%，非分散組合。<br>
⑨ <b>執行層 A2（同實單主系統）</b>：|目標 − 現持| ≥ 20pp 才調整，調整取整至 10% 格、再 clamp 於 50×1.5＝75pp（<b>固定，不隨 cap_eff 變動</b>）；<b>回測主數字含此執行層</b>。<br>
<span style="color:var(--muted);font-size:.78rem">閘門為週頻（僅週五可能翻轉），套袖 RV20／σ_t／均線條件皆為日頻，故本頁每交易日更新（台股收盤後、美股收盤後各一次，date-keyed 冪等）。<b>本頁無 email</b>——可行動變化只顯示在頁面上，不觸發任何通知。</span>
</div>
</div>

<div class="card" style="border:2px solid var(--blue-border)">
<h3 style="color:var(--blue-text)">預註冊採用判準（{PROPOSAL_DATE}）</h3>
<div class="rule-list" style="font-size:.86rem">
預註冊（2026-09-15）：本頁與實單並行 ≥ 60 交易日後、於 2026-10 回顧點比較三件事——(a) 市場已從高點跌超過 5% 仍持有超過 100% 曝險的天數，(b) 執行層變動次數，(c) 兩條執行層淨值差。本頁不自動採用；回測顯示美股 Calmar 持平（0.60→0.61、CAGR −0.3pp）、台股變差（1.24→1.14、CAGR −1.5pp），這是用報酬買心理壓力，數字上沒有理由自動採用。
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research · cap 1.5＋日線均線確認（美+台）· 唯讀影子追蹤・實單主系統見 <a href="/long-track/#live">/long-track/#live</a></div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
<script>
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;
var GREEN="#16a34a",BLUE="#1565c0",AMBER="#d97706";
function _dd(nav){{var dd=[],pk=0;for(var i=0;i<nav.length;i++){{if(nav[i]>pk)pk=nav[i];dd.push((nav[i]/pk-1)*100);}}return dd;}}
{markets_js}

// ---- 一鍵切換美股／台股（純前端，兩市場區塊皆由伺服器端產出，僅切顯示；
//      務必等所有 Chart.js 圖表建立完成後才隱藏非選取市場，避免隱藏容器內
//      canvas 量到 0 寬高）----
var MKT_LS_KEY = 'ltw52_market';
function switchMarket(key){{
  document.querySelectorAll('.mkt-section').forEach(function(el){{
    el.style.display = (el.getAttribute('data-market') === key) ? '' : 'none';
  }});
  document.querySelectorAll('.mkt-switch-btn').forEach(function(b){{
    b.classList.toggle('active', b.getAttribute('data-mkt') === key);
  }});
  try {{ localStorage.setItem(MKT_LS_KEY, key); }} catch(e) {{}}
}}
// 合法市場 key 由 MARKETS 推導；未通過白名單的值一律落回預設，避免 MARKETS 增減
// 或改 key 後，老訪客殘留的 localStorage 值讓每個區塊都被隱藏（整頁空白）。
var MKT_KEYS = {mkt_keys_js};
function _mktValid(k){{ return MKT_KEYS.indexOf(k) !== -1; }}
(function(){{
  var saved = MKT_KEYS[0];
  try {{
    var v = localStorage.getItem(MKT_LS_KEY);
    if (_mktValid(v)) saved = v;
    else if (v !== null) localStorage.removeItem(MKT_LS_KEY);   // 清掉失效的殘留值
  }} catch(e) {{}}
  var h = (location.hash || '').replace('#', '');
  if (_mktValid(h)) saved = h;   // 頁內／外部若帶 #us 或 #tw 錨點，切到對應市場
  switchMarket(saved);
}})();
window.addEventListener('hashchange', function(){{
  var h = (location.hash || '').replace('#', '');
  if (_mktValid(h)) switchMarket(h);
}});
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# change detection — 本頁無 email，detect_changes 只用於 log／頁面顯示，不寫 alert 檔
# ---------------------------------------------------------------------------
def detect_changes(prev: dict, sigs: dict) -> list:
    """可行動變化＝任一腿今日目標與現持（執行層 executed_pct）差 ≥ 20pp（EXEC_BAND，
    與回測 A2 執行層 band_exec_replay 用同一個門檻）。閘門翻轉本身不是獨立觸發條件——
    若翻轉後的目標仍落在 20pp 門檻內，A2 不會調整部位。held is None（首次執行、無前一次
    executed_pct 紀錄，無法比較門檻）時仍視為需要通知。本頁無 email——本函式只供 log
    與頁面 change_html 顯示用，不寫任何 alert／mail 檔案。"""
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
        drift = held is None or abs(target - held) >= EXEC_BAND
        if drift:
            new_exec = min(round(target / EXEC_GRID) * EXEC_GRID, EXEC_CLAMP)
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

    main_state = load_main_state()   # 唯讀：實單主系統 state.json（供對照卡／雙線圖）

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

    # 本頁無 email／alert：僅 log，供人工複審對照（可行動變化仍顯示於頁面 change_html）。
    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES (shadow, no email): {last_change_desc}")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        print("No actionable change vs last run (shadow).")

    html = generate_html(sigs, changes, last_change_date, hist_map, exec_map,
                         main_state=main_state, last_change_desc=last_change_desc)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "ruleset_locked_date": FREEZE_DATE,
        "candidate_proposal_date": PROPOSAL_DATE,
        "mechanism": "W52 gate x adaptive sigma_t (RV20 rolling(756,252) median) x cap_eff (1.5 if daily-MA-score5 long-confirm else 1.0, lag %d, price conditions w/ %.0f%% hysteresis since 2026-09-15) x exec layer A2 20pp/10%%round/clamp fixed 75pp" % (MA_LAG, MA_BUF * 100),
        "status": "READ-ONLY SHADOW tracking page (holder proposal %s); not adopted as live rule; no email; review point 2026-10 (>=60 tracking days)" % PROPOSAL_DATE,
        "not_a_live_signal": True,
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
        "weights": WEIGHTS,
        "combined_exposure_us_pct": round(exp["us"], 1),
        "combined_exposure_tw_pct": round(exp["tw"], 1),
        "tickers": {
            t: {
                "market": TICKER_MARKET[t],
                "gate": sigs[t]["gate"],
                "sigma_t_pct": round(sigs[t]["sigma_t"] * 100, 2),
                "rv20_pct": round(sigs[t]["rv20"] * 100, 2),
                "raw_ratio": round(sigs[t]["raw_ratio"], 4),
                "levered": sigs[t]["levered"],
                "sleeve_weight": round(sigs[t]["sleeve"], 4),
                "ma5_on": sigs[t]["ma5_on"],
                "cap_eff": sigs[t]["cap_eff"],
                "ma_cond": sigs[t]["ma_cond"],
                "sleeve_variant": sigs[t]["sleeve_variant"],
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
