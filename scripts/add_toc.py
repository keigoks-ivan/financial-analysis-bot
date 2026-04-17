#!/usr/bin/env python3
"""Retrofit TOC into all docs/dd/DD_*.html files.

Idempotent: files already containing `class="dd-toc"` (new TOC) or
`href="#s1"` (legacy TOC in v6-v9 DDs) are skipped.

Strategy:
- Add `id="sec-N"` to each `<h2>` that starts with `§N` (N in 1..13).
  This works for both bare `<h2>§N...</h2>` and `<h2 class="section-title">§N...</h2>`.
- Insert TOC nav after `<div class="container">` (fallback: after `<body>`).
- Append TOC CSS before `</style>`.
- Does NOT touch SKILL.md — future DDs rely on SKILL.md updates.

Usage:
  python scripts/add_toc.py
"""
import re
from pathlib import Path

DD_DIR = Path(__file__).parent.parent / "docs" / "dd"

TOC_CSS = """
/* DD TOC (retrofit) */
.dd-toc{background:#F1F5F9;border-left:4px solid var(--accent,#3B82F6);padding:14px 18px;margin-bottom:20px;border-radius:2px}
.dd-toc .toc-title{font-weight:700;color:#1E3A5F;font-size:14px;margin-bottom:8px}
.dd-toc .toc-list{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:6px}
.dd-toc .toc-list li a{display:inline-block;padding:4px 10px;background:#fff;color:#1E3A5F;text-decoration:none;font-size:12.5px;border:1px solid #cbd5e1;border-radius:2px;font-weight:500}
.dd-toc .toc-list li a:hover{background:#1E3A5F;color:#fff;border-color:#1E3A5F}
html{scroll-behavior:smooth}
h2[id^="sec-"],section[id^="sec-"],div[id^="sec-"]{scroll-margin-top:60px}
@media print{.dd-toc{display:none}}
"""

SECTION_LABELS = {
    1: "§1 結論", 2: "§2 序章", 3: "§3 論點", 4: "§4 財報",
    5: "§5 門檻", 6: "§6 成長", 7: "§7 護城河", 8: "§8 財務",
    9: "§9 產業", 10: "§10 治理", 11: "§11 估值", 12: "§12 R:R",
    13: "§13 辯論",
}

# Match section-header elements with `§N` (N in 1..13) across DD schema variants.
# Negative lookahead (?![.0-9]) prevents matching "§1" in "§1.5" or truncating "§11" to "§1".
H2_SEC_RE = re.compile(
    r'<h2(\s[^>]*)?>\s*§\s*(1[0-3]|[1-9])(?![.0-9])',
    re.DOTALL,
)
H1_SEC_RE = re.compile(
    r'<h1(\s[^>]*)?>\s*§\s*(1[0-3]|[1-9])(?![.0-9])',
    re.DOTALL,
)
DIV_TITLE_RE = re.compile(
    r'<div(\s[^>]*class="[^"]*\bsection-title\b[^"]*"[^>]*)>\s*§\s*(1[0-3]|[1-9])(?![.0-9])',
    re.DOTALL,
)
DIV_HEADER_RE = re.compile(
    r'<div(\s[^>]*class="[^"]*\bsection-header\b[^"]*"[^>]*)>\s*(?:<span[^>]*>)?\s*§\s*(1[0-3]|[1-9])(?![.0-9])',
    re.DOTALL,
)

LEGACY_TOC_RE = re.compile(r'href="#s[0-9]')


def build_toc_html(section_nums):
    items = "".join(
        f'      <li><a href="#sec-{n}">{SECTION_LABELS.get(n, f"§{n}")}</a></li>\n'
        for n in section_nums
    )
    return (
        '<nav class="dd-toc">\n'
        '  <div class="toc-title">目錄</div>\n'
        '  <ul class="toc-list">\n'
        f'{items}'
        '  </ul>\n'
        '</nav>\n'
    )


def process_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if 'class="dd-toc"' in html:
        return False
    if LEGACY_TOC_RE.search(html):
        # Very old DDs with their own TOC; skip to avoid duplication.
        return False

    section_nums = []

    def make_id_adder(tag_name):
        def add_id(m):
            attrs = m.group(1) or ''
            n_str = m.group(2)
            n = int(n_str)
            if 'id="sec-' in attrs:
                return m.group(0)
            new_attrs = (attrs + f' id="sec-{n}"') if attrs else f' id="sec-{n}"'
            section_nums.append(n)
            orig = m.group(0)
            i = orig.index('§')
            return f'<{tag_name}{new_attrs}>{orig[i:]}'
        return add_id

    html_new = H2_SEC_RE.sub(make_id_adder('h2'), html)
    html_new = H1_SEC_RE.sub(make_id_adder('h1'), html_new)
    html_new = DIV_TITLE_RE.sub(make_id_adder('div'), html_new)
    html_new = DIV_HEADER_RE.sub(make_id_adder('div'), html_new)

    if not section_nums:
        return False

    # Dedupe while preserving order
    seen = set()
    ordered = [n for n in section_nums if not (n in seen or seen.add(n))]

    toc = build_toc_html(ordered)

    if '<div class="container">' in html_new:
        html_new = html_new.replace(
            '<div class="container">',
            '<div class="container">\n' + toc,
            1,
        )
    else:
        html_new = re.sub(
            r'(<body[^>]*>)',
            rf'\1\n{toc}',
            html_new,
            count=1,
        )

    if '</style>' in html_new:
        html_new = html_new.replace('</style>', TOC_CSS + '</style>', 1)

    path.write_text(html_new, encoding="utf-8")
    return True


def main():
    modified = 0
    skipped = 0
    for f in sorted(DD_DIR.glob("DD_*.html")):
        if process_file(f):
            modified += 1
        else:
            skipped += 1
    print(f"Modified: {modified}  |  Skipped: {skipped}  |  Total: {modified + skipped}")


if __name__ == "__main__":
    main()
