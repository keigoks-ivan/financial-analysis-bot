#!/usr/bin/env python3
"""detective_state.py — 市場偵探 v2 狀態機（純函數、零 IO、零外部依賴、可單測）.

被 build_detective.py 呼叫；本模組不讀寫任何檔案、不解析任何來源，只吃
「本 tick 滿足條件的 met 集合」與前次 state，吐出新 state（含 transitions_today）。

── 轉移參數表 ──────────────────────────────────────────────
GRACE_DAYS             = 3    條件消失後的 cooling 寬限（交易日）；連續 miss 超過即 resolved
REVIVE_WINDOW          = 5    resolved 後 N 交易日內重現 → 直接回 active（非 new、不算新增通知）
SUSTAINED_DAYS         = 5    黃燈連續滿足 ≥N 交易日 → 升級觸發 (b) 的天數腿
SUSTAINED_SCORE_RATIO  = 0.8  且當日 score ≥ 歷史峰值 × 此比例 → 升級觸發 (b) 成立
FLAP_MUTE_THRESHOLD    = 3    flap_count ≥ 此值 → 自動 mute（只擋即時信，仍進日摘）
MUTE_DAYS              = 14   mute_until = as_of + N 日曆天
IMMEDIATE_MIN_GAP_DAYS = 7    同鍵即時信最小間隔（日曆天；本 phase 只記帳，Phase 4 消費）
HISTORY_RETENTION_DAYS = 90   history 保留天數（日曆天，按 resolved_at 修剪）
AS_OF_LOG_CAP          = 120  交易日序列（as_of_log）保留筆數

── 狀態圖 ──────────────────────────────────────────────────
absent ──首日滿足──▶ new ──第 2 個資料日仍滿足──▶ active
active／new ──條件消失──▶ cooling（寬限 GRACE_DAYS 交易日，頁面灰化顯示）
cooling ──寬限內再滿足──▶ active（flap_count＋1）
cooling ──寬限盡（連續 miss > GRACE_DAYS）──▶ resolved（寫入 history，從 keys 移除）
resolved ──REVIVE_WINDOW 交易日內重現──▶ active（直接回，flap_count＋1，非 new、
          不算新增通知事件；first_seen／days_active／score_peak 自 history 延續）
active ──升級觸發──▶ escalated（一次性事件態：記入 escalations 後回 active、sev 更新；
          當日 display state 由 build 端從 transitions_today 的 to=="escalated" 推得）

升級觸發（_check_escalation）：
  (a) sev_jump   — 源頭 sev 黃→紅
  (b) sustained  — 黃燈連續 met_streak ≥ SUSTAINED_DAYS 且當日 score ≥
                   score_peak×SUSTAINED_SCORE_RATIO（每 episode 至多一次）
  (c) composite  — 該鍵成為新 fire 紅級 composite 成員
                   （met[key]["composite_red"]；Phase 3 掛鉤，本 phase 恆缺省）

flap／mute：cooling→active 回彈或 resolved→active 復活都算一次 flap；
flap_count ≥ FLAP_MUTE_THRESHOLD 時設 notify.mute_until = as_of＋MUTE_DAYS 日曆天
（只擋即時信，訊號本身照常進 latest.json 日摘；通知消費是 Phase 4）。

── 交易日定義 ──────────────────────────────────────────────
「交易日」以引擎見過的資料 as_of 序列（state["as_of_log"]）計，不是日曆日：
  · 寬限（GRACE_DAYS）與復活窗（REVIVE_WINDOW）用 as_of_log 內的索引距離
    （鍵日期若已被 log cap 擠出，退回日曆天差，屬保守近似）；
  · mute_until／last_immediate 間隔／history 修剪用日曆天（ISO date 直減）。

── 冪等（replay 守則）───────────────────────────────────────
advance(state, met, as_of)：
  · as_of <= state["as_of"] → 完全 no-op，原 state 原樣回傳（不重置 transitions、
    不重複 append escalations／history）。workflow_run 重複觸發因此安全。
  · 只有 as_of > state["as_of"] 才是「真推進」（一次 advance＝一個交易日 tick）。
  · source_snapshots 守則：本模組不讀不寫 state["source_snapshots"]——它由
    build_detective.py 在「真推進」時才更新；replay（as_of <= state.as_of）時
    build 端**不得**改寫 source_snapshots，否則事件型來源（regime／macro_clock／
    variance fleet）的 delta 基準會被提前吃掉，翻折事件將無法在下一個真交易日
    被偵測到。

── keys entry 欄位 ─────────────────────────────────────────
{"state","sev","peak_sev","first_seen","last_seen","last_met","days_active",
 "miss_days","met_streak","flap_count","score_peak","escalations":[],
 "display":{…訊號呈現欄位，met tick 時由 build 端餵入、cooling 期沿用…},
 "notify":{"last_immediate","mute_until"}}
history entry：{"key","first_seen","resolved_at","peak_sev","days_active",
 "flap_count","score_peak"}（後兩欄供 REVIVE_WINDOW 復活時延續 episode 帳）。
"""
import copy
from datetime import date, timedelta

