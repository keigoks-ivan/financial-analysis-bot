#!/usr/bin/env python3
"""CEO 關注清單「幕僚備忘」的證據包與機械檢查（skill `horizon-memo`）。

  python3 scripts/check_horizon_memo.py --brief   # 印出寫備忘要讀的證據包（本週 vs 7 天前）
  python3 scripts/check_horizon_memo.py           # 檢查 docs/horizon/data/memo.json，FAIL 回非零

檢查項目：
  1. schema 欄位齊全、長度上限
  2. data_as_of 等於 horizon.json 的 as_of
  3. refs 路徑都解得到非空值（far.<題目 id>.… 用題目 id 取，其餘照 key 走）
  4. 文字裡帶小數點的數字，都要在 horizon.json 或 history.json 找得到（照顯示位數四捨五入比對）
  5. 不得出現買賣指令用語、破折號
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "horizon" / "data"

BANNED = ["買進", "買入", "賣出", "加碼", "減碼", "建倉", "清倉", "出場", "進場", "停損", "停利",
          "目標價", "應該買", "應該賣", "建議買", "建議賣", "——"]
LIMITS = {"headline": 40, "changed": 90, "chain": 180, "question": 60, "why": 180, "blind": 140}


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def resolve(doc, path):
    cur = doc
    parts = path.split(".")
    i = 0
    while i < len(parts):
        k = parts[i]
        if isinstance(cur, list):
            if k.isdigit():
                cur = cur[int(k)] if int(k) < len(cur) else None
            else:  # 用 id 找清單裡的元素（far.ai_compute）
                cur = next((x for x in cur if isinstance(x, dict) and x.get("id") == k), None)
        elif isinstance(cur, dict):
            cur = cur.get(k)
        else:
            return None
        if cur is None:
            return None
        i += 1
    return cur


def all_numbers(o, out):
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        out.add(float(o))
    elif isinstance(o, str):
        for m in re.findall(r"-?\d+\.\d+", o):
            out.add(float(m))
    elif isinstance(o, dict):
        for v in o.values():
            all_numbers(v, out)
    elif isinstance(o, list):
        for v in o:
            all_numbers(v, out)


def brief():
    h = load(DATA / "horizon.json")
    hist = load(DATA / "history.json")["rows"]
    today = date.fromisoformat(h["as_of"])
    olds = [d for d in hist if date.fromisoformat(d) <= today - timedelta(days=7)]
    week_ago = hist[max(olds)] if olds else {}
    print(f"# 證據包　資料日 {h['as_of']}　對照 {max(olds) if olds else '（還沒有 7 天前的紀錄）'}\n")
    print("## 今天先看")
    for t in h["top"]:
        print(f"- {t['text']}")
    print("\n## 九題（現在｜7 天前）")
    for f in h["far"]:
        m = f["metrics"]
        now = (hist.get(h["as_of"]) or {}).get(f["id"], {})
        then = week_ago.get(f["id"], {})
        lean = (f.get("lean") or {}).get("text")
        print(f"### {f['id']}　{f['q']}　市場目前：{lean}　警戒線：{f['alarm_def']['text']}（{'已碰到' if (f['alarm'] or {}).get('hit') else '未碰到'}）")
        if m.get("gain"):
            g = m["gain"]
            print(f"  受惠籃：EPS 上修 {g.get('eps_rev_3m')}｜三年成長預估 {g.get('growth_3y')}（月變 {g.get('growth_3y_chg')}）"
                  f"｜自有資金撐得起 {g.get('self_funded')}｜一年對大盤 {g.get('rs_52w')}｜半年對大盤 {g.get('rs_26w')}")
        if m.get("lose"):
            l_ = m["lose"]
            print(f"  對照籃：EPS 上修 {l_.get('eps_rev_3m')}｜三年成長預估 {l_.get('growth_3y')}｜一年對大盤 {l_.get('rs_52w')}")
        if m.get("series"):
            print("  序列：" + "｜".join(f"{k} {v}" for k, v in m["series"].items() if not k.endswith("_as_of")))
        if then:
            diffs = [f"{k} {then.get(k)}→{now.get(k)}" for k in now if k in then and then.get(k) != now.get(k)]
            print("  7 天變化：" + ("、".join(diffs) if diffs else "沒變"))
        print(f"  席位在這題：{'、'.join(f['my_seats']) or '沒有'}｜一起動：{f.get('moves_with')}")
        print(f"  最新故事線：{[e['title'] for e in f.get('evidence_recent', [])[:4]]}")
    print("\n## 幾個押注")
    for b in h["bets"]:
        print(f"- {b['qids']} 平均相關 {b['avg_corr']} 席位 {b['seats']}")
    print("\n## 方法還管不管用")
    for s in h["strategy"]:
        print(f"- {s['label']} {s['window']}：{s['ret']} vs {s['bench_label']} {s['bench']}（差 {s['diff']}）")
    print("\n## 最怕什麼")
    for r in h["risks"]:
        print(f"- {r['title']}：{r['value']}")
    for s in h["stress"]:
        print(f"- 壓力 {s['label']}：SPY {s['spy']}｜實單美不動 {s['live_us_hold']}／照規則 {s['live_us_rule']}"
              f"｜實單台不動 {s['live_tw_hold']}／照規則 {s['live_tw_rule']}｜席位 {s['seats']}")
    print("\n## 盲點（沒配到任何一題的故事線）")
    for b in h["blind_spots"]:
        print(f"- {b['title']}（{b['days']} 天，{b['heat']}）")
    print("\n## 今天要處理")
    for x in h["fires_out"] + h["fires_co"]:
        print(f"- [{x['side']}] {x['text']}")
    print("\n## 方向一致嗎")
    for c in h["conflicts"]:
        print(f"- {c}")
    print("\n## 60 天內（前 15 件）")
    for u in h["upcoming"][:15]:
        print(f"- {u['date']} [{u['side']}] {u['label']}")
    if h.get("market_headline"):
        print(f"\n## 市況判讀（{h.get('market_read_as_of')}）\n{h['market_headline']}")
    memo_p = DATA / "memo.json"
    if memo_p.exists():
        m = load(memo_p)
        print(f"\n## 上一份備忘（{m.get('as_of')}）\n{m.get('headline')}\n等你決定：{(m.get('decision') or {}).get('question')}")


def check():
    errs = []
    h = load(DATA / "horizon.json")
    try:
        m = load(DATA / "memo.json")
    except Exception as e:  # noqa: BLE001
        print(f"FAIL memo.json 讀不到：{e}")
        return 1
    if m.get("schema") != "horizon-memo-v1":
        errs.append("schema 不是 horizon-memo-v1")
    if m.get("data_as_of") != h["as_of"]:
        errs.append(f"data_as_of {m.get('data_as_of')} ≠ horizon.json {h['as_of']}")
    fields = [("headline", m.get("headline"), LIMITS["headline"])]
    ch = m.get("changed") or []
    if not 2 <= len(ch) <= 4:
        errs.append(f"changed 要 2～4 條，現在 {len(ch)}")
    fields += [(f"changed[{i}]", c.get("text"), LIMITS["changed"]) for i, c in enumerate(ch)]
    if m.get("chain"):
        fields.append(("chain", m["chain"], LIMITS["chain"]))
    dec = m.get("decision") or {}
    fields += [("decision.question", dec.get("question"), LIMITS["question"]),
               ("decision.why", dec.get("why"), LIMITS["why"]),
               ("blind_spot.text", (m.get("blind_spot") or {}).get("text"), LIMITS["blind"])]
    for name, text, lim in fields:
        if not text:
            errs.append(f"{name} 空白")
            continue
        if len(text) > lim:
            errs.append(f"{name} 超過 {lim} 字（{len(text)}）")
        for w in BANNED:
            if w in text:
                errs.append(f"{name} 出現禁用詞「{w}」")
    if dec.get("question") and not dec["question"].rstrip().endswith(("？", "?")):
        errs.append("decision.question 要是問句")
    # refs
    ref_lists = [("changed", r) for c in ch for r in (c.get("refs") or [])] + \
        [("decision", r) for r in dec.get("refs") or []] + \
        [("blind_spot", r) for r in (m.get("blind_spot") or {}).get("refs") or []]
    if not ref_lists:
        errs.append("沒有任何 refs")
    for where, r in ref_lists:
        if resolve(h, r) is None:
            errs.append(f"{where} ref 解不到：{r}")
    # 數字
    known = set()
    all_numbers(h, known)
    try:
        all_numbers(load(DATA / "history.json"), known)
    except Exception:  # noqa: BLE001
        pass
    for name, text, _ in fields:
        for s in re.findall(r"\d+\.\d+", text or ""):
            dec_n = len(s.split(".")[1])
            v = float(s)
            if not any(abs(round(abs(k), dec_n) - v) < 1e-9 for k in known):
                errs.append(f"{name} 的數字 {s} 在資料裡找不到")
    if errs:
        print("FAIL")
        for e in errs:
            print(" -", e)
        return 1
    print(f"PASS memo {m.get('as_of')}（資料日 {m.get('data_as_of')}）")
    return 0


if __name__ == "__main__":
    if "--brief" in sys.argv:
        brief()
        sys.exit(0)
    sys.exit(check())
