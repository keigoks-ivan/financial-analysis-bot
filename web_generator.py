"""
web_generator.py — 靜態網站生成器

生成供 GitHub Pages 托管的 HTML 頁面：
  docs/index.html              — 首頁（今日報告 + 產業瀏覽 + 搜尋）
  docs/company/{TICKER}.html  — 個別公司頁面（歷史報告 + 護城河趨勢）
  docs/industry/{name}.html   — 產業比較頁面（護城河橫向比較）

網址：https://research.investmquest.com
"""

import os
import json
import datetime
import html as html_lib
import requests
from pathlib import Path
from jinja2 import Environment, BaseLoader
# ── 路徑常數 ─────────────────────────────────────────────────────────────────
DOCS_DIR    = Path("docs")

# ── Notion 設定 ──────────────────────────────────────────────────────────────
NOTION_TOKEN      = os.environ.get("NOTION_TOKEN")
NOTION_8K_DB_ID   = os.environ.get("NOTION_8K_DB_ID")
NOTION_10Q_DB_ID  = os.environ.get("NOTION_10Q_DB_ID")
NOTION_10K_DB_ID  = os.environ.get("NOTION_10K_DB_ID")
KB_DIR      = Path("knowledge_base")
BASE_URL    = "https://research.investmquest.com"

DISCLAIMER = """
<strong>免責聲明：</strong>
本網站所有內容（包含財報摘要、護城河評分及產業分析）均由 AI 自動生成，
僅供參考，<strong>不構成任何投資建議</strong>。
投資涉及風險，投資人應自行判斷並諮詢專業顧問。
過往表現不代表未來業績。本網站與任何被分析公司均無利益關係。
"""

# ── Jinja2 環境 ──────────────────────────────────────────────────────────────
jinja_env = Environment(loader=BaseLoader(), autoescape=True)

# ── 共用 CSS（內嵌於每頁，減少依賴） ────────────────────────────────────────
SHARED_CSS = """
:root{--brand:#1a56db;--bg:#f8fafc;--card:#fff;--text:#1e293b;--muted:#64748b;
      --border:#e2e8f0;--green:#16a34a;--red:#dc2626;--yellow:#d97706}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
     background:var(--bg);color:var(--text);line-height:1.6}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1100px;margin:0 auto;padding:0 1.5rem}
header{background:var(--brand);color:#fff;padding:1rem 0}
header .logo{font-size:1.4rem;font-weight:700}
header nav a{color:rgba(255,255,255,.85);margin-left:1.5rem;font-size:.9rem}
header nav a:hover{color:#fff}
.hero{background:linear-gradient(135deg,#1a56db,#0d3a8a);color:#fff;
      padding:2.5rem 0;text-align:center}
.hero h1{font-size:2rem;margin-bottom:.5rem}
.hero p{opacity:.85}
.search-bar{margin:1.5rem auto;max-width:480px;display:flex;gap:.5rem}
.search-bar input{flex:1;padding:.65rem 1rem;border:none;border-radius:8px;font-size:1rem}
.search-bar button{padding:.65rem 1.2rem;background:#fff;color:var(--brand);
                   border:none;border-radius:8px;cursor:pointer;font-weight:600}
.section{padding:2.5rem 0}
.section-title{font-size:1.4rem;font-weight:700;margin-bottom:1.25rem;
               border-left:4px solid var(--brand);padding-left:.75rem}
.grid{display:grid;gap:1rem}
.grid-3{grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
.grid-4{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;
      padding:1.25rem;transition:box-shadow .2s}
.card:hover{box-shadow:0 4px 16px rgba(0,0,0,.08)}
.card-title{font-weight:700;margin-bottom:.4rem}
.tag{display:inline-block;padding:.15rem .55rem;border-radius:4px;
     font-size:.75rem;font-weight:600}
.tag-8k{background:#fef3c7;color:#92400e}
.tag-10q{background:#dbeafe;color:#1e40af}
.tag-10k{background:#d1fae5;color:#065f46}
.tag-synthesis{background:#ede9fe;color:#5b21b6}
.moat-bar{height:8px;border-radius:4px;background:var(--border);overflow:hidden}
.moat-fill{height:100%;border-radius:4px;background:var(--brand)}
.score{font-weight:700;font-size:1.1rem}
.score-high{color:var(--green)}
.score-mid{color:var(--yellow)}
.score-low{color:var(--red)}
table{width:100%;border-collapse:collapse;font-size:.9rem}
th,td{text-align:left;padding:.6rem .75rem;border-bottom:1px solid var(--border)}
th{background:#f1f5f9;font-weight:600}
tr:hover td{background:#f8fafc}
.disclaimer{background:#fef9c3;border:1px solid #fde68a;border-radius:8px;
            padding:1rem 1.25rem;font-size:.8rem;color:#78350f;margin-top:2rem}
footer{background:#1e293b;color:rgba(255,255,255,.6);text-align:center;
       padding:1.5rem 0;font-size:.8rem;margin-top:3rem}
footer a{color:rgba(255,255,255,.7)}
@media(max-width:640px){.grid-3,.grid-4{grid-template-columns:1fr}}
"""

