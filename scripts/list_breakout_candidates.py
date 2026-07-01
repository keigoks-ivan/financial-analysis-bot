#!/usr/bin/env python3
"""List multi-bagger breakout candidates from ID related_tickers (discovery pool).

Scans docs/id/ID_*.html id-meta blocks, collects depth-🔴 related tickers, and
cross-checks against the existing DD universe (docs/dd/DD_*.html). The output
is the "🔴 core beneficiary with no DD yet" discovery pool — the names the ID
layer has already surfaced but which never entered the dd-screener funnel
(screener universe = DD'd tickers only).

Ranking uses the industry-analyst v2.4 fields when present:
  - id-meta demand_5y_multiple  (industry-level blast radius; ≥2 = 爆發獵場)
  - related_tickers[].purity_pct / mcap_bucket (ticker-level leverage;
    multi-baggers cluster in high-purity × mid/small)
Legacy IDs (pre-v2.4) lack these fields — those rows rank by 🔴-appearance
count + ID conviction only and are marked so the gap is visible, not silent.

Usage:
  python3 scripts/list_breakout_candidates.py            # 無 DD 的 🔴 候選池
  python3 scripts/list_breakout_candidates.py --all      # 含已有 DD 的 🔴
  python3 scripts/list_breakout_candidates.py --json     # machine-readable
  python3 scripts/list_breakout_candidates.py --top 30   # 只列前 N
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"
DD_DIR = ROOT / "docs" / "dd"

ID_META_RE = re.compile(
    r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
DD_FILE_RE = re.compile(r"^DD_([A-Za-z0-9.\-]+)_\d{8}\.html$")

MCAP_ORDER = {"small": 0, "mid": 1, "large": 2, "mega": 3}
CONVICTION_ORDER = {"high": 0, "mid": 1, "low": 2}


def load_id_metas():
    metas = []
    for p in sorted(ID_DIR.glob("ID_*.html")):
        if p.name.endswith("_full.html"):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        m = ID_META_RE.search(text)
        if not m:
            continue
        try:
            meta = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        meta["_file"] = p.name
        metas.append(meta)
    return metas


def dd_universe():
    tickers = set()
    for p in DD_DIR.glob("DD_*.html"):
        m = DD_FILE_RE.match(p.name)
        if m:
            tickers.add(m.group(1).upper())
    return tickers


def collect(metas, dd_set, include_dd):
    pool = {}
    for meta in metas:
        theme = meta.get("theme", meta["_file"])
        conviction = (meta.get("conviction") or "").lower() or None
        demand_mult = meta.get("demand_5y_multiple")
        for t in meta.get("related_tickers") or []:
            if not isinstance(t, dict) or t.get("depth") != "🔴":
                continue
            tk = str(t.get("ticker", "")).upper()
            if not tk:
                continue
            has_dd = tk in dd_set
            if has_dd and not include_dd:
                continue
            row = pool.setdefault(tk, {
                "ticker": tk,
                "has_dd": has_dd,
                "themes": [],
                "core_count": 0,
                "purity_pct": None,
                "mcap_bucket": None,
                "best_demand_mult": None,
                "best_conviction": None,
                "roles": [],
            })
            row["core_count"] += 1
            row["themes"].append(theme)
            if t.get("role"):
                row["roles"].append(t["role"])
            if isinstance(t.get("purity_pct"), (int, float)):
                row["purity_pct"] = max(row["purity_pct"] or 0, t["purity_pct"])
            if t.get("mcap_bucket") in MCAP_ORDER:
                row["mcap_bucket"] = t["mcap_bucket"]
            if isinstance(demand_mult, (int, float)):
                row["best_demand_mult"] = max(row["best_demand_mult"] or 0, demand_mult)
            if conviction in CONVICTION_ORDER:
                if row["best_conviction"] is None or (
                    CONVICTION_ORDER[conviction] < CONVICTION_ORDER[row["best_conviction"]]
                ):
                    row["best_conviction"] = conviction
    return sorted(pool.values(), key=rank_key)


def rank_key(row):
    # v2.4-field-rich rows first (they carry real ranking signal), then:
    # small/mid cap ahead of mega, higher purity, higher demand multiple,
    # stronger conviction, more 🔴 appearances.
    has_v24 = row["purity_pct"] is not None or row["mcap_bucket"] is not None
    return (
        0 if has_v24 else 1,
        MCAP_ORDER.get(row["mcap_bucket"], 9),
        -(row["purity_pct"] or 0),
        -(row["best_demand_mult"] or 0),
        CONVICTION_ORDER.get(row["best_conviction"], 9),
        -row["core_count"],
        row["ticker"],
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="include tickers that already have a DD")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--top", type=int, default=0, help="limit to top N rows")
    args = ap.parse_args()

    metas = load_id_metas()
    dd_set = dd_universe()
    rows = collect(metas, dd_set, include_dd=args.all)
    total = len(rows)
    n_v24 = sum(1 for r in rows if r["purity_pct"] is not None or r["mcap_bucket"] is not None)
    if args.top:
        rows = rows[: args.top]

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    shown = f"，列前 {len(rows)}" if len(rows) < total else ""
    print(f"ID 掃描 {len(metas)} 份｜DD universe {len(dd_set)} 檔｜"
          f"🔴 候選 {total} 檔（{'含' if args.all else '不含'}已有 DD{shown}）｜"
          f"帶 v2.4 排序欄位 {n_v24} 檔")
    print(f"{'ticker':<10}{'DD':<4}{'市值':<7}{'純度%':<7}{'需求5Y×':<9}{'conv':<6}{'🔴次':<5}themes")
    for r in rows:
        themes = "; ".join(dict.fromkeys(r["themes"]))[:60]
        print(f"{r['ticker']:<10}"
              f"{'有' if r['has_dd'] else '—':<4}"
              f"{r['mcap_bucket'] or '待補':<7}"
              f"{r['purity_pct'] if r['purity_pct'] is not None else '待補':<7}"
              f"{r['best_demand_mult'] if r['best_demand_mult'] is not None else '待補':<9}"
              f"{r['best_conviction'] or '—':<6}"
              f"{r['core_count']:<5}"
              f"{themes}")
    if n_v24 < len(rows):
        print(f"\n註：「待補」＝該 ID 為 v2.4 前的 legacy 報告，缺 purity_pct/mcap_bucket/"
              f"demand_5y_multiple；ID 重跑（v2.4+）後自動補齊排序訊號。")


if __name__ == "__main__":
    main()
