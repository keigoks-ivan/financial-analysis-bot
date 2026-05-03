# industry-analyst v1.7 — Pre-Publish Gate Check（10 Gates）

每份 Industry DD 發布前必跑。Step 8.5 讀取本檔並逐條檢查。

v1.7（2026-05-03）相對 v1.6 的差異：新增 Gate 9（§0.7 PM Implication Existence + Conviction Consistency），要求每份 ID 必含 §0.7 綠色 PM 行動結論段，conviction pill 需與 §11/§8 一致。觸發自 2026-05-03 ID_AIDataCenter v1.1 patch（commit f1c450b）——user 要求把臨時加入的 PM Implication block 升格為所有 ID 的標準必填段。

v1.6（2026-04-27）：新增 Gate 8（id-meta JSON Validation）。
v1.5（2026-04-21）：新增 Gate 2.1（Thesis Cornerstone Fact Verification）+ Gate 3.1（Cross-ID Thesis Bias Detection）。

---

## Gate 1 [必備 / 阻斷]｜Core Ticker Financials Refresh（< 60 天）

**規則**：所有 🔴 核心 ticker 的最新公告季度財報必須在發布日前 60 天內。

**檢查步驟**：
1. 列出 §11 所有 🔴 核心 ticker
2. 對每檔 → 查最近公告的 quarterly earnings release 日期
3. 若 `(發布日 - earnings 日) > 60 天`：
   - **阻斷發布**
   - 列出該 ticker 名稱 + 需查的最新季 + 預期公告日

**典型 fail 情境**：
- 報告發布 4/19，ticker Q 結束 3/18（30 天前已公告）但 skill 仍用 Q1 舊數據
- 報告引用「Q × 4」推估而非最新 actual

---

## Gate 2 [必備 / 阻斷]｜Event-Triggered Thesis Refresh（< 14 天）

**規則**：§12 Non-Consensus thesis 引用的事件性 data point，必須在發布日前 14 天內重新檢索最新狀態。

**事件性 data point 定義**：
- 具體 yield 數字（"Samsung SF2P 70% yield"）
- 具體訂單 / 簽約（"Intel 18A 無外部客戶"）
- backlog 絕對值（"GEV $135B backlog"）
- 併購 / 股權狀態（"AMAT 併 BESI 傳聞"）
- 產能 sold out / 量產時序（"Samsung HBM4 Feb 2026 量產"）

**檢查步驟**：
1. 掃 §12 三條 thesis 的「分歧事實」與「證偽條件」段落
2. 標註每條為 `[event-triggered]` 或 `[structural]`
3. 對 event-triggered → WebSearch 最近 14 天是否有更新
4. 若最新資料矛盾：
   - 降信心級別（高 → 中、中 → 低）
   - 或直接重寫 thesis
   - 若時間不夠重寫 → **阻斷發布**

**典型 fail 情境**：
- LEN ID 引用 Samsung SF2P 70%（1 月舊報導），但 4/14 TrendForce 已更新為 SF2 55%
- AP ID 寫「AMAT/LRCX 併 BESI 傳聞」，但 AMAT 2025-04 已持股 9%

---

## Gate 2.1 [必備 / 阻斷 · v1.5 新增]｜Thesis Cornerstone Fact Verification

**規則**：§12 每條 thesis 的「核心分歧事實」必須獨立 WebSearch 最新狀態，特別針對含有「獨家」「首家」「唯一」「only」等定性的 claim 逐一驗證。

**為何新增**：
ID_Transformers v1.4 發生的「Eaton 800V DC 獨家 co-design」錯誤是典型案例 — Gate 2 確實檢查了 Eaton Beam Rubin DSX 公告 14 天內正確，但未驗證「是否真的獨家」這個 thesis 基石 claim。實際狀況：NVDA MGX 800V DC 官方 14+ 家夥伴（ABB、Delta、Schneider、Vertiv 等），Eaton 是 top 3 而非獨家。此類錯誤不是 data 過期，是 cornerstone 定性從未被獨立驗證。

**檢查步驟**：
1. 掃 §12 每條 thesis，圈出所有含「獨家」「首家」「唯一」「only」「first」「exclusive」「sole」「lock-in」「壟斷」等詞的 claim
2. 對每條 → 獨立 WebSearch：
   - `"{相關技術或事件}" partners list` 或
   - `"{相關技術或事件}" ecosystem OR alliance OR consortium`
   - 確認「除了該公司，還有誰也有類似地位」
