#!/usr/bin/env python3
"""scripts/intel/fetch.py — Phase 1（市場層）情報抓取／正規化／去重／預過濾。

對應 notes/site-internal/intel/DESIGN.md §6（最省資源）／§7（正確性五道）／
§10（每天怎麼跑，本檔＝06:00 那個 job）／§11（卡片 schema）／§14（防護）。

全程零 LLM：抓取 → 正規化 → 站內數字卡（門檻／變化觸發）→ 去重（URL＋標題相似度）
→ 新鮮度過濾 → 關鍵字預過濾（deny-list）→ 連結存活檢查 → 寫
docs/intel/pending/YYYY-MM-DD.json ＋ docs/intel/data/sources_health.json。

CLI:
    python3 scripts/intel/fetch.py --date 2026-08-19
    python3 scripts/intel/fetch.py --date 2026-08-19 --dry-run
    python3 scripts/intel/fetch.py --date 2026-08-19 --only fed_press_all

退出碼：永遠 0，除非「本次嘗試抓取的來源」超過一半失敗才回傳 1（GHA 用來標示
本次抓取品質下降，不代表 pending JSON 沒寫出來 —— 檔案照樣會寫）。
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
import json
import re
import statistics
import sys
import time
import unicodedata
from urllib.parse import urljoin
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests
import yaml

import sec_filings  # 2026-08-19 新增：kind=="sec_8k" dispatch，見該檔 docstring

ROOT = Path(__file__).resolve().parent.parent.parent
INTEL_DIR = ROOT / "scripts" / "intel"
SOURCES_YML = INTEL_DIR / "sources.yml"
DATA_DIR = ROOT / "docs" / "intel" / "data"
PENDING_DIR = ROOT / "docs" / "intel" / "pending"
STATE_FILE = DATA_DIR / "state.json"
HEALTH_FILE = DATA_DIR / "sources_health.json"

UA = "IntelBot/1.0 (+https://research.investmquest.com; market-layer intel monitor)"
TIMEOUT = 10
LINK_CHECK_TIMEOUT = 5
LINK_CHECK_TOP_N = 60
FRESHNESS_HOURS = 36
MAX_KEPT = 420
DEDUP_JACCARD = 0.85
# 2026-08-19：來源擴充後同一事件常同時被直接來源與 Google News 聚合命中；
# 這條較寬鬆的門檻只負責「跨來源」合併（見 dedup_cards 第二段），避免同日
# 同事件在頁面上重複出現、卻仍保留 corroboration 計數。
DEDUP_JACCARD_CROSS = 0.6

# Google News RSS 聚合搜尋（kind: gnews）：逐則卡片依 <source> 標籤覆寫
# source_name/source_short/source_tier，這份清單只決定「覆寫成 T2 還是 T3」
# ——不在清單內一律 T3（聚合層預設，即使查到具名發布方）。比對前先轉小寫。
GNEWS_MAJOR_PUBLISHERS = [
    "reuters", "bloomberg", "cnbc", "wsj", "wall street journal",
    "financial times", "ft.com", "associated press", "ap news",
    "nikkei", "經濟日報", "工商時報", "鉅亨網", "中央社",
]

TIER_RANK = {"T1": 0, "T2": 1, "T3": 2, "T4": 3}

# 關鍵字預過濾：deny-list（運動／娛樂／八卦），與投資無關，直接丟。刻意保持
# 極短——Phase 1 來源清單本身已是精選官方／總經／地緣媒體，不是泛用新聞牆，
# 誤傷風險低；allow-hints 留待 Phase 2（產業層來源變雜後）再視需要加。
DENY_KEYWORDS = [
    "celebrity", "kardashian", "box office", "grammy", "oscar awards",
    "football transfer", "premier league", "world cup final", "olympics medal",
    "娛樂圈", "八卦", "緋聞", "演唱會", "偶像團體", "選秀節目",
]

FRED_SIGMA_MULT = 2.0

# monitor/alerts.json 的 cat -> intel 13 維度 key 對照（實測 cat 全集見腳本 docstring）。
MONITOR_CAT_MAP = {
    "commodities": "commodities",
    "credit": "credit",
    "crypto": "crypto",
    "factors": "breadth",
    "fx": "fx",
    "indices": "breadth",
    "liquidity": "liquidity",
    "rates": "rates",
    "sectors": "breadth",
    "vol": "vol",
}

POLYMARKET_KEYWORDS = [
    "fed", "rate cut", "rate hike", "recession", "government shutdown",
    "default", "tariff", "war", "invade", "invasion", "ceasefire",
    "election", "impeach", "sanction",
]

# 2026-08-19 新增：Kalshi（第二家預測市場，補 polymarket）。跟 polymarket 不同，
# Kalshi 的 /markets?limit=100&status=open 泛用清單本身以運動合約為主（實測：
# 100 筆裡關鍵字比對只會誤中球員姓名子字串，例如 "Federico" 含 "fed"），所以不
# 走「抓一批→關鍵字篩」，改成「先指定經濟類 series_ticker→逐一查」，見
# fetch_kalshi_source()。四個 series 對應 DESIGN.md §3「地緣／央行」要的
# Fed／衰退／關稅機率：
#   KXFED         下次會議後 Fed funds 利率（多檔 strike，取離 0.5 最近的一檔代表）
#   KXFEDDECISION 下次會議升/降息機率
#   KXRECSSNBER   NBER 認定的衰退機率
#   KXEFFTARIFF   美國有效關稅稅率（季度）
KALSHI_SERIES = ["KXFED", "KXFEDDECISION", "KXRECSSNBER", "KXEFFTARIFF"]
KALSHI_MAX_CARDS = 8


# ── 小工具 ───────────────────────────────────────────────────────────────
def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha1_id(s: str, n: int = 12) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:n]


TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_html(text: str, limit: int = 400) -> str:
    """§14 prompt-injection hygiene：去 HTML tag、collapse 空白、截斷。純資料，
    不執行、不解讀來源文字裡的任何「指令」。"""
    if not text:
        return ""
    text = html.unescape(text)
    text = TAG_RE.sub(" ", text)
    text = WS_RE.sub(" ", text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def norm_title_tokens(title: str) -> set:
    t = unicodedata.normalize("NFKC", title or "").lower()
    t = re.sub(r"[^\w\s一-鿿]", " ", t)
    return {tok for tok in t.split() if tok}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def parse_dt(value) -> datetime | None:
    if not value:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc)
        except (OSError, OverflowError, ValueError):
            return None
    if isinstance(value, time.struct_time):
        try:
            return datetime(*value[:6], tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


# ── 來源健康追蹤 ─────────────────────────────────────────────────────────
class Health:
    def __init__(self):
        self.records = []

    def record(self, source_id, ok, status=None, latency_ms=None, item_count=0, error=None):
        self.records.append(
            {
                "source_id": source_id,
                "ok": ok,
                "status": status,
                "latency_ms": latency_ms,
                "item_count": item_count,
                "error": error,
                "checked_at": iso(now_utc()),
            }
        )


def http_get(url: str, retries: int = 1, timeout: int = TIMEOUT, ua: str = UA, cookies: dict | None = None):
    """GET with a single retry. Returns (ok, status, latency_ms, text_or_none, error_or_none).
    `ua` 預設用全站 UA；2026-08-19 加這個參數是因為 mining.com 的 WAF 專門擋
    UA 字串裡含 "Bot"（同一端點用瀏覽器風格 UA 測試回 200），見
    fetch_rss_source 的 source.get("ua") 覆寫。`cookies`（2026-08-20 新增）：
    PTT 分齡確認用（`over18=1`），見 fetch_ptt_source。"""
    last_err = None
    for attempt in range(retries + 1):
        t0 = time.time()
        try:
            resp = requests.get(
                url, headers={"User-Agent": ua, "Accept": "*/*"}, timeout=timeout,
                cookies=cookies,
            )
            latency_ms = int((time.time() - t0) * 1000)
            if resp.status_code >= 400:
                last_err = f"HTTP {resp.status_code}"
                if attempt < retries:
                    continue
                return False, resp.status_code, latency_ms, None, last_err
            return True, resp.status_code, latency_ms, resp.text, None
        except requests.RequestException as e:
            latency_ms = int((time.time() - t0) * 1000)
            last_err = str(e)[:200]
            if attempt < retries:
                continue
            return False, None, latency_ms, None, last_err
    return False, None, None, None, last_err


# ── RSS 來源 ─────────────────────────────────────────────────────────────
def fetch_rss_source(source: dict, health: Health) -> list[dict]:
    sid = source["id"]
    ok, status, latency_ms, text, err = http_get(source["url"], ua=source.get("ua", UA))
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    parsed = feedparser.parse(text)
    entries = parsed.entries[: source.get("max_items", 30)]
    cards = []
    for e in entries:
        title = strip_html(e.get("title", ""), limit=200)
        link = e.get("link", "") or ""
        if link and not link.startswith("http"):
            # 2026-08-19：BOK／RBI 這類 feed 給相對路徑，補成絕對網址（否則 QC 當站內死連結）
            link = urljoin(source["url"], link)
        if not title or not link:
            continue
        summary = strip_html(
            e.get("summary", "") or e.get("description", ""), limit=400
        )
        pub = parse_dt(e.get("published_parsed")) or parse_dt(e.get("updated_parsed"))
        cards.append(
            {
                "kind": "news",
                "level": source.get("level", "market"),
                "category": source["category"],
                "source_tier": source["tier"],
                "source_id": sid,
                "title": title,
                "url": link,
                "published_at": iso(pub) if pub else None,
                "lang": source.get("lang", "en"),
                "summary_raw": summary,
            }
        )
    health.record(sid, True, status, latency_ms, len(cards))
    return cards


# ── Google News 主題聚合（kind: gnews）──────────────────────────────────
def _gnews_tier_for(publisher: str, default_tier: str) -> str:
    p = (publisher or "").lower()
    if any(m in p for m in GNEWS_MAJOR_PUBLISHERS):
        return "T2"
    return default_tier if default_tier in ("T2", "T3") else "T3"


def _gnews_short(publisher: str) -> str:
    """≤8 字短名：具名主流媒體用慣用縮寫，其餘直接截斷（CJK 也算一個字元）。"""
    p = (publisher or "").strip()
    lower = p.lower()
    known = {
        "reuters": "Reuters", "bloomberg": "Bloomberg", "cnbc": "CNBC",
        "wsj": "WSJ", "wall street journal": "WSJ",
        "financial times": "FT", "ft.com": "FT",
        "associated press": "AP", "ap news": "AP",
        "nikkei": "Nikkei", "經濟日報": "經濟日報", "工商時報": "工商時報",
        "鉅亨網": "鉅亨網", "cnyes": "鉅亨網", "中央社": "中央社",
        "investor's business daily": "IBD", "marketwatch": "MktWatch",
        "barron": "Barron's", "udn": "UDN", "ltn": "自由財經", "ctee": "工商時報",
        "economist": "Economist", "guardian": "Guardian", "yahoo": "Yahoo",
        "new york times": "NYT", "washington post": "WaPo",
    }
    for k, v in known.items():
        if k in lower:
            return v
    return _smart_short(p) if p else "GNews"


def _smart_short(name: str, limit: int = 14) -> str:
    """短名不硬切字：CJK 直接取前 8 字；拉丁文先去 The/網域尾巴，超長就切到
    最後一個完整的字（例 "The Mighty Ducks Times" → "Mighty Ducks"）。"""
    n = (name or "").strip()
    if re.search(r"[\u4e00-\u9fff]", n):
        return n[:8]
    n = re.sub(r"^(the|www\.)\s*", "", n, flags=re.I)
    n = re.sub(r"\.(com|net|org|tw|cn|jp|hk|co\.uk)(\.[a-z]{2})?$", "", n, flags=re.I)
    if len(n) <= limit:
        return n
    words, out = n.split(), ""
    for w in words:
        if len(out) + len(w) + (1 if out else 0) > limit:
            break
        out = f"{out} {w}".strip()
    return out or n[:limit]


def fetch_gnews_source(source: dict, health: Health) -> list[dict]:
    """Google News RSS 聚合搜尋：每則的真正發布方來自 <source> 標籤
    （feedparser 解析為 entry.source.title），標題會被 Google News 加上
    「 - 發布方」尾巴，這裡剝掉。tier/source_name/source_short 逐則覆寫，
    sources.yml 上的 tier/short 只是找不到 <source> 時的保守預設值。"""
    sid = source["id"]
    ok, status, latency_ms, text, err = http_get(source["url"])
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    parsed = feedparser.parse(text)
    entries = parsed.entries[: source.get("max_items", 10)]
    cards = []
    for e in entries:
        raw_title = strip_html(e.get("title", ""), limit=260)
        link = e.get("link", "") or ""
        if not raw_title or not link:
            continue
        src_obj = e.get("source")
        publisher = ""
        if isinstance(src_obj, dict):
            publisher = (src_obj.get("title") or "").strip()
        if not publisher:
            # fallback：標題本身就是「標題 - 發布方」格式
            m = re.search(r"\s-\s([^-]+)$", raw_title)
            if m:
                publisher = m.group(1).strip()
        # 去掉標題尾巴的 " - 發布方"
        title = raw_title
        if publisher and title.endswith(publisher):
            title = title[: -len(publisher)].rstrip()
            if title.endswith("-"):
                title = title[:-1].rstrip()
        summary = strip_html(e.get("summary", "") or e.get("description", ""), limit=400)
        pub = parse_dt(e.get("published_parsed")) or parse_dt(e.get("updated_parsed"))
        tier = _gnews_tier_for(publisher, source["tier"])
        cards.append(
            {
                "kind": "news",
                "level": source.get("level", "market"),
                "category": source["category"],
                "source_tier": tier,
                "source_id": sid,
                "source_name_override": publisher or source["name"],
                "source_short_override": _gnews_short(publisher) if publisher else None,
                "title": title or raw_title,
                "url": link,
                "published_at": iso(pub) if pub else None,
                "lang": source.get("lang", "en"),
                "summary_raw": summary,
            }
        )
    health.record(sid, True, status, latency_ms, len(cards))
    return cards


# ── ForexFactory 經濟日曆（kind: ff_calendar，不產卡）───────────────────
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

_ET_ZONE = ZoneInfo("America/New_York")
_TPE_ZONE = ZoneInfo("Asia/Taipei")
FF_CALENDAR_FILE = None  # set lazily from DATA_DIR in main() / module import


def et_time_to_taipei(date_str: str, time_str: str) -> tuple[str | None, str | None]:
    """ForexFactory 給的日期/時間是美東（ET，DST-aware）；轉台北（UTC+8，無 DST）。
    回傳 (YYYY-MM-DD, HH:MM)；解析失敗（例如 "All Day"/"Tentative"）回傳
    (None, None) —— 呼叫端保留原始欄位、只是不做時區換算。"""
    time_str = (time_str or "").strip()
    date_str = (date_str or "").strip()
    if not time_str or not date_str:
        return None, None
    try:
        dt_naive = datetime.strptime(f"{date_str} {time_str}", "%m-%d-%Y %I:%M%p")
    except ValueError:
        return None, None
    dt_et = dt_naive.replace(tzinfo=_ET_ZONE)
    dt_tpe = dt_et.astimezone(_TPE_ZONE)
    return dt_tpe.strftime("%Y-%m-%d"), dt_tpe.strftime("%H:%M")


def fetch_ff_calendar(source: dict, health: Health) -> list[dict]:
    """回傳 CALENDAR 條目（不是卡片，不進 fetched_cards/pending.json）：
    {date, time, country, text, hi, impact, forecast, previous, source, url}。
    只保留 impact in (High, Medium) —— DESIGN 要求的「未來 7 天」窗口留給
    summarize.py build_calendar 在渲染當下再過濾（本檔只負責忠實轉換這週的
    ForexFactory 排程）。單一來源失敗非致命：回傳 []，呼叫端不寫檔即可。"""
    sid = source["id"]
    ok, status, latency_ms, text, err = http_get(source["url"])
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        health.record(sid, False, status, latency_ms, 0, f"bad xml: {e}")
        return []

    out = []
    for ev in root.findall("event"):
        impact = (ev.findtext("impact") or "").strip()
        if impact not in ("High", "Medium"):
            continue
        title = (ev.findtext("title") or "").strip()
        country = (ev.findtext("country") or "").strip()
        date_raw = (ev.findtext("date") or "").strip()
        time_raw = (ev.findtext("time") or "").strip()
        if not title or not date_raw:
            continue
        date_tpe, time_tpe = et_time_to_taipei(date_raw, time_raw)
        if not date_tpe:
            # 轉換失敗（All Day/Tentative 等）：退回用原始 ET 日期，不換算時間。
            try:
                date_tpe = datetime.strptime(date_raw, "%m-%d-%Y").strftime("%Y-%m-%d")
            except ValueError:
                continue
            time_tpe = None
        out.append(
            {
                "date": date_tpe,
                "time": time_tpe,
                "country": country,
                "text": f"{country} {title}".strip(),
                "hi": impact == "High",
                "impact": "high" if impact == "High" else "medium",
                "forecast": (ev.findtext("forecast") or "").strip() or None,
                "previous": (ev.findtext("previous") or "").strip() or None,
                "source": "ForexFactory",
                "url": (ev.findtext("url") or "").strip() or None,
            }
        )
    health.record(sid, True, status, latency_ms, len(out))
    return out


# ── FRED CSV（kind: csv）─────────────────────────────────────────────────
def fetch_fred_source(source: dict, health: Health, state: dict) -> list[dict]:
    """簡單規則：20 個交易日變化是否超過近 1 年「20 日變化」標準差的 2 倍。純統計、
    零門檻表（keep it simple per DESIGN.md）。"""
    sid = source["id"]
    ok, status, latency_ms, text, err = http_get(source["url"])
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []

    rows = []
    for line in text.splitlines()[1:]:
        line = line.strip()
        if not line or "," not in line:
            continue
        d, v = line.split(",", 1)
        v = v.strip()
        if v == "." or v == "":
            continue
        try:
            rows.append((d.strip(), float(v)))
        except ValueError:
            continue

    if len(rows) < 30:
        health.record(sid, True, status, latency_ms, len(rows))
        return []

    window = rows[-260:]  # ~1 年交易日
    values = [v for _, v in window]
    # 20 日變化要對 20 日變化的分布比（不是對日變化 σ 比，否則幾乎天天觸發）
    changes = [values[i] - values[i - 20] for i in range(20, len(values))]
    sigma = statistics.pstdev(changes) if len(changes) > 1 else 0.0

    latest_date, latest_val = rows[-1]
    lookback = min(20, len(rows) - 1)
    prev_val = rows[-1 - lookback][1]
    change_20d = latest_val - prev_val
    threshold = FRED_SIGMA_MULT * sigma

    sorted_vals = sorted(values)
    pctile = round(
        100.0 * sum(1 for v in sorted_vals if v <= latest_val) / len(sorted_vals), 1
    )

    health.record(sid, True, status, latency_ms, 1)

    # 規則 2：一年水位進出極端帶（≥95 或 ≤5 分位），只在「換帶」那天發卡（state 記上次的帶）
    band = "hi" if pctile >= 95 else ("lo" if pctile <= 5 else "mid")
    bands = state.setdefault("fred_bands", {})
    prev_band = bands.get(sid)
    bands[sid] = band
    band_flip = band != "mid" and band != prev_band

    if not band_flip and (sigma <= 0 or abs(change_20d) <= threshold):
        return []

    m = re.search(r"[?&]id=([A-Za-z0-9_]+)", source["url"])
    series_id = m.group(1) if m else sid.replace("fred_", "").upper()
    if band_flip:
        title = f"{source['name']}：現值 {latest_val:g} 進入一年水位{'前' if band == 'hi' else '後'} 5%（分位 {pctile}）"
    else:
        title = f"{source['name']}：20 日變化 {change_20d:+.3f} 超過 1 年 20 日變化 {FRED_SIGMA_MULT:.0f}σ（{threshold:.3f}）"
    return [
        {
            "kind": "data",
            "level": "market",
            "category": source["category"],
            "source_tier": source["tier"],
            "source_id": sid,
            "title": title,
            "url": f"https://fred.stlouisfed.org/series/{series_id}",
            "published_at": None,
            "lang": "zh",
            "summary_raw": title,
            "data": {
                "series": series_id,
                "value": latest_val,
                "as_of": latest_date,
                "change_20d": round(change_20d, 4),
                "threshold": round(threshold, 4),
                "pctile": pctile,
            },
        }
    ]


# ── Polymarket（kind: json，特判）───────────────────────────────────────
def fetch_polymarket_source(source: dict, health: Health, state: dict) -> list[dict]:
    sid = source["id"]
    ok, status, latency_ms, text, err = http_get(source["url"])
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    try:
        markets = json.loads(text)
    except json.JSONDecodeError as e:
        health.record(sid, False, status, latency_ms, 0, f"bad json: {e}")
        return []

    health.record(sid, True, status, latency_ms, len(markets))

    prev_probs = state.get("polymarket_probs", {})
    new_probs = {}
    cards = []
    matched = 0
    for m in markets:
        q = (m.get("question") or "").lower()
        if not any(k in q for k in POLYMARKET_KEYWORDS):
            continue
        slug = m.get("slug")
        if not slug:
            continue
        try:
            prices = json.loads(m.get("outcomePrices") or "[]")
            prob = float(prices[0]) if prices else None
        except (ValueError, json.JSONDecodeError, IndexError):
            prob = None
        if prob is None:
            continue
        new_probs[slug] = prob
        change_1d = None
        if slug in prev_probs:
            change_1d = round(prob - prev_probs[slug], 4)
        matched += 1
        if matched > 10:
            break
        cards.append(
            {
                "kind": "event",
                "level": "market",
                "category": source["category"],
                "source_tier": source["tier"],
                "source_id": sid,
                "title": strip_html(m.get("question", ""), limit=200),
                "url": f"https://polymarket.com/event/{slug}",
                "published_at": None,
                "lang": "en",
                "summary_raw": strip_html(m.get("description", ""), limit=400),
                "data": {
                    "series": slug,
                    "value": round(prob, 4),
                    "change_1d": change_1d,
                    "threshold": 0.10,
                },
            }
        )
    state["polymarket_probs"] = new_probs
    return cards


# ── Kalshi（第二家預測市場；kind: kalshi）───────────────────────────────
def fetch_kalshi_source(source: dict, health: Health, state: dict) -> list[dict]:
    """建模同 fetch_polymarket_source：state-based 1 日機率變化卡、同一個
    change_1d 門檻（0.10）。跟 polymarket 的差異只在「怎麼選市場」——見
    KALSHI_SERIES 常數上方的註解：Kalshi 的泛用 /markets 清單以運動合約為主，
    關鍵字比對會誤中球員姓名子字串，所以改成逐一查經濟類 series_ticker，
    每個 event_ticker 只取機率最接近 0.5（資訊量最大）的一檔代表，避免同一
    事件的多檔 strike（"above 5%"/"above 6%"/...）洗版。"""
    sid = source["id"]
    base_url = source["url"]
    all_markets = []
    ok_any = False
    last_status = None
    last_latency = None
    last_err = None
    for series in KALSHI_SERIES:
        sep = "&" if "?" in base_url else "?"
        url = f"{base_url}{sep}series_ticker={series}&status=open&limit=100"
        ok, status, latency_ms, text, err = http_get(url)
        last_status, last_latency, last_err = status, latency_ms, err
        if not ok:
            continue
        ok_any = True
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            continue
        all_markets.extend(data.get("markets") or [])

    if not ok_any:
        health.record(sid, False, last_status, last_latency, 0, last_err)
        return []
    health.record(sid, True, last_status, last_latency, len(all_markets))

    # 同一 event_ticker 只留機率最接近 0.5 的一檔（多 strike 事件的代表檔）。
    best_by_event: dict[str, dict] = {}
    for m in all_markets:
        # 已在查詢字串加 status=open，這裡不再重複判斷 m["status"]（Kalshi 用
        # "active" 標示可交易中，不是 "open"——踩過一次這個假設錯誤）。
        try:
            prob = float(m.get("last_price_dollars") or "nan")
        except (TypeError, ValueError):
            continue
        if prob != prob:  # NaN
            continue
        ev = m.get("event_ticker") or m.get("ticker")
        if not ev:
            continue
        dist = abs(prob - 0.5)
        prev = best_by_event.get(ev)
        if prev is None or dist < prev["_dist"]:
            m2 = dict(m)
            m2["_prob"] = prob
            m2["_dist"] = dist
            best_by_event[ev] = m2

    prev_probs = state.get("kalshi_probs", {})
    new_probs = {}
    cards = []
    # 依「離 0.5 最近」排序，資訊量最大的先進（跟 cap 一起決定誰被丟）。
    for ev, m in sorted(best_by_event.items(), key=lambda kv: kv[1]["_dist"]):
        ticker = m.get("ticker") or ev
        prob = round(m["_prob"], 4)
        new_probs[ticker] = prob
        change_1d = round(prob - prev_probs[ticker], 4) if ticker in prev_probs else None
        title = strip_html(m.get("title", ""), limit=200)
        sub = strip_html(m.get("yes_sub_title", "") or m.get("no_sub_title", ""), limit=200)
        cards.append(
            {
                "kind": "event",
                "level": "market",
                "category": source["category"],
                "source_tier": source["tier"],
                "source_id": sid,
                "title": title or ev,
                "url": f"https://kalshi.com/markets/{(m.get('event_ticker') or ev).split('-')[0].lower()}",
                "published_at": None,
                "lang": "en",
                "summary_raw": sub,
                "data": {
                    "series": ticker,
                    "value": prob,
                    "change_1d": change_1d,
                    "threshold": 0.10,
                },
            }
        )
        if len(cards) >= KALSHI_MAX_CARDS:
            break
    # 未進卡的市場機率仍寫回 state，下次才有基準算 change_1d。
    for ev, m in best_by_event.items():
        t = m.get("ticker") or ev
        new_probs.setdefault(t, round(m["_prob"], 4))
    state["kalshi_probs"] = new_probs
    return cards


# ── PTT Stock 板（小道消息／傳聞層，kind: ptt，2026-08-20 新增）───────────
try:
    from bs4 import BeautifulSoup as _BS4
except ImportError:  # pragma: no cover — beautifulsoup4 已是站內既有依賴（yfinance 帶入）
    _BS4 = None

PTT_MIN_PUSH = 30  # 只收推文「爆」或 ≥30 篇（DESIGN 2026-08-20 傳聞層試行規則）
PTT_CATEGORY_RE = re.compile(r"^\s*\[([^\]]{1,10})\]\s*")


def fetch_ptt_source(source: dict, health: Health) -> list[dict]:
    """PTT Stock 板：抓最新 2 頁（index.html ＋「‹ 上頁」連結），只收推文數
    「爆」或 ≥30 的文章；標題去掉 [分類] 前綴（保留進 tags.themes）；連結組
    https://www.ptt.cc + href；PTT 版面沒有逐篇時間戳，published_at 一律
    None（呼叫端統一補 fetched_at，first_seen_filter 會用「第一次看到」判新舊）。
    需要 cookie over18=1（分齡確認）；沒裝 beautifulsoup4 就整條跳過。"""
    sid = source["id"]
    if _BS4 is None:
        health.record(sid, False, None, None, 0, "beautifulsoup4 not installed")
        return []
    base_url = source["url"]
    ua = source.get("ua", UA)
    cookies = {"over18": "1"}

    ok, status, latency_ms, text, err = http_get(base_url, ua=ua, cookies=cookies)
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    total_latency = latency_ms
    texts = [text]
    try:
        soup0 = _BS4(text, "lxml")
        prev_href = None
        for a in soup0.select(".action-bar a.btn.wide"):
            if a.get_text(strip=True) == "‹ 上頁" and a.get("href"):
                prev_href = a["href"]
                break
        if prev_href:
            prev_url = urljoin(base_url, prev_href)
            ok2, status2, latency2, text2, err2 = http_get(prev_url, ua=ua, cookies=cookies)
            if ok2:
                texts.append(text2)
                total_latency = (total_latency or 0) + (latency2 or 0)
    except Exception:  # noqa: BLE001 — 拿不到第二頁不影響第一頁的結果
        pass

    scored: list[tuple[bool, int, dict]] = []
    for page_text in texts:
        try:
            soup = _BS4(page_text, "lxml")
        except Exception:  # noqa: BLE001
            continue
        for ent in soup.select("div.r-ent"):
            title_a = ent.select_one("div.title a")
            if not title_a:
                continue  # 已刪除文章（標題欄無 <a>）
            href = title_a.get("href") or ""
            if not href:
                continue
            raw_title = strip_html(title_a.get_text(strip=True), limit=200)
            nrec = ent.select_one("div.nrec")
            push_text = (nrec.get_text(strip=True) if nrec else "").strip()
            is_bao = push_text == "爆"
            try:
                push_n = int(push_text)
            except ValueError:
                push_n = None
            if not (is_bao or (push_n is not None and push_n >= PTT_MIN_PUSH)):
                continue
            m = PTT_CATEGORY_RE.match(raw_title)
            cat_tag = m.group(1) if m else None
            title = raw_title[m.end():].strip() if m else raw_title
            link = urljoin(base_url, href)
            card = {
                "kind": "news",
                "level": source.get("level", "market"),
                "category": source["category"],
                "source_tier": source["tier"],
                "source_id": sid,
                "title": title or raw_title,
                "url": link,
                "published_at": None,  # PTT index 頁無逐篇時間戳（見上方 docstring）
                "lang": source.get("lang", "zh"),
                "summary_raw": (f"推文數 {push_text}" + (f"；分類 {cat_tag}" if cat_tag else "")),
                "tags": {"tickers": [], "themes": [cat_tag] if cat_tag else []},
            }
            rank_push = 999 if is_bao else (push_n or 0)
            scored.append((is_bao, rank_push, card))

    # 同一篇文章可能同時出現在「最新頁」與「上頁」（換頁時邊界重疊）——用連結去重。
    seen_urls: set = set()
    deduped: list[tuple[bool, int, dict]] = []
    for is_bao, rank, card in scored:
        if card["url"] in seen_urls:
            continue
        seen_urls.add(card["url"])
        deduped.append((is_bao, rank, card))

    deduped.sort(key=lambda x: (0 if x[0] else 1, -x[1]))
    max_items = source.get("max_items", 6)
    cards = [c for _, _, c in deduped[:max_items]]
    health.record(sid, True, status, total_latency, len(cards))
    return cards


# ── generic JSON 來源（Phase 1 僅健康檢查，不產卡；見 sources.yml note）──
def fetch_json_healthcheck_source(source: dict, health: Health) -> list[dict]:
    sid = source["id"]
    ok, status, latency_ms, text, err = http_get(source["url"])
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    try:
        data = json.loads(text)
        item_count = len(data) if isinstance(data, (list, dict)) else 1
    except json.JSONDecodeError as e:
        health.record(sid, False, status, latency_ms, 0, f"bad json: {e}")
        return []
    health.record(sid, True, status, latency_ms, item_count)
    return []


def fetch_html_source(source: dict, health: Health) -> list[dict]:
    sid = source["id"]
    ok, status, latency_ms, text, err = http_get(source["url"])
    health.record(sid, ok, status, latency_ms, 1 if ok else 0, err)
    return []


# ── 站內數字卡（monitor／regime／rotation／crowding／detective）零 LLM ──
def _load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def build_onsite_cards(state: dict) -> tuple[list[dict], dict]:
    cards = []
    updates = {}

    # 1) monitor/alerts.json 的 latest.json.alerts_today —— 上游已算好「今天新
    #    穿越門檻」的清單，本身就是 edge-triggered，不需要再對 state 去重。
    monitor = _load_json(ROOT / "docs" / "monitor" / "data" / "latest.json")
    if monitor:
        as_of = monitor.get("as_of")
        for a in monitor.get("alerts_today", []):
            cat = MONITOR_CAT_MAP.get(a.get("cat"), "regime")
            sev = a.get("sev", "yellow")
            title = f"[monitor] {a.get('key')}：{a.get('msg')}"
            cards.append(
                {
                    "kind": "data",
                    "level": "market",
                    "category": cat,
                    "source_tier": "T1",
                    "source_id": "onsite_monitor",
                    "title": title,
                    "url": "/monitor/",
                    "published_at": None,
                    "lang": "zh",
                    "summary_raw": a.get("msg", ""),
                    "data": {
                        "series": a.get("key"),
                        "rule": a.get("rule"),
                        "severity": sev,
                        "as_of": as_of,
                    },
                }
            )

    # 2) regime/latest.json —— composite label 變了才發卡（bootstrap 視為變了）。
    regime = _load_json(ROOT / "docs" / "regime" / "data" / "latest.json")
    if regime:
        composite = regime.get("composite", {})
        label = composite.get("label_zh") or composite.get("label_en")
        pos = composite.get("pos_0to1")
        prev_label = state.get("regime_composite_label")
        if label and label != prev_label:
            cards.append(
                {
                    "kind": "data",
                    "level": "market",
                    "category": "regime",
                    "source_tier": "T1",
                    "source_id": "onsite_regime",
                    "title": f"[regime] 跨市場 regime：{label}",
                    "url": "/regime/",
                    "published_at": None,
                    "lang": "zh",
                    "summary_raw": f"regime composite 由「{prev_label}」變為「{label}」"
                    if prev_label
                    else f"regime composite 首次記錄：{label}",
                    "data": {
                        "series": "regime_composite",
                        "value": pos,
                        "prev_label": prev_label,
                        "label": label,
                    },
                }
            )
        updates["regime_composite_label"] = label

    # 3) rotation/radar.json —— cross_asset 最新一筆的領先象限（G/I/L/W 計數最
    #    大者）變了才發卡。
    rotation = _load_json(ROOT / "docs" / "rotation" / "data" / "radar.json")
    if rotation:
        try:
            frames = rotation["breadth"]["cross_asset"]["120"]
            latest = frames[-1]
            letters = {k: latest.get(k, 0) for k in ("G", "I", "L", "W")}
            leader = max(letters, key=letters.get)
        except (KeyError, IndexError, ValueError, TypeError):
            leader = None
        prev_leader = state.get("rotation_leader")
        if leader and leader != prev_leader:
            cards.append(
                {
                    "kind": "data",
                    "level": "market",
                    "category": "regime",
                    "source_tier": "T1",
                    "source_id": "onsite_rotation",
                    "title": f"[rotation] 輪動雷達領先象限轉為 {leader}",
                    "url": "/rotation/radar.html",
                    "published_at": None,
                    "lang": "zh",
                    "summary_raw": f"跨資產輪動領先象限由「{prev_leader}」轉為「{leader}」"
                    if prev_leader
                    else f"跨資產輪動領先象限首次記錄：{leader}",
                    "data": {"series": "rotation_leader", "value": leader, "prev": prev_leader},
                }
            )
        if leader:
            updates["rotation_leader"] = leader

    # 4) crowding/latest.json —— COT 5y 分位進入 <=10 / >=90 極端（edge-trigger）
    #    ＋ 主題龍頭換人。
    crowding = _load_json(ROOT / "docs" / "crowding" / "data" / "latest.json")
    if crowding:
        prev_extremes = set(state.get("crowding_extremes", []))
        cur_extremes = set()
        for c in crowding.get("cot", []):
            p = c.get("pctile_5y")
            if p is None:
                continue
            if p >= 90 or p <= 10:
                key = f"cot:{c.get('market')}"
                cur_extremes.add(key)
                if key not in prev_extremes:
                    cards.append(
                        {
                            "kind": "data",
                            "level": "market",
                            "category": "positioning",
                            "source_tier": "T1",
                            "source_id": "onsite_crowding",
                            "title": f"[crowding] {c.get('market')} 部位進入極端（5y 分位 {p}，{c.get('direction')}）",
                            "url": "/crowding/",
                            "published_at": None,
                            "lang": "zh",
                            "summary_raw": f"{c.get('market')} CFTC 淨部位 5 年分位 {p}，方向 {c.get('direction')}",
                            "data": {
                                "series": key,
                                "value": p,
                                "threshold": 90 if p >= 90 else 10,
                                "pctile": p,
                            },
                        }
                    )
        updates["crowding_extremes"] = sorted(cur_extremes)

        themes = crowding.get("themes", [])
        top_theme = themes[0]["name"] if themes else None
        prev_top = state.get("crowding_top_theme")
        if top_theme and top_theme != prev_top:
            cards.append(
                {
                    "kind": "data",
                    "level": "market",
                    "category": "positioning",
                    "source_tier": "T1",
                    "source_id": "onsite_crowding",
                    "title": f"[crowding] 最擁擠主題換人：{top_theme}",
                    "url": "/crowding/",
                    "published_at": None,
                    "lang": "zh",
                    "summary_raw": f"擁擠度排名第一主題由「{prev_top}」變為「{top_theme}」"
                    if prev_top
                    else f"擁擠度排名第一主題首次記錄：{top_theme}",
                    "data": {"series": "crowding_top_theme", "value": top_theme, "prev": prev_top},
                }
            )
        if top_theme:
            updates["crowding_top_theme"] = top_theme

    # 5) detective/kill_watch.json —— near 新進榜者發卡；breached 全部發卡
    #    （論點連結，§0 三核心之一：對著論點看）。
    kw = _load_json(ROOT / "docs" / "detective" / "data" / "kill_watch.json")
    if kw:
        items_by_id = {it.get("id"): it for it in kw.get("items", [])}
        near_ids = set(kw.get("near", []))
        breached_ids = set(kw.get("breached", []))
        prev_near = set(state.get("kill_watch_near_ids", []))

        def _kill_card(item_id, status_label):
            it = items_by_id.get(item_id, {})
            return {
                "kind": "data",
                "level": "market",
                "category": "regime",
                "source_tier": "T1",
                "source_id": "onsite_detective",
                "title": f"[kill-watch] {status_label}：{it.get('theme', item_id)} — {it.get('metric_text', '')}",
                "url": "/detective/",
                "published_at": None,
                "lang": "zh",
                "summary_raw": it.get("threshold_text", "")[:400],
                "data": {
                    "series": item_id,
                    "value": it.get("current"),
                    "threshold": it.get("value"),
                    "op": it.get("op"),
                    "status": it.get("status"),
                    "doc": it.get("doc"),
                    "theme": it.get("theme", item_id),
                    "metric_text": it.get("metric_text", ""),
                },
            }

        for item_id in sorted(near_ids - prev_near):
            cards.append(_kill_card(item_id, "kill metric 接近閾值"))
        for item_id in sorted(breached_ids):
            cards.append(_kill_card(item_id, "kill metric 已突破"))

        updates["kill_watch_near_ids"] = sorted(near_ids)
        updates["kill_watch_breached_ids"] = sorted(breached_ids)

    return cards, updates


# ── 去重 ─────────────────────────────────────────────────────────────────
def dedup_cards(cards: list[dict]) -> list[dict]:
    """URL 精確去重＋標題相似度近重複合併。**只對 kind=="news" 做**——data／
    event 卡（含站內數字卡）常共用同一個站內區塊 url（如 "/monitor/"），且每
    張本來就代表獨立的一筆門檻事件，不該被當成同一篇報導的轉載去重掉。"""
    news = [c for c in cards if c.get("kind") == "news"]
    non_news = [c for c in cards if c.get("kind") != "news"]
    for c in non_news:
        c["corroboration"] = c.get("corroboration", 1)

    seen_urls: dict[str, dict] = {}
    ordered: list[dict] = []
    for c in news:
        url = c.get("url") or ""
        key = url if url.startswith("http") else None
        if key and key in seen_urls:
            primary = seen_urls[key]
            primary["corroboration"] = primary.get("corroboration", 1) + 1
            continue
        c["corroboration"] = c.get("corroboration", 1)
        c["_tokens"] = norm_title_tokens(c.get("title", ""))
        if key:
            seen_urls[key] = c
        ordered.append(c)

    # 標題相似度近重複（同日、jaccard >= 0.85）：merge 進較高 tier 的那則。
    merged: list[dict] = list(non_news)
    used = [False] * len(ordered)
    for i, c in enumerate(ordered):
        if used[i]:
            continue
        group = [i]
        for j in range(i + 1, len(ordered)):
            if used[j]:
                continue
            other = ordered[j]
            if c.get("published_at") and other.get("published_at"):
                if c["published_at"][:10] != other["published_at"][:10]:
                    continue
            if jaccard(c["_tokens"], other["_tokens"]) >= DEDUP_JACCARD:
                group.append(j)
        for j in group:
            used[j] = True
        if len(group) == 1:
            merged.append(c)
            continue
        candidates = [ordered[j] for j in group]
        candidates.sort(key=lambda x: TIER_RANK.get(x["source_tier"], 9))
        primary = candidates[0]
        source_ids = {x["source_id"] for x in candidates}
        primary["corroboration"] = len(source_ids)
        merged.append(primary)

    for c in merged:
        c.pop("_tokens", None)

    # 第二段（2026-08-19 新增）：跨來源較寬鬆合併（jaccard >= DEDUP_JACCARD_CROSS，
    # 同日），只在其中一則來自 Google News 聚合（source_id 前綴 gnews_）時觸發
    # ——目的是讓 Google News 命中的同一則報導併入已存在的直接來源卡（記
    # corroboration+1），不因措辭不同而在頁面上重複出現；不對兩則「都不是
    # gnews」的卡片套用這條寬鬆門檻，避免不同事件因用詞相近被誤併。
    news2 = [c for c in merged if c.get("kind") == "news"]
    rest2 = [c for c in merged if c.get("kind") != "news"]
    for c in news2:
        c["_tokens2"] = norm_title_tokens(c.get("title", ""))

    used2 = [False] * len(news2)
    final_news: list[dict] = []
    for i, c in enumerate(news2):
        if used2[i]:
            continue
        group = [i]
        for j in range(i + 1, len(news2)):
            if used2[j]:
                continue
            other = news2[j]
            if c.get("source_id") == other.get("source_id"):
                continue
            is_gnews_pair = (c.get("source_id") or "").startswith("gnews_") or (
                other.get("source_id") or ""
            ).startswith("gnews_")
            if not is_gnews_pair:
                continue
            if c.get("published_at") and other.get("published_at"):
                if c["published_at"][:10] != other["published_at"][:10]:
                    continue
            if jaccard(c["_tokens2"], other["_tokens2"]) >= DEDUP_JACCARD_CROSS:
                group.append(j)
        for j in group:
            used2[j] = True
        if len(group) == 1:
            final_news.append(c)
            continue
        candidates = [news2[j] for j in group]
        candidates.sort(key=lambda x: TIER_RANK.get(x["source_tier"], 9))
        primary = candidates[0]
        source_ids = {x.get("source_id") for x in candidates}
        primary["corroboration"] = max(primary.get("corroboration", 1), len(source_ids))
        final_news.append(primary)

    for c in final_news:
        c.pop("_tokens2", None)

    return rest2 + final_news


# ── 新鮮度 ───────────────────────────────────────────────────────────────
def freshness_filter(cards: list[dict], now: datetime) -> tuple[list[dict], int]:
    kept = []
    dropped = 0
    cutoff = now - timedelta(hours=FRESHNESS_HOURS)
    for c in cards:
        if c.get("kind") == "data":
            kept.append(c)
            continue
        # 2026-08-19：低頻官方來源（EIA 週報、RBI）可在 sources.yml 設 max_age_hours
        # 放寬新鮮度窗；沒設就用全域 36h。
        src_hours = c.get("_max_age_hours")
        cutoff = now - timedelta(hours=src_hours if src_hours else FRESHNESS_HOURS)
        pub = c.get("published_at")
        if not pub:
            kept.append(c)  # 沒有時間戳的保留，交給人工／後續 stage 判斷
            continue
        try:
            pub_dt = datetime.strptime(pub, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            kept.append(c)
            continue
        if pub_dt < cutoff:
            dropped += 1
            continue
        kept.append(c)
    return kept, dropped


# ── 沒有時間戳的新聞：靠「第一次看到」判新舊 ────────────────────────────
SEEN_KEEP_DAYS = 7


def first_seen_filter(cards: list[dict], state: dict, now: datetime) -> tuple[list[dict], int]:
    """沒有 published_at 的 news（例：Nikkei Asia RSS 無日期）：state.json 記住
    看過的 id；之後只留第一次出現的。首跑全部視為新（bootstrap）。有日期的不動。"""
    seen: dict = state.get("seen_news", {})
    cutoff = iso(now - timedelta(days=SEEN_KEEP_DAYS))
    seen = {k: v for k, v in seen.items() if v >= cutoff}
    kept, dropped = [], 0
    for c in cards:
        if c.get("kind") != "news" or c.get("published_at"):
            kept.append(c)
            continue
        if c["id"] in seen:
            dropped += 1
            continue
        c["first_seen_at"] = iso(now)
        kept.append(c)
        seen[c["id"]] = iso(now)
    state["seen_news"] = seen
    return kept, dropped


# ── 關鍵字預過濾 ─────────────────────────────────────────────────────────
def deny_list_filter(cards: list[dict]) -> tuple[list[dict], int]:
    kept = []
    dropped = 0
    for c in cards:
        text = f"{c.get('title', '')} {c.get('summary_raw', '')}".lower()
        if any(k in text for k in DENY_KEYWORDS):
            dropped += 1
            continue
        kept.append(c)
    return kept, dropped


def priority_key(c: dict):
    """排序鍵：tier 升序 → corroboration 降序 → data 卡優先於 news/event
    （門檻事件比一般新聞重要）→ 有時間戳的優先、且新的在前 → id 兜底穩定排序。
    """
    pub = c.get("published_at") or ""
    has_pub = 0 if pub else 1
    pub_desc = tuple(-ord(ch) for ch in pub) if pub else ()
    return (
        TIER_RANK.get(c.get("source_tier"), 9),
        -c.get("corroboration", 1),
        c.get("kind") != "data",
        has_pub,
        pub_desc,
        c.get("id", ""),
    )


SOURCE_FLOOR = 3  # 2026-08-19：每個來源至少保 3 則（最新優先），T3 才不會被 T1/T2 大量擠光


def cap_and_sort(cards: list[dict]) -> tuple[list[dict], int]:
    cards.sort(key=priority_key)
    if len(cards) <= MAX_KEPT:
        return cards, 0
    floor_ids, per_src = set(), {}
    for c in cards:  # 已依 tier/新舊排序，每來源取前 SOURCE_FLOOR 則
        sid = c.get("source_id", "")
        if per_src.get(sid, 0) < SOURCE_FLOOR:
            per_src[sid] = per_src.get(sid, 0) + 1
            floor_ids.add(c.get("id"))
    floor = [c for c in cards if c.get("id") in floor_ids]
    rest = [c for c in cards if c.get("id") not in floor_ids]
    kept = (floor + rest)[:MAX_KEPT]
    kept.sort(key=priority_key)
    return kept, len(cards) - len(kept)


# ── 連結存活檢查 ─────────────────────────────────────────────────────────
def _check_one_link(card: dict) -> bool:
    url = card.get("url") or ""
    if not url.startswith("http"):
        return True  # 站內相對路徑（onsite 卡）不對外檢查
    try:
        resp = requests.head(
            url, headers={"User-Agent": UA}, timeout=LINK_CHECK_TIMEOUT, allow_redirects=True
        )
        if resp.status_code >= 400 or resp.status_code == 405:
            resp = requests.get(
                url,
                headers={"User-Agent": UA},
                timeout=LINK_CHECK_TIMEOUT,
                allow_redirects=True,
                stream=True,
            )
        return resp.status_code < 400
    except requests.RequestException:
        return False


def link_check(cards: list[dict]) -> None:
    top = cards[:LINK_CHECK_TOP_N]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(_check_one_link, top))
    for c, ok in zip(top, results):
        c["checks"] = {"link_ok": ok}
    for c in cards[LINK_CHECK_TOP_N:]:
        c["checks"] = {"link_ok": None}


# ── main ─────────────────────────────────────────────────────────────────
def load_sources() -> list[dict]:
    with open(SOURCES_YML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dispatch_source(source: dict, health: Health, state: dict) -> list[dict]:
    cards = _dispatch_source(source, health, state)
    if source.get("max_age_hours"):
        for c in cards:
            c["_max_age_hours"] = float(source["max_age_hours"])
    if source.get("rumor"):
        # 2026-08-20 傳聞層試行：非底線欄位，_strip_private 不會剝掉，會隨卡片
        # 一路傳到 classify/summarize/render，供各層過濾傳聞卡不進主摘要。
        for c in cards:
            c["source_rumor"] = True
    return cards


def _dispatch_source(source: dict, health: Health, state: dict) -> list[dict]:
    kind = source["kind"]
    if kind == "rss":
        return fetch_rss_source(source, health)
    if kind == "gnews":
        return fetch_gnews_source(source, health)
    if kind == "csv":
        return fetch_fred_source(source, health, state)
    if kind == "json":
        if source["id"] == "polymarket_markets":
            return fetch_polymarket_source(source, health, state)
        return fetch_json_healthcheck_source(source, health)
    if kind == "html":
        return fetch_html_source(source, health)
    if kind == "sec_8k":
        return sec_filings.fetch_sec_8k_source(source, health)
    if kind == "kalshi":
        return fetch_kalshi_source(source, health, state)
    if kind == "ptt":
        return fetch_ptt_source(source, health)
    # kind == "ff_calendar" 不回傳卡片，main() 另外用 fetch_ff_calendar() 呼叫。
    return []


def _strip_private(pending):
    for c in (pending.get("cards") or []) if isinstance(pending, dict) else []:
        c.pop("_max_age_hours", None)
    return pending


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default=None, help="只跑單一 source id（或 'onsite'）")
    ap.add_argument("--out", default=None,
                     help="覆寫 pending JSON 輸出路徑（測試用，預設 docs/intel/pending/{date}.json）")
    ap.add_argument("--health-out", default=None,
                     help="覆寫 sources_health.json 輸出路徑（測試用，預設 docs/intel/data/sources_health.json）")
    ap.add_argument("--calendar-out", default=None,
                     help="覆寫 ff_calendar.json 輸出路徑（測試用，預設 docs/intel/data/ff_calendar.json）")
    ap.add_argument("--state-file", default=None,
                     help="覆寫 state.json 讀寫路徑（測試用，預設 docs/intel/data/state.json，"
                          "避免測試跑污染正式 first-seen/FRED band/polymarket 狀態）")
    args = ap.parse_args()

    state_file = Path(args.state_file) if args.state_file else STATE_FILE

    now = now_utc()
    sources = load_sources()
    health = Health()
    state = _load_json(state_file) or {}

    fetched_cards: list[dict] = []
    calendar_entries: list[dict] = []
    attempted = 0
    for source in sources:
        if not source.get("enabled", False):
            continue
        if args.only and source["id"] != args.only:
            continue
        attempted += 1
        try:
            if source["kind"] == "ff_calendar":
                calendar_entries.extend(fetch_ff_calendar(source, health))
                continue
            fetched_cards.extend(dispatch_source(source, health, state))
        except Exception as e:  # noqa: BLE001 — 單一來源壞掉不能拖垮整批
            health.record(source["id"], False, None, None, 0, f"unhandled: {e}")

    onsite_updates = {}
    if args.only is None or args.only == "onsite":
        onsite_cards, onsite_updates = build_onsite_cards(state)
        fetched_cards.extend(onsite_cards)

    total_fetched = len(fetched_cards)

    for c in fetched_cards:
        url = c.get("url") or ""
        if c.get("kind") == "news" and url.startswith("http"):
            basis = url
        else:
            # data/event 卡（含站內數字卡）常共用同一個站內區塊 url（如
            # "/monitor/"），不能拿 url 當唯一性依據，一律用 source+title+日期。
            basis = f"{c.get('source_id')}|{c.get('title')}|{args.date}"
        c["id"] = sha1_id(basis)
        c["fetched_at"] = iso(now)
        c.setdefault("published_at", None)

    deduped = dedup_cards(fetched_cards)
    dup_dropped = total_fetched - len(deduped)

    fresh, stale_dropped = freshness_filter(deduped, now)
    fresh, unseen_dropped = first_seen_filter(fresh, state, now)
    allowed, deny_dropped = deny_list_filter(fresh)
    kept, cap_dropped = cap_and_sort(allowed)

    link_check(kept)

    ok_sources = sum(1 for r in health.records if r["ok"])
    fail_sources = sum(1 for r in health.records if not r["ok"])

    pending = {
        "meta": {
            "date": args.date,
            "generated_at": iso(now),
            "counts": {
                "fetched": total_fetched,
                "kept": len(kept),
                "dropped_by": {
                    "duplicate": dup_dropped,
                    "stale": stale_dropped,
                    "seen_before": unseen_dropped,
                    "deny_list": deny_dropped,
                    "over_cap": cap_dropped,
                },
            },
            "sources_ok": ok_sources,
            "sources_fail": fail_sources,
        },
        "cards": kept,
    }

    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    health_out = {
        "schema": "intel-sources-health-v1",
        "date": args.date,
        "generated_at": iso(now),
        "sources": health.records,
    }

    calendar_out = {
        "schema": "intel-ff-calendar-v1",
        "date": args.date,
        "generated_at": iso(now),
        "events": calendar_entries,
    }

    if not args.dry_run:
        pending_out_path = Path(args.out) if args.out else (PENDING_DIR / f"{args.date}.json")
        health_out_path = Path(args.health_out) if args.health_out else HEALTH_FILE
        calendar_out_path = Path(args.calendar_out) if args.calendar_out else (DATA_DIR / "ff_calendar.json")
        pending_out_path.parent.mkdir(parents=True, exist_ok=True)
        health_out_path.parent.mkdir(parents=True, exist_ok=True)
        calendar_out_path.parent.mkdir(parents=True, exist_ok=True)
        pending_out_path.write_text(
            json.dumps(_strip_private(pending), ensure_ascii=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        health_out_path.write_text(
            json.dumps(health_out, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        calendar_out_path.write_text(
            json.dumps(calendar_out, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        state.update(onsite_updates)  # polymarket_probs 已由 fetch_polymarket_source 直接寫回 state dict
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(
            json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(
        f"[intel/fetch] date={args.date} attempted_sources={attempted} "
        f"ok={ok_sources} fail={fail_sources} fetched={total_fetched} kept={len(kept)} "
        f"calendar_entries={len(calendar_entries)} "
        f"dropped(dup={dup_dropped},stale={stale_dropped},seen={unseen_dropped},deny={deny_dropped},cap={cap_dropped})"
    )

    if attempted > 0 and fail_sources > attempted / 2:
        print(
            f"[intel/fetch] WARNING: {fail_sources}/{attempted} attempted sources failed "
            "(>50%) — exiting non-zero for GHA visibility, pending JSON still written.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
