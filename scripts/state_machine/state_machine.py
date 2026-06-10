"""五狀態機 — state_machine.py：狀態判定 + 優先序仲裁 + 記憶 + 動作映射。

純函數（無 I/O）。輸入 = 當日指標 + 記憶（state.json 該檔項）+ breakout 登記 + 情境，
輸出 = 當日狀態/動作/進場訊號 + 更新後的記憶與 breakout。

實作 SPEC §4（演算法）、§4.3（記憶與一次性動作）、§4.4（態⑤回歸）、§4.5（突破登記簿）、
§4.6（進場訊號）、§5（動作映射）。優先序嚴格 ⑤>④>③>②>①（SPEC S-3）。
"""
from __future__ import annotations

import copy
from typing import Optional

from config import ATH_PROXIMITY, RETEST_BAND


# ── 預設記憶 / breakout 結構 ────────────────────────────────────────────────
def default_memory(state: int = 1, since: Optional[str] = None) -> dict:
    return {
        "state": state,
        "state_since": since,
        "overheat_episode": {"active": False, "trim_done": False},
        "pullback": {"trim_to_core_done": False},   # r2: 移除 reentry_armed（死碼）
        "pending_state5_warning": False,
        "exited": False,
        "exit_date": None,
        "state1_clean": state == 1,   # 態①全程未掛 pending warning（B 型門檻）
        "was_below_60d": False,        # 近期曾跌破 60MA（B 型 60MA 參考）
        "last_confirmed_week": None,   # r2 P0-2：最近一個已判定的「完成週」frozen_week_date
        "data_error_streak": 0,
    }


def default_breakout(breakout_date: str, prior_ath: float) -> dict:
    return {
        "breakout_date": breakout_date,
        "prior_ath": prior_ath,
        "first_retest_done": False,
        "entered_band": False,   # 收盤曾進入 prior_ath±2%（B 型前高用）
        "retest_date": None,
    }


# ── 條件函數（SPEC §4.1）────────────────────────────────────────────────────
def _conditions(ind: dict, ctx: dict) -> dict:
    mid_ok = ind.get("bb_upper2") is not None and ind.get("bb_upper3") is not None
    fwc = ind.get("frozen_weekly_close")
    overheat = bool(
        mid_ok and fwc is not None
        and fwc > ind["bb_upper2"] and fwc <= ind["bb_upper3"]
    )
    touch3 = bool(
        ind.get("bb_upper3") is not None and ind.get("week_high_so_far") is not None
        and ind["week_high_so_far"] >= ind["bb_upper3"]
    )
    # C_weekly_break：週五收盤 < MA52w（凍結週收盤即該週收盤）。
    weekly_break = bool(
        fwc is not None and ind.get("ma52w") is not None and fwc < ind["ma52w"]
    )
    # C_earnings_gap_break：今日為財報後首個交易日 且 開盤即低於 MA52w 且 收盤 < MA52w。
    gap_break = bool(
        ctx.get("is_first_day_after_earnings")
        and ind.get("open") is not None and ind.get("ma52w") is not None
        and ind["open"] < ind["ma52w"] and ind.get("below_52w")
    )
    return {
        "above_52w": ind.get("above_52w", False),
        "alignment": ind.get("alignment", False),
        "overheat_zone": overheat,
        "touch_3sigma": touch3,
        "below_60d": ind.get("below_60d", False),
        "friday": ind.get("last_bar_is_friday", False),
        "weekly_break": weekly_break,
        "earnings_gap_break": gap_break,
        "below_52w": ind.get("below_52w", False),
    }


def _direct_state(C: dict, ind: dict) -> tuple[int, bool]:
    """忽略記憶、純由當日正向條件判態（首次運行 seed / 「維持前態」無前態時的 fallback）。

    回傳 (state, exited)。below_52w（且非過渡）→ seed 為態⑤、exited=True（保守：
    上線首日不對已破線的標的噴 EXIT，靠 exited 走回歸路徑等新 ATH）。
    """
    if C["below_52w"]:
        return 5, True
    if C["below_60d"] and C["above_52w"]:
        return 4, False
    if C["touch_3sigma"]:
        return 3, False
    if C["overheat_zone"]:
        return 2, False
    if C["above_52w"] and C["alignment"]:
        return 1, False
    if C["above_52w"]:
        return 1, False   # 站上 52w 但排列待確認 → 保守 seed 態①
    return 5, True


