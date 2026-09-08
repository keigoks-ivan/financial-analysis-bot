"""
個股階段雷達 ("Stages") — zero-LLM daily builder for docs/stages/.

WHAT THIS IS
------------
A discovery-layer descriptor, same family as scripts/screener.py (RS+VCP)
and scripts/build_rs_turn.py (轉強觀察): it does NOT rank across stages,
does NOT blend RS×VCP into one score, and never feeds picks/GRP/dd-screener/
cockpit rankings. It answers "which stage of the lifecycle is this name in
right now" (弱勢→轉強→築底→收縮完成→領先) and "what happened, historically,
to names that just entered a given stage" (transition base rates — a
descriptive backward-look, never a timing call). See design spec
notes/site-internal/root/_stages_radar_design_20260908.md §3/§4/§5.

UNIVERSE: reuses build_rs_turn.build_universe() verbatim (same ~1,400-name
S&P 500 ∪ Nasdaq-100 ∪ S&P 400 ∪ DD-pool ∪ Russell-1000-proxy union) — this
is both a "don't invent a second universe" and a "same universe = same
tech_core cache keys" choice: when this script runs after build_rs_turn.py
in the same daily-us-close.yml run, its price download is served entirely
from scripts/tech_core.py's same-day cache (zero new network calls) because
build_rs_turn.py already pulled every one of these tickers at the same
2-year width this run also needs.

S1 (轉強) reuses build_rs_turn.compute_metrics()'s own 'passed' boolean
matrix directly — the six-condition math is never re-derived or re-typed
here, only imported, so a future PARAMS change in build_rs_turn.py can't
silently drift out of sync with what "S1" means on this page.

HISTORY: same whole-window-recompute-and-merge discipline as
build_rs_turn.py's history.json — the last WINDOW_DAYS trading days are
recomputed and OVERWRITE the merged file's matching dates every run; dates
outside that window are carried over unchanged from whatever is already on
disk. Every per-ticker stage string is re-padded to the full merged `dates`
length on every run (missing days -> '9', i.e. 過渡/no-signal) so the
"string length == len(dates)" invariant holds even as tickers enter/leave
the universe over time.
"""

import json
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tech_core
import build_rs_turn

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'docs' / 'stages' / 'data'
LATEST_JSON = DATA_DIR / 'latest.json'
HISTORY_JSON = DATA_DIR / 'history.json'
LAMP_JSON = DATA_DIR / 'lamp.json'
DOCS_T_DIR = ROOT / 'docs' / 't'

DEFINITION_VERSION = "v1"
TRANSITIONS_VERSION = "v2"  # 2026-09 owner decision: end-state + peak-state,
# not "ever touched" (S1 的「曾觸及弱勢」在舊口徑下把「剛脫離深回檔、第 60 日
# 前仍有一天貼在 200 日均線下」誤記成 74–78% 的假警訊；v2 只看第 60 日當天在
# 哪一段，以及期間到過的最高段，見 build_transitions_table()).
CONTROL_VERSION = "v1"  # 2026-09-08 owner decision: 轉強（S1）轉場基率不該拿
# 全母體（無條件）當比較基準——全母體被築底／領先這類進場時已結構性貼近收縮
# 完成以上的名字主導，不是轉強真正該比的對照組。v1 改成「同一天同樣剛從深回
# 檔上來、但沒有轉強」的配對對照組，見 build_control_deep_pullback()。深回檔
# 旗標門檻沿用 build_rs_turn.PARAMS 的 pullback_min_pct／dist_high_max_pct
# （condition 2／5 的同一套數字），不在此重複定義。
CONTROL_NOT_S1_LOOKBACK_DAYS = 5  # 對照組成員在配對日 t 之前這麼多個交易日內
# 本身也不能在轉強段（避免與轉強事件本身的剛轉出／即將轉入重疊，owner 決策原文）

STAGE_NAMES = {'S0': '弱勢', 'S1': '轉強', 'S2': '築底', 'S3': '收縮完成',
               'S4': '領先', 'S9': '過渡'}
STAGE_DIGIT = {'S0': '0', 'S1': '1', 'S2': '2', 'S3': '3', 'S4': '4', 'S9': '9'}
DIGIT_STAGE = {v: k for k, v in STAGE_DIGIT.items()}

WINDOW_DAYS = 250      # § 4 — trading days re-persisted to history.json every run
FORWARD_DAYS = 60      # § 4 — transition base-rate forward-look horizon
RECENCY_MIN_DAYS = 60  # § 4 — an "entry" must be >= this many trading days old
LOW_SAMPLE_N = 20      # § 4 — n below this gets a low_sample flag on the row