# ── 共用 Header / Footer 模板片段 ────────────────────────────────────────────

def _header(active: str = "") -> str:
    links = [
        ("首頁", "/"),
        ("公司", "/company/"),
        ("產業", "/industry/"),
        ("播客", "/podcast.xml"),
    ]
    nav = " ".join(
        f'<a href="{url}" {"style=color:#fff;font-weight:700" if active==lbl else ""}>{lbl}</a>'
        for lbl, url in links
    )
    return f"""
<header>
  <div class="container" style="display:flex;align-items:center;justify-content:space-between">
    <a class="logo" href="/" style="color:#fff">📊 InvestMQuest Research</a>
    <nav>{nav}</nav>
  </div>
</header>"""


def _footer() -> str:
    year = datetime.date.today().year
    return f"""
<div class="container"><div class="disclaimer">{DISCLAIMER}</div></div>
<footer>
  <div class="container">
    © {year} InvestMQuest Research ·
    <a href="/podcast.xml">Podcast RSS</a> ·
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
  <meta name="description" content="AI 驅動財報分析平台，提供 8-K / 10-Q / 10-K 深度解讀">
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
// 簡易客戶端搜尋（過濾 .searchable 元素）
function doSearch(q) {{
  q = q.toLowerCase();
  document.querySelectorAll('.searchable').forEach(el => {{
    el.style.display = el.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}
const si = document.getElementById('search-input');
if(si) si.addEventListener('input', e => doSearch(e.target.value));
</script>
</body>
</html>"""


# ── 資料載入 ─────────────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict | list:
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _moat_score_class(score: float) -> str:
    if score >= 7:
        return "score-high"
    if score >= 5:
        return "score-mid"
    return "score-low"


def _moat_fill_pct(score: float, max_score: float = 10.0) -> int:
    return min(100, int(score / max_score * 100))


# ── 首頁生成 ─────────────────────────────────────────────────────────────────

