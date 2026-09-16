"""
Momentum-5 Short builder — purely mechanical PEAD (post-earnings-announcement
drift) paper track, feeds docs/research/momentum-5-short/short.json.

WHAT THIS IS
------------
A five-seat, equal-weight, fully mechanical paper portfolio that rides the
"financial-report-surprise then a slow 60-trading-day drift" hypothesis. It
reads ONLY docs/research/momentum-5/raw_factors.json (the same weekly
full-universe raw-factor dump build_momentum5.py already writes) — no new
download, no new data source. It does NOT touch data.json, portfolio.json,
shadow.json, or anything in build_momentum5.py / build_momentum5_shadow.py.

There is no human judgment layer here (unlike the main Momentum-5 portfolio):
entries and exits are both fully rule-driven. See PREREG below (mirrors the
frozen-spec convention build_momentum5_shadow.py uses) for the exact rules;
it is echoed verbatim into short.json's "prereg" block and rendered on the
page.

DATA GATES (see main() for the exact branching)
----------------------------------------------------------------------------
  - surprise_coverage OR report_date_coverage (both raw_factors.json's own
    fields) < SURPRISE_MIN_COVERAGE: the real "data gate" — universe-wide
    earnings data is too thin to trust this week, so NEITHER exits NOR fills
    run; existing holdings are only marked to market. An old raw_factors.json
    predating the report_date field (missing the key entirely) reads as
    report_date_coverage=0, which trips this gate.
  - eligible candidate pool < MIN_ELIGIBLE (3) this week: a narrower rule
    scoped to new entries only ("本週不進新席") — exits still run as normal
    (holding-period/new-earnings exits are per-seat mechanical triggers, and
    have nothing to do with how thin this week's candidate pool is), only
    fill_seats() is skipped.
  - raw_factors.json's as_of is NOT newer than short.json's already-recorded
    as_of: treated as idempotent (same week re-run) — the whole run is a
    no-op, exit 0, short.json is not touched at all (this is a stronger
    no-op than the two gates above, which still append a data_gap and a nav
    row for a genuinely new week with bad data).

CANDIDATE POOL & SCORING (see PREREG.entry_rules / PREREG.scoring for the
verbatim rule text)
----------------------------------------------------------------------------
Eligible this week = fresh positive earnings surprise AND rev30_avg (mean of
rev30_fy1/rev30_fy2, both required) > 0 AND above200 AND ret12 <=
VETO_RET12 AND not already a held seat. "Fresh" is anchored on report_date —
the ACTUAL announcement date from yfinance get_earnings_dates(), <=45
calendar days old — NOT surprise_date, which is earnings_history's
fiscal-period-END date (2026-09-16 fix: using the quarter-end as a proxy for
the report date squeezed the real post-announcement window down to 2-3
weeks and skewed the pool toward early reporters; see the bug's paper trail
in surprise_info()'s comment in build_momentum5.py). A ticker with no
report_date is simply ineligible (excluded, not treated as stale-but-ok).
Score = z(surprise_pct, winsorized to the pool's 5th/95th percentile) +
z(rev30_avg), both z-scores computed within the eligible pool (ddof=0,
std==0 -> that term is 0 for everyone). Ties broken by ticker ascending.
Because "not already a held seat" is one of the pool's defining conditions,
candidates_top10's is_seat field is trivially False for every row today —
kept in the schema for forward-compatibility / sanity, not because it
currently does anything.

SEAT / SLEEVE MECHANICS
------------------------
Five seats, each its own "sleeve" starting at nav_base/5 = 20. A seat holds
one ticker or sits empty (cash, value frozen at whatever it settled at on
exit). Exit triggers (either, checked BEFORE this week's rebalance, and only
when neither data gate above is tripped):
  (a) held >= HOLD_DAYS (84 calendar days, ~60 trading days) calendar days
      since entry_date;
  (b) the ticker's CURRENT report_date (real announcement date) is now newer
      than entry_report_date (the one recorded at entry) — i.e. it has
      reported a subsequent quarter. entry_surprise_date (fiscal-period-end)
      is still recorded on the seat as a reference field, but no longer
      drives this trigger.
There is NO stop-loss — deliberately, to match the backtest this line is
modeled on; see PREREG.known_weaknesses. On exit the sleeve settles to cash
at sleeve_at_entry * price_now/entry_price; on the next entry that same cash
figure becomes the new sleeve_at_entry (sleeves compound independently of
each other, mirroring build_momentum5_shadow.py's nav_base carry-forward).
Empty seats are refilled by score, one ticker per empty seat, until either
the seats are full or the eligible pool is exhausted.

Idempotent: re-running against an unchanged raw_factors.json (same as_of) is
a no-op (see DATA GATES above). Failure (missing/corrupt raw_factors.json)
prints an error, exits non-zero, and never touches an existing short.json.

Runs in the weekly-market-update GitHub Actions workflow, after
build_momentum5.py (and build_momentum5_shadow.py) — wired by maintainer.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_FACTORS_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'raw_factors.json'
SHORT_DIR = ROOT / 'docs' / 'research' / 'momentum-5-short'
SHORT_JSON = SHORT_DIR / 'short.json'

# ── frozen thresholds (PREREG'd 2026-09-16) ──
N_SEATS = 5
NAV_BASE = 100.0
SLEEVE_BASE = NAV_BASE / N_SEATS          # 20.0
HOLD_DAYS = 84                            # ~60 trading days
SURPRISE_FRESH_DAYS = 45                  # candidate pool freshness gate
SURPRISE_MIN_COVERAGE = 300               # data gate: universe-wide surprise coverage floor
MIN_ELIGIBLE = 3                          # data gate: candidate pool floor
VETO_RET12 = 2.5                          # 12M return > +250% -> excluded (mirrors main line's veto)
WINSOR_LO, WINSOR_HI = 0.05, 0.95         # surprise_pct winsorize quantiles (pool-internal)

PREREG = {
    "title": "Momentum-5 Short：財報後六十日驚喜漂移機械線",
    "frozen_date": "2026-09-16",
    "objective": "檢定財報驚喜後的股價反應能不能在六十個交易日內持續產生超額報酬。",
    "design": (
        "純機械操作，每週六用 Momentum-5 主線同一份原始資料跑五席等權組合，不做任何人工判斷。"
        "進場看財報驚喜與 30 天修正動能，出場只看持有天數與下一次財報，沒有停損。"
    ),
    "entry_rules": [
        "財報公布日（yfinance get_earnings_dates 的實際公布日，非季底日）距本週資料截止日在 45 個日曆天內，且財報驚喜（surprise_pct）大於 0",
        "30 天 EPS 修正平均（rev30_fy1 與 rev30_fy2 平均）大於 0，兩者都要有值",
        "收盤價站上 200 日均線",
        "12 個月報酬不超過 250%（同 Momentum-5 主線的極端否決）",
        "不可為現任五席任一持股",
        "候選池不足 3 檔時，本週不進新席",
    ],
    "exit_rules": [
        "進場滿 84 個日曆天（約 60 個交易日）強制出場",
        "該股公布下一次財報（以實際公布日 report_date 判斷）即出場",
        "無停損——刻意設計，為了跟回測條件一致",
    ],
    "data_gates": [
        "全市場財報驚喜覆蓋不到 300 檔：本週不換倉，現有持倉照最新收盤價 mark-to-market",
        "全市場財報公布日覆蓋不到 300 檔：與驚喜覆蓋閘同等處理，本週不換倉，只 mark-to-market",
        "raw_factors.json 的資料日未比 short.json 已記錄的更新：視為同一週，不重複處理",
    ],
    "scoring": "分數＝驚喜幅度的 z 分數（候選池內先做 5/95 百分位 winsorize）加上 30 天修正平均的 z 分數，同分以 ticker 字母序決勝。",
    "portfolio_rules": {
        "weighting": "等權五席，各占 NAV 20%",
        "nav_base": "100（成立當週）",
        "sleeve": "每席各自一個 sleeve，起始值 20；出場結算為現金，再進場時把現金投入新股",
        "no_stop": "無停損；出場只看持有天數到期或下一次財報公布，不看虧損幅度",
    },
    "evidence": (
        "持有人自有回測（v7-backtest pead_backtest，SEC EDGAR SUE，2009–2026）："
        "最高驚喜五分位 60 日事件累積超額 +0.66%，t 值 3.7；效果統計上存在但幅度小"
    ),
    "known_weaknesses": [
        "效果本身很小：自有回測最高驚喜五分位的 60 日累積超額只有 +0.66%",
        "yfinance 的 surprisePercent 不是學術定義的 SUE（標準化未預期盈餘），只是實際數字對預估數字的粗略比例",
        "五席等權集中，單一持股占 NAV 20%",
        "無停損，中途下跌不會提前出場",
        "分析師修正資料本身有 2-6 週滯後",
        "驚喜%在預估值很小時容易失真，已用 winsorize 5/95 處理極端值",
        "沒有公布日（report_date）資料的股票會直接被排除出候選池，不是記為不新鮮",
    ],
    "disclosure": "紙上研究組合，機械式進出場，無交易成本，非投資建議。",
}


def z0(s):
    """z-score within s, ddof=0. std==0 (or NaN, e.g. a 0/1-row pool) -> all 0."""
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


def surprise_date_lookup(df, ticker):
    if ticker not in df.index:
        return None
    v = df.at[ticker, 'surprise_date']
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    return str(v)


def report_date_lookup(df, ticker):
    """The real announcement date (see build_momentum5.py's surprise_info()),
    distinct from surprise_date_lookup()'s fiscal-period-end date. Column may
    be entirely absent on an old raw_factors.json predating this field —
    guarded the same way price_lookup/surprise_date_lookup guard on ticker
    absence."""
    if 'report_date' not in df.columns or ticker not in df.index:
        return None
    v = df.at[ticker, 'report_date']
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    return str(v)


def compute_eligible_pool(df, as_of, exclude_tickers):
    """This week's candidate pool: fresh positive surprise (freshness anchored
    on report_date, the actual announcement date — NOT surprise_date, which is
    the fiscal-period-end date; see module docstring's 2026-09-16 fix note),
    rev30_avg>0 (both fy1/fy2 present), above200, ret12<=VETO_RET12, not
    already a held seat. Returns a DataFrame sorted by score desc, ticker
    asc, with columns surprise_pct, rev30_avg, score (plus the original raw
    columns)."""
    as_of_ts = pd.Timestamp(as_of)
    d = df.copy()
    d['rev30_avg'] = d[['rev30_fy1', 'rev30_fy2']].astype(float).mean(axis=1, skipna=False)

    def fresh(row):
        sp = row.get('surprise_pct')
        if sp is None or pd.isna(sp) or sp <= 0:
            return False
        rd = row.get('report_date')
        if rd is None or (isinstance(rd, float) and pd.isna(rd)):
            return False  # no report_date -> ineligible, not "stale but ok"
        try:
            age = (as_of_ts - pd.Timestamp(rd)).days
        except (ValueError, TypeError):
            return False
        return 0 <= age <= SURPRISE_FRESH_DAYS

    d['_fresh'] = d.apply(fresh, axis=1)
    mask = (
        d['_fresh']
        & d['rev30_avg'].notna() & (d['rev30_avg'] > 0)
        & (d['above200'] == True)  # noqa: E712 — safe against None/NaN, unlike .astype(bool)
        & d['ret12'].notna() & (d['ret12'].astype(float) <= VETO_RET12)
        & (~d.index.isin(exclude_tickers))
    )
    pool = d[mask].copy()
    if pool.empty:
        return pool
    pool['surprise_pct_w'] = winsorize(pool['surprise_pct'], WINSOR_LO, WINSOR_HI)
    pool['score'] = z0(pool['surprise_pct_w']) + z0(pool['rev30_avg'])
    pool['_tkr_sort'] = pool.index
    pool = pool.sort_values(['score', '_tkr_sort'], ascending=[False, True])
    return pool.drop(columns=['_fresh', '_tkr_sort'])


def make_empty_seat(seat_no):
    return {
        'seat_no': seat_no,
        'ticker': None,
        'entry_date': None,
        'entry_price': None,
        'entry_surprise_date': None,
        'entry_report_date': None,
        'entry_surprise_pct': None,
        'entry_rev30_avg': None,
        'entry_score': None,
        'sleeve_at_entry': SLEEVE_BASE,
        'sleeve_value': SLEEVE_BASE,
        'last_price': None,
        'days_held': None,
        'exit_due_date': None,
    }


def process_exits(state, df, as_of):
    as_of_ts = pd.Timestamp(as_of)
    for seat in state['seats']:
        t = seat.get('ticker')
        if not t:
            continue
        held_days = (as_of_ts - pd.Timestamp(seat['entry_date'])).days
        reason = None
        if held_days >= HOLD_DAYS:
            reason = 'holding_period'
        else:
            # exit trigger (b): compare the REAL announcement date, not the
            # fiscal-period-end date (2026-09-16 fix — see module docstring).
            cur_rd = report_date_lookup(df, t)
            if cur_rd and seat.get('entry_report_date') and cur_rd > seat['entry_report_date']:
                reason = 'new_earnings'
        if not reason:
            continue
        p_now = price_lookup(df, t)
        if p_now is None:
            p_now = seat.get('last_price') or seat['entry_price']
        settled = round(seat['sleeve_at_entry'] * p_now / seat['entry_price'], 2)
        state['events'].append({
            'date': as_of, 'seat': seat['seat_no'], 'action': 'exit',
            'ticker': t, 'reason': reason, 'price': round(p_now, 2),
        })
        seat.update({
            'ticker': None, 'entry_date': None, 'entry_price': None,
            'entry_surprise_date': None, 'entry_report_date': None, 'entry_surprise_pct': None,
            'entry_rev30_avg': None, 'entry_score': None,
            'sleeve_at_entry': settled, 'sleeve_value': settled,
            'last_price': None, 'days_held': None, 'exit_due_date': None,
        })


def fill_seats(state, df, pool, as_of, is_inception):
    empty_seats = [s for s in state['seats'] if s['ticker'] is None]
    if not empty_seats or pool is None or pool.empty:
        return
    for seat, ticker in zip(empty_seats, pool.index):
        price = price_lookup(df, ticker)
        if price is None:
            continue
        row = pool.loc[ticker]
        seat['ticker'] = ticker
        seat['entry_date'] = as_of
        seat['entry_price'] = round(price, 2)
        seat['entry_surprise_date'] = surprise_date_lookup(df, ticker)  # reference only, not the exit trigger
        seat['entry_report_date'] = report_date_lookup(df, ticker)  # drives exit trigger (b)
        sp = row.get('surprise_pct')
        seat['entry_surprise_pct'] = round(float(sp), 1) if pd.notna(sp) else None
        ra = row.get('rev30_avg')
        seat['entry_rev30_avg'] = round(float(ra), 1) if pd.notna(ra) else None
        seat['entry_score'] = round(float(row['score']), 2)
        seat['sleeve_at_entry'] = seat['sleeve_value']  # carry forward the cash this sleeve held
        seat['sleeve_value'] = seat['sleeve_at_entry']  # ratio 1 at the moment of entry
        seat['last_price'] = round(price, 2)
        seat['days_held'] = 0
        seat['exit_due_date'] = (pd.Timestamp(as_of) + pd.Timedelta(days=HOLD_DAYS)).date().isoformat()
        state['events'].append({
            'date': as_of, 'seat': seat['seat_no'], 'action': 'enter',
            'ticker': ticker, 'reason': ('inception' if is_inception else 'fill'),
            'price': round(price, 2),
        })


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
    surprise_coverage = raw.get('surprise_coverage')
    if as_of is None or spy_close is None or surprise_coverage is None:
        print("  ✗ raw_factors.json missing as_of / spy_close / surprise_coverage")
        sys.exit(1)
    # report_date_coverage is a newer field (2026-09-16 fix) — an old
    # raw_factors.json predating it is missing the key entirely, which reads
    # as 0 and trips the data gate below (not a hard failure of this script).
    report_date_coverage = raw.get('report_date_coverage')
    if report_date_coverage is None:
        report_date_coverage = 0

    is_inception = not SHORT_JSON.exists()
    state = None
    if not is_inception:
        try:
            state = json.loads(SHORT_JSON.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"  ✗ failed to parse existing {SHORT_JSON}: {type(e).__name__}: {e}")
            sys.exit(1)
        if state.get('as_of') and as_of <= state['as_of']:
            print(f"  · raw_factors as_of={as_of} not newer than short.json as_of={state['as_of']} "
                  f"— idempotent, no-op")
            return

    if state is None:
        print(f"  · no existing short.json — building inception ({as_of})")
        state = {
            'schema': 'momentum5-short-v1',
            'prereg': PREREG,
            'as_of': as_of,
            'inception': as_of,
            'spy_close_inception': float(spy_close),
            'seats': [make_empty_seat(i + 1) for i in range(N_SEATS)],
            'nav': [],
            'events': [],
            'candidates_top10': [],
            'data_gaps': [],
        }
    else:
        state['as_of'] = as_of
        state['prereg'] = PREREG  # keep prereg block byte-synced with the frozen spec above

    current_tickers = {s['ticker'] for s in state['seats'] if s['ticker']}
    pool = compute_eligible_pool(df, as_of, current_tickers)

    # coverage<300 (surprise OR report_date) is the real "data gate":
    # universe-wide earnings data is too thin to trust this week, so we don't
    # touch positions at all (no exits, no fills) — only mark-to-market.
    # eligible<3 is a NARROWER rule scoped to the candidate pool only: it
    # blocks new entries ("本週不進新席") but must NOT block exits, since
    # holding-period/new-earnings exits are per-seat mechanical triggers
    # independent of how thin this week's candidate pool is (see
    # build_momentum5_short.py docstring / PREREG.entry_rules).
    gate_reasons = []
    if surprise_coverage < SURPRISE_MIN_COVERAGE:
        gate_reasons.append(f"surprise_coverage<300（實際 {surprise_coverage}）")
    if report_date_coverage < SURPRISE_MIN_COVERAGE:
        gate_reasons.append(f"report_date_coverage<300（實際 {report_date_coverage}）")

    if gate_reasons:
        gate_reason = "；".join(gate_reasons)
        state['data_gaps'].append({'date': as_of, 'reason': gate_reason})
        print(f"  ! data gate tripped: {gate_reason} — 本週不換倉，僅 mark-to-market")
    else:
        process_exits(state, df, as_of)
        if len(pool) < MIN_ELIGIBLE:
            gate_reason = f"eligible<3（候選池僅 {len(pool)} 檔）"
            state['data_gaps'].append({'date': as_of, 'reason': gate_reason})
            print(f"  ! {gate_reason} — 本週不進新席（出場仍照常執行）")
        else:
            fill_seats(state, df, pool, as_of, is_inception)

    mark_to_market_all(state, df, as_of)

    nav = round(sum(s['sleeve_value'] for s in state['seats']), 2)
    spy_nav = round(100.0 * float(spy_close) / state['spy_close_inception'], 2)
    state['nav'].append({'date': as_of, 'nav': nav, 'spy_nav': spy_nav})

    top10 = []
    for t in pool.head(10).index:
        row = pool.loc[t]
        sp = row.get('surprise_pct')
        ra = row.get('rev30_avg')
        top10.append({
            'ticker': t,
            'surprise_pct': round(float(sp), 1) if pd.notna(sp) else None,
            'surprise_date': surprise_date_lookup(df, t),
            'report_date': report_date_lookup(df, t),
            'rev30_avg': round(float(ra), 1) if pd.notna(ra) else None,
            'score': round(float(row['score']), 2),
            'is_seat': t in current_tickers,
        })
    state['candidates_top10'] = top10

    SHORT_DIR.mkdir(parents=True, exist_ok=True)
    SHORT_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {SHORT_JSON.relative_to(ROOT)}  as_of={as_of}  NAV={nav}  SPY_NAV={spy_nav}")
    print("    seats: " + ", ".join(f"{s['seat_no']}:{s['ticker'] or 'cash'}" for s in state['seats']))
    if state['data_gaps'] and state['data_gaps'][-1]['date'] == as_of:
        print(f"    data_gap: {state['data_gaps'][-1]['reason']}")


if __name__ == '__main__':
    main()
