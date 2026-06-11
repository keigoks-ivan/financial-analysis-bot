#!/usr/bin/env python3
"""Add 「🎯 Flow」 top-level nav link to this-repo HTML pages that carry the
unified top nav (imq-menu) with the 「心智模型」 entry.

Insertion point: right before `<a href="/mental-models/">🧠 心智模型</a>`.
Result:

    </div>            ← end of 工具 dropdown
    <a href="/flow/">🎯 Flow</a>
    <a href="/mental-models/">🧠 心智模型</a>

Mirrors `add_dd_screener_nav_link.py` (PR2 of DD Screener ↔ Flow bridge).

Cross-repo dirs (qgm/, qgm-tw/, briefing/, weekly/, backtest/) are skipped
— their nav comes from external repos via cron push.

The Flow's own pages (`docs/flow/`) are skipped — they have a separate
footer-nav structure (handled by direct edits, not this script).

Idempotent: if a page already has `/flow/` link in nav it is skipped.

Usage:
  python3 scripts/add_flow_nav_link.py             # apply
  python3 scripts/add_flow_nav_link.py --dry-run   # report only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

EXTERNAL_REPO_DIRS = {"qgm", "qgm-tw", "briefing", "weekly", "backtest"}

# Match the mental-models anchor inside the unified top nav. Look for the
# imq-menu context to avoid hitting unrelated mentions of /mental-models/.
PAT_MENTAL = re.compile(r'(<a href="/mental-models/"[^>]*>🧠 心智模型</a>)')

FLOW_LINK = '<a href="/flow/" title="🎯 投資流程儀表板 — Cockpit / ATH Hunter / Timing Board / RS Board">🎯 Flow</a>\n      '


def is_external_repo(path: Path) -> bool:
    try:
        rel = path.relative_to(DOCS)
    except ValueError:
        return True
    return bool(rel.parts) and rel.parts[0] in EXTERNAL_REPO_DIRS


def is_flow_own_page(path: Path) -> bool:
    try:
        rel = path.relative_to(DOCS)
    except ValueError:
        return False
    return rel.parts[:1] == ("flow",)


def process_file(path: Path, dry_run: bool = False) -> str:
    try:
        html = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return f"read_error:{e}"

    # Idempotence — same nav already has /flow/.
    if 'href="/flow/"' in html and "imq-menu" in html:
        return "skip_already_has_link"

    if "心智模型" not in html or "imq-menu" not in html:
        return "skip_no_mental_anchor"

    if not PAT_MENTAL.search(html):
        return "skip_no_match"

    new_html = PAT_MENTAL.sub(FLOW_LINK + r"\1", html, count=1)
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

    # ARCHIVED 2026-06-11: /flow/ has been archived. This script is a no-op.
    # To re-enable: remove the early return below and restore FLOW_LINK injection.
    print("INFO: /flow/ is archived — add_flow_nav_link.py is a no-op.", file=sys.stderr)
    return

    targets = sorted(DOCS.rglob("*.html"))
    print(f"Scanning {len(targets):,} HTML under {DOCS}/", file=sys.stderr)

    counts: dict[str, int] = {}
    for f in targets:
        if is_external_repo(f):
            counts["skip_external"] = counts.get("skip_external", 0) + 1
            continue
        if is_flow_own_page(f):
            counts["skip_flow_own"] = counts.get("skip_flow_own", 0) + 1
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
