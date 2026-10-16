"""AI 融資事件紀錄：從早報證據帳本（docs/briefing/data/evidence_ledger.json）用關鍵字挑出融資事件，
去重後累積到 data/ai_credit/events.jsonl。

早報存檔實況：docs/briefing/YYYY-MM-DD.html 只有「市場」分頁，沒有新聞；新聞只在每天覆寫的
news.html 等分頁。機器可讀的新聞只有證據帳本 evidence_ledger.json（origin=briefing 的事實，
含標題 claim、摘要 detail、sources[{source,url,published}]，自 2026-09-23 起累積）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

# ---------------------------------------------------------------------------
# 關鍵字（常數）。規則：(基礎建設詞 或 公司名) 且 融資詞，或單獨命中特定片語。
# ---------------------------------------------------------------------------
INFRA_TERMS = [r"data ?cent(?:er|re)s?", r"\bGPUs?\b", r"AI infrastructure", r"AI compute", r"\bStargate\b", r"hyperscaler"]
NAME_TERMS = [r"CoreWeave", r"Oracle", r"OpenAI", r"\bxAI\b", r"Blue Owl", r"Nebius", r"Crusoe", r"Anthropic", r"SoftBank", r"SpaceX"]
FINANCE_TERMS = [
    r"\bfinanc(?:e|es|ed|ing)\b", r"\bbonds?\b", r"\bloans?\b", r"\bdebt\b", r"private credit", r"\bSPVs?\b", r"\bABS\b",
    r"asset-backed", r"\bleas(?:e|es|ed|ing)\b", r"credit facilit(?:y|ies)", r"\bborrow(?:s|ed|ing)?\b", r"securiti[sz]ation",
    r"off-balance", r"project finance", r"notes offering", r"debt offering", r"\bjunk\b", r"high-yield", r"credit default swap",
    r"\bCDS\b", r"term loan", r"\bconvertibles?\b", r"capital raise",
]
DIRECT_PHRASES = [r"GPU-backed", r"GPU-collateral", r"compute-backed", r"data ?cent(?:er|re)[- ]backed"]

_RX = lambda terms: re.compile("|".join(terms), re.I)  # noqa: E731
RX_INFRA, RX_NAME, RX_FIN, RX_DIRECT = _RX(INFRA_TERMS), _RX(NAME_TERMS), _RX(FINANCE_TERMS), _RX(DIRECT_PHRASES)
# ABS／CDS／SPV 大小寫敏感，避免 abs、cds 之類的字誤中
_RX_CASE = re.compile(r"\bABS\b|\bSPVs?\b|\bCDS\b")


def _terms(rx: re.Pattern, text: str) -> set[str]:
    return {m.group(0).lower() for m in rx.finditer(text)}


def _fin_terms(text: str) -> set[str]:
    fin = _terms(RX_FIN, text)
    # 大小寫敏感的縮寫：只認大寫，避免 abs、cds 之類誤中
    return {f for f in fin if f not in ("abs", "spv", "spvs", "cds") or _RX_CASE.search(text)}


def match_event(title: str, detail: str = "") -> list[str]:
    """回傳命中的關鍵字清單；空清單＝不是融資事件。

    規則：標題帶特定片語（GPU-backed 等）直接算；否則需要「基礎建設詞或公司名」與「融資詞」同時出現，
    且至少一邊在標題裡（避免只在摘要裡順帶提到的雜訊）。
    """
    direct = _terms(RX_DIRECT, title + " " + detail)
    if direct:
        return sorted(direct)
    a_t = _terms(RX_INFRA, title) | _terms(RX_NAME, title)
    a_d = _terms(RX_INFRA, detail) | _terms(RX_NAME, detail)
    f_t, f_d = _fin_terms(title), _fin_terms(detail)
    if (a_t and (f_t or f_d)) or (f_t and a_d):
        return sorted(a_t | a_d) + sorted(f_t | f_d)
    return []


def norm_url(u: str) -> str:
    if not u:
        return ""
    p = urlsplit(u.strip())
    return (p.netloc.lower() + p.path.rstrip("/")).lower()


def norm_title(t: str) -> str:
    return re.sub(r"[^0-9a-z一-鿿]+", "", (t or "").lower())


def _first_date(s: str | None) -> str | None:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s or "")
    return m.group(1) if m else None


def extract_candidates(ledger: dict) -> list[dict]:
    """證據帳本 → 命中關鍵字的候選事件（尚未去重）。只取早報來源（origin=briefing）。"""
    out = []
    for f in ledger.get("facts", []):
        if f.get("origin") != "briefing":
            continue
        title = (f.get("claim") or "").strip()
        hit = match_event(title, f.get("detail") or "")
        if not hit:
            continue
        srcs = f.get("sources") or []
        with_url = [s for s in srcs if s.get("url")]
        pick = with_url[0] if with_url else (srcs[0] if srcs else {})
        pubs = [d for d in (_first_date(s.get("published")) for s in srcs) if d]
        date = min(pubs) if pubs else (f.get("first_seen") or "")
        out.append({
            "date": date, "title": title, "source": pick.get("source") or "", "url": pick.get("url") or "",
            "first_seen": f.get("first_seen") or "", "matched": hit[:6],
        })
    return out


def merge_events(existing: list[dict], cands: list[dict]) -> tuple[list[dict], list[dict]]:
    """把候選併入既有紀錄，同網址或同標題視為重複。回傳 (全部紀錄, 新增紀錄)。"""
    urls = {norm_url(e.get("url", "")) for e in existing} - {""}
    titles = {norm_title(e.get("title", "")) for e in existing} - {""}
    added = []
    for c in cands:
        u, t = norm_url(c["url"]), norm_title(c["title"])
        if (u and u in urls) or (t and t in titles):
            continue
        if u:
            urls.add(u)
        if t:
            titles.add(t)
        added.append(c)
    return existing + added, added


def load_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def append_events(path: Path, added: list[dict]) -> None:
    if not added:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for e in added:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")


def latest(events: list[dict], n: int = 30) -> list[dict]:
    return sorted(events, key=lambda e: (e.get("date", ""), e.get("first_seen", "")), reverse=True)[:n]
