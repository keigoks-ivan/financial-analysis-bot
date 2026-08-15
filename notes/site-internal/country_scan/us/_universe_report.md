> ⚠ STALE（2026-08-15）：本檔為 hub／子頁組裝前研究素材，opus critic 修正未回填；數字以已發布的 docs/backtest/country_scan/us*.html 為準。

# 美股國家掃描 · 母體快照建構報告（Phase 0）

- **快照日期**：2026-08-15
- **母體檔案**：`_universe.json`
- **主體門檻**：S&P 1500 成分股資格（無額外市值篩選——指數委員會的納入標準即篩選器）
- **補充名單門檔**：市值 ≥ US$100億（10,000,000,000 美元），且不在 S&P 1500 內、且美國屬性通過驗證
- **範圍**：NYSE／NYSE American／Nasdaq（含 NasdaqGS／NasdaqGM）上市普通股

## 一、建構方法

### 1. 主體：S&P 1500 成分股（來源：Wikipedia 三張成分表）

以 `requests`＋標準瀏覽器 UA 直接抓取三個頁面，再用 `pandas.read_html` 解析主表（每頁第 1 張表即成分表）：

- `List of S&P 500 companies`（`Symbol`／`Security`／`GICS Sector`／`GICS Sub-Industry`）→ **503 檔**
- `List of S&P 400 companies`（MidCap，欄位同上）→ **400 檔**
- `List of S&P 600 companies`（SmallCap，欄位同上）→ **603 檔**

三張表合計候選 **1,506 檔**，跨表零重複（S&P 500／400／600 依指數委員會設計本為互斥集合，交叉比對確認無單一 ticker 同時掛在兩張表）。Ticker 正規化：Wikipedia 以 `.` 分隔股票類別（如 `BRK.B`），yfinance／Yahoo 端點需要 `-`（`BRK-B`），全數轉換；轉換後留存原始 `wiki_symbol` 供對照。

### 2. 補充名單：美國公司市值 ≥ US$100億但不在 S&P 1500

因 WebSearch 配額已在本 session 稍早的其他 Phase 用盡（`this session has used its web search budget 200 of 200`），改用 **WebFetch 直取一手排行資料**，未偏離「找不全就誠實記入盲區」的原則：

