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
THREADS_FILE = DATA_DIR / "threads.json"

# 2.0 Phase A：跨站台唯讀資料源（各自獨立 fail-safe，缺檔/缺欄位一律回 DASH，
# 不讓任一來源拖垮整頁）。見 notes/site-internal/intel/DESIGN.md 2026-08-20 節。
DOCS = ROOT / "docs"
MONITOR_SCORE_FILE = DOCS / "monitor" / "data" / "score_history.json"
DETECTIVE_LATEST_FILE = DOCS / "detective" / "data" / "latest.json"
DETECTIVE_STATE_FILE = DOCS / "detective" / "data" / "state.json"
KILL_WATCH_FILE = DOCS / "detective" / "data" / "kill_watch.json"
REGIME_LATEST_FILE = DOCS / "regime" / "data" / "latest.json"
MACRO_CLOCK_FILE = DOCS / "macro" / "data" / "clock.json"
RISK_GAUGE_FILE = DOCS / "cache" / "risk_gauge.json"
ROTATION_RADAR_FILE = DOCS / "rotation" / "data" / "radar.json"
CATALYST_CALENDAR_FILE = DOCS / "catalyst" / "calendar.json"
# Phase B（2026-08-20）：週更頁原生渲染直接讀的另外兩份週更資料源。
CROWDING_LATEST_FILE = DOCS / "crowding" / "data" / "latest.json"
ROTATION_LATEST_FILE = DOCS / "rotation" / "data" / "latest.json"
# Phase C（2026-08-20）：「現況」彙整層的落地檔——首頁「市場現況」磚 2/3/4 的
# 現值／色帶唯一事實源（docs/index.html 讀本檔；歷史走勢仍讀各歷史 JSON）。
STATUS_SNAPSHOT_FILE = DATA_DIR / "status_snapshot.json"
# Phase 2（2026-08-20）：產業／主題層新增的三個唯讀來源＋一個寫入落地檔。
THEMES_YML = INTEL_SCRIPTS_DIR / "themes.yml"
HOME_PULSE_FILE = DOCS / "home" / "pulse.json"
THEME_HISTORY_FILE = DATA_DIR / "theme_history.json"
THEME_WEEKLY_FILE = DATA_DIR / "theme_weekly.json"
THEME_HISTORY_RETENTION_DAYS = 14
THEME_WEEKLY_STALE_DAYS = 8

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


def load_json_safe(path: Path):
    """load_json 的 fail-safe 版本：任何例外（缺檔／壞 JSON／權限）一律回 None，
    呼叫端用 `or {}` 接手，不得讓任一跨站台資料源拖垮整頁渲染。"""
    try:
        return load_json(path)
    except Exception:
        return None


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


def load_themes_yml() -> list:
    """Phase 2（2026-08-20）：scripts/intel/themes.yml 的固定主題清單（見該檔
    頭註解的欄位定義）。render.py 自成一體不 import common.py（render.py 是
    純渲染器，故意不依賴 pipeline 端模組），故這裡另外自帶一份等價的 fail-safe
    loader，與 common.load_themes() 各自獨立但讀同一份 YAML。"""
    if not THEMES_YML.exists():
        return []
    try:
        data = yaml.safe_load(THEMES_YML.read_text(encoding="utf-8")) or []
    except Exception:
        return []
    return [t for t in data if isinstance(t, dict) and t.get("key")]


def _theme_by_key() -> dict:
    return {t["key"]: t for t in load_themes_yml()}


def assign_theme(card: dict, themes: list) -> str | None:
    """card.theme 有填（haiku 分類階段挑的）就直接用；沒有（舊 payload／haiku
    漏判）就退回關鍵字 fallback——比對 card 標題＋tags.themes（大小寫不分）
    是否含有該主題 keywords 任一字串，第一個命中的主題勝出（themes.yml 的
    順序即優先序）。找不到就回 None（歸「其他」）。"""
    theme = card.get("theme")
    if theme:
        return theme
    hay = (card.get("title") or "").lower()
    tags_themes = " ".join((card.get("tags") or {}).get("themes") or []).lower()
    hay = f"{hay} {tags_themes}"
    for t in themes:
        for kw in t.get("keywords") or []:
            if kw and kw.lower() in hay:
                return t["key"]
    return None


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


def render_site_read(site_read_zh) -> str:
    """B2（2026-08-20）：早報之後的「站內監測判讀」——digest 頂層選填欄位
    `site_read_zh`（只有 summarize.py 有 site_snapshot 素材時才會出現）。缺欄位
    /空字串一律回空字串，build_day_body 完全不渲染這段（向後相容舊 JSON）。
    跟 brief_zh 一樣是 LLM 產出，render 端仍跑一次 allow-list sanitize 當第二道防線。"""
    if not isinstance(site_read_zh, str) or not site_read_zh.strip():
        return ""
    body = sanitize_brief(site_read_zh)
    if not body.strip():
        return ""
    return (
        '<div class="box" style="margin-top:10px">'
        '<h3>站內監測判讀'
        '<span><a href="/intel/change.html" style="color:inherit;text-decoration:none">'
        "機械層數字→ 變化分頁</a></span></h3>"
        f'<p style="margin:8px 0 0;font-size:13px;line-height:1.7">{body}</p>'
        "</div>"
    )


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


def render_theme_grouped_list(cards: list, themes: list, empty_text: str, thread_map=None) -> str:
    """Task C5（2026-08-20）：今日頁「產業層」改按主題分組（取代原本的 category
    分組）——骨架完全比照 render_grouped_list，分組鍵改用 assign_theme()（haiku
    的 card.theme 優先，缺欄位退關鍵字 fallback，見上方定義）。無主題的卡片歸
    「其他」，且「其他」固定排最後一組（不管張數，避免雜項因為量大反而排到主題
    前面，喧賓奪主）。"""
    if not cards:
        return f'<div class="list">{LIST_HEAD}<div class="empty">{esc(empty_text)}</div></div>'
    theme_label = {t["key"]: t.get("name_zh") or t["key"] for t in themes}
    by_theme: dict = {}
    for c in cards:
        key = assign_theme(c, themes) or "other"
        by_theme.setdefault(key, []).append(c)
    seq = sorted((k for k in by_theme if k != "other"), key=lambda k: -len(by_theme[k]))
    if "other" in by_theme:
        seq.append("other")
    parts = [LIST_HEAD]
    for key in seq:
        items = sorted(by_theme[key], key=card_sort_key)
        label = theme_label.get(key, "其他")
        parts.append(group_header(label, len(items)))
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


def _thread_sort_key(t: dict):
    """排序＝升溫→持平→降溫，同組內依今日新增數 desc、再依天數 desc。抽成
    module-level 函式讓 index 頁「前 5 條預覽」與 render_threads() 本身共用同一
    順序定義，不會兩處各自維護一份排序邏輯而漂移。"""
    heat = t.get("heat") if t.get("heat") in HEAT_ARROW else "flat"
    return (
        HEAT_SORT_RANK.get(heat, 1),
        -(t.get("today_count") or 0),
        -(t.get("day_n") or 0),
    )


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


def render_threads(threads: list, detail_limit: int | None = 3) -> str:
    """進行中的故事線：一行一條清單（`<details>`/`<summary>`，無 JS）——
    熱度 pill／主題／第 N 天／今日 +n／（有 total_count 時）共 T 張／14 天
    sparkline／最新一則標題（單行截斷）的緊湊列；點列展開最新則（連原文／
    來源短名／日期）。排序＝升溫→持平→降溫，同組內依今日新增數 desc、再依
    天數 desc；升溫前 3 條預設展開。空陣列由呼叫端負責整段（含 h2）省略。

    detail_limit：展開內容顯示的則數上限；index 頁前 5 條預覽維持 3 則
    （保持頁面不加長），threads.html 完整清單傳 None 顯示全部
    card_ids_latest（規格：「expanded shows all card_ids_latest」）。"""
    if not threads:
        return ""

    ordered = sorted(threads, key=_thread_sort_key)
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

        total_count = t.get("total_count")
        total_cell = (
            f'<span class="tht">共 {esc(fmt_num(int(total_count)))} 張</span>'
            if isinstance(total_count, (int, float)) else ""
        )

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

        # 展開內容：最新則（連原文／來源短名／日期）——detail_limit=None 顯示全部
        detail_items = []
        detail_source = latest if detail_limit is None else latest[:detail_limit]
        for e in detail_source:
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
            f'{total_cell}'
            f'<span class="thsp">{spark}</span>'
            f'<span class="thlast">{latest_cell}</span>'
            f'<span class="chev"></span>'
            f"</summary>"
            f'<div class="thr-body">{detail_html}</div>'
            f"</details>"
        )
    return '<div class="threads">' + "\n".join(rows_html) + "</div>"


