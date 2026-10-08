#!/usr/bin/env python3
"""Fiscal-year rollover detection for cross-snapshot EPS revision comparisons.

Bug this fixes (2026-10-08): Koyfin's FY1/FY2/FY3 columns are RELATIVE
(FY1 = the fiscal year currently in progress or most recently ended but not
yet reported). After a company files its annual report, Koyfin rolls the
columns forward one year: new FY1 = old FY2's fiscal year. _compute_fy_eps_
revision() compared FY1-vs-FY1, FY2-vs-FY2, FY3-vs-FY3 across snapshots, so
any ticker whose rollover fell between the baseline and the current export
showed a fake revision (MU: FY27 176.15 vs old FY26 73.60 = "+43%"; the true
FY27-vs-FY27 revision is 176.15 vs 159.49 = +10%).

Source-aware (2026-10-08): shift = rolled(current) - rolled(baseline) in
{-1, 0, +1}. yfinance-sourced snapshots roll at the fiscal-year END, Koyfin
(xlsx) after the annual report (first report <= FYE+120d); see fy_shift().
-1 means the baseline (yfinance) had rolled but the current Koyfin row has not.

Rule (date-based, never inferred from the numbers alone):

  PREFERRED (when the ticker's list of past reported-earnings dates is known):
    A = earliest reported date strictly after the (rolled-forward) last_fye;
    none -> (0, "no_shift"); shifted iff baseline_date <= A < current_date.

  FALLBACK (list missing/empty) — the 105-day heuristic below; statuses get a
  "_heuristic" suffix:

  Koyfin rolls FY1 only after the ANNUAL report. Let A be that report date.
    last_fye       most recent fiscal-year-end (yfinance info["lastFiscalYearEnd"])
    last_earnings  most recent reported earnings date (any quarter)

    last_earnings unknown or last_fye unknown        -> (0, "unknown")
    last_earnings > 366d before last_fye (bad data)  -> (0, "unknown")
    last_fye < last_earnings <= last_fye + 105d      -> A = last_earnings
    last_earnings <= last_fye                        -> (0, "no_shift")   annual report not out yet
    last_earnings >  last_fye + 105d                 -> A somewhere in (last_fye, last_fye+105d]:
        baseline >= last_fye + 105d or current <= last_fye -> (0, "no_shift")
        baseline <= last_fye and current >= last_fye + 105d -> (1, "shifted")
        otherwise                    -> (0, "ambiguous")
    with A known: shifted iff baseline_date <= A < current_date.
      (Snapshot dates are Taipei dates taken ~09:30 Taipei, i.e. before a
      same-day US report, hence the inclusive baseline side.)

When shifted, callers compare current FY1 vs baseline FY2, current FY2 vs
baseline FY3, and current FY3 has no baseline (None).

A numbers-based sanity check (check_numbers_agree) only logs; it never
overrides the date decision.

Persistent cache data/fiscal_year_end.json — {ticker: {"last_fye":
"YYYY-MM-DD", "checked": "YYYY-MM-DD"}}, same load/save/thread-lock pattern
as eps_fx_normalize.py's reporting-currency cache. Refetched when older than
FYE_CACHE_MAX_AGE_DAYS; fail-open (None -> status "unknown").
"""
from __future__ import annotations

import json
import threading
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FYE_CACHE_PATH = ROOT / "data" / "fiscal_year_end.json"
FYE_CACHE_MAX_AGE_DAYS = 180   # FYEs rarely change; CI never commits data/ caches
ANNUAL_REPORT_WINDOW_DAYS = 105
ANNUAL_REPORT_MAX_LAG_DAYS = 120

_fye_lock = threading.Lock()

# FY key -> the key holding the SAME fiscal year in a pre-rollover baseline.
SHIFTED_BASELINE_KEY = {
    "eps_fy_curr": "eps_fy_next",
    "eps_fy_next": "eps_fy3",
    "eps_fy3": None,
}
# shift == -1 (baseline already rolled, current not): current FY2 vs baseline FY1, etc.
SHIFTED_BACK_BASELINE_KEY = {
    "eps_fy_curr": None,
    "eps_fy_next": "eps_fy_curr",
    "eps_fy3": "eps_fy_next",
}


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------


