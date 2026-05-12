#!/usr/bin/env python3
"""Bootstrap docs/ds/index.html from docs/id/index.html.

Reads docs/id/index.html as a structural template and applies a series of
targeted transformations to produce an empty DS gallery page that:

  • shares the site nav chrome, toolbar, cat-jump bar, and 15 mega categories
  • carries all `<!-- subgroup-anchor: {mega}.{sub} -->` markers (so the
    industry-ds skill can insert new DS cards in the same way industry-analyst
    does for ID)
  • strips ID-specific decoration (flagship hero, tier matrix passthrough,
    article cards, meta-strip numeric counters that hard-code ID stats)
  • re-labels visible text from ID → DS terminology
  • marks the new "/ds/" nav entry as active and keeps the existing "/id/" entry

Idempotent: re-run to refresh chrome from /id/ if it evolves. WARNING: any DS
cards that have been inserted into docs/ds/index.html will be lost on re-run.
Only re-run when:
  (a) initial bootstrap (no DS cards exist yet), or
  (b) you have a way to preserve the inserted DS cards (e.g., script extracts
      them, regenerates chrome, re-injects).

Usage:
  python3 scripts/init_ds_index.py              # writes docs/ds/index.html
  python3 scripts/init_ds_index.py --dry-run    # report only, no write
  python3 scripts/init_ds_index.py --force      # overwrite even if existing
                                                  docs/ds/index.html has cards
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "id" / "index.html"
OUT = ROOT / "docs" / "ds" / "index.html"


# ─── Transformations ──────────────────────────────────────────────────────────

def t_title_and_meta(html: str) -> str:
    """Update <title>, <meta name='description'>."""
    html = re.sub(
        r"<title>產業深度報告 — InvestMQuest Research</title>",
        "<title>產業敘述報告 — InvestMQuest Research</title>",
        html,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="跨多檔個股共用的產業敘述型研究（Industry Discourse / DS），以歷史脈絡 → 供需循環 → 短中長期推估為骨架，文字 ≥ 80%、表格 ≤ 20%"',
        html,
        count=1,
    )
    return html


def t_nav_chrome(html: str) -> str:
    """Replace single ID link with two links (ID + DS), mark DS active.

    The /id/ source has:
        <a href="/id/" class="active">產業深度 ID</a>
    We want, on the /ds/ page:
        <a href="/id/">產業深度 ID</a>
        <a href="/ds/" class="active">產業敘述 DS</a>
    """
    old = '<a href="/id/" class="active">產業深度 ID</a>'
    new = (
        '<a href="/id/">產業深度 ID</a>\n'
        '          <a href="/ds/" class="active">產業敘述 DS</a>'
    )
    if old in html:
        html = html.replace(old, new, 1)
    else:
        # Fallback: try without active class
        old2 = '<a href="/id/">產業深度 ID</a>'
        if old2 in html:
            new2 = (
                '<a href="/id/">產業深度 ID</a>\n'
                '          <a href="/ds/" class="active">產業敘述 DS</a>'
            )
            html = html.replace(old2, new2, 1)
    return html


def t_breadcrumb_and_head(html: str) -> str:
    """Update breadcrumb + h1 + sub description."""
    # Breadcrumb: 產業深度 → 產業敘述
    html = re.sub(
        r'(<div class="crumb">.*?&rsaquo;)\s*產業深度\s*</div>',
        r'\1 產業敘述</div>',
        html,
        flags=re.DOTALL,
    )
    # h1
    html = re.sub(
        r"<h1>產業深度報告</h1>",
        "<h1>產業敘述報告</h1>",
        html,
    )
    # sub description — content has nested <code>, so match the whole element greedily
    # within head-row scope
    html = re.sub(
        r'<p class="sub">.*?</p>',
        '<p class="sub">跨多檔個股共用的<b>敘述型</b>產業研究，由 <code>industry-ds</code> 產出 — 以「歷史 → 現供 → 未供 → 現需 → 未需 → 短中長期推估」為骨架，文字 ≥ 80%、表格 ≤ 20%。與 <a href="/id/"><code>industry-analyst</code> 產的 ID</a> 互補（ID 表格 dashboard、DS 敘述供需循環），同 theme 可並存。</p>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def t_meta_strip(html: str) -> str:
    """Replace ID-specific meta-strip numeric chips with DS-appropriate ones."""
    # The meta-strip contains hard-coded counts like "35 已建 ID". DS starts at 0.
    # We replace the whole meta-strip with DS-version placeholders.
    new_meta_strip = (
        '<div class="meta-strip">\n'
        '      <span class="item"><b id="ds-count">0</b> 已建 DS</span>\n'
        '      <span class="item"><b id="ticker-count">0</b> 涵蓋個股</span>\n'
        '      <span class="item">敘述比 <b>≥ 80%</b></span>\n'
        '      <span class="item">表格比 <b>≤ 20%</b></span>\n'
        '      <button class="info-toggle" id="phase-info-btn">ⓘ 短中長期說明</button>\n'
        '    </div>'
    )
    html = re.sub(
        r'<div class="meta-strip">.*?</div>\s*</div>(?=\s*<div class="phase-pop")',
        new_meta_strip + "\n    </div>",
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def t_phase_pop(html: str) -> str:
    """Replace ID Phase I-IV pop content with DS short/medium/long timeframe pop."""
    new_pop = (
        '<div class="phase-pop" id="phase-info">\n'
        '    <div class="row">\n'
        '      <div><b>短期 · 12 個月內</b><br>下一輪供需缺口、capex / order book 兌現、ASP / utilization 已可觀察。</div>\n'
        '      <div><b>中期 · 1-3 年</b><br>新進入者爬坡、新世代產品迭代、地緣 / 政策 binary 落地。</div>\n'
        '      <div><b>長期 · 3-5+ 年</b><br>S 曲線位置 / TAM 滲透率 / 替代技術成熟度、結構性人口或需求轉移。</div>\n'
        '    </div>\n'
        '  </div>'
    )
    html = re.sub(
        r'<div class="phase-pop" id="phase-info">.*?</div>\s*</div>',
        new_pop,
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def t_strip_flagship(html: str) -> str:
    """Remove the <div class="flagship" id="flagship">...</div> hero block.

    DS v1.0 does not have cross-DS synthesis flagship. Strip the entire block
    (including the JS that controls its tab/toggle behavior).
    """
    # Strip flagship div (balanced)
    html = _strip_balanced_div(html, r'<div class="flagship"[^>]*>')
    # Strip flagship-related JS init (if recognizable)
    html = re.sub(
        r"<script>\s*\(function\(\)\{[^}]*flagship[^}]*\}\)\(\);?\s*</script>",
        "",
        html,
        flags=re.DOTALL,
    )
    return html


def t_strip_tier_matrix(html: str) -> str:
    """Remove <div class="tier-passthrough">...</div> block."""
    return _strip_balanced_div(html, r'<div class="tier-passthrough"[^>]*>')


def t_strip_articles(html: str) -> str:
    """Strip all <article class="topic-card..."> blocks (per-report cards)."""
    out = []
    pos = 0
    length = len(html)
    pattern = re.compile(r'<article\s+class="topic-card[^"]*"', re.IGNORECASE)
    while pos < length:
        m = pattern.search(html, pos)
        if not m:
            out.append(html[pos:])
            break
        out.append(html[pos:m.start()])
        depth = 1
        scan = m.end()
        article_close = re.compile(r"</article>", re.IGNORECASE)
        article_open = re.compile(r"<article\b", re.IGNORECASE)
        while depth > 0 and scan < length:
            next_close = article_close.search(html, scan)
            next_open = article_open.search(html, scan)
            if not next_close:
                break
            if next_open and next_open.start() < next_close.start():
                depth += 1
                scan = next_open.end()
            else:
                depth -= 1
                scan = next_close.end()
        pos = scan
    return "".join(out)


def t_count_badges(html: str) -> str:
    """Reset cat-head .count badges and cat-jump .n badges to 0."""
    html = re.sub(
        r'(<span class="count">)\s*\d+\s*份(</span>)',
        r"\g<1>0 份\g<2>",
        html,
    )
    # cat-jump .n badges have format "<span class="n">19 份</span>" (含「份」)
    html = re.sub(
        r'(<span class="n">)\s*\d+(\s*份\s*</span>)',
        r"\g<1>0\g<2>",
        html,
    )
    # Bare format without "份" (fallback)
    html = re.sub(
        r'(<span class="n">)\s*\d+(\s*</span>)',
        r"\g<1>0\g<2>",
        html,
    )
    return html


def t_help_box(html: str) -> str:
    """Update the bottom helper box (如何新增產業 ID → DS) + freshness legend."""
    new_box = (
        '<div style="margin-top:32px;padding:14px 18px;background:#F5F3FF;'
        'border-left:4px solid #7C3AED;border-radius:6px;font-size:12.5px;'
        'color:#4C1D95;line-height:1.65">\n'
        '    <strong>🚀 如何新增產業 DS：</strong><br>\n'
        '    對 Claude Code 說「{主題} ds」或「ds {主題}」即自動觸發 '
        '<code>industry-ds</code> skill；產出會自動放入對應類別。<br>\n'
        '    <strong>鮮度燈：</strong>🟢 新鮮 ｜ 🟡 history 過期（&gt; 730 天）'
        '｜ 🟠 supply-demand 過期（&gt; 180 天）｜ 🔴 forecast 過期（&gt; 60 天）\n'
        '  </div>'
    )
    html = re.sub(
        r'<div style="margin-top:32px;padding:14px 18px;background:#F5F3FF;[^"]*"[^>]*>\s*'
        r'<strong>🚀 如何新增產業 ID.*?</div>',
        new_box,
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def t_footer(html: str) -> str:
    """Update footer line to reflect DS skill."""
    html = re.sub(
        r"InvestMQuest Research · 產業深度由 industry-analyst v[\d.]+ 自動生成.*?</div>",
        "InvestMQuest Research · 產業敘述由 industry-ds v1.0 自動生成 · 沿用 Claude Opus 深度研究能力</div>",
        html,
        flags=re.DOTALL,
    )
    return html


def t_strip_flagship_js(html: str) -> str:
    """Strip the JS block that initializes flagship tabs / fl-pane behaviour.

    After stripping the flagship div, this JS would crash on null .fl-tab refs.
    Strip the entire flagship JS block (from `// Flagship tabs` through `]];}`).
    """
    # Pattern: from "// Flagship tabs" comment through next "// " comment or </script>
    html = re.sub(
        r"//\s*Flagship tabs.*?(?=//\s|</script>)",
        "",
        html,
        flags=re.DOTALL,
        count=1,
    )
    # Also strip flagship toggle/collapse code if present
    html = re.sub(
        r"//\s*Flagship.*?(?=//\s|</script>)",
        "",
        html,
        flags=re.DOTALL,
    )
    return html


def t_subgroup_comments(html: str) -> str:
    """Update the helper text inside cat-body that says '新 ID 由 industry-analyst...'.

    These are HTML comments + visible help text inside each empty cat-body.
    """
    html = html.replace(
        "新 ID 由 industry-analyst skill 生成時",
        "新 DS 由 industry-ds skill 生成時",
    )
    html = html.replace(
        "新 ID 由 industry-ds skill 生成時",  # already-rewritten in earlier pass
        "新 DS 由 industry-ds skill 生成時",
    )
    html = html.replace("id-meta JSON", "ds-meta JSON")
    return html


def t_injection_zone(html: str) -> str:
    """Update INJECTION ZONE comment + footer maintenance note."""
    html = html.replace(
        "INJECTION ZONE: industry-analyst skill",
        "INJECTION ZONE: industry-ds skill",
    )
    html = html.replace(
        "由 industry-analyst skill 維護",
        "由 industry-ds skill 維護",
    )
    return html


def t_internal_links(html: str) -> str:
    """Repoint internal cross-links: /id/ID_*.html links inside cat-body helper text → /ds/DS_*.html."""
    # We only changed the active nav link's href above. Per-card inserted links
    # come from individual DS reports later. But the helper text inside empty
    # cat-bodies may still reference /id/. Replace anchor text only.
    html = html.replace("docs/id/ID_", "docs/ds/DS_")
    return html


def t_new_tab_handler(html: str) -> str:
    """Extend the 'Open in new tab' JS handler to cover both /ds/DS_ and /id/ID_ links."""
    html = re.sub(
        r"// Open ID report links in new tab[^\n]*\n"
        r"document\.querySelectorAll\('a\[href\*=\"/id/ID_\"\]'\)",
        "// Open DS / ID report links in new tab\n"
        "document.querySelectorAll('a[href*=\"/ds/DS_\"], a[href*=\"/id/ID_\"], a[href^=\"DS_\"], a[href^=\"ID_\"]')",
        html,
        count=1,
    )
    return html


def _strip_balanced_div(html: str, open_pattern: str) -> str:
    """Find a div matching open_pattern and remove the balanced <div>...</div>."""
    m = re.search(open_pattern, html)
    if not m:
        return html
    depth = 1
    scan = m.end()
    div_open = re.compile(r"<div\b", re.IGNORECASE)
    div_close = re.compile(r"</div>", re.IGNORECASE)
    while depth > 0 and scan < len(html):
        next_open = div_open.search(html, scan)
        next_close = div_close.search(html, scan)
        if not next_close:
            return html  # unbalanced; safer to leave alone
        if next_open and next_open.start() < next_close.start():
            depth += 1
            scan = next_open.end()
        else:
            depth -= 1
            scan = next_close.end()
    return html[:m.start()] + html[scan:]


# ─── Pipeline ─────────────────────────────────────────────────────────────────

PIPELINE = [
    ("title + meta description", t_title_and_meta),
    ("nav chrome (add /ds/ active link)", t_nav_chrome),
    ("breadcrumb + h1 + sub", t_breadcrumb_and_head),
    ("meta-strip numeric chips", t_meta_strip),
    ("phase-pop content", t_phase_pop),
    ("strip flagship hero", t_strip_flagship),
    ("strip flagship JS init", t_strip_flagship_js),
    ("strip tier matrix passthrough", t_strip_tier_matrix),
    ("strip article cards", t_strip_articles),
    ("reset count badges to 0", t_count_badges),
    ("bottom help box (ID → DS)", t_help_box),
    ("footer line", t_footer),
    ("subgroup helper comments (ID → DS)", t_subgroup_comments),
    ("injection zone marker", t_injection_zone),
    ("internal /id/ID_ link text", t_internal_links),
    ("new-tab JS handler (extend to DS_)", t_new_tab_handler),
]


def transform(html: str, verbose: bool = False) -> str:
    for label, fn in PIPELINE:
        before = len(html)
        html = fn(html)
        if verbose:
            print(f"  · {label}: {before:,} → {len(html):,} bytes", file=sys.stderr)
    return html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if not SRC.exists():
        print(f"ERROR: source not found: {SRC}", file=sys.stderr)
        sys.exit(1)

    # Refuse to overwrite if existing /ds/index.html has DS cards (unless --force)
    if OUT.exists() and not args.force and not args.dry_run:
        existing = OUT.read_text(encoding="utf-8")
        if 'href="/ds/DS_' in existing or 'href="DS_' in existing:
            print(f"REFUSING to overwrite {OUT} — it contains DS cards.", file=sys.stderr)
            print("Pass --force to overwrite anyway (cards will be lost).", file=sys.stderr)
            sys.exit(2)

    html_in = SRC.read_text(encoding="utf-8")
    html_out = transform(html_in, verbose=args.verbose)

    if args.dry_run:
        print(f"Would write {len(html_out):,} bytes to {OUT}")
        print(f"  (source {len(html_in):,} bytes → output {len(html_out):,} bytes)")
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_out, encoding="utf-8")
    print(f"✅ Wrote {OUT} ({len(html_out):,} bytes)")


if __name__ == "__main__":
    main()
