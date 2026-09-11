#!/usr/bin/env python3
"""測試 `scripts/render_dd.py` 的 v19 版面組裝（`--assemble --layout v19`，
WP-H2-2，2026-09-11）：`assemble_from_parts_v19()` 讀 PROSE_DIR（s1..s12/
decision，13 段）＋TABLES_DIR（`gen_dd_tables.py` 既有與 v19 片段）組出完整
v19.html/v19.css 版面；canonical section id 與舊版面共用；免費資料折疊區在
注入層包 `<details>`；舊版面（`--layout legacy`，預設）完全不受影響。

驗收依據：`notes/site-internal/dd/_v19_layout_spec_20260911.md`。用 v19
fixture 三件（judgment/facts/scenario_meta）＋ `dd_project.py prose-stub`
產出的散文佔位，端到端組出一頁，逐區塊核對規格要求的結構（不驗散文品質
——那是 H2 散文 prompt 之後真跑才驗的東西，見 prose.md.tmpl 開頭）。

Python 3.9 相容（`from __future__ import annotations`）。
"""
from __future__ import annotations

import html.parser
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

sys.path.insert(0, str(SCRIPTS_DIR))
import render_dd  # noqa: E402

V19_JUDGMENT = FIXTURES / "judgment_v19_FIX.json"
V19_FACTS = FIXTURES / "facts_FIX_20260911.json"
V19_SCENARIO_META = FIXTURES / "scenario_meta_FIX_20260911.json"


def _run(args):
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    return r


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    """gen_dd_tables.py + dd_project.py prose-stub 產出一組完整 TABLES_DIR /
    PROSE_DIR，供本檔多個測試共用（module scope，只組一次）。"""
    base = tmp_path_factory.mktemp("v19build")
    tables = base / "tables"
    prose = base / "prose"
    _run([str(SCRIPTS_DIR / "gen_dd_tables.py"), str(V19_JUDGMENT),
          "--out", str(tables), "--scenario-meta", str(V19_SCENARIO_META)])
    _run([str(SCRIPTS_DIR / "dd_project.py"), "prose-stub", str(V19_JUDGMENT),
          "--out", str(prose), "--facts", str(V19_FACTS)])
    return tables, prose


@pytest.fixture(scope="module")
def assembled_html(built):
    tables, prose = built
    return render_dd.assemble_from_parts_v19(
        prose, tables, judgment_path=V19_JUDGMENT,
    )


# ---------------------------------------------------------------------------
# 結構驗收：canonical id、無殘留標記、合法 HTML
# ---------------------------------------------------------------------------

def test_all_canonical_ids_present(assembled_html):
    for cid in ("s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11",
                "s12", "decision", "s14", "appA", "appB", "appC", "revlog", "dd-meta"):
        assert f'id="{cid}"' in assembled_html, f"missing id={cid}"


def test_no_leftover_v19_tokens(assembled_html):
    assert "V19:" not in assembled_html


def test_parses_as_valid_html(assembled_html):
    errors = []

    class _P(html.parser.HTMLParser):
        def error(self, message):
            errors.append(message)

    _P().feed(assembled_html)
    assert errors == []


def test_single_header_no_nesting(assembled_html):
    """v19-dashboard.html 自帶 <header>，模板不得再包一層（曾經巢狀過一次）。"""
    assert assembled_html.count("<header") == 1
    assert assembled_html.count("</header>") == 1


def test_head_carries_schema_and_title(assembled_html):
    assert 'name="dd-schema-version" content="v15.2"' in assembled_html
    assert "<title>" in assembled_html and "</title>" in assembled_html
    assert 'name="dd-render" content="render_dd-v15.2"' in assembled_html
    assert 'name="dd-layout" content="v19"' in assembled_html


def test_footer_and_printbtn_present(assembled_html):
    assert "本報告由 stock-analyst" in assembled_html
    assert 'class="printbtn"' in assembled_html


# ---------------------------------------------------------------------------
# 頁首儀表板：五張卡／24 格／改變主意
# ---------------------------------------------------------------------------

