#!/usr/bin/env python3
"""primary_docs 台股來源：公開資訊觀測站重大訊息、年報／財報主要客戶表、公平會處分書、證交所 ESG 開放資料。

四個來源函式 src_* 各自獨立；任一個失敗只丟 FetchError／回 note，由 primary_docs.collect 記進 manifest、
不擋 DD。零 LLM。端點與版型為 2026-10-20 實測（新版 MOPS 連打約 17 次會 TLS reset，故每個來源
獨立 Session、請求間隔 ≥1 秒、失敗換新連線重試）。
"""
from __future__ import annotations

import datetime as _dt
import html as _html
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from primary_common import FetchError, clip_to_weight, mk_item, one_line, squash, weight

MOPS_API = "https://mops.twse.com.tw/mops/api/"
MOPS_PAGE = "https://mops.twse.com.tw/mops/#/web/t05st01?companyId={code}"
MOPS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Content-Type": "application/json",
    "Origin": "https://mops.twse.com.tw",
    "Referer": "https://mops.twse.com.tw/mops/",
}
DOC_BASE = "https://doc.twse.com.tw/server-java/t57sb01"
DOC_LIST_URL = DOC_BASE + "?step=1&colorchg=1&co_id={code}&year={year}&seamon=&mtype={mtype}&dtype="
FTC_URL = "https://www.ftc.gov.tw/internet/main/decision/decisionList.aspx?mid=11"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
TWSE_BASIC = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
TPEX_BASIC = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
TWSE_ANTI = "https://openapi.twse.com.tw/v1/opendata/t187ap46_L_20"
TPEX_ANTI = "https://www.tpex.org.tw/openapi/v1/t187ap46_O_20"
CACHE_DAYS = 7  # 公司基本資料／ESG 開放資料整份快取天數

# 重大訊息標題關鍵字（規格十二個，後段是同義補充）；severity 決定先抓哪幾則全文（4 最高）
KEYWORDS = [
    ("併購", 3), ("合併", 3), ("收購", 3), ("處分", 2), ("訴訟", 4), ("仲裁", 4), ("停工", 4), ("工安", 4),
    ("裁罰", 4), ("重編", 4), ("異常", 2), ("更正", 1),
    ("罰鍰", 4), ("罰款", 4), ("職災", 4), ("火災", 4), ("公平會", 4), ("公平交易", 4), ("反托拉斯", 4),
]
# 「合併財務報告」是每季例行公告，不是併購；比對關鍵字前先拿掉
_ROUTINE_MERGE_RE = re.compile(r"合併(?:及個體)?(?:財務)?(?:報告|報表|財報|營收|損益|資產負債|綜合損益)|個別及合併|合併財務")
ANTITRUST_RE = re.compile(r"公平會|公平交易|反托拉斯|裁罰|罰鍰|罰款|結合申報")
MAX_DETAIL = 8          # 重大訊息全文最多抓幾則（severity≥3 優先）
MAX_DETAIL_SEV2 = 3     # 「處分」「異常」這類中等級只補到幾則（同標題只取最新一則）
HITS_BUDGET = 900       # 命中清單那一則的單位上限


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------

def roc_to_iso(s):
    """'115/01/14'、'1150114'、'115/05/08 15:40:55' → '2026-01-14'；解析不了回 None。"""
    s = (s or "").strip()
    m = re.match(r"(\d{2,3})[/\-.]?(\d{2})[/\-.]?(\d{2})", s)
    if not m:
        return None
    try:
        return _dt.date(int(m.group(1)) + 1911, int(m.group(2)), int(m.group(3))).isoformat()
    except ValueError:
        return None


def _roc_year(d):
    return d.year - 1911


def _norm_name(name):
    """正式全名去掉『股份有限公司』，當公平會全文搜尋關鍵字（處分書常寫簡稱式全名）。"""
    n = (name or "").strip()
    n = re.sub(r"(股份)?有限公司$", "", n)
    return n.strip()


def tag_keywords(title):
    t = _ROUTINE_MERGE_RE.sub("", one_line(title))
    tags = []
    for kw, _sev in KEYWORDS:
        if kw in t and kw not in tags:
            tags.append(kw)
    return tags


def _severity(tags):
    sev = dict(KEYWORDS)
    return max([sev[t] for t in tags] or [0])


# ---------------------------------------------------------------------------
# 公司基本資料（正式全名、上市／上櫃）
# ---------------------------------------------------------------------------

