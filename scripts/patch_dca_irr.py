#!/usr/bin/env python3
"""One-shot patch: inject annualized IRR into the §4 機率加權期望值 cell of
each DCA report under docs/dca/.

Reads the existing 5Y % using the same extraction logic as
scripts/update_dd_index.py, computes IRR = (1 + r)^(1/5) - 1, and rewrites
the §4 期望值 <strong> cell to a canonical form:

    <strong>{原值} / IRR ≈ {±X.X}%/yr</strong>

Existing inline "年化 ~X%" or "（IRR ≈ ...）" snippets inside the cell are
stripped first so we don't stack tags across reruns.

Default mode is dry-run (prints proposed diffs).  Use --apply to write back.

Usage:
    python scripts/patch_dca_irr.py                  # dry-run all
    python scripts/patch_dca_irr.py --files KLAC NVDA 2330TW
    python scripts/patch_dca_irr.py --apply
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

# Reuse helpers from update_dd_index without re-implementing.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_dd_index import (  # noqa: E402
    DCA_DIR,
    DCA_FILENAME_RE,
    extract_dca_ev_5y,
)

ANCHORS = (
    "機率加權期望值",
    "機率加權 5 年期望值",
    "機率加權 5年期望值",
    "機率加權 EV（5Y）",
    "機率加權 EV (5Y)",
    "機率加權EV（5Y）",
    "機率加權EV(5Y)",
    "期望值（機率加權）",
    "期望值(機率加權)",
)

# Anchor must be in a table-cell context. We approve when the FIRST closing
# tag found matches `</td>` or `</th>`. Closes like `</p>`, `</h2>`, `</li>`
# disqualify the anchor (it's in narrative text, not a value cell).
_CELL_CLOSE_RE = re.compile(r"</(td|th|p|h[1-6]|li|div|section|tr|article)\b", re.IGNORECASE)
# Bound the value-strong search to the same row.
_TR_CLOSE_RE = re.compile(r"</tr\s*>", re.IGNORECASE)

# Stale IRR / 年化 fragments to strip from inside the value <strong>.
# Order matters: more specific patterns first so we don't leave trailing junk.
_STRIP_PATTERNS = [
    # Trailing comma-prefixed inline: "，年化 ~13.5%" / ", 年化 13.5%"
    re.compile(r"[，,]\s*年化\s*[~≈]?\s*[+\-−]?\d+(?:\.\d+)?\s*%(?:\s*/\s*(?:yr|年))?"),
    # Trailing comma-prefixed inline: "，IRR ≈ 9.5%/yr"
    re.compile(r"[，,]\s*IRR\s*[~≈]?\s*[+\-−]?\d+(?:\.\d+)?\s*%(?:\s*/\s*(?:yr|年))?"),
    # Slash-separated tail: " / IRR ≈ 9.5%/yr" or " / 年化 9.5%"
    re.compile(r"\s*/\s*(?:IRR|年化)\s*[~≈]?\s*[+\-−]?\d+(?:\.\d+)?\s*%(?:\s*/\s*(?:yr|年))?"),
    # Parenthesized: "（IRR ≈ 9.5%/yr）" or "(IRR ~ 9.5%/年)"
    re.compile(r"\s*[（(]\s*IRR\s*[~≈]?\s*[+\-−]?\d+(?:\.\d+)?\s*%(?:\s*/\s*(?:yr|年))?[^）)]*[）)]"),
    # Parenthesized: "（年化 13.5%）"
    re.compile(r"\s*[（(]\s*年化\s*[~≈]?\s*[+\-−]?\d+(?:\.\d+)?\s*%(?:\s*/\s*(?:yr|年))?[）)]"),
]

# Pattern that decides whether a <strong> is the value cell — must contain a
# percentage like "+58%" or a multiple like "1.88x".
_VALUE_PROBE = re.compile(
    r"(?:[+\-−]\s*\d+(?:\.\d+)?\s*%|(?<![\d.])\d+\.\d+\s*x)"
)

# Locate the FIRST <strong>...</strong> after the anchor.
_STRONG_RE = re.compile(r"<strong>(.*?)</strong>", re.DOTALL)


def compute_irr(pct_5y: float) -> float:
    """+58% 5Y → 9.59%/yr; -51% → -13.36%/yr. Undefined for r ≤ -100%."""
    base = 1 + pct_5y / 100
    if base <= 0:
        # Total wipeout — fall back to -100%/yr sentinel; should not occur.
        return -100.0
    return (base ** (1 / 5) - 1) * 100


def format_irr_tag(irr_pct: float) -> str:
    """Canonical form: ` / IRR ≈ +9.6%/yr` (slash-separated, leading sign)."""
    sign = "+" if irr_pct >= 0 else "−"  # use Unicode minus for visual parity
    return f" / IRR ≈ {sign}{abs(irr_pct):.1f}%/yr"


def find_anchor(html: str) -> int:
    for kw in ANCHORS:
        idx = html.find(kw)
        if idx >= 0:
            return idx
    return -1


def _find_all(s: str, kw: str) -> list[int]:
    out: list[int] = []
    start = 0
    while True:
        i = s.find(kw, start)
        if i < 0:
            return out
        out.append(i)
        start = i + len(kw)


def _patch_anchor(window: str, irr_tag: str) -> tuple[str, str, str] | None:
    """Patch a single anchor's window. Returns (new_window, before, after)
    or None if no value <strong> found / already canonical."""
    for m in _STRONG_RE.finditer(window):
        inner = m.group(1)
        if "期望值" in inner and not _VALUE_PROBE.search(inner):
            continue  # label-only strong, skip
        if not _VALUE_PROBE.search(inner):
            continue
        cleaned = inner
        for pat in _STRIP_PATTERNS:
            cleaned = pat.sub("", cleaned)
        cleaned = cleaned.rstrip()
        rebuilt = cleaned + irr_tag
        if rebuilt == inner:
            return None  # already canonical
        old_strong = m.group(0)
        new_strong = f"<strong>{rebuilt}</strong>"

        # Strip stale IRR/年化 fragments that follow the strong WITHIN the
        # same cell (bounded by the next </td>).
        post_start = m.end()
        post_section = window[post_start:]
        td_close = post_section.find("</td>")
        if td_close < 0:
            # No </td> in window — be conservative, only strip a small tail
            td_close = min(len(post_section), 200)
        in_cell = post_section[:td_close]
        after_cell = post_section[td_close:]
        cleaned_in_cell = in_cell
        for pat in _STRIP_PATTERNS:
            cleaned_in_cell = pat.sub("", cleaned_in_cell)
        new_post = cleaned_in_cell + after_cell

        new_window = window[: m.start()] + new_strong + new_post
        return new_window, old_strong, new_strong
    return None


def _is_table_cell_anchor(html: str, anchor_idx: int) -> bool:
    """Return True iff the FIRST block-level close tag after the anchor is
    </td> or </th>. Filters out narrative anchors inside <p>/<h2>/<li>/etc."""
    lookahead = html[anchor_idx : anchor_idx + 400]
    m = _CELL_CLOSE_RE.search(lookahead)
    if m is None:
        return False
    return m.group(1).lower() in ("td", "th")


def _row_window(html: str, anchor_idx: int) -> tuple[int, str]:
    """Return (window_end_byte, window_str). Window extends from anchor to
    the next </tr>, capped at 1500 bytes (a generous row-size ceiling)."""
    cap = min(len(html), anchor_idx + 1500)
    candidate = html[anchor_idx:cap]
    m = _TR_CLOSE_RE.search(candidate)
    end_offset = m.end() if m else len(candidate)
    return anchor_idx + end_offset, candidate[:end_offset]


def patch_html(html: str) -> tuple[str, dict | None]:
    """Patch every table-cell EV anchor in the doc. Returns (new_html, info)
    where info = {"pct", "irr", "patches": [{before, after}, ...]} or
    (html, None) when nothing changed.
    """
    pct = extract_dca_ev_5y_from_text(html)
    if pct is None:
        return html, None

    positions = sorted({
        idx for kw in ANCHORS for idx in _find_all(html, kw)
    })
    if not positions:
        return html, None

    irr = compute_irr(pct)
    irr_tag = format_irr_tag(irr)

    new_html = html
    patches: list[dict] = []
    # Process anchors right-to-left so earlier anchor positions remain valid.
    for anchor_idx in reversed(positions):
        if not _is_table_cell_anchor(new_html, anchor_idx):
            continue
        window_end, window = _row_window(new_html, anchor_idx)
        head = new_html[:anchor_idx]
        tail = new_html[window_end:]
        result = _patch_anchor(window, irr_tag)
        if result is None:
            continue
        new_window, before, after = result
        new_html = head + new_window + tail
        patches.append({"before": before, "after": after})

    if not patches:
        return html, None

    return new_html, {"pct": pct, "irr": irr, "patches": list(reversed(patches))}


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


_PARSE_SIGN = r"[+\-−]"


def _norm_sign(s: str) -> str:
    return "-" if s in ("-", "−") else "+"


def _parse_pct(text: str) -> float | None:
    rng = re.search(
        rf"({_PARSE_SIGN})?\s*(\d+(?:\.\d+)?)\s*%\s*(?:to|~|至|–|—|-)\s*({_PARSE_SIGN})?\s*(\d+(?:\.\d+)?)\s*%",
        text,
    )
    if rng:
        s1 = _norm_sign(rng.group(1) or "+")
        v1 = float(rng.group(2)) * (1 if s1 == "+" else -1)
        s2 = _norm_sign(rng.group(3) or s1)
        v2 = float(rng.group(4)) * (1 if s2 == "+" else -1)
        return (v1 + v2) / 2
    signed = re.search(rf"({_PARSE_SIGN})\s*(\d+(?:\.\d+)?)\s*%", text)
    if signed:
        sign = _norm_sign(signed.group(1))
        val = float(signed.group(2))
        return val if sign == "+" else -val
    bare = re.search(r"(?<![=×x.\d])(\d+(?:\.\d+)?)\s*%", text)
    if bare:
        return float(bare.group(1))
    return None


def _parse_mult(text: str) -> float | None:
    m = re.search(r"(?<![\d.×])(\d+\.\d+)\s*x", text)
    if m:
        mult = float(m.group(1))
        if mult >= 1.0:
            return (mult - 1) * 100
    return None


_OUR_IRR_TAG_RE = re.compile(
    r"\s*/\s*IRR\s*[~≈]?\s*[+\-−]?\s*\d+(?:\.\d+)?\s*%(?:\s*/\s*(?:yr|年))?"
)


def _drop_our_irr(s: str) -> str:
    """Strip the canonical "/ IRR ≈ ±X.X%/yr" tag we ourselves emit, so a
    second pass doesn't mis-parse it as the 5Y absolute return."""
    return _OUR_IRR_TAG_RE.sub("", s)


