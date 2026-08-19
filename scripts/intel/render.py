#!/usr/bin/env python3
"""scripts/intel/render.py — Phase 1 static renderer for /intel/.

對應 notes/site-internal/intel/DESIGN.md §11（卡片 schema）／§12（頁面，版型決議
A，2026-08-19）／§14（防護）。本檔零判斷、零 LLM：讀 `docs/intel/data/{date}.json`
（haiku/sonnet 那一步的輸出），機械渲染成靜態 HTML。找不到當日 JSON 時退回讀
`docs/intel/pending/{date}.json`（只有原始抓取，尚未分類摘要）並在頁面上標示
banner，讓頁面永遠不 404、不悄悄失真。

CLI:
    python3 scripts/intel/render.py --date 2026-08-19

輸出：
    docs/intel/index.html          今日（= --date 那天）
    docs/intel/{date}.html         同一天的封存副本（含「回今日」連結）
    docs/intel/archive.html        封存列表（掃描 docs/intel/*.html 已存在的日期頁）
    docs/intel/status.html         來源健康 + 當日用量

安全：
    - 除 brief_zh 外，JSON 裡所有字串一律 html.escape。
    - brief_zh 用允許清單白名單 sanitizer（僅 <a href>（http/https/相對路徑）、
      <b>、<span class="n"> / <span class="src">），其餘標籤整個丟棄（純文字保留
      並照樣跳脫），達成「來源文字是資料不是指令」（DESIGN §14）。
    - 站外連結一律加 rel="noopener nofollow"。

決定性：輸出不嵌入渲染當下的 wall-clock 時間戳（唯一用到「現在」的地方是
status.html 頁尾「stale 警告」的判斷本身，這是刻意的活判斷，不是渲染噪音——
同一份輸入在 30 小時視窗內重跑會得到 byte-identical 輸出）。
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
INTEL_SCRIPTS_DIR = ROOT / "scripts" / "intel"
TEMPLATE_CSS = INTEL_SCRIPTS_DIR / "templates" / "intel.css"
SOURCES_YML = INTEL_SCRIPTS_DIR / "sources.yml"
DOCS_INTEL = ROOT / "docs" / "intel"
DATA_DIR = DOCS_INTEL / "data"
PENDING_DIR = DOCS_INTEL / "pending"
HEALTH_FILE = DATA_DIR / "sources_health.json"

TAIPEI_OFFSET = timedelta(hours=8)
STALE_HOURS = 30

WEEKDAY_ZH = ["一", "二", "三", "四", "五", "六", "日"]

GAUGE_ORDER = [
    "rates", "credit", "liquidity", "fx", "commodities", "vol", "breadth",
    "positioning", "econ", "cb", "geo", "regime", "asia",
]
GAUGE_LABEL_ZH = {
    "rates": "利率", "credit": "信用", "liquidity": "流動性", "fx": "匯率",
    "commodities": "商品", "vol": "波動", "breadth": "股市內部",
    "positioning": "部位", "econ": "經濟數據", "cb": "央行財政",
    "geo": "地緣", "regime": "regime", "asia": "亞洲",
}

LEVEL_ORDER = ["market", "industry", "company"]
LEVEL_LABEL_ZH = {"market": "市場", "industry": "產業", "company": "個股"}


# ------------------------------------------------------------------ json io

def load_json(path: Path):
    import json
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_sources_yml():
    """id -> {name, tier, category} from scripts/intel/sources.yml (best-effort)."""
    out = {}
    if not SOURCES_YML.exists():
        return out
    try:
        entries = yaml.safe_load(SOURCES_YML.read_text(encoding="utf-8")) or []
    except Exception:
        return out
    for e in entries:
        if isinstance(e, dict) and e.get("id"):
            out[e["id"]] = {
                "name": e.get("name", e["id"]),
                "tier": e.get("tier", ""),
                "category": e.get("category", ""),
            }
    return out


# --------------------------------------------------------------- html utils

def esc(v) -> str:
    """Hard escape — used for every JSON string field except brief_zh."""
    if v is None:
        return ""
    return html.escape(str(v), quote=True)


_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")


def _safe_href(href: str) -> bool:
    href = (href or "").strip()
    if not href:
        return False
    if href.startswith("#"):
        return True
    if href.startswith("//"):
        return False  # protocol-relative — ambiguous scheme, reject
    m = _SCHEME_RE.match(href)
    if m:
        return m.group(0)[:-1].lower() in ("http", "https")
    return True  # relative / root-relative path


class _BriefSanitizer(HTMLParser):
    """Allow-list sanitizer for brief_zh paragraphs.

    Allowed: <a href="http(s)/relative">, <b>, <span class="n">,
    <span class="src">. Everything else is dropped as a tag but its text
    content is kept (escaped) — matches DESIGN §14 "來源文字是資料不是指令".
    """

    ALLOWED_SPAN_CLASSES = {"n", "src"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self._stack = []  # tag names we actually opened, for matching close

    def handle_starttag(self, tag, attrs):
        self._open(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._open(tag, attrs)
        # self-closed tags never allowed in our list -> nothing to close

    def _open(self, tag, attrs):
        a = dict(attrs)
        if tag == "a":
            href = a.get("href", "")
            if _safe_href(href):
                self.out.append(f'<a href="{esc(href)}" rel="noopener nofollow">')
                self._stack.append("a")
            else:
                self._stack.append(None)
        elif tag == "b":
            self.out.append("<b>")
            self._stack.append("b")
        elif tag == "span":
            cls = (a.get("class") or "").strip()
            if cls in self.ALLOWED_SPAN_CLASSES:
                self.out.append(f'<span class="{cls}">')
                self._stack.append("span")
            else:
                self._stack.append(None)
        else:
            self._stack.append(None)

    def handle_endtag(self, tag):
        if not self._stack:
            return
        opened = self._stack.pop()
        if opened:
            self.out.append(f"</{opened}>")

    def handle_data(self, data):
        self.out.append(html.escape(data))

    def result(self) -> str:
        return "".join(self.out)


def sanitize_brief(text: str) -> str:
    p = _BriefSanitizer()
    p.feed(text or "")
    p.close()
    return p.result()


# ----------------------------------------------------------------- time fmt

def parse_iso(s):
    if not s:
        return None
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_taipei(dt: datetime) -> datetime:
    return dt + TAIPEI_OFFSET


def fmt_hm(iso_s) -> str:
    dt = parse_iso(iso_s)
    if dt is None:
        return "--:--"
    tp = to_taipei(dt)
    return f"{tp.hour:02d}:{tp.minute:02d}"


def fmt_full(iso_s) -> str:
    dt = parse_iso(iso_s)
    if dt is None:
        return "—"
    tp = to_taipei(dt)
    return f"{tp.year:04d}-{tp.month:02d}-{tp.day:02d} {tp.hour:02d}:{tp.minute:02d}"


def weekday_zh(d: "datetime.date") -> str:
    return WEEKDAY_ZH[d.weekday()]


def sort_epoch(card) -> float:
    dt = parse_iso(card.get("published") or card.get("published_at") or card.get("fetched_at"))
    return dt.timestamp() if dt else 0.0


# ------------------------------------------------------------------ gauges

def render_gauges(gauges: list) -> str:
    if not gauges:
        return '<div class="gauges"><div class="row empty">今日儀表資料尚未產出。</div></div>'
    rows = []
    for g in gauges:
        status = (g.get("status") or "green").lower()
        cls = "crit" if status == "red" else "warn" if status == "yellow" else ""
        cls_attr = f"g {cls}" if cls else "g"
        label = esc(g.get("label") or g.get("category") or "")
        value = esc(g.get("value") or "")
        delta = esc(g.get("delta") or "")
        rows.append(
            f'<div class="{cls_attr}"><span class="dot"></span>'
            f'<span class="name">{label}</span>'
            f'<span class="v mono">{value}</span>'
            f'<span class="d">{delta}</span></div>'
        )
    return '<div class="gauges" aria-label="市場儀表">\n' + "\n".join(rows) + "\n</div>"


# ------------------------------------------------------------------- flags

FLAG_LABEL = {"near": "⚠ 接近中", "confirmed": "🔴 已確認", "thesis": "🔴 論點連結"}


def render_flags(flags: list) -> str:
    if not flags:
        return ""
    out = []
    for fl in flags:
        level = (fl.get("level") or "near").lower()
        hard = " hard" if level in ("confirmed", "thesis") else ""
        label = FLAG_LABEL.get(level, "⚠ 接近中")
        text = esc(fl.get("text_zh") or "")
        link = fl.get("link") or ""
        body = f'<span class="k">{esc(label)}</span>{text}'
        if link and _safe_href(link):
            body += f' <a href="{esc(link)}" rel="noopener nofollow">詳情</a>'
        out.append(f'<div class="flag{hard}">{body}</div>')
    return "\n".join(out)


# -------------------------------------------------------------------- brief

def render_brief(brief_zh: list) -> str:
    if not brief_zh:
        return '<p class="note">今日市場早報尚未產出。</p>'
    paras = [f"<p>{sanitize_brief(p)}</p>" for p in brief_zh]
    return '<div class="brief">\n' + "\n".join(paras) + "\n</div>"


# --------------------------------------------------------------- card rows

def is_rumor(card) -> bool:
    return card.get("kind") == "rumor" or card.get("source_tier") in ("T3", "T4")


def card_source_label(card, sources_meta) -> str:
    tier = card.get("source_tier") or ""
    name = card.get("source_name") or card.get("source") or ""
    if not name:
        meta = sources_meta.get(card.get("source_id") or "")
        name = meta["name"] if meta else (card.get("source_id") or "")
    corrob = card.get("corroboration") or 1
    if card.get("kind") == "data":
        return f"數據 · {esc(name)}"
    if is_rumor(card):
        return f"{esc(tier)} · 傳聞"
    if corrob and corrob >= 2:
        return f"{esc(tier)} · {corrob} 源"
    return f"{esc(tier)} · {esc(name)}" if name else esc(tier)


def card_tags_html(card) -> str:
    tags = card.get("tags") or {}
    out = []
    propagated = tags.get("propagated_to") or []
    tickers = tags.get("tickers") or []
    if propagated:
        out.append(f'<span class="tag p">→ {esc(" · ".join(propagated))}</span>')
    elif tickers and card.get("level") != "company":
        out.append(f'<span class="tag p">→ {esc(" · ".join(tickers))}</span>')
    if is_rumor(card):
        out.append('<span class="tag r">傳聞</span>')
    return "".join(out)


def card_lvl_label(card) -> str:
    tags = card.get("tags") or {}
    tickers = tags.get("tickers") or []
    themes = tags.get("themes") or []
    if tickers:
        return " · ".join(tickers[:3])
    if themes:
        return themes[0]
    return card.get("level") or ""


_DATA_KEYS = (("value", "現值"), ("pctile", "分位"), ("threshold", "門檻"), ("change_20d", "20 日變化"),
              ("prev", "前值"), ("status", "狀態"), ("as_of", "截至"), ("rule", "規則"), ("severity", "等級"))


def render_data_line(data) -> str:
    """數字卡的 data 欄：把 value／分位／門檻等以「鍵：值」列出（純文字、全部 escape）。"""
    if not isinstance(data, dict):
        return ""
    parts = []
    for key, label in _DATA_KEYS:
        v = data.get(key)
        if v is None or v == "":
            continue
        if isinstance(v, float):
            v = f"{v:g}"
        parts.append(f"{label} {esc(str(v))}")
    if data.get("doc"):
        parts.append(f'<a href="/{esc(str(data["doc"]).replace("docs/", "", 1))}">相關報告</a>')
    return (" <span class=\"mono\">" + " · ".join(parts) + "</span>") if parts else ""


def render_row(card, sources_meta, lvl_text=None) -> str:
    t = fmt_hm(card.get("published") or card.get("published_at") or card.get("fetched_at"))
    imp = int(card.get("importance") or 1)
    imp = 1 if imp < 1 else 3 if imp > 3 else imp
    cat = esc(card.get("category") or "")
    src = card_source_label(card, sources_meta)
    title = esc(card.get("summary_zh") or card.get("title") or "")
    why = esc(card.get("why_zh") or "")
    url = card.get("url") or ""
    src_name = esc(card.get("source_name") or card.get("source") or "")
    tags_html = card_tags_html(card)
    lvl = esc(lvl_text if lvl_text is not None else card_lvl_label(card))
    link_html = (
        f' <a href="{esc(url)}" rel="noopener nofollow">{src_name or "來源"}</a>'
        if url and _safe_href(url) else ""
    )
    data_html = render_data_line(card.get("data"))
    if why:
        why_html = f"<b>為什麼重要：</b>{why}{data_html}{link_html}"
    else:
        why_html = (data_html + link_html).strip()
    return (
        '<div class="row">'
        f'<span class="t mono">{t}</span>'
        f'<span class="imp i{imp}"></span>'
        f'<span class="cat">{cat}</span>'
        f'<span class="src">{src}</span>'
        f'<div class="hd"><details><summary>{title}{tags_html}</summary>'
        f'<div class="body">{why_html}</div></details></div>'
        f'<span class="lvl">{lvl}</span>'
        "</div>"
    )


LIST_HEAD = (
    '<div class="row head"><span>時間</span><span></span><span>類別</span>'
    "<span>來源</span><span>標題</span><span></span></div>"
)


def render_card_list(cards: list, sources_meta, empty_text: str) -> str:
    if not cards:
        return f'<div class="list">{LIST_HEAD}<div class="row empty">{esc(empty_text)}</div></div>'
    ordered = sorted(cards, key=lambda c: (-int(c.get("importance") or 1), -sort_epoch(c)))
    rows = "\n".join(render_row(c, sources_meta) for c in ordered)
    return f'<div class="list">{LIST_HEAD}\n{rows}\n</div>'


def render_dense_feed(cards: list, sources_meta) -> str:
    by_level = {lv: [] for lv in LEVEL_ORDER}
    for c in cards:
        by_level.setdefault(c.get("level") or "market", []).append(c)
    parts = [LIST_HEAD]
    any_rows = False
    for lv in LEVEL_ORDER + [k for k in by_level if k not in LEVEL_ORDER]:
        items = by_level.get(lv) or []
        if not items:
            continue
        any_rows = True
        ordered = sorted(items, key=lambda c: (-int(c.get("importance") or 1), -sort_epoch(c)))
        parts.append(f'<div class="row grp">{esc(lv.capitalize())} · {esc(LEVEL_LABEL_ZH.get(lv, lv))}</div>')
        parts.extend(render_row(c, sources_meta, lvl_text=lv) for c in ordered)
    if not any_rows:
        parts.append('<div class="row empty">今日尚無卡片。</div>')
    return '<div class="list">' + "\n".join(parts) + "</div>"


# ----------------------------------------------------------------- calendar

def render_calendar(calendar: list, base_date) -> str:
    """7 upcoming days, starting tomorrow (base_date+1 .. base_date+7) — "今天"
    itself is already covered by the market brief / gauges above."""
    by_date = {}
    for e in calendar or []:
        by_date.setdefault(e.get("date"), []).append(e)
    days = []
    for i in range(1, 8):
        d = base_date + timedelta(days=i)
        ds = d.isoformat()
        label = f"{weekday_zh(d)} {d.month:02d}-{d.day:02d}"
        events = by_date.get(ds) or []
        if events:
            ev_html = "".join(
                f'<div class="e{" hi" if e.get("hi") else ""}">{esc(e.get("text") or "")}</div>'
                for e in events
            )
        else:
            ev_html = '<div class="e">—</div>'
        days.append(f'<div class="d"><div class="w">{esc(label)}</div>{ev_html}</div>')
    return '<div class="cal">\n' + "\n".join(days) + "\n</div>"


# ------------------------------------------------------------------- status

def render_status_line(status: dict) -> str:
    if not status:
        return ""
    sources_ok = status.get("sources_ok")
    sources_fail = status.get("sources_fail")
    fetched = status.get("fetched")
    kept = status.get("kept")
    classified = status.get("classified")
    summarized = status.get("summarized")
    tokens = status.get("tokens") or {}
    next_run = status.get("next_run")
    parts = []
    if sources_ok is not None:
        total = (sources_ok or 0) + (sources_fail or 0)
        parts.append(f"來源 {sources_ok}／{total} 正常")
    if fetched is not None:
        parts.append(
            f"抓到 {fetched} · 留 {kept if kept is not None else '—'} · "
            f"分類 {classified if classified is not None else '—'} · "
            f"摘要 {summarized if summarized is not None else '—'}"
        )
    if tokens:
        tok_str = " · ".join(f"{esc(k)} {v:,}" for k, v in tokens.items())
        total_tok = sum(v for v in tokens.values() if isinstance(v, (int, float)))
        parts.append(f"今日 token ≈ {total_tok:,}（{tok_str}）")
    if next_run:
        parts.append(f"下次：{esc(next_run)}")
    spans = "".join(f"<span>{p}</span>" for p in parts)
    return f'<div class="status mono">{spans}</div>'


# ---------------------------------------------------------------- page shell

def head(title: str, description: str, indexable: bool) -> str:
    robots = "index,follow" if indexable else "noindex,nofollow"
    css = TEMPLATE_CSS.read_text(encoding="utf-8")
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="{robots}">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:site_name" content="InvestMQuest Research">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>"""


