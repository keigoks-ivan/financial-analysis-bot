---
name: supply-chain-cartographer
description: 建立「產業供應鏈互動地圖」— 把產業鏈拆成節點 × 廠商 × 競爭態勢 × 客戶獨家／關鍵單點的視覺化頁面，與 industry-analyst（ID 表格 dashboard）和 industry-ds（敘述供需循環）並列的第三種產業視角。輸入產業主題（如「HBM」「ASIC」「先進製程」「IC 設計」「人形機器人」），skill 執行多輪 WebSearch / WebFetch 研究（英文 + TW 中文雙語策略），輸出 docs/supply-chain/data/{topic}.json + 一支 thin {topic}.html template，引擎 (engine.css + engine.js) 已存在不需動。row 數量自由（3-6 列），由產業敘事決定；每個 single-point ⚑ 必須引用 ≥2 來源並標註信心度。觸發：使用者說「跑 {topic} 供應鏈地圖」/「{topic} supply chain map」/「畫 {topic} 供應鏈」/「{topic} supply-chain」/「supply-chain {topic}」。
version: v1.0
date: 2026-05-26
---

# supply-chain-cartographer skill v1.0

## 定位

把產業鏈拆解成**互動式視覺地圖**：節點 = 製程環節 / 元件子段 / 客戶層 ; 邊 = 上下游關係 ; 標籤 = 競爭態勢（壟斷 / 寡占 / 紅海 / 高速增長 / 新興萌芽）+ ⚑ 客戶獨家／關鍵單點。

**與 ID / DS 的分工**：
| 視角 | 主要載體 | 適用情境 |
|---|---|---|
| ID（industry-analyst） | 14 章節 HTML，表格 ≥ 70% | PM 快速決策的 dashboard |
| DS（industry-ds） | 11 章節 HTML，敘述 ≥ 80% | 供需循環的深度準備 |
| **本 skill** | 互動式 JSON map | **看「製程節點上誰是脆弱依賴點」**、surface 沒做過 DD 的關鍵小單點 |

三者**可並存**：同 theme 出 ID + DS + supply-chain 三份不衝突。

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

## 工作流（標準 5 輪研究 + 4 步輸出）

### Round 0：先看現況

```
# 1. 確認 topic 在 manifest（不在就要加）
grep '"id": "{topic}"' docs/supply-chain/data/topics.json

# 2. 看既有 topic 範例
ls docs/supply-chain/data/   # cowos.json, cpo.json

# 3. 估計研究時間
- 半導體製造 topic（HBM、先進製程、ASIC）：~60-90 min
- 跨產業 topic（機器人、衛星、軍工）：~90-120 min
```

### Round 1：產業 Overview + 主玩家（4-5 平行 WebSearch）

英文 sources 優先（覆蓋面廣、行業報告多）。

```python
parallel_search([
    "{topic} supply chain 2026 主要玩家 architecture",
    "{topic} market size 2026 2030 IDTechEx Yole forecast",
    "{topic} key technology 鎖喉點 single-source bottleneck",
    "{topic} hyperscaler customer adoption timeline",
    "{topic} TSMC Samsung foundry partner 2026",
])
```

抓出：
- 產業骨架（哪幾個製程環節、產品段）
- 全球 majors（美/日/歐/韓大廠）
- 預期上量時間（2025/2026/2027）
- 關鍵客戶（hyperscaler、AI 晶片廠）

### Round 2：TW 中文供應鏈（5-8 中文 WebSearch）

**這是 stingtao 種子最強、純自研最弱的環節**。必須用中文搜尋找 TW 小型股的客戶獨家。

優先源：
1. **TechNews 科技新報**（technews.tw）
2. **Money Weekly 理財周刊**（moneyweekly.com.tw）
3. **TrendForce**（中文版報導）
4. **Digitimes**（digitimes.com）
5. **工商時報** / **經濟日報**（chinatimes.com / udn.com）
6. **數位時代**（bnext.com.tw）
7. **鉅亨網**（cnyes.com）
8. **Vocus** / **Pocket** / **StatementDog**（個股法說會整理）