3. 若發現 ≥ 2 家其他玩家同樣定位：
   - 改寫為「結構性優勢」「top 3 玩家之一」等非獨家措辭
   - 重新評估信心級別（高→中）
   - 重新評估估值敏感度（+5-8x PE → +2-3x）
   - 重新定義證偽條件（原條件若已被其他玩家進入滿足，需改寫）
4. 若 thesis 作者堅持「獨家」定性：
   - 必須在 thesis block 明確列出「被考慮但排除的競爭玩家」+「為何它們不算同級」
   - 無此防禦 → **阻斷發布**

**典型 fail 情境**：
- Transformers ID「Eaton 獨家 co-design NVIDIA 800V DC」— 實際 14+ 家夥伴
- 若未來 SiPho/CPO ID 寫「TSMC COUPE 獨家」但 Intel / Samsung 也在做
- 若未來 Glass ID 寫「LPKF LIDE 唯一」但 NEC / Disco 也有類似技術

**輸出格式**（在 pre_publish_report 內）：
```
## Gate 2.1: Thesis Cornerstone Fact Verification
Thesis 1 cornerstone: "{關鍵 claim}"
  → WebSearch 查 ecosystem 玩家 → {發現結果}
  → 結論：✅ 獨家驗證 / ⚠ 需改寫 / ❌ 阻斷
```

---

## Gate 3 [必備 / 阻斷]｜Cross-ID Reconciliation

**規則**：同批次發布的所有 ID，共用數字、ticker 評級、關鍵事實必須一致。

**需 reconcile 的項目**：
- 共用 ticker 的核心財務數字（NVDA DC Rev、AVGO AI Rev、Credo Rev 等）
- 共用事實（Rubin Ultra stack、AI capex 總和、CoWoS 分配）
- Ticker 評級（🔴/🟡/🟢 在多份 ID 出現必須一致）
- TAM 數字（避免 AI DC ID 和 Liquid Cooling ID 的「液冷 2026 TAM $4-5B vs $6.4B」類似情境）

**檢查步驟**：
1. 掃所有待發布 ID 的 §4 SOM 表 + §6 玩家清單 + §11 關聯個股
2. 對每檔共用 ticker → 列所有 ID 的核心數字
3. 若 inconsistency：
   - 數字差 > 10% → **阻斷發布**
   - 評級不一致 → **阻斷發布**
4. 輸出 reconciliation report 並修正

**典型 fail 情境**：
- 兩份 ID 對同一檔 ticker 給不同評級（LITE 在 Networking ID 是 🟢、在 SiPho 是 🟡）
- 液冷 TAM 在 AI DC 和 Liquid Cooling 數字差 40%

---

## Gate 3.1 [重要 / warning · v1.5 新增]｜Cross-ID Thesis Bias Detection

**規則**：跨 ID 檢查同一 ticker 的「定性偏差」— 若某 ticker 在多份 ID 被定性為「獨家」「首家」「領先」「lock-in」，觸發 red flag 並要求獨立驗證每份 ID 的 claim 是否基於相同錯誤來源。

**為何新增**：
peer review 發現 AI DC ID 和 Transformers ID 對 Eaton 有同一 cross-ID bias（兩份 ID 都誇大 Eaton 在 800V DC 的獨占地位）。這不是兩個獨立錯誤，是一個 common mistake 重複出現。Gate 3 reconciliation 只看「數字是否一致」，沒抓到「定性是否同樣錯誤」。

**檢查步驟**：
1. 列出 cross-ID ticker 定性 claim：
   - 所有在 ≥ 2 份 ID 提及的 ticker
   - 針對每檔，列出各 ID 對它的「角色描述」（從 §6 玩家矩陣 + §12 thesis 段）
2. Red flag 觸發條件：
   - 同一 ticker 在 ≥ 2 份 ID 都出現「獨家」「首家」「lock-in」類定性
   - 同一 ticker 在 ≥ 2 份 ID 都被歸為「最大受益者」
3. 若 red flag 觸發：
   - 套用 Gate 2.1 獨立驗證（WebSearch ecosystem 玩家清單）
   - 若錯誤成立 → 修正所有相關 ID 的定性（不只是當前發布的那份）
   - 若錯誤不成立 → 在 pre_publish_report 註記「cross-ID 定性一致且事實驗證通過」
