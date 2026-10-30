"""check_picks_text.py：「本站挑選」文字檢查（登記四段＋月評）。"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import check_picks_text as cpt  # noqa: E402

EVIDENCE = """# 證據包　資料日 2026-10-27
00981A 近一年含息 +155.9%｜00985A 近一年 +40.2%｜0050 近一年 +119.1%
最大回檔（近三年）00981A -18.4%｜00985A -9.7%｜0050 -22.3%
遠期本益比 00981A 21.5｜00985A 14.8　持股重疊 36.9%
20 日命中率 62.5%　上修寬度 71.0%　三個月上修 +3.25
查核點 0／6 觸發
"""


def good_register():
    return {
        "paragraphs": [
            {"lead": "", "text": "22 檔的持股結構相近。近一年含息報酬最高的是 00981A，+155.9%，0050 為 +119.1%。"},
            {"lead": "00981A 是攻方。", "text": "遠期本益比 21.5，20 日命中率 62.5%，2025 年 7 月 15 日起贏 0050。"},
            {"lead": "00985A 是守方。", "text": "近三年最大回檔 -9.7%，0050 為 -22.3%，與攻方重疊 36.9%。"},
            {"lead": "", "text": "攻方錯在評價：遠期本益比 21.5 若跌破 14.8，贏面消失。守方錯在落後：近一年只有 +40.2%。"},
        ],
        "frozen_note": "兩檔持股加權重疊 36.9%。",
    }


def run(obj, mode="register", evidence=EVIDENCE):
    return cpt.check("active-etf", obj, evidence, mode)


def test_register_pass():
    assert run(good_register()) == []


def test_register_number_not_in_evidence_fails():
    obj = good_register()
    obj["paragraphs"][0]["text"] = "近一年含息報酬最高的是 00981A，+158.9%。"
    errs = run(obj)
    assert any("158.9" in e for e in errs)


def test_negative_sign_must_match_negative_value():
    obj = good_register()
    # 證據裡 21.5 是正值，文字寫 -21.5 不得通過
    obj["paragraphs"][1]["text"] = "遠期本益比 -21.5。"
    assert any("-21.5" in e for e in run(obj))


def test_exempt_years_codes_dates_and_fixed_terms():
    obj = good_register()
    obj["paragraphs"][0]["text"] = ("22 檔裡 00981A 與 2558.T、W52 在 2026-10-28 登記。2022 年 3 個月與 126 日不算數字。"
                                    "0050 也不算。")
    assert run(obj) == []


def test_paragraph_too_long_fails():
    obj = good_register()
    obj["paragraphs"][0]["text"] = "近一年報酬最高。" * 25
    errs = run(obj)
    assert any("超過 160 字" in e for e in errs)


def test_sentence_too_long_fails():
    obj = good_register()
    obj["paragraphs"][0]["text"] = "近一年含息報酬最高的是 00981A" + "而且" * 35 + "。"
    errs = run(obj)
    assert any("句超過 60 字" in e for e in errs)


@pytest.mark.parametrize("word", ["吹出", "煞車", "天花板", "扛", "閘門", "同一張牌"])
def test_metaphor_fails(word):
    obj = good_register()
    obj["paragraphs"][1]["text"] = f"遠期本益比 21.5，{word}。"
    errs = run(obj)
    assert any(word in e for e in errs)


def test_dash_semicolon_and_selftalk_fail():
    obj = good_register()
    obj["paragraphs"][0]["text"] = "近一年 +155.9%——很高；0050 為 +119.1%；差距明顯。值得點出。"
    errs = "\n".join(run(obj))
    assert "——" in errs and "「；」有 2 個" in errs and "值得點出" in errs


def test_not_a_b_pattern_limit():
    obj = good_register()
    obj["paragraphs"][0]["text"] = "不是看報酬，是看回檔。"
    obj["paragraphs"][1]["text"] = "不是看本益比，是看命中率。"
    errs = run(obj)
    assert any("不是 A，是 B" in e for e in errs)
    obj["paragraphs"][1]["text"] = "遠期本益比 21.5。"
    assert run(obj) == []


def test_register_needs_four_paragraphs_and_note():
    obj = good_register()
    obj["paragraphs"].pop()
    obj["frozen_note"] = ""
    errs = "\n".join(run(obj))
    assert "剛好 4 段" in errs and "frozen_note 空白" in errs


# ── review 模式 ────────────────────────────────────────────────────────────

GOOD_REVIEW = {
    "status_line": "兩檔各半相對 0050 差距見證據，查核點 0／6 觸發",
    "text": "兩檔近一年含息 +155.9% 與 +40.2%，0050 為 +119.1%。查核點 0／6 觸發。",
}


def test_review_pass():
    assert run(GOOD_REVIEW, "review") == []


def test_review_sentence_count():
    one = {"text": "兩檔近一年含息 +155.9%，0050 為 +119.1%。"}
    errs = run(one, "review")
    assert any("2～4 句" in e for e in errs)
    five = {"text": "。".join(["近一年 +155.9%"] * 5) + "。"}
    assert any("2～4 句" in e for e in run(five, "review"))


def test_review_length_and_number():
    long_ = {"text": "近一年含息 +155.9%。" + "報酬持續領先。" * 40}
    assert any("超過 220 字" in e for e in run(long_, "review"))
    bad = {"text": "近一年含息 +155.9%。0050 為 +99.9%。"}
    assert any("99.9" in e for e in run(bad, "review"))


def test_cli_exit_codes(tmp_path):
    ev = tmp_path / "ev.txt"
    ev.write_text(EVIDENCE, encoding="utf-8")
    ok = tmp_path / "ok.json"
    ok.write_text(json.dumps(good_register(), ensure_ascii=False), encoding="utf-8")
    bad_obj = good_register()
    bad_obj["paragraphs"][0]["text"] = "近一年 +158.9%。"
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(bad_obj, ensure_ascii=False), encoding="utf-8")
    script = str(ROOT / "scripts" / "check_picks_text.py")
    r_ok = subprocess.run([sys.executable, script, "--kind", "active-etf", "--text", str(ok), "--evidence", str(ev)],
                          capture_output=True, text=True)
    r_bad = subprocess.run([sys.executable, script, "--kind", "etf-dash", "--text", str(bad), "--evidence", str(ev)],
                           capture_output=True, text=True)
    assert r_ok.returncode == 0 and r_ok.stdout.startswith("PASS")
    assert r_bad.returncode != 0 and r_bad.stdout.startswith("FAIL") and "158.9" in r_bad.stdout


# ── 固定句（skill picks-monthly v1.4，2026-10-30）──────────────────────────
FIXED = cpt.FIXED_SENTENCE
DIGEST_TRIG = """## 登記 2026-10-28　狀態 tracking
  查核點 1／6 觸發
  - cp1 [untriggered] <lag> 落後｜現值：x
  - cp2 [triggered] <rev_3m> 修正低於 -10%｜現值：-12.0%
