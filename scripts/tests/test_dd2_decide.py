#!/usr/bin/env python3
"""測試 `scripts/dd2/decide.py`（DD 閘機械化第一批：A／B／C／H 四類，README §8k）。

離線測（不打真實 `claude` 子行程）：
- `expand_A`／`expand_B`／`expand_C`／`expand_H` 對 `.dd_build/runs/
  MU_20260917/` 的真實 judgment.json／facts.json 展開，核對設計稿驗收條件
  （README §8k「A 類必須抓到 R4」「B 類必須抓到 $750 路徑與 rearm 第二腿」）。
- `expand_C` 用合成 fixture 驗證「負向且未被引用」的偵測規則（三檔真實樣本
  全部已被引用，展開結果剛好是 0 題，合成 fixture 才驗得到偵測邏輯本身）。
- `apply_decisions` 用假答案驗四類分流與 0.95／0.70 門檻邊界，含 A 類命中時
  的 `triggered_by_evidence` 覆寫與 `scenario.json` bull／base 機率調整。
- `decide_batch` monkeypatch `spawn.oneshot_stream`，驗參數組裝（`--effort`／
  `--json-schema` 進 `extra_args`）、答案驗證（`answer` 不在 `options` 內時
  `valid=False`／`confidence` 強制歸零）、漏答補位。
- `_extract_answers` 對 `structured_output`（dict／list 兩種形狀）與純文字
  `result_text` 三種輸入。
- TSM_20260916／TXN_20260916 離線展開一次，只印題數（README §8k 要求）。

Python 3.9 相容（不用 `match`、不用 `X | None`）。
"""
import json
import shutil
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))

import decide  # noqa: E402
import spawn as dd2_spawn  # noqa: E402

FIXTURE_RUN_DIR = REPO_ROOT / ".dd_build" / "runs" / "MU_20260917"
TSM_RUN_DIR = REPO_ROOT / ".dd_build" / "runs" / "TSM_20260916"
TXN_RUN_DIR = REPO_ROOT / ".dd_build" / "runs" / "TXN_20260916"


@pytest.fixture()
def run_dir(tmp_path):
    dst = tmp_path / FIXTURE_RUN_DIR.name
    shutil.copytree(FIXTURE_RUN_DIR, dst)
    return dst


def _judgment_facts(rd):
    return decide._load_json(rd / "judgment.json"), decide._load_json(rd / "facts.json")


# ---------------------------------------------------------------------------
# expand_A：MU 真實 judgment，必須抓到 R4（HBM4 <15%），context 含
# customer_second_source#1 原文
# ---------------------------------------------------------------------------

def test_expand_a_finds_r4_with_customer_second_source_context(run_dir):
    judgment, facts = _judgment_facts(run_dir)
    questions = decide.expand_A(judgment, facts)
    r4_qs = [q for q in questions if q["_r_id"] == "R4"]
    assert len(r4_qs) == 1
    q = r4_qs[0]
    assert q["kind"] == "noul"
    assert q["options"] == ["是", "否"]
    assert "customer_second_source#1" in q["context"]
    assert "15%" in q["_threshold"]


def test_expand_a_only_covers_r_items_with_threshold_and_resolvable_refs(run_dir):
    judgment, facts = _judgment_facts(run_dir)
    questions = decide.expand_A(judgment, facts)
    # MU 四條 R 都有 threshold 且 evidence_refs 全部可在 findings_digest 找到
    assert [q["_r_id"] for q in questions] == ["R1", "R2", "R3", "R4"]
    for q in questions:
        assert q["id"].startswith("A")


# ---------------------------------------------------------------------------
# expand_B：MU 真實 judgment，必須拆出含 $750 的路徑與 rearm 第二腿
# ---------------------------------------------------------------------------

def test_expand_b_finds_750_path_and_rearm_second_leg(run_dir):
    judgment, _facts = _judgment_facts(run_dir)
    questions = decide.expand_B(judgment)
    paths = [q["_path_text"] for q in questions]
    assert any("$750" in p for p in paths)
    assert any("SCA 覆蓋 ≥40%" in p and "86%" in p for p in paths)
    # 約束句本身（含「約束」「解除」「才進場」）不應該被當成一條路徑出題
    for q in questions:
        assert q["_path_text"] != q["_constraint"]


