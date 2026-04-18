# Portfolio Data

這個目錄是 CCR 遠端 PM agent 的資料來源。

## 檔案

| 檔案 | 產生者 | 用途 |
|:---|:---|:---|
| `watchlist.txt` | 手動編輯 | 強制納入 PM 候選池的 ticker（一行一檔，# 開頭為註解） |
| `prices.json` | GitHub Actions | 最新一次收盤現價 + 前日 close + 成交量 |
| `history.json` | GitHub Actions | 近 300 日 OHLC，供 PM 計算 W52 / W104 MA |
| `current_holdings.yaml` | 手動編輯 | 當前持倉（ticker × cost × current_pct × tier） |

## GitHub Actions 取價流程

`.github/workflows/fetch_portfolio_prices.yml` 每週六 UTC 00:30 執行：

1. 解析 `docs/dd/INDEX.md` 抽 v11+ DD 的所有 ticker
2. 加上 `watchlist.txt` 與三個 benchmark（^GSPC, ^NDX, ^TWII）
3. 用 yfinance 抓現價 + 300 日歷史
4. 輸出至 `prices.json` / `history.json`
5. 自動 commit + push

## 為什麼需要

Anthropic CCR 遠端環境有出站白名單，無法直接打 Yahoo Finance / Finnhub / Stooq。
改由 GitHub Actions（雲端無封鎖）當「資料管家」先把資料推進 repo，
CCR 遠端 PM agent clone repo 時就有最新資料，無需對外發起 HTTP 請求。

這對應 PM skill 的哲學：**分析師 / 基金經理人分工** — 資料層（yfinance via GHA）與決策層（CCR PM agent）獨立。