FOOT = (
    '<footer class="imq-foot">'
    "<div>© 2026 InvestMQuest Research</div>"
    '<div><a href="/disclosures.html">方法論與揭露</a> · '
    "本頁為機械聚合＋LLM 摘要，卡片內容為第三方來源之摘要，正確性以原文為準，"
    "不構成投資建議</div>"
    "</footer>"
)

TOGGLE_SCRIPT = (
    "<script>(function(){"
    "var b=document.body,btns=document.querySelectorAll('.seg button');"
    "btns.forEach(function(x){x.addEventListener('click',function(){"
    "b.setAttribute('data-mode',x.getAttribute('data-set'));"
    "btns.forEach(function(y){y.setAttribute('aria-pressed',String(y===x))});"
    "})});"
    "})();</script>"
)


def banner_html(text: str, stale: bool = False) -> str:
    cls = "banner stale" if stale else "banner"
    return f'<div class="{cls}">{text}</div>'


def build_day_body(date_str: str, payload: dict, mode_note: str, archive_link: str) -> str:
    gauges = payload.get("gauges") or []
    flags = payload.get("flags") or []
    brief_zh = payload.get("brief_zh") or []
    cards = payload.get("cards") or []
    calendar = payload.get("calendar") or []
    status = payload.get("status") or {}
    sources_meta = payload.get("_sources_meta") or {}
    generated_at = payload.get("generated_at")

    industry_cards = [c for c in cards if c.get("level") == "industry" and not is_rumor(c)]
    company_cards = [c for c in cards if c.get("level") == "company" and not is_rumor(c)]
    rumor_cards = [c for c in cards if is_rumor(c)]

    base_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    parts = []
    parts.append('<div class="wrap">')
    parts.append('<div class="top">')
    when = fmt_hm(generated_at) if generated_at else "--:--"
    parts.append(f'<h1>Intel 監視器<small>{esc(date_str)} · {esc(when)} 更新</small></h1>')
    parts.append(
        '<div class="seg" role="group" aria-label="版型">'
        '<button type="button" data-set="brief" aria-pressed="true">A · 早報＋列表</button>'
        '<button type="button" data-set="list" aria-pressed="false">B · 純列表</button>'
        "</div></div>"
    )
    if mode_note:
        parts.append(mode_note)
    if archive_link:
        parts.append(archive_link)

    parts.append(render_gauges(gauges))

    parts.append('<section class="only-brief">')
    flags_html = render_flags(flags)
    if flags_html:
        parts.append('<h2>Alerts <span class="zh">轉折提醒</span></h2>')
        parts.append(flags_html)
    parts.append('<h2>Market <span class="zh">市場早報</span></h2>')
    parts.append(render_brief(brief_zh))
    parts.append('<h2>Industry <span class="zh">產業</span></h2>')
    parts.append(render_card_list(industry_cards, sources_meta, "Phase 1 僅涵蓋市場層，產業層尚未上線。"))
    parts.append('<h2>Company <span class="zh">個股</span></h2>')
    parts.append(render_card_list(company_cards, sources_meta, "Phase 1 僅涵蓋市場層，個股層尚未上線。"))
    parts.append('<h2>Rumor <span class="zh">傳聞</span></h2>')
    parts.append(render_card_list(rumor_cards, sources_meta, "今日無 T3／T4 傳聞卡片。"))
    parts.append("</section>")

    parts.append('<section class="only-list">')
    parts.append('<h2>Feed <span class="zh">全部一行一則，依層級分組</span></h2>')
    parts.append(render_dense_feed(cards, sources_meta))
    parts.append("</section>")

    parts.append('<h2>Next 7 days <span class="zh">接下來 7 天</span></h2>')
    parts.append(render_calendar(calendar, base_date))

    parts.append('<h2>Status <span class="zh">狀態</span></h2>')
    status_html = render_status_line(status)
    parts.append(status_html or '<p class="note">今日狀態資料尚未產出。</p>')
    parts.append(
        '<p class="note">完整來源健康表見 '
        '<a href="/intel/status.html">/intel/status.html</a>。</p>'
    )

    parts.append("</div>")  # .wrap
    parts.append(FOOT)
    parts.append(TOGGLE_SCRIPT)
    return "\n".join(parts)


