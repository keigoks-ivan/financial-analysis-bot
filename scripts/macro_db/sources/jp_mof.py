"""財務省：公債殖利率（日次）、外貨準備等（月次）、對外證券投資、法人企業統計、稅收。

kind=jgb       jgbcm_all.csv（Shift_JIS，1974 年起每日）。第 2 列為欄名（基準日,1年,2年,...,40年），
               日期為和曆（S49.9.24、H31.4.30、R8.9.30），缺值為 "-"。
               注意：jgbcm_all.csv 只在每月初更新一次（涵蓋到上個月底），當月的每日數字在同目錄的 jgbcm.csv，
               所以另抓 recent_url 並合併（同日期以 recent 為準）。
               params: url, recent_url, tenor（例如 "10年"）
kind=securities 對外及對內證券投資 montha1.csv（月次，Shift_JIS，億日圓）：年份只出現在 1 月列，向下沿用；
               月份取第 1 欄；金額含千分位逗號。params: url, col（0 起算）
kind=ssc_pct   法人企業統計季別 percent.xlsx（季調前期比，%）：期別形如「19854~6月」＝年份連續數字＋起訖月。
               params: url, col, col_check
kind=ssc_level 法人企業統計季別 keitune.xlsx（經常利益金額）：期別為和曆「平成21年4-6月」。params: url, col, col_check
kind=tax       歷年稅收 zeisyu.xls（會計年度，第 3 欄為西曆年，日期記為該年度 4 月 1 日）。params: url, col, col_check
kind=reserves  外貨準備等の状況 historical.csv（月次，單位百萬美元）。params: url, col（0 起算）, col_check, scale（選填；百萬美元 -> 億美元 用 0.01）
"""
from __future__ import annotations

import re

from .jp_common import (Cache, check_header, compact, csv_rows, d_month, month_of, nfkc, num, run_specs,
                        sheets_any, wareki_dot, wareki_year_text)

ERA_BASE = {"昭和": 1925, "平成": 1988, "令和": 2018}


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


def securities_obs(raw: bytes, col: int) -> list:
    rows = csv_rows(raw, "cp932")
    out = []
    year = None
    for r in rows:
        if len(r) <= max(col, 1):
            continue
        if re.match(r"^\d{4}$", r[0].strip()):
            year = int(r[0])
        m = re.match(r"^(\d{1,2})月$", nfkc(r[1]).strip())
        if year is None or not m:
            continue
        v = num(r[col])
        if v is not None:
            out.append((d_month(year, int(m.group(1))), v))
    return out


def ssc_pct_obs(rows, col: int) -> list:
    out = []
    for r in rows:
        if len(r) > max(col, 1):
            m = re.match(r"^(\d{4})(\d{1,2})~(\d{1,2})月", compact(r[1]))
            if m:
                v = num(r[col])
                if v is not None:
                    out.append((d_month(int(m.group(1)), int(m.group(2))), v))
    return out


def ssc_level_obs(rows, col: int) -> list:
    out = []
    for r in rows:
        if len(r) > col:
            m = re.match(r"^(昭和|平成|令和)(\d+)年(\d+)-(\d+)月", compact(r[0]))
            if m:
                v = num(r[col])
                if v is not None:
                    out.append((d_month(ERA_BASE[m.group(1)] + int(m.group(2)), int(m.group(3))), v))
    return out


def tax_obs(rows, col: int) -> list:
    out = []
    for r in rows:
        if len(r) > max(col, 3) and isinstance(r[3], float) and 1900 < r[3] < 2200:
            v = num(r[col])
            if v is not None:
                out.append((d_month(int(r[3]), 4), v))
    return out


def fetch(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        raw = cache.get_url(p["url"])
        k = p.get("kind")
        if k == "securities":
            return securities_obs(raw, p["col"])
        if k in ("ssc_pct", "ssc_level", "tax"):
            rows = list(sheets_any(raw).values())[0]
            if k == "ssc_pct":
                check_header(rows, p["col"], range(11, 13), p["col_check"], s["sid"])
                return ssc_pct_obs(rows, p["col"])
            if k == "ssc_level":
                check_header(rows, p["col"], range(0, 4), p["col_check"], s["sid"])
                return ssc_level_obs(rows, p["col"])
            check_header(rows, p["col"], range(2, 5), p["col_check"], s["sid"])
            return tax_obs(rows, p["col"])
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
