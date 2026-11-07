#!/usr/bin/env python3
"""Print a compact, human-auditable table of a cleaned evidence pack:
importance, kind, topic, which claims it bears on, headline, source.

Usage:
  python3 scripts/jev/show_evidence.py --ticker NVDA [--date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import sys

from jev_common import DATA_DIR, load_json, today_str

HEADLINE_WIDTH = 78
DROPPED_PREVIEW = 20  # how many dropped items to print, highest relevance first


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--date", default=None, help="defaults to today (UTC)")
    a = ap.parse_args()
    date = a.date or today_str()

    path = DATA_DIR / "evidence" / a.ticker / f"{date}.json"
    pack = load_json(path)
    if pack is None:
        sys.exit(f"no cleaned evidence at {path}; run clean_evidence.py first")

    items = pack["items"]
    usage = pack.get("usage_tokens", {})
    print(f"{a.ticker} {date}  kept={len(items)} dropped={len(pack.get('dropped', []))}  "
          f"tokens_total={usage.get('total', '?')}")
    print(f"{'imp':>5}  {'kind':30} {'topic':26} {'claims':20} headline")
    print("-" * 130)
    for it in items:
        claims = ",".join(it.get("bearing", [])) or "-"
        headline = it["headline"][:HEADLINE_WIDTH]
        print(f"{it['importance']:5.2f}  {it['kind']['choice']:30} {it['topic']['choice']:26} {claims:20} {headline}")
        print(f"{'':5}  {'':30} {'':26} {'':20} {it['source']} | {it['url']}")

    dropped = pack.get("dropped", [])
    if dropped:
        print(f"\n-- dropped (relevance below threshold), {len(dropped)} items, top {DROPPED_PREVIEW} shown --")
        for d in sorted(dropped, key=lambda x: x["relevance"], reverse=True)[:DROPPED_PREVIEW]:
            print(f"  rel={d['relevance']:.2f}  {d['headline'][:80]}  ({d['source']})")


if __name__ == "__main__":
    main()
