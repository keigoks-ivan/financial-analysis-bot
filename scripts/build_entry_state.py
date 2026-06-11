#!/usr/bin/env python3
"""Entry State Machine — 進場狀態機 (dd-screener sub-page).

Source-of-truth spec: /Users/ivanchang/.claude/plans/zazzy-questing-castle.md
Per repo: /Users/ivanchang/Downloads/entry_state_machine_spec.md

Pipeline:
  1. Load docs/dd-screener/latest.json (timing + ma block, including v1.6
     250w cycle fields)  AND  docs/dd-screener/quality-entry.json (Q/G
     sub-scores + archetype).
  2. Build universe = 品質中間層 ∩ 成長型 with hysteresis:
       - Q >= 0.55 + G >= 0.50 to enter
       - Q >= 0.50 + G >= 0.45 to remain (avoids boundary in/out churn)
  3. First-layer MA gate: 🟢 healthy / 🟡 mixed / 🟢 W250-N/A / 🔴 weak /
     🔴 W250-N/A / ⚪ n/a (excluded).
  4. Second-layer state (only for tickers passing first-layer):
       - BREAKOUT  (動能突破派接手) — true ATH breakout: dist_250w in [-3,0],
         wsh ≤ 2, drift_4w > +5%, ma50 ≥ 0, RS ≥ 80
       - PULLBACK_WATCH (回調買入派候選) — real ATH retracement: dist_250w in
         [-15,-5], wsh in [2,26], drift_4w_min_in_8w < -3% (true decline
         history), ma50 in [-3,+3]
       - RIDING — passes first-layer but neither BREAKOUT nor PULLBACK
       - WEAK   — first-layer rejected
  5. is_new flag: compare today's state vs most recent ticker entry in prior
     5 snapshots (handles GHA cron miss).
  6. WATCH counter (build-count units, GRACE_BUILDS=7) persists across
     builds in entry-state-state/watch_counters.json.
  7. Write entry-state.html + entry-state.json + daily snapshot.

Usage:
  python3 scripts/build_entry_state.py
  python3 scripts/build_entry_state.py --dry-run      # no writes
  python3 scripts/build_entry_state.py --no-snapshot  # skip snapshot/state writes
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"
QE_JSON = ROOT / "docs" / "dd-screener" / "quality-entry.json"
OUTPUT_DIR = ROOT / "docs" / "dd-screener"
HTML_OUT = OUTPUT_DIR / "entry-state.html"
JSON_OUT = OUTPUT_DIR / "entry-state.json"
SNAPSHOT_DIR = OUTPUT_DIR / "entry-state-snapshots"
STATE_DIR = OUTPUT_DIR / "entry-state-state"
WATCH_COUNTERS_PATH = STATE_DIR / "watch_counters.json"

TAIPEI_TZ = timezone(timedelta(hours=8))
# v1.1 (2026-06-10): within-state sort key changed from RS desc → FundScore desc
# (0.571*Q + 0.429*G); each stock record gains a `fund_score` field (float|null).
SCHEMA_VERSION = "1.1"

# ── universe filter (hysteresis) ──────────────────────────────────────────────
# v1.2 retune (2026-05-20): Q≥0.55/G≥0.50 produced 83-ticker universe (too
# many). Q distribution starts at min=0.58 → Q≥0.55 had no filtering effect;
# raised Q to 0.75 + tightened G to 0.60 → ~49 ticker universe.
QUALITY_ENTER = 0.75
QUALITY_EXIT = 0.70
GROWTH_ENTER = 0.60
GROWTH_EXIT = 0.55
UNIVERSE_MIN_WARN = 10   # banner warning if universe drops below

# ── second-layer state thresholds (圓整、寬鬆,backtest-validated) ───────────
# Distance to true 5y ATH
BREAKOUT_DIST_250W = (-3.0, 0.0)
PULLBACK_DIST_250W = (-15.0, -5.0)
# Cycle position (weeks since 250w high)
BREAKOUT_WSH_MAX = 2
PULLBACK_WSH = (2, 26)
# 4-week direction
BREAKOUT_DRIFT_MIN = 5.0           # drift_4w_pct > +5% (現在強勢往上)
PULLBACK_DRIFT_HIST_MAX = -3.0     # drift_4w_min_in_8w < -3% (過去 8w 曾深跌)
# 50DMA + RS
BREAKOUT_MA50 = 0.0
BREAKOUT_RS = 80.0
PULLBACK_MA50 = (-3.0, 3.0)

# ── FundScore (within-state sort key, v1.1) ───────────────────────────────────
# Re-weight the quality (0.40) + growth (0.30) pillars to a [0,1] fundamentals
# score, dropping the entry pillar (entry timing is already what the state machine
# itself captures). FundScore = (0.40*Q + 0.30*G) / 0.70 = 0.571*Q + 0.429*G.
# v1.1 replaces the old "RS desc" within-state ordering with FundScore desc; RS
# stays as a display-only column.
FUNDSCORE_Q_WEIGHT = 0.40 / 0.70   # ≈ 0.5714
FUNDSCORE_G_WEIGHT = 0.30 / 0.70   # ≈ 0.4286

# ── WATCH counter (build-count units) ─────────────────────────────────────────
GRACE_BUILDS = 7                  # ~1.4 weeks (5 builds/week Tue-Sat)
WATCH_N_DAYS_THRESHOLD = 3        # display "止跌候選" hint when builds_no_new_low >= 3

# ── is_new lookback ───────────────────────────────────────────────────────────
SNAPSHOT_LOOKBACK = 5              # most recent 5 snapshots checked for prior state

# ── DD freshness ──────────────────────────────────────────────────────────────
DD_STALE_DAYS = 90

# ── state constants (mutually exclusive top-level) ────────────────────────────
STATE_BREAKOUT = "BREAKOUT"
STATE_PULLBACK = "PULLBACK"
STATE_RIDING = "RIDING"
STATE_WEAK = "WEAK"
SUB_WATCH = "WATCH"
SUB_CONFIRMED = "CONFIRMED"


# ── helpers ───────────────────────────────────────────────────────────────────
def _safe_float(x) -> Optional[float]:
    if x is None:
        return None
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    if f != f:  # NaN
        return None
    return f


def _safe_int(x) -> Optional[int]:
    if x is None:
        return None
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def _today_str() -> str:
    return datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d")


def _fmt_pct(v: Optional[float], decimals: int = 1) -> str:
    if v is None:
        return "—"
    return f"{v:+.{decimals}f}%"


def _fmt_pct_unsigned(v: Optional[float], decimals: int = 1) -> str:
    if v is None:
        return "—"
    return f"{v:.{decimals}f}%"


def _fmt_score(v: Optional[float]) -> str:
    if v is None:
        return "—"
    return f"{v:.2f}"


def _fmt_fund_score(v: Optional[float]) -> str:
    if v is None:
        return "—"
    return f"{v:.3f}"


def _fmt_int(v: Optional[int]) -> str:
    if v is None:
        return "—"
    return str(v)


def _ticker_link(row: dict) -> str:
    dd = row.get("dd_path")
    label = row["ticker"]
    if dd:
        return f'<a href="{dd}">{label}</a>'
    return label


def _fmt_taipei_stamp(iso_str: Optional[str]) -> str:
    if not iso_str or "T" not in iso_str:
        return iso_str or "—"
    date, time = iso_str.split("T", 1)
    return f"{date} {time[:5]}"


# ── loaders ───────────────────────────────────────────────────────────────────
def _load_json_or_fail(path: Path, label: str) -> dict:
    """Hard-fail on missing/corrupt input file — prefer staleness over wrong data."""
    if not path.exists():
        print(f"  ERR: {label} not found at {path} — upstream build did not run",
              file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ERR: {label} at {path} is corrupt JSON: {e}", file=sys.stderr)
        sys.exit(2)


def _load_prior_snapshots(n: int = SNAPSHOT_LOOKBACK) -> list[dict]:
    """Return up to n most recent snapshots (newest first), [] if none yet.

    Each snapshot is the entry-state.json doc structure; caller extracts the
    {ticker -> state} map via _ticker_state_map.
    """
    if not SNAPSHOT_DIR.exists():
        return []
    files = sorted(
        SNAPSHOT_DIR.glob("*.json"),
        key=lambda p: p.name,
        reverse=True,
    )
    out: list[dict] = []
    for p in files[:n]:
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            # Skip corrupt snapshot but keep loading older ones — robust to a single bad file
            continue
        if len(out) >= n:
            break
    return out


def _ticker_state_map(snapshot: dict) -> dict[str, str]:
    """Extract {ticker -> combined_state_str} from a snapshot doc."""
    out: dict[str, str] = {}
    for s in snapshot.get("stocks", []) or []:
        t = s.get("ticker")
        if not t:
            continue
        state = s.get("state")
        sub = s.get("sub_state")
        # Combined-state key for is_new comparison: 'BREAKOUT' / 'PULLBACK:WATCH' /
        # 'PULLBACK:CONFIRMED' / 'RIDING' / 'WEAK'. Mirrors classify_state output.
        if sub:
            out[t] = f"{state}:{sub}"
        else:
            out[t] = state
    return out


def _load_state_store() -> dict:
    """Load WATCH counter persistent state. Empty dict if first deploy.
    Hard-fail on corrupt — defensive: silently resetting all counters would
    mask a real bug."""
    if not WATCH_COUNTERS_PATH.exists():
        return {}
    try:
        return json.loads(WATCH_COUNTERS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ERR: {WATCH_COUNTERS_PATH} is corrupt JSON: {e} — "
              "manual inspection required (do NOT silently reset counters)",
              file=sys.stderr)
        sys.exit(2)


# ── universe filter (with hysteresis) ─────────────────────────────────────────
def build_universe(
    qe_rows: list[dict],
    yesterday_universe_tickers: set[str],
) -> dict[str, dict]:
    """Apply품質中間層 ∩ 成長型 hysteresis filter to quality-entry.json rows.

    Hysteresis:
      - Ticker not in yesterday's universe → must pass ENTER thresholds to enter
      - Ticker in yesterday's universe     → must drop below EXIT thresholds to be kicked out
      - archetype hard cutoff (no hysteresis on it — its underlying growth ≥ 0.55
        cutoff is indirectly smoothed by our growth EXIT=0.45 leniency)
    """
    universe: dict[str, dict] = {}
    for r in qe_rows:
        t = r.get("ticker")
        if not t:
            continue
        q = _safe_float(r.get("quality"))
        g = _safe_float(r.get("growth"))
        if q is None or g is None:
            continue
        if r.get("archetype") != "成長型":
            continue

        was_in = t in yesterday_universe_tickers
        if was_in:
            if q >= QUALITY_EXIT and g >= GROWTH_EXIT:
                universe[t] = r
        else:
            if q >= QUALITY_ENTER and g >= GROWTH_ENTER:
                universe[t] = r
    return universe


def _yesterday_universe_tickers(prior_snapshots: list[dict]) -> set[str]:
    """Extract universe (= all tickers that appeared) from the most recent
    snapshot. Empty set if first deploy."""
    if not prior_snapshots:
        return set()
    latest = prior_snapshots[0]
    return {s["ticker"] for s in (latest.get("stocks") or []) if s.get("ticker")}


# ── first-layer MA gate ───────────────────────────────────────────────────────
MA_GREEN_HEALTHY = "GREEN_HEALTHY"
MA_YELLOW_MIXED = "YELLOW_MIXED"
MA_GREEN_W250_NA = "GREEN_W52_W250_NA"
MA_RED_WEAK = "RED_WEAK"
MA_RED_W250_NA = "RED_W52_W250_NA"
MA_NA = "NA_INSUFFICIENT"

OPEN_STATES: dict[str, Optional[set[str]]] = {
    MA_GREEN_HEALTHY:  {STATE_BREAKOUT, STATE_RIDING, STATE_PULLBACK},
    MA_YELLOW_MIXED:   {STATE_RIDING, STATE_PULLBACK},      # BREAKOUT closed
    MA_GREEN_W250_NA:  {STATE_RIDING, STATE_PULLBACK},      # BREAKOUT closed (long-term unconfirmed)
    MA_RED_WEAK:       set(),                                # first-layer veto
    MA_RED_W250_NA:    set(),                                # first-layer veto
    MA_NA:             None,                                  # excluded entirely
}


def ma_gate(ma: Optional[dict]) -> str:
    """First-layer MA gate (weekly W52/W250 health). See plan §First-layer."""
    if ma is None:
        return MA_NA
    a52 = ma.get("above_w52")
    if a52 is None:
        return MA_NA
    a250 = ma.get("above_w250")
    slope = _safe_float(ma.get("slope_w250_pct"))
    if a250 is None:
        return MA_GREEN_W250_NA if a52 else MA_RED_W250_NA
    if not a52 or not a250:
        return MA_RED_WEAK
    if slope is not None and slope > 0:
        return MA_GREEN_HEALTHY
    return MA_YELLOW_MIXED


def ma_label_display(label: str) -> str:
    """Human-readable MA badge for table cell."""
    return {
        MA_GREEN_HEALTHY:  "🟢 healthy",
        MA_YELLOW_MIXED:   "🟡 mixed",
        MA_GREEN_W250_NA:  "🟢 W250 N/A",
        MA_RED_WEAK:       "🔴 weak",
        MA_RED_W250_NA:    "🔴 W250 N/A",
        MA_NA:             "⚪ n/a",
    }.get(label, "—")


# ── second-layer state classifier ─────────────────────────────────────────────
def classify_state(
    ma_label: str,
    ma: dict,
    timing: Optional[dict],
) -> tuple[str, Optional[str]]:
    """Returns (state, sub_state).

    state    ∈ {BREAKOUT, PULLBACK, RIDING, WEAK}
    sub_state ∈ {WATCH, CONFIRMED, None}

    See plan §Second-layer state. Order: BREAKOUT → PULLBACK → RIDING.
    """
    open_set = OPEN_STATES.get(ma_label)
    if open_set is None:
        # NA_INSUFFICIENT should be excluded from universe before reaching here;
        # treat as WEAK to be safe (table row will surface the gap).
        return (STATE_WEAK, None)
    if len(open_set) == 0:
        return (STATE_WEAK, None)

    timing = timing or {}

    d250 = _safe_float(ma.get("dist_250w_high_pct"))
    wsh = _safe_int(ma.get("weeks_since_250w_high"))
    drift_now = _safe_float(ma.get("drift_4w_pct"))
    drift_min_8w = _safe_float(ma.get("drift_4w_min_in_8w"))
    m50 = _safe_float(timing.get("ma50_pct"))
    rs = _safe_float(timing.get("rs_score"))

    # Any of the core fields missing → conservative RIDING (don't claim BK/PB
    # without enough signal). is_full_5y=false rows have d250/wsh present (via
    # "上市以來高點" fallback) but drift_min_8w may be None for very new listings.
    if d250 is None or wsh is None or drift_now is None or m50 is None:
        return (STATE_RIDING, None)

    # 1) BREAKOUT — true 250w ATH breakout, requires GREEN_HEALTHY + direction +
    #    RS confirmation. (rs may be None for some tickers; we honor the rs ≥ 80
    #    gate strictly when rs is present — if missing, fail the gate to stay
    #    conservative.)
    if (STATE_BREAKOUT in open_set
            and BREAKOUT_DIST_250W[0] <= d250 <= BREAKOUT_DIST_250W[1]
            and wsh <= BREAKOUT_WSH_MAX
            and drift_now > BREAKOUT_DRIFT_MIN
            and m50 >= BREAKOUT_MA50
            and rs is not None and rs >= BREAKOUT_RS):
        return (STATE_BREAKOUT, None)

    # 2) PULLBACK_WATCH — real ATH retracement (cycle gate + 8w historical
    #    decline + 50DMA support zone). drift_min_8w required (signals "真跌
    #    進場過,不是 stale ATH 慢漂"); if missing, can't claim PULLBACK.
    if (STATE_PULLBACK in open_set
            and PULLBACK_DIST_250W[0] <= d250 <= PULLBACK_DIST_250W[1]
            and PULLBACK_WSH[0] <= wsh <= PULLBACK_WSH[1]
            and drift_min_8w is not None and drift_min_8w < PULLBACK_DRIFT_HIST_MAX
            and PULLBACK_MA50[0] <= m50 <= PULLBACK_MA50[1]):
        return (STATE_PULLBACK, SUB_WATCH)

    return (STATE_RIDING, None)


def applicable_school(state: str) -> str:
    """進場派別 column."""
    if state == STATE_BREAKOUT:
        return "動能突破派"
    if state == STATE_PULLBACK:
        return "回調買入派"
    return "—"


def compute_fund_score(
    quality: Optional[float],
    growth: Optional[float],
) -> Optional[float]:
    """Blend the quality + growth sub-scores into a single [0,1] fundamentals
    score (FundScore = 0.571*Q + 0.429*G). Returns None when either sub-score is
    missing — the row then sinks to the bottom of its state bucket (see
    _state_sort_key) and renders as '—' in the table."""
    if quality is None or growth is None:
        return None
    return FUNDSCORE_Q_WEIGHT * quality + FUNDSCORE_G_WEIGHT * growth


# ── is_new flag ───────────────────────────────────────────────────────────────
def compute_is_new(
    today_state_key: str,
    ticker: str,
    prior_snapshot_maps: list[dict[str, str]],
) -> bool:
    """Return True iff today's state differs from the most recent prior state
    observed for this ticker. Looks back through up to N snapshots so a missed
    GHA cron doesn't manufacture false 'new' flags."""
    for sm in prior_snapshot_maps:
        prior = sm.get(ticker)
        if prior is not None:
            return prior != today_state_key
    # No prior observation in lookback window → truly new
    return True


