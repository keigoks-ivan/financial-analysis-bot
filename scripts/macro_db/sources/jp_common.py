"""日本 fetcher 共用工具：和曆轉西曆、全形數字、Excel／CSV 讀取、逐條包 try/except。

fetcher 介面（SPEC）：fetch(specs) -> {sid: {"obs": [(YYYY-MM-DD, float)]} | {"error": str}}
下載一律走 _http.get（網站網址 UA、timeout 60 秒、失敗重試 2 次）；憑證驗證不關。
"""
from __future__ import annotations

import csv
import io
import re
import unicodedata
import warnings

from ._http import get, to_float

# 和曆元年的前一年（西元年 = 偏移 + 和曆年）
ERA_OFFSET = {"M": 1867, "T": 1911, "S": 1925, "H": 1988, "R": 2018,
              "明": 1867, "大": 1911, "昭": 1925, "平": 1988, "令": 2018}


def nfkc(s) -> str:
    """全形英數字、全形空白轉半形（１月 -> 1月）。"""
    return unicodedata.normalize("NFKC", str(s)) if s is not None else ""


def compact(s) -> str:
    """NFKC 後去掉所有空白（含全形空白、換行），用來比對表頭。"""
    return re.sub(r"\s+", "", nfkc(s))


def wareki_dot(s: str):
    """財務省格式 'S49.9.24' / 'R8.9.30' -> (1974, 9, 24)；不符回 None。"""
    m = re.match(r"^\s*([MTSHR])\s*(\d+|元)\.(\d+)\.(\d+)\s*$", nfkc(s))
    if not m:
        return None
    n = 1 if m.group(2) == "元" else int(m.group(2))
    return ERA_OFFSET[m.group(1)] + n, int(m.group(3)), int(m.group(4))


def wareki_year_text(s) -> int | None:
    """'昭和28年' / '令和元年' / '平成12年' -> 西元年；4 位數字 / 浮點年（1953.0）也接受。"""
    if s is None or s == "":
        return None
    if isinstance(s, (int, float)):
        v = int(s)
        return v if 1800 < v < 2200 else None
    t = nfkc(s).strip()
    m = re.match(r"^(\d{4})(?:\.0)?(?:年)?$", t)
    if m:
        return int(m.group(1))
    m = re.match(r"^(明治|大正|昭和|平成|令和)\s*(元|\d+)\s*年", t)
    if m:
        n = 1 if m.group(2) == "元" else int(m.group(2))
        return ERA_OFFSET[m.group(1)[0]] + n
    return None


def month_of(s) -> int | None:
    """'1月' / '１月' / 'Jan.' 以外只認 'N月'；也接受整數 1..12。"""
    if isinstance(s, (int, float)) and not isinstance(s, bool):
        v = int(s)
        return v if 1 <= v <= 12 and float(s) == v else None
    m = re.match(r"^\s*(\d{1,2})\s*月\s*$", nfkc(s))
    if m and 1 <= int(m.group(1)) <= 12:
        return int(m.group(1))
    return None


def d_month(y, m) -> str:
    return "%04d-%02d-01" % (int(y), int(m))


def d_quarter(y, q) -> str:
    return "%04d-%02d-01" % (int(y), (int(q) - 1) * 3 + 1)


def num(x):
    """儲存格 -> float 或 None。吃千分位、全形、'p 202608' 之類不會進這裡。"""
    if x is None or isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        f = float(x)
        return None if f != f else f
    s = nfkc(x).strip().replace(",", "")
    if s in ("", "-", "…", "***", "x", "X", "－", "#N/A", "n.a.", "NA"):
        return None
    return to_float(s)


def decode_text(raw: bytes, enc: str = "cp932") -> str:
    return raw.decode(enc, "replace")


def csv_rows(raw: bytes, enc: str = "cp932") -> list:
    return list(csv.reader(io.StringIO(raw.decode(enc, "replace"))))


def xlsx_sheets(raw: bytes) -> dict:
    """xlsx -> {sheet名: [row tuple, ...]}（data_only）。"""
    import openpyxl
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(io.BytesIO(raw), data_only=True)
    return {n: [tuple(r) for r in wb[n].iter_rows(values_only=True)] for n in wb.sheetnames}


def xls_sheets(raw: bytes) -> dict:
    """xls -> {sheet名: [row list, ...]}（xlrd；空儲存格為 ''）。"""
    import xlrd
    wb = xlrd.open_workbook(file_contents=raw)
    return {s.name: [s.row_values(i) for i in range(s.nrows)] for s in wb.sheets()}


def sheets_any(raw: bytes) -> dict:
    return xlsx_sheets(raw) if raw[:2] == b"PK" else xls_sheets(raw)


def header_text(rows, col, hdr_rows) -> str:
    """某欄在表頭各列的文字（合併儲存格：每列向左補到最近的非空儲存格，最多 3 欄），去空白後以 | 相連。"""
    out = []
    for r in hdr_rows:
        if r >= len(rows):
            continue
        row = rows[r]
        txt = ""
        for c in range(col, max(col - 4, -1), -1):
            if c < len(row) and row[c] not in (None, ""):
                txt = compact(row[c])
                break
        out.append(txt)
    return "|".join(out)


def check_header(rows, col, hdr_rows, expect, what=""):
    """欄位順序改版偵測：expect（字串或字串清單）必須全部出現在該欄表頭。"""
    exp = [expect] if isinstance(expect, str) else list(expect)
    h = header_text(rows, col, hdr_rows)
    for e in exp:
        if compact(e) not in h:
            raise ValueError("%s 第 %d 欄表頭應含「%s」，實為「%s」（欄位順序可能已改版）" % (what, col, e, h[:80]))


def run_specs(specs, fn):
    """逐條呼叫 fn(spec) -> obs；一條失敗不影響其他條。"""
    res = {}
    for s in specs:
        try:
            obs = fn(s)
            obs = sorted(set(obs))
            if not obs:
                res[s["sid"]] = {"error": "解析後沒有資料"}
            else:
                res[s["sid"]] = {"obs": obs}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": ("%s：%s" % (type(e).__name__, e))[:300]}
    return res


class Cache(dict):
    """同一次 fetch 內，同網址只下載一次。"""

    def get_url(self, url, **kw):
        if url not in self:
            self[url] = get(url, binary=True, **kw)
        return self[url]


def find_link(html: str, pattern: str, base: str) -> str:
    """從 HTML 找第一個符合 pattern 的 href，回傳絕對網址。"""
    from urllib.parse import urljoin
    m = re.search(r'href="([^"]*%s[^"]*)"' % pattern, html)
    if not m:
        raise ValueError("頁面上找不到連結 %s" % pattern)
    return urljoin(base, m.group(1).replace("&amp;", "&"))
