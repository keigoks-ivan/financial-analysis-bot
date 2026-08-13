#!/usr/bin/env python3
"""notify_render.py — 市場偵探 v2 Phase 4：統一通知模組.

Phase 2（build_detective.py＋detective_state.py）已把三源家族收斂成單一狀態機，
state.json 帶 notify 帳（keys.*.notify.{last_immediate,mute_until}）但只記帳、
不消費。本模組是唯一的「消費者＋單一寫入者」：讀 docs/detective/data/latest.json
（detective-v2，當日渲染快照）＋ state.json（detective-state-v1，真相源），
產出三級 email body（immediate／digest／weekly），並把 immediate 層實際寄出的
鍵回寫 notify.last_immediate（讓帳跟著同一次 workflow commit）。

三級定位：
  immediate — 只為「新紅燈（new 且 sev red）／escalated 至紅／composite 新 fire
              紅」這類會被漏掉的急件開窗；受 7 日曆天最小間隔 + mute_until 節流
              （escalation 事件可穿透間隔閘，但穿不透 mute）。
  digest    — 平日一次性彙總：counts 板 + top10 訊號 + 當日 transitions +
              composites + sources_stale。
  weekly    — 週六恆產：本週新增/解除/升級統計 + resolved 清單 + composite 次數
              + sources 新鮮度 + kill_watch（若存在）覆蓋率。

描述器紀律：body 全中文全形標點、純文字、只陳述事實，不判斷不擇時不給買賣指令。

CLI：
  python3 scripts/notify_render.py --tier immediate|digest|weekly [--force]
      [--out PATH] [--latest PATH] [--state PATH]

--force：無資格也產最小樣本檔（test_email 用），且**不**寫回 state.json
（避免手動測試觸發污染真實的 notify 帳）。

單一寫入者守則：本 script 只動 state.json 的
state["keys"][key]["notify"]["last_immediate"]，不動 keys 其他任何欄位；
序列化沿用 build_detective.py 的協議（ensure_ascii=False, indent=1,
sort_keys=True）以避免假 diff。
"""
import argparse
import json
import os
import re
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "docs", "detective", "data")
DEFAULT_LATEST = os.path.join(DATA_DIR, "latest.json")
DEFAULT_STATE = os.path.join(DATA_DIR, "state.json")
DEFAULT_KILL_WATCH = os.path.join(DATA_DIR, "kill_watch.json")

IMMEDIATE_MIN_GAP_DAYS = 7

FOOTER_FIXED = (
    "本信為機械描述器輸出，陳述數據狀態，不構成投資建議或擇時訊號。"
    "詳情：https://research.investmquest.com/detective/"
)
FOOTER_DEEP_READ = "可在本機 session 說「detective read」取得深度判讀"

TAG = {"new_red": "🔴", "escalated_red": "⤴", "composite_red": "🧩"}
REASON_LABEL = {"new_red": "新紅燈", "escalated_red": "升級至紅", "composite_red": "複合訊號新觸發"}
SEV_ZH = {"red": "紅", "yellow": "黃"}

# 家族聚合用的中文標籤表（weekly 新增/解除彙整）；未收錄的 source/cat 組合走
# 通用 fallback（見 _family_label），不會印出原始英文 token 以外的內部代號。
_COMBO_ZH = {
    ("sector", "rotation"): "板塊輪動",
    ("rotation", "quadrant"): "資產輪動象限",
    ("crowding", "cot"): "COT 部位擁擠",
    ("crowding", "etf"): "ETF 動能擁擠",
    ("crowding", "theme"): "主題擁擠",
    ("variance", "ticker"): "財測落差",
}
_SOURCE_ZH = {
    "monitor": "監測", "crowding": "擁擠度", "rotation": "資產輪動",
    "sector": "板塊", "reversal": "反轉", "variance": "財測", "composite": "複合規則",
}
_CAT_ZH = {
    "rates": "利率", "sectors": "板塊", "commodities": "商品", "factors": "因子",
    "indices": "指數", "credit": "信用", "vol": "波動", "liquidity": "流動性",
    "fx": "外匯", "cot": "COT 部位", "etf": "ETF 動能", "theme": "主題擁擠",
    "rotation": "輪動", "quadrant": "象限", "ticker": "財測落差", "rule": "規則",
    "diverge": "背離", "cluster": "群聚", "fleet": "組合彙總",
}

