#!/usr/bin/env python3
"""Validate <script id="dd-meta"> JSON blocks across all v12+ DD HTML files.

Purpose: enforce a stable contract between stock-analyst skill output and
downstream consumers (research index, portfolio-manager skill,
morning-briefing). Run in CI / pre-commit to fail PRs that introduce broken
or incomplete dd-meta blocks.

Usage:
  python scripts/validate_dd_meta.py            # strict: exit 1 on any issue
  python scripts/validate_dd_meta.py --report   # exit 0 always; print issues
  python scripts/validate_dd_meta.py --json     # machine-readable output
  python scripts/validate_dd_meta.py FILE...    # validate specific files only
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DD_DIR = ROOT / "docs" / "dd"

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
META_VERSION_RE = re.compile(
    r'<meta\s+name="dd-schema-version"\s+content="([^"]+)"', re.IGNORECASE
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# v12.x = legacy DD; v13.x / v14.x = merged DD+DCA report (decision layer folded in).
# v14.0–v14.3 are methodology bumps (QC-39/40/41, row5 demotion, F1-F3 long-wave
# calibration, v14.3 breakout-candidate path adding optional asym_ratio); same
# dd-meta required-field contract as v13 — the v13-required-fields rule
# below applies to v13.x AND v14.x identically.
SCHEMA_RE = re.compile(r"^v1[234]\.\d+$")
IN_SCOPE_VERSIONS = ("v12", "v13", "v14")

# Required fields with their expected Python types (after json.loads).
# Keys present here MUST appear in every v12 dd-meta block.
REQUIRED_FIELDS = {
    "ticker": str,
    "schema": str,
    "date": str,
    "price_at_dd": (int, float),
    "signal": str,
    "trap": str,
    "trap_label": str,
    "moat": str,
    "val": str,
    "ma": str,
    "fpe_fy2": (int, float),
    "pct_5y": (int, float),
    "peg_fy2": (int, float),
    "upside_short_pct": (int, float),
    "upside_mid_pct": (int, float),
    "stress": dict,
    "moat_score": (int, float),
    "growth_durability": (int, float),
    "quality_score": (int, float),
    "ai_risk": str,
    "long_term_confidence": str,
    "verdict": str,
    "oneliner": str,
}

ENUM_FIELDS = {
    "signal": {"A+", "A", "B", "C", "X"},
    "trap": {"🟢", "🟡", "🔴"},
    "moat": {"S", "A", "B", "C", "X"},
    "val": {"🟢", "🟡", "🟠", "🔴"},
    "ma": {"🟢", "✅", "🟡", "🟠", "❌", "-"},
    "ai_risk": {"🟢", "🟡", "🔴"},
    "long_term_confidence": {"高", "中", "低"},
}

NUMERIC_RANGES = {
    "moat_score": (1, 10),
    "growth_durability": (1, 10),
    "quality_score": (1, 10),
    "pct_5y": (0, 100),
}

ONELINER_HARD_CAP = 200  # hard cap; ≤ 120 is the soft target per skill spec

# ── v13 (merged DD+DCA) additions ──────────────────────────────────────────
# The v13 report folds the former DCA decision layer into the DD. These fields
# are REQUIRED only when schema is v13.x; v12 reports never carry them, so the
# legacy contract is untouched. The aggregators (update_dd_index,
# dd_screener_dd_loader, aggregate_dca_stats) read these straight from JSON
# instead of regex-parsing a separate DCA HTML.
V13_REQUIRED_FIELDS = {
    "dca_verdict": str,
    "dca_role": str,
    "moat_trend": str,
    "runway_post_y5": str,
    "ev5y_pct": (int, float),
}

V13_ENUM_FIELDS = {
    # v14.5 adds conditional-entry verdicts (§14 row 8b). Body text has long
    # carried "進場·條件式" as prose; v14.5 promotes it to a first-class meta
    # value with an archetype-qualifier suffix (全形括號＋間隔號 · style, matching
    # the existing 「進場·條件式」 prose). Both flavours are treated as entry
    # verdicts by downstream (爆發/循環 tracks). 進場·條件式（爆發候選）is
    # whitelisted for parity even before the first report emits it.
    "dca_verdict": {
        "進場",
        "進場·條件式（循環衛星）",
        "進場·條件式（爆發候選）",
        "觀望",
        "迴避",
    },
    # dca_role enum mirrors aggregate_dca_stats.py CATEGORY_ORDER (minus the
    # "缺資料" fallback, which must never be emitted by a real report).
    "dca_role": {
        "核心持倉",
        "條件式核心持倉",
        "衛星持倉",
        "條件式衛星持倉",
        "投機部位",
        "不持有/迴避",
        "候選/追蹤池",
    },
    "moat_trend": {"↑", "→", "↓"},
    "runway_post_y5": {"🟢", "🟡", "🔴"},
}

# Optional v13 fields: validated for type only when present.
V13_OPTIONAL_TYPES = {
    "irr_base_pct": (int, float),
    "max_dd_pct": (int, float),
    # v14.3: §11.5 asymmetry ratio (P_bull×|Bull 5Y%|)/(P_bear×|Bear 5Y%|)
    "asym_ratio": (int, float),
    # v14.3 F4 (AR Live): §11.5 Bull/Bear 5Y target prices + scenario
    # probabilities — lets dd-screener recompute ar_live at today's price.
    "bull_5y_price": (int, float),
    "bear_5y_price": (int, float),
    "p_bull_pct": (int, float),
    "p_bear_pct": (int, float),
    # 2026-07-05 T-minus 鏈群組：catalyst 日程 + Base-case EPS 路徑 + 會計年度截止
    # + EPS 口徑。型別檢查 only（消費端做 skip-and-log shape validation，
    # validator 不擋回填與欄位演進，故不驗 list 元素 / dict 值的形狀）。
    "catalysts": (list,),
    "base_eps_path": (dict,),
    "fy_end_month": (int,),
    "eps_basis": (str,),
    # v14.4/v14.5 archetype & QC-42 cyclical-lens metadata. Type-check only
    # (same policy as eps_basis: consumers skip-and-log, validator never blocks
    # field evolution). cycle_position / cycle_verdict / rearm_trigger are v14.5.
    "archetype": (str,),
    "rearm_trigger": (str,),
    "cycle_position": (str,),
    "cycle_verdict": (str,),
    # Fundamental sub-grades surfaced to the screener (present in most v14 DDs;
    # dd_screener_dd_loader already reads moat_execution / moat_pricing_power /
    # upside_5y_pct). Previously unregistered — added so their type is checked.
    # NB: moat_execution / moat_pricing_power are emitted as /10 numeric scores
    # across the live corpus (one legacy str in pricing_power) — accept numeric
    # AND str so no existing report turns red and future letter grades are OK.
    "endo_growth_ceiling": (int, float),
    "capalloc_grade": (str,),
    "moat_execution": (int, float, str),
    "moat_pricing_power": (int, float, str),
    "upside_5y_pct": (int, float),
}

# Keys knowingly tolerated beyond required/optional — silences their warning.
# Empty by design: ad-hoc descriptive keys (name / company / regime /
# market_cap_b / inception_dd / …) SHOULD surface as warnings so schema drift
# stays visible. Warnings are warn-only and never fail CI (see main()).
WHITELIST_KEYS: set = set()


def _known_keys() -> set:
    """Union of required ∪ v13-required ∪ v13-optional ∪ whitelist keys."""
    return (
        set(REQUIRED_FIELDS)
        | set(V13_REQUIRED_FIELDS)
        | set(V13_OPTIONAL_TYPES)
        | WHITELIST_KEYS
    )


def _is_v13(meta: dict) -> bool:
    # "v13-style" merged DD+DCA contract — applies to v13.x and v14.x (same fields).
    s = meta.get("schema")
    return isinstance(s, str) and s.startswith(("v13", "v14"))


def _type_name(expected_type) -> str:
    return (
        expected_type.__name__
        if isinstance(expected_type, type)
        else " or ".join(t.__name__ for t in expected_type)
    )


def validate_meta(meta: dict):
    """Return (errors, warnings). Empty errors = valid (warnings never fail CI)."""
    errs = []
    warns = []

    # Unknown-key sweep (warn-only): flag any top-level key not in the
    # required ∪ v13-required ∪ v13-optional ∪ whitelist union. Scoped to the
    # v13/v14 merged-report contract only — legacy v12 reports carry ~200 organic
    # ad-hoc keys (frozen corpus) that we deliberately do NOT police. On v13+,
    # ad-hoc descriptive keys (SE: name/inception_dd/regime, VIK: market_cap_b, …)
    # are tolerated but surfaced so schema drift on new reports stays visible.
    if _is_v13(meta):
        known = _known_keys()
        for k in meta:
            if k not in known:
                warns.append(
                    f"unknown dd-meta key: {k!r} (not in required∪optional∪whitelist)"
                )

    # Required fields: presence + type
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in meta:
            errs.append(f"missing required field: {field}")
            continue
        v = meta[field]
        if v is None:
            errs.append(f"{field}: must not be null (omit field instead)")
            continue
        if not isinstance(v, expected_type):
            type_name = (
                expected_type.__name__
                if isinstance(expected_type, type)
                else " or ".join(t.__name__ for t in expected_type)
            )
            errs.append(
                f"{field}: expected {type_name}, got {type(v).__name__} ({v!r})"
            )

    # Enum: allowed values only
    for field, allowed in ENUM_FIELDS.items():
        v = meta.get(field)
        if v is not None and v not in allowed:
            errs.append(
                f"{field}: invalid value {v!r}; allowed: {sorted(allowed)}"
            )

    # Date format
    date_v = meta.get("date")
    if isinstance(date_v, str) and not DATE_RE.match(date_v):
        errs.append(f"date: format must be YYYY-MM-DD, got {date_v!r}")

    # Schema format
    schema_v = meta.get("schema")
    if isinstance(schema_v, str) and not SCHEMA_RE.match(schema_v):
        errs.append(
            f"schema: must match ^v1[234]\\.\\d+$ "
            f"(e.g. v12.0 / v13.0 / v14.5), got {schema_v!r}"
        )

    # Numeric ranges
    for field, (lo, hi) in NUMERIC_RANGES.items():
        v = meta.get(field)
        if isinstance(v, (int, float)) and not (lo <= v <= hi):
            errs.append(f"{field}: {v} out of range [{lo}, {hi}]")

    # Stress object structure
    stress = meta.get("stress")
    if isinstance(stress, dict):
        for k in ("pass", "total"):
            if k not in stress:
                errs.append(f"stress.{k}: required key missing")
            elif not isinstance(stress[k], int):
                errs.append(
                    f"stress.{k}: must be int, got {type(stress[k]).__name__}"
                )
        if "pass" in stress and "total" in stress:
            if stress["total"] <= 0:
                errs.append(f"stress.total: must be > 0, got {stress['total']}")
            if stress["pass"] < 0 or (
                stress["total"] > 0 and stress["pass"] > stress["total"]
            ):
                errs.append(
                    f"stress: pass {stress['pass']} > total {stress['total']}"
                )

    # Oneliner hard cap (soft cap 120 is documented in skill, hard cap here)
    one = meta.get("oneliner")
    if isinstance(one, str) and len(one) > ONELINER_HARD_CAP:
        errs.append(
            f"oneliner: {len(one)} chars exceeds hard cap {ONELINER_HARD_CAP}"
        )

    # v13 merged-report contract (only enforced when schema is v13.x)
    if _is_v13(meta):
        for field, expected_type in V13_REQUIRED_FIELDS.items():
            if field not in meta:
                errs.append(f"missing required field (v13): {field}")
                continue
            v = meta[field]
            if v is None:
                errs.append(f"{field}: must not be null (omit field instead)")
            elif not isinstance(v, expected_type):
                errs.append(
                    f"{field}: expected {_type_name(expected_type)}, "
                    f"got {type(v).__name__} ({v!r})"
                )
        for field, allowed in V13_ENUM_FIELDS.items():
            v = meta.get(field)
            if v is not None and v not in allowed:
                errs.append(
                    f"{field}: invalid value {v!r}; allowed: {sorted(allowed)}"
                )
        for field, expected_type in V13_OPTIONAL_TYPES.items():
            v = meta.get(field)
            if v is not None and not isinstance(v, expected_type):
                errs.append(
                    f"{field}: expected {_type_name(expected_type)}, "
                    f"got {type(v).__name__} ({v!r})"
                )

        # fy_end_month must be a real calendar month — the T-minus catalyst
        # consumer reads it, so a bad value (e.g. 13) is an error, not a warning.
        fem = meta.get("fy_end_month")
        if isinstance(fem, int) and not isinstance(fem, bool) and not (1 <= fem <= 12):
            errs.append(f"fy_end_month: {fem} out of range [1, 12]")

    return errs, warns


def validate_file(path: Path) -> dict:
    """Inspect one DD HTML; return {status, errors[, meta_keys]}.

    status:
      - "non_v12": meta tag missing or pre-v12 (out of scope; skipped from CI)
      - "missing_block": in-scope DD without <script id="dd-meta">
      - "parse_error": JSON could not be parsed
      - "invalid": JSON parsed but failed validation
      - "ok": fully valid
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {"status": "read_error", "errors": [f"OSError: {e}"]}

    version_m = META_VERSION_RE.search(text)
    version = version_m.group(1) if version_m else ""
    # In scope = v12.x (legacy DD) or v13.x (merged DD+DCA). The "non_v12"
    # status label is kept for back-compat with the counts/printing below;
    # it now means "out of scope" (pre-v12).
    if not version.startswith(IN_SCOPE_VERSIONS):
        return {"status": "non_v12", "version": version}

    meta_m = DD_META_RE.search(text)
    if not meta_m:
        return {
            "status": "missing_block",
            "errors": ["no <script id=\"dd-meta\"> found in <head>"],
        }

    raw = meta_m.group(1).strip()
    try:
        meta = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"status": "parse_error", "errors": [f"JSON parse error: {e}"]}

    errs, warns = validate_meta(meta)
    result = {"ticker": meta.get("ticker")}
    if warns:
        result["warnings"] = warns
    if errs:
        result["status"] = "invalid"
        result["errors"] = errs
    else:
        result["status"] = "ok"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files", nargs="*", help="Specific DD HTML files (default: all in docs/dd/)"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Always exit 0; just report issues (for diagnostic / backfill flow).",
    )
    parser.add_argument(
        "--json", dest="json_out", action="store_true", help="JSON output."
    )
    args = parser.parse_args()

    if args.files:
        targets = [Path(p) for p in args.files]
    else:
        targets = sorted(DD_DIR.glob("DD_*.html"))

    results = []
    for p in targets:
        r = validate_file(p)
        r["file"] = p.name
        results.append(r)

    if args.json_out:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        bad = any(r["status"] not in ("ok", "non_v12") for r in results)
        sys.exit(0 if (args.report or not bad) else 1)

    # Plain-text summary
    counts = {"ok": 0, "non_v12": 0, "missing_block": 0, "parse_error": 0, "invalid": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    n_warn_files = sum(1 for r in results if r.get("warnings"))
    n_warn_total = sum(len(r.get("warnings", [])) for r in results)

    print(f"Scanned {len(results)} DD file(s):")
    print(f"  ✅ ok                : {counts['ok']}")
    print(f"  ⚠  missing dd-meta  : {counts.get('missing_block', 0)}")
    print(f"  ❌ JSON parse error : {counts.get('parse_error', 0)}")
    print(f"  ❌ validation error : {counts.get('invalid', 0)}")
    print(f"  ↪  non-v12 (skipped): {counts.get('non_v12', 0)}")
    print(f"  ⚠  warnings         : {n_warn_total} across {n_warn_files} file(s) (non-blocking)")

    # Detailed report
    bad_statuses = ("missing_block", "parse_error", "invalid")
    bad = [r for r in results if r["status"] in bad_statuses]
    if bad:
        print()
        print("=" * 70)
        for r in bad:
            ticker = r.get("ticker", "?")
            print(f"\n[{r['status'].upper()}] {r['file']} (ticker={ticker})")
            for e in r.get("errors", []):
                print(f"    - {e}")

    # Warnings (warn-only; never affects exit code)
    warned = [r for r in results if r.get("warnings")]
    if warned:
        print()
        print("=" * 70)
        print("WARNINGS (non-blocking):")
        for r in warned:
            print(f"\n[WARN] {r['file']} (ticker={r.get('ticker', '?')})")
            for w in r["warnings"]:
                print(f"    - {w}")

    if bad and not args.report:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