GRACE_DAYS = 3
REVIVE_WINDOW = 5
SUSTAINED_DAYS = 5
SUSTAINED_SCORE_RATIO = 0.8
FLAP_MUTE_THRESHOLD = 3
MUTE_DAYS = 14
IMMEDIATE_MIN_GAP_DAYS = 7
HISTORY_RETENTION_DAYS = 90
AS_OF_LOG_CAP = 120

STATE_SCHEMA = "detective-state-v1"


def empty_state():
    return {"schema": STATE_SCHEMA, "as_of": "", "as_of_log": [],
            "source_snapshots": {}, "keys": {}, "transitions_today": [],
            "history": []}


def _parse(d):
    return date.fromisoformat(d)


def days_between(a, b):
    """日曆天差（絕對值）。"""
    return abs((_parse(b) - _parse(a)).days)


def add_days(d, n):
    return (_parse(d) + timedelta(days=n)).isoformat()


def _trading_dist(log, a, b):
    """as_of_log 內的索引距離（交易日）；a 若已被 cap 擠出則退回日曆天差。"""
    try:
        return abs(log.index(b) - log.index(a))
    except ValueError:
        return days_between(a, b)


def _check_escalation(entry, sev, score, new_peak, met_item):
    """升級三觸發，回傳 escalation dict（不含 date）或 None。

    呼叫時 entry 的 met_streak 已含本日；entry["sev"] 仍為前一 tick 的 sev。
    (a) sev_jump：黃→紅。
    (b) sustained：黃燈連續 met_streak ≥ SUSTAINED_DAYS 且 score ≥ 峰值×0.8，
        每 episode 至多一次（以 escalations 內已有 type=="sustained" 判重）。
    (c) composite：met_item["composite_red"] 為真（Phase 3 掛鉤）。
    """
    if entry.get("sev") == "yellow" and sev == "red":
        return {"from": "yellow", "to": "red", "type": "sev_jump",
                "reason": "源頭嚴重度黃→紅"}
    if met_item.get("composite_red") and not any(
            x.get("type") == "composite" for x in entry.get("escalations", [])):
        return {"from": entry.get("sev"), "to": sev, "type": "composite",
                "reason": "成為新觸發紅級 composite 成員"}
    if (sev == "yellow" and entry.get("met_streak", 0) >= SUSTAINED_DAYS
            and new_peak > 0 and score >= new_peak * SUSTAINED_SCORE_RATIO
            and not any(x.get("type") == "sustained"
                        for x in entry.get("escalations", []))):
        return {"from": "yellow", "to": "yellow", "type": "sustained",
                "reason": (f"黃燈連續 {entry['met_streak']} 交易日"
                           f"且當日分數仍達峰值 {int(SUSTAINED_SCORE_RATIO*100)}%")}
    return None


def _prune_history(history, as_of):
    return [h for h in history
            if days_between(h["resolved_at"], as_of) <= HISTORY_RETENTION_DAYS]


