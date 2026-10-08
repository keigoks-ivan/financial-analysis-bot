"""e-Stat「ファイル」免登入下載（不是 e-Stat API，不需 appId）。

網址：https://www.e-stat.go.jp/stat-search/file-download?statInfId=<ID>&fileKind=<0 或 4>
statInfId 是固定編號：官方每次發布會把同一個檔案原地更新（若某次發布後失效，頁面會標過期，
到 e-Stat 該統計的「ファイル」頁找新編號）。每條序列都驗證表頭／標題，改版時明確報錯而不是抓錯欄。

kind=lfs     勞動力調查長期時系列表（xlsx）。params: sheet（工作表名開頭）, col, col_check, url
kind=wage    每月勤勞統計長期時系列表（xls，sheet TL）。同一張表上段是指數、下段是「對前年同月增減率」，
             依標題列切段，這裡取下段（官方公布的年增率）。params: expect（表頭應含的字串清單）, url
kind=iip     鉱工業指數 時系列表（xlsx）。params: sheet, item（品目番號，鉱工業總合＝1000000000）, url
"""
from __future__ import annotations

import re

from ._http import get
from .jp_common import (Cache, check_header, compact, d_month, month_of, num, run_specs, sheets_any,
                        wareki_year_text)


def sheet_by_prefix(sheets: dict, prefix: str):
    for n, rows in sheets.items():
        if compact(n).startswith(compact(prefix)):
            return rows
    raise ValueError("找不到工作表 %s*（現有：%s）" % (prefix, "、".join(list(sheets)[:6])))


# ---------- 勞動力調查 ----------

def lfs_obs(rows, col, col_check=None, what="") -> list:
    if col_check:
        check_header(rows, col, range(4, 9), col_check, what)
    out = []
    year = None
    for r in rows[9:]:
        if len(r) <= max(col, 1):
            continue
        y = wareki_year_text(r[0])
        if y:
            year = y
        m = month_of(r[1])
        if year is None or m is None:
            continue
        v = num(r[col])
        if v is not None:
            out.append((d_month(year, m), v))
    return out


def fetch_lfs(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        sheets = sheets_any(cache.get_url(p["url"]))
        return lfs_obs(sheet_by_prefix(sheets, p["sheet"]), p["col"], p.get("col_check"), s["sid"])
    return run_specs(specs, one)


# ---------- 每月勤勞統計 ----------

MONTH_COLS = list(range(8, 20))   # 年、年平均、上半期、下半期、Q1-4 之後的 1～12 月


def wage_check(rows, expect):
    head = "|".join(compact(rows[r][5]) for r in range(0, 4) if len(rows[r]) > 5)
    for e in expect:
        if compact(e) not in head:
            raise ValueError("表頭應含「%s」，實為「%s」（statInfId 可能已換成別張表）" % (e, head[:90]))


def wage_obs(rows, expect) -> list:
    wage_check(rows, expect)
    # 月份欄位自檢：上段表頭列的 8～19 欄應為 1～12
    hdr = next((r for r in rows[:12] if len(r) > 19 and num(r[8]) == 1.0 and num(r[19]) == 12.0), None)
    if hdr is None:
        raise ValueError("找不到月份表頭列（1～12 月應在第 9～20 欄）")
    start = next((i for i, r in enumerate(rows) if r and compact(r[0]).startswith("前年比")), None)
    if start is None:
        raise ValueError("找不到「前年比」段")
    out = []
    for r in rows[start + 1:]:
        if not r:
            continue
        y = num(r[0])
        if y is None or not (1900 < y < 2200):
            continue
        for k, c in enumerate(MONTH_COLS):
            if c < len(r):
                v = num(r[c])
                if v is not None:
                    out.append((d_month(int(y), k + 1), v))
    return out


def fetch_wage(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        sheets = sheets_any(cache.get_url(p["url"]))
        return wage_obs(sheets["TL"], p["expect"])
    return run_specs(specs, one)


# ---------- 鉱工業指數 ----------

def iip_obs(rows, item) -> list:
    hdr = next((r for r in rows[:6] if any(re.match(r"^(p\s*)?\d{6}$", compact(c)) for c in r)), None)
    if hdr is None:
        raise ValueError("找不到 YYYYMM 表頭列")
    row = next((r for r in rows if r and str(r[0]).strip() == item), None)
    if row is None:
        raise ValueError("找不到品目 %s" % item)
    out = []
    for c, h in enumerate(hdr):
        m = re.match(r"^(?:p\s*)?(\d{4})(\d{2})$", compact(h)) if h is not None else None
        if m and c < len(row):
            v = num(row[c])
            if v is not None:
                out.append((d_month(m.group(1), m.group(2)), v))
    return out


def fetch_iip(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        sheets = sheets_any(cache.get_url(p["url"]))
        return iip_obs(sheet_by_prefix(sheets, p["sheet"]), p["item"])
    return run_specs(specs, one)


def fetch(specs):
    groups: dict = {}
    for s in specs:
        groups.setdefault(s["params"].get("kind"), []).append(s)
    fns = {"lfs": fetch_lfs, "wage": fetch_wage, "iip": fetch_iip}
    res = {}
    for kind, group in groups.items():
        try:
            res.update(fns[kind](group))
        except Exception as e:  # noqa: BLE001
            for s in group:
                res[s["sid"]] = {"error": ("%s：%s" % (type(e).__name__, e))[:300]}
    return res
