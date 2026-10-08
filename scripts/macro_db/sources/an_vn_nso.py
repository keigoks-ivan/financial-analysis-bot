"""越南國家統計局（NSO，前身統計總局 GSO）fetcher（www.nso.gov.vn，免金鑰）。

兩種來源，由 params["kind"] 區分，同一次 fetch() 內依序處理（同站請求一律隔 1 秒以上）：

kind="report"  每月／每季社經報告附表 Excel
    列表頁 https://www.nso.gov.vn/en/monthly-report/?paged=N（每頁 5 篇，新到舊）→ 報告頁 → 附表連結（.xlsx／.xls）。
    附表檔名每期不同、工作表名稱各年不同，所以一律用「表內標題文字」找表、用「欄位表頭文字」找欄、用「列名」找列，
    不寫死位置。每份附表的期別（年月）從 CPI 表頭「<月份> <年> over」讀；讀不到才退回報告頁網址。
    平常只看列表第 1 頁（最新 5 篇）。環境變數 MACRO_DB_BACKFILL=1 時把列表全部頁抓完（只收 2020 年以後的期別），
    約 100 份附表，要 6～8 分鐘；store 會保留舊日期，回補跑一次就好。
    params：table（表代號，見 TABLES）、row（列代號）、sub（選填，見各表）、scale（選填）。
kind="customs"  海關進出口 E01–E07（NSO 轉載，固定網址、原地更新、每年一份）
    報告頁 /en/data-and-statistics/<年>/<月>/exports-and-imports-value-by-months-of-<年>/ 找各檔連結。
    平常抓今年（1～2 月再加去年）；回補模式往回抓到 2020 年（找不到該年檔就略過）。
    params：file（E01…E07）、row（列名開頭，不分大小寫）、flow（E03 用，export／import）、scale（選填）。
iip_file       IIP 序列的 params 加 "iip_file": true 時，另讀資料統計頁第 1 頁上的單月 IIP 附表（比社經報告早約 1 週），
    只取當月「9/2026 over 9/2025」的年增率；同月以社經報告附表為準。

規則：IIP 不同月份檔案的同月水準不一致，所以只取每檔「當月」的年增率（指數－100），不拼水準。
同一份檔案被多條序列共用時只下載、只解析一次。缺值略過。
"""
from __future__ import annotations

import datetime as dt
import io
import os
import re
import time

import requests
from bs4 import BeautifulSoup

try:
    from . import _http
except ImportError:
    import _http

BASE = "https://www.nso.gov.vn"
LIST_URL = BASE + "/en/monthly-report/?paged=%d"
DATA_URL = BASE + "/en/data-and-statistics/"
CUSTOMS_URL = BASE + "/en/data-and-statistics/%d/%02d/exports-and-imports-value-by-months-of-%d/"
MIN_YEAR = 2020           # 回補只收這一年以後
MAX_PAGES = 40
GAP = 1.1                 # 同站請求最短間隔（秒）

MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
          "october", "november", "december"]
_MON_RX = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
MON_YEAR = re.compile(r"\b" + _MON_RX + r"\b\.?[\s,]*(20\d\d)\b", re.I)
Q_YEAR = re.compile(r"\bq([1-4])\b[\s/,.-]*(20\d\d)\b", re.I)


def mon_num(name: str) -> int:
    return [m[:3] for m in MONTHS].index(name.lower()[:3]) + 1


# ---------- 網路 ----------
_last = [0.0]


def _get(url: str, *, binary: bool = False, ok404: bool = False):
    """GET，同站至少隔 GAP 秒；429／5xx／連線錯誤退避重試 3 次；ok404 時 404 回傳 None。"""
    last = None
    for i in range(4):
        wait = GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = requests.get(url, headers={"User-Agent": _http.NAMED_UA}, timeout=_http.TIMEOUT)
            if r.status_code == 200:
                return r.content if binary else r.content.decode("utf-8", "replace")
            if r.status_code == 404 and ok404:
                return None
            last = RuntimeError("HTTP %s" % r.status_code)
            if r.status_code not in (429, 500, 502, 503, 504):
                break
        except requests.RequestException as e:
            last = e
        time.sleep(2 * (i + 1))
    raise RuntimeError("%s：%s" % (url[-90:], last))


