"""2026-09-13：防止週更時間掩蓋歷史評分，並驗證共用市場判讀的顯示邊界。"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import build_regime as regime
import build_market_state as market


def build(tmp_path, monkeypatch, missing=False):
    cot = {"markets": {code: {"series": [["2026-09-08", 1.0]]}
                       for code, _, _ in regime.REGIME_COT_MARKETS}}
    path = tmp_path / "cot.json"
    path.write_text(json.dumps(cot))
    ratios = [{"key": r["key"], "name": r["name"], "reading": r["reading"],
               "pos_0to1": r["pos"], "mechanical": {"as_of": "2026-09-07", "value": 1.0,
               "pctile_2y": 50.0, "chg_12m_pct": 0.0}} for r in regime.RATIOS_EDITORIAL]
    monkeypatch.setattr(regime, "build_price_cache", lambda *a: {})
    monkeypatch.setattr(regime, "ratio_compute", lambda *a: (ratios, []))
    if missing:
        monkeypatch.setattr(regime, "cot_compute", lambda *a: ([], None, []))
        monkeypatch.setattr(regime, "ratio_compute", lambda *a: ([], []))
    monkeypatch.setattr(sys, "argv", ["build_regime", "--skip-fetch", "--out-dir", str(tmp_path),
                                     "--cot-history", str(path)])
    regime.main()
    return json.loads((tmp_path / "data/latest.json").read_text())


def test_weekly_refresh_never_redates_editorial(tmp_path, monkeypatch):
    p = build(tmp_path, monkeypatch)
    assert p["meta"]["data_as_of"] == "2026-09-07"
    assert p["historical_editorial"]["as_of"] == "2026-07-06"
    assert p["composite"] == {} and p["axes"] == [] and p["triggers"] == []
    assert "2026-06-23" not in p["meta"]["cot_note"]
    assert all("reading" not in r for r in p["growth_defense_ratios"])
    html = regime.render_dashboard(p)
    assert "歷史評分（非本期判讀）" in html
    assert "HG=F/GC=F" in html and "HYG/LQD" in html
    assert "2026-09-08" in html and "2026-09-07" in html


def test_noop_preserves_timestamp_and_failure_preserves_artifact(tmp_path, monkeypatch):
    build(tmp_path, monkeypatch)
    path = tmp_path / "data/latest.json"
    before = path.read_bytes()
    build(tmp_path, monkeypatch)
    assert path.read_bytes() == before
    with pytest.raises(SystemExit):
        build(tmp_path, monkeypatch, missing=True)
    assert path.read_bytes() == before


def test_cot_retains_each_markets_actual_date():
    codes = [x[0] for x in regime.REGIME_COT_MARKETS[:2]]
    rows, latest, _ = regime.cot_compute({"markets": {
        codes[0]: {"series": [["2026-09-01", -1.0]]},
        codes[1]: {"series": [["2026-09-08", 2.0]]}}})
    assert {x["as_of"] for x in rows} == {"2026-09-01", "2026-09-08"}
    assert latest == "2026-09-08"


def test_small_ratio_retains_useful_precision():
    from datetime import date, timedelta
    dates = [(date(2025, 9, 1) + timedelta(weeks=i)).isoformat() for i in range(53)]
    ratios, _ = regime.ratio_compute({"HG=F": [(d, 6.4695) for d in dates],
                                     "GC=F": [(d, 4366.2) for d in dates]})
    assert ratios[0]["mechanical"]["value"] == round(6.4695 / 4366.2, 8)


def test_partial_coverage_cannot_claim_a_complete_fresh_date(tmp_path, monkeypatch):
    original = regime.cot_compute
    monkeypatch.setattr(regime, "cot_compute", lambda h: (original(h)[0][1:], "2026-09-08", []))
    p = build(tmp_path, monkeypatch)
    assert p["meta"]["data_as_of"] is None
    assert "部分資料缺漏" in regime.render_dashboard(p)


def test_market_and_intel_use_observations_not_legacy_score(tmp_path, monkeypatch):
    from datetime import date
    p = build(tmp_path, monkeypatch)
    tile = market.build_environment(p, {}, {}, {}, {}, {}, date(2026, 9, 13), [])[0]
    assert tile["as_of"] == "2026-09-07" and not tile["stale"]
    assert "0.63" not in tile["sub"] and tile["tone"] == "neutral"
    spec = importlib.util.spec_from_file_location("regime_test_intel_render", SCRIPTS / "intel/render.py")
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    monkeypatch.setattr(renderer, "load_json_safe", lambda *a: p)
    html = renderer.render_weekly_regime()
    assert "晚週期再通脹" not in html
    assert "週線標記日" in html and "2026-09-08" in html


@pytest.mark.skipif(not shutil.which("node"), reason="Node is needed for frontend contract checks")
def test_shared_release_missing_future_unreviewed_and_escaped_values():
    js = SCRIPTS.parent / "docs/regime/current.js"
    code = r'''
const assert = require('assert');
const ui = require(process.argv[1]);
const now = Date.parse('2026-09-13T12:00:00Z');
const q = {'monitor:dxy': {num: 99, val: '<script>bad</script>', as_of:'2026-09-11'}};
let h = ui.render({state:{evidence:{quotes:q}}, refresh:{status:'needs_review'},
 read:{as_of:'2026-09-13', thesis_zh:'unapproved'}}, now);
assert(h.includes('等待重評') && !h.includes('unapproved'));
assert(h.includes('&lt;script&gt;') && !h.includes('<script>bad'));
assert(h.includes('缺少有效觀測'));
assert(ui.quoteHTML('x', {x:{num:12345,val:'12345',as_of:'2026-09-14'}}, now).includes('缺少有效觀測'));
h = ui.render({read:{as_of:'bad-date',review:{verdict:'pass'},thesis_zh:'invalid'}}, now);
assert(!h.includes('invalid'));
h = ui.render({read:{as_of:'2026-07-06',valid_days:10,review:{verdict:'pass'},thesis_zh:'approved'}}, now);
assert(h.includes('approved') && h.includes('超過有效期'));
h = ui.render({refresh:{status:'needs_review'},read:{as_of:'2026-09-13',review:{verdict:'pass'},thesis_zh:'prior'}}, now);
assert(h.includes('prior') && h.includes('上一份判讀（等待重評）') && h.includes('尚未依本次新資料重評'));
h = ui.render({refresh:{status:'blocked'},read:{as_of:'2026-09-13',review:{verdict:'pass'},thesis_zh:'blocked-thesis'}}, now);
assert(!h.includes('blocked-thesis'));
'''
    subprocess.run([shutil.which("node"), "-e", code, str(js)], check=True)


def test_intel_frontpage_does_not_reuse_archived_regime_label(monkeypatch):
    spec = importlib.util.spec_from_file_location("regime_frontpage_render", SCRIPTS / "intel/render.py")
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    monkeypatch.setattr(renderer, "load_json_safe", lambda path: {"schema": "regime-observations-v2"}
                        if path == renderer.REGIME_LATEST_FILE else {})
    payload = {"date": "2026-09-12", "gauges": [{"category": "regime", "value": "OLD_REGIME",
               "metric": "regime"}], "site_read_zh": "OLD_RESEARCH"}
    current = renderer.build_day_body("2026-09-12", payload, "", False)
    archived = renderer.build_day_body("2026-09-12", payload, "", True)
    assert "OLD_REGIME" not in current and "OLD_RESEARCH" not in current
    assert "OLD_REGIME" in archived and "OLD_RESEARCH" in archived
    assert payload["gauges"][0]["value"] == "OLD_REGIME"
