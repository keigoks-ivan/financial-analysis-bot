#!/usr/bin/env python3
"""早報用台股寬名單 -> docs/dd-screener/tw-wide/latest.json（2026-10-21）。

來源：data/eps-estimates/DD_tw_wide_EPS_estimates_*.xlsx（Koyfin watchlist dd_tw_wide：
市值前 500 大裡有 FY1～FY3 任一 EPS 預估的股票，含金融股與興櫃；
koyfin_families.py 的 family `tw_wide`）。

用途只有一個：morning-briefing/briefing/dd_numbers.py 的 TW_URLS 第二個網址，
創高名單掛 EPS 年增三格、3y CAGR、ROIC、PEG。**不進席位／stages／FunnelRank／
dd-screener 台股頁，不算任何排名。** 欄位名與 docs/dd-screener/tw/latest.json 相同，
dd_numbers.facts() 直接吃。

口徑（與主名單 build_dd_screener.py --universe tw 的非 DD 列一致）：
  - EPS：Koyfin 是美元，乘 xlsx 日的 TWD/USD 一個匯率（eps_fx_normalize.get_fx_rate，
    與主名單 display_fx.local_per_usd 同函式同日期），原值留 *_usd_orig。
  - eps_fy1_fy3_cagr_pct：build_dd_screener._koyfin_eps_growth(rec, "fy1_fy3")，FY1／FY3 年化。
  - roic：xlsx ROIC（百分比數字，2330 約 30）。
  - eps_year_ago：不用 Koyfin 實際值換匯，用 yfinance earnings_estimate 0y.yearAgoEps（新台幣），
    沿用 build_dd_screener 的 year_ago_fye／decide_year_ago_carry／_fetch_year_ago_light。
    同財年的值直接沿用上一份 tw-wide/latest.json（再退到主名單 tw/latest.json），只對缺的抓。

python3.12 執行。失敗時 exit 非 0（koyfin_refresh_all.py 把這一步當不擋推送的步驟）。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

ROOT = SCRIPTS_DIR.parent
DATA_DIR = ROOT / "data" / "eps-estimates"
OUT_DIR = ROOT / "docs" / "dd-screener" / "tw-wide"
OUT_PATH = OUT_DIR / "latest.json"
MAIN_TW_PATH = ROOT / "docs" / "dd-screener" / "tw" / "latest.json"
FAMILY_PREFIX = "DD_tw_wide_EPS_estimates_"
SCHEMA_VERSION = "1.0"
NOTE = ("早報用台股寬名單：市值前 500 大有 EPS 預估，含金融與興櫃；只供早報創高名單查數字，"
        "不進席位／stages／FunnelRank，不排名。EPS 為 Koyfin 美元 × 一個匯率換成新台幣，"
        "eps_year_ago 為 yfinance 新台幣實際值。")
YA_FETCH_GAP = 0.5   # 秒；FYE／year-ago 兩種 yfinance 呼叫之間的最小間隔（避免限流）


def usd_to_local(v, rate):
    """Koyfin 美元 EPS -> 新台幣（2 位小數，與 build_dd_screener._tw_eps_to_local 同）。"""
    return None if v is None or not rate else round(v * rate, 2)


def build_row(code: str, rec: dict, listing: dict | None, rate: float, ya: dict, fiscal_year_end,
              growth_fn) -> dict:
    """一檔 -> latest.json 的一列。listing＝tw_listing_suffix.resolve_tw_codes 的一筆（None＝解不出）。"""
    fy = {"eps_fy_curr": rec.get("fy1"), "eps_fy_next": rec.get("fy2"), "eps_fy3": rec.get("fy3")}
    row = {
        "ticker": (listing or {}).get("ticker") or code,
        "name": (listing or {}).get("name") or code,
        "tw_industry": (listing or {}).get("industry"),
        "tw_market": (listing or {}).get("market"),
        "roic": rec.get("roic_pct"),
    }
    for k, v in fy.items():
        row[k] = usd_to_local(v, rate)
    row["eps_fy1_fy3_cagr_pct"] = growth_fn(rec, "fy1_fy3")
    row.update({
        "eps_year_ago": ya.get("eps_year_ago"),
        "eps_year_ago_fye": ya.get("eps_year_ago_fye"),
        "eps_year_ago_source": ya.get("eps_year_ago_source"),
        "fiscal_year_end": fiscal_year_end,
        "eps_display_currency": "TWD",
        "eps_fx_rate": round(float(rate), 4),
    })
    for k, v in fy.items():
        row[k + "_usd_orig"] = v
    return row


def pick_year_ago(code, ticker, cur_fye, prev_rows, fetch, decide_carry):
    """沿用同財年的舊值；沒有才抓。回傳 eps_year_ago 那幾個欄位。
    prev_rows: [(source_label, {ticker: prev_row}), ...] 依優先順序。"""
    for label, rows in prev_rows:
        carried = decide_carry(rows.get(ticker), cur_fye)
        if carried:
            return {"eps_year_ago": carried["eps_year_ago"], "eps_year_ago_fye": cur_fye,
                    "eps_year_ago_source": label}
    got = fetch(ticker) if cur_fye else {}
    if got and got.get("eps_year_ago") is not None:
        return {"eps_year_ago": got["eps_year_ago"], "eps_year_ago_fye": cur_fye,
                "eps_year_ago_source": "yfinance"}
    return {"eps_year_ago": None, "eps_year_ago_fye": cur_fye, "eps_year_ago_source": None}


def seed_fye_cache(shared: dict, *docs: dict) -> dict:
    """最後一個財年末日的快取：共用 data/fiscal_year_end.json 優先（CI 上通常是空的），
    其次各份 latest.json 的 fiscal_year_end（docs/ 會 commit，CI 讀得到）。"""
    cache = dict(shared or {})
    for d in docs:
        for s in (d or {}).get("stocks") or []:
            t, fye = s.get("ticker"), s.get("fiscal_year_end")
            if t and fye and t not in cache and d.get("as_of"):
                cache[t] = {"last_fye": fye, "checked": d["as_of"]}
    return cache


def _load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xlsx", type=Path, default=None, help="指定 xlsx（預設：最新一份）")
    ap.add_argument("--out", type=Path, default=OUT_PATH)
    ap.add_argument("--no-network-year-ago", action="store_true",
                    help="只用快取沿用 eps_year_ago，不打 yfinance（測試用）")
    args = ap.parse_args()

    import build_dd_screener as bds
    import load_eps_estimates_xlsx as leex
    from eps_fx_normalize import get_fx_rate, load_fx_daily_cache
    from eps_fy_shift import _taipei_today, get_last_fye, load_fye_cache
    from tw_listing_suffix import resolve_tw_codes

    xlsx = args.xlsx or leex.find_latest_excel(DATA_DIR, FAMILY_PREFIX)
    if not xlsx:
        print(f"ERROR: no {FAMILY_PREFIX}*.xlsx under {DATA_DIR}", file=sys.stderr)
        return 2
    snap = leex.load_excel(xlsx)
    codes = sorted(snap.tickers)
    print(f"[tw-wide] {xlsx.name}: {len(codes)} rows, snapshot {snap.snapshot_date}")

    # 匯率：主名單同一天（as_of 相同）就直接用它的 display_fx.local_per_usd，兩份名單同日同匯率；
    # 日期對不上（主名單還沒更新）才自己取 get_fx_rate（主名單用的就是這個函式）。
    main_fx = (_load_json(MAIN_TW_PATH).get("display_fx") or {})
    if main_fx.get("as_of") == snap.snapshot_date and main_fx.get("local_per_usd"):
        rate, fx_src = float(main_fx["local_per_usd"]), "tw/latest.json"
    else:
        rate, fx_src = get_fx_rate("TWD", snap.snapshot_date, load_fx_daily_cache()), "get_fx_rate"
    if not rate:
        print("ERROR: TWD/USD rate unavailable; refusing to mix currencies", file=sys.stderr)
        return 3

    resolved, unresolved = resolve_tw_codes(codes)
    if unresolved:
        print(f"[tw-wide] WARN unresolved codes (kept as bare code): {unresolved}", file=sys.stderr)

    prev_wide, main_tw = _load_json(args.out), _load_json(MAIN_TW_PATH)
    prev_rows = [("carried", bds.load_prev_year_ago(args.out)),
                 ("carried_main", bds.load_prev_year_ago(MAIN_TW_PATH))]
    fye_cache = seed_fye_cache(load_fye_cache(), prev_wide, main_tw)
    today = _taipei_today()
    last_net = [0.0]

    def paced(fn, *a):
        wait = YA_FETCH_GAP - (time.time() - last_net[0])
        if wait > 0:
            time.sleep(wait)
        try:
            return fn(*a)
        finally:
            last_net[0] = time.time()

    def fetch(ticker):
        return {} if args.no_network_year_ago else bds._fetch_year_ago_light(ticker)

    t0 = time.time()
    stocks = []
    for code in codes:
        listing = resolved.get(code)
        ticker = (listing or {}).get("ticker") or code
        hit = fye_cache.get(ticker) or {}
        stale = not hit.get("last_fye") or bds._fye_to_date(hit.get("checked")) is None
        if not stale:
            stale = (today - bds._fye_to_date(hit["checked"])).days >= 180
        last_fye = (hit.get("last_fye") if not stale or args.no_network_year_ago
                    else paced(get_last_fye, ticker, ticker, fye_cache))
        cur_fye = bds.year_ago_fye(last_fye, today) if last_fye else None
        ya = pick_year_ago(code, ticker, cur_fye, prev_rows,
                           lambda t: paced(fetch, t), bds.decide_year_ago_carry)
        stocks.append(build_row(code, snap.tickers[code], listing, rate, ya, last_fye, bds._koyfin_eps_growth))

    src = [s["eps_year_ago_source"] for s in stocks]
    now = datetime.now(timezone(timedelta(hours=8)))
    doc = {
        "schema_version": SCHEMA_VERSION,
        "run_timestamp": now.isoformat(timespec="seconds"),
        "as_of": snap.snapshot_date,
        "universe_mode": "tw_wide",
        "universe_size": len(stocks),
        "display_fx": {"currency": "TWD", "local_per_usd": round(float(rate), 4), "as_of": snap.snapshot_date, "source": fx_src,
                       "applies_to": "eps_fy_curr / eps_fy_next / eps_fy3 converted from Koyfin USD; *_usd_orig keeps USD"},
        "note": NOTE,
        "eps_estimates_source": {"snapshot_date": snap.snapshot_date, "source_file": xlsx.name},
        "eps_year_ago_summary": {k or "none": src.count(k) for k in dict.fromkeys(src)},
        "unresolved": unresolved,
        "stocks": stocks,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"[tw-wide] wrote {args.out} universe={len(stocks)} fx={rate:.4f} year_ago={doc['eps_year_ago_summary']} "
          f"unresolved={len(unresolved)} ({time.time() - t0:.0f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
