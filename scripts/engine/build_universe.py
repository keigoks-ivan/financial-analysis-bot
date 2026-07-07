#!/usr/bin/env python3
"""決策引擎 L0 — 雷達 universe 名單（三指數 ∪ DD 池美國上市）.

v1.1 持有人 2026-07-04 拍板：排除 S&P 600 小型股（噪音多、不符合 mandate 的 size floor）；
母體 = 大型（sp500 ∪ ndx100）＋中型（sp400），約 920 檔。
v1.2 持有人 2026-07-08 拍板：納入 DD 池（docs/dd-screener/latest.json）美國上市全員
（tier=ddpool，約 +54 檔）——起因 TSM（核心持倉 ADR）對雷達隱形；機械規則零人工圈選，
隨研究池自動維護。外國掛牌（含「.」後綴如 2330.TW）仍排除；小型股由下游 GRP 板
市值閘（≥$20B）續擋，雷達層放行供衛星/循環發現。
來源 Wikipedia 成分股表 ∪ DD 池 → data/engine/universe.json（含 sector 與層級）。
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
DD_POOL = ROOT / "docs" / "dd-screener" / "latest.json"

WIKI = {
    "sp500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "ndx100": "https://en.wikipedia.org/wiki/Nasdaq-100",
    "sp400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
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
            sym = "symbol" if "symbol" in cols else ("ticker" if "ticker" in cols else None)
            if sym is None:
                continue
            tbl.columns = [str(c).strip().lower() for c in tbl.columns]
            sec = "gics sector" if "gics sector" in tbl.columns else None
            for _, r in tbl.iterrows():
                t = str(r[sym]).strip()
                if not t or t in seen:
                    continue   # 重疊（ndx100 ∩ sp500）保留先見層級
                seen.add(t)
                rows.append({"ticker": t, "sector": str(r[sec]) if sec else "",
                             "tier": tier})
            break
    if len(rows) < 750:   # sanity：三表齊全應 ~920
        raise RuntimeError(f"成分股僅 {len(rows)} 檔，疑似表結構變動 — 保留舊檔")
    seen = {r["ticker"] for r in rows}
    rows.extend(dd_pool_extras(seen))
    return rows


def dd_pool_extras(seen: set[str]) -> list[dict]:
    """DD 池美國上市、不在三指數者（universe v1.2）。池檔缺失時不擋主流程。"""
    try:
        data = json.loads(DD_POOL.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"⚠ DD 池讀取失敗（{e}）— 本輪僅三指數")
        return []
    pool = data if isinstance(data, list) else data.get("rows") or data.get("stocks") or []
    extras = []
    for r in pool:
        t = str(r.get("ticker", "")).strip()
        if not t or t in seen or "." in t:   # 外國掛牌（.TW 等）排除
            continue
        seen.add(t)
        extras.append({"ticker": t, "sector": "", "tier": "ddpool"})
    return extras


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
    tiers = {t: sum(1 for r in rows if r["tier"] == t) for t in [*WIKI, "ddpool"]}
    print(f"universe.json: {len(rows)} 檔 {tiers}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
