#!/usr/bin/env python3
"""Build per-category drilldown pages from docs/ds/index.html.

Mirror of build_id_category_pages.py for the industry-ds skill output.

Usage:
  python3 scripts/build_ds_category_pages.py

Reads docs/ds/index.html (single-page source of truth) and writes
docs/ds/cat-{mega}.html for each of the 15 mega-categories.

Each cat-{mega}.html contains:
  - Full <head> with adapted <title>
  - Site nav header
  - Breadcrumb nav + category h1 + hint
  - Sticky cat-jump bar (hrefs changed to cat-{mega}.html, active class on current)
  - The full .category block (forced open)
  - Filter bar + Filter JS (copied verbatim)
  - Auto-generated footer with ISO timestamp

All category HTML stays in index.html (hidden injection zone) so the
industry-ds skill can still insert new cards via subgroup-anchor markers.
After insertion, re-run this script to sync cat-*.html files.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "ds" / "index.html"
OUT_DIR = ROOT / "docs" / "ds"

# ── Taxonomy: shared with ID (docs/id/taxonomy.md is single source of truth) ──
TAXONOMY = [
    {"mega": "semi",       "data_cat": "semi",       "chinese": "半導體 / AI 基建",        "icon": "🔷", "hint": "AI Accelerator / 封裝 / 記憶體 / 製程 / 互連"},
    {"mega": "bio",        "data_cat": "bio",        "chinese": "生技 / 醫療",            "icon": "🧬", "hint": "GLP-1 / 基因治療 / 醫材 / 數位健康"},
    {"mega": "cloud",      "data_cat": "cloud",      "chinese": "雲端 / SaaS / 軟體",      "icon": "☁️", "hint": "資安 / Agentic AI / Token / 媒體 SaaS"},
    {"mega": "energy",     "data_cat": "energy",     "chinese": "能源 / 電動車 / 新能源",  "icon": "⚡", "hint": "核能 / EV / 太陽風能 / 油氣"},
    {"mega": "consumer",   "data_cat": "consumer",   "chinese": "消費 / 零售 / 精品",      "icon": "🛍️", "hint": "服飾 / 餐飲 / 奢侈品 / E-commerce"},
    {"mega": "finance",    "data_cat": "finance",    "chinese": "金融 / 保險 / FinTech",   "icon": "🏦", "hint": "支付 / 銀行 / Stablecoin / 財富"},
    {"mega": "industrial", "data_cat": "industrial", "chinese": "工業 / 航太 / 自動化",    "icon": "🔧", "hint": "國防 / 機器人 / 重機 / 自駕"},
    {"mega": "staples",    "data_cat": "staples",    "chinese": "必選消費 / 飲料 / 個護",  "icon": "🛒", "hint": "飲料 / 包裝食品 / 個護"},
    {"mega": "reits",      "data_cat": "reits",      "chinese": "REITs / 數位基建房東",   "icon": "🏢", "hint": "數位基建 / 倉儲 / 老人公寓"},
    {"mega": "space",      "data_cat": "space",      "chinese": "太空經濟 / 衛星 / 低軌道", "icon": "🛰️", "hint": "衛星 / Launch / 太空材料"},
    {"mega": "housing",    "data_cat": "housing",    "chinese": "住房 / 房貸 / Builders",  "icon": "🏠", "hint": "美國 builders / 海外房產 / 房貸"},
    {"mega": "transport",  "data_cat": "transport",  "chinese": "運輸 / 物流 / 航運 / 旅遊", "icon": "✈️", "hint": "航空 / 海運 / 鐵路 / 旅遊 / 賭博"},
    {"mega": "materials",  "data_cat": "materials",  "chinese": "材料 / 礦業 / 特殊化學",  "icon": "⛏️", "hint": "銅 / 鋰 / 鋼鐵 / 化工 / 稀土"},
    {"mega": "agri",       "data_cat": "agri",       "chinese": "農業 / 食品 / 大宗商品",  "icon": "🌾", "hint": "牛肉 / 穀物 / 漁業 / 肥料"},
    {"mega": "macro",      "data_cat": "macro",      "chinese": "跨域 / 地緣 / 其他",     "icon": "🌐", "hint": "地緣政治 / 跨域影響"},
]

TAXONOMY_BY_MEGA = {t["mega"]: t for t in TAXONOMY}


# ─── Parsing helpers (identical structure to build_id_category_pages.py) ────


def extract_head(html: str) -> str:
    m = re.search(r"<head>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    if not m:
        raise ValueError("No <head> block found in source HTML")
    return m.group(1)


def extract_nav_block(html: str) -> str:
    m = re.search(
        r'(<style>\s*\.imq-nav-root.*?</style>.*?<header class="imq-nav-root">.*?</header>\s*<script>.*?</script>)',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        raise ValueError("No imq-nav-root nav block found")
    return m.group(1)


def extract_cat_jump_links(html: str) -> list[dict]:
    m = re.search(r'<div class="cat-jump">(.*?)</div>', html, re.DOTALL)
    if not m:
        raise ValueError("No .cat-jump block found")
    inner = m.group(1)
    links = []
    for am in re.finditer(r'<a\s([^>]*)>(.*?)</a>', inner, re.DOTALL):
        attrs = am.group(1)
        text = am.group(2)
        href_m = re.search(r'href="([^"]*)"', attrs)
        href = href_m.group(1) if href_m else ""
        links.append({"href_original": href, "text": text.strip()})
    return links


def extract_filter_bar(html: str) -> str:
    m = re.search(
        r'<div class="toolbar-inner">(.*?)</div>\s*<div class="cat-jump">',
        html,
        re.DOTALL,
    )
    if not m:
        return ""
    return m.group(1).strip()


def extract_filter_js(html: str) -> str:
    m = re.search(
        r"(// Filters &amp; search\s*\nvar filterState.*?applyFilters\(\);)",
        html,
        re.DOTALL,
    )
    if not m:
        m = re.search(
            r"(// Filters & search\s*\nvar filterState.*?applyFilters\(\);)",
            html,
            re.DOTALL,
        )
    if not m:
        raise ValueError("No filter JS block found")
    return m.group(1)


def extract_category_block(html: str, mega: str) -> tuple[str, int]:
    """Extract the full <div class="category..." id="cat-{mega}"> block for a given mega."""
    if mega == "staples":
        pattern = r'(<div class="category[^"]*"[^>]*data-cat="consumer"[^>]*>)'
        matches = list(re.finditer(pattern, html))
        block_start = None
        for m in matches:
            after = html[m.start():m.start() + 300]
            if "必選消費" in after:
                block_start = m.start()
                break
        if block_start is None:
            m2 = re.search(
                r'<div class="category[^>]*>(?=\s*<div class="cat-head">.*?🛒)',
                html,
                re.DOTALL,
            )
            if m2:
                block_start = m2.start()
            else:
                print(
                    "  WARNING: staples category block not found; generating empty page",
                    file=sys.stderr,
                )
                return "", 0
    else:
        pattern = rf'<div class="category[^"]*"\s+id="cat-{re.escape(mega)}"[^>]*>'
        m = re.search(pattern, html)
        if not m:
            m = re.search(rf'<div[^>]*\bid="cat-{re.escape(mega)}"[^>]*>', html)
        if not m:
            print(f"  WARNING: category block for mega={mega!r} not found", file=sys.stderr)
            return "", 0
        block_start = m.start()

    block = _extract_balanced_div(html, block_start)
    if block is None:
        print(
            f"  WARNING: could not extract balanced div for mega={mega!r}",
            file=sys.stderr,
        )
        return "", 0

    article_count = len(re.findall(r'<article class="topic-card', block))
    return block, article_count


def _extract_balanced_div(html: str, start: int) -> str | None:
    if not html[start:].startswith("<div"):
        return None
    depth = 0
    pos = start
    length = len(html)
    while pos < length:
        open_m = re.search(r"<div\b", html[pos:])
        close_m = re.search(r"</div>", html[pos:])
        if open_m is None and close_m is None:
            break
        open_pos = pos + open_m.start() if open_m else length
        close_pos = pos + close_m.start() if close_m else length
        if open_pos <= close_pos:
            depth += 1
            pos = open_pos + 1
        else:
            depth -= 1
            end_pos = close_pos + len("</div>")
            if depth == 0:
                return html[start:end_pos]
            pos = close_pos + 1
    return None


def build_cat_jump_bar(links: list[dict], active_mega: str) -> str:
    """Build cat-jump bar with hrefs (relative cat-X.html) and active class on current.

    DS-specific: «↩ 全部» link points to /ds/ (not /id/).
    """
    items = []
    items.append('<a href="/ds/">↩ 全部</a>')
    for link in links:
        href = link["href_original"]
        text = link["text"]
        anchor_m = re.match(r"#cat-(.+)", href)
        if anchor_m:
            cat_slug = anchor_m.group(1)
            new_href = f"cat-{cat_slug}.html"
            is_active = (cat_slug == active_mega)
            if cat_slug == "consumer" and "必選消費" in text:
                new_href = "cat-staples.html"
                is_active = (active_mega == "staples")
            elif cat_slug == "consumer" and "必選消費" not in text:
                new_href = "cat-consumer.html"
                is_active = (active_mega == "consumer")
            active_attr = ' class="active"' if is_active else ""
            items.append(f'<a href="{new_href}"{active_attr}>{text}</a>')
        else:
            # Hrefs already in cat-X.html form (DS index already has them) — just preserve
            is_active = False
            m_cat = re.match(r"cat-([\w-]+)\.html", href or "")
            if m_cat:
                cat_slug = m_cat.group(1)
                is_active = (cat_slug == active_mega)
            active_attr = ' class="active"' if is_active else ""
            items.append(f'<a href="{href}"{active_attr}>{text}</a>')
    return "\n".join(f"      {item}" for item in items)


def force_open_category(block: str, mega: str) -> str:
    """Ensure the category div has class 'category open' and fix data-cat for staples."""
    if mega == "staples":
        block = re.sub(
            r'<div class="category[^"]*" id="cat-staples" data-cat="consumer">',
            '<div class="category open" id="cat-staples" data-cat="staples">',
            block,
            count=1,
        )
    if 'class="category open"' not in block[:80] and 'class="category"' in block[:80]:
        block = block.replace('class="category"', 'class="category open"', 1)
    elif 'class="category open"' not in block[:80]:
        block = re.sub(r'class="category[^"]*"', 'class="category open"', block, count=1)
    return block


def generate_cat_page(
    mega: str,
    head_content: str,
    nav_block: str,
    cat_jump_links: list[dict],
    filter_bar_inner: str,
    filter_js: str,
    category_block: str,
    article_count: int,
    timestamp: str,
) -> str:
    """Generate the full HTML for a cat-{mega}.html page."""
    meta = TAXONOMY_BY_MEGA.get(mega)
    if not meta:
        raise ValueError(f"Unknown mega: {mega!r}")

    chinese = meta["chinese"]
    icon = meta["icon"]
    hint = meta["hint"]

    adapted_head = re.sub(
        r"<title>.*?</title>",
        f"<title>{chinese} — 產業敘述 DS 索引</title>",
        head_content,
        flags=re.DOTALL,
    )
    cat_css = """