def _cached_json(http, url, cache_path, headers=None):
    cache_path = Path(cache_path)
    if cache_path.exists() and (time.time() - cache_path.stat().st_mtime) < CACHE_DAYS * 86400:
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    r = http.get(url, headers=headers or {"Accept": "application/json", **UA})
    if r.status_code != 200:
        raise FetchError("HTTP {0} {1}".format(r.status_code, url))
    try:
        data = r.json()
    except ValueError as e:
        raise FetchError("非 JSON：{0}".format(url)) from e
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return data


def _row_code(row):
    return str(row.get("公司代號") or row.get("SecuritiesCompanyCode") or row.get("Code") or "").strip()


def src_company(ctx):
    """查正式全名與市場別。先照代號尾碼（.TW 上市／.TWO 上櫃）查對應名冊，查不到再查另一邊。"""
    order = [("sii", "L", TWSE_BASIC), ("otc", "O", TPEX_BASIC)]
    if ctx.suffix == "TWO":
        order.reverse()
    last_err = None
    for kind, tag, url in order:
        try:
            data = _cached_json(ctx.http_open, url, ctx.global_cache / "tw_basic_{0}.json".format(tag))
        except FetchError as e:
            last_err = e
            continue
        for row in data:
            if _row_code(row) == ctx.code:
                full = (row.get("公司名稱") or row.get("CompanyName") or "").strip()
                abbr = (row.get("公司簡稱") or row.get("CompanyAbbreviation") or "").strip()
                return {"meta": {"full_name": full, "abbr": abbr, "market": kind}}
    if last_err:
        raise last_err
    raise FetchError("證交所／櫃買中心基本資料查無代號 {0}".format(ctx.code))


# ---------------------------------------------------------------------------
# MOPS 重大訊息
# ---------------------------------------------------------------------------

def _mops_post(http, name, body):
    r = http.post(MOPS_API + name, json=body, headers=MOPS_HEADERS)
    try:
        data = r.json()
    except ValueError as e:
        raise FetchError("MOPS {0} 回傳非 JSON（HTTP {1}）".format(name, r.status_code)) from e
    if data.get("code") != 200:
        raise FetchError("MOPS {0} code={1} {2}".format(name, data.get("code"), data.get("message")))
    return data.get("result") or {}


def fetch_mops_rows(http, code, date):
    """近 12 個月（含今年與去年兩個民國年）的重大訊息列：[(iso日期, 時間, 標題, detail參數)]。"""
    start = date - _dt.timedelta(days=365)
    years = sorted({_roc_year(date), _roc_year(start)}, reverse=True)
    rows, errs = [], []
    for y in years:
        try:
            res = _mops_post(http, "t05st01", {"companyId": code, "year": str(y), "month": "all",
                                               "firstDay": "", "lastDay": ""})
        except FetchError as e:
            errs.append(str(e))
            continue
        for r in res.get("data") or []:
            iso = roc_to_iso(r[2])
            if not iso or not (start.isoformat() <= iso <= date.isoformat()):
                continue
            params = (r[5] or {}).get("parameters") if len(r) > 5 and isinstance(r[5], dict) else None
            rows.append({"date": iso, "time": r[3], "title": one_line(r[4]), "params": params})
    if not rows and errs:
        raise FetchError("；".join(errs))
    rows.sort(key=lambda x: (x["date"], x["time"] or ""), reverse=True)
    return rows, errs


def fetch_mops_detail(http, params):
    res = _mops_post(http, "t05st01_detail", params)
    data = res.get("data") or []
    if not data:
        return None
    row = data[0]
    # 欄位：序號、發言日期、發言時間、發言人、職稱、電話、主旨、符合條款、事實發生日、說明
    return {"subject": one_line(row[6]) if len(row) > 6 else "", "clause": one_line(row[7]) if len(row) > 7 else "",
            "body": squash(row[9]) if len(row) > 9 else ""}


