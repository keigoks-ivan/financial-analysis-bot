#!/usr/bin/env python3
"""測試 `scripts/dd2/clue_backfill.py`（Stage 0 線索補原文，零 LLM）。

離線：fixture 放 scripts/tests/fixtures/clue_backfill/（UTF-8／Big5 新聞頁、最小 PDF），
HTTP 層用本機 http.server 模擬（轉址、Big5 標頭／meta／無宣告、PDF、404），不碰外網。
涵蓋：全形半形與千分位比對、數字邊界、命中門檻（≥2 且 ≥ 一半、弱詞不算）、窗大小、
HTML 去 script／style／nav、發布日解析、各種編碼、PDF、快取、
backfill 的命中／未命中／重複／超額／頁面日期覆蓋／備份／冪等，
以及升級後的 axis 能通過 validate_evidence.check_axis 與 `--part` CLI。

Python 3.9 相容（不用 `match`、不用 `X | None`）。
"""
import http.server
import json
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
FIX = Path(__file__).resolve().parent / "fixtures" / "clue_backfill"

sys.path.insert(0, str(SCRIPTS_DIR / "dd2"))
sys.path.insert(0, str(SCRIPTS_DIR))
import clue_backfill as cb  # noqa: E402
import validate_evidence  # noqa: E402


def _page_text(name="news_utf8.html"):
    text, _ = cb.html_to_text(cb.decode_body((FIX / name).read_bytes()))
    return text


# ---------------------------------------------------------------------------
# 比對
# ---------------------------------------------------------------------------

def test_fullwidth_and_thousands_match():
    text = _page_text()
    # 頁面是「1,000 萬元」「７.5％」「３９．５％」（全形），term 用半形無逗號
    w = cb.find_window(text, ["1000萬元", "罰鍰"])
    assert w and set(w["hits"]) == {"1000萬元", "罰鍰"}
    w = cb.find_window(text, ["39.5%", "毛利率"])
    assert w and "39.5%" in w["hits"]
    w = cb.find_window(text, ["7.5%", "申報門檻"])
    assert w and "7.5%" in w["hits"]
    # 反方向：term 用千分位全形、頁面半形
    w = cb.find_window(text, ["１，０００萬元", "罰鍰"])
    assert w and len(w["hits"]) == 2


def test_number_boundaries_exact():
    # 39 不能命中 139 或 3.9；年份 2025 不能命中 12025
    assert cb.find_window("成長139%，營收創高，毛利率提升", ["39%", "營收創高"]) is None
    assert cb.find_window("成長3.9%，營收創高，毛利率提升", ["9%", "營收創高"]) is None  # 「9%」前面是小數點
    assert cb.find_window("成長39.5%，營收創高", ["39%", "營收創高"]) is None  # 39% 不是 39.5% 的前綴
    assert cb.find_window("成長39%，營收創高", ["39%", "營收創高"]) is not None
    assert cb.find_window("股數12,345,678股，持股比例上升", ["345", "持股比例"]) is None


def test_hit_threshold_half_and_at_least_two():
    text = "甲客戶占營收39%。" + "無關。" * 30 + "其他內容。"
    # 3 個詞只中 1 個 → 不升級
    assert cb.find_window(text, ["甲客戶", "不存在詞A", "不存在詞B"]) is None
    # 3 個詞中 2 個 → 升級
    assert cb.find_window(text, ["甲客戶", "39%", "不存在詞B"]) is not None
    # 4 個詞中 2 個（剛好一半）→ 升級
    assert cb.find_window(text, ["甲客戶", "39%", "不存在詞B", "不存在詞C"]) is not None
    # 5 個詞中 2 個（不到一半）→ 不升級
    assert cb.find_window(text, ["甲客戶", "39%", "詞B", "詞C", "詞D"]) is None
    # 只給 1 個詞 → 不升級
    assert cb.find_window(text, ["甲客戶"]) is None


def test_weak_terms_do_not_count():
    text = "2026年公平會審議乙案。"
    # 年份、1～2 位裸數字是弱詞：去掉後只剩 1 個詞 → 不升級
    assert cb.find_window(text, ["2026", "公平會"]) is None
    assert cb.find_window(text, ["2026", "9", "公平會"]) is None
    assert cb.find_window(text, ["公平會", "審議"]) is not None


