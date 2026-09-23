"""Tests for scripts/build_stock_dash_all.py — the batch driver's yfinance
rate-limit handling added after run 35823204018 (2026-09-23) got the GitHub
runner's IP rate-limited around ticker #186/339, after which every remaining
ticker failed in 1-2s with yfinance.exceptions.YFRateLimitError.

No network: build_one's subprocess.run and the retry loop's build_one calls
are both monkeypatched, since the actual cloud rate limit can't be reproduced
locally (see the task's own note on this). Covers:
  1. build_one() correctly flags a YFRateLimitError failure as retryable
     (via the traceback text in stderr) and leaves other failures alone.
  2. run_batch() paces ticker-submission start times by --stagger.
  3. main()'s retry-pass loop: a ticker that recovers after a couple of
     rate-limited attempts eventually counts as ok; a ticker that never
     recovers, and a non-rate-limited failure, both end up in the final
     failures list; and a failure rate over --fail-threshold-pct makes the
     job exit non-zero (deploy-pages.yml only ever pulls this workflow's
     last *successful* run's artifact, so that's safe — see main()'s
     comment on the exit-code decision).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_stock_dash_all as bda  # noqa: E402


class _FakeCompletedProcess:
    def __init__(self, returncode, stderr):
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = ""


def test_build_one_flags_rate_limit_error_from_stderr(monkeypatch):
    traceback_tail = (
        "Traceback (most recent call last):\n"
        "  File \"scripts/build_stock_dash.py\", line 3716, in <module>\n"
        "    main()\n"
        "yfinance.exceptions.YFRateLimitError: Too Many Requests. Rate limited. Try after a while.\n"
    )
    monkeypatch.setattr(bda.subprocess, "run", lambda *a, **k: _FakeCompletedProcess(1, traceback_tail))
    r = bda.build_one("python3", "NVDA", 240, {}, [])
    assert r["ok"] is False
    assert r["rate_limited"] is True


def test_build_one_does_not_flag_other_failures(monkeypatch):
    stderr = "RuntimeError: yfinance returned no price history for 5274.TW\n"
    monkeypatch.setattr(bda.subprocess, "run", lambda *a, **k: _FakeCompletedProcess(1, stderr))
    r = bda.build_one("python3", "5274.TW", 240, {}, [])
    assert r["ok"] is False
    assert r["rate_limited"] is False


def test_run_batch_staggers_submissions(monkeypatch):
    def fake_build_one(python_bin, ticker, timeout, env, extra_args):
        return {"ticker": ticker, "ok": True, "seconds": 0.0}

    monkeypatch.setattr(bda, "build_one", fake_build_one)
    tickers = ["A", "B", "C", "D"]
    t0 = time.time()
    results = bda.run_batch(tickers, "python3", 240, {}, [], workers=4, stagger=0.05)
    elapsed = time.time() - t0
    assert set(results) == set(tickers)
    assert all(r["ok"] for r in results.values())
    assert elapsed >= 0.05 * (len(tickers) - 1)


def test_main_retries_rate_limited_and_fails_over_threshold(monkeypatch, tmp_path, capsys):
    # Per-ticker scripted outcomes, one entry per call (last entry repeats once
    # a ticker's list is exhausted):
    #   OK1      — succeeds immediately.
    #   RECOVER  — rate-limited twice (initial pass + retry 1), then succeeds
    #              on retry 2 — proves a ticker can recover mid-retry-loop.
    #   STUCK    — rate-limited on every attempt — proves retries give up
    #              after RATE_LIMIT_BACKOFFS_S is exhausted, not forever.
    #   BADDATA  — fails once, NOT rate-limited (e.g. the real 5274.TW/8299.TW
    #              "Quote not found" case) — proves it is never retried.
    scripts = {
        "OK1": [{"ok": True}],
        "RECOVER": [
            {"ok": False, "error": "exit 1", "rate_limited": True},
            {"ok": False, "error": "exit 1", "rate_limited": True},
            {"ok": True},
        ],
        "STUCK": [{"ok": False, "error": "exit 1", "rate_limited": True}],
        "BADDATA": [{"ok": False, "error": "exit 1", "rate_limited": False}],
    }
    call_counts = {}

    def fake_build_one(python_bin, ticker, timeout, env, extra_args):
        call_counts[ticker] = call_counts.get(ticker, 0) + 1
        n = call_counts[ticker]
        spec_list = scripts[ticker]
        spec = dict(spec_list[min(n, len(spec_list)) - 1])
        spec.setdefault("seconds", 0.1)
        spec["ticker"] = ticker
        return spec

    monkeypatch.setattr(bda, "build_one", fake_build_one)
    monkeypatch.setattr(bda, "prebuild_shared_files", lambda refresh_universe: {"stub": True})
    monkeypatch.setattr(bda.time, "sleep", lambda *_a, **_k: None)  # skip real backoff waits
    monkeypatch.setattr(bda, "OUT_DIR", tmp_path)
    monkeypatch.setattr(bda, "BUILD_REPORT_PATH", tmp_path / "_build_report.json")
    monkeypatch.setattr(
        sys, "argv",
        ["build_stock_dash_all.py", "--tickers", "OK1,RECOVER,STUCK,BADDATA", "--workers", "2", "--stagger", "0"],
    )

    with pytest.raises(SystemExit) as exc:
        bda.main()
    assert exc.value.code == 1
    assert "FAILING" in capsys.readouterr().err

    report = json.loads((tmp_path / "_build_report.json").read_text())
    assert report["n_tickers"] == 4
    assert report["n_ok"] == 2
    assert report["n_failed"] == 2
    assert {f["ticker"] for f in report["failures"]} == {"STUCK", "BADDATA"}

    assert len(report["retry_passes"]) == len(bda.RATE_LIMIT_BACKOFFS_S)
    assert [p["n_recovered"] for p in report["retry_passes"]] == [0, 1, 0]

    assert call_counts["OK1"] == 1
    assert call_counts["BADDATA"] == 1  # never retried — not rate-limited
    assert call_counts["RECOVER"] == 3  # initial + 2 retries, then it succeeded
    assert call_counts["STUCK"] == 1 + len(bda.RATE_LIMIT_BACKOFFS_S)  # every retry pass, then gives up


def test_main_stays_green_under_fail_threshold(monkeypatch, tmp_path, capsys):
    """A couple of genuinely-bad tickers (like 5274.TW / 8299.TW) among many
    good ones must NOT fail the job — only a failure rate over the threshold
    should (see the test above)."""
    scripts = {f"OK{i}": [{"ok": True}] for i in range(1, 19)}
    scripts["BADDATA"] = [{"ok": False, "error": "exit 1", "rate_limited": False}]
    call_counts = {}

    def fake_build_one(python_bin, ticker, timeout, env, extra_args):
        call_counts[ticker] = call_counts.get(ticker, 0) + 1
        spec = dict(scripts[ticker][0])
        spec.setdefault("seconds", 0.1)
        spec["ticker"] = ticker
        return spec

    monkeypatch.setattr(bda, "build_one", fake_build_one)
    monkeypatch.setattr(bda, "prebuild_shared_files", lambda refresh_universe: {"stub": True})
    monkeypatch.setattr(bda.time, "sleep", lambda *_a, **_k: None)
    monkeypatch.setattr(bda, "OUT_DIR", tmp_path)
    monkeypatch.setattr(bda, "BUILD_REPORT_PATH", tmp_path / "_build_report.json")
    monkeypatch.setattr(
        sys, "argv",
        ["build_stock_dash_all.py", "--tickers", ",".join(scripts), "--workers", "2", "--stagger", "0"],
    )

    bda.main()  # must NOT raise SystemExit — 1/19 failed is well under the 10% threshold

    report = json.loads((tmp_path / "_build_report.json").read_text())
    assert report["n_failed"] == 1
    assert report["failures"][0]["ticker"] == "BADDATA"
    assert call_counts["BADDATA"] == 1
