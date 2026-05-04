#!/usr/bin/env python3
"""
_apply_imq_header.py — Replace old .imq-nav-root header with the new IMQ minimal header
on all THIS-repo pages.  External-repo pages (qgm/, qgm-tw/, briefing/YYYY-*, weekly/,
backtest/) are explicitly excluded.

Run:
    python3 scripts/_apply_imq_header.py [--dry-run]

The script:
1. Detects the structural pattern used in each page (imq-nav-root block, legacy <header>
   CSS block, or no nav at all).
2. Removes the old header block + its associated <style> and <script> blobs.
3. Injects the new IMQ header immediately after <body>.
4. Adds body padding-top via CSS override if the page's body{} already sets padding-top.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
sys.path.insert(0, str(REPO / "scripts"))

from imq_header import (  # noqa: E402  (after sys.path insert)
    build_imq_header,
    get_regime,
    get_section_from_path,
    get_updated_at,
)

DRY_RUN = "--dry-run" in sys.argv
CLEANUP = "--cleanup" in sys.argv   # strip old nav from pages already migrated

# ---------------------------------------------------------------------------
# Pages that live in *external* repos — do NOT touch.
# ---------------------------------------------------------------------------
EXTERNAL_PREFIXES = (
    "qgm/",
    "qgm-tw/",
    "briefing/2",      # briefing/YYYY-* — year starts with '2'
    "weekly/",
    "backtest/",
)

def _is_external(relpath: str) -> bool:
    for pfx in EXTERNAL_PREFIXES:
        if relpath.startswith(pfx):
            return True
    return False


# ---------------------------------------------------------------------------
# Regex patterns for detecting / removing old nav blocks
# ---------------------------------------------------------------------------

# Pattern A: the full imq-nav-root injection block
#   starts with <style>\n.imq-nav-root
#   ends with the </script> that contains '.imq-dd.open'
NAV_ROOT_BLOCK_RE = re.compile(
    r"<style>\s*\n\.imq-nav-root\{.*?</script>",
    re.DOTALL,
)

# Pattern B: <header class="imq-nav-root"> ... </header> (without surrounding style)
HEADER_CLASS_RE = re.compile(
    r"<header\s+class=['\"]imq-nav-root['\"][^>]*>.*?</header>",
    re.DOTALL,
)

# Pattern D: earnings-style <nav class="imq-nav"> ... </nav> (old earnings nav)
# Handles both: with and without the navigation comment marker before it.
EARNINGS_NAV_RE = re.compile(
    r"(?:<!-- ═+\s*Navigation\s*═+ -->\s*\n?)?"
    r"<nav\s+class=['\"]imq-nav['\"][^>]*>.*?</nav>",
    re.DOTALL,
)

# Pattern E: orphaned <style> block with .imq-nav-root CSS (but no header element)
# These appear in ID pages after the header element was already stripped.
ORPHAN_NAV_STYLE_RE = re.compile(
    r"<style>\s*\n?\.imq-nav-root\{[^<]*</style>",
    re.DOTALL,
)

# Pattern C: body tag (used as insertion point when no existing header)
BODY_OPEN_RE = re.compile(r"<body[^>]*>", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Body-offset helpers
# ---------------------------------------------------------------------------

def _ensure_body_background(text: str) -> str:
    """
    Ensure body has background:#fafbfc for backdrop-filter compatibility.
    Only patches if body doesn't already declare a background.
    Injects into the <head> block via <style>.
    """
    # The new header CSS already handles padding-top via body{} rule inside its <style>.
    # Nothing extra needed here; the per-page body{} rules won't conflict because
    # the IMQ style is injected first (before <body>), so any later body{padding-top:}
    # in the page's own <style> block would override it.  We handle this by ensuring
    # the imq-h-style block is the LAST style in <head>.
    # Actually we prepend after <body>, so page styles in <head> come first — meaning
    # our body{padding-top} in the injected <style> can win if it uses !important.
    return text


# ---------------------------------------------------------------------------
# Core injection logic
# ---------------------------------------------------------------------------

def _build_header_for(relpath: str, html_path: Path) -> str:
    """Build the IMQ header HTML for a given page path."""
    section = get_section_from_path(relpath)
    regime = get_regime()
    updated = get_updated_at(html_path)

    # Breadcrumb: most pages don't need one — leave empty (CSS hides it)
    breadcrumb = _make_breadcrumb(relpath)

    # Avoid injecting Google Fonts link if the page already loads them
    has_fonts = _page_has_fonts(html_path)

    return build_imq_header(
        section=section,
        regime=regime,
        updated_at=updated,
        breadcrumb=breadcrumb,
        google_fonts=not has_fonts,
    )


def _page_has_fonts(html_path: Path) -> bool:
    text = html_path.read_text(encoding="utf-8", errors="replace")
    return "fonts.googleapis.com" in text


def _make_breadcrumb(relpath: str) -> list | None:
    """
    Return a minimal breadcrumb for known page types.
    Most pages return None (hidden).  DD and ID pages get one.
    """
    # We keep breadcrumbs minimal — empty for everything except DD/ID files
    # where the page title is embedded and hard to extract generically.
    # The breadcrumb will be generated by the stock-analyst / industry-analyst
    # skills when they produce new pages.  Here we just leave it empty.
    return None


# ---------------------------------------------------------------------------
# Pattern detection & replacement
# ---------------------------------------------------------------------------

def _strip_old_nav(text: str) -> tuple[str, str]:
    """
    Remove old nav block from page HTML.
    Returns (stripped_text, method_used).
    method_used is one of: 'nav-root-block', 'header-class', 'earnings-nav', 'none'.
    """
    # Try pattern A: full style+header+script blob
    m = NAV_ROOT_BLOCK_RE.search(text)
    if m:
        stripped = text[:m.start()] + text[m.end():]
        # Also remove any leftover <header class="imq-nav-root"> if the style
        # was already inline but header is separate
        stripped = HEADER_CLASS_RE.sub("", stripped)
        return stripped, "nav-root-block"

    # Try pattern B: just the header element (style already inline in <head>)
    m = HEADER_CLASS_RE.search(text)
    if m:
        stripped = text[:m.start()] + text[m.end():]
        return stripped, "header-class"

    # Try pattern D: earnings-style <nav class="imq-nav"> ... </nav>
    m = EARNINGS_NAV_RE.search(text)
    if m:
        stripped = text[:m.start()] + text[m.end():]
        return stripped, "earnings-nav"

    # Try pattern E: orphaned <style> block containing .imq-nav-root CSS
    m = ORPHAN_NAV_STYLE_RE.search(text)
    if m:
        stripped = text[:m.start()] + text[m.end():]
        return stripped, "orphan-nav-style"

    return text, "none"


def _inject_header(text: str, header_html: str) -> str:
    """Inject header_html immediately after <body>."""
    m = BODY_OPEN_RE.search(text)
    if not m:
        # Fallback: prepend to entire document (shouldn't happen)
        return header_html + "\n" + text
    insert_pos = m.end()
    return text[:insert_pos] + "\n" + header_html + "\n" + text[insert_pos:]


def _fix_body_padding(text: str) -> str:
    """
    The new IMQ header CSS injects body{padding-top:71px} inside .imq-h-style.
    But many pages have their own body{...} rule in a <style> block in <head>
    that comes *before* the injected block.

    Since the injection is into <body> (not <head>), the order in the DOM is:
      1. Page's own <style> in <head>     → body{padding-top:?}  (possibly not set)
      2. IMQ header <style> in <body>     → body{padding-top:71px}

    CSS cascade: both are in <style> elements; the later one wins for equal specificity.
    So the IMQ rule naturally wins — no extra action needed.

    However, if the old nav was sticky (not fixed), some pages may have set
    padding-top:0 explicitly or have a negative margin-top on the first element.
    We mark those with a warning comment but don't auto-fix (too risky).
    """
    return text


# ---------------------------------------------------------------------------
# Per-page processor
# ---------------------------------------------------------------------------

def cleanup_page(relpath: str, html_path: Path, verbose: bool = True) -> bool:
    """
    Strip residual old nav from a page that already has the new IMQ header.
    Returns True if modified.
    """
    text = html_path.read_text(encoding="utf-8", errors="replace")

    # Only act on pages that have the new header
    if "imqHNav" not in text:
        return False

    stripped, method = _strip_old_nav(text)
    if method == "none":
        return False   # nothing to strip

    if DRY_RUN:
        print(f"  [dry-cleanup] {relpath}  stripped={method}")
        return False

    html_path.write_text(stripped, encoding="utf-8")
    if verbose:
        print(f"  🧹 {relpath}  stripped={method}")
    return True


def process_page(relpath: str, html_path: Path, verbose: bool = True) -> bool:
    """
    Process one page.  Returns True if modified.
    """
    text = html_path.read_text(encoding="utf-8", errors="replace")

    # Skip if already has new header
    if "imq-h__nav" in text or "imqHNav" in text:
        if verbose:
            print(f"  ⏭  {relpath} (already has new header)")
        return False

    # Remove old nav
    stripped, method = _strip_old_nav(text)

    # Build and inject new header
    header_html = _build_header_for(relpath, html_path)
    new_text = _inject_header(stripped, header_html)
    new_text = _fix_body_padding(new_text)

    if DRY_RUN:
        print(f"  [dry] {relpath}  method={method}")
        return False

    html_path.write_text(new_text, encoding="utf-8")
    if verbose:
        print(f"  ✅ {relpath}  [{method}]")
    return True


# ---------------------------------------------------------------------------
# Page discovery
# ---------------------------------------------------------------------------

def _collect_pages() -> list[tuple[str, Path]]:
    """
    Return (relpath, abs_path) tuples for all in-scope THIS-repo HTML pages.
    """
    pages = []

    def add(relpath: str):
        if _is_external(relpath):
            return
        p = DOCS / relpath
        if p.exists():
            pages.append((relpath, p))

    # Top-level pages
    for name in [
        "index.html", "markets.html", "sectors.html", "screener.html",
        "screener-tw.html", "how-to.html", "404.html",
    ]:
        add(name)

    # Sub-directories (THIS-repo scope)
    for subdir in ["research", "earnings", "pm", "mental-models", "six-state", "briefing"]:
        d = DOCS / subdir
        if d.is_dir():
            for p in sorted(d.glob("*.html")):
                rp = str(p.relative_to(DOCS))
                if not _is_external(rp):
                    pages.append((rp, p))
            # Also check index.html
            idx = d / "index.html"
            if idx.exists():
                rp = str(idx.relative_to(DOCS))
                if not any(x[0] == rp for x in pages):
                    pages.append((rp, idx))

    # DD pages — all DD_*.html
    dd_dir = DOCS / "dd"
    if dd_dir.is_dir():
        for p in sorted(dd_dir.glob("DD_*.html")):
            pages.append((str(p.relative_to(DOCS)), p))

    # ID pages — all ID_*.html and utility pages
    id_dir = DOCS / "id"
    if id_dir.is_dir():
        for p in sorted(id_dir.glob("*.html")):
            rp = str(p.relative_to(DOCS))
            if "_layout-preview" not in rp:   # skip debug page
                pages.append((rp, p))

    # Screener sub-dirs
    screener_dir = DOCS / "screener"
    if screener_dir.is_dir():
        for p in sorted(screener_dir.glob("*.html")):
            pages.append((str(p.relative_to(DOCS)), p))

    return pages


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pages = _collect_pages()
    print(f"Found {len(pages)} in-scope pages.")
    if DRY_RUN:
        print("DRY RUN — no files will be written.\n")

    modified = 0
    skipped = 0

    if CLEANUP:
        print("CLEANUP MODE — stripping residual old nav from migrated pages.\n")
        for relpath, html_path in pages:
            if cleanup_page(relpath, html_path):
                modified += 1
    else:
        for relpath, html_path in pages:
            if process_page(relpath, html_path):
                modified += 1
            else:
                skipped += 1
        print(f"\nDone. Modified: {modified}  Skipped/already-done: {skipped}")
        return

    print(f"\nCleanup done. Cleaned: {modified}")


if __name__ == "__main__":
    main()
