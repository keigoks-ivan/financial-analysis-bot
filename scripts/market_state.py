"""
Market Regime Engine (IBD-style Big Picture).

Per-index state machine on SPY / QQQ / IWM with 5 states:
  correction / rally_attempt / early_uptrend / confirmed_uptrend / under_pressure

Detects Day 1 (first up-close after recent low), Follow-Through Day (FTD),
and Distribution Days. Combines three indices into a dominant overlay with
three rules (unanimous / narrow_leadership / mixed).

v1 is memoryless: state is inferred from current price action each run.
See TODO inside infer_state() for v2 persistence plan.

Usage:
  python scripts/market_state.py
"""

import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           'yfinance', 'pandas', 'numpy', '-q'])
    import numpy as np
    import pandas as pd
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / 'docs' / 'screener' / 'market_state.json'

INDICES = ['SPY', 'QQQ', 'IWM']

STATE_RANK = {
    'correction': 0,
    'rally_attempt': 1,
    'under_pressure': 2,
    'confirmed_uptrend': 3,
    'early_uptrend': 4,
}

ADVICE_MAP = {
    'correction': {
        'zh': '不主動建倉，等大盤確認轉強。今日 ATH Hunter 六層可能全空，屬於正常現象。',
        'en': 'Stay defensive. Avoid new positions. Wait for follow-through confirmation.',
    },
    'rally_attempt': {
        'zh': '反彈嘗試中，Day {rally_day} of 7。不動，等待 FTD 確認（漲幅 ≥ 1.7% + 量增）。',
        'en': 'Rally attempt Day {rally_day} of 7. Hold. Wait for FTD confirmation.',
    },
    'early_uptrend': {
        'zh': '🔥 黃金進場窗口 · FTD 後 {days_since_ftd} 天。主動建倉 S/A 級，可承擔正常部位。',
        'en': 'Golden window: Day {days_since_ftd} post-FTD. Build new positions in S/A tier candidates.',
    },
    'confirmed_uptrend': {
        'zh': '確認上升趨勢已 {days_in_state} 天。維持持倉，謹慎加碼，只動 S 級候選股。',
        'en': 'Confirmed uptrend for {days_in_state} days. Hold positions, add only to S-tier.',
    },
    'under_pressure': {
        'zh': '⚠️ 上升趨勢承壓 · 過去 25 天有 {dd_count} 個 Distribution Days。不加碼，觀察證偽條件。',
        'en': 'Uptrend under pressure. {dd_count} distribution days in 25. No new positions.',
    },
}


def fetch_indices(period='400d'):
    df = yf.download(INDICES, period=period, interval='1d',
                     group_by='ticker', auto_adjust=True,
                     progress=False, threads=True)
    out = {}
    for t in INDICES:
        sub = df[t].dropna(subset=['Close']).copy()
        out[t] = sub
    return out


def compute_indicators(df):
    df = df.copy()
    df['ma50'] = df['Close'].rolling(50).mean()
    df['ma200'] = df['Close'].rolling(200).mean()
    df['vol_ratio'] = df['Volume'] / df['Volume'].shift(1)
    df['close_change_pct'] = df['Close'].pct_change() * 100
    return df


def detect_distribution_days(df, window=25):
    recent = df.iloc[-window:]
    is_dd = (recent['close_change_pct'] <= -0.2) & (recent['vol_ratio'] > 1.0)
    dates = [d.strftime('%Y-%m-%d') for d in recent.index[is_dd]]
    return int(is_dd.sum()), sorted(dates, reverse=True)


def detect_rally_day1(df, lookback=30):
    """Day 1 = first up-close day at or after the most recent low in lookback window."""
    recent = df.iloc[-lookback:]
    if len(recent) < 2:
        return None, None
    low_idx = recent['Close'].idxmin()
    after_low = df.loc[low_idx:]
    if len(after_low) < 2:
        return None, None
    up_mask = after_low['Close'] > after_low['Close'].shift(1)
    up_days = after_low[up_mask]
    if len(up_days) == 0:
        return None, None
    day1 = up_days.index[0]
    day1_pos = df.index.get_loc(day1)
    rally_day_count = len(df) - day1_pos  # Day 1 = 1, today = N
    return day1, int(rally_day_count)


