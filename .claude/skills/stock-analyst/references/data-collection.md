# stock-analyst v14.7 — data-collection.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

## 【即時數據協議】（yfinance-first 批量採集）

**執行順序強制規則**：① 第一步（強制）執行「yfinance 批量採集腳本」一次抓齊所有可由 yfinance 提供的資料;② 第二步（僅補漏）針對 yfinance 無法提供的執行 web_search（降至 6-8 次）;③ 禁止對 yfinance 已涵蓋的項目重複 web_search。

### yfinance 涵蓋範圍（禁止用 web_search 重搜）

| 類別 | 項目 |
|:---|:---|
| 價格 | current, 52W H/L, 歷史週線 OHLC（6 年）、近 5 日日線 OHLC |
| 技術指標 | W52 / W104 / W250 SMA、W250 斜率（13 週）、Bollinger Band 2σ |
| 估值 | Forward PE, Trailing PE, EV/EBITDA, Beta, Market Cap |
| 預估 | FY+1 / FY+2 EPS 共識（+ 修正軌跡）、Revenue estimates |
| 財報 | 5 年 Income / Balance / Cashflow |
| 股權 | insider %, institutional %, top holders |
| 事件 | 下次財報日期 |
| 大盤 | ^GSPC / ^TWII 週線 W104 判定系統性風險 |

### web_search 必查（yfinance 無法提供）

| 類別 | 關鍵字範例 |
|:---|:---|
| 5Y Forward P/E 歷史分位 | `[ticker] forward PE history Macrotrends` / GuruFocus |
| 同業當前估值倍數 | `[competitor] forward PE EV/EBITDA 2026` |
| 重大事件（M&A、訴訟、臨床）| `[ticker] acquisition lawsuit 2026`（QC-19） |
| 競爭者新品 / 產業趨勢 | QC-12 產業掃描 |
| 分析師目標價 consensus | `[ticker] price target analyst consensus` |
| 5Y 平均 ROIC、毛利率 | `[ticker] ROIC history Macrotrends` |
| TradingView Beta | `[ticker] beta TradingView`（QC-25 雙源驗證）|
| **§11.5 IRR 用** | `[ticker] 5-year forward PE band` + `[ticker] EPS consensus FY+3 long-term growth`（IRR re-rate 與 EPS CAGR 基底，同輪搜得） |
| **QC-39 產業態勢變化（雙向，強制）** | 競爭惡化:`[ticker] market share gaining OR losing 2026` + `[ticker] largest customer second-source OR in-house` + `[competitor] design win at [ticker's customer]` + `[ticker] new entrant 2026`；結構 durability:`[industry] shortage OR oversupply structural OR cyclical 2026 2027` + `[industry] supply discipline new capacity timeline` + `[ticker product] demand durability AI structural`（完整規格見 QC-39） |

### yfinance 批量採集腳本（強制第一步）

