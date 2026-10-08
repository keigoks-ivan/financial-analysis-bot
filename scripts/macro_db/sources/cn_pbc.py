"""中國人民銀行「調查統計司／統計數據」年度 Excel（www.pbc.gov.cn）。

人行每年一組頁面、每個月把當年的 xlsx（舊年份是 xls）換成新版，只含當年 12 欄／12 列。做法：
  1. 抓統計數據總覽頁，解析出各年份、各分類（貨幣統計概覽、社會融資規模）的頁面網址
  2. 抓分類頁，用表格標題（官方儲備資產、貨幣供應量…）找到 Excel 連結
  3. 讀 Excel：橫向表（月份在欄、項目在列）或縱向表（月份在列、項目在欄）
第一次（本地沒有歷史）回補到 since 年，之後只抓今年與去年，歷史靠 store 累積。

params：
  sec     分類頁名稱："貨幣統計概覽" 的簡體 "货币统计概览" 或 "社会融资规模"
  table   表格標題（簡體，子字串即可）
  kind    "horiz"（橫向：label 為列名的正規式）或 "vert"（縱向：col 為欄名）
  label   kind=horiz：項目列名的正規式（比對時已去掉全部空白）
  col     kind=vert：欄名（去空白後完全相等）
  scale   選填，乘以此數
  since   選填，回補起始年，預設 2016
  probe_url 完整網址（CI probe 用）
"""
from __future__ import annotations

import io
import re

try:
    from . import cn_common as C
except ImportError:
    import cn_common as C

HOST = "https://www.pbc.gov.cn"
INDEX = HOST + "/diaochatongjisi/116219/116319/index.html"


# ---------- 索引與分類頁 ----------
def parse_index(html: str) -> dict:
    """{年: {分類名: 絕對網址}}。年份標題是「2026年统计数据」，其後的連結屬於該年，直到下一個年份標題。"""
    out: dict = {}
    year = None
    for m in re.finditer(r"<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>([^<]{2,40})</a>", html):
        href, text = m.group(1), m.group(2).strip()
        ym = re.match(r"^(\d{4})年统计数据$", text)
        if ym:
            year = int(ym.group(1))
            out.setdefault(year, {})
        elif year and "/116319/" in href and text != "统计数据":
            out[year].setdefault(text, href if href.startswith("http") else HOST + href)
    return out


def parse_section(html: str) -> list:
    """分類頁 -> [(標題去空白, [xls/xlsx 絕對網址])]。"""
    out = []
    for m in re.finditer(r'titp20">(.*?)</div>(.*?)</tr>', html, re.S):
        title = C.clean(re.sub(r"<[^>]+>", " ", m.group(1)))
        links = re.findall(r'href="([^"]+\.xlsx?)"', m.group(2), re.I)
        out.append((title, [l if l.startswith("http") else HOST + l for l in links]))
    return out


# ---------- Excel ----------
def read_rows(content: bytes, url: str) -> list:
    """第一張有內容的工作表 -> list[list]（空字串轉 None）。xls 用 xlrd、xlsx 用 openpyxl。"""
    if url.lower().endswith(".xls"):
        import xlrd
        wb = xlrd.open_workbook(file_contents=content)
        for sh in wb.sheets():
            if sh.nrows:
                return [[(c.value if c.value != "" else None) for c in sh.row(i)] for i in range(sh.nrows)]
        return []
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True, read_only=True)
    for ws in wb.worksheets:
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        if any(any(c is not None for c in r) for r in rows):
            return rows
    return []


def month_of(v, ordinal=None):
    """2026.01／'2026.10'／2026.1 -> '2026-MM-01'；其他回 None。
    人行把 10 月寫成 2026.1 或 '2026.10'，1 月又可能寫成 2026.1：小數只有 1 位時，用「這是該年第幾個月份格」(ordinal) 判斷。"""
    if v is None or isinstance(v, bool):
        return None
    m = re.match(r"^((?:19|20)\d\d)\.(\d{1,2})$", str(v).strip())
    if not m:
        return None
    if len(m.group(2)) == 2:
        mo = int(m.group(2))
    elif ordinal:
        mo = ordinal
    else:
        mo = int(m.group(2))
    return "%s-%02d-01" % (m.group(1), mo) if 1 <= mo <= 12 else None


def label_of(row: list) -> str:
    for c in row[:3]:
        if isinstance(c, str) and C.clean(c):
            return C.clean(c)
    return ""


