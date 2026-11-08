"""修補輪的 contradictions 索引要跟著預留狀態換位置。2026-11-08 FICO／WLDN／AMD 案。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dd2"))
import run  # noqa: E402

MA = {"axis": "[程式歸因]均線", "prior_field": ["ma"]}
VERDICT = {"axis": "[程式歸因]裁決", "prior_field": ["dca_verdict"]}
ROLE = {"axis": "[程式歸因]角色", "prior_field": ["dca_role"]}
MERGED = {"axis": "[程式歸因]裁決與角色（預留）", "prior_field": ["dca_verdict", "dca_role"]}
PROB = {"axis": "機率變動", "prior_field": ["p_bull_pct"]}
REARM = {"axis": "重新評估條件", "prior_field": ["rearm_trigger"]}

BEFORE = [MA, VERDICT, ROLE, PROB, REARM]
AFTER = [MA, MERGED, PROB, REARM]


def _path(i, tail=""):
    return "$.counter_evidence.contradictions[{0}]{1}".format(i, tail)


def test_index_follows_entry_after_merge():
    patches = {"judgment": {_path(3): {"axis": "機率變動（修）"}}}
    notes = run._remap_contradiction_patch_paths(patches, BEFORE, AFTER)
    assert list(patches["judgment"]) == [_path(2)]  # 寫到機率條目，不是照舊索引蓋掉 rearm_trigger
    assert notes == ["contradictions[3] → [2]"]


def test_subpath_is_kept():
    patches = {"judgment": {_path(4, ".cause"): "新證據"}}
    run._remap_contradiction_patch_paths(patches, BEFORE, AFTER)
    assert patches["judgment"] == {_path(3, ".cause"): "新證據"}


def test_program_entry_missing_after_rebuild_is_dropped():
    patches = {"judgment": {_path(1): {"axis": "改裁決條目"}}}
    notes = run._remap_contradiction_patch_paths(patches, BEFORE, AFTER)
    assert patches["judgment"] == {}
    assert "修補丟棄" in notes[0]


def test_entry_changed_in_rebuild_matches_by_axis():
    stripped = dict(PROB, prior_field=[])
    patches = {"judgment": {_path(3): {"axis": "機率變動（修）"}}}
    run._remap_contradiction_patch_paths(patches, BEFORE, [MA, MERGED, stripped, REARM])
    assert list(patches["judgment"]) == [_path(2)]


def test_other_paths_and_same_order_untouched():
    patches = {"judgment": {"$.answers.q1_business.reasoning": "x", _path(0): {"axis": "均線（修）"}}}
    notes = run._remap_contradiction_patch_paths(patches, BEFORE, BEFORE)
    assert set(patches["judgment"]) == {"$.answers.q1_business.reasoning", _path(0)}
    assert notes == []
