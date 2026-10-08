"""印尼分檔（catalog/an_id.json）結構測試：離線。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from macro_db import catalog_io
from macro_db.sources import REGISTRY

CATDIR = Path(__file__).resolve().parents[2] / "macro_db" / "catalog"


@pytest.fixture(scope="module")
def part():
    return json.loads((CATDIR / "an_id.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def main():
    return catalog_io.load_catalog("an")


def series(part):
    for c in part["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                yield c, ch, s


def test_shape(part):
    assert part["region"] == "an" and part["part"] == "id" and part["group"] == "印尼"
    keys = [c["key"] for c in part["categories"]]
    assert keys[0] == "id-gdp" and len(keys) == len(set(keys))
    assert 6 <= len(keys) <= 8
    for c in part["categories"]:
        assert c["key"].startswith("id-") and len(c["charts"]) >= 3, c["key"]


def test_chart_titles_start_with_country_and_keys_unique(part):
    seen = set()
    for _, ch, _s in series(part):
        pass
    for c in part["categories"]:
        for ch in c["charts"]:
            assert ch["title_zh"].startswith("印尼"), ch["title_zh"]
            assert ch["key"] not in seen and ch["key"] not in {x["key"] for x in part["categories"]}
            seen.add(ch["key"])


def test_sids_unique_and_prefixed(part):
    sids = [s["sid"] for _, _, s in series(part)]
    assert len(sids) == len(set(sids))
    for sid in sids:
        assert sid.startswith("id.") or sid.startswith("an."), sid


def test_reused_an_sids_identical_to_an_json(part):
    an = json.loads((CATDIR / "an.json").read_text(encoding="utf-8"))
    ref = {s["sid"]: s for c in an["categories"] for ch in c["charts"] for s in ch["series"]}
    reused = [s for _, _, s in series(part) if s["sid"] in ref]
    assert {s["sid"] for s in reused} >= {"an.id_gdp_real", "an.id_exports", "an.cbpol_id", "an.spp_id", "an.xru_id"}
    for s in reused:
        assert s == ref[s["sid"]], s["sid"]


def test_fields_and_fetchers(part):
    for _, _, s in series(part):
        for k in ("sid", "label_zh", "source", "freq", "unit", "sa", "license", "display", "axis", "fetcher", "params"):
            assert k in s, (s["sid"], k)
        assert s["fetcher"] in REGISTRY
        assert s["params"]["probe_url"].startswith("http")
        assert s["display"] != "yoy" or "年增率" not in s["label_zh"], s["sid"]
        if s["fetcher"] == "an_id_seki":
            assert {"table", "item"} <= set(s["params"]) and s["params"]["probe_url"].startswith("https://www.bi.go.id/SEKI/")
            assert "sheet" not in s["params"]
        if s["fetcher"] == "intl_oecd":
            assert {"dataflow", "key"} <= set(s["params"])


def test_seki_cpi_uses_new_base_only(part):
    cpi = [s for _, _, s in series(part) if s["sid"].startswith("id.cpi_")]
    seki = [s for s in cpi if s["fetcher"] == "an_id_seki"]
    assert len(seki) == 8
    for s in seki:
        assert s["params"]["start"] == "2024-01"        # 2024-01 改 2022=100 基期，舊基期不接
    assert any("history_note" in s for s in seki)


def test_spliced_series_name_old_sheet(part):
    spliced = [s for _, _, s in series(part) if s["params"].get("history")]
    assert {s["sid"] for s in spliced} == {"id.lr_wc", "id.lr_inv", "id.lr_cons", "id.dr_1m", "id.dr_3m", "id.dr_12m",
                                           "id.deposits", "id.loan_housing", "id.loan_flat", "id.loan_realest", "id.loan_constr"}
    assert any("history_note" in s for s in spliced)


def test_stale_has_reason_and_provisional_noted(part):
    for _, _, s in series(part):
        if s.get("stale_days"):
            assert s.get("stale_reason"), s["sid"]
        if s["fetcher"] == "an_id_seki":
            assert "暫定值" in s.get("notes", ""), s["sid"]


def test_excluded_items_not_collected(part):
    sids = {s["sid"] for _, _, s in series(part)}
    for gone in ("id.ipi_mfg", "id.cspi", "id.lq45", "id.wpi", "id.unemp_wb", "id.bci"):
        assert gone not in sids
    texts = " ".join(u["mm_ref"] + u["reason"] for u in json.loads((CATDIR / "an_id.json").read_text(encoding="utf-8"))["unavailable"])
    assert "製造業生產指數" in texts and "IDX" in texts or "證券交易所" in texts


def test_needs_key_items_are_todo(part):
    txt = " ".join(t["reason"] for t in part["todo"])
    assert "https://webapi.bps.go.id/developer/" in txt
    for t in part["todo"]:
        assert t["priority"] in (2, 3) and t["reason"] and t["chart"]


def test_merged_catalog_includes_id(main):
    assert "id-gdp" in {c["key"] for c in main["categories"]}
    assert any(r.get("part") == "id" for r in main["todo"])
