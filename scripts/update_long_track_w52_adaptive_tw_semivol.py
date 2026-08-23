#!/usr/bin/env python3
"""台股 0050+2330 — W52 × 自適應波動率 cap 1.5 × B-ii 下跌半變異套袖 — 影子追蹤產生器
================================================================================
2026-08-17 用戶決定：預註冊判準（docs/Adaptive_Sigma_Spec.md 2026-08-17「B 下跌半變異
分母」章節）中，台股主戰場證據 5/5 週線錨點勝出、Calmar 中位數 1.030→1.282，但美股對照
5/5 錨點全輸、2330 長窗 GFC 段 MDD 加深——判準未全數過關，**不採用為實單規則**。改為本頁
**唯讀影子追蹤**：訊號與實單主系統（update_long_track_w52_adaptive.py，cap 1.5＋執行層 A2）
完全相同，**唯一差異＝台股腿套袖分母改用 B-ii（兩邊皆下跌半變異）**，美股腿不在本頁範圍
（本頁僅台股 0050／2330，不追蹤美股）。無 email、不構成倉位建議、不影響實單。

每交易日抓兩腿台股日線（0050.TW、2330.TW auto-adjust＋幻影分割修復），逐腿算：
  1. 週線 W52 單線閘門（W-FRI；週收 > SMA52w 在場、< 出場；無 W104/W250 斜率滯後條件；
     長多 only）→ 0/1，與實單主系統逐位元相同。
  2. **B-ii 套袖（下跌半變異分母，VERBATIM port of
     src/vol_target_backtest/run_b_semivol.py::vol_components + ratio_variant("B-ii")）**：
     r ＝日對數報酬；D20 ＝ √2 × sqrt(mean_20d(min(r,0)²)) × √252（下跌半變異，年化）；
     σ_t ＝ D20 的 rolling(756, min_periods=252).median()；raw_ratio ＝ σ_t/D20（D20=0 →
     +∞、暖身期 NaN → 1.0）；w = clip(raw_ratio, upper=1.5)（真波動率目標，可到 150%）。
  3. 執行層 A2（同實單主系統）：20pp 門檻＋10% 取整＋取整後 clamp 於 50×cap（cap1.5→
     75pp／單腿；組合上限 150%）；最終目標權重 = 0.5 × 閘門 × 套袖（兩腿各自計算）。

規則凍結：成本 7 bps／邊、t+1、台股現金 1%。**本頁自 2026-08-17 起以 B-ii 規則從頭回放整段
history（backfill 1260 交易日）——與實單主系統的「切換日前不重算」處理不同：本頁是全新
頁面，沒有「切換前」的舊規則歷史需要保留，回放窗全程套用 B-ii。**

回測數字見 BT_TW（B-ii 分支，轉錄自 results/vol_targeting/b_semivol.json）；主系統對照數字
（RV20 分母、cap1.5+A2）轉錄自同一報告的 base 列。本頁另讀取（唯讀，不寫入）實單主系統的
docs/long-track-w52-adaptive/state.json 的 history_tw，供「本頁 vs 主系統」並排卡片與雙線
曝險時間軸使用。

CANONICAL COPY：本檔在 v7-backtest（src/vol_target_backtest/）與 financial-analysis-bot
（scripts/）兩處逐位元相同——nav 匯入以 try/except 兼容兩 repo，輸出路徑自動解析為
<repo_root>/docs/long-track-w52-adaptive/。CI 由 fab 執行（update_long_track_w52_adaptive.yml，
台股收盤後 + 美股收盤後各跑一次，date-keyed merge 冪等所以安全）。本頁無 email。

執行層（同實單主系統 A2）：|目標 − 現持| ≥ 20pp 才調整、調整取整至 10% 格後 clamp 於
50×cap（cap1.5→75pp）；整數 pp 空間比較。以 band_exec_replay 從本頁自身 history_tw
確定性重放，供時間軸粗階梯線、事件表與 state 的 executed_pct 用。

圖像化（Chart.js）：合成曝險量表＋每腿乘法鏈 bar、近五年權重時間軸（粗階梯＝執行層持股率
＋細線＝每日理論目標）、近五年 D20 下跌波動 vs σ_t（動態線）、「本頁 vs 主系統」執行層曝險
雙線對照（僅重疊日期）、最近一年執行層變化事件表、回測縮圖（B-ii vs 主系統 RV20，靜態轉錄）。
時間軸資料存於 tw_semivol_state.json 的 history_tw 陣列：首次生成以 build_backfill 規則回放
近 1260 交易日＝約五年（source='replay'），此後 CI 逐日以 _daily_record 追加當日實錄
（source='live'）；merge_history 以日期為 key 冪等，上限 HISTORY_CAP。回放與實錄在圖上以
虛線／實線區隔（誠實紀律，回放不偽裝成實錄）。
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# ---- nav import (byte-identical file across two repos) ---------------------
HERE = Path(__file__).resolve().parent
for _p in (HERE, HERE.parents[2] if len(HERE.parents) >= 3 else HERE):
    sys.path.insert(0, str(_p))
try:                                       # fab: scripts/site_nav.py
    from site_nav import full_nav_block
except ImportError:                        # v7-backtest: repo-root snippet
    from site_nav_snippet import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "lthub")  # 2026-08-23 系統群瘦身：voltrack 項移除，併入系統主控台

# ---- output dir: <repo_root>/docs/long-track-w52-adaptive/ -----------------
_cand = [HERE.parent / "docs", HERE.parents[2] / "docs" if len(HERE.parents) >= 3 else HERE / "docs"]
DOCS = next((c for c in _cand if c.exists()), _cand[0])
OUTPUT = DOCS / "long-track-w52-adaptive" / "tw-semivol.html"
STATE_JSON = DOCS / "long-track-w52-adaptive" / "tw_semivol_state.json"
MAIN_STATE_JSON = DOCS / "long-track-w52-adaptive" / "state.json"   # 唯讀：實單主系統對照
# 無 email／alert：影子追蹤頁（B-ii 台股套袖，不採用為實單規則）；可行動變化 email 由主系統覆蓋（且主系統不受本頁規則影響）。

TW_TICKERS = ["0050", "2330"]
ALL_TICKERS = TW_TICKERS                   # 本頁僅追蹤台股（B-ii 僅台股主戰場證據，美股不在範圍）
YF_SYMBOL = {"0050": "0050.TW", "2330": "2330.TW"}
IS_TW = {"0050": True, "2330": True}
TICKER_MARKET = {"0050": "台股", "2330": "台股"}
WEIGHTS = {t: 0.5 for t in ALL_TICKERS}    # 兩腿各 50%
CAP = 1.5                                  # 曝險上限（同實單主系統 cap 1.5；本頁僅台股腿換套袖分母）
MED_WIN = 756                              # 自適應中位數視窗（3 年），凍結不再調整
MIN_PERIODS = 252                          # 首年 expanding
FREEZE_DATE = "2026-07-17"                 # 機制凍結日（W52 閘門／自適應中位數視窗，同主系統）
SLEEVE_SWITCH_DATE = "2026-08-17"          # 本頁上線日（B-ii 全程回放，無「切換前」舊規則段）

BACKFILL_DAYS = 1260                       # 回放窗（近五年交易日）
HISTORY_CAP = 1320                         # state.json history 陣列上限（>1260 留實錄餘裕）

# 執行層常數（同實單主系統 A2：門檻 20pp／格 10%／取整後 clamp 於 50×cap；cap1.5→75pp／單腿，
# 組合上限 150%）。band／grid／clamp 皆組合 pp；整數 pp 空間比較（不在 0..1 浮點空間重寫）。
EXEC_BAND = 20.0
EXEC_GRID = 10.0
EXEC_CLAMP = 50.0 * CAP             # cap1.5→75pp
EXEC_UPGRADE_DATE = "2026-07-22"

# ---------------------------------------------------------------------------
# 回測摘要（results/vol_targeting/b_semivol.json，2026-08-15 版）— 轉錄
# 每列：(label, cagr%, mdd%, calmar, martin, avg_expo%, adj_per_year|None)
# 五個週線錨點（W-MON…W-FRI，同 A2 執行層）：舊套袖 RV20 Calmar 中位數 1.030（全距 0.363）
# → 台股腿改 B-ii 後 5/5 錨點全勝、Calmar 中位數升至 1.282（全距收窄至 0.244）。
# 依 2026-08-02 timing-luck 稽核，W-FRI（本頁追蹤所用錨點）是五者中最幸運的一支——下表
# 「本頁追蹤」列不宜當作五錨點代表值，僅供對照本頁實際執行的那條路徑。
# ---------------------------------------------------------------------------
BT_TW = {
    "window": "2014-01 – 2026-07",
    "rows": [
        ("台股腿 B-ii，cap1.5＋執行層 A2（本頁影子追蹤）", 25.75, -19.86, 1.2965, 2.705, 90.1, 17.1),
        ("台股腿 B-ii，cap1.5（每日連續・理論）", 24.75, -20.33, 1.2176, 2.724, 86.8, None),
        ("舊套袖 RV20，cap1.5＋執行層 A2（實單主系統・對照）", 22.98, -18.88, 1.2173, 2.544, 83.0, 12.3),
        ("舊套袖 RV20，cap1.5（每日連續・理論對照）", 22.17, -19.24, 1.1524, 2.637, None, None),
    ],
    "anchor": {"base_median": 1.030, "base_range": 0.363,
               "bii_median": 1.282, "bii_range": 0.244},
}

# 單腿 2330 長窗（含 2008 GFC）＝台股架構下深熊唯一檢驗（b_semivol_report.md）
APPENDIX_2330 = {
    "window": "2005-06 – 2026-07",
    "note": ("B-ii 分母把「上漲造成的波動」排除在風險量測外，於反彈段維持較高曝險——"
             "含崩盤樣本的長窗檢驗顯示 GFC 段 MDD 由 −38.7% 加深至 −41.8%（B-ii，+3.1pp），"
             "此為預註冊判準未全數過關、本頁維持為影子而非實單的主因之一。"),
}

# 市場定義（渲染與資料處理共用；本頁僅台股一個市場）
MARKETS = [
    {"key": "tw", "name": "台股 0050 + 2330（B-ii 影子）", "short": "0050+2330",
     "legs": TW_TICKERS, "hist_key": "history_tw", "bt": BT_TW},
]
MKT = {m["key"]: m for m in MARKETS}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def repair_phantom_splits(c: pd.Series, thresh: float = 0.4) -> pd.Series:
    """Yahoo phantom-split repair (port of tw_0050_backtest.backtest_tw):
    single-bar |return| > thresh with no recorded split -> rescale the PRIOR
    segment so the return series is continuous. TW price limit is ±10%, so a
    genuine move can never trip this. Known case: 0050.TW 2014-01-02 (~4:1)."""
    c = c.copy()
    r = c.pct_change()
    for d in r[r.abs() > thresh].index:
        i = c.index.get_loc(d)
        factor = float(c.iloc[i] / c.iloc[i - 1])
        c.iloc[:i] *= factor
        print(f"  phantom split repaired at {d.date()} (factor {factor:.5f})")
    return c


def fetch_close(ticker: str) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 13)   # 13y: W250 (~4.8y) warmup + state history
    df = yf.download(YF_SYMBOL[ticker], start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    c = c.dropna()
    if getattr(c.index, "tz", None) is not None:
        c.index = c.index.tz_localize(None)
    return repair_phantom_splits(c) if IS_TW[ticker] else c


# ---------------------------------------------------------------------------
# Gate — verbatim port of run_ext_ltrack_smh.longtrack_weight (weekly, long-only)
# ---------------------------------------------------------------------------
def _gate_core(px: pd.Series):
    """W52 單線閘門（週收 > SMA52w 在場、< 出場，W-FRI，無滯後條件）。逐位元對齊
    run_w52_adaptive.gate_w52。回傳 (wk, pos, w52, w104, w250, s104, s250)——W104/W250
    與斜率僅供頁面卡片作參考背景，<b>閘門決策只用 W52</b>；共用給 gate_state 與 build_backfill。"""
    wk = px.resample("W-FRI").last().dropna()
    w52 = wk.rolling(52).mean()
    w104 = wk.rolling(104).mean()
    w250 = wk.rolling(250).mean()
    s104 = w104 - w104.shift(4)
    s250 = w250 - w250.shift(4)
    pos = (wk > w52).astype(int)      # W52 單線：無 W104/W250 斜率滯後條件
    pos[w52.isna()] = 0
    pos = pos.astype(int)
    return wk, pos, w52, w104, w250, s104, s250


def gate_state(px: pd.Series) -> dict:
    wk, pos, w52, w104, w250, s104, s250 = _gate_core(px)

    recent = []
    for i in range(-8, 0):
        recent.append({
            "date": wk.index[i].strftime("%Y-%m-%d"),
            "close": float(wk.iloc[i]),
            "w52": float(w52.iloc[i]) if not pd.isna(w52.iloc[i]) else None,
            "w104": float(w104.iloc[i]) if not pd.isna(w104.iloc[i]) else None,
            "w250": float(w250.iloc[i]) if not pd.isna(w250.iloc[i]) else None,
            "s104_pos": bool(s104.iloc[i] > 0) if not pd.isna(s104.iloc[i]) else None,
            "s250_pos": bool(s250.iloc[i] > 0) if not pd.isna(s250.iloc[i]) else None,
            "in": bool(pos.iloc[i]),
        })
    return {
        "gate": bool(pos.iloc[-1]),
        "wk_date": wk.index[-1].strftime("%Y-%m-%d"),
        "wk_close": float(wk.iloc[-1]),
        "w52": float(w52.iloc[-1]), "w104": float(w104.iloc[-1]), "w250": float(w250.iloc[-1]),
        "s104_pos": bool(s104.iloc[-1] > 0), "s250_pos": bool(s250.iloc[-1] > 0),
        "recent": recent,
    }


# ---------------------------------------------------------------------------
# Sleeve — adaptive median (verbatim port of
#          run_adaptive_sigma.vt_weight_adaptive_median with n_days=756)
# ---------------------------------------------------------------------------
def _sleeve_from(px: pd.Series, win: int = 20):
    """B-ii（下跌半變異分母；VERBATIM port of
    src/vol_target_backtest/run_b_semivol.py::vol_components + ratio_variant("B-ii")）。
    r ＝日對數報酬；D20 ＝ √2 × sqrt(mean_20d(min(r,0)^2)) × √252（下跌半變異，年化）；
    σ_t ＝ D20 的 rolling(756, min_periods=252).median()；raw_ratio ＝ σ_t/D20，D20=0
    → +∞（clip 後即 cap）、暖身期 NaN → 1.0；w = clip(raw_ratio, upper=CAP)。回傳
    (d20_now, sigma_t_now, sleeve, raw_ratio)——d20_now／sigma_t_now 是下跌波動 D20／
    σ_t(D20)，不是全波動 RV20（欄名沿用 rv20/sigma_t 以與主系統 schema 一致，見
    sleeve_variant 標記）。因果、無前視。"""
    lr = np.log(px / px.shift(1))
    neg = lr.clip(upper=0.0)
    d20 = np.sqrt(2.0) * np.sqrt((neg ** 2).rolling(win).mean()) * np.sqrt(252)
    sigma_semi = d20.rolling(MED_WIN, min_periods=MIN_PERIODS).median()
    d20_now = float(d20.iloc[-1])
    sig_now = float(sigma_semi.iloc[-1])
    num, den = sig_now, d20_now
    if pd.isna(num) or pd.isna(den):
        raw = 1.0
        if pd.isna(sig_now):
            sig_now = d20_now
    elif den == 0:
        raw = 1e6
    else:
        raw = num / den
    w = min(CAP, raw)
    return d20_now, sig_now, w, raw


def sleeve_state(px: pd.Series) -> dict:
    d20_now, sig_now, w, raw = _sleeve_from(px)
    # 距離開槓桿：raw < 1 時波動還要降 (1-raw) 才到 1.0（開始借錢）；raw ≥ 1 已在借
    return {"rv20": d20_now, "sigma_t": sig_now, "sleeve": w, "raw_ratio": raw,
            "sleeve_variant": "semivol_bii",
            "levered": bool(raw > 1.0), "dist_to_lever": max(0.0, 1.0 - raw)}


def compute_ticker(t: str, px: pd.Series) -> dict:
    g = gate_state(px)
    s = sleeve_state(px)
    fill = (1 if g["gate"] else 0) * s["sleeve"]        # 0..CAP fill of the 0.5 slot
    final = WEIGHTS[t] * fill
    return {**g, **s, "fill": fill, "final": final}


# ---------------------------------------------------------------------------
# History — rule-replay backfill (誠實紀律：回放 ≠ 實錄，欄位 source 標記區分)
# ---------------------------------------------------------------------------
def _daily_record(px_map: dict, legs: list, d: pd.Timestamp, source: str) -> dict:
    """One market's one-day target weights, computed byte-identically to the
    live path: gate = _gate_core(px[:d]).pos.iloc[-1]；sleeve = B-ii on px[:d].
    source ∈ {'replay','live'}. Records rv20_pct/sigma_t_pct per leg — for this
    page these fields carry D20／σ_t(D20)（下跌波動），see sleeve_variant."""
    rec = {"date": d.strftime("%Y-%m-%d"), "source": source, "tickers": {}}
    combined = 0.0
    for t in legs:
        pxd = px_map[t].loc[:d]
        _, pos, *_ = _gate_core(pxd)
        gate = bool(pos.iloc[-1])
        vol_now, sig_now, sleeve, raw = _sleeve_from(pxd)
        final = WEIGHTS[t] * ((1 if gate else 0) * sleeve)
        combined += final
        rec["tickers"][t] = {
            "gate": gate,
            "rv20_pct": round(vol_now * 100, 2),
            "sigma_t_pct": round(sig_now * 100, 2),
            "raw_ratio": round(raw, 4),
            "sleeve": round(sleeve, 4),
            "sleeve_variant": "semivol_bii",
            "final_pct": round(final * 100, 1),   # 組合 pp，0..75（單腿滿槓桿 75）
        }
    rec["combined_pct"] = round(combined * 100, 1)
    return rec


def build_backfill(px_map: dict, legs: list, n_days: int = BACKFILL_DAYS) -> list:
    """Replay the exact daily rule over the last n_days common trading days of
    this market's legs. Every record is marked source='replay'."""
    common = None
    for t in legs:
        common = px_map[t].index if common is None else common.intersection(px_map[t].index)
    dates = common.sort_values()[-n_days:]
    return [_daily_record(px_map, legs, d, "replay") for d in dates]


