# stock-analyst v14.7 — data-collection.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-07 v14.7 結構拆分，內容自 v14.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。
>
> **2026-08-07 更新**：機械數據採集層改為 **fan-out 給採集 agent**——writer 不再自跑 yfinance 腳本與機械類 web_search，改為 spawn 一個 sonnet 採集 agent，只收回**結構化數字包**（≤6KB）。原「writer 自跑」協議全文保留於本檔【fallback】段，僅在 spawn 連續失敗 2 次時啟用。判斷性搜尋（QC-39／QC-12／Munger／QC-19 深查）**不外包**，仍由 writer 執行。

## 【即時數據協議】（fan-out 採集 agent；writer 只收數字包）

**執行順序強制規則**：① 第一步（強制）spawn **一個**採集 agent（sonnet），由它跑 yfinance 批量腳本＋機械類 web_search＋QC-19 事件初掃，回傳結構化數字包；② 第二步 writer 收到數字包後，**只**對缺項或自相矛盾項補查；③ **禁止** writer 自跑腳本、禁止對數字包已涵蓋的機械項重複 web_search；④ 判斷性搜尋與判斷性閱讀由 writer 自行執行，不進採集 agent 的派工單。

WHY：yfinance 腳本原始輸出（5 年三表 dump、6 年週線序列、共識修正軌跡）與機械搜尋原文，過去全部留在 writer 的 context 裡，而 writer 是上百輪的長 session——這些位元組會被之後每一輪工具呼叫 cache-read 重讀一次。改為 fan-out 後，writer context 只留數字包。

### 職責切分（誰做什麼；不得越界）

| 層 | 項目 | 誰做 |
|:---|:---|:---|
| 機械採集 | yfinance 批量腳本：價格／技術指標（W52・W104・W250・斜率・BB）／估值倍數／FY+1・FY+2 共識與修正軌跡／5 年三表／股權結構／下次財報日／大盤 W104 | 採集 agent |
| 機械搜尋 | 5Y Forward P/E 歷史分位、同業當前估值倍數、分析師目標價 consensus、5Y ROIC 與毛利率史、TradingView Beta（QC-25 雙源）、§10.5 IRR 用 forward PE band ＋ FY+3 EPS／長期成長共識 | 採集 agent |
| 事件初掃 | QC-19 重大事件**headline 清單**（日期＋一句話＋來源），**只列不解讀** | 採集 agent |
| 判斷性掃描 | **QC-39 產業態勢雙向掃描**（競爭惡化軸＋結構 durability 軸，三軸 ≥9 條）、**QC-12 產業掃描** | writer |
| 判斷性掃描 | **Munger 護城河維度搜尋協議**、**EPS CAGR 強制搜尋協議**中涉及口徑取捨與來源採信的部分 | writer |
| 判斷性閱讀 | **§8 財報 call 語氣解析**（讀原文本身就是判斷的一部分）、隨附逐字稿（§8.5）、前份 DD 的假設與觸發器、ID 事實區塊 | writer |
| 事件深查 | 對數字包 headline 清單中「**可能影響 thesis**」者的深查與定性（QC-19 本體） | writer |

界線一句話：**有唯一正確答案、派工前就問得死的＝採集 agent；需要先知道自己在找什麼才看得見答案的＝writer 自讀自搜。**

### spawn 模板（照抄即用；`{TICKER}` / `{PEERS}` / `{CUSTOMERS}` 換成實際值後直接送出）

