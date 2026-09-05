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
        # a_1 每次都「成功交出」part 檔（模擬正常完成）；a_2 從不寫出檔案
        # （模擬撞輪次上限、從未 Write 出產物）——驗證新版重派候選判斷
        # （needs 清單 ∪ 檔案缺件）不會把已交件的 a_1 誤重派。
        for s in specs:
            if s["id"] == "a_1":
                (run_dir / "parts" / "axes_1.json").write_text("{}", encoding="utf-8")
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


def test_stage0_first_run_respawns_once_when_part_file_never_written(monkeypatch):
    """WP8 待補 #4：首跑 finalize FAIL 若是因為某 spec 撞輪次上限、從未
    Write 出 part 檔（`dd_evidence.py finalize` 的「需重派」清單只涵蓋
    『檔案存在但驗證不合格』，不含『整批沒交出來』，故 `needs` 對這種缺件
    是空集合）——舊版 `while needs and rc != 0` 因 `needs` 為空而完全不進
    迴圈、retries 卡在 0 就直接停（STRL 首跑 a_2/a_5 實測症狀）。新版改用
    `_respawn_candidates`（needs ∪ 檔案缺件）判斷，應該還是會重派一次；
    這裡讓重派後 a_2 補寫出檔案、finalize 轉 PASS，驗證 retries 計數為 1
    且整段最終 PASS（不是「仍 FAIL 才停」的另一半，那半由前一個測試涵蓋）。
    """
    ticker, date = "ZTESTFIRSTRETRY", "20260101"
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
        ids = [s["id"] for s in specs]
        spawn_many_calls.append(ids)
        for s in specs:
            if s["id"] == "a_1":
                (run_dir / "parts" / "axes_1.json").write_text("{}", encoding="utf-8")
            elif s["id"] == "a_2" and len(spawn_many_calls) >= 2:
                # 第一次撞輪次上限、什麼都沒寫；重派（第二次派工）才補上。
                (run_dir / "parts" / "axes_2.json").write_text("{}", encoding="utf-8")
        return [{"ok": True, "over_budget": False, "num_turns": 1, "id": s["id"]} for s in specs]

    monkeypatch.setattr(ddreport.dd_headless, "spawn_many", fake_spawn_many)

    finalize_calls = {"n": 0}

    def fake_finalize(run_dir_arg):
        finalize_calls["n"] += 1
        axes2 = run_dir / "parts" / "axes_2.json"
        if axes2.exists():
            return 0, "finalize PASS #{0}".format(finalize_calls["n"]), set()
        # a_2 檔案根本不存在——`dd_evidence.py finalize` 的「需重派」清單
        # 只列「檔案在但驗證不合格」，故這裡回傳空 needs 集合模擬真實症狀。
        return 1, "finalize FAIL #{0}".format(finalize_calls["n"]), set()

    monkeypatch.setattr(ddreport, "_finalize_run_dir", fake_finalize)

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {}}
        plan_kwargs = {"archetype": None, "peers": None, "segments": None,
                       "axes_per_batch": 2, "offline": True}
        rc = ddreport._do_stage0(ticker, date, plan_kwargs, None, False, manifest)

        assert rc == 0
        assert finalize_calls["n"] == 2  # 首次 FAIL + 重派後一次 PASS

        m = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert m["stages"]["stage0"]["state"] == "PASS"
        assert m["stages"]["stage0"]["finalize_retries"] == 1

        assert spawn_many_calls[0] == ["a_1", "a_2"]
        # 重派只挑缺件的 a_2，不重派已交件的 a_1
        assert spawn_many_calls[1] == ["a_2"]
        assert len(spawn_many_calls) == 2
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

    def fake_resume_judge(t, d, model, replay_dir, accept_over_budget, manifest_arg):
        # WP7b #5：`judged_fail` 狀態下 --resume 應叫 `_resume_judge_stage`
        # （先重跑 judge check），不是直接重派整段判斷的 `_do_judge`。
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

    def _unexpected_do_judge(*a, **k):
        raise AssertionError("judged_fail 下 --resume 不該直接呼叫 _do_judge（應先走 _resume_judge_stage）")

    monkeypatch.setattr(ddreport, "_do_stage0", fake_stage0)
    monkeypatch.setattr(ddreport, "_do_judge", _unexpected_do_judge)
    monkeypatch.setattr(ddreport, "_resume_judge_stage", fake_resume_judge)
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


