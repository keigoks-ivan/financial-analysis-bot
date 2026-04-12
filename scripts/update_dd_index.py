#!/usr/bin/env python3
"""
Scan docs/dd/ for DD_*.html files and update the deep research table in
docs/research/index.html (Phase 3: homepage cleaned, reports moved to /research/).
Run after adding new DD files to auto-update the research page listing.
"""
import re
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
DD_DIR = DOCS / "dd"
INDEX = DOCS / "research" / "index.html"

VERSION_CUTOFF = "2026-04-11"  # Only show version column for DDs on/after this date
META_RE = re.compile(r'<meta\s+name="dd-schema-version"\s+content="([^"]+)"', re.IGNORECASE)


def extract_version(path: Path) -> str:
    """Read <meta name="dd-schema-version" content="vX.Y"> from DD HTML head."""
    try:
        # Read first 4KB — meta tag is always in <head>
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            head = fh.read(4096)
        m = META_RE.search(head)
        return m.group(1) if m else ""
    except OSError:
        return ""


def scan_dd_files():
    """Parse DD_{TICKER}_{YYYYMMDD}.html filenames and extract schema version."""
    entries = []
    for f in sorted(DD_DIR.glob("DD_*.html")):
        m = re.match(r"DD_(.+)_(\d{4})(\d{2})(\d{2})\.html", f.name)
        if not m:
            continue
        ticker = m.group(1)
        date_str = f"{m.group(2)}-{m.group(3)}-{m.group(4)}"
        version = extract_version(f) if date_str >= VERSION_CUTOFF else ""
        entries.append({
            "ticker": ticker,
            "date": date_str,
            "href": f"/dd/{f.name}",
            "version": version,
        })
    # Sort priority: 1) date desc, 2) ticker asc, 3) version desc
    # Apply in reverse order — Python's sort is stable, so earlier sorts
    # become tiebreakers for later ones.
    entries.sort(key=lambda e: e["version"], reverse=True)
    entries.sort(key=lambda e: e["ticker"])
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries


def build_rows(entries):
    rows = []
    for e in entries:
        version_cell = e["version"] or "&mdash;"
        rows.append(
            f'<tr class="searchable">\n'
            f'  <td><strong>{e["ticker"]}</strong></td>\n'
            f'  <td><span class="tag tag-dd">深度研究</span></td>\n'
            f'  <td>{e["date"]}</td>\n'
            f'  <td>{version_cell}</td>\n'
            f'  <td><a href="{e["href"]}">查看 &rarr;</a></td>\n'
            f'</tr>'
        )
    return "\n".join(rows)


def update_index(entries):
    html = INDEX.read_text(encoding="utf-8")

    # Target the DD tbody directly (research page uses id="dd-tbody" for this).
    # Replace everything between <tbody id="dd-tbody"> ... </tbody>.
    pattern = r'(<tbody id="dd-tbody">)\n?.*?(\s*</tbody>)'
    replacement = r'\1\n' + build_rows(entries) + r'\2'
    new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)

    if count == 0:
        print(f"ERROR: Could not find <tbody id=\"dd-tbody\"> in {INDEX}")
        return False

    INDEX.write_text(new_html, encoding="utf-8")
    return True


def main():
    entries = scan_dd_files()
    print(f"Found {len(entries)} DD files:")
    for e in entries:
        print(f"  {e['ticker']:8s} {e['date']}  {e['href']}")

    if update_index(entries):
        print(f"\nUpdated {INDEX}")
    else:
        print("\nFailed to update index.html")


if __name__ == "__main__":
    main()
