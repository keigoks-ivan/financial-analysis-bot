"""「多類同時」上線版的每日狀態：全史重播，不存狀態。

規則照 docs/Panic_Call_Prereg.md 第 41～77 行與修改紀錄，程式直接用同目錄的 signals.py、positions.py（回測同一支）：
- 甲類：隱含波動率水位（S&P 500＝VIX、Nasdaq-100＝VXN、台股＝自算台指 VIX）落在最極端 5%。
- 乙類：連三天加速下跌版本一（三天都跌、跌幅一天比一天大，整數基點），且三日標準化報酬 z3 落在最差 5%。
- 丙類：美股 VIX ÷ VIX3M、台股鎖跌停家數比率，落在最極端 5%。
- 三類裡至少兩類同一天亮＝訊號。分位數每天只跟到前一天為止的全部歷史比，整數空間判斷。
- 重新待命（2026-11-24 改）：部位結束就重新待命。每個版本一次只抱一筆，上一筆結束那天之後任何一天訊號亮著，
  就算新的一筆，隔天收盤進場。call 版到期結束；期貨版停損或到期，先到的那天結束；賣出賣權價差（對照）到期結束。
  同一個版本一年最多進 4 次。部位是規則上的紙上部位（進場規格見 specs_core.py），不是持有人的實際成交。
  （舊規則「波動率回到歷史中位數以下才能再亮」2026-11-24 起不用。）

本檔只依賴 signals.py、positions.py、numpy、pandas，網站 repo 的 CI 用同一份副本（scripts/panic_multi/，逐字複製）。
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right

import numpy as np
import pandas as pd

try:
    from . import positions as PS
    from . import signals as S
except ImportError:  # 網站 CI 以腳本方式執行
    import positions as PS  # type: ignore
    import signals as S  # type: ignore

P = 500  # 最極端 5%（基點）
VERSIONS = ("call", "fut", "put")
VNAME = {"call": "call 版", "fut": "期貨版", "put": "賣出賣權價差（對照）"}


def _sorted_hist(tr: "S.Track", upto: int) -> list:
    """到第 upto 天（含）為止的有效整數值，排序後回傳。"""
    return sorted(v for v in tr.val[: upto + 1] if v is not None)


def _rank(tr: "S.Track", i: int, high: bool):
    """第 i 天的值跟到前一天為止的歷史比：回傳 (c, n)。c＝歷史上比今天更極端或相等的個數。"""
    if tr.val[i] is None:
        return None, None
    hist = _sorted_hist(tr, i - 1)
    n = len(hist)
    x = tr.val[i]
    c = (n - bisect_left(hist, x)) if high else bisect_right(hist, x)
    return c, n


def _next_threshold(tr: "S.Track", i: int, high: bool):
    """明天要亮的門檻（用到今天為止的全部歷史）：high 時明天的值要「大於」回傳值，low 時要「小於」回傳值。"""
    hist = _sorted_hist(tr, i)
    n = len(hist)
    if n < S.BURN:
        return None, n
    m = (P * n) // 10_000           # 最多容許 m 個歷史值比明天更極端或相等
    if high:
        return hist[n - m - 1] / S.SCALE, n
    return hist[m] / S.SCALE, n


def open_fns(df: pd.DataFrame, specs: pd.DataFrame | None) -> dict:
    """三個版本的進場函式（給 positions.replay）。specs：以日期為索引，欄位 call_exit、call_prem、put_exit
    （specs_core.py／data/panic_multi/entry_specs.csv）；沒有那一天的規格就進不了場。"""
    dates = df.index
    n = len(df)
    close = df["close"].to_numpy(float)
    sp = (specs.reindex(dates) if specs is not None else pd.DataFrame(index=dates))
    ce = sp["call_exit"] if "call_exit" in sp else pd.Series(pd.NaT, index=dates)
    cp = sp["call_prem"].to_numpy(float) if "call_prem" in sp else np.full(n, np.nan)
    pe = sp["put_exit"] if "put_exit" in sp else pd.Series(pd.NaT, index=dates)
    last = dates[-1]

    def end_of(t):
        if t is None or pd.isna(t):
            return None
        t = pd.Timestamp(t)
        if t > last:
            return n - 1, True, t
        return int(dates.searchsorted(t, side="right") - 1), False, t

    def call(e):
        r = end_of(ce.iloc[e])
        if r is None:
            return None, "沒有符合規格的合約或波動率資料"
        x, op, t = r
        return dict(exit_i=x, open=op, end_date=str(t.date())), ""

    def fut(e):
        r = end_of(ce.iloc[e])
        if r is None or cp[e] != cp[e]:
            return None, "沒有符合規格的合約或波動率資料"
        x, op, t = r
        j, stopped = PS.futures_exit(close, e, x, float(cp[e]))
        return dict(exit_i=j, open=bool(op and not stopped), stopped=bool(stopped), end_date=str(t.date()),
                    prem=float(cp[e]), stop_level=float(close[e] - cp[e]), entry_close=float(close[e])), ""

    def put(e):
        r = end_of(pe.iloc[e])
        if r is None:
            return None, "沒有符合規格的合約或波動率資料"
        x, op, t = r
        return dict(exit_i=x, open=op, end_date=str(t.date())), ""

    return {"call": call, "fut": fut, "put": put}


def next_weekday(d: pd.Timestamp) -> pd.Timestamp:
    n = d + pd.Timedelta(days=1)
    while n.weekday() >= 5:
        n += pd.Timedelta(days=1)
    return n


def version_state(rows: list, dates, close, v: str) -> dict:
    """一個版本重播完的逐筆與最後一天的部位。"""
    n = len(dates)
    last = dates[-1]
    entries, pending, over = [], None, None
    for r in rows:
        sd = str(dates[r["sig_i"]].date())
        if r["status"] == "進場":
            x = int(r["exit_i"])
            how = "持有中" if r["open"] else ("停損" if r.get("stopped") else "到期")
            e = dict(sig_date=sd, entry_date=str(dates[r["entry_i"]].date()), end_date=r["end_date"],
                     exit_date=None if r["open"] else str(dates[x].date()), how=how)
            if v == "fut":
                e.update(stop_level=r["stop_level"], prem=r["prem"], entry_close=r["entry_close"])
            entries.append(e)
        elif r["status"] == "待進場":
            pending = dict(sig_date=sd, entry_est=str(next_weekday(last).date()))
        elif r["status"] == "超過年預算" and r["sig_i"] == n - 1:
            over = dict(sig_date=sd)
    pos = entries[-1] if entries and entries[-1]["how"] == "持有中" else None
    yr = last.year
    n_year = sum(1 for e in entries if e["entry_date"][:4] == str(yr))
    if pending and pending["entry_est"][:4] == str(yr):
        n_year += 1
    return dict(entries=entries, position=pos, pending=pending, over_budget_today=over,
                entries_this_year=n_year, flat=pos is None and pending is None,
                last_entry=entries[-1] if entries else None)


def replay(df: pd.DataFrame, specs: pd.DataFrame | None = None) -> dict:
    """df：index 為交易日，欄位 close、vol（甲類水位）、ratio（丙類）。specs：進場規格（見 open_fns）。
    回傳全史重播結果與最後一天的狀態。"""
    T = S.build(df)
    n = len(df)
    dates = df.index
    lit_a = T["vol"].lit[P]
    lit_b = T["a1"] & T["z3"].lit[P]
    lit_c = T["ratio"].lit[P]
    multi = S.lit_series(T, "multi", P)
    i = n - 1
    close = df["close"].to_numpy(float)
    r = close[1:] / close[:-1] - 1.0
    last3 = [float(x) for x in r[-3:]] if n >= 4 else []
    z3 = S.z3_and_flags(df)[0].to_numpy(float)

    def cls(tr, high, lit, val):
        c, m = _rank(tr, i, high)
        thr, nh = _next_threshold(tr, i, high)
        return dict(value=None if val != val else float(val), c=c, n=m,
                    share=None if (c is None or not m) else c / m,
                    lit=bool(lit[i]), next_threshold=thr, next_n=nh, high=high)

    a = cls(T["vol"], True, lit_a, float(df["vol"].iloc[i]) if "vol" in df else np.nan)
    b = cls(T["z3"], False, T["z3"].lit[P], z3[i])
    b["accel"] = bool(T["a1"][i])
    b["lit"] = bool(lit_b[i])
    b["z3_lit"] = bool(T["z3"].lit[P][i])
    b["last3_ret"] = last3
    b["last3_bp"] = [int(round(x * 1e4)) for x in last3]
    c_ = cls(T["ratio"], True, lit_c, float(df["ratio"].iloc[i]) if "ratio" in df else np.nan)
    fns = open_fns(df, specs)
    rows = {v: PS.replay(multi, dates, fns[v]) for v in VERSIONS}
    vs = {v: version_state(rows[v], dates, close, v) for v in VERSIONS}
    new_today = [v for v in VERSIONS if vs[v]["pending"] and vs[v]["pending"]["sig_date"] == str(dates[i].date())]
    state = dict(
        date=str(dates[i].date()), close=float(close[i]),
        classes=dict(vol=a, accel=b, ratio=c_),
        n_lit=int(a["lit"]) + int(b["lit"]) + int(c_["lit"]),
        multi_lit=bool(multi[i]),
        versions=vs,
        new_today=new_today,
        event_today=any(v in new_today for v in ("call", "fut")),   # 通知只看 call 版與期貨版
        lit_days=[str(dates[k].date()) for k in np.flatnonzero(multi)],
    )
    hist = pd.DataFrame({"lit_vol": lit_a, "lit_accel": lit_b, "lit_ratio": lit_c, "multi": multi}, index=dates)
    return dict(state=state, rows=rows, hist=hist, T=T)
