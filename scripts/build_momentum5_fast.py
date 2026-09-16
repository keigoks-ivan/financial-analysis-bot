"""
Momentum-5 Fast builder — purely mechanical, fast-cadence momentum line,
feeds docs/research/momentum-5-fast/fast.json.

WHAT THIS IS
------------
A five-seat, equal-weight, fully mechanical paper portfolio combining two of
the Momentum-5 shadow-track's single-variable experiments (line F's 30-day
revision window, line H's 52-week-high proximity) into one score, rebalanced
every 28 calendar days. It reads ONLY docs/research/momentum-5/raw_factors.json
(the same weekly full-universe raw-factor dump build_momentum5.py already
writes, now including a 'sector' column added 2026-09-16) — no new download,
no new data source. It does NOT touch data.json, portfolio.json, shadow.json,
short.json, or anything in build_momentum5.py / build_momentum5_shadow.py /
build_momentum5_short.py.

There is no human judgment layer (same convention as Short): entries and
exits are both fully rule-driven. See PREREG below for the exact rules; it
is echoed verbatim into fast.json's "prereg" block and rendered on the page.
Unlike Short (per-seat holding-period + earnings-date exit triggers), Fast's
exit/rebalance logic operates on the WHOLE portfolio at once, on a fixed
28-day cadence — see REBALANCE below.

CANDIDATE POOL & SCORING
-------------------------
The "scored pool" (compute_scored_pool()) is EVERY ticker in this week's
universe that passes ALL of: above200, rev30_avg (mean of rev30_fy1/
rev30_fy2, BOTH required) > 0, ret12 <= VETO_RET12, px_over_52wh >=
PX52WH_MIN (0.90), growth not null. This set DELIBERATELY INCLUDES current
seat holders (unlike Short's pool, which excludes them) — Fast needs a
single "rank in the full population" number to decide whether a current
holder has fallen out of the top 10 (see REBALANCE below). Score = 0.5 *
z(rev30_avg, winsorized 5th/95th pct) + 0.3 * z(px_over_52wh, NOT
winsorized) + 0.2 * z(growth, winsorized 5th/95th pct), all z-scores
computed within the scored pool (ddof=0, std==0 -> that term is 0 for
everyone). Ties broken by ticker ascending. The ENTRY-eligible pool (used to
fill empty seats) is the scored pool with current holders filtered out.

REBALANCE (cadence + evict/fill, see main() for exact branching)
-----------------------------------------------------------------
Inception week is always a rebalance week. After that, a week is a
rebalance week whenever (as_of - last_rebalance_date).days >= 28; other
weeks only mark existing holdings to market. On a rebalance week:
  1. EVICT first: for each held seat, evict if EITHER (a) the ticker no
     longer passes the scored-pool's own base conditions (above200,
     rev30_avg>0, ret12<=2.5, px_over_52wh>=0.90, growth not null) — or is
     simply no longer present in this week's universe (delisted/dropped) —
     OR (b) its rank within the scored pool (which includes current
     holders) is > EXIT_RANK_MAX (10). The entry gate is "top of the scored
     pool with score-based fill order"; exit is deliberately tighter
     (top-10) than Short/main-line's looser exit gates, matching this
     line's faster, higher-turnover design.
  2. FILL second: empty seats (freshly evicted this run, or already empty
     from an earlier rebalance) are filled from the entry-eligible pool in
     score order, skipping any candidate whose GICS sector already holds
     SECTOR_CAP (2) seats (incumbents counted). An unfillable seat is left
     empty (cash), never force-filled.
A seat's sleeve settles at eviction exactly as in build_momentum5_short.py:
sleeve_at_entry * close/entry_price (or unchanged if this week's close is
unavailable) becomes the new sleeve_at_entry, i.e. it goes to cash and stays
there until refilled.

DATA GATES
-----------
  - rev30_coverage (count of tickers in this week's universe with BOTH
    rev30_fy1 and rev30_fy2 present) < MIN_REV30_COVERAGE (300): the real
    data gate — universe-wide revision data is too thin to trust this week,
    so on a rebalance week NEITHER evictions NOR fills run (holdings are
    only marked to market); this OVERRIDES the rebalance-day cadence check
    entirely (a rebalance day under this gate quietly waits until the next
    scheduled rebalance day, same as an ordinary non-rebalance week).
  - entry-eligible pool < MIN_ELIGIBLE (3) on a rebalance week: narrower
    rule, blocks ONLY the fill step (evictions still run — a fallen-out
    holder still exits even if there's nothing to replace it with).
  - raw_factors.json's as_of is NOT newer than fast.json's already-recorded
    as_of: idempotent no-op, exit without touching the file at all.

KNOWN WEAKNESSES: no backtest exists for this exact combined rule (see
PREREG.evidence — this is a forward-only registration, not a validated
strategy); no stop-loss; buying proximity to a 52-week high is inherently a
momentum-chasing entry with no margin-of-safety check; see
PREREG.known_weaknesses for the full list.

Runs in the weekly-market-update GitHub Actions workflow, after
build_momentum5.py / build_momentum5_shadow.py / build_momentum5_short.py —
wired by maintainer.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_FACTORS_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'raw_factors.json'
FAST_DIR = ROOT / 'docs' / 'research' / 'momentum-5-fast'
FAST_JSON = FAST_DIR / 'fast.json'

# ── frozen thresholds (PREREG'd 2026-09-16) ──
N_SEATS = 5
NAV_BASE = 100.0
SLEEVE_BASE = NAV_BASE / N_SEATS          # 20.0
REBALANCE_DAYS = 28                       # ~4 weeks
VETO_RET12 = 2.5                          # 12M return > +250% -> excluded (mirrors main line's veto)
PX52WH_MIN = 0.90                         # px_over_52wh < 0.90 -> excluded (mirrors main line's stalled flag)
MIN_ELIGIBLE = 3                          # data gate: entry-eligible pool floor (fill-blocking only)
MIN_REV30_COVERAGE = 300                  # data gate: universe-wide rev30 coverage floor (real gate)
WINSOR_LO, WINSOR_HI = 0.05, 0.95         # rev30_avg / growth winsorize quantiles (pool-internal)
SECTOR_CAP = 2                            # same GICS sector, incumbents included, max 2 seats
EXIT_RANK_MAX = 10                        # scored-pool rank (incl. current holders) > 10 -> evict

PREREG = {
    "title": "Momentum-5 Fast：三十天上修快線",
    "frozen_date": "2026-09-16",
    "objective": "檢定「30 天上修動能＋52 週高點接近度」合併後、搭配四週換手，能不能比 12 個月上修動能主線抓得更快。",
    "design": (
        "純機械操作，每週六用 Momentum-5 主線同一份原始資料跑五席等權組合，不做任何人工判斷。"
        "每 28 天重新檢查一次全池排名，候選池條件不再成立或排名跌出前 10 就出場，沒有停損。"
    ),
    "entry_rules": [
        "收盤價站上 200 日均線",
        "30 天 EPS 修正平均（rev30_fy1 與 rev30_fy2 平均）大於 0，兩者都要有值",
        "12 個月報酬不超過 250%（同 Momentum-5 主線的極端否決）",
        "收盤價距 52 週高點在 10% 以內（px_over_52wh ≥ 0.90）",
        "FY1→FY2 前瞻成長（growth）要有值",
        "不可為現任五席任一持股",
        "候選池不足 3 檔時，該次換手只不補位",
    ],
    "exit_rules": [
        "每 28 個日曆天重新檢查一次（成立當週起算）",
        "候選池條件（上述五項，不含「不可為現任」）任一不再成立即出場",
        "在當週全池（含現任）排名跌出前 10 即出場",
        "無停損——四週換手本身就是唯一的風險控管，刻意不加停損",
    ],
    "data_gates": [
        "全市場可算 30 天修正的檔數不到 300 檔：換手日當週不換手，現有持倉照最新收盤價 mark-to-market",
        "候選池（不含現任）不足 3 檔：只不補位，出場照常執行",
        "raw_factors.json 的資料日未比 fast.json 已記錄的更新：視為同一週，不重複處理",
    ],
    "scoring": "分數＝0.5×z(rev30_avg)＋0.3×z(px_over_52wh)＋0.2×z(growth)，rev30_avg 與 growth 先做 5/95 百分位 winsorize，z 分數在全池（含現任）內計算（ddof=0），同分以 ticker 字母序決勝。",
    "portfolio_rules": {
        "weighting": "等權五席，各占 NAV 20%",
        "nav_base": "100（成立當週）",
        "sleeve": "每席各自一個 sleeve，起始值 20；出場結算為現金，再進場時把現金投入新股",
        "no_stop": "無停損；出場只看候選池條件是否還成立、或排名是否跌出前 10",
    },
    "evidence": (
        "30 天修正窗與 52 週高點接近度各為影子 Line F／Line H 的單變數實驗（2026-08-20 起），"
        "本線是兩者合併＋四週換手的快線，尚無自有回測，屬前瞻登記"
    ),
    "known_weaknesses": [
        "沒有回測：這是前瞻登記，不是已驗證過的策略",
        "貼近 52 週高點本身就是追價，沒有安全邊際",
        "四週換手仍可能落後真正的動能轉折",
        "五席等權集中，單一持股占 NAV 20%",
        "無停損，中途下跌不會提前出場",
        "growth 只取單一分析師共識預估，本身可能不穩定",
        "同產業上限 2 席只降低、不能消除產業集中度",
    ],
    "disclosure": "紙上研究組合，機械式進出場，無交易成本，非投資建議。",
}


def z0(s):
    """z-score within s, ddof=0. std==0 (or NaN) -> all 0."""
    s = s.astype(float)
    std = s.std(ddof=0)
    if not std or pd.isna(std):
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / std


def winsorize(s, lo, hi):
    s = s.astype(float)
    if s.empty:
        return s
    lo_v, hi_v = s.quantile(lo), s.quantile(hi)
    return s.clip(lo_v, hi_v)


def load_raw_factors():
    raw = json.loads(RAW_FACTORS_JSON.read_text(encoding='utf-8'))
    df = pd.DataFrame(raw['universe']).set_index('ticker')
    return raw, df


def price_lookup(df, ticker):
    if ticker in df.index and pd.notna(df.at[ticker, 'price']):
        return float(df.at[ticker, 'price'])
    return None


def rev30_avg_of(df, ticker):
    """None unless BOTH rev30_fy1 and rev30_fy2 are present (mirrors
    build_momentum5_short.py's skipna=False convention)."""
    if ticker not in df.index:
        return None
    v1, v2 = df.at[ticker, 'rev30_fy1'], df.at[ticker, 'rev30_fy2']
    for v in (v1, v2):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return None
    return (float(v1) + float(v2)) / 2.0


def compute_scored_pool(df):
    """Every ticker (INCLUDING current seat holders) passing above200,
    rev30_avg>0, ret12<=VETO_RET12, px_over_52wh>=PX52WH_MIN, growth not
    null. Returns a DataFrame sorted by score desc, ticker asc, with a
    1-based 'rank' column, plus rev30_avg/score."""
    d = df.copy()
    d['rev30_avg'] = d[['rev30_fy1', 'rev30_fy2']].astype(float).mean(axis=1, skipna=False)
    mask = (
        (d['above200'] == True)  # noqa: E712 — safe against None/NaN
        & d['rev30_avg'].notna() & (d['rev30_avg'] > 0)
        & d['ret12'].notna() & (d['ret12'].astype(float) <= VETO_RET12)
        & d['px_over_52wh'].notna() & (d['px_over_52wh'].astype(float) >= PX52WH_MIN)
        & d['growth'].notna()
    )
    pool = d[mask].copy()
    if pool.empty:
        return pool
    pool['rev30_avg_w'] = winsorize(pool['rev30_avg'], WINSOR_LO, WINSOR_HI)
    pool['growth_w'] = winsorize(pool['growth'], WINSOR_LO, WINSOR_HI)
    pool['score'] = (0.5 * z0(pool['rev30_avg_w'])
                      + 0.3 * z0(pool['px_over_52wh'].astype(float))
                      + 0.2 * z0(pool['growth_w']))
    pool['_tkr_sort'] = pool.index
    pool = pool.sort_values(['score', '_tkr_sort'], ascending=[False, True])
    pool = pool.drop(columns=['_tkr_sort'])
    pool['rank'] = range(1, len(pool) + 1)
    return pool


def base_condition_reasons(df, ticker):
    """Reasons a currently-held ticker fails the scored pool's OWN base
    conditions (excludes the entry-only "not already a seat" rule, which
    doesn't apply when checking the seat's own incumbent). Empty list =
    still passes everything."""
    if ticker not in df.index:
        return ['不在本週名單（下市／剔除指數）']
    reasons = []
    if df.at[ticker, 'above200'] != True:  # noqa: E712 — value may be numpy.bool_, "is True" fails identity
        reasons.append('跌破 200 日線')
    rev30_avg = rev30_avg_of(df, ticker)
    if rev30_avg is None or rev30_avg <= 0:
        reasons.append('30D 修正≤0')
    ret12 = df.at[ticker, 'ret12']
    if ret12 is None or (isinstance(ret12, float) and pd.isna(ret12)) or float(ret12) > VETO_RET12:
        reasons.append('12M報酬>250%')
    px52 = df.at[ticker, 'px_over_52wh']
    if px52 is None or (isinstance(px52, float) and pd.isna(px52)) or float(px52) < PX52WH_MIN:
        reasons.append('距52週高點>10%')
    growth = df.at[ticker, 'growth']
    if growth is None or (isinstance(growth, float) and pd.isna(growth)):
        reasons.append('growth缺值')
    return reasons


def make_empty_seat(seat_no):
    return {
        'seat_no': seat_no,
        'ticker': None,
        'sector': None,
        'entry_date': None,
        'entry_price': None,
        'sleeve_at_entry': SLEEVE_BASE,
        'sleeve_value': SLEEVE_BASE,
        'last_price': None,
        'days_held': None,
    }


def process_evictions(state, df, scored_pool, as_of):
    rank_map = {}
    if not scored_pool.empty:
        rank_map = {t: int(r) for t, r in zip(scored_pool.index, scored_pool['rank'])}
    for seat in state['seats']:
        t = seat.get('ticker')
        if not t:
            continue
        reasons = base_condition_reasons(df, t)
        if not reasons:
            rank = rank_map.get(t)
            if rank is None or rank > EXIT_RANK_MAX:
                reasons = [f'全池排名>{EXIT_RANK_MAX}']
        if not reasons:
            continue
        p_now = price_lookup(df, t)
        if p_now is None:
            p_now = seat.get('last_price') or seat['entry_price']
        settled = round(seat['sleeve_at_entry'] * p_now / seat['entry_price'], 2)
        state['events'].append({
            'date': as_of, 'seat': seat['seat_no'], 'action': 'exit',
            'ticker': t, 'reason': '／'.join(reasons), 'price': round(p_now, 2),
        })
        seat.update({
            'ticker': None, 'sector': None, 'entry_date': None, 'entry_price': None,
            'sleeve_at_entry': settled, 'sleeve_value': settled,
            'last_price': None, 'days_held': None,
        })


def fill_seats(state, df, eligible_pool, as_of, sector_map, is_inception):
    empty_seats = [s for s in state['seats'] if s['ticker'] is None]
    if not empty_seats or eligible_pool is None or eligible_pool.empty:
        return []
    current_tickers = {s['ticker'] for s in state['seats'] if s['ticker']}
    sector_counts = {}
    for s in state['seats']:
        if s['ticker']:
            sec = s.get('sector') or sector_map.get(s['ticker'])
            if sec:
                sector_counts[sec] = sector_counts.get(sec, 0) + 1

    filled = []
    for seat in empty_seats:
        chosen = None
        for t in eligible_pool.index:
            if t in current_tickers:
                continue
            sec = sector_map.get(t)
            if sec and sector_counts.get(sec, 0) >= SECTOR_CAP:
                continue
            chosen = t
            break
        if chosen is None:
            continue  # no qualifying candidate left — leave this seat empty (cash)
        price = price_lookup(df, chosen)
        if price is None:
            continue
        sec = sector_map.get(chosen)
        seat['ticker'] = chosen
        seat['sector'] = sec
        seat['entry_date'] = as_of
        seat['entry_price'] = round(price, 2)
        seat['last_price'] = round(price, 2)
        seat['days_held'] = 0
        seat['sleeve_value'] = seat['sleeve_at_entry']  # ratio 1 at the moment of entry
        sector_counts[sec] = sector_counts.get(sec, 0) + 1
        current_tickers.add(chosen)
        filled.append({'ticker': chosen, 'sector': sec})
        state['events'].append({
            'date': as_of, 'seat': seat['seat_no'], 'action': 'enter',
            'ticker': chosen, 'reason': ('inception' if is_inception else 'rebalance_fill'),
            'price': round(price, 2),
        })
    return filled


def mark_to_market_all(state, df, as_of):
    as_of_ts = pd.Timestamp(as_of)
    for seat in state['seats']:
        t = seat.get('ticker')
        if not t:
            continue
        p_now = price_lookup(df, t)
        if p_now is None:
            p_now = seat.get('last_price') or seat['entry_price']
        else:
            seat['last_price'] = round(p_now, 2)
        seat['sleeve_value'] = round(seat['sleeve_at_entry'] * p_now / seat['entry_price'], 2)
        seat['days_held'] = (as_of_ts - pd.Timestamp(seat['entry_date'])).days


def main():
    try:
        raw, df = load_raw_factors()
    except Exception as e:
        print(f"  ✗ failed to load {RAW_FACTORS_JSON}: {type(e).__name__}: {e}")
        sys.exit(1)

    as_of = raw.get('as_of')
    spy_close = raw.get('spy_close')
    if as_of is None or spy_close is None:
        print("  ✗ raw_factors.json missing as_of / spy_close")
        sys.exit(1)

    is_inception = not FAST_JSON.exists()
    state = None
    if not is_inception:
        try:
            state = json.loads(FAST_JSON.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"  ✗ failed to parse existing {FAST_JSON}: {type(e).__name__}: {e}")
            sys.exit(1)
        if state.get('as_of') and as_of <= state['as_of']:
            print(f"  · raw_factors as_of={as_of} not newer than fast.json as_of={state['as_of']} "
                  f"— idempotent, no-op")
            return

    if state is None:
        print(f"  · no existing fast.json — building inception ({as_of})")
        state = {
            'schema': 'momentum5-fast-v1',
            'prereg': PREREG,
            'as_of': as_of,
            'inception': as_of,
            'spy_close_inception': float(spy_close),
            'last_rebalance_date': None,
            'seats': [make_empty_seat(i + 1) for i in range(N_SEATS)],
            'nav': [],
            'events': [],
            'candidates_top10': [],
            'data_gaps': [],
        }
    else:
        state['as_of'] = as_of
        state['prereg'] = PREREG  # keep prereg block byte-synced with the frozen spec above

    sector_map = df['sector'].to_dict() if 'sector' in df.columns else {}
    rev30_coverage = sum(1 for t in df.index if rev30_avg_of(df, t) is not None)
    scored_pool = compute_scored_pool(df)  # always computed — feeds candidates_top10 even off-cadence

    if rev30_coverage < MIN_REV30_COVERAGE:
        gate_reason = f"rev30_coverage<300（實際 {rev30_coverage}）"
        state['data_gaps'].append({'date': as_of, 'reason': gate_reason})
        print(f"  ! data gate tripped: {gate_reason} — 本次不換手，僅 mark-to-market")
    else:
        last_date = state.get('last_rebalance_date')
        if is_inception or last_date is None:
            is_rebalance, days_since = True, 0
        else:
            days_since = (pd.Timestamp(as_of) - pd.Timestamp(last_date)).days
            is_rebalance = days_since >= REBALANCE_DAYS

        if is_rebalance:
            process_evictions(state, df, scored_pool, as_of)
            current_tickers = {s['ticker'] for s in state['seats'] if s['ticker']}
            eligible_pool = (scored_pool[~scored_pool.index.isin(current_tickers)]
                              if not scored_pool.empty else scored_pool)
            if len(eligible_pool) < MIN_ELIGIBLE:
                gate_reason = f"eligible<3（候選池僅 {len(eligible_pool)} 檔）"
                state['data_gaps'].append({'date': as_of, 'reason': gate_reason})
                print(f"  ! {gate_reason} — 本次不補位（出場仍照常執行）")
            else:
                fill_seats(state, df, eligible_pool, as_of, sector_map, is_inception)
            state['last_rebalance_date'] = as_of
        else:
            print(f"  · not a rebalance week (last={last_date}, {days_since}d < {REBALANCE_DAYS}d) "
                  f"— mark-to-market only")

    mark_to_market_all(state, df, as_of)

    nav = round(sum(s['sleeve_value'] for s in state['seats']), 2)
    spy_nav = round(100.0 * float(spy_close) / state['spy_close_inception'], 2)
    state['nav'].append({'date': as_of, 'nav': nav, 'spy_nav': spy_nav})

    current_tickers_final = {s['ticker'] for s in state['seats'] if s['ticker']}
    top10 = []
    for t in scored_pool.head(10).index:
        row = scored_pool.loc[t]
        rev30_avg = row.get('rev30_avg')
        px52 = row.get('px_over_52wh')
        growth = row.get('growth')
        top10.append({
            'ticker': t,
            'sector': sector_map.get(t),
            'rev30_avg': round(float(rev30_avg), 1) if pd.notna(rev30_avg) else None,
            'px_over_52wh': round(float(px52), 4) if pd.notna(px52) else None,
            'growth': round(float(growth), 1) if pd.notna(growth) else None,
            'score': round(float(row['score']), 2),
            'is_seat': t in current_tickers_final,
        })
    state['candidates_top10'] = top10

    FAST_DIR.mkdir(parents=True, exist_ok=True)
    FAST_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {FAST_JSON.relative_to(ROOT)}  as_of={as_of}  NAV={nav}  SPY_NAV={spy_nav}  "
          f"rev30_coverage={rev30_coverage}  scored_pool={len(scored_pool)}")
    print("    seats: " + ", ".join(f"{s['seat_no']}:{s['ticker'] or 'cash'}" for s in state['seats']))
    if state['data_gaps'] and state['data_gaps'][-1]['date'] == as_of:
        print(f"    data_gap: {state['data_gaps'][-1]['reason']}")


if __name__ == '__main__':
    main()
