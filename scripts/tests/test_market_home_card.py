"""build_market_state.build_home_card：thesis_points／只有 forces／判讀過期／缺 pulse 四種情境，加 CTA 方向核對。"""
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_market_state as market  # noqa: E402

TODAY = date(2026, 10, 27)


def _q(label, val, num, pctile, as_of="2026-10-26", window="252_observations", freq="daily"):
    return {"label": label, "val": val, "num": num, "pctile": pctile, "as_of": as_of,
            "pctile_window": window, "frequency": freq}


QUOTES = {
    "monitor:hy_oas": _q("HY OAS 高收益利差", "3.38%", 3.38, 98.8, "2026-10-23"),
    "monitor:brent": _q("Brent 原油", "$115.81", 115.81, 98.8),
    "monitor:wti": _q("WTI 原油", "$101.76", 101.76, 92.1),
    "internals:sahm": _q("Sahm", "0.00", 0.0, 25.0, window="12_observations", freq="monthly"),
    "cot:Gold": {"label": "Gold", "val": "+49.68%", "num": 49.68, "pctile": 62.2, "as_of": "2026-10-20",
                 "pctile_window": None, "frequency": "weekly"},
    "stress:b.credit": {"label": "壓力分項·信用", "val": "55.7", "num": 55.7, "pctile": None,
                        "as_of": "2026-10-26", "pctile_window": None},
}
MONITOR = {"categories": [{"items": [
    {"key": "hy_oas", "frequency": "daily", "pctile": 98.8, "p20": 70.6, "p60": 55.2},
    {"key": "brent", "frequency": "daily", "pctile": 98.8, "p20": 88.5, "p60": 71.4},
]}]}


def _obs(ref, num, as_of="2026-10-26"):
    return {"ref": ref, "field": "num", "value": num, "as_of": as_of}


def _read(**extra):
    r = {
        "as_of": "2026-10-27", "valid_days": 10,
        "thesis_zh": "油價回落，但利率與信用的壓力還在。布蘭特原油回到 110.01 美元。",
        "forces": [
            {"title": "信用利差續寬", "refs": [{"ref": "monitor:hy_oas", "why": "指數層的信用壓力"},
                                         {"ref": "stress:b.credit", "why": "信用壓力分項"},
                                         {"ref": "monitor:brent", "why": "不該在這組出現第二次"},
                                         {"ref": "monitor:wti", "why": "美國油價"},
                                         {"ref": "cot:Gold", "why": "黃金部位"}]},
            {"title": "油價回落", "refs": [{"ref": "monitor:brent", "why": "油價衝擊的主要讀數"},
                                       {"ref": "monitor:wti", "why": "美國本土油價"}]},
        ],
        "observations": [_obs("monitor:brent", 110.01), _obs("monitor:wti", 101.11)],
        # 判讀落地時凍結的證據（accept 時寫入 read.json）：盤中價 110.01，之後被收盤價 115.81 取代
        "evidence_snapshot": {"quotes": {"monitor:brent": dict(QUOTES["monitor:brent"], val="$110.01", num=110.01),
                                         "monitor:wti": dict(QUOTES["monitor:wti"])}},
    }
    r.update(extra)
    return r


def _card(read, pulse=None, **kw):
    headline, as_of = market.read_headline_fields(read, TODAY)
    return market.build_home_card(
        read, headline, as_of, {"headline": "機械 headline。"}, {"quotes": QUOTES}, MONITOR, pulse,
        kw.get("environment", []), kw.get("council", {}), kw.get("flows", {}), None, None, "2026-10-27")


PULSE = {"radar_as_of": "2026-10-26", "assets": [
    {"label": "大宗", "ticker": "DBC", "quadrant": "領先", "cell": "strong_up", "streak_days": 2,
     "streak_capped": False, "change": {"from": "轉弱", "to": "領先", "status": "near", "held_days": 2}},
    {"label": "標普500", "ticker": "SPY", "quadrant": "轉弱", "cell": "strong_down", "streak_days": 3,
     "streak_capped": False, "change": {"from": "領先", "to": "轉弱", "status": "confirmed", "held_days": 3}},
    {"label": "美長債", "ticker": "TLT", "quadrant": "改善", "cell": "weak_up", "streak_days": 8,
     "streak_capped": False, "change": None},
    {"label": "黃金", "ticker": "GLD", "quadrant": "落後", "cell": "weak_down", "streak_days": 24,
     "streak_capped": False, "change": None},
]}


