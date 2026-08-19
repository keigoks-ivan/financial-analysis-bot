#!/usr/bin/env python3
"""scripts/intel/sec_filings.py — SEC EDGAR 8-K filings, filtered to the
site's ticker universe. 對應 notes/site-internal/intel/DESIGN.md §5（個股層
一手來源：SEC 8-K 按 item 分類）／§6（零 LLM 原則）。

設計：EDGAR 的 `getcurrent` atom feed 是「全市場最新 N 筆」，不是「查某公司」
——所以先建站內 ticker universe（dd-meta 全部 ticker ∪ id-meta 全部
related_tickers[].ticker，不限 dca_verdict，因為一筆 8-K 值得浮出來的門檻是
「這檔在站上被研究過」，不是「目前判進場」），再用 SEC 官方 `company_tickers.json`
把 ticker 轉成 CIK（10 碼零填），逐筆比對 feed 裡每筆申報附帶的 CIK——不做公司
名稱模糊比對（名稱格式在 EDGAR 端不穩定，如 "NVIDIA CORP" vs "NVIDIA
Corporation"，CIK 是唯一穩定鍵）。海外掛牌（.TW/.KL/.DE…）在 company_tickers.json
裡查不到 CIK，正常被跳過（它們對美國 SEC 而言多半是 20-F/6-K 申報人，不在
getcurrent 的 8-K 清單裡）。

輸出卡片 kind="data"（結構化、已知 ticker，不需要 haiku 判斷 relevant/level/
category——見 classify.py classify_data_card），level="company"，
category="filing"，zero LLM cost。

SEC 要求所有 request 的 User-Agent 帶聯絡方式（不遵守會被暫時封鎖），此模組
自己開一個 UA 常數，跟 fetch.py 全站共用的 UA 不同，不共用 fetch.py 的
http_get()（避免循環 import：fetch.py 要 import 本檔來 dispatch kind=="sec_8k"）。

呼叫入口（供 fetch.py dispatch_source() 使用）：
    fetch_sec_8k_source(source: dict, health: Health) -> list[dict]
"""
from __future__ import annotations

import html
import json
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
DD_DIR = ROOT / "docs" / "dd"
ID_DIR = ROOT / "docs" / "id"
DATA_DIR = ROOT / "docs" / "intel" / "data"
TICKER_MAP_CACHE = DATA_DIR / "sec_ticker_map.json"

# SEC 要求聯絡方式，見 https://www.sec.gov/os/webmaster-faq#developers 。
# 刻意跟 fetch.py 的全站 UA 不同（那個沒有 email，怕被 EDGAR 的較嚴格規則擋）。
UA = "IntelBot/1.0 (research.investmquest.com; keigoks@gmail.com)"
TIMEOUT = 12
TICKER_MAP_TTL_DAYS = 7
MAX_CARDS_PER_DAY = 20

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL
)
ID_META_RE = re.compile(
    r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL
)
FEED_ENTRY_TITLE_RE = re.compile(
    r"^(8-K(?:/A)?)\s*-\s*(.+?)\s*\((\d{10})\)\s*\(Filer\)\s*$"
)
# 摘要在 strip_html() 之後 <br> 換行已被壓成單行空白，各 Item 段落之間沒有分隔
# 字元，所以用「lookahead 到下一個 'Item X.X:' 或字串結尾」而非貪婪吃到行尾，
# 否則第一個 item 的 label 會把後面所有 item 一起吃掉（曾經踩過這個 bug）。
ITEM_RE = re.compile(
    r"Item\s+([\d]+\.[\d]+):\s*(.+?)(?=\s*Item\s+[\d]+\.[\d]+:|$)"
)


