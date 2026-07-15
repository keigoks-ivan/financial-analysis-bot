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

def _display_for(key, keys_state, sig_by_key, composite_by_key):
    """回傳 (fact, context, label, score)。一般鍵優先取 latest.json signals[]
    的渲染值（含 persist bonus，與頁面一致）；composite:* 鍵不在 signals[]
    （render_signals 明文排除），改讀 state.keys[key].display（build 端注入的
    {source,cat,label,fact,context,score_base}），fact/label 缺時 fallback
    latest.json composites[] 的 narrative/name。"""
    sig = sig_by_key.get(key)
    if sig:
        return (sig.get("fact", ""), sig.get("context", ""),
                sig.get("label", key), sig.get("score", 0))
    disp = (keys_state.get(key) or {}).get("display", {}) or {}
    c = composite_by_key.get(key)
    fact = disp.get("fact") or (c or {}).get("narrative", "")
    label = disp.get("label") or (c or {}).get("name", key)
    return fact, disp.get("context", ""), label, disp.get("score_base", 0)


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
        fact, context, label, score = _display_for(key, keys_state, sig_by_key, composite_by_key)
        rows.append((score, key, e["reasons"], fact, context, label))
    rows.sort(key=lambda r: -r[0])

    lines = [f"市場偵探 — 即時警報 {as_of or ''}", ""]
    if rows:
        for score, key, reasons, fact, context, label in rows:
            reasons = sorted(reasons)
            tag = TAG.get(reasons[0], "🔴")
            why = "、".join(REASON_LABEL.get(r, r) for r in reasons)
            line = f"{tag} {fact or label}"
            if context:
                line += f"（{context}）"
            line += f"　[{why}]"
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

    counts = latest.get("counts", {})
    lines = [f"市場偵探 — 每日摘要 {as_of or ''}", ""]
    lines.append(
        f"總訊號 {counts.get('total', 0)}｜紅 {counts.get('red', 0)}｜"
        f"黃 {counts.get('yellow', 0)}｜新增 {counts.get('new', 0)}｜"
        f"活躍 {counts.get('active', 0)}｜升級 {counts.get('escalated', 0)}｜"
        f"冷卻 {counts.get('cooling', 0)}"
    )
    lines.append("")

    if not signals and not force:
        lines.append("（目前無任何訊號。）")
    elif not signals:
        lines.append("（測試信：目前無訊號，這是每日摘要管線的測試樣本。）")
    else:
        lines.append("Top 10 訊號（依分數降冪）：")
        top = sorted(signals, key=lambda s: -s.get("score", 0))[:10]
        for s in top:
            lines.append(
                f"・{s.get('label', s.get('key'))}｜{s.get('fact', '')}｜"
                f"state={s.get('state', '')}｜days_active={s.get('days_active', 0)}"
            )
    lines.append("")

    lines.append(f"當日 transitions（{len(transitions)} 筆）：")
    if transitions:
        for t in transitions:
            lines.append(f"・{t.get('key')}：{t.get('from')}→{t.get('to')}（{t.get('reason', '')}）")
    else:
        lines.append("（無）")
    lines.append("")

    composites = [c for c in (latest.get("composites") or []) if isinstance(c, dict)]
    fired = [c for c in composites if c.get("fired")]
    lines.append(f"Composites（{len(composites)} 條規則，{len(fired)} 條 fired；缺檔或空陣列時安全顯示 0）：")
    if composites:
        for c in composites:
            tag = "FIRED" if c.get("fired") else c.get("status", "")
            lines.append(
                f"・{c.get('name', c.get('id', ''))}｜{tag}｜sev={c.get('sev', '')}｜"
                f"成員 {c.get('met_count', 0)}/{c.get('min_true', 0)}"
            )
    else:
        lines.append("（無）")
    lines.append("")

    stale = latest.get("sources_stale") or []
    lines.append(f"Sources stale（{len(stale)} 筆）：{'、'.join(stale) if stale else '（無）'}")

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

    new_this_week = sorted(
        k for k, e in keys_state.items()
        if e.get("first_seen") and window_start <= e["first_seen"] <= as_of
    )
    resolved_this_week = sorted(
        h.get("key") for h in history
        if h.get("resolved_at") and window_start <= h["resolved_at"] <= as_of
    )
    escalated_events = []
    for k, e in keys_state.items():
        for esc in (e.get("escalations") or []):
            d = esc.get("date")
            if d and window_start <= d <= as_of:
                escalated_events.append((k, esc))

    # composite 新 fire：只看本次快照（latest.json composites[] 是 as_of 當日
    # 現況，抓不到本週已 fire 又已停止的 composite——已知限制，誠實列出）。
    composites_now = [c for c in (latest.get("composites") or []) if isinstance(c, dict)]
    new_fires_this_week = [
        c for c in composites_now
        if c.get("fired") and c.get("fired_since") and window_start <= c["fired_since"] <= as_of
    ]

    lines = [f"市場偵探 — 週報 {window_start} ~ {as_of}", ""]
    lines.append(f"本週新增 {len(new_this_week)} 筆：{'、'.join(new_this_week) if new_this_week else '（無）'}")
    lines.append(f"本週解除 {len(resolved_this_week)} 筆：{'、'.join(resolved_this_week) if resolved_this_week else '（無）'}")
    lines.append(f"本週升級 {len(escalated_events)} 筆事件：")
    if escalated_events:
        for k, esc in escalated_events:
            lines.append(f"・{k}：{esc.get('from')}→{esc.get('to')}（{esc.get('type')}，{esc.get('date')}）")
    else:
        lines.append("（無）")
    lines.append(
        f"本週 composite 新 fire {len(new_fires_this_week)} 條"
        "（僅計本次快照仍在 fired 狀態者，已提早停止的 composite 不計入）："
    )
    if new_fires_this_week:
        for c in new_fires_this_week:
            lines.append(f"・{c.get('name', c.get('id', ''))}｜sev={c.get('sev', '')}｜fired_since={c.get('fired_since')}")
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

    kill_watch = load_json(DEFAULT_KILL_WATCH)
    if kill_watch:
        coverage = kill_watch.get("coverage_pct", kill_watch.get("coverage"))
        breached = kill_watch.get("breached", [])
        lines.append("Kill watch：")
        if coverage is not None:
            lines.append(f"・覆蓋率：{coverage}")
        lines.append(f"・breached（{len(breached)} 筆）：{'、'.join(breached) if breached else '（無）'}")
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
