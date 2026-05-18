#!/usr/bin/env python3
"""Monthly fundamentals cache builder — region-split (US / TW).

Builds `docs/cache/fundamentals-{us,tw}.json` from:
  - QGM-region passthrough for the ~94 tickers QGM already covers (quality + trends + EPS)
  - yfinance fetch for everyone else (.info / .balance_sheet / .income_stmt /
    .cashflow / .earnings_estimate / .quarterly_income_stmt / .quarterly_cashflow)

Refresh cadence: monthly (1st of month). See plan: cache layer is producer-only,
no consumer is wired up yet — viewer page at /cache/ shows results.

Universe per region:
  us: DD non-TW ∪ SP500+NQ100 extras (~560 tickers)
  tw: DD TW ∪ ETF_0050+0051+00714 (~200 tickers)

Schema v1.0 — per ticker:
  currency: USD | TWD | EUR | JPY | ...
  quality:        {fcf, roic, eps2y, peg, de}          # percentages 0-100 except peg/de (ratios)
  eps_estimate:   {fy0, fy1}                            # dollar values in native currency
  info:           {forwardEps, trailingEps, bookValue}  # native currency
  growth:         {rev_growth_yoy, rev_cagr_3y}         # percentages
  margins:        {gross, operating, net}               # percentages
  trends:         {gm_5y_trend, roic_5y_stability,      # qgm-only; null for non-QGM
                   fcf_5y_normalized, quality_score}
  quarterly:      {eps_yoy_neg_streak, fcf_margin_decline_streak}
  quality_source: qgm-us | qgm-tw | yfinance | yfinance-eu | ...
  fetched_at:     ISO timestamp

CLI:
  python3 scripts/build_fundamentals_cache.py --region us
  python3 scripts/build_fundamentals_cache.py --region tw
  python3 scripts/build_fundamentals_cache.py --region us --dry-run
  python3 scripts/build_fundamentals_cache.py --region us --top 10  # smoke test
  python3 scripts/build_fundamentals_cache.py --region us --no-resume  # ignore checkpoint
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "pandas", "-q"])
    import yfinance as yf
    import pandas as pd

logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dd_screener_dd_loader import load_dd_universe  # noqa: E402
from dd_screener_quality import (  # noqa: E402
    QGM_US_PATH,
    QGM_TW_PATH,
    load_qgm_index,
    compute_yfinance_quality,
    _yf_ticker_for,
)

# ── Partial-success policy ────────────────────────────────────────────────────
ABORT_FAILURE_RATIO = 0.80   # >= 80% failures → abort (keep prior cache)
PARTIAL_ERROR_RATIO = 0.20   # >= 20% → red badge
PARTIAL_WARN_RATIO  = 0.05   # >= 5%  → yellow badge

# ── Schema constants ──────────────────────────────────────────────────────────
SCHEMA_VERSION = "1.0"
STALE_AFTER_DAYS = 35
OUTPUT_DIR = ROOT / "docs" / "cache"
CHECKPOINT_DIR = ROOT / ".cache"


# ─────────────────────────────────────────────────────────────────────────────
# Universe builders
# ─────────────────────────────────────────────────────────────────────────────

def _is_tw(ticker: str) -> bool:
    """TW listing: .TW / .TWO suffix OR bare 4-digit numeric (DD convention 2330 = 2330.TW)."""
    if ticker.endswith(".TW") or ticker.endswith(".TWO"):
        return True
    if ticker.isdigit() and len(ticker) == 4:
        return True
    return False


def _yf_ticker_for_local(ticker: str) -> str:
    """Like dd_screener_quality._yf_ticker_for but also map bare 4-digit TW to .TW form."""
    if ticker.isdigit() and len(ticker) == 4:
        return f"{ticker}.TW"
    return _yf_ticker_for(ticker)


def _load_sp500_nq100() -> list[str]:
    """Reuse screener.py's S&P 500 + NQ 100 extras list."""
    from screener import fetch_sp500_tickers, NQ100_EXTRAS  # noqa: E402
    sp500 = fetch_sp500_tickers() or {}
    return sorted(set(sp500.keys()) | set(NQ100_EXTRAS.keys()))


