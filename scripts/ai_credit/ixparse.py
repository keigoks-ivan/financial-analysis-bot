"""讀 10-Q／10-K 內嵌 XBRL（含維度）。companyfacts 只有無維度的標準事實，
維度事實（如 OtherCommitment 的成員）與自訂 tag 要從申報檔本體解析。
"""
from __future__ import annotations

import html as _html
import re
import time

import requests

from sec_facts import CIKS, SEC_UA, fetch_submissions

_CTX_RE = re.compile(r"<(?:xbrli:)?context id=\"([^\"]+)\">(.*?)</(?:xbrli:)?context>", re.S)
_NF_RE = re.compile(r"<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>", re.S)


def contexts(h: str) -> dict[str, dict]:
    out = {}
    for m in _CTX_RE.finditer(h):
        body = m.group(2)
        dims = re.findall(r"<xbrldi:explicitMember dimension=\"([^\"]+)\">([^<]+)<", body)
        s = re.search(r"<(?:xbrli:)?startDate>([^<]+)<", body)
        e = re.search(r"<(?:xbrli:)?endDate>([^<]+)<", body)
        i = re.search(r"<(?:xbrli:)?instant>([^<]+)<", body)
        out[m.group(1)] = {
            "dims": [(a.strip(), b.strip()) for a, b in dims],
            "start": s.group(1) if s else None,
            "end": e.group(1) if e else None,
            "instant": i.group(1) if i else None,
        }
    return out


def parse_number(raw: str, scale: str | None, sign: str, fmt: str | None = None) -> float | None:
    txt = _html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
    if txt in ("—", "–", "-", "") or (fmt and ("zerodash" in fmt or "fixed-zero" in fmt)):
        val = 0.0
    else:
        t = txt.replace(",", "").replace("$", "").replace("%", "").strip()
        try:
            val = float(t)
        except ValueError:
            return None
    if scale:
        val *= 10 ** int(scale)
    return -val if sign == "-" else val


def facts(h: str, name_pat: str, ctxs: dict[str, dict] | None = None) -> list[dict]:
    """回傳 [{name, value, dims, start, end, instant}]；value 已乘上 scale 與正負號。"""
    ctxs = ctxs if ctxs is not None else contexts(h)
    pat = re.compile(name_pat)
    out = []
    for m in _NF_RE.finditer(h):
        a = m.group(1)
        nm = re.search(r"name=\"([^\"]+)\"", a)
        if not nm or not pat.search(nm.group(1)):
            continue
        cref = re.search(r"contextRef=\"([^\"]+)\"", a)
        c = ctxs.get(cref.group(1)) if cref else None
        if c is None:
            continue
        sc = re.search(r"scale=\"(-?\d+)\"", a)
        fm = re.search(r"format=\"([^\"]+)\"", a)
        val = parse_number(m.group(2), sc.group(1) if sc else None, "-" if 'sign="-"' in a else "", fm.group(1) if fm else None)
        if val is None:
            continue
        out.append({"name": nm.group(1), "value": val, "dims": c["dims"], "start": c["start"], "end": c["end"], "instant": c["instant"]})
    return out


def members(f: dict) -> frozenset[str]:
    return frozenset(m for _, m in f["dims"])


def pick_instant(fs: list[dict], name: str, need_members: set[str] | None) -> dict | None:
    """同 tag、維度成員集合恰等於 need_members（None＝不限定、空集合＝無維度）的最新時點事實。"""
    cand = [f for f in fs if f["name"] == name and f["instant"]
            and (need_members is None or members(f) == frozenset(need_members))]
    if not cand:
        return None
    last = max(f["instant"] for f in cand)
    return [f for f in cand if f["instant"] == last][0]


def latest_periodic(ticker: str) -> dict:
    """最新一份 10-Q／10-K 的 {accession, form, report_date, filing_date, url}。"""
    s = fetch_submissions(ticker)
    f = s["filings"]["recent"]
    cik = CIKS[ticker]
    for i, form in enumerate(f["form"]):
        if form in ("10-Q", "10-K"):
            acc = f["accessionNumber"][i]
            return {
                "accession": acc, "form": form, "report_date": f["reportDate"][i], "filing_date": f["filingDate"][i],
                "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{f['primaryDocument'][i]}",
            }
    raise RuntimeError(f"{ticker} 找不到 10-Q／10-K")


def fetch_html(url: str, tries: int = 3, timeout: int = 180) -> str:
    err = None
    for i in range(tries):
        try:
            r = requests.get(url, headers=SEC_UA, timeout=timeout)
            r.raise_for_status()
            return r.text
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"申報檔下載失敗 {url}：{err!r}")