4. Warning 不阻斷發布，但必須在 report 明確列出所有 red flag

**典型 fail 情境**：
- Eaton 在 AI DC ID 和 Transformers ID 都被寫成「NVDA 獨家 co-design」（實際 14+ 家夥伴）
- 若未來 Alchip 在 AP ID、Hybrid Bonding ID、AI ASIC ID 都被寫成「AWS Trainium 3 唯一 backend partner」— 需驗證是否多源化

**輸出格式**：
```
## Gate 3.1: Cross-ID Thesis Bias Detection
Ticker: Eaton (ETN)
  - AI DC ID：「Boyd Thermal 後 800V DC co-design」
  - Transformers ID：「Eaton + NVIDIA 獨家 SST co-design」
  → Red flag 觸發（兩份 ID 都說獨家）
  → 獨立驗證：NVDA 14+ 家夥伴 → ❌ 定性錯誤
  → 修正：AI DC ID + Transformers ID 同步改寫為「top 3」
```

---

## Gate 4 [重要 / warning]｜Catalyst & Falsification Status Check

**規則**：§10.5 Catalyst Timeline 中所有日期早於發布日的條目，必須標示「已發生」並評估結果；§13 Falsification Test 條件若已觸發或已越過，必須明確標示。

**檢查步驟**：
1. §10.5 掃所有日期 < 發布日的 catalyst
   - 已發生 → 標 ✅「已發生，結果：{brief}」
   - 未標示 → warning
2. §13 每條閾值
   - 已觸發（thesis 破） → 紅字警示
   - 已強烈越過（thesis 強化） → 綠字確認
   - 未評估 → warning

**典型 fail 情境**：
- HBM ID §10.5「2026-02 Samsung HBM4 Feb 量產」標成「未來事件」但實際上已發生且 Samsung 未如期
- §13「Credo 季 revenue < $250M」但 Q3 FY26 已達 $407M 卻沒標「強烈越過」

---

## Gate 5 [重要 / warning]｜Unit & Scope Consistency

**規則**：ASP、BOM、Revenue 等關鍵數字必須宣告單位與口徑。

**檢查項目**：
- ASP 單位：`$/wafer` vs `$/stack` vs `$/GB` vs `$/unit`
- Revenue 口徑：全年 / 季度 / annualized run-rate
- 營收 scope：segment / AI-only / total company
- 百分比：必須有 source 或降級為定性描述

**檢查步驟**：
1. 報告開頭必須有 unit glossary（§0 TL;DR 前或後）
2. 所有百分比抽樣檢查 source
3. Revenue 數字附註時間範圍（"FY26" vs "Q4 FY26" vs "annualized"）

**典型 fail 情境**：
- HBM ID 寫 HBM ASP "$20 → $25 → $35 per GB" 但沒宣告 per-stack 還是 per-GB
- §5 議價權「NVDA 45% / TSMC 30%」無 source

---

## Gate 6 [重要 / warning]｜Cross-ID Layer Disambiguation

**規則**：同一主題跨多份 ID 出現時，必須明確區分層次。Ticker 評級在跨 ID 時必須一致。

**常見需分層主題**：
- **CPO**：switch-level（2026 已商用）vs chip-to-chip（2028+ Feynman）
- **UALink**：規格完成（2025 H2）vs hardware ramp（2026 H2）vs 商用（2027+）
- **Intel 角色**：foundry 客戶 vs GPU 設計商 vs 下游封裝
- **AVGO AI Revenue**：AI-only networking vs AI ASIC vs AI total

**檢查步驟**：
1. 掃同批次 ID 是否有 overlap 主題
2. 對每 overlap 主題 → 確認各 ID 明確標層次
3. Ticker 評級跨 ID 比對（讀 `references/ticker_ratings.md`）

---

## Gate 7 [重要 / warning]｜Sub-Topic ID Value-Add Rule

**規則**：子題 ID（如 Liquid Cooling vs 母題 AI DC、SiPho/CPO vs 母題 Networking）必須有獨立 value-add，不能只重複母題 + 加幾檔 non-obvious。

**檢查方式**：
產出 sub-topic value-add matrix：
```
| 面向 | 母題 ID 涵蓋度 | 子題 ID 新增深度 |
|:---|:---|:---|
| 技術 | 母題寫幾段 | 子題必須 deep dive |
| TAM | 母題合併數字 | 子題必須拆分細項 |
| 玩家 | 母題列主要 | 子題必須加次要玩家 |
| Thesis | 母題的 thesis | 子題必須有獨立 thesis |
```

