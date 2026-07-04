"""Weekly close cache — persistent 5y weekly bars for DD universe tickers.

Backs scripts/dd_screener_ma.compute_ma_snapshot() so MA / cycle-context
computations don't need full 5y yfinance pulls every day.

# Operating modes (per ticker per daily build)

  - **Full rebackfill** (1/5 of universe per build, by hash slot):
      Pulls 5y weekly via yfinance, overwrites the cache file. Each ticker
      is fully refreshed on its slot day (~once every 5 days), which
      auto-corrects yfinance back-adjustment drift after corporate actions.

  - **Incremental** (remaining 4/5):
      Pulls ~2 months of weekly bars via yfinance (just to grab the in-
      progress current week + any recent bars), splices into existing cache.
      The current week's bar is `close = latest daily close` per yfinance
      semantics — naturally daily-responsive.

  - **Emergency rebackfill** (split detection):
      If incremental's latest close differs from cached previous close by
      > 50%, suspects a stock split / spinoff / huge gap. Triggers a full
      yfinance pull immediately, bypassing the 5-day rotation.

  - **Cache fallback** (yfinance failure):
      Any of the above pulls fail → caller can `compute_from_bars()` using
      the existing cache. Outage resilience is unlimited (as long as the
      git-tracked cache file survives).

# Schema (per file `data/weekly_cache/{TICKER}.json`)

  {
    "ticker": "NVDA",
    "last_full_refresh": "2026-05-20",          // last day full 5y pull succeeded
    "last_attempt_failed_at": null,              // YYYY-MM-DD if yfinance failed on slot day
    "rebackfill_slot": 2,                        // 0..4, derived from hash(ticker)
    "source": "yfinance:5y:1wk auto_adjust=True",
    "weekly_bars": [
      {"week_end": "2021-05-24", "close": 22.45},
      ...,
      {"week_end": "2026-05-16", "close": 134.20}
    ]
  }

Bars are sorted ascending by week_end. Capped at ~260 bars (5y + buffer) —
older bars trimmed on each write to keep file size stable.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Optional

# ── paths & constants ────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = ROOT / "data" / "weekly_cache"

ROLLING_CYCLE_DAYS = 5           # universe split across 5 slots → ~1/5 per day
SPLIT_DETECT_THRESHOLD = 0.395   # |new/prev - 1| >= ~40% → suspect split / spinoff.
                                  # 0.395 (not 0.40) to dodge float-precision edges
                                  # like 140/100 - 1 = 0.3999...9. Catches 2-for-1
                                  # (50%), 3-for-1 (67%), reverse splits, large gaps.
                                  # 40-49% earnings moves trigger a harmless full pull.
BARS_CAP = 270                   # keep at most ~5y + 1 quarter buffer per ticker

SOURCE_TAG = "yfinance:5y:1wk auto_adjust=True"

# ── epsilon-stable write tolerances ───────────────────────────────────────────
# yfinance re-serializes adjusted closes with sub-cent drift at the 4th decimal
# (e.g. 132.4611 → 132.461, 129.3356 → 129.3355) on every pull. Rewriting the
# file with that noise produced 10k+ blob versions and nightly rebase collisions.
# A bar whose close moves by less than *both* an absolute and a relative floor is
# treated as unchanged: we keep the OLD serialized value so the file bytes (and
# therefore the git diff) stay stable. Real daily/weekly moves are dollars, not
# sub-cent, so genuine price tracking is unaffected.
CLOSE_ABS_TOL = 0.005            # |Δ| < half a cent → noise
CLOSE_REL_TOL = 1e-4             # OR |Δ|/price < 1e-4 → noise (covers high-$ names)
# Metadata fields that, if changed, justify a rewrite even when bars are stable.
# `last_full_refresh` is deliberately excluded: it is diagnostic-only (no consumer
# reads it) and advancing it on a no-material-change day would reintroduce churn.
_META_KEYS_FOR_SKIP = ("ticker", "rebackfill_slot", "source", "last_attempt_failed_at")


# ── helpers ──────────────────────────────────────────────────────────────────
def cache_path(ticker: str) -> Path:
    """Per-ticker cache file path. Ticker characters '.' '/' ':' are tolerated
    in filenames on all major OSes; we keep them as-is for readability
    (e.g. '2330.TW.json', '6857.T.json', 'BRK.B.json')."""
    safe = ticker.replace("/", "_").replace(":", "_")
    return CACHE_DIR / f"{safe}.json"


def slot_for(ticker: str) -> int:
    """Stable 0..4 slot derived from SHA1(ticker). Deterministic across
    Python runs (unlike hash(), which is salted)."""
    h = hashlib.sha1(ticker.encode("utf-8")).hexdigest()
    return int(h, 16) % ROLLING_CYCLE_DAYS


def today_slot(today: Optional[date] = None) -> int:
    """Today's slot. Uses ordinal day-count so the slot advances by exactly 1
    per calendar day regardless of timezone — Tue-Sat cron skipping Sun/Mon
    means slots {0,1,2,3,4} each get touched within any 5-7 day window."""
    d = today or date.today()
    return d.toordinal() % ROLLING_CYCLE_DAYS


def is_full_rebackfill_day(ticker: str, today: Optional[date] = None) -> bool:
    return slot_for(ticker) == today_slot(today)


def detect_split(new_close: Optional[float], last_cached_close: Optional[float]) -> bool:
    """True if a single-bar price change exceeds the split threshold.

    50% bar moves on US/TW/JP equities almost never occur outside corporate
    actions; tolerable false-positive rate is low. We accept the rare false
    positive (e.g. an extreme earnings move) because the recovery cost is one
    extra yfinance pull, not data loss.
    """
    if new_close is None or last_cached_close is None or last_cached_close <= 0:
        return False
    return abs(new_close / last_cached_close - 1) >= SPLIT_DETECT_THRESHOLD


# ── read / write ─────────────────────────────────────────────────────────────
def read_ticker_cache(ticker: str) -> Optional[dict]:
    """Return full cache dict (incl. metadata + weekly_bars), or None if
    missing / corrupt. Corrupt files are not silently reset — caller decides."""
    p = cache_path(ticker)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        # Surface to caller via None — they'll either skip or trigger full pull
        return None


def _round_bars(bars: list[dict]) -> list[dict]:
    """Canonical 4-decimal rounding of every close (idempotent; upstream
    df_to_bars already rounds, this is defensive so the write path is the
    single source of truth for on-disk precision)."""
    out: list[dict] = []
    for b in bars:
        nb = dict(b)
        c = nb.get("close")
        if c is not None:
            try:
                nb["close"] = round(float(c), 4)
            except (TypeError, ValueError):
                pass
        out.append(nb)
    return out


def _close_equiv(a: Optional[float], b: Optional[float]) -> bool:
    """True if two closes are equal within noise tolerance (abs OR rel)."""
    if a is None or b is None:
        return a == b
    d = abs(a - b)
    if d < CLOSE_ABS_TOL:
        return True
    denom = max(abs(a), abs(b))
    return denom > 0 and (d / denom) < CLOSE_REL_TOL


def _reconcile_bars(old_bars: list[dict], new_bars: list[dict]) -> list[dict]:
    """Return `new_bars`, but for every bar whose week_end also exists in the
    cache AND whose close is within noise tolerance, revert to the OLD cached
    bar verbatim. This strips re-serialization drift from unchanged bars while
    letting genuinely new bars, removed bars (window roll-off), and real moves
    (> tolerance) flow through. Net effect: a full 5y pull that only jitters the
    4th decimal produces byte-identical output; a true one-bar change produces a
    one-bar diff instead of a whole-file rewrite."""
    old_by = {b.get("week_end"): b for b in (old_bars or [])}
    out: list[dict] = []
    for nb in new_bars:
        ob = old_by.get(nb.get("week_end"))
        if ob is not None and _close_equiv(ob.get("close"), nb.get("close")):
            # Preserve the old bar exactly (close value + any other fields).
            out.append(dict(ob))
        else:
            out.append(nb)
    return out


def _is_noop_write(existing: Optional[dict], payload: dict) -> bool:
    """True if writing `payload` would not change anything material relative to
    the file already on disk — same bars (already reconciled to old values) and
    same skip-relevant metadata. `last_full_refresh` is intentionally ignored so
    a no-material-change refresh day leaves the file (and git) untouched."""
    if existing is None:
        return False
    if (existing.get("weekly_bars") or []) != payload.get("weekly_bars"):
        return False
    return all(existing.get(k) == payload.get(k) for k in _META_KEYS_FOR_SKIP)


def write_ticker_cache(
    ticker: str,
    weekly_bars: list[dict],
    *,
    full_refresh: bool,
    last_attempt_failed_at: Optional[str] = None,
) -> None:
    """Atomic, epsilon-stable write of the per-ticker cache JSON.

    - `full_refresh=True` updates `last_full_refresh` to today (only when the
      write actually lands — a no-op refresh leaves it stale, which is truthful)
    - `full_refresh=False` preserves prior `last_full_refresh` (incremental)
    - bars trimmed to BARS_CAP newest entries, closes canonicalised to 4dp
    - unchanged bars are reconciled to their old serialized value, and if the
      resulting payload is materially identical to the file on disk, NO write
      happens at all (old bytes preserved → zero git diff)
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()

    weekly_bars = _round_bars(weekly_bars)
    if len(weekly_bars) > BARS_CAP:
        weekly_bars = weekly_bars[-BARS_CAP:]

    existing = read_ticker_cache(ticker)

    # Kill re-serialization drift: keep old close bytes for bars that didn't
    # materially move, so only genuine adds/removes/moves ever hit disk.
    if existing is not None:
        weekly_bars = _reconcile_bars(existing.get("weekly_bars") or [], weekly_bars)

    # Preserve last_full_refresh across incremental writes
    if full_refresh:
        refresh_date = today_str
    else:
        refresh_date = (existing or {}).get("last_full_refresh") or today_str

    payload: dict[str, Any] = {
        "ticker": ticker,
        "last_full_refresh": refresh_date,
        "last_attempt_failed_at": last_attempt_failed_at,
        "rebackfill_slot": slot_for(ticker),
        "source": SOURCE_TAG,
        "weekly_bars": weekly_bars,
    }

    # Skip-if-equivalent: nothing material changed → leave the file untouched so
    # the git blob is byte-stable across nightly rebuilds.
    if _is_noop_write(existing, payload):
        return

    # Compact JSON: tabular layout for bars (one bar per line) helps diff
    # readability, and indent=2 with the fixed key order above is already
    # deterministic — no sort_keys needed (and sort_keys would reorder every
    # bar's close/week_end, turning a one-bar change into a whole-file diff).
    p = cache_path(ticker)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


