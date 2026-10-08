"""國家外匯管理局統計數據 Excel（www.safe.gov.cn）：國際收支季表、銀行結售匯、銀行代客涉外收付款、外債、貨物和服務貿易。

附件網址含日期與雜湊（/safe/file/file/20260929/<hash>.xlsx），每次更新都會變，不能寫死。做法：
  1. 抓每個檔固定的「說明頁」（params.landing_page），解析頁面上的 xls/xlsx 附件連結
  2. 依附件標題選出對應的時間序列檔（國際收支 bop、結售匯 jsh、涉外收付款 skk、外債 debt、貨物和服務貿易 trade）
  3. 下載一次、同一檔的所有序列共用
說明頁改版、解析不到附件連結時，這個檔的全部序列回 {"error": …} 並寫明原因，不會靜默回空。
單位皆為億美元（原表標示）。

params：
  file          bop｜jsh｜skk｜debt｜trade
  landing_page  說明頁完整網址（CI probe 也用它）
  sheet         工作表名稱（bop、jsh、skk、trade 用；比對時去掉空白）
  lab_rx        列標籤正規式（比對時已去掉列標籤內的全部空白）。bop 取第一個符合的列（貸方／借方列標籤重複，所以要用正規式，不能用固定列號）
  hdr_row/col0  jsh、skk：表頭所在列（0 起算）、第一個月份欄
  sec_rx        jsh、skk：項目所在區段（「一、結匯」等區段標題）的正規式；debt：外債部門列標籤的正規式
  row_idx_rx    trade：列標籤正規式；occ 為第幾個符合的列（預設 1）
月份欄的處理：jsh 表頭是 Excel 日期序號，但最前面約 10 格序號壞掉（例如 2010-01-22），所以只相信最後一欄的月份，
往前逐月推算，並檢查最後 24 欄的序號月份與推算相同。trade 表頭是「2015.1」這類文字（1 與 10 月無法區分），同樣從 2015-01 逐月推算並對最後一欄。
"""
from __future__ import annotations

import datetime as dt
import io
import re

try:
    from . import cn_common as C
except ImportError:
    import cn_common as C

HOST = "https://www.safe.gov.cn"
# 各檔附件標題要符合的正規式（標題＝<a> 的 title 或連結文字）
LINK_RX = {
    "bop": r"国际收支平衡表时间序列",
    "jsh": r"银行结售汇数据时间序列",
    "skk": r"银行代客涉外收付款数据时间序列",
    "debt": r"外债.*时间序列",
    "trade": r"国际收支货物和服务贸易数据",
}
SECTION = re.compile(r"^[一二三四五六七八九十]+、")


class LayoutError(RuntimeError):
    """Excel 版面和預期不同。"""


# ---------- 說明頁 ----------
def parse_links(html: str) -> list:
    """說明頁 -> [(絕對網址, 標題)]，只收 .xls／.xlsx 連結。"""
    out = []
    for m in re.finditer(r'<a\s[^>]*href="([^"]+\.xlsx?)"([^>]*)>(.*?)</a>', html, flags=re.S | re.I):
        t = re.search(r'title="([^"]*)"', m.group(2))
        title = (t.group(1) if t else "") or re.sub(r"<[^>]+>", "", m.group(3))
        href = m.group(1)
        out.append((href if href.startswith("http") else HOST + href, C.clean(title)))
    return out


def pick_link(links: list, kind: str):
    rx = re.compile(LINK_RX[kind])
    hits = [u for u, t in links if rx.search(t)]
    return hits[0] if hits else None


