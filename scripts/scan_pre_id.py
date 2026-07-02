#!/usr/bin/env python3
"""Pre-ID discovery scan — 爆發形狀 × 零研究覆蓋（研究盲區掃描）.

The ID→pool→DD funnel only sees names research attention already reached;
multi-baggers' best entries happen BEFORE coverage (RKLB 2025 @$20-30 had no
ID). This scan inverts the direction: price/fundamental signals drive
research attention instead of research defining the universe.

Universe (two arms, union):
  A. docs/screener/latest.json (~510 S&P500/NQ100, daily cron) — RS leaders
     (rs_score ≥ 80): mid/large names whose leadership is confirmed.
  B. yfinance predefined screens (small_cap_gainers / aggressive_small_caps /
     growth_technology_stocks) — the arm that reaches OUTSIDE the indices,
     where cold small caps live.

Exclusion = the entire existing field of view: DD universe (docs/dd) ∪ every
ticker any ID names in related_tickers (any depth). What survives is, by
construction, a research blind spot.

爆發形狀 gates (fetched via yfinance .info for the uncovered shortlist):
  - mcap $0.3B–$30B (multi-baggers cluster small/mid; mega excluded)
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
MCAP_MIN, MCAP_MAX = 0.3e9, 30e9
REV_GROWTH_MIN = 0.20
RANGE_POS_MIN = 0.60
GM_MIN = 0.25
RS_MIN = 80.0


def covered_set():
    cov = set(dd_universe())
    for meta in load_id_metas():
        for t in meta.get("related_tickers") or []:
            if isinstance(t, dict) and t.get("ticker"):
                cov.add(norm_ticker(str(t["ticker"])))
    return cov


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
    """Fetch shape inputs for one uncovered candidate; None on failure."""
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
    if not isinstance(mc, (int, float)) or not (MCAP_MIN <= mc <= MCAP_MAX):
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


def main():
    dry = "--dry-run" in sys.argv
    cov = covered_set()
    cands = gather_candidates()
    uncovered = [r for tk, r in cands.items() if tk not in cov]
    print(f"候選 {len(cands)}（RS 領導 + 小市值 screens 聯集）→ 未被 DD/ID 覆蓋 {len(uncovered)} 檔，抓基本面…")
    with ThreadPoolExecutor(max_workers=8) as ex:
        enriched = [r for r in ex.map(enrich, uncovered) if r]
    hits = sorted((r for r in enriched if passes_shape(r)),
                  key=lambda r: -(r.get("rev_growth") or 0))
    print(f"\n爆發形狀 × 零覆蓋：{len(hits)} 檔（營收成長排序）\n")
    print(f"{'ticker':<8}{'mcap':<8}{'營收YoY':<9}{'GM':<7}{'52w位置':<8}{'RS':<6}{'來源':<28}industry")
    for r in hits[:40]:
        print(f"{r['ticker']:<8}"
              f"{'$'+str(round(r['mcap_usd']/1e9,1))+'B':<8}"
              f"{round(r['rev_growth']*100):+d}%{'':<4}"
              f"{round((r.get('gross_margin') or 0)*100)}%{'':<3}"
              f"{r.get('range_pos') if r.get('range_pos') is not None else '—':<8}"
              f"{r.get('rs_score') or '—':<6}"
              f"{','.join(a.replace('_','-')[:12] for a in r['arms']):<28}"
              f"{(r.get('industry') or '')[:36]}")
    if dry:
        print("\n(dry-run) 不寫 JSON")
        return
    now = datetime.now(timezone(timedelta(hours=8)))
    doc = {"as_of": now.strftime("%Y-%m-%d"), "generated_at": now.isoformat(timespec="seconds"),
           "candidates_scanned": len(cands), "uncovered": len(uncovered), "hits": len(hits),
           "criteria": {"mcap_usd": [MCAP_MIN, MCAP_MAX], "rev_growth_min": REV_GROWTH_MIN,
                        "range_pos_min": RANGE_POS_MIN, "gm_min": GM_MIN, "rs_min": RS_MIN},
           "rows": hits[:60]}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n✓ Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
