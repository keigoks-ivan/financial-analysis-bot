#!/usr/bin/env python3
"""測試 `scripts/dd_brief.py`（v17 WP4a：零 LLM 速判渲染）。

用四份回溯 fixture（notes/site-internal/dd/_src/{BE_20260905,CIEN_20260905,
CRDO_20260904,PANW_20260904}/）當固定樣本，涵蓋：
- CLI 兩種形狀都能跑（--judgment/--scenario-meta/--evidence 三檔法；--run-dir 目錄法）
- dd-meta 欄位與同一份 judgment 產出的真正上站 DD（docs/dd/DD_{T}.html）逐欄比對，
  必須全同（brief 只是零 LLM 重渲染，不應改變任何裁決欄位）
- qc.py 全形標點／結構檢查通過
- 缺值不崩：一份只剩 meta 的最小 judgment.json 仍能渲染出合法 HTML

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
NOTES_DIR = ROOT / "notes" / "site-internal" / "dd"
SRC_DIR = NOTES_DIR / "_src"
DOCS_DD = ROOT / "docs" / "dd"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_brief  # noqa: E402

TICKERS = ["BE_20260905", "CIEN_20260905", "CRDO_20260904", "PANW_20260904"]

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.S
)


def _extract_dd_meta(html_text: str) -> dict:
    m = DD_META_RE.search(html_text)
    assert m, "dd-meta script block missing"
    return json.loads(m.group(1))


def _run_cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "dd_brief.py")] + args,
        capture_output=True, text=True, cwd=cwd or ROOT,
    )


@pytest.mark.parametrize("t", TICKERS)
def test_three_file_cli_matches_live_dd_meta(t, tmp_path):
    src = SRC_DIR / t
    live_dd = DOCS_DD / f"DD_{t}.html"
    if not live_dd.exists():
        pytest.skip(f"no live DD for {t}")
    out = tmp_path / f"{t}.html"
    r = _run_cli([
        "--judgment", str(src / f"{t}.judgment.json"),
        "--scenario-meta", str(src / f"{t}.scenario_meta.json"),
        "--evidence", str(src / f"{t}.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    assert out.exists()
    html_text = out.read_text(encoding="utf-8")

    brief_meta = _extract_dd_meta(html_text)
    live_meta = _extract_dd_meta(live_dd.read_text(encoding="utf-8"))
    assert brief_meta.get("brief") is True

    diff = {
        k: (brief_meta.get(k), live_meta.get(k))
        for k in live_meta
        if k != "brief" and brief_meta.get(k) != live_meta.get(k)
    }
    assert diff == {}, f"{t} dd-meta 欄位不同：{diff}"


@pytest.mark.parametrize("t", TICKERS)
def test_run_dir_cli_shape(t, tmp_path):
    src = SRC_DIR / t
    run_dir = tmp_path / t
    run_dir.mkdir()
    (run_dir / "judgment.json").write_text(
        (src / f"{t}.judgment.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (run_dir / "scenario_meta.json").write_text(
        (src / f"{t}.scenario_meta.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (run_dir / "evidence.json").write_text(
        (src / f"{t}.evidence.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    out = run_dir / "brief.html"
    r = _run_cli(["--run-dir", str(run_dir), "--out", str(out)])
    assert r.returncode == 0, r.stderr
    assert out.exists()
    meta = _extract_dd_meta(out.read_text(encoding="utf-8"))
    assert meta.get("brief") is True
    assert meta.get("ticker") == t.split("_")[0]


@pytest.mark.parametrize("t", TICKERS)
def test_qc_passes(t, tmp_path):
    src = SRC_DIR / t
    out = tmp_path / f"{t}.html"
    r = _run_cli([
        "--judgment", str(src / f"{t}.judgment.json"),
        "--scenario-meta", str(src / f"{t}.scenario_meta.json"),
        "--evidence", str(src / f"{t}.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    qc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "qc.py"), str(out)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert qc.returncode == 0, qc.stdout + qc.stderr
    assert "QC passed" in qc.stdout


def test_gate_audit_yellow_section_renders(tmp_path):
    audit = NOTES_DIR / "_audit_BE_20260905.md"
    if not audit.exists():
        pytest.skip("no _audit_BE_20260905.md fixture")
    src = SRC_DIR / "BE_20260905"
    out = tmp_path / "BE_with_audit.html"
    r = _run_cli([
        "--judgment", str(src / "BE_20260905.judgment.json"),
        "--scenario-meta", str(src / "BE_20260905.scenario_meta.json"),
        "--evidence", str(src / "BE_20260905.evidence.json"),
        "--audit", str(audit),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    m = re.search(r"跨模型閘的黃燈</h2>\s*(.*?)</section>", html_text, re.S)
    assert m, "gate-yellow section missing"
    assert "本次未提供 gate audit" not in m.group(1)


def test_minimal_judgment_does_not_crash(tmp_path):
    """A judgment.json with almost nothing populated must still render valid
    HTML with '—' placeholders, never raise."""
    minimal = {
        "meta": {"ticker": "XX", "date": "2026-09-05", "schema": "v16.0", "company_name": "Test Co"}
    }
    jpath = tmp_path / "min.judgment.json"
    jpath.write_text(json.dumps(minimal), encoding="utf-8")
    out = tmp_path / "min_brief.html"
    r = _run_cli(["--judgment", str(jpath), "--out", str(out)])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "<title>XX 速判 2026-09-05</title>" in html_text
    meta = _extract_dd_meta(html_text)
    assert meta.get("ticker") == "XX"
    assert meta.get("brief") is True
    # no leftover unfilled {{TOKEN}} placeholders
    assert "{{" not in html_text


def test_missing_judgment_file_exits_nonzero(tmp_path):
    out = tmp_path / "nope.html"
    r = _run_cli(["--judgment", str(tmp_path / "does_not_exist.json"), "--out", str(out)])
    assert r.returncode != 0
    assert not out.exists()
