#!/usr/bin/env python3
"""learn/ course tooling — 股票分析完整框架 (research.investmquest.com/learn/)

Subcommands
  scaffold [NN ...]   write skeleton pages (nav / header / ribbon / pager / footer
                      generated from manifest.json). Only the region between
                      <!-- BODY:START --> … <!-- BODY:END --> (and SCRIPT markers)
                      is authored by writers. Never overwrites an existing page
                      unless --force.
  index               rebuild docs/learn/index.html course map section between
                      <!-- MAP:START --> … <!-- MAP:END --> from manifest.
  review              extract every module's data-quiz into docs/learn/review-bank.json
  qc [files ...]      quality gate: skeleton integrity (links), lang-span parity,
                      quiz/predict JSON validity, CJK punctuation, forbidden
                      (personalised / internal-jargon) words, dead links,
                      required blocks, size band. Non-zero exit on failure.

Everything is stdlib-only.
"""
import json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "learn"
MANIFEST = json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))
MODS = MANIFEST["modules"]
PARTS = {p["key"]: p for p in MANIFEST["parts"]}
PART_ORDER = [p["key"] for p in MANIFEST["parts"]]
BY_NUM = {m["num"]: m for m in MODS}

BODY_START, BODY_END = "<!-- BODY:START -->", "<!-- BODY:END -->"
SCRIPT_START, SCRIPT_END = "<!-- SCRIPT:START -->", "<!-- SCRIPT:END -->"


def esc(s):
    return html.escape(s, quote=True)


def bi(en, zh, tag="span", cls=""):
    c = (" " + cls) if cls else ""
    return (f'<{tag} class="lang-en{c}">{en}</{tag}>'
            f'<{tag} class="lang-zh{c}" style="display:none">{zh}</{tag}>')


def nav_block(prev, nxt):
    def link(m, arrow_left):
        if not m:
            return f'<a href="#" class="disabled">{"&larr; " if arrow_left else ""}{bi("Prev" if arrow_left else "Next", "上一課" if arrow_left else "下一課")}{"" if arrow_left else " &rarr;"}</a>'
        return (f'<a href="{m["file"]}">{"&larr; " if arrow_left else ""}'
                f'{bi("Prev" if arrow_left else "Next", "上一課" if arrow_left else "下一課")}'
                f'{"" if arrow_left else " &rarr;"}</a>')
    return f'''<nav class="course-nav">
  <div class="course-nav-inner">
    <div class="course-nav-brand">
      <a href="/">&larr; {bi("Research Home", "研究站首頁")}</a>
      <span class="course-nav-sep">/</span>
      <a href="/learn/index.html" class="course-nav-home">{bi("Course Home", "課程首頁")}</a>
      <span class="course-nav-sep">/</span>
      <a href="/learn/review.html">{bi("Review Deck", "複習牌組")}</a>
    </div>
    <div class="course-nav-pager">
      {link(prev, True)}
      {link(nxt, False)}
    </div>
    <div class="course-nav-lang">
      <button class="lang-btn" data-lang="zh" onclick="setLang('zh')">中文</button>
      <button class="lang-btn" data-lang="en" onclick="setLang('en')">EN</button>
    </div>
  </div>
</nav>'''


def ribbon(m):
    steps = []
    for k in PART_ORDER:
        p = PARTS[k]
        short_en = p["en"].split("·")[-1].strip() if "·" in p["en"] else p["en"]
        short_zh = p["zh"].split("・")[-1].strip() if "・" in p["zh"] else p["zh"]
        cls = "fw-ribbon-step active" if k == m["part"] else "fw-ribbon-step"
        steps.append(f'<span class="{cls}">{bi(short_en, short_zh)}</span>')
    p = PARTS[m["part"]]
    return (f'<div class="fw-ribbon"><span class="fw-ribbon-label">{bi("Where you are in the framework", "你在框架的哪一層")}</span>'
            + "".join(steps)
            + f'<span class="fw-ribbon-q">{bi(p["q_en"], p["q_zh"])}</span></div>')


