---
name: industry-analyst
description: 建立「產業深度報告（Industry DD / ID）」— 一份跨多檔個股共用的產業研究文件。輸入產業主題（如「玻璃基板封裝」「HBM 供需循環」「GLP-1 治療藍圖」），skill 執行 WebSearch / WebFetch 多輪研究，輸出一份 11 章節、表格為主 + 敘述為輔、含 S 曲線與 value chain 圖示的 HTML 報告；並把對應個股登記於 §11 關聯清單，供 stock-analyst（公司 DD）自動讀取引用。觸發：使用者提到「產業研究 / sector DD / 產業報告 / industry landscape / 產業藍圖」或具體主題（玻璃基板、HBM、CoWoS、AI ASIC、GLP-1、核融合、玻璃纖維基板等）且尚未要求做個股 DD。
version: v1.11
date: 2026-05-02
---

# industry-analyst skill v1.11

## 【六大原則（v1.5，2026-04-21 基於 ID_Transformers peer review 強化）】

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
| §0 | TL;DR 卡片 | 數據 | 主題 / 時長 / 規模 / 關鍵玩家 3 / 關鍵風險 3 / 今日 Phase + ★**一句 Thesis（本 ID 最核心的非共識觀點，必須帶 [I:] 或 [X:] tag — QC-I24）**|
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
| **§12** | **Non-Consensus View（共識差異）** | 判斷（🟡） | ★**3 條本 ID vs 市場共識的具體分歧**：共識說什麼 / 本 ID 看法 / 分歧原因；每條 thesis 必須以 [F:] cornerstone fact + [X: base/bull/bear] 三情境呈現（QC-I26）；本章是 insight 核心|
| **§13** | **Falsification Test（證偽條件）** | 數據 | ★**3-5 條具體 metric + base/bull/bear 三情境閾值**（QC-I26）：bear 閾值即 thesis 作廢點，必須是真 falsification 不是 strawman；數字使用 range（QC-I25）；為 PM 層提供停損觸發條件|

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

## 【Claim Taxonomy v1（v1.10 新增，2026-05-01）】

**為什麼加**：Step 8.7 critic gate 已抓「事實對不對」，但 pilot 在 ID_AIInferenceEconomics 找到的 4 條 SIGNIFICANTLY_WRONG 大多屬於這三類，是 pre-publish gate 與 cold-read critic 都不容易抓的：

1. **單一情境被當必然**（"Rubin Ultra 2027 量產 → thesis 成立"，沒列 if 落後 / if 提前）
2. **Spurious specificity**（"Samsung HBM4 yield 78.3%"，實際是 ~75-80% 區間）
3. **意見偽裝事實**（infer 結論寫得像 fact，沒揭露推論鏈）

Claim taxonomy 強制寫稿者**自己在 inline tag 揭露 claim 性質**，讓 reader / critic 一眼看出這是事實還是推論還是情境預測。

### 4-class（不允許第 5 類）

```
🟢 [F: T1: ...]                                  事實 — 有可驗證 source（T1/T2 + 日期）
🟡 [I: A→B]                                      推論 — 寫明事實鏈與結論連結
🔵 [X: base 很可能 / bull 可能 / bear 不太可能]   情境預測 — 三情境並列，詞彙級機率
⚪ [A: ...]                                      假設 — 顯式承認的 prior
```

**意見類（[O:]）刻意拿掉**：避免「意見」變 hand-wave 借口。任何 opinion 必須改寫為 [I: A→B] 揭露推論鏈，否則就是 [A:]（顯式假設）。沒有第三條路。

### 機率用詞彙級（不寫精準百分比）

| 詞彙 | 對應機率區間 |
|---|---|
| 幾乎確定 / near-certain | > 90%（限現場已發生 + 1 步衍生）|
| 很可能 / likely | > 60% |
| 可能 / possible | 30-60% |
| 不太可能 / unlikely | < 30% |
| 幾乎不可能 / near-impossible | < 10% |

**禁止**：寫精準百分比（"60% 機率" / "25% / 15%" / "70% chance"），這本身是 spurious specificity 的高階版（QC-I25 阻擋）。

### Tier-aware enforcement（Q0/Q1/Q2 強度不同）

| Tier | Tag 強制範圍 |
|:---|:---|
| **Q0 Flagship** | 全文：§0 thesis、§2 forecast、§4 TAM、§6 變動方向、§8-§13 全部判斷層 |
| **Q1 Standard** | §0 thesis、§9.5 Kill、§10 phase、§10.5 catalyst、§12 Non-Consensus、§13 Falsification |
| **Q2 Quick** | §12 Non-Consensus、§13 Falsification |

**所有 tier 都強制三段帶 tag**：§0 一句 Thesis、§12 任一 thesis、§13 任一 metric forecast。

