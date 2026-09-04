#!/usr/bin/env python3
"""render_dd.py — BODY <-> full v15.2 DD HTML assembler.

Two directions (see notes/site-internal/dd/_v15_2_design_spec_20260903.md §2.2):

  python3 scripts/render_dd.py BODY -o docs/dd/DD_{T}_{D}.html [--no-postprocess]
      Assemble a writer-authored BODY file (dd-meta + TITLE/SOURCES comments +
      dashboard + <section>/<details> ids s1..s14/decision/s85/appA/appB/
      revlog/sources) into a full standalone report: <head> (charset/robots/
      viewport/dd-schema-version/title/dd-meta/inlined dd.css) + <body> +
      dashboard + an auto-generated <nav class="dd-toc"> + the sections +
      footer + printbtn + toc-expand <script>. Then runs the three
      post-process injectors (site_nav / inject_report_primer /
      inject_dd_livebar) unless --no-postprocess.

      <head> also carries <meta name="dd-render" content="render_dd-v15.2">
      — a provenance marker meaning "this exact file passed through
      render_dd.py" (deliberately NOT "stock-analyst v..." / "DD Schema v..."
      text, so it can never collide with verify_dd_math.py's check D version-
      stamp regexes). qc.py's leak check (check 6) uses its presence to tell
      a delta-refresh (`cp` of an old report to a new date, then patched —
      inherits that old file's pre-existing leaks, and was never itself
      rendered fresh) apart from a brand-new render_dd.py-produced report, so
      only the latter gets the "whole file added -> leaks are errors" gate.

  python3 scripts/render_dd.py --to-body FILE -o BODY
      Reverse: strip an existing full HTML report down to a BODY file (drops
      head/style/nav/primer/toc/printbtn/toc-script/livebar; adds the TITLE/
      SOURCES comments). Legacy files whose sections aren't already wrapped in
      canonical <section id="sN">/<details id="appA"> tags (e.g. SE's bare
      <h2 id="s1"> or its <details id="appxA"> appendix) are canonicalized
      during this pass.

  python3 scripts/render_dd.py --check FILE
      Regression check: --to-body FILE in memory, render it back, and diff
      dd_sections.readable_text() of the original vs. the round-tripped
      version. Informational — always exits 0; read the diff.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_sections  # noqa: E402

TEMPLATE_DIR = Path(__file__).resolve().parent / "dd_template"
CSS_PATH = TEMPLATE_DIR / "dd.css"

TOC_LABELS = {
    "s1": "§1 結論", "s2": "§2 論點", "s3": "§3 產業", "s4": "§4 商模門檻",
    "s5": "§5 護城河", "s6": "§6 成長", "s7": "§7 財務", "s8": "§8 財報",
    "s85": "§8.5 文獻", "s9": "§9 治理", "s10": "§10 估值", "s11": "§11 矛盾",
    "s12": "§12 pre-mortem", "decision": "§13 決策", "s14": "§14 複審",
    "appA": "附錄 A 擇時", "appB": "附錄 B 循環讀數",
}
TOC_ORDER = list(TOC_LABELS.keys())

FOOTER_TEMPLATE = (
    '<p class="small" style="margin-top:30px;border-top:1px solid #e2e8f0;'
    'padding-top:12px">本報告由 stock-analyst {schema} 生成。資料來源：{sources}</p>'
)
PRINTBTN = '<button class="printbtn" onclick="window.print()">列印為 PDF</button>'
TOC_SCRIPT = """<script>
document.querySelectorAll('.dd-toc a').forEach(function(a){
  a.addEventListener('click',function(e){
    var t=document.querySelector(this.getAttribute('href'));
    if(t&&t.tagName==='DETAILS'){t.open=true;}
  });
});
</script>"""

_GUARD_TOKENS = ("<head", "<style", "imq-nav", "dd-toc")


def _body_guard(raw: str):
    """Return the offending token if BODY looks like it already has a full
    document skeleton (head/style/nav/toc), else None."""
    for tok in _GUARD_TOKENS:
        if tok in raw:
            return tok
    return None


# ---------------------------------------------------------------------------
# --to-body
# ---------------------------------------------------------------------------

def _canonicalize_chunk(chunk: str, mk: dict) -> str:
    """Ensure an extracted section chunk carries its canonical id.

    via="attr": already has id="<canonical id>" verbatim -> no change.
    via="text", tag=="h2": wrapperless (e.g. legacy <h2 id="s1"> with no
      enclosing <section>) -> wrap it.
    via="text", tag=="details": has a *different* id attr (e.g. SE's
      id="appxA" located via its <summary>附錄A</summary> text) -> rewrite
      just that attribute to the canonical id.
    """
    cid = mk["id"]
    if mk["via"] == "attr":
        return chunk
    if mk["tag"] == "h2":
        return f'<section id="{cid}">\n{chunk}\n</section>'
    if mk["tag"] == "details":
        new_chunk, n = re.subn(
            r'(<details\b[^>]*?)\bid=["\'][^"\']*["\']',
            lambda m: m.group(1) + f'id="{cid}"',
            chunk, count=1,
        )
        if n == 0:
            new_chunk = re.sub(r"^<details\b", f'<details id="{cid}"', chunk, count=1)
        return new_chunk
    return chunk


def _dashboard_or_fallback(html: str) -> str:
    """Extract the dashboard region; for files with no <div class="topbar">
    (e.g. SE), fall back to "everything between the end of nav/primer and the
    first section marker", stripping any embedded <nav class="dd-toc"> so it
    isn't duplicated (a fresh one is auto-generated at render time)."""
    span = dd_sections.dashboard_span(html)
    if span is not None:
        return html[span[0]:span[1]]

    markers = dd_sections.split_sections(html)
    if not markers:
        return ""
    end = markers[0]["start"]

    m = re.search(r"<!-- PLAIN_PRIMER_END -->", html)
    if m:
        start = m.end()
    else:
        m = re.search(r"</header>", html)
        if m:
            start = m.end()
        else:
            m = re.search(r"<body[^>]*>", html)
            start = m.end() if m else 0

    chunk = html[start:end]
    chunk = re.sub(r'<nav\s+class="dd-toc"[^>]*>.*?</nav>', "", chunk, flags=re.DOTALL)
    return chunk.strip("\n")


