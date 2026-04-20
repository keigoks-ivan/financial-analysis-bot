---
name: industry-analyst
description: 建立「產業深度報告（Industry DD / ID）」— 一份跨多檔個股共用的產業研究文件。輸入產業主題（如「玻璃基板封裝」「HBM 供需循環」「GLP-1 治療藍圖」），skill 執行 WebSearch / WebFetch 多輪研究，輸出一份 11 章節、表格為主 + 敘述為輔、含 S 曲線與 value chain 圖示的 HTML 報告；並把對應個股登記於 §11 關聯清單，供 stock-analyst（公司 DD）自動讀取引用。觸發：使用者提到「產業研究 / sector DD / 產業報告 / industry landscape / 產業藍圖」或具體主題（玻璃基板、HBM、CoWoS、AI ASIC、GLP-1、核融合、玻璃纖維基板等）且尚未要求做個股 DD。
version: v1.0
date: 2026-04-19
---

# industry-analyst skill v1.0

## 【六大原則（v1.4 事件/結構 thesis 分類）】

1. **完整 AND 洞見**：本 skill 追求**兩者同時達成**，不是 trade-off。每章先寫完整到「讀者讀完能當教科書用」，再在最後提煉 💡 Insight（市場沒看到的角度）。完整度 × 洞見 = 這份 ID 的價值。
2. **Insight-first（最後一哩）**：每章的終點是 💡 Insight Bullet，不是數據清單。但 insight 必須建立在完整數據之上 — 若章節內容太薄，insight 會變主觀意見。
3. **Data-first, judgment-tagged**：§0-§7 為數據層，T1 優先；§8-§13 為判斷層，🟡 judgment 必須附證偽條件。
4. **Tables-heavy, narrative-supported**：每章以表格為主幹，敘述用於連接、強調與轉折（敘述 < 30% 章節內容）。
5. **跨 DD 槓桿**：一份 ID 被 5-10 檔公司 DD 共享，產業背景只寫一次；公司 DD 只寫差異化。
6. **事件型 vs 結構型 thesis 分類（v1.4 新增）**：每條 §12 thesis 必須標 `[event-triggered]` 或 `[structural]`。
   - 事件型（引用具體 yield / 訂單 / 簽約 / backlog 絕對值）→ **14 天強制 refresh**（QC-I22）
   - 結構型（物理定律 / 產業邏輯 / 歷史類比）→ 60 天 refresh
   - 混合型 → 兩種週期都跑，以較嚴格者為準
   - **八份 2026-04-19 ID peer review 累積教訓**：事件型 thesis 的 data refresh 不及時是 C/D 級 ID 的根因（HBM Samsung HBM4 時序、LEN Samsung yield 70% 都屬此類）

### 「完整 + 洞見」怎麼同時做到？

每章分**兩層**：

```
┌─────────────────────────────────────────────┐
│ 第 1 層：完整層（Depth）                      │
│ - 2-4 張表格（覆蓋該主題所有重要角度）         │
│ - 每個子主題至少 3-5 個 data point            │
│ - 敘述段落解釋數據的 context                  │
│ - 每個數字附 source（T1 優先）                 │
│                                              │
│ ➜ 目標：讀完這章可獨立寫報告                  │
├─────────────────────────────────────────────┤
│ 第 2 層：洞見層（Insight）                    │
│ - 💡 2-3 條 Insight Bullet（非顯而易見）       │
│ - 引用第 1 層的具體事實 → 導出結論            │
│ - 對投資的具體意義                            │
│                                              │
│ ➜ 目標：讀者 take away 3 個可行動結論         │
└─────────────────────────────────────────────┘
```

**兩層缺一不可**：
- 只有完整層 → 教科書 / 剪報，無分析師附加價值（QC-I10 fail）
- 只有洞見層 → 觀點文章，缺事實支撐，信度不足（QC-I15 fail）

---

## 【路徑】

```
~/.claude/skills/industry-analyst/
  SKILL.md                         # 本檔
  templates/
    html_template.md               # HTML 視覺 & 樣式規範
    schema_fields.md               # 11 章節必填 / 選填欄位
    scurve_ascii.md                # S 曲線 ASCII 樣板
    value_chain_svg.md             # value chain inline SVG 樣板
```

輸出：

```
financial-analysis-bot/
  docs/id/
    INDEX.md                       # 產業 DD 索引
    index.html                     # 產業列表首頁
    ID_{Theme}_{YYYYMMDD}.html     # 單份產業報告
```

---

## 【14 章節 Schema（v1.1 Insight-first 定版）】

