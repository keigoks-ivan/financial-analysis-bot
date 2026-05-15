#!/usr/bin/env python3
"""Add 「DD Screener」 nav link to all this-repo HTML files that carry the
existing 「量化回測」 nav dropdown entry under 工具.

Insertion point: right after `<a href="/backtest/">量化回測</a>`. New entry
shape:

    <a href="/backtest/">量化回測</a>
              <a href="/dd-screener/">DD Screener</a>

The DD Screener's own page (`docs/dd-screener/index.html`) is skipped — it
was bootstrapped with its own active-state link and shouldn't be re-stamped.

Cross-repo dirs (qgm/, qgm-tw/, briefing/, weekly/, backtest/) are skipped
— they come from external repos via cron push and changes here would be
overwritten. Update the generators in those repos separately.

Idempotent: if a page already has 「DD Screener」 it is skipped.

Usage:
  python3 scripts/add_dd_screener_nav_link.py             # apply
  python3 scripts/add_dd_screener_nav_link.py --dry-run   # report only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

EXTERNAL_REPO_DIRS = {"qgm", "qgm-tw", "briefing", "weekly", "backtest"}

PAT_BACKTEST = re.compile(r'(<a href="/backtest/">量化回測</a>)')

DD_SCREENER_LINK = '\n          <a href="/dd-screener/">DD Screener</a>'


def is_external_repo(path: Path) -> bool:
    try:
        rel = path.relative_to(DOCS)
    except ValueError:
        return True
    return bool(rel.parts) and rel.parts[0] in EXTERNAL_REPO_DIRS


def is_dd_screener_own_page(path: Path) -> bool:
    try:
        rel = path.relative_to(DOCS)
    except ValueError:
        return False
    return rel.parts[:1] == ("dd-screener",)


def process_file(path: Path, dry_run: bool = False) -> str:
    try:
        html = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return f"read_error:{e}"

    if "DD Screener" in html and "/dd-screener/" in html:
        return "skip_already_has_link"

    if "量化回測" not in html:
        return "skip_no_tools_nav"

    if not PAT_BACKTEST.search(html):
        return "skip_no_match"

    new_html = PAT_BACKTEST.sub(r"\1" + DD_SCREENER_LINK, html, count=1)
    if dry_run:
        return "would_update"
    path.write_text(new_html, encoding="utf-8")
    return "updated"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    if not DOCS.exists():
        print(f"ERROR: {DOCS} missing", file=sys.stderr)
        sys.exit(1)

    targets = sorted(DOCS.rglob("*.html"))
    print(f"Scanning {len(targets):,} HTML under {DOCS}/", file=sys.stderr)

    counts: dict[str, int] = {}
    for f in targets:
        if is_external_repo(f):
            counts["skip_external"] = counts.get("skip_external", 0) + 1
            continue
        if is_dd_screener_own_page(f):
            counts["skip_own_page"] = counts.get("skip_own_page", 0) + 1
            continue
        status = process_file(f, dry_run=args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        if args.verbose and status in ("updated", "would_update"):
            print(f"  ✏  {f.relative_to(ROOT)}", file=sys.stderr)

    print(f"\nSummary{'  (DRY RUN)' if args.dry_run else ''}:", file=sys.stderr)
    for k, v in sorted(counts.items()):
        print(f"  {k:<25} {v}", file=sys.stderr)


if __name__ == "__main__":
    main()
