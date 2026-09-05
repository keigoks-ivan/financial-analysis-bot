#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_crossasset_frozen.py — 凍結搬運版：v7-backtest crossasset D1 訊號（S-F 影子帳戶用）。

JUDGMENT CALL（見 Shadow_Tracks_Spec.md 開發交接）：fab 這支 repo 的 CI（GitHub
Actions）跑不到 /Users/ivanchang/v7-backtest 的本機路徑（grep scripts/ 與
.github/workflows/ 已確認：既有 v7 相依一律走「CANONICAL COPY + try/except
ImportError fallback」或「靜態轉錄常數」兩種既有慣例，從無跨 repo import）。
本檔即是「vendor 進 fab 的最小凍結函式集」，功能上逐行對齊 v7-backtest 下列
三支檔案（原始檔案路徑與函式名稱列於各函式 docstring）：

  - src/long_track_backtest/ensemble_experiment.py :: exec_dates / signal_daily /
    build_signals
  - src/long_track_backtest/supertrend_experiment.py :: weekly_ohlc
  - src/long_track_backtest/chandelier_tw_validation.py :: e3_pos / chand_gate /
    half_gate（HH=22／M=2.0／ATR_P=10 沿用 crossasset_system.py 常數）
  - src/long_track_backtest/taiwan_lt.py :: run_pos_tw 的每日報酬公式
    （p_prev*qr + (1-p_prev)*cr − turn*COST，COST=0.0007，逐字對齊）

JUDGMENT CALL（現金腿替代）：v7 原版 TSMOM 與 run_pos_tw 用的 cash 序列是
backtest_lto_qqq.load_cash_close()（SHY 接 BIL 的價格拼接，取自 v7 repo 內部
pickle 快照，fab 抓不到、也不該跨 repo 讀本機檔案）。本檔改用 yfinance 即時
抓 SHY（1-3y 公債 ETF，auto-adjust）當現金腿代理——SHY/BIL 兩者短率高度貼近，
差異遠小於本影子帳戶要看的訊號雜訊；SHY 現時仍在存續中所以不需要 BIL 銜接。
這條 JUDGMENT CALL 記入呼叫端 judgment_calls。

不做的事：不快取到 docs/（避免 D1 訊號被誤認為機械日更資料層）；不重算 v7 本身
任何回測結果；本檔輸出只餵 S-F 影子帳戶，不進系統實錄、不觸發任何帳本動作。
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import yfinance as yf

D1_LEGS = ["SPY", "TLT", "GLD", "DBC"]
CASH_PROXY_TICKER = "SHY"   # JUDGMENT CALL：v7 SHY→BIL 拼接的 fab 代理，見檔頭
HH = 22
MULT = 2.0
ATR_P = 10
TURNOVER_COST = 0.0007      # taiwan_lt.py COST，逐字對齊


def fetch_ohlc(ticker: str, period: str = "6y") -> pd.DataFrame:
    """對齊 taiwan_lt.py::load_ohlc 的抓取參數（auto_adjust=True），差別只在
    fab 這裡不落地 pickle 快取（每次即時抓，避免 docs/ 外新增快取檔的治理疑慮）。"""
    df = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index = pd.to_datetime(df.index)
    if getattr(df.index, "tz", None) is not None:
        df.index = df.index.tz_localize(None)
    return df[["Open", "High", "Low", "Close"]].dropna(subset=["Close"]).sort_index()


def exec_dates(px: pd.Series, freq: str) -> pd.Series:
    """逐字對齊 ensemble_experiment.py::exec_dates。"""
    return px.resample(freq).apply(lambda x: x.index[-1] if len(x) else pd.NaT).dropna()


def signal_daily(sig: pd.Series, ex: pd.Series, idx: pd.DatetimeIndex) -> pd.Series:
    """逐字對齊 ensemble_experiment.py::signal_daily。"""
    s = pd.Series(sig.values, index=ex.reindex(sig.index).values).dropna()
    s = s[~s.index.duplicated(keep="last")]
    return s.reindex(idx).ffill()


def build_signals(px: pd.Series, cash: pd.Series) -> dict:
    """逐字對齊 ensemble_experiment.py::build_signals（僅拿掉未用到的
    extra_wk_lens 參數；固定 W40/W52/TSMOM 三訊號與原版一致）。"""
    wk = px.resample("W-FRI").last().dropna()
    exw = exec_dates(px, "W-FRI")
    mo = px.resample("ME").last().dropna()
    exm = exec_dates(px, "ME")
    cash_m = cash.resample("ME").last()

    w40 = (wk > wk.rolling(40).mean()).astype(float)
    w52 = (wk > wk.rolling(52).mean()).astype(float)
    ts = ((mo / mo.shift(12) - 1) >
          (cash_m / cash_m.shift(12) - 1).reindex(mo.index).fillna(0)).astype(float)

    return {
        "W40": signal_daily(w40, exw, px.index),
        "W52": signal_daily(w52, exw, px.index),
        "TSMOM": signal_daily(ts, exm, px.index),
    }