| § | 標題 | 類型 | 核心輸出（標★為 insight-forcing 欄位）|
|:---|:---|:---|:---|
| §0 | TL;DR 卡片 | 數據 | 主題 / 時長 / 規模 / 關鍵玩家 3 / 關鍵風險 3 / 今日 Phase + ★**一句 Thesis（本 ID 最核心的非共識觀點）**|
| §1 | 產業定義與邊界 | 數據 | in-scope vs out-of-scope 表 + ★**灰色地帶**（邊界爭議本身常是 insight 來源）|
| §2 | 技術演進 + S 曲線 + **歷史類比** | 數據 | S 曲線 + 過去→現在→未來 + ★**2-3 個歷史類比**（前例轉折：誰被錯估、本次異同）|
| §3 | 核心技術棧拆解 | 數據 | 子技術 × 良率卡點 × 專利持有者；★**哪個子技術成為 kingmaker**|
| §4 | 市場規模 + CAGR | 數據 | TAM / SAM / SOM + ★**過去 3 次 TAM forecast 實際偏差**（多數 TAM 被高估）|
| §5 | 供應鏈 value chain | 數據 | 上→中→下 SVG + 毛利 + ★**議價權近 5 年轉移史**（利潤池正在往哪段集中）|
| §6 | 玩家矩陣 | 數據 | 設備 / 材料 / 製程 / 封測 / 設計 5 類 × ticker × 市佔 + ★**近 12 個月市佔變動方向**|
| §7 | Unit Economics + **ASP 動態** | 數據 | 產業平均 ROIC / Gross / Capex cycle + ★**ASP 過去 5Y + 未來 2Y + 抗 commoditization 分析**|
| §8 | 估值影響機制 | 判斷（🟡） | 產業變數 → 公司 Fwd PE/PEG 傳導表 + ★**敏感度：+1pp 毛利 ⇒ ? 倍數擴張**|
| §9 | 風險矩陣 + **政策地緣子表** | 判斷（🟡） | 技術 / 需求 / 替代 3 軸 + 政策地緣獨立列（關鍵立法 / 制裁時程）+ ★**市場最低估的風險**|
| **§9.5** | **Kill Scenario / Steel-man 反方** | 判斷（🟡） | ★**3 條最有力反方論證**，每條附：具體路徑 + 當前證據 + 成真時間窗；若分析師想不出 3 條 → 返工|
| §10 | 投資時鐘 + **Phase 轉換訊號** | 判斷（🟡） | 當前 Phase 判定 + 各 phase 贏家切換 + ★**I→II / II→III 必要+充分條件表**|
| **§10.5** | **Catalyst Timeline** | 數據+判斷 | ★**未來 18 個月日期表**：事件 × 檢視指標 × 若達成 / 若落空的動作|
| §11 | 關聯個股清單 | 數據 | ticker × 深度 🔴🟡🟢 × 受益 / 受害 × DD 連結 + ★**1-2 檔 non-obvious 二次受益者**|
| **§11.5** | **Cross-ID 依賴圖** | 數據 | ★上游依賴（誰廢它連鎖反應）+ 下游受益（本 ID 成立帶動誰）+ 兄弟 ID|
| **§12** | **Non-Consensus View（共識差異）** | 判斷（🟡） | ★**3 條本 ID vs 市場共識的具體分歧**：共識說什麼 / 本 ID 看法 / 分歧原因；本章是 insight 核心|
| **§13** | **Falsification Test（證偽條件）** | 數據 | ★**3-5 條具體 metric + 閾值**：若達該值，本 ID thesis 作廢；為 PM 層提供停損觸發條件|

### §0-§7（數據層）硬性規則

- 每個 claim 必須 `[source: URL or T1/T2/T3 標籤 + 頁碼/slide 編號]`
- 未驗證數字一律以「—」佔位，禁止填入無來源值
- 表格優先，敘述用於解釋 context（敘述 < 30% 章節內容）

### 完整度（Depth）最低門檻（QC-I15）

每個數據章節必須達到下列最低深度，否則返工：

| 章節 | 最低表格數 | 最低 data point | 最低敘述段落 |
|:---|:---|:---|:---|
| §1 定義與邊界 | 2（in-scope + out-of-scope）| 各 ≥ 5 項 | 2 段（為何這樣切） |
| §2 技術演進 + 歷史類比 | 3（過去/現在/未來表 + S 曲線資料 + 歷史類比）| 時間點 ≥ 5、類比 ≥ 2 | 3 段 |
| §3 技術棧拆解 | 2-3（子技術 × 瓶頸 × 專利）| 子技術 ≥ 5、瓶頸 ≥ 3 | 3 段（每個關鍵子技術一段）|
| §4 市場規模 | 2（TAM/SAM/SOM + 預估偏差）| 各年 ≥ 3 層 | 2 段（CAGR 假設、預估可信度） |
| §5 Value chain | 1 SVG + 2 表（毛利 + 議價權）| 每段 ≥ 3 玩家 | 3 段（上/中/下利潤邏輯） |
| §6 玩家矩陣 | 3-4（5 類分開列）| 每類 ≥ 3 公司 | 2 段（市佔變動、在位者 vs 挑戰者） |
| §7 Unit Economics + ASP | 2（ROIC/Gross + ASP 趨勢）| ≥ 5Y 歷史 + 2Y 預估 | 2 段 |

### 洞見層（Insight）強制（QC-I10）

**每章結尾強制 2-3 條 💡 Insight Bullet**，格式：
```
💡 {一句非顯而易見的結論}
    事實基礎：引用本章 §X 表 Y 的數據
    推論邏輯：為何從事實 → 結論
    投資意義：對 ticker / 進場時機 / 估值的具體含義
```
沒寫 = QC-I10 fail。純數據陳述不算 insight。