# ---------- 活頁簿 → 方格 ----------
def _norm(s) -> str:
    return re.sub(r"\s+", " ", str(s).replace("\xa0", " ")).strip()


def _cell(v):
    if v is None:
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    if isinstance(v, (dt.datetime, dt.date)):
        return "%s %d" % (MONTHS[v.month - 1].capitalize(), v.year)
    s = _norm(v)
    return s or None


def load_grids(content: bytes, name: str = "") -> list:
    """回傳 [(工作表名稱, 方格 rows[list[cell]])]；合併儲存格的值填滿整個合併範圍（只填空格）。"""
    is_xlsx = content[:2] == b"PK"
    out = []
    if is_xlsx:
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
        for ws in wb.worksheets:
            rows = [[_cell(c) for c in r] for r in ws.iter_rows(values_only=True)]
            for rng in ws.merged_cells.ranges:
                v = rows[rng.min_row - 1][rng.min_col - 1] if rng.min_row - 1 < len(rows) and rng.min_col - 1 < len(rows[0]) else None
                if v is None:
                    continue
                for i in range(rng.min_row - 1, min(rng.max_row, len(rows))):
                    for j in range(rng.min_col - 1, min(rng.max_col, len(rows[i]))):
                        if rows[i][j] is None:
                            rows[i][j] = v
            out.append((ws.title, rows))
    else:
        import xlrd
        try:
            wb = xlrd.open_workbook(file_contents=content, formatting_info=True)
        except Exception:  # noqa: BLE001
            wb = xlrd.open_workbook(file_contents=content)
        for sh in wb.sheets():
            rows = [[_cell(sh.cell_value(i, j)) if sh.cell_type(i, j) not in (0, 5, 6) else None
                     for j in range(sh.ncols)] for i in range(sh.nrows)]
            for (r0, r1, c0, c1) in getattr(sh, "merged_cells", []):
                v = rows[r0][c0] if r0 < len(rows) and c0 < sh.ncols else None
                if v is None:
                    continue
                for i in range(r0, min(r1, len(rows))):
                    for j in range(c0, min(c1, sh.ncols)):
                        if rows[i][j] is None:
                            rows[i][j] = v
            out.append((sh.name, rows))
    return out


def sheet_title(rows) -> str:
    """表內標題：前 3 列的文字合併（去掉開頭編號「16.」）。"""
    toks = []
    for r in rows[:3]:
        for c in r:
            if isinstance(c, str):
                toks.append(c)
    t = _norm(" ".join(toks))
    return re.sub(r"^\s*\d+\s*\.?\s*", "", t).lower()


def row_label(r) -> str:
    """列名：該列第一個數值之前（最多前 3 欄）的文字合併，小寫。"""
    toks = []
    for c in r[:3]:
        if isinstance(c, str):
            toks.append(c)
        elif isinstance(c, float):
            break
    return _norm(" ".join(toks)).lower()


def find_row(rows, rx, start: int = 0) -> int | None:
    pat = re.compile(rx, re.I)
    for i in range(start, len(rows)):
        if pat.search(row_label(rows[i])):
            return i
    return None


def col_headers(rows, upto: int) -> list:
    """每欄的表頭文字（第 0..upto-1 列合併；整數年份轉字串；相鄰重複去掉）。"""
    n = max((len(r) for r in rows[:upto]), default=0)
    out = []
    for j in range(n):
        toks = []
        for i in range(upto):
            c = rows[i][j] if j < len(rows[i]) else None
            if isinstance(c, float):
                if c == int(c) and 1990 <= c <= 2100:
                    c = str(int(c))
                else:
                    continue
            if c and (not toks or toks[-1] != c):
                toks.append(c)
        out.append(_norm(" ".join(toks)).lower())
    return out


def num(rows, i, j):
    if i is None or i >= len(rows) or j >= len(rows[i]):
        return None
    v = rows[i][j]
    return v if isinstance(v, float) else None


