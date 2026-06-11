---
name: industry-analyst
description: 建立「產業深度報告（Industry Deep Report / ID）」— 一份跨多檔個股共用、敘事為骨表格為窗的產業研究文件。輸入產業主題（如「玻璃基板封裝」「HBM 供需循環」「GLP-1 治療藍圖」「全球航運週期」），skill 執行四軸 WebSearch / WebFetch 研究（歷史 / 供給 / 需求 / 驗證），輸出一份 §0 決策層 + 三幕共 9 章節、文字 ≥55% / 表格 ≤10 張、以「白話定義 → 技術成熟 → 供需循環 → 供需裁決 → 估值傳導 → 分歧證偽 → catalyst → 關聯個股」為敘事骨架、嵌入決策資產（玩家矩陣 / 利潤池 / TAM 三角驗證 / 資本週期 / priced-in / 證偽表）的 HTML 報告；並把對應個股登記於 §9 關聯清單，供 stock-analyst（公司 DD）自動讀取引用。v2.0 合併 industry-ds（DS）— 吸收其敘事弧 + 因果閉合 + 推導鏈 + §末 aside 來源系統。觸發：使用者提到「產業研究 / sector DD / 產業報告 / 產業藍圖 / industry landscape」「{主題} ds」「ds {主題}」「{產業} 敘述報告」「分析 {產業} 的供需循環」「{產業} 歷史與未來」「discourse {industry}」或具體主題（玻璃基板、HBM、CoWoS、AI ASIC、GLP-1、核融合、玻璃纖維基板、航運週期等）且尚未要求做個股 DD。
version: v2.1
date: 2026-06-11
---

# industry-analyst skill v2.0 — 敘事為骨、表格為窗

## 【v2.0 定位：合併 ID + DS 的單一產業深度報告】

v1.x 的 ID 是**表格 dashboard**：決策密度高、PM 掃讀快，但 70-80% 表格、讀者要自己在表格之間建因果鏈，難讀。姊妹 skill industry-ds（DS）是**供需敘事**：深入淺出好讀，但缺 ID 的決策層（PM 結論、玩家矩陣、估值傳導、證偽表）。

v2.0 把兩者合成一個 skill：**用 DS 的因果敘事弧當骨架（讀者跟著供需循環走），把 ID 的決策資產當器官嵌入對應章節**。每章先講人話、再上數據；表格不再是主體，而是敘事到該處時打開的「窗」。

### 三條核心原則

1. **敘事為骨、表格為窗**：報告的脊椎是「為何今天到這裡 → 未來會去哪裡」的因果敘事，表格是敘事到該處時打開的 dashboard 窗格，不是主體。文字 ≥55%、表格 ≤10 張、每張 ≤8 行（§9 例外 ≤16）。低於 55% 文字 = 退化成舊 ID；全無表格 = 退化成純觀點文。
2. **深入淺出**：寫給「聰明的非專業者」。每章開頭 2-3 句人話導讀（lede）、術語首現給一行白話解釋、每張表三句話框住（表前 1 句為什麼看、表後 2 句怎麼讀）、每章末 💡 對投資的意義。讀者讀完能當教科書用，又能 take away 可行動結論。
3. **決策深度不打折**：ID 的全部嚴謹性保留 — Claim Taxonomy [F:]/[I:]/[X:]/[A:]、T1 來源 ≥60%、spurious specificity 禁令、推導鏈、freshness、每個 🟡 判斷附證偽條件。深入淺出是「表達層」放鬆，不是「論證層」放鬆。

### 與 legacy ID / DS 的關係（凍結共存）

- 既有 105 份 v1.x ID + 8 份 DS **凍結為 legacy**，不主動 batch retrofit，不遷移。
- 新報告一律用 v2.0 格式，仍寫到 `docs/id/`，仍用 `id-meta` schema（schema 零改動）。
- `industry-ds` 已 deprecated，其觸發語（「{主題} ds」「敘述報告」「供需循環」「discourse」）自動轉向本 skill v2.0。
- `skill_version: "v2.0"` 即新格式標記；下游（stock-analyst / DCA / earnings-synthesis / comparator 讀 id-meta JSON + INDEX.md）零感知、零改動。

---

## 【路徑】

```
~/.claude/skills/industry-analyst/
  SKILL.md                         # 本檔（v2.0）
  templates/
    html_template.md               # HTML 視覺 & 樣式規範（v2 骨架；§2 含 S 曲線 ASCII 樣板）
    schema_fields.md               # §0-§9 章節必填 / 選填欄位 + 字數 target
    value_chain_svg.md             # 利潤池語境 value chain inline SVG 樣板
  pre_publish_check.md             # 預發布 10 道 gate
  references/                      # 跨 ID 共享事實卡與 best practice
```

輸出：

```
financial-analysis-bot/
  docs/id/
    INDEX.md                       # 產業深度報告索引
    index.html                     # 產業列表首頁（v2 卡片加「v2 敘事版」badge）
    ID_{Theme}_{YYYYMMDD}.html     # 單份產業報告
    cat-{mega}.html                # 分類 drilldown 頁（build_id_category_pages.py 生成）
```

---

## 【章節骨架：§0 決策層 + 三幕共 9 章】

設計原則：**DS 的因果敘事弧當骨架，ID 的決策資產當器官嵌入對應章節**。

| § | 標題 | 幕 | 主要形式 | 嵌入決策資產 | 字數目標 |
|:---|:---|:---|:---|:---|:---|
| **§0** | 決策摘要層 | 摘要 | **結論先行段** + 6-box 卡片 + thesis + PM 綠卡 | 結論 / TL;DR / oneliner / PM Implication | 500-800 |
| **§1** | 產業白話定義 + 歷史脈絡 | 一 | 敘事 + 1 表 | 歷史 cycle 統計表 | 1,800-2,800 |
| **§2** | 技術成熟度 + S 曲線 | 一 | 敘事 + S 曲線 + 1 小表 | S-curve（強制）+ kingmaker 小表 | 1,200-1,800 |
| **§3** | 供給側：現在與未來 + 利潤池 | 二 | 敘事 + 2-3 表 | 玩家矩陣 / 利潤池遷移 / 成本曲線 | 2,400-3,600 |
| **§4** | 需求側：現在與未來 + 三角驗證 | 二 | 敘事 + 1-2 表 | TAM 三情境推導 / 需求三角對帳 | 2,000-3,000 |
| **§5** | 供需裁決 + 短中長期推估 + 投資時鐘 | 二 | 敘事 + 1-2 表 | 資本週期證據 / 三視野×三情境 / 庫存訂單指標 / phase 判定 | 2,400-3,600 |
| **§6** | 產業經濟學與估值傳導 | 三 | 敘事 + 1 表 | unit economics / ASP / multiple pass-through | 1,400-2,200 |
| **§7** | Non-Consensus + Priced-in + Kill Scenario | 三 | 敘事 / bullet | 3 分歧（含 priced-in）+ 3 steel-man | 1,800-2,800 |
| **§8** | Catalyst Timeline + 證偽表 | 三 | bullet + 1 表 | 5-8 catalyst 雙路徑 + 證偽表 | 1,000-1,600 |
| **§9** | 關聯個股 | 三 | 表格 + 敘事 | 🔴🟡🟢 表（≤16 行）+ non-obvious | 800-1,400 |

**全文可見字數 target：16,000–22,000 字**（v2.1 上修 — 8-12K 經 pilot 驗證對母題級主題太薄、每章只剩 2-3 段、論證層被壓縮；**低於 14,000 可見字視為偷懶**，對齊 DD ≥80KB / DCA ≥50KB 的 anti-laziness 政策）。擴展靠文字不靠表格 — 表格上限不變。

### 深度擴展規則（v2.1 新增 — 用戶反饋「主要用文字擴展」的八個槓桿）

擴深度 = 補論證層，不是加長句子。以下八項是強制的敘事深度檢核（id-review critic 抽查）：

1. **機制敘事**：每個承重數字（裁決依據、catalyst 閾值、利潤池遷移）必有一段「為什麼會這樣」的因果機制 — 不是只給數字 + 推導行，要寫出背後的經濟學 / 會計 / 合約結構。
2. **歷史類比完整敘事**：§1 的 1-2 個主類比寫成完整故事（當年融資結構、逐年時序、多頭錯在哪 / 空頭錯在哪、本次量化差異逐條件對照）— 不是 3 句帶過。
3. **資金流 / 合約結構圖譜**：產業內的循環融資、預付、take-or-pay、租賃結構用敘事拆開 — 點名誰承擔終端信用風險。
4. **🔴 玩家個體敘事**：每個 🔴 ticker 在 §3（或 §9）有自己的一段深度敘事（策略、客戶結構、在本 thesis 中的位置），不只是矩陣表一行。
5. **Kill scenario 完整 steel-man**：§7 每條反方寫成空頭最強版本的完整論證段（他們的數據 + 邏輯鏈），再逐點回應 — 不是一條 bullet。
6. **情境敘事化**：§5 三情境表的 bear（至少）要有「那個世界長什麼樣」的展開敘事：誰先砍單 → 誰的營收先掉 → 股價時序。
7. **二階效應**：至少一段寫本產業變數對鄰接領域的外溢（電力 / 記憶體 / 債市 / 勞動力等，視主題）。
8. **編年史段落**：§1 或 §3 至少一處用「逐季 / 逐年推進」的編年敘事呈現關鍵競賽或轉折的時序感。

### 章節順序硬性規則

§0 → §1 → §2 → §3 → §4 → §5 → §6 → §7 → §8 → §9，**不可重排、不可刪節**。

特別地，§3 現供→未供 與 §4 現需→未需 必須在 §5 開頭合流出供需裁決；§5 投資時鐘 phase 是供需裁決的自然結論，放在裁決後因果才順。

---

### §0 決策摘要層（純 ID 優點，給掃讀的 PM）

掃讀的 PM 不讀 9 章，他讀 §0 就要拿到行動結論。本層五件事（順序固定，**結論先行**）：

1. **結論先行段（v2.1 新增，必填，報告第一個內容塊）**：3-6 句**純白話文字**把本報告結論完整寫出來 — 裁決是什麼（過剩/平衡/短缺 + 時間範圍）、最核心的一條非共識判斷、真正的風險是什麼、所以該做什麼（方向 + 標的層級）。讀者只讀這一段就知道全文說了什麼。**禁止**：用卡片 / pill / bullet 替代這段文字；埋伏筆（「詳見 §5」不算結論）；騎牆語。放在 cross-link callout 之後、6-box 卡片之前，視覺上用結論框（紫框白底，見 templates）。
2. **TL;DR 6-box 卡片**：TAM / 5Y CAGR / 投資時鐘 Phase / **供需裁決（過剩/平衡/短缺三選一）** / conviction pill（high/mid/low）/ top picks（2-3 ticker）。
3. **一句話 thesis**（≤200 字，必帶 [I:] 或 [X:] tag）→ 同步寫進 id-meta `oneliner`。這是本 ID 最核心的非共識觀點。
4. **PM Implication 綠卡**（沿用舊 §0.7，**必填，缺即 Gate 9 阻斷**）：五 bullet + ①②③④ 四行動 + conviction pill。
5. **legacy cross-link callout**（若同主題已有 legacy ID / DS）：頂部加 callout 連回去，標明本份為 v2 敘事版。

**PM Implication 綠卡五 bullet + j-logic**（缺任一 = 未完成）：

| bullet | 內容來源 | 禁止空話 |
|:---|:---|:---|
| **thesis 方向** | §7 Non-Consensus 三條 thesis 的綜合方向 | 禁止「待觀察」「暫不明朗」等無行動涵義 |
| **個股 conviction tier 變化** | §9 🔴🟡🟢 標記 + 跨 ID sync 註記 | 必須點名 ticker（不寫「部分核心股」）|
| **關鍵新監測點** | §8 證偽表 rows + catalyst 中投資人最該盯的 ≤3 點 | 必須可量化（metric + 閾值）|
| **multiple / 估值 / 週期定位風險** | §6 估值傳導判斷 + §5 Phase 位置 | 必須含當前 Phase 與下個 Phase 轉換條件 |
| **Entry 時機** | §8 catalyst 日期 + 證偽閾值距離 | 必須給「現在 / 等 catalyst X / 等回調 Y%」其中一個 |