def merge_history(prev_history: list, backfill: list, today_rec: dict,
                  cap: int = HISTORY_CAP) -> list:
    """Idempotent, date-keyed merge. Backfill only fills dates absent from
    prior history (never overwrites a recorded 'live' point with a 'replay').
    Today's live record always wins its date. Kept sorted, capped at `cap`."""
    by_date = {r["date"]: r for r in (prev_history or [])}
    for r in backfill:
        by_date.setdefault(r["date"], r)
    by_date[today_rec["date"]] = today_rec       # live wins
    out = [by_date[k] for k in sorted(by_date)]
    return out[-cap:]


# ---------------------------------------------------------------------------
# Execution layer — A2：20pp 門檻＋10% 取整＋取整後 clamp 於 50×cap（升格 2026-07-22）
# 每市場各自從 history 確定性重放（history_us／history_tw），冪等可重現。
# band／grid／clamp 以組合 pp 為單位（每腿滿載＝50 pp；本頁 cap1.5 clamp＝75pp／單腿）。
# ---------------------------------------------------------------------------
def band_exec_replay(history: list, legs: list) -> dict:
    """對每腿的最終權重（組合 pp）重放執行層：executed 初始 0，逐日若
    |target − executed| ≥ 20pp 則 executed = min(round(target/10)×10, 50×cap)，否則不變
    （cap1.5→75pp／單腿，組合上限 150%）。回傳每腿每日 executed、組合合計、事件清單
    （日期、腿、from→to、原因＝該日閘門翻轉則「閘門翻轉」否則「波動調整」、當日組合
    執行曝險）與各腿當前值。"""
    executed = {t: [] for t in legs}
    combined, events = [], []
    cur = {t: 0.0 for t in legs}
    prev_gate = {t: None for t in legs}
    for r in history:
        for t in legs:
            tk = r["tickers"][t]
            target = tk["final_pct"]
            gate = bool(tk["gate"])
            if abs(target - cur[t]) >= EXEC_BAND:
                new = min(round(target / EXEC_GRID) * EXEC_GRID, EXEC_CLAMP)
                if new != cur[t]:
                    flipped = prev_gate[t] is not None and gate != prev_gate[t]
                    events.append({"date": r["date"], "leg": t,
                                   "from": cur[t], "to": new,
                                   "reason": "閘門翻轉" if flipped else "波動調整"})
                    cur[t] = new
            executed[t].append(cur[t])
            prev_gate[t] = gate
        combined.append(round(sum(cur[t] for t in legs), 1))
    date_idx = {r["date"]: i for i, r in enumerate(history)}
    for ev in events:
        ev["combined_exec_pct"] = combined[date_idx[ev["date"]]]
    last = {t: (executed[t][-1] if executed[t] else 0.0) for t in legs}
    return {"executed": executed, "combined": combined, "events": events, "last": last}