# ---------- 表定義 ----------
# title：表標題（正規表示式，比對 sheet_title）；exclude：排除；first：資料區第一列的列名（表頭到這一列之前）
TABLES = {
    "cpi": dict(title=r"consumer price index", exclude=None, first=r"^consumer price index"),
    "iip": dict(title=r"index of industrial production", exclude=r"quarters?\b|shipment|inventory|labou?r", first=r"^(whole|entire) industry"),
    "retail": dict(title=r"retail sales? of good|gross retail sales", exclude=r"quarters?\b", first=r"^total"),
    "visitors": dict(title=r"international visitors to viet ?nam", exclude=r"quarters?\b", first=r"^total"),
    "pass": dict(title=r"(passengers? carried|carriage of passengers)", exclude=r"quarters?\b", first=r"(passengers? carried|volume carried)"),
    "stateinv": dict(title=r"(disbursed|realized) .*state budget|state budget investment", exclude=r"quarters?\b", first=r"^total"),
    "newent": dict(title=r"number of newly registered enterprises", exclude=None, first=r"^total"),
    "fdi": dict(title=r"licensed fdi projects", exclude=None, first=r"^total"),
    "gdp_real": dict(title=r"gross domestic (products? )?at constant", exclude=None, first=r"^total"),
    "gdp_nom": dict(title=r"gross domestic (products? )?at current", exclude=None, first=r"^total"),
    "ppi": dict(title=r"^producer price index", exclude=r"input|transport", first=r"^agriculture"),
    "tot": dict(title=r"merchandise terms of trade", exclude=None, first=r"^general index"),
    "labour": dict(title=r"(some labou?r indicators|selected indicators on labou?rs?)", exclude=None, first=r"^labou?r force"),
    "unemp": dict(title=r"unemployment (rate )?and underemployment", exclude=None, first=r"unemployment rate"),
}

# 列代號 → 列名正規表示式（比對 row_label，小寫；各年用字不同，所以寫成能涵蓋新舊用語的樣式）
ROWS = {
    "cpi": {
        "total": r"^consumer price index", "core": r"^core inflation",
        "food": r"^food and (foodstuff|food|catering) service", "bev": r"^(beverages?|drinks?) and (cigarette|tobacco)",
        "garment": r"^(garment|textile)", "housing": r"^housing", "household": r"^(household|family) (equipment|appliance)",
        "health": r"^medic", "transport": r"^transport",
        "comm": r"^(information and communication|post(al)?( and| &)? (tele)?communicat|telecommunication|communication)",
        "educ": r"^education$", "culture": r"^culture", "other": r"^other(s$| goods| commodities)",
    },
    "iip": {"whole": r"^(whole|entire) industry", "mfg": r"^manufactur", "mining": r"^mining and qua"},
    "retail": {"total": r"^total", "goods": r"^retail( sales?)?$", "food": r"^accommodation and (food|catering)",
               "travel": r"^travel", "other": r"^other services"},
    "visitors": {"total": r"^total"},
    "pass": {"total": r"(passengers? carried|volume carried)"},
    "stateinv": {"total": r"^total"},
    "newent": {"total": r"^total"},
    "fdi": {"total": r"^total"},
    "gdp_real": {"total": r"^total", "agri": r"^agriculture, forestry and fish", "ind": r"^industry and construction$",
                 "serv": r"^services?$", "mfg": r"^manufactur"},
    "gdp_nom": {"total": r"^total"},
    "ppi": {"industry": r"^industry$"},
    "tot": {"general": r"^general index"},
    "labour": {"lf": r"^labou?r force", "emp": r"^employed (persons|labou?rs?)", "agri": r"^agriculture, forestry and fish",
               "ind": r"^industry and construction$", "serv": r"^services?$"},
    "unemp": {},
}


def locate(grids, table: str):
    """回傳 (rows, 資料區第一列索引) 或 None。"""
    t = TABLES[table]
    for _, rows in grids:
        title = sheet_title(rows)
        if not re.search(t["title"], title, re.I) or (t["exclude"] and re.search(t["exclude"], title, re.I)):
            continue
        i = find_row(rows, t["first"], 3)
        if i is not None:
            return rows, i
    return None