# ---------------------------------------------------------------------------
# 5) WP7a #1：Koyfin 步驟改零 LLM——`_run_koyfin_step` 直接 subprocess，不再
#    走 spawn；輸出 parts/transcripts.json 並 merge 進 evidence.json。
# ---------------------------------------------------------------------------

def test_run_koyfin_step_zero_llm_writes_transcripts_and_merges(tmp_path, monkeypatch):
    ticker, date = "ZKOYFIN", "20260101"
    run_dir = tmp_path / "run"
    (run_dir / "parts").mkdir(parents=True)
    evidence_dest = run_dir / "evidence.json"
    evidence_dest.write_text(json.dumps({"ticker": ticker, "transcripts": {}}), encoding="utf-8")

    drive_dir = tmp_path / "drive" / ticker
    drive_dir.mkdir(parents=True)
    (drive_dir / "Q1.md").write_text("q1", encoding="utf-8")
    (drive_dir / "Q2.md").write_text("q2", encoding="utf-8")

    fake_selector = tmp_path / "selector.py"
    fake_selector.write_text("", encoding="utf-8")

    monkeypatch.setattr(ddreport, "KOYFIN_DOWNLOADER", tmp_path / "no_such_downloader.py")
    monkeypatch.setattr(ddreport, "KOYFIN_SELECTOR", fake_selector)
    monkeypatch.setattr(ddreport, "_find_koyfin_drive_folder", lambda t: drive_dir)

    def fake_run(cmd, **kw):
        cmd = [str(c) for c in cmd]
        if cmd[1].endswith("selector.py"):
            payload = json.dumps({
                "ticker": ticker, "mode": "first-run",
                "must_read": ["Q1.md", "Q2.md"], "optional_read": [],
                "must_read_tokens_total": 100,
            })
            return _FakeCompleted(0, stdout=payload)
        if "dd_evidence.py" in cmd[1] and "merge" in cmd:
            # 忠實模擬 dd_evidence.py merge：把 part 檔淺層併進 evidence.json
            file_arg, part_arg = cmd[-2], cmd[-1]
            base = json.loads(Path(file_arg).read_text(encoding="utf-8"))
            part = json.loads(Path(part_arg).read_text(encoding="utf-8"))
            base.update(part)
            Path(file_arg).write_text(json.dumps(base), encoding="utf-8")
            return _FakeCompleted(0)
        return _FakeCompleted(0)

    monkeypatch.setattr(ddreport.subprocess, "run", fake_run)

    manifest = {"steps": []}
    result = ddreport._run_koyfin_step(ticker, date, run_dir, evidence_dest, manifest)

    assert result["transcripts"]["koyfin_session_status"] == "downloader_missing"
    sel = result["transcripts"]["selected"]
    assert sel["recent_four_quarters"] == [str(drive_dir / "Q1.md"), str(drive_dir / "Q2.md")]
    assert sel["high_signal_optional"] == []

    out = json.loads((run_dir / "parts" / "transcripts.json").read_text(encoding="utf-8"))
    assert out["transcripts"]["selected"]["recent_four_quarters"] == sel["recent_four_quarters"]

    merged = json.loads(evidence_dest.read_text(encoding="utf-8"))
    assert merged["transcripts"]["selected"]["recent_four_quarters"] == sel["recent_four_quarters"]
    assert manifest["koyfin_session_status"] == "downloader_missing"


# ---------------------------------------------------------------------------
# 6) WP7a #3：peers 來源優先順序 --peers → archive(_src) → id-meta → 都沒有
# ---------------------------------------------------------------------------

