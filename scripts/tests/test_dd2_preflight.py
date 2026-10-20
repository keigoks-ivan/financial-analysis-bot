#!/usr/bin/env python3
"""測試 DD 管線 WP2（2026-10-20）：開跑預檢、證據驗證矛盾、散文自動修一次。

(a) 前份 DD 查找（dd_prior）：以 dd-meta ticker 為準（DD_2317_／DD_3037.TW_／DD_2308TW_／BRIEF_ 都認得）；
    帶點代號（2317.TW、6857.T）傳進 build_ledger／build_canonical_id，不再被去點
(b) 純數字代號補尾碼：前份 DD → security_meta → 判不了才停
(c) 對手清單：id_meta 要貼題才採用；找不到時不自動採用 dd-screener，只列候選供參考
(c') peer_financials 的 .SH 在送進 yfinance 時換成 .SS
(d) status=none 且只查 1 條：warn 加 (info)、stage0 補派一次
(e) 散文自動修一次：「未覆蓋數字」擋下時也走 prose_fix

全部用 tmp_path 自建 fixture，不碰 docs/、不呼叫 LLM、不上網。Python 3.9 相容。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))

import dd_numbers_extra  # noqa: E402
import dd_prior  # noqa: E402
import ddreport  # noqa: E402
import validate_evidence  # noqa: E402
from dd2 import run as dd2_run  # noqa: E402


def _dd_html(ticker, extra=None):
    meta = {"ticker": ticker, "schema": "v19", "dca_verdict": "進場", "dca_role": "核心", "price_at_dd": 10}
    meta.update(extra or {})
    return '<html><body><script id="dd-meta" type="application/json">{0}</script></body></html>'.format(
        json.dumps(meta, ensure_ascii=False))


@pytest.fixture
def dd_dir(tmp_path, monkeypatch):
    d = tmp_path / "docs" / "dd"
    (d / "brief").mkdir(parents=True)
    monkeypatch.setattr(ddreport, "DD_DIR", d)
    monkeypatch.setattr(ddreport, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(dd_prior, "DD_DIR", d)
    monkeypatch.setattr(dd_prior, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(ddreport, "DD_SCREENER_LATEST_PATH", tmp_path / "docs" / "dd-screener" / "latest.json")
    return d


# ---------------------------------------------------------------------------
# (a) 前份 DD 查找
# ---------------------------------------------------------------------------

def test_ticker_key_normalizes_dots_and_tw_two():
    assert dd_prior.ticker_key("3037.TW") == dd_prior.ticker_key("3037TW") == "3037TW"
    assert dd_prior.ticker_key("6187.TWO") == "6187TW"
    assert dd_prior.ticker_key("6139.KL") == "6139KL"
    assert dd_prior.ticker_key("brk.b") == "BRKB"


def test_find_dd_files_filename_variants_and_meta_wins(dd_dir):
    (dd_dir / "DD_2317_20260601.html").write_text(_dd_html("2317.TW"), encoding="utf-8")        # 檔名無尾碼
    (dd_dir / "DD_2317TW_20260414.html").write_text(_dd_html("2317.TW"), encoding="utf-8")      # 檔名去點
    (dd_dir / "DD_2317.TW_20261019.html").write_text(_dd_html("2317.TW"), encoding="utf-8")     # 檔名帶點
    (dd_dir / "brief" / "BRIEF_2317.TW_20260905.html").write_text(_dd_html("2317.TW"), encoding="utf-8")
    (dd_dir / "DD_2317_20250101.html").write_text(_dd_html("2317.KL"), encoding="utf-8")        # 檔名相同代號、檔內是別家
    (dd_dir / "DD_23170_20260101.html").write_text(_dd_html("23170.TW"), encoding="utf-8")      # 前綴相同的別檔
    got = dd_prior.find_dd_files("2317.TW")
    assert [d for d, _ in got] == ["20260414", "20260601", "20260905", "20261019"]
    assert [d for d, _ in dd_prior.find_dd_files("2317.TWO")] == [d for d, _ in got]   # TW／TWO 視為同家


def test_find_dd_files_no_meta_falls_back_to_filename_and_us_unchanged(dd_dir):
    (dd_dir / "DD_NVDA_20260411.html").write_text("<html>legacy 沒有 dd-meta</html>", encoding="utf-8")
    (dd_dir / "DD_NVDA_20260511.html").write_text(_dd_html("NVDA"), encoding="utf-8")
    assert [d for d, _ in dd_prior.find_dd_files("NVDA")] == ["20260411", "20260511"]
    assert dd_prior.find_dd_files("NVDAX") == []
    (dd_dir / "DD_BRK.B_20260101.html").write_text(_dd_html("BRK.B"), encoding="utf-8")
    assert [d for d, _ in dd_prior.find_dd_files("BRK.B")] == ["20260101"]


def test_build_prior_dd_finds_dotted_filename_with_dated_before(dd_dir):
    (dd_dir / "DD_3037.TW_20260601.html").write_text(_dd_html("3037.TW", {"archetype": "循環/商品"}), encoding="utf-8")
    (dd_dir / "DD_3037.TW_20261020.html").write_text(_dd_html("3037.TW"), encoding="utf-8")   # 同日，不算前份
    prior = dd_prior.build_prior_dd("3037.TW", "20261020")
    assert prior["status"] == "ok" and prior["date"] == "20260601"
    assert prior["prior_meta"]["archetype"] == "循環/商品"


def test_dd_prior_main_passes_raw_dotted_ticker_to_all_builders(monkeypatch, tmp_path):
    seen = {}
    monkeypatch.setattr(dd_prior, "build_prior_dd", lambda t, d: seen.setdefault("prior", t) and {})
    monkeypatch.setattr(dd_prior, "build_ledger", lambda t: seen.setdefault("ledger", t) and {})
    monkeypatch.setattr(dd_prior, "build_canonical_id", lambda t: seen.setdefault("cid", t) and {})
    monkeypatch.setattr(dd_prior, "build_transcripts", lambda t: {})
    monkeypatch.setattr(sys, "argv", ["dd_prior.py", " 3711.tw ", "--out", str(tmp_path / "o.json")])
    dd_prior.main()
    assert seen == {"prior": "3711.TW", "ledger": "3711.TW", "cid": "3711.TW"}


def test_build_canonical_id_queries_with_dotted_ticker(monkeypatch):
    asked = []
    monkeypatch.setattr(dd_prior.dd_meta_reader, "find_ids_for_ticker", lambda d, t: asked.append(t) or [])
    assert dd_prior.build_canonical_id("3711.TW") == {"status": "gap"}
    assert asked == ["3711.TW"]


def test_build_ledger_matches_dotted_entity_alias_and_passes_raw_to_q(tmp_path, monkeypatch):
    kd = tmp_path / "knowledge"
    kd.mkdir()
    (kd / "graph.json").write_text(json.dumps({
        "aliases": {"2330.TW": "TSM"}, "nodes": [{"id": "TSM", "canonical": "進場"}]}), encoding="utf-8")
    (kd / "decisions.jsonl").write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in [
        {"kind": "decision", "id": "d1", "entity": "TSM", "date": "2026-03-01", "verdict": "進場"},
        {"kind": "decision", "id": "d2", "entity": "2330.TW", "date": "2026-07-01", "verdict": "進場"},
        {"kind": "decision", "id": "d3", "entity": "3017.TW", "date": "2026-07-01", "verdict": "觀望"},
    ]), encoding="utf-8")
    (kd / "falsifiers.json").write_text(json.dumps({"items": [{"ticker": "2330.TW", "metric": "m"}]}), encoding="utf-8")
    monkeypatch.setattr(dd_prior, "KNOWLEDGE_DIR", kd)
    calls = []

    class _P:
        stdout = ""

    monkeypatch.setattr(dd_prior, "_run_q", lambda args, timeout=120: calls.append(list(args)) or _P())
    out = dd_prior.build_ledger("2330.TW")
    assert [d["date"] for d in out["decision_history"]] == ["2026-03-01", "2026-07-01"]   # 別名 TSM 的決策也帶出
    assert [f["metric"] for f in out["falsifiers"]] == ["m"]
    assert calls == [["2330.TW"], ["--note", "2330.TW"]]
    # 去點寫法（舊 bug）查不到——保留這個斷言，防回退
    assert dd_prior.build_ledger("2330TW")["decision_history"] == []


# ---------------------------------------------------------------------------
# (b) 純數字代號補尾碼
# ---------------------------------------------------------------------------

def _write_security_meta(tmp_path, entries):
    p = tmp_path / "data" / "active_etf" / "security_meta.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")


def _write_screener(tmp_path, tickers):
    p = tmp_path / "docs" / "dd-screener" / "latest.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    stocks = [t if isinstance(t, dict) else {"ticker": t} for t in tickers]
    p.write_text(json.dumps({"stocks": stocks}), encoding="utf-8")


def test_infer_suffix_from_prior_dd_meta(dd_dir, tmp_path):
    (dd_dir / "DD_2317_20260601.html").write_text(_dd_html("2317.TW"), encoding="utf-8")
    (dd_dir / "DD_6857T_20260522.html").write_text(_dd_html("6857.T"), encoding="utf-8")
    assert ddreport._infer_exchange_suffix("2317")[0] == "2317.TW"
    assert ddreport._infer_exchange_suffix("6857")[0] == "6857.T"      # 前份 DD 說是日股就是日股


def test_infer_suffix_conflicting_prior_stops(dd_dir):
    (dd_dir / "DD_6146T_20260522.html").write_text(_dd_html("6146.T"), encoding="utf-8")
    (dd_dir / "DD_6146TW_20260522.html").write_text(_dd_html("6146.TW"), encoding="utf-8")
    full, why = ddreport._infer_exchange_suffix("6146")
    assert full is None and "多種尾碼" in why


def test_infer_suffix_from_security_meta(dd_dir, tmp_path):
    _write_security_meta(tmp_path, {
        "2303.TW": {"market": "TWSE", "name": "聯電"},
        "6187.TWO": {"market": "TPEx", "name": "萬潤"},
    })
    _write_screener(tmp_path, ["NVDA", "6857.T"])
    assert ddreport._infer_exchange_suffix("2303")[0] == "2303.TW"
    assert ddreport._infer_exchange_suffix("6187")[0] == "6187.TWO"
    full, why = ddreport._infer_exchange_suffix("9999")
    assert full is None and "查不到" in why


def test_infer_suffix_ambiguous_with_japan_in_pool_stops(dd_dir, tmp_path):
    _write_security_meta(tmp_path, {"6857.TW": {"market": "TWSE", "name": "某台股"}})
    _write_screener(tmp_path, ["6857.T"])
    full, why = ddreport._infer_exchange_suffix("6857")
    assert full is None and "6857.T" in why


def test_main_autocompletes_bare_tw_code(monkeypatch, capsys):
    monkeypatch.setattr(dd2_run.ddreport, "_infer_exchange_suffix", lambda c: ("2317.TW", "測試依據"))

    class _Stop(Exception):
        pass

    def _fake_ctx(ticker, date, args):
        raise _Stop(ticker)

    monkeypatch.setattr(dd2_run, "Ctx", _fake_ctx)
    with pytest.raises(_Stop) as ei:
        dd2_run.main(["2317", "--until", "plan", "--dry-run"])
    assert str(ei.value) == "2317.TW"
    assert "[auto] 2317 沒有交易所尾碼：依 測試依據，補成 2317.TW" in capsys.readouterr().out


def test_main_stops_when_suffix_unknown(monkeypatch, capsys):
    monkeypatch.setattr(dd2_run.ddreport, "_infer_exchange_suffix", lambda c: (None, "查不到"))
    assert dd2_run.main(["9999", "--until", "plan", "--dry-run"]) == 2
    assert "[stop] 9999 沒有交易所尾碼（查不到）" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# (c) 對手清單
# ---------------------------------------------------------------------------

@pytest.fixture
def peer_env(tmp_path, monkeypatch):
    """假的產業／市值資料：兩個 GICS 組（Staples／Comm）、台股電子兩個產業別、一檔非電子。"""
    uni = tmp_path / "universe.json"
    uni.write_text(json.dumps({"tickers": [
        {"ticker": "WMT", "sector": "Consumer Staples"}, {"ticker": "COST", "sector": "Consumer Staples"},
        {"ticker": "TGT", "sector": "Consumer Staples"}, {"ticker": "DG", "sector": "Consumer Staples"},
        {"ticker": "KO", "sector": "Consumer Staples"},
        {"ticker": "META", "sector": "Communication Services"}, {"ticker": "GOOGL", "sector": "Communication Services"},
        {"ticker": "AMZN", "sector": "Consumer Discretionary"},
    ]}), encoding="utf-8")
    sm = tmp_path / "security_meta.json"
    sm.write_text(json.dumps({
        "2303.TW": {"industry_code": "24", "industry_name": "半導體", "shares_outstanding": 100},
        "3711.TW": {"industry_code": "24", "industry_name": "半導體", "shares_outstanding": 200},
        "3443.TW": {"industry_code": "24", "industry_name": "半導體", "shares_outstanding": 50},
        "2330.TW": {"industry_code": "24", "industry_name": "半導體", "shares_outstanding": 5000},
        "3017.TW": {"industry_code": "28", "industry_name": "電子零組件", "shares_outstanding": 100},
        "2002.TW": {"industry_code": "10", "industry_name": "鋼鐵", "shares_outstanding": 100},
    }), encoding="utf-8")
    px = tmp_path / "prices-tw.json"
    px.write_text(json.dumps({"tickers": {k: {"price": v} for k, v in {
        "2303.TW": 10, "3711.TW": 6, "3443.TW": 20, "2330.TW": 100, "3017.TW": 11, "2002.TW": 10}.items()}}),
        encoding="utf-8")
    monkeypatch.setattr(ddreport, "PEER_UNIVERSE_PATH", uni)
    monkeypatch.setattr(ddreport, "SECURITY_META_PATH", sm)
    monkeypatch.setattr(ddreport, "PRICES_TW_PATH", px)
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", tmp_path / "no_archive")
    monkeypatch.setattr(ddreport, "DD_SCREENER_LATEST_PATH", tmp_path / "latest.json")
    monkeypatch.setattr(ddreport, "_yf_market_cap", lambda t: None)   # 不上網
    return tmp_path


def _fund(mcap):
    return {"fund": {"dil_shares_fy": mcap, "last_price_local": 1}}


def _fake_ids(monkeypatch, tmp_path, ids):
    """ids: {檔名: meta}；find_ids_for_ticker 依 related_tickers 比對。"""
    (tmp_path / "id").mkdir(exist_ok=True)
    monkeypatch.setattr(ddreport, "ID_DIR", tmp_path / "id")

    def fake_find(_d, ticker):
        return [(tmp_path / "id" / name, meta) for name, meta in sorted(ids.items())
                if any(r["ticker"].upper() == ticker.upper() for r in meta["related_tickers"])]

    monkeypatch.setattr(ddreport.dd_meta_reader, "find_ids_for_ticker", fake_find)


def _rt(*items):
    out = []
    for it in items:
        t, depth = it if isinstance(it, tuple) else (it, "🟡")
        out.append({"ticker": t, "depth": depth})
    return out


def test_id_meta_rejects_off_theme_id_and_takes_industry_match(peer_env, monkeypatch):
    _fake_ids(monkeypatch, peer_env, {
        "ID_AIAdRetailMedia_20260429.html": {   # WMT 在這份是 🔴 但排第 4，其餘多半是廣告／平台股 → 不貼題
            "publish_date": "2026-04-29", "related_tickers": _rt("META", "GOOGL", "AMZN", ("WMT", "🔴"), "TGT")},
        "ID_DiscountRetail_20260430.html": {    # 同產業成員 ≥2 → 採用，且只取同產業成員
            "publish_date": "2026-04-30", "related_tickers": _rt("TJX", "DG", "TGT", ("WMT", "🟡"), "COST", "NDLS")},
    })
    assert ddreport._peers_from_id_meta("WMT") == ["DG", "TGT", "COST"]


def test_id_meta_main_member_takes_first_four_and_beats_industry_match(peer_env, monkeypatch):
    _fake_ids(monkeypatch, peer_env, {
        "ID_Banks_20260428.html": {"publish_date": "2026-04-28", "related_tickers": _rt(
            ("JPM", "🔴"), "MS", "GS", "BAC", "WFC", "C")},
        "ID_Airline_20260429.html": {"publish_date": "2026-04-29", "related_tickers": _rt(
            "DAL", "UAL", "AAL", "LUV", "ALK", "JBLU", ("JPM", "🔴"))},   # 🔴 但排最後、無 purity → 非主要成員
    })
    assert ddreport._peers_from_id_meta("JPM") == ["MS", "GS", "BAC", "WFC"]


def test_id_meta_purity_threshold_makes_main_member(peer_env, monkeypatch):
    rts = _rt("A1", "A2", "A3")
    rts.append({"ticker": "ZCO", "depth": "🔴", "purity_pct": 40})
    _fake_ids(monkeypatch, peer_env, {"ID_X_20260101.html": {"publish_date": "2026-01-01", "related_tickers": rts}})
    assert ddreport._peers_from_id_meta("ZCO") == ["A1", "A2", "A3"]


def test_id_meta_old_version_superseded_by_newer_same_id(peer_env, monkeypatch):
    _fake_ids(monkeypatch, peer_env, {
        "ID_EDA_20260427.html": {"theme": "AI EDA + IP", "publish_date": "2026-04-27",
                                 "related_tickers": _rt(("SNPS", "🔴"), "CDNS", "ARM", "QCOM", "NVDA")},
        "ID_EDA_20261014.html": {"theme": "EDA", "publish_date": "2026-10-14",   # 改版後主題字串不同，仍是同一份
                                 "related_tickers": _rt(("SNPS", "🔴"), "CDNS", "ARM", "688521.SH")},
    })
    assert ddreport._peers_from_id_meta("SNPS") == ["CDNS", "ARM", "688521.SH"]


def test_id_meta_returns_none_when_nothing_fits(peer_env, monkeypatch):
    _fake_ids(monkeypatch, peer_env, {
        "ID_Ads_20260429.html": {"publish_date": "2026-04-29", "related_tickers": _rt("META", "GOOGL", ("WMT", "🔴"))}})
    assert ddreport._peers_from_id_meta("WMT") is None


def _screener(tmp_path, rows):
    (tmp_path / "latest.json").write_text(json.dumps({"stocks": rows}), encoding="utf-8")


def test_screener_candidates_same_industry_nearest_market_cap(peer_env):
    _screener(peer_env, [
        dict(ticker="WMT", **_fund(950)), dict(ticker="COST", **_fund(440)), dict(ticker="KO", **_fund(400)),
        dict(ticker="TGT", **_fund(60)), dict(ticker="DG", **_fund(20)),
        dict(ticker="META", **_fund(900)),   # 市值最近但不同產業
    ])
    got, note = ddreport._peers_from_screener("WMT")
    assert got == ["COST", "KO", "TGT", "DG"]
    assert "僅供參考" in note and "--peers" in note and "COST" in note


def test_screener_candidates_prefer_same_official_industry_within_electronics(peer_env):
    _screener(peer_env, [
        dict(ticker="2303.TW"), dict(ticker="3711.TW"), dict(ticker="3443.TW"), dict(ticker="3017.TW"),
        dict(ticker="2330.TW"), dict(ticker="2002.TW"),
    ])
    # 2303 市值 1000；3711=1200、3443=1000、2330=500000（差 500 倍）、3017=1100（電子但非半導體）、2002 非電子
    got, _ = ddreport._peers_from_screener("2303.TW")
    assert got[:3] == ["3443.TW", "3711.TW", "3017.TW"]    # 半導體且市值在 10 倍內的先，再補市值接近的電子股
    assert "2002.TW" not in got


def test_screener_candidates_target_market_cap_from_yfinance(peer_env, monkeypatch):
    _screener(peer_env, [dict(ticker="WMT"), dict(ticker="COST", **_fund(440)), dict(ticker="KO", **_fund(400))])
    calls = []
    monkeypatch.setattr(ddreport, "_yf_market_cap", lambda t: calls.append(t) or 430)
    assert ddreport._peers_from_screener("WMT")[0] == ["COST", "KO"]   # 標的 430：|ln(440/430)| < |ln(400/430)| → COST 先
    assert calls == ["WMT"]


def test_screener_candidates_need_two(peer_env):
    _screener(peer_env, [dict(ticker="WMT", **_fund(950)), dict(ticker="COST", **_fund(440))])
    assert ddreport._peers_from_screener("WMT") == (None, None)
    assert ddreport._peers_from_screener("UNKNOWN") == (None, None)   # 判不出產業


def test_resolve_peers_never_adopts_screener_candidates(peer_env, monkeypatch):
    """id_meta／archive 都沒有時回 (None, None) 讓 plan 停下；dd-screener 候選只進錯誤訊息，不自動採用。"""
    _fake_ids(monkeypatch, peer_env, {})
    _screener(peer_env, [dict(ticker="WMT", **_fund(950)), dict(ticker="COST", **_fund(440)),
                         dict(ticker="KO", **_fund(400)), dict(ticker="TGT", **_fund(60))])
    assert ddreport._peers_from_screener("WMT")[0]                      # 候選有，
    assert ddreport._resolve_peers(None, "WMT") == (None, None)        # 但不採用
    assert ddreport._resolve_peers("A,B", "WMT") == ("A,B", "cli")
    assert ddreport._resolve_peers(None, "UNKNOWN") == (None, None)


# ---------------------------------------------------------------------------
# (c') peer_financials 的 .SH → .SS（只在送進 yfinance 的呼叫點）
# ---------------------------------------------------------------------------

def test_yf_symbol_maps_sh_to_ss_only():
    assert dd_numbers_extra._yf_symbol("688521.SH") == "688521.SS"
    assert dd_numbers_extra._yf_symbol("688521.sh") == "688521.SS"
    for t in ("301269.SZ", "6857.T", "2317.TW", "SNPS", "688521.SS"):
        assert dd_numbers_extra._yf_symbol(t) == t


def test_ttm_financials_sends_ss_to_yfinance_but_keeps_key(monkeypatch):
    asked = []

    class _YF:
        @staticmethod
        def Ticker(sym):
            asked.append(sym)

            class _T:
                quarterly_income_stmt = None   # 沒資料也無妨：只驗送進 yfinance 的代號
                quarterly_cashflow = None
            return _T()

    monkeypatch.setattr(dd_numbers_extra, "_lazy_imports", lambda: (None, None, _YF))
    out = dd_numbers_extra.compute_peer_financials("SNPS", ["688521.SH"])
    assert asked == ["SNPS", "688521.SS"]
    assert list(out) == ["SNPS", "688521.SH"]          # 報告上的鍵維持原代號


# ---------------------------------------------------------------------------
# (d) 證據驗證矛盾
# ---------------------------------------------------------------------------

def test_none_with_one_query_warn_is_info_and_not_escalated_by_strict():
    fails, warns = validate_evidence.check_axis(
        "competitive_share_entrants", {"status": "none", "queries_run": ["only one"], "findings": []}, {})
    assert not fails
    assert warns and all(w.startswith("(info)") for w in warns)
    # --strict 只升級不以 (info) 開頭的 warn
    assert [w for w in warns if not w.startswith("(info)")] == []


class _Ctx(object):
    """do_stage0 補派／prose_fix 測試用的最小 ctx。"""

    def __init__(self, run_dir):
        self.run_dir = run_dir
        self.manifest = {}
        self.saved = 0

    def save(self):
        self.saved += 1


def _write_part(path, axis, status, queries, findings=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"coverage": {axis: {
        "status": status, "queries_run": queries, "findings": findings or []}}}, ensure_ascii=False), encoding="utf-8")


def _thin_env(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    (run_dir / "prompts").mkdir(parents=True)
    specs = []
    for k, axis in enumerate(["thin_axis", "ok_axis", "gap_axis", "found_axis"], start=1):
        (run_dir / "prompts" / "a_{0}_{1}.md".format(k, axis)).write_text("原提示 " + axis, encoding="utf-8")
        specs.append({"id": "a_{0}_{1}".format(k, axis), "axis_id": axis, "model": "sonnet",
                      "prompt": "prompts/a_{0}_{1}.md".format(k, axis), "out": "parts/axes_{0}.json".format(k)})
    _write_part(run_dir / "parts/axes_1.json", "thin_axis", "none", ["q1"])
    _write_part(run_dir / "parts/axes_2.json", "ok_axis", "none", ["q1", "q2"])
    _write_part(run_dir / "parts/axes_3.json", "gap_axis", "none", ["(agent incomplete)"])
    _write_part(run_dir / "parts/axes_4.json", "found_axis", "found", ["q1"], [{"claim": "x"}])
    # 驗證器替身：status=none 且沒有任何查詢才不合格
    def fake_sub(cmd, cwd=None):
        d = json.loads(Path(cmd[-1]).read_text(encoding="utf-8"))
        bad = any(c.get("status") == "none" and not c.get("queries_run") for c in d["coverage"].values())
        return (1 if bad else 0), ""
    monkeypatch.setattr(dd2_run, "_sub", fake_sub)
    monkeypatch.setattr(dd2_run, "_enrich_from_raw", lambda r, p: r)
    return run_dir, specs


def test_retry_thin_none_axes_respawns_only_thin_axis_once(tmp_path, monkeypatch):
    run_dir, specs = _thin_env(tmp_path, monkeypatch)
    spawned = []

    def fake_spawn_many(sp, max_parallel=4):
        for s in sp:
            spawned.append(s)
            assert not (run_dir / "parts/axes_1.json").exists()          # 舊檔先刪（子 agent 沒有 Read）
            assert "補查" in (run_dir / s["prompt"]).read_text(encoding="utf-8")
            _write_part(run_dir / "parts/axes_1.json", "thin_axis", "found", ["q1", "q2"], [{"claim": "新查到"}])
        return [{"ok": True} for _ in sp]

    monkeypatch.setattr(dd2_run.dd_headless, "spawn_many", fake_spawn_many)
    ctx, st = _Ctx(run_dir), {"agent_usage": []}
    dd2_run._retry_thin_none_axes(ctx, st, specs, "python3")
    assert [s["id"] for s in spawned] == ["a_1_thin_axis_retry"]           # 只有 thin；2 條查詢／缺口檔／found 都不補
    new = json.loads((run_dir / "parts/axes_1.json").read_text(encoding="utf-8"))
    assert new["coverage"]["thin_axis"]["status"] == "found"
    assert (run_dir / "parts/axes_1.json.thin1").exists()
    assert st["thin_none_retry"]["thin_axis"] == {
        "queries_before": 1, "queries_after": 2, "status_after": "found", "kept_retry": True}
    assert len(st["agent_usage"]) == 1
    # 同一份 parts 再跑一次（例如 --resume）：已有 .thin1 記號，不再補派
    spawned.clear()
    dd2_run._retry_thin_none_axes(ctx, {"agent_usage": []}, specs, "python3")
    assert spawned == []


def test_retry_thin_none_axes_restores_original_when_retry_fails(tmp_path, monkeypatch):
    run_dir, specs = _thin_env(tmp_path, monkeypatch)
    monkeypatch.setattr(dd2_run.dd_headless, "spawn_many", lambda sp, max_parallel=4: [{"ok": False} for _ in sp])
    ctx, st = _Ctx(run_dir), {"agent_usage": []}
    dd2_run._retry_thin_none_axes(ctx, st, specs, "python3")
    kept = json.loads((run_dir / "parts/axes_1.json").read_text(encoding="utf-8"))
    assert kept["coverage"]["thin_axis"]["queries_run"] == ["q1"]            # 原件還原
    assert st["thin_none_retry"]["thin_axis"]["kept_retry"] is False


def test_retry_thin_none_axes_noop_when_nothing_thin(tmp_path, monkeypatch):
    run_dir, specs = _thin_env(tmp_path, monkeypatch)
    _write_part(run_dir / "parts/axes_1.json", "thin_axis", "none", ["q1", "q2"])
    monkeypatch.setattr(dd2_run.dd_headless, "spawn_many",
                        lambda *a, **k: pytest.fail("沒有薄軸不該派工"))
    dd2_run._retry_thin_none_axes(_Ctx(run_dir), {"agent_usage": []}, specs, "python3")


# ---------------------------------------------------------------------------
# (e) 散文自動修一次
# ---------------------------------------------------------------------------

UNC = "validate_prose：2 個未覆蓋數字：12.5%（…毛利率 12.5%…）"


def _prose_ctx(tmp_path, sids=("s5", "s7")):
    run_dir = tmp_path / "run"
    (run_dir / "prose").mkdir(parents=True)
    (run_dir / "prompts").mkdir()
    (run_dir / "agents").mkdir()
    (run_dir / "prompts" / "prose_A.md").write_text("BASE 散文卡與白名單", encoding="utf-8")
    for sid in sids:
        (run_dir / "prose" / (sid + ".html")).write_text("<section><h2>{0}</h2><p>毛利率 12.5%</p></section>".format(sid),
                                                         encoding="utf-8")
    ctx = _Ctx(run_dir)
    ctx.prose_misses = {"s5": [{"raw": "12.5%", "context": "毛利率 12.5% 高於同業"},
                               {"raw": "3.2 倍", "context": "約 3.2 倍"}]}
    return ctx


def test_prose_fix_targets_uncovered_only(tmp_path):
    ctx = _prose_ctx(tmp_path)
    sids, unc = dd2_run._prose_fix_targets(ctx, [("s5", UNC)])
    assert sids == ["s5"] and list(unc) == ["s5"] and len(unc["s5"]) == 2


def test_prose_fix_targets_mixed_short_and_uncovered(tmp_path):
    ctx = _prose_ctx(tmp_path)
    sids, unc = dd2_run._prose_fix_targets(ctx, [("s5", UNC), ("s7", "篇幅 800B < 下限 1,200B"), ("_depth", "整檔 60,000B < 下限 70,000B")])
    assert sids == ["s7", "s5"] and list(unc) == ["s5"]


def test_prose_fix_targets_length_only_unchanged(tmp_path):
    ctx = _prose_ctx(tmp_path)
    sids, unc = dd2_run._prose_fix_targets(ctx, [("s7", "篇幅 800B < 下限 1,200B"), ("_depth", "散文本體 1B < 下限 2B")])
    assert sids == ["s7"] and unc == {}
    assert dd2_run._length_only_short_sids([("s7", "篇幅 800B < 下限 1,200B")]) == ["s7"]   # 舊函式不動


@pytest.mark.parametrize("findings", [
    [("s5", UNC), ("s5", "leaks：AI 痕跡（…）")],                       # 夾別種原因 → 不補寫
    [("s5", UNC), ("_qc", "qc 失敗")],
    [("_validate_prose", "驗證器壞了")],
    [("appA", UNC)],                                                     # 機械表章節的數字不是散文能解
    [("s99", UNC)],                                                      # prose/ 底下沒這章
    [("_depth", "整檔 60,000B < 下限 70,000B")],                         # 只有整檔偏短、沒有可重寫章節
    [],
])
def test_prose_fix_targets_not_applicable(tmp_path, findings):
    assert dd2_run._prose_fix_targets(_prose_ctx(tmp_path), findings) is None


def test_prose_fix_spawn_prompt_lists_numbers_and_rule(tmp_path, monkeypatch):
    ctx = _prose_ctx(tmp_path)
    captured = {}

    def fake_spawn_many(sp, max_parallel=1):
        captured["prompt"] = Path(sp[0]["prompt"]).read_text(encoding="utf-8")
        return [{"ok": True}]

    monkeypatch.setattr(dd2_run.dd_headless, "spawn_many", fake_spawn_many)
    monkeypatch.setattr(dd2_run, "_enrich_from_raw", lambda r, p: r)
    sids, unc = dd2_run._prose_fix_targets(ctx, [("s5", UNC), ("s7", "篇幅 800B < 下限 1,200B")])
    dd2_run._prose_fix_spawn(ctx, sids, unc)
    p = captured["prompt"]
    assert p.startswith("BASE 散文卡與白名單")
    assert "`12.5%` ｜ …毛利率 12.5% 高於同業…" in p and "`3.2 倍`" in p
    assert "要嘛刪掉" in p and "不得自行推算新數字" in p
    assert "`s5`：含 2 個未覆蓋數字" in p and "`s7`：現在" in p            # 兩種原因各自的列
    assert "<!-- SID:s5 -->" in p and "prose_fix.html" in p


def test_prose_fix_spawn_length_only_prompt_keeps_old_wording(tmp_path, monkeypatch):
    ctx = _prose_ctx(tmp_path)
    captured = {}
    monkeypatch.setattr(dd2_run.dd_headless, "spawn_many",
                        lambda sp, max_parallel=1: captured.setdefault("p", Path(sp[0]["prompt"]).read_text(encoding="utf-8")) and [{"ok": True}])
    monkeypatch.setattr(dd2_run, "_enrich_from_raw", lambda r, p: r)
    dd2_run._prose_fix_spawn(ctx, ["s7"])
    p = captured["p"]
    assert "只有下列章節篇幅不足、被硬閘擋下。" in p
    assert "做法：保留現稿的論點與結論，補的是深度" in p
    assert "未覆蓋數字" not in p


def test_gates_v20_stashes_structured_misses(tmp_path, monkeypatch):
    """_gates_v20 把 validate_prose 的 by_section 留在 ctx.prose_misses，供補寫提示列數字。"""
    ctx = _Ctx(tmp_path / "run")
    (ctx.run_dir / "prose").mkdir(parents=True)
    (ctx.run_dir / "tables").mkdir()
    (ctx.run_dir / "judgment.json").write_text("{}", encoding="utf-8")
    payload = {"by_section": {"s5": [{"raw": "12.5%", "context": "毛利率 12.5%"}]}}

    class _R:
        stdout, stderr, returncode = json.dumps(payload), "", 1

    monkeypatch.setattr(dd2_run.subprocess, "run", lambda *a, **k: _R())
    monkeypatch.setattr(dd2_run, "_sub", lambda cmd, cwd=None: (1, "assemble 故意失敗"))
    ok, findings, _ = dd2_run._gates_v20(ctx)
    assert not ok and findings[0][0] == "_assemble"        # 組裝先失敗，後面不跑；ctx.prose_misses 已初始化成空
    assert ctx.prose_misses == {}


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
