---
name: supply-chain-cartographer
description: 建立「產業供應鏈互動地圖」— 把產業鏈拆成節點 × 廠商 × 競爭態勢 × 客戶獨家／關鍵單點的視覺化頁面，與 industry-analyst v2.0（敘事為骨、表格為窗的產業深度報告，含供需循環敘事 + 決策層）並列的另一種產業視角。輸入產業主題（如「HBM」「ASIC」「先進製程」「IC 設計」「人形機器人」），skill 執行多輪 WebSearch / WebFetch 研究（英文 + TW 中文雙語策略），輸出 docs/supply-chain/data/{topic}.json + 一支 thin {topic}.html template，引擎 (engine.css + engine.js) 已存在不需動。row 數量自由（3-6 列），由產業敘事決定；每個 single-point ⚑ 必須引用 ≥2 來源並標註信心度。v1.1：新 topic 必餵機械層 sidecar（terminal_markets.json 終端封鎖值＋substitution_lags.json 替代難度四檔）——hub 瓶頸分級為編輯層（curated T0-T2/OVER）＋機械層對帳（漏網提名）兩層制。觸發：使用者說「跑 {topic} 供應鏈地圖」/「{topic} supply chain map」/「畫 {topic} 供應鏈」/「{topic} supply-chain」/「supply-chain {topic}」。
version: v1.2
date: 2026-07-16
---

# supply-chain-cartographer skill v1.2

## 條件載入路由表（v1.2 結構拆分：核心 = always-on，references/ = 按需載入）

> v1.2 把 5 輪研究細則、💎/Tier pick 框架、JSON schema、HTML template、輸出機械層、版本沿革搬到 `references/`（內容自 v1.1 原文零語意變更搬移），核心從 724 行減到 ~290 行——目的是把注意力預算還給研究深度與 ⚑ 掛旗判斷。核心保留：定位/觸發語、既有架構、機械層 sidecar 紀律、工作流骨架、⚑ Single-Point Framework（掛旗閘）、信心度標註 convention、品質 Gate、stingtao 殘留檢查。

| 時點 | 條件 | 必 Read |
|---|---|---|
| 研究階段（Round 0 開始） | 一律 | `references/research-rounds.md`（5 輪研究搜尋詞範本＋TW 中文源清單＋DD 對照指令） |
| Step 1 寫 JSON | 一律 | `references/json-schema.md`（頂層/Node/Company 欄位表＋範例 node） |
| 寫 JSON 標註 core_business / supply_chain_lock / node_role 時 | 有候選 💎/🐘/🔒 | `references/pick-frameworks.md`（💎 Top Picks v1.3 + 三層 Tier 全文） |
| Step 2 寫 {topic}.html | 一律 | `references/html-template.md`（thin template 全文） |
| Step 3 之後（manifest 翻牌→hub→build→push→驗證） | 一律 | `references/output-plumbing.md`（Step 3/3.5/4/5 全文） |
| 修改本 skill 規則 / 查動機與 gap 時 | — | `references/changelog.md`（預期效益＋已知限制＋版本沿革） |

標準流程只需載入 research-rounds（研究階段）、json-schema（Step 1）、html-template + output-plumbing（Step 2 之後）；有 💎 候選才載入 pick-frameworks。

## 定位

把產業鏈拆解成**互動式視覺地圖**：節點 = 製程環節 / 元件子段 / 客戶層 ; 邊 = 上下游關係 ; 標籤 = 競爭態勢（壟斷 / 寡占 / 紅海 / 高速增長 / 新興萌芽）+ ⚑ 客戶獨家／關鍵單點。

**與 ID 的分工**：
| 視角 | 主要載體 | 適用情境 |
|---|---|---|
| ID（industry-analyst v2.0） | §0 決策層 + 9 章節 HTML，敘事為骨表格為窗（含供需循環敘事 + 決策資產） | PM 決策 + 深度準備（v2.0 已併入舊 DS 的敘述供需循環） |
| **本 skill** | 互動式 JSON map | **看「製程節點上誰是脆弱依賴點」**、surface 沒做過 DD 的關鍵小單點 |

