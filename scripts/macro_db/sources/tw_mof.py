"""財政部統計處：貿易統計。

kind=njswww：web02.mof.gov.tw/njswww/webMain.aspx（統計資料庫 CSV，UTF-8 BOM）
  第一欄為民國期間：「90年」＝年合計列（略過）、「115年 8月」＝月資料。
  params: url, col（表頭子字串，取第一個符合者）
kind=u2010：service.mof.gov.tw/public/data/statistic/trade/u2010ex.csv／u2010im.csv（Big5，各國別）
  第一欄為西元「2026年8月」月資料（「2001年」年合計略過）。
  params: url, col（表頭開頭字串，取第一個符合者）
"""
from __future__ import annotations

import csv
import io
import re

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C


def parse_njswww(text: str, col: str) -> list:
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise ValueError("空檔")
    hdr = [h.strip() for h in rows[0]]
    idx = [i for i, h in enumerate(hdr) if col in h]
    if not idx:
        raise KeyError(f"找不到欄名含「{col}」")
    ci = idx[0]
    out = []
    for r in rows[1:]:
        if r and ci < len(r):
            out.append((C.roc_label_to_date(r[0]), r[ci]))
    return C.clean_obs(out)


def parse_u2010(text: str, col: str) -> list:
    rows = list(csv.reader(io.StringIO(text)))
    hdr = [h.strip() for h in rows[0]]
    idx = [i for i, h in enumerate(hdr) if h.startswith(col)]
    if not idx:
        raise KeyError(f"找不到欄名開頭「{col}」")
    ci = idx[0]
    out = []
    for r in rows[1:]:
        if not r or ci >= len(r):
            continue
        m = re.match(r"^(\d{4})年\s*(\d{1,2})月$", r[0].strip())
        if m:
            out.append((C.d_month(m.group(1), m.group(2)), r[ci]))
    return C.clean_obs(out)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s: dict):
        p = C.params(s)
        raw = C.http_get_cached(cache, p["url"])
        if p.get("kind") == "u2010":
            return parse_u2010(raw.decode("big5", errors="replace"), p["col"])
        return parse_njswww(raw.decode("utf-8-sig", errors="replace"), p["col"])

    return C.run_specs(specs, one)
