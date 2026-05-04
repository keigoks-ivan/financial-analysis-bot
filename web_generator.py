"""
web_generator.py — 靜態網站生成器

生成供 GitHub Pages 托管的 HTML 頁面：
  docs/index.html              — 首頁（報告總表 + 搜尋）
  docs/report/{page_id}.html   — 10-K / 10-Q 個別報告頁面
  docs/company/{TICKER}.html   — 個別公司頁面（歷史報告 + 護城河趨勢）
  docs/industry/{name}.html    — 產業比較頁面（護城河橫向比較）

網址：https://research.investmquest.com
"""

from __future__ import annotations

import os
import re
import json
import datetime
import html as html_lib
import requests
import markdown as md_lib
from pathlib import Path

# ── 路徑常數 ─────────────────────────────────────────────────────────────────
DOCS_DIR = Path("docs")
KB_DIR = Path("knowledge_base")
BASE_URL = "https://research.investmquest.com"

# ── Notion 設定 ──────────────────────────────────────────────────────────────
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_10Q_DB_ID = os.environ.get("NOTION_10Q_DB_ID")
NOTION_10K_DB_ID = os.environ.get("NOTION_10K_DB_ID")

DISCLAIMER = """
<strong>免責聲明：</strong>
本網站所有內容（包含財報摘要、護城河評分及產業分析）均由 AI 自動生成，
僅供參考，<strong>不構成任何投資建議</strong>。
投資涉及風險，投資人應自行判斷並諮詢專業顧問。
過往表現不代表未來業績。本網站與任何被分析公司均無利益關係。
"""

# ── 護城河五維度標籤 ─────────────────────────────────────────────────────────
MOAT_5_DIMS = {
    "brand_power": "品牌力",
    "switching_costs": "轉換成本",
    "network_effects": "網絡效應",
    "cost_advantage": "成本優勢",
    "regulatory_moat": "監管護城河",
}

# ── 巴菲特蒙格八維度 ────────────────────────────────────────────────────────
DIM_8 = [
    ("業務可理解性", "Understandability"),
    ("歷史經營一致性", "Track Record"),
    ("長期競爭優勢", "Economic Moat"),
    ("管理層品質", "Management Quality"),
    ("財務強健度", "Financial Strength"),
    ("自由現金流品質", "Owner Earnings"),
    ("成長空間", "Growth Runway"),
    ("產業結構與競爭動態", "Industry Dynamics"),
]

CN_NUMS = "一二三四五六七八"

# ── 共用 CSS ─────────────────────────────────────────────────────────────────
SHARED_CSS = """
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;
      --text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
     background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem}

/* Header */
header{background:#fff;border-bottom:1px solid var(--border);padding:.7rem 0}
.hdr-inner{display:flex;align-items:center;justify-content:space-between}
header .logo{font-size:1.1rem;font-weight:700;color:var(--text);letter-spacing:-.02em}
header nav a{color:var(--muted);margin-left:1.4rem;font-size:.85rem;font-weight:500}
header nav a:hover,header nav a.active{color:var(--brand)}

/* Page Header */
.page-hdr{padding:1.75rem 0 1.25rem;background:#fff;border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.6rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.9rem;margin-top:.2rem}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}
.crumb a{color:var(--muted)}

/* Card */
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem}
.card h3{font-size:1rem;font-weight:600;margin-bottom:.85rem;color:var(--text)}

/* Tags */
.tag{display:inline-block;padding:.15rem .55rem;border-radius:4px;
     font-size:.72rem;font-weight:600;letter-spacing:.02em}
.tag-10q{background:#dbeafe;color:#1e40af}
.tag-10k{background:#f3e8ff;color:#6b21a8}
.tag-dd{background:#1e3a5f;color:#fff}

/* Moat Badges */
.moat-badge{display:inline-block;padding:.2rem .7rem;border-radius:20px;
            font-size:.78rem;font-weight:600}
.moat-wide{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.moat-narrow{background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)}
.moat-none{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}

/* Table */
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{text-align:left;padding:.65rem .8rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.78rem;text-transform:uppercase;
   letter-spacing:.04em;color:var(--muted)}
tbody tr:hover td{background:#f3f4f6}

/* Search */
.search-wrap{margin:1.25rem 0}
.search-wrap input{width:100%;max-width:380px;padding:.55rem 1rem;
                   border:1px solid var(--border);border-radius:6px;font-size:.88rem;
                   background:var(--card)}
.search-wrap input:focus{outline:none;border-color:var(--brand);
                         box-shadow:0 0 0 3px rgba(26,86,219,.1)}

/* Filter Bar */
.filter-bar{display:flex;flex-wrap:wrap;gap:.75rem;margin-bottom:1rem;align-items:center}
.filter-group{display:flex;align-items:center;gap:.35rem;flex-wrap:wrap}
.filter-label{font-size:.78rem;font-weight:600;color:var(--muted);margin-right:.2rem;
              text-transform:uppercase;letter-spacing:.03em}
.filter-btn{padding:.3rem .7rem;border:1px solid var(--border);border-radius:5px;
            background:var(--card);font-size:.8rem;color:var(--text);cursor:pointer;
            transition:all .15s}
.filter-btn:hover{border-color:var(--brand);color:var(--brand)}
.filter-btn.active{background:var(--brand);color:#fff;border-color:var(--brand)}

/* Score Hero (10-K gauge area) */
.score-hero{display:flex;align-items:center;gap:2.5rem;padding:1.5rem 0}
.gauge-wrap{text-align:center;flex-shrink:0}
.gauge-meta{display:flex;flex-direction:column;gap:.6rem}
.gauge-meta .moat-badge{align-self:flex-start}

/* Dimension Cards */
.dim-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.85rem;margin:1.25rem 0}
.dim-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.1rem 1.2rem}
.dim-hdr{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.35rem}
.dim-name{font-weight:600;font-size:.9rem}
.dim-en{font-size:.72rem;color:var(--muted);font-weight:400;margin-left:.3rem}
.dim-score{font-weight:700;font-size:1.05rem;white-space:nowrap}
.dim-bar{height:5px;background:var(--border);border-radius:3px;overflow:hidden;margin:.6rem 0}
.dim-bar .fill{height:100%;border-radius:3px}
.dim-text{font-size:.82rem;color:#4b5563;line-height:1.55}
.dim-text h3{font-size:.88rem;font-weight:600;color:var(--text);margin:.6rem 0 .25rem}
.dim-text p{margin-bottom:.4rem}.dim-text strong{color:var(--text)}
.dim-text ul,.dim-text ol{margin:0 0 .4rem 1.1rem}

/* Thesis */
.thesis{background:var(--brand-light);border-left:4px solid var(--brand);
        padding:1.1rem 1.4rem;border-radius:0 8px 8px 0;margin:1.25rem 0}
.thesis p{font-size:1.1rem;font-weight:600;color:var(--text);line-height:1.55}

/* Summary Hero (10-Q) */
.summary-hero{text-align:center;padding:1.75rem 1.5rem;background:var(--card);
              border:1px solid var(--border);border-radius:8px;margin:1.25rem 0}
.summary-hero p{font-size:1.25rem;font-weight:600;color:var(--text)}

/* Risks */
.risk-box{background:var(--red-bg);border:1px solid var(--red-border);border-radius:8px;
          padding:.85rem 1.1rem;margin-bottom:.6rem;font-size:.88rem;color:var(--red-text)}
.risk-num{font-weight:700;margin-right:.4rem}

/* Moat Signals */
.signal{display:inline-block;padding:.25rem .65rem;border-radius:4px;
        font-size:.78rem;margin:.2rem .2rem .2rem 0;line-height:1.4}
.signal-pos{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.signal-neg{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}
.signal-neu{background:#f3f4f6;color:#374151;border:1px solid #d1d5db}

/* Guidance Box (10-Q) */
.guidance-box{background:var(--brand-light);border:1px solid #93c5fd;border-radius:8px;
              padding:1rem 1.25rem;margin-bottom:1.25rem}
.guidance-box h4{color:var(--brand);font-size:.9rem;font-weight:600;margin-bottom:.4rem}
.guidance-box .gd-text{font-size:.85rem;line-height:1.6;color:#1e40af}

/* Capital Cards (10-Q) */
.cap-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.85rem}
.cap-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem 1.1rem}
.cap-card .cap-icon{font-size:1.2rem;margin-bottom:.25rem}
.cap-card .cap-label{font-size:.76rem;color:var(--muted);text-transform:uppercase;
                     letter-spacing:.03em;margin-bottom:.25rem}
.cap-card .cap-amount{font-size:1.05rem;font-weight:700;color:var(--text)}
.cap-card .cap-detail{font-size:.78rem;color:var(--muted);margin-top:.25rem;line-height:1.45}

/* Change Arrows (10-Q table) */
.chg-up{color:var(--green);font-weight:600}
.chg-down{color:var(--red);font-weight:600}
.chg-flat{color:var(--muted);font-weight:600}

/* 10-Q Consistency Badges */
.consistency-badge{display:inline-flex;align-items:center;gap:.3rem;padding:.35rem .75rem;
  border-radius:6px;font-size:.82rem;font-weight:600;margin:.25rem .3rem .25rem 0}
.consistency-pass{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.consistency-fail{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}

/* 10-Q Footnote List */
.footnote-list{list-style:none;padding:0;margin:0}
.footnote-list li{padding:.55rem .75rem;border-bottom:1px solid var(--border);font-size:.85rem;
  line-height:1.65;color:#374151}
.footnote-list li:last-child{border-bottom:none}
.footnote-list li::before{content:'\1F4CC';margin-right:.5rem}

/* 10-Q Management Card */
.mgmt-card{background:linear-gradient(135deg,#eff6ff,#fff);border:1px solid #93c5fd}

/* Moat Bar */
.moat-bar{height:7px;border-radius:4px;background:var(--border);overflow:hidden}
.moat-fill{height:100%;border-radius:4px}

/* Radar + Risks layout */
.radar-risks{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin:1.25rem 0}

/* Section */
.section{padding:1.75rem 0}
.section-title{font-size:1.1rem;font-weight:700;margin-bottom:.85rem;
               padding-bottom:.4rem;border-bottom:2px solid var(--brand)}

/* Content */
.analysis{font-size:.88rem;line-height:1.75;color:#374151}
.analysis h1,.analysis h2,.analysis h3{color:var(--text);margin:1rem 0 .4rem;line-height:1.3}
.analysis h1{font-size:1.15rem}.analysis h2{font-size:1.05rem}.analysis h3{font-size:.95rem}
.analysis p{margin-bottom:.6rem}.analysis ul,.analysis ol{margin:0 0 .6rem 1.2rem}
.analysis strong{color:var(--text)}

/* Financials Card */
.fin-section{margin-bottom:1.25rem}
.fin-section h4{font-size:.9rem;font-weight:600;margin-bottom:.5rem;color:var(--text);
                padding-bottom:.3rem;border-bottom:1px solid var(--border)}
.fin-content{font-size:.85rem;line-height:1.7;color:#374151;white-space:pre-line}

/* Disclaimer & Footer */
.disclaimer{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;
            padding:.85rem 1.1rem;font-size:.76rem;color:#78350f;margin:1.75rem 0}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem}
footer a{color:var(--muted)}

/* Score colors */
.sc-hi{color:var(--green)}.sc-mid{color:var(--amber)}.sc-lo{color:var(--red)}

/* Responsive */
@media(max-width:768px){
  .dim-grid{grid-template-columns:1fr}
  .score-hero{flex-direction:column;text-align:center}
  .gauge-meta{align-items:center}
  .gauge-meta .moat-badge{align-self:center}
  .radar-risks{grid-template-columns:1fr}
  .hdr-inner{flex-direction:column;gap:.5rem}
  header nav a{margin-left:0;margin-right:1rem}
  .cap-grid{grid-template-columns:1fr}
}
"""


# ── 輔助函式：分數 / 護城河等級 ──────────────────────────────────────────────

def _score_cls(score: float) -> str:
    if score >= 7:
        return "sc-hi"
    if score >= 5:
        return "sc-mid"
    return "sc-lo"


def _score_color(score: float, scale: float = 10.0) -> str:
    pct = score / scale if scale else 0
    if pct >= 0.7:
        return "var(--green)"
    if pct >= 0.5:
        return "var(--amber)"
    return "var(--red)"


def _moat_level(avg: float) -> str:
    if avg >= 7:
        return "Wide"
    if avg >= 5:
        return "Narrow"
    return "No Moat"


def _moat_level_cn(avg: float) -> str:
    if avg >= 7:
        return "寬護城河 Wide Moat"
    if avg >= 5:
        return "窄護城河 Narrow Moat"
    return "無護城河 No Moat"


def _moat_badge_cls(level: str) -> str:
    return {"Wide": "moat-wide", "Narrow": "moat-narrow"}.get(level, "moat-none")


def _fill_pct(score: float, max_score: float = 10.0) -> int:
    return min(100, int(score / max_score * 100))


# ── 儀表板顏色 ───────────────────────────────────────────────────────────────

def _gauge_color_hex(score: float, max_score: float = 80.0) -> str:
    """回傳儀表板主色（十六進位），依分數百分比決定。"""
    pct = score / max_score if max_score > 0 else 0
    if pct >= 0.7:
        return "#059669"
    if pct >= 0.5:
        return "#d97706"
    return "#dc2626"


# ── HTML 骨架 ────────────────────────────────────────────────────────────────

def _header(active: str = "") -> str:
    links = [
        ("首頁", "/"),
        ("每日簡報", "/briefing/"),
        ("週報", "/weekly/"),
        ("回測", "/backtest/"),
        ("研究報告", "/research/"),
        ("QGM 美股", "/qgm/"),
        ("QGM 台股", "/qgm-tw/"),
        ("六狀態機", "/six-state/"),
    ]
    nav = " ".join(
        f'<a href="{url}" class="{"active" if active == lbl else ""}">{lbl}</a>'
        for lbl, url in links
    )
    return f"""<header>
  <div class="container hdr-inner">
    <a class="logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav>{nav}</nav>
  </div>
</header>"""


def _footer() -> str:
    year = datetime.date.today().year
    return f"""<div class="container"><div class="disclaimer">{DISCLAIMER}</div></div>
<footer>
  <div class="container">
    &copy; {year} InvestMQuest Research &middot;
    由 AI 自動生成，僅供參考
  </div>
</footer>"""


def _base_page(title: str, body: str, extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html_lib.escape(title)} | InvestMQuest Research</title>
  <meta name="description" content="AI 驅動財報分析平台，提供 10-Q / 10-K 深度解讀">
  <meta property="og:title" content="{html_lib.escape(title)}">
  <meta property="og:site_name" content="InvestMQuest Research">
  <style>{SHARED_CSS}</style>
  {extra_head}
