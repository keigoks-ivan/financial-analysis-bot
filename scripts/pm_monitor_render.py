#!/usr/bin/env python3
"""
pm_monitor_render.py — docs/pm/MONITOR_YYYYMMDD.md -> docs/pm/index.html

position-thesis-monitor sub-agent 每週吐一份新的 docs/pm/MONITOR_YYYYMMDD.md
(純 markdown)。這支腳本掃 docs/pm/ 底下全部 MONITOR_*.md，取檔名日期最新的一份，
把它轉成 HTML 內嵌進 docs/pm/index.html（沿用既有頁首 imq-nav / 樣式 / 版型），並
重建「歷史週掃報告」清單（全部 MONITOR_*.md，新到舊）。

不依賴任何外部套件（repo 慣例：只用 python3 標準庫）；md -> html 轉換是這支腳本
自己手寫的簡易 parser（見 _MdToHtml 一段），只涵蓋 MONITOR_*.md 實際會用到的語法：
標題 #..####、水平線 ---、表格、有序/無序清單（含一層巢狀 list 或巢狀表格）、
blockquote、粗體 **、行內 code `、連結 [text](url)。

用法：
  python3 scripts/pm_monitor_render.py

Idempotent：同一批 MONITOR_*.md 重跑會產生相同的 docs/pm/index.html（只有
「頁面更新」時間戳會變），可放進雲端週排程重複執行。

風格對齊 scripts/pm_render.py（已於 2026-07-19 歸檔至 _archived/scripts/，但
仍是本 repo「PM 渲染腳本」的既有寫法參照：純函式、REPO 常數、main() 收尾印訊息）。
"""
import html
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PM_DIR = REPO / "docs" / "pm"
INDEX_PATH = PM_DIR / "index.html"

MONITOR_RE = re.compile(r"^MONITOR_(\d{8})\.md$")


# ── discover reports ────────────────────────────────────────────────────────
def find_reports():
    """Return list of (date_str 'YYYY-MM-DD', yyyymmdd, Path), newest first."""
    reports = []
    for p in PM_DIR.glob("MONITOR_*.md"):
        m = MONITOR_RE.match(p.name)
        if not m:
            continue
        yyyymmdd = m.group(1)
        date_str = f"{yyyymmdd[0:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"
        reports.append((date_str, yyyymmdd, p))
    reports.sort(key=lambda t: t[1], reverse=True)
    return reports


# ── inline markdown (bold / code / links) ───────────────────────────────────
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_CODE_RE = re.compile(r"`([^`]+)`")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def inline_md(text: str) -> str:
    text = html.escape(text, quote=False)

    code_spans = []

    def _stash_code(m):
        code_spans.append(m.group(1))
        return f"\x00CODE{len(code_spans) - 1}\x00"

    text = _CODE_RE.sub(_stash_code, text)
    text = _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    text = _BOLD_RE.sub(r"<strong>\1</strong>", text)

    def _restore_code(m):
        return f"<code>{code_spans[int(m.group(1))]}</code>"

    text = re.sub(r"\x00CODE(\d+)\x00", _restore_code, text)
    return text


# ── block-level markdown -> html ────────────────────────────────────────────
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_HR_RE = re.compile(r"^-{3,}$")
_OL_RE = re.compile(r"^(\d+)\.\s+(.*)$")
_UL_RE = re.compile(r"^[-*+]\s+(.*)$")
_TABLE_SEP_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?$")
_HEADING_TAG = {1: "h2", 2: "h3", 3: "h4", 4: "h5", 5: "h6", 6: "h6"}


def _is_table_sep(line: str) -> bool:
    return bool(_TABLE_SEP_RE.match(line.strip()))


def _split_row(line: str):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    s = s.replace("\\|", "\x00PIPE\x00")
    cells = [c.strip().replace("\x00PIPE\x00", "|") for c in s.split("|")]
    return [inline_md(c) for c in cells]


def _parse_table(lines, i):
    n = len(lines)
    header = _split_row(lines[i])
    i += 2  # header + separator row
    rows = []
    while i < n and lines[i].strip().startswith("|"):
        rows.append(_split_row(lines[i]))
        i += 1
    thead = "<tr>" + "".join(f"<th>{c}</th>" for c in header) + "</tr>"
    tbody = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows
    )
    out = f'<div class="tbl"><table><thead>{thead}</thead><tbody>{tbody}</tbody></table></div>'
    return out, i


