#!/usr/bin/env python3
"""測試 `scripts/dd_flash.py`（閃判即時裁決層）。

四類：
1. 證據沿用：`_find_reusable_evidence` 在 90 天窗內挑最新一份、窗外全數
   排除。
2. `_parse_flash_oneshot` fenced 解析：`json:flash`／`json:scenario` 標籤
   成功抽取；缺標籤／JSON 不合法都回 None。
3. 端到端整合（mock 判斷 spawn）：把 `TXN_20260906.judgment.json` 的
   `decision_inputs`／`plain` 併成一份假 flash 物件＋同份 fixture 的
   `scenario.json`，monkeypatch `ddreport._spawn_oneshot` 回傳這兩個
   fenced 區塊，走完步驟 5-7（`dd_scenario.py`／`dd_decision.py run`／
   markdown 渲染），確認 `decision_out` 有值、markdown 含固定第一行與
   結尾指令、且不寫任何檔案進 `docs/`。
4. 同一條端到端路徑，但把 `expected` 故意設成與矩陣算出的裁決不同，確認
   markdown 的 🔴 清單有「白話預期與矩陣不一致」。

不 spawn 真的模型（`ddreport._spawn_oneshot` 全程 monkeypatch）；
`dd_scenario.py`／`dd_decision.py run` 是零 LLM 腳本，讓它們真的跑（快、
不打網路）。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent
TXN_FIXTURE = REPO_ROOT / "notes" / "site-internal" / "dd" / "_src" / "TXN_20260906"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_flash  # noqa: E402
import ddreport  # noqa: E402


def _load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1) 證據沿用：90 天窗內挑最新
# ---------------------------------------------------------------------------

def test_find_reusable_evidence_picks_latest_within_window(tmp_path, monkeypatch):
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", tmp_path)
    from datetime import datetime, timedelta

    run_date = "20260401"
    run_dt = datetime.strptime(run_date, "%Y%m%d")

    # 三個候選：60 天前（窗內、較舊）、10 天前（窗內、最新）、200 天前（窗外）。
    for offset in (60, 10, 200):
        d = (run_dt - timedelta(days=offset)).strftime("%Y%m%d")
        folder = tmp_path / "ZFT_{0}".format(d)
        folder.mkdir()
        (folder / "{0}.evidence.json".format(folder.name)).write_text(
            json.dumps({"marker": offset}), encoding="utf-8")
        (folder / "{0}.transcript_digest.json".format(folder.name)).write_text(
            json.dumps({"items": []}), encoding="utf-8")

    ev_path, dig_path, age = dd_flash._find_reusable_evidence("ZFT", run_date)
    assert ev_path is not None and dig_path is not None
    assert age == 10
    assert json.loads(ev_path.read_text(encoding="utf-8"))["marker"] == 10


def test_find_reusable_evidence_none_when_all_outside_window(tmp_path, monkeypatch):
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", tmp_path)
    folder = tmp_path / "ZFT_20250101"
    folder.mkdir()
    (folder / "{0}.evidence.json".format(folder.name)).write_text("{}", encoding="utf-8")

    ev_path, dig_path, age = dd_flash._find_reusable_evidence("ZFT", "20260901")
    assert (ev_path, dig_path, age) == (None, None, None)


def test_find_reusable_evidence_no_archive_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(ddreport, "SRC_ARCHIVE_DIR", tmp_path / "no_such_dir")
    assert dd_flash._find_reusable_evidence("ZFT", "20260901") == (None, None, None)


# ---------------------------------------------------------------------------
# 2) fenced 解析
# ---------------------------------------------------------------------------

def test_parse_flash_oneshot_tagged_success():
    text = (
        "前言文字，不算數。\n"
        "```json:flash\n{\"a\": 1}\n```\n"
        "其他雜訊。\n"
        "```json:scenario\n{\"b\": 2}\n```\n"
    )
    parsed = dd_flash._parse_flash_oneshot(text)
    assert parsed == {"flash": {"a": 1}, "scenario": {"b": 2}}


def test_parse_flash_oneshot_missing_scenario_tag_returns_none():
    text = "```json:flash\n{\"a\": 1}\n```\n"
    assert dd_flash._parse_flash_oneshot(text) is None


def test_parse_flash_oneshot_invalid_json_returns_none():
    text = (
        "```json:flash\n{not valid json}\n```\n"
        "```json:scenario\n{\"b\": 2}\n```\n"
    )
    assert dd_flash._parse_flash_oneshot(text) is None


def test_parse_flash_oneshot_empty_text_returns_none():
    assert dd_flash._parse_flash_oneshot("") is None
    assert dd_flash._parse_flash_oneshot(None) is None


# ---------------------------------------------------------------------------
# 3)/4) 端到端整合：mock 判斷 spawn，走完算術與裁決＋markdown 渲染
# ---------------------------------------------------------------------------

def _make_flash_obj(judgment, expected_verdict, expected_role):
    """從 TXN 真實判斷物抽 `decision_inputs`／`plain`，其餘 flash 頂層鍵
    另外手填最小合法值（TXN judgment.json 是完整 v16.2 schema，沒有這幾個
    flash 專屬鍵）。`ev5y_pct`／`irr_base_pct`／`asym_ratio` 依 flash 規則
    清成 null，交給 `dd_scenario.py` 從 scenario.json 算回。"""
    decision_inputs = dict(judgment["decision_inputs"])
    for k in ("ev5y_pct", "irr_base_pct", "asym_ratio"):
        decision_inputs[k] = None
    return {
        "meta": {"ticker": "TXN", "date": "2026-09-06", "mode": "flash", "price": 258.44},
        "oneliner": "德儀（TXN）維持進場、核心持有。",
        "archetype": "品質複利成長",
        "decision_inputs": decision_inputs,
        "inputs_basis": {"signal": "見 numbers 同業表", "val": "見 numbers 估值分位"},
        "expected": {"verdict": expected_verdict, "role": expected_role, "row": "10"},
        "plain": judgment["plain"],
        "reasoning": {"valuation": "估值合理", "growth": "成長穩健", "moat": "護城河 A 級", "scenario": "機率依規則分配"},
        "evidence_gaps": [],
        "escalate": {"recommend_full": False, "why": "無特殊缺口，暫不需正式版"},
    }


def _run_mocked_flash(tmp_path, monkeypatch, expected_verdict, expected_role):
    judgment = _load_json(TXN_FIXTURE / "TXN_20260906.judgment.json")
    scenario = _load_json(TXN_FIXTURE / "TXN_20260906.scenario.json")
    flash_obj = _make_flash_obj(judgment, expected_verdict, expected_role)

    fake_text = (
        "```json:flash\n" + json.dumps(flash_obj, ensure_ascii=False) + "\n```\n"
        "```json:scenario\n" + json.dumps(scenario, ensure_ascii=False) + "\n```\n"
    )

    build_dir = tmp_path / "build"
    output_dir = tmp_path / "output"
    monkeypatch.setattr(dd_flash, "FLASH_BUILD_DIR", build_dir)
    monkeypatch.setattr(dd_flash, "FLASH_OUTPUT_DIR", output_dir)
    monkeypatch.setattr(
        dd_flash, "_run_zero_llm_prep",
        lambda py, ticker, date, parts_dir, peers_str: ({}, {}, []),
    )
    monkeypatch.setattr(
        dd_flash, "_find_reusable_evidence", lambda ticker, date: (None, None, None),
    )

    spawn_calls = []

    def fake_spawn_oneshot(prompt_path, model, out_json, cwd, budget):
        spawn_calls.append(model)
        return {
            "ok": True, "num_turns": 1, "cache_read": 12345, "cache_creation": 0,
            "output_tokens": 500, "cost_usd": 0.05, "duration_ms": 1000,
            "result_text": fake_text, "raw_path": None,
        }

    monkeypatch.setattr(ddreport, "_spawn_oneshot", fake_spawn_oneshot)

    rc = dd_flash.main(["TXN", "--date", "20260906", "--no-web"])
    run_dir = build_dir / "TXN_20260906"
    final_flash = _load_json(run_dir / "flash.json")
    out_md_path = output_dir / "TXN_20260906.md"
    md_text = out_md_path.read_text(encoding="utf-8") if out_md_path.exists() else ""
    return rc, final_flash, md_text, spawn_calls


@pytest.mark.skipif(not TXN_FIXTURE.exists(), reason="TXN_20260906 fixture 不存在")
def test_cmd_flash_end_to_end_produces_decision_and_markdown(tmp_path, monkeypatch):
    docs_dd_dir = REPO_ROOT / "docs" / "dd"
    before = set(p.name for p in docs_dd_dir.glob("*.html")) if docs_dd_dir.exists() else set()

    rc, final_flash, md_text, spawn_calls = _run_mocked_flash(
        tmp_path, monkeypatch, expected_verdict="進場", expected_role="核心",
    )

    after = set(p.name for p in docs_dd_dir.glob("*.html")) if docs_dd_dir.exists() else set()
    assert before == after, "閃判不應該寫任何檔案進 docs/"

    assert rc == 0
    assert len(spawn_calls) == 1  # 一次判斷就成功，不需要重試

    decision_out = final_flash.get("decision_out") or {}
    assert decision_out.get("verdict")
    assert decision_out.get("row_hit")

    assert md_text.startswith("⚡ 即時版（閃判）")
    assert "未經跨模型閘" in md_text
    assert "python3 scripts/ddreport.py batch TXN" in md_text
    assert "🔴 白話預期與矩陣不一致" not in md_text


@pytest.mark.skipif(not TXN_FIXTURE.exists(), reason="TXN_20260906 fixture 不存在")
def test_cmd_flash_flags_expected_mismatch(tmp_path, monkeypatch):
    # 矩陣真正算出的裁決是「進場／核心」（見 test 3）；這裡故意把 expected
    # 設成不同的裁決，驗證 🔴 清單抓得到。
    rc, final_flash, md_text, _spawn_calls = _run_mocked_flash(
        tmp_path, monkeypatch, expected_verdict="觀望", expected_role="衛星",
    )

    assert rc == 0
    decision_out = final_flash.get("decision_out") or {}
    assert decision_out.get("verdict") == "進場"  # 矩陣本身不受 expected 影響

    assert "白話預期與矩陣不一致" in md_text
    assert "expected.verdict='觀望'" in md_text or "expected.verdict=‘觀望’" in md_text or "觀望" in md_text
