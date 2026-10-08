"""新加坡統計局（SingStat）Table Builder API（免金鑰）。

網址：https://tablebuilder.singstat.gov.sg/api/table/tabledata/<table_id>?limit=5000&offset=<格數>
  limit、offset 都以「格」計（列數 × 期數），伺服器單頁上限 5000 格；列多、歷史長的表要用 offset 分頁。
  一列可能被頁界切成兩段（後一頁開頭是同一個 seriesNo 的續段），這裡依 seriesNo 接回。
  回應 Data.row[]：{seriesNo, rowText, columns:[{key:"2026 Aug"|"2026 2Q"|"2026", value:"字串"}]}。
  要帶 User-Agent（用 _http 的網站網址 UA）。
params：
  table_id   表格代碼（必填），如 "M014811"
  row        列名 rowText（必填，去空白後完全比對），如 "GDP In Chained (2015) Dollars"
  series_no  選填，列序號 seriesNo（如 "1.1"）。表內有同名列（多區塊表）時必填；
             有給時用序號找列，同時檢查該列的 rowText 等於 row（不符就報錯，防表格改版後錯位）。
  scale      選填，乘以此數後再存
  probe_url  選填（fetcher 不讀）
同名列沒給 series_no 會報錯（不猜）。缺值（空白、"-"、"na"）略過。
抓法：同一張表只抓一次、多條序列共用；先依序翻頁（最多 FULL_PAGES 頁），所有要的列都完整收到就提早停；
  還沒收到的列改用 search=<列名> 或 seriesNoORrowNo=<序號> 單獨查（各一個請求，不再翻整張表）。
  同一站請求之間隔 PAUSE 秒（>=1）。
"""
from __future__ import annotations

import json
import re
import time

try:
    from . import _http
    from . import an_common as A
except ImportError:
    import _http
    import an_common as A

BASE = "https://tablebuilder.singstat.gov.sg/api/table/tabledata/%s"
LIMIT = 5000        # 伺服器單頁上限（格）
FULL_PAGES = 4      # 整表最多先翻幾頁，之後改單列查詢
MAX_PAGES = 200     # 單一查詢的翻頁保險絲
PAUSE = 1.0
_last = [0.0]


