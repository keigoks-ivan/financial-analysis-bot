#!/usr/bin/env python3
"""Build docs/pm/index.html — the 持倉週掃 (position-thesis-monitor) report index.

Scans docs/pm/MONITOR_YYYYMMDD.md (weekly triage reports produced by the
position-thesis-monitor agent, manually / cron triggered), renders the newest
one to HTML with a lightweight line-based markdown converter, and lists the
full history. The page carries a <body> so scripts/site_nav.py injects the
canonical site nav after it (pm/ is mapped to ('system','pm') in PREFIX_ACTIVE;
pm/index.html was removed from SKIP_FILES on 2026-07-19).

Idempotent. Re-run whenever a new MONITOR_*.md lands:
    python3 scripts/build_pm_index.py
"""
from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path

PM = Path(__file__).resolve().parent.parent / "docs" / "pm"
OUT = PM / "index.html"


def _fmt_date(stem: str) -> str:
    m = re.search(r"(\d{4})(\d{2})(\d{2})", stem)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else stem


def md_to_html(md: str) -> str:
    """Line-based, HTML-escaping markdown → HTML. Handles #/##/###/#### headings,
    ---/*** hr, unordered lists (-/*/+), ordered lists, | tables |, > quotes,
    inline **bold** / *italic* / `code` / [text](url). Safe: escape first."""
    def inline(t: str) -> str:
        t = html.escape(t, quote=False)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
        return t

    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    list_open = None  # 'ul' | 'ol' | None

    def close_list():
        nonlocal list_open
        if list_open:
            out.append(f"</{list_open}>")
            list_open = None

    while i < n:
        ln = lines[i]
        raw = ln.rstrip()
        # table block: a line with | followed by a |---| separator
        if raw.lstrip().startswith("|") and i + 1 < n and re.match(r"\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            close_list()
            header = [c.strip() for c in raw.strip().strip("|").split("|")]
            out.append('<div class="tbl"><table><thead><tr>'
                        + "".join(f"<th>{inline(c)}</th>" for c in header)
                        + "</tr></thead><tbody>")
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table></div>")
            continue
        m = re.match(r"(#{1,4})\s+(.*)$", raw)
        if m:
            close_list()
            lvl = len(m.group(1))
            out.append(f"<h{lvl+1}>{inline(m.group(2))}</h{lvl+1}>")
            i += 1
            continue
        if re.match(r"\s*([-*_])\1?\1?\s*$", raw) and set(raw.strip()) <= {"-", "*", "_"} and len(raw.strip()) >= 3:
            close_list()
            out.append("<hr>")
            i += 1
            continue
        m = re.match(r"\s*[-*+]\s+(.*)$", raw)
        if m:
            if list_open != "ul":
                close_list()
                out.append("<ul>")
                list_open = "ul"
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue
        m = re.match(r"\s*\d+[.)]\s+(.*)$", raw)
        if m:
            if list_open != "ol":
                close_list()
                out.append("<ol>")
                list_open = "ol"
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue
        m = re.match(r"\s*>\s?(.*)$", raw)
        if m:
            close_list()
            out.append(f"<blockquote>{inline(m.group(1))}</blockquote>")
            i += 1
            continue
        if raw.strip() == "":
            close_list()
            i += 1
            continue
        close_list()
        out.append(f"<p>{inline(raw)}</p>")
        i += 1
    close_list()
    return "\n".join(out)


CSS = """<style>
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
</style>"""


def build() -> str:
    reports = sorted(PM.glob("MONITOR_*.md"), reverse=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if not reports:
        body_report = '<div class="report"><p>目前無週掃報告。position-thesis-monitor 產出後會列於此。</p></div>'
        hist = ""
        latest_date = "—"
    else:
        latest = reports[0]
        latest_date = _fmt_date(latest.stem)
        body_report = f'<div class="report">{md_to_html(latest.read_text(encoding="utf-8"))}</div>'
        items = ""
        for idx, r in enumerate(reports):
            cur = ' class="cur"' if idx == 0 else ""
            items += f'<li{cur}><a href="/pm/{r.name}">{_fmt_date(r.stem)}{"（最新）" if idx == 0 else ""}</a></li>\n'
        hist = (f'<div class="hist"><h3>歷史週掃報告（共 {len(reports)} 份）</h3>'
                f'<ul>{items}</ul>'
                f'<div style="font-size:.76rem;color:var(--muted);margin-top:.5rem">點日期開啟該週原始 Markdown 報告。</div></div>')
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>持倉週掃｜InvestMQuest Research</title>
<meta name="description" content="position-thesis-monitor 每週掃全持倉與近期研究 DD 的否證指標、催化劑時程、thesis 老化與產業 ID kill 門檻——手動/cron 觸發的分流報告索引。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/imq-base.css">
{CSS}
</head>
<body>
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/track-record/">系統</a> / 持倉週掃</div>
    <h1>持倉週掃</h1>
    <div class="sub">position-thesis-monitor 週掃輸出：逐一檢查每個持倉與近期研究 DD 的否證指標、催化劑時程、DD／ID 老化，並獨立掃每張產業 ID 的 kill 門檻，標出「沉默衰退」（催化劑錯過、指標破線、thesis 過半衰期、ID kill 門檻跨越）供人工重審。<b>手動 / cron 觸發，非即時。</b></div>
    <div class="badge">最新報告：{latest_date}　·　頁面更新 {now}</div>
  </div>
</div>
<div class="container">
{hist}
{body_report}
</div>
<footer>
  &copy; {datetime.now().year} InvestMQuest Research · 持倉週掃（position-thesis-monitor）· 本頁為研究監控輸出，不構成投資建議
</footer>
</body>
</html>
"""


def main():
    OUT.write_text(build(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
