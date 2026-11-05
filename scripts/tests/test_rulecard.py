"""席位規則卡（engine/rulecard.py）：門檻與日期從程式常數讀、三張卡都產得出來、精選榜標記可原地更新。"""
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from engine import grp, rulecard, seat_st, seat_tm, seat_valhold


def test_us_card_reads_constants_and_has_sell_table():
    h = rulecard.us_card_html({'status': 'bull', 'data_date': '2026-11-05', 'close': 110.0, 'ma200': 100.0})
    assert 'id="seat-rules"' in h and seat_st.REVIEW_DATE in h and seat_valhold.CUTOVER_DATE in h
    assert f'{grp.G_MIN_CAGR:g}%' in h and f'{grp.VAL_PEG_MAX:g}' in h and '<b>多頭</b>' in h
    assert h.count('<tr>') >= 4 and '估值偏貴・不加碼' not in h and '基本面不合格' in h
    assert not re.search(r'[一-鿿][,.:;]', re.sub(r'<[^>]*>', '', h))


def test_stale_market_falls_back_to_bear_text():
    assert '照空頭處理' in rulecard.market_line({'status': 'stale', 'data_date': '2026-10-01'})
    assert f'{seat_tm.MKT_MA}' in rulecard.market_line({'status': 'bear', 'data_date': 'x', 'close': 1.0, 'ma200': 2.0})


def test_tw_and_picks_cards_and_embed_refresh(tmp_path):
    assert '席位規則（台股席位）' in rulecard.tw_card_html('')
    assert '席位規則（精選榜）' in rulecard.picks_card_html()
    p = tmp_path / '_embed.html'
    p.write_text('a<!--RULECARD-->ZZSTALE<!--/RULECARD-->b', encoding='utf-8')
    assert rulecard.refresh_picks_embed(p) is True and 'ZZSTALE' not in p.read_text(encoding='utf-8')
    assert rulecard.refresh_picks_embed(p) is False
