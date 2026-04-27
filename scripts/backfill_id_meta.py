#!/usr/bin/env python3
"""Backfill <script id="id-meta"> JSON block into legacy ID HTML files.

Extracts:
  - theme, skill_version, id_version, publish_date, sections_refreshed
    from existing <meta name="id-*"> tags
  - related_tickers from §11 關聯個股清單 table
  - oneliner from §0 / §1 first paragraph (best-effort, length-capped)

Conservative defaults for fields that need judgment:
  - thesis_type = "structural" (most industry DDs are structural)
  - ai_exposure = "🟡" (neutral; user can patch to 🟢/🔴 manually)

Usage:
  python scripts/backfill_id_meta.py --dry-run
  python scripts/backfill_id_meta.py
  python scripts/backfill_id_meta.py --file ID_AIEDAIP_20260427.html
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"

ID_META_RE = re.compile(
    r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
META_TAG_RE = re.compile(
    r'<meta\s+name="(id-[^"]+)"\s+content="([^"]*)"', re.IGNORECASE
)
INSERT_AFTER_RE = re.compile(r'(<title>[^<]*</title>)')

# §11 row format: tier-red/yellow/green pill = depth; "受益"/"受害" in 3rd cell
TIER_COLOR_TO_EMOJI = {"red": "🔴", "yellow": "🟡", "green": "🟢"}

# Capture: ticker (1st td), depth color (tier-X class), beneficiary (受益/受害 text), role (5th-7th td concat)
SEC11_ROW_RE = re.compile(
    r'<tr>\s*<td[^>]*>\s*([^<]{1,50}?)\s*</td>\s*'
    r'<td[^>]*>\s*<span\s+class="tier-pill\s+tier-(red|yellow|green)"[^>]*>[^<]*</span>\s*</td>\s*'
    r'<td[^>]*>\s*([^<]+?)\s*</td>'
    r'(?:[^<]*<td[^>]*>[^<]*</td>){0,2}'
    r'\s*<td[^>]*>\s*([^<]+?)\s*</td>',
    re.DOTALL,
)

# Find theme name from <meta name="id-theme"> or fallback from filename suffix
THEME_FROM_FILENAME_RE = re.compile(r'^ID_(.+?)_\d{8}\.html$')


def _strip_tags(s: str) -> str:
    return re.sub(r'<[^>]+>', '', s).strip()


def _trim_oneliner(s: str, cap: int = 198) -> str:
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) > cap:
        s = s[:cap].rstrip("，。、；,.:;") + "…"
    return s


def harvest_meta_tags(text: str) -> dict:
    out = {}
    for name, content in META_TAG_RE.findall(text):
        if name == "id-theme":
            out["theme"] = content
        elif name == "id-skill-version":
            out["skill_version"] = content if content.startswith("v") else f"v{content}"
        elif name == "id-version":
            out["id_version"] = content if content.startswith("v") else f"v{content}"
        elif name == "id-publish-date":
            out["publish_date"] = content
        elif name == "id-sections-refreshed":
            try:
                out["sections_refreshed"] = json.loads(content)
            except json.JSONDecodeError:
                pass
    return out


def harvest_related_tickers(text: str) -> list:
    """Parse §11 關聯個股 table rows. Uses a simpler row-by-row approach
    because the table format varies across IDs (different cell counts,
    nested tags). Strategy: split on </tr>, then per row extract ticker,
    tier color, beneficiary text, and a role description."""
    out: list[dict] = []
    # Locate the §11 <h2> header (skip past HTML comments that contain §11).
    # Match: <h2>...§11... and start scope from there.
    h2_match = re.search(r'<h2[^>]*>[^<]{0,40}§11(?!\.5)[^<]*</h2>', text)
    if not h2_match:
        h2_match = re.search(r'<h2[^>]*>[^<]{0,40}關聯個股[^<]*</h2>', text)
    if not h2_match:
        return out
    sec_start = h2_match.end()
    sec_text = text[sec_start:sec_start + 60000]
    # Cut at the next <h2> (e.g. §11.5 or §12)
    nxt = re.search(r'<h2', sec_text)
    if nxt:
        sec_text = sec_text[: nxt.start()]

    seen = set()
    for row in re.split(r'</tr>', sec_text):
        if "tier-pill" not in row:
            continue  # skip header rows / non-ticker rows
        # Ticker: first <td>...</td>
        tm = re.search(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if not tm:
            continue
        ticker_raw = _strip_tags(tm.group(1))
        # Strip parenthetical descriptor: "AWE.L（Alphawave）" → "AWE.L"
        ticker = re.sub(r'[（(].*$', '', ticker_raw).strip()
        if not ticker or len(ticker) > 30:
            continue
        # Tier color
        cm = re.search(r'tier-(red|yellow|green)', row)
        if not cm:
            continue
        depth = TIER_COLOR_TO_EMOJI[cm.group(1)]
        # Beneficiary: "受益" present AND "受害" absent
        full = _strip_tags(row)
        beneficiary = ("受益" in full) and not (
            "受害" in full and full.find("受害") < full.find("受益")
        )
        # Role: pick first non-empty <td> cell after the depth pill
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        role = ""
        for c in cells[2:]:
            c_clean = _strip_tags(c)
            if c_clean and len(c_clean) > 4:
                role = c_clean[:80]
                break
        if not role:
            role = "—"
        if ticker in seen:
            continue
        seen.add(ticker)
        out.append({
            "ticker": ticker,
            "role": role,
            "depth": depth,
            "beneficiary": beneficiary,
        })
    return out


def harvest_oneliner(text: str, theme: str) -> str:
    """Pull a one-line summary from §0 / §1 / first <p> after <h2>."""
    # Try §0 first
    for marker in ("§0", "§1", "Industry DD overview"):
        idx = text.find(marker)
        if idx < 0:
            continue
        scope = text[idx:idx + 4000]
        # First <p> after the marker
        m = re.search(r'<p[^>]*>(.*?)</p>', scope, re.DOTALL)
        if m:
            inner = _strip_tags(m.group(1))
            if len(inner) > 30:
                return _trim_oneliner(inner)
    return _trim_oneliner(f"{theme} 產業深度報告（自動 backfill — 未填寫詳細 oneliner，待手動補完）")


def build_id_meta(text: str, fname: str) -> dict:
    tags = harvest_meta_tags(text)
    theme = tags.get("theme")
    if not theme:
        m = THEME_FROM_FILENAME_RE.match(fname)
        theme = m.group(1) if m else "未知主題"

    related = harvest_related_tickers(text)
    oneliner = harvest_oneliner(text, theme)

    meta: dict = {
        "theme": theme,
        "skill_version": tags.get("skill_version", "v1.0"),
        "id_version": tags.get("id_version", "v1.0"),
        "publish_date": tags.get("publish_date", "1970-01-01"),
        "thesis_type": "structural",  # default; user can patch
        "ai_exposure": "🟡",  # neutral default
        "oneliner": oneliner,
        "related_tickers": related,
    }
    if "sections_refreshed" in tags:
        meta["sections_refreshed"] = tags["sections_refreshed"]
    return meta


def inject_into_html(text: str, meta: dict, force: bool = False):
    """Insert <script id="id-meta"> block after <title>. Returns (new_text, ok)."""
    if ID_META_RE.search(text) and not force:
        return text, False
    block = (
        '\n<script id="id-meta" type="application/json">\n'
        + json.dumps(meta, ensure_ascii=False, indent=2)
        + '\n</script>'
    )
    if force and ID_META_RE.search(text):
        return ID_META_RE.sub(block.strip(), text, count=1), True
    new_text = INSERT_AFTER_RE.sub(lambda m: m.group(1) + block, text, count=1)
    if new_text == text:
        return text, False
    return new_text, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = ID_DIR / p.name
        targets = [p]
    else:
        targets = sorted(ID_DIR.glob("ID_*.html"))

    backfilled = 0
    skipped = 0
    failed = []
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="ignore")
        # Skip geopolitics IDs — they share ID_*.html naming but are produced by
        # geopolitics-dd skill (different schema). Will need their own meta block
        # eventually, but not part of this industry-analyst plan A.
        skill_v_m = re.search(
            r'<meta\s+name="id-skill-version"\s+content="([^"]+)"', text, re.IGNORECASE
        )
        if skill_v_m and "geopolitics" in skill_v_m.group(1):
            skipped += 1
            continue
        if ID_META_RE.search(text) and not args.force:
            skipped += 1
            continue
        meta = build_id_meta(text, path.name)
        new_text, ok = inject_into_html(text, meta, force=args.force)
        if not ok:
            failed.append((path.name, "no <title> anchor"))
            continue
        if not args.dry_run:
            path.write_text(new_text, encoding="utf-8")
        action = "DRY-RUN" if args.dry_run else "wrote"
        print(f"  + {path.name:48s} ({meta['theme'][:30]:30s}) {action} | {len(meta['related_tickers'])} tickers")
        backfilled += 1

    print()
    print(f"Backfilled       : {backfilled}")
    print(f"Already present  : {skipped}")
    if failed:
        print(f"Failed           : {len(failed)}")
        for fname, reason in failed:
            print(f"  - {fname}: {reason}")


if __name__ == "__main__":
    main()