# ── stage thresholds (design spec §3 — kept here, not in build_rs_turn.PARAMS,
#    since these are Stages-specific; the S1 six-condition thresholds it DOES
#    share with 轉強觀察 stay solely in build_rs_turn.PARAMS, imported below) ──
S4_RS_IBD_MIN = 80
S4_DIST_HIGH_MIN_PCT = -8
S3_DIST_HIGH_MIN_PCT = -8
S3_ATR_RATIO_MAX = 0.7
S3_VOL_RATIO_MAX = 0.9
S2_DIST_HIGH_MIN_PCT = -25
S2_DIST_HIGH_MAX_PCT = -8
S2_TT_MIN = 3
EXTENDED_PCT_ABOVE_E21 = 15.0
EXTENDED_RSI_MIN = 80
RS_LINE_HIGH_TOL_PCT = -0.5


def _warn(msg):
    print(f"::warning::stages: {msg}")


# ── prices (own retry wrapper — same shape as build_rs_turn's, but needs
#    Open/High/Low/Close/Volume, not just Close/Volume, so it calls
#    tech_core.download_prices() directly instead of going through
#    build_rs_turn.download_prices_with_retry(). Coverage-floor thresholds
#    are IMPORTED from build_rs_turn.PARAMS, not re-typed, per design spec
#    §3's "import build_rs_turn.PARAMS ... 勿複製數字". ──
def download_ohlcv_with_retry(tickers, extra_benchmarks):
    P = build_rs_turn.PARAMS
    req = list(dict.fromkeys(tickers))
    all_tickers = req + [b for b in extra_benchmarks if b not in req]
    last_reason = None
    for attempt in range(1, build_rs_turn.MAX_DOWNLOAD_ATTEMPTS + 1):
        print(f"  price download attempt {attempt}/{build_rs_turn.MAX_DOWNLOAD_ATTEMPTS} "
              f"({len(all_tickers)} tickers incl. {extra_benchmarks}, via tech_core)")
        close_all = open_all = high_all = low_all = vol_all = None
        try:
            px = tech_core.download_prices(all_tickers, period='2y', auto_adjust=True)
            # single tuple assignment: if any .xs() raises, NONE of the five
            # names get (re)bound, so close_all stays None and the coverage
            # check below can't see a partial/inconsistent set of frames.
            open_all, high_all, low_all, close_all, vol_all = (
                px.xs('Open', axis=1, level=1), px.xs('High', axis=1, level=1),
                px.xs('Low', axis=1, level=1), px.xs('Close', axis=1, level=1),
                px.xs('Volume', axis=1, level=1))
        except Exception as e:
            last_reason = f"attempt {attempt} raised {type(e).__name__}: {e}"
            print(f"    ! {last_reason}")
            close_all = None

        if close_all is not None:
            n_sufficient = build_rs_turn._count_sufficient(close_all, req, P['min_bars'])
            frac = n_sufficient / len(req) if req else 0.0
            if frac >= P['coverage_floor_pct']:
                print(f"    ✓ attempt {attempt} succeeded: coverage {n_sufficient}/{len(req)} "
                      f"({frac:.1%}) >= floor {P['coverage_floor_pct']:.0%}")
                return open_all, high_all, low_all, close_all, vol_all
            last_reason = (f"attempt {attempt}: coverage {n_sufficient}/{len(req)} "
                            f"({frac:.1%}) < floor {P['coverage_floor_pct']:.0%}")
            print(f"    ! {last_reason}")

        if attempt < build_rs_turn.MAX_DOWNLOAD_ATTEMPTS:
            backoff = build_rs_turn.RETRY_BACKOFF_SECONDS[attempt - 1]
            print(f"    … retrying in {backoff:.0f}s")
            time.sleep(backoff)
    raise RuntimeError(
        f"price download failed after {build_rs_turn.MAX_DOWNLOAD_ATTEMPTS} attempts "
        f"(last: {last_reason})")


def _num(v, ndigits=None):
    return build_rs_turn._num(v, ndigits)


