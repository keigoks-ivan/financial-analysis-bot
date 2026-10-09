"""東南亞目錄（catalog/an.json＋各國分檔 an_<國碼>.json）完整性檢查：離線。"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from macro_db import catalog_io
from macro_db.sources import REGISTRY

CATALOG = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "an.json"
REQUIRED = ["sid", "label_zh", "source", "freq", "unit", "sa", "license", "display", "axis", "fetcher", "params"]
PARAM_KEYS = {
    "intl_imf": {"dataflow", "key"},
    "intl_bis": {"dataflow", "key"},
    "intl_worldbank": {"indicator", "country"},
    "an_singstat": {"table_id", "row"},
    "an_opendosm": {"id", "field"},
}


PARTS = ["vn", "my", "th", "id", "sg"]


@pytest.fixture(scope="module")
def main():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def cat():
    return catalog_io.load_catalog("an")


def all_series(cat):
    for c in cat["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                yield c["key"], ch, s


def test_top_level(main, cat):
    assert main["country"] == "an"
    assert [c["key"] for c in main["categories"]] == ["asean", "tradewar"]
    assert main["categories"][0]["name_zh"] == "東南亞總覽"
    assert all(c["group"] == "五國對照" for c in main["categories"])
    assert main["parts"] == PARTS
    keys = {c["key"] for c in cat["categories"]}
    for old, new in main["redirects"].items():
        assert old in PARTS and new == old + "-gdp"
        if (CATALOG.parent / f"an_{old}.json").exists():
            assert new in keys, new
    for rec in cat["todo"]:
        assert rec["reason"] and rec["chart"] and rec["priority"] in (2, 3)
    for rec in cat["unavailable"]:
        assert rec["reason"]


def test_series_fields_and_probe_url(cat):
    for _, ch, s in all_series(cat):
        for k in REQUIRED:
            assert k in s, (s.get("sid"), k)
        assert s["freq"] in {"D", "W", "M", "Q", "A"}
        assert s["sa"] in {"SA", "NSA", "SAAR", "n/a"}
        assert s["license"] == "public" or s["license"].startswith("copyright:")
        assert s["axis"] in {"L", "R"}
        assert s["params"]["probe_url"].startswith("http")
        assert "ref_sids" not in ch


def test_sid_prefix_and_part_keys(cat):
    for c in cat["categories"]:
        part = c.get("part")
        if part:
            assert c["key"].startswith(part + "-"), c["key"]
        for ch in c["charts"]:
            for s in ch["series"]:
                assert s["sid"].startswith("an.") or (part and s["sid"].startswith(part + ".")), s["sid"]


def test_same_sid_same_spec_everywhere(cat):
    seen = {}
    for _, ch, s in all_series(cat):
        key = {k: v for k, v in s.items() if k not in ("axis", "display")}   # 同一序列可在同圖以水準值與年增率各用一次
        assert seen.setdefault(s["sid"], key) == key, s["sid"]


def test_fetchers_registered_and_params_complete(cat):
    for _, ch, s in all_series(cat):
        f = s["fetcher"]
        assert f in REGISTRY and (f.startswith("an_") or f.startswith("intl_")), f
        assert PARAM_KEYS.get(f, set()) <= set(s["params"]), s["sid"]
        assert callable(importlib.import_module(REGISTRY[f]).fetch)


def test_no_philippines(cat):
    assert all(not s["sid"].endswith("_ph") and s["fetcher"] != "an_psa" for _, _, s in all_series(cat))
    assert any(t["category"] == "ph" and "菲律賓之後再加" in t["reason"] for t in cat["todo"])


def test_no_needs_key_series_collected(cat):
    sids = {s["sid"] for _, _, s in all_series(cat)}
    for gone in ("an.th_mpi", "an.id_ip", "an.th_money", "an.vn_gdp_q_gso", "an.my_money_bm"):
        assert gone not in sids
    texts = " ".join(u["reason"] for u in cat["unavailable"])
    assert "apiportal.bot.or.th" in texts and "webapi.bps.go.id" in texts


def test_slow_series_have_stale_days(cat):
    for _, _, s in all_series(cat):
        if s["sid"] in ("an.th_exports", "an.th_imports", "an.id_exports", "an.id_imports", "an.reserves_th"):
            assert s.get("stale_days"), s["sid"]


def test_stale_has_reason(cat):
    for _, _, s in all_series(cat):
        if s.get("stale_days"):
            assert s.get("stale_reason"), s["sid"]
