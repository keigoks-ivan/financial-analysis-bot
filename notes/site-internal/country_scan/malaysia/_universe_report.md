# 馬股國家掃描 · 母體快照建構報告

- **快照日期**：2026-09-10（母體完整性交叉比對同日補做，見一之3）
- **母體檔案**：`_universe.json`
- **母體定義**：Bursa Malaysia 主板（Main Market）普通股，市值 ≥ RM 20 億（2,000,000,000）
- **範圍**：Bursa Malaysia Main Market 上市普通股（不含 ACE 市場、LEAP 市場）

## 一、建構方法

### 1. 候選名單來源

因 Bursa Malaysia 官方「List of Companies」PDF 受 Cloudflare 反爬蟲保護無法直接下載，
`companiesmarketcap.com/malaysia` 頁面經查證後發現只收錄約 57 檔（且混雜多檔在美國 OTC／
新加坡主要上市的馬來西亞裔公司，如 Maybank 用美股 ADR 代號 MLYBY、IHH Healthcare 用新加坡
代號 Q0F.SI），不是可靠的 Bursa 主板全量來源，故改用：

- **主體**：Wikipedia「List of companies listed on the Malaysia Exchange」（頁面標註反映
  2017-04-10 的 Main Market 名冊），以程式解析頁面 wikitable，取得 **807 檔**候選（公司名＋
  Bursa 四碼代號）。
- **補充名單**：9 檔本頁研究過程中已知的 2017 年後掛牌／改名之大型個股，且不在上述 807 檔
  候選中者：99 Speed Mart Retail Holdings（5326）、Mr D.I.Y. Group（5296）、Greatech
  Technology（0208）、UWC Berhad（5292）、Focus Point Holdings（0157）、SD Guthrie
  （5285，原 Sime Darby Plantation）、Farm Fresh（6068）、Solarvest Holdings（0215）、
  DXN Holdings（0220）。

候選總數：807 + 9 = **814 檔**。Ticker 轉換為 yfinance 格式：Bursa 四碼代號 + `.KL` 後綴
（如 `1295.KL`）。**注意**：補充名單當時把 Farm Fresh 的代號寫成 6068、DXN Holdings 寫成 0220，
兩者皆錯（正確為 5306 與 5318），因此這兩檔實際上並未進入第一輪母體——這個錯誤在第三段的完整性
交叉比對中被抓出來並補正。

### 2. yfinance 兩段式快照（比照台股／美股輪的 429 防護協議）

- **第一段（Phase A，market cap 篩選）**：對全部 814 檔候選逐檔呼叫 `yfinance.Ticker(x).fast_info`
  （比 `.info` 輕量、不易觸發速率限制的即時報價端點），10 條併發執行緒批次處理，取得市值、
  quoteType、現價、52 週高低。首輪完成後對其中回傳錯誤的 215 檔（多數為 429 速率限制或已下市）
  以 4 條併發執行緒、每次重試最多 3 次的方式重跑，最終仍有 **92 檔**查無資料或確認已下市／
  改名（quoteType 非 EQUITY 或連續 3 次查詢失敗）。
- **篩選**：對 Phase A 成功取得資料的 722 檔，以 `market_cap ≥ RM 20 億` 且 `quoteType == EQUITY`
  為門檻篩選，得 **116 檔**合格母體（**595 檔**因市值低於門檻被排除）。
- **第二段（Phase B，逐檔 info）**：僅對 116 檔合格母體呼叫 `yfinance.Ticker(x).get_info()`，
  批次 20 檔、批間 sleep 2.5 秒、單檔間 sleep 0.25 秒，失敗重試一次。**116 檔全數成功、零硬失敗**。
  取得欄位：Yahoo sector/industry、trailing PE、forward PE、price-to-book、ROE、殖利率、
  營收成長率、盈餘成長率、毛利率／營業利益率／淨利率、總負債、總現金、負債權益比。

### 3. 第三段（完整性交叉比對，2026-09-10 補做）

第一、二段的候選名單主體是 2017 年的靜態快照，結構上必然漏掉 2018 年後掛牌的公司。為了把這個
盲區關掉，另取一份**獨立的、即時的**馬股市值排行全量名單做交叉比對：

- 來源：TradingView 馬來西亞股票篩選器，條件 `market_cap_basic ≥ RM 20 億`，2026-09-10 查詢，
  回傳 **136 檔**（含 REIT，不含權證與債券）。
- 與第一輪的 116 檔逐檔對照（以正規化公司名 + 市值近似雙軌比對，並人工處理 12 檔改名個案，
  如 Digi.Com→CelcomDigi、Lafarge Malaysia→Malayan Cement、Goldis→IGB、Comintel→Binastra、
  UMW Oil & Gas→Velesto、Complete Logistic Services→Hextar Technologies、AirAsia X→AirAsia Group 等），
  找出 **19 檔**第一輪未涵蓋者。
