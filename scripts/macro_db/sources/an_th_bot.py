"""泰國銀行（BOT）統計資料庫網頁匯出（BOTWEBSTAT，ASP.NET 表單，免金鑰）。

流程（一張報表三次請求）：GET 報表頁取 __VIEWSTATE → POST btnSubmit（起迄年選最早到最新）→ 再 POST imbExportText 取 CSV。
同一張報表只匯出一次，多條序列共用；同站任兩次請求至少隔 1 秒。

CSV 版面：前幾列是表名、單位、更新時間；表頭列前兩格為空，其餘格是期別（'AUG 2026 p'，新到舊）；
資料列第 1 格是列號、第 2 格是列名（前面有縮排空白）。以「列號＋列名」雙重定位，列名對不上就回 error，不猜。

params：
  report_id   報表代碼（必填），如 638
  row_no      列號（必填，整數）
  row_label   列名（必填，與 CSV 的列名比對時忽略前後與重複空白、大小寫）
  scale       選填，乘以此數後再存
  probe_url   選填（fetcher 不讀）
"""
from __future__ import annotations

import csv
import html as _html
import io
import re
import time

import requests

try:
    from . import _http
    from . import an_common as A
except ImportError:
    import _http
    import an_common as A

BASE = "https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?reportID=%s&language=ENG"
GAP = 1.1          # 同站請求最小間隔（秒）
_last = [0.0]
MON = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def _wait():
    d = GAP - (time.time() - _last[0])
    if d > 0:
        time.sleep(d)
    _last[0] = time.time()


def _req(sess, method, url, data=None, tries=3):
    last = None
    for i in range(tries):
        _wait()
        try:
            r = sess.post(url, data=data, timeout=120) if method == "POST" else sess.get(url, timeout=60)
            if r.status_code == 200:
                return r.content.decode("utf-8-sig", "replace")
            last = RuntimeError("HTTP %s" % r.status_code)
            if r.status_code not in (429, 500, 502, 503, 504):
                break
        except requests.RequestException as e:
            last = e
        time.sleep(5 * (i + 1))        # 退避
    raise RuntimeError("%s：%s" % (url[:80], last))


def hidden_fields(h: str) -> dict:
    return {m.group(1): _html.unescape(m.group(2))
            for m in re.finditer(r'<input type="hidden" name="(\w+)" id="\w+" value="([^"]*)"', h)}


def select_options(h: str, name: str) -> list:
    """回傳 [(是否 selected, value)]；找不到下拉選單回 []。"""
    m = re.search(r'<select name="%s".*?</select>' % re.escape(name), h, re.S)
    if not m:
        return []
    return [(bool(sel), v) for sel, v in re.findall(r'<option( selected="selected")? value="([^"]*)"', m.group(0))]


def _selected(h, name):
    o = [v for s, v in select_options(h, name) if s]
    return o[0] if o else ""


def _form_range(h: str) -> dict:
    """依頁面下拉選單組出「最早年～最新」的表單欄位；缺必要欄位時丟 ValueError。"""
    d = hidden_fields(h)
    if "__VIEWSTATE" not in d:
        raise ValueError("找不到 __VIEWSTATE（表單改版？）")
    years = [v for _, v in select_options(h, "drpFromYear") if v]
    to_years = [v for _, v in select_options(h, "drpToYear") if v]
    if not years or not to_years:
        raise ValueError("找不到起迄年下拉選單")
    d["drpPeriod"] = _selected(h, "drpPeriod")
    d["drpFromYear"] = years[0]
    d["drpToYear"] = to_years[-1]
    if select_options(h, "drpFromMonth"):
        d["drpFromMonth"] = [v for _, v in select_options(h, "drpFromMonth") if v][0]
        d["drpToMonth"] = _selected(h, "drpToMonth")
    return d


def period_date(label: str) -> str | None:
    """'AUG 2026 p' -> '2026-08-01'；不是月期別回 None。"""
    m = re.match(r"\s*([A-Za-z]{3})\s+(\d{4})", str(label))
    if not m or m.group(1).upper() not in MON:
        return None
    return A.ym_date(m.group(2), MON[m.group(1).upper()])


def parse_csv(text: str):
    """回傳 (rows, header_index, meta)。找不到表頭列就丟 ValueError。"""
    rows = list(csv.reader(io.StringIO(text)))
    hi = next((i for i, r in enumerate(rows) if i >= 3 and len(r) > 3 and r[0] == "" and r[1] == ""), None)
    if hi is None:
        raise ValueError("匯出內容不是預期的 CSV 表格")
    meta = {}
    for r in rows[:hi]:
        if r and r[0].startswith("Last Updated"):
            meta["updated"] = r[0].split(":", 1)[1].strip()
    return rows, hi, meta


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def extract(rows, hi, row_no: int, row_label: str, scale: float = 1.0) -> list:
    head = rows[hi]
    for r in rows[hi + 1:]:
        if r and r[0].strip() == str(row_no):
            if _norm(r[1]) != _norm(row_label):
                raise ValueError("列 %s 的名稱是「%s」，與預期「%s」不符" % (row_no, r[1].strip(), row_label))
            pairs = []
            for j in range(2, min(len(head), len(r))):
                d = period_date(head[j])
                if d:
                    pairs.append((d, r[j]))
            return A.clean_obs(pairs, scale)
    raise ValueError("找不到列號 %s" % row_no)


def export_report(sess, rid) -> str:
    url = BASE % rid
    h = _req(sess, "GET", url)
    d = _form_range(h)
    d["btnSubmit"] = "Submit"
    h2 = _req(sess, "POST", url, d)
    d2 = hidden_fields(h2)
    if "__VIEWSTATE" not in d2:
        raise ValueError("送出查詢後找不到 __VIEWSTATE")
    for k in ("drpPeriod", "drpFromMonth", "drpFromYear", "drpToMonth", "drpToYear"):
        if k in h2:
            d2[k] = _selected(h2, k)
    d2["imbExportText.x"] = "5"
    d2["imbExportText.y"] = "5"
    t = _req(sess, "POST", url, d2)
    if t.lstrip().startswith("<"):
        raise ValueError("匯出回傳的是網頁而不是 CSV")
    return t


def fetch(specs: list[dict]) -> dict:
    sess = requests.Session()
    sess.headers["User-Agent"] = _http.NAMED_UA
    by_report: dict = {}
    for s in specs:
        by_report.setdefault(str(s["params"]["report_id"]), []).append(s)
    res: dict = {}
    for rid, group in by_report.items():
        try:
            rows, hi, _meta = parse_csv(export_report(sess, rid))
        except Exception as e:  # noqa: BLE001
            for s in group:
                res[s["sid"]] = {"error": "報表 %s：%s" % (rid, str(e)[:160])}
            continue
        for s in group:
            p = s["params"]
            try:
                obs = extract(rows, hi, int(p["row_no"]), p["row_label"], float(p.get("scale", 1.0)))
                res[s["sid"]] = {"obs": obs} if obs else {"error": "解析後沒有任何觀測值"}
            except Exception as e:  # noqa: BLE001
                res[s["sid"]] = {"error": "報表 %s：%s" % (rid, str(e)[:160])}
    return res
