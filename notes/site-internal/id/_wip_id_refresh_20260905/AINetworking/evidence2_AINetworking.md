# Evidence Pack 2 — AI Networking（第二輪採集，2026-09-05，補缺口）

**環境確認**：本輪 WebSearch 仍完全不可用（額度已罄，google/bing/duckduckgo 全封）。全程僅用 WebFetch 直打已知 URL（SEC EDGAR browse-edgar／efts.sec.gov 全文檢索、公司 IR 直連頁、Wikipedia、標準組織官網、federalregister.gov API）。以下逐題標注結果與 T 級。

---

## P0｜市場撮合價（本輪最高優先）— **仍未取得任何真正的模組 ASP 序列**

**結論置頂：P0 撮合價依然全數落空。** 四條路徑逐一嘗試，結果如下：

1. **AAOI 10-K／10-Q MD&A（ASP/unit shipment 原句）**：**查不到（已試多份文件與精確定位提示）**。
   - 確認 EDGAR 全文檢索（`efts.sec.gov`，真實查詢，非摘要）AAOI 歷年 10-K 含「average selling price」字串命中 11 份，含最新 FY2025 10-K（filed 2026-02-26，accession 0001437749-26-005875）與 FY2024 10-K（filed 2025-02-28）。**但** WebFetch 對這兩份大型 HTML 文件（2.7MB／類似大小）的抓取＋小模型摘要管線在到達 Item 7 MD&A 之前即被截斷（截斷點落在 Item 1A 風險因子附近），多次以不同 prompt（含明確要求跳到「Item 7」「page 23」）重試皆無法取得該段落原文。10-Q（period 2026-06-30, filed 2026-08-06, accession 0001437749-26-026278）同樣在 Note 11 附近截斷，未達 Item 2 MD&A（page 23）。
   - **改試 AAOI 最新一期 8-K exhibit 99.1 財報新聞稿**（filed 2026-08-06，accession 0001683168-26-006055，`sec.gov/Archives/edgar/data/1158114/000168316826006055/aaoi_ex9901.htm`）——**成功取得財務數字但無 ASP**：Q2 2026 總營收 $191.9M（去年同期 $103.0M）、Data Center 營收 $107.7M（去年同期 $44.8M）、GAAP 毛利率 27.7%／non-GAAP 29.8%；CEO 談話僅有定性描述「800G products…more than doubled sequentially」（無單價、無出貨顆數）；Q3 2026 展望營收 $255–290M。**結論：AAOI 近年財報揭露已不含逐產品 ASP 或出貨單位數，這是揭露口徑本身的限制，非採集失敗。**｜來源＝T1（8-K exhibit 99.1）｜as-of 2026-08-06
2. **中際旭創／新易盛年報（implied ASP）**：**未嘗試成功**——本輪未再測試（陸股公司公告不在 SEC EDGAR 體系，`cninfo.com.cn` 類站點在前一輪已知不易存取，本輪時間分配優先給 P0-1／P1，未重複驗證是否仍 403；視為與前一輪同狀態的缺口延續）。
3. **FS.com 公開通路報價 ＋ Wayback 快照**：**完全查不到**。`fs.com`（首頁與任何猜測式產品頁 URL）WebFetch 全部回傳空內容／無法解析（非 403，而是回傳空白頁殼層，判斷為需要 JS 執行或反爬蟲阻擋，WebFetch 無法繞過）。未能取得任何 fs.com 頁面內容，故 Wayback Machine 快照比對步驟未能執行（沒有可鎖定的基準 URL）。
4. **替代品（AEC／EML）單價序列**：**查不到**。CRDO 10-Q／8-K 新聞稿均未揭露 AEC 每條單價（見下 P1，10-Q 明說 AEC 貢獻營收增量 90%+，但無單價或單位數字）。

**若要補齊 P0，本輪工具集判定為結構性不可行**（需要 LightCounting/Omdia/650 Group 等訂閱制報告，或可用的 WebSearch 去定位陸股/公開通路頁面）——與前一輪 D6/A5 判定一致，非本輪執行力問題。

---

## P1｜換相雙閘第二訊號 — **CRDO QoQ 序列已補齊；叢集部署案例仍空；NVDA 揭露口徑歷史已查清**