def _extract_from_window(window: str) -> float | None:
    for sm in re.finditer(r"<strong>(.*?)</strong>", window, re.DOTALL):
        text = _drop_our_irr(_strip_tags(sm.group(1)))
        if "期望值" in text and "%" not in text and "x" not in text:
            continue
        pct = _parse_pct(text)
        if pct is not None:
            return pct
        mult = _parse_mult(text)
        if mult is not None:
            return mult
    flat = _drop_our_irr(_strip_tags(window))
    for kw in ANCHORS:
        flat = flat.replace(kw, "", 1)
    pct = _parse_pct(flat)
    if pct is not None:
        return pct
    return _parse_mult(flat)


def extract_dca_ev_5y_from_text(html: str) -> float | None:
    """Walk every table-cell anchor in document order; return the first
    parseable EV. Skips anchors in narrative contexts (`<p>`, `<h2>`, `<li>`)
    where a stray "1.5%" elsewhere in the doc could mislead the regex.
    """
    positions = sorted({idx for kw in ANCHORS for idx in _find_all(html, kw)})
    for anchor_idx in positions:
        if not _is_table_cell_anchor(html, anchor_idx):
            continue
        _, window = _row_window(html, anchor_idx)
        ev = _extract_from_window(window)
        if ev is not None:
            return ev
    return None