````js
Agent({
  description: "Collect {TICKER} data pack",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `你是 stock-analyst DD 的機械數據採集 agent。標的：{TICKER}（yfinance 代碼；台股用 2330.TW、港股用 9988.HK 格式）。

你的職責是**採集與回報，零判斷**：不解讀、不評級、不下裁決、不外推、不以訓練知識代替查證。查不到就寫 N/A 並註明已試過哪些查詢詞。**回傳總量 ≤6KB，禁止回傳任何原始 dump（腳本 stdout 全文、網頁全文、表格未收斂的多年矩陣）。**

## 任務 1：執行 yfinance 批量腳本（用 Bash 跑一次，把結果收斂進回傳格式）

\`\`\`python
import yfinance as yf
import numpy as np

ticker = "{TICKER}"  # 台股用 "2330.TW" 格式
t = yf.Ticker(ticker)
info = t.info

# 1. 基本資訊
print("=== 基本資訊 ===")
for k in ['currentPrice', 'regularMarketPrice', 'marketCap', 'fiftyTwoWeekHigh',
          'fiftyTwoWeekLow', 'forwardPE', 'trailingPE', 'enterpriseToEbitda',
          'priceToBook', 'bookValue',  # 循環／商品股 P/B 錨（QC-42 附錄 B；非循環股忽略即可）
          'beta', 'heldPercentInsiders', 'heldPercentInstitutions']:
    print(f"{k}: {info.get(k)}")

# 1.5 財報時效閘（v15.2.4 新增；SNOW 2026-09-03 教訓：財報後次日跑 DD 用了財報前價格與共識）
print("\\n=== 財報時效 ===")
try:
    edates = t.earnings_dates
    last_earnings = edates[edates.index <= __import__("pandas").Timestamp.now(tz=edates.index.tz)].index.max()
except Exception:
    last_earnings = None
print(f"最近財報日: {last_earnings}")
if last_earnings is not None:
    trading_days_since = __import__("numpy").busday_count(last_earnings.date(), __import__("datetime").date.today())
    print(f"距今交易日數(概估): {trading_days_since}")
    if trading_days_since <= 3:
        print("⚠ earnings_recency: ≤3d —— 財報後價格與共識未穩定，見下方盤後/盤前價")
        print(f"postMarketPrice: {info.get('postMarketPrice')}")
        print(f"preMarketPrice: {info.get('preMarketPrice')}")
        print(f"regularMarketPrice(RTH收盤): {info.get('regularMarketPrice')}")

# 2. EPS / Revenue 共識
print("\\n=== EPS Estimates ===")
print(t.earnings_estimate)  # 0q, +1q, 0y (FY+1), +1y (FY+2)
print("\\n=== EPS Trend（7/30/60/90d 修正軌跡）===")
print(t.eps_trend)
print("\\n=== Revenue Estimate ===")
print(t.revenue_estimate)

# 3. 財務三表（多年）— flagship 深度模組所需全欄一次抓齊（robust 逐行，缺行不報錯）
#    §7.E DuPont/CCC 需要：Pretax/Tax(NOPAT)、AR/Inventory/AP(CCC)、Total Assets/Invested Capital(DuPont)
#    §9.D 資本配置需要：D&A、Dividends Paid、Repurchase
def _dump(df, keys, title):
    print(f"\\n=== {title} ===")
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

print(f"\\n=== MA / Bollinger ===")
print(f"現價: {current:.2f}")
print(f"W52: {w52:.2f}" if w52 else "W52: N/A（樣本不足）")
print(f"W104: {w104:.2f}" if w104 else "W104: N/A")
print(f"W250: {w250:.2f}" if w250 else "W250: N/A")
print(f"W250 斜率（13w）: {slope_pct:.2f}%" if slope_pct else "W250 斜率: N/A")
print(f"BB 上/中/下: {sma20+2*std20:.2f} / {sma20:.2f} / {sma20-2*std20:.2f}")

# 5. 近 5 交易日 OHLC（QC-24 intraday 訊號）
daily5 = yf.download(ticker, period="10d", interval="1d", auto_adjust=False, progress=False)
print(f"\\n=== 近 5 交易日 OHLC ===")
print(daily5.tail(5)[['Open', 'High', 'Low', 'Close', 'Volume']])

# 6. 大盤豁免檢查（附錄 A 必需）
idx = "^TWII" if ticker.endswith(".TW") else "^GSPC"
idx_w = yf.download(idx, period="3y", interval="1wk", auto_adjust=True, progress=False)
idx_closes = idx_w['Close'].values.flatten()
idx_current = float(idx_closes[-1])
idx_w104 = float(np.mean(idx_closes[-104:]))
print(f"\\n=== 大盤 {idx} ===")
print(f"現價 vs W104: {idx_current:.2f} vs {idx_w104:.2f} | 破線: {idx_current < idx_w104}")
\`\`\`

腳本若整支失敗（yfinance 429／欄位缺失），逐項回報哪些欄位 N/A，**不要**改用網頁估算填補價格或三表。若 W52/W104/W250 因樣本不足為 N/A，照實回報，不得用「雙年均值外推」或起訖平均代替（與下方 QC-2 的合法替代指標不同——後者是標註清楚的既定統計量，非臨時外推）。

**三項採集端計算（v15.2 新增，用既有數據算，非原始 dump）**：
- **QC-24 intraday 旗標**：近 5 交易日 OHLC（上方第 5 步）逐日檢查——shooting star＝(High−Close)/High > 5%（盤中衝高回落）；gap-up 收黑＝(Open−前日 Close)/前日 Close > 5% 且 Close < Open；各列命中日期；無命中寫「無」。
- **QC-25 Beta 雙源判定**：yfinance `beta`（第 1 步）vs TradingView Beta（任務 2 第 5 項 web_search）算差異 %；差異 >30% → 採較高值（保守）並註明理由，差異 ≤30% → 採 yfinance 值、TradingView 值列出供交叉核對。
- **QC-2 替代指標備注**：W104 因樣本不足（< 104 週，如 IPO 未滿 2 年）為 N/A 時，改算 W100 或 MA520d 並標「替代指標」；樣本足夠則本項寫「不適用」。

## 任務 2：機械 web_search 必查清單（合計 6-8 次；每項給數字＋來源 URL＋as-of）

1. **5Y Forward P/E 歷史分位** — \`{TICKER} forward PE history Macrotrends\` 或 GuruFocus（要現值＋5 年區間／中位數）
2. **同業當前估值倍數** — \`{PEERS} forward PE EV/EBITDA 2026\`（同業名單：{PEERS}）
3. **分析師目標價 consensus** — \`{TICKER} price target analyst consensus\`（avg／high／low／分析師家數）
4. **5Y 平均 ROIC 與毛利率史** — \`{TICKER} ROIC history Macrotrends\`
5. **TradingView Beta（QC-25 雙源）** — \`{TICKER} beta TradingView\`
6. **§10.5 IRR 用** — \`{TICKER} 5-year forward PE band\` ＋ \`{TICKER} EPS consensus FY+3 long-term growth\`

**一手數字優先序（2026-08-08，SHOP 稽核教訓）**：損益表關鍵行（營收／營業利益／淨利／EPS）一律以公司 8-K／新聞稿／財報 PDF 為準;yfinance 或聚合站數字與一手衝突時**取一手**，並在使用處註明差異來源。淨利增速與營業利益增速差 >20pp → 必查一次性項目（股權處分利得／稅務／出售資產），拆出本業口徑再進 §7/§8。SBC 與稀釋數字**不准以「yfinance 未回傳」交 N/A**——去 10-K/10-Q 拿。

## 任務 3：QC-19 重大事件初掃（只列 headline，嚴禁解讀）

\`{TICKER} acquisition OR lawsuit OR investigation OR recall OR guidance cut 2026\`，涵蓋近 12 個月。每則只給「日期｜一句話事實｜來源」。**不要判斷影響大小、不要說「對 thesis 有利／不利」**——那是委派者的工作。

\`{TICKER} top customers supplier agreement OR contract signed 2026\`＋\`{CUSTOMERS} custom chip OR component second source agreement 2026\`（近 90 天，每則 日期｜事實｜來源；\`{CUSTOMERS}\`＝spawn 時代入前三大客戶名，未知則用 ticker 名）。

## 任務 4：kill_watch 現況（2026-08-08 接線）

若 \`docs/detective/data/kill_watch.json\` 存在，grep 本 ticker 的條目（含 \`last_status\`／是否越線）附進資料包；讓「前次觸發器哪條已發火」是機器比對事實，供 QC-49／§14 引用，不靠 writer 翻舊檔散文。查無條目照實回報「查無」，不要用散文回填。

## 回傳格式（Markdown；逐節照填；總量 ≤6KB）

### 0. 頂部標註
資料抓取時間（含時區）｜最新股價（含幣別＋as-of）｜最近財報季｜下次財報日｜yfinance 呼叫成功與否＋web_search 次數｜**財報時效**（`earnings_recency`：最近財報日 vs 報告日相隔交易日數；≤3d 時附加標註，見下）

**若 `earnings_recency` ≤3 個交易日**，本節第一行加醒目警語：「⚠ 財報後 ≤3 天：估值層一律用財報後價格（盤後/盤前），共識 EPS 標『財報前快照，財報後共識未更新』，不得宣稱已納入財報後共識」；同時給 RTH 收盤價與 postMarketPrice/preMarketPrice 兩者（取不到 postMarketPrice/preMarketPrice 時標 N/A，並要求 writer 用 web_search「{ticker} after hours stock price {日期}」補查一次）。

### 1. §8 財報（最近季）
最近季營收／毛利／營益／EPS 與 YoY、QoQ（來源：yfinance income_stmt 或 quarterly，標 as-of）

### 2. §4·§7 財務品質（關鍵行 × 年，5 年緊湊表）
三張表各一個 Markdown 表格，**列＝腳本裡的 keys，欄＝年度**，單位標明（bn）。Income／Balance／Cash Flow 分開三表。缺行寫 N/A。**不要貼腳本 stdout。**

### 3. §9 資本配置
insider %／institutional %／top holders 前 3；股息、回購、capex、D&A 逐年（已在第 2 節表內者寫「見上表」不重複）

### 4. §10 估值與共識
現價（`earnings_recency` ≤3d 時取財報後最新價 postMarketPrice/preMarketPrice，並同列 RTH 收盤價供對照）／市值／Forward PE／Trailing PE／EV/EBITDA／P/B／Beta(yfinance)／Beta(TradingView)／52W H/L；
EPS 共識 FY+1／FY+2（avg、分析師數、YoY）；eps_trend 7/30/60/90d 修正方向；Revenue estimate；
web 補項逐條一行：**5Y Fwd PE 分位｜同業倍數｜目標價 consensus｜5Y ROIC 與毛利率｜5Y forward PE band｜FY+3 EPS 與長期成長共識**，每條後綴「查詢詞｜來源｜日期」

### 5. 附錄 A 技術狀態
現價／W52／W104／W250／W250 斜率(13w)／BB 上・中・下／近 5 交易日 OHLC（5 行）／大盤（^GSPC 或 ^TWII）現價 vs W104 與是否破線
**QC-24 intraday 旗標**：近 5 日 shooting star（(High−Close)/High > 5%）／gap-up 收黑（跳空 > 5% 且收黑）各列命中日期，無則「無」。
**QC-25 Beta 雙源判定**：yfinance 值／TradingView 值／差異 %／採用值（>30% 差異採較高值）。
**QC-2 替代指標備注**：W104 樣本足夠則「不適用」；不足則列 W100 或 MA520d 替代值並標「替代指標」。

### 6. 事件 headline 清單（QC-19 初掃）
表格：日期｜一句話｜來源。無事件寫「近 12 個月無命中」。

### 7. 採集缺口
逐項列出 N/A 的欄位、已嘗試的查詢詞、失敗原因。**不得用估算值填空。**
`
})
````

