# Evidence Pack 3 — AI Networking（第三輪採集，2026-09-05）

**環境確認**：WebSearch 仍不可用。本輪確認 Dell'Oro News（`delloro.com/news/`）與 650 Group Blog（`650group.com/blog/`）列表頁可讀（先前誤判 403 已更正），逐篇 fetch 成功；Yole（`yolegroup.com/press-release/` 與 `/press-releases/`）與 LightCounting 首頁**本輪重試仍 403**；TrendForce presscenter 可讀。TOP500 統計頁本輪用「逐字引用」重複驗證，**證實第一輪某 agent 對 TOP500 list 頁的「Slingshot 60%／InfiniBand 20%／LingQi 10%」數字為模型幻覺（hallucination）——本輪逐字引用比對後查無該等百分比或「LingQi」字樣，特此更正，該數字不可用**。

---

## P0｜市場撮合價／價格代理 — **仍未取得任何真正的 ASP／單價序列，本輪判定結構性不可行**

逐一嘗試 Dell'Oro／650 Group／Yole／TrendForce／LightCounting 列表頁與逐篇文章，**無一篇含 800G/1.6T 模組 ASP、每 Gbps 成本、AEC/DAC 單價、或 EML 晶粒單價的具體數字**。Dell'Oro 「AI Back-End Networks Switch Sales Surpass Front-End」（2026-09-03）與「Optical Transport Equipment Market Grew 15%」（2026-08-20）两篇皆只有市場規模成長率／份額，無單價。Yole 兩個 press-release 路徑本輪重試皆 403（`/press-release/`、`/press-releases/`）。LightCounting 首頁本輪重試仍 403。

**退而求其次的代理數字（唯一可用的一條，仍非嚴格 ASP）**：
- P0-1｜TrendForce：Vera Rubin 機櫃系統 ASP「預期約為 GB300 機櫃的兩倍」（定性比較句，非絕對美元數字，且是整機櫃非網路組件）｜`https://www.trendforce.com/presscenter/news/20260828-13204.html`｜as-of 2026-08-28｜**T2**（此為代理，非網路設備 ASP，寫作時須明確標注口徑差異，不可誤植為光模組價格）

**結論：本節維持紅色警示，未能拿到任何一種真正的逐期價格序列或可信代理，0 個時間點。** 若要解決，需 LightCounting/Omdia/650 Group 訂閱制報告存取或可用的 WebSearch。

---

## P1｜TAM（C1，必交物 D4）— **三則機構數字到手，口徑互不相同，未經調和**

