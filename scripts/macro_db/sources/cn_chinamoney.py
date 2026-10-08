"""中國外匯交易中心暨全國銀行間同業拆借中心（www.chinamoney.com.cn）：LPR、SHIBOR、人民幣匯率中間價。

三支 API 都限制「一次查詢區間最多一年」：本地沒有歷史時依 since 往回一年一年切片，之後只抓最近約 4 個月。
LPR 的歷史查詢不可帶 pageNum／pageSize；中間價要分頁（pageSize 最大 50，更大會被擋）。

params：
  kind    "lpr"（tenor: "1Y"|"5Y"）、"shibor"（tenor: "ON"|"1W"|"1M"|"3M"|"6M"|"1Y"…）、"ccpr"（currency: "USD/CNY"）
  tenor／currency  見上
  probe_url 完整網址（CI probe 用）
LPR 只收 2019-08-20 新機制之後的報價，日期記為當月 1 日。
"""
from __future__ import annotations

import datetime as dt

try:
    from . import cn_common as C
except ImportError:
    import cn_common as C

B = "https://www.chinamoney.com.cn/ags/ms"
SINCE = {"lpr": "2019-08-20", "shibor": "2006-10-08", "ccpr": "2005-07-21"}
RECENT_DAYS = 120


def windows(start: str, end: dt.date):
    """由新到舊的 ≤ 360 天區間 [(a, b)]，涵蓋 start～end。"""
    s0 = dt.date.fromisoformat(start)
    out, b = [], end
    while b >= s0:
        a = max(s0, b - dt.timedelta(days=359))
        out.append((a.isoformat(), b.isoformat()))
        b = a - dt.timedelta(days=1)
    return out


def parse_lpr(j: dict, tenor: str) -> list:
    out = []
    for r in j.get("records", []):
        d, v = r.get("showDateCN"), C.to_float(r.get(tenor))
        if d and v is not None and d >= SINCE["lpr"]:
            out.append((d[:7] + "-01", v))
    return out


def parse_shibor(j: dict, tenor: str) -> list:
    out = []
    for r in j.get("records", []):
        d, v = r.get("showDateCN"), C.to_float(r.get(tenor))
        if d and v is not None:
            out.append((d, v))
    return out


def parse_ccpr(j: dict) -> list:
    out = []
    for r in j.get("records", []):
        vals = r.get("values") or []
        v = C.to_float(vals[0]) if vals else None
        if r.get("date") and v is not None:
            out.append((r["date"], v))
    return out


def fetch(specs: list[dict]) -> dict:
    res: dict = {}
    s = C.session()
    today = C.today()
    cache: dict = {}

    def get(url):
        if url not in cache:
            cache[url] = C.http_json(s, "GET", url)
        return cache[url]

    # 同種資料（kind＋currency）合併成一次切片查詢，各 tenor 共用
    groups: dict = {}
    for sp in specs:
        p = sp["params"]
        groups.setdefault((p["kind"], p.get("currency", "")), []).append(sp)
    for (kind, cur), sps in groups.items():
        backfill = any(C.need_backfill(sp["sid"], int(SINCE[kind][:4])) for sp in sps)
        start = SINCE[kind] if backfill else (today - dt.timedelta(days=RECENT_DAYS)).isoformat()
        pages: list = []   # 每個視窗的 json（ccpr 為多頁合併後的 records）
        err = None
        try:
            for a, b in windows(start, today):
                if kind == "lpr":
                    pages.append(get("%s/cm-u-bk-currency/LprHis?lang=CN&strStartDate=%s&strEndDate=%s" % (B, a, b)))
                elif kind == "shibor":
                    pages.append(get("%s/cm-u-bk-shibor/ShiborHis?lang=cn&startDate=%s&endDate=%s" % (B, a, b)))
                else:
                    recs, n = [], 1
                    while True:
                        j = get("%s/cm-u-bk-ccpr/CcprHisNew?startDate=%s&endDate=%s&currency=%s&pageNum=%d&pageSize=50"
                                % (B, a, b, cur, n))
                        recs += j.get("records", [])
                        if n >= int((j.get("data") or {}).get("pageTotal") or 1):
                            break
                        n += 1
                    pages.append({"records": recs})
        except Exception as e:  # noqa: BLE001
            err = "外匯交易中心抓取失敗：%s" % str(e)[:150]
        for sp in sps:
            if err:
                res[sp["sid"]] = {"error": err}
                continue
            p = sp["params"]
            obs = {}
            for pg in pages:
                rows = (parse_lpr(pg, p["tenor"]) if kind == "lpr" else
                        parse_shibor(pg, p["tenor"]) if kind == "shibor" else parse_ccpr(pg))
                obs.update(rows)
            res[sp["sid"]] = {"obs": sorted(obs.items())} if obs else {"error": "沒有解析到數值"}
    return res
