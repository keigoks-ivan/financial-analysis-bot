"""國家統計局每月「70 個大中城市商品住宅銷售價格變動情況」（www.stats.gov.cn 數據發布／最新發布）。

國家數據平台沒有這張表，只能讀統計局網站的月度發布頁：
  1. 列表頁 /sj/zxfb/index.html、index_1.html… 找標題「X年X月份70个大中城市商品住宅销售价格变动情況」的連結
  2. 內頁第 1 張表＝新建商品住宅、第 2 張表＝二手住宅；每列兩組欄位各 35 城（城市／環比／同比），指數皆為「＝100」
每個內頁約 1.4–2.2 MB，統計局回應慢（單頁 45–85 秒），所以：
  - 平常只看列表第 1 頁，只抓「store 還沒有」的最新 2 期（每月通常只多 1 頁）；沒有新一期就不抓內頁、直接回傳 store 現有資料
  - 回補模式 MACRO_DB_BACKFILL=1：列表翻頁到底，抓回最近 60 期（3 條並行，同站請求仍間隔 ≥ 1 秒）。
    可另設 MACRO_DB_HP70_CACHE=<目錄> 把每期解析結果存成 JSON，中斷後重跑只補沒抓到的期別。
    統計局網站的列表只留到 2021 年 10 月那一期之後，更早的期別抓不到。

params：
  kind      "new"（新建商品住宅）或 "used"（二手住宅）
  metric    "mom"（環比，上月＝100）或 "yoy"（同比，上年同月＝100）
  city      單一城市（簡體，例「广州」）；與 stat 擇一
  stat      "up"／"down"：該期 70 城裡環比 > 100／< 100 的城市數（本站自行統計，非統計局公布值）
  offset    選填，加在每個值上（環比序列用 -100，直接存成漲跌幅 %）
  index_url 列表頁網址（CI probe 用）
回應結構改版（找不到標題、找不到表格或欄位）時整批回 error 並寫明原因，不會靜默回空。
"""
from __future__ import annotations

import html as _html
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from . import cn_common as C
    from .. import store
except ImportError:  # 直接以腳本方式載入時
    import cn_common as C
    import store

BASE = "https://www.stats.gov.cn/sj/zxfb/"
TITLE_RX = re.compile(r"^(\d{4})年(\d{1,2})月份70个大中城市商品住宅销售价格变动情况$")
RECENT = 2            # 平常最多補抓幾期
BACKFILL_N = 60       # 回補抓回幾期
PAGE_TIMEOUT = 240
WORKERS = 3
EXPECT_CITIES = 60    # 一張表至少要解析出幾個城市，否則視為結構改變


class Restructured(RuntimeError):
    """頁面結構與預期不同（改版）。"""


# ---------- 解析 ----------
def parse_list(html: str) -> dict:
    """列表頁 -> {'YYYY-MM': 絕對網址}。同一篇在頁面上會出現多次（桌機／手機版、被截短的標題），以完整標題比對。"""
    out = {}
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>\s*([^<]{4,80}?)\s*</a>', html):
        t = TITLE_RX.match(_html.unescape(m.group(2)).strip())
        if t:
            href = m.group(1)
            url = href if href.startswith("http") else BASE + href.lstrip("./")
            out.setdefault("%s-%02d" % (t.group(1), int(t.group(2))), url)
    return out


def _cells(table: str) -> list:
    rows = []
    for tr in re.findall(r"<tr.*?</tr>", table, flags=re.S):
        rows.append([re.sub(r"\s+", "", _html.unescape(re.sub(r"<[^>]+>", "", c)))
                     for c in re.findall(r"<t[dh].*?</t[dh]>", tr, flags=re.S)])
    return rows


def parse_page(html: str) -> dict:
    """內頁 -> {('new'|'used', 城市簡體名): (環比, 同比)}。表格結構不符就丟 Restructured。"""
    tabs = re.findall(r"<table.*?</table>", html, flags=re.S)
    if len(tabs) < 2:
        raise Restructured("內頁找不到兩張價格表（只有 %d 張表）" % len(tabs))
    out: dict = {}
    for key, ti in (("new", 0), ("used", 1)):
        rows = _cells(tabs[ti])
        hdr = next((r for r in rows[:3] if "城市" in r and "环比" in r and "同比" in r), None)
        if hdr is None:
            raise Restructured("第 %d 張表的表頭不是 城市／环比／同比" % (ti + 1))
        starts = [i for i, c in enumerate(hdr) if c == "城市"]
        ncol = starts[1] if len(starts) > 1 else len(hdr)
        i_mom, i_yoy = hdr.index("环比"), hdr.index("同比")
        n = 0
        for r in rows:
            for off in starts or [0]:
                if len(r) <= off + max(i_mom, i_yoy) or r[off] == "城市":
                    continue
                mom, yoy = C.to_float(r[off + i_mom]), C.to_float(r[off + i_yoy])
                if r[off] and mom is not None and yoy is not None:
                    out[(key, r[off])] = (mom, yoy)
                    n += 1
        if n < EXPECT_CITIES:
            raise Restructured("第 %d 張表只解析到 %d 個城市（應有約 70）" % (ti + 1, n))
    return out