**conviction pill**：`high`（§9 ≥2 個 🔴 且 §8 falsification 距離 >2 sigma）/ `mid`（≥1 🔴 + 至少 1 條 kill 未排除）/ `low`（thesis AT_RISK 或 BROKEN 跡象明顯）。**j-logic**：四行動 ①②③④，格式「動詞 + 具體標的（ticker）+ 觸發條件或時機」。

HTML 樣板（綠卡，沿用 DS 綠 #16A34A 點綴）：

```html
<h2>§0 決策摘要層</h2>
<!-- 6-box TL;DR 卡片 + 一句話 thesis（帶 [I:]/[X:] tag）-->
<div class="judgment-card" style="background:#F0FDF4;border-left:4px solid #16A34A">
  <div class="j-head">📊 <strong>Portfolio Implication（PM 級行動結論）</strong> <span class="j-conf high">conviction：{{level}}</span></div>
  <ul class="j-facts" style="color:#14532D">
    <li><strong>thesis 方向</strong>：{{保持 / 強化 / 降級 — 說明}}</li>
    <li><strong>個股 conviction tier 變化</strong>：{{ticker A 從 X → Y；含 cross-ID sync 註記}}</li>
    <li><strong>關鍵新監測點</strong>：{{§8 falsification metric / catalyst（可量化）}}</li>
    <li><strong>multiple / 估值 / 週期定位風險</strong>：{{de-rating window / cycle-peak proximity / 現價 vs entry 區間}}</li>
    <li><strong>Entry 時機</strong>：{{現在追高 / 等 sector correction X% / 等具體 catalyst}}</li>
  </ul>
  <div class="j-logic" style="background:rgba(22,163,74,.1);color:#14532D">→ PM 級行動：① {{action 1}}；② {{action 2}}；③ {{action 3}}；④ {{action 4}}</div>
</div>
```

---

### 第一幕：這是什麼產業、怎麼走到今天

#### §1 產業白話定義 + 歷史脈絡（深入淺出入口）

**lede（2-3 句人話導讀）**：開門見山講這產業賣什麼、誰付錢、為什麼現在重要 — 寫給聰明的非專業者，不假設讀者懂行話。

本章內容：

- **白話開場**（新規則）：這產業賣什麼、誰付錢、為什麼現在重要。第一段不准出現未解釋的行話。
- **邊界界定收斂為敘事一段**（in-scope vs out-of-scope）— 不再立表，用一段話說清楚為何這樣切、灰色地帶在哪（邊界爭議本身常是 insight 來源）。
- **歷史敘事 2-3 個轉折點**，**每個轉折強制：具體日期（YYYY 或 YYYY-MM）+ 至少一個量化錨點**（DS-9 規則，見下方【§1 歷史錨點規則】）。不允許「過去幾年」「最近」「近期」這類模糊表述。
- **1-2 個歷史類比**：當年誰看錯、為什麼（沿用舊 §2 analogs + QC 反向類比警示）。引具體前例（年份 + 主角 + 當年關鍵數據），指出當年多頭錯在哪、空頭錯在哪、本次的**量化差異**（不是「這次不一樣」空話）。
- **歷史 cycle 統計表 1 張**（新模組，見【新增分析模組】§1）：過去幾輪 cycle 的長度、峰谷振幅、**股價領先/落後基本面幾個月** — 把敘事歷史升級成可用於 timing 的統計。

章末 💡 對投資的意義：這段歷史對今天意味著什麼。

#### §2 技術成熟度 + S 曲線

**lede**：用兩三句講清「為什麼是現在，不是三年前、也不是三年後」。

- **敘事講「為什麼是現在」**：技術成熟度的因果鏈（哪個 bottleneck 剛被解、哪個成本曲線剛跨過拐點）。
- **S-curve 圖強制保留**（QC-I4，見下）：優先用官方 roadmap 數據；`<pre>` ASCII（IBM Plex Mono）為主，複雜情境改 inline SVG。
- **技術棧 kingmaker 判斷收斂為敘事 + 1 小表**：子技術 × 良率卡點 × 專利持有者，敘事點出「哪個子技術成為 kingmaker」，表只放最關鍵 3-5 子技術（不再立 ID 舊 §3 大表）。

章末 💡：技術成熟度對 entry timing / 哪家技術領導的含義。

---

### 第二幕：供需循環（DS 骨架，嵌 ID 器官）

#### §3 供給側：現在與未來 + 利潤池

**lede**：兩三句講「誰在供給、瓶頸在哪、利潤被誰賺走」。

- **現供敘事 + 玩家矩陣 1 張**（ID §6 精簡版）：top players × share × **T-2 / 現在 / T+1 三時間欄**（DS 趨勢三欄規則，讓讀者看出加速/穩定/衰退，不只是 snapshot）。新興供給結構（<3 年歷史）→ 用 T-1 / 當年 / T+1 並 footnote 註明數據起始限制。
- **利潤池遷移分析**（新模組，強制，見【新增分析模組】§3）：整條 value chain 的利潤總額分布在哪些環節、往哪遷移、誰在搶誰的池子 — 取代舊 ID §5 靜態毛利率表，用敘事 + 1 張利潤池表。
- **成本曲線**（新模組，週期性產業強制 / 結構成長型可省須註明理由）：主要廠商在 cost curve 上的位置 → 價格跌到哪誰先停產，價格戰終局判斷。
- **未供敘事**：capex pipeline（誰宣布擴 capacity、何時完成）/ 新進入者（門檻）/ 地緣政策 / 供給彈性（價格漲時多快能擴）。
- **因果閉合**（DS-2 規則）：§1 提出的結構變數（如某代際技術、護城河、製程獨家性）必須在 §3 或 §4 至少有一段（≥50 字符）直接回應「該變數在未來 3-5 年是否仍 binding」 — **不准推到判斷層（§7 Non-Consensus 不算閉合點）**。

章末 💡：12-36M 內供給能否回應需求、議價權往哪段集中。

#### §4 需求側：現在與未來 + 三角驗證

**lede**：兩三句講「誰在買、為何買、哪塊需求最不可替代」。

- **現需敘事**：end-market mix / 地域分布 / 客戶集中度 / pricing power（哪段需求最 price inelastic）。
- **未需：TAM 三情境表含推導鏈**：base / bull / bear，每個數字「推導：A×B→C」可回溯（見【推導可追溯性原則】）。bull/bear 偏離 base 必須由「假設改了什麼」推出，不准黑盒數字。
- **需求三角驗證**（新模組，硬規則，見【新增分析模組】§4）：top-down TAM 必須與 bottom-up 對帳 — 下游客戶 capex/採購 guidance 加總 vs 上游廠商營收 consensus 加總；**兩邊差 >20% 必須解釋缺口在哪**（重複計算？樂觀滲透率？），不能只給 top-down 數字。
- **因果閉合**：若 §1 提及某需求驅動（生成式 AI / 生育率 / 人口老化），§4 必須回應「該驅動未來 5-10 年走向 / 是否拐點」。

章末 💡：哪塊需求最有定價權、TAM forecast 史上偏差、需求拐點。

#### §5 供需裁決 + 短中長期推估 + 投資時鐘

**lede**：兩三句先給結論方向 —「綜合 §3 §4，本產業未來 X 年是過剩/平衡/短缺」。

- **資本週期證據**（新模組，裁決的量化依據，至少引 2 項，見【新增分析模組】§5-1）：capex/折舊比趨勢、產業 ROIC vs WACC、新產能 lead time — 「高報酬引資本→過剩→均值回歸」機制檢查。裁決不能只靠敘事推理。
- **強制裁決**（DS bridge 規則）：「依本章 §3 與 §4 的推導，未來 X 年產業供需狀態是 **過剩 / 平衡 / 短缺**，因為 [具體原因]」。**三選一不准騎牆**，不允許「可能 X 也可能 Y」。
- **三視野 × 三情境表**：12M / 3Y / 5Y+ 各給 base / bull / bear + **可量化 trigger metric + 推導鏈**。Trigger 禁止「demand booms」「inference takes off」這種模糊詞，改寫成「NVDA inference run-rate ≥ $80B annualized（推導：DC rev $130B × 60% inference penetration）」。
- **投資時鐘 phase 判定**：當前 Phase（I/II/III/IV）+ 各 phase 贏家切換 + 換 phase 的**必要 ∩ 充分條件**。
- **庫存/訂單週期指標**（新模組，phase 判定的證據，產業適用時強制，見【新增分析模組】§5-2）：channel inventory 週數 / book-to-bill / 訂單能見度；軟體服務類改用 NRR / backlog / RPO 等對應指標。

章末 💡：本產業現在處於 cycle 哪段、下個 phase 的觸發條件、現在 act 還是等。

---

### 第三幕：錢怎麼賺、市場錯在哪、怎麼證偽（ID 判斷層，DS 語氣）

#### §6 產業經濟學與估值傳導

**lede**：兩三句講「這產業的錢是怎麼賺的、估值跟著什麼變數動」。

- **unit economics / ASP 動態**：敘事講機制 + 1 表（ROIC / Gross / Capex cycle + ASP 過去 5Y + 未來 2Y + 抗 commoditization 分析）。
- **估值傳導**：產業變數 → 公司 Fwd PE/PEG 怎麼 pass-through（敘事為主，舊 ID §8 傳導表改寫成敘事 + 敏感度錨點：「+1pp 毛利 ⇒ ? 倍數擴張」）。

章末 💡：估值現在 price 了什麼、哪個變數動會 re-rate / de-rate。

#### §7 Non-Consensus + Priced-in 檢驗 + Kill Scenario

**lede**：兩三句講「市場主流怎麼看、我們哪裡不同、為什麼這分歧還能賺錢」。

- **Priced-in 檢驗**（新模組，分歧可操作性的前提，每個分歧強制，見【新增分析模組】§7）：sector 估值歷史分位（現在 EV/Sales 或 P/E band 在過去兩輪 cycle 的哪個位置）+ 現價隱含的成長假設。**每個分歧必須對照「市場已 price 多少」** — 分歧對但已 priced 就不可操作。
- **3 個與共識的分歧**（舊 ID §12 + DS §8 同構合併）：共識說 X（引 ≥1 家主流券商/媒體 T3）/ 我們說 Y / 證據 Z（§1-§6 某處事實支撐）/ **市場 price 了多少**。每條 thesis 以 [F:] cornerstone fact + [X: base/bull/bear] 三情境呈現。禁止「本 ID 也認同 X」這種無 insight 章節。
- **3 個 steel-man 反方**（舊 ID §9.5 + DS §9 同構合併）：每條附具體路徑 + 當前證據 + 證偽窗口。想不出 3 條 = 分析深度不足，返工。
- **風險矩陣降級為敘事素材**：技術/需求/替代 + 政策補貼管制，融入本章敘事（不再獨立成章）。點名「市場最低估的風險」。

章末 💡：這三條分歧裡哪條最可操作（對 + 未 priced）。

#### §8 Catalyst Timeline + 證偽表

**lede**：兩三句講「未來 18 個月盯哪些節點、哪些數字一破就要砍」。

- **Catalyst Timeline**：18M 內 5-8 個節點，每個必含明確日期（季度層級 OK）+ 事件類別 + 檢視指標 + **雙路徑：若達成→ / 若落空→**（DS §10 + ID §10.5 同構合併）。寫成 bullet（時間線並列）。
- **證偽表**（舊 ID §13 原樣保留，這是 position-thesis-monitor 的輸入）：3-5 個 kill metrics + base/bull/bear 門檻 + 時間窗。bear 閾值即 thesis 作廢點，必須是真 falsification 不是 strawman；數字用 range。

