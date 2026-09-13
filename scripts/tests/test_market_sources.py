"""2026-09-13：來源增量、修訂、保密、缺口及市況串接的離線驗收。"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
import sys
from datetime import date
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import market_sources as m
import build_market_state as state_builder


def spec():
    return {"id": "test_series", "provider": "ofr", "label": "測試融資", "domain": "liquidity", "region": "US",
            "series": "TEST", "unit": "%", "frequency": "daily", "source_url": "https://data.financialresearch.gov/",
            "data_mode": "latest_revised", "enabled": True}


def row(day, value, vintage=None, published=None):
    return {"date": day, "value": value, "vintage": vintage, "published_at": published}


def test_same_data_is_idempotent_but_reverted_revision_is_preserved():
    definition = spec()
    saved, _ = m.merge_observations(definition, None, [row("2026-09-01", 1)], [], "first", date(2026, 9, 13))
    same, added = m.merge_observations(definition, saved, [row("2026-09-01", 1)], [], "second", date(2026, 9, 13))
    assert same == saved and added == 0
    revised, _ = m.merge_observations(definition, saved, [row("2026-09-01", 2)], [], "third", date(2026, 9, 13))
    reverted, added = m.merge_observations(definition, revised, [row("2026-09-01", 1)], [], "fourth", date(2026, 9, 13))
    assert added == 1 and [r["value"] for r in reverted["observations"]] == [1, 2, 1]
    assert m.current_observations(reverted, date(2026, 9, 13))[-1]["value"] == 1


@pytest.mark.parametrize("bad", [row("2026-09-14", 1), row("2026-09-01", float("nan")), row("2026-09-01", True)])
def test_malformed_or_future_values_do_not_enter_history(bad):
    with pytest.raises(ValueError):
        m.merge_observations(spec(), None, [bad], [], "now", date(2026, 9, 13))


def test_changed_definition_cannot_splice_history():
    original = spec()
    saved, _ = m.merge_observations(original, None, [row("2026-09-01", 1)], [], "now", date(2026, 9, 13))
    changed = dict(original, unit="USD")
    with pytest.raises(ValueError):
        m.merge_observations(changed, saved, [row("2026-09-02", 2)], [], "now", date(2026, 9, 13))


def test_failures_keep_last_good_history_and_mark_status(tmp_path):
    registry = {"schema": "market-source-registry-v1", "sources": [spec()]}
    client = m.HttpClient()
    m.collect(registry, tmp_path, client, date(2016, 1, 1), date(2026, 9, 13), write=True,
              fetcher=lambda *args: [row("2026-09-10", 3.2)])
    before = (tmp_path / "series/test_series.json").read_bytes()

    def fail(*args):
        raise RuntimeError("offline")

    result, updated = m.collect(registry, tmp_path, client, date(2016, 1, 1), date(2026, 9, 13), write=True,
                                fetcher=fail, refresh_hours=0)
    assert not updated
    assert result["sources"][0]["status"] == "failed"
    assert result["sources"][0]["latest"]["value"] == 3.2
    assert (tmp_path / "series/test_series.json").read_bytes() == before


def test_incremental_fetch_overlaps_and_backfill_uses_original_start(tmp_path):
    registry = {"schema": "market-source-registry-v1", "sources": [spec()]}
    calls = []

    def fetch(spec, client, start, end):
        calls.append(start)
        return [row("2026-09-10", 3.2)]

    client = m.HttpClient()
    for backfill in (False, False, True):
        m.collect(registry, tmp_path, client, date(2016, 1, 1), date(2026, 9, 13), write=True,
                  fetcher=fetch, refresh_hours=0, backfill=backfill)
    assert calls == ["2016-01-01", "2026-08-06", "2016-01-01"]


def test_periods_show_true_baseline_and_missing_history():
    definition = spec()
    saved, _ = m.merge_observations(definition, None, [row("2025-09-10", 10), row("2026-09-10", 20)], [], "now", date(2026, 9, 13))
    summary = m.summarize_series(definition, saved, {"status": "ok"}, date(2026, 9, 13))
    assert summary["periods"][0]["status"] == "insufficient_history"
    assert summary["periods"][-1]["actual_start"] == "2025-09-10"
    assert summary["periods"][-1]["delta"] == 10


def test_filing_versions_select_latest_known_release_not_append_order():
    saved = {"data_mode": "filing_versions", "observations": [
        row("2024-12-31", 20, "v2", "2025-02-01"),
        row("2024-12-31", 10, "v1", "2025-01-01"),
        row("2024-12-31", 30, "v3", "2027-01-01"),
    ]}
    assert m.current_observations(saved, date(2026, 9, 13))[0]["value"] == 20


def test_credentials_are_redacted(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "private-key-123")
    client = m.HttpClient()
    client.get_env("FRED_API_KEY")
    assert "private-key-123" not in client.redact("error api_key=private-key-123")
    with pytest.raises(ValueError):
        client.get_text("https://untrusted.invalid/data")


def test_env_file_is_literal_and_only_accepts_data_service_names(tmp_path, monkeypatch):
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    path = tmp_path / "credentials"
    path.write_text("FRED_API_KEY='literal-$(not-a-command)'\n", encoding="utf-8")
    m.load_credentials(path)
    assert m.HttpClient().get_env("FRED_API_KEY") == "literal-$(not-a-command)"
    path.write_text("OPENAI_API_KEY=unexpected\n", encoding="utf-8")
    with pytest.raises(ValueError):
        m.load_credentials(path)


def test_official_redirect_does_not_allow_http_downgrade():
    with pytest.raises(ValueError):
        m.OfficialRedirect().redirect_request(None, None, 302, "", {}, "http://fred.stlouisfed.org/")


def test_twse_resume_uses_recent_verified_raw_month_without_redownload(tmp_path):
    body = b'{"stat":"OK"}'
    sha = hashlib.sha256(body).hexdigest()
    url = "https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date=20160101"
    receipt = {"url": url, "raw_hash": sha, "retrieved_at": datetime.now(timezone.utc).isoformat()}
    (tmp_path / (sha + ".txt.gz")).write_bytes(gzip.compress(body))
    (tmp_path / (sha + ".receipt.json")).write_text(json.dumps(receipt))
    client = m.HttpClient(tmp_path)
    assert client.get_json(url) == {"stat": "OK"}
    assert client.receipts == [receipt]
    (tmp_path / (sha + ".txt.gz")).write_bytes(gzip.compress(b'changed'))
    with pytest.raises(ValueError, match="雜湊"):
        client.get_json(url)


def test_row_provenance_must_come_from_this_fetch_and_can_select_one_month():
    observation = dict(row("2026-09-01", 1), raw_hashes=["month-one"])
    saved, _ = m.merge_observations(spec(), None, [observation], [{"raw_hash": "month-one"}, {"raw_hash": "month-two"}], "now", date(2026, 9, 13))
    assert saved["observations"][0]["raw_hashes"] == ["month-one"]
    with pytest.raises(ValueError, match="原始回應"):
        m.merge_observations(spec(), None, [observation], [], "now", date(2026, 9, 13))


def test_partial_backfill_saves_progress_but_cannot_report_success(tmp_path):
    from market_sources_global import PartialHistoryError
    registry = {"schema": "market-source-registry-v1", "sources": [spec()]}

    def interrupted(*args):
        raise PartialHistoryError("source rate limited", [row("2020-01-01", 1)])

    result, updated = m.collect(registry, tmp_path, m.HttpClient(), date(2016, 1, 1), date(2026, 9, 13),
                                write=True, fetcher=interrupted)
    assert updated == ["test_series"]
    assert result["sources"][0]["status"] == "partial_history"
    assert result["sources"][0]["last_success_at"] is None
    assert result["sources"][0]["latest"]["date"] == "2020-01-01"
    assert (tmp_path / "series/test_series.json").exists()


def test_state_integration_preserves_old_quote_and_exposes_conflict():
    evidence = {"quotes": {"monitor:vix": {"num": 10, "as_of": "2026-09-10"}}}
    source = {"schema": "market-source-evidence-v1", "quotes": {"source:cboe_vix": {"num": 11, "as_of": "2026-09-10"}},
              "sources": [{"id": "cboe_vix", "label": "VIX", "compare_ref": "monitor:vix", "status": "ok"}]}
    result = state_builder.attach_source_evidence(evidence, source, [])
    assert evidence["quotes"]["monitor:vix"]["num"] == 10
    assert result["conflicts"][0]["source_value"] == 11
    source["quotes"] = {"monitor:vix": {"num": 12}}
    with pytest.raises(ValueError):
        state_builder.attach_source_evidence(evidence, source, [])


def test_latest_revised_keeps_newer_published_version_regardless_of_append_order():
    # 2026-09-13：EIA 這類帶發布日的 latest_revised 序列，較舊發布日不得因晚附加而蓋掉新版。
    saved = {"data_mode": "latest_revised", "observations": [
        row("2024-01-03", 105.0, None, "2024-01-24"),
        row("2024-01-03", 999.0, None, "2024-01-05"),
    ]}
    assert m.current_observations(saved, date(2026, 9, 13))[0]["value"] == 105.0
    unversioned = {"data_mode": "latest_revised", "observations": [row("2024-01-03", 1), row("2024-01-03", 2)]}
    assert m.current_observations(unversioned, date(2026, 9, 13))[0]["value"] == 2


def test_percentile_reports_actual_window_start_and_null_fields_when_empty():
    # 2026-09-13：短歷史的分位要帶實際起點；沒有觀測值時欄位以 null 明示而不是缺鍵。
    definition = spec()
    saved, _ = m.merge_observations(definition, None, [row("2026-08-%02d" % d, d) for d in range(1, 25)], [], "now", date(2026, 9, 13))
    summary = m.summarize_series(definition, saved, {"status": "ok"}, date(2026, 9, 13))
    assert summary["percentile_from"] == "2026-08-01" and summary["percentile_sample"] == 24
    empty = m.summarize_series(definition, None, {"status": "blocked_credentials"}, date(2026, 9, 13))
    assert empty["percentile"] is None and empty["percentile_from"] is None and empty["stale"] is None