### 寫稿時的 inline 標記範例

```
✅ 對：
🔵 [X: base 很可能 — Rubin Ultra 2027 H2 量產（§10.5 catalyst #3）；
       bull 可能 — 2027 H1 提前（NVDA GTC commentary）；
       bear 不太可能 — 2028 延後（CoWoS 良率惡化超出 §13 metric #2）]
       → §12 thesis #1 在 base/bull 都成立；bear 情境本 thesis 失效

❌ 錯：
「Rubin Ultra 2027 H2 量產，本 thesis 成立」
（→ 單一情境當必然，缺 base/bull/bear；違反 QC-I26）

❌ 錯：
「Rubin Ultra 60% 機率 2027 H2 量產，25% 提前，15% 延後」
（→ 精準機率違反 spurious specificity 禁令；違反 QC-I25）

❌ 錯：
「Samsung HBM4 yield 已達 78.3%」
（除非 T1 直接公告該確切值；否則應為 "~75-80%" 或 "~8 成"；違反 QC-I25）

✅ 對：
🟡 [I: ASIC TAM CAGR 推論
       事實 1: Hyperscaler capex 2024-2026 三年 CAGR ~35%（GOOG/MSFT/META 法說 [T1]）
       事實 2: 內製 ASIC 占 capex 比重 從 ~15% → ~25%（SemiAnalysis 2026-Q1 [T3-A]）
       → 本 ID 推論：ASIC 細分 CAGR 應在 ~25-35% 區間
       ⚠ 證偽：若 hyperscaler capex 連兩季 < 20% YoY，本推論 invalid]
```

### 與既有 🟡 judgment bullet 的關係

舊規定 §8-§13 的 🟡 bullet 結構（事實 1/事實 2/→ 推論/⚠ 證偽條件）**仍然保留**。新加的 [F:]/[I:]/[X:]/[A:] tag 是**前綴 inline marker**，不取代 🟡 bullet 結構：

- 一條 🟡 bullet 通常 = 一個 [I:] tag 包整段推論
- §13 metric 表的每格通常 = 一個 [X:] tag（含 base/bull/bear 三情境閾值）
- §0 一句 Thesis = 一個 [I:] 或 [X:] tag

### v1.0-v1.9 與 v1.10 共存策略（機會主義升級）

舊 ID（v1.0-v1.9 寫稿的 80 份）**不主動 batch retrofit** — 80 份 × 1.5-3h = 120-200h，不可承受成本。新 tag 只 apply 於 v1.10 起新寫的 ID 與「大改」的 ID。

**判定「大改」(= 升 v1.10) vs 「小修」(= 保留 v1.0 結構) 的規則**：

| 情境 | 升 v1.10？ | 做法 |
|:---|:---|:---|
| 寫全新主題 ID | ✅ 強制 | 走完整 Step 1-9 v1.10 流程 |
| user 要求「重寫 ID_X」/「全面更新」/ thesis 大方向變更 | ✅ 強制 | 視為新 ID，重跑 Step 1-9，產出 v1.10 |
| user 在 PM 決策重度引用某舊 ID（要加大 theme 配置）| 🟡 建議升 | 手動 retrofit 該份 1-1.5h，值得；ROI 高 |
| user 跑 id-review 修大錯 | 🟢 機會主義 | critic 改動到的段落「順手」手動加 v1.10 tag（不是全文 retrofit）；每份增量 ~10-15 min |
| user 只問資訊（「ID_X 寫了什麼」）| ❌ 不升 | 一字不動 |
| 自動化 patch（未來 cron 級 refresh）| ❌ 不升 | 視為小修，保留 v1.0 結構 |

**為什麼採機會主義而非全面 retrofit**：
1. 80 份舊 ID 中，PM 真正重度引用的 < 20 份（80/20 法則）
2. 機會主義讓「最重要的舊 ID」逐漸升 v1.10，60+ 份 long-tail 永遠停在 v1.0 也無妨
3. 兩年內新 ID 自然取代舊 ID，舊 ID 退場時不需 retrofit cost

**reader 端共存體感**：
- 同一份 INDEX.md 看到不同格式 ID，新 ID 帶 tag、舊 ID 不帶
- v1.10 ID 開頭加 banner 解釋 4-class 與機率詞彙；舊 ID 沒 banner = 默認 v1.0 結構
- 視覺不一致期 ~6-12 個月，可接受

**reader banner（v1.10 ID 必加）**：

