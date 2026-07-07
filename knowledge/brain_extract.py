#!/usr/bin/env python3
"""
brain_extract.py — 第二大腦抽取層（純函數，無寫入副作用）。

把各內容家族（DD/DCA/ID/earnings/comparisons/synthesis/monitors/supply-chain/
briefing/weekly/qgm/策略規則/internal notes/外部 repo md）的檔案抽成統一 note dict：

  {id, type, entity?, theme?, title, date?, verdict?, grade?, oneliner?,
   tags[], source, url?, parse_level, sections: [(sec_id, heading, text)]}

HTML 解析走 stdlib html.parser（repo 慣例：不加 bs4/lxml）。
切段 fallback 鏈：h2 標題 → 舊版 div.section-title → 整篇單 chunk，絕不 crash。

由 brain_build.py 呼叫；discover() 回傳 (source_path, family, extractor) 清單，
extractor 只在檔案變動時才被呼叫（增量由 build 端的 mtime cache 控制）。
"""
import ast
import glob
import json
import os
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = "https://research.investmquest.com"

# 與 build_knowledge.py 同一條 canonical regex
DD_META_RE = re.compile(r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL)
ID_META_RE = re.compile(r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL)

# 外部 repo registry：repo 目錄名（在 $HOME 下）→ 知識文件 globs（md ＋ 站點內容 html）。
# 加新 repo = 加一行；目錄不存在時 build 端 warn 跳過（兩台 Mac 容錯）。
SIBLING_REPOS = {
    "v7-backtest": ["docs/*.md", "results/**/report.md", "README.md", "CLAUDE.md"],
    "minervini-quality-backtest": ["SPEC.md", "README.md", "docs/*.md"],
    "morning-briefing": ["SYSTEM_BLUEPRINT.md", "CLAUDE.md", "context.md",
                          "CHANGELOG.md", "README.md", "briefing/CLAUDE.md"],
    # tools.investmquest.com：history/ 城市史詩 + 各國置產工具頁 + docs/dd
    "tools": ["CLAUDE.md", "CONTEXT.md", "README.md", "UPDATE_GUIDE.md",
              "MAINTENANCE.md", "data/*.md", "**/*.html"],
    # myproperty.investmquest.com：kl/ 物件 DD + kl-check + my/
    "malaysia-property": ["CLAUDE.md", "CONTEXT.md", "README.md", "UPDATE_GUIDE.md",
                           "MAINTENANCE.md", "data/*.md", "**/*.html"],
    "dotfiles": ["README.md", "claude/CLAUDE.md"],
}
SIBLING_EXCLUDE = {"gemini_review_bundle.md", "404.html"}  # 噪音
# 站點內容 html 的垃圾規則：建置中間物 / 舊版堆 / 樣板 / 測試頁
SIBLING_JUNK_DIRS = {"demo", "templates", "archive", "node_modules", "css", "js"}
# 各 repo 對應的公開站（頁面「線上版」連結用）
SIBLING_URL = {
    "tools": "https://tools.investmquest.com",
    "malaysia-property": "https://myproperty.investmquest.com",
}
SIBLING_HTML_TYPE = {"tools": "tools", "malaysia-property": "property"}


def _sibling_junk(root, path):
    rel = Path(path).relative_to(root)
    if any(part.startswith("_") or part in SIBLING_JUNK_DIRS for part in rel.parts):
        return True
    return rel.name.startswith("test")


# ─────────────────────────── HTML → sections ───────────────────────────

