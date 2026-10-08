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
    "cn_nbs_hp70": {"kind", "metric", "index_url"},
    "cn_safe": {"file", "landing_page"},
    "cn_mof": {"metric", "field", "index_url"},
}
INTL = {"intl_bis", "intl_imf", "intl_oecd"}


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
    assert [c["key"] for c in cat["categories"]] == ["gdp", "monthly", "consumption", "investment", "prices", "trade", "bop", "housing", "fiscal", "industry", "finance", "credit", "new_productivity"]
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
        # 同一條原始序列可在水準圖與年增率圖各用一次（display 不同），所以 display／unit 不列入比對
        key = (s.get("fetcher"), json.dumps(s.get("params"), sort_keys=True), s["freq"], json.dumps(s.get("derived"), sort_keys=True))
        assert seen.setdefault(s["sid"], key) == key, s["sid"]


def test_fetchers_registered_and_params_complete(cat):
    for _, ch, s in all_series(cat):
        if s.get("derived"):
            assert "fetcher" not in s
            continue
        f = s["fetcher"]
        assert f in REGISTRY and (f.startswith("cn_") or f in INTL), (s["sid"], f)
        missing = PARAM_KEYS.get(f, set()) - set(s["params"])
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


# ---------- 第二次擴充（2026-10）----------
def chart_map(cat):
    return {ch["key"]: ch for c in cat["categories"] for ch in c["charts"]}


def test_new_categories_have_at_least_three_charts_and_names(cat):
    cats = {c["key"]: c for c in cat["categories"]}
    assert cats["bop"]["name_zh"] == "國際收支與外匯" and cats["fiscal"]["name_zh"] == "財政" and cats["credit"]["name_zh"] == "信貸與存款"
    for c in cat["categories"]:
        assert len(c["charts"]) >= 3, c["key"]


def test_sids_and_chart_keys_unique_across_all_catalogs(cat):
    import glob
    mine = {s["sid"] for _, _, s in all_series(cat)}
    assert all(s.startswith("cn.") for s in mine)
    keys = [ch["key"] for c in cat["categories"] for ch in c["charts"]]
    assert len(keys) == len(set(keys))
    for f in glob.glob(str(CATALOG.parent / "*.json")):
        if f == str(CATALOG):
            continue
        other = json.loads(Path(f).read_text(encoding="utf-8"))
        theirs = {s["sid"] for c in other.get("categories", []) for ch in c["charts"] for s in ch["series"]}
        assert not (mine & theirs), (f, sorted(mine & theirs)[:3])


def test_self_computed_series_are_labeled_as_not_official(cat):
    by = {s["sid"]: s for _, _, s in all_series(cat)}
    charts = chart_map(cat)
    for sid in ("cn.hp70_new_mom_up", "cn.hp70_new_mom_down", "cn.hp70_used_mom_up", "cn.hp70_used_mom_down"):
        assert "本站" in by[sid]["label_zh"] and "非官方" in by[sid]["source"] and by[sid]["self_calc"]
    assert "非國統局公布" in charts["hp70-breadth-mom"]["definition"]
    assert "本站" in by["cn.imts_x_asean6"]["label_zh"] and "非官方" in by["cn.imts_x_asean6"]["source"]
    assert "非官方統計" in charts["exports-asean-yoy"]["definition"] and "非官方統計" in charts["trade-balance-by-partner"]["definition"]
    for _, ch, s in all_series(cat):
        if s["sid"].startswith("cn.imts_bal_"):
            assert s["self_calc"] and "非官方" in s["source"] and "derived" in s


def test_derived_inputs_exist_and_hidden_helpers_are_flagged(cat):
    by = {s["sid"]: s for _, _, s in all_series(cat)}
    for sid in ("cn.imts_m_vnm", "cn.imts_m_ind"):
        assert by[sid].get("hidden") is True and by[sid]["fetcher"] == "intl_imf"