```html
<div style="background:#EEF2FF;border-left:4px solid #6366F1;padding:10px 14px;margin:12px 0;font-size:12.5px;line-height:1.6">
  <strong style="color:#3730A3">📐 Claim Taxonomy v1（v1.10+）</strong>：本 ID 在 §0/§9.5/§10/§10.5/§12/§13 使用 4 類 inline tag 揭露 claim 性質：
  <strong>[F:]</strong> 事實（有 source）｜
  <strong>[I:]</strong> 推論（A→B 揭露）｜
  <strong>[X:]</strong> 情境預測（base/bull/bear 三情境，詞彙級機率）｜
  <strong>[A:]</strong> 顯式假設。
  數字以 range / ~xxx 呈現（除非 T1 公告精準值）；機率用「很可能 / 可能 / 不太可能」非百分比。
</div>
```

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

**Evidence pool 引用**（v1.11 新增，2026-05-02）：

引用 `evidence/` 目錄內的 PDF / 法說會 transcript 時用：

```html
<span class="source-tag">[evidence: <a href="evidence/ir_decks/NVDA_2026Q1_earnings.pdf">NVDA_2026Q1_earnings.pdf p.23</a>]</span>
```

對 transcript 用行號代替 page：

```html
<span class="source-tag">[evidence: transcripts/txt/TSM_2025Q4_call.txt L.412-428]</span>
```

`evidence/` 在本地 `.gitignore`（不公開），但寫進 HTML 方便 `id-review` / `industry-thesis-critic` 回查。若 manifest 內 `fetched_from` 是可公開 URL，加 fallback link：

```html
<span class="source-tag">[evidence: NVDA_2026Q1_earnings.pdf p.23 · <a href="https://www.sec.gov/...">SEC EDGAR</a>]</span>
```

詳見 `SEMI_EVIDENCE_SPEC.md` §7。

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

### Step 0 — Evidence Prefetch（v1.11 新增，2026-05-02）

寫稿前先撈本地 evidence pool（投資人日 deck / 法說會 transcript / 技術論文），避免每章重複 WebSearch 抓不到 PDF。詳見 `SEMI_EVIDENCE_SPEC.md`。

**Phase 0a — 候選 ticker（~10 秒）**：

接到主題後列出 candidate ticker（10-15 家寬鬆名單，比最終 §11 list 寬）。對每家：
- 若 ticker **在** `evidence/tickers.json`：列入 fetch 隊列
- 若 ticker **不在**：auto-discover（CIK via EDGAR company-tickers JSON、ir_url 試 5 種 pattern + HEAD 200）→ 列出來給 user confirm 一次 → confirm 後 append `tickers.json` → 列入隊列
- 若 auto-discover 失敗：列入 missing 清單，請 user 手動補

**Phase 0b — Fast fetchers（~2 分鐘，平行）**：

呼叫 `scripts/evidence/orchestrator.py` 的 `fetch_for_id_session(candidate_tickers, topic_keywords)`：
- 對每家 ticker：`grep_manifest(ticker, days=30)` 有 hit → skip；否則跑 Tier 1（EDGAR 8-K + EX-99 過去 90 天）+ Tier 2（IR 雙頁面爬）
- 對主題 keywords 跑 Tier 3（arXiv 過去 180 天）

**Phase 0c — Slow transcripts（背景非阻塞）**：

對 top 3-5 ticker（ID 主題最相關）的最近一場 earnings call 或 investor day webcast 跑 `youtube_transcript`，背景跑、不卡 Phase 1 寫稿。20-40 分鐘完成後可被 §10 / §11 / §12 引用。

**Phase 0 結束時的 deliverable**：

1. 列「missing 清單」給 user：哪些 ticker 抓不到、哪些 webcast 沒 PDF deck，請 user 補 upload 到 `evidence/inbox/`
2. 列已 fetch 完成的 evidence count（e.g.「NVDA: 2 EDGAR + 1 IR deck，TSM: 0 EDGAR + 6 IR deck」）
3. 進入 Step 1 開始研究

**例外：單家 ID**：若主題只關 1 家公司（如 ASML High-NA EUV 專題），prefetch 退化成單家撈，Phase 0a/0b/0c 合併為一次跑完。

**離線 fallback**：若 `evidence/` 目錄不存在或 orchestrator 不可用（新機器尚未 setup），跳過 Step 0 直接進 Step 1，不阻斷 ID 寫稿。Step 1+ 仍走 WebSearch / WebFetch 原路徑。

### Step 1 — 主題界定（2 輪 WebSearch）
- Search 1：`{主題} technology overview 2026` → 技術輪廓
- Search 2：`{主題} market size forecast` → 規模錨點
- 產出：§0 TL;DR 卡片 + §1 邊界表的草稿