若「子題新增深度」全空 → 子題無存在必要，**建議合併回母題**。

**典型 fail 情境**：
- Liquid Cooling ID 大部分內容與 AI DC ID 重複，only 多了 Chemours 等 non-obvious → value-add 不足

---

## Gate 8 [必備 / 阻斷 · v1.6 新增]｜id-meta JSON 區塊存在且通過 strict 驗證

**規則**：每份 ID HTML 的 `<head>` 內必含 `<script id="id-meta" type="application/json">{...}</script>`，且該 JSON 通過 `scripts/validate_id_meta.py` strict 驗證（必填欄位齊全、enum 值合法、`oneliner` ≤ 200 chars、`related_tickers` 結構正確）。

**為何新增（v1.6, 2026-04-27）**：
2026-04-27 連 11 份新 ID（AerospaceMetals / CommercialAerospace / DefenseAerospaceUpgrade / EdgeAI / FoundryGeography / HeavyMachineryMining / HumanoidIndustrialRobotics / IndustrialAutomation / ProductivityCopilot / TokenEconomics / GlobalLuxury）漏了 id-meta 區塊，CI `Validate DD + ID metadata` workflow strict gate 全部 fail，使用者收到連續失敗信件。根因：`templates/html_template.md` 骨架未列 id-meta，QC-I14.5 只在 QC 列表（事後檢核），缺乏 pre-publish blocking gate。本 Gate 把 id-meta 從「QC 提醒」升格為「阻斷式 publish gate」。

**檢查步驟**：
1. 執行 `python3 scripts/validate_id_meta.py docs/id/ID_{Theme}_{YYYYMMDD}.html`
2. exit code != 0 → **阻斷發布**，列出缺漏 / 違規欄位
3. 常見 fail：
   - 沒有 `<script id="id-meta">` 區塊（漏寫）
   - `oneliner` 超過 200 chars（沒裁切，把 §0 整段塞進去）
   - `ai_exposure` 用了預設 🟡 但語意上應該是 🟢/🔴（warning，不阻斷；發布前人工調整）
   - `related_tickers` 為空陣列且非 cross-cutting 主題

**典型 fail 情境**：
- skill 從 html_template 複製骨架但忘記填 id-meta JSON 內容 → block
- backfill 工具產的 oneliner 是 §0 截斷段 → block（length > 200）

**輸出格式**：
```
## Gate 8: id-meta JSON Validation
$ python3 scripts/validate_id_meta.py docs/id/ID_XXX_YYYYMMDD.html
{exit code, errors}
✅ PASS / ❌ FAIL — {缺漏欄位列表}
```

---

## Gate 9 [必備 / 阻斷 · v1.7 新增]｜§0.7 PM Implication 存在 + conviction 一致性

**規則**：每份 ID HTML 的 §0 與 §1 之間必須存在 `<h2>§0.7 Portfolio Implication（PM 級行動結論）</h2>` 及對應的綠色 `judgment-card`（`background:#F0FDF4;border-left:4px solid #16A34A`），且內容必須通過以下一致性查驗。

**為何新增（v1.7, 2026-05-03）**：
2026-05-03 ID_AIDataCenter v1.1 patch 由 user 臨時加入綠色 PM Implication block（commit f1c450b），user 認可並要求改為每份 ID 的標準段落。核心理由：§11 conviction tier / §8 de-rating window / §13 falsification metric 這三個判斷層完成後，PM 的行動結論必須在同一文件明文化——否則讀者得自己從三個不同章節拼湊，增加誤讀風險。

**檢查步驟**：

1. **存在性查驗**（阻斷）
   - HTML 中搜尋 `§0.7 Portfolio Implication`（或 `id="s0-7"`）
   - 搜尋 `background:#F0FDF4` + `border-left:4px solid #16A34A`
   - 缺任一 → **阻斷發布**：「§0.7 PM Implication section missing」

2. **五 bullet 完整性**（阻斷）
   - 確認存在以下五個 `<strong>` 標籤的 bullet：
     - `thesis 方向`
     - `個股 conviction tier 變化`
     - `關鍵新監測點`
     - `multiple / 估值 / 週期定位風險`（允許近似詞）
     - `Entry 時機`
   - 任一 bullet 缺失 → 阻斷

