#!/usr/bin/env python3
"""build_detective.py — 市場偵探 v2（持續狀態機、純機械、零 LLM、確定性）.

Phase 1（detective-v1）是無狀態聚合警報網；v2 加上跨日持續狀態機：
每條訊號有穩定機器鍵與生命週期（new → active → cooling → resolved，
含 escalated 一次性事件態與 resolved 後短窗復活），真相源存
docs/detective/data/state.json（schema detective-state-v1，狀態機邏輯在
scripts/detective_state.py 純函數庫）。

聚合源（v1 的 3 源 → v2 的 9 源家族）：
  1. monitor    — monitor 異常引擎（alerts.json 紅／黃燈＋三點分位軌跡 enrich）
  2. crowding   — COT 5 年分位極端／ETF 動能分位極端／主題擁擠 top3 且 ≥70
  3. rotation   — rotation radar cross_asset 120d 象限翻轉（已確認／接近中）
  4. reversal   — monitor latest.json 每條 series 的 p60→p20→pctile 三點翻折
                  ≥30 分位點（與 home pulse 同族演算法自算，不讀 pulse.json）
  5. regime     — regime composite 位置位移 ≥0.15（0-1 尺度）或任一軸 pill 變更
                  （週更、事件型：對 state.json source_snapshots 比差）
  6. macro_clock— 總經時鐘象限遷移（月頻、事件型）；遷入滯脹＝紅
  7. variance   — 財測落差紅旗（drift < −15%，白旗＝幣別待確認永不出訊號）
                  逐 ticker 黃；同週新增紅旗 ≥3 檔加一條 fleet 級紅
  8. kill       — ID／macro kill_metrics 機械對帳（kill_watch.json，Phase 6）：
                  breached 條目→紅（附「建議 spawn industry-thesis-critic 複審」），
                  near 不出訊號（只留頁面對帳表）；缺檔／stale→誠實標示不炸
  9. sector     — 產業結構分歧（回答「今天是誰在跌」）：單一產業 ETF 當日 z 極端
                  而大盤持平的單日分歧（下跌／對稱向上）、同日多產業分歧叢集（≥2 黃／
                  ≥3 紅）、us_sectors 120d 象限翻轉（複用 cross_asset 邏輯換宇宙）。
                  半導體無獨立 GICS sector，以費城半導體 SOX 為代理併入產業宇宙掃描。

穩定機器鍵：source:cat:series_key[:dir]。方向敏感的 move 型訊號把 dir 納入鍵
（同商品先爆漲後爆跌＝兩個 episode）；水位型不帶 dir。v1 的 source:label 鍵
已證實脆弱（2026-07-14 出現 21/21 全標 new），廢棄。

冪等：同一組 sources as_of 重跑輸出逐位元相同——advance() 對 as_of 未推進的
replay 是完全 no-op（transition 以 (key, as_of) 判重）；source_snapshots 只在
「真推進」tick 更新（replay 時不得改寫，否則事件型來源的 delta 基準被吃掉）；
寫檔沿用 build_monitor.py 的 write_json_if_changed 零 churn 協議。
workflow_run 重複觸發因此安全。

輸出：
  · docs/detective/data/latest.json — schema detective-v2（頁面渲染）
  · docs/detective/data/state.json  — schema detective-state-v1（狀態機真相源）
  · detective_alert.txt（未 commit）— 紅燈級＋今日新增＋今日升級（扣除 mute），
    供 GitHub Actions email 步驟

描述器紀律：只陳述事實，不判斷、不擇時、不給買賣指令。
"""
import json
import os
import re
from datetime import date, timedelta

import detective_rules as drules
import detective_state as dstate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

SHORT = {
    "房地產REIT": "房地產", "美長天期公債": "美長債", "投資級公司債": "投資級債",
    "成熟市場股": "成熟股", "新興市場股": "新興市場", "大宗商品": "大宗",
    "高收益債": "高收益",
}

# 各源新鮮度閾值（日曆天，頻率×2；超過即進 sources_stale[]）
SOURCE_FRESH_DAYS = {
    "monitor": 4, "crowding": 16, "rotation": 4,
    "regime": 16, "macro_clock": 62, "variance": 16, "kill": 10,
    "sector": 4,   # as_of＝monitor as_of（日更）
}

REVERSAL_FLIP_PCTL = 30.0     # 三點翻折門檻（分位點，兩腿皆須 ≥ 此值）
# ── 源 9：sector（產業結構分歧）門檻常數 ────────────────────────────────
# 描述器紀律，PREREG 凍結至下輪校準（2026-10）；ALERT_WEIGHTS 不新增成分，
# sector 黃燈計入 yellow_signal（硬封頂）、紅燈計入 red_signal。
SECTOR_DIVERGE_Z = -2.0       # 單一產業當日 z ≤ 此值 → 下跌分歧候選
SECTOR_UP_DIVERGE_Z = 2.0     # 對稱向上分歧：產業 z ≥ 此值（描述過熱集中）
SECTOR_MKT_FLAT_Z = 1.0       # 大盤持平：|S&P 500 z| ≤ 此值（下跌分歧要求 sp500 z ≥ −1.0；向上要求 ≤ +1.0）
SECTOR_CLUSTER_MIN = 2        # 分歧叢集黃燈門檻（同日 ≥N 個下跌分歧產業）
SECTOR_CLUSTER_RED = 3        # 分歧叢集升紅門檻（同日 ≥N 個）
# 產業宇宙：monitor sectors 類全體（動態掃描）＋ 半導體代理 SOX（隸 indices 類）
SECTOR_EXTRA = [("indices", "sox")]  # 半導體無獨立 GICS sector，取費半指數為代理
REGIME_COMPOSITE_MOVE = 0.15  # regime composite 位移門檻（0-1 尺度）
VARIANCE_DRIFT_RED = -15.0    # 財測落差紅旗門檻（%）
VARIANCE_FLEET_MIN = 3        # 同週新增紅旗 ≥N 檔 → fleet 級紅
PERSIST_BONUS_PER_DAY = 0.2   # 持續加成：days_active×0.2，上限 2.0
PERSIST_BONUS_CAP = 2.0
COMPOSITE_BONUS = 1.0         # composite 成員加成（Phase 3 掛鉤）

