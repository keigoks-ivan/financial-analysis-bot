#!/usr/bin/env python3
"""DD v12.3 upgrade status — bootstrap & live progress for batch upgrade.

Read-only scan of docs/dd/*.html. Per-ticker latest detection. Schema parse
from <script id="dd-meta"> JSON. Output the work manifest seed (markdown table)
or progress report.

Usage:
  python3 scripts/dd_v12_3_status.py              # write notes/site-internal/dd/_v12_3_manifest.md (won't overwrite if exists)
  python3 scripts/dd_v12_3_status.py --force      # overwrite manifest (DESTROYS in-flight claims)
  python3 scripts/dd_v12_3_status.py --report     # progress counts (reads existing manifest)
  python3 scripts/dd_v12_3_status.py --stdout     # print seed table to stdout, don't write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DD_DIR = ROOT / "docs" / "dd"
# Manifest is internal scaffolding — lives OUTSIDE the published docs/ tree.
MANIFEST = ROOT / "notes" / "site-internal" / "dd" / "_v12_3_manifest.md"

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
META_TAG_RE = re.compile(
    r'<meta\s+name="dd-schema-version"\s+content="(v12\.[0-9]+)"',
)
SCHEMA_FIELD_RE = re.compile(r'"schema"\s*:\s*"(v12\.[0-9]+)"')
FILENAME_RE = re.compile(
    r"^DD_(?P<ticker>[A-Z0-9]+)(?P<vinfix>_v\d+)?_(?P<date>\d{8})(?P<suffix>_v\d+)?\.html$"
)

# In-flight in another window — never claim
SKIP_TICKERS = {"META", "CRDO", "DIS"}


def parse_filename(name: str):
    m = FILENAME_RE.match(name)
    if not m:
        return None
    return {
        "ticker": m.group("ticker"),
        "date": m.group("date"),
        "filename": name,
    }


def detect_schema(html: str) -> str:
    """Return 'v12.0' / 'v12.1' / 'v12.2' / 'v12.3' / 'pre-v12'."""
    mt = META_TAG_RE.search(html)
    if mt:
        return mt.group(1)
    mj = DD_META_RE.search(html)
    if mj:
        sf = SCHEMA_FIELD_RE.search(mj.group(1))
        if sf:
            return sf.group(1)
        # has dd-meta JSON but no schema field → treat as v12.0 era
        return "v12.0"
    return "pre-v12"


def latest_per_ticker():
    """Return dict[ticker] = {filename, date, schema_version, size_kb}."""
    files_by_ticker = defaultdict(list)
    for path in DD_DIR.glob("DD_*.html"):
        info = parse_filename(path.name)
        if not info:
            continue
        files_by_ticker[info["ticker"]].append((info["date"], path))

    latest = {}
    for ticker, items in files_by_ticker.items():
        items.sort(key=lambda x: x[0], reverse=True)
        date, path = items[0]
        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            continue
        schema = detect_schema(html)
        size_kb = path.stat().st_size / 1024
        latest[ticker] = {
            "filename": path.name,
            "date": date,
            "schema": schema,
            "size_kb": round(size_kb, 1),
        }
    return latest


def status_for(ticker: str, schema: str) -> str:
    if ticker in SKIP_TICKERS:
        return "skip"
    if schema == "v12.3":
        return "dca_only"
    return "pending"


def category_label(schema: str) -> str:
    if schema == "v12.3":
        return "v12.3 (DCA only)"
    if schema in ("v12.0", "v12.1", "v12.2"):
        return f"legacy ({schema})"
    return "pre-v12 (heavy)"


def build_manifest(latest: dict) -> str:
    """Generate manifest markdown."""
    rows = []
    counts = defaultdict(int)
    for ticker in sorted(latest.keys()):
        info = latest[ticker]
        st = status_for(ticker, info["schema"])
        notes_parts = []
        if st == "skip":
            notes_parts.append("in flight (other window)")
        if info["schema"] == "pre-v12":
            notes_parts.append("pre-v12-heavy")
        if info["size_kb"] < 80 and st != "skip":
            notes_parts.append(f"under-80kb ({info['size_kb']}kb)")
        notes = "; ".join(notes_parts) if notes_parts else "–"
        rows.append({
            "ticker": ticker,
            "latest_dd": info["filename"],
            "schema": info["schema"],
            "size_kb": info["size_kb"],
            "status": st,
            "claimed_by": "–",
            "notes": notes,
        })
        counts[st] += 1
        counts[f"_schema_{info['schema']}"] += 1

    lines = []
    lines.append("# DD v12.3 Upgrade Manifest")
    lines.append("")
    lines.append("**Live work tracker.** Each window: pull → claim 3 `pending` (or `dca_only`) → mark `in_progress` + window-id → push manifest → do work → commit batch (DD + DCA + manifest `done`) → push.")
    lines.append("")
    lines.append("Trigger skill: `/dd-v12-3-upgrade 3`  (or natural: `跑 v12.3 升級 3 檔`)")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- **pending** (legacy → full body upgrade + DCA cascade): {counts.get('pending', 0)}")
    lines.append(f"- **dca_only** (already v12.3, just DCA cascade audit): {counts.get('dca_only', 0)}")
    lines.append(f"- **skip** (META/CRDO/DIS in flight elsewhere): {counts.get('skip', 0)}")
    lines.append(f"- **total tickers**: {len(rows)}")
    lines.append("")
    lines.append("Schema breakdown (latest DD per ticker):")
    for k in ["v12.3", "v12.2", "v12.1", "v12.0", "pre-v12"]:
        c = counts.get(f"_schema_{k}", 0)
        if c:
            lines.append(f"- {k}: {c}")
    lines.append("")
    lines.append("## Hard gates (per upgrade)")
    lines.append("")
    lines.append("- DD post-upgrade size **≥ 80 KB**")
    lines.append("- DCA post-cascade size **≥ 50 KB**")
    lines.append("- No-fabricate: every number in §8.H / §11 / §12 / §10 peer / §13.4 needs inline source citation")
    lines.append("- Pre-flight WebSearch ≥ 3 (customer concentration / SBC / M&A 5Y)")
    lines.append("- Cold-review every 5 batch (sonnet sub-agent on random ticker)")
    lines.append("")
    lines.append("## Manifest")
    lines.append("")
    lines.append("| ticker | latest_dd | schema | size_kb | status | claimed_by | notes |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append(
            f"| {r['ticker']} | {r['latest_dd']} | {r['schema']} | {r['size_kb']} | {r['status']} | {r['claimed_by']} | {r['notes']} |"
        )
    lines.append("")
    return "\n".join(lines)


def parse_existing_manifest_status(text: str) -> dict:
    """Read existing manifest, count by status. Used for --report."""
    counts = defaultdict(int)
    in_table = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("|---"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            in_table = False
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 7:
            continue
        status = cols[4]
        counts[status] += 1
    return dict(counts)


def cmd_report():
    if not MANIFEST.exists():
        print(f"manifest not found: {MANIFEST}", file=sys.stderr)
        print("run without --report first to generate it.", file=sys.stderr)
        sys.exit(1)
    counts = parse_existing_manifest_status(MANIFEST.read_text(encoding="utf-8"))
    total = sum(counts.values())
    print(f"DD v12.3 progress  ({total} tickers)")
    print()
    for k in ["pending", "in_progress", "dca_only", "done", "skip"]:
        c = counts.get(k, 0)
        bar = "█" * int(c / max(total, 1) * 40)
        print(f"  {k:13s} {c:4d}  {bar}")
    print()
    if counts.get("pending", 0) == 0 and counts.get("in_progress", 0) == 0 and counts.get("dca_only", 0) == 0:
        print("DONE — all tickers processed (or skipped).")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", action="store_true", help="show progress counts (reads existing manifest)")
    ap.add_argument("--force", action="store_true", help="overwrite existing manifest (DESTROYS in-flight claims)")
    ap.add_argument("--stdout", action="store_true", help="print seed to stdout, don't write")
    args = ap.parse_args()

    if args.report:
        cmd_report()
        return

    latest = latest_per_ticker()
    text = build_manifest(latest)

    if args.stdout:
        sys.stdout.write(text)
        return

    if MANIFEST.exists() and not args.force:
        print(f"manifest exists: {MANIFEST}", file=sys.stderr)
        print("use --force to overwrite (will destroy any in-flight claims) or --stdout to preview.", file=sys.stderr)
        sys.exit(1)

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(text, encoding="utf-8")
    print(f"wrote {MANIFEST.relative_to(ROOT)} ({len(latest)} tickers)")


if __name__ == "__main__":
    main()