### §8-§13（判斷層）🟡 規則（v1.1 加強）

- 🟡 judgment bullet 必須結構化為：
  ```
  🟡 {推論結論} [信心: 高/中/低]
      事實 1: {可驗證事實 + source}
      事實 2: {可驗證事實 + source}
      → 推論邏輯: {為何從事實 → 結論}
      ⚠ 證偽條件: {什麼發生就推翻這個結論}
  ```
- 整篇 🟡 bullet 比例上限 20%（QC-I1）
- 信心度 [低] 的 🟡 bullet 不被 stock-analyst 引用為 DD 論點
- **所有 🟡 必須有證偽條件**（QC-I11）；沒寫 = 未完成

---

## 【資料來源階層（v1.1 強化，T1 最高優先）】

資料來源**分 4 級**，**Tier 1（公司官方簡報 / 技術 keynote / 10-K / IR deck）為最高優先**，必須先嘗試。低階層只能在高階層找不到時作為補充，且必須標註等級。

### 硬性規則（QC-I7）
- 每個產業 ID 至少要有 **60% 以上數據 claim** 引用自 T1 來源（2026-04-19 從 50% 提高至 60%）
- §2 S 曲線、§4 TAM、§6 玩家矩陣 **核心數字必須 T1**，否則直接返工
- 若某主題 T1 全無可得（少見），必須在 §0 TL;DR 下方加黃底警語：「本報告依賴 T2/T3 為主，結論偏觀點」

### Tier 1（Primary · 一手原始）— 優先搜

| 類別 | 範例 | 搜尋方式 |
|:---|:---|:---|
| 公司投資人簡報（IR deck） | `nvidianews.nvidia.com/events/gtc` / `investor.amd.com` | WebSearch：`{公司} investor day 2026 slides`、`{公司} quarterly presentation Q4` |
| 技術 keynote 簡報 | NVIDIA GTC / Apple WWDC / Intel Tech Tour / TSMC Symposium | WebSearch：`{公司} GTC 2026 Rubin architecture slides`、`{公司} technology roadmap keynote` |
| 財報電話會議逐字稿 | Seeking Alpha transcript、公司官網 IR 頁 | WebFetch 公司 IR 頁或 motleyfool.com/earnings-call-transcripts |
| 10-K / 10-Q / 20-F | SEC EDGAR（美股）/ TWSE 公開資訊觀測站（台股）/ HKEX | WebFetch `sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}` |
| 公司官網技術白皮書 | `nvidia.com/technologies/`、`asml.com/en/technology` | WebFetch 直接抓 HTML |
| 專利庫查詢 | USPTO、EPO、Google Patents | WebSearch：`{technology} patents holder 2025 USPTO` |

### Tier 2（Authoritative Third-party · 權威第三方）

| 類別 | 範例 |
|:---|:---|
| 產業協會 / 研究機構報告 | SEMI、SIA、Yole Group、IC Insights、TechInsights、IDC、Gartner |
| 學術期刊 / IEEE | IEEE Xplore、Nature Electronics、ACM Digital Library |
| 政府 / 政策文件 | US CHIPS Act filings、EU Chips Act、工研院報告 |
| 標準組織 | JEDEC（HBM 規格）、IEEE P1838（3D IC）、OCP |

### Tier 3（Analyst / Media · 分析師媒體）— 內部再分三級

**T3 內部優先序（由高至低）**：

#### T3-A｜券商產業研究報告（highest priority in T3，**優於 T2 部分資料**）
- **產業深度 Primer / Initiation Report**：Morgan Stanley "AI Infrastructure Primer"、TD Cowen "Advanced Packaging Deep-Dive"、Barclays "Memory Cycle Update"
- **Sector Update / Thematic Report**：Goldman "Pharmaceuticals 2030"、JPM "Semi Capex Outlook"、UBS "EV Battery Chemistry"
- **Channel Check Reports**：當券商報告引用實地訪談供應鏈，數據質量接近 T1
- **處理原則**：
  - 券商「產業報告」(primer / sector) 優先級 **與 T2 並列**，甚至部分情境高於 T2
  - 券商「個股目標價」(target price / PO update) 維持 T3
  - 引用時標 `[T3-A: Morgan Stanley AI Infra Primer 2026-03-15 p.24]`
  - 遇 T3-A vs 公司 T1 IR deck 衝突時，IR deck 為準，但 T3-A 的 commentary 可作為反方依據

#### T3-B｜券商個股報告 / 主流財經媒體
- 券商個股 target price update（Goldman / Morgan Stanley / Jefferies 個股 PT）
- Bloomberg / Reuters / WSJ / FT 深度報導
- Barron's、Forbes、Fortune

#### T3-C｜專業媒體 / Substack 深度分析
- AnandTech、SemiAnalysis、Tom's Hardware、The Information
- SemiWiki、EE Times、Hackernews 深度討論
- 付費 Substack：SemiAnalysis（Dylan Patel）、Stratechery（Ben Thompson）、大叔美股筆記
- 處理原則：署名分析師（e.g., Dylan Patel、Ben Thompson）可信度升至 T3-A 等級

### Tier 4（Social / Wiki · 社群維基）— 僅作線索

