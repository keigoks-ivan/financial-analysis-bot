#!/usr/bin/env python3
"""決策引擎頁面共用：canonical nav + 統一頁殼 CSS。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from site_nav import ENGINE_SUBNAV, build_subnav, full_nav_block  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = ROOT / "docs" / "engine"

PAGE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--sans),-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans TC",sans-serif;
     background:var(--paper);color:var(--body);font-size:14px;line-height:1.65}
.wrap{max-width:1080px;margin:0 auto;padding:24px 20px 60px}
.hero h1{font-family:var(--serif);font-size:24px;font-weight:700;color:var(--ink);margin:14px 0 6px}
.hero-sub{color:var(--sec);font-size:13.5px;max-width:860px}
.asof{font-size:12px;color:var(--muted);margin-top:6px}
.block{background:var(--card);border:1px solid var(--line);border-radius:var(--r);
       box-shadow:var(--sh-1);padding:18px 20px;margin-top:18px}
.block h2{font-family:var(--serif);font-size:17px;font-weight:700;color:var(--ink);margin-bottom:6px}
.block-sub{color:var(--sec);font-size:12.5px;margin-bottom:10px}
.stat-row{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:6px;
      padding:10px 14px;min-width:110px}
.stat strong{display:block;font-family:var(--mono);font-size:20px;color:var(--ink)}
.stat span{font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
th{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
   color:var(--sec);text-align:right;padding:6px 8px;
   border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:6px 8px;text-align:right;border-bottom:1px solid var(--line-soft);white-space:nowrap;
   font-family:var(--mono);font-variant-numeric:tabular-nums}
th.left,td.left{text-align:left;font-family:inherit;font-variant-numeric:normal}
tr:hover td{background:#fbf8f1}
td a{color:var(--accent);text-decoration:none;font-weight:650}
td a:hover{text-decoration:underline}
.pos{color:var(--pos);font-weight:650}.neg{color:var(--neg);font-weight:650}
.muted{color:var(--muted)}
.tag{display:inline-block;font-family:var(--mono);font-size:11px;font-weight:600;
     letter-spacing:.02em;border-radius:5px;padding:1px 7px}
.tag-pool{background:#eafaef;color:var(--pos)}
.tag-blind{background:#fbf3df;color:var(--warn)}
.tag-up{background:#eafaef;color:var(--pos)}
.tag-dn{background:#fbeceb;color:var(--neg)}
.shape-card{border-left:3px solid var(--accent);margin-top:14px;background:var(--card);
            border-top:1px solid var(--line);border-right:1px solid var(--line);
            border-bottom:1px solid var(--line);border-radius:var(--r);padding:14px 16px}
.shape-card h3{font-family:var(--serif);font-size:15px;font-weight:700;color:var(--ink);margin-bottom:4px}
.shape-card h3 .cnt{font-size:11px;font-weight:600;color:var(--muted);margin-left:6px}
.shape-desc{font-size:12px;color:var(--sec);margin-bottom:6px}
.s-breakout{border-left-color:var(--accent)}
.s-cyclical{border-left-color:var(--accent)}
.s-momentum{border-left-color:var(--accent)}
.s-theme{border-left-color:var(--accent)}
.empty{color:var(--muted);padding:14px 0;text-align:center}
.note{font-size:12px;color:var(--sec);background:var(--paper);border:1px solid var(--line);
      border-radius:6px;padding:10px 12px;margin-top:10px}
.warn{background:#fbf3df;border-color:var(--warn);color:var(--warn)}
.layers{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-top:12px}
.layer{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:12px 14px}
.layer .lno{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--accent)}
.layer h3{font-family:var(--serif);font-size:14.5px;font-weight:700;color:var(--ink);margin:2px 0 4px}
.layer p{font-size:12px;color:var(--sec)}
.layer .status{display:inline-block;margin-top:6px;font-family:var(--mono);font-size:11px;font-weight:600;
               border-radius:5px;padding:1px 7px}
.st-live{background:#eafaef;color:var(--pos)}
.st-soon{background:var(--line-soft);color:var(--sec)}
.imq-foot{margin-top:26px;padding:14px 0;border-top:1px solid var(--line);
          color:var(--sec);font-size:12px;text-align:center;line-height:1.8}
.imq-foot a{color:var(--accent);text-decoration:none}
.imq-foot a:hover{text-decoration:underline}
.overview-wrap{overflow-x:auto;margin:16px 0 4px;border:1px solid var(--line);
               border-radius:var(--r);background:var(--card)}
.overview-tbl{font-size:12.5px;margin-top:0}
.overview-tbl th{padding:8px 10px}
.overview-tbl td{padding:7px 10px}
.overview-tbl a.tk-link{color:var(--ink);font-weight:700;text-decoration:none;font-family:inherit}
.overview-tbl a.tk-link:hover{text-decoration:underline;color:var(--accent)}
.gate-mini{white-space:nowrap;font-size:11px}
.gate-mini b{font-weight:700;color:var(--muted);margin:0 1px 0 6px}
.gate-mini b:first-child{margin-left:0}
.seat-section{font-family:var(--serif);font-size:16px;font-weight:700;color:var(--ink);margin:24px 0 2px}
.seat-section .cnt{font-size:12px;font-weight:600;color:var(--muted);margin-left:6px}
details.card-block{background:var(--card);border:1px solid var(--line);border-radius:var(--r);
                    box-shadow:var(--sh-1);margin-top:10px}
details.card-block>summary{list-style:none;cursor:pointer;padding:12px 16px;
                            display:flex;align-items:center;gap:8px;flex-wrap:wrap}
details.card-block>summary::-webkit-details-marker{display:none}
details.card-block>summary::before{content:"▸";color:var(--muted);font-size:12px}
details.card-block[open]>summary::before{content:"▾"}
details.card-block>summary:hover{background:var(--paper);border-radius:var(--r)}
.card-summary .cs-ticker{font-family:var(--mono);font-size:15.5px;font-weight:700;color:var(--ink)}
.card-summary .cs-verdict{font-size:12.5px;font-weight:650;color:var(--sec)}
.card-body{padding:0 20px 18px}
details.bench-wrap{margin-top:22px;border:1px dashed var(--muted);border-radius:var(--r);
                    background:var(--card);padding:2px 6px 8px}
details.bench-wrap>summary{list-style:none;cursor:pointer;padding:12px 14px;
                            font-family:var(--serif);font-size:16px;font-weight:700;color:var(--ink)}
details.bench-wrap>summary::-webkit-details-marker{display:none}
details.bench-wrap>summary::before{content:"▸ ";color:var(--muted)}
details.bench-wrap[open]>summary::before{content:"▾ "}
details.bench-wrap details.card-block{margin:8px 6px 0}
@media(max-width:760px){.wrap{padding:16px 10px 40px}.block{padding:14px 12px}
  table{display:block;overflow-x:auto}
  details.card-block>summary{padding:10px 12px}.card-body{padding:0 12px 14px}}
"""