def test_terms_must_cooccur_within_window():
    far = "投審會裁罰甲公司。" + "無關的句子。" * 100 + "罰款一千萬元。"
    assert cb.find_window(far, ["投審會", "一千萬元"]) is None
    near = "投審會裁罰甲公司。" + "無關的句子。" * 5 + "罰款一千萬元。"
    assert cb.find_window(near, ["投審會", "一千萬元"]) is not None


def test_excerpt_is_verbatim_and_contains_hits():
    text = _page_text()
    w = cb.find_window(text, ["投審會", "1,000 萬元", "罰鍰"])
    ex = cb.make_excerpt(text, w["start"], w["end"])
    flat = text.replace("\n", " ")
    assert ex in flat  # 原文截取，不改寫（只有換行併成空格）
    assert "罰鍰" in ex and "1,000 萬元" in ex
    assert len(ex) <= cb.WINDOW + 20
    # 頁面導覽列／頁尾（nav、footer）與 script／style 裡的字不會被當證據
    assert "熱門：丙公司法說會" not in text and "轉載請註明" not in text
    assert "tracker" not in text and "color: red" not in text


# ---------------------------------------------------------------------------
# HTML／編碼
# ---------------------------------------------------------------------------

def test_html_to_text_strips_noise_and_reads_publish_date():
    html = ('<html><head><meta property="article:published_time" content="2026-09-30T10:00:00Z">'
            '<style>.x{}</style></head><body><script>alert("隱藏")</script><p>正文<b>一</b>段</p>'
            '<noscript>隱藏2</noscript><p>第二段</p></body></html>')
    text, date = cb.html_to_text(html)
    assert text == "正文一段\n第二段"
    assert date == "2026-09-30"


def test_html_hidden_elements_skipped():
    html = ('<body><div style="display: none"><ix:header>IPhoneMember2023 MacMember</ix:header>'
            '<div>內層隱藏</div></div><p>可見正文</p><span hidden>屬性隱藏</span><p>結尾</p></body>')
    text, _ = cb.html_to_text(html)
    assert text == "可見正文\n結尾"


def test_html_unclosed_nav_falls_back_to_full_text():
    html = "<html><body><nav>目錄" + "<p>這是正文內容，沒有閉合 nav 標籤。</p>" * 5 + "</body></html>"
    text, _ = cb.html_to_text(html)
    assert "這是正文內容" in text


def test_page_date_rules():
    assert cb._parse_page_date("2026-10-14T08:30:00+08:00") == "2026-10-14"
    assert cb._parse_page_date("2026年10月14日 08:30") == "2026-10-14"
    assert cb._parse_page_date("2026-10") is None      # 只有年月不算
    assert cb._parse_page_date("2099-01-01") is None   # 未來日期視為壞值
    html = '<script type="application/ld+json">{"datePublished": "2026-08-01T00:00:00+08:00"}</script><p>內文</p>'
    assert cb.html_to_text(html)[1] == "2026-08-01"


def test_dateline_fallback_needs_timestamp_and_meta_wins():
    assert cb.html_to_text("<h1>標題</h1><p>Jan. 20, 2023 16:40</p><p>內文</p>")[1] == "2023-01-20"
    assert cb.html_to_text("<h1>標題</h1><p>2026年10月11日 17:06 - 優分析</p>")[1] == "2026-10-11"
    assert cb.html_to_text("<h1>標題</h1><p>2025/02/03 10:55 加入</p>")[1] == "2025-02-03"
    # 內文提到的日期沒有時分，不當戳記
    assert cb.html_to_text("<h1>標題</h1><p>公司於2026年10月9日宣布啟動調查。</p>")[1] is None
    # meta 有日期就用 meta
    html = ('<meta property="article:published_time" content="2026-09-30T10:00:00Z">'
            "<h1>標題</h1><p>2025/02/03 10:55 加入</p>")
    assert cb.html_to_text(html)[1] == "2026-09-30"


def test_zero_width_chars_removed_from_text():
    text, _ = cb.html_to_text("<p>Delta\u2060 Electronics\u200b’ customers\ufeff include Nvidia</p>")
    assert text == "Delta Electronics’ customers include Nvidia"
    w = cb.find_window("Delta\u2060Electronics customers include Nvidia", ["DeltaElectronics", "Nvidia"])
    assert w and len(w["hits"]) == 2


@pytest.mark.parametrize("name", ["news_utf8.html", "news_big5.html"])
def test_decode_declared_in_meta(name):
    text = _page_text(name)
    assert "投審會昨（14）日表示" in text


