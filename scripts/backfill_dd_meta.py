#!/usr/bin/env python3
"""Backfill <script id="dd-meta"> JSON block into legacy v12 DDs.

For each v12 DD without a dd-meta block, harvest fields via:
  1) INDEX.md row (canonical for: ticker, date, schema, verdict, trap, triax)
  2) Existing regex extractors in update_dd_index.py
     (signal, fpe_fy2, pct_5y, peg_fy2, upside_*, stress)
Write a JSON block into <head>, after <title>.

Best-effort: required fields the script cannot confidently extract are
*omitted* (not nulled). The validator (scripts/validate_dd_meta.py) will
list per-file gaps so they can be patched manually before the strict gate
is enabled in CI.

Usage:
  python scripts/backfill_dd_meta.py --dry-run       # preview, no writes
  python scripts/backfill_dd_meta.py                 # write to disk
  python scripts/backfill_dd_meta.py --file FOO.html # one file only
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"
DD_DIR = ROOT / "docs" / "dd"

# Reuse the regex extractors from update_dd_index.py
sys.path.insert(0, str(SCRIPTS))
import update_dd_index as u  # noqa: E402

INSERT_AFTER_RE = re.compile(r'(<title>[^<]*</title>)')
TRAP_LABEL_MAP = {
    "🟢": "🟢 非陷阱",
    "🟡": "🟡 觀察期",
    "🔴": "🔴 高風險",
}


def _maybe_float(s):
    if not s:
        return None
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def build_meta(path: Path, md: dict, text: str) -> dict:
    """Best-effort dd-meta dict from INDEX.md row + DD HTML regex.

    Required fields the regex cannot extract reliably are OMITTED so the
    validator flags them per-file (rather than write a wrong placeholder).
    """
    moat, val_emoji, ma_state = u.parse_triax(md["rr_raw"])
    sig = u.extract_signal_light(text) or u._verdict_to_signal(md["verdict"])
    sp, st = u.extract_stress_v12(text)
    fpe = _maybe_float(u.extract_fpe_fy2(text))
    pct = _maybe_float(u.extract_5y_pct(text))
    peg = _maybe_float(u.extract_peg_v12(text))
    up_mid = _maybe_float(u.extract_upside_fy2(text, md.get("comment", "")))

    trap_emoji = (md["trap"] or "").strip()[:1] or ""
    trap_label = TRAP_LABEL_MAP.get(trap_emoji, md["trap"].strip() if md["trap"] else "")

    meta: dict = {
        "ticker": md["ticker"],
        "schema": md["schema"],
        "date": md["date"],
        "stress": {"pass": int(sp), "total": int(st)},
        "verdict": md["verdict"],
    }
    if sig:
        meta["signal"] = sig
    if trap_emoji:
        meta["trap"] = trap_emoji
    if trap_label:
        meta["trap_label"] = trap_label
    if moat:
        meta["moat"] = moat
    if val_emoji:
        meta["val"] = val_emoji
    if ma_state:
        meta["ma"] = ma_state
    if fpe is not None:
        meta["fpe_fy2"] = fpe
    if pct is not None:
        meta["pct_5y"] = pct
    if peg is not None:
        meta["peg_fy2"] = peg
    if up_mid is not None:
        meta["upside_mid_pct"] = up_mid
    # Capture INDEX.md comment as oneliner fallback (capped at hard limit)
    comment = (md.get("comment") or "").strip()
    if comment:
        # Strip <br> tags and limit length
        flat = re.sub(r"<br\s*/?>", "；", comment)
        flat = re.sub(r"<[^>]+>", "", flat).strip()
        if len(flat) > 200:
            flat = flat[:200].rstrip("，。、；,.:;") + "…"
        meta["oneliner"] = flat
    return meta


def inject_into_html(text: str, meta: dict):
    """Insert <script id="dd-meta"> block after <title>. Returns (new_text, ok).
    ok=False if a dd-meta block already exists or no <title> anchor found."""
    if u.DD_META_RE.search(text):
        return text, False
    block = (
        '\n<script id="dd-meta" type="application/json">\n'
        + json.dumps(meta, ensure_ascii=False, indent=2)
        + '\n</script>'
    )
    new_text = INSERT_AFTER_RE.sub(lambda m: m.group(1) + block, text, count=1)
    if new_text == text:
        return text, False
    return new_text, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Print actions but don't modify files."
    )
    parser.add_argument(
        "--file", help="Backfill a single file (basename or full path).",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-write dd-meta block even if one already exists (DESTRUCTIVE)."
    )
    args = parser.parse_args()

    index_data = u.parse_index_md()

    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = DD_DIR / p.name
        targets = [p]
    else:
        targets = sorted(DD_DIR.glob("DD_*.html"))

    backfilled = 0
    skipped_present = 0
    skipped_no_index = 0
    skipped_non_v12 = 0
    failed = []

    for path in targets:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            failed.append((path.name, f"read error: {e}"))
            continue
        version_m = u.META_RE.search(text)
        version = version_m.group(1) if version_m else ""
        if not version.startswith("v12"):
            skipped_non_v12 += 1
            continue
        if u.DD_META_RE.search(text) and not args.force:
            skipped_present += 1
            continue
        md = index_data.get(path.name)
        if not md or not md["schema"].startswith("v12"):
            skipped_no_index += 1
            failed.append((path.name, "no v12 INDEX.md row"))
            continue

        meta = build_meta(path, md, text)

        if args.force and u.DD_META_RE.search(text):
            # Replace existing block
            new_text = u.DD_META_RE.sub(
                '<script id="dd-meta" type="application/json">\n'
                + json.dumps(meta, ensure_ascii=False, indent=2)
                + '\n</script>',
                text,
                count=1,
            )
            ok = True
        else:
            new_text, ok = inject_into_html(text, meta)

        if not ok:
            failed.append((path.name, "no <title> anchor for insertion"))
            continue

        if not args.dry_run:
            path.write_text(new_text, encoding="utf-8")

        action = "DRY-RUN" if args.dry_run else "wrote"
        print(f"  + {path.name}: {len(meta)} fields ({action})")
        backfilled += 1

    print()
    print(f"Backfilled       : {backfilled}")
    print(f"Already present  : {skipped_present}")
    print(f"Non-v12 skipped  : {skipped_non_v12}")
    if failed:
        print(f"Failed / no-index: {len(failed)}")
        for fname, reason in failed:
            print(f"  - {fname}: {reason}")


if __name__ == "__main__":
    main()
