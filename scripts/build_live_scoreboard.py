#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_live_scoreboard.py — 實單前瞻記分板（PREREG 2026-09-05）。

WHAT THIS IS
------------
凍結規格：/Users/ivanchang/v7-backtest/docs/Live_Scoreboard_Spec.md（原樣抄錄於
本檔 PREREG dict，並寫入輸出 JSON 供稽核）。三條 kill condition 都是回看歷史算
的，歷史回測數字以後不會再變；唯一會隨時間累積新證據的是實錄。本頁把 kill
condition 變成日更的前瞻記分：只用 docs/long-track-w52-adaptive/state.json 的
source=='live' 日紀錄，每月一個樣本，問「系統這個月有沒有贏過同標的的稀釋
B&H」，走與市況曝險 paper track（build_exposure_track.py）完全相同的 SPRT 淘汰
賽（復用 scripts/score_flowmap.py 的 sprt_with_latch，非另開一份可能漂移的複
製邏輯）。

不是收斂面：不產名單、不下買賣指令；判紅只是「證據累積到該檢討」，動作由持
有人決。

不做的事（PREREG）：不調 k、不調 SPRT 參數、不因回測結果改口徑；不在頁面寫
任何配置或停單建議。

輸出
----
- docs/market/data/live_scoreboard.json（機械資料，供頁面渲染與稽核）
- docs/long-track/_scoreboard_body.html（nav-less iframe 片段，嵌入
  /long-track/#live，緊接在 _body.html 之後——比照
  docs/long-track-w52-adaptive/_body.html 的既有慣例）

FAIL-SAFE：任何資料缺口／例外一律 print 警告、exit 0、兩個輸出檔完全不動
（鏡射 build_exposure_track.py／build_trend_track.py 的既有慣例）。
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STATE_JSON = DOCS / "long-track-w52-adaptive" / "state.json"
OUT_JSON = DOCS / "market" / "data" / "live_scoreboard.json"
OUT_BODY = DOCS / "long-track" / "_scoreboard_body.html"

sys.path.insert(0, str(ROOT / "scripts"))
import score_flowmap as _sf  # noqa: E402  (top-level imports stdlib-only; reuse SPRT helper + latch)
import update_long_track_w52_adaptive as _w52  # noqa: E402  (reuse fetch_close / band_exec_replay / WEIGHTS)
import _crossasset_frozen as _d1  # noqa: E402  (S-F 影子帳戶 D1 腿；凍結搬運自 v7-backtest，見檔頭 docstring)

SCHEMA = "live-scoreboard-v0"

# ═══════════════════════════════════════════════════════════════════════
# CONFIG — PREREG 凍結（Live_Scoreboard_Spec.md；不得依單一案例調參）
# ═══════════════════════════════════════════════════════════════════════

MARKETS = [
    {
        "key": "us", "label": "美股", "hist_key": "history_us",
        "legs": _w52.US_TICKERS,
        "cash_ticker": "^IRX",  # 13-week T-bill 殖利率（年化 %），yfinance 直抓
        "k_cagr": 0.72, "k_mdd": 0.56,   # E-cagr/E-mdd k（US W2 主判準窗，2010 起）
    },
    {
        "key": "tw", "label": "台股", "hist_key": "history_tw",
        "legs": _w52.TW_TICKERS,
        "cash_ticker": None,  # 台股現金率＝固定 1%/年（凍結口徑，非市場利率）
        "k_cagr": 0.86, "k_mdd": 0.44,   # E-cagr/E-mdd k（TW1 主判準窗，2014 起）
    },
]

TW_CASH_ANNUAL = 0.01
BORROW_SPREAD_ANNUAL = 0.015     # 借款部分 1.5%/年
TURNOVER_COST_FRAC = 0.0007      # 7 bps
TRADING_DAYS = 252

# ═══════════════════════════════════════════════════════════════════════
# 影子帳戶 CONFIG（PREREG 凍結；v7-backtest/docs/Shadow_Tracks_Spec.md）
# ═══════════════════════════════════════════════════════════════════════
S60_K = 0.6                # S-60：同標的 50/50 B&H 固定 60% + 現金 40%
SA10_CAP = 1.0              # S-A10：cap 1.0（無槓桿），leg weight = gate × min(1, raw_ratio)
SA10_CLAMP = 50.0 * SA10_CAP  # 執行層 clamp（A2 同門檻/格，clamp 隨 cap 改為 50pp／腿）

SHADOW_DEFINITIONS = {
    "s60": "S-60：同標的 50/50 B&H 固定 60% ＋ 現金 40%，月再平衡，7 bps（保險價格頁 E-60 的事前可執行版本）。",
    "sf": "S-F：50% 系統實錄 NAV ＋ 50% D1（SPY/TLT/GLD/DBC 等權、E3 趨勢＋Chandelier 半倉閘門，逐日重算），月再平衡，7 bps。僅美股。",
    "sa10": "S-A10：系統規則但 cap 1.0（無槓桿），執行層同 A2（20pp 門檻／10% 取整），clamp 改為 50pp／腿。",
}

SHADOW_SPRT_TEXT = (
    "每條影子帳戶對「系統實錄」各一條 SPRT（同參數：p0=0.5／p1=0.65／α=0.05／β=0.10、"
    "n_eff floor 20；月樣本；命中＝影子帳戶月報酬 > 系統月報酬）——方向與主記分板（系統 vs "
    "稀釋基準）相反：這裡問「如果當初選了這條影子，會不會比現在的系統好」。判定：綠＝影子帳戶"
    "實錄勝過系統（回顧點的反事實證據）；紅＝系統勝過該影子；黃＝進行中。任何判定都不觸發帳本"
    "動作——影子帳戶是回顧點的資訊，不是 kill condition。"
)

K_SOURCE_NOTE = (
    "k 凍結為 Insurance_Premium_Comparison_Spec.md 的 2010 起主判準窗（US W2：E-cagr "
    "k=0.7193≈0.72／E-mdd k=0.5569≈0.56）與台股 2014 起主窗（TW1：E-cagr "
    "k=0.862≈0.86／E-mdd k=0.4377≈0.44）——results/vol_targeting/insurance_premium.json "
    "轉錄；PREREG 凍結，不隨新資料重解（比照 build_exposure_track.py RV21 gate 常數慣例）。"
)

SPRT_KILL_TEXT = (
    "SPRT（p0=0.5／p1=0.65／α=0.05／β=0.10，n_eff≥20，樣本＝逐月「系統月報酬 − 基準月報酬 "
    "> 0」命中序列）累積 LLR ≤ B(-2.2513) → accept_h0 → 實錄證據支持「系統不比稀釋好」＝"
    "kill condition (d)，登記帳本、持有人檢討；累積 LLR ≥ A(2.8904) → accept_h1 → 帳本記"
    "「前瞻證據轉正」；期間不調參、paper only 永不連實倉。"
)

