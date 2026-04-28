#!/usr/bin/env python3
"""One-off migration: rebuild docs/id/index.html with new layout (compressed hero + sticky toolbar + 2-col grid + collapsible cards)
preserving every category, topic card, child, suggest block, and inline content."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "id" / "index.html"
DST = ROOT / "docs" / "id" / "index.new.html"  # safety: avoid clobber. After structural rerun, mv .new.html -> index.html. CSS-only tweaks edit index.html directly.
PROTO = ROOT / "docs" / "id" / "_layout-preview.html"


# ---------- helpers ----------

def inner_html(tag: Tag) -> str:
    return tag.decode_contents().strip() if tag else ""


def text_of(tag: Tag) -> str:
    return tag.get_text(" ", strip=True) if tag else ""


def slugify_cat(title: str) -> str:
    """產生 category id, e.g. '半導體 / AI 基建' -> 'semi'."""
    mapping = {
        "半導體": "semi",
        "生技": "bio",
        "雲端": "cloud",
        "能源": "energy",
        "消費": "consumer",
        "金融": "finance",
        "工業": "industrial",
        "必選消費": "staples",
        "REITs": "reits",
        "太空": "space",
        "住房": "housing",
        "運輸": "transport",
        "材料": "materials",
        "農業": "agri",
        "跨域": "macro",
    }
    for k, v in mapping.items():
        if k in title:
            return v
    return re.sub(r"[^a-z0-9]+", "-", title.lower())[:20]


# ---------- parse topic card ----------

def parse_topic_card(card: Tag, is_child: bool = False) -> dict:
    """從 .topic-card 抽出結構化資料。"""
    # number
    num = text_of(card.select_one(":scope > .topic-head > .topic-num"))

    # title
    title_a = card.select_one(":scope > .topic-head > .topic-title")
    href = title_a.get("href") if title_a else ""
    # title text: strip badge / arrow children, keep main text
    title_clone = BeautifulSoup(str(title_a), "html.parser").find("a") if title_a else None
    if title_clone:
        for sub in title_clone.select(".root-badge, .child-tag, .arrow"):
            sub.decompose()
        title_text = title_clone.get_text(" ", strip=True)
    else:
        title_text = ""

    # parent / standalone / child
    parent_badge_tag = title_a.select_one(".root-badge") if title_a else None
    child_badge_tag = title_a.select_one(".child-tag") if title_a else None
    parent_badge = text_of(parent_badge_tag) if parent_badge_tag else ""
    child_badge = text_of(child_badge_tag) if child_badge_tag else ""

    is_parent = "is-parent" in (card.get("class") or [])

    # tags
    tags = inner_html(card.select_one(":scope > .topic-tags"))

    # meta: keep all chips/pills as-is in order, plus extract phase separately
    meta_box = card.select_one(":scope > .topic-meta")
    phase_pill = meta_box.select_one(".phase-pill") if meta_box else None
    phase_class = ""
    phase_text = ""
    if phase_pill:
        for c in phase_pill.get("class") or []:
            if c.startswith("phase-") and c != "phase-pill":
                phase_class = c
                break
        phase_text = text_of(phase_pill)

    # full meta children (for "expanded details" section): every span/button except phase pill (we render that separately)
    meta_children_html = []
    if meta_box:
        for child in meta_box.children:
            if not isinstance(child, Tag):
                continue
            classes = child.get("class") or []
            if "phase-pill" in classes:
                continue
            if "toggle-children" in classes:
                continue  # we replace this with a generic ▾ button
            meta_children_html.append(str(child))

    # thesis (HTML preserved)
    thesis_tag = card.select_one(":scope > .topic-thesis")
    thesis_html = inner_html(thesis_tag)

    # child chips (parent only)
    child_chips_box = card.select_one(":scope > .child-chips")
    child_chips_html = ""
    if child_chips_box:
        # keep just <a class="chip"> elements
        chips = []
        for a in child_chips_box.select("a.chip"):
            chips.append(str(a))
        child_chips_html = "\n".join(chips)

    # children (parent only, recursively)
    children = []
    children_box = card.select_one(":scope > .children")
    if children_box:
        for child_card in children_box.select(":scope > .topic-card"):
            children.append(parse_topic_card(child_card, is_child=True))

    return {
        "num": num,
        "title": title_text,
        "href": href,
        "is_parent": is_parent,
        "is_child": is_child,
        "parent_badge": parent_badge,
        "child_badge": child_badge,
        "tags": tags,
        "meta_extras_html": "\n".join(meta_children_html),
        "phase_class": phase_class,
        "phase_text": phase_text,
        "thesis_html": thesis_html,
        "child_chips_html": child_chips_html,
        "children": children,
    }


# ---------- parse category ----------

def parse_category(cat: Tag) -> dict:
    head = cat.select_one(":scope > .cat-head")
    icon = text_of(head.select_one(".cat-icon"))
    title = text_of(head.select_one("h2"))
    count = text_of(head.select_one(".count"))
    hint = text_of(head.select_one(".hint"))

    body = cat.select_one(":scope > .cat-body")
    topic_list = body.select_one(":scope > .topic-list") if body else None

    topics = []
    if topic_list:
        for card in topic_list.select(":scope > .topic-card"):
            topics.append(parse_topic_card(card))

    empty_state_tag = body.select_one(":scope > .empty-state") if body else None
    empty_state_html = inner_html(empty_state_tag) if empty_state_tag else ""

    suggest_tag = body.select_one(":scope > .suggest") if body else None
    suggest_html = inner_html(suggest_tag) if suggest_tag else ""

    return {
        "id": slugify_cat(title),
        "icon": icon,
        "title": title,
        "count": count,
        "hint": hint,
        "topics": topics,
        "empty_state_html": empty_state_html,
        "suggest_html": suggest_html,
    }


# ---------- render ----------

def render_topic_card(t: dict) -> str:
    """Render single topic card in new compact layout."""
    is_parent = t["is_parent"] and not t["is_child"]
    is_child = t["is_child"]
    classes = ["topic-card"]
    if is_parent:
        classes.append("is-parent")
    badge = ""
    if is_parent and t["parent_badge"]:
        badge = f'<span class="tc-badge">{t["parent_badge"]}</span>'
    elif is_child and t["child_badge"]:
        badge = f'<span class="tc-badge child">{t["child_badge"]}</span>'

    phase_html = ""
    if t["phase_class"]:
        phase_html = f'<span class="tc-phase {t["phase_class"]}">{t["phase_text"]}</span>'

    # data-search: tags + title (lowercase, for quick text match)
    search_blob = f'{t["title"]} {t["tags"]}'.lower()
    search_blob = re.sub(r"<[^>]+>", " ", search_blob)
    search_blob = re.sub(r'"', "", search_blob)

    # short thesis: strip tags, take first ~100 chars
    short_thesis = re.sub(r"<[^>]+>", "", t["thesis_html"])
    short_thesis = re.sub(r"\s+", " ", short_thesis).strip()

    # children chips (parent only) shown always
    children_block = ""
    if is_parent and t["child_chips_html"]:
        # rewrite chip class from .chip to .tc-chip
        chips_rewritten = t["child_chips_html"].replace('class="chip"', 'class="tc-chip"')
        children_block = f'''<div class="tc-children">
  <span class="label">↳ 子題：</span>
  {chips_rewritten}
</div>'''

    # type for filter
    dtype = "parent" if is_parent else ("child" if is_child else "standalone")

    # phase data attr (without phase- prefix)
    phase_attr = t["phase_class"].replace("phase-", "") if t["phase_class"] else ""

    # meta extras HTML (without phase pill) - rewrite .chip → keep, remove .phase-pill
    meta_extras = t["meta_extras_html"]

    return f'''<article class="{ ' '.join(classes) }" data-phase="{phase_attr}" data-type="{dtype}" data-search="{search_blob}">
  <div class="tc-head">
    <span class="tc-num">{t["num"]}</span>
    <a class="tc-title" href="{t["href"]}">{t["title"]} <span class="arrow">→</span></a>
    {badge}
    {phase_html}
    <button class="tc-expand" aria-label="展開">▾</button>
  </div>
  <div class="tc-thesis-short">{short_thesis}</div>
  {children_block}
  <div class="tc-details">
    <div class="tc-tags">{t["tags"]}</div>
    <div class="tc-meta">{meta_extras}</div>
    <div class="tc-thesis-full">{t["thesis_html"]}</div>
  </div>
</article>'''


def flatten_topics(topics: list) -> list:
    """Flatten parent + children into a single list (parent first, then its children, then next parent...)."""
    out = []
    for t in topics:
        out.append(t)
        for c in t["children"]:
            c["is_child"] = True
            out.append(c)
    return out


def render_category(c: dict) -> str:
    flat = flatten_topics(c["topics"])
    has_topics = len(flat) > 0

    cards_html = "\n".join(render_topic_card(t) for t in flat) if has_topics else ""

    body_inner = ""
    if has_topics:
        body_inner += f'<div class="topic-grid">\n{cards_html}\n</div>\n'
    elif c["empty_state_html"]:
        body_inner += f'<div class="empty-state">{c["empty_state_html"]}</div>\n'
    if c["suggest_html"]:
        body_inner += f'''<details class="suggest"><summary>📋 建議補建</summary>
<div class="suggest-body">{c["suggest_html"]}</div>
</details>\n'''

    cat_classes = "category"
    if has_topics:
        cat_classes += " open"

    return f'''<div class="{cat_classes}" id="cat-{c["id"]}" data-cat="{c["id"]}">
  <div class="cat-head">
    <div class="left">
      <span class="cat-icon">{c["icon"]}</span>
      <h2>{c["title"]}</h2>
      <span class="count">{c["count"]}</span>
    </div>
    <span class="hint">{c["hint"]}</span>
    <span class="cat-chev">▾</span>
  </div>
  <div class="cat-body">
    {body_inner}
  </div>
</div>'''


# ---------- main ----------

def main():
    src_html = SRC.read_text(encoding="utf-8")
    soup = BeautifulSoup(src_html, "html.parser")

    # Extract preserved blocks (Flagship 1 & 2, Tier Matrix alert, stats values, phase legend already known)
    container = soup.select_one("div.container")
    if not container:
        sys.exit("ERROR: no .container in index.html")

    # Flagship 1 (purple) — first big gradient div with theses.html link
    flagships_purple = None
    flagships_blue = None
    for div in container.find_all("div", recursive=False):
        style = div.get("style", "") or ""
        if "background:linear-gradient(135deg,#4C1D95" in style:
            flagships_purple = div
        elif "background:linear-gradient(135deg,#1E3A8A" in style:
            flagships_blue = div

    # Tier Matrix alert — find by HTML comment markers
    tier_alert_match = re.search(
        r"<!-- TIER_MATRIX_ALERT_START -->(.+?)<!-- TIER_MATRIX_ALERT_END -->",
        src_html, re.S
    )
    tier_alert_html = tier_alert_match.group(1).strip() if tier_alert_match else ""

    # Stats values
    stats_values = {}
    for c in container.select(".stats-card"):
        label = text_of(c.select_one(".label"))
        value = text_of(c.select_one(".value"))
        desc = text_of(c.select_one(".desc"))
        stats_values[label] = (value, desc)

    # Categories
    categories = []
    for cat in container.select(":scope > .category"):
        categories.append(parse_category(cat))

    # Trigger explainer (last big block before footer)
    trigger_match = re.search(
        r'<!-- ========== 觸發說明 ========== -->\s*<div [^>]*?>(.+?)</div>\s*</div>\s*<div class="footer">',
        src_html, re.S
    )
    trigger_html = trigger_match.group(1).strip() if trigger_match else ""

    # ---------- build categories nav (cat-jump) ----------
    cat_jump_links = []
    for c in categories:
        # extract leading icon from category title isn't needed; we have c.icon
        cat_jump_links.append(
            f'<a href="#cat-{c["id"]}">{c["icon"]} {c["title"]} <span class="n">{c["count"]}</span></a>'
        )
    cat_jump_html = "\n".join(cat_jump_links)

    # ---------- compress flagships into tabbed block ----------
    # Extract teaser cards from each flagship banner: each has h2 + grid of <a> anchors
    def extract_flagship(fl_div: Tag) -> dict:
        if fl_div is None:
            return None
        h2 = fl_div.select_one("h2")
        # full-flagship link: outer <a> with ".html"
        more_a = None
        for a in fl_div.select("a"):
            href = a.get("href", "")
            if href.endswith(".html") and "theses" in href and "#" not in href:
                more_a = a
                break
        more_href = more_a.get("href") if more_a else "#"
        cards = []
        for a in fl_div.select("a"):
            if a is more_a:
                continue
            href = a.get("href", "")
            if "#t" not in href:
                continue
            # 提取子節點 div 結構
            divs = a.find_all("div", recursive=False)
            num_text = text_of(divs[0]) if len(divs) >= 1 else ""
            title_text = text_of(divs[1]) if len(divs) >= 2 else text_of(a)
            cards.append({"href": href, "num": num_text, "title": title_text})
        return {
            "title": text_of(h2),
            "more_href": more_href,
            "cards": cards,
        }

    fl_ai = extract_flagship(flagships_purple)
    fl_sw = extract_flagship(flagships_blue)

    def render_fl_pane(pane_id: str, data: dict) -> str:
        if not data:
            return ""
        cards = ""
        for i, c in enumerate(data["cards"]):
            extra = " extra" if i >= 4 else ""
            cards += f'''<a class="{extra.strip()}" href="{c["href"]}"><div class="num">{c["num"]}</div><div class="title">{c["title"]}</div></a>\n'''
        active_cls = "active" if pane_id == "ai" else ""
        return f'''<div class="fl-pane {active_cls}" data-pane="{pane_id}">
  <div class="fl-grid" data-collapsed="true">
    {cards}
  </div>
  <div class="fl-foot">
    <button class="toggle" data-toggle="{pane_id}">查看全部 {len(data["cards"])} 個 ▾</button>
    <a class="more" href="{data["more_href"]}">完整 flagship →</a>
  </div>
</div>'''

    fl_ai_pane = render_fl_pane("ai", fl_ai)
    fl_sw_pane = render_fl_pane("sw", fl_sw)
    fl_ai_title = fl_ai["title"] if fl_ai else "Flagship Theses"
    fl_sw_title = fl_sw["title"] if fl_sw else ""

    # ---------- categories rendered ----------
    cats_html = "\n".join(render_category(c) for c in categories)

    # ---------- build full HTML ----------
    out = build_full_html(
        stats=stats_values,
        tier_alert_html=tier_alert_html,
        fl_ai_title=fl_ai_title,
        fl_sw_title=fl_sw_title,
        fl_ai_pane=fl_ai_pane,
        fl_sw_pane=fl_sw_pane,
        cat_jump_html=cat_jump_html,
        cats_html=cats_html,
        trigger_html=trigger_html,
        # keep original navigation by re-using src
        nav_html=extract_nav(src_html),
        head_extras=extract_head_extras(src_html),
    )
    DST.write_text(out, encoding="utf-8")
    print(f"✓ wrote {DST} ({len(out):,} bytes)")
    print(f"  categories: {len(categories)}")
    print(f"  total topics (incl. children): {sum(len(flatten_topics(c['topics'])) for c in categories)}")


def extract_nav(src_html: str) -> str:
    """Extract the imq-nav-root header block + its preceding style + the dropdown-toggle script."""
    m = re.search(
        r"(<style>\s*\.imq-nav-root.+?</style>)\s*(<header class=\"imq-nav-root\">.+?</header>)\s*(<script>.+?</script>)",
        src_html, re.S
    )
    if not m:
        return ""
    return m.group(1) + "\n" + m.group(2) + "\n" + m.group(3)


def extract_head_extras(src_html: str) -> str:
    """preserve any <script> in original index that maintains freshness (the dynamic version-status updater near bottom)"""
    # the last <script> block (freshness update)
    scripts = re.findall(r"<script>(?!\s*\(function\(\)\{document\.querySelectorAll\('\.imq-dd-btn'\)).+?</script>", src_html, re.S | re.I)
    # actually simpler: find any script that updates flagship-version / flagship-status
    m = re.search(
        r"<script>\s*\(function\(\)\{[^<]*?LAST_REFRESH[^<]*?\}\)\(\);?\s*</script>",
        src_html, re.S
    )
    return m.group(0) if m else ""


def build_full_html(*, stats, tier_alert_html, fl_ai_title, fl_sw_title, fl_ai_pane, fl_sw_pane,
                    cat_jump_html, cats_html, trigger_html, nav_html, head_extras) -> str:
    # stats lookup with safe fallback
    def s(label, default):
        v = stats.get(label)
        return v[0] if v else default

    def sd(label, default):
        v = stats.get(label)
        return v[1] if v else default

    return f"""<!DOCTYPE html>