```python
parallel_search([
    "{TW player 1} {topic} TSMC NVIDIA 供應鏈 2026",
    "{TW player 2} {topic} 獨家 客戶 送樣",
    "{TW player 3} {topic} 法說 市佔",
    # 通用詞
    "{topic} 台廠 受惠股 供應鏈",
    "{topic} 客戶獨家 鎖喉點 台灣",
])
```

抓出：
- TW 小/中型股對 TSMC / NVDA / AMD 的客戶獨家狀態
- 法說會公開數字（最強信心度來源）
- 送樣 / 驗證 / 量產時程

### Round 3：垂直深度（3-5 平行 WebSearch）

針對 topic 特定的關鍵環節做深掘。例：
- HBM → DRAM 三強市佔 / TC bonder / HBM4 base die
- CPO → DFB 雷射 / III-V epi / MLA / FAU
- ASIC → EDA / 設計服務 / IP / chiplet
- 機器人 → 致動器 / 減速機 / 感測器

```python
parallel_search([
    "{topic} 關鍵環節 1 supplier market share 2026",
    "{topic} 關鍵環節 2 bottleneck monopoly",
    "{topic} downstream demand hyperscaler",
    "{topic} new entrant disruptor 2026",
    "{topic} OFC SEMICON {year} announcement",  # 重大會議
])
```

### Round 4：競爭驗證（2-3 focused WebSearch）

對每個你打算標 ⚑ 的 single-point，**強制找第二個獨立來源**驗證。

```python
parallel_search([
    "{single-point 1} confirmed 2026 sole supplier",
    "{single-point 2} 法說 確認",
    "{single-point 3} second source alternative challenger",
])
```

**規則**：
- 高信心 ⚑：≥2 來源（含 1 個權威源 = 法說會 / 公司公告 / 大行報告）
- 中信心 ⚑：1 個權威源 或 2 個次要源 — 在 single 欄位明標「送樣中 / 待量產 / 單一來源」
- 低信心 ⚑（謠傳 / 單一 substack）：**不要標 ⚑**，放主表但不打旗

### Round 5：DD universe 對照

```bash
# 跑 build script 確保 dd_links.json 是最新
python3 scripts/build_supply_chain_dd_index.py

# 列出本 topic 涵蓋的 ticker 中哪些有 DD
for t in <list of tickers>; do
  f=$(ls docs/dd/DD_${t}_*.html 2>/dev/null | sort -r | head -1)
  if [ -n "$f" ]; then echo "✓ $t → $(basename $f)"; else echo "✗ $t (no DD)"; fi
done
```

→ 沒有 DD 的小型 ticker **不是問題**（supply chain map 就是要 surface 這些 gap）。但要在 commit message 列出來，作為未來 DD 工作的待補清單。

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

## 💎 Top Picks Framework — v1.3 收緊（3 條件 AND + 每 topic 上限 3-5）

> **v1.3 變更**：(1) `supply_chain_lock="tight"` 從「5 訊號任一」改「**≥2 訊號**」；(2) `core_business` 砍掉「管理層公開定位 flagship」敘事後門，只留可查的 ≥20% rev / pure-play；(3) **每 topic 💎 硬上限 3-5 檔**（validator 在 `single_point_framework:"v1.3"` 下強制 ≤5）；(4) **禁止把「第二供應源 / oligopoly 互打的一員 / 大集團一小 segment」標 💎** — 即使所在節點是 ⚑。hbm 三宗實例：Amkor（CoWoS 第二來源）、欣興/南電/景碩（互打 oligopoly）、Ajinomoto（食品集團）。根因都是「把**受惠於鎖喉的人**，誤當**鎖喉本身**」— 兩者投資 thesis 可能都成立，但 supply-chain map 的 💎 只標後者。

⚑ 是「strategic single-point」但**單獨用會把 TSMC / Corning / Broadcom 也標出來** — 那些是「太大太分散，部位推不動 EPS」的大象。投資視角需要更嚴格的篩子：

**isGolden(node, company) = node.single AND company.core_business AND company.supply_chain_lock == "tight"**

三條件同時滿足才是 💎 Top Pick，缺一不可。引擎 (`engine.js`) 自動算交集、在頁面底部 hero section 列表，drawer 公司表的 Top Pick row 加 💎 prefix + 淡金色背景。