# ── vectorized indicators (§3) ────────────────────────────────────────────
def compute_stage_frame(highs, lows, closes, volumes, qqq, spy):
    """Returns (stage_df, fields) — stage_df is a date x ticker DataFrame of
    'S0'..'S9' string codes; fields is a dict of the wide DataFrames the
    latest-day row / lamp.json readers need."""
    C, H, L, V = closes, highs, lows, volumes

    # S1 六條件 — reuse build_rs_turn.compute_metrics() verbatim, not
    # re-derived (design spec §3: "import build_rs_turn.PARAMS 與同一套算式").
    m = build_rs_turn.compute_metrics(C, V, qqq)
    s1_passed = m['passed']
    eligible = m['eligible']
    e21 = m['e21']
    rs21, rs63 = m['rs21'], m['rs63']
    dist_high_pct = m['dist_high_pct']
    pullback_pct = m['pullback_pct']
    adv20_usd = m['adv20_usd']

    # 深回檔旗標（§control，2026-09-08 owner decision）——condition 2／5 的同一套
    # 門檻，imported not copied: pullback_pct <= PARAMS['pullback_min_pct'] AND
    # dist_high_pct <= PARAMS['dist_high_max_pct'] AND eligible（流動性／資料量）。
    P_deep = build_rs_turn.PARAMS
    deep = ((pullback_pct <= P_deep['pullback_min_pct'])
            & (dist_high_pct <= P_deep['dist_high_max_pct'])
            & eligible).fillna(False)

    sma50 = C.rolling(50).mean()
    sma150 = C.rolling(150).mean()
    sma200 = C.rolling(200).mean()
    sma200_21ago = sma200.shift(21)
    roll_max_252 = C.rolling(252, min_periods=1).max()
    roll_min_252 = C.rolling(252, min_periods=1).min()
    low_52w_ratio = C / roll_min_252

    tt1 = (C > sma150) & (sma150 > sma200)
    tt2 = sma200 > sma200_21ago
    tt3 = sma50 > sma150
    tt4 = C >= 1.30 * roll_min_252
    tt5 = C >= 0.75 * roll_max_252
    tt_pass_count = tt1.astype(int) + tt2.astype(int) + tt3.astype(int) + tt4.astype(int) + tt5.astype(int)

    # rs_ibd_pct — IBD 加權報酬（2*r63+r126+r189+r252）當日全母體百分位
    r63 = C / C.shift(63) - 1.0
    r126 = C / C.shift(126) - 1.0
    r189 = C / C.shift(189) - 1.0
    r252 = C / C.shift(252) - 1.0
    raw_ibd = 2 * r63 + r126 + r189 + r252
    rs_ibd_pct = raw_ibd.rank(axis=1, pct=True) * 100.0

    # ATR10/ATR60 (True Range on High/Low/Close)
    prev_c = C.shift(1)
    tr = pd.DataFrame(
        np.maximum(np.maximum((H - L).values, (H - prev_c).abs().values),
                   (L - prev_c).abs().values),
        index=C.index, columns=C.columns)
    atr10 = tr.rolling(10, min_periods=10).mean()
    atr60 = tr.rolling(60, min_periods=60).mean()
    atr_ratio = atr10 / atr60

    # vol10/vol50 (design spec §3 — distinct window from screener's own
    # 10d/60d vol_ratio; deliberate, not a typo)
    vol10 = V.rolling(10).mean()
    vol50 = V.rolling(50).mean()
    vol_ratio = vol10 / vol50

    # RSI14 (Wilder, same formula as screener.py::calc_extra_indicators)
    delta = C.diff()
    gain = delta.clip(lower=0)
    loss = (-delta.clip(upper=0))
    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    with np.errstate(divide='ignore', invalid='ignore'):
        rs = avg_gain / avg_loss
        rsi14 = 100 - 100 / (1 + rs)
    rsi14 = rsi14.where(avg_loss != 0, 100.0)

    extended = ((C / e21 - 1.0) * 100.0 > EXTENDED_PCT_ABOVE_E21) | (rsi14 > EXTENDED_RSI_MIN)

    # rs_line_high — C/SPY 是否在 252 日高的 0.5% 內 (screener.py's own
    # rs_line_new_high definition, reused literally)
    spy_aligned = spy.reindex(C.index).ffill()
    rs_line = C.div(spy_aligned, axis=0)
    rs_line_roll_max = rs_line.rolling(252, min_periods=1).max()
    rs_line_pct_from_high = (rs_line / rs_line_roll_max - 1.0) * 100.0
    rs_line_high = rs_line_pct_from_high >= RS_LINE_HIGH_TOL_PCT

    # ── stage classification (priority: S4 > S3 > S1 > S2 > S0 > S9) ──────
    cond_s4 = tt_pass_count.eq(5) & (rs_ibd_pct >= S4_RS_IBD_MIN) & (dist_high_pct >= S4_DIST_HIGH_MIN_PCT)
    cond_s3 = (tt_pass_count.eq(5) & (dist_high_pct >= S3_DIST_HIGH_MIN_PCT)
               & (atr_ratio < S3_ATR_RATIO_MAX) & (vol_ratio < S3_VOL_RATIO_MAX))
    cond_s1 = s1_passed
    cond_s2 = ((C > sma50) & (tt_pass_count >= S2_TT_MIN)
               & (dist_high_pct >= S2_DIST_HIGH_MIN_PCT) & (dist_high_pct < S2_DIST_HIGH_MAX_PCT))
    cond_s0 = (C < sma50) & (C < sma200) & (rs63 < 0)

    stage = pd.DataFrame('S9', index=C.index, columns=C.columns)
    for code, cond in [('S0', cond_s0), ('S2', cond_s2), ('S1', cond_s1),
                        ('S3', cond_s3), ('S4', cond_s4)]:
        stage = stage.where(~cond.fillna(False), code)
    # 流動性／資料量門檻同 rs-turn：不過者一律 S9（覆蓋前面任何分類）
    stage = stage.where(eligible.fillna(False), 'S9')

    fields = {
        'C': C, 'e21': e21, 'rs21': rs21, 'rs63': rs63, 'dist_high_pct': dist_high_pct,
        'rs_ibd_pct': rs_ibd_pct, 'tt_pass_count': tt_pass_count, 'atr_ratio': atr_ratio,
        'vol_ratio': vol_ratio, 'extended': extended, 'rs_line_high': rs_line_high,
        'adv20_usd': adv20_usd, 'eligible': eligible, 'qqq': m['qqq'], 'deep': deep,
    }
    return stage, fields


