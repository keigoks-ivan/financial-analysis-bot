#!/usr/bin/env python3
"""Build docs/rss.xml — RSS 2.0 feed of the latest 50 dated research entries.

Shares the report inventory with build_search_index.py (single source of
truth via collect_inventory). Zero-churn write. Does NOT touch
docs/feed.xml (an orphaned podcast shell).
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from email.utils import format_datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_search_index import collect_inventory, _write_if_changed  # noqa: E402

SITE = "https://research.investmquest.com"
FEED_URL = f"{SITE}/rss.xml"
TITLE = "InvestMQuest Research — 研究發布"
DESC = "獨立投資研究：個股 DD、產業 ID、總經、財報、跨資產監測的最新發布。"
LIMIT = 50


def _esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _pubdate(d: str) -> str:
    dt = datetime.strptime(d, "%Y-%m-%d").replace(
        hour=12, tzinfo=timezone.utc)
    return format_datetime(dt)


def build_rss() -> str:
    entries = [e for e in collect_inventory() if e["d"]][:LIMIT]
    # channel lastBuildDate pinned to newest item's pubDate -> zero-churn stable
    last = _pubdate(entries[0]["d"]) if entries else format_datetime(
        datetime(2026, 1, 1, tzinfo=timezone.utc))
    items = []
    for e in entries:
        link = SITE + e["u"]
        items.append(
            "    <item>\n"
            f"      <title>{_esc(e['t'])}</title>\n"
            f"      <link>{_esc(link)}</link>\n"
            f"      <guid isPermaLink=\"true\">{_esc(link)}</guid>\n"
            f"      <category>{_esc(e['k'])}</category>\n"
            f"      <pubDate>{_pubdate(e['d'])}</pubDate>\n"
            "    </item>"
        )
    body = "\n".join(items)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{_esc(TITLE)}</title>\n"
        f"    <link>{SITE}/</link>\n"
        f"    <description>{_esc(DESC)}</description>\n"
        "    <language>zh-Hant</language>\n"
        f"    <lastBuildDate>{last}</lastBuildDate>\n"
        f'    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>\n'
        f"{body}\n"
        "  </channel>\n"
        "</rss>\n"
    )


def main() -> None:
    xml = build_rss()
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "rss.xml")
    changed = _write_if_changed(out, xml)
    n = xml.count("<item>")
    print(f"rss.xml: {n} items, {len(xml)} bytes — "
          f"{'written' if changed else 'zero-churn'}")


if __name__ == "__main__":
    main()