- Wikipedia（可用於歷史事件時間軸，不用於數字）
- Reddit / Twitter / Seeking Alpha 評論（僅作 lead 發現）
- 禁止作為 data claim 的唯一來源

### 券商研究在本 skill 的特殊地位

券商產業研究報告（T3-A）是 industry DD 的**關鍵差異化來源**，處理上比其他 T3 更嚴謹：

| 規則 | 說明 |
|:---|:---|
| **優先抓取策略** | Step 3 市場與供應鏈研究時，除了 Yole / IC Insights，應主動搜 `{主題} Morgan Stanley primer site:morganstanley.com` / `{主題} Goldman initiation report` / `{主題} Jefferies deep dive` |
| **多券商交叉** | 單一券商結論不可作為唯一依據，需至少 **2 家券商**支持（或與 T1/T2 交叉） |
| **偏見校準** | 記錄券商 stance（Long / Short / Neutral）；若三家券商都是 Long，§12 Non-Consensus 章要特別小心 |
| **時效性** | 券商 primer 通常 12-24 個月為一次大更新；需看是否為最新版 |
| **頁碼標註** | 引用必須含 `p.XX` 或 slide number，便於日後回溯 |

---

### 中文來源分類（獨立表）

中文來源在台股 / 大中華區半導體鏈是剛需，但品質參差極大，獨立為下表，對應到 T1-T4：

| 對應 Tier | 來源類別 | 具體名稱 | 使用規則 |
|:---|:---|:---|:---|
| **T1-zh** | 公司中文 IR / 法說材料 | 台積電 / 聯電 / 聯發科 / 日月光 / 光寶等**官網法說 PDF** 或 **公開資訊觀測站**檔案 | 等同 T1，優先使用 |
| **T1-zh** | 公開資訊觀測站年報 / 重訊 | `mops.twse.com.tw` | 等同 T1 |
| **T1-zh** | 台股法說會逐字 / 簡報錄影 | 公司官網 IR 直播、YouTube 官方帳號 | 等同 T1（需寫引用時間戳）|
| **T2-zh** | 政府 / 法人研究機構 | 工研院 IEK / 資策會 MIC / 金工中心 / 國發會 | 等同 T2 |
| **T2-zh** | 專業研究公司 | TrendForce（集邦）、DRAMeXchange、MIC 產業情報、CINNO | 等同 T2，但 TrendForce 半導體預測需與英文 T1 交叉驗證（曾有偏差） |
| **T3-zh** | 半導體專業媒體 | DIGITIMES、電子時報 | 等同 T3，單一來源需交叉驗證 |
| **T3-zh** | 主流財經媒體 | 工商時報、經濟日報、財訊、商周、天下、鉅亨網 | 等同 T3 |
| **T3-zh** | 中文付費 Substack / 產業分析 | 大叔美股筆記、半導體行業觀察（微信公眾號）、Medium 中文產業專欄 | 等同 T3，但署名分析師可信度可升 T2 |
| **T3.5-zh** | 知名 Named-analyst 貼文 | 天風證券郭明錤（Ming-Chi Kuo Twitter）、Dan Nystedt、DIGITIMES 謝達志 | 高可信度 T3，但仍需交叉驗證 |
| **T4-zh** | 社群 / 論壇 | PTT Stock 板、Mobile01、Facebook 社團 | 僅作 lead，不可作唯一來源 |

**引用規範**：
- 中文來源引用時標籤加 `-zh` 後綴：`[T1-zh: <a href="...">台積電 2026Q1 法說會 slide 14</a>]`
- 中文與英文 T1 衝突時，**優先英文 T1**（因投資人多為英語市場），但保留中文觀點作為補充
- 工研院 / TrendForce 預測與英文 T2（Yole / IC Insights）差異 > 20% 時，須在 §4 TAM 列兩者並註明差異

---

### 引用規範

每個 claim 後必須附來源標籤：

```html
<span class="source-tag">[T1: <a href="https://nvidianews.nvidia.com/.../gtc-2026-keynote">NVIDIA GTC 2026 Keynote slide 47</a>]</span>
<span class="source-tag">[T2: <a href="https://www.semi.org/report-xxx">SEMI 2025 Advanced Packaging Report</a>]</span>
<span class="source-tag">[T3: <a href="https://www.semianalysis.com/p/xxx">SemiAnalysis 2026-03 Rubin deep-dive</a>]</span>
```

**規則**：
- 同一事實能同時被 T1 + T2 驗證 → 只標較高 tier
- 僅 T3/T4 單一來源 → 在章節末加 ⚠️ 註：「此事實僅 T3 來源，無 T1/T2 交叉驗證」
- T1 投資人簡報的頁碼 / slide 編號必須寫出來（方便日後回溯）

### 常見來源搜尋捷徑