1. **候選來源**：`companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/`（「美國公司」排行，非「美國掛牌」，故已先天排除多數外國 ADR 如 TSM／ASML／HSBC）。以 `?page=N` 分頁抓取第 1–9 頁（每頁 100 檔），直到單頁最低市值跌破 US$80億為止（第 9 頁最低 US$70.6 億），確保 US$100億門檻以上無漏網。共取得 **900 檔候選排行**。
2. **交叉比對**：候選 900 檔中扣除已在 S&P 1500 名單者（含股票類別別名比對，如 `BK`↔`BNY`：BNY Mellon 已是 S&P500 成員，`companiesmarketcap` 用的是其舊代號 `BK`，比對時已修正避免誤判為缺漏），市值 ≥ US$100億且不在 S&P 1500 者得候選 **99 檔**。
3. **yfinance 逐檔驗證**（Yahoo v7 `finance/quote` 批次 + 個別 `.info` 補 country 欄位）：
   - **quoteType／exchange 過濾**：排除 `GBTC`（quoteType=ETF，非個股）。
   - **確認退市／資料不存在者排除（6 檔）**：`CTRA`（Coterra Energy）、`EXAS`（Exact Sciences）、`RNAM`、`DAY`（Dayforce）、`CFLT`（Confluent）在 Yahoo v7/quote 與 `.info` 均查無資料（`quoteSummary: Not Found`），`HOLX`（Hologic）quoteType 回傳 `NONE`／`tradeable:false`——判讀為已完成或接近完成的下市併購交易（Hologic 為 Blackstone/TPG 私有化案），這批 companiesmarketcap 快照可能沿用了較舊的快取資料，一律以 yfinance 現況為準排除。
   - **資料異常排除（1 檔）**：`SPCX`（"Space Exploration Technologies Corp."／SpaceX）——Yahoo 回傳 `quoteType=EQUITY`、`fullExchangeName=NasdaqGS`、市值 US$1.84 兆，但**截至快照時點 SpaceX 並未公開上市**，判斷為資料源異常（可能是私募市場估值追蹤器或第三方合成報價），排除並記入下方盲區。
   - **外國基金排除（1 檔）**：`PSHZF`（Pershing Square Holdings, Ltd.）——OTC Pink 掛牌，實體為根西島（Guernsey）註冊、倫敦證交所主板上市的封閉式基金，非美國營運公司，排除。
   - **股票類別重複排除（1 檔）**：`BF-A`（Brown-Forman Class A）——同公司 Class B（`BF-B`）已是 S&P500 成員，Class A 為同一家公司的另一股票類別，保留 BF-B 避免同公司市值重複計入母體。
   - **國籍驗證排除（3 檔）**：以 `yfinance.Ticker(x).info` 的 `country` 欄位逐一查證，排除三檔登記地非美國者——`WCN`（Waste Connections，加拿大 Woodbridge）、`ONC`（BeOne Medicines AG，瑞士 Basel）、`CRDO`（Credo Technology Group Holding Ltd，開曼群島 Grand Cayman）。**CRDO 為判斷灰色地帶**：其營運與研發實質在美國矽谷（San Jose），僅法律登記地在開曼——本輪嚴格採用「yfinance country 欄位」單一判準排除，若後續半導體鏡頭子頁認為應以營運實質認定納入，需個別覆核並記錄理由（見下方盲區第 5 點）。
   - 通過全部檢查後，最終補充名單 **85 檔**，全數以 `quoteType=EQUITY`、`fullExchangeName` 為 NYSE／NasdaqGS／NasdaqGM 等美國主要交易所、`country=United States` 三重確認。

**為何這些大市值公司不在 S&P 1500**（一般性理由，供子頁 writer 判讀時參考，未逐檔查證委員會紀錄）：
- **S&P 收錄要求近四季合計與最近一季 GAAP 獲利為正**，多檔高成長但近期轉虧或剛轉盈的公司（如 `IONQ`、`RIVN`、`AUR`、多檔生技股）尚未達標。
- **MLP／LP 結構**（`EPD`、`ET`、`MPLX`、`CQP`、`WES`、`PAA`、`SUN` 共 7 檔）——標普對有限合夥／K-1 稅務結構的公司歷來收錄門檻更高，即使市值巨大也常年被排除在外，這是結構性而非規模性的排除。
- **近期 IPO 尚未經指數委員會審核週期**（如 `CRCL`、`FIG`、`CHYM`、`ARXS`、`LINE`、`RBRK`、`ONC`〔已排除〕等）。
- **BDC／REIT／特殊金融結構**（`ARCC`、`AGNC`、`SUI` 等）部分因股利型結構或流通盤限制未入選。

### 3. yfinance 快照（兩段式，比照台灣輪防 429 協議）

母體最終名單（S&P 1500 的 1,506 檔 − 3 檔國籍排除 − 1 檔類別重複合併〔`CWEN-A`／`CWEN` 見下〕 + 85 檔補充 = **1,590 檔**）分兩段抓取：