# ------------------------------------------------------------- data loading

def resolve_day_payload(date_str: str, sources_meta: dict):
    """Return (payload, banner_html, is_stale). payload always has all keys."""
    real_path = DATA_DIR / f"{date_str}.json"
    pending_path = PENDING_DIR / f"{date_str}.json"

    if real_path.exists():
        data = load_json(real_path)
        data["_sources_meta"] = sources_meta
        generated_at = data.get("generated_at")
        stale = False
        banner = ""
        dt = parse_iso(generated_at)
        if dt is not None:
            age_h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0
            if age_h > STALE_HOURS:
                stale = True
                banner = banner_html(
                    f"<b>資料已逾 {STALE_HOURS} 小時未更新。</b>"
                    f"最後產出時間：{esc(fmt_full(generated_at))}（台北時間）。",
                    stale=True,
                )
        return data, banner, stale

    if pending_path.exists():
        pending = load_json(pending_path)
        meta = pending.get("meta") or {}
        cards_raw = pending.get("cards") or []
        cards = []
        for c in cards_raw:
            cc = dict(c)
            cc.setdefault("summary_zh", cc.get("title") or cc.get("summary_raw") or "")
            cc.setdefault("why_zh", "")
            cc.setdefault("importance", 1)
            cards.append(cc)
        counts = meta.get("counts") or {}
        data = {
            "schema": "intel-daily-v1",
            "date": date_str,
            "generated_at": meta.get("generated_at"),
            "gauges": [],
            "brief_zh": [],
            "flags": [],
            "cards": cards,
            "calendar": [],
            "status": {
                "sources_ok": meta.get("sources_ok"),
                "sources_fail": meta.get("sources_fail"),
                "fetched": counts.get("fetched"),
                "kept": counts.get("kept"),
                "classified": None,
                "summarized": None,
                "tokens": {},
                "next_run": "—",
            },
            "_sources_meta": sources_meta,
        }
        banner = banner_html(
            "<b>今日尚未整理（只有原始抓取）。</b>"
            "haiku／sonnet 分類摘要步驟尚未跑完，以下卡片為未經摘要的原始標題，"
            "無「為什麼重要」與儀表列。",
        )
        return data, banner, False

    # neither file exists — render an empty, honest shell.
    data = {
        "schema": "intel-daily-v1", "date": date_str, "generated_at": None,
        "gauges": [], "brief_zh": [], "flags": [], "cards": [], "calendar": [],
        "status": {}, "_sources_meta": sources_meta,
    }
    banner = banner_html(f"<b>{esc(date_str)} 尚無任何資料（抓取步驟尚未執行）。</b>")
    return data, banner, False


