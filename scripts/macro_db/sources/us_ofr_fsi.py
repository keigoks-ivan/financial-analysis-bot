"""美國財政部金融研究辦公室（OFR）金融壓力指數 fsi.csv：欄 Date、OFR FSI、Credit、Equity valuation、
Safe assets、Funding、Volatility…（各分項為對 OFR FSI 的貢獻點數，加總＝總指數）。"""
import csv
import io

from ._http import get, to_float
from .us_common import run_specs


def parse(text, col):
    out = []
    for r in csv.DictReader(io.StringIO(text)):
        v = to_float(r.get(col))
        d = (r.get("Date") or "").strip()
        if v is not None and len(d) >= 10:
            out.append((d[:10], v))
    return out


def fetch(specs):
    cache = {}

    def load(s):
        p = s["params"]
        if p["url"] not in cache:
            cache[p["url"]] = get(p["url"])
        return parse(cache[p["url"]], p["col"])

    return run_specs(specs, load)
