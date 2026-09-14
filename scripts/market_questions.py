#!/usr/bin/env python3
"""2026-09-14：驗證市場待驗證問題板，並依新證據派生重評狀態。"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from datetime import date
from pathlib import Path


def _encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def board_hash(board):
    # 2026-09-14：編輯冷讀綁研究正文；派生狀態與冷讀本身不進正文雜湊。
    body = {key: value for key, value in board.items() if key not in ("editorial_review", "review")}
    return hashlib.sha256(_encoded(body).encode("utf-8")).hexdigest()


def _day(value):
    try:
        return date.fromisoformat(value) if isinstance(value, str) else None
    except ValueError:
        return None


def _walk_finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        return False
    if isinstance(value, dict):
        return all(_walk_finite(item) for item in value.values())
    if isinstance(value, list):
        return all(_walk_finite(item) for item in value)
    return True


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _snapshot_quotes(snapshot):
    state = snapshot.get("state", snapshot) if isinstance(snapshot, dict) else {}
    return ((state.get("evidence") or {}).get("quotes") or {}) if isinstance(state, dict) else {}


def _snapshot_digest(snapshot):
    payload = {"state": {key: value for key, value in snapshot["state"].items()
                         if key not in ("generated_at", "read_headline", "read_as_of")}, "intel": snapshot["intel"]}
    def evidence_only(value):
        if isinstance(value, dict):
            return {key: evidence_only(item) for key, item in value.items()
                    if key not in ("generated_at", "last_attempt_at", "last_success_at", "added_revisions", "observation_age_days")}
        if isinstance(value, list):
            return [evidence_only(item) for item in value]
        return value
    if snapshot["state"].get("source_research"):
        research = evidence_only(snapshot["state"]["source_research"])
        research.pop("as_of", None)
        payload["state"]["source_research"] = research
    return hashlib.sha256(_encoded(payload).encode("utf-8")).hexdigest()


def _referenced_refs(board):
    refs = set()
    for question in board.get("questions") or []:
        if not isinstance(question, dict):
            continue
        for side in ("supports", "opposes"):
            refs.update(row.get("ref") for row in question.get(side) or []
                        if isinstance(row, dict) and _text(row.get("ref")))
    return refs


def validate_board(board, anchor_snapshot, require_review=True):
    """Return validation errors for an authored board anchored to one immutable snapshot."""
    errors = []
    if not isinstance(board, dict) or not _walk_finite(board):
        return ["問題板格式錯誤或含非有限數值"]
    if board.get("schema") != "market-question-board-v1":
        errors.append("問題板 schema 錯誤")
    as_of = _day(board.get("as_of"))
    if as_of is None:
        errors.append("問題板 as_of 必須是 ISO 日期")
    anchor_day = _day((anchor_snapshot.get("state", anchor_snapshot) or {}).get("as_of"))
    if as_of and anchor_day and as_of < anchor_day:
        errors.append("問題板日期不可早於綁定證據日期")
    snapshot_id = board.get("snapshot_id")
    if (not isinstance(snapshot_id, str) or len(snapshot_id) != 64
            or any(char not in "0123456789abcdef" for char in snapshot_id)
            or snapshot_id != anchor_snapshot.get("snapshot_id")):
        errors.append("問題板未綁定指定證據版本")
    if not _text(board.get("summary")) or not _text(board.get("author_model")):
        errors.append("問題板缺少摘要或作者模型")
    questions = board.get("questions")
    if not isinstance(questions, list) or not questions:
        errors.append("問題板至少需要一題")
        questions = []
    ids = [row.get("id") for row in questions if isinstance(row, dict)]
    if len(ids) != len(set(ids)) or any(not _text(item) for item in ids):
        errors.append("問題 id 必須存在且唯一")
    for row in questions:
        if not isinstance(row, dict):
            errors.append("問題格式錯誤")
            continue
        required_text = ("id", "title", "assessment", "main_explanation", "confidence", "independence_note")
        if any(not _text(row.get(key)) for key in required_text):
            errors.append("問題缺少必要文字欄位：" + str(row.get("id")))
        alternatives = row.get("alternative_explanations")
        if not isinstance(alternatives, list) or not alternatives or any(not _text(item) for item in alternatives):
            errors.append("每題至少需要一個替代解釋：" + str(row.get("id")))
        for side in ("supports", "opposes"):
            items = row.get(side)
            if not isinstance(items, list) or not items or any(
                    not isinstance(item, dict) or not _text(item.get("ref")) or not _text(item.get("note"))
                    for item in (items or [])):
                errors.append("每題需有完整支持與反對證據：" + str(row.get("id")))
        if not isinstance(row.get("unexplained"), list) or any(not _text(item) for item in row.get("unexplained") or []):
            errors.append("unexplained 必須是文字陣列：" + str(row.get("id")))
        priced = row.get("priced_in")
        if not isinstance(priced, dict) or any(not _text(priced.get(key)) for key in ("known", "unknown")):
            errors.append("priced_in 需含 known 與 unknown：" + str(row.get("id")))
        checks = row.get("next_checks")
        if not isinstance(checks, list) or not checks:
            errors.append("每題至少需要一個 next_check：" + str(row.get("id")))
        for check in checks or []:
            if not isinstance(check, dict):
                errors.append("next_check 欄位或日期錯誤：" + str(row.get("id")))
                continue
            check_day = _day(check.get("by"))
            if any(not _text(check.get(key)) for key in ("watch", "if_seen", "if_absent")) or check_day is None:
                errors.append("next_check 欄位或日期錯誤：" + str(row.get("id")))
            elif as_of and check_day < as_of:
                errors.append("next_check 截止日不可早於問題板日期：" + str(row.get("id")))
    anchor_quotes = _snapshot_quotes(anchor_snapshot)
    saved_quotes = ((board.get("evidence_snapshot") or {}).get("quotes") or {})
    if not isinstance(saved_quotes, dict):
        errors.append("問題板缺少 evidence_snapshot.quotes")
        saved_quotes = {}
    for ref in sorted(ref for ref in _referenced_refs(board) if ref):
        if ref not in anchor_quotes:
            errors.append("引用不存在於證據版本：" + ref)
        elif ref not in saved_quotes or saved_quotes.get(ref) != anchor_quotes.get(ref):
            errors.append("引用的完整數值、日期或單位與證據不同：" + ref)
    if set(saved_quotes) != _referenced_refs(board):
        errors.append("evidence_snapshot.quotes 必須恰好保存全部引用")
    review = board.get("editorial_review") or {}
    if require_review and (review.get("verdict") != "pass" or not _text(review.get("model"))
                           or review.get("model") == board.get("author_model")):
        errors.append("需要不同模型完成編輯冷讀且通過")
    if require_review and review.get("content_hash") != board_hash(board):
        errors.append("編輯冷讀內容版本不同，修改正文後必須重新冷讀")
    for finding in review.get("findings") or []:
        if isinstance(finding, dict) and (finding.get("severity") in ("🔴", "red") or finding.get("blocking") is True):
            errors.append("編輯冷讀仍有阻斷問題")
    return errors


def _quote_expired(quote, current_day):
    if not isinstance(quote, dict):
        return True
    if quote.get("stale") is True or quote.get("status") == "stale":
        return True
    observed = _day(quote.get("as_of"))
    if observed is None or current_day is None:
        return True
    frequency = str(quote.get("frequency", "daily")).lower()
    limits = {"daily": 7, "day": 7, "weekly": 10, "week": 10,
              "monthly": 45, "month": 45, "quarterly": 120, "quarter": 120}
    return (current_day - observed).days > limits.get(frequency, 7)


def derive_review(board, current_snapshot):
    reasons = []
    changed_refs = []
    current = _snapshot_quotes(current_snapshot)
    saved = ((board.get("evidence_snapshot") or {}).get("quotes") or {})
    current_state = current_snapshot.get("state", current_snapshot) or {}
    current_day = _day(current_state.get("as_of"))
    for ref in sorted(_referenced_refs(board)):
        if ref not in current:
            reasons.append("引用證據已缺失：" + ref)
            changed_refs.append(ref)
        elif current[ref] != saved.get(ref):
            reasons.append("引用證據已有變動：" + ref)
            changed_refs.append(ref)
        if ref in current and _quote_expired(current[ref], current_day):
            reasons.append("引用證據已過期：" + ref)
            if ref not in changed_refs:
                changed_refs.append(ref)
    due = sorted({check.get("by") for row in board.get("questions") or [] for check in row.get("next_checks") or []
                  if _day(check.get("by")) and current_day and _day(check.get("by")) <= current_day})
    if due:
        reasons.append("下一次檢查期限已到：" + "、".join(due))
    quality_notes = [str(row.get("pipeline", "來源")) + "：" + str(row.get("status"))
                     for row in current_state.get("freshness") or []
                     if isinstance(row, dict) and row.get("status") in ("stale", "warn")]
    return {"status": "needs_review" if reasons else "current", "reason": "；".join(reasons),
            "reasons": reasons, "changed_refs": changed_refs, "quality_notes": quality_notes}


def load_question_board(data_dir, current_snapshot, require_review=True):
    """Load and validate questions.json without changing its authored content."""
    path = Path(data_dir) / "questions.json"
    if not path.exists():
        return None
    board = json.loads(path.read_text(encoding="utf-8"))
    snapshot_id = board.get("snapshot_id") if isinstance(board, dict) else None
    if (not isinstance(snapshot_id, str) or len(snapshot_id) != 64
            or any(char not in "0123456789abcdef" for char in snapshot_id)):
        raise ValueError("問題板 snapshot_id 格式錯誤")
    anchor_path = Path(data_dir) / "snapshots" / (str(snapshot_id) + ".json")
    if not anchor_path.exists():
        raise ValueError("問題板找不到綁定的歷史證據版本")
    anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
    # 2026-09-14：在本模組重算快照正文 hash，避免反向 import refresh 形成循環。
    if _snapshot_digest(anchor) != snapshot_id:
        raise ValueError("問題板綁定的歷史證據版本驗證失敗")
    errors = validate_board(board, anchor, require_review=require_review)
    board_day = _day(board.get("as_of"))
    current_day = _day((current_snapshot.get("state", current_snapshot) or {}).get("as_of"))
    if board_day and current_day and board_day > current_day:
        errors.append("問題板日期不可晚於目前市場日期")
    if errors:
        raise ValueError("問題板驗證失敗：" + "；".join(errors))
    result = copy.deepcopy(board)
    result["review"] = derive_review(board, current_snapshot)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=("validate",))
    ap.add_argument("--candidate", type=Path, required=True)
    ap.add_argument("--data-dir", type=Path, required=True)
    args = ap.parse_args()
    try:
        board = json.loads(args.candidate.read_text(encoding="utf-8"))
        snapshot_id = board.get("snapshot_id") if isinstance(board, dict) else None
        if (not isinstance(snapshot_id, str) or len(snapshot_id) != 64
                or any(char not in "0123456789abcdef" for char in snapshot_id)):
            raise ValueError("問題板 snapshot_id 格式錯誤")
        anchor_path = args.data_dir / "snapshots" / (snapshot_id + ".json")
        anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
        if _snapshot_digest(anchor) != snapshot_id:
            raise ValueError("問題板綁定的歷史證據版本驗證失敗")
        errors = validate_board(board, anchor)
        print(_encoded({"status": "blocked" if errors else "validated", "errors": errors}))
        return 1 if errors else 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(_encoded({"status": "blocked", "errors": [str(exc)]}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
