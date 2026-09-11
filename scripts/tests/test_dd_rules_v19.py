#!/usr/bin/env python3
"""測試 `scripts/dd_rules.py`：規則的單一人工來源與 v19 產物（WP-H2-3，2026-09-11）。

釘三件事：
1. **來源改了、產物一定跟著變**——同一支生成器對不同來源產出不同內容與不同版本戳。
2. **產物與來源版本戳不一致就不准組判斷包**——`dd_bundle.py judge --contract v19`
   直接回非零，不是印個警告照跑。
3. **v18 視圖不掉內容**——`render("v18")` 只拿掉標記行與 `only:v19` 段，其餘一字不動。

另有一條護欄測試：repo 內現行的 `judgment-rules-v19.md` 必須是當下來源的產物
（有人手改過或忘了重生，這裡就會紅）。

Python 3.9 相容。
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_bundle  # noqa: E402
import dd_rules  # noqa: E402

SOURCE = """# 標題

共用段落一。

<!-- only:v18 -->
只有 v18 看得到的段落。
<!-- /only -->

<!-- only:v19 -->
只有 v19 看得到的段落。
<!-- /only -->

共用段落二。
"""


def test_render_splits_by_marker():
    v18 = dd_rules.render("v18", source_text=SOURCE)
    v19 = dd_rules.render("v19", source_text=SOURCE)
    assert "只有 v18 看得到的段落。" in v18 and "只有 v18 看得到的段落。" not in v19
    assert "只有 v19 看得到的段落。" in v19 and "只有 v19 看得到的段落。" not in v18
    for text in (v18, v19):
        assert "共用段落一。" in text and "共用段落二。" in text
        assert "only:" not in text and "/only" not in text  # 標記行兩邊都拿掉


def test_render_rejects_unclosed_marker():
    with pytest.raises(ValueError):
        dd_rules.render("v19", source_text="<!-- only:v19 -->\n沒有收尾\n")


def test_source_change_changes_product_and_stamp(tmp_path):
    """核心：產物是**從來源算出來的**，不是另一份人工檔——來源改一個字，產物
    的內容與版本戳都必須跟著變。"""
    src = tmp_path / "rules.md"
    out = tmp_path / "rules-v19.md"
    src.write_text(SOURCE, encoding="utf-8")
    dd_rules.build_v19(out_path=out, source_path=src)
    first, stamp1 = out.read_text(encoding="utf-8"), dd_rules.source_stamp(src)
    assert "共用段落一。" in first
    assert "由 scripts/dd_rules.py build-v19 產生，勿手改" in first
    assert dd_rules.product_stamp(out) == stamp1

    src.write_text(SOURCE.replace("共用段落一。", "共用段落一（改過）。"), encoding="utf-8")
    assert dd_rules.check(out, src)[0] is False  # 先過期
    dd_rules.build_v19(out_path=out, source_path=src)
    second = out.read_text(encoding="utf-8")
    assert "共用段落一（改過）。" in second and "共用段落一。\n" not in second
    assert dd_rules.product_stamp(out) != stamp1
    assert dd_rules.check(out, src)[0] is True


def test_check_flags_handwritten_product(tmp_path):
    src = tmp_path / "rules.md"
    out = tmp_path / "rules-v19.md"
    src.write_text(SOURCE, encoding="utf-8")
    out.write_text("# 有人手寫的一份\n", encoding="utf-8")
    ok, msg = dd_rules.check(out, src)
    assert ok is False and "沒有版本戳" in msg


def test_repo_product_is_current():
    """repo 內現行的 v19 規則產物必須是當下來源的產物（pre-commit 也擋這件事，
    這條測試讓忘記重生在 CI／本機測試階段就紅）。"""
    ok, msg = dd_rules.check()
    assert ok, msg


def test_judge_bundle_refuses_stale_rules_product(tmp_path, monkeypatch, capsys):
    """版本戳對不上時 `cmd_judge` 回非零並且不寫 bundle——拿過期規則去判斷，
    錯在哪不會有人發現，所以這裡是擋不是警告。"""
    shutil.copyfile(FIXTURES / "evidence_FIX_20260911.json", tmp_path / "evidence.json")
    shutil.copyfile(FIXTURES / "facts_FIX_20260911.json", tmp_path / "facts.json")
    stale = tmp_path / "judgment-rules-v19.md"
    stale.write_text("<!-- generated-from: x sha256:0000000000000000 -->\n舊產物\n", encoding="utf-8")
    monkeypatch.setattr(dd_bundle, "JUDGMENT_RULES_V19_PATH", stale)
    out = tmp_path / "judge.md"
    args = argparse.Namespace(run_dir=str(tmp_path), evidence=None, digest=None, transcript=None,
                              judgment_rules=None, facts=None, contract="v19", out=str(out))
    assert dd_bundle.cmd_judge(args) == 1
    assert not out.exists()
    assert "v19 規則產物過期" in capsys.readouterr().err


def test_v18_bundle_carries_v18_view_not_markers(tmp_path):
    """v18 判斷包讀的是 `render("v18")` 的視圖：標記行與 v19 專屬段都不該漏進去，
    但 v18 自己的段落一條不少。"""
    shutil.copyfile(FIXTURES / "evidence_FIX_20260911.json", tmp_path / "evidence.json")
    out = tmp_path / "judge_v18.md"
    args = argparse.Namespace(run_dir=str(tmp_path), evidence=None, digest=None, transcript=None,
                              judgment_rules=None, facts=None, contract="v18", out=str(out))
    assert dd_bundle.cmd_judge(args) == 0
    text = out.read_text(encoding="utf-8")
    assert "<!-- only:v18 -->" not in text and "<!-- only:v19 -->" not in text
    assert "你是誰：v18判斷階段" in text            # v18 專屬段在
    assert "你是誰：v19判斷階段" not in text        # v19 專屬段不在
    assert "北極星" in text                          # 共用段在


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