# ── 警戒度描述器（alert_level）常數 ─────────────────────────────────────
# 純視覺聚合描述器：把警報網當前狀態壓成單一 0-100 溫度數字，餵頁面半圓威脅
# 指針。**非擇時訊號、非決策閘、不改任何裁決**，故不登記 rule_ledger（見
# compute_alert_level docstring）。權重集中於此，PREREG 凍結至下輪校準
# （2026-10）；校準時只在此調 pts／cap，公式結構不動。
# 每成分＝命中數 × pts，各自封頂 cap，加總後 clamp 0-100。黃燈 cap 是關鍵：
# 今日 26 條黃燈也只計 18 分，多黃燈**不得單獨把指針頂到緊張/警戒**。
ALERT_WEIGHTS = {
    "red_signal":       {"pts": 8.0,  "cap": 30.0},   # 紅燈 signal（重）
    "yellow_signal":    {"pts": 0.7,  "cap": 18.0},   # 黃燈 signal（輕＋硬封頂）
    "composite_red":    {"pts": 12.0, "cap": 36.0},   # composite fired 紅（重）
    "composite_yellow": {"pts": 6.0,  "cap": 18.0},   # composite fired 黃
    "composite_near":   {"pts": 6.0,  "cap": 15.0},   # near-fire（met==min_true−1，中）
    "kill_breached":    {"pts": 14.0, "cap": 42.0},   # kill breached（很重）
    "kill_near":        {"pts": 2.5,  "cap": 15.0},   # kill near（輕）
    "escalated":        {"pts": 4.0,  "cap": 16.0},   # 今日升級狀態數
    "sustained":        {"pts": 2.0,  "cap": 12.0},   # 持續紅燈（days_active 高）
}
ALERT_SUSTAINED_DAYS = 5      # 紅燈 days_active ≥ 此值算「持續」
ALERT_BANDS = [               # (上界 exclusive, band, 中文標籤)；calm 0-20 … alert 80-100
    (20.0, "calm", "平靜"), (40.0, "watch", "留意"),
    (60.0, "warming", "升溫"), (80.0, "tense", "緊張"),
    (float("inf"), "alert", "警戒"),
]
ALERT_DRIVER_LABELS = {
    "red_signal":       lambda n: f"{n} 條紅燈訊號",
    "yellow_signal":    lambda n: f"{n} 條黃燈訊號（封頂計分）",
    "composite_red":    lambda n: f"{n} 項複合規則觸發（紅）",
    "composite_yellow": lambda n: f"{n} 項複合規則觸發（黃）",
    "composite_near":   lambda n: f"{n} 項複合規則距觸發差 1 個成員",
    "kill_breached":    lambda n: f"{n} 條 kill 指標越線",
    "kill_near":        lambda n: f"{n} 條 kill 指標接近閾值",
    "escalated":        lambda n: f"{n} 條訊號今日升級",
    "sustained":        lambda n: f"{n} 條紅燈持續 ≥{ALERT_SUSTAINED_DAYS} 日",
}


# ── zero-churn IO（協議抄 build_monitor.py）──────────────────────────────

