#!/usr/bin/env python3
"""把 _page_meta.py 的標題、狀態標籤與橫幅套到 /backtest/ 各頁（可重複執行，冪等）。

每頁會被做的事：
  1. <title> 與頁首 <h1> 換成白話標題（txf_daily／txf_hourly 沒有頁首區塊，只換 <title>）。
  2. 麵包屑最後一段換成短標籤。
  3. 在頁首（.sub 之後）放一塊 <!--bt-meta-->…<!--/bt-meta-->：狀態標籤＋該頁需要的橫幅
     （對照線／退役存檔／「本頁是某主頁某一章的完整版」）。重跑時整塊重寫。
  4. <head> 內放一份 <style id="bt-meta-style">。

頁面若由 v7-backtest 或 scripts/build_*.py 重新產生，標題與標籤會被蓋回原樣；重產後再跑一次本檔即可。

用法：python3 _apply_meta.py [--check]
"""
from __future__ import annotations

import html as H
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import _page_meta as PM  # noqa: E402

STYLE_ID = "bt-meta-style"
CSS = """
.bt-meta{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin:.7rem 0 0;font-size:.82rem}
.bt-st{display:inline-block;font-size:.78rem;font-weight:700;padding:.12rem .6rem;border-radius:999px;line-height:1.5;border:1px solid transparent}
.bt-st-live{background:#fbf3df;color:#7a5a1a;border-color:#e6cf98}
.bt-st-cand{background:#e8f0fb;color:#1d4ea0;border-color:#b9cdee}
.bt-st-note{background:#eef1f4;color:#4b5563;border-color:#d7dce2}
.bt-st-rej{background:#fbeceb;color:#b42318;border-color:#f0c4c0}
.bt-st-ret{background:#f1f1f1;color:#6b7280;border-color:#d4d4d4}
.bt-st-def{color:#6b7280;font-size:.8rem}
.bt-banner{margin:.7rem 0 0;padding:.6rem .9rem;border-radius:8px;font-size:.86rem;line-height:1.65;border:1px solid;border-left-width:4px}
.bt-banner a{font-weight:600}
.bt-banner-ref{background:#fffbeb;border-color:#fde68a;border-left-color:#d97706;color:#78350f}
.bt-banner-ret{background:#f4f4f5;border-color:#d4d4d8;border-left-color:#71717a;color:#3f3f46}
.bt-banner-member{background:#eff6ff;border-color:#bfdbfe;border-left-color:#1a56db;color:#1e3a5f}
.mchap>.bt-banner{margin:.2rem 0 1rem}
"""
SUFFIX = " | InvestMQuest Research"
META_RE = re.compile(r"<!--bt-meta-->.*?<!--/bt-meta-->", re.S)


def rel_path(url: str) -> Path:
    r = url.replace("/backtest/", "", 1)
    return ROOT / (r + "index.html" if r.endswith("/") else r)


def is_stub(text: str) -> bool:
    return 'http-equiv="refresh"' in text[:1500] and len(text) < 4000


def banners_for(url: str) -> str:
    out = []
    if url in PM.REF_BANNER_URLS:
        out.append(f'<div class="bt-banner bt-banner-ref">{PM.REF_LINE}</div>')
    if url in PM.RET_BANNER:
        out.append(f'<div class="bt-banner bt-banner-ret">{PM.RET_BANNER[url]}</div>')
    m = PM.MEMBERS.get(url)
    if m:
        main = PM.PAGES[m["main"]]
        out.append(
            f'<div class="bt-banner bt-banner-member">本頁是「{H.escape(main["title"])}」中「{H.escape(m["chapter"])}」一節的完整版。'
            f'<a href="{m["main"]}#{m["anchor"]}">回到該節 →</a></div>')
    return "".join(out)