def report_ym(grids, url: str = ""):
    """附表的報告期別 (年, 月)。NSO 附表偶有筆誤（例如 2024 年 9 月的檔表頭寫成 September 2023），
    所以多處取票、多數決：農業表「as of <月> <日>, <年>」、FDI 表「to <月> <日>, <年>」、CPI 表標題與表頭、檔名「09-2024」。"""
    from collections import Counter
    votes = []

    def add(mon, year):
        try:
            votes.append((int(year), mon_num(mon)))
        except (ValueError, IndexError):
            pass

    cpi_votes = []
    for _, rows in grids:
        t = sheet_title(rows)
        m = re.search(r"\bas of " + _MON_RX + r"\b\.?\s*\d{1,2},?\s*(20\d\d)", t, re.I)
        if m:
            add(m.group(1), m.group(2))
        m = re.search(r"licensed fdi projects.*?\bto " + _MON_RX + r"\b\.?\s*\d{1,2},?\s*(20\d\d)", t, re.I)
        if m:
            add(m.group(1), m.group(2))
        if "consumer price index" in t:
            m = re.search(r"core inflation in " + _MON_RX + r"\b\.?,?\s*(20\d\d)", t, re.I)
            if m:
                cpi_votes.append((m.group(1), m.group(2)))
            for r in rows[:10]:
                for c in r:
                    if isinstance(c, str):
                        m = re.search(r"\b" + _MON_RX + r"\b[\s,.]*(20\d\d)\s*(?:over|versus|vs|compared)", c, re.I)
                        if m:
                            cpi_votes.append((m.group(1), m.group(2)))
                            break
    for mon, yr in cpi_votes:
        add(mon, yr)
    m = re.search(r"(?<!\d)(\d{1,2})[-._](20\d\d)(?!\d)", url.rsplit("/", 1)[-1])
    if m and 1 <= int(m.group(1)) <= 12:
        votes.append((int(m.group(2)), int(m.group(1))))
    if not votes:
        return None
    return Counter(votes).most_common(1)[0][0]


def _d(y, m):
    return "%04d-%02d-01" % (y, m)


def _qd(y, q):
    return "%04d-%02d-01" % (y, (q - 1) * 3 + 1)


BAD_LEVEL = re.compile(r"y-?o-?y|m-?o-?m|%|structure|months?\b|accumulat|quarter|first half|over|plan|same period|\bq[1-4]\b", re.I)


ORD_Q = {"1st": 1, "first": 1, "2nd": 2, "second": 2, "3rd": 3, "third": 3, "4th": 4, "fourth": 4}
_QTOK = re.compile(r"\bq([1-4])\b[\s/,.-]*(20\d\d)|\b(1st|2nd|3rd|4th|first|second|third|fourth)\s+quarters?\b[\s,]*(?:of\s+)?(20\d\d)", re.I)


def parse_quarters(h: str) -> list:
    """表頭或列名裡的所有 (年, 季)：「Q2 2026」「2nd quarter of 2025」。"""
    out = []
    for m in _QTOK.finditer(h):
        if m.group(1):
            out.append((int(m.group(2)), int(m.group(1))))
        else:
            out.append((int(m.group(4)), ORD_Q[m.group(3).lower()]))
    return out


