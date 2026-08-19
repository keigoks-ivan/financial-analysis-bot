#!/usr/bin/env python3
"""scripts/intel/classify.py — Phase 1 stage 1: haiku relevance/level/category
classification + deterministic post-rules + selection for stage 2.

對應 notes/site-internal/intel/DESIGN.md §6（haiku ≤200 條／日）／§7（正確性
五道）／§11（卡片 schema）。

規則（見 DESIGN §6）：
- kind=="data" 的卡片（onsite monitor/regime/rotation/crowding/kill-watch、
  FRED）已經是結構化資料，**全程零 LLM**——直接判定 relevant=True、
  level="market"、沿用既有 category，importance_guess 由 Python 規則決定。
- 其餘卡片（news/event/rumor/…）batch ~25 條送 haiku，逐張回
  relevant/level/category/tickers/themes/headline_ok/is_rumor/importance_guess。
- Python 決定性後規則（不是模型判斷）：
  * T4-only（source_tier=="T4"）⇒ importance_guess 上限 2。
  * headline_ok=false ⇒ checks.headline_mismatch=true（下游 §7 規則 4）。
- 選 ≤60 條進 stage 2，依 (importance_guess desc, tier asc, corroboration
  desc, recency desc) 排序，log 被丟掉的張數。

可獨立跑（除錯／驗收）：
    python3 scripts/intel/classify.py --date 2026-08-19 --limit 10
輸出寫到 --out（預設 docs/intel/data/{date}.classify-debug.json），不會動
docs/intel/data/{date}.json（那是 run_daily.py 的產出，由它統一寫）。
"""
from __future__ import annotations

import argparse
import json
import sys

from common import (
    CATEGORY_ORDER,
    TIER_RANK,
    iso,
    load_json,
    now_utc,
    pending_path,
    read_prompt,
)
from llm import Ledger, run_claude

BATCH_SIZE = 40
STAGE2_LIMIT = 60
SUMMARY_TRUNCATE = 300  # DESIGN §6 rule 2: LLM 只看 ≤300 字 snippet

CLASSIFY_SYSTEM = None  # lazy-loaded via read_prompt("classify.md")


def _classify_system_prompt() -> str:
    global CLASSIFY_SYSTEM
    if CLASSIFY_SYSTEM is None:
        CLASSIFY_SYSTEM = read_prompt("classify.md")
    return CLASSIFY_SYSTEM


# ── deterministic path for kind=="data" cards ───────────────────────────────
def classify_data_card(card: dict) -> dict:
    data = card.get("data") or {}
    title = card.get("title", "")
    severity = data.get("severity")
    importance_guess = 2
    if severity == "red" or "已突破" in title:
        importance_guess = 3
    elif severity == "yellow" and "接近閾值" in title:
        importance_guess = 2
    card["relevant"] = True
    card.setdefault("level", "market")
    card.setdefault("tags", {})
    card["tags"].setdefault("tickers", [])
    card["tags"].setdefault("themes", [])
    card["headline_ok"] = True
    card["is_rumor"] = False
    card["importance_guess"] = importance_guess
    card["checks"] = dict(card.get("checks") or {})
    card["checks"]["headline_mismatch"] = False
    card["_classify_source"] = "deterministic"
    return card


# ── haiku path for everything else ──────────────────────────────────────────
def _batch_input(cards: list[dict]) -> list[dict]:
    out = []
    for c in cards:
        out.append(
            {
                "id": c["id"],
                "title": c.get("title", "")[:200],
                "summary": (c.get("summary_raw") or "")[:SUMMARY_TRUNCATE],
                "source": c.get("source_id", ""),
                "category_hint": c.get("category", ""),
                "tier": c.get("source_tier", ""),
            }
        )
    return out


def classify_batch(cards: list[dict], ledger: Ledger, batch_no: str) -> dict:
    """One haiku call for one batch. Returns {id: result_dict}; empty dict on
    total failure (caller falls back to conservative defaults)."""
    payload = json.dumps(_batch_input(cards), ensure_ascii=False)
    parsed, usage = run_claude(
        system=_classify_system_prompt(),
        user=payload,
        model="haiku",
        label=f"classify batch {batch_no}",
        ledger=ledger,
        card_count=len(cards),
    )
    if parsed is None:
        return {}, usage
    if not isinstance(parsed, list):
        return {}, usage
    by_id = {}
    for item in parsed:
        if isinstance(item, dict) and item.get("id"):
            by_id[item["id"]] = item
    return by_id, usage