def test_decode_header_and_undeclared_big5():
    raw = "甲公司營收年增３９．５％，投審會裁罰。".encode("cp950")
    assert "投審會裁罰" in cb.decode_body(raw, "big5")
    assert "投審會裁罰" in cb.decode_body(raw, "Big5-HKSCS")
    assert "投審會裁罰" in cb.decode_body(raw, None)               # 沒宣告：utf-8 失敗後退到 Big5
    assert "投審會裁罰" in cb.decode_body(raw, "iso-8859-1")       # 標頭只有預設的 latin-1：不信
    assert "投審會裁罰" in cb.decode_body("投審會裁罰".encode("utf-8"), "utf-8")
    assert "投審会" in cb.decode_body("投審会裁罰".encode("gb18030"), "gbk")


@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="沒有 pdftotext")
def test_pdf_text_and_match():
    text, err = cb._pdf_to_text((FIX / "report.pdf").read_bytes())
    assert err is None
    w = cb.find_window(text, ["Customer A", "39.5%", "net revenue"])
    assert w and len(w["hits"]) == 3


# ---------------------------------------------------------------------------
# HTTP 層（本機伺服器）
# ---------------------------------------------------------------------------

class _Handler(http.server.BaseHTTPRequestHandler):
    hits = []

    def log_message(self, *a):
        pass

    def do_GET(self):
        _Handler.hits.append(self.path)
        utf8 = (FIX / "news_utf8.html").read_bytes()
        big5 = (FIX / "news_big5.html").read_bytes()
        raw_big5 = (FIX / "news_big5.html").read_text(encoding="cp950").replace("charset=\"big5\"", "").encode("cp950")
        routes = {
            "/utf8": (200, "text/html; charset=utf-8", utf8),
            "/big5-meta": (200, "text/html", big5),
            "/big5-header": (200, "text/html; charset=big5", big5),
            "/big5-none": (200, "text/html", raw_big5),
            "/pdf": (200, "application/pdf", (FIX / "report.pdf").read_bytes()),
            "/empty": (200, "text/html", b"<html><body><script>x</script></body></html>"),
            "/shell": (200, "text/html", "<html><body><div>Loading...</div></body></html>".encode()),
        }
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/utf8")
            self.end_headers()
            return
        code, ctype, body = routes.get(self.path, (404, "text/html", b"not found"))
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


@pytest.fixture
def server(monkeypatch):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    _Handler.hits = []
    monkeypatch.setattr(cb, "_url_ok", lambda url: True)   # 本機位址正式環境會被擋
    monkeypatch.setattr(cb, "MIN_INTERVAL", 0)
    monkeypatch.setattr(cb, "MIN_CACHE_CHARS", 0)
    yield "http://127.0.0.1:{0}".format(srv.server_address[1])
    srv.shutdown()
    srv.server_close()


@pytest.mark.parametrize("path", ["/utf8", "/big5-meta", "/big5-header", "/big5-none", "/redirect"])
def test_fetch_text_encodings_and_redirect(server, path, tmp_path):
    r = cb.fetch_text(server + path, tmp_path / "cache")
    assert r["ok"], r
    assert "投審會昨（14）日表示" in r["text"]
    assert r["page_date"] == "2026-10-14"
    if path == "/redirect":
        assert r["final_url"].endswith("/utf8")


def test_fetch_text_pdf_and_failures(server, tmp_path):
    cache = tmp_path / "cache"
    if shutil.which("pdftotext"):
        r = cb.fetch_text(server + "/pdf", cache)
        assert r["ok"] and r["kind"] == "pdf" and "39.5%" in r["text"]
    r = cb.fetch_text(server + "/missing", cache)
    assert not r["ok"] and r["error"] == "HTTP 404"
    r = cb.fetch_text(server + "/empty", cache)
    assert not r["ok"]
    # 失敗的不快取；只有成功的 PDF 留一份
    assert len(list(cache.glob("*.json"))) == (1 if shutil.which("pdftotext") else 0)


def test_short_js_shell_page_not_cached(server, tmp_path, monkeypatch):
    monkeypatch.setattr(cb, "MIN_CACHE_CHARS", 150)
    cache = tmp_path / "cache"
    r = cb.fetch_text(server + "/shell", cache)
    assert r["ok"] and "Loading" in r["text"] and not list(cache.glob("*.json"))