### 數字包規格（驗收標準）

- **按消費章節分節**：§8 財報／§4·§7 財務品質／§9 資本配置／§10 估值與共識／附錄 A 技術狀態／事件 headline 清單／採集缺口——writer 寫哪一章就翻哪一節，不需要重新解析。
- **每個數字帶來源與 as-of**。yfinance 來源可在每張表下方標一次「yfinance，抓取時間 YYYY-MM-DD HH:MM TZ」；**web_search 來的每一項各自附「查詢詞｜來源｜日期」一行**，不得合併省略。
- **三表多年數據收斂為「關鍵行 × 年」緊湊表**（沿用腳本現有 keys），**不回傳原始 dump**。
- **總量目標 ≤6KB。** 超出多半代表回傳了原始輸出或加了解讀，退回要求收斂。
- **頂部標註**（資料抓取時間｜最新股價｜最近財報季｜搜尋次數｜財報時效）由 writer 從數字包第 0 節**轉錄**至報告頂部，不另行查證、不改寫數字。**`earnings_recency` ≤3d 時，`price_at_dd`（dd-meta／頁首）一律取財報後最新價（postMarketPrice/preMarketPrice），並在 as-of 標「盤後」或「盤前」；共識 EPS 標「財報前快照」。**

### 缺項處置（禁止整包重做）