def events_card(mkt: dict, events: list) -> str:
    # 2026-07-24：事件表由近三年窗改為過濾最近一年（365 個日曆天），標題同步；
    # band_exec_replay 本身仍對全史（現已近五年）重放以確保現持狀態正確，只有本表顯示過濾。
    cutoff = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    recent_events = [e for e in events if e["date"] >= cutoff]
    if not recent_events:
        body = ('<tr><td colspan="5" style="text-align:center;color:var(--muted)">'
                '最近一年窗內無執行層調整事件（皆未跨 20pp 門檻）</td></tr>')
    else:
        body = ""
        for ev in reversed(recent_events):          # 倒序（最新在上）
            rc = "var(--blue-text)" if ev["reason"] == "閘門翻轉" else "var(--amber-text)"
            body += (f'<tr><td>{ev["date"]}</td><td><b>{ev["leg"]}</b></td>'
                     f'<td>{ev["from"]:.0f}% → {ev["to"]:.0f}%</td>'
                     f'<td style="color:{rc}">{ev["reason"]}</td>'
                     f'<td class="num">{ev["combined_exec_pct"]:.0f}%</td></tr>\n')
    return f"""<div class="card">
<h3>{mkt['short']} 最近一年執行層訊號變化事件（A2：20pp 門檻＋10% 取整＋clamp 75%）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
只有當某腿目標與現持差 ≥ 20pp 才調整（取整到 10% 格、再 clamp 於 75%），故事件遠少於每日微調。倒序列出最近 365 天內全部事件；「變化」為該腿最終權重（組合 pp，單腿滿槓桿 75%）；原因＝當日閘門翻轉則「閘門翻轉」否則「波動調整」。</p>
<table><thead><tr><th>日期</th><th>腿</th><th>變化</th><th>原因</th><th class="num">當日組合執行曝險</th></tr></thead>
<tbody>{body}</tbody></table>
</div>"""


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------
def fmt_pct(v, dp=2):
    return f"{'+' if v >= 0 else ''}{v:.{dp}f}%"


def fill_color(fill):
    if fill >= 0.99:
        return "green"
    if fill >= 0.66:
        return "blue"
    if fill >= 0.33:
        return "amber"
    return "red"


def ticker_card(t: str, d: dict) -> str:
    col = fill_color(d["fill"])
    gate_on = d["gate"]
    d52 = (d["wk_close"] / d["w52"] - 1) * 100
    d104 = (d["wk_close"] / d["w104"] - 1) * 100
    d250 = (d["wk_close"] / d["w250"] - 1) * 100
    near_exit = gate_on and abs(d52) < 2.0
    warn = (' <span style="color:var(--amber);font-weight:700;font-size:.72rem">'
            '⚠ 接近出場（近 W52）</span>') if near_exit else ""
    rv = d["rv20"] * 100
    sig = d["sigma_t"] * 100
    return f"""<div class="tcard">
  <div class="tcard-hdr">
    <span class="tname">{t}</span>
    <span class="pos-badge pos-{col}">最終權重 {d['final']*100:.0f}%</span>
  </div>
  <div class="tcard-sub">閘門 {'在場' if gate_on else '出場'} × 套袖 {d['sleeve']*100:.0f}%
    → 佔本標的 50% 額度的 {d['fill']*100:.0f}% · 目標權重 0.5 × {1 if gate_on else 0} × {d['sleeve']:.2f} = {d['final']*100:.0f}%{warn}</div>
  <div class="sig-row">
    <div class="sig {'on' if gate_on else 'off'}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">週線長軌閘門</span><span class="sig-mark">{'✓ 在場' if gate_on else '✕ 出場'}</span></div>
      <div class="sig-detail">週收 {d['wk_close']:.2f}｜W52 {d['w52']:.2f} <b style="color:var(--{'green' if d52>=0 else 'red'})">{fmt_pct(d52,1)}</b>
        ｜W104 {d['w104']:.2f} <b style="color:var(--{'green' if d104>=0 else 'red'})">{fmt_pct(d104,1)}</b>
        ｜W250 {d['w250']:.2f} <b style="color:var(--{'green' if d250>=0 else 'red'})">{fmt_pct(d250,1)}</b>
        ｜W104斜率 {'↑' if d['s104_pos'] else '↓'}｜W250斜率 {'↑' if d['s250_pos'] else '↓'}
        <br><span style="font-size:.72rem">W52 單線閘門：週收 &gt; W52 在場、&lt; W52 出場（W104/W250 僅供背景參考，不入閘門決策）。與實單主系統逐位元相同。</span></div>
    </div>
    <div class="sig {'on' if d['levered'] else ('off' if d['sleeve']<0.999 else '')}">
      <div class="sig-top"><span class="sig-dot"></span><span class="sig-name">B-ii 套袖（下跌半變異，cap 1.5）</span><span class="sig-mark">{d['sleeve']*100:.0f}%</span></div>
      <div class="sig-detail">下跌波動 D20 <b>{rv:.1f}%</b> vs σ_t <b>{sig:.1f}%</b> → σ_t/D20 原始比率 <b>{d['raw_ratio']:.2f}</b>
        → w = clip({d['raw_ratio']:.2f}, 上限 1.5) = <b>{d['sleeve']:.2f}</b>
        <br><span style="font-size:.72rem">{('<b style=color:var(--green)>已開槓桿</b>：下跌波動低於自身近 3 年中位，加碼到 %.0f%%。' % (d['sleeve']*100)) if d['levered'] else (f'未開槓桿（σ_t/D20 &lt; 1，減碼中）：下跌波動<b>再降 %.0f%%</b>才到 1.0 開始借錢。' % (d['dist_to_lever']*100))} 分母為下跌半變異（B-ii），與實單主系統的 RV20（全波動）不同，是本頁唯一與主系統的差異。</span></div>
    </div>
  </div>
</div>"""


def recent_table(t: str, d: dict) -> str:
    rows = ""
    for r in d["recent"]:
        if r["w52"] is None:
            continue
        d52 = (r["close"] / r["w52"] - 1) * 100
        c52 = "var(--green)" if d52 >= 0 else "var(--red)"
        incell = (f'<span class="tag" style="background:var(--green-bg);color:var(--green-text)">在場</span>'
                  if r["in"] else
                  f'<span class="tag" style="background:var(--red-bg);color:var(--red-text)">出場</span>')
        rows += f"""<tr>
  <td>{r['date']}</td><td>{r['close']:.2f}</td>
  <td>{r['w52']:.2f}</td><td style="color:{c52}">{fmt_pct(d52,1)}</td>
  <td>{r['w104']:.2f}</td><td>{r['w250']:.2f}</td>
  <td>{'↑' if r['s104_pos'] else '↓'} / {'↑' if r['s250_pos'] else '↓'}</td>
  <td>{incell}</td>
</tr>\n"""
    return f"""<div class="card">
<h3>{t} — 近 8 週閘門軌跡（週線 W-FRI）</h3>
<table><thead><tr><th>週五</th><th>週收</th><th>W52</th><th>距 W52</th><th>W104</th><th>W250</th><th>W104/W250 斜率</th><th>閘門</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>"""


def backtest_section(mkt: dict) -> str:
    bt = mkt["bt"]
    rows = ""
    for lab, cagr, mdd, calmar, martin, avg, adj in bt["rows"]:
        hl = "rowhl" if "本頁" in lab else ("rowbh" if "實單主系統" in lab else "")
        avg_s = f"{avg:.1f}%" if avg is not None else "—"
        adj_s = f"{adj:.1f}" if adj is not None else "—"
        rows += (f'<tr class="{hl}"><td>{lab}</td><td class="num">{cagr:.2f}%</td>'
                 f'<td class="num">{mdd:.2f}%</td><td class="num">{calmar:.4f}</td>'
                 f'<td class="num">{martin:.3f}</td><td class="num">{avg_s}</td>'
                 f'<td class="num">{adj_s}</td></tr>\n')
    an = bt["anchor"]
    return f"""<div class="card">
<h3>回測摘要 — {mkt['short']}（B-ii 下跌半變異套袖 vs 實單主系統 RV20 套袖・窗 {bt['window']}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
兩標的日報酬 50/50 加權合成（等效每日再平衡，如實揭露）。<b>主列（藍底）＝本頁追蹤（B-ii，cap1.5＋執行層 A2）</b>；
灰底列＝實單主系統對照（RV20 分母，cap1.5＋執行層 A2，規則與追蹤操作完全相同的分支）。「每日連續」為未過執行層的理論對照。
數字轉錄自 results/vol_targeting/b_semivol.json（2026-08-15 版報告）。</p>
<table><thead><tr><th>配置</th><th class="num">CAGR</th><th class="num">MDD</th><th class="num">Calmar</th><th class="num">Martin</th><th class="num">平均曝險</th><th class="num">年調整次數</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="takeaway"><b>五個週線錨點穩健性（W-MON…W-FRI，同 A2 執行層）</b>：舊套袖 RV20 下 Calmar 中位數 <b>{an['base_median']:.3f}</b>（全距 {an['base_range']:.3f}）→ 台股腿改 B-ii 後 <b>5/5 錨點全勝</b>，Calmar 中位數升至 <b>{an['bii_median']:.3f}</b>（全距收窄至 {an['bii_range']:.3f}）。
<b>提醒</b>：依 2026-08-02 timing-luck 稽核，本頁追蹤所用的 W-FRI 錨點是五者中最幸運的一支——上表「本頁追蹤」列數字<b>不宜當作五錨點的代表值</b>，僅供對照本頁實際執行的那條路徑。完整五錨點分布見 <code>results/vol_targeting/b_semivol_report.md</code>。</div>
</div>"""


