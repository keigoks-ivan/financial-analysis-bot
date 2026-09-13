"""2026-09-13：訂閱額度熔斷與 intel degraded status 回歸測試。"""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "intel"))
import llm
import run_daily


def test_quota_error_trips_run_breaker_without_retries(monkeypatch):
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))
        return SimpleNamespace(
            returncode=1,
            stdout="",
            stderr="You've hit your limit; resets later",
        )

    monkeypatch.setattr(llm.shutil, "which", lambda _: "/usr/local/bin/claude")
    monkeypatch.setattr(llm.subprocess, "run", fake_run)
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "subscription-test")
    monkeypatch.setattr(llm.time, "sleep", lambda _: pytest.fail("quota errors must not retry"))

    ledger = llm.Ledger()
    parsed, usage = llm.run_claude("system", "user", "haiku", "first", ledger=ledger)

    assert parsed is None
    assert usage["quota_exhausted"] is True
    assert ledger.quota_exhausted is True
    assert len(calls) == 1
    assert len(ledger.failures) == 1

    parsed, usage = llm.run_claude("system", "user", "sonnet", "second", ledger=ledger)
    assert parsed is None
    assert usage["quota_exhausted"] is True
    assert len(calls) == 1


@pytest.mark.parametrize("error_source", ["envelope", "stderr"])
def test_transient_retry_then_long_quota_error_trips_breaker(monkeypatch, error_source):
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))
        if len(calls) == 1:
            raise RuntimeError("temporary transport failure")
        if error_source == "envelope":
            result = "x" * 400 + " usage limit reached; resets later"
            stdout = json.dumps(
                {"is_error": True, "subtype": "error", "result": result}
            )
            return SimpleNamespace(returncode=0, stdout=stdout, stderr="")
        stderr = "x" * 400 + " usage limit reached; resets later"
        return SimpleNamespace(returncode=1, stdout="", stderr=stderr)

    monkeypatch.setattr(llm.shutil, "which", lambda _: "/usr/local/bin/claude")
    monkeypatch.setattr(llm.subprocess, "run", fake_run)
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "subscription-test")
    monkeypatch.setattr(llm.time, "sleep", lambda _: None)

    ledger = llm.Ledger()
    parsed, usage = llm.run_claude("system", "user", "haiku", "retry", ledger=ledger)

    assert parsed is None
    assert usage["quota_exhausted"] is True
    assert ledger.quota_exhausted is True
    assert len(calls) == 2


def test_successful_research_text_does_not_trip_quota_breaker(monkeypatch):
    monkeypatch.setattr(llm.shutil, "which", lambda _: "/usr/local/bin/claude")
    monkeypatch.setattr(
        llm.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(
            returncode=0,
            stdout=json.dumps(
                {
                    "is_error": False,
                    "subtype": "success",
                    "result": json.dumps([{"text": "usage limit is a research topic"}]),
                    "usage": {},
                }
            ),
            stderr="",
        ),
    )
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "subscription-test")

    ledger = llm.Ledger()
    parsed, usage = llm.run_claude("system", "user", "haiku", "success", ledger=ledger)

    assert parsed == [{"text": "usage limit is a research topic"}]
    assert "quota_exhausted" not in usage
    assert ledger.quota_exhausted is False


def test_preflight_failure_is_visible_to_ledger(monkeypatch):
    monkeypatch.setattr(llm.shutil, "which", lambda _: None)
    ledger = llm.Ledger()

    parsed, usage = llm.run_claude("system", "user", "haiku", "missing", ledger=ledger)

    assert parsed is None
    assert usage["error"] == "claude CLI not found on PATH"
    assert len(ledger.failures) == 1
    assert run_daily._llm_status(ledger) == "degraded"


@pytest.mark.parametrize(
    "mutate",
    [
        lambda ledger: ledger.failures.append({"label": "x"}),
        lambda ledger: ledger.capped.__setitem__("haiku", True),
        lambda ledger: setattr(ledger, "quota_exhausted", True),
    ],
)
def test_llm_status_marks_fallback_as_degraded(mutate):
    ledger = llm.Ledger()
    assert run_daily._llm_status(ledger) == "ok"
    mutate(ledger)
    assert run_daily._llm_status(ledger) == "degraded"


def test_llm_status_marks_card_fallback_as_degraded():
    ledger = llm.Ledger()

    assert run_daily._llm_status(ledger, [{"_summarize_source": "fallback_no_llm"}]) == "degraded"


def test_build_output_reports_failed_subscription_path(monkeypatch):
    pending = {"meta": {}, "cards": []}

    def fake_classify(_pending, ledger):
        ledger.trip_quota("classify batch 1", "haiku", "usage limit reached")
        return {"selected": [], "all": []}

    monkeypatch.setattr(run_daily, "classify", fake_classify)
    monkeypatch.setattr(run_daily, "load_source_name_map", lambda: {})
    monkeypatch.setattr(run_daily, "load_source_short_map", lambda: {})
    monkeypatch.setattr(run_daily, "build_calendar", lambda _date: [])
    monkeypatch.setattr(run_daily.threads_mod, "load_state", lambda: {"threads": []})
    monkeypatch.setattr(run_daily.threads_mod, "active_thread_list", lambda _state: [])
    monkeypatch.setattr(run_daily.threads_mod, "assign_mechanical", lambda *_args: None)
    monkeypatch.setattr(run_daily.threads_mod, "merge_daily", lambda *_args: [])
    monkeypatch.setattr(run_daily.threads_mod, "save_state", lambda _state: None)
    monkeypatch.setattr(
        run_daily,
        "summarize_cards",
        lambda *_args, **_kwargs: {"cards": [], "log": {"summarized": 0}},
    )
    monkeypatch.setattr(run_daily, "run_deepread", lambda *_args: {})
    monkeypatch.setattr(run_daily, "build_digest", lambda *_args: {"brief_zh": [], "claims": []})
    monkeypatch.setattr(run_daily, "build_gauges", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(run_daily, "build_flags", lambda *_args: [])

    output = run_daily.build_output("2026-09-13", pending, llm_available=True)

    assert output["llm"] == "degraded"
    assert output["status"]["tokens"] == {"haiku": 0, "sonnet": 0}