| 主題 | 首選 T1 來源 |
|:---|:---|
| AI 硬體 / GPU | NVIDIA GTC keynote、AMD Advancing AI Event、Intel Innovation |
| 半導體設備 | ASML Investor Day、AMAT IMEC Technology Symposium、TSMC Technology Symposium、Applied Materials SEMICON West |
| 先進封裝 | TSMC OIP、ASE SEMICON、IMEC Future Summit、LPKF Photonics |
| 記憶體 HBM | Micron Investor Day、Samsung Memory Tech Day、SK Hynix 韓國 IR |
| EV / 電池 | Tesla Battery Day、BYD IR、Panasonic Tech Day |
| 生技 / GLP-1 | Novo Nordisk R&D Day、Lilly Investor Day、ACC/ADA 學術年會 |
| 雲端 / SaaS | Microsoft Ignite、Google Cloud Next、AWS re:Invent |

---

## 【研究管線（零素材啟動）】

收到主題後按此順序執行，每步產出中間結果（不中斷）：

### Step 1 — 主題界定（2 輪 WebSearch）
- Search 1：`{主題} technology overview 2026` → 技術輪廓
- Search 2：`{主題} market size forecast` → 規模錨點
- 產出：§0 TL;DR 卡片 + §1 邊界表的草稿

### Step 2 — 技術深挖（3-5 輪，優先抓 T1 簡報）
- **先試**：`{主流玩家} investor day 2026 slides filetype:pdf` / `{玩家} technology keynote deck`
- 若主題是半導體：`{公司} GTC 2026 keynote`、`{公司} technology symposium 2026`、`TSMC OIP 2026`
- 若主題是生技：`{公司} R&D day presentation`、`ADA 2026 abstract {藥物}`
- 若主題提到特定技術（如 LIDE、TGV、HBM4E）→ 針對性 search 該技術 IEEE 論文 + 設備商網站
- **WebFetch 抓 T1 簡報**：取關鍵 slide 標題、數據、路線圖
- 產出：§2 S 曲線（優先用官方 roadmap）、§3 技術棧矩陣（引用 slide 編號）

### Step 3 — 市場與供應鏈（3-5 輪）
- `{主題} market size TAM 2030 SEMI report` / `Yole {主題}` / `IC Insights {主題}`
- 回頭掃 Step 2 抓到的 IR deck 找 TAM 圖
- `{主題} supply chain value chain`
- `{主題} margin structure`
- 產出：§4 TAM/SAM/SOM、§5 value chain SVG、§7 unit economics

### Step 4 — 玩家 landscape（4-8 輪，T1 為主）
- `{主題} equipment suppliers market share`
- `{主題} material suppliers`
- `{主題} top public companies exposure`
- **對每家關鍵玩家**：
  1. WebFetch 公司 IR 頁抓最新投資人簡報
  2. WebFetch SEC EDGAR 10-K / 20-F 查業務組成
  3. WebSearch 最近 earnings transcript 找 commentary
- 產出：§6 玩家矩陣（每欄必附 T1 source link）

### Step 5 — 判斷層（基於前 4 步的累積事實）
- §8：產業變數（如良率 / CAPEX / ASP）→ 公司 Fwd PE 的傳導表 + 敏感度
- §9：3 軸風險矩陣 + 政策地緣子表
- **§9.5 Kill Scenario**：強制列 3 條反方論證（QC-I8）。問自己：
  - 「如果 3 年後證明這個 thesis 錯了，最可能的錯誤路徑是哪個？」
  - 「誰在 short 這個產業？他們看到什麼我沒看到？」
  - 「最近 3 個月哪些 data point 不符合本 thesis？」
- §10：當前 Phase + 贏家切換 + **Phase 轉換訊號表**（必要 + 充分條件）
- **§10.5 Catalyst Timeline**：未來 18 個月 ≥ 5 個具體日期事件（QC-I13）
- 所有 🟡 bullet 必須標事實鍊 + **證偽條件**（QC-I11）

### Step 6 — §11 關聯個股清單 + §11.5 Cross-ID
- 從 §6 玩家矩陣抓出「有公開股票 + 本產業曝險 > 10% revenue」的公司
- 對每檔：評定影響深度
  - 🔴 核心：營收 >40% 依賴此產業 OR 技術領導者
  - 🟡 次要：營收 10-40%，重要但非主導
  - 🟢 邊緣：營收 <10% 但被市場連動
- **強制找 1-2 檔 non-obvious 二次受益者**（e.g., 本產業需某設備 → 該設備的乾燥爐供應商）
- 若 `docs/dd/INDEX.md` 已有該 ticker 的 DD → 附連結；否則標「DD 未建，建議後續追加」
- §11.5 Cross-ID：列本 ID 的上游依賴 / 下游受益 / 兄弟 ID（若存在 docs/id/INDEX.md 對應條目，附連結）

### Step 7 — Insight Synthesis（§12 + §13，本 skill 的靈魂）
前 6 步是 data gathering；本步是**從 data 提煉 insight**。
- **§12 Non-Consensus View**：寫 3 條本 ID 與市場共識的具體分歧
  - 對每條：先列共識觀點（引 1 家主流券商 / 媒體 T3）→ 再列本 ID 看法 → 指出分歧的**事實基礎**
  - 禁止「本 ID 也認同 X」的章節（= 沒有 insight，QC-I12 fail）
  - 問自己：「如果這 3 條只是複述共識，我這份 ID 的價值是什麼？」
