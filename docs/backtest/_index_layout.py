"""LIVE renderer for /backtest/index.html — 依問題分七區的回測目錄（2026-10 重整）。

資料來源：_page_meta.py（每頁的白話標題、所屬區、狀態、一行說明）。
首頁結構：
  * 頁首：標題、七區跳轉、狀態標籤圖例。
  * ①～⑦ 七區，每區列出該區的頁；已否決、已退役的頁收在每區底部的摺疊區。
  * ① 只放一個入口（/long-track/ 系統主控台，實盤證據都在那邊）。
  * 「方法與術語」放在最後，不算七區。
  * 頁尾：頁數與日期由程式計算（看實際檔案，不手寫）。

子專區（房價與所得、各國股市結構、外部策略檢驗）各佔一個入口。

Run: python3 _build_index.py   （本模組由它匯入，不直接執行）
"""
from __future__ import annotations

import html as H
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _page_meta as PM  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "bt")
ROOT = Path(__file__).parent
OUT = ROOT / "index.html"

LONG_TRACK_URL = "/long-track/"
ZONE_ID = {1: "z1", 2: "z2", 3: "z3", 4: "z4", 5: "z5", 6: "z6", 7: "z7", 8: "methods"}
CIRCLED = {1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤", 6: "⑥", 7: "⑦"}
DEAD = ("rej", "ret")

# 子專區入口附帶的市場連結（各國股市結構：美／台／日／馬）
EXTRA_LINKS = {
    "/backtest/country_scan/us.html": [
        ("美國", "/backtest/country_scan/us.html"), ("台灣", "/backtest/country_scan/taiwan.html"),
        ("日本", "/backtest/country_scan/japan.html"), ("馬來西亞", "/backtest/country_scan/malaysia.html"),
    ],
}


def _desc(p: dict) -> str:
    d = p.get("desc", "")
    return d


def _entry(url: str, p: dict) -> str:
    st = p["status"]
    extra = EXTRA_LINKS.get(url)
    title = H.escape(p["title"], quote=False)
    if extra:
        links = " · ".join(f'<a href="{u}">{H.escape(n)}</a>' for n, u in extra)
        head = f'<span class="ov-title">{title}</span>'
        tail = f'<div class="ov-extra">各市場：{links}</div>'
    else:
        head = f'<a class="ov-title" href="{url}">{title}</a>'
        tail = ""
    return (f'<li class="ov-entry"><span class="ov-st ov-st-{st}">{PM.STATUS[st]}</span>'
            f'<div class="ov-main">{head}<div class="ov-desc">{H.escape(_desc(p), quote=False)}</div>{tail}</div></li>')


def _zone_html(z: int) -> str:
    title, intro = PM.ZONES[z]
    label = f'{CIRCLED[z]} {title}' if z in CIRCLED else title
    urls = PM.ZONE_ORDER[z]
    if z == 1:
        n = len(urls)
        body = (f'<ul class="ov-list"><li class="ov-entry"><span class="ov-st ov-st-live">{PM.STATUS["live"]}</span>'
                f'<div class="ov-main"><a class="ov-title" href="{LONG_TRACK_URL}">系統主控台：實單系統的每日狀態與 {n} 頁實盤證據</a>'
                f'<div class="ov-desc">實單配置、每日訊號與追蹤紀錄，以及支撐它的檢驗（前瞻證偽、重抽樣、保險價格、合併帳戶、慢熊頻率、候選方案與已否決方案）。證據頁的網址不變，列表在主控台的「實盤證據」一節。</div></div></li></ul>')
        count = 1
    else:
        live = [u for u in urls if PM.PAGES[u]["status"] not in DEAD]
        dead = [u for u in urls if PM.PAGES[u]["status"] in DEAD]
        body = '<ul class="ov-list">' + "".join(_entry(u, PM.PAGES[u]) for u in live) + "</ul>"
        if dead:
            nr = sum(PM.PAGES[u]["status"] == "rej" for u in dead)
            nt = sum(PM.PAGES[u]["status"] == "ret" for u in dead)
            cap = "、".join(x for x in (f"已否決 {nr} 頁" if nr else "", f"已退役 {nt} 頁" if nt else "") if x)
            body += (f'<details class="ov-dead"><summary>{cap}</summary><ul class="ov-list">'
                     + "".join(_entry(u, PM.PAGES[u]) for u in dead) + "</ul></details>")
        count = len(urls)
    return (f'<section class="ov-zone" id="{ZONE_ID[z]}"><h2 class="ov-zone-hd">{label}'
            f'<span class="ov-zone-n">{count} 項</span></h2>'
            f'<p class="ov-zone-intro">{H.escape(intro, quote=False)}</p>{body}</section>')


def zones_html() -> str:
    return "".join(_zone_html(z) for z in sorted(PM.ZONES))


def zone_counts() -> dict:
    """首頁每區顯示的項目數（①只算一個入口）。"""
    return {z: (1 if z == 1 else len(PM.ZONE_ORDER[z])) for z in PM.ZONES}


def jump_html() -> str:
    out = []
    for z in sorted(PM.ZONES):
        t = PM.ZONES[z][0]
        lab = f"{CIRCLED[z]} {t}" if z in CIRCLED else t
        out.append(f'<a href="#{ZONE_ID[z]}">{lab}</a>')
    return "".join(out)


def legend_html() -> str:
    return "".join(
        f'<li><span class="ov-st ov-st-{k}">{PM.STATUS[k]}</span>{H.escape(PM.STATUS_DEF[k], quote=False)}</li>'
        for k in ("live", "cand", "note", "rej", "ret"))


# ── 頁數與日期：看實際檔案，不手寫 ─────────────────────────────────────────
def _is_stub(text: str) -> bool:
    return 'http-equiv="refresh"' in text[:1500] and len(text) < 4000


def page_stats() -> dict:
    """docs/backtest 底下實際內容頁數（跳轉頁不算），並拆出三個子專區。"""
    total = 0
    sub = {"housing_gdp": 0, "vendor": 0, "country_scan": 0}
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(("_", "__")) for part in rel.parts) or "data" in rel.parts:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if _is_stub(text):
            continue
        total += 1
        if rel.parts[0] in sub:
            sub[rel.parts[0]] += 1
    return {"total": total, **sub}