**為何用 `supply_chain_lock` 取代之前的 `growth_trajectory`**：YoY 高成長是 momentum 信號（股價已漲完？），不是「供應鏈緊俏」信號。ASML 整體 +15% YoY 但 EUV backlog $30B+ 全球必經，TSMC corporate +25% YoY 但 N2/CoWoS sold out 到 2027 — 這些是「客戶離不開」的結構性 lock，比 YoY 強得多。換成 lock 後 false negatives 大幅下降。

### 判準（明確化、減少主觀）

**`core_business: true` 的條件（任一即過）**：
- 當前 ≥ **20% revenue** 來自此 segment（從財報 / 法說資料）
- **Pure-play** 純玩家（整家公司就做這個，如 Lumentum / Coherent / FOCI / Browave）
- ~~公司管理層公開定位 flagship / 未來主成長引擎~~ **（v1.3 移除：純敘事後門，管理層永遠這樣講；要 forward 例外走下方 Forward-Core 三 hard gate）**

**`core_business: false` 的條件（任一即否決）**：
- 大集團一小 segment（如 TSMC COUPE 占 <1%、Corning AI fiber 占 <20%、Broadcom CPO 占 <5%）
- 主業在別處（味之素 Ajinomoto 雖然 ABF 膜 95% 獨佔，但味之素是大食品/化工集團）

**Forward-Core 例外（用 `core_business_trajectory: "high"`）**：

預設規則：用「**今天**的 segment revenue %」判 `core_business`。但少數高確信案例可開 forward 例外 — 即使 segment 當前 <20% rev，仍可標 `core_business: true` + 加 `core_business_trajectory: "high"` 升 💎。

**三條件必須全過**（任一缺 → 不開 forward 例外）：

1. **管理層公開 guide 具體金額** — 必須是「2027 ASIC > $10 億美元」這種**具體數字** + 時間點，不是「策略佈局」「未來重點」這類空話。
2. **已 signed 多年合約 ≥3 年** — 必須是公開揭露的 binding contract、非 MOU / LOI。
3. **已有 named hyperscaler 級客戶** — Apple / NVIDIA / Google / AWS / Meta / MSFT / OpenAI / Anthropic / Tesla 任一具名 + 公開承諾。

**已批准的 forward-core 案例**：
- **MediaTek 2454 (asic ds-mtk-others)**：(i) 自報 ASIC 2026 >$10 億、2027 target $10B+；(ii) Google TPU v8i 合約鎖到 2031；(iii) Google + AWS 公開命名。當前 ASIC ~10% MTK 營收，三條件全過 → forward 例外升 💎。

**不通過的反例**（即使 narrative 漂亮）：
- **鴻海 2317 humanoid**：humanoid <1% Foxconn 營收、Foxconn 集團 $200B → 要做到 20% 需 humanoid 業務 $40B，數學上 5 年內不可能。
- **Hoya 7741 EUV mask blank**：沒具體金額 guide、沒 signed 合約、客戶經 ASML 中介非直接 named。
- **京鼎 3413 AMAT OEM**：80%+ 已經 AMAT 營收（current core 過），但結構是 supplier-captive（AMAT 可換 OEM）不是 customer-exclusive，是 ⚑ 框架誤用不是 forward 問題。

→ Forward-core **是「升級加分項」**、不是「萬用救生圈」。三條件 hard gate。寧可漏 alpha 也不要 false positive。

**`supply_chain_lock: "tight"` 的條件（v1.3：**≥2 訊號**過 — 舊版「任一即過」太鬆，2026 半導體隨便一家緊俏廠都有「訂單能見 ≥12 月」這條）**：
1. 📅 **訂單能見度 ≥ 12 個月** — ASML EUV backlog $30B+；京鼎 3413 訂單看到 9 個月；Apple 鎖 TSMC N2 三年
2. 🚫 **Sold out / capacity-constrained** — TSMC CoWoS 2026 月產能 120K 仍緊；SK Hynix HBM sold out through 2026
3. 🤝 **多年 exclusive 公開命名** — NVIDIA → Navitas 800V Kyber；Meta → Broadcom 1GW（2031 合約）；Anthropic → Google TPU 3.5GW；Tesla → Samsung AI6 ₩22 兆
4. 💰 **Pricing power demonstrated** — HBM3E → HBM4 ASP \$300 → \$500/stack；EUV pellicle 每片 \$300-500K
5. 🎯 **客戶公開多代 supplier** — AWS → Alchip Trainium 3+4；Apple → TSMC N2/N2P/A16；NVIDIA Rubin → 健策/AVC/Cooler Master/Delta（centralized procurement）

