#!/usr/bin/env python3
"""
retrofit_ds_references.py — One-shot migration of DS HTML reports from
industry-ds skill v1.1 (inline source-tags) to v1.2 (§-end aside refs).

What it does:
  For each docs/ds/DS_*.html file:
  1. Find every <section id="sN" ...> block.
  2. Within each section, collect all
     <span class="source-tag">[TIER: <a href="URL">TITLE</a>]</span>
     in document order.
  3. Deduplicate by URL (keep first occurrence's tier + title).
  4. Remove the inline spans from section body; clean up residual whitespace
     artifacts (double spaces, lonely ，/。/；/ before CJK text).
  5. Build <aside class="ds-refs"> HTML if the section had any source-tags.
  6. Insert aside immediately before </section>.
  7. Replace the .source-tag CSS block in <style> with the .ds-refs CSS block.
  8. Save in-place (or print diff if --dry-run).

Usage:
  python3 scripts/retrofit_ds_references.py              # batch all DS files
  python3 scripts/retrofit_ds_references.py --dry-run    # preview only
  python3 scripts/retrofit_ds_references.py --file docs/ds/DS_Foo_20260513.html

This is a one-shot retrofit for the v1.1 → v1.2 migration.
Files that have no inline source-tags are skipped silently (already migrated).

IMPORTANT: Does NOT touch <span class="ds-derive"> or <div class="ds-derive"> —
those are the math/calculation traceability lines that remain inline per spec.
"""

import re
import os
import sys
import argparse
from collections import OrderedDict

# ---------------------------------------------------------------------------
# CSS blocks
# ---------------------------------------------------------------------------

# The old inline source-tag CSS (3 lines) to be removed.
# Matches: .source-tag{...}\n.source-tag a{...}\n.source-tag a:hover{...}
OLD_SOURCE_TAG_CSS_PATTERN = re.compile(
    r'\.source-tag\{[^}]+\}\n\.source-tag a\{[^}]+\}\n\.source-tag a:hover\{[^}]+\}',
    re.DOTALL,
)

# New .ds-refs CSS block that replaces the old source-tag block.
NEW_DS_REFS_CSS = (
    ".ds-refs{margin:28px 0 8px;padding:10px 14px;background:#FAFAF9;"
    "border-left:2px solid #D1D5DB;border-radius:3px;font-size:12px;"
    "color:#6B7280;line-height:1.7}\n"
    ".ds-refs .ds-refs-label{color:#4B5563;font-size:10.5px;letter-spacing:.5px;"
    "text-transform:uppercase;display:block;margin-bottom:6px;font-weight:700}\n"
    ".ds-refs ol{margin:0;padding-left:20px}\n"
    ".ds-refs li{margin:3px 0}\n"
    ".ds-refs a{color:#7C3AED;text-decoration:none}\n"
    ".ds-refs a:hover{text-decoration:underline}\n"
    ".ds-refs .tier{display:inline-block;color:#4B5563;font-weight:600;"
    "margin-right:6px;font-size:11px}"
)

# ---------------------------------------------------------------------------
# Source-tag extraction
# ---------------------------------------------------------------------------

# Matches: <span class="source-tag">[TIER: <a href="URL">TITLE</a>]</span>
# TIER: T1, T2, T3-A, T3-B, T3-C, T1-zh, T2-zh, T3-zh, T4
INLINE_TAG_PATTERN = re.compile(
    r'<span\s+class="source-tag">'
    r'\[(?P<tier>T[1234](?:-[ABCzh]+)?)'
    r'[:：]\s*'
    r'<a\s+href="(?P<url>[^"]*)">'
    r'(?P<title>[^<]*)'
    r'</a>'
    r'\]'
    r'</span>',
    re.DOTALL,
)


def extract_tags_from_section(section_html):
    """
    Return an OrderedDict mapping url -> (tier, title) for all inline source-tags
    found in section_html, in document order (first occurrence wins for dedup).
    """
    refs = OrderedDict()
    for m in INLINE_TAG_PATTERN.finditer(section_html):
        tier = m.group('tier')
        url = m.group('url').strip()
        title = m.group('title').strip()
        if url not in refs:
            refs[url] = (tier, title)
    return refs