章末 💡：最該盯的 1-2 個 leading indicator。

#### §9 關聯個股

**lede**：兩三句講「誰是這產業的純度玩家、誰是市場沒注意到的二次受益者」。

- **🔴🟡🟢 表**（≤16 行）：ticker × 角色 × 深度 × 受益/受害 × 對應 DD 連結 + **caption 時間限定**（DS-18：閾值必須明示 current actual 還是 forward-looking；若 forward-looking，每行另列 current actual 對照欄）。
  - 🔴 核心：營收 >40% 依賴此產業 OR 技術領導者
  - 🟡 次要：營收 10-40%，重要但非主導
  - 🟢 邊緣：營收 <10% 但被市場連動
- **1-2 個非顯而易見受益者敘事**（強制）：e.g. 本產業需某設備 → 該設備的乾燥爐供應商。
- 同步 id-meta `related_tickers[]`（下游 hook 不變）。對每檔查 `docs/dd/INDEX.md`，已有 DD 必附連結；否則標「DD 未建，建議後續追加」。

章末 💡：哪檔是最高純度 play、哪檔被低估其曝險。

---

## 【新增分析模組（7 個，兩個舊 skill 都沒有）】

這 7 個模組是 v2.0 review 補上、用戶已核定的。每個寫清楚落點 / 做什麼 / 強制性 / 來源要求。

### 模組 §1 — 歷史 cycle 統計

- **落點**：§1 末，1 張表。
- **做什麼**：列過去幾輪 cycle 的長度（峰到峰幾個月）、峰谷振幅（ASP / 出貨 / 營收 的 peak-to-trough %）、**股價相對基本面的領先/落後（幾個月）**。把敘事歷史升級成可用於 timing 的統計量。
- **強制性**：**有 ≥2 輪歷史 cycle 的產業強制**（半導體記憶體、面板、航運、大宗商品等）；單向結構成長、無明顯 cycle 的產業（如某些早期軟體）可省，須在章內註明「本產業尚無可統計的完整 cycle」。
- **來源要求**：cycle 長度/振幅優先 T1（公司歷史財報）或 T2（產業協會時序）；股價領先落後可用 T3-A 券商 primer 的 cycle 分析，但需註明資料窗口。
- **表格範例欄位**：`Cycle | 起訖 | 長度(月) | ASP peak-to-trough | 股價領先/落後基本面(月)`。

### 模組 §3-1 — 利潤池遷移分析

- **落點**：§3，1 張利潤池表 + 敘事。
- **做什麼**：把整條 value chain 的利潤**總額**（不是毛利率）分布畫出來 — 哪幾個環節吃掉多少 % 的產業利潤池、近 3-5 年往哪遷移、誰在搶誰的池子。取代舊 ID §5 靜態毛利率表。
- **強制性**：**強制**。
- **來源要求**：各環節利潤池 % 必 source（沿用 QC-I19：百分比無 source → 改定性「主導/均勢/次要」）。遷移方向至少引 1 項 T1/T2 的時序證據。
- **表格範例欄位**：`環節 | 利潤池占比 T-2 | 現在 | 遷移方向 | 搶/被搶`。

### 模組 §3-2 — 成本曲線位置

- **落點**：§3，敘事 + 可選 1 小表。
- **做什麼**：主要廠商在 cost curve（單位成本由低到高排序）上的位置 → 價格跌到哪個 level 誰先停產（marginal producer）→ 價格戰終局判斷。
- **強制性**：**週期性 / 大宗型產業強制**（記憶體、面板、太陽能、鋼鐵、航運、化工）；**結構成長型產業可省，但須在 §3 一句註明省略理由**（如「本產業為設計服務，無實體產能成本曲線，價格戰由 IP 護城河而非邊際成本決定」）。
- **來源要求**：cost curve 位置優先 T1（公司成本結構揭露）/ T2（產業成本研究如 Yole/IC Insights）；無精確數據時用定性序位（誰最低成本、誰是 marginal producer）。

### 模組 §4 — 需求三角驗證（top-down vs bottom-up 對帳）

- **落點**：§4，敘事（可附對帳小表）。
- **做什麼**：top-down TAM（市場研究機構的總量）必須與 bottom-up（下游客戶 capex/採購 guidance 加總 vs 上游廠商營收 consensus 加總）對帳。
- **強制性**：**強制**。**兩邊差 >20% 必須解釋缺口在哪**（重複計算？樂觀滲透率假設？口徑不同？），不能只給 top-down 數字了事。
- **來源要求**：bottom-up 的客戶 capex guidance 必 T1（法說 / IR）；上游營收 consensus 可 T2/T3-A。對帳結論寫明採信哪邊、為什麼。

### 模組 §5-1 — 資本週期證據

- **落點**：§5 裁決前，敘事（可附小表）。
- **做什麼**：用資本週期框架（「高報酬引資本進入 → 產能過剩 → 報酬均值回歸」）的三個量化指標檢查裁決：① capex/折舊比趨勢、② 產業 ROIC vs WACC、③ 新產能 lead time。
- **強制性**：**強制，裁決至少引這三個指標中的 2 項**。
- **來源要求**：capex/折舊、ROIC 優先 T1（財報）；WACC 可用合理 proxy（須註明假設，[A:] tag）；lead time 用 T1/T2（設備商交期、產能擴張公告）。

### 模組 §5-2 — 庫存/訂單週期指標

- **落點**：§5 phase 判定，敘事。
- **做什麼**：用 leading indicator 佐證 phase 判定 — channel inventory 週數、book-to-bill ratio、訂單能見度（backlog 月數）。
- **強制性**：**產業適用時強制**；軟體/服務/平台類無實體庫存 → 改用 NRR / backlog / RPO / billings 等對應領先指標（須在章內說明用了哪個替代指標及理由）。
- **來源要求**：book-to-bill / inventory 週數優先 T1（公司法說、SEMI book-to-bill）/ T2（產業協會）；事件型數字適用 14 天 freshness。

### 模組 §7 — Priced-in 檢驗

- **落點**：§7 每個分歧，敘事。
- **做什麼**：每個 non-consensus 分歧旁邊都要回答「市場已經 price 了多少」 — ① sector 估值歷史分位（現在 EV/Sales 或 Fwd P/E 在過去兩輪 cycle band 的哪個 percentile）、② 現價隱含的成長假設（reverse 推回市場隱含的 CAGR / margin）。
- **強制性**：**強制，每個分歧附 priced-in**。分歧對但已被 price → 標明「不可操作」。
- **來源要求**：估值分位需有來源（券商 valuation band 圖 T3-A、或自算但註明資料來源與窗口）；隱含成長假設的推算須附推導行。

---

## 【可讀性規則層（「深入淺出」的硬規則）】

| 規則 | 細節 | 來源 |
|:---|:---|:---|
| **文字 ≥55% / 表格 ≤10 張、每張 ≤8 行** | §9 例外可至 16 行；成本曲線 / 庫存指標表視產業屬性可省 | 新（ID 70-80% 表 ↔ DS 80% 文字的中間值）|
| **每章開頭 2-3 句「人話導讀」lede** | 不假設讀者懂行話 | 新 |
| **每張表三句話** | 表前 1 句「為什麼看這張表」、表後 2 句「怎麼讀」 | 新 |
| **術語首次出現給一行白話解釋** | 行話第一次出現括號內或破折號後白話 | 新 |
| **每章末 💡 對投資的意義 box** | 把該章事實連回投資判斷 | DS（ID 的 💡 insight bullets 併入）|
| **來源全部走節末 `<aside class="ds-refs">`，正文零 inline tag** | 每個含量化斷言的 section 末加 aside，按 URL 去重 | DS v1.2 |
| **敘事 / 條列 hybrid** | 因果鏈用段落、≥3 平行同類項用 bullet | DS v1.3 |
| **全文長度 target 8,000–12,000 可見字** | 深於 DS、短於舊 ID | 新 |

### 敘述 vs 條列判準（v1.3 hybrid，搬自 DS §360-399）

v2.0 採**內容驅動格式**：

**該 bullet 的徵兆（任一即 bullet）**：
- **3 個以上平行同類項目**：多個 catalyst、多個 falsification metric、多個情境 trigger、多個玩家比較點。
- **對稱結構描述**：每項都是「項目名：屬性 + 數字 + 影響」這種同模板。
- **無因果列舉**：top 5 玩家、4 個關鍵假設、3 個 trigger metric、3 條 Kill scenario。

**該保留敘事的徵兆（任一即敘事）**：
- **因果鏈 A→B→C**：歷史轉折推理、供需閉合、推導展開。
- **漸進論證**：一段一個結論，下段繼續延伸（§1 ChatGPT 引爆 → §3 CUDA inference 護城河 → §5 ASIC 攻擊路徑這種多段推進）。
- **解釋「為何」**：解釋一個現象成因 / 機制 / 路徑。

**章節傾向（建議，非硬性）**：

| 章節 | 預設格式 | 何時切換 |
|---|---|---|
| §0 TL;DR | 卡片 + thesis box + PM 綠卡 | （固定）|
| §1 歷史 | 敘事段落為主 + cycle 統計表 | 列舉 3+ inflection 對稱結構 → bullet |
| §2 技術 | 敘事 + S 曲線 + 小表 | （固定 S 曲線）|
| §3-§4 供需 | 敘事為主（因果推導）+ 玩家/利潤池/TAM 表 | 列舉 top suppliers / parallel drivers → bullet 或表 |
| §5 裁決推估 | 敘事 + 三視野×三情境表 | 表格固定 |
| §6 估值傳導 | 敘事 + 1 表 | unit economics 多項並列 → bullet |
| §7 Non-Consensus | bullet（3 條並列）| 因果展開段落 |
| §8 Catalyst | bullet（時間線並列）+ 證偽表 | （固定）|
| §9 ticker | 表格（固定）+ non-obvious 敘事 | （固定）|

**反 pattern（避免）**：
- ❌ 把因果鏈寫成 bullet — 「A → B」變兩個獨立 bullet，邏輯連結消失。
- ❌ 把 3 個對稱項目硬塞成段落 — 讀者要自己拆。
- ❌ Bullet 內又寫長句不分點 — Bullet 是用來 scan 的，每點 1-2 行內結束。

### 文字 55% / 表格機制（Gate 計算）

「文字比例」= 純文字字元數（含段落 + bullet 內容）/ 整篇 HTML 可見字元數（剔除 HTML tags、CSS、JS、注釋）。**bullet 內字元算文字**（`<ul>/<ol>/<li>` tags 排除，內容字元計入）。

**目標**：文字 ≥55%，即表格相關字元（含 `<table>/<tr>/<td>` 內容）≤45%。**hard cap**：表格數量 ≤10 張，每張 ≤8 行（§9 例外 ≤16；成本曲線 / 庫存指標表視產業屬性可省）。

55% 是「敘述真的負責主幹」的最低門檻 — 低於這個比例，文字會被表格切碎、退化回舊 ID。

### 來源標籤系統（§末 aside，搬自 DS v1.2）

v2.0 正文與表格**不使用 inline `<span class="source-tag">`**。每節結尾（`</section>` 之前）加 `<aside class="ds-refs">`：

```html
<aside class="ds-refs">
  <span class="ds-refs-label">本節參考來源</span>
  <ol>
    <li><span class="tier">[T1]</span><a href="https://nvidianews.nvidia.com/.../gtc-2026-keynote">NVIDIA GTC 2026 Keynote slide 47 — H100 配給 lead time 12+ 個月</a></li>
    <li><span class="tier">[T2]</span><a href="https://www.semi.org/report-xxx">SEMI 2025 Advanced Packaging Report — CoWoS capacity 2026-2027</a></li>
    <li><span class="tier">[T3-A]</span><a href="...">Morgan Stanley AI Infra Primer 2026-03-15 p.24 — ASIC capex share forecast</a></li>
    <li><span class="tier">[T1-zh]</span><a href="...">台積電 2026Q1 法說會 slide 14 — CoWoS 配額分配</a></li>
  </ol>
</aside>
```

