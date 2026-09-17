"""Unit tests for scripts/engine/build_arena.py's `--lamp-only` read-only lamp
refresh (2026-09-17 席位引擎 v4「時機燈日更、席位月更」— see
knowledge/rule_ledger.md「時機燈日更、席位月更」row and build_arena.py's
`--lamp-only` docstring section).

Two levels, same style as scripts/tests/test_arena_rotation_v4.py:
  - `_refresh_row_timing()` is exercised with hand-made row/stock fixtures.
    `weekly_structure()` safely returns {} for a fake ticker with no
    data/weekly_cache*/ file on disk, so no cache fixtures are needed.
  - `run_lamp_only()` is exercised end-to-end against tmp paths (monkeypatched
    onto the module's path constants) to prove it never writes
    arena-ledger.json and leaves seats/scores/ranks untouched while updating
    lamp/action.

2026-09-17（全母體看板欄位對齊）：added coverage for the extended behavior where
`run_lamp_only()` also refreshes `own_board[]`'s timing fields (`_refresh_flat_view_timing()`)
and re-renders the full-board section of board.txt/_board_body.html in place, including
for a ticker that holds no seat at all (own_board-only row) — see
notes/site-internal/root/_seat_engine_v4_20260917.md「全母體看板欄位對齊」section.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from engine import build_arena  # noqa: E402
from engine.build_arena import (  # noqa: E402
    _own_board_ascii_hdr, _patch_seat_section_in_html, _patch_seat_section_in_text,
    _refresh_flat_view_timing, _refresh_row_timing, run_lamp_only,
)
from engine.grp import LAMP_ACTION  # noqa: E402


def _row(ticker, **grp_overrides):
    grp = {"above_w52": True, "p_label": "in_trend", "dist_hi": -10.0, "price": 100.0,
           "overheated": False, "g": 20.0, "pass": True, "own": {"score": 55.0}}
    grp.update(grp_overrides)
    return {"ticker": ticker, "score": 55.0, "rank": 3, "route": "core",
            "core_candidate": True, "seat_note": "現任", "durable_5y": True,
            "grp": grp, "lamp": {"code": "yellow", "label": "🟡 半倉"}, "action": "半倉",
            "r26": 5.0, "r52": 10.0}


def _stock(ticker, above_w52=True, dist_hi=-10.0, price=100.0, mom=None, vs200=1.0, rs=60.0):
    return {"ticker": ticker,
            "ma": {"above_w52": above_w52, "price": price, "mom_12_1_pct": mom},
            "timing": {"dist_52w_high_pct": dist_hi, "vs_200ma_pct": vs200, "rs_score": rs}}


def _flat_row(ticker, score=48.0, **overrides):
    """arena.json own_board[] 一列（`_flat_view()` 扁平 schema 的最小子集）——用於
    測試全母體表的每日時機刷新（`_refresh_flat_view_timing()`），特意不含 core_seats/
    sat_seats/bench_seats 才會出現的 rank/route/core_candidate 等欄位。"""
    row = {"ticker": ticker, "score": score, "p_label": "in_trend", "overheated": False,
           "mom": 12.0, "durable_5y": True, "lamp": {"code": "yellow", "label": "🟡 半倉"},
           "action": "半倉", "r26": 5.0, "dd_tag": None, "route_why": None, "seat_note": None}
    row.update(overrides)
    return row


# ── _refresh_row_timing(): updates timing fields only ─────────────────────

def test_refresh_row_timing_updates_only_timing_fields():
    row = _row("ZZZLAMP1")
    before_score, before_rank, before_route = row["score"], row["rank"], row["route"]
    before_g = row["grp"]["g"]
    s = _stock("ZZZLAMP1", above_w52=True, dist_hi=-3.0, price=123.0)
    _refresh_row_timing(row, s, {})
    # timing fields refreshed from the fresh grp_score() P-block
    assert row["grp"]["above_w52"] is True
    assert row["grp"]["dist_hi"] == -3.0
    assert row["grp"]["price"] == 123.0
    assert row["grp"]["p_label"] == "breakout"
    # ownership-layer fields (score/rank/route/g/pass/own) must stay untouched
    assert row["score"] == before_score
    assert row["rank"] == before_rank
    assert row["route"] == before_route
    assert row["grp"]["g"] == before_g
    assert row["grp"]["pass"] is True
    assert row["grp"]["own"] == {"score": 55.0}


def test_refresh_row_timing_updates_lamp_and_action_when_position_flips_to_out():
    row = _row("ZZZLAMP2")   # fixture starts "yellow" / 半倉
    s = _stock("ZZZLAMP2", above_w52=False)   # fell below the 52-week line
    _refresh_row_timing(row, s, {})
    assert row["grp"]["above_w52"] is False
    assert row["lamp"]["code"] == "out"
    assert row["action"] == LAMP_ACTION["out"]


def test_refresh_row_timing_overheated_flips_lamp_to_hot():
    row = _row("ZZZLAMP3")
    s = _stock("ZZZLAMP3", above_w52=True, dist_hi=-2.0, mom=200.0, vs200=2.0, rs=70.0)
    _refresh_row_timing(row, s, {})
    assert row["grp"]["overheated"] is True
    assert row["lamp"]["code"] == "hot"
    assert row["action"] == LAMP_ACTION["hot"]


# ── _refresh_flat_view_timing(): same contract as _refresh_row_timing() but for
#    own_board[]'s flat schema (2026-09-17 全母體看板欄位對齊) ──────────────────

def test_refresh_flat_view_timing_updates_only_timing_fields():
    v = _flat_row("ZZZFLAT1")
    before_score = v["score"]
    s = _stock("ZZZFLAT1", above_w52=True, dist_hi=-3.0, price=123.0)
    _refresh_flat_view_timing(v, s, {})
    # timing fields refreshed from the fresh grp_score() P-block
    assert v["p_label"] == "breakout"
    assert v["lamp"]["code"] in LAMP_ACTION
    # ownership-layer fields (score, and rank which this schema simply has none of)
    # must stay untouched
    assert v["score"] == before_score
    assert "rank" not in v


def test_refresh_flat_view_timing_flips_lamp_to_out_when_below_52w():
    v = _flat_row("ZZZFLAT2")   # fixture starts "yellow" / 半倉
    s = _stock("ZZZFLAT2", above_w52=False)   # fell below the 52-week line
    _refresh_flat_view_timing(v, s, {})
    assert v["p_label"] is None
    assert v["lamp"]["code"] == "out"
    assert v["action"] == LAMP_ACTION["out"]


def test_refresh_flat_view_timing_overheated_flips_lamp_to_hot():
    v = _flat_row("ZZZFLAT3")
    s = _stock("ZZZFLAT3", above_w52=True, dist_hi=-2.0, mom=200.0, vs200=2.0, rs=70.0)
    _refresh_flat_view_timing(v, s, {})
    assert v["overheated"] is True
    assert v["mom"] == 200.0
    assert v["lamp"]["code"] == "hot"
    assert v["action"] == LAMP_ACTION["hot"]


# ── seat-section text/html splice helpers: graceful None on missing marker ─

def test_patch_seat_section_in_text_returns_none_when_marker_missing():
    assert _patch_seat_section_in_text("no markers in this file at all", ["x"]) is None


def test_patch_seat_section_in_html_returns_none_when_marker_missing():
    assert _patch_seat_section_in_html("<div>no markers here</div>", "<p>new</p>") is None


# ── run_lamp_only(): end-to-end against tmp paths ──────────────────────────

def _arena_payload_fixture():
    return {
        "schema_version": "4.0",
        "core_seats": [_row("CORE1"), _row("CORE2")],
        "sat_seats": [_row("SAT1")],
        "bench_seats": [_row("BENCH1")],
        # BOARD1：只出現在全母體表、不坐任何席的列——用來驗證 --lamp-only 現在也
        # 每日刷新全母體表的時機／倉位（2026-09-17 全母體看板欄位對齊）。
        "own_board": [{"ticker": "CORE1", "score": 55.0}, _flat_row("BOARD1", score=48.0)],
        "duels": [], "regime": {"level": 1.0}, "rotation": {"rotated": False},
        "concentration": [{"sector": "Tech", "n": 3}],
    }


def _patch_paths(monkeypatch, tmp_path):
    paths = {
        "ARENA_JSON": tmp_path / "arena.json",
        "LEDGER_JSON": tmp_path / "arena-ledger.json",
        "BOARD_TXT": tmp_path / "board.txt",
        "BOARD_HTML": tmp_path / "_board_body.html",
        "DD_LATEST": tmp_path / "latest.json",
        "QGM_US": tmp_path / "qgm_us.json",
        "QGM_TW": tmp_path / "qgm_tw.json",
        "LAMP_JSON": tmp_path / "lamp.json",
    }
    for name, p in paths.items():
        monkeypatch.setattr(build_arena, name, p)
    return paths


def _write_common_fixtures(paths, core_ticker="CORE1"):
    paths["DD_LATEST"].write_text(json.dumps({
        "as_of": "2026-09-20",
        "stocks": [
            {"ticker": core_ticker, "dd_status": "dd",
             "ma": {"above_w52": True, "price": 50.0, "mom_12_1_pct": None},
             "timing": {"dist_52w_high_pct": -1.0, "vs_200ma_pct": 3.0, "rs_score": 80.0}},
            # BOARD1：全母體表獨有列的來源資料（見 _arena_payload_fixture()）——
            # 給它一組會把 fixture 起始值 yellow/半倉 翻成 green/正常倉 的多頭排列輸入。
            {"ticker": "BOARD1", "dd_status": "dd",
             "ma": {"above_w52": True, "price": 80.0, "mom_12_1_pct": 22.0},
             "timing": {"dist_52w_high_pct": -1.0, "vs_200ma_pct": 3.0, "rs_score": 80.0}},
        ],
    }), encoding="utf-8")
    paths["QGM_US"].write_text(json.dumps({"candidates": []}), encoding="utf-8")
    paths["QGM_TW"].write_text(json.dumps({"candidates": []}), encoding="utf-8")
    paths["LAMP_JSON"].write_text(json.dumps({"as_of": "2026-09-20", "lamp": {}}), encoding="utf-8")


def test_run_lamp_only_never_writes_ledger_and_preserves_seats_scores_ranks(tmp_path, monkeypatch):
    paths = _patch_paths(monkeypatch, tmp_path)
    payload = _arena_payload_fixture()
    paths["ARENA_JSON"].write_text(json.dumps(payload), encoding="utf-8")
    _write_common_fixtures(paths)
    # arena-ledger.json 完全不存在（模擬目前 repo 真實狀態：v4 roster 尚未寫入）——
    # run_lamp_only() 必須退回 arena.json 現有席位，且全程不得建立/寫入該檔。

    rc = run_lamp_only()
    assert rc == 0
    assert not paths["LEDGER_JSON"].exists(), "--lamp-only 唯讀：全程不得建立/寫入 arena-ledger.json"

    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    assert out["lamp_source"] == "daily"
    assert out["lamp_as_of"] == "2026-09-20"

    core1 = next(r for r in out["core_seats"] if r["ticker"] == "CORE1")
    assert core1["score"] == 55.0
    assert core1["rank"] == 3
    assert core1["grp"]["pass"] is True
    assert core1["grp"]["g"] == 20.0
    # CORE1 有來源資料 -> 時機欄位被刷新（above_w52/位置/燈號）
    assert core1["grp"]["above_w52"] is True
    assert core1["grp"]["p_label"] == "breakout"
    assert core1["lamp"]["code"] in LAMP_ACTION

    # 找不到來源資料的席位（CORE2／SAT1／BENCH1）維持原 fixture 的 lamp/action，不崩潰
    core2 = next(r for r in out["core_seats"] if r["ticker"] == "CORE2")
    assert core2["lamp"]["code"] == "yellow"
    assert core2["action"] == "半倉"

    # 全母體表（own_board[]）也每日刷新（2026-09-17 全母體看板欄位對齊）：CORE1（有
    # 來源資料）的 own_board 列時機翻新、score 不變；BOARD1（不坐任何席、只出現在
    # own_board 的列）同樣被刷新——證明刷新不是只挑坐席的名字做。
    ob_core1 = next(r for r in out["own_board"] if r["ticker"] == "CORE1")
    assert ob_core1["score"] == 55.0   # 擁有層分數不因 --lamp-only 改變
    assert "p_label" in ob_core1 and "lamp" in ob_core1   # 時機欄位已補上

    ob_board1 = next(r for r in out["own_board"] if r["ticker"] == "BOARD1")
    assert ob_board1["score"] == 48.0   # score/rank 這條月頻時鐘完全不受影響
    assert ob_board1["p_label"] == "breakout"
    assert ob_board1["lamp"]["code"] == "green"
    assert ob_board1["action"] == LAMP_ACTION["green"]

    # 其餘 payload 欄位（duels／regime／rotation／concentration）原樣保留
    assert out["duels"] == payload["duels"]
    assert out["regime"] == payload["regime"]
    assert out["rotation"] == payload["rotation"]
    assert out["concentration"] == payload["concentration"]


def test_run_lamp_only_never_mutates_existing_ledger_file(tmp_path, monkeypatch):
    paths = _patch_paths(monkeypatch, tmp_path)
    paths["ARENA_JSON"].write_text(json.dumps(_arena_payload_fixture()), encoding="utf-8")
    _write_common_fixtures(paths)
    ledger_content = json.dumps({
        "schema_version": "4.0", "last_rotation_month": None, "roster": None,
        "snapshots": [{"date": "2026-09-12", "core": ["CORE1"], "sat": [], "rotated": True}],
    })
    paths["LEDGER_JSON"].write_text(ledger_content, encoding="utf-8")
    before = paths["LEDGER_JSON"].stat().st_mtime_ns

    rc = run_lamp_only()

    assert rc == 0
    assert paths["LEDGER_JSON"].read_text(encoding="utf-8") == ledger_content, (
        "--lamp-only 唯讀：既有 arena-ledger.json 內容必須逐位元組不變"
    )
    assert paths["LEDGER_JSON"].stat().st_mtime_ns == before


def test_run_lamp_only_prefers_ledger_roster_over_arena_json_seats(tmp_path, monkeypatch):
    paths = _patch_paths(monkeypatch, tmp_path)
    payload = _arena_payload_fixture()   # arena.json 現有席位：CORE1/CORE2 核心、SAT1 衛星
    paths["ARENA_JSON"].write_text(json.dumps(payload), encoding="utf-8")
    _write_common_fixtures(paths, core_ticker="CORE2")
    # ledger 有 roster，只認 CORE2（核心）／SAT1（衛星）——run_lamp_only() 應以 ledger
    # 的 roster 為準決定「誰現在坐哪席」，不是照抄 arena.json 舊的核心清單。
    ledger_content = json.dumps({"roster": {"core": ["CORE2"], "sat": ["SAT1"]}})
    paths["LEDGER_JSON"].write_text(ledger_content, encoding="utf-8")

    rc = run_lamp_only()

    assert rc == 0
    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    assert [r["ticker"] for r in out["core_seats"]] == ["CORE2"]
    assert [r["ticker"] for r in out["sat_seats"]] == ["SAT1"]
    assert paths["LEDGER_JSON"].read_text(encoding="utf-8") == ledger_content


def test_run_lamp_only_exits_zero_with_warning_when_arena_json_missing(tmp_path, monkeypatch, capsys):
    paths = _patch_paths(monkeypatch, tmp_path)
    assert not paths["ARENA_JSON"].exists()

    rc = run_lamp_only()

    assert rc == 0
    assert not paths["LEDGER_JSON"].exists()
    captured = capsys.readouterr()
    assert "::warning::" in captured.out


def _board_txt_fixture() -> str:
    """board.txt 最小 fixture——含席位表／全母體表兩段 marker，供全母體表原地刷新
    測試用（見 _patch_seat_section_in_text()／_patch_main_table_in_text()）。"""
    return "\n".join([
        "== 目前席位：核心 5 ＋ 衛星 5 ＋ 候補 5",
        "OLD SEAT ROW",
        _own_board_ascii_hdr(),
        "OLD MAIN ROW",
        "",
        "== DD 裁決進場 vs 機械資格",
        "OLD DD GATE LINE",
    ]) + "\n"


def _board_html_fixture() -> str:
    return ('<h3 class="bw-sec">目前席位：核心 5 ＋ 衛星 5 ＋ 候補 5</h3>OLD_SEAT_HTML'
           '<h3 class="bw-sec">全母體看板（擁有層排序）</h3>OLD_MAIN_HTML'
           '<h3 class="bw-sec">DD 進場 vs 機械資格</h3>OLD_DD_GATE_HTML')


def test_run_lamp_only_refreshes_main_table_section_when_own_board_present(tmp_path, monkeypatch):
    paths = _patch_paths(monkeypatch, tmp_path)
    paths["ARENA_JSON"].write_text(json.dumps(_arena_payload_fixture()), encoding="utf-8")
    _write_common_fixtures(paths)
    paths["BOARD_TXT"].write_text(_board_txt_fixture(), encoding="utf-8")
    paths["BOARD_HTML"].write_text(_board_html_fixture(), encoding="utf-8")

    rc = run_lamp_only()
    assert rc == 0

    txt = paths["BOARD_TXT"].read_text(encoding="utf-8")
    # 全母體表本體（表頭到 == DD 裁決 之間）被換成新內容，舊 placeholder 列消失，
    # BOARD1（非坐席、依 fixture 應翻成 green）出現在新內容裡。
    assert "OLD MAIN ROW" not in txt
    assert "BOARD1" in txt
    # 表頭本身（marker）與表頭之後的區段（DD 裁決那段）逐字不動。
    assert _own_board_ascii_hdr() in txt
    assert "OLD DD GATE LINE" in txt
    # 席位區塊本身也照舊被刷新（既有行為，未受本次擴充影響）。
    assert "OLD SEAT ROW" not in txt

    html = paths["BOARD_HTML"].read_text(encoding="utf-8")
    assert "OLD_MAIN_HTML" not in html
    assert "BOARD1" in html
    assert "OLD_DD_GATE_HTML" in html   # 下一段（DD 進場 vs 機械資格）逐字不動
    assert "OLD_SEAT_HTML" not in html


def test_run_lamp_only_falls_back_to_seat_section_only_when_own_board_missing(tmp_path, monkeypatch):
    paths = _patch_paths(monkeypatch, tmp_path)
    payload = _arena_payload_fixture()
    del payload["own_board"]   # 舊版 schema／缺 own_board 的情境——見 run_lamp_only() docstring
    paths["ARENA_JSON"].write_text(json.dumps(payload), encoding="utf-8")
    _write_common_fixtures(paths)
    paths["BOARD_TXT"].write_text(_board_txt_fixture(), encoding="utf-8")
    paths["BOARD_HTML"].write_text(_board_html_fixture(), encoding="utf-8")

    rc = run_lamp_only()
    assert rc == 0

    # 全母體表本體維持上次 --ledger 跑次內容不變（逐字保留 OLD MAIN ROW／OLD_MAIN_HTML）；
    # 席位區塊仍照舊每日刷新——這是本次擴充明訂的向下相容 fallback，不是漏刷新。
    txt = paths["BOARD_TXT"].read_text(encoding="utf-8")
    assert "OLD MAIN ROW" in txt
    assert "OLD SEAT ROW" not in txt

    html = paths["BOARD_HTML"].read_text(encoding="utf-8")
    assert "OLD_MAIN_HTML" in html
    assert "OLD_SEAT_HTML" not in html

    out = json.loads(paths["ARENA_JSON"].read_text(encoding="utf-8"))
    assert "own_board" not in out
    assert not paths["LEDGER_JSON"].exists()


def test_run_lamp_only_exits_zero_with_warning_when_no_seats_anywhere(tmp_path, monkeypatch, capsys):
    paths = _patch_paths(monkeypatch, tmp_path)
    paths["ARENA_JSON"].write_text(json.dumps({"core_seats": [], "sat_seats": [], "bench_seats": []}),
                                   encoding="utf-8")

    rc = run_lamp_only()

    assert rc == 0
    assert not paths["LEDGER_JSON"].exists()
    captured = capsys.readouterr()
    assert "::warning::" in captured.out
