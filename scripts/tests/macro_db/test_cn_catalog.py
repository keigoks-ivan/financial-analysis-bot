"""中國目錄（catalog/cn.json）完整性檢查：離線。"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from macro_db.sources import REGISTRY

CATALOG = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "cn.json"
REQUIRED = ["sid", "label_zh", "source", "freq", "unit", "sa", "license", "display", "axis"]
# 每個 fetcher 的 params 至少要有的鍵
PARAM_KEYS = {
    "cn_nbs": {"probe_url"},
    "cn_pbc": {"sec", "table", "kind", "probe_url"},
    "cn_chinamoney": {"kind", "probe_url"},
    "cn_chinabond": {"term", "probe_url"},
    "cn_csindex": {"index_code", "probe_url"},
    "intl_bis": {"dataflow", "key", "probe_url"},
}


@pytest.fixture(scope="module")
def cat():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def all_series(cat):
    for c in cat["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                yield c["key"], ch, s


def test_catalog_top_level(cat):
    assert cat["country"] == "cn" and cat["name_zh"] == "中國"
    assert [c["key"] for c in cat["categories"]] == ["gdp", "monthly", "consumption", "investment", "prices", "trade", "housing", "industry", "finance", "new_productivity"]
    for rec in cat["todo"]:
        assert rec["reason"] and rec["chart"]
    for rec in cat["unavailable"]:
        assert rec["reason"]


def test_every_series_has_required_fields(cat):
    for _, ch, s in all_series(cat):
        for k in REQUIRED:
            assert k in s, (s.get("sid"), k)
        assert s["sid"].startswith("cn.")
        assert s["freq"] in {"D", "W", "M", "Q", "A"}
        assert s["sa"] in {"SA", "NSA", "SAAR", "n/a"}
        assert s["license"] == "public" or s["license"].startswith("copyright:")
        assert s["axis"] in {"L", "R"}
        assert ch["series"], ch["key"]            # 不放空圖


def test_same_sid_means_same_source(cat):
    seen = {}
    for _, ch, s in all_series(cat):
        key = (s.get("fetcher"), json.dumps(s.get("params"), sort_keys=True), s["freq"], s["unit"], s["display"], s.get("yoy_from"))
        assert seen.setdefault(s["sid"], key) == key, s["sid"]


def test_fetchers_registered_and_params_complete(cat):
    for _, ch, s in all_series(cat):
        if s.get("derived"):
            assert "fetcher" not in s
            continue
        f = s["fetcher"]
        assert f in REGISTRY and (f.startswith("cn_") or f == "intl_bis"), (s["sid"], f)
        missing = PARAM_KEYS[f] - set(s["params"])
        assert not missing, (s["sid"], missing)
        urls = [v for v in s["params"].values() if isinstance(v, str) and v.startswith("http")]
        assert urls, s["sid"]                        # CI probe 要靠完整網址


def test_registered_cn_modules_expose_fetch():
    for name, path in REGISTRY.items():
        if name.startswith("cn_"):
            assert callable(importlib.import_module(path).fetch)


def test_nbs_series_have_name_or_parts(cat):
    for _, ch, s in all_series(cat):
        if s.get("fetcher") != "cn_nbs":
            continue
        p = s["params"]
        if "parts" in p:
            assert len(p["parts"]) >= 2 and all(x["cid"] and x["name"] for x in p["parts"]), s["sid"]
        else:
            assert len(p["cid"]) == 32 and p["name"], s["sid"]
        assert p.get("tree", "M") == ("Q" if s["freq"] == "Q" else "M"), s["sid"]


def test_yoy_series_declare_how_the_source_is_expressed(cat):
    """國統局的 yoy 一律是來源已給的年增率：idx100（上年同期＝100 指數）或 pct（%）；不自行用水準值再算。"""
    for _, ch, s in all_series(cat):
        if s.get("fetcher") == "cn_nbs" and s["display"] == "yoy":
            assert s.get("yoy_from") in ("idx100", "pct"), s["sid"]
        if s.get("yoy_from") == "idx100":
            assert s["unit"].startswith("指數（上年同"), s["sid"]
        if s.get("yoy_from") == "pct":
            assert s["unit"] == "%", s["sid"]


def test_derived_series_reference_existing_sids(cat):
    sids = {s["sid"] for _, _, s in all_series(cat)}
    for _, _, s in all_series(cat):
        for x in (s.get("derived") or {}).get("sids", []):
            assert x in sids, (s["sid"], x)
        if s.get("derived"):
            assert s.get("self_calc")


def test_daily_history_notes_and_snapshots(cat):
    by = {s["sid"]: s for _, _, s in all_series(cat)}
    assert "累積" in by["cn.cgb_10y"]["history_note"] and "2026 年 10 月" in by["cn.cgb_10y"]["history_note"]
    assert by["cn.csi300"]["license"].startswith("copyright:中證指數有限公司")
    assert by["cn.csi300"]["source"] == "中證指數有限公司"


def test_overlay_sources_named(cat):
    by = {s["sid"]: s for _, _, s in all_series(cat)}
    assert "國家統計局" in by["cn.m2_level"]["source"] and "中國人民銀行" in by["cn.m2_level"]["source"]
    assert "新聞稿" in by["cn.pmi_mfg"]["source"] and by["cn.pmi_mfg"]["notes"]
    for sid in ("cn.m2_level", "cn.pmi_mfg"):
        assert "overlay" in by[sid]["params"]


def test_no_hk_no_szse_and_placeholders_kept_out(cat):
    sids = {s["sid"] for _, _, s in all_series(cat)}
    assert "cn.szse_component" not in sids and not any(x.startswith("cn.hk") for x in sids)
    assert any("深圳證券交易所" in u["reason"] or "szse" in u["reason"] for u in cat["unavailable"])
    assert any(t["chart"].startswith("hk-") and "另立區" in t["reason"] for t in cat["todo"])


def test_priority_rule(cat):
    for c in cat["categories"]:
        for ch in c["charts"]:
            assert ch["priority"] in (1, 2)
    assert all(rec["priority"] in (1, 2, 3) for rec in cat["todo"])
