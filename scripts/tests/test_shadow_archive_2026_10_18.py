#!/usr/bin/env python3
"""2026-10-18 影子／對照線歸檔的結構測試（不打網路、不跑任何更新腳本）。

守三件事：
  1. 六個已產出的歸檔頁頂端有歸檔橫幅，且文字等於 scripts/archive_banner.py 的 ARCHIVE_TEXT；
     產生腳本裡也接了橫幅（以後手動重產不會消失）。
  2. 實單頁（_body.html）與對照線頁（cap15.html）不連到已歸檔的影子頁，唯一的例外是實單頁那一行
     「上線前的影子紀錄：不借錢版、債金版」。
  3. 系統主控台 /long-track/ 分三區：實單主系統／還在測的／歸檔（14 條，預設收起）。
2026-10-19 追加：SMH 槓桿疊加（/long-track-smh/leverage/）歸檔，排程與寫檔路徑拿掉，舊 STX50／E3 週更排程停用。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import archive_banner as ab  # noqa: E402

DOCS = ROOT / "docs"
W52 = DOCS / "long-track-w52-adaptive"

GEN_SCRIPT = {
    "leverage": "update_long_track_w52_adaptive_leverage.py",
    "c1": "update_long_track_w52_adaptive_c1.py",
    "noma": "update_long_track_w52_adaptive_noma.py",
    "tw_semivol": "update_long_track_w52_adaptive_tw_semivol.py",
    "gld": "update_long_track_gld.py",
    "turtle": "update_turtle_sleeve.py",
    "smh_leverage": "update_leverage_overlay.py",
}


def test_banner_in_every_archived_page_and_matches_text():
    for key, rel in ab.PAGES.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert text.count(ab.START) == 1 and text.count(ab.END) == 1, rel
        a, b = text.index(ab.START), text.index(ab.END)
        block = text[a:b]
        assert ab.ARCHIVE_LABEL in block, rel
        assert ab.ARCHIVE_TEXT[key] in block, rel
        # 橫幅在全站導覽之後、頁首之前（<body> 之後第一個頁面內容）
        assert text.index("<body") < a < text.index('class="page-hdr"'), rel


def test_apply_is_idempotent():
    for key, rel in ab.PAGES.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert ab.apply_to_html(text, key) == text, rel


def test_generators_wire_the_banner():
    for key, fn in GEN_SCRIPT.items():
        src = (ROOT / "scripts" / fn).read_text(encoding="utf-8")
        assert "archive_banner" in src, fn
        assert (f'archive_banner("{key}")' in src) or (f"archive_banner('{key}')" in src), fn


def test_f70_page_uses_retired_banner_and_status():
    sys.path.insert(0, str(DOCS / "backtest"))
    import _page_meta as pm  # noqa: E402
    assert pm.PAGES["/backtest/f_comfort/"]["status"] == "ret"
    assert "已歸檔・2026-10-18 停止更新" in pm.RET_BANNER["/backtest/f_comfort/"]
    assert ab.ARCHIVE_TEXT["f70"] in pm.RET_BANNER["/backtest/f_comfort/"]
    html = (DOCS / "backtest" / "f_comfort" / "index.html").read_text(encoding="utf-8")
    assert "bt-banner-ret" in html and "已歸檔・2026-10-18 停止更新" in html


FORBIDDEN = ("noma.html", "tw-semivol.html", "long-track-gld", "turtle-sleeve", "f_comfort")
ALLOWED_SHADOW_LINKS = ("/long-track-w52-adaptive/leverage.html", "/long-track-w52-adaptive/c1-shadow.html")


def _hrefs(path: Path) -> list[str]:
    return re.findall(r'href="([^"]+)"', path.read_text(encoding="utf-8"))


def test_live_and_cap15_pages_do_not_link_archived_pages():
    for name in ("_body.html", "cap15.html"):
        hrefs = _hrefs(W52 / name)
        for h in hrefs:
            assert not any(f in h for f in FORBIDDEN), (name, h)
    live = _hrefs(W52 / "_body.html")
    # 實單頁只留「上線前的影子紀錄：不借錢版、債金版」這一行（兩個連結）
    for h in ALLOWED_SHADOW_LINKS:
        assert h in live
    assert "上線前的影子紀錄" in (W52 / "_body.html").read_text(encoding="utf-8")
    assert not any(h in _hrefs(W52 / "cap15.html") for h in ALLOWED_SHADOW_LINKS)


def test_console_has_three_zones_and_archive_is_collapsed():
    html = (DOCS / "long-track" / "index.html").read_text(encoding="utf-8")
    assert '<div class="grp-h">實單主系統</div>' in html
    assert '<div class="grp-h">還在測的</div>' in html
    m = re.search(r'<details class="ov-retired" id="archive"([^>]*)><summary>歸檔（(\d+)）</summary>', html)
    assert m, "archive details missing"
    assert "open" not in m.group(1), "archive must be collapsed by default"
    assert int(m.group(2)) == 14
    for url in ("/long-track-w52-adaptive/leverage.html", "/long-track-w52-adaptive/c1-shadow.html",
                "/long-track-w52-adaptive/noma.html", "/long-track-w52-adaptive/tw-semivol.html",
                "/long-track-gld/", "/turtle-sleeve/", "/backtest/f_comfort/",
                "/long-track-smh/", "/long-track-smh/leverage/", "/long-track-tw/", "/long-track-tw-vt/",
                "/long-track-adaptive-vt/", "/long-track-qs-vt/", "/backtest/six_state/status/"):
        assert f'<a class="arch-row" href="{url}">' in html, url
    # 還在測的兩列
    assert "2026-10-19 起累積中" in html and "NFCI 紅燈時持股減半" in html
    # 舊的影子對照表與前瞻候選區已不存在
    assert "影子對照（跟實盤同一套引擎" not in html
    assert "前瞻 OOS 候選" not in html.split('id="panel-overview"')[1].split('id="panel-live"')[0]


def test_workflows_no_longer_run_archived_lines():
    wf = ROOT / ".github" / "workflows"
    main = (wf / "update_long_track_w52_adaptive.yml").read_text(encoding="utf-8")
    for s in ("update_long_track_w52_adaptive_leverage.py", "update_long_track_w52_adaptive_noma.py",
              "update_long_track_w52_adaptive_tw_semivol.py", "update_long_track_w52_adaptive_c1.py",
              "build_f70_alert.py"):
        assert f"run: python scripts/{s}" not in main, s
    # 實單與對照線兩個 step 還在
    assert "python scripts/update_long_track_w52_adaptive.py\n" in main
    assert "python scripts/update_long_track_w52_adaptive.py --profile cap15" in main
    for gone in ("update_long_track_gld.yml", "update_turtle_sleeve.yml", "f70-test-mail.yml"):
        assert not (wf / gone).exists(), gone
    us_close = (wf / "daily-us-close.yml").read_text(encoding="utf-8")
    assert "run: python scripts/update_turtle_sleeve.py" not in us_close
    assert "docs/turtle-sleeve/" not in us_close.split("PATHS=")[1]
    assert "run: python scripts/update_turtle_sleeve.py" not in (wf / "us-close-stale-recheck.yml").read_text(encoding="utf-8")
    # 2026-10-19：SMH 槓桿疊加不再由收盤帶與隔日重查帶寫入
    assert "run: python scripts/update_leverage_overlay.py" not in us_close
    assert "docs/long-track-smh/leverage/" not in us_close.split("PATHS=")[1]
    recheck = (wf / "us-close-stale-recheck.yml").read_text(encoding="utf-8")
    assert "run: python scripts/update_leverage_overlay.py" not in recheck
    assert "docs/long-track-smh/leverage/" not in recheck.split("PATHS=")[1]


def test_old_stx50_e3_workflows_have_no_schedule_but_keep_manual_dispatch():
    wf = ROOT / ".github" / "workflows"
    for fn in ("update_long_track_smh.yml", "update_long_track_tw.yml"):
        text = (wf / fn).read_text(encoding="utf-8")
        on_block = text.split("\non:\n")[1].split("\npermissions:")[0]
        live = [ln for ln in on_block.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        assert not any(ln.strip().startswith("schedule:") for ln in live), fn
        assert any(ln.strip().startswith("workflow_dispatch:") for ln in live), fn
