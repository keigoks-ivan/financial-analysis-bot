#!/usr/bin/env python3
"""態④觸發變體研究引擎(STUDY-trim-variants.md 實作)。

輸入:寬表收盤價(index=date, columns=tickers)。
輸出:per-variant M1-M4 聚合 + 平原九宮格 + 時代切分排名。
禁區:不算報酬、不算 CAGR/Sharpe(§7 護欄)。
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd

# ── 研究參數(自帶,不碰生產 config)─────────────────────────────────────────
MA_D = 60
MA_W = 52
FALSE_ALARM_DAYS = 10          # M2:確認後 10 交易日內收回 60MA 上
V1_BAND = 0.97
V1_DAYS = 3
V2_STAGE2_BAND = 0.95
V3_EXT = 0.15
PLATEAU_V1 = [(b, d) for b in (0.96, 0.97, 0.98) for d in (2, 3, 4)]
PLATEAU_V3 = [0.12, 0.15, 0.18]


def per_ticker_frames(close: pd.Series):
    """回傳對齊到日線的 ma60d / frozen ma52w / weekly(close,ma52w) 。"""
    close = close.dropna()
    if len(close) < 300:
        return None
    ma60 = close.rolling(MA_D).mean()
    wclose = close.resample("W-FRI").last().dropna()
    wma52 = wclose.rolling(MA_W).mean()
    # 凍結語義:日 d 可見的週線值 = 最近一個 bucket 端點 ≤ d 的週(週五當天即含當週)
    frozen52 = wma52.reindex(close.index, method="ffill")
    return dict(close=close, ma60=ma60, frozen52=frozen52,
                wclose=wclose, wma52=wma52)


def detect_episodes(fr: dict) -> list[dict]:
    """碰觸事件切分 + 結局標記。"""
    c, ma60, f52 = fr["close"], fr["ma60"], fr["frozen52"]
    valid = (~ma60.isna()) & (~f52.isna())
    below = (c < ma60) & valid
    idx = c.index
    eps, i, n = [], 0, len(idx)
    barr = below.values
    while i < n:
        if barr[i] and (i == 0 or not barr[i - 1]):
            touch_i = i
            j = i
            while j < n and barr[j]:
                j += 1
            # j = 第一個收回 60MA 之上的 bar(或資料尾)
            span = idx[touch_i:j]
            # 升級檢查:span 內任一週末(W-FRI bucket 端點落在 span)wclose < wma52
            esc_date = None
            w_in = fr["wclose"].loc[(fr["wclose"].index >= span[0])
                                    & (fr["wclose"].index <= (span[-1] if j >= n else idx[j - 1]))]
            for wd, wc in w_in.items():
                wm = fr["wma52"].get(wd)
                if wm is not None and not np.isnan(wm) and wc < wm:
                    esc_date = wd
                    break
            eps.append(dict(
                touch_i=touch_i, end_i=j,            # end_i = 收回日(exclusive of below run)
                touch_date=idx[touch_i], touch_close=float(c.iloc[touch_i]),
                escalated=esc_date is not None, esc_date=esc_date,
                ext_at_touch=float(c.iloc[touch_i] / f52.iloc[touch_i] - 1.0),
            ))
            i = j
        else:
            i += 1
    return eps


def confirm_day(fr, ep, variant: str, p1=None, p2=None):
    """回傳 (confirm_i or None, weight)。weight: V2 階梯回傳 [(i,0.25),(i2,0.25)] 清單。"""
    c, ma60 = fr["close"], fr["ma60"]
    t, e = ep["touch_i"], ep["end_i"]
    # episode 有效終點:升級日(若有)截斷
    if ep["escalated"]:
        esc_pos = c.index.searchsorted(ep["esc_date"], side="right")
        e = min(e, esc_pos)
    rng = range(t, e)
    if variant == "V0":
        return [(t, 0.50)]
    if variant == "V1":
        band, days = (p1 or V1_BAND), (p2 or V1_DAYS)
        consec = 0
        for i in rng:
            consec += 1                      # episode 內天天在線下
            if c.iloc[i] < band * ma60.iloc[i] or consec >= days:
                return [(i, 0.50)]
        return []
    if variant == "V2":
        out = [(t, 0.25)]
        for i in rng:
            if c.iloc[i] < V2_STAGE2_BAND * ma60.iloc[i]:
                out.append((i, 0.25))
                break
        return out
    if variant == "V3":
        ext = p1 if p1 is not None else V3_EXT
        return [(t, 0.50)] if ep["ext_at_touch"] >= ext else []
    if variant == "V4":
        for i in rng:
            d = c.index[i]
            if d in fr["wclose"].index:      # 該日即週末 bucket 端點
                return [(i, 0.50)]
        return []
    raise ValueError(variant)


def measure(fr, eps, variant, p1=None, p2=None) -> dict:
    c, ma60 = fr["close"], fr["ma60"]
    years = max((c.index[-1] - c.index[0]).days / 365.25, 1e-9)
    n_confirm = 0
    false_alarm = 0
    churn = 0.0
    m3 = []
    for ep in eps:
        confs = confirm_day(fr, ep, variant, p1, p2)
        if not confs:
            if ep["escalated"]:
                # 未確認即升級:代價量到升級日收盤(真實成本:沒減碼直到全出)
                esc_close = float(fr["wclose"].loc[ep["esc_date"]])
                m3.append((ep["touch_close"] - esc_close) / ep["touch_close"])
            continue
        n_confirm += 1
        first_i, _ = confs[0]
        if ep["escalated"]:
            last_i = confs[-1][0]
            m3.append((ep["touch_close"] - float(c.iloc[last_i])) / ep["touch_close"])
        else:
            # 假警報:首確認後 10 交易日內收回 60MA 上(episode 未升級)
            back = ep["end_i"] - first_i        # 收回所需 bar 數
            if back <= FALSE_ALARM_DAYS:
                false_alarm += 1
            churn += sum(w for _, w in confs)   # 收回的 episode = 來回一輪
    return dict(m1=n_confirm / years, m2_fa=false_alarm, m2_n=n_confirm,
                m3=m3, m4=churn / years, years=years)


def aggregate(per_ticker: list[dict]) -> dict:
    m1 = [r["m1"] for r in per_ticker]
    fa = sum(r["m2_fa"] for r in per_ticker)
    nc = sum(r["m2_n"] for r in per_ticker)
    m3 = [x for r in per_ticker for x in r["m3"]]
    m4 = [r["m4"] for r in per_ticker]
    q = lambda a, p: float(np.percentile(a, p)) if a else None
    return dict(
        m1_med=q(m1, 50), m1_p75=q(m1, 75),
        m2=fa / nc if nc else None, m2_confirmed=nc,
        m3_med=q(m3, 50), m3_p90=q(m3, 90), m3_n=len(m3),
        m4_med=q(m4, 50),
    )


def run_study(closes: pd.DataFrame, eras: dict | None = None) -> dict:
    variants = ["V0", "V1", "V2", "V3", "V4"]
    results = {v: [] for v in variants}
    plateau_v1 = {f"{b}/{d}": [] for b, d in PLATEAU_V1}
    plateau_v3 = {str(e): [] for e in PLATEAU_V3}
    era_results = {k: {v: [] for v in variants} for k in (eras or {})}
    n_used = 0
    for t in closes.columns:
        fr = per_ticker_frames(closes[t])
        if fr is None:
            continue
        n_used += 1
        eps = detect_episodes(fr)
        for v in variants:
            results[v].append(measure(fr, eps, v))
        for b, d in PLATEAU_V1:
            plateau_v1[f"{b}/{d}"].append(measure(fr, eps, "V1", b, d))
        for e in PLATEAU_V3:
            plateau_v3[str(e)].append(measure(fr, eps, "V3", e))
        for name, (d0, d1) in (eras or {}).items():
            sub_eps = [ep for ep in eps if d0 <= ep["touch_date"].strftime("%Y-%m-%d") < d1]
            for v in variants:
                era_results[name][v].append(measure(fr, sub_eps, v))
    out = {
        "n_tickers_used": n_used,
        "variants": {v: aggregate(results[v]) for v in variants},
        "plateau_v1": {k: aggregate(r) for k, r in plateau_v1.items()},
        "plateau_v3": {k: aggregate(r) for k, r in plateau_v3.items()},
        "eras": {k: {v: aggregate(r) for v, r in vr.items()}
                 for k, vr in era_results.items()},
    }
    return out


if __name__ == "__main__":
    import sys
    px = pd.read_parquet(sys.argv[1]) if sys.argv[1].endswith(".parquet") \
        else pd.read_csv(sys.argv[1], index_col=0, parse_dates=True)
    eras = {"2020crash": ("2020-01-01", "2020-07-01"),
            "2022bear": ("2022-01-01", "2023-01-01"),
            "2023-24trend": ("2023-01-01", "2025-01-01"),
            "front_half": ("1900-01-01", "2019-01-01"),
            "back_half": ("2019-01-01", "2099-01-01")}
    res = run_study(px, eras)
    print(json.dumps(res, indent=2, ensure_ascii=False))
