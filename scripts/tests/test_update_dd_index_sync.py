#!/usr/bin/env python3
"""2026-09-07：DD 必須同步集合的回傳碼測試。"""
from __future__ import annotations

import sys
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import update_dd_index  # noqa: E402


def test_update_dd_index_research_failure_returns_nonzero(monkeypatch, capsys):
    # 2026-09-07：research 主表寫入失敗不得再以 Python 預設 rc=0 結束。
    monkeypatch.setattr(update_dd_index, "parse_index_md", lambda: {})
    monkeypatch.setattr(update_dd_index, "scan_files", lambda index_data: [])
    monkeypatch.setattr(update_dd_index, "update_index", lambda *a, **k: False)
    monkeypatch.setattr(sys, "argv", ["update_dd_index.py"])

    assert update_dd_index.main() != 0
    captured = capsys.readouterr()
    assert "[sync-summary] FAIL 必須同步：research 主表未更新" in captured.err


def test_update_dd_index_summary_keeps_optional_failures_nonfatal(capsys):
    # 2026-09-07：非必要 cascade 只列 WARN，不改必要集合的成功 rc。
    assert update_dd_index._emit_sync_result([], ["build_picks.py exit 1"]) == 0
    captured = capsys.readouterr()
    assert "必須同步：PASS" in captured.out
    assert "[sync-summary] WARN 非必要同步：build_picks.py exit 1" in captured.err


def test_update_dd_index_screener_failure_returns_nonzero(monkeypatch, capsys):
    # 2026-09-07：screener 子行程失敗屬必要同步失敗，不能只留下 warning。
    monkeypatch.setattr(update_dd_index, "parse_index_md", lambda: {})
    monkeypatch.setattr(update_dd_index, "scan_files", lambda index_data: [])
    monkeypatch.setattr(update_dd_index, "update_index", lambda *a, **k: True)
    monkeypatch.setattr(update_dd_index, "inject_asym_flags", lambda *a, **k: 0)

    def fake_run(cmd, *args, **kwargs):
        if str(cmd[1]).endswith("build_dd_screener.py"):
            raise subprocess.CalledProcessError(7, cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["update_dd_index.py"])

    assert update_dd_index.main() != 0
    assert "[sync-summary] FAIL 必須同步：dd-screener rebuild exit 7" in capsys.readouterr().err


def test_update_dd_index_skip_screener_is_successful_maintenance(monkeypatch, capsys):
    # 2026-09-07：單獨 maintenance 可略過 screener，但不得宣稱發布級同步。
    monkeypatch.setattr(update_dd_index, "parse_index_md", lambda: {})
    monkeypatch.setattr(update_dd_index, "scan_files", lambda index_data: [])
    monkeypatch.setattr(update_dd_index, "update_index", lambda *a, **k: True)
    monkeypatch.setattr(
        subprocess, "run", lambda cmd, *a, **k: subprocess.CompletedProcess(cmd, 0))
    monkeypatch.setattr(sys, "argv", ["update_dd_index.py", "--skip-dd-screener"])

    assert update_dd_index.main() == 0
    output = capsys.readouterr().out
    assert "本次不是發布級同步" in output
    assert "latest.json 未重建" in output
