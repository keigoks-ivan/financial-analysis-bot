# industry-analyst v1.4 — Pre-Publish Gate Check（7 Gates）

每份 Industry DD 發布前必跑。Step 8.5 讀取本檔並逐條檢查。

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

## Final Status
✅ ALL GATES PASS - 允許發布
⚠ WARNINGS (4, 5, 6, 7): {list}
❌ BLOCKED at Gate {n}: {reason}
```

---

## 版本歷史
- v1.0（2026-04-19）：基於 8 份 ID peer review 累積建立。核心 Gate 1/2/3 阻斷式，Gate 4-7 warning。