def test_expand_b_options_and_kind(run_dir):
    judgment, _facts = _judgment_facts(run_dir)
    questions = decide.expand_B(judgment)
    assert questions  # MU 真實資料至少有幾條路徑
    for q in questions:
        assert q["kind"] == "noul"
        assert q["options"] == ["是", "否"]
        assert q["_source"] in ("exec_line", "rearm_trigger")


def test_split_paths_helper():
    text = "甲；乙。丙或丁"
    assert decide._split_paths(text) == ["甲", "乙", "丙", "丁"]


def test_expand_b_empty_when_no_action_conditions():
    judgment = {"counter_evidence": {}}
    assert decide.expand_B(judgment) == []


# ---------------------------------------------------------------------------
# expand_C：三檔真實樣本剛好都是 0 題（全部已被引用），用合成 fixture 驗
# 偵測規則本身——負向、id 沒出現在 judgment 全文任何地方。
# ---------------------------------------------------------------------------

def test_expand_c_on_mu_real_data_is_zero_because_all_referenced(run_dir):
    judgment, facts = _judgment_facts(run_dir)
    questions = decide.expand_C(judgment, facts)
    assert questions == []


def test_expand_c_flags_negative_unreferenced_finding_with_direction_field():
    facts = {"findings_digest": [
        {"id": "axis_x#0", "axis": "axis_x", "direction": "-", "claim": "沒被接住的負向事實",
         "source": "s", "as_of": "2026-01-01"},
        {"id": "axis_x#1", "axis": "axis_x", "direction": "-", "claim": "有被接住的負向事實",
         "source": "s", "as_of": "2026-01-01"},
        {"id": "axis_x#2", "axis": "axis_x", "direction": "+", "claim": "正向事實不該出題",
         "source": "s", "as_of": "2026-01-01"},
    ]}
    judgment = {"oneliner": "測試", "decision_out": {"verdict": "觀望"},
                "counter_evidence": {"contradictions": [{"evidence_refs": ["axis_x#1"]}]}}
    questions = decide.expand_C(judgment, facts)
    assert [q["_finding_id"] for q in questions] == ["axis_x#0"]
    assert questions[0]["kind"] == "noul"
    assert questions[0]["options"] == ["有", "沒有"]


def test_expand_c_fallback_when_digest_has_no_direction_field():
    facts = {"findings_digest": [
        {"id": "geo_supply_chain#9", "axis": "geo_supply_chain", "claim": "台灣廠傳出罷工訴求",
         "source": "s", "as_of": "2026-01-01"},
        {"id": "end_markets#9", "axis": "end_markets", "claim": "終端需求穩健成長",
         "source": "s", "as_of": "2026-01-01"},
    ]}
    judgment = {"oneliner": "x", "decision_out": {"verdict": "觀望"}}
    questions = decide.expand_C(judgment, facts)
    # 沒有 direction 欄位時退回風險軸＋負向詞：geo_supply_chain 命中「罷工」，
    # end_markets 不在風險軸清單也沒有負向詞，不出題
    assert [q["_finding_id"] for q in questions] == ["geo_supply_chain#9"]


# ---------------------------------------------------------------------------
# expand_H
# ---------------------------------------------------------------------------

def test_expand_h_one_question_with_oneliner_context(run_dir):
    judgment, _facts = _judgment_facts(run_dir)
    questions = decide.expand_H(judgment)
    assert len(questions) == 1
    q = questions[0]
    assert q["id"] == "H1"
    assert q["kind"] == "choice"
    assert q["options"] == ["進場", "觀望", "迴避", "看不出"]
    assert q["context"] == judgment["oneliner"]


# ---------------------------------------------------------------------------
# apply_decisions：四類分流與 0.95／0.70 門檻邊界
# ---------------------------------------------------------------------------

def _mk_a_question(idx=3, r_id="R4", threshold="Nvidia HBM4 分配 <15%，bull 機率降至 15%"):
    return {"id": "A1", "kind": "noul", "question": "q", "options": ["是", "否"], "context": "{}",
            "_r_index": idx, "_r_id": r_id, "_threshold": threshold}