### Step 2 — 技術深挖（3-5 輪，優先抓 T1 簡報）
- **先讀本地 evidence**（v1.11）：`grep_manifest(tags=[主題 keywords])` 撈 `evidence/ir_decks/` + `evidence/tech_papers/` + `evidence/transcripts/` 相關檔，先 `Read` 完再決定要 WebSearch 補什麼 — 投資人日 deck 與會議論文這層 PDF 多在本地，不要重複 WebFetch
- **先試**：`{主流玩家} investor day 2026 slides filetype:pdf` / `{玩家} technology keynote deck`
- 若主題是半導體：`{公司} GTC 2026 keynote`、`{公司} technology symposium 2026`、`TSMC OIP 2026`
- 若主題是生技：`{公司} R&D day presentation`、`ADA 2026 abstract {藥物}`
- 若主題提到特定技術（如 LIDE、TGV、HBM4E）→ 針對性 search 該技術 IEEE 論文 + 設備商網站
- **WebFetch 抓 T1 簡報**：取關鍵 slide 標題、數據、路線圖
- 產出：§2 S 曲線（優先用官方 roadmap）、§3 技術棧矩陣（引用 slide 編號）

### Step 3 — 市場與供應鏈（3-5 輪）
- `{主題} market size TAM 2030 SEMI report` / `Yole {主題}` / `IC Insights {主題}`
- 回頭掃 Step 2 抓到的 IR deck **+ `evidence/ir_decks/` + `evidence/industry_research/`（user-uploaded Yole / SemiAnalysis 等付費深度）+ `evidence/broker_reports/`** 找 TAM 圖（v1.11）
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
- **先讀 ticker-level evidence**（v1.11）：對 §6 玩家矩陣每家 ticker 跑 `grep_manifest(ticker=X)` → 對 hits 用 `Read` tool 讀取（PDF / .htm / .txt 都支援，PDF 分頁 ≤20）。重點抽：營收 segment mix（決定 §11 影響深度 🔴🟡🟢）、capacity / capex 數字、management commentary。Citation 用 `[evidence: <path> p.<N>]` 格式
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

### Step 8.5 — Pre-Publish Gate Check（v1.6，10 條 Gate）

讀取 `pre_publish_check.md` 的 10 條 Gate，逐條跑阻斷檢查：
- Gate 1 [阻斷] 核心 ticker financials < 60 天
- Gate 2 [阻斷] Event-triggered thesis < 14 天
- **Gate 2.1 [阻斷, v1.5 新增] Thesis Cornerstone Fact Verification** — 「獨家 / 首家 / 唯一」類 claim 必須獨立 WebSearch 驗證 ecosystem 玩家，避免重演 Eaton 獨家 800V DC 類錯誤
- Gate 3 [阻斷] Cross-ID reconciliation（共用 ticker / 事實一致）
- **Gate 3.1 [warning, v1.5 新增] Cross-ID Thesis Bias Detection** — 跨 ID 同 ticker 定性偏差 red flag 檢查
- Gate 4 [warning] Catalyst & Falsification 狀態標示
- Gate 5 [warning] Unit & scope consistency
- Gate 6 [warning] Cross-ID layer disambiguation（switch vs chip-level）
- Gate 7 [warning] Sub-topic ID value-add rule（子題 vs 母題）
- **Gate 8 [阻斷, v1.6 新增] id-meta JSON validation** — `python3 scripts/validate_id_meta.py docs/id/ID_X.html` 必須 exit 0（避免 CI strict gate 連坐被擋）

任一阻斷 Gate (1/2/2.1/3/8) fail → 阻斷發布 + 列修正項；阻斷 Gate 全過、warning Gate (3.1/4/5/6/7) 有 fail → 允許發布但輸出 warning。輸出 `pre_publish_report.md` 記錄 pass/fail 明細。

### Step 8.7 — Mandatory Critic Gate（v1.9，2026-05-01 新增）

寫好 ID HTML 草稿後（暫存於 `/tmp/` 或 staging path），**必須**呼叫 `industry-thesis-critic` sub-agent 跑 cold review，找出 conclusion-changing 大錯。

**為什麼加這一步**：Step 8.5 的 Gate 都是「機械正確性」（id-meta valid、cornerstone fact 14d 內、source 不在黑名單等）— 抓不到「推理錯誤 / thesis 與外部現實不符」。Step 8.7 引入跨模型（Sonnet）冷讀者抓真正的 thesis-level 大錯。Pilot 在既有 4 份 ID 上找到平均 1-4 條 CHANGES_CONCLUSION 大錯，證明 Step 8.5 不夠。

**呼叫方式**：