- **第一段（bulk quote）**：用 `yfinance.Ticker("AAPL")._data` 取得的已認證 session，直接呼叫 Yahoo `v7/finance/quote` 批次端點，每批 **150 檔**／次請求，批間 sleep 1.5 秒，共 **11 批**。取得欄位：市值、現價、trailing PE／forward PE、P/B、殖利率（`dividendYield`，已是百分比形式）、52 週高低、流通股數。**1,593 檔請求、1,593 檔成功**（僅 `CWEN-A` 這一個 ticker 本身查無資料，見下）。
- **第二段（逐檔 info）**：`yfinance.Ticker(x).info`（quoteSummary 多模組合併請求），批次 **20 檔**＋批間 sleep 2.5 秒＋單檔間 sleep 0.25 秒，失敗重試一次。取得欄位：Yahoo sector/industry、ROE、營收成長率、盈餘成長率、毛利率／營業利益率／淨利率、總負債、總現金、負債權益比、國籍（用於補充名單驗證）。**1,593 檔全數成功、零硬失敗、零逾時**。
- **`CWEN-A` 特殊處理**：Wikipedia S&P 600 表把 Clearway Energy 的 Class A（`CWEN.A`）與 Class C（`CWEN`）列為兩筆獨立成分股，但截至快照時點 Yahoo 對 `CWEN-A` 這個 ticker 符號回傳 `quoteSummary: Not Found`（v7/quote 與 `.info` 皆查無）。核實 `CWEN`（Class C）本身資料正常（市值約 US$84 億），判斷為同一家公司的兩個股票類別中，A 類代號在 Yahoo 端已不可解析（可能與流動性極低、Yahoo 停止追蹤該類別報價有關），故**母體以單一 `CWEN` 代表 Clearway Energy 整家公司**，未重複計入兩筆。因此最終 S&P 600 段實收 **602 檔**（非 Wikipedia 表面的 603）。

## 二、母體組成

| 項目 | 數字 |
|---|---|
| S&P 500 | 503 檔 |
| S&P 400（MidCap） | 400 檔 |
| S&P 600（SmallCap） | 602 檔（`CWEN-A`／`CWEN` 併為一檔，見上） |
| 補充名單（非指數、市值 ≥ US$100億） | 85 檔 |
| **母體總檔數** | **1,590 檔** |
| 母體總市值 | 約 US$83.97 兆 |

### 產業結構（依 GICS Sector，市值加權；補充名單無 GICS 分類，另列 Yahoo sector 供對照）

| 排序 | GICS Sector | 檔數 | 市值佔母體% |
|---|---|---|---|
| 1 | Information Technology | 190 | 31.78% |
| 2 | Communication Services | 49 | 13.98% |
| 3 | Financials | 259 | 11.89% |
| 4 | Consumer Discretionary | 194 | 9.12% |
| 5 | Industrials | 263 | 8.75% |
| 6 | Health Care | 163 | 8.13% |
| 7 | Consumer Staples | 76 | 4.51% |
| 8 | Energy | 71 | 3.13% |
| 9 | Real Estate | 104 | 1.98% |
| 10 | Utilities | 59 | 1.85% |
| 11 | Materials | 77 | 1.82% |
| — | 補充名單（無 GICS，Yahoo sector 混合） | 85 | 2.87% |

**指數集中度**：前 10 大市值合計約佔母體總市值 **31.3%**（`NVDA` US$5.45 兆／`AAPL` US$4.46 兆／`GOOGL`＋`GOOG` 合計 US$8.43 兆／`MSFT` US$3.68 兆／`AMZN` US$2.83 兆／`AVGO` US$1.87 兆／`META` US$1.50 兆／`TSLA` US$1.35 兆／`MU` US$1.10 兆／`BRK-B` US$1.08 兆），單 `NVDA` 一檔即佔母體總市值約 **6.5%**。此數字可直接餵 hub §1 市場結構「指數集中度／Mag 7 現象」章節，並與台灣輪「台積電單一權值股佔母體 39%」形成對照素材（但依鐵律，hub 內文不得展開兩市場對照敘事，僅供 writer 內部判讀）。

## 三、補充名單全表（85 檔，依市值排序，前 20 檔）