**Aside 編排規則**：
- 同節內 URL 相同的來源只列一次（取首次出現的 tier + title）。
- `<li>` 按節內首次出現順序排列。
- 格式：`<span class="tier">[TX]</span><a href="URL">Source title — claim/page（可選）</a>`。
- 若某節**無任何量化斷言**（如純定性 phase 敘述），aside 可省略。
- §0 thesis box 若含數字 → 加 aside；只有定性判斷 → 可省略。

CSS 見 `templates/html_template.md`（`.ds-refs` / `.ds-refs-label` / `.tier` / `.source-warning` 全套搬入）。

---

## 【推導可追溯性原則（搬自 DS v1.1）】

source-tag 標「**數字來自哪裡**」；推導行標「**為什麼是這個數字而不是別的**」。

### 規則（硬性）

任何被當作「結論」的數字（TAM、CAGR、market share、滲透率、ASP、產能、capex 規模、bull/bear delta），在初次出現的**同段或前一段**內，必須附 ≤3 行推導：

```
推導：<input1> + <input2> + <input3> → <calculation> → <implication>
```

範例（照搬 DS）：

> 2026E TAM base case 落在 **$280B**。
> 推導：hyperscaler capex $600B（GOOG/MSFT/META/AMZN 三年 CAGR 35%）× AI infrastructure 工作負載 35% × 加速器（GPU + ASIC）占 AI infra 比 1.33 → $280B。
> 此 base 假設 hyperscaler capex 兌現度 100%；若兌現 75%（衰退衝擊）→ bear case $230B；若兌現 120%（FOMO 加碼）→ bull case $340B。
> （本節末 `<aside class="ds-refs">` 列出 hyperscaler capex $600B 的 T1 來源）

### 章節覆蓋（硬性）

| 章節 | 必須推導的數字類型 |
|:---|:---|
| **§4（需求 / TAM）** | TAM 三情境、CAGR、demand inflection 年份、三角驗證對帳缺口 |
| **§5（供需裁決 / 推估）** | 三 horizon × 三 case 所有量化 cell；bull/bear 偏離 base 必須由「假設改了什麼」推出；資本週期指標換算；phase 轉換量化閾值 |
| **§7（Priced-in）** | 估值分位、現價隱含成長假設的 reverse 推算 |
| **§8（證偽表）** | kill metric 的閾值換算（如「DC rev YoY +50% 腰斬至 +15%」的基準）|
| **§9（ticker depth 閾值）** | depth label（🔴/🟡/🟢）判定門檻；forward-looking 閾值須註明時間基準 + 當前 actual |

### Anti-pattern

- ❌「我們估 2026E TAM $300B」← 無 input、無推導、節末 aside 無來源。
- ❌「TAM 約 $300B」← 無推導，PM 無法獨立驗證 +20%/-25% 從哪推出。
- ✅「TAM $300B。推導：$600B × 35% × 1.33 → $280-320B base range」+ 節末 aside 列 [T1] 來源。

`pre_publish_check.md` Gate 7（推導 regex）自動掃 §4/§5/§7/§8/§9 是否有「推導：」或等效標記（「→」「換算」「計算」開頭短行），缺一即 fail。

---

## 【§1 歷史錨點規則（DS-9，搬自 DS v1.1）】

### 規則（必須）

§1 中每個 inflection point 段落（通常 2-4 段）必須同時包含：

1. **具體日期或月份**：YYYY 或 YYYY-MM 格式（不允許「過去幾年」「最近」「近期」模糊表述）。
2. **至少一個量化錨點**：價格、性能指標（TFLOPS / GB / 頻寬）、市占、capacity（GW / wafers）、用戶數、營收。

### 範例對比（照搬 DS）

❌ **口語寫法**：「ChatGPT 興起後，NVDA H100 變成稀缺品」
✅ **v2.0 寫法**：「**2022-11-30 ChatGPT 發布**，兩個月內 MAU 衝破 1 億；**2023-03 H100 launch** 時 hyperscaler 已大量採購；**2023-Q3 NVDA DC 營收同比 +279%**，第一次出現 12+ 個月 lead time 配給」（來源在節末 aside 中列出）。

Gate 9（§1 錨點檢查，阻斷）每段正則檢查 `\b(19|20)\d{2}\b` 日期 + 至少一個數字（% / $ / x / GW / TFLOPS / GB / MAU / B / M 等）。違反 → 阻斷發布，返工補錨點。

---

## 【Claim Taxonomy v1（4-class，搬自 ID v1.10，全保留）】

判斷層章節（§0 thesis / §5 裁決 / §7 / §8）強制寫稿者**自己在 inline tag 揭露 claim 性質**，讓 reader / critic 一眼看出這是事實還是推論還是情境預測。

### 4-class（不允許第 5 類）

```
🟢 [F: T1: ...]                                  事實 — 有可驗證 source（T1/T2 + 日期）
🟡 [I: A→B]                                      推論 — 寫明事實鏈與結論連結
🔵 [X: base 很可能 / bull 可能 / bear 不太可能]   情境預測 — 三情境並列，詞彙級機率
⚪ [A: ...]                                      假設 — 顯式承認的 prior
```

**意見類（[O:]）刻意拿掉**：任何 opinion 必須改寫為 [I: A→B] 揭露推論鏈，否則就是 [A:]（顯式假設）。沒有第三條路。

### 機率用詞彙級（不寫精準百分比）

| 詞彙 | 對應機率區間 |
|---|---|
| 幾乎確定 / near-certain | > 90%（限現場已發生 + 1 步衍生）|
| 很可能 / likely | > 60% |
| 可能 / possible | 30-60% |
| 不太可能 / unlikely | < 30% |
| 幾乎不可能 / near-impossible | < 10% |

**禁止**：寫精準百分比（"60% 機率" / "70% chance"），這是 spurious specificity 的高階版（QC-I25 阻擋）。

### Tier-aware enforcement（Q0/Q1/Q2 強度不同，已 remap 至 v2 章節）

| Tier | Tag 強制範圍 |
|:---|:---|
| **Q0 Flagship** | 全文：§0 thesis、§2 forecast、§4 TAM、§3 變動方向、§5-§9 全部判斷層 |
| **Q1 Standard** | §0 thesis、§5 裁決、§7 Non-Consensus + Kill、§8 catalyst + 證偽 |
| **Q2 Quick** | §7 Non-Consensus、§8 證偽表 |

**所有 tier 都強制三段帶 tag**：§0 一句 Thesis、§7 任一 thesis、§8 任一 metric forecast。

### 寫稿時的 inline 標記範例（照搬 ID v1.10）

```
✅ 對：
🔵 [X: base 很可能 — Rubin Ultra 2027 H2 量產（§8 catalyst #3）；
       bull 可能 — 2027 H1 提前（NVDA GTC commentary）；
       bear 不太可能 — 2028 延後（CoWoS 良率惡化超出 §8 證偽 metric #2）]
       → §7 thesis #1 在 base/bull 都成立；bear 情境本 thesis 失效

❌ 錯：
「Rubin Ultra 2027 H2 量產，本 thesis 成立」
（→ 單一情境當必然，缺 base/bull/bear；違反 QC-15）

❌ 錯：
「Rubin Ultra 60% 機率 2027 H2 量產，25% 提前，15% 延後」
（→ 精準機率違反 spurious specificity 禁令；違反 QC-14）

❌ 錯：
「Samsung HBM4 yield 已達 78.3%」
（除非 T1 直接公告該確切值；否則應為 "~75-80%" 或 "~8 成"；違反 QC-14）

✅ 對：
🟡 [I: ASIC TAM CAGR 推論
       事實 1: Hyperscaler capex 2024-2026 三年 CAGR ~35%（GOOG/MSFT/META 法說 [T1]）
       事實 2: 內製 ASIC 占 capex 比重 從 ~15% → ~25%（SemiAnalysis 2026-Q1 [T3-A]）
       → 本 ID 推論：ASIC 細分 CAGR 應在 ~25-35% 區間
       ⚠ 證偽：若 hyperscaler capex 連兩季 < 20% YoY，本推論 invalid]
```

### 🟡 judgment bullet 結構（保留）

判斷層的 🟡 bullet 結構**仍然保留**，[F:]/[I:]/[X:]/[A:] tag 是前綴 inline marker，不取代它：

```
🟡 {推論結論} [信心: 高/中/低]
    事實 1: {可驗證事實 + source}
    事實 2: {可驗證事實 + source}
    → 推論邏輯: {為何從事實 → 結論}
    ⚠ 證偽條件: {什麼發生就推翻這個結論}
```

- 一條 🟡 bullet 通常 = 一個 [I:] tag 包整段推論。
- §8 證偽表每格通常 = 一個 [X:] tag（含 base/bull/bear 三情境閾值）。
- §0 一句 Thesis = 一個 [I:] 或 [X:] tag。
- **所有 🟡 必須有 ⚠ 證偽條件 + [信心: 高/中/低]**；沒寫 = 未完成（QC-9）。信心度 [低] 的 🟡 bullet 不被 stock-analyst 引用為 DD 論點。

### v2.0 ID reader banner（v2 ID 必加）

```html
<div style="background:#EEF2FF;border-left:4px solid #6366F1;padding:10px 14px;margin:12px 0;font-size:12.5px;line-height:1.6">
  <strong style="color:#3730A3">📐 Claim Taxonomy v1（v2.0 敘事版）</strong>：本 ID 在 §0/§5/§7/§8 使用 4 類 inline tag 揭露 claim 性質：
  <strong>[F:]</strong> 事實（有 source）｜
  <strong>[I:]</strong> 推論（A→B 揭露）｜
  <strong>[X:]</strong> 情境預測（base/bull/bear 三情境，詞彙級機率）｜
  <strong>[A:]</strong> 顯式假設。
  數字以 range / ~xxx 呈現（除非 T1 公告精準值）；機率用「很可能 / 可能 / 不太可能」非百分比。來源收在每節末「本節參考來源」區塊。
</div>
```

---

## 【資料來源階層（T1 最高優先，全保留）】

資料來源分 4 級，**Tier 1（公司官方簡報 / 技術 keynote / 10-K / IR deck）為最高優先**，必須先嘗試。低階層只能在高階層找不到時作為補充，且必須標註等級。

### 硬性規則（QC-6）

- 每份 ID 至少要有 **60% 以上數據 claim** 引用自 T1 來源（計算全文所有 aside 的 `[T1]` + `[T1-zh]` 條目占比）。
- §2 S 曲線、§4 TAM、§3 玩家矩陣 **核心數字必須 T1**，否則直接返工。
- 若某主題 T1 全無可得（少見），必須在 §0 TL;DR 下方加黃底警語：「本報告依賴 T2/T3 為主，結論偏觀點」。

### Tier 1（Primary · 一手原始）— 優先搜

| 類別 | 範例 | 搜尋方式 |
|:---|:---|:---|
| 公司投資人簡報（IR deck） | `nvidianews.nvidia.com/events/gtc` / `investor.amd.com` | `{公司} investor day 2026 slides`、`{公司} quarterly presentation Q4` |
| 技術 keynote 簡報 | NVIDIA GTC / Apple WWDC / Intel Tech Tour / TSMC Symposium | `{公司} GTC 2026 Rubin architecture slides`、`{公司} technology roadmap keynote` |
| 財報電話會議逐字稿 | Seeking Alpha transcript、公司官網 IR 頁 | WebFetch 公司 IR 頁或 motleyfool.com/earnings-call-transcripts |
| 10-K / 10-Q / 20-F | SEC EDGAR / TWSE 公開資訊觀測站 / HKEX | WebFetch `sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}` |
| 公司官網技術白皮書 | `nvidia.com/technologies/`、`asml.com/en/technology` | WebFetch 直接抓 HTML |
| 專利庫查詢 | USPTO、EPO、Google Patents | `{technology} patents holder 2025 USPTO` |

### Tier 2（Authoritative Third-party · 權威第三方）