數字包某項為 N/A、或**自相矛盾**（典型：forwardPE × FY+1 EPS 推不回現價；Beta 雙源差 > 30%；三表某年缺行導致 DuPont 算不出）→ writer **只補查該項**（1-2 次 web_search 或單行 yfinance 呼叫），改動處在報告內標明「補查來源＋as-of」。**禁止**因為單項缺漏就重 spawn 採集 agent 或重跑整支腳本。

### fallback（採集 agent spawn 失敗 2 次）

spawn 連續失敗 2 次（agent 未回、回傳空、或回傳完全不符格式無法使用）→ writer 依本檔【fallback：writer 自跑協議】段執行，不再第 3 次 spawn。fallback 路徑的產出品質要求與數字包相同（同樣要有頂部標註與來源 as-of）。

### 【v16.2 新增】財報日來源與數字包扁平鍵（PANW 教訓）

- **財報日唯一來源＝公司 IR 新聞稿**（`investors.{company}.com` 或公司官網 IR 頁的正式新聞稿），媒體轉載／彙整站（如財經媒體標題頁）的日期不採；`numbers.latest_quarter_kpis.quarter` 與任何「最近財報日」欄位**必附該新聞稿 URL**。PANW 教訓：三方來源對財報日期（8/18 vs 9/1）不一致，最終須回查官方新聞稿定案。
- **數字包必須扁平**：`scripts/dd_numbers_extra.py` 已產出 `numbers.price_at_dd`／`numbers.price_as_of`／`numbers.earnings_recency` 三個扁平鍵（validate_evidence.py 必填）。採集 agent **只能在這三個鍵原地補值**（例如 yfinance 查詢失敗時用 web_search 補一個 price_at_dd），**不得改鍵名、不得把它們包進另一個巢狀物件**（例如塞進 `top_banner` 之類的自造結構）——PANW dry-run 就是回傳巢狀鍵，orchestrator 得手動機械對映。其餘欄位可自由巢狀，但這三個扁平鍵一律在 `numbers` 頂層原地存在。

