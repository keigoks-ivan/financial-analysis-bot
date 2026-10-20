#!/usr/bin/env python3
"""DD 發布推送修正（WP1，2026-10-20）：彙總檔衝突自救、存檔標點正規化、
update_dd_index 重建篩選器帶 `--include-non-dd`。

純函式（選自己的檔／合併 INDEX 列／衝突判斷／標點正規化）直接單測；自救流程用
tmp 目錄的真 git（bare origin＋work clone＋另一個 clone 模擬遠端領先）整段跑一遍，
`update_dd_index.py`／`build_dd_screener.py` 換成假腳本，不碰網路、不真的 push 任何
真實 remote。

Python 3.9 相容。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import ddreport  # noqa: E402
import qc  # noqa: E402
import update_dd_index  # noqa: E402
from test_ddreport_finish import (  # noqa: E402
    _FakeCompleted, _make_run_dir, _sample_meta, _setup_fake_repo, _write_brief_html,
)


# ---------------------------------------------------------------------------
# 純函式：INDEX 列
# ---------------------------------------------------------------------------

_HEADER = (
    "# DD 報告索引\n\n說明一行\n\n---\n\n"
    "| 日期 | Ticker | Schema | 裁決 | 陷阱定性 | R:R | 檔案 | 備註 |\n"
    "|:---|:---|:---|:---|:---|:---|:---|:---|\n"
)


def _row(date, ticker, file_cell, note="備註"):
    return "| {0} | {1} | v15.2 | 觀望 | 🟡 | B→/🟡/🟡 | {2} | {3} |".format(
        date, ticker, file_cell, note)


def test_merge_index_rows_inserts_after_last_table_row():
    a = _row("2026-10-19", "AAA", "DD_AAA_20261019.html")
    b = _row("2026-10-20", "BBB", "DD_BBB_20261020.html")
    c = _row("2026-10-20", "CCC", "brief/BRIEF_CCC_20261020.html")
    text = _HEADER + a + "\n" + b + "\n"
    new_text, added = ddreport._merge_index_rows(text, [c])
    assert added == [c]
    assert new_text == _HEADER + a + "\n" + b + "\n" + c + "\n"


def test_merge_index_rows_skips_same_row_and_same_file_key():
    a = _row("2026-10-19", "AAA", "DD_AAA_20261019.html")
    a_other_note = _row("2026-10-19", "AAA", "DD_AAA_20261019.html", note="另一版備註")
    b = _row("2026-10-20", "BBB", "DD_BBB_20261020.html")
    text = _HEADER + a + "\n"
    # 整列相同、同檔名但備註不同，都算已存在
    new_text, added = ddreport._merge_index_rows(text, [a, a_other_note, b])
    assert added == [b]
    assert new_text.count("DD_AAA_20261019.html") == 1
    # 冪等：再合併一次不動
    again, added2 = ddreport._merge_index_rows(new_text, [a, b])
    assert added2 == [] and again == new_text


def test_merge_index_rows_multiple_rows_keep_order_and_trailing_text():
    a = _row("2026-10-19", "AAA", "DD_AAA_20261019.html")
    b = _row("2026-10-20", "BBB", "DD_BBB_20261020.html")
    c = _row("2026-10-20", "CCC", "DD_CCC_20261020.html")
    text = _HEADER + a + "\n\n表格後的附註\n"
    new_text, added = ddreport._merge_index_rows(text, [b, c])
    assert added == [b, c]
    # 插在表格最後一列之後、附註之前，順序照傳入
    assert new_text == _HEADER + a + "\n" + b + "\n" + c + "\n\n表格後的附註\n"


def test_merge_index_rows_without_table_appends_at_end():
    b = _row("2026-10-20", "BBB", "DD_BBB_20261020.html")
    new_text, added = ddreport._merge_index_rows("", [b])
    assert added == [b] and new_text == b + "\n"


def test_added_index_rows_takes_only_new_table_rows_from_diff():
    new_row = _row("2026-10-20", "BBB", "DD_BBB_20261020.html")
    old_row = _row("2026-10-19", "AAA", "DD_AAA_20261019.html")
    diff = "\n".join([
        "diff --git a/docs/dd/INDEX.md b/docs/dd/INDEX.md",
        "--- a/docs/dd/INDEX.md",
        "+++ b/docs/dd/INDEX.md",
        "@@ -70,0 +71 @@",
        "+" + new_row,
        "-" + old_row,
        "+一般新增文字",
        "+| 日期 | Ticker |",
    ])
    assert ddreport._added_index_rows(diff) == [new_row]
    assert ddreport._added_index_rows("") == []


# ---------------------------------------------------------------------------
# 純函式：自己的檔、衝突判斷、push 輸出判斷
# ---------------------------------------------------------------------------

def test_select_own_paths_picks_report_archive_and_hub_data_only():
    changed = [
        "docs/dd/DD_ZZZ_20261020.html",
        "docs/dd/brief/BRIEF_ZZZ_20261020.html",
        "notes/site-internal/dd/_src/ZZZ_20261020/manifest.json",
        "notes/site-internal/dd/_src/ZZZ_20261020/prompts/gate.md",
        "docs/t/data/ZZZ.json",
        # 不收：轉址樁、彙總檔、別檔、別天、別人被掃進來的檔
        "docs/t/ZZZ.html",
        "docs/t/index.html",
        "docs/dd/INDEX.md",
        "docs/dd-screener/latest.json",
        "docs/dd/DD_OTHER_20261020.html",
        "docs/dd/DD_ZZZ_20261019.html",
        "notes/site-internal/dd/_src/ZZZ_20261019/manifest.json",
        "notes/site-internal/dd/_src/ZZZ_20261020X/manifest.json",
        "docs/t/data/OTHER.json",
        "docs/other_session.html",
    ]
    own = ddreport._select_own_paths(changed, ["ZZZ"], "20261020")
    assert own == [
        "docs/dd/DD_ZZZ_20261020.html",
        "docs/dd/brief/BRIEF_ZZZ_20261020.html",
        "notes/site-internal/dd/_src/ZZZ_20261020/manifest.json",
        "notes/site-internal/dd/_src/ZZZ_20261020/prompts/gate.md",
        "docs/t/data/ZZZ.json",
    ]


def test_select_own_paths_batch_sync_only_hub_data():
    changed = ["docs/dd/INDEX.md", "docs/t/data/AAA.json", "docs/t/AAA.html",
               "docs/t/data/BBB.json", "docs/t/data/CCC.json", "docs/dd/DD_AAA_20261020.html"]
    assert ddreport._select_own_paths(changed, ["AAA", "BBB"]) == [
        "docs/t/data/AAA.json", "docs/t/data/BBB.json"]


def test_conflicts_only_aggregates():
    agg = ddreport._aggregate_rel_paths()
    assert agg == [
        "docs/dd/INDEX.md", "docs/research/_body.html", "docs/dd-screener/latest.json",
        "docs/picks/candidates.json", "docs/t/index.html"]
    assert ddreport._conflicts_only_aggregates(["docs/dd/INDEX.md", "docs/t/index.html"], agg)
    assert not ddreport._conflicts_only_aggregates([], agg)
    assert not ddreport._conflicts_only_aggregates(["docs/dd/INDEX.md", "docs/dd/DD_ZZZ_20261020.html"], agg)
    assert not ddreport._conflicts_only_aggregates(["docs/other.html"], agg)


def test_is_non_fast_forward():
    assert ddreport._is_non_fast_forward(" ! [rejected] HEAD -> main (non-fast-forward)")
    assert ddreport._is_non_fast_forward(" ! [rejected] HEAD -> main (fetch first)")
    assert not ddreport._is_non_fast_forward("QC FAIL: CJK followed by half-width punctuation")
    assert not ddreport._is_non_fast_forward("")


# ---------------------------------------------------------------------------
# 標點正規化：對齊 qc.py
# ---------------------------------------------------------------------------

def test_normalize_cjk_punct_converts_only_what_qc_flags():
    text = "來源提示:請查證。價格是3.5,不變.\n中文,接逗號.接句點:接冒號;分號？問號! ok.\nA,B.C:D 英文不動\n"
    new_text, hits = ddreport._normalize_cjk_punct(text)
    assert new_text == "來源提示：請查證。價格是3.5,不變。\n中文，接逗號。接句點：接冒號;分號？問號! ok.\nA,B.C:D 英文不動\n"
    assert hits == 5  # 提示: ／不變. ／文, ／號. ／點:；3.5, 與 `;` `?` `!` 不算
    # 冪等
    assert ddreport._normalize_cjk_punct(new_text) == (new_text, 0)


def test_normalize_cjk_punct_keeps_code_spans_like_qc():
    text = "正文:一\n```\n程式碼中文,這裡不轉.\n```\n行內 `中文,不轉` 之後中文,轉\n"
    new_text, hits = ddreport._normalize_cjk_punct(text)
    assert "程式碼中文,這裡不轉." in new_text
    assert "`中文,不轉`" in new_text
    assert "正文：一" in new_text and "中文，轉" in new_text
    assert hits == 2


def test_normalize_output_passes_qc_cjk_check():
    text = "# 提示\n\n來源提示: 請看。\n結論,偏多.\n- 項目:甲\n```\n中文,code\n```\n"
    assert qc.check_cjk_punct(Path("x.md"), text)  # 轉換前 qc 會擋
    new_text, _ = ddreport._normalize_cjk_punct(text)
    assert qc.check_cjk_punct(Path("x.md"), new_text) == []


def test_normalize_archive_punct_only_md_and_preserves_bytes(tmp_path):
    d = tmp_path / "ZZZ_20261020"
    (d / "prompts").mkdir(parents=True)
    md = d / "prompts" / "gate.md"
    md.write_bytes("第一行來源:甲\r\n第二行\r\n".encode("utf-8"))
    clean_md = d / "clean.md"
    clean_md.write_text("乾淨。\n", encoding="utf-8")
    js = d / "x.json"
    js.write_text(json.dumps({"k": "中文,逗號:冒號"}, ensure_ascii=False), encoding="utf-8")
    txt = d / "n.txt"
    txt.write_text("中文,逗號\n", encoding="utf-8")
    bad = d / "latin.md"
    bad.write_bytes("中文,".encode("big5"))  # 非 UTF-8：略過不炸

    files, hits = ddreport._normalize_archive_punct(d)
    assert (files, hits) == (1, 1)
    assert md.read_bytes() == "第一行來源：甲\r\n第二行\r\n".encode("utf-8")  # CRLF 保留
    assert json.loads(js.read_text(encoding="utf-8")) == {"k": "中文,逗號:冒號"}
    assert txt.read_text(encoding="utf-8") == "中文,逗號\n"
    assert clean_md.read_text(encoding="utf-8") == "乾淨。\n"


def test_archive_run_dir_normalizes_archive_copy_not_run_dir(tmp_path):
    run_dir = tmp_path / "run" / "ZZZ_20261020"
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "prompts" / "gate.md").write_text("來源提示:請查證\n", encoding="utf-8")
    (run_dir / "prompts" / "gate_inline.md").write_text("來源提示:內嵌版\n", encoding="utf-8")
    (run_dir / "gate_audit.md").write_text("審查結論,通過.\n", encoding="utf-8")
    (run_dir / "manifest.json").write_text("{}", encoding="utf-8")
    archive_dir = tmp_path / "_src" / "ZZZ_20261020"

    ddreport._archive_run_dir(run_dir, archive_dir)

    assert (archive_dir / "prompts" / "gate.md").read_text(encoding="utf-8") == "來源提示：請查證\n"
    assert (archive_dir / "ZZZ_20261020.gate_audit.md").read_text(encoding="utf-8") == "審查結論，通過。\n"
    assert not (archive_dir / "prompts" / "gate_inline.md").exists()
    # 原 run 目錄不動
    assert (run_dir / "prompts" / "gate.md").read_text(encoding="utf-8") == "來源提示:請查證\n"
    for p in archive_dir.rglob("*.md"):
        assert qc.check_cjk_punct(p, p.read_text(encoding="utf-8")) == []


# ---------------------------------------------------------------------------
# update_dd_index.py：重建篩選器帶 --include-non-dd
# ---------------------------------------------------------------------------

def test_update_dd_index_runs_screener_with_include_non_dd(monkeypatch):
    calls = []

    def fake_run(cmd, *args, **kwargs):
        calls.append(list(cmd))
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(update_dd_index, "parse_index_md", lambda: {})
    monkeypatch.setattr(update_dd_index, "scan_files", lambda index_data: [])
    monkeypatch.setattr(update_dd_index, "update_index", lambda *a, **k: True)
    monkeypatch.setattr(update_dd_index, "inject_asym_flags", lambda *a, **k: 0)
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["update_dd_index.py"])

    update_dd_index.main()
    screener_calls = [c for c in calls if str(c[1]).endswith("build_dd_screener.py")]
    assert len(screener_calls) == 1
    assert screener_calls[0][2:] == ["--include-non-dd"]


def test_update_dd_index_skip_dd_screener_still_skips_screener(monkeypatch):
    calls = []
    monkeypatch.setattr(update_dd_index, "parse_index_md", lambda: {})
    monkeypatch.setattr(update_dd_index, "scan_files", lambda index_data: [])
    monkeypatch.setattr(update_dd_index, "update_index", lambda *a, **k: True)
    monkeypatch.setattr(
        subprocess, "run", lambda cmd, *a, **k: calls.append(list(cmd)) or subprocess.CompletedProcess(cmd, 0))
    monkeypatch.setattr(sys, "argv", ["update_dd_index.py", "--skip-dd-screener"])

    assert update_dd_index.main() == 0
    assert not any(str(c[1]).endswith("build_dd_screener.py") for c in calls)


# ---------------------------------------------------------------------------
# 自救流程：真 git（bare origin＋work＋other）模擬一次彙總檔衝突
# ---------------------------------------------------------------------------

_FAKE_UPDATE_DD_INDEX = '''\
import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
(root / "ran_update_dd_index").write_text("1")
idx = (root / "docs/dd/INDEX.md").read_text(encoding="utf-8")
rows = [ln for ln in idx.splitlines() if ln.startswith("| 20")]
(root / "docs/dd-screener/latest.json").write_text(json.dumps({"rows": len(rows)}))
(root / "docs/research/_body.html").write_text("<p>%d</p>" % len(rows))
(root / "docs/picks/candidates.json").write_text(json.dumps({"n": len(rows)}))
(root / "docs/t/index.html").write_text("<p>hubs %d</p>" % len(rows))
(root / "docs/t/data/ZZZ.json").write_text(json.dumps({"regen": True}))
(root / "data/cache.txt").write_text("dirty cache")
'''
# origin 版 update_dd_index.py 已帶旗標（修正上線後的常態）：以字樣出現在腳本內容為準
_FAKE_UPDATE_DD_INDEX_WITH_FLAG = _FAKE_UPDATE_DD_INDEX + "# --include-non-dd\n"

_FAKE_BUILD_DD_SCREENER = '''\
import json, pathlib, sys
assert "--include-non-dd" in sys.argv, sys.argv
root = pathlib.Path(__file__).resolve().parent.parent
p = root / "docs/dd-screener/latest.json"
d = json.loads(p.read_text())
d["include_non_dd"] = True
p.write_text(json.dumps(d))
(root / "ran_build_dd_screener").write_text("1")
'''


def _run_git(cwd, *args):
    r = subprocess.run(["git"] + list(args), cwd=str(cwd), capture_output=True, text=True)
    assert r.returncode == 0, "git {0} 失敗：{1}{2}".format(" ".join(args), r.stdout, r.stderr)
    return r.stdout


def _commit_all(cwd, msg):
    _run_git(cwd, "add", "-A")
    _run_git(cwd, "commit", "-q", "-m", msg)
    return _run_git(cwd, "rev-parse", "HEAD").strip()


def _write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _clone(origin, dest):
    _run_git(dest.parent, "clone", "-q", str(origin), str(dest))
    _run_git(dest, "config", "user.email", "t@example.com")
    _run_git(dest, "config", "user.name", "t")
    _run_git(dest, "config", "commit.gpgsign", "false")


ROW_A = _row("2026-10-19", "AAA", "DD_AAA_20261019.html")
ROW_B = _row("2026-10-20", "BBB", "DD_BBB_20261020.html")
ROW_C = _row("2026-10-20", "ZZZ", "DD_ZZZ_20261020.html", note="自己這檔")


@pytest.fixture
def rescue_env(tmp_path, monkeypatch):
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    work = tmp_path / "work"
    _clone(origin, work)
    _run_git(work, "checkout", "-q", "-b", "main")

    base_files = {
        "docs/dd/INDEX.md": _HEADER + ROW_A + "\n",
        "docs/dd-screener/latest.json": json.dumps({"rows": 1}),
        "docs/research/_body.html": "<p>1</p>",
        "docs/picks/candidates.json": json.dumps({"n": 1}),
        "docs/t/index.html": "<p>hubs 1</p>",
        "docs/t/data/AAA.json": "{}",
        "docs/misc.txt": "misc 0\n",
        "data/cache.txt": "clean cache",
        "scripts/update_dd_index.py": _FAKE_UPDATE_DD_INDEX,
        "scripts/build_dd_screener.py": _FAKE_BUILD_DD_SCREENER,
        ".gitignore": "ran_*\n",
    }
    for rel, text in base_files.items():
        _write(work, rel, text)
    _commit_all(work, "base")
    _run_git(work, "push", "-q", "origin", "main")

    other = tmp_path / "other"
    _clone(origin, other)

    # 遠端先前進：別的 DD（BBB）發布，動了 INDEX 與全部彙總檔
    _write(other, "docs/dd/INDEX.md", _HEADER + ROW_A + "\n" + ROW_B + "\n")
    _write(other, "docs/dd-screener/latest.json", json.dumps({"rows": 2, "by": "other"}))
    _write(other, "docs/research/_body.html", "<p>2 other</p>")
    _write(other, "docs/picks/candidates.json", json.dumps({"n": 2, "by": "other"}))
    _write(other, "docs/t/index.html", "<p>hubs 2 other</p>")
    _write(other, "docs/dd/DD_BBB_20261020.html", "<html>BBB</html>")
    _commit_all(other, "Add BBB DD")
    _run_git(other, "push", "-q", "origin", "main")

    # 本地 finish commit：自己的檔＋INDEX 列＋彙總檔改動＋舊式 /t/{T}.html 轉址樁
    _write(work, "docs/dd/DD_ZZZ_20261020.html", "<html>ZZZ</html>")
    _write(work, "notes/site-internal/dd/_src/ZZZ_20261020/manifest.json", "{}")
    _write(work, "notes/site-internal/dd/_src/ZZZ_20261020/prompts/gate.md", "來源提示：已正規化\n")
    _write(work, "docs/t/data/ZZZ.json", json.dumps({"local": True}))
    _write(work, "docs/t/ZZZ.html", "<meta http-equiv='refresh'>")
    _write(work, "docs/dd/INDEX.md", _HEADER + ROW_A + "\n" + ROW_C + "\n")
    _write(work, "docs/dd-screener/latest.json", json.dumps({"rows": 2, "by": "local"}))
    _write(work, "docs/research/_body.html", "<p>2 local</p>")
    _write(work, "docs/picks/candidates.json", json.dumps({"n": 2, "by": "local"}))
    _write(work, "docs/t/index.html", "<p>hubs 2 local</p>")
    message = "Add ZZZ DD 完整版 20261020（觀望；dd2-v20 $1.00／1.0M）; resync research+screener\n\nCo-Authored-By: T <t@example.com>"
    _run_git(work, "add", "-A")
    _run_git(work, "commit", "-q", "-m", message)
    sha = _run_git(work, "rev-parse", "HEAD").strip()
    _run_git(work, "fetch", "-q", "origin", "main")

    monkeypatch.setattr(ddreport, "REPO_ROOT", work)
    monkeypatch.setattr(ddreport, "DD_DIR", work / "docs" / "dd")
    monkeypatch.setattr(ddreport, "INDEX_MD_PATH", work / "docs" / "dd" / "INDEX.md")
    monkeypatch.setattr(ddreport, "RESEARCH_BODY_PATH", work / "docs" / "research" / "_body.html")
    monkeypatch.setattr(ddreport, "DD_SCREENER_LATEST_PATH", work / "docs" / "dd-screener" / "latest.json")
    monkeypatch.setattr(ddreport, "PICKS_CANDIDATES_PATH", work / "docs" / "picks" / "candidates.json")
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", work / "notes" / "site-internal" / "dd" / "_src")
    monkeypatch.setattr(ddreport, "TICKER_HUB_DIR", work / "docs" / "t")
    monkeypatch.setattr(ddreport, "DD_WORKTREE_DIR", tmp_path / "wt1")
    monkeypatch.setattr(ddreport, "DD_WORKTREE_PUSH_DIR", tmp_path / "wt2")
    monkeypatch.setattr(ddreport, "_pick_python", lambda: sys.executable)

    def origin_show(rel, ref="main"):
        r = subprocess.run(["git", "show", "{0}:{1}".format(ref, rel)], cwd=str(origin),
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    return {
        "tmp": tmp_path, "origin": origin, "work": work, "other": other, "sha": sha,
        "message": message, "show": origin_show,
        "origin_head": lambda: _run_git(origin, "rev-parse", "main").strip(),
    }


def _assert_worktrees_gone(env):
    listing = _run_git(env["work"], "worktree", "list")
    assert "wt1" not in listing and "wt2" not in listing
    assert not (env["tmp"] / "wt1").exists() and not (env["tmp"] / "wt2").exists()


def test_rescue_aggregate_conflict_end_to_end(rescue_env):
    env = rescue_env
    before = env["origin_head"]()

    ok, reason = ddreport._push_head_via_worktree(env["sha"], tickers=["ZZZ"], date="20261020")
    assert (ok, reason) == (True, "")

    # 自己的檔上 origin
    assert env["show"]("docs/dd/DD_ZZZ_20261020.html") == "<html>ZZZ</html>"
    assert env["show"]("notes/site-internal/dd/_src/ZZZ_20261020/manifest.json") == "{}"
    assert env["show"]("notes/site-internal/dd/_src/ZZZ_20261020/prompts/gate.md") == "來源提示：已正規化\n"
    # 遠端別人的檔還在
    assert env["show"]("docs/dd/DD_BBB_20261020.html") == "<html>BBB</html>"
    # INDEX：A、B、C 三列，C 在 B 之後，沒有衝突標記
    index = env["show"]("docs/dd/INDEX.md")
    assert "<<<<<<<" not in index and ">>>>>>>" not in index
    assert index == _HEADER + ROW_A + "\n" + ROW_B + "\n" + ROW_C + "\n"
    # 彙總檔是重建的產物（3 列），且沒有本地版／遠端舊版的殘留
    assert json.loads(env["show"]("docs/dd-screener/latest.json")) == {"rows": 3, "include_non_dd": True}
    assert env["show"]("docs/research/_body.html") == "<p>3</p>"
    assert json.loads(env["show"]("docs/picks/candidates.json")) == {"n": 3}
    assert env["show"]("docs/t/index.html") == "<p>hubs 3</p>"
    assert json.loads(env["show"]("docs/t/data/ZZZ.json")) == {"regen": True}
    # 轉址樁不帶上去、非白名單的重建髒檔不進 commit
    assert env["show"]("docs/t/ZZZ.html") is None
    assert env["show"]("data/cache.txt") == "clean cache"
    # 只前進一個 commit，訊息沿用原 commit
    assert _run_git(env["origin"], "rev-list", "--count", "{0}..main".format(before)).strip() == "1"
    assert _run_git(env["origin"], "log", "-1", "--format=%B", "main").strip() == env["message"].strip()
    _assert_worktrees_gone(env)


def test_rescue_skips_screener_rerun_when_update_script_already_has_flag(rescue_env, monkeypatch):
    env = rescue_env
    _write(env["other"], "scripts/update_dd_index.py", _FAKE_UPDATE_DD_INDEX_WITH_FLAG)
    _commit_all(env["other"], "update_dd_index 帶旗標")
    _run_git(env["other"], "push", "-q", "origin", "main")
    _run_git(env["work"], "fetch", "-q", "origin", "main")

    ran = []
    real_run = ddreport._rescue_run

    def spy(cmd, wt):
        ran.append(Path(cmd[1]).name)
        return real_run(cmd, wt)

    monkeypatch.setattr(ddreport, "_rescue_run", spy)
    ok, reason = ddreport._push_head_via_worktree(env["sha"], tickers=["ZZZ"], date="20261020")
    assert ok, reason
    assert ran == ["update_dd_index.py"]  # 沒有補跑 build_dd_screener
    assert json.loads(env["show"]("docs/dd-screener/latest.json")) == {"rows": 3}


def test_conflict_on_non_aggregate_file_still_holds(rescue_env):
    env = rescue_env
    # 本地 commit 與遠端都改 docs/misc.txt → 衝突涉及彙總檔以外的檔
    _write(env["other"], "docs/misc.txt", "misc remote\n")
    _commit_all(env["other"], "遠端改 misc")
    _run_git(env["other"], "pull", "-q", "--rebase", "origin", "main")
    _run_git(env["other"], "push", "-q", "origin", "main")
    _write(env["work"], "docs/misc.txt", "misc local\n")
    _run_git(env["work"], "add", "-A")
    _run_git(env["work"], "commit", "-q", "--amend", "--no-edit")
    sha = _run_git(env["work"], "rev-parse", "HEAD").strip()
    _run_git(env["work"], "fetch", "-q", "origin", "main")
    before = env["origin_head"]()

    ok, reason = ddreport._push_head_via_worktree(sha, tickers=["ZZZ"], date="20261020")
    assert not ok and reason.startswith("cherry-pick 衝突")
    assert env["origin_head"]() == before
    assert not (env["work"] / "ran_update_dd_index").exists()
    assert not (env["tmp"] / "wt1" / "ran_update_dd_index").exists()
    _assert_worktrees_gone(env)


def test_rescue_push_blocked_by_hook_holds_without_retry(rescue_env):
    env = rescue_env
    hooks = env["tmp"] / "hooks"
    hooks.mkdir()
    hook = hooks / "pre-push"
    hook.write_text("#!/bin/sh\necho 'QC FAIL: CJK followed by half-width punctuation' >&2\nexit 1\n")
    hook.chmod(0o755)
    _run_git(env["work"], "config", "core.hooksPath", str(hooks))
    before = env["origin_head"]()

    ok, reason = ddreport._push_head_via_worktree(env["sha"], tickers=["ZZZ"], date="20261020")
    assert not ok
    assert "push 被擋" in reason and "QC FAIL" in reason
    assert env["origin_head"]() == before
    _assert_worktrees_gone(env)


def test_rescue_push_retries_in_clean_worktree_after_non_fast_forward(rescue_env, monkeypatch):
    env = rescue_env
    real_run = ddreport._rescue_run

    def run_then_remote_moves(cmd, wt):
        out = real_run(cmd, wt)
        if Path(cmd[1]).name == "build_dd_screener.py":
            # 重建期間遠端又前進一次（不碰彙總檔）→ 原 worktree 的 push 會 non-fast-forward
            _write(env["other"], "docs/misc.txt", "misc remote moved\n")
            _commit_all(env["other"], "遠端在重建期間前進")
            _run_git(env["other"], "push", "-q", "origin", "main")
        return out

    monkeypatch.setattr(ddreport, "_rescue_run", run_then_remote_moves)
    ok, reason = ddreport._push_head_via_worktree(env["sha"], tickers=["ZZZ"], date="20261020")
    assert (ok, reason) == (True, "")
    assert env["show"]("docs/misc.txt") == "misc remote moved\n"  # 重推沒蓋掉遠端新 commit
    assert env["show"]("docs/dd/DD_ZZZ_20261020.html") == "<html>ZZZ</html>"
    assert env["show"]("docs/dd/INDEX.md") == _HEADER + ROW_A + "\n" + ROW_B + "\n" + ROW_C + "\n"
    _assert_worktrees_gone(env)


def test_rescue_retry_cherry_pick_conflict_holds(rescue_env, monkeypatch):
    env = rescue_env
    real_run = ddreport._rescue_run

    def run_then_remote_touches_aggregate(cmd, wt):
        out = real_run(cmd, wt)
        if Path(cmd[1]).name == "build_dd_screener.py":
            _write(env["other"], "docs/dd-screener/latest.json", json.dumps({"rows": 9, "by": "ci"}))
            _commit_all(env["other"], "CI 更新 latest.json")
            _run_git(env["other"], "push", "-q", "origin", "main")
        return out

    monkeypatch.setattr(ddreport, "_rescue_run", run_then_remote_touches_aggregate)
    ok, reason = ddreport._push_head_via_worktree(env["sha"], tickers=["ZZZ"], date="20261020")
    assert not ok and "cherry-pick 又衝突" in reason
    assert env["show"]("docs/dd/DD_ZZZ_20261020.html") is None  # 沒推任何東西
    _assert_worktrees_gone(env)


def test_rescue_aborts_when_commit_has_no_own_files(rescue_env):
    env = rescue_env
    # 以不含 ZZZ 自己檔的 ticker 呼叫：找不到自己的檔就中止，不重建、不推
    before = env["origin_head"]()
    ok, reason = ddreport._push_head_via_worktree(env["sha"], tickers=["NOPE"], date="20261020")
    assert not ok and "找不到" in reason
    assert env["origin_head"]() == before
    assert not (env["tmp"] / "wt1").exists()
    _assert_worktrees_gone(env)


def test_batch_sync_commit_rescue_uses_hub_data_as_own_files(rescue_env):
    env = rescue_env
    # 批尾同步 commit：INDEX 列＋彙總檔＋docs/t/data/{T}.json，不含報告檔、date=None；
    # 報告在 sync-later 時已各自先推上 origin
    _run_git(env["work"], "reset", "-q", "--hard", "HEAD~1")
    _write(env["other"], "docs/dd/DD_ZZZ_20261020.html", "<html>ZZZ</html>")
    _commit_all(env["other"], "報告先推")
    _run_git(env["other"], "push", "-q", "origin", "main")
    _write(env["work"], "docs/dd/INDEX.md", _HEADER + ROW_A + "\n" + ROW_C + "\n")
    _write(env["work"], "docs/dd-screener/latest.json", json.dumps({"rows": 2, "by": "local"}))
    _write(env["work"], "docs/research/_body.html", "<p>2 local</p>")
    _write(env["work"], "docs/t/data/ZZZ.json", json.dumps({"local": True}))
    _run_git(env["work"], "add", "-A")
    _run_git(env["work"], "commit", "-q", "-m", "Sync DD batch 20261020（1 檔；research+screener once）")
    sync_sha = _run_git(env["work"], "rev-parse", "HEAD").strip()
    _run_git(env["work"], "fetch", "-q", "origin", "main")

    ok, reason = ddreport._push_head_via_worktree(sync_sha, tickers=["ZZZ"])
    assert ok, reason
    index = env["show"]("docs/dd/INDEX.md")
    assert index == _HEADER + ROW_A + "\n" + ROW_B + "\n" + ROW_C + "\n"
    assert json.loads(env["show"]("docs/t/data/ZZZ.json")) == {"regen": True}
    assert json.loads(env["show"]("docs/dd-screener/latest.json")) == {"rows": 3, "include_non_dd": True}
    _assert_worktrees_gone(env)


# ---------------------------------------------------------------------------
# 呼叫端：finish／batch-sync 都把 tickers／date 帶給 _push_head_via_worktree
# ---------------------------------------------------------------------------

def test_finish_passes_ticker_and_date_to_push_helper(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    ticker, date = "ZTEST", "20261020"
    html_path = paths["brief_dir"] / "BRIEF_{0}_{1}.html".format(ticker, date)
    _write_brief_html(html_path, _sample_meta())
    _make_run_dir(paths, ticker, date, html_path)

    def _fake_git(args, cwd=None):
        if args and args[0] == "rev-parse":
            return _FakeCompleted(0, "deadbeef1234\n", "")
        return _FakeCompleted(0, "", "")

    seen = []
    monkeypatch.setattr(ddreport, "_git", _fake_git)
    monkeypatch.setattr(ddreport, "_git_ahead_behind", lambda: (0, 2))
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: _FakeCompleted(0, "", ""))
    monkeypatch.setattr(
        ddreport, "_push_head_via_worktree",
        lambda sha, tickers=None, date=None: seen.append((sha, tickers, date)) or (True, ""))

    assert ddreport._do_finish(ticker, date) == 0
    assert seen == [("deadbeef1234", [ticker], date)]


def test_batch_sync_passes_batch_tickers_to_push_helper(tmp_path, monkeypatch):
    paths = _setup_fake_repo(tmp_path, monkeypatch)
    rows = []
    for ticker in ("ZAAA", "ZBBB"):
        date = "20261020"
        html_path = paths["brief_dir"] / "BRIEF_{0}_{1}.html".format(ticker, date)
        _write_brief_html(html_path, _sample_meta())
        _make_run_dir(paths, ticker, date, html_path)
        rows.append({"ticker": ticker, "date": date, "rc": 0})

    def _fake_git(args, cwd=None):
        if args and args[0] == "rev-parse":
            return _FakeCompleted(0, "cafe5678\n", "")
        return _FakeCompleted(0, "", "")

    seen = []
    monkeypatch.setattr(ddreport, "_git", _fake_git)
    monkeypatch.setattr(ddreport, "_git_ahead_behind", lambda: (0, 1))
    monkeypatch.setattr(ddreport.subprocess, "run", lambda *a, **k: _FakeCompleted(0, "", ""))
    monkeypatch.setattr(ddreport, "_mark_sync_rows", lambda *a, **k: None)
    monkeypatch.setattr(
        ddreport, "_push_head_via_worktree",
        lambda sha, tickers=None, date=None: seen.append((sha, tickers, date)) or (True, ""))

    assert ddreport._sync_batch_site(rows, "20261020") == 0
    assert seen == [("cafe5678", ["ZAAA", "ZBBB"], None)]
