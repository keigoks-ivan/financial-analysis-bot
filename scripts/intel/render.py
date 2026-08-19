#!/usr/bin/env python3
"""scripts/intel/render.py — 靜態渲染器 for /intel/（版型 A）。

對應 notes/site-internal/intel/DESIGN.md §11（卡片 schema）／§12（頁面，版型決議
A，2026-08-19）／§14（防護）。本檔零判斷、零 LLM：讀 `docs/intel/data/{date}.json`
（haiku/sonnet 那一步的輸出），機械渲染成靜態 HTML。找不到當日 JSON 時退回讀
`docs/intel/pending/{date}.json`（只有原始抓取，尚未分類摘要）並在頁面上標示
banner，讓頁面永遠不 404、不悄悄失真。

版面（2026-08-19 重製）：
    1. masthead        標題＋日期＋更新時間＋狀態 chips＋歷史／狀態連結
    2. 儀表列          13 格：label／大數字 value／metric·chg·分位 pill，左側狀態色條
    3. 轉折警示        表格：等級 pill｜主題｜指標｜現值｜門檻｜距離｜來源
    4. 市場早報        雙欄：早報段落 ＋ aside（今日焦點／7 日日曆／資料狀態）
    5. 市場／產業／個股 密集列表，依類別分組；其他標題（未摘要）；傳聞（T3/T4）
    6. footer          方法說明＋站內連結＋聲明

CLI:
    python3 scripts/intel/render.py --date 2026-08-19
    python3 scripts/intel/render.py --date 2026-08-19 --data <json> --out <dir>
        （--data／--out 為測試用：直接指定輸入 JSON 與輸出目錄，不動 docs/。）

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

相容性：所有新欄位（gauges.metric/pctile/chg、flags 的結構化欄位、calendar 的
time/impact/country/forecast/previous、cards 的 summarized/source_short）皆為
選填；缺席時退回舊行為，不得因此壞版或出現半截句子。

決定性：輸出不嵌入渲染當下的 wall-clock 時間戳（唯一用到「現在」的地方是
stale 警告的判斷本身，這是刻意的活判斷，不是渲染噪音）。
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

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
DASH = "—"

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
# 產業／個股層才會出現的類別（市場層 13 類沿用 GAUGE_LABEL_ZH）。
INDUSTRY_LABEL_ZH = {
    "semis": "半導體", "ai": "AI", "ev": "電動車", "battery": "電池",
    "robotics": "機器人", "logistics": "物流", "renewable-energy": "再生能源",
    "automation": "自動化", "software": "軟體", "cloud": "雲端",
    "biotech": "生技", "healthcare": "醫療", "defense": "國防",
    "materials": "材料", "chemical": "化學材料", "energy": "能源",
    "consumer": "消費", "retail": "零售", "financials": "金融",
    "industrials": "工業", "telecom": "電信", "property": "房地產",
    "crypto": "加密資產", "autos": "汽車", "aerospace": "航太",
    "shipping": "航運", "tourism": "觀光", "process-node": "先進製程",
    "gpu": "GPU", "llm": "大型語言模型", "other": "其他",
}


def cat_label(cat: str) -> str:
    cat = cat or ""
    return GAUGE_LABEL_ZH.get(cat) or INDUSTRY_LABEL_ZH.get(cat) or cat or "其他"


LEVEL_ORDER = ["market", "industry", "company"]
LEVEL_LABEL_ZH = {"market": "市場", "industry": "產業", "company": "個股"}

FLAG_ORDER = {"confirmed": 0, "near": 1, "thesis": 2}
FLAG_LABEL = {"confirmed": "已確認", "near": "接近中", "thesis": "論點"}


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


def fmt_hm(iso_s, dash: str = DASH) -> str:
    """台北時間 HH:MM；無時間戳一律回 dash（不再輸出 "--:--"）。"""
    dt = parse_iso(iso_s)
    if dt is None:
        return dash
    tp = to_taipei(dt)
    return f"{tp.hour:02d}:{tp.minute:02d}"


def fmt_full(iso_s) -> str:
    dt = parse_iso(iso_s)
    if dt is None:
        return DASH
    tp = to_taipei(dt)
    return f"{tp.year:04d}-{tp.month:02d}-{tp.day:02d} {tp.hour:02d}:{tp.minute:02d}"


def weekday_zh(d) -> str:
    return WEEKDAY_ZH[d.weekday()]


def card_time(card) -> str:
    return card.get("published") or card.get("published_at") or card.get("fetched_at")


def sort_epoch(card) -> float:
    dt = parse_iso(card_time(card))
    return dt.timestamp() if dt else 0.0


def card_sort_key(card):
    return (-int(card.get("importance") or 1), -int(card.get("corroboration") or 1),
            -sort_epoch(card))


def fmt_num(v) -> str:
    if v is None or v == "":
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


# ------------------------------------------------------------------ gauges

def _pct_pill(pctile) -> str:
    if pctile is None or pctile == "":
        return ""
    try:
        p = float(pctile)
    except (TypeError, ValueError):
        return ""
    cls = "pct hot" if p >= 90 else "pct cold" if p <= 10 else "pct"
    return f'<span class="{cls}" title="一年分位">分位 {esc(f"{p:g}")}</span>'


def _chg_span(chg) -> str:
    chg = (chg or "").strip()
    if not chg:
        return ""
    cls = "chg up" if chg.startswith("▲") else "chg dn" if chg.startswith("▼") else "chg"
    return f'<span class="{cls}">{esc(chg)}</span>'


def render_gauges(gauges: list) -> str:
    if not gauges:
        return '<div class="empty">今日儀表資料尚未產出。</div>'
    tiles = []
    for g in gauges:
        status = (g.get("status") or "green").lower()
        cls = "g crit" if status == "red" else "g warn" if status == "yellow" else "g"
        label = esc(g.get("label") or cat_label(g.get("category")))
        value = (g.get("value") or "").strip()
        metric = (g.get("metric") or "").strip()
        delta = (g.get("delta") or "").strip()
        pct = _pct_pill(g.get("pctile"))
        chg = _chg_span(g.get("chg"))

        if metric:
            # 新格式：value 是短數字、metric 是 ≤10 字序列名。
            val_html = f'<div class="val" title="{esc(value)}">{esc(value) or DASH}</div>'
            sub_bits = [f'<span class="m" title="{esc(metric)}">{esc(metric)}</span>']
            if chg:
                sub_bits.append(chg)
            if pct:
                sub_bits.append(pct)
            sub_html = f'<div class="sub">{"".join(sub_bits)}</div>'
        else:
            # 舊格式：value／delta 可能是整句 — 夾住行數，永不出現半截字。
            val_html = f'<div class="val long" title="{esc(value)}">{esc(value) or DASH}</div>'
            sub_bits = []
            if delta:
                sub_bits.append(f'<span class="m" title="{esc(delta)}">{esc(delta)}</span>')
            if chg:
                sub_bits.append(chg)
            if pct:
                sub_bits.append(pct)
            sub_html = (
                f'<div class="sub long">{"".join(sub_bits)}</div>' if sub_bits else ""
            )
        tiles.append(
            f'<div class="{cls}">'
            f'<div class="lab"><span class="dot"></span>{label}</div>'
            f"{val_html}{sub_html}</div>"
        )
    # 2026-08-20：儀表列鎖死 7＋6 兩排（持有人回饋「每天固定排列」）——13 個固定
    # 維度依序排完後，補齊到 7 的倍數（目前恆為 1 格），讓桌機永遠是兩排整齊的
    # 7／6+1，格位不隨螢幕寬度或缺資料重排。缺資料的維度本身已由 build_gauges()
    # 的 emit() 用「無新增訊號」佔位輸出，不會整格消失；這裡補的是「湊滿整排」
    # 的視覺留白格，不是資料缺格。
    pad = (-len(tiles)) % 7
    for _ in range(pad):
        tiles.append('<div class="g blank" aria-hidden="true"><span class="bd">—</span></div>')
    return '<div class="gauges" aria-label="市場儀表">\n' + "\n".join(tiles) + "\n</div>"


# ------------------------------------------------------------------- flags

def _flag_link(fl) -> str:
    link = fl.get("link") or ""
    if not (link and _safe_href(link)):
        return f'<span class="mut">{DASH}</span>'
    text = "報告 ↗" if link.startswith("/macro/") or link.startswith("/id/") else "詳情 ↗"
    return f'<a href="{esc(link)}" rel="noopener nofollow">{esc(text)}</a>'


def _dist_cell(fl) -> str:
    d = fl.get("distance_pct")
    if (fl.get("level") or "").lower() == "confirmed" and d in (None, ""):
        return '<div class="dist"><div class="bar"><i style="width:100%"></i></div>' \
               '<span class="dv">已觸發</span></div>'
    try:
        v = float(d)
    except (TypeError, ValueError):
        return f'<span class="dv">{DASH}</span>'
    prox = 100.0 - abs(v)
    prox = 0.0 if prox < 0 else 100.0 if prox > 100 else prox
    return (
        f'<div class="dist"><div class="bar" role="img" aria-label="距離門檻 {esc(f"{v:g}")}%">'
        f'<i style="width:{prox:.0f}%"></i></div>'
        f'<span class="dv">{esc(f"{abs(v):g}")}%</span></div>'
    )


FLAG_HEAD = (
    "<thead><tr><th>等級</th><th>主題</th><th>指標</th><th>現值</th>"
    "<th>門檻</th><th>距離</th><th>來源</th></tr></thead>"
)
FLAG_HEAD_PLAIN = "<thead><tr><th>等級</th><th>內容</th><th>來源</th></tr></thead>"


def _flag_structured(fl) -> bool:
    return bool(
        (fl.get("metric") or "").strip()
        or (fl.get("theme") or "").strip()
        or fmt_num(fl.get("value"))
        or fmt_num(fl.get("threshold"))
    )


def render_flags(flags: list) -> str:
    if not flags:
        return '<div class="empty">今日無轉折警示。</div>'
    ordered = sorted(
        flags, key=lambda f: FLAG_ORDER.get((f.get("level") or "near").lower(), 3)
    )
    any_structured = any(_flag_structured(f) for f in ordered)
    rows = []
    for fl in ordered:
        level = (fl.get("level") or "near").lower()
        if level not in FLAG_LABEL:
            level = "near"
        pill = f'<span class="pill {level}">{FLAG_LABEL[level]}</span>'
        metric = (fl.get("metric") or "").strip()
        value = fmt_num(fl.get("value"))
        threshold = fmt_num(fl.get("threshold"))
        theme = (fl.get("theme") or "").strip()
        if _flag_structured(fl):
            rows.append(
                f'<tr class="{level}"><td class="lv">{pill}</td>'
                f'<td class="thm">{esc(theme) or DASH}</td>'
                f"<td>{esc(metric) or DASH}</td>"
                f'<td class="num">{esc(value) or DASH}</td>'
                f'<td class="num">{esc(threshold) or DASH}</td>'
                f"<td>{_dist_cell(fl)}</td>"
                f"<td>{_flag_link(fl)}</td></tr>"
            )
        else:
            text = esc(fl.get("text_zh") or "")
            span = 5 if any_structured else 1
            rows.append(
                f'<tr class="{level}"><td class="lv">{pill}</td>'
                f'<td class="span" colspan="{span}">{text}</td>'
                f"<td>{_flag_link(fl)}</td></tr>"
            )
    cls = "t flags" if any_structured else "t flags plain"
    return (
        f'<div class="twrap"><table class="{cls}">'
        + (FLAG_HEAD if any_structured else FLAG_HEAD_PLAIN)
        + "<tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


# -------------------------------------------------------------------- brief

_LEAD_B_RE = re.compile(r"^\s*<b>(.{1,14}?)</b>")


def render_brief(brief_zh: list) -> str:
    if not brief_zh:
        return '<div class="empty">今日市場早報尚未產出。</div>'
    paras = []
    for i, raw in enumerate(brief_zh):
        body = sanitize_brief(raw)
        body = _LEAD_B_RE.sub(lambda m: f'<b class="lead-chip">{m.group(1)}</b>', body, count=1)
        cls = ' class="lead"' if i == 0 else ""
        paras.append(f"<p{cls}>{body}</p>")
    return '<div class="brief">\n' + "\n".join(paras) + "\n</div>"


# --------------------------------------------------------------- card bits

def is_rumor(card) -> bool:
    return bool(
        card.get("is_rumor")
        or card.get("kind") == "rumor"
        or card.get("source_tier") in ("T3", "T4")
    )


def is_title_only(card) -> bool:
    return card.get("summarized") is False


def source_short(card) -> str:
    """≤10 字的來源短名：優先用 source_short，否則從 source_name 砍掉破折號／
    括號後的補述。長度由 CSS 省略號負責，這裡只做語意裁切。"""
    s = (card.get("source_short") or "").strip()
    if s:
        return s
    name = (card.get("source_name") or card.get("source") or "").strip()
    if not name:
        return ""
    for sep in (" — ", " – ", " - ", "—", "（", "(", "｜", "|", "："):
        if sep in name:
            name = name.split(sep, 1)[0].strip()
            break
    return name.strip(" ·")


def tier_badge(card) -> str:
    tier = (card.get("source_tier") or "").strip()
    if not tier:
        return ""
    cls = "tier " + tier.lower()
    return f'<span class="{cls}">{esc(tier)}</span>'


def card_tags_html(card, thread_map=None) -> str:
    thread_map = thread_map or {}
    tags = card.get("tags") or {}
    out = []
    propagated = tags.get("propagated_to") or []
    tickers = tags.get("tickers") or []
    if propagated:
        out.append(f'<span class="tag p">→ {esc(" · ".join(propagated))}</span>')
    elif tickers:
        out.append(f'<span class="tag p">{esc(" · ".join(tickers[:3]))}</span>')
    if is_rumor(card):
        out.append('<span class="tag r">傳聞</span>')
    tid = card.get("thread_id")
    if tid:
        title_zh = thread_map.get(tid)
        if title_zh:
            out.append(f'<a class="tag th" href="#thread-{esc(tid)}">🧵 {esc(title_zh)}</a>')
    return "".join(out)


_DATA_KEYS = (("value", "現值"), ("pctile", "分位"), ("threshold", "門檻"),
              ("change_20d", "20 日變化"), ("prev", "前值"), ("status", "狀態"),
              ("as_of", "截至"), ("rule", "規則"), ("severity", "等級"),
              ("series", "序列"))


def render_data_line(data) -> str:
    """數字卡的 data 欄：把 value／分位／門檻等以「鍵：值」列出（純文字、全部 escape）。"""
    if not isinstance(data, dict):
        return ""
    parts = []
    for key, label in _DATA_KEYS:
        v = data.get(key)
        if v is None or v == "":
            continue
        parts.append(f"{label} {esc(fmt_num(v))}")
    if data.get("doc"):
        parts.append(f'<a href="/{esc(str(data["doc"]).replace("docs/", "", 1))}">相關報告</a>')
    return ('<div class="mono">' + " · ".join(parts) + "</div>") if parts else ""


_TITLE_PREFIX_RE = re.compile(r"^\s*\[[^\]]{1,20}\]\s*")


_KEY_PREFIX_RE = re.compile(r"^[a-z0-9_]{2,24}：")


def _card_title(card) -> str:
    t = card.get("summary_zh") or card.get("title") or ""
    if card.get("kind") == "data":
        t = _KEY_PREFIX_RE.sub("", _TITLE_PREFIX_RE.sub("", t))
    return esc(t)


_CONF_LABEL_ZH = {"high": "高信心", "med": "中信心", "low": "低信心"}


def render_deep_block(deep: dict) -> str:
    """「深讀」block：數字小表格＋要點＋接下來看什麼＋實體 chips＋信心度。
    deep_status != "ok"（沒有 deep dict）的卡片一律不呼叫本函式，什麼都不畫。"""
    if not isinstance(deep, dict):
        return ""
    numbers = deep.get("numbers") or []
    entities = deep.get("entities") or {}
    takeaway = esc(deep.get("takeaway_zh") or "")
    watch = esc(deep.get("watch_zh") or "")
    confidence = (deep.get("confidence") or "").lower()
    conf_label = _CONF_LABEL_ZH.get(confidence, "")

    parts = ['<div class="deep">']
    head = '<div class="deep-h">深讀'
    if conf_label:
        head += f'<span class="conf {esc(confidence)}">{esc(conf_label)}</span>'
    head += "</div>"
    parts.append(head)

    if numbers:
        rows = []
        for n in numbers[:6]:
            what = esc(n.get("what") or "")
            value = esc(n.get("value") or "")
            period = n.get("period") or ""
            period_html = f' <span class="mut">{esc(period)}</span>' if period else ""
            rows.append(f"<tr><td>{what}</td><td class=\"num\">{value}{period_html}</td></tr>")
        parts.append(f'<table class="deep-nums"><tbody>{"".join(rows)}</tbody></table>')
    if takeaway:
        parts.append(f'<div class="deep-take"><b>要點：</b>{takeaway}</div>')
    if watch:
        parts.append(f'<div class="deep-watch"><b>接下來看：</b>{watch}</div>')

    chips = []
    for key in ("tickers", "themes", "countries"):
        for v in (entities.get(key) or [])[:6]:
            chips.append(f'<span class="chip2">{esc(v)}</span>')
    if chips:
        parts.append('<div class="deep-ent">' + "".join(chips) + "</div>")

    parts.append("</div>")
    return "".join(parts)


def render_row(card, thread_map=None) -> str:
    """一列 = <details>；<summary> 本身是整條 grid（時間｜重要度｜標題｜來源｜tier+chevron）。
    未摘要（summarized == False）的卡片改用純 <div>，不掛 chevron。"""
    t = fmt_hm(card_time(card))
    imp = int(card.get("importance") or 1)
    imp = 1 if imp < 1 else 3 if imp > 3 else imp
    title = _card_title(card)
    src = esc(source_short(card))
    tier = tier_badge(card)
    url = card.get("url") or ""
    safe_url = url if (url and _safe_href(url)) else ""

    head_cells = (
        f'<span class="t">{esc(t)}</span>'
        f'<span class="imp i{imp}" aria-hidden="true"></span>'
    )

    if is_title_only(card):
        ttl = (
            f'<span class="ti"><a href="{esc(safe_url)}" rel="noopener nofollow">{title}</a></span>'
            if safe_url else f'<span class="ti">{title}</span>'
        )
        return (
            '<div class="plain">' + head_cells + ttl
            + f'<span class="src" title="{esc(card.get("source_name") or "")}">{src}</span>'
            + f'<span class="end">{tier}</span></div>'
        )

    tags_html = card_tags_html(card, thread_map)
    why = esc(card.get("why_zh") or "")
    summary_zh = esc(card.get("summary_zh") or "")
    full_title = esc(card.get("title") or "")

    body_bits = []
    if summary_zh and summary_zh != title:
        body_bits.append(f"<div>{summary_zh}</div>")
    elif full_title and _TITLE_PREFIX_RE.sub("", full_title).strip() != title:
        body_bits.append(f'<div class="why"><b>原標題：</b>{full_title}</div>')
    if why:
        body_bits.append(f'<div class="why"><b>為什麼重要：</b>{why}</div>')
    data_html = render_data_line(card.get("data"))
    if data_html:
        body_bits.append(data_html)
    if card.get("deep") and card.get("deep_status") == "ok":
        body_bits.append(render_deep_block(card["deep"]))

    meta_bits = []
    src_full = esc(card.get("source_name") or card.get("source") or "")
    if src_full:
        meta_bits.append(f"來源 {src_full}")
    corrob = card.get("corroboration")
    if corrob and int(corrob) >= 2:
        meta_bits.append(f"{int(corrob)} 源交叉")
    cat = card.get("category")
    if cat:
        meta_bits.append(esc(cat_label(cat)))
    if safe_url:
        meta_bits.append(f'<a href="{esc(safe_url)}" rel="noopener nofollow">原文 ↗</a>')
    if meta_bits:
        body_bits.append('<div class="meta">' + "".join(
            f"<span>{b}</span>" for b in meta_bits) + "</div>")
    if not body_bits:
        body_bits.append('<div class="meta"><span>本卡無補充內容。</span></div>')

    return (
        '<details class="r"><summary>'
        + head_cells
        + f'<span class="ti">{title}{tags_html}</span>'
        + f'<span class="src" title="{src_full}">{src}</span>'
        + f'<span class="end">{tier}<span class="chev" aria-hidden="true"></span></span>'
        + "</summary>"
        + '<div class="body">' + "".join(body_bits) + "</div></details>"
    )


LIST_HEAD = (
    '<div class="head rowgrid"><span>時間</span><span></span><span>標題</span>'
    '<span class="hsrc">來源</span><span>來源層級</span></div>'
)


def group_header(label: str, n: int) -> str:
    return f'<div class="grp">{esc(label)}<span class="c">{n}</span></div>'


def render_grouped_list(cards: list, order: list, empty_text: str, thread_map=None) -> str:
    """依 category 分組（order 先、其餘依卡片數排序），空組略過。"""
    if not cards:
        return f'<div class="list">{LIST_HEAD}<div class="empty">{esc(empty_text)}</div></div>'
    by_cat = {}
    for c in cards:
        by_cat.setdefault(c.get("category") or "other", []).append(c)
    seq = [c for c in order if c in by_cat]
    seq += sorted((c for c in by_cat if c not in seq), key=lambda k: -len(by_cat[k]))
    parts = [LIST_HEAD]
    for cat in seq:
        items = sorted(by_cat[cat], key=card_sort_key)
        parts.append(group_header(cat_label(cat), len(items)))
        parts.extend(render_row(c, thread_map) for c in items)
    return '<div class="list">' + "\n".join(parts) + "</div>"


def render_flat_list(cards: list, empty_text: str, thread_map=None) -> str:
    if not cards:
        return f'<div class="list">{LIST_HEAD}<div class="empty">{esc(empty_text)}</div></div>'
    rows = "\n".join(render_row(c, thread_map) for c in sorted(cards, key=card_sort_key))
    return f'<div class="list">{LIST_HEAD}\n{rows}\n</div>'


def render_title_list(cards: list) -> str:
    """未摘要卡片：兩欄標題清單（標題 + 來源 + 時間）。"""
    if not cards:
        return ""
    items = []
    for c in sorted(cards, key=card_sort_key):
        title = _card_title(c)
        url = c.get("url") or ""
        h = (
            f'<a href="{esc(url)}" rel="noopener nofollow">{title}</a>'
            if url and _safe_href(url) else title
        )
        src = esc(source_short(c))
        items.append(
            '<div class="ti2">'
            f'<span class="h">{h}</span>'
            f'<span class="m">{esc(fmt_hm(card_time(c)))}</span>'
            f'<span class="s">{src}</span>'
            "</div>"
        )
    return '<div class="tlist">' + "\n".join(items) + "</div>"


# ---------------------------------------------- 「其他標題」改版（Task B，2026-08-20）
# 持有人原話：「其他標題 277 這個那麼多其實等於沒有 因為不會看」。改法：同題去重
# （title token Jaccard ≥0.6）→ 只在上方列「值得一瞥」的重要度前 30 則（單一類別
# ≤5 則避免洗版）→ 其餘依類別收合在 <details> 裡，不再是一段看不完的兩欄清單。

_TITLE_ONLY_TIER_RANK = {"T1": 0, "T2": 1, "T3": 2, "T4": 3}
_CJK_CHAR_RE = re.compile(r"[一-鿿]")
_CHUNK_RE = re.compile(r"[一-鿿]+|[^一-鿿]+")
_ASCII_WORD_RE = re.compile(r"[a-z0-9]+")
_DEDUP_JACCARD_THRESHOLD = 0.6
_TITLE_ONLY_VISIBLE_LIMIT = 30
_TITLE_ONLY_PER_CAT_CAP = 5
_RUMOR_TITLE_ONLY_SHOW_LIMIT = 20


def _title_only_text(card) -> str:
    """同 `_card_title` 的文字來源（summary_zh 優先、data 卡去前綴），但不 escape
    ——同題去重比對用原文 token，escape 與否不影響比對結果，直接用原文較省事。"""
    t = card.get("summary_zh") or card.get("title") or ""
    if card.get("kind") == "data":
        t = _KEY_PREFIX_RE.sub("", _TITLE_PREFIX_RE.sub("", t))
    return t


def _title_ngram_tokens(title: str) -> set:
    """同題判斷用的 token 集合：中文連續字用 2-gram（bigram），英文/數字用小寫
    整詞。跟 fetch.py 既有（較鬆、只比對同日窗內）的去重邏輯是兩套獨立實作，
    互不共用——這裡要的是「同一則新聞被多來源轉載」的精準判斷，不是粗篩。"""
    t = (title or "").strip()
    tokens: set = set()
    for chunk in _CHUNK_RE.findall(t):
        if not chunk or not chunk.strip():
            continue
        if _CJK_CHAR_RE.match(chunk[0]):
            n = len(chunk)
            if n < 2:
                tokens.add(chunk)
            else:
                tokens.update(chunk[i:i + 2] for i in range(n - 1))
        else:
            tokens.update(_ASCII_WORD_RE.findall(chunk.lower()))
    return tokens


def _title_jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if not inter:
        return 0.0
    union = len(a) + len(b) - inter
    return inter / union if union else 0.0


def dedup_title_only(cards: list) -> list:
    """同題去重（title token Jaccard ≥0.6 視為同一則），回傳 `[(代表卡, 同題數)]`。
    代表卡＝該群裡 tier 最高（T1 最佳）、同 tier 取最新的一則；同題數＝群內其餘
    則數（渲染時掛「＋n 同題」灰字後綴）。O(n²) 比對，「其他標題」單日量級（幾百
    則）可接受，不需要更複雜的索引結構。"""
    n = len(cards)
    if n == 0:
        return []
    tokens = [_title_ngram_tokens(_title_only_text(c)) for c in cards]

    def priority(i):
        return (_TITLE_ONLY_TIER_RANK.get(cards[i].get("source_tier"), 9), -sort_epoch(cards[i]))

    order = sorted(range(n), key=priority)
    assigned = [False] * n
    out = []
    for i in order:
        if assigned[i]:
            continue
        cluster = [i]
        assigned[i] = True
        for j in order:
            if assigned[j]:
                continue
            if _title_jaccard(tokens[i], tokens[j]) >= _DEDUP_JACCARD_THRESHOLD:
                cluster.append(j)
                assigned[j] = True
        rep_idx = min(cluster, key=priority)
        out.append((cards[rep_idx], len(cluster) - 1))
    return out


def _select_visible_title_only(deduped: list) -> tuple:
    """依 importance desc → tier T1>T2>T3>T4 desc → 新到舊排序，取前
    `_TITLE_ONLY_VISIBLE_LIMIT` 則，同一類別最多 `_TITLE_ONLY_PER_CAT_CAP` 則
    （避免單一類別洗版）。回傳 (visible, rest)，兩者皆為 `(卡, 同題數)` list。"""
    def key(pair):
        c, _dup = pair
        imp = int(c.get("importance") or 1)
        tier_rank = _TITLE_ONLY_TIER_RANK.get(c.get("source_tier"), 9)
        return (-imp, tier_rank, -sort_epoch(c))

    ordered = sorted(deduped, key=key)
    visible, rest = [], []
    cat_count: dict = {}
    for pair in ordered:
        c, _dup = pair
        cat = c.get("category") or "other"
        if len(visible) < _TITLE_ONLY_VISIBLE_LIMIT and cat_count.get(cat, 0) < _TITLE_ONLY_PER_CAT_CAP:
            visible.append(pair)
            cat_count[cat] = cat_count.get(cat, 0) + 1
        else:
            rest.append(pair)
    return visible, rest


def _render_title_only_row(card, dup_count: int = 0) -> str:
    """一行一則：時間｜類別 chip｜標題（連結）｜來源短名｜tier。"""
    t = fmt_hm(card_time(card))
    title = _card_title(card)
    url = card.get("url") or ""
    h = (
        f'<a href="{esc(url)}" rel="noopener nofollow">{title}</a>'
        if url and _safe_href(url) else title
    )
    if dup_count > 0:
        h += f' <span class="dupn">＋{dup_count} 同題</span>'
    src = esc(source_short(card))
    tier = tier_badge(card)
    cat = card.get("category")
    cat_chip = f'<span class="cchip">{esc(cat_label(cat))}</span>' if cat else '<span class="cchip"></span>'
    return (
        '<div class="ti3">'
        f'<span class="m">{esc(t)}</span>'
        f'{cat_chip}'
        f'<span class="h">{h}</span>'
        f'<span class="s">{src}</span>'
        f'<span class="tr">{tier}</span>'
        "</div>"
    )


def render_title_only_section(cards: list) -> tuple:
    """「其他標題」整段（去重＋top 30＋依類別收合）。回傳 (html, visible_n, raw_total)。"""
    raw_total = len(cards)
    if raw_total == 0:
        return "", 0, 0
    deduped = dedup_title_only(cards)
    visible, rest = _select_visible_title_only(deduped)
    visible_n = len(visible)

    parts = ['<div class="tlist2">']
    parts.extend(_render_title_only_row(c, dup) for c, dup in visible)
    parts.append("</div>")

    if rest:
        rest_raw_n = raw_total - visible_n  # 含被摺進代表卡裡的同題則數
        by_cat: dict = {}
        for pair in rest:
            cat = pair[0].get("category") or "other"
            by_cat.setdefault(cat, []).append(pair)
        cat_order = sorted(by_cat.keys(), key=lambda k: -len(by_cat[k]))
        parts.append(f'<details class="tmore"><summary>其餘 {rest_raw_n} 則（依類別收合）</summary>')
        for cat in cat_order:
            items = sorted(by_cat[cat], key=lambda pair: card_sort_key(pair[0]))
            parts.append(
                f'<details class="tcat"><summary>{esc(cat_label(cat))}'
                f'<span class="c">{len(items)}</span></summary>'
                '<div class="tlist2">'
                + "".join(_render_title_only_row(c, dup) for c, dup in items)
                + "</div></details>"
            )
        parts.append("</details>")

    return "".join(parts), visible_n, raw_total


def render_dense_feed(cards: list, thread_map=None) -> str:
    """版型 B：全部卡片一行一則，依層級分組。"""
    by_level = {}
    for c in cards:
        by_level.setdefault(c.get("level") or "market", []).append(c)
    parts = [LIST_HEAD]
    any_rows = False
    seq = [lv for lv in LEVEL_ORDER if lv in by_level]
    seq += [lv for lv in by_level if lv not in LEVEL_ORDER]
    for lv in seq:
        items = by_level.get(lv) or []
        if not items:
            continue
        any_rows = True
        parts.append(group_header(LEVEL_LABEL_ZH.get(lv, lv), len(items)))
        parts.extend(render_row(c, thread_map) for c in sorted(items, key=card_sort_key))
    if not any_rows:
        parts.append('<div class="empty">今日尚無卡片。</div>')
    return '<div class="list">' + "\n".join(parts) + "</div>"


# ------------------------------------------------------------------ threads

HEAT_ARROW = {"up": "▲", "down": "▼", "flat": "→"}
HEAT_LABEL_ZH = {"up": "升溫", "down": "降溫", "flat": "持平"}


def _sparkline_svg(values: list, width: int = 100, height: int = 22) -> str:
    """14 天迷你長條圖，inline SVG（無外部資源，符合站台自我約束）。"""
    if not values:
        return ""
    n = len(values)
    maxv = max(values) or 1
    bw = width / n
    bars = []
    for i, v in enumerate(values):
        h = 2 if v <= 0 else max(2, round((v / maxv) * (height - 3)) + 2)
        x = round(i * bw)
        w = max(1.0, bw - 1)
        y = height - h
        bars.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="1"></rect>')
    return (
        f'<svg class="spark" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'preserveAspectRatio="none" role="img" aria-label="近 14 天卡片數">'
        + "".join(bars) + "</svg>"
    )


HEAT_SORT_RANK = {"up": 0, "flat": 1, "down": 2}
THREAD_OPEN_TOP_N = 3  # 升溫的前 N 條預設展開


def _thread_source_short(url: str) -> str:
    """從最新標題的 URL 取網域當來源短名（thread.latest[] 只有 url/title/date，
    沒有 source_name/source_short 欄位，故從連結本身推短名，非資料造假）。"""
    if not url:
        return ""
    try:
        host = (urlparse(url).netloc or "").lower()
    except ValueError:
        return ""
    host = re.sub(r"^www\.", "", host)
    return host[:16]


def render_threads(threads: list) -> str:
    """進行中的故事線：一行一條清單（`<details>`/`<summary>`，無 JS）——
    熱度 pill／主題／第 N 天／今日 +n／14 天 sparkline／最新一則標題（單行截斷）
    的緊湊列；點列展開最新 2–3 則（連原文／來源短名／日期）。排序＝升溫→持平→
    降溫，同組內依今日新增數 desc、再依天數 desc；升溫前 3 條預設展開。空陣列
    由呼叫端負責整段（含 h2）省略。"""
    if not threads:
        return ""

    def _sort_key(t: dict):
        heat = t.get("heat") if t.get("heat") in HEAT_ARROW else "flat"
        return (
            HEAT_SORT_RANK.get(heat, 1),
            -(t.get("today_count") or 0),
            -(t.get("day_n") or 0),
        )

    ordered = sorted(threads, key=_sort_key)
    up_total = sum(1 for t in ordered if (t.get("heat") or "flat") == "up")
    open_budget = min(THREAD_OPEN_TOP_N, up_total)

    rows_html = []
    opened = 0
    for t in ordered:
        tid = t.get("id") or ""
        title_zh = esc(t.get("title_zh") or "")
        day_n = t.get("day_n") or 1
        today_n = t.get("today_count") or 0
        heat = t.get("heat") or "flat"
        if heat not in HEAT_ARROW:
            heat = "flat"
        arrow = HEAT_ARROW[heat]
        heat_zh = HEAT_LABEL_ZH.get(heat, "")
        spark = _sparkline_svg(t.get("sparkline") or [], width=80, height=18)
        latest = t.get("latest") or []

        is_open = heat == "up" and opened < open_budget
        if is_open:
            opened += 1

        # 收合行的「最新一則標題」欄
        if latest:
            top = latest[0]
            top_title = esc((top.get("title") or "")[:120])
            top_url = top.get("url") or ""
            if top_title and top_url and _safe_href(top_url):
                latest_cell = f'<a href="{esc(top_url)}" rel="noopener nofollow">{top_title}</a>'
            elif top_title:
                latest_cell = f"<span>{top_title}</span>"
            else:
                latest_cell = f'<span class="mut">{DASH}</span>'
        elif heat == "down" and today_n == 0:
            latest_cell = '<span class="mut">今日無新卡</span>'
        else:
            latest_cell = f'<span class="mut">{DASH}</span>'

        # 展開內容：最新 2–3 則（連原文／來源短名／日期）
        detail_items = []
        for e in latest[:3]:
            eu = e.get("url") or ""
            et = esc((e.get("title") or "")[:160])
            if not et:
                continue
            src = esc(_thread_source_short(eu))
            when = (e.get("date") or "")[5:]  # MM-DD
            meta_bits = [b for b in (src, when) if b]
            meta_html = f'<span class="th-meta">{" · ".join(meta_bits)}</span>' if meta_bits else ""
            if eu and _safe_href(eu):
                detail_items.append(f'<li><a href="{esc(eu)}" rel="noopener nofollow">{et}</a>{meta_html}</li>')
            else:
                detail_items.append(f"<li>{et}{meta_html}</li>")
        detail_html = (
            f'<ul class="th-l">{"".join(detail_items)}</ul>' if detail_items
            else '<div class="th-empty">今日無新卡</div>'
        )

        rows_html.append(
            f'<details class="thr" id="thread-{esc(tid)}"{" open" if is_open else ""}>'
            f"<summary>"
            f'<span class="hpill {esc(heat)}" title="{esc(heat_zh)}">{arrow} {esc(heat_zh)}</span>'
            f'<span class="tt">{title_zh}</span>'
            f'<span class="thd">第 {esc(fmt_num(day_n))} 天</span>'
            f'<span class="thn">今日 +{esc(fmt_num(today_n))}</span>'
            f'<span class="thsp">{spark}</span>'
            f'<span class="thlast">{latest_cell}</span>'
            f'<span class="chev"></span>'
            f"</summary>"
            f'<div class="thr-body">{detail_html}</div>'
            f"</details>"
        )
    return '<div class="threads">' + "\n".join(rows_html) + "</div>"


# ------------------------------------------------------------- aside boxes

def render_focus(cards: list, n: int = 5) -> str:
    pool = [c for c in cards if not is_rumor(c) and not is_title_only(c)]
    top = sorted(pool, key=card_sort_key)[:n]
    if not top:
        return '<div class="box"><h3>今日焦點<span>Focus</span></h3>' \
               '<div class="cal"><div class="none">今日尚無卡片。</div></div></div>'
    items = []
    for c in top:
        imp = int(c.get("importance") or 1)
        imp = 1 if imp < 1 else 3 if imp > 3 else imp
        title = _card_title(c)
        url = c.get("url") or ""
        h = (
            f'<a href="{esc(url)}" rel="noopener nofollow">{title}</a>'
            if url and _safe_href(url) else f'<span class="h">{title}</span>'
        )
        mt = [esc(cat_label(c.get("category")))]
        s = source_short(c)
        if s:
            mt.append(esc(s))
        t = fmt_hm(card_time(c))
        if t != DASH:
            mt.append(esc(t))
        items.append(
            f'<li><span class="imp i{imp}" aria-hidden="true"></span>'
            f'<span class="tx">{h}<span class="mt">'
            + "".join(f"<span>{m}</span>" for m in mt)
            + "</span></span></li>"
        )
    return (
        '<div class="box"><h3>今日焦點<span>Focus</span></h3>'
        '<ul class="focus">' + "\n".join(items) + "</ul></div>"
    )


def render_calendar(calendar: list, base_date) -> str:
    """接下來 7 天（base_date+1 .. base_date+7）；今天本身已被早報／儀表覆蓋。"""
    by_date = {}
    for e in calendar or []:
        by_date.setdefault(e.get("date"), []).append(e)
    items = []
    for i in range(1, 8):
        d = base_date + timedelta(days=i)
        ds = d.isoformat()
        events = by_date.get(ds) or []
        if not events:
            continue
        label = f"{d.month:02d}/{d.day:02d}（{weekday_zh(d)}）"
        for e in events:
            impact = (e.get("impact") or "").lower()
            dot_cls = f"idot {impact}" if impact in ("high", "medium", "low") else "idot"
            hi = " hi" if e.get("hi") or impact == "high" else ""
            mt = []
            if e.get("time"):
                mt.append(esc(e["time"]))
            if e.get("country"):
                mt.append(esc(e["country"]))
            if e.get("forecast") not in (None, ""):
                mt.append("預估 " + esc(fmt_num(e["forecast"])))
            if e.get("previous") not in (None, ""):
                mt.append("前值 " + esc(fmt_num(e["previous"])))
            mt_html = (
                '<span class="mt">' + "".join(f"<span>{m}</span>" for m in mt) + "</span>"
            ) if mt else ""
            items.append(
                f'<li><span class="d">{esc(label)}</span>'
                f'<span class="ev{hi}"><span class="{dot_cls}" aria-hidden="true"></span>'
                f'{esc(e.get("text") or "")}{mt_html}</span></li>'
            )
    more = ""
    if len(items) > 12:
        more = f'<div class="mut" style="font-size:12px;margin-top:6px">…另有 {len(items) - 12} 項（見完整 JSON）</div>'
        items = items[:12]
    inner = (
        '<ul class="cal">' + "\n".join(items) + "</ul>" + more
        if items else '<div class="none">接下來 7 天無排定事件。</div>'
    )
    return '<div class="box"><h3>接下來 7 天<span>Calendar</span></h3>' + inner + "</div>"


def render_mini_status(status: dict, cards_n: int) -> str:
    if not status:
        rows = [("卡片", str(cards_n))]
    else:
        ok, fail = status.get("sources_ok"), status.get("sources_fail")
        tokens = status.get("tokens") or {}
        total_tok = sum(v for v in tokens.values() if isinstance(v, (int, float)))
        rows = []
        if ok is not None:
            rows.append(("來源正常", f"{ok}／{(ok or 0) + (fail or 0)}"))
        if status.get("fetched") is not None:
            rows.append(("抓取 → 保留", f"{status.get('fetched')} → {status.get('kept', DASH)}"))
        rows.append(("卡片", str(cards_n)))
        if total_tok:
            rows.append(("今日 token", f"{int(total_tok):,}"))
        if status.get("next_run"):
            rows.append(("下次排程", str(status["next_run"])))
    body = "".join(f"<div><span>{esc(k)}</span><b>{esc(v)}</b></div>" for k, v in rows)
    return (
        '<div class="box"><h3>資料狀態<span>Status</span></h3>'
        f'<div class="mini">{body}</div>'
        '<div class="mini" style="margin-top:6px">'
        '<a class="back" href="/intel/status.html">完整來源健康表 →</a></div></div>'
    )


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
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>"""