def compute_full_threads(date_str: str) -> list:
    """故事線分頁（threads.html）用：讀 threads.json 全部條目（不受單日 JSON 挑選
    名額限制），依規格公式機械算出 today_count／prev／heat／day_n／total／
    sparkline，補齊 render_threads() 需要的欄位。任何單一條目算壞不擋其餘條目。"""
    data = load_json_safe(THREADS_FILE) or {}
    threads = data.get("threads") or []
    try:
        td = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        td = None

    out = []
    for t in threads:
        try:
            dc = t.get("daily_counts") or {}
            today_count = dc.get(date_str, 0) or 0
            prior_days = sorted(d for d in dc if d < date_str)
            prev = dc.get(prior_days[-1], 0) if prior_days else 0
            last_seen = t.get("last_seen") or ""
            if last_seen and last_seen < date_str:
                heat = "down"
            elif today_count > prev:
                heat = "up"
            elif today_count < prev:
                heat = "down"
            else:
                heat = "flat"
            total = sum(v for v in dc.values() if isinstance(v, (int, float)))
            day_n = 1
            first_seen = t.get("first_seen")
            if td and first_seen:
                try:
                    fd = datetime.strptime(first_seen, "%Y-%m-%d").date()
                    day_n = max((td - fd).days + 1, 1)
                except ValueError:
                    day_n = 1
            sparkline = []
            if td:
                for i in range(13, -1, -1):
                    ds = (td - timedelta(days=i)).isoformat()
                    sparkline.append(dc.get(ds, 0) or 0)
            tt = dict(t)
            tt.update(
                today_count=today_count, heat=heat, day_n=day_n,
                total_count=total, latest=t.get("card_ids_latest") or [],
                sparkline=sparkline,
            )
            out.append(tt)
        except Exception:
            continue
    return out


# ------------------------------------------------------- 今日重點（Task A）

def _thread_heat_bonus(card: dict, threads_by_id: dict, threads: list) -> int:
    """打分公式第四項：所屬故事線熱度加分。優先用 card.thread_id 直接查
    （threads_output 裡有的卡片本來就已被指派 thread_id）；沒有 thread_id
    的卡片退回關鍵字比對（標題是否含有某條故事線的任一 keyword）。up=+5／
    flat=+2／down or 無匹配=0——升溫故事線的卡片更值得放進今日重點。"""
    tid = card.get("thread_id")
    heat = None
    if tid and tid in threads_by_id:
        heat = threads_by_id[tid].get("heat")
    else:
        title_l = (card.get("title") or "").lower()
        for t in threads:
            for kw in t.get("keywords") or []:
                if kw and kw.lower() in title_l:
                    heat = t.get("heat")
                    break
            if heat:
                break
    return {"up": 5, "flat": 2}.get(heat, 0)


def _news_highlight_score(card: dict, threads_by_id: dict, threads: list) -> float:
    """今日重點新聞卡池打分公式（Task A，DESIGN.md Phase 2 節記載）：
    importance×10 ＋ corroboration×3 ＋（T1 來源 +2）＋ 故事線熱度加分。"""
    score = int(card.get("importance") or 1) * 10
    score += int(card.get("corroboration") or 1) * 3
    if card.get("source_tier") == "T1":
        score += 2
    score += _thread_heat_bonus(card, threads_by_id, threads)
    return score


def _site_event_items(payload: dict) -> list:
    """站內事件池（排在新聞前面）：detective 新觸發紅色警示（band 換檔的機械
    代理——detective 本身不存 band 逐日歷史，state=="new" 且 sev=="red" 的
    訊號是最貼近「今天新出現的警示」的既有訊號）、kill 指標 breached／near
    （沿用 payload.flags，不重寫文字）、home/pulse.json 轉折確認（evidence
    含「持穩」字樣＝confirmed，此判定字串沿用 scripts/build_home_pulse.py
    內部既有用法，不是本次新發明的判斷邏輯）。任一來源缺檔／壞檔各自
    fail-safe 跳過，不影響其他兩種。"""
    items = []

    det = load_json_safe(DETECTIVE_LATEST_FILE) or {}
    for s in (det.get("signals") or []):
        if s.get("state") == "new" and s.get("sev") == "red":
            label = (s.get("label") or "").strip()
            fact = (s.get("fact") or "").strip()
            summary = f"{label}：{fact}" if label and fact else (fact or label)
            if not summary:
                continue
            items.append({
                "summary": summary,
                "why": "今日新觸發之紅色警示訊號（機械監測分類，非擇時判斷）。",
                "source": "站內偵探",
                "url": "/detective/",
            })

    near_pool = []
    for fl in (payload.get("flags") or []):
        level = (fl.get("level") or "").lower()
        if level not in ("confirmed", "near"):
            continue
        text_zh = (fl.get("text_zh") or "").strip()
        if not text_zh:
            continue
        item = {
            "summary": text_zh,
            "why": "已觸發設定門檻。" if level == "confirmed" else "接近設定門檻，尚未觸發。",
            "source": "站內 kill-watch",
            "url": fl.get("link") or "/detective/",
        }
        if level == "confirmed":
            items.append(item)
        else:
            # near＝長期不變的狀態，非今日事件——整池只留距離門檻最近的 1 條，
            # 避免同一批 near 旗標天天霸佔「今日重點」擠掉新聞（2026-08-20 驗收修正）。
            near_pool.append((fl.get("distance_pct") if isinstance(fl.get("distance_pct"), (int, float)) else 999.0, item))

    pulse = load_json_safe(HOME_PULSE_FILE) or {}
    for rf in (pulse.get("reversal_flags") or []):
        evidence = (rf.get("evidence") or "").strip()
        if "持穩" not in evidence:
            continue
        axis = (rf.get("axis") or "").strip()
        frm, to = rf.get("from"), rf.get("to")
        summary = f"{axis}：{frm} → {to}" if axis and frm and to else (evidence or axis)
        if not summary:
            continue
        items.append({
            "summary": summary,
            "why": evidence or "轉折訊號已連續確認。",
            "source": "站內轉折雷達",
            "url": "/",
        })

    if near_pool:
        near_pool.sort(key=lambda t: t[0])
        items.append(near_pool[0][1])

    return items


def compute_today_highlights(payload: dict, n: int = 5) -> list:
    """Task A（2026-08-20）：今日重點，純機械打分，零新增 LLM 呼叫。回傳
    ≤n 條 {summary, why, source, url} dict——站內事件池優先（detective 新警示／
    kill 指標／轉折確認），剩餘名額由新聞卡池依打分公式（見
    `_news_highlight_score`）填滿，同 category 最多 2 條保多樣性。整段包在
    try/except：任何一步壞掉都回 []，呼叫端據此完全省略這個區塊，不擋頁面。"""
    try:
        # 站內事件最多佔 2 席（真變化優先），其餘留給新聞卡——
        # 否則 kill-watch near 這類長期狀態會天天填滿五條（2026-08-20 驗收修正）。
        site_items = _site_event_items(payload)[:min(2, n)]
        remaining = max(n - len(site_items), 0)
        news_items = []
        if remaining:
            threads = payload.get("threads") or []
            threads_by_id = {t.get("id"): t for t in threads if t.get("id")}
            cards = payload.get("cards") or []
            pool = [
                c for c in cards
                if not is_rumor(c) and not is_title_only(c) and (c.get("summary_zh") or "").strip()
            ]
            scored = sorted(pool, key=lambda c: -_news_highlight_score(c, threads_by_id, threads))
            per_cat: dict = {}
            for c in scored:
                if len(news_items) >= remaining:
                    break
                cat = c.get("category") or ""
                if per_cat.get(cat, 0) >= 2:
                    continue
                per_cat[cat] = per_cat.get(cat, 0) + 1
                news_items.append({
                    "summary": c.get("summary_zh") or _card_title(c),
                    "why": c.get("why_zh") or "",
                    "source": source_short(c),
                    "url": c.get("url") or "",
                })
        return (site_items + news_items)[:n]
    except Exception:
        return []


def render_highlights(items: list) -> str:
    """今日重點清單——沿用 `.focus`（render_focus 同一套 CSS，見
    templates/intel.css `.focus`），每條：summary（連結）＋ why（一句）＋
    來源短名。描述器紀律：summary/why 全部沿用既有欄位文字，這裡不生成任何
    新的判斷句。"""
    if not items:
        return ""
    lis = []
    for it in items:
        summary = esc(it.get("summary") or "")
        if not summary:
            continue
        why = esc(it.get("why") or "")
        src = esc(it.get("source") or "")
        url = it.get("url") or ""
        head_html = (
            f'<a href="{esc(url)}" rel="noopener nofollow">{summary}</a>'
            if url and _safe_href(url) else f'<span class="h">{summary}</span>'
        )
        mt_bits = [m for m in (why, src) if m]
        mt_html = "".join(f"<span>{m}</span>" for m in mt_bits)
        lis.append(
            f'<li><span class="imp i2" aria-hidden="true"></span>'
            f'<span class="tx">{head_html}<span class="mt">{mt_html}</span></span></li>'
        )
    if not lis:
        return ""
    return '<ul class="focus">' + "\n".join(lis) + "</ul>"


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


# ------------------------------------------------------------- 2.0 分頁殼