# ── 主判定（SPEC §4.2）──────────────────────────────────────────────────────
def evaluate(ticker: str, ind: Optional[dict], mem: Optional[dict],
             breakout: Optional[dict], ctx: dict) -> dict:
    """回傳 {state, action, entry_signal, flags[], mem, breakout, change|None}。

    ctx keys: held(bool), quality_pass(bool), earnings_blackout(bool),
              earnings_unknown(bool), is_first_day_after_earnings(bool),
              today(str), data_error(bool), seed(bool).
    """
    flags: list[str] = []
    today = ctx["today"]
    prior_mem = copy.deepcopy(mem) if mem else None
    prior_state = prior_mem["state"] if prior_mem else None

    # ── 資料錯誤（§8.4）：沿用前日狀態，灰色警示，不重算指標 ──────────────────
    if ctx.get("data_error") or ind is None:
        m = copy.deepcopy(prior_mem) if prior_mem else default_memory(state=1, since=today)
        m["data_error_streak"] = (prior_mem.get("data_error_streak", 0) + 1) if prior_mem else 1
        flags.append("data_error")
        st = m["state"]
        action = _action_for(st, m, ctx, ind=None)
        return {"state": st, "action": action, "entry_signal": None,
                "flags": flags, "mem": m, "breakout": breakout, "change": None}

    m = copy.deepcopy(prior_mem) if prior_mem else default_memory(state=1, since=today)
    m["data_error_streak"] = 0
    # schema 遷移正規化：補 last_confirmed_week、清掉已廢除的 reentry_armed 死鍵。
    m.setdefault("last_confirmed_week", None)
    if isinstance(m.get("pullback"), dict):
        m["pullback"].pop("reentry_armed", None)
    C = _conditions(ind, ctx)

    # 短歷史 / 財報未知旗標
    if ind.get("short_history"):
        flags.append("short_history")
    if ctx.get("earnings_unknown"):
        flags.append("earnings_unknown")

    # ── 首次運行 seed（§8.6）：保守初始化記憶旗標，避免噴補做指令 ─────────────
    if ctx.get("seed") or prior_mem is None:
        st, exited = _direct_state(C, ind)
        m["state"] = st
        m["state_since"] = today
        m["exited"] = exited
        m["exit_date"] = today if exited else None
        m["overheat_episode"] = {"active": st == 3, "trim_done": True}
        m["pullback"] = {"trim_to_core_done": True}
        m["pending_state5_warning"] = False
        m["state1_clean"] = (st == 1)
        m["was_below_60d"] = bool(C["below_60d"])
        # r2 P0-2：seed 把「當前完成週」標為已確認，避免上線首日對歷史週補確認。
        m["last_confirmed_week"] = ind.get("frozen_week_date")
        flags.append("seed_init")
        action = _action_for(st, m, ctx, ind=ind)
        entry = _entry_signal(ind, st, m, breakout, ctx) if not ctx["held"] else None
        if entry:
            m, breakout = _consume_entry(entry, m, breakout, today)
        return {"state": st, "action": action, "entry_signal": entry,
                "flags": flags, "mem": m, "breakout": breakout, "change": None}

    # ── §4.2 判定順序（嚴格 ⑤>④>③>②>①）──────────────────────────────────
    pending = False
    degraded = False

    # r2 P0-2：態⑤「週收盤確認」改事件式。frozen_week_date 只在一週完成後前進；
    # 當它超過 last_confirmed_week，代表「新完成週」首次判定 → 才檢查週線破線確認。
    # 假日週（週四即週收盤）與週五漏跑改週一補跑都因此被涵蓋，不會遲到或丟失。
    fwk = ind.get("frozen_week_date")
    lcw = prior_mem.get("last_confirmed_week")
    # 需有「已建立的 baseline」(lcw 非 None) 且本週嚴格較新，才算新完成週 → 才確認。
    # lcw is None（新檔/schema 遷移）→ 本次只建立 baseline，不回溯確認歷史週。
    new_completed_week = bool(fwk and lcw is not None and fwk > lcw)
    establish_baseline = bool(fwk and lcw is None)

    if prior_mem.get("exited"):
        # 1. 已是態⑤（已出場、等新 ATH）→ 維持⑤，只查 §4.4 回歸。
        new_state = 5
        regained = _check_reentry_from_exit(ind, ctx)
        if regained:
            m = default_memory(state=1, since=today)   # 清空全部記憶旗標
            m["last_confirmed_week"] = fwk             # 保留週確認進度
            new_state = 1
            flags.append("reentry_from_exit")
    elif C["earnings_gap_break"]:
        new_state = 5                                   # 2. 財報 gap 破線（當日確認，不等週收）
        flags.append("earnings_gap_break")
    elif new_completed_week and C["weekly_break"]:
        new_state = 5                                   # 3. 新完成週 + 週收盤破 52w → 確認
        flags.append("weekly_break_confirmed")
    elif C["below_52w"]:
        # 4. r2 P0-1：週中（或未確認週）破 52w → 判態④、發減碼、外掛黃牌。
        #    不再「維持原態 + 只掛 WARN 而無動作」（生死線下方滿倉等週五的 bug）。
        new_state = 4
        pending = True
    elif C["below_60d"] and C["above_52w"]:
        new_state = 4                                   # 5. 態④回檔（跌破 60MA、仍站上 52w）
    elif C["touch_3sigma"]:
        new_state = 3                                   # 6. 態③過熱（觸 3σ）
    elif C["overheat_zone"]:
        new_state = 2                                   # 7. 態②偏熱
    elif C["above_52w"] and C["alignment"]:
        new_state = 1                                   # 8. 態①健康多頭
    else:
        new_state = prior_state                         # 9. 維持前態 + degraded
        degraded = True

    if new_state is None:                               # prior_state 不存在的極端 fallback
        new_state, ex = _direct_state(C, ind)
        m["exited"] = ex

    # r2 P0-2：新完成週判定後推進 last_confirmed_week（一週只確認一次）；
    # 或首次建立 baseline（lcw 原為 None）。
    if new_completed_week or establish_baseline:
        m["last_confirmed_week"] = fwk

    # ── 記憶更新（§4.3）─────────────────────────────────────────────────────
    m["pending_state5_warning"] = pending
    if pending:
        flags.append("pending_state5_warning")
        m["state1_clean"] = False   # 態①期間掛過預警 → 不再 clean（B 型失格）
    if degraded:
        flags.append("degraded")

    # state1_clean / state_since 維護
    if new_state == 1:
        if prior_state != 1:
            m["state_since"] = today
            m["state1_clean"] = True            # 重新進入態① → 重置 clean
    else:
        if prior_state == 1 and new_state != 1:
            m["state1_clean"] = False
        if new_state != prior_state:
            m["state_since"] = today

    # 近期曾跌破 60MA（B 型 60MA 參考；站回後仍保留，由 entry 消費後清除）
    if C["below_60d"]:
        m["was_below_60d"] = True

    # 態③ overheat episode（一次性）
    oe = m["overheat_episode"]
    if C["touch_3sigma"]:
        if not oe["active"]:
            oe["active"] = True          # 首次觸 3σ → 新事件
            oe["trim_done"] = False
    else:
        # 週收盤回落至 中軌+2σ 以下 → 本輪結束（僅在週線/凍結值判定）
        fwc = ind.get("frozen_weekly_close")
        if oe["active"] and fwc is not None and ind.get("bb_upper2") is not None \
                and fwc <= ind["bb_upper2"]:
            oe["active"] = False
            oe["trim_done"] = False

    # 態⑤ 出場標記
    if new_state == 5 and not m["exited"]:
        m["exited"] = True
        m["exit_date"] = today
    if new_state != 5 and prior_state == 5 and not prior_mem.get("exited"):
        pass  # 不會發生（⑤一定 exited）；保留註記

    # 態④ pullback 記憶：進入態④（新一輪回檔）時重置減碼旗標。
    # r2 P2：移除 reentry_armed —— 態④內不可達（站回 60MA+排列多頭即判態①），
    #        回補由 ①-ADD_TRIGGER 正確發出。
    pb = m["pullback"]
    if new_state == 4 and prior_state != 4:
        pb["trim_to_core_done"] = False

    m["state"] = new_state

    # ── 動作映射（§5）──────────────────────────────────────────────────────
    action = _action_for(new_state, m, ctx, ind=ind, pending=pending)

    # ── 一次性指令「自動推定 done」：發出後標記，下一輪不重發（§4.3）──────────
    if action == "TRIM_1_3":
        m["overheat_episode"]["trim_done"] = True
    elif action == "TRIM_TO_CORE_50":
        m["pullback"]["trim_to_core_done"] = True
    elif action == "ADD_TRIGGER":
        m["was_below_60d"] = False   # 加碼板機消費掉「曾跌破 60MA」，不隔日重亮

    # ── 進場訊號（§4.6，僅 watchlist held=false）─────────────────────────────
    entry = None
    if not ctx["held"]:
        entry = _entry_signal(ind, new_state, m, breakout, ctx)
        if entry:
            m, breakout = _consume_entry(entry, m, breakout, today)

    # ── 突破登記簿維護（§4.5）────────────────────────────────────────────────
    breakout = _update_breakout(ind, breakout, ctx, m)

    change = None
    if prior_state is not None and new_state != prior_state:
        change = {"symbol": ticker, "from": prior_state, "to": new_state, "action": action}

    return {"state": new_state, "action": action, "entry_signal": entry,
            "flags": flags, "mem": m, "breakout": breakout, "change": change}


