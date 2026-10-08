"""經濟部能源署開放資料（moeaea.gov.tw/ECW/populace/opendata/wHandOpenData_File.ashx?set_id=N，UTF-8 BOM）。

首欄為日期：月資料 YYYYMM（西元）、年資料 YYYY；第 2 欄為單位；之後各欄為「…(數值)」。
params: set_id, col（欄名；以表頭完全相符）
"""
from __future__ import annotations

import csv
import io

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

URL = "https://www.moeaea.gov.tw/ECW/populace/opendata/wHandOpenData_File.ashx?set_id={}"


def parse(text: str, col: str) -> list:
    rows = list(csv.reader(io.StringIO(text)))
    hdr = [h.strip() for h in rows[0]]
    if col not in hdr:
        raise KeyError(f"找不到欄「{col}」，表頭：{hdr[:6]}")
    ci = hdr.index(col)
    out = []
    for r in rows[1:]:
        if r and ci < len(r):
            out.append((C.period_to_date(r[0].strip()), r[ci]))
    return C.clean_obs(out)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s: dict):
        p = C.params(s)
        raw = C.http_get_cached(cache, URL.format(p["set_id"]))
        return parse(raw.decode("utf-8-sig", errors="replace"), p["col"])

    return C.run_specs(specs, one)
