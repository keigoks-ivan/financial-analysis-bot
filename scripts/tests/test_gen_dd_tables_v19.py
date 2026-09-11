#!/usr/bin/env python3
"""測試 `scripts/gen_dd_tables.py` 的 v19 版面片段 renderer（WP-H2-2，
2026-09-11）：頁首儀表板（五張卡／24 格篩選器資料列／改變主意三條）、§5/§6
的 v19 專屬表格（moat.spread_table 等欄位形狀與舊 E5/E7/E8 renderer 不同）、
v19 專用附錄 A/B/C 的條件式生成、以及 `_unexpanded_table()` 的 colspan 迴歸
測試（新增 `class="num"` 表頭後，舊的 exact-match `"<th>"` 計數曾把 5 欄算
成 1 欄）。

本檔只讀 `scripts/tests/fixtures/judgment_v19_FIX.json` 等既有 WP-H1 fixture，
不新增、不改動 fixture 本身。Python 3.9 相容（`from __future__ import
annotations`）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

sys.path.insert(0, str(SCRIPTS_DIR))
import dd_project  # noqa: E402
import gen_dd_tables as gdt  # noqa: E402

V19_JUDGMENT = FIXTURES / "judgment_v19_FIX.json"
V19_FACTS = FIXTURES / "facts_FIX_20260911.json"
V19_SCENARIO_META = FIXTURES / "scenario_meta_FIX_20260911.json"
V18_JUDGMENT = FIXTURES / "judgment_v18_TXN.json"


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def view():
    raw = _load(V19_JUDGMENT)
    return dd_project.view_for(raw, V19_JUDGMENT)


@pytest.fixture(scope="module")
def facts():
    return _load(V19_FACTS)


@pytest.fixture(scope="module")
def scenario_meta():
    return _load(V19_SCENARIO_META)


@pytest.fixture(scope="module")
def meta(view, scenario_meta):
    return gdt.build_dd_meta(view, scenario_meta)


# ---------------------------------------------------------------------------
# 頁首：條列拆分（_split_bullets）
# ---------------------------------------------------------------------------

def test_split_bullets_splits_on_semicolon():
    text = "資料中心機電承包龍頭，在手訂單 $14.1B、毛利率 25.9% 皆在高點；現價 32.9x FY26 要求高成長。"
    parts = gdt._split_bullets(text, max_items=3)
    assert len(parts) == 2
    assert "；" not in parts[0] and "；" not in parts[1]
    assert parts[0].startswith("資料中心")
    assert parts[1].startswith("現價")


def test_split_bullets_caps_at_max_items():
    text = "一；二；三；四；五"
    parts = gdt._split_bullets(text, max_items=3)
    assert len(parts) == 3
    # 超過上限的片段併入最後一條，用「，」不是「；」（不能違反本輪新規則）
    assert "；" not in parts[-1]


def test_split_bullets_single_segment_when_no_delimiter():
    text = "沒有分句標點的一整句話"
    parts = gdt._split_bullets(text, max_items=3)
    assert parts == [text]


def test_split_bullets_empty_input():
    assert gdt._split_bullets("") == []
    assert gdt._split_bullets(None) == []


# ---------------------------------------------------------------------------
# 頁首：v19-dashboard（五張卡／24 格／改變主意）
# ---------------------------------------------------------------------------

def test_header_top_uses_bullets_not_paragraph(view, meta, facts):
    html = gdt.render_v19_header_top_html(view, meta, facts)
    assert "<ul class=\"pts\"" in html
    assert "<p style=\"margin:0;font-size:16px" not in html  # 舊版單段 <p> 不應再出現
    assert "<li>" in html


def test_cards_html_has_five_cards(meta, view):
    html = gdt.render_v19_cards_html(meta, view)
    assert html.count('font-size:12px') >= 5  # 每張卡的 label div 至少各一個
    for label in ("裁決", "五年機率加權報酬", "基本情境年化", "最大回撤範圍", "本益比"):
        assert label in html


def test_maxdd_card_shows_shallow_to_deep_order(meta, view):
    """規格讀法：淺至深（如「−30～−56%」），不是數值由小到大排序。"""
    html = gdt.render_v19_cards_html(meta, view)
    i = html.find("最大回撤範圍")
    window = html[i:i + 400]
    assert "−30%～−56%" in window


def test_grid_html_has_24_cells(meta, view):
    html = gdt.render_v19_grid_html(meta, view)
    assert html.count('<div class="k">') == 24


def test_grid_missing_ai_risk_renders_em_dash():
    meta_no_ai = {"dca_verdict": "觀望"}
    html = gdt.render_v19_grid_html(meta_no_ai, {"decision_out": {}, "archetype": {}})
    i = html.find("AI 風險")
    assert "—" in html[i:i + 60]


def test_grid_rearm_label_depends_on_verdict(meta, view):
    html_hold = gdt.render_v19_grid_html(meta, view)
    assert "重啟門檻" in html_hold
    meta_buy = dict(meta, dca_verdict="進場")
    html_buy = gdt.render_v19_grid_html(meta_buy, {"decision_out": {"verdict": "進場"}, "archetype": {}})
    assert "加碼窗口" in html_buy


def test_changemind_has_three_items_no_semicolon_inside_strong(view):
    html = gdt.render_v19_changemind_html(view)
    assert html.count("<li>") == 3


def test_dashboard_assembles_header_cards_grid_changemind(view, meta, facts):
    html = gdt.render_v19_dashboard_html(view, meta, facts)
    assert html.startswith('<header')
    assert html.count('<div class="k">') == 24
    assert "什麼會讓我改變主意" in html
    assert html.count("<li>") >= 3  # 改變主意 3 條（頁首摘要條列另計，兩者都算 <li>）


# ---------------------------------------------------------------------------
# §5/§6 v19 專屬表格（欄位形狀與舊 E5/E7/E8 renderer 不同）
# ---------------------------------------------------------------------------

def test_spread_table_uses_wide_shape_columns(view):
    html = gdt.render_v19_spread_html(view)
    assert html is not None
    assert 'id="spread"' in html
    assert "FIX" in html and "EME" in html
    assert "16.45" in html  # FIX 營益率數字確實落進表格，不是空欄


def test_roic_checkpoints_uses_item_level_text_shape(view):
    html = gdt.render_v19_roic_checkpoints_html(view)
    assert html is not None
    assert "需求基礎值" in html
    assert html.count('<span class="dot"') >= 4


def test_segments_uses_share_driver_note_shape(view):
    html = gdt.render_v19_segments_html(view)
    assert html is not None
    assert "科技（資料中心＋半導體廠）" in html
    assert "58%（Q2）" in html


def test_threats_renders_when_present(view):
    html = gdt.render_v19_threats_html(view)
    assert html is not None
    assert "客戶自購設備" in html


def test_legacy_e5_e7_e8_are_empty_for_v19_shape_documenting_the_gap(view):
    """既有 E5/E7/E8 renderer 對 v19 判斷檔的欄位形狀不吻合——這不是本輪要修
    的東西（v19 版面改走 v19-spread/v19-roic/v19-segs），但迴歸測試留一個
    誠實的紀錄，避免以後有人誤以為 e5/e7/e8.html 對 v19 檔也能用。"""
    e5 = gdt.render_e5_html(view)
    e7 = gdt.render_e7_html(view)
    e8 = gdt.render_e8_html(view)
    assert "16.45" not in e5  # 對照 test_spread_table_uses_wide_shape_columns 有抓到
    assert "需求基礎值" not in e7
    assert "58%（Q2）" not in e8


# ---------------------------------------------------------------------------
# v19 附錄 A/B/C：appA 一律輸出，appB/appC 條件式
# ---------------------------------------------------------------------------

def test_appA_always_renders_and_does_not_fabricate_missing_fields(view, meta, facts):
    html = gdt.render_v19_appA_html(view, meta, facts)
    assert '<details id="appA">' in html
    assert "均線" in html
    assert "不進裁決" in html


def test_appB_renders_when_findings_digest_present(facts):
    html = gdt.render_v19_appB_html(facts)
    assert html is not None
    assert '<details id="appB">' in html


def test_appB_none_when_facts_missing():
    assert gdt.render_v19_appB_html(None) is None
    assert gdt.render_v19_appB_html({"findings_digest": []}) is None


def test_appC_renders_when_contradictions_have_prior_field(view):
    html = gdt.render_v19_appC_html(view)
    assert html is not None
    assert '<details id="appC">' in html
    assert "DRIFT_WATCH" in html


def test_appC_none_when_no_prior_field():
    assert gdt.render_v19_appC_html({"contradictions": [{"axis": "x", "prior_field": None}]}) is None
    assert gdt.render_v19_appC_html({}) is None


# ---------------------------------------------------------------------------
# _unexpanded_table colspan 迴歸測試（class="num" 表頭曾讓 exact-match count
# 算少，見 render-rules.md §2b 與 gen_dd_tables.py 該函式的模組註解）
# ---------------------------------------------------------------------------

def test_unexpanded_table_colspan_matches_header_with_num_class():
    header = ('<tr><th>年度</th><th class="num">回購</th><th class="num">股利</th>'
              '<th class="num">資本支出</th><th class="num">研發</th></tr>')
    block = {"expanded": False, "reason": "測試理由"}
    html = gdt._unexpanded_table("e10", block, header)
    assert html is not None
    assert 'colspan="5"' in html  # 5 個 <th>，不是被 exact-match "<th>" 漏算成 1


def test_e10_unexpanded_via_public_api_has_correct_colspan():
    judgment = {"governance": {"capital_returns": {"expanded": False, "reason": "有機成長"}}}
    html = gdt.render_e10_html(judgment)
    assert 'colspan="5"' in html


# ---------------------------------------------------------------------------
# main() CLI：v19 判斷檔多寫 v19-*.html；舊形狀判斷檔完全不寫
# ---------------------------------------------------------------------------

def test_cli_writes_v19_fragments_only_for_v19_contract(tmp_path):
    out_v19 = tmp_path / "v19_out"
    import subprocess
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "gen_dd_tables.py"), str(V19_JUDGMENT),
         "--out", str(out_v19), "--scenario-meta", str(V19_SCENARIO_META)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    for name in ("v19-dashboard.html", "v19-appA.html", "v19-revlog.html", "v19-s14.html",
                 "v19-spread.html", "v19-roic.html", "v19-segs.html"):
        assert (out_v19 / name).exists(), f"missing {name}"

    out_legacy = tmp_path / "legacy_out"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "gen_dd_tables.py"), str(V18_JUDGMENT),
         "--out", str(out_legacy)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    v19_files = list(out_legacy.glob("v19-*"))
    assert v19_files == [], f"legacy(非 v19) 判斷檔不應產出任何 v19-* 檔: {v19_files}"
