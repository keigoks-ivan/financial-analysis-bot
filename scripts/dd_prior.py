#!/usr/bin/env python3
"""dd_prior.py — stock-analyst v16 Stage 0d: zero-LLM evidence-pack extractor.

Merges four previously-manual/LLM-mediated inputs into one JSON fragment
that `dd_evidence.py merge` (WP1a, written in parallel) can fold into
evidence.json:

  prior_dd     — QC-17/18 three-block extraction from the latest existing
                 DD_{TICKER}_*.html (revlog / §2.B H1-H3 + §2.C R1-R3 / E12
                 trigger table), plus inception_dd and dd_12m_ago pointers.
                 NEVER loads the whole prior HTML into the output (QC-17).
  ledger       — knowledge/q.py's decision history + usernote + falsifiers
                 for this ticker, read from the derived JSON files
                 (knowledge/decisions.jsonl, graph.json, settlement.json,
                 falsifiers.json) after invoking `q.py TICKER` once to
                 trigger its own staleness/auto-rebuild logic.
  canonical_id — QC-52 Stage-1 "facts only" excerpt from the ticker's
                 canonical industry ID (mechanics/appendix for v3+/v4 IDs,
                 supply/demand heading text for legacy v1.x/v2.x IDs).
                 Decision-layer sections (summary/thesis/debates, or legacy
                 §0/§4/§5) are never read.
  transcripts  — must-read/optional-read file lists from
                 ~/scripts/koyfin-downloader/transcripts_for_dd.py, trimmed
                 to "most recent 4 quarters + <=1 high-signal optional".

Zero LLM, stdlib only (Python 3.9-compatible; run with /tmp/ddvenv/bin/python
for consistency with the rest of the v16 WP1 scripts). Every block degrades
to a `status` field ("unavailable"/"gap") on failure rather than raising —
this script must never block report generation.

Usage:
    dd_prior.py TICKER [--date YYYYMMDD] [--out PART.json] [--drive-ticker T]

    TICKER          normalized or raw form (2330.TW / 2330TW both accepted)
    --date          the NEW report's date; prior_dd picks the latest existing
                     DD strictly before this date. Omitted -> latest overall.
    --out           write the JSON fragment to this path instead of stdout.
    --drive-ticker  raw Koyfin-Drive-folder ticker form (e.g. "2330.TW") when
                     it differs from TICKER; defaults to TICKER as given.

See notes/site-internal/dd/_v16_design_spec_20260903.md §2 Stage 0(0d)/§3.1
and .claude/skills/stock-analyst/SKILL.md QC-17/QC-18/QC-52 for the rules
this script mechanizes.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import dd_sections  # sibling module in scripts/ — sys.path[0] already covers this
import dd_meta_reader

REPO_ROOT = Path(__file__).resolve().parent.parent
DD_DIR = REPO_ROOT / "docs" / "dd"
ID_DIR = REPO_ROOT / "docs" / "id"
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"
TRANSCRIPTS_SCRIPT = Path.home() / "scripts" / "koyfin-downloader" / "transcripts_for_dd.py"

TEXT_CAP = 4000       # per-block plain-text cap (chars) for prior_dd sub-blocks
ID_FACTS_CAP = 8000    # per-section cap (chars) for canonical_id facts


# ---------------------------------------------------------------------------
# small shared text helpers (reuse dd_sections' private table/tag utilities —
# same module, same repo, documented as importable for internal scripts)
# ---------------------------------------------------------------------------

def _chunk_to_text(chunk: str, cap: int = TEXT_CAP) -> str:
    chunk = re.sub(r"<script\b.*?</script>", "", chunk, flags=re.DOTALL | re.IGNORECASE)
    chunk = re.sub(r"<style\b.*?</style>", "", chunk, flags=re.DOTALL | re.IGNORECASE)
    chunk = dd_sections._flatten_tables(chunk)
    chunk = dd_sections._tags_to_text(chunk)
    chunk = re.sub(r"[ \t]+", " ", chunk)
    chunk = re.sub(r"\n{3,}", "\n\n", chunk).strip()
    return chunk[:cap]


def normalize_ticker(raw: str) -> str:
    return raw.strip().upper().replace(".", "")


def _version_tuple(s):
    m = re.match(r"v?(\d+)\.(\d+)", s or "")
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)))


# ---------------------------------------------------------------------------
# prior_dd
# ---------------------------------------------------------------------------

_FNAME_RE = re.compile(r"^DD_(?P<ticker>.+)_(?P<date>\d{8})\.html$")

# v16 修法 5（judgment-rules.md §12 item 3b, QC-49 執行細則）：Stage 1 判斷層
# 逐欄比對 prior_meta 與本次 decision_inputs/情境六欄/rearm/val/runway_post_y5，
# 任一不同須在 contradictions[] 有獨立條目。固定清單，語意見設計稿 §5.5。
DRIFT_WATCH = [
    "dca_verdict", "dca_role", "signal", "val", "ma", "trap",
    "moat_trend", "runway_post_y5", "asym_ratio", "ev5y_pct",
    "irr_base_pct", "max_dd_pct", "bull_5y_price", "bear_5y_price",
    "p_bull_pct", "p_bear_pct", "rearm_trigger", "price_at_dd",
    "archetype", "cycle_position",
]


def find_dd_files(ticker_norm: str):
    """[(YYYYMMDD, Path), ...] ascending by date, for this ticker only."""
    out = []
    for f in DD_DIR.glob(f"DD_{ticker_norm}_*.html"):
        m = _FNAME_RE.match(f.name)
        if m and m.group("ticker") == ticker_norm:
            out.append((m.group("date"), f))
    out.sort(key=lambda x: x[0])
    return out


def _read(f: Path) -> str:
    return f.read_text(encoding="utf-8", errors="ignore")


def extract_revlog(html: str) -> dict:
    span = None
    for mk in dd_sections.split_sections(html):
        if mk["id"] == "revlog":
            span = (mk["start"], mk["end"])
            break
    if span is None:
        m = re.search(r"<h[23]\b[^>]*>\s*版本修訂紀錄\s*</h[23]>", html)
        if not m:
            return {"status": "unavailable"}
        end_m = re.search(r"<h[23]\b|<!--\s*DD_LIVEBAR|</body", html[m.end():])
        end = m.end() + end_m.start() if end_m else len(html)
        span = (m.start(), end)
    return {"status": "ok", "text": _chunk_to_text(html[span[0]:span[1]])}


def _parse_generic_table(table_html: str):
    """[{"headers":[...], "vals":[...]}, ...] for data rows (header row excluded)."""
    rows = re.findall(r"<tr\b.*?</tr>", table_html, re.S | re.I)
    if len(rows) < 2:
        return None
    header_cells = re.findall(r"<t[hd]\b.*?</t[hd]>", rows[0], re.S | re.I)
    headers = [re.sub(r"\s+", " ", dd_sections._tags_to_text(c)).strip() for c in header_cells]
    out = []
    for r in rows[1:]:
        cells = re.findall(r"<t[hd]\b.*?</t[hd]>", r, re.S | re.I)
        if not cells:
            continue
        vals = [re.sub(r"\s+", " ", dd_sections._tags_to_text(c)).strip() for c in cells]
        out.append({"headers": headers, "vals": vals})
    return out or None


def _rows_to_structured(parsed_rows, id_prefix: str):
    out = []
    for row in parsed_rows:
        headers, vals = row["headers"], row["vals"]
        rid = vals[0] if vals else None
        text = vals[1] if len(vals) > 1 else None
        columns = {}
        for i, h in enumerate(headers):
            if i < len(vals) and i >= 2:
                columns[h or f"col{i}"] = vals[i]
        out.append({"id": rid, "text": text, "columns": columns})
    # sanity: at least one row id should start with id_prefix, else caller
    # should treat this as a mis-parse and fall back to raw text.
    if not any((r["id"] or "").upper().startswith(id_prefix) for r in out):
        return None
    return out


def _heading_span_by_text(html: str, tag_pattern: str, contains: str):
    """First <tag>...</tag> (tag matching tag_pattern, e.g. "h3" or "h[23]")
    whose flattened text contains `contains` — robust to inline <em>/<strong>
    breaking a naive [^<]* regex (e.g. AVGO's '<h2>供給側：<em>...</em>...')."""
    for m in re.finditer(r"<(" + tag_pattern + r")\b[^>]*>(.*?)</\1>", html, re.S | re.I):
        if contains in dd_sections._tags_to_text(m.group(2)):
            return m
    return None


def _capture_after_heading(html: str, heading_pat: str, end_pat: str = r"<h[23]\b"):
    m = re.search(heading_pat, html)
    if not m:
        return None
    return _capture_after_match(html, m, end_pat)


def _capture_after_match(html: str, m, end_pat: str = r"<h[23]\b"):
    if m is None:
        return None
    end_m = re.search(end_pat, html[m.end():])
    end = m.end() + end_m.start() if end_m else min(m.end() + 20000, len(html))
    return html[m.start():end]


def extract_hr_tables(html: str) -> dict:
    """§2.B H1-H3 (核心假設) + §2.C R1-R3 (風險) — structured if parseable,
    else raw text of the captured chunk. Independent per block (H can
    succeed while R degrades, or vice versa)."""
    result = {}

    h_chunk = _capture_after_match(html, _heading_span_by_text(html, "h3", "核心假設"))
    if h_chunk is None:
        result["H"] = {"status": "unavailable"}
    else:
        tables = re.findall(r"<table\b.*?</table>", h_chunk, re.S | re.I)
        rows = _parse_generic_table(tables[0]) if tables else None
        structured = _rows_to_structured(rows, "H") if rows else None
        if structured:
            result["H"] = {"status": "ok", "format": "table", "rows": structured}
            if len(tables) > 1:
                result["H"]["extra_text"] = _chunk_to_text("".join(tables[1:]))
        else:
            result["H"] = {"status": "ok", "format": "text", "text": _chunk_to_text(h_chunk)}

    r_chunk = _capture_after_match(html, _heading_span_by_text(html, "h3", "推翻論點"))
    if r_chunk is None:
        result["R"] = {"status": "unavailable"}
    else:
        tables = re.findall(r"<table\b.*?</table>", r_chunk, re.S | re.I)
        rows = _parse_generic_table(tables[0]) if tables else None
        structured = _rows_to_structured(rows, "R") if rows else None
        if structured:
            result["R"] = {"status": "ok", "format": "table", "rows": structured}
        else:
            result["R"] = {"status": "ok", "format": "text", "text": _chunk_to_text(r_chunk)}

    return result


def extract_triggers(html: str) -> dict:
    """E12 monitoring/trigger table (v15: id="triggers" table or heading).
    Legacy v13/v14 has no E12 table -> falls back to §15 (or nearby
    "複審觸發"/"觸發器" heading) raw text."""
    table_html = None
    m = re.search(r'<table\b[^>]*\bid=["\']triggers["\'][^>]*>(.*?)</table>', html, re.S | re.I)
    if m:
        table_html = "<table>" + m.group(1) + "</table>"
    else:
        hm = re.search(r'<h3\b[^>]*\bid=["\']triggers["\'][^>]*>.*?</h3>', html, re.S | re.I)
        if hm:
            tm = re.search(r"<table\b.*?</table>", html[hm.end():hm.end() + 6000], re.S | re.I)
            if tm:
                table_html = tm.group(0)

    if table_html:
        rows = _parse_generic_table(table_html)
        if rows:
            out = []
            for row in rows:
                headers, vals = row["headers"], row["vals"]
                rec = {"n": vals[0] if vals else None}
                for i, h in enumerate(headers):
                    if i < len(vals) and i >= 1:
                        rec[h or f"col{i}"] = vals[i]
                rec["status_now"] = None
                out.append(rec)
            return {"status": "ok", "format": "table", "rows": out}

    # legacy fallback: <section id="s15"> or a heading mentioning 複審觸發/觸發器
    m = re.search(r'<section\b[^>]*\bid=["\']s15["\'][^>]*>', html)
    if m:
        close_end = dd_sections._matching_close(html, m.end(), "section")
        return {"status": "ok", "format": "text", "text": _chunk_to_text(html[m.start():close_end])}

    hm2 = (_heading_span_by_text(html, "h[23]", "複審觸發")
           or _heading_span_by_text(html, "h[23]", "監測與觸發器"))
    chunk = _capture_after_match(html, hm2, end_pat=r"<h[23]\b|<details\b|</body")
    if chunk:
        return {"status": "ok", "format": "text", "text": _chunk_to_text(chunk)}
    return {"status": "unavailable"}


def _schema_ge(schema, min_major, min_minor):
    v = _version_tuple(schema)
    return v is not None and v >= (min_major, min_minor)


def find_inception(files):
    """Earliest file with schema >= v12.2 (dd-meta became reliable at v12.2+
    per repo convention). None if no file qualifies."""
    for d, f in files:
        meta = dd_sections.dd_meta_json(_read(f))
        schema = meta.get("schema") if meta else None
        if _schema_ge(schema, 12, 2):
            return {"path": str(f.relative_to(REPO_ROOT)), "date": d, "schema": schema}
    return None


def find_12m_ago(files, ref_date_str):
    from datetime import datetime, timedelta
    ref = datetime.strptime(ref_date_str, "%Y%m%d").date()
    target = ref - timedelta(days=365)
    best, best_diff = None, None
    for d, f in files:
        dd = datetime.strptime(d, "%Y%m%d").date()
        if dd >= ref:
            continue
        diff = abs((dd - target).days)
        if best_diff is None or diff < best_diff:
            best, best_diff = (d, f), diff
    if best is None:
        return None
    d, f = best
    return {"path": str(f.relative_to(REPO_ROOT)), "date": d, "days_from_365d_mark": best_diff}


def build_prior_dd(ticker_norm: str, before_date: str | None) -> dict:
    files = find_dd_files(ticker_norm)
    if not files:
        return {"status": "no_prior_dd"}

    cands = [(d, f) for d, f in files if before_date is None or d < before_date]
    if not cands:
        return {"status": "no_prior_dd"}
    date_str, path = cands[-1]
    html = _read(path)
    meta = dd_sections.dd_meta_json(html)

    out = {
        "status": "ok",
        "path": str(path.relative_to(REPO_ROOT)),
        "date": date_str,
        "schema": meta.get("schema") if meta else None,
        "dca_verdict": meta.get("dca_verdict") if meta else None,
        "dca_role": meta.get("dca_role") if meta else None,
        "price_at_dd": meta.get("price_at_dd") if meta else None,
        "revlog": extract_revlog(html),
        # v16 修法 5: 前份 dd-meta 全欄原樣（判斷層逐欄 diff 用；不裁剪）＋固定
        # drift_watch 清單（Stage 1 據此在 contradictions[] 逐項歸因，見
        # judgment-rules.md §12 item 3b）。
        "prior_meta": meta if meta else None,
        "drift_watch": DRIFT_WATCH,
    }
    hr = extract_hr_tables(html)
    out["H"] = hr["H"]
    out["R"] = hr["R"]
    out["triggers"] = extract_triggers(html)
    out["inception_dd"] = find_inception(files)
    out["dd_12m_ago"] = find_12m_ago(files, before_date or date_str)
    return out


# ---------------------------------------------------------------------------
# ledger (knowledge/q.py derived files)
# ---------------------------------------------------------------------------

def _run_q(args_list, timeout=120):
    return subprocess.run(
        [sys.executable, str(KNOWLEDGE_DIR / "q.py")] + args_list,
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=timeout, check=False,
    )


def build_ledger(ticker_norm: str) -> dict:
    try:
        _run_q([ticker_norm])  # triggers decisions/graph/settlement rebuild-if-stale
    except Exception as e:
        return {"status": "unavailable", "error": f"q.py invoke failed: {e}"}

    try:
        graph_path = KNOWLEDGE_DIR / "graph.json"
        decisions_path = KNOWLEDGE_DIR / "decisions.jsonl"
        settlement_path = KNOWLEDGE_DIR / "settlement.json"
        falsifiers_path = KNOWLEDGE_DIR / "falsifiers.json"

        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        aliases = graph.get("aliases", {})
        canonical = aliases.get(ticker_norm, ticker_norm)
        members = {canonical} | {a for a, c in aliases.items() if c == canonical}

        decisions = []
        if decisions_path.exists():
            for line in decisions_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                if d.get("kind") != "decision":
                    continue
                if (d.get("entity") or "").upper() in members:
                    decisions.append(d)
        decisions.sort(key=lambda d: d.get("date") or "")

        settlement = {}
        if settlement_path.exists():
            sdata = json.loads(settlement_path.read_text(encoding="utf-8"))
            settlement = {r["id"]: r for r in sdata.get("rows", [])}

        node = next((n for n in graph.get("nodes", []) if n["id"] == canonical), None)
        current = (node or {}).get("canonical")

        decision_history = []
        for d in decisions:
            st = settlement.get(d.get("id"))
            decision_history.append({
                "date": d.get("date"),
                "verdict": d.get("verdict"),
                "role": d.get("role"),
                "price_at_decision": d.get("price_at_decision"),
                "fundamental_grade": d.get("fundamental_grade"),
                "to_date_pct": st.get("to_date_pct") if st else None,
                "days": st.get("days") if st else None,
                "source_report": d.get("source_report"),
            })

        prior_watch_return_pct = None
        qc50_trigger_1 = False
        if decision_history:
            latest = decision_history[-1]
            if latest.get("verdict") in ("觀望", "迴避") and latest.get("to_date_pct") is not None:
                prior_watch_return_pct = latest["to_date_pct"]
                qc50_trigger_1 = prior_watch_return_pct > 30

        falsifiers = []
        if falsifiers_path.exists():
            fdata = json.loads(falsifiers_path.read_text(encoding="utf-8"))
            falsifiers = [
                it for it in fdata.get("items", [])
                if (it.get("ticker") or "").upper() == ticker_norm
            ]

        usernote = None
        try:
            p = _run_q(["--note", ticker_norm])
            text = (p.stdout or "").strip()
            usernote = text[:TEXT_CAP] if text else None
        except Exception:
            usernote = None

        return {
            "status": "ok",
            "canonical_entity": canonical,
            "current_verdict": current,
            "decision_history": decision_history,
            "prior_watch_return_pct": prior_watch_return_pct,
            "qc50_trigger_1": qc50_trigger_1,
            "falsifiers": falsifiers,
            "usernote": usernote,
        }
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}


