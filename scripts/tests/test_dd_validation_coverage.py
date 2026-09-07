#!/usr/bin/env python3
"""2026-09-07：v17 brief 的 schema／QC／math gate 覆蓋測試。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import qc  # noqa: E402
import validate_dd_meta  # noqa: E402
import verify_dd_math  # noqa: E402


def test_validate_dd_meta_default_targets_include_brief(tmp_path, monkeypatch, capsys):
    # 2026-09-07：無參數 validator 必須同時列舉 DD_ 與 BRIEF_。
    dd_dir = tmp_path / "docs" / "dd"
    brief_dir = dd_dir / "brief"
    brief_dir.mkdir(parents=True)
    full_path = dd_dir / "DD_TEST_20260101.html"
    brief_path = brief_dir / "BRIEF_TEST_20260101.html"
    full_path.write_text("full", encoding="utf-8")
    brief_path.write_text("brief", encoding="utf-8")
    seen = []

    monkeypatch.setattr(validate_dd_meta, "DD_DIR", dd_dir)
    monkeypatch.setattr(validate_dd_meta, "BRIEF_DIR", brief_dir)
    monkeypatch.setattr(
        validate_dd_meta, "validate_file",
        lambda path: seen.append(path) or {"status": "ok"},
    )
    monkeypatch.setattr(sys, "argv", ["validate_dd_meta.py"])

    with pytest.raises(SystemExit) as exc:
        validate_dd_meta.main()
    assert exc.value.code == 0
    assert seen == [full_path, brief_path]
    assert "Scanned 2 DD file(s)" in capsys.readouterr().out


def test_validate_dd_meta_brief_without_head_version_is_not_skipped(tmp_path):
    # 2026-09-07：快速版以檔名進入 gate，不能因沒有 dd-schema-version meta 而 fail-open。
    path = tmp_path / "BRIEF_TEST_20260101.html"
    path.write_text(
        '<script id="dd-meta" type="application/json">{}</script>',
        encoding="utf-8",
    )

    result = validate_dd_meta.validate_file(path)
    assert result["status"] == "invalid"


def test_validate_dd_meta_brief_marker_is_whitelisted():
    # 2026-09-07：v17 正式形態標記不應讓每份 brief 永久多一個 warning。
    assert "brief" in validate_dd_meta.WHITELIST_KEYS
    _, warnings = validate_dd_meta.validate_meta({"brief": True})
    assert not any("unknown dd-meta key: 'brief'" in item for item in warnings)


@pytest.mark.parametrize(
    ("filename", "html"),
    [
        ("BRIEF_NOMETA.html", "<!doctype html><title>無 meta</title>"),
        ("BRIEF_BADJSON.html", '<script id="dd-meta">{"schema":"v17.0",}</script>'),
    ],
)
def test_verify_dd_math_explicit_bad_brief_fails(tmp_path, capsys, filename, html):
    # 2026-09-07：明示 BRIEF 缺 meta／壞 JSON 都不能落成 checked=0 綠燈。
    path = tmp_path / filename
    path.write_text(html, encoding="utf-8")

    assert verify_dd_math.main([str(path)]) != 0
    output = capsys.readouterr().out
    assert "[FAIL]" in output
    assert "驗算 1 檔（v15+），有 FAIL" in output


def test_verify_dd_math_zero_checked_is_not_all_pass(tmp_path, capsys):
    # 2026-09-07：明示 legacy 非目標仍可略過，但摘要不得宣稱全數通過。
    path = tmp_path / "DD_LEGACY.html"
    path.write_text("<!doctype html><title>legacy</title>", encoding="utf-8")

    assert verify_dd_math.main([str(path)]) == 0
    output = capsys.readouterr().out
    assert "驗算 0 檔（v15+），沒有可驗算目標" in output
    assert "全數通過" not in output


def test_qc_recognizes_only_canonical_brief_path():
    # 2026-09-07：QC 只把 dd/brief/BRIEF_*.html 納入 DD 結構閘。
    assert qc.is_dd_html(REPO_ROOT / "docs/dd/DD_TEST_20260101.html")
    assert qc.is_dd_html(REPO_ROOT / "docs/dd/brief/BRIEF_TEST_20260101.html")
    assert not qc.is_dd_html(REPO_ROOT / "docs/other/BRIEF_TEST_20260101.html")


def test_hook_and_ci_route_brief_to_validator():
    # 2026-09-07：靜態契約鎖住 pre-commit TARGETS_DD 與 CI 的 brief 路徑。
    hook = (SCRIPTS_DIR / "hooks" / "pre-commit").read_text(encoding="utf-8")
    workflow = (REPO_ROOT / ".github/workflows/validate_dd_meta.yml").read_text(encoding="utf-8")

    assert 'TARGETS_DD="$STAGED_DD $STAGED_BRIEF"' in hook
    assert "docs/dd/brief/**" in workflow
    assert "run: python scripts/validate_dd_meta.py" in workflow
    assert "docs/dd/brief/BRIEF_*.html" not in workflow
