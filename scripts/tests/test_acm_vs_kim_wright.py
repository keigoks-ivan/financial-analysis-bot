"""2026-10-19：ACM（紐約聯準會）與 Kim–Wright（FRED THREEFYTP10，monitor tp10y）不可互換。

證偽門檻寫的是 ACM，就必須用 ACM 序列（總經資料庫 us.acm_tp10）判斷；
收割程式不得把 ACM 門檻綁到 monitor tp10y。
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import build_kill_watch as bkw  # noqa: E402
import harvest_macro_falsifiers as hmf  # noqa: E402


# ── kill_watch：macro_db 資料來源 ─────────────────────────────────────────

def test_macro_db_source_reads_last_row(tmp_path, monkeypatch):
    (tmp_path / "us.acm_tp10.csv").write_text(
        "date,value\n2026-10-13,0.851455\n2026-10-14,0.808603\n2026-10-15,0.747453\n",
        encoding="utf-8")
    monkeypatch.setattr(bkw, "MACRO_DB_SERIES", str(tmp_path))
    cur, asof, err = bkw.get_current({"type": "macro_db", "key": "us.acm_tp10"}, {}, {})
    assert err is None
    assert cur == pytest.approx(0.747453)
    assert asof == "2026-10-15"


def test_macro_db_source_missing_series_is_unknown_not_guess(tmp_path, monkeypatch):
    monkeypatch.setattr(bkw, "MACRO_DB_SERIES", str(tmp_path))
    cur, asof, err = bkw.get_current({"type": "macro_db", "key": "us.nope"}, {}, {})
    assert cur is None and err


@pytest.mark.parametrize("bad", ["../registry", "us/acm_tp10", "", None])
def test_macro_db_source_rejects_path_tricks(bad, tmp_path, monkeypatch):
    monkeypatch.setattr(bkw, "MACRO_DB_SERIES", str(tmp_path))
    cur, _, err = bkw.get_current({"type": "macro_db", "key": bad}, {}, {})
    assert cur is None and err


def test_real_acm_series_is_below_registry_threshold_levels():
    """repo 內的 ACM 序列真的存在、最後一筆是 ACM（不是 Kim–Wright）。"""
    pts = bkw._macro_db_points("us.acm_tp10")
    kw = bkw._macro_db_points("us.threefytp10")
    assert pts and kw
    assert pts[0][0] == "1961-06-14"  # ACM 從 1961 起；Kim–Wright 1990 年才開始
    assert kw[0][0] > "1980"


# ── 登記表：ACM 門檻必須綁 ACM 序列 ────────────────────────────────────────

def _registry_mechanical():
    reg = json.loads((ROOT / "docs/detective/data/kill_registry.json").read_text(encoding="utf-8"))
    return [it for it in reg["items"] if it["parse"].get("mode") == "mechanical"]


def test_registry_acm_items_use_acm_series():
    acm = [it for it in _registry_mechanical()
           if hmf.ACM_RE.search(it["metric_text"]) and "term premium" in it["metric_text"].lower()]
    assert acm, "登記表應有 ACM 期限溢價的機械門檻"
    for it in acm:
        assert it["parse"]["data_source"] == {"type": "macro_db", "key": "us.acm_tp10"}, it["id"]


def test_registry_no_acm_text_bound_to_kim_wright():
    for it in _registry_mechanical():
        if hmf.ACM_RE.search(it["metric_text"] + " " + it["threshold_text"]):
            assert it["parse"]["data_source"].get("key") != "rates/tp10y", it["id"]


def test_kill_watch_snapshot_acm_items_use_acm_series():
    kw = json.loads((ROOT / "docs/detective/data/kill_watch.json").read_text(encoding="utf-8"))
    acm = [it for it in kw["items"] if hmf.ACM_RE.search(it["metric_text"])]
    assert acm
    for it in acm:
        assert it["data_source"] == {"type": "macro_db", "key": "us.acm_tp10"}, it["id"]


# ── 收割程式：ACM 不收、Kim–Wright 才綁 tp10y ───────────────────────────────

@pytest.mark.parametrize("text,hit", [
    ("ACM 10 年期期限溢價 紐約聯準會 ACM", True),
    ("NY Fed ACM", True),
    ("ACM term premium 回落", True),
    ("ACME 公司", False),
    ("AECOM", False),
    ("Kim–Wright 10Y term premium", False),
])
def test_acm_regex(text, hit):
    assert bool(hmf.ACM_RE.search(text)) is hit


def test_series_map_has_no_acm_needle_for_tp10y():
    for needle, keys in hmf.SERIES_MAP:
        if "tp10y" in keys:
            assert "ACM" not in needle
            assert any(w in needle for w in ("Kim", "THREEFYTP10"))


def _macro_html(metrics, refresh_due):
    meta = {"refresh_due": refresh_due, "kill_metrics": metrics}
    return ('<html><script type="application/json" id="macro-meta">'
            + json.dumps(meta, ensure_ascii=False) + "</script></html>")


def test_harvest_skips_acm_and_binds_kim_wright_only_to_tp10y(tmp_path, monkeypatch):
    due = (date.today() + timedelta(days=60)).isoformat()
    mdir = tmp_path / "macro"
    mdir.mkdir()
    (mdir / "MACRO_Fake_20261019.html").write_text(_macro_html([
        {"metric": "ACM 10 年期期限溢價", "threshold": "站上 1.0%", "source": "紐約聯準會 ACM"},
        {"metric": "ACM 10Y term premium 突破", "threshold": ">1.0%", "source": "NY Fed ACM"},
        {"metric": "10 年期期限溢價（Kim–Wright）", "threshold": "站上 1.2%",
         "source": "FRED THREEFYTP10"},
    ], due), encoding="utf-8")
    mon = tmp_path / "latest.json"
    mon.write_text(json.dumps({"categories": [{"key": "rates", "items": [
        {"key": "tp10y", "label": "10Y 期限溢價（Kim–Wright）", "val": "1.07%", "date": "2026-10-09"},
    ]}]}), encoding="utf-8")
    monkeypatch.setattr(hmf, "MACRO_DIR", mdir)
    monkeypatch.setattr(hmf, "MONITOR_LATEST", mon)

    drafts, skipped, _ = hmf.harvest(ledger_path=tmp_path / "none.jsonl")

    skipped_acm = [s for s in skipped if "ACM" in s[1]]
    assert len(skipped_acm) == 2
    assert len(drafts) == 1
    d = drafts[0]
    assert d["resolver"]["series"] == "monitor:tp10y"
    assert "ACM" not in d["claim"].replace("Kim–Wright", "")
    assert d["resolver"]["value"] == 1.2