TABS = [
    ("index.html", "今日", None),
    ("change.html", "變化", "change_n"),
    ("gauges.html", "儀表", None),
    ("weekly.html", "週更", None),
    ("themes.html", "產業", "theme_n"),
    ("calendar.html", "行事曆", "cal_n"),
    ("threads.html", "故事線", None),
    ("archive.html", "封存", None),
    ("status.html", "狀態", None),
]


def render_tabstrip(active: str, badges: dict = None) -> str:
    badges = badges or {}
    items = []
    for href, label, badge_key in TABS:
        cls = "tab on" if href == active else "tab"
        n = badges.get(badge_key) if badge_key else None
        n_html = f'<span class="n">{esc(fmt_num(n))}</span>' if n not in (None, "") else ""
        items.append(f'<a class="{cls}" href="/intel/{href}">{esc(label)}{n_html}</a>')
    return '<nav class="tabstrip" aria-label="情報監視器分頁">' + "".join(items) + "</nav>"


def compute_tab_badges(date_str: str, calendar: list, det: dict) -> dict:
    """分頁小數字：變化＝訊號數、行事曆＝未來 14 天事件數（intel calendar ∪
    catalyst events）。任何一步失敗都回 None（render_tabstrip 略過不顯示）。"""
    badges = {}
    try:
        badges["change_n"] = len((det or {}).get("signals") or [])
    except Exception:
        badges["change_n"] = None
    try:
        base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        days = {(base_date + timedelta(days=i)).isoformat() for i in range(14)}
        cat = load_json_safe(CATALYST_CALENDAR_FILE) or {}
        n = sum(1 for e in (calendar or []) if e.get("date") in days)
        n += sum(1 for e in (cat.get("events") or []) if e.get("date") in days)
        badges["cal_n"] = n
    except Exception:
        badges["cal_n"] = None
    return badges


def _util_chips() -> str:
    return (
        '<div class="chips"><a class="chip" href="/intel/">回今日</a>'
        '<a class="chip" href="/intel/archive.html">歷史</a>'
        '<a class="chip" href="/intel/status.html">狀態</a></div>'
    )


# --------------------------------------------------------- 1 現況（狀態列）

def _band_key_for_score(score, bands) -> str:
    """Phase C：回傳帶位的原始 key（calm/normal/…），首頁四磚靠它對色票；
    無法判定回空字串。"""
    try:
        s = float(score)
    except (TypeError, ValueError):
        return ""
    for k, rng in (bands or {}).items():
        try:
            a, b = rng
            if a <= s < b:
                return k
        except (TypeError, ValueError):
            continue
    return ""


def _band_zh_for_score(score, bands) -> str:
    bz = {"calm": "平靜", "normal": "正常", "warming": "升溫", "tense": "緊張", "extreme": "極端"}
    k = _band_key_for_score(score, bands)
    return bz.get(k, k)


def load_status_snapshot() -> dict:
    """「現況」六格的原始數字：讀 6 個跨站台 JSON，各自獨立 fail-safe。
    `_detective` 鍵把完整 detective payload 一併帶出，供「變化」預覽段複用，
    避免同一份 JSON 讀兩次。"""
    out = {}

    sh = load_json_safe(MONITOR_SCORE_FILE) or {}
    series = sh.get("series") or []
    last = series[-1] if series else {}
    score = last.get("s")
    out["stress_score"] = fmt_num(score) or DASH
    out["stress_band"] = _band_zh_for_score(score, sh.get("bands"))
    out["stress_band_key"] = _band_key_for_score(score, sh.get("bands"))
    out["stress_int"] = fmt_num(last.get("int_s"))
    out["stress_date"] = last.get("d") or ""

    det = load_json_safe(DETECTIVE_LATEST_FILE) or {}
    al = det.get("alert_level") or {}
    counts = det.get("counts") or {}
    out["alert_score"] = fmt_num(al.get("score")) or DASH
    out["alert_band"] = al.get("band_label") or ""
    out["alert_band_key"] = al.get("band") or ""
    out["alert_date"] = al.get("as_of") or ""
    out["alert_red"] = counts.get("red")
    out["alert_yellow"] = counts.get("yellow")
    out["alert_escalated"] = counts.get("escalated")
    out["_detective"] = det

    reg = load_json_safe(REGIME_LATEST_FILE) or {}
    out["regime_label"] = (reg.get("composite") or {}).get("label_zh") or DASH

    clock = load_json_safe(MACRO_CLOCK_FILE) or {}
    out["clock_quadrant"] = clock.get("quadrant") or DASH

    rg = load_json_safe(RISK_GAUGE_FILE) or {}
    try:
        rg_label = rg.get("label_zh")
        rg_score = rg.get("score")
        out["risk_gauge"] = (
            f"{rg_label} {float(rg_score):.2f}" if (rg_label and rg_score is not None) else DASH
        )
    except (TypeError, ValueError):
        out["risk_gauge"] = DASH
    # Phase C：另存原始欄位（label／score／date 分離），首頁磚 2 直接用，
    # 不必回頭解析上面的組合字串。
    out["risk_gauge_label"] = rg.get("label_zh") or ""
    try:
        out["risk_gauge_score"] = (
            round(float(rg.get("score")), 4) if rg.get("score") is not None else None
        )
    except (TypeError, ValueError):
        out["risk_gauge_score"] = None
    out["risk_gauge_date"] = rg.get("as_of") or ""

    radar = load_json_safe(ROTATION_RADAR_FILE) or {}
    ca = next(
        (u for u in (radar.get("universes") or []) if u.get("key") == "cross_asset"), None
    )
    scored = []
    for m in (ca or {}).get("members") or []:
        exc = ((m.get("frames") or {}).get("120") or {}).get("exc")
        if exc is None:
            continue
        try:
            scored.append((m.get("label") or "", float(exc)))
        except (TypeError, ValueError):
            continue
    scored.sort(key=lambda x: -x[1])
    out["radar_top3"] = "／".join(
        f"{lbl} {'+' if v >= 0 else ''}{fmt_num(v)}" for lbl, v in scored[:3]
    ) or DASH

    kw = load_json_safe(KILL_WATCH_FILE) or {}
    out["kill_near"] = len(kw.get("near") or [])
    out["kill_breached"] = len(kw.get("breached") or [])
    out["_kill_watch"] = kw

    return out


