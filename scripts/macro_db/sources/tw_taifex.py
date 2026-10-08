"""臺灣期貨交易所（TAIFEX）openapi：https://openapi.taifex.com.tw/v1/<端點>。

openapi 只回「最近一個交易日」或「近約 21 個交易日」，沒有更長的歷史，所以每天抓、靠 store 的合併規則累積
（新值覆蓋、舊檔保留）。期交所官網的歷史 CSV 會擋機器，不使用。

kind:
- inst_futures：MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheDate（三大法人各期貨契約，最新一個交易日）
  params: contract（如「臺股期貨」）, item（如「外資及陸資」）, field（如「OpenInterest(Net)」）, url
- pcr：PutCallRatio（臺指選擇權買賣權比，近約 21 個交易日）
  params: field（如「PutCallOIRatio%」）, url
日期欄 Date＝YYYYMMDD。
"""
from __future__ import annotations

import json

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

GAP = 1.0


def _rows(cache: dict, url: str) -> list:
    if url not in cache:
        C.throttle("taifex", GAP)
        d = json.loads(C.http_get(url).decode("utf-8-sig"))
        if not isinstance(d, list):
            raise ValueError("期交所 openapi 回傳不是陣列（格式可能改版）")
        cache[url] = d
    return cache[url]


def _iso(s: str) -> str | None:
    return C.period_to_date(str(s).strip()) if len(str(s).strip()) == 8 else None


def inst_futures_obs(rows: list, contract: str, item: str, field: str) -> list:
    out = []
    for r in rows:
        if r.get("ContractCode") == contract and r.get("Item") == item:
            if field not in r:
                raise KeyError(f"找不到欄位 {field}（格式可能改版）")
            out.append((_iso(r["Date"]), r[field]))
    return C.clean_obs(out)


def pcr_obs(rows: list, field: str) -> list:
    out = []
    for r in rows:
        if field not in r:
            raise KeyError(f"找不到欄位 {field}（格式可能改版）")
        out.append((_iso(r["Date"]), r[field]))
    return C.clean_obs(out)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s: dict):
        p = C.params(s)
        rows = _rows(cache, p["url"])
        kind = p["kind"]
        if kind == "inst_futures":
            return inst_futures_obs(rows, p["contract"], p["item"], p["field"])
        if kind == "pcr":
            return pcr_obs(rows, p["field"])
        raise ValueError(f"未知 kind {kind}")

    return C.run_specs(specs, one)