```
Agent({
  description: "Pre-publish critic gate on {Theme}",
  subagent_type: "general-purpose",
  model: "sonnet",  // 必須 Sonnet — 與寫稿者（Opus）跨模型，避免 echo chamber
  prompt: """
You are operating as the industry-thesis-critic sub-agent.
Read spec at /Users/ivanchang/.claude/agents/industry-thesis-critic.md.

ID file path: {staging path}
User's intent: 「pre-publish gate check — 即將 publish，找出 conclusion-changing 大錯」

Run all 6 items + Item 6.5 CONCLUSION_IMPACT triage.
Save report to /tmp/_prepub_critic_{Theme}_{date}.md.

After saving, return brief summary with COUNTS by tier:
- 🔴 CHANGES_CONCLUSION: N
- 🟡 PARTIAL_IMPACT: M
- 🟢 COSMETIC: K

Highest priority issues (top 3 by CONCLUSION_IMPACT).
"""
})
```

對 Q0 Flagship ID 必須再跑 Pass 2（focused 大錯掃描，prompt 同 id-review skill Step 3）。

**Gate 判定**：

| Quality Tier | 0 🔴 | ≥1 🔴 |
|---|---|---|
| **Q0 Flagship** | ✅ Pass | 🔴 **BLOCKING** — 必須先在 industry-analyst 內修，重跑 critic 直到 0 🔴 才放行 Step 9 |
| **Q1 Standard** | ✅ Pass | ⚠ **WARNING** — 給 user 看 critic findings，user 選擇 ship 或 fix |
| **Q2 Quick** | ✅ Pass | ⚠ **WARNING** | 同 Q1 |

**WARNING 模式下 user 選 fix**：
- 進入 id-review skill 的 patch 流程（mode (a) user-in-the-loop）
- 改完後重跑 Step 8.7 → 進 Step 9 publish
- 改完後若仍有 🔴 → 再次 WARNING 給 user

**BLOCKING 模式下**：
- industry-analyst skill 必須回到 Step 5（判斷層）/ Step 6（§11）/ Step 7（§12-§13 synthesis）修正
- 修正完成重跑 Step 8.5 + Step 8.7（這次只跑 Pass 1 即可，因為大錯已修）
- 重跑 critic 仍有 🔴 → 重複，最多 3 輪。3 輪仍未過 → 告訴 user「critic 持續找到大錯，建議重新研究」

**事實基礎**（為何這個 gate 有效）：
- Pilot Pass 1 critic 在 ID_AdvancedPackaging（既有 publish）找到 Thesis #2 cornerstone fact BROKEN（Rubin Ultra 4-tile 設計與 ID 寫法不符）— 這是寫稿時 self-review 抓不到的
- Pilot Pass 2 在 ID_AIInferenceEconomics 找到 3 條 Pass 1 沒抓到的大錯（ASIC CAGR 44.6% 過度誇大 / GOOG「唯一三層」MSFT 已 launch Maia 200 / Rubin 10x MoE-specific）
- 跨模型（Sonnet）+ 沒有寫作 context = cold reader 視角，這是寫稿者（Opus）做不到的

### Step 9 — 產出 HTML + INDEX
- 寫入 `docs/id/ID_{Theme_CamelCase}_{YYYYMMDD}.html`
- **`<head>` 必含 `<script id="id-meta" type="application/json">{...}</script>`**（在 `<title>` 之後、`<style>` 之前）— 這是下游消費者（stock-analyst §11、CI validator、未來 sector index）的 SSOT。完整欄位定義見 QC-I14.5；範例骨架見 `templates/html_template.md`。**漏寫此區塊 → CI `Validate DD + ID metadata` workflow strict gate fail，整 push 連坐被擋**
- append `docs/id/INDEX.md` 一行
- 更新 `docs/id/index.html` 列表
- 若 `docs/research/index.html` 有「產業深度」tab，更新 markers
- **重新生成 DD ↔ ID 對應表**：執行 `python3 scripts/id_dd_mapping.py`（若該腳本存在）
- **回補現有 DD 的 ID banner**：執行 `python3 scripts/retrofit_dd_id_banner.py`（若該腳本存在）→ 新 ID 的覆蓋 ticker 會自動在其 DD 頂部顯示連結
- **本地最後驗證**：`python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{YYYYMMDD}.html`（exit 0 才能 commit）
- `git add + commit + push`（依 MEMORY feedback）

### Step 9.5 — Tier Matrix 健康度檢查（v1.7+ 新增）

**完稿後必跑**：`python3 scripts/check_tier_matrix.py --inject-html`

此步驟做兩件事：
1. **掃描差距**：偵測新 ID 中出現但未列入 `docs/id/tier_matrix.html` 的 ticker（≥ 2 份 ID 為 signal threshold）
2. **更新 alert**：自動把健康度 banner 注入 `/research/index.html`（已發財報但 DD 未更新下方）+ `/id/index.html`（已建 ID 總數 flash card 上方）