def select_files(filter_tickers: list[str] | None) -> list[Path]:
    if not DCA_DIR.exists():
        return []
    latest: dict[str, tuple[str, Path]] = {}
    for path in DCA_DIR.glob("DCA_*.html"):
        m = DCA_FILENAME_RE.match(path.name)
        if not m:
            continue
        ticker, date_str = m.group(1), m.group(2)
        if filter_tickers and ticker not in filter_tickers:
            continue
        prev = latest.get(ticker)
        if prev is None or date_str > prev[0]:
            latest[ticker] = (date_str, path)
    # Return all files (not just latest) so older versions also get patched.
    if filter_tickers:
        # When filtering, allow caller to see all dated versions of the ticker.
        out = []
        for path in DCA_DIR.glob("DCA_*.html"):
            m = DCA_FILENAME_RE.match(path.name)
            if not m:
                continue
            if m.group(1) in filter_tickers:
                out.append(path)
        return sorted(out)
    return sorted(DCA_DIR.glob("DCA_*.html"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="actually write changes (default: dry-run)")
    ap.add_argument("--files", nargs="*", default=None,
                    help="restrict to these tickers (e.g. KLAC NVDA 2330TW)")
    ap.add_argument("--quiet", action="store_true",
                    help="only print summary, not per-file diff")
    args = ap.parse_args()

    files = select_files(args.files)
    if not files:
        print("[patch_dca_irr] no DCA files matched.")
        return 0

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[patch_dca_irr] mode={mode}, files={len(files)}")

    n_patched = n_unchanged = n_skipped = 0
    for path in files:
        try:
            html = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[skip] {path.name}: read error {e}")
            n_skipped += 1
            continue

        new_html, change = patch_html(html)
        if change is None:
            n_unchanged += 1
            if not args.quiet:
                print(f"[noop] {path.name}: no §4 期望值 cell or already canonical")
            continue

        n_patched += 1
        if not args.quiet:
            print(
                f"[patch] {path.name}: 5Y={change['pct']:+.2f}% → "
                f"IRR={change['irr']:+.2f}%/yr  ({len(change['patches'])} cell(s))"
            )
            for i, p in enumerate(change["patches"]):
                print(f"        [{i+1}] before: {p['before']}")
                print(f"            after : {p['after']}")

        if args.apply:
            path.write_text(new_html, encoding="utf-8")

    print(
        f"[patch_dca_irr] done. patched={n_patched}, "
        f"unchanged={n_unchanged}, skipped={n_skipped}"
    )
    if not args.apply:
        print("[patch_dca_irr] dry-run only; rerun with --apply to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
