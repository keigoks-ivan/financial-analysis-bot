#!/usr/bin/env python3
"""測試 `scripts/dd_headless.py`（v17 WP1c）。

全程用假 `claude` binary（`scripts/tests/fake_claude.py`，透過
`DD_CLAUDE_BIN` 指過去），不打真實 API。涵蓋：
- cache_read 加總（modelUsage 多模型加總）
- over_budget 判定（超過/未超過兩種）
- is_error 處理（fixture 標 is_error=true → ok=False）
- spawn_many 順序保留（刻意讓後送出的先完成，仍照 specs 順序回傳）

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent
FAKE_CLAUDE = TESTS_DIR / "fake_claude.py"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_headless  # noqa: E402


@pytest.fixture(autouse=True)
def _fake_claude_bin(monkeypatch):
    monkeypatch.setenv("DD_CLAUDE_BIN", str(FAKE_CLAUDE))
    monkeypatch.delenv("FAKE_CLAUDE_RESPONSE", raising=False)
    monkeypatch.delenv("FAKE_CLAUDE_LOG", raising=False)
    yield


def _write_prompt(tmp_path, name, text="只回 OK"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def _write_response_fixture(tmp_path, name, payload):
    p = tmp_path / name
    p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return p


# 規格文件已知回傳形狀樣本（2026-09-05 實測），逐字複製自
# notes/site-internal/dd/_wp_spec_v17_20260905.md WP1c 第 5 點。
KNOWN_SAMPLE = {
    "type": "result",
    "is_error": False,
    "num_turns": 3,
    "duration_ms": 11692,
    "total_cost_usd": 0.0915,
    "result": "Bloom Energy 2026 年 Q2 營收 10.65 億美元 …",
    "usage": {
        "input_tokens": 6,
        "cache_creation_input_tokens": 12597,
        "cache_read_input_tokens": 77719,
        "output_tokens": 297,
    },
    "modelUsage": {
        "claude-haiku-4-5-20251001": {
            "inputTokens": 10371,
            "outputTokens": 446,
            "cacheReadInputTokens": 0,
            "cacheCreationInputTokens": 0,
            "webSearchRequests": 1,
            "costUSD": 0.0226,
        },
        "claude-sonnet-5": {
            "inputTokens": 6,
            "outputTokens": 297,
            "cacheReadInputTokens": 77719,
            "cacheCreationInputTokens": 12597,
            "webSearchRequests": 0,
            "costUSD": 0.0689,
        },
    },
}


def test_cache_read_summation_across_models(tmp_path, monkeypatch):
    resp = _write_response_fixture(tmp_path, "resp.json", KNOWN_SAMPLE)
    monkeypatch.setenv("FAKE_CLAUDE_RESPONSE", str(resp))
    prompt = _write_prompt(tmp_path, "prompt.md")
    out = tmp_path / "out.json"

    result = dd_headless.spawn(
        prompt_path=prompt,
        model="sonnet",
        allowed_tools=["WebSearch", "Read"],
        max_turns=4,
        budget_cache_read=1_000_000,
        out_json=out,
    )

    # 兩個模型 cacheReadInputTokens 加總：0 + 77719
    assert result["cache_read"] == 77719
    assert result["cache_creation"] == 0 + 12597
    assert result["output_tokens"] == 446 + 297
    assert result["num_turns"] == 3
    assert result["cost_usd"] == pytest.approx(0.0915)
    assert result["ok"] is True
    assert result["over_budget"] is False
    assert set(result["by_model"].keys()) == {"claude-haiku-4-5-20251001", "claude-sonnet-5"}
    # 原始 JSON 有寫到 out_json
    assert out.exists()
    raw = json.loads(out.read_text(encoding="utf-8"))
    assert raw == KNOWN_SAMPLE


def test_over_budget_true_when_cache_read_exceeds_budget(tmp_path, monkeypatch):
    resp = _write_response_fixture(tmp_path, "resp.json", KNOWN_SAMPLE)
    monkeypatch.setenv("FAKE_CLAUDE_RESPONSE", str(resp))
    prompt = _write_prompt(tmp_path, "prompt.md")

    result = dd_headless.spawn(
        prompt_path=prompt,
        model="sonnet",
        allowed_tools=None,
        max_turns=1,
        budget_cache_read=50_000,  # 77719 > 50000
        out_json=tmp_path / "out.json",
    )
    assert result["cache_read"] == 77719
    assert result["over_budget"] is True


def test_over_budget_false_when_under_budget(tmp_path, monkeypatch):
    resp = _write_response_fixture(tmp_path, "resp.json", KNOWN_SAMPLE)
    monkeypatch.setenv("FAKE_CLAUDE_RESPONSE", str(resp))
    prompt = _write_prompt(tmp_path, "prompt.md")

    result = dd_headless.spawn(
        prompt_path=prompt,
        model="sonnet",
        allowed_tools=None,
        max_turns=1,
        budget_cache_read=2_000_000,
        out_json=tmp_path / "out.json",
    )
    assert result["over_budget"] is False


def test_over_budget_none_when_no_budget_given(tmp_path, monkeypatch):
    resp = _write_response_fixture(tmp_path, "resp.json", KNOWN_SAMPLE)
    monkeypatch.setenv("FAKE_CLAUDE_RESPONSE", str(resp))
    prompt = _write_prompt(tmp_path, "prompt.md")

    result = dd_headless.spawn(
        prompt_path=prompt,
        model="sonnet",
        allowed_tools=None,
        max_turns=1,
        budget_cache_read=None,
        out_json=tmp_path / "out.json",
    )
    assert result["over_budget"] is False


def test_is_error_true_maps_to_ok_false(tmp_path, monkeypatch):
    bad = dict(KNOWN_SAMPLE)
    bad["is_error"] = True
    bad["result"] = "API error: overloaded"
    resp = _write_response_fixture(tmp_path, "resp_err.json", bad)
    monkeypatch.setenv("FAKE_CLAUDE_RESPONSE", str(resp))
    prompt = _write_prompt(tmp_path, "prompt.md")

    result = dd_headless.spawn(
        prompt_path=prompt,
        model="sonnet",
        allowed_tools=None,
        max_turns=1,
        budget_cache_read=None,
        out_json=tmp_path / "out.json",
    )
    assert result["ok"] is False
    assert result["result_text"] == "API error: overloaded"


def test_is_error_default_ok_true(tmp_path, monkeypatch):
    # fake_claude.py 沒設 FAKE_CLAUDE_RESPONSE 時，預設回應 is_error=False
    prompt = _write_prompt(tmp_path, "prompt.md")
    result = dd_headless.spawn(
        prompt_path=prompt,
        model="sonnet",
        allowed_tools=None,
        max_turns=1,
        budget_cache_read=None,
        out_json=tmp_path / "out.json",
    )
    assert result["ok"] is True


def test_unparseable_output_is_treated_as_error(tmp_path, monkeypatch):
    # FAKE_CLAUDE_RESPONSE 指向一個非 JSON 的檔，模擬子行程輸出壞掉
    bad_path = tmp_path / "not_json.txt"
    bad_path.write_text("not a json line", encoding="utf-8")
    monkeypatch.setenv("FAKE_CLAUDE_RESPONSE", str(bad_path))
    prompt = _write_prompt(tmp_path, "prompt.md")

    result = dd_headless.spawn(
        prompt_path=prompt,
        model="sonnet",
        allowed_tools=None,
        max_turns=1,
        budget_cache_read=None,
        out_json=tmp_path / "out.json",
    )
    assert result["ok"] is False
    assert result["cache_read"] == 0


def test_spawn_many_preserves_input_order_despite_out_of_order_completion(tmp_path):
    # 5 個 spec，故意讓「後面送出的」先睡醒回應（sleep 隨 index 遞減），
    # 逼出真的 out-of-order completion，驗證 spawn_many 仍照輸入順序回傳。
    n = 5
    run_dir = tmp_path
    specs = []
    for i in range(n):
        prompt_name = "prompts/p_{}.md".format(i)
        prompt_path = run_dir / prompt_name
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        sleep_s = (n - i) * 0.05  # spec 0 睡最久、spec 4 睡最短
        prompt_path.write_text("SLEEP:{}\nspec-{}".format(sleep_s, i), encoding="utf-8")
        specs.append(
            {
                "id": "spec-{}".format(i),
                "model": "sonnet",
                "prompt": prompt_name,
                "out": "parts/out_{}.json".format(i),
                "tools": ["WebSearch"],
                "max_turns": 4,
                "budget_cache_read": 1_000_000,
                "run_dir": str(run_dir),
            }
        )

    results = dd_headless.spawn_many(specs, max_parallel=5)

    assert len(results) == n
    for i, r in enumerate(results):
        assert r is not None
        assert r["id"] == "spec-{}".format(i)
        # result_text 是 fake_claude 原樣回傳的 stdin，應含對應的 spec-i 標記
        assert "spec-{}".format(i) in r["result_text"]
        assert r["ok"] is True


def test_cli_main_prints_summary_line_and_writes_out(tmp_path, monkeypatch, capsys):
    resp = _write_response_fixture(tmp_path, "resp.json", KNOWN_SAMPLE)
    monkeypatch.setenv("FAKE_CLAUDE_RESPONSE", str(resp))
    prompt = _write_prompt(tmp_path, "prompt.md")
    out = tmp_path / "out.json"

    rc = dd_headless.main(
        [
            "--prompt",
            str(prompt),
            "--model",
            "sonnet",
            "--max-turns",
            "1",
            "--budget",
            "200000",
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    captured = capsys.readouterr()
    line = captured.out.strip()
    parts = line.split("／")
    assert len(parts) == 5
    assert parts[0] == "sonnet"
    assert out.exists()


def test_cli_passes_setting_sources_through_to_binary(tmp_path, monkeypatch):
    # 用 FAKE_CLAUDE_LOG 檢查 --setting-sources 有原樣轉傳給子行程 argv
    log_path = tmp_path / "log.jsonl"
    monkeypatch.setenv("FAKE_CLAUDE_LOG", str(log_path))
    prompt = _write_prompt(tmp_path, "prompt.md")
    out = tmp_path / "out.json"

    rc = dd_headless.main(
        [
            "--prompt",
            str(prompt),
            "--model",
            "sonnet",
            "--max-turns",
            "1",
            "--out",
            str(out),
            "--setting-sources",
            "user",
        ]
    )
    assert rc == 0
    logged = json.loads(log_path.read_text(encoding="utf-8").splitlines()[0])
    assert "--setting-sources" in logged["argv"]
    assert "user" in logged["argv"]
