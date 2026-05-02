"""
web_fallback.py — WebSearch + WebFetch fallback for evidence pool.

This module is designed to be called from within a Claude Code agent session
where WebSearch and WebFetch tools are available.  It is NOT a standalone
command-line fetcher — it exposes Python functions that the orchestrator or
an agent session can call.

Trigger condition (per spec §3):
    Only run after Tier 1 (EDGAR), Tier 2 (IR fetcher), and Tier 3 (arXiv)
    have all returned zero results for the query.

Query patterns (from spec §3):
    "<company> investor day 2026 filetype:pdf site:investor.<domain>"
    "<ticker> earnings call presentation 2026Q1 filetype:pdf"

Design intent:
    - Called by orchestrator.py when fetch_for_ticker() or fetch_for_topic()
      gets zero hits from Tiers 1-3.
    - Returns a list of candidate PDF URLs for the agent session to review
      and selectively download (the agent uses WebFetch to retrieve PDFs
      that look promising).
    - Does NOT auto-download everything found — IR PDFs from unknown sites
      may have access restrictions; human-in-the-loop review is preferred.

Usage (from orchestrator or interactive session):
    from scripts.evidence.web_fallback import search_for_ticker, search_for_topic

    candidates = search_for_ticker("AVGO", "Broadcom Inc.", year=2026)
    candidates = search_for_topic(["HBM", "high bandwidth memory"], year=2026)

Note on WebSearch / WebFetch:
    These Claude Code built-in tools are NOT available as Python importable
    functions outside an active Claude Code agent session.  This module
    provides the query construction logic and result parsing so the agent
    can call the tools with correctly-formed queries.  The actual tool calls
    are issued by the orchestrator or inline agent session code.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "evidence"
IR_DECKS_DIR = EVIDENCE_DIR / "ir_decks"
MANIFEST_PATH = EVIDENCE_DIR / "manifest.jsonl"
TICKERS_PATH = EVIDENCE_DIR / "tickers.json"


# ---------------------------------------------------------------------------
# Query builders
# ---------------------------------------------------------------------------

def build_ticker_queries(ticker: str, company_name: str, year: int = 2026) -> list[str]:
    """
    Build search query strings for a given ticker/company.
    Returns a list of queries to try in order (most specific first).
    """
    return [
        f'"{company_name}" investor day {year} filetype:pdf',
        f'"{company_name}" capital markets day {year} presentation filetype:pdf',
        f'"{ticker}" earnings call presentation {year}Q1 filetype:pdf',
        f'"{ticker}" earnings presentation {year} quarterly results',
        f'"{company_name}" {year} annual meeting presentation filetype:pdf',
    ]


def build_topic_queries(keywords: list[str], year: int = 2026) -> list[str]:
    """
    Build search query strings for a topic / set of keywords.
    Returns a list of queries to try.
    """
    joined = " ".join(f'"{kw}"' for kw in keywords[:2])  # quote top 2 keywords
    return [
        f"{joined} semiconductor {year} investor presentation filetype:pdf",
        f"{joined} earnings call {year} supply demand outlook",
        f"{joined} technology roadmap {year} analyst day filetype:pdf",
    ]


def build_ir_domain_query(
    ticker: str,
    company_name: str,
    ir_domain: str,
    year: int = 2026,
) -> str:
    """
    Build a site:-scoped query for a known IR domain.
    Example: site:investor.nvidia.com NVDA investor day 2026 filetype:pdf
    """
    return f'site:{ir_domain} {ticker} investor day {year} filetype:pdf'


# ---------------------------------------------------------------------------
# Result parsing helpers
# ---------------------------------------------------------------------------

def extract_pdf_urls_from_search_results(search_text: str) -> list[str]:
    """
    Parse PDF URLs from WebSearch result text.
    Handles common patterns: direct .pdf URLs and Google's cache of PDF links.
    """
    # Match http(s):// URLs ending in .pdf
    urls = re.findall(r'https?://[^\s\'"<>]+\.pdf', search_text, re.IGNORECASE)
    # Deduplicate while preserving order
    seen: set[str] = set()
    result = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result


def filter_credible_pdf_urls(urls: list[str]) -> list[str]:
    """
    Filter PDF URLs to those from credible IR/SEC sources.
    Removes aggregator sites, cached copies, etc.
    """
    credible_patterns = [
        r"investor\.",
        r"investors\.",
        r"ir\.",
        r"\.sec\.gov",
        r"ourbrand\.asml\.com",
        r"prnewswire\.com",
        r"businesswire\.com",
        r"globenewswire\.com",
    ]
    result = []
    for url in urls:
        if any(re.search(p, url, re.IGNORECASE) for p in credible_patterns):
            result.append(url)
    return result


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------

def append_manifest(entry: dict[str, Any]) -> None:
    with MANIFEST_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def record_web_fallback_download(
    pdf_url: str,
    dest: Path,
    ticker: str | None,
    title: str | None = None,
) -> None:
    """Write a manifest entry after a successful web_fallback download."""
    sha = sha256_file(dest)
    entry: dict[str, Any] = {
        "path": str(dest.relative_to(EVIDENCE_DIR)),
        "ticker": ticker,
        "source_type": "other",
        "title": title or dest.name,
        "date": None,
        "added_by": "web_fallback",
        "fetched_from": pdf_url,
        "sha256": sha,
        "tags": [],
        "added_at": datetime.now(tz=timezone.utc).isoformat(),
        "page_count": None,
    }
    append_manifest(entry)


# ---------------------------------------------------------------------------
# High-level API (called by orchestrator or agent session)
# ---------------------------------------------------------------------------

def get_search_queries_for_ticker(
    ticker: str,
    year: int = 2026,
) -> list[str]:
    """
    Load company name from tickers.json and return ordered list of
    WebSearch queries to try for this ticker.
    Called by orchestrator when Tiers 1-3 miss.
    """
    try:
        data = json.loads(TICKERS_PATH.read_text())
        entry = next((t for t in data["tickers"] if t["ticker"] == ticker), None)
        if entry:
            company_name = entry["name"]
            return build_ticker_queries(ticker, company_name, year)
    except Exception as exc:
        log.warning("Could not load tickers.json: %s", exc)
    # Fallback if tickers.json lookup fails
    return build_ticker_queries(ticker, ticker, year)


def get_search_queries_for_topic(
    keywords: list[str],
    year: int = 2026,
) -> list[str]:
    """
    Return ordered list of WebSearch queries for a topic/keyword set.
    Called by orchestrator when Tiers 1-3 miss on a topic search.
    """
    return build_topic_queries(keywords, year)


# ---------------------------------------------------------------------------
# Instructions for agent session use
# ---------------------------------------------------------------------------

WEB_FALLBACK_USAGE = """
## web_fallback.py — Agent Session Usage

This module provides query building + URL filtering for the Tier 4 fallback.
Use it in an agent session like this:

    from scripts.evidence.web_fallback import (
        get_search_queries_for_ticker,
        get_search_queries_for_topic,
        extract_pdf_urls_from_search_results,
        filter_credible_pdf_urls,
        record_web_fallback_download,
    )

    # 1. Get queries
    queries = get_search_queries_for_ticker("AVGO")

    # 2. Call WebSearch tool for each query (in agent session)
    #    results_text = WebSearch(query=queries[0])

    # 3. Extract and filter PDF URLs
    #    all_urls = extract_pdf_urls_from_search_results(results_text)
    #    credible = filter_credible_pdf_urls(all_urls)

    # 4. Use WebFetch to retrieve promising PDFs
    #    content = WebFetch(url=credible[0], prompt="Is this an IR earnings deck or investor day PDF?")

    # 5. If confirmed, download and record
    #    record_web_fallback_download(pdf_url, dest_path, ticker="AVGO", title="AVGO Q1 2026 Deck")
"""

if __name__ == "__main__":
    print(WEB_FALLBACK_USAGE)
