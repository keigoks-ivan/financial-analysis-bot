"""
台股核心席 — docs/cockpit-tw/data/ (2026-10-10).

Same seat rules as the US engine (scripts/engine/build_arena.py v5.2), run on
the TW Koyfin pool (docs/dd-screener/tw/latest.json). grp.py and build_arena.py
are imported as libraries and not modified: the owner decided on 2026-09-02 that
TW is a separate system, and the US engine excludes .TW. Every row goes through
build_arena.row_dict() / _flat_view() and the US table renderer, so the gates,
the timing lamp and the columns stay identical to the US table.

Owner decisions 2026-10-09/10 (knowledge/rule_ledger.md「台股核心席」):
  1. Growth gate: the US three-year Koyfin rule (FY1→FY3 CAGR >= 15% with the
     base-effect correction), not the TW pool's FY1→FY2 criterion.
  2. Quality gate: operating-cash-flow margin in place of FCF margin, same
     thresholds (TW pool CASH_BASIS decision: capex-heavy names).
  3. No market-cap gate beyond the pool's own US$1B floor.
  4. (Superseded by v5.7, see below.) Seats needed revision >= +5% like the US pool.

Owner decision 2026-10-18 (v5.3, same day as the US board): yellow lamp sizing
0.5 -> 1.0, so 綠 1.0 / 黃 1.0 / 橘 0.5 / 紅 0 / 不合格 0. Basis: v7-backtest
docs/SeatSizing_Results_TW_Small.md (c61b63b), classified 「無法分辨」 — registered
criterion 4 (crash-window drawdown) not passed — so this is the owner's informed
choice, not a registered pass. tw_row() passes yellow_full=True to row_dict().

Owner decision 2026-10-18 (v5.4, TW seats page only): 看大盤切換出場 (X1). Registered in
v7-backtest docs/SeatExitSwitch_Prereg.md (e26888d); the registered conclusion is
「現行維持」 (US small/mid caps failed), TW passed all four criteria, and the owner decided
to switch the TW seats page only — an exception, not a registered pass.
  - Market state at the decision day: TWSE total-return index close < its 200-day simple
    average = 大盤空頭; otherwise (equal included) 大盤多頭. Source: data/macro_db/series/
    tw.twse_tri.csv (TWSE TAIEX/MFI94U, identical to the backtest's index_tr.parquet on all
    4,353 overlapping days). Latest row not later than the decision day; older than 7
    calendar days (or missing) → that week falls back to the current exit.
  - 大盤多頭 (bull): an incumbent leaves only when its close < its own 200-day line or it is no longer
    eligible/in the pool; a drop of more than 10% from the high does not remove it.
    大盤空頭 (bear): the current red-lamp exit. Entry, ranking, sizing are unchanged.
  - A held name that is red only by distance keeps the sizing coefficient of its last non-red
    day (backtest rule), kept in docs/cockpit-tw/data/seats_tw_state.json (written on every
    run). Missing entry → 1.0 and a log line.
  - The exit is judged where the roster is re-selected (--ledger, Saturday, Friday close).
    Daily runs use the market state of the last Saturday's decision day.

Owner decision 2026-10-21 (v5.6, TW seats page only): 大盤跌破 200 日線不買新股. Registered in
v7-backtest docs/SeatEntryGate_Prereg.md (fafc772); the registered conclusion is 「現行維持」 (US
small/mid caps failed on the fixed data: five seats better, hold-all worse), TW passed all four
criteria (X1N vs X1, 999/1000 seeds, also at matched exposure, independent recompute 5.9e-11),
and the owner decided to switch the TW seats page only — an exception, not a registered pass.
  - Same market state as v5.4. In a 大盤空頭 week (status 'bear', i.e. computed from fresh data)
    the Saturday re-selection adds no new names: empty seats stay empty (cash). Incumbents leave
    only when out of the pool or red (the bear-week exit); being out-ranked by a new name does not
    remove them, because that swap would be a buy. Sizing changes of held names are unchanged.
  - Stale or missing market data does not block buying (falls back to the v5.4 behaviour).
  - The names that would have been added are kept as rotation['blocked'] for display.

Owner decision 2026-10-21 (v5.7, TW seats page only, third item of the same day): 拿掉「上修 ≥5% 才進池」.
Not a registered pass — an exception: the v7-backtest TW rule (docs/SeatFullGrid_Results.md) never had a
revision threshold (TW has no historical estimates), nor the valuation gate or the three-year growth gate.
  - Pool = every name that passes all eligibility gates (grp.pass, valuation gate included; names red
    only on valuation stay in 「③b 太貴不入池」). Revision is a sort key only (grp.pool_sort_key, the
    existing pool order). The US board and the ten-bagger page dropped the same threshold later that day (fourth item), so grp.in_pool() / POOL_REV_MIN now have no callers.
  - Everything else is unchanged: the lamp-lit top 5, X1 exit, bear-week no-buy, yellow full size,
    Saturday re-selection. Reason for the change: 30 names passed eligibility but the highest revision
    was +2.6%, so the seats had been empty since 2026-10-09.
  - Why the sections 「④ 候補」「⑤ 其他過關」 are gone: both only existed for names outside the +5% pool.

Owner decision 2026-10-21 (v5.8, TW seats page only): 每月依波動分配每席大小. (Superseded by v5.9, see below.)
Registered in v7-backtest docs/SeatRebal_Prereg.md (f6d7dfd), results docs/SeatRebal_Results.md (2c8aaca,
owner decision 6b78bfb). Rule R2 passed all six criteria on TW (750/1000 seeds, median Calmar 0.799 -> 0.872,
CAGR 24.3% -> 22.9%, max drawdown -30.6% -> -26.2%); US small/mid caps missed one (second-half Calmar), so the
registered conclusion is 「單一市場」 and switching the TW page was the owner's exception, like v5.4 / v5.6.
  - Each incumbent's weight was set once a month by inverse 60-day volatility (sum equal to equal weight),
    new names used 1/5 until the next rebalance day, and a mail / Discord alert went out on that day.
    The code for this (seat_weights, update_vol_rebal, tw_seats_rebal_alert.txt, state key 'vol_rebal',
    the 「本月占比」 column) was removed in v5.9; see commit b8595de8f for the v5.8 implementation.

Owner decision 2026-10-23 (v5.9, TW seats page only): 拿掉 v5.8 的每月依波動分配，恢復每檔等權 (1/5 each,
lamp size on top: 綠 1.0 / 黃 1.0 / 橘 0.5 / 紅 0), i.e. back to the v5.7 sizing. This is the owner's decision,
not a test conclusion. Basis he looked at: the one-year replay (2025-10-22 flat -> 2026-10-22, the same 10
entries and exits) gives +29.6% / max drawdown -33.6% with the volatility allocation and +39.8% / -34.0% with
equal weight (0050: +74.0%); the 2010-2026 test (v7 docs/SeatRebal_Results.md, 1,000 seeds) says the volatility
allocation costs 1.4 points of CAGR for Calmar 0.80 -> 0.87. Registered in knowledge/rule_ledger.md (v5.9 row).
  - The old state key 'vol_rebal' in seats_tw_state.json is no longer read; the next run rewrites the file
    with only schema_version and last_nonred.

TW pool has no short-interest data, so that US gate never fires; insider
buying (a display chip in the US) is almost always empty. 下次財報 falls back to the
statutory filing deadline when yfinance has no date.

Seats are re-selected only with --ledger (the Saturday Taipei run, Friday
close). Other runs keep the stored roster and refresh lamps only — the same
split as the US engine.

Outputs:
  docs/cockpit-tw/data/_seats_tw_body.html  board fragment for cockpit-tw 席位排序
  docs/cockpit-tw/data/seats_tw.json        seats / pool / candidates / board as data
  docs/cockpit-tw/data/seats_tw_ledger.json roster state + weekly snapshots

Usage:
  python3 scripts/build_seats_tw.py            # daily: lamps only
  python3 scripts/build_seats_tw.py --ledger   # Saturday: re-select seats
"""

