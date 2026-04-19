#!/usr/bin/env python3
"""Prepend unified nav to ID_*.html files (they currently have NO top nav)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _apply_nav import full_nav_block  # type: ignore

ROOT = Path("/Users/ivanchang/Desktop/financial-analysis-bot/docs")

active = {"group": "research", "item": "id"}
nav = full_nav_block(active)

targets = sorted((ROOT / "id").glob("ID_*.html"))

for p in targets:
    text = p.read_text(encoding="utf-8")
    if ".imq-nav-root" in text:
        print(f"  ⏭  {p.name} (already migrated)")
        continue
    if "<body>" not in text:
        print(f"  ❌ no <body> in {p.name}")
        continue
    new_text = text.replace("<body>", "<body>\n" + nav, 1)
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {p.name}")