def generate_index(
    reports: list[dict],
    industries: list[str],
    synthesis: str,
) -> None:
    """
    生成 docs/index.html。

    reports: list of {
      ticker, form, date, summary (前200字), moat_score (可選)
    }
    industries: list of industry name strings
    synthesis: 今日整合報告全文
    """
    today = datetime.date.today().strftime("%Y 年 %m 月 %d 日")

    # 報告卡片（顯示所有報告）
    report_cards = ""
    for r in reports:
        form    = r.get("form", "")
        ticker  = r.get("ticker", "")
        name    = r.get("name", "")
        summary = html_lib.escape(r.get("summary", "")[:180])
        date    = r.get("date", "")
        page_id = r.get("page_id", "")
        tag_cls = {"8-K": "tag-8k", "10-Q": "tag-10q", "10-K": "tag-10k"}.get(form, "tag-8k")
        slug    = page_id.replace("-", "")

        moat_html = ""
        if ms := r.get("moat_score"):
            cls = _moat_score_class(ms)
            moat_html = f'<p style="margin-top:.5rem">護城河：<span class="score {cls}">{ms:.1f}/10</span></p>'

        report_cards += f"""
<div class="card searchable">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem">
    <span class="card-title">{html_lib.escape(ticker or name)}</span>
    <span class="tag {tag_cls}">{html_lib.escape(form)}</span>
  </div>
  <p style="font-size:.85rem;color:var(--muted)">{date}</p>
  <p style="font-size:.9rem;margin-top:.5rem">{html_lib.escape(name)}</p>
  {moat_html}
  <a href="/report/{slug}.html" style="font-size:.85rem;display:block;margin-top:.75rem">
    → 查看完整分析
  </a>
</div>"""

    # 產業瀏覽
    industry_cards = ""
    for ind in industries:
        slug = ind.lower().replace(" ", "-")
        industry_cards += f"""
<a class="card searchable" href="/industry/{slug}.html" style="display:block;text-align:center">
  <div class="card-title">{html_lib.escape(ind)}</div>
  <div style="font-size:.85rem;color:var(--muted);margin-top:.25rem">護城河橫向比較 →</div>
</a>"""

    # 整合報告預覽
    synth_preview = ""
    if synthesis:
        preview = html_lib.escape(synthesis[:400])
        synth_preview = f"""
<section class="section">
  <div class="container">
    <h2 class="section-title">今日整合報告</h2>
    <div class="card">
      <div style="display:flex;justify-content:space-between;margin-bottom:.5rem">
        <span class="card-title">跨公司產業趨勢</span>
        <span class="tag tag-synthesis">SYNTHESIS</span>
      </div>
      <p style="white-space:pre-line;font-size:.9rem">{preview}…</p>
      <a href="/company/synthesis.html" style="display:block;margin-top:.75rem;font-size:.85rem">
        → 閱讀完整整合報告
      </a>
    </div>
  </div>
</section>"""

    body = f"""
<div class="hero">
  <div class="container">
    <h1>財報自動化分析</h1>
    <p>{today} ── AI 驅動，每日更新</p>
    <div class="search-bar">
      <input id="search-input" type="text" placeholder="搜尋 Ticker 或關鍵字…">
      <button onclick="doSearch(document.getElementById('search-input').value)">搜尋</button>
    </div>
  </div>
</div>

{synth_preview}

<section class="section">
  <div class="container">
    <h2 class="section-title">今日申報報告</h2>
    <div class="grid grid-3">{report_cards or '<p>今日尚無報告。</p>'}</div>
  </div>
</section>

<section class="section" style="background:#f1f5f9;padding:2rem 0">
  <div class="container">
    <h2 class="section-title">產業瀏覽</h2>
    <div class="grid grid-4">{industry_cards or '<p>尚未建立產業分類。</p>'}</div>
  </div>
</section>"""

    _write_html(DOCS_DIR / "index.html", _base_page(f"首頁 — {today}", body))


# ── 公司頁面 ─────────────────────────────────────────────────────────────────

