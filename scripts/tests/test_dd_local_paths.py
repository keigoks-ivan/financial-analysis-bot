#!/usr/bin/env python3
"""scripts/dd_local_paths.py：存檔副本的本機路徑去帳號（2026-11-25）。

repo 是公開的；存查檔不能帶 Google Drive 資料夾名裡的信箱與家目錄的使用者
名稱。這裡驗三件事：置換規則本身、`ddreport._archive_run_dir` 存檔時有套、
`FactsStore.put_transcripts` 寫檔時有套。
"""
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))
import dd_local_paths  # noqa: E402
import ddreport  # noqa: E402
from facts_store import FactsStore  # noqa: E402

USER = "someone"
MAIL = "some.one@example.com"
GDRIVE = "/Users/{0}/Library/CloudStorage/GoogleDrive-{1}/我的雲端硬碟/007美股".format(USER, MAIL)
CALL = GDRIVE + "/TSM/TSM_Q3_2025_Earnings_Call_20251016.md"
RUN = "/Users/{0}/financial-analysis-bot/.dd_build/runs/TSM_20261017/digest.json".format(USER)


def _clean(text):
    return MAIL not in text and "/Users/" not in text and "GoogleDrive-" not in text


def test_scrub_rules_and_idempotent():
    text = '{{"file": "{0}", "digest_path": "{1}"}} 另見 ~/Library/CloudStorage/GoogleDrive-{2}/x.md'.format(
        CALL, RUN, MAIL)
    out, hits = dd_local_paths.scrub(text)
    assert hits == 3
    assert _clean(out)
    assert "~/GoogleDrive/我的雲端硬碟/007美股/TSM/TSM_Q3_2025_Earnings_Call_20251016.md" in out
    assert "~/financial-analysis-bot/.dd_build/runs/TSM_20261017/digest.json" in out
    assert "~/GoogleDrive/x.md" in out
    assert dd_local_paths.scrub(out) == (out, 0)
    # 檔名不變——沿用舊存查靠 Path(file).name 比對
    assert Path(json.loads(out.split(" 另見")[0])["file"]).name == Path(CALL).name


def test_scrub_leaves_ordinary_text_alone():
    text = "營收 +12%，見 https://example.com/Users/guide 與 docs/dd/DD_TSM.html；聯絡 ir@example.com"
    assert dd_local_paths.scrub(text) == (text, 0)


def test_archive_run_dir_scrubs_copy_not_run_dir(tmp_path):
    run_dir = tmp_path / "run"
    (run_dir / "agents").mkdir(parents=True)
    digest = {"items": [{"file": CALL, "quote": "..."}]}
    (run_dir / "digest.json").write_text(json.dumps(digest, ensure_ascii=False), encoding="utf-8")
    (run_dir / "manifest.json").write_text(json.dumps({"run_dir": RUN}), encoding="utf-8")
    (run_dir / "agents" / "a_01.md").write_text("讀 {0} 之後整理如下\n".format(CALL), encoding="utf-8")
    archive_dir = tmp_path / "_src" / "TSM_20261017"

    ddreport._archive_run_dir(run_dir, archive_dir)

    archived = sorted(p for p in archive_dir.rglob("*") if p.is_file())
    assert len(archived) == 3
    for p in archived:
        assert _clean(p.read_text(encoding="utf-8")), p
    item = json.loads((archive_dir / "TSM_20261017.transcript_digest.json").read_text(encoding="utf-8"))["items"][0]
    assert Path(item["file"]).name == Path(CALL).name
    # run 目錄原樣（agent 還要照路徑開檔）
    assert json.loads((run_dir / "digest.json").read_text(encoding="utf-8")) == digest


def test_put_transcripts_scrubs_but_keeps_latest_quarter(tmp_path):
    store = FactsStore(tmp_path, "TSM")
    obj = {"selected": {"recent_four_quarters": [CALL]}, "digest_path": RUN}
    store.put_transcripts(obj, "2026-10-17", "TSM_20261017")
    raw = (tmp_path / "facts" / "TSM" / "transcripts.json").read_text(encoding="utf-8")
    assert _clean(raw)
    assert obj["digest_path"] == RUN  # 傳進來的物件不被改動
    assert store.latest_transcript_date() == "20251016"