</head>
<body>
{_header()}
{body}
{_footer()}
<script>
(function(){{
  // DD table search
  var ddSearch=document.getElementById('dd-search');
  var ddCount=document.getElementById('dd-count');
  var ddRows=document.querySelectorAll('#dd-tbody tr.searchable');
  function renderDdCount(s,t){{ if(ddCount) ddCount.textContent='\u5171 '+t+' \u7B46'+(s!==t?'\uFF08\u986F\u793A '+s+'\uFF09':''); }}
  function filterDd(){{
    var q=(ddSearch&&ddSearch.value||'').toLowerCase();
    var shown=0;
    ddRows.forEach(function(r){{
      var m=!q||r.textContent.toLowerCase().indexOf(q)>=0;
      r.style.display=m?'':'none';
      if(m) shown++;
    }});
    renderDdCount(shown,ddRows.length);
  }}
  if(ddSearch) ddSearch.addEventListener('input',filterDd);
  if(ddRows.length) renderDdCount(ddRows.length,ddRows.length);

  // Earnings table search + filter
  var erSearch=document.getElementById('earnings-search');
  var erCount=document.getElementById('earnings-count');
  var erRows=document.querySelectorAll('#report-tbody tr.searchable');
  var filters={{form:'all',moat:'all'}};
  function renderErCount(s,t){{ if(erCount) erCount.textContent='\u5171 '+t+' \u7B46'+(s!==t?'\uFF08\u986F\u793A '+s+'\uFF09':''); }}
  function filterEr(){{
    var q=(erSearch&&erSearch.value||'').toLowerCase();
    var shown=0;
    erRows.forEach(function(el){{
      var matchText=!q||el.textContent.toLowerCase().indexOf(q)>=0;
      var matchForm=filters.form==='all'||el.getAttribute('data-form')===filters.form;
      var matchMoat=filters.moat==='all'||el.getAttribute('data-moat')===filters.moat;
      var vis=matchText&&matchForm&&matchMoat;
      el.style.display=vis?'':'none';
      if(vis) shown++;
    }});
    renderErCount(shown,erRows.length);
  }}
  if(erSearch) erSearch.addEventListener('input',filterEr);
  document.querySelectorAll('.filter-btn').forEach(function(btn){{
    btn.addEventListener('click',function(){{
      var group=btn.getAttribute('data-filter');
      var val=btn.getAttribute('data-value');
      filters[group]=val;
      btn.parentElement.querySelectorAll('.filter-btn').forEach(function(b){{
        b.classList.remove('active');
      }});
      btn.classList.add('active');
      filterEr();
    }});
  }});
  if(erRows.length) renderErCount(erRows.length,erRows.length);
}})();
</script>
</body>
</html>"""


# ── Markdown → HTML 轉換 ────────────────────────────────────────────────────

def _md(text: str) -> str:
    """將 Notion 分析文本中的 Markdown 語法轉為 HTML。"""
    if not text:
        return ""
    return md_lib.markdown(text, extensions=["tables"])


# ── 分析文本解析 ─────────────────────────────────────────────────────────────

def _parse_10k_analysis(text: str) -> dict:
    """
    解析 10-K 分析文本，萃取八維度評分、護城河等級、風險、核心論點。
    若解析失敗則回傳空值，頁面會降級為顯示原始文本。
    """
    result = {
        "dimensions": [],
        "total_score": None,
        "moat_level": None,
        "risks": [],
        "core_thesis": "",
    }

    # 解析八維度
    for i, (cn_name, en_name) in enumerate(DIM_8):
        cn_num = CN_NUMS[i]
        pattern = rf"維度{cn_num}[：:．.]\s*{re.escape(cn_name)}"
        match = re.search(pattern, text)
        if not match:
            result["dimensions"].append(
                {"cn": cn_name, "en": en_name, "score": None, "text": ""}
            )
            continue

        start = match.end()
        if i + 1 < 8:
            end_pat = rf"維度{CN_NUMS[i + 1]}[：:．.]"
        else:
            end_pat = r"綜合評估|---"
        end_m = re.search(end_pat, text[start:])
        end = start + end_m.start() if end_m else len(text)
        section = text[start:end].strip()

        score_m = re.search(
            r"\*?\*?評分[：:]\s*(\d+(?:\.\d+)?)\s*/\s*10\*?\*?", section
        )
        score = float(score_m.group(1)) if score_m else None

        clean = re.sub(r"\*?\*?評分[：:].*", "", section).strip()
        clean = re.sub(r"^[（(].*?[）)]\s*", "", clean)  # 移除開頭括號
        clean = clean.lstrip("#* \n")

        result["dimensions"].append(
            {"cn": cn_name, "en": en_name, "score": score, "text": clean}
        )

    # 總分（支援 /80 和 /110 兩種格式）
    total_m = re.search(r"總分[：:]\s*(\d+(?:\.\d+)?)\s*/\s*(?:80|110)", text)
    if total_m:
        result["total_score"] = float(total_m.group(1))
    else:
        scores = [d["score"] for d in result["dimensions"] if d["score"] is not None]
        if scores:
            result["total_score"] = sum(scores)

    # 護城河等級
    if re.search(r"寬護城河|Wide\s*Moat", text):
        result["moat_level"] = "Wide"
    elif re.search(r"窄護城河|Narrow\s*Moat", text):
        result["moat_level"] = "Narrow"
    elif re.search(r"無護城河|No\s*Moat", text):
        result["moat_level"] = "No Moat"

    # 三大風險
    risk_sec = re.search(
        r"(?:三個關鍵風險|關鍵風險|三大風險)(.*?)(?:一句話|核心論點|\Z)",
        text,
        re.DOTALL,
    )
    if risk_sec:
        items = re.findall(r"\d+[.、]\s*(.+?)(?:\n|$)", risk_sec.group(1))
        result["risks"] = [r.strip().strip("[]") for r in items[:3]]

    # 一句話核心論點
    thesis_m = re.search(
        r"一句話核心論點.*?\n(.+?)(?:\n\n|\n\*\*|\Z)", text, re.DOTALL
    )
    if thesis_m:
        t = thesis_m.group(1).strip()
        t = re.sub(r'[\*\"\u300c\u300d\u300e\u300f]', "", t).strip()
        result["core_thesis"] = t

    return result


def _parse_committee_summary(text: str) -> dict:
    """
    解析「## 投資委員會總結」區塊，回傳 {raw, viewpoints}。
    viewpoints: [{label, content}, ...] — 四位大師的觀點。
    """
    m = re.search(r"##\s*投資委員會總結\s*\n(.*?)(?:\n---|\n##\s|\Z)", text, re.DOTALL)
    if not m:
        return {"raw": "", "viewpoints": []}
    raw = m.group(1).strip()

    # 解析各大師觀點行
    viewpoints = []
    vp_pat = re.compile(
        r"\*{0,2}(巴菲特[/／]蒙格|Peter\s*Lynch|Hamilton\s*Helmer|Howard\s*Marks)"
        r"\s*觀點[：:]\s*\*{0,2}\s*(.*?)(?=\n\*{0,2}(?:巴菲特|Peter|Hamilton|Howard)|\Z)",
        re.DOTALL,
    )
    for vm in vp_pat.finditer(raw):
        label = vm.group(1).strip()
        content = vm.group(2).strip()
        # 清理多餘 markdown 標記
        content = re.sub(r"^\*{1,2}|\*{1,2}$", "", content).strip()
        if content:
            viewpoints.append({"label": label, "content": content})

    return {"raw": raw, "viewpoints": viewpoints}


_MASTER_NAMES = ["Peter Lynch", "Hamilton Helmer", "Howard Marks"]
_MASTER_ICONS = {"Peter Lynch": "📈", "Hamilton Helmer": "🏰", "Howard Marks": "⚖️"}

# Helmer 七種 Power
_HELMER_POWERS = [
    "規模經濟", "網絡經濟", "反向定位", "轉換成本",
    "壟斷性資源", "品牌", "流程優勢",
]


def _parse_master_frameworks(text: str) -> list[dict]:
    """
    解析「## 大師框架分析」之後的三位大師段落。
    回傳 [{name, content, score, extra}, ...]
    extra 為各大師特有的結構化資料。
    """
    sec_m = re.search(r"##\s*大師框架分析\s*\n", text)
    if not sec_m:
        return []
    body = text[sec_m.end():]
    # 截斷到下一個 ## 段落或 ---
    end_m = re.search(r"\n##\s[^#]|\n---", body)
    if end_m:
        body = body[:end_m.start()]

    results = []
    for i, name in enumerate(_MASTER_NAMES):
        pat = re.compile(rf"###?\s*{re.escape(name)}.*?\n", re.IGNORECASE)
        m = pat.search(body)
        if not m:
            continue
        start = m.end()
        # 找下一位大師或結尾
        next_m = None
        for next_name in _MASTER_NAMES[i + 1:]:
            next_pat = re.compile(rf"###?\s*{re.escape(next_name)}", re.IGNORECASE)
            next_m = next_pat.search(body[start:])
            if next_m:
                break
        end = start + next_m.start() if next_m else len(body)
        raw = body[start:end].strip()

        # 提取評分 (X/10)
        score_m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", raw)
        score = score_m.group(1) if score_m else None

        extra = {}

        # Hamilton Helmer: 解析七種 Power 強弱
        if name == "Hamilton Helmer":
            powers = []
            for pw in _HELMER_POWERS:
                pw_pat = re.compile(
                    rf"{re.escape(pw)}[：:（(]?\s*(強|中等|弱|不存在|無|✓|✗|有)",
                    re.IGNORECASE,
                )
                pw_m = pw_pat.search(raw)
                if pw_m:
                    level = pw_m.group(1).strip()
                    powers.append({"name": pw, "level": level})
                else:
                    # 嘗試從行內判斷：包含該 Power 名稱且有強/弱等關鍵字
                    for line in raw.split("\n"):
                        if pw in line:
                            if any(k in line for k in ["強", "✓", "最強", "存在", "有"]):
                                powers.append({"name": pw, "level": "強"})
                            elif any(k in line for k in ["弱", "較弱", "有限"]):
                                powers.append({"name": pw, "level": "弱"})
                            elif any(k in line for k in ["不存在", "無", "✗", "不適用"]):
                                powers.append({"name": pw, "level": "不存在"})
                            else:
                                powers.append({"name": pw, "level": "中等"})
                            break
            extra["powers"] = powers

        # Howard Marks: 解析週期位置
        if name == "Howard Marks":
            cycle_pos = None
            cycle_kw = {
                "底部": 10, "早期": 25, "中前期": 35, "中期": 50,
                "中後期": 65, "後期": 75, "晚期": 85, "頂部": 95,
            }
            for kw, pct in cycle_kw.items():
                if kw in raw:
                    cycle_pos = {"label": kw, "pct": pct}
                    break
            extra["cycle"] = cycle_pos

        results.append({
            "name": name, "content": raw, "score": score, "extra": extra,
        })
    return results


def _parse_10q_sections(text: str) -> dict:
    """
    解析 10-Q 分析文本，拆成五個段落 + 護城河信號標籤。
    """
    result = {"sections": {}, "summary": "", "signals": []}

    titles = ["數字變化", "敘事變化", "資本配置", "護城河信號", "一句話摘要"]
    for i, title in enumerate(titles):
        cn_num = CN_NUMS[i]
        pattern = rf"(?:##?\s*)?{cn_num}[、.]\s*{re.escape(title)}"
        match = re.search(pattern, text)
        if not match:
            continue

        start = match.end()
        if i + 1 < 5:
            next_title = titles[i + 1]
            next_num = CN_NUMS[i + 1]
            end_pat = rf"(?:##?\s*)?{next_num}[、.]\s*{re.escape(next_title)}"
        else:
            end_pat = r"\Z"
        end_m = re.search(end_pat, text[start:])
        end = start + end_m.start() if end_m else len(text)
        content = text[start:end].strip()
        result["sections"][i + 1] = {"title": title, "content": content}

    # 一句話摘要
    if 5 in result["sections"]:
        s = result["sections"][5]["content"].strip()
        s = re.sub(r"^[#*\s]+", "", s)
        s = re.sub(r'[\*\"\u300c\u300d]', "", s).strip()
        result["summary"] = s

    # ── 額外維度：管理層誠信驗證（二點五 / 指引 vs 實際）
    mgmt_m = re.search(
        r"(?:##?\s*)?(?:二點五|2\.5)[、.]\s*(.*?)$",
        text, re.MULTILINE,
    )
    if not mgmt_m:
        mgmt_m = re.search(r"(?:##?\s*)?指引\s*vs\.?\s*實際", text)
    if mgmt_m:
        start = mgmt_m.end()
        end_m = re.search(r"\n(?:##?\s*)?[三四五六七八][\u3001.]", text[start:])
        end = start + end_m.start() if end_m else len(text)
        result["mgmt_integrity"] = text[start:end].strip()

    # ── 額外維度：附注重點掃描（六、附注）
    note_m = re.search(r"(?:##?\s*)?六[、.]\s*附注", text)
    if note_m:
        start = note_m.end()
        end_m = re.search(r"\n(?:##?\s*)?[七八九][\u3001.]", text[start:])
        end = start + end_m.start() if end_m else len(text)
        result["footnote_scan"] = text[start:end].strip()

    # ── 額外維度：數字一致性驗證（七、數字一致性）
    consist_m = re.search(r"(?:##?\s*)?七[、.]\s*數字一致性", text)
    if consist_m:
        start = consist_m.end()
        end_m = re.search(r"\n(?:##?\s*)?[八九十][\u3001.]|\n---|\Z", text[start:])
        end = start + end_m.start() if end_m else len(text)
        result["consistency_check"] = text[start:end].strip()

    # 護城河信號分類
    if 4 in result["sections"]:
        pos_kw = ["強化", "提升", "增加", "擴大", "改善", "成長", "上升", "漲價", "穩定"]
        neg_kw = ["弱化", "下降", "降低", "縮小", "惡化", "萎縮", "流失", "壓縮", "下滑"]
        for line in result["sections"][4]["content"].split("\n"):
            line = line.strip().lstrip("-•*").strip()
            if not line or line.startswith("#"):
                continue
            if any(k in line for k in pos_kw):
                sig_type = "positive"
            elif any(k in line for k in neg_kw):
                sig_type = "negative"
            else:
                sig_type = "neutral"
            result["signals"].append({"text": line, "type": sig_type})

    return result


def _parse_moat_from_text(text: str) -> dict:
    """
    從 10-K 分析文字中解析護城河五維度評分。
    支援格式：
      - 品牌力（8/10分）、品牌力：8/10
      - 品牌力（2/2分）（滿分 2 分制，按比例換算為 10 分制）
      - 品牌力（1分）（無分母，假設滿分 2 分制換算為 10 分制）
    回傳 {brand_power: float, ...}，找不到的維度不包含。
    """
    result = {}
    for key, cn_label in MOAT_5_DIMS.items():
        # 優先匹配「品牌力（8/10分）」或「品牌力：8/10」（含分母）
        pat_frac = rf"{re.escape(cn_label)}[（(：:]\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*分?[）)]?"
        m = re.search(pat_frac, text)
        if m:
            score = float(m.group(1))
            max_score = float(m.group(2))
            if max_score > 0:
                result[key] = round(score / max_score * 10, 1)
            else:
                result[key] = 0.0
            continue
        # 備援匹配「品牌力（1分）」（無分母，假設滿分 2 分換算為 10 分制）
        pat_simple = rf"{re.escape(cn_label)}[（(：:]\s*(\d+(?:\.\d+)?)\s*分[）)]?"
        m2 = re.search(pat_simple, text)
        if m2:
            score = float(m2.group(1))
            result[key] = round(score / 2 * 10, 1)
    return result


def _extract_10q_financials(content: str) -> list[dict]:
    """
    從 10-Q 數字變化段落提取財務指標，含變動方向偵測。
    回傳 [{label, value, current, previous, change, direction}, ...]
    """
    up_kw = ["上升", "增加", "成長", "提升", "增長", "上漲", "擴大",
             "改善", "高出", "超越", "優於", "好轉"]
    down_kw = ["下降", "減少", "衰退", "降低", "下滑", "縮小", "惡化",
               "低於", "不及", "壓縮", "收窄", "萎縮"]
    flat_kw = ["持平", "不變", "維持", "穩定", "持穩"]

    NUM_PAT = r'[\$￥]?\s*\d[\d,.]*\s*(?:億|百萬|千萬|million|billion|萬|%|％)?'

    rows = []
    for line in content.split("\n"):
        line = line.strip().lstrip("-•*").strip()
        # Strip markdown bold markers
        line = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', line)
        if not line:
            continue
        m = re.split(r"[：:]", line, maxsplit=1)
        label = m[0].strip() if m else line
        value = m[1].strip() if len(m) >= 2 else ""

        current = ""
        previous = ""
        change = ""

        if value:
            # Try to find previous period number
            prev_m = re.search(
                r'(?:前期|去年同期?|上期|上季|前季|prior)\s*[:：]?\s*(' + NUM_PAT + r')',
                value, re.IGNORECASE,
            )
            if prev_m:
                previous = prev_m.group(1).strip()

            # Try to find change percentage
            chg_m = re.search(
                r'(?:年增|季增|成長|增長|下降|衰退|變化|YoY|QoQ|年減|季減)\s*[:：]?\s*([+-]?\s*'
                + NUM_PAT + r')',
                value, re.IGNORECASE,
            )
            if not chg_m:
                chg_m = re.search(r'([+-]\s*\d[\d,.]*\s*[%％])', value)
            if chg_m:
                change = chg_m.group(1).strip()

            # First number in value is likely current period
            first_num = re.search(NUM_PAT, value)
            if first_num:
                candidate = first_num.group(0).strip()
                if candidate != previous and candidate != change:
                    current = candidate

        check = value or line
        if any(k in check for k in up_kw) or re.search(r"[+＋]\s*\d", check):
            direction = "up"
        elif any(k in check for k in down_kw) or re.search(r"[-－]\s*\d", check):
            direction = "down"
        elif any(k in check for k in flat_kw):
            direction = "flat"
        else:
            direction = ""

        if label or value:
            rows.append({
                "label": label, "value": value,
                "current": current, "previous": previous,
                "change": change, "direction": direction,
            })
    return rows


def _extract_10q_guidance(content: str) -> str:
    """
    從 10-Q 段落二（敘事變化）擷取前瞻指引文字。
    找不到時回傳空字串。
    """
    lines = content.split("\n")
    guidance_lines = []
    capturing = False
    for line in lines:
        stripped = line.strip().lstrip("-•*").strip()
        if any(kw in stripped for kw in ["前瞻指引", "guidance", "Guidance"]):
            capturing = True
            parts = re.split(r"[：:]", stripped, maxsplit=1)
            if len(parts) >= 2 and parts[1].strip():
                guidance_lines.append(parts[1].strip())
            elif parts[0].strip():
                guidance_lines.append(parts[0].strip())
            continue
        if capturing:
            if stripped and not stripped.startswith("#"):
                # 仍屬同一段（縮排或無新 bullet 開頭）
                if line.startswith("  ") or line.startswith("\t"):
                    guidance_lines.append(stripped)
                else:
                    break
            else:
                break
    return " ".join(guidance_lines).strip()


def _extract_10q_capital(content: str) -> list[dict]:
    """
    從 10-Q 段落三（資本配置）擷取結構化卡片資料。
    回傳 [{icon, label, amount, detail}, ...]。
    """
    items = []
    for line in content.split("\n"):
        line = line.strip().lstrip("-•*").strip()
        if not line:
            continue
        parts = re.split(r"[：:]", line, maxsplit=1)
        label = parts[0].strip()
        detail = parts[1].strip() if len(parts) >= 2 else ""

        # 嘗試從描述中提取關鍵數字
        num_m = re.search(
            r"[\$￥]?\s*\d[\d,.]*\s*(?:億|百萬|千萬|million|billion|萬)?",
            detail, re.IGNORECASE,
        )
        amount = num_m.group(0).strip() if num_m else ""

        # 依關鍵字選 icon
        if any(k in label for k in ["回購", "buyback", "庫藏股"]):
            icon = "&#x1F4B8;"
        elif any(k in label for k in ["股息", "dividend", "配息"]):
            icon = "&#x1F4B5;"
        elif any(k in label for k in ["收購", "acquisition", "合資", "出售", "佈局"]):
            icon = "&#x1F3E2;"
        elif any(k in label for k in ["資產負債", "淨現金", "淨負債", "利息"]):
            icon = "&#x1F3E6;"
        else:
            icon = "&#x1F4CA;"

        items.append({
            "icon": icon, "label": label,
            "amount": amount, "detail": detail,
        })
    return items


# ── Notion 資料讀取 ──────────────────────────────────────────────────────────

def _fetch_page_content(page_id: str) -> str:
    """讀取 Notion 頁面的所有 block，拼接為純文字。"""
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
    }
    resp = requests.get(
        f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100",
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    blocks = resp.json()
    parts: list[str] = []
    for block in blocks.get("results", []):
        btype = block.get("type", "")
        data = block.get(btype, {})
        rich_text = data.get("rich_text", [])
        text = "".join(rt.get("plain_text", "") for rt in rich_text)
        if text:
            parts.append(text)
    return "\n".join(parts)


def _get_title_text(page: dict, prop_name: str) -> str:
    prop = page.get("properties", {}).get(prop_name, {})
    for item in prop.get("title", []):
        return item.get("plain_text", "")
    return ""


def _get_rich_text(page: dict, prop_name: str) -> str:
    prop = page.get("properties", {}).get(prop_name, {})
    for item in prop.get("rich_text", []):
        return item.get("plain_text", "")
    return ""


def _get_date_value(page: dict, prop_name: str) -> str:
    prop = page.get("properties", {}).get(prop_name, {})
    date_obj = prop.get("date")
    if date_obj:
        return date_obj.get("start", "")
    return ""


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _normalize_full_date(raw: str, page: dict) -> str:
    """確保日期為 YYYY-MM-DD 格式；若不符則回退至頁面時間戳。"""
    if raw and _DATE_RE.match(raw):
        return raw[:10]  # 截取前 10 字元，避免帶時間
    # 回退：優先 created_time，再 last_edited_time
    for key in ("created_time", "last_edited_time"):
        ts = page.get(key, "")
        if ts and _DATE_RE.match(ts):
            return ts[:10]
    return raw  # 最後保底


def _get_number_value(page: dict, prop_name: str) -> float | None:
    """讀取 Notion 頁面的 number 屬性，回傳 float 或 None。"""
    prop = page.get("properties", {}).get(prop_name, {})
    val = prop.get("number")
    return float(val) if val is not None else None


def _query_all_pages(db_id: str) -> list[dict]:
    """分頁查詢 Notion 資料庫的所有頁面。"""
    pages: list[dict] = []
    cursor = None
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    while True:
        body: dict = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        resp = requests.post(
            f"https://api.notion.com/v1/databases/{db_id}/query",
            headers=headers,
            json=body,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        pages.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return pages


def fetch_notion_reports() -> list[dict]:
    """
    從兩個 Notion 資料庫讀取所有報告，回傳統一格式的 list。
    每筆：{name, ticker, form, date, page_id}
    """
    reports: list[dict] = []

    # 10-Q
    pages_10q = _query_all_pages(NOTION_10Q_DB_ID)
    print(f"  [DEBUG] 10-Q 資料庫讀取到 {len(pages_10q)} 筆頁面")
    for page in pages_10q:
        raw_date = (
            _get_date_value(page, "財報年度")
            or _get_date_value(page, "Date")
            or _get_date_value(page, "日期")
            or _get_rich_text(page, "財報年度")
        )
        full_date = _normalize_full_date(raw_date, page)
        reports.append({
            "name": _get_title_text(page, "Name"),
            "ticker": _get_rich_text(page, "Ticker"),
            "form": "10-Q",
            "date": full_date,
            "page_id": page["id"],
        })

    # 10-K
    pages_10k = _query_all_pages(NOTION_10K_DB_ID)
    print(f"  [DEBUG] 10-K 資料庫讀取到 {len(pages_10k)} 筆頁面")
    for page in pages_10k:
        name = _get_title_text(page, "Name")
        ticker = name.split()[0] if name else ""
        raw_date = (
            _get_date_value(page, "財報年度")
            or _get_date_value(page, "Date")
            or _get_date_value(page, "日期")
            or _get_rich_text(page, "財報年度")
        )
        full_date = _normalize_full_date(raw_date, page)
        # 嘗試從 Notion 欄位讀取護城河五維度分數
        moat_sub = {}
        for key in MOAT_5_DIMS:
            val = _get_number_value(page, key)
            if val is not None:
                moat_sub[key] = val
        if moat_sub:
            print(f"  [DEBUG] {ticker} Notion 護城河欄位: {moat_sub}")
        reports.append({
            "name": name,
            "ticker": ticker,
            "form": "10-K",
            "date": full_date,
            "page_id": page["id"],
            "moat_sub_scores": moat_sub,
        })

    # 依日期降冪排序（最新在最上面）
    reports.sort(key=lambda r: r.get("date", ""), reverse=True)
    return reports


# ── 深度研究掃描 ─────────────────────────────────────────────────────────────

def _scan_dd_reports() -> list[dict]:
    """
    掃描 docs/dd/ 資料夾，找出所有 DD_*.html 檔案。
    檔名格式：DD_TICKER_YYYYMMDD.html
    回傳 [{ticker, date, filename}, ...]，按 Ticker 字母順序排序。
    """
    results = []
    dd_dir = DOCS_DIR / "dd"
    if not dd_dir.is_dir():
        return results
    for p in dd_dir.glob("DD_*.html"):
        m = re.match(r"DD_([A-Za-z]+)_(\d{8})\.html$", p.name)
        if not m:
            continue
        ticker = m.group(1).upper()
        raw_date = m.group(2)
        date_fmt = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
        results.append({
            "ticker": ticker,
            "date": date_fmt,
            "filename": p.name,
        })
    results.sort(key=lambda r: r["ticker"])
    return results


# ── 首頁生成 ─────────────────────────────────────────────────────────────────

def generate_index(reports: list[dict]) -> None:
    """生成 docs/index.html —— 乾淨 landing page（hero + feature cards only）。

    Phase 3: 報告表格已移至 /research/。首頁只留導覽與入口卡片。
    `reports` 參數保留為介面相容，實際不使用內容。
    """
    dd_count = len(_scan_dd_reports())
    body = f"""
