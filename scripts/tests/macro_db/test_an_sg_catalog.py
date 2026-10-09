"""新加坡分檔（catalog/an_sg.json）結構檢查：離線。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from macro_db import catalog_io

CAT_DIR = Path(__file__).resolve().parents[2] / "macro_db" / "catalog"


@pytest.fixture(scope="module")
def sg():
    return json.loads((CAT_DIR / "an_sg.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def full():
    return catalog_io.load_catalog("an")


def series(sg):
    for c in sg["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                yield c, ch, s


def test_structure(sg):
    assert sg["part"] == "sg" and sg["group"] == "新加坡"
    keys = [c["key"] for c in sg["categories"]]
    assert keys[0] == "sg-gdp" and 6 <= len(keys) <= 8
    for c in sg["categories"]:
        assert c["key"].startswith("sg-") and len(c["charts"]) >= 3, c["key"]
        for ch in c["charts"]:
            assert ch["title_zh"].startswith("新加坡"), ch["title_zh"]
            assert "新加坡新加坡" not in ch["title_zh"]


def test_sids_unique_and_prefixed(sg):
    sids = [s["sid"] for _, _, s in series(sg)]
    keys = [(s["sid"], s["display"]) for _, _, s in series(sg)]   # 同一 sid 可用不同 display 畫兩次
    assert len(keys) == len(set(keys))
    assert all(x.startswith(("sg.", "an.")) for x in sids)


def test_duplicate_name_tables_use_series_no(sg):
    for _, _, s in series(sg):
        if s["params"].get("table_id") in ("M250141", "M400001"):
            assert s["params"].get("series_no"), s["sid"]


def test_unemployment_labels_say_adjustment(sg):
    by = {s["sid"]: s for _, _, s in series(sg)}
    assert "未季調" in by["an.sg_unemp"]["label_zh"] and by["an.sg_unemp"]["sa"] == "NSA"
    assert by["sg.unemp_total_sa"]["sa"] == "SA" and "季調" in by["sg.unemp_total_sa"]["label_zh"]
    assert "含外籍家庭幫傭" in by["sg.emp_change_total"]["label_zh"]


def test_money_supply_history_note(sg):
    by = {s["sid"]: s for _, _, s in series(sg)}
    assert "2021-07" in by["an.sg_m2"]["history_note"]


def test_core_cpi_not_using_bad_row(sg):
    for _, _, s in series(sg):
        assert "Percent Change Over Corresponding" not in s["params"].get("row", "")


def test_shared_with_an_json_identical(full):
    seen = {}
    for c in full["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                if s["sid"] in ("an.sg_gdp_real", "an.sg_exports", "an.xru_sg"):
                    seen.setdefault(s["sid"], []).append({k: v for k, v in s.items() if k not in ("axis", "label_zh", "display")})
    assert set(seen) == {"an.sg_gdp_real", "an.sg_exports", "an.xru_sg"}
    for v in seen.values():
        assert all(x == v[0] for x in v)


def test_todo_mentions_mas_key(sg):
    txt = " ".join(t["reason"] for t in sg["todo"])
    assert "MAS API 金鑰" in txt and "developer.tech.gov.sg" in txt
