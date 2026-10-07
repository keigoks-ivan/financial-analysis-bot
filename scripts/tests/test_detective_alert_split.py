"""警戒度拆分（2026-10-06）：分面、序列去重、警戒度只數壓力面、熱度計數、歷史第 5 欄。

分面只看訊號量的是什麼；pts／cap 一個數字都沒動。
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import build_detective as bd  # noqa: E402


def sig(key, fact="", sev="yellow", state="active", days=1, score=5.0, source=None):
    return {"key": key, "fact": fact, "sev": sev, "state": state, "days_active": days,
            "score": score, "source": source or key.split(":")[0]}


MOVE_DOWN = "{} 單日跌幅 ▼ 2.50%，為一年日波動的 2.40 倍標準差"
MOVE_UP = "{} 單日漲幅 ▲ 2.50%，為一年日波動的 2.40 倍標準差"
LVL_HI = "{} 現值 1 進入一年歷史高位前 1.0%（分位 99.0）"
LVL_HI_OLD = "{} 現值 1 進入一年水位前 1.0%（分位 99.0）"
LVL_LO = "{} 現值 1 落到一年歷史低位後 1%（低分位警示）"
STREAK_UP = "{} 連續 5 日上漲"
STREAK_DN = "{} 連續 8 日下跌"
NEW_LOW = "{} 觸及一年新低（1）"


@pytest.mark.parametrize("key,fact,want", [
    # 風險資產：重挫／新低／水位極低＝壓力；水位極高、連漲、急漲＝過熱
    ("monitor:indices:sp500:down", MOVE_DOWN.format("S&P 500"), "stress"),
    ("monitor:indices:ndx:down", NEW_LOW.format("Nasdaq 100"), "stress"),
    ("monitor:sectors:xlv:down", MOVE_DOWN.format("XLV"), "stress"),
    ("monitor:indices:sp500:up", MOVE_UP.format("S&P 500"), "heat"),
    ("monitor:indices:ndx:up", STREAK_UP.format("Nasdaq 100"), "heat"),
    ("monitor:factors:mtum:up", STREAK_UP.format("MTUM"), "heat"),
    ("monitor:indices:ftse:down", STREAK_DN.format("FTSE"), "other"),   # 連跌歸 other
    ("monitor:indices:sp500", LVL_HI.format("S&P"), "heat"),
    ("monitor:indices:sp500", LVL_LO.format("S&P"), "stress"),
    # 壓力計
    ("monitor:vol:vvix:up", MOVE_UP.format("VVIX"), "stress"),
    ("monitor:vol:vix9d:up", MOVE_UP.format("VIX9D"), "stress"),
    ("monitor:vol:vix:down", MOVE_DOWN.format("VIX"), "other"),         # 壓力解除不算壓力
    ("monitor:vol:vix", LVL_HI.format("VIX"), "stress"),
    ("monitor:vol:vix", LVL_LO.format("VIX"), "heat"),                  # 壓力計極低＝自滿
    ("monitor:vol:vix_ts", "VIX 短天期比長天期貴中：VIX9D/VIX = 1.020 > 1", "stress"),
    ("monitor:vol:move", LVL_HI.format("MOVE"), "stress"),
    ("monitor:vol:skew:up", MOVE_UP.format("SKEW"), "other"),
    # 信用
    ("monitor:credit:ccc_oas", LVL_HI.format("CCC OAS"), "stress"),
    ("monitor:credit:ccc_oas", LVL_HI_OLD.format("CCC OAS"), "stress"),  # 早期快照寫法
    ("monitor:credit:hy_oas:up", MOVE_UP.format("HY OAS"), "stress"),
    ("monitor:credit:hy_oas:down", MOVE_DOWN.format("HY OAS"), "other"),
    ("monitor:credit:hyg:down", MOVE_DOWN.format("HYG"), "stress"),
    ("monitor:credit:hyg_lqd:down", MOVE_DOWN.format("HYG/LQD"), "stress"),
    ("monitor:credit:hyg_lqd:up", "股市漲但信用市場不買單：S&P 500 ▲ 0.5% 上漲，但 HYG/LQD 信用比 z = -2.1 大幅走弱", "stress"),
    ("monitor:credit:lqd:down", MOVE_DOWN.format("LQD"), "other"),      # 久期驅動，歸 other
    ("monitor:credit:emb:down", MOVE_DOWN.format("EMB"), "other"),
    # 結構事件
    ("monitor:rates:t10y2y", "10Y−2Y 利差正負翻轉：+0.10% → -0.02%", "stress"),
    ("monitor:vol:fear_greed", "CNN Fear & Greed 進入極端恐懼區：8", "stress"),
    ("monitor:vol:fear_greed", "CNN Fear & Greed 進入極端貪婪區：93", "heat"),
    # 商品／外匯／利率單日波動、水位：other
    ("monitor:commodities:corn:down", MOVE_DOWN.format("玉米"), "other"),
    ("monitor:fx:dxy:up", MOVE_UP.format("DXY"), "other"),
    ("monitor:rates:real10y", LVL_HI.format("實質利率"), "other"),
    ("monitor:rates:tlt:down", STREAK_DN.format("TLT"), "other"),
    ("monitor:crypto:btc:down", MOVE_DOWN.format("BTC"), "other"),
    ("monitor:factors:itb_spy", LVL_LO.format("ITB/SPY"), "other"),     # 拿不準 → other
    # 其他源
    ("reversal:indices:hsi:down", "香港恆生 一年分位三點路徑 8→38→6", "other"),
    ("rotation:quadrant:QQQ:up", "象限 轉弱→領先", "other"),
    ("sector:rotation:XLK:up", "科技 XLK 象限 轉弱→領先", "other"),
    ("sector:diverge:xlv:down", "XLV 單日 -2.4σ，同日 S&P 500 +0.1σ", "stress"),
    ("sector:diverge:xlk:up", "XLK 單日 +2.4σ，同日 S&P 500 +0.1σ", "heat"),
    ("sector:cluster:down", "3 個產業同日領跌", "stress"),
    ("regime:axis:x", "regime 軸變化", "other"),
    ("regime:composite", "regime 位置位移", "other"),
    ("macro_clock:quadrant", "總經時鐘象限由「復甦」移至「滯脹」（a→b）", "stress"),
    ("macro_clock:quadrant", "總經時鐘象限由「滯脹」移至「復甦」（a→b）", "other"),
    ("variance:ticker:APH", "APH 財測落差", "other"),
    ("variance:fleet:redflags", "財測落差紅旗叢集", "other"),
    ("kill:MACRO_X_1:0", "否證指標已越線", "other"),
    ("crowding:cot:gold", "Gold COT 偏多極端", "heat"),
    ("crowding:cot:gold", "Gold COT 偏空極端", "heat"),
    ("crowding:etf:GLD", "GLD 動能分位 99", "heat"),
    ("crowding:theme:ai-networking", "AI Networking 擁擠分 75", "heat"),
])
def test_signal_side(key, fact, want):
    assert bd._signal_side(sig(key, fact)) == want


def test_every_historical_key_gets_a_side_and_unknowns_are_other():
    assert bd._signal_side({"key": "mystery:x:y", "fact": "?"}) == "other"
    assert bd._signal_side({}) == "other"
    # 有 monitor 前綴但文字認不得規則 → other
    assert bd._signal_side(sig("monitor:indices:sp500", "不認得的句子")) == "other"


# ── 序列去重 ───────────────────────────────────────────────────────────
@pytest.mark.parametrize("a,b", [
    ("monitor:indices:hsi:down", "reversal:indices:hsi:down"),
    ("monitor:indices:hsi:down", "monitor:indices:hsi:up"),
    ("monitor:indices:hsi:down", "sector:diverge:hsi:down"),
    ("sector:rotation:XLV:down", "sector:rotation:XLV:up"),
    ("rotation:quadrant:XLV:down", "sector:rotation:XLV:up"),
    ("crowding:theme:advanced-packaging", "crowding:theme:advancedpackaging"),
])
def test_series_key_merges_same_underlying_series(a, b):
    assert bd._series_key({"key": a}) == bd._series_key({"key": b})


@pytest.mark.parametrize("a,b", [
    ("monitor:indices:hsi:down", "monitor:indices:ndx:down"),
    ("crowding:cot:gold", "crowding:etf:GLD"),
    ("crowding:theme:ai-networking", "crowding:theme:ai-eda-ip"),
    ("variance:ticker:APH", "variance:ticker:PANW"),
])
def test_series_key_keeps_different_series_apart(a, b):
    assert bd._series_key({"key": a}) != bd._series_key({"key": b})


# ── 警戒度只數壓力面 ────────────────────────────────────────────────────
def test_weights_unchanged_except_kill_components_removed():
    assert bd.ALERT_WEIGHTS == {
        "red_signal": {"pts": 8.0, "cap": 30.0},
        "yellow_signal": {"pts": 0.7, "cap": 18.0},
        "composite_red": {"pts": 12.0, "cap": 36.0},
        "composite_yellow": {"pts": 6.0, "cap": 18.0},
        "composite_near": {"pts": 6.0, "cap": 15.0},
        "escalated": {"pts": 4.0, "cap": 16.0},
        "sustained": {"pts": 2.0, "cap": 12.0},
    }


def _stress_sigs(n):
    names = sorted(bd._SIDE_RISK_ASSETS)
    return [sig(f"monitor:indices:{names[i]}:down", MOVE_DOWN.format(names[i])) for i in range(n)]


def test_score_counts_only_stress_signals():
    stress = [sig("monitor:indices:sp500:down", MOVE_DOWN.format("S&P"), sev="red")]
    heat = [sig("crowding:cot:gold", "x"), sig("monitor:indices:ndx:up", STREAK_UP.format("N"))]
    other = [sig("monitor:commodities:corn:down", MOVE_DOWN.format("玉米"), sev="red"),
             sig("kill:MACRO_X_1:0", "kill", sev="red", days=9)]
    only_stress = bd.compute_alert_level(stress, [], "d")
    mixed = bd.compute_alert_level(stress + heat + other, [], "d")
    assert only_stress["score"] == mixed["score"] == 8        # 1 條紅燈 × 8 分
    assert only_stress["drivers"] == [{"label": "1 條訊號亮紅燈", "points": 8}]


def test_yellow_pts_and_cap_unchanged():
    assert bd.compute_alert_level(_stress_sigs(10), [], "d")["score"] == 7     # 10 × 0.7
    assert bd.compute_alert_level(_stress_sigs(29), [], "d")["score"] == 18    # 29 × 0.7 = 20.3 → cap 18


def test_same_series_counted_once_and_most_severe_wins():
    a = sig("monitor:indices:hsi:down", MOVE_DOWN.format("恆生"), sev="yellow")
    b = sig("monitor:indices:hsi:down", NEW_LOW.format("恆生"), sev="red")
    # reversal 是 other；monitor 兩筆同鍵（實務上同鍵只會有一筆，這裡直接測去重取最嚴重）
    assert bd.compute_alert_level([a, b], [], "d")["score"] == 8
    assert bd.compute_alert_level([a], [], "d")["score"] == 1                  # 0.7 → 1


def test_escalated_and_sustained_only_from_stress():
    s_stress = sig("monitor:indices:sp500:down", NEW_LOW.format("S&P"), sev="red",
                   state="escalated", days=6)
    s_heat = sig("crowding:cot:gold", "x", sev="red", state="escalated", days=9)
    lv = bd.compute_alert_level([s_stress, s_heat], [], "d")
    # 紅 8 ＋ escalated 4 ＋ sustained 2
    assert lv["score"] == 14


def _comp(cid, fired=False, sev=None, met=1, need=2):
    return {"id": cid, "status": "active", "fired": fired, "sev": sev,
            "met_count": met, "min_true": need}


def test_composites_split_by_side_and_near_counted_for_stress_only():
    comps = [_comp("R1", False, met=2, need=3),           # 壓力面 near → 6
             _comp("R7", False, met=1, need=2),           # 過熱面 near → 不計
             _comp("R6", True, "yellow", 2, 2),           # 過熱面 fired → 不計
             _comp("R4", True, "red", 3, 3)]              # 壓力面 fired 紅 → 12
    assert bd.compute_alert_level([], comps, "d")["score"] == 18
    assert bd.STRESS_COMPOSITES == {"R1", "R2", "R3", "R4", "R5", "R8"}
    assert bd.HEAT_COMPOSITES == {"R6", "R7", "R9"}


def test_kill_watch_no_longer_affects_score():
    import inspect
    assert list(inspect.signature(bd.compute_alert_level).parameters) == ["signals", "composites", "as_of"]


# ── 熱度 ───────────────────────────────────────────────────────────────
def test_heat_count_distinct_series_and_fired_heat_composites():
    sigs = [sig("crowding:theme:advanced-packaging", "x"),
            sig("crowding:theme:advancedpackaging", "x"),       # 同一主題只算一次
            sig("crowding:cot:gold", "x"),
            sig("monitor:indices:ndx:up", STREAK_UP.format("N")),
            sig("monitor:indices:sp500:down", MOVE_DOWN.format("S&P")),   # 壓力面不算
            sig("sector:rotation:XLK:up", "x")]                            # other 不算
    comps = [_comp("R6", True, "yellow", 2, 2), _comp("R7", False), _comp("R4", True, "red", 3, 3)]
    h = bd.compute_heat_level(sigs, comps, "2026-10-05")
    assert h == {"count": 3, "composites_fired": ["R6"], "as_of": "2026-10-05"}


def test_heat_level_empty():
    assert bd.compute_heat_level([], [], "d") == {"count": 0, "composites_fired": [], "as_of": "d"}


# ── crowding 主題合併 ───────────────────────────────────────────────────
def test_crowding_signals_merge_advanced_packaging_keep_higher_score():
    crowd = {"cot_as_of": "x", "cot": [], "etf": [], "themes": [
        {"name": "Advanced Packaging", "score": 74.2, "rank": 6},
        {"name": "AdvancedPackaging", "score": 78.0, "rank": 3},
        {"name": "AI Networking", "score": 75.6, "rank": 4},
        {"name": "HBM", "score": 71.0, "rank": 5},
        {"name": "Low", "score": 60.0, "rank": 9}]}
    out = bd.crowding_signals(crowd)
    keys = [s["key"] for s in out]
    assert keys == ["crowding:theme:advancedpackaging", "crowding:theme:ai-networking",
                    "crowding:theme:hbm"]
    assert "78" in out[0]["fact"]


# ── 歷史第 5 欄 ─────────────────────────────────────────────────────────
def test_update_alert_history_writes_heat_as_fifth_column(tmp_path, monkeypatch):
    monkeypatch.setattr(bd, "DOCS", str(tmp_path))
    (tmp_path / "detective" / "data").mkdir(parents=True)
    lv = {"score": 8, "band": "calm"}
    assert bd.update_alert_history("2026-10-05", lv, 7773.95, 20) is True
    p = tmp_path / "detective" / "data" / "alert_history.json"
    assert json.loads(p.read_text())["points"] == [["2026-10-05", 8, "calm", 7773.95, 20]]
    # 同日重跑零 churn；隔日 append
    assert bd.update_alert_history("2026-10-05", lv, 7773.95, 20) is False
    bd.update_alert_history("2026-10-06", {"score": 9, "band": "calm"}, 7800.0, 18)
    assert len(json.loads(p.read_text())["points"]) == 2
