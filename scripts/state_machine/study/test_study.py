#!/usr/bin/env python3
"""合成數據驗證(STUDY §6.4):episode 切分、各變體確認日、M2/M3。"""
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, ".")
from study_trim_variants import (per_ticker_frames, detect_episodes,
                                 confirm_day, measure)

fails = []
def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)

def mk_series(closes, start="2018-01-01"):
    idx = pd.bdate_range(start, periods=len(closes))
    return pd.Series(closes, index=idx, dtype=float)

# 基底:400 根穩定上升(MA60 在價下方),再接情境
base = list(np.linspace(100, 180, 400))

# ── 情境 1:淺回檔(收在 60MA 下 -1%,2 天,然後收復)→ V0 確認、V1 不確認 ──
def scen_shallow():
    c = base.copy()
    # 估 MA60 ≈ 最近 60 根均值;讓兩天收在 ma60*0.99
    s = mk_series(c + [0, 0, 0])  # 占位
    # 先構造:平台讓 MA60 貼近價格,再下穿 1%
    flat = base + [180] * 60
    s = mk_series(flat)
    ma60_now = s.iloc[-60:].mean()
    dip = [ma60_now * 0.995, ma60_now * 0.993]      # 兩天,深度 <3%
    rec = [ma60_now * 1.02] * 15
    s = mk_series(flat + dip + rec)
    fr = per_ticker_frames(s)
    eps = detect_episodes(fr)
    check("情境1: 恰一個 episode", len(eps) == 1, f"got {len(eps)}")
    ep = eps[0]
    check("情境1: 未升級", not ep["escalated"])
    check("情境1: V0 碰觸即確認", confirm_day(fr, ep, "V0")[0][0] == ep["touch_i"])
    check("情境1: V1 不確認(<3% 且 <3日)", confirm_day(fr, ep, "V1") == [])
    r0 = measure(fr, eps, "V0"); r1 = measure(fr, eps, "V1")
    check("情境1: V0 假警報=1", r0["m2_fa"] == 1, str(r0))
    check("情境1: V1 確認數=0", r1["m2_n"] == 0)

# ── 情境 2:急殺穿 -5% 再升級破 52 週線 → V1 條件A 當天確認;M3 量到確認日 ──
def scen_crash():
    flat = base + [180] * 60
    s0 = mk_series(flat)
    ma60_now = s0.iloc[-60:].mean()
    crash = [ma60_now * 0.94]                        # day1 即 < ×0.97
    # 繼續殺到破 52 週線(遠低於價格史 → 殺到 90)
    crash += list(np.linspace(ma60_now * 0.90, 90, 40))
    s = mk_series(flat + crash)
    fr = per_ticker_frames(s)
    eps = detect_episodes(fr)
    check("情境2: 一個 episode", len(eps) == 1, f"got {len(eps)}")
    ep = eps[0]
    check("情境2: 升級態⑤", ep["escalated"])
    c1 = confirm_day(fr, ep, "V1")
    check("情境2: V1 第一天確認(條件A)", c1 and c1[0][0] == ep["touch_i"], str(c1))
    r1 = measure(fr, eps, "V1")
    check("情境2: V1 M3 額外跌幅≈0(同日確認)", r1["m3"] and abs(r1["m3"][0]) < 1e-9, str(r1["m3"]))

# ── 情境 3:陰跌(-1%/日 × 5 日)→ V1 第 3 日確認(條件B) ──
def scen_bleed():
    flat = base + [180] * 60
    s0 = mk_series(flat)
    ma = s0.iloc[-60:].mean()
    bleed = [ma * (0.995 - 0.004 * k) for k in range(5)]   # 全部 > ×0.97? 0.995,0.991,0.987... 第3日 0.987 > 0.97 ✓
    rec = [ma * 1.02] * 15
    s = mk_series(flat + bleed + rec)
    fr = per_ticker_frames(s)
    eps = detect_episodes(fr)
    ep = eps[0]
    c1 = confirm_day(fr, ep, "V1")
    check("情境3: V1 第 3 日確認(條件B)", c1 and c1[0][0] == ep["touch_i"] + 2, str(c1))

# ── 情境 4:V3 延伸度資格 ──
def scen_ext():
    flat = base + [180] * 60
    s0 = mk_series(flat)
    ma = s0.iloc[-60:].mean()
    dip = [ma * 0.99] * 2 + [ma * 1.02] * 15
    s = mk_series(flat + dip)
    fr = per_ticker_frames(s)
    eps = detect_episodes(fr)
    ep = eps[0]
    ext = ep["ext_at_touch"]
    c_hi = confirm_day(fr, ep, "V3", 0.01)    # 門檻 1% → 必過 → 確認
    c_lo = confirm_day(fr, ep, "V3", ext + 0.10)  # 門檻高於實際延伸 → 不確認
    check("情境4: 延伸足夠→V3 確認", c_hi != [], str(ext))
    check("情境4: 延伸不足→V3 不確認", c_lo == [])

# ── 情境 5:V4 只在週末 bucket 端點確認 ──
def scen_weekly():
    flat = base + [180] * 60
    s0 = mk_series(flat)
    ma = s0.iloc[-60:].mean()
    dip = [ma * 0.95] * 8 + [ma * 1.02] * 10   # 8 天在線下,必含一個週五
    s = mk_series(flat + dip)
    fr = per_ticker_frames(s)
    eps = detect_episodes(fr)
    ep = eps[0]
    c4 = confirm_day(fr, ep, "V4")
    check("情境5: V4 有確認", c4 != [])
    if c4:
        d = fr["close"].index[c4[0][0]]
        check("情境5: 確認日=週末端點", d in fr["wclose"].index, str(d))
        check("情境5: 確認日不早於碰觸", c4[0][0] >= ep["touch_i"])

for t in (scen_shallow, scen_crash, scen_bleed, scen_ext, scen_weekly):
    print(t.__doc__ or t.__name__)
    t()
print()
print("❌ FAIL:" + str(fails) if fails else "✅ 合成驗證全綠")
sys.exit(1 if fails else 0)