**`supply_chain_lock: "med"`**：有部分鎖喉但沒過 5 訊號（如雙占之一非絕對 lead、補位廠商）
**`supply_chain_lock: "loose"`**：替代源多、紅海、無多年 visibility

### 標註時機

寫 JSON 時，**只在你已有具體證據時才標 `core_business` / `supply_chain_lock`**。Missing 視為 false / unknown — 不會誤判為 💎。寧可漏標也不要錯標。Validator (`scripts/validate_supply_chain_meta.py`) 會驗 enum 值合法（`tight` / `med` / `loose`）。

### 為什麼這個交集有 alpha

- ⚑ 單獨 → 把大象（broad 集團）也標出來
- ⚑ + core_business → 排除「side bet」非核心業務
- + supply_chain_lock=tight → 排除「YoY 高但客戶可換」的雜訊 + 抓「YoY 普通但 backlog 鎖死」的真緊俏（如 ASML）
- 三個 AND → 留下 **真客戶離不開、EPS 推力結構性 high-conviction 的 5-15 檔**

worked example 的 💎 池：
- **HBM（v1.3 re-graded：⚑ 11→5、💎 12→4）**：ASML（EUV 唯一）/ SK Hynix + Micron（DRAM cartel 鎖定者，pricing power + sold-out）/ 欣興 Unimicron（AI-grade ABF #2，NVDA Blackwell 命名、結構性缺口）。砍掉的 8 檔多是 demoted-node 連帶（Lam/Disco/BESI/Onto/GUC）或第二源/oligopoly 互打（Amkor/南電/景碩）。
- **CoWoS（6 檔，**仍 v1.2 未 re-grade**）**：健策 3653 / 家登 3680 / 弘塑 3131 / 新應材 4749 / 萬潤 6187 / Amkor AMKR — 待 v1.3 雙軸 + critic 重評（含 Amkor 是否為第二源的同類檢查）。

這些正好是 sell-side / activist（Hunterbrook、Ming-Chi Kuo、Citrini）反覆推的標的 — 不是巧合，他們用類似框架。

## 三層 Tier — 鎖喉 ≠ 可買（v1.4 起，2026-05-29）

> **動機**：💎 單獨用會把「最不可或缺的節點 owner」誤判 — 因為最深的鎖喉（TSMC、Ajinomoto、ZEISS）往往**太大或不可投資**，反而過不了 💎 的 core_business gate。但「不是 💎」不代表「不重要」。v1.4 把坐在 ⚑ 節點上的公司分三層，讓「最不可或缺」與「最 top pick」**分開呈現**。

| Tier | 判準 | 怎麼評 | 範例 |
|---|---|---|---|
| 💎 **Satellite** | ⚑ 節點 × `core_business:true` × `supply_chain_lock:"tight"` — 鎖喉**推得動該股 EPS**（純玩家 / 純度高） | satellite alpha，部位推得動 | ASML、家登、台光電、ASPEED |
| 🐘 **Elephant** | `node_role:"elephant"` — **它就是鎖喉本身**（壟斷／近獨佔）但身處大型多角化集團，單節點 <~30% 營收推不動 EPS | **core-holding 框架**（估值/整體成長/週期），非 single-point | TSMC、Ajinomoto、Mitsui Chemicals |
| 🔒 **Uninvestable** | `node_role:"uninvestable"` — sole-source 但**買不到純曝險**：未上市，或已是某上市母體的次組件 | 透過母體 / 客戶玩 | ZEISS+Cymer+Trumpf（→ ASML）、Namics、Crusoe |