- 這 19 檔逐檔以 `yfinance.Ticker(x).get_info()` 補抓（批 ≤ 20、批間 sleep 2 秒、失敗重試一次），結果：
  - **14 檔** yfinance 市值 ≥ RM 20 億，納入母體：Sunway Healthcare（5555）、Eco-Shop Marketing（5337）、
    SkyeChip（5357）、Johor Plantations（5323）、ITMAX System（5309）、NationGate（0270）、
    Farm Fresh（5306）、Southern Cable（0225）、Stratus Global（5356）、TMK Chemical（5330）、
    MN Holdings（0245）、DXN Holdings（5318）、Leong Hup International（6633）、MTT Shipping（5352）。
  - **4 檔** 在本快照日的 yfinance 市值低於門檻，不納入（TradingView 口徑略高於 yfinance）：
    Zetrix AI（0138，RM19.7 億）、TSH Resources（9059，RM18.9 億）、MBM Resources（5983，RM19.1 億）、
    Hume Cement Industries（5000，RM19.8 億）。
  - **1 檔** 依外國公司第二上市規則排除：UMS Integration（5340），境外註冊、主要上市地為另一個交易所、
    Bursa 僅為第二上市，納入會與主要上市地重複計算市值。
- 反向檢查：136 檔 TradingView 名單逐列比對「母體 130 檔 + 上述 5 檔排除者」後，**未匹配 0 列**，
  即在 RM 20 億門檻之上，兩份名單已完全互相覆蓋。
- 同時把 12 檔改名公司的 `name` 欄位由 2017 年舊名更新為 Yahoo 現行名稱，舊名保留在 `data_flags`。

**母體檔數因此由 116 檔更新為 130 檔**，總市值由約 RM1.74 兆更新為約 RM1.82 兆。

全程使用 `/Users/ivanchang/.venvs/v7bt/bin/python`（yfinance 1.4.1、pandas 2.3.3<3）。

## 二、母體組成

| 項目 | 數字 |
|---|---|
| 候選總數 | 833 檔（807 檔 Wikipedia 主體 + 9 檔補充 + 19 檔交叉比對補入） |
| 查無資料／確認已下市或改名 | 92 檔 |
| 市值低於 RM 20 億門檻 | 599 檔（含交叉比對補抓後低於門檻的 4 檔） |
| 外國公司第二上市排除 | 1 檔（UMS Integration，5340） |
| **母體合格檔數** | **130 檔** |
| 母體總市值 | 約 RM 1.82 兆（1,815,621,613,750） |

### 92 檔「查無資料」的性質：多數是已驗證的私有化／下市事件，不是資料缺失

抽查這 92 檔的公司名稱，發現絕大多數是本頁鏡頭四（事件驅動）已查證到的近年私有化／下市案例，
包括：UMW Holdings（2024 下市）、Boustead Holdings（2023 下市）、Malaysia Airports
Holdings（2025 下市）、Cocoaland Holdings（2022 下市）、GHL Systems（2024 下市）、
Felda Global Ventures／FGV Holdings（2025 下市）、Apex Healthcare（2026 下市）、
UEM Edgenta（2026 年 7 月下市）——這與母體建構本身無關的資料缺失不同，反而是私有化管道
活躍這個市場結構性事實的獨立佐證。其餘查無資料者多為已破產清算、長期停牌或公司名稱重大
變更後 Wikipedia 舊名冊未能對應的小型股（如 Perisai Petroleum、Sumatec Resources、
Serba Dinamik 等）。

### 產業結構（依 Yahoo Finance sector，市值加權）

| 排序 | Yahoo Sector | 檔數 | 市值佔母體% |
|---|---|---|---|
| 1 | Financial Services | 17 | 26.52% |
| 2 | Industrials | 24 | 13.62% |
| 3 | Consumer Defensive | 23 | 11.30% |
| 4 | Utilities | 7 | 9.60% |
| 5 | Basic Materials | 8 | 7.21% |
| 6 | Communication Services | 5 | 6.49% |
| 7 | Healthcare | 5 | 6.36% |
| 8 | Real Estate | 17 | 5.90% |
| 9 | Consumer Cyclical | 9 | 5.41% |
| 10 | Energy | 7 | 4.30% |
| 11 | Technology | 8 | 3.30% |