def _canonical_sections_block(html: str, markers) -> str:
    """The full contiguous span from the first marker's start to the last
    marker's end, with only the non-canonical markers' *own* opening tags
    rewritten in place.

    Using the whole span (rather than joining each marker's own chunk with
    separators) matters because sibling content can sit BETWEEN two markers
    without being any marker's own content — e.g. NVDA carries a bare
    <p class="note">附錄B...不適用，整段省略。</p> between </details> (appA)
    and <section id="revlog">, which belongs to neither marker. Chunk-joining
    would silently drop it; slicing the full span does not.
    """
    base = markers[0]["start"]
    end = markers[-1]["end"]
    text = html[base:end]
    for mk in reversed(markers):
        if mk["via"] == "attr":
            continue
        rel_start = mk["start"] - base
        rel_end = mk["end"] - base
        chunk = text[rel_start:rel_end]
        text = text[:rel_start] + _canonicalize_chunk(chunk, mk) + text[rel_end:]
    return text


def to_body(html: str) -> str:
    meta_span = dd_sections.dd_meta_span(html)
    if meta_span is None:
        raise ValueError("找不到 <script id=\"dd-meta\"> 區塊，無法轉 BODY")
    meta_block = html[meta_span[0]:meta_span[1]]

    title_m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    title_text = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""

    src_m = re.search(r"資料來源[:：]\s*(.*?)</p>", html, re.DOTALL)
    sources_text = re.sub(r"\s+", " ", src_m.group(1)).strip() if src_m else ""

    dashboard_block = _dashboard_or_fallback(html)

    markers = dd_sections.split_sections(html)
    sections_block = _canonical_sections_block(html, markers) if markers else ""

    parts = [
        meta_block,
        f"<!-- TITLE: {title_text} -->",
        f"<!-- SOURCES: {sources_text} -->",
    ]
    if dashboard_block.strip():
        parts.append(dashboard_block.strip("\n"))
    if sections_block.strip():
        parts.append(sections_block)
    return "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# render (BODY -> full HTML)