PREREG = {
    "title": "實單前瞻記分板（PREREG 2026-09-05）",
    "source_doc": "v7-backtest/docs/Live_Scoreboard_Spec.md",
    "frozen_date": "2026-09-05",
    "positioning": (
        "不是回測，是 paper-track 機械層；不是收斂面：不產名單、不下買賣指令；判紅只是"
        "「證據累積到該檢討」，動作由持有人決。"
    ),
    "data": {
        "records": (
            "系統實錄：docs/long-track-w52-adaptive/state.json 的 history_us／history_tw，"
            "只取 source=='live' 的日紀錄；每日四腿的 final_pct 經 band_exec_replay（A2："
            "20pp／10 格／clamp 75）得到執行層持股率（＝實際該持有的部位）。"
        ),
        "daily_return_formula": (
            "系統日報酬 ＝ Σ腿 執行持股率(前一日) × 腿日報酬 ＋ 現金部分 × 現金日率（美 "
            "^IRX／台 1%） − 借款部分 × 1.5%/252 − |Δ執行持股率| × 7 bps。腿日報酬用 "
            "auto-adjust 收盤（與 live 腳本同源 fetch_close）。"
        ),
    },
    "benchmarks": {
        "definition": (
            "兩個基準（每市場，皆固定比例、每月再平衡、成本 7 bps）：B-cagr＝同標的 50/50 "
            "B&H 以現金稀釋到 k＝保險價格頁 W2 的 E-cagr k（美 0.72、台 0.86）；B-mdd＝k＝"
            "E-mdd k（美 0.56、台 0.44）。k 凍結為上述數值，不隨新資料重解。"
        ),
        "k_source": K_SOURCE_NOTE,
        "rebalance": (
            "JUDGMENT CALL：規格文件僅寫「每月再平衡」未明訂月初或月末；本檔採月末再平衡"
            "（本月最後一個 live 交易日，以當日已計入市場變動後的淨值為基礎再平衡回 k，"
            "換手成本＝|實際權重−k|×7bps×淨值）——與 build_exposure_track.py 的 60/40 基準"
            "（月初再平衡、不收成本）刻意不同，因本規格明文要求收成本，月末再平衡讓「當月"
            "報酬」與「再平衡後淨值」在同一天結算，語意較乾淨。"
        ),
    },
    "scoring": {
        "monthly_sample": "月樣本＝當月系統報酬 − 基準月報酬 > 0 為命中（依日曆月分桶，最後一個未走完的月不計）。",
        "sprt": (
            "SPRT 參數逐字沿用 scripts/score_flowmap.py：p0=0.5、p1=0.65、α=0.05、β=0.10、"
            "A=ln(18)=2.8904、B=ln(0.1/0.95)=−2.2513、n_eff floor 20；用 sprt_with_latch；"
            "兩基準各自一條 SPRT，判定以 B-mdd（同風險）為主、B-cagr 並列。"
        ),
        "verdict": {
            "green": "SPRT LLR ≥ A → 實錄支持 edge → 帳本記「前瞻證據轉正」。",
            "yellow": "進行中（樣本不足，n_eff floor 20 個月＝最快 2028 年中才可能判定）。",
            "red": "SPRT LLR ≤ B → 實錄證據支持「系統不比稀釋好」＝kill condition (d)，登記帳本、持有人檢討。",
        },
    },
    "kill_conditions": {"kill_d": SPRT_KILL_TEXT},
    "shadows": {
        "source_doc": "v7-backtest/docs/Shadow_Tracks_Spec.md",
        "positioning": (
            "10 月回顧點無論決定什麼，之後都需要前瞻的、非回測的對照：如果當初改成別的，會怎樣。"
            "三條影子帳戶從同一天起、用同一套實錄與價格、同樣的成本，每天記、每月一個位元。"
            "不是收斂面，任何判定都不觸發帳本動作。"
        ),
        "definitions": SHADOW_DEFINITIONS,
        "coverage": "美股三條（S-60／S-F／S-A10）都跑；台股跑 S-60 與 S-A10（無 D1 腿，spec 明文 D1 僅美股）。",
        "scoring": SHADOW_SPRT_TEXT,
        "no_ledger_action": "任何判定都不觸發帳本動作（spec 明文）——影子帳戶是回顧點的資訊，不是 kill condition。",
        "disclosure": (
            "影子帳戶與系統共用同一段實錄期，樣本同樣只有幾個月；它們的價值在累積，不在現在的數字。"
            "S-F 的 D1 腿是回測期選的規則，影子期是它的第一段 OOS。"
        ),
        "judgment_calls": {
            "d1_cash_proxy": (
                "S-F 的 D1 腿現金部位（TSMOM 比較基準、run_pos_tw 未投入部位的現金報酬）改用 "
                "yfinance 即時抓 SHY 當代理，取代 v7-backtest 原版 SHY→BIL 價格拼接（該拼接來自 "
                "v7 repo 內部 pickle 快照，fab CI 抓不到、也不該跨 repo 讀本機檔案）；SHY 現時仍在"
                "存續中，短率與 BIL 高度貼近，差異遠小於本影子帳戶要看的訊號雜訊。"
            ),
            "d1_vendoring": (
                "fab 這支 repo 的 CI 跑不到 /Users/ivanchang/v7-backtest 本機路徑（既有 v7 相依一律"
                "走「CANONICAL COPY + try/except」或「靜態轉錄常數」慣例，從無跨 repo import）。故將"
                "e3_pos／chand_gate／half_gate／build_signals 等函式逐行搬運進 scripts/_crossasset_frozen.py，"
                "功能上對齊 v7-backtest 對應原始函式（檔頭列出每個函式的搬運來源）。"
            ),
            "sa10_clamp": (
                "S-A10「cap 1.0」翻譯為執行層 clamp＝50pp／腿（cap1.0×50pp 滿載）；A2 的 band=20pp／"
                "grid=10% 逐字沿用（spec 明文「執行層 A2 同」，只有 clamp 隨 cap 改變，非另開一套"
                "執行層參數）。"
            ),
            "sf_rebalance": (
                "S-F 月再平衡的時點採月末再平衡（同主記分板 B-cagr/B-mdd 的既有 JUDGMENT CALL，"
                "維持口徑一致）；換手成本＝|實際權重−0.5|×7bps×淨值。"
            ),
            "s60_rebalance": "S-60 直接重用主記分板既有的 build_diluted(k) 月末再平衡＋7bps 邏輯，k 固定 0.6，不走 k_cagr/k_mdd 兩個 PREREG 凍結值。",
        },
    },
    "disclosure": (
        "誠實預告：n_eff floor 20 個月＝最快 2028 年中才可能判定；本頁上線後大部分時間是"
        "「進行中」。它的價值是把每月的一個位元誠實記下來，而不是在校準點靠回測做決定。"
        "不調 k、不調 SPRT 參數、不因回測結果改口徑；不在頁面寫任何配置或停單建議。"
    ),
}


class FailSafeAbort(Exception):
    pass


def warn(msg):
    print(f"[live-scoreboard][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[live-scoreboard] {msg}")


def month_of(date_str):
    return date_str[:7]


def load_json(path, default=None):
    if not path.exists():
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {path.name}: {e}")
        return default


# ═══════════════════════════════════════════════════════════════════════
# Cash rate series
# ═══════════════════════════════════════════════════════════════════════

def fetch_us_cash_series():
    """^IRX 年化殖利率（%），date -> annual_pct。JUDGMENT CALL：非交易日/缺值
    以前值 forward-fill（週頻更新的短率、缺一兩天用前值合理）。"""
    import yfinance as yf
    df = yf.download("^IRX", period="2y", progress=False, auto_adjust=False)
    if hasattr(df.columns, "get_level_values") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if hasattr(c, "iloc") and c.ndim == 2:
        c = c.iloc[:, 0]
    out = {}
    for ts, v in c.items():
        d = ts.strftime("%Y-%m-%d") if hasattr(ts, "strftime") else str(ts)[:10]
        if v == v:  # not NaN
            out[d] = float(v)
    return out


