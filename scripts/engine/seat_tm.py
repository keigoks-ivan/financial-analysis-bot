"""美股看板 v5.7（2026-10-21 持有人破例決定）：大盤空頭才看紅燈（回測定義：紅燈 ∧ 大盤空頭，TM）。
純函式，不連網、不讀寫檔，除 load_close_series。

規則（大盤判法與台股 v5.4 相同，指數換成 SPY 還原收盤；台股實作在 scripts/build_seats_tw.py，本檔不動它。
注意這不是台股的「看大盤切換出場」：這裡多頭週所有紅燈都續抱，不另看跌破自己的 200 日線）：
- 決策日 SPY 還原收盤 < 其 200 日簡單均線＝大盤空頭；其餘（含恰好相等、均線不足 200 列）＝大盤多頭。
- 大盤多頭：在席者只在「資格不成立／出池」時下席（資格含站上 52 週線，grp.py p_pass）；紅燈（不論距新高 < −10%
  或跌破 200 日線）一律續抱，倉位沿用最近一次非紅燈的倉位（回測規則，狀態檔記錄）。
- 大盤空頭：照現行（時機燈轉紅或資格不成立就下席）。
- 大盤資料缺或比決策日早超過 7 個日曆天：該週退回現行賣法。
入場、排序、倉位係數、五席都不變。十倍股頁與台股不用本檔。
"""
from __future__ import annotations

import json
import math
from datetime import date

MKT_MA = 200
MKT_STALE_DAYS = 7
TM_DEFAULT_SIZE = 1.0


def load_close_series(path, symbol: str = "SPY") -> list:
    """data/flowmap_prices.json（flowmap-daily 每日更新，yfinance 還原收盤）→ [(date, close)] 升冪。
    檔案缺或壞掉回傳 []（呼叫端視為資料缺，退回現行賣法）。"""
    try:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)["series"][symbol]
    except (OSError, ValueError, KeyError, TypeError):
        return []
    out = []
    for item in rows:
        try:
            out.append((date.fromisoformat(str(item[0])[:10]), float(item[1])))
        except (ValueError, TypeError, IndexError):
            continue
    out.sort(key=lambda x: x[0])
    return out


def market_state(series, decision_date, ma_days: int = MKT_MA, stale_days: int = MKT_STALE_DAYS) -> dict:
    """決策日的大盤狀態。mode 'tm'＝大盤多頭（紅燈不下席，所有紅燈）；'e1'＝現行賣法（空頭，或資料缺／太舊而退回）。"""
    dd = decision_date if isinstance(decision_date, date) else date.fromisoformat(str(decision_date)[:10])
    res = {"mode": "e1", "status": "missing", "decision_date": dd.isoformat(),
           "data_date": None, "close": None, "ma200": None}
    i = max((k for k, (d, _) in enumerate(series) if d <= dd), default=None)
    if i is None:
        return res
    d, close = series[i]
    res.update(data_date=d.isoformat(), close=close)
    if (dd - d).days > stale_days:
        res["status"] = "stale"
        return res
    if i + 1 >= ma_days:
        ma = math.fsum(v for _, v in series[i + 1 - ma_days:i + 1]) / ma_days
        res["ma200"] = ma
        bear = close < ma
    else:
        bear = False
    res["status"] = "bear" if bear else "bull"
    res["mode"] = "e1" if bear else "tm"
    return res


def is_red(r: dict) -> bool:
    return (r.get("lamp") or {}).get("code") == "red"


def _as_lit(r: dict) -> dict:
    """選席用的副本：把大盤多頭時續抱的紅燈在席者當作亮燈。不改原列。"""
    return dict(r, lamp=dict(r["lamp"], code="yellow"))


def select_roster(pool_ranked: list, prev_core, market, selector, **kw) -> dict:
    """大盤多頭（market['mode']=='tm'）時，池內的紅燈現任當作亮燈交給 selector
    （build_arena.select_hold_roster）；其餘情況原樣呼叫 selector（與 v5.6 逐位元相同）。
    v5.11 起現任抱著，不再被更高名次擠出。"""
    pool = pool_ranked
    if market and market.get("mode") == "tm":
        inc = set(prev_core or [])
        pool = [_as_lit(r) if r["ticker"] in inc and is_red(r) else r for r in pool_ranked]
    return selector(pool, prev_core, **kw)


def held_tickers(core_rows: list, pool_set: set, market, lit_codes) -> set:
    """顯示用：目前不亮燈、但大盤多頭下只因距新高轉紅而續抱的在席者。"""
    if not (market and market.get("mode") == "tm"):
        return set()
    return {r["ticker"] for r in core_rows
            if (r.get("lamp") or {}).get("code") not in lit_codes
            and r["ticker"] in pool_set and is_red(r)}


def apply_hold(core_rows: list, held: set, state: dict, log=print) -> None:
    """續抱者：燈號維持紅，倉位改用最近一次非紅燈的倉位（回測規則）。state＝{ticker: {'size': ...}}；
    缺值用 TM_DEFAULT_SIZE 並印一行。直接改 core_rows 內的 lamp／action。"""
    for r in core_rows:
        if r["ticker"] not in held:
            continue
        size = (state.get(r["ticker"]) or {}).get("size")
        if size is None:
            size = TM_DEFAULT_SIZE
            log(f"  ! arena: {r['ticker']} 狀態檔沒有最近非紅燈倉位，續抱倉位用 {TM_DEFAULT_SIZE}")
        lamp = dict(r["lamp"])
        why = lamp.get("why") or ""
        lamp.update(label="🔴 續抱", size=size, trigger=None,
                    why=f"大盤多頭，紅燈不賣，只在資格不成立（出池）才賣；倉位沿用最近一次非紅燈的倉位 {size}｜{why}")
        r["lamp"] = lamp
        r["action"] = ("正常倉" if size >= 1.0 else "半倉") + "・續抱"
        r["tm_hold"] = True


def update_state(state: dict, core_rows: list, as_of: str, lit_codes) -> dict:
    """每個在席者最近一次非紅燈的倉位。亮燈且距新高有資料才更新；其餘保留舊值；離席者丟掉。"""
    new = {}
    for r in core_rows:
        t = r["ticker"]
        lamp = r.get("lamp") or {}
        if lamp.get("code") in lit_codes and r.get("dist_ath_pct") is not None:
            new[t] = {"size": lamp.get("size"), "code": lamp.get("code"), "date": as_of}
        elif t in state:
            new[t] = state[t]
    return new
