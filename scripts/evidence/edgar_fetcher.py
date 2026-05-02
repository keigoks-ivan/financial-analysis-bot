"""
edgar_fetcher.py — SEC EDGAR 8-K + EX-99 PDF fetcher for evidence pool.

Fetches 8-K filings from the past `lookback_days` (default 90) for each
whitelisted ticker, downloads EX-99.1 (press release) and EX-99.2 (deck) PDFs
to evidence/ir_decks/, and writes a manifest entry per downloaded file.

Usage:
    python scripts/evidence/edgar_fetcher.py [TICKER [TICKER ...]]
    python scripts/evidence/edgar_fetcher.py          # all active tickers
    python scripts/evidence/edgar_fetcher.py NVDA AMD --days 180

Requires: requests (pip install requests)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "evidence"
IR_DECKS_DIR = EVIDENCE_DIR / "ir_decks"
MANIFEST_PATH = EVIDENCE_DIR / "manifest.jsonl"
TICKERS_PATH = EVIDENCE_DIR / "tickers.json"

EDGAR_SUBMISSIONS_BASE = "https://data.sec.gov/submissions"
EDGAR_ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar"

HEADERS = {
    "User-Agent": "keigoks@gmail.com financial-analysis-bot/1.0",
    "Accept-Encoding": "gzip, deflate",
}

# EX-99 exhibit types to download
TARGET_EXHIBIT_TYPES = {"EX-99.1", "EX-99.2"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------

def load_manifest() -> set[str]:
    """Return set of already-fetched URLs (fetched_from field) from manifest."""
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
    """Append one JSON line to manifest.jsonl."""
    with MANIFEST_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# SHA-256 helper
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# EDGAR API helpers
# ---------------------------------------------------------------------------

def get_submissions(cik: str) -> dict[str, Any]:
    """Fetch CIK submissions JSON from EDGAR (rate-limited)."""
    # CIK must be zero-padded to 10 digits
    padded = cik.lstrip("0").zfill(10)
    url = f"{EDGAR_SUBMISSIONS_BASE}/CIK{padded}.json"
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    time.sleep(0.12)  # EDGAR 10 req/s courtesy limit
    return resp.json()


def list_8k_since(submissions: dict, lookback_days: int) -> list[dict]:
    """
    Return list of {accessionNumber, filingDate, primaryDocument} for 8-K
    filings within the lookback window.
    """
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=lookback_days)
    recent = submissions.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])

    result = []
    for i, form in enumerate(forms):
        if form not in ("8-K", "8-K/A"):
            continue
        try:
            filing_date = datetime.fromisoformat(dates[i]).replace(tzinfo=timezone.utc)
        except (ValueError, IndexError):
            continue
        if filing_date < cutoff:
            continue
        result.append({
            "accessionNumber": accessions[i],
            "filingDate": dates[i],
        })
    return result


def get_filing_index(cik: str, accession: str) -> list[dict]:
    """
    Fetch the filing index for an accession number; return list of
    {name, type, url} for each document.

    Uses two strategies:
    1. Parse the {accession}-index.html (human-readable) via BeautifulSoup to get
       exhibit type mappings — most reliable for EX-99 type detection.
    2. Fallback: list the directory via index.json.
    """
    from bs4 import BeautifulSoup

    padded_cik = cik.lstrip("0")
    acc_no_dash = accession.replace("-", "")
    base_url = f"{EDGAR_ARCHIVES_BASE}/data/{padded_cik}/{acc_no_dash}"

    # Strategy 1: parse the index HTML for exhibit type + filename
    index_html_url = f"{base_url}/{accession}-index.html"
    try:
        resp = requests.get(index_html_url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        time.sleep(0.12)
        soup = BeautifulSoup(resp.text, "html.parser")
        docs = []
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 3:
                continue
            exhibit_type = cells[1].get_text(strip=True)
            # Find the href in this row
            for a in row.find_all("a", href=True):
                href = a["href"].strip()
                # Normalize: strip /ix?doc= wrapper if present
                href = href.replace("/ix?doc=", "").replace("/ix?doc%3D", "")
                name = href.split("/")[-1]
                full_url = f"https://www.sec.gov{href}" if href.startswith("/") else href
                docs.append({
                    "name": name,
                    "type": exhibit_type,
                    "url": full_url,
                })
        if docs:
            return docs
    except Exception as exc:
        log.debug("Index HTML parse failed for %s: %s — falling back to index.json", accession, exc)

    # Strategy 2: directory listing via index.json
    dir_url = f"{base_url}/index.json"
    try:
        resp = requests.get(dir_url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        time.sleep(0.12)
        data = resp.json()
        docs = []
        for item in data.get("directory", {}).get("item", []):
            name = item.get("name", "")
            docs.append({
                "name": name,
                "type": "unknown",
                "url": f"{base_url}/{name}",
            })
        return docs
    except Exception as exc:
        log.warning("Could not fetch index for %s: %s", accession, exc)
        return []


def download_exhibit(url: str, dest: Path) -> bool:
    """
    Download an EX-99 exhibit (PDF or HTML) from SEC to dest.
    Returns True on success.

    Accepts both .pdf and .htm/.html EX-99 exhibits — many companies
    (e.g. NVDA) submit earnings releases as .htm rather than .pdf.
    """
    lower_url = url.lower()
    allowed_exts = (".pdf", ".htm", ".html")
    if not any(lower_url.endswith(ext) for ext in allowed_exts):
        log.debug("Skipping non-exhibit URL: %s", url)
        return False
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=65536):
                fh.write(chunk)
        time.sleep(0.12)
        return True
    except Exception as exc:
        log.warning("Download failed for %s: %s", url, exc)
        return False


# ---------------------------------------------------------------------------
# Main fetch logic per ticker
# ---------------------------------------------------------------------------

def fetch_ticker(ticker_entry: dict, lookback_days: int, already_fetched: set[str]) -> list[dict]:
    """Fetch 8-K EX-99 PDFs for one ticker. Returns list of new manifest entries."""
    ticker = ticker_entry["ticker"]
    cik = ticker_entry["cik"]
    industry_tags = ticker_entry.get("industry", [])

    log.info("[%s] Fetching EDGAR 8-K submissions (CIK %s)...", ticker, cik)
    try:
        submissions = get_submissions(cik)
    except Exception as exc:
        log.error("[%s] Failed to fetch submissions: %s", ticker, exc)
        return []

    filings = list_8k_since(submissions, lookback_days)
    log.info("[%s] Found %d 8-K filings in past %d days", ticker, len(filings), lookback_days)

    new_entries = []
    for filing in filings:
        accession = filing["accessionNumber"]
        filing_date = filing["filingDate"]

        docs = get_filing_index(cik, accession)
        for doc in docs:
            if doc["type"] not in TARGET_EXHIBIT_TYPES:
                continue
            exhibit_url = doc["url"]
            # Accept .pdf, .htm, .html exhibits — many companies use .htm
            lower_url = exhibit_url.lower()
            if not any(lower_url.endswith(ext) for ext in (".pdf", ".htm", ".html")):
                continue
            if exhibit_url in already_fetched:
                log.debug("[%s] Skipping already-fetched: %s", ticker, exhibit_url)
                continue

            # Build local filename: NVDA_20260225_EX-99_2_q4fy26pr.htm
            date_compact = filing_date.replace("-", "")
            safe_type = doc["type"].replace(".", "_").replace("/", "_")
            filename = f"{ticker}_{date_compact}_{safe_type}_{doc['name']}"
            dest = IR_DECKS_DIR / filename

            if dest.exists():
                log.debug("[%s] File already exists: %s", ticker, dest.name)
                already_fetched.add(exhibit_url)
                continue

            log.info("[%s] Downloading %s from %s", ticker, doc["type"], exhibit_url)
            ok = download_exhibit(exhibit_url, dest)
            if not ok:
                continue

            sha = sha256_file(dest)
            source_type = "earnings_deck" if doc["type"] == "EX-99.2" else "earnings_deck"
            if doc["type"] == "EX-99.1":
                source_type = "earnings_deck"  # press release still categorized here

            entry: dict[str, Any] = {
                "path": str(dest.relative_to(EVIDENCE_DIR)),
                "ticker": ticker,
                "source_type": source_type,
                "title": f"{ticker} {filing_date} {doc['type']}",
                "date": filing_date,
                "added_by": "edgar_fetcher",
                "fetched_from": exhibit_url,
                "sha256": sha,
                "tags": industry_tags,
                "added_at": datetime.now(tz=timezone.utc).isoformat(),
                "page_count": None,
            }
            append_manifest(entry)
            already_fetched.add(exhibit_url)
            new_entries.append(entry)
            log.info("[%s] Saved: %s (sha256 %s...)", ticker, dest.name, sha[:12])

    return new_entries


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
    parser = argparse.ArgumentParser(description="Fetch SEC EDGAR 8-K EX-99 PDFs.")
    parser.add_argument(
        "tickers",
        nargs="*",
        help="Ticker symbols to fetch (default: all active tickers)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Lookback window in days (default: 90)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List filings without downloading",
    )
    args = parser.parse_args()

    IR_DECKS_DIR.mkdir(parents=True, exist_ok=True)
    tickers = load_tickers(args.tickers if args.tickers else None)
    if not tickers:
        log.error("No matching active tickers found.")
        sys.exit(1)

    already_fetched = load_manifest()
    total_new = 0
    for ticker_entry in tickers:
        if args.dry_run:
            cik = ticker_entry["cik"]
            try:
                subs = get_submissions(cik)
                filings = list_8k_since(subs, args.days)
                log.info(
                    "[DRY-RUN] %s: %d 8-K filings in past %d days",
                    ticker_entry["ticker"], len(filings), args.days,
                )
                for f in filings[:3]:
                    log.info("  %s  %s", f["filingDate"], f["accessionNumber"])
            except Exception as exc:
                log.error("[DRY-RUN] %s: %s", ticker_entry["ticker"], exc)
        else:
            new_entries = fetch_ticker(ticker_entry, args.days, already_fetched)
            total_new += len(new_entries)

    if not args.dry_run:
        log.info("Done. %d new files downloaded.", total_new)


if __name__ == "__main__":
    main()