def _load_twse_etfs() -> list[str]:
    """Reuse screener_tw.py's ETF dicts (0050 + 0051 + 00714)."""
    from screener_tw import ETF_0050, ETF_0051, ETF_00714  # noqa: E402
    return sorted(set(ETF_0050.keys()) | set(ETF_0051.keys()) | set(ETF_00714.keys()))


def build_universe(region: str) -> list[str]:
    """Per-region universe = DD-of-region ∪ region's market index list."""
    dd = [e["ticker"] for e in load_dd_universe()]
    if region == "us":
        # Non-TW DD tickers (EU/JP DDs go in the US bucket per plan)
        dd_us = [t for t in dd if not _is_tw(t)]
        market = _load_sp500_nq100()
        return sorted(set(dd_us) | set(market))
    elif region == "tw":
        dd_tw = [t for t in dd if _is_tw(t)]
        market = _load_twse_etfs()
        return sorted(set(dd_tw) | set(market))
    else:
        raise ValueError(f"Unknown region: {region}")


# ─────────────────────────────────────────────────────────────────────────────
# Currency inference
# ─────────────────────────────────────────────────────────────────────────────

CURRENCY_BY_SUFFIX = {
    ".TW": "TWD", ".TWO": "TWD",
    ".T": "JPY",
    ".PA": "EUR", ".AS": "EUR", ".MC": "EUR", ".DE": "EUR", ".MI": "EUR",
    ".L": "GBP",
    ".HK": "HKD",
    ".SS": "CNY", ".SZ": "CNY",
}


def _infer_currency(ticker: str) -> str:
    """Heuristic — uses suffix to pick currency; default USD.
    Bare 4-digit numeric (e.g. 2330) → TWD."""
    for suffix, ccy in CURRENCY_BY_SUFFIX.items():
        if ticker.endswith(suffix):
            return ccy
    if ticker.isdigit() and len(ticker) == 4:
        return "TWD"
    return "USD"


# ─────────────────────────────────────────────────────────────────────────────
# Quarterly streaks (mirror quarterly_us.py logic, but inline)
# ─────────────────────────────────────────────────────────────────────────────

def _cell(df, key_substring: str, col):
    if df is None or getattr(df, "empty", True) or col not in df.columns:
        return None
    for r in df.index:
        if key_substring.lower() in str(r).lower():
            v = df.loc[r, col]
            try:
                f = float(v)
                return f if pd.notna(f) else None
            except (TypeError, ValueError):
                return None
    return None


def _fcf_for_quarter(cf_df, col):
    fcf = _cell(cf_df, 'Free Cash Flow', col)
    if fcf is not None:
        return fcf
    ocf = _cell(cf_df, 'Operating Cash Flow', col)
    capex = _cell(cf_df, 'Capital Expenditure', col)
    if ocf is not None and capex is not None:
        return ocf + capex
    return None


def _yoy_streak(quarters, field):
    streak = 0
    for i in range(len(quarters)):
        j = i + 4
        if j >= len(quarters):
            break
        curr = quarters[i].get(field)
        prev = quarters[j].get(field)
        if curr is None or prev is None:
            break
        if curr < prev:
            streak += 1
        else:
            break
    return streak