def pager_block(prev, nxt):
    def cell(m, is_next):
        if not m:
            return '<span></span>'
        cls = ' class="lc-pager-next"' if is_next else ''
        return (f'<a href="{m["file"]}"{cls}>'
                f'<span class="lc-pager-dir lang-en">{"Next" if is_next else "Previous"}</span>'
                f'<span class="lc-pager-dir lang-zh" style="display:none">{"下一課" if is_next else "上一課"}</span>'
                f'<div class="lc-pager-label lang-en">{m["num"]} · {esc(m["en"])}</div>'
                f'<div class="lc-pager-label lang-zh" style="display:none">{m["num"]}・{esc(m["zh"])}</div></a>')
    return f'<div class="lc-pager">\n    {cell(prev, False)}\n    {cell(nxt, True)}\n  </div>'


def head_block(m):
    title = f'{m["num"]} · {esc(m["en"])}｜{esc(m["zh"])} | {esc(MANIFEST["course"]["title_zh"])} | InvestMQuest'
    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="DESCRIPTION_PLACEHOLDER">
<meta name="color-scheme" content="light">
<link rel="stylesheet" href="/learn/learn.css">
</head>
<body>'''


def skeleton(m, body="", script="", desc=None):
    i = MODS.index(m)
    prev = MODS[i - 1] if i > 0 else None
    nxt = MODS[i + 1] if i + 1 < len(MODS) else None
    part = PARTS[m["part"]]
    head = head_block(m)
    if desc:
        head = head.replace("DESCRIPTION_PLACEHOLDER", esc(desc))
    return f'''{head}

{nav_block(prev, nxt)}

<div class="lc-wrap">

  <header class="module-header">
    <span class="module-eyebrow lang-en">MODULE {m["num"]} · {esc(part["en"])}</span>
    <span class="module-eyebrow lang-zh" style="display:none">第 {m["num"]} 課・{esc(part["zh"])}</span>
    <h1 class="lang-en">{esc(m["en"])}</h1>
    <h1 class="lang-zh" style="display:none">{esc(m["zh"])}</h1>
    {ribbon(m)}
  </header>

  {BODY_START}{body}{BODY_END}

  {pager_block(prev, nxt)}

  <footer class="lc-footer">
    <a href="/learn/index.html"><span class="lang-en">&larr; Course Home</span><span class="lang-zh" style="display:none">&larr; 課程首頁</span></a>
    <span class="lc-footer-note">INVESTMQUEST &middot; LEARN &middot; MODULE {m["num"]}</span>
  </footer>

</div>