def test_mom_index_series_are_stored_as_pct_not_labeled_yearly(cat):
    for _, _, s in all_series(cat):
        if s["sid"].startswith(("cn.ppi_mom_", "cn.hp70_new_") ) and s["sid"].endswith(("_mom", "_total", "_means", "_consumer")) and "mom_up" not in s["sid"] and "mom_down" not in s["sid"]:
            assert s["display"] == "level" and s["unit"] == "%" and s["params"]["offset"] == -100, s["sid"]
            assert "月增率" in s["label_zh"] and "年增率" not in s["label_zh"]


def test_history_notes_for_known_breaks(cat):
    by = {s["sid"]: s for _, _, s in all_series(cat)}
    assert "G998" in by["cn.imts_x_g998"]["history_note"] and "成員隨年份調整" in by["cn.imts_m_g998"]["history_note"]
    cpi = [s for _, ch, s in all_series(cat) if ch["key"] in ("cpi-goods-services", "cpi-clothing-education-health")]
    assert len(cpi) == 7 and all((s["params"].get("parts") and "基期改版" in s["history_note"]) for s in cpi)
    mof = [s for _, _, s in all_series(cat) if s.get("fetcher") == "cn_mof"]
    assert len(mof) == 13 and all("2022 年部分月份官方稿件格式不同，未收" in s["history_note"] for s in mof)
    hp = [s for _, _, s in all_series(cat) if s.get("fetcher") == "cn_nbs_hp70"]
    assert len(hp) == 16 and all("2021 年 10 月" in s["history_note"] for s in hp)


def test_slow_quarterly_and_monthly_sources_have_stale_thresholds(cat):
    for _, _, s in all_series(cat):
        if s.get("fetcher") == "cn_safe" and s["freq"] == "Q":
            assert s["stale_days"] >= 280 and s["stale_reason"], s["sid"]
        if s.get("fetcher") in ("cn_mof", "cn_nbs_hp70"):
            assert s["stale_days"] >= 80 and s["stale_reason"], s["sid"]


def test_new_fetcher_params_name_their_landing_page_or_index(cat):
    for _, _, s in all_series(cat):
        p = s.get("params") or {}
        if s.get("fetcher") == "cn_safe":
            assert p["landing_page"].startswith("https://www.safe.gov.cn/safe/") and p["file"] in ("bop", "jsh", "skk", "debt", "trade"), s["sid"]
        if s.get("fetcher") == "cn_mof":
            assert p["index_url"].startswith("https://gks.mof.gov.cn/") and p["field"] in ("yoy_pct", "ytd_amount")
            assert s["display"] == "yoy" and s["yoy_from"] == "pct"        # 累計年增率直接用官方公布值，不自行推算
        if s.get("fetcher") == "cn_nbs_hp70":
            assert p["kind"] in ("new", "used") and p["metric"] in ("mom", "yoy") and ("city" in p) != ("stat" in p)


def test_priority3_charts_are_in_todo_with_reason(cat):
    todo = {t["chart"]: t for t in cat["todo"]}
    assert "mof-land-transfer-level" in todo and "累計轉單月" in todo["mof-land-transfer-level"]["reason"]
    assert "hp70-mean-yoy" in todo and "非官方" in todo["hp70-mean-yoy"]["reason"]
    assert not (set(todo) & set(chart_map(cat)))           # 收進來的不再留在 todo
    assert len(cat["todo"]) >= 50


def test_every_nbs_indicator_has_an_id_hint(cat):
    """cn_nbs 靠 id 提示省掉每個 cid 一次「指標清單」請求（平台限速，否則每天抓取超過 4 分鐘）。新增序列後要重產 cn_nbs_ids.py。"""
    from macro_db.sources.cn_nbs_ids import ID_HINTS
    missing = []
    for _, _, s in all_series(cat):
        if s.get("fetcher") == "cn_nbs":
            for part in (s["params"].get("parts") or [s["params"]]):
                if (part["cid"], part["name"]) not in ID_HINTS:
                    missing.append((s["sid"], part["name"]))
    assert not missing, missing[:5]
