#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兩檔配法比較器的共用函式（美股 etf-dash 與台股 active-etf 兩支 build_compare_data.py 共用）。

負責三件事：取價（price_store 或 yfinance，兩者回傳同一種表）、把序列轉成「起日索引＋數值陣列」
的小檔格式、找基準回檔 ≥10% 的區段。價格與匯率的對齊規則寫在各 build 腳本。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
V7_ROOT = Path.home() / "v7-backtest"
DECIMALS = 5
SCALE = 10 ** DECIMALS
SCHEMA = "compare-series-v1"

# 1475.T（TOPIX ETF）：Yahoo 還原係數在 2024-08-09 一次跳 16.1%，其餘半年配息約 1%，判斷是壞的配息記錄。
# 把該日以前的還原價乘上這個常數，讓當日的跳動回到中位數。1.1496 是 2026-10-28 深度檢驗用同一組資料
# 反推的估計值（跳動 ÷ 其餘配息跳動的中位數），不是官方配息資料。
TOPIX_ADJ_FIX = 1.1496
TOPIX_BAD_BAR_DAYS = ("2024-08-08", "2024-08-09")
TOPIX_FIX_DAY = "2024-08-09"


def _norm_index(idx) -> pd.DatetimeIndex:
    idx = pd.DatetimeIndex(idx)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    return idx.normalize()


def load_bars(tk: str, source: str, start: str) -> pd.DataFrame:
    """回傳 DataFrame（index＝當地日期，欄 close／adj_close／volume）。
    close＝未還原收盤，adj_close＝含息還原收盤。source：price_store（本機）或 yfinance（雲端 CI）。"""
    if source == "price_store":
        sys.path.insert(0, str(V7_ROOT))
        from src.price_store import get_ohlcv  # noqa: E402
        df = get_ohlcv(tk, start=start)
        if df is None or df.empty:
            raise RuntimeError(f"price_store 沒有 {tk}")
        out = df[["close", "adj_close", "volume"]].copy()
        out.index = _norm_index(out.index)
    else:
        import yfinance as yf  # 延後 import：price_store 模式不需要
        sys.path.insert(0, str(REPO_ROOT / "scripts" / "etf_dash"))
        import build_etf_dash as etfdash  # noqa: E402 — 借 yf_call_with_backoff()

        h = etfdash.yf_call_with_backoff(
            lambda: yf.Ticker(tk).history(start=start, auto_adjust=False), label=f"compare {tk}")
        if h is None or h.empty:
            raise RuntimeError(f"yfinance 沒有 {tk}")
        h = h.copy()
        h.index = _norm_index(h.index)
        h = h[~h.index.duplicated(keep="last")]
        if "Adj Close" in h.columns:
            adj = h["Adj Close"]
        else:  # 新版 yfinance 若不給 Adj Close，改用 auto_adjust=True 的 Close
            ha = etfdash.yf_call_with_backoff(
                lambda: yf.Ticker(tk).history(start=start, auto_adjust=True), label=f"compare-adj {tk}")
            ha.index = _norm_index(ha.index)
            adj = ha["Close"].reindex(h.index)
        out = pd.DataFrame({"close": h["Close"], "adj_close": adj,
                            "volume": h["Volume"] if "Volume" in h.columns else np.nan})
    out = out[~out.index.duplicated(keep="last")].sort_index()
    out = out.dropna(subset=["close", "adj_close"])
    if tk == "0050.TW" and source != "price_store":
        out = fix_0050(out, [])
    return out


def fix_0050(bars: pd.DataFrame, notes: list[str]) -> pd.DataFrame:
    """0050.TW 的 Yahoo 原始資料（雲端 CI 用 yfinance 時）：2025-06 的 4:1 拆股只調整了 2014-01-02 以後，
    更早的價格仍是拆股前（高約 4 倍），把 2014-01-02 以前的價格除以 4。另刪除 2009-01-02～02-27 與 2009-03-06
    （日報酬與加權指數無關）。與 ~/v7-backtest/src/price_store.py 的 CORRECTIONS["0050.TW"] 同一套，
    price_store 模式的資料已經修過，比值檢查不會再套第二次。"""
    b = bars.copy()
    d0 = pd.Timestamp("2014-01-02")
    before, after = b[b.index < d0], b[b.index >= d0]
    if len(before) and len(after):
        ratio = float(after["close"].iloc[0] / before["close"].iloc[-1])
        if 0.8 * 0.25 <= ratio <= 1.25 * 0.25:
            m = b.index < d0
            b.loc[m, ["close", "adj_close"]] = b.loc[m, ["close", "adj_close"]] * 0.25
            if "volume" in b:
                b.loc[m, "volume"] = b.loc[m, "volume"] * 4.0
            notes.append("0050.TW 的 Yahoo 資料只把 2014-01-02 以後調成 2025-06 拆股後口徑，2014-01-02 以前的價格除以 4。")
    b = b[~(((b.index >= pd.Timestamp("2009-01-02")) & (b.index <= pd.Timestamp("2009-02-27")))
            | (b.index == pd.Timestamp("2009-03-06")))]
    return b