# ---------- Excel ----------
def read_sheet(content: bytes, url: str, sheet: str) -> list:
    want = C.clean(sheet)
    if url.lower().endswith(".xls"):
        import xlrd
        wb = xlrd.open_workbook(file_contents=content)
        for sh in wb.sheets():
            if C.clean(sh.name) == want:
                return [[(c.value if c.value != "" else None) for c in sh.row(i)] for i in range(sh.nrows)]
        raise LayoutError("Excel 裡沒有工作表「%s」（有：%s）" % (sheet, "、".join(s.name for s in wb.sheets())))
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True, read_only=True)
    for ws in wb.worksheets:
        if C.clean(ws.title) == want:
            return [list(r) for r in ws.iter_rows(values_only=True)]
    raise LayoutError("Excel 裡沒有工作表「%s」（有：%s）" % (sheet, "、".join(w.title for w in wb.worksheets)))


def _serial_month(x) -> tuple:
    d = dt.date(1899, 12, 30) + dt.timedelta(days=int(x))
    return d.year, d.month


def _shift(ym: tuple, n: int) -> tuple:
    k = ym[0] * 12 + ym[1] - 1 + n
    return k // 12, k % 12 + 1


def _iso(ym: tuple) -> str:
    return "%04d-%02d-01" % ym


def month_columns(hdr: list, col0: int) -> list:
    """表頭序號列 -> [(欄位索引, 'YYYY-MM-01')]。最後一欄的序號月份為準，往前逐月推算，並核對最後 24 欄。"""
    cols = [j for j, c in enumerate(hdr) if j >= col0 and isinstance(c, (int, float)) and not isinstance(c, bool)]
    if len(cols) < 24:
        raise LayoutError("表頭找不到足夠的月份序號欄（只有 %d 欄）" % len(cols))
    last = _serial_month(hdr[cols[-1]])
    out = [(j, _iso(_shift(last, i - (len(cols) - 1)))) for i, j in enumerate(cols)]
    for j, d in out[-24:]:
        if _iso(_serial_month(hdr[j])) != d:
            raise LayoutError("表頭月份序號不連續（%s 欄序號與推算的 %s 不同），版面可能改版" % (j, d))
    return out


def parse_monthly_section(rows: list, hdr_row: int, col0: int, sec_rx: str, lab_rx: str) -> list:
    """jsh／skk：表頭序號列 + 區段標題（一、二、三…）+ 列標籤。"""
    cols = month_columns(rows[hdr_row], col0)
    sec = None
    for r in rows[hdr_row + 1:]:
        lab = C.clean(r[0])
        if not lab:
            continue
        if SECTION.match(lab):
            sec = lab
        if re.search(sec_rx, sec or "") and re.search(lab_rx, lab):
            return [(d, x) for j, d in cols if j < len(r) and (x := C.to_float(r[j])) is not None]
    raise LayoutError("找不到區段「%s」下的列「%s」" % (sec_rx, lab_rx))


def parse_quarterly(rows: list, lab_rx: str, hdr_row: int = 3) -> list:
    """bop：表頭 '2026Q2'，取第一個符合 lab_rx 的列。"""
    cols = []
    for j, c in enumerate(rows[hdr_row]):
        m = re.match(r"^(\d{4})Q([1-4])$", str(c or "").strip())
        if m:
            cols.append((j, "%s-%02d-01" % (m.group(1), (int(m.group(2)) - 1) * 3 + 1)))
    if len(cols) < 8:
        raise LayoutError("表頭找不到季度欄（YYYYQn），只有 %d 欄" % len(cols))
    for r in rows[hdr_row + 1:]:
        if re.search(lab_rx, C.clean(r[0])):
            return [(d, x) for j, d in cols if j < len(r) and (x := C.to_float(r[j])) is not None]
    raise LayoutError("找不到列「%s」" % lab_rx)