### 【v16.2 新增】現價一律引 numbers.price_at_dd（CRDO 教訓）

**硬規則**：任何章節或子 agent 提到「現價」「trading at」時，一律引用 `numbers.price_at_dd`／`price_as_of`（`scripts/dd_numbers_extra.py` 由 yfinance 算好的錨），不得自行從網頁／聚合站抓一個「現價」數字寫進報告或 claim。市值、距 52 週高低點 % 同理，一律由 `numbers.price_at_dd` 換算，不得另查一個市值/現價數字。**理由**：CRDO 2026-09-04 一份聚合站顯示現價 $234，實為財報前舊價，財報後（9/2 財報，9/3 收盤）實際現價 $164.17，差 30%——聚合站的快取／未更新頁面是系統性風險，`numbers.price_at_dd` 是財報時效閘（見上方「財報時效」段）已處理過的唯一可信來源。

### 一致性紅利與時效

- **頁首儀表板與各章數字一律引用數字包的同一來源**（同一個現價、同一組共識、同一組倍數）。這是 QC-7 內部一致性最便宜的保證——分歧只可能來自 writer 的補查，而補查處都有標注。
- **時效閘**：數字包的抓取時間距離當下 **> 3 個交易日**（writer 中途中斷後重跑的典型情況）→ **重 spawn 採集 agent**取新包，不得沿用舊價格與舊共識寫估值章。