3. **j-logic 四行動**（阻斷）
   - 確認 `.j-logic` div 存在，且包含 `①`、`②`、`③`、`④` 四個行動符號
   - 缺少任一符號 → 阻斷

4. **conviction pill 一致性**（warning）
   - 讀取 `<span class="j-conf">` 內的 conviction 值（high/mid/low）
   - 對比 §11 🔴 ticker 數量：
     - ≥ 2 個 🔴 且 §12 verdict 傾向 INTACT → 預期 `high`；若標 `low` → warning
     - 0 個 🔴 → 預期 `low`；若標 `high` → warning
   - Conviction 不一致 → warning（不阻斷，但必須在 report 說明）

5. **ticker 點名查驗**（warning）
   - `個股 conviction tier 變化` bullet 中必須出現至少一個 ticker symbol（大寫英文字母組合，如 NVDA、AVGO、TSMC）
   - 若只寫「部分核心股」「相關個股」等泛語 → warning

**典型 fail 情境**：
- 整份 ID 缺 §0.7（舊格式或未跑 Step 7.5）→ 阻斷
- §0.7 只有 3 條 bullet，漏寫 Entry 時機 → 阻斷
- j-logic 只列 ①②③，沒有 ④ → 阻斷
- conviction 標 `high` 但 §11 無任何 🔴 ticker → warning

**輸出格式**：
```
## Gate 9: §0.7 PM Implication Existence + Conviction Consistency
§0.7 block exists: ✅ / ❌ MISSING
Five bullets: ✅ all present / ❌ missing: {bullet names}
j-logic 4 actions: ✅ / ❌ missing: {①②③④ which absent}
Conviction consistency: ✅ / ⚠ {explain mismatch}
Ticker name-check: ✅ / ⚠ {no ticker found}
→ Gate 9: ✅ PASS / ❌ BLOCKED / ⚠ WARNED
```

---

## 輸出格式：pre_publish_report.md

每次 gate check 產出一份報告：

```markdown
# Pre-Publish Gate Report — {ID_Name} v{version}
發布日：{date}

## Gate 1: Core Ticker Financials
✅ PASS / ❌ FAIL
- NVDA Q4 FY26（2026-02-25）在 60 天內 ✅
- BESI FY25（2026-02-19）在 60 天內 ✅

## Gate 2: Event-Triggered Thesis
✅ PASS / ❌ FAIL
- Thesis 1 [event]：Samsung yield 55% (2026-04-14 TrendForce 最新) ✅
- Thesis 2 [structural]：not checked ✅

...

## Gate 8: id-meta JSON Validation
✅ PASS / ❌ FAIL — {缺漏欄位列表}

## Gate 9: §0.7 PM Implication Existence + Conviction Consistency
§0.7 block exists: ✅ / ❌ MISSING
Five bullets: ✅ all present / ❌ missing: {bullet names}
j-logic 4 actions: ✅ / ❌ missing: {①②③④ which absent}
Conviction consistency: ✅ / ⚠ {explain mismatch}
→ Gate 9: ✅ PASS / ❌ BLOCKED / ⚠ WARNED

## Final Status
✅ ALL GATES PASS - 允許發布
⚠ WARNINGS (4, 5, 6, 7): {list}
❌ BLOCKED at Gate {n}: {reason}
```

---

## 版本歷史
- v1.0（2026-04-19）：基於 8 份 ID peer review 累積建立。核心 Gate 1/2/3 阻斷式，Gate 4-7 warning。
- v1.5（2026-04-21）：基於 ID_Transformers v1.4 peer review 發現新增 2 個 gate。Gate 2.1 Thesis Cornerstone Fact Verification（阻斷）— 針對「獨家 / 首家 / 唯一」類 claim 必須獨立 WebSearch 驗證 ecosystem 玩家；Gate 3.1 Cross-ID Thesis Bias Detection（warning）— 跨 ID 同 ticker 的「定性偏差」要 red flag 並獨立驗證。
- v1.6（2026-04-27）：新增 Gate 8（id-meta JSON 必要區塊 + strict validator）。
- v1.7（2026-05-03）：新增 Gate 9（§0.7 PM Implication 存在 + conviction 一致性）— 源自 ID_AIDataCenter v1.1 patch。
