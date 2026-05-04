#!/usr/bin/env python3
"""
_update_imq_style.py — Update the <style id="imq-h-style"> block in-place
in all pages that already have the new IMQ header, without re-running the
full migration. Useful when only the CSS changes.

Run:
    python3 scripts/_update_imq_style.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
sys.path.insert(0, str(REPO / "scripts"))

from imq_header import IMQ_H_CSS  # noqa: E402

STYLE_BLOCK_RE = re.compile(
    r"<style id=['\"]imq-h-style['\"]>.*?</style>",
    re.DOTALL,
)

EXTERNAL_PREFIXES = (
    "qgm/", "qgm-tw/", "briefing/2", "weekly/", "backtest/",
)


def _is_external(relpath: str) -> bool:
    for pfx in EXTERNAL_PREFIXES:
        if relpath.startswith(pfx):
            return True
    return False


def main():
    pages = list(DOCS.rglob("*.html"))
    updated = 0
    for p in sorted(pages):
        rp = str(p.relative_to(DOCS))
        if _is_external(rp):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "imq-h-style" not in text:
            continue
        new_text, n = STYLE_BLOCK_RE.subn(IMQ_H_CSS, text, count=1)
        if n == 0:
            continue
        if new_text == text:
            continue  # unchanged (CSS was already up to date)
        p.write_text(new_text, encoding="utf-8")
        updated += 1
        print(f"  ✅ {rp}")

    print(f"\nUpdated CSS in {updated} pages.")


if __name__ == "__main__":
    main()