<html lang=\"zh-Hant\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>產業深度報告 — InvestMQuest Research</title>
<meta name=\"description\" content=\"跨多檔個股共用的產業深度研究（Industry DD），按產業類別整理\">
<style>
*{{box-sizing:border-box}}
body{{font-family:-apple-system,'Noto Sans TC',sans-serif;background:#FAFAF9;color:#1E1B4B;margin:0;padding:0;font-size:14px;line-height:1.65;-webkit-text-size-adjust:100%}}
.container{{max-width:1240px;margin:0 auto;padding:1.4rem 1.5rem 3rem}}
.crumb{{font-size:.78rem;color:#6B7280;margin-bottom:.5rem}}
.crumb a{{color:#6B7280;text-decoration:none}}

/* H1 + meta strip */
.head-row{{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;flex-wrap:wrap;border-bottom:1px solid #E5E7EB;padding-bottom:14px;margin-bottom:14px}}
h1{{color:#4C1D95;font-size:1.7rem;font-weight:800;letter-spacing:-.03em;margin:0}}
.sub{{color:#6B7280;font-size:.88rem;margin-top:.35rem;max-width:680px;line-height:1.55}}
.sub code{{background:#EDE9FE;padding:1px 6px;border-radius:3px;font-size:11.5px;color:#6B21A8}}

.meta-strip{{display:flex;align-items:center;gap:10px 14px;flex-wrap:wrap;font-size:11.5px;color:#4B5563}}
.meta-strip .item{{display:inline-flex;align-items:center;gap:5px;background:#fff;border:1px solid #E5E7EB;padding:5px 10px;border-radius:14px}}
.meta-strip .item b{{color:#4C1D95;font-weight:700;font-family:'IBM Plex Mono',ui-monospace,monospace}}
.meta-strip .info-toggle{{cursor:pointer;color:#7C3AED;background:none;border:0;font:inherit;font-size:11.5px;padding:0;text-decoration:underline;text-decoration-style:dotted;text-underline-offset:3px}}
.phase-pop{{display:none;background:#fff;border:1px solid #DDD6FE;border-radius:8px;padding:10px 14px;margin-top:8px;font-size:12px;color:#4B5563;line-height:1.6}}
.phase-pop.open{{display:block}}
.phase-pop b{{color:#6B21A8}}
.phase-pop .row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}}

/* Compressed Flagship */
.flagship{{background:linear-gradient(135deg,#4C1D95 0%,#7C3AED 100%);color:#fff;border-radius:12px;padding:16px 20px;margin:14px 0;box-shadow:0 4px 14px rgba(76,29,149,.15)}}
.fl-head{{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:12px}}
.fl-head .label{{font-size:10.5px;letter-spacing:.5px;text-transform:uppercase;opacity:.8;font-weight:600}}
.fl-head h2{{margin:2px 0 0;font-size:16px;font-weight:700;letter-spacing:-.01em}}
.fl-tabs{{display:flex;gap:4px;background:rgba(255,255,255,.1);padding:3px;border-radius:8px}}
.fl-tab{{background:none;border:0;color:rgba(255,255,255,.75);padding:6px 12px;border-radius:6px;cursor:pointer;font:inherit;font-size:12px;font-weight:600}}
.fl-tab.active{{background:#fff;color:#4C1D95}}
.fl-pane{{display:none}}
.fl-pane.active{{display:block}}
.fl-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}}
.fl-grid a{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:6px;padding:9px 11px;text-decoration:none;color:#fff;transition:background .15s}}
.fl-grid a:hover{{background:rgba(255,255,255,.18)}}
.fl-grid .num{{font-size:9.5px;opacity:.7;font-weight:600;letter-spacing:.5px}}
.fl-grid .title{{font-size:12px;font-weight:600;margin-top:2px;line-height:1.4}}
.fl-foot{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px;font-size:11.5px;flex-wrap:wrap}}
.fl-foot .more{{background:#fff;color:#4C1D95;padding:5px 12px;border-radius:5px;text-decoration:none;font-weight:700;font-size:11.5px}}
.fl-foot .toggle{{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);color:#fff;padding:5px 10px;border-radius:5px;cursor:pointer;font:inherit;font-size:11px;font-weight:500}}

/* Tier Matrix one-liner: keep as-is from original (passes through tier_alert_html which already has its own styling). Wrapped in margin reset */
.tier-passthrough{{margin:8px 0 16px}}
.tier-passthrough > div{{margin:0 !important}}

/* Sticky toolbar */
.toolbar{{position:sticky;top:48px;z-index:50;background:rgba(250,250,249,.96);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);padding:10px 0;margin:6px -1.5rem 0;border-bottom:1px solid #E5E7EB}}
.toolbar-inner{{max-width:1240px;margin:0 auto;padding:0 1.5rem;display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.search-box{{flex:1 1 280px;min-width:0;position:relative}}
.search-box input{{width:100%;border:1px solid #E5E7EB;border-radius:8px;padding:8px 12px 8px 32px;font:inherit;font-size:13px;background:#fff;color:#1E1B4B;outline:none;transition:border-color .15s,box-shadow .15s}}
.search-box input:focus{{border-color:#7C3AED;box-shadow:0 0 0 3px rgba(124,58,237,.12)}}
.search-box::before{{content:\"🔍\";position:absolute;top:50%;left:10px;transform:translateY(-50%);font-size:13px;opacity:.55;pointer-events:none}}
.f-group{{display:flex;gap:5px;flex-wrap:wrap}}
.f-chip{{background:#fff;border:1px solid #E5E7EB;color:#4B5563;padding:6px 10px;border-radius:14px;cursor:pointer;font:inherit;font-size:11.5px;font-weight:500;transition:all .12s;white-space:nowrap}}
.f-chip:hover{{border-color:#C4B5FD;color:#4C1D95}}
.f-chip.active{{background:#7C3AED;color:#fff;border-color:#7C3AED}}
.f-clear{{background:none;border:0;color:#7C3AED;font:inherit;font-size:11.5px;font-weight:600;cursor:pointer;padding:4px 6px;text-decoration:underline;text-decoration-style:dotted;text-underline-offset:3px}}
.cat-jump{{display:flex;gap:6px;overflow-x:auto;margin:10px -1.5rem 0;padding:6px 1.5rem;border-bottom:1px solid #E5E7EB;background:#fff;scrollbar-width:thin}}
.cat-jump a{{flex-shrink:0;background:#F5F3FF;color:#6B21A8;padding:5px 11px;border-radius:14px;text-decoration:none;font-size:11.5px;font-weight:500;border:1px solid transparent;white-space:nowrap}}
.cat-jump a:hover{{background:#EDE9FE;border-color:#DDD6FE}}
.cat-jump a .n{{color:#94A3B8;font-size:10.5px;margin-left:4px;font-weight:400}}
.filter-status{{font-size:11.5px;color:#6B7280;margin-top:10px}}
.filter-status b{{color:#4C1D95;font-weight:700}}

/* Categories */
.category{{margin-top:24px;border:1px solid #E5E7EB;border-radius:10px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.025);overflow:hidden;scroll-margin-top:130px}}
.cat-head{{display:flex;align-items:center;justify-content:space-between;padding:12px 18px;border-bottom:1px solid #E5E7EB;background:linear-gradient(90deg,#F5F3FF,#fff);gap:10px;flex-wrap:wrap;cursor:pointer;user-select:none}}
.cat-head:hover{{background:linear-gradient(90deg,#EDE9FE,#FAF5FF)}}
.cat-head .left{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.cat-head h2{{margin:0;color:#4C1D95;font-size:15.5px;font-weight:700}}
.cat-head .cat-icon{{font-size:18px}}
.cat-head .count{{background:#EDE9FE;color:#6B21A8;padding:2px 10px;border-radius:14px;font-size:11px;font-weight:600}}
.cat-head .hint{{color:#94A3B8;font-size:11.5px;flex:1 1 auto;text-align:right}}
.cat-chev{{font-size:11px;color:#7C3AED;transition:transform .25s;font-weight:700;display:inline-block}}
.category:not(.open) .cat-chev{{transform:rotate(-90deg)}}
.cat-body{{padding:14px 18px 18px}}
.category:not(.open) .cat-body{{display:none}}

/* Topic grid */
.topic-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:10px}}
.topic-card{{background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:11px 14px;transition:border-color .15s,box-shadow .15s;display:flex;flex-direction:column}}
.topic-card:hover{{border-color:#C4B5FD;box-shadow:0 2px 10px rgba(124,58,237,.06)}}
.topic-card.is-parent{{background:linear-gradient(180deg,#FAF5FF,#fff);border-color:#DDD6FE;grid-column:1/-1}}

.tc-head{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.tc-num{{flex:0 0 auto;background:#EDE9FE;color:#6B21A8;font-weight:700;font-size:11.5px;min-width:22px;height:22px;padding:0 5px;border-radius:5px;display:inline-flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',ui-monospace,monospace}}
.topic-card.is-parent .tc-num{{background:#7C3AED;color:#fff}}
.tc-title{{flex:1 1 auto;min-width:0;font-size:14.5px;font-weight:700;color:#4C1D95;text-decoration:none;line-height:1.35}}
.tc-title:hover{{color:#7C3AED;text-decoration:underline}}
.tc-title .arrow{{font-size:12px;opacity:.55;font-weight:500;margin-left:3px}}
.tc-badge{{background:#7C3AED;color:#fff;padding:1px 6px;border-radius:3px;font-size:9.5px;font-weight:600;letter-spacing:.3px}}
.tc-badge.child{{background:#F5F3FF;color:#7C3AED;border:1px solid #DDD6FE}}
.tc-phase{{display:inline-block;padding:2px 7px;border-radius:8px;font-size:10px;font-weight:600;flex-shrink:0}}
.phase-I{{background:#DCFCE7;color:#166534}}
.phase-II{{background:#FEF3C7;color:#92400E}}
.phase-III{{background:#FEE2E2;color:#991B1B}}
.phase-IV{{background:#E0E7FF;color:#3730A3}}
.tc-expand{{flex:0 0 auto;background:none;border:0;color:#94A3B8;cursor:pointer;font-size:13px;padding:2px 4px;line-height:1;transition:transform .2s,color .15s}}
.tc-expand:hover{{color:#7C3AED}}
.topic-card.expanded .tc-expand{{transform:rotate(180deg);color:#7C3AED}}

.tc-thesis-short{{font-size:12px;color:#4B5563;margin-top:6px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;text-overflow:ellipsis}}

.tc-details{{display:none;border-top:1px dashed #E5E7EB;margin-top:10px;padding-top:10px}}
.topic-card.expanded .tc-details{{display:block}}
.tc-tags{{color:#6B7280;font-size:11.5px;margin-bottom:6px}}
.tc-meta{{display:flex;flex-wrap:wrap;gap:5px 8px;align-items:center;margin-bottom:6px;font-size:11px;color:#6B7280}}
.tc-meta .chip{{display:inline-flex;align-items:center;gap:3px;background:#F3F4F6;padding:2px 7px;border-radius:9px;color:#4B5563;font-weight:500}}
.tc-thesis-full{{padding:8px 11px;background:#FAFAF9;border-left:3px solid #C4B5FD;border-radius:0 4px 4px 0;font-size:11.5px;color:#4B5563;line-height:1.55;margin-top:4px}}
.tc-thesis-full::before{{content:\"非共識\";display:block;font-size:9px;color:#7C3AED;font-weight:700;letter-spacing:.5px;text-transform:uppercase;margin-bottom:2px}}

.tc-children{{margin-top:8px;display:flex;flex-wrap:wrap;gap:5px;align-items:center}}
.tc-children .label{{font-size:10px;color:#7C3AED;font-weight:700;letter-spacing:.3px}}
.tc-chip{{display:inline-flex;align-items:center;gap:3px;background:#fff;border:1px solid #C4B5FD;color:#6B21A8;padding:3px 9px;border-radius:12px;font-size:11px;font-weight:600;text-decoration:none;transition:all .15s}}
.tc-chip:hover{{background:#7C3AED;color:#fff;border-color:#7C3AED}}
.tc-chip .arrow{{font-size:9px;opacity:.7}}

.empty-state{{text-align:center;padding:18px 14px;color:#94A3B8;font-size:12px}}
.empty-state .eco{{font-size:24px;margin-bottom:4px}}
.suggest{{background:#F5F3FF;border:1px dashed #C4B5FD;border-radius:6px;padding:10px 14px;margin-top:10px;color:#6B21A8;font-size:12px;line-height:1.65}}
.suggest summary{{cursor:pointer;font-weight:600;list-style:none;color:#4C1D95}}
.suggest summary::-webkit-details-marker{{display:none}}
.suggest summary::before{{content:\"▸\";display:inline-block;margin-right:6px;transition:transform .2s}}
.suggest[open] summary::before{{transform:rotate(90deg)}}
.suggest-body{{margin-top:8px}}
.suggest strong{{color:#4C1D95}}
.suggest code{{background:#EDE9FE;padding:1px 6px;border-radius:3px;color:#6B21A8;font-size:11.5px;font-weight:600}}
.suggest ul{{margin:8px 0 0;padding-left:18px}}
.suggest ul li{{margin-bottom:6px;color:#4C1D95;font-size:11.5px}}

.footer{{margin-top:2.5rem;padding-top:1rem;border-top:1px solid #E5E7EB;color:#6B7280;font-size:.78rem;text-align:center}}

.topic-card.hidden,.category.hidden{{display:none !important}}

/* ===== Responsive breakpoints =====
   ≥1280px desktop（容器封頂 1240）
   1024-1280 平板橫 / 小桌面（保留 2 col）
   768-1024 平板直 / 大手機橫
   480-768 手機橫 / 小平板直
   ≤480 手機直
   ≤360 ultra narrow
*/
@media(max-width:1024px){{
  .container{{padding:1.2rem 1.2rem 2.5rem}}
  .toolbar{{margin:6px -1.2rem 0}}
  .toolbar-inner{{padding:0 1.2rem}}
  .cat-jump{{margin:8px -1.2rem 0;padding:6px 1.2rem}}
  .head-row{{align-items:flex-start}}
  .meta-strip{{font-size:11px;gap:6px 8px}}
  .meta-strip .item{{padding:4px 8px}}
  .flagship{{padding:14px 16px}}
  .fl-grid{{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}}
  .topic-grid{{gap:8px}}
}}
@media(max-width:768px){{
  .container{{padding:1rem 1rem 2.2rem}}
  h1{{font-size:1.4rem}}
  .sub{{font-size:.85rem}}
  .head-row{{flex-direction:column;gap:10px;padding-bottom:10px;margin-bottom:10px}}
  .meta-strip{{width:100%}}
  .toolbar{{margin:6px -1rem 0;top:46px;padding:8px 0}}
  .toolbar-inner{{padding:0 1rem;gap:6px}}
  .search-box{{flex:1 1 100%;order:1}}
  .toolbar .f-group{{order:2}}
  .toolbar .f-clear{{order:3}}
  .cat-jump{{margin:8px -1rem 0;padding:6px 1rem;-webkit-overflow-scrolling:touch}}
  .topic-grid{{grid-template-columns:1fr;gap:8px}}
  .topic-card{{padding:10px 12px}}
  .topic-card.is-parent{{grid-column:auto}}
  .fl-head{{flex-direction:column;align-items:flex-start;gap:10px}}
  .fl-tabs{{align-self:stretch}}
  .fl-tab{{flex:1 1 50%;text-align:center}}
  .fl-grid{{grid-template-columns:1fr 1fr}}
  .tc-title{{font-size:13.5px}}
  .tc-num{{font-size:11px;height:20px;min-width:20px;padding:0 4px}}
  .tc-badge{{font-size:9px;padding:1px 5px}}
  .tc-phase{{font-size:9.5px;padding:1px 6px}}
  .cat-head{{padding:11px 14px}}
  .cat-head h2{{font-size:14.5px}}
  .cat-head .hint{{display:none}}
  .cat-body{{padding:12px 12px 14px}}
  /* Tier matrix passthrough — force wrap on tiny screens */
  .tier-passthrough > div{{font-size:12px !important}}
  .tier-passthrough > div span{{word-break:break-all}}
}}
@media(max-width:480px){{
  body{{font-size:13.5px}}
  .container{{padding:.85rem .8rem 2rem}}
  h1{{font-size:1.25rem}}
  .sub{{font-size:.82rem;line-height:1.5}}
  .meta-strip{{display:grid;grid-template-columns:repeat(2,1fr);gap:6px;width:100%}}
  .meta-strip .item{{justify-content:center;padding:5px 8px;font-size:10.5px}}
  .meta-strip .info-toggle{{grid-column:1/-1;text-align:center;padding:4px 0}}
  .toolbar{{margin:6px -.8rem 0;top:42px}}
  .toolbar-inner{{padding:0 .8rem}}
  .cat-jump{{margin:8px -.8rem 0;padding:6px .8rem}}
  .flagship{{padding:12px 14px;border-radius:10px}}
  .fl-head h2{{font-size:14.5px}}
  .fl-head .label{{font-size:9.5px}}
  .fl-grid{{grid-template-columns:1fr}}
  .fl-foot{{flex-direction:column;align-items:stretch;gap:6px}}
  .fl-foot .more,.fl-foot .toggle{{text-align:center}}
  .topic-card{{padding:9px 11px;border-radius:7px}}
  .tc-head{{gap:6px}}
  .tc-title{{font-size:13px;flex:1 1 100%;order:2}}
  .tc-num{{order:1}}
  .tc-badge,.tc-phase{{order:3}}
  .tc-expand{{order:4;margin-left:auto}}
  .tc-thesis-short{{font-size:11.5px;margin-top:5px;-webkit-line-clamp:3}}
  .tc-children{{margin-top:6px;gap:4px}}
  .tc-chip{{font-size:10.5px;padding:2px 8px}}
  .tc-tags,.tc-meta{{font-size:10.5px}}
  .tc-thesis-full{{font-size:11px;padding:7px 9px}}
  .cat-head{{padding:10px 12px;gap:6px}}
  .cat-head h2{{font-size:14px}}
  .cat-head .count{{font-size:10.5px;padding:2px 8px}}
  .cat-body{{padding:10px 10px 12px}}
  .filter-status{{font-size:11px}}
  .suggest{{padding:9px 12px;font-size:11.5px}}
  .suggest ul{{padding-left:16px}}
  .suggest ul li{{font-size:11px}}
  .phase-pop .row{{grid-template-columns:1fr}}
}}
@media(max-width:360px){{
  .container{{padding:.7rem .65rem 1.8rem}}
  h1{{font-size:1.15rem}}
  .meta-strip{{grid-template-columns:1fr;gap:4px}}
  .meta-strip .info-toggle{{grid-column:auto}}
  .toolbar{{margin:5px -.65rem 0}}
  .toolbar-inner{{padding:0 .65rem}}
  .cat-jump{{margin:6px -.65rem 0;padding:5px .65rem}}
  .topic-card{{padding:8px 10px}}
  .tc-head{{gap:5px}}
  .tc-title{{font-size:12.5px}}
  .tc-thesis-short{{font-size:11px;-webkit-line-clamp:4}}
  .fl-tab{{font-size:11px;padding:5px 8px}}
}}
/* Landscape phones (low height): keep sticky usable */
@media(max-height:500px) and (orientation:landscape){{
  .toolbar{{position:static;border-bottom:none}}
  .imq-nav-root{{position:static}}
  .category{{scroll-margin-top:8px}}
}}
/* Wide screens: allow optional 3-col (still respects 1240 cap) */
@media(min-width:1280px){{
  .topic-grid{{grid-template-columns:repeat(auto-fit,minmax(360px,1fr))}}
}}
/* Print */
@media print{{
  .toolbar,.cat-jump,.tc-expand,.imq-nav-root{{display:none !important}}
  .category{{break-inside:avoid;page-break-inside:avoid}}
  .topic-card{{break-inside:avoid}}
  .tc-details{{display:block !important}}
  .category:not(.open) .cat-body{{display:block !important}}
  body{{font-size:11px}}
}}
</style>
</head>
<body>

{nav_html}

<div class=\"container\">
  <div class=\"crumb\"><a href=\"/\">首頁</a> &rsaquo; <a href=\"/research/\">研究</a> &rsaquo; 產業深度</div>

  <div class=\"head-row\">
    <div>
      <h1>產業深度報告</h1>
      <p class=\"sub\">跨多檔個股共用的產業研究，由 <code>industry-analyst</code> 產出。個股 DD 可引用對應 ID 作為背景，避免重複鋪墊。</p>
    </div>
    <div class=\"meta-strip\">
      <span class=\"item\"><b>{s('已建 ID 總數', '30')}</b> 已建 ID</span>
      <span class=\"item\"><b>{s('涵蓋個股', '50+')}</b> 涵蓋個股</span>
      <span class=\"item\">🟡 <b>{s('平均 🟡 比例', '18%')}</b> · 上限 20%</span>
      <span class=\"item\">T1 <b>{s('平均 T1 來源占比', '60%+')}</b></span>
      <button class=\"info-toggle\" id=\"phase-info-btn\">ⓘ Phase 說明</button>
    </div>
  </div>
  <div class=\"phase-pop\" id=\"phase-info\">
    <div class=\"row\">
      <div><b>Phase I · CAPEX 爆發</b><br>設備商最先兌現；新技術導入期，材料/工具供應商毛利最好。</div>
      <div><b>Phase II · 材料高毛利 / 擴產期</b><br>量產穩定，化學/材料/IP 授權穩定收割；ROIC 達高點。</div>
      <div><b>Phase III · 封裝 / 應用集中</b><br>下游擴產，封測/系統整合商利潤集中；估值常提前 price in。</div>
      <div><b>Phase IV · 後段 / 結構性分化</b><br>K 形分歧、subsegment 結構性贏家集中；估值通常已 price in 大部分。</div>
    </div>
  </div>

  <div class=\"flagship\" id=\"flagship\">
    <div class=\"fl-head\">
      <div>
        <div class=\"label\">⭐ Flagship · Cross-ID Synthesis · <span id=\"flagship-status\" class=\"status\">🟢 Fresh</span></div>
        <h2 id=\"fl-title\">{fl_ai_title}</h2>
      </div>
      <div class=\"fl-tabs\" role=\"tablist\">
        <button class=\"fl-tab active\" data-pane=\"ai\">AI 基建</button>
        <button class=\"fl-tab\" data-pane=\"sw\">軟體股</button>
      </div>
    </div>
    {fl_ai_pane}
    {fl_sw_pane}
  </div>

  <div class=\"tier-passthrough\">{tier_alert_html}</div>

  <div class=\"toolbar\">
    <div class=\"toolbar-inner\">
      <div class=\"search-box\">
        <input id=\"q\" type=\"search\" placeholder=\"搜尋產業 / 標題 / ticker / tag（如 CoWoS、CRWD、液冷）\" autocomplete=\"off\">
      </div>
      <div class=\"f-group\" id=\"type-filter\">
        <button class=\"f-chip\" data-filter=\"type\" data-val=\"parent\">母題</button>
        <button class=\"f-chip\" data-filter=\"type\" data-val=\"child\">子題</button>
      </div>
      <button class=\"f-clear\" id=\"clear-filters\">清除</button>
    </div>
    <div class=\"cat-jump\">
      {cat_jump_html}
    </div>
  </div>
  <div class=\"filter-status\" id=\"filter-status\">顯示全部 <b id=\"visible-count\">—</b> 份報告</div>

  {cats_html}

  <div style=\"margin-top:32px;padding:14px 18px;background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:6px;font-size:12.5px;color:#4C1D95;line-height:1.65\">
    {trigger_html}
  </div>
</div>

<div class=\"footer\">
  InvestMQuest Research · 產業深度由 industry-analyst v1.4 自動生成 · 沿用 Claude Opus 深度研究能力
</div>

<script>
// Phase popup
document.getElementById('phase-info-btn').addEventListener('click', function(){{
  document.getElementById('phase-info').classList.toggle('open');
}});

// Flagship tabs
document.querySelectorAll('.fl-tab').forEach(function(btn){{
  btn.addEventListener('click', function(){{
    var pane = btn.dataset.pane;
    document.querySelectorAll('.fl-tab').forEach(function(b){{b.classList.toggle('active', b===btn);}});
    document.querySelectorAll('.fl-pane').forEach(function(p){{p.classList.toggle('active', p.dataset.pane===pane);}});
    var titleMap = {{ai: {fl_ai_title!r}, sw: {fl_sw_title!r}}};
    document.getElementById('fl-title').textContent = titleMap[pane] || titleMap.ai;
  }});
}});

// Flagship show-all toggle
function applyFlagshipCollapse(){{
  document.querySelectorAll('.fl-grid').forEach(function(g){{
    var collapsed = g.dataset.collapsed === 'true';
    g.querySelectorAll('a.extra').forEach(function(a){{a.style.display = collapsed ? 'none' : '';}});
  }});
}}
document.querySelectorAll('.fl-foot .toggle').forEach(function(btn){{
  btn.addEventListener('click', function(){{
    var grid = btn.closest('.fl-pane').querySelector('.fl-grid');
    grid.dataset.collapsed = grid.dataset.collapsed === 'true' ? 'false' : 'true';
    var n = grid.querySelectorAll('a').length;
    btn.textContent = grid.dataset.collapsed === 'true' ? ('查看全部 ' + n + ' 個 ▾') : '收起 ▴';
    applyFlagshipCollapse();
  }});
}});
applyFlagshipCollapse();

// Topic card expand (event delegation)
document.addEventListener('click', function(e){{
  var btn = e.target.closest('.tc-expand');
  if(!btn) return;
  e.preventDefault();
  btn.closest('.topic-card').classList.toggle('expanded');
}});

// Category accordion
document.querySelectorAll('.category > .cat-head').forEach(function(head){{
  head.addEventListener('click', function(e){{
    if(e.target.closest('a, button')) return;
    head.parentElement.classList.toggle('open');
  }});
}});

// Filters & search
var filterState = {{type:new Set(), q:''}};
function applyFilters(){{
  var visible = 0;
  document.querySelectorAll('.topic-card').forEach(function(card){{
    var ok = true;
    if(filterState.type.size > 0 && !filterState.type.has(card.dataset.type)) ok = false;
    if(ok && filterState.q){{
      var hay = (card.dataset.search || '') + ' ' + card.textContent.toLowerCase();
      if(hay.indexOf(filterState.q) === -1) ok = false;
    }}
    card.classList.toggle('hidden', !ok);
    if(ok) visible++;
  }});
  document.querySelectorAll('.category').forEach(function(cat){{
    var topics = cat.querySelectorAll('.topic-card');
    if(topics.length === 0) return;
    var anyVisible = Array.from(topics).some(function(c){{return !c.classList.contains('hidden');}});
    cat.classList.toggle('hidden', !anyVisible);
  }});
  document.getElementById('visible-count').textContent = visible;
  var any = filterState.type.size || filterState.q;
  document.getElementById('filter-status').firstChild.textContent = any ? '篩選後顯示 ' : '顯示全部 ';
}}

document.querySelectorAll('.f-chip').forEach(function(chip){{
  chip.addEventListener('click', function(){{
    var f = chip.dataset.filter, v = chip.dataset.val;
    if(filterState[f].has(v)){{ filterState[f].delete(v); chip.classList.remove('active'); }}
    else {{ filterState[f].add(v); chip.classList.add('active'); }}
    applyFilters();
  }});
}});
document.getElementById('q').addEventListener('input', function(e){{
  filterState.q = e.target.value.trim().toLowerCase();
  applyFilters();
}});
document.getElementById('clear-filters').addEventListener('click', function(){{
  filterState.type.clear(); filterState.q = '';
  document.querySelectorAll('.f-chip.active').forEach(function(c){{c.classList.remove('active');}});
  document.getElementById('q').value = '';
  applyFilters();
}});
applyFilters();

// Freshness updater (preserve original behavior)
(function(){{
  const LAST_REFRESH = '2026-04-19';
  const today = new Date();
  const daysSince = Math.floor((today - new Date(LAST_REFRESH)) / (1000 * 60 * 60 * 24));
  const el = document.getElementById('flagship-status');
  if(!el) return;
  if(daysSince < 60){{ el.textContent = '🟢 Fresh'; }}
  else if(daysSince < 90){{ el.textContent = '🟡 Approaching refresh'; }}
  else if(daysSince < 120){{ el.textContent = '🟠 B refresh 已到期'; }}
  else {{ el.textContent = '🔴 Overdue'; }}
}})();

// Open ID report links in new tab (preserve original behavior)
document.querySelectorAll('a[href*="/id/ID_"]').forEach(function(a){{
  a.target = '_blank';
  a.rel = 'noopener';
}});
</script>

</body>
</html>
"""


if __name__ == "__main__":
    main()