### CRDO 前季營收絕對值（K3 用）— **已解決**
逐季序列（10-Q／8-K exhibit 99.1 原文數字）：
- Q3 FY26（截至 2026-01-31）：**$407.012M**
- Q4 FY26（截至 2026-05-02）：**$437.0M**（QoQ +7.4%）
- Q1 FY27（截至 2026-08-01）：**$479.0M**（QoQ +9.6%；YoY +114.7% vs Q1 FY26 $223.074M，與前一輪一致）
- Q1 FY27 財報稿中管理層對 Q1 FY27 給出的原始 guidance 為 $465.0–475.0M——**實際 $479.0M 超出財測上緣**。
｜來源：CRDO 8-K exhibit 99.1（Q4 FY26，`sec.gov/Archives/edgar/data/1807794/000162828026039474/credoq42026ex-991.htm`）＋ 10-Q（Q1 FY27，`sec.gov/Archives/edgar/data/1807794/000162828026060111/crdo-20260801.htm`）｜**T1**｜as-of 2026-06-01／2026-09-02（filing 日）
**K3（AVGO+ANET+CRDO QoQ 合計）現在三家均可算 QoQ**：AVGO Q3→Q2 FY26 明確正成長（見第一輪 D7）、ANET 逐季正成長（見第一輪）、CRDO 三點序列如上，逐季皆正成長。

### 2026 年具名 Ethernet AI 叢集部署公告 ≥3 例 — **仍完全查不到**
- 唯一命中：**AWS × NVIDIA「新增 200 萬顆 GPU」公告**（2026-08-26，`nvidianews.nvidia.com`）——**但公告內容未提及所用互連技術**（未明說 Ethernet／Spectrum-X／InfiniBand），無法計入「Ethernet AI 叢集部署」案例。｜T1（來源真實存在）但**不滿足題目「Ethernet」條件**｜as-of 2026-08-26
- Broadcom newsroom（`broadcom.com/company/news/product-releases`）：頁面僅回傳空殼（JS 渲染），無法取得任何 2026 年新聞內容。
- Arista investor 頁：`investor.arista.com` DNS 無法解析，`investors.arista.com/news-releases` 回傳 404——**兩個猜測域名均失敗，正確 IR 網址未能定位**（無 WebSearch 無法查證正確網址）。
- AWS blogs／Google Cloud blog／Meta engineering blog：本輪未及嘗試（時間分配給 NVDA 揭露口徑追查，見下，判斷該題資訊密度更高）。
- **結論：本題本輪仍 0/3，較上輪無實質進展（唯一新發現的 AWS/NVDA 公告不滿足「Ethernet」限定條件）。**

### NVDA Networking 揭露口徑變更歷史 — **已解決，重大發現**
逐季 Networking 營收（Data Center 內 Compute vs Networking 兩行揭露）與揭露存續狀態：
- **Q2 FY26**（截至 2025-07-27）：Networking **$7,252M**（YoY +98%、QoQ +46%）｜來源：CFO commentary `sec.gov/Archives/edgar/data/1045810/000104581025000207/q2fy26cfocommentary.htm`｜**T1**
- **Q3 FY26**（截至 2025-10-26）：Networking **$8,187M**（vs 去年同期 $3,127M）；同期 Compute $43,028M（vs $27,644M）｜來源：10-Q Note 13 Segment Information，`sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm`｜**T1**
- **Q4 FY26**（截至 2026-01-25）：Networking **$11,000M**（YoY +263%、QoQ +34%）；FY26 全年 Networking **$31.376B**（YoY +142% vs FY25 $12.990B）｜來源：CFO commentary `sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26cfocommentary.htm`｜**T1**
- **Q1 FY27**（截至 2026-04-26）：**揭露口徑已改變**——10-Q 僅存「Compute & Networking」合併可報導分部一行（$74,550M vs 去年同期 $39,589M），**不再單獨列 Networking 子項**。｜來源：`sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm`｜**T1**
- **Q2 FY27**（截至 2026-07-26）：與第一輪已確認一致，新聞稿全文「networking」出現 0 次，維持合併揭露。

**結論**：Networking 獨立揭露行**在 Q4 FY26（2026-01-25 止，2026-02-25 發布）之後、Q1 FY27（2026-04-26 止，2026-05-20 發布）之前消失**——最後三個有揭露的季度為 **Q2 FY26 $7,252M → Q3 FY26 $8,187M（+12.9% QoQ）→ Q4 FY26 $11,000M（+34% QoQ）**，三點序列逐季加速成長，之後即斷點。**Writer 若要用 K4 當換相 kill metric，此指標在 Q1 FY27 起已結構性失效，需改用其他驗證器（如 AVGO AI semiconductor revenue 或 CRDO/ANET 序列）或明確標注此揭露口徑已停止。**