**標註規則**：
- `node_role` 是 optional enum（`elephant` / `uninvestable`），**只標在 ⚑ 節點**上的公司。
- 與 💎 satellite **互斥**：標了 `node_role` 就不能同時 `core_business:true`+`tight`（validator 強制；標 node_role 時應移除 cb/lock）。
- 💎 satellite **不另設欄位**，仍由 `isGolden()` = `core_business`×`supply_chain_lock` 推導。
- 判斷「elephant vs satellite」的關鍵問句：**「這個鎖喉節點占這家公司營收多少 %？」** ≥~30% 或純玩家 → satellite；個位數 %（大集團一小塊）→ elephant。
- 判斷「uninvestable」：沒有可買的獨立 equity（ticker `—`／私人／已併入母體）。
- engine 在頁尾 `#goldBlock` **分三區渲染**（💎 / 🐘 / 🔒），各自獨立表格與顏色。

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

## JSON Schema

### 頂層

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | ✓ | topic 短代碼，等於檔名（cowos / cpo / hbm…） |
| `tab` | ✓ | tab 文字（短，6 字內：CoWoS / CPO / HBM） |
| `title` | ✓ | 完整中文標題 |
| `subtitle` | ✓ | 1-3 句敘述本 topic 的核心 thesis，**禁止 stingtao 殘留 voice**（如「本版補齊...」）|
| `stats` | ✓ | 3 個 stat cards（節點數 / 廠商數 / single 數 + sub） |
| `rows` | ✓ | row 陣列（3-6 列，由產業決定） |
| `nodes` | ✓ | 節點陣列 |
| `edges` | ✓ | 邊陣列（`[[from_id, to_id], ...]`） |

### Node 欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | ✓ | 唯一短 ID（`eq-` 開頭=設備、`f-` 開頭=主流、`m-` 開頭=材料、`d-` 開頭=demand） |
| `row` | ✓ | 必須對應到 `rows[].id` |
| `col` | ✓ | 1-based 起始 column |
| `span` | ✓ | 占幾個 column（1-3） |
| `kind` | ✓ | `rail` / `stage` / `demand`（影響卡片背景） |
| `name` | ✓ | 中文節點名 |
| `nameEn` | ✓ | 英文節點名 |
| `competition` | ✓ | `monopoly` / `oligopoly` / `redocean` / `highgrowth` / `emerging` |
| `single` | (opt) | 4-bucket 之一的 single-point 描述，含信心度 |
| `desc` | ✓ | 1-2 句說明這環節在做什麼 |
| `marketSize` | (opt) | TAM / 戰略地位短描述（顯示在卡片底部） |
| `growth` | ✓ | CAGR or 短描述（顯示在卡片底部，狀態色） |
| `analysis` | ✓ | 1-3 句競爭態勢分析（drawer 中顯示） |
| `companies` | ✓ | 廠商陣列（≥1） |
| `upstream` | ✓ | `[{id: "..."}]` |
| `downstream` | ✓ | `[{id: "..."}]` |
| `sources` | ✓ | `[{label: "...", url: "https://..."}]` ≥1 |

### Company 欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| `name` | ✓ | 公司名（中英混排 OK） |
| `ticker` | ✓ | Yahoo-style ticker（`2330.TW`、`6146.T`、`AMAT`） |
| `country` | ✓ | ISO 大寫（TW/US/JP/CN/KR/EU/IL/SE/SG/DE/FR/AT/HK/NL/UK/CH/DK/GLOBAL） |
| `share` | ✓ | 市佔短描述（可含數字 % 或描述「TSMC 獨家」） |
| `products` | (opt) | 具體產品線 |
| `note` | (opt) | 1-2 句說明這家在本節點的角色 |
| `src` | (opt) | 該廠商獨家來源 URL（drawer 中顯示 ↗ 小圖示） |
| `core_business` | (opt) | **Top Pick（💎）標註用** — bool；TRUE = 此 segment 是該公司核心業務（≥20% revenue / pure-play / 公司公開定位 flagship）。FALSE 或省略視為「side bet / 大集團一小塊」 |
| `supply_chain_lock` | (opt) | **Top Pick（💎）標註用** — enum `"tight"` / `"med"` / `"loose"`：TIGHT = 5 訊號任一過（≥12 月訂單能見 / sold out / 多年 exclusive 命名 / pricing power demonstrated / 客戶多代 supplier）；MED = 雙占 #2 或補位；LOOSE = 替代源多 / 紅海。**用 lock 取代舊 `growth_trajectory`** 是為了抓真正客戶離不開的供應商（YoY growth 是噪音）。|
| `growth_trajectory` | (legacy) | 舊版欄位，已被 `supply_chain_lock` 取代。仍可標但 isGolden() 不再使用。|

