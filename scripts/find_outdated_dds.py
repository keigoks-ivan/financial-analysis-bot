#!/usr/bin/env python3
"""Detect DDs whose ticker has reported earnings AFTER the DD date.

Output: list of (ticker, dd_date, latest_post_dd_earnings_date) where
the user has a DD but earnings reports came in after — meaning DD is stale
and needs a re-run.

Stdlib only. Reads dd-meta JSON from docs/dd/DD_*.html and parses
<span class="ticker">TICKER · ...</span> entries from docs/earnings/earnings_*.html.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
DD_DIR = ROOT / "docs" / "dd"
EARNINGS_DIR = ROOT / "docs" / "earnings"

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
EARNINGS_DATE_RE = re.compile(r"earnings_(\d{4}-\d{2}-\d{2})\.html$")
TICKER_SPAN_RE = re.compile(r'<span class="ticker">([A-Z0-9.]+)\s*[·•・]')


def normalize_ticker(t: str) -> str:
    return t.upper().replace(".", "").strip()


def latest_dd_per_ticker():
    latest = {}
    for path in sorted(DD_DIR.glob("DD_*.html")):
        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            continue
        m = DD_META_RE.search(html)
        if not m:
            continue
        try:
            meta = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        t = normalize_ticker(str(meta.get("ticker", "")))
        d = str(meta.get("date", ""))
        if not t or not d:
            continue
        prev = latest.get(t)
        if prev is None or d > prev["dd_date"]:
            latest[t] = {
                "ticker": meta.get("ticker"),
                "dd_date": d,
                "dd_path": str(path.relative_to(ROOT)),
            }
    return latest


def earnings_dates_per_ticker():
    by_ticker = defaultdict(list)
    if not EARNINGS_DIR.exists():
        return by_ticker
    for path in sorted(EARNINGS_DIR.glob("earnings_*.html")):
        m = EARNINGS_DATE_RE.search(path.name)
        if not m:
            continue
        edate = m.group(1)
        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for raw in TICKER_SPAN_RE.findall(html):
            by_ticker[normalize_ticker(raw)].append(edate)
    return by_ticker


def find_outdated():
    latest_dd = latest_dd_per_ticker()
    earnings = earnings_dates_per_ticker()
    out = []
    for tnorm, info in latest_dd.items():
        post = [e for e in earnings.get(tnorm, []) if e > info["dd_date"]]
        if post:
            out.append({
                "ticker": info["ticker"],
                "dd_date": info["dd_date"],
                "earnings_date": max(post),
            })
    out.sort(key=lambda r: (r["earnings_date"], r["ticker"]), reverse=True)
    return out


def main():
    rows = find_outdated()
    if "--json" in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("No outdated DDs found — all caught up.")
        return
    print(f"Outdated DDs ({len(rows)}):")
    for r in rows:
        print(f"  {r['ticker']:<10s} DD {r['dd_date']} → earnings {r['earnings_date']}")


if __name__ == "__main__":
    main()