def apply_llm_result(card: dict, result: dict | None) -> dict:
    if not result:
        # Fail-safe default: conservative (keep it visible but low-priority,
        # DESIGN §6 rule 3 寧可漏不爆額度 — never invent a "relevant" verdict).
        card["relevant"] = False
        card["level"] = card.get("level", "market")
        card["headline_ok"] = True
        card["is_rumor"] = card.get("source_tier") in ("T3", "T4")
        card["importance_guess"] = 1
        card["_classify_source"] = "fallback_no_llm"
    else:
        card["relevant"] = bool(result.get("relevant", False))
        card["level"] = result.get("level") or card.get("level", "market")
        if result.get("category"):
            card["category"] = result["category"]
        card.setdefault("tags", {})
        card["tags"]["tickers"] = result.get("tickers") or []
        card["tags"]["themes"] = result.get("themes") or []
        card["headline_ok"] = bool(result.get("headline_ok", True))
        card["is_rumor"] = bool(result.get("is_rumor", False))
        try:
            card["importance_guess"] = int(result.get("importance_guess", 2))
        except (TypeError, ValueError):
            card["importance_guess"] = 2
        card["_classify_source"] = "haiku"

    # Python post-rules (deterministic, DESIGN §6/§7 — not the model's call).
    if card.get("source_tier") == "T4":
        card["importance_guess"] = min(card.get("importance_guess", 2), 2)
    card["checks"] = dict(card.get("checks") or {})
    card["checks"]["headline_mismatch"] = not card.get("headline_ok", True)
    card.setdefault("tags", {"tickers": [], "themes": []})
    return card


def _recency_key(card: dict) -> str:
    return card.get("published_at") or card.get("fetched_at") or ""


def select_stage2(cards: list[dict], limit: int = STAGE2_LIMIT) -> tuple[list[dict], int]:
    """(importance_guess desc, tier asc, corroboration desc, recency desc).
    Python sort is stable, so applying keys from least- to most-significant
    in separate passes gives the same result as one composite tuple, without
    fighting over ascending-vs-descending direction in a single key."""
    relevant = [c for c in cards if c.get("relevant")]
    relevant.sort(key=lambda c: _recency_key(c), reverse=True)          # 4th: recency desc
    relevant.sort(key=lambda c: -c.get("corroboration", 1))             # 3rd: corroboration desc
    relevant.sort(key=lambda c: TIER_RANK.get(c.get("source_tier"), 9))  # 2nd: tier asc
    relevant.sort(key=lambda c: -c.get("importance_guess", 1))          # 1st: importance desc
    kept = relevant[:limit]
    dropped = len(relevant) - len(kept)
    return kept, dropped


def classify(pending: dict, ledger: Ledger, batch_size: int = BATCH_SIZE,
             stage2_limit: int = STAGE2_LIMIT, only_kinds: set | None = None) -> dict:
    cards = pending.get("cards", [])
    if only_kinds:
        cards = [c for c in cards if c.get("kind") in only_kinds]

    data_cards = [c for c in cards if c.get("kind") == "data"]
    other_cards = [c for c in cards if c.get("kind") != "data"]

    for c in data_cards:
        classify_data_card(c)

    llm_calls = 0
    llm_failures = 0
    for i in range(0, len(other_cards), batch_size):
        batch = other_cards[i : i + batch_size]
        by_id, usage = classify_batch(batch, ledger, batch_no=f"{i // batch_size + 1}")
        if not by_id and usage.get("capped"):
            # Cap hit — remaining batches also skipped; mark all as not-relevant
            # fallback rather than burning further calls.
            for c in batch:
                apply_llm_result(c, None)
            continue
        if not by_id:
            llm_failures += 1
        else:
            llm_calls += 1
        for c in batch:
            apply_llm_result(c, by_id.get(c["id"]))

    all_classified = data_cards + other_cards
    relevant_count = sum(1 for c in all_classified if c.get("relevant"))
    not_relevant_count = len(all_classified) - relevant_count

    selected, dropped_over_cap = select_stage2(all_classified, stage2_limit)

    drop_log = {
        "total_classified": len(all_classified),
        "not_relevant": not_relevant_count,
        "selected_for_stage2": len(selected),
        "dropped_over_stage2_cap": dropped_over_cap,
        "llm_batches_ok": llm_calls,
        "llm_batches_failed": llm_failures,
        "data_cards_zero_llm": len(data_cards),
    }
    print(f"[intel/classify] {json.dumps(drop_log, ensure_ascii=False)}", file=sys.stderr)
    return {"all": all_classified, "selected": selected, "drop_log": drop_log}


# ── CLI (debug/verification only; run_daily.py calls classify() directly) ──
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--pending", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=None, help="only take the first N pending cards")
    ap.add_argument("--kind", default=None, help="only classify cards of this kind (debug)")
    ap.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = ap.parse_args()

    ppath = args.pending or str(pending_path(args.date))
    pending = load_json(ppath)
    if pending is None:
        print(f"pending file not found: {ppath}", file=sys.stderr)
        return 1

    only_kinds = {args.kind} if args.kind else None
    if args.limit:
        pending = dict(pending)
        cards = pending.get("cards", [])
        if only_kinds:
            cards = [c for c in cards if c.get("kind") in only_kinds]
        pending["cards"] = cards[: args.limit]
        only_kinds = None  # already filtered

    ledger = Ledger()
    result = classify(pending, ledger, batch_size=args.batch_size, only_kinds=only_kinds)
    result["ledger"] = ledger.to_status_dict()
    result["generated_at"] = iso(now_utc())

    out_path = args.out or str(pending_path(args.date)).replace(".json", ".classify-debug.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[intel/classify] wrote {out_path}")
    print(f"[intel/classify] ledger: {json.dumps(ledger.to_status_dict(), ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