<script src="/learn/learn.js"></script>
{SCRIPT_START}{script}{SCRIPT_END}
</body>
</html>
'''


BODY_PLACEHOLDER = '''
  <!-- WRITER: replace everything between BODY:START and BODY:END. Keep the .module-goals block first. -->
  <div class="module-goals">
    <div class="module-goals-title"><span class="lang-en">What You'll Learn</span><span class="lang-zh" style="display:none">這一課學什麼</span></div>
    <ul>
      <li><span class="lang-en">TODO</span><span class="lang-zh" style="display:none">TODO</span></li>
    </ul>
  </div>
  '''


def split_regions(text):
    b0, b1 = text.find(BODY_START), text.find(BODY_END)
    s0, s1 = text.find(SCRIPT_START), text.find(SCRIPT_END)
    if min(b0, b1, s0, s1) < 0 or b1 < b0 or s1 < s0:
        return None
    body = text[b0 + len(BODY_START):b1]
    script = text[s0 + len(SCRIPT_START):s1]
    m = re.search(r'<meta name="description" content="([^"]*)">', text)
    desc = html.unescape(m.group(1)) if m else None
    return body, script, desc


# --------------------------------------------------------------- scaffold
def cmd_scaffold(args):
    force = "--force" in args
    nums = [a for a in args if re.fullmatch(r"\d\d", a)] or [m["num"] for m in MODS]
    DOCS.mkdir(parents=True, exist_ok=True)
    for n in nums:
        m = BY_NUM[n]
        p = DOCS / m["file"]
        if p.exists() and not force:
            print("exists, skip:", p.name)
            continue
        p.write_text(skeleton(m, BODY_PLACEHOLDER, "\n<script>\n  // calculator wiring (initCalc(...)) goes here; leave the script empty if the module has no calculator\n</script>\n"), encoding="utf-8")
        print("wrote", p.name)


# ----------------------------------------------------------------- inject
def cmd_inject(args):
    """inject NN BODY_FILE [--script JS_FILE] [--desc "text"]  → writes docs/learn/<module>.html"""
    n = args[0]; body_path = Path(args[1])
    m = BY_NUM[n]
    script = "\n"
    desc = None
    if "--script" in args:
        js = Path(args[args.index("--script") + 1]).read_text(encoding="utf-8").strip()
        if js and not js.lstrip().startswith("<script"):
            js = "<script>\n" + js + "\n</script>"
        script = "\n" + js + "\n"
    if "--desc" in args:
        desc = args[args.index("--desc") + 1]
    else:
        existing = DOCS / m["file"]
        if existing.exists():
            r = split_regions(existing.read_text(encoding="utf-8"))
            if r and r[2] and r[2] != "DESCRIPTION_PLACEHOLDER":
                desc = r[2]
    body = body_path.read_text(encoding="utf-8")
    body = "\n" + body.strip("\n") + "\n  "
    (DOCS / m["file"]).write_text(skeleton(m, body, script, desc), encoding="utf-8")
    print("injected", m["file"], len(body.encode()), "bytes body")


# ------------------------------------------------------------------ index
def cmd_index(_):
    p = DOCS / "index.html"
    text = p.read_text(encoding="utf-8")
    a, b = text.find("<!-- MAP:START -->"), text.find("<!-- MAP:END -->")
    if a < 0 or b < 0:
        sys.exit("index.html lacks MAP markers")
    out = []
    for key in PART_ORDER:
        part = PARTS[key]
        out.append(f'  <div class="map-part">{bi(esc(part["en"]), esc(part["zh"]))}</div>')
        out.append('  <div class="course-map">')
        for m in [x for x in MODS if x["part"] == key]:
            out.append(f'''    <a class="module-card" href="{m["file"]}">
      <span class="module-card-num">{m["num"]}</span>
      <div class="module-card-title">{bi(esc(m["en"]), esc(m["zh"]))}</div>
      <div class="module-card-meta"><span class="module-card-time lang-en">~{m["min"]} min</span><span class="module-card-time lang-zh" style="display:none">約 {m["min"]} 分鐘</span></div>
    </a>''')
        out.append('  </div>')
    new = text[:a + len("<!-- MAP:START -->")] + "\n" + "\n".join(out) + "\n  " + text[b:]
    p.write_text(new, encoding="utf-8")
    print("index map rebuilt:", len(MODS), "cards")


# ----------------------------------------------------------------- review
QUIZ_RE = re.compile(r'<div class="quiz-block"([^>]*?)data-quiz=\'(.*?)\'\s*>', re.S)


def cmd_review(_):
    bank = []
    for m in MODS:
        p = DOCS / m["file"]
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for k, mm in enumerate(QUIZ_RE.finditer(text)):
            attrs, raw = mm.group(1), mm.group(2)
            qid_m = re.search(r'data-quiz-id="([^"]+)"', attrs)
            qid = qid_m.group(1) if qid_m else f'{m["num"]}-q{k}'
            try:
                data = json.loads(html.unescape(raw))
            except Exception as e:
                print("bad quiz JSON in", p.name, e)
                continue
            for qi, item in enumerate(data):
                if item.get("from"):
                    continue  # interleaved review questions already live in their home module
                bank.append({"id": f"{qid}#{qi}", "module": m["num"], "q": item["q"], "opts": item["opts"], "a": item["a"], "exp": item.get("exp", {"en": "", "zh": ""})})
    (DOCS / "review-bank.json").write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("review bank:", len(bank), "questions")


# --------------------------------------------------------------------- qc
FORBIDDEN = [
    (r"本站", "personalised: 本站"), (r"我們的", "personalised: 我們的"), (r"(?<![a-zA-Z])我的", "personalised: 我的"),
    (r"QC-\d", "internal code QC-"), (r"§\s?\d", "internal section §"), (r"\bsonnet\b|\bopus\b|\bagent\b|\bskill\b|\bcritic\b", "internal jargon"),
    (r"rule_ledger|dd-meta|id-meta|stock-analyst|industry-analyst|update_dd_index", "internal file/tool name"),
    (r"TODO|TBD|PLACEHOLDER|lorem ipsum", "placeholder text"), (r"DESCRIPTION_PLACEHOLDER", "meta description not filled"),
    (r"本課程作者|筆者|本人", "personalised voice"),
]
CJK_PUNCT = re.compile(r"[一-鿿][,\.:;!\?](?![0-9])")
LANG_SPAN = re.compile(r'class="lang-(en|zh)')
REQUIRED = [
    ("module-goals", 1), ("war-story", 1), ("worked-example", 1), ("predict-block", 1),
    ("think-first", 2), ("pitfall", 1), ("checklist", 1), ("quiz-block", 1),
]
SIZE_MIN, SIZE_MAX = 60_000, 170_000


def strip_site_nav(text):
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import site_nav  # type: ignore
        for pat in site_nav.STRIP_PATTERNS:
            text = pat.sub("", text)
    except Exception:
        pass
    return text


def qc_file(p: Path):
    errs, warns = [], []
    text = p.read_text(encoding="utf-8")
    m = next((x for x in MODS if x["file"] == p.name), None)
    if m:
        regions = split_regions(text)
        if not regions:
            return [f"{p.name}: BODY/SCRIPT markers missing or out of order"], []
        body, script, desc = regions
        expect = strip_site_nav(skeleton(m, body, script, desc))
        got = strip_site_nav(text)
        if expect.strip() != got.strip():
            errs.append(f"{p.name}: generated skeleton (nav/header/pager/footer) was modified — regenerate with `course.py scaffold --force {m['num']}` and re-insert body")
        if not desc or desc == "DESCRIPTION_PLACEHOLDER":
            errs.append(f"{p.name}: meta description not written")
        # required blocks
        for cls, n in REQUIRED:
            c = len(re.findall(rf'class="{cls}\b', body))
            if c < n:
                errs.append(f"{p.name}: needs ≥{n} .{cls} block(s), found {c}")
        # quiz count
        total_q = 0
        for mm in QUIZ_RE.finditer(body):
            if "'" in mm.group(2):
                errs.append(f"{p.name}: raw single quote inside data-quiz attribute — browser truncates the attribute; use &#39;")
            try:
                data = json.loads(html.unescape(mm.group(2)))
            except Exception as e:
                errs.append(f"{p.name}: quiz JSON invalid: {e}")
                continue
            for item in data:
                if not (isinstance(item.get("a"), int) and 0 <= item["a"] < len(item.get("opts", []))):
                    errs.append(f"{p.name}: quiz answer index out of range")
                for k in ("q", "exp"):
                    if not (isinstance(item.get(k), dict) and item[k].get("en") and item[k].get("zh")):
                        errs.append(f"{p.name}: quiz item missing bilingual {k}")
                for o in item.get("opts", []):
                    if not (isinstance(o, dict) and o.get("en") and o.get("zh")):
                        errs.append(f"{p.name}: quiz option missing bilingual text")
                for sub in ("q", "exp"):
                    if isinstance(item.get(sub), dict) and "from" in item[sub]:
                        errs.append(f"{p.name}: quiz 'from' tag nested inside '{sub}' — must be a top-level key of the question item")
                if any(isinstance(o, dict) and "from" in o for o in item.get("opts", [])):
                    errs.append(f"{p.name}: quiz 'from' tag nested inside opts — must be top-level")
                if item.get("from") and (not re.fullmatch(r"\d\d", str(item["from"])) or item["from"] >= m["num"]):
                    errs.append(f"{p.name}: interleaved question 'from' must be an EARLIER module number, got {item.get('from')}")
            total_q += len(data)
        for tag in ("p", "span", "div", "li", "ul", "ol", "details", "summary", "table", "tr", "td", "th", "h2", "h3", "section", "blockquote", "strong", "em"):
            n_open = len(re.findall(rf"<{tag}(?=[\s>])", body))
            n_close = len(re.findall(rf"</{tag}\s*>", body))
            if n_open != n_close:
                errs.append(f"{p.name}: unbalanced <{tag}> tags in body ({n_open} open / {n_close} close)")
        for pat in (r"&lt;/?span", r"&lt;/?p\b", r"&lt;/?li\b"):
            n = len(re.findall(pat, body))
            if n:
                errs.append(f"{p.name}: {n}× HTML-escaped tag text ({pat}) in body — likely a broken tag")
        if total_q < 8:
            errs.append(f"{p.name}: only {total_q} quiz questions (need ≥8)")
        for mm in re.finditer(r"data-predict='(.*?)'\s*>", body, re.S):
            if "'" in mm.group(1):
                errs.append(f"{p.name}: raw single quote inside data-predict attribute — use &#39;")
            try:
                d = json.loads(html.unescape(mm.group(1)))
                assert d["q"]["en"] and d["q"]["zh"] and d["reveal"]["en"] and d["reveal"]["zh"] and len(d["opts"]) >= 2
            except Exception as e:
                errs.append(f"{p.name}: predict JSON invalid: {e}")
        # size
        sz = len(text.encode("utf-8"))
        if sz < SIZE_MIN:
            errs.append(f"{p.name}: {sz//1000}KB < {SIZE_MIN//1000}KB floor — too thin")
        elif sz > SIZE_MAX:
            warns.append(f"{p.name}: {sz//1000}KB > {SIZE_MAX//1000}KB — consider trimming")
    # lang parity (whole file)
    en, zh = 0, 0
    for mm in LANG_SPAN.finditer(text):
        if mm.group(1) == "en": en += 1
        else: zh += 1
    if en and abs(en - zh) > max(4, 0.03 * en):
        errs.append(f"{p.name}: lang-en/lang-zh count mismatch {en} vs {zh} — some text lacks its translation")
    # CJK punctuation
    bad = CJK_PUNCT.findall(text)
    if bad:
        errs.append(f"{p.name}: {len(bad)} CJK-followed-by-halfwidth punctuation hits e.g. {bad[:5]}")
    # forbidden
    for pat, why in FORBIDDEN:
        hits = re.findall(pat, text)
        if hits:
            errs.append(f"{p.name}: {why} ×{len(hits)}")
    # links
    for href in re.findall(r'(?:href|src)="([^"#]+)(?:#[^"]*)?"', text):
        if href.startswith(("http://", "https://", "mailto:", "data:", "javascript:")) or href == "#":
            continue
        target = (ROOT / "docs" / href.lstrip("/")) if href.startswith("/") else (p.parent / href)
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errs.append(f"{p.name}: dead link {href}")
    # unbalanced key-term tips: .key-term must contain .key-term-tip
    kt = len(re.findall(r'class="key-term"', text)); tip = len(re.findall(r'class="key-term-tip"', text))
    if kt != tip:
        warns.append(f"{p.name}: key-term ({kt}) vs key-term-tip ({tip}) mismatch")
    return errs, warns


def cmd_qc(args):
    files = [Path(a) for a in args if a.endswith(".html")] or sorted(DOCS.glob("*.html"))
    errs, warns = [], []
    for f in files:
        e, w = qc_file(f)
        errs += e; warns += w
    for w in warns: print("WARN", w)
    for e in errs: print("FAIL", e)
    print(f"qc: {len(files)} files, {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "qc"
    {"scaffold": cmd_scaffold, "inject": cmd_inject, "index": cmd_index, "review": cmd_review, "qc": cmd_qc}[cmd](sys.argv[2:])