兩者**可並存**：同 theme 出 ID + supply-chain 兩份不衝突。（註：舊 industry-ds DS 已於 2026-06-11 併入 industry-analyst v2.0；8 份 legacy DS 凍結保留。）

## 觸發語

- 「跑 {topic} 供應鏈地圖」/「{topic} 供應鏈」/「畫 {topic} 供應鏈」
- 「supply-chain {topic}」/「{topic} supply chain map」/「supply chain {topic}」
- 用戶丟一個產業主題 + 要視覺化節點圖

## 既有架構（不需動）

**引擎** — 已抽離，所有 topic 共用：
```
docs/supply-chain/
  assets/
    engine.css      # 全部視覺規則（status colors / cards / drawer / tooltip）
    engine.js       # 渲染引擎 + SVG edges + drawer + search + DD-link lookup
  data/
    topics.json     # 全 topic manifest（active flag 控制是否上線）
    dd_links.json   # ticker → DD HTML path（由 build script 重建）
    {topic}.json    # ← 本 skill 主要產出
  index.html        # Hub 頁（hardcoded HTML — 不是動態渲染 topics.json，新 topic 上線要手動補入口，見 Step 3.5）
  cowos.html        # 第 1 個 topic（worked example）
  cpo.html          # 第 2 個 topic（worked example）
  {topic}.html      # ← 本 skill 順手產出（thin template，~50 行）
```

**支援腳本**：
```
scripts/
  build_supply_chain_dd_index.py   # 掃 docs/dd/ 重建 dd_links.json
  build_supply_chain_tiers.py      # 掃全部 data/*.json，把 💎/🐘/🔒 三層去重聚合，
                                   # 注入 index.html 的「全站 Top Picks 統整」區（TIERS_AUTO 標記）
```
> 任何 map 的 ⚑/💎/`node_role` 改動後（含新增 topic），**重跑 `python3 scripts/build_supply_chain_tiers.py`** 刷新 hub 統整區，與 index.html 併入同一 commit。

## 【機械層輸入（v1.1，2026-07-09——瓶頸強度兩層制）】

Hub 的稀缺分級是兩層制：**編輯層**（tiers script 內 T0/T1/T2/OVER curated 清單）＋**機械層對帳**（替代難度 × 終端封鎖值，挑戰者角色——「機械高分 × 編輯未收」＝漏網提名，防小產業被編輯視野漏掉）。新 topic 上線時必須餵機械層兩個 sidecar：

1. **`data/terminal_markets.json`** append 一筆：本鏈最下游產出品的年市場規模（USD B）＋basis＋source＋confidence。**定義紀律**：鏈的「直接產出」終端市場，不放大到全經濟；這是「下游封鎖值」權重——**刻意不用節點自身 marketSize**（防味之素 ABF 型「小節點大封鎖」被市場規模埋掉）。
2. **`data/substitution_lags.json`** append 本鏈候選節點（monopoly ∪ ⚑ ∪ 終端市場前二大節點）的替代難度判定：`>5y`（十年級技術/生態壁壘，**此檔必附外部佐證**）/ `2-5y`（長認證週期材料/設備）/ `<2y`（第二源認證中）/ `replaceable`。不確定取較短 tier（防高估稀缺）；需求/買方層節點一律 `replaceable`。

之後重跑 tiers script，機械對帳表自動吃進新鏈。**⚑ 的角色自 v1.1 起是排行榜輸入訊號之一**，不是獨立維護的 metadata——掛旗紀律（≥2 源）不變，但「本鏈最窄節點是誰、為什麼」的 KEY CALL 判斷以 substitution_lags 的 tier 為權威表達。

## 工作流骨架（標準 5 輪研究 + 4 步輸出）

> 每輪的搜尋詞範本、TW 中文源清單、DD 對照指令 → 研究階段開始時載入 `references/research-rounds.md`（此處只列骨架）。