# ── history merge (§4 — same whole-window-overwrite discipline as
#    build_rs_turn.merge_history, adapted to Stages' dates+counts+qqq+stages
#    (+ deep, since 2026-09-08 §control) shape) ─────────────────────────────
def merge_history(existing, window_dates, stage_window, qqq_window, deep_window):
    existing = existing or {}
    old_dates = set(existing.get('dates', []))

    counts_new = {}
    for code in ('S0', 'S1', 'S2', 'S3', 'S4'):
        is_code = (stage_window == code)
        counts_new[code] = dict(zip(window_dates, is_code.sum(axis=1).astype(int).tolist()))

    qqq_new = {d: _num(v, 2) for d, v in zip(window_dates, qqq_window.tolist())}

    old_counts = existing.get('counts', {})
    merged_counts_map = {}
    for code in ('S0', 'S1', 'S2', 'S3', 'S4'):
        m = dict(zip(existing.get('dates', []), old_counts.get(code, [])))
        m.update(counts_new[code])
        merged_counts_map[code] = m

    old_qqq_map = dict(zip(existing.get('dates', []), existing.get('qqq', [])))
    old_qqq_map.update(qqq_new)

    all_dates = sorted(old_dates | set(window_dates))

    old_stages = existing.get('stages', {})
    new_stage_strings = {}
    for t in stage_window.columns:
        col = stage_window[t].tolist()
        new_stage_strings[t] = {d: STAGE_DIGIT.get(c, '9') for d, c in zip(window_dates, col)}

    old_deep = existing.get('deep', {})
    new_deep_strings = {}
    for t in deep_window.columns:
        col = deep_window[t].tolist()
        new_deep_strings[t] = {d: ('1' if v else '0') for d, v in zip(window_dates, col)}

    # stages 與 deep 共用同一份 ticker 集合（同一個 all_dates 長度、同一套「缺
    # 值補預設碼」規則），下游（imq-badge.js）才能安全地逐字元對齊兩條字串。
    all_tickers = (set(old_stages.keys()) | set(new_stage_strings.keys())
                   | set(old_deep.keys()) | set(new_deep_strings.keys()))

    merged_stages = {}
    merged_deep = {}
    for t in all_tickers:
        old_str = old_stages.get(t, '')
        old_map = dict(zip(existing.get('dates', []), old_str)) if old_str else {}
        old_map.update(new_stage_strings.get(t, {}))
        merged_stages[t] = ''.join(old_map.get(d, '9') for d in all_dates)

        old_deep_str = old_deep.get(t, '')
        old_deep_map = dict(zip(existing.get('dates', []), old_deep_str)) if old_deep_str else {}
        old_deep_map.update(new_deep_strings.get(t, {}))
        merged_deep[t] = ''.join(old_deep_map.get(d, '0') for d in all_dates)

    merged = {
        'schema': 'stages-history-v2',
        'definition_version': DEFINITION_VERSION,
        'control_version': CONTROL_VERSION,
        'updated': window_dates[-1] if window_dates else existing.get('updated'),
        'dates': all_dates,
        'counts': {code: [merged_counts_map[code].get(d, 0) for d in all_dates]
                   for code in ('S0', 'S1', 'S2', 'S3', 'S4')},
        'qqq': [old_qqq_map.get(d) for d in all_dates],
        'stages': merged_stages,
        'deep': merged_deep,
    }
    return merged


