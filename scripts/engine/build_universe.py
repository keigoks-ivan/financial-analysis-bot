#!/usr/bin/env python3
"""決策引擎 L0 — 雷達 universe 名單（S&P 500 + 400 + 600 ≈ 1,500 檔）.

來源 Wikipedia 成分股表 → data/engine/universe.json（含 sector 與指數層級）。
Fail-safe：抓取失敗時保留舊檔（雷達照跑上一版名單），月更即可。

Usage: python3 scripts/engine/build_universe.py
"""
from __future__ import annotations

import io
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "data" / "engine" / "universe.json"

WIKI = {
    "sp500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "sp400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "sp600": "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
}
UA = {"User-Agent": "Mozilla/5.0 (imq-engine-universe; research script)"}


def fetch() -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    for tier, url in WIKI.items():
        req = urllib.request.Request(url, headers=UA)
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
        for tbl in pd.read_html(io.StringIO(html)):
            cols = {str(c).strip().lower() for c in tbl.columns}
            if "symbol" not in cols:
                continue
            tbl.columns = [str(c).strip().lower() for c in tbl.columns]
            sec = "gics sector" if "gics sector" in tbl.columns else None
            for _, r in tbl.iterrows():
                t = str(r["symbol"]).strip()
                if not t or t in seen:
                    continue
                seen.add(t)
                rows.append({"ticker": t, "sector": str(r[sec]) if sec else "",
                             "tier": tier})
            break
    if len(rows) < 1200:   # sanity：三表齊全應 ~1500
        raise RuntimeError(f"成分股僅 {len(rows)} 檔，疑似表結構變動 — 保留舊檔")
    return rows


def main() -> int:
    try:
        rows = fetch()
    except Exception as e:
        if OUT.exists():
            print(f"⚠ universe 抓取失敗（{e}）— 保留舊檔")
            return 0
        raise
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n": len(rows), "tickers": rows,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    tiers = {t: sum(1 for r in rows if r["tier"] == t) for t in WIKI}
    print(f"universe.json: {len(rows)} 檔 {tiers}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
