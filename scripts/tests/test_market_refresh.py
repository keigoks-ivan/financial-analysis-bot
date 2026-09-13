#!/usr/bin/env python3
"""2026-09-13：market_refresh 的離線證據版本、驗證與發布契約測試。"""
from __future__ import annotations

import copy
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import market_refresh as refresh  # noqa: E402


def _state(as_of="2026-09-13", value=100.0, council_summary="穩定"):
    """最小可保存 state；每筆 quote 同時帶驗證所需數值與日期。"""
    return {
        "schema": "market-state-v1",
        "as_of": as_of,
        "components": [],
        "environment": {},
        "council": [],
        "council_summary": council_summary,
        "flows": [],
        "fuses": [],
        "anomalies": [],
        "freshness": [],
        "evidence": {
            "quotes": {
                "monitor:sp500": {
                    "label": "S&P 500",
                    "num": value,
                    "pctile": 50.0,
                    "chg30_pct": 1.0,
                    "z": 0.2,
                    "as_of": as_of,
                },
            },
        },
    }


def _intel(as_of="2026-09-13", llm="ok"):
    return {"date": as_of, "llm": llm, "cards": [], "brief_zh": [], "flags": []}


def _snapshot(as_of="2026-09-13", value=100.0, council_summary="穩定"):
    return refresh.make_snapshot(_state(as_of, value, council_summary), _intel(as_of))


def _candidate(snapshot, today, reviewer_model="cold-reader"):
    """小型 candidate；critic 本體只在特定合約測試中隔離。"""
    quote = snapshot["state"]["evidence"]["quotes"]["monitor:sp500"]
    forecasts = []
    for index, horizon in enumerate((90, 180, 365)):
        forecasts.append({
            "p": (0.45, 0.50, 0.55)[index],
            "claim": "測試命題-{0}".format(index),
            "resolver": {"series": "pxd:SPY", "op": ">"},
            "horizon_days": horizon,
        })
    candidate = {
        "schema": "market-read-v1",
        "snapshot_id": snapshot["snapshot_id"],
        "as_of": today.isoformat(),
        "billing": "subscription_only",
        "valid_days": 7,
        "model": "writer-model",
        "thesis_zh": "初稿判讀。",
        "review": {"model": reviewer_model, "verdict": "pass", "snapshot_id": snapshot["snapshot_id"]},
        "forces": [{"refs": [{"ref": "monitor:sp500"}]}],
        "analogs": [],
        "falsifiers": [],
        "observations": [{"ref": "monitor:sp500", "field": "num", "value": quote["num"], "as_of": quote["as_of"]}],
        "horizons": [
            {"key": key, "p_up": forecasts[index]["p"],
             "resolve_by": (today + timedelta(days=forecasts[index]["horizon_days"])).isoformat()}
            for index, key in enumerate(("3m", "6m", "12m"))
        ],
        "forecasts": forecasts,
        "claim_ids": ["claim-{0}".format(index) for index in range(len(forecasts))],
        "scenarios": [{
            "name_zh": "基準",
            "horizon": "3m",
            "conditions_zh": "條件",
            "falsifiers_zh": "反證",
            "asset_implications_zh": "影響",
            "refs": ["monitor:sp500"],
        }],
    }
    candidate["review"]["content_hash"] = refresh.candidate_hash(candidate)
    return candidate


def _request(prior):
    return {"prior_read_hash": refresh.digest(prior)}


def _write_snapshot(data_dir, snapshot):
    refresh.atomic_json(data_dir / "snapshots" / (snapshot["snapshot_id"] + ".json"), snapshot)


def _ledger_rows(candidate, today, wrong_p=False):
    rows = []
    for index, (claim_id, forecast) in enumerate(zip(candidate["claim_ids"], candidate["forecasts"])):
        item = copy.deepcopy(forecast)
        item.update({
            "id": claim_id,
            "source": "market-read",
            "resolve_by": (today.fromordinal(today.toordinal() + forecast["horizon_days"])).isoformat(),
        })
        if wrong_p and index == 0:
            item["p"] = forecast["p"] + 0.01
        rows.append(item)
    return rows


