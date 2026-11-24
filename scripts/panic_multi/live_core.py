"""「多類同時」上線版的每日狀態：全史重播，不存狀態。

規則照 docs/Panic_Call_Prereg.md 第 41～77 行，程式直接用同目錄的 signals.py（回測同一支），不改任何規則：
- 甲類：隱含波動率水位（S&P 500＝VIX、Nasdaq-100＝VXN、台股＝自算台指 VIX）落在最極端 5%。
- 乙類：連三天加速下跌版本一（三天都跌、跌幅一天比一天大，整數基點），且三日標準化報酬 z3 落在最差 5%。
- 丙類：美股 VIX ÷ VIX3M、台股鎖跌停家數比率，落在最極端 5%。
- 三類裡至少兩類同一天亮＝訊號。分位數每天只跟到前一天為止的全部歷史比，整數空間判斷。
- 同一波只算一次：亮過之後，要等波動率水位回到自己歷史中位數以下（到前一天為止，取偏小的中位數）才能再亮。

本檔只依賴 signals.py、numpy、pandas，網站 repo 的 CI 用同一份副本（scripts/panic_multi/，逐字複製）。
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right

import numpy as np
import pandas as pd

try:
    from . import signals as S
except ImportError:  # 網站 CI 以腳本方式執行
    import signals as S  # type: ignore

P = 500  # 最極端 5%（基點）


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


def _median_next(tr: "S.Track", i: int):
    """明天判斷重新觸發用的中位數（到今天為止的歷史，取偏小的中位數）。"""
    hist = _sorted_hist(tr, i)
    if len(hist) < S.BURN:
        return None
    return hist[(len(hist) - 1) // 2] / S.SCALE


def replay(df: pd.DataFrame) -> dict:
    """df：index 為交易日，欄位 close、vol（甲類水位）、ratio（丙類）。回傳全史重播結果與最後一天的狀態。"""
    T = S.build(df)
    n = len(df)
    dates = df.index
    lit_a = T["vol"].lit[P]
    lit_b = T["a1"] & T["z3"].lit[P]
    lit_c = T["ratio"].lit[P]
    multi = S.lit_series(T, "multi", P)
    ev = S.events(T, "multi", P, n)
    # 逐日 armed 狀態（跟 signals.events 同一個迴圈）
    armed_open = np.zeros(n, bool)  # 當天開始時是否可觸發
    armed = True
    for i in range(n):
        armed_open[i] = armed
        if armed:
            if multi[i]:
                armed = False
        elif S.rearm_ok(T, "multi", i):
            armed = True
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
    vt = T["vol"]
    med_today = vt.med[i] / S.SCALE if vt.med[i] is not None else None
    state = dict(
        date=str(dates[i].date()), close=float(close[i]),
        classes=dict(vol=a, accel=b, ratio=c_),
        n_lit=int(a["lit"]) + int(b["lit"]) + int(c_["lit"]),
        multi_lit=bool(multi[i]),
        armed_open=bool(armed_open[i]),
        event_today=bool(len(ev) and ev[-1] == i),
        armed_next=bool(armed),
        vol_median_today=med_today,
        vol_median_next=_median_next(vt, i),
        vol_le_median_today=bool(vt.val[i] is not None and vt.med[i] is not None and vt.val[i] <= vt.med[i]),
        events=[str(dates[k].date()) for k in ev],
        last_event=str(dates[ev[-1]].date()) if ev else None,
        last_event_i=int(ev[-1]) if ev else None,
        rearm_date=None,
    )
    # 上一個事件之後第一次回到中位數以下的日子（已重新可觸發時才有）
    if ev and armed:
        for k in range(ev[-1] + 1, n):
            if S.rearm_ok(T, "multi", k):
                state["rearm_date"] = str(dates[k].date())
                break
    hist = pd.DataFrame({"lit_vol": lit_a, "lit_accel": lit_b, "lit_ratio": lit_c, "multi": multi,
                         "armed_open": armed_open}, index=dates)
    hist["event"] = False
    hist.iloc[ev, hist.columns.get_loc("event")] = True
    return dict(state=state, events=ev, hist=hist, T=T)
