"""馬來西亞分檔 an_my.json 結構檢查：離線。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from macro_db import catalog_io
from macro_db.sources import REGISTRY

DIR = Path(__file__).resolve().parents[2] / "macro_db" / "catalog"
KEYS = ["my-gdp", "my-price", "my-labor", "my-trade", "my-industry", "my-finance", "my-external", "my-estate"]


@pytest.fixture(scope="module")
def my():
    return json.loads((DIR / "an_my.json").read_text(encoding="utf-8"))


def series(my):
    for c in my["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                yield c, ch, s


def test_structure(my):
    assert my["region"] == "an" and my["part"] == "my" and my["group"] == "馬來西亞"
    assert [c["key"] for c in my["categories"]] == KEYS
    assert 6 <= len(my["categories"]) <= 8
    for c in my["categories"]:
        assert len(c["charts"]) >= 3, c["key"]
        for ch in c["charts"]:
            assert ch["title_zh"].startswith("馬來西亞"), ch["title_zh"]
            assert ch["series"]


def test_series_rules(my):
    sids = set()
    for _, ch, s in series(my):
        assert s["fetcher"] in REGISTRY
        assert s["sid"].startswith(("my.", "an.")), s["sid"]
        assert s["params"]["probe_url"].startswith("http"), s["sid"]
        sids.add(s["sid"])
        if s["display"] == "yoy":
            assert "年增率" not in s["label_zh"], s["sid"]
        if s["fetcher"] == "an_my_bnm":
            assert s["params"]["layout"] in ("ym", "yq", "daily") and s["params"]["table"]
    assert "intl_imf" not in {s["fetcher"] for _, _, s in series(my) if "S13BOND" in json.dumps(s["params"])}
    assert not any("MFS_MA" in json.dumps(s["params"]) for _, _, s in series(my))


def test_shared_an_sids_match_an_json(my):
    an = json.loads((DIR / "an.json").read_text(encoding="utf-8"))
    ref = {s["sid"]: s for c in an["categories"] for ch in c["charts"] for s in ch["series"]}
    used = [s for _, _, s in series(my) if s["sid"] in ref]
    assert {s["sid"] for s in used} >= {"an.my_gdp_real", "an.cbpol_my", "an.reserves_my", "an.my_exports",
                                         "an.spp_my", "an.xru_my", "an.tw_exp_us_my"}
    for s in used:
        assert {k: v for k, v in s.items() if k not in ("axis", "display")} == \
            {k: v for k, v in ref[s["sid"]].items() if k not in ("axis", "display")}, s["sid"]


def test_special_cases(my):
    by = {s["sid"]: s for _, _, s in series(my)}
    assert by["my.wage_median"]["params"].get("to_quarterly") and by["my.wage_median"]["freq"] == "Q"
    assert "history_note" in by["my.loan_total"]
    assert {"my.mgs_1y", "my.mgs_3y", "my.mgs_5y", "my.mgs_10y"} <= set(by)
    assert by["my.m3"]["params"]["id"] == "monetary_aggregates"


def test_merged(my):
    cat = catalog_io.load_catalog("an")
    mine = [c for c in cat["categories"] if c.get("part") == "my"]
    assert [c["key"] for c in mine] == KEYS
    assert all(r["reason"] for r in my["unavailable"]) and all(r["reason"] and r["priority"] in (2, 3) for r in my["todo"])