def meta_block(url: str, status: str) -> str:
    # 個別頁面的標籤與說明可在 _page_meta.CHIP_OVERRIDE 覆寫（2026-10-19 規則切換後的舊規則證據頁等）
    label, defn, cls = PM.CHIP_OVERRIDE.get(url, (PM.STATUS[status], PM.STATUS_DEF[status], status))
    chip = (f'<div class="bt-meta"><span class="bt-st bt-st-{cls}">{label}</span>'
            f'<span class="bt-st-def">{defn}</span></div>')
    return f"<!--bt-meta-->{chip}{banners_for(url)}<!--/bt-meta-->"


def ensure_style(text: str) -> str:
    block = f'<style id="{STYLE_ID}">{CSS}</style>'
    if f'id="{STYLE_ID}"' in text:
        return re.sub(rf'<style id="{STYLE_ID}">.*?</style>', lambda _m: block, text, count=1, flags=re.S)
    return text.replace("</head>", block + "\n</head>", 1)


CHIP_ONLY = {"/backtest/country_scan/us.html"}  # 版型自成一格（masthead），只放標籤、不動標題


def apply_one(url: str, title: str, short: str, status: str) -> str | None:
    p = rel_path(url)
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    if is_stub(text):
        return None
    orig = text
    t_esc = H.escape(title, quote=False)
    if url not in CHIP_ONLY:
        text = re.sub(r"<title>.*?</title>", lambda _m: f"<title>{t_esc}{SUFFIX}</title>", text, count=1, flags=re.S)
    text = ensure_style(text)
    text = META_RE.sub("", text)
    has_hdr = 'class="page-hdr"' in text or "class='page-hdr'" in text
    if url in CHIP_ONLY:
        block = meta_block(url, status)
        m = re.search(r'<div class="kicker">.*?</div>', text, flags=re.S)
        if not m:
            return f"{url}: 找不到放標籤的位置"
        text = text[:m.end()] + block + text[m.end():]
    elif has_hdr:
        # 舊的行內狀態字樣（F 組合頁的「研究候選・未採用」）由新標籤取代
        text = re.sub(r'<span class="status">[^<]*</span>', "", text)
        text = re.sub(r"(<h1\b[^>]*>).*?(</h1>)", lambda m: f"{m.group(1)}{t_esc}{m.group(2)}", text, count=1, flags=re.S)
        text = re.sub(r'(<div class="crumb">.*? / )((?:(?! / )[^<>])*?)(</div>)',
                      lambda m: f"{m.group(1)}{H.escape(short, quote=False)}{m.group(3)}", text, count=1, flags=re.S)
        block = meta_block(url, status)
        m = re.search(r'<div class="sub">.*?</div>', text, flags=re.S)
        if m:
            text = text[:m.end()] + block + text[m.end():]
        else:
            m = re.search(r"</h1>", text)
            text = text[:m.end()] + block + text[m.end():]
    else:
        # txf_daily／txf_hourly：沒有頁首區塊，標籤放在 eyebrow 之後
        block = meta_block(url, status)
        m = re.search(r"<p class='eyebrow'>.*?</p>", text, flags=re.S)
        if not m:
            return f"{url}: 找不到放標籤的位置"
        text = text[:m.end()] + block + text[m.end():]
    if text != orig:
        p.write_text(text, encoding="utf-8")
    return "changed" if text != orig else "same"


def main() -> int:
    check = "--check" in sys.argv
    changed = same = missing = 0
    problems = []
    for url, rec in PM.PAGES.items():
        r = apply_one(url, rec["title"], rec["short"], rec["status"]) if not check else "skip"
        if r is None:
            missing += 1
        elif r == "changed":
            changed += 1
        elif r == "same":
            same += 1
        elif r != "skip":
            problems.append(r)
    for url, m in PM.MEMBERS.items():
        r = apply_one(url, m["title"], m["short"], m["status"]) if not check else "skip"
        if r is None:
            missing += 1
        elif r == "changed":
            changed += 1
        elif r == "same":
            same += 1
        elif r != "skip":
            problems.append(r)
    print(f"套用 {changed}、無變動 {same}、檔案不存在或為跳轉頁 {missing}")
    for x in problems:
        print("⚠", x)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
