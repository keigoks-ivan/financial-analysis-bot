#!/usr/bin/env python3
"""2026-10-19：docs/intel 資料檔的保留規則（站台體積逼近 GitHub Pages 的 1 GB 上限，這兩處原本每天各增加約 0.35 MB）。

只處理檔名恰為 YYYY-MM-DD.json 的每日檔；threads.json、theme_history.json、sources_health.json 這類每天覆寫的
狀態檔、sec_ticker_map.json 這類快取、日期頁 docs/intel/YYYY-MM-DD.html 都不碰。

- pending/YYYY-MM-DD.json（抓取後、AI 整理前的原始卡片）：只有當天的 run_daily.py 與 render.py（日報還沒產出時的後備）
  會讀，留最近 7 份。
- data/YYYY-MM-DD.json（每日整理結果）：theme_weekly.py 回看 7 天、harvest_intel_claims.py 取最新 7 份、
  市況主控台只讀最新一份，留最近 14 份。頁面不讀舊日報（故事線與主題趨勢另存在 threads.json、theme_history.json）。

被刪的舊檔由 ~/v7-backtest/tools/sync_site_data.py 在本機另存一份（data/intel_archive/）。規則在每次寫完日報後自動執行，
重複執行不會再刪（冪等）。
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

KEEP_PENDING = 7
KEEP_DAILY = 14

_DAY_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.json$")


def _dated_files(directory):
    """（日期、路徑），由舊到新；檔名日期不合法的不計入、不動。"""
    found = []
    for path in Path(directory).glob("*.json"):
        m = _DAY_FILE.match(path.name)
        if not m:
            continue
        try:
            day = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        found.append((day, path))
    return sorted(found)


def prune_dated(directory, keep, protect=()):
    """只留檔名日期最近的 keep 份，另加 protect 內的日期（YYYY-MM-DD 字串）。回傳實際刪除的檔名，由舊到新。"""
    directory = Path(directory)
    if not directory.is_dir():
        return []
    protected = set(protect)
    files = _dated_files(directory)
    cut = max(len(files) - keep, 0)
    removed = []
    for day, path in files[:cut]:
        if day.isoformat() in protected:
            continue
        path.unlink(missing_ok=True)
        removed.append(path.name)
    return removed


def prune_intel(data_dir, pending_dir, protect=(), keep_daily=KEEP_DAILY, keep_pending=KEEP_PENDING):
    """日報與抓取檔各自套用保留規則。protect 放這次正在處理的日期，補跑舊日期時才不會剛寫完就被清掉。"""
    return {
        "data": prune_dated(data_dir, keep_daily, protect),
        "pending": prune_dated(pending_dir, keep_pending, protect),
    }