def generate_company_page(
    ticker: str,
    company_name: str,
    history: list[dict],
    moat_history: dict,
) -> None:
    """
    生成 docs/company/{ticker}.html。

    history: list of {form, date, analysis, moat_score}
             按 date 降冪（最新在前）
    moat_history: { "2022": {brand_power: 7, ...}, "2023": {...}, ... }
    """
    ticker_esc = html_lib.escape(ticker.upper())
    name_esc   = html_lib.escape(company_name or ticker.upper())

    # 歷史報告列表
    history_rows = ""
    for rep in history:
        form    = rep.get("form", "")
        date    = rep.get("date", "")
        summary = html_lib.escape(rep.get("analysis", "")[:200])
        tag_cls = {"8-K": "tag-8k", "10-Q": "tag-10q", "10-K": "tag-10k"}.get(form, "tag-8k")
        ms      = rep.get("moat_score")
        moat_td = f'<span class="score {_moat_score_class(ms)}">{ms:.1f}</span>' if ms else "–"

        history_rows += f"""
<tr>
  <td><span class="tag {tag_cls}">{html_lib.escape(form)}</span></td>
  <td>{html_lib.escape(date)}</td>
  <td>{moat_td}</td>
  <td style="font-size:.85rem">{summary}…</td>
</tr>"""

    # 護城河維度雷達（HTML 文字版）
    dim_labels = {
        "brand_power":    "品牌力",
        "switching_costs": "轉換成本",
        "network_effects": "網絡效應",
        "cost_advantage":  "成本優勢",
        "regulatory_moat": "監管護城河",
    }

    moat_bars = ""
    latest_year = sorted(moat_history.keys())[-1] if moat_history else None
    if latest_year:
        scores = moat_history[latest_year]
        for dim_key, dim_label in dim_labels.items():
            score = scores.get(dim_key, 0)
            pct   = _moat_fill_pct(score)
            cls   = _moat_score_class(score)
            moat_bars += f"""
<div style="margin-bottom:.75rem">
  <div style="display:flex;justify-content:space-between;margin-bottom:.25rem">
    <span style="font-size:.9rem">{html_lib.escape(dim_label)}</span>
    <span class="score {cls}">{score:.1f}/10</span>
  </div>
  <div class="moat-bar"><div class="moat-fill" style="width:{pct}%"></div></div>
</div>"""

    # 歷年護城河趨勢表
    moat_trend_rows = ""
    for year in sorted(moat_history.keys()):
        sc   = moat_history[year]
        avg  = sum(sc.values()) / len(sc) if sc else 0
        cls  = _moat_score_class(avg)
        cols = " ".join(
            f"<td>{sc.get(k, 0):.1f}</td>" for k in dim_labels
        )
        moat_trend_rows += f"""
<tr>
  <td>{html_lib.escape(year)}</td>
  {cols}
  <td class="score {cls}">{avg:.1f}</td>
</tr>"""

    dim_headers = "".join(
        f"<th>{label}</th>" for label in dim_labels.values()
    )

    moat_section = ""
    if moat_bars or moat_trend_rows:
        moat_section = f"""
<div class="card" style="margin-top:1rem">
  <h3 style="margin-bottom:1rem">護城河評分（{latest_year}）</h3>
  {moat_bars}
</div>
{"" if not moat_trend_rows else f'''
<div class="card" style="margin-top:1rem;overflow-x:auto">
  <h3 style="margin-bottom:1rem">護城河歷年趨勢</h3>
  <table>
    <thead><tr><th>年份</th>{dim_headers}<th>平均</th></tr></thead>
    <tbody>{moat_trend_rows}</tbody>
  </table>
</div>'''}"""

    body = f"""
<div class="hero">
  <div class="container">
    <h1>{ticker_esc}</h1>
    <p>{name_esc} ── 歷史財報分析</p>
  </div>
</div>
<section class="section">
  <div class="container">
    <a href="/" style="font-size:.85rem">← 返回首頁</a>
    {moat_section}
    <div class="card" style="margin-top:1rem;overflow-x:auto">
      <h3 style="margin-bottom:1rem">申報歷史</h3>
      <table>
        <thead><tr><th>類型</th><th>日期</th><th>護城河</th><th>摘要</th></tr></thead>
        <tbody>{''.join(history_rows) or '<tr><td colspan="4">尚無記錄</td></tr>'}</tbody>
      </table>
    </div>
  </div>
</section>"""

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

    companies: list of {
      ticker, company_name, moat_scores: {brand_power: X, ...}, avg_moat: X
    }
    按 avg_moat 降冪排序。
    """
    slug       = industry_name.lower().replace(" ", "-")
    name_esc   = html_lib.escape(industry_name)

    dim_labels = {
        "brand_power":    "品牌力",
        "switching_costs": "轉換成本",
        "network_effects": "網絡效應",
        "cost_advantage":  "成本優勢",
        "regulatory_moat": "監管護城河",
    }

    # 排序（護城河高 → 低）
    sorted_cos = sorted(companies, key=lambda c: c.get("avg_moat", 0), reverse=True)

    rows = ""
    for co in sorted_cos:
        ticker   = co.get("ticker", "")
        scores   = co.get("moat_scores", {})
        avg      = co.get("avg_moat", 0)
        cls      = _moat_score_class(avg)

        dim_cells = " ".join(
            f"<td>{scores.get(k, 0):.1f}</td>" for k in dim_labels
        )
        rows += f"""
<tr>
  <td><a href="/company/{ticker.lower()}.html">{html_lib.escape(ticker)}</a></td>
  {dim_cells}
  <td class="score {cls}">{avg:.1f}</td>
</tr>"""

    # 視覺化：水平護城河評分條
    bar_chart = ""
    for co in sorted_cos:
        ticker = co.get("ticker", "")
        avg    = co.get("avg_moat", 0)
        pct    = _moat_fill_pct(avg)
        cls    = _moat_score_class(avg)
        bar_chart += f"""
<div style="margin-bottom:.6rem;display:flex;align-items:center;gap:.75rem">
  <a href="/company/{ticker.lower()}.html"
     style="min-width:60px;font-weight:600;font-size:.9rem">{html_lib.escape(ticker)}</a>
  <div class="moat-bar" style="flex:1"><div class="moat-fill" style="width:{pct}%"></div></div>
  <span class="score {cls}" style="min-width:40px;text-align:right">{avg:.1f}</span>