def test_resolve_peers_cli_takes_priority():
    peers, src = ddreport._resolve_peers("AMD,NVDA", "AVGO")
    assert (peers, src) == ("AMD,NVDA", "cli")


def test_resolve_peers_falls_back_to_archive(tmp_path, monkeypatch):
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", tmp_path)
    monkeypatch.setattr(ddreport, "ID_DIR", tmp_path / "no_such_id_dir")

    run_dir = tmp_path / "ZPEER_20260101"
    run_dir.mkdir()
    ev_path = run_dir / "ZPEER_20260101.evidence.json"
    ev_path.write_text(json.dumps({
        "numbers": {"peer_financials": {
            "ZPEER": {"gm": 1}, "AMD": {"gm": 2}, "NVDA": {"gm": 3}, "_note": "x",
        }},
    }), encoding="utf-8")

    peers, src = ddreport._resolve_peers(None, "ZPEER")
    assert src == "archive"
    assert set(peers.split(",")) == {"AMD", "NVDA"}


def test_resolve_peers_falls_back_to_id_meta(tmp_path, monkeypatch):
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", tmp_path / "no_such_archive")
    fake_id_dir = tmp_path / "id"
    fake_id_dir.mkdir()
    monkeypatch.setattr(ddreport, "ID_DIR", fake_id_dir)

    def fake_find(id_dir, ticker):
        assert ticker == "ZPEER"
        return [(fake_id_dir / "ID_Fake.html", {
            "related_tickers": [
                {"ticker": "ZPEER"}, {"ticker": "AMD"}, {"ticker": "NVDA"},
                {"ticker": "MU"}, {"ticker": "WDC"}, {"ticker": "STX"},
            ],
        })]

    monkeypatch.setattr(ddreport.dd_meta_reader, "find_ids_for_ticker", fake_find)
    peers, src = ddreport._resolve_peers(None, "ZPEER")
    assert src == "id_meta"
    assert peers.split(",") == ["AMD", "NVDA", "MU", "WDC"]


def test_resolve_peers_none_when_all_sources_exhausted(tmp_path, monkeypatch):
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", tmp_path / "no_archive")
    monkeypatch.setattr(ddreport, "ID_DIR", tmp_path / "no_id")
    peers, src = ddreport._resolve_peers(None, "ZPEER")
    assert (peers, src) == (None, None)


# ---------------------------------------------------------------------------
# 7) cmd_plan：peers 都沒有時（非 offline）印錯誤並提早退出，不跑
#    dd_numbers_extra.py
# ---------------------------------------------------------------------------

def test_cmd_plan_aborts_when_no_peers_resolved_and_not_offline(monkeypatch):
    ticker, date = "ZPLANNOPEER", "20260101"
    run_dir = _clean_run_dir(ticker, date)

    monkeypatch.setattr(ddreport, "_resolve_peers", lambda cli, t: (None, None))

    try:
        args = argparse.Namespace(
            ticker=ticker, date=date, archetype="品質複利成長", peers=None,
            segments=None, axes_per_batch=2, offline=False,
        )
        rc = ddreport.cmd_plan(args)
        assert rc == 1
        assert not (run_dir / "parts" / "numbers_extra.json").exists()
        assert not (run_dir / "spawn_list.json").exists()
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# 8) WP7b #1：bundle（或修補時的 judgment.json 全文）內嵌進 prompt，
#    分隔行 `===== BUNDLE =====`，agent 不必自己 Read 大檔。
# ---------------------------------------------------------------------------

def test_write_inline_prompt_appends_bundle_after_separator(tmp_path):
    prompt_path = tmp_path / "b1_judge.md"
    prompt_path.write_text("這是渲染後的 prompt 本文。", encoding="utf-8")
    bundle_path = tmp_path / "bundle.md"
    bundle_path.write_text("這是 bundle 全文，含 {大括號} 也不影響。", encoding="utf-8")

    inline_path = ddreport._write_inline_prompt(prompt_path, bundle_path)

    assert inline_path.name == "b1_judge_inline.md"
    text = inline_path.read_text(encoding="utf-8")
    assert "===== BUNDLE =====" in text
    assert (
        text.index("這是渲染後的 prompt 本文。")
        < text.index("===== BUNDLE =====")
        < text.index("這是 bundle 全文")
    )