def test_source_health_check_time_does_not_create_new_research_but_failure_does():
    state = _state()
    state["source_research"] = {"generated_at": "first", "as_of": "2026-09-13", "sources": [
        {"id": "fred_cpi", "status": "ok", "last_attempt_at": "first", "last_success_at": "first", "latest": {"date": "2026-08-01", "value": 300}}
    ]}
    before = refresh.make_snapshot(state, {})
    state["source_research"].update({"generated_at": "second", "as_of": "2026-09-14"})
    state["source_research"]["sources"][0].update({"last_attempt_at": "second", "last_success_at": "second"})
    assert before == refresh.make_snapshot(state, {})
    state["source_research"]["sources"][0]["status"] = "failed"
    after = refresh.make_snapshot(state, {})
    assert before["snapshot_id"] != after["snapshot_id"]
    assert any("本次取得失敗" in warning for warning in refresh.quality(after, date(2026, 9, 13))[1])


def test_snapshot_identity_is_idempotent_and_changes_with_observation_or_metadata(tmp_path):
    data_dir, work_dir = tmp_path / "data", tmp_path / "work"
    snapshot = _snapshot()
    read = {"snapshot_id": "old", "as_of": "2026-09-12"}

    first = refresh.prepare(snapshot, read, data_dir, work_dir, date(2026, 9, 13))
    second = refresh.prepare(copy.deepcopy(snapshot), read, data_dir, work_dir, date(2026, 9, 13))

    evidence = Path(first["run_dir"]) / "evidence.json"
    assert first["snapshot_id"] == second["snapshot_id"] == snapshot["snapshot_id"]
    assert json.loads(evidence.read_text(encoding="utf-8")) == snapshot
    assert _snapshot(value=101.0)["snapshot_id"] != snapshot["snapshot_id"]
    assert _snapshot(council_summary="改變")["snapshot_id"] != snapshot["snapshot_id"]


def test_period_comparisons_mark_missing_history_and_never_select_future_snapshot():
    current = _snapshot("2026-09-13", 110.0)
    only_future = [_snapshot("2026-09-20", 999.0)]
    missing = refresh.period_comparisons(current, only_future)
    assert {row["status"] for row in missing} == {"insufficient_history"}

    prior = _snapshot("2026-09-06", 100.0)
    periods = refresh.period_comparisons(current, [prior, only_future[0]])
    week = next(row for row in periods if row["days"] == 7)
    assert week["status"] == "ok"
    assert week["actual_start"] == "2026-09-06"
    assert week["changes"][0]["before"]["num"] == 100.0


def test_prepare_compares_last_read_even_when_record_already_points_at_current_snapshot(tmp_path):
    data_dir, work_dir = tmp_path / "data", tmp_path / "work"
    old = _snapshot("2026-09-06", 100.0)
    current = _snapshot("2026-09-13", 101.0)
    _write_snapshot(data_dir, old)
    _write_snapshot(data_dir, current)
    # record 已經把 refresh 指到 current，但發表的 read 還依賴 old 證據。
    refresh.atomic_json(data_dir / "refresh.json", {"snapshot_id": current["snapshot_id"]})
    prior_read = {"snapshot_id": old["snapshot_id"], "as_of": "2026-09-06"}

    request = refresh.prepare(current, prior_read, data_dir, work_dir, date(2026, 9, 13))

    assert request["comparison_baseline"] == old["snapshot_id"]
    assert request["changes"] == [{
        "ref": "monitor:sp500", "label": "S&P 500",
        "before": old["state"]["evidence"]["quotes"]["monitor:sp500"],
        "current": current["state"]["evidence"]["quotes"]["monitor:sp500"],
        "change": "updated", "delta": 1.0,
    }]


def test_quality_blocks_stale_state_and_discloses_incomplete_sources():
    snapshot = refresh.make_snapshot(_state("2026-09-08"), _intel("2026-09-08", llm="degraded"))
    snapshot["state"]["freshness"] = [{"pipeline": "行情", "status": "stale", "as_of": "2026-09-08"}]

    errors, warnings = refresh.quality(snapshot, date(2026, 9, 13))

    assert any("超過四個曆日" in item for item in errors)
    assert any("情報摘要" in item for item in warnings)
    assert any("行情資料偏舊" in item for item in warnings)


def test_quality_blocks_stale_required_sp500_quote_even_when_state_is_current():
    state = _state("2026-09-13")
    state["evidence"]["quotes"]["monitor:sp500"]["as_of"] = "2026-09-08"
    snapshot = refresh.make_snapshot(state, _intel())

    errors, _ = refresh.quality(snapshot, date(2026, 9, 13))

    assert any("主要行情已超過四個曆日" in item for item in errors)


