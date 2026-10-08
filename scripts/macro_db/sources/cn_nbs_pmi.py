"""國家統計局「中國採購經理指數運行情況」新聞稿附件（最新 13 個月）。

國家數據平台通常比新聞稿晚一個月才有當月 PMI，所以 cn_nbs 的 overlay 用這支補最新月份。
流程：統計局「最新發布」列表頁 → 找標題含「采购经理指数运行情况」的最新一篇 → 頁內第一個 .xls 附件 → 讀「制造业」「非制造业」兩張表。
不是 fetcher（REGISTRY 沒有登記），只給 cn_nbs 呼叫。
"""
from __future__ import annotations

import datetime as dt
import re
from urllib.parse import urljoin

try:
    from . import cn_common as C
except ImportError:
    import cn_common as C

LIST_URL = "https://www.stats.gov.cn/sj/zxfb/"
EPOCH = dt.date(1899, 12, 30)


def find_release(list_html: str) -> str | None:
    for m in re.finditer(r"<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>([^<]*)</a>", list_html):
        if "采购经理指数运行情况" in C.clean(m.group(2)):
            return m.group(1)
    return None


def find_xls(page_html: str) -> str | None:
    m = re.search(r"href=['\"]([^'\"]+\.xls)['\"]", page_html, re.I)
    return m.group(1) if m else None


def parse_sheet(rows: list, col: str) -> list:
    """標題列含 col（去空白後相等）；其下各列第一格為 Excel 日期序號（當月 1 日）。"""
    hdr = j = None
    for i, r in enumerate(rows):
        names = [C.clean(c) for c in r]
        if col in names:
            hdr, j = i, names.index(col)
            break
    if hdr is None:
        raise ValueError("新聞稿附件找不到欄 %s" % col)
    out = []
    for r in rows[hdr + 1:]:
        if not r or not isinstance(r[0], (int, float)) or j >= len(r):
            continue
        d = EPOCH + dt.timedelta(days=int(r[0]))
        x = C.to_float(r[j])
        if x is not None:
            out.append(("%04d-%02d-01" % (d.year, d.month), x))
    return out


def load_sheets(s, cache: dict) -> dict:
    """-> {工作表名: rows}；同一次 fetch 內只下載一次。"""
    if "sheets" in cache:
        return cache["sheets"]
    lst = C.http(s, "GET", LIST_URL).content.decode("utf-8", "replace")
    rel = find_release(lst)
    if not rel:
        raise ValueError("統計局最新發布列表裡找不到 PMI 新聞稿")
    page_url = urljoin(LIST_URL, rel)
    page = C.http(s, "GET", page_url).content.decode("utf-8", "replace")
    xls = find_xls(page)
    if not xls:
        raise ValueError("PMI 新聞稿頁面沒有 xls 附件")
    content = C.http(s, "GET", urljoin(page_url, xls)).content
    import xlrd
    wb = xlrd.open_workbook(file_contents=content)
    cache["sheets"] = {sh.name: [[(c.value if c.value != "" else None) for c in sh.row(i)] for i in range(sh.nrows)]
                       for sh in wb.sheets()}
    return cache["sheets"]


def latest(cfg: dict, s, cache: dict) -> list:
    sheets = load_sheets(s, cache)
    name = C.clean(cfg["sheet"])
    for k, rows in sheets.items():
        if C.clean(k) == name:
            return parse_sheet(rows, C.clean(cfg["col"]))
    raise ValueError("附件沒有工作表 %s" % cfg["sheet"])