### 範例：

```json
{
  "id": "m-mla",
  "row": "optics",
  "col": 1, "span": 2,
  "kind": "rail",
  "name": "微透鏡陣列 MLA",
  "nameEn": "Microlens Array (MLA)",
  "competition": "monopoly",
  "single": "客戶獨家 · Himax 為 TSMC COUPE Gen1 + Gen2 唯一 MLA 供應（Hunterbrook + Ming-Chi Kuo 多源證實）",
  "desc": "把 PIC grating coupler 出來的散射光收成平行光、再聚焦進光纖核心的微小光學陣列；nanoimprint lithography（NIL）製程。",
  "marketSize": "鎖喉點",
  "growth": "Himax 2028 EPS $3.40e",
  "analysis": "Himax 透過獨家 NIL 製程在玻璃晶圓上做 V-groove + 微透鏡 + 微稜鏡，是 TSMC COUPE Gen1/2 的唯一 MLA 供應；玉晶光在 1.6T 光模組 MLA 已進入美系資料中心客戶供應鏈（不同路線）。",
  "companies": [
    {
      "name": "Himax 奇景",
      "ticker": "HIMX",
      "country": "TW",
      "share": "COUPE Gen1/2 唯一",
      "products": "WLO MLA + V-groove glass wafer (NIL)",
      "note": "與 FOCI 合作 FAU 整合，鎖喉點",
      "src": "https://hntrbrk.com/himax/"
    },
    { "name": "玉晶光 Genius Electronic", "ticker": "3406.TW", "country": "TW", "share": "1.6T MLA 美系 DC", "products": "Pancake Lens 衍生 MLA", "note": "已進美系 DC 供應鏈" }
  ],
  "upstream": [],
  "downstream": [{ "id": "f-assembly" }],
  "sources": [
    { "label": "Hunterbrook: Himax stealth supplier for NVIDIA optics", "url": "https://hntrbrk.com/himax/" },
    { "label": "Ming-Chi Kuo: Himax key AI upstream winner in TSMC COUPE", "url": "https://medium.com/@mingchikuo/himax-emerging-as-a-key-ai-upstream-winner-in-tsmcs-coupe-silicon-photonics-significantly-baf39a9393c9" }
  ]
}
```

## 輸出步驟

### Step 1：寫 `docs/supply-chain/data/{topic}.json`

按上面 schema 寫。確認：
- 每個 ⚑ 節點 `single` 欄位有信心度標註
- 每個節點 `sources` ≥1 個權威 URL
- `edges` 中每個 ID 都對應到 `nodes[].id`
- `upstream` / `downstream` 內 ID 也要對應到 nodes

### Step 1.5（v1.3 必做）：spawn single-point-critic 對抗驗 ⚑ / 💎

寫完 JSON 的候選 ⚑ / 💎 後、commit 之前，**強制** spawn `single-point-critic` sub-agent（範本見上方 ⚑ Framework「Critic gate」段），對每個候選跑雙軸 + Kill Test、強制 name 第二源。依裁決：
- DEMOTE → 移除該 node 的 `single`，competition 改回真實 enum（monopoly→oligopoly 等），保留 analysis 文字當主表 note
- SPLIT 且超預算 → 用非替代性分排序，擠掉最弱者
- 💎 mis-assignment（第二源 / oligopoly 一員 / 大集團）→ 移除該公司 `core_business` / 把 `supply_chain_lock` 降 `med`

新 topic JSON 頂層標 `"single_point_framework": "v1.3"`，validator 才會強制硬預算。critic report 可選存 `docs/supply-chain/_critic_{topic}_{YYYYMMDD}.md`。

### Step 2：寫 thin `docs/supply-chain/{topic}.html`（複製 cowos.html / cpo.html 改 3 處）

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{Topic 完整標題} — InvestMQuest Research</title>
<meta name="description" content="{1-2 句描述 nodes 數 + 單點數 + 核心 thesis}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/engine.css">
</head>
<body data-topic="{topic-id}">