| 類別 | 範例 |
|:---|:---|
| 產業協會 / 研究機構 | SEMI、SIA、Yole Group、IC Insights、TechInsights、IDC、Gartner、IEA、USDA、IFR |
| 學術期刊 / IEEE | IEEE Xplore、Nature Electronics、ACM Digital Library |
| 政府 / 政策文件 | US CHIPS Act filings、EU Chips Act、工研院報告、Fed、ECB、BLS、Eurostat |
| 標準組織 | JEDEC（HBM 規格）、IEEE P1838（3D IC）、OCP |
| 權威財經媒體 | Bloomberg、Reuters、FT、WSJ、Nikkei |

### Tier 3（Analyst / Media · 分析師媒體）— 內部再分三級

**T3-A｜券商產業研究報告**（highest in T3，**優於 T2 部分資料**）：
- 產業深度 Primer / Initiation：Morgan Stanley "AI Infrastructure Primer"、TD Cowen "Advanced Packaging Deep-Dive"、Barclays "Memory Cycle Update"。
- Sector Update / Thematic：Goldman "Pharmaceuticals 2030"、JPM "Semi Capex Outlook"、UBS "EV Battery Chemistry"。
- Channel Check：券商引用實地供應鏈訪談時，數據質量接近 T1。
- **處理原則**：券商「產業報告」優先級與 T2 並列、部分情境高於 T2；券商「個股目標價」維持 T3。引用標 `[T3-A: Morgan Stanley AI Infra Primer 2026-03-15 p.24]`。遇 T3-A vs 公司 T1 IR deck 衝突，IR deck 為準，T3-A commentary 可作反方依據。

**T3-B｜券商個股報告 / 主流財經媒體**：券商個股 PT、Barron's、Forbes、Fortune。

**T3-C｜專業媒體 / Substack 深度**：AnandTech、SemiAnalysis、Tom's Hardware、The Information、SemiWiki、EE Times；付費 Substack（Dylan Patel、Ben Thompson）。署名分析師可信度升至 T3-A 等級。

### Tier 4（Social / Wiki · 社群維基）— 僅作線索

Wikipedia（歷史時間軸，不用於數字）、Reddit / Twitter / Seeking Alpha 評論（僅作 lead）。**禁止作為 data claim 的唯一來源**。

### 券商研究的特殊地位

| 規則 | 說明 |
|:---|:---|
| **優先抓取** | §3/§4 研究時主動搜 `{主題} Morgan Stanley primer` / `{主題} Goldman initiation` / `{主題} Jefferies deep dive` |
| **多券商交叉** | 單一券商結論不可作唯一依據，需 ≥2 家券商支持（或與 T1/T2 交叉）|
| **偏見校準** | 記錄券商 stance（Long / Short / Neutral）；三家都 Long → §7 Non-Consensus 要特別小心 |
| **時效性** | 券商 primer 通常 12-24 個月一次大更新；確認最新版 |
| **頁碼標註** | 引用必須含 `p.XX` 或 slide number |

### 中文來源分類（獨立表）

| 對應 Tier | 來源類別 | 具體名稱 | 使用規則 |
|:---|:---|:---|:---|
| **T1-zh** | 公司中文 IR / 法說材料 | 台積電 / 聯電 / 聯發科 / 日月光 / 光寶官網法說 PDF 或公開資訊觀測站 | 等同 T1，優先使用 |
| **T1-zh** | 公開資訊觀測站年報 / 重訊 | `mops.twse.com.tw` | 等同 T1 |
| **T1-zh** | 台股法說會逐字 / 簡報錄影 | 公司官網 IR 直播、YouTube 官方帳號 | 等同 T1（需寫引用時間戳）|
| **T2-zh** | 政府 / 法人研究機構 | 工研院 IEK / 資策會 MIC / 金工中心 / 國發會 | 等同 T2 |
| **T2-zh** | 專業研究公司 | TrendForce（集邦）、DRAMeXchange、CINNO | 等同 T2，但 TrendForce 半導體預測需與英文 T1 交叉（曾有偏差）|
| **T3-zh** | 半導體專業媒體 | DIGITIMES、電子時報 | 等同 T3，單一來源需交叉驗證 |
| **T3-zh** | 主流財經媒體 | 工商時報、經濟日報、財訊、商周、天下、鉅亨網 | 等同 T3 |
| **T3-zh** | 中文付費 Substack / 產業分析 | 大叔美股筆記、半導體行業觀察、Medium 中文產業專欄 | 等同 T3，署名分析師可升 T2 |
| **T3.5-zh** | 知名 Named-analyst 貼文 | 天風郭明錤、Dan Nystedt、DIGITIMES 謝達志 | 高可信度 T3，仍需交叉驗證 |
| **T4-zh** | 社群 / 論壇 | PTT Stock 板、Mobile01、Facebook 社團 | 僅作 lead，不可作唯一來源 |

**引用規範**：
- 中文來源 aside 條目 tier 加 `-zh` 後綴。
- 中文與英文 T1 衝突時，優先英文 T1（投資人多為英語市場），保留中文觀點作補充。
- 工研院 / TrendForce 預測與英文 T2（Yole / IC Insights）差異 >20% 時，須在 §4 TAM 列兩者並註明差異。

### 衝突處理（QC-7）

兩個 T1 給出不同數字時，必須明確列衝突（照搬 ID）：

```
項目X：A 公司投資人日報 80%（slide 12）[T1]
        B 公司技術大會 60%（slide 4）[T1]
        [衝突] → 差異原因：統計口徑不同（含 / 不含 OEM）
        結論採值：70%（區間中點）或選較保守值
```

禁止「偷偷擇一不說衝突」。

### 常見來源搜尋捷徑

| 主題 | 首選 T1 來源 |
|:---|:---|
| AI 硬體 / GPU | NVIDIA GTC、AMD Advancing AI、Intel Innovation |
| 半導體設備 | ASML Investor Day、AMAT IMEC Symposium、TSMC Technology Symposium |
| 先進封裝 | TSMC OIP、ASE SEMICON、IMEC Future Summit |
| 記憶體 HBM | Micron Investor Day、Samsung Memory Tech Day、SK Hynix 韓國 IR |
| EV / 電池 | Tesla Battery Day、BYD IR、Panasonic Tech Day |
| 生技 / GLP-1 | Novo Nordisk R&D Day、Lilly Investor Day、ACC/ADA 學術年會 |
| 雲端 / SaaS | Microsoft Ignite、Google Cloud Next、AWS re:Invent |
| 航運 / 大宗 | Clarksons、Drewry、Baltic Exchange、LME、Citi/GS commodity desk |

---

## 【Freshness（鮮度）半衰期】

事件型 vs 結構型 thesis 分類（每條判斷層斷言必須隱含分類）：

- **事件型**（引用具體 yield / 訂單 / 簽約 / backlog / earnings 數字）→ **14 天強制 refresh**。
- **結構型**（物理定律 / 產業邏輯 / 歷史類比 / TAM 結構）→ **60 天 refresh**。
- 混合型 → 兩種都跑，以較嚴格者為準。

章節級半衰期（INDEX.md 鮮度欄 + index.html 視覺警示用，沿用 ID 三桶）：

| 章節桶（sections_refreshed key）| 對應章節 | 半衰期 | 超過則標示 |
|:---|:---|:---|:---|
| `technical` | §1 定義 / 歷史 / §2 技術 S 曲線 | **365 天** | 🟡 stale-tech |
| `market` | §3 供給 / §4 TAM / §5 推估 | **90 天** | 🟠 stale-market |
| `judgment` | §6 估值 / §7 Non-Consensus / §8 catalyst+證偽 / §9 ticker | **60 天** | 🔴 stale-judgment |

---

## 【研究流程（四軸，零素材啟動）】

收到主題後執行四軸研究。每軸 3-5 輪 WebSearch，T1 優先；玩家矩陣與利潤池補 2-3 輪 T1。

> **歷史筆記**：v1.11 曾插入 Step 0 Evidence Prefetch（自動撈 EDGAR + IR + arXiv），同日跑 HBM4 ID 驗證失敗 — 自動 fetcher 結構性錯位於 ID 真正需要的 primary source（韓國 IR、付費 SemiAnalysis/Yole、投資人日 deck、法說 Q&A 音訊）。v1.12 移除，v2.0 沿用純 WebSearch / WebFetch 流程。Lesson：別把「自動化好玩」誤當成「自動化有用」。

### Step 0 — Theme 確認 + scope

1. **Theme 是否夠具體**：太籠統（「半導體」）→ 要求縮小（「AI ASIC 設計服務」「DRAM 超循環」）。
2. **檢查同 theme 是否已有 legacy ID / DS**：`ls docs/id/ID_*${theme}*.html docs/ds/DS_*${theme}*.html` → 若有，列入 §0 cross-link callout，本份標 v2 敘事版。
3. **mega + sub_group 分類**：從 `docs/id/taxonomy.md` 白名單選一組。

### Axis A — 歷史（含 cycle 統計，3-5 輪）

- `{theme} history evolution 1990 2000 2010 2020`、`{theme} technology generations`、`{theme} historical analog`
- `{theme} cycle length peak trough amplitude`、`{theme} stock price lead lag fundamentals`（cycle 統計表素材）
- 產出：§1 歷史敘事 + cycle 統計表、§2 S 曲線（優先官方 roadmap）。

### Axis B — 供給（含利潤池、成本曲線、capex pipeline，3-5 輪 + 玩家/利潤池補 2-3 輪 T1）

- `{theme} top suppliers 2026 market share`、`{theme} capex pipeline 2026 2027`、`{theme} capacity utilization`、`{theme} new entrants`
- `{theme} profit pool value chain margin distribution`（利潤池遷移）、`{theme} cost curve marginal producer`（成本曲線）
- **對每家關鍵玩家**：WebFetch IR 頁抓最新簡報 → WebFetch SEC EDGAR 10-K/20-F 查業務組成 → WebSearch earnings transcript 找 commentary。
- 產出：§3 玩家矩陣（T1 source）+ 利潤池表 + 成本曲線 + 未供敘事。

### Axis C — 需求（含 TAM 推導鏈，3-5 輪）

- `{theme} demand drivers 2026 end markets`、`{theme} TAM forecast 2030`、`{theme} customer concentration`、`{theme} demand inflection point`
- 回頭掃 Axis B 抓到的 IR deck 找 TAM 圖。
- 產出：§4 現需敘事 + TAM 三情境推導鏈。

### Axis D — 驗證（新軸，3-5 輪）

- **需求三角對帳**：下游客戶 capex/採購 guidance（`{client} capex guidance 2026`）vs 上游廠商營收 consensus（`{supplier} revenue consensus 2026`）→ 對帳，差 >20% 找缺口。
- **資本週期指標**：`{theme} capex depreciation ratio`、`{theme} industry ROIC WACC`、`{theme} capacity lead time`。
- **sector 估值歷史分位**：`{sector} EV/Sales historical band`、`{sector} forward PE percentile cycle`（§7 priced-in）。
- **庫存/訂單指標**：`{theme} book-to-bill`、`{theme} channel inventory weeks`、`{theme} backlog visibility`（軟體服務類找 NRR/RPO）。
- 產出：§4 三角驗證、§5 資本週期 + 庫存指標、§7 priced-in 分位。

### 寫稿順序

研究完成後：**§0 thesis sketch（一句話 thesis ≤200 字 + id-meta JSON block 草稿）→ §1-§9 依序寫 → §0 定稿（6-box + PM 綠卡，基於 §7/§8/§9 完成的素材）**。

§0 PM 綠卡必須在 §7（Non-Consensus）/ §8（證偽 metric）/ §9（conviction tier）完成後才寫，因為那是把這三章壓縮為「PM 今天能做什麼決定」的橋接段。

---

## 【QC 規則（QC-1 ~ QC-20）】

### QC-1｜🟡 判斷比例 ≤ 20%
全篇 bullet 中 🟡 bullet 數量 / 總 bullet 數量 ≤ 0.20；超過強制返工。

