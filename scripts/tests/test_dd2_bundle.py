#!/usr/bin/env python3
"""測試 `scripts/dd2/bundle.py`（dd2 v20 prompt bundle 組裝器，README §4 契約）。

用 `.dd_build/runs/FIX_20260911/`（有 evidence.json／facts.json／judgment.json／
parts/prior.json）當 fixture，只讀；每個測試把整個 run_dir 複製到 `tmp_path`
再組 bundle，不碰真實 fixture 目錄。涵蓋：

- 三個 builder（`build_judge`／`build_gate`／`build_prose`）都能跑，回傳
  `prompt_path`／`bundle_path`／`bytes`，且檔案真的落地。
- judge／gate／prose 的 bundle 不含 v17/v19 舊鏈的胖段落
  （`_evidence_compact`／`_digest_section`／`_judgment_rules_section` 的
  段落標題字樣）。
- judge bundle 含 `judge_card.md` 的來源戳檔頭，與兩張常載附卡
  （ROIC 持續期檢核、情境判斷問題字典）的標題。
- `select_addenda`：品質複利成長 → 空、循環/商品 → cyclical 附卡、
  金融 → archetype 附卡。
- `prior_summary`：一般情況與刻意灌爆 H/R 的情況都 ≤ 5,000 bytes（超過會
  先砍 H/R 的長文字欄，見 `bundle._trim_prior_rows`）。
- judge／gate 的最終 prompt 檔不含「Write」字樣（v20 判斷與閘都是單回合、
  無工具）。

Python 3.9 相容（`from __future__ import annotations`，不用 3.10+ 語法）。
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))

import bundle  # noqa: E402

FIXTURE_RUN_DIR = REPO_ROOT / ".dd_build" / "runs" / "FIX_20260911"
CARDS_DIR = SCRIPTS_DIR / "dd2" / "cards"

# 舊鏈 v17/v19 胖段落的段落標題字樣（README §4「不放」清單）：dd2 bundle 不得
# 出現，證明真的走的是 dd2 自己的組裝順序，不是不小心把整條舊鏈函式串回去。
_BANNED_SUBSTRINGS = (
    "## ③ Evidence 緊湊版",   # dd_bundle._evidence_compact
    "## ⑤ Digest",             # dd_bundle._digest_section
    "judgment-rules.md 全文",  # dd_bundle._judgment_rules_section 的段落標題
)


@pytest.fixture()
def run_dir(tmp_path) -> Path:
    dst = tmp_path / FIXTURE_RUN_DIR.name
    shutil.copytree(FIXTURE_RUN_DIR, dst)
    return dst


# ---------------------------------------------------------------------------
# 三個 builder 都能跑
# ---------------------------------------------------------------------------


def test_build_judge_runs_and_writes_files(run_dir):
    result = bundle.build_judge(run_dir, cards_dir=CARDS_DIR)

    assert result["prompt_path"] == run_dir / "prompts" / "judge.md"
    assert result["bundle_path"] == run_dir / "bundles" / "judge.md"
    assert result["prompt_path"].exists()
    assert result["bundle_path"].exists()
    assert isinstance(result["bytes"], dict)
    assert result["bytes"]["prompt_total"] > result["bytes"]["bundle_total"] > 0

    prompt_text = result["prompt_path"].read_text(encoding="utf-8")
    bundle_text = result["bundle_path"].read_text(encoding="utf-8")
    # 分隔行沿用舊鏈 `ddreport.py::BUNDLE_SEPARATOR` 慣例；bundle 全文原樣接在
    # 分隔行之後（用 endswith 而非按分隔字串 partition——任務頭本身的說明文字
    # 也會提到「===== BUNDLE =====」這個詞，partition 會切錯段）。
    assert bundle.BUNDLE_SEPARATOR in prompt_text
    assert prompt_text.endswith(bundle_text)
    header = prompt_text[: -len(bundle_text)]
    assert "FIX" in header


def test_build_gate_runs_and_writes_files(run_dir):
    result = bundle.build_gate(run_dir, cards_dir=CARDS_DIR)

    assert result["prompt_path"] == run_dir / "prompts" / "gate.md"
    assert result["bundle_path"] == run_dir / "bundles" / "gate.md"
    assert result["prompt_path"].exists()
    assert result["bundle_path"].exists()
    assert result["bytes"]["prompt_total"] > result["bytes"]["bundle_total"] > 0

    bundle_text = result["bundle_path"].read_text(encoding="utf-8")
    # 被審對象（judgment.json 全文）真的在 bundle 裡，且是緊湊格式（無縮排換行）。
    raw_judgment = json.loads((run_dir / "judgment.json").read_text(encoding="utf-8"))
    compact = json.dumps(raw_judgment, ensure_ascii=False, separators=(",", ":"))
    assert compact in bundle_text


def test_build_prose_runs_and_writes_files(run_dir):
    result = bundle.build_prose(run_dir, cards_dir=CARDS_DIR)

    assert result["prompt_path"] == run_dir / "prompts" / "prose.md"
    assert result["bundle_path"] == run_dir / "bundles" / "prose.md"
    assert result["prompt_path"].exists()
    assert result["bundle_path"].exists()
    assert result["bytes"]["prompt_total"] > result["bytes"]["bundle_total"] > 0

    prompt_text = result["prompt_path"].read_text(encoding="utf-8")
    # prose.md.tmpl 任務頭要點名兩個輸出檔與 s1-s7 / s8-s12+decision 分段。
    assert str(run_dir / "prose_A.html") in prompt_text
    assert str(run_dir / "prose_B.html") in prompt_text
    assert "s1" in prompt_text and "decision" in prompt_text


# ---------------------------------------------------------------------------
# 不放：v17/v19 舊鏈胖段落
# ---------------------------------------------------------------------------


def test_judge_bundle_excludes_legacy_fat_sections(run_dir):
    result = bundle.build_judge(run_dir, cards_dir=CARDS_DIR)
    text = result["bundle_path"].read_text(encoding="utf-8")
    for needle in _BANNED_SUBSTRINGS:
        assert needle not in text, "judge bundle 不該含舊鏈段落：{0}".format(needle)


def test_gate_bundle_excludes_legacy_fat_sections(run_dir):
    result = bundle.build_gate(run_dir, cards_dir=CARDS_DIR)
    text = result["bundle_path"].read_text(encoding="utf-8")
    for needle in _BANNED_SUBSTRINGS:
        assert needle not in text, "gate bundle 不該含舊鏈段落：{0}".format(needle)
    # gate_view（v17 機械抽出，v20 已由 gate_card.md ＋ referenced_facts 取代）
    assert "gate_view（機械抽出" not in text


# ---------------------------------------------------------------------------
# judge bundle 含 judge_card 檔頭與兩張常載附卡
# ---------------------------------------------------------------------------


def test_judge_bundle_contains_judge_card_header_and_always_load_addenda(run_dir):
    result = bundle.build_judge(run_dir, cards_dir=CARDS_DIR)
    text = result["bundle_path"].read_text(encoding="utf-8")

    judge_card_header = (CARDS_DIR / "judge_card.md").read_text(encoding="utf-8").splitlines()[0]
    assert judge_card_header in text

    roic_title = "§5.R 報酬持續期檢核（ROIC durability）附卡"
    playbook_title = "情境判斷問題字典附卡（QC-53）"
    assert roic_title in text
    assert playbook_title in text


# ---------------------------------------------------------------------------
# select_addenda
# ---------------------------------------------------------------------------


def test_select_addenda_quality_compounding_returns_empty():
    assert bundle.select_addenda("品質複利成長", CARDS_DIR) == []


def test_select_addenda_cyclical_returns_cyclical_card():
    paths = bundle.select_addenda("循環/商品", CARDS_DIR)
    assert [p.name for p in paths] == ["judge_addendum_cyclical.md"]
    assert paths[0].exists()


def test_select_addenda_financial_returns_archetype_card():
    paths = bundle.select_addenda("金融", CARDS_DIR)
    assert [p.name for p in paths] == ["judge_addendum_archetype.md"]
    assert paths[0].exists()


def test_select_addenda_default_cards_dir_matches_explicit(run_dir):
    # 契約簽名是 select_addenda(archetype_hint) -> list[Path]（單一位置參數即可
    # 呼叫），cards_dir 只是給 builder 覆寫用的選填參數。
    assert bundle.select_addenda("循環/商品") == bundle.select_addenda("循環/商品", CARDS_DIR)


def test_judge_bundle_with_cyclical_archetype_loads_conditional_addendum(run_dir):
    evidence_path = run_dir / "evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["archetype_hint"] = "循環/商品"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

    result = bundle.build_judge(run_dir, cards_dir=CARDS_DIR)
    text = result["bundle_path"].read_text(encoding="utf-8")
    assert "QC-42 循環交易讀數" in text
    assert "addendum_cyclical" in result["bytes"]


# ---------------------------------------------------------------------------
# prior_summary
# ---------------------------------------------------------------------------


def test_prior_summary_from_fixture_within_byte_cap(run_dir):
    prior_json = json.loads((run_dir / "parts" / "prior.json").read_text(encoding="utf-8"))
    text = bundle.prior_summary(prior_json)
    assert len(text.encode("utf-8")) <= bundle.PRIOR_SUMMARY_MAX_BYTES
    obj = json.loads(text)  # 必須是合法 JSON
    assert obj["date"]
    assert obj["verdict"]


def test_prior_summary_trims_h_and_r_when_oversized():
    big_rows = [
        {"id": "H{0}".format(i), "text": "t" * 50,
         "columns": {"a": "x" * 3000, "b": "y" * 3000}}
        for i in range(1, 5)
    ]
    prior_json = {
        "prior_dd": {
            "status": "ok", "date": "2026-05-16", "dca_verdict": "進場", "dca_role": "核心",
            "H": {"status": "ok", "format": "table", "rows": big_rows},
            "R": {"status": "ok", "format": "table", "rows": big_rows},
        }
    }
    raw_len = len(json.dumps(prior_json["prior_dd"], ensure_ascii=False).encode("utf-8"))
    assert raw_len > bundle.PRIOR_SUMMARY_MAX_BYTES  # 前提：不砍真的會超

    text = bundle.prior_summary(prior_json)
    assert len(text.encode("utf-8")) <= bundle.PRIOR_SUMMARY_MAX_BYTES
    obj = json.loads(text)
    assert obj["H"]["rows"][0] == {"id": "H1", "text": "t" * 50}
    assert "columns" not in obj["H"]["rows"][0]


def test_prior_summary_missing_prior_returns_compact_status():
    text = bundle.prior_summary({"prior_dd": {"status": "none"}})
    assert len(text.encode("utf-8")) <= bundle.PRIOR_SUMMARY_MAX_BYTES
    assert json.loads(text) == {"status": "none"}


# ---------------------------------------------------------------------------
# prompt 檔不含「Write」（judge／gate：單回合、無工具）
# ---------------------------------------------------------------------------


def test_judge_prompt_has_no_write_tool_language(run_dir):
    result = bundle.build_judge(run_dir, cards_dir=CARDS_DIR)
    text = result["prompt_path"].read_text(encoding="utf-8")
    assert "Write" not in text
    assert "下一次呼叫" not in text
    assert "只准改被點名欄位" not in text
    assert "max_turns" not in text


def test_gate_prompt_has_no_write_tool_language(run_dir):
    result = bundle.build_gate(run_dir, cards_dir=CARDS_DIR)
    text = result["prompt_path"].read_text(encoding="utf-8")
    assert "Write" not in text
    assert "下一次呼叫" not in text
    assert "只准改被點名欄位" not in text
    assert "max_turns" not in text


def test_prose_prompt_uses_write_tool(run_dir):
    # 對照組：散文層本來就該提 Write（唯一工具、最多 6 輪），不是全域禁詞。
    result = bundle.build_prose(run_dir, cards_dir=CARDS_DIR)
    text = result["prompt_path"].read_text(encoding="utf-8")
    assert "Write" in text