def fetch_quarterly_streaks(t: yf.Ticker) -> dict:
    """Return {eps_yoy_neg_streak, fcf_margin_decline_streak} or {None, None}."""
    out = {"eps_yoy_neg_streak": None, "fcf_margin_decline_streak": None}
    try:
        is_df = t.quarterly_income_stmt
        if is_df is None or getattr(is_df, "empty", True):
            return out
        cf_df = t.quarterly_cashflow
        cols = sorted(is_df.columns, reverse=True)
        quarters = []
        for col in cols:
            rev = _cell(is_df, "Total Revenue", col)
            eps = _cell(is_df, "Diluted EPS", col) or _cell(is_df, "Basic EPS", col)
            fcf = _fcf_for_quarter(cf_df, col)
            margin = (fcf / rev) if (fcf is not None and rev and rev > 0) else None
            quarters.append({"eps": eps, "fcf_margin": margin})
        out["eps_yoy_neg_streak"] = _yoy_streak(quarters[:8], "eps")
        out["fcf_margin_decline_streak"] = _yoy_streak(quarters[:8], "fcf_margin")
    except Exception:
        pass
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Per-ticker fetcher (combines all sources)
# ─────────────────────────────────────────────────────────────────────────────

def _round(v, digits=2):
    if v is None:
        return None
    try:
        return round(float(v), digits)
    except (TypeError, ValueError):
        return None


def _pct(v, digits=2):
    """0.2007 → 20.07; None → None."""
    if v is None:
        return None
    try:
        return round(float(v) * 100, digits)
    except (TypeError, ValueError):
        return None


def load_qgm_full_records() -> dict[str, dict]:
    """Load full per-ticker QGM records (watch_list + quality_pool + candidates)
    keyed by ticker. Unlike dd_screener_quality.load_qgm_index() which flattens
    to hard_filter_details, this preserves the entire entry so we can extract
    fy1_eps / fy2_eps / quality_breakdown / quality_score / etc.

    First-write-wins precedence: candidates > watch_list > quality_pool.
    """
    out: dict[str, dict] = {}
    for path in (QGM_US_PATH, QGM_TW_PATH):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for pool in ("candidates", "watch_list", "quality_pool"):
            for entry in data.get(pool, []) or []:
                if not isinstance(entry, dict):
                    continue
                t = entry.get("ticker")
                if not t:
                    continue
                if t not in out:
                    out[t] = entry
    return out


def _qgm_passthrough(qgm_full_record: dict) -> dict:
    """Extract A (quality) + EPS + trends from full QGM entry.

    Expected nesting:
      qgm_full_record['hard_filter_details'] = {fcf_margin, roic, eps_cagr_2y_fwd, peg, debt_to_equity}
      qgm_full_record['quality_breakdown']   = {fcf_5y_normalized, roic_5y_stability, gm_5y_trend, ...}
      qgm_full_record['fy1_eps'] / ['fy2_eps']  (dollar values)
      qgm_full_record['quality_score']  (0-100)
    """
    hfd = qgm_full_record.get("hard_filter_details") or {}
    qb = qgm_full_record.get("quality_breakdown") or {}

    quality = {
        "fcf":   _pct((hfd.get("fcf_margin") or {}).get("value")),
        "roic":  _pct((hfd.get("roic") or {}).get("value")),
        "eps2y": _pct((hfd.get("eps_cagr_2y_fwd") or {}).get("value")),
        "peg":   _round((hfd.get("peg") or {}).get("value")),
        "de":    _round((hfd.get("debt_to_equity") or {}).get("value"), 3),
    }

    eps_estimate = {
        "fy0": _round(qgm_full_record.get("fy1_eps"), 4),
        "fy1": _round(qgm_full_record.get("fy2_eps"), 4),
    }

    # gm_5y_trend in QGM is an int direction score; expose raw for now
    gm_dir = (qb.get("gm_5y_trend") or {}).get("direction")
    trends = {
        "fcf_5y_normalized": _round((qb.get("fcf_5y_normalized") or {}).get("avg"), 4),
        "roic_5y_stability": _round((qb.get("roic_5y_stability") or {}).get("pct_above"), 3),
        "gm_5y_trend": gm_dir,
        "quality_score": _round(qgm_full_record.get("quality_score"), 1),
    }
    return {"quality": quality, "eps_estimate": eps_estimate, "trends": trends}