def test_thesis_points_used_with_labels_position_and_dedupe():
    read = _read(
        headline_zh="油價回落，但利率與信用的壓力還在。",
        thesis_points=[
            {"claim_zh": "信用利差仍在高檔", "refs": [{"ref": "monitor:hy_oas", "why": "垃圾債的壓力"}]},
            {"claim_zh": "油價高於一般水準", "refs": [{"ref": "monitor:brent", "why": "油價"},
                                              {"ref": "monitor:hy_oas", "why": "重複，不該再出現"},
                                              {"ref": "monitor:wti", "why": "美國油價"}]},
        ])
    card = _card(read, PULSE)
    assert card["headline"] == "油價回落，但利率與信用的壓力還在。"
    assert card["headline_source"] == "headline_zh"
    assert card["read_as_of"] == "2026-10-27" and card["data_as_of"] == "2026-10-27"
    assert [g["source"] for g in card["groups"]] == ["thesis_points", "thesis_points"]
    assert [g["claim"] for g in card["groups"]] == ["信用利差仍在高檔", "油價高於一般水準"]
    hy = card["groups"][0]["lines"][0]
    assert hy["label"] == "高收益債利差" and hy["value_text"] == "3.38%" and hy["as_of"] == "2026-10-23"
    assert hy["position_text"] == "高於近一年 99% 的交易日；三個月前這個位置是 55%、一個月前 71%"
    refs2 = [l["ref"] for l in card["groups"][1]["lines"]]
    assert refs2 == ["monitor:brent", "monitor:wti"]            # hy_oas 已出現過，不重複
    # 判讀寫稿時的價格（110.01）與現值（115.81）不同：現值為主，舊值另存
    brent = card["groups"][1]["lines"][0]
    assert brent["value_text"] == "$115.81" and brent["read_value_text"] == "$110.01"
    assert "read_value_text" not in hy


def test_forces_fallback_caps_lines_and_uses_why_when_label_unknown():
    card = _card(_read(), PULSE)
    assert card["headline_source"] == "thesis_zh"
    assert card["headline"] == "油價回落，但利率與信用的壓力還在。"          # 第一句完整，不截字
    g0, g1 = card["groups"]
    assert g0["source"] == "forces" and g0["claim"] == "信用利差續寬"
    assert [l["ref"] for l in g0["lines"]] == ["monitor:hy_oas", "stress:b.credit", "monitor:brent"]  # 上限 3 條，wti、gold 被截掉
    assert g0["lines"][1]["label"] == "信用壓力分數" and g0["lines"][1]["position_text"] == ""
    assert [l["ref"] for l in g1["lines"]] == ["monitor:wti"]               # brent 已在第一組出現過，不重複


def test_unknown_ref_label_falls_back_to_why():
    read = _read(forces=[{"title": "x", "refs": [{"ref": "theme:HBM 超級循環", "why": "擁擠度第一名的主題"}]}])
    quotes_with_theme = dict(QUOTES, **{"theme:HBM 超級循環": _q("主題擁擠度", "74.9", 74.9, None, window=None, freq="weekly")})
    headline, as_of = market.read_headline_fields(read, TODAY)
    card = market.build_home_card(read, headline, as_of, {}, {"quotes": quotes_with_theme}, MONITOR, None, [], {}, {}, None, None, "x")
    assert card["groups"][0]["lines"][0]["label"] == "擁擠度第一名的主題"


def test_window_words_for_weekly_monthly_and_unknown_window():
    assert market.home_position_text(QUOTES["internals:sahm"]) == "高於近一年 25% 的月份"
    assert market.home_position_text(QUOTES["cot:Gold"]) == ""               # 窗口不明就不寫
    assert market.home_position_text(_q("x", "1", 1, 100.0)) == "是近一年最高"
    assert market.home_position_text(_q("x", "1", 1, 99.6)) == "高於近一年 99% 的交易日"   # 不可進位成 100


def test_expired_read_falls_back_to_mechanical_and_drops_groups():
    read = _read(as_of="2026-10-01", valid_days=10, headline_zh="過期的一句話。")
    card = _card(read, PULSE)
    assert card["headline"] == "機械 headline。" and card["headline_source"] == "mechanical"
    assert card["read_expired"] is True
    assert card["read_as_of"] == "2026-10-01"
    assert card["groups"] == []


def test_long_first_sentence_is_not_truncated():
    read = _read(thesis_zh="這是一句非常非常長的主張" * 10 + "。後面還有一句。")
    card = _card(read)
    assert card["headline"] == "機械 headline。" and card["headline_source"] == "mechanical"


def test_no_read_at_all():
    card = market.build_home_card(None, None, None, {"headline": "機械 headline。"}, {"quotes": QUOTES},
                                  MONITOR, None, [], {}, {}, None, None, "2026-10-27")
    assert card["headline"] == "機械 headline。" and card["groups"] == [] and card["read_expired"] is False


def test_missing_pulse_gives_no_momentum_and_old_pulse_without_assets_too():
    assert _card(_read(), None)["momentum"] is None
    assert _card(_read(), {"headline": "舊版 pulse，沒有 assets"})["momentum"] is None


def test_momentum_two_by_two():
    m = _card(_read(), PULSE)["momentum"]
    assert m["as_of"] == "2026-10-26"
    assert {k: [i["ticker"] for i in v["items"]] for k, v in m["cells"].items()} == {
        "strong_up": ["DBC"], "strong_down": ["SPY"], "weak_up": ["TLT"], "weak_down": ["GLD"]}
    assert [v["title"] for v in m["cells"].values()] == ["強且變強", "強但轉弱", "弱但轉強", "弱且變弱"]
    spy = m["cells"]["strong_down"]["items"][0]
    assert spy["change"]["text"] == "由「強且變強」轉入，已站穩 3 個交易日"
    dbc = m["cells"]["strong_up"]["items"][0]
    assert dbc["change"]["text"] == "剛從「強但轉弱」跨進來 2 個交易日，還沒站穩"
    assert m["cells"]["weak_up"]["items"][0]["change"] is None