def test_fetch_text_cache_hit_makes_no_request(server, tmp_path):
    cache = tmp_path / "cache"
    cb.fetch_text(server + "/utf8", cache)
    n = len(_Handler.hits)
    r = cb.fetch_text(server + "/utf8", cache)
    assert r["ok"] and r["cached"] and len(_Handler.hits) == n


def test_url_guard():
    assert cb._url_ok("https://money.udn.com/money/story/5612/9730124")
    for bad in ("file:///etc/passwd", "ftp://example.com/x", "http://localhost:8000/", "http://127.0.0.1/",
                "http://192.168.1.1/admin", "http://10.0.0.5/", "javascript:alert(1)", "https:///nohost"):
        assert not cb._url_ok(bad), bad
    assert cb._clean_url("money.udn.com/money/story/5612/9730124#top") == "https://money.udn.com/money/story/5612/9730124"
    assert cb._clean_url("鴻海 搜尋結果") == "鴻海 搜尋結果"  # 不像網址的不補 scheme


# ---------------------------------------------------------------------------
# backfill 主流程（fetch 注入，不上網）
# ---------------------------------------------------------------------------

def _run_dir(tmp_path, parts, axes_json=None):
    run = tmp_path / "2317.TW_20261020"
    (run / "parts").mkdir(parents=True)
    for name, obj in parts.items():
        (run / "parts" / name).write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    if axes_json is not None:
        (run / "axes.json").write_text(json.dumps(axes_json, ensure_ascii=False), encoding="utf-8")
    return run


def _fake_fetch(pages):
    calls = []

    def fetch(url):
        calls.append(url)
        p = pages.get(url)
        if p is None:
            return {"ok": False, "error": "HTTP 404", "text": ""}
        return dict({"ok": True, "text": _page_text(), "page_date": None, "final_url": url, "cached": False}, **p)
    fetch.calls = calls
    return fetch


def _clue(url="https://news.example.com/a", terms=None, **kw):
    c = {"claim": "甲公司因未申報取得乙公司股權遭罰 1,000 萬元", "url": url, "as_of": "2026-10-14",
         "direction": "-", "affects": ["decision_inputs.bear"], "source": "示範新聞",
         "match_terms": terms or ["投審會", "1,000 萬元", "罰鍰"]}
    c.update(kw)
    return c


def _axis(status="none", clues=None, findings=None, note="三次搜尋均未取得原文。"):
    return {"status": status, "queries_run": ["q1"], "findings": findings or [], "note": note,
            "clues": clues if clues is not None else []}


def test_backfill_upgrades_hit_and_discards_miss(tmp_path):
    part = {"coverage": {"regulatory_antitrust": _axis(clues=[
        _clue(),
        _clue(url="https://news.example.com/b", terms=["完全無關", "不存在的詞"]),
    ])}}
    run = _run_dir(tmp_path, {"axes_2.json": part}, [{"id": "regulatory_antitrust", "affects": ["thesis.R"]}])
    fetch = _fake_fetch({"https://news.example.com/a": {"page_date": "2026-10-14"},
                         "https://news.example.com/b": {}})
    st = cb.backfill(run, fetch=fetch)
    assert st["clues"] == 2 and st["verified"] == 1 and st["discarded"] == 1 and st["urls"] == 2
    assert st["axes_upgraded"] == ["regulatory_antitrust"]
    out = json.loads((run / "parts" / "axes_2.json").read_text(encoding="utf-8"))
    ax = out["coverage"]["regulatory_antitrust"]
    assert ax["status"] == "found" and "clues" not in ax
    assert len(ax["findings"]) == 1
    f = ax["findings"][0]
    assert f["excerpt_source"] == "program_fetch" and f["excerpt_from"] == "page"
    assert f["url"] == "https://news.example.com/a" and f["as_of"] == "2026-10-14" and "as_of_note" not in f
    assert f["direction"] == "-" and f["affects"] == ["decision_inputs.bear"] and f["source"] == "示範新聞"
    assert "罰鍰" in f["excerpt"] and "1,000 萬元" in f["excerpt"]
    assert f["excerpt"] in _page_text().replace("\n", " ")
    assert ax["note"].endswith("線索 2 條，程式核實 1 條")
    # 升級後的 axis 通過 evidence 驗證
    fails, _ = validate_evidence.check_axis("regulatory_antitrust", ax, {})
    assert fails == []
    # 原檔備份
    bak = json.loads((run / "parts" / "_pre_backfill" / "axes_2.json").read_text(encoding="utf-8"))
    assert len(bak["coverage"]["regulatory_antitrust"]["clues"]) == 2
    # 記錄檔
    log = json.loads((run / "fetch_cache" / "backfill_log.json").read_text(encoding="utf-8"))
    assert [d["outcome"] for d in log] == ["verified", "no_match"]