**輸出處理**：
- 若返回「✅ 與 ID / DD 同步」 → 無需動作
- 若返回「🆕 N 檔新 ticker」 → **必須在回給 user 的訊息中提示**：「本次 ID 新增 X 檔 ticker（A、B、C），是否評估加入 Tier Matrix？建議 PM 級 3 軸打分後決定 Tier。」
- 若返回「⏰ 半衰期警示」 → 提示 user 已超過 53 天，建議完整 review

此步驟與 Step 9 的 commit 一起 push（同 commit 涵蓋 ID 新增 + alert 更新）。

---

## 【QC-I 規則（v1.10 含 Claim Taxonomy）】

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

---

### QC-I14.5｜【v1.8+ 必備】id-meta JSON 結構化區塊

**根因解決**：取代散落 individual meta tags 的反向 parse 困難。每份 ID HTML 的 `<head>` 內必含
`<script id="id-meta" type="application/json">{...}</script>`，作為下游消費者
（stock-analyst skill §11 自動引用、未來 sector index page、自訂分析腳本）的 SSOT。

**生成位置**：在 `<title>` 之後、第一個 `<style>` 之前，與既有 `<meta name="id-*">` tags 並存
（meta tags 可保留作為向後相容；新工具一律讀 JSON）。

**必填欄位**：

| 欄位 | 型別 | 說明 |
|:---|:---|:---|
| `theme` | string | 產業主題（e.g. `"AI EDA + IP"`、`"HBM 供需循環"`） |
| `skill_version` | string | 建立時 industry-analyst skill 版本（`"v1.8"` 等） |
| `id_version` | string | 此 ID 自身版本（`"v1.0"` for 初版，更新後 `v1.1` etc） |
| `publish_date` | string | `"YYYY-MM-DD"` |
| `thesis_type` | enum | `"structural"` / `"event-triggered"` / `"mixed"`（QC-I22 半衰期判定） |
| `ai_exposure` | enum | `"🟢"` 直接受益 / `"🟡"` 部分受益 / `"🔴"` 中性或受害 |
| `oneliner` | string | ≤ 200 chars，本 ID 的核心 thesis 一句話 |
| `related_tickers` | array | 關聯個股清單；每項 `{ticker, role, depth, beneficiary}` |

**選填欄位**（補充用，不強制）：

| 欄位 | 型別 | 說明 |
|:---|:---|:---|
| `tam_usd_2030` | number | 2030 TAM in billion USD |
| `cagr_pct_5y` | number | 5Y CAGR % |
| `growth_phase` | enum | `"early"` / `"mid"` / `"late"` / `"declining"` |
| `value_chain_position` | enum | `"upstream"` / `"midstream"` / `"downstream"` / `"cross-tier"` |
| `industry_structure` | enum | `"monopoly"` / `"duopoly"` / `"oligopoly"` / `"fragmented"` |
| `sections_refreshed` | object | `{"technical": "YYYY-MM-DD", "market": "YYYY-MM-DD", "judgment": "YYYY-MM-DD"}` |
| `sister_ids` | array | 兄弟 ID HTML 檔名列表 |

> #### 🚫 **嚴禁複合 enum 值 / 自創字串 / 加修飾詞**（CI strict gate 阻斷）
>
> Validator 嚴格匹配上面的 enum 字串集合。**禁止以下實際發生過的錯誤**：
>
> | ❌ 違規寫法 | ✅ 正確寫法 | 說明 |
> |:---|:---|:---|
> | `"thesis_type": "structural+event"` | `"mixed"` | 用 `mixed` 表達雙重屬性，不要 `+` 拼接 |
> | `"growth_phase": "mature_diverging"` | `"late"` | mature 對應 `late`；diverging 是敘事細節，不放 metadata |
> | `"growth_phase": "structural_supercycle_expansion"` | `"mid"` 或 `"early"` | 自創長字串一律映射到四選一 |
> | `"growth_phase": "consolidation"` | `"late"` | consolidation 屬於 mature 後期 |
> | `"value_chain_position": "concentrate-to-shelf"` | `"cross-tier"` | 跨多段價值鏈一律 `cross-tier` |
> | `"value_chain_position": "upstream_commodity"` | `"upstream"` | 不要加修飾詞 |
> | `"value_chain_position": "intermediation"` | `"cross-tier"` | 銀行業中介性質 = 跨上下游 |
> | `"industry_structure": "oligopoly+disruption"` | `"oligopoly"` | disruption 是動態描述，不放結構 enum |
> | `"industry_structure": "regional_oligopoly"` | `"oligopoly"` | 地區性質寫進 oneliner，不加修飾 |
>
> **規則**：metadata 是給 validator + 下游 parser 讀的「分類標籤」，不是給人讀的「敘事描述」。複雜的二元性、地區屬性、disruption 動態，都寫進 §1 / §2 章節內文裡，metadata 只保留 enum 主分類。
>
> #### 🚫 **`oneliner` 嚴格 ≤ 200 chars**（包含中英文混合）
>
> Validator hard cap 200 字元。實際發生過 308 / 468 / 483 / 614 字元 violation——LLM 容易把整段 thesis 塞進 oneliner。**正確做法**：
>
> 1. oneliner 只放 3–5 個關鍵數字錨點 + 1 個結論動詞
> 2. 詳細論述全部留給 §1 投資論點 / §11 兄弟 ID 章節
> 3. 寫完後用 `len(d['oneliner'])` 自測；若 > 180 立刻精簡（留 20 char buffer 應付下游 emoji / 全形字元計算差異）
>
> 範例（180 chars 內）：「銅 2026 預期 \$11K–13K（Citi \$13K / GS \$10.7K / MS 600kt deficit「20 年最嚴」）；三引擎共振：AI DC + Grid + EV；Anglo-Teck \$53B + Codelco \$40B 響應。」