- **§13 Falsification Test**：寫 3-5 條「若達到此 metric，thesis 作廢」
  - 每條必須是**可量化的 metric + 具體閾值 + 時間窗**
  - 範例（不是）：「如果 AI 需求放緩，thesis 錯」 ❌
  - 範例（是）：「NVIDIA 單季 DC revenue YoY < +15% 連續 2 季（閾值從 +50% 腰斬）」✅
- **每章回頭補 💡 Insight Bullet**（QC-I10）

### Step 8 — QC 檢核（QC-I1 ~ QC-I23）
- 跑 QC-I1 ~ QC-I14（下述）
- 未過直接返工，不落稿
- 特別檢查：§12 Non-Consensus 是否真的非共識、§9.5 反方是否夠硬、§10.5 Catalyst 日期是否具體

### Step 8.5 — Pre-Publish Gate Check（v1.4 新增，阻斷式）

讀取 `pre_publish_check.md` 的 7 條 Gate，逐條跑阻斷檢查：
- Gate 1 核心 ticker financials < 60 天
- Gate 2 Event-triggered thesis < 14 天
- Gate 3 Cross-ID reconciliation（共用 ticker / 事實一致）
- Gate 4 Catalyst & Falsification 狀態標示
- Gate 5 Unit & scope consistency
- Gate 6 Cross-ID layer disambiguation（switch vs chip-level）
- Gate 7 Sub-topic ID value-add rule（子題 vs 母題）

任一必備 Gate (1/2/3) fail → 阻斷發布 + 列修正項；必備 Gate 全過、重要 Gate (4-7) 有 fail → 允許發布但輸出 warning。輸出 `pre_publish_report.md` 記錄 pass/fail 明細。

### Step 9 — 產出 HTML + INDEX
- 寫入 `docs/id/ID_{Theme_CamelCase}_{YYYYMMDD}.html`
- append `docs/id/INDEX.md` 一行
- 更新 `docs/id/index.html` 列表
- 若 `docs/research/index.html` 有「產業深度」tab，更新 markers
- `git add + commit + push`（依 MEMORY feedback）

---

## 【QC-I 規則（14 條，v1.1 Insight-first）】

### QC-I1｜🟡 判斷比例 ≤ 20%
全篇 bullet 中 🟡 bullet 數量 / 總 bullet 數量 ≤ 0.20；超過強制返工。

### QC-I2｜§0-§7 禁止無來源數字
數據層每個數字必須 `[source: ...]`；缺源以「—」或移到 §8-§10 並轉 🟡。

### QC-I3｜§11 必須追蹤既有 DD
對 §11 每檔 ticker 查 `docs/dd/INDEX.md`；已有 DD 必須附連結。

### QC-I4｜S 曲線 + value chain 必出
§2 S 曲線（ASCII or SVG）與 §5 value chain SVG 為 MUST HAVE；缺任一返工。

### QC-I5｜🟡 信心度強制分級
每個 🟡 bullet 必須有 `[信心: 高/中/低]`，否則不計入（視為 data claim，需補 source）。

### QC-I6｜時效性
所有數據 source 優先選擇 < 12 個月；超過 3 年的資料必須標「(hist)」。

### QC-I7｜T1 來源優先率 ≥ 50%
全篇所有帶 source 的 claim 中，T1（公司官方簡報 / 技術 keynote / 10-K / IR deck / 官網白皮書）占比 **≥ 50%**。§2 S 曲線、§4 TAM、§6 玩家矩陣三章的核心數字必須為 T1，否則返工。若 T1 完全不可得，需在 §0 下方加警語「本報告以 T2/T3 為主」。

### QC-I8｜Steel-man 反方必須 3 條
§9.5 必須列出至少 3 條「最有力的反方論證」，每條附具體路徑 + 當前證據 + 成真時間窗。若分析師只能想出 < 3 條，代表分析深度不足，返工。

### QC-I9｜T1 來源衝突處理
兩個 T1 給出不同數字時（e.g., 不同公司年報 / 不同 keynote），必須明確列衝突：
```
項目X：A 公司投資人日報 80%（slide 12）[T1]
        B 公司技術大會 60%（slide 4）[T1]
        [衝突] → 差異原因：統計口徑不同（含 / 不含 OEM）
        結論採值：70%（區間中點）或選較保守值
```
禁止「偷偷擇一不說衝突」。

### QC-I10｜💡 Insight Bullet 每章必出
§0-§13 每一章結尾強制 2-3 條 💡 Insight Bullet。純數據陳述、純定義、純 TAM 數字等不算 insight。Insight 的判準：
- 是否為「非顯而易見」（讀者讀完 T1 還是需要 analyst 點出來的結論）
- 是否為「可行動」（對投資決策有指向）
- 是否為「非 tautology」（不是換句話重寫數據）

### QC-I11｜證偽條件強制
§8-§13 所有 🟡 judgment bullet 必須附 `⚠ 證偽條件`。無證偽條件的 judgment 視為「信念」而非「分析」，剔除。

### QC-I12｜Non-Consensus View 必須可驗證
§12 的 3 條分歧必須：
- 明確引用至少 1 家主流券商 / 共識媒體（T3）的觀點作為「共識」對照
- 本 ID 的不同觀點必須有 §2-§11 某處的事實支撐（不可純主觀）
- 若 §12 的「非共識」實際上就是共識（e.g., 也是 Street 主流觀點），本章 QC fail，返工

