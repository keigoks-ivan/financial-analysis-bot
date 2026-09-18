"""VCP (Volatility Contraction Pattern, Mark Minervini style) — pure calculation core.

Split out of scripts/screener.py on 2026-09-18 (VCP depth 1, see
notes/site-internal/root/_seat_engine_v5_1_20260918.md §3 / knowledge/rule_ledger.md
「VCP 深度 1」列) so scripts/build_dd_screener.py can reuse calc_vcp() without
importing screener.py — screener.py has an import-time side effect
(`HISTORY_DIR.mkdir(parents=True, exist_ok=True)`, writes to docs/screener/history/
just by being imported), which is not safe to trigger from a different pipeline
(dd-screener) that has nothing to do with docs/screener/. screener.py (and
screener_tw.py/screener_jp.py/screener_my.py, which already do
`from screener import find_local_highs, calc_vcp, ...`) now import these three
names from here instead — behavior-preserving, no signature/logic changes.
"""

import numpy as np
import pandas as pd


def find_local_highs(highs, window=90):
    """Find local high points in the last `window` days."""
    if len(highs) < window:
        return []
    segment = highs.iloc[-window:]
    peaks = []
    for i in range(10, len(segment) - 5):
        left = max(0, i - 10)
        right = min(len(segment), i + 6)
        if segment.iloc[i] == segment.iloc[left:right].max():
            peaks.append((segment.index[i], segment.iloc[i], i))
    # Merge peaks within 10 days
    merged = []
    for p in peaks:
        if merged and (p[2] - merged[-1][2]) < 10:
            if p[1] > merged[-1][1]:
                merged[-1] = p
        else:
            merged.append(p)
    return merged


VCP_MIN_BARS = 221  # 200 (MA200) + 21 (MA200-21-bars-ago), the Trend Template's tightest need


def _vcp_empty_result(trend_ok=False, tt_fails=None):
    """Shared zero-score shape for insufficient-data / degenerate cases.
    Existing keys keep the same meaning/shape they had pre-2026-09-08;
    new keys (trend_template_pass/tt_fails/contraction_ok/vcp_gate/
    base_age_days/base_high/vol_dryup_ratio) default to the
    fails-everything state so a downstream `vcp_gate` read never KeyErrors."""
    return {
        'score': 0, 'pullback_count': 0, 'last_pullback_pct': 0,
        'dist_from_high_pct': 0, 'atr_ratio': 1.0, 'vol_ratio': 1.0,
        'trend_ok': bool(trend_ok),
        'trend_template_pass': False, 'tt_fails': tt_fails or ['insufficient_data'],
        'contraction_ok': False, 'vcp_gate': 'trend',
        'base_age_days': 0, 'base_high': 0.0, 'vol_dryup_ratio': 1.0,
    }