import argparse
import copy
import csv
import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from engine import build_arena as ba  # noqa: E402
from engine import grp  # noqa: E402
from engine import seat_st  # noqa: E402
from engine import seat_valhold  # noqa: E402
from engine import rulecard  # noqa: E402
import tw_filing_calendar  # noqa: E402

TW_POOL_JSON = ROOT / 'docs' / 'dd-screener' / 'tw' / 'latest.json'
LAMP_TW_JSON = ROOT / 'docs' / 'stages' / 'data' / 'lamp_tw.json'
OUT_DIR = ROOT / 'docs' / 'cockpit-tw' / 'data'
BODY_HTML = OUT_DIR / '_seats_tw_body.html'
SEATS_JSON = OUT_DIR / 'seats_tw.json'
LEDGER_JSON = OUT_DIR / 'seats_tw_ledger.json'
ST_NAV_JSON = OUT_DIR / 'seat_st_nav_tw.json'   # 新舊規則名單的每週淨值（退回條件用，只在 --ledger 週跑追加）
ST_STATE_JSON = OUT_DIR / 'seat_st_state_tw.json'   # 2026-11-05 折衷組：買進日／切換狀態（engine/seat_st.py）
ST_HYPO_JSON = OUT_DIR / 'seat_st_hypo_tw.json'   # 第三條對照線：假設折衷組從 2024-01-02 起一直在跑（只在週六重選時更新）
ST_HYPO_SEED_JSON = OUT_DIR / 'seat_st_hypo_seed_tw.json'   # 該線的種子（一次性回放結果，不改）
VALHOLD_JSON = OUT_DIR / 'seat_valhold_state_tw.json'   # 2026-11-05 估值偏貴現任續抱：轉紅前最後一次的倉位（三條線各一份，見 engine/seat_valhold.py）
STATE_NAME = 'seats_tw_state.json'     # path resolved from OUT_DIR at run time (see _state_path)
MARKET_CSV = ROOT / 'data' / 'macro_db' / 'series' / 'tw.twse_tri.csv'   # 發行量加權股價報酬指數
MKT_MA = 200            # 大盤均線天數（登記 SeatExitSwitch_Prereg.md 第三節）
MKT_STALE_DAYS = 7      # 最近一筆比決策日早超過這麼多日曆天＝大盤資料未更新，該週退回現行賣法
X1_DEFAULT_SIZE = 1.0   # 狀態檔缺這檔的最近非紅燈倉位時的預設

TPE = timezone(timedelta(hours=8))
CORE_SLOTS = ba.CORE_SLOTS
# 證券交易法第 36 條：年報 3/31、第一季 5/15、第二季 8/14、第三季 11/14。
TW_DEADLINES = tw_filing_calendar.DEADLINES


def _warn(msg):
    print(f"::warning::seats-tw: {msg}")


def tw_row(s0):
    """One TW pool stock → the US row_dict() shape, quality gate on OCF margin."""
    s = copy.deepcopy(s0)
    s['fcf'] = s.get('ocf')
    # v5.5 (2026-10-18): US board / ten-bagger page moved to FCF > 0; this page keeps the
    # original rule (OCF margin >= 10%, or ROIC >= 25% and OCF >= 0).
    s[grp.QUALITY_RULE_KEY] = grp.Q_RULE_MARGIN10
    r = ba.row_dict(s, yellow_full=True)   # v5.3 (2026-10-18): yellow lamp = full size
    r['name'] = s0.get('name')
    g = r['grp'] = dict(r['grp'])
    g['why'] = [w.replace('品質閘 FCF', '品質閘 營業現金流利潤率') for w in g.get('why') or []]
    # v5.4: 跌破自己的 200 日線？（缺值不算跌破，同 grp.timing_lamp 的 vs200 判斷）
    vs200 = grp._f((s0.get('timing') or {}).get('vs_200ma_pct'))
    r['_below200'] = vs200 is not None and vs200 < 0
    return r


# ── 看大盤切換出場（v5.4，2026-10-18，SeatExitSwitch X1）────────────────────

