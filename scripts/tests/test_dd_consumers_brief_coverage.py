#!/usr/bin/env python3
"""測試 P1-3 修復：DD consumer 一旦只 glob docs/dd/DD_*.html 根目錄，會漏讀
docs/dd/brief/BRIEF_*.html 快速版，導致下游讀到已被取代的舊裁決。

複審報告 notes/site-internal/dd/_review_v17_pipeline_20260907.md 指出 13 份
brief 全部比同 ticker 最新完整版新；本檔鎖住兩層迴歸：

  (a) 合成 fixture（tmp_path）——決定性驗證候選集合聯集、同日完整版優先
      tie-break、brief 相對路徑（"brief/BRIEF_..."）三件事，不依賴真實語料
      現況（真實語料目前沒有同日完整版＋快速版碰撞的案例）。
  (b) 對真實 docs/dd/ 語料的輕量 smoke test——用「動態算 glob 聯集」而非寫死
      668/13/681 這類數字，避免語料成長後測試腐化；只驗證「brief 有被看見」
      這個關係，不驗證絕對值。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import glob as globmod
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import aggregate_dca_stats  # noqa: E402
import aggregate_dd_stats  # noqa: E402
import check_dd_earnings_freshness  # noqa: E402
import check_tier_matrix  # noqa: E402
import dd_decision  # noqa: E402
import dd_meta_reader  # noqa: E402
import dd_prior  # noqa: E402
import inject_dd_livebar  # noqa: E402
import list_breakout_candidates  # noqa: E402
import snapshot_consensus  # noqa: E402
import sync_kill_registry  # noqa: E402

DD_DIR = ROOT / "docs" / "dd"
BRIEF_DIR = DD_DIR / "brief"


# ---------------------------------------------------------------------------
# synthetic fixture helpers
# ---------------------------------------------------------------------------

def _write_report(dd_dir: Path, prefix: str, ticker: str, date_str: str,
                   extra: dict | None = None) -> Path:
    """寫一份最小可用的 DD/BRIEF HTML（含 dd-meta script 區塊）。

    prefix="DD" 產出帶 <body></body> 的完整版形狀；prefix="BRIEF" 產出無
    <body> 的無頭片段（比照真實 docs/dd/brief/BRIEF_*.html 現況——見
    inject_dd_livebar 遷移時的實測發現：brief 是 bodyless fragment）。
    """
    date_iso = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    meta = {
        "ticker": ticker,
        "schema": "v15.0",
        "date": date_iso,
        "price_at_dd": 100.0,
        "dca_verdict": "觀望",
        "dca_role": "追蹤",
        "kill_metrics": [
            {"metric": "測試證偽門檻", "bear_threshold": "測試門檻值", "window": "每季"}
        ],
    }
    if extra:
        meta.update(extra)
    meta_json = json.dumps(meta, ensure_ascii=False)
    script_tag = f'<script id="dd-meta" type="application/json">{meta_json}</script>'
    if prefix == "DD":
        html = f"<!DOCTYPE html>\n<html><body>\n{script_tag}\n</body></html>\n"
        out_dir = dd_dir
    else:
        html = f"<title>{ticker} 速判 {date_iso}</title>\n{script_tag}\n"
        out_dir = dd_dir / "brief"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{prefix}_{ticker}_{date_str}.html"
    path.write_text(html, encoding="utf-8")
    return path


def _build_fixture_tree(tmp_path: Path) -> Path:
    """三檔 ticker：
    AAA — 兩份完整版（20260101 舊／20260301）＋一份快速版（20260401，最新）。
    BBB — 一份完整版與一份快速版同日期（20260101）——測 tie-break：完整版優先。
    CCC — 只有快速版（20260301），沒有任何完整版。
    """
    dd_dir = tmp_path / "dd"
    _write_report(dd_dir, "DD", "AAA", "20260101")
    _write_report(dd_dir, "DD", "AAA", "20260301")
    _write_report(dd_dir, "BRIEF", "AAA", "20260401")
    _write_report(dd_dir, "DD", "BBB", "20260101")
    _write_report(dd_dir, "BRIEF", "BBB", "20260101")
    _write_report(dd_dir, "BRIEF", "CCC", "20260301")
    return dd_dir


def _live_full_count() -> int:
    return len(globmod.glob(str(DD_DIR / "DD_*.html")))


def _live_brief_count() -> int:
    if not BRIEF_DIR.exists():
        return 0
    return len(globmod.glob(str(BRIEF_DIR / "BRIEF_*.html")))


# ---------------------------------------------------------------------------
# (a) 合成 fixture — 決定性測試
# ---------------------------------------------------------------------------

def test_iter_dd_paths_union_and_tiebreak(tmp_path):
    dd_dir = _build_fixture_tree(tmp_path)
    paths = list(dd_meta_reader.iter_dd_paths(dd_dir, include_brief=True))
    assert len(paths) == 6  # 3 full + 3 brief

    latest = dict(
        (m["ticker"], p)
        for p, m in dd_meta_reader.iter_latest_dd_metas(dd_dir, include_brief=True)
    )
    assert latest["AAA"].name == "BRIEF_AAA_20260401.html"  # 純日期較新
    assert latest["BBB"].name == "DD_BBB_20260101.html"     # 同日完整版優先
    assert latest["CCC"].name == "BRIEF_CCC_20260301.html"  # 只有快速版


def test_dd_prior_find_dd_files_prefers_full_on_tie(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(dd_prior, "DD_DIR", dd_dir)
    # build_prior_dd() 另外用 REPO_ROOT 算相對路徑（與 DD_DIR 是兩個獨立常數），
    # 一併搬到 tmp_path 讓 fixture 檔案落在它的子路徑內。
    monkeypatch.setattr(dd_prior, "REPO_ROOT", tmp_path)

    files_aaa = dd_prior.find_dd_files("AAA")
    assert [f.name for _, f in files_aaa] == [
        "DD_AAA_20260101.html", "DD_AAA_20260301.html", "BRIEF_AAA_20260401.html",
    ]

    files_bbb = dd_prior.find_dd_files("BBB")
    # 同日期時完整版排在最後，讓 build_prior_dd() 的 cands[-1] 選中它。
    assert files_bbb[-1][1].name == "DD_BBB_20260101.html"

    prior = dd_prior.build_prior_dd("AAA", None)
    assert prior["path"].endswith("BRIEF_AAA_20260401.html")

    prior_bbb = dd_prior.build_prior_dd("BBB", None)
    assert prior_bbb["path"].endswith("DD_BBB_20260101.html")


def test_aggregate_dd_stats_load_records_brief_path_prefix(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(aggregate_dd_stats, "DD_DIR", dd_dir)
    monkeypatch.setattr(aggregate_dd_stats, "_get_table_attrs", lambda: {})

    records = aggregate_dd_stats.load_records()
    assert records["AAA"]["_path"] == "brief/BRIEF_AAA_20260401.html"
    assert records["BBB"]["_path"] == "DD_BBB_20260101.html"
    assert records["CCC"]["_path"] == "brief/BRIEF_CCC_20260301.html"


def test_aggregate_dca_stats_overlay_brief_path_and_link(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(aggregate_dca_stats, "DD_DIR", dd_dir)
    monkeypatch.setattr(aggregate_dca_stats, "DCA_DIR", tmp_path / "dca_empty")

    records = aggregate_dca_stats.load_dca_records()
    assert records["AAA"]["path"] == "brief/BRIEF_AAA_20260401.html"
    assert records["BBB"]["path"] == "DD_BBB_20260101.html"

    link = aggregate_dca_stats._ticker_link("AAA", records["AAA"]["path"])
    assert link.startswith('<a href="/dd/brief/BRIEF_AAA_20260401.html"')


def test_check_dd_earnings_freshness_brief_path(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(check_dd_earnings_freshness, "DD_DIR", dd_dir)

    records = check_dd_earnings_freshness.load_records()
    assert records["AAA"]["_path"] == "brief/BRIEF_AAA_20260401.html"
    assert records["AAA"]["date"] == "2026-04-01"


def test_check_tier_matrix_recent_signals_sees_brief(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(check_tier_matrix, "DD_DIR", dd_dir)

    # 用超大 days 值把 fixture 的日期全部涵蓋進來（不依賴「今天」）。
    signals = check_tier_matrix.get_recent_dd_signals(days=365 * 20)
    assert signals["AAA"]["date"].isoformat() == "2026-04-01"
    assert signals["BBB"]["date"].isoformat() == "2026-01-01"
    assert signals["CCC"]["date"].isoformat() == "2026-03-01"


def test_snapshot_consensus_base_path_ref_brief_dd_file(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(snapshot_consensus, "DD_DIR", dd_dir)

    notes: list = []
    ref = snapshot_consensus.resolve_base_path_ref("AAA", "2026-12-31", notes)
    assert ref["dd_file"] == "/dd/brief/BRIEF_AAA_20260401.html"


def test_list_breakout_candidates_dd_universe_includes_brief_only_ticker(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(list_breakout_candidates, "DD_DIR", dd_dir)

    universe = list_breakout_candidates.dd_universe()
    # CCC 只有快速版、沒有任何完整版——P1-3 修復前這裡會漏掉它。
    assert universe == {"AAA", "BBB", "CCC"}


def test_sync_kill_registry_scan_sees_brief_kill_metrics(tmp_path, monkeypatch):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(sync_kill_registry, "DD_DIR", dd_dir)

    rows = sync_kill_registry.scan_dd_kill_metrics()
    stems = {stem for stem, _doc_rel, _ticker, _km in rows}
    assert "BRIEF_CCC_20260301" in stems
    assert "BRIEF_AAA_20260401" in stems
    assert "DD_BBB_20260101" in stems
    assert "BRIEF_BBB_20260101" in stems  # additive：兩份都各自收，不去重


def test_inject_dd_livebar_scans_brief_and_flags_bodyless(tmp_path, monkeypatch, capsys):
    dd_dir = _build_fixture_tree(tmp_path)
    monkeypatch.setattr(inject_dd_livebar, "DD_DIR", str(dd_dir))
    monkeypatch.setattr(sys, "argv", ["inject_dd_livebar.py", "--dry-run"])

    rc = inject_dd_livebar.main()
    assert rc == 0
    out = capsys.readouterr().out
    assert "Scanned            : 6 DD_*.html + brief/BRIEF_*.html" in out
    # brief fixture 故意無 <body>，process() 應正確歸類為 skip-no-body 而非
    # 靜默漏看；三份 brief 全落這一類（無任何一份被誤判 injected）。
    assert "Skipped (no body)  : 3" in out
    assert "WOULD inject       : 3" in out  # 三份完整版都有 </body> 可注入


# ---------------------------------------------------------------------------
# (b) 真實語料 smoke test —— 動態算聯集，不寫死絕對數字
# ---------------------------------------------------------------------------

def test_live_repo_iter_dd_paths_matches_glob_union():
    expected = _live_full_count() + _live_brief_count()
    got = len(list(dd_meta_reader.iter_dd_paths(DD_DIR, include_brief=True)))
    assert got == expected


def test_live_repo_dd_decision_check_all_sees_every_brief_with_v15_schema(capsys):
    # dd_decision.cmd_check_all() 篩 schema 含 "v15" 的檔（同它自身邏輯，不
    # 寫死判斷式），故在這裡用一模一樣的字串測試法算期望集合。
    expected_stems = set()
    if BRIEF_DIR.exists():
        for f in sorted(BRIEF_DIR.glob("BRIEF_*.html")):
            text = f.read_text(encoding="utf-8", errors="ignore")
            if '"schema"' in text and "v15" in text:
                expected_stems.add(f.stem)

    rc = dd_decision.cmd_check_all(None, infer=False)
    assert rc == 0
    out = capsys.readouterr().out
    # 每份 schema=v15 的 brief 都必須出現在彙總表裡（P1-3 修復前恆為 0）。
    for stem in expected_stems:
        assert stem in out, f"{stem} 未出現在 check-all 彙總表輸出中"
