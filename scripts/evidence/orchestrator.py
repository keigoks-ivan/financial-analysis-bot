"""
orchestrator.py — Evidence pool fetch orchestrator.

Chains Tier 1 (EDGAR) → Tier 2 (IR fetcher) → Tier 3 (arXiv) → Tier 4
(web_fallback) per spec §3 and §6.  Provides two primary entry points:

    fetch_for_ticker(ticker)         — fetch all evidence for one company
    fetch_for_topic(keywords)        — fetch papers/evidence for a topic/theme

Used by the industry-analyst skill (Step 8) and can be called directly from
the CLI for manual prefetch before a writing session.

Usage:
    python scripts/evidence/orchestrator.py NVDA
    python scripts/evidence/orchestrator.py NVDA TSM ASML --days 90
    python scripts/evidence/orchestrator.py --topic "HBM" "CoWoS"
    python scripts/evidence/orchestrator.py --all    # all active tickers
    python scripts/evidence/orchestrator.py NVDA --tier 1   # EDGAR only
    python scripts/evidence/orchestrator.py --topic "HBM" --tier 3  # arXiv only

Tier mapping:
    Tier 1: edgar_fetcher  (8-K + EX-99 PDFs via SEC EDGAR API)
    Tier 2: ir_fetcher     (IR page scrape for earnings/investor-day decks)
    Tier 3: arxiv_fetcher  (arXiv papers for topic keywords)
    Tier 4: web_fallback   (WebSearch/WebFetch — only if Tiers 1-3 all miss)

Requires: requests, beautifulsoup4, arxiv  (pip install requests beautifulsoup4 arxiv)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "evidence"
MANIFEST_PATH = EVIDENCE_DIR / "manifest.jsonl"
TICKERS_PATH = EVIDENCE_DIR / "tickers.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lazy imports of fetcher modules (avoid hard failures if deps missing)
# ---------------------------------------------------------------------------

def _import_edgar_fetcher():
    try:
        from scripts.evidence import edgar_fetcher
        return edgar_fetcher
    except ImportError:
        # Try relative import fallback
        import importlib.util, os
        spec = importlib.util.spec_from_file_location(
            "edgar_fetcher",
            Path(__file__).parent / "edgar_fetcher.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


def _import_ir_fetcher():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "ir_fetcher",
        Path(__file__).parent / "ir_fetcher.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _import_arxiv_fetcher():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "arxiv_fetcher",
        Path(__file__).parent / "arxiv_fetcher.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _import_web_fallback():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "web_fallback",
        Path(__file__).parent / "web_fallback.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Manifest / tickers helpers
# ---------------------------------------------------------------------------

def load_tickers(filter_tickers: list[str] | None = None) -> list[dict]:
    data = json.loads(TICKERS_PATH.read_text())
    entries = [t for t in data["tickers"] if t.get("active", True)]
    if filter_tickers:
        upper = [t.upper() for t in filter_tickers]
        entries = [t for t in entries if t["ticker"].upper() in upper]
    return entries


def grep_manifest(
    ticker: str | None = None,
    tags: list[str] | None = None,
    days: int | None = None,
) -> list[dict]:
    """
    Search manifest.jsonl for entries matching ticker, tags, or recency.
    Returns list of matching manifest entries (dicts).
    """
    from datetime import datetime, timedelta, timezone

    results = []
    cutoff = None
    if days:
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)

    if not MANIFEST_PATH.exists():
        return results

    for line in MANIFEST_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        if ticker and entry.get("ticker") != ticker:
            continue

        if tags:
            entry_tags = entry.get("tags", [])
            if not any(t in entry_tags for t in tags):
                continue

        if cutoff:
            added_at_str = entry.get("added_at", "")
            try:
                added_at = datetime.fromisoformat(added_at_str)
                if added_at.tzinfo is None:
                    added_at = added_at.replace(tzinfo=timezone.utc)
                if added_at < cutoff:
                    continue
            except (ValueError, TypeError):
                pass

        results.append(entry)

    return results


def has_recent_evidence(ticker: str, days: int = 30) -> bool:
    """Return True if manifest has any entry for ticker within the past `days` days."""
    return len(grep_manifest(ticker=ticker, days=days)) > 0


# ---------------------------------------------------------------------------
# Core entry points
# ---------------------------------------------------------------------------

def fetch_for_ticker(
    ticker: str,
    lookback_days: int = 90,
    tiers: list[int] | None = None,
    list_only: bool = False,
) -> dict[str, Any]:
    """
    Fetch all evidence for a single ticker, chaining Tier 1 → Tier 2 → Tier 4.
    (Tier 3 / arXiv is topic-based, not ticker-based — use fetch_for_topic.)

    Args:
        ticker:        Ticker symbol (must be in tickers.json)
        lookback_days: How far back to search (default 90 days)
        tiers:         Which tiers to run (default [1, 2]). Pass [1] for EDGAR only.
        list_only:     If True, list found items without downloading.

    Returns:
        dict with keys 'tier1_count', 'tier2_count', 'tier4_queries', 'ticker'
    """
    if tiers is None:
        tiers = [1, 2]

    ticker = ticker.upper()
    ticker_entries = load_tickers([ticker])
    if not ticker_entries:
        log.error("Ticker %s not found in tickers.json", ticker)
        return {"ticker": ticker, "error": "not in tickers.json"}

    ticker_entry = ticker_entries[0]
    result: dict[str, Any] = {"ticker": ticker, "tier1_count": 0, "tier2_count": 0, "tier4_queries": []}

    # -- Tier 1: EDGAR --
    if 1 in tiers:
        log.info("=== %s Tier 1: EDGAR ===", ticker)
        try:
            ef = _import_edgar_fetcher()
            already_fetched = ef.load_manifest()
            new_entries = ef.fetch_ticker(ticker_entry, lookback_days, already_fetched)
            result["tier1_count"] = len(new_entries)
            log.info("[%s] Tier 1 done: %d new files", ticker, len(new_entries))
        except Exception as exc:
            log.error("[%s] Tier 1 failed: %s", ticker, exc)

    # -- Tier 2: IR Fetcher --
    if 2 in tiers:
        log.info("=== %s Tier 2: IR Fetcher ===", ticker)
        try:
            irf = _import_ir_fetcher()
            already_fetched = irf.load_manifest_urls()
            recipe = irf.RECIPES.get(ticker, irf.scrape_generic)
            new_entries = recipe(ticker_entry, list_only, already_fetched)
            result["tier2_count"] = len(new_entries)
            log.info("[%s] Tier 2 done: %d new files", ticker, len(new_entries))
        except Exception as exc:
            log.error("[%s] Tier 2 failed: %s", ticker, exc)

    # -- Tier 4: Web Fallback (only if Tier 1+2 both returned 0) --
    if 4 in tiers or (result["tier1_count"] == 0 and result["tier2_count"] == 0 and 4 not in [t * -1 for t in tiers]):
        # Only auto-trigger Tier 4 if explicitly requested OR if Tiers 1+2 returned nothing
        if result["tier1_count"] == 0 and result["tier2_count"] == 0:
            log.info("=== %s Tier 4: Web Fallback (Tiers 1+2 returned 0) ===", ticker)
            try:
                wf = _import_web_fallback()
                queries = wf.get_search_queries_for_ticker(ticker)
                result["tier4_queries"] = queries
                log.info(
                    "[%s] Tier 4 queries (run in agent session with WebSearch):\n  %s",
                    ticker,
                    "\n  ".join(queries),
                )
            except Exception as exc:
                log.error("[%s] Tier 4 query build failed: %s", ticker, exc)

    return result


def fetch_for_topic(
    keywords: list[str],
    lookback_days: int = 180,
    max_results: int = 5,
    tiers: list[int] | None = None,
    list_only: bool = False,
) -> dict[str, Any]:
    """
    Fetch evidence for a topic described by keywords.
    Runs Tier 3 (arXiv) as primary; falls back to Tier 4 (web) if 0 results.

    Args:
        keywords:      List of search keywords (e.g. ["HBM", "high bandwidth memory"])
        lookback_days: arXiv lookback window (default 180 days)
        max_results:   Max arXiv results per query (default 5)
        tiers:         Which tiers to run (default [3]). Pass [3, 4] to also run web fallback.
        list_only:     If True, list without downloading.

    Returns:
        dict with keys 'tier3_count', 'tier4_queries', 'keywords'
    """
    if tiers is None:
        tiers = [3]

    result: dict[str, Any] = {
        "keywords": keywords,
        "tier3_count": 0,
        "tier4_queries": [],
    }

    # -- Tier 3: arXiv --
    if 3 in tiers:
        log.info("=== Tier 3: arXiv (keywords=%s) ===", keywords)
        try:
            af = _import_arxiv_fetcher()
            already_fetched = af.load_manifest_arxiv_ids()
            query = " ".join(keywords)
            new_entries = af.fetch_query(
                query=query,
                max_results=max_results,
                lookback_days=lookback_days,
                list_only=list_only,
                already_fetched=already_fetched,
            )
            result["tier3_count"] = len(new_entries)
            log.info("Tier 3 done: %d new papers", len(new_entries))
        except Exception as exc:
            log.error("Tier 3 failed: %s", exc)

    # -- Tier 4: Web Fallback --
    if 4 in tiers or result["tier3_count"] == 0:
        if result["tier3_count"] == 0:
            log.info("=== Tier 4: Web Fallback (Tier 3 returned 0) ===")
            try:
                wf = _import_web_fallback()
                queries = wf.get_search_queries_for_topic(keywords)
                result["tier4_queries"] = queries
                log.info(
                    "Tier 4 queries (run in agent session with WebSearch):\n  %s",
                    "\n  ".join(queries),
                )
            except Exception as exc:
                log.error("Tier 4 query build failed: %s", exc)

    return result


def fetch_for_id_session(
    candidate_tickers: list[str],
    topic_keywords: list[str] | None = None,
    lookback_days: int = 90,
) -> dict[str, Any]:
    """
    Phase 0a/0b prefetch for an ID writing session (per spec §6).

    For each candidate ticker:
      - Skip if manifest has evidence fetched within 30 days
      - Otherwise run fetch_for_ticker (Tier 1 + Tier 2)

    For topic keywords (if provided):
      - Run fetch_for_topic (Tier 3)

    Returns summary dict with per-ticker results.
    """
    log.info("=== ID Session Prefetch: %d tickers ===", len(candidate_tickers))

    summary: dict[str, Any] = {
        "tickers": {},
        "topic": {},
        "skipped": [],
    }

    for ticker in candidate_tickers:
        ticker = ticker.upper()
        if has_recent_evidence(ticker, days=30):
            log.info("[%s] Skipping — fresh evidence in manifest (< 30 days)", ticker)
            summary["skipped"].append(ticker)
            continue
        log.info("[%s] Fetching...", ticker)
        result = fetch_for_ticker(ticker, lookback_days=lookback_days, tiers=[1, 2])
        summary["tickers"][ticker] = result

    if topic_keywords:
        log.info("=== Topic prefetch: %s ===", topic_keywords)
        topic_result = fetch_for_topic(topic_keywords, tiers=[3])
        summary["topic"] = topic_result

    total = sum(
        r.get("tier1_count", 0) + r.get("tier2_count", 0)
        for r in summary["tickers"].values()
    )
    total += summary.get("topic", {}).get("tier3_count", 0)
    log.info("=== Prefetch complete: %d new files total ===", total)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Orchestrate evidence fetching across EDGAR, IR, arXiv, and web fallback."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "tickers",
        nargs="*",
        help="Ticker symbols to fetch (e.g. NVDA TSM)",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Fetch all active tickers",
    )
    parser.add_argument(
        "--topic",
        nargs="+",
        metavar="KEYWORD",
        help="Fetch for topic keywords (Tier 3 arXiv); e.g. --topic HBM CoWoS",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Lookback window in days (default: 90 for tickers, 180 for topics)",
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4],
        action="append",
        dest="tiers",
        help="Restrict to specific tier(s) (can repeat: --tier 1 --tier 2)",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="List found items without downloading",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Max arXiv results per query (for --topic, default: 5)",
    )
    args = parser.parse_args()

    if args.topic:
        days = args.days if args.days != 90 else 180
        result = fetch_for_topic(
            keywords=args.topic,
            lookback_days=days,
            max_results=args.max_results,
            tiers=args.tiers,
            list_only=args.list_only,
        )
        log.info("Topic fetch result: %s", json.dumps(result, indent=2, default=str))
        return

    if args.all:
        ticker_list = [t["ticker"] for t in load_tickers()]
    elif args.tickers:
        ticker_list = [t.upper() for t in args.tickers]
    else:
        parser.print_help()
        sys.exit(0)

    for ticker in ticker_list:
        result = fetch_for_ticker(
            ticker=ticker,
            lookback_days=args.days,
            tiers=args.tiers or [1, 2],
            list_only=args.list_only,
        )
        log.info(
            "[%s] Result: tier1=%d, tier2=%d, tier4_queries=%d",
            ticker,
            result.get("tier1_count", 0),
            result.get("tier2_count", 0),
            len(result.get("tier4_queries", [])),
        )


if __name__ == "__main__":
    main()