def page_shell(title: str, current: str, body: str, desc: str = "") -> str:
    nav = full_nav_block("pick", "eng", build_subnav(ENGINE_SUBNAV, current))
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | InvestMQuest Research</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="/assets/imq-base.css">
<style>{PAGE_CSS}</style>
</head>
<body>
{nav}
<div class="wrap">
{body}
<footer class="imq-foot">
  <div>© 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</div>
</body>
</html>"""


def page_embed_shell(title: str, body: str, desc: str = "") -> str:
    """Nav-less fragment for embedding inside the 選股主控台 console iframe.

    No site nav / no subnav (那些屬 console 外殼)；`<base target="_parent">` 讓內部
    跨頁連結（DD／engine 深頁）在頂層視窗開啟而非 iframe 內。noindex——正式入口是
    /cockpit/#seats，本片段不獨立索引。"""
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title} | InvestMQuest Research</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="/assets/imq-base.css">
<style>{PAGE_CSS}
body{{background:transparent}}.wrap{{padding-top:8px}}</style>
</head>
<body>
<div class="wrap">
{body}
</div>
<!-- 主控台 iframe 嵌入：跨頁連結在頂層開啟，站內 #錨點留在 iframe 內滾動 -->
<script>(function(){{function fix(){{var as=document.querySelectorAll('a[href]');for(var i=0;i<as.length;i++){{var a=as[i],h=a.getAttribute('href');if(h&&h.charAt(0)!=='#'&&!a.hasAttribute('target'))a.setAttribute('target','_parent');}}}}if(document.readyState!=='loading')fix();else document.addEventListener('DOMContentLoaded',fix);window.addEventListener('load',fix);[400,1200,2500].forEach(function(t){{setTimeout(fix,t);}});}})();</script>
</body>
</html>"""


def pct(v, digits=1, signed=True):
    if v is None:
        return '<span class="muted">—</span>'
    cls = "pos" if v > 0 else ("neg" if v < 0 else "")
    sign = "+" if (signed and v > 0) else ""
    return f'<span class="{cls}">{sign}{v:.{digits}f}%</span>'