def _pause():
    wait = PAUSE - (time.monotonic() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.monotonic()


def _page(table_id, offset, extra=None):
    _pause()
    params = {"limit": LIMIT, "offset": offset}
    params.update(extra or {})
    text = _http.get(BASE % table_id, params=params)
    d = json.loads(text)
    if d.get("StatusCode") not in (None, 200):
        raise RuntimeError("SingStat %s：%s" % (d.get("StatusCode"), d.get("Message")))
    return d["Data"]["row"]


def key_to_date(k: str) -> str | None:
    k = str(k).strip()
    m = re.match(r"^(\d{4}) ([A-Za-z]{3})$", k)
    if m:
        mon = A.month_num(m[2])
        return A.ym_date(m[1], mon) if mon else None
    m = re.match(r"^(\d{4}) ([1-4])Q$", k)
    if m:
        return A.yq_date(m[1], int(m[2]))
    if re.match(r"^\d{4}$", k):
        return "%s-01-01" % k
    return None


def parse(text: str, row: str) -> list:
    """單頁文字解析（離線測試用）：依列名找第一個同名列。"""
    d = json.loads(text)["Data"]
    for r in d["row"]:
        if r["rowText"].strip() == row:
            out = []
            for c in r["columns"]:
                dt = key_to_date(c["key"])
                if dt is not None:
                    out.append((dt, c["value"]))
            return out
    raise ValueError("表內找不到列「%s」" % row)


class Table:
    """一張表已收到的列：seriesNo -> {"text": rowText, "cols": {key: value}}，保持表內順序。"""

    def __init__(self):
        self.rows: dict = {}
        self.ended = False

    def add(self, rows):
        """加入一頁；回傳這頁的格數。"""
        n = 0
        for r in rows:
            sn = str(r.get("seriesNo", r["rowText"]))
            rec = self.rows.setdefault(sn, {"text": r["rowText"].strip(), "cols": {}})
            for c in r["columns"]:
                rec["cols"][c["key"]] = c["value"]
            n += len(r["columns"])
        return n

    def match(self, p):
        """依 params 找列；回傳 seriesNo 或 None（還沒收到）；同名多列報錯。"""
        if p.get("series_no"):
            sn = str(p["series_no"])
            rec = self.rows.get(sn)
            if rec is None:
                return None
            if rec["text"] != p["row"].strip():
                raise ValueError("序號 %s 的列名是「%s」，不是「%s」（表格改版？）" % (sn, rec["text"], p["row"]))
            return sn
        hits = [sn for sn, rec in self.rows.items() if rec["text"] == p["row"].strip()]
        if len(hits) > 1:
            raise ValueError("表內有 %d 個同名列「%s」，要在 params 加 series_no（%s）" % (len(hits), p["row"], "、".join(hits[:6])))
        return hits[0] if hits else None

    def closed(self, sn):
        """該列是否已完整：後面還有別的列，或整張表已讀完。"""
        if self.ended:
            return True
        return list(self.rows)[-1] != sn


def _walk(table_id, table, extra=None, stop=None, max_pages=MAX_PAGES):
    """從 offset=0 翻頁到沒有資料；stop(table) 為真就提早停。"""
    offset = 0
    for _ in range(max_pages):
        rows = _page(table_id, offset, extra)
        n = table.add(rows)
        if n < LIMIT:
            table.ended = True
            return
        offset += n
        if stop and stop(table):
            return


def _search_term(row):
    """search 參數對 & 等符號會回 420；取列名中最長的純字母數字片段（子字串比對，之後仍精確比對列名）。"""
    parts = re.split(r"[^A-Za-z0-9 ,'()-]+", row)
    return max(parts, key=len).strip() or row


def load(table_id, params_list):
    """抓一張表，回傳 Table（含所有 params_list 需要的列；找不到的在 match 時回 None）。"""
    t = Table()

    def done(tb):
        for p in params_list:
            try:
                sn = tb.match(p)
            except ValueError:
                return True  # 同名列錯誤：不用再翻，交給後面報錯
            if sn is None or not tb.closed(sn):
                return False
        return True

    _walk(table_id, t, stop=done, max_pages=FULL_PAGES)
    if t.ended or done(t):
        return t
    # 整表翻不完：缺的列單獨查
    for p in params_list:
        try:
            if t.match(p) is not None and t.closed(t.match(p)):
                continue
        except ValueError:
            continue
        sub = Table()
        if p.get("series_no"):
            _walk(table_id, sub, extra={"seriesNoORrowNo": str(p["series_no"])})
        else:
            _walk(table_id, sub, extra={"search": _search_term(p["row"])})
        for sn, rec in sub.rows.items():
            t.rows[sn] = rec  # 單查結果是完整的列，覆蓋可能被截斷的舊段
    t.ended = True
    return t


def fetch(specs: list[dict]) -> dict:
    by_table: dict = {}
    for s in specs:
        by_table.setdefault(s["params"]["table_id"], []).append(s["params"])
    tables: dict = {}
    errors: dict = {}
    for tid, plist in by_table.items():
        try:
            tables[tid] = load(tid, plist)
        except Exception as e:  # noqa: BLE001
            errors[tid] = "%s：%s" % (tid, e)

    def one(s):
        p = s["params"]
        tid = p["table_id"]
        if tid in errors:
            raise RuntimeError(errors[tid])
        t = tables[tid]
        sn = t.match(p)
        if sn is None:
            raise ValueError("表內找不到列「%s」" % p["row"])
        out = {}
        for k, v in t.rows[sn]["cols"].items():
            dt = key_to_date(k)
            x = A.to_float(v)
            if dt is not None and x is not None:
                out[dt] = x * float(p.get("scale", 1.0))
        return sorted(out.items())

    return A.run_specs(specs, one)