# ---------------------------------------------------------------------------

def _render_shell(meta_block: str, schema: str, title: str, sources: str,
                   dash_block: str, sections_block: str) -> str:
    """Shared tail: given the four already-resolved pieces (dd-meta script
    block, schema string, TITLE text, SOURCES text, dashboard fragment,
    sections fragment), build the full standalone HTML document. Used by
    both single-file `assemble()` (BODY -> full HTML) and
    `assemble_from_parts()` (v16 prose/+tables/ -> full HTML) so the two
    modes share one <head>/<nav>/footer/printbtn/toc-script pipeline (v16
    WP1e requirement: "組好後走同一條既有 head／toc／footer／post-process
    管線")."""
    markers = dd_sections.split_sections(sections_block)
    if not markers:
        raise ValueError("找不到任何 canonical section id（s1..s14/decision/appA/appB/...）")

    present = {m["id"] for m in markers}
    toc_links = "".join(
        f'<a href="#{cid}">{TOC_LABELS[cid]}</a>' for cid in TOC_ORDER if cid in present
    )
    toc_html = f'<nav class="dd-toc">\n{toc_links}\n</nav>'

    css = CSS_PATH.read_text(encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="dd-schema-version" content="{schema}">
<meta name="dd-render" content="render_dd-v15.2">
<title>{title}</title>
{meta_block}
<style>
{css}
</style>
</head>
<body>
{dash_block}

{toc_html}

{sections_block}

{FOOTER_TEMPLATE.format(schema=schema, sources=sources)}

{PRINTBTN}
</div>
{TOC_SCRIPT}
</body>
</html>
"""
    return html


def assemble(body: str) -> str:
    guard = _body_guard(body)
    if guard is not None:
        raise ValueError(f"BODY 已含 {guard!r}，看起來是完整 HTML 而非 BODY，拒絕組裝")

    meta_span = dd_sections.dd_meta_span(body)
    if meta_span is None:
        raise ValueError("BODY 缺少 <script id=\"dd-meta\"> 區塊")
    meta_block = body[meta_span[0]:meta_span[1]]
    meta = dd_sections.dd_meta_json(body) or {}
    schema = meta.get("schema", "v15.0")

    rest = body[meta_span[1]:]

    title_m = re.search(r"<!--\s*TITLE:\s*(.*?)\s*-->", rest, re.DOTALL)
    title = title_m.group(1).strip() if title_m else ""
    if title_m:
        rest = rest[:title_m.start()] + rest[title_m.end():]

    src_m = re.search(r"<!--\s*SOURCES:\s*(.*?)\s*-->", rest, re.DOTALL)
    sources = src_m.group(1).strip() if src_m else ""
    if src_m:
        rest = rest[:src_m.start()] + rest[src_m.end():]

    rest = rest.strip("\n")

    markers = dd_sections.split_sections(rest)
    if not markers:
        raise ValueError("BODY 找不到任何 canonical section id（s1..s14/decision/appA/appB/...）")

    dash_block = rest[:markers[0]["start"]].strip("\n")
    sections_block = rest[markers[0]["start"]:].strip("\n")

    return _render_shell(meta_block, schema, title, sources, dash_block, sections_block)


# ---------------------------------------------------------------------------
# --assemble PROSE_DIR --tables TABLES_DIR  (v16 mode, WP1e)
# ---------------------------------------------------------------------------

# Canonical prose ids in document order. s85/appB/sources stay conditional
# (matches html-output.md); "s1–s14、decision、appA、revlog 缺任一 → FAIL"
# per the WP1e brief.
_ASSEMBLE_ORDER = [
    "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s85", "s9", "s10",
    "s11", "s12", "decision", "s14", "appA", "appB", "revlog", "sources",
]
_ASSEMBLE_REQUIRED = [
    "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10",
    "s11", "s12", "decision", "s14", "appA", "revlog",
]
# gen_dd_tables.py's always-written outputs; e11.html (dd_scenario.py
# --html product) and audit.html (only when decision_out.audit_rows is
# non-empty) are conditional, so not required here.
_TABLES_REQUIRED = [
    "dd-meta.html", "dashboard.html", "e2.html", "e12.html", "appA-table.html",
    "e3.html", "e5.html", "e6.html", "e7.html", "e8.html", "e9.html", "e10.html",
]


def _read_opt(path: Path):
    return path.read_text(encoding="utf-8") if path.exists() else None


def _outer_tag(chunk: str):
    """First real tag name in a prose fragment (leading HTML comments
    skipped) — used to find that fragment's own closing tag for
    append-fallback injection."""
    m = re.match(r"\s*(?:<!--.*?-->\s*)*<(\w+)\b", chunk, re.DOTALL)
    return m.group(1) if m else None


def _inject_marker_or_append(chunk: str, marker: str, insert_html, tag) -> str:
    """Splice `insert_html` at `marker` if present; else append it just
    before the chunk's own closing tag (still inside the outer element).
    No-op (marker stripped) when insert_html is falsy/None."""
    if marker in chunk:
        return chunk.replace(marker, insert_html or "", 1)
    if not insert_html:
        return chunk
    if not tag:
        return chunk + insert_html
    idx = chunk.rfind(f"</{tag}>")
    if idx == -1:
        return chunk + insert_html
    return chunk[:idx] + insert_html + chunk[idx:]


def _inject_e2(chunk: str, e2_html, tag) -> str:
    """E2 (§2.B 三個核心假設表) has its own fallback anchor: right after
    s2's first "B｜" <h3> heading, not at the section's tail."""
    if "<!-- E2 -->" in chunk:
        return chunk.replace("<!-- E2 -->", e2_html or "", 1)
    if not e2_html:
        return chunk
    m = re.search(r"<h3[^>]*>\s*B｜.*?</h3>", chunk, re.DOTALL)
    if m:
        idx = m.end()
        return chunk[:idx] + "\n" + e2_html + chunk[idx:]
    # no marker, no "B｜" heading found -> fall back to tail-append like
    # every other injection point.
    return _inject_marker_or_append(chunk, "\x00no-such-marker\x00", e2_html, tag)


def _title_from_judgment(j: dict) -> str:
    meta = j.get("meta") or {}
    ticker = meta.get("ticker") or ""
    company = meta.get("company_name") or ticker
    date = meta.get("date") or ""
    verdict = (j.get("decision_out") or {}).get("verdict") or ""
    return f"DD {company}（{ticker}）— {date}（統一裁決：{verdict}）"


def assemble_from_parts(prose_dir: Path, tables_dir: Path, title=None,
                         sources=None, judgment_path=None) -> str:
    """v16 mode: PROSE_DIR/{sid}.html (writer-authored prose — each file is
    that section's full outer element, e.g. `<section id="s5">…</section>`)
    + TABLES_DIR/*.html (gen_dd_tables.py mechanical output) -> full
    standalone HTML, via the same _render_shell tail as single-file
    assemble(). Table injection points: e2.html into s2 (after the "B｜"
    <h3>, or at `<!-- E2 -->`), e3.html into s3 (`<!-- E3 -->` or tail),
    e5.html/e6.html/e7.html into s5 (`<!-- E5 -->`/`<!-- E6 -->`/`<!-- E7 -->`
    or tail, in that order), e8.html into s6 (`<!-- E8 -->` or tail), e9.html
    into s7 (`<!-- E9 -->` or tail), e10.html into s9 (`<!-- E10 -->` or
    tail), e11.html into s10 (`<!-- E11 -->` or tail), audit.html then
    e12.html into decision (`<!-- AUDIT -->`/`<!-- E12 -->` or tail, audit
    first so a double-fallback still lands before E12), appA-table.html into
    appA (`<!-- APPA_TABLE -->` or tail)."""
    missing_prose = [cid for cid in _ASSEMBLE_REQUIRED
                      if not (prose_dir / f"{cid}.html").exists()]
    if missing_prose:
        raise ValueError(f"PROSE_DIR 缺少必要段落：{', '.join(missing_prose)}")

    missing_tables = [name for name in _TABLES_REQUIRED
                       if not (tables_dir / name).exists()]
    if missing_tables:
        raise ValueError(f"TABLES_DIR 缺少必要檔案：{', '.join(missing_tables)}")

    meta_block = (tables_dir / "dd-meta.html").read_text(encoding="utf-8")
    meta = dd_sections.dd_meta_json(meta_block) or {}
    schema = meta.get("schema", "v15.0")

    judgment = None
    if judgment_path is not None:
        judgment = json.loads(Path(judgment_path).read_text(encoding="utf-8"))

    if title is None:
        title = _title_from_judgment(judgment) if judgment else ""
    if sources is None:
        # judgment.json 目前無 sources 欄位（見 dd_schema/judgment.schema.json）
        # -- 只能靠 --sources 旗標帶入，這裡留空不捏造。
        sources = ""

    dash_block = (tables_dir / "dashboard.html").read_text(encoding="utf-8").strip("\n")

    e2_html = _read_opt(tables_dir / "e2.html")
    e3_html = _read_opt(tables_dir / "e3.html")
    e5_html = _read_opt(tables_dir / "e5.html")
    e6_html = _read_opt(tables_dir / "e6.html")
    e7_html = _read_opt(tables_dir / "e7.html")
    e8_html = _read_opt(tables_dir / "e8.html")
    e9_html = _read_opt(tables_dir / "e9.html")
    e10_html = _read_opt(tables_dir / "e10.html")
    e11_html = _read_opt(tables_dir / "e11.html")
    e12_html = _read_opt(tables_dir / "e12.html")
    audit_html = _read_opt(tables_dir / "audit.html")
    appA_table_html = _read_opt(tables_dir / "appA-table.html")

    chunks = []
    for cid in _ASSEMBLE_ORDER:
        p = prose_dir / f"{cid}.html"
        if not p.exists():
            continue
        chunk = p.read_text(encoding="utf-8")
        tag = _outer_tag(chunk)
        if cid == "s2":
            chunk = _inject_e2(chunk, e2_html, tag)
        elif cid == "s3":
            chunk = _inject_marker_or_append(chunk, "<!-- E3 -->", e3_html, tag)
        elif cid == "s5":
            chunk = _inject_marker_or_append(chunk, "<!-- E5 -->", e5_html, tag)
            chunk = _inject_marker_or_append(chunk, "<!-- E6 -->", e6_html, tag)
            chunk = _inject_marker_or_append(chunk, "<!-- E7 -->", e7_html, tag)
        elif cid == "s6":
            chunk = _inject_marker_or_append(chunk, "<!-- E8 -->", e8_html, tag)
        elif cid == "s7":
            chunk = _inject_marker_or_append(chunk, "<!-- E9 -->", e9_html, tag)
        elif cid == "s9":
            chunk = _inject_marker_or_append(chunk, "<!-- E10 -->", e10_html, tag)
        elif cid == "s10":
            chunk = _inject_marker_or_append(chunk, "<!-- E11 -->", e11_html, tag)
        elif cid == "decision":
            chunk = _inject_marker_or_append(chunk, "<!-- AUDIT -->", audit_html, tag)
            chunk = _inject_marker_or_append(chunk, "<!-- E12 -->", e12_html, tag)
        elif cid == "appA":
            chunk = _inject_marker_or_append(chunk, "<!-- APPA_TABLE -->", appA_table_html, tag)
        chunks.append(chunk)

    sections_block = "\n\n".join(chunks)
    return _render_shell(meta_block, schema, title, sources, dash_block, sections_block)


def _direct_site_nav(out_path: Path):
    import site_nav
    return site_nav.process(out_path)


def _direct_primer(out_path: Path):
    import inject_report_primer
    if hasattr(inject_report_primer, "inject_one"):
        return inject_report_primer.inject_one(out_path)
    action, _ = inject_report_primer.process_file(  # pragma: no cover - defensive
        out_path, "dd", inject_report_primer.dd_template_for, dry_run=False
    )
    return action


def _direct_livebar(out_path: Path):
    import inject_dd_livebar
    if hasattr(inject_dd_livebar, "inject_one"):
        return inject_dd_livebar.inject_one(str(out_path))
    return inject_dd_livebar.process(str(out_path), False)  # pragma: no cover


_DIRECT_FN = {"site_nav": _direct_site_nav, "primer": _direct_primer, "livebar": _direct_livebar}

# None of the three scripts expose a real single-file CLI (site_nav.py's
# main() only sweeps the whole docs/ tree via --check; we are not allowed to
# add one — "不准改 site_nav.py 本身"), so the fallback calls the same
# single-file function directly via `python3.12 -c`, in-process import, no
# CLI parsing involved.
_FALLBACK_SNIPPET = {
    "site_nav": (
        "import site_nav\n"
        "from pathlib import Path\n"
        "print(site_nav.process(Path({path!r})))\n"
    ),
    "primer": (
        "import inject_report_primer\n"
        "from pathlib import Path\n"
        "print(inject_report_primer.inject_one(Path({path!r})))\n"
    ),
    "livebar": (
        "import inject_dd_livebar\n"
        "print(inject_dd_livebar.inject_one({path!r}))\n"
    ),
}

# checked in this order; first one that exists (absolute paths) / resolves on
# PATH (bare name) wins.
_FALLBACK_PY_CANDIDATES = [
    "/tmp/ddvenv/bin/python",
    "/opt/homebrew/bin/python3.12",
    "python3.12",
]


def _find_fallback_python():
    for cand in _FALLBACK_PY_CANDIDATES:
        if cand.startswith("/"):
            p = Path(cand)
            if p.is_file() and os.access(str(p), os.X_OK):
                return cand
        else:
            found = shutil.which(cand)
            if found:
                return found
    return None


def _run_fallback(name: str, out_path: Path) -> str:
    python_bin = _find_fallback_python()
    if python_bin is None:
        print(f"WARN: post-process {name} skipped（需 py3.12）", file=sys.stderr)
        return "skipped(no-py312)"
    code = (
        f"import sys; sys.path.insert(0, {str(Path(__file__).resolve().parent)!r})\n"
        + _FALLBACK_SNIPPET[name].format(path=str(out_path))
    )
    try:
        r = subprocess.run(
            [python_bin, "-c", code], capture_output=True, text=True, timeout=60
        )
    except Exception as e:  # interpreter vanished mid-run, etc.
        print(f"WARN: post-process {name} skipped（fallback 執行失敗：{e}）", file=sys.stderr)
        return "skipped(fallback-error)"
    if r.returncode != 0:
        tail = (r.stderr or "").strip().splitlines()[-1:] or ["(no stderr)"]
        print(f"WARN: post-process {name} skipped（{python_bin} 執行失敗：{tail[0]}）", file=sys.stderr)
        return "skipped(fallback-failed)"
    return f"ok-via-{python_bin}:{r.stdout.strip()}"


def _run_step(name: str, out_path: Path) -> str:
    try:
        return _DIRECT_FN[name](out_path)
    except (SyntaxError, ImportError):
        # this interpreter can't even parse the target module (e.g. site_nav.py
        # needs py3.12's relaxed f-string grammar) -> fall back to a subprocess
        # under a newer interpreter rather than failing the whole render.
        return _run_fallback(name, out_path)


def _postprocess(out_path: Path):
    return {name: _run_step(name, out_path) for name in ("site_nav", "primer", "livebar")}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cmd_render(args):
    body = Path(args.body).read_text(encoding="utf-8")
    try:
        html = assemble(body)
    except ValueError as e:
        print(f"render_dd: {e}", file=sys.stderr)
        sys.exit(2)
    # resolve to absolute: site_nav.ROOT is absolute and Path.relative_to()
    # is purely lexical (no cwd-awareness), so a relative -o here would make
    # site_nav.process() raise "not in the subpath" even for a real docs/dd/
    # path — this is our calling convention to fix, not site_nav.py's job.
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"寫入 {out_path}（{len(html.encode('utf-8'))}B）")
    if not args.no_postprocess:
        report = _postprocess(out_path)
        for k, v in report.items():
            print(f"  post-process {k}: {v}")
    sys.exit(0)


def _cmd_to_body(args):
    html = Path(args.to_body).read_text(encoding="utf-8")
    try:
        body = to_body(html)
    except ValueError as e:
        print(f"render_dd: {e}", file=sys.stderr)
        sys.exit(2)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(f"寫入 {out_path}（{len(body.encode('utf-8'))}B）")
    sys.exit(0)


def _cmd_check(args):
    path = Path(args.check)
    original = path.read_text(encoding="utf-8")
    try:
        body = to_body(original)
        rendered = assemble(body)
    except ValueError as e:
        print(f"❌ {path}: {e}", file=sys.stderr)
        sys.exit(2)

    orig_text = dd_sections.readable_text(original)
    new_text = dd_sections.readable_text(rendered)

    if orig_text == new_text:
        print(f"✅ {path}: --check 可見文字完全一致")
        sys.exit(0)

    diff = list(difflib.unified_diff(
        orig_text.splitlines(), new_text.splitlines(),
        fromfile="original", tofile="round-tripped", lineterm="", n=1,
    ))
    changed = sum(1 for ln in diff if ln.startswith(("+", "-")) and not ln.startswith(("+++", "---")))
    print(f"⚠️  {path}: 可見文字有差異（±{changed} 行，diff 標頭另計）")
    for ln in diff:
        print(ln)
    sys.exit(0)


def _cmd_assemble(args):
    if not args.output:
        print("render_dd: --assemble 需要搭配 -o OUT", file=sys.stderr)
        sys.exit(2)
    if not args.tables:
        print("render_dd: --assemble 需要搭配 --tables DIR", file=sys.stderr)
        sys.exit(2)
    try:
        html = assemble_from_parts(
            Path(args.assemble), Path(args.tables),
            title=args.title, sources=args.sources,
            judgment_path=Path(args.judgment) if args.judgment else None,
        )
    except ValueError as e:
        print(f"render_dd: {e}", file=sys.stderr)
        sys.exit(2)
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"寫入 {out_path}（{len(html.encode('utf-8'))}B）")
    if not args.no_postprocess:
        report = _postprocess(out_path)
        for k, v in report.items():
            print(f"  post-process {k}: {v}")
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("body", nargs="?", help="BODY 檔路徑（render 模式）")
    ap.add_argument("-o", "--output", help="輸出檔路徑")
    ap.add_argument("--no-postprocess", action="store_true", help="跳過 nav/primer/livebar 注入")
    ap.add_argument("--to-body", metavar="FILE", help="既有完整 HTML 檔 -> BODY")
    ap.add_argument("--check", metavar="FILE", help="回歸測試：既有檔 to-body 再 render，比對可見文字")
    ap.add_argument("--assemble", metavar="PROSE_DIR", help="v16 模式：組裝 prose/ 目錄（需搭配 --tables）")
    ap.add_argument("--tables", metavar="TABLES_DIR", help="v16 模式：gen_dd_tables.py 產物目錄")
    ap.add_argument("--title", help="v16 模式：TITLE 註解內容（覆蓋 judgment 推導）")
    ap.add_argument("--sources", help="v16 模式：SOURCES 註解內容（judgment.json 無此欄位，建議手動帶）")
    ap.add_argument("--judgment", metavar="JUDGMENT.json", help="v16 模式：judgment.json 路徑，用於推導 TITLE")
    args = ap.parse_args()

    if args.assemble:
        _cmd_assemble(args)
    elif args.check:
        _cmd_check(args)
    elif args.to_body:
        if not args.output:
            print("render_dd: --to-body 需要搭配 -o BODY_OUT", file=sys.stderr)
            sys.exit(2)
        _cmd_to_body(args)
    elif args.body:
        if not args.output:
            print("render_dd: 需要 -o OUT", file=sys.stderr)
            sys.exit(2)
        _cmd_render(args)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
