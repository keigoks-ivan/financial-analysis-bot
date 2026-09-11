"""2026-09-11：簡化後的資料完整性、分類原意與最終版本驗收，全部不呼叫模型。"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dd_bundle
import ddreport


def _run(tmp_path, monkeypatch):
    monkeypatch.setattr(ddreport, "_run_dir", lambda *a: tmp_path)
    monkeypatch.setattr(ddreport, "_pick_python", lambda: sys.executable)
    for folder in ("prompts", "agents", "bundles"):
        (tmp_path / folder).mkdir(exist_ok=True)
    for name in ("evidence", "digest", "facts", "scenario", "scenario_meta"):
        (tmp_path / (name + ".json")).write_text('{}')
    (tmp_path / "judgment.json").write_text(json.dumps({"decision_out": {"verdict": "觀望"}}))
    audit = tmp_path / "gate_audit.md"
    audit.write_text("審核內容")
    stage = {"state": "RUNNING", "agent_usage": [],
             "input_signature": ddreport._gate_input_signature(tmp_path),
             "audit_sha256": hashlib.sha256(audit.read_bytes()).hexdigest()}
    manifest = {"stages": {"gated": stage}}
    return stage, manifest, audit


@pytest.mark.parametrize("name", ["judgment", "evidence", "facts", "digest", "scenario", "scenario_meta"])
def test_resume_cannot_reuse_audit_after_any_input_changes(tmp_path, monkeypatch, name):
    stage, manifest, audit = _run(tmp_path, monkeypatch)
    assert ddreport._gate_audit_is_current(tmp_path, stage)
    p = tmp_path / (name + ".json")
    value = json.loads(p.read_text())
    value["reason"] = "新證據；裁決維持觀望"
    p.write_text(json.dumps(value))
    calls = []
    monkeypatch.setattr(ddreport, "_do_gate", lambda *a, **k: calls.append("review") or 7)
    assert ddreport._resume_gate_stage("FIX", "20260911", "fable", None, False, manifest) == 7
    assert calls == ["review"]


def test_changed_audit_or_missing_stamp_is_not_current(tmp_path, monkeypatch):
    stage, manifest, audit = _run(tmp_path, monkeypatch)
    audit.write_text("人工改成零紅燈")
    assert not ddreport._gate_audit_is_current(tmp_path, stage)
    assert not ddreport._gate_audit_is_current(tmp_path, {})


def test_zero_red_does_not_override_invalid_final_judgment(tmp_path, monkeypatch):
    stage, manifest, audit = _run(tmp_path, monkeypatch)
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k:
                        SimpleNamespace(returncode=0, stdout='{"red":0}', stderr=''))
    monkeypatch.setattr(ddreport, "_validate_current_judgment", lambda p: (False, "4 FAIL"))
    assert ddreport._gate_finalize_from_audit(
        "FIX", "20260911", "fable", None, False, manifest, stage, audit) == 1
    assert stage["state"] == "FAIL"
    assert stage["patch_check_tail"] == "4 FAIL"


def test_same_verdict_patch_is_reviewed_once_then_stops_if_still_red(tmp_path, monkeypatch):
    stage, manifest, audit = _run(tmp_path, monkeypatch)
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k:
                        SimpleNamespace(returncode=0, stdout='{"red":1}', stderr=''))
    monkeypatch.setattr(ddreport, "_gate_patch_mode", lambda: "patchmap")
    monkeypatch.setattr(ddreport, "_spawn_oneshot", lambda *a, **k:
                        {"ok": True, "result_text": "patch"})
    monkeypatch.setattr(ddreport, "_parse_patch_map", lambda text: {"reason": "new"})
    monkeypatch.setattr(ddreport, "_apply_patch_map", lambda *a: (1, []))
    monkeypatch.setattr(ddreport, "_judge_check", lambda *a: (True, "PASS"))
    reviews = []
    monkeypatch.setattr(ddreport, "_do_gate", lambda *a, **k: reviews.append(k["_depth"]) or 0)
    assert ddreport._gate_finalize_from_audit(
        "FIX", "20260911", "fable", None, False, manifest, stage, audit) == 0
    assert reviews == [1]
    monkeypatch.setattr(ddreport, "_spawn_oneshot", lambda *a, **k: pytest.fail("不得無限修補"))
    assert ddreport._gate_finalize_from_audit(
        "FIX", "20260911", "fable", None, False, manifest, stage, audit, _depth=1) == 1


def test_original_evidence_keeps_nested_values_and_positive_counterevidence():
    evidence = {"numbers": {"kpi": {"value": 1, "prior_quarter": 2, "sbc_share": 2.74}},
                "prior_dd": {"rearm_trigger": "原有門檻"},
                "coverage": {"tariff": {"direction": "+", "claim": "反駁偏空假設"}}}
    section = dd_bundle._source_evidence_section(evidence)
    block = section.split('```json\n', 1)[1].split('```', 1)[0]
    assert json.loads(block) == evidence


def test_final_check_uses_actual_output_and_rejects_stale_gate(tmp_path, monkeypatch):
    stage, manifest, audit = _run(tmp_path, monkeypatch)
    (tmp_path / "judgment.json").write_text('{"meta":{"contract":"v19"}}')
    target = tmp_path / "actual-final.html"
    target.write_text('<meta name="dd-layout" content="v19">')
    monkeypatch.setattr(ddreport, "_validate_current_judgment", lambda p: (True, ""))
    seen = []
    monkeypatch.setattr(ddreport, "_v19_structure_findings",
                        lambda p, html: seen.append(html) or [("appC", "附錄內部用語")])
    findings = ddreport._final_v19_findings(tmp_path, target, manifest)
    assert seen == [target]
    assert {x[0] for x in findings} == {"_gate", "appC"}


def test_failed_new_review_cannot_pick_up_old_audit(tmp_path, monkeypatch):
    stage, manifest, audit = _run(tmp_path, monkeypatch)
    (tmp_path / "bundles/gate.md").write_text("新審核包")
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k:
                        SimpleNamespace(returncode=0, stdout='', stderr=''))
    monkeypatch.setattr(ddreport.dd_headless, "spawn", lambda **k: {"ok": False})
    assert ddreport._do_gate("FIX", "20260911", "fable", None, False, manifest) == 1
    assert not audit.exists()
    assert stage["state"] == "FAIL"


def test_quick_report_keeps_judgment_checks_without_full_layout_requirement(tmp_path, monkeypatch):
    stage, manifest, audit = _run(tmp_path, monkeypatch)
    (tmp_path / "judgment.json").write_text('{"meta":{"contract":"v19"}}')
    stage["input_signature"] = ddreport._gate_input_signature(tmp_path)
    stage["state"] = "PASS"
    quick = tmp_path / "brief.html"
    quick.write_text("<html>快速版</html>")
    monkeypatch.setattr(ddreport, "_validate_current_judgment", lambda p: (True, ""))
    monkeypatch.setattr(ddreport, "_v19_structure_findings", lambda *a: pytest.fail("快速版不套完整版面"))
    assert ddreport._final_v19_findings(tmp_path, quick, manifest) == []
    monkeypatch.setattr(ddreport, "_validate_current_judgment", lambda p: (False, "數字錯誤"))
    assert ddreport._final_v19_findings(tmp_path, quick, manifest) == [("_judgment", "數字錯誤")]