def test_backfill_idempotent_and_keeps_first_backup(tmp_path):
    part = {"coverage": {"x_axis": _axis(clues=[_clue()])}}
    run = _run_dir(tmp_path, {"axes_1.json": part})
    cb.backfill(run, fetch=_fake_fetch({"https://news.example.com/a": {}}))
    after_first = (run / "parts" / "axes_1.json").read_text(encoding="utf-8")
    st = cb.backfill(run, fetch=_fake_fetch({}))
    assert st["clues"] == 0
    assert (run / "parts" / "axes_1.json").read_text(encoding="utf-8") == after_first
    assert "clues" in (run / "parts" / "_pre_backfill" / "axes_1.json").read_text(encoding="utf-8")


def test_backfill_no_clues_touches_nothing(tmp_path):
    part = {"coverage": {"x_axis": {"status": "none", "queries_run": ["q"], "findings": [], "note": "n"}}}
    run = _run_dir(tmp_path, {"axes_1.json": part})
    before = (run / "parts" / "axes_1.json").read_text(encoding="utf-8")
    st = cb.backfill(run, fetch=_fake_fetch({}))
    assert st["clues"] == 0 and (run / "parts" / "axes_1.json").read_text(encoding="utf-8") == before
    assert not (run / "parts" / "_pre_backfill").exists()
    assert cb.backfill(tmp_path / "不存在的目錄")["clues"] == 0


def test_backfill_found_axis_appends_and_dedups_existing_url(tmp_path):
    existing = {"claim": "既有", "source": "s", "url": "https://news.example.com/a/", "as_of": "2026-10-01",
                "direction": "0", "affects": ["thesis.R"], "excerpt": None, "excerpt_from": "snippet"}
    part = {"coverage": {"x_axis": _axis(status="found", findings=[existing], clues=[
        _clue(url="https://News.Example.com/a#frag"),        # 同網址（大小寫、尾斜線、fragment 不同）→ 重複
        _clue(url="https://news.example.com/c"),
    ])}}
    run = _run_dir(tmp_path, {"axes_1.json": part})
    fetch = _fake_fetch({"https://news.example.com/c": {}})
    st = cb.backfill(run, fetch=fetch)
    assert st["duplicate"] == 1 and st["verified"] == 1
    assert fetch.calls == ["https://news.example.com/c"]   # 重複的不去抓
    ax = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]
    assert ax["status"] == "found" and len(ax["findings"]) == 2 and ax["findings"][0] == existing


def test_backfill_page_date_overrides_agent_date_with_note(tmp_path):
    part = {"coverage": {"x_axis": _axis(clues=[_clue(as_of="2026-04-30")])}}
    run = _run_dir(tmp_path, {"axes_1.json": part})
    cb.backfill(run, fetch=_fake_fetch({"https://news.example.com/a": {"page_date": "2026-10-14"}}))
    f = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]["findings"][0]
    assert f["as_of"] == "2026-10-14" and "2026-04-30" in f["as_of_note"]


@pytest.mark.parametrize("agent_as_of,page_date,expect_as_of,expect_note", [
    ("2026-10-14", "2026-10-14", "2026-10-14", False),      # 相同：不動
    ("2026-10", "2026-10-14", "2026-10-14", False),         # agent 只到月、頁面在該月：補全不註記
    ("2026-09", "2026-10-14", "2026-10-14", True),          # 月份不同：註記
    ("", "2026-10-14", "2026-10-14", False),                # agent 沒填：用頁面
    ("2026-10-14", None, "2026-10-14", False),              # 頁面沒日期：照 agent
])
def test_pick_as_of(agent_as_of, page_date, expect_as_of, expect_note):
    as_of, note = cb._pick_as_of(agent_as_of, page_date)
    assert as_of == expect_as_of and bool(note) == expect_note


def test_backfill_no_usable_date_is_discarded(tmp_path):
    part = {"coverage": {"x_axis": _axis(clues=[_clue(as_of="不明")])}}
    run = _run_dir(tmp_path, {"axes_1.json": part})
    st = cb.backfill(run, fetch=_fake_fetch({"https://news.example.com/a": {"page_date": None}}))
    assert st["verified"] == 0
    ax = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]
    assert ax["status"] == "none" and ax["findings"] == []
    assert ax["note"].endswith("線索 1 條，程式核實 0 條")


