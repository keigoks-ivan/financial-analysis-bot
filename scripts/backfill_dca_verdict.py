#!/usr/bin/env python3
"""
backfill_dca_verdict.py

Surface-only retrofit for DCA HTML reports:
  1. Injects <!-- dca-verdict: {verdict} --> into HTML <head>
  2. Appends 5th cell to status-bar (if present)
  3. Injects verdict chip + subtitle after §7 section header

Idempotent — safe to re-run; skips files where injection already exists.

Output:
  - scripts/dca_verdict_manifest.json
  - Modified docs/dca/DCA_*.html files
"""

import glob
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
DCA_DIR = REPO / "docs" / "dca"
MANIFEST_PATH = Path(__file__).parent / "dca_verdict_manifest.json"

# Color map for verdict
VERDICT_COLOR = {
    "進場": "#166534",
    "觀望": "#92400E",
    "迴避": "#991B1B",
}

VERDICT_BG_COLOR = {
    "進場": "#F0FDF4",
    "觀望": "#FEF9C3",
    "迴避": "#FFF1F2",
}


# ─────────────────────────────────────────────
# 1. Verdict Classification
# ─────────────────────────────────────────────

# Keyword → verdict mapping (longest match first)
# IMPORTANT: Only match in emphasized text (strong/h2/h3/decision-box).
# Do NOT match "清倉" or "加碼" in plain text — they appear in every §7b table row.
# Do NOT match plain "進場" — too common; only match it in emphasis context.
KEYWORDS_EMPHASIS_ONLY = [
    ("觀望偏迴避", "觀望"),
    ("觀望偏進場", "觀望"),
    ("迴避", "迴避"),
    ("不買", "迴避"),
    ("退出持倉", "迴避"),
    ("不進場", "迴避"),
    ("觀望", "觀望"),
    ("建倉", "進場"),
    ("進場", "進場"),
]

# These only match in plain §7 text (must NOT appear in td/th table cells)
KEYWORDS_PLAIN_STRICT = [
    # None — too risky without emphasis context
]


def find_section7_text(html: str) -> str:
    """Extract the §7 section text (up to next major section or 8KB)."""
    # Find the §7 anchor
    anchors = [
        r'§7',
        r'section-7',
        r'id=["\']7["\']',
        r'Decision',
    ]
    start = -1
    for pat in anchors:
        m = re.search(pat, html)
        if m:
            start = m.start()
            break

    if start == -1:
        return ""

    # Return a window of up to 8KB after the anchor
    return html[start: start + 8000]


def extract_emphasized_text(segment: str) -> str:
    """Extract text from emphasis tags (strong, h3, h2, decision-box classes)."""
    emphasized = []
    # h2/h3 content
    for tag in ["h2", "h3", "strong", "b"]:
        for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", segment, re.DOTALL):
            emphasized.append(re.sub(r"<[^>]+>", "", m.group(1)))
    # class containing "decision" or "verdict"
    for m in re.finditer(r'class="[^"]*(?:decision|verdict)[^"]*"[^>]*>(.*?)</div>', segment, re.DOTALL):
        emphasized.append(re.sub(r"<[^>]+>", "", m.group(1)))
    return " ".join(emphasized)