def parse_trade(rows: list, row_idx_rx: str, occ: int = 1, hdr_row: int = 3) -> list:
    """trade：表頭是月序文字（2015.1…2026.08），從 2015-01 逐月，對最後一欄核對。"""
    hdr = rows[hdr_row]
    n = len([c for c in hdr[1:] if c not in (None, "")])
    last = str(hdr[n]).strip()
    m = re.match(r"^(\d{4})\.(\d{1,2})$", last)
    months = [_iso(_shift((2015, 1), i)) for i in range(n)]
    if not m or months[-1] != "%s-%02d-01" % (m.group(1), int(m.group(2))):
        raise LayoutError("表頭最後一欄「%s」與從 2015-01 起算的第 %d 個月（%s）不同，版面可能改版" % (last, n, months[-1]))
    k = 0
    for r in rows[hdr_row + 1:]:
        if re.search(row_idx_rx, C.clean(r[0])):
            k += 1
            if k == occ:
                return [(months[i], x) for i in range(n) if (x := C.to_float(r[1 + i])) is not None]
    raise LayoutError("找不到列「%s」" % row_idx_rx)


def parse_debt(rows: list, sec_rx: str, sheet_hdr: int = 2) -> list:
    """debt：表頭 '2026年6月末'（取季首月），部門列是沒有縮排的列。"""
    cols = []
    for j, c in enumerate(rows[sheet_hdr]):
        m = re.match(r"^(\d{4})年(\d{1,2})月末$", C.clean(c))
        if m and int(m.group(2)) in (3, 6, 9, 12):
            cols.append((j, "%s-%02d-01" % (m.group(1), int(m.group(2)) - 2)))
    if len(cols) < 8:
        raise LayoutError("表頭找不到「YYYY年M月末」欄（只有 %d 欄）" % len(cols))
    for r in rows[sheet_hdr + 1:]:
        raw = str(r[0] or "")
        if raw.strip() and not raw[:1].isspace() and re.search(sec_rx, C.clean(raw)):
            return [(d, x) for j, d in cols if j < len(r) and (x := C.to_float(r[j])) is not None]
    raise LayoutError("找不到外債部門列「%s」" % sec_rx)


def parse_spec(rows: list, kind: str, p: dict) -> list:
    if kind == "bop":
        return parse_quarterly(rows, p["lab_rx"])
    if kind in ("jsh", "skk"):
        return parse_monthly_section(rows, p["hdr_row"], p["col0"], p["sec_rx"], p["lab_rx"])
    if kind == "trade":
        return parse_trade(rows, p["row_idx_rx"], p.get("occ", 1))
    if kind == "debt":
        return parse_debt(rows, p["sec_rx"])
    raise LayoutError("不認得的 file：%s" % kind)


# ---------- 抓取 ----------
def fetch(specs: list[dict]) -> dict:
    res: dict = {}
    s = C.session()
    by_file: dict = {}
    for sp in specs:
        by_file.setdefault(sp["params"]["file"], []).append(sp)
    for kind, group in by_file.items():
        landing = group[0]["params"]["landing_page"]
        try:
            if kind not in LINK_RX:
                raise LayoutError("不認得的 file：%s" % kind)
            html = C.http_backoff(s, "GET", landing).content.decode("utf-8", "replace")
            links = parse_links(html)
            url = pick_link(links, kind)
            if not url:
                raise LayoutError("說明頁解析不到「%s」附件連結（頁面上有 %d 個 xls/xlsx 連結；外管局可能改版）" % (LINK_RX[kind], len(links)))
            content = C.http_backoff(s, "GET", url).content
        except Exception as e:  # noqa: BLE001
            for sp in group:
                res[sp["sid"]] = {"error": "外管局「%s」下載失敗：%s" % (kind, str(e)[:200])}
            continue
        sheets: dict = {}
        for sp in group:
            p = sp["params"]
            try:
                key = p.get("sheet") or "Sheet1"
                if key not in sheets:
                    sheets[key] = read_sheet(content, url, key)
                obs = parse_spec(sheets[key], kind, p)
                res[sp["sid"]] = {"obs": obs} if obs else {"error": "外管局「%s」這一列沒有數值" % kind}
            except Exception as e:  # noqa: BLE001
                res[sp["sid"]] = {"error": "外管局「%s」解析失敗：%s" % (kind, str(e)[:200])}
    return res
