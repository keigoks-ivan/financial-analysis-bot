#!/usr/bin/env python3
"""第三條對照線（假設折衷組從 2024-01-02 起一直在跑）的種子檔建置。一次性：把 v7 回放結果轉成網站的假設線狀態。

輸入：~/v7-backtest/data/seat_supertrend_compare_2010-2026/<large|tw>/hypo_seed.json
      （v7 `python -m src.seat_supertrend_compare.hypo_seed <market>`；折衷組 sw4，2024-01-02 起連續回放）
輸出：美股 docs/engine/seat_st_hypo_seed.json、台股 docs/cockpit-tw/data/seat_st_hypo_seed_tw.json
      同內容再複製成工作狀態檔 seat_st_hypo.json／seat_st_hypo_tw.json（之後每週六 --ledger 才更新工作檔，種子檔不動）。

種子停在預估資料還有效的最後一個決策日（SEED_DECISION），之後由網站 seat_st.hypo_step 每週接續。
買進價一律改用網站同一條還原收盤序列在買進日的收盤價，才和停損線同尺度。
Usage: python3 scripts/build_seat_hypo_seed.py <us|tw> [--v7 路徑]"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from engine import seat_st  # noqa: E402

SEED_DECISION = "2026-10-30"
V7 = Path.home() / "v7-backtest/data/seat_supertrend_compare_2010-2026"
CFG = {
    "us": dict(v7="large", seed=ROOT / "docs/engine/seat_st_hypo_seed.json", work=ROOT / "docs/engine/seat_st_hypo.json",
               sfx="", label="美股看板"),
    "tw": dict(v7="tw", seed=ROOT / "docs/cockpit-tw/data/seat_st_hypo_seed_tw.json",
               work=ROOT / "docs/cockpit-tw/data/seat_st_hypo_tw.json", sfx=".TW", label="台股席位"),
}
REASON = {"盤整突破": "a", "停損線高過買進價": "b", "盤整突破與停損線同週": "ab"}
COMMON_DIFF = [
    "資料終點：回放價格到 2026-11-04，預估 EPS 序列只到 10-19（美）與 10-22（台）。最後一次補席在 2026-09-14（美）與 2026-10-12（台），之後沒有補席，預估資料變舊不影響這份名單。",
    "交易成本：2026-10-30 以前的淨值已扣回放設定的交易成本，之後由網站記帳，不扣成本。",
    "買進價：回放用成交價。種子改用網站還原收盤序列在買進日的收盤價，才和週線 Supertrend 停損線同一尺度。",
    "倉位：未切換的持股用時機燈倉位（0.5 或 1），已切換的滿倉，和網站相同。10-30 以後的倉位由網站燈號決定。",
]
SPECIFIC = {
    "us": [
        "補席排序：回放依預估 EPS 13 週變化由大到小補席。網站依 PEG 由低到高，並先過估值閘。",
        "資格：回放只含品質閘與成長閘。網站另有站上 52 週線、估值閘、市值帶、融券、180 天內 DD 迴避、體質拒絕，這些條件回放沒有，估值與 PEG 也沒有歷史資料可補。",
        "已切換持股的出池：回放在品質閘或成長閘不成立時賣出。網站看基本面的全部條件，包括上修否決、體質拒絕與衰退，比回放多看幾項。",
        "大盤多頭續抱：回放與網站相同，大盤在 200 日線之上時，沒切換的持股不因距新高轉紅而賣。",
    ],
    "tw": [
        "補席排序：回放依預估 EPS 13 週變化由大到小補席。網站用自己的排序，並先過網站的資格。",
        "資格：回放只含品質閘。網站另有融券、市值帶、180 天內 DD 迴避、體質拒絕，這些條件回放沒有，也沒有歷史資料可補。",
        "已切換持股的出池：回放在品質閘不成立時賣出。網站看基本面的全部條件。",
        "大盤空頭不補新席、看大盤切換出場：回放與網站相同。",
        "母體：回放的台股母體比網站 dd-screener 的台股名單寬，部分持股（例如崇越）不在網站名單內。網站看不到這類股票的基本面，假設線的處理是已切換的續抱到週線 Supertrend 翻空才賣，並占一席。",
    ],
}


def friday(d) -> str:
    d = pd.Timestamp(str(d)[:10])
    return (d + pd.Timedelta(days=(4 - d.weekday()) % 7 if d.weekday() <= 4 else -(d.weekday() - 4))).date().isoformat()


def _coef_after(events, tickers):
    """逐檔最後一次的倉位係數（買進／加碼／減碼事件的 why 字串 '係數a→b' 或 '係數a'）。"""
    last = {}
    for e in events:
        d, t, kind, why = e[0], e[1], e[2], e[-1]
        if d > SEED_DECISION or t not in tickers:
            continue
        if kind == "賣出":
            last.pop(t, None)
            continue
        m = re.search(r"係數([\d.]+)(?:→([\d.]+))?", str(why))
        if m:
            last[t] = float(m.group(2) or m.group(1))
    return last


def convert(raw: dict, market: str, loader, name_of=lambda t: t) -> dict:
    """純函式：v7 hypo_seed.json（dict）＋日線載入函式 → 種子 doc。"""
    cfg = CFG[market]
    sfx = cfg["sfx"]
    site = lambda t: f"{t}{sfx}"  # noqa: E731
    wk = [w for w in raw["weeks"] if w["date"] <= SEED_DECISION]
    final = wk[-1]
    held = list(final["held"])
    open_tr = {x["t"]: x for x in raw["trades"] if x["d1"] is None}
    coef = _coef_after(raw["events"], set(held))
    holdings, disc = {}, []
    for t in sorted(held, key=lambda x: (open_tr[x]["d0"], x)):
        tr = open_tr[t]
        daily = loader(site(t))
        comp = (seat_st.evaluate_holding(daily, tr["d0"], SEED_DECISION)
                if daily is not None and len(daily) else
                {"data_ok": False, "switched": False, "switch_week": None, "reason": None, "st_dir": None,
                 "st_line": None, "entry_price": None, "week": None})
        sw_replay = tr.get("sw_date") is not None and tr["sw_date"] <= SEED_DECISION
        h = {"entry_date": tr["d0"], "entry_price": comp["entry_price"], "switched": bool(sw_replay),
             "switch_week": friday(tr["sw_date"]) if sw_replay else None,
             "switch_reason": REASON.get(tr.get("sw_why")) if sw_replay else None,
             "st_dir": comp["st_dir"], "st_line": comp["st_line"], "week": comp["week"], "data_ok": comp["data_ok"],
             "name": tr.get("name") or name_of(t)}
        if bool(comp["switched"]) != bool(sw_replay):
            disc.append(f"{site(t)}：回放{'已' if sw_replay else '未'}切換，網站同一套規則算出{'已' if comp['switched'] else '未'}切換"
                        f"（網站版切換週 {comp['switch_week']}）")
        holdings[site(t)] = h
    positions = {site(t): (1.0 if holdings[site(t)]["switched"] else float(coef.get(t, 1.0))) for t in held}
    series = [{"week": raw["start"], "nav": 1.0, "ret": 0.0, "missing": [], "source": "replay"}]
    seen = set()
    for w in wk:
        lab = friday(w["date"])
        if lab in seen or lab > friday(SEED_DECISION):
            continue
        seen.add(lab)
        series.append({"week": lab, "nav": round(w["nav"], 6), "ret": round(w["nav"] / series[-1]["nav"] - 1.0, 6),
                       "missing": [], "source": "replay"})
    events = []
    for x in sorted(raw["trades"], key=lambda x: (x["d0"], x["t"])):
        events.append({"date": x["d0"], "ticker": site(x["t"]), "kind": "買進", "why": "回放補席"})
        if x["d1"] is not None and x["d1"] <= SEED_DECISION:
            events.append({"date": x["d1"], "ticker": site(x["t"]), "kind": "賣出", "why": x["why"], "ret": round(x["ret"], 4)})
    events.sort(key=lambda e: (e["date"], 0 if e["kind"] == "賣出" else 1, e["ticker"]))
    return {
        "schema": seat_st.HYPO_SCHEMA, "market": market, "label": cfg["label"], "start": raw["start"],
        "decision_date": SEED_DECISION, "as_of": SEED_DECISION,
        "roster": [site(t) for t in sorted(held, key=lambda x: (open_tr[x]["d0"], x))],
        "holdings": holdings, "events": events,
        "nav": {"series": series, "asof": friday(SEED_DECISION), "positions": positions},
        "seed": {"source": "v7 src/seat_supertrend_compare/hypo_seed.py（折衷組 sw4 回放）", "v7_price_end": raw["price_end"],
                 "decision_date": SEED_DECISION, "continues_from": "2026-11-07 週六席位排程（決策日 2026-11-06 收盤）",
                 "replay_nav_last": round(raw["nav_last"], 4), "replay_mdd": round(raw["mdd"], 4),
                 "differences": COMMON_DIFF + SPECIFIC[market], "switch_discrepancies": disc},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("market", choices=sorted(CFG))
    ap.add_argument("--v7", default=None)
    a = ap.parse_args()
    cfg = CFG[a.market]
    raw = json.loads(Path(a.v7 or V7 / cfg["v7"] / "hypo_seed.json").read_text(encoding="utf-8"))
    doc = convert(raw, a.market, seat_st.make_loader())
    txt = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    cfg["seed"].write_text(txt, encoding="utf-8")
    if not cfg["work"].exists():
        cfg["work"].write_text(txt, encoding="utf-8")
    print(a.market, doc["roster"], {t: (h["switched"], h["switch_week"]) for t, h in doc["holdings"].items()})
    print("discrepancies:", doc["seed"]["switch_discrepancies"])


if __name__ == "__main__":
    main()
