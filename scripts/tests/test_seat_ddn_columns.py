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

N_DDN = 10     # 2026-10-21：PEG（明年）欄拿掉，估值欄已顯示同一個 PEG


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
    assert f"{s['live_fpe_est']:.1f}" in cells[5]
    assert f"{s['incremental_roic_pct']:.1f}" in cells[6] and f"{s['reinvest_rate_pct']:.1f}" in cells[7]
    assert f"{s['implied_growth_pct']:.1f}" in cells[8] and s['ol_divergence_label'] in cells[9] and f"{s['ol_divergence_pp']:+.2f}" in cells[9]
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


def _nvda_view():
    return ba._flat_view(ba.row_dict(_stocks('docs/dd-screener/latest.json')['NVDA'], yellow_full=True))


def test_peg_durable_bottom_columns_are_gone():
    heads = ''.join(ba._shared_thead_cells()) + ''.join(ba._shared_thead_cells('tw'))
    for gone in ('PEG（明年）', '>耐久<', '>底部<'):
        assert gone not in heads
    assert '>估值<' in heads            # 估值欄仍顯示 PEG


def test_column_groups_cover_every_cell_and_keep_core_columns_always_on():
    head = ba._shared_thead_cells()
    assert len(head) == len(ba.SHARED_COL_GROUPS) == 19
    cls = lambda c: re.search(r'class="([^"]*)"', c).group(1).split() if 'class="' in c else []  # noqa: E731
    always = [h for h, g in zip(head, ba.SHARED_COL_GROUPS) if g in ('', 'sv-code')]
    assert [re.sub(r'<[^>]+>', '', h) for h in always] == ['代號', '上修%（財報後）', '時機', '倉位']
    timing = [re.sub(r'<[^>]+>', '', h) for h in head if 'g-t' in cls(h)]
    assert timing == ['距歷史新高%', '下次財報', '估值', 'DD', '備註']
    fund = [h for h in head if 'g-f' in cls(h)]
    assert len(fund) == N_DDN
    row = ba._row_cells(_nvda_view(), {})
    assert [('g-t' in cls(c)) for c in row] == [('g-t' in cls(h)) for h in head]
    assert 'sv-code' in cls(head[0]) and 'sv-code' in cls(row[0])


def test_remark_carries_durable_and_bottom_tags_with_tooltips():
    v = _nvda_view()
    v.update(durable_5y=True, durable_roic_5y_avg_pct=31.2, durable_qgm_pct=88.0,
             vcp_scope='ok', vcp_gate=True, vcp_score=70, vcp_pullback_count=2,
             vcp_last_pullback_pct=4.5, vcp_vol_dryup_ratio=0.6, vcp_base_age_days=40,
             vcp_tight=True, dist_ath_pct=-4.0)
    note = ba._seat_remark(v)
    assert '耐久 ✓' in note and '五年 ROIC 平均 31.2%' in note
    if ba._vcp_kind(v) in ('tight', 'loose'):
        assert '底部 ' in note and 'VCP 分數' in note
    v2 = dict(v, durable_5y=False, dist_ath_pct=-40.0)
    note2 = ba._seat_remark(v2)
    assert '耐久' not in note2 and '底部' not in note2          # 「—」不放標籤


def test_board_html_has_no_full_universe_section_and_four_sections_collapsed():
    html = ba.render_board_html("2026-10-21", [], [], [], [], [], {}, [], {})
    assert '全母體看板' not in html and '>席<' not in html
    assert html.count('class="sv-bar"') == 1
    fold = re.findall(r'<details class="bw-fold bw-secfold"[^>]*><summary>([^<]*)</summary>', html)
    assert len(fold) == 4 and fold[0].startswith('③ 等待池') and fold[1].startswith('③b')
    assert not any('<details class="bw-fold bw-secfold"' in t and ' open' in t.split('>')[0]
                   for t in re.findall(r'<details[^>]*>', html) if 'secfold' in t)
    assert re.search(r'<details class="bw-fold" open><summary>怎麼讀這張表</summary>', html)
    assert '耐久、底部改在備註' in html or '備註欄顯示「耐久 ✓」' in html


def test_tw_empty_seat_row_keeps_cell_count():
    tr = ba._empty_seat_row('C4')
    assert tr.count('<td') == len(ba.SHARED_COL_GROUPS) + 1 and 'colspan' not in tr