# 底線雙 token 的比值／利差族，短代號取自站上既有 label 定義（scripts/
# build_monitor.py 對應 _d() 呼叫的 label 欄位、取符號段，非機械美化猜測）——
# 查得到就照站上寫法（含 DJIA 這種與 ident 本身拼法不同、及 SOFR−IORB 的
# U+2212 全形負號慣用寫法），查不到才落到 _short_ident 的機械 A/B 大寫規則。
_MONITOR_RATIO_LABEL = {
    "rsp_spy": "RSP/SPY", "iwm_spy": "IWM/SPY", "vtv_vug": "VTV/VUG",
    "sox_ndx": "SOX/NDX", "djt_dji": "DJT/DJIA", "kre_xlf": "KRE/XLF",
    "itb_spy": "ITB/SPY", "xly_xlp": "XLY/XLP", "sphb_splv": "SPHB/SPLV",
    "hyg_lqd": "HYG/LQD", "vix_ts": "VIX9D/VIX",
    "copper_gold": "銅金比", "gold_silver": "金銀比",
    "sofr_iorb": "SOFR−IORB",
}


# ── IO（沿用 build_detective.py 的零 churn／序列化協議）──────────────────

def load_json(path, default=None):
    if not path or not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def _serialize(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def save_state(path, state):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(_serialize(state))


def _days_between(a, b):
    return abs((date.fromisoformat(b) - date.fromisoformat(a)).days)


def _write_body(out_path, lines):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    text = "\n".join(lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


def _footer(has_active_red):
    lines = ["", "—", FOOTER_FIXED]
    if has_active_red:
        lines.append(FOOTER_DEEP_READ)
    return lines


# ── immediate ────────────────────────────────────────────────────────────

def _display_for(key, keys_state, sig_by_key, composite_by_key, history_by_key=None):
    """回傳 (fact, context, label, score, no_label)。一般鍵優先取 latest.json
    signals[] 的渲染值（含 persist bonus，與頁面一致）；composite:* 鍵不在
    signals[]（render_signals 明文排除），改讀 state.keys[key].display（build
    端注入的 {source,cat,label,fact,context,score_base}），fact/label 缺時
    fallback latest.json composites[] 的 narrative/name。

    已 resolved 且從 state.keys 移除（單一寫入者：detective_state.py 結案時
    del keys[key]）的鍵，落到 history 條目自帶欄位（僅 peak_sev／days_active，
    無 label/fact）與 key 結構共同合成一句可讀敘述——這已是實質內容，不標記
    no_label（也不印「無標籤」字樣）。真的連 history 都沒有、合成徹底失敗，才
    印 key 本身並以「（無標籤）」標記且回傳 no_label=True——這是資料生命週期的
    誠實反映，不是內部代號外流。"""
    sig = sig_by_key.get(key)
    if sig:
        return (sig.get("fact", ""), sig.get("context", ""),
                sig.get("label", key), sig.get("score", 0), False)
    entry = keys_state.get(key) or {}
    disp = entry.get("display", {}) or {}
    c = composite_by_key.get(key)
    fact = disp.get("fact") or (c or {}).get("narrative", "")
    label = disp.get("label") or (c or {}).get("name")
    if label:
        return (fact, disp.get("context", ""), label, disp.get("score_base", 0), False)
    fallback = _readable_fallback(key)
    hist = (history_by_key or {}).get(key)
    if hist:
        sev_zh = SEV_ZH.get(hist.get("peak_sev"), hist.get("peak_sev") or "")
        tail = f"峰值{sev_zh}，" if sev_zh else ""
        return ("", "", f"{fallback}（{tail}歷時 {hist.get('days_active', 0)} 天）", 0, False)
    return ("", "", f"{fallback}（無標籤）", 0, True)


def _family_of(key, keys_state, sig_by_key):
    """回傳 (source, cat)。優先取 signals[]／state.keys[key].display 的顯式欄位，
    兩者皆缺（典型為已 resolved 且移出 state.keys 的鍵）才退回解析 key 前兩段
    命名空間——這兩段本身是設計時的分類詞（monitor/crowding/sector...），不是
    不透明內部代號，可安全用於分組標籤。"""
    sig = sig_by_key.get(key)
    if sig and sig.get("source") and sig.get("cat"):
        return sig["source"], sig["cat"]
    disp = (keys_state.get(key) or {}).get("display") or {}
    if disp.get("source") and disp.get("cat"):
        return disp["source"], disp["cat"]
    parts = key.split(":")
    if parts and parts[0] == "composite":
        return "composite", "rule"
    if len(parts) >= 2:
        return parts[0], parts[1]
    return parts[0] if parts else key, ""


def _family_label(source, cat):
    if (source, cat) in _COMBO_ZH:
        return _COMBO_ZH[(source, cat)]
    s = _SOURCE_ZH.get(source, source)
    c = _CAT_ZH.get(cat, cat)
    return s if s == c else f"{s}{c}"


def _direction_suffix(keys):
    dirs = {k.split(":")[-1] for k in keys if k.split(":")[-1] in ("up", "down")}
    if dirs == {"up"}:
        return "走升"
    if dirs == {"down"}:
        return "走弱"
    return ""


def _short_ident(key):
    """取 key 最後一段（扣掉 up/down 方向尾綴）當家族內部的簡短識別名——多半是
    ticker／代碼本身（XLB、GLD、MPWR），是站上既有慣用顯示名，非不透明內部代號。
    比值／利差族（底線雙 token）優先查 _MONITOR_RATIO_LABEL 取站上同名；查不到
    才落到機械規則：單 token 全大寫、多字組合詞全大寫＋空白分隔（不做 title-case
    半成品——WTI CRUDE 而非 Wti Crude）。"""
    parts = key.split(":")
    tail = parts[-1]
    ident = parts[-2] if tail in ("up", "down") and len(parts) >= 2 else tail
    if ident in _MONITOR_RATIO_LABEL:
        return _MONITOR_RATIO_LABEL[ident]
    if re.fullmatch(r"[A-Za-z]{2,6}", ident):
        return ident.upper()
    cleaned = ident.replace("-", " ").replace("_", " ")
    if re.fullmatch(r"[A-Za-z0-9 ]{2,24}", cleaned):
        return cleaned.upper()
    return cleaned


def _readable_fallback(key):
    """key 本身查無任何 label/fact 時的最終備援——不印帶冒號／up/down 尾綴的原始
    key，改用同一套家族命名（source/cat 中文＋短識別名）組一句人話，讓「無標籤」
    仍是可讀的事實句而非內部代號。"""
    source, cat = _family_of(key, {}, {})
    fam = _family_label(source, cat)
    short = _short_ident(key)
    if short and short.lower() != fam.lower():
        return f"{fam} {short}"
    return fam


def _render_family_lines(keys, keys_state, sig_by_key, composite_by_key, history_by_key):
    """把一批鍵（新增/解除清單）依 source+cat 家族聚合成精簡行；單一鍵的家族直接
    印該鍵的 label，不勉強分組。"""
    if not keys:
        return ["（無）"]
    groups = {}
    for k in sorted(set(keys)):
        fam = _family_of(k, keys_state, sig_by_key)
        groups.setdefault(fam, []).append(k)
    out = []
    for (source, cat), members in sorted(groups.items()):
        if len(members) == 1:
            _, _, label, _, _ = _display_for(members[0], keys_state, sig_by_key,
                                              composite_by_key, history_by_key)
            out.append(f"・{label}")
        else:
            fam_label = _family_label(source, cat) + _direction_suffix(members)
            shorts = "、".join(dict.fromkeys(_short_ident(k) for k in members))
            out.append(f"・{fam_label}：{shorts}")
    return out


def _immediate_candidates(latest, state):
    """回傳 [(key, reason, bypass_gap)]；reason ∈ new_red/escalated_red/
    composite_red；bypass_gap 僅 escalated_red 為 True（可穿透 7 日閘，
    仍不能穿透 mute）。

    一般鍵（含 composite:* 鍵——兩者走同一狀態機）以 transitions_today 判定
    new/escalated；composite 的「新 fire 紅」另有獨立判準：confirm_days 跨越
    可能發生在 composite 已 active 多日之後（不一定與 to=="new"/"escalated"
    重合），故改用 latest.json composites[] 的 fired_since==as_of 精確抓
    「今天剛跨過確認門檻」那一天。
    """
    as_of = latest.get("as_of") or state.get("as_of")
    keys_state = state.get("keys", {})
    trans_today = [t for t in state.get("transitions_today", []) if t.get("date") == as_of]
    new_keys = {t["key"] for t in trans_today if t.get("to") == "new"}
    esc_keys = {t["key"] for t in trans_today if t.get("to") == "escalated"}

    out = []
    for key in new_keys:
        entry = keys_state.get(key)
        if entry and entry.get("sev") == "red":
            out.append((key, "new_red", False))
    for key in esc_keys:
        entry = keys_state.get(key)
        if entry and entry.get("sev") == "red":
            out.append((key, "escalated_red", True))

    seen = {k for k, _, _ in out}
    for c in (latest.get("composites") or []):
        if not isinstance(c, dict):
            continue
        if c.get("fired") and c.get("sev") == "red" and c.get("fired_since") == as_of:
            ckey = f"composite:{c.get('id')}"
            if ckey not in seen:
                out.append((ckey, "composite_red", False))
    return out


def render_immediate(latest, state, force=False):
    """回傳 (body_text_or_None, eligible_keys[])。呼叫端只在 eligible_keys
    非空且非 force 時才寫回 state.json。"""
    as_of = latest.get("as_of") or state.get("as_of")
    keys_state = state.get("keys", {})
    sig_by_key = {s["key"]: s for s in latest.get("signals", [])}
    composite_by_key = {f"composite:{c.get('id')}": c for c in (latest.get("composites") or [])
                        if isinstance(c, dict)}

    eligible = {}  # key -> {"reasons": set()}
    for key, reason, bypass in _immediate_candidates(latest, state):
        notify = (keys_state.get(key) or {}).get("notify") or {}
        mute_until = notify.get("mute_until")
        last_immediate = notify.get("last_immediate")
        if mute_until and as_of and mute_until >= as_of:
            continue  # mute 一律擋，escalation 也穿不透
        if last_immediate == as_of:
            continue  # 同一 as_of 已記過帳——冪等閘（重跑不重複）
        if last_immediate:
            gap_ok = _days_between(last_immediate, as_of) >= IMMEDIATE_MIN_GAP_DAYS
        else:
            gap_ok = True
        if not gap_ok and not bypass:
            continue
        eligible.setdefault(key, {"reasons": set()})["reasons"].add(reason)

    if not eligible and not force:
        return None, []

    rows = []
    for key, e in eligible.items():
        fact, context, label, score, no_label = _display_for(key, keys_state, sig_by_key, composite_by_key)
        rows.append((score, key, e["reasons"], fact, context, label, no_label))
    rows.sort(key=lambda r: -r[0])

    lines = [f"市場偵探 — 即時警報 {as_of or ''}", ""]
    if rows:
        for score, key, reasons, fact, context, label, no_label in rows:
            reasons = sorted(reasons)
            tag = TAG.get(reasons[0], "🔴")
            why = "、".join(REASON_LABEL.get(r, r) for r in reasons)
            days = (keys_state.get(key) or {}).get("days_active", 1)
            line = f"{tag} {fact or label}"
            if context:
                line += f"（{context}）"
            line += f"　第 {days} 天　[{why}]"
            if no_label:
                line += "（無標籤）"
            lines.append(line)
    else:
        lines.append("（測試信：目前無資格事件，這是即時警報管線的測試樣本。）")
    lines += _footer(has_active_red=True)  # immediate 層恆為紅燈事件
    return "\n".join(lines), sorted(eligible.keys())


# ── digest ───────────────────────────────────────────────────────────────

def render_digest(latest, state, force=False):
    as_of = latest.get("as_of")
    signals = latest.get("signals", [])
    transitions = state.get("transitions_today", [])
    active_red = [s for s in signals if s.get("sev") == "red"]
    # composite:* 鍵不進 signals[]（render_signals 明文排除），現存紅級 composite
    # 一樣算「存在 active 紅燈」，否則 fired composite 會被誤判成當天無事可摘。
    fired_red_composites = [c for c in (latest.get("composites") or [])
                            if isinstance(c, dict) and c.get("fired") and c.get("sev") == "red"]
    eligible = bool(transitions) or bool(active_red) or bool(fired_red_composites)
    if not eligible and not force:
        return None

    keys_state = state.get("keys", {})
    history_by_key = {h.get("key"): h for h in state.get("history", []) if h.get("key")}
    sig_by_key = {s["key"]: s for s in signals}
    composite_by_key = {f"composite:{c.get('id')}": c for c in (latest.get("composites") or [])
                        if isinstance(c, dict)}
    counts = latest.get("counts", {})
    new_count = counts.get("new", 0)
    n_red = len(active_red)
    n_yellow = counts.get("yellow", max(counts.get("total", 0) - n_red, 0))
    n_total = counts.get("total", n_red + n_yellow)
    composites_all = [c for c in (latest.get("composites") or []) if isinstance(c, dict)]
    fired_composites = [c for c in composites_all if c.get("fired")]
    n_comp_fired = len(fired_composites)

    # transitions 只點名四類會被漏掉的重要事件（新紅／升級至紅／composite
    # fire／紅燈 resolved），其餘黃燈流水帳收斂成一行計數；分類提前到這裡算，
    # 讓「今日新增／升級／結案」可以先併入頭條總覽，讀者不用往下找。
    trans_today = [t for t in transitions if t.get("date") == as_of]
    red_keys_now = {s["key"] for s in active_red}
    new_red_keys = [t["key"] for t in trans_today if t.get("to") == "new" and t["key"] in red_keys_now]
    esc_red_keys = [t["key"] for t in trans_today if t.get("to") == "escalated" and t["key"] in red_keys_now]
    composite_fire_today = [c for c in composites_all
                            if c.get("fired") and c.get("fired_since") == as_of]
    resolved_red_keys = [t["key"] for t in trans_today if t.get("to") == "resolved"
                         and (history_by_key.get(t["key"]) or {}).get("peak_sev") == "red"]
    counted = set(new_red_keys) | set(esc_red_keys) | set(resolved_red_keys)
    n_esc_confirm = len([t for t in trans_today if t.get("to") == "escalated" and t["key"] not in counted])
    n_cooling = len([t for t in trans_today if t.get("to") == "cooling"])
    n_closed = len([t for t in trans_today if t.get("to") == "resolved" and t["key"] not in counted])
    n_other = len([t for t in trans_today
                  if t.get("to") not in ("new", "escalated", "cooling", "resolved")])
    n_esc_total = len(esc_red_keys) + n_esc_confirm
    n_closed_total = len(resolved_red_keys) + n_closed

    lines = [f"市場偵探 — 每日摘要 {as_of or ''}", ""]

    # 例外報告的核心收斂：紅／composite fired／新增皆為 0 時，一行帶過並收工，
    # 不逼讀者掃過一整份狀態機 dump 才確認「今天沒事」。
    if n_red == 0 and n_comp_fired == 0 and new_count == 0:
        lines.append(f"今日無紅級事件與新訊號，黃燈變動 ±{len(transitions)}（詳頁面）")
        lines += _footer(has_active_red=False)
        return "\n".join(lines)

    lines.append(
        f"總覽：{n_total} 訊號｜紅 {n_red}｜黃 {n_yellow}｜"
        f"今日新增 {new_count}、升級 {n_esc_total}、結案 {n_closed_total}"
    )
    lines.append("")

    if active_red:
        lines.append("紅級訊號：")
        for s in sorted(active_red, key=lambda s: -s.get("score", 0)):
            line = f"🔴 {s.get('fact') or s.get('label', s.get('key', ''))}"
            if s.get("context"):
                line += f"（{s['context']}）"
            line += f"　第 {s.get('days_active', 1)} 天"
            lines.append(line)
        lines.append("")

    new_keys_today = sorted({t["key"] for t in transitions
                             if t.get("date") == as_of and t.get("to") == "new"})
    if new_keys_today:
        lines.append(f"新增訊號（{len(new_keys_today)} 筆）：")
        for k in new_keys_today:
            fact, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            lines.append(f"・{fact or label}")
        lines.append("")

    if trans_today:
        lines.append("當日轉變：")
        for k in new_red_keys:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            lines.append(f"・新紅：{label}")
        for k in esc_red_keys:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            lines.append(f"・升級至紅：{label}")
        for c in composite_fire_today:
            lines.append(f"・composite fire：{c.get('name', c.get('id', ''))}")
        for k in resolved_red_keys:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key, history_by_key)
            lines.append(f"・紅燈 resolved：{label}")
        tail_bits = []
        if n_esc_confirm:
            tail_bits.append(f"升級確認 {n_esc_confirm}")
        if n_cooling:
            tail_bits.append(f"轉冷卻 {n_cooling}")
        if n_closed:
            tail_bits.append(f"結案 {n_closed}")
        if n_other:
            tail_bits.append(f"其他 {n_other}")
        if tail_bits:
            lines.append(f"黃燈變動：{'、'.join(tail_bits)}（詳頁面）")
        lines.append("")

    if composites_all:
        if fired_composites:
            lines.append("Composites（fired）：")
            for c in fired_composites:
                lines.append(
                    f"・{c.get('name', c.get('id', ''))}"
                    f"（{SEV_ZH.get(c.get('sev'), c.get('sev') or '')}）｜"
                    f"成員 {c.get('met_count', 0)}/{c.get('min_true', 0)}"
                )
        else:
            closest = max(composites_all, key=lambda c: c.get("proximity", 0))
            lines.append(
                f"Composite 0/{len(composites_all)} fired（最接近觸發："
                f"{closest.get('name', closest.get('id', ''))} "
                f"{closest.get('met_count', 0)}/{closest.get('min_true', 0)}）"
            )

    stale = latest.get("sources_stale") or []
    if stale:
        lines.append(f"Sources stale（{len(stale)} 筆）：{'、'.join(stale)}")

    lines += _footer(has_active_red=bool(active_red) or bool(fired_red_composites))
    return "\n".join(lines)


# ── weekly ───────────────────────────────────────────────────────────────

def render_weekly(latest, state):
    as_of = latest.get("as_of") or state.get("as_of")
    if not as_of:
        lines = ["市場偵探 — 週報", "", "（測試信：目前無 as_of 可回顧，這是週報管線的測試樣本。）"]
        lines += _footer(has_active_red=False)
        return "\n".join(lines)

    ref = date.fromisoformat(as_of)
    window_start = (ref - timedelta(days=6)).isoformat()

    keys_state = state.get("keys", {})
    history = state.get("history", [])
    history_by_key = {h.get("key"): h for h in history if h.get("key")}
    signals = latest.get("signals", [])
    sig_by_key = {s["key"]: s for s in signals}
    composite_by_key = {f"composite:{c.get('id')}": c for c in (latest.get("composites") or [])
                        if isinstance(c, dict)}
    kill_watch = load_json(DEFAULT_KILL_WATCH)

    new_this_week = sorted(
        k for k, e in keys_state.items()
        if e.get("first_seen") and window_start <= e["first_seen"] <= as_of
    )
    resolved_this_week = sorted(
        h.get("key") for h in history
        if h.get("resolved_at") and window_start <= h["resolved_at"] <= as_of
    )

    # 「升級」只認 sev 真的變了（from != to，如 yellow→red）；yellow→yellow
    # 的 sustained 確認不算升級，另外收斂成一行計數。
    escalated_events = []
    sustained_count = 0
    for k, e in keys_state.items():
        for esc in (e.get("escalations") or []):
            d = esc.get("date")
            if not (d and window_start <= d <= as_of):
                continue
            if esc.get("from") != esc.get("to"):
                escalated_events.append((k, esc))
            elif esc.get("type") == "sustained":
                sustained_count += 1

    # composite 新 fire：只看本次快照（latest.json composites[] 是 as_of 當日
    # 現況，抓不到本週已 fire 又已停止的 composite——已知限制，誠實列出）。
    composites_now = [c for c in (latest.get("composites") or []) if isinstance(c, dict)]
    new_fires_this_week = [
        c for c in composites_now
        if c.get("fired") and c.get("fired_since") and window_start <= c["fired_since"] <= as_of
    ]

    new_red_this_week = {k for k in new_this_week if (keys_state.get(k) or {}).get("sev") == "red"}
    new_red_this_week |= {k for k, esc in escalated_events if esc.get("to") == "red"}
    kill_breached = (kill_watch or {}).get("breached") or []

    lines = [f"市場偵探 — 週報 {window_start} ~ {as_of}", ""]
    lines.append(
        f"【本週要點】新紅 {len(new_red_this_week)}｜composite fire {len(new_fires_this_week)}｜"
        f"kill breached {len(kill_breached)}｜"
        f"訊號淨變化（新增 {len(new_this_week)}／解除 {len(resolved_this_week)}）"
    )
    lines.append("")

    lines.append(f"本週新增（{len(new_this_week)} 筆）：")
    lines.extend(_render_family_lines(new_this_week, keys_state, sig_by_key,
                                       composite_by_key, history_by_key))
    lines.append("")
    lines.append(f"本週解除（{len(resolved_this_week)} 筆）：")
    lines.extend(_render_family_lines(resolved_this_week, keys_state, sig_by_key,
                                       composite_by_key, history_by_key))
    lines.append("")

    lines.append(f"本週升級（sev 真升級）{len(escalated_events)} 筆：")
    if escalated_events:
        for k, esc in sorted(escalated_events, key=lambda x: x[0]):
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key, history_by_key)
            from_zh = SEV_ZH.get(esc.get("from"), esc.get("from") or "")
            to_zh = SEV_ZH.get(esc.get("to"), esc.get("to") or "")
            lines.append(f"・{label}：{from_zh}→{to_zh}（{esc.get('date')}）")
    else:
        lines.append("（無）")
    lines.append(f"黃燈持續確認 {sustained_count} 筆")
    lines.append("")

    lines.append(
        f"本週 composite 新 fire {len(new_fires_this_week)} 條"
        "（僅計本次快照仍在 fired 狀態者，已提早停止的 composite 不計入）："
    )
    if new_fires_this_week:
        for c in new_fires_this_week:
            sev_zh = SEV_ZH.get(c.get("sev"), c.get("sev") or "")
            lines.append(f"・{c.get('name', c.get('id', ''))}（{sev_zh}）｜觸發日 {c.get('fired_since')}")
    else:
        lines.append("（無）")
    lines.append("")

    sources = latest.get("sources", {})
    stale = latest.get("sources_stale") or []
    lines.append("各源 as-of：")
    for name, sd in sorted(sources.items()):
        flag = "（過期）" if name in stale else ""
        lines.append(f"・{name}：{sd or '（缺）'}{flag}")
    lines.append("")

    if kill_watch:
        coverage = kill_watch.get("coverage") or {}
        mechanical = coverage.get("mechanical", 0)
        total = coverage.get("total", 0)
        llm_only = coverage.get("llm_only", 0)
        items_by_id = {it.get("id"): it for it in (kill_watch.get("items") or [])
                      if isinstance(it, dict)}
        breached_labels = [
            (items_by_id.get(b) or {}).get("metric_text", b) for b in kill_breached
        ]
        breached_part = f"breached {len(kill_breached)} 筆"
        if breached_labels:
            breached_part += f"：{'、'.join(breached_labels)}"
        lines.append(
            f"Kill watch：機械監控 {mechanical}/{total}，{breached_part}"
            f"（另 {llm_only} 條屬 LLM 語意判定、不在機械比對內）"
        )
    else:
        lines.append("Kill watch：（kill_watch.json 尚未建置，略過）")

    active_red = any(s.get("sev") == "red" for s in latest.get("signals", [])) or any(
        isinstance(c, dict) and c.get("fired") and c.get("sev") == "red"
        for c in (latest.get("composites") or [])
    )
    lines += _footer(has_active_red=active_red)
    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────────