def _http_get(url: str, ua: str = UA, timeout: int = TIMEOUT):
    """回傳 (ok, status, latency_ms, text_or_None, error_or_None)。單次嘗試、
    不重試——EDGAR 對過度重試的行為特別敏感（會 rate-limit UA），寧可這次
    健康檢查標失敗，下次排程再試。"""
    t0 = time.time()
    try:
        resp = requests.get(url, headers={"User-Agent": ua, "Accept": "*/*"}, timeout=timeout)
        latency_ms = int((time.time() - t0) * 1000)
        if resp.status_code >= 400:
            return False, resp.status_code, latency_ms, None, f"HTTP {resp.status_code}"
        return True, resp.status_code, latency_ms, resp.text, None
    except requests.RequestException as e:
        latency_ms = int((time.time() - t0) * 1000)
        return False, None, latency_ms, None, str(e)[:200]


def _strip(text: str, limit: int = 400) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def _load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


# ── ticker -> CIK（SEC 官方 company_tickers.json，週快取）──────────────────
def _fetch_ticker_map() -> dict | None:
    ok, _status, _latency, text, _err = _http_get(
        "https://www.sec.gov/files/company_tickers.json"
    )
    if not ok:
        return None
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return None
    # raw: {"0": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA CORP"}, ...}
    out = {}
    for row in raw.values():
        t = (row.get("ticker") or "").upper()
        cik = row.get("cik_str")
        if t and cik is not None:
            out[t] = {"cik": f"{int(cik):010d}", "title": row.get("title", "")}
    return out