### 【v16.1 新增】最新一季官方 KPI（`numbers.latest_quarter_kpis.items[]`）

**WHY**：v16 兩次 dry-run critic 首輪 🔴 的共同模式是「判斷層引用比最新一季更舊的數字」——某段落引用的是財報前或上上季的 KPI，而不是最新一季官方公布值。此段把「最新一季 KPI」結構化成必填清單，讓判斷層只准引這一份，不得自己從逐字稿或舊報告裡東拼西湊。

**任務 5（新增，接在任務 3 之後）**：採集 agent 從最新一季財報新聞稿／10-Q／法說投影片，逐項填 `numbers.latest_quarter_kpis.items[]`，每項格式：

```json
{"metric": "Non-GAAP operating margin", "value": 23.4, "unit": "%",
 "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-09-02）",
 "source": "公司新聞稿 investor.snowflake.com Q2 FY27 press release",
 "vs_consensus": "consensus 21.8%（來源：dd_numbers_extra.py consensus_revision 或 web_search）",
 "prior_quarter": "Q1 FY2027: 21.1%"}
```

**通用必填（每份 DD 都要）**：
1. 營收（GAAP，含 YoY／QoQ）
2. Non-GAAP 營業利益／利益率
3. GAAP 營業利益／利益率
4. 自由現金流（FCF）
5. SBC 占營業利益（或占營收）%
6. 管理層對下一季／全年的指引（guidance，含區間）

**依 archetype 追加**（archetype_hint 對照 `coverage-axes.md` 分類）：
- **SaaS／未獲利高成長**：客戶數 ≥$1M ARR、NRR（淨留存率）、RPO 與 cRPO（及 vs 共識）、product gross margin
- **硬體／設備**：backlog、book-to-bill、產能利用率
- **循環／商品**：ASP（平均售價）、庫存天數
- **平台／消費**：MAU（月活）、ARPU

**鐵律**：同一指標只准引最新一季，`as_of` 必填（季別＋公告日期）；判斷層（Stage 1／writer 決策段）引用官方 KPI 數字時，一律以 `numbers.latest_quarter_kpis.items[]` 為準，不得從逐字稿原文或前份 DD 另行摘一個舊數字替換。若某項查無，整筆省略而非填造。

**與 `dd_numbers_extra.py` 的分工**：Stage 0a 會先跑 `python3 scripts/dd_numbers_extra.py {TICKER} {DATE} [--peers ...] [--evidence ...]`（零 LLM，見 `evidence-pack.md`），已算好 `numbers.valuation_history`／`numbers.momentum_26w`／`numbers.consensus_revision`／`numbers.peer_financials`／`numbers.edgar_concentrations` 五個欄位，並留一個空的 `numbers.latest_quarter_kpis` 佔位符（`{"_required": true, "quarter": "...", "items": []}`）。採集 agent **只需要填 `items[]`**，其餘五個欄位已存在時**不要重抓、不要改寫其 `method`／`source` 標籤**——那五欄的口徑（trailing vs fwd、TTM 季數、annual 樣本點數）已在欄位內自我說明，重複查證只會製造第二個不一致的數字。若某欄為 `null` 且帶 `note`（例如某 peer 查無資料），才視情況個別補查該一格，不必整段重做。