def _serialize(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def write_json_if_changed(path, obj, volatile=("generated_at",)) -> bool:
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(_serialize(obj))
    return True


def _load(rel, default=None):
    return load_json(os.path.join(DOCS, rel), default)


# ── 小工具 ─────────────────────────────────────────────────────────────

def _fmt(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def _slug(s):
    out = "".join(ch if ch.isalnum() else "-" for ch in str(s).lower())
    return re.sub(r"-+", "-", out).strip("-") or "x"


def quad(r, m):
    if r >= 100 and m >= 100:
        return "領先"
    if r >= 100 and m < 100:
        return "轉弱"
    if r < 100 and m >= 100:
        return "改善"
    return "落後"


def _mon_series(latest, cat, key):
    for c in latest.get("categories", []):
        if c.get("key") != cat:
            continue
        for it in c.get("items", []):
            if it.get("key") == key:
                return it
    return None


def _score(sev, magnitude):
    """0-15 連續分：紅燈基底 10、黃燈 5，加幅度（|z|／分位極端／天數），上限 +5。"""
    base = 10.0 if sev == "red" else 5.0
    return round(base + min(magnitude, 5.0), 2)


def _sig(key, source, cat, label, fact, sev, magnitude, context=""):
    return {"key": key, "source": source, "cat": cat, "label": label,
            "fact": fact, "sev": sev, "score_base": _score(sev, magnitude),
            "context": context}


def _dir_from_alert(rule, msg):
    """move 型訊號的方向；水位型（pctile）不帶 dir。"""
    if rule == "pctile":
        return None
    if "▲" in msg or "上漲" in msg or "新高" in msg:
        return "up"
    if "▼" in msg or "下跌" in msg or "新低" in msg:
        return "down"
    return None


# ── 源 1：monitor 異常（alerts.json 當日紅／黃燈，enrich 軌跡）───────────

def monitor_signals(latest, alerts, as_of):
    out = []
    for a in (alerts.get("days", {}) or {}).get(as_of, []):
        sev = a.get("sev", "yellow")
        cat, skey = a.get("cat", ""), a.get("key", "")
        it = _mon_series(latest, cat, skey)
        mag, ctx = 2.0, ""
        if it:
            if a.get("rule") == "move_z":
                mag = abs(it.get("z", 0) or 0)
            elif a.get("rule") == "pctile":
                mag = abs((it.get("pctile", 50) or 50) - 50) / 10.0
            if all(k in it for k in ("p60", "p20", "pctile")):
                ctx = f"分位 {_fmt(it['p60'])}→{_fmt(it['p20'])}→{_fmt(it['pctile'])}"
        d = _dir_from_alert(a.get("rule"), a.get("msg", ""))
        key = f"monitor:{cat}:{skey}" + (f":{d}" if d else "")
        out.append(_sig(key, "monitor", cat, (it or {}).get("label", skey),
                        a.get("msg", ""), sev, mag, ctx))
    return out


# ── 源 4：reversal（三點分位翻折，直讀 monitor latest.json）──────────────

def reversal_signals(latest):
    out = []
    for c in latest.get("categories", []):
        ckey = c.get("key", "")
        if ckey.startswith("_"):
            continue
        for it in c.get("items", []):
            if it.get("stale"):
                continue
            p60, p20, pc = it.get("p60"), it.get("p20"), it.get("pctile")
            if p60 is None or p20 is None or pc is None:
                continue
            if (p60 - p20 >= REVERSAL_FLIP_PCTL
                    and pc - p20 >= REVERSAL_FLIP_PCTL):
                d, shape = "up", "先落後回升（谷底翻折）"
                legs = min(p60 - p20, pc - p20)
            elif (p20 - p60 >= REVERSAL_FLIP_PCTL
                    and p20 - pc >= REVERSAL_FLIP_PCTL):
                d, shape = "down", "先升後回落（峰頂翻折）"
                legs = min(p20 - p60, p20 - pc)
            else:
                continue
            label = it.get("label", it.get("key", ""))
            traj = f"{_fmt(p60)}→{_fmt(p20)}→{_fmt(pc)}"
            out.append(_sig(
                f"reversal:{ckey}:{it.get('key')}:{d}", "reversal", ckey, label,
                (f"{label} 一年分位三點路徑 {traj}，{shape}，"
                 f"兩腿皆 ≥{_fmt(REVERSAL_FLIP_PCTL)} 分位點"),
                "yellow", legs / 10.0))
    return out


# ── 源 2：crowding（COT 極端＋主題擁擠＋ETF 動能極端）────────────────────

def crowding_signals(crowd):
    if not crowd:
        return []
    out = []
    asof = crowd.get("cot_as_of", "")
    for m in crowd.get("cot", []):
        p5 = m.get("pctile_5y", 50)
        if not (m.get("extreme") or p5 >= 90 or p5 <= 10):
            continue
        side = "偏多極端" if p5 >= 90 else "偏空極端"
        out.append(_sig(
            f"crowding:cot:{_slug(m['market'])}", "crowding", "cot",
            f"{m['market']} 投機部位",
            (f"{m['market']} COT {m.get('direction', '')}、5 年分位 {_fmt(p5)}"
             f"（{side}；淨 {m.get('net_pct_oi')}% OI）"),
            "yellow", abs(p5 - 50) / 10.0, f"COT as-of {asof}"))
    for e in crowd.get("etf", []):
        mp = e.get("momentum_pctile", 50)
        if mp is None or not (mp >= 95 or mp <= 5):
            continue
        out.append(_sig(
            f"crowding:etf:{e.get('ticker')}", "crowding", "etf",
            f"{e.get('label', e.get('ticker'))} 動能",
            (f"{e.get('label')}（{e.get('ticker')}）動能分位 {_fmt(mp)}"
             f"、偏離分位 {_fmt(e.get('deviation_pctile', 0) or 0)}"),
            "yellow", abs(mp - 50) / 10.0))
    themes = sorted((t for t in crowd.get("themes", []) if t.get("score")),
                    key=lambda t: -t["score"])[:3]
    for t in themes:
        if t["score"] < 70:
            continue
        out.append(_sig(
            f"crowding:theme:{_slug(t['name'])}", "crowding", "theme",
            f"主題擁擠：{t['name']}",
            f"{t['name']} 擁擠分 {_fmt(t['score'])}（五維綜合，排名第 {t.get('rank', '?')}）",
            "yellow", (t["score"] - 70) / 10.0))
    return out


# ── 象限翻轉偵測（cross_asset 與 us_sectors 共用；只換宇宙與訊號家族）────────

def _quadrant_signals(radar, universe_key, source, cat):
    """radar 某宇宙 120d 框架的象限翻轉訊號（RS-M 升破／跌破 100，已確認／接近中）。
    key＝{source}:{cat}:{ticker}:{dir}；cross_asset→(rotation,quadrant)、
    us_sectors→(sector,rotation)。偵測邏輯完全一致，僅換 universe。"""
    if not radar:
        return []
    uni = next((u for u in radar.get("universes", [])
                if u.get("key") == universe_key), None)
    if not uni:
        return []
    out = []
    for mem in uni.get("members", []):
        fr = mem.get("frames", {}).get("120")
        if not fr or not fr.get("trail"):
            continue
        trail = fr["trail"]
        n = len(trail)
        cross = None
        for i in range(n - 1, max(n - 1 - 8, 0), -1):
            if (trail[i - 1]["m"] >= 100) != (trail[i]["m"] >= 100):
                cross = i
                break
        if cross is None:
            continue
        held = n - cross
        m_now = trail[-1]["m"]
        disp = abs(m_now - 100.0)
        if disp < 0.15 and held < 2:
            continue
        q_before = quad(trail[cross - 1]["r"], trail[cross - 1]["m"])
        q_now = quad(trail[-1]["r"], m_now)
        confirmed = held >= 5 or (held >= 3 and disp >= 0.5)
        label = mem.get("label", mem.get("ticker", ""))
        tk = mem.get("ticker", "")
        short = SHORT.get(label, label)
        # sectors 標籤已含 ticker（如「XLK 科技」）→ 去重顯示；cross_asset 不含
        name = short[len(tk):].strip() if tk and short.startswith(tk) else short
        state = "已確認" if confirmed else "接近中"
        d = "up" if m_now >= 100 else "down"
        out.append(_sig(
            f"{source}:{cat}:{tk}:{d}", source, cat,
            f"{name} {tk} 動能".strip(),
            (f"{name} {tk} 象限 {q_before}→{q_now}"
             f"（RS-M {'升破' if d == 'up' else '跌破'} 100，{state}）").strip(),
            "yellow", (2.5 if confirmed else 1.0) + min(disp, 2.0),
            f"持穩 {held} 交易日、RS-M {m_now:.2f}"))
    return out


# ── 源 3：rotation（cross_asset 120d 象限翻轉）───────────────────────────

def rotation_signals(radar):
    return _quadrant_signals(radar, "cross_asset", "rotation", "quadrant")


# ── 源 5：regime（週更、事件型：對 source_snapshots 比差）─────────────────

def regime_signals(regime, snap):
    """回傳 (signals, new_snap)。首次僅 seed baseline 不出訊號；
    generated_at 未變（同一期資料）不重比。"""
    if not regime:
        return [], snap
    gen = regime.get("generated_at", "")
    pos = (regime.get("composite") or {}).get("pos_0to1")
    axes = {a["key"]: {"pill": a.get("pill", ""), "name": a.get("name", a["key"])}
            for a in regime.get("axes", []) if a.get("key")}
    new_snap = {"generated_at": gen, "composite_pos": pos,
                "axes": {k: v["pill"] for k, v in axes.items()}}
    if not snap or snap.get("generated_at") == gen:
        return [], (snap or new_snap)
    out = []
    prev_pos = snap.get("composite_pos")
    if pos is not None and prev_pos is not None:
        delta = pos - prev_pos
        if abs(delta) >= REGIME_COMPOSITE_MOVE:
            out.append(_sig(
                "regime:composite", "regime", "composite", "regime 綜合位置",
                (f"大類資產 regime 綜合位置由 {prev_pos:.2f} 移至 {pos:.2f}"
                 f"（0-1 尺度，Δ{delta:+.2f}，門檻 0.15）"),
                "yellow", abs(delta) * 10.0,
                f"regime 快照 {snap.get('generated_at', '')[:10]}→{gen[:10]}"))
    for k, a in axes.items():
        old_pill = (snap.get("axes") or {}).get(k)
        if old_pill is not None and old_pill != a["pill"]:
            out.append(_sig(
                f"regime:axis:{k}", "regime", "axis", f"regime 軸：{a['name']}",
                f"regime「{a['name']}」軸讀值由「{old_pill}」變為「{a['pill']}」",
                "yellow", 2.0,
                f"regime 快照 {snap.get('generated_at', '')[:10]}→{gen[:10]}"))
    return out, new_snap


# ── 源 6：macro_clock（月頻、事件型）─────────────────────────────────────

def macro_clock_signals(clock, snap):
    """回傳 (signals, new_snap)。象限遷移→黃；遷入滯脹→紅（fact 附歷史條件
    事實，不加判斷）。首次僅 seed。"""
    if not clock:
        return [], snap
    asof = clock.get("as_of", "")
    q = clock.get("quadrant", "")
    new_snap = {"as_of": asof, "quadrant": q}
    if not snap or snap.get("as_of") == asof:
        return [], (snap or new_snap)
    out = []
    prev_q = snap.get("quadrant")
    if q and prev_q and q != prev_q:
        sev = "red" if q == "滯脹" else "yellow"
        fact = (f"總經時鐘象限由「{prev_q}」移至「{q}」"
                f"（{snap.get('as_of')}→{asof}，z6 等權 G／I 動能）")
        if sev == "red":
            qa = clock.get("quadrant_asset", "")
            if qa:
                fact += f"；本期象限的歷史條件資產對應欄為「{qa}」（歷史統計，非預測）"
        out.append(_sig("macro_clock:quadrant", "macro_clock", "clock",
                        "總經時鐘象限", fact, sev,
                        3.0 if sev == "red" else 2.0, f"clock as-of {asof}"))
    return out, new_snap


# ── 源 7：variance（週更：逐 ticker 紅旗持續型＋fleet 叢集事件型）─────────

def variance_signals(var, snap):
    """回傳 (signals, new_snap)。
    逐 ticker：drift_pct < −15 且非白旗（currency_suspect＝幣別待確認，永不出
    訊號）→ 黃，持續型（每 tick 依現檔重評）。
    fleet：generated_at 變新時，對 snapshot 的紅旗名單比差，新增 ≥3 檔 → 紅
    （事件型，一次性）。"""
    if not var:
        return [], snap
    gen = var.get("generated_at", "")
    best = {}
    for r in var.get("rows", []):
        t, d = r.get("ticker"), r.get("drift_pct")
        if not t or d is None:
            continue
        if t not in best or d < best[t].get("drift_pct", 0):
            best[t] = r
    red = sorted(t for t, r in best.items()
                 if r["drift_pct"] < VARIANCE_DRIFT_RED
                 and not r.get("currency_suspect"))
    out = []
    for t in red:
        r = best[t]
        out.append(_sig(
            f"variance:ticker:{t}", "variance", "ticker", f"{t} 財測落差",
            (f"{t} {r.get('fy_label', '')} 共識 EPS 較 DD 基準漂移 "
             f"{r['drift_pct']:.1f}%（紅旗門檻 −15%）"),
            "yellow", (abs(r["drift_pct"]) - 15.0) / 5.0,
            f"variance {gen[:10]}"))
    if snap and snap.get("generated_at") == gen:
        return out, snap  # generated_at 未變：沿用舊 snapshot（含舊紅旗名單）
    if snap:
        fresh = sorted(set(red) - set(snap.get("redflag_tickers", [])))
        if len(fresh) >= VARIANCE_FLEET_MIN:
            out.append(_sig(
                "variance:fleet:redflags", "variance", "fleet",
                "財測落差紅旗叢集",
                (f"本期新增財測落差紅旗 {len(fresh)} 檔"
                 f"（{'、'.join(fresh)}），單期新增達 {VARIANCE_FLEET_MIN} 檔門檻"),
                "red", float(len(fresh)), f"variance {gen[:10]}"))
    return out, {"generated_at": gen, "redflag_tickers": red}


# ── 源 8：kill（ID／macro kill_metrics 機械對帳；Phase 6）─────────────────

def kill_signals(kw):
    """kill_watch.json 的 breached 條目 → 紅燈，鍵 kill:{doc_stem}:{idx}；
    near／green／unknown／stale_needs_reparse 皆不出訊號（只留頁面對帳表）。
    fact 附固定流程語式「建議 spawn industry-thesis-critic 複審該 thesis」——這是
    流程動作、非買賣指令，維持描述器紀律。缺檔（kw 空）→ 回空、源 stale 由 staleness 標。"""
    if not kw:
        return []
    by_id = {it.get("id"): it for it in kw.get("items", [])}
    kw_asof = kw.get("as_of", "")
    out = []
    for rid in kw.get("breached", []):
        it = by_id.get(rid)
        if not it:
            continue
        parts = rid.split(":")            # kind:stem:idx
        if len(parts) < 3:
            continue
        stem, idx = parts[1], parts[2]
        theme = it.get("theme", "")
        metric = it.get("metric_text", "")
        cur, op, val = it.get("current"), it.get("op", ""), it.get("value")
        unit, doc = it.get("unit", ""), it.get("doc", "")
        thr = f"{op} {_fmt(val) if isinstance(val, (int, float)) else val}"
        if unit:
            thr += f" {unit}"
        cur_s = _fmt(cur) if isinstance(cur, (int, float)) else str(cur)
        fact = (f"{theme}｜{metric} 已越線：現值 {cur_s} vs 閾值 {thr}（源 {stem}）。"
                f"建議 spawn industry-thesis-critic 複審該 thesis")
        mag = 3.0
        if isinstance(cur, (int, float)) and isinstance(val, (int, float)) and val != 0:
            mag = min(abs(cur - val) / abs(val) * 10.0, 5.0)
        out.append(_sig(
            f"kill:{stem}:{idx}", "kill", "kill_metric", f"{theme} kill 指標",
            fact, "red", mag, f"kill_watch {kw_asof}｜{doc}"))
    return out


# ── 源 9：sector（產業結構分歧：單日分歧＋叢集＋us_sectors 象限翻轉）────────

def _sector_universe(latest):
    """回傳 [(cat, item)] — monitor sectors 類全體 ＋ SECTOR_EXTRA（半導體 SOX
    代理）。呼叫端自行過濾 stale／缺 z。"""
    out = []
    for c in latest.get("categories", []):
        if c.get("key") != "sectors":
            continue
        for it in c.get("items", []):
            out.append(("sectors", it))
    for cat, key in SECTOR_EXTRA:
        it = _mon_series(latest, cat, key)
        if it is not None:
            out.append((cat, it))
    return out


def sector_signals(latest, radar):
    """回答「今天是誰在跌」：單一產業 z 極端而大盤持平（下跌／對稱向上分歧）、
    同日多產業下跌分歧叢集（≥2 黃／≥3 紅）、us_sectors 120d 象限翻轉。
    描述器：只陳述當日 z 對比事實，不判斷、不擇時。"""
    out = []
    sp = _mon_series(latest, "indices", "sp500")
    sp_z = sp.get("z") if sp and not sp.get("stale") else None
    down_hits = []          # 收集下跌分歧產業標籤（供叢集彙總）
    for cat, it in _sector_universe(latest):
        if it.get("stale"):
            continue
        z = it.get("z")
        if z is None:
            continue
        label = it.get("label", it.get("key", ""))
        key = it.get("key", "")
        ctx = f"當日 {it.get('chg', '')}".strip()
        if (z <= SECTOR_DIVERGE_Z and sp_z is not None
                and sp_z >= -SECTOR_MKT_FLAT_Z):
            # 規則 1（下跌分歧）：產業 z ≤ −2 且 S&P 500 z ≥ −1（大盤未同步走弱）
            down_hits.append(label)
            out.append(_sig(
                f"sector:diverge:{key}:down", "sector", "diverge", label,
                (f"{label} 單日 {z:+.1f}σ，同日 S&P 500 {sp_z:+.1f}σ"
                 f"——跌勢集中於單一產業"),
                "yellow", abs(z) - 2.0, ctx))
        elif (z >= SECTOR_UP_DIVERGE_Z and sp_z is not None
              and abs(sp_z) <= SECTOR_MKT_FLAT_Z):
            # 規則 1 對稱（向上分歧）：產業 z ≥ +2 且大盤平（描述過熱集中）
            out.append(_sig(
                f"sector:diverge:{key}:up", "sector", "diverge", label,
                (f"{label} 單日 {z:+.1f}σ，同日 S&P 500 {sp_z:+.1f}σ"
                 f"——漲勢集中於單一產業"),
                "yellow", z - 2.0, ctx))
    if len(down_hits) >= SECTOR_CLUSTER_MIN:
        # 規則 2：下跌分歧叢集（≥2 黃／≥3 紅）
        sev = "red" if len(down_hits) >= SECTOR_CLUSTER_RED else "yellow"
        out.append(_sig(
            "sector:cluster:down", "sector", "cluster", "產業分歧叢集",
            (f"{len(down_hits)} 個產業同日領跌而大盤持平"
             f"（{'、'.join(sorted(down_hits))}）——產業層壓力未反映於指數"),
            sev, float(len(down_hits))))
    # 規則 3：us_sectors 120d 象限翻轉（複用 cross_asset 偵測邏輯，換宇宙）
    out += _quadrant_signals(radar, "us_sectors", "sector", "rotation")
    return out


# ── staleness ──────────────────────────────────────────────────────────

def _month_end(ym):
    y, m = int(ym[:4]), int(ym[5:7])
    nxt = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
    return (nxt - timedelta(days=1)).isoformat()


def source_staleness(as_of, sources):
    """回傳 stale source 名單。>頻率×2（日曆天）或缺檔 → stale。"""
    stale = []
    ref = date.fromisoformat(as_of)
    for name, sdate in sources.items():
        thr = SOURCE_FRESH_DAYS[name]
        if not sdate:
            stale.append(name)
            continue
        d = sdate
        if name == "macro_clock" and len(sdate) == 7:  # YYYY-MM → 月底
            d = _month_end(sdate)
        try:
            age = (ref - date.fromisoformat(d[:10])).days
        except ValueError:
            stale.append(name)
            continue
        if age > thr:
            stale.append(name)
    return sorted(stale)


# ── 主流程 ─────────────────────────────────────────────────────────────

def collect_met(latest, alerts, crowd, radar, regime, clock, var, kw, snaps, as_of):
    """組本 tick 的 met 集合＋新 source_snapshots（僅真推進時由呼叫端寫回）。"""
    sigs = []
    sigs += monitor_signals(latest, alerts, as_of)
    sigs += reversal_signals(latest)
    sigs += crowding_signals(crowd)
    sigs += rotation_signals(radar)
    sigs += sector_signals(latest, radar)
    sigs += kill_signals(kw)
    rg, snap_regime = regime_signals(regime, snaps.get("regime"))
    mc, snap_clock = macro_clock_signals(clock, snaps.get("macro_clock"))
    va, snap_var = variance_signals(var, snaps.get("variance"))
    sigs += rg + mc + va
    met = {}
    for s in sigs:
        met[s["key"]] = {"sev": s["sev"], "score": s["score_base"],
                         "display": {k: s[k] for k in
                                     ("source", "cat", "label", "fact",
                                      "context", "score_base")}}
    new_snaps = dict(snaps)
    for name, sn in (("regime", snap_regime), ("macro_clock", snap_clock),
                     ("variance", snap_var)):
        if sn is not None:
            new_snaps[name] = sn
    return met, new_snaps


def render_signals(state):
    """由 state 導出 latest.json 的 signals[]（含 cooling 灰化條目）。"""
    esc_today = {t["key"] for t in state.get("transitions_today", [])
                 if t.get("to") == "escalated" and t.get("date") == state.get("as_of")}
    out = []
    for key, e in state.get("keys", {}).items():
        if key.startswith("composite:"):
            continue  # composite 鍵走狀態機做 lifecycle，但由 composites[] 呈現，不入 signals[]
        disp = e.get("display", {})
        members = e.get("composite_members", [])
        score = round(disp.get("score_base", 0.0)
                      + min(e.get("days_active", 0) * PERSIST_BONUS_PER_DAY,
                            PERSIST_BONUS_CAP)
                      + (COMPOSITE_BONUS if members else 0.0), 2)
        st = "escalated" if key in esc_today else e.get("state", "active")
        out.append({
            "key": key, "source": disp.get("source", key.split(":")[0]),
            "cat": disp.get("cat", ""), "label": disp.get("label", key),
            "fact": disp.get("fact", ""), "sev": e.get("sev", "yellow"),
            "score": score, "context": disp.get("context", ""),
            "state": st, "first_seen": e.get("first_seen"),
            "last_seen": e.get("last_seen"),
            "days_active": e.get("days_active", 0),
            "escalations": e.get("escalations", []),
            "composite_members": members,
            "muted_until": (e.get("notify") or {}).get("mute_until"),
        })
    out.sort(key=lambda s: (-s["score"], s["key"]))
    return out


# ── Phase 3：複合規則層（規則評估在 detective_rules，本處只做狀態機接線）──

def _prospective_streak(state, key):
    """預估本 tick advance 後該 composite 鍵的 met_streak（與 advance 結果一致），
    供升級 (c) 需在 advance 前先知道是否 fire。"""
    e = (state.get("keys") or {}).get(key)
    if e is None:
        return 1                        # absent／revive → 首日算 1
    if e.get("state") == "cooling":
        return 1                        # 寬限內重滿足 → 重置為 1
    return int(e.get("met_streak", 0)) + 1


def inject_composites(met, rule_evals, state):
    """把 base_met 的 active 規則以 composite:R{n} 鍵注入 met（進同一狀態機）；
    fire 紅級時對其 series 型成員對應的當日 primitive 鍵標 composite_red，觸發升級 (c)。"""
    for ev in rule_evals:
        if ev["status"] != "active" or not ev["base_met"]:
            continue
        ckey = f"composite:{ev['id']}"
        csev = ev["sev"]
        cscore = 10.0 if csev == "red" else 5.0
        met[ckey] = {
            "sev": csev, "score": cscore,
            "display": {"source": "composite", "cat": ev["id"],
                        "label": ev["name"], "fact": ev["narrative"],
                        "context": f"成員 {ev['met_count']}/{ev['min_true']} 成立",
                        "score_base": cscore}}
        fired = _prospective_streak(state, ckey) >= ev["confirm_days"]
        if fired and csev == "red":
            for pref in ev["monitor_prefixes"]:
                for mk in list(met):
                    if mk.startswith("composite:"):
                        continue
                    if mk == pref or mk.startswith(pref + ":"):
                        met[mk]["composite_red"] = True


def fill_composite_members(state, rule_evals):
    """post-advance：把當日 fire 紅級 composite 的 id 回填至其 primitive 成員鍵的
    composite_members（供 +1.0 加成與呈現）。空則移除欄位以維持零 churn。"""
    keys = state.get("keys", {})
    linkage = {k: [] for k in keys}
    for ev in rule_evals:
        if ev["status"] != "active" or not ev["base_met"] or ev["sev"] != "red":
            continue
        e = keys.get(f"composite:{ev['id']}")
        if not e or e.get("met_streak", 0) < ev["confirm_days"]:
            continue                     # 未 fire（confirm 未滿）
        for pref in ev["monitor_prefixes"]:
            for k in keys:
                if k.startswith("composite:"):
                    continue
                if k == pref or k.startswith(pref + ":"):
                    linkage[k].append(ev["id"])
    for k, e in keys.items():
        mem = sorted(set(linkage.get(k, [])))
        if mem:
            e["composite_members"] = mem
        else:
            e.pop("composite_members", None)


def build_composites_output(rule_evals, state, as_of):
    """由規則評估＋狀態機導出 latest.json 的 composites[]（每次 build 都重算）。"""
    log = state.get("as_of_log", [])
    keys = state.get("keys", {})
    out = []
    for ev in rule_evals:
        entry = keys.get(f"composite:{ev['id']}")
        fired, fired_since = False, None
        if ev["status"] == "active" and ev["base_met"] and entry:
            M, C = entry.get("met_streak", 0), ev["confirm_days"]
            if M >= C:
                fired = True
                idx = M - C + 1
                fired_since = (log[-idx] if 0 < idx <= len(log)
                               else entry.get("first_seen"))
        out.append({
            "id": ev["id"], "name": ev["name"], "status": ev["status"],
            "members": ev["members"], "met_count": ev["met_count"],
            "min_true": ev["min_true"], "fired": fired, "fired_since": fired_since,
            "sev": ev["sev"], "narrative": ev["narrative"]})
    return out


# ── 警戒度描述器（alert_level）─────────────────────────────────────────

def _alert_band(score):
    for hi, band, label in ALERT_BANDS:
        if score < hi:
            return band, label
    return "alert", "警戒"


def compute_alert_level(signals, composites, kw, as_of):
    """警戒度 0-100 描述器（環境溫度計，非擇時訊號、非決策閘）.

    把警報網當前狀態聚合成單一總覽數字，餵頁面半圓威脅指針。純機械、確定性、
    冪等（同 state／同 kw 重跑同分；signals 由 state 導出，故 replay 不變）。
    **是 describer 不是 signal**：不預測轉折時點、不給買賣指令、不改任何裁決；
    band_label 一律用環境溫度語言（平靜/留意/升溫/緊張/警戒），drivers 是事實
    陳述（「X 條紅燈」「N 項複合規則距觸發差 1 成員」）非建議。因此不登記
    rule_ledger（它不是 veto/gate/救援/hysteresis 這類判斷類閘）。

    公式（權重集中於模組頂部 ALERT_WEIGHTS，PREREG 凍結至 2026-10 校準）：
      score = clamp_0_100( Σ min(命中數 × pts, cap) )，各成分：
        · red_signal      紅燈 signal 數（重）
        · yellow_signal   黃燈 signal 數（輕，**硬封頂 18**——今日 26 條黃燈
                          也只計 18 分，多黃燈不得單獨把指針頂到緊張/警戒）
        · composite_red / composite_yellow  composite fired（重／中）
        · composite_near  near-fire＝met_count==min_true−1 且 active 未 fire（中）
        · kill_breached   kill 越線（很重）／ kill_near  接近閾值（輕）
        · escalated       今日升級狀態數 ／ sustained  紅燈 days_active≥5（持續）
    band 對映：calm 0-20 / watch 20-40 / warming 40-60 / tense 60-80 /
    alert 80-100（下界含、上界不含）。缺檔／缺欄的成分 fail-soft 給 0、不炸。

    校準錨（as_of 2026-07-14 真實資料：1 紅 26 黃、9 composite 全未 fire（R7
    near）、kill 0 breached 6 near）刻意落在 warming 中段（約 47 分）——這是
    「有東西在動但沒觸發」的典型日常態，指針該指中間而非警戒。
    """
    w = ALERT_WEIGHTS
    comps = {}                              # 成分名 -> (命中數, 加總分)

    def add(name, hits):
        pts = min(hits * w[name]["pts"], w[name]["cap"])
        comps[name] = (hits, round(pts, 2))
        return pts

    signals = signals or []
    n_red = sum(1 for s in signals if s.get("sev") == "red")
    n_yellow = sum(1 for s in signals if s.get("sev") != "red")
    n_esc = sum(1 for s in signals if s.get("state") == "escalated")
    n_sustained = sum(1 for s in signals if s.get("sev") == "red"
                      and (s.get("days_active") or 0) >= ALERT_SUSTAINED_DAYS)

    c_red = c_yellow = c_near = 0
    for c in (composites or []):
        if c.get("fired"):
            if c.get("sev") == "red":
                c_red += 1
            else:
                c_yellow += 1
        elif (c.get("status") == "active" and (c.get("min_true") or 0) >= 1
              and c.get("met_count", 0) == (c.get("min_true") or 0) - 1):
            c_near += 1

    kw = kw or {}
    n_kill_breached = len(kw.get("breached") or [])
    n_kill_near = len(kw.get("near") or [])

    score = 0.0
    score += add("red_signal", n_red)
    score += add("yellow_signal", n_yellow)
    score += add("composite_red", c_red)
    score += add("composite_yellow", c_yellow)
    score += add("composite_near", c_near)
    score += add("kill_breached", n_kill_breached)
    score += add("kill_near", n_kill_near)
    score += add("escalated", n_esc)
    score += add("sustained", n_sustained)
    score_i = max(0, min(100, int(round(score))))

    band, label = _alert_band(score_i)

    drivers = [{"label": ALERT_DRIVER_LABELS[name](hits), "points": int(round(pts))}
               for name, (hits, pts) in comps.items() if hits > 0 and pts > 0]
    drivers.sort(key=lambda d: (-d["points"], d["label"]))

    return {"score": score_i, "band": band, "band_label": label,
            "drivers": drivers[:5], "as_of": as_of}


def main():
    latest = _load("monitor/data/latest.json", {})
    alerts = _load("monitor/data/alerts.json", {})
    internals = _load("monitor/data/internals.json", {})
    crowd = _load("crowding/data/latest.json", {})
    radar = _load("rotation/data/radar.json", {})
    regime = _load("regime/data/latest.json", {})
    clock = _load("macro/data/clock.json", {})
    var = _load("catalyst/variance.json", {})
    kw = _load("detective/data/kill_watch.json", {})

    state_path = os.path.join(DOCS, "detective", "data", "state.json")
    state = load_json(state_path)
    if not state or state.get("schema") != dstate.STATE_SCHEMA:
        state = dstate.empty_state()

    # tick 時鐘＝monitor as_of（日更主時鐘；fallback radar → 前次 state）
    as_of = latest.get("as_of") or radar.get("as_of") or state.get("as_of")
    if not as_of:
        print("detective: no dated source available and no prior state — abort")
        return

    # 複合規則評估：純函數、確定性，tick／replay 皆算（供 composites[] 呈現）
    rule_sources = {"monitor": latest, "crowding": crowd,
                    "rotation": radar, "macro_clock": clock,
                    "internals": internals}
    rule_evals = drules.evaluate_rules(rule_sources)

    is_tick = as_of > (state.get("as_of") or "")
    if is_tick:
        snaps = state.get("source_snapshots", {})
        met, new_snaps = collect_met(latest, alerts, crowd, radar,
                                     regime, clock, var, kw, snaps, as_of)
        inject_composites(met, rule_evals, state)  # composite 鍵入狀態機＋升級 (c) 標記
        state = dstate.advance(state, met, as_of)
        state["source_snapshots"] = new_snaps  # 只在真推進時更新（replay 守則）
        fill_composite_members(state, rule_evals)  # 回填 primitive 成員 → +1.0 加成
    # replay（as_of 未推進）：state 與 source_snapshots 原樣沿用 → 冪等

    composites_out = build_composites_output(rule_evals, state, as_of)

    signals = render_signals(state)
    sev_red = [s for s in signals if s["sev"] == "red"]
    by_state = {"new": 0, "active": 0, "escalated": 0, "cooling": 0}
    for s in signals:
        by_state[s["state"]] = by_state.get(s["state"], 0) + 1

    sources = {
        "monitor": latest.get("as_of"),
        "crowding": crowd.get("cot_as_of"),
        "rotation": radar.get("as_of"),
        "regime": (regime.get("generated_at") or "")[:10] or None,
        "macro_clock": clock.get("as_of"),
        "variance": (var.get("generated_at") or "")[:10] or None,
        "kill": kw.get("as_of"),
        "sector": latest.get("as_of"),   # as_of＝monitor as_of
    }
    stale = source_staleness(as_of, sources)
    gen = radar.get("generated_at") or latest.get("generated_at")

    alert_level = compute_alert_level(signals, composites_out, kw, as_of)

    out = {
        "schema": "detective-v2",
        "as_of": as_of,
        "generated_at": gen,
        "alert_level": alert_level,
        "counts": {"total": len(signals), "red": len(sev_red),
                   "yellow": len(signals) - len(sev_red),
                   "new": by_state["new"], "active": by_state["active"],
                   "escalated": by_state["escalated"],
                   "cooling": by_state["cooling"]},
        "signals": signals,
        "composites": composites_out,
        "sources": sources,
        "sources_stale": stale,
        # v1 鏡射欄位（現頁 as-of 列相容，附加不移除）
        "monitor_as_of": sources["monitor"],
        "crowding_as_of": sources["crowding"],
        "radar_as_of": sources["rotation"],
    }

    latest_path = os.path.join(DOCS, "detective", "data", "latest.json")
    ch_latest = write_json_if_changed(latest_path, out)

    # ── alert digest：紅燈＋今日新增（state==new）＋今日升級，扣除 mute ──
    alert_items, notified = [], []
    for s in signals:
        is_new = s["state"] == "new"
        is_esc = s["state"] == "escalated"
        if not (s["sev"] == "red" or is_new or is_esc):
            continue
        mu = s.get("muted_until")
        if mu and mu >= as_of:
            continue        # mute 只擋即時信；訊號仍在 latest.json 日摘
        tag = "🔴" if s["sev"] == "red" else ("⤴" if is_esc else "🆕")
        line = f"{tag} {s['fact']}"
        if s["context"]:
            line += f"（{s['context']}）"
        alert_items.append((s["score"], line))
        notified.append(s["key"])
    alert_items.sort(key=lambda x: -x[0])

    if is_tick and notified:
        for k in notified:          # notify 帳：Phase 4 消費
            if k in state["keys"]:
                state["keys"][k]["notify"]["last_immediate"] = as_of
    state["generated_at"] = gen
    ch_state = write_json_if_changed(state_path, state)

    alert_file = os.path.join(ROOT, "detective_alert.txt")
    if alert_items:
        lines = [f"市場偵探 — {as_of}",
                 (f"紅燈 {len(sev_red)}、今日新增 {by_state['new']}、"
                  f"今日升級 {by_state['escalated']}、"
                  f"冷卻 {by_state['cooling']}、總訊號 {len(signals)}"), ""]
        lines += [ln for _, ln in alert_items]
        lines += ["", "— 描述器：只陳述事實，非擇時訊號。",
                  "詳見 https://research.investmquest.com/detective/"]
        with open(alert_file, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"detective: {len(signals)} signals ({by_state}), {len(sev_red)} red "
              f"— alert digest written ({len(alert_items)} items)")
    else:
        if os.path.exists(alert_file):
            os.remove(alert_file)
        print(f"detective: {len(signals)} signals ({by_state}), "
              f"{len(sev_red)} red — no alert")
    print(f"detective as_of={as_of} tick={'yes' if is_tick else 'no (replay)'} "
          f"stale={stale or '[]'}")
    print(f"latest.json: {'written' if ch_latest else 'zero-churn'} · "
          f"state.json: {'written' if ch_state else 'zero-churn'}")


if __name__ == "__main__":
    main()