_SKIP_TAGS = {"script", "style", "nav", "header", "footer", "svg", "noscript"}
_BLOCK_TAGS = {"p", "div", "li", "tr", "br", "table", "ul", "ol", "section",
               "article", "aside", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote"}


class SectionTextParser(HTMLParser):
    """把 HTML 流切成 [(sec_id, heading, text)]。

    section 邊界＝<h2>（所有世代報告的共同骨架），或舊版 DD/DCA 的
    <div class="section-title">。h2 之前的內容進「導言」section。
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self._skip_depth = 0
        self._heading_mode = None      # None | "h2" | "sectitle"
        self._heading_buf = []
        self._heading_id = ""
        self._buf = []
        self._cur_heading = ""
        self._cur_id = ""
        self.sections = []             # [(sec_id, heading, text)]
        self.h2_count = 0
        self.sectitle_count = 0

    # -- helpers --
    def _flush(self):
        text = _normalize("".join(self._buf))
        if text or self._cur_heading:
            self.sections.append((self._cur_id, self._cur_heading, text))
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        ad = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "h2":
            self._flush()
            self._heading_mode = "h2"
            self._heading_buf = []
            self._heading_id = ad.get("id", "")
            self.h2_count += 1
        elif tag == "div" and "section-title" in (ad.get("class") or ""):
            self._flush()
            self._heading_mode = "sectitle"
            self._heading_buf = []
            self._heading_id = ad.get("id", "")
            self.sectitle_count += 1
        elif tag in _BLOCK_TAGS:
            self._buf.append("\n")
        elif tag in ("td", "th"):
            self._buf.append(" | ")

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return
        if tag == "title":
            self._in_title = False
        elif (tag == "h2" and self._heading_mode == "h2") or \
             (tag == "div" and self._heading_mode == "sectitle"):
            self._cur_heading = _normalize(" ".join(self._heading_buf))
            self._cur_id = self._heading_id
            self._heading_mode = None
        elif tag in _BLOCK_TAGS:
            self._buf.append("\n")

    def handle_data(self, data):
        if self._skip_depth:
            return
        if self._in_title:
            self.title += data
        elif self._heading_mode:
            self._heading_buf.append(data)
        else:
            self._buf.append(data)

    def close(self):
        super().close()
        self._flush()


def _normalize(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[ \t　]+", " ", s)
    s = re.sub(r" ?\n ?", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# 舊世代頁面的 legacy nav 是 inline-style <div>（非 header/nav tag），tag 層濾不掉；
# 導言段用文字層過濾：純選單字行 + logo 行。內容段落不會是一行孤立的「首頁」。
_CHROME_LABELS = {
    "首頁", "每日簡報", "週報", "回測", "六狀態機", "財報分析", "研究", "市場", "量化",
    "選股駕駛艙", "個股 DD", "期望落差綜合研判", "產業深度 ID", "多股對比", "供應鏈地圖",
    "擁擠交易監測", "產業輪動", "大類資產 regime", "精選清單", "Momentum-5",
    "🎯 Tier Matrix", "Tier Matrix", "美股 QGM", "台股 QGM", "DD Screener", "選股 SOP",
    "知識庫", "工具",
}


def _strip_chrome(text):
    out = []
    for line in text.splitlines():
        s = line.strip().rstrip("▾").strip()
        if "InvestMQuest" in s or s in _CHROME_LABELS or s == "☰" \
                or s.startswith(("←返回", "← 返回")):
            continue
        out.append(line)
    return "\n".join(out).strip()


def html_to_sections(html):
    """回傳 (title, sections, parse_level)。fallback 鏈保證永遠有輸出。"""
    p = SectionTextParser()
    try:
        p.feed(html)
        p.close()
    except Exception:
        # 極端破損 HTML：暴力剝 tag 整篇
        text = _normalize(re.sub(r"<[^>]+>", " ", re.sub(
            r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)))
        return "", [("", "", _strip_chrome(text))], "body"
    secs = [(sid, h, t) for sid, h, t in p.sections if t or h]
    if secs:  # chrome 只會出現在第一個 heading 之前的導言段
        sid0, h0, t0 = secs[0]
        secs[0] = (sid0, h0, _strip_chrome(t0))
        if not (secs[0][1] or secs[0][2]):
            secs = secs[1:]
    if p.h2_count >= 2:
        level = "h2"
    elif p.sectitle_count >= 2:
        level = "sectitle"
    else:
        level = "body"
    if not secs:
        secs = [("", "", "")]
    return _normalize(p.title), secs, level


# ─────────────────────────── 共用小工具 ───────────────────────────

def _read(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def _meta_from(html, regex):
    m = regex.search(html)
    if not m:
        return None
    try:
        return json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None


def _date_from_name(name):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", name)
    if m:
        return m.group(1)
    m = re.search(r"_(\d{8})(?:_full)?\.\w+$", name) or re.search(r"_(\d{8})_", name)
    if m:
        s = m.group(1)
        return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"
    return None


def _rel(path):
    return os.path.relpath(str(path), str(REPO))


def _url(path):
    r = _rel(path)
    return SITE + "/" + r[len("docs/"):] if r.startswith("docs/") else None


def md_to_sections(text):
    """markdown 依 ## 切段；## 之前進導言。"""
    secs, cur_h, buf = [], "", []
    for line in text.splitlines():
        m = re.match(r"##\s+(.*)", line)
        if m and not line.startswith("###"):
            if buf or cur_h:
                secs.append(("", cur_h, "\n".join(buf).strip()))
            cur_h, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    if buf or cur_h:
        secs.append(("", cur_h, "\n".join(buf).strip()))
    return [(s, h, t) for s, h, t in secs if h or t] or [("", "", "")]


def _note(nid, ntype, title, source, sections, parse_level, **kw):
    d = {"id": nid, "type": ntype, "title": title, "source": source,
         "sections": sections, "parse_level": parse_level}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ─────────────────────────── 家族 extractors ───────────────────────────
# 每個 extractor(path) → [note dict]；discover() 只列檔不讀內容
#（ID 家族例外：需 2KB sniff 判 redirect stub / _full 去重）。

def ex_dd(path):
    html = _read(path)
    meta = _meta_from(html, DD_META_RE) or {}
    title, secs, level = html_to_sections(html)
    base = os.path.basename(path)
    ticker = meta.get("ticker") or base.split("_")[1]
    d = meta.get("date") or _date_from_name(base)
    return [_note(
        f"dd-{ticker}-{(d or '').replace('-', '')}", "dd",
        title or base, _rel(path), secs,
        ("meta+" + level) if meta else level,
        entity=ticker, date=d,
        verdict=meta.get("dca_verdict"),
        grade=meta.get("signal"),
        oneliner=meta.get("oneliner"),
        extra={k: meta[k] for k in ("schema", "dca_role", "moat_trend", "archetype",
                                     "long_term_confidence") if meta.get(k)},
        url=_url(path),
    )]


def ex_dca(path):
    html = _read(path)
    title, secs, level = html_to_sections(html)
    base = os.path.basename(path)
    parts = base.replace(".html", "").split("_")
    ticker = parts[1] if len(parts) > 1 else ""
    d = _date_from_name(base)
    return [_note(
        f"dca-{ticker}-{(d or '').replace('-', '')}", "dca",
        title or base, _rel(path), secs, level,
        entity=ticker, date=d, extra={"status": "archived"}, url=_url(path),
    )]


def ex_id(path):
    html = _read(path)
    meta = _meta_from(html, ID_META_RE) or {}
    title, secs, level = html_to_sections(html)
    base = os.path.basename(path)
    theme = meta.get("theme") or re.sub(r"^ID_|_\d{8}.*", "", base)
    d = meta.get("publish_date") or _date_from_name(base)
    return [_note(
        f"id-{re.sub(r'[^A-Za-z0-9]+', '', base.split('_')[1])}-{(d or '').replace('-', '')}",
        "id", title or theme, _rel(path), secs,
        ("meta+" + level) if meta else level,
        theme=theme, date=d,
        verdict=meta.get("sd_verdict"),
        oneliner=meta.get("oneliner"),
        tags=[t for t in (meta.get("thesis_type"), meta.get("sub_group")) if t],
        extra={k: meta[k] for k in ("skill_version", "clock_phase", "conviction",
                                     "action", "now_state") if meta.get(k)},
        related_tickers=[rt.get("ticker") for rt in meta.get("related_tickers", [])
                         if rt.get("ticker")],
        url=_url(path),
    )]


def _ex_simple_html(path, ntype, subdir_tag=None):
    html = _read(path)
    title, secs, level = html_to_sections(html)
    base = os.path.basename(path)
    d = _date_from_name(base)
    return [_note(
        f"{ntype}-{re.sub(r'[^A-Za-z0-9._-]+', '', base.replace('.html', ''))}",
        ntype, title or base, _rel(path), secs, level,
        date=d, tags=[subdir_tag] if subdir_tag else None, url=_url(path),
    )]


def ex_earnings(path):
    base = os.path.basename(path)
    notes = _ex_simple_html(path, "earnings")
    m = re.match(r"(?:preview|earnings)_([A-Z0-9.]+)_", base)
    if m:
        notes[0]["entity"] = m.group(1)
    return notes


def ex_comparison(path):
    notes = _ex_simple_html(path, "comparison")
    base = os.path.basename(path).replace(".html", "")
    body = re.sub(r"^MS_|_\d{8}$", "", base)
    tickers = [t for t in re.split(r"vs|_", body) if t]
    notes[0]["tickers"] = tickers
    return notes


def ex_synthesis(path):
    notes = _ex_simple_html(path, "synthesis")
    m = re.match(r"([A-Z0-9.]+)_\d{8}", os.path.basename(path))
    if m:
        notes[0]["entity"] = m.group(1)
    return notes


def ex_monitor(path):
    kind = _rel(path).split("/")[1]  # crowding / regime / rotation
    return _ex_simple_html(path, "monitor", subdir_tag=kind)


def ex_supply_chain(path):
    data = json.loads(_read(path))
    tid = data.get("id") or Path(path).stem
    secs = []
    tickers = set()
    for nd in data.get("nodes", []):
        parts = [nd.get("desc") or "", nd.get("analysis") or ""]
        cos = nd.get("companies", [])
        if cos:
            parts.append("廠商：" + "、".join(
                f"{c.get('name', '')}({c.get('ticker', '')})" for c in cos))
            for c in cos:
                for tk in re.split(r"[/,、]", (c.get("ticker") or "")):
                    tk = tk.strip()
                    if tk and tk not in {"—", "-", "–", "N/A", "n/a", "未上市"}:
                        tickers.add(tk)
        srcs = nd.get("sources") or []
        if srcs:
            parts.append("來源：" + "；".join(str(s) for s in srcs[:6]))
        secs.append((nd.get("id") or "", nd.get("name") or "", _normalize("\n".join(p for p in parts if p))))
    return [_note(
        f"sc-{tid}", "supplychain", data.get("title") or tid, _rel(path),
        secs or [("", "", "")], "json",
        theme=tid, oneliner=data.get("subtitle"),
        related_tickers=sorted(tickers),
        url=f"{SITE}/supply-chain/{tid}.html",
    )]


def ex_briefing(path):
    ntype = "briefing" if "/briefing/" in str(path) else "weekly"
    return _ex_simple_html(path, ntype)


def ex_qgm(path):
    data = json.loads(_read(path))
    which = "qgm-tw" if "qgm-tw" in str(path) else "qgm"
    summary = data.get("summary") or {}
    lines = [f"run: {data.get('run_timestamp', '')}  universe: {data.get('universe_size', '')}"]
    lines.append("summary: " + json.dumps(summary, ensure_ascii=False))
    for c in (data.get("candidates") or [])[:40]:
        lines.append(f"- {c.get('ticker', '')}: pool={c.get('pool', '')} "
                     f"quality={c.get('quality_score', '')}")
    return [_note(
        f"{which}-latest", "qgm", f"{which.upper()} 最新篩選", _rel(path),
        [("", "候選清單", "\n".join(lines))], "json",
        url=_url(path).replace("latest.json", "latest.html") if _url(path) else None,
    )]


def ex_markdown(path, ntype, nid_prefix, tag=None):
    text = _read(path)
    secs = md_to_sections(text)
    base = os.path.basename(path)
    m = re.match(r"#\s+(.+)", text.lstrip()[:200])
    title = m.group(1).strip() if m else base
    src = str(path)
    src = _rel(src) if str(REPO) in src else src.replace(str(Path.home()), "~")
    return [_note(
        f"{nid_prefix}-{re.sub(r'[^A-Za-z0-9._-]+', '-', base.replace('.md', ''))}",
        ntype, title, src, secs, "md",
        date=_date_from_name(base), tags=[tag] if tag else None,
    )]


def ex_strategy_md(path):
    return ex_markdown(path, "strategy", "strategy")


def ex_skill(path):
    skill = Path(path).parent.name
    notes = ex_markdown(path, "strategy", f"skill-{skill}", tag="skill")
    notes[0]["title"] = f"SKILL: {skill}"
    return notes


def ex_py_docstring(path):
    try:
        doc = ast.get_docstring(ast.parse(_read(path))) or ""
    except SyntaxError:
        doc = ""
    if not doc.strip():
        return []
    base = os.path.basename(path)
    return [_note(
        f"engine-{base.replace('.py', '')}", "strategy",
        f"engine: {base}", _rel(path),
        [("", "module docstring", _normalize(doc))], "py", tags=["engine"],
    )]


def ex_data_summary(path):
    """picks / turtle-sleeve 等 JSON：只留指標摘要，不進全文。"""
    try:
        data = json.loads(_read(path))
    except json.JSONDecodeError:
        return []
    preview = json.dumps(data, ensure_ascii=False, indent=1)
    if len(preview) > 2500:
        preview = preview[:2500] + "\n…(截斷)"
    base = _rel(path)
    return [_note(
        f"data-{re.sub(r'[^A-Za-z0-9._-]+', '-', base)}", "strategy",
        f"data: {base}", base,
        [("", "摘要", preview)], "json", tags=["data"], url=_url(path),
    )]


def ex_internal_note(path):
    sub = _rel(path).split("/")  # notes/site-internal/<area>/x.md
    area = sub[2] if len(sub) > 3 else "root"
    return ex_markdown(path, "internal-note", f"note-{area}", tag=area)


def _sibling_ex(repo_name):
    def ex(path):
        p = Path(path)
        root = Path.home() / repo_name
        rel = p.relative_to(root)
        slug = re.sub(r"[^A-Za-z0-9._-]+", "-", str(rel.with_suffix("")).replace("/", "--"))
        site = SIBLING_URL.get(repo_name)
        if p.suffix == ".html":
            title, secs, level = html_to_sections(_read(path))
            note = _note(
                f"kb-{repo_name}-{slug}",
                SIBLING_HTML_TYPE.get(repo_name, "repo-doc"),
                title or rel.stem, str(path).replace(str(Path.home()), "~"),
                secs, level, date=_date_from_name(p.name), tags=[repo_name],
                url=f"{site}/{rel}" if site else None)
        else:
            ntype = "whitepaper" if repo_name in (
                "v7-backtest", "minervini-quality-backtest") else "repo-doc"
            note = ex_markdown(path, ntype, f"kb-{repo_name}", tag=repo_name)[0]
            note["id"] = f"kb-{repo_name}-{slug}"
            if p.name.lower() == "report.md":
                note["title"] = f"{p.parent.name} — {note['title']}"
        note["repo"] = repo_name
        # vault 內保留子目錄結構，避免 us/demand.html 與 tw/demand.html 撞名
        note["kbrel"] = str(rel.parent) if str(rel.parent) != "." else ""
        return [note]
    return ex


# ─────────────────────────── discovery ───────────────────────────

def _is_id_stub_or_dupe(path, all_names):
    """redirect stub（首 2KB 有 meta refresh）或有 _full 版的 base 檔 → 跳過。"""
    base = os.path.basename(path)
    if not base.endswith("_full.html"):
        if base.replace(".html", "_full.html") in all_names:
            return True
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(2048)
        if 'http-equiv="refresh"' in head:
            return True
    except OSError:
        return True
    return False


def discover():
    """回傳 [(abs_path, family, extractor)]。只列檔＋ID 家族 2KB sniff，不做全文讀取。"""
    out = []

    def add(pattern, family, ex, exclude=None):
        for f in sorted(glob.glob(str(REPO / pattern), recursive=True)):
            b = os.path.basename(f)
            if b == "index.html" or (exclude and exclude(f)):
                continue
            out.append((f, family, ex))

    add("docs/dd/DD_*.html", "dd", ex_dd)
    add("docs/dca/DCA_*.html", "dca", ex_dca)

    id_files = sorted(glob.glob(str(REPO / "docs/id/ID_*.html")))
    id_names = {os.path.basename(f) for f in id_files}
    for f in id_files:
        if not _is_id_stub_or_dupe(f, id_names):
            out.append((f, "id", ex_id))

    add("docs/earnings/*.html", "earnings", ex_earnings)
    add("docs/comparisons/MS_*.html", "comparison", ex_comparison)
    add("docs/research/synthesis/*.html", "synthesis", ex_synthesis)
    for sub in ("crowding", "regime", "rotation"):
        add(f"docs/{sub}/*.html", "monitor", ex_monitor)
    add("docs/supply-chain/data/*.json", "supplychain", ex_supply_chain,
        exclude=lambda f: os.path.basename(f) in ("topics.json", "dd_links.json"))
    add("docs/briefing/[0-9]*.html", "briefing", ex_briefing)
    add("docs/weekly/*.html", "weekly", ex_briefing)
    for q in ("docs/qgm/latest.json", "docs/qgm-tw/latest.json"):
        p = REPO / q
        if p.exists():
            out.append((str(p), "qgm", ex_qgm))

    # 策略規則層
    p = REPO / "CLAUDE.md"
    if p.exists():
        out.append((str(p), "strategy", ex_strategy_md))
    add(".claude/skills/*/SKILL.md", "strategy", ex_skill)
    add("scripts/engine/*.py", "strategy", ex_py_docstring,
        exclude=lambda f: os.path.basename(f).startswith(("test_", "__")))
    add("scripts/sop_funnel/*.py", "strategy", ex_py_docstring,
        exclude=lambda f: os.path.basename(f).startswith(("test_", "__")))
    for dp in ("docs/picks/picks.json", "docs/picks/candidates.json",
               "docs/picks/tenbagger.json", "docs/turtle-sleeve/state.json"):
        p = REPO / dp
        if p.exists():
            out.append((str(p), "strategy", ex_data_summary))

    add("notes/site-internal/**/*.md", "internal-note", ex_internal_note)

    # 外部 repo（registry；缺目錄由 build 端 warn）
    home = Path.home()
    for repo_name, patterns in SIBLING_REPOS.items():
        root = home / repo_name
        if not root.is_dir():
            out.append((str(root), "__missing_repo__", None))
            continue
        seen = set()
        for pat in patterns:
            for f in sorted(glob.glob(str(root / pat), recursive=True)):
                if os.path.basename(f) in SIBLING_EXCLUDE or f in seen \
                        or not os.path.isfile(f) or _sibling_junk(root, f):
                    continue
                seen.add(f)
                out.append((f, f"kb:{repo_name}", _sibling_ex(repo_name)))

    return out