def test_dashboard_five_cards_and_grid_and_changemind(assembled_html):
    assert "裁決" in assembled_html and "觀望" in assembled_html
    assert assembled_html.count('<div class="k">') == 24
    assert "什麼會讓我改變主意" in assembled_html


# ---------------------------------------------------------------------------
# 側欄目錄：present 集合對應實際輸出的段落
# ---------------------------------------------------------------------------

def test_toc_lists_all_present_sections(assembled_html):
    for cid, label in render_dd.V19_TOC_LABELS.items():
        assert f'href="#{cid}"' in assembled_html, f"toc missing link to {cid}"
        assert label in assembled_html


def test_toc_is_a_collapsible_details(assembled_html):
    assert '<details class="toc" open>' in assembled_html
    assert "<summary>目錄</summary>" in assembled_html


# ---------------------------------------------------------------------------
# 免費資料折疊區：折疊的有 <details>，常駐的（E2/AUDIT）沒有二次包裝
# ---------------------------------------------------------------------------

def test_s3_market_table_is_folded(assembled_html):
    i = assembled_html.find('id="s3"')
    j = assembled_html.find('id="s4"')
    window = assembled_html[i:j]
    assert "<details>" in window
    assert "市場空間與利潤池流向" in window
    assert 'id="e3"' in window


def test_s2_h1_h3_table_not_folded(assembled_html):
    """規格：§2 的 H1-H3 表是常駐內容，不折疊。"""
    i = assembled_html.find('id="s2"')
    j = assembled_html.find('id="s3"')
    window = assembled_html[i:j]
    assert "<table>" in window  # e2.html 本身無 id，是裸 <table>
    # 不應該被包進這段自己新增的 <details>（判斷本段沒有 <summary> 緊貼在
    # e2 表格前）
    assert "<summary>市場空間" not in window


def test_decision_has_two_separate_folded_blocks(assembled_html):
    i = assembled_html.find('id="decision"')
    j = assembled_html.find('id="s14"')
    window = assembled_html[i:j]
    assert 'class="audit"' in window  # audit.html 自帶外層，不二次包裝
    assert "監測與觸發器、致命指標、催化劑" in window
    assert 'id="triggers"' in window
    assert 'id="kill"' in window
    assert 'id="catalysts"' in window
    # audit 的 <details class="audit"> 不應該又被包進第二層 <details><summary>
    assert window.count("<details") >= 2


def test_appA_appB_appC_all_present_in_order(assembled_html):
    i_a = assembled_html.find('id="appA"')
    i_b = assembled_html.find('id="appB"')
    i_c = assembled_html.find('id="appC"')
    i_rev = assembled_html.find('id="revlog"')
    assert i_a < i_b < i_c < i_rev


# ---------------------------------------------------------------------------
# 缺檔行為：ValueError with actionable message
# ---------------------------------------------------------------------------

def test_missing_prose_section_raises(built, tmp_path):
    tables, prose = built
    broken_prose = tmp_path / "broken_prose"
    broken_prose.mkdir()
    for p in sorted(prose.glob("*.html"))[:-1]:  # 缺最後一個 section
        (broken_prose / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="PROSE_DIR 缺少必要段落"):
        render_dd.assemble_from_parts_v19(broken_prose, tables)


def test_missing_required_table_raises(built, tmp_path):
    tables, prose = built
    broken_tables = tmp_path / "broken_tables"
    broken_tables.mkdir()
    for p in tables.glob("*.html"):
        if p.name == "v19-appA.html":
            continue
        (broken_tables / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="TABLES_DIR 缺少必要檔案"):
        render_dd.assemble_from_parts_v19(prose, broken_tables)


# ---------------------------------------------------------------------------
# _v19_gather：折疊包裝、多檔合併、缺檔靜默略過
# ---------------------------------------------------------------------------

def test_v19_gather_folds_with_label(tmp_path):
    (tmp_path / "a.html").write_text("<table>x</table>", encoding="utf-8")
    spec = {"marker": "<!-- X -->", "files": ["a.html"], "folded": True, "label": "測試折疊"}
    out = render_dd._v19_gather(tmp_path, spec)
    assert out.startswith("<details><summary>測試折疊</summary>")
    assert "<table>x</table>" in out