### QC-2｜文字比例 ≥ 55%、表格 ≤ 10 張 / ≤ 8 行
純文字字元（含 bullet 內容）/ 可見字元 ≥ 55%；表格數量 ≤ 10、每張 ≤ 8 行（§9 例外 ≤ 16）。低於 55% 返工，刪表 / 擴敘述。

### QC-3｜數據層斷言必有來源
每個量化斷言所在的 section 末必有 `<aside class="ds-refs">` 對應條目；缺源數字以「—」佔位或改定性，禁止無來源精準值。

### QC-4｜S 曲線必出
§2 S 曲線（ASCII or SVG）為 MUST HAVE；缺則返工。（v1.x 的 value chain SVG 在 v2.0 改為 §3 利潤池語境的 value chain 圖，建議保留但非強制阻斷。）

### QC-5｜🟡 信心度 + 證偽強制
每個判斷層 🟡 bullet 必須有 `[信心: 高/中/低]` + `⚠ 證偽條件`，否則不計入（視為 data claim 需補 source）。無證偽條件的 judgment 視為「信念」而非「分析」，剔除。

### QC-6｜T1 來源優先率 ≥ 60%
全篇所有 aside 條目中 T1 + T1-zh 占比 ≥ 60%。§2 S 曲線、§4 TAM、§3 玩家矩陣核心數字必須 T1，否則返工。T1 全無可得 → §0 下方加警語「本報告以 T2/T3 為主」。

### QC-7｜T1 來源衝突處理
兩個 T1 給出不同數字時必須明確列衝突 + 差異原因 + 採值邏輯（範例見【資料來源階層】衝突處理段）。禁止偷偷擇一不說衝突。

### QC-8｜💡 對投資的意義每章必出
§1-§9 每章結尾強制 💡 box（≥1 段，2-4 句），把該章事實連回投資判斷。純數據陳述、純定義不算。判準：非顯而易見 + 可行動 + 非 tautology。

### QC-9｜證偽條件強制（判斷層）
§5 裁決 / §7 / §8 所有 🟡 judgment bullet 必須附 ⚠ 證偽條件。無證偽條件 = 未完成。

### QC-10｜Non-Consensus 必須可驗證且真非共識（同構合併：原 QC-I12 + DS §8）
§7 的 3 條分歧必須：① 明確引 ≥1 家主流券商/媒體（T3）作「共識」對照；② 本 ID 不同觀點有 §1-§6 事實支撐（不可純主觀）；③ 若「非共識」實際就是 Street 主流 → fail 返工。禁止「本 ID 也認同 X」章節。

### QC-11｜Steel-man 反方必須 3 條（同構合併：原 QC-I8 + DS §9）
§7 必須列 ≥3 條最有力反方論證，每條附具體路徑 + 當前證據 + 證偽窗口。想不出 3 條 = 分析深度不足，返工。

### QC-12｜Catalyst 雙路徑（同構合併：原 §10.5 if-hit/if-miss + DS QC-DS07）
§8 Catalyst Timeline ≥ 5 個具體事件，每個必含：明確日期（季度層級 OK）+ 事件類別 + 檢視指標 + **若達成 / 若落空雙路徑動作**。缺雙路徑 → 補。

### QC-13｜證偽表真 falsification（原 QC-I26 bear sanity）
§8 證偽表 3-5 條 metric + base/bull/bear 三情境閾值。bear 閾值即 thesis 作廢點，必須是真 falsification 不是 strawman；數字用 range。bear sanity check：① bear 觸發點對應至少 1 條 falsification metric？② bear 成真時 §7 該 thesis 真的方向變（不是 conviction 微降）？③ bear 機率沒低於 10%（near-impossible）？低於 = strawman，重列。單一情境（"X 將發生 → thesis 成立"）= fail。

### QC-14｜Spurious Specificity 禁令（原 QC-I25 全保留）
**禁止精準數字**（除非 source 直接公告該確切值）：

| 類別 | ❌ 禁止 | ✅ 允許 |
|:---|:---|:---|
| 市佔（估算）| "62.7%" / "78.3%" | "~70%" / "60-65%" / "~6 成" |
| 預估時間 | "2027-09-15" / "2027 Q3 中旬" | "2027 H2" / "2027 Q3-Q4" |
| 預估 TAM | "$53.7B" | "~$50B" / "$50-60B" |
| 預估良率 | "yield 78.3%" | "~80%" / "yield 7-8 成" |
| 機率 | "60% 機率" / "p=0.6" | 詞彙級「很可能」|
| Multiple | "5.3x EPS" | "~5x" / "4-6x" |

**例外（保留精準）**：T1 source 直接公告（10-K "Q4 revenue $63.2B"）→ 保留 + [F: T1:] tag；過去歷史已實現數字；行業標準規格（"HBM3E 8-Hi stack"、"3nm node"）。判斷原則：**這個精準數字是 source 公告的、還是分析師估算的？** 估的就改 range。

### QC-15｜Claim Taxonomy 標記強制（原 QC-I24）
依 Tier-aware enforcement 表，強制章節 claim 必須有 4 類 tag 之一。§7 每條 thesis ≥1 [F:] + ≥1 [I:]/[X:]；§8 每條 falsification metric ≥1 [X:]；§0 一句 Thesis ≥1 [I:]/[X:]；§8 catalyst 每條 expected 結果 ≥1 [X:]；§7 Kill 每條 ≥1 [I:]。缺 tag = 視為 [O:] 意見類 = fail。

### QC-16｜歷史類比不可空洞 + 反向類比警示（同構合併：原 QC-I14 + QC-I21）
§1 歷史類比引 2-3 個具體前例（年份 + 主角 + 當年關鍵數據），指出當年多頭/空頭錯在哪 + 本次的**量化差異**（不是「這次不一樣」空話）。引先例時須列先例所有關鍵條件並逐條對照本次；多條件不成立 → 標「反向類比警示」避免錯誤歸因。

### QC-17｜SOM / 玩家矩陣禁推估值（原 QC-I17）
玩家矩陣不得用「Q × 4」推估，只引實際公告。最新季已公告 → 四季加總；僅一季 → 註明「年化推估，actual 待 FY 公告」。

### QC-18｜利潤池 / 議價權百分比必 source 或降定性（原 QC-I19）
§3 利潤池、議價權的所有百分比必標 source；無 source → 改定性（「主導 / 均勢 / 次要」）。

### QC-19｜ASP / 成本單位 glossary（原 QC-I20）
報告開頭（§0 前後）列 unit glossary：ASP 單位（$/wafer vs $/stack vs $/GB vs $/unit）、Revenue 口徑（全年 vs 季度 vs annualized run-rate）、營收 scope（segment / AI-only / total company）。不統一 → 返工。

### QC-20｜事件型 thesis 14 天 refresh + 策略結盟 90 天查（同構合併：原 QC-I22 + QC-I18）
判斷層標為事件型的 thesis，其引用的具體事件（yield / 訂單 / 簽約 / backlog）必須在發布日前 14 天內重新檢索；最新資料矛盾 → 降信心或重寫。非股價類 corporate action（持股變動、共同開發協議、併購、SEC 8-K）查最近 90 天狀態。

---

### 新模組對應 QC（6 條，QC-M1 ~ QC-M6）

### QC-M1｜裁決必引資本週期證據至少 2 項
§5 供需裁決（過剩/平衡/短缺）必須引資本週期三指標（capex/折舊比、ROIC vs WACC、新產能 lead time）中**至少 2 項**作量化依據，不能只靠敘事推理。缺 → 返工補。

### QC-M2｜TAM 必有三角對帳，差 >20% 必解釋
§4 TAM 必須有 top-down vs bottom-up 三角驗證。**兩邊差 >20% 必須解釋缺口在哪**（重複計算 / 樂觀滲透率 / 口徑不同）並寫明採信哪邊。只給 top-down 數字 = fail。

### QC-M3｜每個分歧必附 priced-in
§7 每條 non-consensus 分歧必須對照「市場已 price 多少」（sector 估值歷史分位 + 現價隱含成長假設）。分歧對但已 priced → 標「不可操作」。缺 priced-in = fail。

### QC-M4｜成本曲線省略必註明理由
§3 成本曲線：週期性 / 大宗型產業強制；結構成長型可省，**但必須在 §3 一句註明省略理由**（如「設計服務無實體產能成本曲線」）。週期性產業缺成本曲線且無理由 = 返工。

### QC-M5｜cycle 統計表 ≥2 輪歷史時強制
§1 歷史 cycle 統計表：產業有 ≥2 輪可統計的完整 cycle 時強制。無明顯 cycle 的單向結構成長產業可省，**須在 §1 註明「本產業尚無可統計的完整 cycle」**。

### QC-M6｜庫存指標產業適用性判定
§5 庫存/訂單週期指標：有實體庫存 / 訂單可見度的產業強制（book-to-bill / channel inventory weeks / backlog）；軟體服務/平台類無實體庫存 → 改用 NRR / backlog / RPO / billings 等對應領先指標，**須在章內說明用了哪個替代指標及理由**。完全略過 leading indicator = 返工。

---

## 【Pre-Publish Gate（10 道）】

寫好 ID HTML 草稿後，讀取 `pre_publish_check.md` 逐條跑（細節在該檔，這裡列清單）：

| Gate | 性質 | 檢查 |
|:---|:---|:---|
| **Gate 1** | 阻斷 | 核心 ticker financials < 60 天 |
| **Gate 2** | 阻斷 | Event-triggered thesis < 14 天 refresh |
| **Gate 2.1** | 阻斷 | Thesis Cornerstone Fact Verification — 「獨家 / 首家 / 唯一」類 claim 必須獨立 WebSearch 驗證 ecosystem 玩家（避免 Eaton 獨家 800V DC 類錯誤）|
| **Gate 3** | 阻斷 | Cross-ID reconciliation（共用 ticker / 事實一致）|
| **Gate 4** | 阻斷 | id-meta JSON validation — `python3 scripts/validate_id_meta.py docs/id/ID_X.html` 必須 exit 0（CI strict gate 連坐）|
| **Gate 5** | 阻斷 | §0 PM Implication 綠卡存在 + 五 bullet + 四行動 + conviction 與 §9 🔴 數量 / §6 de-rating 一致 |
| **Gate 6** | 阻斷 | 文字比 ≥ 55%（搬自 DS Gate 11；inline Python 計算可見字元比）|
| **Gate 7** | 阻斷 | 推導鏈 regex — §4/§5/§7/§8/§9 結論數字必有「推導：」或等效標記（搬自 DS Gate 13）|
| **Gate 8** | 阻斷 | aside 來源 — 每個含量化斷言的 section 末必有 `<aside class="ds-refs">` 且 ≥1 條；全文 aside T1+T1-zh 占比 ≥ 60%（搬自 DS Gate 12，T1 門檻取 ID 嚴值 60%）|
| **Gate 9** | 阻斷 | §1 錨點 — §1 每個 inflection 段含具體日期 + 量化錨點（搬自 DS Gate；正則 `\b(19|20)\d{2}\b` + 數字）|
| **Gate 10** | warning | 供需裁決明確（§5 過剩/平衡/短缺三選一）+ §9 ticker depth 時間限定 + Catalyst 雙路徑齊備 |

任一阻斷 Gate (1/2/2.1/3/4/5/6/7/8/9) fail → 阻斷發布 + 列修正項。阻斷全過、warning Gate (10) fail → 允許發布但輸出 warning。輸出 `pre_publish_report.md` 記 pass/fail 明細。

---

## 【Step 8.7 — Mandatory Critic Gate】

寫好 ID HTML 草稿後（暫存 staging path），**必須**呼叫 `id-review` skill（`--mode id`）做 cold review，找出 conclusion-changing 大錯。