# ── transitions v2 (§4, 2026-09 owner decision — end-state + peak-state) ───
# Old v1 counted "ever touched stage X within FORWARD_DAYS", which read a
# name that merely brushed S0 for a single day (common right after leaving a
# deep pullback, while still under its 200dma) as a full round-trip back to
# 弱勢. v2 instead asks two separate questions per qualifying entry event:
#   end_stage  = stage exactly FORWARD_DAYS later (may be S9)
#   peak_stage = highest ORDERED_STAGES stage touched in (t, t+FORWARD_DAYS],
#                ignoring S9 days entirely (S9 is outside the lifecycle order)
ORDERED_STAGES = ('S0', 'S1', 'S2', 'S3', 'S4')  # lifecycle order; S9 excluded
STAGE_RANK = {s: i for i, s in enumerate(ORDERED_STAGES)}
END_BUCKETS = ('S0', 'S1', 'S2', 'S3', 'S4', 'S9')


def _raw_transition_stats(stage_window, from_stage):
    """For every ticker, every entry into `from_stage` (prior day != it) that
    is >= RECENCY_MIN_DAYS trading days old (i.e. has a full FORWARD_DAYS of
    realized forward data), records end_stage (day t+FORWARD_DAYS) and
    peak_stage (highest ORDERED_STAGES stage in (t, t+FORWARD_DAYS], S9 days
    skipped). Returns raw (unrounded) counts, not percentages, so several
    from-stage results can be summed into the pooled baseline without a
    round-then-sum error."""
    values = stage_window.values
    n_dates = values.shape[0]
    end_counts = {s: 0 for s in END_BUCKETS}
    peak_s3plus = 0
    peak_s4 = 0
    n_events = 0
    for j in range(values.shape[1]):
        col = values[:, j]
        for i in range(1, n_dates):
            if col[i] != from_stage or col[i - 1] == from_stage:
                continue
            if i > n_dates - 1 - FORWARD_DAYS:
                continue  # not >= RECENCY_MIN_DAYS old yet (== FORWARD_DAYS here)
            n_events += 1
            end_stage = col[i + FORWARD_DAYS]
            end_counts[end_stage] = end_counts.get(end_stage, 0) + 1
            peak_rank = -1
            for k in range(i + 1, i + 1 + FORWARD_DAYS):
                c = col[k]
                if c == 'S9':
                    continue
                r = STAGE_RANK.get(c)
                if r is not None and r > peak_rank:
                    peak_rank = r
            if peak_rank >= STAGE_RANK['S3']:
                peak_s3plus += 1
            if peak_rank == STAGE_RANK['S4']:
                peak_s4 += 1
    return {'n': n_events, 'end_counts': end_counts, 'peak_s3plus': peak_s3plus, 'peak_s4': peak_s4}


def _finalize_transition_stats(raw):
    n = raw['n']
    end_pct = {s: (round(100.0 * raw['end_counts'][s] / n, 1) if n else None) for s in END_BUCKETS}
    peak_S3plus_pct = round(100.0 * raw['peak_s3plus'] / n, 1) if n else None
    peak_S4_pct = round(100.0 * raw['peak_s4'] / n, 1) if n else None
    return {
        'n': n,
        'end_pct': end_pct,
        'peak_S3plus_pct': peak_S3plus_pct,
        'peak_S4_pct': peak_S4_pct,
        'end_S0_pct': end_pct['S0'],
        'low_sample': bool(n < LOW_SAMPLE_N),
    }


def _s1_entry_days(stage_window):
    """Row-indices i into `stage_window` (NOT per-ticker events — the
    underlying set of calendar days) where >= 1 ticker entered S1 on day i
    (prior day != S1) and the entry is >= RECENCY_MIN_DAYS old (has a full
    FORWARD_DAYS of realized forward data) — same recency gate
    _raw_transition_stats uses for from_stage='S1', collapsed to unique
    days so a day with several S1 entries only contributes ONE matched-day
    control cohort (see build_control_deep_pullback docstring)."""
    values = stage_window.values
    n_dates = values.shape[0]
    days = []
    for i in range(1, n_dates):
        if i > n_dates - 1 - FORWARD_DAYS:
            continue
        if np.any((values[i] == 'S1') & (values[i - 1] != 'S1')):
            days.append(i)
    return days