# ── §4.4 態⑤回歸：close 突破 ATH 且 quality_pass ──────────────────────────────
def _check_reentry_from_exit(ind: dict, ctx: dict) -> bool:
    return bool(ind.get("is_new_ath_today") and ctx.get("quality_pass"))


# ── §5 動作映射 ─────────────────────────────────────────────────────────────
def _action_for(state: int, m: dict, ctx: dict, ind: Optional[dict] = None,
                pending: bool = False) -> str:
    held = ctx["held"]
    blackout = ctx.get("earnings_blackout")
    pend = bool(pending or m.get("pending_state5_warning"))

    if state == 5:
        return "EXIT_ALL" if held else "DISQUALIFIED"

    # r2 P0-1：態④減碼優先於 pending —— 週中破線時，持有者先拿到「減至核心 50%」
    # 指令（黃牌另由 flags 同列顯示），減碼已 done 才退回 WARN_PENDING_5。
    if state == 4 and held and not m["pullback"]["trim_to_core_done"]:
        return "TRIM_TO_CORE_50"
    if pend:
        # WARN 是持有側指令（本週收盤若仍 < 52w 即全出）；watchlist 無倉可出 → 落入
        # 下方 by-state（態④ watch → WAIT），黃牌仍由 flags 呈現。
        if held:
            return "WARN_PENDING_5"

    if state == 1:
        if held:
            # 加碼板機：回踩後站回 60MA 且 非靜默期（B 型 reentry 語義）
            reclaimed = bool(ind and not ind.get("below_60d"))
            if m.get("was_below_60d") and reclaimed and not blackout:
                return "ADD_TRIGGER"
            return "NONE"
        return "WATCH"   # 訊號由 _entry_signal 另填 entry_signal 欄；action 用 WATCH
    if state == 2:
        return "NO_ADD" if held else "WAIT"
    if state == 3:
        if held:
            return "TRIM_1_3" if not m["overheat_episode"]["trim_done"] else "NO_ADD"
        return "WAIT"
    if state == 4:
        # held 且 trim 已 done（上方未攔截）→ 抱核心；watchlist → 觀望。
        return "HOLD_CORE" if held else "WAIT"
    return "NONE"