def cash_daily_return_us(cash_series, dates_sorted, ymd):
    """回傳 ymd 當日的現金日報酬（年化%/100/252），無資料時 forward-fill 最近
    一筆 <= ymd 的年化率；完全查無資料回傳 None（記 gap，該日以 0 代替不捏造）。"""
    best = None
    for d in dates_sorted:
        if d <= ymd:
            best = cash_series[d]
        else:
            break
    if best is None:
        return None
    return (best / 100.0) / TRADING_DAYS


def fetch_usdtwd_series():
    """TWD=X 收盤（TWD per USD）。JUDGMENT CALL：直接 yfinance 即時抓，不用
    v7-backtest six_state_backtest/data/TWD_X.pkl（該檔案是 v7-backtest repo 內
    部快照、fab CI 跑不到跨 repo 路徑，且已停留在 2026-06-25 明顯落後——與
    results/vol_targeting 數字用「轉錄常數」處理的慣例不同，這裡選即時抓取因
    為匯率是連續每日變動量，轉成一次性常數會系統性失真）。"""
    import yfinance as yf
    df = yf.download("TWD=X", period="2y", progress=False, auto_adjust=False)
    if hasattr(df.columns, "get_level_values") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if hasattr(c, "iloc") and c.ndim == 2:
        c = c.iloc[:, 0]
    out = {}
    for ts, v in c.items():
        d = ts.strftime("%Y-%m-%d") if hasattr(ts, "strftime") else str(ts)[:10]
        if v == v:
            out[d] = float(v)
    return out


def px_at_or_before(series_dict, dates_sorted, ymd):
    best = None
    for d in dates_sorted:
        if d <= ymd:
            best = series_dict[d]
        else:
            break
    return best


# ═══════════════════════════════════════════════════════════════════════
# 影子帳戶：S-A10 執行層重放（同 A2 band/grid，clamp 隨 cap 改變）
# ═══════════════════════════════════════════════════════════════════════

def band_exec_replay_capped(history, legs, weights, clamp):
    """S-A10：對每腿逐日重放執行層，target 用「系統規則但 cap 1.0」——
    weights[t] × (1 if gate else 0) × min(1.0, raw_ratio) × 100（pp）——取代
    _w52.band_exec_replay 用的 final_pct（cap 1.5）。band/grid 逐字沿用 A2
    （_w52.EXEC_BAND=20pp／_w52.EXEC_GRID=10%），只有 clamp 隨 cap 改變。"""
    executed = {t: [] for t in legs}
    cur = {t: 0.0 for t in legs}
    for r in history:
        for t in legs:
            tk = r["tickers"][t]
            gate = bool(tk["gate"])
            raw = float(tk["raw_ratio"])
            target = weights[t] * 100.0 * (1.0 if gate else 0.0) * min(1.0, raw)
            if abs(target - cur[t]) >= _w52.EXEC_BAND:
                new = min(round(target / _w52.EXEC_GRID) * _w52.EXEC_GRID, clamp)
                cur[t] = new
            executed[t].append(cur[t])
    return executed


def leg_daily_returns_generic(mkt, legs, history, live_dates, date_to_idx, executed,
                              px, px_dates, cash_series, cash_dates, gaps, tag):
    """逐字對齊 build_market() 內系統本身 nav_sys 迴圈的日報酬公式，改參數化
    executed 讓 S-A10 可重用同一套簿記（腿報酬×前日執行率＋現金×剩餘比例－借款
    利差×超額比例－換手成本×7bps）。獨立於 build_market 之外，供影子帳戶重用，
    不動 build_market 原本的迴圈（風險最低的加法式改動）。"""
    rows = []
    for d in live_dates:
        idx = date_to_idx[d]
        if idx == 0:
            rows.append({"date": d, "ret": 0.0})
            continue
        prev_row = history[idx - 1]
        prev_d = prev_row["date"]
        exec_prev = {t: executed[t][idx - 1] for t in legs}
        exec_now = {t: executed[t][idx] for t in legs}
        sum_exec_prev = sum(exec_prev.values()) / 100.0

        r_leg = {}
        ok = True
        for t in legs:
            p_now = px[t].get(d) or px_at_or_before(px[t], px_dates[t], d)
            p_prev = px[t].get(prev_d) or px_at_or_before(px[t], px_dates[t], prev_d)
            if p_now is None or p_prev is None or p_prev == 0:
                gaps.append({"market": mkt["key"], "date": d,
                             "reason": f"[{tag}] {t} 缺 {prev_d}→{d} 收盤價，本日報酬計為 0"})
                ok = False
                break
            r_leg[t] = p_now / p_prev - 1.0
        if not ok:
            rows.append({"date": d, "ret": 0.0})
            continue

        if mkt["cash_ticker"] == "^IRX":
            r_cash = cash_daily_return_us(cash_series, cash_dates, d)
            if r_cash is None:
                r_cash = 0.0
        else:
            r_cash = TW_CASH_ANNUAL / TRADING_DAYS

        r_leg_contrib = sum((exec_prev[t] / 100.0) * r_leg[t] for t in legs)
        cash_frac = max(0.0, 1.0 - sum_exec_prev)
        borrow_frac = max(0.0, sum_exec_prev - 1.0)
        turnover_frac = sum(abs(exec_now[t] - exec_prev[t]) for t in legs) / 100.0

        r = (r_leg_contrib + cash_frac * r_cash
             - borrow_frac * (BORROW_SPREAD_ANNUAL / TRADING_DAYS)
             - turnover_frac * TURNOVER_COST_FRAC)
        rows.append({"date": d, "ret": r})
    return rows


def nav_from_returns(rows, inception):
    nav = 100.0
    out = []
    for row in rows:
        if row["date"] != inception:
            nav *= (1.0 + row["ret"])
        out.append({"date": row["date"], "nav": round(nav, 4)})
    return out


# ═══════════════════════════════════════════════════════════════════════
# Per-market build
# ═══════════════════════════════════════════════════════════════════════

