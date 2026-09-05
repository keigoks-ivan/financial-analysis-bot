#!/usr/bin/env python3
"""測試 `scripts/ddreport.py`（v17 WP6a：`finish`／`index-row` 子命令）。

只測本輪新增的東西：
- `index-row`：從一份含 dd-meta＋`<p class="sub…">` 的 HTML 生出 INDEX.md 八欄一列。
- append 冪等：同一份檔名（file_cell）重複 append 不重複。
- `finish` 的 commit 檔案集白名單：只 stage 六類白名單檔（`_git` 全程 monkeypatch，
  不碰真實 git）。
- 遠端領先時 `finish` 回傳 exit code 2、且不呼叫 push。

全程用 `monkeypatch` 把 `ddreport.REPO_ROOT`／`DD_DIR`／`INDEX_MD_PATH` 等模組層路徑常數
與 `RUNS_DIR` 換成 tmp_path 下的假 repo 骨架，`subprocess.run` 整支換假（不論 git 或
`update_dd_index.py` 呼叫都攔下，回傳成功），比照 `test_ddreport_run.py` 既有作法
（`monkeypatch.setattr(ddreport.subprocess, "run", ...)`）。

Python 3.9 相容。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import ddreport  # noqa: E402


class _FakeCompleted:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _sample_meta(brief=True):
    return {
        "ticker": "ZTEST",
        "schema": "v15.0",
        "date": "2026-09-05",
        "dca_verdict": "觀望",
        "dca_role": "追蹤",
        "rearm_trigger": "股價 ≤$100 且 Q4 財報確認 backlog",
        "trap_label": "🟡 觀察期",
        "moat": "B",
        "moat_trend": "↑",
        "val": "🟢",
        "trap": "🟡",
        "ev5y_pct": 18.9,
        "irr_base_pct": 3.4,
        "max_dd_pct": -65,
        "oneliner": "fallback oneliner，不應被用到。",
        "brief": brief,
    }


def _write_brief_html(path, meta, sub_text="測試句子一。"):
    path.parent.mkdir(parents=True, exist_ok=True)
    html = (
        "<!doctype html><html><body>\n"
        '<p class="sub fallback">{sub}</p>\n'
        '<script id="dd-meta" type="application/json">\n{meta}\n</script>\n'
        "</body></html>\n"
    ).format(sub=sub_text, meta=json.dumps(meta, ensure_ascii=False, indent=2))
    path.write_text(html, encoding="utf-8")
    return path


def _setup_fake_repo(tmp_path, monkeypatch):
    """建一個最小假 repo 骨架，monkeypatch ddreport 的模組層路徑常數指過去。"""
    repo = tmp_path / "repo"
    dd_dir = repo / "docs" / "dd"
    brief_dir = dd_dir / "brief"
    brief_dir.mkdir(parents=True)

    index_md = dd_dir / "INDEX.md"
    index_md.write_text("# DD 報告索引\n\n既有內容一行\n", encoding="utf-8")

    research_body = repo / "docs" / "research" / "_body.html"
    research_body.parent.mkdir(parents=True)
    research_body.write_text("<div>body</div>", encoding="utf-8")

    screener = repo / "docs" / "dd-screener" / "latest.json"
    screener.parent.mkdir(parents=True)
    screener.write_text("{}", encoding="utf-8")

    picks = repo / "docs" / "picks" / "candidates.json"
    picks.parent.mkdir(parents=True)
    picks.write_text("{}", encoding="utf-8")

    src_archive = repo / "notes" / "site-internal" / "dd" / "_src"
    src_archive.mkdir(parents=True)

    runs_dir = repo / ".dd_build" / "runs"
    runs_dir.mkdir(parents=True)

    monkeypatch.setattr(ddreport, "REPO_ROOT", repo)
    monkeypatch.setattr(ddreport, "DD_DIR", dd_dir)
    monkeypatch.setattr(ddreport, "INDEX_MD_PATH", index_md)
    monkeypatch.setattr(ddreport, "RESEARCH_BODY_PATH", research_body)
    monkeypatch.setattr(ddreport, "DD_SCREENER_LATEST_PATH", screener)
    monkeypatch.setattr(ddreport, "PICKS_CANDIDATES_PATH", picks)
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", src_archive)
    monkeypatch.setattr(ddreport, "RUNS_DIR", runs_dir)

    return {
        "repo": repo, "dd_dir": dd_dir, "brief_dir": brief_dir,
        "index_md": index_md, "research_body": research_body,
        "screener": screener, "picks": picks, "src_archive": src_archive,
        "runs_dir": runs_dir,
    }


def _make_run_dir(paths, ticker, date, html_path, extra_stages=None):
    run_dir = paths["runs_dir"] / "{0}_{1}".format(ticker, date)
    run_dir.mkdir(parents=True)
    for name in ("evidence.json", "digest.json", "judgment.json", "scenario.json", "scenario_meta.json"):
        (run_dir / name).write_text("{}", encoding="utf-8")
    (run_dir / "gate_audit.md").write_text("# audit\n", encoding="utf-8")
    for sub in ("parts", "prompts", "agents"):
        d = run_dir / sub
        d.mkdir()
        (d / "x.json").write_text("{}", encoding="utf-8")

    stages = {
        "stage0": {
            "state": "PASS",
            "agent_usage": [
                {"num_turns": 2, "by_model": {"claude-sonnet-5": {
                    "cacheReadInputTokens": 1_000_000, "cacheCreationInputTokens": 10, "outputTokens": 5}}},
            ],
        },
        "judged": {
            "state": "PASS",
            "agent_usage": [
                {"num_turns": 1, "by_model": {"claude-fable-5": {
                    "cacheReadInputTokens": 500_000, "cacheCreationInputTokens": 1, "outputTokens": 1}}},
            ],
        },
        "gated": {
            "state": "PASS",
            "agent_usage": [
                {"num_turns": 1, "by_model": {"claude-opus-5": {
                    "cacheReadInputTokens": 250_000, "cacheCreationInputTokens": 1, "outputTokens": 1}}},
            ],
        },
        "brief": {
            "state": "PASS",
            "out_path": str(html_path),
        },
    }
    if extra_stages:
        stages.update(extra_stages)

    manifest = {
        "ticker": ticker, "date": date, "state": "brief_pass",
        "stages": stages,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return run_dir, manifest


# ---------------------------------------------------------------------------
# index-row：八欄
# ---------------------------------------------------------------------------

def test_index_row_eight_columns(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    html_path = paths["brief_dir"] / "BRIEF_ZTEST_20260905.html"
    _write_brief_html(html_path, _sample_meta())

    fields = ddreport._index_row_fields(html_path)
    row = fields["row"]

    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    assert len(cells) == 8, "INDEX.md 一列必須恰八欄：{0}".format(cells)

    date_c, ticker_c, schema_c, verdict_c, trap_c, col6_c, file_c, note_c = cells
    assert date_c == "2026-09-05"
    assert ticker_c == "ZTEST"
    assert schema_c == "v15.0"
    assert verdict_c == "觀望｜追蹤·rearm＝股價 ≤$100 且 Q4 財報確認 backlog"
    assert trap_c == "🟡 觀察期"
    assert col6_c == "B↑/🟢/🟡"
    assert file_c == "brief/BRIEF_ZTEST_20260905.html"
    # 備註：sub 文字優先於 oneliner；含三個決策數字；帶 v17 快速版尾註
    assert note_c.startswith("測試句子一。")
    assert "EV5y +18.9%" in note_c
    assert "IRR +3.4%/yr" in note_c
    assert "Max DD −65%" in note_c
    assert "**v17 快速版" in note_c
    assert fields["file_cell"] == "brief/BRIEF_ZTEST_20260905.html"


def test_index_row_full_version_suffix(tmp_path, monkeypatch):
    """`brief` 不為真時（完整版）尾註要換成「**v17 完整版**」。"""
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    html_path = paths["dd_dir"] / "DD_ZTEST_20260905.html"
    _write_brief_html(html_path, _sample_meta(brief=False))
    fields = ddreport._index_row_fields(html_path)
    assert "**v17 完整版**" in fields["row"]
    assert fields["file_cell"] == "DD_ZTEST_20260905.html"


# ---------------------------------------------------------------------------
# append 冪等
# ---------------------------------------------------------------------------

def test_index_row_append_idempotent(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    html_path = paths["brief_dir"] / "BRIEF_ZTEST_20260905.html"
    _write_brief_html(html_path, _sample_meta())
    fields = ddreport._index_row_fields(html_path)

    ok1 = ddreport._append_index_row(fields["row"], fields["file_cell"])
    assert ok1 is True
    text_after_first = paths["index_md"].read_text(encoding="utf-8")
    assert text_after_first.count(fields["file_cell"]) == 1

    ok2 = ddreport._append_index_row(fields["row"], fields["file_cell"])
    assert ok2 is False
    text_after_second = paths["index_md"].read_text(encoding="utf-8")
    assert text_after_second.count(fields["file_cell"]) == 1
    assert text_after_second == text_after_first


def test_index_row_cli_append(tmp_path, monkeypatch, capsys):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    html_path = paths["brief_dir"] / "BRIEF_ZTEST_20260905.html"
    _write_brief_html(html_path, _sample_meta())
    ns = ddreport.build_parser().parse_args(
        ["index-row", "--html", str(html_path), "--append"]
    )
    rc = ns.func(ns)
    assert rc == 0
    assert "BRIEF_ZTEST_20260905.html" in paths["index_md"].read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# finish：commit 檔案集白名單
# ---------------------------------------------------------------------------

def test_finish_commit_file_whitelist_and_push(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    ticker, date = "ZTEST", "20260905"
    html_path = paths["brief_dir"] / "BRIEF_{0}_{1}.html".format(ticker, date)
    _write_brief_html(html_path, _sample_meta())
    run_dir, manifest = _make_run_dir(paths, ticker, date, html_path)

    git_calls = []

    def _fake_git(args, cwd=None):
        git_calls.append(list(args))
        return _FakeCompleted(0, "", "")

    sub_calls = []

    def _fake_subprocess_run(cmd, *a, **k):
        sub_calls.append(list(cmd))
        return _FakeCompleted(0, "", "")

    monkeypatch.setattr(ddreport, "_git", _fake_git)
    monkeypatch.setattr(ddreport, "_git_ahead_behind", lambda: (0, 0))
    monkeypatch.setattr(ddreport.subprocess, "run", _fake_subprocess_run)

    rc = ddreport._do_finish(ticker, date)
    assert rc == 0

    add_calls = [c for c in git_calls if c[0] == "add"]
    assert len(add_calls) == 1
    staged = set(add_calls[0][1:])

    expected = {
        str(html_path),
        str(paths["index_md"]),
        str(paths["research_body"]),
        str(paths["screener"]),
        str(paths["picks"]),
        str(paths["src_archive"] / "{0}_{1}".format(ticker, date)),
    }
    assert staged == expected, "commit 檔案集白名單不符：{0} vs {1}".format(staged, expected)

    commit_calls = [c for c in git_calls if c[0] == "commit"]
    assert len(commit_calls) == 1
    assert "-m" in commit_calls[0]
    msg = commit_calls[0][commit_calls[0].index("-m") + 1]
    assert ticker in msg
    assert "v17 全帳" in msg
    assert "resync research+screener" in msg

    push_calls = [c for c in git_calls if c[0] == "push"]
    assert len(push_calls) == 1

    # 存查：archive 目錄與 token.json 都寫出來了
    archive_dir = paths["src_archive"] / "{0}_{1}".format(ticker, date)
    assert (archive_dir / "{0}_{1}.evidence.json".format(ticker, date)).exists()
    assert (archive_dir / "{0}_{1}.transcript_digest.json".format(ticker, date)).exists()
    assert (archive_dir / "parts").is_dir()
    token_path = archive_dir / "token.json"
    assert token_path.exists()
    ledger = json.loads(token_path.read_text(encoding="utf-8"))
    assert ledger["totals"]["sonnet"]["cache_read"] == 1_000_000
    assert ledger["totals"]["fable"]["cache_read"] == 500_000
    assert ledger["totals"]["opus"]["cache_read"] == 250_000

    # INDEX.md 已寫入這列
    assert "BRIEF_{0}_{1}.html".format(ticker, date) in paths["index_md"].read_text(encoding="utf-8")

    # update_dd_index.py 有被呼叫（透過假 subprocess.run）
    assert any("update_dd_index.py" in " ".join(c) for c in sub_calls)


def test_finish_dry_run_touches_nothing(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    ticker, date = "ZTEST", "20260905"
    html_path = paths["brief_dir"] / "BRIEF_{0}_{1}.html".format(ticker, date)
    _write_brief_html(html_path, _sample_meta())
    _make_run_dir(paths, ticker, date, html_path)

    git_calls = []
    monkeypatch.setattr(ddreport, "_git", lambda args, cwd=None: git_calls.append(list(args)))
    monkeypatch.setattr(ddreport, "_git_ahead_behind", lambda: (0, 0))

    index_before = paths["index_md"].read_text(encoding="utf-8")
    rc = ddreport._do_finish(ticker, date, dry_run=True)
    assert rc == 0
    assert git_calls == []
    assert paths["index_md"].read_text(encoding="utf-8") == index_before
    assert not (paths["src_archive"] / "{0}_{1}".format(ticker, date)).exists()


def test_finish_missing_brief_stage_errors(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    ticker, date = "ZTEST", "20260905"
    run_dir = paths["runs_dir"] / "{0}_{1}".format(ticker, date)
    run_dir.mkdir(parents=True)
    manifest = {"ticker": ticker, "date": date, "stages": {"brief": {"state": "FAIL"}}}
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    rc = ddreport._do_finish(ticker, date)
    assert rc == 1


# ---------------------------------------------------------------------------
# finish：遠端領先 → exit 2，且不 push
# ---------------------------------------------------------------------------

def test_finish_remote_ahead_exits_2_without_push(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    ticker, date = "ZTEST", "20260906"
    html_path = paths["brief_dir"] / "BRIEF_{0}_{1}.html".format(ticker, date)
    _write_brief_html(html_path, _sample_meta())
    _make_run_dir(paths, ticker, date, html_path)

    git_calls = []

    def _fake_git(args, cwd=None):
        git_calls.append(list(args))
        return _FakeCompleted(0, "", "")

    monkeypatch.setattr(ddreport, "_git", _fake_git)
    monkeypatch.setattr(ddreport, "_git_ahead_behind", lambda: (0, 3))
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: _FakeCompleted(0, "", ""))

    rc = ddreport._do_finish(ticker, date)
    assert rc == 2

    # commit 仍應完成（HOLD 只擋 push），但 push 絕不能被呼叫
    assert any(c[0] == "commit" for c in git_calls)
    assert not any(c[0] == "push" for c in git_calls)


def test_finish_no_push_flag_skips_push(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    ticker, date = "ZTEST", "20260907"
    html_path = paths["brief_dir"] / "BRIEF_{0}_{1}.html".format(ticker, date)
    _write_brief_html(html_path, _sample_meta())
    _make_run_dir(paths, ticker, date, html_path)

    git_calls = []
    ahead_behind_calls = []

    def _fake_git(args, cwd=None):
        git_calls.append(list(args))
        return _FakeCompleted(0, "", "")

    def _fake_ahead_behind():
        ahead_behind_calls.append(1)
        return (0, 0)

    monkeypatch.setattr(ddreport, "_git", _fake_git)
    monkeypatch.setattr(ddreport, "_git_ahead_behind", _fake_ahead_behind)
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: _FakeCompleted(0, "", ""))

    rc = ddreport._do_finish(ticker, date, no_push=True)
    assert rc == 0
    assert not any(c[0] == "push" for c in git_calls)
    # --no-push 應該連遠端領先檢查都省了（不必要的 fetch）
    assert ahead_behind_calls == []


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