def appendix_2330_section() -> str:
    ap = APPENDIX_2330
    return f"""<div class="card">
<h3>附錄 — 單腿 2330 長窗（含 2008 GFC）＝台股架構下深熊的唯一檢驗（窗 {ap['window']}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.7rem">
台股正式窗自 2014 起（0050 免費歷史限制）不含深熊。2330 有 2005 起資料，單腿拉長把 2008 GFC 收進來，
檢驗含崩盤樣本時 B-ii 分母相對 RV20 分母的行為。</p>
<div class="takeaway">{ap['note']}</div>
</div>"""


# ---------------------------------------------------------------------------
# per-market render (html block + chart JS)
# ---------------------------------------------------------------------------
def _market_data(mkt: dict, sigs: dict, history: list, exec_replay: dict) -> dict:
    legs = mkt["legs"]
    a, b = legs[0], legs[1]

    def _col(fn):
        return json.dumps([fn(r) for r in history], separators=(",", ":"))
    H = {
        "labels": _col(lambda r: r["date"]),
        "comb": _col(lambda r: r["combined_pct"]),
        "a": _col(lambda r: r["tickers"][a]["final_pct"]),
        "b": _col(lambda r: r["tickers"][b]["final_pct"]),
        "arv": _col(lambda r: r["tickers"][a]["rv20_pct"]),
        "brv": _col(lambda r: r["tickers"][b]["rv20_pct"]),
        "asig": _col(lambda r: r["tickers"][a]["sigma_t_pct"]),
        "bsig": _col(lambda r: r["tickers"][b]["sigma_t_pct"]),
        "src": _col(lambda r: r["source"]),
        # executed layer (A2: 20pp band + 10% round + clamp 50×cap) — deterministic replay
        "cexe": json.dumps(exec_replay["combined"], separators=(",", ":")),
        "aexe": json.dumps(exec_replay["executed"].get(a, []), separators=(",", ":")),
        "bexe": json.dumps(exec_replay["executed"].get(b, []), separators=(",", ":")),
    }
    combined = sum(sigs[t]["final"] for t in legs) * 100            # 今日目標（訊號）
    exec_combined = round(exec_replay["combined"][-1], 1) if exec_replay["combined"] else combined  # 現持（執行層）
    exec_finals = [round(exec_replay["last"].get(t, 0.0), 1) for t in legs]   # 每腿現持（執行層）
    ccol = fill_color(combined / 100)
    slot = {t: WEIGHTS[t] * 100 for t in legs}
    finals = [round(sigs[t]["final"] * 100, 1) for t in legs]        # 組合 pp（滿載 50%；A2 門檻判斷用，不動）
    # 每腿乘法鏈圖（chart-chain）：「自身滿載＝100%」基準顯示（純顯示變換，
    # 不影響上面 finals／組合 pp 判斷）；本頁 cap 1.5，但此圖恆以自身滿載為 100% 基準，與 cap 無關。
    fill_self = [round(sigs[t]["fill"] * 100, 1) for t in legs]
    gate_cut = [round(100.0 if not sigs[t]["gate"] else 0.0, 1) for t in legs]
    sleeve_cut = [round(max(0.0, 100.0 - fill_self[i] - gate_cut[i]), 1) for i, t in enumerate(legs)]
    n_replay = sum(1 for r in history if r["source"] == "replay")
    n_live = sum(1 for r in history if r["source"] == "live")
    span = (f"{history[0]['date']} → {history[-1]['date']}" if history else "—")
    return {
        "legs": legs, "a": a, "b": b, "combined": combined, "exec_combined": exec_combined,
        "exec_finals": exec_finals, "ccol": ccol,
        "finals": finals, "fill_self": fill_self,
        "C_FINALS": json.dumps(fill_self, separators=(",", ":")),
        "C_SLEEVE": json.dumps(sleeve_cut, separators=(",", ":")),
        "C_GATE": json.dumps(gate_cut, separators=(",", ":")),
        "H": H, "n_replay": n_replay, "n_live": n_live, "span": span,
        "nhist": len(history), "events": exec_replay["events"],
    }


def _cmp_chart_js(suf: str, cmp: dict) -> str:
    """本頁 vs 主系統雙線曝險比較圖的 Chart.js 區塊。cmp['available']=False 時不產生
    canvas 對應的 dataset（頁面端該卡片本身也會略過渲染），回傳空字串，不偽造資料。"""
    if not cmp or not cmp.get("available"):
        return ""
    return f"""
var CMP_LAB_{suf}={cmp['labels']},CMP_SHADOW_{suf}={cmp['shadow']},CMP_MAIN_{suf}={cmp['main']};
new Chart(document.getElementById('chart-cmp-{suf}'),{{
  type:'line',
  data:{{labels:CMP_LAB_{suf},datasets:[
    {{label:'本頁（B-ii）現持',data:CMP_SHADOW_{suf},borderColor:GREEN,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,tension:0}},
    {{label:'實單主系統（RV20）現持',data:CMP_MAIN_{suf},borderColor:BLUE,borderWidth:2,borderDash:[5,3],stepped:true,pointRadius:0,pointHoverRadius:3,tension:0}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{min:0,max:150,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});
"""


def _cmp_card_html(suf: str, cmp: dict) -> str:
    """本頁 vs 主系統執行層曝險雙線圖卡片。cmp 不可用時顯示誠實提示（不畫假圖）。"""
    if not cmp or not cmp.get("available"):
        return ('<div class="card"><h3>本頁 vs 實單主系統 — 執行層曝險時間軸對照</h3>'
                '<p style="font-size:.82rem;color:var(--muted)">兩邊歷史尚無重疊日期，暫無法對照（本頁剛建立，需與主系統累積共同的實錄天數後才會出現對照線）。</p></div>')
    return f"""<div class="card">
<h3>台股 執行層曝險時間軸對照 — 本頁（B-ii）vs 實單主系統（RV20）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
兩條線都是<b>執行層現持</b>（A2 20pp 門檻＋10% 取整後的實際組合曝險，非每日理論目標），差異僅來自套袖分母（本頁 D20 下跌半變異 vs 主系統 RV20 全波動）。
交集窗 {cmp['span']}，共 {cmp['n']} 個交易日。</p>
<div class="chart-wrap"><canvas id="chart-cmp-{suf}"></canvas></div>
</div>"""


# ---------------------------------------------------------------------------
# 本頁 vs 實單主系統對照（唯讀）：讀取主系統 state.json 的 history_tw／tickers，
# 用同一套 band_exec_replay（cap1.5＋A2，主系統早已相同規則）重建其執行層曝險序列，
# 與本頁自身執行層曝險並排——只取兩邊日期的交集，不外推、不填補缺口。
# ---------------------------------------------------------------------------
def load_main_state() -> dict:
    if not MAIN_STATE_JSON.exists():
        return {}
    try:
        return json.loads(MAIN_STATE_JSON.read_text())
    except Exception:
        return {}


def main_vs_shadow_series(shadow_history: list, shadow_exec: dict, main_state: dict) -> dict:
    """回傳 {available, labels, shadow, main, n} 供雙線曝險時間軸；main_state 缺失或
    無 history_tw 時 available=False（頁面誠實顯示「主系統尚無可比資料」，不偽造）。"""
    main_hist = main_state.get("history_tw") or []
    if not main_hist:
        return {"available": False}
    main_exec = band_exec_replay(main_hist, TW_TICKERS)
    main_by_date = {r["date"]: v for r, v in zip(main_hist, main_exec["combined"])}
    shadow_by_date = {r["date"]: v for r, v in zip(shadow_history, shadow_exec["combined"])}
    common = sorted(set(main_by_date) & set(shadow_by_date))
    if not common:
        return {"available": False}
    return {
        "available": True,
        "labels": json.dumps(common, separators=(",", ":")),
        "shadow": json.dumps([shadow_by_date[d] for d in common], separators=(",", ":")),
        "main": json.dumps([main_by_date[d] for d in common], separators=(",", ":")),
        "n": len(common), "span": f"{common[0]} → {common[-1]}",
    }


