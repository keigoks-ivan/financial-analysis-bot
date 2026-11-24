"""「多類同時」紙上部位的進場規格：某一天收盤進場的話，三個月價內 5% call（call 版與期貨版共用）與一個月賣出賣權價差。

跟回測同一套規則（src/panic_call/options.py 的 tw_open／Formula.trade），寫成只依賴 numpy、pandas 的小函式，
給網站 CI 每天補新的一天用（scripts/panic_multi/specs_core.py 是逐字副本）。歷史的部分由 v7
`python3 -m src.panic_call.entry_specs` 用回測程式本身算好，存成 data/panic_multi/entry_specs.csv，並逐日核對跟本檔算的一樣。

欄位（每個市場每個交易日一列）：
- call_exit：call 版部位結束日（台股＝該合約最後結算日；美股＝進場日加 91 天，遇休市取之前最後一個交易日）。
- call_prem：call 的進場價（指數點，含成本），期貨版的停損額度。
- put_exit：賣出賣權價差（一個月）的到期日。
其餘欄位只供頁面與通知顯示。
"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import pandas as pd

TICKS = [(10.0, 0.1), (50.0, 0.5), (500.0, 1.0), (1000.0, 5.0)]
SIGMA_FLOOR = 0.05
US_COST = 0.03
US_SLOPE = 0.5
CALL_DAYS = 91
PUT_DAYS = 30
COLS = ["market", "date", "call_exit", "call_prem", "call_strike", "call_expiry", "put_exit", "put_k_sell", "put_k_buy",
        "put_expiry", "put_credit"]


def tick(p: float) -> float:
    for lim, t in TICKS:
        if p < lim:
            return t
    return 10.0


def tw_cost(p: float) -> float:
    return max(p * 0.02, tick(p)) + 1.0


def third_wednesday(expiry: str) -> pd.Timestamp:
    y, m = int(expiry[:4]), int(expiry[4:])
    d = dt.date(y, m, 1)
    return pd.Timestamp(y, m, 1 + (2 - d.weekday()) % 7 + 14)


def pick_expiry(cands: dict, spec: str):
    """cands：{到期代碼: 距進場日曆天數}。A：>=21 天裡最近；B：60～100 天裡最接近 91（平手取較近）。"""
    if spec == "A":
        c = [(d, e) for e, d in cands.items() if d >= 21]
        return min(c)[1] if c else None
    c = [(abs(d - 91), d, e) for e, d in cands.items() if 60 <= d <= 100]
    return min(c)[2] if c else None


def pick_strike_low(strikes, settles, target):
    """最接近 target 的履約價（一樣近取較低者）；沒有結算價（或 ≤0）就換次近的。"""
    strikes = np.asarray(strikes, float)
    settles = np.asarray(settles, float)
    ok = np.isfinite(settles) & (settles > 0)
    order = sorted(range(len(strikes)), key=lambda j: (abs(strikes[j] - target), strikes[j]))
    for j in order:
        if ok[j]:
            return j
    return None


def tw_fill(settle: float, bid: float, ask: float, side: str) -> float:
    """買進用最後最佳賣價 +1 點、賣出用最後最佳買價 −1 點；沒有有效報價時用結算價 ± 成本模型。"""
    if side == "buy" and ask == ask and ask > 0 and (bid != bid or ask >= bid):
        return float(ask) + 1.0
    if side == "sell" and bid == bid and bid > 0 and (ask != ask or ask >= bid):
        return max(float(bid) - 1.0, 0.0)
    c = tw_cost(settle)
    return settle + c if side == "buy" else max(settle - c, 0.0)


def tw_row(day: pd.DataFrame, d: pd.Timestamp, S: float, exp_date: dict, exit_date: dict | None = None) -> dict:
    """台股某一天：day＝當天台指選擇權（欄位 expiry 6 碼、strike、cp C／P、settle、bid、ask），S＝加權指數收盤，
    exp_date＝{到期代碼: 到期日}（選合約算天數用），exit_date＝{到期代碼: 最後結算日}（部位結束日，預設同 exp_date；
    2008 年以前最後結算日在到期日隔天，回測才需要分開）。回傳一列（算不出來的欄位不放）。"""
    exit_date = exit_date or exp_date
    out = dict(market="TW", date=d)

    def pick(cp, spec, target):
        g = day[day.cp == cp]
        if g.empty:
            return None
        cands = {e: (exp_date[e] - d).days for e in g.expiry.unique()}
        e = pick_expiry(cands, spec)
        if e is None:
            return None
        ge = g[g.expiry == e].reset_index(drop=True)
        j = pick_strike_low(ge.strike.to_numpy(float), ge.settle.to_numpy(float), target)
        if j is None:
            return None
        r = ge.iloc[j]
        return dict(expiry=e, strike=float(r.strike), settle=float(r.settle), bid=float(r.bid), ask=float(r.ask))

    c = pick("C", "B", 0.95 * S)
    if c is not None:
        px = tw_fill(c["settle"], c["bid"], c["ask"], "buy")
        if px > 0:
            out.update(call_exit=exit_date[c["expiry"]], call_prem=px, call_strike=c["strike"], call_expiry=c["expiry"])
    s, b = pick("P", "A", 0.95 * S), pick("P", "A", 0.90 * S)
    if s is not None and b is not None and s["expiry"] == b["expiry"] and s["strike"] > b["strike"]:
        D = -tw_fill(s["settle"], s["bid"], s["ask"], "sell") + tw_fill(b["settle"], b["bid"], b["ask"], "buy")
        if s["strike"] - b["strike"] + D > 0:
            out.update(put_exit=exit_date[s["expiry"]], put_k_sell=s["strike"], put_k_buy=b["strike"],
                       put_expiry=s["expiry"], put_credit=-D)
    return out


def _ncdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_put(S, K, T, r, q, sigma):
    if T <= 0:
        return max(0.0, K - S)
    st = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / st
    d2 = d1 - st
    return K * math.exp(-r * T) * _ncdf(-d2) - S * math.exp(-q * T) * _ncdf(-d1)


def f_value(kind, S, K, T, atm, r, q, slope_pt=US_SLOPE):
    """kind 0＝call、1＝put；價內每 1% 加 slope_pt 個波動率點（有號），下限 5%。"""
    if T <= 0:
        return max(S - K, 0.0) if kind == 0 else max(K - S, 0.0)
    sg = max(SIGMA_FLOOR, atm + slope_pt * 100.0 * (S - K) / S / 100.0)
    p = bs_put(S, K, T, r, q, sg)
    return p if kind == 1 else p + S * math.exp(-q * T) - K * math.exp(-r * T)


def us_row(market: str, d: pd.Timestamp, S: float, vol1: float, vol3: float, r: float, q: float) -> dict:
    """美股某一天（公式估價，同回測 Formula）：vol1＝VIX 或 VXN（%），vol3＝VIX3M（%，Nasdaq-100 傳 NaN），r、q 為小數。"""
    out = dict(market=market, date=d)
    atm3 = vol3 / 100.0 if vol3 == vol3 else vol1 / 100.0
    if atm3 == atm3:
        f = f_value(0, S, 0.95 * S, CALL_DAYS / 365.0, atm3, r, q)
        D = f * (1 + US_COST)
        if D > 0:
            out.update(call_exit=d + pd.Timedelta(days=CALL_DAYS), call_prem=D, call_strike=0.95 * S,
                       call_expiry=str((d + pd.Timedelta(days=CALL_DAYS)).date()))
    atm1 = vol1 / 100.0
    if atm1 == atm1:
        T = PUT_DAYS / 365.0
        f1, f2 = f_value(1, S, 0.95 * S, T, atm1, r, q), f_value(1, S, 0.90 * S, T, atm1, r, q)
        D = -f1 * (1 - US_COST) + f2 * (1 + US_COST)
        if 0.05 * S + D > 0:
            out.update(put_exit=d + pd.Timedelta(days=PUT_DAYS), put_k_sell=0.95 * S, put_k_buy=0.90 * S,
                       put_expiry=str((d + pd.Timedelta(days=PUT_DAYS)).date()), put_credit=-D)
    return out


def read_table(path) -> pd.DataFrame:
    t = pd.read_csv(path, dtype={"call_expiry": str, "put_expiry": str}, parse_dates=["date", "call_exit", "put_exit"],
                    float_precision="round_trip")
    return t


def market_specs(table: pd.DataFrame, market: str) -> pd.DataFrame:
    return table[table.market == market].set_index("date").sort_index()
