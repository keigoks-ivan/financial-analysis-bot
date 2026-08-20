#!/usr/bin/env python3
"""update_home_stats.py — 把首頁 hero 統計數字換成實際值。

docs/index.html hero 區的「個股 DD」「產業 ID」兩個數字是手動寫死的字面值
（例如「240+」「90+」），會隨著報告持續產出而過期。本腳本掃三個來源目錄的
實際檔案數，用 <div class="stat-num" data-stat="...">…</div> 的 data-stat
錨點做可重複執行的替換（不依賴脆弱的字面數字比對），讓 index.html 可以
之後隨時重跑同步。

計數規則：
  - dd-count  = docs/dd/DD_*.html 檔案數（個股 DD 報告總數，含同一 ticker
                多次報告；符號一致沿用站上既有「+」慣例）
  - id-count  = docs/id/ID_*.html 檔案數（含 _full 附文獻變體；產業 ID
                報告總數）
  - 另外掃 docs/t/*.html（排除 index.html）取得個股總覽頁數 = 實際覆蓋的
    不重複 ticker 數，僅供 console 輸出與人工核對用，不直接寫回 hero
    （hero 目前沒有對應的「個股覆蓋數」卡片，避免無中生有新增版位）。

可重複執行（idempotent）：重跑會用最新檔案數覆寫，不會累加。
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = REPO_ROOT / "docs" / "index.html"
DD_DIR = REPO_ROOT / "docs" / "dd"
ID_DIR = REPO_ROOT / "docs" / "id"
T_DIR = REPO_ROOT / "docs" / "t"


def count_dd() -> int:
    return len(list(DD_DIR.glob("DD_*.html")))


def count_id() -> int:
    return len(list(ID_DIR.glob("ID_*.html")))


def count_t_pages() -> int:
    return len([f for f in T_DIR.glob("*.html") if f.name != "index.html"])


def replace_stat(html: str, stat_key: str, new_value: str) -> str:
    pattern = re.compile(
        r'(<div class="stat-num" data-stat="' + re.escape(stat_key) + r'">)([^<]*)(</div>)'
    )
    new_html, n = pattern.subn(lambda m: m.group(1) + new_value + m.group(3), html)
    if n == 0:
        raise SystemExit(
            f"找不到 data-stat=\"{stat_key}\" 錨點於 {INDEX_HTML} —— "
            "hero 區塊可能被改過，需先確認 <div class=\"stat-num\" data-stat=...> 是否還在。"
        )
    return new_html


def main() -> None:
    dd_n = count_dd()
    id_n = count_id()
    t_n = count_t_pages()

    html = INDEX_HTML.read_text(encoding="utf-8")
    html = replace_stat(html, "dd-count", f"{dd_n}+")
    html = replace_stat(html, "id-count", f"{id_n}+")
    INDEX_HTML.write_text(html, encoding="utf-8")

    print(f"docs/dd/  DD_*.html      : {dd_n}  -> hero 個股 DD = {dd_n}+")
    print(f"docs/id/  ID_*.html      : {id_n}  -> hero 產業 ID = {id_n}+")
    print(f"docs/t/   *.html (-index): {t_n}  （個股總覽覆蓋 ticker 數，僅供核對，hero 無對應卡片）")


if __name__ == "__main__":
    main()
