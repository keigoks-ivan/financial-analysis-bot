#!/usr/bin/env python3
"""2026-10-19 選股區停更與歸檔的結構測試（不打網路、不跑任何更新腳本）。

守五件事：
  1. QGM（/qgm/、/qgm-tw/）：封存目錄只留最近 30 個日期、archive/index.html 沒有死連結、latest.html 頁頂有說明；
     選股席位讀的 latest.json 照常在。
  2. 美股技術結構只留階段雷達：screener.html、rs-turn/、screeners.html 是轉址頁（meta refresh＋location.replace＋noindex＋連結）；
     產生資料的程式與排程照跑；站內其他連結改指 /stages/。
  3. Quality-Entry、Tier Matrix、衛星·循環軌三頁頂端有歸檔橫幅，產生程式也接了橫幅；
     Quality-Entry 的排程步驟與 DD 發布觸發拿掉，快照搬出網站；循環軌預設不再重寫頁面，但資料（JSON）照常產生。
  4. DD 管線沒被弄壞：dd2/run.py 還在 import build_quality_entry.ma_state_label_and_score。
  5. 長線歸檔頁（archive_banner.PAGES）原本的橫幅與文字沒被動到。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
DOCS = ROOT / "docs"
WF = ROOT / ".github" / "workflows"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import archive_banner as ab  # noqa: E402


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ───────────────────────── 1. QGM ─────────────────────────

def _archive_days(d: Path) -> set[str]:
    return {m.group(1) for p in d.iterdir()
            if (m := re.match(r"^(?:candidates|snapshot)_(\d{4}-\d{2}-\d{2})\.(?:html|json)$", p.name))}


def test_qgm_archives_keep_at_most_30_dates_and_index_has_no_dead_links():
    for name in ("qgm", "qgm-tw"):
        arch = DOCS / name / "archive"
        days = _archive_days(arch)
        assert 1 <= len(days) <= 30, (name, len(days))
        for day in days:  # 每個日期整對都在
            assert (arch / f"candidates_{day}.html").exists() and (arch / f"snapshot_{day}.json").exists(), (name, day)
        links = re.findall(r'<a href="(candidates_[^"]+)">', _read(arch / "index.html"))
        assert links and all((arch / f).exists() for f in links), name
        assert len(links) == len(days), name


def test_qgm_latest_json_still_present_for_seat_engine_and_page_has_note():
    notes = {
        "qgm": "本頁不再列在選單；資料仍每週更新，供選股席位的候選母體使用。",
        "qgm-tw": "本頁不再列在選單；資料仍每週更新，供 DD Screener 台股池的品質與市值資料使用。",
    }
    for name, note in notes.items():
        data = json.loads(_read(DOCS / name / "latest.json"))
        assert {"candidates", "watch_list", "quality_pool"} <= set(data), name
        html = _read(DOCS / name / "latest.html")
        assert html.count(note) == 1 and html.count("<!--qgm-note-->") == 1, name
        assert html.index("</section>") < html.index("<!--qgm-note-->") < html.index('<main class="container"'), name
        assert "已歸檔" not in html[html.index("<!--qgm-note-->"):html.index("<!--/qgm-note-->")], name
    # 席位引擎、DD Screener 讀的就是這兩個檔
    import dd_screener_quality as q
    assert q.QGM_US_PATH == DOCS / "qgm" / "latest.json" and q.QGM_TW_PATH == DOCS / "qgm-tw" / "latest.json"


# ───────────────────────── 2. 美股技術結構只留階段雷達 ─────────────────────────

# 2026-10-30：screener.html、screeners.html 持有人要求恢復為完整頁，只剩 rs-turn 維持轉址頁
RETIRED = ("rs-turn/index.html",)


def test_retired_pages_are_redirect_stubs_to_stages():
    for rel in RETIRED:
        html = _read(DOCS / rel)
        assert '<meta http-equiv="refresh" content="0; url=/stages/">' in html, rel
        assert 'location.replace("/stages/")' in html, rel
        assert '<meta name="robots" content="noindex,nofollow">' in html, rel
        assert '<a href="/stages/"' in html and "個股階段雷達" in html, rel
        assert 'rel="canonical" href="https://research.investmquest.com/stages/"' in html, rel
        # 舊頁面內容已不在（篩選表與讀資料的程式）
        assert "screener/latest.json" not in html and "rs-turn/data" not in html, rel
        assert len(html) < 12000, rel


def test_stage_radar_still_exists_and_data_generators_keep_running():
    assert (DOCS / "stages" / "index.html").exists() and (DOCS / "stages" / "tw" / "index.html").exists()
    close = _read(WF / "daily-us-close.yml")
    for step in ("python scripts/screener.py --quick", "python scripts/build_rs_turn.py", "python scripts/build_stages.py"):
        assert step in close, step
    paths = close.split("PATHS=")[1]
    for p in ("docs/screener/", "docs/rs-turn/data/", "docs/stages/data/"):
        assert p in paths, p
    asia = _read(WF / "daily-asia-close.yml")
    assert "python scripts/screener_tw.py" in asia and "python scripts/build_stages_tw.py" in asia
    # 產生程式不寫這三個 HTML（資料照寫、網頁不重寫）
    for fn in ("screener.py", "build_rs_turn.py"):
        src = _read(SCRIPTS / fn)
        assert not re.search(r"write_text\([^)]*(screener\.html|rs-turn/index\.html|screeners\.html)", src), fn
        assert not re.search(r"open\([^)]*(screener\.html|rs-turn/index\.html|screeners\.html)", src), fn


def test_site_links_to_retired_pages_now_point_to_stages():
    expect_gone = {
        "docs/stages/index.html": ('href="/rs-turn/"',),
        # 2026-10-30 三頁恢復且選單加「RS 排行」(/screeners.html)，每頁站頭都有該連結，不再檢查它
        "docs/simplicity.html": ('href="/rs-turn/"',),
        "docs/research/price-momentum/index.html": (),
        "docs/screener-jp.html": ('href="/screener.html"',),
        "docs/screener-my.html": ('href="/screener.html"',),
        "docs/assets/imq-badge.js": ('"/rs-turn/"',),
    }
    for rel, needles in expect_gone.items():
        text = _read(ROOT / rel)
        for n in needles:
            assert n not in text, (rel, n)
        assert "/stages/" in text, rel


# ───────────────────────── 3. 三頁歸檔 ─────────────────────────

SCREEN_GEN = {
    "quality_entry": "build_quality_entry.py",
    "cyclical_track": "build_cyclical_track.py",
}


def test_banner_in_each_screen_page_and_matches_text():
    assert set(ab.SCREEN_ARCHIVE) == {"quality_entry", "tier_matrix", "cyclical_track"}
    for key, spec in ab.SCREEN_ARCHIVE.items():
        text = _read(ROOT / spec["page"])
        assert text.count(ab.START) == 1 and text.count(ab.END) == 1, key
        a = text.index(ab.START)
        block = text[a: text.index(ab.END)]
        assert "已歸檔・2026-10-19 停止更新" in block, key
        assert spec["text"] in block, key
        assert f'href="{spec["link"][0]}"' in block, key
        # 橫幅在整個導覽區（含 dd-screener 次選單與下拉選單腳本）之後
        assert text.rfind("</header>", 0, a) < a, key
        assert text[:a].rstrip().endswith("</script>"), key
        assert ab.apply_to_html(text, key) == text, key  # 冪等


def test_generators_wire_the_screen_banner():
    for key, fn in SCREEN_GEN.items():
        src = _read(SCRIPTS / fn)
        assert f'archive_banner("{key}")' in src, fn
        assert "{ARCHIVE_BANNER}" in src, fn


def test_generated_pages_carry_the_banner_in_the_same_place_as_apply(tmp_path):
    """產生程式重產出來的頁面，橫幅位置跟 archive_banner.apply_to_html 一致（重跑 --apply 是空操作）。"""
    import build_cyclical_track as cyc
    import build_quality_entry as qe
    for mod, key, jpath in ((qe, "quality_entry", DOCS / "dd-screener" / "quality-entry.json"),
                            (cyc, "cyclical_track", DOCS / "dd-screener" / "cyclical-track.json")):
        out = tmp_path / f"{key}.html"
        mod.render_html(json.loads(_read(jpath)), out)
        html = _read(out)
        assert html.count(ab.START) == 1, key
        assert ab.apply_to_html(html, key) == html, key


def test_quality_entry_is_no_longer_scheduled_or_triggered():
    morning = _read(WF / "daily-taipei-morning.yml")
    assert "run: python scripts/build_quality_entry.py" not in morning
    assert "docs/dd-screener/quality-entry" not in morning.split("PATHS=")[1]
    for fn in WF.glob("*.yml"):
        assert "run: python scripts/build_quality_entry.py" not in _read(fn), fn.name
    assert "qe_script" not in _read(SCRIPTS / "update_dd_index.py")


def test_quality_entry_snapshots_left_the_site_and_page_still_there():
    assert not (DOCS / "dd-screener" / "quality-entry-snapshots").exists()
    html = _read(DOCS / "dd-screener" / "quality-entry.html")
    assert "quality-entry-snapshots" not in html and "已移出網站" in html
    assert (DOCS / "dd-screener" / "quality-entry.json").exists()


def test_dd_pipeline_still_imports_quality_entry_function():
    run = _read(SCRIPTS / "dd2" / "run.py")
    assert "import build_quality_entry" in run and "build_quality_entry.ma_state_label_and_score" in run
    import build_quality_entry as qe
    assert callable(qe.ma_state_label_and_score)


def test_cyclical_track_keeps_writing_data_but_not_the_page_by_default(tmp_path, monkeypatch):
    import build_cyclical_track as cyc
    doc = json.loads(_read(DOCS / "dd-screener" / "cyclical-track.json"))
    monkeypatch.setattr(cyc, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(cyc, "HTML_OUT", tmp_path / "cyclical-track.html")
    monkeypatch.setattr(cyc, "JSON_OUT", tmp_path / "cyclical-track.json")
    monkeypatch.setattr(cyc, "SNAPSHOT_DIR", tmp_path / "snaps")
    monkeypatch.setattr(cyc, "build_pipeline", lambda: doc)
    monkeypatch.setattr(sys, "argv", ["build_cyclical_track.py"])
    assert cyc.main() == 0
    assert (tmp_path / "cyclical-track.json").exists()
    assert any((tmp_path / "snaps").glob("*.json"))
    assert not (tmp_path / "cyclical-track.html").exists()
    monkeypatch.setattr(sys, "argv", ["build_cyclical_track.py", "--write-html"])
    assert cyc.main() == 0
    assert ab.START in _read(tmp_path / "cyclical-track.html")


def test_cyclical_track_data_consumers_and_weekly_job_untouched():
    weekly = _read(WF / "weekly-fundamental-refresh.yml")
    assert "run: python scripts/build_cyclical_track.py" in weekly
    assert "docs/dd-screener/cyclical-track.json" in weekly
    assert "cyclical-track.json" in _read(SCRIPTS / "build_pipeline_page.py")  # 漏斗總覽頁的循環軌區塊還在讀
    assert "cyclical-track.json" in _read(ROOT / ".claude" / "skills" / "portfolio-manager" / "SKILL.md")  # 席位對照還在讀
    assert "cyclical-track.json" not in _read(DOCS / "cockpit" / "index.html")  # 2026-10-20 等待池位置閘已拿掉


def test_tier_matrix_card_and_inject_are_archived(capsys):
    idx = _read(DOCS / "id" / "index.html")
    assert "Tier Matrix：已歸檔（2026-10-19 停止更新）" in idx
    assert "Tier Matrix 健康度" not in idx
    import check_tier_matrix as ctm
    assert ctm.inject_html_alert() == 0
    assert "已於 2026-10-19 歸檔" in capsys.readouterr().out
    assert _read(DOCS / "id" / "index.html") == idx


# ───────────────────────── 5. 長線歸檔頁沒被動到 ─────────────────────────

def test_long_track_archive_banners_unchanged():
    assert ab.ARCHIVE_DATE == "2026-10-18" and ab.ARCHIVE_LABEL == "已歸檔・2026-10-18 停止更新"
    assert len(ab.PAGES) == 7 and set(ab.PAGES).isdisjoint(ab.SCREEN_ARCHIVE)
    for key, rel in ab.PAGES.items():
        text = _read(ROOT / rel)
        assert ab.apply_to_html(text, key) == text, rel
        assert 'href="/long-track/#archive"' in text[text.index(ab.START): text.index(ab.END)], rel