def build_market(mkt, state, gaps, judgment_calls):
    key, legs, hist_key = mkt["key"], mkt["legs"], mkt["hist_key"]
    history = state.get(hist_key) or []
    if not history:
        gaps.append({"market": key, "reason": f"state.json 缺 {hist_key}"})
        return None

    history = sorted(history, key=lambda r: r["date"])
    live_rows = [r for r in history if r.get("source") == "live"]
    if not live_rows:
        gaps.append({"market": key, "reason": "尚無 source=='live' 日紀錄，NAV 簿記無法起算"})
        return None

    inception = live_rows[0]["date"]
    data_through = live_rows[-1]["date"]

    # 執行層持股率：對「全史」（回放+實錄）重放 band_exec_replay，取得連續的
    # executed 狀態（實錄第一天之前的執行層延續自回放段，這是實際會被沿用的
    # 起始持股率，不是憑空 0）——逐字沿用 update_long_track_w52_adaptive.py。
    exec_replay = _w52.band_exec_replay(history, legs)
    executed = exec_replay["executed"]  # {leg: [pct,...]} aligned to history order
    date_to_idx = {r["date"]: i for i, r in enumerate(history)}

    # 腿收盤價（auto-adjust，與 live 腳本同源）
    px = {}
    for t in legs:
        s = _w52.fetch_close(t)
        px[t] = {ts.strftime("%Y-%m-%d"): float(c) for ts, c in s.items()}
    px_dates = {t: sorted(px[t].keys()) for t in legs}

    # 現金日率
    if mkt["cash_ticker"] == "^IRX":
        cash_series = fetch_us_cash_series()
        cash_dates = sorted(cash_series.keys())
    else:
        cash_series, cash_dates = None, None

    live_dates = [r["date"] for r in live_rows]

    nav_sys = []
    exec_events = []
    for i, d in enumerate(live_dates):
        idx = date_to_idx[d]
        if idx == 0:
            gaps.append({"market": key, "date": d, "reason": "無前一日可算 t-1 執行層，設為 inception baseline"})
            nav_sys.append({"date": d, "ret": 0.0})
            continue
        prev_row = history[idx - 1]
        prev_d = prev_row["date"]

        exec_prev = {t: executed[t][idx - 1] for t in legs}
        exec_now = {t: executed[t][idx] for t in legs}
        sum_exec_prev = sum(exec_prev.values()) / 100.0

        r_leg = {}
        ok = True
        for t in legs:
            p_now = px[t].get(d) or px_at_or_before(px[t], px_dates[t], d)
            p_prev = px[t].get(prev_d) or px_at_or_before(px[t], px_dates[t], prev_d)
            if p_now is None or p_prev is None or p_prev == 0:
                gaps.append({"market": key, "date": d, "reason": f"{t} 缺 {prev_d}→{d} 收盤價，本日系統報酬計為 0"})
                ok = False
                break
            r_leg[t] = p_now / p_prev - 1.0
        if not ok:
            nav_sys.append({"date": d, "ret": 0.0})
            continue

        if mkt["cash_ticker"] == "^IRX":
            r_cash = cash_daily_return_us(cash_series, cash_dates, d)
            if r_cash is None:
                gaps.append({"market": key, "date": d, "reason": "^IRX 查無 <= 當日資料，現金日率計為 0"})
                r_cash = 0.0
        else:
            r_cash = TW_CASH_ANNUAL / TRADING_DAYS

        r_leg_contrib = sum((exec_prev[t] / 100.0) * r_leg[t] for t in legs)
        cash_frac = max(0.0, 1.0 - sum_exec_prev)
        borrow_frac = max(0.0, sum_exec_prev - 1.0)
        turnover_frac = sum(abs(exec_now[t] - exec_prev[t]) for t in legs) / 100.0

        r_sys = (r_leg_contrib + cash_frac * r_cash
                 - borrow_frac * (BORROW_SPREAD_ANNUAL / TRADING_DAYS)
                 - turnover_frac * TURNOVER_COST_FRAC)
        nav_sys.append({"date": d, "ret": r_sys, "exec_prev": exec_prev, "exec_now": exec_now,
                        "r_leg": r_leg, "r_cash": r_cash, "turnover_frac": turnover_frac})

    # exec-change events within live window（供頁面顯示；沿用 band_exec_replay 全史事件、篩 live 窗）
    exec_events = [e for e in exec_replay["events"] if e["date"] >= inception]

    # NAV 序列（inception=100）
    nav_series = []
    nav = 100.0
    for row in nav_sys:
        if row["date"] != inception:
            nav *= (1.0 + row["ret"])
        nav_series.append({"date": row["date"], "nav": round(nav, 4)})

    # 基準：raw B&H（50/50，不再平衡）＋ B-cagr／B-mdd（50/50 稀釋到 k，月末再平衡，7bps 成本）
    p0 = {t: (px[t].get(inception) or px_at_or_before(px[t], px_dates[t], inception)) for t in legs}
    if any(v is None for v in p0.values()):
        gaps.append({"market": key, "reason": "inception 日缺腿收盤價，無法建基準序列"})
        raw_bh, b_cagr, b_mdd, nav_s60 = [], [], [], []
    else:
        raw_units = {t: 50.0 / p0[t] for t in legs}
        raw_bh = []
        for d in live_dates:
            v = sum(raw_units[t] * (px[t].get(d) or px_at_or_before(px[t], px_dates[t], d)) for t in legs)
            raw_bh.append({"date": d, "nav": round(v, 4)})

        def build_diluted(k):
            out = []
            basket_units = {t: (k * 100.0 / len(legs)) / p0[t] for t in legs}
            cash = (1.0 - k) * 100.0
            prev_d = inception
            for i, d in enumerate(live_dates):
                if d == inception:
                    out.append({"date": d, "nav": 100.0})
                    prev_d = d
                    continue
                basket_val = sum(basket_units[t] * (px[t].get(d) or px_at_or_before(px[t], px_dates[t], d)) for t in legs)
                if mkt["cash_ticker"] == "^IRX":
                    r_c = cash_daily_return_us(cash_series, cash_dates, d) or 0.0
                else:
                    r_c = TW_CASH_ANNUAL / TRADING_DAYS
                cash = cash * (1.0 + r_c)
                nav_pre = basket_val + cash
                is_month_end = (i == len(live_dates) - 1) or (month_of(live_dates[i + 1]) != month_of(d))
                if is_month_end and nav_pre > 0:
                    actual_basket_frac = basket_val / nav_pre
                    turnover = abs(k - actual_basket_frac)
                    cost = turnover * TURNOVER_COST_FRAC * nav_pre
                    nav_post = nav_pre - cost
                    basket_units = {t: (k * nav_post / len(legs)) / (px[t].get(d) or px_at_or_before(px[t], px_dates[t], d)) for t in legs}
                    cash = (1.0 - k) * nav_post
                    out.append({"date": d, "nav": round(nav_post, 4)})
                else:
                    out.append({"date": d, "nav": round(nav_pre, 4)})
                prev_d = d
            return out

        b_cagr = build_diluted(mkt["k_cagr"])
        b_mdd = build_diluted(mkt["k_mdd"])
        nav_s60 = build_diluted(S60_K)   # S-60：同標的 50/50 B&H 固定 60%＋現金 40%，重用同一套月末再平衡＋7bps 邏輯

    # 影子帳戶 S-A10：系統規則但 cap 1.0（無槓桿），執行層同 A2、clamp 改 50pp／腿。
    executed_a10 = band_exec_replay_capped(history, legs, _w52.WEIGHTS, SA10_CLAMP)
    a10_rows = leg_daily_returns_generic(mkt, legs, history, live_dates, date_to_idx,
                                        executed_a10, px, px_dates, cash_series, cash_dates,
                                        gaps, tag="S-A10")
    nav_a10 = nav_from_returns(a10_rows, inception)
    a10_last_exec_pct = {t: executed_a10[t][-1] for t in legs}

    monthly_samples_cagr, n_closed_cagr = compute_monthly_samples(nav_series, b_cagr)
    monthly_samples_mdd, n_closed_mdd = compute_monthly_samples(nav_series, b_mdd)

    prior = (state.get("_live_scoreboard_prior") or {}).get(key, {})
    sprt_cagr = build_sprt_block(monthly_samples_cagr, prior.get("sprt_cagr"))
    sprt_mdd = build_sprt_block(monthly_samples_mdd, prior.get("sprt_mdd"))

    cur_dd_sys = current_drawdown_pct(nav_series)
    cum_diff_cagr = (nav_series[-1]["nav"] - b_cagr[-1]["nav"]) if (nav_series and b_cagr) else None
    cum_diff_mdd = (nav_series[-1]["nav"] - b_mdd[-1]["nav"]) if (nav_series and b_mdd) else None

    return {
        "market": key, "label": mkt["label"], "legs": legs,
        "inception": inception, "data_through": data_through,
        "n_live_days": len(live_rows),
        "nav_sys": nav_series, "nav_b_cagr": b_cagr, "nav_b_mdd": b_mdd, "nav_raw_bh": raw_bh,
        "exec_events": exec_events,
        "monthly_samples_cagr": monthly_samples_cagr, "monthly_samples_mdd": monthly_samples_mdd,
        "n_closed_months": n_closed_mdd,
        "sprt_b_cagr": sprt_cagr, "sprt_b_mdd": sprt_mdd,
        "current_dd_pct": cur_dd_sys,
        "cum_diff_vs_b_cagr": round(cum_diff_cagr, 4) if cum_diff_cagr is not None else None,
        "cum_diff_vs_b_mdd": round(cum_diff_mdd, 4) if cum_diff_mdd is not None else None,
        # 供影子帳戶重用（不進既有渲染/既有下游，純加法）：
        "sys_returns_by_date": {row["date"]: row["ret"] for row in nav_sys},
        "nav_s60": nav_s60,
        "nav_a10": nav_a10,
        "a10_last_exec_pct": a10_last_exec_pct,
    }


