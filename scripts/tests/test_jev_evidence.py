"""Offline tests for the Jev evidence layer (scripts/jev/). No network: the
Jev call and the network fetchers are monkeypatched. Run with:
  python3.12 -m pytest scripts/tests/test_jev_evidence.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "jev"))

import jev_common as jc
import fetch_evidence as fe
import clean_evidence as ce


# ---------------------------------------------------------------------------
# fetch_evidence: dedup, seen_before, one source failing doesn't sink the run
# ---------------------------------------------------------------------------

def make_item(url, headline, channel="test", published="2026-09-22T00:00:00Z", text="text"):
    return {"url": url, "headline": headline, "text": text, "source": "Wire",
            "published": published, "channel": channel}


def test_dedup_by_exact_url():
    items = [make_item("https://a.example/1", "Headline A"),
             make_item("https://a.example/1", "Different headline, same url")]
    out = fe.dedup_items(items)
    assert len(out) == 1
    assert out[0]["headline"] == "Headline A"


def test_dedup_by_normalized_headline():
    items = [make_item("https://a.example/1", "NVIDIA Raises Guidance!"),
             make_item("https://b.example/2", "nvidia raises guidance")]
    out = fe.dedup_items(items)
    assert len(out) == 1


def test_dedup_keeps_distinct_items():
    items = [make_item("https://a.example/1", "Story one"),
             make_item("https://a.example/2", "Story two")]
    assert len(fe.dedup_items(items)) == 2


def test_seen_before_marks_recurring_ids_and_new_ones_get_added():
    items = [make_item("https://a.example/1", "Story one"),
             make_item("https://a.example/2", "Story two")]
    seen_store = {"schema": "jev-seen-v1", "ticker": "NVDA",
                  "ids": {jc.sha_id("https://a.example/1"): "2026-09-15"}}
    final, updated = fe.finalize_items(items, seen_store, "2026-09-22", "2026-09-22T00:00:00Z")
    by_url = {i["url"]: i for i in final}
    assert by_url["https://a.example/1"]["seen_before"] is True
    assert by_url["https://a.example/2"]["seen_before"] is False
    # the new id should now be recorded for future runs
    assert jc.sha_id("https://a.example/2") in updated["ids"]


def test_seen_store_prunes_entries_older_than_30_days():
    seen_store = {"schema": "jev-seen-v1", "ticker": "NVDA",
                  "ids": {"stale-id": "2020-01-01", "fresh-id": "2026-09-20"}}
    _, updated = fe.finalize_items([], seen_store, "2026-09-22", "2026-09-22T00:00:00Z")
    assert "stale-id" not in updated["ids"]
    assert "fresh-id" in updated["ids"]


def test_collect_raw_one_failing_source_does_not_abort_others(monkeypatch):
    def boom():
        raise RuntimeError("simulated network failure")

    monkeypatch.setattr(fe, "fetch_yfinance_news", lambda ticker: boom())
    monkeypatch.setattr(fe, "fetch_google_news",
                         lambda q, n, channel: [make_item(f"https://g.example/{q}", f"news about {q}", channel)])
    monkeypatch.setattr(fe, "fetch_sec_8k", lambda cik, max_items=10: [make_item("https://sec.example/1", "8-K filed", "sec_8k")])
    monkeypatch.setattr(fe, "fetch_newsroom_rss", lambda url, max_items=10: boom())

    cfg = {"google_news_queries": ["NVIDIA", "Jensen Huang"], "cik": "0001045810",
           "newsroom_rss": "https://nvidianews.nvidia.com/rss.xml", "max_items_per_query": 8}
    items, statuses = fe.collect_raw(cfg, "NVDA", sleep=lambda s: None)

    by_id = {s["id"]: s for s in statuses}
    assert by_id["yfinance_news"]["status"] == "error"
    assert by_id["newsroom_rss"]["status"] == "error"
    assert by_id["sec_8k"]["status"] == "ok"
    assert by_id["google_news:nvidia"]["status"] == "ok"
    # the two good sources still produced items despite the two bad ones
    assert len(items) == 3


# ---------------------------------------------------------------------------
# chunking stays under the token budget (pure function, jev_common.py)
# ---------------------------------------------------------------------------

def test_chunk_indices_by_budget_never_exceeds_budget():
    costs = [1000] * 37  # deliberately not a clean multiple of the budget
    budget = 4500
    chunks = jc.chunk_indices_by_budget(costs, budget)
    covered = sorted(i for chunk in chunks for i in chunk)
    assert covered == list(range(len(costs)))  # every item placed exactly once
    for chunk in chunks:
        assert sum(costs[i] for i in chunk) <= budget


def test_chunk_indices_by_budget_oversized_single_item_gets_its_own_chunk():
    costs = [100, 100, 999999, 100]
    chunks = jc.chunk_indices_by_budget(costs, 500)
    assert [2] in chunks
    covered = sorted(i for chunk in chunks for i in chunk)
    assert covered == [0, 1, 2, 3]


# ---------------------------------------------------------------------------
# importance formula
# ---------------------------------------------------------------------------

CLAIMS_BY_ID = {
    "A1": {"weight": "key"}, "A2": {"weight": "load"}, "A5": {"weight": "support"},
    "E1": {"weight": "risk"},
}


def test_importance_zero_when_nothing_borne():
    imp, borne = ce.compute_importance({"A1": 0.1, "A2": 0.2}, "dated_company_statement", False, CLAIMS_BY_ID)
    assert imp == 0.0 and borne == []


def test_importance_uses_max_weight_among_borne_claims():
    bearing = {"A1": 0.9, "A5": 0.8}  # key (3) and support (1) both borne -> max is key
    imp, borne = ce.compute_importance(bearing, "dated_company_statement", False, CLAIMS_BY_ID)
    assert set(borne) == {"A1", "A5"}
    assert imp == pytest.approx(3 * 1.0 * 1.0)


def test_importance_applies_kind_factor():
    imp, _ = ce.compute_importance({"A2": 0.9}, "analyst_opinion", False, CLAIMS_BY_ID)
    assert imp == pytest.approx(2 * 0.4 * 1.0)


def test_importance_applies_novelty_discount_for_seen_before():
    imp_new, _ = ce.compute_importance({"A2": 0.9}, "dated_third_party_report", False, CLAIMS_BY_ID)
    imp_seen, _ = ce.compute_importance({"A2": 0.9}, "dated_third_party_report", True, CLAIMS_BY_ID)
    assert imp_new == pytest.approx(2 * 0.8 * 1.0)
    assert imp_seen == pytest.approx(2 * 0.8 * 0.3)
    assert imp_seen < imp_new


def test_importance_risk_claims_always_weight_3():
    imp, _ = ce.compute_importance({"E1": 0.6}, "dated_company_statement", False, CLAIMS_BY_ID)
    assert imp == pytest.approx(3 * 1.0 * 1.0)


# ---------------------------------------------------------------------------
# clean_evidence end-to-end (mocked call), on the real questions_NVDA.json
# ---------------------------------------------------------------------------

def load_real_spec():
    return jc.load_json(Path(__file__).resolve().parents[1] / "jev" / "questions_NVDA.json")


def fake_call_factory(relevant_ids):
    """Builds a fake `call` that answers relevance noul=0.9 for items whose
    id is in relevant_ids (else 0.1), and for tagging questions answers a
    fixed topic/kind and bearing=1.0 only for the A1 claim."""
    def fake_call(state, questions, key):
        answers = {}
        for qid, q in questions.items():
            if qid.endswith("_relevance"):
                answers[qid] = {"type": "noul", "noul": 0.9 if qid in relevant_ids else 0.1}
            elif qid.endswith("_topic"):
                answers[qid] = {"type": "choice", "choice": "supply_and_capacity",
                                 "confidence": 0.9, "probabilities": {"supply_and_capacity": 0.9}}
            elif qid.endswith("_kind"):
                answers[qid] = {"type": "choice", "choice": "dated_company_statement",
                                 "confidence": 0.9, "probabilities": {"dated_company_statement": 0.9}}
            elif "_bear_" in qid:
                claim_id = qid.split("_bear_")[1]
                answers[qid] = {"type": "noul", "noul": 0.9 if claim_id == "A1" else 0.05}
        return {"model": "jev-1.13.0-test", "answers": answers,
                "usage": {"input_tokens": 123, "output_tokens": 4}}
    return fake_call


def test_clean_end_to_end_marks_relevant_items_and_computes_importance(tmp_path):
    spec = load_real_spec()
    items = [
        {"id": "id1", "headline": "TSMC secures more CoWoS capacity for NVIDIA Rubin",
         "source": "Wire", "url": "https://x.example/1", "text": "TSMC and NVIDIA discuss CoWoS capacity.",
         "published": "2026-09-22T00:00:00Z", "seen_before": False},
        {"id": "id2", "headline": "Local weather forecast for the weekend",
         "source": "Wire", "url": "https://x.example/2", "text": "Sunny with a chance of rain.",
         "published": "2026-09-22T00:00:00Z", "seen_before": False},
    ]
    relevant_qids = {"item_0_relevance"}
    fake_call = fake_call_factory(relevant_qids)
    log_path = tmp_path / "jev_log.jsonl"

    pack = ce.clean(items, spec, "fake-key", "NVDA", call_fn=fake_call, log_path=log_path)

    assert len(pack["items"]) == 1
    assert pack["items"][0]["id"] == "id1"
    assert pack["items"][0]["bearing"] == ["A1"]
    assert pack["items"][0]["importance"] > 0
    assert len(pack["dropped"]) == 1
    assert pack["dropped"][0]["id"] == "id2"
    assert pack["usage_tokens"]["total"] > 0
    # calibration log got at least one line per Jev answer (relevance + topic + kind + 16 bearing for the kept item)
    log_lines = log_path.read_text().strip().splitlines()
    assert len(log_lines) >= 1 + 1 + 1 + 16


# ---------------------------------------------------------------------------
# nothing Chinese is ever sent to Jev
# ---------------------------------------------------------------------------

def test_no_chinese_sent_in_state_or_questions(tmp_path):
    spec = load_real_spec()
    # sanity: the real spec does carry Chinese display fields (zh); this
    # test must prove clean_evidence never forwards them.
    assert jc.has_cjk(spec["claims"])

    items = [{"id": "id1", "headline": "NVIDIA confirms Rubin Ultra on schedule",
               "source": "Wire", "url": "https://x.example/1",
               "text": "NVIDIA said Rubin Ultra production remains on schedule for next year.",
               "published": "2026-09-22T00:00:00Z", "seen_before": False}]
    captured = []

    def capturing_call(state, questions, key):
        captured.append((state, questions))
        answers = {}
        for qid in questions:
            if qid.endswith("_relevance"):
                answers[qid] = {"type": "noul", "noul": 0.9}
            elif qid.endswith("_topic"):
                answers[qid] = {"type": "choice", "choice": "supply_and_capacity", "confidence": 0.9,
                                 "probabilities": {"supply_and_capacity": 0.9}}
            elif qid.endswith("_kind"):
                answers[qid] = {"type": "choice", "choice": "dated_company_statement", "confidence": 0.9,
                                 "probabilities": {"dated_company_statement": 0.9}}
            elif "_bear_" in qid:
                answers[qid] = {"type": "noul", "noul": 0.9}
        return {"model": "jev-1.13.0-test", "answers": answers, "usage": {"input_tokens": 1, "output_tokens": 1}}

    ce.clean(items, spec, "fake-key", "NVDA", call_fn=capturing_call, log_path=None)

    assert captured, "the fake call should have been invoked at least once"
    for state, questions in captured:
        assert not jc.has_cjk(state), "state sent to Jev must be English-only"
        assert not jc.has_cjk(questions), "questions sent to Jev must be English-only"


def test_has_cjk_detects_chinese():
    assert jc.has_cjk({"a": "沒有前沿實驗室"})
    assert not jc.has_cjk({"a": "no frontier lab"})