# ------------------------------------------------------------------ archive

DATE_HTML_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.html$")


def render_archive(current_date: str) -> str:
    dates = set()
    for p in DOCS_INTEL.glob("*.html"):
        m = DATE_HTML_RE.match(p.name)
        if m:
            dates.add(m.group(1))
    dates.add(current_date)
    ordered = sorted(dates, reverse=True)
    items = []
    for d in ordered:
        try:
            wd = weekday_zh(datetime.strptime(d, "%Y-%m-%d").date())
        except ValueError:
            wd = ""
        items.append(f'<li><a href="/intel/{esc(d)}.html">{esc(d)}（{wd}）</a></li>')
    body = [
        '<div class="wrap">',
        '<div class="top"><h1>Intel 封存<small>依日期排列</small></h1></div>',
        '<p class="note"><a class="back" href="/intel/">回今日</a></p>',
        f'<ul class="arclist">{"".join(items)}</ul>' if items else '<p class="note">尚無封存頁面。</p>',
        "</div>",
        FOOT,
    ]
    return "\n".join(body)


# ------------------------------------------------------------------- status

def render_status_page(date_str: str, payload: dict, sources_meta: dict) -> str:
    status = payload.get("status") or {}
    generated_at = payload.get("generated_at")
    health = {"sources": []}
    if HEALTH_FILE.exists():
        health = load_json(HEALTH_FILE)
    rows = []
    for s in health.get("sources") or []:
        sid = s.get("source_id") or ""
        meta = sources_meta.get(sid) or {}
        name = meta.get("name", sid)
        tier = meta.get("tier", "")
        ok = bool(s.get("ok"))
        ok_html = '<td class="ok">OK</td>' if ok else '<td class="fail">FAIL</td>'
        latency = s.get("latency_ms")
        latency_s = f"{latency} ms" if latency is not None else "—"
        item_count = s.get("item_count")
        item_s = item_count if item_count is not None else "—"
        err = s.get("error") or ""
        err_s = (err[:140] + "…") if len(err) > 140 else err
        rows.append(
            "<tr>"
            f"<td>{esc(sid)}</td><td>{esc(name)}</td><td>{esc(tier)}</td>"
            f"{ok_html}<td>{esc(latency_s)}</td><td>{esc(item_s)}</td>"
            f'<td class="err">{esc(err_s)}</td>'
            "</tr>"
        )
    table = (
        '<div class="twrap"><table class="stbl"><thead><tr>'
        "<th>source_id</th><th>名稱</th><th>tier</th><th>狀態</th>"
        "<th>延遲</th><th>抓到筆數</th><th>錯誤</th>"
        "</tr></thead><tbody>"
        + ("".join(rows) if rows else '<tr><td colspan="7">健康檢查資料尚未產出。</td></tr>')
        + "</tbody></table></div>"
    )

    tokens = status.get("tokens") or {}
    cards = [
        ("健康檢查時間（台北）", esc(fmt_full(health.get("generated_at")))),
        ("今日產出時間（台北）", esc(fmt_full(generated_at))),
        ("來源正常／失敗", f"{status.get('sources_ok', '—')} ／ {status.get('sources_fail', '—')}"),
        ("抓到 → 保留", f"{status.get('fetched', '—')} → {status.get('kept', '—')}"),
        ("分類 → 摘要", f"{status.get('classified', '—')} → {status.get('summarized', '—')}"),
        ("今日 token", " · ".join(f"{k} {v:,}" for k, v in tokens.items()) or "—"),
        ("下次排程", esc(status.get("next_run") or "—")),
    ]
    stat_html = "".join(
        f'<div class="c"><div class="k">{k}</div><div class="v mono">{v}</div></div>'
        for k, v in cards
    )

    body = [
        '<div class="wrap">',
        '<div class="top"><h1>Intel 狀態<small>來源健康 · 每日用量</small></h1></div>',
        f'<p class="note"><a class="back" href="/intel/">回今日</a> · '
        f'<a class="back" href="/intel/archive.html">封存</a></p>',
        f'<div class="stat-cards">{stat_html}</div>',
        "<h2>Sources <span class=\"zh\">來源健康</span></h2>",
        table,
        "</div>",
        FOOT,
    ]
    return "\n".join(body)