def compute_monthly_samples(nav_series, bench_series):
    """依日曆月分桶（同 build_exposure_track.py 慣例），最後未走完的月不計。"""
    if not nav_series or not bench_series:
        return [], 0
    bench_by_date = {r["date"]: r["nav"] for r in bench_series}
    by_month = {}
    order = []
    for row in nav_series:
        m = month_of(row["date"])
        if row["date"] not in bench_by_date:
            continue
        if m not in by_month:
            order.append(m)
        by_month[m] = {"sys": row["nav"], "bench": bench_by_date[row["date"]]}
    closed_months = order[:-1] if len(order) >= 1 else []
    samples = []
    for i in range(1, len(closed_months)):
        m_prev, m_cur = closed_months[i - 1], closed_months[i]
        row_prev, row_cur = by_month[m_prev], by_month[m_cur]
        ret_sys = row_cur["sys"] / row_prev["sys"] - 1.0
        ret_bench = row_cur["bench"] / row_prev["bench"] - 1.0
        hit = (ret_sys - ret_bench) > 1e-12
        samples.append({
            "month": m_cur, "ret_sys_pct": round(ret_sys * 100, 4),
            "ret_bench_pct": round(ret_bench * 100, 4), "hit": bool(hit),
        })
    return samples, len(closed_months)


def build_sprt_block(samples, prior_sprt):
    hit_seq = [s["hit"] for s in samples]
    sprt = _sf.sprt_with_latch(hit_seq, prior_sprt)
    status = _sf.SPRT_STATE_TO_STATUS[sprt["state"]]
    status_label = _sf.sprt_status_label(status, sprt, len(hit_seq))
    return {**sprt, "status": status, "status_label": status_label,
            "n_required": _sf.SPRT_N_EFF_FLOOR, "samples": samples}


def current_drawdown_pct(nav_series):
    if not nav_series:
        return None
    peak = None
    for row in nav_series:
        v = row["nav"]
        if peak is None or v > peak:
            peak = v
    last = nav_series[-1]["nav"]
    return round((last / peak - 1.0) * 100, 4) if peak else 0.0


# ═══════════════════════════════════════════════════════════════════════
# 回測先驗（保險價格頁 W2 月勝率）——不捏造，查無月度序列就寫「未計算」
# ═══════════════════════════════════════════════════════════════════════

def load_backtest_prior(gaps):
    path = Path("/Users/ivanchang/v7-backtest/results/vol_targeting/insurance_premium.json")
    data = load_json(path)
    if not data:
        gaps.append({"reason": "results/vol_targeting/insurance_premium.json 讀不到（跨 repo 路徑，"
                                "CI 環境本來就不會有 v7-backtest checkout），回測先驗一律標未計算"})
        return "未計算（insurance_premium.json 無月度序列可供計算月勝率，查無則不捏造）"
    w2 = (data.get("us_windows") or {}).get("W2") or {}
    if "monthly" not in w2 and "monthly_series" not in w2:
        gaps.append({"reason": "insurance_premium.json us_windows.W2 無 monthly/monthly_series 欄位，"
                                "無法計算月勝率，回測先驗標「未計算」而非捏造"})
        return "未計算（insurance_premium.json 的 W2 窗只有彙總統計，無月度序列可供計算月勝率）"
    return "未計算（月度序列欄位存在但本檔尚未實作抽取邏輯，保守標未計算而非估算）"


# ═══════════════════════════════════════════════════════════════════════
# 兩市場合併（TWD，50/50 月再平衡）
# ═══════════════════════════════════════════════════════════════════════

def build_sf_series(mkt_us, d1_returns, gaps):
    """S-F：50% 系統實錄 NAV ＋ 50% D1，月末再平衡＋7bps（同主記分板 build_diluted
    月末再平衡口徑，但這裡再平衡的兩腿是「系統 NAV」與「D1 NAV」而非個股腿）。"""
    live_dates = [r["date"] for r in mkt_us["nav_sys"]]
    inception = mkt_us["inception"]
    sys_ret = mkt_us["sys_returns_by_date"]
    sys_val, d1_val = 50.0, 50.0
    out = [{"date": inception, "nav": 100.0}]
    for i in range(1, len(live_dates)):
        d = live_dates[i]
        r_sys = sys_ret.get(d, 0.0)
        r_d1 = d1_returns.get(d)
        if r_d1 is None:
            gaps.append({"market": "us", "date": d, "reason": "[S-F] D1 缺當日報酬，計為 0（不捏造）"})
            r_d1 = 0.0
        sys_val *= (1.0 + r_sys)
        d1_val *= (1.0 + r_d1)
        nav_pre = sys_val + d1_val
        is_month_end = (i == len(live_dates) - 1) or (month_of(live_dates[i + 1]) != month_of(d))
        if is_month_end and nav_pre > 0:
            turnover = abs(0.5 - sys_val / nav_pre)
            cost = turnover * TURNOVER_COST_FRAC * nav_pre
            nav_post = nav_pre - cost
            sys_val, d1_val = 0.5 * nav_post, 0.5 * nav_post
            out.append({"date": d, "nav": round(nav_post, 4)})
        else:
            out.append({"date": d, "nav": round(nav_pre, 4)})
    return out


def build_shadow_block(shadow_key, mkt, shadow_nav, prior_sprt):
    """一條影子帳戶對「系統實錄」的月度比較與 SPRT——命中＝影子帳戶月報酬 > 系統
    月報酬（方向與主記分板相反），逐字重用 compute_monthly_samples/build_sprt_block
    （nav_series 傳影子帳戶、bench_series 傳系統，函式本身語意不變，只是誰當
    「基準」互換）。"""
    samples, n_closed = compute_monthly_samples(shadow_nav, mkt["nav_sys"])
    sprt = build_sprt_block(samples, prior_sprt)
    cum_diff = (shadow_nav[-1]["nav"] - mkt["nav_sys"][-1]["nav"]) if (shadow_nav and mkt["nav_sys"]) else None
    return {
        "definition": SHADOW_DEFINITIONS[shadow_key],
        "nav": shadow_nav,
        "monthly_samples": samples,
        "n_closed_months": n_closed,
        "sprt": sprt,
        "cum_diff_vs_sys": round(cum_diff, 4) if cum_diff is not None else None,
    }


