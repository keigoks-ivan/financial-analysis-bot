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


# ---------------------------------------------------------------------------
# --assemble PROSE_DIR --tables TABLES_DIR --layout v19  (WP-H2-2, 2026-09-11)
# ---------------------------------------------------------------------------
#
# 新版面（notes/site-internal/dd/_v19_layout_spec_20260911.md）：頁首五張卡＋
# 24 格篩選器資料列＋改變主意三條由 gen_dd_tables.py 的 v19-dashboard.html
# 一次生成（見該檔 render_v19_dashboard_html）；本函式只負責讀 PROSE_DIR 的
# 13 段散文（s1..s12/decision，判斷 agent 或 dd_project.py prose-stub 產出）
# ＋TABLES_DIR 的機械片段（含既有 e2/e3/e6/e9/e10/e12/audit 與新 v19-* 片段），
# 用 scripts/dd_templates/v19.html／v19.css 組成整頁。canonical section id 與
# 舊版面共用（s1..s14/decision/appA/appB/appC/revlog），dd_sections.py 的
# bytes／leaks 掃描不需改動即可涵蓋 v19 產物。
#
# 與 assemble_from_parts()（舊版面）的關鍵差異：
#   - 免費資料區的表格片段大半是 v19 專屬 renderer（v19-spread/v19-roic/
#     v19-segs 等）而非舊 e5/e7/e8——v19 判斷檔的欄位形狀與舊 E5/E7/E8
#     renderer 預期的窄表欄位名不同，沿用舊 renderer 會整表空白（已實測），
#     見 gen_dd_tables.py 該三個新函式的模組註解。
#   - appA/appB/appC/revlog/s14 一律從 TABLES_DIR 讀（gen_dd_tables.py 的
#     v19 分支輸出），不是 PROSE_DIR——這五段是純機械投影，不需要散文 agent
#     或 prose-stub 產出對應檔案（呼應 dd_project.prose_stub() 的既有慣例：
#     「revlog／s14／appA 由 gen_dd_tables.py 機械生成，不在此」）。
#   - 目錄（側欄 <details class="toc">）與頁首五張卡/24格/改變主意都是 v19
#     版面自有元件，不透過舊 TOC_LABELS／`<nav class="dd-toc">`／TOC_SCRIPT。

V19_TEMPLATE_DIR = Path(__file__).resolve().parent / "dd_templates"
V19_HTML_PATH = V19_TEMPLATE_DIR / "v19.html"
V19_CSS_PATH = V19_TEMPLATE_DIR / "v19.css"

V19_TOC_LABELS = {
    "s1": "1　結論", "s2": "2　我押的事", "s3": "3　產業", "s4": "4　商模與致命數字",
    "s5": "5　護城河", "s6": "6　成長", "s7": "7　財務", "s8": "8　最新一季",
    "s9": "9　治理與資本配置", "s10": "10　估值與三種未來", "s11": "11　矛盾裁定",
    "s12": "12　最可能怎麼賠", "decision": "13　怎麼行動", "s14": "14　複審",
    "appA": "附錄 A　擇時", "appB": "附錄 B　證據清單", "appC": "附錄 C　跟上一份比",
    "revlog": "版本紀錄",
}
V19_TOC_ORDER = list(V19_TOC_LABELS.keys())

# 13 段散文（判斷 agent 或 dd_project.py prose-stub 產出，PROSE_DIR/{sid}.html）。
# s14/appA/appB/appC/revlog 是機械段，不在此列（見上方模組註解）。
_ASSEMBLE_ORDER_V19 = [
    "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "decision",
]
_ASSEMBLE_REQUIRED_V19 = list(_ASSEMBLE_ORDER_V19)

# gen_dd_tables.py 的 v19 分支必然輸出的機械段（appB/appC 條件性，不在此列）。
_TABLES_REQUIRED_V19 = [
    "dd-meta.html", "v19-dashboard.html", "v19-appA.html", "v19-revlog.html", "v19-s14.html",
]

