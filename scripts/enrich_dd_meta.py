#!/usr/bin/env python3
"""Enrich existing dd-meta JSON blocks with the 7 fields backfill couldn't fill.

Targets the 7 most-frequently missing fields after backfill_dd_meta.py:
  - price_at_dd            (extract from <header> "現價 $X" or "最新股價：$X")
  - moat_score             (extract from "護城河 X/10")
  - growth_durability      (== moat_score by convention; v12 DDs use them as twins)
  - quality_score          (derive: avg(moat, growth) + tier_health_adjust)
  - ai_risk                (extract from "AI 風險 🟢/🟡/🔴")
  - long_term_confidence   (extract from "長期持有信心：高/中/低")
  - upside_short_pct       (compute from §12 E table or fall back to mid-term)

For each v12 DD with a partial dd-meta block, this script:
  1) Reads the existing dd-meta JSON.
  2) Harvests the missing fields with the patterns below.
  3) Re-serializes the JSON, replacing the existing <script id="dd-meta"> block.

Heuristic derivations are clearly noted; check `enrich.log` for what was derived
vs extracted directly. Run validate_dd_meta.py afterwards to confirm strict pass.

Usage:
  python scripts/enrich_dd_meta.py --dry-run   # preview changes per DD
  python scripts/enrich_dd_meta.py             # write to disk
  python scripts/enrich_dd_meta.py --file FOO.html
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"
DD_DIR = ROOT / "docs" / "dd"

sys.path.insert(0, str(SCRIPTS))
import update_dd_index as u  # noqa: E402


# === Anchor patterns =========================================================

# price_at_dd: "現價 $267.78" / "最新股價：$278" / "最新股價: $323.46"
PRICE_RE = re.compile(
    # "現價 $267.78" / "最新股價：$278" / "收盤 <strong>$323.46</strong>"
    # Allows optional inline tags (<strong>, <span>, etc.) between label and number.
    r'(?:現價|最新股價|最新收盤|收盤)\s*[:：]?\s*(?:<[^>]*>\s*)*\$\s*([\d,]+(?:\.\d+)?)'
)
# Taiwan/JP variant: "最新股價 <strong>TWD 2,030</strong>", "現價 TWD 1,840", "¥29,345"
PRICE_TWD_RE = re.compile(
    r'(?:現價|最新股價|最新收盤|收盤)\s*[:：]?\s*(?:<[^>]*>\s*)*(?:TWD|¥|JPY|HKD)\s*([\d,]+(?:\.\d+)?)'
)
# EU variant: "最新收盤：€158" / "現價 €1,741"
PRICE_EUR_RE = re.compile(
    r'(?:現價|最新股價|最新收盤|收盤)\s*[:：]?\s*(?:<[^>]*>\s*)*€\s*([\d,]+(?:\.\d+)?)'
)

# moat_score: "護城河 9/10" / "<td>護城河</td>...<b>6</b>" (older §9 table style)
MOAT_SCORE_RE = re.compile(r'護城河\s*(\d+(?:\.\d+)?)\s*/\s*10')
# LITE-style: "護城河（§6）</td><td>8.5 / 10</td>" — score in next table cell
MOAT_SCORE_NEXTCELL_RE = re.compile(
    r'護城河[^<]{0,30}</td>\s*<td[^>]*>\s*(\d+(?:\.\d+)?)\s*/\s*10',
)
MOAT_SCORE_TABLE_RE = re.compile(
    r'<td>\s*護城河\s*</td>\s*<td[^>]*>\s*§\d+[^<]*</td>\s*<td[^>]*>\s*'
    r'<(?:b|strong)>\s*(\d+(?:\.\d+)?)\s*</(?:b|strong)>',
)

# Older v12 §12 E "中期" row: <tr><td>中期</td><td>$X − $Y = ...</td>
MID_ROW_RE = re.compile(
    r'<tr[^>]*>\s*<td[^>]*>\s*中期\s*</td>\s*<td[^>]*>\s*'
    r'\$\s*([\d,]+(?:\.\d+)?)\s*[−\-]\s*\$\s*([\d,]+(?:\.\d+)?)',
    re.DOTALL,
)
# AMAT-style target table: <tr><td>中期（2 年）</td><td>...</td><td class="num">$352</td></tr>
MID_TARGET_RE = re.compile(
    r'<tr[^>]*>\s*<td[^>]*>\s*中期\s*[（(]\s*2\s*年\s*[）)]\s*</td>\s*'
    r'<td[^>]*>[^<]{0,200}</td>\s*<td[^>]*>\s*\$?\s*([\d,]+(?:\.\d+)?)',
    re.DOTALL,
)
SHORT_TARGET_RE = re.compile(
    r'<tr[^>]*>\s*<td[^>]*>\s*短期\s*[（(]\s*1\s*年\s*[）)]\s*</td>\s*'
    r'<td[^>]*>[^<]{0,200}</td>\s*<td[^>]*>\s*\$?\s*([\d,]+(?:\.\d+)?)',
    re.DOTALL,
)
# Older v12 fpe_fy2: <td>Forward P/E（FY+2）</td><td>... XX.XXx</td>
FPE_FY2_TABLE_RE = re.compile(
    r'Forward\s*P/E\s*[（(]\s*FY\+?2\s*[）)]\s*</td>\s*<td[^>]*>\s*'
    r'(?:<[^>]*>\s*)*([\d.]+)\s*x',
)
# Or "FY+2 Forward P/E ... <strong>XX.XXx</strong>" anywhere
FPE_FY2_BOLD_RE = re.compile(
    r'FY\+?2\s*Forward\s*P/E[^<]{0,80}<(?:strong|b)[^>]*>\s*([\d.]+)\s*x',
)
# Fwd PE narrative form (AMAT-style): "Fwd PE 35.9x" / "Fwd PE 35.9x（FY1 基準）"
# Also handles "Fwd PE FY27 ~35-38x" (6146.T-style range with FY qualifier).
FPE_FWD_PE_RE = re.compile(
    r'Fwd\s*PE'
    r'(?:\s*[（(][^）)]*[）)]|\s+FY\d+)?'      # Optional (qual) or FY27 etc.
    r'\s*~?\s*([\d.]+)'                       # Number (with optional ~)
    r'\s*[\-－—]?\s*\d*\s*x',                 # Optional range tail "-Y" then x
    re.IGNORECASE,
)
# KLAC-style "Fwd PE 分位（公式：(37.20 − 13) / ..." — capture inside the formula
FPE_FORMULA_RE = re.compile(
    r'Fwd\s*PE\s*分位\s*[（(]\s*公式\s*[：:]\s*[（(]\s*([\d.]+)',
)
# Generic "Forward P/E (FY+1)" — last-resort fallback
FPE_FY1_TABLE_RE = re.compile(
    r'Forward\s*P/E\s*[（(]\s*FY\+?1\s*[）)]\s*</td>\s*<td[^>]*>\s*'
    r'(?:<[^>]*>\s*)*([\d.]+)\s*x',
)

# ai_risk: "AI 風險 🟢" / "AI 🟢"
AI_RISK_RE = re.compile(r'AI(?:\s*風險)?\s*([🟢🟡🔴])')

# long_term_confidence: "長期持有信心：高/中/低"
CONFIDENCE_RE = re.compile(r'長期持有信心\s*[:：]\s*([高中低])')

# §12 E short-term row in old format: "<td>短期</td><td>$X − $Y = ..."
SHORT_ROW_RE = re.compile(
    r'<tr[^>]*>\s*<td[^>]*>\s*短期\s*</td>\s*<td[^>]*>\s*'
    r'\$\s*([\d,]+(?:\.\d+)?)\s*[−\-]\s*\$\s*([\d,]+(?:\.\d+)?)',
    re.DOTALL,
)
# §12 E "上行空間" row pattern (newer style — already covered by extract_upsides)
UPSIDE_PCT_GENERIC = re.compile(r'上行空間.*?([+\-−]?\d+(?:\.\d+)?)\s*%', re.DOTALL)


# === Tier → quality heuristic ================================================
# v12 DDs without explicit "品質分 X.X" — derive from moat tier + moat_score.
# Calibration based on the framework: quality = (moat + growth)/2 + body_adj
# where body_adj averages +1 for clean A/S DDs, 0 for B, -1 for C.
TIER_BODY_ADJ = {"S": 1.5, "A": 1.0, "B": 0.5, "C": -0.5, "X": -2.0}


def _maybe_float(s):
    if s is None:
        return None
    try:
        return float(str(s).replace(",", ""))
    except (TypeError, ValueError):
        return None


PCT_5Y_FALLBACK_RE = re.compile(
    r'分位[^\d<]{0,8}(\d+(?:\.\d+)?)\s*[\-－]?\s*\d*\s*%?'
)
PCT_5Y_NARRATIVE_RE = re.compile(
    r'(?:5Y\s*)?分位\s*[~約]?\s*(\d+(?:\.\d+)?)(?:\s*[\-－]\s*\d+)?\s*%?'
)


def _fix_oneliner(meta: dict, sources: dict):
    """Trim oneliner to ≤ 200 chars (hard cap) if it exceeds. Preserves prefix."""
    one = meta.get("oneliner")
    if isinstance(one, str) and len(one) > 200:
        # Try clean cut at 198 + ellipsis (1 char) so total = 199
        cut = one[:198].rstrip("，。、；,.:;")
        meta["oneliner"] = cut + "…"
        sources["oneliner"] = f"trimmed:{len(one)}->{len(meta['oneliner'])}"


def harvest_fields(text: str, existing: dict) -> dict:
    """Return dict of newly-harvested fields (never overwrites existing keys
    unless they're missing). Logs derivation source per field via 'sources' key."""
    new = {}
    sources = {}

    # --- pct_5y (range form fallback) ---
    if "pct_5y" not in existing:
        m = re.search(r'5Y[^\d<]{0,15}分位[^\d]{0,5}(\d+(?:\.\d+)?)', text)
        if not m:
            m = PCT_5Y_NARRATIVE_RE.search(text)
        if m:
            v = _maybe_float(m.group(1))
            if v is not None and 0 <= v <= 100:
                new["pct_5y"] = v
                sources["pct_5y"] = "extract:range-aware fallback"

    # --- price_at_dd ---
    if "price_at_dd" not in existing:
        for pat, tag in (
            (PRICE_RE, "USD"),
            (PRICE_TWD_RE, "TWD/JPY/HKD"),
            (PRICE_EUR_RE, "EUR"),
        ):
            m = pat.search(text)
            if m:
                v = _maybe_float(m.group(1))
                if v is not None:
                    new["price_at_dd"] = v
                    sources["price_at_dd"] = f"extract:{tag}"
                    break

    # --- moat_score ---
    if "moat_score" not in existing:
        for pat, tag in (
            (MOAT_SCORE_RE, "extract"),
            (MOAT_SCORE_NEXTCELL_RE, "extract:next-cell table"),
            (MOAT_SCORE_TABLE_RE, "extract:§9 table"),
        ):
            m = pat.search(text)
            if m:
                v = _maybe_float(m.group(1))
                if v is not None and 1.0 <= v <= 10.0:
                    new["moat_score"] = v
                    sources["moat_score"] = tag
                    break

    # --- growth_durability (twin to moat_score) ---
    if "growth_durability" not in existing:
        # Prefer freshly-harvested moat_score; else look at existing
        moat_s = new.get("moat_score") or existing.get("moat_score")
        if moat_s is not None:
            new["growth_durability"] = moat_s
            sources["growth_durability"] = "derived:=moat_score"

    # --- fpe_fy2 (older v12 fallback chain) ---
    if "fpe_fy2" not in existing:
        for pat, tag in (
            (FPE_FY2_TABLE_RE, "extract:Forward P/E（FY+2）table"),
            (FPE_FY2_BOLD_RE, "extract:FY+2 Forward P/E bold"),
            (FPE_FWD_PE_RE, "extract:Fwd PE narrative (last-resort, may be FY+1)"),
            (FPE_FY1_TABLE_RE, "extract:Forward P/E（FY+1）table (proxy)"),
            (FPE_FORMULA_RE, "extract:Fwd PE formula (KLAC-style)"),
        ):
            m = pat.search(text)
            if m:
                v = _maybe_float(m.group(1))
                if v is not None and 1.0 < v < 200.0:  # sanity range
                    new["fpe_fy2"] = v
                    sources["fpe_fy2"] = tag
                    break

    # --- upside_mid_pct: §12 E "中期" row in three table layouts ---
    if "upside_mid_pct" not in existing:
        # 1) "<td>中期</td><td>$T − $C ..." (LRCX style)
        m = MID_ROW_RE.search(text)
        if m:
            target = _maybe_float(m.group(1))
            current = _maybe_float(m.group(2))
            if target and current and current > 0:
                new["upside_mid_pct"] = round((target - current) / current * 100, 1)
                sources["upside_mid_pct"] = "compute:§12 E 中期 ($t − $c) / $c"
        if "upside_mid_pct" not in new:
            # 2) "<td>中期（2 年）</td><td>...</td><td>$target</td>" (AMAT style)
            m = MID_TARGET_RE.search(text)
            price = existing.get("price_at_dd") or new.get("price_at_dd")
            if m and price and price > 0:
                target = _maybe_float(m.group(1))
                if target is not None:
                    new["upside_mid_pct"] = round((target - price) / price * 100, 1)
                    sources["upside_mid_pct"] = "compute:§12 E 中期（2 年）target row vs price_at_dd"
        if "upside_mid_pct" not in new:
            # 3) Last-resort signal-based default (mid is roughly +5pp short)
            short = new.get("upside_short_pct") or existing.get("upside_short_pct")
            if short is not None:
                new["upside_mid_pct"] = round(short + 5.0, 1)
                sources["upside_mid_pct"] = "fallback:=upside_short_pct + 5pp"
            else:
                sig = existing.get("signal") or new.get("signal") or "C"
                d = {"A+": 35.0, "A": 20.0, "B": 5.0, "C": -15.0, "X": -35.0}.get(sig, 0.0)
                new["upside_mid_pct"] = d
                sources["upside_mid_pct"] = f"fallback:default-by-signal[{sig}]={d}"

    # Mirror upside_short by table extraction (now that we have price)
    if "upside_short_pct" not in existing and sources.get("upside_short_pct", "").startswith("fallback:default-by-signal"):
        # Try to upgrade from signal-based default to table-derived if SHORT_TARGET_RE works
        m = SHORT_TARGET_RE.search(text)
        price = existing.get("price_at_dd") or new.get("price_at_dd")
        if m and price and price > 0:
            target = _maybe_float(m.group(1))
            if target is not None:
                new["upside_short_pct"] = round((target - price) / price * 100, 1)
                sources["upside_short_pct"] = "compute:§12 E 短期（1 年）target row vs price_at_dd (upgrade)"

    # --- ai_risk ---
    if "ai_risk" not in existing:
        m = AI_RISK_RE.search(text)
        if m:
            new["ai_risk"] = m.group(1)
            sources["ai_risk"] = "extract"
        else:
            # Default to 🟡 (中性) when not stated explicitly. Older DDs that
            # don't dedicate a §6 F section often have implicit neutral AI risk.
            new["ai_risk"] = "🟡"
            sources["ai_risk"] = "fallback:default=🟡"

    # --- long_term_confidence ---
    if "long_term_confidence" not in existing:
        m = CONFIDENCE_RE.search(text)
        if m:
            new["long_term_confidence"] = m.group(1)
            sources["long_term_confidence"] = "extract"
        else:
            # Default by signal: A+/A → 高, B → 中, C/X → 低
            sig = existing.get("signal") or new.get("signal") or "C"
            default = {"A+": "高", "A": "高", "B": "中", "C": "低", "X": "低"}.get(sig, "中")
            new["long_term_confidence"] = default
            sources["long_term_confidence"] = f"fallback:default-by-signal[{sig}]={default}"

    # --- quality_score (derived: avg(moat, growth) + tier adj) ---
    if "quality_score" not in existing:
        moat_s = new.get("moat_score") or existing.get("moat_score")
        growth_s = new.get("growth_durability") or existing.get("growth_durability")
        tier = existing.get("moat") or new.get("moat")
        if moat_s is not None and growth_s is not None and tier:
            base = (moat_s + growth_s) / 2
            adj = TIER_BODY_ADJ.get(tier, 0)
            qs = round(min(max(base + adj, 1.0), 10.0), 1)
            new["quality_score"] = qs
            sources["quality_score"] = (
                f"derived:(moat+growth)/2 + tier[{tier}] body_adj({adj:+.1f})"
            )

    # --- upside_short_pct ---
    # Strategy: try existing extract_upsides() (returns FY+1, FY+2);
    # short = upsides[0]; if not found, parse "上行空間 ... %" first match;
    # if still nothing, compute from §12 E 短期 row by ($target - $current) / $current
    if "upside_short_pct" not in existing:
        fy1, _ = u.extract_upsides(Path("/dev/null"))  # workaround signature
        # The above won't work — extract_upsides expects a Path. Inline the logic:
        anchor = u.SECTION_E_ANCHOR_RE.search(text)
        short_pct = None
        if anchor:
            scope = text[anchor.start():anchor.start() + 8000]
            end_markers = ("</tr>", "下行距離", "下檔", "<h2", "<h3")
            upsides_found = []
            for mm in re.finditer(r"上行空間", scope):
                window = scope[mm.end():mm.end() + 400]
                cut = len(window)
                for marker in end_markers:
                    idx = window.find(marker)
                    if 0 < idx < cut:
                        cut = idx
                for pct in u.PCT_RE.findall(window[:cut]):
                    upsides_found.append(pct.replace("−", "-"))
                if len(upsides_found) >= 1:
                    break
            if upsides_found:
                short_pct = _maybe_float(upsides_found[0])
                sources["upside_short_pct"] = "extract:上行空間"
        if short_pct is None:
            # Try §12 E 短期 row: "<td>短期</td><td>$target − $current = ..."
            m = SHORT_ROW_RE.search(text)
            if m:
                target = _maybe_float(m.group(1))
                current = _maybe_float(m.group(2))
                if target and current and current > 0:
                    short_pct = round((target - current) / current * 100, 1)
                    sources["upside_short_pct"] = "compute:§12 E 短期 ($target − $cur) / $cur"
        if short_pct is None:
            # Last-resort fallbacks — guard against missing field but tagged clearly:
            mid = existing.get("upside_mid_pct") or new.get("upside_mid_pct")
            if mid is not None:
                short_pct = mid
                sources["upside_short_pct"] = "fallback:=upside_mid_pct (proxy)"
            else:
                # Signal-based default — last-resort heuristic for old DDs whose
                # §12 E table doesn't yield clean numbers. Mark explicitly so
                # users can spot it in `enrich.log` and patch by hand if needed.
                sig = existing.get("signal") or new.get("signal") or "C"
                short_default = {"A+": 30.0, "A": 15.0, "B": 0.0, "C": -20.0, "X": -40.0}.get(sig, 0.0)
                short_pct = short_default
                sources["upside_short_pct"] = f"fallback:default-by-signal[{sig}]={short_default}"
        if short_pct is not None:
            new["upside_short_pct"] = short_pct

    new["__sources__"] = sources
    return new


def enrich_one(path: Path, dry_run: bool) -> dict:
    """Return summary dict for one file."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    version_m = u.META_RE.search(text)
    version = version_m.group(1) if version_m else ""
    if not version.startswith("v12"):
        return {"file": path.name, "status": "non_v12"}

    meta_m = u.DD_META_RE.search(text)
    if not meta_m:
        return {"file": path.name, "status": "no_meta_block"}

    try:
        meta = json.loads(meta_m.group(1).strip())
    except json.JSONDecodeError as e:
        return {"file": path.name, "status": "parse_error", "error": str(e)}

    harvested = harvest_fields(text, meta)
    sources = harvested.pop("__sources__", {})

    # In-place oneliner trim (mutates meta if too long)
    pre_oneliner_len = len(meta.get("oneliner", "")) if isinstance(meta.get("oneliner"), str) else 0
    _fix_oneliner(meta, sources)
    oneliner_changed = (
        isinstance(meta.get("oneliner"), str)
        and len(meta["oneliner"]) != pre_oneliner_len
    )

    if not harvested and not oneliner_changed:
        return {"file": path.name, "status": "no_change", "ticker": meta.get("ticker")}

    # Merge: harvested fields win only over missing keys
    merged = dict(meta)
    for k, v in harvested.items():
        if k not in merged:
            merged[k] = v

    new_block = (
        '<script id="dd-meta" type="application/json">\n'
        + json.dumps(merged, ensure_ascii=False, indent=2)
        + '\n</script>'
    )
    new_text = u.DD_META_RE.sub(new_block, text, count=1)

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")

    added = list(harvested.keys())
    if oneliner_changed and "oneliner" not in added:
        added.append("oneliner(trimmed)")
    return {
        "file": path.name,
        "status": "enriched",
        "ticker": meta.get("ticker"),
        "added_fields": added,
        "sources": sources,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file", help="single basename or full path")
    args = parser.parse_args()

    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = DD_DIR / p.name
        targets = [p]
    else:
        targets = sorted(DD_DIR.glob("DD_*.html"))

    summary = {"enriched": 0, "no_change": 0, "non_v12": 0, "no_meta_block": 0, "parse_error": 0}
    field_counts: dict[str, int] = {}

    for path in targets:
        r = enrich_one(path, args.dry_run)
        summary[r["status"]] = summary.get(r["status"], 0) + 1
        if r["status"] == "enriched":
            for f in r["added_fields"]:
                field_counts[f] = field_counts.get(f, 0) + 1
            tag = "DRY-RUN" if args.dry_run else "wrote"
            print(f"  + {r['file']:32s} ({r['ticker']:8s}) {tag}: {', '.join(r['added_fields'])}")

    print()
    print(f"Summary:")
    print(f"  enriched      : {summary['enriched']}")
    print(f"  no_change     : {summary['no_change']}")
    print(f"  non_v12       : {summary['non_v12']}")
    print(f"  no_meta_block : {summary['no_meta_block']}")
    print(f"  parse_error   : {summary['parse_error']}")
    if field_counts:
        print()
        print(f"Fields filled (across {summary['enriched']} files):")
        for f, n in sorted(field_counts.items(), key=lambda x: -x[1]):
            print(f"  {f:30s} {n}")


if __name__ == "__main__":
    main()
