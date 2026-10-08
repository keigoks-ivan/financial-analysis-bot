"""歐洲目錄（catalog/eu.json）完整性檢查：離線。"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from macro_db.sources import REGISTRY

CATALOG = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "eu.json"
REQUIRED = ["sid", "label_zh", "source", "freq", "unit", "sa", "license", "display", "axis", "fetcher", "params"]
PARAM_KEYS = {
    "eu_eurostat": {"dataset", "key", "url"},
    "eu_ecb": {"dataset", "key", "url"},
    "eu_smard": {"filter", "region", "resolution", "url"},
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
    assert cat["country"] == "eu"
    assert len(cat["categories"]) == 8
    for rec in cat["todo"]:
        assert rec["reason"] and rec["chart"]
    for rec in cat["unavailable"]:
        assert rec["reason"]


def test_every_series_has_required_fields(cat):
    for _, ch, s in all_series(cat):
        for k in REQUIRED:
            assert k in s, (s.get("sid"), k)
        assert s["sid"].startswith("eu.")
        assert s["freq"] in {"D", "W", "M", "Q", "A"}
        assert s["sa"] in {"SA", "NSA", "SAAR", "n/a"}
        assert s["license"] == "public" or s["license"].startswith("copyright:")
        assert s["axis"] in {"L", "R"}


def test_same_sid_means_same_source(cat):
    seen = {}
    for _, ch, s in all_series(cat):
        key = (s["fetcher"], json.dumps(s["params"], sort_keys=True), s["freq"], s["unit"], s["display"])
        assert seen.setdefault(s["sid"], key) == key, s["sid"]


def test_chart_keys_unique_and_composites_are_plain_charts(cat):
    keys = [ch["key"] for c in cat["categories"] for ch in c["charts"]]
    assert len(keys) == len(set(keys))
    assert "composites" not in cat
    by = {ch["key"]: ch for c in cat["categories"] for ch in c["charts"]}
    assert [s["sid"] for s in by["gdp-vs-esi"]["series"]] == ["eu.gdp_real", "eu.esi_ea"]
    assert {s["axis"] for s in by["gdp-vs-esi"]["series"]} == {"L", "R"}
    assert any(ch["key"] == "hicp-market" for ch in by.values())


def test_fetchers_registered_and_params_complete(cat):
    for _, ch, s in all_series(cat):
        f = s["fetcher"]
        assert f.startswith("eu_") and f in REGISTRY, f
        missing = PARAM_KEYS[f] - set(s["params"])
        assert not missing, (s["sid"], missing)
        assert s["params"]["url"].startswith("https://")


def test_registered_modules_expose_fetch():
    for name, path in REGISTRY.items():
        if name.startswith("eu_"):
            assert callable(importlib.import_module(path).fetch)


def test_hicp_uses_new_dataset_only(cat):
    for _, _, s in all_series(cat):
        if s["fetcher"] == "eu_eurostat":
            assert s["params"]["dataset"] not in ("prc_hicp_manr", "prc_hicp_midx")
    hicp = next(s for _, _, s in all_series(cat) if s["sid"] == "eu.hicp")
    assert hicp["params"]["dataset"] == "prc_hicp_minr" and hicp["display"] == "yoy"


def test_retail_is_seasonally_adjusted(cat):
    """sts_trtu_m 的 CA 只調日數、沒調季節，月變動會跳 ±40%；一律用 SCA。"""
    for _, _, s in all_series(cat):
        if s["params"].get("dataset") == "sts_trtu_m":
            assert ".SCA." in s["params"]["key"] and s["sa"] == "SA", s["sid"]


def test_changing_composition_series_say_so(cat):
    for _, _, s in all_series(cat):
        if s["fetcher"] == "eu_ecb" and s["params"]["dataset"] in ("BSI", "YC", "BLS", "ILM"):
            assert "歐元區成員逐年增加" in s["history_note"] and s.get("notes"), s["sid"]


def test_weekly_series_documented_as_friday(cat):
    ilm = [s for _, _, s in all_series(cat) if s["freq"] == "W"]
    assert ilm and all("星期五" in s["notes"] for s in ilm)


def test_flash_note_on_hicp(cat):
    s = next(s for _, _, s in all_series(cat) if s["sid"] == "eu.hicp")
    assert "快報" in s["history_note"]


def test_de_orders_moved_to_unavailable(cat):
    assert "eu.de_orders" not in {s["sid"] for _, _, s in all_series(cat)}
    assert any(u.get("chart") == "de-orders" and "金鑰" in u["reason"] for u in cat["unavailable"])


def test_spf_only_long_term_collected(cat):
    spf = [s for _, _, s in all_series(cat) if s["params"].get("dataset") == "SPF"]
    assert spf and all(".LT." in s["params"]["key"] for s in spf)
    assert any("SPF" in t["title_zh"] for t in cat["todo"])


def test_no_uk_series(cat):
    assert not [s for _, _, s in all_series(cat) if "英國" in s["label_zh"]]


def test_labels_use_fullwidth_punctuation(cat):
    import re
    bad = re.compile(r"[一-鿿][,.:;()]|[,.:;()][一-鿿]")
    for c in cat["categories"]:
        for ch in c["charts"]:
            assert not bad.search(ch["title_zh"]), ch["title_zh"]
            for s in ch["series"]:
                assert not bad.search(s["label_zh"]), s["label_zh"]
                assert not bad.search(s.get("history_note", "")), s["sid"]


def test_slow_series_have_stale_days(cat):
    sids = {s["sid"]: s for _, _, s in all_series(cat)}
    for sid in ("eu.gdp_real", "eu.labour_cost", "eu.hpi_ea", "eu.exp_cap", "eu.ip_ea"):
        assert sids[sid].get("stale_days") and sids[sid].get("stale_reason"), sid
