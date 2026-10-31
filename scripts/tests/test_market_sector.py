"""2026-10-15：市況判讀「那斯達克與半導體」段落——book:*／theme:* 證據與第 18 項檢查。"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_market_state as market  # noqa: E402
import check_market_read as critic  # noqa: E402
import market_read_summary as summary  # noqa: E402

PAGE = Path(__file__).parents[2] / "docs" / "market" / "index.html"


def _long_track():
    return {
        "tickers": {
            "SMH": {"market": "美股", "executed_pct": 50.0, "final_weight_pct": 59.1,
                    "wk_close": 588.12, "w52": 480.62},
            "QQQ": {"market": "美股", "executed_pct": 50.0, "wk_close": 743.57, "w52": 661.74},
            "2330": {"market": "台股", "executed_pct": 60.0, "wk_close": 2490.0, "w52": 2012.26},
        },
        "history_us": [{"date": "2026-10-12"}, {"date": "2026-10-13"}],
        "history_tw": [{"date": "2026-10-14"}],
    }


def test_book_quotes_use_executed_exposure_and_market_dates():
    q = market.build_quotes(None, None, None, None, None, {}, [], _long_track())
    assert q["book:SMH_exec"]["num"] == 100.0  # 執行層水位（pp 50 × 2），不是目標權重 59.1
    assert q["book:SMH_exec"]["as_of"] == "2026-10-13"
    assert q["book:2330_exec"]["as_of"] == "2026-10-14"
    assert q["book:SMH_w52_dist"]["num"] == 22.4
    assert q["book:us_exec_total"]["num"] == 100.0
    assert q["book:tw_exec_total"]["num"] == 60.0
    assert q["book:SMH_exec"]["source_label"] == "實單執行層"


def test_book_quotes_missing_long_track_records_gap():
    gaps = []
    q = market.build_quotes(None, None, None, None, None, {}, gaps)
    assert not any(k.startswith("book:") for k in q)
    assert any("book:*" in g for g in gaps)


def test_theme_quotes_take_top_ranked_themes():
    themes = [{"rank": r, "name": f"主題{r}", "score": 80 - r} for r in range(12, 0, -1)]
    crowding = {"themes": themes, "generated_at": "2026-10-12T01:29:03Z"}
    q = market.build_quotes(None, None, None, crowding, None, {}, [])
    keys = sorted(k for k in q if k.startswith("theme:"))
    assert len(keys) == market.THEME_TOP_N
    assert q["theme:主題1"]["num"] == 79 and q["theme:主題1"]["as_of"] == "2026-10-12"
    assert "theme:主題9" not in q


def _sector(refs):
    return {"body_zh": "半導體轉弱，那斯達克也跟著回落。", "refs": [{"ref": r, "why": "說明"} for r in refs]}


def test_sector_check_old_read_warns_new_read_fails():
    assert critic.check_sector({"as_of": "2026-10-14"})[0] == critic.WARN
    assert critic.check_sector({"as_of": "2026-10-16"})[0] == critic.FAIL


def test_sector_check_requires_semis_nasdaq_and_book_refs():
    ok = _sector(["monitor:sox", "internals:qqew_qqq", "book:SMH_exec"])
    assert critic.check_sector({"as_of": "2026-10-16", "sector": ok})[0] == critic.PASS
    no_book = _sector(["monitor:sox", "monitor:sox_ndx", "monitor:ndx"])
    status, detail = critic.check_sector({"as_of": "2026-10-16", "sector": no_book})
    assert status == critic.FAIL and "book:*" in detail
    no_semis = _sector(["monitor:ndx", "cot:Nasdaq-100 E-mini", "book:SMH_exec"])
    assert critic.check_sector({"as_of": "2026-10-16", "sector": no_semis})[0] == critic.FAIL


def test_sector_refs_and_headline_are_collected():
    data = {"sector": _sector(["monitor:sox", "monitor:ndx", "book:SMH_exec"])}
    assert ("sector.refs[2].ref", "book:SMH_exec") in critic.collect_refs(data)
    assert ("$.sector.body_zh", data["sector"]["body_zh"]) in critic.headline_fields(data)


def test_sector_in_page_and_email():
    html = PAGE.read_text(encoding="utf-8")
    assert 'id="sec-sector"' in html and "renderSector(usableRead, data);" in html
    data = {"mode": "commentary", "as_of": "2026-10-16", "sector": {"body_zh": "半導體轉弱。"}}
    assert "那斯達克與半導體" in summary.render_sector_html(data)
    assert summary.render_sector_html({"mode": "commentary"}) == ""
