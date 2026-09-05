#!/usr/bin/env python3
"""測試 `scripts/ddreport.py` 的 v17 WP1d 新增子命令（`run`／`stage0`／
`judge`／`gate`／`brief`，含 `judge check`）：Stage 0 → 判斷 → 閘 → 快速版
的狀態機串接、over_budget 熔斷、finalize 需重派清單只重派該批、
`--resume` 從最後成功步接續。

分兩類：
- 一個端到端整合測試，真的用 `--replay-from` 跑
  `notes/site-internal/dd/_src/CIEN_20260905/` 這份真實回溯 fixture 到
  `--until judged`（不打真實 API，`DD_CLAUDE_BIN` 指到
  `scripts/tests/fake_claude.py` 的 replay 模式），驗證 manifest 狀態機
  真的推進、agent_usage 有記錄。
- 三個針對 `_do_judge`／`_do_stage0`／`cmd_run` 內部函式的隔離單元測試
  （monkeypatch `dd_headless.spawn`／`spawn_many`，不碰任何 fixture 或
  子行程），驗證 over_budget 熔斷、finalize 重派只挑失敗批、`--resume`
  跳過已成功的段。

用假 ticker（`ZTEST*`）＋自建最小 run_dir 做單元測試，不動真實 ticker
的 `.dd_build/runs/`；整合測試用完會清掉自己建的
`.dd_build/runs/CIEN_20260905/`（若之前不存在）。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent
TESTS_DIR = Path(__file__).resolve().parent
FAKE_CLAUDE = TESTS_DIR / "fake_claude.py"
CIEN_FIXTURE = REPO_ROOT / "notes/site-internal/dd/_src/CIEN_20260905"

sys.path.insert(0, str(SCRIPTS_DIR))
import ddreport  # noqa: E402


class _FakeCompleted:
    """`subprocess.CompletedProcess` 的最小替身，供 monkeypatch 用。"""

    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _clean_run_dir(ticker, date):
    d = ddreport._run_dir(ticker, date)
    if d.exists():
        shutil.rmtree(d)
    return d


# ---------------------------------------------------------------------------
# 1) 整合測試：真 fixture、replay 模式、狀態機真的推進到 judged
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not CIEN_FIXTURE.exists(), reason="CIEN_20260905 回溯 fixture 不存在")
def test_run_replay_reaches_judged_and_advances_state_machine():
    ticker, date = "CIEN", "20260905"
    run_dir = ddreport._run_dir(ticker, date)
    pre_existing = run_dir.exists()
    if not pre_existing:
        pass  # 讓 run 自己建
    else:
        shutil.rmtree(run_dir)

    try:
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "ddreport.py"), "run", ticker,
             "--date", date, "--offline", "--replay-from", str(CIEN_FIXTURE),
             "--until", "judged"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=180,
            env={**__import__("os").environ, "DD_J1_WARN": "1"},
        )
        assert r.returncode == 0, "run 應該一路 PASS 到 judged：\n{0}\n{1}".format(r.stdout, r.stderr)

        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        stages = manifest.get("stages", {})

        assert stages.get("stage0", {}).get("state") == "PASS"
        assert stages.get("stage0", {}).get("started")
        assert stages.get("stage0", {}).get("ended")

        assert stages.get("judged", {}).get("state") == "PASS"
        assert len(stages.get("judged", {}).get("agent_usage") or []) >= 1
        # judged 尚未觸及（--until judged 未含 gated）
        assert "gated" not in stages

        # `judge check` 這個獨立子命令本身也要能單獨跑（sub-agent 透過 Bash
        # 呼叫的同一支指令）
        r2 = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "ddreport.py"), "judge", "check", ticker, date],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60,
            env={**__import__("os").environ, "DD_J1_WARN": "1"},
        )
        assert r2.returncode == 0
        assert "[PASS]" in r2.stdout
    finally:
        if run_dir.exists():
            shutil.rmtree(run_dir)


# ---------------------------------------------------------------------------
# 2) over_budget 熔斷：任一 spawn over_budget 即停，--accept-over-budget 才放行
# ---------------------------------------------------------------------------

def test_judge_stage_stops_on_over_budget_unless_accepted(monkeypatch):
    ticker, date = "ZTESTOB", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "agents").mkdir(parents=True)
    (run_dir / "bundles").mkdir(parents=True)

    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: _FakeCompleted(0))
    monkeypatch.setattr(
        ddreport.dd_headless, "spawn",
        lambda **kw: {"ok": True, "over_budget": True, "num_turns": 1, "cache_read": 999999},
    )
    monkeypatch.setattr(ddreport, "_judge_check", lambda t, d: (True, "[PASS] 假造：judge check ok"))

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {}}
        rc = ddreport._do_judge(ticker, date, "fable", None, False, manifest)
        assert rc == 1
        m = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert m["stages"]["judged"]["state"] == "OVER_BUDGET"
        assert m["stages"]["judged"]["over_budget"] is True

        # --accept-over-budget=True 時同一情境應該放行
        manifest2 = {"ticker": ticker, "date": date, "stages": {}}
        rc2 = ddreport._do_judge(ticker, date, "fable", None, True, manifest2)
        assert rc2 == 0
        m2 = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert m2["stages"]["judged"]["state"] == "PASS"
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# 3) finalize FAIL 產重派清單，只重派該批（≤2 次）
# ---------------------------------------------------------------------------

def test_stage0_finalize_retry_respawns_only_failing_batch(monkeypatch):
    ticker, date = "ZTESTRETRY", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    (run_dir / "parts").mkdir(parents=True)
    (run_dir / "prompts").mkdir(parents=True)

    spawn_list = [
        {"id": "a_1", "model": "sonnet", "prompt": "prompts/a_1.md", "out": "parts/axes_1.json",
         "tools": [], "max_turns": 1, "budget_cache_read": 1000},
        {"id": "a_2", "model": "sonnet", "prompt": "prompts/a_2.md", "out": "parts/axes_2.json",
         "tools": [], "max_turns": 1, "budget_cache_read": 1000},
    ]
    (run_dir / "spawn_list.json").write_text(json.dumps(spawn_list), encoding="utf-8")
    for p in ("prompts/a_1.md", "prompts/a_2.md"):
        (run_dir / p).write_text("dummy", encoding="utf-8")

    spawn_many_calls = []

    def fake_spawn_many(specs, max_parallel=4):
        spawn_many_calls.append([s["id"] for s in specs])
        return [{"ok": True, "over_budget": False, "num_turns": 1, "id": s["id"]} for s in specs]

    monkeypatch.setattr(ddreport.dd_headless, "spawn_many", fake_spawn_many)

    finalize_calls = {"n": 0}

    def fake_finalize(run_dir_arg):
        finalize_calls["n"] += 1
        # 每次都只有 axes_2.json 失敗（模擬該批一直交不出合格證據）
        return 1, "finalize FAIL #{0}".format(finalize_calls["n"]), {"axes_2.json"}

    monkeypatch.setattr(ddreport, "_finalize_run_dir", fake_finalize)

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {}}
        plan_kwargs = {"archetype": None, "peers": None, "segments": None,
                       "axes_per_batch": 2, "offline": True}
        rc = ddreport._do_stage0(ticker, date, plan_kwargs, None, False, manifest)

        assert rc == 1  # finalize 從未真的過
        assert finalize_calls["n"] == 3  # 1 次初次 + 至多 2 次重試 = 3

        m = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert m["stages"]["stage0"]["state"] == "FAIL"
        assert m["stages"]["stage0"]["finalize_retries"] == 2

        # 第一次 spawn_many：兩批都送（沒有 k_koyfin，故只有一次 other_specs 呼叫）
        assert spawn_many_calls[0] == ["a_1", "a_2"]
        # 之後每次重派：只有 a_2（out=parts/axes_2.json 撞到 needs 清單），
        # 絕不重派 a_1
        for retry_call in spawn_many_calls[1:]:
            assert retry_call == ["a_2"]
        assert len(spawn_many_calls) == 3  # 初次 + 2 次重試
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# 4) --resume：從最後一個成功（PASS／SKIPPED）的段接續，已成功的段不重跑
# ---------------------------------------------------------------------------

def test_run_resume_skips_completed_stages(monkeypatch):
    ticker, date = "ZTESTRESUME", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    run_dir.mkdir(parents=True)

    manifest = {
        "ticker": ticker, "date": date, "state": "judged_fail",
        "stages": {
            "stage0": {"state": "PASS"},
            "judged": {"state": "FAIL"},
        },
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    calls = []

    def fake_stage0(*a, **k):
        calls.append("stage0")
        return 0

    def fake_judge(t, d, model, replay_dir, accept_over_budget, manifest_arg):
        calls.append("judged")
        mm = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        mm["stages"]["judged"] = {"state": "PASS"}
        (run_dir / "manifest.json").write_text(json.dumps(mm), encoding="utf-8")
        return 0

    def fake_gate(t, d, model, replay_dir, accept_over_budget, manifest_arg):
        calls.append("gated")
        mm = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        mm["stages"]["gated"] = {"state": "PASS"}
        (run_dir / "manifest.json").write_text(json.dumps(mm), encoding="utf-8")
        return 0

    def fake_brief(*a, **k):
        calls.append("brief")
        return 0

    monkeypatch.setattr(ddreport, "_do_stage0", fake_stage0)
    monkeypatch.setattr(ddreport, "_do_judge", fake_judge)
    monkeypatch.setattr(ddreport, "_do_gate", fake_gate)
    monkeypatch.setattr(ddreport, "_do_brief", fake_brief)

    try:
        args = argparse.Namespace(
            ticker=ticker, date=date, archetype=None, peers=None, axes_per_batch=2,
            judgment_model=None, full=False, replay_from=None, until="gated",
            resume=True, offline=False, accept_over_budget=False,
        )
        rc = ddreport.cmd_run(args)
        assert rc == 0
        # stage0 已是 PASS，--resume 不該再跑；judged 曾 FAIL，要重跑；
        # gated 之前不存在，跟著跑；brief 不在 --until gated 範圍內不該跑
        assert calls == ["judged", "gated"]
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