- **Round 0 · 先看現況**：確認 topic 在 manifest（不在就加）、看既有範例（cowos/cpo）、估研究時間（半導體製造 ~60-90 min / 跨產業 ~90-120 min）。
- **Round 1 · 產業 Overview + 主玩家**（4-5 平行 WebSearch，英文優先）：抓產業骨架、全球 majors、上量時間、關鍵客戶。
- **Round 2 · TW 中文供應鏈**（5-8 中文 WebSearch）：這是純自研最弱環節，**必須用中文源**（TechNews / Money Weekly / TrendForce / Digitimes / 工商時報 / 經濟日報 / 數位時代 / 鉅亨 / Vocus / StatementDog）找 TW 小型股客戶獨家與法說數字。
- **Round 3 · 垂直深度**（3-5 平行 WebSearch）：對 topic 特定關鍵環節深掘（HBM→DRAM 三強/TC bonder；CPO→DFB 雷射/MLA/FAU 等）。
- **Round 4 · 競爭驗證**（2-3 focused WebSearch）：對每個要標 ⚑ 的 single-point **強制找第二個獨立來源**。高信心 ⚑≥2 源（含 1 權威源）；中信心明標「送樣中/待量產/單一來源」；低信心（謠傳/單一 substack）**不標 ⚑**。
- **Round 5 · DD universe 對照**：跑 `build_supply_chain_dd_index.py`，列出本 topic ticker 哪些有 DD。沒 DD 的小型 ticker 不是問題（正是要 surface 的 gap），但要在 commit message 列為未來 DD 待補清單。

## Row 數量決策表

**重點**：3 列不是強制。Row 數量由**產業敘事自然走向**決定。

| Topic 類型 | 建議 row 數 | 範例 row 結構 |
|---|---|---|
| 半導體製造（CoWoS、HBM、面板級封裝） | **3** | 設備 / 主製程流 / 材料 |
| 半導體光電混合（CPO、矽光子） | **5** | 設備 / 光電晶片 / 整合系統 / 光學元件 / 光纖材料 |
| 先進製程（2nm GAA、High-NA） | **4-5** | EUV/設備 / FEOL / BEOL / 材料 / 良率測試 |
| IC 設計類（Fabless / ASIC） | **5** | IP / EDA / Fabless / Foundry / Hyperscaler（**無設備層**） |
| 半導體材料（純材料 topic） | **2-3** | 純材料分段 |
| 系統組裝（AI 伺服器 ODM、電源散熱） | **5** | 加速器/HBM / 機板連接 / ODM 組裝 / 散熱電源 / Hyperscaler |
| 跨領域硬體（人形機器人） | **5-6** | 致動器 / 感測器 / 算力 / 機構 / 電池 / 軟體 |
| 太空 / 國防 | **5** | 載台 / Payload / 通訊電戰 / 地面 / 軟體 |

**規則**：
- 每一列要是**有意義的概念層**（不只是「節點變多」）
- 太多列（>6）→ 視覺垃圾，重新分群
- 太少列（=2，除非純材料）→ 失去階層感

## ⚑ Single-Point Framework — v1.3 雙軸 + 硬預算 + critic gate（2026-05-29 起）

> **重大變更**（取代 v1.2 的單軸 3-Gate）：
> 1. **主軸從「市佔集中度」換成「非替代性」**。v1.2 拿 Gate A（結構壟斷）當必過主軸，但**市佔高 ≠ 不可或缺** — 一家 95% 市佔但有 3 家已認證替代源、6 個月可 ramp 的供應商不是單點；一家 40% 市佔但 IP 被 co-design 進客戶產品、requalify 要 3 年的才是。v1.3 把**非替代性（換不換得掉 × 多久）設為主軸（Axis 1）**，市佔結構降為**佐證軸（Axis 2）**。兩軸 AND。
> 2. **每 topic 硬預算**：⚑ ≤ `max(5, ceil(節點數 × 0.15))`。強迫排序，超出降主表 note。validator pre-commit 把關（topic JSON 標 `single_point_framework: "v1.3"` 後變 hard error；未標只 warn，供漸進遷移）。
> 3. **critic gate**：寫 ⚑ 的 agent ≠ 判 ⚑ 的 agent（Boris verify pattern）。候選清單寫完後 spawn `single-point-critic` 對抗裁決。
> Reason: v1.2 後全站仍 **29% 節點打 ⚑**（hbm / advanced 達 50%）。市佔軸漏了一堆「市佔高但客戶可換」的假單點 + 把「重要製程」「第二供應源」也誤標。

