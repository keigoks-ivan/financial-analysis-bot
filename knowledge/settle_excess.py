#!/usr/bin/env python3
"""
settle_excess.py — v13+ DD 裁決的「相對基準超額報酬」結算（2026-10 校準輪新增）。

settle_outcomes.py 只算絕對報酬；本檔補基準：
  美股 -> QQQ；.TW/.TWO -> 0050.TW；.T -> ^N225；.KL -> ^KLSE；.AX -> ^AXJO；.SW -> ^SSMI
價格：個股用 data/weekly_cache 週線（同 settle_outcomes）；基準用 yfinance 日線
（auto_adjust）快取在 data/benchmarks_daily.json（缺檔或 --refresh 才抓）。
基準取「個股實際用到的那根週線日期」當日或之前最近一個收盤，兩端對齊。
離散比較（超額>0、門檻）一律在整數 bps 空間做，避免浮點邊界誤差。

輸出 knowledge/settlement_excess.json（衍生物，gitignore）。
  python3.12 knowledge/settle_excess.py [--refresh]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import settle_outcomes as so  # noqa: E402

KDIR = Path(__file__).resolve().parent
ROOT = KDIR.parent
BENCH_FILE = ROOT / "data" / "benchmarks_daily.json"
OUT = KDIR / "settlement_excess.json"
DECISIONS = KDIR / "decisions.jsonl"
DD_DIR = ROOT / "docs" / "dd"

BENCH_TICKERS = ["QQQ", "0050.TW", "^N225", "^KLSE", "^AXJO", "^SSMI"]
HZ = {"h91": 91, "h182": 182}


def bench_for(entity):
    m = re.search(r"\.([A-Z]+)$", entity)
    suf = m.group(1) if m else ""
    return {"TW": "0050.TW", "TWO": "0050.TW", "T": "^N225", "KL": "^KLSE",
            "AX": "^AXJO", "SW": "^SSMI"}.get(suf, "QQQ")


def load_bench(refresh=False):
    if BENCH_FILE.exists() and not refresh:
        return json.loads(BENCH_FILE.read_text())
    import yfinance as yf
    out = {}
    for t in BENCH_TICKERS:
        df = yf.download(t, start="2025-12-01", auto_adjust=True, progress=False)
        if df is None or df.empty:
            print("benchmark fetch failed:", t, file=sys.stderr)
            continue
        c = df["Close"]
        if hasattr(c, "columns"):
            c = c.iloc[:, 0]
        out[t] = [[str(i.date()), float(v)] for i, v in c.dropna().items()]
    BENCH_FILE.write_text(json.dumps({"fetched": date.today().isoformat(), "series": out}))
    return json.loads(BENCH_FILE.read_text())


def at_or_before(series, ymd):
    best = None
    for d, c in series:
        if d <= ymd:
            best = (d, c)
        else:
            break
    return best


def bps(a, b):
    return int(round((b / a - 1) * 10000))


def pipeline_of(rec):
    sr = rec.get("source_report")
    if not sr:
        return None
    p = ROOT / sr
    if not p.exists():
        return None
    t = p.read_text(errors="ignore")
    m = re.search(r'"pipeline"\s*:\s*"([^"]+)"', t[:200000])
    return m.group(1) if m else None


def gen_of(rec, pipeline):
    sch = str(rec.get("schema") or "")
    if sch.startswith(("v13", "v14")):
        return "v13-14"
    if pipeline and rec["date"] >= "2026-09-17":
        return "v20"
    if pipeline:
        return "v17-19"
    return "v15"


def main():
    refresh = "--refresh" in sys.argv
    bench = load_bench(refresh)["series"]
    decs = [json.loads(l) for l in DECISIONS.read_text().splitlines() if l.strip()]
    rows = []
    for r in decs:
        if r.get("kind") != "decision" or r.get("entity_type") != "company":
            continue
        if not r.get("verdict") or r.get("source") != "dd-meta":
            continue
        ent, d0 = r["entity"], r["date"]
        bars = so._bars(ent)
        bser = bench.get(bench_for(ent))
        if not bars or not bser:
            continue
        at0 = so._close_at_or_before(bars, d0)
        if not at0:
            continue
        p0d, p0 = at0
        b0 = at_or_before(bser, p0d)
        if not b0:
            continue
        last_d, last_c = bars[-1]
        pipe = pipeline_of(r)
        verdict = r["verdict"]
        if verdict.startswith("進場"):
            verdict_n = "進場"
        else:
            verdict_n = verdict
        row = {"id": r["id"], "entity": ent, "date": d0, "verdict": verdict_n,
               "verdict_raw": verdict, "role": r.get("role"), "grade": r.get("fundamental_grade"),
               "schema": r.get("schema"), "pipeline": pipe, "gen": gen_of(r, pipe),
               "bench": bench_for(ent), "p0_date": p0d}
        wins = dict(HZ)
        for key, n in list(wins.items()) + [("td", None)]:
            if n is None:
                pd, px = last_d, last_c
            else:
                tgt = so._plus_days(d0, n)
                if last_d < tgt:
                    row[key] = None
                    continue
                pd, px = so._close_at_or_before(bars, tgt)
            bx = at_or_before(bser, pd)
            if not bx:
                row[key] = None
                continue
            s, b = bps(p0, px), bps(b0[1], bx[1])
            row[key] = {"abs_bps": s, "bench_bps": b, "ex_bps": s - b, "end": pd}
        row["days"] = so._days_between(d0, last_d)
        rows.append(row)
    OUT.write_text(json.dumps({"as_of": bars[-1][0] if rows else None, "n": len(rows), "rows": rows},
                              ensure_ascii=False, indent=1))
    print(f"settlement_excess.json: {len(rows)} 筆")


if __name__ == "__main__":
    main()