# ── WATCH counter (build-count units) ─────────────────────────────────────────
def update_watch_counter(
    ticker: str,
    is_watch_today: bool,
    today_close: Optional[float],
    today_date: str,
    state_store: dict,
) -> Optional[dict]:
    """Mutates state_store in place. Returns the (possibly updated) counter
    dict for this ticker, or None if not tracked today.

    All counts are in **build-count units** (per-cron execution) for unit
    consistency with GRACE_BUILDS.
    """
    s = state_store.get(ticker)

    if is_watch_today:
        if today_close is None:
            # WATCH today but no price — preserve any existing counter, don't update
            return s
        if s is None:
            state_store[ticker] = {
                "watch_start_build": today_date,
                "watch_period_low_close": today_close,
                "builds_no_new_low": 1,
                "last_seen_in_watch_build": today_date,
                "builds_outside_watch": 0,
            }
            return state_store[ticker]

        # Already in WATCH (continuing or returning from a brief detour)
        s["builds_outside_watch"] = 0
        if today_close < s.get("watch_period_low_close", today_close):
            # 真正惡化:跌破 WATCH 期間前低 → 計數歸零、更新低點
            s["watch_period_low_close"] = today_close
            s["builds_no_new_low"] = 1
        else:
            s["builds_no_new_low"] = (s.get("builds_no_new_low") or 0) + 1
        s["last_seen_in_watch_build"] = today_date
        return s

    # Today is NOT WATCH
    if s is None:
        return None

    if today_close is not None and today_close < s.get("watch_period_low_close", today_close):
        # 短暫跳出但同時跌破前低 → 視為惡化、清除狀態
        del state_store[ticker]
        return None

    s["builds_outside_watch"] = (s.get("builds_outside_watch") or 0) + 1
    if s["builds_outside_watch"] > GRACE_BUILDS:
        del state_store[ticker]
        return None
    return s


