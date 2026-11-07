#!/usr/bin/env python3
"""Turn one day's answers into claim states, pillar states, and a verdict.

Shadow mode: reads files, writes only under data/jev/. Nothing on the site
changes. The tree (claims, weights, code rules) lives in
scripts/jev/questions_<TICKER>.json; the synthesis rules live at the top of
this file. Jev never decides the verdict; this program does, from the table
below.

Inputs
  scripts/jev/questions_<T>.json          the tree
  data/jev/answers/<T>/<date>.json        Jev claim answers (probe.py --evidence)
  data/jev/evidence/<T>/<date>.json       cleaned evidence (for review context, E4)
  docs/stock-dash/data/<T>.json           numbers for code-answered claims
  data/jev/state/<T>.json                 claim states carried from earlier days
  data/jev/reviews/<T>.json   (optional)  human decisions: {"A1": {"state": "是", "note": "...", "date": "2026-09-23"}}

Outputs
  data/jev/verdict/<T>/<date>.json
  data/jev/state/<T>.json (updated)

Usage
  python3 scripts/jev/synthesize.py --ticker NVDA [--date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "jev"
sys.path.insert(0, str(HERE))
from probe import NEG_CHOICES, POS_CHOICES, MID_CHOICES  # one list of choice meanings

# ---------------------------------------------------------------------------
# Synthesis rules. Every rule the verdict depends on is here.
#
# Claim states: 是 (holds), 否 (broken), 不明 (unknown).
# Risk claims (pillar E) read the other way: 否 = the bad thing has not
# happened, 是 = it happened and a human confirmed it, 待確認 = Jev or code
# raised it and a human has not confirmed. A risk never fires on its own.
#
# Pillar A-D:
#   any key claim 否                         -> 鬆動
#   any key claim 不明, or >= 2 load claims
#   in 否/不明                                -> 不明
#   otherwise                                -> 撐住   (support claims never move a pillar)
# Pillar E: any 是 -> 觸發; any 待確認 -> 待確認; else 無.
# Verdict:
#   E 觸發 or any A-D 鬆動   -> 迴避
#   E 待確認 or any A-D 不明 -> 觀望
#   otherwise                -> 進場
# ---------------------------------------------------------------------------
LOAD_UNKNOWN_LIMIT = 2
STATE_RANK = {"是": 0, "不明": 1, "否": 2}  # for combining a claim's code part and Jev part: worst wins
HYPERSCALERS = {"Microsoft": r"microsoft|azure", "Alphabet": r"alphabet|google",
                "Amazon": r"amazon|aws", "Meta": r"\bmeta\b"}
CUT_WORDS = r"\b(cut|cuts|trim|trims|lower|lowers|lowered|reduce|reduces|reduced|slash|slashes)\b"
CAPEX_WORDS = r"capex|capital spending|capital expenditure"


def load(p, default=None):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else default


def write(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1))
    tmp.replace(p)


# --------------------------- numbers for code claims ------------------------
def extract_metrics(dash):
    """Pull every number a code rule can ask for. Missing -> None (never guessed)."""
    jc = dash.get("full", {}).get("judgment_core", {})
    er = jc.get("eps_revision", {})
    eps_by_fy = {r["fy"]: r.get("current_estimate") for r in er.get("table", [])}
    rev = er.get("analyst_revisions_30d", {}).get("periods", {}).get("+1y", {})
    pve = jc.get("price_vs_eps", {})
    p3m = next((x for x in pve.get("periods", []) if x.get("label") == "近3個月"), {})
    bullet = pve.get("pe_bullet", {})
    close = dash.get("quote", {}).get("close")
    fr = jc.get("funnel_rank", {})
    qc = {c["key"]: c.get("value") for c in fr.get("quality_criteria", [])}
    gm = next((m.get("now") for m in dash.get("full", {}).get("moat_changes", []) if m.get("proxy") == "毛利率(LTM)"), None)
    quarters = jc.get("earnings_surprise", {}).get("surprises", {}).get("quarters", [])
    latest_q = max(quarters, key=lambda q: q["date"]) if quarters else None
    pe5 = bullet.get("pe_ntm_5y_avg_x")

    m = {
        "gm_ltm_pct": gm,
        "eps_by_fy": eps_by_fy,
        "analyst_up_minus_down_30d_next_fy": (rev["up_30d"] - rev["down_30d"]) if "up_30d" in rev else None,
        "fcf_margin_pct": qc.get("fcf"),
        "roic_ltm_pct": jc.get("roic_decomposition", {}).get("dupont", {}).get("roic_ltm_screener_pct"),
        "price_minus_eps_chg_3m_pp": (p3m["price_chg_pct"] - p3m["eps_fy_next_chg_pct"]) if p3m else None,
        "peg_live": bullet.get("live_peg"),
        "close": close,
        "pe_ntm_5y_avg_x": pe5,
        "latest_surprise": latest_q,
        # not in the data pack yet (need 10-Q segment and cash-flow detail)
        "dc_rev_yoy_pct": None, "networking_yoy_minus_dc_yoy_pp": None, "dso_change_days_yoy": None,
        "sbc_pct_rev": None, "inventory_writedown_usd_q": None,
        "hyperscaler_capex_2027_yoy_pct": None, "supply_commitments_qoq_usd": None,
    }
    flags = []
    if qc.get("peg") is not None and bullet.get("live_peg") is not None and abs(qc["peg"] - bullet["live_peg"]) > 0.05:
        flags.append(f"PEG 兩個口徑不一致：排序用 {qc['peg']}，即時算 {bullet['live_peg']}。D3 用即時算的。")
    return m, flags


def metric_value(rule, m, today, due, pillar_states):
    name = rule["metric"]
    if name == "eps_next_fy":
        return m["eps_by_fy"].get(rule.get("fy", "FY28"))
    if name == "implied_eps_minus_consensus":
        eps = m["eps_by_fy"].get("FY28")
        if None in (m["close"], m["pe_ntm_5y_avg_x"], eps):
            return None
        return m["close"] / (m["pe_ntm_5y_avg_x"] / 2) - eps
    if name == "eps_surprise_latest_pct":
        q = m["latest_surprise"]
        return q["surprise_pct"] if q and due and q["date"] >= due else None
    if name == "pillar_A_not_loosened":
        return pillar_states.get("A") != "鬆動" if "A" in pillar_states else None
    return m.get(name)


def compare(v, op, x):
    return {">": v > x, ">=": v >= x, "<": v < x, "<=": v <= x, "==": v == x}[op]


def eval_code(claim, m, today, pillar_states):
    rule, due = claim["rule"], claim.get("due")
    if rule.get("resolve_at_due") and due and today < due:
        return "是", f"未到期（{due}），推定成立"
    v = metric_value(rule, m, today, due, pillar_states)
    if v is None:
        return "不明", f"缺資料：{rule['metric']}"
    x = rule.get("value_at_due", rule["value"]) if (due and today >= due) else rule["value"]
    ok = compare(v, rule["op"], x)
    shown = f"{v:.2f}" if isinstance(v, float) else str(v)
    return ("是" if ok else "否"), f"{rule['metric']} = {shown}，門檻 {rule['op']} {x}"


# --------------------------- Jev claims -------------------------------------
def eval_jev(claim, ans, prior, review, th, today):
    """Returns (state, basis, sticky). Sticky states wait for a human."""
    risk = claim["weight"] == "risk"
    if review:  # a human decision stands until a later high-confidence break
        state, basis, sticky = review["state"], f"人工判定（{review.get('date', '')}）：{review.get('note', '')}", False
        if ans and ans["type"] == "choice" and ans["choice"] in NEG_CHOICES \
                and ans["confidence"] >= th["choice_auto_flip_confidence"] and today > review.get("date", ""):
            return "否", f"Jev 高信心翻掉（{ans['choice']} {ans['confidence']:.2f}），晚於人工判定", True
        return state, basis, sticky
    if prior and prior.get("sticky"):
        return prior["state"], prior["basis"], True
    if ans is None:
        return prior["state"], prior["basis"], False

    if ans["type"] == "noul":
        p = ans["noul"]
        if risk:
            if p >= th["risk_noul_alert"]:
                return "待確認", f"Jev 警示 {p:.2f}，要人確認", True
            if p >= th["risk_noul_review"]:
                return "待確認", f"Jev {p:.2f}，送 Opus 複核", True
            return prior["state"], prior["basis"], False
        if p >= th["choice_auto_flip_confidence"]:
            return "不明", f"新聞可能有數字了（{p:.2f}），要人填", True
        return prior["state"], prior["basis"], False

    c, conf = ans["choice"], ans["confidence"]
    if c in NEG_CHOICES:
        if conf >= th["choice_auto_flip_confidence"]:
            return "否", f"Jev 翻掉：{c}（信心 {conf:.2f}）", True
        if conf >= th["choice_review_confidence"]:
            return "不明", f"Jev 偏向翻掉：{c}（信心 {conf:.2f}），送 Opus 複核", True
        return "不明", f"Jev 偏向翻掉：{c}（信心 {conf:.2f}），太低，交人", True
    if c in MID_CHOICES:
        return "不明", f"中間狀態：{c}（信心 {conf:.2f}）", False
    if c in POS_CHOICES:
        if conf < th["choice_review_confidence"]:  # a weak "holds" confirms nothing
            return prior["state"], prior["basis"], False
        return "是", f"Jev 再確認：{c}（信心 {conf:.2f}）", False
    return prior["state"], prior["basis"], False


def initial(claim):
    if claim["weight"] == "risk":
        return {"state": "否", "basis": "初始：未發生", "sticky": False}
    s = claim.get("initial_state", "是")
    return {"state": s, "basis": "初始：要人填數字" if s == "不明" else "初始：還沒被推翻，推定成立", "sticky": False}


# --------------------------- pillars and verdict ----------------------------
def pillar_state(claims, states):
    keys = [c for c in claims if c["weight"] == "key"]
    loads = [c for c in claims if c["weight"] == "load"]
    key_bad = [c["id"] for c in keys if states[c["id"]]["state"] == "否"]
    key_unk = [c["id"] for c in keys if states[c["id"]]["state"] == "不明"]
    load_bad = [c["id"] for c in loads if states[c["id"]]["state"] in ("否", "不明")]
    if key_bad:
        return "鬆動", key_bad
    if key_unk or len(load_bad) >= LOAD_UNKNOWN_LIMIT:
        return "不明", key_unk + (load_bad if len(load_bad) >= LOAD_UNKNOWN_LIMIT else [])
    return "撐住", []


def hyperscalers_cutting(evidence):
    names = set()
    for it in (evidence or {}).get("items", []):
        if "B6" not in it.get("bearing", []):
            continue
        text = f"{it['headline']} {it.get('text', '')}".lower()
        if re.search(CUT_WORDS, text) and re.search(CAPEX_WORDS, text):
            names |= {n for n, pat in HYPERSCALERS.items() if re.search(pat, text)}
    return sorted(names)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--date", default=None, help="defaults to the latest answers file")
    a = ap.parse_args()
    t = a.ticker

    spec = load(HERE / f"questions_{t}.json")
    ans_dir = DATA / "answers" / t
    date = a.date or (sorted(p.stem for p in ans_dir.glob("*.json"))[-1] if ans_dir.exists() else None)
    if not date:
        sys.exit(f"no Jev answers under {ans_dir}; run probe.py --evidence first")
    answers = (load(ans_dir / f"{date}.json") or {}).get("answers", {})
    evidence = load(DATA / "evidence" / t / f"{date}.json")
    dash = load(ROOT / "docs" / "stock-dash" / "data" / f"{t}.json") or {}
    prior_all = (load(DATA / "state" / f"{t}.json") or {}).get("claims", {})
    reviews = load(DATA / "reviews" / f"{t}.json") or {}
    th = spec["thresholds"]
    m, flags = extract_metrics(dash)
    claims = spec["claims"]
    by_pillar = {}
    for c in claims:
        by_pillar.setdefault(c["pillar"], []).append(c)

    states, pillar = {}, {}
    order = ["A", "B", "C", "D", "E"]  # D4 reads pillar A, so A goes first
    for p in order:
        for c in by_pillar.get(p, []):
            prior = prior_all.get(c["id"]) or initial(c)
            parts = []
            if "rule" in c and c["id"] != "E4":
                parts.append(eval_code(c, m, date, pillar) + (False,))
            if "jev" in c:
                parts.append(eval_jev(c, answers.get(c["id"]), prior, reviews.get(c["id"]), th, date))
            if c["id"] == "E4":
                cutting = hyperscalers_cutting(evidence) if answers.get("B6", {}).get("choice") == "cut" else []
                if len(cutting) >= c["rule"]["value"]:
                    parts.append(("待確認", f"新聞裡砍資本支出的有：{', '.join(cutting)}，要人確認", True))
                else:
                    parts.append((prior["state"] if prior["state"] != "待確認" else "否",
                                  f"砍資本支出的 hyperscaler：{len(cutting)} 家", False))
            if not parts:
                parts.append((prior["state"], prior["basis"], prior.get("sticky", False)))
            if c["weight"] == "risk":
                rank = {"否": 0, "待確認": 1, "是": 2}
                st = max(parts, key=lambda x: rank[x[0]])
            else:
                st = max(parts, key=lambda x: STATE_RANK[x[0]])
            states[c["id"]] = {"state": st[0], "basis": " ／ ".join(x[1] for x in parts), "sticky": any(x[2] for x in parts),
                               "zh": c["zh"], "weight": c["weight"], "pillar": p}
        if p != "E":
            pillar[p] = pillar_state(by_pillar.get(p, []), states)[0]

    pillars = {}
    for p in ["A", "B", "C", "D"]:
        s, drivers = pillar_state(by_pillar.get(p, []), states)
        pillars[p] = {"state": s, "drivers": drivers}
    e_states = [states[c["id"]]["state"] for c in by_pillar.get("E", [])]
    e = "觸發" if "是" in e_states else ("待確認" if "待確認" in e_states else "無")
    pillars["E"] = {"state": e, "drivers": [c["id"] for c in by_pillar.get("E", []) if states[c["id"]]["state"] != "否"]}

    ad = [pillars[p]["state"] for p in "ABCD"]
    if e == "觸發" or "鬆動" in ad:
        verdict = "迴避"
    elif e == "待確認" or "不明" in ad:
        verdict = "觀望"
    else:
        verdict = "進場"
    drivers = [d for p in "ABCDE" for d in pillars[p]["drivers"]]

    # what a person needs to look at, with the evidence Jev saw for that claim
    items = (evidence or {}).get("items", [])
    queue = []
    for cid, s in states.items():
        if s["sticky"] and s["state"] in ("不明", "待確認", "否"):
            ev = [f"{it['headline']}（{it['source']}）" for it in items if cid in it.get("bearing", [])][:3]
            queue.append({"id": cid, "zh": s["zh"], "why": s["basis"], "evidence": ev})
    gaps = [cid for cid, s in states.items() if "缺資料" in s["basis"]]
    unknown_news = {u["id"]: [it["headline"] for it in items if u["id"] in it.get("bearing", [])][:3]
                    for u in spec.get("unknowns", []) if "jev" in u}

    out = {"schema": "claim-tree-verdict-v0", "ticker": t, "date": date, "metrics_as_of": dash.get("as_of"),
           "verdict": verdict, "drivers": drivers, "pillars": pillars, "claims": states,
           "review_queue": queue, "data_gaps": gaps, "unknowns_news": unknown_news, "flags": flags,
           "note": "shadow mode; verdict computed by rules in scripts/jev/synthesize.py, not by a model"}
    write(DATA / "verdict" / t / f"{date}.json", out)
    write(DATA / "state" / f"{t}.json", {"ticker": t, "updated": date,
          "claims": {k: {"state": v["state"], "basis": v["basis"], "sticky": v["sticky"]} for k, v in states.items()}})

    # ---- print
    names = {"A": "護城河", "B": "成長對預期", "C": "賺的是不是真錢", "D": "現價划不划算", "E": "推翻一切的風險"}
    print(f"{t}  {date}  數字截至 {dash.get('as_of')}   判決：{verdict}")
    print(f"卡住判決的主張：{', '.join(drivers) if drivers else '無'}\n")
    for p in "ABCDE":
        print(f"[{p}] {names[p]}：{pillars[p]['state']}" + (f"   ← {', '.join(pillars[p]['drivers'])}" if pillars[p]["drivers"] else ""))
        for c in by_pillar.get(p, []):
            s = states[c["id"]]
            mark = "＊" if s["sticky"] else "  "
            print(f"   {mark}{c['id']:3} {c['weight']:7} {s['state']:3}  {c['zh']}")
            print(f"        {s['basis']}")
    if queue:
        print("\n要人看的（＊）：")
        for q in queue:
            print(f"  {q['id']} {q['zh']}：{q['why']}")
            for e_ in q["evidence"]:
                print(f"      · {e_}")
    if gaps:
        print(f"\n缺資料：{', '.join(gaps)}")
    for u, hs in unknown_news.items():
        if hs:
            print(f"\n不知道的事 {u} 今天有相關新聞：")
            for h in hs:
                print(f"      · {h}")
    for f in flags:
        print(f"\n注意：{f}")
    print(f"\nwrote {DATA / 'verdict' / t / (date + '.json')}")


if __name__ == "__main__":
    main()
