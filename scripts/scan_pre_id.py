#!/usr/bin/env python3
"""Pre-ID discovery scan — 爆發形狀 × 覆蓋標籤（multi-bagger shape screen）.

The multi-bagger hunt should filter on SHAPE (price/fundamental momentum), not on
coverage state. Coverage (has DD / in some ID / blind spot) is a research-workflow
concern — it belongs as a TAG, not a filter. Earlier versions excluded every
covered name, which optimized for "where to write the next ID" but actively threw
away the most valuable signal: a name we already researched (has a DD) that is NOW
showing breakout shape. So: shape gate runs over the WHOLE candidate universe;
each hit is tagged by coverage. The 🔭 blind-spot rows still answer "write ID
here"; the full ranked list is the investment view "all multi-bagger shapes."

Universe (two arms, union):
  A. docs/screener/latest.json (~510 S&P500/NQ100, daily cron) — RS leaders
     (rs_score ≥ 80): mid/large names whose leadership is confirmed.
  B. yfinance predefined screens (small_cap_gainers / aggressive_small_caps /
     growth_technology_stocks) — the arm that reaches OUTSIDE the indices,
     where cold small caps live.

Coverage tag (not a filter): ✅ has DD > 🟡 in some ID, no DD > 🔭 blind spot.
A ✅/🟡 shape-hit means "we know this name AND it just turned" — highest value,
previously discarded. Note AR Live (main table) only fires on PULLBACKS (AR≥4);
a breaking-OUT covered name won't trigger it — this scan catches that.

爆發形狀 gates (fetched via yfinance .info):
  - mcap ≥ $0.3B (microcap junk floor only; NO upper cap — large-caps multi-bag
    too, NVDA $300B→$3T being the proof. Market cap is a TAG (small/mid/large/
    mega), not a filter: small/mid = "undiscovered" hunt, large/mega = "cycle /
    re-rate the market underprices" hunt. Excluding large-caps was a frequency
    bias mistaken for a law.)
  - quarterly revenue growth ≥ +20% YoY
  - price strength: 52w range position ≥ 0.6 (B arm) / rs_score ≥ 80 (A arm)
  - gross margin ≥ 25% (soft filter vs commodity junk; financials exempt)

Output: ranked CLI table + docs/dd-screener/pre_id_scan.json (FE renders a
collapsed section; hidden when file absent). NOT hooked into the
build_dd_screener chain (yfinance-heavy) — run manually or via weekly cron:
  python3 scripts/scan_pre_id.py            # scan + write JSON
  python3 scripts/scan_pre_id.py --dry-run  # scan, print only
"""
import json
import re
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).parent.parent
OUT = ROOT / "docs" / "dd-screener" / "pre_id_scan.json"
SCREENER = ROOT / "docs" / "screener" / "latest.json"

sys.path.insert(0, str(Path(__file__).parent))
from list_breakout_candidates import load_id_metas, dd_universe, norm_ticker  # noqa: E402

YF_SCREENS = ("small_cap_gainers", "aggressive_small_caps", "growth_technology_stocks")
MCAP_MIN = 0.3e9  # microcap junk floor only; no upper cap (large-caps multi-bag too)


def mcap_bucket(mc):
    if not isinstance(mc, (int, float)) or mc <= 0:
        return None
    b = mc / 1e9
    return "mega" if b > 200 else "large" if b > 10 else "mid" if b > 2 else "small"
REV_GROWTH_MIN = 0.20
RANGE_POS_MIN = 0.60
GM_MIN = 0.25
RS_MIN = 80.0


def coverage_map():
    """Map each ticker → coverage state. Coverage is a TAG, not a filter:
    the shape gate hunts multi-bagger shape across the WHOLE universe; whether a
    name is already researched is metadata, not a reason to drop it. A shape-hit
    that already has a DD ("我們懂它且它剛轉強") is the highest-value signal, not
    something to exclude.

    States (most-researched wins): "dd" (has DD) > "id" (in some ID, no DD) >
    "" (blind spot, zero coverage).
    """
    dd = set(dd_universe())
    id_named = set()
    for meta in load_id_metas():
        for t in meta.get("related_tickers") or []:
            if isinstance(t, dict) and t.get("ticker"):
                id_named.add(norm_ticker(str(t["ticker"])))

    def state(tk):
        if tk in dd:
            return "dd"
        if tk in id_named:
            return "id"
        return ""
    return state


def gather_candidates():
    """arm A: RS leaders from the daily index screener; arm B: yf.screen."""
    cands = {}
    try:
        rows = json.loads(SCREENER.read_text())["rankings"]
        for r in rows:
            if (r.get("rs_score") or 0) >= RS_MIN:
                tk = norm_ticker(r["ticker"])
                cands[tk] = {"ticker": tk, "arms": ["rs_leader"], "rs_score": r["rs_score"],
                             "dist_52w_high_pct": r.get("dist_52w_high_pct"), "sector": r.get("sector")}
    except Exception as e:
        print(f"  ⚠ arm A (index screener) unavailable: {e}", file=sys.stderr)
    try:
        import yfinance as yf
        for q in YF_SCREENS:
            try:
                for quote in yf.screen(q, count=100).get("quotes", []):
                    sym = quote.get("symbol", "")
                    if not sym or "." in sym or "-" in sym:
                        continue  # US common stock only
                    tk = norm_ticker(sym)
                    row = cands.setdefault(tk, {"ticker": tk, "arms": [], "sector": quote.get("sector")})
                    if q not in row["arms"]:
                        row["arms"].append(q)
                    mc = quote.get("marketCap")
                    if mc:
                        row["mcap_usd"] = mc
            except Exception as e:
                print(f"  ⚠ yf.screen {q} failed: {e}", file=sys.stderr)
    except ImportError:
        print("  ⚠ yfinance unavailable — arm B skipped", file=sys.stderr)
    return cands