# ── pipeline ──────────────────────────────────────────────────────────────────
def _state_sort_key(row: dict) -> tuple:
    """Sort priority — state bucket first, then FundScore desc (v1.1).

    Bucket order (state-priority; CONFIRMED before WATCH, BREAKOUT new before
    continuing):
      0 PULLBACK_CONFIRMED
      1 PULLBACK_WATCH
      2 BREAKOUT + is_new=true
      3 BREAKOUT + is_new=false (continuing)
      4 RIDING
      5 WEAK
    Within bucket: FundScore desc (None sinks to bottom via -inf), then ticker
    asc (stable). v1.1: RS no longer participates in sorting — it is a
    display-only column.
    """
    state = row["state"]
    sub = row.get("sub_state")
    is_new = row.get("is_new", False)
    if state == STATE_PULLBACK:
        bucket = 0 if sub == SUB_CONFIRMED else 1
    elif state == STATE_BREAKOUT:
        bucket = 2 if is_new else 3
    elif state == STATE_RIDING:
        bucket = 4
    else:
        bucket = 5
    fs = row.get("fund_score")
    fs_key = fs if fs is not None else float("-inf")
    return (bucket, -fs_key, row["ticker"])


def build_pipeline() -> tuple[dict, dict]:
    """Returns (doc, updated_state_store)."""
    print(f"=== Entry-State build · {_now_taipei_iso()} ===\n")

    latest = _load_json_or_fail(LATEST_JSON, "latest.json")
    qe = _load_json_or_fail(QE_JSON, "quality-entry.json")
    as_of = latest.get("as_of") or _today_str()
    today_date = _today_str()
    print(f"  latest.json as_of={as_of}  stocks={len(latest.get('stocks', []) or [])}")
    print(f"  quality-entry.json tier_a+tier_b={len(qe.get('tier_a', []) or []) + len(qe.get('tier_b', []) or [])}")

    # Snapshot lookback (for is_new + yesterday-universe)
    prior_snapshots = _load_prior_snapshots(SNAPSHOT_LOOKBACK)
    prior_snapshot_maps = [_ticker_state_map(snap) for snap in prior_snapshots]
    yesterday_universe = _yesterday_universe_tickers(prior_snapshots)
    print(f"  prior snapshots loaded: {len(prior_snapshots)} (lookback={SNAPSHOT_LOOKBACK})")
    print(f"  yesterday universe: {len(yesterday_universe)} tickers")

    # Universe = quality-middle-layer growth-type (hysteresis-filtered).
    # v1.1: read from `all_scored` (added in build_quality_entry v1.4) which
    # contains ALL post-veto rows — not just the top-25 display slice
    # (tier_a + tier_b), which silently capped our universe at ~23 tickers
    # and dropped quality compounders like GOOGL / META / NFLX into overflow.
    qe_rows = qe.get("all_scored")
    if qe_rows is None:
        # Fallback for older quality-entry.json (pre-v1.4): use display slice.
        # WARN so we don't silently under-cover the universe.
        qe_rows = (qe.get("tier_a") or []) + (qe.get("tier_b") or [])
        print("  WARN: quality-entry.json missing 'all_scored' — falling back to "
              f"tier_a+tier_b ({len(qe_rows)} rows). Universe will under-cover; "
              "rerun build_quality_entry.py to refresh.", file=sys.stderr)
    universe = build_universe(qe_rows, yesterday_universe)
    print(f"  Universe (Q≥{QUALITY_ENTER} / G≥{GROWTH_ENTER} / archetype=成長型, "
          f"with hysteresis): {len(universe)} tickers")

    if len(universe) == 0:
        print(f"  ERR: universe collapsed to 0 — quality-entry.json upstream "
              "likely broken. Refusing to write empty entry-state page.",
              file=sys.stderr)
        sys.exit(2)

    # Index latest.json by ticker for fast join
    latest_by_ticker = {s["ticker"]: s for s in (latest.get("stocks") or []) if s.get("ticker")}

    # Load WATCH counter state store
    state_store = _load_state_store()
    print(f"  state_store: {len(state_store)} tickers carrying WATCH counters")

    # Classify each ticker
    rows: list[dict] = []
    summary = {
        "BREAKOUT_new": 0,
        "BREAKOUT_continuing": 0,
        "PULLBACK_WATCH": 0,
        "PULLBACK_CONFIRMED": 0,
        "RIDING": 0,
        "WEAK": 0,
    }

    for ticker, qe_row in universe.items():
        live = latest_by_ticker.get(ticker)
        if live is None:
            # Universe says yes, but latest.json missing this ticker — skip with
            # warning. (Shouldn't happen if both upstreams ran same cron, but defensive.)
            print(f"  WARN: {ticker} in universe but missing from latest.json, skipping",
                  file=sys.stderr)
            continue

        ma = live.get("ma") or {}
        timing = live.get("timing") or {}
        ma_lbl = ma_gate(ma)

        # Exclude tickers with no MA at all (NA_INSUFFICIENT). They wouldn't
        # produce useful state, and the universe filter doesn't catch them
        # because quality-entry.json doesn't carry MA data.
        if ma_lbl == MA_NA:
            print(f"  INFO: {ticker} excluded — no MA data (NA_INSUFFICIENT)")
            continue

        state, sub_state = classify_state(ma_lbl, ma, timing)

        # is_new comparison key (mirrors snapshot extraction)
        state_key = f"{state}:{sub_state}" if sub_state else state
        is_new = compute_is_new(state_key, ticker, prior_snapshot_maps)

        # WATCH counter update (only PULLBACK_WATCH triggers tracking)
        is_watch_today = (state == STATE_PULLBACK and sub_state == SUB_WATCH)
        today_close = _safe_float(ma.get("price"))
        counter = update_watch_counter(
            ticker, is_watch_today, today_close, today_date, state_store
        )

        # Promote to PULLBACK_CONFIRMED if WATCH and counter has reached threshold.
        # (Auto-confirm based on builds_no_new_low ≥ N. Manual confirmation could
        # override this later via entry-state-state/manual_confirmations.json;
        # not implemented in v1.0 — keep human-loop in spec line 81.)
        # NOTE: per plan, formal CONFIRMED upgrade is human-only in v1.0; we
        # display the counter and let user decide. So sub_state stays WATCH here.

        # Build the per-ticker row
        days_no_new_low = (counter or {}).get("builds_no_new_low")

        # FundScore (within-state sort key + display column). Q/G joined from
        # quality-entry.json; None when either is missing → row sinks to bottom.
        q_score = _safe_float(qe_row.get("quality"))
        g_score = _safe_float(qe_row.get("growth"))
        fund_score = compute_fund_score(q_score, g_score)

        row = {
            "ticker": ticker,
            "name": qe_row.get("name") or ticker,
            "sector": qe_row.get("sector") or "",
            "ma_label": ma_lbl,
            "state": state,
            "sub_state": sub_state,
            "is_new": is_new,
            "applicable_school": applicable_school(state),
            "quality": q_score,
            "growth": g_score,
            "fund_score": fund_score,
            # 5y cycle (primary distance)
            "dist_250w_high_pct": _safe_float(ma.get("dist_250w_high_pct")),
            "weeks_since_250w_high": _safe_int(ma.get("weeks_since_250w_high")),
            "is_full_5y": ma.get("is_full_5y"),
            "high_250w_price": _safe_float(ma.get("high_250w_price")),
            # Direction
            "drift_4w_pct": _safe_float(ma.get("drift_4w_pct")),
            "drift_4w_min_in_8w": _safe_float(ma.get("drift_4w_min_in_8w")),
            # Daily timing
            "ma50_pct": _safe_float(timing.get("ma50_pct")),
            "rs_score": _safe_float(timing.get("rs_score")),
            "dist_52w_high_pct": _safe_float(timing.get("dist_52w_high_pct")),
            # Slope / W250 cache flag
            "slope_w250_pct": _safe_float(ma.get("slope_w250_pct")),
            "ma_from_cache": bool(live.get("ma_from_cache")),
            # WATCH counter snapshot for this ticker (None if not tracked)
            "builds_no_new_low": days_no_new_low,
            "watch_period_low_close": (counter or {}).get("watch_period_low_close"),
            "watch_start_build": (counter or {}).get("watch_start_build"),
            # DD freshness
            "dd_age_days": _safe_int(live.get("dd_age_days")),
            "dd_date": live.get("dd_date"),
            "dd_path": live.get("dd_path"),
            "dca_path": live.get("dca_path"),
            # Misc quality context
            "moat_grade": qe_row.get("moat_grade"),
            "signal": qe_row.get("signal"),
            "archetype": qe_row.get("archetype"),
        }
        rows.append(row)

        # Update summary
        if state == STATE_BREAKOUT:
            summary["BREAKOUT_new" if is_new else "BREAKOUT_continuing"] += 1
        elif state == STATE_PULLBACK:
            summary["PULLBACK_CONFIRMED" if sub_state == SUB_CONFIRMED else "PULLBACK_WATCH"] += 1
        elif state == STATE_RIDING:
            summary["RIDING"] += 1
        else:
            summary["WEAK"] += 1

    # Sort by state-priority then RS
    rows.sort(key=_state_sort_key)

    print(f"  Classified: {len(rows)} rows")
    print(f"  Summary: {summary}")
    if state_store:
        print(f"  WATCH counters carried forward: {len(state_store)} tickers")

    doc = {
        "schema_version": SCHEMA_VERSION,
        "run_timestamp": _now_taipei_iso(),
        "as_of": as_of,
        "universe_size": len(rows),
        "universe_min_warn": UNIVERSE_MIN_WARN,
        "summary": summary,
        "thresholds": {
            "quality_enter": QUALITY_ENTER,
            "quality_exit": QUALITY_EXIT,
            "growth_enter": GROWTH_ENTER,
            "growth_exit": GROWTH_EXIT,
            "breakout": {
                "dist_250w_high_pct": list(BREAKOUT_DIST_250W),
                "weeks_since_250w_high_max": BREAKOUT_WSH_MAX,
                "drift_4w_pct_min": BREAKOUT_DRIFT_MIN,
                "ma50_pct_min": BREAKOUT_MA50,
                "rs_min": BREAKOUT_RS,
            },
            "pullback": {
                "dist_250w_high_pct": list(PULLBACK_DIST_250W),
                "weeks_since_250w_high": list(PULLBACK_WSH),
                "drift_4w_min_in_8w_max": PULLBACK_DRIFT_HIST_MAX,
                "ma50_pct": list(PULLBACK_MA50),
            },
            "stale_ath_weeks": PULLBACK_WSH[1],
            "watch_n_builds_threshold": WATCH_N_DAYS_THRESHOLD,
            "watch_grace_builds": GRACE_BUILDS,
            "dd_stale_days": DD_STALE_DAYS,
            "snapshot_lookback": SNAPSHOT_LOOKBACK,
        },
        "stocks": rows,
    }
    return doc, state_store