## 登記 2026-10-29　狀態 tracking
  查核點 0／5 觸發
  - cp2 [untriggered] <rev_3m> 修正｜現值：+3.0%
  - cp5 [triggered] <outflow> 流出｜現值：x
"""
EV2 = EVIDENCE + DIGEST_TRIG
BODY = "兩檔各半含息 +40.2%，0050 為 +119.1%，落後。查核點 1／6 觸發，上修寬度 71.0%。"


def rv(text, kind="etf-dash", reg_id=None):
    return cpt.check(kind, {"text": text}, EV2, "review", reg_id=reg_id)


def test_fixed_sentence_triggered_requires_it():
    assert rv(BODY + FIXED, reg_id="2026-10-28") == []
    errs = rv(BODY, reg_id="2026-10-28")
    assert any("要逐字加固定句" in e for e in errs)


def test_fixed_sentence_not_triggered_forbidden():
    errs = rv(BODY + FIXED, reg_id="2026-10-29")  # 只有 outflow 觸發，不算落後訊號
    assert any("不得出現固定句" in e for e in errs)
    assert rv(BODY, reg_id="2026-10-29") == []


def test_fixed_sentence_not_counted_in_limits():
    long_body = "兩檔各半含息 +40.2%，0050 為 +119.1%。查核點 1／6 觸發。"
    assert rv(long_body + FIXED, reg_id="2026-10-28") == []
    four = "甲 +40.2%。乙 +119.1%。丙 71.0%。丁 62.5%。"
    assert rv(four + FIXED, reg_id="2026-10-28") == []  # 4 句＋固定句仍是 4 句


def test_fixed_sentence_must_be_verbatim():
    mangled = BODY + "依本站價格與獲利研究，預估修正是落後訊號，只當資訊。"
    assert any("逐字" in e for e in rv(mangled, reg_id="2026-10-28"))
    assert any("逐字" in e for e in rv(mangled))  # 沒給 reg-id 也擋改寫


def test_fixed_sentence_without_reg_id_only_verbatim():
    assert rv(BODY + FIXED) == []
    assert rv(BODY) == []


def test_fixed_sentence_forbidden_in_active_etf_and_status_line():
    assert any("active-etf" in e for e in rv(BODY + FIXED, kind="active-etf"))
    errs = cpt.check("etf-dash", {"text": BODY, "status_line": FIXED}, EV2, "review")
    assert any("status_line" in e for e in errs)


def test_fixed_sentence_unknown_reg_fails():
    assert any("找不到登記" in e for e in rv(BODY, reg_id="2099-01-01"))


def test_fixed_sentence_legacy_digest_without_kind():
    ev = EVIDENCE + "## 登記 2026-10-28\n  - cp3 [triggered] 本益比\n"
    errs = cpt.check("etf-dash", {"text": BODY}, ev, "review", reg_id="2026-10-28")
    assert any("pe_max" in e for e in errs)