def enrich(row):
    """Fetch shape inputs for one candidate; None on failure."""
    import yfinance as yf
    try:
        info = yf.Ticker(row["ticker"]).info
    except Exception:
        return None
    mc = info.get("marketCap") or row.get("mcap_usd")
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    hi, lo = info.get("fiftyTwoWeekHigh"), info.get("fiftyTwoWeekLow")
    row.update({
        "mcap_usd": mc,
        "rev_growth": info.get("revenueGrowth"),
        "gross_margin": info.get("grossMargins"),
        "price": price,
        "range_pos": round((price - lo) / (hi - lo), 2) if all(
            isinstance(x, (int, float)) for x in (price, hi, lo)) and hi > lo else None,
        "name": info.get("shortName"),
        "sector": row.get("sector") or info.get("sector"),
        "industry": info.get("industry"),
    })
    return row


def passes_shape(r):
    # financials / REITs excluded outright: their revenueGrowth is an
    # accounting artifact (mREIT +1569% ≠ 爆發), and the multi-bagger shape
    # this scan hunts is operating-leverage growth, not balance-sheet spread.
    sector = (r.get("sector") or "")
    industry = (r.get("industry") or "")
    if sector in ("Financial Services", "Real Estate") or "REIT" in industry or "Insurance" in industry:
        return False
    mc, rg = r.get("mcap_usd"), r.get("rev_growth")
    if not isinstance(mc, (int, float)) or mc < MCAP_MIN:
        return False
    if not isinstance(rg, (int, float)) or rg < REV_GROWTH_MIN:
        return False
    strong = (r.get("rs_score") or 0) >= RS_MIN or (r.get("range_pos") or 0) >= RANGE_POS_MIN
    if not strong:
        return False
    gm = r.get("gross_margin")
    if isinstance(gm, (int, float)) and gm < GM_MIN:
        return False
    return True


COV_LABEL = {"dd": "✅ 有 DD", "id": "🟡 有 ID 無 DD", "": "🔭 盲區"}
# Sort: strongest signal first, but surface blind spots ahead of ties (they need
# ID action). Within same coverage, rank by revenue growth. Coverage state is a
# tag — every shape-hit is shown, not filtered.
COV_ORDER = {"dd": 0, "id": 1, "": 2}


def main():
    dry = "--dry-run" in sys.argv
    state = coverage_map()
    cands = gather_candidates()
    all_cands = list(cands.values())
    # Shape filter runs over the WHOLE candidate universe — no coverage exclusion.
    print(f"候選 {len(cands)}（RS 領導 + 小市值 screens 聯集）→ 全數抓基本面過爆發形狀閘（覆蓋為標籤非過濾）…")
    with ThreadPoolExecutor(max_workers=8) as ex:
        enriched = [r for r in ex.map(enrich, all_cands) if r]
    hits = [r for r in enriched if passes_shape(r)]
    for r in hits:
        r["coverage"] = state(r["ticker"])
        r["mcap_bucket"] = mcap_bucket(r.get("mcap_usd"))
    hits.sort(key=lambda r: -(r.get("rev_growth") or 0))
    n_dd = sum(1 for r in hits if r["coverage"] == "dd")
    n_id = sum(1 for r in hits if r["coverage"] == "id")
    n_blind = sum(1 for r in hits if r["coverage"] == "")
    from collections import Counter
    bk = Counter(r["mcap_bucket"] for r in hits)
    print(f"\n爆發形狀命中 {len(hits)} 檔（營收成長排序）｜覆蓋：🔭盲區 {n_blind}｜🟡有ID {n_id}｜✅有DD {n_dd}"
          f"｜市值：small {bk['small']}/mid {bk['mid']}/large {bk['large']}/mega {bk['mega']}\n")
    print(f"{'ticker':<8}{'覆蓋':<16}{'市值級':<7}{'mcap':<8}{'營收YoY':<9}{'GM':<7}{'52w位置':<8}{'RS':<6}industry")
    for r in hits[:50]:
        print(f"{r['ticker']:<8}"
              f"{COV_LABEL[r['coverage']]:<16}"
              f"{(r.get('mcap_bucket') or '—'):<7}"
              f"{'$'+str(round(r['mcap_usd']/1e9,1))+'B':<8}"
              f"{round(r['rev_growth']*100):+d}%{'':<4}"
              f"{round((r.get('gross_margin') or 0)*100)}%{'':<3}"
              f"{r.get('range_pos') if r.get('range_pos') is not None else '—':<8}"
              f"{r.get('rs_score') or '—':<6}"
              f"{(r.get('industry') or '')[:36]}")
    if dry:
        print("\n(dry-run) 不寫 JSON")
        return
    now = datetime.now(timezone(timedelta(hours=8)))
    doc = {"as_of": now.strftime("%Y-%m-%d"), "generated_at": now.isoformat(timespec="seconds"),
           "candidates_scanned": len(cands), "hits": len(hits),
           "coverage_counts": {"blind": n_blind, "id": n_id, "dd": n_dd},
           "mcap_counts": dict(bk),
           "criteria": {"mcap_usd_min": MCAP_MIN, "mcap_usd_max": None, "rev_growth_min": REV_GROWTH_MIN,
                        "range_pos_min": RANGE_POS_MIN, "gm_min": GM_MIN, "rs_min": RS_MIN},
           "rows": hits[:70]}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n✓ Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
