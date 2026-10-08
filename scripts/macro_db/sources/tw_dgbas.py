"""行政院主計總處（DGBAS）XML：國民所得、物價、人力資源。

兩種格式：
- long：<Obs><Item/><TIME_PERIOD/><FREQ/><TYPE/><Item_VALUE/></Obs>（國民所得 na*、物價 pr*）。
  params: dataset, file, item（Item 開頭字串）, typ（預設「原始值」）, contains（選填）, url（寫死的備援網址）
- wide：<DataCollection> 下每筆為一個月（欄位為子元素，第 1 個子元素是年月別）（人力資源 mp*）。
  params: dataset, file, col（第幾個值欄，1＝緊接年月別之後）, url

網址中的 relfile 流水號每次更新可能改變：先問 data.gov.tw（dataset 的 distribution），
物價類的 dataset 44211 是一份 CSV 清單；問不到才用 params.url。
"""
from __future__ import annotations

import csv
import io
import re
import xml.etree.ElementTree as ET

try:
    from . import tw_common as C
except ImportError:  # 直接以 script 方式載入時
    import tw_common as C

PRICE_LIST_DATASET = 44211  # 「物價指數統計XML網址連結」CSV


def _resolve(p: dict, cache: dict) -> str:
    fname = p["file"]
    ds = p.get("dataset")
    fallback = p["url"]
    suffix = "/" + fname.lower() + ".xml"
    if ds == PRICE_LIST_DATASET:
        try:
            for u in C.datagov_urls(ds, cache):
                if u.lower().endswith(".csv"):
                    raw = C.http_get_cached(cache, u).decode("utf-8-sig", errors="replace")
                    for row in csv.reader(io.StringIO(raw)):
                        for cell in row:
                            if cell.lower().endswith(suffix):
                                return cell.strip()
        except Exception:  # noqa: BLE001
            pass
        return fallback
    return C.resolve_url(ds, cache, fallback, pick=lambda u: u.lower().endswith(suffix))


# ---------- long ----------

def parse_long(text: str) -> dict:
    """{(Item, TYPE): [(TIME_PERIOD, Item_VALUE), ...]}（保持出現順序）。"""
    agg: dict = {}
    for m in re.finditer(r"<Obs>(.*?)</Obs>", text, re.S):
        b = m.group(1)

        def g(k, b=b):
            mm = re.search(r"<%s>(.*?)</%s>" % (k, k), b, re.S)
            return mm.group(1).strip() if mm else ""

        agg.setdefault((g("Item"), g("TYPE")), []).append((g("TIME_PERIOD"), g("Item_VALUE")))
    return agg


def pick_long(agg: dict, item: str, typ: str = "原始值", contains: str | None = None):
    for (it, ty), rows in agg.items():
        if ty == typ and it.startswith(item) and (contains is None or contains in it):
            return rows
    raise KeyError(f"找不到 Item 開頭「{item}」TYPE={typ}")


def long_obs(rows) -> list:
    """只收月（YYYYMmm）與季（YYYYQn）；年列略過。"""
    out = []
    for p, v in rows:
        if re.match(r"^\d{4}[MQ]\d{1,2}$", p):
            out.append((C.period_to_date(p), v))
    return C.clean_obs(out)


# ---------- wide ----------

def parse_wide(text: str) -> list[list[str]]:
    """每筆記錄 -> 子元素文字清單（第 0 個是年月別）。"""
    root = ET.fromstring(text.encode("utf-8") if isinstance(text, str) else text)
    recs = []
    for rec in root:
        recs.append([(c.text or "").strip() for c in rec])
    return recs


def wide_obs(recs: list[list[str]], col: int) -> list:
    out = []
    for r in recs:
        if len(r) <= col:
            continue
        p = r[0]
        # 只收月列：YYYYMmm 或 YYYYMM（可帶 Ⓡ/Ⓟ），年列（4 碼）略過
        if re.match(r"^\d{4}M\d{2}$", p) or re.match(r"^\d{6}[ⓅⓇ]?$", p):
            out.append((C.period_to_date(p), r[col]))
    return C.clean_obs(out)


def _decode(b: bytes) -> str:
    return b.decode("utf-8-sig", errors="replace")


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}
    parsed: dict = {}  # url -> parsed structure

    def one(s: dict):
        p = C.params(s)
        url = _resolve(p, cache)
        kind = p.get("kind", "long")
        key = (url, kind)
        if key not in parsed:
            text = _decode(C.http_get_cached(cache, url))
            parsed[key] = parse_long(text) if kind == "long" else parse_wide(text)
        if kind == "long":
            rows = pick_long(parsed[key], p["item"], p.get("typ", "原始值"), p.get("contains"))
            return long_obs(rows)
        return wide_obs(parsed[key], int(p["col"]))

    return C.run_specs(specs, one)