（完整市值佔比由 `_build_hub.py` 對 `_universe.json` 現算並嵌入頁面 Exhibit 2；金融服務業以 17 檔
（占母體家數 13.1%）拿下母體市值 26.52%，家數占比雖不像全市場口徑那麼懸殊，但市值集中的方向一致。
補入 14 檔後，科技分類由 5 檔增為 8 檔、工業由 20 檔增為 24 檔、必需消費由 19 檔增為 23 檔——
新掛牌的公司集中在科技與消費，正是舊名冊最容易漏掉的一塊。）

**指數集中度**：前十大個股合計約佔母體總市值 **38.6%**（補入 14 檔後由 40.3% 稀釋），
第一大個股 Malayan Banking Berhad（Maybank）單獨佔約 **7.0%**。

## 三、缺值率（母體 130 檔）

| 欄位 | 缺值數 | 缺值率 | 判讀 |
|---|---|---|---|
| market_cap / price / week52_high / week52_low | 0 | 0.00% | 全數取得，零缺失 |
| price_to_book | 0 | 0.00% | 全數取得 |
| total_debt_myr / total_cash_myr | 0 / 0 | 0.00% | 全數取得 |
| profit_margins / operating_margins / gross_margins | 0 | 0.00% | 全數取得 |
| roe | 2 | 1.54% | 個別公司近期虧損或財報結構特殊 |
| revenue_growth | 4 | 3.08% | 個別公司缺同期比較基期（多為新掛牌未滿兩個完整年度者） |
| trailing_pe | 11 | 8.46% | 多數為近期獲利為負，Yahoo 不回傳正值 trailing P/E，屬業務事實非缺失 |
| forward_pe | 12 | 9.23% | 個別公司無分析師前瞻獲利估計覆蓋 |
| dividend_yield | 15 | 11.54% | 未配息或近四季無配發現金股利的公司 Yahoo 不回傳殖利率欄位，屬業務事實；新掛牌股多屬此類 |
| debt_to_equity | 13 | 10.00% | 部分集中於金融服務業（銀行/保險資產負債表結構特殊，Yahoo 不 populate 此欄） |
| earnings_growth | 16 | 12.31% | Yahoo `earningsGrowth` 欄位本身覆蓋率偏低，非本次抓取失敗 |

**壞 tick 檢查**：對全部 130 檔逐一檢查 `price <= 0` 與 `market_cap <= 0/null`，**零筆觸發**；
Phase B 與第三段補抓對合格母體的 `get_info()` 呼叫**零硬失敗**（`phaseB_results.json` 中無任何
`_error` 欄位殘留）。

## 四、盲區自陳

1. **（已修復）候選名單主體是 2017 年的 Wikipedia 靜態快照**——2026-09-10 的完整性交叉比對已把
   這個盲區關掉：實際遺漏 14 檔（占母體 10.8%、市值 RM760 億），全部是 2018 年後掛牌或改名的公司，
   最大一檔 Sunway Healthcare（5555，RM247 億）直接是母體第 23 大，遺漏規模比原先自陳的
   「個位數至十位數檔案級別」更嚴重。剩餘風險：交叉比對用的第三方市值排行若自身漏列某檔，
   本頁同樣會漏；此風險無法用現有免費來源進一步降低（Bursa 官方名冊 PDF 受 Cloudflare 阻擋）。
2. **ACE 市場與 LEAP 市場完全未涵蓋**——僅涵蓋 Bursa Malaysia 主板（Main Market），創業板與
   有限公開發行市場的公司即使市值達標也不在候選名單中，因為候選來源的 Wikipedia 頁面本身
   即以主板為範圍。
3. **REIT／信託類股納入、外國公司第二上市已查證並排除**——母體中包含具名 REIT（如 IGB REIT、
   Axis REIT、Sunway REIT、Pavilion REIT），建構時不特別排除 REIT／信託架構，這是刻意選擇而非疏漏；
   外國公司第二上市已在第三段逐檔查證，唯一命中的 UMS Integration（5340）已排除並列名，
   排除規則從「未查證」升級為「已查證，1 檔排除」。
4. **92 檔查無資料者的下市／改名原因僅抽查驗證，未逐檔查證**——本報告第二節列出的具名下市
   案例是抽查後確認的，其餘查無資料的小型股未逐一查證其確切下市或改名原因，可能存在
   Wikipedia 名冊本身列名有誤（如同名異碼）的個別案例未被排除。
5. **yfinance 欄位缺值率整體偏低，但金融服務業的 debt_to_equity 缺值有結構性原因**——這與
   台股／美股輪觀察到的現象一致：Yahoo 對銀行/保險/資產管理公司的資產負債表結構（無傳統
   「股東權益」對「有息負債」二分）不 populate 此欄，屬業務事實非資料缺失，金融鏡頭（鏡頭二）
   已改用 P/B 反推隱含 ROE 的方法論繞開此限制。
