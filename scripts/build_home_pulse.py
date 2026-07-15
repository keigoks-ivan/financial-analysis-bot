#!/usr/bin/env python3
"""Generate docs/home/pulse.json — 首頁「市場脈動」（純機械、零 LLM）.

只陳述事實 + 機械偵測轉折：讀 monitor 機械層（latest.json）＋ rotation radar
（radar.json，cross_asset 120d），輸出事實 bullet 與轉折提醒（象限跨界演算法，
分「已確認 / 接近中」兩級）。不做判斷分析、不擇時、不給買賣指令。

自動化：GitHub Actions cron（home-pulse-daily），在 monitor（build_monitor.py）與
rotation radar（build_rotation_radar.py）日更之後執行。設計規格見
notes/site-internal/root/_routine_home_pulse_spec.md（schema=home-pulse-v2）。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# 縮短過長的 radar 標籤（純顯示用）
SHORT = {
    "房地產REIT": "房地產", "美長天期公債": "美長債", "投資級公司債": "投資級債",
    "成熟市場股": "成熟股", "新興市場股": "新興市場", "大宗商品": "大宗",
    "高收益債": "高收益", "美股": "美股", "黃金": "黃金", "美元": "美元",
    "比特幣": "比特幣",
}


def _load(rel):
    with open(os.path.join(DOCS, rel), encoding="utf-8") as fh:
        return json.load(fh)


def _series(latest, key):
    for cat in latest.get("categories", []):
        for it in cat.get("items", []):
            if it.get("key") == key:
                return it
    return None


def _fmt(x):
    """100.0 -> '100'；11.5 -> '11.5'；50.8 -> '50.8'."""
    return f"{x:.1f}".rstrip("0").rstrip(".")


def _traj(it):
    return f"{_fmt(it['p60'])}→{_fmt(it['p20'])}→{_fmt(it['pctile'])}"


def _chg(s):
    """'▲ 132B' -> '＋132B'；'▼ 106B' -> '−106B'."""
    return (str(s).replace("▲ ", "＋").replace("▼ ", "−")
            .replace("▲", "＋").replace("▼", "−")
            .replace("＝ ", "").replace("＝", "").strip())


def quad(r, m):
    if r >= 100 and m >= 100:
        return "領先"   # 領先
    if r >= 100 and m < 100:
        return "轉弱"   # 轉弱
    if r < 100 and m >= 100:
        return "改善"   # 改善
    return "落後"       # 落後


# ── monitor 事實 bullet ──

def monitor_points(latest):
    pts = []
    r10 = _series(latest, "real10y")
    if r10:
        pts.append(f"10Y TIPS 實質利率 {r10['val']}，分位 "
                   f"{_fmt(r10['pctile'])}（{_traj(r10)}）")

    liq = latest.get("status", {}).get("liquidity", {}).get("label", "")
    res = _series(latest, "reserves")
    sofr = _series(latest, "sofr_iorb")
    seg = []
    if res:
        seg.append(f"銀行準備金單週 {_chg(res['chg'])}")
    if sofr:
        seg.append(f"SOFR−IORB 分位 {_fmt(sofr['pctile'])}")
    if liq and seg:
        pts.append(f"{liq}：" + "、".join(seg))
    elif seg:
        pts.append("、".join(seg))

    bei = _series(latest, "bei5y")
    vix = _series(latest, "vix")
    fg = latest.get("fear_greed", {})
    seg3 = []
    if bei:
        seg3.append(f"5Y 通膨預期分位 {_fmt(bei['pctile'])}"
                    f"（{_traj(bei)}）")
    tail = []
    if vix:
        tail.append(f"VIX {vix['val']}")
    if fg:
        tail.append(f"恐懼貪婪 {fg['score']}")
    if tail:
        seg3.append("、".join(tail))
    if seg3:
        pts.append("；".join(seg3))
    return pts


# ── radar 象限分析 + 轉折偵測 ──

def radar_members(radar):
    ca = next(u for u in radar["universes"] if u["key"] == "cross_asset")
    out = []
    for m in ca["members"]:
        fr = m.get("frames", {}).get("120")
        if not fr or not fr.get("trail"):
            continue
        trail = fr["trail"]
        last = trail[-1]
        q = quad(last["r"], last["m"])
        streak = 1
        for i in range(len(trail) - 2, -1, -1):
            if quad(trail[i]["r"], trail[i]["m"]) == q:
                streak += 1
            else:
                break
        out.append({"label": m["label"], "short": SHORT.get(m["label"], m["label"]),
                    "ticker": m["ticker"], "r": last["r"], "m": last["m"],
                    "q": q, "streak": streak, "trail": trail})
    return out


def detect_reversals(members, lookback=8):
    """偵測近 lookback 交易日內 RS-M 穿越 100 的動能轉折。"""
    flagged = []
    for mem in members:
        trail = mem["trail"]
        n = len(trail)
        cross = None
        for i in range(n - 1, max(n - 1 - lookback, 0), -1):
            if (trail[i - 1]["m"] >= 100) != (trail[i]["m"] >= 100):
                cross = i
                break
        if cross is None:
            continue
        held = n - cross                      # 跨界後交易日數（含跨界日）
        m_now = trail[-1]["m"]
        disp = abs(m_now - 100.0)             # 現值離 100 中軸多遠
        if disp < 0.15 and held < 2:          # 純雜訊過濾
            continue
        q_before = quad(trail[cross - 1]["r"], trail[cross - 1]["m"])
        # 已確認：站穩夠久（≥5 日）或（≥3 日且明顯離開中軸 ≥0.5）
        confirmed = held >= 5 or (held >= 3 and disp >= 0.5)
        mem["_rev"] = {"held": held, "disp": disp, "up": m_now >= 100,
                       "from": q_before, "to": mem["q"], "confirmed": confirmed}
        flagged.append(mem)
    return flagged


def reversal_flags(flagged):
    groups = {}
    for mem in flagged:
        rv = mem["_rev"]
        groups.setdefault((rv["from"], rv["to"], rv["confirmed"], rv["up"]), []).append(mem)
    out = []
    for (frm, to, conf, up), mems in sorted(groups.items(), key=lambda kv: not kv[0][2]):
        axis = "、".join(f"{m['short']} {m['ticker']}" for m in mems) + " 動能"
        held = min(m["_rev"]["held"] for m in mems)
        vals = "、".join(f"{m['ticker']} {m['trail'][-1]['m']:.2f}" for m in mems)
        verb = "升破" if up else "跌破"
        if conf:
            ev = f"RS-M {verb} 100、持穩 {held} 交易日（{vals}）"
        else:
            ev = (f"RS-M {verb} 100 未站穩、接近"
                  f"（{held} 交易日、{vals}）")
        out.append({"axis": axis, "from": frm, "to": to, "evidence": ev})
    return out


def radar_points(members):
    by_q = {"領先": [], "改善": [], "轉弱": [], "落後": []}
    for m in members:
        by_q[m["q"]].append(m)
    pts = []
    lead = by_q["領先"]
    if lead:
        names = "、".join(f"{m['short']} {m['ticker']}" for m in lead)
        pts.append(f"{names} 在領先象限")
    imp = by_q["改善"]
    if imp:
        names = "、".join(f"{m['short']} {m['ticker']}" for m in imp)
        pts.append(f"{names} 在改善象限")
    weak = by_q["轉弱"] + by_q["落後"]
    if weak:
        segs = []
        for m in by_q["轉弱"]:
            segs.append(f"{m['short']} {m['ticker']} 轉弱（連 {m['streak']} 日）")
        lag = by_q["落後"]
        if lag:
            segs.append("、".join(f"{m['short']} {m['ticker']}" for m in lag)
                        + " 落後")
        pts.append("；".join(segs))
    return pts


def build_headline(latest, members, flags):
    parts = []
    r10 = _series(latest, "real10y")
    if r10:
        parts.append(f"實質利率分位 {r10['pctile']:.0f}")
    liq = latest.get("status", {}).get("liquidity", {}).get("label", "")
    if liq:
        parts.append(liq)
    seg1 = "、".join(parts)

    lead = [m["short"] for m in members if m["q"] == "領先"][:2]
    weak = [m["short"] for m in members if m["q"] == "轉弱"][:2]
    rseg = []
    if lead:
        rseg.append("、".join(lead) + "居領先")
    if weak:
        rseg.append("、".join(weak) + "走弱")
    seg2 = "，".join(rseg)

    conf = [f for f in flags if "持穩" in f["evidence"]]
    if conf:
        seg3 = "轉折：" + "；".join(f"{f['axis']} {f['from']}→{f['to']}"
                                                    for f in conf)
    elif flags:
        seg3 = "動能接近轉折（見轉折提醒）"
    else:
        seg3 = "無過門檻轉折"

    return "；".join(x for x in [seg1, seg2, seg3] if x) + "。"


def main():
    latest = _load("monitor/data/latest.json")
    radar = _load("rotation/data/radar.json")

    members = radar_members(radar)
    flagged = detect_reversals(members)
    flags = reversal_flags(flagged)

    pulse = {
        "schema": "home-pulse-v2",
        "monitor_as_of": latest.get("as_of"),
        "radar_as_of": radar.get("as_of"),
        "generated_at": radar.get("generated_at") or latest.get("generated_at"),
        "engine": "build_home_pulse.py",
        "headline": build_headline(latest, members, flags),
        "monitor": {"points": monitor_points(latest)},
        "radar": {"points": radar_points(members)},
        "reversal_flags": flags,
    }

    out = os.path.join(DOCS, "home", "pulse.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    content = json.dumps(pulse, ensure_ascii=False, indent=1) + "\n"
    old = None
    if os.path.exists(out):
        with open(out, encoding="utf-8") as fh:
            old = fh.read()
    if old == content:
        print("home-pulse: zero-churn (unchanged)")
        return
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"home-pulse: written ({len(flags)} reversal flag(s)) "
          f"monitor={pulse['monitor_as_of']} radar={pulse['radar_as_of']}")


if __name__ == "__main__":
    main()