def _to_date(v) -> date | None:
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    try:
        return datetime.strptime(str(v)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _add_years(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # Feb 29
        return d.replace(year=d.year + n, day=28)


def roll_fye_forward(fye: date, current: date) -> date:
    """Roll a possibly stale last-FYE forward by whole years while the next
    year's FYE is already in the past (handles a stale cache)."""
    while _add_years(fye, 1) <= current:
        fye = _add_years(fye, 1)
    return fye


# ---------------------------------------------------------------------------
# Decision
# ---------------------------------------------------------------------------


def _norm_src(src) -> str:
    return "yfinance" if str(src or "").lower() == "yfinance" else "xlsx"


def fy_shift(last_fye, last_earnings_date, baseline_date, current_date,
             past_earnings_dates=None, baseline_source=None,
             current_source=None) -> tuple[int, str]:
    """(shift, status), shift in {-1, 0, +1} = rolled(current) - rolled(baseline),
    where "rolled" means the snapshot's FY1 column already points at the fiscal
    year AFTER last_fye:

      source "yfinance": rolled iff snapshot_date > last_fye  (yfinance's 0y
                         rolls at the fiscal-year END)
      source "xlsx" (Koyfin, default for None): rolled iff the annual report A
                         is known and A < snapshot_date. A = first reported
                         date after last_fye, only if A <= last_fye + 120d,
                         else there is no annual report yet.

    Koyfin side with no annual report within FYE+120d: not rolled while the
    snapshot is inside the window, ASSUMED rolled once it is past it (spin-offs,
    new listings); statuses then read assumed_rolled / shifted_assumed.

    Status: shifted (+1) | shifted_back (-1) | no_shift | no_annual_report |
    ambiguous | unknown; "_heuristic" suffix when decided without the dates
    list (105-day rule, see _fy_shift_heuristic)."""
    fye = _to_date(last_fye)
    base = _to_date(baseline_date)
    cur = _to_date(current_date)
    if fye is None or base is None or cur is None:
        return 0, "unknown"
    fye = roll_fye_forward(fye, cur)
    bs, cs = _norm_src(baseline_source), _norm_src(current_source)
    both_yf = bs == "yfinance" and cs == "yfinance"

    def rolled_yf(d):
        return d > fye

    past = sorted(d for d in (_to_date(x) for x in (past_earnings_dates or [])) if d)
    if past or both_yf:
        a = next((d for d in past if d > fye), None)
        if a is not None and a > fye + timedelta(days=ANNUAL_REPORT_MAX_LAG_DAYS):
            a = None

        window_end = fye + timedelta(days=ANNUAL_REPORT_MAX_LAG_DAYS)
        assumed = []

        def rolled(d, src):
            if src == "yfinance":
                return rolled_yf(d)
            if a is not None:
                return a < d
            # No annual report within FYE+120d: spin-offs / new listings. Once the
            # snapshot is past the window, assume Koyfin has rolled anyway.
            if d > window_end:
                assumed.append(d)
                return True
            return False

        delta = int(rolled(cur, cs)) - int(rolled(base, bs))
        tag = "_assumed" if assumed and delta else ""
        if delta == 1:
            return 1, "shifted" + tag
        if delta == -1:
            return -1, "shifted_back" + tag
        if assumed:
            return 0, "assumed_rolled"
        if a is None and not both_yf:
            return 0, "no_annual_report"
        return 0, "no_shift"

    # No dates list. Both Koyfin: the single-date 105-day heuristic.
    le = _to_date(last_earnings_date)
    if le is None:
        return 0, "unknown"
    if bs == cs == "xlsx":
        sh, st = _fy_shift_heuristic(fye, le, base, cur)
        return sh, (st if st == "unknown" else st + "_heuristic")
    # Mixed sources: take A = last_earnings_date when it is plausibly the annual report.
    if le > fye + timedelta(days=ANNUAL_REPORT_MAX_LAG_DAYS) or le < fye - timedelta(days=366):
        return 0, "unknown"
    a = le if le > fye else None

    def rolled_m(d, src):
        return rolled_yf(d) if src == "yfinance" else (a is not None and a < d)

    delta = int(rolled_m(cur, cs)) - int(rolled_m(base, bs))
    return delta, {1: "shifted_heuristic", -1: "shifted_back_heuristic", 0: "no_shift_heuristic"}[delta]


def _fy_shift_heuristic(fye: date, le: date, base: date, cur: date) -> tuple[int, str]:
    window_end = fye + timedelta(days=ANNUAL_REPORT_WINDOW_DAYS)
    if le < fye - timedelta(days=366):
        return 0, "unknown"   # last-earnings date predates the prior FYE: bad source data
    if le <= fye:
        return 0, "no_shift"
    if le <= window_end:
        a = le
    else:
        if base >= window_end or cur <= fye:
            return 0, "no_shift"
        if base <= fye and cur >= window_end:
            return 1, "shifted"
        return 0, "ambiguous"
    if base <= a < cur:
        return 1, "shifted"
    return 0, "no_shift"


def check_numbers_agree(cur_fy1, base_fy1, base_fy2) -> bool:
    """Sanity check for a shifted ticker: the new FY1 should sit closer to the
    old FY2 than to the old FY1. False means the numbers disagree with the
    date decision (log only). True when it can't be judged."""
    if cur_fy1 is None or base_fy1 is None or base_fy2 is None:
        return True
    return abs(cur_fy1 - base_fy2) <= abs(cur_fy1 - base_fy1)


# ---------------------------------------------------------------------------
# Last-FYE cache
# ---------------------------------------------------------------------------


def load_fye_cache(path: Path | None = None) -> dict:
    p = path or FYE_CACHE_PATH
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_fye_cache(cache: dict, path: Path | None = None) -> None:
    p = path or FYE_CACHE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
                 encoding="utf-8")


def _taipei_today() -> date:
    return datetime.now(timezone(timedelta(hours=8))).date()


def get_last_fye(dd_ticker: str, yf_ticker: str, cache: dict) -> str | None:
    """Most recent fiscal-year-end date (YYYY-MM-DD) for `dd_ticker`, from
    yfinance info["lastFiscalYearEnd"] (UTC epoch seconds). Cached per ticker;
    refetched when older than FYE_CACHE_MAX_AGE_DAYS. Never raises: any failure
    returns the previously cached value (or None)."""
    today = _taipei_today()
    with _fye_lock:
        hit = dict(cache.get(dd_ticker) or {})
    checked = _to_date(hit.get("checked"))
    if hit.get("last_fye") and checked and (today - checked).days < FYE_CACHE_MAX_AGE_DAYS:
        return hit["last_fye"]
    try:
        import yfinance as yf
        ts = yf.Ticker(yf_ticker).info.get("lastFiscalYearEnd")
        fye = datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat() if ts else None
    except Exception:
        return hit.get("last_fye")
    if not fye:
        return hit.get("last_fye")
    with _fye_lock:
        cache[dd_ticker] = {"last_fye": fye, "checked": today.isoformat()}
    return fye


# ---------------------------------------------------------------------------
# Calendar-year basis (2026-10-08): every company compared on the same years
# ---------------------------------------------------------------------------
# A fiscal year belongs to the calendar year holding most of its months; one
# ending in June (6/6 split) counts as the year it ends. Display years are this
# calendar year + the next two (switch on Jan 1). The two years used for
# screening switch on June 1: by then every fiscal-year pattern (Dec, Jan, Mar,
# Sep, ...) has published its annual report, so all companies carry both years.
CONDITION_YEAR_SWITCH_MONTH = 6


def calendar_year_of_fy(fy_end) -> int | None:
    d = _to_date(fy_end)
    if d is None:
        return None
    return d.year if d.month >= 6 else d.year - 1


def display_calendar_years(as_of) -> tuple[int, int, int] | None:
    d = _to_date(as_of)
    return None if d is None else (d.year, d.year + 1, d.year + 2)


def condition_calendar_years(as_of) -> tuple[int, int] | None:
    d = _to_date(as_of)
    if d is None:
        return None
    y = d.year + (1 if d.month >= CONDITION_YEAR_SWITCH_MONTH else 0)
    return y, y + 1


def snapshot_fy1_end(last_fye, snapshot_date, past_earnings_dates=None,
                     source=None, last_earnings_date=None) -> date | None:
    """End date of the fiscal year a snapshot's FY1 column points at. Same
    rolled rule as fy_shift(): yfinance rolls at the FYE, Koyfin (xlsx) after
    the annual report A (first reported date in (FYE, FYE+120d]); with no A,
    assumed rolled once past FYE+120d. None when undecidable."""
    fye, d = _to_date(last_fye), _to_date(snapshot_date)
    if fye is None or d is None:
        return None
    while fye > d:                      # snapshot older than the cached FYE
        fye = _add_years(fye, -1)
    fye = roll_fye_forward(fye, d)
    nxt = _add_years(fye, 1)
    if _norm_src(source) == "yfinance":
        return nxt if d > fye else fye
    window_end = fye + timedelta(days=ANNUAL_REPORT_MAX_LAG_DAYS)
    past = sorted(x for x in (_to_date(v) for v in (past_earnings_dates or [])) if x)
    if past:
        a = next((x for x in past if x > fye), None)
    else:
        le = _to_date(last_earnings_date)
        a = le if le is not None and le > fye else None
        if a is None and d <= window_end:
            return None                 # no dates list, inside the window: unknown
    if a is not None and a > window_end:
        a = None
    if a is not None:
        return nxt if a < d else fye
    return nxt if d > window_end else fye


def calendar_year_columns(fy1_end, years) -> dict:
    """{calendar year: FY column 1..3, or None if outside the 3 columns}."""
    base = calendar_year_of_fy(fy1_end)
    out = {}
    for y in years or ():
        k = None if base is None else y - base + 1
        out[y] = k if k in (1, 2, 3) else None
    return out
