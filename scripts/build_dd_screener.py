#!/usr/bin/env python3
"""DD Screener Phase 1 — stateless orchestrator.

Pipeline:
  Step 1-2  load 98 DDs + latest DCA per ticker  (dd_screener_dd_loader)
  Step 3    hybrid quality data (QGM + yfinance)  (dd_screener_quality)
  Step 4    MA snapshot                            (dd_screener_ma)
  Step 5    compute pass/fail per criterion
  Step 6    rule-based take-away
  Step 7    write docs/dd-screener/latest.json

Output schema: scripts/dd_screener_schema.md (locked v1.0)

Usage:
  python3 scripts/build_dd_screener.py             # full universe, ~6-8 min
  python3 scripts/build_dd_screener.py --top 10    # smoke-test first 10 tickers
  python3 scripts/build_dd_screener.py --dry-run   # don't write file
  python3 scripts/build_dd_screener.py --no-ma     # skip MA fetch (faster smoke)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dd_screener_dd_loader import load_dd_universe  # noqa: E402
from dd_screener_quality import (  # noqa: E402
    EU_SUFFIX_MAP,
    get_quality_for_ticker,
    load_qgm_index,
)
from dd_screener_ma import compute_ma_snapshot  # noqa: E402

OUTPUT_DIR = ROOT / "docs" / "dd-screener"
OUTPUT_PATH = OUTPUT_DIR / "latest.json"

# Locked v1.0 criteria — matches scripts/dd_screener_schema.md
CRITERIA = [
    {"key": "fcf",   "label": "FCF≥10%",  "threshold": 10.0, "invert": False, "unit": "%"},
    {"key": "roic",  "label": "ROIC≥15%", "threshold": 15.0, "invert": False, "unit": "%"},
    {"key": "eps2y", "label": "EPS≥15%",  "threshold": 15.0, "invert": False, "unit": "%"},
    {"key": "peg",   "label": "PEG≤2.0",  "threshold": 2.0,  "invert": True,  "unit": "x"},
    {"key": "de",    "label": "D/E≤0.7",  "threshold": 0.7,  "invert": True,  "unit": "x"},
]

PRESETS = {
    "MLB": {"fcf": 10.0, "roic": 15.0, "eps2y": 15.0, "peg": 2.0, "de": 0.7},
    "3A":  {"fcf": 8.0,  "roic": 12.0, "eps2y": 12.0, "peg": 2.5, "de": 1.0},
}

DEFAULT_FILTER = {"moat_min": 9.5, "directions": ["↑", "→"]}


# ---------------------------------------------------------------------------
# Step 5: pass/fail
# ---------------------------------------------------------------------------


def evaluate_criteria(quality: dict) -> tuple[int, list[str]]:
    """Return (pass_count, fail_criteria) using locked MLB thresholds.

    A null field is treated as a failed criterion (can't verify), recorded
    in fail_criteria so the front-end can show "—" rather than red.
    """
    fails: list[str] = []
    passes = 0
    for c in CRITERIA:
        v = quality.get(c["key"])
        if v is None:
            fails.append(c["key"])
            continue
        ok = (v <= c["threshold"]) if c["invert"] else (v >= c["threshold"])
        if ok:
            passes += 1
        else:
            fails.append(c["key"])
    return passes, fails


# ---------------------------------------------------------------------------
# Step 6: rule-based take-away
# ---------------------------------------------------------------------------


def _signal_rank(signal: str) -> int:
    return {"A+": 5, "A": 4, "B": 3, "C": 2, "X": 1}.get(signal, 0)


def build_takeaway(stocks: list[dict]) -> dict:
    """Generate rule-based narrative from finalized stock list."""
    pass5 = [s for s in stocks if s["pass_count"] == 5]
    pass4 = [s for s in stocks if s["pass_count"] == 4]
    pass3 = [s for s in stocks if s["pass_count"] == 3]

    # Top tickers among pass_5 by signal rank → upside_mid_pct
    top_5 = sorted(
        pass5,
        key=lambda s: (
            -_signal_rank(s["signal"]),
            -(s.get("upside_mid_pct") or -1e9),
            s["ticker"],
        ),
    )
    top_tickers_by_signal = [s["ticker"] for s in top_5[:3]]

    # Sector breakdown: only meaningful when sector is non-empty.
    sectors = Counter(s["sector"] for s in pass5 if s["sector"])
    sector_breakdown = [
        {"sector": sec, "count": n}
        for sec, n in sectors.most_common(5)
    ]

    # Edge cases: pass_4 candidates with S-tier moat (品質卓越但卡 1 條 QGM 硬閾值)
    edge_cases: list[str] = []
    for s in sorted(pass4, key=lambda x: (-x["moat_score"], x["ticker"])):
        if s["moat_score"] >= 9.5 and s["fail_criteria"]:
            fail_names = "+".join(s["fail_criteria"]).upper()
            edge_cases.append(
                f"{s['ticker']} 差 {fail_names} — S 級護城河卡 QGM 硬閾值"
            )
        if len(edge_cases) >= 5:
            break

    # Summary line — narrative version of the counts
    total_candidates = len(pass5) + len(pass4) + len(pass3)
    if pass5:
        if sector_breakdown:
            top_sec = sector_breakdown[0]
            summary = (
                f"{len(pass5)}/{len(stocks)} 完全符合 — "
                f"top 集中於 {top_sec['sector']}（{top_sec['count']} 檔）。"
                f"差一條 {len(pass4)} 檔、差兩條 {len(pass3)} 檔。"
            )
        else:
            summary = (
                f"{len(pass5)}/{len(stocks)} 完全符合 — "
                f"差一條 {len(pass4)}、差兩條 {len(pass3)}（共 {total_candidates} 候選）。"
            )
    else:
        summary = (
            f"0/{len(stocks)} 完全符合 — "
            f"差一條 {len(pass4)} 為最接近 setup（共 {total_candidates} 候選）。"
        )

    return {
        "summary": summary,
        "top_tickers_by_signal": top_tickers_by_signal,
        "sector_breakdown": sector_breakdown,
        "edge_cases": edge_cases,
    }


# ---------------------------------------------------------------------------
# Step 7: orchestrate
# ---------------------------------------------------------------------------


def _sort_key(s: dict) -> tuple:
    return (
        -s["pass_count"],
        -(s.get("moat_score") or 0),
        -(s.get("upside_mid_pct") if s.get("upside_mid_pct") is not None else -1e9),
        s["ticker"],
    )


def _yf_ticker_for_ma(dd_ticker: str) -> str:
    """Same suffix resolution as quality module."""
    return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}" if dd_ticker in EU_SUFFIX_MAP else dd_ticker


def _empty_ma() -> dict:
    return {
        "price": None, "w52": None, "w104": None, "w250": None,
        "slope_w250_pct": None, "drift_4w_pct": None,
        "above_w52": None, "above_w250": None,
    }


def enrich_ticker(
    entry: dict,
    qgm_index: dict,
    skip_ma: bool,
) -> dict:
    """Add quality + MA + pass_count + fail_criteria to a loader entry."""
    t = entry["ticker"]
    quality, source = get_quality_for_ticker(t, qgm_index)
    pass_count, fails = evaluate_criteria(quality)

    if skip_ma:
        ma = _empty_ma()
    else:
        try:
            ma = compute_ma_snapshot(_yf_ticker_for_ma(t))
        except Exception:
            ma = _empty_ma()

    return {
        **entry,
        **quality,
        "pass_count": pass_count,
        "fail_criteria": fails,
        "quality_source": source,
        "ma": ma,
    }


def build(top_n: int | None, skip_ma: bool, dry_run: bool, workers: int) -> dict:
    print(f"=== DD Screener build · {datetime.now().isoformat(timespec='seconds')} ===\n")
    t0 = time.time()

    # Step 1-2
    universe = load_dd_universe()
    if top_n:
        universe = universe[:top_n]
    print(f"  Step 1-2  DD universe: {len(universe)} tickers")

    # Step 3 prep
    qgm_index = load_qgm_index()
    print(f"  Step 3    QGM index: {len(qgm_index)} entries ({sum(1 for s,_ in qgm_index.values() if s=='qgm-us')} US, {sum(1 for s,_ in qgm_index.values() if s=='qgm-tw')} TW)")

    # Step 3 + 4 enrichment, parallel
    print(f"  Step 3-4  enriching (workers={workers}, skip_ma={skip_ma}) ...")
    enriched: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(enrich_ticker, e, qgm_index, skip_ma): e["ticker"]
            for e in universe
        }
        for i, fut in enumerate(as_completed(futs), 1):
            t = futs[fut]
            try:
                row = fut.result()
                enriched.append(row)
            except Exception as exc:
                print(f"    ERR {t}: {exc}", file=sys.stderr)
            if i % 10 == 0 or i == len(futs):
                elapsed = time.time() - t0
                print(f"    [{i:>3}/{len(futs)}] {elapsed:.0f}s")

    # Step 5: sort (pass/fail already computed above)
    enriched.sort(key=_sort_key)

    # Source-tag breakdown
    src_counts = Counter(s["quality_source"] for s in enriched)
    print(f"  Step 5    quality sources: {dict(src_counts)}")

    # Step 6: take-away
    takeaway = build_takeaway(enriched)
    print(f"  Step 6    take-away: pass5={sum(1 for s in enriched if s['pass_count']==5)} "
          f"pass4={sum(1 for s in enriched if s['pass_count']==4)} "
          f"pass3={sum(1 for s in enriched if s['pass_count']==3)}")

    # Summary
    pass_counts = Counter(s["pass_count"] for s in enriched)
    no_data = sum(
        1 for s in enriched
        if all(s.get(c["key"]) is None for c in CRITERIA)
    )
    summary = {
        "pass_5":  pass_counts.get(5, 0),
        "pass_4":  pass_counts.get(4, 0),
        "pass_3":  pass_counts.get(3, 0),
        "pass_lt3": sum(v for k, v in pass_counts.items() if k < 3),
        "no_data": no_data,
    }

    # Build final document
    tz_taipei = timezone(timedelta(hours=8))
    now = datetime.now(tz_taipei)
    doc = {
        "schema_version": "1.0",
        "run_timestamp": now.isoformat(timespec="seconds"),
        "as_of": now.strftime("%Y-%m-%d"),
        "universe_size": len(enriched),
        "default_preset": "MLB",
        "criteria": CRITERIA,
        "presets": PRESETS,
        "default_filter": DEFAULT_FILTER,
        "summary": summary,
        "stocks": enriched,
        "takeaway": takeaway,
    }

    print(f"\n  ✓ Elapsed: {time.time()-t0:.0f}s")

    if dry_run:
        print(f"  (dry-run) skipping write to {OUTPUT_PATH}")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Wrote {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)")

    return doc


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top", type=int, default=None, help="Limit to first N tickers (smoke test)")
    p.add_argument("--no-ma", action="store_true", help="Skip MA fetch (faster smoke)")
    p.add_argument("--dry-run", action="store_true", help="Don't write latest.json")
    p.add_argument("--workers", type=int, default=8, help="Concurrent yfinance fetchers (default 8)")
    args = p.parse_args()
    build(top_n=args.top, skip_ma=args.no_ma, dry_run=args.dry_run, workers=args.workers)


if __name__ == "__main__":
    main()
