"""紐約聯準銀行 Markets API：EFFR 每日成交量等（JSON refRates）。"""
import datetime as dt
import json

from ._http import get, to_float


def parse(text, field):
    obs = {}
    for r in json.loads(text).get("refRates", []):
        v = to_float(r.get(field))
        d = r.get("effectiveDate")
        if v is not None and d:
            obs[d[:10]] = v
    return sorted(obs.items())


def fetch(specs):
    res = {}
    end = (dt.date.today() + dt.timedelta(days=30)).isoformat()
    for s in specs:
        p = s["params"]
        try:
            url = ("https://markets.newyorkfed.org/api/rates/unsecured/effr/search.json"
                   "?startDate=%s&endDate=%s" % (p.get("start", "2016-03-01"), end))
            obs = parse(get(url), p["field"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