def detect_ftd(df, day1_date):
    """FTD within trading-days 4-7 after Day 1. Returns last qualifying day per spec."""
    if day1_date is None:
        return None
    after_day1 = df.loc[day1_date:]
    if len(after_day1) < 4:
        return None
    window = after_day1.iloc[3:7]  # positions 3..6 = Days 4..7 (1-indexed from Day 1)
    candidates = window[(window['close_change_pct'] >= 1.7) &
                        (window['vol_ratio'] > 1.0)]
    if len(candidates) == 0:
        return None
    last_ftd = candidates.index[-1]
    ftd_pos = df.index.get_loc(last_ftd)
    days_since_ftd = len(df) - 1 - ftd_pos
    return {
        'last_ftd_date': last_ftd.strftime('%Y-%m-%d'),
        'last_ftd_close_change_pct': round(float(df.loc[last_ftd, 'close_change_pct']), 2),
        'last_ftd_volume_ratio': round(float(df.loc[last_ftd, 'vol_ratio']), 2),
        'days_since_ftd': int(days_since_ftd),
    }


def infer_state(df, ftd_info, dd_count, rally_day_count):
    # TODO v2: 持久化 state machine 到 docs/screener/market_state_history/YYYY-MM-DD.json
    # 用過去 state 紀錄做精確 transition，而不是 inference
    close = float(df['Close'].iloc[-1])
    ma50 = df['ma50'].iloc[-1]
    ma200 = df['ma200'].iloc[-1]
    if pd.isna(ma50) or pd.isna(ma200):
        return 'rally_attempt'
    ma50_slope = float(df['ma50'].iloc[-1] - df['ma50'].iloc[-5])

    if close < ma200 and ma50_slope < 0:
        return 'correction'

    if close > ma200:
        if dd_count >= 6:
            return 'under_pressure'
        if ftd_info and ftd_info['days_since_ftd'] <= 30:
            return 'early_uptrend'
        if ftd_info and ftd_info['days_since_ftd'] > 30:
            return 'confirmed_uptrend'
        if rally_day_count is not None and rally_day_count <= 10:
            return 'rally_attempt'
        return 'confirmed_uptrend'

    if rally_day_count is not None and rally_day_count <= 10:
        return 'rally_attempt'
    return 'correction'


def state_since_proxy(df):
    """Heuristic for v1: date of last Close/MA200 crossing (either direction)."""
    valid = df.dropna(subset=['ma200'])
    if len(valid) == 0:
        return df.index[0].strftime('%Y-%m-%d')
    above = (valid['Close'] > valid['ma200']).astype(int)
    crossings = above.diff().abs()
    cross_dates = crossings[crossings > 0].index
    if len(cross_dates) == 0:
        return valid.index[0].strftime('%Y-%m-%d')
    return cross_dates[-1].strftime('%Y-%m-%d')


def trading_days_between(df, start_date_str):
    try:
        start = pd.Timestamp(start_date_str)
        pos = df.index.searchsorted(start)
        return max(0, len(df) - 1 - int(pos))
    except Exception:
        return 0