def test_apply_decisions_a_high_confidence_hit_sets_triggered_and_scenario(run_dir):
    judgment = {"thesis": {"R": [{"id": "R{0}".format(i)} for i in range(4)]},
                "oneliner": "x", "decision_out": {"verdict": "觀望"}}
    q = _mk_a_question()
    decisions = [{"id": "A1", "answer": "是", "confidence": 0.95, "note": "n", "valid": True}]
    result = decide.apply_decisions(run_dir, judgment, decisions, [q])
    assert len(result["mechanical_items"]) == 1
    item = result["mechanical_items"][0]
    assert item["item"] == "M-A1"
    assert item["light"] == "🔴"
    assert item["judgment_path"] == "$.thesis.R[3].threshold"
    assert judgment["thesis"]["R"][3]["triggered_by_evidence"] is True
    scenario = decide._load_json(run_dir / "scenario.json")
    assert scenario["scenarios"]["bull"]["p"] == 15
    assert scenario["scenarios"]["base"]["p"] == 55
    assert scenario["scenarios"]["bear"]["p"] == 30  # 不動 bear


def test_apply_decisions_a_hit_without_bull_pct_pattern_only_flags(run_dir):
    judgment = {"thesis": {"R": [{"id": "R1"}]}, "oneliner": "x", "decision_out": {"verdict": "觀望"}}
    q = _mk_a_question(idx=0, r_id="R1", threshold="沒有百分比可抓的門檻文字")
    decisions = [{"id": "A1", "answer": "是", "confidence": 0.99, "note": "n", "valid": True}]
    scenario_path = Path(run_dir) / "scenario.json"
    original_bull_p = decide._load_json(scenario_path)["scenarios"]["bull"]["p"]
    result = decide.apply_decisions(run_dir, judgment, decisions, [q])
    assert len(result["mechanical_items"]) == 1
    assert "機率待補丁輪處理" in result["mechanical_items"][0]["reason"]
    assert decide._load_json(scenario_path)["scenarios"]["bull"]["p"] == original_bull_p  # scenario.json 沒被亂改


def test_apply_decisions_confidence_boundaries(tmp_path):
    judgment = {"thesis": {"R": [{"id": "R1"}]}, "oneliner": "x", "decision_out": {"verdict": "觀望"}}
    q = _mk_a_question(idx=0, r_id="R1")
    run_dir = tmp_path
    (run_dir / "scenario.json").write_text("{}", encoding="utf-8")

    # 0.95 剛好達門檻 -> 機械處置
    d_high = [{"id": "A1", "answer": "是", "confidence": 0.95, "note": "n", "valid": True}]
    r_high = decide.apply_decisions(run_dir, dict(judgment), d_high, [q])
    assert len(r_high["mechanical_items"]) == 1
    assert r_high["mid_items"] == []
    assert r_high["owner_queue"] == []

    # 0.94999 差一點點 -> 中信心
    d_mid_top = [{"id": "A1", "answer": "是", "confidence": 0.94999, "note": "n", "valid": True}]
    r_mid_top = decide.apply_decisions(run_dir, dict(judgment), d_mid_top, [q])
    assert r_mid_top["mechanical_items"] == []
    assert len(r_mid_top["mid_items"]) == 1
    assert r_mid_top["mid_items"][0]["confidence"] == pytest.approx(0.94999)

    # 0.70 剛好 -> 中信心（含邊界本身）
    d_mid_low = [{"id": "A1", "answer": "是", "confidence": 0.70, "note": "n", "valid": True}]
    r_mid_low = decide.apply_decisions(run_dir, dict(judgment), d_mid_low, [q])
    assert len(r_mid_low["mid_items"]) == 1
    assert r_mid_low["owner_queue"] == []

    # 0.69999 差一點點 -> owner_queue
    d_low = [{"id": "A1", "answer": "是", "confidence": 0.69999, "note": "n", "valid": True}]
    r_low = decide.apply_decisions(run_dir, dict(judgment), d_low, [q])
    assert r_low["mid_items"] == []
    assert len(r_low["owner_queue"]) == 1

    # valid=False（答案不在 options 內），即使信心很高也進 owner_queue
    d_invalid = [{"id": "A1", "answer": "不知道", "confidence": 0.999, "note": "n", "valid": False}]
    r_invalid = decide.apply_decisions(run_dir, dict(judgment), d_invalid, [q])
    assert r_invalid["mechanical_items"] == []
    assert r_invalid["mid_items"] == []
    assert len(r_invalid["owner_queue"]) == 1


