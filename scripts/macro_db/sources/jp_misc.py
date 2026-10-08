"""其他單一來源：日本政府觀光局（JNTO）訪日外客數、國土交通省不動產價格指數。

kind=jnto  統計頁（visitors-statistics）上的 Excel（檔名含公布日，每月換）：先抓頁面解析連結。
           每個工作表是一年（名稱 2026、2025…），「総数」列的奇數月欄為人數、偶數欄為伸率。
           params: page（頁面網址）, row（列名，預設 総数）
kind=mlit  不動產價格指數（住宅）Excel（檔名是 CMS 序號，每次發布換）：先抓統計頁，取緊接在
           「不動産価格指数（住宅）」文字之後的 .xlsx 連結。params: page, sheet, col（0 起算）, col_check
           選填 anchor：改取緊接在該標題文字（例如「不動産価格指数（商業用不動産）」）之後的連結；
           選填 quarterly：true 時資料為季資料，第 0、1 欄是「年、季別（1～4）」而不是日期。
"""
from __future__ import annotations

import datetime as dt
import re

from ._http import get
from .jp_common import (Cache, check_header, compact, d_month, find_link, month_of, num, run_specs,
                        sheets_any, xlsx_sheets)

JNTO_PAGE = "https://www.jnto.go.jp/statistics/data/visitors-statistics/"
MLIT_PAGE = "https://www.mlit.go.jp/totikensangyo/totikensangyo_tk5_000085.html"


def jnto_obs(sheets: dict, row_name: str = "総数") -> list:
    out = []
    for name, rows in sheets.items():
        if not re.match(r"^\d{4}$", name.strip()):
            continue
        year = int(name)
        hdr = next((r for r in rows[:8] if sum(1 for c in r if month_of(c)) >= 6), None)
        data = next((r for r in rows if r and compact(r[0]) == compact(row_name)), None)
        if hdr is None or data is None:
            continue
        for c, h in enumerate(hdr):
            m = month_of(h)
            if m and c < len(data):
                v = num(data[c])
                if v is not None:
                    out.append((d_month(year, m), v))
    return out


def fetch_jnto(specs):
    cache = Cache()
    html = get(JNTO_PAGE)
    url = find_link(html, r"/statistics/data/_files/[^\"]*\.xlsx", JNTO_PAGE)

    def one(s):
        sheets = xlsx_sheets(cache.get_url(url))
        return jnto_obs(sheets, s["params"].get("row", "総数"))
    return run_specs(specs, one)


def mlit_link(html: str) -> str:
    """統計頁 -> 住宅指數 Excel 連結：取緊接在「不動産価格指数（住宅）」之後第一個 .xlsx。"""
    from urllib.parse import urljoin
    for m in re.finditer(r'href="([^"]+\.xlsx)"', html):
        seg = html[max(0, m.start() - 400):m.start()]
        seg = seg[:seg.rfind("<a")] if "<a" in seg else seg      # 去掉 href 所在的 <a 標籤本身
        before = re.sub(r"<[^>]+>|\s+", "", seg)
        if before.endswith("不動産価格指数（住宅）") or before.endswith("不動産価格指数(住宅)"):
            return urljoin(MLIT_PAGE, m.group(1))
    raise ValueError("統計頁找不到「不動産価格指数（住宅）」的 Excel 連結")


def mlit_obs(rows, col, col_check=None, what="") -> list:
    if col_check:
        check_header(rows, col, range(4, 9), col_check, what)
    out = []
    for r in rows[9:]:
        if len(r) > col and isinstance(r[0], (dt.datetime, dt.date)):
            v = num(r[col])
            if v is not None:
                out.append((d_month(r[0].year, r[0].month), v))
    return out


def mlit_link_anchor(html: str, anchor: str) -> str:
    """統計頁 -> 緊接在 anchor 標題文字之後的第一個 .xlsx 連結。"""
    from urllib.parse import urljoin
    want = compact(anchor)
    for m in re.finditer(r'href="([^"]+\.xlsx)"', html):
        seg = html[max(0, m.start() - 400):m.start()]
        seg = seg[:seg.rfind("<a")] if "<a" in seg else seg
        before = re.sub(r"<[^>]+>|\s+", "", seg)
        if compact(before).endswith(want):
            return urljoin(MLIT_PAGE, m.group(1))
    raise ValueError("統計頁找不到「%s」的 Excel 連結" % anchor)


def mlit_q_obs(rows, col, col_check=None, what="") -> list:
    """季資料：第 0 欄＝年、第 1 欄＝季別（1～4）。"""
    if col_check:
        check_header(rows, col, range(3, 8), col_check, what)
    out = []
    for r in rows:
        if (len(r) > col and isinstance(r[0], (int, float)) and isinstance(r[1], (int, float))
                and 1 <= r[1] <= 4):
            v = num(r[col])
            if v is not None:
                out.append((d_month(int(r[0]), int((r[1] - 1) * 3 + 1)), v))
    return out


def fetch_mlit(specs):
    cache = Cache()
    html = get(MLIT_PAGE, binary=True).decode("utf-8", "replace")
    urls: dict = {}

    def one(s):
        p = s["params"]
        key = p.get("anchor")
        if key not in urls:
            urls[key] = mlit_link_anchor(html, key) if key else mlit_link(html)
        sheets = xlsx_sheets(cache.get_url(urls[key]))
        name = next((n for n in sheets if n.startswith(p["sheet"])), None)
        if name is None:
            raise ValueError("找不到工作表 %s*" % p["sheet"])
        fn = mlit_q_obs if p.get("quarterly") else mlit_obs
        return fn(sheets[name], p["col"], p.get("col_check"), s["sid"])
    return run_specs(specs, one)


def fetch(specs):
    groups: dict = {}
    for s in specs:
        groups.setdefault(s["params"].get("kind"), []).append(s)
    fns = {"jnto": fetch_jnto, "mlit": fetch_mlit}
    res = {}
    for kind, group in groups.items():
        try:
            res.update(fns[kind](group))
        except Exception as e:  # noqa: BLE001
            for s in group:
                res[s["sid"]] = {"error": ("%s：%s" % (type(e).__name__, e))[:300]}
    return res
