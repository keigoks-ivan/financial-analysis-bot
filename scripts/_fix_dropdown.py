#!/usr/bin/env python3
"""Fix dropdown hover flicker by removing the 6px gap.

Bug: `.imq-dd-menu{top:calc(100% + 6px)}` creates a gap where :hover is lost
as the mouse moves from the button to the menu, causing the menu to close mid-movement.

Fix: Remove the gap entirely. Menu now sits flush against the button,
so hover is never interrupted.
"""

from pathlib import Path

ROOT = Path("/Users/ivanchang/Desktop/financial-analysis-bot/docs")

OLD = "top:calc(100% + 6px);left:0;background:#1e293b;"
NEW = "top:100%;left:0;background:#1e293b;"

count = 0
for p in ROOT.rglob("*.html"):
    t = p.read_text(encoding="utf-8")
    if OLD in t:
        p.write_text(t.replace(OLD, NEW), encoding="utf-8")
        count += 1

print(f"Fixed {count} files.")