def test_apply_decisions_high_confidence_clean_answer_produces_nothing(tmp_path):
    judgment = {"thesis": {"R": [{"id": "R1"}]}, "oneliner": "x", "decision_out": {"verdict": "觀望"}}
    q = _mk_a_question(idx=0, r_id="R1")
    (tmp_path / "scenario.json").write_text("{}", encoding="utf-8")
    decisions = [{"id": "A1", "answer": "否", "confidence": 0.99, "note": "n", "valid": True}]
    result = decide.apply_decisions(tmp_path, judgment, decisions, [q])
    assert result["mechanical_items"] == []
    assert result["mid_items"] == []
    assert result["owner_queue"] == []
    assert "triggered_by_evidence" not in judgment["thesis"]["R"][0]


def test_apply_decisions_b_hit_and_clean(tmp_path):
    q_hit = {"id": "B1", "kind": "noul", "question": "q", "options": ["是", "否"], "context": "{}",
            "_source": "exec_line", "_path_text": "路徑X（價 ≤$750）", "_constraint": "約束句才進場"}
    q_clean = {"id": "B2", "kind": "noul", "question": "q", "options": ["是", "否"], "context": "{}",
              "_source": "rearm_trigger", "_path_text": "路徑Y", "_constraint": "約束句才進場"}
    judgment = {"oneliner": "x", "decision_out": {"verdict": "觀望"}}
    decisions = [
        {"id": "B1", "answer": "否", "confidence": 0.96, "note": "n", "valid": True},
        {"id": "B2", "answer": "是", "confidence": 0.96, "note": "n", "valid": True},
    ]
    (tmp_path / "scenario.json").write_text("{}", encoding="utf-8")
    result = decide.apply_decisions(tmp_path, judgment, decisions, [q_hit, q_clean])
    assert len(result["mechanical_items"]) == 1
    item = result["mechanical_items"][0]
    assert item["item"] == "M-B1"
    assert "$750" in item["reason"]
    assert item["judgment_path"] == "$.counter_evidence.action_conditions.exec_line"


def test_apply_decisions_c_hit(tmp_path):
    q = {"id": "C1", "kind": "noul", "question": "q", "options": ["有", "沒有"],
        "context": json.dumps({"claim": "某負向事實原文"}, ensure_ascii=False), "_finding_id": "axis_x#0"}
    judgment = {"oneliner": "x", "decision_out": {"verdict": "觀望"}}
    decisions = [{"id": "C1", "answer": "沒有", "confidence": 0.97, "note": "n", "valid": True}]
    (tmp_path / "scenario.json").write_text("{}", encoding="utf-8")
    result = decide.apply_decisions(tmp_path, judgment, decisions, [q])
    assert len(result["mechanical_items"]) == 1
    item = result["mechanical_items"][0]
    assert item["item"] == "M-C1"
    assert "axis_x#0" in item["reason"]
    assert item["judgment_path"] == "$.counter_evidence.contradictions"


def test_apply_decisions_h_kan_bu_chu_lai_never_hits_even_at_high_confidence(tmp_path):
    q = {"id": "H1", "kind": "choice", "question": "q", "options": ["進場", "觀望", "迴避", "看不出"], "context": "x"}
    judgment = {"oneliner": "x", "decision_out": {"verdict": "觀望"}}
    decisions = [{"id": "H1", "answer": "看不出", "confidence": 0.999, "note": "n", "valid": True}]
    (tmp_path / "scenario.json").write_text("{}", encoding="utf-8")
    result = decide.apply_decisions(tmp_path, judgment, decisions, [q])
    assert result["mechanical_items"] == []
    assert result["mid_items"] == []
    assert result["owner_queue"] == []


def test_apply_decisions_h_direction_mismatch_hits(tmp_path):
    q = {"id": "H1", "kind": "choice", "question": "q", "options": ["進場", "觀望", "迴避", "看不出"], "context": "x"}
    judgment = {"oneliner": "x", "decision_out": {"verdict": "觀望"}}
    decisions = [{"id": "H1", "answer": "迴避", "confidence": 0.97, "note": "n", "valid": True}]
    (tmp_path / "scenario.json").write_text("{}", encoding="utf-8")
    result = decide.apply_decisions(tmp_path, judgment, decisions, [q])
    assert len(result["mechanical_items"]) == 1
    assert result["mechanical_items"][0]["judgment_path"] == "$.oneliner"


# ---------------------------------------------------------------------------
# decide_batch：monkeypatch spawn.oneshot_stream
# ---------------------------------------------------------------------------