def extract(grids, table: str, ym, want: dict) -> dict:
    """want：{列代號: True}。回傳 {列代號: {date: value}}（只含該表有的）。"""
    got = locate(grids, table)
    if not got:
        return {}
    rows, first = got
    hdr = col_headers(rows, first)
    out: dict = {k: {} for k in want}

    def row_idx(key):
        rx = ROWS[table].get(key)
        return find_row(rows, rx, first) if rx else None

    if table == "cpi":
        if not ym:
            return {}
        y, m = ym
        # 有數字卻沒有列名的列＝列名與數字錯位（例如 2023 年 10 月檔），整張表不採用
        for r in rows[first:first + 20]:
            if not row_label(r) and sum(1 for c in r if isinstance(c, float)) >= 3:
                return {}
        # 欄位：Base year｜上年同月｜上年 12 月｜上月｜累計平均。上年同月欄＝「基期欄」的下一欄，且表頭含上一年的年份
        b = next((j for j, h in enumerate(hdr) if "base year" in h), None)
        if b is None or str(y - 1) not in (hdr[b + 1] if b + 1 < len(hdr) else ""):
            return {}
        col = b + 1
        for key in want:
            v = num(rows, row_idx(key), col)
            if v is not None:
                out[key][_d(y, m)] = v if key == "core" else v - 100.0
        return out

    if table == "iip":
        if not ym:
            return {}
        y, m = ym
        mon = MONTHS[m - 1][:3]
        here = re.compile(r"\b%s[a-z]*\.?,?\s*%d\b" % (mon, y), re.I)                 # 「June 2025」「Mar. 2024」「April, 2024」
        yoy_mark = re.compile(r"y-?o-?y|same period|(over|versus|vs\.?|compared( to| with)?)\s*%s[a-z]*\.?,?\s*%d\b" % (mon, y - 1), re.I)
        mom_mark = re.compile(r"m-?o-?m|(last|previous|prior) month", re.I)
        col = next((j for j, h in enumerate(hdr) if here.search(h) and yoy_mark.search(h) and not mom_mark.search(h)), None)
        if col is None:
            return {}
        for key in want:
            v = num(rows, row_idx(key), col)
            if v is not None:
                out[key][_d(y, m)] = v - 100.0
        return out

    if table in ("retail", "visitors", "pass", "stateinv"):
        cols = []
        for j, h in enumerate(hdr):
            mm = MON_YEAR.findall(h)
            if len(mm) == 1 and not BAD_LEVEL.search(MON_YEAR.sub("", h)):
                cols.append((j, int(mm[0][1]), mon_num(mm[0][0])))
        for key in want:
            i = row_idx(key)
            for j, y, m in cols:
                v = num(rows, i, j)
                if v is not None:
                    out[key][_d(y, m)] = v
        return out

    if table in ("newent", "fdi"):
        if not ym:
            return {}
        pat = re.compile(r"number of (enterprises?|projects?)" if table == "newent" else r"newly registered", re.I)
        col = next((j for j, h in enumerate(hdr) if pat.search(h) and not re.search(r"y-?o-?y|%", h)), None)
        if col is None:
            return {}
        for key in want:
            v = num(rows, row_idx(key), col)
            if v is not None:
                out[key][_d(*ym)] = v
        return out

    if table == "gdp_real":
        cols = []
        for j, h in enumerate(hdr):
            qs = parse_quarters(h)
            if len(qs) == 1 and re.search(r"y-?o-?y|compared|same period", h):
                cols.append((j,) + qs[0])
        for key in want:
            i = row_idx(key)
            for j, y, q in cols:
                v = num(rows, i, j)
                if v is not None:
                    out[key][_qd(y, q)] = v - 100.0
        return out

    if table == "gdp_nom":
        cols = []
        for j, h in enumerate(hdr):
            qs = parse_quarters(h)
            if len(qs) == 1 and not re.search(r"structure|y-?o-?y|%|compared", h):
                cols.append((j,) + qs[0])
        for key in want:
            i = row_idx(key)
            for j, y, q in cols:
                v = num(rows, i, j)
                if v is not None:
                    out[key][_qd(y, q)] = v
        return out

    if table in ("ppi", "tot"):
        for j, h in enumerate(hdr):
            qs = parse_quarters(h)
            if len(qs) >= 2 and qs[1] == (qs[0][0] - 1, qs[0][1]) and re.search(r"over|compared|vs|y-?o-?y", h):
                for key in want:
                    v = num(rows, row_idx(key), j)
                    if v is not None:
                        out[key][_qd(*qs[0])] = v - 100.0 if table == "ppi" else v
        return out

    if table == "labour":
        cols = []
        for j, h in enumerate(hdr):
            qs = parse_quarters(h)
            if len(qs) == 1 and not re.search(r"months|first half|structure|%", h):
                cols.append((j,) + qs[0])
        emp0 = find_row(rows, ROWS[table]["emp"], first)
        for key in want:
            rx = ROWS[table][key]
            i = find_row(rows, rx, emp0 if key in ("agri", "ind", "serv") and emp0 is not None else first)
            for j, y, q in cols:
                v = num(rows, i, j)
                if v is not None:
                    out[key][_qd(y, q)] = v
        return out

    if table == "unemp":
        # 三個區塊（一般、青年、就業不足），底下每列「Q2 2026」「2nd Quarter of 2025」；欄「General／Total」＝第 1 個數值欄
        blocks = {"general": r"^unemployment rate(?!.*youth)", "youth": r"(youth unemployment|unemployment rate of the youth)",
                  "under": r"^underemployment"}
        starts = {k: find_row(rows, rx, first) for k, rx in blocks.items()}
        bounds = sorted(v for v in starts.values() if v is not None)
        for key in want:
            b = starts.get(key)
            if b is None:
                continue
            end = next((x for x in bounds if x > b), len(rows))
            for i in range(b + 1, end):
                lab = row_label(rows[i])
                qs = parse_quarters(lab)
                if len(qs) != 1 or re.search(r"estimate|months|half", lab):
                    continue
                nums_ = [c for c in rows[i] if isinstance(c, float)]
                if nums_:
                    out[key][_qd(*qs[0])] = nums_[0]
        return out
    return {}