def _parse_list(lines, i, indent=0):
    n = len(lines)
    ordered = None
    items = []
    while i < n:
        raw = lines[i]
        if not raw.strip():
            break
        cur_indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        if cur_indent < indent:
            break
        if cur_indent > indent:
            if not items:
                break
            if stripped.startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
                nested_html, i = _parse_table(lines, i)
            elif _OL_RE.match(stripped) or _UL_RE.match(stripped):
                nested_html, i = _parse_list(lines, i, indent=cur_indent)
            else:
                break
            items[-1] = items[-1][: -len("</li>")] + nested_html + "</li>"
            continue
        m_ol = _OL_RE.match(stripped)
        m_ul = _UL_RE.match(stripped)
        if m_ol and ordered is not False:
            ordered = True
            items.append(f"<li>{inline_md(m_ol.group(2))}</li>")
            i += 1
        elif m_ul and ordered is not True:
            ordered = False
            items.append(f"<li>{inline_md(m_ul.group(1))}</li>")
            i += 1
        else:
            break
    tag = "ol" if ordered else "ul"
    return f"<{tag}>{''.join(items)}</{tag}>", i


def md_to_html(md_text: str) -> str:
    lines = md_text.replace("\r\n", "\n").split("\n")
    n = len(lines)
    i = 0
    out = []
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            tag = _HEADING_TAG.get(level, "h6")
            out.append(f"<{tag}>{inline_md(m.group(2).strip())}</{tag}>")
            i += 1
            continue
        if _HR_RE.match(stripped):
            out.append("<hr>")
            i += 1
            continue
        if stripped.startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(inline_md(lines[i].strip()[1:].strip()))
                i += 1
            out.append("<blockquote>" + "<br>".join(quote_lines) + "</blockquote>")
            continue
        if stripped.startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            table_html, i = _parse_table(lines, i)
            out.append(table_html)
            continue
        if _OL_RE.match(stripped) or _UL_RE.match(stripped):
            list_html, i = _parse_list(lines, i, indent=0)
            out.append(list_html)
            continue
        out.append(f"<p>{inline_md(stripped)}</p>")
        i += 1
    return "\n".join(out)


# ── CJK + half-width punctuation normalization (post-render safety pass) ────
_CJK_CLASS = r"[㐀-䶿一-鿿豈-﫿]"
_PUNCT_MAP = {",": "，", ".": "。", ":": "：", ";": "；", "!": "！", "?": "？"}
_CJK_PUNCT_RE = re.compile(_CJK_CLASS + r"([,.:;!?])")
_SKIP_TAGS = {"script", "style", "code", "pre", "textarea"}
_TAG_SPLIT_RE = re.compile(r"(<[^>]+>)")
_TAG_NAME_RE = re.compile(r"^</?\s*([a-zA-Z][a-zA-Z0-9]*)")


def _cjk_punct_sub(m: re.Match) -> str:
    return m.group(0)[0] + _PUNCT_MAP[m.group(1)]


def normalize_punct(full_html: str) -> str:
    """Full-width-ify CJK-adjacent half-width , . : ; ! ? in text nodes only.

    Tag-aware: never touches tag markup/attributes, and never touches text
    inside <script>/<style>/<code>/<pre>/<textarea> (those are code/markup,
    not Chinese prose).
    """
    tokens = _TAG_SPLIT_RE.split(full_html)
    skip_depth = 0
    out = []
    for tok in tokens:
        if tok.startswith("<") and tok.endswith(">"):
            m = _TAG_NAME_RE.match(tok)
            name = m.group(1).lower() if m else ""
            is_close = tok.startswith("</")
            self_closing = tok.rstrip(">").endswith("/") or name in ("br", "hr", "img", "meta", "link")
            if name in _SKIP_TAGS and not self_closing:
                if is_close:
                    skip_depth = max(0, skip_depth - 1)
                else:
                    skip_depth += 1
            out.append(tok)
        else:
            if skip_depth > 0:
                out.append(tok)
            else:
                out.append(_CJK_PUNCT_RE.sub(_cjk_punct_sub, tok))
    return "".join(out)


# ── history list + head/foot template ───────────────────────────────────────
def render_history_list(reports, latest_yyyymmdd):
    items = []
    for date_str, yyyymmdd, _p in reports:
        label = f"{date_str}（最新）" if yyyymmdd == latest_yyyymmdd else date_str
        cur_cls = ' class="cur"' if yyyymmdd == latest_yyyymmdd else ""
        items.append(
            f'<li{cur_cls}><a href="/pm/MONITOR_{yyyymmdd}.md">{label}</a></li>'
        )
    return "\n".join(items)


