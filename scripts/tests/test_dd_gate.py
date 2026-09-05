#!/usr/bin/env python3
"""測試 `scripts/dd_gate.py`（v17 WP3）。

用 `notes/site-internal/dd/_audit_{BE,CIEN}_20260905.md` 兩份真實 gate 稽核輸出
（形狀分別是散文式與半表格式）當固定樣本，涵蓋：
- parse：red 以首行「判斷級🔴 = N」為準；yellow 排除標「不計」的列（CIEN ⑧）
- parse：散文式 path 從文字內抽出候選 JSON 路徑（BE ②含 supply_demand_durability）
- resolve_path：完整路徑解析、找不到時往上層退、完全找不到時回傳 (None, None)
- patch-prompt：只取 🔴 條目、渲染出的 prompt 含受點名的 judgment 子樹與 evidence finding
- decide：red>0 印 BLOCK exit 1；red=0 印 PASS exit 0

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
NOTES_DIR = ROOT / "notes" / "site-internal" / "dd"
SRC_BE = NOTES_DIR / "_src" / "BE_20260905"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_gate  # noqa: E402


AUDIT_BE = NOTES_DIR / "_audit_BE_20260905.md"
AUDIT_CIEN = NOTES_DIR / "_audit_CIEN_20260905.md"


# ---------------------------------------------------------------------------
# parse
# ---------------------------------------------------------------------------

def test_parse_be_prose_red_and_path():
    result = dd_gate.parse_audit(str(AUDIT_BE))
    assert result["red"] == 1
    reds = [f for f in result["findings"] if f["level"] == "🔴"]
    assert len(reds) == 1
    assert "②" in reds[0]["axis"]
    assert "supply_demand_durability" in reds[0]["path"]


def test_parse_cien_table_red_and_yellow():
    result = dd_gate.parse_audit(str(AUDIT_CIEN))
    assert result["red"] == 0
    assert result["yellow"] == 4
    yellow_axes = "".join(f["axis"] for f in result["findings"] if f["level"] == "🟡")
    # ⑧ 明標「不計判斷級」，不應計入 yellow 計數（但仍可留在 findings 列表內）
    for axis in ("②", "④", "⑥", "⑦"):
        assert axis in yellow_axes


def test_parse_cien_row8_excluded_from_tally_but_present():
    result = dd_gate.parse_audit(str(AUDIT_CIEN))
    row8 = [f for f in result["findings"] if f["axis"].startswith("⑧")]
    assert len(row8) == 1
    assert row8[0]["level"] == "🟡"
    # 若 row8 被誤計入，yellow 會變 5；上一條測試已鎖 4。


def test_parse_json_cli_matches_function(capsys):
    rc = dd_gate.main(["parse", str(AUDIT_CIEN), "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["red"] == 0
    assert data["yellow"] == 4


def test_parse_no_first_line_warns_and_falls_back(tmp_path, capsys):
    p = tmp_path / "audit_no_header.md"
    p.write_text("① 隨便🟢：沒事。\n② 隨便二🔴：出事了 foo.bar[0]。\n", encoding="utf-8")
    result = dd_gate.parse_audit(str(p))
    err = capsys.readouterr().err
    assert "WARNING" in err
    assert result["red"] == 1


# ---------------------------------------------------------------------------
# resolve_path
# ---------------------------------------------------------------------------

def test_resolve_path_exact():
    obj = {"moat": {"threats": [{"a": 1}, {"a": 2}]}}
    value, resolved = dd_gate.resolve_path(obj, "moat.threats[1]")
    assert value == {"a": 2}
    assert resolved == "moat.threats[1]"


def test_resolve_path_backs_off_to_parent():
    obj = {"contradictions": [{"axis": "x"}]}
    # contradictions[5] 不存在（只有 1 條），應退回 contradictions 整個 list
    value, resolved = dd_gate.resolve_path(obj, "contradictions[5]")
    assert resolved == "contradictions"
    assert value == obj["contradictions"]


def test_resolve_path_no_match_returns_none():
    obj = {"a": {"b": 1}}
    value, resolved = dd_gate.resolve_path(obj, "totally.missing[2]")
    assert value is None
    assert resolved is None


def test_resolve_path_list_no_dict_wrapper():
    obj = {"thesis": {"R": [{"id": "R1"}, {"id": "R2"}]}}
    value, resolved = dd_gate.resolve_path(obj, "thesis.R[1]")
    assert value == {"id": "R2"}
    assert resolved == "thesis.R[1]"


# ---------------------------------------------------------------------------
# patch-prompt（用 BE 真實 judgment/evidence fixture）
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not SRC_BE.exists(), reason="BE fixture 缺失")
def test_patch_prompt_be_contains_crossroads(tmp_path):
    out = tmp_path / "patch.md"
    rc = dd_gate.main(
        [
            "patch-prompt",
            "--audit",
            str(AUDIT_BE),
            "--judgment",
            str(SRC_BE / "BE_20260905.judgment.json"),
            "--evidence",
            str(SRC_BE / "BE_20260905.evidence.json"),
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "Crossroads" in text
    assert "BE" in text
    assert "20260905" in text
    # 模板佔位符必須全部被替換，不留 {xxx} 殘跡
    assert "{findings_block}" not in text
    assert "{judgment_path}" not in text
    assert "{ticker}" not in text
    assert "{date}" not in text


@pytest.mark.skipif(not SRC_BE.exists(), reason="BE fixture 缺失")
def test_patch_prompt_only_takes_red_findings(tmp_path):
    out = tmp_path / "patch.md"
    dd_gate.main(
        [
            "patch-prompt",
            "--audit",
            str(AUDIT_BE),
            "--judgment",
            str(SRC_BE / "BE_20260905.judgment.json"),
            "--evidence",
            str(SRC_BE / "BE_20260905.evidence.json"),
            "--out",
            str(out),
        ]
    )
    text = out.read_text(encoding="utf-8")
    # BE 只有一條 🔴（②供需 durability），不應把 🟢/🟡 的軸也當成「發現」條目編號
    assert text.count("🔴") >= 1
    assert "發現 2" not in text


def test_patch_prompt_uses_builtin_template_when_missing(tmp_path):
    judgment = {"meta": {"ticker": "ZZZ", "date": "2026-01-02"}, "contradictions": []}
    evidence = {"coverage": {}}
    jf = tmp_path / "j.json"
    ef = tmp_path / "e.json"
    jf.write_text(json.dumps(judgment, ensure_ascii=False), encoding="utf-8")
    ef.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

    audit = tmp_path / "audit.md"
    audit.write_text("## AUDIT: 判斷級🔴 = 1\n\n① 測試🔴：foo.bar[0] 有問題。\n", encoding="utf-8")

    out = tmp_path / "patch.md"
    rc = dd_gate.main(
        [
            "patch-prompt",
            "--audit",
            str(audit),
            "--judgment",
            str(jf),
            "--evidence",
            str(ef),
            "--out",
            str(out),
            "--template",
            str(tmp_path / "does_not_exist.tmpl"),
        ]
    )
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "ZZZ" in text
    assert "20260102" in text
    assert "{findings_block}" not in text


# ---------------------------------------------------------------------------
# decide
# ---------------------------------------------------------------------------

def test_decide_block_on_red(tmp_path, capsys):
    p = tmp_path / "parsed.json"
    p.write_text(json.dumps({"red": 1, "yellow": 0, "findings": []}), encoding="utf-8")
    rc = dd_gate.main(["decide", str(p)])
    assert rc == 1
    assert "BLOCK" in capsys.readouterr().out


def test_decide_pass_on_zero_red(tmp_path, capsys):
    p = tmp_path / "parsed.json"
    p.write_text(json.dumps({"red": 0, "yellow": 4, "findings": []}), encoding="utf-8")
    rc = dd_gate.main(["decide", str(p)])
    assert rc == 0
    assert "PASS" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# CLI 入口（subprocess，確保 argparse 與 __main__ 正常運作）
# ---------------------------------------------------------------------------

def test_cli_subprocess_parse():
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "dd_gate.py"), "parse", str(AUDIT_BE), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["red"] == 1
