#!/usr/bin/env python3
"""dd_delta.py — stock-analyst v16 delta-mode: zero-LLM re-run diff engine.

On a re-run of an existing ticker, tells Stage 1 (judgment agent) and Stage 2
(prose agent) exactly what changed since the prior report so they only touch
the affected judgment fields / prose sections instead of rewriting the whole
report. Reads two v16 evidence.json snapshots (prior vs new) plus the prior
judgment.json, and produces a delta.json consumed by the writer pipeline.

Zero LLM, stdlib only. Run with /tmp/ddvenv/bin/python for consistency with
the rest of the v16 WP1/WP2 scripts.

Usage:
    dd_delta.py TICKER DATE --prior PRIOR_SRC_DIR --evidence NEW_EVIDENCE.json
                [--digest DIGEST.json] --out DELTA_OUT.json
                [--stage-prose PROSE_OUT_DIR]

    dd_delta.py check DELTA.json --judgment NEW_JUDGMENT.json
                --prior-judgment PRIOR_JUDGMENT.json

See scripts/dd_schema/delta.md for the field/rule reference and
notes/site-internal/dd/_v16_design_spec_20260903.md for the surrounding
pipeline. Judgment-path <-> dd-meta field authority: scripts/dd_schema/
judgment-to-ddmeta.md. Prior-report extraction convention (prior_meta /
DRIFT_WATCH) reused from scripts/dd_prior.py — this script imports its
DRIFT_WATCH constant rather than duplicating the list.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dd_prior  # sibling module — reuse DRIFT_WATCH (single source of truth)

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Rule tables (top of file per repo governance: 判斷類規則表寫在腳本頂部常數)
# ---------------------------------------------------------------------------

# evidence.numbers.<subkey> changed -> which judgment.json subtrees must be
# re-examined by Stage 1. Coverage-axis and events findings carry their own
# `affects[]` list in evidence.json (used directly, not via a table here);
# this table only covers the `numbers` block, which has no `affects` field.
# GUESSED (render-rules.md does not enumerate this; inferred from
# html-output.md's section-content descriptions — flag for holder review).
NUMBERS_FIELD_RULES = {
    "valuation_history": ["valuation.history_note", "valuation.percentile_5y"],
    "momentum_26w": ["decision_inputs.week26_return_pct", "decision_inputs.momentum_overheated"],
    "consensus_revision": ["growth.seven_questions", "decision_inputs.consensus_rev_3m_pct"],
    "consensus_fy123": ["valuation.fwd_pe", "eps_meta.base_eps_path"],
    "peer_financials": ["moat.competitors", "quality.three_year"],
    "edgar_concentrations": ["thesis.R", "moat.roic_durability"],
    "latest_quarter_kpis": [
        "growth.segments", "growth.seven_questions", "quality.three_year",
        "decision_inputs.signal", "moat.spread_table", "eps_meta.base_eps_path",
    ],
    "top_banner": ["decision_inputs.price_at_dd"],
    "price_technical": ["decision_inputs.ma"],
    "valuation_multiples": ["valuation.fwd_pe", "valuation.peg", "decision_inputs.val"],
    "peer_valuation_multiples": ["valuation.peers", "valuation.tier"],
    "analyst_price_target_consensus": ["valuation.targets"],
    "fwd_pe_5y_percentile": ["valuation.val_light_derivation"],
    "five_year_financials": ["quality.three_year", "quality.dupont", "governance.capital_returns"],
    "equity_structure": ["governance.ownership"],
    "qc19_event_headlines": ["premortem.blind_spots", "triggers"],
    "management_commitments": ["thesis.H", "growth.seven_questions"],
    "price_at_dd": ["decision_inputs.price_at_dd", "valuation.targets"],
}

# NUMBERS_SID_OVERRIDES (evidence-only sections with no dedicated judgment
# field, e.g. s8 財報情報) is defined further below alongside
# JUDGMENT_PATH_TO_SID / ALWAYS_REWRITE_SIDS, all three loaded from the
# single authority scripts/dd_schema/section_map.json (fallback built-in).

# event category -> judgment fields, used only when a finding has no
# `affects[]` of its own (evidence.json events findings normally do carry
# `affects`, so this is a fallback, not the primary path). GUESSED.
EVENTS_CATEGORY_FALLBACK = {
    "ma_merger": ["governance.scorecard", "governance.ma_track_10y", "thesis.R"],
    "lawsuit_class_action": ["premortem.blind_spots", "governance.insider_comp"],
    "clinical_fda": ["thesis.R"],
    "product_recall_warning": ["moat.threats", "premortem.blind_spots", "triggers"],
    "sec_investigation_restatement": ["governance.insider_comp", "contradictions"],
}

# ---------------------------------------------------------------------------
# section_map.json — single authority for sid<->judgment-path mapping
# ---------------------------------------------------------------------------
# scripts/dd_schema/section_map.json is the authoritative, editable copy of
# the three tables below (judgment_path_to_sid / numbers_sid_overrides /
# always_rewrite_sids) — see render-rules.md §2 tail note: prose agent and
# dd_delta.py must read the same file, so a mapping fix only touches one
# place. The constants defined here are the FALLBACK used only when that
# file is missing or fails to parse (this script must never hard-fail on a
# bad section_map.json). GUESSED origin unchanged: render-rules.md §1/§2 only
# documents the five table-injection markers (E2/E11/AUDIT/E12/APPA_TABLE);
# the rest is inferred from html-output.md's "章節顯示順序" content
# descriptions — flag for holder review (tracked in section_map.json's own
# `_note` fields, not just here).
SECTION_MAP_PATH = REPO_ROOT / "scripts" / "dd_schema" / "section_map.json"

_FALLBACK_JUDGMENT_PATH_TO_SID = [
    ("meta", "s1"),
    ("oneliner", "s1"),
    ("trap_analysis", "s1"),
    ("archetype", "s4"),
    ("munger_gates", "s4"),
    ("thesis", "s2"),
    ("industry", "s3"),
    ("moat", "s5"),
    ("growth", "s6"),
    ("quality", "s7"),
    ("governance", "s9"),
    ("valuation", "s10"),
    ("eps_meta", "s10"),
    ("scenario_ref", "s10"),
    ("appendix_a", "appA"),
    ("catalysts", "s14"),
    ("decision_inputs", "decision"),
    ("decision_out", "decision"),
    ("triggers", "decision"),
    ("contradictions", "s11"),
    ("premortem", "s12"),
    ("reasoning.archetype", "s4"),
    ("reasoning.thesis", "s2"),
    ("reasoning.industry", "s3"),
    ("reasoning.moat", "s5"),
    ("reasoning.growth", "s6"),
    ("reasoning.quality", "s7"),
    ("reasoning.governance", "s9"),
    ("reasoning.valuation", "s10"),
    ("reasoning.trap_analysis", "s1"),
    ("reasoning.premortem", "s12"),
    ("reasoning.scenario", "s10"),
]

# Sections rewritten on every delta run regardless of what changed: s1
# (headline conclusion), decision (§13 unified verdict — always re-derived),
# revlog (must record this run either way), s14 (review cadence/catalysts),
# appA (mechanical grade row, cheap to regen and downstream-critical). Per
# the CLI contract this is "s1/s13/decision/revlog always + s14/appA
# always" — the actual prose file is named `decision.html` (there is no
# separate s13.html in the v16 prose set), so "s13" and "decision" are the
# same file.
_FALLBACK_ALWAYS_REWRITE_SIDS = ["s1", "decision", "revlog", "s14", "appA"]

_FALLBACK_NUMBERS_SID_OVERRIDES = {
    "latest_quarter_kpis": ["s8"],
    "qc19_event_headlines": ["s8", "s1"],
    "management_commitments": ["s8"],
    "top_banner": ["s1"],
}


def _load_section_map():
    """Read section_map.json; fall back to the built-in constants above on
    any error (missing file, bad JSON, missing keys) — this script must
    never hard-fail because someone hand-edited the map file badly."""
    try:
        data = json.loads(SECTION_MAP_PATH.read_text(encoding="utf-8"))
        path_to_sid = [
            (e["path"], e["sid"]) for e in data.get("judgment_path_to_sid", [])
            if "path" in e and "sid" in e
        ] or list(_FALLBACK_JUDGMENT_PATH_TO_SID)
        always_rewrite = set(data.get("always_rewrite_sids") or _FALLBACK_ALWAYS_REWRITE_SIDS)
        numbers_overrides = data.get("numbers_sid_overrides") or dict(_FALLBACK_NUMBERS_SID_OVERRIDES)
        return path_to_sid, always_rewrite, numbers_overrides
    except (OSError, ValueError, KeyError, TypeError):
        return (
            list(_FALLBACK_JUDGMENT_PATH_TO_SID),
            set(_FALLBACK_ALWAYS_REWRITE_SIDS),
            dict(_FALLBACK_NUMBERS_SID_OVERRIDES),
        )


JUDGMENT_PATH_TO_SID, ALWAYS_REWRITE_SIDS, NUMBERS_SID_OVERRIDES = _load_section_map()

# judgment.json paths that are allowed to change on every delta run even if
# not flagged by evidence diff, because their backing sections are always
# rewritten. Derived (not separately hand-maintained) from JUDGMENT_PATH_TO_SID:
# any path whose sid is in ALWAYS_REWRITE_SIDS. Editing section_map.json's
# judgment_path_to_sid or always_rewrite_sids therefore changes what `check`
# permits too — see section_map.json's judgment_path_to_sid_note.
ALWAYS_ALLOWED_JUDGMENT_PATHS = sorted({
    p for p, sid in JUDGMENT_PATH_TO_SID if sid in ALWAYS_REWRITE_SIDS
})

# DRIFT_WATCH field -> its one authoritative judgment.json path, per
# scripts/dd_schema/judgment-to-ddmeta.md §二/§三. Fields with `None` live
# only in scenario_meta.json (bull/bear price, p_bull/p_bear) and are out of
# scope for a judgment.json-only `check` — documented gap, not a guess.
DRIFT_FIELD_JUDGMENT_PATH = {
    "dca_verdict": "decision_out.verdict",
    "dca_role": "decision_out.role",
    "signal": "appendix_a.signal",
    "val": "appendix_a.val",
    "ma": "appendix_a.ma",
    "trap": "trap_analysis.verdict",
    "moat_trend": "moat.trend",
    "runway_post_y5": "growth.runway_post_y5",
    "asym_ratio": "decision_inputs.asym_ratio",
    "ev5y_pct": "decision_inputs.ev5y_pct",
    "irr_base_pct": "decision_inputs.irr_base_pct",
    "max_dd_pct": "premortem.max_dd.lo",
    "bull_5y_price": None,
    "bear_5y_price": None,
    "p_bull_pct": None,
    "p_bear_pct": None,
    "rearm_trigger": "decision_out.rearm_trigger",
    "price_at_dd": "decision_inputs.price_at_dd",
    "archetype": "archetype.primary",
    "cycle_position": "decision_inputs.cycle_position",
}

# Free-text/meta noise keys ignored when diffing evidence.json's `numbers`
# block (they change every collection run without representing a real number
# change). NOT applied to judgment.json diffing in `check` — a changed prose
# `note` in judgment.json is real judgment content, not noise.
IGNORE_EVIDENCE_LEAF_KEYS = frozenset({
    "note", "queries_run", "collection_timestamp", "search_calls_note", "method",
})

FULL_REWRITE_PRICE_MOVE_PCT = 40.0
FULL_REWRITE_MAX_AGE_DAYS = 180


# ---------------------------------------------------------------------------
# generic recursive diff — shared by numbers_changed and `check`
# ---------------------------------------------------------------------------

_ALIGN_KEYS = ("metric", "id", "n", "name", "axis", "year", "segment", "driver", "commitment")


def _align_key(items):
    if not items or not all(isinstance(i, dict) for i in items):
        return None
    for k in _ALIGN_KEYS:
        if all(k in i for i in items):
            return k
    return None


def deep_diff(old, new, path="", ignore_keys=frozenset()):
    """Yield (path, old_val, new_val, kind) for every leaf-level difference.

    kind in {"changed", "added", "removed"}. Dicts recurse by key; lists of
    dicts sharing a common id-like key (see _ALIGN_KEYS) are aligned by that
    key and recursed into (this is how latest_quarter_kpis.items gets
    aligned by "metric" without special-casing that one path); any other
    list is compared as a whole (changed/unchanged), no recursion.
    """
    out = []
    if isinstance(old, dict) or isinstance(new, dict):
        old_d = old if isinstance(old, dict) else {}
        new_d = new if isinstance(new, dict) else {}
        for k in sorted(set(old_d) | set(new_d)):
            if k in ignore_keys:
                continue
            p = f"{path}.{k}" if path else k
            if k not in old_d:
                out.append((p, None, new_d[k], "added"))
            elif k not in new_d:
                out.append((p, old_d[k], None, "removed"))
            else:
                out.extend(deep_diff(old_d[k], new_d[k], p, ignore_keys))
    elif isinstance(old, list) or isinstance(new, list):
        old_l = old if isinstance(old, list) else []
        new_l = new if isinstance(new, list) else []
        key = _align_key(old_l) or _align_key(new_l)
        if key:
            old_m = {i.get(key): i for i in old_l if isinstance(i, dict)}
            new_m = {i.get(key): i for i in new_l if isinstance(i, dict)}
            for kk in sorted(set(old_m) | set(new_m), key=lambda x: str(x)):
                p = f"{path}[{kk}]"
                if kk not in old_m:
                    out.append((p, None, new_m[kk], "added"))
                elif kk not in new_m:
                    out.append((p, old_m[kk], None, "removed"))
                else:
                    out.extend(deep_diff(old_m[kk], new_m[kk], p, ignore_keys))
        else:
            if old_l != new_l:
                out.append((path, old_l, new_l, "changed"))
    else:
        if old != new:
            out.append((path, old, new, "changed"))
    return out


def _pct_change(old_v, new_v):
    if isinstance(old_v, (int, float)) and isinstance(new_v, (int, float)) and not isinstance(old_v, bool) and not isinstance(new_v, bool):
        if old_v == 0:
            return None
        return round((new_v - old_v) / abs(old_v) * 100, 2)
    return None


def _get_path(d, path):
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _normalize_claim(s):
    return re.sub(r"\s+", "", (s or "")).strip()


# ---------------------------------------------------------------------------
# numbers_changed
# ---------------------------------------------------------------------------

def build_numbers_changed(old_evidence: dict, new_evidence: dict):
    old_numbers = old_evidence.get("numbers") or {}
    new_numbers = new_evidence.get("numbers") or {}
    diffs = deep_diff(old_numbers, new_numbers, path="numbers", ignore_keys=IGNORE_EVIDENCE_LEAF_KEYS)
    changed = []
    fields_to_review = set()
    for p, old_v, new_v, kind in diffs:
        rec = {"path": p, "old": old_v, "new": new_v}
        if kind == "added":
            rec = {"path": p, "new": new_v, "added": True}
        elif kind == "removed":
            rec = {"path": p, "old": old_v, "removed": True}
        else:
            pct = _pct_change(old_v, new_v)
            if pct is not None:
                rec["pct_change"] = pct
        changed.append(rec)
        # numbers.<subkey>[...] -> subkey is the second dotted component
        parts = p.split(".")
        subkey = parts[1] if len(parts) > 1 else None
        if subkey in NUMBERS_FIELD_RULES:
            fields_to_review.update(NUMBERS_FIELD_RULES[subkey])
    return changed, fields_to_review


# ---------------------------------------------------------------------------
# coverage_changed / events_changed (share the same axis-diff shape)
# ---------------------------------------------------------------------------

def _diff_axis_block(old_block: dict, new_block: dict, category: str, fallback_affects):
    old_findings = (old_block or {}).get("findings") or []
    new_findings_all = (new_block or {}).get("findings") or []
    old_claims = {_normalize_claim(f.get("claim")) for f in old_findings}
    new_findings = [f for f in new_findings_all if _normalize_claim(f.get("claim")) not in old_claims]

    status_old = (old_block or {}).get("status")
    status_new = (new_block or {}).get("status")
    status_change = None if status_old == status_new else {"old": status_old, "new": status_new}

    affects = set()
    for f in new_findings:
        finding_affects = f.get("affects") or []
        if finding_affects:
            affects.update(finding_affects)
        else:
            affects.update(fallback_affects.get(category, []))

    return new_findings, status_change, affects


def build_coverage_changed(old_evidence: dict, new_evidence: dict):
    old_cov = old_evidence.get("coverage") or {}
    new_cov = new_evidence.get("coverage") or {}
    result = {}
    fields_to_review = set()
    for axis in sorted(set(old_cov) | set(new_cov)):
        new_findings, status_change, affects = _diff_axis_block(
            old_cov.get(axis), new_cov.get(axis), axis, {},
        )
        if new_findings or status_change:
            entry = {}
            if new_findings:
                entry["new_findings"] = new_findings
            if status_change:
                entry["status_change"] = status_change
            result[axis] = entry
            fields_to_review.update(affects)
    return result, fields_to_review


def build_events_changed(old_evidence: dict, new_evidence: dict):
    old_ev = old_evidence.get("events") or {}
    new_ev = new_evidence.get("events") or {}
    result = {}
    fields_to_review = set()
    for category in sorted(set(old_ev) | set(new_ev)):
        new_findings, status_change, affects = _diff_axis_block(
            old_ev.get(category), new_ev.get(category), category, EVENTS_CATEGORY_FALLBACK,
        )
        if new_findings or status_change:
            entry = {}
            if new_findings:
                entry["new_findings"] = new_findings
            if status_change:
                entry["status_change"] = status_change
            result[category] = entry
            fields_to_review.update(affects)
    return result, fields_to_review


# ---------------------------------------------------------------------------
# sections_to_rewrite
# ---------------------------------------------------------------------------

def _path_to_sids(path: str):
    sids = set()
    bare = path[:-2] if path.endswith(".*") else path
    for prefix, sid in JUDGMENT_PATH_TO_SID:
        if bare == prefix or bare.startswith(prefix + "."):
            sids.add(sid)
    return sids


def build_sections_to_rewrite(judgment_fields_to_review, numbers_changed, all_sids):
    to_rewrite = set(ALWAYS_REWRITE_SIDS) & all_sids
    for path in judgment_fields_to_review:
        to_rewrite |= (_path_to_sids(path) & all_sids)
    changed_numbers_subkeys = set()
    for rec in numbers_changed:
        parts = rec["path"].split(".")
        if len(parts) > 1:
            changed_numbers_subkeys.add(parts[1])
    for subkey in changed_numbers_subkeys:
        for sid in NUMBERS_SID_OVERRIDES.get(subkey, []):
            if sid in all_sids:
                to_rewrite.add(sid)
    carry_forward = sorted(all_sids - to_rewrite)
    return sorted(to_rewrite), carry_forward


# ---------------------------------------------------------------------------
# full_rewrite_required
# ---------------------------------------------------------------------------

def build_full_rewrite_required(new_date, prior_date, numbers_changed, prior_judgment, new_evidence):
    reasons = []

    price_rec = next((r for r in numbers_changed if r["path"] == "numbers.price_at_dd" and "pct_change" in r), None)
    if price_rec and abs(price_rec["pct_change"]) > FULL_REWRITE_PRICE_MOVE_PCT:
        reasons.append(f"price_at_dd moved {price_rec['pct_change']}% (> {FULL_REWRITE_PRICE_MOVE_PCT}%)")

    try:
        d_new = datetime.strptime(new_date, "%Y%m%d")
        d_prior = datetime.strptime(prior_date, "%Y%m%d")
        age_days = (d_new - d_prior).days
        if age_days > FULL_REWRITE_MAX_AGE_DAYS:
            reasons.append(f"prior report is {age_days}d old (> {FULL_REWRITE_MAX_AGE_DAYS}d)")
    except ValueError:
        pass

    prior_archetype = _get_path(prior_judgment, "archetype.primary")
    new_archetype_hint = new_evidence.get("archetype_hint")
    if prior_archetype and new_archetype_hint and prior_archetype != new_archetype_hint:
        reasons.append(
            f"archetype_hint diverges from prior verdict archetype ({prior_archetype!r} -> {new_archetype_hint!r})"
        )

    return {"required": bool(reasons), "reasons": reasons}


# ---------------------------------------------------------------------------
# main (generate) command
# ---------------------------------------------------------------------------

_PRIOR_DIRNAME_RE = re.compile(r"^(?P<ticker>.+)_(?P<date>\d{8})$")


def cmd_generate(argv):
    ap = argparse.ArgumentParser(prog="dd_delta.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("ticker")
    ap.add_argument("date", help="新報告日期 YYYYMMDD")
    ap.add_argument("--prior", required=True, help="prior 來源包目錄（notes/site-internal/dd/_src/{T}_{PRIOR_D}）")
    ap.add_argument("--evidence", required=True, help="新 evidence.json 路徑")
    ap.add_argument("--digest", default=None, help="選填：transcript_digest.json 路徑（僅記錄路徑，見 delta.md 已知缺口）")
    ap.add_argument("--out", required=True, help="輸出 delta.json 路徑")
    ap.add_argument("--stage-prose", default=None, help="選填：複製 prior 的 carry_forward prose 段到此目錄")
    args = ap.parse_args(argv)

    ticker_norm = args.ticker.strip().upper()
    prior_dir = Path(args.prior)
    m = _PRIOR_DIRNAME_RE.match(prior_dir.name)
    if not m:
        print(f"ERROR: --prior 目錄名不符 {{TICKER}}_{{YYYYMMDD}} 格式: {prior_dir.name}", file=sys.stderr)
        return 2
    prior_ticker, prior_date = m.group("ticker"), m.group("date")

    prior_evidence_path = prior_dir / f"{prior_ticker}_{prior_date}.evidence.json"
    prior_judgment_path = prior_dir / f"{prior_ticker}_{prior_date}.judgment.json"
    if not prior_evidence_path.exists() or not prior_judgment_path.exists():
        print(f"ERROR: prior 包缺檔: {prior_evidence_path} / {prior_judgment_path}", file=sys.stderr)
        return 2

    prior_evidence = json.loads(prior_evidence_path.read_text(encoding="utf-8"))
    prior_judgment = json.loads(prior_judgment_path.read_text(encoding="utf-8"))
    new_evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))

    numbers_changed, fields_from_numbers = build_numbers_changed(prior_evidence, new_evidence)
    coverage_changed, fields_from_coverage = build_coverage_changed(prior_evidence, new_evidence)
    events_changed, fields_from_events = build_events_changed(prior_evidence, new_evidence)

    fields_to_review = set()
    fields_to_review.update(fields_from_numbers)
    fields_to_review.update(fields_from_coverage)
    fields_to_review.update(fields_from_events)
    # prior_meta 任一欄 -> contradictions（QC-49 執行細則，沿用 dd_prior 慣例）
    fields_to_review.add("contradictions")
    judgment_fields_to_review = sorted(fields_to_review)

    prose_dir = prior_dir / "prose"
    all_sids = {f.stem for f in prose_dir.glob("*.html")} if prose_dir.is_dir() else set(ALWAYS_REWRITE_SIDS)
    sections_to_rewrite, carry_forward = build_sections_to_rewrite(judgment_fields_to_review, numbers_changed, all_sids)

    full_rewrite = build_full_rewrite_required(args.date, prior_date, numbers_changed, prior_judgment, new_evidence)

    prior_meta = {f: _get_path(prior_judgment, p) for f, p in DRIFT_FIELD_JUDGMENT_PATH.items() if p}
    prior_meta_diff = {"prior_meta": prior_meta, "drift_watch": dd_prior.DRIFT_WATCH}

    delta = {
        "prior": {
            "dir": str(prior_dir),
            "date": prior_date,
            "judgment_path": str(prior_judgment_path),
            "evidence_path": str(prior_evidence_path),
        },
        "numbers_changed": numbers_changed,
        "coverage_changed": coverage_changed,
        "events_changed": events_changed,
        "prior_meta_diff": prior_meta_diff,
        "judgment_fields_to_review": judgment_fields_to_review,
        "sections_to_rewrite": sections_to_rewrite,
        "carry_forward": carry_forward,
        "full_rewrite_required": full_rewrite,
    }
    if args.digest:
        delta["digest_path"] = args.digest

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(delta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} ({len(numbers_changed)} numbers_changed, "
          f"{len(coverage_changed)} coverage axes, {len(events_changed)} event categories, "
          f"{len(sections_to_rewrite)} sections_to_rewrite, "
          f"full_rewrite_required={full_rewrite['required']})")

    if args.stage_prose:
        stage_dir = Path(args.stage_prose)
        stage_dir.mkdir(parents=True, exist_ok=True)
        copied = 0
        if prose_dir.is_dir():
            for f in prose_dir.glob("*.html"):
                if f.stem in carry_forward:
                    (stage_dir / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
                    copied += 1
        judgment_prior_out = out_path.parent / f"{ticker_norm}_{args.date}.judgment.prior.json"
        judgment_prior_out.write_text(
            json.dumps(prior_judgment, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Staged {copied} carry_forward prose file(s) to {stage_dir}; "
              f"prior judgment copied to {judgment_prior_out}")

    return 0


# ---------------------------------------------------------------------------
# check subcommand
# ---------------------------------------------------------------------------

def _is_allowed(path: str, allowed_bare_prefixes):
    for bare in allowed_bare_prefixes:
        if path == bare or path.startswith(bare + ".") or path.startswith(bare + "["):
            return True
    return False


def cmd_check(argv):
    ap = argparse.ArgumentParser(prog="dd_delta.py check")
    ap.add_argument("delta_json")
    ap.add_argument("--judgment", required=True)
    ap.add_argument("--prior-judgment", required=True)
    args = ap.parse_args(argv)

    delta = json.loads(Path(args.delta_json).read_text(encoding="utf-8"))
    judgment = json.loads(Path(args.judgment).read_text(encoding="utf-8"))
    prior_judgment = json.loads(Path(args.prior_judgment).read_text(encoding="utf-8"))

    review_paths = delta.get("judgment_fields_to_review", [])
    allowed_bare = set()
    for p in review_paths + ALWAYS_ALLOWED_JUDGMENT_PATHS:
        allowed_bare.add(p[:-2] if p.endswith(".*") else p)
    always_exact = {"meta.date", "meta.schema", "scenario_ref"}

    diffs = deep_diff(prior_judgment, judgment)
    violations = []
    for path, old_v, new_v, kind in diffs:
        if path in always_exact:
            continue
        if _is_allowed(path, allowed_bare):
            continue
        violations.append({"path": path, "kind": kind, "old": old_v, "new": new_v})

    # contradictions[] must carry a prior_field entry for every DRIFT_WATCH
    # field whose value actually changed (fields living only in
    # scenario_meta.json are skipped — out of scope for a judgment-only check).
    contradictions = judgment.get("contradictions") or []
    prior_fields_present = {c.get("prior_field") for c in contradictions if c.get("prior_field")}
    missing_prior_field = []
    for field, jpath in DRIFT_FIELD_JUDGMENT_PATH.items():
        if not jpath:
            continue
        old_v = _get_path(prior_judgment, jpath)
        new_v = _get_path(judgment, jpath)
        if old_v is not None and old_v != new_v and field not in prior_fields_present:
            missing_prior_field.append({"field": field, "path": jpath, "old": old_v, "new": new_v})

    ok = not violations and not missing_prior_field
    if ok:
        print("PASS: judgment.json 只改動 judgment_fields_to_review（含永遠允許欄）列出的路徑；"
              "漂移欄位皆有 contradictions[].prior_field 條目。")
        return 0

    print("FAIL")
    if violations:
        print(f"  改動了清單外的路徑（{len(violations)} 項）：")
        for v in violations:
            print(f"    - [{v['kind']}] {v['path']}: {v['old']!r} -> {v['new']!r}")
    if missing_prior_field:
        print(f"  漂移欄位缺 contradictions[].prior_field 條目（{len(missing_prior_field)} 項）：")
        for m in missing_prior_field:
            print(f"    - {m['field']} ({m['path']}): {m['old']!r} -> {m['new']!r}")
    return 1


# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        sys.exit(cmd_check(sys.argv[2:]))
    sys.exit(cmd_generate(sys.argv[1:]))


if __name__ == "__main__":
    main()