def _default_out(tier):
    return os.path.join(ROOT, f"detective_mail_{tier}.txt")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tier", required=True, choices=["immediate", "digest", "weekly"])
    ap.add_argument("--force", action="store_true", help="無資格也產最小樣本檔（test_email 用）；不寫回 state.json")
    ap.add_argument("--out", default=None, help="輸出 body 檔路徑（預設 repo 根 detective_mail_{tier}.txt，已 gitignore）")
    ap.add_argument("--latest", default=DEFAULT_LATEST)
    ap.add_argument("--state", default=DEFAULT_STATE)
    args = ap.parse_args()

    out_path = args.out or _default_out(args.tier)
    latest = load_json(args.latest, {})
    state = load_json(args.state, {})

    if args.tier == "immediate":
        body, eligible_keys = render_immediate(latest, state, force=args.force)
        if body is None:
            print("notify_render[immediate]: no eligible event, no file written")
            return
        _write_body(out_path, [body])
        if eligible_keys and not args.force:
            as_of = latest.get("as_of")
            for k in eligible_keys:
                if k in state.get("keys", {}):
                    state["keys"][k].setdefault("notify", {})["last_immediate"] = as_of
            save_state(args.state, state)
            print(f"notify_render[immediate]: {len(eligible_keys)} eligible key(s), "
                  f"state.json notify 帳已更新 → {args.state}")
        else:
            print(f"notify_render[immediate]: body written (force={args.force}, "
                  f"{len(eligible_keys)} eligible key(s)), state.json 未動")
        print(f"body → {out_path}")

    elif args.tier == "digest":
        body = render_digest(latest, state, force=args.force)
        if body is None:
            print("notify_render[digest]: no eligible day, no file written")
            return
        _write_body(out_path, [body])
        print(f"notify_render[digest]: body → {out_path}")

    else:  # weekly
        body = render_weekly(latest, state)
        _write_body(out_path, [body])
        print(f"notify_render[weekly]: body → {out_path}")


if __name__ == "__main__":
    main()