# ── HTML rendering ────────────────────────────────────────────────────────────
def _state_chip_html(row: dict) -> str:
    state = row["state"]
    sub = row.get("sub_state")
    is_new = row.get("is_new", False)
    if state == STATE_BREAKOUT:
        chip = '<span class="chip chip-breakout">🟢 BREAKOUT</span>'
    elif state == STATE_PULLBACK and sub == SUB_CONFIRMED:
        chip = '<span class="chip chip-pullback-confirmed">🔵 PULLBACK</span>'
    elif state == STATE_PULLBACK:
        chip = '<span class="chip chip-pullback-watch">🔷 PULLBACK · WATCH</span>'
    elif state == STATE_RIDING:
        chip = '<span class="chip chip-riding">⚪ RIDING</span>'
    else:
        chip = '<span class="chip chip-weak">🔴 WEAK</span>'

    # is_new badge — only meaningful for actionable states (BK / PB_WATCH / PB_CONFIRMED)
    actionable = (state == STATE_BREAKOUT) or (state == STATE_PULLBACK)
    if actionable and is_new:
        chip += ' <span class="new-badge" title="今日剛轉入此狀態">★ NEW</span>'
    return chip


def _ma_chip_html(label: str) -> str:
    """Color-coded MA badge cell."""
    text = ma_label_display(label)
    cls = {
        MA_GREEN_HEALTHY:  "ma-green",
        MA_GREEN_W250_NA:  "ma-green",
        MA_YELLOW_MIXED:   "ma-yellow",
        MA_RED_WEAK:       "ma-red",
        MA_RED_W250_NA:    "ma-red",
        MA_NA:             "ma-na",
    }.get(label, "ma-na")
    return f'<span class="ma-chip {cls}">{text}</span>'