def load_ticker_cik_map() -> dict:
    """ticker(upper) -> {"cik": "0001045810", "title": "NVIDIA CORP"}。快取在
    docs/intel/data/sec_ticker_map.json，7 天內重用；抓失敗時退回舊快取（有
    總比沒有好——這只是查表用，不影響 SEC 官方資料的正確性）。"""
    cached = _load_json(TICKER_MAP_CACHE)
    if cached:
        fetched_at = cached.get("fetched_at", "")
        try:
            age_days = (
                datetime.now(timezone.utc)
                - datetime.strptime(fetched_at, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=timezone.utc
                )
            ).days
        except ValueError:
            age_days = 999
        if age_days < TICKER_MAP_TTL_DAYS and cached.get("map"):
            return cached["map"]

    fresh = _fetch_ticker_map()
    if fresh:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        TICKER_MAP_CACHE.write_text(
            json.dumps(
                {
                    "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "map": fresh,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return fresh
    if cached and cached.get("map"):
        return cached["map"]  # stale but better than nothing
    return {}


# ── 站內 ticker universe（dd-meta ∪ id-meta related_tickers）───────────────
def load_site_ticker_universe() -> set:
    """全部 dd-meta ticker ∪ 全部 id-meta related_tickers[].ticker，大寫正規化。
    不做 verdict 篩選——見模組 docstring。"""
    tickers = set()
    if DD_DIR.exists():
        for p in DD_DIR.glob("DD_*.html"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            m = DD_META_RE.search(text)
            if not m:
                continue
            try:
                d = json.loads(m.group(1).strip())
            except json.JSONDecodeError:
                continue
            t = d.get("ticker")
            if t:
                tickers.add(t.upper())
    if ID_DIR.exists():
        for p in ID_DIR.glob("*.html"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            m = ID_META_RE.search(text)
            if not m:
                continue
            try:
                d = json.loads(m.group(1).strip())
            except json.JSONDecodeError:
                continue
            for row in d.get("related_tickers") or []:
                t = (row or {}).get("ticker")
                if t:
                    tickers.add(t.upper())
    return tickers


def _cik_lookup_for_universe() -> dict:
    """回傳 {cik(10碼零填): {"ticker":..., "title":...}} 只含站內 universe 且
    能在 SEC company_tickers.json 查到的 ticker（美股／可查 CIK 的掛牌；
    .TW/.KL/.DE 等海外掛牌預期查不到，正常被跳過）。"""
    universe = load_site_ticker_universe()
    ticker_map = load_ticker_cik_map()
    out = {}
    for t in universe:
        row = ticker_map.get(t)
        if row:
            out[row["cik"]] = {"ticker": t, "title": row["title"]}
    return out


# ── EDGAR getcurrent atom feed 解析 ─────────────────────────────────────────
_ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


def _parse_entry(entry) -> dict | None:
    title_raw = (entry.findtext("a:title", namespaces=_ATOM_NS) or "").strip()
    m = FEED_ENTRY_TITLE_RE.match(title_raw)
    if not m:
        return None
    form_type, company, cik = m.group(1), m.group(2).strip(), m.group(3)
    link_el = entry.find("a:link", namespaces=_ATOM_NS)
    url = link_el.get("href") if link_el is not None else ""
    summary_raw = entry.findtext("a:summary", namespaces=_ATOM_NS) or ""
    summary_clean = _strip(summary_raw, limit=600)
    items = ITEM_RE.findall(summary_clean)
    updated_raw = (entry.findtext("a:updated", namespaces=_ATOM_NS) or "").strip()
    published_at = None
    if updated_raw:
        try:
            dt = datetime.fromisoformat(updated_raw)
            published_at = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            published_at = None
    return {
        "form_type": form_type,
        "company": company,
        "cik": cik,
        "url": url,
        "items": items,  # list[(item_no, item_label)]
        "published_at": published_at,
    }


def fetch_sec_8k_source(source: dict, health) -> list[dict]:
    """dispatch_source() 對 kind=="sec_8k" 的實作。health 是 fetch.py 的
    Health 實例（duck-typed：只用 .record(...)）。"""
    sid = source["id"]
    ok, status, latency_ms, text, err = _http_get(source["url"])
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        health.record(sid, False, status, latency_ms, 0, f"bad xml: {e}")
        return []

    entries = root.findall("a:entry", namespaces=_ATOM_NS)
    parsed = [e for e in (_parse_entry(en) for en in entries) if e]
    health.record(sid, True, status, latency_ms, len(parsed))

    cik_lookup = _cik_lookup_for_universe()
    if not cik_lookup:
        # ticker→CIK 對照表拿不到（company_tickers.json 抓失敗且無快取）：
        # 誠實回空，不要在沒有比對表的情況下瞎猜「全部保留」或「全部丟棄」。
        return []

    cards = []
    for row in parsed:
        # 兩邊（EDGAR feed 的 CIK、company_tickers.json 算出的 CIK）都是 10 碼零填字串，直接比對。
        hit = cik_lookup.get(row["cik"])
        if not hit:
            continue
        item_labels = [f"{no} {label.strip()}" for no, label in row["items"]]
        items_txt = "；".join(item_labels[:3]) if item_labels else row["form_type"]
        title = f"[8-K] {row['company']} — {items_txt}"
        cards.append(
            {
                "kind": "data",
                "level": "company",
                "category": "filing",
                "source_tier": source["tier"],
                "source_id": sid,
                "title": title[:220],
                "url": row["url"],
                "published_at": row["published_at"],
                "lang": "en",
                "summary_raw": items_txt,
                "tags": {"tickers": [hit["ticker"]], "themes": []},
                "data": {
                    "cik": row["cik"],
                    "form_type": row["form_type"],
                    "items": item_labels,
                },
            }
        )
        if len(cards) >= min(MAX_CARDS_PER_DAY, source.get("max_items", MAX_CARDS_PER_DAY)):
            break
    return cards


if __name__ == "__main__":
    # 獨立除錯：python3 scripts/intel/sec_filings.py
    class _FakeHealth:
        def record(self, *a, **k):
            print("[health]", a, k)

    src = {
        "id": "sec_edgar_8k",
        "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&output=atom",
        "tier": "T1",
        "max_items": 20,
    }
    out = fetch_sec_8k_source(src, _FakeHealth())
    print(f"{len(out)} cards")
    for c in out[:5]:
        print(" -", c["title"], "|", c["url"])
