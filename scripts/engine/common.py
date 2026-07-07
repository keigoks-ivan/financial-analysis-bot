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
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans TC",sans-serif;
     background:#f7f8fa;color:#1a2332;font-size:14px;line-height:1.65}
.wrap{max-width:1080px;margin:0 auto;padding:24px 20px 60px}
.hero h1{font-size:24px;font-weight:800;color:#0f2a45;margin:14px 0 6px}
.hero-sub{color:#475569;font-size:13.5px;max-width:860px}
.asof{font-size:12px;color:#94a3b8;margin-top:6px}
.block{background:#fff;border:1px solid #e2e8f0;border-radius:12px;
       padding:18px 20px;margin-top:18px}
.block h2{font-size:17px;font-weight:750;color:#0f2a45;margin-bottom:6px}
.block-sub{color:#64748b;font-size:12.5px;margin-bottom:10px}
.stat-row{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0}
.stat{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
      padding:10px 14px;min-width:110px}
.stat strong{display:block;font-size:20px;color:#0f2a45}
.stat span{font-size:11.5px;color:#64748b}
table{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
th{font-size:11.5px;color:#64748b;text-align:right;padding:6px 8px;
   border-bottom:2px solid #e2e8f0;white-space:nowrap}
td{padding:6px 8px;text-align:right;border-bottom:1px solid #f1f5f9;white-space:nowrap}
th.left,td.left{text-align:left}
td a{color:#1d4ed8;text-decoration:none;font-weight:650}
td a:hover{text-decoration:underline}
.pos{color:#166534;font-weight:650}.neg{color:#b91c1c;font-weight:650}
.muted{color:#94a3b8}
.tag{display:inline-block;font-size:11px;font-weight:700;border-radius:5px;padding:1px 7px}
.tag-pool{background:#dcfce7;color:#166534}
.tag-blind{background:#fef3c7;color:#92400e}
.tag-up{background:#dcfce7;color:#166534}
.tag-dn{background:#fee2e2;color:#991b1b}
.shape-card{border-left:4px solid #2563eb;margin-top:14px;background:#fbfdff;
            border-top:1px solid #dce8f5;border-right:1px solid #dce8f5;
            border-bottom:1px solid #dce8f5;border-radius:10px;padding:14px 16px}
.shape-card h3{font-size:15px;font-weight:700;color:#0f2a45;margin-bottom:4px}
.shape-card h3 .cnt{font-size:11px;font-weight:600;color:#94a3b8;margin-left:6px}
.shape-desc{font-size:12px;color:#64748b;margin-bottom:6px}
.s-breakout{border-left-color:#166534}
.s-cyclical{border-left-color:#c2410c}
.s-momentum{border-left-color:#7c3aed}
.s-theme{border-left-color:#0e7490}
.empty{color:#94a3b8;padding:14px 0;text-align:center}
.note{font-size:12px;color:#64748b;background:#f8fafc;border:1px solid #e2e8f0;
      border-radius:8px;padding:10px 12px;margin-top:10px}
.warn{background:#fffbeb;border-color:#fde68a;color:#92400e}
.layers{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-top:12px}
.layer{background:#fbfdff;border:1px solid #dce8f5;border-radius:10px;padding:12px 14px}
.layer .lno{font-size:11px;font-weight:800;color:#2563eb}
.layer h3{font-size:14.5px;font-weight:750;color:#0f2a45;margin:2px 0 4px}
.layer p{font-size:12px;color:#64748b}
.layer .status{display:inline-block;margin-top:6px;font-size:11px;font-weight:700;
               border-radius:5px;padding:1px 7px}
.st-live{background:#dcfce7;color:#166534}
.st-soon{background:#f1f5f9;color:#64748b}
.imq-foot{margin-top:26px;padding:14px 0;border-top:1px solid #e2e8f0;
          color:#94a3b8;font-size:12px;text-align:center;line-height:1.8}
.imq-foot a{color:#1d4ed8;text-decoration:none}
.imq-foot a:hover{text-decoration:underline}
.overview-wrap{overflow-x:auto;margin:16px 0 4px;border:1px solid #e2e8f0;
               border-radius:12px;background:#fff}
.overview-tbl{font-size:12.5px;margin-top:0}
.overview-tbl th{padding:8px 10px}
.overview-tbl td{padding:7px 10px}
.overview-tbl a.tk-link{color:#0f2a45;font-weight:750;text-decoration:none}
.overview-tbl a.tk-link:hover{text-decoration:underline;color:#1d4ed8}
.gate-mini{white-space:nowrap;font-size:11px}
.gate-mini b{font-weight:700;color:#94a3b8;margin:0 1px 0 6px}
.gate-mini b:first-child{margin-left:0}
.seat-section{font-size:16px;font-weight:800;color:#0f2a45;margin:24px 0 2px}
.seat-section .cnt{font-size:12px;font-weight:600;color:#94a3b8;margin-left:6px}
details.card-block{background:#fff;border:1px solid #e2e8f0;border-radius:12px;
                    margin-top:10px}
details.card-block>summary{list-style:none;cursor:pointer;padding:12px 16px;
                            display:flex;align-items:center;gap:8px;flex-wrap:wrap}
details.card-block>summary::-webkit-details-marker{display:none}
details.card-block>summary::before{content:"▸";color:#94a3b8;font-size:12px}
details.card-block[open]>summary::before{content:"▾"}
details.card-block>summary:hover{background:#f8fafc;border-radius:10px}
.card-summary .cs-ticker{font-size:15.5px;font-weight:800;color:#0f2a45}
.card-summary .cs-verdict{font-size:12.5px;font-weight:650;color:#64748b}
.card-body{padding:0 20px 18px}
details.bench-wrap{margin-top:22px;border:1px dashed #cbd5e1;border-radius:12px;
                    background:#fbfdff;padding:2px 6px 8px}
details.bench-wrap>summary{list-style:none;cursor:pointer;padding:12px 14px;
                            font-size:16px;font-weight:800;color:#0f2a45}
details.bench-wrap>summary::-webkit-details-marker{display:none}
details.bench-wrap>summary::before{content:"▸ ";color:#94a3b8}
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


def pct(v, digits=1, signed=True):
    if v is None:
        return '<span class="muted">—</span>'
    cls = "pos" if v > 0 else ("neg" if v < 0 else "")
    sign = "+" if (signed and v > 0) else ""
    return f'<span class="{cls}">{sign}{v:.{digits}f}%</span>'
