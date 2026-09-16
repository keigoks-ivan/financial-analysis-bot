#!/usr/bin/env python3
"""測試 `scripts/dd2/spawn.py`（dd2 LLM 通）。

全程 monkeypatch `dd_headless.spawn`（不打真實 `claude` 子行程），涵蓋：
- `oneshot`／`agentic` 的參數組裝（allowed_tools／max_turns／budget_cache_read
  等原樣轉給 `dd_headless.spawn`）。
- `thinking_cap` 對 `MAX_THINKING_TOKENS` 環境變數的暫設與還原（含「呼叫前
  本來就有值」與「呼叫前沒有值」兩種情況）。
- `thinking_tokens`／`haiku_input_tokens` 從 out_json 原始檔 `modelUsage`
  正確加總。
- `strip_json` 對 fence、前後雜訊、純 JSON 三種輸入。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))

import dd_headless  # noqa: E402
from dd2 import spawn as dd2_spawn  # noqa: E402


def _write_prompt(tmp_path, name="prompt.md", text="請先想一下再回一句"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def _fake_spawn_factory(captured, out_payload=None, extra_result=None):
    """回傳一個可取代 `dd_headless.spawn` 的假函式。

    - 把收到的 kwargs 原樣記進 `captured`（list，供斷言參數組裝）。
    - 若給了 `out_payload`，把它當 raw JSON 寫進 `kwargs["out_json"]`
      （模擬 `dd_headless.spawn` 真的把子行程回應寫檔的行為）。
    - 回傳的 dict 是 `dd_headless.spawn` 平常會回的形狀（`extra_result`
      可覆寫／補充個別欄位）。
    """

    def _fake(**kwargs):
        captured.append(kwargs)
        out_json = kwargs.get("out_json")
        if out_json and out_payload is not None:
            out_path = Path(out_json)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(out_payload, ensure_ascii=False), encoding="utf-8")
        base = {
            "ok": True,
            "slim": True,
            "num_turns": 1,
            "cache_read": 0,
            "cache_creation": 0,
            "output_tokens": 0,
            "by_model": (out_payload or {}).get("modelUsage", {}),
            "over_budget": False,
            "over_target": False,
            "quota_exhausted": False,
            "cost_usd": 0.001,
            "duration_ms": 100,
            "result_text": "stub",
            "raw_path": str(out_json) if out_json else None,
        }
        if extra_result:
            base.update(extra_result)
        return base

    return _fake


# ---------------------------------------------------------------------------
# oneshot：參數組裝
# ---------------------------------------------------------------------------


def test_oneshot_assembles_call_with_no_tools_and_max_turns_1(tmp_path, monkeypatch):
    captured = []
    monkeypatch.setattr(dd_headless, "spawn", _fake_spawn_factory(captured))

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    result = dd2_spawn.oneshot(
        prompt_path=prompt,
        model="sonnet",
        out_json=out,
        cwd=str(tmp_path),
        budget_cache_read=500_000,
    )

    assert len(captured) == 1
    kwargs = captured[0]
    assert kwargs["prompt_path"] == prompt
    assert kwargs["model"] == "sonnet"
    assert kwargs["allowed_tools"] is None
    assert kwargs["max_turns"] == 1
    assert kwargs["out_json"] == out
    assert kwargs["cwd"] == str(tmp_path)
    assert kwargs["budget_cache_read"] == 500_000
    assert result["ok"] is True


# ---------------------------------------------------------------------------
# agentic：參數組裝
# ---------------------------------------------------------------------------


def test_agentic_assembles_call_with_tools_and_max_turns(tmp_path, monkeypatch):
    captured = []
    monkeypatch.setattr(dd_headless, "spawn", _fake_spawn_factory(captured))

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    tools = ["Write", "Read"]
    result = dd2_spawn.agentic(
        prompt_path=prompt,
        model="sonnet",
        out_json=out,
        cwd=str(tmp_path),
        tools=tools,
        max_turns=6,
        budget_cache_read=200_000,
    )

    assert len(captured) == 1
    kwargs = captured[0]
    assert kwargs["allowed_tools"] == tools
    assert kwargs["max_turns"] == 6
    assert kwargs["budget_cache_read"] == 200_000
    assert result["ok"] is True


def test_agentic_budget_cache_read_defaults_to_none(tmp_path, monkeypatch):
    captured = []
    monkeypatch.setattr(dd_headless, "spawn", _fake_spawn_factory(captured))

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    dd2_spawn.agentic(
        prompt_path=prompt,
        model="opus",
        out_json=out,
        cwd=str(tmp_path),
        tools=["Write"],
        max_turns=3,
    )

    assert captured[0]["budget_cache_read"] is None


# ---------------------------------------------------------------------------
# thinking_cap → MAX_THINKING_TOKENS 環境變數暫設／還原
# ---------------------------------------------------------------------------


def test_thinking_cap_sets_env_var_during_call_and_removes_after(tmp_path, monkeypatch):
    monkeypatch.delenv("MAX_THINKING_TOKENS", raising=False)
    seen = {}

    def _fake(**kwargs):
        import os

        seen["value"] = os.environ.get("MAX_THINKING_TOKENS")
        out_json = kwargs.get("out_json")
        if out_json:
            Path(out_json).write_text("{}", encoding="utf-8")
        return {"ok": True, "by_model": {}, "raw_path": str(out_json)}

    monkeypatch.setattr(dd_headless, "spawn", _fake)

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    dd2_spawn.oneshot(prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path), thinking_cap=1024)

    assert seen["value"] == "1024"
    import os

    assert "MAX_THINKING_TOKENS" not in os.environ


def test_thinking_cap_none_does_not_touch_env_var(tmp_path, monkeypatch):
    monkeypatch.delenv("MAX_THINKING_TOKENS", raising=False)
    seen = {}

    def _fake(**kwargs):
        import os

        seen["value"] = os.environ.get("MAX_THINKING_TOKENS")
        out_json = kwargs.get("out_json")
        if out_json:
            Path(out_json).write_text("{}", encoding="utf-8")
        return {"ok": True, "by_model": {}, "raw_path": str(out_json)}

    monkeypatch.setattr(dd_headless, "spawn", _fake)

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    dd2_spawn.oneshot(prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path), thinking_cap=None)

    assert seen["value"] is None
    import os

    assert "MAX_THINKING_TOKENS" not in os.environ


def test_thinking_cap_restores_prior_env_var_value_after_call(tmp_path, monkeypatch):
    monkeypatch.setenv("MAX_THINKING_TOKENS", "999")
    seen = {}

    def _fake(**kwargs):
        import os

        seen["value"] = os.environ.get("MAX_THINKING_TOKENS")
        out_json = kwargs.get("out_json")
        if out_json:
            Path(out_json).write_text("{}", encoding="utf-8")
        return {"ok": True, "by_model": {}, "raw_path": str(out_json)}

    monkeypatch.setattr(dd_headless, "spawn", _fake)

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    dd2_spawn.oneshot(prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path), thinking_cap=2048)

    assert seen["value"] == "2048"
    import os

    assert os.environ["MAX_THINKING_TOKENS"] == "999"


def test_thinking_cap_restores_even_when_dd_headless_spawn_raises(tmp_path, monkeypatch):
    monkeypatch.delenv("MAX_THINKING_TOKENS", raising=False)

    def _raising_fake(**kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(dd_headless, "spawn", _raising_fake)

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    with pytest.raises(RuntimeError):
        dd2_spawn.oneshot(prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path), thinking_cap=4096)

    import os

    assert "MAX_THINKING_TOKENS" not in os.environ


# ---------------------------------------------------------------------------
# thinking_tokens／haiku_input_tokens 加總
# ---------------------------------------------------------------------------

RAW_WITH_HAIKU = {
    "type": "result",
    "is_error": False,
    "result": "OK",
    "modelUsage": {
        "claude-haiku-4-5-20251001": {
            "inputTokens": 10371,
            "outputTokens": 446,
            "thinkingTokens": 0,
        },
        "claude-sonnet-5": {
            "inputTokens": 6,
            "outputTokens": 297,
            "thinkingTokens": 812,
        },
    },
}


def test_thinking_tokens_summed_across_all_models(tmp_path, monkeypatch):
    captured = []
    monkeypatch.setattr(
        dd_headless, "spawn", _fake_spawn_factory(captured, out_payload=RAW_WITH_HAIKU)
    )

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    result = dd2_spawn.oneshot(prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path))

    # 0（haiku）+ 812（sonnet）
    assert result["thinking_tokens"] == 812


def test_haiku_input_tokens_only_sums_haiku_named_models(tmp_path, monkeypatch):
    captured = []
    monkeypatch.setattr(
        dd_headless, "spawn", _fake_spawn_factory(captured, out_payload=RAW_WITH_HAIKU)
    )

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    result = dd2_spawn.oneshot(prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path))

    # 只有 claude-haiku-4-5-20251001 的 inputTokens（10371），sonnet 的 6 不計入
    assert result["haiku_input_tokens"] == 10371


def test_no_haiku_model_gives_zero_haiku_input_tokens(tmp_path, monkeypatch):
    payload = {
        "modelUsage": {
            "claude-sonnet-5": {"inputTokens": 6, "outputTokens": 297, "thinkingTokens": 5},
        }
    }
    captured = []
    monkeypatch.setattr(dd_headless, "spawn", _fake_spawn_factory(captured, out_payload=payload))

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "out.json"
    result = dd2_spawn.agentic(
        prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path), tools=["Write"], max_turns=2
    )

    assert result["haiku_input_tokens"] == 0
    assert result["thinking_tokens"] == 5


def test_missing_out_json_file_gives_zero_totals(tmp_path, monkeypatch):
    # dd_headless.spawn 被 monkeypatch 成完全不寫檔（模擬 out_json 未落地的邊界情況）
    def _fake(**kwargs):
        return {"ok": True, "by_model": {}, "raw_path": None}

    monkeypatch.setattr(dd_headless, "spawn", _fake)

    prompt = _write_prompt(tmp_path)
    out = tmp_path / "does_not_exist.json"
    result = dd2_spawn.oneshot(prompt_path=prompt, model="sonnet", out_json=out, cwd=str(tmp_path))

    assert result["thinking_tokens"] == 0
    assert result["haiku_input_tokens"] == 0


# ---------------------------------------------------------------------------
# strip_json
# ---------------------------------------------------------------------------


def test_strip_json_pure_json():
    obj, err = dd2_spawn.strip_json('{"a": 1, "b": [1, 2, 3]}')
    assert err is None
    assert obj == {"a": 1, "b": [1, 2, 3]}


def test_strip_json_with_code_fence():
    text = '這是結果：\n```json\n{\n  "verdict": "進場",\n  "score": 8\n}\n```\n'
    obj, err = dd2_spawn.strip_json(text)
    assert err is None
    assert obj == {"verdict": "進場", "score": 8}


def test_strip_json_with_leading_and_trailing_prose_no_fence():
    text = '根據判斷，結果如下：\n{"verdict": "觀望", "score": 5}\n以上是我的回覆，如有問題請告知。'
    obj, err = dd2_spawn.strip_json(text)
    assert err is None
    assert obj == {"verdict": "觀望", "score": 5}


def test_strip_json_array_with_noise():
    text = 'here is the array:\n[{"item": "a"}, {"item": "b"}]\nhope this helps'
    obj, err = dd2_spawn.strip_json(text)
    assert err is None
    assert obj == [{"item": "a"}, {"item": "b"}]


def test_strip_json_no_json_present_returns_error():
    obj, err = dd2_spawn.strip_json("完全沒有 JSON 的一段話。")
    assert obj is None
    assert err is not None


def test_strip_json_none_input_returns_error():
    obj, err = dd2_spawn.strip_json(None)
    assert obj is None
    assert err is not None