def test_backfill_defaults_for_missing_fields(tmp_path):
    c = _clue()
    for k in ("direction", "affects", "source"):
        del c[k]
    run = _run_dir(tmp_path, {"axes_1.json": {"coverage": {"x_axis": _axis(clues=[c])}}},
                   [{"id": "x_axis", "affects": ["moat_trend", "thesis.H"]}])
    cb.backfill(run, fetch=_fake_fetch({"https://news.example.com/a": {}}))
    f = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]["findings"][0]
    assert f["direction"] == "0" and f["affects"] == ["moat_trend", "thesis.H"] and f["source"] == "news.example.com"


def test_backfill_url_limit_and_invalid_clues(tmp_path):
    clues = [_clue(url="https://news.example.com/p{0}".format(i)) for i in range(5)]
    clues += [{"claim": "沒有網址", "match_terms": ["a", "b"]}, "不是物件", _clue(url="file:///etc/passwd")]
    run = _run_dir(tmp_path, {"axes_1.json": {"coverage": {"x_axis": _axis(clues=clues)}}})
    pages = {"https://news.example.com/p{0}".format(i): {"text": "第{0}頁：投審會表示，甲公司遭處1,000 萬元罰鍰。".format(i)}
             for i in range(5)}
    fetch = _fake_fetch(pages)
    st = cb.backfill(run, max_urls=3, fetch=fetch)
    assert len(fetch.calls) == 3 and st["over_limit"] == 2 and st["verified"] == 3
    assert [d["outcome"] for d in st["details"]] == ["verified"] * 3 + ["over_limit"] * 2 + ["invalid", "invalid", "bad_url"]
    ax = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]
    assert ax["note"].endswith("線索 8 條，程式核實 3 條")


def test_backfill_shared_url_fetched_once_across_axes(tmp_path):
    parts = {"axes_1.json": {"coverage": {"a1": _axis(clues=[_clue()])}},
             "axes_2.json": {"coverage": {"a2": _axis(clues=[_clue(terms=["投審會", "紫光"])])}}}
    run = _run_dir(tmp_path, parts)
    fetch = _fake_fetch({"https://news.example.com/a": {}})
    st = cb.backfill(run, fetch=fetch)
    assert fetch.calls == ["https://news.example.com/a"] and st["urls"] == 1
    # a2 的詞「紫光」不在內文（只在被剝掉的 script／style 裡）→ 不升級
    assert st["axes_upgraded"] == ["a1"]


def test_backfill_fetch_exception_and_failure_never_leave_clues(tmp_path):
    def boom(url):
        raise RuntimeError("連線炸了")
    run = _run_dir(tmp_path, {"axes_1.json": {"coverage": {"x_axis": _axis(clues=[_clue()])}}})
    st = cb.backfill(run, fetch=boom)
    assert st["verified"] == 0 and st["details"][0]["outcome"] == "error"
    ax = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]
    assert "clues" not in ax and ax["status"] == "none"


def test_backfill_over_http_end_to_end(server, tmp_path, monkeypatch):
    part = {"coverage": {"x_axis": _axis(clues=[
        _clue(url=server + "/big5-meta"),
        _clue(url=server + "/missing"),
    ])}}
    run = _run_dir(tmp_path, {"axes_1.json": part})
    st = cb.backfill(run)
    assert st["fetched"] == 1 and st["fetch_failed"] == 1 and st["verified"] == 1
    f = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]["findings"][0]
    assert "罰鍰" in f["excerpt"]
    assert any((run / "fetch_cache").glob("*.json"))


