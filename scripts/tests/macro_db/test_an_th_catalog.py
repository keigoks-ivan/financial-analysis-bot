"""泰國分檔目錄（catalog/an_th.json）結構檢查：離線。"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from macro_db.sources import REGISTRY

CAT_DIR = Path(__file__).resolve().parents[2] / "macro_db" / "catalog"
REQUIRED = ["sid", "label_zh", "source", "freq", "unit", "sa", "license", "display", "axis", "fetcher", "params"]
PARAM_KEYS = {
    "an_th_bot": {"report_id", "row_no", "row_label"},
    "an_th_tpso": {"api"},
    "an_th_oie": {"file", "row_label"},
    "intl_imf": {"dataflow", "key"},
    "intl_bis": {"dataflow", "key"},
}
# 沿用 an.json（五國對照）的泰國序列：spec 必須一字不差
SHARED = ["an.cbpol_th", "an.xru_th", "an.spp_th"]


@pytest.fixture(scope="module")
def cat():
    return json.loads((CAT_DIR / "an_th.json").read_text(encoding="utf-8"))


def all_series(cat):
    for c in cat["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                yield c, ch, s


def test_top_level(cat):
    assert cat["region"] == "an" and cat["part"] == "th" and cat["group"] == "泰國"
    keys = [c["key"] for c in cat["categories"]]
    assert keys[0] == "th-gdp"                       # 舊網址 an/th.html 轉到這裡
    assert 6 <= len(keys) <= 8 and len(set(keys)) == len(keys)
    for c in cat["categories"]:
        assert c["key"].startswith("th-") and len(c["charts"]) >= 3, c["key"]
    for rec in cat["todo"]:
        assert rec["reason"] and rec["chart"] and rec["priority"] in (2, 3)
    for rec in cat["unavailable"]:
        assert rec["reason"] and rec["mm_ref"]


def test_series_fields_probe_and_titles(cat):
    sids = set()
    for _, ch, s in all_series(cat):
        for k in REQUIRED:
            assert k in s, (s.get("sid"), k)
        assert ch["title_zh"].startswith("泰國"), ch["title_zh"]
        assert s["sid"].startswith("th.") or s["sid"] in SHARED, s["sid"]
        assert s["freq"] in {"D", "W", "M", "Q", "A"} and s["sa"] in {"SA", "NSA", "SAAR", "n/a"}
        assert s["license"] == "public" and s["axis"] in {"L", "R"}
        assert s["params"]["probe_url"].startswith("http"), s["sid"]
        if s["display"] == "yoy":
            assert "年增率" not in s["label_zh"], s["sid"]       # render 會自己加「年增率」
        if s.get("stale_days"):
            assert s.get("stale_reason"), s["sid"]
        sids.add((s["sid"], s["display"]))
    n = sum(1 for _ in all_series(cat))
    assert n == len(sids)                                           # 全檔 (sid, 顯示方式) 唯一；同圖可以水準值與年增率各用一次


def test_fetchers_registered_and_params_complete(cat):
    for _, _, s in all_series(cat):
        f = s["fetcher"]
        assert f in REGISTRY and (f.startswith("an_th_") or f.startswith("intl_")), f
        assert PARAM_KEYS[f] <= set(s["params"]), s["sid"]
        assert callable(importlib.import_module(REGISTRY[f]).fetch)
        if f == "an_th_tpso" and s["params"]["api"] != "cci":
            assert {"type", "code", "year_base"} <= set(s["params"]), s["sid"]
        if f == "an_th_tpso" and s["params"]["api"] == "cci":
            assert s["params"]["name"], s["sid"]


def test_shared_sids_match_an_json_exactly(cat):
    main = json.loads((CAT_DIR / "an.json").read_text(encoding="utf-8"))
    base = {s["sid"]: s for c in main["categories"] for ch in c["charts"] for s in ch["series"]}
    mine = {s["sid"]: s for _, _, s in all_series(cat)}
    for sid in SHARED:
        assert sid in mine and sid in base, sid
        assert mine[sid] == base[sid], sid


def test_key_cases(cat):
    mine = {s["sid"]: s for _, _, s in all_series(cat)}
    # 固定投資主線用未季調年增率（官方口徑）；季調版只當對照
    assert mine["th.gdp_gfcf"]["sa"] == "NSA" and ".NSA." in mine["th.gdp_gfcf"]["params"]["key"]
    assert mine["th.gdp_gfcf_sa"]["sa"] == "SA" and "對照" in mine["th.gdp_gfcf_sa"]["label_zh"]
    # MPI 只有 2021 年起
    assert "2021" in mine["th.mpi_sa"]["history_note"]
    # 零售總指數要附上與分項方向不同的原因
    assert "其他零售" in mine["th.retail_total"]["history_note"]
    # 國家頁的出口、進口、外匯存底、CPI 用 BOT／TPSO 版本
    assert mine["th.exp_total"]["fetcher"] == "an_th_bot" and mine["th.res_gross"]["fetcher"] == "an_th_bot"
    assert mine["th.cpi_headline"]["fetcher"] == "an_th_tpso"
    for gone in ("an.th_exports", "an.th_imports", "an.reserves_th", "an.cpi_yoy_th"):
        assert gone not in mine


def test_bot_api_key_charts_in_todo(cat):
    keyed = [t for t in cat["todo"] if "portal.api.bot.or.th" in t["reason"]]
    assert len(keyed) == 15 and all("免費" in t["reason"] for t in keyed)
