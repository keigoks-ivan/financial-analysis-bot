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


def write_ticker_cache(
    ticker: str,
    weekly_bars: list[dict],
    *,
    full_refresh: bool,
    last_attempt_failed_at: Optional[str] = None,
) -> None:
    """Atomic write of the per-ticker cache JSON.

    - `full_refresh=True` updates `last_full_refresh` to today
    - `full_refresh=False` preserves prior `last_full_refresh` (incremental)
    - bars trimmed to BARS_CAP newest entries
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()

    if len(weekly_bars) > BARS_CAP:
        weekly_bars = weekly_bars[-BARS_CAP:]

    # Preserve last_full_refresh across incremental writes
    if full_refresh:
        refresh_date = today_str
    else:
        existing = read_ticker_cache(ticker)
        refresh_date = (existing or {}).get("last_full_refresh") or today_str

    payload: dict[str, Any] = {
        "ticker": ticker,
        "last_full_refresh": refresh_date,
        "last_attempt_failed_at": last_attempt_failed_at,
        "rebackfill_slot": slot_for(ticker),
        "source": SOURCE_TAG,
        "weekly_bars": weekly_bars,
    }
    # Compact JSON: tabular layout for bars (one bar per line) would help diff
    # readability, but standard indent=2 is enough at this size — and avoids
    # custom serialization fragility.
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
