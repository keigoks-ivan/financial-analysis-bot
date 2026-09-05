# Evidence Pack — AI Networking（採集 agent 交回，2026-09-05）

**重大限制聲明（讀者必看）**：本次採集開始時 session 的 WebSearch 額度已耗盡（200/200，非本 agent 用盡，疑為同 session 其他並行任務耗用），**全程零 WebSearch 可用**。所有證據改以 (a) SEC EDGAR 直接瀏覽／全文檢索（`efts.sec.gov`）、(b) 已知公司 IR／newsroom／機構官網 URL 直接 WebFetch 取得。這對 10-Q/10-K/8-K/新聞稿類（Axis B／D 多數、C4）覆蓋良好，但對純粹依賴搜尋才能定位的項目（Axis A 歷史統計、C1 TAM 報告、C2 拆解報告、D6 模組 ASP、部分 Axis E 新聞）造成**結構性缺口**，並非未嘗試——Google/Bing/DuckDuckGo 網頁版 WebFetch 均被封鎖或回傳空結果（已實測）。以下逐題如實標注「查不到」。

---

## 最高優先三題

### D8｜資料完整性查核 — **已解決，關鍵發現**

- **APH 確認發生 2-for-1 股票分割**：Amphenol 8-K（Item 8.01）2026-08-06 公告，"the Company's Board of Directors approved a two-for-one stock split to be paid in the form of a stock dividend"；record date **2026-08-17**，distribution date **2026-09-02**。｜來源：SEC EDGAR 8-K exhibit 99.1，`sec.gov/Archives/edgar/data/820313/000110465926091969/tm2622441d1_ex99-1.htm`｜as-of 2026-08-06｜**T1**
- **FN（Fabrinet）2026-01-01～2026-08-31 期間無任何股票分割／特別配息／資本重組**：EDGAR 全文檢索 "stock split" 對 Fabrinet 於此區間回傳 0 筆；其唯一 2026-08-17 8-K（Item 1.01/2.02/2.03/5.02/9.01）內容為 term loan 修訂＋CFA amendment＋FQ4 FY26 財報，與分割無關。｜來源：`efts.sec.gov` 全文檢索＋`sec.gov/Archives/edgar/data/1408710/000140871026000026/`｜as-of 2026-08-31｜**T1**
- **除權息調整後收盤價**（Yahoo Finance chart API，直接 curl 取原始 JSON 逐筆核對，非小模型摘要）：
  - APH：2026-02-27（最近交易日，2/28 為週六）close **$73.03**／adjclose **$72.776**；2026-08-31 close **$79.275**／adjclose 同｜**T2**（資料聚合商即時流，非申報文件）｜這代表**分割調整後**兩點實為 **+8.6%～+8.9%**，而非站內 26W/52W 報表顯示的 −37.1%/−57.3%——強烈支持 writer NC#6 假設：舊報表混用「分割前原始價」與「分割後調整價」造成約 2 倍的資料假象。
  - FN：2026-02-27 close **$545.63**；2026-08-31 close **$412.93**（皆為原始未分割值，因 FN 無分割）——真實下跌 **約 −24.3%**，與其自身基本面判讀分開處理，非資料假象。｜同上 T2
  - 補充：本機 repo 本地快取 `data/weekly_cache/APH.json`（last_full_refresh 2026-09-05）週線在 2026-08-24（$161.38）→2026-08-31（$82.78）出現整整 ~1.95× 斷點，與 2-for-1 比例精確吻合，**是本機快取尚未追溯調整分割前資料的直接證據**（T4，內部快取，僅供交叉佐證不作為對外引用）。

**結論**：D8 兩問全部解決。APH 的異常報酬**確認為分割相關資料完整性問題**（是否 100% 解釋站內 −57.3%/−37.1% 需 writer 自行核對報表口徑與計算日，但方向與量級吻合）；FN 的下跌是真實的，需基本面解讀。

### D7｜外部驗證器 — **部分解決**

