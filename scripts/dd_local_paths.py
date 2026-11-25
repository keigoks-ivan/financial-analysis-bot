#!/usr/bin/env python3
"""把本機絕對路徑換成不帶帳號的寫法，給「會進 git 的存查檔」用（2026-11-25）。

這個 repo 是公開的。Google Drive 的資料夾名帶信箱
（`~/Library/CloudStorage/GoogleDrive-<信箱>/…`）、家目錄帶使用者名稱，
寫進存查檔就等於公開。這裡只換掉路徑前綴，檔名不動：

    /Users/<名稱>/Library/CloudStorage/GoogleDrive-<信箱>/我的雲端硬碟/007美股/TSM/x.md
        → ~/GoogleDrive/我的雲端硬碟/007美股/TSM/x.md
    /Users/<名稱>/financial-analysis-bot/.dd_build/runs/…
        → ~/financial-analysis-bot/.dd_build/runs/…

只用在存檔副本（`notes/site-internal/dd/_src/`、`facts/`）；run 目錄裡 agent
要照著開檔的路徑不動。沿用舊存查時靠檔名比對（`Path(file).name`），不受影響。
換完的字串不是可直接開啟的路徑，不要拿存檔裡的 `file` 欄位去開檔。
"""
import json
import re
from pathlib import Path

_SEG = r"[^/\s\"'<>|\\]+"
_GDRIVE_RE = re.compile(r"(?:/Users/" + _SEG + r"|~)/Library/CloudStorage/GoogleDrive-" + _SEG)
_GDRIVE_BARE_RE = re.compile(r"GoogleDrive-[^/\s\"'<>|\\@]*@" + _SEG)
_HOME_RE = re.compile(r"/Users/[A-Za-z0-9._-]+(?=/)")

TEXT_SUFFIXES = (".md", ".json", ".jsonl", ".txt", ".html", ".yml", ".yaml", ".csv")


def scrub(text):
    """回傳 `(新文字, 置換處數)`。冪等：換完再跑不會再命中。"""
    text, n1 = _GDRIVE_RE.subn("~/GoogleDrive", text)
    text, n2 = _GDRIVE_BARE_RE.subn("GoogleDrive", text)
    text, n3 = _HOME_RE.subn("~", text)
    return text, n1 + n2 + n3


def scrub_obj(obj):
    """對可轉成 JSON 的物件做 `scrub`，回傳新物件（原物件不動）。"""
    text, hits = scrub(json.dumps(obj, ensure_ascii=False))
    return json.loads(text) if hits else obj


def scrub_dir(root, suffixes=TEXT_SUFFIXES):
    """對目錄底下的文字檔做 `scrub`，有改才寫回（位元組層讀寫，保留換行原樣；
    非 UTF-8 的檔略過）。回傳 `(改動檔數, 總處數)`。"""
    files_changed = 0
    total_hits = 0
    for path in sorted(Path(root).rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            continue
        new_text, hits = scrub(text)
        if hits:
            path.write_bytes(new_text.encode("utf-8"))
            files_changed += 1
            total_hits += hits
    return files_changed, total_hits