@pytest.mark.parametrize(
    "mutate, expected",
    [
        (lambda candidate: candidate.__setitem__("snapshot_id", "wrong"), "不同批次"),
        (lambda candidate: candidate["observations"][0].__setitem__("value", 101.0), "引用數字或日期"),
        (lambda candidate: candidate["observations"][0].__setitem__("as_of", "2026-09-12"), "引用數字或日期"),
    ],
)
def test_candidate_must_bind_snapshot_and_exact_observations(tmp_path, monkeypatch, mutate, expected):
    monkeypatch.setattr(refresh.critic, "CHECKS", ())
    today, snapshot, prior = date(2026, 9, 13), _snapshot(), {"snapshot_id": "prior"}
    candidate = _candidate(snapshot, today)
    mutate(candidate)

    errors, _ = refresh.validate_candidate(
        candidate, snapshot, _request(prior), prior, today, tmp_path / "ledger.jsonl", require_ledger=False)

    assert any(expected in item for item in errors)


def test_candidate_requires_independent_reviewer(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh.critic, "CHECKS", ())
    today, snapshot, prior = date(2026, 9, 13), _snapshot(), {}
    candidate = _candidate(snapshot, today, reviewer_model="writer-model")

    errors, _ = refresh.validate_candidate(
        candidate, snapshot, _request(prior), prior, today, tmp_path / "ledger.jsonl", require_ledger=False)

    assert any("不同模型" in item for item in errors)


def test_candidate_cannot_change_content_after_cold_review(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh.critic, "CHECKS", ())
    today, snapshot, prior = date(2026, 9, 13), _snapshot(), {}
    candidate = _candidate(snapshot, today)
    candidate["thesis_zh"] = "冷讀後被改過的判讀。"

    errors, _ = refresh.validate_candidate(
        candidate, snapshot, _request(prior), prior, today, tmp_path / "ledger.jsonl", require_ledger=False)

    assert any("冷讀內容版本" in item for item in errors)


def test_candidate_horizon_expiry_must_match_forecast(tmp_path, monkeypatch):
    monkeypatch.setattr(refresh.critic, "CHECKS", ())
    today, snapshot, prior = date(2026, 9, 13), _snapshot(), {}
    candidate = _candidate(snapshot, today)
    candidate["horizons"][0]["resolve_by"] = "2026-12-11"
    candidate["review"]["content_hash"] = refresh.candidate_hash(candidate)

    errors, _ = refresh.validate_candidate(
        candidate, snapshot, _request(prior), prior, today, tmp_path / "ledger.jsonl", require_ledger=False)

    assert any("頁面到期日與預測不同：3m" in item for item in errors)


@pytest.mark.parametrize("ledger_exists, wrong_p", [(False, False), (True, True)])
def test_candidate_forecasts_must_be_present_and_match_ledger(tmp_path, monkeypatch, ledger_exists, wrong_p):
    monkeypatch.setattr(refresh.critic, "CHECKS", ())
    today, snapshot, prior = date(2026, 9, 13), _snapshot(), {}
    candidate = _candidate(snapshot, today)
    ledger_path = tmp_path / "forecasts.jsonl"
    if ledger_exists:
        ledger_path.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in _ledger_rows(candidate, today, wrong_p)),
            encoding="utf-8",
        )

    errors, _ = refresh.validate_candidate(candidate, snapshot, _request(prior), prior, today, ledger_path)

    assert any("預測帳簿與判讀不一致" in item for item in errors)


