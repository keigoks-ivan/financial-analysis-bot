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
  4. Seats need revision >= +5% like the US pool. Until TW revision data
     exists the seats stay empty, and names that pass every gate with a lit
     timing lamp are listed unranked as candidates.

TW pool has no short-interest data, so that US gate never fires; insider
buying (a display chip in the US) is almost always empty. 下次財報 falls back to the
statutory filing deadline when yfinance has no date.

Seats are re-selected only with --ledger (the Saturday Taipei run, Friday
close). Other runs keep the stored roster and refresh lamps only — the same
split as the US engine.

Outputs:
  docs/cockpit-tw/data/_seats_tw_body.html  board fragment for cockpit-tw 席位排序
  docs/cockpit-tw/data/seats_tw.json        seats / pool / candidates as data
  docs/cockpit-tw/data/seats_tw_ledger.json roster state + weekly snapshots

Usage:
  python3 scripts/build_seats_tw.py            # daily: lamps only
  python3 scripts/build_seats_tw.py --ledger   # Saturday: re-select seats
"""

import argparse
import copy
import json
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from engine import build_arena as ba  # noqa: E402
from engine import grp  # noqa: E402
import tw_filing_calendar  # noqa: E402

TW_POOL_JSON = ROOT / 'docs' / 'dd-screener' / 'tw' / 'latest.json'
LAMP_TW_JSON = ROOT / 'docs' / 'stages' / 'data' / 'lamp_tw.json'
OUT_DIR = ROOT / 'docs' / 'cockpit-tw' / 'data'
BODY_HTML = OUT_DIR / '_seats_tw_body.html'
SEATS_JSON = OUT_DIR / 'seats_tw.json'
LEDGER_JSON = OUT_DIR / 'seats_tw_ledger.json'

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
    r = ba.row_dict(s)
    r['name'] = s0.get('name')
    g = r['grp'] = dict(r['grp'])
    g['why'] = [w.replace('品質閘 FCF', '品質閘 營業現金流利潤率') for w in g.get('why') or []]
    return r


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


def select(rows, prev_core, reselect, last_snap=None):
    """Split rows into the board sections. Pure apart from the inputs.

    reselect=False keeps prev_core and carries the last rotation's removed/filled
    for display, so 新席 and the DOWN lines stay up until the next Saturday.
    """
    eligible = [r for r in rows if r['grp'].get('pass')]
    pool = sorted((r for r in eligible if grp.in_pool(r['grp'].get('rev_used_pct'))), key=_pool_key)
    by_t = {r['ticker']: r for r in rows}
    if reselect:
        rotation = ba.select_lit_roster_v52(pool, prev_core, core_slots=CORE_SLOTS)
    else:
        last_snap = last_snap or {}
        rotation = {'core': [t for t in (prev_core or []) if t in by_t], 'rotated': False,
                    'removed': [tuple(x) for x in last_snap.get('removed') or []],
                    'filled': [tuple(x) for x in last_snap.get('filled') or []]}
    core = [by_t[t] for t in rotation['core']]
    filled = {t for _, t in rotation['filled']}
    for r in core:
        r['seat_note'] = '新席' if r['ticker'] in filled else '現任'
        if not _lit(r):
            r['seat_note'] += '・週中轉紅，週六複判'
    seated = set(rotation['core'])
    waiting = [r for r in pool if r['ticker'] not in seated]
    buyable = [r for r in waiting if (r.get('lamp') or {}).get('code') in ('green', 'hot')]
    waiting_rest = [r for r in waiting if r not in buyable]
    not_in_pool = [r for r in eligible if not grp.in_pool(r['grp'].get('rev_used_pct'))]
    candidates = sorted((r for r in not_in_pool
                         if r['grp'].get('rev_used_pct') is None and _lit(r)),
                        key=lambda r: r['ticker'])
    cand_set = {r['ticker'] for r in candidates}
    others = sorted((r for r in not_in_pool if r['ticker'] not in cand_set), key=_pool_key)
    return {'eligible': eligible, 'pool': pool, 'rotation': rotation, 'core': core,
            'buyable': buyable, 'waiting_rest': waiting_rest,
            'too_expensive': ba.too_expensive_rows(rows),
            'candidates': candidates, 'others': others}


def concentration(sel, industry):
    """Industry mix of the core seats, or of the candidates while the seats are
    empty. Informational like the US 最大單一產業占席 (no cap, owner 2026-09-17);
    industry = TWSE/TPEx official classification (latest.json tw_industry)."""
    basis, rows = ('core', sel['core']) if sel['core'] else ('candidates', sel['candidates'])
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
            else f"核心席空著，先看候補 {conc['n']} 檔的產業分布")
    warn = (f"單一產業占 {conc['max_share_pct']}%，超過一半。產業不設上限（同美股），這行只是提示。"
            if conc['max_share_pct'] > 50 else '')
    return f'<div class="bw-note-line">{lead}（證交所／櫃買中心產業別）：{mix}。{warn}</div>'


# ── HTML ──────────────────────────────────────────────────────────────────

def _cells(v, lamp_map):
    cells = ba._row_cells(v, lamp_map)
    tk = escape(v['ticker'].split('.')[0])
    label = f"{tk} {escape(v['name'])}" if v.get('name') else tk
    link = (f'<a href="{escape(v["dd_path"])}#decision">{label}</a>' if v.get('dd_path') else label)
    cells[0] = f'<td class="bw-l"><strong>{link}</strong></td>'
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
        cells[3] = f'<td class="bw-l"><span{cls} title="{title}">≤{days} 天</span></td>'
    return cells


def _table(views, lamp_map, seat_prefix=None, empty_seats=0):
    if not views and not empty_seats:
        return '<div class="bw-note-line">（無）</div>'
    head = ('<tr><th class="bw-l">' + ('席' if seat_prefix else '#') + '</th>'
            + ''.join(ba._shared_thead_cells()) + '</tr>')
    body = []
    for i, v in enumerate(views, 1):
        code = f"{seat_prefix}{i}" if seat_prefix else str(i)
        body.append(f'<tr><td class="bw-l">{escape(code)}</td>' + ''.join(_cells(v, lamp_map)) + '</tr>')
    n_cols = len(ba._shared_thead_cells())
    for j in range(len(views) + 1, len(views) + empty_seats + 1):
        body.append(f'<tr class="bw-muted-row"><td class="bw-l">{seat_prefix}{j}</td>'
                    f'<td class="bw-l" colspan="{n_cols}">空席</td></tr>')
    return ('<div class="bw-scroll"><table><thead>' + head + '</thead><tbody>'
            + ''.join(body) + '</tbody></table></div>')


def _legend():
    return """<details class="bw-fold" open><summary>怎麼讀這張表</summary>
