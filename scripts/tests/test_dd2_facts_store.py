#!/usr/bin/env python3
"""測試 `scripts/dd2/facts_store.py`（dd2 v20 證據庫，README §2 契約）。

全程用 `tmp_path` 當 repo_root，不碰真實 `facts/` 目錄。涵蓋：
- TTL 邊界（`age_days == TTL_DAYS[axis]` 剛好到期算 stale，`age_days == TTL-1` 仍 fresh）
- 強制刷新：`new_quarter` 使 90 天軸失效、`price_move_pct` 使
  `capital_markets_pricing` 失效、`major_events` 14 天窗且不受兩種強制刷新影響
- `plan_refresh` 對未知軸 id 用預設 90 天（TTL 邊界與強制刷新不套用）
- `seed_from_evidence` 不覆蓋較新（含同日）的既有存查
- `plan_refresh` 回傳的 fresh 物件（含 findings 逐條）帶 `reused_from`／`age_days`
- `put_axis` 的 `axis_meta`（顯式傳入優先於 `.dd_build/runs/{run}/axes.json` 查找）
- `put_transcripts`／`latest_transcript_date`（雙形狀相容：evidence.transcripts
  原形狀與 `ddreport._run_koyfin_step` 雙層形狀）
- `last_price`（`numbers.json.latest_quarter_kpis.price_at_dd`）
- 用真實 `.dd_build/runs/TXN_20260910/evidence.json` 做一次端到端 seed 驗形狀
- CLI `status`／`seed`

Python 3.9 相容（不用 `match`、不用 `X | None`）。
"""
import datetime
import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent

sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))
import facts_store  # noqa: E402
from facts_store import FactsStore  # noqa: E402


TODAY = datetime.date(2026, 9, 16)
TXN_EVIDENCE_PATH = REPO_ROOT / ".dd_build" / "runs" / "TXN_20260910" / "evidence.json"


def _iso(d):
    return d.strftime("%Y-%m-%d")


def _mk_axis_obj(status="found", note="n", findings=None):
    return {
        "status": status,
        "queries_run": ["q1"],
        "findings": findings if findings is not None else [{"claim": "c1", "id": "x#0"}],
        "note": note,
    }


# ---------------------------------------------------------------------------
# TTL 邊界
# ---------------------------------------------------------------------------

