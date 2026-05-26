#!/usr/bin/env python3
"""Scan docs/dd/DD_{TICKER}_{YYYYMMDD}.html and emit a ticker→relative-path map
for the supply-chain pages to deep-link company rows to their DD reports.

Output: docs/supply-chain/data/dd_links.json
  (Filename intentionally non-_prefixed — GitHub Pages' Jekyll strips
   underscore-prefix files from publish output.)

Conventions:
  * Filename pattern: DD_<TICKER>_<YYYYMMDD>.html
  * For each TICKER token, keep the file with the LATEST date suffix.
  * Emit several aliases for non-US tickers so JSON nodes can match different forms:
      - "2330"    → DD_2330_20260409.html (legacy bare digits, kept if file exists)
      - "2330TW"  → DD_2330TW_20260514.html
      - "2330.TW" → DD_2330TW_20260514.html   (Yahoo-style with dot)
      - "6146T"   → DD_6146T_20260522.html
      - "6146.T"  → DD_6146T_20260522.html    (Tokyo .T suffix)
  * For US tickers (no exchange suffix) the bare ticker is the only key.

Why this exists:
  Supply-chain node JSON uses Yahoo-style tickers (2330.TW, 6146.T). DD filenames
  use a stripped form (2330TW, 6146T). The engine looks up DD links by exact
  ticker token; this script bridges the gap by emitting both forms as keys.

Re-run after adding new DD reports. Pre-commit hook recommendation:
  python3 scripts/build_supply_chain_dd_index.py
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DD_DIR = ROOT / "docs" / "dd"
OUT = ROOT / "docs" / "supply-chain" / "data" / "dd_links.json"
REL_FROM_SUPPLY_CHAIN = "../dd"  # /supply-chain/cowos.html → ../dd/DD_...html

PAT = re.compile(r"^DD_(?P<ticker>[A-Za-z0-9.]+)_(?P<date>\d{8})\.html$")


def latest_per_ticker(dd_dir: Path) -> dict[str, str]:
    """Returns {ticker: filename} keeping latest YYYYMMDD per ticker."""
    latest: dict[str, tuple[str, str]] = {}
    for p in dd_dir.glob("DD_*.html"):
        m = PAT.match(p.name)
        if not m:
            continue
        ticker = m.group("ticker")
        date = m.group("date")
        if ticker not in latest or date > latest[ticker][0]:
            latest[ticker] = (date, p.name)
    return {t: fn for t, (_d, fn) in latest.items()}


def derive_aliases(ticker: str) -> list[str]:
    """Emit alternative ticker forms used in supply-chain JSON.

    DD filenames already strip dots/punctuation. Re-add them for Yahoo-style:
      2330TW → 2330.TW (TW)
      6146T  → 6146.T  (Tokyo .T)
      6488TW → 6488.TWO won't reverse cleanly; ignore.
    """
    aliases = [ticker]
    # TW listings (legacy 4-digit and *TW suffix)
    m = re.fullmatch(r"(\d{4})TW", ticker)
    if m:
        aliases += [f"{m.group(1)}.TW"]
    # JP listings (4-digit + T)
    m = re.fullmatch(r"(\d{4})T", ticker)
    if m:
        aliases += [f"{m.group(1)}.T"]
    return aliases


def build() -> dict[str, str]:
    if not DD_DIR.exists():
        raise SystemExit(f"DD dir not found: {DD_DIR}")
    files = latest_per_ticker(DD_DIR)
    links: dict[str, str] = {}
    for ticker, fn in sorted(files.items()):
        rel = f"{REL_FROM_SUPPLY_CHAIN}/{fn}"
        for alias in derive_aliases(ticker):
            links[alias] = rel
    return links


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    links = build()
    OUT.write_text(json.dumps(links, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(links)} ticker aliases for {len(set(links.values()))} DD files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
