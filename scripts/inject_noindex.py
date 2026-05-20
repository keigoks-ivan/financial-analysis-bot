#!/usr/bin/env python3
"""Bulk-inject <meta name="robots" content="noindex,nofollow"> into HTML files.

Used to keep docs/ files in sync with robots.txt — belt-and-suspenders private-
mode policy. Idempotent: skips files that already carry a noindex meta tag.

Run after external repo regens (qgm/, briefing/, weekly/, backtest/, six-state/)
to re-stamp any files they rewrote.

Usage:
    python3 scripts/inject_noindex.py              # patch all docs/**/*.html
    python3 scripts/inject_noindex.py --dry-run    # report what would change
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

META_TAG = '<meta name="robots" content="noindex,nofollow">'
HEAD_OPEN_RE = re.compile(r"(<head[^>]*>)", re.IGNORECASE)
NOINDEX_RE = re.compile(
    r"""<meta\s+name=["']robots["']\s+content=["'][^"']*noindex""",
    re.IGNORECASE,
)


def patch_file(path: Path, dry_run: bool) -> str:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:
        return f"read-fail: {exc}"

    if NOINDEX_RE.search(content):
        return "skip"

    m = HEAD_OPEN_RE.search(content)
    if not m:
        return "no-head"

    if dry_run:
        return "would-patch"

    new = content[: m.end()] + "\n  " + META_TAG + content[m.end():]
    path.write_text(new, encoding="utf-8")
    return "patched"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    counts: dict[str, int] = {}
    no_head_paths: list[Path] = []

    for path in sorted(DOCS.rglob("*.html")):
        result = patch_file(path, args.dry_run)
        counts[result] = counts.get(result, 0) + 1
        if result == "no-head":
            no_head_paths.append(path)

    print(f"docs/ HTML files: {sum(counts.values())}")
    for k in ("patched", "would-patch", "skip", "no-head", "read-fail"):
        if k in counts:
            print(f"  {k}: {counts[k]}")
    if no_head_paths:
        print("no-head paths (need manual review):")
        for p in no_head_paths[:20]:
            print(f"  {p.relative_to(ROOT)}")
        if len(no_head_paths) > 20:
            print(f"  ... +{len(no_head_paths) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
