#!/usr/bin/env python3
"""Add 「產業敘述 DS」 nav link to all this-repo HTML files that have the
existing 「產業深度 ID」 nav dropdown entry.

Variants handled:
  1. ID file (active on /id/):
     <a href="/id/" class="active">產業深度 ID</a>
     →
     <a href="/id/" class="active">產業深度 ID</a>
               <a href="/ds/">產業敘述 DS</a>

  2. Non-ID-non-DS file (no active class):
     <a href="/id/">產業深度 ID</a>
     →
     <a href="/id/">產業深度 ID</a>
               <a href="/ds/">產業敘述 DS</a>

  3. DS file (active on /ds/): already handled by init_ds_index.py — skip.

  4. File already containing 「產業敘述 DS」: skip (idempotent).

Cross-repo files (qgm/, qgm-tw/, briefing/, weekly/, backtest/) are
deliberately SKIPPED — they are populated by cron push from external repos
and changes here would be overwritten. Update the generators in those repos
separately.

Usage:
  python3 scripts/add_ds_nav_link.py             # apply to all eligible files
  python3 scripts/add_ds_nav_link.py --dry-run   # report only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Directories that come from external repos via cron push — DO NOT touch.
EXTERNAL_REPO_DIRS = {"qgm", "qgm-tw", "briefing", "weekly", "backtest"}

# Pattern variants of the existing ID nav link.
PAT_ID_ACTIVE = re.compile(
    r'(<a href="/id/" class="active">產業深度 ID</a>)'
)
PAT_ID_PLAIN = re.compile(
    r'(<a href="/id/">產業深度 ID</a>)'
)

# The DS link to inject.
DS_LINK_AFTER_ID = '\n          <a href="/ds/">產業敘述 DS</a>'


def is_external_repo(path: Path) -> bool:
    """Check if path falls under any external-repo subdirectory."""
    try:
        rel = path.relative_to(DOCS)
    except ValueError:
        return True
    parts = rel.parts
    return len(parts) > 0 and parts[0] in EXTERNAL_REPO_DIRS


def is_ds_file(path: Path) -> bool:
    """Check if path is a DS file (active on /ds/)."""
    try:
        rel = path.relative_to(DOCS)
    except ValueError:
        return False
    return rel.parts[0] == "ds" if rel.parts else False


def process_file(path: Path, dry_run: bool = False) -> dict:
    """Process one file. Return dict with status + diff info."""
    try:
        html = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {"status": "read_error", "msg": str(e)}

    # Skip if already has DS link
    if "產業敘述 DS" in html:
        return {"status": "skip_already_has_ds"}

    # Skip if no ID nav at all
    if "產業深度 ID" not in html:
        return {"status": "skip_no_id_nav"}

    # Apply substitution (try both variants)
    new_html = html
    matched = False
    if PAT_ID_ACTIVE.search(new_html):
        new_html = PAT_ID_ACTIVE.sub(r"\1" + DS_LINK_AFTER_ID, new_html, count=1)
        matched = True
    elif PAT_ID_PLAIN.search(new_html):
        new_html = PAT_ID_PLAIN.sub(r"\1" + DS_LINK_AFTER_ID, new_html, count=1)
        matched = True

    if not matched:
        return {"status": "skip_no_match"}

    if dry_run:
        return {"status": "would_update"}

    path.write_text(new_html, encoding="utf-8")
    return {"status": "updated"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if not DOCS.exists():
        print(f"ERROR: docs dir not found: {DOCS}", file=sys.stderr)
        sys.exit(1)

    targets = sorted(DOCS.rglob("*.html"))
    print(f"Scanning {len(targets):,} HTML files under {DOCS}/...", file=sys.stderr)

    counts: dict = {
        "updated": 0,
        "would_update": 0,
        "skip_external": 0,
        "skip_already_has_ds": 0,
        "skip_no_id_nav": 0,
        "skip_no_match": 0,
        "skip_ds_file": 0,
        "read_error": 0,
    }

    for path in targets:
        if is_external_repo(path):
            counts["skip_external"] += 1
            continue
        if is_ds_file(path):
            counts["skip_ds_file"] += 1
            continue

        result = process_file(path, dry_run=args.dry_run)
        counts[result["status"]] = counts.get(result["status"], 0) + 1
        if args.verbose and result["status"] in ("updated", "would_update"):
            print(f"  ✏  {path.relative_to(ROOT)}", file=sys.stderr)
        elif args.verbose and result["status"] == "read_error":
            print(f"  ⚠  {path.relative_to(ROOT)}: {result['msg']}", file=sys.stderr)

    print(file=sys.stderr)
    print(f"Summary{'  (DRY RUN)' if args.dry_run else ''}:", file=sys.stderr)
    print(f"  ✅ updated              : {counts['updated']}", file=sys.stderr)
    print(f"  📝 would_update (dry)   : {counts['would_update']}", file=sys.stderr)
    print(f"  ↪  skip_ds_file         : {counts['skip_ds_file']}  (already has active /ds/)", file=sys.stderr)
    print(f"  ↪  skip_external        : {counts['skip_external']}  (qgm/briefing/weekly/backtest — other repos)", file=sys.stderr)
    print(f"  ↪  skip_already_has_ds  : {counts['skip_already_has_ds']}", file=sys.stderr)
    print(f"  ↪  skip_no_id_nav       : {counts['skip_no_id_nav']}  (no nav to update)", file=sys.stderr)
    print(f"  ⚠  skip_no_match        : {counts['skip_no_match']}  (has ID nav but pattern didn't match — investigate)", file=sys.stderr)
    print(f"  ⚠  read_error           : {counts['read_error']}", file=sys.stderr)


if __name__ == "__main__":
    main()
