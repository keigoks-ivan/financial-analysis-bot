#!/usr/bin/env python3
"""池外贏家稽核（宇宙入池盲區）— 季度手動跑一次.

回看鏡（pipeline 頁 step 5）只審「池內名字有沒有 DD」，看不到池外贏家。
本腳本補上游：拿 S&P 1500（500+400+600，機構可投資的 size floor）當全市場代理，
算 12M 報酬 top N，對照 dd-screener 宇宙（latest.json 240 檔）——
「漲最多的名字裡，有多少根本不在我的池子裡」。

口徑：
  - 12M 報酬 = close[-1]/close[-53]（週線，repo 回看鏡同慣例）
  - 名單來源 Wikipedia 成分股表；BRK.B 型 ticker 轉 yfinance 的 BRK-B
  - 池內判定：ticker 在 latest.json（US 無後綴）或 data/weekly_cache/ 有檔

Usage:
  python3 scripts/audit_universe_intake.py            # top 50
  python3 scripts/audit_universe_intake.py --top 100
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"
WEEKLY_CACHE_DIR = ROOT / "data" / "weekly_cache"

WIKI = {
    "sp500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "sp400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "sp600": "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
}
UA = {"User-Agent": "Mozilla/5.0 (universe-intake-audit; local research script)"}


def fetch_constituents() -> pd.DataFrame:
    import urllib.request
    frames = []
    for idx, url in WIKI.items():
        req = urllib.request.Request(url, headers=UA)
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
        for tbl in pd.read_html(io.StringIO(html)):
            cols = {str(c).strip().lower() for c in tbl.columns}
            if "symbol" in cols and ("gics sector" in cols or "security" in cols or "company" in cols):
                tbl.columns = [str(c).strip().lower() for c in tbl.columns]
                sec_col = "gics sector" if "gics sector" in tbl.columns else None
                out = pd.DataFrame({
                    "ticker": tbl["symbol"].astype(str).str.strip(),
                    "sector": tbl[sec_col].astype(str) if sec_col else "",
                    "index": idx,
                })
                frames.append(out)
                break
        else:
            print(f"⚠ {idx}: 找不到成分股表，跳過", file=sys.stderr)
    df = pd.concat(frames).drop_duplicates(subset="ticker")
    return df


def returns_12m(tickers: list[str]) -> dict[str, float]:
    import yfinance as yf
    out: dict[str, float] = {}
    CHUNK = 250
    for i in range(0, len(tickers), CHUNK):
        chunk = tickers[i:i + CHUNK]
        data = yf.download(chunk, period="13mo", interval="1wk",
                           progress=False, auto_adjust=True, group_by="column")
        closes = data["Close"] if "Close" in data else data
        if isinstance(closes, pd.Series):
            closes = closes.to_frame(chunk[0])
        for t in closes.columns:
            s = closes[t].dropna()
            if len(s) >= 53 and s.iloc[-53] > 0:
                out[str(t)] = float(s.iloc[-1] / s.iloc[-53] - 1.0)
        print(f"  …{min(i + CHUNK, len(tickers))}/{len(tickers)}", file=sys.stderr)
    return out


def load_universe() -> set[str]:
    tickers: set[str] = set()
    try:
        latest = json.loads(LATEST_JSON.read_text(encoding="utf-8"))
        tickers |= {s["ticker"] for s in latest.get("stocks", [])}
    except (OSError, json.JSONDecodeError):
        print("⚠ latest.json 讀不到，只用 weekly_cache 判定池內", file=sys.stderr)
    tickers |= {p.stem for p in WEEKLY_CACHE_DIR.glob("*.json")}
    return tickers


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=50)
    args = ap.parse_args()

    cons = fetch_constituents()
    print(f"成分股 {len(cons)} 檔（500/400/600 = "
          f"{(cons['index'] == 'sp500').sum()}/{(cons['index'] == 'sp400').sum()}/{(cons['index'] == 'sp600').sum()}）")

    yf_map = {t: t.replace(".", "-") for t in cons["ticker"]}
    rets = returns_12m(list(yf_map.values()))

    universe = load_universe()
    rows = []
    for t, yft in yf_map.items():
        r = rets.get(yft)
        if r is None:
            continue
        rec = cons[cons["ticker"] == t].iloc[0]
        rows.append({"ticker": t, "ret": r, "sector": rec["sector"], "idx": rec["index"],
                     "in_universe": t in universe or yft in universe})
    rows.sort(key=lambda x: -x["ret"])
    top = rows[:args.top]

    blind = [r for r in top if not r["in_universe"]]
    print(f"\n12M 報酬 top {args.top}（S&P1500 代理全市場）：池外 {len(blind)} 檔 / 池內 {len(top) - len(blind)} 檔\n")
    print(f"{'#':>3} {'ticker':<8} {'12M':>8}  {'池':<6} {'idx':<6} sector")
    for i, r in enumerate(top, 1):
        mark = "✅" if r["in_universe"] else "🔭盲區"
        print(f"{i:>3} {r['ticker']:<8} {r['ret'] * 100:>+7.0f}%  {mark:<5} {r['idx']:<6} {r['sector']}")

    if blind:
        print("\n🔭 池外盲區清單（候選入池研究，非買入清單）：")
        print("   " + "、".join(f"{r['ticker']}({r['ret'] * 100:+.0f}%)" for r in blind))
    return 0


if __name__ == "__main__":
    sys.exit(main())
