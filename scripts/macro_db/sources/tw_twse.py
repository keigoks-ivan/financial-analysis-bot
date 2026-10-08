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
- mi_index_ind：afterTrading/MI_INDEX?type=IND（各類指數收盤，單日；第一張「價格指數(臺灣證券交易所)」表）
  params: row（指數名稱，如「半導體類指數」）
- mfi94u：TAIEX/MFI94U（發行量加權股價報酬指數，一次回傳整月；2003-01 起）
- twtb4u：dayTrading/TWTB4U（當日沖銷統計，單日；tables[0].data[0]）
  params: col（1＝成交股數占市場比重%、3＝買進成交金額占市場比重%）
單日類（bfi82u／margn／mi_index_ind／twtb4u）：往回看 LOOKBACK_DAYS 個日曆日的平日，stat 非 OK（假日／尚未公布）略過。
"""
from __future__ import annotations

import json
import os
import time

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

BASE = "https://www.twse.com.tw/rwd/zh/"
GAP = 3.0               # 秒；同站請求間隔
LOOKBACK_DAYS = 7

# ---- 新增 kind（mi_index_ind／mfi94u／twtb4u）用的設定 ----
GAP_FAST = 1.0                      # 秒；新 kind 同站請求間隔（規格下限 1 秒）
# 回補模式：MACRO_DB_BACKFILL=1。證交所這幾個端點沒有「整月」版本（mfi94u 除外），單日端點每個交易日要 1 次請求，
# 全部回到 2010 年要 4,000 次以上，超過 30 分鐘上限，所以只回補到下列起日（實測平均每個請求約 1.5 秒；約 950 次請求，連同平常的抓取約 26 分鐘）。
BACKFILL_SINCE = {"mi_index_ind": "2025-07-01", "twtb4u": "2025-07-01"}
BACKFILL_MFI94U_FROM = (2003, 1)    # 報酬指數月頁，2003-01 起（更早被拒）；約 280 次請求
BACKFILL_MAX_SEC = 1500             # 回補總時間上限（25 分鐘）；到時間就停，已抓的照常寫入
_T0: list = []


def _get_json(cache: dict, url: str):
    if url not in cache:
        C.throttle("twse", GAP)
        cache[url] = json.loads(C.http_get(url).decode("utf-8-sig"))
    return cache[url]


def backfill_on() -> bool:
    return os.environ.get("MACRO_DB_BACKFILL") == "1"


def _get_json_fast(cache: dict, url: str):
    """GAP_FAST 間隔版；回補模式超過時間上限且網址未快取時回 None（呼叫端停止往更早的日子）。"""
    if url in cache:
        return cache[url]
    if backfill_on():
        if not _T0:
            _T0.append(time.time())
        if time.time() - _T0[0] > BACKFILL_MAX_SEC:
            return None
    C.throttle("twse", GAP_FAST)
    cache[url] = json.loads(C.http_get(url).decode("utf-8-sig"))
    return cache[url]


def mi_index_table(d: dict) -> dict:
    """MI_INDEX?type=IND -> {指數名稱: 收盤指數字串}（取「價格指數(臺灣證券交易所)」表，找不到就取第一張首欄為「指數」的表）。"""
    if d.get("stat") != "OK":
        return {}
    tabs = d.get("tables") or []
    pick = next((t for t in tabs if "價格指數" in str(t.get("title", "")) and "臺灣證券交易所" in str(t.get("title", ""))), None)
    if pick is None:
        pick = next((t for t in tabs if (t.get("fields") or [""])[0].strip() == "指數"), None)
    if pick is None:
        return {}
    return {str(r[0]).strip(): r[1] for r in pick.get("data", []) if len(r) > 1}


def twtb4u_row(d: dict) -> list:
    if d.get("stat") != "OK" or not d.get("tables"):
        return []
    data = d["tables"][0].get("data") or []
    return data[0] if data else []


def mfi94u_obs(d: dict) -> list:
    if d.get("stat") != "OK":
        return []
    return C.clean_obs([(C.roc_date_to_iso(r[0]), r[1]) for r in d.get("data", [])])


def _days(kind: str, today) -> list:
    """要抓的日子（新到舊）：平常近 LOOKBACK_DAYS 天；回補模式到 BACKFILL_SINCE 的所有平日。"""
    if not backfill_on():
        return C.recent_weekdays(LOOKBACK_DAYS, today)
    from datetime import date
    since = date.fromisoformat(BACKFILL_SINCE[kind])
    return C.recent_weekdays((today - since).days + 1, today)


def _daily_new(cache: dict, kind: str, today, row: str | None, col: int | None) -> list:
    out, errs, ok = [], 0, 0
    for day in _days(kind, today):
        ds = day.strftime("%Y%m%d")
        key = (kind, ds)
        if key not in cache:
            url = (f"{BASE}afterTrading/MI_INDEX?date={ds}&type=IND&response=json" if kind == "mi_index_ind"
                   else f"{BASE}dayTrading/TWTB4U?date={ds}&response=json")
            try:
                d = _get_json_fast(cache, url)
            except Exception:  # noqa: BLE001  單日失敗不拖垮整批；全部失敗才報錯
                cache[key] = None
                d = False
            if d is None:      # 回補時間到
                break
            # 只留需要的部分，避免回補時把整天個股表留在記憶體
            if d is not False:
                cache[key] = mi_index_table(d) if kind == "mi_index_ind" else twtb4u_row(d)
                cache.pop(url, None)
        got = cache[key]
        if got is None:
            errs += 1
            continue
        if kind == "mi_index_ind":
            if not got:
                continue
            if row not in got:
                raise KeyError(f"{ds} 找不到指數「{row}」（格式可能改版）")
            out.append((day.isoformat(), got[row]))
        else:
            if not got:
                continue
            out.append((day.isoformat(), got[col]))
        ok += 1
    if not ok and errs:
        raise C.FetchError(f"{kind} 全部 {errs} 天請求失敗")
    return C.clean_obs(out)


def mfi94u_months(today) -> list:
    if not backfill_on():
        return _months_to_fetch(today)
    out, (y, m) = [], BACKFILL_MFI94U_FROM
    while (y, m) <= (today.year, today.month):
        out.append(f"{y:04d}{m:02d}01")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out[::-1]      # 新到舊，時間到先丟掉最舊的


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
        if kind in ("mi_index_ind", "twtb4u"):
            return _daily_new(cache, kind, today, p.get("row"), int(p["col"]) if "col" in p else None)
        if kind == "mfi94u":
            for ds in mfi94u_months(today):
                d = _get_json_fast(cache, f"{BASE}TAIEX/MFI94U?date={ds}&response=json")
                if d is None:
                    break
                rows.extend(mfi94u_obs(d))
            return C.clean_obs(rows)
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