- **(i) AVGO＋ANET＋CRDO 網路相關營收 6 季序列**：
  - **AVGO**（官方口徑為「AI semiconductor revenue」，未單獨分列 networking；10-Q 本身不揭露此細分，數字均出自法說新聞稿 Item 2.02 exhibit）：
    - Q3 FY25（截至 2025-08-03）：$5.2B（YoY +63%）
    - Q4 FY25（截至 2025-11-02）：金額未在新聞稿明列，僅揭露 YoY +74%（"AI semiconductor revenue increasing 74% year-over-year"）
    - Q1 FY26（截至 2026-02-01）：$8.4B（YoY +106%）
    - Q2 FY26（截至 2026-05-03）：$10.8B（YoY +143%）
    - Q3 FY26（截至 2026-08-02）：$16.7B（YoY +221%、QoQ +54%）
    - Q4 FY26 展望（管理層口頭guide）：$21.7B（YoY +236%）
    - 來源：各季 8-K Item 2.02 exhibit 99，`sec.gov/Archives/edgar/data/1730168/...`｜**T1**
  - **ANET**（公司幾乎 100% 為網路營收，故以總營收近似）：Q3 2025 $2.308B（+27.5% YoY）／Q4 2025 $2.488B（+28.9% YoY，FY25 合計 $9.006B）／Q1 2026 $2.709B（+35.1% YoY）／Q2 2026 $3.036B（+37.7% YoY）／Q3 2026 展望 ~$3.3B。遞延營收：2025Q3 $4.69B→2025Q4 $5.372B→2026Q1 $6.198B→2026Q2 $6.866B（逐季上升）。**未能在新聞稿文字中找到「AI 目標凍結在 $3.5B」的具體句子**（該句很可能出自法說逐字稿而非新聞稿，本次無法取得逐字稿）。｜來源：各季 8-K Item 2.02 exhibit，`sec.gov/Archives/edgar/data/1596532/...`｜**T1**｜as-of 各季報日
  - **CRDO**：Q1 FY27（截至 2026-08-01）總營收 $479.0M（YoY +114.7% vs Q1 FY26 $223.1M）；10-Q 明說「AEC products 貢獻超過 90% 的營收增量」，但無單獨 AEC 美元金額或前四季序列（本季度 10-Q 只揭露當季與去年同季，未见逐季表）。客戶集中度：依「contracting party」Customer A 43%／Customer B 28%；依「end-customer」Customer D 33%／Customer C 28%／Customer E 13%。｜來源：10-Q，`sec.gov/Archives/edgar/data/1807794/000162828026060111/crdo-20260801.htm`｜**T1**｜as-of 2026-08-01
- **(ii) 2026 年公開宣布的 Ethernet AI 叢集部署 ≥3 例＋官方新聞稿**：**查不到**——此類發現高度依賴新聞搜尋定位具體案例（如「XX hyperscaler 宣布採用 Ethernet 部署 N 萬顆 GPU」），WebSearch 不可用、且新聞聚合站（Bing/DuckDuckGo/Google）WebFetch 全數被封鎖，未能定位任何一例。**此為本次採集最大缺口之一。**
- **(iii) UALink 1.0 產品出貨公告**：**確認「無」**。UALink Consortium 官網（`ualinkconsortium.org`）新聞列表最新條目仍停在 2025 年（"UALink Consortium Releases the Ultra Accelerator Link 200G 1.0 Specification"，"Statements of Support"，2025 年內，無 2026 年更新條目可見）；Astera Labs FQ2 2026 財報新聞稿（2026-08-04，`sec.gov/Archives/edgar/data/1736297/000173629726000033/q226exhibit991.htm`）中僅提及「UALink connectivity」相容的 Taurus retimer 產品，以及**"UALink 2.0"** 的時程討論（"the ability of UALink 2.0 to provide for a purpose-built AI compute fabric... and the timing of any initial programs"）——**產業論述已進到 2.0 世代的時程討論，代表 1.0 矽產品截至 2026-08 仍無可查證的規模出貨公告**。｜來源：`ualinkconsortium.org`（T2，標準組織官網）＋ALAB 8-K exhibit（**T1**）｜as-of 2026-08-04

