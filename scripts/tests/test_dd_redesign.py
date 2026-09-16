"""2026-09-11：重設的失敗路徑與來源完整性回歸；所有模型呼叫皆是假執行器。"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dd_bundle
import dd_codex
import dd_project
import ddreport

FIX = Path(__file__).parent / "fixtures"


def make_run(tmp_path, monkeypatch):
    raw = json.loads((FIX / "judgment_v19_FIX.json").read_text())
    raw["facts_ref"] = str(FIX / "facts_FIX_20260911.json")
    raw["scenario_ref"] = str(tmp_path / "scenario.json")
    for name in ("prompts", "agents", "bundles", "tables"):
        (tmp_path / name).mkdir(exist_ok=True)
    for name in ("evidence", "scenario", "scenario_meta"):
        (tmp_path / (name + ".json")).write_bytes((FIX / (name + "_FIX_20260911.json")).read_bytes())
    (tmp_path / "judgment.json").write_text(json.dumps(raw, ensure_ascii=False))
    monkeypatch.setattr(ddreport, "_run_dir", lambda *a: tmp_path)
    monkeypatch.setattr(ddreport, "_pick_python", lambda: sys.executable)
    return raw


def test_shared_sources_keep_raw_digest_and_latest_transcript(tmp_path):
    transcript = tmp_path / "latest.txt"
    transcript.write_text("原文：gross margin 25.9%；Hunt $250 million。\n反方原句。")
    digest = tmp_path / "digest.json"
    data = {"unexpected": {"positive": "正面反證", "negative": "負面", "neutral": "中性"}}
    digest.write_text(json.dumps(data))
    evidence = {"numbers": {"x": 25.9}, "prior_dd": {"reason": "前判斷"}}
    author = dd_bundle._frozen_sources(tmp_path, evidence, digest, transcript)
    transcript.write_text("事後改變的原文")
    reviewer = dd_bundle._frozen_sources(tmp_path, evidence, digest, None)
    assert dd_bundle._frozen_source_parts(author) == dd_bundle._frozen_source_parts(reviewer)
    assert reviewer["digest"] == data
    assert "25.9" in reviewer["transcript"] and "$250 million" in reviewer["transcript"]
    assert "事後改變" not in reviewer["transcript"]
    with pytest.raises(ValueError, match="來源快照"):
        dd_bundle._frozen_sources(tmp_path, {"new": 1}, digest, None)


def test_declared_source_pointer_must_resolve(tmp_path):
    (tmp_path / "source_snapshot.json").write_text(json.dumps({"evidence": {"a/b": [25.9]}}))
    assert dd_bundle.source_locator_errors({"source": "evidence.json#/a~1b/0"}, tmp_path) == []
    assert dd_bundle.source_locator_errors({"source": "evidence.json#/a~1b/3"}, tmp_path)
    assert dd_bundle.source_locator_errors({"scenario": "假設成長 20%"}, tmp_path) == []


def test_missing_impact_prompt_includes_enum_and_probability_type(tmp_path, monkeypatch):
    raw = make_run(tmp_path, monkeypatch)
    raw["catalysts"][0].pop("impact", None)
    raw["thesis"]["single_thing"].pop("probability", None)
    context = ddreport._repair_schema_context(raw, "missing required key")
    assert '"enum"' in context and '"高"' in context
    assert '"probability"' in context and '"string"' in context


@pytest.mark.parametrize("patch", [
    {"$.evidence_dismissed": [{"ref": "PFAS", "reason": "原文有反證"}]},
    {"$.catalysts[0].impact": "這是一整段未評級的長句"},
    {"$.thesis.single_thing.probability": 20},
    {"$.meta.contract": "v18"},
    {"$.answers.q2_moat.verdict_values.moat.roic_durability.roiic": "缺算式"},
])
def test_invalid_patch_keeps_original_and_retains_rejected_candidate(tmp_path, monkeypatch, patch):
    make_run(tmp_path, monkeypatch)
    before = (tmp_path / "judgment.json").read_bytes()
    monkeypatch.setattr(ddreport, "_judge_check_v19", lambda *a: (False, ["ROIIC 無法複算"]))
    count, errors = ddreport._apply_patch_map(tmp_path, {"judgment": patch})
    assert count == 0 and errors
    assert (tmp_path / "judgment.json").read_bytes() == before
    assert list((tmp_path / "agents").glob("patch_candidate_*/validation.json"))


def test_real_candidate_check_accepts_valid_reason_patch(tmp_path, monkeypatch):
    raw = make_run(tmp_path, monkeypatch)
    path = "$.answers.q2_moat.reasoning"
    # 用真實計算／驗證鏈，不 mock 算術檢查。
    count, errors = ddreport._apply_patch_map(tmp_path, {"judgment": {path: raw["answers"]["q2_moat"]["reasoning"]}})
    assert count == 1, errors
    assert json.loads((tmp_path / "judgment.json").read_text())["scenario_ref"] == raw["scenario_ref"]


def test_conflicting_empty_canonical_array_does_not_drop_pfas(tmp_path, monkeypatch):
    raw = make_run(tmp_path, monkeypatch)
    raw["counter_evidence"]["evidence_dismissed"] = []
    raw["evidence_dismissed"] = [{"ref": "PFAS", "reason": "完整理由"}, {"ref": "other", "reason": "第二項"}]
    before = copy.deepcopy(raw)
    with pytest.raises(ValueError, match="衝突"):
        dd_project.normalize(raw)
    assert raw == before


def test_report_repair_budget_persists_across_resume_and_stages(tmp_path):
    assert ddreport._claim_report_repair(tmp_path, "schema")
    assert not ddreport._claim_report_repair(tmp_path, "gate")
    assert not ddreport._claim_report_repair(tmp_path, "schema_resume")
    assert json.loads((tmp_path / "repair_budget.json").read_text())["reason"] == "schema"


def test_old_repair_artifact_cannot_get_fresh_budget(tmp_path):
    (tmp_path / "agents").mkdir()
    (tmp_path / "agents/judge_fix_1.json").write_text("{}")
    assert not ddreport._claim_report_repair(tmp_path, "gate")


def test_schema_repair_then_red_gate_never_calls_second_repair(tmp_path, monkeypatch):
    make_run(tmp_path, monkeypatch)
    assert ddreport._claim_report_repair(tmp_path, "schema")
    stage = {"agent_usage": []}
    manifest = {"stages": {"gated": stage}}
    audit = tmp_path / "gate_audit.md"
    audit.write_text("## AUDIT: 判斷級🔴 = 1")
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stdout='{"red":1}', stderr=''))
    monkeypatch.setattr(ddreport, "_spawn_oneshot", lambda *a, **k: pytest.fail("不可第二次修補"))
    assert ddreport._gate_finalize_from_audit("FIX", "20260911", "gpt-5.6-sol", None, False, manifest, stage, audit) == 1
    assert "一次修補" in stage["note"]


def test_zero_red_but_missing_critical_source_does_not_pass(tmp_path, monkeypatch):
    make_run(tmp_path, monkeypatch)
    stage = {"agent_usage": []}
    manifest = {"stages": {"gated": stage}}
    audit = tmp_path / "gate_audit.md"
    audit.write_text("## AUDIT: 判斷級🔴 = 0\n## COMPLETENESS: FAIL")
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stdout='{"red":0}', stderr=''))
    assert ddreport._gate_finalize_from_audit("FIX", "20260911", "gpt-5.6-sol", None, False, manifest, stage, audit) == 1


def test_reader_content_preserves_counterevidence_and_actions(tmp_path, monkeypatch):
    raw = make_run(tmp_path, monkeypatch)
    q = raw["answers"]["q4_capital"]["verdict_values"]["quality"]
    q["financial_note"] = "財務判讀：預收影響現金流。"
    q["latest_quarter_note"] = "本季判讀：收入增加，仍須核對認列。"
    parts = dd_project.research_sections(raw, dd_project.view_for(raw, tmp_path / "judgment.json"))
    assert len(parts) == 13
    import html
    text = html.unescape("\n".join(parts.values()))
    for item in raw["counter_evidence"]["blind_spots"]:
        for key in ("evidence", "consequence", "ruling", "watch"):
            if item.get(key):
                assert item[key] in text
    assert raw["counter_evidence"]["action_conditions"]["rearm_trigger"] in text
    assert q["financial_note"] in parts["s7"] and q["latest_quarter_note"] in parts["s8"]


def test_missing_reader_sections_never_trigger_prose_model(tmp_path, monkeypatch):
    make_run(tmp_path, monkeypatch)
    monkeypatch.setattr(ddreport, "_do_prose_prepare", lambda *a: 1)
    monkeypatch.setattr(ddreport, "_spawn_short", lambda *a: pytest.fail("不可追加散文模型"))
    manifest = {"stages": {}}
    assert ddreport._do_prose_run("FIX", "20260911", manifest, dry_run=True) == 1
    assert manifest["stages"]["prose"]["agent_usage"] == []


def fake_cli(monkeypatch, failed=False, tools=False):
    def run(cmd, **kwargs):
        assert "--sandbox" in cmd and "read-only" in cmd
        assert "--ignore-user-config" in cmd
        assert "resume" not in cmd and "claude" not in cmd
        result = {"meta": {"contract": "v19"}, "body": "完整內容" * 60000}
        Path(cmd[cmd.index("--output-last-message") + 1]).write_text(json.dumps(result))
        events = [{"type": "turn.completed", "usage": {"input_tokens": 1000, "cached_input_tokens": 800,
                   "output_tokens": 500, "reasoning_output_tokens": 200}}]
        if failed:
            events = [{"type": "turn.failed", "error": {"message": "usage limit reached"}}]
        if tools:
            events.insert(0, {"type": "item.completed", "item": {"type": "command_execution"}})
        return SimpleNamespace(returncode=1 if failed else 0, stdout="\n".join(map(json.dumps, events)), stderr="")
    monkeypatch.setattr(dd_codex.subprocess, "run", run)


def test_codex_full_output_and_usage_are_not_truncated_or_double_counted(tmp_path, monkeypatch):
    fake_cli(monkeypatch)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("輸入")
    first = dd_codex.spawn(prompt, "gpt-5.6-sol", tmp_path / "judge_1.json")
    second = dd_codex.spawn(prompt, "gpt-5.6-sol", tmp_path / "judge_1.json")
    assert first["ok"] and len(first["result_text"]) > 100000
    assert first["input_tokens"] == 200 and first["cache_read"] == 800
    assert first["output_tokens"] == 500 and first["thinking_tokens"] == 200
    assert first["cost_usd"] is None
    assert first["raw_path"] != second["raw_path"]
    assert Path(first["raw_path"]).exists() and Path(second["raw_path"]).exists()


@pytest.mark.parametrize("failed,tools", [(True, False), (False, True)])
def test_failed_or_tool_using_codex_result_is_rejected(tmp_path, monkeypatch, failed, tools):
    fake_cli(monkeypatch, failed, tools)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("輸入")
    result = dd_codex.spawn(prompt, "gpt-6-astra", tmp_path / "gate_1.json")
    assert not result["ok"] and result["errors"]
    assert result["quota_exhausted"] == failed


@pytest.mark.parametrize("schema_error,gate_red,expected_calls,success", [
    (False, False, 2, True), (True, False, 3, True), (False, True, 4, True),
    (True, True, 3, False),
])
def test_complete_orchestration_call_budget(tmp_path, monkeypatch, schema_error, gate_red, expected_calls, success):
    raw = make_run(tmp_path, monkeypatch)
    (tmp_path / "facts.json").write_bytes((FIX / "facts_FIX_20260911.json").read_bytes())
    (tmp_path / "digest.json").write_text('{}')
    calls = []
    checks = []
    def check(*args):
        checks.append(1)
        return (False, "$.catalysts[0]: missing required key 'impact'") if schema_error and len(checks) == 1 else (True, "PASS")
    monkeypatch.setattr(ddreport, "_judge_check", check)
    monkeypatch.setattr(ddreport, "_validate_current_judgment", lambda *a: (True, "PASS"))
    monkeypatch.setattr(ddreport, "_apply_patch_map", lambda *a: (1, []))
    def spawn(prompt, model, out, cwd, budget):
        name = Path(prompt).name
        calls.append(name)
        if name == "b1_judge_direct.md":
            text = json.dumps(raw)
        elif "patch" in name or "fix" in name:
            text = '```json:patch\n{"judgment":{"$.oneliner":"內容"}}\n```'
        else:
            reviews = sum("g_gate" in c for c in calls)
            red = int(gate_red and reviews == 1)
            rows = ["| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |", "|---|---|---|---|---|---|"]
            for i in range(1, 9):
                rows.append("| {0} | 競爭 | {1} | 原文依據 | thesis.H[0] | 補依據 |".format(i, "🔴" if red and i == 1 else "🟢"))
            text = "## AUDIT: 判斷級🔴 = {0}\n\n{1}\n\n## COMPLETENESS: PASS".format(red, "\n".join(rows))
        return {"ok": True, "result_text": text, "over_budget": False, "cost_usd": None}
    monkeypatch.setattr(ddreport, "_spawn_oneshot", spawn)
    monkeypatch.setattr(ddreport.dd_headless, "spawn", lambda **k: pytest.fail("Codex 不得回退 Claude"))
    stage = {"state": "RUNNING", "agent_usage": []}
    manifest = {"stages": {"judged": stage}}
    assert ddreport._do_judge_full("FIX", "20260911", "gpt-5.6-sol", None, False, manifest, stage) == 0
    rc = ddreport._do_gate("FIX", "20260911", "gpt-5.6-sol", None, False, manifest)
    assert (rc == 0) == success
    assert len(calls) == expected_calls, calls


def test_unknown_codex_cost_is_not_reported_as_free():
    manifest = {"stages": {"judged": {"agent_usage": [{"cost_usd": None, "cost_available": False}]}}}
    ledger = ddreport._build_token_ledger(manifest)
    assert ledger["summary"]["cost_complete"] is False
    assert "美元費用未知" in ddreport._ledger_summary_line(ledger)


def test_new_submission_detects_missing_body_before_model_review(tmp_path, monkeypatch):
    make_run(tmp_path, monkeypatch)
    (tmp_path / "manifest.json").write_text('{"render_mode":"research_fields"}')
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: pytest.fail("正文缺失應先擋下"))
    ok, errors = ddreport._judge_check_v19(tmp_path, tmp_path / "judgment.json", tmp_path / "evidence.json", tmp_path / "tables", sys.executable)
    assert not ok and "financial_note" in "\n".join(errors)


def test_direct_research_assembles_real_template_and_tables(tmp_path, monkeypatch):
    import render_dd
    raw = make_run(tmp_path, monkeypatch)
    quality = raw["answers"]["q4_capital"]["verdict_values"]["quality"]
    # 僅為離線排版 fixture 複用既有文字，不能把此產物當真實研究報告。
    quality["financial_note"] = raw["answers"]["q4_capital"]["reasoning"]
    quality["latest_quarter_note"] = raw["answers"]["q3_growth"]["reasoning"]
    (tmp_path / "judgment.json").write_text(json.dumps(raw, ensure_ascii=False))
    assert ddreport._do_prose_prepare("FIX", "20260911") == 0
    page = render_dd.assemble_from_parts_v19(tmp_path / "prose", tmp_path / "tables", judgment_path=tmp_path / "judgment.json")
    assert 'name="dd-layout" content="v19"' in page
    for sid in ("s1", "s7", "s8", "s12", "decision", "appB"):
        assert 'id="' + sid + '"' in page
    assert "三到四年財務表" in page
    assert not (tmp_path / "prompts/b2_prose.md").exists()


def test_failed_render_never_overwrites_public_page(tmp_path, monkeypatch):
    make_run(tmp_path, monkeypatch)
    public = tmp_path / "public"
    public.mkdir()
    target = public / "DD_FIX_20260911.html"
    target.write_text("既有合格頁面")
    monkeypatch.setattr(ddreport, "DD_DIR", public)
    monkeypatch.setattr(ddreport, "_do_prose_prepare", lambda *a: 0)
    def reject(*a, **k):
        Path(k["out_html"]).write_text("不合格候選")
        return False, [("s7", "缺財務資料")]
    monkeypatch.setattr(ddreport, "_run_gates", reject)
    assert ddreport._do_prose_run("FIX", "20260911", {"stages": {}}, dry_run=False) == 1
    assert target.read_text() == "既有合格頁面"
