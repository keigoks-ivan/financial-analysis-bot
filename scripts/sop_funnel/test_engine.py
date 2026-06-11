#!/usr/bin/env python3
"""SOP 漏斗引擎驗證 — 合成序列單元測試 + 真實資料回放錨。

跑法：python3 scripts/sop_funnel/test_engine.py
合成測試覆蓋每條五狀態機轉換的邊界；回放錨鎖定 2026-06-11 設計時驗證過的
NVDA/AVGO/2330 起漲點行為（引擎改動若挪動這些錨 = regression）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sop_funnel.engine import (  # noqa: E402
    PARAMS, build_frame, scan_ticker, simulate_trade, quality_check,
)

WIDE = Path(__file__).resolve().parent.parent.parent / "data" / "state_machine_cache" / "study_closes_wide_latest.csv.gz"
N_PASS = 0


def ok(cond, msg):
    global N_PASS
    if not cond:
        raise AssertionError(f"FAIL: {msg}")
    N_PASS += 1
    print(f"  ✓ {msg}")


def make_series(segments: list[tuple[int, float, float]],
                start="2015-01-01") -> pd.Series:
    """[(天數, 起價, 迄價), ...] → 連續 business-day 收盤序列（線性內插）。"""
    vals: list[float] = []
    for n, a, b in segments:
        vals.extend(np.linspace(a, b, n, endpoint=False))
    idx = pd.bdate_range(start, periods=len(vals))
    return pd.Series(vals, index=idx)


# ── 合成測試 ─────────────────────────────────────────────────────────────────
def test_frozen_no_lookahead():
    print("[1] 凍結週線 — 無部分週 look-ahead")
    ser = make_series([(1500, 50, 100)])
    fr = build_frame(ser)
    d = ser.index[-1]                      # 序列末日（多半非週五）
    pos = fr._frozen_pos(d)
    ok(fr.wclose.index[pos] < d, "frozen 週 label 嚴格早於當日")
    # 把當日價格改成 10 倍，frozen 值不得改變
    ser2 = ser.copy(); ser2.iloc[-1] *= 10
    fr2 = build_frame(ser2)
    ok(fr.frozen("wma52", d) == fr2.frozen("wma52", d), "改動當日價不影響凍結 MA52w")
    ok(fr.frozen("bb2", d) == fr2.frozen("bb2", d), "改動當日價不影響凍結 BBand")


def test_a1_vs_a2():
    print("[2] A1 起漲（基期≥26週）vs A2 續勢")
    # 長升段（天天創高 → A2）→ 平台 30 週不創高 → 突破日 = A1
    ser = make_series([(1500, 50, 100), (150, 99, 99.5), (5, 101, 103)])
    fr = build_frame(ser)
    evs = scan_ticker(fr, True, [])
    a1 = [e for e in evs if e["type"] == "A1"]
    a2 = [e for e in evs if e["type"] == "A2"]
    ok(len(a1) >= 1, f"平台突破產生 A1（{len(a1)} 筆）")
    ok(a1[-1]["base_age_weeks"] >= 26, f"A1 基期 {a1[-1]['base_age_weeks']}w ≥ 26")
    ok(len(a2) > 0, "升段途中的新高為 A2 續勢")
    ok(all(e["base_age_weeks"] < 26 for e in a2), "所有 A2 基期 < 26 週")


def test_quality_veto_recorded():
    print("[3] 四條件 fail → 訊號記錄為 vetoed")
    ser = make_series([(1500, 50, 100), (150, 99, 99.5), (5, 101, 103)])
    fr = build_frame(ser)
    evs = scan_ticker(fr, False, ["PEG≥2"])
    a1 = [e for e in evs if e["type"] == "A1"][-1]
    ok(any("四條件fail" in v for v in a1["vetoes"]), "A1 帶四條件 fail 否決標記")
    evs2 = scan_ticker(fr, None, [])
    a12 = [e for e in evs2 if e["type"] == "A1"][-1]
    ok("四條件缺資料" in a12["vetoes"], "缺資料 = 不過閘（記錄缺資料否決）")


def test_b_second_train():
    print("[4] B 第二班車 — 錨定 A1、首次站回、一錨一次")
    # A1 突破 → 漲遠（拉開與 52週線距離）→ 回踩破 60MA 但守住 52週線 → 站回（B）
    # → 再回踩再站回（不得再 B）
    ser = make_series([
        (1500, 50, 100), (150, 99, 99.5),    # 基期平台
        (40, 101, 130),                      # A1 突破段，跑遠
        (20, 130, 108),                      # 回踩破 60MA（守住 52週線 ~99）
        (20, 108, 126),                      # 站回 → B
        (15, 126, 110),                      # 第二次回踩
        (20, 110, 128),                      # 第二次站回 → 不得再 B
    ])
    fr = build_frame(ser)
    evs = scan_ticker(fr, True, [])
    bs = [e for e in evs if e["type"] == "B"]
    a1_dates = [e["date"] for e in evs if e["type"] == "A1"]
    ok(len(bs) == 1, f"每錨僅一次 B（實得 {len(bs)} 筆）")
    ok(bs[0]["anchor_a1_date"] in a1_dates, "B 錨指向 A1 事件日")


def test_t4_band_trim_and_rebuy():
    print("[5] 態④ ×0.97 減碼 + T+1 執行 + 回補")
    # 進場後盤整（遠離 52週線）→ 單日跌破 60MA×0.97 → 次日減至 50%
    # → 回升站回 60MA → 回補（回踩全程守住 52週線，不得觸態⑤）
    ser = make_series([
        (1500, 50, 100),                     # 趨勢段（鋪 200 週均線排列）
        (30, 100, 118),                      # 推升段，拉開與 52週線距離
        (60, 117, 118),                      # 盤整（60MA ≈ 117.5）
        (1, 113.0, 113.0),                   # 跌破 0.97×60MA（≈114）
        (2, 113.5, 113.8),                   # 低檔兩日（執行日落這裡）
        (40, 114, 126),                      # 站回 60MA → 回補
    ])
    fr = build_frame(ser)
    entry = ser.index[1545]
    res = simulate_trade(fr, entry)
    reasons = [l["reason"] for l in res["legs"]]
    ok("態④減碼" in reasons, "態④減碼腿存在")
    trim = next(l for l in res["legs"] if l["reason"] == "態④減碼")
    trig_d = ser.index[1590]                 # 跌破日
    ok(pd.Timestamp(trim["date"]) > trig_d, f"T+1 執行（觸發 {trig_d.date()} → 執行 {trim['date']}）")
    ok(abs(trim["fraction"] - 0.5) < 1e-6, "一次減至核心 50%（賣出 0.5）")
    ok("態④回補" in reasons, "站回 60MA 且態① → 回補腿存在")


def test_t4_consec3():
    print("[6] 態④ 連 3 日收線下（未破 ×0.97 band）")
    ser = make_series([
        (1500, 50, 100),
        (60, 100, 101),                      # 60MA ≈ 100.5
        (5, 99.0, 98.6),                     # 連續 5 日 < 60MA 但 > 0.97×60MA(≈97.5)
        (30, 99, 104),
    ])
    fr = build_frame(ser)
    res = simulate_trade(fr, ser.index[1520])
    trims = [l for l in res["legs"] if l["reason"] == "態④減碼"]
    ok(len(trims) == 1, "連 3 日確認觸發一次減碼")
    third = ser.index[1562]                  # 第 3 個線下日
    ok(pd.Timestamp(trims[0]["date"]) > third, "第 3 日確認、T+1 執行")


def test_t3_overheat_trim():
    print("[7] 態③ 觸 3σ 減 1/3（一次性）")
    ser = make_series([
        (1500, 50, 100),
        (40, 100, 101),
        (3, 118, 119),                       # 單日 +17% 噴出 ≥ 3σ
        (5, 119, 120),                       # 高檔停留（不得重複減）
        (30, 119, 115),
    ])
    fr = build_frame(ser)
    res = simulate_trade(fr, ser.index[1510])
    t3 = [l for l in res["legs"] if l["reason"] == "態③減1/3"]
    ok(len(t3) == 1, f"觸 3σ 僅減一次（實得 {len(t3)}）")
    ok(abs(t3[0]["fraction"] - 1 / 3) < 1e-3, "減碼量 = 1/3")


def test_t5_full_exit():
    print("[8] 態⑤ 週收盤破 52週線 → 全出、trade 關閉")
    ser = make_series([
        (1500, 50, 100),
        (30, 100, 101),
        (60, 100, 62),                       # 崩跌穿 52週線
        (30, 62, 64),
    ])
    fr = build_frame(ser)
    res = simulate_trade(fr, ser.index[1510])
    ok(res["status"] == "closed", "trade 關閉")
    ok(res["exit_reason"] == "態⑤", "出場原因 = 態⑤")
    exits = [l for l in res["legs"] if l["reason"] == "態⑤全出"]
    ok(len(exits) == 1 and res["current_fraction"] == 0.0, "全出一腿、部位歸零")
    ok(res["ret_pct"] is not None and res["ret_pct"] < 0, "崩跌 trade 報酬為負（誠實記錄）")


def test_t4_staged_ab():
    print("[9] 態④ 階梯參數（backtest A/B 用）：25% + 25%")
    ser = make_series([
        (1500, 50, 100),
        (30, 100, 118),                      # 推升段（遠離 52週線，免觸態⑤）
        (60, 117, 118),                      # 盤整（60MA ≈ 117.5）
        (1, 113.0, 113.0),                   # 破 ×0.97（≈114）→ 第一段 25%
        (3, 112, 111.5),
        (1, 109.0, 109.0),                   # 破 ×0.94（≈110.5）→ 第二段補到核心 50%
        (3, 109, 110),
        (30, 111, 124),
    ])
    fr = build_frame(ser)
    p = dict(PARAMS); p["t4_staged"] = True
    res = simulate_trade(fr, ser.index[1545], params=p)
    trims = [l for l in res["legs"] if l["reason"] == "態④減碼"]
    ok(len(trims) == 2, f"階梯式兩段減碼（實得 {len(trims)}）")
    ok(abs(trims[0]["fraction"] - 0.25) < 1e-3, "第一段賣 25%")
    remaining_after = 1 - trims[0]["fraction"] - trims[1]["fraction"]
    ok(abs(remaining_after - 0.50) < 1e-2, f"兩段後剩餘 ≈ 核心 50%（實得 {remaining_after:.3f}）")


# ── 回放錨（真實資料；引擎 regression 防線）─────────────────────────────────
def test_replay_anchors():
    print("[10] 回放錨 — NVDA / AVGO / 2330 起漲點行為")
    if not WIDE.exists():
        print("  SKIP: 寬表不存在")
        return
    df = pd.read_csv(WIDE, index_col=0, parse_dates=True)

    def events(t):
        fr = build_frame(df[t])
        return scan_ticker(fr, True, []), fr

    ev, _ = events("NVDA")
    a1 = {str(e["date"].date()): e for e in ev if e["type"] == "A1"}
    ok("2023-05-25" in a1, "NVDA A1 2023-05-25 存在")
    ok(abs(a1["2023-05-25"]["base_age_weeks"] - 77) < 3, "NVDA 基期 ≈ 77 週")
    bs = [e for e in ev if e["type"] == "B" and not e["vetoes"]]
    ok(any(str(e["date"].date()) == "2023-08-14" for e in bs),
       "NVDA B 第二班車 2023-08-14 乾淨可進場（A1 被否決後由 B 接）")

    ev, _ = events("AVGO")
    a1 = {str(e["date"].date()): e for e in ev if e["type"] == "A1"}
    ok("2023-05-17" in a1, "AVGO A1 2023-05-17 存在")
    ok(not a1["2023-05-17"]["vetoes"], "AVGO 2023-05-17 五問乾淨直接進場")

    ev, _ = events("2330.TW")
    a1 = {str(e["date"].date()): e for e in ev if e["type"] == "A1"}
    ok("2024-02-15" in a1, "2330 A1 2024-02-15 存在")
    ok("態②過熱" in a1["2024-02-15"]["vetoes"], "2330 2024 突破被態②否決（charter 張力，by design）")
    ok(any(str(e["date"].date()) == "2024-08-09" and not e["vetoes"]
           for e in ev if e["type"] == "B"), "2330 B 第二班車 2024-08-09 接到")
    ok("2022-01-14" in a1, "2330 反例 A1 2022-01-14 存在")
    bad_anchor = a1["2022-01-14"]["date"]
    bs_after_bad = [e for e in ev if e["type"] == "B" and not e["vetoes"]
                    and e["anchor_a1_date"] == bad_anchor]
    ok(len(bs_after_bad) == 0, "2022 反例：回踩破 52週線 → 錨作廢 → 熊市全程空手")


def test_quality_gate():
    print("[11] 四條件閘門欄位語義")
    p, fails, used = quality_check({"eps_fy1_fy3_cagr_pct": 32.3, "roic": 62.1,
                                    "fcf": 18.3, "live_peg": 0.51, "peg": 0.27})
    ok(p is True and used["peg_source"] == "live_peg", "NVDA 樣本 4/4 pass、live_peg 優先")
    p, fails, _ = quality_check({"eps_fy1_fy3_cagr_pct": 10, "roic": 62,
                                 "fcf": 18, "live_peg": 0.5})
    ok(p is False and "CAGR≤15" in fails, "CAGR 10 → fail 標記")
    p, fails, _ = quality_check({"eps_fy1_fy3_cagr_pct": None, "roic": 62,
                                 "fcf": 18, "live_peg": 0.5})
    ok(p is None and fails == ["缺資料"], "缺值 = 不過閘（None）")


if __name__ == "__main__":
    for fn in [test_frozen_no_lookahead, test_a1_vs_a2, test_quality_veto_recorded,
               test_b_second_train, test_t4_band_trim_and_rebuy, test_t4_consec3,
               test_t3_overheat_trim, test_t5_full_exit, test_t4_staged_ab,
               test_replay_anchors, test_quality_gate]:
        fn()
    print(f"\nALL PASS — {N_PASS} 斷言")