### D6｜市場撮合價（800G／1.6T ASP） — **完全查不到，紅色警示**

**本題完全落空，須標紅**。LightCounting（`lightcounting.com/news`）、Omdia（`omdia.tech.informa.com/pr`）皆回傳 403 Forbidden，無法讀取任何內容；TrendForce 新聞中心（`trendforce.com/presscenter`）唯一相關條目是 2026-05-11 的「Micro LED CPO 光模組市場 2030 年達 8.48 億美元」（**T2-zh**，但這是 TAM 預測非 ASP，且是小眾 Micro LED CPO 技術不是主流 800G/1.6T pluggable），與本題無關。替代品 AEC 每條單價／EML 晶粒單價序列同樣查不到——CRDO 10-Q 未揭露 AEC 單價，法說新聞稿也未提及。**此題若要補齊，必須靠 WebSearch 或訂閱制報告存取，本次工具集無法達成。**

---

## Axis A — 歷史與 cycle 統計

- **A1**（IEEE 標準批准日期／量產年）：部分查到。IEEE 802.3 官網確認負責 800G／1.6T 的任務小組為 **IEEE P802.3dj**（"200 Gb/s, 400 Gb/s, 800 Gb/s, and 1.6 Tb/s Ethernet Task Force"），頁面顯示有一份 2024-11-14 制定的 "Adopted Timeline" 文件，但**具體核准日期本身查不到**（PDF 連結嘗試 404，且 IEEE 802.3 官網為動態導覽頁，WebFetch 無法取得深層數據表）。10G/40G/100G/400G 各代標準批准年月／量產年：**查不到**（需 WebSearch 或 IEEE 官方歷史頁逐頁人工比對，超出本次工具能力）。｜`ieee802.org/3/`｜**T2**（標準組織官網，但關鍵日期缺失）
- **A2**（TOP500 InfiniBand vs Ethernet 占比）：**查不到**。`top500.org/statistics/list/` 為 JS 驅動的互動篩選頁面，WebFetch 只能讀到導覽殼層（確認「June 2026」為最新榜單存在），無法取得實際 Interconnect Family 分類數據表。
- **A3**（NVLink 各代頻寬／域大小）：**查不到**（未能定位 NVIDIA 官方白皮書或 GTC 簡報頁的可直接 URL；newsroom 首頁僅顯示近一週新聞，GTC 2026（3月）內容不在可見範圍，猜測式 URL 全部 404）。
- **A4**（前次光通訊資本週期峰谷）：**查不到**（需 JDSU/Finisar/Lumentum 十年以上 10-K 逐年比對或產業歷史統計站，超出本次可行範圍；建議 writer 改用 T2 產業統計並註明降級，設計稿本身已預留此 fallback）。
- **A5**（800G ASP 歷史落點，含 100G/400G）：**查不到**（與 D6 同源限制——需 LightCounting/Omdia/Yole 原始新聞稿，皆不可及）。

---

## Axis B — 供給