def test_validate_evidence_accepts_clues_and_excerpt_source(tmp_path):
    f = {"claim": "c", "source": "s", "url": "https://a.example.com/x", "excerpt": "原文", "excerpt_from": "page",
         "excerpt_source": "program_fetch", "as_of": "2026-10-14", "direction": "+", "affects": ["thesis.R"]}
    ax = {"status": "found", "queries_run": ["q"], "findings": [f], "note": "",
          "clues": [{"claim": "x", "url": "https://a.example.com/y", "as_of": "2026-10-01", "match_terms": ["a", "b"]}]}
    fails, warns = validate_evidence.check_axis("x_axis", ax, {})
    assert fails == [] and warns == []
    ax["clues"] = "壞形狀"
    fails, warns = validate_evidence.check_axis("x_axis", ax, {})
    assert fails == [] and any(w.startswith("(info)") and "clues" in w for w in warns)
    part = tmp_path / "axes_1.json"
    ax["clues"] = [{"claim": "x", "url": "https://a.example.com/y", "match_terms": ["a", "b"]}]
    part.write_text(json.dumps({"coverage": {"customer_second_source": ax}}, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "validate_evidence.py"), "--part", str(part)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_backfill_same_page_same_excerpt_not_duplicated(tmp_path):
    part = {"coverage": {"x_axis": _axis(clues=[_clue(), _clue(claim="換個說法的同一件事")])}}
    run = _run_dir(tmp_path, {"axes_1.json": part})
    st = cb.backfill(run, fetch=_fake_fetch({"https://news.example.com/a": {}}))
    assert st["verified"] == 1 and st["duplicate"] == 1
    ax = json.loads((run / "parts" / "axes_1.json").read_text(encoding="utf-8"))["coverage"]["x_axis"]
    assert len(ax["findings"]) == 1 and ax["note"].endswith("線索 2 條，程式核實 1 條")


# ---------------------------------------------------------------------------
# rescue_undated：驗證前先救沒有 as_of 的 finding
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clear_rescue_budget():
    cb._rescue_seen.clear()
    yield
    cb._rescue_seen.clear()


def _undated(url, **kw):
    f = {"claim": "c", "source": "s", "url": url, "excerpt": None, "excerpt_from": "snippet",
         "direction": "0", "affects": ["thesis.R"]}
    f.update(kw)
    return f


def _part(tmp_path, findings, status="found", name="axes_1.json"):
    p = tmp_path / "parts"
    p.mkdir(exist_ok=True)
    path = p / name
    path.write_text(json.dumps({"coverage": {"x_axis": {"status": status, "queries_run": ["q"],
                                                        "findings": findings, "note": ""}}},
                               ensure_ascii=False), encoding="utf-8")
    return path


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))["coverage"]["x_axis"]


def test_rescue_fills_page_date_and_leaves_the_rest(tmp_path):
    fs = [_undated("https://a.example.com/1"),                        # 頁面有日期 → 救
          _undated("https://a.example.com/2"),                        # 頁面沒日期 → 不動
          _undated("https://a.example.com/3"),                        # 抓不到 → 不動
          _undated("https://a.example.com/4", as_of="不明"),          # as_of 無法解析 → 也救
          _undated("https://a.example.com/5", as_of="2026-09-01"),    # 已有日期 → 不碰
          _undated("https://a.example.com/6", claim=""),              # 其餘欄位不齊 → 救了也過不了驗證，不碰
          {"claim": "無網址", "source": "s", "direction": "0", "affects": ["x"]}]
    path = _part(tmp_path, fs)
    pages = {"https://a.example.com/1": {"page_date": "2026-10-14"}, "https://a.example.com/2": {"page_date": None},
             "https://a.example.com/4": {"page_date": "2026-08-01"}}
    fetch = _fake_fetch(pages)
    st = cb.rescue_undated(path, tmp_path / "fetch_cache", fetch=fetch)
    assert (st["rescued"], st["no_date"], st["fetch_failed"], st["over_limit"]) == (2, 1, 1, 0)
    assert fetch.calls == ["https://a.example.com/{0}".format(i) for i in (1, 2, 3, 4)]
    out = _read(path)["findings"]
    assert out[0]["as_of"] == "2026-10-14" and out[0]["as_of_note"] == "頁面發布日（程式補）"
    assert out[3]["as_of"] == "2026-08-01" and out[3]["as_of_note"] == "頁面發布日（程式補）"
    assert "as_of" not in out[1] and "as_of" not in out[2] and "as_of_note" not in out[1]
    assert out[4]["as_of"] == "2026-09-01" and "as_of_note" not in out[4]
    assert out[5]["claim"] == "" and "as_of" not in out[5]
    bak = json.loads((tmp_path / "parts" / "_pre_backfill" / "axes_1.json").read_text(encoding="utf-8"))
    assert "as_of" not in bak["coverage"]["x_axis"]["findings"][0]