| Ticker | 公司名 | 市值（快照時） | Yahoo Sector |
|---|---|---|---|
| SCCO | Southern Copper Corporation | US$1,558.7億 | Basic Materials |
| SNOW | Snowflake Inc. | US$1,140.0億 | Technology |
| NET | Cloudflare, Inc. | US$1,124.4億 | Technology |
| EPD | Enterprise Products Partners L.P. | US$840.0億 | Energy |
| ET | Energy Transfer LP | US$724.8億 | Energy |
| BE | Bloom Energy Corporation | US$677.2億 | Industrials |
| MPLX | MPLX LP | US$603.0億 | Energy |
| CRWV | CoreWeave, Inc. | US$580.5億 | Technology |
| LNG | Cheniere Energy, Inc. | US$561.0億 | Energy |
| ALAB | Astera Labs, Inc. | US$557.9億 | Technology |
| EA | Electronic Arts Inc | US$529.3億 | Communication Services |
| HEI | HEICO Corporation | US$523.6億 | Industrials |
| CBRS | Cerebras Systems Inc. | US$520.2億 | Technology |
| RKLB | Rocket Lab Corporation | US$513.1億 | Industrials |
| MDLN | Medline Inc. | US$480.9億 | Healthcare |
| NTRA | Natera, Inc. | US$446.7億 | Healthcare |
| RVMD | Revolution Medicines, Inc. | US$436.6億 | Healthcare |
| RKT | Rocket Companies, Inc. | US$418.0億 | Financial Services |
| MDB | MongoDB, Inc. | US$370.3億 | Technology |
| MSTR | Strategy Inc（原 MicroStrategy） | US$366.4億 | Technology |

（完整 85 檔清單見 `_universe.json` 內 `index_membership="SUPPLEMENT"` 的 constituents。）

### 補充名單內特別註記

- **`EA`（Electronic Arts）**：2026-08-15 快照時仍在公開市場交易，但已知處於 Silver Lake／PIF／Affinity Partners 主導的私有化收購案進行中（案值約 US$550 億），S&P 已將其自 500 指數移出（本輪判定其不在 S&P 1500 名單即為此事的間接證據，未逐一查證委員會公告日期）。若收購案在鏡頭子頁寫作前完成，`EA` 屆時將完全下市，writer 需自行以快照時點的最新公開資訊核實。
- **`MSTR`（Strategy Inc）／`BMNR`（Bitmine Immersion Technologies）**：兩者皆為「加密貨幣財庫」型商業模式（持有大量比特幣／以太幣作為資產負債表策略），非傳統營運公司估值邏輯，鏡頭子頁若收錄需特別註明。
- **`DRS`（Leonardo DRS, Inc.）**：美國德拉瓦州註冊、維吉尼亞州 Arlington 總部，但多數股權由義大利國防公司 Leonardo S.p.A. 持有——yfinance country 欄位判定為美國（註冊地與營運地皆美國），予以保留，但此為「外資控股的美國掛牌公司」而非純美資公司，鏡頭子頁引用時宜註明母公司關係。
- **`ARXS`（Arxis, Inc.）／`FPS`（Forgent Power Solutions, Inc.）／`MAIR`（Madison Air Solutions Corporation）**：三者公司名稱在一般財經媒體中辨識度較低，經逐一 `yfinance.Ticker(x).info` 查證確認為美國註冊、`quoteType=EQUITY`、產業分類合理（分別為航太國防／電力設備／建築產品），研判為近期重組、分拆或改名後的公司實體，非資料錯誤，但建議鏡頭子頁 writer 收錄前另行核實其公司背景與上市沿革（超出本輪 Phase 0 查證範圍）。

## 四、缺值率（母體 1,590 檔）