<section class="hero">
  <div class="container">
    <span class="eyebrow">AI 驅動 · 每日更新</span>
    <h1>InvestMQuest Research</h1>
    <p class="sub">量化系統回測 · 每日市場簡報 · 深度週報 · 個股 DD · 財報分析 — 一站式投資研究平台</p>
    <div class="stats">
      <div class="stat"><div class="stat-num">{dd_count}+</div><div class="stat-label">深度研究</div></div>
      <div class="stat"><div class="stat-num">10+</div><div class="stat-label">量化系統</div></div>
      <div class="stat"><div class="stat-num">06:00</div><div class="stat-label">每日簡報</div></div>
      <div class="stat"><div class="stat-num">10</div><div class="stat-label">週報主題</div></div>
    </div>
  </div>
</section>

<section class="features">
  <div class="container">
    <div class="feature-grid">
      <a href="/research/" class="feature-card">
        <div class="feature-icon-wrap">📑</div>
        <h3>研究報告 <span class="arrow">&rarr;</span></h3>
        <p>個股深度 DD 報告（買側框架、護城河、估值、R:R 診斷）與 10-K / 10-Q 財報分析，涵蓋美股與台股。</p>
      </a>
      <a href="/backtest/" class="feature-card">
        <div class="feature-icon-wrap">📈</div>
        <h3>量化系統回測 <span class="arrow">&rarr;</span></h3>
        <p>10+ 量化交易系統的完整 20 年回測。趨勢跟蹤、動量輪動、波動率加權、海龜系統等，真實 yfinance 資料。</p>
      </a>
      <a href="/briefing/" class="feature-card">
        <div class="feature-icon-wrap">📰</div>
        <h3>每日市場簡報 <span class="arrow">&rarr;</span></h3>
        <p>每日全球市場數據、新聞主題、央行政策、技術面與基本面綜合分析。每天台北時間 06:00 自動更新。</p>
      </a>
      <a href="/weekly/" class="feature-card">
        <div class="feature-icon-wrap">📊</div>
        <h3>每週深度週報 <span class="arrow">&rarr;</span></h3>
        <p>10 個主題的深度週度分析：央行、流動性、信用、選擇權、AI 產業、半導體、財報、宏觀、商品、黑天鵝。</p>
      </a>
      <a href="/six-state/" class="feature-card">
        <div class="feature-icon-wrap">🎯</div>
        <h3>六狀態機即時狀態 <span class="arrow">&rarr;</span></h3>
        <p>即時市場狀態指示器。SPY/QQQ 當前 S1 巡航 / S2 防守 / S5 趨勢重啟狀態，以及 Grid 加碼觸發判斷。</p>
      </a>
    </div>
  </div>
</section>"""

    # 首頁使用客製 CSS（lean landing），不走 _base_page
    _write_html(DOCS_DIR / "index.html", _landing_page("InvestMQuest Research", body))


def _landing_page(title: str, body: str) -> str:
    """Clean landing page template（僅 homepage 使用）。"""
    landing_css = """
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;
      --text:#111827;--muted:#6b7280;--border:#e5e7eb}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
     background:var(--bg);color:var(--text);line-height:1.65;font-size:15px;
     min-height:100vh;display:flex;flex-direction:column}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem;width:100%}