def build_mops_items(code, rows, details, date, detail_order=None):
    """重大訊息 → major_events／regulatory_antitrust 的 item。details＝{(date,title): 全文}；
    detail_order＝全文呈現順序（severity 高到低）。"""
    url = MOPS_PAGE.format(code=code)
    d0 = (date - _dt.timedelta(days=365)).isoformat()
    kws = "、".join(k for k, _s in KEYWORDS[:12])
    hits = [r for r in rows if tag_keywords(r["title"])]
    rest = [r for r in rows if not tag_keywords(r["title"])]
    head = ("【程式統計】公開資訊觀測站「歷史重大訊息」（t05st01），{0} 至 {1} 共 {2} 則；"
            "標題含關鍵字（{3}等）者 {4} 則，未含者 {5} 則。").format(d0, date.isoformat(), len(rows), kws, len(hits), len(rest))
    if hits:
        # 命中太多時依 severity、日期留最重要的幾則，顯示仍依日期新到舊
        fmt = lambda r: "{0}［{1}］{2}".format(r["date"], "、".join(tag_keywords(r["title"])), r["title"][:70])
        keep, used = [], weight(head)
        for r in sorted(hits, key=lambda r: (-_severity(tag_keywords(r["title"])), -int(r["date"].replace("-", "")))):
            w = weight(fmt(r))
            if used + w > HITS_BUDGET:
                continue
            keep.append(r)
            used += w
        keep.sort(key=lambda r: r["date"], reverse=True)
        lines = [head, "標題含關鍵字者（日期［命中關鍵字］標題）" + ("；另 {0} 則較不重要者從略".format(len(hits) - len(keep)) if len(keep) < len(hits) else "") + "："]
        lines += [fmt(r) for r in keep]
    else:
        lines = [head + "近 12 個月沒有任何標題含上述關鍵字。"]
    items = [mk_item("公開資訊觀測站", "歷史重大訊息清單（近12個月）", url, date.isoformat(),
                     "重大訊息標題清單", "\n".join(lines))]
    order = detail_order or [(r["date"], r["title"]) for r in hits]
    for key in order:
        det = details.get(key)
        if not det:
            continue
        r_date, r_title = key
        body = "主旨：{0}\n符合條款：{1}\n說明：\n{2}".format(det["subject"], det["clause"], det["body"])
        items.append(mk_item("公開資訊觀測站", "重大訊息全文：" + r_title[:40], url, r_date,
                             "重大訊息全文（{0}）".format("、".join(tag_keywords(r_title))), clip_to_weight(body, 300)))
    if rest:
        omitted = 0
        out = []
        used = 0
        for r in rest:
            ln = "{0} {1}".format(r["date"], r["title"][:40])
            w = weight(ln)
            if used + w > 650:
                omitted += 1
                continue
            out.append(ln)
            used += w
        head2 = "未含關鍵字之重大訊息標題（日期＋標題，新到舊）"
        if omitted:
            head2 += "；另 {0} 則例行公告標題因篇幅從略".format(omitted)
        items.append(mk_item("公開資訊觀測站", "歷史重大訊息清單（未命中關鍵字者）", url, date.isoformat(),
                             "重大訊息標題清單", head2 + "：\n" + "\n".join(out)))
    return items


def src_mops(ctx):
    rows, errs = fetch_mops_rows(ctx.http_mops, ctx.code, ctx.date)
    # 全文只抓最重要的幾則：severity≥3 先（最多 MAX_DETAIL），中等級（處分／異常）補到 MAX_DETAIL_SEV2；
    # 同標題只取最新一則（rows 已是新到舊）；單純「更正」不抓
    cand, seen = [], set()
    for r in rows:
        sev = _severity(tag_keywords(r["title"]))
        if sev >= 2 and r["params"] and r["title"] not in seen:
            seen.add(r["title"])
            cand.append((sev, r))
    pick = [r for sev, r in cand if sev >= 3][:MAX_DETAIL]
    pick += [r for sev, r in cand if sev == 2][:max(0, min(MAX_DETAIL_SEV2, MAX_DETAIL - len(pick)))]
    pick.sort(key=lambda r: -_severity(tag_keywords(r["title"])))  # 穩定排序：同級仍新到舊
    details, derr = {}, 0
    for r in pick:
        try:
            d = fetch_mops_detail(ctx.http_mops, r["params"])
        except FetchError:
            derr += 1
            continue
        if d:
            details[(r["date"], r["title"])] = d
    items = build_mops_items(ctx.code, rows, details, ctx.date, [(r["date"], r["title"]) for r in pick])
    axes = {"major_events": items}
    anti = [r for r in rows if ANTITRUST_RE.search(r["title"])]
    if anti:
        txt = "公開資訊觀測站重大訊息中，標題涉及公平會／裁罰／罰鍰者 {0} 則：\n".format(len(anti)) + "\n".join(
            "{0} {1}".format(r["date"], r["title"][:60]) for r in anti[:15])
        axes["regulatory_antitrust"] = [mk_item("公開資訊觀測站", "歷史重大訊息（公平會／裁罰類標題）",
                                                MOPS_PAGE.format(code=ctx.code), ctx.date.isoformat(),
                                                "重大訊息標題", txt)]
    note = ""
    if errs:
        note += "；".join(errs) + "。"
    if derr:
        note += "{0} 則全文抓取失敗。".format(derr)
    news = [{"date": r["date"], "ticker": ctx.ticker, "title": r["title"],
             "keyword_tags": ";".join(tag_keywords(r["title"])), "url": MOPS_PAGE.format(code=ctx.code)} for r in rows]
    return {"axes": axes, "csv_news": news, "note": note.strip()}