def advance(state, met, as_of):
    """推進一個交易日 tick；純函數（不改動傳入 state）。

    met = {key: {"sev": "red"/"yellow", "score": float,
                 "display": {…呈現欄位…}, ["composite_red": bool]}}
    回傳新 state。冪等：as_of <= state["as_of"] → 原 state 原樣回傳（no-op）。
    """
    if state and state.get("as_of") and as_of <= state["as_of"]:
        return state
    st = copy.deepcopy(state) if state else empty_state()
    for k, v in empty_state().items():
        st.setdefault(k, v)
    st["transitions_today"] = []
    st["as_of_log"] = (st["as_of_log"] + [as_of])[-AS_OF_LOG_CAP:]
    trans, keys, history = st["transitions_today"], st["keys"], st["history"]

    def _t(key, frm, to, reason):
        trans.append({"key": key, "from": frm, "to": to,
                      "date": as_of, "reason": reason})

    # ── A. 本 tick 滿足條件的 key ──
    for key in sorted(met):
        m = met[key]
        sev = m.get("sev", "yellow")
        score = float(m.get("score", 0.0))
        entry = keys.get(key)

        if entry is None:
            # 復活檢查：REVIVE_WINDOW 交易日內 resolved 的同鍵 episode
            hidx = next((i for i in range(len(history) - 1, -1, -1)
                         if history[i]["key"] == key), None)
            hit = None
            if hidx is not None and _trading_dist(
                    st["as_of_log"], history[hidx]["resolved_at"], as_of) <= REVIVE_WINDOW:
                hit = history.pop(hidx)
            if hit:
                flap = int(hit.get("flap_count", 0)) + 1
                entry = {"state": "active", "sev": sev,
                         "peak_sev": ("red" if "red" in (sev, hit.get("peak_sev"))
                                      else "yellow"),
                         "first_seen": hit["first_seen"], "last_seen": as_of,
                         "last_met": as_of,
                         "days_active": int(hit.get("days_active", 0)) + 1,
                         "miss_days": 0, "met_streak": 1, "flap_count": flap,
                         "score_peak": max(float(hit.get("score_peak", 0.0)), score),
                         "escalations": [],
                         "notify": {"last_immediate": None, "mute_until": None}}
                if flap >= FLAP_MUTE_THRESHOLD:
                    entry["notify"]["mute_until"] = add_days(as_of, MUTE_DAYS)
                if "display" in m:
                    entry["display"] = m["display"]
                keys[key] = entry
                _t(key, "resolved", "active",
                   f"resolved 後 {REVIVE_WINDOW} 交易日內重現，直接回 active"
                   f"（flap {flap}，不計新增通知）")
            else:
                entry = {"state": "new", "sev": sev, "peak_sev": sev,
                         "first_seen": as_of, "last_seen": as_of, "last_met": as_of,
                         "days_active": 1, "miss_days": 0, "met_streak": 1,
                         "flap_count": 0, "score_peak": score, "escalations": [],
                         "notify": {"last_immediate": None, "mute_until": None}}
                if "display" in m:
                    entry["display"] = m["display"]
                keys[key] = entry
                _t(key, "absent", "new", "首日滿足條件")
            continue

        # 既有 key：狀態回推
        if entry["state"] == "cooling":
            entry["state"] = "active"
            entry["miss_days"] = 0
            entry["met_streak"] = 0
            entry["flap_count"] = int(entry.get("flap_count", 0)) + 1
            if (entry["flap_count"] >= FLAP_MUTE_THRESHOLD
                    and not entry["notify"].get("mute_until")):
                entry["notify"]["mute_until"] = add_days(as_of, MUTE_DAYS)
            _t(key, "cooling", "active",
               f"寬限內條件再滿足（flap {entry['flap_count']}）")
        elif entry["state"] == "new":
            entry["state"] = "active"
            _t(key, "new", "active", "第 2 個資料日仍滿足條件")

        entry["days_active"] = int(entry.get("days_active", 0)) + 1
        entry["met_streak"] = int(entry.get("met_streak", 0)) + 1
        entry["last_seen"] = as_of
        entry["last_met"] = as_of
        new_peak = max(float(entry.get("score_peak", 0.0)), score)

        esc = _check_escalation(entry, sev, score, new_peak, m)
        if esc:
            esc = dict(esc, date=as_of)
            entry["escalations"].append(esc)
            _t(key, entry["state"], "escalated", esc["reason"])

        entry["sev"] = sev
        if sev == "red":
            entry["peak_sev"] = "red"
        entry["score_peak"] = new_peak
        if "display" in m:
            entry["display"] = m["display"]

    # ── B. 本 tick 未滿足、但仍在 keys 的 key ──
    for key in sorted(list(keys)):
        if key in met:
            continue
        entry = keys[key]
        prev = entry["state"]
        entry["last_seen"] = as_of
        entry["met_streak"] = 0
        if prev in ("new", "active"):
            entry["state"] = "cooling"
            entry["miss_days"] = 1
            _t(key, prev, "cooling",
               f"條件消失，進入 {GRACE_DAYS} 交易日寬限")
        elif prev == "cooling":
            entry["miss_days"] = int(entry.get("miss_days", 0)) + 1
            if entry["miss_days"] > GRACE_DAYS:
                history.append({"key": key,
                                "first_seen": entry["first_seen"],
                                "resolved_at": as_of,
                                "peak_sev": entry.get("peak_sev", entry.get("sev")),
                                "days_active": entry.get("days_active", 0),
                                "flap_count": entry.get("flap_count", 0),
                                "score_peak": entry.get("score_peak", 0.0)})
                del keys[key]
                _t(key, "cooling", "resolved",
                   f"寬限 {GRACE_DAYS} 交易日已盡，episode 結案入 history")

    st["history"] = _prune_history(history, as_of)
    st["as_of"] = as_of
    return st