#### 寫完後自我驗證（不可省略）

Write 完 ID HTML 後**立即執行**（在報告 terminal 摘要之前）：

```bash
python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{YYYYMMDD}.html
```

- exit code 0 → 繼續輸出 terminal 摘要
- exit code != 0 → 讀取錯誤訊息，用 Edit 工具修正 id-meta JSON，重跑 validator，直到 exit 0 才宣告完成。**不允許帶錯誤推 commit**（CI strict gate 會擋）

**`related_tickers` 物件 schema**：

```json
{
  "ticker": "AVGO",
  "role": "AI ASIC 設計 + 網通 silicon photonics",
  "depth": "🔴",
  "beneficiary": true
}
```

- `depth`: 🔴 核心受益（核心業務直接相關）/ 🟡 中度（部分業務相關）/ 🟢 輕度（衍生效應）
- `beneficiary`: `true` 受益 / `false` 受害

**範例**（AI EDA + IP）：

```html
<script id="id-meta" type="application/json">
{
  "theme": "AI EDA + IP",
  "skill_version": "v1.8",
  "id_version": "v1.0",
  "publish_date": "2026-04-27",
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
  "industry_structure": "duopoly"
}
</script>
```

**驗證**：寫完 ID HTML 後，重點是 JSON 可解析 + 必填欄位齊全。執行
`python scripts/validate_id_meta.py` 驗證。CI 也會自動跑。

**為什麼需要 id-meta**：DD plan A 的相同邏輯——避免下游消費者反向 parse HTML
內文（每次 skill template 改寫就崩）。stock-analyst skill §11 可直接從 id-meta 的
`related_tickers` array 自動 join 公司 DD ↔ 產業 ID，無需手動維護。

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

### QC-I24｜Claim Taxonomy 標記強制（v1.10 新增）

依 Tier-aware enforcement 表（Q0 全文 / Q1 §0+§9.5+§10+§10.5+§12+§13 / Q2 §12+§13），強制章節的 claim 必須有 4 類 tag 之一（[F:] / [I:] / [X:] / [A:]）。檢查方式：

- **§12 每條 thesis** 至少 1 個 [F:]（cornerstone fact）+ 1 個 [I:] 或 [X:]（推論 / 情境）
- **§13 每條 falsification metric** 至少 1 個 [X:]（base/bull/bear 三情境的閾值）
- **§0 一句 Thesis** 至少 1 個 [I:] 或 [X:]
- **§10.5 catalyst** 每條 expected 結果至少 1 個 [X:]（達成 / 落空 / 部分）
- **§9.5 Kill scenario** 每條至少 1 個 [I:]（揭露 kill 機制的推論鏈，避免 strawman）

缺 tag = 視為 [O:] 意見類 = QC-I24 fail，返工。

**bull case**：tag 雖然會增加報告「視覺密度」，但這是 reader 端可立即識別 claim type 的代價；且 v1.10 起新 ID 開頭的 banner 會解釋 4-class 含義，learning curve 一次性。

### QC-I25｜Spurious Specificity 禁令（v1.10 新增）

**禁止精準數字**（除非 source 直接公告該確切值）：

| 類別 | ❌ 禁止 | ✅ 允許 |
|:---|:---|:---|
| 市佔（估算）| "62.7%" / "78.3%" | "~70%" / "60-65%" / "~6 成" |
| 預估時間 | "2027-09-15" / "2027 Q3 中旬" | "2027 H2" / "2027 Q3-Q4" |
| 預估 TAM | "$53.7B" | "~$50B" / "$50-60B" |
| 預估良率 | "yield 78.3%" | "~80%" / "yield 7-8 成" |
| 機率 | "60% 機率" / "p=0.6" | 詞彙級「很可能」 |
| Multiple | "5.3x EPS" | "~5x" / "4-6x" |