# ---------------------------------------------------------------------------
# canonical_id (QC-52 Stage 1 facts-only excerpt)
# ---------------------------------------------------------------------------

_ID_ATTR_TAGS = "section|header|details|div"


def _id_attr_span(html: str, cid: str):
    pat = re.compile(r"<(" + _ID_ATTR_TAGS + r")\b[^>]*\bid=[\"']" + re.escape(cid) + r"[\"'][^>]*>")
    m = pat.search(html)
    if not m:
        return None
    tag = m.group(1)
    close_end = dd_sections._matching_close(html, m.end(), tag)
    return (m.start(), close_end)


def _extract_chapter_at(html: str, pos: int):
    """The nearest enclosing <section>...</section> around byte offset `pos`
    (used for legacy ID/DD pages where a chapter has no id attr of its own)."""
    sec_open = None
    for sm in re.finditer(r"<section\b[^>]*>", html[:pos]):
        sec_open = sm
    if sec_open is None:
        return None
    close_end = dd_sections._matching_close(html, sec_open.end(), "section")
    if close_end <= pos:
        return None
    return html[sec_open.start():close_end]


def extract_id_facts(html: str, skill_version: str) -> dict:
    ver = _version_tuple(skill_version)
    parts = {}
    if ver and ver >= (3, 0):
        for cid in ("mechanics", "appendix"):
            span = _id_attr_span(html, cid)
            if span:
                parts[cid] = _chunk_to_text(html[span[0]:span[1]], cap=ID_FACTS_CAP)
        if parts:
            return {"status": "ok", "sections": parts}
    # legacy v1.x/v2.x: no id attrs — locate by 供給/需求 heading text (h2 in
    # practice, but inline <em> inside the heading breaks a naive [^<]*
    # regex, so match on flattened text via _heading_span_by_text).
    for label, kw in (("supply", "供給"), ("demand", "需求")):
        m = _heading_span_by_text(html, "h[23]", kw)
        chunk = _extract_chapter_at(html, m.start()) if m else None
        if chunk:
            parts[label] = _chunk_to_text(chunk, cap=ID_FACTS_CAP)
    if parts:
        return {"status": "ok", "sections": parts}
    return {"status": "unavailable"}


