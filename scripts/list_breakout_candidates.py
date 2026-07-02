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
  python3 scripts/list_breakout_candidates.py --write    # 寫 docs/dd-screener/discovery_pool.json
                                                         #（build_dd_screener.py 每次 build 後自動呼叫）
"""
import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"
DD_DIR = ROOT / "docs" / "dd"
POOL_PATH = ROOT / "docs" / "dd-screener" / "discovery_pool.json"

ID_META_RE = re.compile(
    r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
DD_FILE_RE = re.compile(r"^DD_([A-Za-z0-9.\-]+)_\d{8}\.html$")

MCAP_ORDER = {"small": 0, "mid": 1, "large": 2, "mega": 3}
CONVICTION_ORDER = {"high": 0, "mid": 1, "low": 2}

# Cross-listing aliases: id-meta may cite the local listing while the DD was
# written on the US ADR (or vice versa). Map both directions onto one key so
# the pool doesn't show phantom "no DD" candidates (e.g. 2330.TW when
# DD_TSM_*.html exists).
TICKER_ALIASES = {
    "2330.TW": "TSM",
    "2330": "TSM",
}


def norm_ticker(raw: str) -> str:
    """Canonical ticker key: uppercase, dots stripped for TW/KS local listings
    (DD filenames use 2308TW while id-meta uses 2308.TW), aliases applied."""
    tk = str(raw).upper().strip()
    tk = TICKER_ALIASES.get(tk, tk)
    m = re.match(r"^(\d{4,6})\.(TW|KS|T|HK)$", tk)
    if m:
        tk = m.group(1) + m.group(2)
    return TICKER_ALIASES.get(tk, tk)


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
            tickers.add(norm_ticker(m.group(1)))
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
            raw_tk = str(t.get("ticker", "")).upper().strip()
            if not raw_tk:
                continue
            tk = norm_ticker(raw_tk)
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
    # Rank by attention-INDEPENDENT signals: small/mid cap first, then purity,
    # demand multiple, conviction. core_count (how many IDs flag it 🔴) is
    # deliberately demoted to last tiebreak — it measures ID overlap density
    # (research attention), which anti-correlates with undiscovered multi-baggers:
    # a cold-industry pure-play covered by exactly one ID must not lose to a
    # steakhouse chain that five overlapping restaurant IDs all happen to name.
    return (
        MCAP_ORDER.get(row["mcap_bucket"], 9),
        -(row["purity_pct"] or 0),
        -(row["best_demand_mult"] or 0),
        CONVICTION_ORDER.get(row["best_conviction"], 9),
        -row["core_count"],
        row["ticker"],
    )


def yf_symbol(tk: str) -> str:
    """Pool keys are normalized (2308TW); yfinance wants dotted (2308.TW)."""
    m = re.match(r"^(\d{4,6})(TW|KS|T|HK)$", tk)
    return f"{m.group(1)}.{m.group(2)}" if m else tk


def bucket_mcap(mcap) -> str | None:
    if not isinstance(mcap, (int, float)) or mcap <= 0:
        return None
    usd_b = mcap / 1e9
    if usd_b > 200:
        return "mega"
    if usd_b > 10:
        return "large"
    if usd_b > 2:
        return "mid"
    return "small"


def backfill_mcap(rows, prev_pool_path=None):
    """Fill mcap_bucket mechanically via yfinance for rows the IDs left blank.

    mcap needs no ID regen — it's mechanical data, and it is the single most
    important attention-independent rank key. Failures fall back to the
    previous pool file's value (MA-cache pattern), else stay None (待補).
    Note: non-US local listings are bucketed on their native-currency mcap as
    a rough proxy (KRW/TWD overstate size); acceptable for 4-bucket coarseness
    of US-heavy pool, refined when ID v2.4 regen supplies authored buckets.
    """
    prev = {}
    if prev_pool_path and Path(prev_pool_path).exists():
        try:
            for r in json.loads(Path(prev_pool_path).read_text())["rows"]:
                if r.get("mcap_bucket"):
                    prev[r["ticker"]] = r["mcap_bucket"]
        except Exception:
            pass
    todo = [r for r in rows if r["mcap_bucket"] is None]
    if not todo:
        return 0
    try:
        import yfinance as yf
        from concurrent.futures import ThreadPoolExecutor
    except ImportError:
        for r in todo:
            r["mcap_bucket"] = prev.get(r["ticker"])
        return 0

    def fetch(r):
        try:
            mc = yf.Ticker(yf_symbol(r["ticker"])).fast_info["marketCap"]
            return r, bucket_mcap(mc)
        except Exception:
            return r, None

    filled = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for r, bucket in ex.map(fetch, todo):
            r["mcap_bucket"] = bucket or prev.get(r["ticker"])
            if r["mcap_bucket"]:
                r["mcap_source"] = "yfinance" if bucket else "cache"
                filled += 1
    return filled


def build_pool_doc():
    """Assemble the discovery-pool document consumed by /dd-screener/ FE."""
    metas = load_id_metas()
    dd_set = dd_universe()
    rows = collect(metas, dd_set, include_dd=False)
    backfill_mcap(rows, prev_pool_path=POOL_PATH)
    rows.sort(key=rank_key)
    for r in rows:
        r["themes"] = list(dict.fromkeys(r["themes"]))
        r.pop("roles", None)
    now = datetime.now(timezone(timedelta(hours=8)))
    return {
        "as_of": now.strftime("%Y-%m-%d"),
        "generated_at": now.isoformat(timespec="seconds"),
        "id_files_scanned": len(metas),
        "dd_universe_size": len(dd_set),
        "total": len(rows),
        "v24_ranked": sum(1 for r in rows
                          if r["purity_pct"] is not None or r["mcap_bucket"] is not None),
        "rows": rows,
    }


def write_pool(path: Path = POOL_PATH) -> Path:
    doc = build_pool_doc()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="include tickers that already have a DD")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--top", type=int, default=0, help="limit to top N rows")
    ap.add_argument("--write", action="store_true",
                    help="write docs/dd-screener/discovery_pool.json (for the FE section)")
    args = ap.parse_args()

    if args.write:
        path = write_pool()
        doc = json.loads(path.read_text(encoding="utf-8"))
        print(f"✓ Wrote {path} ({path.stat().st_size:,} bytes, "
              f"{doc['total']} tickers, v2.4-ranked {doc['v24_ranked']})")
        return

    metas = load_id_metas()
    dd_set = dd_universe()
    rows = collect(metas, dd_set, include_dd=args.all)
    backfill_mcap(rows, prev_pool_path=POOL_PATH)
    rows.sort(key=rank_key)
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