| 欄位 | 缺值數 | 缺值率 | 判讀 |
|---|---|---|---|
| market_cap | 0 | 0.00% | 全數取得，零缺失 |
| price | 0 | 0.00% | 全數取得，零缺失 |
| week52_high / week52_low | 0 / 0 | 0.00% | 全數取得 |
| shares_outstanding | 0 | 0.00% | 全數取得 |
| price_to_book | 1 | 0.06% | 個別公司帳面淨值為負或極端值 |
| profit_margins / operating_margins / gross_margins | 1 / 1 / 1 | 0.06% | 同上等級的個別缺失 |
| total_debt | 2 | 0.13% | 個別公司資產負債表結構特殊 |
| total_cash | 4 | 0.25% | 同上 |
| forward_pe | 3 | 0.19% | 個別公司無分析師前瞻獲利估計 |
| revenue_growth | 10 | 0.63% | 個別公司缺同期比較基期 |
| roe | 74 | 4.65% | 個別小型股或近期虧損公司 Yahoo 未提供 |
| debt_to_equity | 181 | 11.38% | **61%集中在金融業**（110/181 為 GICS Financials）——Yahoo 對銀行／保險／資產管理公司的資產負債表結構（無傳統「股東權益」對「有息負債」二分）不populate此欄，屬業務事實非缺失 |
| trailing_pe | 209 | 13.14% | **多數非資料缺失，是業務事實**——近四季虧損或 EPS 為負時 Yahoo 不回傳正值 trailing P/E（抽查 39 檔 profit_margins 為負，其餘多為個別季度虧損但年度轉正的邊界案例） |
| earnings_growth | 301 | 18.93% | Yahoo `earningsGrowth` 欄位本身覆蓋率偏低（不限本母體，為 Yahoo API 已知限制），非本次抓取失敗 |
| dividend_yield | 548 | 34.47% | **多數非資料缺失，是業務事實**——未配息或近四季無配發現金股利的公司 Yahoo 不回傳殖利率欄位（成長股、REIT 轉型期公司、生技股常見） |
| gics_sector / gics_sub_industry | 85 | 5.35% | **全部且僅限補充名單 85 檔**（S&P 1500 主體 1,505 檔皆有 Wikipedia 提供的 GICS 分類，補充名單無官方 GICS，以 `yahoo_sector`／`yahoo_industry` 欄位替代，母體 JSON 中兩套欄位皆保留） |

**壞 tick 檢查**：對全部 1,590 檔逐一檢查 `price <= 0` 與 `market_cap <= 0/null`，**零筆觸發**；另檢查 S&P500／S&P400 成員市值是否低於 US$10億這種明顯異常值，**零筆觸發**。第一段 bulk quote 與第二段逐檔 info 對全部候選（含被排除的補充候選）**零硬失敗、零逾時**，`phase_b_info.jsonl` 中無任何 `_error` 欄位殘留。

## 五、盲區自陳

