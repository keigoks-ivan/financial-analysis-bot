"""台股資料：官方面板 → 還原開收矩陣、成交金額、月營收、NTM EPS、加權報酬指數、隔夜拆款利率。

還原價：日因子 mark／ref 連乘（src/revmom_backtest 的做法），3454 在 2011-07-27 的 ref 依
src/revmom_backtest/data.py 的 REF_FIXES 更正；|mark／ref − 1| > 30% 的日子因子記 1
（docs/Behavioral_Pattern_Prereg.md 沿用 src/ath_patterns/data_load.py::load_tw 的台股做法）。
還原開盤＝當日還原收盤 × 開盤 ÷ mark（同日開到收之間沒有公司行動）。沒有成交（開盤缺）的日子還原開盤為 NaN。
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from .common import ROOT

PANEL = ROOT / "data" / "revmom"
EPS_CSV = ROOT / "data" / "koyfin_estimates_tw" / "eps_ntm.csv"
CASH_CSV = ROOT / "data" / "tw_cash_rate" / "call_rate_on_d.csv"
# 網站 repo（financial-analysis-bot）沒有上面那個檔，改讀總經資料庫的同一條序列（同欄位 date,value）。
CASH_FALLBACK = ROOT / "data" / "macro_db" / "series" / "tw.call_rate_on_d.csv"
ANOMALY = 0.30
REF_FIXES = (("2011-07-27", "3454", -2.3, 79.07),)     # 與 src/revmom_backtest/data.py 相同（測試核對）


def code_ok(c: str) -> bool:
    """排除 00 開頭（ETF）與 91 開頭（存託憑證）。"""
    return not (c.startswith("00") or c.startswith("91"))


@dataclass
class Mkt:
    name: str
    dates: pd.DatetimeIndex
    codes: list
    C: np.ndarray            # (T, N) 還原收盤，存續期間內缺列向前補，存續期外 NaN
    O: np.ndarray            # (T, N) 還原開盤，沒有成交或沒有列為 NaN
    row: np.ndarray          # (T, N) bool，當日有報價列（掛牌）
    first: np.ndarray        # (N,) 第一列位置
    last: np.ndarray         # (N,) 最後一列位置
    liq: np.ndarray          # (T, N) bool，近 20 日平均成交金額 ≥ 門檻（台股）；美股全 True
    rate: np.ndarray         # (T,) 現金年化利率（%），已向前補
    bench: pd.Series         # 對照指數（加權報酬指數／SPY／IJR），index＝dates
    cost_buy: float
    cost_sell: float
    info: dict = field(default_factory=dict)


def _apply_ref_fixes(p: pd.DataFrame) -> int:
    n = 0
    for d, c, bad, good in REF_FIXES:
        m = (p["date"] == pd.Timestamp(d)) & (p["code"] == c) & ((p["ref"] - bad).abs() < 1e-9)
        n += int(m.sum())
        p.loc[m, "ref"] = good
    return n


def cash_csv() -> Path:
    """隔夜拆款利率檔：環境變數 TB_CASH_CSV 指定者優先；否則 CASH_CSV，不存在再用 CASH_FALLBACK；都沒有就報錯。"""
    env = os.environ.get("TB_CASH_CSV")
    if env:
        return Path(env)
    for p in (CASH_CSV, CASH_FALLBACK):
        if p.exists():
            return p
    raise FileNotFoundError(f"找不到隔夜拆款利率檔：{CASH_CSV}、{CASH_FALLBACK}（可用 TB_CASH_CSV 指定）")


def load_prices(start="2007-01-01", anomaly=True):
    """anomaly=False：不套 30% 異常日規則（只供疑點節的敏感度比較）。"""
    from .common import LIQ_MIN_TWD, LIQ_WIN, TW_COST_BUY, TW_COST_SELL
    p = pd.read_parquet(PANEL / "prices.parquet", columns=["date", "code", "open", "value", "mark", "ref"])
    p = p[(p["date"] >= pd.Timestamp(start)) & p["code"].map(code_ok)].copy()
    nfix = _apply_ref_fixes(p)
    p = p.sort_values(["code", "date"])
    r = p["mark"] / p["ref"]
    bad = ((r - 1).abs() > ANOMALY) & r.notna() & anomaly
    nbad = int(bad.sum())
    r = r.where(r.notna() & ~bad, 1.0)
    p["adj"] = r.groupby(p["code"]).cumprod()
    dates = pd.DatetimeIndex(sorted(p["date"].unique()))
    codes = sorted(p["code"].unique())
    T, N = len(dates), len(codes)
    di = pd.Series(np.arange(T), index=dates)
    ci = pd.Series(np.arange(N), index=codes)
    ti = di.loc[p["date"]].values
    cj = ci.loc[p["code"]].values
    C = np.full((T, N), np.nan)
    C[ti, cj] = p["adj"].values
    row = np.zeros((T, N), dtype=bool)
    row[ti, cj] = True
    mark = p["mark"].values
    opn = p["open"].values
    O = np.full((T, N), np.nan)
    okO = np.isfinite(opn) & np.isfinite(mark) & (mark > 0) & (opn > 0)
    O[ti[okO], cj[okO]] = p["adj"].values[okO] * opn[okO] / mark[okO]
    V = np.zeros((T, N))
    V[ti, cj] = p["value"].fillna(0.0).values
    first = row.argmax(0)
    last = T - 1 - row[::-1].argmax(0)
    # 存續期間內缺列向前補
    C = pd.DataFrame(C).ffill().values
    tt = np.arange(T)[:, None]
    C[(tt < first[None, :]) | (tt > last[None, :])] = np.nan
    # 流動性：近 20 個交易日（含決策日）成交金額合計 ≥ 20 × 1,000 萬（整數元，浮點表示精確）
    cs = np.cumsum(V, axis=0)
    s20 = cs.copy()
    s20[LIQ_WIN:] = cs[LIQ_WIN:] - cs[:-LIQ_WIN]
    s20[:LIQ_WIN - 1] = 0.0
    liq = np.rint(s20).astype(np.int64) >= LIQ_WIN * LIQ_MIN_TWD
    tr = pd.read_parquet(PANEL / "index_tr.parquet").set_index("date")["taiex_tr"]
    bench = tr.reindex(dates).ffill()
    cash = pd.read_csv(cash_csv(), parse_dates=["date"]).set_index("date")["value"]
    rate = cash.reindex(cash.index.union(dates)).ffill().reindex(dates).values
    info = dict(ref_fixed_rows=nfix, anomaly_days=nbad, n_codes=N, first_date=str(dates[0].date()),
                last_date=str(dates[-1].date()), cash_last=str(cash.index.max().date()),
                delisted=int((last < T - 1).sum()))
    return Mkt("tw", dates, codes, C, O, row, first, last, liq, rate, bench, TW_COST_BUY, TW_COST_SELL, info)


def load_revenue(codes) -> pd.DataFrame:
    """回傳寬表（連續的 PeriodIndex 月 × 代號），單位千元，缺值 NaN。"""
    r = pd.read_parquet(PANEL / "revenue.parquet")
    w = r.pivot(index="month", columns="code", values="revenue")
    w.index = pd.PeriodIndex(w.index, freq="M")
    full = pd.period_range(w.index.min(), w.index.max(), freq="M")
    return w.reindex(index=full, columns=list(codes))


def load_eps(codes, dates) -> tuple:
    """NTM EPS 寬表（已向前補，查某日即得「當天含以前最近一筆」），與原檔有值的代號集合。
    EPS 檔不存在（網站 repo 的雲端副本沒有 Koyfin 資料）時回傳空寬表與空集合：L3 全部不成立，只用 L1、L2 的組別不受影響。"""
    if not EPS_CSV.exists():
        return pd.DataFrame(index=pd.DatetimeIndex([], name="date"), dtype=float), set()
    e = pd.read_csv(EPS_CSV, index_col=0, parse_dates=True)
    e.columns = [str(c) for c in e.columns]
    have = set(e.columns)
    e = e.reindex(columns=[c for c in codes if c in have])
    return e.sort_index().ffill(), have