- **B1**（交換矽產品發表/出貨日）：**查不到**。Broadcom Tomahawk 6／Tomahawk Ultra／Jericho 4、Marvell Teralynx 10、NVIDIA Spectrum-X／Spectrum-6 的官方新聞稿發表日期需要新聞搜尋定位（各公司 newsroom 首頁僅顯示最近數週內容，GTC/OFC 等發表會的舊聞不可見，猜測式 URL 未命中）。
- **B2**｜**AVGO 最近四季**：見上方 D7(i) 已整理 Q1–Q3 FY26 三季 AI semiconductor revenue（$8.4B／$10.8B／$16.7B）與 Q4 FY26 guide（$21.7B）；Semiconductor Solutions 分部總營收：Q1 FY26 $12,515M、Q2 FY26 $15,009M（10-Q 與新聞稿一致）、Q3 FY26 隱含由 $29.6B 總營收×70%≈$20.839B（新聞稿明確標「$20.839 billion (70%)，+127% YoY」）。**Networking 未單獨分列**（10-Q 與新聞稿皆無此細分行）。｜**T1**｜as-of 2026-09-02（Q3 FY26 電話會/新聞稿）
- **B3**｜**ANET 最近四季**：見 D7(i)。FY26 全年指引：新聞稿中僅見逐季展望（無單一 FY26 全年數字被本次擷取到，可能藏在法說逐字稿）。**「AI 相關營收目標」原句查不到**（新聞稿無此揭露，需逐字稿）。遞延營收與採購承諾：遞延營收已列出四季序列（見上）；purchase commitments **新聞稿均未揭露**（10-Q 附註可能有，未及查）。｜**T1**（已取得部分）／缺口標注
- **B4**（Innolight／Eoptolink／COHR／LITE／Fabrinet／CIEN 最近一季）：COHR 與 LITE 已在下方 B5 取得；Innolight（300308.SZ）、Eoptolink（300502.SZ）、CIEN**查不到**（陸股公告需巨潮資訊網逐檔查詢，CIEN 需另開 EDGAR 檢索，本次未及做）。
- **B5**｜**光引擎鎖喉現值**：
  - **Coherent FQ4 FY2026**（截至約 2026-06/07，8-K 2026-08-12）：Datacenter & Communications 分部營收 **$1,615.0M**（去年同期 $1,018.3M，YoY +58.6%）；FY26 全年營收 $7,118.2M，FY26 資本支出 $1,102.9M；新聞稿僅有定性敘述「AI datacenter architectures increasingly transition from copper to optical connectivity」，**無 lead time 週數、book-to-bill、售罄年份的具體數字或原句**（該類細節高機率在法說逐字稿，未能取得）。
  - **Lumentum FQ4 FY2026**（8-K 2026-08-11）：總營收 $1.01B（YoY +109.3%），FY26 全年 $3.01B；分產品類（非分光引擎/系統）：Components $649.4M／Systems $356.9M；提及「OCS solutions 與 cloud module 業務正在推進 1.6T 導入」但**無 lead time／InP 產能／book-to-bill 具體數字**。
  - ｜來源：COHR 8-K exhibit 99.1（`sec.gov/Archives/edgar/data/820318/000119312526346860/`）、LITE 8-K exhibit（`sec.gov/Archives/edgar/data/1633978/000162828026055726/`）｜**T1**｜as-of 2026-08-11／2026-08-12
  - **本題最關鍵的 lead time／book-to-bill／售罄狀態查不到**——需法說逐字稿，本次工具無法取得。
- **B6**（AEC 競爭格局現值）：CRDO 10-Q 確認 AEC 貢獻本季營收增量 90% 以上，但**無份額或價格的法說原句**（10-Q 非法說稿）；競爭者（MRVL／ALAB／APH／TE／Semtech／Spectra7／Point2）**已公告量產或客戶認證產品清單查不到**（需個別新聞稿搜尋）。
- **B7**（retimer 供給）：**Astera Labs Q2 2026**：總營收 $392.4M（YoY +104%）；管理層預期 Scorpio fabric switch 將於 2026 Q3「提前一季」成為最大產品線（"one quarter ahead of prior expectations"）。Aries／Scorpio 個別營收占比**未揭露**。競爭者（Broadcom PCIe retimer／Montage／Parade／Rambus）已公告產品**查不到**。｜來源：ALAB 8-K exhibit（`sec.gov/Archives/edgar/data/1736297/000173629726000033/q226exhibit991.htm`）｜**T1**｜as-of 2026-08-04
- **B8**（利潤池絕對金額）：**未完成**——需要把 B2–B7 已取得的營收數字按環節加總，且多數環節缺營業利益數字（僅營收）。時間所限，本次交回原始數字供 writer 自行彙總，不代為推算利潤率（依 sources.md 規則，無 source 的利潤率必須降定性）。
- **B9**（BOM 結構、毛利率）：**查不到**（BOM 拆解通常來自 Yole/TechInsights 付費報告或產業媒體深度拆解，本次工具無法取得；毛利率可由已抓到的營收數字搭配 10-Q 損益表自算，但因篇幅未及展開）。