def classify_from_explicit_label(html: str) -> tuple:
    """
    Primary: search for explicit "DCA 決策：{verdict}" label (v1.1+ pattern)
    or "裁決：{text}" pattern in §7 region.
    Returns (verdict, subtitle, confidence, source) or (None, None, 0, None).
    """
    section7 = find_section7_text(html)
    plain7 = re.sub(r"<[^>]+>", "", section7) if section7 else ""

    # Pattern 1: "DCA 決策：進場/觀望/迴避" — direct 3-char verdict
    m = re.search(r"DCA\s*決策[：:\s]+\s*(進場|觀望|迴避)", plain7)
    if m:
        verdict = m.group(1)
        subtitle = extract_subtitle(section7, verdict)
        return verdict, subtitle, 0.95, f"explicit 'DCA 決策：{verdict}' label"

    # Pattern 2: "裁決：{text}" — need to infer verdict from sentence content
    m = re.search(r"裁決[：:\s]+([^。\n<]{5,120})", plain7)
    if m:
        text = m.group(1)
        # 迴避: only if explicit 迴避 keyword OR ("不進場" WITHOUT 等待/回測/觀察 context)
        is_hard_avoid = any(kw in text for kw in ["迴避", "不買", "永久迴避", "X 迴避"])
        is_soft_avoid = ("不進場" in text and not any(kw in text for kw in ["觀察池", "等", "暫"]))
        if is_hard_avoid or is_soft_avoid:
            subtitle = text[:60]
            return "迴避", subtitle, 0.85, f"裁決 text → 迴避: {text[:50]}"
        # 觀望: "等待", "觀察池", "不進場+等" context, "觀望", "條件式", "Wait"
        if any(kw in text for kw in ["觀望偏迴避", "等待", "觀察池", "暫不", "等回", "等估值", "Wait", "觀望", "條件式", "動能冷卻", "等price", "不進"]):
            subtitle = text[:60]
            return "觀望", subtitle, 0.85, f"裁決 text → 觀望: {text[:50]}"
        if any(kw in text for kw in ["進場", "建倉", "滿格", "加碼", "核心持倉", "強勢", "試倉"]):
            # Extra check: if also contains "禁止" near entry words → 觀望
            if any(veto in text for veto in ["禁止", "不進", "等回", "等待"]):
                subtitle = text[:60]
                return "觀望", subtitle, 0.80, f"裁決 text → 觀望 (進場 vetoed): {text[:50]}"
            subtitle = text[:60]
            return "進場", subtitle, 0.85, f"裁決 text → 進場: {text[:50]}"

    # Pattern 3: look for the verdict-tag div / decision-card verdict-tag in §7 area
    # e.g. <div class="verdict-tag">WAIT & SCALE-IN</div>
    m = re.search(r'class="verdict-tag"[^>]*>([^<]{3,40})<', section7 or "")
    if m:
        text = m.group(1).strip()
        if any(kw in text for kw in ["WAIT", "觀望", "HOLD", "SCALE"]):
            return "觀望", text[:60], 0.85, f"verdict-tag: {text}"
        if any(kw in text for kw in ["AVOID", "迴避"]):
            return "迴避", text[:60], 0.85, f"verdict-tag: {text}"
        if any(kw in text for kw in ["BUY", "進場", "GO", "ENTER"]):
            return "進場", text[:60], 0.85, f"verdict-tag: {text}"

    return None, None, 0, None


def classify_from_keywords(html: str) -> tuple:
    """
    Secondary: keyword search in §7 region.
    Only uses unambiguous keywords in emphasized context.
    Returns (verdict, subtitle, confidence, source) or (None, None, 0, None).
    """
    section7 = find_section7_text(html)
    if not section7:
        return None, None, 0, None

    emphasized = extract_emphasized_text(section7)

    # Only 觀望/迴避 as emphasis matches — 進場/建倉 too ambiguous in emphasis
    safe_emphasis = {
        "觀望偏迴避": "觀望",
        "觀望偏進場": "觀望",
        "迴避": "迴避",
        "不買": "迴避",
        "退出持倉": "迴避",
        "不進場": "迴避",
        "觀望": "觀望",
    }
    for keyword, verdict in safe_emphasis.items():
        if keyword in emphasized:
            # Sanity: don't match "觀望" if "建倉" also appears (conflicting signals)
            if keyword == "觀望" and "建倉" in emphasized and "禁止" not in emphasized:
                continue  # ambiguous
            subtitle = extract_subtitle(section7, verdict)
            return verdict, subtitle, 0.80, f"keyword '{keyword}' in §7 emphasis (safe)"

    return None, None, 0, None


def extract_subtitle(section7: str, verdict: str) -> str:
    """Try to extract a short subtitle sentence."""
    plain = re.sub(r"<[^>]+>", "", section7)
    # For 觀望: find sentence with 等/觸發
    if verdict == "觀望":
        for pat in [r"等[^。；\n]{5,50}", r"觸發條件[^。；\n]{5,50}", r"等待[^。；\n]{5,50}"]:
            m = re.search(pat, plain)
            if m:
                return m.group(0)[:60].strip()
    # For 迴避: find sentence about thesis/護城河/估值
    if verdict == "迴避":
        for pat in [r"thesis[^。；\n]{5,50}", r"護城河[^。；\n]{5,50}", r"估值[^。；\n]{5,50}", r"不進場[^。；\n]{5,50}"]:
            m = re.search(pat, plain)
            if m:
                return m.group(0)[:60].strip()
    return ""


