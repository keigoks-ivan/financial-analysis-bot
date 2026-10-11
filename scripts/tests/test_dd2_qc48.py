"""QC-48（row 8a 爆發候選 Bull 冷讀）接線：dd_decision 的放行／降級、run.py 的解析與快取。2026-10-11 6187.TWO 案。"""
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dd2"))
import dd_decision  # noqa: E402
import run  # noqa: E402

# 6187.TWO 20261011 投影視圖的 decision_inputs（8a 資格全過的真實樣本，長字串欄截短）
DI_8A = {"signal": "B", "ma": "✅", "cycle_position": "中循環", "cycle_verdict": "等回踩",
         "thesis_irreconcilable": False, "valuation_dependent": False, "market_wrong_reason_given": "市場把擴產高峰當結構成長",
         "momentum_overheated": None, "cycle_gates_pass": False, "qc49_inherit_prior": None,
         "wait_for_price": True, "wait_for_price_condition": "等 900 元以下", "trap": "🟡", "val": "🔴", "moat": "B",
         "moat_trend": "→", "runway_post_y5": "🟢", "capalloc_grade": "C", "archetype": "循環/商品", "price_at_dd": 1525.0,
         "week26_return_pct": 74.31, "consensus_rev_3m_pct": None, "asym_ratio": None, "irr_base_pct": None,
         "ev5y_pct": None, "val_denominator_disputed": True, "val_denominator_note": "分母爭議"}


def _rows(out):
    return {r["row"]: r for r in out["audit_rows"]}


def test_qc48_null_keeps_8a():  # 舊鏈（沒經 dd2 critic）行為不變
    out = dd_decision.evaluate(dict(DI_8A))
    assert out["row_hit"] == "8a" and out["verdict"] == "進場·條件式（爆發候選）"
    assert "8a-QC48" not in _rows(out)


def test_qc48_pass_keeps_8a():
    out = dd_decision.evaluate(dict(DI_8A, qc48_result="pass", qc48_note="Bull 依據成立"))
    assert out["row_hit"] == "8a"
    assert _rows(out)["8a-QC48"]["hit"] is False


def test_qc48_fail_and_not_run_fall_to_row8():
    for res in ("fail", "not_run"):
        out = dd_decision.evaluate(dict(DI_8A, qc48_result=res, qc48_note="結論"))
        assert out["verdict"] == "觀望", res
        assert not str(out["row_hit"]).startswith("8a"), res
        rows = _rows(out)
        assert rows["8a"]["hit"] is True and rows["8a-QC48"]["hit"] is True  # 資格仍記錄為過，攔下的是 critic
        assert "QC-48" not in out["requires_critic"]


def _reply(lights, conclusion="結論一句"):
    return json.dumps({"items": [{"item": k, "light": l, "reason": "r", "evidence": "e"}
                                 for k, l in zip(("①", "②", "③"), lights)], "conclusion": conclusion}, ensure_ascii=False)


def test_qc48_parse():
    assert run._qc48_parse(_reply(["🟢", "🟡", "🟢"]))[0] == "pass"
    assert run._qc48_parse(_reply(["🟢", "🟡", "🔴"]))[0] == "fail"
    assert run._qc48_parse("```json\n" + _reply(["🟢", "🟢", "🟢"]) + "\n```")[0] == "pass"
    assert run._qc48_parse(_reply(["🟢", "🟢"])) is None  # 缺一項
    assert run._qc48_parse(_reply(["🟢", "綠", "🟢"])) is None  # 燈號不合法
    assert run._qc48_parse(_reply(["🟢", "🟢", "🟢"], conclusion="")) is None
    assert run._qc48_parse("不是 JSON") is None


def _ctx(tmp_path, eligible=True):
    (tmp_path / "agents").mkdir()
    (tmp_path / "prompts").mkdir()
    j = {"decision_inputs": {"signal": "B"},
         "decision_out": {"row_hit": "8a" if eligible else "8", "audit_rows": [{"row": "8a", "hit": eligible}]}}
    (tmp_path / "judgment.json").write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    ctx = types.SimpleNamespace(run_dir=tmp_path, gate_model="sonnet", manifest={}, save=lambda: None)
    return ctx, {"agent_usage": []}


def _patch(monkeypatch, tmp_path, replies, prompt="P"):
    calls = []
    p = tmp_path / "prompts" / "qc48.md"

    def fake_build(run_dir):
        p.write_text(prompt, encoding="utf-8")
        return {"prompt_path": p}

    def fake_agentic(prompt_path, model, out, cwd, tools, max_turns, budget_cache_read=None):
        calls.append(model)
        text = replies[len(calls) - 1]
        return {"ok": text is not None, "result_text": text, "num_turns": 3}

    monkeypatch.setattr(run.bundle, "build_qc48", fake_build)
    monkeypatch.setattr(run.sp, "agentic", fake_agentic)
    return calls


def _di(tmp_path):
    return json.loads((tmp_path / "judgment.json").read_text(encoding="utf-8"))["decision_inputs"]


def test_qc48_apply_fail_then_cached(tmp_path, monkeypatch):
    ctx, st = _ctx(tmp_path)
    calls = _patch(monkeypatch, tmp_path, [_reply(["🟢", "🟡", "🔴"], "跑道證據查無來源")])
    assert run._qc48_apply(ctx, st) is True
    assert _di(tmp_path)["qc48_result"] == "fail" and _di(tmp_path)["qc48_note"] == "跑道證據查無來源"
    assert calls == ["sonnet"]
    # 同 prompt 重跑（--reuse-judgment 重建判斷物、qc48 欄被清掉）→ 沿用結果、不再 spawn
    j = json.loads((tmp_path / "judgment.json").read_text(encoding="utf-8"))
    j["decision_inputs"].pop("qc48_result")
    j["decision_inputs"].pop("qc48_note")
    (tmp_path / "judgment.json").write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    assert run._qc48_apply(ctx, st) is True and len(calls) == 1
    assert st["qc48"]["reused"] is True
    assert run._qc48_apply(ctx, st) is False  # 已寫入、值沒變


def test_qc48_apply_two_invalid_is_not_run(tmp_path, monkeypatch):
    ctx, st = _ctx(tmp_path)
    calls = _patch(monkeypatch, tmp_path, ["亂回", None])
    assert run._qc48_apply(ctx, st) is True
    assert _di(tmp_path)["qc48_result"] == "not_run" and len(calls) == 2
    # not_run 不沿用：下一輪會重派
    _patch(monkeypatch, tmp_path, [_reply(["🟢", "🟢", "🟢"])])
    assert run._qc48_apply(ctx, st) is True and _di(tmp_path)["qc48_result"] == "pass"


def test_qc48_apply_clears_when_not_eligible(tmp_path, monkeypatch):
    ctx, st = _ctx(tmp_path, eligible=False)
    calls = _patch(monkeypatch, tmp_path, [])
    assert run._qc48_apply(ctx, st) is False and calls == []
    j = json.loads((tmp_path / "judgment.json").read_text(encoding="utf-8"))
    j["decision_inputs"].update(qc48_result="pass", qc48_note="舊值")  # 例：patch 自己填了
    (tmp_path / "judgment.json").write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    assert run._qc48_apply(ctx, st) is True and "qc48_result" not in _di(tmp_path)
