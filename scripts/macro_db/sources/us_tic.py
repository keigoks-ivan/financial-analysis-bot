"""美國財政部 TIC：外國持有美國公債（主要外國持有人，十億美元）。

近 13 個月：slt_table5.txt（tab 分隔，欄＝月份 YYYY-MM）；較早的歷史：mfhhis01.txt
（每個年度一段，分段標頭列為 'Country, <月份縮寫...>' 與年份列）。兩檔拼接，近期優先。
"""
import re
import time

from ._http import get, to_float
from .us_common import SITE_GAP, run_specs

MM = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}


def parse_recent(text, country):
    out = {}
    hdr = None
    for line in text.replace("\r", "").split("\n"):
        c = [x.strip().strip('"') for x in line.split("\t")]
        if c and c[0] == "Country":
            hdr = c
            continue
        if hdr and c and c[0] == country:
            for h, v in zip(hdr[1:], c[1:]):
                x = to_float(v)
                if x is not None and re.fullmatch(r"\d{4}-\d\d", h):
                    out[h + "-01"] = x
    return out


def parse_history(text, country):
    """mfhhis01.txt：年份列（'Country' 起頭、其餘為年）與月份列（第 2 欄起為月份縮寫）成對出現。"""
    out = {}
    years = months = None
    for line in text.replace("\r", "").split("\n"):
        c = [x.strip().strip('"') for x in line.split("\t")]
        if len(c) > 2 and c[1] in MM:
            months = c
            continue
        if c and c[0] == "Country":
            years = c
            continue
        if c and c[0] == country and years and months:
            for k in range(1, len(c)):
                try:
                    y, mo = int(years[k]), MM[months[k]]
                except (ValueError, KeyError, IndexError):
                    continue
                v = to_float(c[k])
                if v is not None:
                    out["%04d-%02d-01" % (y, mo)] = v
    return out


def fetch(specs):
    docs = {}

    def doc(url):
        if url not in docs:
            if docs:
                time.sleep(SITE_GAP)
            docs[url] = get(url)
        return docs[url]

    def load(s):
        p = s["params"]
        recent = parse_recent(doc(p["url"]), p["country"])
        hist = parse_history(doc(p["history"]), p["country"])
        hist.update(recent)          # 同月以近期檔為準
        return sorted(hist.items())

    return run_specs(specs, load)