def _dd_freshness_html(days: Optional[int]) -> str:
    """DD freshness cell: 'DD N 天', red if >90."""
    if days is None:
        return '<span class="dd-fresh dd-unknown">DD 天數未知</span>'
    cls = "dd-stale" if days > DD_STALE_DAYS else "dd-fresh"
    return f'<span class="{cls}">DD {days} 天</span>'


def _watch_counter_html(row: dict) -> str:
    """WATCH counter cell — only meaningful for PULLBACK_WATCH/CONFIRMED rows."""
    n = row.get("builds_no_new_low")
    if row["state"] != STATE_PULLBACK or n is None:
        return "—"
    threshold = WATCH_N_DAYS_THRESHOLD
    ready = n >= threshold
    cls = "watch-ready" if ready else "watch-counting"
    hint = "✓ 可進場考慮" if ready else f"等止跌（{threshold} build 門檻）"
    return f'<span class="{cls}" title="{hint}">{n} build / 未破新低</span>'


def _is_full_5y_marker(row: dict) -> str:
    if row.get("is_full_5y") is False:
        return '<span class="not-full-5y" title="上市以來高點 — &lt; 5 年歷史">*</span>'
    return ""


def _links_html(row: dict) -> str:
    parts = []
    dd = row.get("dd_path")
    dca = row.get("dca_path")
    if dd:
        parts.append(f'<a href="{dd}">DD</a>')
    if dca:
        parts.append(f'<a href="{dca}">DCA</a>')
    return " · ".join(parts) if parts else "—"


def _filter_state_key(row: dict) -> str:
    """Composite filter key matching the chip toggles (v1.2 filter chips).

    Returns one of: BREAKOUT, PULLBACK_WATCH, PULLBACK_CONFIRMED, RIDING, WEAK.
    """
    state = row["state"]
    sub = row.get("sub_state")
    if state == STATE_PULLBACK and sub == SUB_CONFIRMED:
        return "PULLBACK_CONFIRMED"
    if state == STATE_PULLBACK:
        return "PULLBACK_WATCH"
    return state  # BREAKOUT / RIDING / WEAK


def _row_html(row: dict) -> str:
    ticker_cell = _ticker_link(row)
    sector_sub = ""  # v1.x: industry subtitle removed per user request — ticker only

    high_250w = row.get("high_250w_price")
    if high_250w is not None:
        high_tip = f'真 5 年高點 = ${high_250w:.2f}'
    else:
        high_tip = "5y high N/A"

    is_new_actionable = bool(
        row.get("is_new") and row["state"] in (STATE_BREAKOUT, STATE_PULLBACK)
    )
    state_class = f"state-{row['state'].lower()}{'_new' if is_new_actionable else ''}"
    filter_key = _filter_state_key(row)

    return f"""<tr class="{state_class}" data-state="{filter_key}" data-is-new="{'1' if is_new_actionable else '0'}">
  <td class="left">{ticker_cell}{sector_sub}</td>
  <td>{_ma_chip_html(row['ma_label'])}</td>
  <td>{_state_chip_html(row)}</td>
  <td class="left school-cell">{row['applicable_school']}</td>
  <td>{_fmt_score(row.get('quality'))}</td>
  <td>{_fmt_score(row.get('growth'))}</td>
  <td class="fund-score">{_fmt_fund_score(row.get('fund_score'))}</td>
  <td title="{high_tip}">{_fmt_pct(row.get('dist_250w_high_pct'))}{_is_full_5y_marker(row)}</td>
  <td>{_fmt_int(row.get('weeks_since_250w_high'))}</td>
  <td>{_fmt_pct(row.get('drift_4w_pct'))}</td>
  <td>{_fmt_pct(row.get('ma50_pct'))}</td>
  <td>{_fmt_pct_unsigned(row.get('rs_score'))}</td>
  <td>{_watch_counter_html(row)}</td>
  <td>{_dd_freshness_html(row.get('dd_age_days'))}</td>
  <td class="left">{_links_html(row)}</td>
</tr>"""


def _universe_warning_banner_html(doc: dict) -> str:
    n = doc["universe_size"]
    if n < UNIVERSE_MIN_WARN:
        return f"""<div class="caveat-panel warn-panel">
  <strong>⚠️ Universe 過小</strong>
  目前 universe 僅 <b>{n}</b> 檔(正常應為 20+)— quality-entry 上游可能有問題,
  或市場 regime 切換中導致多檔被踢出。請檢查 <code>quality-entry.json</code>
  與 <code>build_dd_screener.py</code> 是否正常。
</div>"""
    return ""


def render_html(doc: dict, out_path: Path) -> None:
    as_of = doc["as_of"]
    run_ts_display = _fmt_taipei_stamp(doc.get("run_timestamp"))
    summary = doc["summary"]
    universe_size = doc["universe_size"]
    new_signals = summary["BREAKOUT_new"] + summary["PULLBACK_WATCH"]
    rows_html = "\n".join(_row_html(r) for r in doc["stocks"]) if doc["stocks"] else \
                '<tr><td colspan="15" class="empty-row">沒有 universe 標的可顯示</td></tr>'
    warning_banner = _universe_warning_banner_html(doc)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entry State Machine — 進場狀態機 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f0f5fb;color:#1e3a5f;line-height:1.5}}