# ── §4.6 進場訊號（held=false）──────────────────────────────────────────────
def _entry_signal(ind: dict, state: int, m: dict, breakout: Optional[dict],
                  ctx: dict) -> Optional[str]:
    if state != 1 or not ctx.get("quality_pass") or ctx.get("earnings_blackout"):
        return None

    # A 突破型：突破「首日」收盤創新高（前一日未創）且 前一日 pct_vs_ath ≥ -5%。
    # r2 P2：加 not prev_is_new_ath 去重 —— 連續創高日（如 LLY 一路噴）不重發 A。
    prev = ind.get("prev_pct_vs_ath")
    if (ind.get("is_new_ath_today") and not ind.get("prev_is_new_ath")
            and prev is not None and prev >= -ATH_PROXIMITY):
        return "ENTRY_A"

    # B 回踩型：態①全程乾淨（未掛過 pending warning）
    if not m.get("state1_clean"):
        return None
    close = ind.get("close")
    # B-前高：未完成首次回測的 breakout，曾進入 prior_ath±2%，今日站回前高之上
    if breakout and not breakout.get("first_retest_done") and breakout.get("entered_band"):
        pa = breakout.get("prior_ath")
        if pa and close is not None and close >= pa:
            return "ENTRY_B"
    # B-60MA：近期曾跌破 60MA，今日收盤站回 60MA 之上
    if m.get("was_below_60d") and not ind.get("below_60d") \
            and ind.get("ma60d") is not None and close is not None and close > ind["ma60d"]:
        return "ENTRY_B"
    return None


def _consume_entry(entry: str, m: dict, breakout: Optional[dict], today: str):
    """訊號觸發後消費對應的一次性記憶，避免隔日重複亮燈。"""
    if entry == "ENTRY_B":
        if breakout and not breakout.get("first_retest_done") and breakout.get("entered_band"):
            breakout = dict(breakout)
            breakout["first_retest_done"] = True
            breakout["retest_date"] = today
        m["was_below_60d"] = False
    return m, breakout


# ── §4.5 突破登記簿維護 ─────────────────────────────────────────────────────
def _update_breakout(ind: dict, breakout: Optional[dict], ctx: dict, m: dict):
    close = ind.get("close")
    # 新 ATH 突破首日（今日創高且前一日未創）→ 寫入/更新登記。
    if ind.get("is_new_ath_today") and not ind.get("prev_is_new_ath"):
        prior_ath = ind.get("ath_prev")
        if prior_ath:
            breakout = default_breakout(ctx["today"], round(prior_ath, 4))
            return breakout
    # 既有 breakout：偵測收盤進入 prior_ath±2% 區域 → entered_band=true（§4.5 首次回測）
    if breakout and not breakout.get("first_retest_done"):
        pa = breakout.get("prior_ath")
        if pa and close is not None:
            lo, hi = pa * (1 - RETEST_BAND), pa * (1 + RETEST_BAND)
            if lo <= close <= hi:
                breakout = dict(breakout)
                breakout["entered_band"] = True
    return breakout