---

## Axis C — 需求

- **C1**（AI 網路 TAM 三家獨立預測）：**查不到**。Dell'Oro／LightCounting／650 Group／Omdia 官網新聞稿頁全數不可及（403 或無相關內容）。
- **C2**（每顆加速器網路含量）：**查不到**（需拆解報告或 NVIDIA rack 規格頁，猜測 URL 全部 404）。
- **C3**（800G/1.6T 出貨量預估序列）：**查不到**（同 D6/C1 限制）。
- **C4**（四大 hyperscaler capex）：**部分取得**——
  - **META**：2026Q2（截至 2026-06-30）實際 capex **$31.08B**；FY2026 guidance **收窄為 $130–145B**（前次展望為 $125–145B）。無 2027 展望。
  - **AMZN**：2026Q2 capex **$54.2B**（去年同期 $32.2B）；TTM（至 2026Q2）**$169.0B**，YoY +64%。管理層敘述capex增加"primarily reflects investments in artificial intelligence"。無明確 FY26/27 guidance dollar figure。
  - **GOOGL**：2026Q2 capex **$44.924B**。無 FY26/27 guidance；提及 2026-06 完成 $49.6B 融資「用於擴大 AI 基礎設施與全球運算容量的資本支出」。
  - **MSFT**：FQ4 FY26（截至 2026-06-30）capex **$35.802B**；新聞稿無前瞻 guidance 或 AI 基礎設施具體評論（CFO Amy Hood 談雲端營收成長，未談 capex 展望）。
  - ｜來源：各公司 2026Q2 earnings 8-K exhibit（EDGAR，公司名/CIK：META 1326801、AMZN 1018724、GOOGL 1652044、MSFT 789019）｜**T1**｜as-of 各 2026-07/08 財報日
  - **註**：以上皆為「實際 capex」而非「官方 2026/2027 前瞻指引具體數字」——後者多在財報電話會議逐字稿中給出範圍，本次新聞稿文字檔未包含，屬缺口。
- **C5**｜**NVDA networking 分部營收**：**重大結構性發現**——NVIDIA 自 FQ2 FY27（截至 2026-07-26，8-K 2026-08-26）起，**其 10-Q 與 CFO commentary／新聞稿皆已不再單獨揭露「Networking」子項營收**，僅維持「Compute & Networking」合併可報導分部（本季 $88,299M vs 去年同期 $41,331M）與「Graphics」（$7,922M）兩分部；新聞稿全文（`q2fy27pr.htm`）逐字搜尋「networking」一詞出現 **0 次**。Data Center 總營收 $89.0B（QoQ +18%、YoY +117%）。**這代表 writer phase1 草稿中作為 K4 換相 kill metric 的「NVDA networking 分部季營收」指標，若指的是曾經存在的獨立 Networking 揭露行，該揭露口徑已在最近一或兩季消失，需要 writer 重新設計 K4 或改用其他驗證器。**｜來源：NVDA 10-Q（`sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm`）＋CFO commentary（`sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27cfocommentary.htm`）＋press release｜**T1**｜as-of 2026-08-26
- **C6**（客戶集中度）：**CRDO** 已取得（見 B2/D7 上方，Customer A 43%／Customer B 28% by contracting party；Customer D 33%／C 28%／E 13% by end-customer，10-Q as-of 2026-08-01）。ALAB／COHR／LITE 的客戶集中度揭露**查不到**（需另行深入各自 10-K 附註，時間所限未完成）。

---

## Axis D — 驗證