def _raw_control_stats(stage_window, deep_window, entry_days):
    """Matched control for S1 (§control, 2026-09-08 owner decision): for
    every day t in `entry_days` (a day that saw >= 1 S1 entry somewhere in
    the universe), every OTHER ticker that (a) carries the deep-pullback
    flag on day t, (b) is itself NOT in S1 on day t, and (c) was not in S1
    on any of the CONTROL_NOT_S1_LOOKBACK_DAYS trading days immediately
    before t, is exactly one control event — identified by its (ticker, t)
    pair (looping over the deduped `entry_days` set, not per S1-ticker-event,
    is what keeps each pair unique even when several tickers enter S1 on the
    same day t). End/peak stats computed along that ticker's own forward
    path from t, identically to _raw_transition_stats."""
    stage_values = stage_window.values
    deep_values = deep_window.values
    n_tickers = stage_values.shape[1]
    end_counts = {s: 0 for s in END_BUCKETS}
    peak_s3plus = 0
    peak_s4 = 0
    n_events = 0
    for i in entry_days:
        lookback_start = max(0, i - CONTROL_NOT_S1_LOOKBACK_DAYS)
        for j in range(n_tickers):
            if not deep_values[i, j]:
                continue
            if stage_values[i, j] == 'S1':
                continue
            if np.any(stage_values[lookback_start:i, j] == 'S1'):
                continue
            n_events += 1
            end_stage = stage_values[i + FORWARD_DAYS, j]
            end_counts[end_stage] = end_counts.get(end_stage, 0) + 1
            peak_rank = -1
            for k in range(i + 1, i + 1 + FORWARD_DAYS):
                c = stage_values[k, j]
                if c == 'S9':
                    continue
                r = STAGE_RANK.get(c)
                if r is not None and r > peak_rank:
                    peak_rank = r
            if peak_rank >= STAGE_RANK['S3']:
                peak_s3plus += 1
            if peak_rank == STAGE_RANK['S4']:
                peak_s4 += 1
    return {'n': n_events, 'end_counts': end_counts, 'peak_s3plus': peak_s3plus, 'peak_s4': peak_s4}


def build_control_deep_pullback(stage_window, deep_window):
    """Matched control for 轉強（S1）— owner decision 2026-09-08: the pooled
    `baseline` (全母體無條件) is dominated by 築底／領先 entries that are
    structurally already near S3+ the moment they're entered, so it
    overstates what 轉強 itself adds. This asks the narrower, owner-specified
    question instead: of tickers that were ALSO deep-in-a-pullback the same
    day, but did NOT show the 轉強 six-condition pattern, what happened to
    them over the same forward window? Same v2 end/peak stats shape as
    `baseline`/`rows`, so the page can diff them cell-for-cell."""
    entry_days = _s1_entry_days(stage_window)
    raw = _raw_control_stats(stage_window, deep_window, entry_days)
    return _finalize_transition_stats(raw)


def build_transitions_table(stage_window, deep_window):
    """Returns {'rows': [per-from-stage v2 stats for S0/S1/S2/S3],
    'baseline': v2 stats pooled over entry events of EVERY ordered stage
    (S0..S4) — the unconditional 母體無條件比率, 'control_deep_pullback':
    the matched deep-pullback-but-not-S1 control (see
    build_control_deep_pullback), 'control_version': CONTROL_VERSION}."""
    raws = {s: _raw_transition_stats(stage_window, s) for s in ORDERED_STAGES}
    rows = []
    for from_stage in ('S0', 'S1', 'S2', 'S3'):
        row = {'from': from_stage}
        row.update(_finalize_transition_stats(raws[from_stage]))
        rows.append(row)
    baseline_raw = {
        'n': sum(raws[s]['n'] for s in ORDERED_STAGES),
        'end_counts': {b: sum(raws[s]['end_counts'][b] for s in ORDERED_STAGES) for b in END_BUCKETS},
        'peak_s3plus': sum(raws[s]['peak_s3plus'] for s in ORDERED_STAGES),
        'peak_s4': sum(raws[s]['peak_s4'] for s in ORDERED_STAGES),
    }
    baseline = _finalize_transition_stats(baseline_raw)
    control = build_control_deep_pullback(stage_window, deep_window)
    return {'rows': rows, 'baseline': baseline,
            'control_deep_pullback': control, 'control_version': CONTROL_VERSION}


