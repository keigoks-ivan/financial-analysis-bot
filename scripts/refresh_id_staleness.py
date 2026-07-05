#!/usr/bin/env python3
"""Refresh ID staleness — 把產業 ID 的鮮度從「發布時蓋章」變成「週更動態翻牌」。

半衰期規則（SKILL.md `sections_refreshed` 三桶）：
  - technical  > 365 天 → 🟡 stale-tech
  - market     >  90 天 → 🟠 stale-market
  - judgment   >  60 天 → 🔴 stale-judgment（建議刷新）

本 script 唯讀掃 docs/id/ID_*.html canonical（排除 _full.html）的 <script id="id-meta"> JSON，
依當天日期重算三桶狀態，然後：
  1. 更新 docs/id/INDEX.md 主表「鮮度」欄 → 標準格式
     `tech:YYYY-MM-DD {emoji} ｜ market:YYYY-MM-DD {emoji} ｜ judgment:YYYY-MM-DD {emoji}`
  2. 對 judgment 已 stale（🔴）的 ID 卡片，在 docs/id/index.html 注入冪等 stale pill。

零 churn 協議：內容無變化不寫檔（weekly run 無事時零 diff）。
--dry-run 只印摘要不寫檔；--today YYYY-MM-DD 覆寫「當天」（測試 / 回放用）。
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import date, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID_DIR = os.path.join(REPO, "docs", "id")
INDEX_MD = os.path.join(ID_DIR, "INDEX.md")
INDEX_HTML = os.path.join(ID_DIR, "index.html")

# 半衰期（天）
HALF_LIFE = {"technical": 365, "market": 90, "judgment": 60}
# 各桶過期時的 emoji
STALE_EMOJI = {"technical": "🟡", "market": "🟠", "judgment": "🔴"}
FRESH = "🟢"

META_RE = re.compile(
    r'<script[^>]*id=["\']id-meta["\'][^>]*>(.*?)</script>', re.S
)


def parse_date(s):
    y, m, d = map(int, s.split("-"))
    return date(y, m, d)


def scan(today):
    """回傳 (results, stats)。

    results: dict filename -> {
        'buckets': {bucket: {'date': 'YYYY-MM-DD', 'emoji': ..., 'stale': bool, 'age': int}},
        'freshness_cell': 標準格式字串,
        'judgment_stale': bool,
    }
    stats: dict 計數
    """
    files = sorted(
        f for f in glob.glob(os.path.join(ID_DIR, "ID_*.html"))
        if not f.endswith("_full.html")
    )
    results = {}
    stats = {
        "total_canonical": len(files),
        "no_meta": 0,
        "no_sections_refreshed": 0,
        "parsed": 0,
        "stale_tech": 0,
        "stale_market": 0,
        "stale_judgment": 0,
        "expiring_30d": 0,  # judgment 30 天內將過期（尚未過但快到）
    }
    for path in files:
        fn = os.path.basename(path)
        try:
            html = open(path, encoding="utf-8").read()
        except OSError:
            continue
        m = META_RE.search(html)
        if not m:
            stats["no_meta"] += 1
            continue
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError:
            stats["no_meta"] += 1
            continue
        sr = meta.get("sections_refreshed")
        if not sr or not all(k in sr for k in ("technical", "market", "judgment")):
            stats["no_sections_refreshed"] += 1
            continue
        stats["parsed"] += 1

        buckets = {}
        for bucket in ("technical", "market", "judgment"):
            try:
                d = parse_date(sr[bucket])
            except (ValueError, AttributeError):
                # 壞日期 → 視為缺欄，整檔跳過
                buckets = None
                break
            age = (today - d).days
            stale = age > HALF_LIFE[bucket]
            buckets[bucket] = {
                "date": sr[bucket],
                "emoji": STALE_EMOJI[bucket] if stale else FRESH,
                "stale": stale,
                "age": age,
            }
        if buckets is None:
            stats["no_sections_refreshed"] += 1
            continue

        if buckets["technical"]["stale"]:
            stats["stale_tech"] += 1
        if buckets["market"]["stale"]:
            stats["stale_market"] += 1
        if buckets["judgment"]["stale"]:
            stats["stale_judgment"] += 1
        # judgment 尚未過期但 30 天內將過期
        j = buckets["judgment"]
        if not j["stale"] and (HALF_LIFE["judgment"] - j["age"]) <= 30:
            stats["expiring_30d"] += 1

        cell = (
            f"tech:{buckets['technical']['date']} {buckets['technical']['emoji']}"
            f" ｜ market:{buckets['market']['date']} {buckets['market']['emoji']}"
            f" ｜ judgment:{buckets['judgment']['date']} {buckets['judgment']['emoji']}"
        )
        results[fn] = {
            "buckets": buckets,
            "freshness_cell": cell,
            "judgment_stale": buckets["judgment"]["stale"],
        }
    return results, stats


FILENAME_CELL_RE = re.compile(r"^ID_\w+\.html$")


def update_index_md(results, dry_run):
    """重寫 INDEX.md 主表鮮度欄。回傳 (changed, updated_count, skipped_rows)。

    對齊策略：對每個 markdown table row（以 | 開頭），split by '|'，找出內容恰為
    某個掃描到之檔名的 cell（＝檔名欄），把它「前一個」cell（＝鮮度欄）重寫為標準格式。
    對齊不到 / 無鮮度欄 / 檔名不在 results → 跳過不動，記 log。
    """
    orig = open(INDEX_MD, encoding="utf-8").read()
    lines = orig.split("\n")
    out = []
    updated = 0
    skipped = []
    for line in lines:
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            out.append(line)
            continue
        parts = line.split("|")
        # 找檔名欄
        fn_idx = None
        for i, p in enumerate(parts):
            if FILENAME_CELL_RE.match(p.strip()):
                fn_idx = i
                break
        if fn_idx is None:
            out.append(line)
            continue
        fn = parts[fn_idx].strip()
        if fn not in results:
            skipped.append(fn)  # 檔名有但無 sections_refreshed（stub/geo）
            out.append(line)
            continue
        if fn_idx - 1 < 1:
            # 檔名前無鮮度欄（不該發生於主表，但防呆）
            skipped.append(fn)
            out.append(line)
            continue
        # 保留原 cell 的左右一格 padding 風格
        new_cell = " " + results[fn]["freshness_cell"] + " "
        if parts[fn_idx - 1] == new_cell:
            out.append(line)  # 已是最新，零 churn
            continue
        parts[fn_idx - 1] = new_cell
        out.append("|".join(parts))
        updated += 1

    new_text = "\n".join(out)
    changed = new_text != orig
    if changed and not dry_run:
        with open(INDEX_MD, "w", encoding="utf-8") as f:
            f.write(new_text)
    return changed, updated, skipped


PILL_HTML = '<span class="stale-pill">🔴 judgment 過期</span>'
STALE_CSS = (
    ".stale-pill{display:inline-flex;align-items:center;background:#b3261e;"
    "color:#fff;padding:1px 7px;border-radius:9px;font-size:9.5px;font-weight:700;"
    "letter-spacing:.2px;line-height:1.4;vertical-align:middle;margin-left:4px}"
)


def update_index_html(results, dry_run):
    """對 judgment🔴 卡片注入冪等 stale pill；狀態恢復 🟢 時移除。

    回傳 (changed, injected_count).
    """
    orig = open(INDEX_HTML, encoding="utf-8").read()
    html = orig

    # 1) 先移除所有既有 pill block（配對 marker，backref 保證成對），確保冪等
    html = re.sub(
        r"<!-- STALE_PILL:(ID_\S+) -->.*?<!-- /STALE_PILL:\1 -->",
        "",
        html,
        flags=re.S,
    )

    # 2) 對目前 judgment stale 的檔案重新注入
    stale_files = [fn for fn, r in results.items() if r["judgment_stale"]]
    injected = 0
    for fn in stale_files:
        # 錨在該檔 canonical 的 tc-title anchor 後面
        title_re = re.compile(
            r'(<a class="tc-title" href="/id/' + re.escape(fn) + r'">.*?</a>)',
            re.S,
        )
        pill = (
            f"<!-- STALE_PILL:{fn} -->{PILL_HTML}<!-- /STALE_PILL:{fn} -->"
        )
        html, n = title_re.subn(r"\1" + pill, html, count=1)
        if n:
            injected += 1

    # 3) 若有注入且 CSS 未存在 → 補一條極簡規則（放 .v2-badge 之後）
    if injected and ".stale-pill{" not in html:
        anchor = ".v2-badge{"
        pos = html.find(anchor)
        if pos != -1:
            # 找該規則結尾的 '}' 後插入
            end = html.find("}", pos)
            if end != -1:
                html = html[: end + 1] + STALE_CSS + html[end + 1 :]

    changed = html != orig
    if changed and not dry_run:
        with open(INDEX_HTML, "w", encoding="utf-8") as f:
            f.write(html)
    return changed, injected


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="只印摘要不寫檔")
    ap.add_argument(
        "--today",
        default=None,
        help="覆寫『當天』日期 YYYY-MM-DD（測試 / 回放用；預設系統當天）",
    )
    args = ap.parse_args()

    today = parse_date(args.today) if args.today else date.today()

    results, stats = scan(today)

    if not args.dry_run:
        md_changed, md_updated, md_skipped = update_index_md(results, dry_run=False)
        html_changed, html_injected = update_index_html(results, dry_run=False)
    else:
        md_changed, md_updated, md_skipped = update_index_md(results, dry_run=True)
        html_changed, html_injected = update_index_html(results, dry_run=True)

    # ── fleet 摘要 ──
    print(f"=== ID staleness fleet 摘要（as of {today.isoformat()}）===")
    print(f"canonical ID 檔      : {stats['total_canonical']}")
    print(f"  有 sections_refreshed: {stats['parsed']}")
    print(f"  無 id-meta          : {stats['no_meta']}")
    print(f"  無 sections_refreshed: {stats['no_sections_refreshed']}")
    print("--- stale 桶（依半衰期）---")
    print(f"  🟡 tech  過期 (>365d): {stats['stale_tech']}")
    print(f"  🟠 market 過期 (>90d): {stats['stale_market']}")
    print(f"  🔴 judgment 過期(>60d): {stats['stale_judgment']}")
    print(f"  ⏳ judgment 30 天內將過期: {stats['expiring_30d']}")
    print("--- 寫檔 ---")
    mode = "[dry-run 不寫]" if args.dry_run else ""
    print(f"  INDEX.md   : {'CHANGED' if md_changed else 'no change'}"
          f" (鮮度欄翻牌 {md_updated} 行, 跳過 {len(md_skipped)} 個無 SR 檔名) {mode}")
    print(f"  index.html : {'CHANGED' if html_changed else 'no change'}"
          f" (stale pill 注入 {html_injected}) {mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