### 判定：兩軸都過 AND（缺一不可）+ 經濟 gate + Kill Test

> **v1.5 修正（2026-05-29）— 能力非替代性是唯一合格軸，「客戶獨家」不算**：
> 「X 是客戶 Y 的獨家供應」混了兩種**相反**的東西 —（a）**能力獨佔**：全世界別人做不出來，moat 是技術/製程；（b）**客戶配置**：別人做得出來，只是 Y 現在單選 X = **客戶集中風險,非護城河**。v1.3 把「客戶獨家」當合格證是 bug。v1.5 起 S1 的判準是**「全世界有沒有別人能做」,不是「這個客戶有沒有別家可選」**。和大（Tesla 台灣獨家減速機，但 Harmonic Drive / 綠的 / 三花都能做）→ **降級**；台光電（M9 CCL ~90% 市佔、技術難複製）→ **留，但理由是技術領先不是客戶獨家**。**疑則降級**：無法證明「別人真做不出來」就拿掉 ⚑。

**Axis 1 · 能力非替代性（主軸）— 全世界沒有別人能在時間內做出來**

- **S1** **全球**今天沒有、且 18-24 個月內也無法 qualify 出第二量產源（能力/IP/良率 gap）。判準是**供應商能力稀缺,不是客戶採購選擇** — 「X 是 Y 的獨家」若其他廠商有能力做（只是 Y 暫時單選）→ 是客戶配置,**S1 不成立**。送樣 / R&D / 規劃中不算第二源。
- **S2** 替換 requalification + ramp 週期 ≥ 18-24 個月（製程整合，非型錄零件可隨插即用）
- **S3** IP / co-design lock — 客戶產品**實體整合**此供應商 IP（NDA / 專利交叉 / 客製光罩 / 共同開發製程）
- **Axis 1 過 = S1 為真 AND（S2 或 S3）**。**疑則降級** — 證不出「別人做不出來」就不標 ⚑。
- **「客戶獨家」本身不是合格證,只是佐證**：唯有伴隨能力獨佔（別人做不出）才算數；單客戶依賴反而是**風險**,在 note 標明,不是 pick 訊號。

**Axis 2 · 市場結構（佐證軸）— 確認鎖喉是結構性、非暫時單一採購**

- **M1** 該家 ≥ 60% **addressable**（排除 China-only 受限供應）市場、且 sustained ≥3 年，或
- **M2** ≤3 家 ≥90% addressable + 結構性 capex / IP / qualification barrier 阻 4th entrant ≥5 年 viable（**structural cartel**，非 competitive oligopoly — 後者客戶 5 年內能 reshuffle）
- **Axis 2 過 = M1 或 M2**
- **「Addressable market」定義**：對非中國 hyperscaler 客戶可實際購買的市場（排除 Empyrean China-only EDA、Yusur China-only NIC 等地緣受限）。同 topic 內口徑一致。
- M2 典範 cartel（兩軸都過的真案例）：HBM-grade DRAM trio（$30B/fab barrier）、EUV mask blank (AGC 59% + HOYA 34%)、BaTiO₃ 粉體 (Sakai + Fuji ~70%)、TC-NCF 若客戶無法 dual-source 時。

