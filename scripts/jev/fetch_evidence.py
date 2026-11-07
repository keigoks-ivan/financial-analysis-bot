#!/usr/bin/env python3
"""Fetch a day's raw news evidence for one ticker, from broad free sources,
no new API keys. English text only (what gets summarized downstream goes to
Jev, whose CJK accuracy is lower — see questions_NVDA.json's own note).

Sources (each wrapped so one failing source never aborts the run):
  - yfinance Ticker(t).news
  - Google News RSS, one query per entry in scripts/jev/sources_<TICKER>.json
  - SEC EDGAR company 8-K filings (Atom), by CIK
  - the company newsroom RSS feed, if configured

Output: data/jev/raw/<TICKER>/<date>.json — deduped items (by url, then by
normalized headline), each tagged `seen_before` against a rolling 30-day
store at data/jev/seen/<TICKER>.json.

Usage:
  python3 scripts/jev/fetch_evidence.py --ticker NVDA [--date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from jev_common import (
    JEV_DIR, DATA_DIR, USER_AGENT, http_get, strip_html, normalize_headline,
    rfc822_to_iso, sha_id, load_json, atomic_json, now_iso, today_str,
)

ALLOWED_HOSTS = {"news.google.com", "www.sec.gov", "nvidianews.nvidia.com"}
# A recurring story (same url or headline seen in the last N days) still
# gets tagged, but clean_evidence.py's importance formula discounts it —
# see NOVELTY_SEEN_BEFORE there. This constant only controls the window.
SEEN_WINDOW_DAYS = 30
GOOGLE_NEWS_QUERY_PAUSE_SEC = 0.3  # politeness between queries to the same host
DEFAULT_MAX_ITEMS_PER_QUERY = 8
DEFAULT_MAX_SEC_ITEMS = 10
DEFAULT_MAX_NEWSROOM_ITEMS = 10
DESCRIPTION_CHARS = 400  # how much of an RSS <description> we keep as `text`


def fetch_yfinance_news(ticker):
    import yfinance as yf  # imported lazily so other sources still work if this errors
    items = []
    raw = yf.Ticker(ticker).news or []
    for entry in raw:
        c = entry.get("content", entry)
        url = ((c.get("canonicalUrl") or {}).get("url")
               or (c.get("clickThroughUrl") or {}).get("url"))
        headline = (c.get("title") or "").strip()
        if not url or not headline:
            continue
        text = strip_html(c.get("summary") or c.get("description") or "")
        provider = (c.get("provider") or {}).get("displayName") or "Yahoo Finance"
        items.append({"url": url, "headline": headline, "text": text,
                      "source": provider, "published": c.get("pubDate", ""),
                      "channel": "yfinance_news"})
    return items


def fetch_google_news(query, max_items, channel):
    url = "https://news.google.com/rss/search?" + urlencode(
        {"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
    body = http_get(url, allowed_hosts=ALLOWED_HOSTS)
    root = ET.fromstring(body)
    items = []
    for it in root.findall(".//item")[:max_items]:
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        if not title or not link:
            continue
        src_el = it.find("source")
        src_name = (src_el.text or "").strip() if src_el is not None else "Google News"
        suffix = " - " + src_name
        if src_name and title.endswith(suffix):
            title = title[: -len(suffix)].strip()
        desc = strip_html(it.findtext("description") or "")[:DESCRIPTION_CHARS]
        items.append({"url": link, "headline": title, "text": desc,
                      "source": src_name or "Google News",
                      "published": rfc822_to_iso(it.findtext("pubDate") or ""),
                      "channel": channel})
    return items


ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch_sec_8k(cik, max_items=DEFAULT_MAX_SEC_ITEMS):
    url = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + cik
           + "&type=8-K&dateb=&owner=include&count=" + str(max_items) + "&output=atom")
    body = http_get(url, allowed_hosts=ALLOWED_HOSTS)
    root = ET.fromstring(body)
    items = []
    for entry in root.findall("a:entry", ATOM_NS)[:max_items]:
        link_el = entry.find("a:link", ATOM_NS)
        link = link_el.get("href") if link_el is not None else ""
        if not link:
            continue
        content = entry.find("a:content", ATOM_NS)
        items_desc = (content.findtext("a:items-desc", "", ATOM_NS) if content is not None else "").strip()
        form_name = (content.findtext("a:form-name", "", ATOM_NS) if content is not None else "").strip()
        filing_date = (content.findtext("a:filing-date", "", ATOM_NS) if content is not None else "").strip()
        updated = (entry.findtext("a:updated", "", ATOM_NS) or "").strip()
        summary = strip_html(entry.findtext("a:summary", "", ATOM_NS))
        headline = "NVIDIA 8-K: " + (items_desc or form_name or "filing")
        items.append({"url": link, "headline": headline, "text": summary,
                      "source": "SEC EDGAR", "published": updated or filing_date,
                      "channel": "sec_8k"})
    return items


_ALT_RSS_RE = re.compile(
    r'<link[^>]*rel="alternate"[^>]*type="application/rss\+xml"[^>]*href="([^"]+)"', re.I)


def fetch_newsroom_rss(url, max_items=DEFAULT_MAX_NEWSROOM_ITEMS):
    body = http_get(url, allowed_hosts=ALLOWED_HOSTS)
    if not body.lstrip().startswith("<?xml") and "<rss" not in body[:400]:
        # Some newsroom RSS "hub" pages (e.g. nvidianews.nvidia.com/rss) are
        # landing pages that link to the actual feed; follow that once.
        m = _ALT_RSS_RE.search(body)
        if not m:
            raise ValueError("newsroom page has no discoverable rss+xml link")
        body = http_get(m.group(1), allowed_hosts=ALLOWED_HOSTS)
    root = ET.fromstring(body)
    items = []
    for it in root.findall(".//item")[:max_items]:
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        if not title or not link:
            continue
        desc = strip_html(it.findtext("description") or "")[:DESCRIPTION_CHARS]
        items.append({"url": link, "headline": title, "text": desc,
                      "source": "NVIDIA Newsroom",
                      "published": rfc822_to_iso(it.findtext("pubDate") or ""),
                      "channel": "newsroom_rss"})
    return items


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def collect_raw(cfg, ticker, sleep=time.sleep):
    """Call every configured source; one failure never aborts the run.
    Returns (all_items, statuses). Kept separate from main() so tests can
    exercise it with monkeypatched fetchers and no network."""
    all_items, statuses = [], []

    def record(source_id, fn):
        try:
            got = fn()
            all_items.extend(got)
            statuses.append({"id": source_id, "status": "ok", "count": len(got)})
        except Exception as exc:  # one bad source must not sink the run
            statuses.append({"id": source_id, "status": "error", "count": 0,
                              "reason": str(exc)[:300]})

    record("yfinance_news", lambda: fetch_yfinance_news(ticker))
    max_per_query = cfg.get("max_items_per_query", DEFAULT_MAX_ITEMS_PER_QUERY)
    for q in cfg.get("google_news_queries", []):
        channel = "google_news:" + slugify(q)
        record(channel, lambda q=q, channel=channel: fetch_google_news(q, max_per_query, channel))
        sleep(GOOGLE_NEWS_QUERY_PAUSE_SEC)
    if cfg.get("cik"):
        record("sec_8k", lambda: fetch_sec_8k(cfg["cik"]))
    if cfg.get("newsroom_rss"):
        record("newsroom_rss", lambda: fetch_newsroom_rss(cfg["newsroom_rss"]))
    return all_items, statuses


def dedup_items(items):
    """Dedup within the day: first by exact url, then by normalized
    headline. First occurrence wins (yfinance, then Google queries in
    config order, then SEC, then newsroom)."""
    seen_urls, seen_heads, out = set(), set(), []
    for it in items:
        url = it["url"]
        head_norm = normalize_headline(it["headline"])
        if url in seen_urls or (head_norm and head_norm in seen_heads):
            continue
        seen_urls.add(url)
        if head_norm:
            seen_heads.add(head_norm)
        out.append(it)
    return out


def finalize_items(deduped, seen_store, date, fetched_at):
    """Assign ids, mark seen_before against the rolling store, and return
    the updated store (pruned to SEEN_WINDOW_DAYS). Pure aside from not
    touching disk, so it's directly testable."""
    cutoff = (datetime.strptime(date, "%Y-%m-%d").date() - timedelta(days=SEEN_WINDOW_DAYS)).isoformat()
    ids = {k: v for k, v in seen_store.get("ids", {}).items() if v >= cutoff}
    final_items = []
    for it in deduped:
        item_id = sha_id(it["url"])
        seen_before = item_id in ids
        if not seen_before:
            ids[item_id] = date
        final_items.append({
            "id": item_id, "fetched_at": fetched_at, "published": it.get("published", ""),
            "source": it["source"], "url": it["url"], "headline": it["headline"],
            "text": it.get("text", ""), "channel": it.get("channel", ""),
            "seen_before": seen_before,
        })
    final_items.sort(key=lambda x: x["published"], reverse=True)
    updated_store = {"schema": "jev-seen-v1", "ticker": seen_store.get("ticker"), "ids": ids}
    return final_items, updated_store


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--date", default=None, help="defaults to today (UTC)")
    a = ap.parse_args()
    date = a.date or today_str()

    cfg = load_json(JEV_DIR / f"sources_{a.ticker}.json")
    if cfg is None:
        sys.exit(f"missing scripts/jev/sources_{a.ticker}.json")

    all_items, statuses = collect_raw(cfg, a.ticker)
    deduped = dedup_items(all_items)

    seen_path = DATA_DIR / "seen" / f"{a.ticker}.json"
    seen_store = load_json(seen_path, {"schema": "jev-seen-v1", "ticker": a.ticker, "ids": {}})
    fetched_at = now_iso()
    final_items, updated_store = finalize_items(deduped, seen_store, date, fetched_at)
    atomic_json(seen_path, updated_store)

    out = {
        "schema": "jev-evidence-raw-v1", "ticker": a.ticker, "date": date,
        "generated_at": fetched_at, "sources": statuses,
        "raw_count": len(all_items), "deduped_count": len(final_items),
        "items": final_items,
    }
    out_path = DATA_DIR / "raw" / a.ticker / f"{date}.json"
    atomic_json(out_path, out)

    ok = sum(s["status"] == "ok" for s in statuses)
    errors = [s for s in statuses if s["status"] == "error"]
    seen_before_n = sum(i["seen_before"] for i in final_items)
    print(f"fetch_evidence: ticker={a.ticker} date={date} sources_ok={ok}/{len(statuses)} "
          f"raw={len(all_items)} deduped={len(final_items)} seen_before={seen_before_n}")
    for s in errors:
        print(f"  FAILED {s['id']}: {s['reason']}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
