#!/usr/bin/env python3
"""Pre-ID discovery scan — 爆發形狀 × 前瞻確認 × 覆蓋標籤（multi-bagger shape screen）.

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
  B. yfinance custom EquityQuery (US main exchanges × mcap ≥ $0.3B × quarterly
     rev growth ≥ +20%, sorted by 52w change) — the arm that reaches OUTSIDE the
     indices systematically. Replaces the old predefined day-gainer screens
     (small_cap_gainers etc.), which sampled "who spiked on scan day" — a name
     breaking out steadily but flat today never entered the pool. Predefined
     screens remain as fallback if the custom query API fails.

爆發形狀 gates (fetched via yfinance .info):
  - mcap ≥ $0.3B (microcap junk floor only; NO upper cap — large-caps multi-bag
    too, NVDA $300B→$3T being the proof. Market cap is a TAG (small/mid/large/
    mega), not a filter.)
  - quarterly revenue growth ≥ +20% YoY (trailing, confirmatory)
  - price strength: 52w range position ≥ 0.6 (B arm) / rs_score ≥ 80 (A arm)
  - gross margin ≥ 25% (soft filter vs commodity junk; financials/REIT excluded)

Forward layer (TAGS + sort, not gates — a zero-coverage name is "truly
undiscovered", which is signal, not a reason to drop):
  - fwd growth %: Koyfin FY1→FY3 EPS CAGR from docs/dd-screener/latest.json for
    names inside the DD universe (same source as the main table — 同源, plus
    revision% chip); yfinance revenue_estimate (+1y consensus rev growth) for
    names outside. Tag: 🟢 續強 ≥ +15% / ➖ 放緩 0..15 / 🔴 反轉 < 0 / ⚪ 無預估.
  - accel: expected next-quarter YoY vs trailing reported YoY (both from the
    same revenue_estimate call; only 5 quarters of history exist on yfinance so
    true historical acceleration is not computable). 📈 next ≥ trailing×1.15,
    📉 next ≤ trailing×0.70 or < 0, ➖ in between. Coarse multiplicative
    thresholds on purpose — no parameter tuning.
  - Sort key = min(trailing, fwd) desc (conservative take-the-smaller): a
    trailing +104% with fwd −24% (cycle top / base effect, e.g. tanker names)
    sinks; trailing +346% with fwd +83% (MU) stays on top. No-estimate names
    rank by trailing alone.

Persistence (memory across runs): first_seen / weeks_on_list carried from the
previous JSON — a shape that survives 3 weekly scans is stronger than a
one-day wonder, and the history doubles as future hit-rate backtest data.
Same-day re-runs do not increment weeks_on_list.

Output: ranked CLI table + docs/dd-screener/pre_id_scan.json (FE renders a
collapsed section; hidden when file absent). NOT hooked into the
build_dd_screener chain (yfinance-heavy) — run manually or via weekly cron:
  python3 scripts/scan_pre_id.py            # scan + write JSON
  python3 scripts/scan_pre_id.py --dry-run  # scan, print only
"""
import json
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).parent.parent
OUT = ROOT / "docs" / "dd-screener" / "pre_id_scan.json"
SCREENER = ROOT / "docs" / "screener" / "latest.json"
DD_SCREENER = ROOT / "docs" / "dd-screener" / "latest.json"

sys.path.insert(0, str(Path(__file__).parent))
from list_breakout_candidates import load_id_metas, dd_universe, norm_ticker  # noqa: E402

YF_FALLBACK_SCREENS = ("small_cap_gainers", "aggressive_small_caps", "growth_technology_stocks")
US_EXCHANGES = ("NMS", "NYQ", "NGM", "NCM", "ASE")  # main boards only, no OTC/pink
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
FWD_STRONG_MIN = 15.0   # 🟢 前瞻續強 threshold (fwd growth %, either source)
ACCEL_UP = 1.15         # 📈 expected next-q YoY ≥ trailing × 1.15
ACCEL_DOWN = 0.70       # 📉 expected next-q YoY ≤ trailing × 0.70 (or < 0)


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


def load_koyfin_fwd():
    """ticker → forward EPS view from docs/dd-screener/latest.json (Koyfin xlsx,
    DD-universe only, ~240 names). Same source the main table renders — the
    radar's forward numbers for covered names never disagree with 管線② (同源).
    """
    try:
        stocks = json.loads(DD_SCREENER.read_text())["stocks"]
        if isinstance(stocks, dict):
            stocks = [dict(s, ticker=tk) for tk, s in stocks.items()]
    except Exception as e:
        print(f"  ⚠ Koyfin forward layer unavailable: {e}", file=sys.stderr)
        return {}
    out = {}
    for s in stocks:
        cagr = s.get("eps_fy1_fy3_cagr_pct")
        if isinstance(cagr, (int, float)) and s.get("ticker"):
            out[norm_ticker(str(s["ticker"]))] = {
                "fwd_pct": round(cagr, 1),
                "revision_pct": s.get("eps_revision_pct"),
            }
    return out


