#!/usr/bin/env python3
"""每日 closes 切片寫入器（CI 用，輕量）。

定位：在 GitHub Actions（fresh runner，無持久 cache）上**只抓今日收盤**，把 universe
226 檔的單日收盤寫成一支小 JSON（~4.6 KB），commit 進 repo。配合 run_study.py --rebuild
在本機把「本機全歷史 base + repo 累積切片」併成最新寬表。

刻意不呼叫 price_cache.load_prices（那會在 runner 上建 period=max 全歷史快取，每天重抓
~16k 根 × 226 檔，浪費）。改用 _chunked_download(period="5d") 取最近數根、抓最後一根
收盤即可——沿用生產的 chunk + retry/backoff 韌性。

輸出：docs/dd-screener/state-machine/data/study/closes_daily/{as_of}.json
  { schema_version, run_timestamp, as_of, n_tickers, closes:{tk:{date,close}}, missing[] }

split 註記：本切片存當日 auto_adjust 收盤；日後若拆股，base 歷史會被 yfinance 重新
調整，切片 forward-stitch 不會回頭重算 → 尾段可能有微幅 split 漂移。需 split-exact
全歷史時，本機定期改跑 run_study.py（預設 / --refresh-only，走 price_cache split 偵測）
重新 baseline 即可。永不 raise（CI 容錯）。
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STUDY_DIR = Path(__file__).resolve().parent
ENGINE_DIR = STUDY_DIR.parent
sys.path.insert(0, str(STUDY_DIR))
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent))   # scripts/ — dd_screener_quality ticker maps

import config as CFG  # noqa: E402
from price_cache import _chunked_download, _extract  # noqa: E402
from run_daily import _yf_ticker, load_universe  # noqa: E402

CLOSES_DAILY = CFG.DATA_DIR / "study" / "closes_daily"


def main() -> int:
    universe = load_universe()
    symbols = [u["symbol"] for u in universe]
    yf_map = {s: _yf_ticker(s) for s in symbols}
    print(f"  universe: {len(symbols)} symbols", file=sys.stderr)

    raw = _chunked_download(list(yf_map.values()), period="5d")
    if raw.empty:
        print("  ERROR: 抓不到任何收盤（download 全空）— 不寫切片", file=sys.stderr)
        return 0   # CI 容錯：不 raise，讓其他 step 照跑

    single = (len(yf_map) == 1)
    closes, missing = {}, []
    for s in symbols:
        df = _extract(raw, yf_map[s], single)
        if df is None or "Close" not in df.columns:
            missing.append(s)
            continue
        c = df["Close"].dropna()
        if c.empty:
            missing.append(s)
            continue
        closes[s] = {"date": c.index[-1].strftime("%Y-%m-%d"),
                     "close": round(float(c.iloc[-1]), 6)}

    if not closes:
        print("  ERROR: 226 檔皆無有效收盤 — 不寫切片", file=sys.stderr)
        return 0

    as_of = max(v["date"] for v in closes.values())
    payload = {
        "schema_version": "1.0",
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": as_of,
        "n_tickers": len(closes),
        "closes": dict(sorted(closes.items())),
        "missing": sorted(missing),
    }
    CLOSES_DAILY.mkdir(parents=True, exist_ok=True)
    out = CLOSES_DAILY / f"{as_of}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  切片 → {out}  ({len(closes)} 檔, missing {len(missing)})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