**經濟槓桿 gate（必過，沿用 v1.2 Gate C）**：此 segment ≥30% 該公司 revenue **或** pure-play 純玩家 — 否則只是 vulnerability note，不是可投資鎖喉。（注意：節點本身可以是 ⚑，但若該節點的壟斷者是大集團一小 segment〔如 Ajinomoto〕，⚑ 仍成立、但**不得**把該大集團標 💎。）

**Kill Test（最後驗證）**：「客戶能不能在 **12 個月內無 yield / 出貨延遲**地把這家換掉？」
- **NO** → 可標 ⚑
- **MAYBE** → 主表 + drawer note，**不打 ⚑**
- **YES** → 拿掉 ⚑

### 非替代性分（超預算時用來排序、決定誰留）

候選數超過硬預算時，用下式由高到低排序，只留 top N：
```
非替代性分 = 下游停產風險(此節點斷供 → 下游多少 % 產出停, 0-1)
           × 替代 ramp 時間(月 / 24, cap 1.0)
           × 該家對此節點的控制度(% addressable, 0-1)
```
三項都接近滿分才是真單點。被擠掉的候選**在 commit message 列出**（no silent truncation）。

### Critic gate（v1.3 新增 — 寫 ⚑ 與驗 ⚑ 分離）

寫完候選 ⚑ 清單後（Step 1 之後、commit 之前），spawn sub-agent 對抗裁決：

```
Agent({
  description: "Cold-review {topic} ⚑ flags",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are the single-point-critic. 用 v1.3 雙軸框架（Axis 1 非替代性 S1/S2/S3、Axis 2 結構 M1/M2、經濟 gate、Kill Test）對 {topic} 的 N 個候選 ⚑ 逐一判 KEEP / DEMOTE / SPLIT。對每個**強制說出第二供應源或替代品的名字** — 說得出 = DEMOTE，說不出 = 真單點。同時檢查 💎 是否誤標在『第二供應源 / oligopoly 互打的一員 / 大集團一小 segment』。Default to DEMOTE when uncertain。"
})
```

critic 投 KEEP / DEMOTE / SPLIT；SPLIT 由主 agent 最終定奪並在 commit message 註明裁決理由。

### Anti-patterns（容易誤標的陷阱）

1. **Demand-side concentration ≠ supplier ⚑**：TSMC 占 70% 先進邏輯需求是 demand 集中，不是 TSMC 為單點供應商（除非 topic 是把 TSMC 當 supplier 看，如 IC 設計→ Foundry）
2. **Supplier captive to customer ≠ customer-exclusive supplier**：京鼎 80% 營收來自 AMAT 是「供應商依賴客戶」（vulnerability），不是「客戶只能找京鼎」（moat）。要看反向：AMAT 有多 OEM (UCTT / Ichor)，不算 ⚑。
3. **Competitive Oligopoly ≠ Structural Cartel**（最常見混淆）：
   - **不打 ⚑（competitive oligopoly）**：4-6 家加總 >85% 但個別都 <40% + **新進入者 5 年內 commercial 可能**（如 DPU 三強 Nvidia/AMD/Marvell、Retimer 六強 Astera/Credo/Parade/Renesas/Montage/Microchip、SerDes IP 四強 Synopsys/Cadence/Alphawave/Credo）— 客戶能在 12 月內 reshuffle、無結構性鎖
   - **打 ⚑（過 Gate A4 structural cartel）**：≤3 家加總 ≥90% + **結構性 capex / IP barrier 5 年內阻擋 4th entrant**（如 HBM-grade DRAM trio、EUV mask blank duopoly、BaTiO₃ + nano-Ni 雙占、TC-NCF 雙占）— 客戶結構性 locked-in 整個 cartel
   - **快速判別**：問「5 年內會不會有有效第 4 家？」— 不會 → Gate A4；有 → competitive oligopoly
4. **代理商 / 通路商不是真正的鎖喉**：合約模型、客戶可短期切換或自建直購通路。不打 ⚑。
5. **「全球少數能做」≠ 「唯一」**：3+ 家能做就是 oligopoly。不打 ⚑。
6. **「領先 / 第一名」≠ 「壟斷」**：40-60% 是 leader，>75% sustained 才是 monopoly。
7. **「送樣中 / 量產規劃」不算量產**：only commercial mass-production counts for Gate A。