def test_v19_gather_not_folded_when_folded_false(tmp_path):
    (tmp_path / "a.html").write_text("<table>x</table>", encoding="utf-8")
    spec = {"marker": "<!-- X -->", "files": ["a.html"], "folded": False}
    out = render_dd._v19_gather(tmp_path, spec)
    assert out == "<table>x</table>"


def test_v19_gather_merges_multiple_files(tmp_path):
    (tmp_path / "a.html").write_text("<p>A</p>", encoding="utf-8")
    (tmp_path / "b.html").write_text("<p>B</p>", encoding="utf-8")
    spec = {"marker": "<!-- X -->", "files": ["a.html", "b.html"], "folded": False}
    out = render_dd._v19_gather(tmp_path, spec)
    assert "<p>A</p>" in out and "<p>B</p>" in out


def test_v19_gather_returns_none_when_all_files_missing(tmp_path):
    spec = {"marker": "<!-- X -->", "files": ["missing.html"], "folded": True, "label": "x"}
    assert render_dd._v19_gather(tmp_path, spec) is None


def test_v19_gather_skips_missing_but_keeps_present(tmp_path):
    (tmp_path / "a.html").write_text("<p>A</p>", encoding="utf-8")
    spec = {"marker": "<!-- X -->", "files": ["missing.html", "a.html"], "folded": False}
    out = render_dd._v19_gather(tmp_path, spec)
    assert out == "<p>A</p>"


# ---------------------------------------------------------------------------
# CLI：--layout v19 與 --layout legacy（預設）
# ---------------------------------------------------------------------------

def test_cli_layout_v19_writes_file(built, tmp_path):
    tables, prose = built
    out = tmp_path / "FIX_v19_cli.html"
    _run([str(SCRIPTS_DIR / "render_dd.py"), "--assemble", str(prose), "--tables", str(tables),
          "--layout", "v19", "--judgment", str(V19_JUDGMENT), "-o", str(out), "--no-postprocess"])
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert 'id="decision"' in text
    assert 'name="dd-layout" content="v19"' in text


def test_cli_layout_invalid_rejected(built, tmp_path):
    tables, prose = built
    out = tmp_path / "bad.html"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "render_dd.py"), "--assemble", str(prose),
         "--tables", str(tables), "--layout", "nope", "-o", str(out)],
        capture_output=True, text=True,
    )
    assert r.returncode != 0


def test_cli_default_layout_is_legacy_and_unaffected(tmp_path):
    """--layout 不給時走 assemble_from_parts()（舊版面），和 WP-H1 既有測試
    （test_dd_project_v19.py::test_prose_stub_and_full_assembly）用的是同一條
    路徑——這裡只驗證『不給 --layout』時 CLI 不會誤走 v19 分支（dd-layout
    meta 不應出現）。"""
    tables = tmp_path / "tables"
    prose = tmp_path / "prose"
    _run([str(SCRIPTS_DIR / "gen_dd_tables.py"), str(V19_JUDGMENT),
          "--out", str(tables), "--scenario-meta", str(V19_SCENARIO_META)])
    _run([str(SCRIPTS_DIR / "dd_project.py"), "prose-stub", str(V19_JUDGMENT),
          "--out", str(prose), "--facts", str(V19_FACTS)])
    import gen_dd_tables as gdt
    import dd_project
    raw = json.loads(V19_JUDGMENT.read_text(encoding="utf-8"))
    view = dd_project.view_for(raw, V19_JUDGMENT)
    scenario_meta = json.loads(V19_SCENARIO_META.read_text(encoding="utf-8"))
    prior = None
    gdt.write_mechanical_prose(view, prior, prose, scenario_meta)
    out = tmp_path / "legacy.html"
    _run([str(SCRIPTS_DIR / "render_dd.py"), "--assemble", str(prose), "--tables", str(tables),
          "--judgment", str(V19_JUDGMENT), "-o", str(out), "--no-postprocess"])
    text = out.read_text(encoding="utf-8")
    assert 'name="dd-layout"' not in text
    assert 'class="dd-toc"' in text  # 舊版面的頂部 toc，v19 不會有這個 class