def build_index_payload(df):
    df = compute_indicators(df)
    close = float(df['Close'].iloc[-1])
    ma50_v = df['ma50'].iloc[-1]
    ma200_v = df['ma200'].iloc[-1]
    ma50 = float(ma50_v) if pd.notna(ma50_v) else None
    ma200 = float(ma200_v) if pd.notna(ma200_v) else None

    dd_count, dd_dates = detect_distribution_days(df)
    day1, rally_day = detect_rally_day1(df)
    ftd_info = detect_ftd(df, day1)
    state = infer_state(df, ftd_info, dd_count, rally_day)
    since = state_since_proxy(df)

    return {
        'state': state,
        'state_since': since,
        'days_in_state': trading_days_between(df, since),
        'close': round(close, 2),
        'vs_50dma_pct': round((close / ma50 - 1) * 100, 1) if ma50 else None,
        'vs_200dma_pct': round((close / ma200 - 1) * 100, 1) if ma200 else None,
        'ma50_above_200': bool(ma50 > ma200) if (ma50 is not None and ma200 is not None) else None,
        'ftd': ftd_info or {
            'last_ftd_date': None,
            'last_ftd_close_change_pct': None,
            'last_ftd_volume_ratio': None,
            'days_since_ftd': None,
        },
        'rally_attempt': {
            'in_progress': rally_day is not None and rally_day <= 10,
            'day1_date': day1.strftime('%Y-%m-%d') if day1 is not None else None,
            'current_rally_day': rally_day,
        },
        'distribution_days': {
            'count_25d': dd_count,
            'dates': dd_dates,
        },
    }


def dominant_regime(spy_state, qqq_state, iwm_state):
    ranks = [STATE_RANK[s] for s in [spy_state, qqq_state, iwm_state]]
    if spy_state == qqq_state == iwm_state:
        return spy_state, 'unanimous'
    if spy_state in ('confirmed_uptrend', 'early_uptrend') \
       and qqq_state in ('confirmed_uptrend', 'early_uptrend') \
       and iwm_state == 'rally_attempt':
        return 'confirmed_uptrend', 'narrow_leadership'
    states = [spy_state, qqq_state, iwm_state]
    min_state = states[ranks.index(min(ranks))]
    return min_state, 'mixed'


def main():
    print("=== Market Regime Engine ===")
    print(f"  Fetching {INDICES} 400d OHLCV ...")
    data = fetch_indices()

    indices_payload = {}
    for t in INDICES:
        indices_payload[t] = build_index_payload(data[t])
        s = indices_payload[t]
        print(f"  {t}: {s['state']:<18} since={s['state_since']}  "
              f"DD25={s['distribution_days']['count_25d']:>2}  "
              f"FTD={s['ftd']['last_ftd_date']}  "
              f"vs50={s['vs_50dma_pct']}  vs200={s['vs_200dma_pct']}")

    spy = indices_payload['SPY']
    qqq = indices_payload['QQQ']
    iwm = indices_payload['IWM']
    dom_state, agreement = dominant_regime(spy['state'], qqq['state'], iwm['state'])

    if agreement == 'unanimous':
        dom_since = max(spy['state_since'], qqq['state_since'], iwm['state_since'])
    elif agreement == 'narrow_leadership':
        dom_since = max(spy['state_since'], qqq['state_since'])
    else:
        dom_since = next((ix['state_since'] for ix in (spy, qqq, iwm)
                          if ix['state'] == dom_state),
                         max(spy['state_since'], qqq['state_since'], iwm['state_since']))

    days_in_dom = trading_days_between(data['SPY'], dom_since)
    rep = next((ix for ix in (spy, qqq, iwm) if ix['state'] == dom_state), spy)
    ctx = {
        'rally_day': rep['rally_attempt'].get('current_rally_day') or 0,
        'days_since_ftd': rep['ftd'].get('days_since_ftd') or 0,
        'days_in_state': days_in_dom,
        'dd_count': rep['distribution_days']['count_25d'],
    }
    advice_zh = ADVICE_MAP[dom_state]['zh'].format(**ctx)
    advice_en = ADVICE_MAP[dom_state]['en'].format(**ctx)

    data_date = data['SPY'].index[-1].strftime('%Y-%m-%d')
    payload = {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_date': data_date,
        'indices': indices_payload,
        'dominant': {
            'state': dom_state,
            'agreement': agreement,
            'started_at': dom_since,
            'days_in_state': days_in_dom,
            'advice_zh': advice_zh,
            'advice_en': advice_en,
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Dominant: {dom_state} ({agreement}) since {dom_since} ({days_in_dom} td)")
    print(f"  ✓ Output: {OUT_PATH}")


if __name__ == '__main__':
    main()
