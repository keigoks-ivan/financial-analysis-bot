"""聯準會理事會 FEDS Notes 的 CSV（EBP 衰退機率、FCI-G）。月末日期轉當月 1 日。"""
import csv
import io

from ._http import get, month_first, to_float


def parse(text, col, scale=1.0):
    obs = {}
    for r in csv.DictReader(io.StringIO(text)):
        v = to_float(r.get(col))
        d = (r.get("date") or "").strip()
        if v is None or not d:
            continue
        obs[month_first(d)] = round(v * scale, 6)
    return sorted(obs.items())


def fetch(specs):
    res, cache = {}, {}
    for s in specs:
        p = s["params"]
        try:
            if p["url"] not in cache:
                cache[p["url"]] = get(p["url"])
            obs = parse(cache[p["url"]], p["col"], p.get("scale", 1.0))
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料：%s" % p["col"]}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