# 段 -> 注入規格清單。每筆 {marker, files, folded, label}：files 是
# TABLES_DIR 底下的檔名（可多檔合併成一塊折疊區，缺檔的靜默略過）；
# folded=True 時外面包一層 `<details><summary>{label}</summary>…</details>`
# （規格表「折疊：…」欄逐條對應）；folded=False 的是規格表寫「常駐」的內容
# （§2 的 H1-H3 表、§10 的情境表），直接注入不折疊。標記命名沿用既有
# `<!-- E.. -->` 慣例（render-rules.md §2），v19 新增的標記見
# .claude/skills/stock-analyst/references/v16/render-rules.md 同節的 v19 表。
# audit.html 本身已自帶 `<details class="audit">` 外層（gen_dd_tables.py::
# render_audit_html），folded=False 避免重複包裝。
_V19_MARKER_SPECS = {
    "s2": [
        {"marker": "<!-- E2 -->", "files": ["e2.html"], "folded": False},
    ],
    "s3": [
        {"marker": "<!-- E3 -->", "files": ["e3.html"], "folded": True, "label": "市場空間與利潤池流向"},
    ],
    "s5": [
        {"marker": "<!-- E6 -->", "files": ["e6.html", "v19-spread.html", "v19-threats.html"],
         "folded": True, "label": "對手財務對照與威脅分級"},
        {"marker": "<!-- E7 -->", "files": ["v19-roic.html"], "folded": True, "label": "持續期四檢查點"},
    ],
    "s6": [
        {"marker": "<!-- E8 -->", "files": ["v19-segs.html"], "folded": True, "label": "分部前瞻"},
    ],
    "s7": [
        {"marker": "<!-- E9B -->", "files": ["v19-e9b.html"], "folded": True, "label": "三到四年財務表"},
        {"marker": "<!-- ROE -->", "files": ["v19-roe.html"], "folded": True, "label": "ROE 拆解"},
    ],
    "s8": [
        {"marker": "<!-- QUOTES -->", "files": ["v19-quotes.html"], "folded": True, "label": "法說原話"},
    ],
    "s9": [
        {"marker": "<!-- E10 -->", "files": ["e10.html"], "folded": True, "label": "資本配置四年表"},
    ],
    "s10": [
        {"marker": "<!-- E11 -->", "files": ["e11.html"], "folded": False},
        {"marker": "<!-- STREE -->", "files": ["v19-stree.html"], "folded": True, "label": "終端 EPS 與倍數依據"},
        {"marker": "<!-- PEERS -->", "files": ["v19-peers.html"], "folded": True, "label": "同業對照"},
    ],
    "decision": [
        {"marker": "<!-- E12 -->", "files": ["e12.html", "v19-kill.html", "v19-catalysts.html"],
         "folded": True, "label": "監測與觸發器、致命指標、催化劑"},
        {"marker": "<!-- AUDIT -->", "files": ["audit.html"], "folded": False},
    ],
}


def _v19_gather(tables_dir: Path, spec: dict):
    """依 spec 讀 files（缺檔靜默略過），非空才回傳；folded 時外包一層
    `<details><summary>{label}</summary>…</details>`。"""
    parts = [html_text for html_text in (_read_opt(tables_dir / f) for f in spec["files"]) if html_text]
    if not parts:
        return None
    content = "\n".join(parts)
    if spec.get("folded") and spec.get("label"):
        return f'<details><summary>{spec["label"]}</summary>\n{content}\n</details>\n'
    return content


def _render_shell_v19(meta_block: str, schema: str, title: str, sources: str,
                       dashboard_block: str, sections_html: str, present: set) -> str:
    css = V19_CSS_PATH.read_text(encoding="utf-8")
    tmpl = V19_HTML_PATH.read_text(encoding="utf-8")
    toc_links = "\n".join(
        f'<a href="#{cid}">{V19_TOC_LABELS[cid]}</a>' for cid in V19_TOC_ORDER if cid in present
    )
    html = tmpl
    html = html.replace("<!-- V19:SCHEMA -->", schema)
    html = html.replace("<!-- V19:TITLE -->", title)
    html = html.replace("<!-- V19:DD_META -->", meta_block)
    html = html.replace("<!-- V19:CSS -->", css)
    html = html.replace("<!-- V19:TOC -->", toc_links)
    html = html.replace("<!-- V19:DASHBOARD -->", dashboard_block)
    html = html.replace("<!-- V19:SECTIONS -->", sections_html)
    html = html.replace("<!-- V19:FOOTER -->", FOOTER_TEMPLATE.format(schema=schema, sources=sources))
    html = html.replace("<!-- V19:PRINTBTN -->", PRINTBTN)
    return html


