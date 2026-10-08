"""內閣府（ESRI）：GDP 速報、景氣動向指數（CI）、景氣觀察調查、機械訂單。

kind=gdp      GDP 速報統計表 CSV（Shift_JIS）。網址含發布代碼（qe262_2 -> 2622），每次改定都變，
              所以每次先抓 https://www.esri.cao.go.jp/jp/sna/sokuhou/sokuhou_top.html 解析最新代碼。
              params: table（ritu-jg / nritu-jk / ritu-jk / gaku-jk / gaku-mk / gaku-jg / kiyo-jg / kiyo-jk）,
                      col（0 起算）, col_check（該欄表頭應含的英文字串，偵測欄位改版）, url
kind=ci       景氣動向指數 Excel（檔名 MMDDci.xlsx 每月變）：先抓 di.html 解析連結。
              params: col（0 起算）, col_check, url
kind=watcher  景氣觀察調查 watcher3.xls（固定網址，每月原地更新）。
              params: sheet（工作表名開頭）, col_label（表頭文字，找欄）, url
kind=machinery 機械訂單長期系列 Excel（檔名 YYMMchouki-1.xlsx 每月變）：先抓 juchu.html 解析連結。
              params: sheet, col, col_check, url
"""
from __future__ import annotations

import re

from ._http import get
from .jp_common import (Cache, check_header, compact, csv_rows, d_month, d_quarter, find_link, month_of, num,
                        run_specs, sheets_any)

GDP_TOP = "https://www.esri.cao.go.jp/jp/sna/sokuhou/sokuhou_top.html"
CI_PAGE = "https://www.esri.cao.go.jp/jp/stat/di/di.html"
JUCHU_PAGE = "https://www.esri.cao.go.jp/jp/stat/juchu/juchu.html"
WATCHER = "https://www5.cao.go.jp/keizai3/watcher/watcher3.xls"


# ---------- GDP 速報 ----------

def gdp_base(top_html: str) -> tuple:
    """首頁 -> (表格目錄網址, 代碼)。連結形如 .../files/2026/qe262_2/gdemenuja.html。"""
    m = re.search(r'href="([^"]*/files/(\d{4})/qe(\d{2})(\d)_(\d)/)[^"]*"', top_html)
    if not m:
        raise ValueError("GDP 速報首頁找不到最新發布目錄（qeYYQ_N）")
    from urllib.parse import urljoin
    base = urljoin(GDP_TOP, m.group(1)) + "tables/"
    code = m.group(3) + m.group(4) + m.group(5)   # 26 + 2 + 2 -> 2622
    return base, code


def gdp_obs(raw: bytes, col: int, col_check=None, what="") -> list:
    rows = csv_rows(raw, "cp932")
    if col_check:
        check_header(rows, col, range(1, 7), col_check, what)
    out = []
    year = None
    started = False
    for r in rows:
        first = (r[0] if r else "").strip()
        m = re.match(r"^(\d{4})/\s*(\d+)-\s*\d+\.?$", first)
        if m:
            year, mon = int(m.group(1)), int(m.group(2))
        else:
            m2 = re.match(r"^(\d+)-\s*\d+\.?$", first)
            if not m2 or year is None:
                if started:
                    break          # 資料區塊結束（空列或註解列）
                continue
            mon = int(m2.group(1))
        started = True
        if col < len(r):
            v = num(r[col])
            if v is not None:
                out.append((d_quarter(year, (mon - 1) // 3 + 1), v))
    return out


def fetch_gdp(specs):
    cache = Cache()
    top = get(GDP_TOP)
    base, code = gdp_base(top)

    def one(s):
        p = s["params"]
        raw = cache.get_url("%s%s%s.csv" % (base, p["table"], code))
        return gdp_obs(raw, p["col"], p.get("col_check"), s["sid"])
    return run_specs(specs, one)


# ---------- 景氣動向指數 ----------

def ci_obs(rows, col, col_check=None, what="") -> list:
    if col_check:
        check_header(rows, col, range(0, 4), col_check, what)
    out = []
    for r in rows:
        if len(r) > col and isinstance(r[1], (int, float)) and isinstance(r[2], (int, float)):
            v = num(r[col])
            if v is not None:
                out.append((d_month(int(r[1]), int(r[2])), v))
    return out


def fetch_ci(specs):
    cache = Cache()
    html = get(CI_PAGE)
    url = find_link(html, r"\d{4}ci\.xlsx", CI_PAGE)

    def one(s):
        p = s["params"]
        sheets = sheets_any(cache.get_url(url))
        rows = list(sheets.values())[0]
        return ci_obs(rows, p["col"], p.get("col_check"), s["sid"])
    return run_specs(specs, one)


# ---------- 景氣觀察調查 ----------

def watcher_obs(rows, col_label: str) -> list:
    hdr = rows[4:7]
    col = None
    for c in range(len(rows[4])):
        for r in hdr:
            if c < len(r) and compact(r[c]) == compact(col_label):
                col = c
                break
        if col is not None:
            break
    if col is None:
        raise ValueError("找不到表頭「%s」" % col_label)
    out = []
    year = None
    for r in rows[7:]:
        ytxt = compact(r[2]) if len(r) > 2 else ""
        m = re.match(r"^(\d{4})年$", ytxt)
        if m:
            year = int(m.group(1))
        mon = month_of(r[3]) if len(r) > 3 else None
        if year is None or mon is None:
            continue
        v = num(r[col]) if col < len(r) else None
        if v is not None:
            out.append((d_month(year, mon), v))
    return out


def fetch_watcher(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        sheets = sheets_any(cache.get_url(p.get("url") or WATCHER))
        name = next((n for n in sheets if n.startswith(p["sheet"])), None)
        if name is None:
            raise ValueError("找不到工作表 %s*" % p["sheet"])
        return watcher_obs(sheets[name], p["col_label"])
    return run_specs(specs, one)


# ---------- 機械訂單 ----------

def machinery_obs(rows, col, col_check=None, what="") -> list:
    if col_check:
        check_header(rows, col, range(3, 9), col_check, what)
    out = []
    for r in rows:
        if len(r) > col and isinstance(r[1], (int, float)) and isinstance(r[2], (int, float)):
            v = num(r[col])
            if v is not None:
                out.append((d_month(int(r[1]), int(r[2])), v))
    return out


def fetch_machinery(specs):
    cache = Cache()
    html = get(JUCHU_PAGE)
    url = find_link(html, r"\d{4}chouki-1\.xlsx", JUCHU_PAGE)

    def one(s):
        p = s["params"]
        sheets = sheets_any(cache.get_url(url))
        name = next((n for n in sheets if n.startswith(p["sheet"])), None)
        if name is None:
            raise ValueError("找不到工作表 %s*" % p["sheet"])
        return machinery_obs(sheets[name], p["col"], p.get("col_check"), s["sid"])
    return run_specs(specs, one)


def fetch(specs):
    groups: dict = {}
    for s in specs:
        groups.setdefault(s["params"].get("kind"), []).append(s)
    fns = {"gdp": fetch_gdp, "ci": fetch_ci, "watcher": fetch_watcher, "machinery": fetch_machinery}
    res = {}
    for kind, group in groups.items():
        try:
            res.update(fns[kind](group))
        except Exception as e:  # noqa: BLE001
            for s in group:
                res[s["sid"]] = {"error": ("%s：%s" % (type(e).__name__, e))[:300]}
    return res