def write_status_snapshot(snap: dict) -> None:
    """Phase C（2026-08-20）：把「現況」彙整層序列化成 status_snapshot.json，
    供首頁「市場現況」磚 2/3/4 讀取現值／色帶（單一計算來源，取代首頁自行
    重算同一批跨站台 JSON）。`_` 開頭私有鍵（完整 detective／kill watch
    payload）不落地。zero-churn：內容不變不重寫（build_home_pulse.py 同慣例）；
    刻意不含 generated_at，新鮮度由 stress_date／alert_date 等來源日期表達。
    除 render.py 每日鏈外，scripts/build_home_pulse.py 也會呼叫本函式，
    讓 monitor-daily／daily-us-close 等下午刷新鏈同步更新快照。"""
    import json

    pub = {k: v for k, v in snap.items() if not k.startswith("_")}
    pub["schema"] = "intel-status-snapshot-v1"
    content = json.dumps(pub, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    try:
        if STATUS_SNAPSHOT_FILE.read_text(encoding="utf-8") == content:
            return
    except OSError:
        pass
    STATUS_SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_SNAPSHOT_FILE.write_text(content, encoding="utf-8")


def render_status_strip(snap: dict) -> str:
    stress_sub = " · ".join(x for x in (
        snap.get("stress_band") or "",
        (f"內部 {snap['stress_int']}" if snap.get("stress_int") not in (None, "") else ""),
        snap.get("stress_date") or "",
    ) if x) or DASH

    alert_bits = []
    if snap.get("alert_band"):
        alert_bits.append(snap["alert_band"])
    if snap.get("alert_red") is not None:
        alert_bits.append(f"{snap['alert_red']} 紅 {snap.get('alert_yellow') or 0} 黃")
    if snap.get("alert_escalated") is not None:
        alert_bits.append(f"升級 {snap['alert_escalated']}")
    alert_sub = " · ".join(alert_bits) or DASH

    tiles = [
        '<div class="ss-tile"><div class="ss-lab">跨資產壓力（monitor）</div>'
        f'<div class="ss-val">{esc(snap.get("stress_score") or DASH)}</div>'
        f'<div class="ss-sub">{esc(stress_sub)}</div>'
        '<a class="ss-link" href="/intel/gauges.html">儀表 →</a></div>',

        '<div class="ss-tile"><div class="ss-lab">警戒度（detective）</div>'
        f'<div class="ss-val">{esc(snap.get("alert_score") or DASH)}</div>'
        f'<div class="ss-sub">{esc(alert_sub)}</div>'
        '<a class="ss-link" href="/intel/change.html">變化 →</a></div>',

        '<div class="ss-tile"><div class="ss-lab">Regime（週更）</div>'
        f'<div class="ss-val ss-val-s">{esc(snap.get("regime_label") or DASH)}</div>'
        '<a class="ss-link" href="/intel/weekly.html">週更 →</a></div>',

        '<div class="ss-tile"><div class="ss-lab">宏觀時鐘 · 風險偏好</div>'
        f'<div class="ss-val ss-val-s">{esc(snap.get("clock_quadrant") or DASH)}</div>'
        f'<div class="ss-sub">{esc(snap.get("risk_gauge") or DASH)}</div>'
        '<div class="ss-note">市場風險儀表保留在首頁</div></div>',

        '<div class="ss-tile"><div class="ss-lab">輪動雷達 cross-asset 120d</div>'
        f'<div class="ss-val ss-val-s">領先：{esc(snap.get("radar_top3") or DASH)}</div>'
        '<a class="ss-link" href="/rotation/radar.html#cross_asset/120" '
        'target="_blank" rel="noopener nofollow">開雷達 ↗</a></div>',

        '<div class="ss-tile"><div class="ss-lab">證偽表（kill watch）</div>'
        f'<div class="ss-val">{esc(fmt_num(snap.get("kill_near")) or "0")}</div>'
        f'<div class="ss-sub">接近 · {esc(fmt_num(snap.get("kill_breached")) or "0")} 突破</div>'
        '<a class="ss-link" href="/intel/change.html">對帳表 →</a></div>',
    ]
    return '<div class="ss-strip">' + "".join(tiles) + "</div>"


# --------------------------------------------------------- 2 變化（訊號表）

_SIG_STATE_LABEL = {
    "new": "新", "active": "活躍", "escalated": "升級",
    "cooling": "冷卻", "resolved": "解除", "cleared": "解除",
}
_SIG_SEV_LABEL = {"red": "紅", "yellow": "黃"}
SIGNAL_HEAD = (
    "<thead><tr><th>等級</th><th>訊號</th><th>來源層</th>"
    "<th>首見</th><th>持續</th><th>狀態</th></tr></thead>"
)


def _signal_sort_rank(sig: dict) -> float:
    sev = (sig.get("sev") or "").lower()
    state = (sig.get("state") or "").lower()
    r = 0.0 if sev == "red" else 1.0
    r += 0.0 if state in ("escalated", "new") else 0.5
    r += 1.0 if state == "cooling" else 0.0
    return r


def sorted_signals(signals: list) -> list:
    """紅在前、新/升級在前、冷卻最後，同層再依 days_active 降冪。"""
    return sorted(signals, key=lambda s: (_signal_sort_rank(s), -(s.get("days_active") or 0)))


def _signal_row(sig: dict) -> str:
    sev = (sig.get("sev") or "").lower()
    sev_cls = "pill sred" if sev == "red" else "pill samber" if sev == "yellow" else "pill"
    sev_label = _SIG_SEV_LABEL.get(sev, sev or DASH)
    state = (sig.get("state") or "").lower()
    state_label = _SIG_STATE_LABEL.get(state, state or DASH)
    label = esc(sig.get("label") or "")
    fact = esc(sig.get("fact") or sig.get("context") or "")
    fact_html = f' <span class="mut">· {fact}</span>' if fact else ""
    src = esc(sig.get("source") or "") or DASH
    first_seen = (sig.get("first_seen") or "")[5:] or DASH
    days = sig.get("days_active")
    days_s = f"{days} 天" if days is not None else DASH
    return (
        "<tr>"
        f'<td><span class="{sev_cls}">{esc(sev_label)}</span></td>'
        f"<td>{label}{fact_html}</td>"
        f'<td class="mono">{src}</td>'
        f'<td class="mono">{esc(first_seen)}</td>'
        f'<td class="mono">{esc(days_s)}</td>'
        f'<td><span class="pill">{esc(state_label)}</span></td>'
        "</tr>"
    )


def render_signal_table(signals: list) -> str:
    if not signals:
        return '<div class="empty">目前無訊號資料。</div>'
    rows = "".join(_signal_row(s) for s in signals)
    return f'<div class="twrap"><table class="t sigtbl">{SIGNAL_HEAD}<tbody>{rows}</tbody></table></div>'


def render_change_preview(det: dict, transitions_today: int) -> str:
    signals = det.get("signals") or []
    ordered = sorted_signals(signals)
    non_cooling = [s for s in ordered if (s.get("state") or "").lower() != "cooling"]
    top8 = non_cooling[:8]
    rest_n = max(len(ordered) - len(top8), 0)
    parts = [render_signal_table(top8)]
    if signals:
        parts.append(
            f'<p class="note">…其餘 {rest_n} 條（含冷卻中）收在「變化」分頁。'
            f"今日狀態轉移：{transitions_today} 筆。"
            ' <a href="/intel/change.html">看全部 →</a></p>'
        )
    return "".join(parts)


def _pct(v) -> str:
    try:
        return f"{float(v) * 100:.0f}%"
    except (TypeError, ValueError):
        return DASH


_KILL_STATUS_LABEL = {"near": "接近", "breached": "突破"}


def render_kill_table(kw: dict) -> str:
    items_by_id = {i.get("id"): i for i in (kw.get("items") or []) if i.get("id")}
    rows = []
    for status, ids in (("breached", kw.get("breached") or []), ("near", kw.get("near") or [])):
        for iid in ids:
            it = items_by_id.get(iid)
            if not it:
                continue
            doc = it.get("doc") or ""
            doc_href = "/" + doc[len("docs/"):] if doc.startswith("docs/") else doc
            link_html = (
                f'<a href="{esc(doc_href)}" rel="noopener nofollow">報告 ↗</a>' if doc_href else DASH
            )
            value = it.get("value")
            unit = it.get("unit") or ""
            threshold_s = (
                f'{esc(fmt_num(value))} <span class="mut">{esc(unit)}</span>'
                if value not in (None, "") else DASH
            )
            rows.append(
                "<tr>"
                f'<td><span class="pill {esc(status)}">{_KILL_STATUS_LABEL.get(status, status)}</span></td>'
                f'<td>{esc(it.get("theme") or "")}</td>'
                f'<td>{esc(it.get("metric_text") or "")}</td>'
                f'<td class="num">{esc(fmt_num(it.get("current"))) or DASH}</td>'
                f'<td class="num">{threshold_s}</td>'
                f"<td>{link_html}</td>"
                "</tr>"
            )
    if not rows:
        return '<div class="empty">目前無接近或突破的證偽指標。</div>'
    head = (
        "<thead><tr><th>狀態</th><th>主題</th><th>指標</th>"
        "<th>現值</th><th>門檻</th><th>報告</th></tr></thead>"
    )
    return f'<div class="twrap"><table class="t killtbl">{head}<tbody>{"".join(rows)}</tbody></table></div>'


def render_composite_table(composites: list) -> str:
    if not composites:
        return '<div class="empty">今日無複合規則資料。</div>'
    rows = []
    for c in composites:
        narrative = (c.get("narrative") or "")[:60]
        fired = c.get("fired")
        fired_html = '<span class="pill sred">觸發</span>' if fired else '<span class="pill">未觸發</span>'
        rows.append(
            "<tr>"
            f'<td class="mono">{esc(c.get("id") or "")}</td>'
            f'<td>{esc(c.get("name") or "")} <span class="mut">· {esc(narrative)}'
            f'{"…" if narrative else ""}</span></td>'
            f'<td class="num">{esc(fmt_num(c.get("met_count")))}/{esc(fmt_num(c.get("min_true")))}</td>'
            f'<td class="num">{esc(_pct(c.get("proximity")))}</td>'
            f"<td>{fired_html}</td>"
            "</tr>"
        )
    head = (
        "<thead><tr><th>規則</th><th>名稱</th><th>成員達標</th>"
        "<th>接近度</th><th>狀態</th></tr></thead>"
    )
    return f'<div class="twrap"><table class="t compositetbl">{head}<tbody>{"".join(rows)}</tbody></table></div>'


def h2(zh: str, en: str, count=None) -> str:
    cnt = f'<span class="cnt">{count}</span>' if count is not None else ""
    return f'<h2>{esc(zh)}<span class="en">{esc(en)}</span>{cnt}</h2>'


def build_day_body(date_str: str, payload: dict, mode_note: str, is_archive: bool,
                    badges: dict = None) -> str:
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
    p.append(render_tabstrip("archive.html" if is_archive else "index.html", badges))

    if mode_note:
        p.append(mode_note)

    # 1／2. 現況＋變化（只在「今日」頁顯示；封存頁是歷史快照，不該疊上「現在」的
    # 即時跨站台數字，避免誤讀成那一天的現況）。
    if not is_archive:
        highlights = compute_today_highlights(payload)
        if highlights:
            p.append(h2("今日重點", "Highlights", len(highlights)))
            p.append(render_highlights(highlights))

        snap = load_status_snapshot()
        p.append(h2("現況", "Status"))
        p.append(render_status_strip(snap))
        det = snap.get("_detective") or {}
        state = load_json_safe(DETECTIVE_STATE_FILE) or {}
        transitions_n = len(state.get("transitions_today") or [])
        p.append(h2("變化", "Change"))
        p.append(render_change_preview(det, transitions_n))

    # 2. 儀表列
    p.append(h2("儀表列", "Gauges", len(gauges) or None))
    p.append(render_gauges(gauges))

    # 3. 轉折警示
    p.append(h2("轉折警示", "Alerts", len(flags) or None))
    p.append(render_flags(flags))

    # 3.5 進行中的故事線（空陣列整段省略，含標題）——2026-08-20：頁面不加長，
    # 只留前 5 條一行式＋「看全部故事線 →」連 threads.html（完整清單）。
    if threads:
        p.append(h2("進行中的故事線", "Threads", len(threads)))
        top5 = sorted(threads, key=_thread_sort_key)[:5]
        p.append(render_threads(top5))
        if len(threads) > 5:
            p.append(
                f'<p class="note"><a href="/intel/threads.html">'
                f"看全部故事線 →（共 {len(threads)} 條）</a></p>"
            )

    # 4. 市場早報（雙欄）
    p.append('<section class="only-brief">')
    p.append(h2("市場早報", "Brief"))
    p.append('<div class="sheet"><div class="main">')
    p.append(render_brief(brief_zh))
    p.append(render_site_read(payload.get("site_read_zh")))
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
    p.append(render_theme_grouped_list(industry_cards, load_themes_yml(), "今日無產業層卡片。", thread_map))

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


# ---------------------------------------------------------- 2.0 其餘分頁

def build_change_body(date_str: str, det: dict, state: dict, kw: dict, badges: dict) -> str:
    al = det.get("alert_level") or {}
    drivers = al.get("drivers") or []
    drv_text = "　".join(
        f"{esc(d.get('label') or '')} +{esc(fmt_num(d.get('points')))}" for d in drivers
    ) or DASH

    p = ['<div class="wrap">']
    p.append(
        '<div class="mast"><div class="ttl"><h1>變化</h1>'
        f'<div class="date">{esc(date_str)}　今日訊號、生命週期、證偽對帳、複合規則</div></div>'
        + _util_chips() + "</div>"
    )
    p.append(render_tabstrip("change.html", badges))

    p.append(h2("警戒度", "Alert level"))
    p.append(
        '<p class="note" style="font-size:13.5px;color:var(--ink2);max-width:none">'
        f'警戒度 <b style="color:var(--ink);font-size:15px">{esc(fmt_num(al.get("score")) or DASH)}</b>'
        f'（{esc(al.get("band_label") or DASH)}）'
        f"　計分來源：{drv_text}</p>"
    )

    signals = sorted_signals(det.get("signals") or [])
    p.append(h2("全部訊號", "Signals", len(signals) or None))
    p.append(render_signal_table(signals))

    p.append(h2("證偽對帳表", "Kill watch"))
    p.append(render_kill_table(kw))

    p.append(h2("複合規則靶盤", "Composites"))
    p.append(render_composite_table(det.get("composites") or []))

    p.append("</div>")
    p.append(FOOT)
    return "\n".join(p)


def build_gauges_body(badges: dict) -> str:
    p = ['<div class="wrap">']
    p.append(
        '<div class="mast"><div class="ttl"><h1>儀表</h1>'
        '<div class="date">機械層 96 條序列，來自 /monitor/</div></div>'
        + _util_chips() + "</div>"
    )
    p.append(render_tabstrip("gauges.html", badges))
    p.append('<iframe class="fullframe" src="/monitor/" title="市場監測" loading="lazy"></iframe>')
    p.append("</div>")
    p.append(FOOT)
    return "\n".join(p)


# ---------------------------------------------- 週更原生渲染（Phase B，2026-08-20）
# 舊版三個 iframe 嵌 /crowding/ /regime/ /rotation/ 全部拆掉，改成 Python 端直接
# 讀三份週更 JSON 渲染真數字（沿用既有 intel.css：.box/.twrap table.t/.stat-cards/
# .note），底部留一排連到完整互動頁的小連結。任一來源缺檔/壞檔只讓該區塊顯示
# 「尚無資料」，不擋其他兩塊或整頁（同站台一貫的 fail-safe 慣例）。

_STALE_DAYS = 10


def _as_of_date(s) -> "datetime.date | None":
    if not s:
        return None
    try:
        return datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _stale_note(as_of) -> str:
    """as_of 超過 _STALE_DAYS 天時回「（資料 N 天前）」，否則空字串。"""
    d = _as_of_date(as_of)
    if d is None:
        return ""
    days = (datetime.now(timezone.utc).date() - d).days
    return f"（資料 {days} 天前）" if days > _STALE_DAYS else ""


def _weekly_section_head(zh: str, en: str, as_of) -> str:
    stale = _stale_note(as_of)
    as_of_s = esc(as_of) if as_of else DASH
    stale_html = f" <span>{esc(stale)}</span>" if stale else ""
    return h2(zh, en) + f'<p class="note">as_of {as_of_s}{stale_html}</p>'


def render_weekly_crowding() -> str:
    d = load_json_safe(CROWDING_LATEST_FILE) or {}
    if not d:
        return (
            _weekly_section_head("擁擠交易", "Crowding", None)
            + '<div class="empty">今日尚無資料，見 <a href="/crowding/">/crowding/</a>。</div>'
        )
    as_of = d.get("cot_as_of") or (d.get("generated_at") or "")[:10]
    parts = [_weekly_section_head("擁擠交易", "Crowding", as_of)]

    themes = [t for t in (d.get("themes") or []) if t.get("rank") is not None]
    themes = sorted(themes, key=lambda t: t["rank"])[:10]
    if themes:
        rows = "".join(
            "<tr>"
            f'<td>{esc(t.get("name")) or DASH}</td>'
            f'<td class="num">{esc(fmt_num(t.get("score"))) or DASH}</td>'
            f'<td class="num">{esc(fmt_num(t.get("rank"))) or DASH}</td>'
            "</tr>"
            for t in themes
        )
        parts.append(
            '<div class="twrap"><table class="t"><thead><tr>'
            "<th>主題</th><th>擁擠分數</th><th>排名</th>"
            "</tr></thead><tbody>" + rows + "</tbody></table></div>"
        )
    else:
        parts.append('<div class="empty">今日無主題擁擠資料。</div>')

    def _cot_extreme_key(c):
        try:
            return -abs(float(c.get("pctile_5y")) - 50.0)
        except (TypeError, ValueError):
            return 0.0

    cot_top = sorted(
        (c for c in (d.get("cot") or []) if c.get("pctile_5y") is not None),
        key=_cot_extreme_key,
    )[:8]
    if cot_top:
        rows = "".join(
            "<tr>"
            f'<td>{esc(c.get("market")) or DASH}</td>'
            f'<td>{esc(c.get("direction")) or DASH}</td>'
            f'<td class="num">{esc(fmt_num(c.get("pctile_5y"))) or DASH}</td>'
            "</tr>"
            for c in cot_top
        )
        parts.append(
            '<div class="twrap" style="margin-top:8px"><table class="t"><thead><tr>'
            "<th>市場</th><th>方向</th><th>5 年分位</th>"
            "</tr></thead><tbody>" + rows + "</tbody></table></div>"
        )
    else:
        parts.append('<div class="empty">今日無 COT 極端值資料。</div>')

    parts.append(
        '<p class="note">來源：/crowding/ 每週日更新 · '
        '<a href="/crowding/">完整互動頁 →</a></p>'
    )
    return "".join(parts)


def render_weekly_regime() -> str:
    d = load_json_safe(REGIME_LATEST_FILE) or {}
    if not d:
        return (
            _weekly_section_head("Regime", "Regime", None)
            + '<div class="empty">今日尚無資料，見 <a href="/regime/">/regime/</a>。</div>'
        )
    meta = d.get("meta") or {}
    as_of = meta.get("publish_date") or (d.get("generated_at") or "")[:10]
    parts = [_weekly_section_head("Regime", "Regime", as_of)]

    comp = d.get("composite") or {}
    label_zh = comp.get("label_zh") or DASH
    label_en = comp.get("label_en") or ""
    parts.append(
        '<div style="margin:2px 0 10px">'
        f'<div style="font-size:19px;font-weight:700;color:var(--ink)">{esc(label_zh)}</div>'
        + (f'<div class="note" style="margin-top:2px">{esc(label_en)}</div>' if label_en else "")
        + "</div>"
    )

    axes = d.get("axes") or []
    if axes:
        rows = "".join(
            "<tr>"
            f'<td>{esc(a.get("name")) or DASH}</td>'
            f'<td>{esc((a.get("reading") or "")[:90]) or DASH}</td>'
            f'<td><span class="pill">{esc(a.get("pill")) or DASH}</span></td>'
            "</tr>"
            for a in axes
        )
        parts.append(
            '<div class="twrap"><table class="t"><thead><tr>'
            "<th>維度</th><th>現值</th><th>訊號</th>"
            "</tr></thead><tbody>" + rows + "</tbody></table></div>"
        )
    else:
        parts.append('<div class="empty">今日無維度資料。</div>')

    parts.append('<p class="note"><a href="/regime/">完整互動頁 →</a></p>')
    return "".join(parts)


def render_weekly_rotation() -> str:
    d = load_json_safe(ROTATION_LATEST_FILE) or {}
    if not d:
        return (
            _weekly_section_head("產業輪動", "Rotation", None)
            + '<div class="empty">今日尚無資料，見 <a href="/rotation/">/rotation/</a>。</div>'
        )
    as_of = d.get("as_of") or (d.get("generated_at") or "")[:10]
    parts = [_weekly_section_head("產業輪動", "Rotation", as_of)]

    qc = d.get("quadrant_counts") or {}
    quad_labels = [("leading", "領先"), ("improving", "轉強"), ("weakening", "轉弱"), ("lagging", "落後")]
    quad_html = "".join(
        f'<div class="c"><div class="k">{esc(lab)}</div>'
        f'<div class="v">{esc(fmt_num(qc.get(key))) or "0"}</div></div>'
        for key, lab in quad_labels
    )
    parts.append(f'<div class="stat-cards">{quad_html}</div>')

    themes = d.get("themes") or []

    def _theme_table(items) -> str:
        if not items:
            return '<div class="empty">無資料。</div>'
        rows = "".join(
            "<tr>"
            f'<td>{esc(t.get("theme")) or DASH}</td>'
            f'<td class="num">{esc(fmt_num(t.get("rs_ratio"))) or DASH}</td>'
            f'<td class="num">{esc(fmt_num(t.get("rs_mom"))) or DASH}</td>'
            "</tr>"
            for t in items
        )
        return (
            '<div class="twrap"><table class="t"><thead><tr>'
            "<th>主題</th><th>RS-Ratio</th><th>RS-Mom</th>"
            "</tr></thead><tbody>" + rows + "</tbody></table></div>"
        )

    leading = sorted(
        (t for t in themes if t.get("quadrant") == "leading" and t.get("rs_ratio") is not None),
        key=lambda t: -t["rs_ratio"],
    )[:5]
    lagging = sorted(
        (t for t in themes if t.get("quadrant") == "lagging" and t.get("rs_ratio") is not None),
        key=lambda t: t["rs_ratio"],
    )[:5]

    parts.append('<div style="font-weight:600;font-size:12.5px;margin:10px 0 4px;color:var(--ink2)">領先前 5</div>')
    parts.append(_theme_table(leading))
    parts.append('<div style="font-weight:600;font-size:12.5px;margin:10px 0 4px;color:var(--ink2)">落後前 5</div>')
    parts.append(_theme_table(lagging))

    parts.append(
        '<p class="note"><a href="/rotation/">完整互動頁 →</a> · '
        '<a href="/rotation/radar.html">輪動雷達 →</a></p>'
    )
    return "".join(parts)


def build_weekly_body(badges: dict) -> str:
    p = ['<div class="wrap">']
    p.append(
        '<div class="mast"><div class="ttl"><h1>週更</h1>'
        '<div class="date">擁擠交易／Regime／產業輪動（原生渲染，週日更新）</div></div>'
        + _util_chips() + "</div>"
    )
    p.append(render_tabstrip("weekly.html", badges))
    p.append(render_weekly_crowding())
    p.append(render_weekly_regime())
    p.append(render_weekly_rotation())
    p.append(
        '<p class="note" style="margin-top:16px">完整互動頁：'
        '<a href="/crowding/">/crowding/</a> · '
        '<a href="/regime/">/regime/</a> · '
        '<a href="/rotation/">/rotation/</a> · '
        '<a href="/rotation/radar.html">/rotation/radar.html</a></p>'
    )
    p.append("</div>")
    p.append(FOOT)
    return "\n".join(p)


def build_calendar_body(date_str: str, calendar: list, badges: dict) -> str:
    try:
        base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        base_date = datetime.now(timezone.utc).date()
    cat = load_json_safe(CATALYST_CALENDAR_FILE) or {}
    cat_events = cat.get("events") or []

    by_date: dict = {}
    for e in calendar or []:
        d = e.get("date")
        if d:
            by_date.setdefault(d, []).append(("intel", e))
    for e in cat_events:
        d = e.get("date")
        if d:
            by_date.setdefault(d, []).append(("catalyst", e))

    days = [base_date + timedelta(days=i) for i in range(14)]
    cells = []
    for d in days:
        ds = d.isoformat()
        items = by_date.get(ds) or []
        label = f"{d.month:02d}/{d.day:02d}（{weekday_zh(d)}）"
        rows = []
        for kind, e in items[:6]:
            if kind == "intel":
                impact = (e.get("impact") or "").lower()
                hi = bool(e.get("hi")) or impact == "high"
                t = (e.get("time") or "").strip()
                txt = (e.get("text") or "").strip()
                line = (esc(t) + " " + esc(txt)).strip()
            else:
                hi = (e.get("impact") or "") in ("高", "high", "High")
                line = f'{esc(e.get("ticker") or "")}：{esc(e.get("event") or "")}'
            cls = " hi" if hi else ""
            rows.append(f'<div class="cd{cls}">{line}</div>')
        more = len(items) - 6
        if more > 0:
            rows.append(f'<div class="cd more">+{more}</div>')
        cells.append(
            f'<div class="cal14-cell"><div class="cal14-d">{esc(label)}</div>{"".join(rows)}</div>'
        )

    p = ['<div class="wrap">']
    p.append(
        '<div class="mast"><div class="ttl"><h1>行事曆</h1>'
        '<div class="date">接下來 14 天　intel 日曆（總經／ForexFactory／財報）＋ catalyst 催化劑</div></div>'
        + _util_chips() + "</div>"
    )
    p.append(render_tabstrip("calendar.html", badges))
    p.append(f'<div class="cal14">{"".join(cells)}</div>')
    p.append("</div>")
    p.append(FOOT)
    return "\n".join(p)


# --------------------------------------------------------- 產業（Task C3/C4）

def load_theme_history() -> dict:
    return load_json_safe(THEME_HISTORY_FILE) or {"schema": "intel-theme-history-v1", "themes": []}


def update_theme_history(date_str: str, cards: list, themes: list) -> None:
    """Task C3（2026-08-20）：每主題每日卡數 state，比照 threads.json 慣例（見
    threads.py 設計樣板）——只記有卡的（主題, 日期）配對（沒卡的日期不寫 0，
    跟 threads.json 的 daily_counts 慣例一致，讀取端用 `.get(date, 0)` 補
    空缺），14 天保留窗，超窗的日期整批砍掉；一個主題砍到 daily_counts 變空
    就整條移除，state 檔不會無限成長。zero-churn：序列化內容不變就不重寫，
    不寫 generated_at（比照 write_status_snapshot()）。只在正式輸出（out_dir
    == DOCS_INTEL）呼叫；任何一步失敗都吞掉，不擋頁面渲染——這是狀態累積檔，
    不是當日渲染的必要輸入。"""
    import json

    counts: dict = {}
    for c in cards:
        key = assign_theme(c, themes)
        if key:
            counts[key] = counts.get(key, 0) + 1

    state = load_theme_history()
    by_key = {t.get("key"): dict(t) for t in (state.get("themes") or []) if t.get("key")}

    try:
        base = datetime.strptime(date_str, "%Y-%m-%d").date()
        cutoff = (base - timedelta(days=THEME_HISTORY_RETENTION_DAYS - 1)).isoformat()
    except ValueError:
        cutoff = None

    for key, cnt in counts.items():
        entry = by_key.setdefault(key, {"key": key, "daily_counts": {}})
        dc = dict(entry.get("daily_counts") or {})
        dc[date_str] = cnt
        entry["daily_counts"] = dc

    out_themes = []
    for key in sorted(by_key):
        entry = by_key[key]
        dc = entry.get("daily_counts") or {}
        if cutoff:
            dc = {d: v for d, v in dc.items() if d >= cutoff}
        if not dc:
            continue
        out_themes.append({"key": key, "daily_counts": dc})

    content = json.dumps(
        {"schema": "intel-theme-history-v1", "themes": out_themes},
        ensure_ascii=False, sort_keys=True, indent=1,
    ) + "\n"
    try:
        if THEME_HISTORY_FILE.read_text(encoding="utf-8") == content:
            return
    except OSError:
        pass
    try:
        THEME_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        THEME_HISTORY_FILE.write_text(content, encoding="utf-8")
    except OSError as exc:
        print(f"[render.py] theme_history write skipped ({exc})", file=sys.stderr)


def theme_sparkline(date_str: str, key: str, days: int = 7) -> list:
    state = load_theme_history()
    by_key = {t.get("key"): t for t in (state.get("themes") or [])}
    dc = (by_key.get(key) or {}).get("daily_counts") or {}
    try:
        td = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return [0] * days
    out = []
    for i in range(days - 1, -1, -1):
        ds = (td - timedelta(days=i)).isoformat()
        out.append(dc.get(ds, 0) or 0)
    return out


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


KILL_STATUS_ZH = {"breached": "已突破", "near": "接近門檻", "green": "正常"}


def _kill_theme_pick(kill_theme: str, kw_items: list) -> dict | None:
    """C4 產業分頁站內錨點之一：從 kill_watch items 挑同一 macro theme 裡最
    值得關注的一筆——breached 優先於 near 優先於 green，同組內取現值離門檻
    最近（distance 最小）的那筆。找不到回 None（頁面該格整段省略，不是空
    佔位）。"""
    cand = [it for it in kill_items_for(kill_theme, kw_items)]
    if not cand:
        return None
    status_rank = {"breached": 0, "near": 1, "green": 2}

    def _dist(it):
        v, t = _f(it.get("current")), _f(it.get("value"))
        if v is None or t is None or t == 0:
            return 999.0
        return abs(v - t) / abs(t) * 100.0

    cand.sort(key=lambda it: (status_rank.get(it.get("status"), 3), _dist(it)))
    return cand[0]


def kill_items_for(kill_theme: str, kw_items: list) -> list:
    return [it for it in kw_items if it.get("theme") == kill_theme]


def _crowding_theme_pick(crowding_key: str, crowding_themes: list) -> dict | None:
    ck = crowding_key.lower()
    for ct in crowding_themes:
        if ck in (ct.get("name") or "").lower():
            return ct
    return None


def compute_theme_rows(date_str: str, payload: dict) -> list:
    """Task C4：組出「產業」分頁每一列需要的資料——name_zh／7 日 sparkline／
    今日最重要 1 條（沿用 Task A 的打分法）／站內錨點（ID 連結／kill 距離／
    擁擠分數，各自缺就省略）／週更綜述（Task D，缺檔不渲染）。近 7 日零卡且
    無任何站內錨的主題整條不回傳（規格：「近 7 日零卡且無站內錨的主題不
    顯示」）。任一跨站台來源壞掉都各自 fail-safe，不影響其他主題或其他錨點
    種類。"""
    themes = load_themes_yml()
    cards = payload.get("cards") or []
    kw = load_json_safe(KILL_WATCH_FILE) or {}
    kw_items = kw.get("items") or []
    crowding = load_json_safe(CROWDING_LATEST_FILE) or {}
    crowding_themes = crowding.get("themes") or []
    weekly = load_json_safe(THEME_WEEKLY_FILE) or {}
    weekly_themes = weekly.get("themes") if isinstance(weekly.get("themes"), dict) else {}
    weekly_week_of = weekly.get("week_of")

    threads = payload.get("threads") or []
    threads_by_id = {t.get("id"): t for t in threads if t.get("id")}
    pool = [
        c for c in cards
        if not is_rumor(c) and not is_title_only(c) and (c.get("summary_zh") or "").strip()
    ]
    top_by_theme: dict = {}
    for c in pool:
        key = assign_theme(c, themes)
        if not key:
            continue
        score = _news_highlight_score(c, threads_by_id, threads)
        cur = top_by_theme.get(key)
        if cur is None or score > cur[0]:
            top_by_theme[key] = (score, c)

    rows = []
    for t in themes:
        key = t["key"]
        try:
            spark = theme_sparkline(date_str, key, days=7)
        except Exception:
            spark = [0] * 7
        total7 = sum(spark)
        top_card = (top_by_theme.get(key) or (None, None))[1]

        id_page = t.get("id_page")
        id_link = f"/id/{id_page}" if id_page else None

        kill_item = None
        if t.get("kill_theme"):
            try:
                kill_item = _kill_theme_pick(t["kill_theme"], kw_items)
            except Exception:
                kill_item = None

        crowding_item = None
        if t.get("crowding_key"):
            try:
                crowding_item = _crowding_theme_pick(t["crowding_key"], crowding_themes)
            except Exception:
                crowding_item = None

        if total7 == 0 and not (id_link or kill_item or crowding_item):
            continue

        rows.append({
            "key": key, "name_zh": t.get("name_zh") or key,
            "sparkline": spark, "total7": total7, "top_card": top_card,
            "id_link": id_link, "kill_item": kill_item, "crowding_item": crowding_item,
            "weekly_zh": (weekly_themes or {}).get(key), "weekly_week_of": weekly_week_of,
        })

    rows.sort(key=lambda r: -r["total7"])
    return rows


def _theme_weekly_block(weekly_zh: str | None, week_of: str | None, date_str: str) -> str:
    """Task D 渲染：週更綜述掛在每主題列下方，>8 天視為過期整段標灰（缺檔
    不渲染、不報錯——呼叫端只在 weekly_zh 有值時才呼叫本函式）。"""
    if not weekly_zh or not weekly_zh.strip():
        return ""
    stale = False
    if week_of:
        try:
            wd = datetime.strptime(week_of, "%Y-%m-%d").date()
            td = datetime.strptime(date_str, "%Y-%m-%d").date()
            stale = (td - wd).days > THEME_WEEKLY_STALE_DAYS
        except ValueError:
            pass
    cls = "theme-weekly stale" if stale else "theme-weekly"
    stale_note = "（已過期，等待下次週更）" if stale else ""
    as_of = esc(week_of or "")
    return (
        f'<div class="{cls}">{esc(weekly_zh)}'
        f'<div class="tw-meta">週更綜述 · {as_of}{esc(stale_note)}</div></div>'
    )


def render_theme_row(row: dict, date_str: str) -> str:
    spark = _sparkline_svg(row.get("sparkline") or [], width=90, height=20)
    top_card = row.get("top_card")
    if top_card:
        title = _card_title(top_card)
        url = top_card.get("url") or ""
        top_html = (
            f'<a href="{esc(url)}" rel="noopener nofollow">{title}</a>'
            if url and _safe_href(url) else f'<span>{title}</span>'
        )
    else:
        top_html = f'<span class="mut">{DASH}</span>'

    anchors = []
    if row.get("id_link"):
        anchors.append(f'<a class="chip" href="{esc(row["id_link"])}">產業報告 ↗</a>')
    ki = row.get("kill_item")
    if ki:
        status_zh = KILL_STATUS_ZH.get(ki.get("status"), ki.get("status") or "")
        metric = esc((ki.get("metric_text") or "")[:24])
        doc = ki.get("doc") or ""
        href = "/" + doc.split("docs/", 1)[-1] if doc else "/detective/"
        anchors.append(
            f'<a class="chip" href="{esc(href)}">kill：{metric}｜{esc(status_zh)} ↗</a>'
        )
    ci = row.get("crowding_item")
    if ci and ci.get("score") is not None:
        anchors.append(
            f'<a class="chip" href="/crowding/">擁擠分數 {esc(fmt_num(ci.get("score")))}'
            f'（第 {esc(fmt_num(ci.get("rank")))} 名）↗</a>'
        )
    anchors_html = f'<div class="theme-anchors">{"".join(anchors)}</div>' if anchors else ""

    weekly_html = _theme_weekly_block(row.get("weekly_zh"), row.get("weekly_week_of"), date_str)

    return (
        '<div class="theme-row">'
        f'<div class="theme-top"><span class="tt">{esc(row["name_zh"])}</span>'
        f'<span class="thsp">{spark}</span>'
        f'<span class="tht">近 7 日 {row.get("total7", 0)} 張</span></div>'
        f'<div class="theme-card">{top_html}</div>'
        f'{anchors_html}{weekly_html}'
        '</div>'
    )


def build_themes_body(date_str: str, payload: dict, badges: dict) -> str:
    rows = compute_theme_rows(date_str, payload)
    p = ['<div class="wrap">']
    p.append(
        '<div class="mast"><div class="ttl"><h1>產業</h1>'
        f'<div class="date">依主題分組的產業層卡片，共 {len(rows)} 個主題有資料或站內錨點</div></div>'
        + _util_chips() + "</div>"
    )
    p.append(render_tabstrip("themes.html", badges))
    if not rows:
        p.append('<div class="empty">近 7 日尚無任何主題卡片或站內錨點資料。</div>')
    else:
        p.append('<div class="theme-list">' + "\n".join(render_theme_row(r, date_str) for r in rows) + "</div>")
    p.append("</div>")
    p.append(FOOT)
    return "\n".join(p)


def build_threads_body(date_str: str, badges: dict) -> str:
    threads = compute_full_threads(date_str)
    p = ['<div class="wrap">']
    p.append(
        '<div class="mast"><div class="ttl"><h1>故事線</h1>'
        f'<div class="date">進行中的故事線，共 {len(threads)} 條</div></div>'
        + _util_chips() + "</div>"
    )
    p.append(render_tabstrip("threads.html", badges))
    p.append(render_threads(threads, detail_limit=None) if threads else '<div class="empty">目前無進行中的故事線。</div>')
    p.append("</div>")
    p.append(FOOT)
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


def render_archive(current_date: str, out_dir: Path, badges: dict = None) -> str:
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
        render_tabstrip("archive.html", badges),
        f'<ul class="arclist">{"".join(items)}</ul>' if items else '<div class="empty">尚無封存頁面。</div>',
        "</div>",
        FOOT,
    ]
    return "\n".join(body)