- P1-1｜Dell'Oro（2026-09-03）「AI Back-End Networks Switch Sales Surpass Front-End Networks for the First Time in 2Q 2026」：**無具體美元金額**——新聞稿正文未揭露 AI back-end 或 front-end 網路市場的絕對美元規模，僅有質性敘述「AI 後端網路支出在短短三年內即超越前端網路市場」（VP Sameh Boujelbene 引言）與份額訊息：**800Gbps 交換器占該季 AI 後端網路 Ethernet 交換器出貨與營收的「絕大多數」**；1.6Tbps 交換器剛開始送樣，預期 2026 下半年放量；供應商排名（Ethernet AI 後端）：Celestica 第一、NVIDIA 緊追、Arista 第三（若計入遞延營收會更高）、Cisco 份額增幅最大；市場預期至少 1-2 年供給吃緊。｜`https://www.delloro.com/news/ai-back-end-networks-switch-sales-surpass-front-end-networks-for-the-first-time-in-2q2026/`｜as-of 2026-09-03｜**T2**（機構預測/研究稿，無絕對金額可用於 TAM 堆疊，僅可用於敘事佐證）
- P1-2｜Dell'Oro（2026-08-20）「Optical Transport Equipment Market Grew 15 Percent YoY in 2Q 2026」：整體光傳輸設備市場 **2026Q2 YoY +15%**；資料中心互連（DCI）子分項——IPoDWDM ZR/ZR+ 與 WDM 系統 YoY +45%；解構式 WDM 光線路系統 YoY +80%；雲端業者占光傳輸市場營收 **34%**；北美貢獻逾 40% 設備營收；近四季（2025Q3–2026Q2）前四大廠：Huawei、Ciena、Nokia、Cisco(Acacia)；亞太（尤其中國）因基建支出策略轉向而衰退。**口徑＝光傳輸設備（非交換器、非模組本身）**。｜同上網域｜as-of 2026-08-20｜**T2**
- P1-3｜Dell'Oro（2026-08-19）「Data Center Physical Infrastructure Market Forecast to Reach $120 Billion by 2030」：**DCPI 市場 2030 年達 $120B，2025–2030 CAGR 22%**（base year 2025）。**口徑明確排除網路設備／光模組**——範圍為 UPS、散熱、機櫃配電/busway、機架配電、IT 機櫃與圍籠、及相關軟體服務，**不含交換器或光通訊**，故不可直接當作 AI networking TAM，只可當同源資本開支背景數字。附帶：2030 年前將新增近 200GW 資料中心容量，2026 年為新增容量高峰後逐步放緩但維持雙位數成長；EMEA 因供電與許可挑戰下修。｜同上網域｜as-of 2026-08-19｜**T2**
- P1-4｜650 Group（2026-08-18）「Mixture of Experts and Disaggregated Architectures Are Rewriting the Rules of Network Infrastructure」（作者 Alan Weckel）：**無 TAM／市場規模數字**，全文聚焦技術架構敘事（MoE 專家數「8、64 或數百個」、Groq 3 LPU 每 MW 推論吞吐量宣稱高 35 倍、150TB/s 晶片內 SRAM 頻寬），**無可用於 D4 的市場規模輸入**。｜`https://650group.com/blog/mixture-of-experts-and-disaggregated-architectures-are-rewriting-the-rules-of-network-infrastructure/`｜as-of 2026-08-18｜**T2**（僅供敘事引用，非數字來源）
- P1-5（額外撿到，供 writer 判斷是否採用）｜TrendForce（2026-08-28）「NVIDIA's AI Rack Transition Accelerates; NVL72 Output Value to Exceed US$710 Billion in 2027」：**NVL72 機櫃系統 2027 年合計產值預期超過 $710B（較 2026 年成長 214%）**；機櫃出貨量年增逾 50%；主要 CSP 採購占比 2025 年約 70%→2026 年預期降至 60%；NVIDIA 資料中心營收占總營收比重逼近 93%。**口徑＝整機櫃系統產值（含 GPU/HBM/機構件等），非網路設備子項，不可直接當網路 TAM，只可當「機櫃整體規模」的量級對照**。｜`https://www.trendforce.com/presscenter/news/20260828-13204.html`｜as-of 2026-08-28｜**T2**

**P1 小結**：三家獨立機構（Dell'Oro ×3 篇、650 Group、TrendForce）皆有數字，但**沒有一篇給出「AI 後端網路交換器/光模組市場」本身的絕對美元 TAM**——Dell'Oro 的旗艦交換器文章只給份額與質性語句、DCPI 數字口徑排除網路設備、650 Group 文章無數字、TrendForce 數字是整機櫃非網路子項。**如實並列，不調和**：這代表目前可查證的公開新聞稿層級，沒有一家機構把「AI back-end network switch/optical TAM」的絕對美元數字放進免費新聞稿（很可能鎖在付費報告內），writer 若要用 D4 TAM 堆疊，只能：(a) 引用 Dell'Oro 質性"surpassed front-end" 判斉＋份額語句佐證趨勢方向，(b) 用 DCPI $120B/2030、22% CAGR 當同源資本支出量級背景並明確標注排除網路設備，(c) 用 NVL72 $710B/2027 當機櫃整體規模對照並標注非網路子項。

---

## P2｜承重數字補齊

### A2｜TOP500 互連占比 — **查不到（且更正前一輪的幻覺數字）**
`top500.org/statistics/list/` 與 `top500.org/lists/top500/2026/06/` 皆為 JS 驅動頁面。本輪用「逐字引用，禁止推算」的 prompt 重新驗證：list 頁確實含文字提及「Cray Slingshot 11 network」「Cray's Slingshot-11 interconnect」「Quad-Rail NVIDIA InfiniBand NDR200」「NVIDIA Infiniband NDR」等系統層級描述，**但無任何 Interconnect Family 占比百分比或「Ethernet」字樣**；statistics 頁確認為導覽殼層無數據。**更正**：先前一次 WebFetch 回應宣稱「Slingshot-11 60%／InfiniBand 20%／LingQi 10%」為模型幻覺，未見於實際頁面內容，**不得採用**。｜as-of 2026-09-05｜結論：**查不到**（已試 URL：`top500.org/statistics/list/`、`top500.org/lists/top500/2026/06/`）

