"""check_market_read 第 13–17 項：可讀性（2026-09-24）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_market_read as critic  # noqa: E402


def test_number_count_skips_dates_and_tenors():
    assert critic.count_numbers("10 年期在 12/23 前、2007 年 7 月、3 個月、200 日線、標普 500") == 0
    assert critic.count_numbers("VIX 15.18（分位 11.9）") == 2
    assert critic.count_numbers("銀行準備金 3,014") == 1


def test_headline_lead_too_long_fails():
    data = {"thesis_zh": "利率壓力從短端擴散到長端，指數已退到機械賣壓的門口，先弱後強的「弱」那段有了觸發者。後面是證據。"}
    assert critic.check_headline_leads(data)[0] == critic.FAIL


def test_headline_lead_two_numbers_fails():
    data = {"horizons": [{"logic_zh": "我給 46%，比上期低 1 個百分點。"}]}
    assert critic.check_headline_leads(data)[0] == critic.FAIL


def test_headline_lead_plain_passes():
    data = {"thesis_zh": "長天期利率也開始漲了，股市短線偏弱的理由出現。10 年期盤中 5.14%。",
            "horizons": [{"logic_zh": "我給 46%，比上期略低。"}]}
    assert critic.check_headline_leads(data)[0] == critic.PASS


def test_sentence_semicolon_splits_and_counts():
    ok = {"path_zh": "10 年期盤中 5.14%；MOVE（債券波動指數）95.45。"}
    assert critic.check_sentence_size(ok)[0] == critic.PASS
    crowded = {"path_zh": "標普 7,706.03 跌 0.76%、分位從 98.8 掉到 93.7。"}
    assert critic.check_sentence_size(crowded)[0] == critic.FAIL


def test_sentence_length_ignores_gloss():
    gloss = "期限溢價（" + "投資人要求多付的長天期補償" * 5 + "）上升。"
    assert critic.check_sentence_size({"path_zh": gloss})[0] == critic.PASS
    assert critic.check_sentence_size({"path_zh": "長" * 61 + "。"})[0] == critic.FAIL


def test_forces_title_and_deviation_why_are_checked():
    data = {"forces": [{"title": "指數到了門口"}], "deviations_from_tables": [{"why": "帳上給 84%。"}]}
    status, detail = critic.check_plain_words(data)
    assert status == critic.FAIL
    assert "門口" in detail and "帳上" in detail


def test_source_mid_sentence_fails_end_passes():
    mid = {"path_zh": "5 年期破 5%（鉅亨 9/24），MOVE 跳升。"}
    end = {"path_zh": "5 年期破 5%（鉅亨 9/24）。"}
    assert critic.check_source_position(mid)[0] == critic.FAIL
    assert critic.check_source_position(end)[0] == critic.PASS


def test_data_gaps_len():
    assert critic.check_data_gaps_len({"data_gaps_zh": "缺" * 151})[0] == critic.FAIL
    assert critic.check_data_gaps_len({"data_gaps_zh": "缺" * 150})[0] == critic.PASS


def test_vs_prior_lead_number_limit():
    status, detail = critic.check_vs_prior_lead({"vs_prior_zh": "上期 46% 這期 47%。"})
    assert status == critic.FAIL
    assert "數字" in detail


def test_jargon_gloss_now_fails():
    assert critic.check_jargon_gloss({"path_zh": "期限溢價上升。"})[0] == critic.FAIL


def test_registered_in_checks():
    names = [name for name, _, _ in critic.CHECKS]
    for n in ("headline_leads", "sentence_size", "plain_words", "source_position", "data_gaps_len"):
        assert n in names
