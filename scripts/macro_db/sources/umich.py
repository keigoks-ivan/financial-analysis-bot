"""密西根大學消費者調查官網檔（比 FRED 早約一個月）。欄位：Month,YYYY,<col>"""
import csv
import io

from ._http import get, to_float

MONTHS = {m: i + 1 for i, m in enumerate(
    "January February March April May June July August September October November December".split())}


def parse(text, col):
    obs = []
    for r in csv.DictReader(io.StringIO(text)):
        m = MONTHS.get((r.get("Month") or "").strip())
        v = to_float(r.get(col))
        if m is None or v is None or not (r.get("YYYY") or "").strip():
            continue
        obs.append(("%s-%02d-01" % (r["YYYY"].strip(), m), v))
    obs.sort()
    return obs


def fetch(specs):
    res, cache = {}, {}
    for s in specs:
        p = s["params"]
        try:
            if p["url"] not in cache:
                cache[p["url"]] = get(p["url"])
            obs = parse(cache[p["url"]], p["col"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料：%s" % p["col"]}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