# ------------------------------------------------------------------- status

def render_status_page(date_str: str, payload: dict, sources_meta: dict, badges: dict = None) -> str:
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
        render_tabstrip("status.html", badges),
        render_chain_status(),
        h2("當日摘要", "Summary"),
        f'<div class="stat-cards">{stat_html}</div>',
        h2("來源健康", "Sources"),
        table,
        "</div>",
        FOOT,
    ]
    return "\n".join(body)


CHAIN_STATUS_FILE = DATA_DIR / "chain_status.json"
_CHAIN_ICON = {"success": "✅", "failure": "❌", "cancelled": "◻︎", "skipped": "◻︎"}
# Phase B（2026-08-20）：每節後面的人話說明——名字對照
# .github/workflows/intel-2-daily.yml 寫進 /tmp/chain_status.txt 的固定七個
# step name（monitor/detective/crossasset/catalyst/killwatch/intel_fetch/
# intel_run），未知 name 就不加說明（不擋渲染）。
_CHAIN_STEP_DESC = {
    "monitor": "跨資產壓力儀表",
    "detective": "訊號網",
    "crossasset": "週更三頁（擁擠交易／Regime／產業輪動）",
    "catalyst": "催化劑行事曆",
    "killwatch": "證偽表",
    "intel_fetch": "新聞抓取",
    "intel_run": "AI 摘要",
}