def remove_inline_tags(section_html):
    """
    Remove all <span class="source-tag">...</span> from section_html.
    After removal, clean up common residual artifacts:
    - Multiple consecutive spaces collapsed to one
    - Spaces before CJK punctuation (，、。；：！？）》〕】）)
    - Trailing space before </p>, </td>, </div>, </li>
    - Lonely leading space at start of text node (e.g. "text  ，" -> "text，")
    """
    cleaned = INLINE_TAG_PATTERN.sub('', section_html)

    # collapse multiple spaces (but not newlines/indentation)
    cleaned = re.sub(r'[ \t]{2,}', ' ', cleaned)

    # remove space before CJK punctuation
    cleaned = re.sub(r'\s+([，、。；：！？）》〕】）」』])', r'\1', cleaned)

    # remove trailing space before closing tags
    cleaned = re.sub(r'\s+(</(?:p|td|div|li|th|span|em|strong)>)', r'\1', cleaned)

    # remove space after opening tag that immediately precedes CJK (rare but possible)
    # e.g. "> ，" -> ">，"
    cleaned = re.sub(r'(>[^<]*?)\s+([，。；：！？])', lambda m: m.group(1) + m.group(2), cleaned)

    return cleaned


# ---------------------------------------------------------------------------
# Aside builder
# ---------------------------------------------------------------------------

def build_aside_html(refs):
    """
    Build <aside class="ds-refs"> HTML from an OrderedDict of url -> (tier, title).
    Returns empty string if refs is empty.
    """
    if not refs:
        return ''

    lines = ['<aside class="ds-refs">']
    lines.append('  <span class="ds-refs-label">本節參考來源</span>')
    lines.append('  <ol>')
    for url, (tier, title) in refs.items():
        # Escape any HTML entities that might be in title already handled, but
        # since these come from existing HTML we pass them through as-is.
        lines.append(
            f'    <li><span class="tier">[{tier}]</span>'
            f'<a href="{url}">{title}</a></li>'
        )
    lines.append('  </ol>')
    lines.append('</aside>')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Section processing
# ---------------------------------------------------------------------------

# Matches <section id="sN"> ... </section> with optional class attribute.
# We use a non-greedy approach and anchor on </section> to avoid crossing sections.
SECTION_PATTERN = re.compile(
    r'(<section[^>]*id="s\d+"[^>]*>)(.*?)(</section>)',
    re.DOTALL,
)


def process_section(open_tag, body, close_tag):
    """
    Process one <section> block:
    - Extract inline source-tags
    - Remove them from body
    - Build aside HTML
    - Return (new_section_html, tag_count, aside_inserted, tier_counts)
    """
    refs = extract_tags_from_section(body)
    tag_count = len(list(INLINE_TAG_PATTERN.finditer(body)))  # raw count before dedup

    clean_body = remove_inline_tags(body)
    aside_html = build_aside_html(refs)

    if aside_html:
        # Insert aside just before </section>, with a newline separator.
        # Check if body ends with whitespace to avoid double blank lines.
        new_body = clean_body.rstrip('\n') + '\n\n' + aside_html + '\n'
        aside_inserted = True
    else:
        new_body = clean_body
        aside_inserted = False

    new_section = open_tag + new_body + close_tag

    # Compute tier counts from refs (deduped)
    tier_counts = {}
    for url, (tier, title) in refs.items():
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

    return new_section, tag_count, aside_inserted, tier_counts


# ---------------------------------------------------------------------------
# CSS replacement
# ---------------------------------------------------------------------------

def replace_css(html):
    """
    Replace the old .source-tag CSS block with the new .ds-refs CSS block.
    Returns (new_html, css_replaced_bool).
    """
    if OLD_SOURCE_TAG_CSS_PATTERN.search(html):
        new_html = OLD_SOURCE_TAG_CSS_PATTERN.sub(NEW_DS_REFS_CSS, html, count=1)
        return new_html, True
    # Maybe the 3 lines aren't adjacent but individually present — try line by line.
    # Also handle cases where `display:inline` variant was used.
    alt_pattern = re.compile(
        r'\.source-tag\{[^}]+\}\n?\.source-tag\s+a\{[^}]+\}\n?\.source-tag\s+a:hover\{[^}]+\}',
        re.DOTALL,
    )
    if alt_pattern.search(html):
        new_html = alt_pattern.sub(NEW_DS_REFS_CSS, html, count=1)
        return new_html, True
    return html, False


# ---------------------------------------------------------------------------
# Per-file retrofit
# ---------------------------------------------------------------------------

