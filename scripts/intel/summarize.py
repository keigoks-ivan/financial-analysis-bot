#!/usr/bin/env python3
"""scripts/intel/summarize.py — Phase 1 stage 2: sonnet summarize/why/importance
+ the daily digest (gauges/brief_zh/flags) + calendar (pure Python, no LLM).

對應 notes/site-internal/intel/DESIGN.md §6（sonnet ≤60 條／日）／§7（正確性
五道，尤其規則 3：🔴 需 corroboration≥2 或 T1）／§8（T4 單獨不得 🔴）／
§11（卡片 schema）。

三件事：
1. `summarize_cards()` —— 對 stage 1 選出的 ≤60 張卡逐張補
   summary_zh/why_zh/importance/forecast。kind=="data" 的卡片沿用 §6「已結構化，
   零 LLM」原則，直接用 title 生成摘要，不進 sonnet。importance==3 的卡片，
   Python 強制檢查 corroboration>=2 或 source_tier=="T1"，不合格降到 2
   （不管 LLM 說了什麼——這條不是模型的判斷）。
2. `build_digest()` —— 一次 sonnet 呼叫，輸出 gauges（13 維度儀表）／
   brief_zh（5–8 段早報）／flags（轉折提醒，候選由 Python 先算好，LLM 只負責
   把候選寫成中文句子，不得新增）。brief_zh 寫完在 Python 端跑一次 allow-list
   sanitize（只准 <a>/<b>/<span class="n">）。
3. `build_calendar()` —— 純 Python，讀 docs/monitor/data/macro_calendar.json
   ＋ docs/catalyst/calendar.json 未來 7 天的事件，不經 LLM。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta

from common import (
    CATEGORY_LABELS_ZH,
    CATEGORY_ORDER,
    ROOT,
    iso,
    load_json,
    load_source_name_map,
    now_utc,
    read_prompt,
    source_name_for,
)
from llm import Ledger, run_claude

BATCH_SIZE = 15
SUMMARIZE_SYSTEM = None
BRIEF_SYSTEM = None

MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
REGIME_LATEST = ROOT / "docs" / "regime" / "data" / "latest.json"
MACRO_CALENDAR = ROOT / "docs" / "monitor" / "data" / "macro_calendar.json"
CATALYST_CALENDAR = ROOT / "docs" / "catalyst" / "calendar.json"

# monitor/latest.json `categories[].key` -> intel §3 dimension key (same
# mapping fetch.py uses for on-site alert cards, kept in sync manually).
MONITOR_CAT_MAP = {
    "commodities": "commodities", "credit": "credit", "crypto": None,
    "factors": "breadth", "fx": "fx", "indices": "breadth",
    "liquidity": "liquidity", "rates": "rates", "sectors": "breadth", "vol": "vol",
}

ALLOWED_TAGS_RE = re.compile(r"</?(a(?:\s+href=\"[^\"]*\")?|b|span(?:\s+class=\"n\")?)\s*/?>", re.IGNORECASE)
ANY_TAG_RE = re.compile(r"<[^>]+>")


def _summarize_system_prompt() -> str:
    global SUMMARIZE_SYSTEM
    if SUMMARIZE_SYSTEM is None:
        SUMMARIZE_SYSTEM = read_prompt("summarize.md")
    return SUMMARIZE_SYSTEM


def _brief_system_prompt() -> str:
    global BRIEF_SYSTEM
    if BRIEF_SYSTEM is None:
        BRIEF_SYSTEM = read_prompt("brief.md")
    return BRIEF_SYSTEM


# ── per-card summarize ───────────────────────────────────────────────────────
def _enforce_importance_rules(card: dict, importance: int) -> int:
    """DESIGN §7 rule 3 + §8: importance==3 (🔴) requires corroboration>=2 or
    T1; T4-alone can never be 3. This is a Python gate, not a model opinion —
    it runs regardless of what the LLM (or the deterministic data path)
    proposed."""
    try:
        importance = int(importance)
    except (TypeError, ValueError):
        importance = 2
    importance = max(1, min(3, importance))
    if importance == 3:
        corroborated = card.get("corroboration", 1) >= 2 or card.get("source_tier") == "T1"
        if not corroborated:
            importance = 2
    if card.get("source_tier") == "T4":
        importance = min(importance, 2)
    return importance


def summarize_data_card(card: dict) -> dict:
    title = re.sub(r"^\[[^\]]+\]\s*", "", card.get("title", ""))
    summary_zh = title[:60]
    cat_label = CATEGORY_LABELS_ZH.get(card.get("category"), card.get("category", ""))
    # 數字卡不寫樣板 why（讀者看 data 欄的門檻／分位就夠）；留空由 render 顯示 data 欄
    why_zh = ""
    card["summary_zh"] = summary_zh
    card["why_zh"] = why_zh
    card["importance"] = _enforce_importance_rules(card, card.get("importance_guess", 2))
    card["forecast"] = None
    card["_summarize_source"] = "deterministic"
    return card


def _batch_input(cards: list[dict]) -> list[dict]:
    out = []
    for c in cards:
        out.append(
            {
                "id": c["id"],
                "title": c.get("title", "")[:200],
                "summary": (c.get("summary_raw") or "")[:300],
                "source": c.get("source_id", ""),
                "category": c.get("category", ""),
                "level": c.get("level", "market"),
                "tickers": (c.get("tags") or {}).get("tickers", []),
                "themes": (c.get("tags") or {}).get("themes", []),
                "tier": c.get("source_tier", ""),
                "corroboration": c.get("corroboration", 1),
            }
        )
    return out


def summarize_batch(cards: list[dict], ledger: Ledger, batch_no: str):
    payload = json.dumps(_batch_input(cards), ensure_ascii=False)
    parsed, usage = run_claude(
        system=_summarize_system_prompt(),
        user=payload,
        model="sonnet",
        label=f"summarize batch {batch_no}",
        ledger=ledger,
        card_count=len(cards),
    )
    if parsed is None or not isinstance(parsed, list):
        return {}, usage
    by_id = {item["id"]: item for item in parsed if isinstance(item, dict) and item.get("id")}
    return by_id, usage


def apply_summary_result(card: dict, result: dict | None) -> dict:
    if not result:
        card["summary_zh"] = (card.get("title", "") or "")[:60]
        card["why_zh"] = "摘要生成失敗，見原始標題。"
        card["importance"] = _enforce_importance_rules(card, min(card.get("importance_guess", 2), 2))
        card["forecast"] = None
        card["_summarize_source"] = "fallback_no_llm"
        return card
    card["summary_zh"] = (result.get("summary_zh") or card.get("title", ""))[:80]
    card["why_zh"] = (result.get("why_zh") or "")[:60]
    card["importance"] = _enforce_importance_rules(card, result.get("importance", 2))
    forecast = result.get("forecast")
    card["forecast"] = forecast if isinstance(forecast, dict) and forecast.get("claim") else None
    card["_summarize_source"] = "sonnet"
    return card


def summarize_cards(selected: list[dict], ledger: Ledger, batch_size: int = BATCH_SIZE) -> dict:
    data_cards = [c for c in selected if c.get("kind") == "data"]
    other_cards = [c for c in selected if c.get("kind") != "data"]

    for c in data_cards:
        summarize_data_card(c)

    llm_calls, llm_failures = 0, 0
    for i in range(0, len(other_cards), batch_size):
        batch = other_cards[i : i + batch_size]
        by_id, usage = summarize_batch(batch, ledger, batch_no=f"{i // batch_size + 1}")
        if not by_id and usage.get("capped"):
            for c in batch:
                apply_summary_result(c, None)
            continue
        if not by_id:
            llm_failures += 1
        else:
            llm_calls += 1
        for c in batch:
            apply_summary_result(c, by_id.get(c["id"]))

    finished = data_cards + other_cards
    log = {
        "summarized": len(finished),
        "data_cards_zero_llm": len(data_cards),
        "llm_batches_ok": llm_calls,
        "llm_batches_failed": llm_failures,
    }
    print(f"[intel/summarize] {json.dumps(log, ensure_ascii=False)}", file=sys.stderr)
    return {"cards": finished, "log": log}


# ── finalize card schema (Output contract card object) ─────────────────────
def finalize_card(card: dict, name_map: dict) -> dict:
    out = {
        "id": card.get("id"),
        "kind": card.get("kind"),
        "level": card.get("level", "market"),
        "category": card.get("category"),
        "title": card.get("title"),
        "source_name": source_name_for(card, name_map),
        "source_tier": card.get("source_tier"),
        "url": card.get("url"),
        "published_at": card.get("published_at"),
        "tags": {
            "tickers": (card.get("tags") or {}).get("tickers", []),
            "themes": (card.get("tags") or {}).get("themes", []),
        },
        "importance": card.get("importance", 2),
        "corroboration": card.get("corroboration", 1),
        "checks": {
            "headline_mismatch": bool((card.get("checks") or {}).get("headline_mismatch", False)),
            "link_ok": (card.get("checks") or {}).get("link_ok"),
        },
        "summary_zh": card.get("summary_zh", ""),
        "why_zh": card.get("why_zh", ""),
    }
    if card.get("forecast"):
        out["forecast"] = card["forecast"]
    if card.get("is_rumor"):
        out["is_rumor"] = True
    if card.get("data") is not None:
        out["data"] = card["data"]
    return out


# ── digest: gauges + brief_zh + flags (one sonnet call) ─────────────────────
def build_monitor_snapshot() -> dict:
    monitor = load_json(MONITOR_LATEST)
    snapshot = {k: [] for k in CATEGORY_ORDER}
    if not monitor:
        return snapshot
    for cat_block in monitor.get("categories", []):
        intel_cat = MONITOR_CAT_MAP.get(cat_block.get("key"))
        if not intel_cat:
            continue
        for item in cat_block.get("items", [])[:8]:
            snapshot[intel_cat].append(
                {
                    "key": item.get("key"),
                    "label": item.get("label"),
                    "chg": item.get("chg"),
                    "pctile": item.get("pctile"),
                    "dir": item.get("dir"),
                }
            )
    return snapshot


def build_flag_candidates(all_classified_cards: list[dict]) -> list[dict]:
    """Deterministic candidates (Python, not the LLM) — the sonnet digest call
    only phrases these into Chinese sentences, it cannot add its own."""
    candidates = []
    for c in all_classified_cards:
        if c.get("kind") != "data":
            continue
        title = c.get("title", "")
        if "kill-watch" in title and "接近閾值" in title:
            candidates.append({
                "level": "near", "theme": title, "metric": (c.get("data") or {}),
                "status": "near", "link": c.get("url", "/detective/"),
            })
        elif "kill-watch" in title and "已突破" in title:
            candidates.append({
                "level": "confirmed", "theme": title, "metric": (c.get("data") or {}),
                "status": "breached", "link": c.get("url", "/detective/"),
            })
        elif title.startswith("[regime]"):
            candidates.append({
                "level": "confirmed", "theme": title, "metric": (c.get("data") or {}),
                "status": "regime_change", "link": c.get("url", "/regime/"),
            })
    return candidates


def sanitize_brief_html(fragments: list) -> list:
    """Allow-list per DESIGN Output contract: only <a href>, <b>, <span
    class="n"> survive; everything else is stripped (tags removed, text kept)."""
    cleaned = []
    for frag in fragments:
        if not isinstance(frag, str):
            continue
        # Strip any tag that isn't one of the allowed opening/closing forms.
        def _keep_or_drop(m):
            return m.group(0) if ALLOWED_TAGS_RE.fullmatch(m.group(0)) else ""
        frag = ANY_TAG_RE.sub(_keep_or_drop, frag)
        frag = _ANCHOR_RE.sub(_short_anchor_text, frag)
        if frag.strip():
            cleaned.append(frag.strip())
    return cleaned


def fallback_gauges() -> list:
    return [
        {"category": k, "label": CATEGORY_LABELS_ZH[k], "status": "green",
         "value": "今日無新增訊號", "delta": "變化不大"}
        for k in CATEGORY_ORDER
    ]


def _plain(text, limit: int) -> str:
    """儀表格只收純文字：去 HTML 標籤、壓空白、截長度（LLM 偶爾會把連結塞進來）。"""
    if not isinstance(text, str):
        return ""
    t = re.sub(r"<[^>]+>", "", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit]


def _short_anchor_text(m: "re.Match") -> str:
    """<a href=…>來源全名</a> → 短名：取「 — 」或「（」之前的部分，再截 12 字。"""
    open_tag, text = m.group(1), m.group(2)
    short = re.split(r"\s+—\s+|（|\(|：", text, 1)[0].strip() or text.strip()
    return f"{open_tag}{short[:12]}</a>"


_ANCHOR_RE = re.compile(r"(<a\s+href=\"[^\"]+\">)(.*?)</a>", re.S)


def _canonicalize_gauges(parsed_gauges) -> list:
    """Rebuild the 13-gauge array from CATEGORY_ORDER/CATEGORY_LABELS_ZH
    (the canonical source of truth) instead of trusting the LLM's `category`/
    `label` fields verbatim — only `status`/`value`/`delta` come from the
    model; this guarantees exact order, exact count, and exact Chinese labels
    every day regardless of small LLM formatting drift (e.g. a dropped space
    in a label)."""
    by_cat = {}
    if isinstance(parsed_gauges, list):
        for g in parsed_gauges:
            if isinstance(g, dict) and g.get("category") in CATEGORY_LABELS_ZH:
                by_cat[g["category"]] = g
    out = []
    for cat in CATEGORY_ORDER:
        g = by_cat.get(cat, {})
        out.append({
            "category": cat,
            "label": CATEGORY_LABELS_ZH[cat],
            "status": g.get("status") if g.get("status") in ("green", "yellow", "red") else "green",
            "value": _plain(g.get("value"), 40) or "今日無新增訊號",
            "delta": _plain(g.get("delta"), 30) or "變化不大",
        })
    return out


def fallback_flags(candidates: list[dict]) -> list:
    out = []
    for cand in candidates:
        status_zh = {"near": "接近閾值", "breached": "已突破", "regime_change": "regime 標籤變化"}.get(
            cand.get("status"), "")
        out.append({
            "level": cand.get("level", "near"),
            "text_zh": f"{cand.get('theme', '')}（{status_zh}）",
            "link": cand.get("link", "/detective/"),
        })
    return out


def build_digest(all_classified_cards: list[dict], finalized_market_cards: list[dict],
                  ledger: Ledger, name_map: dict) -> dict:
    monitor_snapshot = build_monitor_snapshot()
    flag_candidates = build_flag_candidates(all_classified_cards)

    market_cards_input = [
        {
            "id": c["id"], "title": c["title"], "summary_zh": c.get("summary_zh", ""),
            "why_zh": c.get("why_zh", ""), "importance": c.get("importance", 2),
            "category": c.get("category"), "url": c.get("url"),
            "source_name": c.get("source_name"),
        }
        for c in finalized_market_cards
        if c.get("level") == "market"
    ]
    payload = json.dumps(
        {"monitor_snapshot": monitor_snapshot, "market_cards": market_cards_input,
         "flag_candidates": flag_candidates},
        ensure_ascii=False,
    )
    # This single call is charged against the sonnet ledger like any other
    # sonnet batch; count it as covering the market-card set it summarizes.
    parsed, usage = run_claude(
        system=_brief_system_prompt(),
        user=payload,
        model="sonnet",
        label="digest (gauges+brief+flags)",
        ledger=ledger,
        card_count=0,  # digest doesn't consume per-card budget, only tokens
    )
    if not parsed or not isinstance(parsed, dict):
        return {
            "gauges": fallback_gauges(),
            "brief_zh": [],
            "flags": fallback_flags(flag_candidates),
        }
    gauges = _canonicalize_gauges(parsed.get("gauges"))
    brief_zh = sanitize_brief_html(parsed.get("brief_zh") or [])
    flags = parsed.get("flags")
    if not isinstance(flags, list):
        flags = fallback_flags(flag_candidates)
    else:
        # LLM must not invent flags beyond the candidates we gave it.
        flags = flags[: len(flag_candidates)] if flag_candidates else []
    return {"gauges": gauges, "brief_zh": brief_zh, "flags": flags}


# ── calendar (pure Python, no LLM) ──────────────────────────────────────────
def build_calendar(date: str, days_ahead: int = 7) -> list:
    d0 = datetime.strptime(date, "%Y-%m-%d").date()
    d1 = d0 + timedelta(days=days_ahead)
    out = []

    macro = load_json(MACRO_CALENDAR)
    if macro:
        for e in macro.get("events", []):
            try:
                ed = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except ValueError:
                continue
            if d0 <= ed <= d1:
                out.append({"date": e["date"], "text": e.get("label", e.get("type", "")), "hi": True})

    catalyst = load_json(CATALYST_CALENDAR)
    if catalyst:
        for e in catalyst.get("events", []):
            try:
                ed = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except ValueError:
                continue
            if d0 <= ed <= d1:
                ticker = e.get("ticker", "")
                label = e.get("event", e.get("type", ""))
                out.append({
                    "date": e["date"],
                    "text": f"{ticker} {label}".strip(),
                    "hi": e.get("impact") == "高",
                })

    seen = set()
    deduped = []
    for e in sorted(out, key=lambda x: (x["date"], not x["hi"])):
        key = (e["date"], e["text"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(e)
    return deduped[:40]


# ── CLI (debug/verification only) ───────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--selected", required=True, help="path to a JSON file with {'selected':[...cards]}")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    payload = load_json(args.selected)
    if payload is None:
        print(f"selected file not found: {args.selected}", file=sys.stderr)
        return 1
    selected = payload.get("selected", payload if isinstance(payload, list) else [])

    ledger = Ledger()
    name_map = load_source_name_map()
    result = summarize_cards(selected, ledger)
    finalized = [finalize_card(c, name_map) for c in result["cards"]]
    digest = build_digest(result["cards"], finalized, ledger, name_map)
    calendar = build_calendar(args.date)

    out = {
        "date": args.date, "generated_at": iso(now_utc()), "cards": finalized,
        "gauges": digest["gauges"], "brief_zh": digest["brief_zh"], "flags": digest["flags"],
        "calendar": calendar, "ledger": ledger.to_status_dict(),
    }
    out_path = args.out or f"/tmp/intel-summarize-debug-{args.date}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[intel/summarize] wrote {out_path}")
    print(f"[intel/summarize] ledger: {json.dumps(ledger.to_status_dict(), ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