def e3_pos(c: pd.Series, cash: pd.Series) -> pd.Series:
    """逐字對齊 chandelier_tw_validation.py::e3_pos（W40/W52/TSMOM 多數決／平均）。"""
    s = build_signals(c, cash)
    return (s["W40"] + s["W52"] + s["TSMOM"]) / 3


def weekly_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """逐字對齊 supertrend_experiment.py::weekly_ohlc。"""
    wk = pd.DataFrame({
        "High": df["High"].resample("W-FRI").max(),
        "Low": df["Low"].resample("W-FRI").min(),
        "Close": df["Close"].resample("W-FRI").last(),
        "exec_date": df["Close"].resample("W-FRI")
                       .apply(lambda x: x.index[-1] if len(x) else pd.NaT),
    }).dropna(subset=["Close"])
    return wk


def chand_gate(ohlc_df: pd.DataFrame, c: pd.Series, hh: int = HH, mult: float = MULT,
               atr_p: int = ATR_P) -> pd.Series:
    """逐字對齊 chandelier_tw_validation.py::chand_gate（HH=22／M=2.0／ATR_P=10，
    crossasset_system.py 凍結常數）。"""
    wk = weekly_ohlc(ohlc_df)
    h, l, cl = wk["High"], wk["Low"], wk["Close"]
    pc = cl.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / atr_p, adjust=False, min_periods=atr_p).mean()
    stop = cl.rolling(hh).max() - mult * atr
    gate_w = (cl > stop).where(stop.notna(), True).astype(float)
    return signal_daily(gate_w, wk["exec_date"], c.index).ffill().fillna(1.0)


def half_gate(e3: pd.Series, gate: pd.Series) -> pd.Series:
    """逐字對齊 chandelier_tw_validation.py::half_gate。"""
    return 0.5 * e3 + 0.5 * np.minimum(e3, gate)


def build_d1_positions(legs=None, cash_ticker: str = CASH_PROXY_TICKER):
    """回傳 (pos, px, cash)：pos[t]＝half_gate 每日部位（0..1）、px[t]＝腿收盤、
    cash＝現金代理收盤（SHY）。對齊 crossasset_system.py::build(gate=True) 的
    每腿部位邏輯（e3_pos 再套 half_gate(chand_gate)），但不跑 run_pos_tw 整段
    NAV 引擎——呼叫端只需要「今天的部位＋日報酬」餵影子帳戶簿記，不需要 v7 那
    支從 SIM_START 開始的完整回測淨值曲線。"""
    legs = legs or D1_LEGS
    cash_df = fetch_ohlc(cash_ticker)
    cash = cash_df["Close"]
    pos, px = {}, {}
    for t in legs:
        df = fetch_ohlc(t)
        c = df["Close"]
        e3 = e3_pos(c, cash)
        g = chand_gate(df, c)
        pos[t] = half_gate(e3, g).fillna(0.0)
        px[t] = c
    return pos, px, cash


def build_d1_daily_returns(legs=None, cash_ticker: str = CASH_PROXY_TICKER) -> dict:
    """回傳 {date_str: daily_return} 的 D1 basket（4 腿等權 0.25，逐腿用
    run_pos_tw 的日報酬公式：p_prev*qr + (1-p_prev)*cr − |Δp|*7bps，
    taiwan_lt.py::run_pos_tw 逐字對齊，COST=0.0007）。用 SPY 的交易日曆為主
    軸（4 腿皆為美股 ETF，交易日曆一致；缺值 reindex+ffill 不捏造報酬——若
    仍缺值該日以 0 記並非本函式責任，由呼叫端在合併進系統實錄窗時對帳）。"""
    legs = legs or D1_LEGS
    pos, px, cash = build_d1_positions(legs, cash_ticker)
    idx = px[legs[0]].index
    for t in legs[1:]:
        idx = idx.intersection(px[t].index)
    idx = idx.sort_values()
    cash_aligned = cash.reindex(idx).ffill()
    cash_ret = cash_aligned.pct_change().fillna(0.0)

    pos_aligned = {t: pos[t].reindex(idx).ffill().fillna(0.0) for t in legs}
    px_aligned = {t: px[t].reindex(idx) for t in legs}

    out = {}
    for i in range(1, len(idx)):
        d = idx[i].strftime("%Y-%m-%d")
        r_total = 0.0
        for t in legs:
            p_prev = float(pos_aligned[t].iloc[i - 1])
            p_now = float(pos_aligned[t].iloc[i])
            p_now_px, p_prev_px = px_aligned[t].iloc[i], px_aligned[t].iloc[i - 1]
            if p_now_px != p_now_px or p_prev_px != p_prev_px or p_prev_px == 0:
                continue
            qr = float(p_now_px / p_prev_px - 1.0)
            cr = float(cash_ret.iloc[i])
            turn = abs(p_now - p_prev)
            r_leg = p_prev * qr + (1 - p_prev) * cr - turn * TURNOVER_COST
            r_total += r_leg / len(legs)
        out[d] = r_total
    return out, {t: {"pos_last": float(pos_aligned[t].iloc[-1]),
                      "gate_state_date": idx[-1].strftime("%Y-%m-%d")} for t in legs}