# ── per-ticker path / stage_since (from the MERGED, potentially
#    multi-month, digit string — not just this run's window — so
#    days_in_stage stays correct once a streak predates the window) ───────
def ticker_path_info(digit_str, dates):
    if not digit_str:
        return None
    cur = digit_str[-1]
    i = len(digit_str) - 1
    while i > 0 and digit_str[i - 1] == cur:
        i -= 1
    days_in_stage = len(digit_str) - i
    stage_since = dates[i] if i < len(dates) else dates[-1]
    prev_code = digit_str[i - 1] if i > 0 else None
    # last <=3 run-length-encoded segments, chronological, for `path`
    segments = []
    j = len(digit_str) - 1
    while j >= 0 and len(segments) < 3:
        c = digit_str[j]
        k = j
        while k > 0 and digit_str[k - 1] == c:
            k -= 1
        segments.append(c)
        j = k - 1
    segments.reverse()
    path = '→'.join(segments)
    return {
        'days_in_stage': days_in_stage,
        'stage_since': stage_since,
        'prev_stage': DIGIT_STAGE.get(prev_code) if prev_code else None,
        'prev_stage_ended': days_in_stage if prev_code else None,
        'path': path,
    }


def build():
    run_started = datetime.now(timezone.utc)
    print(f"=== Stages Build ({DEFINITION_VERSION}) — {run_started.isoformat()} ===")

    tickers, univ_payload = build_rs_turn.build_universe()
    if tickers is None:
        _warn("universe build failed (see build_rs_turn.build_universe output) — abort")
        return None
    print(f"  universe total: {len(tickers)} (sources={univ_payload['sources']})")

    benchmark = build_rs_turn.PARAMS['benchmark']  # QQQ, for S1's rs21/rs63
    extra = [benchmark, 'SPY']  # SPY for rs_line_high (screener.py's own benchmark)
    try:
        opens, highs, lows, closes, volumes = download_ohlcv_with_retry(tickers, extra)
    except RuntimeError as e:
        _warn(f"{e} — abort, latest/history untouched")
        return None

    n_covered = int((closes.notna().sum() >= build_rs_turn.PARAMS['min_bars']).sum())
    print(f"  price coverage: {n_covered}/{len(tickers)} tickers with >= "
          f"{build_rs_turn.PARAMS['min_bars']} bars")

    qqq = closes[benchmark].dropna() if benchmark in closes.columns else pd.Series(dtype=float)
    spy = closes['SPY'].dropna() if 'SPY' in closes.columns else pd.Series(dtype=float)
    cols = [t for t in tickers if t in closes.columns]
    C, H, L, V = closes[cols], highs[cols], lows[cols], volumes[cols]

    stage, fields = compute_stage_frame(H, L, C, V, qqq, spy)

    as_of_idx = C.index[-1]
    as_of = as_of_idx.strftime('%Y-%m-%d')

    window_idx = stage.index[-WINDOW_DAYS:]
    stage_window = stage.loc[window_idx]
    window_dates = [d.strftime('%Y-%m-%d') for d in window_idx]
    qqq_window = fields['qqq'].reindex(window_idx).values
    deep_window = fields['deep'].reindex(columns=stage_window.columns).loc[window_idx]

    existing_history = None
    if HISTORY_JSON.exists():
        try:
            existing_history = json.loads(HISTORY_JSON.read_text(encoding='utf-8'))
        except Exception:
            existing_history = None
    merged_history = merge_history(existing_history, window_dates, stage_window, qqq_window, deep_window)

    transitions = build_transitions_table(stage_window, deep_window)

    stage_today = stage.loc[as_of_idx]
    counts_today = {code: int((stage_today == code).sum()) for code in
                    ('S0', 'S1', 'S2', 'S3', 'S4', 'S9')}
    n_eligible_today = int(fields['eligible'].loc[as_of_idx].sum())

    merged_dates = merged_history['dates']
    rows = []
    for t in cols:
        s = stage_today[t]
        if s not in ('S1', 'S2', 'S3', 'S4'):
            continue
        digit_str = merged_history['stages'].get(t, '')
        info = ticker_path_info(digit_str, merged_dates)
        if info is None:
            continue
        hub = f"/t/{t}.html" if (DOCS_T_DIR / f"{t}.html").exists() else None
        rows.append({
            'ticker': t, 'stage': s, 'stage_name': STAGE_NAMES[s],
            'days_in_stage': info['days_in_stage'], 'stage_since': info['stage_since'],
            'prev_stage': info['prev_stage'], 'prev_stage_ended': info['prev_stage_ended'],
            'path': info['path'],
            'rs_ibd_pct': _num(fields['rs_ibd_pct'].at[as_of_idx, t], 1),
            'rs21': _num(fields['rs21'].at[as_of_idx, t], 1),
            'rs63': _num(fields['rs63'].at[as_of_idx, t], 1),
            'dist_52w_high_pct': _num(fields['dist_high_pct'].at[as_of_idx, t], 1),
            'tt_pass_count': int(fields['tt_pass_count'].at[as_of_idx, t]),
            'atr_ratio': _num(fields['atr_ratio'].at[as_of_idx, t], 2),
            'vol_ratio': _num(fields['vol_ratio'].at[as_of_idx, t], 2),
            'extended': bool(fields['extended'].at[as_of_idx, t]),
            'rs_line_high': bool(fields['rs_line_high'].at[as_of_idx, t]),
            'adv20_usd': (int(round(fields['adv20_usd'].at[as_of_idx, t]))
                          if pd.notna(fields['adv20_usd'].at[as_of_idx, t]) else None),
            'price': _num(C.at[as_of_idx, t], 2),
            'hub': hub,
        })

    stage_order = {'S1': 0, 'S2': 1, 'S3': 2, 'S4': 3}
    rows.sort(key=lambda r: (stage_order.get(r['stage'], 9), r['days_in_stage']))

    lamp = {t: stage_today[t] for t in cols}

    latest_payload = {
        'schema': 'stages-v1',
        'definition_version': DEFINITION_VERSION,
        'transitions_version': TRANSITIONS_VERSION,
        'as_of': as_of,
        'run_timestamp': run_started.isoformat(),
        'benchmark': benchmark,
        'params': {
            's4_rs_ibd_min': S4_RS_IBD_MIN, 's4_dist_high_min_pct': S4_DIST_HIGH_MIN_PCT,
            's3_dist_high_min_pct': S3_DIST_HIGH_MIN_PCT, 's3_atr_ratio_max': S3_ATR_RATIO_MAX,
            's3_vol_ratio_max': S3_VOL_RATIO_MAX, 's2_dist_high_min_pct': S2_DIST_HIGH_MIN_PCT,
            's2_dist_high_max_pct': S2_DIST_HIGH_MAX_PCT, 's2_tt_min': S2_TT_MIN,
            'extended_pct_above_e21': EXTENDED_PCT_ABOVE_E21, 'extended_rsi_min': EXTENDED_RSI_MIN,
            'window_days': WINDOW_DAYS, 'forward_days': FORWARD_DAYS,
            'recency_min_days': RECENCY_MIN_DAYS,
            's1_params': build_rs_turn.PARAMS,
            'control_not_s1_lookback_days': CONTROL_NOT_S1_LOOKBACK_DAYS,
        },
        'universe': {'total': len(tickers), 'covered': n_covered, 'eligible': n_eligible_today},
        'counts_today': counts_today,
        'transitions': transitions,
        'rows': rows,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON.write_text(json.dumps(latest_payload, ensure_ascii=False, indent=1) + '\n',
                            encoding='utf-8')
    HISTORY_JSON.write_text(json.dumps(merged_history, ensure_ascii=False, indent=1) + '\n',
                             encoding='utf-8')
    LAMP_JSON.write_text(json.dumps({
        'as_of': as_of, 'definition_version': DEFINITION_VERSION, 'lamp': lamp,
    }, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    print(f"  ✓ wrote {LATEST_JSON.relative_to(ROOT)}: counts_today={counts_today} rows={len(rows)}")
    print(f"  ✓ wrote {HISTORY_JSON.relative_to(ROOT)}: {len(merged_history['dates'])} dates")
    print(f"  ✓ wrote {LAMP_JSON.relative_to(ROOT)}: {len(lamp)} tickers")
    for row in transitions['rows']:
        print(f"  transitions {row['from']}: n={row['n']} {row}")
    print(f"  transitions baseline: n={transitions['baseline']['n']} {transitions['baseline']}")
    print(f"  transitions control_deep_pullback (control_version={transitions['control_version']}): "
          f"n={transitions['control_deep_pullback']['n']} {transitions['control_deep_pullback']}")
    return latest_payload


def main():
    try:
        result = build()
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — outputs left unchanged")
        _warn(f"build failed ({type(e).__name__}: {e})")
        sys.exit(0)
    if result is None:
        sys.exit(0)


if __name__ == '__main__':
    main()