def build_shadows_for_market(mk, m, prior_shadow_mk, gaps, judgment_calls):
    out = {}
    for shadow_key, nav_field in (("s60", "nav_s60"), ("sa10", "nav_a10")):
        nav_series = m.get(nav_field) or []
        if not nav_series:
            gaps.append({"market": mk, "reason": f"{shadow_key} 缺 NAV 序列，跳過"})
            continue
        prior_sprt = (prior_shadow_mk.get(shadow_key) or {}).get("sprt")
        out[shadow_key] = build_shadow_block(shadow_key, m, nav_series, prior_sprt)
    if mk == "us":
        try:
            d1_returns, d1_diag = _d1.build_d1_daily_returns()
        except Exception as e:  # noqa: BLE001
            gaps.append({"market": "us", "reason": f"S-F D1 建置失敗（{type(e).__name__}: {e}），S-F 跳過本次"})
            d1_returns, d1_diag = {}, {}
        if d1_returns:
            judgment_calls.append(
                "S-F D1 現金腿：SHY 代理取代 v7-backtest 原版 SHY→BIL 拼接（見 PREREG['shadows']"
                "['judgment_calls']['d1_cash_proxy']）；D1 訊號逐日重算，不用回測快取。"
            )
            sf_nav = build_sf_series(m, d1_returns, gaps)
            prior_sprt = (prior_shadow_mk.get("sf") or {}).get("sprt")
            out["sf"] = build_shadow_block("sf", m, sf_nav, prior_sprt)
            out["sf"]["d1_leg_diag"] = d1_diag
        else:
            gaps.append({"market": "us", "reason": "S-F：D1 日報酬序列為空，跳過本次"})
    return out


def build_combined_twd(mkt_us, mkt_tw, gaps, judgment_calls):
    if not mkt_us or not mkt_tw:
        gaps.append({"reason": "美或台任一市場區塊缺失，無法建合併 TWD 序列"})
        return None
    fx = fetch_usdtwd_series()
    fx_dates = sorted(fx.keys())

    us_by_date = {r["date"]: r["nav"] for r in mkt_us["nav_sys"]}
    tw_by_date = {r["date"]: r["nav"] for r in mkt_tw["nav_sys"]}
    start = max(mkt_us["inception"], mkt_tw["inception"])
    all_dates = sorted(set(d for d in us_by_date if d >= start) | set(d for d in tw_by_date if d >= start))
    if not all_dates:
        gaps.append({"reason": "美台實錄無重疊日期，合併序列留空"})
        return None

    judgment_calls.append(
        "合併 TWD 序列的曆日對齊：JUDGMENT CALL——美台交易日曆不同（假日不同），"
        "取兩市場 live 日期聯集，缺當日紀錄的一側該日視為報酬 0（維持前一淨值），"
        "非捏造報酬、只是「當天沒有新資訊就不動」。"
    )

    fx0 = px_at_or_before(fx, fx_dates, start)
    if fx0 is None:
        gaps.append({"reason": "起始日查無 USDTWD 匯率，合併序列留空"})
        return None

    us_units = 0.5 * 100.0  # TWD-denominated notional at start (美腿以 fx0 換算)
    tw_units_nav = 0.5 * 100.0
    us_prev_nav_usd = us_by_date.get(start, 100.0)
    tw_prev_nav = tw_by_date.get(start, 100.0)
    fx_prev = fx0

    combined = [{"date": start, "nav": 100.0}]
    nav = 100.0
    prev_d = start
    for d in all_dates[1:]:
        us_nav_now = us_by_date.get(d, None)
        us_ret = (us_nav_now / us_by_date.get(prev_d, us_prev_nav_usd) - 1.0) if (us_nav_now is not None and us_by_date.get(prev_d) is not None) else 0.0
        fx_now = px_at_or_before(fx, fx_dates, d) or fx_prev
        fx_ret = (fx_now / fx_prev - 1.0) if fx_prev else 0.0
        r_us_twd = (1.0 + us_ret) * (1.0 + fx_ret) - 1.0

        tw_nav_now = tw_by_date.get(d, None)
        r_tw = (tw_nav_now / tw_by_date.get(prev_d, tw_prev_nav) - 1.0) if (tw_nav_now is not None and tw_by_date.get(prev_d) is not None) else 0.0

        us_val = us_units * (1.0 + r_us_twd)
        tw_val = tw_units_nav * (1.0 + r_tw)
        nav_pre = us_val + tw_val
        is_month_end = (d == all_dates[-1]) or (month_of(all_dates[all_dates.index(d) + 1]) != month_of(d))
        if is_month_end and nav_pre > 0:
            turnover = abs(0.5 - us_val / nav_pre)
            cost = turnover * TURNOVER_COST_FRAC * nav_pre
            nav_post = nav_pre - cost
            us_units, tw_units_nav = 0.5 * nav_post, 0.5 * nav_post
            nav = nav_post
        else:
            us_units, tw_units_nav = us_val, tw_val
            nav = nav_pre
        combined.append({"date": d, "nav": round(nav, 4)})
        fx_prev = fx_now
        prev_d = d

    return {"nav_series": combined, "note": "50/50 月再平衡（TWD 計價，美腿含 USDTWD 匯率報酬），供附帶顯示，不進 SPRT 判定。"}


# ═══════════════════════════════════════════════════════════════════════
# Render — nav-less iframe fragment（比照 _body.html 慣例）
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def status_pill(status):
    color = {"green": "#1a7f37", "yellow": "#9a6700", "red": "#cf222e"}.get(status, "#57606a")
    label = {"green": "🟢 綠", "yellow": "🟡 進行中", "red": "🔴 紅"}.get(status, status)
    return f'<span style="display:inline-block;padding:.15rem .55rem;border-radius:999px;font-size:.78rem;font-weight:600;color:#fff;background:{color}">{label}</span>'


