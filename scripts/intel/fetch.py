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
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests
import yaml

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
MAX_KEPT = 200
DEDUP_JACCARD = 0.85

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


def http_get(url: str, retries: int = 1, timeout: int = TIMEOUT):
    """GET with a single retry. Returns (ok, status, latency_ms, text_or_none, error_or_none)."""
    last_err = None
    for attempt in range(retries + 1):
        t0 = time.time()
        try:
            resp = requests.get(
                url, headers={"User-Agent": UA, "Accept": "*/*"}, timeout=timeout
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
    ok, status, latency_ms, text, err = http_get(source["url"])
    if not ok:
        health.record(sid, False, status, latency_ms, 0, err)
        return []
    parsed = feedparser.parse(text)
    entries = parsed.entries[: source.get("max_items", 30)]
    cards = []
    for e in entries:
        title = strip_html(e.get("title", ""), limit=200)
        link = e.get("link", "") or ""
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
    return merged


# ── 新鮮度 ───────────────────────────────────────────────────────────────
def freshness_filter(cards: list[dict], now: datetime) -> tuple[list[dict], int]:
    kept = []
    dropped = 0
    cutoff = now - timedelta(hours=FRESHNESS_HOURS)
    for c in cards:
        if c.get("kind") == "data":
            kept.append(c)
            continue
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


def cap_and_sort(cards: list[dict]) -> tuple[list[dict], int]:
    cards.sort(key=priority_key)
    if len(cards) <= MAX_KEPT:
        return cards, 0
    dropped = len(cards) - MAX_KEPT
    return cards[:MAX_KEPT], dropped


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
    kind = source["kind"]
    if kind == "rss":
        return fetch_rss_source(source, health)
    if kind == "csv":
        return fetch_fred_source(source, health, state)
    if kind == "json":
        if source["id"] == "polymarket_markets":
            return fetch_polymarket_source(source, health, state)
        return fetch_json_healthcheck_source(source, health)
    if kind == "html":
        return fetch_html_source(source, health)
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default=None, help="只跑單一 source id（或 'onsite'）")
    args = ap.parse_args()

    now = now_utc()
    sources = load_sources()
    health = Health()
    state = _load_json(STATE_FILE) or {}

    fetched_cards: list[dict] = []
    attempted = 0
    for source in sources:
        if not source.get("enabled", False):
            continue
        if args.only and source["id"] != args.only:
            continue
        attempted += 1
        try:
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

    if not args.dry_run:
        pending_path = PENDING_DIR / f"{args.date}.json"
        pending_path.write_text(
            json.dumps(pending, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        HEALTH_FILE.write_text(
            json.dumps(health_out, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        state.update(onsite_updates)  # polymarket_probs 已由 fetch_polymarket_source 直接寫回 state dict
        STATE_FILE.write_text(
            json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(
        f"[intel/fetch] date={args.date} attempted_sources={attempted} "
        f"ok={ok_sources} fail={fail_sources} fetched={total_fetched} kept={len(kept)} "
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
