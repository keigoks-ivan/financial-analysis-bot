"""馬來西亞統計局（DOSM）OpenDOSM／data.gov.my 資料目錄 API（免金鑰）。

網址：https://api.data.gov.my/data-catalogue/?id=<id>&limit=100000&sort=date[&filter=<值>@<欄>]
  網址在 data-catalogue 後面要有斜線（沒有會 301）。date 為每期第一天（季＝該季首月 1 日）。
params：
  id      資料集代碼（必填），如 "gdp_qtr_real"
  field   取值的欄位（必填），如 "value"、"index"、"exports"
  filter  選填，如 "abs@series"（series 欄等於 abs）、"overall@division"
  scale   選填，乘以此數後再存
  probe_url 選填（fetcher 不讀）
同一個 (id, filter) 只抓一次。
"""
from __future__ import annotations

import json

try:
    from . import _http
    from . import an_common as A
except ImportError:
    import _http
    import an_common as A

URL = "https://api.data.gov.my/data-catalogue/"


def build_url(p: dict) -> str:
    u = "%s?id=%s&limit=100000&sort=date" % (URL, p["id"])
    if p.get("filter"):
        u += "&filter=" + p["filter"]
    return u


def parse(text: str, field: str) -> list:
    rows = json.loads(text)
    if not isinstance(rows, list):
        raise ValueError("回應不是資料列：%s" % str(rows)[:120])
    return [(r["date"][:10], r.get(field)) for r in rows if "date" in r]


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s):
        p = s["params"]
        url = build_url(p)
        if url not in cache:
            cache[url] = _http.get(url)
        return A.clean_obs(parse(cache[url], p["field"]), float(p.get("scale", 1.0)))

    return A.run_specs(specs, one)
