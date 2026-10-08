"""TSA 每日機場安檢旅客人數：當年頁（/travel/passenger-volumes）與往年頁（/travel/passenger-volumes/<年>）的 HTML 表。"""
import datetime as dt
import re

from ._http import get
from .us_common import SITE_GAP
import time

ROW_RE = re.compile(r"(\d{1,2}/\d{1,2}/\d{4})\s*</td>\s*<td[^>]*>\s*([\d,]+)")
BASE = "https://www.tsa.gov/travel/passenger-volumes"


def parse(html):
    out = {}
    for d, v in ROW_RE.findall(html):
        m, dd, yy = d.split("/")
        out["%04d-%02d-%02d" % (int(yy), int(m), int(dd))] = float(v.replace(",", ""))
    return out


def fetch(specs):
    res = {}
    for s in specs:
        try:
            p = s["params"]
            this = dt.date.today().year
            obs = {}
            for y in range(int(p.get("years_from", 2019)), this + 1):
                url = BASE if y == this else "%s/%d" % (BASE, y)
                try:
                    obs.update(parse(get(url)))
                except Exception:  # noqa: BLE001
                    if y == this:     # 當年頁掛了就算失敗；往年頁掛了略過（已累積在本機）
                        raise
                time.sleep(SITE_GAP)
            res[s["sid"]] = {"obs": sorted(obs.items())} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
