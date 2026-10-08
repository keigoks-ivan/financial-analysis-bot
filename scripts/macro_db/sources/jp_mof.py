"""財務省：公債殖利率（日次）、外貨準備等（月次）。

kind=jgb       jgbcm_all.csv（Shift_JIS，1974 年起每日）。第 2 列為欄名（基準日,1年,2年,...,40年），
               日期為和曆（S49.9.24、H31.4.30、R8.9.30），缺值為 "-"。
               注意：jgbcm_all.csv 只在每月初更新一次（涵蓋到上個月底），當月的每日數字在同目錄的 jgbcm.csv，
               所以另抓 recent_url 並合併（同日期以 recent 為準）。
               params: url, recent_url, tenor（例如 "10年"）
kind=reserves  外貨準備等の状況 historical.csv（月次，單位百萬美元）。params: url, col（0 起算）, col_check, scale（選填；百萬美元 -> 億美元 用 0.01）
"""
from __future__ import annotations

import re

from .jp_common import (Cache, check_header, compact, csv_rows, d_month, month_of, num, run_specs,
                        wareki_dot, wareki_year_text)


def jgb_obs(raw: bytes, tenor: str) -> list:
    rows = csv_rows(raw, "cp932")
    hi = next((i for i, r in enumerate(rows) if r and compact(r[0]) == "基準日"), None)
    if hi is None:
        raise ValueError("找不到欄名列（基準日）")
    names = [compact(c) for c in rows[hi]]
    if compact(tenor) not in names:
        raise ValueError("欄名 %s 不在檔內" % tenor)
    c = names.index(compact(tenor))
    out = []
    for r in rows[hi + 1:]:
        d = wareki_dot(r[0]) if r else None
        if d and c < len(r):
            v = num(r[c])
            if v is not None:
                out.append(("%04d-%02d-%02d" % d, v))
    return out


def reserves_obs(raw: bytes, col: int, col_check=None, what="", scale: float = 1.0) -> list:
    rows = csv_rows(raw, "cp932")
    if col_check:
        check_header(rows, col, range(6, 19), col_check, what)
    out = []
    year = None
    for r in rows[19:]:
        if len(r) <= col:
            continue
        y = None
        if len(r) > 2 and re.match(r"^\d{4}$", r[2].strip()):
            y = int(r[2])
        elif r[0].strip():
            y = wareki_year_text(r[0])
        if y:
            year = y
        m = month_of(r[1])
        if year is None or m is None:
            continue
        v = num(r[col])
        if v is not None:
            out.append((d_month(year, m), round(v * scale, 6) if scale != 1.0 else v))
    return out


def fetch(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        raw = cache.get_url(p["url"])
        if p.get("kind") == "reserves":
            return reserves_obs(raw, p["col"], p.get("col_check"), s["sid"], p.get("scale", 1.0))
        merged = dict(jgb_obs(raw, p["tenor"]))
        if p.get("recent_url"):
            try:
                merged.update(jgb_obs(cache.get_url(p["recent_url"]), p["tenor"]))
            except Exception as e:  # noqa: BLE001  當月檔抓不到：沿用全期間檔，頁面會因資料落後標過期
                if not merged:
                    raise
        return list(merged.items())
    return run_specs(specs, one)
