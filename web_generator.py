"""
web_generator.py — 靜態網站生成器

生成供 GitHub Pages 托管的 HTML 頁面：
  docs/index.html              — 首頁（報告總表 + 搜尋）
  docs/report/{page_id}.html   — 10-K / 10-Q 個別報告頁面
  docs/company/{TICKER}.html   — 個別公司頁面（歷史報告 + 護城河趨勢）
  docs/industry/{name}.html    — 產業比較頁面（護城河橫向比較）

網址：https://research.investmquest.com
"""

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
.dim-text{font-size:.82rem;color:#4b5563;line-height:1.55;
          display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
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
    links = [("首頁", "/")]
    nav = " ".join(
        f'<a href="{url}" class="{"active" if active == lbl else ""}">{lbl}</a>'
        for lbl, url in links
    )
    return f"""<header>
  <div class="container hdr-inner">
    <a class="logo" href="/">InvestMQuest Research</a>
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
  var si=document.getElementById('search-input');
  var fc=document.getElementById('filter-count');
  var filters={{form:'all',moat:'all'}};

  function applyFilters(){{
    var q=si?si.value.toLowerCase():'';
    var rows=document.querySelectorAll('#report-tbody .searchable');
    var total=rows.length,shown=0;
    rows.forEach(function(el){{
      var matchText=!q||el.textContent.toLowerCase().indexOf(q)>=0;
      var matchForm=filters.form==='all'||el.getAttribute('data-form')===filters.form;
      var matchMoat=filters.moat==='all'||el.getAttribute('data-moat')===filters.moat;
      var vis=matchText&&matchForm&&matchMoat;
      el.style.display=vis?'':'none';
      if(vis) shown++;
    }});
    if(fc) fc.textContent='\u986F\u793A '+shown+' / \u5171 '+total+' \u7B46';
  }}

  if(si) si.addEventListener('input',applyFilters);

  document.querySelectorAll('.filter-btn').forEach(function(btn){{
    btn.addEventListener('click',function(){{
      var group=btn.getAttribute('data-filter');
      var val=btn.getAttribute('data-value');
      filters[group]=val;
      btn.parentElement.querySelectorAll('.filter-btn').forEach(function(b){{
        b.classList.remove('active');
      }});
      btn.classList.add('active');
      applyFilters();
    }});
  }});
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


def _parse_committee_summary(text: str) -> str:
    """解析「## 投資委員會總結」到下一個「---」之間的內容。"""
    m = re.search(r"##\s*投資委員會總結\s*\n(.*?)(?:\n---|\n##\s|\Z)", text, re.DOTALL)
    return m.group(1).strip() if m else ""


_MASTER_NAMES = ["Peter Lynch", "Hamilton Helmer", "Howard Marks"]
_MASTER_ICONS = {"Peter Lynch": "📈", "Hamilton Helmer": "🏰", "Howard Marks": "⚖️"}


def _parse_master_frameworks(text: str) -> list[dict]:
    """
    解析「## 大師框架分析」之後的三位大師段落。
    回傳 [{name, content}, ...]
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
        results.append({"name": name, "content": body[start:end].strip()})
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
    回傳 {brand_power: float, ...}，找不到的維度不包含。
    """
    result = {}
    for key, cn_label in MOAT_5_DIMS.items():
        # 匹配「品牌力（8/10分）」或「品牌力：8/10」等
        pattern = rf"{re.escape(cn_label)}[（(：:]\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*分?[）)]?"
        m = re.search(pattern, text)
        if m:
            score = float(m.group(1))
            max_score = float(m.group(2))
            # 統一換算為 10 分制
            if max_score > 0:
                result[key] = round(score / max_score * 10, 1)
            else:
                result[key] = 0.0
    return result


def _extract_10q_financials(content: str) -> list[dict]:
    """
    從 10-Q 數字變化段落提取財務指標，含變動方向偵測。
    回傳 [{label, value, direction}, ...]，direction 為 "up"/"down"/"flat"/""。
    """
    up_kw = ["上升", "增加", "成長", "提升", "增長", "上漲", "擴大",
             "改善", "高出", "超越", "優於", "好轉"]
    down_kw = ["下降", "減少", "衰退", "降低", "下滑", "縮小", "惡化",
               "低於", "不及", "壓縮", "收窄", "萎縮"]
    flat_kw = ["持平", "不變", "維持", "穩定", "持穩"]

    rows = []
    for line in content.split("\n"):
        line = line.strip().lstrip("-•*").strip()
        if not line:
            continue
        m = re.split(r"[：:]", line, maxsplit=1)
        label = m[0].strip() if m else line
        value = m[1].strip() if len(m) >= 2 else ""

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
            rows.append({"label": label, "value": value, "direction": direction})
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
    """生成 docs/index.html —— 報告總表 + 搜尋過濾。"""
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
    body = f"""
<div class="page-hdr">
  <div class="container">
    <h1>財報分析總覽</h1>
    <p class="sub">{today} &mdash; AI 驅動，涵蓋 10-Q / 10-K 深度解讀</p>
  </div>
</div>

<div class="section">
  <div class="container">
    <div class="search-wrap">
      <input id="search-input" type="text" placeholder="搜尋 Ticker、報告類型…">
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

    <div id="filter-count" style="font-size:.82rem;color:var(--muted);margin-bottom:.6rem">
      顯示 {total_count} / 共 {total_count} 筆
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

    # ── 深度研究報告區塊
    dd_reports = _scan_dd_reports()
    if dd_reports:
        dd_rows = ""
        for dd in dd_reports:
            t = html_lib.escape(dd["ticker"])
            d = html_lib.escape(dd["date"])
            fn = html_lib.escape(dd["filename"])
            dd_rows += f"""
<tr class="searchable">
  <td><strong>{t}</strong></td>
  <td><span class="tag tag-dd">深度研究</span></td>
  <td>{d}</td>
  <td><a href="/dd/{fn}">查看 &rarr;</a></td>
</tr>"""

        body += f"""
<div class="section">
  <div class="container">
    <h2 class="section-title">深度研究報告</h2>
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
        <tbody>{dd_rows}</tbody>
      </table>
    </div>
  </div>
</div>"""

    _write_html(DOCS_DIR / "index.html", _base_page(f"首頁 — {today}", body))


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
    remaining = max(0, 110 - total)
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
    committee_raw = _parse_committee_summary(content)
    committee_html = ""
    if committee_raw:
        committee_html = f"""
<div class="card" style="border-left:4px solid var(--brand);background:var(--brand-light);margin-bottom:1.25rem">
  <h3 style="color:var(--brand);margin-bottom:.6rem">投資委員會總結</h3>
  <div class="analysis">{_md(committee_raw)}</div>
</div>"""

    # ── 大師框架分析
    masters = _parse_master_frameworks(content)
    masters_html = ""
    if masters:
        master_cards = ""
        for m in masters:
            icon = _MASTER_ICONS.get(m["name"], "📊")
            master_cards += f"""
<div class="card" style="margin-bottom:.85rem">
  <h3>{icon} {html_lib.escape(m["name"])}</h3>
  <div class="analysis">{_md(m["content"])}</div>
</div>"""
        masters_html = f"""
<h2 class="section-title" style="margin-top:1.5rem">大師框架分析</h2>
{master_cards}"""

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
        data:[{total},{remaining}],
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
    生成 10-Q 報告頁面（與 10-K 風格一致）：
      頂部 Ticker 大標題 + 季度年度 + 一句話摘要大字
      → 五維度卡片排版 → 財務數字表格（含↑↓箭頭）→ 完整分析
    """
    page_id = report.get("page_id", "")
    slug = page_id.replace("-", "")
    ticker = html_lib.escape(report.get("ticker", ""))
    date = html_lib.escape(report.get("date", ""))

    parsed = _parse_10q_sections(content)

    # ── 頂部：Ticker 大字標題 + 季度年度 + 一句話摘要
    summary_hero = ""
    if parsed["summary"]:
        summary_hero = f"""
<div class="thesis">
  <p>&ldquo;{html_lib.escape(parsed["summary"])}&rdquo;</p>
</div>"""

    # ── 五維度卡片（dim-grid，與 10-K 八維度同風格）
    dim_titles = {
        1: ("數字變化", "Financial Changes"),
        2: ("敘事變化", "Narrative Changes"),
        3: ("資本配置", "Capital Allocation"),
        4: ("護城河信號", "Moat Signals"),
        5: ("一句話摘要", "One-line Summary"),
    }

    # ── 1. 數字變化 → 表格卡片
    fin_card_html = ""
    if 1 in parsed["sections"]:
        fin_rows = _extract_10q_financials(parsed["sections"][1]["content"])
        if fin_rows:
            trs = ""
            for fr in fin_rows:
                label = html_lib.escape(fr["label"])
                value = html_lib.escape(fr["value"])
                d = fr["direction"]
                if d == "up":
                    arrow = '<span class="chg-up">&uarr;</span>'
                elif d == "down":
                    arrow = '<span class="chg-down">&darr;</span>'
                elif d == "flat":
                    arrow = '<span class="chg-flat">&mdash;</span>'
                else:
                    arrow = ""
                if value:
                    trs += f"<tr><td style='font-weight:600;white-space:nowrap'>{label}</td><td>{value}</td><td style='text-align:center'>{arrow}</td></tr>"
                else:
                    trs += f"<tr><td colspan='3'>{label}</td></tr>"
            fin_card_html = f"""
<div class="dim-card" style="grid-column:1/-1">
  <div class="dim-hdr">
    <span class="dim-name">一、數字變化<span class="dim-en">Financial Changes</span></span>
  </div>
  <div style="overflow-x:auto;margin-top:.5rem">
    <table>
      <thead><tr><th>指標</th><th>分析</th><th style="text-align:center">趨勢</th></tr></thead>
      <tbody>{trs}</tbody>
    </table>
  </div>
</div>"""
        else:
            fin_card_html = f"""
<div class="dim-card" style="grid-column:1/-1">
  <div class="dim-hdr">
    <span class="dim-name">一、數字變化<span class="dim-en">Financial Changes</span></span>
  </div>
  <div class="dim-text" style="-webkit-line-clamp:unset">{_md(parsed["sections"][1]["content"])}</div>
</div>"""

    # ── 2. 敘事變化卡片 + 前瞻指引
    narrative_card_html = ""
    if 2 in parsed["sections"]:
        sec2 = parsed["sections"][2]["content"]
        guidance_text = _extract_10q_guidance(sec2)

        # 前瞻指引藍色提示（嵌入卡片內）
        guidance_inset = ""
        if guidance_text:
            guidance_inset = f"""
  <div style="background:var(--brand-light);border:1px solid #93c5fd;border-radius:6px;
              padding:.75rem 1rem;margin-top:.6rem">
    <div style="font-size:.78rem;font-weight:600;color:var(--brand);margin-bottom:.25rem">前瞻指引 Forward Guidance</div>
    <div style="font-size:.82rem;line-height:1.55;color:#1e40af">{_md(guidance_text)}</div>
  </div>"""

        remaining_lines = []
        for line in sec2.split("\n"):
            stripped = line.strip().lstrip("-•*").strip()
            if not stripped:
                continue
            if any(kw in stripped for kw in ["前瞻指引", "guidance", "Guidance"]):
                continue
            remaining_lines.append(stripped)
        remaining_text = "\n".join(remaining_lines)

        narrative_card_html = f"""
<div class="dim-card">
  <div class="dim-hdr">
    <span class="dim-name">二、敘事變化<span class="dim-en">Narrative Changes</span></span>
  </div>
  <div class="dim-text" style="-webkit-line-clamp:unset">{_md(remaining_text)}</div>
  {guidance_inset}
</div>"""

    # ── 3. 資本配置卡片（內容為空時不顯示）
    capital_card_html = ""
    if 3 in parsed["sections"] and parsed["sections"][3]["content"].strip():
        cap_items = _extract_10q_capital(parsed["sections"][3]["content"])
        if cap_items:
            # 過濾掉沒有實質內容的卡片
            cap_items = [ci for ci in cap_items if ci.get("amount") or ci.get("detail")]
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
<div class="dim-card">
  <div class="dim-hdr">
    <span class="dim-name">三、資本配置<span class="dim-en">Capital Allocation</span></span>
  </div>
  <div class="cap-grid" style="margin-top:.5rem">{cap_cards}</div>
</div>"""
        else:
            sec3_html = _md(parsed["sections"][3]["content"])
            if sec3_html.strip():
                capital_card_html = f"""
<div class="dim-card">
  <div class="dim-hdr">
    <span class="dim-name">三、資本配置<span class="dim-en">Capital Allocation</span></span>
  </div>
  <div class="dim-text" style="-webkit-line-clamp:unset">{sec3_html}</div>
</div>"""

    # ── 4. 護城河信號卡片（強化=綠色 / 弱化=紅色）
    moat_card_html = ""
    if parsed["signals"] or (4 in parsed["sections"]):
        sig_items = ""
        if parsed["signals"]:
            for sig in parsed["signals"]:
                cls_map = {"positive": "signal-pos", "negative": "signal-neg", "neutral": "signal-neu"}
                prefix_map = {"positive": "&#x2713; ", "negative": "&#x2717; ", "neutral": ""}
                cls = cls_map.get(sig["type"], "signal-neu")
                prefix = prefix_map.get(sig["type"], "")
                sig_items += f'<span class="signal {cls}">{prefix}{html_lib.escape(sig["text"])}</span>\n'
        elif 4 in parsed["sections"]:
            sig_items = f'<div class="dim-text" style="-webkit-line-clamp:unset">{_md(parsed["sections"][4]["content"])}</div>'

        moat_card_html = f"""
<div class="dim-card" style="grid-column:1/-1">
  <div class="dim-hdr">
    <span class="dim-name">四、護城河信號<span class="dim-en">Moat Signals</span></span>
  </div>
  <div style="margin-top:.4rem">{sig_items}</div>
</div>"""

    # ── 新維度：管理層誠信驗證
    mgmt_card_html = ""
    if parsed.get("mgmt_integrity"):
        mgmt_card_html = f"""
<div class="dim-card" style="grid-column:1/-1">
  <div class="dim-hdr">
    <span class="dim-name">管理層誠信驗證<span class="dim-en">Management Integrity</span></span>
  </div>
  <div class="dim-text" style="-webkit-line-clamp:unset">{_md(parsed["mgmt_integrity"])}</div>
</div>"""

    # ── 新維度：附注重點掃描
    footnote_card_html = ""
    if parsed.get("footnote_scan"):
        footnote_card_html = f"""
<div class="dim-card" style="grid-column:1/-1">
  <div class="dim-hdr">
    <span class="dim-name">附注重點掃描<span class="dim-en">Footnote Highlights</span></span>
  </div>
  <div class="dim-text" style="-webkit-line-clamp:unset">{_md(parsed["footnote_scan"])}</div>
</div>"""

    # ── 新維度：數字一致性驗證
    consistency_card_html = ""
    if parsed.get("consistency_check"):
        consistency_card_html = f"""
<div class="dim-card" style="grid-column:1/-1">
  <div class="dim-hdr">
    <span class="dim-name">數字一致性驗證<span class="dim-en">Consistency Check</span></span>
  </div>
  <div class="dim-text" style="-webkit-line-clamp:unset">{_md(parsed["consistency_check"])}</div>
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

    <h2 class="section-title">季報分析</h2>
    <div class="dim-grid">
      {fin_card_html}
      {narrative_card_html}
      {capital_card_html}
      {moat_card_html}
      {mgmt_card_html}
      {footnote_card_html}
      {consistency_card_html}
    </div>

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

    # 首頁（在讀取內容並解析護城河之後生成，確保護城河等級已填入）
    generate_index(notion_reports)

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


if __name__ == "__main__":
    build_site()