### A4｜前次光通訊週期峰谷（Finisar／Viavi） — **僅取得申報清單，未取得營收數字**
- Finisar（CIK 0001094739）10-K 申報清單已取得：2000-07-31 至 2019-06-14 共 20 份 10-K（Finisar 於 2019 年被 II-VI 收購後無獨立申報）。**具體年度營收數字（2000–2003、2017–2019 峰谷）本輪未及逐份開啟比對，查不到**（已試 URL：`sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001094739&type=10-K`，僅取得清單非內文）。
- Viavi/JDSU（CIK 0000912093）10-K 申報清單已取得：2019-08-27 至 2026-08-13（最新一份，FY2026）共 8 份完整列出（原始來源提及「continuing through 1996」但本次回應被截斷未列出全部歷史）。**2000–2003 與 2017–2020 峰谷谷底營收數字本輪未及逐份開啟比對，查不到**。
- ｜結論：**A4 仍查不到具體峰谷數字**，僅有申報清單座標可供下輪直接開啟對應年份 10-K 文件（Finisar 2001/2002/2003 三份、Viavi 相應年份）。

### C2｜每 GPU 網路含量 — **部分取得（機櫃層級，非單顆 GPU 拆解）**
- GB200 NVL72：機櫃層級 NVLink 聚合頻寬 **130 TB/s**（原題設計稿引用常見數字為 GB200 NVL72 的 NVLink 域內頻寬，本次 WebFetch 抓到頁面文字為 130TB/s，與坊間引用的 NVL72 規格一致）；GB200 Grace Blackwell Superchip 單元 NVLink 頻寬 **3.6 TB/s**；技術世代為第五代 NVLink。**頁面內容未包含**：每 GPU NVLink 銅纜條數、纜線長度、每 GPU 對應光模組顆數、互連 BOM 金額——這些細節在完整 datasheet 中，本次 WebFetch 摘要未取得。｜`https://www.nvidia.com/en-us/data-center/gb200-nvl72/`｜as-of 2026-09-05｜**T1**（官方產品頁，但屬部分/摘要，非完整規格書）
- 結論：**C2 仍缺 BOM／模組顆數／纜線條數的量化拆解**，僅取得頻寬規格；建議下輪改抓 NVIDIA 官方 GB200 NVL72 datasheet PDF（非 HTML 產品頁）或 developer blog 逐篇。

### B5｜光引擎鎖喉現值 — **重大新發現（Lumentum FQ4 FY2026 法說簡報，T1）**
成功取得 Lumentum Q4 FY26 Conference Call 簡報 PDF（`https://s21.q4cdn.com/377324469/files/doc_financials/2026/q4/Q4-FY26-Earnings-Presentation_final.pdf`，透過 EDGAR/IR 頁定位，日期 2026-08-11）：
- **Components 分部**：營收 $649.4M（Q4 FY26）vs $533.3M（Q3 FY26，QoQ +22%）vs $320.4M（Q4 FY25，YoY +103%）；創下 **100G 與 200G EML 出貨新公司紀錄**；**200G EML 已占 EML 總營收逾 25%**；200G 波長 CW 雷射銷售擴展至多個模組客戶；CPO 用超高功率雷射出貨成長，「預計 CY2026 出貨前即產生實質營收」；窄線寬雷射（DCI/scale-across 用）連續 10 季環比成長，YoY +130% 以上；泵浦雷射 YoY +80%，「多個長期供貨協議已就位（scale-across 部署用）」。
- **Systems 分部**：營收 $356.9M（Q4 FY26）vs $275.1M（Q3 FY26，QoQ +30%）vs $160.3M（Q4 FY25，YoY +123%）；由「創紀錄雲端收發器出貨」帶動；**已開始 1.6T 收發器初批出貨（部分採用內部 CW 雷射）**；**OCS（optical circuit switch）放量持續，背後有「強化中的、多年期、數十億美元規模的採購協議」支撐**（原句性質：多年期＋multi-billion-dollar purchase agreement，未揭露對手方名稱或確切金額）。
- **公司整體**：Q4 FY26 總營收 $1,006.3M（Non-GAAP），連續第 8 季營收成長、連續第 3 季 QoQ 成長逾 20%；Q1 FY27 guidance：營收 $1,225–1,275M（隱含 QoQ +22–27%）、營業利益率 39.5–40.5%（QoQ 續擴張）。
- **仍缺**：明確的 lead time 週數、book-to-bill 比率數字、售罄到哪一年的具體年份——簡報全文未見這類字眼，**維持「查不到」**（已試：Lumentum Q4 FY26 conference call 簡報全 13 頁）。
｜來源：Lumentum FQ4 FY2026 財報簡報 PDF（IR 頁 `investor.lumentum.com` 定位，8-K exhibit 相關日期 2026-08-11）｜as-of 2026-08-11｜**T1**
- Coherent（COHR）：本輪嘗試 `investors.coherent.com`（重導向至 `coherent.com`，404）、`coherent.com/news`、`coherent.com/company/newsroom`、`coherent.com/news/press-releases` 全數失敗（頁面為 JS 殼層，實際新聞內容未渲染於 WebFetch 可讀範圍）。**COHR 法說簡報本輪未能取得，沿用第一輪 8-K exhibit 99.1 數字**（Datacenter & Communications 分部 $1,615.0M，YoY +58.6%）。