_CONV_RANK = {"high": 3, "mid": 2, "low": 1, None: 0}


def build_canonical_id(ticker_norm: str) -> dict:
    try:
        matches = dd_meta_reader.find_ids_for_ticker(ID_DIR, ticker_norm)
    except Exception as e:
        return {"status": "gap", "error": str(e)}
    if not matches:
        return {"status": "gap"}

    best_by_theme = {}
    for path, meta in matches:
        theme = meta.get("theme") or path.stem
        pd_ = meta.get("publish_date") or ""
        cur = best_by_theme.get(theme)
        if cur is None or pd_ > (cur[1].get("publish_date") or ""):
            best_by_theme[theme] = (path, meta)
    candidates = list(best_by_theme.values())
    candidates.sort(
        key=lambda pm: (_CONV_RANK.get(pm[1].get("conviction")), pm[1].get("publish_date") or ""),
        reverse=True,
    )

    primary_path, primary_meta = candidates[0]
    try:
        primary_html = _read(primary_path)
    except OSError:
        primary_html = ""
    facts = extract_id_facts(primary_html, primary_meta.get("skill_version"))

    cand_list = [{
        "theme": meta.get("theme"),
        "path": str(path.relative_to(REPO_ROOT)),
        "skill_version": meta.get("skill_version"),
        "as_of": meta.get("publish_date"),
        "sd_verdict": meta.get("sd_verdict"),
        "clock_phase": meta.get("clock_phase"),
        "conviction": meta.get("conviction"),
        "priced_in": meta.get("priced_in"),
        "for_stage2_only": True,
    } for path, meta in candidates]

    return {
        "status": "ok",
        "primary": {
            "theme": primary_meta.get("theme"),
            "path": str(primary_path.relative_to(REPO_ROOT)),
            "skill_version": primary_meta.get("skill_version"),
            "as_of": primary_meta.get("publish_date"),
            "facts": facts,
            "machine": {
                "sd_verdict": primary_meta.get("sd_verdict"),
                "clock_phase": primary_meta.get("clock_phase"),
                "priced_in": primary_meta.get("priced_in"),
                "conviction": primary_meta.get("conviction"),
                "for_stage2_only": True,
            },
        },
        "candidates": cand_list,
        "note": (
            None if len(cand_list) <= 1 else
            "primary 由 conviction desc + publish_date desc 排序機械選出，非人工裁定"
            "——ticker 掛在多個產業主題下時，Stage 1 判斷層應覆核 candidates 是否有更貼題者。"
        ),
    }