def calc_vcp(closes, highs, lows, volumes):
    """Calculate VCP score (2026-09-08 rewrite: VCP becomes gate + score).

    Same signature as before (superset of return keys — existing keys keep
    their meaning: score, pullback_count, last_pullback_pct,
    atr_ratio, vol_ratio, trend_ok; dist_from_high_pct now measured vs
    base_high instead of the old fixed 90-day high).

    Shape:
      - Window = last min(260, len) bars. base_high = max High in that
        window, base_high_idx its position. Contraction detection (reuses
        find_local_highs) runs only on the segment from base_high_idx to
        the end — the base_high itself seeds the pullback sequence as
        anchor #1 (find_local_highs' own edge margins can never flag a
        peak within its first ~10 bars, so it would otherwise be missed).
        Base age (bars since base_high) must be >= 15, else pullback_count
        is forced to 0 (no established base yet to measure contractions
        in).
      - Trend Template gate (trend_template_pass / tt_fails): price >
        MA150 > MA200; MA200 today > MA200 21 bars ago; MA50 > MA150;
        price >= 1.30x 52-week low close; price >= 0.75x 52-week high
        close. trend_ok (legacy) stays price > MA150 > MA200 only.
      - Contraction gate (contraction_ok): pullback_count >= 2 AND every
        pullback_pct smaller than the one before it.
      - Score table (component cap 100 before gates): trend template pass
        10; contraction count 2-4 -> 15 (1 -> 5, >4 -> 8); decreasing
        magnitudes 20; higher lows 15; volume dry-up 15 (<0.7x 50d avg) /
        8 (<0.9x); last pullback tightness 15/10/5 for <4/<6/<10%;
        distance from base_high 10/6/3 for <3/<5/<10%, -5 if >=10%;
        ATR10/ATR60 <0.5 -> 10, <0.7 -> 5.
      - Gates: trend template fail -> score capped at 30, vcp_gate="trend";
        else contraction gate fail -> score capped at 40,
        vcp_gate="contraction"; else vcp_gate="pass".
    """
    if len(closes) < VCP_MIN_BARS:
        return _vcp_empty_result()

    price = closes.iloc[-1]
    ma50 = closes.iloc[-50:].mean()
    ma150 = closes.iloc[-150:].mean()
    ma200 = closes.iloc[-200:].mean()
    ma200_21_ago = closes.iloc[-(200 + 21):-21].mean()
    trend_ok = bool(price > ma150 > ma200)  # legacy key, meaning unchanged

    window_52w = closes.iloc[-min(252, len(closes)):]
    low_52w = window_52w.min()
    high_52w = window_52w.max()

    tt_fails = []
    if not (price > ma150 > ma200):
        tt_fails.append('price>MA150>MA200')
    if not (ma200 > ma200_21_ago):
        tt_fails.append('MA200_rising')
    if not (ma50 > ma150):
        tt_fails.append('MA50>MA150')
    if not (low_52w > 0 and price >= 1.30 * low_52w):
        tt_fails.append('>=1.30x52wLow')
    if not (high_52w > 0 and price >= 0.75 * high_52w):
        tt_fails.append('>=0.75x52wHigh')
    trend_template_pass = len(tt_fails) == 0

    # ── Base + contraction detection ──────────────────────────────────
    window_n = min(260, len(closes))
    highs_w = highs.iloc[-window_n:]
    lows_w = lows.iloc[-window_n:]
    vols_w = volumes.iloc[-window_n:]

    base_high_idx = int(np.argmax(highs_w.values))
    base_high = float(highs_w.iloc[base_high_idx])
    base_age_days = (window_n - 1) - base_high_idx

    seg_highs = highs_w.iloc[base_high_idx:]
    seg_lows = lows_w.iloc[base_high_idx:]
    seg_vols = vols_w.iloc[base_high_idx:]

    if base_age_days >= 15:
        # find_local_highs' own left-margin (10 bars) means it can never
        # flag the segment's first point as a peak — seed base_high as
        # anchor #1 explicitly, then append any later local highs found
        # within the segment (dropping any duplicate right at position 0).
        later_peaks = [p for p in find_local_highs(seg_highs, window=len(seg_highs)) if p[2] >= 10]
        peaks = [(seg_highs.index[0], base_high, 0)] + later_peaks
    else:
        peaks = []

    pullbacks = []
    for i in range(1, len(peaks)):
        idx_start = peaks[i-1][2]
        idx_end = peaks[i][2]
        seg_low = seg_lows.iloc[idx_start:idx_end+1]
        seg_vol = seg_vols.iloc[idx_start:idx_end+1]
        if len(seg_low) == 0:
            continue
        low_val = seg_low.min()
        high_val = peaks[i-1][1]
        pullback_pct = (high_val - low_val) / high_val * 100
        if pullback_pct < 3:
            continue
        avg_vol = seg_vol.mean() if len(seg_vol) > 0 else 0
        pullbacks.append({
            'high': high_val, 'low': low_val,
            'pullback_pct': pullback_pct, 'avg_vol': avg_vol
        })

    n = len(pullbacks)

    decreasing_ok = n >= 2 and all(pullbacks[i]['pullback_pct'] < pullbacks[i-1]['pullback_pct'] for i in range(1, n))
    higher_lows_ok = n >= 2 and all(pullbacks[i]['low'] > pullbacks[i-1]['low'] for i in range(1, n))
    contraction_ok = decreasing_ok

    # ── Score table ──────────────────────────────────────────────────
    score = 10 if trend_template_pass else 0

    if 2 <= n <= 4:
        score += 15
    elif n == 1:
        score += 5
    elif n > 4:
        score += 8

    if decreasing_ok:
        score += 20

    if higher_lows_ok:
        score += 15

    # Volume dry-up: mean volume of the LAST contraction segment vs 50-day avg
    vol_50 = volumes.iloc[-50:].mean()
    if n >= 1 and vol_50 > 0:
        vol_dryup_ratio = pullbacks[-1]['avg_vol'] / vol_50
    else:
        vol_dryup_ratio = 1.0
    if vol_dryup_ratio < 0.7: score += 15
    elif vol_dryup_ratio < 0.9: score += 8

    # Last pullback magnitude (tightness)
    last_pb = pullbacks[-1]['pullback_pct'] if pullbacks else 0
    if last_pb > 0:
        if last_pb < 4: score += 15
        elif last_pb < 6: score += 10
        elif last_pb < 10: score += 5

    # Distance from base_high (was: 90-day high)
    dist_pct = (base_high - price) / base_high * 100 if base_high > 0 else 0
    if dist_pct < 3: score += 10
    elif dist_pct < 5: score += 6
    elif dist_pct < 10: score += 3
    elif dist_pct >= 10: score -= 5

    # ATR contraction
    def atr(h, l, c, n):
        tr = pd.concat([h-l, (h-c.shift(1)).abs(), (l-c.shift(1)).abs()], axis=1).max(axis=1)
        return tr.rolling(n).mean().iloc[-1]

    atr10 = atr(highs, lows, closes, 10)
    atr60 = atr(highs, lows, closes, 60)
    atr_ratio = atr10 / atr60 if atr60 > 0 else 1.0
    if atr_ratio < 0.5: score += 10
    elif atr_ratio < 0.7: score += 5

    score = max(0, min(100, score))

    # ── Gates ────────────────────────────────────────────────────────
    if not trend_template_pass:
        score = min(score, 30)
        vcp_gate = 'trend'
    elif not contraction_ok:
        score = min(score, 40)
        vcp_gate = 'contraction'
    else:
        vcp_gate = 'pass'

    # Volume ratio (legacy key, meaning unchanged: 10d avg vs 60d avg)
    vol_10 = volumes.iloc[-10:].mean()
    vol_60 = volumes.iloc[-60:].mean()
    vol_ratio = vol_10 / vol_60 if vol_60 > 0 else 1.0

    return {
        'score': score,
        'pullback_count': n,
        'last_pullback_pct': round(last_pb, 1),
        'dist_from_high_pct': round(dist_pct, 1),
        'atr_ratio': round(atr_ratio, 2),
        'vol_ratio': round(vol_ratio, 2),
        'trend_ok': trend_ok,
        'trend_template_pass': bool(trend_template_pass),
        'tt_fails': tt_fails,
        'contraction_ok': bool(contraction_ok),
        'vcp_gate': vcp_gate,
        'base_age_days': int(base_age_days),
        'base_high': round(base_high, 2),
        'vol_dryup_ratio': round(float(vol_dryup_ratio), 2),
    }