### QC-I13｜Catalyst Timeline 必須含日期
§10.5 Catalyst Timeline 至少 5 個具體事件，每個必須有：
- 明確日期（季度層級 OK，「未來某天」不行）
- 事件類別（財報 / 法說 / keynote / 政策 / 產品上市）
- 檢視指標（看什麼數字確認 thesis 走在軌道上）
- 若達成 / 若落空的對應動作

### QC-I14｜歷史類比不可空洞
§2 歷史類比章節必須引 2-3 個**具體前例**（年份 + 主角 + 當年關鍵數據），並指出：
- 當年多頭錯在哪、空頭錯在哪
- 本次與前例的**量化差異**（不是「這次不一樣」這種空話）

### QC-I17｜SOM 表禁推估值（v1.4 新增，八份 peer review 教訓）
SOM / 玩家矩陣不得使用「Q × 4」或類似推估，只引實際公告數字。若最新季已公告 → 用四季加總；若僅有一季公告 → 註明「年化推估，actual 待 FY 公告」。違反 → 返工。

### QC-I18｜策略結盟 / M&A 狀態 90 天查（v1.4 新增）
非股價類 corporate action（持股變動、共同開發協議、併購、SEC 8-K）必須查最近 90 天狀態。發布日前 90 天內有更新 → 必須反映（例：AMAT 對 BESI 已持股 9%，非「併購傳聞」）。

### QC-I19｜利潤池 / 議價權百分比必 source 或降定性（v1.4 新增）
§5 value chain、議價權轉移表的所有百分比（「NVDA 45% / TSMC 30%」）必須標 source；無 source → 改為定性描述（「主導 / 均勢 / 次要」）。

### QC-I20｜ASP / 成本單位 glossary（v1.4 新增）
報告開頭（§0 TL;DR 前後）必須列 unit glossary：
- ASP 單位：$/wafer vs $/stack vs $/GB vs $/unit
- Revenue 口徑：全年 vs 季度 vs annualized run-rate
- 營收 scope：segment / AI-only / total company
不統一 → 返工。

### QC-I21｜歷史類比反向類比警示（v1.4 新增）
§2 歷史類比引用先例時（如「Samsung 2026 重演 2018 TSMC 7nm 超車」），必須列出先例的**所有關鍵條件**並逐條對照本次。若多條件不成立 → 標「反向類比警示」避免錯誤歸因。

### QC-I22｜Event-triggered thesis 14 天 refresh（v1.4 新增）
§12 標為 `[event-triggered]` 的 thesis，其引用的具體事件（yield / 訂單 / 簽約 / backlog）必須在發布日前 14 天內重新檢索。若最新資料矛盾 → 降信心級別或 thesis 重寫。

### QC-I23｜Reference Card 跨 ID 共享（v1.4 新增）
關鍵跨 ID 事實（Rubin Ultra stack、AVGO AI 營收口徑、Intel Foundry 客戶狀態、TSMC 節點 roadmap、ticker 評級）必須存於 `references/*.md` 共享檔；ID 引用時必須 link 回該檔，不得重寫。Fact 更新時只改 reference card，所有引用 ID 自動受惠。

---

### QC-I16｜差別 stale 機制（v1.3 新增，2026-04-19）

ID 不同章節的半衰期不同，必須分開判斷：

| 章節 | 半衰期 | 超過則標示 |
|:---|:---|:---|
| §2 技術演進 / §1 定義 / §3 技術棧 | **365 天** | 🟡 stale-tech |
| §4 TAM / §6 玩家矩陣 / §10.5 Catalyst / §5 Value chain | **90 天** | 🟠 stale-market |
| §8 估值 / §9 風險 / §9.5 Kill / §10 投資時鐘 / §12 Non-Consensus / §13 Falsification | **60 天** | 🔴 stale-judgment |

**實作要求**：
- 每份 ID HTML 必須有 `<meta name="id-publish-date" content="YYYY-MM-DD">`（現行規定）
- 每份 ID 增加 `<meta name="id-sections-refreshed" content='{"technical":"YYYY-MM-DD","market":"YYYY-MM-DD","judgment":"YYYY-MM-DD"}'>`（新增）
- `docs/id/INDEX.md` 每行加「🆕 最新段刷新日」欄；超半衰期的層級以 🟡🟠🔴 標示
- `docs/id/index.html` 首頁列表對超半衰期的 ID 加視覺警示（邊框變色）

**使用者觸發更新**：
- 「更新 ID_XX 的 §4 TAM」→ 只重跑該章節，更新 market-refreshed
- 「更新 ID_XX 全部」→ 全面重跑，所有 refresh 日期一致
- 跑 stock-analyst 時若命中的 ID 已有 stale-judgment 段 → DD 頁尾提示「引用的 ID 判斷層已過期，請考慮刷新」

---

