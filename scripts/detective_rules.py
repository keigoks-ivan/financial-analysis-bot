#!/usr/bin/env python3
"""detective_rules.py — 市場偵探 v2 Phase 3 複合規則引擎（宣告式規則表＋評估器）.

被 build_detective.py 呼叫；本模組不讀寫任何檔案、不推進狀態機，只吃「已載入
的資料源字典」，把跨指標聯合條件（R1–R9）逐條評估，吐出每條規則的成員現值快照
＋是否滿足 min_true。confirm_days（連續 N 個資料日才 fire）與 fire／cooling 生命
週期由 build_detective 端把 `composite:R{n}` 鍵餵進 detective_state 狀態機處理，
本模組只負責「當日這條規則的成員條件是否成立」的純判定。

── 成員條件兩型 ──────────────────────────────────────────────
series  型：直讀資料層某序列的某欄位並比較。
  {"src":"monitor","key":"sp500","field":"pctile","op":">=","value":90,
   "desc":"…", ["transform":"abs"], ["and":[{"field":"dir","op":"==","value":"pos"}]]}
  · src 註冊表：monitor（monitor latest.json series）、macro_clock（clock.json
    quadrant）、crowding_cot（crowding latest.json cot 某市場 pctile_5y 等欄）。
  · 可選 transform="abs"（先取絕對值再比，供 |z|<1 型條件）。
  · 可選 and[]：同序列的追加條件，全數成立成員才算 met（供「z≥1.5 且 dir 漲」）。
subgroup 型：同一組序列的 k-of-n 子額。
  {"type":"subgroup","min":2,"conds":[{series 條件},…],"desc":"…"}
  · ≥min 個子條件成立→成員 met（供 R7「三取二 分位≤20」）。
signal   型：當日 primitive 訊號集是否存在符合條件者（跨源 join）。
  {"type":"signal","selector":"cot_extreme","params":{"pctile_min":90},"desc":"…"}
  · selector 註冊在 _SELECTORS；供 R6 擁擠×動能翻轉的 COT↔rotation join。

── 逼近度機器欄（proximity machine columns，重構輪新增）──────────────
每個成員在評估結果附純渲染層機器欄，供前端靶盤呈現「還差多少才觸發」：
  current_num／threshold_num／op／scale（pctile｜z｜val｜cat｜subgroup｜event）／
  distance（正=未達、0=已達，clamp≥0）／distance_label（人話）／ref（該成員對應
  primitive 訊號鍵前綴 {source}:{cat}:{key}，供前端點規則高亮熱力牆格子）。
規則層附 proximity（0-1 排序鍵，公式見 _rule_proximity docstring）——非判斷閘、
不推狀態機、不登 rule_ledger；純機械確定性，replay 冪等。

── 規則欄位 ──────────────────────────────────────────────────
id/name/members[]/min_true/fire_sev/confirm_days/narrative/kill_condition/status。
fire_sev：字串 "red"/"yellow"，或分級 dict {"yellow":2,"red":3}（供 R2 2/3 黃 3/3 紅）。
status：active｜dormant。dormant 規則永不評估（成員序列尚未上線，如 R9 internals）。

── dormant 防呆 ──────────────────────────────────────────────
任一成員的底層序列在資料層缺席（key 不存在或 stale）或其源資料整包缺席 →
該規則當日 status:"dormant"、不評估、不報錯（頁面灰顯）。

描述器紀律：narrative 只陳述「組合狀態同現」的事實與構成，禁擇時／買賣語，全形標點。
"""
import re

# ── COT 市場 ↔ rotation cross_asset ticker 對映（R6 join；對不上的市場不評估）──
COT_ROTATION_MAP = {
    "S&P 500 E-mini": "SPY",
    "Gold": "GLD",
    "US Dollar Index (DX)": "UUP",
    "US Treasury 10Y": "TLT",
    "US Treasury Bonds (30Y)": "TLT",
}


# ── 數值解析與比較 ─────────────────────────────────────────────