- **D1**（三角對帳）：**未完成**——已取得 C4 四大 hyperscaler 2026Q2 單季 capex 實際值，但缺 2026 全年 guidance 加總與供應商 2026 營收共識（後者本身需共識資料庫，非 SEC filing 可得），故三角對帳無法在本次完成，交由 writer 用已取得的單季 actual 數字自行框列一個「部分三角」並註明缺口。
- **D2**（資本週期指標）：COHR FY26 全年 capex $1,102.9M、營收 $7,118.2M（capex/revenue ≈15.5%，非 capex/折舊比，折舊數字**查不到**，未及深入現金流量表附註）；LITE 新聞稿無 capex 數字。AVGO／Innolight capex／折舊、各家 ROIC、擴產 lead time 月數：**查不到**。
- **D3**（lead time 逐期序列）：**完全查不到**（同 B5 缺口，需法說逐字稿）。
- **D4**（庫存訂單）：COHR book-to-bill、ANET 遞延營收已有序列（見上，D7/B3），採購承諾與 CRDO/ALAB backlog 表述、光模組四家存貨週轉天數：**查不到**。
- **D5**（priced-in／forward P/E 分位）：**查不到**——這類「forward P/E 現值＋5年分位」數據通常來自站內 dd-screener/DD 既有資料庫或彭博類終端，非 SEC filing 可得，本次工具集無法計算或查證（writer 的 phase1 草稿本身已引用站內 DD 決策欄數字，應直接沿用而非要求本 agent 重查）。
- **D6／D7／D8**：見最高優先三題段落。

---

## Axis E — 替代與圈外掃描（五條，已逐條掃描，非跳過）

- **E1**（中國替代）：**查不到具體公告**。已嘗試 EDGAR 全文檢索與直接官網查詢無果（中國廠商公告不在 SEC EDGAR 體系內，需巨潮資訊網或中文財經站，WebSearch 不可用時難以定位；BIS 官方規則頁 `bis.gov/press-release` 回傳 404，猜測式 URL 未命中正確路徑）。**掃描結論：已嘗試多個資訊管道，本次未能取得 2026 年中國國產交換晶片量產狀態、中國光模組廠海外產能公告、或最新 BIS 規則文號——非「查無此事」而是「本次工具管道查不到」，請 writer 勿誤讀為零威脅。**
- **E2**（替代技術跳躍）：NVIDIA Quantum-X／Spectrum-X Photonics 出貨時點與客戶：**查不到**（newsroom 首頁僅顯示最近一週內容，猜測式產品頁 URL 全部 404，GTC 2026 keynote 內容不可及）。Google OCS/Apollo 部署規模：**查不到**。LPO/LRO 量產客戶：**查不到**。空芯光纖商用公告：**查不到**。**已掃描但全數落空，非顯而易見無關而跳過。**
- **E3**（需求方自供／垂直整合）：**查不到具體公告清單**，但 ALAB 8-K 附帶間接訊號——公司自身產品線（Taurus retimer for 224G Ethernet／UALink）與 Scorpio fabric switch 的敘述隱含 hyperscaler 對開放生態的需求持續存在（非直接證據，僅供參考，**T1** 來源但屬間接推論不可直接當作「已自供」證據）。AWS/Google/Meta/Microsoft 自研網路矽或 NIC 官方公告、白牌交換器（Accton/Celestica/Quanta）採用公告：**查不到**。
- **E4**（監管／地緣）：AVGO 與 NVDA 10-Q 的 Legal Proceedings 章節因文件過大遭 WebFetch 截斷，**未能讀到具體反壟斷／調查揭露內容**（非確認無揭露，是讀取失敗）；USTR/CBP 關稅或原產地規則變動、台馬泰光通訊產能地緣集中度官方統計：**查不到**。
- **E5**（標準與生態）：**部分取得**——UALink 1.0（200G）規格已於 2025 年發布（consortium 官網確認），**截至 2026-08 無可查證的量產矽出貨公告**，產業論述（ALAB）已轉向 UALink 2.0 時程討論（見 D7(iii)）。Ultra Ethernet Consortium 規格版本／符規產品、OCP ESUN 成員與時程、PCIe 7.0 發布狀態：**查不到**。**此軸五條中僅 UALink 一項有實質進展可回報，其餘四項為工具限制下的空白，非查證後判定無關。**