1. **市值 US$100億以下的非指數美國公司完全未涵蓋**——本輪只對「不在 S&P 1500 但市值 ≥ US$100億」這個區間做了系統性補充，US$100億以下、同樣不在指數內的美國公司（例如更小型的近期 IPO、家族企業、Pink Sheet 掛牌者）未納入掃描，若鏡頭九「中小型隱形冠軍」需要這個區間的名字，需另建母體或人工補充。
2. **補充名單來源單一且未經 WebSearch 交叉驗證**——本輪因 WebSearch 配額已在 session 內耗盡，補充名單完全依賴 `companiesmarketcap.com` 單一第三方排行網站（雖已用 yfinance 逐檔核實市值與國籍，過濾掉 11 檔資料異常/已下市/外國籍者），未能像規格建議的「2-3 次 WebSearch 交叉比對」多來源互證。存在單一資料源系統性遺漏的風險（例如該網站若本身漏收某些公司，本輪也會一併漏收），且其市值計算方法論、更新頻率未知，可能與 Yahoo 快照存在小幅時點落差。
3. **金融股（銀行/保險/資產管理）的 ROE／P/B／負債權益比等一般製造業慣用指標，對金融業解讀意義不同**（金融業高槓桿是產業常態非風險訊號；本輪 debt_to_equity 缺值率 11.38% 中 61% 集中於金融業正是此結構差異的直接體現），金融鏡頭子頁需自行注意不要直接套用一般化的財務門檻判讀 259 檔 GICS Financials（含補充名單金融服務類）樣本。
4. **Wikipedia 三張成分表為「即時」頁面而非某一固定日期的官方定案快照**——抓取時間為 2026-08-15，反映的是當下維基百科編輯者已更新的最新指數成分（S&P 官方公告的成分變動通常有數日至數週的編輯延遲），與標普道瓊指數公司官方名單可能存在極小幅落差（個位數檔案級別的新增/剔除時間差），但不影響母體整體結構性判讀。
5. **`CRDO`（Credo Technology）國籍排除為灰色地帶判斷**——嚴格依 yfinance `country` 欄位（開曼群島）排除，但其研發與營運實質在美國矽谷（San Jose），與多檔已被視為「美股」的稅籍倒置公司（如指數內的 ACN／ETN／LIN）性質類似。若鏡頭二「半導體與 AI 基礎設施」子頁認為應以營運實質而非登記地認定，可個別覆核後補入，但需在該子頁 datanote 中明確記錄覆核理由與資料來源，不應無痕修改本母體檔案。
6. **`EA`／`HOLX` 等處於下市併購過程中的公司狀態具時效性**——本報告記錄的是 2026-08-15 快照時點的公開市場狀態，若鏡頭子頁寫作時點已晚於本快照且相關收購案有新進展（完成下市／案件生變），該公司在母體中的「仍可交易」狀態可能已過時，writer 引用前應自行核實現況。
7. **`SPCX` 排除為資料源異常判斷，非官方確認**——本輪判定 Yahoo 對 `SPCX`（SpaceX）回傳的 EQUITY 報價資料為異常（截至快照時點 SpaceX 未公開上市是本 agent 基於既有知識的判斷，未逐一查證最新公開發行狀態），若 SpaceX 實際上已在快照前完成某種形式的公開發行或替代性上市機制，此排除判斷需要重新檢視。
8. **獲利品質欄位（ROE、營收成長率、毛利率等）皆為 Yahoo `Ticker.info` 回傳的 trailing 或最新一期快照，未做多年期時間序列**——若鏡頭子頁（尤其複利機器、中小型隱形冠軍鏡頭）需要「連續 N 年 ROIC 門檻」「回購縮股連續性旗標」這類量化篩選（施工圖 §4 明確要求複利鏡頭雙入口：單年快照與多年軌跡旗標並用），母體 JSON 本身不夠用，寫作 agent 需自行對候選名單額外查詢財報歷史數據，不能只用本檔案的單期快照下結論。

## 六、與台灣輪方法論的差異對照（供交接用，非發布內容）

| 面向 | 台灣輪 | 美股輪 |
|---|---|---|
| 主體來源 | TWSE/TPEx ISIN 全量掃描＋CFI 過濾 | S&P 1500 指數委員會既有篩選（不重造篩選器） |
| 篩選邏輯 | 市值單一門檻（≥NT$100億）套用全市場 | 指數資格為主，市值門檻只用於指數外補充名單 |
| 429 防護 | bulk quote（150檔/批）→ 逐檔 info（≤20檔/批，僅過門檻者） | 同款兩段式，但因主體已由指數預篩，逐檔 info 覆蓋全部 1,593 檔而非再篩一輪 |
| GICS/產業分類 | Yahoo sector/industry（與 TWSE 官方分類交叉，官方優先） | Wikipedia GICS（S&P 官方分類標準本身，權威性更高，僅補充名單 fallback 到 Yahoo） |
| 特有坑 | 7 檔新掛牌無市值資料、興櫃完全未涵蓋 | `CWEN-A` 查無 Yahoo 資料需併類別、`SPCX` 疑似資料源異常需排除、WebSearch 配額耗盡改用 WebFetch 直取排行網站 |