def main_snapshot_card(main_state: dict) -> str:
    """本頁 vs 主系統：今日讀數並排（唯讀，讀主系統 state.json 的 tickers／
    combined_exposure_tw_pct，不做任何寫入或推算超出既有欄位）。"""
    tk = main_state.get("tickers") or {}
    if not tk or "0050" not in tk or "2330" not in tk:
        return ('<div class="card"><h3>本頁 vs 實單主系統（唯讀對照）</h3>'
                '<p style="font-size:.82rem;color:var(--muted)">主系統 state.json 尚無可讀資料，略過本次對照。</p></div>')
    main_data_date = main_state.get("data_date", "—")
    tgt_sum = round(tk["0050"]["final_weight_pct"] + tk["2330"]["final_weight_pct"], 1)
    exe_sum = round(tk["0050"]["executed_pct"] + tk["2330"]["executed_pct"], 1)
    rows = ""
    for t in TW_TICKERS:
        d = tk[t]
        rows += (f'<tr><td>{t}</td><td class="num">{"在場" if d["gate"] else "出場"}</td>'
                 f'<td class="num">{d["rv20_pct"]:.1f}%</td><td class="num">{d["sigma_t_pct"]:.1f}%</td>'
                 f'<td class="num">{d.get("raw_ratio", d["sleeve_weight"]):.2f}</td>'
                 f'<td class="num">{d["final_weight_pct"]:.1f}%</td>'
                 f'<td class="num">{d["executed_pct"]:.0f}%</td></tr>\n')
    return f"""<div class="card" style="border:2px solid var(--blue-border)">
<h3 style="color:var(--blue-text)">本頁（B-ii）vs 實單主系統（RV20，唯讀對照・主系統數據截至 {main_data_date}）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.6rem">
下表為<b>主系統</b>（RV20 分母、cap1.5＋A2，不受本頁規則影響）當前讀數，直接讀取 <code>state.json</code>，唯讀不寫入。
RV20 欄為<b>全波動</b>（與本頁「下跌波動 D20」不同分母，比較同一列的 raw ratio／執行層即可，不必比較原始波動數字本身）。
主系統組合目標 <b>{tgt_sum:.1f}%</b>、執行層現持 <b>{exe_sum:.0f}%</b>。</p>
<table><thead><tr><th>腿</th><th class="num">閘門</th><th class="num">RV20</th><th class="num">σ_t</th><th class="num">raw ratio</th><th class="num">目標</th><th class="num">現持</th></tr></thead>
<tbody>{rows}</tbody></table>
</div>"""


def _dual_breakdown(legs, finals, exec_finals):
    """組合層目標/現持並排＋每腿拆分。合計＝每腿顯示值（四捨五入後）之和，確保
    「腿＋腿＝合計」自洽。回傳 (html、目標合計、現持合計)。"""
    tf = [round(f) for f in finals]
    ef = [round(e) for e in exec_finals]
    td, ed = sum(tf), sum(ef)
    tgt = "＋".join(f"{legs[i]} {tf[i]}%" for i in range(len(legs)))
    exe = "＋".join(f"{legs[i]} {ef[i]}%" for i in range(len(legs)))
    html = (f"<b>目標 {td}%</b>＝{tgt}（訊號，每日隨波動微調）／"
            f"<b>現持 {ed}%</b>＝{exe}（執行層；"
            f"<b>|目標−現持| 未達 20pp 不調，故兩者常有幾 % 差、是設計非錯誤</b>）")
    return html, td, ed


def market_html(mkt: dict, sigs: dict, md: dict) -> str:
    legs = mkt["legs"]
    exec_finals = md["exec_finals"]
    ccol = md["ccol"]
    finals = md["finals"]
    suf = mkt["key"]
    cards = "".join(ticker_card(t, sigs[t]) for t in legs)
    dual, combined, exec_combined = _dual_breakdown(legs, finals, exec_finals)
    return f"""<div class="mkt-hd"><span class="mkt-tag">{mkt['name']}</span></div>

<div class="status-hero hero-{ccol}">
  <div class="status-badge"><span class="dot"></span><span>{mkt['short']} 組合曝險</span></div>
  <div class="status-exposure" style="display:flex;gap:1.4rem;justify-content:center;align-items:baseline;flex-wrap:wrap">
    <span>目標 {combined:.0f}%<span style="font-size:.4em;color:var(--muted);font-weight:600"> 訊號</span></span>
    <span style="opacity:.55;font-size:.7em">／</span>
    <span>現持 {exec_combined:.0f}%<span style="font-size:.4em;color:var(--muted);font-weight:600"> 執行層</span></span>
  </div>
  <div style="font-size:.8rem;color:var(--muted)">{dual}。</div>
</div>

<div class="card">
<h3>{mkt['short']} 當前部位視覺 — 合成曝險量表 × 每腿乘法鏈</h3>
<div class="viz-split">
  <div>
    <div class="gauge-box">
      <canvas id="chart-gauge-{suf}"></canvas>
      <div class="gauge-center"><div class="g-num hero-{ccol}" style="color:var(--{ccol})">{combined:.0f}%</div><div class="g-lab">目標曝險（訊號）· 現持 {exec_combined:.0f}%</div></div>
    </div>
  </div>
  <div>
    <div class="chart-wrap-xs"><canvas id="chart-chain-{suf}"></canvas></div>
  </div>
</div>
<div style="font-size:.76rem;color:var(--muted);margin-top:.7rem"><b>每腿以自身滿載＝150%（cap 1.5）顯示</b>（合成曝險量表仍為組合層 0~150%，不變）＝<b style="color:var(--text)">最終持有</b> ＋ <b style="color:var(--amber-text)">套袖折減</b>（高波減碼）＋ <b>閘門關閉</b>（出場歸零）。{legs[0]} 自身滿載 {md['fill_self'][0]:.0f}%（組合 pp {finals[0]:.0f}%）、{legs[1]} 自身滿載 {md['fill_self'][1]:.0f}%（組合 pp {finals[1]:.0f}%）。</div>
</div>

<div class="card">
<h3>{mkt['short']} 近五年權重時間軸 — 現持（執行層）vs 每日理論目標</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
<b style="color:var(--text)">粗階梯線＝現持（執行層）</b>＝A2 20pp 門檻＋10% 取整的實際持股率（跨門檻才動）；<b>細線＝每日理論目標（訊號）</b>（未過門檻不調）。
末端值：{dual}。
線段<b>實線＝每日實錄</b>、<b>虛線＝規則回放</b>（本頁 2026-08-17 首次生成往回重算，誠實區隔——回放全程套用 B-ii，不是「切換前舊規則」）。窗 {md['span']}，共 {md['nhist']} 個交易日（回放 {md['n_replay']}／實錄 {md['n_live']}）。</p>
<div class="chart-wrap"><canvas id="chart-weights-{suf}"></canvas></div>
<div class="legend-note">
  <span class="ln-item"><span class="ln-line" style="border-top-width:3px"></span>執行層（粗階梯）</span>
  <span class="ln-item"><span class="ln-line" style="border-top-color:rgba(120,120,120,.5)"></span>每日理論目標（細）</span>
  <span class="ln-item"><span class="ln-line"></span>每日實錄</span>
  <span class="ln-item"><span class="ln-line ln-dash"></span>規則回放</span>
</div>
<h3 style="margin-top:1.1rem">{mkt['short']} 近五年套袖觸發脈絡 — D20 下跌波動 vs σ_t（動態）</h3>
<p style="font-size:.8rem;color:var(--muted);margin-bottom:.5rem">
本頁分母為<b>下跌半變異 D20</b>（B-ii），不是主系統的 RV20（全波動）。σ_t 是<b>動態線</b>（D20 近 3 年滾動中位數）。當 D20（實線）升破自身 σ_t（虛線）時套袖按比例減碼；D20 ≤ σ_t 時可加碼到 cap 1.5。regime 抬升時 σ_t 跟著上移。</p>
<div class="chart-wrap-sm"><canvas id="chart-rv-{suf}"></canvas></div>
</div>

{events_card(mkt, md['events'])}

<div class="tgrid">{cards}</div>

{md.get('main_snapshot_html', '')}

{md.get('cmp_card_html', '')}

{"".join(recent_table(t, sigs[t]) for t in legs)}

{backtest_section(mkt)}

{appendix_2330_section()}
"""


def market_js(mkt: dict, md: dict) -> str:
    suf = mkt["key"]
    legs = mkt["legs"]
    combined = md["combined"]
    ccol = md["ccol"]
    CCOL_HEX = {"green": "#16a34a", "blue": "#1d4ed8",
                "amber": "#a16207", "red": "#b91c1c"}[ccol]
    H = md["H"]
    return f"""
// ===== market: {suf} =====
new Chart(document.getElementById('chart-gauge-{suf}'),{{
  type:'doughnut',
  data:{{labels:['曝險','現金'],datasets:[{{data:[{combined:.1f},{100-combined:.1f}],
    backgroundColor:['{CCOL_HEX}','#ece7db'],borderWidth:0}}]}},
  options:{{rotation:-90,circumference:180,cutout:'72%',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:function(c){{return c.label+': '+c.parsed.toFixed(1)+'%'}}}}}}}}}}
}});

new Chart(document.getElementById('chart-chain-{suf}'),{{
  type:'bar',
  data:{{labels:['{legs[0]}','{legs[1]}'],datasets:[
    {{label:'最終持有',data:{md['C_FINALS']},backgroundColor:[GREEN,AMBER],borderWidth:0,stack:'s'}},
    {{label:'套袖折減',data:{md['C_SLEEVE']},backgroundColor:'rgba(161,98,7,0.28)',borderWidth:0,stack:'s'}},
    {{label:'閘門關閉',data:{md['C_GATE']},backgroundColor:'rgba(120,120,120,0.22)',borderWidth:0,stack:'s'}}
  ]}},
  options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:true,position:'bottom',labels:{{usePointStyle:true,pointStyle:'rect',padding:10,boxWidth:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.x.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{stacked:true,min:0,max:100,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}}}}}},
      y:{{stacked:true,grid:{{display:false}}}}}}
  }}
}});

var W_LAB_{suf}={H['labels']},W_SRC_{suf}={H['src']};
function segDash_{suf}(ctx){{return W_SRC_{suf}[ctx.p1DataIndex]==='live'?undefined:[3,3];}}
new Chart(document.getElementById('chart-weights-{suf}'),{{
  type:'line',
  data:{{labels:W_LAB_{suf},datasets:[
    {{label:'合成執行',data:{H['cexe']},borderColor:GREEN,backgroundColor:'rgba(22,163,74,0.09)',
     borderWidth:2.8,stepped:true,pointRadius:0,pointHoverRadius:3,fill:'origin',segment:{{borderDash:segDash_{suf}}}}},
    {{label:'{legs[0]} 執行',data:{H['aexe']},borderColor:BLUE,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash_{suf}}}}},
    {{label:'{legs[1]} 執行',data:{H['bexe']},borderColor:AMBER,borderWidth:2,stepped:true,pointRadius:0,pointHoverRadius:3,segment:{{borderDash:segDash_{suf}}}}},
    {{label:'合成目標（理論）',data:{H['comb']},borderColor:'rgba(22,163,74,0.40)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}},
    {{label:'{legs[0]} 目標',data:{H['a']},borderColor:'rgba(21,101,192,0.35)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}},
    {{label:'{legs[1]} 目標',data:{H['b']},borderColor:'rgba(217,119,6,0.35)',borderWidth:1,pointRadius:0,pointHoverRadius:2,tension:0.15}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:12}}}},
      tooltip:{{callbacks:{{title:function(c){{return c[0].label+' · '+(W_SRC_{suf}[c[0].dataIndex]==='live'?'每日實錄':'規則回放')}},
        label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{min:0,max:100,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});

new Chart(document.getElementById('chart-rv-{suf}'),{{
  type:'line',
  data:{{labels:W_LAB_{suf},datasets:[
    {{label:'{legs[0]} D20 下跌波動',data:{H['arv']},borderColor:BLUE,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{legs[1]} D20 下跌波動',data:{H['brv']},borderColor:AMBER,borderWidth:1.6,pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{legs[0]} σ_t（動態）',data:{H['asig']},borderColor:'rgba(21,101,192,0.55)',borderWidth:1.4,borderDash:[6,4],pointRadius:0,pointHoverRadius:3,tension:0.15}},
    {{label:'{legs[1]} σ_t（動態）',data:{H['bsig']},borderColor:'rgba(217,119,6,0.55)',borderWidth:1.4,borderDash:[6,4],pointRadius:0,pointHoverRadius:3,tension:0.15}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{display:true,position:'top',align:'start',labels:{{usePointStyle:true,pointStyle:'line',padding:10}}}},
      tooltip:{{callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(1)+'%'}}}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{maxTicksLimit:12,font:{{size:10}},maxRotation:0,autoSkip:true}}}},
      y:{{beginAtZero:true,grid:{{color:'rgba(0,0,0,0.06)'}},ticks:{{callback:function(v){{return v+'%'}},font:{{size:10}}}}}}}}
  }}
}});

{_cmp_chart_js(suf, md.get('cmp'))}
"""