def retrofit_file(path, dry_run=False):
    """
    Retrofit a single DS HTML file.
    Returns a dict with stats, or None if file skipped (no inline source-tags).
    """
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    # Skip files with no inline source-tags (already migrated or v1.0).
    if not INLINE_TAG_PATTERN.search(original):
        return None

    html = original

    # Step 1: Replace section-by-section
    total_tags = 0
    total_asides = 0
    section_count = 0
    all_tier_counts = {}

    def replace_section(m):
        nonlocal total_tags, total_asides, section_count, all_tier_counts
        open_tag = m.group(1)
        body = m.group(2)
        close_tag = m.group(3)
        section_count += 1
        new_section, tag_count, aside_inserted, tier_counts = process_section(
            open_tag, body, close_tag
        )
        total_tags += tag_count
        if aside_inserted:
            total_asides += 1
        for tier, cnt in tier_counts.items():
            all_tier_counts[tier] = all_tier_counts.get(tier, 0) + cnt
        return new_section

    html = SECTION_PATTERN.sub(replace_section, html)

    # Step 2: Replace CSS
    html, css_replaced = replace_css(html)

    # Compute T1 stats
    t1_count = all_tier_counts.get('T1', 0) + all_tier_counts.get('T1-zh', 0)
    total_refs = sum(all_tier_counts.values())
    t1_share = t1_count / total_refs if total_refs else 0

    stats = {
        'path': path,
        'filename': os.path.basename(path),
        'sections': section_count,
        'tags_extracted': total_tags,
        'asides_inserted': total_asides,
        'css_replaced': css_replaced,
        'tier_counts': all_tier_counts,
        't1_count': t1_count,
        'total_refs': total_refs,
        't1_share': t1_share,
    }

    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

    return stats


# ---------------------------------------------------------------------------
# Summary printing
# ---------------------------------------------------------------------------

def print_file_stats(stats, dry_run=False):
    prefix = '[DRY-RUN] ' if dry_run else ''
    tc = stats['tier_counts']

    # Build tier summary string
    t1 = tc.get('T1', 0) + tc.get('T1-zh', 0)
    t2 = tc.get('T2', 0) + tc.get('T2-zh', 0)
    t3 = (tc.get('T3-A', 0) + tc.get('T3-B', 0) +
          tc.get('T3-C', 0) + tc.get('T3-zh', 0))
    t4 = tc.get('T4', 0)

    print(
        f"{prefix}{stats['filename']}: "
        f"{stats['sections']} sections, "
        f"{stats['tags_extracted']} source-tags → "
        f"{stats['asides_inserted']} asides "
        f"(T1: {t1}, T2: {t2}, T3: {t3}, T4: {t4})"
    )
    if stats['total_refs'] > 0:
        t1_share_pct = stats['t1_share'] * 100
        status = 'PASS' if stats['t1_share'] >= 0.50 else 'WARN: T1 < 50%'
        print(f"  T1 占比: {t1_share_pct:.1f}% [{status}]")
    if not stats['css_replaced']:
        print('  WARNING: .source-tag CSS block not found — CSS not updated')
    if not dry_run:
        print(f"  Saved: {stats['path']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Retrofit DS HTML files from v1.1 inline source-tags to v1.2 aside refs.'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print what would change but do not write files.',
    )
    parser.add_argument(
        '--file',
        metavar='PATH',
        help='Retrofit a single file instead of all docs/ds/DS_*.html.',
    )
    args = parser.parse_args()

    # Determine target files
    if args.file:
        targets = [args.file]
    else:
        ds_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'docs', 'ds',
        )
        if not os.path.isdir(ds_dir):
            print(f'ERROR: DS directory not found: {ds_dir}', file=sys.stderr)
            sys.exit(1)
        targets = sorted(
            os.path.join(ds_dir, fn)
            for fn in os.listdir(ds_dir)
            if fn.startswith('DS_') and fn.endswith('.html')
        )

    if not targets:
        print('No DS HTML files found.')
        return

    all_stats = []
    skipped = 0

    for path in targets:
        if not os.path.isfile(path):
            print(f'WARNING: File not found: {path}', file=sys.stderr)
            continue

        stats = retrofit_file(path, dry_run=args.dry_run)
        if stats is None:
            print(f'SKIP: {os.path.basename(path)} (no inline source-tags found)')
            skipped += 1
        else:
            print_file_stats(stats, dry_run=args.dry_run)
            all_stats.append(stats)

    # Global summary
    if all_stats:
        print()
        print('=' * 60)
        print('GLOBAL SUMMARY')
        print('=' * 60)
        total_files = len(all_stats)
        total_tags = sum(s['tags_extracted'] for s in all_stats)
        total_asides = sum(s['asides_inserted'] for s in all_stats)
        total_t1 = sum(s['t1_count'] for s in all_stats)
        total_refs = sum(s['total_refs'] for s in all_stats)
        global_t1_share = total_t1 / total_refs if total_refs else 0

        print(f'Files processed : {total_files}  (skipped: {skipped})')
        print(f'Source-tags extracted : {total_tags}')
        print(f'Asides inserted       : {total_asides}')
        print(f'Global T1 占比        : {global_t1_share:.1%}  '
              f'({"PASS" if global_t1_share >= 0.50 else "WARN: T1 < 50%"})')
        if args.dry_run:
            print()
            print('DRY-RUN mode: no files were modified.')


if __name__ == '__main__':
    main()