def _sections_for_check():
    """_build_index._completeness_check 讀的結構：[(label, [item…])]，item[0] 是網址。"""
    rows = [(PM.ZONES[z][0], [(u,) for u in PM.ZONE_ORDER[z]]) for z in PM.ZONES]
    rows.append(("已併入他頁（原網址跳轉）", [(u,) for u in PM.FOLDED]))
    rows.append(("主頁章節的完整版", [(u,) for u in PM.MEMBERS]))
    return [dict(rows=rows)]


SECTIONS = _sections_for_check()


def render() -> str:
    st = page_stats()
    html = TEMPLATE
    foot = (f"共 {st['total']} 頁（含房價與所得 {st['housing_gdp']} 頁、各國股市結構 {st['country_scan']} 頁、"
            f"外部策略檢驗 {st['vendor']} 頁）")
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%JUMP%": jump_html(),
        "%LEGEND%": legend_html(),
        "%ZONES%": zones_html(),
        "%PAGE_FOOT%": foot,
        "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>量化回測：依問題找頁面 | InvestMQuest Research</title>
<link rel="stylesheet" href="/assets/imq-base.css">
<style>
:root{--red-bg:#fbeceb;--accent-bg:#eef1f6}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--paper);color:var(--body);line-height:1.6;font-size:15px}
a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1100px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.5rem 0 1rem;background:var(--card);border-bottom:1px solid var(--line)}
.page-hdr h1{font-family:var(--serif);font-size:1.6rem;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.page-hdr .sub{color:var(--sec);font-size:.88rem;margin-top:.3rem;max-width:70ch;line-height:1.7}
.crumb{font-size:.8rem;color:var(--sec);margin-bottom:.35rem}.crumb a{color:var(--sec)}
.ov-jump{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1rem}
.ov-jump a{padding:.28rem .75rem;background:var(--line-soft);border-radius:999px;font-size:.8rem;font-weight:500;color:var(--body)}
.ov-jump a:hover{background:var(--line);text-decoration:none}
.ov-legend{list-style:none;display:flex;flex-wrap:wrap;gap:.35rem 1.2rem;margin-top:.9rem;font-size:.78rem;color:var(--sec)}
.ov-legend li{display:flex;align-items:center;gap:.4rem;min-width:0}
.ov-zone{margin-top:2.2rem}
.ov-zone-hd{font-family:var(--serif);font-size:1.3rem;font-weight:700;color:var(--ink);padding-top:1rem;border-top:2px solid var(--ink);display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap}
.ov-zone-n{font-family:var(--sans);font-size:.76rem;font-weight:500;color:var(--sec)}
.ov-zone-intro{font-size:.86rem;color:var(--sec);margin:.35rem 0 .8rem;max-width:70ch}
.ov-list{list-style:none;border:1px solid var(--line);border-radius:8px;background:var(--card);overflow:hidden}
.ov-entry{display:flex;gap:.7rem;align-items:flex-start;padding:.6rem .85rem;border-top:1px solid var(--line)}
.ov-entry:first-child{border-top:0}
.ov-main{min-width:0;flex:1}
.ov-title{font-weight:600;font-size:.92rem;color:var(--ink);overflow-wrap:anywhere}
a.ov-title:hover{text-decoration:underline}
.ov-desc{font-size:.8rem;color:var(--sec);margin-top:.15rem;line-height:1.55;overflow-wrap:anywhere}
.ov-extra{font-size:.8rem;margin-top:.25rem}.ov-extra a{font-weight:600}
.ov-st{flex:0 0 auto;display:inline-block;font-size:.7rem;font-weight:700;padding:.08rem .5rem;border-radius:999px;line-height:1.55;border:1px solid transparent;margin-top:.12rem;white-space:nowrap}
.ov-legend .ov-st{margin-top:0}
.ov-st-live{background:#fbf3df;color:#7a5a1a;border-color:#e6cf98}
.ov-st-cand{background:#e8f0fb;color:#1d4ea0;border-color:#b9cdee}
.ov-st-note{background:#eef1f4;color:#4b5563;border-color:#d7dce2}
.ov-st-rej{background:#fbeceb;color:#b42318;border-color:#f0c4c0}
.ov-st-ret{background:#f1f1f1;color:#6b7280;border-color:#d4d4d4}
.ov-dead{margin-top:.6rem}
.ov-dead>summary{cursor:pointer;font-size:.84rem;font-weight:600;color:var(--sec);padding:.45rem .2rem}
.ov-dead>summary:hover{color:var(--ink)}
.ov-dead .ov-list{margin-top:.2rem}
.ov-dead .ov-title{color:var(--body);font-weight:500}
footer{background:var(--card);border-top:1px solid var(--line);color:var(--sec);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2.2rem}
@media(max-width:640px){
  .container{padding:0 1rem}
  .ov-entry{flex-direction:column;gap:.3rem}
}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>量化回測：依你想回答的問題找頁面</h1>
  <div class="sub">分成七個問題，每頁標有狀態。已否決和已退役的頁收在各區底部，點開才會展開。</div>
  <div class="ov-jump">%JUMP%</div>
  <ul class="ov-legend">%LEGEND%</ul>
</div></div>

<div class="container">

%ZONES%

</div>
<footer><div class="container">
  &copy; 2026 InvestMQuest Research · 量化回測 · %PAGE_FOOT% ·
  <a href="/backtest/glossary/">術語對照表</a> · 生成 %NOW%
</div></footer>
</body></html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