/* Cat page extras */
.cat-breadcrumb{padding:12px 0 8px;font-size:.8rem;color:#6B7280}
.cat-breadcrumb a{color:#6B7280;text-decoration:none}
.cat-breadcrumb a:hover{color:#4C1D95;text-decoration:underline}
.cat-breadcrumb strong{color:#4C1D95}
.cat-page-h1{color:#4C1D95;font-size:1.6rem;font-weight:800;letter-spacing:-.03em;margin:0 0 4px}
.cat-page-hint{color:#6B7280;font-size:.88rem;margin:0 0 12px}
.cat-jump a.active{background:#7C3AED;color:#fff;border-color:#7C3AED}
.cat-page-footer{margin-top:2rem;padding-top:1rem;border-top:1px solid #E5E7EB;color:#9CA3AF;font-size:.72rem;text-align:center}
.cat-head{cursor:default !important}
.cat-head:hover{background:linear-gradient(90deg,#F5F3FF,#fff) !important}
"""
    adapted_head = adapted_head.replace("</style>", cat_css + "\n</style>", 1)

    cat_jump_bar = build_cat_jump_bar(cat_jump_links, mega)
    open_block = force_open_category(category_block, mega)

    empty_note = ""
    if article_count == 0:
        empty_note = f"""
  <div style="text-align:center;padding:40px 20px;color:#94A3B8;font-size:14px;">
    <div style="font-size:32px;margin-bottom:8px">📭</div>
    <p>此大類尚無 DS 報告</p>
    <p style="font-size:12px;margin-top:4px">對 Claude Code 說「{chinese} ds」即可新增</p>
  </div>"""

    safe_filter_js = filter_js

    page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>{adapted_head}
</head>
<body>

{nav_block}

<div class="container">
  <nav class="cat-breadcrumb">
    <a href="/">首頁</a> &rsaquo;
    <a href="/research/">研究</a> &rsaquo;
    <a href="/ds/">所有產業 DS 報告</a>
    &rsaquo; <strong>{icon} {chinese}</strong>
  </nav>

  <h1 class="cat-page-h1">{icon} {chinese}（{article_count} 份）</h1>
  <p class="cat-page-hint">{hint}</p>

  <div class="toolbar">
    <div class="toolbar-inner">
      {filter_bar_inner}
    </div>
    <div class="cat-jump">
{cat_jump_bar}
    </div>
  </div>
  <div class="filter-status" id="filter-status">顯示全部 <b id="visible-count">—</b> 份報告</div>

{open_block}
{empty_note}

</div>

<div class="cat-page-footer">
  本頁由 scripts/build_ds_category_pages.py 從 docs/ds/index.html 自動生成 · 最後生成：{timestamp}
</div>

<script>
// Topic card expand (event delegation)
document.addEventListener('click', function(e){{
  var btn = e.target.closest('.tc-expand');
  if(!btn) return;
  e.preventDefault();
  btn.closest('.topic-card').classList.toggle('expanded');
}});

// Open DS / ID report links in new tab
document.querySelectorAll('a[href*="/ds/DS_"], a[href*="/id/ID_"], a[href^="DS_"], a[href^="ID_"]').forEach(function(a){{
  a.target = '_blank';
  a.rel = 'noopener';
}});

{safe_filter_js}
</script>

</body>
</html>"""
    return page


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    if not SRC.exists():
        print(f"ERROR: source not found: {SRC}", file=sys.stderr)
        sys.exit(1)

    html = SRC.read_text(encoding="utf-8")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"Parsing {SRC} ({len(html):,} bytes)...", file=sys.stderr)

    try:
        head_content = extract_head(html)
        nav_block = extract_nav_block(html)
        cat_jump_links = extract_cat_jump_links(html)
        filter_bar_inner = extract_filter_bar(html)
        filter_js = extract_filter_js(html)
    except ValueError as e:
        print(f"PARSE ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"  cat-jump links found: {len(cat_jump_links)}", file=sys.stderr)

    generated = []
    counts: dict = {}

    for meta in TAXONOMY:
        mega = meta["mega"]
        try:
            block, article_count = extract_category_block(html, mega)
        except Exception as e:
            print(f"  ERROR extracting {mega}: {e}", file=sys.stderr)
            block = ""
            article_count = 0

        if not block:
            block = f"""<div class="category open" id="cat-{mega}" data-cat="{mega}">
  <div class="cat-head">
    <div class="left">
      <span class="cat-icon">{meta['icon']}</span>
      <h2>{meta['chinese']}</h2>
      <span class="count">0 份</span>
    </div>
    <span class="hint">{meta['hint']}</span>
    <span class="cat-chev">▾</span>
  </div>
  <div class="cat-body">
    <div class="topic-grid">
    </div>
  </div>
</div>"""

        page_html = generate_cat_page(
            mega=mega,
            head_content=head_content,
            nav_block=nav_block,
            cat_jump_links=cat_jump_links,
            filter_bar_inner=filter_bar_inner,
            filter_js=filter_js,
            category_block=block,
            article_count=article_count,
            timestamp=timestamp,
        )

        out_path = OUT_DIR / f"cat-{mega}.html"
        out_path.write_text(page_html, encoding="utf-8")
        generated.append(f"cat-{mega}.html")
        counts[mega] = article_count
        print(
            f"  {mega:12s} → {article_count:3d} articles → {out_path.name}",
            file=sys.stderr,
        )

    print(f"\nGenerated {len(generated)} cat-*.html files:", file=sys.stderr)
    for name in generated:
        print(f"  {name}", file=sys.stderr)
    print("\nArticle counts by mega:", file=sys.stderr)
    for mega, n in counts.items():
        print(f"  {mega:12s}: {n}", file=sys.stderr)

    print(f"\nDone. Timestamp: {timestamp}", file=sys.stderr)


if __name__ == "__main__":
    main()