def test_decide_batch_assembles_effort_and_json_schema_args(tmp_path, monkeypatch):
    run_dir = tmp_path
    (run_dir / "judgment.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    (run_dir / "facts.json").write_text(json.dumps({"findings_digest": []}), encoding="utf-8")
    (run_dir / "scenario.json").write_text(json.dumps({}), encoding="utf-8")

    captured = []

    def _fake_oneshot_stream(prompt_path, model, out_json, cwd, **kwargs):
        captured.append({"prompt_path": prompt_path, "model": model, "cwd": cwd, "kwargs": kwargs})
        return {"ok": True, "structured_output": {"answers": [
            {"id": "A1", "answer": "是", "confidence": 0.99, "note": "n"},
        ]}, "cost_usd": 0.01, "cache_read": 0, "cache_creation": 100}

    monkeypatch.setattr(dd2_spawn, "oneshot_stream", _fake_oneshot_stream)
    monkeypatch.setattr(decide, "sp", dd2_spawn)

    questions = [{"id": "A1", "kind": "noul", "question": "q？", "options": ["是", "否"], "context": "ctx"}]
    usage = []
    results = decide.decide_batch(run_dir, questions, model="opus", effort="low", batch_size=20,
                                  agents_dir=run_dir / "agents", label_prefix="decide_A", usage_sink=usage)

    assert len(captured) == 1
    kwargs = captured[0]["kwargs"]
    extra_args = kwargs["extra_args"]
    assert extra_args[0:2] == ["--effort", "low"]
    assert extra_args[2] == "--json-schema"
    schema = json.loads(extra_args[3])
    assert schema["type"] == "object"
    assert schema["properties"]["answers"]["items"]["required"] == ["id", "answer", "confidence", "note"]

    assert results == [{"id": "A1", "answer": "是", "confidence": 0.99, "note": "n", "valid": True}]
    assert len(usage) == 1
    assert usage[0]["id"] == "decide_A_1"


def test_decide_batch_invalid_answer_forces_zero_confidence(tmp_path, monkeypatch):
    run_dir = tmp_path
    (run_dir / "judgment.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    (run_dir / "facts.json").write_text(json.dumps({"findings_digest": []}), encoding="utf-8")
    (run_dir / "scenario.json").write_text(json.dumps({}), encoding="utf-8")

    def _fake_oneshot_stream(prompt_path, model, out_json, cwd, **kwargs):
        return {"ok": True, "structured_output": {"answers": [
            {"id": "A1", "answer": "不知道", "confidence": 0.9, "note": "n"},
        ]}}

    monkeypatch.setattr(decide.sp, "oneshot_stream", _fake_oneshot_stream)
    questions = [{"id": "A1", "kind": "noul", "question": "q？", "options": ["是", "否"], "context": "ctx"}]
    results = decide.decide_batch(run_dir, questions, model="opus", agents_dir=run_dir / "agents",
                                  label_prefix="decide_A")
    assert results == [{"id": "A1", "answer": "不知道", "confidence": 0.0, "note": "n", "valid": False}]


def test_decide_batch_fills_missing_answer_when_model_skips_a_question(tmp_path, monkeypatch):
    run_dir = tmp_path
    (run_dir / "judgment.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    (run_dir / "facts.json").write_text(json.dumps({"findings_digest": []}), encoding="utf-8")
    (run_dir / "scenario.json").write_text(json.dumps({}), encoding="utf-8")

    def _fake_oneshot_stream(prompt_path, model, out_json, cwd, **kwargs):
        return {"ok": True, "structured_output": {"answers": [
            {"id": "A1", "answer": "是", "confidence": 0.9, "note": "n"},
        ]}}

    monkeypatch.setattr(decide.sp, "oneshot_stream", _fake_oneshot_stream)
    questions = [
        {"id": "A1", "kind": "noul", "question": "q1？", "options": ["是", "否"], "context": "c1"},
        {"id": "A2", "kind": "noul", "question": "q2？", "options": ["是", "否"], "context": "c2"},
    ]
    results = decide.decide_batch(run_dir, questions, model="opus", agents_dir=run_dir / "agents",
                                  label_prefix="decide_A")
    by_id = {r["id"]: r for r in results}
    assert by_id["A1"]["valid"] is True
    assert by_id["A2"]["valid"] is False
    assert by_id["A2"]["confidence"] == 0.0


def test_decide_batch_splits_into_batches_of_batch_size(tmp_path, monkeypatch):
    run_dir = tmp_path
    (run_dir / "judgment.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    (run_dir / "facts.json").write_text(json.dumps({"findings_digest": []}), encoding="utf-8")
    (run_dir / "scenario.json").write_text(json.dumps({}), encoding="utf-8")

    calls = []

    def _fake_oneshot_stream(prompt_path, model, out_json, cwd, **kwargs):
        calls.append(prompt_path)
        return {"ok": True, "structured_output": {"answers": []}}

    monkeypatch.setattr(decide.sp, "oneshot_stream", _fake_oneshot_stream)
    questions = [{"id": "A{0}".format(i), "kind": "noul", "question": "q", "options": ["是", "否"], "context": "c"}
                for i in range(25)]
    decide.decide_batch(run_dir, questions, model="opus", batch_size=20, agents_dir=run_dir / "agents",
                        label_prefix="decide_A")
    assert len(calls) == 2  # 25 題、batch_size=20 -> 兩包


def test_decide_batch_prefix_identical_across_batches(tmp_path, monkeypatch):
    """跨包快取靠前綴逐位元組相同：兩包看到的 prompt 前綴（扣掉題目列表本身）
    必須一樣。"""
    run_dir = tmp_path
    (run_dir / "judgment.json").write_text(json.dumps({"a": 1}), encoding="utf-8")
    (run_dir / "facts.json").write_text(json.dumps({"findings_digest": [{"id": "x#0", "direction": "-"}]}),
                                        encoding="utf-8")
    (run_dir / "scenario.json").write_text(json.dumps({"p": 1}), encoding="utf-8")

    prompts = []

    def _fake_oneshot_stream(prompt_path, model, out_json, cwd, **kwargs):
        prompts.append(Path(prompt_path).read_text(encoding="utf-8"))
        return {"ok": True, "structured_output": {"answers": []}}

    monkeypatch.setattr(decide.sp, "oneshot_stream", _fake_oneshot_stream)
    questions = [{"id": "A{0}".format(i), "kind": "noul", "question": "q", "options": ["是", "否"], "context": "c"}
                for i in range(25)]
    decide.decide_batch(run_dir, questions, model="opus", batch_size=20, agents_dir=run_dir / "agents",
                        label_prefix="decide_A")
    assert len(prompts) == 2
    prefix = decide._build_prefix(run_dir)
    assert prompts[0].startswith(prefix)
    assert prompts[1].startswith(prefix)


# ---------------------------------------------------------------------------
# _extract_answers
# ---------------------------------------------------------------------------

def test_extract_answers_from_structured_output_dict():
    r = {"structured_output": {"answers": [{"id": "A1", "answer": "是", "confidence": 1, "note": "n"}]}}
    assert decide._extract_answers(r) == [{"id": "A1", "answer": "是", "confidence": 1, "note": "n"}]


def test_extract_answers_from_structured_output_bare_list():
    r = {"structured_output": [{"id": "A1", "answer": "是", "confidence": 1, "note": "n"}]}
    assert decide._extract_answers(r) == [{"id": "A1", "answer": "是", "confidence": 1, "note": "n"}]


def test_extract_answers_falls_back_to_result_text():
    r = {"result_text": '{"answers": [{"id": "A1", "answer": "是", "confidence": 1, "note": "n"}]}'}
    assert decide._extract_answers(r) == [{"id": "A1", "answer": "是", "confidence": 1, "note": "n"}]


def test_extract_answers_empty_when_nothing_present():
    assert decide._extract_answers({}) == []


# ---------------------------------------------------------------------------
# TSM／TXN 離線展開一次，只印題數（README §8k 要求）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ticker_run_dir", [TSM_RUN_DIR, TXN_RUN_DIR])
def test_tsm_txn_offline_expand_smoke(ticker_run_dir, capsys):
    if not ticker_run_dir.exists():
        pytest.skip("fixture 不存在：{0}".format(ticker_run_dir))
    judgment, facts = _judgment_facts(ticker_run_dir)
    questions = (decide.expand_A(judgment, facts) + decide.expand_B(judgment)
                + decide.expand_C(judgment, facts) + decide.expand_H(judgment))
    print("{0}：共 {1} 題".format(ticker_run_dir.name, len(questions)))
    assert len(questions) > 0
    assert questions[-1]["id"] == "H1"
