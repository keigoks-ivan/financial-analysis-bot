#!/usr/bin/env python3
"""GLD 黃金 · W52×自適應波動率 sleeve — 前瞻 OOS 追蹤頁產生器（fab-only）。

定位（§11，凍結 2026-07-23）：**候選追蹤、尚非實單**。單腿 GLD、cap 1.0（研究
規格、不上槓桿）；引擎＝W52 週線閘門 × 自適應 σ(756/min252) × A2 執行層（單資產
語意：滿載 100pp、門檻 20pp、格 10%、clamp 100；整數 pp 空間）。骨架比照
update_long_track_w52_adaptive.py（單市場單腿化）。

閘門對齊 run_w52_adaptive.gate_w52；套袖對齊 run_adaptive_sigma.vt_weight_adaptive_median
(n_days=756)；A2 對齊 nonequity signals.a2_exec_single(cap=1.0)。回測基線區數字轉錄自
v7-backtest results/nonequity/{nonequity,gold_longsample}.json（CI 只在 fab、無跨 repo
讀檔，故凍結轉錄為常數）。756 日回填＋日增歷史；回放（replay）與實錄（live）以
source 欄位區分，圖上虛線／實線區隔（誠實紀律，回放不偽裝實錄）。

用法：python3 scripts/update_long_track_gld.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# ---- nav import ------------------------------------------------------------
HERE = Path(__file__).resolve().parent
for _p in (HERE, HERE.parents[2] if len(HERE.parents) >= 3 else HERE):
    sys.path.insert(0, str(_p))
try:
    from site_nav import full_nav_block
except ImportError:
    from site_nav_snippet import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "lthub")

_cand = [HERE.parent / "docs", HERE.parents[2] / "docs" if len(HERE.parents) >= 3 else HERE / "docs"]
DOCS = next((c for c in _cand if c.exists()), _cand[0])
OUTPUT = DOCS / "long-track-gld" / "index.html"
STATE_JSON = DOCS / "long-track-gld" / "state.json"
ALERT_FILE = DOCS.parent / "lt_gld_alert.txt"    # gate 翻轉或 |target−executed| ≥ 20pp 才寫

# ---- config (凍結，§11) ----------------------------------------------------
TICKER = "GLD"
YF_SYMBOL = "GLD"
MED_WIN = 756                     # 自適應中位數視窗（3 年），凍結
MIN_PERIODS = 252                 # 首年 expanding
FREEZE_DATE = "2026-07-23"
BACKFILL_DAYS = 756
HISTORY_CAP = 820

# A2 執行層（單資產語意）：滿載 100pp、門檻 20pp、格 10%、clamp 100。整數 pp 空間比較。
CAP = 1.0                         # 研究規格，不上槓桿
EXEC_BAND = 20.0
EXEC_GRID = 10.0
EXEC_CLAMP = 100.0 * CAP          # 單資產＝整個組合，滿載 100pp

# ---- 凍結回測基線（轉錄自 nonequity.json / gold_longsample.json，§11 頁面規格）----
BT_ROWS = [   # (label, cagr%, mdd%, calmar, martin, ui, adj/yr, in_market%)
    ("B&H 買進持有", 9.36, -45.6, 0.205, 0.43, 21.6, 0.0, 100.0),
    ("W52 閘門無套袖", 7.55, -30.7, 0.246, 0.43, 17.6, 2.9, 68.2),
    ("W52×自適應 每日（理論對照）", 7.12, -26.9, 0.265, 0.50, 14.3, 92.8, 68.2),
    ("W52×自適應＋A2 執行層（主列）", 7.51, -26.2, 0.287, 0.53, 14.2, 6.2, 68.2),
    ("12M TSMOM（月頻）", 7.07, -33.7, 0.210, 0.37, 19.1, 1.9, 65.6),
    ("Faber 10M SMA（月頻）", 6.49, -41.8, 0.155, 0.27, 23.7, 1.8, 68.6),
]
BT_WINDOW = ["2006-06-01", "2026-07-22"]
GOLD_LS = {   # gold_longsample.json 摘要
    "window": ["1976-07-01", "2026-07-22"],
    "full": {"bh": (6.84, -72.6, 0.094), "w52": (8.77, -43.4, 0.202), "main": (9.00, -26.2, 0.344)},
    "crit_bh": (-3.73, -72.6), "crit_main": (5.14, -21.7),
    "in_market": 37.9, "cash_contrib": 5.07, "shallower_pp": 50.85, "pass": True,
}
# 主列月度 NAV（正規化 1.0；轉錄 nonequity.json GLD monthly_nav_main）——INJECT 佔位
BT_NAV_LABELS = ["2006-06", "2006-07", "2006-08", "2006-09", "2006-10", "2006-11", "2006-12", "2007-01", "2007-02", "2007-03", "2007-04", "2007-05", "2007-06", "2007-07", "2007-08", "2007-09", "2007-10", "2007-11", "2007-12", "2008-01", "2008-02", "2008-03", "2008-04", "2008-05", "2008-06", "2008-07", "2008-08", "2008-09", "2008-10", "2008-11", "2008-12", "2009-01", "2009-02", "2009-03", "2009-04", "2009-05", "2009-06", "2009-07", "2009-08", "2009-09", "2009-10", "2009-11", "2009-12", "2010-01", "2010-02", "2010-03", "2010-04", "2010-05", "2010-06", "2010-07", "2010-08", "2010-09", "2010-10", "2010-11", "2010-12", "2011-01", "2011-02", "2011-03", "2011-04", "2011-05", "2011-06", "2011-07", "2011-08", "2011-09", "2011-10", "2011-11", "2011-12", "2012-01", "2012-02", "2012-03", "2012-04", "2012-05", "2012-06", "2012-07", "2012-08", "2012-09", "2012-10", "2012-11", "2012-12", "2013-01", "2013-02", "2013-03", "2013-04", "2013-05", "2013-06", "2013-07", "2013-08", "2013-09", "2013-10", "2013-11", "2013-12", "2014-01", "2014-02", "2014-03", "2014-04", "2014-05", "2014-06", "2014-07", "2014-08", "2014-09", "2014-10", "2014-11", "2014-12", "2015-01", "2015-02", "2015-03", "2015-04", "2015-05", "2015-06", "2015-07", "2015-08", "2015-09", "2015-10", "2015-11", "2015-12", "2016-01", "2016-02", "2016-03", "2016-04", "2016-05", "2016-06", "2016-07", "2016-08", "2016-09", "2016-10", "2016-11", "2016-12", "2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06", "2017-07", "2017-08", "2017-09", "2017-10", "2017-11", "2017-12", "2018-01", "2018-02", "2018-03", "2018-04", "2018-05", "2018-06", "2018-07", "2018-08", "2018-09", "2018-10", "2018-11", "2018-12", "2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07", "2019-08", "2019-09", "2019-10", "2019-11", "2019-12", "2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06", "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12", "2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09", "2021-10", "2021-11", "2021-12", "2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06", "2022-07", "2022-08", "2022-09", "2022-10", "2022-11", "2022-12", "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07"]
BT_NAV = [1.0, 1.0182, 1.0139, 0.983, 0.9697, 1.0307, 1.0118, 1.0082, 1.0317, 1.0231, 1.0424, 1.0211, 1.0037, 1.0254, 1.036, 1.1341, 1.2054, 1.1969, 1.2454, 1.3411, 1.4044, 1.3276, 1.29, 1.2994, 1.3414, 1.3183, 1.2008, 1.1796, 1.1757, 1.1759, 1.1759, 1.1483, 1.1606, 1.1406, 1.0862, 1.1975, 1.1349, 1.162, 1.1626, 1.2305, 1.2763, 1.4396, 1.3398, 1.319, 1.3622, 1.3562, 1.436, 1.4798, 1.5147, 1.4376, 1.5197, 1.5923, 1.6509, 1.6858, 1.7268, 1.6167, 1.7136, 1.741, 1.8968, 1.8628, 1.8175, 1.9705, 2.1735, 2.052, 2.1364, 2.1656, 1.9795, 2.1556, 2.0982, 2.0873, 2.0728, 2.0729, 2.073, 2.0732, 2.1086, 2.2072, 2.1422, 2.1322, 2.061, 2.0156, 2.0157, 2.0159, 2.016, 2.016, 2.0161, 2.0162, 2.0162, 2.0162, 2.0163, 2.0164, 2.0165, 2.0165, 2.0166, 1.9303, 1.9303, 1.9303, 1.9471, 1.8764, 1.8334, 1.8334, 1.8334, 1.8335, 1.8335, 1.8236, 1.7721, 1.7722, 1.7722, 1.7722, 1.7722, 1.7722, 1.7723, 1.7723, 1.7724, 1.7725, 1.7728, 1.7731, 1.8459, 1.8335, 1.9224, 1.8044, 1.9669, 2.0081, 1.9427, 1.9561, 1.8985, 1.8068, 1.8075, 1.8082, 1.8089, 1.8101, 1.7792, 1.7253, 1.6934, 1.7137, 1.7857, 1.7255, 1.7126, 1.7187, 1.6992, 1.7542, 1.7177, 1.7286, 1.7121, 1.6801, 1.6713, 1.674, 1.6771, 1.6798, 1.6832, 1.6864, 1.6882, 1.737, 1.7264, 1.6988, 1.6875, 1.7172, 1.8535, 1.8493, 1.9374, 1.8994, 1.9401, 1.8779, 1.9465, 2.0341, 2.0437, 2.0684, 2.128, 2.1531, 2.1889, 2.4179, 2.3969, 2.3253, 2.316, 2.2511, 2.3444, 2.2921, 2.2626, 2.2627, 2.2627, 2.3088, 2.154, 2.1541, 2.1542, 2.1542, 2.1543, 2.1029, 2.1305, 2.0764, 2.1759, 2.2246, 2.1838, 2.0909, 2.085, 2.0886, 2.0935, 2.0988, 2.1051, 2.1123, 2.1197, 2.2221, 2.0921, 2.2349, 2.2521, 2.2219, 2.1725, 2.2222, 2.1938, 2.0894, 2.1272, 2.1902, 2.2183, 2.1867, 2.1967, 2.3872, 2.4698, 2.4802, 2.4748, 2.5879, 2.6312, 2.7632, 2.882, 2.7929, 2.7682, 2.9561, 3.0099, 3.2944, 3.4463, 3.4535, 3.44, 3.4123, 3.5663, 3.9441, 4.1254, 4.2618, 4.3589, 4.7395, 4.7951, 4.6136, 4.5867, 4.5424, 4.3572, 4.3668]


# ═══════════════════════════════════════════════════════════════════
# 引擎（逐位元對齊凍結回測構件）
# ═══════════════════════════════════════════════════════════════════
def fetch_close(ticker: str = YF_SYMBOL) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 13)
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    c = c.dropna()
    if getattr(c.index, "tz", None) is not None:
        c.index = c.index.tz_localize(None)
    return c


def _gate_core(px: pd.Series):
    """W52 單線閘門（週收 > SMA52w 在場、否則出場；W-FRI，無滯後）。對齊 gate_w52。"""
    wk = px.resample("W-FRI").last().dropna()
    w52 = wk.rolling(52).mean()
    w104 = wk.rolling(104).mean()
    w250 = wk.rolling(250).mean()
    s104 = w104 - w104.shift(4)
    s250 = w250 - w250.shift(4)
    pos = (wk > w52).astype(int)
    pos[w52.isna()] = 0
    return wk, pos.astype(int), w52, w104, w250, s104, s250


def gate_state(px: pd.Series) -> dict:
    wk, pos, w52, w104, w250, s104, s250 = _gate_core(px)
    recent = []
    for i in range(-8, 0):
        recent.append({
            "date": wk.index[i].strftime("%Y-%m-%d"), "close": float(wk.iloc[i]),
            "w52": float(w52.iloc[i]) if not pd.isna(w52.iloc[i]) else None,
            "w104": float(w104.iloc[i]) if not pd.isna(w104.iloc[i]) else None,
            "w250": float(w250.iloc[i]) if not pd.isna(w250.iloc[i]) else None,
            "s104_pos": bool(s104.iloc[i] > 0) if not pd.isna(s104.iloc[i]) else None,
            "s250_pos": bool(s250.iloc[i] > 0) if not pd.isna(s250.iloc[i]) else None,
            "in": bool(pos.iloc[i]),
        })
    return {"gate": bool(pos.iloc[-1]), "wk_date": wk.index[-1].strftime("%Y-%m-%d"),
            "wk_close": float(wk.iloc[-1]), "w52": float(w52.iloc[-1]),
            "w104": float(w104.iloc[-1]), "w250": float(w250.iloc[-1]),
            "s104_pos": bool(s104.iloc[-1] > 0), "s250_pos": bool(s250.iloc[-1] > 0),
            "recent": recent}


def _sleeve_from(px: pd.Series, win: int = 20):
    """σ_t ＝ RV20 rolling(756,min252).median；raw ＝ σ_t/RV20；w＝clip(raw, upper=CAP=1.0)。"""
    lr = np.log(px / px.shift(1))
    rv = lr.rolling(win).std() * np.sqrt(252)
    sigma = rv.rolling(MED_WIN, min_periods=MIN_PERIODS).median()
    rv_now, sig_now = float(rv.iloc[-1]), float(sigma.iloc[-1])
    if rv_now > 0 and not np.isnan(sig_now):
        raw = sig_now / rv_now
        w = min(CAP, raw)
    else:
        raw, w = 1.0, 1.0
        if np.isnan(sig_now):
            sig_now = rv_now
    return rv_now, sig_now, w, raw


def sleeve_state(px: pd.Series) -> dict:
    rv_now, sig_now, w, raw = _sleeve_from(px)
    return {"rv20": rv_now, "sigma_t": sig_now, "sleeve": w, "raw_ratio": raw}


def compute(px: pd.Series) -> dict:
    g = gate_state(px)
    s = sleeve_state(px)
    fill = (1 if g["gate"] else 0) * s["sleeve"]      # 0..1（單資產整個組合）
    return {**g, **s, "final": fill}                   # final ＝ gate×sleeve（0..1）


# ---- history: rule-replay backfill（source 標記回放 vs 實錄）----------------
def _daily_record(px: pd.Series, d: pd.Timestamp, source: str) -> dict:
    pxd = px.loc[:d]
    _, pos, *_ = _gate_core(pxd)
    gate = bool(pos.iloc[-1])
    rv_now, sig_now, sleeve, raw = _sleeve_from(pxd)
    final = (1 if gate else 0) * sleeve
    return {"date": d.strftime("%Y-%m-%d"), "source": source, "gate": gate,
            "rv20_pct": round(rv_now * 100, 2), "sigma_t_pct": round(sig_now * 100, 2),
            "raw_ratio": round(raw, 4), "sleeve": round(sleeve, 4),
            "final_pct": round(final * 100, 1)}        # 0..100pp（單資產滿載 100）


def build_backfill(px: pd.Series, n_days: int = BACKFILL_DAYS) -> list:
    dates = px.index.sort_values()[-n_days:]
    return [_daily_record(px, d, "replay") for d in dates]


def merge_history(prev_history: list, backfill: list, today_rec: dict,
                  cap: int = HISTORY_CAP) -> list:
    by_date = {r["date"]: r for r in (prev_history or [])}
    for r in backfill:
        by_date.setdefault(r["date"], r)
    by_date[today_rec["date"]] = today_rec
    out = [by_date[k] for k in sorted(by_date)]
    return out[-cap:]


def band_exec_replay(history: list) -> dict:
    """A2 單資產重放：executed 初始 0，逐日若 |target − executed| ≥ 20pp 則
    executed = min(round(target/10)×10, 100)，否則不變。整數 pp 空間比較。"""
    executed, events = [], []
    cur, prev_gate = 0.0, None
    for r in history:
        target, gate = r["final_pct"], bool(r["gate"])
        if abs(target - cur) >= EXEC_BAND:
            new = min(round(target / EXEC_GRID) * EXEC_GRID, EXEC_CLAMP)
            if new != cur:
                flipped = prev_gate is not None and gate != prev_gate
                events.append({"date": r["date"], "from": cur, "to": new,
                               "reason": "閘門翻轉" if flipped else "波動調整"})
                cur = new
        executed.append(cur)
        prev_gate = gate
    return {"executed": executed, "events": events,
            "last": executed[-1] if executed else 0.0}


def detect_changes(prev: dict, sig: dict) -> str | None:
    """可行動變化＝閘門翻轉，或 |今日目標 − 現持（executed_pct）| ≥ 20pp。"""
    if not prev:
        return None
    gate_flip = bool(prev.get("gate")) != bool(sig["gate"])
    target = round(sig["final"] * 100, 1)
    held = prev.get("executed_pct")
    drift = held is not None and abs(target - held) >= EXEC_BAND
    if not (gate_flip or drift):
        return None
    new_exec = min(round(target / EXEC_GRID) * EXEC_GRID, EXEC_CLAMP)
    parts = []
    if gate_flip:
        parts.append("閘門 " + ("出場→在場" if sig["gate"] else "在場→出場"))
    arrow = (f"最終權重 {held:.0f}% → {new_exec:.0f}%" if held is not None
             else f"最終權重 → {new_exec:.0f}%")
    return f"{('、'.join(parts) + ' → ') if parts else ''}{arrow}"


# ═══════════════════════════════════════════════════════════════════
# HTML
# ═══════════════════════════════════════════════════════════════════
def _mn(s):
    return str(s).replace("-", "−")


def fmt_pct(v, dp=1, sign=False):
    s = f"{v:+.{dp}f}" if sign else f"{v:.{dp}f}"
    return _mn(s) + "%"


def signal_card(sig: dict, executed: float) -> str:
    gate = sig["gate"]
    gcls = "gin" if gate else "gout"
    gtxt = "在場（週收 &gt; SMA52w）" if gate else "出場（週收 &lt; SMA52w）"
    return (
        '<div class="sigcard">'
        f'<div class="sig-gate {gcls}">閘門：{gtxt}</div>'
        '<div class="sig-grid">'
        f'<div class="sig-c"><span>RV20（年化）</span><b>{fmt_pct(sig["rv20"]*100)}</b></div>'
        f'<div class="sig-c"><span>σ_t（3年中位）</span><b>{fmt_pct(sig["sigma_t"]*100)}</b></div>'
        f'<div class="sig-c"><span>raw ＝ σ_t/RV20</span><b>{_mn(round(sig["raw_ratio"],3))}</b></div>'
        f'<div class="sig-c"><span>套袖 sleeve（clip 1.0）</span><b>{_mn(round(sig["sleeve"],3))}</b></div>'
        f'<div class="sig-c hl"><span>今日目標權重</span><b>{fmt_pct(sig["final"]*100,0)}</b></div>'
        f'<div class="sig-c hl"><span>A2 執行後現持</span><b>{fmt_pct(executed,0)}</b></div>'
        '</div></div>')


def recent_table(sig: dict) -> str:
    rows = ""
    for r in sig["recent"]:
        rows += (f'<tr><td>{_mn(r["date"])}</td><td class="num">{_mn(round(r["close"],2))}</td>'
                 f'<td class="num">{_mn(round(r["w52"],2)) if r["w52"] else "—"}</td>'
                 f'<td class="ctr">{"● 在場" if r["in"] else "○ 出場"}</td></tr>')
    return ('<div class="tbl-wrap"><table><thead><tr><th>週（W-FRI）</th>'
            '<th class="num">週收</th><th class="num">SMA52w</th><th class="ctr">閘門</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>')


def events_card(events: list) -> str:
    if not events:
        return ('<p class="fine">近 3 年回放窗內無 A2 執行事件（曝險未達 20pp 門檻變動）。</p>')
    rows = ""
    for e in events[-12:][::-1]:
        rows += (f'<tr><td>{_mn(e["date"])}</td>'
                 f'<td class="num">{fmt_pct(e["from"],0)} → {fmt_pct(e["to"],0)}</td>'
                 f'<td>{e["reason"]}</td></tr>')
    return ('<div class="tbl-wrap"><table><thead><tr><th>日期</th>'
            '<th class="num">現持變動</th><th>原因</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'<p class="fine">近 3 年回放窗共 {len(events)} 次 A2 執行事件（顯示最近 12 次）。'
            '｜門檻 20pp、取整 10%、clamp 100pp。</p>')


def backtest_section() -> str:
    rows = ""
    for lab, cagr, mdd, cal, mar, ui, adj, inm in BT_ROWS:
        cls = ' class="rowhl"' if "主列" in lab else (' class="rowbh"' if "B&H" in lab else "")
        rows += (f'<tr{cls}><td>{lab}</td><td class="num">{fmt_pct(cagr,2)}</td>'
                 f'<td class="num neg">{fmt_pct(mdd,1)}</td><td class="num">{_mn(cal)}</td>'
                 f'<td class="num">{_mn(mar)}</td><td class="num">{_mn(ui)}</td>'
                 f'<td class="num">{_mn(adj)}</td><td class="num">{fmt_pct(inm,0)}</td></tr>')
    g = GOLD_LS
    return (
        '<div class="section"><h2 class="section-title">凍結回測基線（研究規格 cap 1.0）</h2>'
        f'<div class="section-sub">六列方法矩陣（窗 {_mn(BT_WINDOW[0])} ～ {_mn(BT_WINDOW[1])}），'
        '轉錄自預註冊回測 <code>results/nonequity/nonequity.json</code>；主列＝W52×自適應＋A2。'
        '數字凍結、與本追蹤頁同規則。</div>'
        '<div class="card"><h3>GLD 方法矩陣</h3><div class="tbl-wrap"><table>'
        '<thead><tr><th>配置</th><th class="num">CAGR</th><th class="num">MDD</th>'
        '<th class="num">Calmar</th><th class="num">Martin</th><th class="num">Ulcer</th>'
        '<th class="num">調整/年</th><th class="num">平均在場</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div></div>'
        '<div class="card"><h3>主列月度 NAV（對數軸，正規化 1×）</h3>'
        '<div class="chart-wrap"><canvas id="chart-bt-nav"></canvas></div></div>'
        f'<div class="good-loud"><b>長樣本壓力測試通過（1976-2026，含 1980-2000 二十年熊市）：</b>'
        f'全窗主列 Calmar {_mn(g["full"]["main"][2])} ≥ B&amp;H {_mn(g["full"]["bh"][2])}；'
        f'判準塊 1980-2000 主列 {fmt_pct(g["crit_main"][0],2,True)}/{fmt_pct(g["crit_main"][1],1)}'
        f'（在場 {fmt_pct(g["in_market"],1)}、現金貢獻 {fmt_pct(g["cash_contrib"],2,True)}/年）'
        f'vs 傻抱 {fmt_pct(g["crit_bh"][0],2,True)}/{fmt_pct(g["crit_bh"][1],1)}'
        f'（MDD 淺 {_mn(g["shallower_pp"])}pp）。凍結引擎讓持有人帶正報酬、淺回撤活著穿過'
        '黃金史上最嚴苛的二十年長熊。</div>'
        '<p class="fine">完整回測、判準四燈、鄰域穩健性、DBC/GEM 對照與長樣本詳表見 '
        '<a href="/backtest/nonequity/">決策前研究頁 /backtest/nonequity/</a>。</p></div>')


def kill_section() -> str:
    return (
        '<div class="section"><h2 class="section-title">預註冊 kill／複審條款（事前凍結，§11.2）</h2>'
        '<div class="killbox"><ol>'
        '<li><b>滾動 3 年 Calmar &lt; 同窗 GLD B&amp;H Calmar</b> → 觸發複審；</li>'
        '<li><b>與美股實單系統 36 月滾動相關 &gt; 0.5 且持續 ≥ 3 個月</b>（分散前提失效）→ 觸發複審；</li>'
        '<li>若日後進實單：上線後 <b>60 交易日複審點</b>（比照 2026-07-18 切換決策慣例）。</li>'
        '</ol>'
        '<p class="killnote"><b>觸發＝人工複審、不自動平倉</b>；條款<b>不得因績效難看而事後放寬</b>。</p>'
        '</div></div>')


def generate_html(sig: dict, change: str | None, last_change_date: str | None,
                  history: list, exec_replay: dict) -> str:
    executed = exec_replay["last"]
    # 曝險歷史：target（final_pct）vs executed，回放/實錄以 source 區分
    labels = [r["date"] for r in history]
    target_series = [r["final_pct"] for r in history]
    exec_series = exec_replay["executed"]
    live_from = next((i for i, r in enumerate(history) if r["source"] == "live"), len(history) - 1)

    banner = ('<div class="oos-banner">⚠ <b>前瞻 OOS 追蹤中・尚非實單</b>'
              '——本頁為 GLD 金 sleeve 的<b>候選追蹤</b>（決策前研究通過後開始紙上前瞻紀錄），'
              '<b>非實際持倉</b>。實單非股票部位目前為 0%。</div>')

    plain = ('<div class="plain-box"><span class="pb-tag">💬 白話</span><span class="pb-body">'
             '這頁在做什麼：把「決策前研究」裡驗證過的<b>黃金持有規則</b>（趨勢紅綠燈＋看波動'
             '決定押多少＋低頻執行），從今天起<b>每個交易日照跑一次、紙上記錄</b>，看它真的上線'
             '前的表現。<b>目前一毛錢都還沒進去</b>——這是「上線前的前瞻測試」，不是已經在買。'
             '綠燈才持有、紅燈退到現金領利息；目標權重只在變動 ≥ 20pp 時才調（低頻）。</span></div>')

    chg = ""
    if change:
        chg = (f'<div class="change-flag">⚡ 今日可行動變化（{_mn(last_change_date)}）：'
               f'{change}</div>')
    elif last_change_date:
        chg = (f'<p class="fine">上次可行動變化：{_mn(last_change_date)}。'
               '今日無新可行動變化。</p>')

    body = (banner + plain + chg +
            '<div class="section"><h2 class="section-title">當日訊號（GLD）</h2>' +
            signal_card(sig, executed) +
            f'<p class="fine">數據截至週線 {_mn(sig["wk_date"])}（W-FRI）。目標權重＝閘門(0/1)×套袖'
            '（cap 1.0）；A2 執行層：|目標−現持| ≥ 20pp 才調整、取整 10%、clamp 100pp。</p></div>' +
            '<div class="section"><h2 class="section-title">近三年曝險（回放＋實錄）</h2>'
            '<div class="section-sub">粗階梯＝A2 執行後現持；細線＝每日理論目標。'
            '回放段（規則重演）以虛線、實錄段以實線區分——回放不偽裝成實錄。</div>'
            '<div class="card"><div class="chart-wrap"><canvas id="chart-expo"></canvas></div></div>' +
            '<div class="card"><h3>A2 執行事件</h3>' + events_card(exec_replay["events"]) + '</div></div>' +
            '<div class="section"><h2 class="section-title">近期週閘門</h2>' +
            recent_table(sig) + '</div>' +
            backtest_section() + kill_section())

    js = f"""
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;
var EXPO={{labels:{json.dumps(labels)},tgt:{json.dumps(target_series)},exe:{json.dumps(exec_series)},live:{live_from}}};
(function(){{
 var tgtReplay=EXPO.tgt.map(function(v,i){{return i<=EXPO.live?v:null}});
 var tgtLive=EXPO.tgt.map(function(v,i){{return i>=EXPO.live?v:null}});
 var exeReplay=EXPO.exe.map(function(v,i){{return i<=EXPO.live?v:null}});
 var exeLive=EXPO.exe.map(function(v,i){{return i>=EXPO.live?v:null}});
 new Chart(document.getElementById('chart-expo'),{{type:'line',data:{{labels:EXPO.labels,datasets:[
  {{label:'A2 執行後現持（回放）',data:exeReplay,borderColor:'#d97706',borderWidth:2.2,stepped:true,pointRadius:0,borderDash:[5,3]}},
  {{label:'A2 執行後現持（實錄）',data:exeLive,borderColor:'#d97706',borderWidth:2.4,stepped:true,pointRadius:0}},
  {{label:'每日理論目標（回放）',data:tgtReplay,borderColor:'rgba(180,120,10,0.35)',borderWidth:1,pointRadius:0,borderDash:[2,2]}},
  {{label:'每日理論目標（實錄）',data:tgtLive,borderColor:'rgba(180,120,10,0.45)',borderWidth:1,pointRadius:0}}
 ]}},options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
  plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:8,font:{{size:10}}}}}},
   tooltip:{{callbacks:{{label:function(c){{return c.parsed.y==null?null:c.dataset.label+': '+c.parsed.y.toFixed(0)+'%'}}}}}}}},
  scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:10,font:{{size:9}},maxRotation:0,autoSkip:true}}}},
   y:{{beginAtZero:true,suggestedMax:100,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:9}}}}}}}}}}}});
}})();
var BTNAV={{labels:{json.dumps(BT_NAV_LABELS)},nav:{json.dumps(BT_NAV)}}};
new Chart(document.getElementById('chart-bt-nav'),{{type:'line',data:{{labels:BTNAV.labels,datasets:[
  {{label:'主列 W52×自適應＋A2',data:BTNAV.nav,borderColor:'#1a56db',borderWidth:2.2,pointRadius:0,tension:0.1}}]}},
 options:{{responsive:true,maintainAspectRatio:false,
  plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',font:{{size:10}}}}}},
   tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(2)+'×'}}}}}}}},
  scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:9,font:{{size:9}},maxRotation:0,autoSkip:true}}}},
   y:{{type:'logarithmic',grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{font:{{size:9}},callback:function(v){{return v+'×'}}}}}}}}}}}});
