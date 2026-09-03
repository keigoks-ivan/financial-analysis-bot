#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_report_primer.py

機械注入「怎麼讀這份報告」白話導讀塊到 7 個報告家族的存量 HTML 檔。
純機械執行：不讀報告內文，只做 mechanical anchor 偵測 + 固定模板套用
（DD 家族依 dd-meta schema 版本字串做二選一分流，本身也是機械 regex 檢查，非內容理解）。

家族與 glob：
  dd          docs/dd/DD_*.html
  id          docs/id/ID_*.html
  dca         docs/dca/DCA_*.html          （legacy 凍結格式）
  earnings    docs/earnings/earnings_*.html
  macro       docs/macro/MACRO_*.html
  comparisons docs/comparisons/MS_*.html
  ds          docs/ds/DS_*.html            （legacy——見下方 DS 特殊處置）

DS 特殊處置：docs/ds/DS_*.html 現況已全部是「已封存」的 meta-refresh 轉址 stub
（90 行、<meta http-equiv="refresh" content="0; url=/id/">，無報告本文），
注入導讀對這種頁面沒有意義（頁面 0 秒轉址、讀者看不到）。腳本會偵測這個 stub
特徵並自動跳過，原因標記為 "ds-stub-redirect"。模板仍保留供持有人複審。

冪等：用 <!-- PLAIN_PRIMER_START --> / <!-- PLAIN_PRIMER_END --> 標記，重跑時整塊替換。

Anchor 優先序（fallback-safe，找不到就跳過不硬插）：
  1. 全站導覽 <header class="imq-nav-root">...</header>（site_nav.py 注入，覆蓋率最高）
  2. <body ...> 開始標籤
  3. </head> 結束標籤（少數殘缺 head 但無 body 標籤的舊檔）
  4. 第一個 </style> 結束標籤（完全無 html/head/body 骨架的純片段檔）
  找不到任何一種 → 跳過，reason="no-safe-anchor"

用法：
  python3 scripts/inject_report_primer.py --dry-run            # 全家族预演
  python3 scripts/inject_report_primer.py --dry-run --family dd
  python3 scripts/inject_report_primer.py                      # 全家族真跑
  python3 scripts/inject_report_primer.py --family id          # 單家族真跑
