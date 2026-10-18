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

2026-10-19 追加選股區三頁（持有人拍板）：Quality-Entry（/dd-screener/quality-entry.html）、
Tier Matrix（/id/tier_matrix.html）、衛星·循環軌（/dd-screener/cyclical-track.html），key 與文字放在下面的
SCREEN_ARCHIVE，日期標籤是 2026-10-19，連結指向各自的上一層（不是長線系統主控台）。上面七條長線的 PAGES、
ARCHIVE_TEXT 與 ARCHIVE_LABEL 完全不動。

F70 的頁面（/backtest/f_comfort/）走回測區既有的「退役橫幅」機制（docs/backtest/_page_meta.py 的
RET_BANNER），文字同 ARCHIVE_TEXT["f70"]。

用法：
    python3 scripts/archive_banner.py --apply   # 補進已產出的 HTML（只動橫幅區塊；含 2026-10-19 追加的三個手動報告索引與三個選股頁）
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

# 2026-10-19 追加三條手動報告類（週報、多股對比、期望落差）。它們不是影子線，不進系統主控台歸檔區，
# 所以不放進上面的 ARCHIVE_TEXT／PAGES（那兩個的測試假設標籤固定、頁首是 page-hdr）。
# key → (標籤, 一句結論, 連結網址或 None, 連結文字)。標籤寫最後更新日，不寫歸檔日。
# 連結帶 target=_top：多股對比、期望落差的 _body.html 是研究清單分頁裡的 iframe 片段。
MANUAL_ARCHIVE = {
    "weekly": (
        "已歸檔・最後更新 2026-06-21",
        "每週深度週報在這一期之後不再新增，內容由每日簡報與市況主控台接手。頁面保留，因為個股報告仍引用這些週報。",
        "/market/", "市況主控台 →",
    ),
    "comparisons": (
        "已歸檔・最後更新 2026-06-11",
        "多股對比不再新增，已有的 14 份保留供查。",
        None, "",
    ),
    "synthesis": (
        "已歸檔・最後更新 2026-07-01",
        "期望落差綜合研判不再新增，已有的 6 份保留供查。",
        None, "",
    ),
}
MANUAL_PAGES = {
    "weekly": "docs/weekly/index.html",
    "comparisons": "docs/comparisons/_body.html",
    "synthesis": "docs/research/synthesis/_body.html",
}

# ── 2026-10-19 選股區三頁歸檔 ──────────────────────────────────────────────────
SCREEN_ARCHIVE_DATE = "2026-10-19"
SCREEN_ARCHIVE_LABEL = f"已歸檔・{SCREEN_ARCHIVE_DATE} 停止更新"
SCREEN_ARCHIVE = {
    "quality_entry": {
        "page": "docs/dd-screener/quality-entry.html",
        "text": "持有人 2026-10-19 決定歸檔：這頁的複合分沒有任何決策流程在用，選股排序以席位引擎和 DD Screener 主表為準。"
                "頁面和最後一版名單保留，每日快照已移出網站。",
        "link": ("/dd-screener/", "DD Screener 主表 →"),
    },
    "tier_matrix": {
        "page": "docs/id/tier_matrix.html",
        "text": "持有人 2026-10-19 決定歸檔：Tier 分級停在 2026-07-05 的判斷，原訂 60 天複審沒有做。"
                "本頁保留作為當時的定見紀錄，Tier 不再更新；表中訊號、裁決等即時欄位仍讀 DD Screener 的當日資料，"
                "個股現行判斷以 DD 報告為準。",
        "link": ("/id/", "產業深度索引 →"),
    },
    "cyclical_track": {
        "page": "docs/dd-screener/cyclical-track.html",
        "text": "持有人 2026-10-19 決定歸檔：循環股不再單獨列一條線。本頁停止更新，名單停在最後一次產生的版本；"
                "循環軌的資料仍每週產生，選股主控台陣容表的等待池位置閘還在讀它。",
        "link": ("/cockpit/", "選股主控台 →"),
    },
}

START = "<!--archive-banner-->"
END = "<!--/archive-banner-->"


def archive_banner(key: str) -> str:
    """單行 HTML（自帶行內樣式，不依賴各頁的 CSS 變數），夾在標記之間。"""
    if key in SCREEN_ARCHIVE:
        return _screen_banner(key)
    if key in MANUAL_ARCHIVE:
        label, txt, href, link_text = MANUAL_ARCHIVE[key]
        link = (f'　<a href="{href}" target="_top" style="color:#1a56db;font-weight:600;white-space:nowrap">{link_text}</a>'
                if href else "")
    else:
        label, txt = ARCHIVE_LABEL, ARCHIVE_TEXT[key]
        link = '　<a href="/long-track/#archive" style="color:#1a56db;font-weight:600;white-space:nowrap">系統主控台歸檔區 →</a>'
    return (
        f'{START}<div style="background:#f4f4f5;border-bottom:1px solid #d4d4d8;border-left:6px solid #71717a;'
        f'color:#3f3f46;padding:.8rem 1.2rem;font-size:.9rem;line-height:1.7">'
        f'<div style="max-width:1080px;margin:0 auto"><b>{label}</b>　{txt}'
        f'{link}'
        f'</div></div>{END}'
    )


def _screen_banner(key: str) -> str:
    """選股區三頁的橫幅：同樣式，日期標籤是 2026-10-19，連結指向各自的上一層。"""
    spec = SCREEN_ARCHIVE[key]
    href, label = spec["link"]
    return (
        f'{START}<div style="background:#f4f4f5;border-bottom:1px solid #d4d4d8;border-left:6px solid #71717a;'
        f'color:#3f3f46;padding:.8rem 1.2rem;font-size:.9rem;line-height:1.7">'
        f'<div style="max-width:1080px;margin:0 auto"><b>{SCREEN_ARCHIVE_LABEL}</b>　{spec["text"]}'
        f'　<a href="{href}" style="color:#1a56db;font-weight:600;white-space:nowrap">{label}</a>'
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
    # dd-screener 各頁在 </header> 後面多一條次選單（<div class="imq-subnav">…</div></div>），橫幅放在它後面
    rest = text[pos:].lstrip("\n")
    if rest.startswith('<div class="imq-subnav">'):
        s = text.find("</div></div>", len(text) - len(rest))
        if s >= 0:
            pos = s + len("</div></div>")
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
    all_pages = {**PAGES, **MANUAL_PAGES, **{k: v["page"] for k, v in SCREEN_ARCHIVE.items()}}
    for key, rel in all_pages.items():
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
