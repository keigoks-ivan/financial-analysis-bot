#!/usr/bin/env python3
"""scripts/intel/threads.py — 故事串連（story threads）。

對應 notes/site-internal/intel/DESIGN.md 2026-08-19「加料」計畫第 2 項。把
每天分散的卡片，串成跨日的「故事線」（同一件事今天有 3 則、昨天有 5 則、
正在冷卻中…），狀態存在 `docs/intel/data/threads.json`（schema
`intel-threads-v1`）。

指派管道分兩條（設計上刻意不為此再燒一次獨立的 LLM 呼叫）：
1. **sonnet 路徑**（零額外呼叫）——summarize.py 既有的 sonnet 摘要批次呼叫
   已經把「目前活躍中的 thread 清單」塞進 payload，模型回傳的每張卡多帶一個
   `thread: {match, new_title_zh, keywords}`（見 summarize.py／
   prompts/summarize.md）。本模組讀 `card["_thread_proposal"]` 消化這個結果。
2. **機械路徑**（zero LLM）——沒進 sonnet 的 title-only（passthrough）卡片，
   用卡片自身的 `tags.tickers` + `tags.themes` 當「關鍵字集合」，跟現有活躍
   thread 的 keywords 做重疊比對（不分大小寫、CJK 用子字串比對），重疊 ≥2
   個才算命中——機械路徑只能「加入」既有 thread，不能「新建」thread（新建
   只走 sonnet 路徑，避免在沒有模型判斷的情況下無限增生）。

呼叫順序（run_daily.py）：
    state = threads.load_state()
    active = threads.active_thread_list(state)          # 餵給 summarize 的 prompt
    summarized = summarize_cards(selected, ledger, active_threads=active)
    passthrough = [...]
    raw_cards = summarized["cards"] + passthrough
    threads.assign_mechanical(passthrough, state)        # 機械路徑，改 raw_cards 裡的 dict
    output = threads.merge_daily(date, raw_cards, state)  # sonnet 路徑 + 計數/熱度/冷卻，改 state 與 raw_cards
    threads.save_state(state)
    finalized = [finalize_card(c, ...) for c in raw_cards]  # finalize_card 需帶出 c["thread_id"]

`merge_daily()` 回傳的 `output` 就是當日 JSON 的 `threads` 欄位（top 12，含
sparkline）；`state`（含全部 ≤60 條 thread 的完整歷史）另外持久化，不進日輸出
JSON（避免每天重複整份歷史膨脹 daily JSON）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta

from common import ROOT, load_json

THREADS_PATH = ROOT / "docs" / "intel" / "data" / "threads.json"
SCHEMA = "intel-threads-v1"

MAX_THREADS = 60
MAX_DAILY_COUNTS_DAYS = 30
MAX_CARD_IDS_LATEST = 5
COOLING_AFTER_ZERO_DAYS = 5
DROP_AFTER_ZERO_DAYS = 14
ACTIVE_THREAD_LIST_LIMIT = 40  # 給 summarize prompt 用的緊湊清單上限
OUTPUT_TOP_N = 12
SPARKLINE_DAYS = 14
NEW_THREAD_JACCARD = 0.5
EXISTING_THREAD_JACCARD = 0.34  # 新建提議 vs 既有 thread 的併線門檻
MECH_MATCH_MIN_OVERLAP = 2


# ── state io ─────────────────────────────────────────────────────────────────
def load_state() -> dict:
    data = load_json(THREADS_PATH)
    if not isinstance(data, dict) or not isinstance(data.get("threads"), list):
        return {"schema": SCHEMA, "threads": []}
    return data


def save_state(state: dict) -> None:
    THREADS_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["schema"] = SCHEMA
    with open(THREADS_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


def active_thread_list(state: dict, limit: int = ACTIVE_THREAD_LIST_LIMIT) -> list[dict]:
    """給 summarize 批次 prompt 用的緊湊清單——active／cooling 都給（cooling
    的 thread 若今天又有新卡命中，merge_daily 會把它翻回 active），dropped
    的不給（等於真的死了）。"""
    pool = [t for t in state.get("threads", []) if t.get("status") in ("active", "cooling")]
    pool.sort(key=lambda t: t.get("last_seen") or "", reverse=True)
    return [
        {"id": t.get("id"), "title_zh": t.get("title_zh", ""), "keywords": t.get("keywords", [])}
        for t in pool[:limit]
    ]


# ── helpers ──────────────────────────────────────────────────────────────────
def _safe_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _jaccard(a: set, b: set) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _new_thread_id(date: str, title_zh: str) -> str:
    h = hashlib.sha1(f"{date}|{title_zh}".encode("utf-8")).hexdigest()[:10]
    return f"th_{h}"


def _trim_daily_counts(t: dict, date: str) -> None:
    d0 = _safe_date(date)
    if d0 is None:
        return
    cutoff = d0 - timedelta(days=MAX_DAILY_COUNTS_DAYS - 1)
    t["daily_counts"] = {
        d: n for d, n in t.get("daily_counts", {}).items()
        if _safe_date(d) is not None and _safe_date(d) >= cutoff
    }


def _compute_heat(t: dict, date: str) -> str:
    """「今日 vs 前 3 天均值」——today>=3 且 (前 3 天均值為 0 或 today>=2x均值)
    視為 up；最近 2 天（含今日）都是 0 視為 down；其餘 flat。"""
    d0 = _safe_date(date)
    if d0 is None:
        return "flat"
    counts = t.get("daily_counts", {})
    today_n = counts.get(date, 0)
    last2 = [(d0 - timedelta(days=i)).isoformat() for i in range(0, 2)]
    if all(counts.get(d, 0) == 0 for d in last2):
        return "down"
    prior_days = [(d0 - timedelta(days=i)).isoformat() for i in range(1, 4)]
    prior_vals = [counts.get(d, 0) for d in prior_days]
    prior_mean = sum(prior_vals) / len(prior_vals) if prior_vals else 0.0
    if today_n >= 3 and (prior_mean == 0 or today_n >= 2 * prior_mean):
        return "up"
    return "flat"


def _consecutive_zero_days(t: dict, date: str) -> int:
    d0 = _safe_date(date)
    if d0 is None:
        return 0
    counts = t.get("daily_counts", {})
    n = 0
    d = d0
    while counts.get(d.isoformat(), 0) == 0:
        n += 1
        d -= timedelta(days=1)
        if n > MAX_DAILY_COUNTS_DAYS:
            break
    return n


def _sparkline(t: dict, date: str, days: int = SPARKLINE_DAYS) -> list:
    d0 = _safe_date(date)
    if d0 is None:
        return [0] * days
    counts = t.get("daily_counts", {})
    return [counts.get((d0 - timedelta(days=i)).isoformat(), 0) for i in range(days - 1, -1, -1)]


def _day_count(first_seen: str, date: str) -> int:
    d0, d1 = _safe_date(first_seen), _safe_date(date)
    if d0 is None or d1 is None:
        return 1
    return max(1, (d1 - d0).days + 1)


# ── mechanical path (title-only / passthrough cards) ────────────────────────
def assign_mechanical(cards: list[dict], state: dict) -> None:
    """對 title-only（passthrough）卡片，用 `tags.tickers`＋`tags.themes` 當
    關鍵字集合，跟現有 active thread 的 keywords 重疊比對；重疊 ≥2 個才命中，
    命中就直接寫 `card["thread_id"]`。只比對「加入既有 thread」，不新建。"""
    active = [t for t in state.get("threads", []) if t.get("status") == "active"]
    if not active:
        return
    thread_kw = [
        (t["id"], {k.strip().lower() for k in (t.get("keywords") or []) if isinstance(k, str) and k.strip()})
        for t in active
    ]
    for c in cards:
        if c.get("thread_id") or c.get("kind") == "data" or c.get("is_rumor"):
            continue  # 2026-08-20 傳聞層試行：傳聞卡不得進故事串連
        tags = c.get("tags") or {}
        card_kw = {
            str(v).strip().lower()
            for v in (list(tags.get("tickers") or []) + list(tags.get("themes") or []))
            if str(v).strip()
        }
        title_l = (c.get("title") or "").lower()
        if not card_kw:
            continue
        best_id, best_overlap = None, 0
        for tid, tkw in thread_kw:
            overlap = 0
            for k in tkw:
                if not k:
                    continue
                if k in card_kw:
                    overlap += 1
                elif len(k) >= 2 and (k in title_l or any(k in ck or ck in k for ck in card_kw)):
                    overlap += 1
            if overlap > best_overlap:
                best_overlap, best_id = overlap, tid
        if best_id and best_overlap >= MECH_MATCH_MIN_OVERLAP:
            c["thread_id"] = best_id


# ── sonnet path + daily merge ────────────────────────────────────────────────
def merge_daily(date: str, cards: list[dict], state: dict) -> list[dict]:
    """消化 sonnet 路徑的 `_thread_proposal`（match 既有／提議新建），機械路徑
    已經在 `assign_mechanical()` 先寫好的 `thread_id` 原樣保留；接著對*所有*
    今天有 thread_id 的卡片計數，更新每條 thread 的 daily_counts／heat／
    status／card_ids_latest，套用 60 條上限與 cooling/drop 規則，回傳當日輸出
    用的 top 12（含 14 天 sparkline）。"""
    threads_by_id = {t["id"]: t for t in state.get("threads", [])}

    # 1) sonnet 路徑：先處理有 match 既有 thread 的
    new_candidates = []
    for c in cards:
        if c.get("kind") == "data" or c.get("thread_id") or c.get("is_rumor"):
            continue  # 2026-08-20 傳聞層試行：傳聞卡不得進故事串連
        prop = c.get("_thread_proposal")
        if not prop:
            continue
        match_id = prop.get("match")
        if match_id and match_id in threads_by_id:
            c["thread_id"] = match_id
            continue
        if (prop.get("new_title_zh") or "").strip():
            # 2026-08-19：新建提議先跟「既有活躍 thread」比關鍵字（Jaccard ≥ 0.34）
            # ——sonnet 常把同一條故事換個標題再開一線（例：「美債長天期殖利率飆升」
            # vs「公債殖利率多年高點賣壓」），這裡機械兜底併回舊線。
            kw = {k.strip().lower() for k in (prop.get("keywords") or []) if isinstance(k, str) and k.strip()}
            best, best_j = None, 0.0
            for t in threads_by_id.values():
                if t.get("status") == "dropped":
                    continue
                j = _jaccard(kw, {k.lower() for k in t.get("keywords", [])})
                if j > best_j:
                    best, best_j = t, j
            if best is not None and best_j >= EXISTING_THREAD_JACCARD:
                c["thread_id"] = best["id"]
                continue
            new_candidates.append(c)

    # 2) 當日新建提議去重（keyword Jaccard >= 0.5 視為同一個新故事）
    groups: list[dict] = []
    for c in new_candidates:
        prop = c["_thread_proposal"]
        kw = {k.strip().lower() for k in (prop.get("keywords") or []) if isinstance(k, str) and k.strip()}
        target = None
        for g in groups:
            if _jaccard(kw, g["keywords"]) >= NEW_THREAD_JACCARD:
                target = g
                break
        if target is None:
            target = {"title_zh": prop["new_title_zh"].strip()[:18], "keywords": set(kw), "cards": []}
            groups.append(target)
        else:
            target["keywords"] |= kw
        target["cards"].append(c)

    # 3) 實例化新 thread（受 60 條上限保護；額滿就不建新的，卡片留無 thread_id）
    for g in groups:
        if len(threads_by_id) >= MAX_THREADS:
            continue
        tid = _new_thread_id(date, g["title_zh"])
        while tid in threads_by_id:  # 極小機率碰撞（同天同標題）——退化成加序號
            tid = tid + "x"
        thread = {
            "id": tid,
            "title_zh": g["title_zh"],
            "keywords": sorted(g["keywords"])[:10],
            "category": (g["cards"][0].get("category") or ""),
            "first_seen": date,
            "last_seen": date,
            "daily_counts": {},
            "card_ids_latest": [],
            "status": "active",
            "heat": "flat",
        }
        threads_by_id[tid] = thread
        for c in g["cards"]:
            c["thread_id"] = tid

    # 4) 今日每條 thread 的命中卡數（機械路徑已寫好的 thread_id 也一併計入）
    counts_today: dict = {}
    for c in cards:
        tid = c.get("thread_id")
        if tid and tid in threads_by_id:
            counts_today[tid] = counts_today.get(tid, 0) + 1

    # 5) 更新每條 thread 的 daily_counts / status / heat（含今天沒中的 thread，
    #    才能正確累積 cooling/drop 的連續零天數）
    for tid, t in threads_by_id.items():
        t.setdefault("daily_counts", {})
        t["daily_counts"][date] = counts_today.get(tid, 0)
        _trim_daily_counts(t, date)
        n = t["daily_counts"].get(date, 0)
        if n > 0:
            t["last_seen"] = date
        t["heat"] = _compute_heat(t, date)
        zero_days = _consecutive_zero_days(t, date)
        if zero_days >= DROP_AFTER_ZERO_DAYS:
            t["status"] = "dropped"
        elif zero_days >= COOLING_AFTER_ZERO_DAYS:
            t["status"] = "cooling"
        elif n > 0:
            t["status"] = "active"
        # else: 介於 1..4 天零命中，維持原狀態不動（不用一天零命中就冷卻）

    # 6) card_ids_latest（保留最新 5 筆，同 id 覆蓋而非重複）
    for c in cards:
        tid = c.get("thread_id")
        if not tid or tid not in threads_by_id:
            continue
        t = threads_by_id[tid]
        entry = {"date": date, "id": c.get("id"), "title": c.get("title"), "url": c.get("url")}
        t["card_ids_latest"] = [e for e in t.get("card_ids_latest", []) if e.get("id") != c.get("id")]
        t["card_ids_latest"].insert(0, entry)
        t["card_ids_latest"] = t["card_ids_latest"][:MAX_CARD_IDS_LATEST]

    # 7) drop 掉的移除；超過 60 條時保留最近活躍的
    kept = [t for t in threads_by_id.values() if t.get("status") != "dropped"]
    kept.sort(key=lambda t: t.get("last_seen") or "", reverse=True)
    kept = kept[:MAX_THREADS]
    state["threads"] = kept
    state["schema"] = SCHEMA

    # 8) 輸出 top 12（active 優先，依今日命中數 desc、heat 排序）+ sparkline
    heat_rank = {"up": 0, "flat": 1, "down": 2}
    active = [t for t in kept if t.get("status") == "active"]
    active.sort(key=lambda t: (-t.get("daily_counts", {}).get(date, 0), heat_rank.get(t.get("heat"), 1)))
    output = []
    for t in active[:OUTPUT_TOP_N]:
        first_seen = t.get("first_seen") or date
        output.append({
            "id": t["id"],
            "title_zh": t.get("title_zh", ""),
            "keywords": t.get("keywords", []),
            "category": t.get("category", ""),
            "first_seen": first_seen,
            "last_seen": t.get("last_seen"),
            "day_n": _day_count(first_seen, date),
            "today_count": t.get("daily_counts", {}).get(date, 0),
            "heat": t.get("heat", "flat"),
            "status": t.get("status", "active"),
            "sparkline": _sparkline(t, date),
            "latest": t.get("card_ids_latest", [])[:3],
        })
    return output


# ── CLI (debug/verification only) ───────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default=str(THREADS_PATH))
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()
    state = load_json(args.state) or {"schema": SCHEMA, "threads": []}
    if args.show:
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        print(f"threads: {len(state.get('threads', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