</div>"""

    dim_headers = "".join(
        f"<th>{label}</th>" for label in dim_labels.values()
    )

    body = f"""
<div class="hero">
  <div class="container">
    <h1>{name_esc}</h1>
    <p>護城河橫向比較</p>
  </div>
</div>
<section class="section">
  <div class="container">
    <a href="/" style="font-size:.85rem">← 返回首頁</a>
    <div class="card" style="margin-top:1rem">
      <h3 style="margin-bottom:1rem">護城河總分排行</h3>
      {bar_chart or '<p>尚無評分資料</p>'}
    </div>
    <div class="card" style="margin-top:1rem;overflow-x:auto">
      <h3 style="margin-bottom:1rem">詳細維度比較</h3>
      <table>
        <thead>
          <tr>
            <th>Ticker</th>{dim_headers}<th>平均</th>
          </tr>
        </thead>
        <tbody>{''.join(rows) or '<tr><td colspan="7">尚無資料</td></tr>'}</tbody>
      </table>
    </div>
  </div>
</section>"""

    out_dir = DOCS_DIR / "industry"
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_html(
        out_dir / f"{slug}.html",
        _base_page(f"{name_esc} 產業比較", body),
    )


# ── 個別報告頁面 ─────────────────────────────────────────────────────────────

def generate_report_page(report: dict) -> None:
    """
    生成 docs/report/{page_id}.html，顯示完整 Notion 分析內容。
    """
    page_id = report.get("page_id", "")
    slug    = page_id.replace("-", "")
    name    = report.get("name", "")
    ticker  = report.get("ticker", "")
    form    = report.get("form", "")
    date    = report.get("date", "")
    tag_cls = {"8-K": "tag-8k", "10-Q": "tag-10q", "10-K": "tag-10k"}.get(form, "tag-8k")

    content = _fetch_page_content(page_id)

    body = f"""
<div class="hero">
  <div class="container">
    <h1>{html_lib.escape(ticker or name)}</h1>
    <p><span class="tag {tag_cls}" style="font-size:.9rem">{html_lib.escape(form)}</span> ── {html_lib.escape(date)}</p>
  </div>
</div>
<section class="section">
  <div class="container">
    <a href="/" style="font-size:.85rem">← 返回首頁</a>
    <div class="card" style="margin-top:1rem">
      <h3 style="margin-bottom:1rem">{html_lib.escape(name)}</h3>
      <div style="white-space:pre-line;font-size:.9rem;line-height:1.8">{html_lib.escape(content)}</div>
    </div>
  </div>
</section>"""

    out_dir = DOCS_DIR / "report"
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_html(
        out_dir / f"{slug}.html",
        _base_page(f"{ticker} {form} — {date}", body),
    )


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
    """從 Notion page properties 中取出 title 欄位的文字。"""
    prop = page.get("properties", {}).get(prop_name, {})
    for item in prop.get("title", []):
        return item.get("plain_text", "")
    return ""


def _get_rich_text(page: dict, prop_name: str) -> str:
    """從 Notion page properties 中取出 rich_text 欄位的文字。"""
    prop = page.get("properties", {}).get(prop_name, {})
    for item in prop.get("rich_text", []):
        return item.get("plain_text", "")
    return ""


def _get_date_value(page: dict, prop_name: str) -> str:
    """從 Notion page properties 中取出 date 欄位的 start 值。"""
    prop = page.get("properties", {}).get(prop_name, {})
    date_obj = prop.get("date")
    if date_obj:
        return date_obj.get("start", "")
    return ""


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
    從三個 Notion 資料庫讀取所有報告，回傳統一格式的 list。
    每筆：{name, ticker, form, date, page_id}
    """
    reports: list[dict] = []

    # 8-K：欄位 Name(title)、日期(date)、公司 Ticker(rich_text)
    pages_8k = _query_all_pages(NOTION_8K_DB_ID)
    print(f"  [DEBUG] 8-K 資料庫讀取到 {len(pages_8k)} 筆頁面")
    for page in pages_8k:
        reports.append({
            "name":    _get_title_text(page, "Name"),
            "ticker":  _get_rich_text(page, "公司 Ticker"),
            "form":    "8-K",
            "date":    _get_date_value(page, "日期"),
            "page_id": page["id"],
        })

    # 10-Q：欄位 Name(title)、Ticker(rich_text)、財報年度(rich_text)
    pages_10q = _query_all_pages(NOTION_10Q_DB_ID)
    print(f"  [DEBUG] 10-Q 資料庫讀取到 {len(pages_10q)} 筆頁面")
    for page in pages_10q:
        reports.append({
            "name":    _get_title_text(page, "Name"),
            "ticker":  _get_rich_text(page, "Ticker"),
            "form":    "10-Q",
            "date":    _get_rich_text(page, "財報年度"),
            "page_id": page["id"],
        })

    # 10-K：欄位 Name(title)、財報年度(rich_text)
    pages_10k = _query_all_pages(NOTION_10K_DB_ID)
    print(f"  [DEBUG] 10-K 資料庫讀取到 {len(pages_10k)} 筆頁面")
    for page in pages_10k:
        name = _get_title_text(page, "Name")
        # 10-K 沒有獨立 Ticker 欄位，從 Name 解析（格式如 "AAPL 10-K — ..."）
        ticker = name.split()[0] if name else ""
        reports.append({
            "name":    name,
            "ticker":  ticker,
            "form":    "10-K",
            "date":    _get_rich_text(page, "財報年度"),
            "page_id": page["id"],
        })

    # 按日期降冪排序（最新在上）
    reports.sort(key=lambda r: r.get("date", ""), reverse=True)
    return reports