### 4-bucket（分類標籤，非合格判準）

通過 v1.2 嚴格 Gate 後，用以下 4 個 bucket **描述** ⚑ 的性質（filled into `single` field 文字）：

| 子類 | 通常符合哪個 Gate | 範例 |
|---|---|---|
| **近乎獨佔** | A1 ✓ | ZEISS SMT EUV optics、ASML EUV、Lasertec EUV mask 90%、家登 EUV pod ~80%、中砂 鑽石碟 3nm 70% |
| ~~**客戶獨家**~~ | **（v1.5 廢除為合格子類）** | 「X 是 Y 的獨家」**不再**單獨成立 ⚑ — 必須證明伴隨能力獨佔（別人做不出）才用「近乎獨佔/鎖喉點/封裝級單點」描述；只是客戶單選（別人能做）→ 降級為主表 note + 標客戶集中風險 |
| **鎖喉點** | A2 ✓ + B2 ✓ | TSMC CoWoS-L、Broadcom Jericho 4 inter-DC router、NVLink scale-up |
| **封裝級單點** | A2/A3 + B2 ✓ | 健策 CoWoS lid/IHS、Mitsui EUV pellicle ASML license |

> 💎 Top Picks Framework（坐在 ⚑ 節點上的公司如何升 💎）+ 三層 Tier（💎 satellite / 🐘 elephant / 🔒 uninvestable）全文 → 有 💎/🐘/🔒 候選時載入 `references/pick-frameworks.md`。⚑ 判掛旗、pick-frameworks 判投資層級，兩者分工。

## 信心度標註 convention（在 `single` 與 `note` 欄位）

```
single: "客戶獨家 · <主張> （信心度 high · <源 1> + <源 2>）"
single: "客戶獨家（送樣中）· <主張> （信心度 med · <源 1>，待量產確認）"
single: "近獨佔 · <主張> （信心度 high · 多源證實）"
```

具體範本：
```json
// 高信心（雙源 + 法說會）
"single": "客戶獨家 · 波若威 Shuffle Box 已確認進 NVIDIA Spectrum-X CPO 交換器供應鏈，市佔 40-50%（BuBu Research + 2026/3/10 法說會雙源）"

// 中信心（送樣中，未量產）
"single": "客戶獨家（送樣中）· 大立光 TSMC 微稜鏡 collimator 送樣 + AMD COUPE 測試中"

// 高信心（多源報導）
"single": "近乎獨佔 · Himax 為 TSMC COUPE Gen1 + Gen2 唯一 MLA 供應（Hunterbrook + Ming-Chi Kuo 多源證實）"
```

## 輸出步驟

> JSON schema 全文 → Step 1 載入 `references/json-schema.md`；thin HTML template → Step 2 載入 `references/html-template.md`；Step 3/3.5/4/5 機械層全文 → Step 3 起載入 `references/output-plumbing.md`。以下為留在核心的 Step 1 + Step 1.5（掛旗閘）。

### Step 1：寫 `docs/supply-chain/data/{topic}.json`

按 `references/json-schema.md` 的 schema 寫。確認：
- 每個 ⚑ 節點 `single` 欄位有信心度標註
- 每個節點 `sources` ≥1 個權威 URL
- `edges` 中每個 ID 都對應到 `nodes[].id`
- `upstream` / `downstream` 內 ID 也要對應到 nodes

### Step 1.5（v1.3 必做）：spawn single-point-critic 對抗驗 ⚑ / 💎

