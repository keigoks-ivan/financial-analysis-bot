"""
ir_fetcher.py — IR page scraper for earnings decks and investor day PDFs.

Scrapes the ir_url (quarterly results) and ir_events_url (events/calendar) for
each ticker to find PDF links not already captured by EDGAR, downloads them to
evidence/ir_decks/, and writes manifest entries.

TEMPLATE TICKERS IMPLEMENTED: NVDA, TSM
Each ticker has a dedicated recipe function (scrape_<ticker>) that knows the
DOM structure of that company's IR site.  All other tickers fall back to a
generic link-harvesting approach which may miss PDFs behind JS rendering but
will catch direct <a href="*.pdf"> links.

TODO: add recipe for ASML  (www.asml.com/en/investors/financial-results)
TODO: add recipe for AMD   (ir.amd.com/financial-information/quarterly-results)
TODO: add recipe for AVGO  (investors.broadcom.com/financial-information/quarterly-results)
TODO: add recipe for INTC  (www.intc.com/financial-info/financial-results)
TODO: add recipe for MU    (investors.micron.com/quarterly-results)
TODO: add recipe for AMAT  (ir.appliedmaterials.com/financial-information/quarterly-results/)
TODO: add recipe for LRCX  (investor.lamresearch.com/quarterly-results)
TODO: add recipe for KLAC  (ir.kla.com/financial-information/financial-results)

Usage:
    python scripts/evidence/ir_fetcher.py [TICKER [TICKER ...]]
    python scripts/evidence/ir_fetcher.py NVDA TSM
    python scripts/evidence/ir_fetcher.py NVDA --list-only   # show found PDFs, don't download

Requires: requests, beautifulsoup4 (pip install requests beautifulsoup4)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "evidence"
IR_DECKS_DIR = EVIDENCE_DIR / "ir_decks"
MANIFEST_PATH = EVIDENCE_DIR / "manifest.jsonl"
TICKERS_PATH = EVIDENCE_DIR / "tickers.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36 "
        "keigoks@gmail.com financial-analysis-bot/1.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Manifest / SHA helpers (shared with edgar_fetcher)
# ---------------------------------------------------------------------------

def load_manifest_urls() -> set[str]:
    seen: set[str] = set()
    if MANIFEST_PATH.exists():
        for line in MANIFEST_PATH.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                url = entry.get("fetched_from", "")
                if url:
                    seen.add(url)
            except json.JSONDecodeError:
                pass
    return seen


def append_manifest(entry: dict[str, Any]) -> None:
    with MANIFEST_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Generic HTTP helpers
# ---------------------------------------------------------------------------

def fetch_html(url: str, timeout: int = 20) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        time.sleep(0.3)
        return resp.text
    except Exception as exc:
        log.warning("fetch_html failed for %s: %s", url, exc)
        return None


def download_file(url: str, dest: Path) -> bool:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=65536):
                fh.write(chunk)
        time.sleep(0.3)
        return True
    except Exception as exc:
        log.warning("Download failed for %s: %s", url, exc)
        return False


# ---------------------------------------------------------------------------
# PDF link extraction helpers
# ---------------------------------------------------------------------------

def extract_pdf_links(html: str, base_url: str) -> list[str]:
    """Generic fallback: find all <a href> pointing to a PDF."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        # Resolve relative URLs
        full = urljoin(base_url, href)
        if full.lower().endswith(".pdf"):
            links.append(full)
    return list(dict.fromkeys(links))  # deduplicate, preserve order


def classify_pdf_url(url: str) -> tuple[str, str]:
    """
    Heuristic classification of a PDF URL.
    Returns (source_type, inferred_title_fragment).
    """
    lower = url.lower()
    if any(kw in lower for kw in ["investor_day", "investorday", "cmd", "capital_market"]):
        return "investor_day", "Investor Day"
    if any(kw in lower for kw in ["presentation", "slides", "deck"]):
        return "earnings_deck", "Earnings Presentation"
    if any(kw in lower for kw in ["release", "earnings_release", "press"]):
        return "earnings_deck", "Earnings Release"
    if any(kw in lower for kw in ["transcript"]):
        return "earnings_deck", "Earnings Transcript"
    return "other", "IR Document"


# ---------------------------------------------------------------------------
# NVDA recipe
# ---------------------------------------------------------------------------