### E2｜CPO 出貨 — **查不到具名客戶/出貨量**
NVIDIA newsroom 列表頁（`nvidianews.nvidia.com/news`）本輪重新確認最新 10 則新聞（2026-08-26～09-03），**無一則涉及 Quantum-X、Spectrum-X Photonics、CPO 出貨或具名 Ethernet AI 叢集客戶**；列表頁分頁/分類參數（`?page=1&category=data-center`）未改變回傳內容（可能該站不支援此查詢參數，回傳同一份預設列表）。**結論：查不到**（已試 URL：`nvidianews.nvidia.com/news`、`nvidianews.nvidia.com/news?page=1&category=data-center`）。**唯一相關但不滿足題目條件的訊號**：2026-08-26「AWS and NVIDIA to Deliver 2 Million Additional GPUs」公告（未提及互連技術）——與前一輪判定一致，不計入。

### E1｜出口管制 — **查不到直接命中（Federal Register API 可用，已排除）**
以 `federalregister.gov/api/v1/documents.json` 分別用關鍵字組合「export control semiconductor」「InfiniBand networking export」「BIS networking equipment China」查詢（API 本身可正常呼叫，回傳真實 JSON），**近期（2026年）文件中無一則直接針對高速網路設備／InfiniBand／交換器的新出口管制規則**。相關但非直接命中的項目：
- 2026-07-14｜Commerce/BIS｜「Enhanced Favorable Treatment for the United Arab Emirates Under the Export Administration Regulations」（間接：UAE 待遇調整，非中國網路設備管制）
- 2026-06-10｜Defense Dept｜「Notice of Availability of Designation of Chinese Military Companies」（間接：中國軍工清單更新，非網路設備專項）
- 2026-08-07｜FCC｜「Protecting Against National Security Threats to the Communications Supply Chain Through the Equipment Authorization Program」（**電信設備供應鏈國安審查，與網路設備主題方向相關但非出口管制、非 BIS**，值得 writer 留意但非本題直接答案）
- 結論：**維持「查不到直接命中」**，非零結果——已用三組不同關鍵字查證。

---

## 回報尾段

**P0（市場撮合價）**：**仍完全落空**——Dell'Oro／650 Group／TrendForce 逐篇讀完皆無 ASP/單價數字，Yole 兩個 press-release 路徑本輪重試仍 403，LightCounting 首頁仍 403。唯一可用代理是 TrendForce 對 Vera Rubin 機櫃 ASP「約為 GB300 兩倍」的定性比較句（T2，非網路組件價格，1 個時間點 2026-08-28）。**紅色警示維持，判定結構性不可行**（需訂閱制報告或可用 WebSearch）。

**P1（TAM）**：**拿到三家機構（Dell'Oro／650 Group／TrendForce）共 5 則數字，但無一則是「AI 後端網路交換器/光模組」本身的絕對美元 TAM**——Dell'Oro AI 後端網路旗艦文章只給份額與質性語句（800G 交換器占絕大多數出貨/營收、Celestica/NVIDIA/Arista/Cisco 排名）；Dell'Oro DCPI $120B/2030（22% CAGR）口徑明確排除網路設備；TrendForce NVL72 $710B/2027 口徑是整機櫃非網路子項；650 Group 文章無數字。三則口徑互不相同，**如實並列不調和**，writer 需自行決定 D4 是否可用質性判斉+份額語句替代絕對 TAM 堆疊，或明確標注「公開新聞稿層級查無 AI 網路子項絕對 TAM」。

**其他高信心新發現**：(1) Lumentum FQ4 FY26 法說簡報（T1）——Components/Systems 分部逐季序列、200G EML 破紀錄、1.6T 初批出貨、OCS 多年期數十億美元採購協議；(2) 更正並確認 TOP500 互連占比第一輪某次回應為模型幻覺（無 Slingshot/InfiniBand/LingQi 占比數字，該引用不可用）；(3) E1 出口管制三組關鍵字皆未命中網路設備專項規則，FCC 2026-08-07 電信供應鏈國安審查規則屬相關但非直接命中，供 writer 參考。

**仍缺**：C2 完整 BOM 拆解（僅取得頻寬規格）、A4 具體峰谷營收數字（僅取得 10-K 申報清單座標）、B5 lead time/book-to-bill 具體數字（COHR 法說簡報本輪未能取得）、E2 CPO 具名客戶出貨。
