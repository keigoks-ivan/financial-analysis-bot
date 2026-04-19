#!/usr/bin/env python3
"""Apply unified nav to remaining sub-pages (backtest systems, qgm archives)."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _apply_nav import full_nav_block, HEADER_RE  # type: ignore

ROOT = Path("/Users/ivanchang/Desktop/financial-analysis-bot/docs")


def apply_header_style(relpath, active):
    p = ROOT / relpath
    text = p.read_text(encoding="utf-8")
    # Skip if already has unified nav
    if ".imq-nav-root" in text:
        print(f"  ⏭  {relpath} (already migrated)")
        return False
    new_block = full_nav_block(active)
    new_text, n = HEADER_RE.subn(new_block, text, count=1)
    if n == 0:
        print(f"  ❌ no match in {relpath}")
        return False
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {relpath}")
    return True


# Backtest sub-pages
print("Applying to /backtest/*/ sub-pages...")
for sub in ROOT.glob("backtest/*/index.html"):
    apply_header_style(
        sub.relative_to(ROOT), {"group": "quant", "item": "bt"}
    )

# QGM archive
print("\nApplying to /qgm/archive/*.html...")
for sub in sorted((ROOT / "qgm/archive").glob("*.html")):
    apply_header_style(
        sub.relative_to(ROOT), {"group": "quant", "item": "qus"}
    )

print("\nApplying to /qgm-tw/archive/*.html...")
for sub in sorted((ROOT / "qgm-tw/archive").glob("*.html")):
    apply_header_style(
        sub.relative_to(ROOT), {"group": "quant", "item": "qtw"}
    )