def _chain_all_success(data: dict) -> bool:
    steps = data.get("steps") or []
    if not steps:
        return False
    return all((s.get("outcome") or "").lower() == "success" for s in steps)


def render_chain_status() -> str:
    """一條鏈 workflow（.github/workflows/intel-2-daily.yml）寫的
    docs/intel/data/chain_status.json 讀得到才顯示；讀不到（舊 workflow 尚未產生
    這份檔，或本機測試 render 時本來就沒有）整段省略，不視為錯誤。"""
    data = load_json_safe(CHAIN_STATUS_FILE)
    if not data or not data.get("steps"):
        return ""
    rows = []
    for s in data["steps"]:
        name = s.get("name") or ""
        outcome = (s.get("outcome") or "").lower()
        icon = _CHAIN_ICON.get(outcome, "◻︎")
        secs = s.get("seconds")
        secs_s = f"{secs}s" if secs is not None else DASH
        desc = _CHAIN_STEP_DESC.get(name, "")
        label = f"{name}　{desc}" if desc else name
        rows.append(
            f'<div class="c"><div class="k">{esc(label)}</div>'
            f'<div class="v">{icon} <span class="note" style="margin:0;font-size:11px">{esc(secs_s)}</span></div></div>'
        )
    # 一行總結：本頁只保留當日 chain_status.json（每次覆蓋、不留歷史），故只能
    # 判斷「今天這條鏈是否整條成功」，不能回溯更早的成功日期——誠實標示這個
    # 侷限，而不是編造一個查不到來源的日期。
    if _chain_all_success(data):
        summary = f"上次完整成功：{esc(data.get('date') or DASH)}"
    else:
        summary = (
            "上次完整成功：非今日（本頁僅追蹤當日鏈路狀態，"
            "更早的成功記錄請查 GitHub Actions run history）"
        )
    return (
        h2("一條鏈狀態", "Chain")
        + f'<p class="note">{esc(data.get("date") or "")}</p>'
        + f'<div class="stat-cards">{"".join(rows)}</div>'
        + f'<p class="note">{summary}</p>'
    )


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

    # Phase C：只在正式輸出（docs/intel/）時落地現況快照；--out 測試模式不動 docs/。
    # 快照失敗不擋頁面渲染。
    if out_dir == DOCS_INTEL:
        try:
            write_status_snapshot(load_status_snapshot())
        except Exception as exc:  # noqa: BLE001
            print(f"status_snapshot: skipped ({exc})", file=sys.stderr)

    payload, banner, stale = resolve_day_payload(date_str, sources_meta, data_path)
    calendar = payload.get("calendar") or []
    det_for_badges = load_json_safe(DETECTIVE_LATEST_FILE) or {}
    badges = compute_tab_badges(date_str, calendar, det_for_badges)

    # Task C3（2026-08-20）：每主題每日卡數 state——只在正式輸出時累積歷史，
    # --out 測試模式不動 docs/。失敗不擋渲染。
    if out_dir == DOCS_INTEL:
        try:
            update_theme_history(date_str, payload.get("cards") or [], load_themes_yml())
        except Exception as exc:  # noqa: BLE001
            print(f"theme_history: skipped ({exc})", file=sys.stderr)

    try:
        theme_rows = compute_theme_rows(date_str, payload)
        badges["theme_n"] = len(theme_rows)
    except Exception as exc:  # noqa: BLE001
        print(f"theme rows: skipped ({exc})", file=sys.stderr)
        badges["theme_n"] = None

    index_body = build_day_body(date_str, payload, banner, is_archive=False, badges=badges)
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

    day_body = build_day_body(date_str, payload, banner, is_archive=True, badges=badges)
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
        + render_archive(date_str, out_dir, badges)
        + "\n</body>\n</html>\n"
    )
    archive_path = out_dir / "archive.html"
    archive_path.write_text(archive_html, encoding="utf-8")

    status_html = (
        head("監視器狀態 — InvestMQuest Research", "全球金融市場監視器來源健康與每日用量。", indexable=False)
        + "\n<body>\n"
        + render_status_page(date_str, payload, sources_meta, badges)
        + "\n</body>\n</html>\n"
    )
    status_path = out_dir / "status.html"
    status_path.write_text(status_html, encoding="utf-8")

    # 2.0 Phase A 新增分頁：變化／儀表／週更／行事曆／故事線。各自獨立讀取跨站台
    # JSON（fail-safe），不依賴今日 intel pipeline 是否跑成功。
    kw_for_change = load_json_safe(KILL_WATCH_FILE) or {}
    state_for_change = load_json_safe(DETECTIVE_STATE_FILE) or {}
    change_html = (
        head("變化 — 全球金融市場監視器 — InvestMQuest Research",
             "今日訊號、生命週期、證偽對帳、複合規則靶盤。", indexable=False)
        + "\n<body>\n"
        + build_change_body(date_str, det_for_badges, state_for_change, kw_for_change, badges)
        + "\n</body>\n</html>\n"
    )
    change_path = out_dir / "change.html"
    change_path.write_text(change_html, encoding="utf-8")

    gauges_html = (
        head("儀表 — 全球金融市場監視器 — InvestMQuest Research",
             "機械層 96 條序列，來自 /monitor/。", indexable=False)
        + "\n<body>\n"
        + build_gauges_body(badges)
        + "\n</body>\n</html>\n"
    )
    gauges_path = out_dir / "gauges.html"
    gauges_path.write_text(gauges_html, encoding="utf-8")

    weekly_html = (
        head("週更 — 全球金融市場監視器 — InvestMQuest Research",
             "擁擠交易／Regime／產業輪動／資產輪動雷達。", indexable=False)
        + "\n<body>\n"
        + build_weekly_body(badges)
        + "\n</body>\n</html>\n"
    )
    weekly_path = out_dir / "weekly.html"
    weekly_path.write_text(weekly_html, encoding="utf-8")

    calendar_html = (
        head("行事曆 — 全球金融市場監視器 — InvestMQuest Research",
             "接下來 14 天：intel 日曆＋ catalyst 催化劑。", indexable=False)
        + "\n<body>\n"
        + build_calendar_body(date_str, calendar, badges)
        + "\n</body>\n</html>\n"
    )
    calendar_path = out_dir / "calendar.html"
    calendar_path.write_text(calendar_html, encoding="utf-8")

    themes_html = (
        head("產業 — 全球金融市場監視器 — InvestMQuest Research",
             "依主題分組的產業層卡片：熱度趨勢、今日焦點、ID／kill-watch／擁擠交易站內錨點。",
             indexable=False)
        + "\n<body>\n"
        + build_themes_body(date_str, payload, badges)
        + "\n</body>\n</html>\n"
    )
    themes_path = out_dir / "themes.html"
    themes_path.write_text(themes_html, encoding="utf-8")

    threads_html = (
        head("故事線 — 全球金融市場監視器 — InvestMQuest Research",
             "進行中的故事線，逐條展開近期所有卡片。", indexable=False)
        + "\n<body>\n"
        + build_threads_body(date_str, badges)
        + "\n</body>\n</html>\n"
    )
    threads_path = out_dir / "threads.html"
    threads_path.write_text(threads_html, encoding="utf-8")

    all_paths = [
        index_path, day_path, archive_path, status_path,
        change_path, gauges_path, weekly_path, themes_path, calendar_path, threads_path,
    ]
    if out_dir == DOCS_INTEL:
        inject_nav(all_paths)

    for p in all_paths:
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