# ── 工具函式 ─────────────────────────────────────────────────────────────────

def _write_html(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  生成：{path}")


def _ensure_404_and_cname() -> None:
    """確保 GitHub Pages 所需的 404.html 和 CNAME 存在。"""
    cname_path = DOCS_DIR / "CNAME"
    if not cname_path.exists():
        _write_html(cname_path, "research.investmquest.com")

    notfound_path = DOCS_DIR / "404.html"
    if not notfound_path.exists():
        body = """
<div class="hero">
  <div class="container">
    <h1>404 — 頁面不存在</h1>
    <p><a href="/" style="color:#fff">← 返回首頁</a></p>
  </div>
</div>"""
        _write_html(notfound_path, _base_page("404 找不到頁面", body))


# ── 主函式 ───────────────────────────────────────────────────────────────────

def build_site() -> None:
    """
    從 Notion 三個資料庫讀取報告，重建完整靜態網站。
    """
    print("\n[Web] 開始生成靜態網站...")

    companies_data: dict = _load_json(KB_DIR / "companies.json")
    industries_data: dict = _load_json(KB_DIR / "industries.json")
    moat_scores: dict   = _load_json(KB_DIR / "moat_scores.json")

    _ensure_404_and_cname()

    # 讀取今日整合報告
    synthesis_path = DOCS_DIR / "latest_synthesis.txt"
    synthesis_text = ""
    if synthesis_path.exists():
        with open(synthesis_path, encoding="utf-8") as f:
            synthesis_text = f.read()

    # 從 Notion 三個資料庫讀取所有報告（已按日期降冪排序）
    print("\n[Web] 從 Notion 資料庫讀取報告...")
    notion_reports = fetch_notion_reports()
    print(f"  [DEBUG] 共讀取 {len(notion_reports)} 筆報告")

    industries = list(industries_data.keys())
    generate_index(notion_reports, industries, synthesis_text)

    # 為每筆報告生成獨立頁面
    for report in notion_reports:
        generate_report_page(report)

    # 個別公司頁面（從 knowledge_base）
    for ticker, co_data in companies_data.items():
        history     = co_data.get("reports", [])
        moat_hist   = moat_scores.get(ticker, {})
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
                sc        = co_moat[latest_yr]
                avg       = sum(sc.values()) / len(sc) if sc else 0
            else:
                sc  = {}
                avg = 0
            cos_in_industry.append({
                "ticker":      ticker,
                "company_name": companies_data.get(ticker, {}).get("name", ticker),
                "moat_scores": sc,
                "avg_moat":    avg,
            })
        generate_industry_page(industry, cos_in_industry)

    print(f"[Web] 網站生成完成！共 {len(notion_reports)} 筆報告、{len(industries_data)} 個產業")


if __name__ == "__main__":
    build_site()