**為什麼加**：Pre-Publish Gate 都是「機械正確性」（id-meta valid、cornerstone fact 14d 內、來源不在黑名單）— 抓不到「推理錯誤 / thesis 與外部現實不符」。Step 8.7 引入跨模型（Sonnet）冷讀者抓真正的 thesis-level 大錯。

**呼叫方式**（v2 報告由 id-review 讀 id-meta `skill_version` ≥ v2.0 自動判別、切換 v2 checklist）：

```
Agent({
  description: "Pre-publish critic gate on {Theme}",
  subagent_type: "general-purpose",
  model: "sonnet",  // 必須 Sonnet — 與寫稿者（Opus）跨模型，避免 echo chamber
  prompt: """
You are operating as the id-review sub-agent.
Read spec at /Users/ivanchang/.claude/skills/id-review/SKILL.md.
The skill auto-detects v2 from id-meta skill_version >= v2.0 and applies the v2 checklist.

ID file path: {staging path}
User's intent: 「pre-publish gate check — 即將 publish，找出 conclusion-changing 大錯」

Run the cornerstone checks + v2-specific checks (表格比 / 因果閉合 / 供需裁決 /
三情境 / 雙路徑 / 推導抽查 / 三角對帳數字可回溯 / 資本週期證據真實引用 / priced-in 分位有來源).
Save report to /tmp/_prepub_critic_{Theme}_{date}.md.

Return brief summary with COUNTS by tier:
- 🔴 CHANGES_CONCLUSION: N
- 🟡 PARTIAL_IMPACT: M
- 🟢 COSMETIC: K
Highest priority issues (top 3 by CONCLUSION_IMPACT).
"""
})
```

對 Q0 Flagship ID 必須再跑 Pass 2（focused 大錯掃描）。

**Gate 判定**：

| Quality Tier | 0 🔴 | ≥1 🔴 |
|---|---|---|
| **Q0 Flagship** | ✅ Pass | 🔴 **BLOCKING** — 必須先在本 skill 內修，重跑 critic 直到 0 🔴 才放行發布 |
| **Q1 Standard** | ✅ Pass | ⚠ **WARNING** — 給 user 看 critic findings，user 選 ship 或 fix |
| **Q2 Quick** | ✅ Pass | ⚠ **WARNING** |

**WARNING 模式 user 選 fix** → 進 id-review patch 流程，改完重跑 Step 8.7 → 發布。**BLOCKING 模式** → 回到 §5/§7/§8/§9 修正，重跑 Pre-Publish Gate + Step 8.7（只跑 Pass 1），仍有 🔴 重複最多 3 輪；3 輪未過 → 告訴 user「critic 持續找到大錯，建議重新研究」。

---

## 【id-meta JSON Schema（原樣保留，schema 不准動）】

> **v2.0 相容說明**：id-meta JSON schema **一個欄位都不加 / 不改**（`validate_id_meta.py` 會 reject unknown key）。`skill_version: "v2.0"` 即新格式標記（validator 只 regex 驗 vN.N，免改）。`sections_refreshed` 沿用 `technical / market / judgment` 三桶，v2 章節 mapping：**technical → §1-§2、market → §3-§5、judgment → §6-§9**。`related_tickers[]` / taxonomy（mega + sub_group）/ oneliner 規則全部不變 → stock-analyst、DCA、earnings-synthesis 零感知。

每份 ID HTML 的 `<head>` 內必含 `<script id="id-meta" type="application/json">{...}</script>`，在 `<title>` 之後、第一個 `<style>` 之前，與既有 `<meta name="id-*">` tags 並存。這是下游消費者（stock-analyst §9 自動引用、CI validator、未來 sector index）的 SSOT。**漏寫 → CI `Validate DD + ID metadata` workflow strict gate fail，整 push 連坐被擋**。

**必填欄位**：

| 欄位 | 型別 | 說明 |
|:---|:---|:---|
| `theme` | string | 產業主題（e.g. `"AI EDA + IP"`、`"HBM 供需循環"`）|
| `skill_version` | string | 建立時 skill 版本（v2 報告填 `"v2.0"`）|
| `id_version` | string | 此 ID 自身版本（`"v1.0"` 初版）|
| `publish_date` | string | `"YYYY-MM-DD"` |
| `thesis_type` | enum | `"structural"` / `"event-triggered"` / `"mixed"` |
| `ai_exposure` | enum | `"🟢"` 直接受益 / `"🟡"` 部分受益 / `"🔴"` 中性或受害 |
| `oneliner` | string | ≤ 200 chars，核心 thesis 一句話 |
| `related_tickers` | array | 關聯個股；每項 `{ticker, role, depth, beneficiary}` |

**選填欄位**（不強制）：

| 欄位 | 型別 | 說明 |
|:---|:---|:---|
| `tam_usd_2030` | number | 2030 TAM in billion USD |
| `cagr_pct_5y` | number | 5Y CAGR % |
| `growth_phase` | enum | `"early"` / `"mid"` / `"late"` / `"declining"` |
| `value_chain_position` | enum | `"upstream"` / `"midstream"` / `"downstream"` / `"cross-tier"` |
| `industry_structure` | enum | `"monopoly"` / `"duopoly"` / `"oligopoly"` / `"fragmented"` |
| `sections_refreshed` | object | `{"technical": "YYYY-MM-DD", "market": "YYYY-MM-DD", "judgment": "YYYY-MM-DD"}` |
| `sister_ids` | array | 兄弟 ID HTML 檔名列表 |
| `quality_tier` | enum | `"Q0"` Flagship / `"Q1"` Standard / `"Q2"` Quick（影響 Claim Taxonomy enforcement 與 Step 8.7 blocking 強度）|
| `mega` | enum | 15 大類白名單（`docs/id/taxonomy.md`）— validator 選填但**本 skill 流程必填**（Step 0 分類 + index.html 卡片插入依賴它）|
| `sub_group` | enum | 對應 mega 的子群白名單（同 taxonomy.md）— 同上，**本 skill 流程必填** |

> #### 🚫 **嚴禁複合 enum 值 / 自創字串 / 加修飾詞**（CI strict gate 阻斷）
>
> Validator 嚴格匹配 enum 字串集合。**禁止以下實際發生過的錯誤**：
>
> | ❌ 違規寫法 | ✅ 正確寫法 | 說明 |
> |:---|:---|:---|
> | `"thesis_type": "structural+event"` | `"mixed"` | 用 `mixed` 表達雙重屬性，不要 `+` 拼接 |
> | `"growth_phase": "mature_diverging"` | `"late"` | mature 對應 `late`；diverging 是敘事細節 |
> | `"growth_phase": "structural_supercycle_expansion"` | `"mid"` 或 `"early"` | 自創長字串映射到四選一 |
> | `"growth_phase": "consolidation"` | `"late"` | consolidation 屬 mature 後期 |
> | `"value_chain_position": "concentrate-to-shelf"` | `"cross-tier"` | 跨多段一律 `cross-tier` |
> | `"value_chain_position": "upstream_commodity"` | `"upstream"` | 不要加修飾詞 |
> | `"value_chain_position": "intermediation"` | `"cross-tier"` | 中介性質 = 跨上下游 |
> | `"industry_structure": "oligopoly+disruption"` | `"oligopoly"` | disruption 是動態描述 |
> | `"industry_structure": "regional_oligopoly"` | `"oligopoly"` | 地區性質寫進 oneliner |
>
> **規則**：metadata 是給 validator + 下游 parser 讀的「分類標籤」，不是給人讀的「敘事描述」。複雜二元性、地區屬性、disruption 動態都寫進章節內文，metadata 只保留 enum 主分類。
>
> #### 🚫 **`oneliner` 嚴格 ≤ 200 chars**（含中英文混合）
>
> Validator hard cap 200 字元。實際發生過 308 / 468 / 483 / 614 字元 violation。**正確做法**：① oneliner 只放 3-5 個關鍵數字錨點 + 1 個結論動詞；② 詳細論述留給 §0 thesis / §7 章節；③ 寫完用 `len(d['oneliner'])` 自測，> 180 立刻精簡（留 20 char buffer 應付下游 emoji / 全形字元計算差異）。
>
> 範例（180 chars 內）：「銅 2026 預期 \$11K–13K（Citi \$13K / GS \$10.7K / MS 600kt deficit「20 年最嚴」）；三引擎共振：AI DC + Grid + EV；Anglo-Teck \$53B + Codelco \$40B 響應。」

#### `related_tickers` 物件 schema

```json
{
  "ticker": "AVGO",
  "role": "AI ASIC 設計 + 網通 silicon photonics",
  "depth": "🔴",
  "beneficiary": true
}
```

- `depth`: 🔴 核心受益 / 🟡 中度 / 🟢 輕度。
- `beneficiary`: `true` 受益 / `false` 受害。

#### 範例（AI EDA + IP，v2.0）

```html
<script id="id-meta" type="application/json">
{
  "theme": "AI EDA + IP",
  "skill_version": "v2.0",
  "id_version": "v1.0",
  "publish_date": "2026-06-11",
  "thesis_type": "structural",
  "ai_exposure": "🟢",
  "oneliner": "AI 晶片設計爆發推動 EDA + IP 需求結構性向上，SNPS/CDNS 雙寡占受益顯著，AI-native EDA tooling 為下一個複利層。",
  "related_tickers": [
    {"ticker": "SNPS", "role": "EDA 雙寡占 + ARC IP", "depth": "🔴", "beneficiary": true},
    {"ticker": "CDNS", "role": "EDA 雙寡占 + Tensilica IP", "depth": "🔴", "beneficiary": true},
    {"ticker": "ARM", "role": "CPU IP 通用授權", "depth": "🟡", "beneficiary": true}
  ],
  "tam_usd_2030": 25.0,
  "cagr_pct_5y": 14.5,
  "growth_phase": "mid",
  "value_chain_position": "upstream",
  "industry_structure": "duopoly",
  "quality_tier": "Q1",
  "mega": "semi",
  "sub_group": "eda_ip",
  "sections_refreshed": {"technical": "2026-06-11", "market": "2026-06-11", "judgment": "2026-06-11"}
}
</script>
```

#### 寫完後自我驗證（不可省略）

Write 完 ID HTML 後**立即執行**（在 terminal 摘要之前）：

```bash
python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{YYYYMMDD}.html
```

- exit 0 → 繼續輸出 terminal 摘要。
- exit != 0 → 讀錯誤訊息，用 Edit 修 id-meta JSON，重跑直到 exit 0。**不允許帶錯誤推 commit**（CI strict gate 會擋）。

**為什麼需要 id-meta**：避免下游反向 parse HTML（每次 template 改寫就崩）。stock-analyst skill §9 可直接從 `related_tickers` array 自動 join 公司 DD ↔ 產業 ID。

---

## 【發布流程（Step 9）】

寫好 + 過 Pre-Publish Gate + 過 Step 8.7 critic 後：

1. **寫 HTML**：`docs/id/ID_{Theme_CamelCase}_{YYYYMMDD}.html`，`<head>` 必含 id-meta JSON。
2. **本地驗證**：`python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{YYYYMMDD}.html`（exit 0 才能 commit）。
3. **append INDEX.md** 一行（欄位規格見下）。
4. **insert index.html 卡片**：找對應的 `<!-- subgroup-anchor: {mega}.{sub_group} -->`，插入新 article 卡片；**卡片加 `v2 敘事版` badge pill**（舊卡片不動）。
5. **跑分類頁**：`python3 scripts/build_id_category_pages.py`（整塊複製 index.html category block，badge 自動帶過去，不需改 script）。
6. **重生 DD↔ID 對應 / banner**（若腳本存在）：`python3 scripts/id_dd_mapping.py`、`python3 scripts/retrofit_dd_id_banner.py`。
7. **Tier Matrix 健康度**：`python3 scripts/check_tier_matrix.py --inject-html` — 掃新 ticker（≥2 份 ID signal）、注入健康度 banner。若返回「🆕 N 檔新 ticker」必須在回 user 訊息中提示是否評估加入 Tier Matrix。
8. `git add + commit + push`（同 commit 涵蓋 ID 新增 + alert 更新）。

