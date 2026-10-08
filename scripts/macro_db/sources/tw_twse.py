"""臺灣證券交易所（TWSE）rwd JSON。

日資料不做大量歷史回填：每次只抓最近幾天／當月，靠 store 的合併規則（新值覆蓋、舊檔保留）累積歷史。
一次性歷史回填見 tw_backfill_twse.py（不隨每日流程執行）。

kind:
- fmtqik：afterTrading/FMTQIK，一次回傳 date 所在整月。欄 [日期(民國115/09/01), 成交股數, 成交金額, 成交筆數, 發行量加權股價指數, 漲跌點數]
  params: col（0 起算；4＝加權指數收盤、2＝成交金額）
- bfi82u：fund/BFI82U（三大法人買賣金額，單日）。data=[單位名稱, 買進金額, 賣出金額, 買賣差額]
  params: row（單位名稱，如「合計」）, col（3＝買賣差額）
- margn：marginTrading/MI_MARGN?selectType=MS（融資融券彙總，單日）。tables[0].data=[項目, 買進, 賣出, 現金(券)償還, 前日餘額, 今日餘額]
  params: row（項目開頭字串，如「融資金額」「融券(」）, col（5＝今日餘額）
單日類（bfi82u／margn）：往回看 LOOKBACK_DAYS 個日曆日的平日，stat 非 OK（假日／尚未公布）略過。
"""
from __future__ import annotations

import json

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

BASE = "https://www.twse.com.tw/rwd/zh/"
GAP = 3.0               # 秒；同站請求間隔
LOOKBACK_DAYS = 7


def _get_json(cache: dict, url: str):
    if url not in cache:
        C.throttle("twse", GAP)
        cache[url] = json.loads(C.http_get(url).decode("utf-8-sig"))
    return cache[url]


def fmtqik_obs(d: dict, col: int) -> list:
    if d.get("stat") != "OK":
        return []
    return C.clean_obs([(C.roc_date_to_iso(r[0]), r[col]) for r in d.get("data", [])])


def row_value(rows, label: str, col: int, exact: bool):
    for r in rows:
        name = str(r[0]).strip()
        if (name == label) if exact else name.startswith(label):
            return r[col]
    return None


def _months_to_fetch(today) -> list[str]:
    y, m = today.year, today.month
    py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
    return [f"{py:04d}{pm:02d}01", f"{y:04d}{m:02d}01"]


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}
    today = C.today_taipei()

    def one(s: dict):
        p = C.params(s)
        kind = p["kind"]
        rows = []
        if kind == "fmtqik":
            for ds in _months_to_fetch(today):
                d = _get_json(cache, f"{BASE}afterTrading/FMTQIK?date={ds}&response=json")
                rows.extend(fmtqik_obs(d, int(p["col"])))
            return C.clean_obs(rows)
        for day in C.recent_weekdays(LOOKBACK_DAYS, today):
            ds = day.strftime("%Y%m%d")
            if kind == "bfi82u":
                d = _get_json(cache, f"{BASE}fund/BFI82U?type=day&dayDate={ds}&response=json")
                data = d.get("data") if d.get("stat") == "OK" else None
                exact = True
            elif kind == "margn":
                d = _get_json(cache, f"{BASE}marginTrading/MI_MARGN?date={ds}&selectType=MS&response=json")
                data = d["tables"][0]["data"] if d.get("stat") == "OK" and d.get("tables") else None
                exact = False
            else:
                raise ValueError(f"未知 kind {kind}")
            if not data:
                continue
            v = row_value(data, p["row"], int(p["col"]), exact)
            if v is None:
                raise KeyError(f"{ds} 找不到列「{p['row']}」（格式可能改版）")
            rows.append((day.isoformat(), v))
        return C.clean_obs(rows)

    return C.run_specs(specs, one)
