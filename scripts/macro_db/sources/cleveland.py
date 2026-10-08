"""克里夫蘭聯準銀行通膨即時預測（月增率，每日）。

JSON 是一串物件，每個目標月一個；chart.subcaption='YYYY-M'，dataset[].data 逐日、tooltext 內含 'MM/DD'。
每日一點取「日期所在月份＝目標月」的那張，即當月即時預測。
"""
import json
import re

from ._http import get, to_float


def parse(text, item):
    data = json.loads(text)
    obs = {}
    for ch in data:
        sub = ch["chart"]["subcaption"]
        ty, tm = [int(x) for x in sub.split("-")]
        ds = next((d for d in ch["dataset"] if d.get("seriesname") == item), None)
        if ds is None:
            continue
        for pt in ds["data"]:
            v = to_float(pt.get("value"))
            if v is None:
                continue
            m = re.search(r"\{br\}(\d{2})/(\d{2})\{br\}", pt.get("tooltext", ""))
            if not m:
                continue
            mo, dy = int(m.group(1)), int(m.group(2))
            if mo != tm:
                continue
            obs["%04d-%02d-%02d" % (ty, mo, dy)] = v
    return sorted(obs.items())


def fetch(specs):
    res, text = {}, None
    for s in specs:
        try:
            if text is None:
                text = get("https://www.clevelandfed.org/-/media/files/webcharts/inflationnowcasting/nowcast_month.json")
            obs = parse(text, s["params"]["item"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