def test_write_inline_prompt_missing_extra_file_writes_empty_tail(tmp_path):
    prompt_path = tmp_path / "g_gate.md"
    prompt_path.write_text("base prompt", encoding="utf-8")
    inline_path = ddreport._write_inline_prompt(prompt_path, tmp_path / "no_such_bundle.md")
    text = inline_path.read_text(encoding="utf-8")
    assert text == "base prompt" + ddreport.BUNDLE_SEPARATOR


def test_do_judge_spawns_inline_prompt_with_bundle(monkeypatch):
    ticker, date = "ZTESTINLINEJ", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "agents").mkdir(parents=True)
    (run_dir / "bundles").mkdir(parents=True)
    (run_dir / "bundles" / "judge.md").write_text("JUDGE-BUNDLE-CONTENT-MARKER", encoding="utf-8")

    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: _FakeCompleted(0))
    monkeypatch.setattr(ddreport, "_pick_python", lambda: "python3")
    spawn_calls = []

    def fake_spawn(**kw):
        spawn_calls.append(kw)
        return {"ok": True, "over_budget": False, "num_turns": 1, "cache_read": 0}

    monkeypatch.setattr(ddreport.dd_headless, "spawn", fake_spawn)
    monkeypatch.setattr(ddreport, "_judge_check", lambda t, d: (True, "[PASS] 假造：judge check ok"))

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {}}
        rc = ddreport._do_judge(ticker, date, "fable", None, False, manifest)
        assert rc == 0
        assert len(spawn_calls) == 1
        prompt_path = Path(spawn_calls[0]["prompt_path"])
        assert prompt_path.name == "b1_judge_inline.md"
        text = prompt_path.read_text(encoding="utf-8")
        assert "===== BUNDLE =====" in text
        assert "JUDGE-BUNDLE-CONTENT-MARKER" in text
        assert "不要 Read" in text
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def test_do_gate_patch_branch_spawns_inline_prompt_with_judgment(monkeypatch):
    ticker, date = "ZTESTINLINEG", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "agents").mkdir(parents=True)
    (run_dir / "bundles").mkdir(parents=True)
    (run_dir / "bundles" / "gate.md").write_text("GATE-BUNDLE-CONTENT-MARKER", encoding="utf-8")
    (run_dir / "judgment.json").write_text(
        json.dumps({"decision_out": {"verdict": "進場"}}), encoding="utf-8")
    (run_dir / "evidence.json").write_text("{}", encoding="utf-8")
    audit_path = run_dir / "gate_audit.md"
    audit_path.write_text(
        "## AUDIT: 判斷級🔴 = 1\n\n"
        "| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |\n|---|---|---|---|---|---|\n"
        "| 1 | 競爭惡化 | 🔴 | 測試 | contradictions[0] | 補一條 |\n",
        encoding="utf-8",
    )

    def fake_subprocess_run(cmd, *a, **k):
        prog = str(cmd[1])
        if prog.endswith("dd_bundle.py"):
            return _FakeCompleted(0)
        if prog.endswith("dd_gate.py") and "patch-prompt" in cmd:
            out_path = Path(cmd[cmd.index("--out") + 1])
            out_path.write_text(
                "你是 stock-analyst v17 判斷 agent，回來做一輪定點修補。\n\n"
                "## 讀（判斷物全文附於本訊息之後，不要 Read 任何檔）\n",
                encoding="utf-8",
            )
            return _FakeCompleted(0)
        if prog.endswith("dd_gate.py") and "parse" in cmd:
            return _FakeCompleted(0, stdout=json.dumps({"red": 1, "yellow": 0, "findings": []}))
        raise AssertionError("未預期的 subprocess.run 呼叫：{0}".format(cmd))

    monkeypatch.setattr(ddreport.subprocess, "run", fake_subprocess_run)
    monkeypatch.setattr(ddreport, "_pick_python", lambda: "python3")

    spawn_calls = []

    def fake_spawn(**kw):
        spawn_calls.append(kw)
        return {"ok": True, "over_budget": False, "num_turns": 1, "cache_read": 0}

    monkeypatch.setattr(ddreport.dd_headless, "spawn", fake_spawn)
    monkeypatch.setattr(ddreport, "_judge_check", lambda t, d: (True, "[PASS] 假造"))
    monkeypatch.setattr(ddreport, "_read_decision_verdict", lambda rd: "進場")

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {}}
        rc = ddreport._do_gate(ticker, date, "fable", None, False, manifest)
        assert rc == 0
        # 第一個 spawn 是 gate 稽核本身、第二個是 patch agent
        assert len(spawn_calls) == 2
        patch_prompt_path = Path(spawn_calls[1]["prompt_path"])
        assert patch_prompt_path.name == "b1_patch_inline.md"
        text = patch_prompt_path.read_text(encoding="utf-8")
        assert "===== BUNDLE =====" in text
        assert '"decision_out"' in text  # judgment.json 全文接在分隔行之後
        assert "不要 Read" in text
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# 9) WP7b #5：`--resume` 在 `judged_fail` 狀態下先重跑 judge check（判斷物
#    可能已被機械修正），PASS 就不派 agent，FAIL 才派修補 agent（不是重派
#    整段判斷 agent）。
# ---------------------------------------------------------------------------