def _yfinance_fetch_full(yf_ticker: str) -> dict:
    """Fetch all 5 yfinance endpoints for a non-QGM ticker. Returns nested dict
    matching schema; missing fields are None."""
    result = {
        "quality": {"fcf": None, "roic": None, "eps2y": None, "peg": None, "de": None},
        "eps_estimate": {"fy0": None, "fy1": None},
        "info": {"forwardEps": None, "trailingEps": None, "bookValue": None},
        "growth": {"rev_growth_yoy": None, "rev_cagr_3y": None},
        "margins": {"gross": None, "operating": None, "net": None},
        "trends": {"gm_5y_trend": None, "roic_5y_stability": None,
                   "fcf_5y_normalized": None, "quality_score": None},
        "quarterly": {"eps_yoy_neg_streak": None, "fcf_margin_decline_streak": None},
        "_fetch_ok": False,
    }
    try:
        t = yf.Ticker(yf_ticker)

        # Quality 5 fields — reuse existing primitive
        q = compute_yfinance_quality(yf_ticker)
        result["quality"] = q

        # EPS estimate — pull from earnings_estimate 0y / +1y rows
        try:
            ee = t.earnings_estimate
            if ee is not None and not getattr(ee, "empty", True):
                for our_key, yf_key in (("fy0", "0y"), ("fy1", "+1y")):
                    try:
                        if yf_key in ee.index:
                            eps = ee.loc[yf_key].get("avg")
                            if eps and eps > 0:
                                result["eps_estimate"][our_key] = _round(eps, 4)
                    except Exception:
                        pass
        except Exception:
            pass

        # Info dict fields
        try:
            info = t.info or {}
            result["info"]["forwardEps"] = _round(info.get("forwardEps"), 4)
            result["info"]["trailingEps"] = _round(info.get("trailingEps"), 4)
            result["info"]["bookValue"] = _round(info.get("bookValue"), 3)

            # Growth (yfinance gives revenueGrowth = YoY decimal)
            result["growth"]["rev_growth_yoy"] = _pct(info.get("revenueGrowth"))

            # Margins (yfinance returns decimals)
            result["margins"]["gross"] = _pct(info.get("grossMargins"))
            result["margins"]["operating"] = _pct(info.get("operatingMargins"))
            result["margins"]["net"] = _pct(info.get("profitMargins"))
        except Exception:
            pass

        # Quarterly streaks
        result["quarterly"] = fetch_quarterly_streaks(t)

        # Mark fetch successful if at least 2 of the 5 quality fields came through
        q_non_null = sum(1 for v in q.values() if v is not None)
        result["_fetch_ok"] = q_non_null >= 2

    except Exception:
        pass
    return result