<header class="site">...</header>  <!-- 從 cowos.html 複製，無改動 -->

<main class="shell">
  <div class="crumb"><a href="/">首頁</a> / <a href="/research/">研究</a> / <a href="/supply-chain/">供應鏈地圖</a> / {Topic 完整標題}</div>
  <div class="sc-head">
    <h1 class="sc-title" id="topicTitle"><span class="spark"></span>{Topic 完整標題}</h1>
    <p class="sc-sub" id="topicSub"></p>
  </div>
  <div class="topic-tabs" id="topicTabs"></div>
  <div class="sc-toolbar">
    <div class="legend" id="legend"></div>
    <label class="sc-search">
      <input id="sc-search-input" type="text" placeholder="搜尋節點 / 公司 / 代號…" autocomplete="off">
    </label>
  </div>
  <div class="stats-row" id="statsRow"></div>
  <div class="map-wrap">
    <div class="map-canvas" id="mapCanvas">
      <svg class="edges-svg" id="edges"></svg>
      <div class="grid" id="grid"></div>
    </div>
  </div>
  <div class="def-block" id="defBlock"></div>
</main>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-hidden="true">...</aside>  <!-- 從 cowos.html 複製 -->

<footer class="site">...</footer>

<script src="assets/engine.js"></script>
</body>
</html>
```

→ **3 處修改點**：`<title>`、`<meta description>`、`<body data-topic="...">`、`<crumb>` 與 `<h1>` 的 topic 名 — 其他完全 copy-paste from cowos.html。

### Step 3：翻 `docs/supply-chain/data/topics.json` 中該 topic 的 `active`

```json
{ "id": "{topic}", "tab": "...", "title": "...", "active": true }
```

### Step 3.5：更新 hub 入口頁 `docs/supply-chain/index.html`（**必做、容易漏**）

`index.html` 是 **hardcoded HTML**（不是從 `topics.json` 動態渲染），所以新 topic 的 `passive.html` / `passive.json` / `active: true` 都備齊後，如果不手動補入口，從 https://research.investmquest.com/supply-chain/ 進來看不到連結 — 用戶會問「為什麼沒看到」。歷史踩雷：MLCC commit 230bcff1 漏這一步，靠 bfab4e82 補救。

對於落在 **8 功能模組 × 5 終端市場** 框架內的 topic（多數情況），改 4 處：

1. **Hero meta**（檔頭附近的 `<div class="meta">`）：
   - `<b id="liveCount">N</b>` → N+1
   - `<b id="soonCount">M</b>` → M-1

2. **覆蓋矩陣 cell**（`<div class="matrix">` 內，定位到該 topic 所屬的 row × col 格子）：
   ```html
   <!-- before -->
   <div class="cell lvl-soon"><div class="c-tag"><span class="dot"></span>規劃中</div><div class="c-title">{title}</div><div class="c-sub">{vendors}</div></div>
   <!-- after -->
   <div class="cell lvl-on"><a href="{topic}.html"><div class="c-tag"><span class="dot"></span>已上線</div><div class="c-title">{title}</div><div class="c-sub">{vendors}</div><div class="arrow">→</div></a></div>
   ```

3. **Module 卡片**（`<div class="module-block">` 的 `.card-grid` 內）：
   ```html
   <!-- before -->
   <div class="tcard soon">
     <span class="t-tag"><span class="dot"></span>規劃中</span>
     <h4>{title}</h4>
     <div class="t-en">{title_en}</div>
     <div class="t-vendors">{vendors}</div>
     <div class="t-foot">即將推出</div>
   </div>
   <!-- after -->
   <a class="tcard live" href="{topic}.html">
     <span class="t-tag"><span class="dot"></span>已上線</span>
     <h4>{title}</h4>
     <div class="t-en">{title_en}</div>
     <div class="t-vendors">{vendors}</div>
     <div class="t-foot">查看供應鏈地圖 →</div>
   </a>
   ```

4. **Module 計數**（`<div class="module-head">` 內的 `.mod-count`）：
   - `<b>K</b> 子產業 · <b>X</b> 已上線` → X+1

對於 **跨主題 topic**（robot / leosat / spacedc / siph 等，落在底部「跨主題地圖」section）：只改 hero `liveCount`，並在 `<!-- Topical / cross-cutting maps -->` section 的 `<div class="card-grid">` 內 append 一張 `<a class="tcard live" href="{topic}.html">` 卡片（不用動矩陣與模組計數）。

`index.html` 也要併進 Step 4 的 `git add` 清單。

### Step 4：跑 build script + 本機驗證 + commit + push

```bash
# 重建 dd_links（DD 新增過就要跑）
python3 scripts/build_supply_chain_dd_index.py