HEAD_NAV = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>持倉週掃｜InvestMQuest Research</title>
<meta name="description" content="每週掃全持倉與近期研究 DD 的否證指標、催化劑時程、thesis 老化與產業 ID kill 門檻——手動/cron 觸發的分流報告索引。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/imq-base.css">
<style>
:root{--brand:#0d2244;--bg:#f7f3ea;--card:#fff;--text:#0c1521;--muted:#8a94a3;--border:#e5dfd0;
  --green:#15803d;--red:#b91c1c;--amber:#a16207;--blue:#1d4ed8;--r:12px}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:var(--bg);color:var(--text);line-height:1.7;font-size:14px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:960px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.6rem 0 1.2rem;background:var(--card);border-bottom:1px solid var(--border)}
.page-hdr h1{font-family:'Noto Serif TC',serif;font-size:1.55rem;font-weight:700}
.page-hdr .sub{color:var(--muted);font-size:.86rem;margin-top:.3rem;max-width:720px}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}.crumb a{color:var(--muted)}
.badge{display:inline-block;font-size:.72rem;font-weight:700;padding:.16rem .6rem;border-radius:99px;background:#e8eef5;color:var(--blue);margin-top:.5rem}
.hist{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1rem 1.2rem;margin:1.1rem 0}
.hist h3{font-size:.9rem;margin-bottom:.5rem}
.hist ul{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem}
.hist li a{font-size:.82rem;font-weight:600;padding:.3rem .7rem;border:1px solid var(--border);border-radius:6px;display:inline-block}
.hist li.cur a{background:var(--text);color:#fff;border-color:var(--text)}
.report{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.3rem 1.5rem;margin:1.1rem 0}
.report h2{font-family:'Noto Serif TC',serif;font-size:1.25rem;color:var(--brand);margin:1.1rem 0 .5rem;padding-bottom:.25rem;border-bottom:1px solid var(--border)}
.report h3{font-size:1.02rem;margin:.9rem 0 .4rem;color:var(--brand)}
.report h4{font-size:.92rem;margin:.7rem 0 .3rem}
.report h5{font-size:.85rem;margin:.6rem 0 .25rem;color:#41505f}
.report p{margin:.45rem 0;font-size:.88rem}
.report ul,.report ol{margin:.4rem 0 .6rem 1.4rem}
.report li{margin:.2rem 0;font-size:.87rem}
.report hr{border:0;border-top:1px solid var(--border);margin:1rem 0}
.report code{background:#f2efe6;padding:.05rem .3rem;border-radius:4px;font-size:.85em;font-family:ui-monospace,Menlo,monospace}
.report blockquote{border-left:3px solid var(--amber);background:#fbf3df;padding:.5rem .8rem;margin:.5rem 0;border-radius:6px;font-size:.86rem}
.report .tbl{overflow-x:auto;margin:.6rem 0}
.report table{width:100%;border-collapse:collapse;font-size:.8rem}
.report th,.report td{border:1px solid var(--border);padding:.4rem .55rem;text-align:left;vertical-align:top}
.report th{background:#faf7f0;font-weight:700;white-space:nowrap}
footer{background:var(--card);border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.1rem 0;font-size:.76rem;margin-top:1.4rem}
</style>
</head>
<body>
<style id="imq-nav-style">
.imq-nav-root{background:linear-gradient(135deg,#081832 0%,#173564 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.imq-nav-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.imq-logo{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}
.imq-logo:hover{color:#fff !important;text-decoration:none !important}
.imq-logo span{color:#d4b576}
.imq-menu{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.imq-menu > a,.imq-dd-btn{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}
.imq-menu > a:hover,.imq-dd-btn:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-dd{position:relative;display:inline-block}
.imq-dd-menu{display:none;position:absolute;top:100%;left:0;background:#0d2244;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(184,146,74,.20)}
.imq-dd-menu a.active{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
.imq-subnav{background:#081832;padding:.45rem 20px;font-family:'Inter','Noto Sans TC',-apple-system,sans-serif}
.imq-subnav-inner{max-width:1140px;margin:0 auto;display:flex;gap:.3rem;flex-wrap:wrap}
.imq-subnav a{color:rgba(255,255,255,.55) !important;font-size:.74rem;font-weight:500;padding:.28rem .6rem;border-radius:5px;text-decoration:none !important}
.imq-subnav a:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-subnav a.active{color:#fff !important;background:rgba(184,146,74,.30);font-weight:600}
@media(max-width:768px){
  .imq-nav-root{padding:.55rem 12px}
  .imq-nav-inner{gap:.4rem}
  .imq-menu{width:100%;justify-content:flex-start;gap:.1rem}
  .imq-menu > a,.imq-dd-btn{font-size:.74rem;padding:.32rem .5rem}
  .imq-dd-menu{position:static;display:none;min-width:auto;box-shadow:none;background:rgba(255,255,255,.04);border:none;padding:.1rem 0 .3rem 1rem;margin:.1rem 0}
  .imq-dd.open .imq-dd-menu{display:block}
}
</style>
<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/">首頁</a>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">市場<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/intel/">情報監視器</a>
          <a href="/briefing/">每日簡報</a>
          <a href="/rotation/radar.html">資產輪動雷達</a>
          <a href="/macro/">總經深度報告</a>
          <a href="/earnings/">財報分析</a>
          <a href="/markets.html">Markets</a>
          <a href="/sectors.html">Sectors</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">選股<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/cockpit/">選股主控台</a>
          <a href="/dd-screener/">DD Screener</a>
          <a href="/research/momentum-5/">Momentum-5</a>
          <a href="/qgm/">QGM 美股</a>
          <a href="/qgm-tw/">QGM 台股</a>
          <a href="/screeners.html">RS+VCP Screener</a>
        </div>
      </div>
      <div class="imq-dd">
        <button type="button" class="imq-dd-btn">研究<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/t/">個股總覽</a>
          <a href="/research/">個股 DD</a>
          <a href="/id/">產業深度 ID</a>
          <a href="/id/tier_matrix.html">Tier Matrix</a>
          <a href="/supply-chain/">供應鏈地圖</a>
          <a href="/comparisons/">多股對比</a>
          <a href="/research/synthesis/">期望落差綜合研判</a>
        </div>
      </div>
      <a href="/mental-models/">心智模型</a>
      <div class="imq-dd active">
        <button type="button" class="imq-dd-btn">系統<span class="imq-caret">▾</span></button>
        <div class="imq-dd-menu">
          <a href="/track-record/">裁決實績</a>
          <a href="/pm/" class="active">持倉週掃</a>
          <a href="/long-track-w52-adaptive/">實單主系統</a>
          <a href="/long-track/">追蹤總覽</a>
          <a href="/backtest/">量化回測</a>
          <a href="/tools/">期貨部位計算機</a>
          <a href="/data.html">公開資料</a>
        </div>
      </div>
      <a href="/flow/">投資流程</a>
      <a href="/how-to.html">使用指南</a>
      <a href="/search.html">搜尋</a>
    </nav>
  </div>
</header>
<script>(function(){document.querySelectorAll('.imq-dd-btn').forEach(function(btn){btn.addEventListener('click',function(e){e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open')})});document.addEventListener('click',function(e){if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){d.classList.remove('open')})});})();</script>
"""

FOOTER = """<footer>
  &copy; 2026 InvestMQuest Research · 持倉週掃 · 本頁為研究監控輸出，不構成投資建議
</footer>
</body>
</html>
"""


def render_index(reports):
    if not reports:
        raise SystemExit("no docs/pm/MONITOR_*.md found — nothing to render")

    latest_date, latest_yyyymmdd, latest_path = reports[0]
    latest_md = latest_path.read_text(encoding="utf-8")
    report_body_html = md_to_html(latest_md)

    now_tpe = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M 台北時間")
    hist_list_html = render_history_list(reports, latest_yyyymmdd)
    hist_count = len(reports)

    page = HEAD_NAV
    page += f'''<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/track-record/">系統</a> / 持倉週掃</div>
    <h1>持倉週掃</h1>
    <div class="sub">本報告逐一檢查每個持倉與近期研究 DD 的否證指標、催化劑時程、DD／ID 老化，並獨立掃每張產業 ID 的 kill 門檻，標出「沉默衰退」（催化劑錯過、指標破線、thesis 過半衰期、ID kill 門檻跨越）供人工重審。<b>手動 / cron 觸發，非即時。</b></div>
    <div class="badge">最新報告：{latest_date}　·　頁面更新 {now_tpe}</div>
  </div>
</div>
<div class="container">
<div class="hist"><h3>歷史週掃報告（共 {hist_count} 份）</h3><ul>{hist_list_html}
</ul><div style="font-size:.76rem;color:var(--muted);margin-top:.5rem">點日期開啟該週原始 Markdown 報告。</div></div>
<div class="report">{report_body_html}</div>
</div>
'''
    page += FOOTER
    return normalize_punct(page)


def main():
    reports = find_reports()
    out_html = render_index(reports)
    INDEX_PATH.write_text(out_html, encoding="utf-8")
    latest_date = reports[0][0]
    print(f"wrote {INDEX_PATH}")
    print(f"latest report: {latest_date}")
    print(f"history count: {len(reports)}")


if __name__ == "__main__":
    main()
