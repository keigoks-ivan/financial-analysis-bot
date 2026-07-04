#!/usr/bin/env python3
"""
settle_outcomes.py — 決策帳本的機械結算（價格對答案）。

把 decisions.jsonl 的每筆裁決 × data/weekly_cache 週線，結算成 forward return：
  - 固定視窗：+30 / +91 / +182 / +365 天（日曆日，取 ≤ 目標日的最近週線 close）
  - to-date：至 cache 最新一根週線
  - p0 / p1 同用 weekly_cache 調整後序列（split 一致）；price_at_decision 只做 sanity flag

輸出 knowledge/settlement.json（衍生物，gitignore，本地重算）。
q.py --calibration 消費本檔：無檔或比 decisions.jsonl 舊會自動重跑。

設計原則：
  - 「說觀望／迴避」同樣結算 —— 錯過成本（miss cost）與套牢成本同權重對答案。
  - 機械結算不取代 ledger.manual.jsonl 的人工 outcome（verdict_held / lesson 是人的判斷），
    兩者在 --calibration 並列呈現。
"""
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

KDIR = Path(__file__).resolve().parent
ROOT = KDIR.parent
DECISIONS = KDIR / "decisions.jsonl"
CACHE_DIR = ROOT / "data" / "weekly_cache"
OUT = KDIR / "settlement.json"

# decisions entity → weekly_cache 檔名（dd-meta ticker 慣例與 cache 命名不一致者）
ALIAS = {
    "5274.TW": "5274.TWO",
    "8299.TW": "8299.TWO",
    "AENA": "AENA.MC",
    "BESI": "BESI.AS",
    "RMS": "RMS.PA",
    "SU": "SU.PA",
    "LVMH": "MC.PA",
    "ABB": "ABBNY",
}

HORIZONS = {"h30": 30, "h91": 91, "h182": 182, "h365": 365}


def _load_decisions():
    if not DECISIONS.exists():
        subprocess.run([sys.executable, str(KDIR / "build_knowledge.py")], check=True)
    return [json.loads(l) for l in DECISIONS.read_text(encoding="utf-8").splitlines() if l.strip()]


def _bars(ticker, _cache={}):
    if ticker in _cache:
        return _cache[ticker]
    p = CACHE_DIR / f"{ALIAS.get(ticker, ticker)}.json"
    bars = None
    if p.exists():
        try:
            raw = json.loads(p.read_text(encoding="utf-8")).get("weekly_bars") or []
            bars = [(b["week_end"], b["close"]) for b in raw if b.get("close")]
        except (json.JSONDecodeError, KeyError):
            bars = None
    _cache[ticker] = bars
    return bars


def _close_at_or_before(bars, ymd):
    """最近一根 week_end ≤ ymd 的 close；無則 None。bars 已按日期升冪。"""
    best = None
    for d, c in bars:
        if d <= ymd:
            best = (d, c)
        else:
            break
    return best


def _plus_days(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


def _days_between(a, b):
    ya, ma, da = map(int, a.split("-"))
    yb, mb, db = map(int, b.split("-"))
    return (date(yb, mb, db) - date(ya, ma, da)).days


def settle(decisions):
    rows, skipped = [], []
    for r in decisions:
        if r.get("kind") != "decision" or r.get("entity_type") != "company":
            continue
        d0, ent = r.get("date"), r.get("entity")
        if not (d0 and ent):
            skipped.append((r.get("id"), "no_date_or_entity"))
            continue
        bars = _bars(ent)
        if not bars:
            skipped.append((r["id"], "no_cache"))
            continue
        at0 = _close_at_or_before(bars, d0)
        if not at0:
            skipped.append((r["id"], "before_cache_start"))
            continue
        p0_date, p0 = at0
        last_date, p_last = bars[-1]

        flags = []
        if _days_between(p0_date, d0) > 14:
            flags.append("stale_p0")  # 裁決日在 cache 最新 bar 之後太久
        pad = r.get("price_at_decision")
        if pad and abs(p0 / pad - 1) > 0.25:
            flags.append("px_mismatch")  # split / 幣別（ADR vs 原市場）/ 調整落差，序列內部仍一致

        row = {
            "id": r["id"],
            "entity": ent,
            "date": d0,
            "verdict": r.get("verdict"),
            "grade": r.get("fundamental_grade"),
            "p0": round(p0, 4),
            "flags": flags,
            "to_date_pct": round((p_last / p0 - 1) * 100, 2),
            "days": _days_between(d0, last_date),
            "as_of": last_date,
        }
        for key, n in HORIZONS.items():
            tgt = _plus_days(d0, n)
            if last_date >= tgt:
                _, px = _close_at_or_before(bars, tgt)
                row[key] = round((px / p0 - 1) * 100, 2)
            else:
                row[key] = None  # 視窗未到期
        rows.append(row)
    return rows, skipped


def main():
    decisions = _load_decisions()
    rows, skipped = settle(decisions)
    as_of = max((r["as_of"] for r in rows), default=None)
    out = {
        "schema": "settlement-v1",
        "as_of": as_of,
        "n_settled": len(rows),
        "n_skipped": len(skipped),
        "skipped": skipped,
        "horizons_days": HORIZONS,
        "rows": rows,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    matured = sum(1 for r in rows if r["h91"] is not None)
    print(f"settlement.json: {len(rows)} 筆結算（h91 到期 {matured}）、{len(skipped)} 筆跳過，as_of {as_of}")
    if skipped:
        from collections import Counter
        print("  跳過原因：", dict(Counter(reason for _, reason in skipped)))


if __name__ == "__main__":
    main()