def fetch_ticker(ticker: str, qgm_index: dict, qgm_full: dict) -> dict:
    """Resolve one ticker → schema-shaped record. QGM passthrough if available.

    qgm_index: from load_qgm_index() — only hard_filter_details (flat, for source-tag)
    qgm_full:  from load_qgm_full_records() — full entry (with quality_breakdown, EPS)
    """
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    currency = _infer_currency(ticker)

    # Check QGM (region-matched in load_qgm_index — returns (source_tag, record))
    qgm_hit = qgm_index.get(ticker)

    if qgm_hit is not None:
        source_tag, _ = qgm_hit
        # Use FULL record for passthrough (has quality_breakdown + EPS); fall back to flat
        full_record = qgm_full.get(ticker, {"hard_filter_details": qgm_hit[1]})
        passthrough = _qgm_passthrough(full_record)

        # Fetch only the missing fields from yfinance (.info + quarterly_*)
        yf_t = _yf_ticker_for_local(ticker)
        info_growth_margins_quarterly = {
            "info": {"forwardEps": None, "trailingEps": None, "bookValue": None},
            "growth": {"rev_growth_yoy": None, "rev_cagr_3y": None},
            "margins": {"gross": None, "operating": None, "net": None},
            "quarterly": {"eps_yoy_neg_streak": None, "fcf_margin_decline_streak": None},
        }
        try:
            t = yf.Ticker(yf_t)
            info = t.info or {}
            info_growth_margins_quarterly["info"]["forwardEps"] = _round(info.get("forwardEps"), 4)
            info_growth_margins_quarterly["info"]["trailingEps"] = _round(info.get("trailingEps"), 4)
            info_growth_margins_quarterly["info"]["bookValue"] = _round(info.get("bookValue"), 3)
            info_growth_margins_quarterly["growth"]["rev_growth_yoy"] = _pct(info.get("revenueGrowth"))
            info_growth_margins_quarterly["margins"]["gross"] = _pct(info.get("grossMargins"))
            info_growth_margins_quarterly["margins"]["operating"] = _pct(info.get("operatingMargins"))
            info_growth_margins_quarterly["margins"]["net"] = _pct(info.get("profitMargins"))
            info_growth_margins_quarterly["quarterly"] = fetch_quarterly_streaks(t)
        except Exception:
            pass

        return {
            "currency": currency,
            **passthrough,
            **info_growth_margins_quarterly,
            "quality_source": source_tag,
            "fetched_at": fetched_at,
            "_fetch_ok": True,  # QGM passthrough never "fails"
        }

    # No QGM → full yfinance fetch
    yf_t = _yf_ticker_for_local(ticker)
    full = _yfinance_fetch_full(yf_t)
    source = "yfinance-eu" if any(ticker.endswith(s) for s in (".PA", ".MC", ".AS", ".DE", ".MI", ".L")) \
        else "yfinance-jp" if ticker.endswith(".T") \
        else "yfinance-hk" if ticker.endswith(".HK") \
        else "yfinance"
    fetch_ok = full.pop("_fetch_ok")
    return {
        "currency": currency,
        **full,
        "quality_source": source,
        "fetched_at": fetched_at,
        "_fetch_ok": fetch_ok,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Resume checkpoint
# ─────────────────────────────────────────────────────────────────────────────

def _checkpoint_path(region: str) -> Path:
    return CHECKPOINT_DIR / f"{region}_fundamentals_progress.json"


def load_checkpoint(region: str) -> dict[str, dict]:
    p = _checkpoint_path(region)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_checkpoint(region: str, partial: dict[str, dict]) -> None:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    p = _checkpoint_path(region)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(partial, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, p)


def clear_checkpoint(region: str) -> None:
    p = _checkpoint_path(region)
    if p.exists():
        p.unlink()


# ─────────────────────────────────────────────────────────────────────────────
# Main build
# ─────────────────────────────────────────────────────────────────────────────

def build_cache(region: str, workers: int = 4, dry_run: bool = False,
                top_n: int | None = None, resume: bool = True) -> dict:
    t0 = time.time()
    print(f"=== Fundamentals cache build · region={region} · "
          f"{datetime.now().isoformat(timespec='seconds')} ===\n")

    universe = build_universe(region)
    if top_n:
        universe = universe[:top_n]
    print(f"  Universe: {len(universe)} tickers ({region})")

    qgm_index = load_qgm_index()
    qgm_full = load_qgm_full_records()
    qgm_in_universe = sum(1 for t in universe if t in qgm_index)
    print(f"  QGM passthrough hits: {qgm_in_universe} (regional + cross-coverage)")
    print(f"  yfinance fetch needed: {len(universe) - qgm_in_universe}")

    # Resume support
    checkpoint = load_checkpoint(region) if resume else {}
    if checkpoint:
        print(f"  Resume: loaded {len(checkpoint)} tickers from checkpoint")

    completed = dict(checkpoint)
    failed: list[str] = []
    todo = [t for t in universe if t not in completed]
    print(f"  TODO this run: {len(todo)} tickers (workers={workers})")

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fetch_ticker, t, qgm_index, qgm_full): t for t in todo}
        last_flush = time.time()
        for i, fut in enumerate(as_completed(futs), 1):
            t = futs[fut]
            try:
                row = fut.result(timeout=30)
                fetch_ok = row.pop("_fetch_ok", True)
                if fetch_ok:
                    completed[t] = row
                else:
                    failed.append(t)
                    completed[t] = row  # still save row with nulls — viewer sees coverage
            except Exception as exc:
                print(f"    ERR {t}: {exc}", file=sys.stderr)
                failed.append(t)

            if i % 25 == 0 or i == len(futs):
                elapsed = time.time() - t0
                print(f"    [{i:>4}/{len(futs)}] {elapsed:>4.0f}s · "
                      f"success={i - len(failed)} failed={len(failed)}")

            # Flush checkpoint every 50 tickers
            if time.time() - last_flush > 30:
                save_checkpoint(region, completed)
                last_flush = time.time()

    # Final partial-success check
    total = len(completed)
    failed_count = sum(1 for r in completed.values()
                       if not any(v is not None for v in (r.get("quality") or {}).values()))
    # Also count tickers in 'failed' list that weren't recorded (rare)
    pure_fail = [t for t in failed if t not in completed]
    failed_count += len(pure_fail)
    failure_ratio = failed_count / max(1, len(universe))

    if failure_ratio >= ABORT_FAILURE_RATIO:
        print(f"\n  ABORT: {failed_count}/{len(universe)} ({failure_ratio:.0%}) failed — "
              f"refusing to overwrite cache. Run again later.", file=sys.stderr)
        print(f"  Checkpoint preserved at {_checkpoint_path(region)} — next run will resume.",
              file=sys.stderr)
        sys.exit(1)

    if failure_ratio >= PARTIAL_ERROR_RATIO:
        status = "partial-error"
        print(f"\n  ERROR: high failure rate {failed_count}/{len(universe)}", file=sys.stderr)
    elif failure_ratio >= PARTIAL_WARN_RATIO:
        status = "partial-warn"
        print(f"\n  WARN: partial failures {failed_count}/{len(universe)}")
    else:
        status = "ok"

    # Source breakdown
    src_counts: dict[str, int] = {}
    for row in completed.values():
        s = row.get("quality_source", "unknown")
        src_counts[s] = src_counts.get(s, 0) + 1
    src_counts["failed"] = failed_count

    runtime = time.time() - t0

    out = {
        "schema_version": SCHEMA_VERSION,
        "region": region,
        "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "run_timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "next_refresh_due": (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d"),
        "stale_after_days": STALE_AFTER_DAYS,
        "universe_size": len(universe),
        "source_breakdown": src_counts,
        "health": {
            "status": status,
            "success_count": len(universe) - failed_count,
            "failed_count": failed_count,
            "failure_ratio": round(failure_ratio, 4),
            "runtime_seconds": int(runtime),
        },
        "failed_tickers": sorted(set(failed)),
        "tickers": completed,
    }

    print(f"\n  Source breakdown: {src_counts}")
    print(f"  Health: {status} (failure ratio {failure_ratio:.1%})")
    print(f"  Runtime: {runtime:.0f}s")

    if dry_run:
        print(f"\n  [dry-run] would write {OUTPUT_DIR}/fundamentals-{region}.json "
              f"(~{len(json.dumps(out)) / 1024:.0f} KB)")
        return out

    # Atomic write
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"fundamentals-{region}.json"
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, out_path)
    print(f"\n  ✓ Wrote {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")

    # Clear checkpoint on full success
    clear_checkpoint(region)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--region", required=True, choices=("us", "tw"),
                    help="Which region cache to build")
    ap.add_argument("--workers", type=int, default=4,
                    help="ThreadPool workers (default 4 — rate-limit friendly)")
    ap.add_argument("--top", type=int, default=None,
                    help="Smoke test: only build first N tickers")
    ap.add_argument("--dry-run", action="store_true",
                    help="Don't write output file")
    ap.add_argument("--no-resume", action="store_true",
                    help="Ignore checkpoint (force full rebuild)")
    args = ap.parse_args()

    build_cache(args.region, workers=args.workers, dry_run=args.dry_run,
                top_n=args.top, resume=not args.no_resume)


if __name__ == "__main__":
    main()