def gather_candidates():
    """arm A: RS leaders from the daily index screener; arm B: yf custom screen."""
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

    def add_quotes(quotes, arm):
        for quote in quotes:
            sym = quote.get("symbol", "")
            if not sym or "." in sym or "-" in sym:
                continue  # US common stock only
            tk = norm_ticker(sym)
            row = cands.setdefault(tk, {"ticker": tk, "arms": [], "sector": quote.get("sector")})
            if arm not in row["arms"]:
                row["arms"].append(arm)
            mc = quote.get("marketCap")
            if mc:
                row["mcap_usd"] = mc

    try:
        import yfinance as yf
        try:
            from yfinance import EquityQuery
            q = EquityQuery("and", [
                EquityQuery("eq", ["region", "us"]),
                EquityQuery("is-in", ["exchange", *US_EXCHANGES]),
                EquityQuery("gt", ["intradaymarketcap", MCAP_MIN]),
                EquityQuery("gt", ["quarterlyrevenuegrowth.quarterly", REV_GROWTH_MIN * 100]),
            ])
            r = yf.screen(q, size=250, sortField="fiftytwowkpercentchange", sortAsc=False)
            add_quotes(r.get("quotes", []), "custom_screen")
            print(f"  arm B custom screen: {r.get('total')} 檔符合，取 52w 強度前 {len(r.get('quotes', []))}")
        except Exception as e:
            print(f"  ⚠ custom EquityQuery failed ({e}) — falling back to predefined screens", file=sys.stderr)
            for name in YF_FALLBACK_SCREENS:
                try:
                    add_quotes(yf.screen(name, count=100).get("quotes", []), name)
                except Exception as e2:
                    print(f"  ⚠ yf.screen {name} failed: {e2}", file=sys.stderr)
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


def fetch_rev_estimates(tk):
    """Consensus revenue-growth estimates for one hit (0q/+1q/+1y YoY, %).
    Even 1-2-analyst small caps usually have these on yfinance."""
    import yfinance as yf
    try:
        df = yf.Ticker(tk).revenue_estimate
        if df is None or df.empty or "growth" not in df:
            return {}
        g = df["growth"]
        out = {}
        for k in ("0q", "+1q", "+1y"):
            v = g.get(k)
            if isinstance(v, (int, float)) and v == v:  # NaN guard
                out[k] = round(float(v) * 100, 1)
        return out
    except Exception:
        return {}


def add_forward_layer(hits, koyfin):
    """Attach fwd growth (tag + %), accel tag, and conservative sort key.
    All TAGS — nothing here filters a row out."""
    with ThreadPoolExecutor(max_workers=8) as ex:
        ests = dict(zip((r["ticker"] for r in hits),
                        ex.map(fetch_rev_estimates, (r["ticker"] for r in hits))))
    for r in hits:
        est = ests.get(r["ticker"]) or {}
        koy = koyfin.get(r["ticker"])
        trailing_pct = round(r["rev_growth"] * 100, 1)
        if koy:  # inside DD universe → Koyfin FY1→FY3 EPS CAGR（與主表同源）
            fwd, src, rev = koy["fwd_pct"], "koyfin", koy.get("revision_pct")
        else:    # outside → yfinance consensus +1y revenue growth
            fwd, src, rev = est.get("+1y"), ("yf" if est.get("+1y") is not None else None), None
        r["fwd_growth_pct"] = fwd
        r["fwd_src"] = src
        r["eps_revision_pct"] = rev
        r["fwd_tag"] = (None if fwd is None else
                        "strong" if fwd >= FWD_STRONG_MIN else
                        "reverse" if fwd < 0 else "slow")
        # accel: expected next-q YoY vs trailing reported YoY (forward trajectory;
        # yfinance history is 5 quarters — too short for true historical accel)
        nq = est.get("+1q", est.get("0q"))
        if nq is None:
            r["accel"] = None
        elif nq < 0 or nq <= trailing_pct * ACCEL_DOWN:
            r["accel"] = "down"
        elif nq >= trailing_pct * ACCEL_UP:
            r["accel"] = "up"
        else:
            r["accel"] = "flat"
        r["next_q_growth_pct"] = nq
        # conservative take-the-smaller sort: trailing hot + forward rollover sinks
        r["sort_key"] = round(min(trailing_pct, fwd) if fwd is not None else trailing_pct, 1)


def add_persistence(hits, today):
    """Carry first_seen / weeks_on_list from the previous JSON (shape that
    survives multiple weekly scans > one-day wonder; doubles as hit-rate
    backtest data). Same-day re-runs don't increment."""
    prev_rows, prev_asof = {}, None
    try:
        prev = json.loads(OUT.read_text())
        prev_asof = prev.get("as_of")
        prev_rows = {r["ticker"]: r for r in prev.get("rows", [])}
    except Exception:
        pass
    same_day = prev_asof == today
    for r in hits:
        p = prev_rows.get(r["ticker"])
        if p:
            r["first_seen"] = p.get("first_seen") or prev_asof
            r["weeks_on_list"] = (p.get("weeks_on_list") or 1) + (0 if same_day else 1)
        else:
            r["first_seen"] = today
            r["weeks_on_list"] = 1