def mkt_section(mkt):
    if not mkt:
        return "<p>資料缺口，無法產出本市場區塊。</p>"
    n = mkt["n_live_days"]
    tiles = f"""
<div class="lsb-tiles">
  <div class="lsb-tile"><div class="lsb-k">實錄起始</div><div class="lsb-v">{esc(mkt['inception'])}</div></div>
  <div class="lsb-tile"><div class="lsb-k">資料截至</div><div class="lsb-v">{esc(mkt['data_through'])}</div></div>
  <div class="lsb-tile"><div class="lsb-k">實錄天數</div><div class="lsb-v">{n}</div></div>
  <div class="lsb-tile"><div class="lsb-k">已收月數</div><div class="lsb-v">{mkt['n_closed_months']}</div></div>
  <div class="lsb-tile"><div class="lsb-k">當前回撤</div><div class="lsb-v">{mkt['current_dd_pct']}%</div></div>
</div>
<div class="lsb-tiles">
  <div class="lsb-tile"><div class="lsb-k">SPRT vs B-mdd（主判準）</div><div class="lsb-v">{status_pill(mkt['sprt_b_mdd']['status'])}</div>
    <div class="lsb-sub">{esc(mkt['sprt_b_mdd']['status_label'])}</div></div>
  <div class="lsb-tile"><div class="lsb-k">SPRT vs B-cagr（並列）</div><div class="lsb-v">{status_pill(mkt['sprt_b_cagr']['status'])}</div>
    <div class="lsb-sub">{esc(mkt['sprt_b_cagr']['status_label'])}</div></div>
  <div class="lsb-tile"><div class="lsb-k">累積差 vs B-mdd</div><div class="lsb-v">{mkt['cum_diff_vs_b_mdd']}</div></div>
  <div class="lsb-tile"><div class="lsb-k">累積差 vs B-cagr</div><div class="lsb-v">{mkt['cum_diff_vs_b_cagr']}</div></div>
</div>"""

    canvas_id = f"lsb-chart-{mkt['market']}"
    labels = [r["date"] for r in mkt["nav_sys"]]
    sys_data = [r["nav"] for r in mkt["nav_sys"]]
    cagr_by_date = {r["date"]: r["nav"] for r in mkt["nav_b_cagr"]}
    mdd_by_date = {r["date"]: r["nav"] for r in mkt["nav_b_mdd"]}
    cagr_data = [cagr_by_date.get(d) for d in labels]
    mdd_data = [mdd_by_date.get(d) for d in labels]
    chart_js = f"""
<canvas id="{canvas_id}" height="90"></canvas>
<script>
(function(){{
  if (typeof Chart === 'undefined') return;
  new Chart(document.getElementById('{canvas_id}').getContext('2d'), {{
    type: 'line',
    data: {{ labels: {json.dumps(labels)}, datasets: [
      {{ label: '系統（實錄）', data: {json.dumps(sys_data)}, borderColor: '#1a7f37', borderWidth:2, pointRadius:0 }},
      {{ label: 'B-mdd（k={mkt['sprt_b_mdd']['n_required'] and ''}稀釋）', data: {json.dumps(mdd_data)}, borderColor: '#cf222e', borderWidth:1, pointRadius:0 }},
      {{ label: 'B-cagr（稀釋）', data: {json.dumps(cagr_data)}, borderColor: '#9a6700', borderWidth:1, pointRadius:0 }}
    ]}},
    options: {{ responsive:true, animation:false, scales:{{ x:{{display:false}}, y:{{title:{{display:true,text:'NAV（inception=100）'}}}} }} }}
  }});
}})();
</script>"""

    hit_rows = ""
    for s in mkt["monthly_samples_mdd"]:
        mark = "✅" if s["hit"] else "—"
        hit_rows += (f'<tr><td>{esc(s["month"])}</td><td class="num">{s["ret_sys_pct"]:+.2f}%</td>'
                     f'<td class="num">{s["ret_bench_pct"]:+.2f}%</td><td>{mark}</td></tr>\n')
    if not hit_rows:
        hit_rows = '<tr><td colspan="4" style="text-align:center;color:#888">尚無已收月樣本（n_eff floor 20 前皆是「進行中」）</td></tr>'

    ev_rows = ""
    for e in mkt["exec_events"][-20:][::-1]:
        ev_rows += f'<tr><td>{esc(e["date"])}</td><td>{esc(e["leg"])}</td><td>{e["from"]:.0f}% → {e["to"]:.0f}%</td></tr>\n'
    if not ev_rows:
        ev_rows = '<tr><td colspan="3" style="text-align:center;color:#888">實錄窗內無執行層調整事件</td></tr>'

    return f"""<div class="lsb-market">
<h3>{esc(mkt['label'])}（{'／'.join(mkt['legs'])}）</h3>
{tiles}
{chart_js}
<table class="lsb-table"><thead><tr><th>月</th><th class="num">系統報酬</th><th class="num">B-mdd 基準報酬</th><th>命中</th></tr></thead>
<tbody>{hit_rows}</tbody></table>
<table class="lsb-table"><thead><tr><th>日期</th><th>腿</th><th>執行層變化</th></tr></thead>
<tbody>{ev_rows}</tbody></table>
</div>"""


SHADOW_LABELS = {"s60": "S-60（固定 60% B&H）", "sf": "S-F（50% 系統 ＋ 50% D1）", "sa10": "S-A10（cap 1.0 無槓桿）"}
SHADOW_COLORS = {"s60": "#8250df", "sf": "#0969da", "sa10": "#bf3989"}


def shadow_market_section(mk, mkt, shadows):
    if not mkt or not shadows:
        return ""
    canvas_id = f"lsb-shadow-chart-{mk}"
    labels = [r["date"] for r in mkt["nav_sys"]]
    sys_data = [r["nav"] for r in mkt["nav_sys"]]
    datasets = [f"{{ label: '系統（實錄）', data: {json.dumps(sys_data)}, borderColor: '#1a7f37', borderWidth:2, pointRadius:0 }}"]
    for key, block in shadows.items():
        by_date = {r["date"]: r["nav"] for r in block["nav"]}
        data = [by_date.get(d) for d in labels]
        datasets.append(
            f"{{ label: {json.dumps(SHADOW_LABELS.get(key, key))}, data: {json.dumps(data)}, "
            f"borderColor: '{SHADOW_COLORS.get(key,'#57606a')}', borderWidth:1, pointRadius:0 }}"
        )
    chart_js = f"""
<canvas id="{canvas_id}" height="90"></canvas>
<script>
(function(){{
  if (typeof Chart === 'undefined') return;
  new Chart(document.getElementById('{canvas_id}').getContext('2d'), {{
    type: 'line',
    data: {{ labels: {json.dumps(labels)}, datasets: [{','.join(datasets)}] }},
    options: {{ responsive:true, animation:false, scales:{{ x:{{display:false}}, y:{{title:{{display:true,text:'NAV（inception=100）'}}}} }} }}
  }});
}})();
</script>"""

    tiles = "<div class=\"lsb-tiles\">"
    for key, block in shadows.items():
        tiles += (f'<div class="lsb-tile"><div class="lsb-k">{esc(SHADOW_LABELS.get(key,key))} vs 系統</div>'
                  f'<div class="lsb-v">{status_pill(block["sprt"]["status"])}</div>'
                  f'<div class="lsb-sub">{esc(block["sprt"]["status_label"])}（已收 {block["n_closed_months"]} 月）</div></div>\n')
    tiles += "</div>"

    tables = ""
    for key, block in shadows.items():
        rows = ""
        for s in block["monthly_samples"]:
            mark = "✅" if s["hit"] else "—"
            rows += (f'<tr><td>{esc(s["month"])}</td><td class="num">{s["ret_sys_pct"]:+.2f}%</td>'
                     f'<td class="num">{s["ret_bench_pct"]:+.2f}%</td><td>{mark}</td></tr>\n')
        if not rows:
            rows = '<tr><td colspan="4" style="text-align:center;color:#888">尚無已收月樣本（n_eff floor 20 前皆是「進行中」）</td></tr>'
        tables += (f'<h4 style="margin:.6rem 0 .2rem;font-size:.88rem">{esc(SHADOW_LABELS.get(key,key))}</h4>'
                   f'<table class="lsb-table"><thead><tr><th>月</th><th class="num">影子帳戶報酬</th>'
                   f'<th class="num">系統報酬</th><th>影子帳戶命中</th></tr></thead><tbody>{rows}</tbody></table>')

    a10_exec = mkt.get("a10_last_exec_pct") or {}
    a10_note = ""
    if a10_exec:
        a10_note = ("<p class='lsb-note'>S-A10 目前各腿執行層持股率：" +
                    "／".join(f"{t} {v:.0f}%" for t, v in a10_exec.items()) + "。</p>")

    return f"""<div class="lsb-market">
<h3>{esc(mkt['label'])}影子帳戶</h3>
{tiles}
{chart_js}
{a10_note}
{tables}
</div>"""


def render_body(out):
    us_sec = mkt_section(out["markets"].get("us"))
    tw_sec = mkt_section(out["markets"].get("tw"))
    shadows_out = out.get("shadows") or {}
    us_shadow_sec = shadow_market_section("us", out["markets"].get("us"), shadows_out.get("us"))
    tw_shadow_sec = shadow_market_section("tw", out["markets"].get("tw"), shadows_out.get("tw"))
    combined = out.get("combined_twd")
    combined_note = ""
    if combined:
        combined_note = f"<p class='lsb-note'>兩市場合併（TWD，50/50 月再平衡）最新 NAV：{combined['nav_series'][-1]['nav']}（inception=100，僅附帶顯示，不進 SPRT 判定）。</p>"

    prereg_json = json.dumps(out["prereg"], ensure_ascii=False, indent=1)

    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>實單前瞻記分板</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>