FOOT = (
    '<footer class="imq-foot"><div class="in">'
    "<div>本頁為機械聚合＋LLM 摘要：固定來源清單每日抓取 → 規則過濾 → 分類與中文摘要 →"
    "靜態渲染；儀表與轉折警示取自站內既有監測管線，卡片內容為第三方來源之摘要，"
    "正確性以原文為準。</div>"
    '<div><a href="/monitor/">市場監測</a> <span class="sep">·</span> '
    '<a href="/detective/">主題偵測</a> <span class="sep">·</span> '
    '<a href="/crowding/">擁擠交易</a> <span class="sep">·</span> '
    '<a href="/intel/archive.html">歷史</a> <span class="sep">·</span> '
    '<a href="/intel/status.html">狀態</a> <span class="sep">·</span> '
    '<a href="/disclosures.html">方法論與揭露</a></div>'
    "<div>聲明：本頁為市場狀態的描述器，只陳述觀察到的數字與新聞，"
    "不做買賣建議、不預測價格。© 2026 InvestMQuest Research</div>"
    "</div></footer>"
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


def _mast_chips(payload: dict, cards: list, archive_link: bool) -> str:
    status = payload.get("status") or {}
    chips = []
    llm = (payload.get("llm") or "").strip()
    if llm:
        cls = "chip ok" if llm.lower() in ("ok", "正常") else "chip warn"
        chips.append(f'<span class="{cls}">LLM <b>{esc(llm)}</b></span>')
    ok, fail = status.get("sources_ok"), status.get("sources_fail")
    if ok is not None:
        total = (ok or 0) + (fail or 0)
        cls = "chip ok" if not fail else "chip warn"
        chips.append(f'<span class="{cls}">來源 <b>{ok}／{total}</b></span>')
    chips.append(f'<span class="chip">卡片 <b>{len(cards)}</b></span>')
    if archive_link:
        chips.append('<a class="chip" href="/intel/">回今日</a>')
    chips.append('<a class="chip" href="/intel/archive.html">歷史</a>')
    chips.append('<a class="chip" href="/intel/status.html">狀態</a>')
    return '<div class="chips">' + "".join(chips) + "</div>"


def h2(zh: str, en: str, count=None) -> str:
    cnt = f'<span class="cnt">{count}</span>' if count is not None else ""
    return f'<h2>{esc(zh)}<span class="en">{esc(en)}</span>{cnt}</h2>'


def build_day_body(date_str: str, payload: dict, mode_note: str, is_archive: bool) -> str:
    gauges = payload.get("gauges") or []
    flags = payload.get("flags") or []
    brief_zh = payload.get("brief_zh") or []
    cards = payload.get("cards") or []
    calendar = payload.get("calendar") or []
    status = payload.get("status") or {}
    generated_at = payload.get("generated_at")

    threads = payload.get("threads") or []
    thread_map = {t.get("id"): t.get("title_zh") for t in threads if t.get("id")}

    title_only = [c for c in cards if is_title_only(c)]
    main = [c for c in cards if not is_title_only(c)]
    rumor_cards = [c for c in main if is_rumor(c)]
    solid = [c for c in main if not is_rumor(c)]
    market_cards = [c for c in solid if (c.get("level") or "market") == "market"]
    industry_cards = [c for c in solid if c.get("level") == "industry"]
    company_cards = [c for c in solid if c.get("level") == "company"]
    # Task B（2026-08-20）：未摘要傳聞卡不進「其他標題」，改摺進傳聞區底部。
    title_only_rumor = [c for c in title_only if is_rumor(c)]
    title_only_other = [c for c in title_only if not is_rumor(c)]

    base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    wd = weekday_zh(base_date)
    when = fmt_hm(generated_at)

    p = []
    p.append('<div class="wrap">')

    # 1. masthead
    p.append('<div class="mast">')
    p.append(
        '<div class="ttl"><h1>全球金融市場監視器</h1>'
        f'<div class="date">{esc(date_str)}（{wd}）'
        f'　·　更新 <b>{esc(when)}</b> 台北時間</div></div>'
    )
    p.append(
        '<div class="seg" role="group" aria-label="版型">'
        '<button type="button" data-set="brief" aria-pressed="true">A · 早報</button>'
        '<button type="button" data-set="list" aria-pressed="false">B · 純列表</button>'
        "</div>"
    )
    p.append(_mast_chips(payload, cards, is_archive))
    p.append("</div>")

    if mode_note:
        p.append(mode_note)

    # 2. 儀表列
    p.append(h2("儀表列", "Gauges", len(gauges) or None))
    p.append(render_gauges(gauges))

    # 3. 轉折警示
    p.append(h2("轉折警示", "Alerts", len(flags) or None))
    p.append(render_flags(flags))

    # 3.5 進行中的故事線（空陣列整段省略，含標題）
    if threads:
        p.append(h2("進行中的故事線", "Threads", len(threads)))
        p.append(render_threads(threads))

    # 4. 市場早報（雙欄）
    p.append('<section class="only-brief">')
    p.append(h2("市場早報", "Brief"))
    p.append('<div class="sheet"><div class="main">')
    p.append(render_brief(brief_zh))
    p.append("</div>")
    p.append('<aside class="side">')
    p.append(render_focus(main))
    p.append(render_calendar(calendar, base_date))
    p.append(render_mini_status(status, len(cards)))
    p.append("</aside></div>")

    # 5. 卡片列表
    p.append(h2("市場層", "Market", len(market_cards)))
    p.append(render_grouped_list(market_cards, GAUGE_ORDER, "今日無市場層卡片。", thread_map))

    p.append(h2("產業層", "Industry", len(industry_cards)))
    p.append(render_grouped_list(industry_cards, [], "今日無產業層卡片。", thread_map))

    p.append(h2("個股層", "Company", len(company_cards)))
    p.append(render_grouped_list(company_cards, [], "今日無個股層卡片。", thread_map))

    if title_only_other:
        section_html, visible_n, raw_n = render_title_only_section(title_only_other)
        p.append(h2("其他標題", "Headlines", f"{visible_n}／{raw_n}"))
        p.append(
            '<p class="note">haiku 篩過但沒進摘要名額的標題；'
            "上面是重要度最高的 30 則，其餘依類別收合。</p>"
        )
        p.append(section_html)

    if rumor_cards or title_only_rumor:
        p.append(h2("傳聞", "Rumor", len(rumor_cards)))
        p.append('<p class="note">只收公開傳聞（T3／T4 來源），不做查證、不代表事實，僅供交叉比對。</p>')
        p.append(render_flat_list(rumor_cards, "今日無 T3／T4 傳聞卡片。", thread_map))
        if title_only_rumor:
            shown = sorted(title_only_rumor, key=card_sort_key)[:_RUMOR_TITLE_ONLY_SHOW_LIMIT]
            p.append(
                f'<details class="tmore"><summary>其餘傳聞標題 {len(title_only_rumor)} 則</summary>'
                + render_title_list(shown)
                + "</details>"
            )
    p.append("</section>")

    # 版型 B：純列表
    p.append('<section class="only-list">')
    p.append(h2("全部卡片", "Feed", len(cards)))
    p.append(render_dense_feed(cards, thread_map))
    p.append("</section>")

    p.append("</div>")  # .wrap
    p.append(FOOT)
    p.append(TOGGLE_SCRIPT)
    return "\n".join(p)


# ------------------------------------------------------------- data loading

def resolve_day_payload(date_str: str, sources_meta: dict, data_path: Path = None):
    """Return (payload, banner_html, is_stale). payload always has all keys."""
    real_path = data_path if data_path is not None else (DATA_DIR / f"{date_str}.json")
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


def render_archive(current_date: str, out_dir: Path) -> str:
    dates = set()
    for p in out_dir.glob("*.html"):
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
        '<div class="mast"><div class="ttl"><h1>監視器封存</h1>'
        '<div class="date">依日期排列</div></div>'
        '<div class="chips"><a class="chip" href="/intel/">回今日</a>'
        '<a class="chip" href="/intel/status.html">狀態</a></div></div>',
        f'<ul class="arclist">{"".join(items)}</ul>' if items else '<div class="empty">尚無封存頁面。</div>',
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
        latency_s = f"{latency} ms" if latency is not None else DASH
        item_count = s.get("item_count")
        item_s = item_count if item_count is not None else DASH
        err = s.get("error") or ""
        err_s = (err[:140] + "…") if len(err) > 140 else err
        rows.append(
            "<tr>"
            f"<td>{esc(sid)}</td><td>{esc(name)}</td><td>{esc(tier)}</td>"
            f'{ok_html}<td class="num">{esc(latency_s)}</td><td class="num">{esc(item_s)}</td>'
            f'<td class="err">{esc(err_s)}</td>'
            "</tr>"
        )
    table = (
        '<div class="twrap"><table class="t stbl"><thead><tr>'
        "<th>source_id</th><th>名稱</th><th>tier</th><th>狀態</th>"
        "<th>延遲</th><th>抓到筆數</th><th>錯誤</th>"
        "</tr></thead><tbody>"
        + ("".join(rows) if rows else '<tr><td colspan="7">健康檢查資料尚未產出。</td></tr>')
        + "</tbody></table></div>"
    )

    tokens = status.get("tokens") or {}
    deep_read = status.get("deep_read") or {}
    deep_s = (
        " · ".join(f"{esc(k)} {v}" for k, v in deep_read.items() if v)
        if any(deep_read.values()) else DASH
    )
    cards = [
        ("健康檢查時間（台北）", esc(fmt_full(health.get("generated_at")))),
        ("今日產出時間（台北）", esc(fmt_full(generated_at))),
        ("來源正常／失敗", f"{status.get('sources_ok', DASH)} ／ {status.get('sources_fail', DASH)}"),
        ("抓到 → 保留", f"{status.get('fetched', DASH)} → {status.get('kept', DASH)}"),
        ("分類 → 摘要", f"{status.get('classified', DASH)} → {status.get('summarized', DASH)}"),
        ("今日 token", " · ".join(f"{esc(k)} {v:,}" for k, v in tokens.items()) or DASH),
        ("深讀（重要卡讀全文）", deep_s),
        ("故事線（進行中／總計）",
         f"{status.get('threads_active', DASH)} ／ {status.get('threads_total', DASH)}"),
        ("下次排程", esc(status.get("next_run") or DASH)),
    ]
    stat_html = "".join(
        f'<div class="c"><div class="k">{k}</div><div class="v">{v}</div></div>'
        for k, v in cards
    )

    body = [
        '<div class="wrap">',
        '<div class="mast"><div class="ttl"><h1>監視器狀態</h1>'
        f'<div class="date">{esc(date_str)} · 來源健康與每日用量</div></div>'
        '<div class="chips"><a class="chip" href="/intel/">回今日</a>'
        '<a class="chip" href="/intel/archive.html">歷史</a></div></div>',
        h2("當日摘要", "Summary"),
        f'<div class="stat-cards">{stat_html}</div>',
        h2("來源健康", "Sources"),
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
    ap.add_argument("--data", default=None,
                    help="（測試用）直接指定輸入 JSON，略過 docs/intel/data/ 解析")
    ap.add_argument("--out", default=None,
                    help="（測試用）輸出目錄，預設 docs/intel/；非預設時不注入站台 nav")
    args = ap.parse_args()
    date_str = args.date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"invalid --date: {date_str}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out).resolve() if args.out else DOCS_INTEL
    data_path = Path(args.data).resolve() if args.data else None
    out_dir.mkdir(parents=True, exist_ok=True)
    sources_meta = load_sources_yml()

    payload, banner, stale = resolve_day_payload(date_str, sources_meta, data_path)

    index_body = build_day_body(date_str, payload, banner, is_archive=False)
    index_html = (
        head(
            "全球金融市場監視器 — InvestMQuest Research",
            "全球金融市場監視器：儀表列、轉折警示、市場早報、市場／產業／個股卡片與接下來 7 天日曆，機械聚合＋LLM 摘要每日更新。",
            indexable=True,
        )
        + "\n<body data-mode=\"brief\">\n"
        + index_body
        + "\n</body>\n</html>\n"
    )
    index_path = out_dir / "index.html"
    index_path.write_text(index_html, encoding="utf-8")

    day_body = build_day_body(date_str, payload, banner, is_archive=True)
    day_html = (
        head(
            f"{date_str} — 全球金融市場監視器封存 — InvestMQuest Research",
            f"{date_str} 全球金融市場監視器封存頁。",
            indexable=False,
        )
        + "\n<body data-mode=\"brief\">\n"
        + day_body
        + "\n</body>\n</html>\n"
    )
    day_path = out_dir / f"{date_str}.html"
    day_path.write_text(day_html, encoding="utf-8")

    archive_html = (
        head("監視器封存 — InvestMQuest Research", "全球金融市場監視器歷史日期列表。", indexable=False)
        + "\n<body>\n"
        + render_archive(date_str, out_dir)
        + "\n</body>\n</html>\n"
    )
    archive_path = out_dir / "archive.html"
    archive_path.write_text(archive_html, encoding="utf-8")

    status_html = (
        head("監視器狀態 — InvestMQuest Research", "全球金融市場監視器來源健康與每日用量。", indexable=False)
        + "\n<body>\n"
        + render_status_page(date_str, payload, sources_meta)
        + "\n</body>\n</html>\n"
    )
    status_path = out_dir / "status.html"
    status_path.write_text(status_html, encoding="utf-8")

    if out_dir == DOCS_INTEL:
        inject_nav([index_path, day_path, archive_path, status_path])

    for p in (index_path, day_path, archive_path, status_path):
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