# ── conversion helpers (pandas DataFrame <→ bars list) ───────────────────────
def df_to_bars(df) -> list[dict]:
    """Convert a yfinance weekly-history DataFrame to bars list.

    Drops NaN closes. Each bar is {"week_end": "YYYY-MM-DD", "close": float}.
    Sorted ascending by week_end (yfinance returns ascending; we preserve).
    """
    out: list[dict] = []
    closes = df["Close"].dropna()
    for idx, close in closes.items():
        try:
            week_end = idx.strftime("%Y-%m-%d")
        except AttributeError:
            # Index isn't a Timestamp — skip defensively
            continue
        try:
            c = float(close)
        except (TypeError, ValueError):
            continue
        if c != c:  # NaN
            continue
        out.append({"week_end": week_end, "close": round(c, 4)})
    return out


def merge_incremental(cached_bars: list[dict], small_df) -> list[dict]:
    """Splice fresh bars from `small_df` (e.g. last 2 months) into cached.

    - If a fresh bar's week_end matches a cached bar's week_end, the fresh
      value OVERWRITES (the in-progress current week's close updates daily).
    - Fresh bars newer than all cached bars are appended.
    - Result is sorted ascending by week_end, capped at BARS_CAP.
    """
    by_week: dict[str, dict] = {b["week_end"]: dict(b) for b in cached_bars}
    fresh_bars = df_to_bars(small_df)
    for fb in fresh_bars:
        by_week[fb["week_end"]] = fb
    merged = sorted(by_week.values(), key=lambda b: b["week_end"])
    if len(merged) > BARS_CAP:
        merged = merged[-BARS_CAP:]
    return merged


def bars_to_closes(bars: list[dict]) -> list[float]:
    """Chronological close-only list."""
    return [b["close"] for b in bars]


def latest_close(bars: list[dict]) -> Optional[float]:
    """Most recent close, or None if bars empty."""
    if not bars:
        return None
    return bars[-1].get("close")


# ── status reporting ─────────────────────────────────────────────────────────
def cache_summary() -> dict:
    """Aggregate stats over data/weekly_cache/ — for build-log diagnostics."""
    if not CACHE_DIR.exists():
        return {"exists": False, "tickers": 0, "total_bytes": 0}
    files = list(CACHE_DIR.glob("*.json"))
    total = sum(p.stat().st_size for p in files)
    return {
        "exists": True,
        "tickers": len(files),
        "total_bytes": total,
        "total_kb": round(total / 1024, 1),
    }
