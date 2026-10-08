"""日本目錄（catalog/jp.json）完整性檢查：離線。"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from macro_db.sources import REGISTRY

CATALOG = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "jp.json"
REQUIRED = ["sid", "label_zh", "source", "freq", "unit", "sa", "license", "display", "axis"]
# 每個 fetcher 的 params 至少要有的鍵（kind 為 None 代表沒有 kind）
PARAM_KEYS = {
    "jp_boj": {None: {"db", "code", "url"}, "cpirev": {"url", "cols", "col_label"}},
    "jp_esri": {"gdp": {"table", "col", "col_check", "url"}, "ci": {"col", "col_check", "url"},
                "watcher": {"sheet", "col_label", "url"}, "machinery": {"sheet", "col", "col_check", "url"}},
    "jp_stat": {None: {"item", "files", "url"}},
    "jp_estat_file": {"lfs": {"sheet", "col", "col_check", "url"}, "wage": {"expect", "url"},
                      "iip": {"sheet", "item", "url"}},
    "jp_mof": {"jgb": {"url", "recent_url", "tenor"}, "reserves": {"url", "col", "col_check", "scale"}},
    "jp_customs": {None: {"url", "col_name", "scale"}},
    "jp_misc": {"jnto": {"page"}, "mlit": {"page", "sheet", "col", "col_check"}},
    "fred": {None: {"id"}},
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
    assert cat["country"] == "jp"
    assert len(cat["categories"]) == 8
    for rec in cat["todo"]:
        assert rec["reason"] and rec["chart"]
    for rec in cat["unavailable"]:
        assert rec["reason"]


def test_every_series_has_required_fields(cat):
    for _, ch, s in all_series(cat):
        for k in REQUIRED:
            assert k in s, (s.get("sid"), k)
        assert s["sid"].startswith("jp.")
        assert s["freq"] in {"D", "W", "M", "Q", "A"}
        assert s["sa"] in {"SA", "NSA", "SAAR", "n/a"}
        assert s["license"] == "public" or s["license"].startswith("copyright:")
        assert s["axis"] in {"L", "R"}
        assert ("fetcher" in s and "params" in s) != ("derived" in s), s["sid"]


def test_same_sid_means_same_source(cat):
    seen = {}
    for _, ch, s in all_series(cat):
        key = (s.get("fetcher"), json.dumps(s.get("params"), sort_keys=True), s["freq"],
               json.dumps(s.get("derived"), sort_keys=True))
        assert seen.setdefault(s["sid"], key) == key, s["sid"]


def test_fetchers_registered_and_params_complete(cat):
    for _, ch, s in all_series(cat):
        if "derived" in s:
            continue
        f = s["fetcher"]
        assert f in PARAM_KEYS and (f == "fred" or f in REGISTRY), f
        schema = PARAM_KEYS[f]
        kind = s["params"].get("kind")
        assert kind in schema or (kind is None and None in schema), (s["sid"], kind)
        missing = schema[kind] - set(s["params"])
        assert not missing, (s["sid"], missing)


def test_probe_urls_are_full_urls(cat):
    for _, _, s in all_series(cat):
        if "derived" in s:
            continue
        p = s["params"]
        u = p.get("url") or p.get("probe_url") or p.get("page")
        assert u and u.startswith("https://"), s["sid"]


def test_registered_modules_expose_fetch():
    for name, path in REGISTRY.items():
        if name.startswith("jp_"):
            assert callable(importlib.import_module(path).fetch)


def test_derived_inputs_exist(cat):
    sids = {s["sid"] for _, _, s in all_series(cat)}
    us = {"us.dgs10", "us.dgs2"}
    for _, _, s in all_series(cat):
        for d in s.get("derived", {}).get("sids", []):
            assert d in sids or d in us, (s["sid"], d)


def test_priority_rule_no_priority3_charts(cat):
    for c in cat["categories"]:
        for ch in c["charts"]:
            assert ch["priority"] in (1, 2)
    assert all(rec["priority"] in (2, 3) for rec in cat["todo"])


def test_estat_key_items_listed_unavailable(cat):
    charts = {u.get("chart") for u in cat["unavailable"]}
    for k in ["job-ratio", "retail", "consumer-confidence", "household-spending", "housing-starts",
              "construction-orders", "tertiary-activity"]:
        assert k in charts, k
    assert any("需 e-Stat API 金鑰" in u["reason"] for u in cat["unavailable"])


def test_nikkei_labelled_copyright(cat):
    n = next(s for _, _, s in all_series(cat) if s["sid"] == "jp.nikkei225")
    assert n["source"] == "日本經濟新聞社，經 FRED" and n["license"].startswith("copyright:日本經濟新聞社")


def test_cpi_charts_have_history_note(cat):
    for c in cat["categories"]:
        for ch in c["charts"]:
            if any(s.get("fetcher") == "jp_stat" for s in ch["series"]):
                assert any(s.get("history_note") for s in ch["series"]), ch["key"]
