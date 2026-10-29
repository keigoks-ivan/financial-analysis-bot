#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETF 儀表板總覽的「強弱」與「判讀」欄。

強弱：每檔基金近 63、252 個交易日（約 3 個月、12 個月）的含息報酬，減 SPY 同期含息報酬，單位百分點。
  - 交易日以 SPY 的交易日曆為準：終點＝SPY 最後一根，起點＝往前數 63（252）根。
  - 含息＝yfinance auto_adjust=True 的還原收盤（picks_candidates.fetch_total_return，含壞 K 棒處理）。
  - 台幣、日圓計價的基金除以當日匯率換成美元（同 picks_candidates 的做法：匯率 ffill 到基金日期）。
  - TAIEX（^TWII）是指數沒有配息，用價格指數，不含息。
  - 基金在起點日之前沒有資料、或最後一根比 SPY 終點早超過 5 天，給 None。
判讀：由「隱含本益比變動（3 個月）」在整數 bps 空間比較，見 align_label_zh()。
價格抓取失敗不丟例外，回空 dict（呼叫端沿用上一份總覽的舊值）。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

WINDOWS = {"rel_spy_3m_pct": 63, "rel_spy_12m_pct": 252}
BENCH = "SPY"
FX_TICKER = {"TWD": "TWD=X", "JPY": "JPY=X"}
MAX_STALE_DAYS = 5

ALIGN_THRESHOLD_BPS = 500
ALIGN_PRICE_AHEAD = "股價跑在獲利前面"
ALIGN_EPS_AHEAD = "獲利跑在股價前面"
ALIGN_MATCHED = "對得上"


def currency_of(yf_ticker: str | None) -> str:
    """同 picks_candidates／drawdown_episodes 的判斷：.TW、^TWII＝TWD；.T＝JPY；其餘 USD。"""
    t = yf_ticker or ""
    if t.endswith(".TW") or t == "^TWII":
        return "TWD"
    if t.endswith(".T"):
        return "JPY"
    return "USD"


def align_label_zh(implied_pe_chg_pct_90d: float | None) -> str | None:
    """隱含本益比 3 個月變動（%）→ 判讀文字。整數 bps 空間比較（bps = round(x*100)），
    >= +500 股價跑在獲利前面，<= −500 獲利跑在股價前面，其餘對得上，缺值 None。"""
    if implied_pe_chg_pct_90d is None:
        return None
    try:
        bps = round(float(implied_pe_chg_pct_90d) * 100)
    except (TypeError, ValueError):
        return None
    if bps >= ALIGN_THRESHOLD_BPS:
        return ALIGN_PRICE_AHEAD
    if bps <= -ALIGN_THRESHOLD_BPS:
        return ALIGN_EPS_AHEAD
    return ALIGN_MATCHED


def to_usd(series, cur: str, fx_series):
    """除以當日匯率（匯率 ffill 到基金日期），同 picks_candidates.build_candidates。"""
    s = series.dropna()
    if cur == "USD":
        return s
    if fx_series is None:
        return None
    fx = fx_series.reindex(s.index.union(fx_series.index)).ffill().reindex(s.index)
    return (s / fx).dropna()


def window_excess_pp(fund, bench, n: int):
    """近 n 個 SPY 交易日，基金含息報酬 − SPY 含息報酬（百分點）。資料不足回 None。"""
    import pandas as pd

    if fund is None or bench is None or len(bench) < n + 1:
        return None
    end_d, start_d = bench.index[-1], bench.index[-1 - n]
    f = fund[fund.index <= end_d]
    if f.empty or f.index[0] > start_d or (end_d - f.index[-1]).days > MAX_STALE_DAYS:
        return None
    f0 = f[f.index <= start_d].iloc[-1]
    f1 = f.iloc[-1]
    b0, b1 = bench.loc[start_d], bench.loc[end_d]
    if not all(pd.notna(v) and v > 0 for v in (f0, f1, b0, b1)):
        return None
    return round(((f1 / f0 - 1) - (b1 / b0 - 1)) * 100, 2)


def compute_strength(usd: dict) -> dict:
    """usd＝{etf_key: 美元計價含息序列}。回傳 {etf_key: {rel_spy_3m_pct, rel_spy_12m_pct}}；
    SPY 自己兩欄都是 None。"""
    bench = usd.get(BENCH)
    out = {}
    for k, s in usd.items():
        if k == BENCH:
            out[k] = {name: None for name in WINDOWS}
            continue
        out[k] = {name: window_excess_pp(s, bench, n) for name, n in WINDOWS.items()}
    return out


def fetch_strength(registry: dict) -> dict:
    """抓 registry 裡全部基金（加匯率）的含息價格，回傳 compute_strength() 的結果。
    任何基金抓不到只影響那一檔（給 None），SPY 抓不到整份回空 dict。"""
    import picks_candidates as pc  # 延後 import：picks_candidates 會 import build_etf_dash

    notes: list[str] = []
    tickers = {k: cfg.get("yf_ticker") for k, cfg in registry.items()}
    series = {}
    for tk in sorted({t for t in tickers.values() if t} | set(FX_TICKER.values())):
        try:
            series[tk] = pc.fetch_total_return(tk, notes)
        except Exception as e:  # noqa: BLE001
            print(f"[etf_dash] WARNING strength: {tk} price fetch failed: {e}", file=sys.stderr)
    cutoff = pc.last_closed_date()
    import pandas as pd
    for tk in list(series):
        series[tk] = series[tk][series[tk].index <= pd.Timestamp(cutoff)]
    for n in notes:
        print(f"[etf_dash] strength note: {n}", file=sys.stderr)
    spy_tk = tickers.get(BENCH)
    if spy_tk not in series or series[spy_tk].empty:
        return {}
    usd = {}
    for k, tk in tickers.items():
        if tk not in series:
            usd[k] = None
            continue
        cur = currency_of(tk)
        usd[k] = to_usd(series[tk], cur, series.get(FX_TICKER.get(cur)))
    usd = {k: v for k, v in usd.items() if v is not None}
    res = compute_strength(usd)
    for k in tickers:
        res.setdefault(k, {name: None for name in WINDOWS})
    as_of = str(usd[BENCH].index[-1].date())   # SPY 最後一根＝強弱截至日，總覽頂層寫成 strength_as_of
    for v in res.values():
        v["as_of"] = as_of
    return res