# ---------------------------------------------------------------------------
# Full HTML
# ---------------------------------------------------------------------------
def generate_html(sigs: dict, changes: list | None, last_change_date: str | None,
                  hist_map: dict, exec_map: dict, main_state: dict | None = None) -> str:
    changes = changes or []
    main_state = main_state or {}
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    data_date = max(sigs[t]["wk_date"] for t in ALL_TICKERS)
    # 週線 bar 由 pandas 以「週結束的週五」為標籤，週間跑時 data_date 為本週五（尚未到）。
    # 用日線最新交易日判斷本週是否已收：daily < 週五標記＝進行中，誠實標暫定不寫「週五收盤」。
    daily_dates = [hist_map[m["key"]][-1]["date"] for m in MARKETS if hist_map.get(m["key"])]
    latest_daily = max(daily_dates) if daily_dates else data_date
    week_provisional = latest_daily < data_date
    data_asof_label = (
        f"數據截至 {latest_daily}（本週最新交易日｜週線 bar 進行中，週五 {data_date} 收盤前為暫定）"
        if week_provisional else
        f"數據截至 {data_date}（週五收盤）")

    md_map = {m["key"]: _market_data(m, sigs, hist_map.get(m["key"], []), exec_map[m["key"]]) for m in MARKETS}
    md_tw = md_map["tw"]
    exp_tw = md_tw["combined"]
    cmp = main_vs_shadow_series(hist_map.get("tw", []), exec_map["tw"], main_state)
    md_tw["cmp"] = cmp
    md_tw["cmp_card_html"] = _cmp_card_html("tw", cmp)
    md_tw["main_snapshot_html"] = main_snapshot_card(main_state)

    change_html = (
        ('<div style="background:var(--red-bg);border:2px solid var(--red-border);border-radius:10px;'
         'padding:.9rem 1.2rem;margin:.5rem 0 1rem;font-size:.9rem"><b style="color:var(--red-text)">'
         '可行動變化</b><br>' + "<br>".join(changes) +
         '<br><span style="font-size:.78rem;color:var(--muted)">下一個交易日將部位調整至上列目標。</span></div>')
        if changes else
        ('<div style="text-align:center;font-size:.78rem;color:var(--muted);margin:.3rem 0 1rem">'
         '無可行動變化（兩腿閘門未翻轉、且無標的目標與現持差 ≥ 20pp——本頁無 email，僅供對照）' +
         (f'（上次變化：{last_change_date}）' if last_change_date else '') + '</div>'))

    markets_html = "\n".join(market_html(m, sigs, md_map[m["key"]]) for m in MARKETS)
    markets_js = "\n".join(market_js(m, md_map[m["key"]]) for m in MARKETS)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>台股 B-ii 影子追蹤（下跌半變異套袖）| InvestMQuest Research</title>
  <meta name="description" content="台股 0050+2330 · 週線 W52 單線閘門 × B-ii 下跌半變異套袖 × cap 1.5 執行層 A2 · 唯讀影子追蹤頁（2026-08-17 用戶決定不採用為實單規則，僅台股腿套袖分母不同、其餘與實單主系統完全相同）· 無 email">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
  <style>
