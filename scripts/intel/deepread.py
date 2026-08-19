#!/usr/bin/env python3
"""scripts/intel/deepread.py — 重要卡讀全文（deep read）。

對應 notes/site-internal/intel/DESIGN.md 2026-08-19「加料」計畫第 1 項。選
今天 ≤12 張最重要的已摘要新聞卡（importance 3 優先，其餘 importance 2 依
corroboration desc / tier asc），機械抓取文章 HTML、抽正文（優先 `<article>`，
否則抓 `<p>` 標籤最密集的父節點），再用 sonnet 讀全文抽出結構化重點——比
40–90 字的日常摘要更深一層：文中真的出現的數字、實體標籤、事實取向要點、
接下來該看什麼。

零 LLM 部分（選卡、抓取、抽正文、數字核對）全部 Python 決定性；LLM 只做
「讀懂正文寫結構化重點」這一件事，一批最多 4 篇，走獨立的 ledger bucket
`"deepread"`（見 llm.py `ledger_key`），不跟 classify/summarize 的 sonnet
額度搶。

Wire-in：run_daily.py 在 summarize + finalize_card 之後、build_digest 之前
呼叫 `run_deepread(finalized_cards, ledger)`——finalized_cards 已經是最終輸出
schema 的 dict，本模組直接在原地加 `card["deep"]` / `card["deep_status"]`。

失敗策略：任何一步失敗（網路、剖析、LLM、數字核對不過）只讓該張卡的
`deep_status` 標記對應狀態，絕不讓整條 pipeline 掛掉（同 DESIGN §6 rule 3
「寧可漏不爆額度」的精神）。

CLI（除錯用）：
    python3 scripts/intel/deepread.py --data /path/to/daily.json --out /tmp/deepread-debug.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urlparse

try:
    import requests
except ImportError:  # pragma: no cover — requests 已是 fetch.py 既有依賴
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover — beautifulsoup4 已是站內既有依賴（yfinance 帶入）
    BeautifulSoup = None

from common import load_json, read_prompt
from llm import Ledger, run_claude

FETCH_TIMEOUT = 12
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
MAX_CANDIDATES = 12
BATCH_SIZE = 4
MAX_CHARS = 6000
MIN_CHARS = 600

# DESIGN：已知付費牆或需要解析才能用的網域——寧可漏不爆額度，不硬抓一定拿不到
# 正文的來源。news.google.com 是 RSS 導回連結（redirect），沒有 resolve 步驟
# 就直接跳過（"unless resolved"，本版不做 resolve）。
BLOCKED_DOMAINS = {
    "ft.com", "www.ft.com",
    "wsj.com", "www.wsj.com",
    "bloomberg.com", "www.bloomberg.com",
    "economist.com", "www.economist.com",
    "nytimes.com", "www.nytimes.com",
    "barrons.com", "www.barrons.com",
    "news.google.com",
}

DEEPREAD_SYSTEM = None


def _system_prompt() -> str:
    global DEEPREAD_SYSTEM
    if DEEPREAD_SYSTEM is None:
        DEEPREAD_SYSTEM = read_prompt("deepread.md")
    return DEEPREAD_SYSTEM


# ── candidate selection ─────────────────────────────────────────────────────
def _domain(url: str) -> str:
    try:
        return (urlparse(url).netloc or "").lower()
    except ValueError:
        return ""


def _is_blocked_domain(url: str) -> bool:
    dom = _domain(url)
    if not dom:
        return True
    if dom in BLOCKED_DOMAINS:
        return True
    return any(dom == d or dom.endswith("." + d) for d in BLOCKED_DOMAINS)


_TIER_RANK = {"T1": 0, "T2": 1, "T3": 2, "T4": 3}


def select_candidates(cards: list[dict], limit: int = MAX_CANDIDATES) -> list[dict]:
    """importance 3 優先，其餘 importance 2 依 corroboration desc / tier asc；
    只挑 kind!=data（站內數字卡零文章可讀）、summarized=True（真的進過 sonnet
    摘要，不是 title-only passthrough）、且網域不在付費牆黑名單裡的卡片。"""
    pool = []
    for c in cards:
        if c.get("kind") == "data":
            continue
        if c.get("is_rumor"):  # 2026-08-20 傳聞層試行：傳聞卡不得進深讀
            continue
        if not c.get("summarized"):
            continue
        if int(c.get("importance") or 0) < 2:
            continue
        url = c.get("url") or ""
        if not url or _is_blocked_domain(url):
            continue
        pool.append(c)

    def sort_key(c):
        imp = int(c.get("importance") or 1)
        corrob = int(c.get("corroboration") or 1)
        tier = _TIER_RANK.get(c.get("source_tier"), 9)
        return (-imp, -corrob, tier)

    pool.sort(key=sort_key)
    return pool[:limit]


# ── fetch + extract ─────────────────────────────────────────────────────────
def extract_main_text(html_text: str) -> str:
    """優先 `<article>` 裡的 `<p>` 全文；沒有或太短就退而求其次抓全頁 `<p>`
    標籤依父節點分組後、文字總長最大的那一組（「密集的 `<p>` 群」）。"""
    if BeautifulSoup is None or not html_text:
        return ""
    soup = BeautifulSoup(html_text, "lxml")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript", "iframe"]):
        tag.decompose()

    article = soup.find("article")
    if article is not None:
        text = "\n".join(
            t for t in (p.get_text(" ", strip=True) for p in article.find_all("p")) if t
        )
        if len(text) >= MIN_CHARS:
            return text[:MAX_CHARS]

    parent_len: dict = {}
    parent_ps: dict = {}
    for p in soup.find_all("p"):
        t = p.get_text(" ", strip=True)
        if not t:
            continue
        parent = p.parent
        if parent is None:
            continue
        key = id(parent)
        parent_len[key] = parent_len.get(key, 0) + len(t)
        parent_ps.setdefault(key, []).append(t)
    if not parent_len:
        return ""
    best_key = max(parent_len, key=lambda k: parent_len[k])
    return "\n".join(parent_ps[best_key])[:MAX_CHARS]


def fetch_article(url: str) -> tuple[str, str]:
    """Returns (text, status) — status ∈ {"ok","paywall","fail"}。<600 字視為
    大概率遇到付費牆／同意頁（DESIGN 原文用詞），不是抓取失敗。"""
    if requests is None or BeautifulSoup is None:
        print("[intel/deepread] missing dependency: requests/beautifulsoup4 — all deep reads skipped",
              file=sys.stderr)
        return "", "fail"
    try:
        resp = requests.get(
            url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*"},
            timeout=FETCH_TIMEOUT,
        )
    except requests.RequestException:
        return "", "fail"
    if resp.status_code != 200 or not resp.text:
        return "", "fail"
    try:
        text = extract_main_text(resp.text)
    except Exception:  # noqa: BLE001 — 剖析失敗不可讓整條 pipeline 掛掉
        return "", "fail"
    if len(text) < MIN_CHARS:
        return text, "paywall"
    return text, "ok"


# ── validation ───────────────────────────────────────────────────────────────
def _plain_text(s, limit: int) -> str:
    if not isinstance(s, str):
        return ""
    s = re.sub(r"<[^>]+>", "", s).strip()
    return s[:limit]


def _digits_only(s: str) -> str:
    return re.sub(r"[^\d]", "", s or "")


def _number_supported(value: str, text: str) -> bool:
    """DESIGN 硬規則：every number value string must appear in the text
    (substring match on digits)。先試逐字子字串，再退而求其次比對純數字序列
    （容忍千分位逗號、單位差異），兩者皆不過就丟掉這個數字。"""
    value = (value or "").strip()
    if not value or not text:
        return False
    if value in text:
        return True
    vd = _digits_only(value)
    if not vd:
        return False
    return vd in _digits_only(text)


def _validate_deep_result(result: "dict | None", text: str) -> "dict | None":
    if not isinstance(result, dict):
        return None
    numbers = []
    for n in (result.get("numbers") or [])[:6]:
        if not isinstance(n, dict):
            continue
        what = _plain_text(n.get("what"), 30)
        value = _plain_text(n.get("value"), 24)
        period = _plain_text(n.get("period"), 20)
        if not what or not value:
            continue
        if not _number_supported(value, text):
            continue
        numbers.append({"what": what, "value": value, "period": period})

    entities_raw = result.get("entities") or {}
    if not isinstance(entities_raw, dict):
        entities_raw = {}

    def _str_list(key, item_limit, n_limit):
        vals = entities_raw.get(key)
        if not isinstance(vals, list):
            return []
        out = []
        for v in vals[:n_limit]:
            if isinstance(v, str) and v.strip():
                out.append(v.strip()[:item_limit])
        return out

    entities = {
        "tickers": _str_list("tickers", 12, 8),
        "themes": _str_list("themes", 20, 8),
        "countries": _str_list("countries", 12, 6),
    }

    takeaway = _plain_text(result.get("takeaway_zh"), 60)
    watch = _plain_text(result.get("watch_zh"), 40)
    confidence = result.get("confidence")
    if confidence not in ("high", "med", "low"):
        confidence = "low"

    if not takeaway:
        return None
    return {
        "numbers": numbers,
        "entities": entities,
        "takeaway_zh": takeaway,
        "watch_zh": watch,
        "confidence": confidence,
    }


# ── LLM batch ────────────────────────────────────────────────────────────────
def _batch_input(items: list[tuple[dict, str]]) -> list[dict]:
    out = []
    for c, text in items:
        out.append({
            "id": c["id"],
            "title": (c.get("title") or "")[:200],
            "source": c.get("source_name") or "",
            "url": c.get("url") or "",
            "text": text,
        })
    return out


def run_deepread(cards: list[dict], ledger: Ledger) -> dict:
    """對 `cards`（已 finalize 的卡片 dict list）原地加 `deep` / `deep_status`。
    只影響被選中的 ≤12 張候選卡；其餘卡片完全不動（不加任何 deep 相關欄位）。"""
    candidates = select_candidates(cards)
    by_id = {c["id"]: c for c in candidates}
    status_map: dict = {}
    fetched: dict = {}

    for c in candidates:
        text, status = fetch_article(c.get("url") or "")
        status_map[c["id"]] = status
        if status == "ok":
            fetched[c["id"]] = text

    ok_ids = list(fetched.keys())
    llm_calls, llm_failures = 0, 0
    for i in range(0, len(ok_ids), BATCH_SIZE):
        batch_ids = ok_ids[i:i + BATCH_SIZE]
        batch_items = [(by_id[cid], fetched[cid]) for cid in batch_ids]
        payload = json.dumps(_batch_input(batch_items), ensure_ascii=False)
        parsed, usage = run_claude(
            system=_system_prompt(),
            user=payload,
            model="sonnet",
            label=f"deepread batch {i // BATCH_SIZE + 1}",
            ledger=ledger,
            card_count=len(batch_items),
            ledger_key="deepread",
        )
        if parsed is None or not isinstance(parsed, list):
            if usage.get("capped"):
                for cid in batch_ids:
                    status_map[cid] = "skipped"
            else:
                llm_failures += 1
                for cid in batch_ids:
                    status_map[cid] = "fail"
            continue
        llm_calls += 1
        result_by_id = {r["id"]: r for r in parsed if isinstance(r, dict) and r.get("id")}
        for cid in batch_ids:
            raw = result_by_id.get(cid)
            validated = _validate_deep_result(raw, fetched[cid]) if raw else None
            if validated:
                by_id[cid]["deep"] = validated
                status_map[cid] = "ok"
            else:
                status_map[cid] = "fail"

    for c in candidates:
        c["deep_status"] = status_map.get(c["id"], "fail")

    log = {
        "candidates": len(candidates),
        "fetched_ok": len(fetched),
        "llm_batches_ok": llm_calls,
        "llm_batches_failed": llm_failures,
        "final_status": {
            s: sum(1 for v in status_map.values() if v == s)
            for s in ("ok", "paywall", "fail", "skipped")
        },
    }
    print(f"[intel/deepread] {json.dumps(log, ensure_ascii=False)}", file=sys.stderr)
    return log


# ── CLI (debug/verification only) ───────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="path to a daily.json (with 'cards')")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    payload = load_json(args.data)
    if payload is None:
        print(f"data file not found: {args.data}", file=sys.stderr)
        return 1
    cards = payload.get("cards", [])

    ledger = Ledger()
    log = run_deepread(cards, ledger)
    log["ledger"] = ledger.to_status_dict()

    out_path = args.out or "/tmp/intel-deepread-debug.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"log": log, "cards": [c for c in cards if c.get("deep_status")]}, f,
                   ensure_ascii=False, indent=2)
    print(f"[intel/deepread] wrote {out_path}")
    print(f"[intel/deepread] {json.dumps(log, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