body{{margin:0;padding:.75rem 1rem 1.5rem;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:#1f2328;background:#fff}}
h3{{margin:1rem 0 .4rem;font-size:1rem}}
.lsb-plain{{background:#f3f6fb;border-left:3px solid #6b8fd6;padding:.5rem .75rem;margin:.4rem 0 .8rem;font-size:.85rem;border-radius:4px}}
.lsb-tiles{{display:flex;flex-wrap:wrap;gap:.5rem;margin:.4rem 0}}
.lsb-tile{{flex:1 1 140px;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:.5rem .6rem}}
.lsb-k{{font-size:.72rem;color:#57606a}}
.lsb-v{{font-size:1rem;font-weight:600;margin-top:.15rem}}
.lsb-sub{{font-size:.72rem;color:#57606a;margin-top:.2rem}}
.lsb-table{{width:100%;border-collapse:collapse;margin:.5rem 0 1rem;font-size:.82rem}}
.lsb-table th,.lsb-table td{{border-bottom:1px solid #eaeef2;padding:.3rem .5rem;text-align:left}}
.lsb-table td.num,.lsb-table th.num{{text-align:right;font-variant-numeric:tabular-nums}}
.lsb-note{{font-size:.8rem;color:#57606a}}
details.lsb-prereg summary{{cursor:pointer;font-size:.82rem;color:#57606a;margin:.6rem 0 .3rem}}
details.lsb-prereg pre{{max-height:280px;overflow:auto;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:.6rem;font-size:.72rem;white-space:pre-wrap}}
</style></head>
<body>
<p class="lsb-note"><a href="/backtest/live_system_evidence/">這套系統的九項證據總覽 →</a></p>
<div class="lsb-plain">💬 白話：這不是回測，是「只用實際發生過的紀錄」每個月記一次系統有沒有贏過同標的的稀釋基準（<b>SPRT</b>＝序貫檢定，累積證據到夠強才判定；<b>LLR</b>＝累積證據強度；<b>命中</b>＝當月系統報酬贏過基準；<b>稀釋基準</b>＝把 50/50 買進持有的一部分換成現金，讓風險與系統相近再比）的淘汰賽。判紅只代表「證據支持系統不比稀釋好」，是登記進帳本待持有人檢討的訊號，不是自動平倉指令；本頁面不下任何買賣或配置建議。</div>
{us_sec}
{tw_sec}
{combined_note}
<h2 style="margin:1.4rem 0 .3rem;font-size:1.05rem">影子帳戶：如果當初選別的</h2>
<div class="lsb-plain">💬 白話：這裡的三條線不是本站現在真的在跑的東西，是「如果 10 月回顧點當初選了別的做法，帳會怎麼記」的平行對照——S-60 是不解方程、事前就能執行的固定六成持股版本；S-F 是把一半資金換成一籃子跨資產（美股／公債／黃金／原物料）趨勢規則；S-A10 是拿掉槓桿上限的系統本尊。上面每個市場的 SPRT 淘汰賽問的是「系統有沒有贏過稀釋現金的基準」，這裡的 SPRT 問的是相反方向的問題：「如果當初選了這條影子帳戶，會不會比現在的系統好」。判紅只代表某條影子帳戶的實錄目前不如系統，判綠代表某條影子帳戶目前贏過系統——兩者都只是留給 10 月回顧點參考的證據，不會觸發任何帳本動作或配置調整。</div>
{us_shadow_sec}
{tw_shadow_sec}
<details class="lsb-prereg"><summary>PREREG（凍結口徑，展開查看逐字條文）</summary><pre>{esc(prereg_json)}</pre></details>
<p class="lsb-note">as_of {esc(out['as_of'])} · built_at {esc(out['built_at'])} · 回測先驗（保險價格頁 2010 起月勝率）：{esc(out['backtest_prior'])}</p>
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def build():
    gaps, judgment_calls = [], []
    judgment_calls.append(
        "NAV inception：以每市場第一筆 source=='live' 紀錄日為 NAV=100 基準日（該日不計報酬，"
        "作為 t-1 錨點），非規格明文逐字規定但與 exposure_track.py inception=100 慣例一致。"
    )
    judgment_calls.append(
        "月末再平衡＋7bps 成本的實作：見 PREREG['benchmarks']['rebalance']（月末以當日已計入市場"
        "變動的淨值為基礎再平衡回 k，成本＝|實際權重−k|×7bps×淨值）。"
    )

    state = load_json(STATE_JSON)
    if not state:
        raise FailSafeAbort(f"{STATE_JSON} 讀不到或為空")

    prior_out = load_json(OUT_JSON) or {}
    prior_sprt_map = {}
    for mk in ("us", "tw"):
        m = (prior_out.get("markets") or {}).get(mk) or {}
        prior_sprt_map[mk] = {"sprt_cagr": m.get("sprt_b_cagr"), "sprt_mdd": m.get("sprt_b_mdd")}
    state["_live_scoreboard_prior"] = prior_sprt_map

    markets_out = {}
    for mkt in MARKETS:
        try:
            markets_out[mkt["key"]] = build_market(mkt, state, gaps, judgment_calls)
        except Exception as e:  # noqa: BLE001
            gaps.append({"market": mkt["key"], "reason": f"build_market failed: {type(e).__name__}: {e}"})
            markets_out[mkt["key"]] = None

    combined = build_combined_twd(markets_out.get("us"), markets_out.get("tw"), gaps, judgment_calls)
    backtest_prior = load_backtest_prior(gaps)

    prior_shadows = prior_out.get("shadows") or {}
    shadows_out = {}
    for mk in ("us", "tw"):
        m = markets_out.get(mk)
        if not m:
            continue
        shadows_out[mk] = build_shadows_for_market(mk, m, prior_shadows.get(mk) or {}, gaps, judgment_calls)

    as_of = max((m["data_through"] for m in markets_out.values() if m), default=date.today().isoformat())

    out = {
        "schema": SCHEMA,
        "prereg": PREREG,
        "as_of": as_of,
        "markets": markets_out,
        "combined_twd": combined,
        "shadows": shadows_out,
        "backtest_prior": backtest_prior,
        "data_gaps": gaps,
        "judgment_calls": judgment_calls,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return out


def main():
    try:
        out = build()
    except FailSafeAbort as e:
        print(f"  ✗ fail-safe triggered: {e} — outputs left unchanged")
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — outputs left unchanged")
        sys.exit(0)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  ✓ wrote {OUT_JSON.relative_to(ROOT)}")

    OUT_BODY.parent.mkdir(parents=True, exist_ok=True)
    OUT_BODY.write_text(render_body(out), encoding="utf-8")
    print(f"  ✓ wrote {OUT_BODY.relative_to(ROOT)}")

    for mk, m in out["markets"].items():
        if not m:
            print(f"  ⚠ market {mk}: no data")
            continue
        print(f"  {mk}: inception={m['inception']} data_through={m['data_through']} "
              f"n_live_days={m['n_live_days']} n_closed_months={m['n_closed_months']} "
              f"sprt_mdd={m['sprt_b_mdd']['status']} sprt_cagr={m['sprt_b_cagr']['status']} "
              f"nav_sys={m['nav_sys'][-1]['nav'] if m['nav_sys'] else None} "
              f"nav_b_mdd={m['nav_b_mdd'][-1]['nav'] if m['nav_b_mdd'] else None} "
              f"nav_b_cagr={m['nav_b_cagr'][-1]['nav'] if m['nav_b_cagr'] else None}")
    if out["data_gaps"]:
        print(f"  data_gaps: {len(out['data_gaps'])}")


if __name__ == "__main__":
    main()