def test_rescue_nothing_to_do_does_not_touch_part_or_network(tmp_path):
    path = _part(tmp_path, [_undated("https://a.example.com/1", as_of="2026-10-01")])
    before = path.read_text(encoding="utf-8")
    fetch = _fake_fetch({})
    st = cb.rescue_undated(path, tmp_path / "fetch_cache", fetch=fetch)
    assert st["details"] == [] and fetch.calls == [] and path.read_text(encoding="utf-8") == before
    assert not (tmp_path / "parts" / "_pre_backfill").exists()
    bad = tmp_path / "parts" / "axes_9.json"
    bad.write_text("{壞掉的 json", encoding="utf-8")
    assert cb.rescue_undated(bad, tmp_path / "fetch_cache")["details"] == []


def test_rescue_budget_is_shared_across_parts_and_url_fetched_once(tmp_path):
    p1 = _part(tmp_path, [_undated("https://a.example.com/{0}".format(i)) for i in range(4)], name="axes_1.json")
    p2 = _part(tmp_path, [_undated("https://a.example.com/0"), _undated("https://a.example.com/9")], name="axes_2.json")
    pages = {"https://a.example.com/{0}".format(i): {"page_date": "2026-10-14"} for i in (0, 1, 2, 3, 9)}
    fetch = _fake_fetch(pages)
    st1 = cb.rescue_undated(p1, tmp_path / "fetch_cache", fetch=fetch, max_urls=3)
    st2 = cb.rescue_undated(p2, tmp_path / "fetch_cache", fetch=fetch, max_urls=3)
    assert (st1["rescued"], st1["over_limit"]) == (3, 1)
    assert (st2["rescued"], st2["over_limit"]) == (1, 1)     # /0 已抓過（共用），/9 超額
    assert len(fetch.calls) == 3


def test_rescue_then_validate_and_drop_order(tmp_path):
    """救在丟之前：救得到的留下，救不到的才被 _drop_undated_findings 拿掉；救完整軸能過驗證。"""
    import run as dd2_run
    path = _part(tmp_path, [_undated("https://a.example.com/1", as_of="2026-10-01"),
                            _undated("https://a.example.com/2"), _undated("https://a.example.com/3")])
    fails, _ = validate_evidence.check_axis("x_axis", _read(path), {})
    assert fails  # 救之前：缺 as_of，驗證不過
    cb.rescue_undated(path, tmp_path / "fetch_cache",
                      fetch=_fake_fetch({"https://a.example.com/2": {"page_date": "2026-10-14"},
                                         "https://a.example.com/3": {"page_date": None}}))
    assert dd2_run._drop_undated_findings(path) == 1
    ax = _read(path)
    assert [f["url"][-1] for f in ax["findings"]] == ["1", "2"] and ax["status"] == "found"
    fails, _ = validate_evidence.check_axis("x_axis", ax, {})
    assert fails == []


def test_rescue_over_http_uses_page_meta_date(server, tmp_path):
    path = _part(tmp_path, [_undated(server + "/utf8"), _undated(server + "/missing")])
    st = cb.rescue_undated(path, tmp_path / "fetch_cache")
    assert (st["rescued"], st["fetch_failed"]) == (1, 1)
    assert _read(path)["findings"][0]["as_of"] == "2026-10-14"


def test_found_with_only_clues_becomes_none_when_nothing_verified(tmp_path):
    # 2383.TW 2026-10-20 供需軸：agent 只交 clues 卻填 found，全沒核實要改回 none，否則驗證判不合格
    part = {"coverage": {"supply_demand_durability": _axis(status="found", clues=[
        _clue(terms=["完全無關", "不存在的詞"])])}}
    run = _run_dir(tmp_path, {"axes_4.json": part}, [{"id": "supply_demand_durability", "affects": ["thesis.H"]}])
    cb.backfill(run, fetch=_fake_fetch({"https://news.example.com/a": {}}))
    ax = json.loads((run / "parts" / "axes_4.json").read_text(encoding="utf-8"))["coverage"]["supply_demand_durability"]
    assert ax["status"] == "none" and ax["findings"] == [] and "clues" not in ax
    # 核實到一條就維持 found
    part["coverage"]["supply_demand_durability"] = _axis(status="found", clues=[_clue()])
    run2 = _run_dir(tmp_path / "r2", {"axes_4.json": part}, [{"id": "supply_demand_durability", "affects": ["thesis.H"]}])
    cb.backfill(run2, fetch=_fake_fetch({"https://news.example.com/a": {"page_date": "2026-10-14"}}))
    ax2 = json.loads((run2 / "parts" / "axes_4.json").read_text(encoding="utf-8"))["coverage"]["supply_demand_durability"]
    assert ax2["status"] == "found" and len(ax2["findings"]) == 1
