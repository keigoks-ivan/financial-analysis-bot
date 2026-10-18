#!/usr/bin/env python3
"""歸檔橫幅（2026-10-18 影子／對照線整理）。

七條已停止更新的線，頁面頂端統一放一個灰色橫幅：「已歸檔・2026-10-18 停止更新」加一句結論。
結論文字只在這個檔案維護，三個地方共用：
  1. 各頁的產生腳本（leverage／noma／tw_semivol／c1／gld／turtle）在 {NAV_BLOCK} 後面接
     archive_banner(key)，以後手動重產頁面時橫幅不會消失；
  2. 系統主控台歸檔區（scripts/build_long_track_index.py）讀 ARCHIVE_TEXT 當每條線的一句結論；
  3. 已經產出的 HTML 用本檔 --apply 一次性補上（冪等，以 <!--archive-banner--> 為界，重跑只會換內容）。

2026-10-19 追加第八條：SMH 槓桿疊加（/long-track-smh/leverage/，key＝smh_leverage），
橫幅的日期與標籤沿用本檔的 ARCHIVE_DATE。

F70 的頁面（/backtest/f_comfort/）走回測區既有的「退役橫幅」機制（docs/backtest/_page_meta.py 的
RET_BANNER），文字同 ARCHIVE_TEXT["f70"]。

用法：
    python3 scripts/archive_banner.py --apply   # 補進六個已產出的 HTML（只動橫幅區塊）
    python3 scripts/archive_banner.py --check   # 只檢查各頁橫幅是否在、文字是否一致
"""
from __future__ import annotations

import sys
from pathlib import Path

ARCHIVE_DATE = "2026-10-18"
ARCHIVE_LABEL = f"已歸檔・{ARCHIVE_DATE} 停止更新"

# 每條線的一句結論（寫在頁面頂端橫幅，也寫在系統主控台歸檔區）
ARCHIVE_TEXT = {
    "leverage": "這條線從 2026-10-19 起成為台股實單，也是美股實單的股票部分。本頁停止更新，之前的影子紀錄保留。",
    "c1": "這條線從 2026-10-19 起成為美股實單。本頁停止更新，之前的影子紀錄保留。",
    "noma": "均線條件只在借錢時才有作用，2026-10-19 起實單不借錢，這個問題不再影響實單。",
    "tw_semivol": "持有人 2026-08-17 決定不採用（台股勝出、美股沒有），而且這條線跑在已經退下的舊規則上。",
    "gld": "實單 2026-10-19 起已有黃金腿（週線三條件版），單腿 GLD 追蹤不再需要。",
    "turtle": "這條線疊在 2026-07-23 停更的舊美股系統（STX50）上，比較的基礎已經不存在。",
    "smh_leverage": "疊在 2026-07-23 停更的舊美股系統 STX50 上，比較的基礎已經不存在。",
    "f70": "持有人 2026-10-18 決定歸檔。「股票以外要不要放別的資產」改由債金版回答。",
}

# key → 已產出的 HTML（相對於 repo 根目錄）。F70 不在這裡（走 _page_meta 的 RET_BANNER）。
PAGES = {
    "leverage": "docs/long-track-w52-adaptive/leverage.html",
    "c1": "docs/long-track-w52-adaptive/c1-shadow.html",
    "noma": "docs/long-track-w52-adaptive/noma.html",
    "tw_semivol": "docs/long-track-w52-adaptive/tw-semivol.html",
    "gld": "docs/long-track-gld/index.html",
    "turtle": "docs/turtle-sleeve/index.html",
    "smh_leverage": "docs/long-track-smh/leverage/index.html",
}

START = "<!--archive-banner-->"
END = "<!--/archive-banner-->"


def archive_banner(key: str) -> str:
    """單行 HTML（自帶行內樣式，不依賴各頁的 CSS 變數），夾在標記之間。"""
    txt = ARCHIVE_TEXT[key]
    return (
        f'{START}<div style="background:#f4f4f5;border-bottom:1px solid #d4d4d8;border-left:6px solid #71717a;'
        f'color:#3f3f46;padding:.8rem 1.2rem;font-size:.9rem;line-height:1.7">'
        f'<div style="max-width:1080px;margin:0 auto"><b>{ARCHIVE_LABEL}</b>　{txt}'
        f'　<a href="/long-track/#archive" style="color:#1a56db;font-weight:600;white-space:nowrap">系統主控台歸檔區 →</a>'
        f'</div></div>{END}'
    )


def _nav_end(text: str) -> int:
    """<body> 之後全站導覽列結束的位置（導覽列由 site_nav 管，橫幅放在它後面，重生導覽不會動到）。"""
    b = text.find("<body")
    if b < 0:
        raise ValueError("no <body>")
    b = text.find(">", b) + 1
    h = text.find("</header>", b)
    if h < 0:
        return b
    pos = h + len("</header>")
    nxt = text[pos:].lstrip("\n")
    if nxt.startswith("<script>(function(){document.querySelectorAll('.imq-dd-btn')"):
        s = text.find("</script>", pos) + len("</script>")
        return s
    return pos


def apply_to_html(text: str, key: str) -> str:
    """把橫幅放進 HTML（已有則整塊換掉）。"""
    banner = archive_banner(key)
    if START in text and END in text:
        a = text.index(START)
        b = text.index(END) + len(END)
        return text[:a] + banner + text[b:]
    pos = _nav_end(text)
    return text[:pos] + "\n" + banner + text[pos:]


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    mode = argv[1] if len(argv) > 1 else ""
    if mode not in ("--apply", "--check"):
        print(__doc__)
        return 2
    bad = 0
    for key, rel in PAGES.items():
        p = root / rel
        text = p.read_text(encoding="utf-8")
        new = apply_to_html(text, key)
        if mode == "--apply":
            if new != text:
                p.write_text(new, encoding="utf-8")
                print(f"[apply] {rel}")
            else:
                print(f"[same ] {rel}")
        else:
            ok = new == text
            bad += 0 if ok else 1
            print(f"[{'ok' if ok else 'MISSING/STALE'}] {rel}")
    return 1 if (mode == "--check" and bad) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
