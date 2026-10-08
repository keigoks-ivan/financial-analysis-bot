"""總務省統計局 消費者物價指數（CPI）月次 CSV（Shift_JIS）。

檔案：https://www.stat.go.jp/data/cpi/<基準年>/csv/zmi<基準年>aa.csv（全國）／tmi<基準年>aa.csv（東京都區部）
結構：前 6 列是表頭（第 1 列為日文品目名、第 3 列為品目符號、最後是權數），之後每列 YYYYMM + 各品目指數。

統計局沒有公布「前年同月比」的長期機器可讀序列（長期時系列在 e-Stat，檔案清單是 JS 頁，抓不到），
所以年增率用各基準期檔「檔內」自算：同一個基準檔裡的當月指數對上年同月指數，和官方公布的做法相同，
不跨基準接續（跨基準的接續指數會多出換算誤差）。多個基準檔重疊的月份，取最新基準檔。

params:
  kind    yoy（預設，輸出年增率 %）
  item    品目名稱（日文，比對第 1 列，取第一個完全相符的欄）
  files   基準檔網址清單，新到舊
"""
from __future__ import annotations

from ._http import get
from .jp_common import csv_rows, run_specs, num


def parse_index(raw: bytes) -> tuple:
    """-> (品目名稱清單, {YYYYMM: row})。"""
    rows = csv_rows(raw, "cp932")
    names = rows[0]
    data = {}
    for r in rows:
        if r and len(r[0]) == 6 and r[0].isdigit():
            data[r[0]] = r
    return names, data


def yoy_in_file(names, data, item) -> dict:
    """單一基準檔內的年增率 {YYYY-MM-01: pct}。品目不在檔內回 {}。"""
    if item not in names:
        return {}
    col = names.index(item)
    out = {}
    for ym, r in data.items():
        prev = "%04d%s" % (int(ym[:4]) - 1, ym[4:])
        if prev not in data:
            continue
        a = num(r[col]) if col < len(r) else None
        b = num(data[prev][col]) if col < len(data[prev]) else None
        if a is None or b is None or b == 0:
            continue
        out["%s-%s-01" % (ym[:4], ym[4:])] = (a / b - 1.0) * 100.0
    return out


def fetch(specs):
    cache: dict = {}

    def load(url):
        if url not in cache:
            cache[url] = parse_index(get(url, binary=True))
        return cache[url]

    def one(s):
        p = s["params"]
        merged: dict = {}
        errs = []
        # 新到舊：舊基準檔只補新基準檔沒有的月份
        for url in p["files"]:
            try:
                names, data = load(url)
            except Exception as e:  # noqa: BLE001
                if url == p["files"][0]:
                    raise          # 最新基準檔抓不到就整條失敗，不拿舊基準檔充數
                errs.append(str(e)[:80])
                continue
            for d, v in yoy_in_file(names, data, p["item"]).items():
                merged.setdefault(d, v)
        if not merged and errs:
            raise RuntimeError("；".join(errs))
        return list(merged.items())
    return run_specs(specs, one)