# ---------- 列表頁／報告頁 ----------
def list_reports(pages: int) -> list:
    """回傳報告頁網址清單（新到舊）。pages=0 表示抓到沒有為止。"""
    out = []
    p = 1
    while p <= (pages or MAX_PAGES):
        html = _get(LIST_URL % p, ok404=True)
        if not html:
            break
        links = []
        for a in BeautifulSoup(html, "lxml").find_all("a", href=True):
            h = a["href"]
            if re.search(r"/en/data-and-statistics/\d{4}/\d{2}/[^/]+/?$", h) and h not in links:
                links.append(h)
        if not links:
            break
        out += [h for h in links if h not in out]
        p += 1
    return out


def attachment(report_url: str):
    html = _get(report_url)
    xs = [a["href"] for a in BeautifulSoup(html, "lxml").find_all("a", href=True)
          if re.search(r"/wp-content/uploads/.*\.xlsx?$", a["href"], re.I)]
    return xs[0] if xs else None


def slug_year(url: str):
    ys = [int(y) for y in re.findall(r"(?<!\d)(20\d\d|19\d\d)(?!\d)", url.rsplit("/data-and-statistics/", 1)[-1].split("/", 2)[-1])]
    return max(ys) if ys else None


# ---------- 各種來源 ----------
def _scale(spec):
    return float((spec.get("params") or {}).get("scale", 1.0))


def _imf_cpi_check(log):
    """回補時用 IMF 的越南 CPI 總指數年增率對 NSO 附表做對帳（NSO 偶有整張表貼錯月份）。回傳 {date: 年增率} 或 {}。"""
    try:
        try:
            from . import intl_imf
        except ImportError:
            import intl_imf
        r = intl_imf.fetch([{"sid": "x", "params": {"dataflow": "CPI", "key": "VNM.CPI._T.YOY_PCH_PA_PT.M"}}])["x"]
        return dict(r.get("obs") or [])
    except Exception as e:  # noqa: BLE001
        log("  an_vn_nso 警告 IMF CPI 對帳資料取不到，略過對帳：%s" % str(e)[:80])
        return {}


def run_reports(specs, backfill: bool, log) -> dict:
    """specs：kind=report。回傳 {sid: {date: value}}。"""
    need: dict = {}
    for s in specs:
        p = s["params"]
        need.setdefault(p["table"], {})[p["row"]] = True
    if "cpi" in need:
        need["cpi"]["total"] = True            # 對帳用
    imf = _imf_cpi_check(log) if (backfill and "cpi" in need) else {}
    res = {s["sid"]: {} for s in specs}
    urls = list_reports(0 if backfill else 1)
    if backfill:
        urls = [u for u in urls if (slug_year(u) or 0) >= MIN_YEAR]
    warnings = []
    for u in reversed(urls):                   # 舊到新：新的修正值覆蓋舊的
        try:
            att = attachment(u)
            if not att:
                warnings.append("%s 沒有附表" % u[-60:])
                continue
            grids = load_grids(_get(att, binary=True), att)
            ym = report_ym(grids, att)
            if ym is None:
                warnings.append("%s 讀不到期別" % att[-50:])
                continue
            for table, rows in need.items():
                got = extract(grids, table, ym, rows)
                if table == "cpi" and got.get("total"):
                    d0, v0 = next(iter(got["total"].items()))
                    if d0 in imf and abs(v0 - imf[d0]) > 0.6:
                        warnings.append("CPI 與 IMF 對不上（%s：NSO 附表 %.2f，IMF %.2f），這份附表的 CPI 不採用：%s" % (d0[:7], v0, imf[d0], att[-40:]))
                        got = {}
                for s in specs:
                    p = s["params"]
                    if p["table"] == table:
                        for d, v in (got.get(p["row"]) or {}).items():
                            if d >= p.get("from", "%d-01-01" % MIN_YEAR):
                                res[s["sid"]][d] = v * _scale(s)
        except Exception as e:  # noqa: BLE001
            warnings.append("%s：%s" % (u[-60:], str(e)[:80]))
    for w in warnings:
        log("  an_vn_nso 警告 " + w)
    return res