header{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.75rem 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.hdr-inner{display:flex;align-items:center;justify-content:space-between}
header .logo{font-size:1.15rem;font-weight:700;color:#fff;letter-spacing:-.02em}
header .logo span{color:#3b82f6}
header nav a{color:rgba(255,255,255,.7);margin-left:1.4rem;font-size:.85rem;font-weight:500;
             padding-bottom:4px;border-bottom:2px solid transparent;transition:all .2s}
header nav a:hover{color:#fff;text-decoration:none;border-bottom-color:rgba(255,255,255,.4)}
header nav a.active{color:#fff;border-bottom-color:#3b82f6}
.hero{padding:4rem 0 3rem;background:linear-gradient(180deg,#f0f4ff 0%,#f9fafb 100%);
      border-bottom:1px solid var(--border);text-align:center}
.hero .eyebrow{display:inline-block;padding:.35rem .9rem;background:rgba(26,86,219,.08);
               color:var(--brand);border-radius:999px;font-size:.75rem;font-weight:600;
               letter-spacing:.04em;margin-bottom:1rem;text-transform:uppercase}
.hero h1{font-size:2.6rem;font-weight:800;letter-spacing:-.03em;line-height:1.15;
         background:linear-gradient(135deg,#0f172a 0%,#1a56db 100%);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         background-clip:text;color:transparent;margin-bottom:.85rem}
.hero .sub{color:var(--muted);font-size:1.05rem;max-width:640px;margin:0 auto;line-height:1.65}
.hero .stats{display:flex;flex-wrap:wrap;justify-content:center;gap:2rem;
             margin-top:1.75rem;padding-top:1.5rem;border-top:1px solid rgba(0,0,0,.05);
             max-width:640px;margin-left:auto;margin-right:auto}
.hero .stat{text-align:center}
.hero .stat-num{font-size:1.35rem;font-weight:700;color:var(--text);line-height:1.1}
.hero .stat-label{font-size:.72rem;color:var(--muted);margin-top:.25rem;
                  text-transform:uppercase;letter-spacing:.05em}
.features{padding:3rem 0 2rem;flex:1}
.feature-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.1rem}
.feature-card{display:block;background:var(--card);border:1px solid var(--border);
              border-radius:12px;padding:1.5rem 1.55rem;text-decoration:none;
              color:var(--text);transition:all .22s ease;position:relative;overflow:hidden}
.feature-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;
                      background:linear-gradient(90deg,var(--brand),#3b82f6);
                      opacity:0;transition:opacity .22s ease}
.feature-card:hover{text-decoration:none;border-color:transparent;transform:translateY(-3px);
                    box-shadow:0 10px 24px rgba(15,23,42,.08),0 2px 4px rgba(26,86,219,.06)}
.feature-card:hover::before{opacity:1}
.feature-icon-wrap{display:inline-flex;align-items:center;justify-content:center;
                   width:44px;height:44px;border-radius:10px;
                   background:linear-gradient(135deg,#eff6ff,#dbeafe);
                   margin-bottom:1rem;font-size:1.4rem}
.feature-card h3{font-size:1.02rem;font-weight:700;color:var(--text);margin-bottom:.45rem;
                 display:flex;align-items:center;gap:.4rem}
.feature-card h3 .arrow{color:var(--muted);font-size:.95rem;
                        transition:transform .22s ease,color .22s ease;margin-left:auto}
.feature-card:hover h3 .arrow{color:var(--brand);transform:translateX(4px)}
.feature-card p{font-size:.83rem;color:var(--muted);line-height:1.65;margin:0}
.disclaimer{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;
            padding:.85rem 1.1rem;font-size:.76rem;color:#78350f;margin:1.75rem 0}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem}
@media(max-width:768px){
  .hero{padding:2.5rem 0 2rem}.hero h1{font-size:1.85rem}
  .hero .sub{font-size:.9rem}.hero .stats{gap:1.25rem;margin-top:1.25rem;padding-top:1rem}
  .hero .stat-num{font-size:1.15rem}.features{padding:2rem 0 1.5rem}
  .feature-grid{grid-template-columns:1fr;gap:.8rem}.feature-card{padding:1.2rem 1.3rem}
  .hdr-inner{flex-direction:column;gap:.5rem}
  header nav{display:flex;flex-wrap:wrap;justify-content:center;gap:.4rem 0}
  header nav a{margin-left:0;margin-right:1rem;font-size:.78rem}
}
"""
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html_lib.escape(title)}</title>
  <meta name="description" content="量化交易系統 20 年回測、每日市場簡報、深度週報、個股 DD 研究、財報分析的整合性投資研究平台">
  <meta property="og:title" content="{html_lib.escape(title)}">
  <meta property="og:site_name" content="InvestMQuest Research">
  <style>{landing_css}</style>
</head>
<body>
{_header('首頁')}
{body}
<div class="container">
  <div class="disclaimer">
    <strong>免責聲明：</strong>
    本網站所有內容均由 AI 自動生成，僅供參考，<strong>不構成任何投資建議</strong>。
    投資涉及風險，投資人應自行判斷並諮詢專業顧問。過往表現不代表未來業績。本網站與任何被分析公司均無利益關係。
  </div>
</div>
<footer>
  <div class="container">
    &copy; {datetime.date.today().year} InvestMQuest Research &middot;
    由 AI 自動生成，僅供參考
  </div>
</footer>
</body>
</html>"""


def generate_research(reports: list[dict]) -> None:
    """生成 docs/research/index.html —— 深度研究報告 + 財報分析總表。"""
    today = datetime.date.today().strftime("%Y 年 %m 月 %d 日")

    rows = ""
    for r in reports:
        ticker = html_lib.escape(r.get("ticker", ""))
        form = r.get("form", "")
        date = html_lib.escape(r.get("date", ""))
        page_id = r.get("page_id", "")
        slug = page_id.replace("-", "")
        tag_cls = "tag-10k" if form == "10-K" else "tag-10q"

        # 護城河等級
        moat_avg = r.get("moat_avg")
        moat_level = r.get("moat_level")
        if moat_avg is not None:
            level = _moat_level(moat_avg)
            badge_cls = _moat_badge_cls(level)
            level_cn = _moat_level_cn(moat_avg)
            moat_cell = f'<span class="moat-badge {badge_cls}">{html_lib.escape(level_cn)}</span>'
        elif moat_level:
            badge_cls = _moat_badge_cls(moat_level)
            level_cn = {"Wide": "寬護城河 Wide Moat", "Narrow": "窄護城河 Narrow Moat"}.get(
                moat_level, "無護城河 No Moat"
            )
            moat_cell = f'<span class="moat-badge {badge_cls}">{html_lib.escape(level_cn)}</span>'
        else:
            moat_cell = '<span style="color:var(--muted)">—</span>'
            moat_data = "none"

        # 設定 data-moat 屬性值
        if moat_avg is not None:
            level = _moat_level(moat_avg)
            moat_data = {"Wide": "wide", "Narrow": "narrow", "No Moat": "nomoat"}.get(level, "unrated")
        elif moat_level:
            moat_data = {"Wide": "wide", "Narrow": "narrow", "No Moat": "nomoat"}.get(moat_level, "unrated")
        else:
            moat_data = "unrated"

        rows += f"""
<tr class="searchable" data-form="{html_lib.escape(form)}" data-moat="{moat_data}">
  <td><strong>{ticker}</strong></td>
  <td><span class="tag {tag_cls}">{html_lib.escape(form)}</span></td>
  <td>{date}</td>
  <td>{moat_cell}</td>
  <td><a href="/report/{slug}.html">查看 &rarr;</a></td>
</tr>"""

    total_count = len(reports)

    # ── 深度研究報告區塊（DD 放在最上方）
    dd_reports = _scan_dd_reports()
    dd_rows_html = ""
    for dd in dd_reports:
        t = html_lib.escape(dd["ticker"])
        d = html_lib.escape(dd["date"])
        fn = html_lib.escape(dd["filename"])
        dd_rows_html += f"""
<tr class="searchable">
  <td><strong>{t}</strong></td>
  <td><span class="tag tag-dd">深度研究</span></td>
  <td>{d}</td>
  <td><a href="/dd/{fn}">查看 &rarr;</a></td>
</tr>"""

    if not dd_rows_html:
        dd_rows_html = '<tr><td colspan="4" style="text-align:center;color:var(--muted);padding:2rem">尚無深度研究報告</td></tr>'

    body = f"""
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> &rsaquo; 研究報告</div>
    <h1>研究報告</h1>
    <p class="sub">深度個股研究（買側 DD 框架）· 10-K / 10-Q 財報分析（AI 驅動）。涵蓋美股與台股。</p>
  </div>
</div>

<div class="section" style="padding-top:1.25rem" id="dd-reports">
  <div class="container">
    <h2 class="section-title">深度研究報告<span class="count" id="dd-count">&nbsp;</span></h2>
    <div class="search-wrap">
      <input id="dd-search" type="text" placeholder="搜尋 Ticker 或日期…">
    </div>
    <div class="card" style="overflow-x:auto;padding:0">
      <table>
        <thead>
          <tr>
            <th>公司</th>
            <th>類型</th>
            <th>日期</th>
            <th></th>
          </tr>
        </thead>
        <tbody id="dd-tbody">
{dd_rows_html}
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="section" id="earnings-reports">
  <div class="container">
    <h2 class="section-title">財報分析<span class="count" id="earnings-count">&nbsp;</span></h2>

    <div class="search-wrap">
      <input id="earnings-search" type="text" placeholder="搜尋 Ticker、報告類型…">
    </div>

    <div class="filter-bar">
      <div class="filter-group">
        <span class="filter-label">類型</span>
        <button class="filter-btn active" data-filter="form" data-value="all">全部</button>
        <button class="filter-btn" data-filter="form" data-value="10-K">10-K</button>
        <button class="filter-btn" data-filter="form" data-value="10-Q">10-Q</button>
      </div>
      <div class="filter-group">
        <span class="filter-label">護城河</span>
        <button class="filter-btn active" data-filter="moat" data-value="all">全部</button>
        <button class="filter-btn" data-filter="moat" data-value="wide">寬護城河</button>
        <button class="filter-btn" data-filter="moat" data-value="narrow">窄護城河</button>
        <button class="filter-btn" data-filter="moat" data-value="nomoat">無護城河</button>
        <button class="filter-btn" data-filter="moat" data-value="unrated">未評級</button>
      </div>
    </div>

    <div class="card" style="overflow-x:auto;padding:0">
      <table>
        <thead>
          <tr>
            <th>公司</th>
            <th>類型</th>
            <th>日期</th>
            <th>護城河等級</th>
            <th></th>
          </tr>
        </thead>
        <tbody id="report-tbody">
          {rows or '<tr><td colspan="5" style="text-align:center;color:var(--muted);padding:2rem">尚無報告</td></tr>'}
        </tbody>
      </table>
    </div>
  </div>
</div>"""

    out_path = DOCS_DIR / "research" / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    _write_html(out_path, _base_page(f"研究報告 — {today}", body))


# ── 10-K 報告頁面 ───────────────────────────────────────────────────────────

def generate_report_page_10k(
    report: dict,
    moat_sub_scores: dict,
    content: str,
) -> None:
    """
    生成 10-K 報告頁面：圓形儀表板 + 八維度卡片 + 雷達圖 + 風險 + 核心論點。
    """
    page_id = report.get("page_id", "")
    slug = page_id.replace("-", "")
    ticker = html_lib.escape(report.get("ticker", ""))
    date = html_lib.escape(report.get("date", ""))

    parsed = _parse_10k_analysis(content)
    total = parsed["total_score"] or 0
    moat_level = parsed["moat_level"]

    # 備援：若 Notion 欄位讀取不到分數，從分析文字解析
    if not moat_sub_scores:
        moat_sub_scores = _parse_moat_from_text(content)

    # 若無法從文本解析護城河等級，從 moat_sub_scores 計算
    if not moat_level and moat_sub_scores:
        avg = sum(moat_sub_scores.values()) / len(moat_sub_scores)
        moat_level = _moat_level(avg)

    level_cn = ""
    badge_html = ""
    if moat_level:
        badge_cls = _moat_badge_cls(moat_level)
        if moat_sub_scores:
            avg = sum(moat_sub_scores.values()) / len(moat_sub_scores)
            level_cn = _moat_level_cn(avg)
        else:
            level_cn = {"Wide": "寬護城河 Wide Moat", "Narrow": "窄護城河 Narrow Moat"}.get(
                moat_level, "無護城河 No Moat"
            )
        badge_html = f'<span class="moat-badge {badge_cls}" style="font-size:.95rem">{html_lib.escape(level_cn)}</span>'

    # ── 核心論點
    thesis_html = ""
    if parsed["core_thesis"]:
        thesis_html = f"""
<div class="thesis">
  <p>&ldquo;{html_lib.escape(parsed["core_thesis"])}&rdquo;</p>
</div>"""

    # ── 圓形儀表（Chart.js Doughnut）+ 護城河等級
    gauge_color = _gauge_color_hex(total, 110.0)
    progress_pct = min(100, total / 110 * 100) if total > 0 else 0
    remaining_pct = 100 - progress_pct
    score_hero = f"""
<div class="score-hero">
  <div class="gauge-wrap" style="position:relative;width:160px;height:160px">
    <canvas id="gaugeChart" width="160" height="160"></canvas>
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center">
      <div style="font-size:28px;font-weight:700;color:{gauge_color}">{total:.0f}</div>
      <div style="font-size:13px;color:var(--muted)">/ 110</div>
    </div>
  </div>
  <div class="gauge-meta">
    {badge_html}
    <div style="font-size:.85rem;color:var(--muted)">
      綜合評分（滿分 110）<br>
      換算：{total / 110 * 100:.0f}%
    </div>
  </div>
</div>"""

    # ── 八維度卡片
    dim_cards = ""
    for d in parsed["dimensions"]:
        score = d["score"]
        if score is not None:
            cls = _score_cls(score)
            pct = _fill_pct(score)
            color = _score_color(score)
            score_html = f'<span class="dim-score {cls}">{score:.1f}/10</span>'
            bar_html = f'<div class="dim-bar"><div class="fill" style="width:{pct}%;background:{color}"></div></div>'
        else:
            score_html = '<span class="dim-score" style="color:var(--muted)">—</span>'
            bar_html = ""

        text_html = _md(d["text"]) if d["text"] else ""
        dim_cards += f"""
<div class="dim-card">
  <div class="dim-hdr">
    <span class="dim-name">{html_lib.escape(d["cn"])}<span class="dim-en">{html_lib.escape(d["en"])}</span></span>
    {score_html}
  </div>
  {bar_html}
  <div class="dim-text">{text_html}</div>
</div>"""

    # ── Chart.js 雷達圖 + 風險
    radar_html = ""
    risks_html = ""

    if moat_sub_scores:
        labels_json = json.dumps(
            [MOAT_5_DIMS[k] for k in MOAT_5_DIMS], ensure_ascii=False
        )
        data_json = json.dumps(
            [moat_sub_scores.get(k, 0) for k in MOAT_5_DIMS]
        )
        radar_html = f"""
<div class="card">
  <h3>護城河五維度</h3>
  <div style="max-width:340px;margin:0 auto">
    <canvas id="moatRadar"></canvas>
  </div>
</div>"""

    if parsed["risks"]:
        risk_items = ""
        for idx, risk in enumerate(parsed["risks"], 1):
            risk_items += f"""
<div class="risk-box">
  <span class="risk-num">{idx}.</span>{html_lib.escape(risk)}
</div>"""
        risks_html = f"""
<div class="card">
  <h3>關鍵風險</h3>
  {risk_items}
</div>"""

    # 雷達圖 + 風險 並排
    radar_risks = ""
    if radar_html or risks_html:
        radar_risks = f'<div class="radar-risks">{radar_html}{risks_html}</div>'

    # ── 投資委員會總結
    committee_parsed = _parse_committee_summary(content)
    committee_html = ""
    if committee_parsed["viewpoints"]:
        vp_rows = ""
        for vp in committee_parsed["viewpoints"]:
            vp_rows += f"""
<div style="display:flex;align-items:flex-start;gap:.75rem;margin-bottom:.7rem">
  <span style="display:inline-block;padding:.25rem .6rem;border-radius:4px;
               background:var(--brand);color:#fff;font-size:.75rem;font-weight:600;
               white-space:nowrap;flex-shrink:0;margin-top:.1rem">{html_lib.escape(vp["label"])}</span>
  <span style="font-size:.88rem;line-height:1.6;color:#374151">{_md(vp["content"])}</span>
</div>"""
        committee_html = f"""
<div class="card" style="border-left:4px solid var(--brand);background:var(--brand-light);margin-bottom:1.25rem">
  <h3 style="color:var(--brand);margin-bottom:.75rem">投資委員會總結</h3>
  {vp_rows}
</div>"""
    elif committee_parsed["raw"]:
        committee_html = f"""
<div class="card" style="border-left:4px solid var(--brand);background:var(--brand-light);margin-bottom:1.25rem">
  <h3 style="color:var(--brand);margin-bottom:.6rem">投資委員會總結</h3>
  <div class="analysis">{_md(committee_parsed["raw"])}</div>
</div>"""

    # ── 大師框架分析
    masters = _parse_master_frameworks(content)
    masters_html = ""
    if masters:
        master_cards = ""
        for mst in masters:
            icon = _MASTER_ICONS.get(mst["name"], "📊")
            score_tag = ""
            if mst.get("score"):
                score_tag = f"""
<div style="text-align:right;margin-top:.75rem;padding-top:.6rem;border-top:1px solid var(--border)">
  <span style="font-size:1.3rem;font-weight:700;color:var(--brand)">{html_lib.escape(mst["score"])}</span>
  <span style="font-size:.85rem;color:var(--muted)">/ 10</span>
</div>"""

            # ── Hamilton Helmer: 七種 Power 表格
            power_table = ""
            if mst["name"] == "Hamilton Helmer" and mst.get("extra", {}).get("powers"):
                pw_rows = ""
                for pw in mst["extra"]["powers"]:
                    lv = pw["level"]
                    if lv in ("強", "✓", "最強", "有"):
                        badge = '<span style="display:inline-block;padding:.15rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600;background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)">強</span>'
                    elif lv in ("弱", "較弱", "有限"):
                        badge = '<span style="display:inline-block;padding:.15rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600;background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)">弱</span>'
                    elif lv in ("不存在", "無", "✗", "不適用"):
                        badge = '<span style="display:inline-block;padding:.15rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600;background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db">不存在</span>'
                    else:
                        badge = f'<span style="display:inline-block;padding:.15rem .5rem;border-radius:4px;font-size:.75rem;font-weight:600;background:#dbeafe;color:#1e40af;border:1px solid #93c5fd">{html_lib.escape(lv)}</span>'
                    pw_rows += f"<tr><td style='font-weight:600;font-size:.85rem'>{html_lib.escape(pw['name'])}</td><td style='text-align:center'>{badge}</td></tr>"
                power_table = f"""
<table style="margin:.6rem 0;font-size:.85rem">
  <thead><tr><th>Power</th><th style="text-align:center">強度</th></tr></thead>
  <tbody>{pw_rows}</tbody>
</table>"""

            # ── Howard Marks: 週期位置進度條
            cycle_bar = ""
            if mst["name"] == "Howard Marks" and mst.get("extra", {}).get("cycle"):
                cyc = mst["extra"]["cycle"]
                pct = cyc["pct"]
                cycle_bar = f"""
<div style="margin:.75rem 0">
  <div style="font-size:.78rem;font-weight:600;color:var(--muted);margin-bottom:.35rem">週期位置</div>
  <div style="position:relative;height:28px;background:linear-gradient(90deg,var(--green-bg) 0%,#fffbeb 50%,var(--red-bg) 100%);border-radius:6px;border:1px solid var(--border)">
    <div style="position:absolute;left:{pct}%;top:50%;transform:translate(-50%,-50%);
                width:14px;height:14px;background:var(--brand);border-radius:50%;border:2px solid #fff;
                box-shadow:0 1px 3px rgba(0,0,0,.25)"></div>
  </div>
  <div style="display:flex;justify-content:space-between;font-size:.7rem;color:var(--muted);margin-top:.2rem">
    <span>底部</span><span>早期</span><span>中期</span><span>晚期</span><span>頂部</span>
  </div>
  <div style="text-align:center;margin-top:.3rem;font-size:.85rem;font-weight:600;color:var(--brand)">{html_lib.escape(cyc["label"])}</div>
</div>"""

            # 組合卡片內容：先文字、再特殊區塊、最後評分
            card_body = f'<div class="dim-text">{_md(mst["content"])}</div>'
            if power_table:
                card_body = power_table + f'<div class="dim-text" style="margin-top:.5rem">{_md(mst["content"])}</div>'
            if cycle_bar:
                card_body = f'<div class="dim-text">{_md(mst["content"])}</div>' + cycle_bar

            master_cards += f"""
<div class="dim-card" style="grid-column:1/-1">
  <div class="dim-hdr">
    <span class="dim-name">{icon} {html_lib.escape(mst["name"])}</span>
  </div>
  {card_body}
  {score_tag}
</div>"""
        masters_html = f"""
<h2 class="section-title" style="margin-top:1.5rem">大師框架分析</h2>
<div class="dim-grid">{master_cards}</div>"""

    # ── 完整分析（可展開）— Markdown → HTML
    full_text = _md(content)

    body = f"""
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">&larr; 返回首頁</a></div>
    <h1>{ticker} 10-K</h1>
    <p class="sub">{date}</p>
  </div>
</div>

<div class="section">
  <div class="container">
    {committee_html}
    {score_hero}
    {thesis_html}
    <h2 class="section-title">八維度評分</h2>
    <div class="dim-grid">{dim_cards}</div>
    {radar_risks}
    {masters_html}
    <details style="margin-top:1.5rem">
      <summary style="cursor:pointer;font-weight:600;font-size:.95rem;color:var(--brand);
                       padding:.5rem 0">展開完整分析文本</summary>
      <div class="card" style="margin-top:.75rem">
        <div class="analysis">{full_text}</div>
      </div>
    </details>
  </div>
</div>"""

    # Chart.js 腳本（Doughnut 儀表 + Radar 雷達圖）
    chart_head = '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>'

    radar_init = ""
    if moat_sub_scores:
        radar_init = f"""
  var rc=document.getElementById('moatRadar');
  if(rc){{new Chart(rc,{{
    type:'radar',
    data:{{
      labels:{labels_json},
      datasets:[{{
        data:{data_json},
        backgroundColor:'rgba(26,86,219,0.12)',
        borderColor:'#1a56db',
        borderWidth:2,
        pointBackgroundColor:'#1a56db',
        pointRadius:4,
        pointHoverRadius:6
      }}]
    }},
    options:{{
      scales:{{r:{{min:0,max:10,ticks:{{stepSize:2,font:{{size:11}}}},
                  pointLabels:{{font:{{size:13}}}}}}}},
      plugins:{{legend:{{display:false}}}}
    }}
  }});}}"""

    chart_script = f"""
<script>
document.addEventListener('DOMContentLoaded',function(){{
  var gc=document.getElementById('gaugeChart');
  if(gc){{new Chart(gc,{{
    type:'doughnut',
    data:{{
      datasets:[{{
        data:[{progress_pct:.1f},{remaining_pct:.1f}],
        backgroundColor:['{gauge_color}','#e5e7eb'],
        borderWidth:0
      }}]
    }},
    options:{{
      cutout:'75%',
      responsive:false,
      plugins:{{legend:{{display:false}},tooltip:{{enabled:false}}}}
    }}
  }});}}{radar_init}
}});
</script>"""

    full_body = body + chart_script
    out_dir = DOCS_DIR / "report"
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_html(
        out_dir / f"{slug}.html",
        _base_page(f"{ticker} 10-K — {date}", full_body, chart_head),
    )


# ── 10-Q 報告頁面 ───────────────────────────────────────────────────────────

def generate_report_page_10q(report: dict, content: str) -> None:
    """
    生成 10-Q 報告頁面（全新版面設計）：
      頂部 Ticker + 一句話摘要 → 數字變化表格 → 敘事變化 →
      管理層誠信 → 資本配置卡片 → 護城河信號 → 附注清單 → 一致性驗證
    """
    page_id = report.get("page_id", "")
    slug = page_id.replace("-", "")
    ticker = html_lib.escape(report.get("ticker", ""))
    date = html_lib.escape(report.get("date", ""))

    parsed = _parse_10q_sections(content)

    # ── 頂部：一句話摘要
    summary_hero = ""
    if parsed["summary"]:
        summary_hero = f"""
<div class="thesis">
  <p>&ldquo;{html_lib.escape(parsed["summary"])}&rdquo;</p>
</div>"""

    # ── 1. 數字變化 → 乾淨表格
    fin_card_html = ""
    if 1 in parsed["sections"]:
        fin_rows = _extract_10q_financials(parsed["sections"][1]["content"])
        if fin_rows:
            trs = ""
            for fr in fin_rows:
                label = html_lib.escape(fr["label"])
                cur = html_lib.escape(fr.get("current", ""))
                prev = html_lib.escape(fr.get("previous", ""))
                chg = html_lib.escape(fr.get("change", ""))
                d = fr["direction"]
                if d == "up":
                    chg_display = f'<span class="chg-up">{chg} &#x2191;</span>' if chg else '<span class="chg-up">&#x2191;</span>'
                elif d == "down":
                    chg_display = f'<span class="chg-down">{chg} &#x2193;</span>' if chg else '<span class="chg-down">&#x2193;</span>'
                elif d == "flat":
                    chg_display = '<span class="chg-flat">&mdash; 持平</span>'
                else:
                    chg_display = html_lib.escape(chg) if chg else ""

                if cur or prev:
                    trs += (f"<tr><td style='font-weight:600'>{label}</td>"
                            f"<td>{cur}</td><td>{prev}</td>"
                            f"<td style='text-align:center'>{chg_display}</td></tr>")
                else:
                    # Fallback: show full value spanning current+previous columns
                    val = html_lib.escape(fr["value"])
                    trs += (f"<tr><td style='font-weight:600'>{label}</td>"
                            f"<td colspan='2'>{val}</td>"
                            f"<td style='text-align:center'>{chg_display}</td></tr>")

            fin_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">一、數字變化 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Financial Changes</span></h3>
  <div style="overflow-x:auto">
    <table>
      <thead><tr><th>指標</th><th>本期數字</th><th>前期數字</th><th style="text-align:center">變化</th></tr></thead>
      <tbody>{trs}</tbody>
    </table>
  </div>
</div>"""
        else:
            fin_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">一、數字變化 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Financial Changes</span></h3>
  <div class="analysis">{_md(parsed["sections"][1]["content"])}</div>
</div>"""

    # ── 2. 敘事變化 + 前瞻指引
    narrative_card_html = ""
    if 2 in parsed["sections"]:
        sec2 = parsed["sections"][2]["content"]
        guidance_text = _extract_10q_guidance(sec2)

        guidance_inset = ""
        if guidance_text:
            guidance_inset = f"""
  <div style="background:var(--brand-light);border:1px solid #93c5fd;border-radius:6px;
              padding:.75rem 1rem;margin-top:.75rem">
    <div style="font-size:.78rem;font-weight:600;color:var(--brand);margin-bottom:.25rem">&#x1F52D; 前瞻指引 Forward Guidance</div>
    <div style="font-size:.85rem;line-height:1.6;color:#1e40af">{_md(guidance_text)}</div>
  </div>"""

        remaining_lines = []
        for line in sec2.split("\n"):
            stripped = line.strip().lstrip("-•*").strip()
            if not stripped:
                continue
            if any(kw in stripped for kw in ["前瞻指引", "guidance", "Guidance"]):
                continue
            remaining_lines.append(line)
        remaining_text = "\n".join(remaining_lines)

        narrative_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">二、敘事變化 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Narrative Changes</span></h3>
  <div class="analysis">{_md(remaining_text)}</div>
  {guidance_inset}
</div>"""

    # ── 2.5 管理層誠信驗證（獨立卡片）
    mgmt_card_html = ""
    if parsed.get("mgmt_integrity"):
        mgmt_card_html = f"""
<div class="card mgmt-card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem;color:var(--brand)">&#x1F50D; 管理層誠信驗證 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Management Integrity Check</span></h3>
  <div class="analysis">{_md(parsed["mgmt_integrity"])}</div>
</div>"""

    # ── 3. 資本配置卡片（只顯示有實際數字的卡片）
    capital_card_html = ""
    if 3 in parsed["sections"] and parsed["sections"][3]["content"].strip():
        cap_items = _extract_10q_capital(parsed["sections"][3]["content"])
        if cap_items:
            # 只保留有實際數字的卡片
            cap_items = [ci for ci in cap_items if ci.get("amount")]
        if cap_items:
            cap_cards = ""
            for ci in cap_items:
                amount_line = f'<div class="cap-amount">{html_lib.escape(ci["amount"])}</div>' if ci["amount"] else ""
                detail_line = f'<div class="cap-detail">{_md(ci["detail"])}</div>' if ci["detail"] else ""
                cap_cards += f"""
<div class="cap-card">
  <div class="cap-icon">{ci["icon"]}</div>
  <div class="cap-label">{html_lib.escape(ci["label"])}</div>
  {amount_line}
  {detail_line}
</div>"""
            capital_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">三、資本配置 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Capital Allocation</span></h3>
  <div class="cap-grid">{cap_cards}</div>
</div>"""

    # ── 4. 護城河信號（強化=綠色✓ / 弱化=紅色✗）
    moat_card_html = ""
    if parsed["signals"] or (4 in parsed["sections"]):
        sig_items = ""
        if parsed["signals"]:
            for sig in parsed["signals"]:
                if sig["type"] == "positive":
                    sig_items += f'<span class="signal signal-pos">&#x2713; {html_lib.escape(sig["text"])}</span>\n'
                elif sig["type"] == "negative":
                    sig_items += f'<span class="signal signal-neg">&#x2717; {html_lib.escape(sig["text"])}</span>\n'
                else:
                    sig_items += f'<span class="signal signal-neu">{html_lib.escape(sig["text"])}</span>\n'
        elif 4 in parsed["sections"]:
            sig_items = f'<div class="analysis">{_md(parsed["sections"][4]["content"])}</div>'

        moat_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">四、護城河信號 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Moat Signals</span></h3>
  <div style="display:flex;flex-wrap:wrap;gap:.4rem">{sig_items}</div>
</div>"""

    # ── 6. 附注重點掃描（清單格式）
    footnote_card_html = ""
    if parsed.get("footnote_scan"):
        fn_lines = parsed["footnote_scan"].split("\n")
        fn_items = ""
        for line in fn_lines:
            stripped = line.strip().lstrip("-•*#").strip()
            stripped = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', stripped)
            if stripped:
                fn_items += f"<li>{html_lib.escape(stripped)}</li>\n"
        if fn_items:
            footnote_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">六、附注重點掃描 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Footnote Highlights</span></h3>
  <ul class="footnote-list">{fn_items}</ul>
</div>"""
        else:
            footnote_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">六、附注重點掃描 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Footnote Highlights</span></h3>
  <div class="analysis">{_md(parsed["footnote_scan"])}</div>
</div>"""

    # ── 7. 數字一致性驗證（通過/不通過視覺化）
    consistency_card_html = ""
    if parsed.get("consistency_check"):
        cc_text = parsed["consistency_check"]
        cc_lines = cc_text.split("\n")
        badges_html = ""
        has_badges = False
        pass_kw = ["通過", "一致", "吻合", "相符", "正確", "pass", "Pass", "✓", "符合"]
        fail_kw = ["不通過", "不一致", "差異", "不符", "偏差", "fail", "Fail", "✗", "異常"]
        for line in cc_lines:
            stripped = line.strip().lstrip("-•*#").strip()
            stripped = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', stripped)
            if not stripped:
                continue
            is_pass = any(k in stripped for k in pass_kw)
            is_fail = any(k in stripped for k in fail_kw)
            if is_fail:
                badges_html += f'<div class="consistency-badge consistency-fail">&#x2717; {html_lib.escape(stripped)}</div>\n'
                has_badges = True
            elif is_pass:
                badges_html += f'<div class="consistency-badge consistency-pass">&#x2713; {html_lib.escape(stripped)}</div>\n'
                has_badges = True
            else:
                badges_html += (f'<div class="consistency-badge" style="background:#f3f4f6;'
                                f'color:#374151;border:1px solid #d1d5db">'
                                f'{html_lib.escape(stripped)}</div>\n')
                has_badges = True

        if has_badges:
            consistency_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">七、數字一致性驗證 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Consistency Check</span></h3>
  <div style="display:flex;flex-wrap:wrap;gap:.5rem">{badges_html}</div>
</div>"""
        else:
            consistency_card_html = f"""
<div class="card" style="margin-bottom:1.25rem">
  <h3 style="margin-bottom:.75rem">七、數字一致性驗證 <span style="font-size:.78rem;color:var(--muted);font-weight:400">Consistency Check</span></h3>
  <div class="analysis">{_md(cc_text)}</div>
</div>"""

    # ── 完整分析（可展開）— Markdown → HTML
    full_text = _md(content)

    body = f"""
<div class="page-hdr" style="background:#fff;padding:2rem 0 1.5rem;border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="crumb"><a href="/">&larr; 返回首頁</a></div>
    <h1 style="font-size:2rem;font-weight:800;letter-spacing:-.04em;color:var(--text)">{ticker}</h1>
    <p style="color:var(--brand);font-size:1rem;font-weight:600;margin-top:.3rem">10-Q &middot; {date}</p>
  </div>
</div>

<div class="section">
  <div class="container">
    {summary_hero}

    <h2 class="section-title" style="margin-top:1.5rem">季報分析</h2>

    {fin_card_html}
    {narrative_card_html}
    {mgmt_card_html}
    {capital_card_html}
    {moat_card_html}
    {footnote_card_html}
    {consistency_card_html}

    <details style="margin-top:1.5rem">
      <summary style="cursor:pointer;font-weight:600;font-size:.95rem;color:var(--brand);
                       padding:.5rem 0">展開完整分析文本</summary>
      <div class="card" style="margin-top:.75rem">
        <div class="analysis">{full_text}</div>
      </div>
    </details>
  </div>
</div>"""

    out_dir = DOCS_DIR / "report"
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_html(
        out_dir / f"{slug}.html",
        _base_page(f"{ticker} 10-Q — {date}", body),
    )


# ── 公司頁面 ─────────────────────────────────────────────────────────────────

def generate_company_page(
    ticker: str,
    company_name: str,
    history: list[dict],
    moat_history: dict,
) -> None:
    """
    生成 docs/company/{ticker}.html。
    history: [{form, date, analysis, moat_score}, ...]
    moat_history: {"2022": {brand_power: 7, ...}, ...}
    """
    ticker_esc = html_lib.escape(ticker.upper())
    name_esc = html_lib.escape(company_name or ticker.upper())

    # 護城河現況
    latest_year = sorted(moat_history.keys())[-1] if moat_history else None
    moat_section = ""
    if latest_year:
        scores = moat_history[latest_year]
        avg = sum(scores.values()) / len(scores) if scores else 0
        level = _moat_level(avg)
        badge_cls = _moat_badge_cls(level)
        level_cn = _moat_level_cn(avg)

        bars = ""
        for dim_key, dim_label in MOAT_5_DIMS.items():
            s = scores.get(dim_key, 0)
            pct = _fill_pct(s)
            color = _score_color(s)
            cls = _score_cls(s)
            bars += f"""
<div style="margin-bottom:.65rem">
  <div style="display:flex;justify-content:space-between;margin-bottom:.2rem">
    <span style="font-size:.88rem">{html_lib.escape(dim_label)}</span>
    <span class="{cls}" style="font-weight:600">{s:.1f}/10</span>
  </div>
  <div class="moat-bar"><div class="moat-fill" style="width:{pct}%;background:{color}"></div></div>
</div>"""

        moat_section = f"""
<div class="card" style="margin-bottom:1rem">
  <h3>護城河評分（{latest_year}）
    <span class="moat-badge {badge_cls}" style="margin-left:.5rem;font-size:.78rem">{html_lib.escape(level_cn)}</span>
  </h3>
  {bars}
</div>"""

    # 歷年趨勢表
    trend_rows = ""
    if moat_history:
        dim_headers = "".join(
            f"<th>{label}</th>" for label in MOAT_5_DIMS.values()
        )
        for year in sorted(moat_history.keys()):
            sc = moat_history[year]
            avg = sum(sc.values()) / len(sc) if sc else 0
            cls = _score_cls(avg)
            cols = "".join(f"<td>{sc.get(k, 0):.1f}</td>" for k in MOAT_5_DIMS)
            trend_rows += f"<tr><td>{html_lib.escape(year)}</td>{cols}<td class='{cls}' style='font-weight:600'>{avg:.1f}</td></tr>"

        trend_table = f"""
<div class="card" style="margin-bottom:1rem;overflow-x:auto">
  <h3>護城河歷年趨勢</h3>
  <table>
    <thead><tr><th>年份</th>{dim_headers}<th>平均</th></tr></thead>
    <tbody>{trend_rows}</tbody>
  </table>
</div>"""
    else:
        trend_table = ""

    # 歷史報告列表
    history_rows = ""
    for rep in history:
        form = rep.get("form", "")
        rdate = rep.get("date", "")
        summary = html_lib.escape(rep.get("analysis", "")[:200])
        tag_cls = "tag-10k" if form == "10-K" else "tag-10q"
        ms = rep.get("moat_score")
        moat_td = f'<span class="{_score_cls(ms)}" style="font-weight:600">{ms:.1f}</span>' if ms else "—"
        history_rows += f"""
<tr>
  <td><span class="tag {tag_cls}">{html_lib.escape(form)}</span></td>
  <td>{html_lib.escape(rdate)}</td>
  <td>{moat_td}</td>
  <td style="font-size:.82rem">{summary}&hellip;</td>
</tr>"""

    body = f"""
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">&larr; 返回首頁</a></div>
    <h1>{ticker_esc}</h1>
    <p class="sub">{name_esc} &mdash; 歷史財報分析</p>
  </div>
</div>
<div class="section">
  <div class="container">
    {moat_section}
    {trend_table}
    <div class="card" style="overflow-x:auto">
      <h3>申報歷史</h3>
      <table>
        <thead><tr><th>類型</th><th>日期</th><th>護城河</th><th>摘要</th></tr></thead>
        <tbody>{history_rows or '<tr><td colspan="4" style="text-align:center;color:var(--muted)">尚無記錄</td></tr>'}</tbody>
      </table>
    </div>
  </div>
</div>"""

    out_dir = DOCS_DIR / "company"
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_html(
        out_dir / f"{ticker.lower()}.html",
        _base_page(f"{ticker_esc} 財報分析", body),
    )


# ── 產業比較頁面 ─────────────────────────────────────────────────────────────

def generate_industry_page(
    industry_name: str,
    companies: list[dict],
) -> None:
    """
    生成 docs/industry/{slug}.html。
    companies: [{ticker, company_name, moat_scores: {...}, avg_moat: X}, ...]
    """
    slug = industry_name.lower().replace(" ", "-")
    name_esc = html_lib.escape(industry_name)

    sorted_cos = sorted(companies, key=lambda c: c.get("avg_moat", 0), reverse=True)

    # 護城河排行條
    bar_chart = ""
    for co in sorted_cos:
        t = co.get("ticker", "")
        avg = co.get("avg_moat", 0)
        pct = _fill_pct(avg)
        color = _score_color(avg)
        cls = _score_cls(avg)
        level = _moat_level(avg)
        badge_cls = _moat_badge_cls(level)
        bar_chart += f"""
<div style="margin-bottom:.6rem;display:flex;align-items:center;gap:.75rem">
  <a href="/company/{t.lower()}.html"
     style="min-width:55px;font-weight:600;font-size:.88rem">{html_lib.escape(t)}</a>
  <div class="moat-bar" style="flex:1"><div class="moat-fill" style="width:{pct}%;background:{color}"></div></div>
  <span class="{cls}" style="font-weight:600;min-width:35px;text-align:right">{avg:.1f}</span>
</div>"""

    # 詳細比較表
    dim_headers = "".join(f"<th>{label}</th>" for label in MOAT_5_DIMS.values())
    rows = ""
    for co in sorted_cos:
        t = co.get("ticker", "")
        scores = co.get("moat_scores", {})
        avg = co.get("avg_moat", 0)
        cls = _score_cls(avg)
        dim_cells = "".join(f"<td>{scores.get(k, 0):.1f}</td>" for k in MOAT_5_DIMS)
        rows += f"""
<tr>
  <td><a href="/company/{t.lower()}.html">{html_lib.escape(t)}</a></td>
  {dim_cells}
  <td class="{cls}" style="font-weight:600">{avg:.1f}</td>
</tr>"""

    body = f"""
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">&larr; 返回首頁</a></div>
    <h1>{name_esc}</h1>
    <p class="sub">護城河橫向比較</p>
  </div>
</div>
<div class="section">
  <div class="container">
    <div class="card" style="margin-bottom:1rem">
      <h3>護城河總分排行</h3>
      {bar_chart or '<p style="color:var(--muted)">尚無評分資料</p>'}
    </div>
    <div class="card" style="overflow-x:auto">
      <h3>詳細維度比較</h3>
      <table>
        <thead><tr><th>Ticker</th>{dim_headers}<th>平均</th></tr></thead>
        <tbody>{rows or '<tr><td colspan="7" style="text-align:center;color:var(--muted)">尚無資料</td></tr>'}</tbody>
      </table>
    </div>
  </div>
</div>"""

    out_dir = DOCS_DIR / "industry"
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_html(
        out_dir / f"{slug}.html",
        _base_page(f"{name_esc} 產業比較", body),
    )


# ── 工具函式 ─────────────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict | list:
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _write_html(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  生成：{path}")


def _ensure_404_and_cname() -> None:
    cname_path = DOCS_DIR / "CNAME"
    if not cname_path.exists():
        _write_html(cname_path, "research.investmquest.com")

    notfound_path = DOCS_DIR / "404.html"
    if not notfound_path.exists():
        body = """
<div class="page-hdr">
  <div class="container">
    <h1>404 — 頁面不存在</h1>
    <p class="sub"><a href="/">&larr; 返回首頁</a></p>
  </div>
</div>"""
        _write_html(notfound_path, _base_page("404 找不到頁面", body))


# ── 主函式 ───────────────────────────────────────────────────────────────────

def build_site() -> None:
    """
    從 Notion 兩個資料庫讀取報告，重建完整靜態網站。
    """
    print("\n[Web] 開始生成靜態網站...")

    companies_data: dict = _load_json(KB_DIR / "companies.json")
    industries_data: dict = _load_json(KB_DIR / "industries.json")
    moat_scores: dict = _load_json(KB_DIR / "moat_scores.json")
    print(f"  [DEBUG] moat_scores.json 載入結果: {len(moat_scores)} 家公司, keys={list(moat_scores.keys())[:10]}")

    _ensure_404_and_cname()

    # 從 Notion 兩個資料庫讀取所有報告
    print("\n[Web] 從 Notion 資料庫讀取報告...")
    notion_reports = fetch_notion_reports()
    print(f"  [DEBUG] 共讀取 {len(notion_reports)} 筆報告")

    # 為每筆報告讀取內容、解析護城河、生成個別頁面
    for report in notion_reports:
        ticker = report.get("ticker", "")
        form = report.get("form", "")
        page_id = report.get("page_id", "")

        try:
            content = _fetch_page_content(page_id)
        except Exception as exc:
            print(f"  [WARN] 無法讀取 {ticker} {form} 頁面內容: {exc}")
            continue

        if form == "10-K":
            # 1) 優先：Notion 欄位直接讀取的護城河分數
            moat_sub = report.get("moat_sub_scores", {})
            # 2) 備援：從 knowledge_base/moat_scores.json
            if not moat_sub:
                co_moat = moat_scores.get(ticker, {})
                if co_moat:
                    latest_yr = sorted(co_moat.keys())[-1]
                    moat_sub = co_moat[latest_yr]
            # 3) 最終備援：從分析文字解析（品牌力（8/10分）格式）
            if not moat_sub:
                moat_sub = _parse_moat_from_text(content)
                if moat_sub:
                    print(f"  [DEBUG] {ticker} 從分析文字解析護城河: {moat_sub}")
            print(f"  [DEBUG] {ticker} 10-K moat_sub_scores = {moat_sub}")

            # 設定護城河等級供首頁使用
            if moat_sub:
                avg = sum(moat_sub.values()) / len(moat_sub)
                report["moat_avg"] = avg
            elif ticker in moat_scores:
                co_moat = moat_scores[ticker]
                if co_moat:
                    latest_yr = sorted(co_moat.keys())[-1]
                    sc = co_moat[latest_yr]
                    avg = sum(sc.values()) / len(sc) if sc else 0
                    report["moat_avg"] = avg

            # 從分析文字解析護城河等級（寬/窄/無）
            if "moat_avg" not in report:
                parsed = _parse_10k_analysis(content)
                if parsed["moat_level"]:
                    report["moat_level"] = parsed["moat_level"]
                    print(f"  [DEBUG] {ticker} 從文字解析護城河等級: {parsed['moat_level']}")

            generate_report_page_10k(report, moat_sub, content)

        elif form == "10-Q":
            generate_report_page_10q(report, content)

    # 首頁 + 研究報告頁（在讀取內容並解析護城河之後生成，確保護城河等級已填入）
    generate_index(notion_reports)
    generate_research(notion_reports)
    print("[Web] 生成心智模型頁面...")
    generate_mental_models()

    # 個別公司頁面
    for ticker, co_data in companies_data.items():
        history = co_data.get("reports", [])
        moat_hist = moat_scores.get(ticker, {})
        company_name = co_data.get("name", ticker)

        for rep in history:
            year = rep.get("date", "")[:4]
            if year and year in moat_hist:
                sc = moat_hist[year]
                rep["moat_score"] = sum(sc.values()) / len(sc) if sc else None

        generate_company_page(ticker, company_name, history, moat_hist)

    # 產業比較頁面
    for industry, ind_data in industries_data.items():
        cos_in_industry: list[dict] = []
        for ticker in ind_data.get("tickers", []):
            co_moat = moat_scores.get(ticker, {})
            if co_moat:
                latest_yr = sorted(co_moat.keys())[-1]
                sc = co_moat[latest_yr]
                avg = sum(sc.values()) / len(sc) if sc else 0
            else:
                sc = {}
                avg = 0
            cos_in_industry.append({
                "ticker": ticker,
                "company_name": companies_data.get(ticker, {}).get("name", ticker),
                "moat_scores": sc,
                "avg_moat": avg,
            })
        generate_industry_page(industry, cos_in_industry)

    print(
        f"[Web] 網站生成完成！共 {len(notion_reports)} 筆報告、"
        f"{len(industries_data)} 個產業"
    )


def generate_mental_models() -> None:
    """
    Production generator for docs/mental-models/index.html.
    Renders the full Latticework page (Network View + Matrix View) as a static
    page with inline JS, using server-side SVG/HTML and embedded JSON data.
    """
    import math
    import json as json_mod
    from mental_models_data import DISCIPLINES, MODELS

    # ── Position formula (verbatim from DirectionA_Network.jsx:15-41) ─────────
    W, H = 1240, 820
    cx, cy = W * 0.42, H * 0.5  # 520.8, 410.0

    CLUSTERS = {
        "psych": {"ax": cx - 320, "ay": cy - 30,  "spread": 230},
        "micro": {"ax": cx + 280, "ay": cy - 200, "spread": 170},
        "math":  {"ax": cx + 320, "ay": cy + 90,  "spread": 170},
        "eng":   {"ax": cx - 30,  "ay": cy + 280, "spread": 150},
        "bio":   {"ax": cx + 200, "ay": cy + 290, "spread": 100},
    }

    def compute_positions(models, disciplines):
        p = {}
        for d_key in disciplines:
            lst = [m for m in models if m["d"] == d_key]
            c = CLUSTERS[d_key]
            for i, m in enumerate(lst):
                angle = (i / len(lst)) * math.pi * 2 - math.pi / 2
                r = c["spread"] * (0.55 + 0.45 * ((i * 1.7) % 1))
                p[m["id"]] = {"x": c["ax"] + math.cos(angle) * r,
                              "y": c["ay"] + math.sin(angle) * r}
        p["m10"] = {"x": cx, "y": cy}  # flagship pin to centre
        return p

    def compute_edges(models, positions):
        seen, out = set(), []
        for m in models:
            for r in m["related"]:
                key = "-".join(sorted([m["id"], r]))
                if key not in seen and r in positions:
                    seen.add(key)
                    out.append({"a": m["id"], "b": r})
        return out

    positions = compute_positions(MODELS, DISCIPLINES)
    edges = compute_edges(MODELS, positions)

    # ── IMQ Nav (verbatim from docs/mental-models/index.html lines 33-306) ───
    IMQ_NAV_CSS = """
.imq-nav-root{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.imq-nav-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.imq-logo{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}
.imq-logo:hover{color:#fff !important;text-decoration:none !important}
.imq-logo span{color:#3b82f6}
.imq-menu{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.imq-menu > a,.imq-dd-btn{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}
.imq-menu > a:hover,.imq-dd-btn:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-menu > a.active{color:#fff !important;background:rgba(59,130,246,.22);font-weight:600}
.imq-dd{position:relative;display:inline-block}
.imq-dd-menu{display:none;position:absolute;top:100%;left:0;background:#1e293b;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(59,130,246,.18)}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
@media(max-width:768px){
  .imq-nav-root{padding:.55rem 12px}
  .imq-nav-inner{gap:.4rem}
  .imq-menu{width:100%;justify-content:flex-start;gap:.1rem}
  .imq-menu > a,.imq-dd-btn{font-size:.74rem;padding:.32rem .5rem}
  .imq-dd-menu{position:static;display:none;min-width:auto;box-shadow:none;background:rgba(255,255,255,.04);border:none;padding:.1rem 0 .3rem 1rem;margin:.1rem 0}
  .imq-dd.open .imq-dd-menu{display:block}
}"""

    IMQ_NAV_HTML = """<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/">首頁</a>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/research/">個股 DD</a>
          <a href="/pm/">PM 複盤</a>
          <a href="/id/">產業深度 ID</a>
          <a href="/id/theses.html">⭐ 九大非共識</a>
          <a href="/id/tier_matrix.html">🎯 Tier Matrix</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">市場<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/briefing/">每日簡報</a>
          <a href="/weekly/">週報</a>
          <a href="/earnings/">財報分析</a>
          <a href="/markets.html">Markets</a>
          <a href="/sectors.html">Sectors</a>
          <a href="/six-state/">六狀態機</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">工具<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/backtest/">量化回測</a>
          <a href="/qgm/">QGM 美股</a>
          <a href="/qgm-tw/">QGM 台股</a>
          <a href="/screener.html">Screener 美股</a>
          <a href="/screener-tw.html">Screener 台股</a>
        </div>
      </div>
      <a href="/mental-models/" class="active">🧠 心智模型</a>
      <a href="/how-to.html">📘 使用說明</a>
    </nav>
  </div>
</header>
<script>(function(){document.querySelectorAll('.imq-dd-btn').forEach(function(btn){btn.addEventListener('click',function(e){e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open')})});document.addEventListener('click',function(e){if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){d.classList.remove('open')})});})();</script>"""

    # ── SVG: cluster labels ───────────────────────────────────────────────────
    def render_cluster_labels(models, disciplines, positions):
        parts = []
        for d_key, d in disciplines.items():
            lst = [m for m in models if m["d"] == d_key]
            xs = [positions[m["id"]]["x"] for m in lst]
            ys = [positions[m["id"]]["y"] for m in lst]
            label_x = sum(xs) / len(xs)
            min_y = min(ys)
            parts.append(
                f'<g class="cluster-label" data-d="{d_key}">'
                f'<text x="{label_x:.2f}" y="{min_y - 32:.2f}" text-anchor="middle" '
                f'style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;font-weight:700;'
                f'letter-spacing:.18em;text-transform:uppercase;fill:{d["color"]}">'
                f'{d["roman"]} · {d["en"]}</text>'
                f'<text x="{label_x:.2f}" y="{min_y - 16:.2f}" text-anchor="middle" '
                f'style="font-family:\'Inter\',\'Noto Sans TC\',sans-serif;font-size:13px;font-weight:600;fill:#0f172a">'
                f'{d["zh"]} <tspan fill="#94a3b8" font-weight="400">· {d["count"]}</tspan></text>'
                f'</g>'
            )
        return "\n    ".join(parts)

    # ── SVG: edges ────────────────────────────────────────────────────────────
    def render_edges(edges, positions):
        parts = []
        for e in edges:
            pa = positions[e["a"]]
            pb = positions[e["b"]]
            parts.append(
                f'<line class="edge" data-a="{e["a"]}" data-b="{e["b"]}" '
                f'x1="{pa["x"]:.2f}" y1="{pa["y"]:.2f}" '
                f'x2="{pb["x"]:.2f}" y2="{pb["y"]:.2f}" '
                f'stroke="#cbd5e1" stroke-width="0.5" stroke-dasharray="2 3" '
                f'style="transition:all .2s"/>'
            )
        return "\n    ".join(parts)

    # ── SVG: nodes ────────────────────────────────────────────────────────────
    def render_nodes(models, disciplines, positions):
        parts = []
        for m in models:
            p = positions[m["id"]]
            d = disciplines[m["d"]]
            flagship = m.get("flagship", False)
            is_new = m.get("isNew", False)
            r = 26 if flagship else 12
            related_str = ",".join(m["related"])
            glyph = "⚡" if flagship else d["glyph"]
            label_y = r + 18

            new_badge = ""
            if is_new:
                new_badge = (
                    f'<g transform="translate({r - 4},{-r - 2})">'
                    f'<rect x="-3" y="-7" width="22" height="11" rx="2" fill="#dc2626"/>'
                    f'<text x="8" y="1" text-anchor="middle" '
                    f'style="font-family:\'IBM Plex Mono\',monospace;font-size:7px;font-weight:700;'
                    f'letter-spacing:.08em;fill:#fff">NEW</text>'
                    f'</g>'
                )

            flagship_inner = ""
            if flagship:
                flagship_inner = f'<circle r="{r - 7}" fill="#fff" opacity="0.18"/>'

            parts.append(
                f'<g class="node{" flagship" if flagship else ""}" '
                f'data-id="{m["id"]}" data-d="{m["d"]}" data-related="{related_str}" '
                f'transform="translate({p["x"]:.2f},{p["y"]:.2f})" '
                f'style="cursor:pointer;transition:all .2s">'
                f'<circle r="{r}" fill="{d["color"]}" fill-opacity="{"0.95" if flagship else "0.85"}"/>'
                f'{flagship_inner}'
                f'<text class="glyph" text-anchor="middle" dy="{5 if flagship else 4}" '
                f'style="font-family:\'IBM Plex Mono\',monospace;font-weight:700;'
                f'fill:#fff;pointer-events:none">{glyph}</text>'
                f'<text x="0" y="{label_y}" text-anchor="middle" class="node-label" '
                f'style="font-family:\'Inter\',\'Noto Sans TC\',sans-serif;'
                f'fill:#475569;pointer-events:none">{m["zh"]}</text>'
                f'{new_badge}'
                f'</g>'
            )
        return "\n    ".join(parts)

    cluster_labels_svg = render_cluster_labels(MODELS, DISCIPLINES, positions)
    edges_svg = render_edges(edges, positions)
    nodes_svg = render_nodes(MODELS, DISCIPLINES, positions)

    m10_pos = positions["m10"]

    # ── JSON data embed ───────────────────────────────────────────────────────
    json_data = json_mod.dumps({"models": MODELS, "disciplines": DISCIPLINES}, ensure_ascii=False)

    # ── Filter chips HTML ─────────────────────────────────────────────────────
    filter_chips = '<button class="filter-chip active" data-filter="all" style="color:#475569;border-color:#e5e7eb">全部</button>\n'
    for d_key, d in DISCIPLINES.items():
        filter_chips += (
            f'<button class="filter-chip" data-filter="{d_key}" '
            f'style="color:{d["color"]};border-color:#e5e7eb">'
            f'<span>{d["glyph"]}</span>{d["zh"]}</button>\n'
        )

    # ── Legend items ──────────────────────────────────────────────────────────
    legend_items = ""
    for d_key, d in DISCIPLINES.items():
        legend_items += (
            f'<div style="display:flex;align-items:center;gap:5px;margin-bottom:4px">'
            f'<span style="display:inline-block;width:12px;height:12px;border-radius:50%;'
            f'background:{d["color"]};flex-shrink:0"></span>'
            f'<span style="font-family:\'IBM Plex Mono\',monospace;font-size:9px;'
            f'font-weight:700;color:{d["color"]};letter-spacing:.1em">{d["roman"]}</span>'
            f'<span style="font-size:10px;color:#475569">{d["zh"]}</span>'
            f'</div>\n'
        )

    # ── Matrix: server-side band rendering ───────────────────────────────────
    def esc(s):
        if not s:
            return ''
        return (str(s)
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

    def render_matrix_bands(models, disciplines):
        bands_html = ''
        for d_key, d in disciplines.items():
            lst = [m for m in models if m['d'] == d_key]
            # Group rail
            band_rule_style = (
                f'background:linear-gradient(to right,{d["color"]}33,transparent)'
            )
            rail = (
                f'<div class="matrix-band-rail">'
                f'<span class="matrix-band-glyph" style="background:{d["color"]}">{esc(d["glyph"])}</span>'
                f'<div>'
                f'<div class="matrix-band-group-label" style="color:{d["color"]}">GROUP {d["roman"]} · {esc(d["en"].upper())}</div>'
                f'<div class="matrix-band-zh">{esc(d["zh"])} <span class="matrix-band-zh-count">· {d["count"]} models</span></div>'
                f'</div>'
                f'<div class="matrix-band-rule" style="{band_rule_style}"></div>'
                f'</div>'
            )
            # Cells
            cells_html = ''
            for i, m in enumerate(lst):
                flagship = m.get('flagship', False)
                is_new = m.get('isNew', False)
                pos_id = f'{d["roman"]}.{str(i + 1).zfill(2)}'
                flagship_badge = f'<span class="matrix-cell-flagship">★</span>' if flagship else ''
                new_badge = f'<span class="matrix-cell-new">NEW</span>' if is_new else ''
                cell_border_top = f'border-top:3px solid {d["color"]}'
                cells_html += (
                    f'<button class="matrix-cell" data-cell-id="{m["id"]}" data-cell-d="{d_key}" '
                    f'style="{cell_border_top}" '
                    f'data-disc-color="{d["color"]}" data-disc-tint="{d["tint"]}">'
                    f'<div class="matrix-cell-top">'
                    f'<span class="matrix-cell-id">{esc(pos_id)}</span>'
                    f'<div class="matrix-cell-badges">{flagship_badge}{new_badge}</div>'
                    f'</div>'
                    f'<div class="matrix-cell-zh">{esc(m["zh"])}</div>'
                    f'<div class="matrix-cell-en">{esc(m["en"])}</div>'
                    f'<hr class="matrix-cell-divider">'
                    f'<div class="matrix-cell-tag" style="color:{d["color"]}">{esc(m["tag"])}</div>'
                    f'</button>'
                )
            bands_html += (
                f'<div class="matrix-band">'
                f'{rail}'
                f'<div class="matrix-cells">{cells_html}</div>'
                f'</div>'
            )
        return bands_html

    matrix_bands_html = render_matrix_bands(MODELS, DISCIPLINES)

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>心智模型 Latticework · Network + Matrix — InvestMQuest Research</title>
  <meta name="description" content="Munger Latticework 30 心智模型 — Network View + Matrix View">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
/* ── Token system (verbatim from colors_and_type.css) ── */
:root {{
  --imq-bg:           #f7f8fa;
  --imq-bg-soft:      #fafbfc;
  --imq-card:         #ffffff;
  --imq-border:       #e5e7eb;
  --imq-border-soft:  #eef0f3;
  --imq-text:         #0f172a;
  --imq-text-sec:     #475569;
  --imq-text-muted:   #94a3b8;
  --imq-accent:       #2563eb;
  --imq-accent-hover: #1d4ed8;
  --imq-indigo-deep:  #534AB7;
  --imq-green:        #0F6E56;
  --imq-brand:        #1a56db;
  --imq-amber:        #B45309;
  --imq-rose:         #C0392B;
  --imq-shadow-sm:    0 1px 2px rgba(15,23,42,.04);
  --imq-shadow-md:    0 4px 14px rgba(15,23,42,.07);
  --imq-shadow-lg:    0 8px 24px rgba(15,23,42,.08);
  --imq-r-sm:   4px;
  --imq-r-md:   6px;
  --imq-r-lg:   8px;
  --imq-r-xl:   10px;
  --imq-r-2xl:  12px;
  --imq-r-pill: 999px;
  --imq-font-sans: 'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --imq-font-mono: 'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--imq-font-sans);background:var(--imq-bg);color:var(--imq-text);line-height:1.65;font-size:14px;min-height:100vh;-webkit-font-smoothing:antialiased}}
a{{color:var(--imq-accent);text-decoration:none;transition:color .15s}}
a:hover{{color:var(--imq-accent-hover)}}

/* IMQ Nav */
{IMQ_NAV_CSS}

/* ── Top chrome ── */
.top-chrome{{padding:20px 28px 14px;border-bottom:1px solid var(--imq-border-soft);background:var(--imq-card);display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}}
.top-eyebrow{{font-family:var(--imq-font-mono);font-size:10px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--imq-accent);margin-bottom:6px}}
.top-title{{margin:0;font-size:28px;font-weight:800;letter-spacing:-.03em}}
.top-title em{{font-style:italic;font-weight:500;color:#64748b}}
.top-sub{{font-size:12px;color:#64748b;margin-top:4px}}
.top-controls{{display:flex;gap:6px;flex-wrap:wrap;align-items:center;justify-content:flex-end}}

/* ── Filter chips ── */
.filter-chip{{
  padding:6px 11px;font-size:11px;font-family:var(--imq-font-mono);font-weight:600;letter-spacing:.05em;
  background:#fff;border:1px solid var(--imq-border);border-radius:var(--imq-r-pill);
  cursor:pointer;display:inline-flex;align-items:center;gap:5px;transition:all .15s
}}
.filter-chip.active{{color:#fff !important;border-color:currentColor}}
.filter-chip span{{font-size:11px}}

/* ── Lollapalooza button ── */
.lolla-btn{{
  padding:6px 11px;font-size:11px;font-family:var(--imq-font-mono);font-weight:700;letter-spacing:.08em;
  background:#fff;color:#0f172a;border:1px solid #0f172a;border-radius:var(--imq-r-pill);
  cursor:pointer;margin-left:8px;transition:all .15s
}}
.lolla-btn.active{{background:#0f172a;color:#fff}}
.view-reset-btn{{
  padding:6px 11px;font-size:11px;font-family:var(--imq-font-mono);font-weight:600;letter-spacing:.05em;
  background:#fff;color:#475569;border:1px solid var(--imq-border);border-radius:var(--imq-r-pill);
  cursor:pointer;transition:all .15s
}}
.view-reset-btn:hover{{color:#0f172a;border-color:#0f172a}}

/* ── Main layout ── */
.main-grid{{display:grid;grid-template-columns:1fr 380px;min-height:820px}}
.canvas-col{{position:relative;border:1px solid var(--imq-border);background:transparent}}
.detail-col{{background:var(--imq-card);padding:24px 24px 32px;overflow:auto;max-height:900px}}

/* ── SVG node states ── */
.node{{cursor:pointer;transition:opacity .2s}}
.node.dimmed{{opacity:.28}}
.node.filtered-out{{opacity:.12}}
.node circle{{transition:r .15s,fill-opacity .15s}}
.node .glyph{{font-size:12px;transition:font-size .15s}}
.node .node-label{{font-size:13.5px;font-weight:500;transition:font-size .15s,font-weight .15s,fill .15s}}
.node.flagship .glyph{{font-size:17px}}
.node.flagship .node-label{{font-size:16px;font-weight:700}}
.node.hovered:not(.flagship) circle,.node.selected:not(.flagship) circle{{r:18}}
.node.hovered:not(.flagship) .glyph,.node.selected:not(.flagship) .glyph{{font-size:16px}}
.node.hovered:not(.flagship) .node-label,.node.selected:not(.flagship) .node-label{{font-size:17px;font-weight:700;fill:#0f172a}}
.node.flagship.hovered circle,.node.flagship.selected circle{{r:32}}
.node.flagship.hovered .glyph,.node.flagship.selected .glyph{{font-size:22px}}
.node.flagship.hovered .node-label,.node.flagship.selected .node-label{{font-size:20px;fill:#0f172a}}
.edge{{transition:stroke .2s,stroke-width .2s,stroke-dasharray .2s,opacity .2s}}
.edge.active{{stroke:#0f172a !important;stroke-width:1.4px !important;stroke-dasharray:0 !important}}
.edge.dimmed{{opacity:.15}}
.edge.filtered-out{{opacity:.05}}

/* ── Detail panel ── */
.panel-discipline-badge{{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;color:#fff;font-family:var(--imq-font-mono);font-size:14px;font-weight:700}}
.panel-tag-new{{font-family:var(--imq-font-mono);font-size:9px;font-weight:700;letter-spacing:.12em;padding:1px 6px;background:#dc2626;color:#fff;border-radius:3px}}
.panel-tag-flagship{{font-family:var(--imq-font-mono);font-size:9px;font-weight:700;letter-spacing:.12em;padding:1px 6px;background:#fbbf24;color:#0f172a;border-radius:3px}}
.panel-id-tag{{font-family:var(--imq-font-mono);font-size:11px;color:#94a3b8;letter-spacing:.04em}}
.panel-zh{{margin:4px 0 2px;font-size:28px;font-weight:800;letter-spacing:-.03em}}
.panel-en{{font-size:13px;font-style:italic;color:#64748b;font-weight:500}}
.panel-body{{margin-top:18px;padding:12px 14px;border-left:3px solid;border-radius:4px;font-size:13px;line-height:1.6;color:#1e293b}}
.panel-quote{{margin:18px 0 0;padding:0 0 0 12px;border-left:2px solid var(--imq-border);font-size:12px;line-height:1.6;color:#475569;font-style:italic}}
.panel-section-label{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#94a3b8;margin-bottom:8px;margin-top:22px}}
.case-row{{display:flex;gap:8px;padding:7px 0;font-size:12.5px;line-height:1.55}}
.case-row + .case-row{{border-top:1px dashed var(--imq-border-soft)}}
.case-num{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;min-width:18px}}
.related-chips{{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}}
.related-chip{{display:inline-flex;align-items:center;gap:5px;padding:5px 10px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer;font-family:var(--imq-font-sans);border:1px solid;transition:opacity .15s}}
.related-chip:hover{{opacity:.8}}
.ask-box{{margin-top:22px;padding:14px;background:#0f172a;color:#fff;border-radius:8px}}
.ask-label{{font-family:var(--imq-font-mono);font-size:9px;font-weight:700;letter-spacing:.18em;color:#fbbf24;margin-bottom:6px}}
.ask-text{{font-size:13px;line-height:1.55}}

/* ── Legend ── */
.legend-box{{position:absolute;bottom:16px;left:24px;background:#fff;border:1px solid var(--imq-border);border-radius:8px;padding:10px 14px;font-size:11px;box-shadow:var(--imq-shadow-sm)}}
.legend-title{{font-family:var(--imq-font-mono);font-size:9px;font-weight:700;letter-spacing:.15em;color:#94a3b8;margin-bottom:8px}}
.legend-row{{display:flex;align-items:center;gap:6px;margin-bottom:4px}}

/* ── Lollapalooza meter ── */
.lolla-meter{{position:absolute;bottom:16px;right:24px;background:#0f172a;color:#fff;border-radius:10px;padding:14px 18px;min-width:280px;box-shadow:0 8px 24px rgba(15,23,42,.18);display:none}}
.lolla-meter.visible{{display:block}}
.lolla-meter-label{{font-family:var(--imq-font-mono);font-size:9px;font-weight:700;letter-spacing:.18em;color:#fbbf24;margin-bottom:6px}}
.lolla-count-row{{display:flex;align-items:baseline;gap:8px}}
.lolla-count{{font-family:var(--imq-font-mono);font-size:32px;font-weight:700;line-height:1}}
.lolla-count-sub{{font-size:11px;color:#94a3b8}}
.lolla-verdict{{margin-top:8px;font-size:11px;line-height:1.5}}
.lolla-picks{{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px}}
.lolla-pick-chip{{font-size:10px;padding:2px 7px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}}

/* ── Matrix view ── */
.matrix-section{{background:var(--imq-bg)}}
.matrix-section-divider{{max-width:1140px;margin:0 auto;padding:48px 32px 0}}
.matrix-eyebrow{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;letter-spacing:.22em;color:var(--imq-accent);margin-bottom:8px}}
.matrix-section-title{{margin:0 0 6px;font-size:28px;font-weight:800;letter-spacing:-.03em}}
.matrix-section-sub{{margin:0 0 24px;font-size:13px;color:#64748b;max-width:680px}}
.matrix-wrap{{max-width:1240px;margin:0 auto;padding:0 32px 48px}}
.matrix-inner{{background:#fff;border:1px solid var(--imq-border);border-radius:12px;overflow:hidden;box-shadow:var(--imq-shadow-sm)}}
.matrix-toolbar{{padding:14px 20px;background:#fafbfc;border-bottom:1px solid #eef0f3;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}}
.matrix-toolbar-label{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;letter-spacing:.18em;color:#94a3b8}}
.matrix-lolla-btn{{padding:6px 12px;font-size:11px;font-family:var(--imq-font-mono);font-weight:700;letter-spacing:.1em;background:#fff;color:#0f172a;border:1px solid #0f172a;border-radius:6px;cursor:pointer;transition:all .15s}}
.matrix-lolla-btn.active{{background:#0f172a;color:#fbbf24;border-color:#0f172a}}
.matrix-lolla-strip{{background:#0f172a;color:#fff;padding:14px 32px;display:none;align-items:center;gap:24px;flex-wrap:wrap}}
.matrix-lolla-strip.visible{{display:flex}}
.matrix-lolla-strip-count-label{{font-family:var(--imq-font-mono);font-size:9px;letter-spacing:.2em;color:#fbbf24;margin-bottom:2px}}
.matrix-lolla-strip-count{{font-family:var(--imq-font-mono);font-size:26px;font-weight:700;line-height:1}}
.matrix-lolla-bar-track{{height:6px;background:#1e293b;border-radius:3px;overflow:hidden;margin-bottom:4px}}
.matrix-lolla-bar-fill{{height:100%;border-radius:3px;transition:all .25s;background:#3b82f6}}
.matrix-lolla-status{{font-family:var(--imq-font-mono);font-size:11px;color:#cbd5e1}}
.matrix-lolla-pills{{display:flex;flex-wrap:wrap;gap:4px;max-width:380px}}
.matrix-lolla-pill{{font-size:10px;padding:3px 8px;border-radius:999px;background:#1e293b;border:1px solid #334155;color:#fff}}
.matrix-bands{{padding:28px 32px 40px}}
.matrix-band{{margin-bottom:22px}}
.matrix-band-rail{{display:flex;align-items:center;gap:14px;margin-bottom:10px}}
.matrix-band-glyph{{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;color:#fff;font-family:var(--imq-font-mono);font-weight:700;font-size:14px;border-radius:4px;flex-shrink:0}}
.matrix-band-group-label{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;margin-bottom:2px}}
.matrix-band-zh{{font-size:16px;font-weight:700;letter-spacing:-.02em}}
.matrix-band-zh-count{{color:#94a3b8;font-weight:400;font-size:13px}}
.matrix-band-rule{{flex:1;height:1px}}
.matrix-cells{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px}}
.matrix-cell{{text-align:left;background:#fff;border:1px solid #e5e7eb;border-radius:4px;padding:10px 12px 12px;cursor:pointer;position:relative;transition:background .15s,border-color .15s;font-family:inherit;width:100%}}
.matrix-cell:hover{{border-color:currentColor}}
.matrix-cell-top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px}}
.matrix-cell-id{{font-family:var(--imq-font-mono);font-size:10px;font-weight:600;letter-spacing:.05em;color:#94a3b8}}
.matrix-cell-badges{{display:flex;gap:3px;align-items:center}}
.matrix-cell-flagship{{font-size:9px;color:#fbbf24}}
.matrix-cell-new{{font-family:var(--imq-font-mono);font-size:7px;font-weight:700;letter-spacing:.1em;padding:1px 4px;background:#dc2626;color:#fff;border-radius:2px}}
.matrix-cell-zh{{font-size:16px;font-weight:700;letter-spacing:-.02em;line-height:1.15;color:#0f172a}}
.matrix-cell-en{{font-size:10px;color:#64748b;font-style:italic;margin-top:2px;font-family:'Inter',sans-serif}}
.matrix-cell-divider{{height:0;border:none;border-top:1px dashed #eef0f3;margin:8px 0 0}}
.matrix-cell-tag{{font-family:var(--imq-font-mono);font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding-top:6px}}
/* picked state */
.matrix-cell.picked .matrix-cell-id{{color:rgba(255,255,255,.75)}}
.matrix-cell.picked .matrix-cell-zh{{color:#fff}}
.matrix-cell.picked .matrix-cell-en{{color:rgba(255,255,255,.8)}}
.matrix-cell.picked .matrix-cell-divider{{border-top-color:rgba(255,255,255,.2)}}
.matrix-cell.picked .matrix-cell-tag{{color:rgba(255,255,255,.7)}}
.matrix-cell.picked .matrix-cell-flagship{{color:#fff}}
/* Matrix modal */
.matrix-modal{{position:fixed;inset:0;background:rgba(15,23,42,.55);backdrop-filter:blur(2px);z-index:1000;display:flex;align-items:center;justify-content:center;padding:32px}}
.matrix-modal[hidden],.matrix-modal[style*="display:none"]{{display:none!important}}
.matrix-modal-box{{background:#fff;max-width:760px;width:100%;max-height:88vh;overflow:auto;border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,.3);position:relative}}
.matrix-modal-header{{padding:26px 32px 22px;border-bottom:3px solid transparent}}
.matrix-modal-header-top{{display:flex;justify-content:space-between;align-items:flex-start}}
.matrix-modal-discipline-row{{display:flex;align-items:center;gap:8px;margin-bottom:8px}}
.matrix-modal-disc-badge{{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;color:#fff;font-family:var(--imq-font-mono);font-weight:700;font-size:12px;border-radius:3px;flex-shrink:0}}
.matrix-modal-disc-label{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;letter-spacing:.2em}}
.matrix-modal-tag-label{{font-family:var(--imq-font-mono);font-size:10px;color:#94a3b8;letter-spacing:.1em}}
.matrix-modal-zh{{margin:0 0 2px;font-size:32px;font-weight:800;letter-spacing:-.03em}}
.matrix-modal-en{{font-size:14px;font-style:italic;color:#64748b}}
.matrix-modal-close{{background:transparent;border:1px solid #e5e7eb;width:32px;height:32px;border-radius:6px;font-size:16px;cursor:pointer;color:#475569;flex-shrink:0;display:flex;align-items:center;justify-content:center}}
.matrix-modal-body{{padding:24px 32px 32px}}
.matrix-modal-desc{{margin:0 0 16px;font-size:14px;line-height:1.65;color:#1e293b;padding:12px 16px;border-left:3px solid transparent;border-radius:4px}}
.matrix-modal-quote{{margin:0 0 24px;padding:12px 16px;border-left:3px solid transparent;font-size:13px;font-style:italic;color:#475569;line-height:1.55;background:#f9fafb}}
.matrix-modal-grid{{display:grid;grid-template-columns:1fr 280px;gap:28px}}
@media(max-width:680px){{.matrix-modal-grid{{grid-template-columns:1fr}}}}
.matrix-modal-section-label{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#94a3b8;margin-bottom:8px}}
.matrix-modal-case{{display:flex;gap:8px;padding:6px 0;font-size:12.5px;line-height:1.55}}
.matrix-modal-case+.matrix-modal-case{{border-top:1px dashed #eef0f3}}
.matrix-modal-case-num{{font-family:var(--imq-font-mono);font-size:10px;font-weight:700;min-width:18px}}
.matrix-modal-related-chips{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}}
.matrix-modal-related-chip{{display:inline-flex;align-items:center;gap:4px;padding:4px 9px;border-radius:4px;font-size:11px;font-weight:600;cursor:pointer;font-family:var(--imq-font-sans);border:1px solid;transition:opacity .15s;background:transparent}}
.matrix-modal-related-chip:hover{{opacity:.8}}
.matrix-modal-ask{{padding:12px 14px;background:#0f172a;color:#fff;border-radius:6px}}
.matrix-modal-ask-label{{font-family:var(--imq-font-mono);font-size:9px;font-weight:700;letter-spacing:.18em;color:#fbbf24;margin-bottom:6px}}
.matrix-modal-ask-text{{font-size:12.5px;line-height:1.55}}
  </style>
</head>
<body>

{IMQ_NAV_HTML}

<!-- Top chrome -->
<div class="top-chrome">
  <div>
    <div class="top-eyebrow">MUNGER LATTICEWORK · 30 MODELS · NETWORK VIEW</div>
    <h1 class="top-title">心智模型 <em>Mental Models</em></h1>
    <div class="top-sub">跨學科框架網絡 · hover 節點高亮鄰居 · 點擊查看詳情</div>
  </div>
  <div class="top-controls">
    {filter_chips}
    <button class="view-reset-btn" id="viewResetBtn" title="重置視圖（拖移背景平移、滾輪縮放、雙擊背景重置）">⟲ 重置視圖</button>
    <button class="lolla-btn" id="lollaToggle">⚡ LOLLAPALOOZA</button>
  </div>
</div>

<!-- Main 2-col grid -->
<div class="main-grid">
  <!-- Left: SVG canvas -->
  <div class="canvas-col">
    <svg id="networkSvg" viewBox="0 0 {W} {H + 110}" style="width:100%;height:auto;display:block;background:transparent">
      <defs>
        <pattern id="latticeGrid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#eef0f3" stroke-width="0.5"/>
        </pattern>
        <radialGradient id="lollaGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#534AB7" stop-opacity="0.18"/>
          <stop offset="100%" stop-color="#534AB7" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="{W}" height="{H + 110}" fill="url(#latticeGrid)"/>

      <!-- Cluster labels -->
      <g id="clusterLabels">
    {cluster_labels_svg}
      </g>

      <!-- Lollapalooza glow -->
      <circle cx="{m10_pos["x"]:.2f}" cy="{m10_pos["y"]:.2f}" r="120" fill="url(#lollaGlow)"/>

      <!-- Edges -->
      <g id="edgesGroup">
    {edges_svg}
      </g>

      <!-- Nodes -->
      <g id="nodesGroup">
    {nodes_svg}
      </g>
    </svg>

    <!-- Legend -->
    <div class="legend-box">
      <div class="legend-title">圖例 · LEGEND</div>
      {legend_items}
      <div class="legend-row" style="margin-top:6px;padding-top:6px;border-top:1px solid var(--imq-border-soft)">
        <span style="display:inline-block;width:18px;height:0;border-top:1.4px solid #0f172a"></span>
        <span style="font-size:10px;color:#475569">關聯邊</span>
      </div>
      <div class="legend-row">
        <span style="font-size:13px">⚡</span>
        <span style="font-size:10px;color:#475569">Lollapalooza 中樞</span>
      </div>
    </div>

    <!-- Lollapalooza meter -->
    <div class="lolla-meter" id="lollaMeter">
      <div class="lolla-meter-label">⚡ LOLLAPALOOZA · 共振計</div>
      <div class="lolla-count-row">
        <span class="lolla-count" id="lollaCount">0</span>
        <span class="lolla-count-sub">個偏誤同向</span>
      </div>
      <div class="lolla-verdict" id="lollaVerdict">點選 2+ 個節點觀察共振強度。</div>
      <div class="lolla-picks" id="lollaPicks"></div>
    </div>
  </div>

  <!-- Right: detail panel -->
  <aside class="detail-col" id="detailPanel">
    <!-- rendered by JS -->
  </aside>
</div>

<!-- Embedded data -->
<script id="mental-models-data" type="application/json">
{json_data}
</script>

<script>
(function() {{
  // ── Data ──────────────────────────────────────────────────────────────────
  var raw = JSON.parse(document.getElementById('mental-models-data').textContent);
  var MODELS = raw.models;
  var DISCIPLINES = raw.disciplines;
  function getModel(id) {{ return MODELS.find(function(m){{return m.id===id}}); }}

  // ── State ─────────────────────────────────────────────────────────────────
  var selectedId = 'm10';
  var hoveredId = null;
  var filter = 'all';
  var lollaMode = false;
  var lollaPicks = new Set();

  // ── DOM refs ──────────────────────────────────────────────────────────────
  var svg = document.getElementById('networkSvg');
  var detailPanel = document.getElementById('detailPanel');
  var lollaToggle = document.getElementById('lollaToggle');
  var lollaMeter = document.getElementById('lollaMeter');
  var lollaCountEl = document.getElementById('lollaCount');
  var lollaVerdictEl = document.getElementById('lollaVerdict');
  var lollaPicksEl = document.getElementById('lollaPicks');
  var filterChips = document.querySelectorAll('.filter-chip');
  var clusterLabels = document.querySelectorAll('.cluster-label');

  // ── Helpers ───────────────────────────────────────────────────────────────
  function getNeighbors(id) {{
    var m = getModel(id);
    if (!m) return new Set([]);
    var s = new Set([id]);
    (m.related || []).forEach(function(r){{ s.add(r); }});
    return s;
  }}

  function allNodes() {{ return svg.querySelectorAll('.node'); }}
  function allEdges() {{ return svg.querySelectorAll('.edge'); }}

  // ── Hover logic ───────────────────────────────────────────────────────────
  function applyHoverState(activeId) {{
    var neighbors = getNeighbors(activeId);
    allNodes().forEach(function(node) {{
      var nid = node.getAttribute('data-id');
      node.classList.toggle('dimmed', !neighbors.has(nid));
      node.classList.toggle('hovered', nid === activeId);
    }});
    allEdges().forEach(function(edge) {{
      var a = edge.getAttribute('data-a');
      var b = edge.getAttribute('data-b');
      var active = neighbors.has(a) && neighbors.has(b);
      edge.classList.toggle('active', active);
      edge.classList.toggle('dimmed', !active);
    }});
  }}

  function clearHoverState() {{
    allNodes().forEach(function(n){{ n.classList.remove('dimmed'); n.classList.remove('hovered'); }});
    allEdges().forEach(function(e){{ e.classList.remove('active','dimmed'); }});
  }}

  // ── Filter logic ──────────────────────────────────────────────────────────
  function applyFilter(f) {{
    allNodes().forEach(function(node) {{
      var d = node.getAttribute('data-d');
      var out = (f !== 'all' && d !== f);
      node.classList.toggle('filtered-out', out);
    }});
    allEdges().forEach(function(edge) {{
      var a = edge.getAttribute('data-a');
      var b = edge.getAttribute('data-b');
      var ma = getModel(a), mb = getModel(b);
      var visible = (f === 'all' || (ma && ma.d === f) || (mb && mb.d === f));
      edge.classList.toggle('filtered-out', !visible);
    }});
    // Cluster labels
    clusterLabels.forEach(function(label) {{
      var d = label.getAttribute('data-d');
      label.style.opacity = (f === 'all' || f === d) ? '1' : '0.2';
    }});
  }}

  // ── Lollapalooza meter ────────────────────────────────────────────────────
  function updateLollaMeter() {{
    var count = lollaPicks.size;
    lollaCountEl.textContent = count;
    var verdict = '';
    if (count === 0) verdict = '點選 2+ 個節點觀察共振強度。';
    else if (count === 1) verdict = '單一偏誤 — 一般風險。';
    else if (count === 2) verdict = '雙偏誤疊加 — 注意。';
    else if (count < 5) verdict = '⚠ 三+ 偏誤同向 — Munger 警報。';
    else verdict = '⚠⚠ 多模型共振 — 災難級風險（FTX / 泡沫）。';
    lollaVerdictEl.textContent = verdict;
    lollaVerdictEl.style.color = count >= 3 ? '#fca5a5' : '#cbd5e1';

    lollaPicksEl.innerHTML = '';
    lollaPicks.forEach(function(id) {{
      var m = getModel(id);
      if (!m) return;
      var chip = document.createElement('span');
      chip.className = 'lolla-pick-chip';
      chip.textContent = m.zh;
      lollaPicksEl.appendChild(chip);
    }});
  }}

  // ── Right panel render ────────────────────────────────────────────────────
  function renderPanel(id) {{
    var m = getModel(id);
    if (!m) return;
    var d = DISCIPLINES[m.d];
    var newBadge = m.isNew ? '<span class="panel-tag-new">NEW</span>' : '';
    var flagshipBadge = m.flagship ? '<span class="panel-tag-flagship">★ FLAGSHIP</span>' : '';

    var casesHtml = (m.cases || []).map(function(c, i) {{
      return '<div class="case-row">'
        + '<span class="case-num" style="color:' + d.color + '">' + String(i+1).padStart(2,'0') + '</span>'
        + '<span style="color:#1e293b">' + escHtml(c) + '</span>'
        + '</div>';
    }}).join('');

    var relatedHtml = (m.related || []).map(function(rid) {{
      var r = getModel(rid);
      if (!r) return '';
      var rd = DISCIPLINES[r.d];
      return '<button class="related-chip" data-related-id="' + rid + '" '
        + 'style="background:' + rd.tint + ';color:' + rd.color + ';border-color:' + rd.color + '33">'
        + '<span style="font-family:var(--imq-font-mono)">' + escHtml(rd.glyph) + '</span>'
        + escHtml(r.zh)
        + '</button>';
    }}).join('');

    detailPanel.innerHTML = '<div>'
      + '<div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">'
      + '<span class="panel-discipline-badge" style="background:' + d.color + '">' + escHtml(d.glyph) + '</span>'
      + '<span style="font-family:var(--imq-font-mono);font-size:10px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:' + d.color + '">' + escHtml(d.zh) + ' · ' + escHtml(d.en) + '</span>'
      + newBadge + flagshipBadge
      + '</div>'
      + '<div class="panel-id-tag">' + escHtml(m.id.toUpperCase()) + ' · ' + escHtml(m.tag) + '</div>'
      + '<h2 class="panel-zh">' + escHtml(m.zh) + '</h2>'
      + '<div class="panel-en">' + escHtml(m.en) + '</div>'
      + '<div class="panel-body" style="background:' + d.tint + ';border-left-color:' + d.color + '">' + escHtml(m.body) + '</div>'
      + '<blockquote class="panel-quote">' + escHtml(m.quote) + '</blockquote>'
      + '<div class="panel-section-label">投資實例 · CASES</div>'
      + casesHtml
      + '<div class="panel-section-label">關聯模型 · RELATED</div>'
      + '<div class="related-chips">' + relatedHtml + '</div>'
      + '<div class="ask-box"><div class="ask-label">? 問自己 · ASK YOURSELF</div>'
      + '<div class="ask-text">' + escHtml(m.ask) + '</div></div>'
      + '</div>';

    // wire up related chip clicks
    detailPanel.querySelectorAll('.related-chip').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        var rid = btn.getAttribute('data-related-id');
        selectNode(rid);
      }});
    }});
  }}

  function escHtml(s) {{
    if (!s) return '';
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }}

  // ── Select node ───────────────────────────────────────────────────────────
  function selectNode(id) {{
    selectedId = id;
    allNodes().forEach(function(node) {{
      node.classList.toggle('selected', node.getAttribute('data-id') === id);
    }});
    renderPanel(id);
  }}

  // ── Node events ───────────────────────────────────────────────────────────
  allNodes().forEach(function(node) {{
    var id = node.getAttribute('data-id');

    node.addEventListener('mouseenter', function() {{
      hoveredId = id;
      applyHoverState(id);
    }});

    node.addEventListener('mouseleave', function() {{
      hoveredId = null;
      clearHoverState();
    }});

    node.addEventListener('click', function() {{
      if (lollaMode) {{
        if (lollaPicks.has(id)) {{
          lollaPicks.delete(id);
          node.querySelector('circle').style.strokeWidth = '';
          node.querySelector('circle').style.stroke = '';
        }} else {{
          lollaPicks.add(id);
          node.querySelector('circle').style.stroke = '#0f172a';
          node.querySelector('circle').style.strokeWidth = '2';
        }}
        updateLollaMeter();
      }} else {{
        selectNode(id);
      }}
    }});
  }});

  // ── Filter chips ──────────────────────────────────────────────────────────
  filterChips.forEach(function(chip) {{
    chip.addEventListener('click', function() {{
      filter = chip.getAttribute('data-filter');
      filterChips.forEach(function(c) {{
        c.classList.remove('active');
        // reset inline color applied by active state
        var f = c.getAttribute('data-filter');
        var disc = DISCIPLINES[f];
        c.style.background = '';
        if (disc) c.style.color = disc.color;
        else c.style.color = '#475569';
      }});
      chip.classList.add('active');
      // set active background
      var activeDisc = DISCIPLINES[filter];
      if (activeDisc) {{
        chip.style.background = activeDisc.color;
        chip.style.color = '#fff';
      }} else {{
        chip.style.background = '#475569';
        chip.style.color = '#fff';
      }}
      applyFilter(filter);
    }});
  }});

  // ── Lollapalooza toggle ───────────────────────────────────────────────────
  lollaToggle.addEventListener('click', function() {{
    lollaMode = !lollaMode;
    lollaPicks.clear();
    // reset any ring strokes
    allNodes().forEach(function(node) {{
      var circle = node.querySelector('circle');
      if (circle) {{ circle.style.stroke = ''; circle.style.strokeWidth = ''; }}
    }});
    lollaToggle.classList.toggle('active', lollaMode);
    lollaToggle.textContent = lollaMode ? '✓ LOLLAPALOOZA' : '⚡ LOLLAPALOOZA';
    lollaMeter.classList.toggle('visible', lollaMode);
    if (lollaMode) updateLollaMeter();
  }});

  // ── Pan & Zoom ────────────────────────────────────────────────────────────
  var VB_W = {W};
  var VB_H = {H} + 110;
  var view = {{ x: 0, y: 0, zoom: 1 }};
  var drag = {{ active: false, sx: 0, sy: 0, px: 0, py: 0, moved: false }};

  function applyView() {{
    var w = VB_W / view.zoom;
    var h = VB_H / view.zoom;
    svg.setAttribute('viewBox', view.x + ' ' + view.y + ' ' + w + ' ' + h);
  }}
  function resetView() {{ view.x = 0; view.y = 0; view.zoom = 1; applyView(); }}

  svg.style.cursor = 'grab';
  svg.style.touchAction = 'none';

  svg.addEventListener('mousedown', function(e) {{
    if (e.target.closest('.node')) return;
    drag.active = true;
    drag.moved = false;
    drag.sx = e.clientX; drag.sy = e.clientY;
    drag.px = view.x; drag.py = view.y;
    svg.style.cursor = 'grabbing';
    e.preventDefault();
  }});
  window.addEventListener('mousemove', function(e) {{
    if (!drag.active) return;
    var rect = svg.getBoundingClientRect();
    var sx = (VB_W / view.zoom) / rect.width;
    var sy = (VB_H / view.zoom) / rect.height;
    var dx = (e.clientX - drag.sx) * sx;
    var dy = (e.clientY - drag.sy) * sy;
    if (Math.abs(dx) + Math.abs(dy) > 2) drag.moved = true;
    view.x = drag.px - dx;
    view.y = drag.py - dy;
    applyView();
  }});
  window.addEventListener('mouseup', function() {{
    if (drag.active) {{ drag.active = false; svg.style.cursor = 'grab'; }}
  }});

  svg.addEventListener('wheel', function(e) {{
    e.preventDefault();
    var rect = svg.getBoundingClientRect();
    var mx = (e.clientX - rect.left) / rect.width;
    var my = (e.clientY - rect.top) / rect.height;
    var oldZ = view.zoom;
    var factor = e.deltaY < 0 ? 1.12 : 1/1.12;
    var newZ = Math.max(0.4, Math.min(4, oldZ * factor));
    var oldW = VB_W / oldZ, oldH = VB_H / oldZ;
    var newW = VB_W / newZ, newH = VB_H / newZ;
    view.x += (oldW - newW) * mx;
    view.y += (oldH - newH) * my;
    view.zoom = newZ;
    applyView();
  }}, {{ passive: false }});

  // Double-click on background = reset view
  svg.addEventListener('dblclick', function(e) {{
    if (e.target.closest('.node')) return;
    resetView();
  }});

  // Reset button
  var resetBtn = document.getElementById('viewResetBtn');
  if (resetBtn) resetBtn.addEventListener('click', resetView);

  // ── Init ──────────────────────────────────────────────────────────────────
  renderPanel(selectedId);
  selectNode(selectedId);
}})();
</script>

<!-- ═══════════════════════════════════════════════════════════════════════
     II · MATRIX VIEW  (Phase 2 — Direction C Periodic Table)
     ═══════════════════════════════════════════════════════════════════════ -->
<section class="matrix-section">

  <!-- Section divider -->
  <div class="matrix-section-divider">
    <div class="matrix-eyebrow">II · MATRIX VIEW</div>
    <h2 class="matrix-section-title">Tier Matrix · 元素表式呈現</h2>
    <p class="matrix-section-sub">同樣 30 個模型，按學科分組成五個橫帶；點擊單元格開啟完整定義；啟用 Lollapalooza 可同時挑選多個觀察共振。</p>
  </div>

  <div class="matrix-wrap">
    <div class="matrix-inner">

      <!-- Toolbar -->
      <div class="matrix-toolbar">
        <span class="matrix-toolbar-label">30 ELEMENTS · 5 GROUPS · 點擊任一格查看完整內容</span>
        <button class="matrix-lolla-btn" id="matrixLollaBtn">⚡ LOLLAPALOOZA</button>
      </div>

      <!-- Lollapalooza readout strip (hidden until picker active) -->
      <div class="matrix-lolla-strip" id="matrixLollaStrip">
        <div>
          <div class="matrix-lolla-strip-count-label">RESONANCE</div>
          <div class="matrix-lolla-strip-count" id="matrixLollaCount">0</div>
        </div>
        <div style="flex:1;min-width:160px">
          <div class="matrix-lolla-bar-track">
            <div class="matrix-lolla-bar-fill" id="matrixLollaBarFill" style="width:0%"></div>
          </div>
          <div class="matrix-lolla-status" id="matrixLollaStatus">點選多個元素 → 觀察偏誤共振強度</div>
        </div>
        <div class="matrix-lolla-pills" id="matrixLollaPills"></div>
      </div>

      <!-- 5 Discipline bands (server-side rendered) -->
      <div class="matrix-bands">
{matrix_bands_html}
      </div>

    </div><!-- /.matrix-inner -->
  </div><!-- /.matrix-wrap -->

</section>

<!-- Matrix modal (single instance, hidden by default) -->
<div class="matrix-modal" id="matrixModal" style="display:none" role="dialog" aria-modal="true" aria-labelledby="matrixModalZh">
  <div class="matrix-modal-box" id="matrixModalBox">
    <div class="matrix-modal-header" id="matrixModalHeader">
      <div class="matrix-modal-header-top">
        <div>
          <div class="matrix-modal-discipline-row" id="matrixModalDisciplineRow"></div>
          <h2 class="matrix-modal-zh" id="matrixModalZh"></h2>
          <div class="matrix-modal-en" id="matrixModalEn"></div>
        </div>
        <button class="matrix-modal-close" id="matrixModalClose" aria-label="關閉">×</button>
      </div>
    </div>
    <div class="matrix-modal-body">
      <p class="matrix-modal-desc" id="matrixModalDesc"></p>
      <blockquote class="matrix-modal-quote" id="matrixModalQuote"></blockquote>
      <div class="matrix-modal-grid">
        <div>
          <div class="matrix-modal-section-label">投資實例 · CASES</div>
          <div id="matrixModalCases"></div>
        </div>
        <div>
          <div class="matrix-modal-section-label">關聯模型 · RELATED</div>
          <div class="matrix-modal-related-chips" id="matrixModalRelated"></div>
          <div class="matrix-modal-ask" id="matrixModalAsk">
            <div class="matrix-modal-ask-label">? 問自己 · ASK YOURSELF</div>
            <div class="matrix-modal-ask-text" id="matrixModalAskText"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
(function matrixView() {{
  // ── Read data from the SAME JSON block Phase 1 already embedded ───────────
  var _raw = JSON.parse(document.getElementById('mental-models-data').textContent);
  var MMODELS = _raw.models;
  var MDISCIPLINES = _raw.disciplines;

  function mGetModel(id) {{ return MMODELS.find(function(m) {{ return m.id === id; }}); }}
  function mEsc(s) {{
    if (!s) return '';
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }}

  // ── State (completely separate from Network view state) ───────────────────
  var mOpenId = null;
  var mPicks = new Set();
  var mPickerOn = false;

  // ── DOM refs ──────────────────────────────────────────────────────────────
  var mLollaBtn = document.getElementById('matrixLollaBtn');
  var mLollaStrip = document.getElementById('matrixLollaStrip');
  var mLollaCount = document.getElementById('matrixLollaCount');
  var mLollaBarFill = document.getElementById('matrixLollaBarFill');
  var mLollaStatus = document.getElementById('matrixLollaStatus');
  var mLollaPills = document.getElementById('matrixLollaPills');
  var mModal = document.getElementById('matrixModal');
  var mModalHeader = document.getElementById('matrixModalHeader');
  var mModalDisciplineRow = document.getElementById('matrixModalDisciplineRow');
  var mModalZh = document.getElementById('matrixModalZh');
  var mModalEn = document.getElementById('matrixModalEn');
  var mModalDesc = document.getElementById('matrixModalDesc');
  var mModalQuote = document.getElementById('matrixModalQuote');
  var mModalCases = document.getElementById('matrixModalCases');
  var mModalRelated = document.getElementById('matrixModalRelated');
  var mModalAskText = document.getElementById('matrixModalAskText');
  var mModalClose = document.getElementById('matrixModalClose');

  // ── Update lolla readout strip ────────────────────────────────────────────
  function mUpdateStrip() {{
    var n = mPicks.size;
    mLollaCount.textContent = n;
    var pct = Math.min(100, n * 16);
    mLollaBarFill.style.width = pct + '%';
    var barColor = n >= 5 ? '#dc2626' : (n >= 3 ? '#fbbf24' : '#3b82f6');
    mLollaBarFill.style.background = barColor;
    var status = '';
    if (n === 0) status = '點選多個元素 → 觀察偏誤共振強度';
    else if (n <= 2) status = '一般範圍：單一/雙偏誤';
    else if (n <= 4) status = '⚠ Munger 警報區：三+ 偏誤同向';
    else status = '⚠⚠ 災難級共振：FTX / 泡沫等級';
    mLollaStatus.textContent = status;

    mLollaPills.innerHTML = '';
    mPicks.forEach(function(id) {{
      var m = mGetModel(id);
      if (!m) return;
      var pill = document.createElement('span');
      pill.className = 'matrix-lolla-pill';
      pill.textContent = m.zh;
      mLollaPills.appendChild(pill);
    }});
  }}

  // ── Open modal with a given model id ─────────────────────────────────────
  function mOpenModal(id) {{
    var m = mGetModel(id);
    if (!m) return;
    mOpenId = id;
    var d = MDISCIPLINES[m.d];

    // Highlight open cell
    document.querySelectorAll('.matrix-cell').forEach(function(btn) {{
      btn.style.borderColor = '';
      if (btn.dataset.cellId === id) {{
        btn.style.borderColor = d.color;
        btn.style.background = d.tint;
      }} else if (!mPicks.has(btn.dataset.cellId)) {{
        btn.style.background = '';
      }}
    }});

    // Header
    mModalHeader.style.background = d.tint;
    mModalHeader.style.borderBottomColor = d.color;
    mModalDisciplineRow.innerHTML =
      '<span class="matrix-modal-disc-badge" style="background:' + d.color + '">' + mEsc(d.glyph) + '</span>'
      + '<span class="matrix-modal-disc-label" style="color:' + d.color + '">' + mEsc(d.zh) + ' · ' + mEsc(d.en.toUpperCase()) + '</span>'
      + '<span class="matrix-modal-tag-label">· ' + mEsc(m.tag) + '</span>';
    mModalZh.textContent = m.zh;
    mModalEn.textContent = m.en;

    // Body text
    mModalDesc.textContent = m.body;
    mModalDesc.style.background = d.tint;
    mModalDesc.style.borderLeftColor = d.color;
    mModalQuote.textContent = m.quote;
    mModalQuote.style.borderLeftColor = d.color;

    // Cases
    mModalCases.innerHTML = (m.cases || []).map(function(c, i) {{
      return '<div class="matrix-modal-case">'
        + '<span class="matrix-modal-case-num" style="color:' + d.color + '">' + String(i+1).padStart(2,'0') + '</span>'
        + '<span style="color:#1e293b">' + mEsc(c) + '</span>'
        + '</div>';
    }}).join('');

    // Related chips
    mModalRelated.innerHTML = (m.related || []).map(function(rid) {{
      var r = mGetModel(rid);
      if (!r) return '';
      var rd = MDISCIPLINES[r.d];
      return '<button class="matrix-modal-related-chip" data-modal-related="' + rid + '" '
        + 'style="background:' + rd.tint + ';color:' + rd.color + ';border-color:' + rd.color + '33">'
        + '<span style="font-family:var(--imq-font-mono)">' + mEsc(rd.glyph) + '</span>'
        + mEsc(r.zh)
        + '</button>';
    }}).join('');

    // Wire related chip clicks (swap modal content, don't close)
    mModalRelated.querySelectorAll('[data-modal-related]').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        mOpenModal(btn.getAttribute('data-modal-related'));
      }});
    }});

    // Ask box
    mModalAskText.textContent = m.ask;

    // Show modal
    mModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }}

  // ── Close modal ───────────────────────────────────────────────────────────
  function mCloseModal() {{
    mOpenId = null;
    mModal.style.display = 'none';
    document.body.style.overflow = '';
    // Reset open-cell highlight
    document.querySelectorAll('.matrix-cell').forEach(function(btn) {{
      if (!mPicks.has(btn.dataset.cellId)) {{
        btn.style.background = '';
        btn.style.borderColor = '';
      }}
    }});
  }}

  // ── Toggle pick (lolla mode) ──────────────────────────────────────────────
  function mTogglePick(id, btn) {{
    var d = MDISCIPLINES[btn.dataset.cellD];
    if (mPicks.has(id)) {{
      mPicks.delete(id);
      btn.classList.remove('picked');
      btn.style.background = '';
      btn.style.color = '';
      btn.style.borderColor = '';
      // restore tag color
      var tagEl = btn.querySelector('.matrix-cell-tag');
      if (tagEl) tagEl.style.color = d.color;
      var newEl = btn.querySelector('.matrix-cell-new');
      if (newEl) newEl.style.background = '#dc2626';
    }} else {{
      mPicks.add(id);
      btn.classList.add('picked');
      btn.style.background = d.color;
      btn.style.color = '#fff';
      btn.style.borderColor = d.color;
      // picked: tag rendered by CSS .matrix-cell.picked .matrix-cell-tag
    }}
    mUpdateStrip();
  }}

  // ── Cell click handler ────────────────────────────────────────────────────
  document.querySelectorAll('.matrix-cell').forEach(function(btn) {{
    var id = btn.dataset.cellId;

    // Hover
    btn.addEventListener('mouseenter', function() {{
      if (!mPicks.has(id) && mOpenId !== id) {{
        var d = MDISCIPLINES[btn.dataset.cellD];
        btn.style.background = d.tint;
      }}
    }});
    btn.addEventListener('mouseleave', function() {{
      if (!mPicks.has(id) && mOpenId !== id) {{
        btn.style.background = '';
      }}
    }});

    btn.addEventListener('click', function() {{
      if (mPickerOn) {{
        mTogglePick(id, btn);
      }} else {{
        mOpenModal(id);
      }}
    }});
  }});

  // ── Lolla toggle button ───────────────────────────────────────────────────
  mLollaBtn.addEventListener('click', function() {{
    mPickerOn = !mPickerOn;
    // Clear picks
    mPicks.forEach(function(id) {{
      var btn = document.querySelector('.matrix-cell[data-cell-id="' + id + '"]');
      if (btn) {{
        btn.classList.remove('picked');
        btn.style.background = '';
        btn.style.color = '';
        btn.style.borderColor = '';
      }}
    }});
    mPicks.clear();
    mLollaBtn.classList.toggle('active', mPickerOn);
    mLollaBtn.textContent = mPickerOn ? '✓ LOLLA MODE' : '⚡ LOLLAPALOOZA';
    mLollaStrip.classList.toggle('visible', mPickerOn);
    if (mPickerOn) mUpdateStrip();
    // Also close modal if open
    if (mOpenId) mCloseModal();
  }});

  // ── Modal close: backdrop click ───────────────────────────────────────────
  mModal.addEventListener('click', function(e) {{
    if (e.target === mModal) mCloseModal();
  }});

  // ── Modal close: × button ────────────────────────────────────────────────
  mModalClose.addEventListener('click', mCloseModal);

  // ── Modal close: ESC key ──────────────────────────────────────────────────
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape' && mOpenId) mCloseModal();
  }});

}})();
</script>
</body>
</html>"""

    out_path = DOCS_DIR / "mental-models" / "index.html"
    _write_html(out_path, html)


if __name__ == "__main__":
    import sys
    if "--mental-models" in sys.argv:
        generate_mental_models()
    else:
        build_site()
