"""台灣目錄（catalog/tw.json）完整性檢查：離線。"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from macro_db.sources import REGISTRY
from macro_db.sources import tw_common as C

CATALOG = Path(__file__).resolve().parents[2] / "macro_db" / "catalog" / "tw.json"
REQUIRED = ["sid", "label_zh", "source", "freq", "unit", "sa", "license", "display", "axis", "fetcher", "params"]
# 每個 fetcher 的 params 至少要有的鍵
PARAM_KEYS = {
    "tw_dgbas": {"long": {"file", "item", "url"}, "wide": {"file", "col", "url"}},
    "tw_cbc": {"cpx": {"file", "col"}, "fsi_csv": {"url", "col"}},
    "tw_ndc": {"zip": {"member", "col", "url"}, "csv": {"col", "url"}},
    "tw_mof": {"njswww": {"url", "col"}, "u2010": {"url", "col"}},
    "tw_moea": {None: {"file", "value"}},
    "tw_energy": {None: {"set_id", "col"}},
    "tw_moi": {"statis": {"url", "label", "col"}, "hpi_pdf": {"url", "col"}},
    "tw_jcic": {None: {"url", "group", "value"}},
    "tw_twse": {"fmtqik": {"col"}, "bfi82u": {"row", "col"}, "margn": {"row", "col"}},
    "tw_tpex": {"inx": {"col"}, "trading": {"col"}, "insti": {"row", "col"}, "margin": {"row", "col"}},
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
    assert cat["country"] == "tw"
    assert len(cat["categories"]) == 9
    for rec in cat["todo"]:
        assert rec["reason"] and rec["chart"]
    for rec in cat["unavailable"]:
        assert rec["reason"]


def test_every_series_has_required_fields(cat):
    for _, ch, s in all_series(cat):
        for k in REQUIRED:
            assert k in s, (s.get("sid"), k)
        assert s["sid"].startswith("tw.")
        assert s["freq"] in {"D", "W", "M", "Q", "A"}
        assert s["sa"] in {"SA", "NSA", "SAAR", "n/a"}
        assert s["license"] == "public" or s["license"].startswith("copyright:")
        assert s["axis"] in {"L", "R"}


def test_same_sid_means_same_source(cat):
    seen = {}
    for _, ch, s in all_series(cat):
        key = (s["fetcher"], json.dumps(s["params"], sort_keys=True), s["freq"], s["unit"])
        assert seen.setdefault(s["sid"], key) == key, s["sid"]


def test_fetchers_registered_and_params_complete(cat):
    for _, ch, s in all_series(cat):
        f = s["fetcher"]
        assert f.startswith("tw_") and f in REGISTRY, f
        schema = PARAM_KEYS[f]
        kind = s["params"].get("kind")
        key = kind if kind in schema else None
        assert key in schema or kind in schema, (s["sid"], kind)
        need = schema[kind] if kind in schema else schema[None]
        missing = need - set(s["params"])
        assert not missing, (s["sid"], missing)


def test_registered_modules_expose_fetch():
    for name, path in REGISTRY.items():
        if name.startswith("tw_"):
            assert callable(importlib.import_module(path).fetch)


def test_denominators_exist(cat):
    sids = {s["sid"] for _, _, s in all_series(cat)}
    for _, _, s in all_series(cat):
        if s["display"] == "ratio":
            assert s["denominator"] in sids and s["unit_out"]


def test_daily_series_say_history_starts_late(cat):
    for _, _, s in all_series(cat):
        if s["freq"] == "D" and s["fetcher"] in ("tw_twse", "tw_tpex"):
            assert s.get("history_note"), s["sid"]


def test_priority_rule_no_priority3_charts(cat):
    for c in cat["categories"]:
        for ch in c["charts"]:
            assert ch["priority"] in (1, 2)
    assert all(rec["priority"] in (2, 3) for rec in cat["todo"])


def test_moved_to_unavailable_not_collected(cat):
    sids = {s["sid"] for _, _, s in all_series(cat)}
    assert "tw.sinyi_hpi_tw" not in sids and "tw.cathay_index_tw" not in sids
    assert any(u.get("chart") == "sinyi-hpi" for u in cat["unavailable"])


def test_copyright_series_labelled(cat):
    pmi = next(s for _, _, s in all_series(cat) if s["sid"] == "tw.pmi")
    assert pmi["source"] == "中華經濟研究院（國發會發布）" and pmi["license"].startswith("copyright:")


# ---------- 憑證鏈不完整的主機：驗證失敗改不驗證（只對該主機） ----------

def test_requests_always_verify_with_bundled_intermediate(monkeypatch):
    """不准關掉憑證驗證：每次請求都帶 certifi＋repo 內附中繼憑證的 bundle 路徑。"""
    seen = []

    class R:
        status_code = 200
        content = b"ok"

    def fake(method, url, **kw):
        seen.append(kw["verify"])
        return R()

    monkeypatch.setattr(C.requests, "request", fake)
    assert C.http_get("https://ws.example.gov.tw/a.xml") == b"ok"
    bundle = seen[0]
    assert isinstance(bundle, str) and bundle.endswith(".pem")
    text = open(bundle).read()
    assert "BEGIN CERTIFICATE" in text
    pem = (C._EXTRA_CA_DIR / "twca_secure_ssl_ca_2023g3.pem").read_text().strip()
    assert pem in text
