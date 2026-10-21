"""席位表「dd-screener 數字欄」（2026-10-21）：表頭與列欄數一致、缺值顯示「—」、
NVDA／2330 的數字與 latest.json 一致。純顯示，不影響資格。無網路。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
ROOT = SCRIPTS_DIR.parent

import build_seats_tw as tw  # noqa: E402
from engine import build_arena as ba  # noqa: E402

N_DDN = 11


def _stocks(path):
    return {s['ticker']: s for s in json.loads((ROOT / path).read_text(encoding='utf-8'))['stocks']}


def _n_th(cells):
    return sum(c.startswith('<th') for c in cells)


def _n_td(cells):
    return sum(c.startswith('<td') for c in cells)


def test_header_and_row_cell_counts_match_us_and_tw():
    assert len(ba._shared_thead_cells()) == len(ba._shared_thead_cells('tw'))
    v = ba._flat_view(ba.row_dict(_stocks('docs/dd-screener/latest.json')['NVDA'], yellow_full=True))
    assert len(ba._row_cells(v, {})) == len(ba._shared_thead_cells())
    assert len(ba._ddn_thead_cells()) == len(ba._ddn_cells(v)) == N_DDN


def test_missing_values_show_dash():
    cells = ba._ddn_cells({'ddn': {}})
    assert len(cells) == N_DDN and all('—' in c for c in cells)
    assert all('—' in c for c in ba._ddn_cells({}))
    assert ba.dd_numbers({'ticker': 'X'})['pe2'] is None


def test_nvda_numbers_match_latest_json():
    s = _stocks('docs/dd-screener/latest.json')['NVDA']
    cells = ba._ddn_cells(ba._flat_view(ba.row_dict(s, yellow_full=True)))
    txt = ' '.join(re.sub(r'<[^>]+>', '', c) for c in cells)
    assert f"{s['eps_fy1_fy3_cagr_pct']:.1f}" in cells[0]
    assert f"{s['fund']['est_rev_cagr_3y_pct']:.1f}" in cells[1]
    assert f"{s['roic']:.1f}" in cells[2] and f"{s['fcf']:.1f}" in cells[3]
    assert f"{s['eps_fy_curr']:.2f}／{s['eps_fy_next']:.2f}／{s['eps_fy3']:.2f}" in cells[4]
    assert f"{s['live_fpe_est']:.1f}" in cells[5] and f"{s['live_peg']:.2f}" in cells[6]
    assert f"{s['incremental_roic_pct']:.1f}" in cells[7] and f"{s['reinvest_rate_pct']:.1f}" in cells[8]
    assert f"{s['implied_growth_pct']:.1f}" in cells[9] and s['ol_divergence_label'] in cells[10] and f"{s['ol_divergence_pp']:+.2f}" in cells[10]
    assert 'None' not in txt and 'nan' not in txt


def test_pe_falls_back_to_frozen_and_peg_to_frozen():
    d = ba.dd_numbers({'live_fpe_est': None, 'fpe_fy2': 20.0, 'live_peg': None, 'peg': 1.5})
    assert d['pe2'] == 20.0 and d['peg'] == 1.5


def test_tw_2330_uses_ocf_and_matches_latest_json():
    s = _stocks('docs/dd-screener/tw/latest.json')['2330.TW']
    v = tw.flat(tw.tw_row(s), __import__('datetime').date(2026, 10, 21))
    cells = tw._cells(v, {})
    assert len(cells) == len(ba._shared_thead_cells('tw'))
    d = v['ddn']
    assert d['cf'] == s['ocf'] and d['eps_ccy'] == 'TWD'
    assert d['pe2'] == s['live_fpe_est'] and d['peg'] == s['live_peg']
    assert any('營業現金流率%' in h for h in ba._shared_thead_cells('tw'))
    assert any('自由現金流率%' in h for h in ba._shared_thead_cells('us'))


def test_board_tr_seat_cell_stays_after_shared_index_8():
    v = ba._flat_view(ba.row_dict(_stocks('docs/dd-screener/latest.json')['NVDA'], yellow_full=True))
    tr = ba._board_tr(v, 1, 'C1', {})
    assert tr.count('<td') == len(ba._shared_thead_cells()) + 2
