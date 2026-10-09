"""越南分檔（catalog/an_vn.json）結構檢查：離線。"""
from __future__ import annotations

import json
from pathlib import Path

CAT = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "an_vn.json"
AN = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "an.json"


def load():
    return json.loads(CAT.read_text(encoding="utf-8"))


def series():
    for c in load()["categories"]:
        for ch in c["charts"]:
            for s in ch["series"]:
                yield c, ch, s


def test_top_level():
    d = load()
    assert d["region"] == "an" and d["part"] == "vn" and d["group"] == "越南"
    assert d["categories"][0]["key"] == "vn-gdp"
    for c in d["categories"]:
        assert c["key"].startswith("vn-")
        assert len(c["charts"]) >= 3, c["key"]
    for t in d["todo"]:
        assert t["reason"] and t["priority"] in (2, 3)
    assert all(u["reason"] for u in d["unavailable"])


def test_titles_start_with_country():
    for c in load()["categories"]:
        for ch in c["charts"]:
            assert ch["title_zh"].startswith("越南"), ch["title_zh"]


def test_sids_and_no_derived():
    for _, _, s in series():
        assert s["sid"].startswith("vn.") or s["sid"].startswith("an."), s["sid"]
        assert "derived" not in s


def test_yoy_label_has_no_suffix():
    for _, _, s in series():
        if s["display"] == "yoy":
            assert "年增率" not in s["label_zh"], s["sid"]


def test_reused_an_sids_match_an_json():
    an = json.loads(AN.read_text(encoding="utf-8"))
    ref = {s["sid"]: s for c in an["categories"] for ch in c["charts"] for s in ch["series"]}
    for _, _, s in series():
        if s["sid"] in ref:
            a = {k: v for k, v in ref[s["sid"]].items() if k not in ("axis", "display")}
            b = {k: v for k, v in s.items() if k not in ("axis", "display")}
            assert a == b, s["sid"]


def test_nso_params():
    from macro_db.sources import an_vn_nso as N
    for _, _, s in series():
        if s["fetcher"] != "an_vn_nso":
            continue
        p = s["params"]
        if p.get("kind", "report") == "report":
            assert p["table"] in N.TABLES and p["row"], s["sid"]
        else:
            assert p["kind"] == "customs" and p["row"], s["sid"]