# ---------------------------------------------------------------------------
# transcripts
# ---------------------------------------------------------------------------

_HI_SIGNAL_KW = ("investor_day", "analyst", "special_call")


def _fdate(fname: str) -> str:
    m = re.search(r"(\d{8})\.md$", fname)
    return m.group(1) if m else ""


def build_transcripts(drive_ticker: str) -> dict:
    if not TRANSCRIPTS_SCRIPT.exists():
        return {"status": "unavailable"}
    try:
        p = subprocess.run(
            [sys.executable, str(TRANSCRIPTS_SCRIPT), drive_ticker],
            capture_output=True, text=True, timeout=60, check=False,
        )
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}

    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    lines = [ln for ln in combined.splitlines() if ln.strip()]
    if not lines:
        return {"status": "unavailable"}
    data = None
    for ln in reversed(lines):
        try:
            data = json.loads(ln)
            break
        except json.JSONDecodeError:
            continue
    if data is None:
        return {"status": "unavailable", "raw_tail": lines[-1][:500]}

    must = data.get("must_read", [])
    optional = data.get("optional_read", [])
    must_sorted = sorted(must, key=_fdate)
    selected_recent_four = must_sorted[-4:]
    hi_candidates = sorted(
        [f for f in optional if any(k in f.lower() for k in _HI_SIGNAL_KW)], key=_fdate,
    )
    selected_optional = hi_candidates[-1:]

    return {
        "status": "ok",
        "mode": data.get("mode"),
        "must_read_all": must,
        "optional_read_all": optional,
        "selected": {
            "recent_four_quarters": selected_recent_four,
            "high_signal_optional": selected_optional,
        },
        "must_read_tokens_total": data.get("must_read_tokens_total"),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("--date", default=None, help="新報告日期 YYYYMMDD；prior_dd 只取此日期之前最新一份")
    ap.add_argument("--out", default=None, help="寫檔路徑；省略則印 stdout")
    ap.add_argument("--drive-ticker", default=None, help="Koyfin Drive 資料夾用原始 ticker（如 2330.TW）")
    args = ap.parse_args()

    ticker_norm = normalize_ticker(args.ticker)
    drive_ticker = args.drive_ticker or args.ticker

    result = {
        "prior_dd": build_prior_dd(ticker_norm, args.date),
        "ledger": build_ledger(ticker_norm),
        "canonical_id": build_canonical_id(ticker_norm),
        "transcripts": build_transcripts(drive_ticker),
    }

    out_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out_json, encoding="utf-8")
        nbytes = len(out_json.encode("utf-8"))
        prior_bytes = len(json.dumps(result["prior_dd"], ensure_ascii=False).encode("utf-8"))
        print(f"Wrote {args.out} ({nbytes}B total; prior_dd={prior_bytes}B)")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