COV_LABEL = {"dd": "✅ 有 DD", "id": "🟡 有 ID 無 DD", "": "🔭 盲區"}
FWD_LABEL = {"strong": "🟢續強", "slow": "➖放緩", "reverse": "🔴反轉", None: "⚪無預估"}
ACCEL_LABEL = {"up": "📈", "down": "📉", "flat": "➖", None: "—"}


def main():
    dry = "--dry-run" in sys.argv
    state = coverage_map()
    koyfin = load_koyfin_fwd()
    cands = gather_candidates()
    all_cands = list(cands.values())
    # Shape filter runs over the WHOLE candidate universe — no coverage exclusion.
    print(f"候選 {len(cands)}（RS 領導 + 自訂全市場 screen 聯集）→ 全數抓基本面過爆發形狀閘（覆蓋為標籤非過濾）…")
    with ThreadPoolExecutor(max_workers=8) as ex:
        enriched = [r for r in ex.map(enrich, all_cands) if r]
    hits = [r for r in enriched if passes_shape(r)]
    for r in hits:
        r["coverage"] = state(r["ticker"])
        r["mcap_bucket"] = mcap_bucket(r.get("mcap_usd"))
    print(f"形狀命中 {len(hits)} 檔 → 抓前瞻預估（Koyfin 同源優先，盲區 yfinance 補）…")
    add_forward_layer(hits, koyfin)
    now = datetime.now(timezone(timedelta(hours=8)))
    today = now.strftime("%Y-%m-%d")
    add_persistence(hits, today)
    hits.sort(key=lambda r: -(r.get("sort_key") or 0))
    n_dd = sum(1 for r in hits if r["coverage"] == "dd")
    n_id = sum(1 for r in hits if r["coverage"] == "id")
    n_blind = sum(1 for r in hits if r["coverage"] == "")
    from collections import Counter
    bk = Counter(r["mcap_bucket"] for r in hits)
    fw = Counter(r["fwd_tag"] for r in hits)
    print(f"\n爆發形狀命中 {len(hits)} 檔（min(trailing, fwd) 保守排序）"
          f"｜覆蓋：🔭盲區 {n_blind}｜🟡有ID {n_id}｜✅有DD {n_dd}"
          f"｜前瞻：🟢 {fw['strong']}/➖ {fw['slow']}/🔴 {fw['reverse']}/⚪ {fw[None]}"
          f"｜市值：small {bk['small']}/mid {bk['mid']}/large {bk['large']}/mega {bk['mega']}\n")
    print(f"{'ticker':<8}{'覆蓋':<16}{'市值級':<7}{'mcap':<8}{'營收YoY':<9}{'前瞻':<10}{'加速':<5}{'週':<4}{'GM':<7}{'52w位置':<8}{'RS':<6}industry")
    for r in hits[:50]:
        fwd = f"{r['fwd_growth_pct']:+.0f}%" if r.get("fwd_growth_pct") is not None else ""
        print(f"{r['ticker']:<8}"
              f"{COV_LABEL[r['coverage']]:<16}"
              f"{(r.get('mcap_bucket') or '—'):<7}"
              f"{'$'+str(round(r['mcap_usd']/1e9,1))+'B':<8}"
              f"{round(r['rev_growth']*100):+d}%{'':<4}"
              f"{FWD_LABEL[r['fwd_tag']] + fwd:<12}"
              f"{ACCEL_LABEL[r['accel']]:<5}"
              f"{r.get('weeks_on_list') or 1:<4}"
              f"{round((r.get('gross_margin') or 0)*100)}%{'':<3}"
              f"{r.get('range_pos') if r.get('range_pos') is not None else '—':<8}"
              f"{r.get('rs_score') or '—':<6}"
              f"{(r.get('industry') or '')[:30]}")
    if dry:
        print("\n(dry-run) 不寫 JSON")
        return
    doc = {"as_of": today, "generated_at": now.isoformat(timespec="seconds"),
           "candidates_scanned": len(cands), "hits": len(hits),
           "coverage_counts": {"blind": n_blind, "id": n_id, "dd": n_dd},
           "mcap_counts": dict(bk),
           "fwd_counts": {"strong": fw["strong"], "slow": fw["slow"],
                          "reverse": fw["reverse"], "none": fw[None]},
           "criteria": {"mcap_usd_min": MCAP_MIN, "mcap_usd_max": None, "rev_growth_min": REV_GROWTH_MIN,
                        "range_pos_min": RANGE_POS_MIN, "gm_min": GM_MIN, "rs_min": RS_MIN,
                        "fwd_strong_min_pct": FWD_STRONG_MIN, "accel_up_x": ACCEL_UP, "accel_down_x": ACCEL_DOWN,
                        "sort": "min(trailing, fwd) desc"},
           "rows": hits[:70]}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n✓ Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