def test_real_market_read_fixture_passes_existing_critic_and_new_binding_contract(tmp_path):
    """真實 read/state 組合讓既有 critic 也跑一次，非只靠 monkeypatch。"""
    state = json.loads((REPO_ROOT / "docs/market/data/state.json").read_text(encoding="utf-8"))
    candidate = json.loads((REPO_ROOT / "docs/market/data/read.json").read_text(encoding="utf-8"))
    today = date.fromisoformat(state["as_of"])
    snapshot = refresh.make_snapshot(state, _intel(state["as_of"]))
    candidate["as_of"] = today.isoformat()
    candidate["snapshot_id"] = snapshot["snapshot_id"]
    candidate["billing"] = "subscription_only"
    candidate["review"] = {"model": "independent-reviewer", "verdict": "pass", "snapshot_id": snapshot["snapshot_id"]}
    candidate["data_gaps_zh"] = "沿用來源新鮮度揭露。"
    candidate["scenarios"] = [{
        "name_zh": "基準", "horizon": "3m", "conditions_zh": "條件",
        "falsifiers_zh": "反證", "asset_implications_zh": "影響",
        "refs": ["monitor:sp500"],
    }]
    for index, horizon in enumerate(candidate["horizons"]):
        horizon["resolve_by"] = (today + timedelta(days=candidate["forecasts"][index]["horizon_days"])).isoformat()
    candidate["observations"] = [
        {"ref": ref, "field": "num", "value": state["evidence"]["quotes"][ref]["num"],
         "as_of": state["evidence"]["quotes"][ref]["as_of"]}
        for ref in sorted({ref for _, ref in refresh.critic.collect_refs(candidate)})
    ]
    ledger_path = tmp_path / "forecasts.jsonl"
    ledger_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in _ledger_rows(candidate, today)),
        encoding="utf-8",
    )
    candidate["review"]["content_hash"] = refresh.candidate_hash(candidate)

    errors, warnings = refresh.validate_candidate(candidate, snapshot, _request({}), {}, today, ledger_path)

    assert errors == []
    assert isinstance(warnings, list)


def test_publish_keeps_old_evidence_and_points_to_one_coherent_release_bundle(tmp_path):
    data_dir = tmp_path / "data"
    old = _snapshot("2026-09-06", 90.0)
    current = _snapshot("2026-09-13", 100.0)
    _write_snapshot(data_dir, old)
    old_path = data_dir / "snapshots" / (old["snapshot_id"] + ".json")
    before = old_path.read_text(encoding="utf-8")
    history = [{"as_of": "2026-09-06", "snapshot_id": old["snapshot_id"], "thesis_zh": "舊判讀"}]
    read = {"snapshot_id": current["snapshot_id"], "as_of": "2026-09-13", "thesis_zh": "新判讀"}

    published = refresh.publish(
        data_dir, current, read, history, "2026-09-13T00:00:00+00:00", [], [], accepted=True)

    bundle_path = data_dir / published["bundle"]
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    assert published["status"] == "ok"
    assert bundle["refresh"]["bundle"] == published["bundle"]
    assert bundle["state"] == current["state"]
    assert bundle["read"] == read
    assert bundle["history"] == history
    assert old_path.read_text(encoding="utf-8") == before


def test_locked_publish_rejects_a_prior_read_changed_by_another_process(tmp_path):
    data_dir = tmp_path / "data"
    prior = {"snapshot_id": "old", "as_of": "2026-09-06"}
    refresh.atomic_json(data_dir / "read.json", {"snapshot_id": "newer", "as_of": "2026-09-13"})

    with pytest.raises(ValueError, match="另一程序更新"):
        refresh.locked_publish(
            data_dir, _snapshot(), prior, [], "2026-09-13T00:00:00+00:00", [], [], False,
            refresh.digest(prior),
        )


def test_same_quotes_with_new_metadata_is_not_a_new_evidence_version(tmp_path):
    # 2026-09-13：引用數字沒變、只有合成日／元資料變，不重做研究、不標等待重評。
    import market_refresh as mr
    quotes = {"monitor:sp500": {"label": "S&P 500", "num": 100.0, "as_of": "2026-09-11"}}
    read = {"snapshot_id": "old", "evidence_snapshot": {"quotes": dict(quotes)}, "as_of": "2026-09-13"}
    state = {"as_of": "2026-09-13", "gaps": ["runner path"], "evidence": {"quotes": dict(quotes)}}
    snapshot = mr.make_snapshot(state, {})
    assert snapshot["snapshot_id"] != "old"
    assert mr.evidence_unchanged(snapshot, read)
    refresh, _ = mr.make_release(snapshot, read, {}, [], "now", [], [], accepted=False)
    assert refresh["status"] == "ok"
    changed = mr.make_snapshot({**state, "evidence": {"quotes": {"monitor:sp500": {**quotes["monitor:sp500"], "num": 101.0}}}}, {})
    assert not mr.evidence_unchanged(changed, read)
    assert mr.make_release(changed, read, {}, [], "now", [], [], accepted=False)[0]["status"] == "needs_review"
