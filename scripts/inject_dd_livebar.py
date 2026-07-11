#!/usr/bin/env python3
"""inject_dd_livebar.py — idempotent, marker-based injector of the LIVE STALENESS BAR loader.

Inserts

    <!-- DD_LIVEBAR -->
    <script src="/assets/dd-livebar.js" defer></script>

immediately before </body> in every docs/dd/DD_*.html that:
  * contains a <script id="dd-meta"> block (skip point-in-time-less legacy files), and
  * does NOT already carry the <!-- DD_LIVEBAR --> marker (idempotent re-run = no-op).

Legacy docs/dca/DCA_*.html is FROZEN and intentionally NOT touched.

Usage:
    python3 scripts/inject_dd_livebar.py            # apply for real
    python3 scripts/inject_dd_livebar.py --dry-run  # print what would change, touch nothing
"""
import argparse
import glob
import os
import re
import sys

MARKER = "<!-- DD_LIVEBAR -->"
SNIPPET = MARKER + '\n<script src="/assets/dd-livebar.js" defer></script>\n'

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD_GLOB = os.path.join(REPO_ROOT, "docs", "dd", "DD_*.html")

HAS_META = re.compile(r'<script\s+id=["\']dd-meta["\']', re.I)
BODY_CLOSE = re.compile(r"</body>", re.I)


def process(path, dry_run):
    """Return one of: 'injected', 'skip-no-meta', 'skip-has-marker', 'skip-no-body'."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    if not HAS_META.search(html):
        return "skip-no-meta"
    if MARKER in html:
        return "skip-has-marker"

    m = None
    for m in BODY_CLOSE.finditer(html):
        pass  # keep the LAST </body>
    if m is None:
        return "skip-no-body"

    idx = m.start()
    new_html = html[:idx] + SNIPPET + html[idx:]

    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
    return "injected"


def main():
    ap = argparse.ArgumentParser(description="Inject DD live staleness bar loader.")
    ap.add_argument("--dry-run", action="store_true", help="print planned changes, write nothing")
    args = ap.parse_args()

    files = sorted(glob.glob(DD_GLOB))
    counts = {"injected": 0, "skip-no-meta": 0, "skip-has-marker": 0, "skip-no-body": 0}
    injected_names = []
    for path in files:
        status = process(path, args.dry_run)
        counts[status] += 1
        if status == "injected":
            injected_names.append(os.path.basename(path))

    verb = "WOULD inject" if args.dry_run else "Injected"
    print("=" * 60)
    print(f"DD live-bar injector {'(DRY RUN)' if args.dry_run else ''}")
    print(f"Scanned            : {len(files)} DD_*.html")
    print(f"{verb:<19}: {counts['injected']}")
    print(f"Skipped (no meta)  : {counts['skip-no-meta']}")
    print(f"Skipped (marker)   : {counts['skip-has-marker']}")
    print(f"Skipped (no body)  : {counts['skip-no-body']}")
    print("=" * 60)
    if args.dry_run and injected_names:
        for n in injected_names[:20]:
            print("  +", n)
        if len(injected_names) > 20:
            print(f"  … and {len(injected_names) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