---

## 【fallback：writer 自跑協議】（僅在採集 agent spawn 失敗 2 次時啟用）

> 以下為 2026-08-07 之前的現行協議全文，保留不刪。啟用時 writer 自行執行：① 第一步跑 yfinance 批量採集腳本（**腳本正本＝上方 spawn 模板 prompt 內的 Python 全文**，同一份，不另存副本以防漂移）一次抓齊所有可由 yfinance 提供的資料;② 第二步（僅補漏）針對 yfinance 無法提供的執行 web_search（降至 6-8 次）;③ 禁止對 yfinance 已涵蓋的項目重複 web_search。

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
| **§10.5 IRR 用** | `[ticker] 5-year forward PE band` + `[ticker] EPS consensus FY+3 long-term growth`（IRR re-rate 與 EPS CAGR 基底，同輪搜得） |
| **QC-39 產業態勢變化（雙向，強制）** | 競爭惡化：`[ticker] market share gaining OR losing 2026` + `[ticker] largest customer second-source OR in-house` + `[competitor] design win at [ticker's customer]` + `[ticker] new entrant 2026`；結構 durability:`[industry] shortage OR oversupply structural OR cyclical 2026 2027` + `[industry] supply discipline new capacity timeline` + `[ticker product] demand durability AI structural`（完整規格見 QC-39） |

### yfinance 批量採集腳本（fallback 時的強制第一步）

**腳本正本＝上方 spawn 模板 prompt 內的 Python 全文**（「任務 1」段），連同 6 段結構（基本資訊／共識／三表／MA・Bollinger／近 5 日 OHLC／大盤 W104）一併沿用。此處不另存副本，避免兩份腳本漂移；fallback 時把該段整段貼進 Bash 執行即可（`{TICKER}` 換成實際標的）。

**執行上述腳本後**，所有 §8、§4、§7、§9、§10、附錄 A 需要的原始數據均已取得。進入各章節撰寫時直接引用，不得針對同一項目再 web_search。

### 報告頂部必須標註

資料抓取時間 ｜ 最新股價 ｜ 最近財報季 ｜ yfinance 採集 + 補充 web_search 次數

（fan-out 路徑下，此四項改為**從數字包第 0 節轉錄**，不重新查證。）

---

## 【退場訊號】

若因數字包錯誤導致**已發布報告的承重數字錯誤 ≥2 例**，本 fan-out 協議收回、機械採集復歸 writer 自跑（即以本檔【fallback】段為常態路徑）。

---



---

## 狀態判定（接續上方批量採集腳本的 closes / w52 / w104 / w250 / slope_pct）

> v15.1（2026-08-08）自 SKILL.md 附錄 A 移入本檔（Python 實作唯一居所）；六態條件表與 W250 斜率定義 ±3%、盲點 2 救援見 `references/timing-appendix.md` §F。

```python
# 狀態判定（接續批量採集腳本的 closes / w52 / w104 / w250 / slope_pct）
w52_slope = (w52 / float(np.mean(closes[-65:-13])) - 1) * 100 if len(closes) >= 65 else None
w104_slope = (w104 / float(np.mean(closes[-117:-13])) - 1) * 100 if len(closes) >= 117 else None
if w250 is None: state = "樣本不足（< 250 週）"
elif current < w250 or slope_pct < -3: state = "❌ 系統失效"
elif current < w104: state = "🟠 暫不進場"
elif current < w52 and w52_slope > 0 and w104_slope > 0 and slope_pct > 0: state = "🟢 最佳進場"
elif current > w52 > w104 > w250 and slope_pct > 3: state = "✅ 強勢進場"
elif current > w52 > w104 > w250 and abs(slope_pct) <= 3: state = "🟡 減半進場"
else: state = "🟡 觀察池"
```
