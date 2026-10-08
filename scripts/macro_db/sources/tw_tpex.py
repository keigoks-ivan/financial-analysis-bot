"""證券櫃檯買賣中心（TPEx）www JSON。

kind:
- inx：indexInfo/inx，date 所在整月；tables[0].data=[日期(西元2026/10/07), 開, 高, 低, 收, 漲跌]
  params: col（4＝收盤）
- trading：afterTrading/tradingIndex，整月；data=[日期(民國115/10/07), 成交張數, 金額(仟元), 筆數, 櫃買指數, 漲跌]
  params: col（2＝金額仟元）
- insti：insti/summary?type=Daily，單日；tables[0].data=[單位名稱, 買進金額, 賣出金額, 買賣超]
  params: row（單位名稱開頭，如「三大法人合計」）, col（3）
- margin：margin/balance，單日；tables[0].summary 兩列「合計(張)」「融資金(仟元)」，欄見 fields
  params: row（summary 列名開頭）, col（欄索引：6＝資餘額、14＝券餘額）
單日類往回看 LOOKBACK_DAYS 日；stat 非 ok 或沒資料略過。
"""
from __future__ import annotations

import json

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

BASE = "https://www.tpex.org.tw/www/zh-tw/"
GAP = 3.0
LOOKBACK_DAYS = 7


def _get_json(cache: dict, url: str):
    if url not in cache:
        C.throttle("tpex", GAP)
        cache[url] = json.loads(C.http_get(url).decode("utf-8-sig"))
    return cache[url]


def _norm_date(s: str):
    s = str(s).strip()
    if "/" in s and len(s.split("/")[0]) == 4:
        y, m, d = s.split("/")
        return C.d_day(y, m, d)
    return C.roc_date_to_iso(s)


def _label(row) -> str:
    """列名：data 列在第 0 欄；margin 的 summary 列第 0 欄是空字串、名稱在第 1 欄。全形空白去掉。"""
    for c in row[:2]:
        if str(c).strip():
            return str(c).replace("\u3000", "").strip()
    return ""


def month_obs(d: dict, col: int) -> list:
    tables = d.get("tables") or []
    if d.get("stat", "").lower() != "ok" or not tables:
        return []
    return C.clean_obs([(_norm_date(r[0]), r[col]) for r in tables[0].get("data", [])])


def _months(today) -> list[str]:
    y, m = today.year, today.month
    py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
    return [f"{py:04d}%2F{pm:02d}%2F01", f"{y:04d}%2F{m:02d}%2F01"]


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}
    today = C.today_taipei()

    def one(s: dict):
        p = C.params(s)
        kind = p["kind"]
        col = int(p["col"])
        if kind in ("inx", "trading"):
            path = "indexInfo/inx" if kind == "inx" else "afterTrading/tradingIndex"
            rows = []
            for ds in _months(today):
                rows.extend(month_obs(_get_json(cache, f"{BASE}{path}?date={ds}&id=&response=json"), col))
            return C.clean_obs(rows)
        rows = []
        for day in C.recent_weekdays(LOOKBACK_DAYS, today):
            ds = day.strftime("%Y%%2F%m%%2F%d")
            if kind == "insti":
                d = _get_json(cache, f"{BASE}insti/summary?type=Daily&date={ds}&id=&response=json")
                key = "data"
            elif kind == "margin":
                d = _get_json(cache, f"{BASE}margin/balance?date={ds}&id=&response=json")
                key = "summary"
            else:
                raise ValueError(f"未知 kind {kind}")
            tables = d.get("tables") or []
            if d.get("stat", "").lower() != "ok" or not tables or not tables[0].get(key):
                continue
            hit = None
            for r in tables[0][key]:
                if _label(r).startswith(p["row"]):
                    hit = r
                    break
            if hit is None:
                raise KeyError(f"{day} 找不到列「{p['row']}」（格式可能改版）")
            rows.append((day.isoformat(), hit[col]))
        return C.clean_obs(rows)

    return C.run_specs(specs, one)