# ------------------------------------------------------------------- inject

def inject_nav(paths):
    """Best-effort: inject the canonical site header into exactly the files we
    just wrote, using scripts/site_nav.py's own process() function — never a
    full-site sweep, so nothing outside docs/intel/ is touched."""
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import site_nav  # noqa: E402
    except Exception as e:  # pragma: no cover - best effort only
        print(f"[render.py] nav injection skipped ({e})", file=sys.stderr)
        return
    for p in paths:
        try:
            site_nav.process(p)
        except Exception as e:  # pragma: no cover
            print(f"[render.py] nav injection failed for {p}: {e}", file=sys.stderr)


# ---------------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    args = ap.parse_args()
    date_str = args.date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"invalid --date: {date_str}", file=sys.stderr)
        sys.exit(1)

    DOCS_INTEL.mkdir(parents=True, exist_ok=True)
    sources_meta = load_sources_yml()

    payload, banner, stale = resolve_day_payload(date_str, sources_meta)

    index_body = build_day_body(date_str, payload, banner, "")
    index_html = (
        head(
            "全球情報監視器 — InvestMQuest Research",
            "全球金融市場情報監視器：儀表列、市場早報、產業／個股卡片、傳聞與接下來 7 天日曆，機械聚合＋LLM 摘要每日更新。",
            indexable=True,
        )
        + "\n<body data-mode=\"brief\">\n"
        + index_body
        + "\n</body>\n</html>\n"
    )
    index_path = DOCS_INTEL / "index.html"
    index_path.write_text(index_html, encoding="utf-8")

    archive_link = f'<p class="note"><a class="back" href="/intel/">回今日</a> · <a class="back" href="/intel/archive.html">封存</a></p>'
    day_body = build_day_body(date_str, payload, banner, archive_link)
    day_html = (
        head(
            f"{date_str} — Intel 監視器封存 — InvestMQuest Research",
            f"{date_str} 全球情報監視器封存頁。",
            indexable=False,
        )
        + "\n<body data-mode=\"brief\">\n"
        + day_body
        + "\n</body>\n</html>\n"
    )
    day_path = DOCS_INTEL / f"{date_str}.html"
    day_path.write_text(day_html, encoding="utf-8")

    archive_html = (
        head("Intel 封存 — InvestMQuest Research", "情報監視器歷史日期列表。", indexable=False)
        + "\n<body>\n"
        + render_archive(date_str)
        + "\n</body>\n</html>\n"
    )
    archive_path = DOCS_INTEL / "archive.html"
    archive_path.write_text(archive_html, encoding="utf-8")

    status_html = (
        head("Intel 狀態 — InvestMQuest Research", "情報監視器來源健康與每日用量。", indexable=False)
        + "\n<body>\n"
        + render_status_page(date_str, payload, sources_meta)
        + "\n</body>\n</html>\n"
    )
    status_path = DOCS_INTEL / "status.html"
    status_path.write_text(status_html, encoding="utf-8")

    inject_nav([index_path, day_path, archive_path, status_path])

    print(f"wrote {index_path}")
    print(f"wrote {day_path}")
    print(f"wrote {archive_path}")
    print(f"wrote {status_path}")


if __name__ == "__main__":
    main()
