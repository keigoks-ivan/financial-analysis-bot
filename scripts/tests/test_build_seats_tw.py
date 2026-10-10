"""台股核心席 (scripts/build_seats_tw.py) — owner decisions 2026-10-09/10.

Checks: OCF margin stands in for FCF margin in the quality gate; seats stay
empty without revision data and lit names become unranked candidates; the
Saturday re-selection follows the US v5.2 rule and is idempotent on a retry;
the statutory filing deadline fills 下次財報 when yfinance has no date.
Synthetic stocks, no network.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_seats_tw as tw  # noqa: E402


def _stock(ticker, dist_ath=-1.0, vs200=5.0, ocf=20.0, fcf=-5.0, cagr=20.0, **extra):
    s = {'ticker': ticker, 'name': ticker.split('.')[0], 'roic': 20.0, 'fcf': fcf, 'ocf': ocf,
         'eps_fy1_fy3_cagr_pct': cagr, 'eps_fy_curr': 10, 'eps_fy_next': 12, 'eps_fy3': 14.4,
         'ma': {'above_w52': True, 'dist_ath_pct': dist_ath, 'vs_200ma_pct': vs200, 'price': 100},
         'timing': {'dist_52w_high_pct': dist_ath}, 'last_earnings_date': '2026-08-10'}
    s.update(extra)
    return s


def _rev(pct):
    # eps_rev_since_earnings_* is what grp reads first (財報錨定上修).
    return {'eps_rev_since_earnings_pct': pct, 'eps_rev_since_earnings_baseline_date': '2026-10-09',
            'eps_rev_anchor': 'earnings'}


# ── quality gate on OCF ───────────────────────────────────────────────────

def test_ocf_replaces_fcf_in_quality_gate():
    r = tw.tw_row(_stock('1111.TW', fcf=-5.0, ocf=20.0))
    assert r['grp']['pass'] is True


def test_low_ocf_fails_quality_gate_with_relabelled_reason():
    r = tw.tw_row(_stock('1111.TW', fcf=30.0, ocf=5.0))
    assert r['grp']['pass'] is False
    assert any('營業現金流利潤率' in w for w in r['grp']['why'])
    assert not any('FCF' in w for w in r['grp']['why'])


def test_three_year_growth_is_required():
    s = _stock('1111.TW')
    s['eps_fy1_fy3_cagr_pct'] = None
    s['eps_fy3'] = None
    assert tw.tw_row(s)['grp']['pass'] is False


# ── selection ─────────────────────────────────────────────────────────────

def _rows(stocks):
    return [tw.tw_row(s) for s in stocks]


def test_no_revision_empty_seats_and_lit_candidates():
    rows = _rows([_stock('3333.TW'), _stock('1111.TW'),
                  _stock('2222.TW', dist_ath=-20.0)])          # red lamp
    sel = tw.select(rows, [], reselect=True)
    assert sel['pool'] == [] and sel['core'] == []
    assert [r['ticker'] for r in sel['candidates']] == ['1111.TW', '3333.TW']   # by code
    assert [r['ticker'] for r in sel['others']] == ['2222.TW']


def test_reselect_takes_top_lit_by_revision():
    stocks = [_stock(f'{1000 + i}.TW', **_rev(30 - i)) for i in range(7)]
    stocks[0]['ma']['dist_ath_pct'] = -20.0                       # top revision, red lamp
    stocks[0]['timing']['dist_52w_high_pct'] = -20.0
    stocks.append(_stock('9999.TW', **_rev(3.0)))                 # below +5%: not in pool
    sel = tw.select(_rows(stocks), [], reselect=True)
    assert [r['ticker'] for r in sel['core']] == ['1001.TW', '1002.TW', '1003.TW', '1004.TW', '1005.TW']
    assert all(r['seat_note'] == '新席' for r in sel['core'])
    assert {r['ticker'] for r in sel['buyable']} == {'1006.TW'}
    assert [r['ticker'] for r in sel['waiting_rest']] == ['1000.TW']
    assert [r['ticker'] for r in sel['others']] == ['9999.TW']
    assert sel['candidates'] == []


def test_daily_keeps_roster_and_carries_last_rotation_notes():
    stocks = [_stock('1000.TW', **_rev(10)), _stock('2000.TW', **_rev(20))]
    stocks[1]['ma']['dist_ath_pct'] = -20.0                       # seated name turned red mid-week
    stocks[1]['timing']['dist_52w_high_pct'] = -20.0
    last = {'date': '2026-10-09', 'core': ['2000.TW'], 'removed': [], 'filled': [['core', '2000.TW']]}
    sel = tw.select(_rows(stocks), ['2000.TW'], reselect=False, last_snap=last)
    assert [r['ticker'] for r in sel['core']] == ['2000.TW']
    assert sel['core'][0]['seat_note'] == '新席・週中轉紅，週六複判'


# ── statutory deadline ────────────────────────────────────────────────────

@pytest.mark.parametrize('today,last,expect', [
    (date(2026, 10, 10), '2026-08-10', (date(2026, 11, 14), '第三季')),
    (date(2026, 10, 10), None, (date(2026, 11, 14), '第三季')),
    (date(2026, 11, 6), '2026-11-05', (date(2027, 3, 31), '年報')),     # Q3 already out
    (date(2026, 11, 15), None, (date(2027, 3, 31), '年報')),
    (date(2027, 3, 25), '2027-03-20', (date(2027, 5, 15), '第一季')),
    (date(2026, 10, 10), '2026-05-10', (date(2026, 11, 14), '第三季')),  # stale date
])
def test_statutory_deadline(today, last, expect):
    assert tw.statutory_deadline(today, last) == expect


# ── build(): outputs and retry idempotency ────────────────────────────────

@pytest.fixture
def paths(tmp_path, monkeypatch):
    pool = tmp_path / 'latest.json'
    out = tmp_path / 'out'
    monkeypatch.setattr(tw, 'TW_POOL_JSON', pool)
    monkeypatch.setattr(tw, 'LAMP_TW_JSON', tmp_path / 'lamp_tw.json')
    monkeypatch.setattr(tw, 'OUT_DIR', out)
    monkeypatch.setattr(tw, 'BODY_HTML', out / '_seats_tw_body.html')
    monkeypatch.setattr(tw, 'SEATS_JSON', out / 'seats_tw.json')
    monkeypatch.setattr(tw, 'LEDGER_JSON', out / 'seats_tw_ledger.json')
    return pool, out


def _write_pool(pool, stocks, as_of):
    pool.write_text(json.dumps({'as_of': as_of, 'stocks': stocks}), encoding='utf-8')


def test_build_writes_fragment_and_fallback_earnings(paths):
    pool, out = paths
    _write_pool(pool, [_stock('1111.TW', next_earnings_date=None)], '2026-10-09')
    tw.build(False, today=date(2026, 10, 10))
    html = (out / '_seats_tw_body.html').read_text(encoding='utf-8')
    assert html.startswith('<div class="board-wrap">') and html.count('空席') >= 5
    assert '≤35 天' in html
    data = json.loads((out / 'seats_tw.json').read_text(encoding='utf-8'))
    assert data['counts']['candidates'] == 1
    assert data['candidates'][0]['next_earn_fallback'] == '第三季法定期限 11/14'
    assert not (out / 'seats_tw_ledger.json').exists()          # daily run never writes the ledger


def test_reselect_retry_on_same_date_is_idempotent(paths):
    pool, out = paths
    ledger = out / 'seats_tw_ledger.json'
    _write_pool(pool, [_stock('1000.TW', **_rev(10))], '2026-10-16')
    tw.build(True, today=date(2026, 10, 17))
    _write_pool(pool, [_stock('1000.TW', **_rev(10)), _stock('2000.TW', **_rev(20))], '2026-10-23')
    tw.build(True, today=date(2026, 10, 24))
    first = json.loads(ledger.read_text(encoding='utf-8'))
    tw.build(True, today=date(2026, 10, 24))                       # workflow retry
    second = json.loads(ledger.read_text(encoding='utf-8'))
    assert first == second
    assert [s['date'] for s in second['snapshots']] == ['2026-10-16', '2026-10-23']
    assert second['snapshots'][-1]['filled'] == [['core', '2000.TW']]
    assert second['roster']['core'] == ['2000.TW', '1000.TW']


def test_quarter_end_anchor_gets_its_own_tooltip():
    s = _stock('1111.TW', eps_rev_since_earnings_pct=8.0,
               eps_rev_since_earnings_baseline_date='2026-09-26', eps_rev_anchor='quarter_end')
    v = tw.flat(tw.tw_row(s), date(2026, 11, 20))
    cell = tw._cells(v, {})[1]
    assert '缺財報日' in cell and '2026-09-26' in cell and '8.0' in cell


# ── industry concentration (informational, 2026-10-10) ────────────────────

def test_concentration_uses_candidates_while_seats_are_empty():
    rows = _rows([_stock('1111.TW'), _stock('2222.TW'), _stock('3333.TW')])
    sel = tw.select(rows, [], reselect=True)
    conc = tw.concentration(sel, {'1111.TW': '半導體業', '2222.TW': '半導體業'})
    assert conc['basis'] == 'candidates' and conc['n'] == 3
    assert conc['rows'] == [{'industry': '半導體業', 'n': 2}, {'industry': '（未分類）', 'n': 1}]
    assert conc['max_share_pct'] == 67
    html = tw._conc_html(conc)
    assert '候補 3 檔' in html and '超過一半' in html


def test_concentration_switches_to_core_seats():
    stocks = [_stock(f'{1000 + i}.TW', **_rev(30 - i)) for i in range(2)]
    sel = tw.select(_rows(stocks), [], reselect=True)
    conc = tw.concentration(sel, {'1000.TW': '半導體業', '1001.TW': '光電業'})
    assert conc['basis'] == 'core' and conc['max_share_pct'] == 50
    assert '超過一半' not in tw._conc_html(conc)


def test_build_writes_industry_and_concentration(paths):
    pool, out = paths
    _write_pool(pool, [_stock('1111.TW', tw_industry='半導體業')], '2026-10-09')
    tw.build(False, today=date(2026, 10, 10))
    data = json.loads((out / 'seats_tw.json').read_text(encoding='utf-8'))
    assert data['candidates'][0]['tw_industry'] == '半導體業'
    assert data['concentration']['rows'] == [{'industry': '半導體業', 'n': 1}]
    assert '證交所／櫃買中心產業別' in (out / '_seats_tw_body.html').read_text(encoding='utf-8')


def test_mops_dated_name_says_so_in_the_revision_tooltip():
    s = _stock('1111.TW', earnings_date_source='mops_board', **_rev(8.0))
    r = tw.tw_row(s)
    r['_earnings_date_source'] = s['earnings_date_source']
    cell = tw._cells(tw.flat(r, date(2026, 10, 10)), {})[1]
    assert '董事會通過日｜錨定：財報後' in cell
    plain = tw._cells(tw.flat(tw.tw_row(_stock('2222.TW', **_rev(8.0))), date(2026, 10, 10)), {})[1]
    assert '董事會通過日' not in plain