def test_resume_judge_stage_precheck_passes_without_any_agent(monkeypatch):
    ticker, date = "ZTESTRESUMEJ1", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "agents").mkdir(parents=True)

    spawn_calls = []
    monkeypatch.setattr(
        ddreport.dd_headless, "spawn",
        lambda **kw: spawn_calls.append(kw) or {"ok": True, "over_budget": False, "num_turns": 1},
    )
    monkeypatch.setattr(ddreport, "_judge_check", lambda t, d: (True, "[PASS] 假造：機械已修正過"))

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {"judged": {"state": "FAIL", "agent_usage": []}}}
        rc = ddreport._resume_judge_stage(ticker, date, "fable", None, False, manifest)
        assert rc == 0
        assert spawn_calls == []  # 不派任何 agent（既有判斷物免修即過）
        m = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert m["stages"]["judged"]["state"] == "PASS"
        assert m["state"] == "judged_pass"
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def test_resume_judge_stage_precheck_fail_dispatches_fix_only(monkeypatch):
    ticker, date = "ZTESTRESUMEJ2", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "agents").mkdir(parents=True)

    spawn_calls = []

    def fake_spawn(**kw):
        spawn_calls.append(kw)
        return {"ok": True, "over_budget": False, "num_turns": 1}

    monkeypatch.setattr(ddreport.dd_headless, "spawn", fake_spawn)

    check_results = iter([(False, "[FAIL] 缺 evidence_dismissed"), (True, "[PASS] 修好了")])
    monkeypatch.setattr(ddreport, "_judge_check", lambda t, d: next(check_results))

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {"judged": {"state": "FAIL", "agent_usage": []}}}
        rc = ddreport._resume_judge_stage(ticker, date, "fable", None, False, manifest)
        assert rc == 0
        # 只派一次「定點修正」agent，不是整段判斷 agent（那需要先建 bundle、
        # 呼叫 dd_bundle.py，這裡完全沒 monkeypatch subprocess.run，若誤呼叫
        # 整段流程會在 dd_bundle.py 真的跑之前就因為找不到 evidence.json 等
        # 檔案而以不同方式失敗，不會静默通過）
        assert len(spawn_calls) == 1
        assert spawn_calls[0]["max_turns"] == ddreport.JUDGE_FIX_MAX_TURNS
        m = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert m["stages"]["judged"]["state"] == "PASS"
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def test_resume_gate_stage_parses_existing_audit_without_respawn(monkeypatch):
    ticker, date = "ZTESTRESUMEG1", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "agents").mkdir(parents=True)
    (run_dir / "gate_audit.md").write_text(
        "## AUDIT: 判斷級🔴 = 0\n\n"
        "| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |\n|---|---|---|---|---|---|\n",
        encoding="utf-8",
    )

    spawn_calls = []
    monkeypatch.setattr(
        ddreport.dd_headless, "spawn",
        lambda **kw: spawn_calls.append(kw) or {"ok": True, "over_budget": False, "num_turns": 1},
    )
    monkeypatch.setattr(
        ddreport.subprocess, "run",
        lambda cmd, *a, **k: _FakeCompleted(0, stdout=json.dumps({"red": 0, "yellow": 0, "findings": []})),
    )

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {"gated": {"state": "RUNNING", "agent_usage": []}}}
        rc = ddreport._resume_gate_stage(ticker, date, "fable", None, False, manifest)
        assert rc == 0
        assert spawn_calls == []  # red=0，不需要 patch agent，也沒有重跑 gate spawn
        m = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assert m["stages"]["gated"]["state"] == "PASS"
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def test_resume_gate_stage_falls_back_to_full_gate_when_no_audit(monkeypatch):
    ticker, date = "ZTESTRESUMEG2", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    run_dir.mkdir(parents=True)

    calls = []

    def fake_do_gate(t, d, model, replay_dir, accept_over_budget, manifest_arg):
        calls.append("do_gate")
        return 0

    monkeypatch.setattr(ddreport, "_do_gate", fake_do_gate)

    try:
        manifest = {"ticker": ticker, "date": date, "stages": {"gated": {"state": "FAIL", "agent_usage": []}}}
        rc = ddreport._resume_gate_stage(ticker, date, "fable", None, False, manifest)
        assert rc == 0
        assert calls == ["do_gate"]
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def test_run_resume_from_judged_fail_calls_precheck_not_full_judge(monkeypatch):
    """端到端一層：`cmd_run` 在 manifest state 為 judged_fail 時，資派給
    `_resume_judge_stage` 而不是 `_do_judge`（見上方 test_run_resume_
    skips_completed_stages 對同一情境的既有斷言；本測試額外鎖定
    `resuming_this_stage` 判斷式本身，避免日後改動誤判 gated 也吃到
    judged 的規則或反過來）。"""
    ticker, date = "ZTESTRESUMEDISPATCH", "20260101"
    run_dir = _clean_run_dir(ticker, date)
    run_dir.mkdir(parents=True)
    manifest = {
        "ticker": ticker, "date": date, "state": "judged_fail",
        "stages": {"stage0": {"state": "PASS"}, "judged": {"state": "FAIL"}},
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    calls = []

    def fake_resume_judge(t, d, model, replay_dir, accept_over_budget, manifest_arg):
        calls.append("resume_judge")
        mm = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        mm["stages"]["judged"] = {"state": "PASS"}
        (run_dir / "manifest.json").write_text(json.dumps(mm), encoding="utf-8")
        return 0

    def _unexpected(*a, **k):
        raise AssertionError("不該呼叫")

    monkeypatch.setattr(ddreport, "_resume_judge_stage", fake_resume_judge)
    monkeypatch.setattr(ddreport, "_do_judge", _unexpected)
    monkeypatch.setattr(ddreport, "_do_stage0", _unexpected)

    try:
        args = argparse.Namespace(
            ticker=ticker, date=date, archetype=None, peers=None, axes_per_batch=2,
            judgment_model=None, full=False, replay_from=None, until="judged",
            resume=True, offline=False, accept_over_budget=False,
        )
        rc = ddreport.cmd_run(args)
        assert rc == 0
        assert calls == ["resume_judge"]
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# 6) WP7d：摘要子 agent 拆成一篇一個 spawn（a2_{k}）＋零 LLM 合併回 digest.json
# ---------------------------------------------------------------------------

def test_merge_digest_parts_combines_per_file_parts_into_digest_json(tmp_path):
    run_dir = tmp_path / "run"
    (run_dir / "parts").mkdir(parents=True)
    (run_dir / "parts" / "digest_1.json").write_text(json.dumps({
        "source_files": ["A.md"],
        "items": [{"topic": "guidance", "claim": "c1", "quote": "q1",
                    "speaker": "CFO", "date": "2026-01-01", "file": "A.md"}],
        "qa_flags": [{"question": "q?", "response_pattern": "評避", "file": "A.md"}],
    }), encoding="utf-8")
    (run_dir / "parts" / "digest_2.json").write_text(json.dumps({
        "source_files": ["B.md"],
        "items": [{"topic": "margin", "claim": "c2", "quote": "q2",
                    "speaker": "CEO", "date": "2026-02-01", "file": "B.md"}],
        "qa_flags": [],
    }), encoding="utf-8")
    # 非 digest part（如 axes_1.json）不該被誤吃進來
    (run_dir / "parts" / "axes_1.json").write_text(json.dumps({"coverage": {}}), encoding="utf-8")

    merged = ddreport._merge_digest_parts(run_dir)

    assert merged["source_files"] == ["A.md", "B.md"]
    assert [it["claim"] for it in merged["items"]] == ["c1", "c2"]
    assert len(merged["qa_flags"]) == 1

    on_disk = json.loads((run_dir / "digest.json").read_text(encoding="utf-8"))
    assert on_disk == merged


def test_merge_digest_parts_empty_when_no_digest_parts(tmp_path):
    run_dir = tmp_path / "run"
    (run_dir / "parts").mkdir(parents=True)

    merged = ddreport._merge_digest_parts(run_dir)

    assert merged == {"source_files": [], "items": [], "qa_flags": []}


@pytest.mark.skipif(not CIEN_FIXTURE.exists(), reason="CIEN_20260905 回溯 fixture 不存在")
def test_plan_spawns_one_digest_agent_per_transcript_not_a2_digest(monkeypatch):
    """CIEN fixture 的 evidence.json `selected.recent_four_quarters` 有 4 篇，
    去掉最後一篇（最新一季）剩 3 篇、`high_signal_optional` 為空 → 應該產生
    `a2_1`／`a2_2`／`a2_3` 三個 spawn，絕不再有單一的 `a2_digest`。"""
    ticker, date = "CIEN", "20260905"
    run_dir = _clean_run_dir(ticker, date)
    monkeypatch.setenv("DD_REPLAY_FROM", str(CIEN_FIXTURE))
    try:
        args = argparse.Namespace(
            ticker=ticker, date=date, archetype=None, peers=None, segments=None,
            axes_per_batch=2, offline=True,
        )
        rc = ddreport.cmd_plan(args)
        assert rc == 0

        spawn_list = json.loads((run_dir / "spawn_list.json").read_text(encoding="utf-8"))
        ids = [s["id"] for s in spawn_list]
        assert "a2_digest" not in ids
        digest_ids = sorted(i for i in ids if i.startswith("a2_"))
        assert digest_ids == ["a2_1", "a2_2", "a2_3"]
        for s in spawn_list:
            if s["id"] in digest_ids:
                assert s["max_turns"] == ddreport.DIGEST_PER_FILE_MAX_TURNS
                assert s["budget_cache_read"] == ddreport.BUDGET_CACHE_READ_DIGEST_PER_FILE
                assert s["out"] == "parts/digest_{0}.json".format(s["id"].split("_", 1)[1])

        targets = json.loads((run_dir / "digest_targets.json").read_text(encoding="utf-8"))
        assert [t["id"] for t in targets] == ["a2_1", "a2_2", "a2_3"]
    finally:
        monkeypatch.delenv("DD_REPLAY_FROM", raising=False)
        shutil.rmtree(run_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