# ---------- 取值 ----------
def values_for(p: dict, pages: dict) -> list:
    """pages：{'YYYY-MM': {(kind, city): (mom, yoy)}} -> [(日期, 值)]。"""
    idx = 0 if p["metric"] == "mom" else 1
    off = float(p.get("offset", 0))
    out = []
    for ym in sorted(pages):
        rows = {c: v for (k, c), v in pages[ym].items() if k == p["kind"]}
        if "stat" in p:
            vs = [v[idx] for v in rows.values()]
            if p["stat"] == "up":
                x = float(sum(1 for v in vs if v > 100))
            elif p["stat"] == "down":
                x = float(sum(1 for v in vs if v < 100))
            else:
                raise ValueError("不認得的 stat：%s" % p["stat"])
        else:
            if p["city"] not in rows:
                continue
            x = rows[p["city"]][idx] + off
        out.append(("%s-01" % ym, round(x, 6)))
    return out


# ---------- 抓取 ----------
def _get_html(s, url: str) -> str:
    return C.http_backoff(s, "GET", url, timeout=PAGE_TIMEOUT).content.decode("utf-8", "replace")


def collect_periods(s, backfill: bool) -> dict:
    """翻列表頁，回傳 {ym: url}。平常只看第 1 頁；回補翻到底（或已湊滿 BACKFILL_N 期）。"""
    found: dict = {}
    page = 0
    while True:
        url = BASE + ("index.html" if page == 0 else "index_%d.html" % page)
        try:
            found.update({k: v for k, v in parse_list(_get_html(s, url)).items() if k not in found})
        except RuntimeError as e:
            if page == 0 or "HTTP 404" not in str(e):
                raise
            break
        page += 1
        if not backfill or len(found) >= BACKFILL_N or page > 120:
            break
    return found


def _cache_path(ym: str):
    d = os.environ.get("MACRO_DB_HP70_CACHE")
    return Path(d) / ("hp70_%s.json" % ym) if d else None


def _load_cache(ym: str):
    p = _cache_path(ym)
    if p and p.exists():
        raw = json.loads(p.read_text(encoding="utf-8"))
        return {tuple(k.split("|", 1)): tuple(v) for k, v in raw.items()}
    return None


def _save_cache(ym: str, page: dict):
    p = _cache_path(ym)
    if p:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"%s|%s" % k: list(v) for k, v in page.items()}, ensure_ascii=False), encoding="utf-8")


def _fetch_page(ym_url):
    ym, url = ym_url
    cached = _load_cache(ym)
    if cached is not None:
        return ym, cached, None
    err = None
    for i in range(3):      # 並行下載時偶爾收到沒有表格的殘缺頁面（HTTP 200），重抓一次通常就好
        try:
            page = parse_page(_get_html(C.session(), url))
            _save_cache(ym, page)
            return ym, page, None
        except Exception as e:  # noqa: BLE001
            err = str(e)[:160]
            if i < 2:
                time.sleep(5)
    return ym, None, err


def fetch(specs: list[dict]) -> dict:
    if not specs:
        return {}
    backfill = C.backfill_mode()
    try:
        listing = collect_periods(C.session(), backfill)
        if not listing:
            raise Restructured("列表頁找不到任何「70个大中城市商品住宅销售价格变动情况」標題（頁面可能改版）")
    except Exception as e:  # noqa: BLE001
        return {sp["sid"]: {"error": "70 城房價列表頁失敗：%s" % str(e)[:160]} for sp in specs}
    periods = sorted(listing, reverse=True)[:BACKFILL_N if backfill else RECENT]
    stored = {sp["sid"]: dict(store.read(sp["sid"])) for sp in specs}
    todo = [ym for ym in periods if any(("%s-01" % ym) not in stored[sp["sid"]] for sp in specs)]
    pages: dict = {}
    failed: list = []
    jobs = [(ym, listing[ym]) for ym in todo]
    if backfill and len(jobs) > 1:
        with ThreadPoolExecutor(WORKERS) as ex:
            results = list(ex.map(_fetch_page, jobs))
    else:
        results = [_fetch_page(j) for j in jobs]
    for ym, page, err in results:
        if err:
            failed.append("%s：%s" % (ym, err))
        else:
            pages[ym] = page
    if failed:
        print("cn_nbs_hp70 失敗期別：" + "；".join(failed), file=sys.stderr)
    if any(f.split("：")[0] == periods[0] for f in failed):
        # 最新一期失敗：不要讓頁面看起來是正常的，整批標 error（store 的舊資料不受影響）
        return {sp["sid"]: {"error": "70 城房價最新一期（%s）抓取失敗：%s" % (periods[0], failed[0])} for sp in specs}
    if failed and not pages:
        return {sp["sid"]: {"error": "70 城房價內頁全部失敗（" + failed[0] + "）"} for sp in specs}
    res = {}
    for sp in specs:
        try:
            new = values_for(sp["params"], pages)
        except Exception as e:  # noqa: BLE001
            res[sp["sid"]] = {"error": "70 城房價取值失敗：%s" % str(e)[:120]}
            continue
        merged = dict(stored[sp["sid"]])
        merged.update(dict(new))
        res[sp["sid"]] = {"obs": sorted(merged.items())} if merged else {
            "error": "70 城房價沒有「%s」的資料" % (sp["params"].get("city") or sp["params"].get("stat"))}
    return res
