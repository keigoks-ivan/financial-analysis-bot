#!/usr/bin/env python3
"""測試 `scripts/dd_brief.py`（v17 WP5c：白話快速版重排）。

用四份回溯 fixture（notes/site-internal/dd/_src/{BE_20260905,CIEN_20260905,
CRDO_20260904,PANW_20260904}/）當固定樣本，涵蓋：
- CLI 兩種形狀都能跑（--judgment/--scenario-meta/--evidence 三檔法；--run-dir 目錄法）
- dd-meta 欄位與同一份 judgment 產出的真正上站 DD（docs/dd/DD_{T}.html）逐欄比對，
  必須全同（brief 只是零 LLM 重渲染，不應改變任何裁決欄位）
- qc.py 全形標點／結構檢查通過
- 缺值不崩：一份只剩 meta 的最小 judgment.json 仍能渲染出合法 HTML
- v17 `plain` 白話欄契約：四份 `_src` fixture 尚未帶 `plain`（WP5a/WP5b 是schema／
  prompt 端工作，不回填這些回溯 fixture），故渲染出的頁面每一個白話段落都應落
  入機械 fallback，帶 `class="fallback"`；反之，一份帶合法 `plain` 的 judgment
  應該讓五句話／三段故事等段落改用 `plain` 內容且不帶 `fallback` class。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
NOTES_DIR = ROOT / "notes" / "site-internal" / "dd"
SRC_DIR = NOTES_DIR / "_src"
DOCS_DD = ROOT / "docs" / "dd"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_brief  # noqa: E402

TICKERS = ["BE_20260905", "CIEN_20260905", "CRDO_20260904", "PANW_20260904"]

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.S
)


def _extract_dd_meta(html_text: str) -> dict:
    m = DD_META_RE.search(html_text)
    assert m, "dd-meta script block missing"
    return json.loads(m.group(1))


def _run_cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "dd_brief.py")] + args,
        capture_output=True, text=True, cwd=cwd or ROOT,
    )


def _valid_plain_block():
    """A `plain` block satisfying the WP5 batch-3 contract shape in full
    (see notes/site-internal/dd/_wp_spec_v17_batch3_20260905.md)."""
    return {
        "verdict_line": "進場，但只放三分之一",
        "verdict_sub": "生意是真的，價格也把好消息算進去了，先放三分之一等回檔。",
        "five": {
            "how_it_makes_money": "賣設備收一次錢，之後收服務費。",
            "why_now": "訂單成長比營收還快。",
            "why_this_size": "股價已經漲很多，五年期望值算下來是負的。",
            "biggest_fear": "關鍵材料供應被卡住。",
            "how_to_act": "新資金先放三分之一。",
        },
        "business": {
            "what_to_whom": "賣發電設備給資料中心與雲端業者。",
            "why_customers_stay": "電網排隊要等好幾年，它幾個月就能供電。",
            "moat_direction": "護城河中等，方向轉強，弱點在定價權。",
        },
        "bets": [
            {"claim": "缺電是結構性的", "wrong_when": "營收連兩季比指引少五個百分點"},
            {"claim": "規模擴大費用不會等比增加", "wrong_when": "毛利率連四季低於三成"},
            {"claim": "材料供應不會卡產能", "wrong_when": "產能連兩季卡在低檔"},
        ],
        "fears": [
            {"clock": "⚡", "text": "失去稅務抵免資格"},
            {"clock": "🔥", "text": "關鍵材料供給吃緊"},
            {"clock": "⚡", "text": "客戶集中度太高"},
        ],
        "market_wrong": "市場用了偏低的稅率假設，正常化後獲利會比共識低一截。",
        "growth_funding": "成長速度靠自己賺的錢撐不住，要靠借錢與稀釋。",
        "stories": {
            "bull": "產能順利擴大，市場給高倍數。",
            "base": "訂單照走但倍數會收斂，股價原地踏步。",
            "bear": "材料被卡、渦輪回歸，獲利腰斬。",
        },
        "change_my_mind": [
            {"what": "年報怎麼寫合規", "threshold": "寫到不確定", "then": "清倉", "when": "2027-02-28"},
            {"what": "產能有沒有爬升", "threshold": "連兩季卡關", "then": "減碼", "when": "2027-06-30"},
            {"what": "下一季財報", "threshold": "營收不達標", "then": "凍結加碼", "when": "2026-10-27"},
        ],
        "prior_compare_reason": "變化主因是價格漲多了，不是生意變壞。",
        "how_to_lose": "最可能的死法是材料被卡加上渦輪回歸，兩件事疊加把毛利率打回原形。",
        "evidence_quality": "十四軸都查得到料，逐字稿讀了最近四季。",
    }


@pytest.mark.parametrize("t", TICKERS)
def test_three_file_cli_matches_live_dd_meta(t, tmp_path):
    src = SRC_DIR / t
    live_dd = DOCS_DD / f"DD_{t}.html"
    if not live_dd.exists():
        pytest.skip(f"no live DD for {t}")
    out = tmp_path / f"{t}.html"
    r = _run_cli([
        "--judgment", str(src / f"{t}.judgment.json"),
        "--scenario-meta", str(src / f"{t}.scenario_meta.json"),
        "--evidence", str(src / f"{t}.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    assert out.exists()
    html_text = out.read_text(encoding="utf-8")

    brief_meta = _extract_dd_meta(html_text)
    live_meta = _extract_dd_meta(live_dd.read_text(encoding="utf-8"))
    assert brief_meta.get("brief") is True

    diff = {
        k: (brief_meta.get(k), live_meta.get(k))
        for k in live_meta
        # 2026-09-07：歷史完整版可能仍保存 judgment 的近似 EV／IRR／AR；
        # 新產物三欄改以 scenario 為權威，不能再拿舊 HTML 當 expected。
        if k not in ("brief", "ev5y_pct", "irr_base_pct", "asym_ratio")
        and brief_meta.get(k) != live_meta.get(k)
    }
    assert diff == {}, f"{t} dd-meta 欄位不同：{diff}"
    expected_meta = dd_brief.gdt.build_dd_meta(
        json.loads((src / f"{t}.judgment.json").read_text(encoding="utf-8")),
        json.loads((src / f"{t}.scenario_meta.json").read_text(encoding="utf-8")),
    )
    for field in ("ev5y_pct", "irr_base_pct", "asym_ratio"):
        assert brief_meta.get(field) == expected_meta.get(field)


@pytest.mark.parametrize("t", TICKERS)
def test_run_dir_cli_shape(t, tmp_path):
    src = SRC_DIR / t
    run_dir = tmp_path / t
    run_dir.mkdir()
    (run_dir / "judgment.json").write_text(
        (src / f"{t}.judgment.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (run_dir / "scenario_meta.json").write_text(
        (src / f"{t}.scenario_meta.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (run_dir / "evidence.json").write_text(
        (src / f"{t}.evidence.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    out = run_dir / "brief.html"
    r = _run_cli(["--run-dir", str(run_dir), "--out", str(out)])
    assert r.returncode == 0, r.stderr
    assert out.exists()
    meta = _extract_dd_meta(out.read_text(encoding="utf-8"))
    assert meta.get("brief") is True
    assert meta.get("ticker") == t.split("_")[0]


@pytest.mark.parametrize("t", TICKERS)
def test_qc_passes(t, tmp_path):
    src = SRC_DIR / t
    out = tmp_path / f"{t}.html"
    r = _run_cli([
        "--judgment", str(src / f"{t}.judgment.json"),
        "--scenario-meta", str(src / f"{t}.scenario_meta.json"),
        "--evidence", str(src / f"{t}.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    qc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "qc.py"), str(out)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert qc.returncode == 0, qc.stdout + qc.stderr
    assert "QC passed" in qc.stdout


@pytest.mark.parametrize("t", TICKERS)
def test_no_plain_fixture_falls_back_cleanly(t, tmp_path):
    """None of the four `_src` judgment.json fixtures carry `plain` yet (WP5a/
    WP5b are schema/prompt-side work, not a backfill of these regression
    fixtures) -- every plain-language section must therefore render via its
    mechanical fallback, flagged with class="fallback", with no leftover
    `{{TOKEN}}` placeholders."""
    src = SRC_DIR / t
    j = json.loads((src / f"{t}.judgment.json").read_text(encoding="utf-8"))
    assert "plain" not in j, f"{t} fixture unexpectedly already carries plain"
    out = tmp_path / f"{t}.html"
    r = _run_cli([
        "--judgment", str(src / f"{t}.judgment.json"),
        "--scenario-meta", str(src / f"{t}.scenario_meta.json"),
        "--evidence", str(src / f"{t}.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "{{" not in html_text
    assert 'class="fallback"' in html_text or ' fallback"' in html_text


def test_gate_audit_counts_render_in_decision_fold(tmp_path):
    audit = NOTES_DIR / "_audit_BE_20260905.md"
    if not audit.exists():
        pytest.skip("no _audit_BE_20260905.md fixture")
    src = SRC_DIR / "BE_20260905"
    out = tmp_path / "BE_with_audit.html"
    r = _run_cli([
        "--judgment", str(src / "BE_20260905.judgment.json"),
        "--scenario-meta", str(src / "BE_20260905.scenario_meta.json"),
        "--evidence", str(src / "BE_20260905.evidence.json"),
        "--audit", str(audit),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    # the audit's red/yellow counts must show up somewhere -- both in the
    # 「這個判斷建立在多少證據上」evidence-quality table and inside the folded
    # 「決策矩陣稽核」detail block (render_gate_yellow).
    assert "判斷級 🔴 1" in html_text
    assert "🟡 3" in html_text
    m = re.search(r"決策矩陣稽核、跨模型冷讀與各模組推理原文</summary>(.*?)</details>", html_text, re.S)
    assert m, "decision-audit fold missing"
    assert "本次未提供 gate audit" not in m.group(1)


def test_minimal_judgment_does_not_crash(tmp_path):
    """A judgment.json with almost nothing populated must still render valid
    HTML with '—' placeholders, never raise."""
    minimal = {
        "meta": {"ticker": "XX", "date": "2026-09-05", "schema": "v16.0", "company_name": "Test Co"}
    }
    jpath = tmp_path / "min.judgment.json"
    jpath.write_text(json.dumps(minimal), encoding="utf-8")
    out = tmp_path / "min_brief.html"
    r = _run_cli(["--judgment", str(jpath), "--out", str(out)])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "<title>XX 速判 2026-09-05</title>" in html_text
    meta = _extract_dd_meta(html_text)
    assert meta.get("ticker") == "XX"
    assert meta.get("brief") is True
    # no leftover unfilled {{TOKEN}} placeholders
    assert "{{" not in html_text


def test_unexpanded_block_renders_reason_line(tmp_path):
    """WP-D（B1–B4）：條件式區塊標成未展開時，快速版要看得到「未展開：理由」。"""
    src = SRC_DIR / "BE_20260905"
    j = copy.deepcopy(json.loads((src / "BE_20260905.judgment.json").read_text(encoding="utf-8")))
    j["industry"]["tam_table"] = {
        "expanded": False,
        "reason": "估值不靠低滲透；份額擴張成為承重假設時重新展開",
    }
    jpath = tmp_path / "BE_unexpanded.judgment.json"
    jpath.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "BE_unexpanded.html"
    r = _run_cli([
        "--judgment", str(jpath),
        "--scenario-meta", str(src / "BE_20260905.scenario_meta.json"),
        "--evidence", str(src / "BE_20260905.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "{{" not in html_text
    assert "未展開區塊" in html_text
    assert "市場邊界與利潤池——估值不靠低滲透" in html_text


def test_counter_evidence_records_render_by_view(tmp_path):
    """WP-D（A1）：反證紀錄按三視角分組渲染；plain.how_to_lose 缺時走這條 fallback。"""
    src = SRC_DIR / "BE_20260905"
    j = copy.deepcopy(json.loads((src / "BE_20260905.judgment.json").read_text(encoding="utf-8")))
    j.pop("plain", None)
    j["premortem"]["blind_spots"] = [
        {"view": "論點失敗", "evidence": "訂單能見度只到 2027",
         "assumption": "H1 產能滿載", "consequence": "FY2 EPS 砍三成",
         "ruling": "採納", "watch": "季度 backlog"},
        {"view": "價格已反映太多", "evidence": "五年分位 92%",
         "assumption": "終端倍數不收斂", "consequence": "re-rate 由正轉負",
         "ruling": "採納", "watch": "FY2 倍數"},
    ]
    j["premortem"].pop("failure_story", None)
    j["premortem"].pop("second_failure", None)
    jpath = tmp_path / "BE_counter.judgment.json"
    jpath.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "BE_counter.html"
    r = _run_cli([
        "--judgment", str(jpath),
        "--scenario-meta", str(src / "BE_20260905.scenario_meta.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "{{" not in html_text
    assert "<b>論點失敗</b>" in html_text
    assert "<b>價格已反映太多</b>" in html_text
    assert "訂單能見度只到 2027 → H1 產能滿載" in html_text
    assert "觀測點：季度 backlog" in html_text


def test_max_dd_without_trigger_time_renders_clean(tmp_path):
    """WP-D（撤配額 4）：Max DD 沒有觸發時點時不留下空冒號。"""
    src = SRC_DIR / "BE_20260905"
    j = copy.deepcopy(json.loads((src / "BE_20260905.judgment.json").read_text(encoding="utf-8")))
    j.pop("plain", None)
    j["premortem"].pop("failure_story", None)
    j["premortem"].pop("second_failure", None)
    j["premortem"]["blind_spots"] = []
    j["premortem"]["max_dd"].pop("trigger_time", None)
    jpath = tmp_path / "BE_nodd.judgment.json"
    jpath.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "BE_nodd.html"
    r = _run_cli(["--judgment", str(jpath), "--out", str(out)])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "（路徑風險" in html_text
    assert "）：</p>" not in html_text


def test_missing_judgment_file_exits_nonzero(tmp_path):
    out = tmp_path / "nope.html"
    r = _run_cli(["--judgment", str(tmp_path / "does_not_exist.json"), "--out", str(out)])
    assert r.returncode != 0
    assert not out.exists()


def test_valid_plain_block_renders_five_and_stories_without_fallback(tmp_path):
    """自造一份合法 `plain`（形狀依 _wp_spec_v17_batch3_20260905.md 契約）：
    五句話與三段故事必須出現且不帶 fallback class（WP5a 的
    /tmp/v17_plain_ok.json 尚未存在時，本測試就地造一份等效 fixture）。"""
    src = SRC_DIR / "BE_20260905"
    j = json.loads((src / "BE_20260905.judgment.json").read_text(encoding="utf-8"))
    j = copy.deepcopy(j)
    j["plain"] = _valid_plain_block()
    jpath = tmp_path / "BE_with_plain.judgment.json"
    jpath.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "BE_with_plain.html"
    r = _run_cli([
        "--judgment", str(jpath),
        "--scenario-meta", str(src / "BE_20260905.scenario_meta.json"),
        "--evidence", str(src / "BE_20260905.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "{{" not in html_text

    five_m = re.search(r"五句話</h2>\s*<div class=\"([^\"]*)\">(.*?)</div>\s*</section>", html_text, re.S)
    assert five_m, "five section missing"
    assert "fallback" not in five_m.group(1)
    assert "賣設備收一次錢" in five_m.group(2)

    stories_m = re.search(r"三種未來</h2>.*?<div class=\"([^\"]*)\">\s*<div class=\"story\">", html_text, re.S)
    assert stories_m, "stories block missing"
    assert "fallback" not in stories_m.group(1)
    assert "產能順利擴大" in html_text
    assert "訂單照走但倍數會收斂" in html_text
    assert "材料被卡、渦輪回歸" in html_text


# ---------------------------------------------------------------------------
# WP8 待補 #5：CJK 後半形標點轉全形（`,;:!?`），不動英文/數字間的標點
# ---------------------------------------------------------------------------

def test_cjk_punct_fullwidth_converts_five_marks_after_cjk():
    assert dd_brief._cjk_punct_fullwidth("停產,復工") == "停產，復工"
    assert dd_brief._cjk_punct_fullwidth("市場;供給") == "市場；供給"
    assert dd_brief._cjk_punct_fullwidth("重點:缺料") == "重點：缺料"
    assert dd_brief._cjk_punct_fullwidth("擴產!") == "擴產！"
    assert dd_brief._cjk_punct_fullwidth("為什麼?") == "為什麼？"


def test_cjk_punct_fullwidth_does_not_touch_ascii_context():
    # 英文/數字之間的半形標點不得被改
    assert dd_brief._cjk_punct_fullwidth("3,000 units") == "3,000 units"
    assert dd_brief._cjk_punct_fullwidth("GAAP, non-GAAP") == "GAAP, non-GAAP"
    # 混合句：只有緊接在 CJK 字元後面的那個標點才轉
    mixed = dd_brief._cjk_punct_fullwidth("營收 3,000 億,續創新高")
    assert mixed == "營收 3,000 億，續創新高"


def test_esc_applies_cjk_punct_fullwidth_before_html_escape():
    assert dd_brief.esc("場,景") == "場，景"
    # 與 html.escape 相容：特殊字元仍要轉義
    assert dd_brief.esc("A&B,場,景") == "A&amp;B,場，景"


def test_render_negative_evidence_claim_fullwidths_half_width_punct_after_cjk():
    """WP8 待補 #5 的實測場景重現（STRL）：子 agent 寫的 finding claim 帶
    半形逗號（如「…市場,占比…」），render_negative_evidence 渲染進負向
    證據處置表時必須已轉全形，不能讓半形逗號原樣流進上站 HTML 被
    pre-push QC（CJK 後半形標點）擋下。"""
    evidence = {
        "coverage": {
            "demand": {
                "findings": [
                    {
                        "claim": "資料中心市場,占比持續上升，但終端需求疲弱",
                        "source": "法說",
                        "as_of": "2026-08",
                        "direction": "-",
                    }
                ]
            }
        }
    }
    row_html = dd_brief.render_negative_evidence({}, evidence)
    assert "市場,占比" not in row_html
    assert "市場，占比" in row_html


# ---------------------------------------------------------------------------
# WP-E（2026-09-10）：修 WP-D 修 #4（Codex 複審
# notes/site-internal/dd/_codex_wpd_review_20260910.md 發現點 4）——新格式時
# plain.how_to_lose 只能當前言，不得取代 premortem.blind_spots[] 三視角反證。
# ---------------------------------------------------------------------------

def test_render_how_to_lose_new_format_shows_all_three_views_with_summary():
    """單元層級：直接呼叫 render_how_to_lose，重現 Codex 複審原始反例——
    plain.how_to_lose 非空時，新格式仍必須完整呈現三視角各自的獨有證據。"""
    data = {
        "plain": {"how_to_lose": "反證詳見下列三視角。"},
        "premortem": {
            "blind_spots": [
                {"view": view, "evidence": "獨有證據" + str(i)}
                for i, view in enumerate(dd_brief._COUNTER_VIEWS)
            ],
        },
    }
    html_text, is_fallback = dd_brief.render_how_to_lose(data)
    assert "反證詳見下列三視角。" in html_text
    for i in range(3):
        assert "獨有證據" + str(i) in html_text, html_text
    assert is_fallback is False


def test_render_how_to_lose_old_format_summary_still_replaces():
    """舊格式（有 failure_story，blind_spots 為純字串）維持原行為：
    how_to_lose 非空就整段用它取代機械渲染，不強制展開三視角區塊。"""
    data = {
        "plain": {"how_to_lose": "舊格式摘要。"},
        "premortem": {
            "failure_story": "舊式失敗故事",
            "blind_spots": ["盲點一", "盲點二"],
        },
    }
    html_text, is_fallback = dd_brief.render_how_to_lose(data)
    assert html_text.strip() == "<p>舊格式摘要。</p>"
    assert "盲點一" not in html_text
    assert is_fallback is False


def test_new_format_how_to_lose_summary_does_not_hide_counter_evidence_in_full_page(tmp_path):
    """整頁 CLI 層級：新格式 + plain.how_to_lose 同時存在時，交付 HTML 裡
    三視角的獨有證據都要出現，不能只看到摘要那一句。"""
    src = SRC_DIR / "BE_20260905"
    j = copy.deepcopy(json.loads((src / "BE_20260905.judgment.json").read_text(encoding="utf-8")))
    j["plain"] = j.get("plain") or {}
    j["plain"]["how_to_lose"] = "反證詳見下列三視角，本句不得取代之。"
    j["premortem"]["blind_spots"] = [
        {"view": "論點失敗", "evidence": "獨有證據Alpha"},
        {"view": "論點成功但股東經濟變差", "evidence": "獨有證據Beta"},
        {"view": "價格已反映太多", "evidence": "獨有證據Gamma"},
    ]
    j["premortem"].pop("failure_story", None)
    j["premortem"].pop("second_failure", None)
    jpath = tmp_path / "BE_newformat_summary.judgment.json"
    jpath.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    out = tmp_path / "BE_newformat_summary.html"
    r = _run_cli([
        "--judgment", str(jpath),
        "--scenario-meta", str(src / "BE_20260905.scenario_meta.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    html_text = out.read_text(encoding="utf-8")
    assert "{{" not in html_text
    assert "反證詳見下列三視角，本句不得取代之。" in html_text
    assert "獨有證據Alpha" in html_text
    assert "獨有證據Beta" in html_text
    assert "獨有證據Gamma" in html_text


# ---------------------------------------------------------------------------
# v18（2026-09-10 WP-F）：新形狀 fixture 要渲染得出六問、三視角反證與數字表；
# 舊形狀（沒有 plain.six）維持「五句話」標題與原本的 five 路徑，逐 byte 不變。
# ---------------------------------------------------------------------------

V18_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "judgment_v18_TXN.json"
V18_SRC = SRC_DIR / "TXN_20260907"


def _render_v18(tmp_path):
    out = tmp_path / "v18_TXN.html"
    r = _run_cli([
        "--judgment", str(V18_FIXTURE),
        "--scenario-meta", str(V18_SRC / "TXN_20260907.scenario_meta.json"),
        "--evidence", str(V18_SRC / "TXN_20260907.evidence.json"),
        "--out", str(out),
    ])
    assert r.returncode == 0, r.stderr
    return out.read_text(encoding="utf-8")


def test_v18_six_questions_render_one_paragraph_each(tmp_path):
    html_text = _render_v18(tmp_path)
    assert "{{" not in html_text
    m = re.search(r"六個問題</h2>\s*<div class=\"([^\"]*)\">(.*?)</div>\s*</section>", html_text, re.S)
    assert m, "六問首段未渲染"
    assert "fallback" not in m.group(1)
    body = m.group(2)
    for _key, label in dd_brief._SIX_ORDER:
        assert f"<b>{label}</b>" in body, f"六問缺「{label}」"
    assert body.count("<p>") == 6
    assert "五句話" not in html_text


def test_v18_three_counter_views_render(tmp_path):
    html_text = _render_v18(tmp_path)
    for view in dd_brief._COUNTER_VIEWS:
        assert f"<b>{view}</b>" in html_text, f"反證缺視角「{view}」"


def test_v18_numbers_survive_the_slim_shape(tmp_path):
    """EV／IRR／Max DD／PEG 四個數字：appendix_a 已不再重填 val／pct_5y 等投影
    欄，這些數字必須仍從權威欄（scenario／premortem／valuation／decision_inputs）
    渲染得出來，dd-meta 也要一起補回。"""
    html_text = _render_v18(tmp_path)
    assert re.search(r"5Y 期望值 EV</div><div class=\"v\">[+\-]\d", html_text)
    assert re.search(r"Base IRR</div><div class=\"v\">\d", html_text)
    assert re.search(r"Max DD</div><div class=\"v\">-\d+%", html_text)
    assert re.search(r"PEG \d", html_text)
    meta = _extract_dd_meta(html_text)
    for key in ("signal", "val", "ma", "verdict", "pct_5y", "upside_short_pct",
                "upside_mid_pct", "moat_score", "dca_role", "max_dd_pct",
                "ev5y_pct", "irr_base_pct", "peg_fy2"):
        assert meta.get(key) is not None, f"dd-meta 缺 {key}"


def test_old_shape_keeps_five_heading(tmp_path):
    """沒有 plain.six 的舊檔：標題仍是「五句話」（14 份重渲染 byte-identical 的
    契約，這裡用單元層再釘一次）。"""
    j = json.loads((SRC_DIR / "BE_20260905" / "BE_20260905.judgment.json").read_text(encoding="utf-8"))
    heading, _html, _fb = dd_brief.render_five(j)
    assert heading == dd_brief.LEAD_HEADING_FIVE
