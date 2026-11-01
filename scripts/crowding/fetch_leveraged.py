#!/usr/bin/env python3
"""fetch_leveraged.py — 四檔槓桿 ETF（TQQQ／SQQQ／SOXL／SOXS）每日流通單位數與 NAV。

輸出：data/crowding_monitor/leveraged_etf_daily.csv，欄位 date,etf,shares,nav。
  date   = 發行商資料的 as-of 日（YYYY-MM-DD）
  shares = 流通單位數（整數）
  nav    = 每單位淨值（小數）
同一 (date, etf) 只一列；重跑不重複，已有的列不改。任一檔抓不到只印警告、跳過，
腳本永遠 exit 0（CI 以 `|| echo ::warning::` 包著，且不寫 None／空值列）。
只用標準函式庫（urllib／csv）。

來源（2026-11-01 實測，皆免登入、免瀏覽器）
==========================================

1. ProShares（TQQQ、SQQQ）— 官方基金資料檔，有完整歷史
   https://accounts.profunds.com/etfdata/ByFund/{TICKER}-historical_nav.csv
   （ProShares 官網基金頁的 "Historical NAV" 下載連結就是這個）
   欄位：Date,ProShares Name,Ticker,NAV,Prior NAV,NAV Change (%),NAV Change ($),
         Shares Outstanding (000),Assets Under Management
   日期格式 MM/DD/YYYY，最新一列在最上面。as-of 日 = Date 欄（就是 NAV 的計價日，
   例：Date=10/30/2026 → NAV 61.9682、Shares Outstanding (000)=531750、AUM=32.95B，
   NAV×單位數與 AUM 對得上）。shares = 欄位值 × 1000。
   本腳本只取最新一列；檔內有歷史，若要回補可再加。

2. Direxion（SOXL、SOXS）— 每日持股檔，沒有 NAV 欄，NAV 由持股反推
   https://www.direxion.com/holdings/{TICKER}.csv
   回應格式：前幾行是 fund 名稱、代號、`Shares Outstanding:237300060`（直接給流通單位數），
   空行後才是 CSV 表頭 "TradeDate","AccountTicker","StockTicker","SecurityDescription",
   "Shares","Price","MarketValue","Cusip","HoldingsPercent"。
   需要瀏覽器式 User-Agent 才回 200（用 urllib 預設 UA 不保證；本腳本帶一般 UA）。
   Direxion 基金頁（/product/...）有 Cloudflare 擋 bot（403），故不使用，也沒有公開的 NAV
   歷史檔 → 只能從持股檔反推 NAV。
   - as-of 日：TradeDate 欄是「檔案發布日」，內容其實是前一個交易日收盤（實測：
     TradeDate=10/30 的檔，AMD 價格 566.42 = 10/29 收盤，而 10/30 收盤是 504.80）。
     所以 as-of = TradeDate 往前推一個平日（週一的檔 → 上週五）。
     限制：遇美國假日隔天會差一天，沒有處理。
   - NAV 反推：Direxion 每日收盤把曝險調回 ±3 倍淨資產，故
       淨資產 ≈ (非現金部位市值合計) ÷ 槓桿倍數（SOXL +3、SOXS -3），NAV = 淨資產 ÷ 流通單位數。
     現金 = StockTicker 為空且 Price=1.0 的貨幣市場／附買回列；其餘（個股與 ICESEMI swap
     名目本金）算曝險。實測驗證：SOXL 推得 102.45，同日 Yahoo 收盤 102.39；
     SOXS 推得 41.70，Yahoo 收盤 41.68（誤差 <0.1%）。這是近似值，不是官方 NAV，
     因為 swap 未實現損益不在檔內；單位數是官方值。

限制
====
只有「當天快照」：ProShares 檔內有歷史但本腳本只取最新一列；Direxion 完全沒有歷史，
漏跑的日子補不回來（所以 CI 要每個工作日跑）。
"""
import csv
import io
import os
import sys
import urllib.request
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "data", "crowding_monitor", "leveraged_etf_daily.csv")
FIELDS = ["date", "etf", "shares", "nav"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

PROSHARES = ["TQQQ", "SQQQ"]
DIREXION = {"SOXL": 3.0, "SOXS": -3.0}  # ticker -> 槓桿倍數


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8-sig", errors="replace")


def prev_weekday(d):
    d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def fetch_proshares(tk):
    text = http_get(f"https://accounts.profunds.com/etfdata/ByFund/{tk}-historical_nav.csv")
    best = None
    for row in csv.DictReader(io.StringIO(text)):
        if (row.get("Ticker") or "").strip().upper() != tk:
            continue
        try:
            d = datetime.strptime(row["Date"].strip(), "%m/%d/%Y").date()
            nav = float(row["NAV"])
            shares = int(round(float(row["Shares Outstanding (000)"].replace(",", "")) * 1000))
        except (KeyError, ValueError, AttributeError):
            continue
        if nav > 0 and shares > 0 and (best is None or d > best[0]):
            best = (d, shares, nav)
    if not best:
        raise ValueError("no valid row")
    return best


def fetch_direxion(tk, lev):
    text = http_get(f"https://www.direxion.com/holdings/{tk}.csv")
    lines = text.splitlines()
    shares = None
    start = None
    for i, ln in enumerate(lines):
        if ln.lower().startswith("shares outstanding"):
            shares = int(float(ln.split(":", 1)[1].strip().replace(",", "")))
        if ln.startswith('"TradeDate"') or ln.startswith("TradeDate"):
            start = i
            break
    if not shares or start is None:
        raise ValueError("header not found")
    exposure = 0.0
    trade_date = None
    for row in csv.DictReader(io.StringIO("\n".join(lines[start:]))):
        try:
            mv = float(row["MarketValue"])
            px = float(row["Price"])
            td = datetime.strptime(row["TradeDate"].split()[0], "%m/%d/%Y").date()
        except (KeyError, ValueError, AttributeError, IndexError):
            continue
        trade_date = td
        is_cash = not (row.get("StockTicker") or "").strip() and abs(px - 1.0) < 1e-9
        if not is_cash:
            exposure += mv
    if trade_date is None or exposure == 0:
        raise ValueError("no usable holdings rows")
    nav = exposure / lev / shares
    if nav <= 0:
        raise ValueError(f"derived nav {nav:.4f} not positive")
    return prev_weekday(trade_date), shares, round(nav, 2)


def load_existing():
    seen = set()
    if os.path.exists(OUT):
        with open(OUT, newline="") as f:
            for r in csv.DictReader(f):
                seen.add((r["date"], r["etf"]))
    return seen


def main():
    seen = load_existing()
    new_rows = []
    jobs = [(tk, lambda tk=tk: fetch_proshares(tk)) for tk in PROSHARES]
    jobs += [(tk, lambda tk=tk, lev=lev: fetch_direxion(tk, lev)) for tk, lev in DIREXION.items()]
    for tk, fn in jobs:
        try:
            d, shares, nav = fn()
        except Exception as e:  # 單檔失敗不擋其他檔
            print(f"WARNING: {tk} fetch failed: {e}", file=sys.stderr)
            continue
        key = (d.isoformat(), tk)
        print(f"{tk}: date={key[0]} shares={shares} nav={nav} "
              f"(approx AUM ${shares * nav / 1e9:.2f}B)")
        if key in seen:
            print(f"  {tk} {key[0]} already in csv, skipped")
            continue
        seen.add(key)
        new_rows.append({"date": key[0], "etf": tk, "shares": shares, "nav": nav})
    if new_rows:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        exists = os.path.exists(OUT) and os.path.getsize(OUT) > 0
        if exists:  # 確保前一列有換行再 append
            with open(OUT, "rb") as f:
                f.seek(-1, os.SEEK_END)
                needs_nl = f.read(1) != b"\n"
        else:
            needs_nl = False
        with open(OUT, "a", newline="") as f:
            if needs_nl:
                f.write("\n")
            w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
            if not exists:
                w.writeheader()
            w.writerows(new_rows)
    print(f"appended {len(new_rows)} row(s) to {OUT}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # 任何意外都不讓 CI 非零結束
        print(f"WARNING: fetch_leveraged unexpected error: {e}", file=sys.stderr)
    sys.exit(0)
