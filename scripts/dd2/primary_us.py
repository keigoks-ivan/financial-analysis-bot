#!/usr/bin/env python3
"""primary_docs 美股來源：SEC EDGAR 最新 10-K（外國發行人 20-F）分節＋依軸關鍵字挑段，近 12 個月 8-K（20-F 為 6-K）清單。

只用 EDGAR 官方端點（submissions JSON、Archives 原檔），User-Agent 用 dd_numbers_extra.SEC_HEADERS，
請求間隔 ≥1 秒（遠低於 SEC 每秒 10 次上限）。零 LLM。
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import time
from pathlib import Path

from primary_common import (FetchError, clip_to_weight, html_to_text, mk_item, one_line, pick_paragraphs, weight)

try:  # 沿用數字包的 SEC User-Agent；萬一 import 失敗（缺套件）用同一字串
    from dd_numbers_extra import SEC_HEADERS
except Exception:  # pragma: no cover
    SEC_HEADERS = {"User-Agent": "financial-analysis-bot keigoks@gmail.com"}

SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
ARCHIVE = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accn}/{doc}"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
MAX_8K_DETAIL = 3

# 各表格式的章節 id → 角色（business／risk／legal／mda／fs）
ROLE = {
    "10-K": {"business": "1", "risk": "1A", "legal": "3", "mda": "7", "fs": "8"},
    "20-F": {"business": "4", "risk": "3", "legal": "8", "mda": "5", "fs": "18"},
}
ITEM_LABEL = {
    "10-K": {"1": "Item 1. Business", "1A": "Item 1A. Risk Factors", "3": "Item 3. Legal Proceedings",
             "7": "Item 7. MD&A", "8": "Item 8. Financial Statements"},
    "20-F": {"4": "Item 4. Information on the Company", "3": "Item 3. Key Information (含 3.D Risk Factors)",
             "8": "Item 8. Financial Information（含 8.A.7 Legal Proceedings）", "5": "Item 5. Operating and Financial Review",
             "18": "Item 18. Financial Statements"},
}
# 章節標題（比對行首）；順序即文件順序，供找「下一個章節標題」
ITEMS_10K = [("1", r"business"), ("1A", r"risk\s+factors"), ("1B", r"unresolved"), ("1C", r"cybersecurity"),
             ("2", r"properties"), ("3", r"legal\s+proceedings"), ("4", r"mine\s+safety"),
             ("5", r"market\s+for"), ("6", r"(?:\[?reserved|selected)"), ("7", r"management[’']?s\s+discussion"),
             ("7A", r"quantitative"), ("8", r"financial\s+statements"), ("9", r"changes\s+in"),
             ("9A", r"controls"), ("9B", r"other\s+information"), ("9C", r"disclosure\s+regarding"),
             ("10", r"directors"), ("11", r"executive\s+compensation"), ("12", r"security\s+ownership"),
             ("13", r"certain\s+relationships"), ("14", r"principal\s+account"), ("15", r"exhibit")]
ITEMS_20F = [("1", r"identity\s+of"), ("2", r"offer\s+statistics"), ("3", r"key\s+information"),
             ("4", r"information\s+on\s+the\s+company"), ("4A", r"unresolved"),
             ("5", r"operating\s+and\s+financial\s+review"), ("6", r"directors,?\s+senior"), ("7", r"major\s+shareholders"),
             ("8", r"financial\s+information"), ("9", r"the\s+offer\s+and\s+listing"), ("10", r"additional\s+information"),
             ("11", r"quantitative"), ("12", r"description\s+of\s+securities"), ("13", r"defaults"),
             ("14", r"material\s+modifications"), ("15", r"controls"), ("16", r"\[?reserved|audit\s+committee"),
             ("17", r"financial\s+statements"), ("18", r"financial\s+statements"), ("19", r"exhibits")]

# 軸 → 規則（regex, 權重）與可挑的章節角色加成；roles=None 表示全文（含財報附註）
def _r(*pairs):
    return [(re.compile(p, re.I), w) for p, w in pairs]


AXIS_RULES = {
    "customer_concentration_credit": {
        "rules": _r((r"largest customers?|two largest|three largest", 5), (r"customer concentration|concentrations? of (?:credit|customer)", 3),
                    (r"(?:accounted for|represent(?:ed|s)?|comprised|made up)[^.]{0,80}\d{1,2}(?:\.\d+)?\s?%[^.]{0,100}(?:revenue|sales|receivable)", 4),
                    (r"significant customers?|major customers?|top (?:five|ten|\d+) customers?|ten largest customers", 2),
                    (r"\d{1,2}(?:\.\d+)?\s?% of (?:our |total |net )?(?:revenue|sales)", 1.5)),
        "roles": None, "budget": 1500, "require": re.compile(r"customer", re.I)},
    "customer_second_source": {
        "rules": _r((r"second[- ]sourc|dual[- ]sourc|multi[- ]sourc|single[- ]sourc|sole[- ]sourc", 3),
                    (r"in-?house|insourc|vertically integrat|develop(?:ing)? (?:their|its) own", 2.5),
                    (r"largest customer|key customers?", 2), (r"design wins?", 1)),
        "roles": {"business": 1.5, "risk": 1.2, "mda": 0.8}, "budget": 1500, "require": re.compile(r"customer", re.I)},
    "regulatory_antitrust": {
        "rules": _r((r"antitrust|anti-trust|anticompetitive|anti-competitive", 4),
                    (r"Federal Trade Commission|\bFTC\b|Department of Justice|\bDOJ\b|European Commission|competition authorit|"
                     r"Competition (?:and Markets )?Authority|\bSAMR\b|State Administration for Market Regulation|Sherman Act|"
                     r"Clayton Act|merger control|monopol", 3),
                    (r"investigation|subpoena|civil investigative demand|statement of objections", 1)),
        "roles": {"business": 1.0, "risk": 1.3, "legal": 1.5, "mda": 0.8}, "budget": 1000},
    "reg_tariff_export": {
        "rules": _r((r"tariff", 3), (r"export (?:control|restriction|licen[cs]e)|Entity List|Export Administration Regulations|"
                                      r"Bureau of Industry and Security", 3),
                    (r"sanction|OFAC|Section 301|Section 232|IEEPA|trade (?:war|restriction|tension)", 2), (r"CHIPS Act", 1),
                    (r"China|Taiwan", 0.5)),
        "roles": {"business": 1.0, "risk": 1.3, "mda": 1.0}, "budget": 1500},
    "substitute_technology": {
        "rules": _r((r"substitut\w+", 3), (r"alternative (?:technolog|solution|product)", 3),
                    (r"disrupt\w*|displace\w*|technolog\w* obsole\w+|new entrants?|emerging technolog|competing technolog|technological change", 2.5),
                    (r"compet", 0.5)),
        "roles": {"business": 1.3, "risk": 1.3}, "budget": 1500},
    "competitive_share_entrants": {
        "rules": _r((r"market share|share of the market", 3), (r"compet\w+", 1.0),
                    (r"new entrants?|entrants|entering the market", 3),
                    (r"principal competitors?|main competitors?|key competitors?|major competitors?|competitors include|we compete (?:with|against)", 3)),
        "roles": {"business": 1.5, "risk": 1.0, "mda": 0.8}, "budget": 1500},
    "channel_business_model_shift": {
        "rules": _r((r"distribut(?:or|ion|ors)", 2), (r"channel", 2.5),
                    (r"resellers?|retail(?:ers)?|direct sales|direct-to-consumer|e-?commerce|marketplace|go-to-market|subscription|"
                     r"licens(?:e|ing) model|business model|OEM", 1.5)),
        "roles": {"business": 1.5, "mda": 1.0}, "budget": 1500, "min_score": 5.0},
}
SENT_MAX = 90  # 平均每句超過 90 詞的段落多半是清單／圖表標題串接，略過
EXCLUDE_RE = re.compile(r"forward-looking|safe harbor|Private Securities Litigation Reform", re.I)
LITIGATION_RULES = _r((r"class action|securities (?:class|litigation)|lawsuits?|filed (?:a )?complaint|complaint (?:was |has been )?filed|plaintiffs?|arbitration", 3),
                      (r"SEC (?:investigation|subpoena)|subpoena|restate|restatement|product recall", 2),
                      (r"settle(?:d|ment)|damages", 1.5), (r"acqui(?:re|sition)|merger|divest", 0.5))
LITIGATION_MIN = 4.0
MIN_SCORE = 3.0

# 8-K 項目編號 → 名稱（SEC Form 8-K 條文標題）；notable 是值得抓全文的優先序
ITEM_8K = {
    "1.01": "Entry into a Material Definitive Agreement", "1.02": "Termination of a Material Definitive Agreement",
    "1.03": "Bankruptcy or Receivership", "1.04": "Mine Safety", "1.05": "Material Cybersecurity Incidents",
    "2.01": "Completion of Acquisition or Disposition of Assets", "2.02": "Results of Operations and Financial Condition",
    "2.03": "Creation of a Direct Financial Obligation", "2.04": "Triggering Events That Accelerate an Obligation",
    "2.05": "Costs Associated with Exit or Disposal Activities", "2.06": "Material Impairments",
    "3.01": "Notice of Delisting or Failure to Satisfy a Listing Rule", "3.02": "Unregistered Sales of Equity Securities",
    "3.03": "Material Modification to Rights of Security Holders",
    "4.01": "Changes in Registrant's Certifying Accountant",
    "4.02": "Non-Reliance on Previously Issued Financial Statements",
    "5.01": "Changes in Control of Registrant", "5.02": "Departure/Election of Directors or Officers",
    "5.03": "Amendments to Articles or Bylaws", "5.07": "Submission of Matters to a Vote of Security Holders",
    "7.01": "Regulation FD Disclosure", "8.01": "Other Events", "9.01": "Financial Statements and Exhibits",
}
NOTABLE_8K = ["4.02", "1.03", "2.06", "2.05", "2.01", "1.01", "1.02", "3.01", "1.05", "5.01", "8.01"]


# ---------------------------------------------------------------------------
# EDGAR 取檔
# ---------------------------------------------------------------------------

def _load_tickers(http, cache_dir):
    cache = Path(cache_dir) / "company_tickers.json"  # 與 dd_numbers_extra 共用同一份快取
    if cache.exists() and (time.time() - cache.stat().st_mtime) < 7 * 86400:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    r = http.get(TICKERS_URL)
    if r.status_code != 200:
        raise FetchError("SEC company_tickers HTTP {0}".format(r.status_code))
    data = r.json()
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(data), encoding="utf-8")
    except OSError:
        pass
    return data


def resolve_cik(http, ticker, cache_dir):
    base = ticker.split(".")[0].upper()
    for v in _load_tickers(http, cache_dir).values():
        if v.get("ticker", "").upper() == base:
            return str(v["cik_str"]).zfill(10)
    raise FetchError("{0} 查無 SEC CIK".format(ticker))


def fetch_submissions(ctx):
    if getattr(ctx, "_sub", None) is None:
        cik = resolve_cik(ctx.http_sec, ctx.ticker, ctx.global_cache)
        r = ctx.http_sec.get(SUBMISSIONS.format(cik=cik))
        if r.status_code != 200:
            raise FetchError("SEC submissions HTTP {0}".format(r.status_code))
        ctx._sub = (cik, r.json())
    return ctx._sub


def _recent_rows(sub):
    rec = sub["filings"]["recent"]
    n = len(rec["form"])
    cols = ["form", "filingDate", "accessionNumber", "primaryDocument", "reportDate", "items", "primaryDocDescription"]
    for i in range(n):
        yield {c: (rec.get(c) or [""] * n)[i] for c in cols}


def pick_annual_filing(sub, date_iso):
    """最新的 10-K（沒有再找 20-F）；filingDate 不晚於 date。"""
    best = None
    for r in _recent_rows(sub):
        if r["form"] not in ("10-K", "20-F") or r["filingDate"] > date_iso:
            continue
        if best is None or r["filingDate"] > best["filingDate"]:
            best = r
    return best


def filing_url(cik, row):
    return ARCHIVE.format(cik_int=int(cik), accn=row["accessionNumber"].replace("-", ""), doc=row["primaryDocument"])


# ---------------------------------------------------------------------------
# 分節與挑段
# ---------------------------------------------------------------------------

def _heading_re(items):
    return [(iid, re.compile(r"^\s*(?:part\s+[iv]+[\s,.\-–—]*)?item\s*{0}\b\s*[\.:\-–—]?\s*{1}".format(re.escape(iid), title), re.I))
            for iid, title in items]


def split_sections(text, form):
    """回傳 (lines, spans)：spans＝{章節id: (起行, 迄行)}。每個章節取「到下一個章節標題為止最長」的那個標題
    （目錄裡的同名標題後面緊接下一個標題，區段極短，自然被挑掉）。"""
    items = ITEMS_20F if form == "20-F" else ITEMS_10K
    raw = text.split("\n")
    lines, i = [], 0
    while i < len(raw):  # 「Item 1A.」與「Risk Factors」被拆成兩行時併回一行
        ln = raw[i]
        if re.fullmatch(r"\s*(?:part\s+[iv]+[\s,.\-–—]*)?item\s*\d{1,2}[A-C]?\s*[\.:\-–—]?\s*", ln, re.I) and i + 1 < len(raw):
            ln = ln.strip() + " " + raw[i + 1]
            i += 1
        lines.append(ln)
        i += 1
    heads = []
    for iid, rx in _heading_re(items):
        for li, ln in enumerate(lines):
            if len(ln) <= 160 and rx.match(ln):
                heads.append((li, iid))
    heads.sort()
    spans = {}
    for li, iid in heads:
        nxt = next((l2 for l2, i2 in heads if l2 > li and i2 != iid), len(lines))
        if iid not in spans or (nxt - li) > (spans[iid][1] - spans[iid][0]):
            spans[iid] = (li, nxt)
    return lines, spans


_ITEM_START_RE = re.compile(r"\s*(?:part\s+[iv]+\b|item\s*\d{1,2}[A-C]?\b)", re.I)


def make_paragraphs(lines):
    """行 → 段落（起始行號, 文字）。正常申報檔一行就是一段；年報型文件（ASML 20-F）一行只是視覺換行，
    要把沒收句號的短行併成一段。段落上限約 1,800 字元。"""
    paras, buf, start = [], [], None
    for li, ln in enumerate(lines):
        if not ln.strip():
            continue
        if buf and _ITEM_START_RE.match(ln):  # Item／Part 標題一律另起一段，不併進前面沒收句號的目錄行
            paras.append((start, " ".join(buf)))
            buf, start = [], None
        if start is None:
            start = li
        buf.append(ln)
        text = " ".join(buf)
        ends = re.search(r"[.!?”\"')\]]\s*$", ln) is not None
        if (ends and (len(ln) > 80 or weight(text) >= 15)) or len(text) > 1800:
            paras.append((start, text))
            buf, start = [], None
    if buf:
        paras.append((start, " ".join(buf)))
    return paras


def paragraphs_by_role(lines, spans, form):
    roles = ROLE[form]
    role_of = {v: k for k, v in roles.items()}
    owner = {}
    for iid, (a, b) in spans.items():
        for li in range(a, b):
            owner[li] = role_of.get(iid, "other")
    return [(li, owner.get(li, "other"), t) for li, t in make_paragraphs(lines) if 40 <= len(t) <= 6000]


def role_label(form, role, spans):
    iid = ROLE[form].get(role)
    return ITEM_LABEL[form].get(iid, role) if iid else "其他章節（財報附註等）"


def section_text(lines, spans, form, role, limit):
    iid = ROLE[form].get(role)
    if iid not in spans:
        return None
    a, b = spans[iid]
    body = "\n".join(l for l in lines[a:b] if len(l) > 3)
    return clip_to_weight(body, limit)


def _group(source, doc, url, as_of, picked, label_of):
    """挑出的段落依章節合併成一則 item（同章節的段落以空行分隔），省掉逐段的來源標頭。"""
    order, by = [], {}
    for role, t in picked:
        if role not in by:
            by[role] = []
            order.append(role)
        by[role].append(t)
    return [mk_item(source, doc, url, as_of, label_of(role), "\n\n".join(by[role])) for role in order]


def build_axis_items(lines, spans, form, doc, url, as_of):
    """依軸規則挑段，回傳 {軸: [item]}。關鍵章節（業務、風險）切不出來時改全文挑段。"""
    paras = paragraphs_by_role(lines, spans, form)
    roles = ROLE[form]
    whole = not (roles["business"] in spans and roles["risk"] in spans)  # 年報型 20-F 等沒有 Item 標題的文件
    label = (lambda role: "全文（無法依 Item 切段）") if whole else (lambda role: role_label(form, role, spans))
    out = {}
    for axis, cfg in AXIS_RULES.items():
        bonus = None if whole else cfg["roles"]
        picked = pick_paragraphs(paras, cfg["rules"], cfg["budget"] - (350 if axis == "regulatory_antitrust" else 0),
                                 min_score=cfg.get("min_score", MIN_SCORE), section_bonus=bonus,
                                 require=cfg.get("require"), exclude=EXCLUDE_RE, max_sentence_words=SENT_MAX)
        if picked:
            out[axis] = _group("SEC EDGAR", doc, url, as_of, picked, label)
    # Legal Proceedings 本文：regulatory_antitrust（前置）與 major_events 共用
    legal = section_text(lines, spans, form, "legal", 350)
    if legal and not whole:
        it = mk_item("SEC EDGAR", doc, url, as_of, role_label(form, "legal", spans), legal)
        out.setdefault("regulatory_antitrust", []).insert(0, it)
        out.setdefault("major_events", []).append(it)
    lit = pick_paragraphs(paras, LITIGATION_RULES, 450, min_score=LITIGATION_MIN, section_bonus=None, exclude=EXCLUDE_RE,
                          max_sentence_words=SENT_MAX)
    if lit:
        out.setdefault("major_events", []).extend(
            _group("SEC EDGAR", doc, url, as_of, lit, lambda role: ("全文" if whole else role_label(form, role, spans)) + "（訴訟／重大事項段落）"))
    return out


def src_us_annual(ctx):
    cik, sub = fetch_submissions(ctx)
    row = pick_annual_filing(sub, ctx.date.isoformat())
    if not row:
        raise FetchError("{0} 在 EDGAR 近況清單內沒有 10-K／20-F（可能是 40-F 或剛上市）".format(ctx.ticker))
    form = row["form"]
    url = filing_url(cik, row)
    r = ctx.http_sec.get(url, timeout=60)
    if r.status_code != 200:
        raise FetchError("{0} HTTP {1}".format(url, r.status_code))
    text = html_to_text(r.text)
    lines, spans = split_sections(text, form)
    doc = "{0}（FY{1}，申報 {2}）".format(form, (row["reportDate"] or row["filingDate"])[:4], row["filingDate"])
    axes = build_axis_items(lines, spans, form, doc, url, row["filingDate"])
    note = "{0} 申報 {1}；抓到章節 {2}。".format(form, row["filingDate"], "、".join(sorted(spans)) or "無")
    if not (ROLE[form]["business"] in spans and ROLE[form]["risk"] in spans):
        note += "業務／風險章節辨識不全（年報型文件），改全文挑段。"
    return {"axes": axes, "note": note}


# ---------------------------------------------------------------------------
# 8-K／6-K 清單
# ---------------------------------------------------------------------------

def build_8k_list(rows, date, foreign):
    start = (date - _dt.timedelta(days=365)).isoformat()
    kind = "6-K" if foreign else "8-K"
    sel = [r for r in rows if r["form"] in (kind, kind + "/A") and start <= r["filingDate"] <= date.isoformat()]
    sel.sort(key=lambda r: r["filingDate"], reverse=True)
    return sel


def _fmt_items(items_str):
    codes = [c.strip() for c in (items_str or "").split(",") if c.strip()]
    return codes, "；".join("{0} {1}".format(c, ITEM_8K.get(c, "")).strip() for c in codes)


def src_us_8k(ctx):
    cik, sub = fetch_submissions(ctx)
    rows = list(_recent_rows(sub))
    foreign = pick_annual_filing(sub, ctx.date.isoformat())
    foreign = bool(foreign and foreign["form"] == "20-F")
    sel = build_8k_list(rows, ctx.date, foreign)
    kind = "6-K" if foreign else "8-K"
    browse = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type={1}".format(cik, kind)
    start = (ctx.date - _dt.timedelta(days=365)).isoformat()
    head = "【程式統計】SEC EDGAR 申報清單，{0} 至 {1} 共 {2} 份 {3}".format(start, ctx.date.isoformat(), len(sel), kind)
    lines = []
    notable = []
    for r in sel:
        if foreign:
            lines.append("{0} {1} {2}".format(r["filingDate"], r["form"], one_line(r["primaryDocDescription"])))
            continue
        codes, label = _fmt_items(r["items"])
        lines.append("{0} {1} Items {2}".format(r["filingDate"], r["form"], label or "（未標項目）"))
        for c in NOTABLE_8K:
            if c in codes:
                notable.append((NOTABLE_8K.index(c), r, c))
                break
    if foreign:
        head += "（外國發行人以 6-K 公告，無 Item 編號）"
    else:
        head += "；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 {0} 份。".format(len(notable))
    head += "" if not foreign else "。"
    body = head + ("\n" + "\n".join(lines) if lines else "\n近 12 個月沒有此類申報。")
    items = [mk_item("SEC EDGAR", "{0} 申報清單（近12個月）".format(kind), browse, ctx.date.isoformat(), "{0} 清單".format(kind),
                     clip_to_weight(body, 650))]
    # 重大項目全文最多 MAX_8K_DETAIL 份：依項目優先序、同級新到舊
    notable.sort(key=lambda t: (t[0], -int(t[1]["filingDate"].replace("-", ""))))
    errs = 0
    for _p, r, code in notable[:MAX_8K_DETAIL]:
        url = filing_url(cik, r)
        try:
            resp = ctx.http_sec.get(url, timeout=30)
            if resp.status_code != 200:
                raise FetchError("HTTP {0}".format(resp.status_code))
            t = html_to_text(resp.text)
            m = re.search(r"item\s*{0}\b".format(re.escape(code)), t, re.I)
            seg = t[m.start():] if m else t
            # 去掉簽名頁之後
            seg = re.split(r"\n\s*SIGNATURE", seg, flags=re.I)[0]
            items.append(mk_item("SEC EDGAR", "8-K（{0}，Item {1}）".format(r["filingDate"], code), url, r["filingDate"],
                                 "8-K Item {0} {1}".format(code, ITEM_8K.get(code, "")), clip_to_weight(seg, 220)))
        except FetchError:
            errs += 1
    return {"axes": {"major_events": items}, "note": ("{0} 份 8-K 全文抓取失敗。".format(errs) if errs else "")}
