"""全站 PEG／預估本益比（明年）統一算法（2026-10-21，持有人指示「PEG 口徑統一處理」）。

  fpe_next ＝ 現價 ÷ 明年預估 EPS（eps_fy_next，Koyfin）
  PEG      ＝ fpe_next ÷ 三年 EPS 年化成長（eps_fy1_fy3_cagr_pct，Koyfin，今年到後年）

算不出來就是 None，不退回任何別的 PEG（QGM、yfinance pegRatio、forwardPE÷eps2y 自算皆不用）。
算不出來的情況：明年 EPS 缺或 ≤0、成長缺或 ≤0、股價缺或 ≤0、EPS 與股價幣別對不上又沒有可靠匯率。

幣別：股價幣別由代號尾碼判定（無尾碼＝美元掛牌，ADR 股價是美元）；EPS 幣別讀該列
eps_display_currency（Koyfin 預設美元；台股與 DD 列換成當地幣後會標 TWD／JPY）。
兩邊相同直接除；EPS 是美元、股價是當地幣時，乘上「當地幣／美元」匯率把 EPS 換成股價幣別；
其餘組合、尾碼不認得、匯率拿不到，一律 None。純函式，不碰網路；匯率由呼叫端傳入。
"""
from __future__ import annotations

# 代號尾碼 → 股價幣別。英國 .L 以便士報價（GBX），不在表內＝不算。
PRICE_CCY_BY_SUFFIX = {
    "TW": "TWD", "TWO": "TWD", "T": "JPY", "KL": "MYR", "SW": "CHF", "AX": "AUD",
    "HK": "HKD", "KS": "KRW", "KQ": "KRW", "SS": "CNY", "SZ": "CNY", "TO": "CAD",
    "PA": "EUR", "AS": "EUR", "DE": "EUR", "MI": "EUR", "MC": "EUR", "BR": "EUR",
    "HE": "EUR", "LS": "EUR",
}


def price_currency(ticker: str | None) -> str | None:
    """股價幣別。無尾碼＝USD；尾碼不認得＝None。"""
    if not ticker:
        return None
    if "." not in ticker:
        return "USD"
    return PRICE_CCY_BY_SUFFIX.get(ticker.rsplit(".", 1)[1].upper())


def _pos(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if f == f and f > 0 else None


def compute_peg_unified(ticker, price, eps_next, growth_pct, eps_ccy="USD",
                        fx_per_usd=None, eps_reliable=True) -> dict:
    """回傳 {"fpe_next": float|None, "live_peg": float|None}。

    eps_ccy：eps_next 的幣別（該列 eps_display_currency）。
    fx_per_usd：股價幣別每 1 美元的單位數；僅在 EPS 是美元、股價是當地幣時用。
    eps_reliable：EPS 幣別是否可信（Koyfin xlsx 來源為 True；yfinance 備援列幣別不明，傳 False）。
    fpe_next 只看股價與明年 EPS；PEG 另需成長 >0。
    """
    out = {"fpe_next": None, "live_peg": None}
    p, e = _pos(price), _pos(eps_next)
    if p is None or e is None or not eps_reliable:
        return out
    p_ccy = price_currency(ticker)
    e_ccy = (eps_ccy or "USD").upper()
    if p_ccy is None:
        return out
    if e_ccy != p_ccy:
        if e_ccy == "USD":
            fx = _pos(fx_per_usd)
            if fx is None:
                return out
            e = e * fx
        else:
            return out
    fpe = p / e
    out["fpe_next"] = round(fpe, 2)
    g = _pos(growth_pct)
    if g is not None:
        out["live_peg"] = round(fpe / g, 2)
    return out
