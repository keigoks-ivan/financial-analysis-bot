#!/usr/bin/env python3
"""2026-09-14：市場問題板驗證、證據漂移與期限重評測試。"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import market_questions as questions  # noqa: E402
import market_refresh as refresh  # noqa: E402


def _state(as_of="2026-09-13", used=100.0, unused=20.0):
    return {"schema": "market-state-v1", "as_of": as_of, "freshness": [], "evidence": {"quotes": {
        "used": {"label": "已引用", "num": used, "as_of": as_of, "unit": "index"},
        "unused": {"label": "未引用", "num": unused, "as_of": as_of, "unit": "percent"},
    }}}


def _snapshot(as_of="2026-09-13", used=100.0, unused=20.0):
    return refresh.make_snapshot(_state(as_of, used, unused), {})


def _board(anchor, by="2026-09-20"):
    quote = copy.deepcopy(anchor["state"]["evidence"]["quotes"]["used"])
    board = {
        "schema": "market-question-board-v1", "as_of": anchor["state"]["as_of"],
        "snapshot_id": anchor["snapshot_id"], "summary": "仍待驗證。", "author_model": "writer",
        "questions": [{
            "id": "q1", "title": "是否延續？", "assessment": "暫時成立。",
            "main_explanation": "已知證據支持，但反證仍在。", "alternative_explanations": ["也可能是短期雜訊。"],
            "supports": [{"ref": "used", "note": "數值支持。"}],
            "opposes": [{"ref": "used", "note": "同一數值亦有反向解釋。"}],
            "unexplained": ["持續性未知。"], "priced_in": {"known": "市場已知。", "unknown": "期限未知。"},
            "next_checks": [{"watch": "更新值", "if_seen": "提高信心", "if_absent": "降低信心", "by": by}],
            "confidence": "中等", "independence_note": "獨立核對。",
        }],
        "evidence_snapshot": {"quotes": {"used": quote}},
        "editorial_review": {"model": "reviewer", "verdict": "pass"},
    }
    board["editorial_review"]["content_hash"] = questions.board_hash(board)
    return board


def _save(data_dir, snapshot, board):
    refresh.atomic_json(data_dir / "snapshots" / (snapshot["snapshot_id"] + ".json"), snapshot)
    refresh.atomic_json(data_dir / "questions.json", board)


def test_valid_board_and_hash_detects_authored_change():
    anchor = _snapshot()
    board = _board(anchor)
    assert questions.validate_board(board, anchor) == []
    board["summary"] = "正文已修改。"
    assert any("內容版本不同" in error for error in questions.validate_board(board, anchor))


def test_invalid_ref_and_nonfinite_value_are_blocked():
    anchor = _snapshot()
    board = _board(anchor)
    board["questions"][0]["supports"][0]["ref"] = "missing"
    board["evidence_snapshot"]["quotes"] = {"missing": {"num": float("nan")}}
    assert questions.validate_board(board, anchor, require_review=False)


def test_due_date_and_referenced_change_need_review_but_unreferenced_change_does_not(tmp_path):
    anchor = _snapshot()
    board = _board(anchor, by="2026-09-14")
    _save(tmp_path, anchor, board)

    unchanged_refs = _snapshot("2026-09-13", unused=99.0)
    assert questions.load_question_board(tmp_path, unchanged_refs)["review"]["status"] == "current"

    changed_ref = _snapshot("2026-09-13", used=101.0)
    changed = questions.load_question_board(tmp_path, changed_ref)["review"]
    assert changed["status"] == "needs_review"
    assert any("已有變動" in reason for reason in changed["reasons"])

    due = _snapshot("2026-09-14")
    due_review = questions.load_question_board(tmp_path, due)["review"]
    assert any("期限已到" in reason for reason in due_review["reasons"])


def test_load_does_not_mutate_authored_board_and_missing_board_is_compatible(tmp_path):
    anchor = _snapshot()
    board = _board(anchor)
    _save(tmp_path, anchor, board)
    before = json.loads((tmp_path / "questions.json").read_text(encoding="utf-8"))
    loaded = questions.load_question_board(tmp_path, anchor)
    assert loaded["review"]["status"] == "current"
    assert loaded["review"]["reason"] == ""
    assert loaded["review"]["changed_refs"] == []
    assert json.loads((tmp_path / "questions.json").read_text(encoding="utf-8")) == before
    assert questions.load_question_board(tmp_path / "empty", anchor) is None


def test_tampered_anchor_snapshot_is_rejected(tmp_path):
    anchor = _snapshot()
    board = _board(anchor)
    _save(tmp_path, anchor, board)
    path = tmp_path / "snapshots" / (anchor["snapshot_id"] + ".json")
    saved = json.loads(path.read_text(encoding="utf-8"))
    saved["state"]["evidence"]["quotes"]["used"]["num"] = 999.0
    path.write_text(json.dumps(saved), encoding="utf-8")
    with pytest.raises(ValueError, match="歷史證據版本驗證失敗"):
        questions.load_question_board(tmp_path, anchor)


def test_malformed_rows_dates_and_blocking_review_are_rejected():
    anchor = _snapshot()
    board = _board(anchor)
    board["as_of"] = "2026-09-12"
    board["questions"][0]["next_checks"] = [None]
    board["editorial_review"]["findings"] = [{"severity": "red"}]
    errors = questions.validate_board(board, anchor)
    assert any("早於綁定證據" in error for error in errors)
    assert any("next_check" in error for error in errors)
    assert any("阻斷" in error for error in errors)


def test_only_referenced_staleness_blocks_and_unrelated_freshness_is_advisory(tmp_path):
    anchor = _snapshot("2026-09-01")
    board = _board(anchor, by="2026-10-01")
    _save(tmp_path, anchor, board)
    advisory = copy.deepcopy(anchor)
    advisory["state"]["freshness"] = [{"pipeline": "未引用來源", "status": "stale"}]
    advisory_loaded = questions.load_question_board(tmp_path, advisory)
    assert advisory_loaded["review"]["status"] == "current"
    assert advisory_loaded["review"]["quality_notes"] == ["未引用來源：stale"]
    current = _snapshot("2026-09-09")
    current["state"]["freshness"] = [{"pipeline": "未引用來源", "status": "stale"}]
    loaded = questions.load_question_board(tmp_path, current)
    assert loaded["review"]["status"] == "needs_review"
    assert loaded["review"]["changed_refs"] == ["used"]
    assert loaded["review"]["quality_notes"] == ["未引用來源：stale"]


def test_cli_validates_without_saving(tmp_path):
    anchor = _snapshot()
    board = _board(anchor)
    _save(tmp_path, anchor, board)
    candidate = tmp_path / "candidate.json"
    candidate.write_text(json.dumps(board, ensure_ascii=False), encoding="utf-8")
    before = (tmp_path / "questions.json").read_text(encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPTS / "market_questions.py"), "validate",
                             "--candidate", str(candidate), "--data-dir", str(tmp_path)],
                            check=False, capture_output=True, text=True)
    assert result.returncode == 0
    assert json.loads(result.stdout)["status"] == "validated"
    assert (tmp_path / "questions.json").read_text(encoding="utf-8") == before


def test_cli_rejects_tampered_anchor(tmp_path):
    anchor = _snapshot()
    board = _board(anchor)
    _save(tmp_path, anchor, board)
    candidate = tmp_path / "candidate.json"
    candidate.write_text(json.dumps(board, ensure_ascii=False), encoding="utf-8")
    anchor_path = tmp_path / "snapshots" / (anchor["snapshot_id"] + ".json")
    tampered = json.loads(anchor_path.read_text(encoding="utf-8"))
    tampered["state"]["evidence"]["quotes"]["used"]["num"] = 999.0
    anchor_path.write_text(json.dumps(tampered), encoding="utf-8")

    result = subprocess.run([sys.executable, str(SCRIPTS / "market_questions.py"), "validate",
                             "--candidate", str(candidate), "--data-dir", str(tmp_path)],
                            check=False, capture_output=True, text=True)

    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "blocked"
    assert "歷史證據版本驗證失敗" in result.stdout
