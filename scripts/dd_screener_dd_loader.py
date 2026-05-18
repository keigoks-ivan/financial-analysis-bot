"""DD Screener Phase 1 — identity + DD-meta-sourced fields loader.

Public API:
    load_dd_universe(dd_dir, dca_dir) -> list[dict]

CLI self-test:
    python3 scripts/dd_screener_dd_loader.py
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

# ── path setup ───────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from dd_meta_reader import iter_dd_metas  # noqa: E402

# ── constants ─────────────────────────────────────────────────────────────────

# Required fields in dd-meta (skip ticker if any absent)
_REQUIRED = ("moat_score", "signal", "trap", "val")

# Moat-grade key: newer DDs use 'moat_grade'; most use 'moat'
_MOAT_GRADE_KEYS = ("moat_grade", "moat")

# Known moat_trend text → arrow mappings (Chinese labels used in early DDs)
_TREND_NORM: dict[str, str] = {
    "加深": "↑",
    "擴大": "↑",
    "改善": "↑",
    "上升": "↑",
    "↑": "↑",
    "穩定": "→",
    "持平": "→",
    "→": "→",
    "縮窄": "↓",
    "衰退": "↓",
    "下降": "↓",
    "↓": "↓",
}

# DD filename date pattern: DD_{STEM}_{YYYYMMDD}[_suffix].html
_DD_FILENAME_DATE_RE = re.compile(r"^DD_.+?_(\d{8})(?:_.*)?\.html$")


# ── helpers ───────────────────────────────────────────────────────────────────

def _ticker_to_filename_stem(ticker: str) -> str:
    """Convert canonical ticker to filename stem (strip dots).

    Examples:
        NVDA       -> NVDA
        2330.TW    -> 2330TW
        6857.T     -> 6857T
        RMS        -> RMS
    """
    return ticker.replace(".", "")


def _normalize_moat_trend(raw: Optional[str]) -> str:
    """Normalize moat_trend text to arrow symbol; default '↑' if absent/unknown."""
    if not raw:
        return "↑"
    normed = _TREND_NORM.get(raw.strip())
    if normed:
        return normed
    # If it's already an arrow, pass through
    if raw.strip() in ("↑", "→", "↓"):
        return raw.strip()
    # Unknown string — default to '↑' (locked decision per schema doc)
    return "↑"


def _extract_date_from_dd_filename(filename: str) -> Optional[str]:
    """Return 'YYYY-MM-DD' from 'DD_{STEM}_{YYYYMMDD}[_suffix].html', or None."""
    m = _DD_FILENAME_DATE_RE.match(filename)
    if not m:
        return None
    d = m.group(1)
    return f"{d[:4]}-{d[4:6]}-{d[6:8]}"


def _find_latest_dca(dca_dir: Path, ticker: str) -> tuple[Optional[str], Optional[str]]:
    """Return (dca_path, dca_date) for the latest DCA file for ticker.

    DCA files follow DCA_{STEM}_{YYYYMMDD}.html where STEM = ticker with dots stripped.
    Returns (None, None) if no DCA exists.
    """
    stem = _ticker_to_filename_stem(ticker)
    pattern = str(dca_dir / f"DCA_{stem}_*.html")
    matches = sorted(glob.glob(pattern))
    if not matches:
        return None, None

    # Pick latest by filename date (lexicographic sort of YYYYMMDD is correct)
    latest_path = Path(matches[-1])
    filename = latest_path.name

    # Parse date from filename: DCA_{STEM}_{YYYYMMDD}.html
    date_re = re.compile(r"^DCA_.+?_(\d{8})\.html$")
    dm = date_re.match(filename)
    if not dm:
        return None, None

    d = dm.group(1)
    dca_date = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    dca_path = f"/dca/{filename}"
    return dca_path, dca_date


def _latest_per_ticker_with_paths(
    dd_dir: Path,
) -> dict[str, tuple[Path, dict]]:
    """Return {ticker: (path, meta)} keeping the latest DD per ticker.

    Uses dd_meta_reader.iter_dd_metas; deduplicates by ticker keeping the
    highest 'date' value (same logic as latest_per_ticker, but preserves path).
    """
    best: dict[str, tuple[Path, dict]] = {}
    for path, meta in iter_dd_metas(dd_dir):
        ticker = meta.get("ticker")
        date = meta.get("date")
        if not ticker or not date:
            continue
        prev = best.get(ticker)
        if prev is None or date > prev[1].get("date", ""):
            best[ticker] = (path, meta)
    return best


# ── public API ────────────────────────────────────────────────────────────────

def load_dd_universe(
    dd_dir: str | Path = "docs/dd",
    dca_dir: str | Path = "docs/dca",
) -> list[dict]:
    """Return one dict per unique ticker (latest DD per ticker), populated with
    the identity + DD-meta-sourced fields per scripts/dd_screener_schema.md.

    Skip any DD whose dd-meta lacks moat_score / signal / trap / val
    (these are required by the schema). Log skipped tickers to stderr.

    Each returned dict has:
        ticker, name, sector,
        moat_score, moat_grade, moat_trend,
        moat_execution, moat_pricing_power,   # v12.3+ optional, None for legacy DDs
        signal, trap, val,
        upside_mid_pct, upside_5y_pct, fpe_fy2,
        pct_5y, growth_durability, quality_score, ai_risk,  # v1.2 quality-entry inputs
        dd_path, dd_date,
        dca_path, dca_date
    """
    dd_dir = Path(dd_dir)
    dca_dir = Path(dca_dir)

    per_ticker = _latest_per_ticker_with_paths(dd_dir)
    results: list[dict] = []

    for ticker, (path, meta) in sorted(per_ticker.items()):
        # ── required field checks ─────────────────────────────────────────
        skip = False
        for field in _REQUIRED:
            if meta.get(field) is None:
                print(f"SKIP {ticker}: missing required field {field}", file=sys.stderr)
                skip = True
                break
        if skip:
            continue

        # moat_grade: prefer 'moat_grade', fallback to 'moat'
        moat_grade: Optional[str] = None
        for key in _MOAT_GRADE_KEYS:
            val = meta.get(key)
            if val is not None:
                moat_grade = str(val)
                break

        if moat_grade is None:
            print(f"SKIP {ticker}: missing required field moat_grade/moat", file=sys.stderr)
            continue

        # ── identity fields ───────────────────────────────────────────────
        name: str = (
            meta.get("company")
            or meta.get("name")
            or ticker
        )
        sector: str = meta.get("industry") or ""

        # ── moat fields ───────────────────────────────────────────────────
        moat_score: float = meta["moat_score"]
        moat_trend: str = _normalize_moat_trend(meta.get("moat_trend"))

        # ── signal / trap / val ───────────────────────────────────────────
        signal: str = meta["signal"]
        trap: str = meta["trap"]
        val_field: str = meta["val"]

        # ── upside fields ─────────────────────────────────────────────────
        upside_mid_pct = meta.get("upside_mid_pct")
        upside_5y_pct = meta.get("upside_5y_pct")

        # ── 2Y forward P/E (FY+2; same value the /research/ table shows) ─
        fpe_fy2 = meta.get("fpe_fy2")

        # ── quality-entry v1.2 fields (propagate dd-meta as-is, allow null) ──
        # `pct_5y` = 5Y FwdPE percentile (lower = cheaper); main Entry-pillar anchor.
        # `growth_durability` (1-10), `quality_score` (1-10) — DD §1 analyst scores.
        # `moat_execution` / `moat_pricing_power` (1-10) — v12.3+ two-axis decomp.
        # `ai_risk` — 🟢/🟡/🔴 disrupt-risk light, used as quality-entry veto.
        pct_5y = meta.get("pct_5y")
        growth_durability = meta.get("growth_durability")
        quality_score = meta.get("quality_score")
        moat_execution = meta.get("moat_execution")
        moat_pricing_power = meta.get("moat_pricing_power")
        ai_risk = meta.get("ai_risk")
        # v1.3: price_at_dd 用於 live FwdPE drift 計算 (live_fpe ≈ fpe_fy2 × price_now/price_at_dd)
        price_at_dd = meta.get("price_at_dd")

        # ── dd_path / dd_date ─────────────────────────────────────────────
        dd_filename = path.name
        dd_path = f"/dd/{dd_filename}"
        dd_date = _extract_date_from_dd_filename(dd_filename) or meta.get("date")

        # ── DCA lookup ────────────────────────────────────────────────────
        dca_path, dca_date = _find_latest_dca(dca_dir, ticker)

        results.append({
            "ticker": ticker,
            "name": name,
            "sector": sector,
            "moat_score": moat_score,
            "moat_grade": moat_grade,
            "moat_trend": moat_trend,
            "moat_execution": moat_execution,
            "moat_pricing_power": moat_pricing_power,
            "signal": signal,
            "trap": trap,
            "val": val_field,
            "upside_mid_pct": upside_mid_pct,
            "upside_5y_pct": upside_5y_pct,
            "fpe_fy2": fpe_fy2,
            "pct_5y": pct_5y,
            "growth_durability": growth_durability,
            "quality_score": quality_score,
            "ai_risk": ai_risk,
            "price_at_dd": price_at_dd,
            "dd_path": dd_path,
            "dd_date": dd_date,
            "dca_path": dca_path,
            "dca_date": dca_date,
        })

    return results


# ── CLI self-test ─────────────────────────────────────────────────────────────

def main() -> None:
    import collections

    # Resolve relative to repo root (one level above scripts/)
    repo_root = Path(__file__).parent.parent
    dd_dir = repo_root / "docs" / "dd"
    dca_dir = repo_root / "docs" / "dca"

    universe = load_dd_universe(dd_dir, dca_dir)

    # ── summary stats ─────────────────────────────────────────────────────
    signal_counts: dict[str, int] = collections.Counter(u["signal"] for u in universe)
    with_dca = sum(1 for u in universe if u["dca_path"] is not None)
    with_explicit_trend = sum(1 for u in universe if u["moat_trend"] != "↑"
                               or (u["ticker"] in {v["ticker"] for v in universe
                                                    if v.get("moat_trend") != "↑"}))
    # Count how many had explicit moat_trend in dd-meta (not defaulted)
    # Reload to count: check raw meta
    raw_metas = [m for _, m in iter_dd_metas(dd_dir)]
    from dd_meta_reader import latest_per_ticker
    latest_raw = latest_per_ticker(raw_metas)
    explicit_trend_count = sum(1 for m in latest_raw if m.get("moat_trend"))

    print("=" * 60)
    print("DD Screener Universe — load_dd_universe() summary")
    print("=" * 60)
    print(f"Total tickers loaded:          {len(universe)}")
    print(f"  with DCA report:             {with_dca}")
    print(f"  with explicit moat_trend:    {explicit_trend_count}")
    print()
    print("Signal breakdown:")
    for sig in sorted(signal_counts, key=lambda s: ["A+", "A", "B", "C", "X"].index(s)
                      if s in ["A+", "A", "B", "C", "X"] else 99):
        print(f"  {sig:4s}: {signal_counts[sig]}")
    print()

    # ── sample dict ───────────────────────────────────────────────────────
    sample = universe[0] if universe else {}
    # Prefer NVDA for a meaningful sample
    nvda = next((u for u in universe if u["ticker"] == "NVDA"), None)
    if nvda:
        sample = nvda

    print("Sample entry:")
    print(json.dumps(sample, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