def fix_topix(bars: pd.DataFrame, notes: list[str]) -> pd.DataFrame:
    """剔除 1475.T 兩個壞 K 棒，並修正 2024-08-09 的壞配息還原係數。"""
    b = bars.copy()
    day = pd.Timestamp(TOPIX_FIX_DAY)
    ratio = (b["adj_close"] / b["close"])
    jump = float(ratio.pct_change().get(day, 0.0) or 0.0)
    if jump > 0.10:
        b.loc[b.index < day, "adj_close"] *= TOPIX_ADJ_FIX
        notes.append(f"1475.T 的 Yahoo 還原係數在 {TOPIX_FIX_DAY} 一次跳 {jump * 100:.1f}%，判斷為壞配息記錄；"
                     f"該日以前的還原價乘 {TOPIX_ADJ_FIX}（估計值，不是官方配息資料）。")
    else:
        notes.append(f"1475.T 在 {TOPIX_FIX_DAY} 的還原係數跳動只有 {jump * 100:.1f}%，未套用壞配息修正。")
    drop = [pd.Timestamp(d) for d in TOPIX_BAD_BAR_DAYS if pd.Timestamp(d) in b.index]
    b = b.drop(index=drop)
    notes.append(f"1475.T 在 {'、'.join(TOPIX_BAD_BAR_DAYS)} 兩天收盤偏離前後中位數一倍以上，整天剔除（以前一日順延）。")
    return b


def to_compact(values: pd.Series, calendar: pd.DatetimeIndex) -> tuple[dict, pd.Series]:
    """序列（已對齊 calendar、前段可能是 NaN）→ ({i0, q, start}, 指數序列)。
    指數的基期（第一個有值日）＝1，乘上 SCALE（1e5）四捨五入成整數存在 q：還原時 q / 1e5，精度 5 位小數，
    省掉小數點讓檔案小約 13%。"""
    s = values.reindex(calendar)
    first = s.first_valid_index()
    i0 = int(calendar.get_loc(first))
    v = s.iloc[i0:].astype(float)
    v = v / float(v.iloc[0])
    q = [int(round(float(x) * SCALE)) for x in v.values]
    return {"i0": i0, "q": q, "start": first.strftime("%Y-%m-%d")}, (pd.Series(q, index=v.index) / SCALE)


def drawdown_episodes(s: pd.Series, threshold: float = 0.10) -> list[dict]:
    """基準回檔 ≥ threshold 的區段：峰日、谷日、回前高日（還沒回到則 None）、跌幅%。
    與 2026-10-28 深度檢驗同口徑：價格回到或超過前高的第一天算回前高日。"""
    s = s.dropna()
    eps: list[dict] = []
    pk = s.index[0]
    mn = None
    inep = False
    for d, v in s.items():
        if v >= s.loc[pk]:
            if inep and mn is not None and s.loc[mn] / s.loc[pk] - 1 <= -threshold:
                eps.append({"peak": pk, "trough": mn, "recovery": d})
            pk, inep, mn = d, False, None
        else:
            inep = True
            if mn is None or v < s.loc[mn]:
                mn = d
    if inep and mn is not None and s.loc[mn] / s.loc[pk] - 1 <= -threshold:
        eps.append({"peak": pk, "trough": mn, "recovery": None})
    out = []
    for e in eps:
        out.append({"peak": e["peak"].strftime("%Y-%m-%d"), "trough": e["trough"].strftime("%Y-%m-%d"),
                    "recovery": e["recovery"].strftime("%Y-%m-%d") if e["recovery"] is not None else None,
                    "dd_pct": round((float(s.loc[e["trough"]] / s.loc[e["peak"]]) - 1) * 100, 2)})
    return out


def write_json(path: Path, payload: dict) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))
