"""中證指數有限公司（www.csindex.com.cn）指數日行情：滬深 300 等。

一次請求就能回全部歷史（5,000 多筆）；本地已有歷史時只抓最近約 400 天。

params：
  index_code  指數代碼，如 "000300"
  since       選填，回補起日（YYYYMMDD），預設 "20050408"
  probe_url   完整網址（CI probe 用）
"""
from __future__ import annotations

import datetime as dt

try:
    from . import cn_common as C
except ImportError:
    import cn_common as C

URL = "https://www.csindex.com.cn/csindex-home/perf/index-perf?indexCode=%s&startDate=%s&endDate=%s"


def parse(j: dict) -> list:
    out = []
    for r in j.get("data") or []:
        d, v = str(r.get("tradeDate", "")), C.to_float(r.get("close"))
        if len(d) == 8 and v is not None:
            out.append(("%s-%s-%s" % (d[:4], d[4:6], d[6:]), v))
    return out


def fetch(specs: list[dict]) -> dict:
    res = {}
    s = C.session()
    today = C.today()
    for sp in specs:
        p = sp["params"]
        since = p.get("since", "20050408")
        try:
            start = since if C.need_backfill(sp["sid"], int(since[:4])) else (today - dt.timedelta(days=400)).strftime("%Y%m%d")
            j = C.http_json(s, "GET", URL % (p["index_code"], start, today.strftime("%Y%m%d")))
            obs = parse(j)
            res[sp["sid"]] = {"obs": sorted(obs)} if obs else {"error": "沒有解析到數值"}
        except Exception as e:  # noqa: BLE001
            res[sp["sid"]] = {"error": "中證指數抓取失敗：%s" % str(e)[:150]}
    return res