def assemble_from_parts_v19(prose_dir: Path, tables_dir: Path, title=None,
                             sources=None, judgment_path=None) -> str:
    """v19 版面：PROSE_DIR/{sid}.html（s1..s12/decision，13 段）+
    TABLES_DIR/*.html（gen_dd_tables.py 的既有與 v19 片段）-> 完整 v19 版面
    HTML。契約細節見本節開頭的模組註解與
    notes/site-internal/dd/_v19_layout_spec_20260911.md。"""
    missing_prose = [cid for cid in _ASSEMBLE_REQUIRED_V19
                      if not (prose_dir / f"{cid}.html").exists()]
    if missing_prose:
        raise ValueError(f"PROSE_DIR 缺少必要段落（v19）：{', '.join(missing_prose)}")

    missing_tables = [name for name in _TABLES_REQUIRED_V19
                       if not (tables_dir / name).exists()]
    if missing_tables:
        raise ValueError(f"TABLES_DIR 缺少必要檔案（v19）：{', '.join(missing_tables)}")

    meta_block = (tables_dir / "dd-meta.html").read_text(encoding="utf-8")
    meta = dd_sections.dd_meta_json(meta_block) or {}
    schema = meta.get("schema", "v15.0")

    judgment = None
    if judgment_path is not None:
        judgment = json.loads(Path(judgment_path).read_text(encoding="utf-8"))

    if title is None:
        title = _title_from_judgment(judgment) if judgment else ""
    if sources is None:
        sources = ""

    dashboard_block = (tables_dir / "v19-dashboard.html").read_text(encoding="utf-8").strip("\n")

    chunks = []
    present = set()
    for cid in _ASSEMBLE_ORDER_V19:
        chunk = (prose_dir / f"{cid}.html").read_text(encoding="utf-8")
        tag = _outer_tag(chunk)
        for spec in _V19_MARKER_SPECS.get(cid, []):
            insert_html = _v19_gather(tables_dir, spec)
            chunk = _inject_marker_or_append(chunk, spec["marker"], insert_html, tag)
        chunks.append(chunk)
        present.add(cid)

    # 機械段：s14 -> appA -> appB(選填) -> appC(選填) -> revlog（順序見規格
    # 表；appA/appB/appC/revlog 一律讀 TABLES_DIR，見模組註解）。
    chunks.append((tables_dir / "v19-s14.html").read_text(encoding="utf-8"))
    present.add("s14")
    chunks.append((tables_dir / "v19-appA.html").read_text(encoding="utf-8"))
    present.add("appA")
    appB_html = _read_opt(tables_dir / "v19-appB.html")
    if appB_html:
        chunks.append(appB_html)
        present.add("appB")
    appC_html = _read_opt(tables_dir / "v19-appC.html")
    if appC_html:
        chunks.append(appC_html)
        present.add("appC")
    chunks.append((tables_dir / "v19-revlog.html").read_text(encoding="utf-8"))
    present.add("revlog")

    sections_html = "\n\n".join(chunks)
    return _render_shell_v19(meta_block, schema, title, sources, dashboard_block, sections_html, present)


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
    layout = getattr(args, "layout", None) or "legacy"
    if layout not in ("legacy", "v19"):
        print(f"render_dd: --layout 只接受 legacy 或 v19，收到 {layout!r}", file=sys.stderr)
        sys.exit(2)
    assemble_fn = assemble_from_parts_v19 if layout == "v19" else assemble_from_parts
    try:
        html = assemble_fn(
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
    ap.add_argument("--assemble", metavar="PROSE_DIR", help="v16/v19 模式：組裝 prose/ 目錄（需搭配 --tables）")
    ap.add_argument("--tables", metavar="TABLES_DIR", help="v16/v19 模式：gen_dd_tables.py 產物目錄")
    ap.add_argument("--layout", choices=["legacy", "v19"], default="legacy",
                     help="--assemble 用哪套版面模板：legacy（預設，既有 dd_template/dd.css）或 v19"
                          "（scripts/dd_templates/v19.html+v19.css，見 WP-H2-2）")
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