def _iip_file_links() -> list:
    html = _get(DATA_URL)
    out = []
    for a in BeautifulSoup(html, "lxml").find_all("a", href=True):
        if re.search(r"/data-and-statistics/\d{4}/\d{2}/index-of-industrial-production-in-[a-z]+-of-\d{4}/?$", a["href"]):
            out.append(a["href"])
    return out


def run_iip_file(specs, log) -> dict:
    """specs：params 帶 iip_file 的 IIP 序列；row 為 ROWS["iip"] 的列代號。"""
    res = {s["sid"]: {} for s in specs}
    for u in _iip_file_links():
        try:
            att = attachment(u)
            if not att:
                continue
            for _, rows in load_grids(_get(att, binary=True), att):
                hit = None
                for r in rows[:8]:
                    for j, c in enumerate(r):
                        if isinstance(c, str):
                            m = re.search(r"\b(\d{1,2})/(20\d\d)\s+over\s+\1/(20\d\d)\b", c)
                            if m and int(m.group(3)) == int(m.group(2)) - 1:
                                hit = (j, int(m.group(2)), int(m.group(1)))
                if not hit:
                    continue
                j, y, mth = hit
                for s in specs:
                    pat = re.compile(ROWS["iip"][s["params"]["row"]], re.I)
                    # 這個檔的第 1 欄是代碼（數字），列名在第 2 欄
                    i = next((k for k, r in enumerate(rows) if len(r) > 1 and isinstance(r[1], str) and pat.search(r[1].lower())), None)
                    v = num(rows, i, j)
                    if v is not None:
                        res[s["sid"]][_d(y, mth)] = v - 100.0
                break
        except Exception as e:  # noqa: BLE001
            log("  an_vn_nso 警告 IIP 單月檔 %s：%s" % (u[-50:], str(e)[:80]))
    return res


def customs_links(year: int) -> dict:
    """{'E01': url, …}；頁面月份不固定（建頁月），逐月試到有為止。"""
    for mm in (3, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12):
        html = _get(CUSTOMS_URL % (year, mm, year), ok404=True)
        if html is None:
            continue
        links = {}
        for a in BeautifulSoup(html, "lxml").find_all("a", href=True):
            m = re.search(r"/(E0[1-7])-%d[^/]*\.xlsx?$" % year, a["href"], re.I)
            if m:
                links.setdefault(m.group(1).upper(), a["href"])
        if links:
            return links
    return {}


_MON_WORDS = {m: i + 1 for i, m in enumerate(MONTHS)}
_MON_WORDS.update({m[:3]: i + 1 for i, m in enumerate(MONTHS)})
_MON_WORDS.update({"sept": 9})


def _month_of(c):
    if not isinstance(c, str):
        return None
    return _MON_WORDS.get(c.strip().lower().rstrip("."))


def customs_extract(rows, file: str, row_rx: str, flow: str | None, year: int) -> dict:
    """E01／E02：每月兩欄（數量、金額千美元）；E03：每月兩欄（出口、進口）。回傳 {date: 千美元}。
    月份欄名稱有 Jan.／Feb／June／January 各種寫法，且合併儲存格會讓同一個月名佔兩欄，取每月第一欄；金額＝其右一欄。"""
    hr = next((i for i, r in enumerate(rows[:10]) if sum(1 for c in r if _month_of(c)) >= 6), None)
    if hr is None:
        return {}
    first_col: dict = {}
    for j, c in enumerate(rows[hr]):
        m = _month_of(c)
        if m and m not in first_col:
            first_col[m] = j
    sub = rows[hr + 1] if hr + 1 < len(rows) else []
    pat = re.compile(row_rx, re.I)
    i = next((k for k in range(hr + 1, len(rows)) if pat.search(row_label(rows[k]))), None)
    if i is None:
        return {}
    out = {}
    for m, j in first_col.items():
        if file == "E03":
            col = j if flow == "export" else j + 1
            if not (col < len(sub) and isinstance(sub[col], str) and ("export" if flow == "export" else "import") in sub[col].lower()):
                continue
        else:
            col = j + 1
            if not (col < len(sub) and isinstance(sub[col], str) and "value" in sub[col].lower()):
                continue
        v = num(rows, i, col)
        if v:
            out["%04d-%02d-01" % (year, m)] = v
    return out


