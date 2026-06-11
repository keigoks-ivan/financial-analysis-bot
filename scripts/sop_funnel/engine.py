#!/usr/bin/env python3
"""Pure MA SOP 漏斗引擎 — charter v2.0 個股部 SOP v2.1 的機器版。

規則來源：InvestMQuest 總守則 v2.0（master charter）LAYER 1 個股部 SOP v2.1。
設計定案：~/.claude/plans/mighty-tickling-valley.md（2026-06-11 用戶拍板）。

核心約定（防 look-ahead / 可執行性）：
1. 週線指標只用「已完成的週」（W-FRI bar 的 label < 當日），整週凍結供每日判定
   — 對齊 charter E-5「日線判斷用當週凍結的 MA 值」。
2. prior ATH = 不含當日的 expanding max。
3. 所有動作 T+1 收盤執行：訊號日收盤後才知道訊號（CI 隔日 09:00 Taipei 跑），
   進場/減碼/出場價一律 = 訊號日的次一交易日收盤。
4. 態⑤ 以「完成週的週收盤 < MA52w」判定，於次一交易日收盤執行。

訊號分級（用戶 2026-06-11 拍板）：
- A1 起漲型：日收盤突破「已站立 ≥26 週」的 prior ATH（主訊號；≥52 週標 ⭐）
- A2 續勢型：基期 <26 週的新高（記錄 + 降級顯示）
- B 第二班車：A1 價格事件後 26 週內，首次回踩 60MA/前高後站回（每 A1 最多一次）
- 否決必記錄：創新高但 態②過熱 / 五條件 fail / 歷史不足 → vetoed 事件含原因

態④減碼幅度參數化（t4_staged）：forward 帳本照 charter（一次減至核心 50%）；
backtest.py 跑 50% vs 25%+25% A/B 供 2026-09 季檢。
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# ── 參數（charter S-2 + 用戶拍板）────────────────────────────────────────────
PARAMS = {
    "base_age_min_weeks": 26,     # A1 起漲基期門檻（用戶拍板 26 週）
    "base_age_star_weeks": 52,    # 超長基期 ⭐ 加強標
    "b_window_weeks": 26,         # B 第二班車窗口（用戶拍板 26 週；超窗灰顯）
    "ma_daily": 60,
    "ma_weeks": (52, 104, 200),
    "bb_len": 20,
    "bb_ddof": 1,                 # 樣本標準差 N-1（charter E-5）
    "t4_band": 0.97,              # 態④：跌破 60MA×0.97
    "t4_days": 3,                 # 或連 3 日收線下
    "t4_trim_to": 0.50,           # 態④減至核心 50%（charter S-2；以減碼後剩餘計）
    "t4_staged": False,           # True = 25%+25% 階梯（僅 backtest A/B 用，forward 禁用）
    "t4_stage2_band": 0.94,       # 階梯第二段：跌破 60MA×0.94（沿用 trim-variants V2 規格）
    "t3_trim": 1.0 / 3.0,         # 態③：觸 3σ 減 1/3
    "pos_max_pct": 10.0,          # 單檔上限（分母 = 個股部淨值）
    "risk_budget_pct": 1.5,       # 單筆風險預算
    "near_ath_pct": 5.0,          # A 待命帶：距 ATH ≤5%
    "base_watch_min_weeks": 20,   # 築基中：ATH 已站 ≥20 週
    "base_watch_dist": (5.0, 25.0),  # 築基中：距 ATH 5-25%
}

QUALITY_GATE = {  # 五條件閘門（用戶 2026-06-11 拍板；資料全取 dd-screener latest.json）
    "eps_fy1_fy3_cagr_pct": 15.0,   # > 15%（用戶指定：EPS 用 FY1→FY3 CAGR）
    "roic": 15.0,                   # > 15%
    "fcf": 10.0,                    # FCF margin > 10%（2026-06-11 自 15 下修：15 在 AI capex
                                    #   超級週期懲罰投資期的 S/A 級公司 — LLY/MSFT/AMAT 案例；
                                    #   資本紀律由 ROIC>15 把守，FCF 只當現金地板）
    "peg": 2.0,                     # < 2（live_peg 優先，缺值退 peg）
    # 第五條件：護城河 — grade ∉ {C, X}（全站 screener veto 慣例）
    #           且 moat_trend ≠ ↓（進場漏斗不開衰退中護城河的新倉；
    #           trend 源頭 = build_dd_screener 的 DCA-authoritative map）
    "moat_veto_grades": ("C", "X"),
    "moat_review_age_days": 183,    # DD 評級逾 6 個月未更新 → 訊號照發但標「護城河待複檢」
}

# ── 預登記裁決規則（跑前鎖定，不得中途修改）────────────────────────────────
PREREG = {
    "a2_adjudication": (
        "【鎖定 2026-06-11】A2 續勢型裁決：A1＋A2 已平倉合計 ≥20 筆後執行一次 — "
        "A2 的中位報酬或平均 α 落後 A1 超過 5 個百分點 → A2 降為純觀察（停止模擬進場，"
        "僅記錄）；未落後 → A2 轉正為正式訊號。裁決前 A2 維持「記錄＋模擬進場」作為對照組；"
        "本規則於資料累積前鎖定，禁止看到結果後修改門檻。"
    ),
    "quarterly_review_items": [
        "26 週（A1 基期）與 20 週（築基中）兩個相近參數是否統一為一個",
        "態⑤ 出場改 T+1 開盤（生死線不該多扛一個交易日；模擬端需先建 OHLC 資料層）",
        "財報窗「標記不擋」複查（2026-06-11 拿掉禁令，依據含偏回測證據 — 用 forward 標記數據無偏複驗）",
        "斷路器拿掉的覆議（2026-06-11 依死鎖發現拿掉 — charter 層決定，留意無保險絲後的 whipsaw 風險）",
    ],
}


def quality_check(row: dict) -> tuple[bool | None, list[str], dict]:
    """五條件閘門（四質量 + 護城河）。回傳 (pass / None=缺資料, fail 清單, 使用值)。
    質量四欄缺值 = 不過閘；moat_grade 缺 = 不過閘；moat_trend 缺 = 視為 →（不否決）。"""
    def _num(v):
        if v is None:
            return None
        try:
            f = float(v)
        except (TypeError, ValueError):
            return None
        return None if np.isnan(f) else f

    cagr = _num(row.get("eps_fy1_fy3_cagr_pct"))
    roic = _num(row.get("roic"))
    fcf = _num(row.get("fcf"))
    peg = _num(row.get("live_peg"))
    peg_src = "live_peg"
    if peg is None:
        peg = _num(row.get("peg"))
        peg_src = "peg"
    grade = row.get("moat_grade")
    trend = row.get("moat_trend")
    used = {"eps_fy1_fy3_cagr_pct": cagr, "roic": roic, "fcf": fcf,
            "peg_used": peg, "peg_source": peg_src,
            "moat_grade": grade, "moat_trend": trend}
    if any(v is None for v in (cagr, roic, fcf, peg)) or not grade:
        return None, ["缺資料"], used
    fails = []
    if not cagr > QUALITY_GATE["eps_fy1_fy3_cagr_pct"]:
        fails.append("CAGR≤15")
    if not roic > QUALITY_GATE["roic"]:
        fails.append("ROIC≤15")
    if not fcf > QUALITY_GATE["fcf"]:
        fails.append("FCFm≤10")
    if not peg < QUALITY_GATE["peg"]:
        fails.append("PEG≥2")
    if grade in QUALITY_GATE["moat_veto_grades"]:
        fails.append(f"護城河{grade}")
    if trend == "↓":
        fails.append("護城河↓")
    return (len(fails) == 0), fails, used


# ── 指標 frame ───────────────────────────────────────────────────────────────
@dataclass
class Frame:
    """單檔的全部指標序列。weekly 序列 index = W-FRI label（含當前未完週的 bar，
    使用端一律經 frozen_*() 取「label < 當日」的最後一根 → 不會吃到未完週）。"""
    close: pd.Series
    ma60: pd.Series
    prior_ath: pd.Series          # 不含當日的 expanding max
    prior_ath_date: pd.Series     # 該 prior ATH 創下的日期
    wclose: pd.Series
    wma: dict = field(default_factory=dict)     # {52:Series,104:Series,200:Series}
    bb2: pd.Series = None
    bb3: pd.Series = None

    def _frozen_pos(self, d: pd.Timestamp) -> int:
        """最後一根 label < d 的完成週位置；無 → -1。"""
        return int(self.wclose.index.searchsorted(d)) - 1

    def frozen(self, name: str, d: pd.Timestamp):
        """凍結週線值：MA52w/'wma52'、'bb2'、'bb3'、'wclose'。無資料回 None。"""
        pos = self._frozen_pos(d)
        if pos < 0:
            return None
        ser = {"wclose": self.wclose, "bb2": self.bb2, "bb3": self.bb3}.get(name)
        if ser is None and name.startswith("wma"):
            ser = self.wma[int(name[3:])]
        v = ser.iloc[pos]
        return None if pd.isna(v) else float(v)

    def state1(self, d: pd.Timestamp, px: float) -> tuple[bool, list[str]]:
        """態① 健康多頭（凍結週線）：價>52週線 ∩ 52>104>200 ∩ 未進過熱帶(<+2σ)。
        回傳 (成立?, 不成立原因)。歷史不足（MA200w 缺）→ 原因 '歷史不足'。"""
        w52 = self.frozen("wma52", d)
        w104 = self.frozen("wma104", d)
        w200 = self.frozen("wma200", d)
        bb2 = self.frozen("bb2", d)
        if w200 is None or w104 is None or w52 is None:
            return False, ["歷史不足"]
        reasons = []
        if not px > w52:
            reasons.append("價≤52週線")
        if not (w52 > w104 > w200):
            reasons.append("排列不正")
        if bb2 is not None and px >= bb2:
            reasons.append("態②過熱")
        return (len(reasons) == 0), reasons


def build_frame(close: pd.Series, params: dict = PARAMS) -> Frame | None:
    """日收盤 Series → Frame。資料 < 60 日回 None。"""
    close = close.dropna()
    if len(close) < params["ma_daily"]:
        return None
    ma60 = close.rolling(params["ma_daily"]).mean()
    # prior ATH（不含當日）與其創下日
    ath_v = np.empty(len(close))
    ath_d: list = [None] * len(close)
    cur, cur_d = -np.inf, None
    for i, (d, px) in enumerate(close.items()):
        ath_v[i] = cur
        ath_d[i] = cur_d
        if px > cur:
            cur, cur_d = px, d
    wk = close.resample("W-FRI").last().dropna()
    sma = wk.rolling(params["bb_len"]).mean()
    sd = wk.rolling(params["bb_len"]).std(ddof=params["bb_ddof"])
    return Frame(
        close=close, ma60=ma60,
        prior_ath=pd.Series(ath_v, index=close.index),
        prior_ath_date=pd.Series(ath_d, index=close.index),
        wclose=wk,
        wma={n: wk.rolling(n).mean() for n in params["ma_weeks"]},
        bb2=sma + 2 * sd, bb3=sma + 3 * sd,
    )


def stop_dist_pct(frame: Frame, d: pd.Timestamp, px: float) -> float | None:
    """停損距離% = (close − 52週線) / close × 100（凍結週線）。"""
    w52 = frame.frozen("wma52", d)
    if w52 is None or px <= 0:
        return None
    return (px - w52) / px * 100.0


def position_pct(sd_pct: float | None, params: dict = PARAMS) -> float | None:
    """charter S-4 Q4：部位% = min(10%, 1.5% ÷ 停損距離)。"""
    if sd_pct is None or sd_pct <= 0:
        return None
    return round(min(params["pos_max_pct"],
                     params["risk_budget_pct"] / (sd_pct / 100.0)), 2)


# ── 訊號掃描（全史 deterministic，build.py 端負責去重/時窗）──────────────────
def scan_ticker(frame: Frame, quality_pass: bool | None, quality_fails: list[str],
                params: dict = PARAMS) -> list[dict]:
    """單檔全史掃描 → 事件清單（含 vetoed）。

    B 型錨定規則：錨 = 最近一次 A1「價格事件」（突破基期 ≥26 週的 ATH，不論是否
    被否決/進場）。錨後 26 週內首次回踩（收盤 < 60MA 或 ≤ 錨 ATH 價）再站回
    （收盤回到 60MA 上 / 收復前高）→ B 板機；每錨一次；回踩中完成週收盤破
    52週線 → 錨作廢。
    """
    ev: list[dict] = []
    c, ma60 = frame.close, frame.ma60
    idx = c.index
    # B 狀態
    anchor_d = None          # A1 價格事件日
    anchor_lvl = None        # 被突破的 ATH 價（前高）
    b_used = True
    touched60 = False
    retested = False
    last_week_pos = -1       # 已檢查過的完成週位置（態⑤ 錨作廢用）

    for i in range(1, len(idx)):
        d, px = idx[i], float(c.iloc[i])

        # — 錨作廢檢查：上次迭代後是否有完成週收盤破 52週線 —
        if anchor_d is not None and not b_used:
            wpos = frame._frozen_pos(d)
            while last_week_pos < wpos:
                last_week_pos += 1
                wlabel = frame.wclose.index[last_week_pos]
                if wlabel <= anchor_d:
                    continue
                w52 = frame.wma[52].iloc[last_week_pos]
                if not pd.isna(w52) and float(frame.wclose.iloc[last_week_pos]) < float(w52):
                    b_used = True   # 破線 → 錨作廢（回到等新基期）
                    break
        else:
            last_week_pos = frame._frozen_pos(d)

        # — A 型：日收盤創新高 —
        ath = float(frame.prior_ath.iloc[i])
        ath_d = frame.prior_ath_date.iloc[i]
        if np.isfinite(ath) and px > ath and ath_d is not None:
            base_age_w = (d - ath_d).days / 7.0
            sig_class = "A1" if base_age_w >= params["base_age_min_weeks"] else "A2"
            ok1, reasons1 = frame.state1(d, px)
            vetoes = list(reasons1)
            if quality_pass is None:
                vetoes.append("五條件缺資料")
            elif not quality_pass:
                vetoes.append("五條件fail:" + ",".join(quality_fails))
            ev.append({
                "type": sig_class, "date": d, "close": px,
                "base_age_weeks": round(base_age_w, 1),
                "base_star": base_age_w >= params["base_age_star_weeks"],
                "anchor_a1_date": None,
                "vetoes": vetoes,
            })
            if sig_class == "A1":   # 不論否決與否，A1 價格事件武裝 B 錨
                anchor_d, anchor_lvl = d, ath
                b_used, touched60, retested = False, False, False
                last_week_pos = frame._frozen_pos(d)
            continue   # 創新高日不可能同時是 B 回踩站回日

        # — B 型：錨存活 + 窗口內 —
        if anchor_d is None or b_used:
            continue
        if (d - anchor_d).days / 7.0 > params["b_window_weeks"]:
            continue   # 超窗：不給訊號（待命區灰顯由 build.py 處理）
        m60 = ma60.iloc[i]
        if pd.isna(m60):
            continue
        m60 = float(m60)
        prev_px = float(c.iloc[i - 1])
        prev_m60 = ma60.iloc[i - 1]
        prev_m60 = float(prev_m60) if not pd.isna(prev_m60) else None
        # 回踩到位偵測
        if px < m60:
            touched60 = True
        if px <= anchor_lvl:
            retested = True
        # 板機：站回 60MA（曾觸 60MA）或收復前高（僅回測前高）
        trigger = False
        if touched60 and prev_m60 is not None and prev_px <= prev_m60 and px > m60:
            trigger = True
        elif (not touched60) and retested and prev_px <= anchor_lvl and px > anchor_lvl:
            trigger = True
        if trigger:
            ok1, reasons1 = frame.state1(d, px)
            vetoes = list(reasons1)
            if quality_pass is None:
                vetoes.append("五條件缺資料")
            elif not quality_pass:
                vetoes.append("五條件fail:" + ",".join(quality_fails))
            ev.append({
                "type": "B", "date": d, "close": px,
                "base_age_weeks": None, "base_star": False,
                "anchor_a1_date": anchor_d,
                "vetoes": vetoes,
            })
            b_used = True   # 每錨最多一次（charter「限突破後首次回測」）
    return ev


# ── 五狀態機模擬器 ───────────────────────────────────────────────────────────
def next_trading_close(close: pd.Series, d: pd.Timestamp) -> tuple[pd.Timestamp, float] | None:
    """d 之後第一個交易日的 (日期, 收盤)。無 → None（T+1 尚未到 = pending）。"""
    after = close.loc[close.index > d]
    if after.empty:
        return None
    return after.index[0], float(after.iloc[0])


def simulate_trade(frame: Frame, entry_date: pd.Timestamp, params: dict = PARAMS) -> dict:
    """從 entry_date（已是 T+1 成交日）模擬五狀態機至資料末端。

    部位記帳：fraction 以「初始部位 = 1.0」為基準；回補棘輪上限 =
    min(1.0, 當下風險預算部位 / 進場時風險預算部位)（charter「棘輪式降風險 by design」）。
    報酬分母 = 累計投入資金（含回補），文件化於頁面 caveat。

    回傳 dict：status open|closed、legs、ret_pct、r_multiple、holding_days、
    current_state、current_fraction、exit_date、exit_reason。
    """
    c, ma60 = frame.close, frame.ma60
    if entry_date not in c.index:
        raise ValueError(f"entry_date {entry_date} 不在價格序列內")
    p0 = float(c.loc[entry_date])
    sd0 = stop_dist_pct(frame, entry_date, p0)
    pos0 = position_pct(sd0, params)

    fraction = 1.0
    invested = p0 * 1.0          # 累計投入（含回補）
    proceeds = 0.0               # 累計賣出
    legs: list[dict] = []
    # 狀態旗標
    t3_done = False              # 態③ 一次性（回落 2σ 內重置）
    t4_active = False            # 態④ 中（已減碼未回補）
    t4_rebuy_done = False
    t4_stage2_done = False
    consec_below = 0
    pending: list[tuple[str, float]] = []   # T+1 執行佇列 [(action, qty_or_target)]
    exit_reason = None
    exit_date = None
    cur_state = "①"
    last_week_pos = frame._frozen_pos(entry_date)

    start = c.index.searchsorted(entry_date) + 1
    for i in range(start, len(c.index)):
        d, px = c.index[i], float(c.iloc[i])

        # ── 1) 執行前一日確認的動作（T+1 收盤）──
        for action, val in pending:
            if action == "exit":
                proceeds += fraction * px
                legs.append({"date": str(d.date()), "fraction": round(fraction, 4),
                             "price": round(px, 4), "reason": "態⑤全出"})
                fraction = 0.0
                exit_reason, exit_date = "態⑤", d
            elif action == "trim_t3":
                qty = fraction * params["t3_trim"]
                proceeds += qty * px
                fraction -= qty
                legs.append({"date": str(d.date()), "fraction": round(qty, 4),
                             "price": round(px, 4), "reason": "態③減1/3"})
            elif action == "trim_t4":
                target = fraction * val   # val = 保留比例（以減碼後剩餘計核心）
                qty = fraction - target
                if qty > 1e-9:
                    proceeds += qty * px
                    fraction = target
                    legs.append({"date": str(d.date()), "fraction": round(qty, 4),
                                 "price": round(px, 4), "reason": "態④減碼"})
            elif action == "rebuy":
                sd_now = stop_dist_pct(frame, d, px)
                cap_now = position_pct(sd_now, params)
                if cap_now is not None and pos0:
                    f_cap = min(1.0, cap_now / pos0)
                    qty = f_cap - fraction
                    if qty > 1e-9:
                        invested += qty * px
                        fraction += qty
                        legs.append({"date": str(d.date()), "fraction": round(qty, 4),
                                     "price": round(px, 4), "reason": "態④回補"})
        pending = []
        if fraction <= 1e-9 and exit_reason:
            break

        # ── 2) 態⑤：完成週收盤 < MA52w（優先序最高）──
        wpos = frame._frozen_pos(d)
        escalated = False
        while last_week_pos < wpos:
            last_week_pos += 1
            w52 = frame.wma[52].iloc[last_week_pos]
            if not pd.isna(w52) and float(frame.wclose.iloc[last_week_pos]) < float(w52):
                escalated = True
        if escalated:
            pending = [("exit", 0.0)]
            cur_state = "⑤"
            continue

        m60 = ma60.iloc[i]
        m60 = float(m60) if not pd.isna(m60) else None
        bb2 = frame.frozen("bb2", d)
        bb3 = frame.frozen("bb3", d)

        # ── 3) 態④：跌破 60MA×0.97 或連 3 日收線下 ──
        if m60 is not None:
            consec_below = consec_below + 1 if px < m60 else 0
            t4_confirm = (px < params["t4_band"] * m60) or (consec_below >= params["t4_days"])
            if not t4_active and t4_confirm:
                t4_active, t4_rebuy_done, t4_stage2_done = True, False, False
                if params["t4_staged"]:
                    pending.append(("trim_t4", 0.75))   # 第一段 25%
                else:
                    pending.append(("trim_t4", params["t4_trim_to"]))
                cur_state = "④"
                continue
            if t4_active and params["t4_staged"] and not t4_stage2_done \
                    and px < params["t4_stage2_band"] * m60:
                t4_stage2_done = True
                pending.append(("trim_t4", 0.50 / 0.75))   # 補到合計核心 50%
                cur_state = "④"
                continue
            # 回補：站回 60MA 且週線仍態①
            if t4_active and not t4_rebuy_done and px > m60:
                ok1, _ = frame.state1(d, px)
                w52 = frame.frozen("wma52", d)
                if w52 is not None and px > w52 and ok1:
                    pending.append(("rebuy", 0.0))
                    t4_rebuy_done = True
                    t4_active = False
                    cur_state = "①"
                    continue

        # ── 4) 態③：觸 3σ 減 1/3（一次性；回落 2σ 內重置）──
        if bb2 is not None and px < bb2:
            t3_done = False
        if bb3 is not None and px >= bb3 and not t3_done and not t4_active:
            t3_done = True
            pending.append(("trim_t3", 0.0))
            cur_state = "③"
            continue

        # ── 5) 無動作：更新顯示態 ──
        if t4_active:
            cur_state = "④"
        elif bb3 is not None and px >= bb3:
            cur_state = "③"
        elif bb2 is not None and px >= bb2:
            cur_state = "②"
        else:
            cur_state = "①"

    # ── 收尾結算 ──
    last_d, last_px = c.index[-1], float(c.iloc[-1])
    final_value = fraction * last_px
    profit = proceeds + final_value - invested
    ret_pct = profit / invested * 100.0 if invested > 0 else None
    closed = exit_reason is not None and fraction <= 1e-9
    holding_end = exit_date if closed else last_d
    # 資料末日剛確認、尚未到 T+1 執行日的動作 → 顯式曝露（避免「態④+100%」誤讀）
    _ACTION_LABEL = {"exit": "態⑤全出", "trim_t3": "態③減1/3",
                     "trim_t4": "態④減碼", "rebuy": "態④回補"}
    pending_action = _ACTION_LABEL.get(pending[0][0]) if pending else None
    return {
        "status": "closed" if closed else "open",
        "entry_date": str(entry_date.date()), "entry_close": round(p0, 4),
        "stop_dist_pct": round(sd0, 2) if sd0 is not None else None,
        "suggested_position_pct": pos0,
        "legs": legs,
        "current_state": cur_state if not closed else "—",
        "pending_action": pending_action,   # 明日收盤執行的已確認動作（無則 None）
        "current_fraction": round(fraction, 4),
        "exit_date": str(exit_date.date()) if exit_date is not None else None,
        "exit_reason": exit_reason,
        "ret_pct": round(ret_pct, 2) if ret_pct is not None else None,
        "r_multiple": round(ret_pct / sd0, 2) if (ret_pct is not None and sd0) else None,
        "holding_days": int((holding_end - entry_date).days),
        "last_price": round(last_px, 4),
    }


def fixed_horizon_ret(close: pd.Series, entry_date: pd.Timestamp,
                      days: int) -> float | None:
    """固定持有對照：entry 後 +days 曆日（取 ≤ 目標日最近收盤）報酬%。未到期 None。"""
    if entry_date not in close.index:
        return None
    target = entry_date + pd.Timedelta(days=days)
    if close.index[-1] < target:
        return None
    seg = close.loc[entry_date:target]
    if len(seg) < 2:
        return None
    return round((float(seg.iloc[-1]) / float(seg.iloc[0]) - 1.0) * 100.0, 2)
