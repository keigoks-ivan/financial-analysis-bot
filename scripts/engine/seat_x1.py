"""美股看板 v5.7（2026-10-21 持有人破例決定）：大盤空頭才看紅燈（純函式，不連網、不讀寫檔，除 load_close_series）。

規則（與台股 v5.4 的 X1 同一種判法，指數換成 SPY 還原收盤；台股實作在 scripts/build_seats_tw.py，本檔不動它）：
- 決策日 SPY 還原收盤 < 其 200 日簡單均線＝大盤空頭；其餘（含恰好相等、均線不足 200 列）＝大盤多頭。
- 大盤多頭：在席者只在「資格不成立／出池」或「收盤跌破自己的 200 日線」時下席；只因距歷史新高 < −10% 轉紅的，續抱。
  續抱者倉位沿用最近一次非紅燈的倉位（回測規則，狀態檔記錄）。
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
X1_DEFAULT_SIZE = 1.0


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
    """決策日的大盤狀態。mode 'x1'＝大盤多頭（紅燈不下席）；'e1'＝現行賣法（空頭，或資料缺／太舊而退回）。"""
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
    res["mode"] = "e1" if bear else "x1"
    return res


def dist_only_red(r: dict) -> bool:
    """紅燈只因距新高 < −10%（沒跌破自己的 200 日線）。r['below_200'] 由 build_arena.row_dict() 給。"""
    return (r.get("lamp") or {}).get("code") == "red" and not r.get("below_200")


def _as_lit(r: dict) -> dict:
    """選席用的副本：把大盤多頭時續抱的紅燈在席者當作亮燈。不改原列。"""
    return dict(r, lamp=dict(r["lamp"], code="yellow"))


def select_roster(pool_ranked: list, prev_core, market, selector, **kw) -> dict:
    """大盤多頭（market['mode']=='x1'）時，池內且只因距新高轉紅的現任當作亮燈交給 selector
    （build_arena.select_lit_roster_v52）；其餘情況原樣呼叫 selector（與 v5.6 逐位元相同）。
    現任仍依池序競爭前 5，被更高名次擠出是上線原有行為，照舊。"""
    pool = pool_ranked
    if market and market.get("mode") == "x1":
        inc = set(prev_core or [])
        pool = [_as_lit(r) if r["ticker"] in inc and dist_only_red(r) else r for r in pool_ranked]
    return selector(pool, prev_core, **kw)


def held_tickers(core_rows: list, pool_set: set, market, lit_codes) -> set:
    """顯示用：目前不亮燈、但大盤多頭下只因距新高轉紅而續抱的在席者。"""
    if not (market and market.get("mode") == "x1"):
        return set()
    return {r["ticker"] for r in core_rows
            if (r.get("lamp") or {}).get("code") not in lit_codes
            and r["ticker"] in pool_set and dist_only_red(r)}


def apply_hold(core_rows: list, held: set, state: dict, log=print) -> None:
    """續抱者：燈號維持紅，倉位改用最近一次非紅燈的倉位（回測規則）。state＝{ticker: {'size': ...}}；
    缺值用 X1_DEFAULT_SIZE 並印一行。直接改 core_rows 內的 lamp／action。"""
    for r in core_rows:
        if r["ticker"] not in held:
            continue
        size = (state.get(r["ticker"]) or {}).get("size")
        if size is None:
            size = X1_DEFAULT_SIZE
            log(f"  ! arena: {r['ticker']} 狀態檔沒有最近非紅燈倉位，續抱倉位用 {X1_DEFAULT_SIZE}")
        lamp = dict(r["lamp"])
        why = lamp.get("why") or ""
        lamp.update(label="🔴 續抱", size=size, trigger=None,
                    why=f"大盤多頭，只在跌破自己的 200 日線才賣；倉位沿用最近一次非紅燈的倉位 {size}｜{why}")
        r["lamp"] = lamp
        r["action"] = ("正常倉" if size >= 1.0 else "半倉") + "・續抱"
        r["x1_hold"] = True


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


def market_note_html(market) -> str:
    """頁面用：賣法一句話＋目前大盤狀態一行＋v5.7 註記（HTML 片段，已跳脫過的固定文字＋數字）。"""
    rule = ("<div class=\"bw-note-line\"><b>賣法</b>：大盤多頭（SPY 還原收盤在 200 日線之上）時，在席者離歷史新高再遠也續抱，"
            "只有資格不成立（出池）或跌破自己的 200 日線才賣；大盤空頭時，時機燈轉紅就賣（距歷史新高超過 10% 或跌破 200 日線）。"
            "續抱者倉位沿用最近一次非紅燈的倉位。</div>")
    st = (market or {}).get("status")
    d = (market or {}).get("data_date") or "—"
    if not market or st in ("stale", "missing"):
        line = (f"大盤資料未更新，本週照空頭處理，用「時機燈轉紅就賣」（最近一筆資料日期 {d}）。")
    else:
        nums = f"SPY 還原收盤 {market['close']:,.2f}"
        nums += (f"，200 日線 {market['ma200']:,.2f}" if market.get("ma200") is not None
                 else "，200 日線資料不足，算多頭")
        word, way = (("多頭", "本週用「跌破自己的 200 日線才賣」") if st == "bull"
                     else ("空頭", "本週用「時機燈轉紅就賣」"))
        line = f"大盤狀態（{d} 收盤）：{nums}，<b>{word}</b>。{way}。"
    note = ("<div class=\"bw-note-line\"><b>v5.7 變更（2026-10-21）</b>：賣法由「時機燈轉紅就賣」改成「大盤空頭才看紅燈」。"
            "這是持有人的破例決定，不是回測登記通過。依據是美股大型股在配對格全期 100%、前段 81%、後段 91% 變好，"
            "但大型股在登記裡只當參考，判定母體（美股中小型）偏好紅燈就賣。研究依據見 "
            "<a href=\"/cockpit/#seats-grid\">席位全格子測試</a>。入場、排序、倉位係數不變。</div>")
    return rule + f"<div class=\"bw-note-line\">{line}</div>" + note