def classify_from_matrix(html: str) -> tuple:
    """
    Derive verdict from decision matrix signals embedded in HTML.
    Returns (verdict, subtitle, confidence, source).
    """
    signals = {}

    # DD signal lamp: look for status-bar first cell value or text near "訊號燈"
    m = re.search(r"訊號燈.*?<[^>]+class[^>]*val[^>]*>([ABCX+]+)", html, re.DOTALL)
    if m:
        signals["dd_signal"] = m.group(1).strip()
    else:
        # Try status-bar first .cell .val
        sb_match = re.search(r'class="status-bar".*?class="(?:cell|lbl)".*?class="(?:val|value)"[^>]*>([ABCX+]+)', html, re.DOTALL)
        if sb_match:
            signals["dd_signal"] = sb_match.group(1).strip()
        else:
            # Try text like "訊號燈：A" or "A+（訊號燈）"
            m2 = re.search(r"訊號燈[：:「\s]*([ABCX+]+)", html)
            if m2:
                signals["dd_signal"] = m2.group(1).strip()

    # Pure MA support: look in §7c table
    section7 = find_section7_text(html)
    if section7:
        plain7 = re.sub(r"<[^>]+>", "", section7)
        if re.search(r"Pure\s*MA[^❌✅]{0,30}❌", plain7):
            signals["pure_ma"] = False
        elif re.search(r"Pure\s*MA[^❌✅]{0,30}✅", plain7):
            signals["pure_ma"] = True

        # RSI overheating
        if re.search(r"RSI[^\n]{0,20}(?:70|75|80|過熱)", plain7) or re.search(r"動能過熱|漂移.*\+10%", plain7):
            signals["momentum_hot"] = True

        # 初始建倉 = 0%
        if re.search(r"初始建倉[倉位]?\s*[|｜]\s*0%|初始倉位.*0%", plain7):
            signals["initial_pos_zero"] = True

    # Moat trend from head marker or status bar
    m = re.search(r"dca-moat-trend:\s*([↑→↓])", html)
    if m:
        arrow = m.group(1)
        signals["moat_trend"] = arrow

    # Moat grade (S/A/B/C) from status bar 2nd cell or text
    moat_match = re.search(r"Moat.*?([SABC])\s*[<↑→↓]", html, re.DOTALL)
    if moat_match:
        signals["moat_grade"] = moat_match.group(1)

    # Runway from status bar 3rd cell
    runway_match = re.search(r"Runway.*?(🟢|🟡|🔴)", html, re.DOTALL)
    if runway_match:
        signals["runway"] = runway_match.group(1)

    # Estimate light: look for 估值 near emoji
    val_match = re.search(r"估值.*?(🟢|🟡|🟠|🔴)", html, re.DOTALL)
    if val_match:
        signals["valuation"] = val_match.group(1)

    # Apply decision matrix (priority 1-10)
    dd = signals.get("dd_signal", "")
    moat_trend = signals.get("moat_trend", "")
    moat_grade = signals.get("moat_grade", "")
    pure_ma = signals.get("pure_ma", None)
    runway = signals.get("runway", "")
    valuation = signals.get("valuation", "")
    momentum_hot = signals.get("momentum_hot", False)
    initial_zero = signals.get("initial_pos_zero", False)

    # Priority 1: DD signal = X
    if dd == "X":
        return "迴避", "DD 訊號燈 X（結構性不持有）", 0.6, "matrix-P1: dd=X"

    # Priority 3: moat_trend ↓ and moat ≤ B
    moat_low = moat_grade in ("B", "C", "")
    if moat_trend == "↓" and moat_low:
        return "迴避", "護城河下滑且等級偏低", 0.6, "matrix-P3: moat↓ + grade≤B"

    # Priority 4: Pure MA ❌
    if pure_ma is False:
        # If initial position 0% → likely already 觀望
        subtitle = "等 MA 信號確認後再評估"
        return "觀望", subtitle, 0.6, "matrix-P4: Pure MA ❌"

    # Priority 5: momentum overheating
    if momentum_hot:
        return "觀望", "動能過熱，等回測後條件式進場", 0.6, "matrix-P5: momentum hot"

    # Priority 6: DD = C
    if dd == "C":
        return "觀望", "DD 訊號燈 C（等評級提升）", 0.6, "matrix-P6: dd=C"

    # Priority 7: runway 🔴
    if runway == "🔴":
        return "觀望", "Runway post-Y5 🔴，持有年限壓縮至 ≤ 3Y", 0.6, "matrix-P7: runway🔴"

    # Priority 8: DD≥B + valuation 🟠
    if dd in ("A+", "A", "B") and valuation == "🟠":
        return "觀望", "估值 🟠（略貴），等估值回落", 0.6, "matrix-P8: dd≥B + val🟠"

    # If initial position 0% without other signals → likely 觀望
    if initial_zero:
        return "觀望", "初始倉位 0%，等觸發條件", 0.5, "matrix-inferred: initial=0%"

    # Priority 9 & 10: baseline → 進場
    if dd in ("A+", "A", "B"):
        if valuation in ("🟢", "🟡", ""):
            return "進場", "", 0.6, "matrix-P9/10: dd≥B + val≤🟡"

    # Default fallback
    return "觀望", "", 0.4, "matrix-fallback: no strong signal"


