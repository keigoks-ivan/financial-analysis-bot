"""
arxiv_fetcher.py — arXiv API fetcher for semiconductor-related papers.

Searches arXiv for papers matching semiconductor topics in the cs.AR (Hardware
Architecture) and eess.SP (Signal Processing) categories within a configurable
lookback window, downloads PDFs to evidence/tech_papers/, and writes manifest
entries.

Usage:
    python scripts/evidence/arxiv_fetcher.py
    python scripts/evidence/arxiv_fetcher.py --query "HBM" --days 30
    python scripts/evidence/arxiv_fetcher.py --query "CoWoS chiplet" --max-results 10
    python scripts/evidence/arxiv_fetcher.py --list-only  # show results without downloading

Default queries (run all if no --query given):
    HBM, CoWoS, TSMC N2, advanced packaging, gate-all-around, backside power delivery

Categories searched: cs.AR, eess.SP, cond-mat.mtrl-sci

Requires: arxiv (pip install arxiv)
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

try:
    import arxiv
except ImportError:
    print("ERROR: arxiv package not installed. Run: pip install arxiv", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "evidence"
TECH_PAPERS_DIR = EVIDENCE_DIR / "tech_papers"
MANIFEST_PATH = EVIDENCE_DIR / "manifest.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default semiconductor queries
# ---------------------------------------------------------------------------
DEFAULT_QUERIES = [
    "HBM memory",
    "CoWoS advanced packaging",
    "TSMC N2 process",
    "gate-all-around transistor",
    "backside power delivery network",
    "chiplet interconnect",
]

# arXiv categories to search within
CATEGORIES = ["cs.AR", "eess.SP", "cond-mat.mtrl-sci"]


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------

def load_manifest_arxiv_ids() -> set[str]:
    """Return set of arXiv IDs already in manifest (to avoid re-download)."""
    seen: set[str] = set()
    if MANIFEST_PATH.exists():
        for line in MANIFEST_PATH.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                url = entry.get("fetched_from", "")
                if "arxiv.org" in url:
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
# arXiv search
# ---------------------------------------------------------------------------

def build_category_filter() -> str:
    """Build arXiv category filter string: (cat:cs.AR OR cat:eess.SP ...)"""
    parts = [f"cat:{c}" for c in CATEGORIES]
    return " OR ".join(parts)


def search_arxiv(
    query: str,
    max_results: int,
    lookback_days: int,
) -> list[arxiv.Result]:
    """
    Search arXiv for `query` within semiconductor categories, filtered to
    papers submitted/updated within the last `lookback_days` days.
    Returns a list of arxiv.Result objects.
    """
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=lookback_days)

    # Combine user query with category filter
    cat_filter = build_category_filter()
    full_query = f"({query}) AND ({cat_filter})"

    client = arxiv.Client(
        page_size=min(max_results, 100),
        delay_seconds=3,
        num_retries=3,
    )
    search = arxiv.Search(
        query=full_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    results = []
    for r in client.results(search):
        # Filter by submission date
        submitted = r.published.replace(tzinfo=timezone.utc) if r.published.tzinfo is None else r.published
        if submitted < cutoff:
            break
        results.append(r)

    return results


# ---------------------------------------------------------------------------
# Download helper
# ---------------------------------------------------------------------------

def download_arxiv_pdf(result: arxiv.Result, dest: Path) -> bool:
    """Download the PDF for an arXiv result to dest. Returns True on success."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        result.download_pdf(dirpath=str(dest.parent), filename=dest.name)
        time.sleep(1)
        return dest.exists()
    except Exception as exc:
        log.warning("Failed to download %s: %s", result.entry_id, exc)
        return False


# ---------------------------------------------------------------------------
# Main fetch logic
# ---------------------------------------------------------------------------

def fetch_query(
    query: str,
    max_results: int,
    lookback_days: int,
    list_only: bool,
    already_fetched: set[str],
) -> list[dict]:
    """Search and optionally download papers for one query. Returns new manifest entries."""
    log.info("Searching arXiv: query=%r, days=%d, max=%d", query, lookback_days, max_results)
    try:
        results = search_arxiv(query, max_results, lookback_days)
    except Exception as exc:
        log.error("arXiv search failed for %r: %s", query, exc)
        return []

    log.info("Found %d result(s) for %r", len(results), query)
    new_entries = []

    for result in results:
        pdf_url = result.pdf_url or ""
        if pdf_url in already_fetched:
            log.debug("Skipping already-fetched: %s", pdf_url)
            continue

        arxiv_id = result.entry_id.split("/")[-1]  # e.g. "2503.12345v1"
        date_str = result.published.strftime("%Y-%m-%d")
        safe_title = re.sub(r"[^\w\-]", "_", result.title[:50]) if result.title else "paper"

        if list_only:
            log.info(
                "  [%s] %s\n    %s\n    %s",
                date_str,
                result.title[:80],
                pdf_url,
                ", ".join(str(c) for c in result.categories[:3]),
            )
            already_fetched.add(pdf_url)
            continue

        filename = f"arxiv_{arxiv_id}_{safe_title}.pdf"
        dest = TECH_PAPERS_DIR / filename

        if dest.exists():
            already_fetched.add(pdf_url)
            continue

        log.info("Downloading arXiv %s: %s", arxiv_id, result.title[:60])
        ok = download_arxiv_pdf(result, dest)
        if not ok:
            continue

        sha = sha256_file(dest)
        entry: dict[str, Any] = {
            "path": str(dest.relative_to(EVIDENCE_DIR)),
            "ticker": None,
            "source_type": "tech_paper",
            "title": result.title,
            "date": date_str,
            "added_by": "arxiv_fetcher",
            "fetched_from": pdf_url,
            "sha256": sha,
            "tags": ["semi"] + list(result.categories[:3]),
            "added_at": datetime.now(tz=timezone.utc).isoformat(),
            "page_count": None,
        }
        append_manifest(entry)
        already_fetched.add(pdf_url)
        new_entries.append(entry)
        log.info("Saved: %s", dest.name)

    return new_entries


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

# Lazy import for re (used in fetch_query)
import re


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch semiconductor arXiv papers to evidence/tech_papers/."
    )
    parser.add_argument(
        "--query",
        help="Search query (default: run all DEFAULT_QUERIES)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=180,
        help="Lookback window in days (default: 180)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Max results per query (default: 5)",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="List results without downloading PDFs",
    )
    args = parser.parse_args()

    TECH_PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    already_fetched = load_manifest_arxiv_ids()

    queries = [args.query] if args.query else DEFAULT_QUERIES
    total_new = 0

    for q in queries:
        new_entries = fetch_query(
            query=q,
            max_results=args.max_results,
            lookback_days=args.days,
            list_only=args.list_only,
            already_fetched=already_fetched,
        )
        total_new += len(new_entries)

    if not args.list_only:
        log.info("Done. %d new papers downloaded.", total_new)
    else:
        log.info("List-only complete.")


if __name__ == "__main__":
    main()
