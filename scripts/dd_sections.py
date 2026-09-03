#!/usr/bin/env python3
"""dd_sections.py — canonical section splitter for v15/v15.2 DD reports.

Single source of truth for "where does §N live in this HTML file" so that
writer/critic/patch agents and qc.py never hand-roll their own regex against
docs/dd/DD_*.html. Both a CLI and an importable module (Python 3.9, stdlib
only — see notes/site-internal/dd/_v15_2_design_spec_20260903.md §2.1).

Canonical section ids: s1..s14 (§13 uses "decision"), s85 (§8.5, optional),
appA / appB (<details id="appA">/"appB">, optional), revlog, sources
(optional). `dashboard` = from <div class="topbar"> up to (not including)
<nav class="dd-toc">. `dd-meta` = the <script id="dd-meta" ...>...</script>
block.

Two ways a section's start can be located in an existing file:
  - "attr"  — an actual id="<cid>" attribute on a <section>/<details>/<h2>/
              <div> tag (the v15.2-forced canonical form; also what VIK/NVDA
              use via <section id=...> and what SE uses via <h2 id=...>).
  - "text"  — no matching id attribute anywhere, so the section is located by
              matching the §N marker inside the nearest <h2> text (s1..s14 /
              decision / s85), or inside a <details><summary> for appA/appB
              (SE's appendix carries id="appxA", not "appA" — exactly this
              case).

`bytes`/`text`/`extract` use attr-first-then-text fallback. `replace` is
attr-only and requires *exactly one* attribute match — falling back to text
inference for a destructive rewrite would be unsafe, so it exits 2 instead.

Subcommands: bytes / text / extract (optional `--out DIR` — one file per id
instead of stdout) / replace / replace-many (batch `replace`, all-or-nothing
against a DIR of `{id}.html` files) / leaks — see module docstring sections
below and the design spec for exact behaviour.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KB = 1000  # repo convention: pre-commit's 70000/80000/115000 are decimal, not 1024-based

# ---------------------------------------------------------------------------
# canonical ids, order, byte budgets
# ---------------------------------------------------------------------------

CANON_IDS = [
    "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s85", "s9", "s10",
    "s11", "s12", "decision", "s14", "appA", "appB", "revlog", "sources",
]

# §-number each canonical section id maps to, for the <h2> text-fallback scan.
_SECTION_NUM = {
    "s1": "1", "s2": "2", "s3": "3", "s4": "4", "s5": "5", "s6": "6",
    "s7": "7", "s8": "8", "s9": "9", "s10": "10", "s11": "11", "s12": "12",
    "decision": "13", "s14": "14",
}

H2_LABEL_PATTERNS = {
    cid: r"§" + num + r"(?![\d.])" for cid, num in _SECTION_NUM.items()
}
H2_LABEL_PATTERNS["s85"] = r"§8\.5(?!\d)"

# byte budgets in bytes (KB * 1000). None = no cap. "decision" is (min, max).
BUDGETS = {
    "dashboard": 7 * KB,
    "s1": 4 * KB,
    "s2": 7 * KB,
    "s3": 8 * KB,
    "s4": 5 * KB,
    "s5": 15 * KB,
    "s6": 11 * KB,
    "s7": 5 * KB,
    "s8": 3 * KB,
    "s85": None,
    "s9": 3.5 * KB,
    "s10": 5 * KB,
    "s11": 3 * KB,
    "s12": 2.5 * KB,
    "decision": (4 * KB, 5 * KB),
    "s14": 2 * KB,
    "appA": 1.5 * KB,
    "appB": 3 * KB,
    "revlog": None,
    "sources": None,
}

# aggregate group definitions (§2.1 彙總列)
PART1_IDS = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s85", "s9", "s10"]
BIZ_IDS = ["s3", "s4", "s5", "s6", "s7"]
VALUATION_IDS = ["s10", "appA"]
DECISION_LAYER_IDS = ["s11", "s12", "decision", "s14"]
# denominator for the two % aggregates: the report "spine" — dashboard is
# budgeted separately and revlog/sources are open-ended appendices, so both
# are excluded here (judgment call; see WP1 handoff notes — flagged because
# the spec does not spell out the denominator explicitly).
SPINE_IDS = [
    "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s85", "s9", "s10",
    "s11", "s12", "decision", "s14", "appA", "appB",
]

TOTAL_FILE_FLOOR = 70 * KB
TOTAL_FILE_WARN_LOW = 80 * KB
TOTAL_FILE_WARN_HIGH = 115 * KB

# ---------------------------------------------------------------------------
# low-level marker location
# ---------------------------------------------------------------------------

_ATTR_TAGS = "section|details|h2|div"


def _attr_matches(html: str, cid: str):
    """All <tag ... id="cid" ...> opening-tag matches (tag in section/details/h2/div)."""
    pat = re.compile(
        r"<(" + _ATTR_TAGS + r")\b[^>]*\bid=[\"']" + re.escape(cid) + r"[\"'][^>]*>"
    )
    return list(pat.finditer(html))


def _appendix_letter_match(html: str, letter: str):
    """Locate a <details>...<summary>附錄{letter}...</summary> block (id-less fallback)."""
    pat = re.compile(
        r"<details\b[^>]*>\s*<summary[^>]*>\s*附錄\s*" + letter + r"\b"
    )
    return pat.search(html)


def _open_tag_end(html: str, start: int) -> int:
    m = re.match(r"<[a-zA-Z0-9]+\b[^>]*>", html[start:])
    return start + (m.end() if m else 1)


def _matching_close(html: str, open_end: int, tag: str) -> int:
    """Index right after the </tag> that balances the <tag> opened at open_end."""
    open_re = re.compile(r"<" + tag + r"\b", re.IGNORECASE)
    close_re = re.compile(r"</" + tag + r"\s*>", re.IGNORECASE)
    depth = 1
    pos = open_end
    while depth > 0:
        nc = close_re.search(html, pos)
        if nc is None:
            return len(html)
        no = open_re.search(html, pos)
        if no is not None and no.start() < nc.start():
            depth += 1
            pos = no.end()
        else:
            depth -= 1
            pos = nc.end()
    return pos


_END_MARKERS_RE = re.compile(
    r'<button[^>]*class="printbtn"|<!--\s*DD_LIVEBAR\s*-->|</body>', re.IGNORECASE
)


def _end_of_content(html: str, start: int) -> int:
    m = _END_MARKERS_RE.search(html, start)
    return m.start() if m else len(html)


def _locate_attr_or_text(html: str, cid: str):
    """Return dict(start, tag, open_end, via) for cid, attr-first then text-fallback.

    Uses the FIRST match only (lenient — uniqueness is replace()'s job, not
    this one's). Returns None if not found by either method.
    """
    matches = _attr_matches(html, cid)
    if matches:
        m = matches[0]
        return {"start": m.start(), "tag": m.group(1), "open_end": m.end(), "via": "attr"}

    if cid in ("appA", "appB"):
        letter = "A" if cid == "appA" else "B"
        m = _appendix_letter_match(html, letter)
        if m is None:
            return None
        return {
            "start": m.start(), "tag": "details",
            "open_end": _open_tag_end(html, m.start()), "via": "text",
        }

    pattern = H2_LABEL_PATTERNS.get(cid)
    if pattern is None:
        return None
    m = re.search(r"<h2\b[^>]*>\s*" + pattern, html)
    if m is None:
        return None
    return {"start": m.start(), "tag": "h2", "open_end": None, "via": "text"}


def _dashboard_span(html: str):
    m1 = re.search(r'<div\s+class="topbar"', html)
    if not m1:
        return None
    m2 = re.search(r'<nav\s+class="dd-toc"', html)
    if m2 and m2.start() > m1.start():
        return (m1.start(), m2.start())
    # No (valid) <nav class="dd-toc"> after topbar — the normal case for a
    # BODY file (writer output / render_dd.py --to-body product), whose toc
    # is auto-generated later by render_dd.py's assemble(). Fall back to the
    # first <section ...> or <details id="appA" ...> after topbar, whichever
    # comes first, as the dashboard's end boundary.
    tail = html[m1.end():]
    candidates = []
    ms = re.search(r"<section\b", tail)
    if ms:
        candidates.append(m1.end() + ms.start())
    md = re.search(r'<details\b[^>]*\bid=["\']appA["\']', tail)
    if md:
        candidates.append(m1.end() + md.start())
    if candidates:
        return (m1.start(), min(candidates))
    return None


def _dd_meta_span(html: str):
    m = re.search(r'<script\s+id=["\']dd-meta["\'][^>]*>', html)
    if not m:
        return None
    close = re.search(r"</script\s*>", html[m.end():], re.IGNORECASE)
    if not close:
        return None
    return (m.start(), m.end() + close.end())


def split_sections(html: str):
    """Ordered list of markers actually present in `html`, each a dict with
    id / start / end / tag / via. Document order. Lenient (first-match) —
    does not itself check for duplicate ids; replace() re-verifies uniqueness.
    """
    found = []
    for cid in CANON_IDS:
        loc = _locate_attr_or_text(html, cid)
        if loc is not None:
            found.append({"id": cid, **loc})
    found.sort(key=lambda m: m["start"])

    n = len(found)
    for i, mk in enumerate(found):
        wrapped = mk["tag"] in ("section", "details", "div") and mk["open_end"] is not None
        if wrapped:
            mk["end"] = _matching_close(html, mk["open_end"], mk["tag"])
        elif i + 1 < n:
            mk["end"] = found[i + 1]["start"]
        else:
            mk["end"] = _end_of_content(html, mk["start"])
        mk["wrapped"] = wrapped
    return found


def dashboard_span(html: str):
    """Public wrapper around _dashboard_span (used by render_dd.py)."""
    return _dashboard_span(html)


def dd_meta_span(html: str):
    """Public wrapper around _dd_meta_span (used by render_dd.py)."""
    return _dd_meta_span(html)


def _dd_meta_json(html: str):
    span = _dd_meta_span(html)
    if span is None:
        return None
    block = html[span[0]:span[1]]
    m = re.search(r">(.*)</script\s*>", block, re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def dd_meta_json(html: str):
    """Public wrapper around _dd_meta_json (used by render_dd.py)."""
    return _dd_meta_json(html)


# ---------------------------------------------------------------------------
# extract / replace
# ---------------------------------------------------------------------------

SECTION_BREAK = "\n<!-- DD_SECTION_BREAK -->\n"


def _span_for_id(html: str, cid: str):
    if cid == "dashboard":
        return _dashboard_span(html)
    if cid == "dd-meta":
        return _dd_meta_span(html)
    markers = split_sections(html)
    for mk in markers:
        if mk["id"] == cid:
            return (mk["start"], mk["end"])
    return None


def extract(html: str, ids) -> str:
    """Raw HTML chunks for the given ids, in DOCUMENT order (not `ids` order),
    joined by DD_SECTION_BREAK. Missing ids are silently skipped.
    """
    spans = []
    for cid in ids:
        span = _span_for_id(html, cid)
        if span is not None:
            spans.append(span)
    spans.sort(key=lambda s: s[0])
    return SECTION_BREAK.join(html[s:e] for s, e in spans)


class ReplaceError(Exception):
    pass


class ReplaceManyError(Exception):
    """Raised by replace_many() when >=1 patch fails validation. `.errors` is
    a list of (cid, reason) covering EVERY failing id (not just the first),
    so the batch can be reported and rejected atomically."""

    def __init__(self, errors):
        self.errors = errors
        super().__init__("; ".join(f"{c}: {r}" for c, r in errors))


def _locate_for_replace(html: str, cid: str, new_block: str):
    """Return (start, end) span that `replace()`/`replace_many()` would
    splice `new_block` into. Raises ReplaceError under the same conditions
    `replace()` used to (id not found exactly once, wrapper missing) —
    shared so replace_many() can dry-run validation against the pristine
    html without duplicating the location logic.
    """
    if cid == "dashboard":
        span = _dashboard_span(html)
        if span is None:
            raise ReplaceError("dashboard region not found (need <div class=\"topbar\"> ... <nav class=\"dd-toc\">)")
        if 'class="topbar"' not in new_block:
            raise ReplaceError('NEWFILE 缺少外層 wrapper（找不到 class="topbar"）')
        return span
    if cid == "dd-meta":
        span = _dd_meta_span(html)
        if span is None:
            raise ReplaceError("dd-meta block not found")
        if 'id="dd-meta"' not in new_block and "id='dd-meta'" not in new_block:
            raise ReplaceError('NEWFILE 缺少外層 wrapper（找不到 id="dd-meta"）')
        return span

    matches = _attr_matches(html, cid)
    if len(matches) != 1:
        raise ReplaceError(
            f'id="{cid}" 命中 {len(matches)} 次（需恰好 1 次）— replace 只支援帶 canonical id 的檔'
        )
    m = matches[0]
    if f'id="{cid}"' not in new_block and f"id='{cid}'" not in new_block:
        raise ReplaceError(f'NEWFILE 缺少外層 wrapper（找不到 id="{cid}"）')
    wrapped = m.group(1) in ("section", "details", "div")
    if wrapped:
        end = _matching_close(html, m.end(), m.group(1))
    else:
        markers = split_sections(html)
        end = None
        for i, mk in enumerate(markers):
            if mk["id"] == cid and mk["start"] == m.start():
                end = mk["end"]
                break
        if end is None:
            end = _end_of_content(html, m.start())
    return (m.start(), end)


def replace(html: str, cid: str, new_block: str) -> str:
    """Splice `new_block` in place of the sole occurrence of `cid`.

    attr-only (no text-fallback) — see module docstring. Raises ReplaceError
    (caller maps to exit 2) if the id is not found exactly once, or if
    new_block doesn't look like it carries the same outer wrapper.
    """
    start, end = _locate_for_replace(html, cid, new_block)
    return html[:start] + new_block + html[end:]


def replace_many(html: str, patches):
    """Batch, all-or-nothing `replace()`.

    `patches`: ordered list of (cid, new_block) tuples. Phase 1 validates
    EVERY patch against the pristine `html` (exactly-one-match + wrapper
    checks, via `_locate_for_replace`) and collects ALL failures; if any
    patch fails, raises ReplaceManyError (nothing applied — the caller must
    not write a file). Phase 2 (only reached if phase 1 is clean) applies
    the patches sequentially, re-locating each cid against the
    progressively-updated html (so later patches see earlier ones' output).

    Returns (new_html, results) where results is a list of
    (cid, old_bytes, new_bytes) in `patches` order.
    """
    errors = []
    for cid, new_block in patches:
        try:
            _locate_for_replace(html, cid, new_block)
        except ReplaceError as e:
            errors.append((cid, str(e)))
    if errors:
        raise ReplaceManyError(errors)

    cur = html
    results = []
    for cid, new_block in patches:
        start, end = _locate_for_replace(cur, cid, new_block)
        old_bytes = len(cur[start:end].encode("utf-8"))
        cur = cur[:start] + new_block + cur[end:]
        results.append((cid, old_bytes, len(new_block.encode("utf-8"))))
    return cur, results


# ---------------------------------------------------------------------------
# readable text (for critic / patch agents)
# ---------------------------------------------------------------------------

_STRIP_TAGS = ("script", "style", "code")


def _blank_preserve_lines(m: "re.Match") -> str:
    return "\n" * m.group(0).count("\n")


def _strip_details_blocks(html: str) -> str:
    """Replace each top-level <details>...</details> with its text content,
    every non-blank line prefixed "[折疊] "."""
    out = []
    pos = 0
    pat = re.compile(r"<details\b", re.IGNORECASE)
    while True:
        m = pat.search(html, pos)
        if not m:
            out.append(html[pos:])
            break
        out.append(html[pos:m.start()])
        open_end = _open_tag_end(html, m.start())
        close_end = _matching_close(html, open_end, "details")
        inner = html[open_end:close_end]
        # strip the details/summary closing tag itself from inner text
        inner = re.sub(r"</?summary[^>]*>", "\n", inner, flags=re.IGNORECASE)
        inner = re.sub(r"</details\s*>\s*$", "", inner, flags=re.IGNORECASE)
        inner_text = _tags_to_text(inner)
        prefixed = "\n".join(
            ("[折疊] " + ln if ln.strip() else ln) for ln in inner_text.split("\n")
        )
        out.append(prefixed)
        pos = close_end
    return "".join(out)


def _flatten_tables(html: str) -> str:
    def _one_table(m: "re.Match") -> str:
        table_html = m.group(0)
        rows = re.findall(r"<tr\b.*?</tr>", table_html, re.DOTALL | re.IGNORECASE)
        lines = []
        for row in rows:
            cells = re.findall(r"<t[dh]\b.*?</t[dh]>", row, re.DOTALL | re.IGNORECASE)
            cell_texts = [_tags_to_text(c).strip() for c in cells]
            lines.append(" | ".join(cell_texts))
        return "\n" + "\n".join(lines) + "\n"

    return re.sub(r"<table\b.*?</table>", _one_table, html, flags=re.DOTALL | re.IGNORECASE)


def _tags_to_text(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html)
    return text


def _strip_nav_and_primer(html: str) -> str:
    html = re.sub(
        r'<header class="imq-nav-root"[^>]*>.*?</header>', "", html, flags=re.DOTALL
    )
    html = re.sub(
        r"<!-- PLAIN_PRIMER_START -->.*?<!-- PLAIN_PRIMER_END -->",
        "", html, flags=re.DOTALL,
    )
    html = re.sub(
        r'<!--\s*DD_LIVEBAR\s*-->\s*<script[^>]*dd-livebar\.js[^>]*></script>',
        "", html, flags=re.DOTALL,
    )
    return html


def readable_text(html: str, ids=None) -> str:
    """Visible-text rendering for critic/patch consumption.

    ids=None -> whole document (dd-meta JSON preamble + body text).
    ids=[...] -> only those sections' text (no preamble unless "dd-meta"
    is itself in `ids`).
    """
    parts = []
    if ids is None:
        meta = _dd_meta_json(html)
        if meta is not None:
            parts.append(json.dumps(meta, ensure_ascii=False, indent=2))
        body = html
        # drop the dd-meta script itself from the body pass (already emitted above)
        span = _dd_meta_span(html)
        if span:
            body = body[:span[0]] + body[span[1]:]
        chunks = [body]
    else:
        chunks = []
        for cid in ids:
            span = _span_for_id(html, cid)
            if span is not None:
                chunks.append(html[span[0]:span[1]])

    for chunk in chunks:
        chunk = _strip_nav_and_primer(chunk)
        chunk = re.sub(r"<style\b.*?</style>", "", chunk, flags=re.DOTALL | re.IGNORECASE)
        chunk = re.sub(r"<script\b.*?</script>", "", chunk, flags=re.DOTALL | re.IGNORECASE)
        chunk = _flatten_tables(chunk)
        chunk = _strip_details_blocks(chunk)
        chunk = _tags_to_text(chunk)
        chunk = re.sub(r"[ \t]+", " ", chunk)
        chunk = re.sub(r"\n{3,}", "\n\n", chunk)
        parts.append(chunk.strip())

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# leaks — visible machine-language scan (also the QC-40 canonical wordlist)
# ---------------------------------------------------------------------------

LEAK_PATTERNS = [
    r"row ?\d",
    r"Hard Veto",
    r"Soft Veto",
    r"signal ?[ABCX]\b",
    r"估值燈",
    r"val ?[🟢🟡🟠🔴]",
    r"MA ?[✅❌🟢🟡🟠]",
    r"Pure MA",
    r"盲點 ?\d",
    r"PREREG",
    r"dd-meta",
    r"runway_post_y5",
    r"capalloc",
    r"QC-\d",
    r"archetype",
    r"metadata",
    r"硬接線",
    r"接線[:：]",
    r"Guardrail",
    r"校驗紀錄",
    r"判定規則",
    r"\bgate\b",
    r"\bF2\b",
    r"row 8[ab]",
    r"爆發候選路徑",
    r"循環衛星進場路徑",
]
_LEAK_RES = [re.compile(p) for p in LEAK_PATTERNS]  # case-sensitive, per spec
# `<` 後面不是標籤起始字元（字母／`/`／`!`／`?`）＝正文未跳脫的小於號
_UNESCAPED_LT_RE = re.compile(r"<(?![A-Za-z/!?])")


def _leak_scan_html(html: str) -> str:
    """Blank (newline-preserving) style/script/code/nav/primer/<details> zones."""
    for tag in ("script", "style", "code"):
        html = re.sub(
            rf"<{tag}\b.*?</{tag}>", _blank_preserve_lines, html,
            flags=re.DOTALL | re.IGNORECASE,
        )
    html = re.sub(
        r'<header class="imq-nav-root"[^>]*>.*?</header>',
        _blank_preserve_lines, html, flags=re.DOTALL,
    )
    html = re.sub(
        r"<!-- PLAIN_PRIMER_START -->.*?<!-- PLAIN_PRIMER_END -->",
        _blank_preserve_lines, html, flags=re.DOTALL,
    )
    # blank every top-level <details>...</details>
    out = []
    pos = 0
    pat = re.compile(r"<details\b", re.IGNORECASE)
    while True:
        m = pat.search(html, pos)
        if not m:
            out.append(html[pos:])
            break
        out.append(html[pos:m.start()])
        open_end = _open_tag_end(html, m.start())
        close_end = _matching_close(html, open_end, "details")
        out.append(_blank_preserve_lines_str(html[m.start():close_end]))
        pos = close_end
    return "".join(out)


def _blank_preserve_lines_str(s: str) -> str:
    return "\n" * s.count("\n")


def leak_hits(html: str):
    """List of (lineno, word, context) for every LEAK_PATTERNS hit in visible text."""
    scanned = _leak_scan_html(html)
    hits = []
    # v15.2.5：未跳脫的 `<`（後接數字／$／−／空白等非標籤字元）會被瀏覽器當成標籤
    # 起點吃掉整段承重句，且躲過下方的 tag-strip 掃描（DELL 2026-09-03 五處實例）。
    # 這一項不分 <details> 內外（折疊區一樣會被截斷），只遮 script/style/code。
    light = html
    for tag in ("script", "style", "code"):
        light = re.sub(rf"<{tag}\b.*?</{tag}>", _blank_preserve_lines, light,
                       flags=re.DOTALL | re.IGNORECASE)
    for i, line in enumerate(light.split("\n"), 1):
        for m in _UNESCAPED_LT_RE.finditer(line):
            ctx = line[max(0, m.start() - 15):m.start() + 25].strip()
            hits.append((i, "未跳脫<", ctx))
    for i, line in enumerate(scanned.split("\n"), 1):
        text = re.sub(r"<[^>]+>", " ", line)
        claimed = []  # (start,end) spans already reported on this line
        for pat in _LEAK_RES:
            for m in pat.finditer(text):
                if any(s < m.end() and m.start() < e for s, e in claimed):
                    continue
                claimed.append((m.start(), m.end()))
                ctx = text[max(0, m.start() - 15):m.start() + 25].strip()
                hits.append((i, m.group(0), ctx))
    return hits


# ---------------------------------------------------------------------------
# section_bytes — the qc.py-facing summary
# ---------------------------------------------------------------------------

def _visible_table_count(html: str) -> int:
    stripped = _leak_scan_html(html)  # already blanks <details> (and script/style)
    return len(re.findall(r"<table\b", stripped, re.IGNORECASE))


def _line_of(html: str, pos: int) -> int:
    return html.count("\n", 0, pos) + 1


def _status_for_budget(cid: str, nbytes: int, present: bool):
    if not present:
        return "N/A"
    budget = BUDGETS.get(cid)
    if budget is None:
        return "N/A"
    if cid == "decision":
        lo, hi = budget
        return "WARN" if (nbytes < lo or nbytes > hi) else "OK"
    return "WARN" if nbytes > budget else "OK"


def section_bytes(html: str):
    """List of dicts describing every canonical section + dashboard + the
    §2.1 aggregate rows. Each row: kind="section"|"aggregate".
    """
    rows = []
    markers = split_sections(html)
    by_id = {m["id"]: m for m in markers}

    dash = _dashboard_span(html)
    dash_bytes = (dash[1] - dash[0]) if dash else 0
    rows.append({
        "id": "dashboard", "kind": "section", "present": dash is not None,
        "bytes": dash_bytes, "budget": BUDGETS["dashboard"],
        "status": _status_for_budget("dashboard", dash_bytes, dash is not None),
        "line": _line_of(html, dash[0]) if dash else None, "via": "attr" if dash else None,
    })

    section_total = {}
    for cid in CANON_IDS:
        mk = by_id.get(cid)
        present = mk is not None
        nbytes = (mk["end"] - mk["start"]) if present else 0
        section_total[cid] = nbytes
        rows.append({
            "id": cid, "kind": "section", "present": present, "bytes": nbytes,
            "budget": BUDGETS.get(cid), "status": _status_for_budget(cid, nbytes, present),
            "line": _line_of(html, mk["start"]) if present else None,
            "via": mk["via"] if present else None,
        })

    spine = sum(section_total.get(cid, 0) for cid in SPINE_IDS if cid in by_id)

    def _pct(ids):
        num = sum(section_total.get(cid, 0) for cid in ids if cid in by_id)
        return (num / spine * 100.0) if spine else 0.0

    part1_pct = _pct(PART1_IDS)
    biz_pct = _pct(BIZ_IDS)
    valuation_bytes = sum(section_total.get(cid, 0) for cid in VALUATION_IDS if cid in by_id)
    decision_layer_bytes = sum(section_total.get(cid, 0) for cid in DECISION_LAYER_IDS if cid in by_id)
    table_count = _visible_table_count(html)
    total_bytes = len(html.encode("utf-8"))

    rows.append({
        "id": "_part1", "kind": "aggregate",
        "label": "Part I（s1-s10+s85）佔 section 總 bytes",
        "value_pct": round(part1_pct, 1), "budget_pct_min": 60,
        "status": "WARN" if part1_pct < 60 else "OK", "line": 1,
    })
    rows.append({
        "id": "_biz", "kind": "aggregate", "label": "商業本質（s3-s7）佔 section 總 bytes",
        "value_pct": round(biz_pct, 1), "budget_pct_min": 45,
        "status": "WARN" if biz_pct < 45 else "OK", "line": 1,
    })
    rows.append({
        "id": "_valuation", "kind": "aggregate", "label": "估值（s10+appA）",
        "value_bytes": valuation_bytes, "budget_bytes_max": 6.5 * KB,
        "status": "WARN" if valuation_bytes > 6.5 * KB else "OK", "line": 1,
    })
    rows.append({
        "id": "_decision_layer", "kind": "aggregate",
        "label": "決策層（s11+s12+decision+s14）",
        "value_bytes": decision_layer_bytes, "budget_bytes_max": 12 * KB,
        "status": "WARN" if decision_layer_bytes > 12 * KB else "OK", "line": 1,
    })
    rows.append({
        "id": "_visible_tables", "kind": "aggregate", "label": "可見表格數（不含 <details> 內）",
        "value": table_count, "budget_max": 14,
        "status": "WARN" if table_count > 14 else "OK", "line": 1,
    })
    if total_bytes < TOTAL_FILE_FLOOR:
        total_status = "WARN"
    elif total_bytes < TOTAL_FILE_WARN_LOW:
        total_status = "WARN"
    elif total_bytes > TOTAL_FILE_WARN_HIGH:
        total_status = "WARN"
    else:
        total_status = "OK"
    rows.append({
        "id": "_total_file", "kind": "aggregate", "label": "總檔案 bytes",
        "value_bytes": total_bytes, "floor": TOTAL_FILE_FLOOR,
        "warn_low": TOTAL_FILE_WARN_LOW, "warn_high": TOTAL_FILE_WARN_HIGH,
        "status": total_status, "line": 1,
    })
    return rows


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _fmt_kb(n) -> str:
    return f"{n / KB:.2f}KB"


def _cmd_bytes(args):
    html = Path(args.file).read_text(encoding="utf-8")
    rows = section_bytes(html)
    meta = _dd_meta_json(html)
    schema = meta.get("schema") if meta else "?"

    if args.json:
        print(json.dumps({"file": args.file, "schema": schema, "rows": rows}, ensure_ascii=False, indent=2))
    else:
        print(f"{args.file} — schema {schema}")
        print(f"{'段落':<16}{'bytes':>10}  {'預算':>10}  狀態")
        for r in rows:
            if r["kind"] != "section":
                continue
            if not r["present"]:
                print(f"{r['id']:<16}{'—':>10}  {'—':>10}  (不存在)")
                continue
            budget = r["budget"]
            budget_s = "—" if budget is None else (
                f"{budget[0]/KB:.1f}-{budget[1]/KB:.1f}KB" if isinstance(budget, tuple) else _fmt_kb(budget)
            )
            print(f"{r['id']:<16}{_fmt_kb(r['bytes']):>10}  {budget_s:>10}  {r['status']} (via={r['via']})")
        print("\n彙總：")
        for r in rows:
            if r["kind"] != "aggregate":
                continue
            if "value_pct" in r:
                print(f"  {r['label']:<32} {r['value_pct']:>6.1f}%  (下限 {r['budget_pct_min']}%)  {r['status']}")
            elif "value_bytes" in r and "budget_bytes_max" in r:
                print(f"  {r['label']:<32} {_fmt_kb(r['value_bytes']):>8}  (上限 {_fmt_kb(r['budget_bytes_max'])})  {r['status']}")
            elif "value_bytes" in r:
                print(f"  {r['label']:<32} {r['value_bytes']:>8}B  (floor {r['floor']} / warn_low {r['warn_low']} / warn_high {r['warn_high']})  {r['status']}")
            else:
                print(f"  {r['label']:<32} {r['value']:>6}  (上限 {r['budget_max']})  {r['status']}")

    any_warn = any(r["status"] == "WARN" for r in rows)
    if args.strict and any_warn:
        sys.exit(1)
    sys.exit(0)


def _cmd_text(args):
    html = Path(args.file).read_text(encoding="utf-8")
    ids = args.ids.split(",") if args.ids else None
    print(readable_text(html, ids))


def _cmd_extract(args):
    html = Path(args.file).read_text(encoding="utf-8")
    ids = args.ids.split(",")

    if args.out_dir:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        written = []
        missing = []
        for cid in ids:
            span = _span_for_id(html, cid)
            if span is None:
                missing.append(cid)
                continue
            chunk = html[span[0]:span[1]]
            (out_dir / f"{cid}.html").write_text(chunk, encoding="utf-8")
            written.append((cid, len(chunk.encode("utf-8"))))
        if not written:
            print(f"找不到任何指定 id：{args.ids}", file=sys.stderr)
            sys.exit(2)
        for cid, nbytes in written:
            print(f"{cid}: {nbytes}B -> {out_dir / (cid + '.html')}")
        if missing:
            print(f"找不到（跳過）：{','.join(missing)}", file=sys.stderr)
        sys.exit(0)

    out = extract(html, ids)
    if not out:
        print(f"找不到任何指定 id：{args.ids}", file=sys.stderr)
        sys.exit(2)
    sys.stdout.write(out)


def _cmd_replace(args):
    html = Path(args.file).read_text(encoding="utf-8")
    new_block = Path(args.newfile).read_text(encoding="utf-8")
    old_bytes = None
    span = _span_for_id(html, args.id)
    if span:
        old_bytes = len((html[span[0]:span[1]]).encode("utf-8"))
    try:
        new_html = replace(html, args.id, new_block)
    except ReplaceError as e:
        print(f"replace 失敗：{e}", file=sys.stderr)
        sys.exit(2)
    Path(args.file).write_text(new_html, encoding="utf-8")
    new_bytes = len(new_block.encode("utf-8"))
    old_s = "?" if old_bytes is None else f"{old_bytes}B"
    print(f"{args.id}: {old_s} → {new_bytes}B")
    sys.exit(0)


def _cmd_replace_many(args):
    html = Path(args.file).read_text(encoding="utf-8")
    src_dir = Path(args.dir)
    files = sorted(src_dir.glob("*.html"))
    if not files:
        print(f"目錄內沒有 .html 檔：{args.dir}", file=sys.stderr)
        sys.exit(2)
    patches = [(f.stem, f.read_text(encoding="utf-8")) for f in files]

    try:
        new_html, results = replace_many(html, patches)
    except ReplaceManyError as e:
        print("replace-many 失敗，整批不寫檔：", file=sys.stderr)
        for cid, reason in e.errors:
            print(f"  {cid}: {reason}", file=sys.stderr)
        sys.exit(2)

    Path(args.file).write_text(new_html, encoding="utf-8")
    for cid, old_b, new_b in results:
        print(f"{cid}: {old_b}B → {new_b}B")
    total_bytes = len(new_html.encode("utf-8"))
    print(f"總檔案: {total_bytes}B ({total_bytes / KB:.2f}KB)")
    sys.exit(0)


def _cmd_leaks(args):
    html = Path(args.file).read_text(encoding="utf-8")
    hits = leak_hits(html)
    for lineno, word, ctx in hits:
        print(f"{lineno}: {word} ｜ {ctx}")
    print(f"總數: {len(hits)}")
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_bytes = sub.add_parser("bytes", help="每段 bytes／預算／狀態")
    p_bytes.add_argument("file")
    p_bytes.add_argument("--json", action="store_true")
    p_bytes.add_argument("--strict", action="store_true", help="任一 WARN 則 exit 1")
    p_bytes.set_defaults(func=_cmd_bytes)

    p_text = sub.add_parser("text", help="可讀純文字")
    p_text.add_argument("file")
    p_text.add_argument("ids", nargs="?", default=None, help="逗號分隔，省略＝全文")
    p_text.set_defaults(func=_cmd_text)

    p_extract = sub.add_parser("extract", help="原始 HTML 片段")
    p_extract.add_argument("file")
    p_extract.add_argument("ids", help="逗號分隔")
    p_extract.add_argument("--out", dest="out_dir", default=None, help="逐段寫入 DIR/{id}.html，取代印到 stdout")
    p_extract.set_defaults(func=_cmd_extract)

    p_replace = sub.add_parser("replace", help="整段替換")
    p_replace.add_argument("file")
    p_replace.add_argument("id")
    p_replace.add_argument("newfile")
    p_replace.set_defaults(func=_cmd_replace)

    p_replace_many = sub.add_parser("replace-many", help="批次整段替換（DIR 下每個 {id}.html；全部命中恰 1 才寫檔，任一失敗整批不寫）")
    p_replace_many.add_argument("file")
    p_replace_many.add_argument("dir")
    p_replace_many.set_defaults(func=_cmd_replace_many)

    p_leaks = sub.add_parser("leaks", help="可見正文機器語言掃描")
    p_leaks.add_argument("file")
    p_leaks.set_defaults(func=_cmd_leaks)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