### INDEX.md 欄位（沿用 ID v1.13）

每份 ID append 一行：

```
| YYYY-MM-DD | 主題 | 涵蓋 ticker 數 | 核心 🔴 / 次要 🟡 / 邊緣 🟢 | 投資時鐘 Phase | 🟡 比例 | 鮮度 | 檔名 | 備註 |
```

**鮮度欄位格式**：`tech:YYYY-MM-DD 🟢 ｜ market:YYYY-MM-DD 🟢 ｜ judgment:YYYY-MM-DD 🟢`
- 🟢 在半衰期內；🟡 超 tech；🟠 超 market；🔴 超 judgment。

範例：
```
| 2026-04-19 | 玻璃基板封裝 | 11 | 3🔴/5🟡/3🟢 | Phase I (CAPEX 爆發) | 17% | tech:2026-04-19 🟢 ｜ market:2026-04-19 🟢 ｜ judgment:2026-04-19 🟢 | ID_GlassSubstrate_20260419.html | 首篇；LIDE / TGV 良率為核心卡點 |
```

### Terminal 摘要格式（沿用 ID v1.13）

```
✅ 產業深度報告完成：{主題}
📄 檔案：docs/id/ID_XXX.html
📊 涵蓋 {N} 檔 ticker（🔴{a} / 🟡{b} / 🟢{c}）
🧠 🟡 判斷比例：{X}%（上限 20%）｜文字比：{Y}%（下限 55%）
⏱ 研究輪數：WebSearch ×{n}，WebFetch ×{m}
🔗 首頁同步：[✅/❌] ｜ 供需裁決：{過剩/平衡/短缺}
🔗 已追蹤的 DD：{list} ｜ 待建議 DD：{list}
```

---

## 【HTML 視覺規格】

沿用紫色主視覺（住在 `/id/`），💡 implication box 用 DS 綠：

- 頁首 badge：`產業深度 · Industry Deep Report`（紫色 #7C3AED）+ `v2 敘事版` pill。
- 章節標題左邊加 accent 直線（紫色）。
- 判斷層章節（§5 裁決 / §7 / §8）頂部加 🟡 banner：「本章含 judgment，已標信心度」。
- 每個 🟡 bullet 用卡片樣式（淡黃底 #FEF9C3 + border-left #EAB308）。
- **💡 對投資的意義 box 用 DS 綠**（背景 #F0FDF4 / border-left #16A34A）。
- **§0 PM Implication 綠卡**用 DS 綠（同上）。
- **`ds-refs` aside CSS 搬入**（每節末來源區塊；`.ds-refs` / `.ds-refs-label` / `.tier` / `.source-warning` 全套，見 templates）。
- 🔴 核心 / 🟡 次要 / 🟢 邊緣 tier 用 pill 標籤。
- **S 曲線強制保留**：優先 `<pre>` ASCII（IBM Plex Mono）；複雜情境改 inline SVG。
- **Value chain SVG 改為利潤池語境**：水平 3-box layout（上游 / 中游 / 下游）+ 箭頭，box 內標利潤池占比（不只毛利率）+ 遷移方向箭頭。
- Claim Taxonomy reader banner（v2 ID 必加，見【Claim Taxonomy】段）。

**頁尾固定**：`產業深度報告 · industry-analyst v2.0（敘事版）· 主題：{theme} · 發布日：{date} · 🟡 占比：{pct}% · 文字比：{ratio}%`

---

## 【整合點：stock-analyst 讀取 ID（不變）】

stock-analyst 執行 DD 時，在護城河 / 競爭格局 / 產業演進章節前先：

```
1. 讀 docs/id/INDEX.md
2. 用 sector / theme 比對當前 ticker
3. 命中 → 讀該 ID 的 §9 找本 ticker 影響深度 + §1/§3/§4 產業背景
4. 公司 DD：產業背景引用 ID_XXX（一句話 + <a href>）+ 本公司差異化 3-5 條量化 bullet；不重複產業通論
5. 未命中 → 照原流程，HTML 頁尾提示「未發現相關產業 DD，建議建立 ID_XXX」
```

下游消費者一律讀 id-meta `related_tickers` array，無需手動維護。

---

## 【啟動觸發】

使用者提到下列任一語意時觸發本 skill：

**ID（dashboard / 研究）觸發語**：
- 「研究 XXX 產業」/「sector 分析」/「industry landscape」/「產業報告」/「產業藍圖」
- 「玻璃基板 / CoWoS / HBM / 先進封裝 / GLP-1 / AI ASIC / EUV / 核融合」等具體主題，且**未帶股票 ticker 的量化分析要求**。
- portfolio 決策時說「這個主題」「這個產業」而非「這檔股票」。

**DS（敘事 / 供需循環）觸發語（v2.0 吸收）**：
- 「{主題} ds」/「ds {主題}」
- 「{產業} 敘述報告」/「discourse {industry}」
- 「分析 {產業} 的供需循環」
- 「{產業} 歷史與未來」/「{產業} 短中長期推估」
- 「寫一份 {產業} 的 DS 報告」

**不觸發**（走其他 skill）：
- 「{ticker} DD」/「{ticker} 深度分析」→ stock-analyst
- 「{ticker} dca」/「{ticker} 定見」→ deep-conviction-analyst
- 純政策事件追蹤 → geopolitics

若同時要求「先做產業 + 再做這檔」，先跑 industry-analyst，再跑 stock-analyst（後者自動讀新產出的 ID）。

---

## 【與 ID / DD / DCA 的關係】

| Layer | Skill | Output | 適用情境 |
|:---|:---|:---|:---|
| 產業層（敘事為骨表格為窗） | **industry-analyst v2.0** | docs/id/ID_*.html | 歷史 / 供需循環 / 玩家矩陣 / 估值傳導 / 證偽 — 單一深度報告 |
| 產業層（互動供應鏈圖） | supply-chain-cartographer | docs/supply-chain/{topic}.html | 節點圖視角看製程脆弱依賴點 |
| 公司層（深度） | stock-analyst | docs/dd/DD_*.html | 單檔護城河 / 估值 / 訊號燈 |
| 公司層（決策） | deep-conviction-analyst | docs/dca/DCA_*.html | 單檔買賣定見、PM 行動 |

`industry-ds` 已 deprecated，併入本 skill。

---

## 【版本歷史】

- **v2.1（2026-06-11，pilot 反饋當日修訂）**：用戶對首發 pilot（AIComputeCapexCycle）的兩條反饋落規格：① **深度上修** — 全文 target 8-12K → **16,000-22,000 可見字**（<14K 視為偷懶），各章字數約 ×2，新增「深度擴展規則」八槓桿（機制敘事 / 類比完整敘事 / 資金流圖譜 / 🔴 個體敘事 / kill 完整 steel-man / bear 情境敘事化 / 二階效應 / 編年史段落），擴展靠文字不靠表格；② **結論先行** — §0 第一個內容塊強制 3-6 句純白話結論段（裁決 + 核心非共識 + 真風險 + 行動），禁止用卡片/pill 替代、禁止埋伏筆。另：QC-6 T1 60% 對 macro/aggregate 主題的例外條款待補（pilot 學習，見 memory）。
- **v2.0（2026-06-11）**：**合併 industry-ds（DS）→ 單一「敘事為骨、表格為窗」產業深度報告**。① 全新章節骨架：§0 決策層 + 三幕共 9 章（§0 決策摘要 / §1 白話定義+歷史 / §2 技術 S 曲線 / §3 供給+利潤池 / §4 需求+三角驗證 / §5 供需裁決+推估+投資時鐘 / §6 估值傳導 / §7 Non-Consensus+priced-in+kill / §8 catalyst+證偽 / §9 ticker）— 取代舊 14 章 ID schema 與 DS 11 章 schema。② 吸收 DS 全部：因果敘事弧、§1 雙錨點（DS-9）、因果閉合（DS-2）、推導鏈、§末 aside 來源系統、敘事/條列 hybrid、每章 💡、可讀性規則層（文字 ≥55%、lede、每表三句話、術語白話）。③ 新增 7 個分析模組：歷史 cycle 統計（§1）、利潤池遷移（§3）、成本曲線（§3）、需求三角驗證（§4）、資本週期證據（§5）、庫存訂單指標（§5）、priced-in 檢驗（§7）。④ 研究流程改四軸（歷史 / 供給 / 需求 / 驗證），每軸 3-5 輪。⑤ QC 重編號 QC-1~20 + QC-M1~M6（同構合併：證偽 / 雙路徑 / non-consensus / steel-man 各一條；砍只服務舊結構的 QC-I15 各章最低表格數；新增 6 條對應新模組）。⑥ Pre-Publish 10 gates（保留 ID Gate 1/2/2.1/3 + id-meta validate；併入 DS 文字比 / aside 來源 / 推導 regex / §1 錨點）。⑦ id-meta schema **零改動**（skill_version "v2.0" 為新格式標記；sections_refreshed 沿用三桶，technical→§1-2 / market→§3-5 / judgment→§6-9）。⑧ Step 8.7 critic 改呼叫 id-review（v2 由 skill_version 自動判別）。⑨ 吸收 DS 觸發語（「{主題} ds」「敘述報告」「供需循環」「discourse」）。⑩ HTML 保留紫色主視覺 + S 曲線強制；💡 / PM 綠卡用 DS 綠；value chain SVG 改利潤池語境。既有 105 ID + 8 DS 凍結為 legacy，不 retrofit、不遷移；industry-ds deprecated 觸發語自動轉向。
- **v1.13（2026-05-03）**：frontmatter 版本與日期更新（body 規則同 v1.12）。
- **v1.12（2026-05-02，post-HBM4 validation）**：revert v1.11 evidence pool hooks。同日跑「2026-2027 HBM4 供需循環」ID 端到端驗證，發現自動 fetcher 拿到的（EDGAR press release ≈ WebFetch 已能讀；arXiv paper 多為 PIM tangential；IR archive 1994-2020 噪音 ~800 個）跟 ID 真正需要的（SK Hynix / Samsung Korean IR primary、付費 SemiAnalysis / Yole 報告、投資人日 deck PDF、法說會 Q&A 音訊）結構性錯位。本次 revert 移除 Step 0 / Step 2/3/6 的 evidence read hook、引用規範裡 `[evidence:]` tag 段落 — 回到純 WebSearch / WebFetch 流程。保留：`scripts/evidence/` dead code、`SEMI_EVIDENCE_SPEC.md`（標 DEPRECATED）、`get_whisper_model.sh`。Lesson：別把「自動化好玩」誤當成「自動化有用」。
- **v1.11（2026-05-02，已 revert，見 v1.12）**：新增 Step 0 — Evidence Prefetch（呼叫 `scripts/evidence/orchestrator.py`）+ Step 2/3/6 evidence-read hook + `[evidence:]` citation tag。源於 `SEMI_EVIDENCE_SPEC.md` 設計：補強 ID primary-source 比例。同日驗證失敗，v1.12 移除。
- **v1.10（2026-05-01）**：Claim Taxonomy v1（4-class [F:]/[I:]/[X:]/[A:]）+ 詞彙級機率 + tier-aware enforcement。新增 QC-I24（taxonomy 標記強制）、QC-I25（spurious specificity 禁令）、QC-I26（多情境強制：base/bull/bear，bear 必須對應 §13 真 trigger 不是 strawman）。v1.0-v1.9 共存策略：機會主義升級（不主動 batch retrofit 80 份）。v1.10 ID 必加 reader banner。
- **v1.0（2026-04-19）**：初版。11 章 schema；🟡 規則；QC-I1-I6；stock-analyst 整合鉤子。

> **註**：v1.1-v1.9 的增量規則（六大原則強化、事件型/結構型分類、Gate 2.1 cornerstone、§0.7 PM Implication、id-meta JSON、差別 stale、Reference Card 等）已逐步併入 v1.10-v1.13 主文並由 v2.0 繼承重編號。v2.0 之前歷史完整快照見 git log。