# ---------------------------------------------------------------------------
# doc.twse.com.tw：年報／財報 → 主要客戶表
# ---------------------------------------------------------------------------

def parse_doc_listing(raw):
    """t57sb01 step=1 回傳（Big5 bytes）→ [{co, yr, desc, kind, filename, upload(iso)}]。"""
    text = raw.decode("big5hkscs", errors="replace") if isinstance(raw, bytes) else raw
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", text, flags=re.S):
        m = re.search(r"readfile2?\(\"(\w)\",\"(\w+)\",\"([^\"]+)\"\)", tr)
        if not m:
            continue
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c).replace("&nbsp;", "")).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        if len(cells) < 6:
            continue
        out.append({"co": cells[0], "yr": cells[1], "desc": cells[5], "kind": m.group(1), "filename": m.group(3),
                    "upload": roc_to_iso(cells[9]) if len(cells) > 9 else None})
    return out


def pick_annual_report(rows, date):
    """從 mtype=F 清單挑股東會年報：中文版、資料年度最新、優先股東會後修訂本，上傳日不晚於 date。"""
    iso = date.isoformat()
    cands = []
    for r in rows:
        d = r["desc"]
        if "股東會年報" not in d or d.startswith("英文"):
            continue
        if r["upload"] and r["upload"] > iso:
            continue
        m = re.match(r"(\d{2,3})", r["yr"])
        yr = int(m.group(1)) if m else 0
        revised = 1 if "修訂本" in d else 0
        cands.append((yr, revised, r["upload"] or "", r))
    if not cands:
        return None
    cands.sort(key=lambda t: t[:3], reverse=True)
    return cands[0][3]


def pick_q4_financials(rows, date):
    """從 mtype=A 清單挑最新第四季合併財報（中文）。"""
    iso = date.isoformat()
    cands = []
    for r in rows:
        if "第四季" not in r["yr"] or r["desc"] != "IFRSs合併財報":
            continue
        if r["upload"] and r["upload"] > iso:
            continue
        m = re.match(r"(\d{2,3})", r["yr"])
        cands.append((int(m.group(1)) if m else 0, r["upload"] or "", r))
    if not cands:
        return None
    cands.sort(key=lambda t: t[:2], reverse=True)
    return cands[0][2]


AR_ANCHORS = [
    re.compile(r"最近二年度[^\n]{0,10}主要銷貨客戶"),
    re.compile(r"主要銷貨客戶"),
    re.compile(r"曾[佔占]銷貨總額百分之十以上"),
    re.compile(r"[佔占]營業收入(?:淨額)?百分之十以上之客戶"),
    re.compile(r"曾[佔占]進[（(]銷[）)]貨總額百分之十以上"),
    re.compile(r"主要進銷貨客戶"),
    # 6223.TWO 年報寫「最近兩年度佔銷貨總額 10%之客戶名單」：「兩」與阿拉伯數字 10%
    re.compile(r"最近[二兩]年度[^\n]{0,6}[佔占]銷貨(?:總額|淨額)\s*10\s*[%％]"),
]
FS_ANCHORS = [re.compile(r"重要客戶資訊"), re.compile(r"主要客戶資訊"), re.compile(r"對單一客戶之銷售"),
              re.compile(r"主要客戶")]
_AMOUNT_RE = re.compile(r"(?<![\d,.])(\d{1,3}(?:,\d{3})+|\d{5,}|0(?=\s+0(?!\d)))(?![\d,])")


def _tablelike(lines):
    """後續幾行是否有金額（千分位或 5 位以上數字）：目錄頁只有頁碼，過不了。"""
    hit = [len(_AMOUNT_RE.findall(ln)) for ln in lines]
    return sum(1 for n in hit if n) >= 2 or any(n >= 2 for n in hit)


def find_table_anchor(pages, anchors, window=30):
    """依錨點優先序、頁序找第一個「後面真的有金額」的位置，回傳 (頁碼 1 起算, 行號, 錨點文字)；找不到 None。"""
    for rx in anchors:
        for pi, page in enumerate(pages):
            lines = page.split("\n")
            for li, ln in enumerate(lines):
                m = rx.search(ln)
                if m and _tablelike(lines[li + 1:li + 1 + window]):
                    return pi + 1, li, m.group(0)
    return None


