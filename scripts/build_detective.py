#!/usr/bin/env python3
"""build_detective.py — 市場偵探引擎（純機械、零 LLM、確定性）.

把站上「已經在跑、卻沒人盯著被觸發」的偵測層聚合成單一警報網：
  · monitor 異常引擎（alerts.json：z-score / 分位 / 結構事件，紅/黃燈）
  · 擁擠交易 COT 極端 + 主題擁擠 + ETF 動能極端（crowding latest.json）
  · 產業/資產輪動象限翻轉（rotation radar cross_asset 120d）

每條訊號帶：來源、事實描述、嚴重度評分、脈絡（軌跡/連續天數）、是否今日新增。
輸出：
  · docs/detective/data/latest.json  — 全部訊號（給測試/偵探頁渲染）
  · detective_alert.txt（未 commit）  — 紅燈級 + 今日新增，供 GitHub Actions email 步驟

描述器紀律：只陳述事實，不判斷、不擇時、不給買賣指令。
規格：notes/site-internal/root/_routine_home_pulse_spec.md（同家族）。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

SHORT = {
    "房地產REIT": "房地產", "美長天期公債": "美長債", "投資級公司債": "投資級債",
    "成熟市場股": "成熟股", "新興市場股": "新興市場", "大宗商品": "大宗",
    "高收益債": "高收益",
}


def _load(rel, default=None):
    p = os.path.join(DOCS, rel)
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def _fmt(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


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
    """0-15 連續分：紅燈基底 10、黃燈 5，加幅度（|z| / 分位極端 / 天數），上限 +5。"""
    base = 10.0 if sev == "red" else 5.0
    return round(base + min(magnitude, 5.0), 2)


# ── monitor 異常（engine 的紅/黃燈，enrich 軌跡）──

def monitor_signals(latest, alerts):
    days = alerts.get("days", {})
    if not days:
        return []
    day = max(days)                       # 最近有異常的交易日
    out = []
    for a in days[day]:
        sev = a.get("sev", "yellow")
        it = _mon_series(latest, a.get("cat"), a.get("key"))
        mag = 0.0
        ctx = ""
        if it:
            if a.get("rule") == "move_z":
                mag = abs(it.get("z", 0) or 0)
            elif a.get("rule") == "pctile":
                mag = abs((it.get("pctile", 50) or 50) - 50) / 10.0
            else:
                mag = 2.0
            if all(k in it for k in ("p60", "p20", "pctile")):
                ctx = f"分位 {_fmt(it['p60'])}→{_fmt(it['p20'])}→{_fmt(it['pctile'])}"
        out.append({
            "source": "monitor", "cat": a.get("cat", ""),
            "label": (it or {}).get("label", a.get("key", "")),
            "fact": a.get("msg", ""), "sev": sev,
            "score": _score(sev, mag), "context": ctx,
        })
    return out


# ── crowding：COT 極端 + 主題擁擠 + ETF 動能極端 ──

def crowding_signals(crowd):
    if not crowd:
        return []
    out = []
    asof = crowd.get("cot_as_of", "")
    for m in crowd.get("cot", []):
        p5 = m.get("pctile_5y", 50)
        ext = m.get("extreme")
        if not (ext or p5 >= 90 or p5 <= 10):
            continue
        side = ("偏多極端" if p5 >= 90 else "偏空極端")
        mag = abs(p5 - 50) / 10.0
        out.append({
            "source": "crowding", "cat": "cot",
            "label": f"{m['market']} 投機部位",
            "fact": (f"{m['market']} COT {m.get('direction', '')}、"
                     f"5 年分位 {_fmt(p5)}（{side}；淨 {m.get('net_pct_oi')}% OI）"),
            "sev": "yellow", "score": _score("yellow", mag),
            "context": f"COT as-of {asof}",
        })
    for e in crowd.get("etf", []):
        mp = e.get("momentum_pctile", 50)
        if mp is None or not (mp >= 95 or mp <= 5):
            continue
        mag = abs(mp - 50) / 10.0
        out.append({
            "source": "crowding", "cat": "etf",
            "label": f"{e.get('label', e.get('ticker'))} 動能",
            "fact": (f"{e.get('label')}（{e.get('ticker')}）動能分位 {_fmt(mp)}"
                     f"、偏離分位 {_fmt(e.get('deviation_pctile', 0) or 0)}"),
            "sev": "yellow", "score": _score("yellow", mag),
            "context": "",
        })
    themes = sorted((t for t in crowd.get("themes", []) if t.get("score")),
                    key=lambda t: -t["score"])[:3]
    for t in themes:
        if t["score"] < 70:
            continue
        mag = (t["score"] - 70) / 10.0
        out.append({
            "source": "crowding", "cat": "theme",
            "label": f"主題擁擠：{t['name']}",
            "fact": f"{t['name']} 擁擠分 {_fmt(t['score'])}（五維綜合，排名第 {t.get('rank', '?')}）",
            "sev": "yellow", "score": _score("yellow", mag),
            "context": "",
        })
    return out


# ── rotation：cross_asset 120d 象限翻轉 ──

def rotation_signals(radar):
    if not radar:
        return []
    ca = next((u for u in radar.get("universes", []) if u.get("key") == "cross_asset"), None)
    if not ca:
        return []
    out = []
    for mem in ca.get("members", []):
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
        short = SHORT.get(mem["label"], mem["label"])
        state = "已確認" if confirmed else "接近中"
        mag = (2.5 if confirmed else 1.0) + min(disp, 2.0)
        out.append({
            "source": "rotation", "cat": "quadrant",
            "label": f"{short} {mem['ticker']} 動能",
            "fact": (f"{short} {mem['ticker']} 象限 {q_before}→{q_now}"
                     f"（RS-M {'升破' if m_now >= 100 else '跌破'} 100，{state}）"),
            "sev": "yellow", "score": _score("yellow", mag),
            "context": f"持穩 {held} 交易日、RS-M {m_now:.2f}",
        })
    return out


def _key(s):
    return f"{s['source']}:{s['label']}"


def main():
    latest = _load("monitor/data/latest.json", {})
    alerts = _load("monitor/data/alerts.json", {})
    crowd = _load("crowding/data/latest.json", {})
    radar = _load("rotation/data/radar.json", {})

    signals = (monitor_signals(latest, alerts)
               + crowding_signals(crowd)
               + rotation_signals(radar))
    signals.sort(key=lambda s: -s["score"])

    prev = _load("detective/data/latest.json", {})
    prev_keys = {_key(s) for s in prev.get("signals", [])}
    for s in signals:
        s["new"] = _key(s) not in prev_keys

    red = [s for s in signals if s["sev"] == "red"]
    new = [s for s in signals if s["new"]]

    out = {
        "schema": "detective-v1",
        "generated_at": radar.get("generated_at") or latest.get("generated_at"),
        "monitor_as_of": latest.get("as_of"),
        "crowding_as_of": crowd.get("cot_as_of"),
        "radar_as_of": radar.get("as_of"),
        "counts": {"total": len(signals), "red": len(red),
                   "yellow": len(signals) - len(red), "new": len(new)},
        "signals": signals,
    }

    path = os.path.join(DOCS, "detective", "data", "latest.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    changed = old != content
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    # email digest：紅燈級 + 今日新增（去重）
    alert_items = []
    seen = set()
    for s in red + new:
        k = _key(s)
        if k in seen:
            continue
        seen.add(k)
        tag = "🔴" if s["sev"] == "red" else "🆕"
        line = f"{tag} {s['fact']}"
        if s["context"]:
            line += f"（{s['context']}）"
        alert_items.append((s["score"], line))
    alert_items.sort(key=lambda x: -x[0])

    alert_file = os.path.join(ROOT, "detective_alert.txt")
    if alert_items:
        lines = [f"市場偵探 — {out['monitor_as_of']}",
                 f"紅燈 {len(red)}、今日新增 {len(new)}、總訊號 {len(signals)}", ""]
        lines += [ln for _, ln in alert_items]
        lines += ["", "— 描述器：只陳述事實，非擇時訊號。",
                  "詳見 https://research.investmquest.com/detective/"]
        with open(alert_file, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"detective: {len(signals)} signals, {len(red)} red, {len(new)} new "
              f"— alert digest written ({len(alert_items)} items)")
    else:
        if os.path.exists(alert_file):
            os.remove(alert_file)
        print(f"detective: {len(signals)} signals, 0 red / 0 new — no alert")
    print(f"detective/data/latest.json: {'written' if changed else 'zero-churn'}")


if __name__ == "__main__":
    main()
