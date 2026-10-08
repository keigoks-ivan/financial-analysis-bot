"""中央銀行（CBC）。

kind=cpx（預設）：cpx.cbc.gov.tw/api/dataapi/Get?FileName=<file>
  JSON：data.dataSets 每列 [期間, 欄1, 欄2, ...]；欄位順序＝data.structure 各 Table 的笛卡兒積；缺值 "-"。
  params: file, col（1 起算）, col_name（選填：該欄的「/」連接名稱，用來偵測欄位順序改版）
  期間：YYYYMmm（月）／YYYYMMDD（日）。
kind=fsi_csv：cbc.gov.tw 開放資料 CSV（金融健全指標-不動產市場），年資料、民國年。
  params: url, col（0 起算，0＝民國年）
kind=fsi_csv_ym：同上開放資料 CSV，但第 0 欄是民國年月（9103＝民國 91 年 3 月＝2002-03；11503＝2026-03），季資料。
  params: url, col（0 起算）
"""
from __future__ import annotations

import csv
import io
import itertools
import json
import re

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

CPX = "https://cpx.cbc.gov.tw/api/dataapi/Get?FileName="


def column_names(d: dict) -> list[str]:
    tabs = [[c["data"] for c in v] for v in d["data"]["structure"].values()]
    return ["/".join(p) for p in itertools.product(*tabs)]


def cpx_obs(d: dict, col: int, col_name: str | None = None) -> list:
    if col_name is not None:
        names = column_names(d)
        if col - 1 >= len(names) or names[col - 1] != col_name:
            got = names[col - 1] if col - 1 < len(names) else "(超出範圍)"
            raise ValueError(f"央行表欄位順序已變：第 {col} 欄預期「{col_name}」實為「{got}」")
    rows = []
    for r in d["data"]["dataSets"]:
        if col < len(r):
            rows.append((C.period_to_date(r[0]), r[col]))
    return C.clean_obs(rows)


def fsi_obs(text: str, col: int) -> list:
    rows = []
    for r in csv.reader(io.StringIO(text)):
        if not r or not re.match(r"^\d{2,3}$", r[0].strip()):
            continue
        if col < len(r):
            rows.append((C.d_year(int(r[0]) + 1911), r[col]))
    return C.clean_obs(rows)


def fsi_ym_obs(text: str, col: int) -> list:
    """第 0 欄民國年月 YYYMM（季資料，月份 03/06/09/12）-> 該季首月 1 日（與全庫季資料口徑一致）。"""
    rows = []
    for r in csv.reader(io.StringIO(text)):
        if not r or not re.match(r"^\d{4,5}$", r[0].strip()):
            continue
        d = C.roc_ym_to_date(r[0])
        if d is None or col >= len(r):
            continue
        y, m = int(d[:4]), int(d[5:7])
        rows.append((C.d_quarter(y, (m - 1) // 3 + 1), r[col]))
    return C.clean_obs(rows)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s: dict):
        p = C.params(s)
        if p.get("kind", "cpx") == "fsi_csv_ym":
            text = C.http_get_cached(cache, p["url"]).decode("utf-8-sig", errors="replace")
            return fsi_ym_obs(text, int(p["col"]))
        if p.get("kind", "cpx") == "fsi_csv":
            text = C.http_get_cached(cache, p["url"]).decode("utf-8-sig", errors="replace")
            return fsi_obs(text, int(p["col"]))
        key = p["file"]
        if ("cpx", key) not in cache:
            cache[("cpx", key)] = json.loads(C.http_get(CPX + key).decode("utf-8-sig"))
        return cpx_obs(cache[("cpx", key)], int(p["col"]), p.get("col_name"))

    return C.run_specs(specs, one)
