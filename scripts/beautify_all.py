#!/usr/bin/env python3
"""
beautify_all.py — Apply consistent styling improvements to all HTML files under docs/.

Actions per file:
  1. Nav: Ensure "六狀態機" link exists after "回測" link (both nav patterns).
  2. DD pages  (docs/dd/*.html):      Inject responsive CSS if @media absent.
  3. Report pages (docs/report/*.html): Inject responsive CSS if @media absent.
  4. Briefing pages (docs/briefing/*.html): Inject card-styling CSS if absent.

Skips: docs/backtest/ and docs/six-state/ (already good).
"""

import re
from pathlib import Path

DOCS_DIR = Path("/Users/ivanchang/Desktop/financial-analysis-bot/docs")

# ---------------------------------------------------------------------------
# CSS snippets
# ---------------------------------------------------------------------------

DD_RESPONSIVE_CSS = """\
@media(max-width:768px){
  .container{padding:0 12px}
  .debate{grid-template-columns:1fr !important}
  .rr{grid-template-columns:1fr !important}
  table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
  h2.section{font-size:16px}
  .kpi-row{flex-wrap:wrap}
  .kpi-row>div{min-width:45%}
  body{font-size:13px}
}"""

REPORT_RESPONSIVE_CSS = """\
@media(max-width:768px){
  .dim-grid{grid-template-columns:1fr}
  .score-hero{flex-direction:column;text-align:center}
  .radar-risks{grid-template-columns:1fr}
  .cap-grid{grid-template-columns:1fr}
  table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
}"""

BRIEFING_CARD_CSS = """\
.section{margin-bottom:24px}
table{border-radius:8px;overflow:hidden}"""

# ---------------------------------------------------------------------------
# Nav injection helpers
# ---------------------------------------------------------------------------

SIX_STATE_LINK_FLEX = '<a href="/six-state/" style="color:#6b7280;text-decoration:none;">六狀態機</a>'
SIX_STATE_LINK_NAV  = ' <a href="/six-state/">六狀態機</a>'


def inject_nav_flex(content: str) -> tuple[str, bool]:
    """Handle the flex-div nav pattern: <div style="display:flex;gap:16px;"> ... </div>"""
    if "六狀態機" in content:
        return content, False

    # Look for the回測 link inside the flex-gap:16px nav block
    # Pattern: <a href="/backtest/" ...>回測</a>
    pattern = r'(<a\s[^>]*href="/backtest/"[^>]*>回測</a>)'
    match = re.search(pattern, content)
    if not match:
        return content, False

    old = match.group(0)
    new = old + "\n    " + SIX_STATE_LINK_FLEX
    return content.replace(old, new, 1), True


def inject_nav_tag(content: str) -> tuple[str, bool]:
    """Handle the <nav> tag pattern: <nav><a href="/">首頁</a> ... </nav>"""
    if "六狀態機" in content:
        return content, False

    # Look for the 回測 link inside a <nav>
    pattern = r'(<a\s[^>]*href="/backtest/"[^>]*>回測</a>)'
    match = re.search(pattern, content)
    if not match:
        return content, False

    old = match.group(0)
    new = old + SIX_STATE_LINK_NAV
    return content.replace(old, new, 1), True


def fix_nav(content: str) -> tuple[str, list[str]]:
    """Try both nav patterns; return modified content and list of changes made."""
    changes = []

    if "六狀態機" in content:
        return content, changes  # already has the link

    # Determine which pattern is present
    has_flex_nav = bool(re.search(r'display:flex;gap:16px', content))
    has_nav_tag  = bool(re.search(r'<nav>', content, re.IGNORECASE))

    if has_flex_nav:
        content, changed = inject_nav_flex(content)
        if changed:
            changes.append("nav: added 六狀態機 link (flex-div pattern)")
    elif has_nav_tag:
        content, changed = inject_nav_tag(content)
        if changed:
            changes.append("nav: added 六狀態機 link (<nav> tag pattern)")

    return content, changes


# ---------------------------------------------------------------------------
# CSS injection helpers
# ---------------------------------------------------------------------------

def inject_css_before_style_close(content: str, css: str) -> tuple[str, bool]:
    """Inject css text just before the first </style> tag."""
    idx = content.find("</style>")
    if idx == -1:
        return content, False
    insertion = "\n" + css + "\n"
    return content[:idx] + insertion + content[idx:], True


def fix_dd_css(content: str) -> tuple[str, list[str]]:
    changes = []
    if "@media" not in content:
        content, ok = inject_css_before_style_close(content, DD_RESPONSIVE_CSS)
        if ok:
            changes.append("dd: injected responsive @media CSS")
    return content, changes


def fix_report_css(content: str) -> tuple[str, list[str]]:
    """Only inject the mobile-responsive rules that are missing."""
    changes = []
    # We check for specific selectors from our snippet to avoid duplicating
    # rules that may already exist in a more complete form
    sentinel = ".radar-risks{grid-template-columns:1fr}"
    if sentinel not in content and "radar-risks" not in content:
        # Full responsive block missing — inject it
        content, ok = inject_css_before_style_close(content, REPORT_RESPONSIVE_CSS)
        if ok:
            changes.append("report: injected responsive @media CSS")
    return content, changes


def fix_briefing_css(content: str) -> tuple[str, list[str]]:
    changes = []
    sentinel = "table{border-radius:8px;overflow:hidden}"
    if sentinel not in content:
        content, ok = inject_css_before_style_close(content, BRIEFING_CARD_CSS)
        if ok:
            changes.append("briefing: injected card-styling CSS")
    return content, changes


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_file(path: Path) -> list[str]:
    """Process a single HTML file. Return list of changes made."""
    content = path.read_text(encoding="utf-8")
    all_changes: list[str] = []

    # 1. Nav fix (all files)
    content, nav_changes = fix_nav(content)
    all_changes.extend(nav_changes)

    # 2. Category-specific CSS
    rel = path.relative_to(DOCS_DIR)
    top_dir = rel.parts[0] if len(rel.parts) > 1 else ""

    if top_dir == "dd":
        content, css_changes = fix_dd_css(content)
        all_changes.extend(css_changes)
    elif top_dir == "report":
        content, css_changes = fix_report_css(content)
        all_changes.extend(css_changes)
    elif top_dir == "briefing":
        content, css_changes = fix_briefing_css(content)
        all_changes.extend(css_changes)

    if all_changes:
        path.write_text(content, encoding="utf-8")

    return all_changes


def main():
    skip_dirs = {"backtest", "six-state"}

    html_files = sorted(DOCS_DIR.rglob("*.html"))
    files_to_process = [
        f for f in html_files
        if not (len(f.relative_to(DOCS_DIR).parts) > 0
                and f.relative_to(DOCS_DIR).parts[0] in skip_dirs)
    ]

    print(f"Found {len(html_files)} HTML files total.")
    print(f"Skipping backtest/ and six-state/ → processing {len(files_to_process)} files.\n")

    total_fixed = 0
    for path in files_to_process:
        changes = process_file(path)
        rel = path.relative_to(DOCS_DIR)
        if changes:
            total_fixed += 1
            print(f"  FIXED  {rel}")
            for c in changes:
                print(f"         • {c}")
        else:
            print(f"  ok     {rel}")

    print(f"\nDone. {total_fixed} file(s) modified out of {len(files_to_process)} processed.")


if __name__ == "__main__":
    main()