def classify(html: str, filename: str) -> dict:
    """
    Main classification: explicit label → keyword emphasis → decision matrix → fallback.
    Returns dict with verdict, subtitle, confidence, source, signals.
    """
    # Priority 1: explicit "DCA 決策：X" or "裁決：X" label
    verdict, subtitle, confidence, source = classify_from_explicit_label(html)
    if verdict and confidence >= 0.80:
        return {
            "verdict": verdict,
            "subtitle": subtitle or "",
            "confidence": confidence,
            "source": source,
            "signals": {},
        }

    # Priority 2: safe keyword in emphasis
    kv, ks, kc, ksrc = classify_from_keywords(html)
    if kv and kc >= 0.75:
        # Override low-confidence explicit label if keyword is stronger
        if not verdict or kc > confidence:
            verdict, subtitle, confidence, source = kv, ks, kc, ksrc
        return {
            "verdict": verdict,
            "subtitle": subtitle or "",
            "confidence": confidence,
            "source": source,
            "signals": {},
        }

    # Priority 3: decision matrix from signals
    mv, ms, mc, msrc = classify_from_matrix(html)
    if mv and mc >= 0.55:
        # Use existing label if confidence is comparable
        if verdict and confidence >= mc:
            pass  # keep existing
        else:
            verdict, subtitle, confidence, source = mv, ms, mc, msrc

    if not verdict:
        # Pure fallback for files with zero signals
        verdict = "觀望"
        confidence = 0.3
        source = "fallback: no signals found"
        subtitle = ""

    return {
        "verdict": verdict,
        "subtitle": subtitle or "",
        "confidence": confidence,
        "source": source,
        "signals": {},
    }


# ─────────────────────────────────────────────
# 2. Injection Logic (idempotent)
# ─────────────────────────────────────────────

def inject_head_marker(html: str, verdict: str) -> tuple[str, bool]:
    """Inject <!-- dca-verdict: {verdict} --> after dca-moat-trend."""
    if "<!-- dca-verdict:" in html:
        return html, False  # already exists

    # Try to insert after dca-moat-trend line
    moat_pattern = r"(<!-- dca-moat-trend:.*?-->)"
    if re.search(moat_pattern, html):
        replacement = r"\1\n<!-- dca-verdict: " + verdict + " -->"
        new_html = re.sub(moat_pattern, replacement, html, count=1)
        return new_html, True

    # Fallback: insert after <head>
    head_pattern = r"(<head[^>]*>)"
    if re.search(head_pattern, html, re.IGNORECASE):
        replacement = r"\1\n<!-- dca-verdict: " + verdict + " -->"
        new_html = re.sub(head_pattern, replacement, html, count=1, flags=re.IGNORECASE)
        return new_html, True

    return html, False


def inject_status_bar_cell(html: str, verdict: str) -> tuple[str, bool]:
    """
    Append 5th cell to status-bar if present and doesn't already have 5+ cells.
    """
    # Check status-bar exists
    if 'class="status-bar"' not in html and "class='status-bar'" not in html:
        return html, False  # No status bar → skip, mark as partial

    # Check if verdict cell already exists
    if "DCA 裁決" in html:
        return html, False  # Already injected

    color = VERDICT_COLOR.get(verdict, "#64748B")
    new_cell = (
        f'\n    <div class="cell">'
        f'<div class="lbl">DCA 裁決</div>'
        f'<div class="val" style="color:{color};font-size:20px">{verdict}</div>'
        f'</div>'
    )

    # Find the closing of status-bar div
    # Pattern: find </div> that closes the status-bar
    # Strategy: find the status-bar opening, then find the matching </div>
    sb_match = re.search(r'<div\s+class="status-bar"', html)
    if not sb_match:
        sb_match = re.search(r"<div\s+class='status-bar'", html)
    if not sb_match:
        return html, False

    start = sb_match.start()
    # Find the closing </div> for the status-bar (depth tracking)
    depth = 0
    i = start
    end = -1
    while i < len(html):
        if html[i:i+4] == "<div":
            depth += 1
        elif html[i:i+6] == "</div>":
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1

    if end == -1:
        return html, False

    # Insert new cell before the closing </div>
    new_html = html[:end] + new_cell + "\n  " + html[end:]
    return new_html, True