def scrape_nvda(ticker_entry: dict, list_only: bool, already_fetched: set[str]) -> list[dict]:
    """
    NVDA IR recipe.
    Quarterly results: https://investor.nvidia.com/financial-info/quarterly-results/
      — Lists earnings releases and presentation PDFs directly as <a href="*.pdf">
    Events page: https://investor.nvidia.com/events-and-presentations/events-and-presentations/default.aspx
      — Contains links to individual event pages; PDF links are buried one level deeper.
    """
    ticker = "NVDA"
    new_entries: list[dict] = []

    pages = [
        (ticker_entry.get("ir_url", ""), "quarterly"),
        (ticker_entry.get("ir_events_url", ""), "events"),
    ]

    for page_url, page_label in pages:
        if not page_url:
            continue
        log.info("[NVDA] Scraping %s page: %s", page_label, page_url)
        html = fetch_html(page_url)
        if not html:
            continue

        pdf_links = extract_pdf_links(html, page_url)

        # For events page: also follow sub-event pages that may contain PDFs
        if page_label == "events":
            soup = BeautifulSoup(html, "html.parser")
            event_links = []
            for a in soup.find_all("a", href=True):
                href = urljoin(page_url, a["href"].strip())
                if "event-details" in href and href not in event_links:
                    event_links.append(href)
            for ev_url in event_links[:20]:  # cap at 20 event sub-pages
                ev_html = fetch_html(ev_url)
                if ev_html:
                    pdf_links += extract_pdf_links(ev_html, ev_url)

        pdf_links = list(dict.fromkeys(pdf_links))
        log.info("[NVDA] Found %d PDF link(s) on %s page", len(pdf_links), page_label)

        for pdf_url in pdf_links:
            entry = _process_pdf_link(pdf_url, ticker, ticker_entry, already_fetched, list_only)
            if entry:
                new_entries.append(entry)

    return new_entries


# ---------------------------------------------------------------------------
# TSM recipe
# ---------------------------------------------------------------------------