**例外（保留精準數字）**：
- T1 source 直接公告該確切值（如 10-K 揭露 "Q4 revenue $63.2B" / NVDA 法說 "Blackwell GB200 unit price $40K"）→ 保留 + 必須帶 [F: T1: ...] tag 並引 source
- 過去歷史已實現的數字（"FY24 Q3 revenue $18.5B"，from 10-K）→ 保留
- 行業標準規格（"HBM3E 8-Hi stack"、"3nm node"）→ 保留

**判斷原則**：
> **這個精準數字是 source 公告的、還是分析師估算的？**
>
> - 公告 → 保留 + [F:] tag + 引 T1/T2 source
> - 估算 → 必須改 range 或 ~xxx；且通常該 claim 應該是 [I:] 或 [X:] 類

**抓 spurious specificity 的自我檢核**：寫完一段後，回頭找所有兩位 / 三位有效數字的非整數，每個都問自己「這是 published source 還是我估的」。估的就改 range。

### QC-I26｜多情境強制（v1.10 新增）

§12 / §13 / §10.5 / §0 thesis 涉及 forecast 的 claim 必須以 [X:] 標記呈現 base / bull / bear 三情境：

- **base**（很可能 / 主基準）：本 ID 預設情境
- **bull**（可能 / 偏多 alternate）：thesis 強化情境
- **bear**（不太可能 / 偏空 alternate）：thesis 弱化或失效情境

**bear 情境必須是 §13 falsification metric 的真實 trigger**，不是 strawman（避免 ID_AIInferenceEconomics critic 抓到的「kill scenario 是 strawman」類錯誤 — 列了「外星人入侵」級別的 bear，等於沒列）。

**bear 情境 sanity check**：
1. bear 情境的觸發點，是否真的對應 §13 至少 1 條 falsification metric？
2. bear 若成真，§12 該 thesis 是否真的 invalid？（不是「conviction 微降」而是「方向變」）
3. bear 機率有沒有低於 10%（near-impossible）？若有 → 你列的可能是 strawman，重列

單一情境呈現（"X 將發生 → thesis 成立"）= QC-I26 fail，返工。

「兩情境」（只有 base + bear，缺 bull）= QC-I26 fail。bull 情境是 thesis-strength 的天花板，缺它會 cap 對 conviction 的調校。

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

- **v1.11（2026-05-02）**：新增 Step 0 — Evidence Prefetch（呼叫 `scripts/evidence/orchestrator.py` 的 `fetch_for_id_session()`，撈 EDGAR 8-K + EX-99 + IR deck + arXiv paper 到 `evidence/`，YouTube webcast 背景跑 whisper 轉文字）。Step 2 / 3 / 6 加 hook：寫稿前先 `grep_manifest` + `Read` 本地 evidence，避免 WebFetch 對 PDF / 音訊無解的限制。引用規範新增 `[evidence: <path> p.<N>]` tag。源於 `SEMI_EVIDENCE_SPEC.md` 設計：補強 ID 的 primary-source 比例（投資人日 deck、法說會 transcript、技術論文）。離線 fallback：`evidence/` 不存在或 orchestrator 不可用時跳過 Step 0，原 WebSearch / WebFetch 路徑繼續可用。**白名單擴充**：`evidence/tickers.json` v1 收 10 家半導體（NVDA/TSM/ASML/AMD/AVGO/INTC/MU/AMAT/LRCX/KLAC），新 ticker 寫 ID 時 auto-discover + user confirm 後 append。
- **v1.10（2026-05-01）**：Claim Taxonomy v1（4-class [F:]/[I:]/[X:]/[A:]）+ 詞彙級機率 + tier-aware enforcement（Q0 全文 / Q1 §0+§9.5+§10+§10.5+§12+§13 / Q2 §12+§13）。新增 QC-I24（taxonomy 標記強制）、QC-I25（spurious specificity 禁令）、QC-I26（多情境強制：base/bull/bear，bear 必須對應 §13 真 trigger 不是 strawman）。§0/§12/§13 schema 描述同步引用 tag 要求。**v1.0-v1.9 共存策略**：機會主義升級（不主動 batch retrofit 80 份；新主題 / user 要求重寫 / PM 重度引用 → 升 v1.10；id-review 修大錯時順手加 tag；純資訊查詢不動）。v1.10 ID 必加 reader banner 解釋 4-class。critic spec（industry-thesis-critic.md）與 id-review skill 在本版**未升** — taxonomy enforcement 暫為 self-check（QC-I24/25/26 寫稿者自跑），observation period 跑 3-5 份 v1.10 ID 後再決定是否 cascade 改 critic（加 version-gate）。
- **v1.0（2026-04-19）**：初版。11 章 schema；🟡 規則；QC-I1-I6；stock-analyst 整合鉤子。
