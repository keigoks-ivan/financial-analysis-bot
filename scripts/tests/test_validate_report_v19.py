#!/usr/bin/env python3
"""測試 `scripts/validate_report_v19.py`：v19 完整版的結構與內容驗收
（WP-H2-3，2026-09-11，取代 v19 產物的 70KB 整檔 floor）。

正向一條（六問齊、三視角齊、行動條件齊、必要表格有資料列、數字在白名單），
負向逐項各一條：**空表／佔位段／缺一問／缺一個視角／缺一條行動條件／lead 過長／
條列沒有 fact id**。負向測試用手組的最小頁面（不是把 fixture 挖洞），這樣每條
FAIL 的成因只有一個，讀測試就知道閘在擋什麼。

Python 3.9 相容。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import validate_report_v19 as vr  # noqa: E402

SIX = ["s4", "s5", "s6", "s9", "s10", "s12"]
OTHER = ["s1", "s2", "s3", "s7", "s8", "s11", "decision"]

H_TABLE = ("<table>\n<tr><th>#</th><th>核心假設</th></tr>\n"
           "<tr><td>H1</td><td>訂單延續到 2028</td></tr>\n</table>")
STREE = ('<table id="stree">\n<tr><th>情境</th><th>機率</th></tr>\n'
         "<tr><td>基本</td><td>45%</td></tr>\n</table>")
TRIGGERS = ('<table id="triggers">\n<tr><th>#</th><th>觸發器</th></tr>\n'
            "<tr><td>1</td><td>同店訂單季減</td></tr>\n</table>")
REVLOG = ('<section id="revlog">\n<h2>版本紀錄</h2>\n<table>\n'
          "<tr><th>日期</th><th>裁決</th></tr>\n<tr><td>2026-09-11</td><td>觀望</td></tr>\n"
          "</table>\n</section>")

VIEW_BULLETS = "\n".join(
    "<li><strong>{0}</strong>：這一條寫了實質內容與依據（f_kpi0_gaap）。</li>".format(v)
    for v in vr.THREE_VIEWS)
ACTION_BULLETS = "\n".join(
    "<li><strong>{0}</strong>：條件與動作各寫一句（f_kpi0_gaap）。</li>".format(a)
    for a in vr.ACTION_CONDITIONS)


def _section(sid, lead="這一段的結論寫成一句話", bullets=None, extra=""):
    bullets = bullets if bullets is not None else [
        "第一條理由，帶事實 id（f_kpi0_gaap）。",
        "第二條理由，另一件事（f_price_at_dd）。",
    ]
    ul = ('<ul class="pts">\n' + "\n".join("<li>{0}</li>".format(b) for b in bullets) + "\n</ul>"
          if bullets else "")
    return ('<section id="{0}">\n<h2>{0}</h2>\n<p class="lead">{1}</p>\n{2}\n{3}\n</section>'
            .format(sid, lead, ul, extra))


def _page(overrides=None, drop=()):
    """組一份最小但合格的 v19 頁面；`overrides` 逐 sid 換掉整段，`drop` 整段拿掉。"""
    overrides = overrides or {}
    parts = []
    for sid in OTHER + SIX:
        if sid in drop:
            continue
        if sid in overrides:
            parts.append(overrides[sid])
            continue
        if sid == "s2":
            parts.append(_section(sid, extra=H_TABLE))
        elif sid == "s10":
            parts.append(_section(sid, extra=STREE))
        elif sid == "s12":
            parts.append(_section(sid, bullets=[
                "第一條理由（f_kpi0_gaap）。", "第二條理由（f_price_at_dd）。"],
                extra="") .replace("</ul>", "\n".join(["</ul>", '<ul class="pts">',
                                                       VIEW_BULLETS, "</ul>"])))
        elif sid == "decision":
            parts.append('<section id="decision">\n<h2>13</h2>\n'
                         '<p class="lead">觀望，等價格</p>\n'
                         '<ul class="pts">\n' + ACTION_BULLETS + "\n</ul>\n" + TRIGGERS + "\n</section>")
        else:
            parts.append(_section(sid))
    parts.append(REVLOG)
    return ('<meta name="dd-layout" content="v19">\n' + "\n".join(parts) + "\n")


def _run(html, tmp_path, name="r.html"):
    p = tmp_path / name
    p.write_text(html, encoding="utf-8")
    return vr.validate(p)


def test_complete_page_passes(tmp_path):
    ok, findings = _run(_page(), tmp_path)
    assert ok, findings


def test_missing_one_question_fails(tmp_path):
    ok, findings = _run(_page(drop=("s6",)), tmp_path)
    assert not ok
    assert any(sid == "s6" and "整段不存在" in r for sid, r in findings)


def test_placeholder_section_fails(tmp_path):
    ok, findings = _run(_page(overrides={
        "s5": '<section id="s5">\n<h2>5</h2>\n<p>（略）</p>\n</section>'}), tmp_path)
    assert not ok
    assert any(sid == "s5" and "佔位" in r for sid, r in findings)


def test_empty_required_table_fails(tmp_path):
    """空表＝只有表頭。標題在、表在，但一列資料都沒有，不算過。"""
    empty = '<table id="triggers">\n<tr><th>#</th><th>觸發器</th></tr>\n</table>'
    page = _page().replace(TRIGGERS, empty)
    ok, findings = _run(page, tmp_path)
    assert not ok
    assert any("空表" in r and "觸發器" in r for _sid, r in findings)


def test_table_of_only_placeholder_cells_fails(tmp_path):
    dashes = ('<table id="stree">\n<tr><th>情境</th><th>機率</th></tr>\n'
              "<tr><td>—</td><td>TODO</td></tr>\n</table>")
    ok, findings = _run(_page().replace(STREE, dashes), tmp_path)
    assert not ok
    assert any("空表" in r and "情境樹" in r for _sid, r in findings)


def test_missing_one_view_fails(tmp_path):
    page = _page().replace(
        "<li><strong>{0}</strong>：這一條寫了實質內容與依據（f_kpi0_gaap）。</li>".format(
            vr.THREE_VIEWS[1]), "")
    ok, findings = _run(page, tmp_path)
    assert not ok
    assert any(sid == "s12" and vr.THREE_VIEWS[1] in r for sid, r in findings)


def test_view_with_no_content_fails(tmp_path):
    page = _page().replace(
        "<li><strong>{0}</strong>：這一條寫了實質內容與依據（f_kpi0_gaap）。</li>".format(
            vr.THREE_VIEWS[2]),
        "<li><strong>{0}</strong>：TODO</li>".format(vr.THREE_VIEWS[2]))
    ok, findings = _run(page, tmp_path)
    assert not ok
    assert any(sid == "s12" and "只有標題沒有內容" in r for sid, r in findings)


def test_missing_action_condition_fails(tmp_path):
    page = _page().replace(
        "<li><strong>清倉</strong>：條件與動作各寫一句（f_kpi0_gaap）。</li>", "")
    ok, findings = _run(page, tmp_path)
    assert not ok
    assert any(sid == "decision" and "清倉" in r for sid, r in findings)


def test_lead_too_long_fails(tmp_path):
    long_lead = "這" * (vr.LEAD_MAX_CHARS + 1)
    ok, findings = _run(_page(overrides={"s9": _section("s9", lead=long_lead, extra="")}), tmp_path)
    assert not ok
    assert any(sid == "s9" and "lead" in r and "字 >" in r for sid, r in findings)


def test_bullets_without_fact_id_fail(tmp_path):
    ok, findings = _run(_page(overrides={"s4": _section("s4", bullets=[
        "第一條理由，沒有引事實。", "第二條理由，也沒有引。"])}), tmp_path)
    assert not ok
    assert any(sid == "s4" and "fact id" in r for sid, r in findings)


def test_number_outside_whitelist_fails(tmp_path, tmp_path_factory):
    judgment = tmp_path / "j.json"
    judgment.write_text('{"decision_out": {"verdict": "觀望"}, "x": 45}', encoding="utf-8")
    page = _page(overrides={"s6": _section("s6", bullets=[
        "成長 45%，在白名單內（f_kpi0_gaap）。",
        "成長 99.7%，不在白名單（f_price_at_dd）。"])})
    p = tmp_path / "r.html"
    p.write_text(page, encoding="utf-8")
    ok, findings = vr.validate(p, judgment_path=judgment)
    assert not ok
    assert any(sid == "s6" and "不在白名單" in r for sid, r in findings)


def test_mechanical_sections_are_not_placeholder_checked(tmp_path):
    """revlog／appA 這類機械段的內容就是一張表——不能因為「扣掉表格後是空的」
    被誤判成空段。"""
    ok, _ = _run(_page(), tmp_path)
    assert ok


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