def scrape_tsm(ticker_entry: dict, list_only: bool, already_fetched: set[str]) -> list[dict]:
    """
    TSM IR recipe.
    Quarterly results: https://investor.tsmc.com/english/quarterly-results
      — Each quarter has a sub-page at /english/quarterly-results/YYYY/qN
        with direct PDF links for Presentation, Earnings Release, etc.
    Events (financial-calendar): https://investor.tsmc.com/english/financial-calendar
      — Lists upcoming/past events; may contain PDF links or event sub-pages.

    Strategy: parse the main quarterly-results page for per-quarter sub-URLs,
    visit each to harvest PDFs (last 4 quarters).
    """
    ticker = "TSM"
    base_url = "https://investor.tsmc.com"
    new_entries: list[dict] = []

    # --- Step 1: quarterly results ---
    qr_url = ticker_entry.get("ir_url", "")
    log.info("[TSM] Scraping quarterly results: %s", qr_url)
    html = fetch_html(qr_url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        # Find per-quarter sub-page links: /english/quarterly-results/YYYY/qN
        quarter_links: list[str] = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            full = urljoin(base_url, href)
            if re.search(r"/quarterly-results/\d{4}/q\d", full):
                if full not in quarter_links:
                    quarter_links.append(full)
        # Take the most recent 4 quarters
        quarter_links = quarter_links[:4]
        log.info("[TSM] Found %d quarter sub-pages", len(quarter_links))

        for q_url in quarter_links:
            q_html = fetch_html(q_url)
            if not q_html:
                continue
            pdf_links = extract_pdf_links(q_html, q_url)
            # Also look for encrypt/files links (TSMC uses these for actual PDFs)
            extra = re.findall(r'https://investor\.tsmc\.com/english/encrypt/files/[^\s"\']+', q_html)
            pdf_links += [u for u in extra if u.lower().endswith(".pdf")]
            pdf_links = list(dict.fromkeys(pdf_links))
            log.info("[TSM] %s: %d PDF link(s)", q_url, len(pdf_links))
            for pdf_url in pdf_links:
                entry = _process_pdf_link(pdf_url, ticker, ticker_entry, already_fetched, list_only)
                if entry:
                    new_entries.append(entry)

    # --- Step 2: financial calendar / events ---
    ev_url = ticker_entry.get("ir_events_url", "")
    log.info("[TSM] Scraping events/calendar: %s", ev_url)
    ev_html = fetch_html(ev_url)
    if ev_html:
        pdf_links = extract_pdf_links(ev_html, ev_url)
        for pdf_url in pdf_links:
            entry = _process_pdf_link(pdf_url, ticker, ticker_entry, already_fetched, list_only)
            if entry:
                new_entries.append(entry)

    return new_entries


# ---------------------------------------------------------------------------
# Generic fallback recipe (used for all tickers without a dedicated recipe)
# ---------------------------------------------------------------------------

def scrape_generic(ticker_entry: dict, list_only: bool, already_fetched: set[str]) -> list[dict]:
    """
    Generic IR scraper: fetch ir_url and ir_events_url, harvest all direct PDF links.
    Does not follow sub-pages or handle JS-rendered content.
    """
    ticker = ticker_entry["ticker"]
    new_entries: list[dict] = []

    for url_key in ("ir_url", "ir_events_url"):
        page_url = ticker_entry.get(url_key, "")
        if not page_url:
            continue
        log.info("[%s] Generic scrape of %s: %s", ticker, url_key, page_url)
        html = fetch_html(page_url)
        if not html:
            continue
        pdf_links = extract_pdf_links(html, page_url)
        log.info("[%s] Found %d PDF link(s) on %s", ticker, len(pdf_links), url_key)
        for pdf_url in pdf_links:
            entry = _process_pdf_link(pdf_url, ticker, ticker_entry, already_fetched, list_only)
            if entry:
                new_entries.append(entry)

    return new_entries


# ---------------------------------------------------------------------------
# Shared download + manifest write
# ---------------------------------------------------------------------------

def _process_pdf_link(
    pdf_url: str,
    ticker: str,
    ticker_entry: dict,
    already_fetched: set[str],
    list_only: bool,
) -> dict | None:
    """
    Given a verified PDF URL: if list_only, just log; otherwise download and
    write manifest.  Returns manifest entry dict or None.
    """
    if pdf_url in already_fetched:
        return None

    source_type, title_frag = classify_pdf_url(pdf_url)

    # Derive filename from URL (last path segment)
    parsed = urlparse(pdf_url)
    raw_name = Path(parsed.path).name or "document.pdf"
    filename = f"{ticker}_{raw_name}"
    dest = IR_DECKS_DIR / filename

    if list_only:
        log.info("[%s] [LIST] %s  %s", ticker, source_type, pdf_url)
        already_fetched.add(pdf_url)
        return None

    if dest.exists():
        already_fetched.add(pdf_url)
        return None

    log.info("[%s] Downloading %s: %s", ticker, source_type, pdf_url)
    ok = download_file(pdf_url, dest)
    if not ok:
        return None

    sha = sha256_file(dest)
    entry: dict[str, Any] = {
        "path": str(dest.relative_to(EVIDENCE_DIR)),
        "ticker": ticker,
        "source_type": source_type,
        "title": f"{ticker} {title_frag}",
        "date": None,
        "added_by": "ir_fetcher",
        "fetched_from": pdf_url,
        "sha256": sha,
        "tags": ticker_entry.get("industry", []),
        "added_at": datetime.now(tz=timezone.utc).isoformat(),
        "page_count": None,
    }
    append_manifest(entry)
    already_fetched.add(pdf_url)
    log.info("[%s] Saved: %s (sha256 %s...)", ticker, dest.name, sha[:12])
    return entry


# ---------------------------------------------------------------------------
# Dispatch table — add new tickers here as dedicated recipes are implemented
# ---------------------------------------------------------------------------

RECIPES: dict[str, Any] = {
    "NVDA": scrape_nvda,
    "TSM": scrape_tsm,
    # TODO: add recipe for ASML
    # TODO: add recipe for AMD
    # TODO: add recipe for AVGO
    # TODO: add recipe for INTC
    # TODO: add recipe for MU
    # TODO: add recipe for AMAT
    # TODO: add recipe for LRCX
    # TODO: add recipe for KLAC
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_tickers(filter_tickers: list[str] | None = None) -> list[dict]:
    data = json.loads(TICKERS_PATH.read_text())
    entries = [t for t in data["tickers"] if t.get("active", True)]
    if filter_tickers:
        upper = [t.upper() for t in filter_tickers]
        entries = [t for t in entries if t["ticker"].upper() in upper]
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape IR pages for earnings/investor-day PDFs.")
    parser.add_argument(
        "tickers",
        nargs="*",
        help="Ticker symbols to scrape (default: all active tickers)",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="List found PDF URLs without downloading",
    )
    args = parser.parse_args()

    IR_DECKS_DIR.mkdir(parents=True, exist_ok=True)
    tickers = load_tickers(args.tickers if args.tickers else None)
    if not tickers:
        log.error("No matching active tickers found.")
        sys.exit(1)

    already_fetched = load_manifest_urls()
    total_new = 0

    for ticker_entry in tickers:
        ticker = ticker_entry["ticker"]
        recipe = RECIPES.get(ticker, scrape_generic)
        new_entries = recipe(ticker_entry, args.list_only, already_fetched)
        total_new += len(new_entries)

    if not args.list_only:
        log.info("Done. %d new files downloaded.", total_new)
    else:
        log.info("List-only mode. No files downloaded.")


if __name__ == "__main__":
    main()