---

## 回報尾段（依指示必附）

**(i) T1（含 T1-zh）自估占比**：本次交回的證據中，**有具體數字支撐的條目**（AVGO/ANET/CRDO/NVDA/META/AMZN/GOOGL/MSFT 各季營收與 capex、COHR/LITE 分部營收、ALAB 營收、APH 分割 8-K、Yahoo 價格數列）估計 **~75-80% 為 T1**（皆直接來自 10-Q 原文或 8-K/exhibit 99 新聞稿全文，非二手轉述）；價格數列（APH/FN 收盘价）標 T2（資料聚合商即時流，非申報文件本身）；TrendForce 一條為 T2-zh。**但若把「本應完成的 33 題」全數計入分母（含大量查不到項目），則已答且達 T1 標準的題目占比遠低於 60% floor**——這是工具受限（WebSearch 額度耗盡）造成的結構性缺口，不是來源品質判斷失誤。writer 需要決定：(a) 對缺口項目啟用 `--t1-floor 45` 覆蓋並註明理由，或 (b) 另行安排有 WebSearch 權限的採集回合補齊 Axis A／C1-C3／D3／D6／E1-E2/E4-E5。

**(ii) 仍缺官方一手來源的承重數字清單**：
- D6 800G/1.6T ASP 逐期序列（完全空白）
- A1-A5 全部歷史/cycle 數字
- C1-C3 TAM 與出貨量預測（三家機構）
- C2 每 GPU 網路含量拆解
- B1 交換矽產品發表/出貨確切日期
- B5/D3 光引擎 lead time／book-to-bill 具體數字（COHR/LITE 法說逐字稿層級）
- D2 完整資本週期指標（折舊、ROIC、擴產月數）
- D5 全部 priced-in 分位數字（建議直接沿用站內 dd-screener）
- E1/E2/E4 全部（中國替代、CPO 出貨客戶、監管調查細節）
- ANET「AI 目標 $3.5B 凍結」原句（需法說逐字稿）
- NVDA networking 分部營收歷史序列（C5/K4）——**該揭露口徑本身可能已在 FQ2 FY27 停止**，需 writer 決定是否改指標

**(iii) D6／D7 取得狀況**：**D6 完全落空**（紅色警示，如指示要求置頂——已在文件最上方標注）。**D7 部分達成**：(i) AVGO/ANET/CRDO 營收序列取得良好（T1，AVGO 6季中5季有精確$金額）；(ii) 2026 年 Ethernet AI 叢集部署案例 3 例——**完全查不到**；(iii) UALink 1.0 出貨狀態——**確認「無」**，且有 T1 佐證（ALAB 談論 UALink 2.0 時程，隱含 1.0 未量產）。**換相雙閘的 K1（ASP）目前無法成立（來源全空），K3（AVGO+ANET+CRDO QoQ 合計）可用已取得數字計算**（AVGO 明確QoQ正成長；ANET 逐季正成長；CRDO 僅一季無法算 QoQ，需 writer 補前一季 $ 金額，10-Q 未揭露前一季絕對值）。

**(iv) 兩個 T1 來源數字衝突**：本次採集**未發現兩個 T1 官方來源給出矛盾數字的情形**（多數缺口是「查不到」而非「數字互相打架」）。唯一需要 writer 注意的口徑落差：AVGO 的「AI semiconductor revenue」與 writer phase1 草稿中提及的「AI networking」用語不完全同義——AVGO 官方揭露口徑是整體 AI 半導體（含客製 ASIC／XPU／networking 矽），並非單獨的 networking 子項，**這不是衝突，而是 writer 需要在報告中明確聲明口徑差異**，避免讀者誤以為 $16.7B 全部是網路收入。