```python
import yfinance as yf
import numpy as np

ticker = "TICKER_PLACEHOLDER"  # 替換為實際標的（台股用 "2330.TW" 格式）
t = yf.Ticker(ticker)
info = t.info

# 1. 基本資訊
print("=== 基本資訊 ===")
for k in ['currentPrice', 'regularMarketPrice', 'marketCap', 'fiftyTwoWeekHigh',
          'fiftyTwoWeekLow', 'forwardPE', 'trailingPE', 'enterpriseToEbitda',
          'priceToBook', 'bookValue',  # 循環/商品股 P/B 錨（QC-42 附錄 B；非循環股忽略即可）
          'beta', 'heldPercentInsiders', 'heldPercentInstitutions']:
    print(f"{k}: {info.get(k)}")

# 2. EPS / Revenue 共識
print("\n=== EPS Estimates ===")
print(t.earnings_estimate)  # 0q, +1q, 0y (FY+1), +1y (FY+2)
print("\n=== EPS Trend（7/30/60/90d 修正軌跡）===")
print(t.eps_trend)
print("\n=== Revenue Estimate ===")
print(t.revenue_estimate)

# 3. 財務三表（多年）— flagship 深度模組所需全欄一次抓齊（robust 逐行，缺行不報錯）
#    §8.E DuPont/CCC 需:Pretax/Tax(NOPAT)、AR/Inventory/AP(CCC)、Total Assets/Invested Capital(DuPont)
#    §10.D 資本配置需:D&A、Dividends Paid、Repurchase
def _dump(df, keys, title):
    print(f"\n=== {title} ===")
    if df is None or df.empty:
        print("N/A"); return
    for k in keys:
        try: print(k, "=", [round(float(v)/1e9,2) if v==v else None for v in df.loc[k].values])
        except Exception: pass  # 該公司無此行（如金融股無 Gross Profit）→ 跳過不報錯
_dump(t.income_stmt, ['Total Revenue','Gross Profit','Operating Income','Pretax Income',
                      'Tax Provision','Net Income','Diluted EPS'], "Income Statement (TWD/USD bn)")
_dump(t.balance_sheet, ['Cash And Cash Equivalents','Accounts Receivable','Receivables','Inventory',
                        'Accounts Payable','Total Debt','Stockholders Equity','Total Assets',
                        'Invested Capital','Working Capital'], "Balance Sheet")
_dump(t.cashflow, ['Operating Cash Flow','Capital Expenditure','Free Cash Flow',
                   'Depreciation And Amortization','Cash Dividends Paid',
                   'Repurchase Of Capital Stock'], "Cash Flow")

# 4. 週線 MA + Bollinger + 近 5 日 intraday
weekly = yf.download(ticker, period="6y", interval="1wk", auto_adjust=True, progress=False)
closes = weekly['Close'].values.flatten()
current = float(closes[-1])
w52 = float(np.mean(closes[-52:])) if len(closes) >= 52 else None
w104 = float(np.mean(closes[-104:])) if len(closes) >= 104 else None
w250 = float(np.mean(closes[-250:])) if len(closes) >= 250 else None
slope_pct = (w250 / float(np.mean(closes[-263:-13])) - 1) * 100 if len(closes) >= 263 else None
sma20 = float(np.mean(closes[-20:]))
std20 = float(np.std(closes[-20:], ddof=0))

print(f"\n=== MA / Bollinger ===")
print(f"現價: {current:.2f}")
print(f"W52: {w52:.2f}" if w52 else "W52: N/A（樣本不足）")
print(f"W104: {w104:.2f}" if w104 else "W104: N/A")
print(f"W250: {w250:.2f}" if w250 else "W250: N/A")
print(f"W250 斜率（13w）: {slope_pct:.2f}%" if slope_pct else "W250 斜率: N/A")
print(f"BB 上/中/下: {sma20+2*std20:.2f} / {sma20:.2f} / {sma20-2*std20:.2f}")

# 5. 近 5 交易日 OHLC（QC-24 intraday 訊號）
daily5 = yf.download(ticker, period="10d", interval="1d", auto_adjust=False, progress=False)
print(f"\n=== 近 5 交易日 OHLC ===")
print(daily5.tail(5)[['Open', 'High', 'Low', 'Close', 'Volume']])

# 6. 大盤豁免檢查（附錄 A 必需）
idx = "^TWII" if ticker.endswith(".TW") else "^GSPC"
idx_w = yf.download(idx, period="3y", interval="1wk", auto_adjust=True, progress=False)
idx_closes = idx_w['Close'].values.flatten()
idx_current = float(idx_closes[-1])
idx_w104 = float(np.mean(idx_closes[-104:]))
print(f"\n=== 大盤 {idx} ===")
print(f"現價 vs W104: {idx_current:.2f} vs {idx_w104:.2f} | 破線: {idx_current < idx_w104}")
```

**執行上述腳本後**，所有 §4、§5、§8、§10、§11、附錄 A 需要的原始數據均已取得。進入各章節撰寫時直接引用，不得針對同一項目再 web_search。

### 報告頂部必須標註

資料抓取時間 ｜ 最新股價 ｜ 最近財報季 ｜ yfinance 採集 + 補充 web_search 次數

---

