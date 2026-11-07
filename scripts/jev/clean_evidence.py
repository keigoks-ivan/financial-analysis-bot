#!/usr/bin/env python3
"""Send a day's raw evidence items to Jev and tag each one: relevance,
topic, kind, and which of the 16 Jev claims in questions_NVDA.json it bears
on. Importance is computed in code from those tags — never asked of Jev
directly (see model-jaggedness_jev-1.13: don't hide a judgment call inside
a "how important is this" question when the pieces can be asked literally
and combined in code).

Two Jev calls per run (each possibly split into several requests to stay
under the 64k combined token budget):
  1. relevance, one noul per item (reuses questions_NVDA.json's
     relevance_filter, the same way probe.py's own step 1 does).
  2. for items that pass relevance: topic (choice), kind (choice), and one
     noul per claim ("does this item bear on claim X"), all against the
     same state so it's one shared context per request.

Output: data/jev/evidence/<TICKER>/<date>.json — kept items with tags and
importance (sorted by importance), plus a `dropped` list (relevance below
threshold) for human audit of false negatives.

Every individual Jev answer is also appended to data/jev/jev_log.jsonl for
later calibration.

Usage:
  python3 scripts/jev/clean_evidence.py --ticker NVDA [--date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import sys

from probe import call  # reuse the tested caller; do not reinvent it
from jev_common import (
    JEV_DIR, DATA_DIR, load_json, atomic_json, append_jsonl, now_iso, today_str,
    estimate_tokens, chunk_indices_by_budget,
)

# --- Importance formula. Every constant it uses lives here, nowhere else. ---
# importance = max_weight_of_claims_it_bears_on (key=3, load=2, support=1,
#              risk=3) x kind_factor (company statement / regulator = 1.0,
#              third-party report = 0.8, analyst opinion = 0.4, commentary
#              = 0.2) x novelty (seen_before ? 0.3 : 1.0)
CLAIM_WEIGHT = {"key": 3, "load": 2, "support": 1, "risk": 3,
                "unknown": 1}  # unknowns (F*) are tagged so their news is kept, weighted like support
KIND_FACTOR = {
    "dated_company_statement": 1.0,
    "regulator_or_court_action": 1.0,
    "dated_third_party_report": 0.8,
    "analyst_opinion": 0.4,
    "market_commentary_or_price_move": 0.2,
    # "other" isn't named in the design memo's kind_factor table; treated
    # like commentary (low-value default) rather than erroring out.
    "other": 0.2,
}
NOVELTY_SEEN_BEFORE = 0.3
NOVELTY_NEW = 1.0

# A claim counts as "borne on" by an item once Jev's noul for that pair is
# at least this. Independent of questions_NVDA.json's own claim-routing
# thresholds (those gate what the program does with a claim's *verdict*;
# this one only gates whether an item is relevant evidence for it).
BEARING_NOUL_MIN = 0.5

# Item text sent to Jev is capped so per-item token cost is small and
# predictable; the full text is still kept in the output file for humans.
ITEM_TEXT_CHARS_FOR_JEV = 500

# Stay well under Jev's 64k combined (state + all questions) budget per
# request. `state` alone (a handful of items, each capped at
# ITEM_TEXT_CHARS_FOR_JEV) never comes close to the separate 32k
# state-plus-longest-question limit.
SAFE_TOKEN_BUDGET = 45000


def build_item_view(item):
    return {"headline": item["headline"], "source": item["source"],
            "text": (item.get("text") or "")[:ITEM_TEXT_CHARS_FOR_JEV]}


def jev_claims_of(spec):
    return [c for c in spec["claims"] if "jev" in c]


def tag_targets_of(spec):
    """What items get bearing-tagged against: the Jev claims plus the
    unknowns (F*) that carry a Jev question. Unknowns never get a claim
    answer from probe.py; they are only tagging targets."""
    return jev_claims_of(spec) + [u for u in spec.get("unknowns", []) if "jev" in u]


def run_relevance(items, spec, key, ticker, call_fn=call, log_path=None):
    """One noul per item: does it pass questions_NVDA.json's relevance
    filter? Chunked to stay under SAFE_TOKEN_BUDGET. Returns
    ({orig_index: noul}, total_input_tokens)."""
    relevance_filter = spec["relevance_filter"]
    views = [build_item_view(it) for it in items]
    base_cost = estimate_tokens(relevance_filter)
    costs = [estimate_tokens(v) + base_cost for v in views]
    chunks = chunk_indices_by_budget(costs, SAFE_TOKEN_BUDGET)

    scores, total_tokens = {}, 0
    for idxs in chunks:
        local = {orig: li for li, orig in enumerate(idxs)}
        state = {"items": [views[orig] for orig in idxs]}
        questions = {}
        for orig in idxs:
            li = local[orig]
            q = dict(relevance_filter)
            q["instructions"] = relevance_filter["instructions"].replace("`item`", f"`items[{li}]`")
            questions[f"item_{orig}_relevance"] = q
        resp = call_fn(state, questions, key)
        total_tokens += resp["usage"]["input_tokens"]
        for orig in idxs:
            ans = resp["answers"][f"item_{orig}_relevance"]
            scores[orig] = ans["noul"]
            if log_path:
                append_jsonl(log_path, {"ts": now_iso(), "model": resp["model"], "ticker": ticker,
                                         "item_id": items[orig]["id"], "question_id": "relevance", "answer": ans})
    return scores, total_tokens


def _bearing_question(li, claim):
    # Structured instructions keep the claim's own question text (from
    # questions_NVDA.json, unmodified) as *data* in one field, and put the
    # literal, `items[i]`-anchored question Jev must answer in another —
    # the pattern primitives/advanced.md recommends, and it avoids echoing
    # a stray `news` reference (the claim texts point at `news`; our state
    # here only has `items`).
    return {
        "type": "noul",
        "instructions": {
            "claim_question": claim["jev"]["instructions"],
            "question": (f"Does `items[{li}]` contain information — a fact, statement, or "
                         "report — that bears on `claim_question`, meaning it would help "
                         "answer it, either toward yes or toward no?"),
        },
    }


def run_tagging(kept, spec, key, ticker, call_fn=call, log_path=None):
    """For items that passed relevance: topic, kind, and one bearing noul
    per Jev claim. Chunked to stay under SAFE_TOKEN_BUDGET. Returns
    ({local_index: {"topic":Answer,"kind":Answer,"bearing":{claim_id:noul}}},
    total_input_tokens)."""
    topic_q, kind_q = spec["cleaning"]["topic"], spec["cleaning"]["kind"]
    claims = tag_targets_of(spec)
    views = [build_item_view(it) for it in kept]

    def item_cost(view):
        # Build the item's *actual* question set (local index doesn't matter
        # for length) and measure it directly — an earlier version tried to
        # shortcut this with per-field estimates and undercounted real
        # requests by ~40-70% (json wrapping + the full bearing-question
        # text add up), which tripped Jev's max_tokens_exceeded in practice.
        qs = {"topic": {**topic_q, "instructions": topic_q["instructions"].replace("`item`", "`items[0]`")},
              "kind": {**kind_q, "instructions": kind_q["instructions"].replace("`item`", "`items[0]`")}}
        for claim in claims:
            qs[f"bear_{claim['id']}"] = _bearing_question(0, claim)
        return estimate_tokens({"item": view, "questions": qs})

    costs = [item_cost(v) for v in views]
    chunks = chunk_indices_by_budget(costs, SAFE_TOKEN_BUDGET)

    results, total_tokens = {}, 0
    for idxs in chunks:
        local = {orig: li for li, orig in enumerate(idxs)}
        state = {"items": [views[orig] for orig in idxs]}
        questions = {}
        for orig in idxs:
            li = local[orig]
            questions[f"item_{orig}_topic"] = {**topic_q, "instructions": topic_q["instructions"].replace("`item`", f"`items[{li}]`")}
            questions[f"item_{orig}_kind"] = {**kind_q, "instructions": kind_q["instructions"].replace("`item`", f"`items[{li}]`")}
            for claim in claims:
                questions[f"item_{orig}_bear_{claim['id']}"] = _bearing_question(li, claim)
        resp = call_fn(state, questions, key)
        total_tokens += resp["usage"]["input_tokens"]
        for orig in idxs:
            li = local[orig]
            topic_ans = resp["answers"][f"item_{orig}_topic"]
            kind_ans = resp["answers"][f"item_{orig}_kind"]
            bearing = {}
            for claim in claims:
                ans = resp["answers"][f"item_{orig}_bear_{claim['id']}"]
                bearing[claim["id"]] = ans["noul"]
                if log_path:
                    append_jsonl(log_path, {"ts": now_iso(), "model": resp["model"], "ticker": ticker,
                                             "item_id": kept[orig]["id"], "question_id": f"bear_{claim['id']}",
                                             "answer": ans})
            if log_path:
                append_jsonl(log_path, {"ts": now_iso(), "model": resp["model"], "ticker": ticker,
                                         "item_id": kept[orig]["id"], "question_id": "topic", "answer": topic_ans})
                append_jsonl(log_path, {"ts": now_iso(), "model": resp["model"], "ticker": ticker,
                                         "item_id": kept[orig]["id"], "question_id": "kind", "answer": kind_ans})
            # keyed by `orig` (index into `kept`/`views`, stable across
            # chunks), not `li` (the per-request local `items[i]` index,
            # which restarts at 0 in every chunk and would collide here).
            results[orig] = {"topic": topic_ans, "kind": kind_ans, "bearing": bearing}
    return results, total_tokens


def compute_importance(bearing, kind_choice, seen_before, claims_by_id):
    """bearing: {claim_id: noul}. Returns (importance, [claim_ids it bears on])."""
    borne = [cid for cid, p in bearing.items() if p >= BEARING_NOUL_MIN]
    if not borne:
        return 0.0, borne
    max_weight = max(CLAIM_WEIGHT[claims_by_id[cid]["weight"]] for cid in borne)
    kind_factor = KIND_FACTOR.get(kind_choice, KIND_FACTOR["other"])
    novelty = NOVELTY_SEEN_BEFORE if seen_before else NOVELTY_NEW
    return round(max_weight * kind_factor * novelty, 4), borne


def clean(items, spec, key, ticker, call_fn=call, log_path=None):
    """Core pipeline, decoupled from file I/O so it's testable. Returns the
    full evidence-pack dict (schema jev-evidence-clean-v1)."""
    relevance_scores, tok1 = run_relevance(items, spec, key, ticker, call_fn, log_path)
    th = spec["thresholds"]["relevance_noul_min"]
    kept_idx = [i for i in range(len(items)) if relevance_scores[i] >= th]
    kept_set = set(kept_idx)
    dropped = [{"id": items[i]["id"], "headline": items[i]["headline"], "source": items[i]["source"],
                "url": items[i]["url"], "relevance": relevance_scores[i]}
               for i in range(len(items)) if i not in kept_set]
    kept = [items[i] for i in kept_idx]

    claims_by_id = {c["id"]: c for c in tag_targets_of(spec)}
    tag_results, tok2 = run_tagging(kept, spec, key, ticker, call_fn, log_path) if kept else ({}, 0)

    cleaned = []
    for li, orig_i in enumerate(kept_idx):
        it = items[orig_i]
        tr = tag_results[li]
        importance, borne = compute_importance(tr["bearing"], tr["kind"]["choice"],
                                                it.get("seen_before", False), claims_by_id)
        cleaned.append({**it, "relevance": relevance_scores[orig_i],
                         "topic": tr["topic"], "kind": tr["kind"],
                         "bearing": borne, "bearing_detail": tr["bearing"],
                         "importance": importance})
    cleaned.sort(key=lambda x: x["importance"], reverse=True)

    return {
        "schema": "jev-evidence-clean-v1", "ticker": ticker, "generated_at": now_iso(),
        "usage_tokens": {"relevance": tok1, "tagging": tok2, "total": tok1 + tok2},
        "items": cleaned, "dropped": dropped,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--date", default=None, help="defaults to today (UTC)")
    a = ap.parse_args()
    date = a.date or today_str()

    spec = load_json(JEV_DIR / f"questions_{a.ticker}.json")
    if spec is None or "cleaning" not in spec:
        sys.exit(f"missing scripts/jev/questions_{a.ticker}.json (or its 'cleaning' section)")
    raw_path = DATA_DIR / "raw" / a.ticker / f"{date}.json"
    raw = load_json(raw_path)
    if raw is None:
        sys.exit(f"no raw evidence at {raw_path}; run fetch_evidence.py first")

    from jev_common import get_api_key
    key = get_api_key()
    if not key:
        sys.exit("no TYPESAFE_API_KEY (env var or ~/.config/typesafe/api_key)")

    log_path = DATA_DIR / "jev_log.jsonl"
    pack = clean(raw["items"], spec, key, a.ticker, call, log_path)
    pack["date"] = date
    pack["ticker"] = a.ticker

    out_path = DATA_DIR / "evidence" / a.ticker / f"{date}.json"
    atomic_json(out_path, pack)

    usage = pack["usage_tokens"]
    print(f"clean_evidence: ticker={a.ticker} date={date} raw_items={len(raw['items'])} "
          f"kept={len(pack['items'])} dropped={len(pack['dropped'])} "
          f"tokens(relevance={usage['relevance']} tagging={usage['tagging']} total={usage['total']})")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