def run_customs(specs, backfill: bool, log) -> dict:
    res = {s["sid"]: {} for s in specs}
    today = dt.date.today()
    years = [today.year] + ([today.year - 1] if today.month <= 2 else [])
    if backfill:
        years = list(range(today.year, MIN_YEAR - 1, -1))
    for y in sorted(years):
        try:
            links = customs_links(y)
        except Exception as e:  # noqa: BLE001
            log("  an_vn_nso 警告 海關 %d 年頁面：%s" % (y, str(e)[:80]))
            continue
        if not links:
            log("  an_vn_nso 警告 海關 %d 年找不到檔案" % y)
            continue
        rows_by_file: dict = {}
        for f in sorted({s["params"]["file"] for s in specs} | ({"E01", "E02"} if any(s["params"].get("balance") for s in specs) else set())):
            if f not in links:
                continue
            try:
                rows_by_file[f] = load_grids(_get(links[f], binary=True), links[f])[0][1]
            except Exception as e:  # noqa: BLE001
                log("  an_vn_nso 警告 海關 %s %d：%s" % (f, y, str(e)[:80]))
        for s in specs:
            p = s["params"]
            try:
                if p.get("balance"):
                    if "E01" not in rows_by_file or "E02" not in rows_by_file:
                        continue
                    a = customs_extract(rows_by_file["E01"], "E01", p["row"], None, y)
                    b = customs_extract(rows_by_file["E02"], "E02", p["row"], None, y)
                    vals = {d: a[d] - b[d] for d in a if d in b}
                elif p["file"] in rows_by_file:
                    rows = rows_by_file[p["file"]]
                    vals = customs_extract(rows, p["file"], p["row"], p.get("flow"), y)
                    if p.get("minus_row"):
                        sub = customs_extract(rows, p["file"], p["minus_row"], p.get("flow"), y)
                        vals = {d: v - sub[d] for d, v in vals.items() if d in sub}
                else:
                    continue
                for d, v in vals.items():
                    res[s["sid"]][d] = v * _scale(s)
            except Exception as e:  # noqa: BLE001
                log("  an_vn_nso 警告 海關 %s %d：%s" % (s["sid"], y, str(e)[:80]))
    return res


def ytd_to_month(d: dict) -> dict:
    """累計值 → 單月值（同年連續兩個月都有才相減；1 月＝累計本身）。"""
    out = {}
    for k in sorted(d):
        y, m = int(k[:4]), int(k[5:7])
        if m == 1:
            out[k] = d[k]
        else:
            prev = "%04d-%02d-01" % (y, m - 1)
            if prev in d:
                out[k] = d[k] - d[prev]
    return out


def fetch(specs: list) -> dict:
    log = print
    backfill = os.environ.get("MACRO_DB_BACKFILL") == "1"
    by_kind: dict = {}
    for s in specs:
        by_kind.setdefault(s["params"].get("kind", "report"), []).append(s)
    iip_specs = [s for s in by_kind.get("report", []) if s["params"].get("iip_file")]
    raw: dict = {}
    errors: dict = {}
    # 先單月 IIP 檔（最新、較早公布），再社經報告附表（同月以附表為準），最後海關
    for label, sp, runner in (("iip_file", iip_specs, lambda x: run_iip_file(x, log)),
                              ("report", by_kind.get("report"), lambda x: run_reports(x, backfill, log)),
                              ("customs", by_kind.get("customs"), lambda x: run_customs(x, backfill, log))):
        if not sp:
            continue
        try:
            for sid, d in runner(sp).items():
                raw.setdefault(sid, {}).update(d)
        except Exception as e:  # noqa: BLE001
            for s in sp:
                errors[s["sid"]] = "%s 整批失敗：%s" % (label, str(e)[:150])
    out = {}
    for s in specs:
        sid = s["sid"]
        d = raw.get(sid) or {}
        if sid in errors and not d:
            out[sid] = {"error": errors[sid]}
            continue
        if s["params"].get("xform") == "ytd_diff":
            d = ytd_to_month(d)
        obs = sorted(d.items())
        out[sid] = {"obs": obs} if obs else {"error": errors.get(sid) or "解析後沒有任何觀測值"}
    return out