def _num(v):
    """把 monitor val 字串（'$774B'／'-5bps'／'2.36%'／'7,543.59'）抽成 float。"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"-?\d[\d,]*\.?\d*", str(v))
    if not m:
        return None
    try:
        return float(m.group().replace(",", ""))
    except ValueError:
        return None


def _cmp(a, op, b):
    if a is None:
        return False
    if op == ">=":
        return a >= b
    if op == "<=":
        return a <= b
    if op == ">":
        return a > b
    if op == "<":
        return a < b
    if op == "==":
        return a == b
    if op == "in":
        return a in b
    raise ValueError(f"unknown op {op}")


# ── 資料源存取（accessor 註冊表）──────────────────────────────

def _mon_item(monitor, key):
    """monitor latest.json 全類掃描找 series；回傳 (item|None)。"""
    for c in (monitor or {}).get("categories", []):
        if str(c.get("key", "")).startswith("_"):
            continue
        for it in c.get("items", []):
            if it.get("key") == key:
                return it
    return None


def _mon_cat(monitor, key):
    for c in (monitor or {}).get("categories", []):
        for it in c.get("items", []):
            if it.get("key") == key:
                return c.get("key")
    return None


def _cot_market(crowd, name):
    for m in (crowd or {}).get("cot", []):
        if m.get("market") == name:
            return m
    return None


def _rotation_rsm(radar, ticker):
    """cross_asset 120 日框架該 ticker 最新 RS-M；無則 None。"""
    for u in (radar or {}).get("universes", []):
        if u.get("key") != "cross_asset":
            continue
        for mem in u.get("members", []):
            if mem.get("ticker") == ticker:
                fr = (mem.get("frames") or {}).get("120") or {}
                trail = fr.get("trail") or []
                if trail:
                    return trail[-1].get("m")
    return None


def _series_fetch(sources, src, key):
    """回傳 (ctx, available)。available=False → 成員不可評估（rule → dormant）。"""
    if src == "monitor":
        it = _mon_item(sources.get("monitor"), key)
        if it is None or it.get("stale"):
            return None, False
        return it, True
    if src == "internals":
        # internals.json 與 monitor latest.json 同 categories/items 結構
        it = _mon_item(sources.get("internals"), key)
        if it is None or it.get("stale"):
            return None, False
        return it, True
    if src == "macro_clock":
        clk = sources.get("macro_clock") or {}
        if not clk.get("quadrant"):
            return None, False
        return clk, True
    if src == "crowding_cot":
        m = _cot_market(sources.get("crowding"), key)
        return (m, m is not None)
    return None, False


def _field_value(ctx, src, field):
    if src in ("monitor", "internals"):
        if field == "val":
            return _num(ctx.get("val"))
        return ctx.get(field)
    if src == "macro_clock":
        return ctx.get(field)
    if src == "crowding_cot":
        return ctx.get(field)
    return None


def _fmt_field(src, field, raw):
    """成員現值的人類可讀字串（描述器：全形、只陳述值）。"""
    if raw is None:
        return "缺"
    if src in ("monitor", "internals"):
        if field == "pctile":
            return f"分位 {raw:.1f}"
        if field in ("p20", "p60"):
            return f"分位 {raw:.1f}"
        if field == "z":
            return f"z {raw:+.2f}"
        if field == "dir":
            return "走高" if raw == "pos" else "走低"
        if field == "val":
            return f"值 {raw:g}"
        if field == "streak":
            return f"連 {int(raw)} 日"
        return f"{field} {raw}"
    if src == "macro_clock":
        if field == "quadrant":
            return f"象限「{raw}」"
        return f"{field} {raw}"
    if src == "crowding_cot":
        if field == "pctile_5y":
            return f"5 年分位 {raw:.1f}"
        return f"{field} {raw}"
    return f"{field} {raw}"


# ── 成員評估 ───────────────────────────────────────────────────

def _eval_conds(ctx, src, conds):
    """一組同序列條件（primary＋and[]），全數成立才 met；回傳 (met, 現值字串)。"""
    met = True
    parts = []
    first = True
    for c in conds:
        raw = _field_value(ctx, src, c["field"])
        val = raw
        if c.get("transform") == "abs" and isinstance(val, (int, float)):
            val = abs(val)
        met = met and _cmp(val, c["op"], c["value"])
        if first:
            parts.append(_fmt_field(src, c["field"], raw))
            first = False
        elif c["field"] == "dir":
            parts.append("走高" if raw == "pos" else "走低")
    return met, "、".join(parts)


# ── 逼近度機器欄（proximity）─────────────────────────────────────
# scale：pctile｜z｜val（數值型，各有正規化分母）；cat（類別型 dir／quadrant，
# 無數值距離）；subgroup（k-of-n 計數）；event（signal 型，事件觸發）。
_SCALE_BY_FIELD = {"pctile": "pctile", "p20": "pctile", "p60": "pctile",
                   "z": "z", "val": "val"}
# closeness 正規化分母（把 distance 換成 0-1 接近度）；val 無穩定尺度→退化處理。
_SCALE_DENOM = {"pctile": 100.0, "z": 4.0}
# signal 型 selector → primitive 源前綴（前端高亮用）。
_SELECTOR_REF = {"cot_extreme": "crowding:cot",
                 "cot_rotation_weak_join": "rotation:quadrant"}


def _member_ref(sources, src, key):
    """成員對應 primitive 訊號鍵前綴 {source}:{cat}:{key}（前端點規則高亮格子）。"""
    if src == "monitor":
        return f"monitor:{_mon_cat(sources.get('monitor'), key) or '?'}:{key}"
    if src == "internals":
        return f"internals:{_mon_cat(sources.get('internals'), key) or '?'}:{key}"
    if src == "macro_clock":
        return "macro_clock:clock:quadrant"
    if src == "crowding_cot":
        return "crowding:cot"
    return f"{src}:{key}"


def _signed_distance(op, cur, thr):
    """還差多少才達標（正=未達、負=已達超過）；op／值非數值→None。"""
    if cur is None or thr is None:
        return None
    if op in (">=", ">"):
        return thr - cur
    if op in ("<=", "<"):
        return cur - thr
    if op == "==":
        return abs(cur - thr)
    return None


def _distance_label(scale, d):
    if d is None:
        return None
    if d <= 0:
        return "已達標"
    if scale == "pctile":
        return f"差 {d:.1f} 分位點"
    if scale == "z":
        return f"差 {d:.1f}σ"
    return f"差 {d:.2f}"


def _closeness(scale, d, met):
    """0-1 接近度（1=已達／最近，0=最遠）；未達時 1−clamp(distance/denom)。"""
    if met:
        return 1.0
    if d is None or d <= 0:
        return 1.0 if d is not None else 0.0    # 類別未達→0；數值已達→1
    denom = _SCALE_DENOM.get(scale) or max(1.0, abs(d))  # val：無穩定尺度→粗略歸一
    return round(max(0.0, min(1.0, 1.0 - d / denom)), 4)


def _series_prox(sources, mem, ctx, met, avail):
    field, op = mem["field"], mem["op"]
    scale = _SCALE_BY_FIELD.get(field, "cat")
    thr = mem.get("value")
    ref = _member_ref(sources, mem["src"], mem["key"])
    thr_num = thr if isinstance(thr, (int, float)) else None
    if not avail or scale == "cat":
        return {"scale": scale, "op": op, "current_num": None,
                "threshold_num": thr_num, "distance": None,
                "distance_label": ("缺席" if not avail else
                                   ("已達標" if met else "未達標")),
                "ref": ref, "_closeness": (0.0 if not avail else
                                           (1.0 if met else 0.0))}
    raw = _field_value(ctx, mem["src"], field)
    cur = abs(raw) if mem.get("transform") == "abs" and isinstance(raw, (int, float)) else raw
    cur = cur if isinstance(cur, (int, float)) else None
    d = _signed_distance(op, cur, thr_num)
    return {"scale": scale, "op": op,
            "current_num": None if cur is None else round(cur, 2),
            "threshold_num": thr_num,
            "distance": None if d is None else round(max(d, 0.0), 2),
            "distance_label": _distance_label(scale, d),
            "ref": ref, "_closeness": _closeness(scale, d, met)}


def _cond_closeness(ctx, c, met):
    scale = _SCALE_BY_FIELD.get(c["field"], "cat")
    raw = _field_value(ctx, c["src"], c["field"])
    cur = abs(raw) if c.get("transform") == "abs" and isinstance(raw, (int, float)) else raw
    cur = cur if isinstance(cur, (int, float)) else None
    thr = c["value"] if isinstance(c["value"], (int, float)) else None
    return _closeness(scale, _signed_distance(c["op"], cur, thr), met)


def _subgroup_prox(sources, mem, sub_met, avail, sub_cl):
    need, n = mem["min"], len(mem["conds"])
    met = avail and sub_met >= need
    ref = _member_ref(sources, mem["conds"][0]["src"], mem["conds"][0]["key"])
    if not avail:
        cl = 0.0
    elif met:
        cl = 1.0
    else:
        best = max((c for m, c in sub_cl if not m), default=0.0)
        cl = round(max(0.0, min(1.0, (sub_met + best) / need)), 4)
    return {"scale": "subgroup", "op": ">=",
            "current_num": None if not avail else sub_met, "threshold_num": need,
            "distance": None if (not avail or met) else float(need - sub_met),
            "distance_label": ("缺席" if not avail else
                               ("已達標" if met else f"差 {need - sub_met} 個子條件")),
            "ref": ref, "_closeness": cl}


def _signal_prox(mem, met):
    return {"scale": "event", "op": None, "current_num": None,
            "threshold_num": None, "distance": None, "distance_label": "事件型",
            "ref": _SELECTOR_REF.get(mem["selector"], ""),
            "_closeness": (1.0 if met else 0.0)}


# ── 成員評估（附逼近度機器欄）─────────────────────────────────────

def _eval_series_member(sources, mem):
    src, key = mem["src"], mem["key"]
    ctx, avail = _series_fetch(sources, src, key)
    if not avail:
        return {"met": False, "current": "缺席", "available": False,
                "prox": _series_prox(sources, mem, None, False, False)}
    conds = [{"field": mem["field"], "op": mem["op"], "value": mem["value"],
              "transform": mem.get("transform")}] + list(mem.get("and", []))
    met, cur = _eval_conds(ctx, src, conds)
    return {"met": met, "current": cur, "available": True,
            "prox": _series_prox(sources, mem, ctx, met, True)}


def _eval_subgroup_member(sources, mem):
    sub_met, parts, avail, sub_cl = 0, [], True, []
    for c in mem["conds"]:
        ctx, ok = _series_fetch(sources, c["src"], c["key"])
        if not ok:
            avail = False
            parts.append(f"{c['key']} 缺席")
            sub_cl.append((False, 0.0))
            continue
        m, cur = _eval_conds(ctx, c["src"], [c])
        sub_met += 1 if m else 0
        parts.append(f"{c['key']} {cur}{'✓' if m else '✗'}")
        sub_cl.append((m, _cond_closeness(ctx, c, m)))
    prox = _subgroup_prox(sources, mem, sub_met, avail, sub_cl)
    if not avail:
        return {"met": False, "current": "、".join(parts), "available": False,
                "prox": prox}
    met = sub_met >= mem["min"]
    return {"met": met, "current": f"{'、'.join(parts)} → {sub_met}/{len(mem['conds'])}",
            "available": True, "prox": prox}


# ── signal 型 selector 註冊表（R6 join）─────────────────────────

def _cot_crowded_markets(sources, pctile_min):
    crowd = sources.get("crowding") or {}
    return [m for m in crowd.get("cot", [])
            if m.get("pctile_5y") is not None
            and m["pctile_5y"] >= pctile_min
            and m.get("market") in COT_ROTATION_MAP]


def _sel_cot_extreme(sources, params):
    crowd = sources.get("crowding") or {}
    if not crowd.get("cot"):
        return {"met": False, "current": "缺席", "available": False}
    hit = _cot_crowded_markets(sources, params["pctile_min"])
    names = "、".join(f"{m['market']}（5 年分位 {m['pctile_5y']:.1f}）" for m in hit)
    return {"met": bool(hit), "current": names or "無符合", "available": True}


def _sel_cot_rotation_weak_join(sources, params):
    crowd = sources.get("crowding") or {}
    radar = sources.get("rotation") or {}
    if not crowd.get("cot") or not radar.get("universes"):
        return {"met": False, "current": "缺席", "available": False}
    weak = []
    for m in _cot_crowded_markets(sources, params["pctile_min"]):
        tk = COT_ROTATION_MAP[m["market"]]
        rsm = _rotation_rsm(radar, tk)
        if rsm is not None and rsm < 100:
            weak.append(f"{m['market']}→{tk}（RS-M {rsm:.2f}）")
    return {"met": bool(weak), "current": "、".join(weak) or "無轉弱", "available": True}


_SELECTORS = {
    "cot_extreme": _sel_cot_extreme,
    "cot_rotation_weak_join": _sel_cot_rotation_weak_join,
}


def _eval_signal_member(sources, mem):
    fn = _SELECTORS[mem["selector"]]
    r = fn(sources, mem.get("params", {}))
    r["prox"] = _signal_prox(mem, r["met"])
    return r


# 成員輸出機器欄（供 composites[] 直接渲染；_closeness 為內部排序用，不輸出）。
MEMBER_PUBLIC = ("desc", "current", "met", "current_num", "threshold_num",
                 "op", "scale", "distance", "distance_label", "ref")


def _eval_member(sources, mem):
    t = mem.get("type", "series")
    if t == "series":
        r = _eval_series_member(sources, mem)
    elif t == "subgroup":
        r = _eval_subgroup_member(sources, mem)
    elif t == "signal":
        r = _eval_signal_member(sources, mem)
    else:
        raise ValueError(f"unknown member type {t}")
    prox = r["prox"]
    out = {"desc": mem["desc"], "current": r["current"], "met": r["met"],
           "_available": r["available"], "_closeness": prox["_closeness"]}
    out.update({k: prox[k] for k in prox if k != "_closeness"})
    return out


# ── sev 分級 ───────────────────────────────────────────────────

def _compute_sev(fire_sev, met_count, min_true, n_members):
    if isinstance(fire_sev, dict):
        if met_count >= fire_sev.get("red", n_members):
            return "red"
        if met_count >= fire_sev.get("yellow", min_true):
            return "yellow"
        return None
    return fire_sev


# ── 供 build 端：規則的 monitor primitive key 前綴（升級 (c)／成員回填用）──

def rule_monitor_prefixes(rule, monitor):
    """回傳該規則所有 series/subgroup monitor 成員對應的 primitive 鍵前綴
    （形如 'monitor:{cat}:{key}'）。build_detective 端據此把當日 primitive 訊號
    標 composite_red 並回填 composite_members。"""
    out = []

    def _add(src, key):
        if src != "monitor":
            return
        cat = _mon_cat(monitor, key)
        if cat:
            out.append(f"monitor:{cat}:{key}")

    for mem in rule["members"]:
        t = mem.get("type", "series")
        if t == "series":
            _add(mem["src"], mem["key"])
        elif t == "subgroup":
            for c in mem["conds"]:
                _add(c["src"], c["key"])
    return out


# ── 規則評估 ───────────────────────────────────────────────────

def _rule_proximity(ev, met_count, min_true):
    """規則逼近度 0-1（排序鍵，非判斷閘、不登 rule_ledger）.

    proximity = met_fraction*0.7 + nearest_unmet_closeness*0.3
      · met_fraction＝min(1, met_count/min_true)（朝觸發門檻的進度）。
      · nearest_unmet_closeness＝未達成員中最接近者的正規化接近度（0-1；pctile
        距離 /100、z 距離 /4，clamp 0-1）；全達（met_count≥min_true）時取 1.0。
    dormant 由呼叫端給 0；fired（confirm_days 滿）由 build 端覆寫為 1.0。"""
    met_fraction = min(1.0, met_count / min_true) if min_true else 0.0
    unmet = [m["_closeness"] for m in ev if not m["met"]]
    nearest = max(unmet) if unmet else 1.0
    return round(met_fraction * 0.7 + nearest * 0.3, 4)


def _pub_members(ev):
    """把 _eval_member 結果收斂為輸出用成員（含逼近度機器欄，去內部欄）。"""
    return [{k: m.get(k) for k in MEMBER_PUBLIC} for m in ev]


def evaluate_rule(sources, rule):
    """評估單一規則；回傳含成員快照的 dict（不含 fired／fired_since，那需狀態機）。"""
    n = len(rule["members"])
    base = {"id": rule["id"], "name": rule["name"], "min_true": rule["min_true"],
            "confirm_days": rule["confirm_days"], "fire_sev": rule["fire_sev"],
            "narrative": rule["narrative"]}
    if rule.get("status") == "dormant":
        members = [{"desc": m["desc"], "current": "—（未上線）", "met": False,
                    "current_num": None, "threshold_num": None, "op": None,
                    "scale": None, "distance": None, "distance_label": "未上線",
                    "ref": None} for m in rule["members"]]
        return {**base, "status": "dormant", "members": members,
                "met_count": 0, "base_met": False, "sev": None,
                "proximity": 0.0, "monitor_prefixes": []}
    ev = [_eval_member(sources, m) for m in rule["members"]]
    if any(not m["_available"] for m in ev):
        return {**base, "status": "dormant", "members": _pub_members(ev),
                "met_count": 0, "base_met": False, "sev": None,
                "proximity": 0.0, "monitor_prefixes": []}
    met_count = sum(1 for m in ev if m["met"])
    base_met = met_count >= rule["min_true"]
    sev = _compute_sev(rule["fire_sev"], met_count, rule["min_true"], n) if base_met else None
    return {**base, "status": "active", "members": _pub_members(ev),
            "met_count": met_count, "base_met": base_met, "sev": sev,
            "proximity": _rule_proximity(ev, met_count, rule["min_true"]),
            "monitor_prefixes": rule_monitor_prefixes(rule, sources.get("monitor"))}


def evaluate_rules(sources):
    """評估全部規則（含 dormant）；回傳 list（順序同 RULES）。"""
    return [evaluate_rule(sources, r) for r in RULES]


# ── 規則表 R1–R9 ───────────────────────────────────────────────

def _mon(key, field, op, value, desc, **extra):
    d = {"src": "monitor", "key": key, "field": field, "op": op,
         "value": value, "desc": desc}
    d.update(extra)
    return d


def _intl(key, field, op, value, desc, **extra):
    """internals.json 序列成員（結構同 monitor，src=internals）。"""
    d = {"src": "internals", "key": key, "field": field, "op": op,
         "value": value, "desc": desc}
    d.update(extra)
    return d


RULES = [
    {
        "id": "R1", "name": "股高位×信用背離×廣度走弱", "status": "active",
        "members": [
            _mon("sp500", "pctile", ">=", 90, "S&P 500 一年分位 ≥90（指數高位）"),
            _mon("hyg_lqd", "pctile", "<=", 25, "高收益／投資級相對比 分位 ≤25（信用相對走弱）"),
            _mon("rsp_spy", "pctile", "<=", 25, "等權／市值 S&P 相對比 分位 ≤25（廣度走弱）"),
        ],
        "min_true": 3, "fire_sev": "red", "confirm_days": 2,
        "narrative": ("指數位於一年高位、同時高收益相對投資級走弱且等權相對市值落後，"
                      "三者同現描述『指數在高位但由少數大型股撐盤、信用與廣度未同步確認』"
                      "的內部結構狀態。"),
        "kill_condition": ("fire 後 20 交易日對應資產回撤中位不劣於未 fire 基準，"
                           "連兩輪審計 → 刪或降黃"),
    },
    {
        "id": "R2", "name": "波動結構三件套", "status": "active",
        "members": [
            _mon("vix_ts", "pctile", ">=", 90, "VIX 期限結構比 一年分位 ≥90"),
            _mon("skew", "pctile", ">=", 90, "SKEW 偏斜 一年分位 ≥90"),
            _mon("vvix", "z", ">=", 2, "VVIX 波動的波動 z ≥2"),
        ],
        "min_true": 2, "fire_sev": {"yellow": 2, "red": 3}, "confirm_days": 1,
        "narrative": ("VIX 期限結構、偏斜與波動的波動三項分位同處高位，描述選擇權市場"
                      "對尾部與波動加速的定價同時偏貴的組合狀態；三取二為黃、三項齊發為紅。"),
        "kill_condition": ("fire 後 20 交易日對應資產回撤中位不劣於未 fire 基準，"
                           "連兩輪審計 → 刪或降黃"),
    },
    {
        "id": "R3", "name": "流動性三管收縮", "status": "active",
        "members": [
            _mon("reserves", "z", "<=", -2, "銀行準備金 z ≤−2（準備金收縮）"),
            _mon("tga", "z", ">=", 2, "財政部一般帳戶 z ≥2（TGA 回補抽水）"),
            _mon("sofr_iorb", "val", ">", 0, "SOFR 對 IORB 利差 >0（擔保隔夜利率相對準備金利率轉正）"),
        ],
        "min_true": 3, "fire_sev": "yellow", "confirm_days": 1,
        "narrative": ("準備金收縮、財政部一般帳戶回補、SOFR 對 IORB 轉正三者同現，"
                      "描述銀行體系準備金邊際趨緊的組合狀態；連續滿足經狀態機 sustained "
                      "路徑升級。"),
        "kill_condition": "fire 與後續 NFCI 走向無相關，連兩輪 → 刪",
    },
    {
        "id": "R4", "name": "信用內部裂縫", "status": "active",
        "members": [
            _mon("ccc_oas", "z", ">=", 2, "CCC 利差 z ≥2（低評級端急擴）"),
            _mon("ig_oas", "z", "<", 1, "投資級利差 |z|<1（投資級按兵不動）", transform="abs"),
            _mon("hyg_lqd", "pctile", "<=", 20, "高收益／投資級相對比 分位 ≤20"),
        ],
        "min_true": 3, "fire_sev": "red", "confirm_days": 2,
        "narrative": ("CCC 利差急擴、投資級利差按兵不動、高收益相對投資級走弱三者同現，"
                      "描述信用壓力集中於低評級端而尚未擴散至投資級的內部裂縫狀態。"),
        "kill_condition": "fire 後 HY OAS 20 日續闊比率 <50%，連兩輪 → 降黃",
    },
    {
        "id": "R5", "name": "避險同框", "status": "active",
        "members": [
            _mon("gold", "z", ">=", 1.5, "黃金 z ≥1.5 且走高",
                 **{"and": [{"field": "dir", "op": "==", "value": "pos"}]}),
            _mon("dxy", "z", ">=", 1.5, "美元指數 z ≥1.5 且走高",
                 **{"and": [{"field": "dir", "op": "==", "value": "pos"}]}),
            _mon("real10y", "dir", "==", "neg", "實質 10Y 殖利率走低"),
        ],
        "min_true": 3, "fire_sev": "yellow", "confirm_days": 1,
        "narrative": ("黃金與美元同時走強、且實質 10Y 殖利率同日下行，描述跨資產同時"
                      "偏向避險的組合狀態。"),
        "kill_condition": "兩輪 0 fire 或與跨資產後續波動無關 → 刪",
    },
    {
        "id": "R6", "name": "擁擠×動能翻轉", "status": "active",
        "members": [
            {"type": "signal", "selector": "cot_extreme",
             "params": {"pctile_min": 90},
             "desc": "COT 投機部位 5 年分位 ≥90 的資產（且有輪動對映）"},
            {"type": "signal", "selector": "cot_rotation_weak_join",
             "params": {"pctile_min": 90},
             "desc": "該擁擠資產於資產輪動 120 日框架象限轉弱（RS-M<100）"},
        ],
        "min_true": 2, "fire_sev": "yellow", "confirm_days": 1,
        "narrative": ("投機部位五年分位極端擁擠的資產、其於資產輪動框架同時轉弱，"
                      "描述擁擠部位與價格動能背離的組合狀態。"),
        "kill_condition": "fire 資產 20 日回撤中位不劣於未 fire 極端 → 刪",
    },
    {
        "id": "R7", "name": "窄領導", "status": "active",
        "members": [
            _mon("sp500", "pctile", ">=", 90, "S&P 500 一年分位 ≥90（指數高位）"),
            {"type": "subgroup", "min": 2, "conds": [
                _mon("iwm_spy", "pctile", "<=", 20, "小型／大盤相對比 分位 ≤20"),
                _mon("kre_xlf", "pctile", "<=", 20, "區域銀行／金融相對比 分位 ≤20"),
                _mon("djt_dji", "pctile", "<=", 20, "運輸／道瓊相對比 分位 ≤20"),
            ], "desc": "小型股／區域銀行／運輸相對比 三取二 分位 ≤20"},
        ],
        "min_true": 2, "fire_sev": "yellow", "confirm_days": 2,
        "narrative": ("指數位於一年高位、同時小型股／區域銀行／運輸相對大盤多數走弱，"
                      "描述由少數權值撐盤的窄基礎領導狀態。"),
        "kill_condition": ("fire 後 20 交易日對應資產回撤中位不劣於未 fire 基準，"
                           "連兩輪審計 → 刪或降黃"),
    },
    {
        "id": "R8", "name": "晚週期滯脹組合", "status": "active",
        "members": [
            {"type": "series", "src": "macro_clock", "key": "quadrant",
             "field": "quadrant", "op": "in", "value": ["過熱", "滯脹"],
             "desc": "總經時鐘象限 ∈｛過熱、滯脹｝"},
            _mon("copper_gold", "pctile", "<=", 30, "銅金比 一年分位 ≤30（走弱）"),
            _mon("bei5y", "z", ">=", 1.5, "五年通膨預期 z ≥1.5（偏高）"),
        ],
        "min_true": 3, "fire_sev": "yellow", "confirm_days": 1,
        "narrative": ("總經時鐘位於過熱或滯脹象限、銅金比走弱且五年通膨預期偏高三者同現，"
                      "描述晚週期疊加通膨黏性的組合狀態。"),
        "kill_condition": "滯脹象限條件劣勢在時鐘審計消失 → 連動降級",
    },
    {
        "id": "R9", "name": "自滿組合", "status": "active",
        "members": [
            _intl("pc_equity", "pctile", "<=", 5, "股票 put／call 比 一年分位 ≤5（極度自滿）"),
            _mon("skew", "pctile", ">=", 90, "SKEW 偏斜 一年分位 ≥90"),
            _mon("vix", "pctile", "<=", 10, "VIX 一年分位 ≤10（波動極低）"),
        ],
        "min_true": 3, "fire_sev": "yellow", "confirm_days": 1,
        "narrative": ("股票 put／call 比處一年極低分位、SKEW 偏斜偏高、VIX 一年分位極低"
                      "三者同現，描述選擇權與波動面同時反映極度自滿的組合狀態；三項齊發為黃。"),
        "kill_condition": ("fire 後 20 交易日 SPX 回撤中位不劣於未 fire 基準，"
                           "連兩輪審計 → 刪或降黃"),
    },
]