<div class="bw-note-line"><b>規則跟美股核心席相同</b>：先過資格，再依財報後上修排序，最後由時機燈決定倉位。核心席每週六（台北）依週五收盤重算：池內時機燈亮著的名字依上修取前 5，亮燈不足就空席。週中燈號只管倉位。這是研究名單，不是帳戶持倉。</div>
<div class="bw-note-line"><b>資格</b>：三年成長、品質、站上 52 週線三項全過。三年成長＝Koyfin 今年到後年的每股盈餘年化成長 ≥15%，沒有第三年預估就不算過。品質＝投入資本報酬率（ROIC）≥15% 且營業現金流利潤率 ≥10%，或 ROIC ≥25% 且營業現金流為正。台股資本支出重，品質改看營業現金流，美股看自由現金流。另外五種情況直接出局：體質拒絕、衰退 ⛔、DD 迴避、財報後上修低於 −5%、估值閘紅燈（PEG &gt;2.0 或本益比相對五年均值 &gt;1.75 倍）。市值不另設門檻，台股池本身已是 10 億美元以上。</div>
<div class="bw-note-line"><b>上修</b>：分析師對每股盈餘預估調高了幾 %，基準是這檔股票最近一次財報前的那份 Koyfin 快照。上修 ≥5% 才入池，池內依上修由高到低排。台股快照從 2026-10 開始存，第一筆上修要等第三季財報之後再匯出一次，在那之前核心席空著，過關且燈亮的名字列在「④ 候補」。yfinance 沒有財報日的名字，改用公開資訊觀測站上董事會通過財報的日期。</div>
<div class="bw-note-line"><b>時機燈</b>：量的是距還原權息歷史新高多遠。🟢 可進＝距新高 3% 以內且站上 200 日線，正常倉。🟡 半倉＝差 3%～10%。🟠 過熱＝近 12 個月（扣最近一個月）漲幅 &gt;150%，半倉。🔴 等板機＝差超過 10% 或跌破 200 日線，零倉。⚫ 不合格＝未站上 52 週線。🟢🟡🟠 算亮燈。滑過燈號可看階段燈，階段燈不影響時機燈。</div>
<div class="bw-note-line"><b>下次財報</b>：「≤N 天」是公司還沒公告日期，依法定期限推算（第一季 5/15、第二季 8/14、第三季 11/14、年報 3/31），實際可能更早。距財報 7 天內標橘色。</div>
<div class="bw-note-line"><b>底部</b>：只在距歷史新高 10% 以內才算。回檔一次比一次小、量縮、離底部高點近算「緊」，否則算「鬆」。只排 ③ 等待池裡 🟡 組的順序，不改燈號或倉位。</div>
<div class="bw-note-line"><b>跟美股的資料差異</b>：融券比在美股是資格條件，台股池沒有這項資料，這一條等於不設。內部人買賣在美股只是備註，台股池幾乎沒有資料。</div>
</details>"""


def render_html(as_of, rev_as_of, lamp_as_of, last_rotation_date, sel, views, n_universe,
                lamp_map, conc=None):
    core_v = [views[r['ticker']] for r in sel['core']]
    rev_n = sum(1 for v in views.values() if v.get('rev_used_pct') is not None)
    head = f"台股核心席 · {as_of} · 台股池 {n_universe} 檔"
    rule = (f"資格全過 {len(sel['eligible'])} 檔，上修 ≥5% 入池 {len(sel['pool'])} 檔，"
            f"有上修數字的 {rev_n} 檔。Koyfin 預估 {rev_as_of or '—'}，股價 {as_of}，"
            f"階段燈 {lamp_as_of or '—'}。")
    fresh = (f'<div class="bw-note-line">時機更新：{escape(as_of)}（每日）／'
             f'席位更新：{escape(last_rotation_date or "尚未重算")}（每週六（台北）依週五收盤）</div>')
    if rev_n == 0:
        status = ('<div class="bw-note-line"><b>目前沒有任何一檔有上修數字，核心席全部空著。</b>'
                  '過關且燈亮的名字列在下方「④ 候補」，不排名。</div>')
    else:
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
    return (
        '<div class="board-wrap">' + ba._BOARD_CSS
        + f'<div class="bw-head">{escape(head)}</div>'
        + f'<div class="bw-rule">{escape(rule)}</div>'
        + '<h3 class="bw-sec">① 核心席（5）</h3>'
        + '<div class="bw-sub">每週六（台北）依週五收盤：池內時機燈亮著（距歷史新高 ≥−10% 且站上 200 日線）'
          '的名字依上修取前 5；亮燈不足就空席，不拿紅燈湊數。</div>'
        + fresh + status
        + _table(core_v, lamp_map, seat_prefix='C', empty_seats=CORE_SLOTS - len(core_v))
        + (_conc_html(conc) if conc else '')
        + _legend() + ''.join(lines)
        + f'<h3 class="bw-sec">② 可買（{len(sel["buyable"])} 檔）</h3>'
        + '<div class="bw-sub">池內沒坐核心席、時機燈綠或橘的名字。</div>'
        + _table(v(sel['buyable']), lamp_map)
        + f'<h3 class="bw-sec">③ 等待池（{len(sel["waiting_rest"])} 檔）</h3>'
        + '<div class="bw-sub">上修夠、還沒突破的池內名字，依時機燈分組，組內依上修排序。</div>'
        + (''.join(waiting_parts) or '<div class="bw-note-line">（無）</div>')
        + f'<h3 class="bw-sec">③b 太貴不入池（{len(sel["too_expensive"])} 檔）</h3>'
        + '<div class="bw-sub">其他資格全過，只有估值閘紅燈。名字在這裡代表不加碼，不是賣出訊號。</div>'
        + _table(v(sel['too_expensive']), lamp_map)
        + f'<h3 class="bw-sec">④ 候補：過關、燈亮、還沒有上修數字（{len(sel["candidates"])} 檔）</h3>'
        + '<div class="bw-sub">資格全過、時機燈亮著，只差上修數字。不排名，依代號排列。'
          '有了上修數字後，≥5% 的進池、依上修排序，未達 5% 的移到 ⑤。</div>'
        + _table(v(sel['candidates']), lamp_map)
        + f'<details class="bw-fold"><summary>⑤ 其他過關名字（{len(sel["others"])} 檔，點開）</summary>'
        + '<div class="bw-sub">資格全過，但上修未達 5%，或時機燈沒亮且還沒有上修數字。不進池、不佔席。</div>'
        + _table(v(sel['others']), lamp_map) + '</details>'
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
    ba.apply_own_score_v4(rows)   # v4 對照分，只進上修欄 tooltip（同美股）

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
    sel = select(rows, prev_core, reselect, last_snap=snaps[-1] if snaps else None)
    views = {r['ticker']: flat(r, today) for r in rows}
    industry = {s['ticker']: s.get('tw_industry') for s in doc['stocks']}
    for t, v in views.items():
        v['tw_industry'] = industry.get(t)
    conc = concentration(sel, industry)

    last_rotation_date = ledger.get('last_rotation_date')
    if reselect:
        last_rotation_date = as_of
        snaps = [x for x in snaps if x.get('date') != as_of]
        snaps.append({'date': as_of, 'rev_data_as_of': rev_as_of, 'core': sel['rotation']['core'],
                      'removed': sel['rotation']['removed'], 'filled': sel['rotation']['filled']})
        ledger = {'schema_version': 'tw-1.0', 'roster': {'core': sel['rotation']['core']},
                  'last_rotation_date': last_rotation_date, 'snapshots': snaps}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BODY_HTML.write_text(render_html(as_of, rev_as_of, lamp_doc.get('as_of'), last_rotation_date,
                                     sel, views, len(rows), lamp_map, conc), encoding='utf-8')
    pick = lambda key: [views[r['ticker']] for r in sel[key]]  # noqa: E731
    SEATS_JSON.write_text(json.dumps({
        'schema_version': 'tw-1.0',
        'as_of': as_of, 'rev_data_as_of': rev_as_of, 'stage_lamp_as_of': lamp_doc.get('as_of'),
        'last_rotation_date': last_rotation_date,
        'counts': {'universe': len(rows), 'eligible': len(sel['eligible']), 'pool': len(sel['pool']),
                   'with_revision': sum(1 for v in views.values() if v.get('rev_used_pct') is not None),
                   'candidates': len(sel['candidates'])},
        'concentration': conc,
        'core_seats': [views[r['ticker']] for r in sel['core']],
        'buyable': pick('buyable'), 'waiting': pick('waiting_rest'),
        'too_expensive': pick('too_expensive'), 'candidates': pick('candidates'),
        'other_eligible': pick('others'),
    }, ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    if reselect:
        LEDGER_JSON.write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ seats-tw {as_of}: eligible {len(sel['eligible'])}, pool {len(sel['pool'])}, "
          f"core {sel['rotation']['core']}, candidates {[r['ticker'] for r in sel['candidates']]}"
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
