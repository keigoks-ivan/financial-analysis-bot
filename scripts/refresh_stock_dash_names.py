#!/usr/bin/env python3
"""更新 data/stock_dash_names.json（ticker → 公司全名），給 build_stock_dash.py 當備援。

GitHub Actions 的 IP 拿不到 yfinance Ticker.info，/stock-dash/ 頁首公司名稱會退成代號。
這支在本機跑（本機拿得到），對 docs/dd-screener/latest.json 的名單逐檔抓 longName／shortName；
抓不到的沿用表裡舊值，不會把已有名稱洗掉。名單有新股票時再跑一次即可。

用法：python3 scripts/refresh_stock_dash_names.py
"""
import json
import sys
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from dd_screener_quality import _yf_ticker_for  # noqa: E402  同 build_stock_dash.py 的代號對照（LVMH → MC.PA 等）
LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
OUT = ROOT / "data" / "stock_dash_names.json"


def main():
    tickers = [s["ticker"] for s in json.loads(LATEST.read_text(encoding="utf-8"))["stocks"]]
    names = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    got, miss = 0, []
    for t in tickers:
        try:
            info = yf.Ticker(_yf_ticker_for(t)).info or {}
        except Exception:  # noqa: BLE001
            info = {}
        name = info.get("longName") or info.get("shortName")
        if name:
            names[t] = name
            got += 1
        elif t not in names:
            miss.append(t)
    OUT.write_text(json.dumps(dict(sorted(names.items())), ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(f"抓到 {got}／{len(tickers)} 檔；表內共 {len(names)} 檔；缺：{', '.join(miss) or '無'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