def parse_horiz(rows: list, label_rx: str) -> list:
    """月份在欄：找月份標題列（至少 6 個月份格）→ 比對項目列 → 逐欄取值。"""
    hdr = None
    for i, r in enumerate(rows):
        cols, n = {}, 0
        for j, c in enumerate(r):
            if month_of(c):
                n += 1
                cols[j] = month_of(c, n)
        if len(cols) >= 6:
            hdr, mcols = i, cols
            break
    if hdr is None:
        raise ValueError("找不到月份標題列")
    rx = re.compile(label_rx)
    for r in rows[hdr + 1:]:
        if rx.search(label_of(r)):
            out = []
            for j, d in mcols.items():
                if j < len(r):
                    x = C.to_float(r[j])
                    if x is not None:
                        out.append((d, x))
            return out
    raise ValueError("找不到項目列 %s" % label_rx)


def parse_vert(rows: list, col: str) -> list:
    """月份在列：找出欄名列（某一格去空白後等於 col），其後第一格為月份的列逐列取值。"""
    hdr = None
    for i, r in enumerate(rows):
        names = [C.clean(c) for c in r]
        if col in names:
            hdr, j = i, names.index(col)
            break
    if hdr is None:
        raise ValueError("找不到欄 %s" % col)
    out, seen = [], {}
    for r in rows[hdr + 1:]:
        if r and month_of(r[0]):
            y = str(r[0]).strip()[:4]
            seen[y] = seen.get(y, 0) + 1
            d = month_of(r[0], seen[y])
        else:
            d = None
        if d and j < len(r):
            x = C.to_float(r[j])
            if x is not None:
                out.append((d, x))
    return out


# ---------- 抓取 ----------
class _Cache:
    def __init__(self, s):
        self.s = s
        self.pages: dict = {}
        self.files: dict = {}
        self.index = None

    def years(self):
        if self.index is None:
            self.index = parse_index(C.http(self.s, "GET", INDEX).content.decode("utf-8", "replace"))
            if not self.index:
                raise C.Blocked("人行統計數據總覽頁解析不到年份")
        return self.index

    def section(self, url):
        if url not in self.pages:
            self.pages[url] = parse_section(C.http(self.s, "GET", url).content.decode("utf-8", "replace"))
        return self.pages[url]

    def file(self, url):
        if url not in self.files:
            self.files[url] = read_rows(C.http(self.s, "GET", url).content, url)
        return self.files[url]


def parse_one(cache: _Cache, year: int, p: dict) -> list:
    sec_url = cache.years().get(year, {}).get(p["sec"])
    if not sec_url:
        raise ValueError("%d 年沒有「%s」頁" % (year, p["sec"]))
    want = C.clean(p["table"])
    for title, links in cache.section(sec_url):
        if want in title and links:
            rows = cache.file(links[0])
            return parse_horiz(rows, p["label"]) if p["kind"] == "horiz" else parse_vert(rows, p["col"])
    raise ValueError("%d 年「%s」頁沒有「%s」的 Excel" % (year, p["sec"], p["table"]))


def fetch(specs: list[dict]) -> dict:
    res: dict = {}
    s = C.session()
    cache = _Cache(s)
    try:
        yrs = sorted(cache.years())
    except Exception as e:  # noqa: BLE001
        return {sp["sid"]: {"error": "人行總覽頁失敗：%s" % str(e)[:120]} for sp in specs}
    newest = yrs[-1]
    for sp in specs:
        p = sp["params"]
        since = p.get("since", 2016)
        first = since if C.need_backfill(sp["sid"], since) else newest - 1
        obs: dict = {}
        errs = []
        for y in [y for y in yrs if y >= first]:
            try:
                for d, v in parse_one(cache, y, p):
                    obs[d] = v
            except C.Blocked as e:
                errs.append((y, str(e)))
                break
            except Exception as e:  # noqa: BLE001
                errs.append((y, str(e)[:120]))
        recent_err = [m for y, m in errs if y >= newest - 1]
        if recent_err or not obs:
            res[sp["sid"]] = {"error": "；".join(m for _, m in errs)[:300] or "沒有解析到數值"}
            continue
        sc = p.get("scale") or 1.0
        res[sp["sid"]] = {"obs": sorted((d, v * sc) for d, v in obs.items())}
    return res


def latest_for(kind: str, s) -> list:
    """給 cn_nbs 補最新月份用。kind='m2_level'：當年貨幣供應量表的 M2 期末餘額。"""
    cfg = {"m2_level": {"sec": "货币统计概览", "table": "货币供应量", "kind": "horiz", "label": "^货币和准货币"}}[kind]
    cache = _Cache(s)
    return parse_one(cache, max(cache.years()), cfg)
