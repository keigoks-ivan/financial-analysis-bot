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


def scan_dd_files():
    """Parse DD_{TICKER}_{YYYYMMDD}.html filenames."""
    entries = []
    for f in sorted(DD_DIR.glob("DD_*.html")):
        m = re.match(r"DD_(.+)_(\d{4})(\d{2})(\d{2})\.html", f.name)
        if not m:
            continue
        ticker = m.group(1)
        date_str = f"{m.group(2)}-{m.group(3)}-{m.group(4)}"
        entries.append({"ticker": ticker, "date": date_str, "href": f"/dd/{f.name}"})
    # Sort by date desc, then ticker
    entries.sort(key=lambda e: (e["date"], e["ticker"]), reverse=True)
    return entries


def build_rows(entries):
    rows = []
    for e in entries:
        rows.append(
            f'<tr class="searchable">\n'
            f'  <td><strong>{e["ticker"]}</strong></td>\n'
            f'  <td><span class="tag tag-dd">深度研究</span></td>\n'
            f'  <td>{e["date"]}</td>\n'
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
