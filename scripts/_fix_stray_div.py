#!/usr/bin/env python3
"""Remove stray </div> left by nav replacement in briefing/weekly pages."""

import re
from pathlib import Path

ROOT = Path("/Users/ivanchang/Desktop/financial-analysis-bot/docs")

# After the nav </script>, remove a stray </div> left from the old outer wrapper.
STRAY = re.compile(
    r"(</header>\s*<script>\(function\(\)\{[^<]*\}\)\(\);</script>)\s*</div>\s*(?=<div)",
    re.DOTALL,
)


def fix(relpath):
    p = ROOT / relpath
    text = p.read_text(encoding="utf-8")
    new_text, n = STRAY.subn(r"\1\n", text, count=1)
    if n:
        p.write_text(new_text, encoding="utf-8")
        return True
    return False


targets = []
targets.extend(sorted((ROOT / "briefing").glob("*.html")))
targets.extend(sorted((ROOT / "weekly").glob("*.html")))

fixed = 0
for t in targets:
    if fix(t.relative_to(ROOT)):
        fixed += 1

print(f"Fixed {fixed}/{len(targets)} pages.")