"""

import argparse
import glob
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MARKER_START = "<!-- PLAIN_PRIMER_START -->"
MARKER_END = "<!-- PLAIN_PRIMER_END -->"
MARKER_BLOCK_RE = re.compile(
    re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\n?", re.S
)

NAV_HEADER_RE = re.compile(r'<header class="imq-nav-root"[^>]*>.*?</header>', re.S)
BODY_TAG_RE = re.compile(r"<body[^>]*>", re.S)
HEAD_CLOSE_RE = re.compile(r"</head>", re.S)
FIRST_STYLE_CLOSE_RE = re.compile(r"</style>", re.S)

DS_STUB_MARK_RE = re.compile(r'<meta http-equiv="refresh" content="0; url=/id/">')

DD_NEW_SCHEMA_RE = re.compile(r'"schema"\s*:\s*"v1[345]')

# ---------------------------------------------------------------------------
# 共用樣式（inline，不依賴任何 class；淺色低調，不搶內文）
# ---------------------------------------------------------------------------

_DETAILS_OPEN = (
    '<details style="max-width:900px;margin:16px auto;background:#F8FAFC;'
    'border:1px solid #E2E8F0;border-radius:8px;padding:2px 18px 14px;'
    'font-family:\'Noto Sans TC\',-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;'
    'font-size:13px;line-height:1.9;color:#334155">\n'
    '<summary style="cursor:pointer;padding:12px 0;font-weight:600;color:#1E3A5F;'
    'font-size:13.5px">📖 第一次讀這種報告？點開看怎麼讀</summary>\n'
    '<div style="margin:2px 0 4px;padding-top:8px;border-top:1px solid #E2E8F0">\n'
)
_DETAILS_CLOSE = "</div>\n</details>"

_GLOSSARY_LINE = (
    '<p style="margin:6px 0 0">想查其他詞的意思，見'
    '<a href="/learn/glossary.html" style="color:#2563EB;text-decoration:underline">投資詞彙表</a>。</p>\n'
)


def _details(*paragraphs: str) -> str:
    body = "".join(f'<p style="margin:6px 0">{p}</p>\n' for p in paragraphs)
    return _DETAILS_OPEN + body + _GLOSSARY_LINE + _DETAILS_CLOSE


# ---------------------------------------------------------------------------
# 7 個家族模板（DD 依 schema 版本二選一，故共 8 個模板常數）
# ---------------------------------------------------------------------------

TEMPLATE_DD_NEW = _details(
    "這是一份「個股深度研究」（DD），從產業、商業模式、護城河到財務體質全面拆解一家公司，最後收斂成一個結論。",
    "<strong>結論在哪：</strong>報告後段的「統一裁決」——只有三種答案：進場、觀望、迴避，並附建議倉位角色（例如核心或衛星）。可以直接搜尋頁面上的「統一裁決」四個字，或跳到 <code>#decision</code> 錨點。",
    "<strong>常見詞：</strong>「護城河評等」是公司競爭優勢的等第（S 最強、X 幾乎沒有）；「ROIC」是投入資本報酬率，看公司一塊錢資本能賺回多少；「PEG」是本益成長比（本益比 ÷ 盈餘成長率），數字越低代表相對成長性越便宜。",
    "<strong>時效提醒：</strong>報告日期寫在檔名與開頭（例如 20260901 即 2026 年 9 月 1 日）。市場會變，這份結論是「當天」的判斷，最新狀態請看 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a> 的即時清單。",
)

TEMPLATE_DD_LEGACY = _details(
    "這是一份「個股深度研究」（DD），從產業、商業模式、護城河到財務體質分析一家公司。",
    "<strong>結論在哪：</strong>這是較舊格式，結論寫在報告後段（常見標題如「投資結論」），格式因報告年代而略有不同。如果同一檔股票另外找得到檔名開頭 DCA_ 的報告，那份才是獨立的「進場／觀望／迴避」決策層；2026 年中之後的新版報告已經把研究與決策合併成一份，最新結論請直接看 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a>。",
    "<strong>常見詞：</strong>「護城河評等」是公司競爭優勢的等第（S 最強、X 幾乎沒有）；「ROIC」是投入資本報酬率；「PEG」是本益成長比（本益比 ÷ 盈餘成長率），數字越低代表相對成長性越便宜。",
    "<strong>時效提醒：</strong>報告日期寫在檔名與開頭；這是「當時」的判斷，公司基本面與股價都可能已經改變。",
)

TEMPLATE_ID = _details(
    "這是一份「產業深度報告」（ID），研究整個產業的供需結構、競爭格局與展望，不是單一公司的結論。",
    "<strong>結論在哪：</strong>報告開頭的「決策摘要層」濃縮全篇重點；完整的情境判斷通常在後段標示「裁決」或「情境」的段落。",
    "<strong>常見詞：</strong>「論點」（thesis）是這份報告對產業走向的核心假設；「否證指標」是一旦數字打到某個門檻，代表論點可能已經不成立的監測指標；「priced-in」是指這個看法是不是已經反映在股價裡——如果已經反映，代表就算利多兌現，股價也不一定會再漲。",
    "<strong>時效提醒：</strong>報告日期寫在檔名，產業情勢變化快；相關個股的最新結論請看個別 DD 報告或 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a>。",
)

TEMPLATE_DCA = _details(
    "這是舊格式的「投資決策分析」（DCA），是 2026-06-22 併入 DD 報告之前獨立存在的決策層文件，內容已經凍結、不再更新。此格式已併入 DD，最新裁決見 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a>。",
    "<strong>結論在哪：</strong>報告後段的「§7 決策」（Decision）段落。",
    "<strong>常見詞：</strong>「不對稱報酬」是比較「猜對能賺多少」跟「猜錯會虧多少」哪邊比較划算；「Pre-mortem」是先假設投資已經失敗，倒推可能是哪裡出錯；「否證指標」是一旦觸發就代表論點可能不成立的監測門檻。",
    "<strong>時效提醒：</strong>這個格式已經退役，最新裁決請直接看同一檔股票最新的 DD 報告，或 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a> 的即時清單——這份只留作歷史紀錄，不代表現在的判斷。",
)

TEMPLATE_EARNINGS = _details(
    "這是財報分析報告，整理公司公布財報當下的數字重點與市場反應。",
    "<strong>結論在哪：</strong>通常在後段的「總結」；部分報告後面附加「Phase R 覆核」，是同一份報告針對特定結論的後續補充，不是新報告。",
    "<strong>常見詞：</strong>「EPS」是每股盈餘；「財測」（guidance）是公司自己對未來業績的預估；「優於預期／不如預期」是跟市場原本的共識預估比較後的結果，不是絕對的好壞——公司賺錢又成長，也可能因為「不如預期」股價當天下跌。",
    "<strong>時效提醒：</strong>這是財報「當天」的即時反應紀錄，之後股價與基本面可能已經變化，相關個股最新結論請看 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a>。",
)

TEMPLATE_MACRO = _details(
    "這是一份「總經深度報告」，研究單一總體經濟或政策主題（例如利率、匯率、資本支出循環），不是個股或產業的投資建議。",
    "這類報告只做環境判讀與情境準備，不給買賣訊號——結論在開頭的「§0 決策摘要層」，後段的情境樹與證偽表是報告主體。",
    "<strong>常見詞：</strong>「base rate」是歷史上類似情況實際發生的機率基準；「情境樹」是把未來拆成幾條分岔路徑（例如樂觀／基準／悲觀），各自附觸發條件；「priced-in」是市場是否已經把這個預期反映在價格裡。",
    "<strong>時效提醒：</strong>總經環境隨數據更新變化快，報告日期寫在檔名；相關個股的最新結論請看個別 DD 報告或 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a>。",
)

TEMPLATE_COMPARISONS = _details(
    "這是「多檔股票對比」報告，把 2 到 5 檔同類股票放進同一份報告，逐一打分比較。",
    "<strong>結論在哪：</strong>報告後段的「§E 最終裁決」，會直接說推薦哪一檔、不選其他檔的理由。",
    "<strong>常見詞：</strong>「IRR」是內部報酬率，衡量長期年化報酬常用的指標；「Max DD」是最大回撤，也就是持有期間可能面臨的最深跌幅；報告用短期（不到 12 個月）／中期（2-3 年）／中長期（3-5 年）／長期（5-10 年）四個時間框架分開比較，同一檔股票在不同框架下排名不同是正常的，不是報告矛盾。",
    "<strong>時效提醒：</strong>報告內的股價是寫作當時的快照，時間久了可能失真，最新狀態請看個別 DD 報告或 <a href=\"/research/\" style=\"color:#2563EB;text-decoration:underline\">/research/</a>。",
)

# DS：僅供持有人複審，實際跑批時全數會被 ds-stub-redirect 規則跳過（見檔頭說明）
TEMPLATE_DS = _details(
    "這是「產業敘述報告」（DS）的舊格式，已於 2026 年 6 月併入「產業深度 ID」，此格式已併入 ID，原內容不再於站上呈現。",
    "這個網址只會直接帶你跳轉到新版 <a href=\"/id/\" style=\"color:#2563EB;text-decoration:underline\">產業深度 ID</a>，等同於這份報告目前的替代版本。",
)


def dd_template_for(html: str) -> str:
    if DD_NEW_SCHEMA_RE.search(html):
        return TEMPLATE_DD_NEW
    return TEMPLATE_DD_LEGACY


FAMILIES = {
    "dd": {
        "glob": "docs/dd/DD_*.html",
        "template": dd_template_for,
    },
    "id": {
        "glob": "docs/id/ID_*.html",
        "template": lambda html: TEMPLATE_ID,
    },
    "dca": {
        "glob": "docs/dca/DCA_*.html",
        "template": lambda html: TEMPLATE_DCA,
    },
    "earnings": {
        "glob": "docs/earnings/earnings_*.html",
        "template": lambda html: TEMPLATE_EARNINGS,
    },
    "macro": {
        "glob": "docs/macro/MACRO_*.html",
        "template": lambda html: TEMPLATE_MACRO,
    },
    "comparisons": {
        "glob": "docs/comparisons/MS_*.html",
        "template": lambda html: TEMPLATE_COMPARISONS,
    },
    "ds": {
        "glob": "docs/ds/DS_*.html",
        "template": lambda html: TEMPLATE_DS,
    },
}


def find_anchor(html: str):
    """回傳 (insert_pos, anchor_kind) 或 (None, None)。"""
    m = NAV_HEADER_RE.search(html)
    if m:
        return m.end(), "nav-header"
    m = BODY_TAG_RE.search(html)
    if m:
        return m.end(), "body-tag"
    m = HEAD_CLOSE_RE.search(html)
    if m:
        return m.end(), "head-close"
    m = FIRST_STYLE_CLOSE_RE.search(html)
    if m:
        return m.end(), "first-style-close"
    return None, None


def process_file(path: Path, family: str, template_fn, dry_run: bool):
    """回傳 (action, reason) — action ∈ {inject, reinject, skip}。"""
    html = path.read_text(encoding="utf-8")

    if family == "ds" and DS_STUB_MARK_RE.search(html):
        return "skip", "ds-stub-redirect"

    block = template_fn(html)
    full_block = MARKER_START + "\n" + block + "\n" + MARKER_END + "\n"

    existing = MARKER_BLOCK_RE.search(html)
    if existing:
        new_html = html[: existing.start()] + full_block + html[existing.end() :]
        if new_html == html:
            return "skip", "no-change(idempotent-identical)"
        if not dry_run:
            path.write_text(new_html, encoding="utf-8")
        return "reinject", "existing-marker-replaced"

    pos, anchor_kind = find_anchor(html)
    if pos is None:
        return "skip", "no-safe-anchor"

    new_html = html[:pos] + "\n" + full_block + html[pos:]
    if not dry_run:
        path.write_text(new_html, encoding="utf-8")
    return "inject", anchor_kind


def inject_one(path: Path) -> bool:
    """單檔冪等注入（DD 家族限定；供 render_dd.py 呼叫）。

    回傳是否實際寫入了變更（True＝inject 或 reinject-with-change）。不改變
    既有 CLI 行為，純粹是 process_file() 對 DD 家族的薄包裝。
    """
    action, _reason = process_file(Path(path), "dd", dd_template_for, dry_run=False)
    return action in ("inject", "reinject")


def main():
    ap = argparse.ArgumentParser(description="注入報告家族「怎麼讀這份報告」導讀塊")
    ap.add_argument("--dry-run", action="store_true", help="只列出將注入/跳過清單，不寫檔")
    ap.add_argument(
        "--family",
        choices=list(FAMILIES.keys()) + ["all"],
        default="all",
        help="限定單一家族（預設全家族）",
    )
    args = ap.parse_args()

    families = list(FAMILIES.keys()) if args.family == "all" else [args.family]

    grand_total = {"inject": 0, "reinject": 0, "skip": 0}

    for fam in families:
        cfg = FAMILIES[fam]
        pattern = str(REPO_ROOT / cfg["glob"])
        files = sorted(glob.glob(pattern))
        template_fn = cfg["template"]

        print(f"\n=== 家族：{fam} （{len(files)} 檔，pattern={cfg['glob']}） ===")
        counts = {"inject": 0, "reinject": 0, "skip": 0}
        skip_reasons = {}

        for f in files:
            path = Path(f)
            action, reason = process_file(path, fam, template_fn, args.dry_run)
            counts[action] += 1
            grand_total[action] += 1
            rel = path.relative_to(REPO_ROOT)
            if action == "skip":
                skip_reasons.setdefault(reason, []).append(str(rel))
                print(f"  [skip:{reason}] {rel}")
            else:
                print(f"  [{action}:{reason}] {rel}")

        print(
            f"--- {fam} 小計：inject={counts['inject']} reinject={counts['reinject']} "
            f"skip={counts['skip']} ---"
        )
        if skip_reasons:
            for reason, flist in skip_reasons.items():
                print(f"    skip 原因「{reason}」共 {len(flist)} 檔")

    print(
        f"\n=== 總計：inject={grand_total['inject']} reinject={grand_total['reinject']} "
        f"skip={grand_total['skip']} （{'dry-run，未寫檔' if args.dry_run else '已寫檔'}） ==="
    )


if __name__ == "__main__":
    sys.exit(main())