---

## P2｜標準與生態 — **多數取得，含關鍵空白**

- **UALink**：UALink Consortium 官網最新 2026 年新聞僅一則——**2026-04-07「UALink Consortium Publishes Four Specifications」**（支援多工作負載環境部署、效能與易導入性提升，未提及 1.0 或 2.0 版號字樣本身，但為 2025 年 1.0（200G）之後的擴充規格）。**截至本輪查證日，仍無任何「已公告採用該規格的矽產品」清單或出貨新聞**（與第一輪 ALAB 8-K 佐證的「UALink 2.0 時程仍在討論」一致，方向不變）。｜`ualinkconsortium.org`｜**T2**｜as-of 2026-04-07
- **Ultra Ethernet Consortium（UEC）**：現行規格版本 **1.0.3**（頁面更新日 2026-08-05），另有「1.0 White Paper」可下載。**官網未列出任何符規產品或已認證清單**；頁面 FAQ 仍殘留「We expect the first full standards-based products from 2024」的過時陳述（截至 2026-08 頁面更新時仍未移除，暗示官網本身可能未積極維護符規產品清單，或市場上確實仍無可具名的符規產品）。｜`ultraethernet.org`｜**T2**｜as-of 2026-08-05
- **OCP ESUN**：**查不到**——`opencompute.org` 首頁與 ESUN 專案頁（`/projects/ethernet-scale-up-networking-esun`）分別回傳空殼／403 Forbidden，無法取得任何內容。
- **PCIe 7.0**：**已正式發布**——PCI-SIG 於 **2025-06-11** 官方宣布 PCI Express 7.0 規格定案（早於本 ID 報告的 2026 as-of，屬既成事實非展望）。對照：PCIe 6.0 定案於 2022-01-11；PCIe 5.0 定案於 2019-05-29。｜來源：Wikipedia「PCI Express」條目｜**T2**｜as-of 條目最後編輯（查證日 2026-09-05）
- **IEEE 802.3 800G/1.6T 標準**：**IEEE Std 802.3df-2024** 由 IEEE-SA Standards Board 於 **2024-02-16** 核准（涵蓋 400GbE 與 800GbE 相關規格）。任務小組頁面另有一份「Adopted Timeline」文件（檔名日期 2022-10-04）與「Key Motions」文件（2022-11-17），但文件內部具體里程碑日期本輪未能取得（頁面為導覽殼層，深層 PDF 內容不可及）。｜`ieee802.org/3/df/index.html`｜**T2**｜as-of 頁面最後更新 2024-02-20

---

## P3｜歷史錨點與含量曲線

- **A2（TOP500 互連占比）**：**仍查不到**。`top500.org/statistics/list/` 確認為 JS 驅動的互動篩選介面（頁面本身顯示「Interconnect Family」為可選分類項，且確認 2026 年 6 月為最新榜單），但實際數據表需要前端互動操作產生，WebFetch 僅能讀取殼層，無法取得任何百分比數字。
- **A3（NVLink 逐代規格）**：**已解決（Wikipedia，T2）**：
  - NVLink 1.0（2016）：20 GB/s／link，4 links＝160 GB/s 聚合；DGX-1 最多 8× P100
  - NVLink 2.0（2017）：25 GB/s／link，6 links＝300 GB/s；V100 4 顆全連接
  - NVLink 3.0（2020）：50 GB/s／link，12 links＝600 GB/s；A100 世代
  - NVLink 4.0（2022）：50 GB/s／bidirectional link，18 links＝900 GB/s；Hopper 世代，NVSwitch 支援最多 32 個雙通道埠
  - NVLink 5.0（2024，Blackwell）：100 GT/s，18 links＝1,800 GB/s
  - **NVLink 6（2026-01-05 公告，Vera Rubin NVL72）**：每 GPU 3.6 TB/s；機櫃層級 scale-up 頻寬 260 TB/s
  ｜來源：`en.wikipedia.org/wiki/NVLink`｜**T2**｜as-of 條目查證日 2026-09-05
