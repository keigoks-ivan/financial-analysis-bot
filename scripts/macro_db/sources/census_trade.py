"""Census 對各國商品貿易頁（foreign-trade/balance/c<code>.html）。

年表格式：月份 年 出口 進口 餘額（百萬美元，Census basis，未季調）。
"""
import re

from ._http import get

MONTHS = {m: i + 1 for i, m in enumerate(
    "January February March April May June July August September October November December".split())}
KIND = {"exports": 0, "imports": 1, "balance": 2}


def parse(html):
    t = re.sub(r"<[^>]*>", "|", html)
    t = re.sub(r"[\s|]+", "|", t)
    rows = re.findall(
        r"\|(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\|(\d{4})\|(-?[\d,.]+)\|(-?[\d,.]+)\|(-?[\d,.]+)", t)
    out = {}
    for mon, yr, a, b, c in rows:
        d = "%s-%02d-01" % (yr, MONTHS[mon])
        out[d] = [float(x.replace(",", "")) for x in (a, b, c)]
    return out


def fetch(specs):
    res, cache = {}, {}
    for s in specs:
        p = s["params"]
        try:
            if p["code"] not in cache:
                cache[p["code"]] = parse(get("https://www.census.gov/foreign-trade/balance/c%s.html" % p["code"]))
            tab = cache[p["code"]]
            if not tab:
                raise ValueError("頁面解析不到月表（c%s）" % p["code"])
            i = KIND[p["kind"]]
            res[s["sid"]] = {"obs": sorted((d, v[i]) for d, v in tab.items())}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