def load_market_series(path=None):
    """tw.twse_tri.csv → [(date, close)]，依日期升冪。檔案缺或壞掉回傳 []（呼叫端視為資料缺）。"""
    out = []
    try:
        with open(path or MARKET_CSV, encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                try:
                    out.append((date.fromisoformat(row['date'][:10]), float(row['value'])))
                except (KeyError, ValueError, TypeError):
                    continue
    except OSError:
        return []
    out.sort(key=lambda x: x[0])
    return out


def market_state(series, decision_date):
    """決策日的大盤狀態（純函式）。

    取最近一筆「不晚於決策日」的加權報酬指數收盤；收盤嚴格小於該筆往前連續 200 列的簡單平均＝空頭，
    其餘（含恰好相等、均線不足 200 列）＝多頭（登記：缺值時比較為假，歸多頭）。
    mode 'x1'＝看大盤切換出場（多頭）；'e1'＝現行賣法（空頭，或資料缺／太舊而退回）。
    最近一筆比決策日早超過 MKT_STALE_DAYS 個日曆天、或沒有任何不晚於決策日的資料＝退回現行賣法。"""
    dd = decision_date if isinstance(decision_date, date) else date.fromisoformat(str(decision_date)[:10])
    res = {'mode': 'e1', 'status': 'missing', 'decision_date': dd.isoformat(),
           'data_date': None, 'close': None, 'ma200': None}
    i = max((k for k, (d, _) in enumerate(series) if d <= dd), default=None)
    if i is None:
        return res
    d, close = series[i]
    res.update(data_date=d.isoformat(), close=close)
    if (dd - d).days > MKT_STALE_DAYS:
        res['status'] = 'stale'
        return res
    if i + 1 >= MKT_MA:
        ma = math.fsum(v for _, v in series[i + 1 - MKT_MA:i + 1]) / MKT_MA
        res['ma200'] = ma
        bear = close < ma
    else:
        bear = False
    res['status'] = 'bear' if bear else 'bull'
    res['mode'] = 'e1' if bear else 'x1'
    return res


# ── 大盤空頭不買新股（v5.6，2026-10-21，SeatEntryGate N）──────────────────────

def bear_no_buy(rotation, pool, prev_core):
    """大盤空頭週不買新股（純函式）。rotation＝select_hold_roster 的結果，pool 依池序排好。
    新進者全部取消、空席留空；在席者只在出池或時機燈轉紅時離席，不因排序被新名字擠出（擠出要買新名字）。
    回傳格式同 select_hold_roster，另加 blocked＝本來會補進的名字。"""
    prev = set(prev_core or [])
    core = [r['ticker'] for r in pool if r['ticker'] in prev and _lit(r)][:CORE_SLOTS]
    return {'core': core, 'rotated': False,
            'removed': [x for x in rotation['removed'] if x[0] not in core],
            'filled': [], 'blocked': [t for _, t in rotation['filled']]}


def x1_market(market):
    return bool(market) and market.get('mode') == 'x1'


def _x1_dist_only(r):
    """紅燈只因距新高 < −10%（沒跌破自己的 200 日線）。"""
    return (r.get('lamp') or {}).get('code') == 'red' and not r.get('_below200')


def _as_lit(r):
    """選席用的副本：把大盤多頭時留任的紅燈在席者當作亮燈。不改原列。"""
    return dict(r, lamp=dict(r['lamp'], code='yellow'))


def apply_x1_hold(sel, state, log=print):
    """大盤多頭續抱的席位：燈號維持紅，倉位改用「最近一次非紅燈的倉位」（回測規則）。
    state＝{ticker: {'size': ...}}；缺值用 X1_DEFAULT_SIZE 並印一行。"""
    for r in sel['core']:
        if not r.get('x1_hold'):
            continue
        t = r['ticker']
        size = (state.get(t) or {}).get('size')
        if size is None:
            size = X1_DEFAULT_SIZE
            log(f"  ! seats-tw: {t} 狀態檔沒有最近非紅燈倉位，續抱倉位用 {X1_DEFAULT_SIZE}")
        lamp = dict(r['lamp'])
        why = lamp.get('why') or ''
        lamp.update(label='🔴 續抱', size=size, trigger=None,
                    why=f"大盤多頭，只在跌破自己的 200 日線才賣；倉位沿用最近一次非紅燈的倉位 {size}｜{why}")
        r['lamp'] = lamp
        r['action'] = ('正常倉' if size >= 1.0 else '半倉') + '・續抱'


def update_state(state, core_rows, as_of):
    """每個在席者最近一次非紅燈的倉位。亮燈（綠／橘／黃）且距新高有資料才更新；
    其餘保留舊值；離席者的紀錄丟掉。"""
    new = {}
    for r in core_rows:
        t = r['ticker']
        lamp = r.get('lamp') or {}
        if lamp.get('code') in ba.LIT_LAMP_CODES and r.get('dist_ath_pct') is not None:
            new[t] = {'size': lamp.get('size'), 'code': lamp.get('code'), 'date': as_of}
        elif t in state:
            new[t] = state[t]
    return new


def _state_path():
    return OUT_DIR / STATE_NAME


def statutory_deadline(today, last_earnings_date=None):
    """Next filing deadline on/after `today` whose period is not reported yet.

    A deadline counts as already met when last_earnings_date falls after the
    previous deadline (e.g. reported 11/05 → the 11/14 Q3 deadline is done).
    Returns (date, label).
    """
    last = None
    if last_earnings_date:
        try:
            last = datetime.strptime(last_earnings_date[:10], '%Y-%m-%d').date()
        except ValueError:
            last = None
    seq = [(date(y, m, d), label) for y in (today.year - 1, today.year, today.year + 1)
           for m, d, label in TW_DEADLINES]
    for i in range(1, len(seq)):
        dl, label = seq[i]
        if dl < today:
            continue
        if last is not None and last > seq[i - 1][0]:
            continue
        return dl, label
    return None, None


def flat(r, today):
    """build_arena._flat_view() plus the TW-only display fields."""
    v = ba._flat_view(r)
    v['name'] = r.get('name')
    # route_why says「只能衛星」; there is no satellite track and 耐久 has its own column.
    v['route_why'] = None
    v['next_earn_fallback'] = None
    v['earnings_date_source'] = r.get('_earnings_date_source')
    v['x1_hold'] = bool(r.get('x1_hold'))
    if v.get('days_to_next_earnings') is None:
        dl, label = statutory_deadline(today, (r.get('_last_earnings_date')))
        if dl is not None:
            v['days_to_next_earnings'] = (dl - today).days
            v['next_earn_fallback'] = f"{label}法定期限 {dl.month}/{dl.day}"
    return v


def _lit(r):
    return (r.get('lamp') or {}).get('code') in ba.LIT_LAMP_CODES


def _pool_key(r):
    ey = ((r['grp'].get('own') or {}).get('raw') or {}).get('ey')
    return grp.pool_sort_key(r['grp'].get('rev_used_pct'), r.get('implied_growth_pct'), ey)


def select(rows, prev_core, reselect, last_snap=None, market=None, st_status=None, valhold=False):
    """Split rows into the board sections. Pure apart from the inputs.

    reselect=False keeps prev_core and carries the last rotation's removed/filled
    for display, so 新席 and the DOWN lines stay up until the next Saturday.

    market（v5.4）：market_state() 的結果。status 'bear'（v5.6）時不補新席，見 bear_no_buy()。mode 'x1'（大盤多頭）時，在席者只要仍在池內
    （資格成立）且沒跌破自己的 200 日線，就算留任候選，仍依池序競爭前 5；
    沒有 market 或 mode 'e1'＝現行賣法，與 v5.3 逐位元相同。
    valhold（2026-11-05，engine/seat_valhold.py）：True 時，還沒切換、只差估值閘的現任當作池內成員參與留任判定（續抱不加碼）；
    非現任不補。倉位上限與標籤在 build() 套用。False＝與現行逐位相同。
    """
    eligible = [r for r in rows if r['grp'].get('pass')]
    pool = sorted(eligible, key=_pool_key)   # v5.7：資格全過即入池，上修只排序（不再 ≥5% 門檻）
    by_t = {r['ticker']: r for r in rows}
    x1 = bool(market) and market.get('mode') == 'x1'
    pool_set = {r['ticker'] for r in pool}
    if valhold:   # 估值偏貴的現任算池內成員（x1 續抱判定用）；不改 pool／waiting，空席補人只看原池
        pool_set |= {t for t in (prev_core or []) if t in by_t and seat_valhold.is_val_hold(by_t[t])}
    if reselect:
        roster_pool = seat_valhold.augment_pool(pool, prev_core, rows, st_status, valhold)
        if x1:
            incumbents = set(prev_core or [])
            roster_pool = [_as_lit(r) if r['ticker'] in incumbents and _x1_dist_only(r) else r
                           for r in roster_pool]
        # 2026-11-05 折衷組：已切換 Supertrend 的現任不吃紅燈／200 日線／看大盤切換，只在週線 Supertrend 翻空或出池下席
        roster_pool, prev_sel, st_removed = seat_st.apply_overlay(roster_pool, prev_core, st_status, rows)
        rotation = ba.select_hold_roster(roster_pool, prev_sel, core_slots=CORE_SLOTS)
        if market and market.get('status') == 'bear':
            rotation = bear_no_buy(rotation, roster_pool, prev_sel)
        rotation['removed'] = list(rotation['removed']) + st_removed
    else:
        last_snap = last_snap or {}
        rotation = {'core': [t for t in (prev_core or []) if t in by_t], 'rotated': False,
                    'removed': [tuple(x) for x in last_snap.get('removed') or []],
                    'filled': [tuple(x) for x in last_snap.get('filled') or []],
                    'blocked': list(last_snap.get('blocked') or [])}
    core = [by_t[t] for t in rotation['core']]
    filled = {t for _, t in rotation['filled']}
    for r in core:
        r['seat_note'] = '新席' if r['ticker'] in filled else '現任'
        r['x1_hold'] = False
        if (st_status or {}).get(r['ticker'], {}).get('switched'):
            r['seat_note'] += '・Supertrend 持有'
        elif not _lit(r):
            if x1 and r['ticker'] in pool_set and _x1_dist_only(r):
                r['x1_hold'] = True
                r['seat_note'] += '・大盤多頭續抱'
            else:
                r['seat_note'] += '・週中轉紅，週六複判'
    seated = set(rotation['core'])
    waiting = [r for r in pool if r['ticker'] not in seated]
    buyable = [r for r in waiting if (r.get('lamp') or {}).get('code') in ba.LIT_LAMP_CODES]
    waiting_rest = [r for r in waiting if r not in buyable]
    candidates, others = [], []   # v5.7：沒有「池外」的資格全過名字了，兩欄留空保持輸出格式
    return {'eligible': eligible, 'pool': pool, 'rotation': rotation, 'core': core,
            'buyable': buyable, 'waiting_rest': waiting_rest,
            'too_expensive': ba.too_expensive_rows(rows),
            'candidates': candidates, 'others': others}


def concentration(sel, industry):
    """Industry mix of the core seats, or of the buyable names while the seats are
    empty (v5.7: the candidates list no longer exists). Informational like the US 最大單一產業占席 (no cap, owner 2026-09-17);
    industry = TWSE/TPEx official classification (latest.json tw_industry)."""
    basis, rows = ('core', sel['core']) if sel['core'] else ('buyable', sel['buyable'])
    counts = {}
    for r in rows:
        k = industry.get(r['ticker']) or '（未分類）'
        counts[k] = counts.get(k, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    share = round(ranked[0][1] / len(rows) * 100) if rows else 0
    return {'basis': basis, 'n': len(rows), 'rows': [{'industry': k, 'n': n} for k, n in ranked],
            'max_share_pct': share}


def _conc_html(conc):
    if not conc['n']:
        return ''
    mix = '、'.join(f"{escape(r['industry'])} ×{r['n']}" for r in conc['rows'])
    lead = ('核心席產業分布' if conc['basis'] == 'core'
            else f"核心席空著，先看可買 {conc['n']} 檔的產業分布")
    warn = (f"單一產業占 {conc['max_share_pct']}%，超過一半。產業不設上限（同美股），這行只是提示。"
            if conc['max_share_pct'] > 50 else '')
    return f'<div class="bw-note-line">{lead}（證交所／櫃買中心產業別）：{mix}。{warn}</div>'


# ── HTML ──────────────────────────────────────────────────────────────────

def _cells(v, lamp_map):
    cells = ba._row_cells(v, lamp_map)
    tk = escape(v['ticker'].split('.')[0])
    label = f"{tk} {escape(v['name'])}" if v.get('name') else tk
    link = (f'<a href="{escape(v["dd_path"])}#decision">{label}</a>' if v.get('dd_path') else label)
    cells[0] = ba._grp_cell(f'<td class="bw-l"><strong>{link}</strong></td>', 'sv-code')
    if v.get('rev_anchor') == 'quarter_end':
        # 缺財報日（build_dd_screener.tw_quarter_anchor_date()）：US 共用 tooltip 沒有這個錨定。
        title = escape(f"錨定：缺財報日，取該季季底前的快照｜基準快照 {v.get('rev_baseline_date') or '—'}")
        cells[1] = f'<td title="{title}">{ba._num(v.get("rev_used_pct"), 1)}</td>'
    elif v.get('earnings_date_source') == 'mops_board':
        # yfinance 沒有日期，財報日取自 MOPS（build_dd_screener / tw_mops_earnings.py）。
        cells[1] = cells[1].replace('title="錨定：', 'title="財報日取自公開資訊觀測站的董事會通過日｜錨定：', 1)
    if v.get('next_earn_fallback'):
        days = v['days_to_next_earnings']
        title = escape(f"公司未公告日期，依{v['next_earn_fallback']}推算，可能提前公布")
        cls = ' class="bw-pill bw-pill-warn"' if 0 <= days <= 7 else ''
        cells[3] = ba._grp_cell(f'<td class="bw-l"><span{cls} title="{title}">≤{days} 天</span></td>', 'g-t')
    return cells


def _table(views, lamp_map, seat_prefix=None, empty_seats=0):
    if not views and not empty_seats:
        return '<div class="bw-note-line">（無）</div>'
    head = ('<tr><th class="bw-l">' + ('席' if seat_prefix else '#') + '</th>'
            + ''.join(ba._shared_thead_cells('tw')) + '</tr>')
    body = []
    for i, v in enumerate(views, 1):
        code = f"{seat_prefix}{i}" if seat_prefix else str(i)
        body.append(f'<tr><td class="bw-l">{escape(code)}</td>' + ''.join(_cells(v, lamp_map)) + '</tr>')
    for j in range(len(views) + 1, len(views) + empty_seats + 1):
        body.append(ba._empty_seat_row(f'{seat_prefix}{j}'))
    return ('<div class="bw-scroll"><table><thead>' + head + '</thead><tbody>'
            + ''.join(body) + '</tbody></table></div>')


def _legend():
    return """<details class="bw-fold" open><summary>怎麼讀這張表</summary>
<div class="bw-note-line"><b>規則在哪裡</b>：進池條件、補席、倉位、賣法、切換 Supertrend、退回條件與版本史，見上方「席位規則」。這是研究名單，不是帳戶持倉。</div>
<div class="bw-note-line"><b>上修</b>：分析師把每股盈餘預估調高了幾 %。基準是這檔股票最近一次財報前的 Koyfin 快照，缺財報錨定時看近三個月。財報日先看 yfinance，沒有就用公開資訊觀測站上董事會通過財報的日期，兩邊都沒有就取該季季底前的快照。資格全過就入池（v5.7 起沒有上修門檻），池內由高到低排，同值先比隱含成長率，再比盈餘殖利率。上修只管排序。</div>
<div class="bw-note-line"><b>時機燈</b>：量的是距還原權息歷史新高多遠，燈號直接對應還沒切換 Supertrend 的持股倉位（已切換者固定滿倉）：綠 1.0／黃 1.0／橘 0.5／紅 0／不合格 0。🟢 可進＝距新高 3% 以內且站上 200 日線，正常倉。🟡 接近＝差 3%～10% 且站上 200 日線，同樣正常倉。距歷史新高資料缺的黃燈標「🟡 資料缺」，暫列半倉。🟠 過熱＝已在突破帶，但近 12 個月（扣最近一個月）漲幅 &gt;150%，半倉。🔴 拉回中＝差超過 10% 或跌破 200 日線，零倉。⚫ 不合格＝未站上 52 週線。🟢🟡🟠 算亮燈。滑過燈號可看階段燈，階段燈不影響時機燈。</div>
<div class="bw-note-line"><b>下次財報</b>：「≤N 天」是公司還沒公告日期，依法定期限推算（第一季 5/15、第二季 8/14、第三季 11/14、年報 3/31），實際可能更早。距財報 7 天內標橘色。</div>
<div class="bw-note-line"><b>底部</b>：只在距歷史新高 10% 以內才算。回檔一次比一次小、量縮、離底部高點近算「緊」，否則算「鬆」。只排 ② 可買裡 🟡 接近新高組的順序，不改燈號或倉位。結果顯示在備註欄，例如「底部 緊 2段」。</div>
<div class="bw-note-line"><b>耐久</b>：QGM 五年 ROIC 穩定度 ≥75%，或 Koyfin 五年平均、三年平均、現值三者都 ≥15%，兩種擇一達標。只是旗標，不擋資格；達標的在備註欄顯示「耐久 ✓」。</div>
<div class="bw-note-line"><b>欄位切換</b>：表格上方可切換「時機／基本面／全部」，一次切換全頁的席位表。代號、上修、時機、倉位永遠顯示；「時機」顯示距歷史新高、下次財報、估值、DD、備註；「基本面」顯示下段的數字欄。左右捲動時代號欄固定在左邊。③ 等待池與 ③b 太貴不入池預設收合，點標題展開。</div>
<div class="bw-note-line"><b>基本面欄組</b>：三年 EPS 成長、營收成長、ROIC、營業現金流率、EPS 預估（新台幣）、預估本益比、增量 ROIC、再投資率、隱含成長、營運槓桿，都來自 dd-screener，只供參考，不影響資格、排序與席位。其中三年 EPS 成長 ≥15%、ROIC 與營業現金流率本來就是資格條件，這裡只是把數字攤開。預估本益比＝現價 ÷ 明年預估 EPS，PEG＝預估本益比 ÷ 三年 EPS 年化成長（估值閘看的 PEG 就是這個），任一項算不出來就留空。</div>
<div class="bw-note-line"><b>跟美股的資料差異</b>：融券比在美股是資格條件，台股池沒有這項資料，這一條等於不設。內部人買賣在美股只是備註，台股池幾乎沒有資料。</div>
</details>"""


BOARD_ROWS = 40


def board_rows(rows):
    """全母體看板：資格全過的名字依 v4 對照分降冪，前 40，同美股
    build_arena.render_board_html()。分數算不出來的（五項百分位少於四項）
    apply_own_score_v4() 已記成 0，排在最後。只供對照，不影響席位或候補。"""
    return sorted((r for r in rows if r['grp'].get('pass')),
                  key=lambda r: -(r.get('score') or 0))[:BOARD_ROWS]


RULE_LINE = ('大盤多頭（加權報酬指數在 200 日線之上）時，在席者離歷史新高再遠也續抱，跌破自己的 200 日線才賣；'
             '大盤空頭時，時機燈轉紅就賣（距歷史新高超過 10% 或跌破 200 日線）。')


BUY_LINE = '大盤空頭的週六不補新席，空席放現金；大盤回到多頭的下一個週六照常補。'


def _market_html(market, rules=True):
    """賣法一句話＋目前大盤狀態一行（v5.4）。market＝market_state() 的結果。"""
    rule = (f'<div class="bw-note-line"><b>賣法</b>：{RULE_LINE}</div>'
            f'<div class="bw-note-line"><b>補位</b>：{BUY_LINE}</div>') if rules else ''
    if not market:
        return rule
    st = market.get('status')
    d = escape(market.get('data_date') or '—')
    if st in ('stale', 'missing'):
        line = (f'大盤資料未更新，本週照空頭處理，用「時機燈轉紅就賣」，新席照常補（最近一筆資料日期 {d}）。'
                if market.get('data_date')
                else '大盤資料未更新，本週照空頭處理，用「時機燈轉紅就賣」，新席照常補（沒有資料）。')
    else:
        nums = f"加權報酬指數 {market['close']:,.2f}"
        nums += f"，200 日線 {market['ma200']:,.2f}" if market.get('ma200') is not None \
            else '，200 日線資料不足，算多頭'
        word, way = ('多頭', '本週用「跌破自己的 200 日線才賣」') if st == 'bull' \
            else ('空頭', '本週用「時機燈轉紅就賣」，不補新席')
        line = f'大盤狀態（{d} 收盤）：{nums}，<b>{word}</b>。{way}。'
    return rule + f'<div class="bw-note-line">{line}</div>'


def render_html(as_of, rev_as_of, lamp_as_of, last_rotation_date, sel, views, n_universe,
                lamp_map, conc=None, market=None, st_html=''):
    core_v = [views[r['ticker']] for r in sel['core']]
    rev_n = sum(1 for v in views.values() if v.get('rev_used_pct') is not None)
    head = f"台股核心席 · 資料日 {as_of} · 台股池 {n_universe} 檔"
    rule = (f"資格全過入池 {len(sel['pool'])} 檔（v5.7 起沒有上修門檻，上修只排序），"
            f"有上修數字的 {rev_n} 檔。上修資料 {rev_as_of or '—'}，股價 {as_of}，"
            f"階段燈 {lamp_as_of or '—'}。")
    fresh = (f'<div class="bw-note-line">時機更新：{escape(as_of)}（每日）／'
             f'席位更新：{escape(last_rotation_date or "尚未重算")}（每週六（台北）依週五收盤）</div>')
    status = ''
    lines = [f'<div class="bw-note-line">🔻 DOWN <b>{escape(t)}</b>：{escape(why)}</div>'
             for t, why in sel['rotation'].get('removed') or []]
    yellow, red, gray = ba._group_waiting_pool_by_timing(sel['waiting_rest'])
    waiting_parts = []
    for (label, _), group in zip(ba._WAIT_GROUP_LABELS, (yellow, red, gray)):
        if group:
            waiting_parts.append(f'<div class="bw-sub" style="margin-top:10px"><b>{escape(label)}</b>'
                                 f'（{len(group)} 檔）</div>'
                                 + _table([views[r['ticker']] for r in group], lamp_map))
    v = lambda rows: [views[r['ticker']] for r in rows]  # noqa: E731
    buy_parts = [f'<div class="bw-sub" style="margin-top:10px"><b>{escape(label)}</b>'
                 f'（{len(group)} 檔）</div>' + _table(v(group), lamp_map)
                 for (label, _), group in zip(ba._BUY_GROUP_LABELS,
                                              ba._group_buyable_by_timing(sel['buyable'])) if group]
    return (
        '<div class="board-wrap">' + ba._BOARD_CSS
        + f'<div class="bw-head">{escape(head)}</div>'
        + f'<div class="bw-rule">{escape(rule)}</div>'
        + '<h3 class="bw-sec">① 核心席（5）</h3>'
        + '<div class="bw-sub">每週六（台北）依週五收盤：池內時機燈亮著（距歷史新高 ≥−10% 且站上 200 日線）'
          '的名字補空席，依上修由高到低；現任抱著，不因排名被換掉；亮燈不足就空席，不拿紅燈湊數。賣法與完整規則見上方「席位規則」。</div>'
        + fresh + rulecard.tw_card_html(_market_html(market, rules=False)) + st_html + status
        + ba._seat_view_bar_html()
        + _table(core_v, lamp_map, seat_prefix='C', empty_seats=CORE_SLOTS - len(core_v))
        + (f'<div class="bw-note-line">空席 {CORE_SLOTS - len(core_v)}：'
           + (escape('大盤空頭，本週不補新席，空席放現金。') if (market or {}).get('status') == 'bear'
              else escape(ba._core_vacancy_note(len(core_v), sel["buyable"])))
           + '</div>' if len(core_v) < CORE_SLOTS else '')
        + (f'<div class="bw-note-line">本週因大盤空頭沒補進：{escape("、".join(sel["rotation"]["blocked"]))}。</div>'
           if sel['rotation'].get('blocked') else '')
        + (_conc_html(conc) if conc else '')
        + _legend() + ''.join(lines)
        + f'<h3 class="bw-sec">② 可買（{len(sel["buyable"])} 檔）</h3>'
        + '<div class="bw-sub">池內沒坐核心席、今天時機燈亮著（綠／黃／橘）的名字，依燈號分組。</div>'
        + (''.join(buy_parts) or '<div class="bw-note-line">（無）</div>')
        + f'<details class="bw-fold bw-secfold"><summary>③ 等待池（{len(sel["waiting_rest"])} 檔）</summary>'
        + '<div class="bw-sub">資格全過、時機燈還沒亮的池內名字，依時機燈分組，組內依上修排序。</div>'
        + (''.join(waiting_parts) or '<div class="bw-note-line">（無）</div>')
        + '</details>'
        + f'<details class="bw-fold bw-secfold"><summary>③b 太貴不入池（{len(sel["too_expensive"])} 檔）</summary>'
        + '<div class="bw-sub">其他資格全過，只有估值偏貴。已在席、還沒切換的現任不賣、不加碼；已切換的不看估值；空席不補這些名字。</div>'
        + _table(v(sel['too_expensive']), lamp_map)
        + '</details>'
        + '</div>'
    )


# ── main ─────────────────────────────────────────────────────────────────

def _load_json(path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return default


def build(reselect, today=None):
    doc = _load_json(TW_POOL_JSON, None)
    if not doc or not doc.get('stocks'):
        _warn(f"{TW_POOL_JSON} missing or empty — outputs untouched")
        return None
    today = today or datetime.now(TPE).date()
    as_of = doc.get('as_of') or today.isoformat()
    rev_as_of = (doc.get('eps_estimates_source') or {}).get('snapshot_date')
    lamp_doc = _load_json(LAMP_TW_JSON, {})
    lamp_map = lamp_doc.get('lamp') or {}

    rows = []
    for s in doc['stocks']:
        r = tw_row(s)
        r['_last_earnings_date'] = s.get('last_earnings_date')
        r['_earnings_date_source'] = s.get('earnings_date_source')
        rows.append(r)
    ba.apply_own_score_v4(rows)   # v4 對照分：上修欄 tooltip 與全母體看板排序（同美股）

    ledger = _load_json(LEDGER_JSON, {'schema_version': 'tw-1.0', 'snapshots': []})
    snaps = sorted(ledger.get('snapshots') or [], key=lambda x: x.get('date') or '')
    if reselect:
        # A second run on the same price date (workflow retry) starts from the
        # roster before that date, so it reproduces the first run instead of
        # seeing its own seats as incumbents.
        prior = [x for x in snaps if (x.get('date') or '') < as_of]
        prev_core = prior[-1]['core'] if prior else []
    else:
        prev_core = (ledger.get('roster') or {}).get('core') or []
    # v5.4：賣法看決策日的大盤狀態。週六重選用當次 as_of；平日只刷燈號，沿用上次週六的決策日。
    decision_date = as_of if reselect else (ledger.get('last_rotation_date') or as_of)
    market = market_state(load_market_series(), decision_date)
    # 2026-11-05 折衷組（engine/seat_st.py）：決策日 >= seat_st.CUTOVER_DATE 才生效；舊規則名單另算，只寫 json
    st_on = seat_st.active(decision_date)
    st_hold_prev = seat_st.load_state(ST_STATE_JSON).get('holdings') or {}
    st_loader = seat_st.make_loader()
    vh_on = seat_valhold.active(decision_date)   # 2026-11-05 估值偏貴現任續抱、不加碼（三條線都套用）
    vh_pre = seat_valhold.load_pre(VALHOLD_JSON) if vh_on else {k: {} for k in seat_valhold.LINES}
    legacy_sel = None
    st_prev = None
    if st_on and reselect:
        legacy_prev = (ledger.get('roster_legacy') or {}).get('core')
        legacy_sel = select(copy.deepcopy(rows), prev_core if legacy_prev is None else legacy_prev, True,
                            last_snap=snaps[-1] if snaps else None, market=market, valhold=vh_on)
        ent0 = seat_st.entry_dates(prev_core, snaps, st_hold_prev, as_of)
        st_prev = seat_st.build_status(prev_core, ent0, decision_date, st_hold_prev, st_loader)
    elif st_on:
        st_prev = {}   # 平日刷新：名單沿用上次週六，下面對在席者另算顯示用狀態
    sel = select(rows, prev_core, reselect, last_snap=snaps[-1] if snaps else None, market=market,
                 st_status=st_prev, valhold=vh_on)
    state_doc = _load_json(_state_path(), {})
    state = state_doc.get('last_nonred') or {}
    st_status = {}
    if st_on:
        core_t = [r['ticker'] for r in sel['core']]
        ent1 = seat_st.entry_dates(core_t, snaps, st_hold_prev, as_of)
        st_status = seat_st.build_status(core_t, ent1, decision_date, st_hold_prev, st_loader)
        for r in sel['core']:   # 已切換者不吃看大盤切換的續抱
            if st_status[r['ticker']].get('switched'):
                r['x1_hold'] = False
    apply_x1_hold(sel, state)
    seat_st.mark_core_rows(sel['core'], st_status)
    new_state = update_state(state, sel['core'], as_of)   # 先於估值上限：狀態檔記未加上限的倉位
    vh_held = seat_valhold.held_set(sel['core'], {r['ticker'] for r in sel['pool']}, st_status, vh_on)
    seat_valhold.cap_rows(sel['core'], vh_held, vh_pre['new'])
    for r in sel['core']:
        if r['ticker'] in vh_held:
            r['seat_note'] += '・' + seat_valhold.TAG
    vh_pre_new = dict(vh_pre)   # 三條線轉紅前倉位的新狀態，只在週六重選時寫檔
    if vh_on and reselect:
        _sz = {r['ticker']: (r.get('lamp') or {}).get('size') for r in sel['core']}
        vh_pre_new['new'] = seat_valhold.next_pre(vh_pre['new'], list(_sz), vh_held, _sz.get, as_of)
    st_nav_doc = seat_st.load_nav(ST_NAV_JSON)
    hypo_doc = seat_st.load_hypo(ST_HYPO_JSON) or seat_st.load_hypo(ST_HYPO_SEED_JSON)
    if st_on and reselect:
        by_row = {r['ticker']: r for r in rows}

        def _legacy_size_raw(t):
            lamp = (by_row.get(t) or {}).get('lamp') or {}
            if lamp.get('code') in ba.LIT_LAMP_CODES:
                return lamp.get('size') or 0.0
            if lamp.get('code') == 'red' and x1_market(market):
                return (state.get(t) or {}).get('size', X1_DEFAULT_SIZE)   # 大盤多頭續抱：沿用最近非紅燈倉位
            return 0.0

        def _vh_line_held(roster, switched=lambda t: False):
            return {t for t in roster if vh_on and not switched(t) and t in by_row
                    and not by_row[t]['grp'].get('pass') and seat_valhold.is_val_hold(by_row[t])}
        _legacy_vh = _vh_line_held(legacy_sel['rotation']['core'])

        def _legacy_size(t):   # 估值偏貴的現任：取現行倉位與轉紅前倉位較小者
            return seat_valhold.capped(_legacy_size_raw(t), vh_pre['legacy'].get(t)) if t in _legacy_vh else _legacy_size_raw(t)
        st_nav_doc = seat_st.update_nav(
            st_nav_doc, decision_date,
            {r['ticker']: (r.get('lamp') or {}).get('size') or 0.0 for r in sel['core']},
            {t: _legacy_size(t) for t in legacy_sel['rotation']['core']}, st_loader)
        # 第三條對照線（假設一直在跑）：同一個 select（含大盤空頭不補席），起點是種子，名單只在週六重選時前進
        hypo_doc = seat_st.hypo_step(
            hypo_doc, decision_date, as_of,
            lambda prev, st0: select(copy.deepcopy(rows), prev, True, last_snap=snaps[-1] if snaps else None,
                                     market=market, st_status=st0, valhold=vh_on)['rotation'],
            lambda t, sw: 1.0 if sw else (seat_valhold.capped(_legacy_size_raw(t), vh_pre['hypo'].get(t))
                                           if t in _vh_line_held([t]) else _legacy_size_raw(t)),
            st_loader, known=set(by_row),
            name_of=lambda t: (by_row.get(t) or {}).get('name'))
        st_nav_doc = seat_st.attach_hypo_to_nav(st_nav_doc, hypo_doc)
        if vh_on:   # 舊規則線與假設線也記下「估值轉紅前最後一次」的倉位（新規則線在上面 cap_rows 之後記）
            _hh = hypo_doc.get('holdings') or {}
            _hyp_roster = hypo_doc.get('roster') or []
            vh_pre_new['legacy'] = seat_valhold.next_pre(vh_pre['legacy'], legacy_sel['rotation']['core'], _legacy_vh,
                                                         _legacy_size_raw, as_of)
            vh_pre_new['hypo'] = seat_valhold.next_pre(
                vh_pre['hypo'], _hyp_roster,
                _vh_line_held(_hyp_roster, lambda t: bool((_hh.get(t) or {}).get('switched'))), _legacy_size_raw, as_of)
    if st_on:
        if legacy_sel is not None:
            legacy_view = {'core': legacy_sel['rotation']['core'], 'removed': list(legacy_sel['rotation']['removed']),
                           'filled': [t for _, t in legacy_sel['rotation']['filled']], 'as_of': as_of}
        else:
            ls = next((x for x in reversed(snaps) if x.get('legacy_core') is not None), {})
            lc = (ledger.get('roster_legacy') or {}).get('core', ls.get('legacy_core'))
            legacy_view = None if lc is None else {
                'core': lc, 'removed': [tuple(x) for x in ls.get('legacy_removed') or []], 'filled': [],
                'as_of': ls.get('date')}
        names = {s0['ticker']: s0.get('name') for s0 in doc['stocks']}
        nm = lambda t: f"{t.split('.')[0]} {names.get(t) or ''}".strip()  # noqa: E731
        st_html = seat_st.legacy_html(legacy_view, '台股席位', nm, nav=seat_st.nav_summary(st_nav_doc))
    else:
        legacy_view, st_html = None, ''
    if hypo_doc:
        hnm = lambda t: (f"{t.split('.')[0]} {h['name']}" if (h := (hypo_doc.get('holdings') or {}).get(t)) and h.get('name')  # noqa: E731
                         else t.split('.')[0])
        st_html += seat_st.hypo_html(hypo_doc, seat_st.hypo_summary(hypo_doc, st_nav_doc), seat_st.nav_summary(st_nav_doc),
                                     '台股席位', hnm)
    views = {r['ticker']: flat(r, today) for r in rows}
    industry = {s['ticker']: s.get('tw_industry') for s in doc['stocks']}
    for t, v in views.items():
        v['tw_industry'] = industry.get(t)
    conc = concentration(sel, industry)
    board = board_rows(rows)
    seat_code = {r['ticker']: f"C{i}" for i, r in enumerate(sel['core'], 1)}

    last_rotation_date = ledger.get('last_rotation_date')
    if reselect:
        last_rotation_date = as_of
        snaps = [x for x in snaps if x.get('date') != as_of]
        snaps.append({'date': as_of, 'rev_data_as_of': rev_as_of, 'core': sel['rotation']['core'],
                      'removed': sel['rotation']['removed'], 'filled': sel['rotation']['filled'],
                      'blocked': sel['rotation'].get('blocked', [])})
        if st_on:
            snaps[-1]['legacy_core'] = legacy_sel['rotation']['core']
            snaps[-1]['legacy_removed'] = [list(x) for x in legacy_sel['rotation']['removed']]
        ledger = {'schema_version': 'tw-1.0', 'roster': {'core': sel['rotation']['core']},
                  'last_rotation_date': last_rotation_date, 'snapshots': snaps}
        if st_on:
            ledger['roster_legacy'] = {'core': legacy_sel['rotation']['core']}
            seat_st.save_state(ST_STATE_JSON, st_status, as_of)
            seat_st.save_nav(ST_NAV_JSON, st_nav_doc)
            seat_st.save_hypo(ST_HYPO_JSON, hypo_doc)
        if vh_on:
            seat_valhold.save_pre(VALHOLD_JSON, vh_pre_new, decision_date)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BODY_HTML.write_text(render_html(as_of, rev_as_of, lamp_doc.get('as_of'), last_rotation_date,
                                     sel, views, len(rows), lamp_map, conc, market, st_html), encoding='utf-8')
    if new_state != state:
        _state_path().write_text(json.dumps({'schema_version': 'tw-state-1.0', 'last_nonred': new_state},
                                            ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    pick = lambda key: [views[r['ticker']] for r in sel[key]]  # noqa: E731
    SEATS_JSON.write_text(json.dumps({
        'schema_version': 'tw-1.0',
        'as_of': as_of, 'rev_data_as_of': rev_as_of, 'stage_lamp_as_of': lamp_doc.get('as_of'),
        'last_rotation_date': last_rotation_date, 'market': market,
        'rotation': {'removed': [{'ticker': t, 'why': w} for t, w in sel['rotation'].get('removed') or []],
                     'filled': [{'ticker': t} for _, t in sel['rotation'].get('filled') or []]},
        'seat_st': {'active': st_on, 'cutover_date': seat_st.CUTOVER_DATE, 'decision_date': decision_date,
                    'status': {t: seat_st.public_view(v) for t, v in st_status.items()},
                    'nav': seat_st.nav_summary(st_nav_doc)},
        'seat_st_hypo': None if not hypo_doc else {
            'decision_date': hypo_doc.get('decision_date'), 'roster': hypo_doc.get('roster'),
            'holdings': hypo_doc.get('holdings'), 'summary': seat_st.hypo_summary(hypo_doc, st_nav_doc),
            'events_tail': (hypo_doc.get('events') or [])[-10:]},
        'legacy_rule': legacy_view,
        'counts': {'universe': len(rows), 'eligible': len(sel['eligible']), 'pool': len(sel['pool']),
                   'with_revision': sum(1 for v in views.values() if v.get('rev_used_pct') is not None),
                   'candidates': len(sel['candidates'])},
        'concentration': conc,
        'core_seats': [views[r['ticker']] for r in sel['core']],
        'buyable': pick('buyable'), 'waiting': pick('waiting_rest'),
        'too_expensive': pick('too_expensive'), 'candidates': pick('candidates'),
        'other_eligible': pick('others'),
        'board_v4': [{'rank': i, 'ticker': r['ticker'], 'name': r.get('name'),
                      'score_v4': (r['grp'].get('own') or {}).get('score'),
                      'seat': seat_code.get(r['ticker'])} for i, r in enumerate(board, 1)],
    }, ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    if reselect:
        LEDGER_JSON.write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ seats-tw {as_of}: eligible {len(sel['eligible'])}, pool {len(sel['pool'])}, "
          f"core {sel['rotation']['core']}, candidates {[r['ticker'] for r in sel['candidates']]}"
          + f", market {market['status']} ({market['data_date']})"
          + (" (re-selected)" if reselect else " (lamps only)"))
    return sel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', action='store_true',
                    help='re-select seats and append a ledger snapshot (Saturday Taipei run)')
    args = ap.parse_args()
    try:
        build(args.ledger)
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — outputs may be stale")
        _warn(f"build failed ({type(e).__name__}: {e})")
    sys.exit(0)


if __name__ == '__main__':
    main()