### QC-I15｜完整度最低門檻
每個數據章節（§1-§7, §11）必須達到「完整度最低門檻」表中的表格數、data point、敘述段落門檻，否則章節視為「薄」，返工補齊：
- §1：2 表、各 ≥ 5 項、2 段敘述
- §2：3 表（含 S 曲線 + 歷史類比）、時間點 ≥ 5 + 類比 ≥ 2
- §3：2-3 表、子技術 ≥ 5 + 瓶頸 ≥ 3
- §4：2 表、各年 ≥ 3 層
- §5：1 SVG + 2 表、每段 ≥ 3 玩家
- §6：3-4 表（5 類分列）、每類 ≥ 3 公司
- §7：2 表、≥ 5Y 歷史
- §11：ticker ≥ 8 + 1-2 檔 non-obvious

**目標判準**：讀完數據層章節，讀者能用該內容當「教科書 / 入門資料」獨立寫 pitch；洞見層另外額外提供「分析師視角」。兩者都必須達標。

---

## 【整合點：stock-analyst 讀取 ID】

stock-analyst skill 執行 DD 時，應在**護城河分析 / 競爭格局 / 產業演進**章節前先執行：

```
1. 讀 docs/id/INDEX.md
2. 用 sector / theme 欄位比對當前 ticker
3. 命中 → 讀該 ID 的 §11 找本 ticker 的影響深度 + §2/§3/§5 產業背景
4. 公司 DD 的 §9 §10 §11 改為：
   - 產業背景：引用 ID_XXX（一句話）+ <a href> 連結
   - 本公司差異化：3-5 條量化 bullet（市佔 / 專利數 / 良率差距）
   - 不重複寫產業通論
5. 未命中 → 照 v12 原流程寫，但在 HTML 頁尾提示「未發現相關產業 DD，建議後續建立 ID_XXX」
```

具體修改位置：stock-analyst SKILL.md 執行管線第 2-3 步之間插入 `ID lookup`。

---

## 【INDEX.md 欄位】

每份 ID append 一行：

```
| YYYY-MM-DD | 主題 | 涵蓋 ticker 數 | 核心 🔴 / 次要 🟡 / 邊緣 🟢 | 投資時鐘 Phase | 🟡 比例 | 鮮度 | 檔名 | 備註 |

**鮮度欄位格式**：`tech:YYYY-MM-DD 🟢` / `market:YYYY-MM-DD 🟡` / `judgment:YYYY-MM-DD 🟢`
- 🟢 在半衰期內；🟡 超出 tech 半衰期；🟠 超出 market；🔴 超出 judgment
- 例：`tech:2026-04-19 🟢 ｜ market:2026-04-19 🟢 ｜ judgment:2026-04-19 🟢`（首發時全綠）
```

範例：
```
| 2026-04-19 | 玻璃基板封裝 | 11 | 3🔴/5🟡/3🟢 | Phase I (CAPEX 爆發) | 17% | ID_GlassSubstrate_20260419.html | 首篇；LIDE / TGV 良率為核心卡點 |
```

---

## 【HTML 視覺規格】

沿用 DD v12 設計語言但區分：
- 頁首 badge：`產業深度 · Industry DD` （紫色 #7C3AED）vs DD 的藍色 #1E3A5F
- 章節標題左邊加 accent 直線（紫色）
- 判斷層（§8-§10）頂部加 🟡 banner：「本章含 judgment，已標信心度」
- 每個 🟡 bullet 用卡片樣式（淡黃底 #FEF9C3 + 左邊 border-left #EAB308）
- 🔴 核心 / 🟡 次要 / 🟢 邊緣 tier 用 pill 標籤
- S 曲線優先 `<pre>` ASCII（font: IBM Plex Mono）；複雜情境改 inline SVG
- Value chain 統一 inline SVG，水平 3-box layout（上游 / 中游 / 下游）+ 箭頭

**頁尾固定**：`產業深度報告 · industry-analyst v1.0 · 主題：{theme} · 發布日：{date} · 🟡 占比：{pct}%`

---

## 【Terminal 摘要格式】

HTML 生成後輸出：

```
✅ 產業 DD 完成：{主題}
📄 檔案：docs/id/ID_XXX.html
📊 涵蓋 {N} 檔 ticker（🔴{a} / 🟡{b} / 🟢{c}）
🧠 🟡 判斷比例：{X}%（上限 20%）
⏱ 研究輪數：WebSearch ×{n}，WebFetch ×{m}
🔗 首頁同步：[✅/❌]
🔗 已追蹤的 DD：{list of existing DD} ｜ 待建議 DD：{list of missing}
```

---

## 【啟動觸發】

使用者提到下列任一語意時觸發本 skill：
- 「研究 XXX 產業」/「sector 分析」/「industry landscape」
- 「玻璃基板 / CoWoS / HBM / 先進封裝 / GLP-1 / AI ASIC / EUV / 核融合」等具體主題，且**未帶股票 ticker 的量化分析要求**
- 使用者在做 portfolio 決策時說「這個主題」「這個產業」而非「這檔股票」

若同時要求「先做產業 + 再做這檔」，先跑 industry-analyst，再跑 stock-analyst（後者會自動讀新產出的 ID）。

---

## 【版本歷史】

- **v1.0（2026-04-19）**：初版。11 章 schema；🟡 規則；QC-I1-I6；stock-analyst 整合鉤子。