.imq-nav-root{{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.imq-nav-inner{{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}}
.imq-logo{{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}}
.imq-logo:hover{{color:#fff !important;text-decoration:none !important}}
.imq-logo span{{color:#3b82f6}}
.imq-menu{{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}}
.imq-menu > a,.imq-dd-btn{{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}}
.imq-menu > a:hover,.imq-dd-btn:hover{{color:#fff !important;background:rgba(255,255,255,.08)}}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}}
.imq-dd{{position:relative;display:inline-block}}
.imq-dd-menu{{display:none;position:absolute;top:100%;left:0;background:#1e293b;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{{display:block}}
.imq-dd-menu a{{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}}
.imq-dd-menu a:hover{{color:#fff !important;background:rgba(59,130,246,.18)}}
.imq-caret{{font-size:.6rem;opacity:.7;margin-top:1px}}
@media(max-width:768px){{.imq-nav-root{{padding:.55rem 12px}}.imq-menu{{width:100%;justify-content:flex-start;gap:.1rem}}.imq-menu > a,.imq-dd-btn{{font-size:.74rem;padding:.32rem .5rem}}.imq-dd-menu{{position:static;display:none;min-width:auto;box-shadow:none;background:rgba(255,255,255,.04);border:none;padding:.1rem 0 .3rem 1rem;margin:.1rem 0}}.imq-dd.open .imq-dd-menu{{display:block}}}}
.hero{{background:#fff;border-bottom:1px solid #dce8f5;padding:24px 32px 18px}}
.hero-inner{{max-width:min(1400px,96vw);margin:0 auto}}
.hero-h1{{font-size:22px;font-weight:600;color:#0f2a45;margin-bottom:6px}}
.hero-sub{{font-size:12px;color:#5a7a9a;line-height:1.6;max-width:920px}}
.hero-stats{{display:flex;gap:14px;margin-top:12px;flex-wrap:wrap}}
.hero-stat{{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:7px 11px;font-size:11px;color:#5a7a9a}}
.hero-stat strong{{color:#1e3a5f;font-size:13px;display:block;margin-bottom:1px}}
.hero-stat.new-stat strong{{color:#92400e}}
.section{{max-width:min(1400px,96vw);margin:0 auto;padding:24px 32px}}
.caveat-panel{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:14px 18px;margin-bottom:20px;font-size:12px;color:#854d0e;line-height:1.65}}
.caveat-panel strong{{color:#78350f;display:block;margin-bottom:6px}}
.caveat-panel ol,.caveat-panel ul{{margin-left:20px}}
.warn-panel{{background:#fef2f2;border-color:#fecaca;color:#991b1b}}
.warn-panel strong{{color:#7f1d1d}}
.tier-card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:16px 18px;margin-bottom:22px}}
.tier-card h2{{font-size:16px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;color:#0f2a45}}
.tier-card h2 .badge{{display:inline-block;padding:2px 9px;border-radius:5px;font-size:11px;font-weight:700;background:#dbeafe;color:#1e40af}}
.tier-card .desc{{font-size:12px;color:#5a7a9a;margin-bottom:12px;line-height:1.6}}
.tier-card table{{width:100%;border-collapse:collapse;font-size:11.5px}}
.tier-card th{{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:7px 8px;text-align:right;border-bottom:2px solid #dce8f5;font-size:10px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap}}
.tier-card th.left{{text-align:left}}
.tier-card td{{padding:7px 8px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums;vertical-align:middle}}
.tier-card td.left{{text-align:left;color:#0f2a45;font-weight:500}}
.tier-card td.left .sub{{font-size:10px;color:#94a3b8;font-weight:400;margin-top:1px}}
.tier-card td a{{color:#2563eb;text-decoration:none;font-weight:600}}
.tier-card td a:hover{{text-decoration:underline}}
.school-cell{{font-size:11px;color:#475569;font-weight:500}}
.fund-score{{font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-weight:700;color:#0f2a45}}
.empty-row{{padding:14px;text-align:center;color:#94a3b8;font-size:12px;font-style:italic}}
/* state row highlights for is_new actionable signals */
tr.state-breakout_new{{background:linear-gradient(90deg,#dcfce7 0%,transparent 60%)}}
tr.state-pullback_new{{background:linear-gradient(90deg,#dbeafe 0%,transparent 60%)}}
/* color chips */
.chip{{display:inline-block;padding:2px 8px;border-radius:5px;font-size:10.5px;font-weight:700;white-space:nowrap;letter-spacing:.02em}}
.chip-breakout{{background:#dcfce7;color:#166534}}
.chip-pullback-confirmed{{background:#dbeafe;color:#1e40af}}
.chip-pullback-watch{{background:#e0f2fe;color:#0c4a6e}}
.chip-riding{{background:#f1f5f9;color:#475569}}
.chip-weak{{background:#fee2e2;color:#991b1b}}
.new-badge{{display:inline-block;padding:1px 6px;border-radius:4px;font-size:9.5px;font-weight:700;background:#fef3c7;color:#92400e;margin-left:3px;letter-spacing:.04em}}
.ma-chip{{display:inline-block;padding:1px 6px;border-radius:4px;font-size:10px;font-weight:600;white-space:nowrap}}
.ma-green{{color:#16a34a}}
.ma-yellow{{color:#ca8a04}}
.ma-red{{color:#dc2626}}
.ma-na{{color:#94a3b8}}
.dd-fresh{{color:#475569;font-size:11px}}
.dd-stale{{color:#dc2626;font-weight:700;font-size:11px}}
.dd-unknown{{color:#94a3b8;font-style:italic;font-size:11px}}
.watch-counting{{color:#0c4a6e;font-size:11px}}
.watch-ready{{color:#166534;font-weight:700;font-size:11px}}
.not-full-5y{{color:#ca8a04;font-weight:700;cursor:help}}
.footer{{padding:30px 32px;font-size:11px;color:#5a7a9a;line-height:1.7;max-width:min(1400px,96vw);margin:0 auto;border-top:1px solid #dce8f5}}
.footer h4{{color:#1e3a5f;font-size:12px;margin-top:14px;margin-bottom:6px;font-weight:700}}
.footer code{{background:#f0f5fb;padding:1px 5px;border-radius:3px;font-size:10px;color:#1e3a5f}}
.methodology{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:14px 18px;margin-bottom:20px}}
.methodology h3{{font-size:13px;font-weight:700;color:#0f2a45;margin-bottom:8px}}
.methodology code{{background:#f0f5fb;padding:1px 6px;border-radius:3px;font-size:11px;color:#1e3a5f}}
.methodology .row{{font-size:12px;color:#334e68;line-height:1.9;margin-bottom:4px}}
/* v1.2 filter chips */
.filter-bar{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:10px 14px;margin-bottom:14px;display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:11.5px}}
.filter-label{{color:#5a7a9a;font-weight:600;margin-right:4px}}
.filter-divider{{color:#cbd5e1;margin:0 4px}}
.filter-count{{color:#475569;font-weight:600;margin-left:auto;white-space:nowrap;font-variant-numeric:tabular-nums}}
.filter-count strong{{color:#0f2a45}}
.filter-chip{{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border:1px solid #dce8f5;border-radius:999px;background:#fff;color:#94a3b8;font-size:11px;font-weight:600;cursor:pointer;user-select:none;transition:all .12s;font-family:inherit;line-height:1.4;letter-spacing:.01em}}
.filter-chip:hover:not(.disabled){{border-color:#94a3b8;color:#475569}}
.filter-chip.active{{background:#0f172a;color:#fff;border-color:#0f172a}}
.filter-chip.active.chip-breakout-tag{{background:#16a34a;border-color:#16a34a}}
.filter-chip.active.chip-pb-watch-tag{{background:#0c4a6e;border-color:#0c4a6e}}
.filter-chip.active.chip-pb-conf-tag{{background:#1e40af;border-color:#1e40af}}
.filter-chip.active.chip-riding-tag{{background:#64748b;border-color:#64748b}}
.filter-chip.active.chip-weak-tag{{background:#dc2626;border-color:#dc2626}}
.filter-chip.active.chip-new-tag{{background:#92400e;border-color:#92400e}}
.filter-chip.disabled{{opacity:.4;cursor:not-allowed}}
.filter-chip .count{{opacity:.7;font-weight:500;margin-left:1px}}
</style>
</head>
<body>
<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/">首頁</a>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/research/">個股 DD</a>
          <a href="/pm/">PM 複盤</a>
          <a href="/id/">產業深度 ID</a>
          <a href="/ds/">產業敘述 DS</a>
          <a href="/comparisons/">多股對比</a>
        </div>
      </div>
      <div class="imq-dd active">
        <button type="button" class="imq-dd-btn">工具<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/dd-screener/">DD Screener</a>

          <a href="/dd-screener/quality-entry.html">Quality-Entry</a>
          <a href="/dd-screener/bottom-out.html">Bottom-Out</a>
          <a href="/dd-screener/breakout.html">Breakout</a>
          <a href="/dd-screener/earnings-acceleration.html">Earnings Acceleration</a>
          <a href="/dd-screener/entry-state.html" class="active">⚙️ Entry State Machine</a>
          <a href="/backtest/">量化回測</a>
        </div>
      </div>
    </nav>
  </div>
</header>
<script>(function(){{document.querySelectorAll('.imq-dd-btn').forEach(function(btn){{btn.addEventListener('click',function(e){{e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){{if(d!==dd)d.classList.remove('open')}});dd.classList.toggle('open')}})}});document.addEventListener('click',function(e){{if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){{d.classList.remove('open')}});}});}})();</script>

<div class="hero">
  <div class="hero-inner">
    <div class="hero-h1">Entry State Machine — 進場狀態機</div>
    <div class="hero-sub">
      雙邏輯接力 — <b>動能突破派</b>抓第一棒(BREAKOUT)、<b>回調買入派</b>抓後續棒(PULLBACK)。
      前置一道 <b>W52/W250 週線 MA 大方向閘</b>(跌破即標 WEAK,不進第二層);
      第二層用 <b>5 年週線 cycle context</b>(真 ATH 距離 + ATH 週齡)+ <b>4 週方向過濾</b>判定當下狀態。
      與 <a href="/dd-screener/quality-entry.html" style="color:#2563eb">Quality-Entry</a>(單一逢回邏輯複合分)定位互補,<b>不重複</b>。
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{run_ts_display}</strong>最後更新(台北)</div>
      <div class="hero-stat"><strong>{as_of}</strong>資料 as-of</div>
      <div class="hero-stat"><strong>{universe_size}</strong>universe</div>
      <div class="hero-stat new-stat"><strong>{new_signals}</strong>今日新訊號(BK new + PB watch)</div>
      <div class="hero-stat"><strong>{summary['BREAKOUT_new']} / {summary['BREAKOUT_continuing']}</strong>BREAKOUT new / 持續</div>
      <div class="hero-stat"><strong>{summary['PULLBACK_WATCH']} / {summary['PULLBACK_CONFIRMED']}</strong>PULLBACK watch / confirmed</div>
      <div class="hero-stat"><strong>{summary['RIDING']}</strong>RIDING(無新訊號)</div>
      <div class="hero-stat"><strong>{summary['WEAK']}</strong>WEAK(第一層否決)</div>
    </div>
  </div>
</div>

<div class="section">

  {warning_banner}

  <div class="caveat-panel">
    <strong>讀法 8 點(動手前必讀)</strong>
    <ol>
      <li><b>與 Quality-Entry 的定位區別</b>:Quality-Entry 是「單一逢回邏輯」的複合評分;本頁是「突破派抓第一棒、回調派抓後續棒」的雙邏輯接力。兩者並存,服務不同進場哲學。</li>
      <li><b>Universe 來源(v1.2 retune)</b>:`build_quality_entry.py` 全量 scored(post-veto)中,<b>新進門檻</b> Quality ≥ <code>{QUALITY_ENTER}</code> ∩ Growth ≥ <code>{GROWTH_ENTER}</code> ∩ archetype=成長型;<b>昨日已在 universe 者</b>只要 Q ≥ <code>{QUALITY_EXIT}</code> / G ≥ <code>{GROWTH_EXIT}</code>(hysteresis <b>保留</b>門檻)就維持,避免邊界 ticker 進出抖動。<b>v1.2 變更</b>:原 Q≥0.55/G≥0.50 → 83 太多;Q 實測 min=0.58 不發揮濾用,只 G 才是 dial。新門檻自然 universe ~49,過渡期含 hysteresis ~72。<b>archetype 分類純量化</b>(`growth_pillar ≥ 0.55` = 成長型),<b>不看 market cap</b>;V/MA/MSFT 等「mature 但仍成長」compounder 因 growth_durability 高,會被分到「成長型」(若想額外過濾大型權值股,需另起 mega-cap saturation filter,非本版)。</li>
      <li><b>兩層結構</b>:第一層 W52/W250 週線 MA 閘(🟢/🟡/🔴/⚪)決定能否進入第二層;第二層才判 BREAKOUT/PULLBACK/RIDING 三狀態。</li>
      <li><b>WEAK ≠ 第二層狀態</b>:WEAK 是第一層否決的標籤(跌破 W52 或 W250),不是第二層的進場狀態。它與三個進場狀態並列顯示是為了完整性。</li>
      <li><b>突破派抓第一棒、回調派抓後續棒;<code>★ NEW</code> 才是新訊號</b>:`is_new=true` 表示今天剛從別狀態轉入此狀態。BREAKOUT 持續中(`is_new=false`)實質接近 RIDING,不是新訊號。</li>
      <li><b>狀態判定用 5 年週線 cycle context + 4 週方向過濾</b>:不是單日 snapshot — `dist_250w_high_pct`(真 ATH 距離)+ `weeks_since_250w_high`(ATH 週齡 0-26 才算近期)+ `drift_4w_min_in_8w`(過去 8 週曾真跌過)是 backtest 證實的設計。</li>
      <li><b>止跌確認需人工;DD 新鮮度紅標 ≠ 閘</b>:PULLBACK_WATCH 升級 PULLBACK_CONFIRMED 由人工看圖判讀(本頁 v1.0 不自動升級,只顯示 WATCH 計數)。DD &gt; {DD_STALE_DAYS} 天紅標代表 quality 判定可能過期 — Ivan 自行決定是否重跑 DD,本頁不擋訊號。</li>
      <li><b>【v1.2 新】Filter chips 預設只顯示 BREAKOUT / PULLBACK_WATCH / PULLBACK_CONFIRMED</b>(actionable 訊號)。點 ⚪ RIDING / 🔴 WEAK chip 可展開所有 universe;點「★ 只看新訊號」會再窄到只剩 `is_new=true` 列(BREAKOUT/PULLBACK 才會有 ★)。所有 filter 純 client-side,reload 重置。</li>
    </ol>
  </div>

  <div class="methodology">
    <h3>方法論(門檻全為圓整、寬鬆數值,backtest 驗證)</h3>
    <div class="row"><b>第一層 MA 閘</b>:🟢 healthy = above_w52 ∩ above_w250 ∩ slope_w250 &gt; 0 · 🟡 mixed = 雙均線上但 slope 平/負 · 🔴 weak = 跌破任一均線(第一層否決)· 🟢 W250 N/A = &lt; 5y 上市但站上 W52(降級,關 BREAKOUT)</div>
    <div class="row"><b>BREAKOUT</b>(僅 🟢 healthy):<code>dist_250w_high_pct ∈ [-3%, 0%]</code> ∩ <code>weeks_since_250w_high ≤ {BREAKOUT_WSH_MAX}</code> ∩ <code>drift_4w_pct &gt; +{BREAKOUT_DRIFT_MIN:.0f}%</code> ∩ <code>ma50_pct ≥ {BREAKOUT_MA50:.0f}</code> ∩ <code>rs_score ≥ {BREAKOUT_RS:.0f}</code></div>
    <div class="row"><b>PULLBACK_WATCH</b>(🟢/🟡):<code>dist_250w_high_pct ∈ [-15%, -5%]</code> ∩ <code>weeks_since_250w_high ∈ [2, 26]</code> ∩ <code>drift_4w_min_in_8w &lt; {PULLBACK_DRIFT_HIST_MAX:.0f}%</code>(過去 8w 曾真跌過)∩ <code>ma50_pct ∈ [-3%, +3%]</code></div>
    <div class="row"><b>排序鍵(v1.1)</b>:主鍵 = 狀態優先序(PULLBACK_CONFIRMED → PULLBACK_WATCH → BREAKOUT new → BREAKOUT 持續 → RIDING → WEAK);次鍵 = <code>FundScore = (0.40×Q + 0.30×G) / 0.70 = 0.571×Q + 0.429×G</code> 由高到低(缺 Q/G 視為 -∞ 沉底)。<b>RS 自 v1.1 起不再參與排序</b>,僅作顯示欄。</div>
    <div class="row"><b>WATCH → CONFIRMED 升級</b>:WATCH 中累積 <code>builds_no_new_low ≥ {WATCH_N_DAYS_THRESHOLD}</code> 顯示「✓ 可進場考慮」hint,但本頁 v1.0 <b>不自動升級</b>;由 Ivan 看圖判讀後手動進場。容忍式計數:離開 WATCH 區後 ≤ {GRACE_BUILDS} build 內回來 → 計數延續;超過 → 視為這一波結束、清除狀態。</div>
    <div class="row" style="color:#5a7a9a;margin-top:6px"><b>已知設計邊界</b>:MA 燈號只看 W250 斜率,不看 W52 斜率(避免 W52 抖動干擾大方向閘)— 趨勢早期警示由 🔴(跌破 W52)觸發。Backtest 結果(原 v1.1 5y × 23 ticker sample,Q≥0.55):PULLBACK 命中 ~6%(每檔每 ~17 週,合 ~3 次/年)/ BREAKOUT ~18%(production 加 RS≥80 gate 後實際降至 ~10%)。<b>v1.2 retune 後 universe 擴至 ~49 但同屬高品質區段,命中率應接近</b>;未在新 universe 上重 backtest,訊號量明顯異常時可再調 Q/G 門檻。</div>
  </div>

  <div class="filter-bar" id="entry-state-filters">
    <span class="filter-label">顯示</span>
    <button type="button" class="filter-chip chip-breakout-tag active" data-filter="BREAKOUT">🟢 BREAKOUT <span class="count">({summary['BREAKOUT_new'] + summary['BREAKOUT_continuing']})</span></button>
    <button type="button" class="filter-chip chip-pb-watch-tag active" data-filter="PULLBACK_WATCH">🔷 PB Watch <span class="count">({summary['PULLBACK_WATCH']})</span></button>
    <button type="button" class="filter-chip chip-pb-conf-tag active" data-filter="PULLBACK_CONFIRMED">🔵 PB Conf <span class="count">({summary['PULLBACK_CONFIRMED']})</span></button>
    <button type="button" class="filter-chip chip-riding-tag" data-filter="RIDING">⚪ RIDING <span class="count">({summary['RIDING']})</span></button>
    <button type="button" class="filter-chip chip-weak-tag" data-filter="WEAK">🔴 WEAK <span class="count">({summary['WEAK']})</span></button>
    <span class="filter-divider">|</span>
    <button type="button" class="filter-chip chip-new-tag" data-filter-newonly="1">★ 只看新訊號 <span class="count">({new_signals})</span></button>
    <span class="filter-count">顯示中 <strong id="filter-visible">0</strong>/<span id="filter-total">0</span></span>
  </div>

  <div class="tier-card">
    <h2>狀態總表 <span class="badge">universe {universe_size}</span></h2>
    <div class="desc">排序(v1.1):<b>狀態優先</b>(PB Conf → PB Watch → BREAKOUT new → BREAKOUT 持續 → RIDING → WEAK),同狀態內按 <b>FundScore 由高到低</b>(FundScore = 0.571×Q + 0.429×G;缺值沉底)。<b>RS 改為顯示欄,不參與排序</b>。Ticker 後綴「*」代表上市 &lt; 5 年(以上市以來高點取代真 5y high)。「距 ATH」 hover 顯示真 5 年高點價位。<br><b>預設只顯示 BREAKOUT / PB Watch / PB Conf</b>(actionable);點上方 chip 切換 RIDING / WEAK / 只看 ★ 新訊號。</div>
    <table>
    <thead>
    <tr>
      <th class="left">Ticker</th>
      <th>MA 燈號</th>
      <th>當前狀態</th>
      <th class="left">進場派別</th>
      <th>Q</th>
      <th>G</th>
      <th title="FundScore = 0.571×Q + 0.429×G(品質+成長重加權至 0-1)— 同狀態內排序主鍵">FundScore</th>
      <th>距 ATH (250w)</th>
      <th>ATH 週齡</th>
      <th>4w drift</th>
      <th>vs 50DMA</th>
      <th title="顯示用,不參與排序(v1.1 排序鍵已改為 state → FundScore)">RS</th>
      <th>WATCH 計數</th>
      <th>DD 新鮮度</th>
      <th class="left">Links</th>
    </tr>
    </thead>
    <tbody>
{rows_html}
    </tbody>
    </table>
  </div>

</div>

<div class="footer">
  <h4>資料來源</h4>
  <ul style="margin-left:18px">
    <li><code>docs/dd-screener/latest.json</code> — timing(<code>ma50_pct</code> / <code>rs_score</code>)+ MA(<code>above_w52/w250</code> / <code>slope_w250_pct</code> / <code>drift_4w_pct</code>)+ v1.6 5y cycle context(<code>dist_250w_high_pct</code> / <code>weeks_since_250w_high</code> / <code>drift_4w_min_in_8w</code> / <code>is_full_5y</code>)<small style="color:#94a3b8"> · v1.6 是 `latest.json.ma` block 的 schema 版號(不同於本頁面 feature 版本 v1.2)</small></li>
    <li><code>docs/dd-screener/quality-entry.json</code> — Quality / Growth sub-scores + archetype(成長型/成熟型)</li>
    <li>WATCH counter 狀態:<code>docs/dd-screener/entry-state-state/watch_counters.json</code>(build-count units)</li>
  </ul>
  <h4>機器可讀</h4>
  <p>JSON sidecar: <a href="/dd-screener/entry-state.json"><code>/dd-screener/entry-state.json</code></a> · 每日快照: <code>/dd-screener/entry-state-snapshots/YYYY-MM-DD.json</code> · 計數狀態: <code>/dd-screener/entry-state-state/watch_counters.json</code></p>
  <p style="margin-top:16px;color:#94a3b8">Generated by <code>scripts/build_entry_state.py</code> · schema v{SCHEMA_VERSION}</p>
</div>
<script>
(function(){{
  // v1.2 filter chips — client-side row visibility toggle.
  // State (predefined defaults, no localStorage — reload resets).
  var filters = {{
    BREAKOUT: true, PULLBACK_WATCH: true, PULLBACK_CONFIRMED: true,
    RIDING: false, WEAK: false, newOnly: false,
  }};
  var rows = document.querySelectorAll('tbody tr[data-state]');
  var totalEl = document.getElementById('filter-total');
  var visEl = document.getElementById('filter-visible');
  totalEl.textContent = rows.length;

  function applyFilters(){{
    var visible = 0;
    rows.forEach(function(tr){{
      var stateOk = filters[tr.dataset.state] === true;
      var newOk = !filters.newOnly || tr.dataset.isNew === '1';
      var show = stateOk && newOk;
      tr.style.display = show ? '' : 'none';
      if (show) visible++;
    }});
    visEl.textContent = visible;
  }}

  function updateChipDisabledState(){{
    document.querySelectorAll('.filter-chip[data-filter]').forEach(function(btn){{
      var key = btn.dataset.filter;
      var n = 0;
      rows.forEach(function(tr){{ if (tr.dataset.state === key) n++; }});
      if (n === 0) btn.classList.add('disabled');
    }});
  }}

  document.querySelectorAll('.filter-chip[data-filter]').forEach(function(btn){{
    btn.addEventListener('click', function(){{
      if (btn.classList.contains('disabled')) return;
      var key = btn.dataset.filter;
      filters[key] = !filters[key];
      btn.classList.toggle('active', filters[key]);
      applyFilters();
    }});
  }});
  var newBtn = document.querySelector('.filter-chip[data-filter-newonly]');
  if (newBtn) newBtn.addEventListener('click', function(){{
    filters.newOnly = !filters.newOnly;
    newBtn.classList.toggle('active', filters.newOnly);
    applyFilters();
  }});

  updateChipDisabledState();
  applyFilters();
}})();
</script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✓ Wrote {out_path} ({out_path.stat().st_size:,} bytes)")


# ── main ──────────────────────────────────────────────────────────────────────
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Don't write any files")
    p.add_argument("--no-snapshot", action="store_true",
                   help="Skip daily snapshot + WATCH counter writes (still writes html/json)")
    args = p.parse_args()

    doc, state_store = build_pipeline()

    if args.dry_run:
        print("\n  (dry-run) skipping writes")
        # Show a tiny preview so user can sanity-check
        print(f"  preview first row keys: {list(doc['stocks'][0].keys()) if doc['stocks'] else 'EMPTY'}")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    JSON_OUT.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  ✓ Wrote {JSON_OUT} ({JSON_OUT.stat().st_size:,} bytes)")

    render_html(doc, HTML_OUT)

    if not args.no_snapshot:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        snap_path = SNAPSHOT_DIR / f"{_today_str()}.json"
        snap_path.write_text(
            json.dumps(doc, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  ✓ Wrote snapshot {snap_path}")

        STATE_DIR.mkdir(parents=True, exist_ok=True)
        WATCH_COUNTERS_PATH.write_text(
            json.dumps(state_store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  ✓ Wrote state_store {WATCH_COUNTERS_PATH} ({len(state_store)} tickers tracked)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