寫完 JSON 的候選 ⚑ / 💎 後、commit 之前，**強制** spawn `single-point-critic` sub-agent（範本見上方 ⚑ Framework「Critic gate」段），對每個候選跑雙軸 + Kill Test、強制 name 第二源。依裁決：
- DEMOTE → 移除該 node 的 `single`，competition 改回真實 enum（monopoly→oligopoly 等），保留 analysis 文字當主表 note
- SPLIT 且超預算 → 用非替代性分排序，擠掉最弱者
- 💎 mis-assignment（第二源 / oligopoly 一員 / 大集團）→ 移除該公司 `core_business` / 把 `supply_chain_lock` 降 `med`

新 topic JSON 頂層標 `"single_point_framework": "v1.3"`，validator 才會強制硬預算。critic report 可選存 `notes/site-internal/supply-chain/_critic_{topic}_{YYYYMMDD}.md`（repo 內部，不進 published docs/ 樹）。

### Step 2-5：thin HTML template → manifest 翻牌 → hub 入口 → build → commit/push → live URL 驗證

全文載入 `references/html-template.md`（Step 2）＋ `references/output-plumbing.md`（Step 3 翻 topics.json active / Step 3.5 更新 hub index.html 四處 / Step 4 build script + 本機驗證 + commit + push / Step 5 live URL 驗證）。**Step 3.5 hub 入口更新容易漏**（MLCC 踩雷史），index.html 併進 Step 4 git add 清單。

## 品質 Gate（commit 前必查）

| Gate | 檢查項 | Pass 條件 |
|---|---|---|
| **G1: Schema** | JSON parse + 所有 required 欄位齊 | `python3 -c "json.load(...)"` 不報錯 |
| **G2: 引用完整** | 每個 node `sources` ≥1，URL 真實 | 不允許「待補」 |
| **G3: Single-point 雙源** | 每個 ⚑ 節點背後 ≥2 來源（或標明 med 信心度） | analysis 文字明標 |
| **G3.5: v1.3 雙軸 + 預算 + critic** | ⚑ 過 Axis 1 非替代性 ∧ Axis 2 結構；⚑ ≤ max(5, ceil(nodes×0.15))；💎 ≤ 5；single-point-critic 已裁決 | topic JSON 標 `single_point_framework:"v1.3"`，validator 強制 |
| **G4: Edge consistency** | 所有 edges 兩端 ID 都在 nodes[] | audit script 通過 |
| **G5: Stats 一致** | `stats[2].v` 等於實際 `single` 數 | python audit 通過 |
| **G6: 命名** | `single` 文字含 4-bucket 之一 + 信心度標註 | 人工檢視 |
| **G7: stingtao 殘留檢查** | `subtitle` / `analysis` 中不含「本版補齊」「先前漏掉」「客戶獨家單點：...」這種第三方 voice | grep 不到 |
| **G8: TW 中文源** | 至少 30% 的 sources URL 是 .tw / 中文媒體域名 | 確保 TW 視角不缺 |
| **G9: 本機 render** | headless screenshot 看得到 nodes + edges + drawer | 視覺確認 |
| **G10: Live URL** | deploy 後 curl 200 | post-push 必驗 |

## stingtao 殘留 patterns（必砍）

如果從任何外部來源（包括 stingtao API）抓資料當種子，**禁止保留**這些 voice：

- 「本版補齊先前漏掉的...」
- 「獨佔/客戶獨家單點：A、B、C、D...」（這種列舉重複 ⚑ 旗標已表達的資訊）
- 「設計參考 photonic CPO supply chain」
- 任何「我們」「本團隊」「補齊」的口吻

→ subtitle 應該只描述**本 topic 的 thesis 與時機**（量產時點、關鍵客戶、技術轉折）。

## 範例參考

**worked examples**（可直接參考結構）：
- `docs/supply-chain/data/cowos.json` — 3 列 × 31 nodes，半導體製造典型結構
- `docs/supply-chain/data/cpo.json` — 5 列 × 19 nodes，光電混合產業典型結構

讀其中一份 + 看對應的 .html 渲染結果，就能照葫蘆畫瓢做新 topic。

> 預期效益（skill 存在動機）＋ v1.0 已知限制 ＋ 版本沿革（含 v1.2 結構拆分）→ `references/changelog.md`。