"""
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GLD 黃金 · W52×自適應波動率 sleeve（前瞻 OOS 追蹤）| InvestMQuest</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>{CSS}</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / <a href="/long-track/">前瞻追蹤</a> / GLD 金 sleeve</div>
  <h1>GLD 黃金 · W52×自適應波動率 sleeve</h1>
  <div class="sub">前瞻 OOS 追蹤（候選・尚非實單）· 單腿 GLD · cap 1.0（不上槓桿）· W52 閘門 × 自適應 σ(756) × A2 執行層 · 規則凍結 {FREEZE_DATE}</div>
</div></div>
<div class="container">
{body}
</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · GLD 金 sleeve 前瞻 OOS 追蹤（候選、非實單）· 規則凍結 {FREEZE_DATE} · 僅供研究參考</div></footer>
<script>
{js}
</script>
</body>
</html>"""


CSS = """
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.6rem 0 1.1rem;background:linear-gradient(180deg,#fffbeb 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.5rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.88rem;margin-top:.25rem;max-width:76ch}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}.crumb a{color:var(--muted)}
.oos-banner{background:var(--amber-bg);border:2px solid var(--amber);border-radius:10px;padding:.9rem 1.15rem;margin:1.1rem 0 .4rem;font-size:.92rem;color:var(--amber-text)}
.oos-banner b{color:#b45309}
.plain-box{display:flex;gap:.6rem;background:#f0f7ff;border:1px solid #cfe3fb;border-left:4px solid #3b82f6;border-radius:8px;padding:.7rem .9rem;margin:.6rem 0;font-size:.86rem;line-height:1.68}
.pb-tag{flex:0 0 auto;font-size:.72rem;font-weight:700;color:#1e40af;background:#dbeafe;border-radius:6px;padding:.15rem .45rem;height:fit-content;white-space:nowrap}
.pb-body{color:#1e3a5f}.pb-body b{color:#1e40af}
.change-flag{background:var(--red-bg);border:1px solid var(--red-border);border-radius:8px;padding:.7rem 1rem;margin:.6rem 0;font-size:.9rem;color:#991b1b;font-weight:600}
.section{padding:1.6rem 0 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:1rem;padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.85rem;color:var(--muted);margin:-.5rem 0 1rem;max-width:84ch}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.2rem;margin-bottom:1rem}
.card h3{font-size:1rem;font-weight:600;margin-bottom:.8rem}
.fine{font-size:.8rem;color:var(--muted);margin-top:.55rem;line-height:1.7}
.sigcard{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem 1.2rem;margin-bottom:.5rem}
.sig-gate{font-size:1.05rem;font-weight:700;padding:.5rem .8rem;border-radius:8px;margin-bottom:.9rem}
.gin{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.gout{background:#f3f4f6;color:var(--muted);border:1px solid var(--border)}
.sig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}
@media(max-width:640px){.sig-grid{grid-template-columns:repeat(2,1fr)}}
.sig-c{background:#f9fafb;border:1px solid var(--border);border-radius:8px;padding:.65rem .8rem}
.sig-c span{display:block;font-size:.72rem;color:var(--muted);margin-bottom:.2rem}
.sig-c b{font-size:1.15rem;font-variant-numeric:tabular-nums}
.sig-c.hl{background:var(--brand-light);border-color:#bfdbfe}.sig-c.hl b{color:var(--brand)}
table{width:100%;border-collapse:collapse;font-size:.86rem}
th,td{text-align:left;padding:.5rem .65rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.74rem;color:var(--muted)}
td{font-variant-numeric:tabular-nums}td.num,th.num{text-align:right}td.ctr,th.ctr{text-align:center}
tbody tr:hover td{background:#f3f4f6}.neg{color:var(--red);font-weight:600}
.rowhl td{background:var(--brand-light)!important}.rowbh td{background:#f9fafb;color:var(--muted)}
.tbl-wrap{overflow-x:auto}
.chart-wrap{position:relative;width:100%;height:300px}
.good-loud{background:var(--green-bg);border:2px solid var(--green-border);border-radius:8px;padding:1rem 1.2rem;font-size:.9rem;color:var(--green-text);margin:1rem 0}
.good-loud b{color:var(--green)}
.killbox{background:#fff7ed;border:2px solid var(--amber-border);border-radius:10px;padding:1rem 1.3rem}
.killbox ol{margin:.2rem 0 .2rem 1.2rem;font-size:.9rem;line-height:1.9}
.killnote{margin-top:.7rem;font-size:.88rem;color:var(--amber-text);font-weight:600}
code{background:#f3f4f6;padding:.05rem .3rem;border-radius:4px;font-size:.85em}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){table{font-size:.78rem}th,td{padding:.4rem .4rem}}
"""