def test_ttl_boundary_exact_expiry_is_stale(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    axis_id = "competitive_share_entrants"  # TTL_DAYS = 90
    fetched_at = _iso(TODAY - datetime.timedelta(days=90))
    store.put_axis(axis_id, _mk_axis_obj(), fetched_at, "TICK_20260618")

    plan = store.plan_refresh([axis_id], TODAY)
    assert plan["stale"] == [axis_id]
    assert plan["fresh"] == {}


def test_ttl_boundary_one_day_before_expiry_is_fresh(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    axis_id = "competitive_share_entrants"
    fetched_at = _iso(TODAY - datetime.timedelta(days=89))
    store.put_axis(axis_id, _mk_axis_obj(), fetched_at, "TICK_20260619")

    plan = store.plan_refresh([axis_id], TODAY)
    assert plan["stale"] == []
    assert axis_id in plan["fresh"]
    assert plan["fresh"][axis_id]["age_days"] == 89


def test_major_events_ttl_is_14_days(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    fetched_expired = _iso(TODAY - datetime.timedelta(days=14))
    fetched_ok = _iso(TODAY - datetime.timedelta(days=13))
    store.put_axis("major_events", _mk_axis_obj(), fetched_expired, "R1")

    plan = store.plan_refresh(["major_events"], TODAY)
    assert plan["stale"] == ["major_events"]

    store.put_axis("major_events", _mk_axis_obj(), fetched_ok, "R2")
    plan2 = store.plan_refresh(["major_events"], TODAY)
    assert plan2["stale"] == []
    assert plan2["fresh"]["major_events"]["age_days"] == 13


def test_180_day_axis_ttl_boundary(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    axis_id = "regulatory_antitrust"  # TTL_DAYS = 180
    store.put_axis(axis_id, _mk_axis_obj(), _iso(TODAY - datetime.timedelta(days=180)), "R1")
    assert store.plan_refresh([axis_id], TODAY)["stale"] == [axis_id]

    store.put_axis(axis_id, _mk_axis_obj(), _iso(TODAY - datetime.timedelta(days=179)), "R2")
    assert store.plan_refresh([axis_id], TODAY)["stale"] == []


# ---------------------------------------------------------------------------
# 強制刷新
# ---------------------------------------------------------------------------

def test_new_quarter_forces_90_day_axis_stale_even_if_fresh(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    axis_id = "supply_demand_durability"  # 在 FORCE_REFRESH_NEW_QUARTER_AXES
    store.put_axis(axis_id, _mk_axis_obj(), _iso(TODAY), "R1")  # age_days = 0

    plan_no_new_q = store.plan_refresh([axis_id], TODAY, new_quarter=False)
    assert plan_no_new_q["stale"] == []

    plan_new_q = store.plan_refresh([axis_id], TODAY, new_quarter=True)
    assert plan_new_q["stale"] == [axis_id]


def test_new_quarter_does_not_force_axes_outside_the_policy_group(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    # 180 天群組（無強制刷新規則）與未知軸都不該被 new_quarter 波及。
    for axis_id in ("regulatory_antitrust", "some_unlisted_axis", "major_events"):
        store.put_axis(axis_id, _mk_axis_obj(), _iso(TODAY), "R1")

    plan = store.plan_refresh(
        ["regulatory_antitrust", "some_unlisted_axis", "major_events"], TODAY, new_quarter=True,
    )
    assert plan["stale"] == []
    assert set(plan["fresh"].keys()) == {"regulatory_antitrust", "some_unlisted_axis", "major_events"}


def test_price_move_forces_capital_markets_pricing_stale(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    axis_id = "capital_markets_pricing"  # TTL_DAYS = 30
    store.put_axis(axis_id, _mk_axis_obj(), _iso(TODAY), "R1")

    small_move = store.plan_refresh([axis_id], TODAY, price_move_pct=15.0)
    assert small_move["stale"] == []

    big_move = store.plan_refresh([axis_id], TODAY, price_move_pct=25.0)
    assert big_move["stale"] == [axis_id]

    # 剛好 20% 不觸發（README：「變動 > 20%」嚴格大於）
    boundary_move = store.plan_refresh([axis_id], TODAY, price_move_pct=20.0)
    assert boundary_move["stale"] == []

    negative_big_move = store.plan_refresh([axis_id], TODAY, price_move_pct=-25.0)
    assert negative_big_move["stale"] == [axis_id]


def test_price_move_does_not_affect_other_axes(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    store.put_axis("major_events", _mk_axis_obj(), _iso(TODAY), "R1")
    plan = store.plan_refresh(["major_events"], TODAY, price_move_pct=999.0)
    assert plan["stale"] == []


# ---------------------------------------------------------------------------
# 未知軸預設 90 天
# ---------------------------------------------------------------------------

def test_plan_refresh_unknown_axis_defaults_to_90_days(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    axis_id = "totally_unlisted_axis"
    assert axis_id not in facts_store.TTL_DAYS

    store.put_axis(axis_id, _mk_axis_obj(), _iso(TODAY - datetime.timedelta(days=90)), "R1")
    assert store.plan_refresh([axis_id], TODAY)["stale"] == [axis_id]

    store.put_axis(axis_id, _mk_axis_obj(), _iso(TODAY - datetime.timedelta(days=89)), "R2")
    assert store.plan_refresh([axis_id], TODAY)["stale"] == []


def test_plan_refresh_missing_axis_is_stale(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    plan = store.plan_refresh(["never_fetched_axis"], TODAY)
    assert plan["stale"] == ["never_fetched_axis"]
    assert plan["fresh"] == {}


# ---------------------------------------------------------------------------
# fresh 物件帶 reused_from／age_days
# ---------------------------------------------------------------------------

def test_fresh_axis_object_carries_reused_from_and_age_days(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    axis_id = "end_markets"
    findings = [{"claim": "a", "id": "end_markets#0"}, {"claim": "b", "id": "end_markets#1"}]
    fetched_at = _iso(TODAY - datetime.timedelta(days=10))
    store.put_axis(axis_id, _mk_axis_obj(findings=findings), fetched_at, "TICK_20260906")

    plan = store.plan_refresh([axis_id], TODAY)
    axis_obj = plan["fresh"][axis_id]
    assert axis_obj["reused_from"] == "TICK_20260906"
    assert axis_obj["age_days"] == 10
    assert len(axis_obj["findings"]) == 2
    for finding in axis_obj["findings"]:
        assert finding["reused_from"] == "TICK_20260906"
        assert finding["age_days"] == 10

    # 原始存查（磁碟上的檔）不應被 plan_refresh 污染。
    stored = store.load_axis(axis_id)
    assert "reused_from" not in stored
    assert "age_days" not in stored
    assert "reused_from" not in stored["findings"][0]


# ---------------------------------------------------------------------------
# seed_from_evidence 不覆蓋較新
# ---------------------------------------------------------------------------

def test_seed_does_not_overwrite_newer_or_same_day_existing(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    store.put_axis(
        "end_markets", _mk_axis_obj(note="existing-newer"), "2026-09-10", "TICK_A",
    )

    evidence = {
        "coverage": {
            "end_markets": {
                "status": "found",
                "findings": [{"claim": "from evidence"}],
                "queries_run": [],
                "note": "from-evidence-older",
                "reused_from": "SOME_OLD_RUN",
                "age_days": 999,
            },
        },
        "numbers": {},
    }

    # 較舊 fetched_at：不覆蓋
    store.seed_from_evidence(evidence, "2026-09-05", "TICK_B")
    stored = store.load_axis("end_markets")
    assert stored["note"] == "existing-newer"
    assert stored["run"] == "TICK_A"

    # 同日 fetched_at：也不覆蓋（既有 >= 新的即跳過）
    store.seed_from_evidence(evidence, "2026-09-10", "TICK_C")
    stored2 = store.load_axis("end_markets")
    assert stored2["run"] == "TICK_A"

    # 較新 fetched_at：覆蓋，且 reused_from/age_days 被剝掉
    store.seed_from_evidence(evidence, "2026-09-15", "TICK_D")
    stored3 = store.load_axis("end_markets")
    assert stored3["run"] == "TICK_D"
    assert stored3["note"] == "from-evidence-older"
    assert "reused_from" not in stored3
    assert "age_days" not in stored3


def test_seed_writes_axis_absent_in_store(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    evidence = {
        "coverage": {
            "major_events": {"status": "found", "findings": [], "queries_run": [], "note": "n"},
        },
    }
    assert store.load_axis("major_events") is None
    store.seed_from_evidence(evidence, "2026-09-10", "TICK_SEED")
    stored = store.load_axis("major_events")
    assert stored is not None
    assert stored["run"] == "TICK_SEED"


def test_seed_numbers_merges_price_at_dd_and_respects_freshness(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    evidence = {
        "coverage": {},
        "numbers": {
            "price_at_dd": 199.5,
            "latest_quarter_kpis": {"quarter": "Q2 FY2026", "items": []},
        },
    }
    store.seed_from_evidence(evidence, "2026-09-10", "TICK_SEED")
    stored = store.load_numbers()
    assert stored["quarter"] == "Q2 FY2026"
    assert stored["latest_quarter_kpis"]["price_at_dd"] == 199.5
    assert store.last_price() == 199.5

    # 較舊 evidence 不覆蓋既有較新的 numbers.json
    older_evidence = {
        "numbers": {
            "price_at_dd": 1.0,
            "latest_quarter_kpis": {"quarter": "Q1 FY2026", "items": []},
        },
    }
    store.seed_from_evidence(older_evidence, "2026-09-01", "TICK_OLD")
    assert store.load_numbers()["quarter"] == "Q2 FY2026"


# ---------------------------------------------------------------------------
# numbers_fresh
# ---------------------------------------------------------------------------

def test_numbers_fresh_false_new_quarter_returns_object(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    store.put_numbers({"quarter": "Q2", "items": []}, "2026-09-10", "R1", "Q2 FY2026")
    obj = store.numbers_fresh(False)
    assert obj is not None
    assert obj["quarter"] == "Q2 FY2026"


def test_numbers_fresh_true_new_quarter_returns_none(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    store.put_numbers({"quarter": "Q2", "items": []}, "2026-09-10", "R1", "Q2 FY2026")
    assert store.numbers_fresh(True) is None


def test_numbers_fresh_no_file_returns_none(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    assert store.numbers_fresh(False) is None
    assert store.numbers_fresh(True) is None


# ---------------------------------------------------------------------------
# put_axis：axis_meta
# ---------------------------------------------------------------------------

def test_put_axis_looks_up_axis_meta_from_run_dir(tmp_path):
    run_id = "TICK_20260910"
    axes_path = tmp_path / ".dd_build" / "runs" / run_id / "axes.json"
    axes_path.parent.mkdir(parents=True)
    axes_path.write_text(json.dumps([
        {"id": "end_markets", "name": "終端市場", "question": "q?"},
        {"id": "major_events", "name": "重大事件", "question": "q2?"},
    ]), encoding="utf-8")

    store = FactsStore(tmp_path, "TICK")
    record = store.put_axis("end_markets", _mk_axis_obj(), "2026-09-16", run_id)
    assert record["axis_meta"]["name"] == "終端市場"
    stored = store.load_axis("end_markets")
    assert stored["axis_meta"]["id"] == "end_markets"


def test_put_axis_explicit_axis_meta_overrides_disk_lookup(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    # 故意不建立 axes.json —— 顯式傳入的 axis_meta 不該依賴磁碟查找。
    record = store.put_axis(
        "end_markets", _mk_axis_obj(), "2026-09-16", "TICK_NO_AXES_FILE",
        axis_meta={"id": "end_markets", "custom": True},
    )
    assert record["axis_meta"] == {"id": "end_markets", "custom": True}


def test_put_axis_no_axis_meta_when_not_found(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    record = store.put_axis("end_markets", _mk_axis_obj(), "2026-09-16", "TICK_NO_RUN_DIR")
    assert "axis_meta" not in record


# ---------------------------------------------------------------------------
# put_transcripts / latest_transcript_date
# ---------------------------------------------------------------------------

def test_put_transcripts_and_latest_transcript_date_single_wrap_shape(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    transcripts_obj = {
        "selected": {
            "recent_four_quarters": [
                "/x/TICK_Q3_2025_Earnings_Call_20251021.md",
                "/x/TICK_Q4_2025_Earnings_Call_20260127.md",
            ],
            "high_signal_optional": [],
        },
        "koyfin_session_status": "ok",
        "must_read_all": [],
        "optional_read_all": [],
    }
    store.put_transcripts(transcripts_obj, "2026-09-16", "TICK_20260916")
    assert store.latest_transcript_date() == "20260127"
    stored = store.load_transcripts()
    assert stored["transcripts"] == transcripts_obj
    assert stored["run"] == "TICK_20260916"


def test_put_transcripts_double_wrap_shape_from_koyfin_step(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    double_wrapped = {
        "transcripts": {
            "selected": {"recent_four_quarters": ["/x/TICK_Q1_2026_20260422.md"]},
            "koyfin_session_status": "ok",
        }
    }
    store.put_transcripts(double_wrapped, "2026-09-16", "R1")
    assert store.latest_transcript_date() == "20260422"


def test_latest_transcript_date_none_when_no_store(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    assert store.latest_transcript_date() is None


def test_put_transcripts_empty_selected_yields_none_latest(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    store.put_transcripts({"selected": {"recent_four_quarters": []}}, "2026-09-16", "R1")
    assert store.latest_transcript_date() is None


# ---------------------------------------------------------------------------
# last_price
# ---------------------------------------------------------------------------

def test_last_price_reads_price_at_dd_from_numbers(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    store.put_numbers(
        {"quarter": "Q2 FY2026", "items": [], "price_at_dd": 195.32}, "2026-09-16", "R1", "Q2 FY2026",
    )
    assert store.last_price() == 195.32


def test_last_price_none_when_no_numbers_file(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    assert store.last_price() is None


def test_last_price_none_when_missing_key(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    store.put_numbers({"quarter": "Q2 FY2026", "items": []}, "2026-09-16", "R1", "Q2 FY2026")
    assert store.last_price() is None


def test_put_numbers_quarter_defaults_to_none(tmp_path):
    store = FactsStore(tmp_path, "TICK")
    record = store.put_numbers({"items": []}, "2026-09-16", "R1")
    assert record["quarter"] is None


# ---------------------------------------------------------------------------
# 端到端：真實 evidence.json 形狀
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not TXN_EVIDENCE_PATH.exists(), reason="fixture run dir 不在（.dd_build/runs/TXN_20260910）")
def test_seed_from_real_txn_evidence_fixture(tmp_path):
    evidence = json.loads(TXN_EVIDENCE_PATH.read_text(encoding="utf-8"))
    store = FactsStore(tmp_path, "TXNTEST")
    store.seed_from_evidence(evidence, "2026-09-10", "TXN_20260910")

    coverage = evidence.get("coverage") or {}
    assert coverage, "fixture evidence.json 應該要有 coverage"
    for axis_id in coverage:
        stored = store.load_axis(axis_id)
        assert stored is not None, "缺軸 {0}".format(axis_id)
        assert stored["axis"] == axis_id

    stored_numbers = store.load_numbers()
    expected_kpis = evidence["numbers"]["latest_quarter_kpis"]
    assert stored_numbers["quarter"] == expected_kpis.get("quarter")
    assert stored_numbers["latest_quarter_kpis"]["items"] == expected_kpis["items"]

    expected_price = evidence["numbers"].get("price_at_dd")
    if expected_price is not None:
        assert store.last_price() == pytest.approx(expected_price)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def test_cli_status_reports_stale_and_fresh(tmp_path, capsys):
    store = FactsStore(tmp_path, "CLITICK")
    store.put_axis(
        "major_events", _mk_axis_obj(), _iso(TODAY - datetime.timedelta(days=14)), "R_OLD",
    )
    store.put_axis(
        "end_markets", _mk_axis_obj(), _iso(TODAY - datetime.timedelta(days=5)), "R_NEW",
    )

    rc = facts_store.main([
        "--repo-root", str(tmp_path), "status", "CLITICK", "--today", "2026-09-16",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "major_events" in out and "STALE" in out
    assert "end_markets" in out and "fresh" in out


def test_cli_status_no_store_reports_gracefully(tmp_path, capsys):
    rc = facts_store.main(["--repo-root", str(tmp_path), "status", "NOSTORE"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "NOSTORE" in out


def test_cli_seed_from_evidence_file(tmp_path, capsys):
    evidence = {
        "date": "20260910",
        "coverage": {
            "major_events": {"status": "found", "findings": [], "queries_run": [], "note": "n"},
        },
        "numbers": {
            "price_at_dd": 42.0,
            "latest_quarter_kpis": {"quarter": "Q1 FY2026", "items": []},
        },
    }
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    rc = facts_store.main([
        "--repo-root", str(tmp_path), "seed", "CLITICK",
        "--evidence", str(evidence_path), "--run-id", "CLITICK_20260910",
    ])
    assert rc == 0
    capsys.readouterr()

    store = FactsStore(tmp_path, "CLITICK")
    assert store.load_axis("major_events") is not None
    assert store.load_numbers()["quarter"] == "Q1 FY2026"
    assert store.last_price() == 42.0


def test_cli_seed_infers_fetched_at_from_evidence_date(tmp_path):
    evidence = {"date": "20260905", "coverage": {}, "numbers": {}}
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    facts_store.main([
        "--repo-root", str(tmp_path), "seed", "CLITICK2",
        "--evidence", str(evidence_path), "--run-id", "CLITICK2_20260905",
    ])
    # 沒有軸／numbers 可灌，但不應該丟例外；CLI 跑完即代表推斷日期成功。
    assert facts_store._infer_fetched_at(evidence, "CLITICK2_20260905") == "2026-09-05"
