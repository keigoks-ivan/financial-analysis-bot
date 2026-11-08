"""修補把說明寫進 endo_ceiling 時不該整份作廢。2026-11-03 MPWR、2026-11-08 NET 案。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dd2"))
import run  # noqa: E402

BASE = "$.answers.q2_moat.verdict_values.moat.roic_durability"
CEIL = BASE + ".endo_ceiling"
NOTE = BASE + ".formula_note"


def test_text_moves_to_note_and_ceiling_is_null():
    patches = {"judgment": {CEIL: "不給單一數字，只列可複算的兩端。"}}
    notes = run._normalize_endo_ceiling_patch(patches)
    assert patches["judgment"] == {CEIL: None, NOTE: "不給單一數字，只列可複算的兩端。"}
    assert "formula_note" in notes[0]


def test_text_is_appended_to_note_in_same_patch():
    patches = {"judgment": {CEIL: "兩年上限約 35.8%。", NOTE: "公式不適用。"}}
    run._normalize_endo_ceiling_patch(patches)
    assert patches["judgment"][NOTE] == "公式不適用；兩年上限約 35.8%。"
    assert patches["judgment"][CEIL] is None


def test_plain_number_text_becomes_number():
    for raw in ("18.5", "18.5%", " 18.5 ％"):
        patches = {"judgment": {CEIL: raw}}
        run._normalize_endo_ceiling_patch(patches)
        assert patches["judgment"] == {CEIL: 18.5}


def test_whole_object_form():
    value = {"checkpoints": [], "roiic": "x", "reinvest_rate": "y", "endo_ceiling": "算不出來", "formula_note": None}
    patches = {"judgment": {BASE: value}}
    run._normalize_endo_ceiling_patch(patches)
    assert value["endo_ceiling"] is None
    assert value["formula_note"] == "算不出來"


def test_numbers_null_and_other_paths_untouched():
    jp = {CEIL: 18.5, "$.answers.q1_business.reasoning": "endo_ceiling 文字", BASE + ".roiic": "約 30%"}
    patches = {"judgment": dict(jp)}
    assert run._normalize_endo_ceiling_patch(patches) == []
    assert patches["judgment"] == jp
    patches = {"judgment": {CEIL: None}}
    assert run._normalize_endo_ceiling_patch(patches) == []