def main():
    prev_state = {}
    if STATE_JSON.exists():
        try:
            prev_state = json.loads(STATE_JSON.read_text())
        except Exception:
            prev_state = {}

    print(f"Fetching {YF_SYMBOL}...")
    px = fetch_close()
    sig = compute(px)
    print(f"  GLD: gate={'IN' if sig['gate'] else 'OUT'} RV20={sig['rv20']*100:.1f}% "
          f"σ_t={sig['sigma_t']*100:.1f}% sleeve={sig['sleeve']:.3f} -> target {sig['final']*100:.0f}%")

    change = detect_changes(prev_state, sig)
    data_date = sig["wk_date"]

    prev_history = prev_state.get("history", [])
    backfill = build_backfill(px) if len(prev_history) < BACKFILL_DAYS else []
    today_rec = _daily_record(px, px.index[-1], "live")
    history = merge_history(prev_history, backfill, today_rec)
    print(f"History: {len(history)} days (backfill {len(backfill)}, "
          f"span {history[0]['date']}→{history[-1]['date']})")

    exec_replay = band_exec_replay(history)
    executed = exec_replay["last"]
    print(f"Exec layer: {len(exec_replay['events'])} events, current executed {executed:.0f}%")

    if change:
        last_change_date = data_date
        last_change_desc = change
        print(f"CHANGE: {change}")
        lines = [f"⚡ GLD 金 sleeve（前瞻 OOS 候選・非實單）可行動變化（數據截至 {data_date}）", "",
                 "• " + change, "",
                 f"當前目標權重（cap 1.0）：{sig['final']*100:.0f}%  "
                 f"(閘門{'在場' if sig['gate'] else '出場'}, RV20 {sig['rv20']*100:.1f}%, "
                 f"σ_t {sig['sigma_t']*100:.1f}%, 套袖 {sig['sleeve']:.2f})",
                 f"A2 執行後現持：{executed:.0f}% · 下一個交易日調整至目標。", "",
                 "GLD 金 sleeve 前瞻 OOS 追蹤（候選、尚非實單）。",
                 "詳細： https://research.investmquest.com/long-track-gld/"]
        ALERT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Alert file: {ALERT_FILE}")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()
        print("No actionable change vs last run.")

    html = generate_html(sig, change, last_change_date, history, exec_replay)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "ruleset_locked_date": FREEZE_DATE,
        "mechanism": "W52 gate x adaptive σ_t(756/min252) x cap 1.0 x A2 exec layer 20pp/10%round/clamp100 (single-asset, scale 0~100)",
        "status": "FORWARD OOS PAPER TRACKING — candidate, NOT live. Non-equity live allocation = 0%. Pre-registered kill/review clauses per spec §11.2.",
        "cap": CAP,
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
        "gate": sig["gate"],
        "rv20_pct": round(sig["rv20"] * 100, 2),
        "sigma_t_pct": round(sig["sigma_t"] * 100, 2),
        "raw_ratio": round(sig["raw_ratio"], 4),
        "sleeve_weight": round(sig["sleeve"], 4),
        "final_weight_pct": round(sig["final"] * 100, 1),
        "executed_pct": executed,
        "wk_date": sig["wk_date"], "wk_close": round(sig["wk_close"], 2),
        "w52": round(sig["w52"], 2), "w104": round(sig["w104"], 2), "w250": round(sig["w250"], 2),
        "s104_pos": sig["s104_pos"], "s250_pos": sig["s250_pos"],
        "history": history,
    }
    STATE_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
