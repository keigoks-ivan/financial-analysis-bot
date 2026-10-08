"""新加坡統計局（SingStat）Table Builder API（免金鑰）。

網址：https://tablebuilder.singstat.gov.sg/api/table/tabledata/<table_id>?limit=2000
  必須加 limit（預設只回 500 筆）；要帶 User-Agent（用 _http 的網站網址 UA）。
  回應 Data.row[]：{rowText, columns:[{key:"2026 Aug"|"2026 2Q"|"2026", value:"字串"}]}。
params：
  table_id  表格代碼（必填），如 "M014811"
  row       列名 rowText（必填，去空白後完全比對），如 "GDP In Chained (2015) Dollars"
  scale     選填，乘以此數後再存
  probe_url 選填（fetcher 不讀）
同一張表被多條序列引用時只抓一次。缺值（空白、"-"、"na"）略過。
"""
from __future__ import annotations

import json
import re

try:
    from . import _http
    from . import an_common as A
except ImportError:
    import _http
    import an_common as A

URL = "https://tablebuilder.singstat.gov.sg/api/table/tabledata/%s?limit=2000"


def key_to_date(k: str) -> str | None:
    k = str(k).strip()
    m = re.match(r"^(\d{4}) ([A-Za-z]{3})$", k)
    if m:
        mon = A.month_num(m[2])
        return A.ym_date(m[1], mon) if mon else None
    m = re.match(r"^(\d{4}) ([1-4])Q$", k)
    if m:
        return A.yq_date(m[1], int(m[2]))
    if re.match(r"^\d{4}$", k):
        return "%s-01-01" % k
    return None


def parse(text: str, row: str) -> list:
    d = json.loads(text)["Data"]
    for r in d["row"]:
        if r["rowText"].strip() == row:
            out = []
            for c in r["columns"]:
                dt = key_to_date(c["key"])
                if dt is not None:
                    out.append((dt, c["value"]))
            return out
    raise ValueError("表內找不到列「%s」" % row)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s):
        p = s["params"]
        url = URL % p["table_id"]
        if url not in cache:
            cache[url] = _http.get(url)
        rows = [(d, v) for d, v in parse(cache[url], p["row"])]
        out = {}
        for d, v in rows:
            x = A.to_float(v)
            if x is not None:
                out[d] = x * float(p.get("scale", 1.0))
        return sorted(out.items())

    return A.run_specs(specs, one)