:root{{--brand:#0d2244;--bg:#f7f3ea;--card:#ffffff;--text:#0c1521;--muted:#9aa7b8;--border:#e5dfd0;
  --green:#15803d;--green-bg:#eafaef;--green-border:var(--line);--green-text:#15803d;
  --red:#b91c1c;--red-bg:#fbeceb;--red-border:var(--line);--red-text:#b91c1c;
  --amber:#a16207;--amber-bg:#fbf3df;--amber-border:var(--line);--amber-text:#a16207;
  --blue:#1d4ed8;--blue-bg:#e8eef5;--blue-border:var(--line);--blue-text:#1d4ed8}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.65;font-size:14px}}
a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:1140px;margin:0 auto;padding:0 1.5rem}}
.page-hdr{{padding:1.5rem 0 1.2rem;background:var(--card);border-bottom:1px solid var(--border)}}
.page-hdr h1{{font-family:var(--serif);font-size:1.5rem;font-weight:700;letter-spacing:-.01em}}
.page-hdr .sub{{color:var(--muted);font-size:.85rem;margin-top:.2rem}}
.crumb{{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}}
.crumb a{{color:var(--muted)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;margin-bottom:1rem;box-shadow:var(--sh-1)}}
.card h3{{font-size:.95rem;font-weight:600;margin-bottom:.75rem}}
.card .takeaway{{font-size:.82rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:8px;background:#f6f8fb;border-left:3px solid var(--brand)}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th,td{{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}}
th{{background:transparent;font-family:var(--mono);font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}
td{{font-variant-numeric:tabular-nums}}
td.num,th.num{{text-align:right}}
.pos{{color:var(--green);font-weight:600}}.neg{{color:var(--red);font-weight:600}}
.rowhl td{{background:#eef3fb!important}}.rowbh td{{background:#faf7f0;color:var(--muted)}}
tbody tr:hover td{{background:#fbf8f1}}
.tag{{display:inline-block;padding:.12rem .5rem;border-radius:6px;font-size:.7rem;font-weight:600}}
footer{{background:var(--card);border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1rem 0;font-size:.75rem;margin-top:1rem}}
.mkt-hd{{margin:1.6rem 0 .8rem;border-bottom:2px solid var(--brand);padding-bottom:.4rem}}
.mkt-tag{{font-family:var(--serif);font-size:1.15rem;font-weight:700;color:var(--brand)}}
.status-hero{{padding:1.4rem 0 1rem;text-align:center}}
.status-badge{{display:inline-flex;align-items:center;gap:.75rem;padding:.8rem 2rem;border-radius:var(--r);font-size:1.15rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.5rem}}
.status-badge .dot{{width:14px;height:14px;border-radius:50%;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.status-exposure{{font-size:2.4rem;font-weight:800;margin:.3rem 0}}
.status-date{{font-size:.8rem;color:var(--muted)}}
.hero-green .status-badge{{background:var(--green-bg);color:var(--green-text);border:2px solid var(--green-border)}}
.hero-green .dot{{background:var(--green)}}.hero-green .status-exposure{{color:var(--green)}}
.hero-blue .status-badge{{background:var(--blue-bg);color:var(--blue-text);border:2px solid var(--blue-border)}}
.hero-blue .dot{{background:var(--blue)}}.hero-blue .status-exposure{{color:var(--blue)}}
.hero-amber .status-badge{{background:var(--amber-bg);color:var(--amber-text);border:2px solid var(--amber-border)}}
.hero-amber .dot{{background:var(--amber)}}.hero-amber .status-exposure{{color:var(--amber)}}
.hero-red .status-badge{{background:var(--red-bg);color:var(--red-text);border:2px solid var(--red-border)}}
.hero-red .dot{{background:var(--red)}}.hero-red .status-exposure{{color:var(--red)}}
.dual-stat{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}}
.dual-stat .ds{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1rem 1.2rem;text-align:center;box-shadow:var(--sh-1)}}
.dual-stat .ds .dsn{{font-size:1.9rem;font-weight:800;letter-spacing:-.02em}}
.dual-stat .ds .dsl{{font-size:.76rem;color:var(--muted);margin-top:.2rem}}
.tgrid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem}}
.tcard{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem;box-shadow:var(--sh-1)}}
.tcard-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.2rem}}
.tname{{font-size:1.3rem;font-weight:800;letter-spacing:-.02em}}
.pos-badge{{font-size:.95rem;font-weight:700;padding:.25rem .7rem;border-radius:6px}}
.pos-green{{background:var(--green-bg);color:var(--green-text)}}.pos-blue{{background:var(--blue-bg);color:var(--blue-text)}}
.pos-amber{{background:var(--amber-bg);color:var(--amber-text)}}.pos-red{{background:var(--red-bg);color:var(--red-text)}}
.tcard-sub{{font-size:.75rem;color:var(--muted);margin-bottom:.75rem}}
.sig-row{{display:grid;grid-template-columns:1fr;gap:.5rem}}
.sig{{border:1px solid var(--border);border-radius:var(--r);padding:.55rem .7rem;background:var(--card)}}
.sig.on{{border-color:var(--green-border);background:var(--green-bg)}}
.sig.off{{border-color:var(--red-border);background:var(--red-bg)}}
.sig-top{{display:flex;align-items:center;gap:.5rem}}
.sig-dot{{width:11px;height:11px;border-radius:50%}}
.sig.on .sig-dot{{background:var(--green)}}.sig.off .sig-dot{{background:var(--red)}}
.sig-name{{font-weight:700;font-size:.85rem}}
.sig-mark{{margin-left:auto;font-weight:800}}
.sig.on .sig-mark{{color:var(--green)}}.sig.off .sig-mark{{color:var(--red)}}
.sig-detail{{font-size:.74rem;color:var(--muted);margin-top:.2rem;font-variant-numeric:tabular-nums}}
.oos-banner{{background:linear-gradient(135deg,#fdf6e3 0%,#faf0d7 100%);border:2px solid var(--amber);border-radius:12px;padding:1rem 1.3rem;margin:1rem 0}}
.oos-banner .tag-loud{{display:inline-block;background:var(--amber);color:#fff;font-size:.72rem;font-weight:800;letter-spacing:.06em;padding:.22rem .7rem;border-radius:99px;margin-bottom:.45rem}}
.oos-banner b{{color:var(--amber-text)}}
.rule-list{{font-size:.82rem;line-height:1.9}}.rule-list b{{color:var(--text)}}
.chart-wrap{{position:relative;width:100%;height:400px}}
.chart-wrap-sm{{position:relative;width:100%;height:300px}}
.chart-wrap-xs{{position:relative;width:100%;height:210px}}
.viz-split{{display:grid;grid-template-columns:260px 1fr;gap:1.25rem;align-items:center}}
.gauge-box{{position:relative;width:100%;max-width:240px;margin:0 auto;height:150px}}
.gauge-center{{position:absolute;left:0;right:0;bottom:6px;text-align:center}}
.gauge-center .g-num{{font-size:2.1rem;font-weight:800;line-height:1;letter-spacing:-.02em}}
.gauge-center .g-lab{{font-size:.7rem;color:var(--muted);margin-top:.15rem}}
.legend-note{{font-size:.74rem;color:var(--muted);margin-top:.6rem;display:flex;gap:1.2rem;flex-wrap:wrap;align-items:center}}
.legend-note .ln-item{{display:inline-flex;align-items:center;gap:.35rem}}
.legend-note .ln-line{{display:inline-block;width:22px;height:0;border-top:2.4px solid var(--muted)}}
.legend-note .ln-dash{{border-top-style:dashed}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
@media(max-width:768px){{.tgrid{{grid-template-columns:1fr}}.status-exposure{{font-size:2rem}}table{{font-size:.74rem}}th,td{{padding:.4rem .45rem}}
  .viz-split{{grid-template-columns:1fr}}.grid2{{grid-template-columns:1fr}}.dual-stat{{grid-template-columns:1fr}}.chart-wrap{{height:320px}}}}
</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/long-track-w52-adaptive/">W52 × 自適應波動率（實單主系統）</a> / 台股 B-ii 影子追蹤</div>
    <h1>台股 B-ii 影子追蹤 — 下跌半變異套袖</h1>
    <div class="sub">台股 0050+2330 · 週線 W52 單線閘門 × <b>B-ii 下跌半變異套袖</b> × cap 1.5 × 執行層 A2 · <b>唯讀影子追蹤頁</b>：與<a href="/long-track-w52-adaptive/">實單主系統</a>訊號完全相同、<b>唯一差異＝台股腿套袖分母改用下跌半變異 D20</b>（美股不在本頁範圍）· 無獨立 email · 不構成倉位建議</div>
    <div style="margin-top:.6rem;display:flex;gap:.4rem;flex-wrap:wrap">
      <a href="/long-track-w52-adaptive/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">實單主系統 cap 1.5</a>
      <a href="/long-track-w52-adaptive/leverage.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">cap 1.0 影子對照</a>
      <a href="/long-track-w52-adaptive/tw-semivol.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border-radius:6px;background:var(--text);color:#fff;text-decoration:none">台股 B-ii 影子（本頁）</a>
      <a href="/backtest/vol_targeting/tw.html" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">台股變體實驗室</a>
      <a href="/long-track-tw/" style="font-size:.82rem;font-weight:600;padding:.35rem .8rem;border:1px solid var(--border);border-radius:6px;color:var(--muted);text-decoration:none">台股長線 2330/0050（舊實倉・對照）</a>
    </div>
  </div>
</div>
<div class="container">

<div class="oos-banner">
  <span class="tag-loud">唯讀影子追蹤・無 email・不構成倉位建議</span>
  <div style="font-size:.86rem"><b>2026-08-17 用戶決定：不採用 B-ii 為實單規則</b>（見 v7-backtest <code>docs/Adaptive_Sigma_Spec.md</code> 2026-08-17「決策記錄」章節）——預註冊判準未全數過關：<b>台股主戰場 5/5 週線錨點勝出</b>（Calmar 中位數 1.030→1.282），但<b>美股對照 0/5 錨點勝出</b>、<b>含 2008 GFC 的 2330 長窗 MDD 反而加深 3~5pp</b>、2024-08 急跌後崩情境更差、執行層調整頻率 +30%。實單主系統（美股／台股）維持 RV20 分母不變。本頁作為<b>唯讀影子追蹤</b>保留：訊號與實單主系統<b>逐位元相同</b>（W52 單線閘門 × cap 1.5 × 執行層 A2），<b>唯一差異＝台股腿套袖分母改用下跌半變異 D20</b>（見下方公式卡）。
  每交易日台股收盤後更新，<b>本頁無獨立 email</b>——可行動變化通知一律由<a href="/long-track-w52-adaptive/">實單主系統</a>覆蓋，本頁僅供人工複審對照。複審時點見下方「為什麼是影子不是實盤」。</div>
</div>

<div class="dual-stat" style="grid-template-columns:1fr">
  <div class="ds"><div class="dsn hero-{md_tw['ccol']}" style="color:var(--{md_tw['ccol']})">{exp_tw:.0f}%</div><div class="dsl">台股 0050+2330 組合目標曝險（B-ii，本頁）</div></div>
</div>
<div class="status-date" style="text-align:center;margin-bottom:.5rem">{data_asof_label} · 頁面更新 {now} 台北時間 · cap 1.5（150% 上限）</div>

{change_html}

{markets_html}

<div class="card">
<h3>追蹤主系統規則（W52 × 自適應波動率；{FREEZE_DATE} 定案，此後不再調整）</h3>
<div class="rule-list">
① <b>兩腿、台股單一市場</b>：0050、2330 各 50%（.TW，內嵌幻影分割修復），日報酬 50/50 加權合成（<b>絕不直接相加 equity curve</b>）。本頁不追蹤美股。<br>
② <b>週線 W52 單線閘門</b>（W-FRI）：<b>週收盤 &gt; SMA52w 在場、&lt; SMA52w 出場</b>；<b>無 W104／W250 斜率滯後條件</b>；<b>長多 only</b>，閘門輸出 0／1。與實單主系統逐位元相同。<br>
③ <b>B-ii 下跌半變異套袖（本頁與主系統唯一差異）</b>：r＝日對數報酬；<b>D20 ＝ √2 × sqrt(mean_20d(min(r,0)²)) × √252</b>（只計下跌日、年化）；σ_t＝D20 的 <b>rolling(756, min_periods=252).median()</b>（近 3 年中位數）；<b>w = clip(σ_t／D20, upper=1.5)</b>——分母排除上漲造成的波動，且<b>可加碼到 150%</b>（真波動率目標，非「只降不加」）。實單主系統分母為 RV20（全波動、只降不加，上限 1.0 再乘 cap）。<br>
④ <b>機制與視窗</b>：W52 閘門、滾動中位數 3 年（756／252）與實單主系統相同、皆已凍結；本頁的套袖分母是唯一未凍結入實單規則的部分（見上方 banner）。<br>
⑤ <b>執行</b>：t 收盤訊號、t+1 收盤生效；成本 7 bps／邊。<br>
⑥ <b>最終權重</b> = 0.5 × 閘門(0/1) × 套袖權重（B-ii），兩腿各自計算，cap 1.5。<br>
⑦ <b>資料揭露</b>：yfinance auto-adjust（還原股價）；0050.TW 2014-01-02 幻影分割壞 bar 由腳本自動修復（回溯縮放，門檻單日 ±40%，台股漲跌停 ±10% 不可能誤觸）；0050 免費歷史約 2009 起。台股 2330 佔 0050 約五成，50/50 組合等效台積電曝險 ≈ 75%，非分散組合。<br>
⑧ <b>執行層 A2（同實單主系統）</b>：|目標 − 現持| ≥ 20pp 才調整，調整取整至 10% 格、再 clamp 於 50×cap（cap1.5→75pp／單腿）；<b>回測主數字含此執行層</b>，與追蹤操作同規則。<br>
<span style="color:var(--muted);font-size:.78rem">閘門為週頻（僅週五可能翻轉），套袖 D20／σ_t 為日頻（每日可能微調），故本頁每交易日更新（台股收盤後）。本頁<b>無 email</b>——可行動變化只在頁面上顯示，不觸發通知。</span>
</div>
</div>

<div class="card">
<details>
<summary style="cursor:pointer;font-weight:600;font-size:.9rem">規則沿革（歷次凍結後的變更紀錄）</summary>
<div class="rule-list" style="font-size:.82rem;margin-top:.75rem">
• <b>2026-07-17</b>：實單主系統規則凍結——W52 單線閘門 × 自適應 σ_t（RV20 近三年滾動中位數，756／252）定案，此後不掃參擇優、不改機制形狀、不加濾網。<br>
• <b>2026-07-22</b>：實單主系統執行層由 10pp 門檻／5% 取整改為現行 A2（20pp 門檻／10% 取整／取整後 clamp）。<br>
• <b>2026-08-17</b>：預註冊「B 下跌半變異分母」研究完成（台股主戰場 5/5 錨點勝出、美股對照 0/5 勝出），用戶決定<b>不採用為實單規則</b>；本頁作為唯讀影子追蹤頁建立，全程以 B-ii 回放近 1260 交易日，此後 CI 逐日追加實錄。詳見 v7-backtest <code>docs/Adaptive_Sigma_Spec.md</code> 2026-08-17 章節。<br>
</div>
</details>
</div>

<div class="card" style="border:2px solid var(--amber-border);background:var(--amber-bg)">
<h3 style="color:var(--amber-text)">為什麼是影子不是實盤（誠實揭露，必讀）</h3>
<div class="rule-list" style="font-size:.82rem">
① <b>預註冊判準未全數過關</b>：本頁改分母的決策前已預先訂好判準（Calmar／Martin、MDD 不惡化、五錨點中位數、含 2008 GFC 的 2330 長窗、曝險統計），事後不得挑對自己有利的子集。結果——<b>台股主戰場 5/5 週線錨點勝出</b>（B-ii Calmar 中位數 1.030→1.282、全距收窄至 0.244），但<b>美股對照 0/5 錨點勝出</b>；<b>含 2008 GFC 的 2330 長窗 MDD 由約 −38.7% 加深至 −41.8%（+3.1pp）</b>；2024-08 急漲後崩情境同樣更差；執行層調整頻率約 +30%（B-ii 分母對上漲不敏感，反彈段維持較高曝險，跌破時减碼更慢）。<br>
② <b>只有台股單一市場證據，機制未經跨市場驗證</b>：B-ii 排除「上漲造成的波動」，在台股（2330 權值集中、單一巨型成長股驅動的長多段）恰好吃到這個特性的紅利；美股（QQQ/SMH，成分更分散）沒有同樣效果，暗示台股結果可能是<b>結構偶合而非普遍規律</b>，不足以改動兩市場共用的機制規則。<br>
③ <b>本頁上線本身已是誠實的路徑運氣提醒</b>：五個週線錨點（W-MON…W-FRI）裡，本頁追蹤所用的 <b>W-FRI 是五者中最幸運的一支</b>（2026-08-02 timing-luck 稽核），上方回測表「本頁影子追蹤」列不宜當五錨點代表值。<br>
④ <b>複審時點與翻案條件</b>：<b>2027-01</b>，或<b>台股（0050/2330 任一腿）出現第一次 ≥10% 從高點回落</b>，兩者先到者為準。屆時比較本頁與實單主系統在同一窗口的<b>執行層 Calmar／MDD／回撤深度</b>——若本頁在真實下跌事件中同時做到「MDD 不劣於主系統」與「Calmar 優於主系統」，才重新考慮是否採用；任一項不滿足則維持影子，不再另立新判準。
</div>
</div>

{appendix_2330_section()}

</div>
<footer class="imq-foot">
  <div>&copy; {datetime.now().year} InvestMQuest Research · 台股 B-ii 影子追蹤（唯讀・實單主系統見 /long-track-w52-adaptive/）</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
<script>
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;
var GREEN="#16a34a",BLUE="#1565c0",AMBER="#d97706";
function _dd(nav){{var dd=[],pk=0;for(var i=0;i<nav.length;i++){{if(nav[i]>pk)pk=nav[i];dd.push((nav[i]/pk-1)*100);}}return dd;}}
{markets_js}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# change detection
# ---------------------------------------------------------------------------
def detect_changes(prev: dict, sigs: dict) -> list:
    """可行動變化＝任一腿閘門翻轉，或 |今日目標 − 現持（執行層 executed_pct）| ≥ 20pp
    （執行層 A2，2026-07-22 升格）。改為與現持比（非與前一日目標比），才不會漏掉緩慢累積的漂移；alert 顯示取整後的
    建議動作（現持 → round(目標/5)×5）。訊息標市場前綴（美股／台股）。"""
    if not prev or "tickers" not in prev:
        return []
    out = []
    for t in ALL_TICKERS:
        pt = prev["tickers"].get(t)
        if not pt:
            continue
        gate_flip = bool(pt.get("gate")) != bool(sigs[t]["gate"])
        target = round(sigs[t]["final"] * 100, 1)
        held = pt.get("executed_pct")
        drift = held is not None and abs(target - held) >= EXEC_BAND
        if gate_flip or drift:
            new_exec = min(round(target / EXEC_GRID) * EXEC_GRID, EXEC_CLAMP)
            parts = []
            if gate_flip:
                parts.append("閘門 " + ("出場→在場" if sigs[t]["gate"] else "在場→出場"))
            arrow = (f"最終權重 {held:.0f}% → {new_exec:.0f}%"
                     if held is not None else f"最終權重 → {new_exec:.0f}%")
            out.append(f"<b>{TICKER_MARKET[t]} {t}</b>：{'、'.join(parts) + ' → ' if parts else ''}{arrow}")
    return out


def main():
    prev_state = {}
    if STATE_JSON.exists():
        try:
            prev_state = json.loads(STATE_JSON.read_text())
        except Exception:
            prev_state = {}

    px_map, sigs = {}, {}
    for t in ALL_TICKERS:
        print(f"Fetching {YF_SYMBOL[t]}...")
        px_map[t] = fetch_close(t)
        d = compute_ticker(t, px_map[t])
        sigs[t] = d
        print(f"  {t}: gate={'IN' if d['gate'] else 'OUT'} D20={d['rv20']*100:.1f}% "
              f"σ_t={d['sigma_t']*100:.1f}% sleeve={d['sleeve']:.2f} -> final {d['final']*100:.0f}%")

    exp = {}
    for m in MARKETS:
        exp[m["key"]] = sum(sigs[t]["final"] for t in m["legs"]) * 100
        print(f"{m['short']} combined target exposure: {exp[m['key']]:.0f}%")

    main_state = load_main_state()

    changes = detect_changes(prev_state, sigs)
    data_date = max(sigs[t]["wk_date"] for t in ALL_TICKERS)

    # ---- per-market history: rule-replay backfill (once) + daily live append ----
    hist_map = {}
    for m in MARKETS:
        legs = m["legs"]
        prev_history = prev_state.get(m["hist_key"], [])
        backfill = build_backfill(px_map, legs) if len(prev_history) < BACKFILL_DAYS else []
        daily_date = max(px_map[t].index[-1] for t in legs)
        today_rec = _daily_record(px_map, legs, daily_date, "live")
        history = merge_history(prev_history, backfill, today_rec)
        hist_map[m["key"]] = history
        print(f"{m['short']} history: {len(history)} days (backfill {len(backfill)}, "
              f"span {history[0]['date']}→{history[-1]['date']})")

    # ---- per-market execution layer replay (deterministic from history) ----
    exec_map = {m["key"]: band_exec_replay(hist_map[m["key"]], m["legs"]) for m in MARKETS}
    exec_last = {}
    for m in MARKETS:
        er = exec_map[m["key"]]
        exec_last.update(er["last"])
        print(f"{m['short']} exec layer: {len(er['events'])} events, current executed " +
              ", ".join(f"{t} {er['last'][t]:.0f}%" for t in m["legs"]))

    # 影子追蹤頁：無 email／alert（本頁不觸發任何通知；可行動變化只顯示在頁面上）；
    # 仍記錄 last_change_date／desc 供頁面 change_html 與 state 對帳用。
    if changes:
        last_change_date = data_date
        last_change_desc = "; ".join(c.replace("<b>", "").replace("</b>", "") for c in changes)
        print(f"CHANGES (shadow, no email): {last_change_desc}")
    else:
        last_change_date = prev_state.get("last_change_date")
        last_change_desc = prev_state.get("last_change_desc")
        print("No actionable change vs last run (shadow).")

    html = generate_html(sigs, changes, last_change_date, hist_map, exec_map, main_state)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes)")

    state_json = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": data_date,
        "ruleset_locked_date": FREEZE_DATE,
        "sleeve_switch_date": SLEEVE_SWITCH_DATE,
        "mechanism": "W52 single-line gate x B-ii downside-semivariance sleeve (D20 rolling(756,252) median ratio) x cap 1.5 x exec layer A2 20pp/10%round/clamp75 (scale 0~150)",
        "status": "TW-only READ-ONLY SHADOW tracking page (not adopted as live rule, 2026-08-17 user decision); no email; review point 2027-01 or TW first >=10% drawdown",
        "not_a_live_signal": True,
        "last_change_date": last_change_date,
        "last_change_desc": last_change_desc,
        "weights": WEIGHTS,
        "combined_exposure_tw_pct": round(exp["tw"], 1),
        "tickers": {
            t: {
                "market": TICKER_MARKET[t],
                "gate": sigs[t]["gate"],
                "sigma_t_pct": round(sigs[t]["sigma_t"] * 100, 2),
                "rv20_pct": round(sigs[t]["rv20"] * 100, 2),
                "raw_ratio": round(sigs[t].get("raw_ratio", sigs[t]["sleeve"]), 4),
                "sleeve_weight": round(sigs[t]["sleeve"], 4),
                "sleeve_variant": sigs[t].get("sleeve_variant", "semivol_bii"),
                "final_weight_pct": round(sigs[t]["final"] * 100, 1),
                "executed_pct": exec_last[t],
                "wk_date": sigs[t]["wk_date"],
                "wk_close": round(sigs[t]["wk_close"], 2),
                "w52": round(sigs[t]["w52"], 2),
                "w104": round(sigs[t]["w104"], 2),
                "w250": round(sigs[t]["w250"], 2),
                "s104_pos": sigs[t]["s104_pos"],
                "s250_pos": sigs[t]["s250_pos"],
            } for t in ALL_TICKERS
        },
        "history_tw": hist_map["tw"],
    }
    STATE_JSON.write_text(json.dumps(state_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


if __name__ == "__main__":
    main()
