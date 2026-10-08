"""紐約聯準銀行 Markets API：EFFR 每日成交量等（JSON refRates）、SOMA 持有組成（summary.json）。"""
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


def parse_soma(text, field, scale=1e12):
    """SOMA 每週持有（美元，字串）：asOfDate 為週三；空字串（例如 FRN 尚未發行前）略過，不填 0。"""
    obs = {}
    for r in json.loads(text)["soma"]["summary"]:
        v = to_float(r.get(field))
        d = r.get("asOfDate")
        if v is not None and d:
            obs[d[:10]] = v / scale
    return sorted(obs.items())


def fetch(specs):
    res = {}
    end = (dt.date.today() + dt.timedelta(days=30)).isoformat()
    soma = {}
    for s in specs:
        p = s["params"]
        try:
            if p.get("kind") == "soma_summary":
                url = p.get("url", "https://markets.newyorkfed.org/api/soma/summary.json")
                if url not in soma:
                    soma[url] = get(url)
                obs = parse_soma(soma[url], p["field"], float(p.get("scale", 1e12)))
            else:
                url = ("https://markets.newyorkfed.org/api/rates/unsecured/effr/search.json"
                       "?startDate=%s&endDate=%s" % (p.get("start", "2016-03-01"), end))
                obs = parse(get(url), p["field"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
