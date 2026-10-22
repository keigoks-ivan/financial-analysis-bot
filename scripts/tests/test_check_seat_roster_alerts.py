"""選股席位變化通知：首跑只建基準、進出席、排隊前 5 成員變動、名次對調不報、資料缺失不崩。
合成資料，不連網。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_seat_roster_alerts as m  # noqa: E402


def _seg(seats, queue):
    return {"seats": [{"t": t, "n": ""} for t in seats], "queue": [{"t": t, "n": ""} for t in queue]}


def _state(**segs):
    return {"schema": m.SCHEMA, "as_of": "2026-10-20", "segments": segs}


def test_first_run_baseline_only():
    segs = {"us": _seg(["A"], ["B", "C"])}
    r = m.compute(None, segs, "2026-10-21")
    assert r["baseline"] and r["lines"] == []
    assert r["new_state"]["segments"]["us"] == segs["us"]


def test_old_schema_state_is_baseline():
    old = {"as_of": "2026-10-21", "seats": {"A": {"section": "衛星", "stage": "S1"}}}
    r = m.compute(old, {"us": _seg(["A"], [])}, "2026-10-21")
    assert r["baseline"] and r["lines"] == []


def test_seat_in_and_out():
    prev = _state(us=_seg(["A", "B"], []))
    r = m.compute(prev, {"us": _seg(["B", "C"], [])}, "2026-10-21")
    (label, text), = r["lines"]
    assert label == "美股看板" and "進席 C" in text and "出席 A" in text and "排隊" not in text


def test_queue_membership_change_reported():
    prev = _state(us=_seg([], ["A", "B", "C", "D", "E"]))
    r = m.compute(prev, {"us": _seg([], ["A", "B", "C", "D", "F"])}, "2026-10-21")
    (_, text), = r["lines"]
    assert "新進 F" in text and "掉出 E" in text


def test_queue_reorder_not_reported():
    prev = _state(tw=_seg([], ["A", "B", "C"]))
    r = m.compute(prev, {"tw": _seg([], ["C", "A", "B"])}, "2026-10-21")
    assert r["lines"] == []


def test_queue_to_seat_annotated():
    prev = _state(tb=_seg(["S"], ["A"]))
    r = m.compute(prev, {"tb": _seg(["S", "A"], [])}, "2026-10-21")
    (_, text), = r["lines"]
    assert "進席 A" in text and "掉出 A（改進席）" in text


def test_missing_segment_keeps_old_state_and_silent():
    prev = _state(us=_seg(["A"], []), tw=_seg(["X"], []))
    r = m.compute(prev, {"us": _seg(["A"], [])}, "2026-10-21")
    assert r["lines"] == []
    assert r["new_state"]["segments"]["tw"] == prev["segments"]["tw"]


def test_tw_label_has_code_and_chinese_name():
    prev = {"seats": [{"t": "2330.TW", "n": "台積電"}], "queue": []}
    cur = {"seats": [], "queue": []}
    assert "出席 2330 台積電" in m._describe(m.diff_segment(prev, cur))


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def _point_at(monkeypatch, tmp_path):
    for name, rel in (("ARENA_JSON", "arena.json"), ("TW_JSON", "tw.json"), ("TB_JSON", "tb.json"),
                      ("STATE_JSON", "state.json"), ("ALERT_TXT", "alert.txt"),
                      ("SUBJECT_TXT", "subject.txt"), ("MAIL_HTML", "mail.html")):
        monkeypatch.setattr(m, name, tmp_path / rel)


def test_load_segments_queue_definitions(monkeypatch, tmp_path):
    _point_at(monkeypatch, tmp_path)
    _write(m.ARENA_JSON, {"run_timestamp": "2026-10-21T06:00:00Z", "core_seats": [{"ticker": "N"}],
                          "buyable_seats": [{"ticker": f"U{i}", "pool_rank": r}
                                            for i, r in enumerate([9, 3, 7, 1, 5, 2, 8])]})
    _write(m.TW_JSON, {"as_of": "2026-10-21", "core_seats": [],
                       "buyable": [{"ticker": f"{i}.TW", "name": f"名{i}"} for i in range(7)]})
    _write(m.TB_JSON, {"as_of": "2026-10-21", "seats": {"roster": [{"ticker": "T0"}, {"ticker": "T1"}]},
                       "buyable": [{"ticker": t} for t in ["T0", "Q1", "T1", "Q2", "Q3", "Q4", "Q5", "Q6"]]})
    segs, as_of = m.load_segments()
    assert as_of == "2026-10-21"
    assert [e["t"] for e in segs["us"]["queue"]] == ["U3", "U5", "U1", "U4", "U2"]  # pool_rank 1,2,3,5,7
    assert len(segs["tw"]["queue"]) == 5 and segs["tw"]["queue"][0]["n"] == "名0"
    assert [e["t"] for e in segs["tb"]["queue"]] == ["Q1", "Q2", "Q3", "Q4", "Q5"]  # 扣掉在席者


def test_main_missing_files_no_crash_no_write(monkeypatch, tmp_path):
    _point_at(monkeypatch, tmp_path)
    assert m.main([]) == 0
    assert not m.STATE_JSON.exists() and not m.ALERT_TXT.exists()


def test_main_end_to_end(monkeypatch, tmp_path):
    _point_at(monkeypatch, tmp_path)
    arena = {"run_timestamp": "2026-10-21T06:00:00Z", "core_seats": [{"ticker": "A"}],
             "buyable_seats": [{"ticker": "B", "pool_rank": 1}]}
    _write(m.ARENA_JSON, arena)
    assert m.main([]) == 0                      # 首跑：建基準，不發
    assert m.STATE_JSON.exists() and not m.ALERT_TXT.exists()
    assert m.main(["--dry-run"]) == 0           # 無變化
    arena["core_seats"] = [{"ticker": "C"}]
    _write(m.ARENA_JSON, arena)
    assert m.main(["--dry-run"]) == 0
    assert not m.ALERT_TXT.exists()             # dry-run 不寫檔
    assert m.main([]) == 0
    assert "進席 C" in m.ALERT_TXT.read_text(encoding="utf-8")
    assert m.SUBJECT_TXT.read_text(encoding="utf-8") == "🧭 選股席位變化 2026-10-21"
    assert "<" in m.MAIL_HTML.read_text(encoding="utf-8")
    assert m.main([]) == 0                      # 沒有新變化：舊通知檔被清掉
    assert not m.ALERT_TXT.exists()
