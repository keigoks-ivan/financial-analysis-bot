"""經濟部統計處開放資料（service.moea.gov.tw/EE520/opendata/*.csv，UTF-8 BOM）。

資料期欄「資料期(民國年)」為民國 YYYMM（11507＝2026-07）。篩選欄值需 strip（行業代碼尾有空白）。
params: file（檔名，會 URL 編碼）, where（{欄名: 值} 篩選）, value（取值欄名）
"""
from __future__ import annotations

import csv
import io
from urllib.parse import quote

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

BASE = "https://service.moea.gov.tw/EE520/opendata/"
PERIOD_COL = "資料期(民國年)"


def parse(text: str, where: dict, value: str) -> list:
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("空檔")
    first = {k.strip(): v for k, v in rows[0].items() if k}
    for k in list(where) + [value, PERIOD_COL]:
        if k not in first:
            raise KeyError(f"CSV 找不到欄「{k}」，表頭：{list(first)[:10]}")
    out = []
    for r in rows:
        r = {(k or "").strip(): (v or "").strip() for k, v in r.items()}
        if all(r.get(k) == v for k, v in where.items()):
            out.append((C.roc_ym_to_date(r[PERIOD_COL]), r[value]))
    return C.clean_obs(out)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s: dict):
        p = C.params(s)
        raw = C.http_get_cached(cache, BASE + quote(p["file"]))
        return parse(raw.decode("utf-8-sig", errors="replace"), p.get("where", {}), p["value"])

    return C.run_specs(specs, one)