def inject_verdict_chip(html: str, verdict: str, subtitle: str) -> tuple[str, bool]:
    """
    Inject verdict chip after §7 header, before §7a content.
    Idempotent check: skip if verdict-chip or decision-chip already present.
    """
    if 'verdict-chip' in html or 'decision-chip' in html:
        return html, False

    color = VERDICT_COLOR.get(verdict, "#64748B")
    bg = VERDICT_BG_COLOR.get(verdict, "#F8FAFC")

    chip_html = (
        f'\n<div class="verdict-chip" style="'
        f'display:inline-block;padding:6px 20px;border-radius:4px;'
        f'background:{color};color:#fff;font-size:18px;font-weight:700;'
        f'border-left:4px solid {color};margin-bottom:8px">'
        f'DCA 決策：{verdict}</div>'
    )
    if subtitle:
        chip_html += (
            f'\n<div class="verdict-subtitle" style="'
            f'font-size:13px;color:#475569;font-style:italic;'
            f'display:block;margin-bottom:16px">{subtitle}</div>'
        )

    # Find §7 section header — various patterns
    patterns = [
        r"(<h2[^>]*>(?:[^<]*§7[^<]*|[^<]*Decision[^<]*)</h2>)",
        r"(<!--\s*(?:§7|=+\s*§7)[^>]*-->)",
        r"(<h2[^>]*>\s*§7[^<]*</h2>)",
        r"(§7[^<]*Decision[^<]*</h2>)",
    ]

    for pat in patterns:
        m = re.search(pat, html, re.DOTALL)
        if m:
            # Insert chip right after the matched header
            insert_pos = m.end()
            new_html = html[:insert_pos] + chip_html + html[insert_pos:]
            return new_html, True

    # Fallback: find "§7" text anywhere and insert chip after its enclosing tag
    m = re.search(r"(§7[^\n<]{0,60})</", html)
    if m:
        insert_pos = m.end()
        new_html = html[:insert_pos] + chip_html + html[insert_pos:]
        return new_html, True

    return html, False


def inject_file(html: str, verdict: str, subtitle: str) -> tuple[str, str]:
    """
    Apply all 3 injections. Returns (new_html, status).
    status ∈ {'ok', 'partial', 'skipped'}
    """
    injected_anything = False
    has_sb = 'class="status-bar"' in html or "class='status-bar'" in html

    html, head_injected = inject_head_marker(html, verdict)
    if head_injected:
        injected_anything = True

    html, chip_injected = inject_verdict_chip(html, verdict, subtitle)
    if chip_injected:
        injected_anything = True

    html, sb_injected = inject_status_bar_cell(html, verdict)
    if has_sb and not sb_injected and "DCA 裁決" not in html:
        # Had status bar but injection failed
        status = "partial"
    elif not has_sb:
        status = "partial"  # No status bar → chip + head marker only
    elif injected_anything:
        status = "ok"
    else:
        status = "skipped"

    if not injected_anything:
        status = "skipped"

    return html, status


# ─────────────────────────────────────────────
# 3. Main
# ─────────────────────────────────────────────

def main():
    files = sorted(glob.glob(str(DCA_DIR / "DCA_*.html")))
    manifest = {}

    counts = {"進場": 0, "觀望": 0, "迴避": 0}
    status_counts = {"ok": 0, "partial": 0, "skipped": 0, "error": 0}

    for fpath in files:
        fname = Path(fpath).name
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                html = f.read()
        except Exception as e:
            print(f"[ERROR] {fname}: {e}", file=sys.stderr)
            manifest[fname] = {"error": str(e), "status": "error"}
            status_counts["error"] += 1
            continue

        # Classify
        result = classify(html, fname)
        verdict = result["verdict"]
        subtitle = result["subtitle"]

        # Inject
        try:
            new_html, status = inject_file(html, verdict, subtitle)
        except Exception as e:
            print(f"[ERROR inject] {fname}: {e}", file=sys.stderr)
            manifest[fname] = {**result, "status": "error", "inject_error": str(e)}
            status_counts["error"] += 1
            continue

        # Write only if changed
        if new_html != html:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)

        manifest[fname] = {**result, "status": status}
        counts[verdict] = counts.get(verdict, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    # Write manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"DCA Verdict Backfill Summary")
    print(f"{'='*60}")
    print(f"Total processed : {len(files)}")
    print(f"  進場           : {counts.get('進場', 0)}")
    print(f"  觀望           : {counts.get('觀望', 0)}")
    print(f"  迴避           : {counts.get('迴避', 0)}")
    print(f"Status breakdown:")
    print(f"  ok             : {status_counts['ok']}")
    print(f"  partial        : {status_counts['partial']}  (no status-bar or chip only)")
    print(f"  skipped        : {status_counts['skipped']}  (already injected)")
    print(f"  error          : {status_counts['error']}")
    print(f"\nManifest: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
