"""Zillow Research 全國寬表（日期為欄）。取 RegionName == United States 那列，月末日期轉成當月 1 日。"""
import csv
import io

from ._http import get, month_first, to_float


def parse(text):
    rows = csv.reader(io.StringIO(text))
    head = next(rows)
    try:
        ri = head.index("RegionName")
    except ValueError:
        ri = 2
    first_date = next(i for i, h in enumerate(head) if h[:2] == "20")
    for r in rows:
        if len(r) > ri and r[ri] == "United States":
            obs = []
            for i in range(first_date, min(len(head), len(r))):
                v = to_float(r[i])
                if v is not None:
                    obs.append((month_first(head[i]), v))
            return obs
    raise ValueError("找不到 United States 列")


def fetch(specs):
    res, cache = {}, {}
    for s in specs:
        url = s["params"]["url"]
        try:
            if url not in cache:
                cache[url] = parse(get(url))
            res[s["sid"]] = {"obs": cache[url]}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