def test_momentum_change_text_when_asset_passed_through_another_cell():
    """QQQ 型：動能 8 日前轉向（領先→轉弱），3 日前相對強弱也跌破（→落後）。兩個日數要分開講。"""
    pulse = {"radar_as_of": "2026-10-26", "assets": [
        {"label": "那斯達克100", "ticker": "QQQ", "quadrant": "落後", "cell": "weak_down", "streak_days": 3,
         "streak_capped": False, "change": {"from": "領先", "to": "落後", "status": "confirmed", "held_days": 8}}]}
    item = market.home_momentum(pulse)["cells"]["weak_down"]["items"][0]
    assert item["change"]["text"] == "動能 8 個交易日前轉向，已由「強且變強」走到這格（在這格 3 日）"


def _cta(market_code, px, level20, composite="+2/3"):
    return {"market": market_code, "proxy": "X", "px": px, "composite": composite,
            "levels": [{"w": 20, "level": level20, "dist_pct": round((level20 / px - 1) * 100, 2)}]}


def test_cta_direction_matches_signal_definition():
    """build_flowmap：signal＝1 if 現價 > flip_level。現價低於翻轉價 → 目前是賣出訊號 → 要「再漲」才轉為買進。"""
    below = market.home_cta_gauge({"cta": [_cta("SPX", 100.0, 101.5)]})
    assert 100.0 < 101.5                       # 現價 < flip_level → signal -1
    assert below["value_text"] == "標普 500 再漲 1.5%" and below["label"] == "20 日訊號將轉為買進"
    above = market.home_cta_gauge({"cta": [_cta("NDX", 100.0, 97.0)]})
    assert 100.0 > 97.0                        # 現價 > flip_level → signal +1
    assert above["value_text"] == "那斯達克 100 再跌 3.0%" and above["label"] == "20 日訊號將轉為賣出"


def test_cta_picks_nearest_20d_across_markets_and_names_it():
    g = market.home_cta_gauge({"cta": [_cta("SPX", 100.0, 103.0), _cta("RTY", 100.0, 99.0, "+0/3"),
                                       _cta("NDX", 100.0, 104.0)]})
    assert g["value_text"] == "羅素 2000 再跌 1.0%"
    assert g["detail"] == "羅素 2000 在 20、60、120 日三個期間中，目前 0 個看多。"
    assert market.home_cta_gauge({"cta": []}) is None
    assert market.home_cta_gauge({}) is None


def test_gauges_now_and_next_month():
    env = [{"key": "monitor", "value": "66.8 · 緊張", "as_of": "2026-10-26"},
           {"key": "detective", "value": "6 · 平靜", "as_of": "2026-10-26"}]
    council = {"vol_up_21d": {"p": 0.65, "p_clim": 0.48}}
    snap = {"risk_gauge_score": 0.167, "risk_gauge_label": "中性", "risk_gauge_date": "2026-10-27"}
    headline, as_of = market.read_headline_fields(_read(), TODAY)
    card = market.build_home_card(_read(), headline, as_of, {}, {"quotes": QUOTES}, MONITOR, None, env, council,
                                  {"cta": [_cta("SPX", 100.0, 101.5)]}, snap, None, "2026-10-27")
    now = {g["key"]: g for g in card["gauges"]["now"]}
    assert now["stress"]["value_text"] == "66.8" and now["stress"]["label"] == "緊張"
    assert now["alert"]["value_text"] == "6" and now["alert"]["label"] == "平靜"
    assert now["risk_gauge"]["value_text"] == "+0.17" and now["risk_gauge"]["label"] == "中性"
    nxt = {g["key"]: g for g in card["gauges"]["next_month"]}
    assert nxt["vol_up_21d"]["value_text"] == "65%" and nxt["vol_up_21d"]["label"] == "高於平常"
    assert "48%" in nxt["vol_up_21d"]["note"]
    assert nxt["cta_flip"]["label"] == "20 日訊號將轉為買進"
    for g in list(now.values()) + list(nxt.values()):
        assert {"key", "name", "value_text", "label", "note", "href"} <= set(g)


def test_risk_gauge_falls_back_to_cache_file_shape():
    headline, as_of = market.read_headline_fields(_read(), TODAY)
    card = market.build_home_card(_read(), headline, as_of, {}, {"quotes": QUOTES}, MONITOR, None, [], {}, {},
                                  None, {"score": -0.5, "label_zh": "風險趨避", "as_of": "2026-10-27"}, "2026-10-27")
    g = card["gauges"]["now"][0]
    assert g["key"] == "risk_gauge" and g["value_text"] == "-0.50" and g["label"] == "風險趨避"
