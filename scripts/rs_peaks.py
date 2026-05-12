"""
RS peaks aggregator.
Output: docs/screener/rs_peaks.json

Reads all daily snapshots in docs/screener/history/*.json and computes per ticker:
  - rs_score_today           : from latest.json (most-recent snapshot)
  - rs_score_max_in_history  : max rs_score across all history files
  - rs_score_max_date        : YYYY-MM-DD of the peak
  - at_new_high              : rs_score_today >= rs_score_max_in_history
  - days_since_peak          : (today - peak_date) in calendar days

Today (2026-05-12) history depth is ~14 days; the workflow appends 1 file/day
via daily-screener-us.yml, so coverage grows automatically. After ~6 months
this becomes a meaningful "RS 線新高" detector.

Consumed by docs/flow/rs-board.html for the 🟢 RS 新高 bucket classification.

Usage:
  python scripts/rs_peaks.py
"""

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREENER_DIR = ROOT / 'docs' / 'screener'
HISTORY_DIR = SCREENER_DIR / 'history'
LATEST_PATH = SCREENER_DIR / 'latest.json'
OUTPUT_PATH = SCREENER_DIR / 'rs_peaks.json'


def _load_rankings(path: Path):
    with open(path) as f:
        d = json.load(f)
    return d.get('rankings') or []


def main():
    if not LATEST_PATH.exists():
        raise SystemExit(f"latest.json not found at {LATEST_PATH}")
    if not HISTORY_DIR.exists():
        raise SystemExit(f"history dir not found at {HISTORY_DIR}")

    today_iso = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    generated_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"=== RS peaks aggregator: {today_iso} ===\n")

    # Today's RS scores from latest.json
    today_rankings = _load_rankings(LATEST_PATH)
    today_rs = {r['ticker']: r.get('rs_score') for r in today_rankings if r.get('rs_score') is not None}
    print(f"  latest.json: {len(today_rs)} tickers with rs_score")

    # Walk history/ — each file is YYYY-MM-DD.json
    history_files = sorted(HISTORY_DIR.glob('*.json'))
    print(f"  history/ : {len(history_files)} daily snapshots")
    if not history_files:
        raise SystemExit("history/ is empty; nothing to aggregate")

    # peaks[ticker] = (max_rs_score, date_iso)
    peaks: dict = {}
    for hf in history_files:
        snap_date = hf.stem  # "2026-05-11"
        try:
            rows = _load_rankings(hf)
        except Exception as e:
            print(f"  WARN: skipping {hf.name}: {e}")
            continue
        for r in rows:
            t = r.get('ticker')
            s = r.get('rs_score')
            if t is None or s is None:
                continue
            cur = peaks.get(t)
            if cur is None or s > cur[0]:
                peaks[t] = (float(s), snap_date)

    print(f"  peaks tracked: {len(peaks)} tickers")

    # Build output per ticker — union of today + history
    all_tickers = set(today_rs.keys()) | set(peaks.keys())
    today_d = date.fromisoformat(today_iso)
    out_tickers = {}
    at_new_high_count = 0
    for t in all_tickers:
        s_today = today_rs.get(t)
        peak = peaks.get(t)
        if peak is None:
            # no history yet; today IS the peak by definition
            out_tickers[t] = {
                'rs_score_today': s_today,
                'rs_score_max_in_history': s_today,
                'rs_score_max_date': today_iso,
                'at_new_high': True if s_today is not None else None,
                'days_since_peak': 0,
            }
            if s_today is not None:
                at_new_high_count += 1
            continue
        peak_score, peak_date_iso = peak
        try:
            peak_date = date.fromisoformat(peak_date_iso)
            dsp = (today_d - peak_date).days
        except Exception:
            dsp = None
        at_high = (s_today is not None) and (s_today >= peak_score)
        out_tickers[t] = {
            'rs_score_today': s_today,
            'rs_score_max_in_history': peak_score,
            'rs_score_max_date': peak_date_iso,
            'at_new_high': at_high,
            'days_since_peak': dsp,
        }
        if at_high:
            at_new_high_count += 1

    output = {
        'generated_at': generated_at,
        'date': today_iso,
        'history_days_available': len(history_files),
        'count': len(out_tickers),
        'tickers': out_tickers,
    }

    SCREENER_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  ✓ Output: {OUTPUT_PATH}")
    print(f"  ✓ Tickers: {len(out_tickers)}")
    print(f"  ✓ at_new_high count: {at_new_high_count}/{len(out_tickers)} "
          f"({100*at_new_high_count/len(out_tickers):.0f}%)")


if __name__ == '__main__':
    main()