# 本機測試
python3 -m http.server 8765 --directory docs &
# 開瀏覽器訪問 http://localhost:8765/supply-chain/{topic}.html
# 或用 chrome headless
"$CHROME_PATH" --headless --window-size=2200,1800 --screenshot=/tmp/sc_{topic}.png "http://localhost:8765/supply-chain/{topic}.html"
pkill -f "http.server 8765"

# JSON schema audit（手寫小 Python 腳本，或拷 cpo audit pattern）
python3 -c "
import json
d = json.load(open('docs/supply-chain/data/{topic}.json'))
node_ids = {n['id'] for n in d['nodes']}
for e in d['edges']:
    assert e[0] in node_ids and e[1] in node_ids, f'edge {e}'
single_count = sum(1 for n in d['nodes'] if n.get('single'))
assert single_count == d['stats'][2]['v'], f'single count mismatch'
print(f'OK: {len(d[\"nodes\"])} nodes / {len(d[\"edges\"])} edges / {single_count} single')
"

# 提交（用 HEREDOC 維持格式）
git add docs/supply-chain/{topic}.html docs/supply-chain/data/{topic}.json docs/supply-chain/data/topics.json docs/supply-chain/index.html
git commit -m "$(cat <<'EOF'
supply-chain: add {Topic} topic — {N} nodes, {K} single-points

<3-5 句說明本 topic 的 thesis、row 結構、最重要的 single-points>

Row structure: {row1} / {row2} / {row3} ...

K single-points (⚑) with confidence levels:
  - {single-point 1}  <bucket>  <confidence>  <evidence>
  ...

DD cross-link coverage: {X} of {N} nodes' companies have ≥1 DD match.
Tickers without DD coverage (candidates for future DD work): <list>

Flipped {topic}.active=true in topics.json.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

git push origin main
```

### Step 5（必）：Live URL 驗證

deploy 完後（GitHub Pages 通常 1-2 min），跑：

```bash
for url in /supply-chain/{topic}.html /supply-chain/data/{topic}.json; do
  echo "$(curl -sI -o /dev/null -w '%{http_code}' https://research.investmquest.com${url}) $url"
done
```

兩個都要 **200**。

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

## 預期效益（為什麼這個 skill 存在）

每個 topic 平均 60-120 分鐘研究 + 30 分鐘寫入 + 10 分鐘驗證 = ~2 小時內完成一份高品質供應鏈圖。

15 個 topic 全部上線後：
- 全站建立**第三種產業視角**（補 ID 表格 + DS 敘述的盲點）
- 每個 topic 平均揭露 5-10 個被市場忽略的 single-point（TW 小型股）
- 自動 cross-link 既有 DD universe，highlight 沒做過 DD 的 ticker 作為 PM 後續工作清單

## v1.0 已知限制 + 未來改進

1. **無 pre-commit validator**（像 dd / id / ds 有 validate_*.py）— 目前靠 commit 前手跑 audit script。v1.1 可加 `scripts/validate_supply_chain_meta.py`。
2. **dd_links.json 沒有 sync hook** — DD 新增/重命名後要記得手動跑 `build_supply_chain_dd_index.py`。可考慮把它整進 `update_dd_index.py` 一起跑。
3. **無 critic gate**（像 id-review）— 目前靠雙源規則 (Gate G3) 自我約束。v1.1 可加 spawn sub-agent 抽查單點主張。
4. **Topic 之間沒交叉**（HBM 的 TSMC 跟 CoWoS 的 TSMC 是同一個節點概念但獨立 JSON）— 可接受重複，每個 topic 從自己視角描述 TSMC 角色。

→ 這些都是「能做更好但目前不阻斷」的 nice-to-have，v1.0 不處理。