- **A4（前次光通訊週期峰谷，Finisar／JDSU-Viavi）**：**未完成**——嘗試以 ticker「viavi」查 EDGAR browse-edgar 未命中（需正確 CIK 或公司全名，本輪僅一次嘗試即失敗，未及用 CIK 912093 重試或改查 Finisar CIK 1094739 的歷史 10-K），時間分配優先給 P0/P1 已耗盡，**此題延續為缺口**，建議下輪直接用 CIK（Finisar 1094739、Viavi/JDSU 912093）而非公司名重試。
- **C2（每 GPU 網路含量）**：**查不到**——NVIDIA GB200 NVL72 官方頁與 developer blog 本輪未及嘗試（時間所限，優先順序讓給 P0-P2），**未嘗試不代表無解**，建議下輪直打 `nvidia.com/en-us/data-center/gb200-nvl72/`。

---

## P4｜餘力項目（本輪未執行）

- **B5（光引擎 lead time／book-to-bill）**：`investor.coherent.com` DNS 無法解析（域名可能已變更或不存在，正確 IR 網址需 WebSearch 確認，本輪猜測失敗）；Lumentum IR 頁本輪未嘗試。**沿用第一輪結論：此題仍完全查不到具體數字，僅有第一輪已取得的 COHR/LITE 分部營收（T1）可用。**
- **E1（出口管制）**：federalregister.gov API **可正常呼叫**（非猜測，回傳真實 JSON 結果）。以關鍵字「export control semiconductor networking」查詢近期文件，**未命中任何直接針對高速網路設備的 2026 年 BIS 新規則**；查到的相關但非直接命中項目：
  - 2026-07-14｜Commerce Dept (BIS)｜「Enhanced Favorable Treatment for the United Arab Emirates Under the Export Administration Regulations」
  - 2026-06-10｜Department of Defense｜「Notice of Availability of Designation of Chinese Military Companies」
  這兩則與 AI 網路矽晶片出口管制**間接相關**（UAE 待遇調整、中國軍工企業清單）但**非直接管制光模組/交換矽的新規則**，未能證實或證偽「2026 年 BIS 是否已將高速網路設備納入管制」，須標注為「查不到直接命中，非零結果」。
- **E4（反壟斷）**：本輪未嘗試（NVDA/AVGO 10-Q Legal Proceedings 段落上輪已知因文件過大遭截斷，本輪未再測試不同 prompt 策略）。

---

## 回報尾段

**(i) P0 是否拿到**：**沒有拿到**。四條路徑（AAOI filing MD&A／中際旭創年報／fs.com 公開報價／替代品單價）全數落空，其中 AAOI filing 路徑首次證實「不是查不到，而是近年財報揭露口徑本身已不含逐產品 ASP／出貨顆數」（8-K 新聞稿有讀到但無此類數字）；fs.com 為工具層級無法存取（非 403，是空白頁殼層）。**此為結構性缺口，非本輪執行疏漏**——如需真正解決，需要可用的 WebSearch 或訂閱制產業報告存取權。

**(ii) 本輪新增的高信心 T1 發現**：
1. NVDA Networking 分部揭露口徑消失的精確窗口＋最後三季完整序列（Q2/Q3/Q4 FY26：$7,252M／$8,187M／$11,000M，逐季加速）——**可直接支撐或替換 K4**。
2. CRDO 三點 QoQ 序列（$407.012M／$437.0M／$479.0M）——**K3 現在三家（AVGO/ANET/CRDO）皆可算 QoQ，換相雙閘的資料可行性問題已解決**。
3. IEEE 802.3df-2024 核准日（2024-02-16）、PCIe 7.0 定案日（2025-06-11，早於本輪 as-of）、UALink 最新規格發布（2026-04-07，仍無矽產品出貨佐證）、UEC 現行版本 1.0.3（2026-08-05 更新，仍無符規產品清單）——**E5／換相標準軸的機械檢核可用**。
4. NVLink 六代規格全表（含 2026-01-05 公告的 NVLink 6／Vera Rubin NVL72）——**A3 完整解決**。

**(iii) 仍缺、建議下輪處理方式**：D6/A5/C1-C3/A2/A4/C2/B5-lead-time/E1(直接命中)/E4——**維持第一輪判定，本輪工具集無法觸及**，需 WebSearch 或訂閱資料。A4 建議下輪直接用 CIK（Finisar 1094739／Viavi 912093）查詢，不要用公司名搜尋 browse-edgar（本輪已知會失敗）。

**(iv) 資料衝突檢查**：本輪未發現任何兩個 T1 來源給出矛盾數字。CRDO Q1 FY27 guidance（$465–475M）與實際值（$479.0M）為「財測 vs 實際」的正常落差，非衝突。