def _pdftotext(pdf, *extra):
    p = subprocess.run(["pdftotext", "-layout", *extra, str(pdf), "-"], capture_output=True, timeout=180)
    if p.returncode != 0:
        raise FetchError("pdftotext 失敗：{0}".format(p.stderr.decode("utf-8", "replace")[:100]))
    return p.stdout.decode("utf-8", errors="replace")


def _crop_below_anchor(pdf, page, anchor_rx, height=300):
    """用 bbox 找到錨點那行的座標，裁出「錨點右下方」一塊。雙欄排版年報（聯電）的表格在右欄，
    整頁 -layout 會把左右欄文字交錯，裁切後才讀得到完整表格。找不到座標回 None。"""
    p = subprocess.run(["pdftotext", "-bbox-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
                       capture_output=True, timeout=120)
    if p.returncode != 0:
        return None
    raw = p.stdout.decode("utf-8", errors="replace")
    pg = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', raw)
    if not pg:
        return None
    pw, ph = float(pg.group(1)), float(pg.group(2))
    for lm in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="[\d.]+" yMax="[\d.]+">(.*?)</line>', raw, flags=re.S):
        words = re.findall(r">([^<]*)</word>", lm.group(3))
        text = _html.unescape("".join(words))
        if anchor_rx.search(text):
            ax = float(lm.group(1))
            x = max(0, int(ax - 4)) if ax > pw * 0.4 else 0  # 單欄排版表格會比標題更靠左，整頁寬才不丟左欄
            y = max(0, int(float(lm.group(2)) - 3))
            h = int(min(height, ph - y))
            w = int(pw - x)
            out = _pdftotext(pdf, "-f", str(page), "-l", str(page), "-x", str(x), "-y", str(y), "-W", str(w), "-H", str(h))
            return out
    return None


def _tidy_layout(text):
    lines = [re.sub(r" {3,}", "  ", ln.rstrip()) for ln in text.split("\n")]
    return "\n".join(ln for ln in lines if ln.strip())


_TOTAL_RE = re.compile(r"(?<![\d.])100(?:\.0+)?\s*%?(?![\d.,])")
_AFTER_TOTAL = re.compile(r"^(註|增減變動原因|變動原因|主係|主要係|說明|Note)")


def trim_table(text, max_lines=26):
    """表格文字修到『合計列＋其後的註記』為止，後面接著的別的章節（員工資料等）不要。
    找不到合計列就只留前 max_lines 行。"""
    lines = text.split("\n")
    tot = None
    for i, ln in enumerate(lines):
        if i > 1 and _TOTAL_RE.search(ln) and _AMOUNT_RE.search(ln):
            tot = i
            break
    if tot is None:
        return "\n".join(lines[:max_lines])
    out = lines[:tot + 1]
    for ln in lines[tot + 1:tot + 12]:
        st = ln.strip()
        toks = st.split()
        if _AFTER_TOTAL.match(st) or (toks and all(len(t) <= 3 for t in toks)):
            out.append(ln)
        elif st.startswith("截至年報刊印日"):
            continue
        else:
            break
    return "\n".join(out)


def extract_customer_table(pdf, anchors, use_crop=True, max_lines=26):
    """回傳 (頁碼, 文字) 或 None。"""
    full = _pdftotext(pdf)
    pages = full.split("\f")
    hit = find_table_anchor(pages, anchors)
    if not hit:
        return None
    page, li, anchor_text = hit
    text = None
    if use_crop:
        text = _crop_below_anchor(pdf, page, re.compile(re.escape(anchor_text)))
    if not text or not _tablelike(text.split("\n")):
        lines = pages[page - 1].split("\n")
        text = "\n".join(lines[max(0, li):li + 30])
    return page, trim_table(_tidy_layout(text), max_lines)


_STOP_LABELS = re.compile(r"其他|營業收入|銷貨淨額|淨額|合計|合\s*計|名稱|客戶名稱|Total|Others|項目|比率|金額")
_PCT_AFTER = r"\s*(\d{1,3}(?:\.\d+)?)\s*%?(?![\d,])"
_UNIT_PAT = re.compile(r"(新[臺台]幣[千仟佰百萬]{0,2}元|百萬元|仟元|千元|NT\$[^\s]{0,8}|美金[千仟]?元|USD[^\s]{0,6})")
_REL_WORDS = re.compile(r"非關係人|關係人|無|之|[$＄%\-－]")


def _clean_label(raw):
    t = _REL_WORDS.sub(" ", raw)
    t = re.sub(r"(?<![A-Za-z\d])\d{1,3}(?![A-Za-z\d])", " ", t)  # 項次
    return re.sub(r"\s+", " ", t).strip()


def parse_customer_rows(text, data_year_roc=None):
    """從表格文字抓『客戶標籤、金額、占比』；年度依表頭「NNN 年」出現順序對應前兩個金額欄。
    列上抓不到兩個金額（欄位被換行拆開）就略過，不猜；其餘版型靠摘錄本文，不硬解析。"""
    lines = text.split("\n")
    years = []
    for ln in lines[:8]:
        for y in re.findall(r"(?<!\d)(1[0-4]\d)\s*年", ln):
            if int(y) not in years:
                years.append(int(y))
    if not years and data_year_roc:
        years = [data_year_roc, data_year_roc - 1]
    mu = _UNIT_PAT.search(re.sub(r"\s+", "", text))
    unit = mu.group(1) if mu else ""
    rows = []
    for ln in lines:
        ams = list(_AMOUNT_RE.finditer(ln))
        if len(ams) < 2:
            continue
        segs, prev = [], 0
        for am in ams:
            amount = int(am.group(1).replace(",", ""))
            pm = re.match(_PCT_AFTER, ln[am.end():am.end() + 14])
            pct, end = None, am.end()
            if pm:
                v = float(pm.group(1))
                nxt = [a2.start() for a2 in ams if a2.start() >= am.end()]
                if 0 <= v <= 100 and not (nxt and am.end() + pm.start(1) >= nxt[0]):
                    pct, end = v, am.end() + pm.end()
            segs.append([_clean_label(ln[prev:am.start()]), amount, pct])
            prev = end
        for i in range(len(segs) - 1, -1, -1):  # 空標籤沿用同列相鄰欄（同一客戶跨年度）
            if not segs[i][0]:
                segs[i][0] = segs[i + 1][0] if i + 1 < len(segs) else ""
        for i in range(1, len(segs)):
            if not segs[i][0]:
                segs[i][0] = segs[i - 1][0]
        label = segs[0][0]
        if not label or len(label) > 24 or _STOP_LABELS.search(label):
            continue
        for k, (lab, amount, pct) in enumerate(segs[:2]):
            fy = (years[k] + 1911) if k < len(years) else None
            rows.append({"customer_label": lab, "amount": amount, "unit": unit, "pct": pct, "fiscal_year": fy})
    return rows


def _fetch_doc_pdf(ctx, rec, workdir):
    """step=9 取得暫時 PDF 連結再下載，存到 workdir，回傳 Path。"""
    r = ctx.http_doc.post(DOC_BASE, data={"step": 9, "kind": rec["kind"], "co_id": ctx.code, "filename": rec["filename"]},
                          headers=UA)
    m = re.search(r"href='(/pdf/[^']+)'", r.content.decode("big5hkscs", errors="replace"))
    if not m:
        raise FetchError("doc.twse 取不到暫時 PDF 連結：{0}".format(rec["filename"]))
    p = ctx.http_doc.get("https://doc.twse.com.tw" + m.group(1), headers=UA)
    if p.status_code != 200 or not p.content.startswith(b"%PDF"):
        raise FetchError("doc.twse PDF 下載失敗（HTTP {0}）".format(p.status_code))
    path = Path(workdir) / rec["filename"]
    path.write_bytes(p.content)
    return path


def _list_docs(ctx, year, mtype):
    r = ctx.http_doc.post(DOC_BASE, data={"step": 1, "colorchg": 1, "co_id": ctx.code, "year": str(year),
                                         "seamon": "", "mtype": mtype, "dtype": ""}, headers=UA)
    if r.status_code != 200:
        raise FetchError("doc.twse 清單 HTTP {0}".format(r.status_code))
    return parse_doc_listing(r.content)


def src_customers(ctx):
    if not shutil.which("pdftotext"):
        raise FetchError("本機沒有 pdftotext（poppler），略過年報主要客戶表")
    ry = _roc_year(ctx.date)
    notes = []
    tmp = tempfile.mkdtemp(prefix="primary_docs_")
    try:
        # 年報優先；年報沒有或沒表才輪到財報附註（惰性產生：年報成功就不查 mtype=A 清單，省請求）
        def sources():
            ar, ar_year = None, ry
            for y in (ry, ry - 1):
                try:
                    ar = pick_annual_report(_list_docs(ctx, y, "F"), ctx.date)
                except FetchError as e:
                    notes.append(str(e))
                if ar:
                    ar_year = y
                    break
            if ar:
                yield ar, "{0}股東會年報".format(ar["yr"].replace(" ", "")), AR_ANCHORS, "F", ar_year
            else:
                notes.append("清單內沒有股東會年報")
            fs, fs_year = None, ry - 1
            for y in (ry - 1, ry - 2):
                try:
                    fs = pick_q4_financials(_list_docs(ctx, y, "A"), ctx.date)
                except FetchError as e:
                    notes.append(str(e))
                if fs:
                    fs_year = y
                    break
            if fs:
                yield fs, "{0}合併財報（附註）".format(fs["yr"].replace(" ", "")), FS_ANCHORS, "A", fs_year

        for rec, doc_name, anchors, mtype, list_year in sources():
            try:
                pdf = _fetch_doc_pdf(ctx, rec, tmp)
                got = extract_customer_table(pdf, anchors, use_crop=(mtype == "F"), max_lines=26 if mtype == "F" else 12)
            except (FetchError, subprocess.TimeoutExpired, OSError) as e:
                notes.append("{0}：{1}".format(doc_name, str(e)[:120]))
                continue
            if not got:
                notes.append("{0}：沒找到主要客戶表".format(doc_name))
                continue
            page, text = got
            data_year = None
            m = re.match(r"(\d{2,3})", rec["yr"])
            if m:
                data_year = int(m.group(1))
            as_of = rec["upload"] or ctx.date.isoformat()
            url = DOC_LIST_URL.format(code=ctx.code, year=list_year, mtype=mtype)
            body = ("【原文：{0}（檔名 {1}，PDF 第 {2} 頁，上傳日 {3}）；排版為 pdftotext -layout 還原，欄位間以空白分隔】\n{4}"
                    .format(doc_name, rec["filename"], page, as_of, text))
            item = mk_item("公開資訊觀測站電子書件（doc.twse.com.tw）", "{0}（{1}）".format(doc_name, rec["filename"]), url, as_of,
                           "主要銷貨客戶表（PDF 第 {0} 頁）".format(page), clip_to_weight(body, 900))
            rows = parse_customer_rows(text, data_year)
            csv = [dict(r, date=as_of, ticker=ctx.ticker, source_url=url) for r in rows]
            return {"axes": {"customer_concentration_credit": [item]}, "csv_customers": csv,
                    "note": "；".join(notes)}
        raise FetchError("；".join(notes) or "年報與財報都找不到主要客戶表")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# 公平會處分書、證交所反競爭訴訟損失
# ---------------------------------------------------------------------------

def _hidden_fields(page):
    return {m.group(1): _html.unescape(m.group(2))
            for m in re.finditer(r'<input[^>]*type="hidden"[^>]*name="([^"]+)"[^>]*value="([^"]*)"', page)}


def parse_ftc_results(page):
    """公平會決定書查詢結果 → (總筆數, [(日期, 類型, 法條, 案由, pdf網址)])。"""
    tot = re.search(r'lb_totalRows"[^>]*>([\d,]+)<', page)
    total = int(tot.group(1).replace(",", "")) if tot else None
    items = []
    for li in re.findall(r'<ul class="result-list">(.*?)</ul>', page, flags=re.S):
        d = re.search(r"<span>發文日期</span><p>([^<]*)", li)
        ty = re.search(r"<span>類型</span><p>([^<]*)", li)
        law = re.search(r"<span>相關法條</span><p>(.*?)</p>", li, flags=re.S)
        a = re.search(r"href='([^']+)'[^>]*>.*?<p>(.*?)</p>", li, flags=re.S)
        items.append((d.group(1).strip() if d else "", ty.group(1).strip() if ty else "",
                      one_line(_html.unescape(re.sub(r"<[^>]+>", " ", law.group(1)))) if law else "",
                      one_line(_html.unescape(re.sub(r"<[^>]+>", "", a.group(2)))) if a else "",
                      a.group(1) if a else ""))
    return (total if total is not None else len(items)), items


def ftc_search(http, keyword):
    g = http.get(FTC_URL, headers=UA)
    if g.status_code != 200:
        raise FetchError("公平會 HTTP {0}".format(g.status_code))
    f = _hidden_fields(g.text)
    f.update({"__EVENTTARGET": "ctl00$ContentPlaceHolder1$searchButton", "__EVENTARGUMENT": "",
              "ctl00$ContentPlaceHolder1$PdfKeyWords": keyword, "ctl00$ContentPlaceHolder1$FormalDocDateStart": "",
              "ctl00$ContentPlaceHolder1$FormalDocDateEnd": "", "ctl00$ContentPlaceHolder1$CaseKindID": "",
              "ctl00$ContentPlaceHolder1$LawID": "", "ctl00$ContentPlaceHolder1$lawList": ""})
    p = http.post(FTC_URL, data=f, headers=UA)
    if p.status_code != 200 or "result-list" not in p.text and "page-statistics" not in p.text:
        raise FetchError("公平會查詢結果頁異常（HTTP {0}）".format(p.status_code))
    return parse_ftc_results(p.text)


def build_ftc_items(keyword, total, rows, date, full_name_known=True):
    date_iso = date.isoformat()
    cav = "" if full_name_known else "（注意：查不到正式全名，改用簡稱搜尋，誤中同名機構的機率較高）"
    head = ("【程式統計】公平會「處分書及決議書」資料庫（ftc.gov.tw 決定書查詢），以關鍵字「{0}」全文搜尋（查詢日 {1}）"
            "共 {2} 筆{3}。命中只代表處分書或決議書全文提到該名稱，不代表該公司被處分；"
            "案由含公司名者標「案名含公司名」，其餘標「僅文內提及」。").format(keyword, date_iso, total, cav)
    if not rows:
        head += "沒有任何命中。"
    items = [mk_item("公平交易委員會", "處分書及決議書全文搜尋「{0}」".format(keyword), FTC_URL, date_iso,
                     "公平會處分書搜尋結果", head)]
    for d, ty, law, title, url in rows[:5]:
        flag = "案名含公司名" if keyword and keyword in title else "僅文內提及"
        iso = d.replace("/", "-") if re.match(r"\d{4}/\d{2}/\d{2}", d) else date_iso
        items.append(mk_item("公平交易委員會", "{0}：{1}".format(ty, title[:50]), url or FTC_URL, iso,
                             "公平會處分書（{0}）".format(flag),
                             "{0} {1}［{2}］{3}（{4}）".format(d, ty, law, title, flag)))
    return items


def parse_anti_loss(rows, code):
    """證交所／櫃買 ESG 開放資料 → (報告年度, 出表日 iso, 金額字串) 或 None。"""
    for r in rows:
        if str(r.get("公司代號") or r.get("SecuritiesCompanyCode") or "").strip() == code:
            amt = None
            for k, v in r.items():
                if "金錢損失" in k:
                    amt = str(v).strip()
            return str(r.get("報告年度") or "").strip(), roc_to_iso(str(r.get("出表日期") or "")), amt
    return None


def src_ftc(ctx):
    meta = ctx.meta or {}
    full = meta.get("full_name") or ""
    kw = _norm_name(full) or meta.get("abbr") or ctx.abbr_fallback
    if not kw:
        raise FetchError("查不到公司名稱，無法搜尋公平會")
    items = []
    note = ""
    total, rows = ftc_search(ctx.http_ftc, kw)
    items += build_ftc_items(kw, total, rows, ctx.date, full_name_known=bool(full))
    if total and total > len(rows):
        note = "公平會共 {0} 筆，只收第一頁 {1} 筆（新到舊）。".format(total, len(rows))
    try:
        url = TPEX_ANTI if (meta.get("market") == "otc" or ctx.suffix == "TWO") else TWSE_ANTI
        tag = "O" if url == TPEX_ANTI else "L"
        data = _cached_json(ctx.http_open, url, ctx.global_cache / "tw_anti_{0}.json".format(tag))
        got = parse_anti_loss(data, ctx.code)
        if got:
            yr, iso, amt = got
            txt = ("{0}（{1}）「企業ESG資訊揭露彙總資料—反競爭行為法律訴訟」：報告年度 {2}，"
                   "因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)＝{3}。").format(
                "證交所 OpenAPI t187ap46_L_20" if tag == "L" else "櫃買中心 OpenAPI t187ap46_O_20",
                meta.get("abbr") or ctx.code, yr, amt)
            items.append(mk_item("證交所／櫃買中心開放資料", "ESG 揭露彙總：反競爭行為法律訴訟", url, iso or ctx.date.isoformat(),
                                 "反競爭行為法律訴訟損失", txt))
    except FetchError as e:
        note += "反競爭訴訟開放資料失敗：{0}".format(str(e)[:80])
    return {"axes": {"regulatory_antitrust": items}, "note": note.strip()}
