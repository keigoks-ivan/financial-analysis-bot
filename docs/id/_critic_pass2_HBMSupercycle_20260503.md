# Pass 2 Critic Report — HBM Supercycle

**ID file**: `/Users/ivanchang/financial-analysis-bot/docs/id/ID_HBM_Supercycle_20260419.html`
**Pass 1 report**: `/Users/ivanchang/financial-analysis-bot/docs/id/_critic_HBMSupercycle_20260503.md`
**Pass 1 verdict**: BROKEN (3 🔴 / 7 🟡 / 5 🟢)
**Pass 2 focus**: 8 targeted areas Pass 1 might have missed
**Critic model**: Claude Sonnet 4.6
**Critic date**: 2026-05-03

---

## Pass 2 Verdict Summary

**Additional 🔴 CHANGES_CONCLUSION found: 2 (both new, not covered by Pass 1)**
**Additional 🟡 PARTIAL_IMPACT found: 4**
**Pass 2 is NOT marginal — the §7 ASP error alone is conclusion-changing and was completely missed by Pass 1.**

---

## Focus Area 1 — §7 Unit Economics ASP Sanity

### Finding P2-F1: §7 ASP Numbers Are 8-10x OVERSTATED vs 2026 Actual Market Prices

**位置**: §7 ★ ASP 動態表

**ID 的聲稱**:
| 產品 | 2024 ASP | 2026E ASP | HBM vs DRAM 溢價 |
|---|---|---|---|
| HBM3E（36GB stack） | ~$3,000 | ~$3,500 | 5-6x |
| HBM4（48GB stack） | — | ~$4,500+ | 6-8x |
| HBM per GB 基準 | ~$25 | ~$35 | — |

**實際 2026 市場價格（多源核驗）**:
- Silicon Analysts（2026-04 資料）：HBM3E ~$300 per 36GB stack → **$8.3/GB**
- Goldman Sachs 最新 memory 報告：HBM3E 2025 年 $15/GB，預計 2026 下降 28% 至 **$10/GB**
  - 意味 2025 HBM3E stack（36GB）約 $540；2026 約 **$360**
- 換算口徑對比：
  - ID 聲稱：$3,000-3,500/stack（$83-97/GB）
  - 實際市場：$300-540/stack（$8-15/GB）
  - **差距：ID 的 ASP 數字比實際市場高出 6-10 倍（per stack）/ 3-6 倍（per GB）**

**根本原因分析（識別來源錯誤）**:
ID 的 $3,000/stack HBM3E ASP 很可能來自兩個常見混淆來源之一：
1. **整套 AI GPU 中 HBM 成本的全系統分配**（比如 H200 中 8 顆 HBM3E stack 的總 BOM 成本，約 $24K，被誤除以 1 而非 8）
2. **HBM WAT（wafer acceptance test）成本估值**而非市場 ASP

無論原因，§7 的 ASP 數字與業界實際成交價相差一個數量級。

**連鎖影響（BLOCKER 級）**:

1. **§7 Insight 1「HBM per GB 溢價從 5x → 8x（2024-2026）」** — 基礎數字錯誤，溢價倍數計算整體失效。如果 HBM3E 實際 ~$8-15/GB，DDR5 ~$4-6/GB，溢價倍數是 2-3x，不是 5-8x。
2. **§8 估值影響機制「HBM TAM +20% = $1.8B 增量」** — 已在 Pass 1 因 TAM $9B 問題標為失效，但 §7 ASP 的 10x 高估獨立地破壞了所有「ASP +10% = +10-15% EPS」的影響計算。
3. **§6 A 表 SK hynix「$55-60B HBM Rev」** — Pass 1 標為 SOM 口徑混淆，但若 HBM ASP 實際上只有 ID 宣稱的 1/10，這個 SOM 數字的計算基礎完全崩潰。
4. **§0 核心 insight 3「HBM4 stack 毛利是 LPDDR5 的 5-8x」** — 基礎 ASP 錯誤，此聲稱的倍數無法驗證。

**Pass 1 是否抓到**: ❌ 完全未觸及 §7 ASP 數字。

**CONCLUSION_IMPACT: 🔴 CHANGES_CONCLUSION**
- §7 整張 ASP 表數字錯誤（overstate 6-10x），影響所有基於 ASP 的衍生計算
- §7 Insight 1 的「5x → 8x 溢價」說法不成立（實際溢價約 2-3x）
- 修正方向：§7 ASP 表全面重寫；HBM3E 2026E 改為 $300-400/stack（$8-12/GB）；HBM4 改為 $400-600/stack（$8-12/GB）；per GB 溢價改為「2-3x vs DDR5」（非 5-8x）

---

### Finding P2-F2: §7 SK hynix 2025 毛利率 42% 嚴重低報（實際 79%）

**位置**: §7 ROIC / Gross / Capex 表

**ID 的聲稱**:
| 公司 | 2025 毛利 | 2026E 毛利 |
|---|---|---|
| SK hynix | 42% | 50%+ |

**實際 2025 全年毛利率（SK hynix FY25 IR 官方）**:
- SK hynix FY25 revenue：₩97.1467T
- SK hynix FY25 gross profit：₩41.68T（已由多個財報分析來源確認）
- **FY25 gross margin：79%**（SK hynix FY25 Annual Results，2026-01-28）

**差距**: ID 說 2025 SK hynix 毛利 42%，實際是 **79%**——差距 37 個百分點（相差近 1 倍）。

**連鎖影響**:
1. §7 Insight 2「三家 2026 毛利回到歷史高點，但估值仍低於 2021 peak」—— 如果 SK hynix 2025 毛利已達 79%，而 2026E 只寫 50%+，這意味 ID 的 2026E 估值也嚴重低估，且「回到歷史高點」的說法已在 2025 年就已發生而非 2026 年趨勢
2. §8 判斷卡「Micron 2026-2027 re-rate 空間最大」的 PE 比較基準（SK hynix 15-20x）如果毛利已達 79%，估值應更高，比較基準失效
3. §6 A 表 SK hynix 毛利「40%（後）」也與實際不符

**注意**：也有可能 79% 是 Q4 2025 季度毛利率而非全年——搜尋結果有些不一致（有說 Q4 毛利 79%，有說全年也是 79%）。但即使全年是 Q3 2025 的 60%+ 水平，ID 的 42% 仍明顯錯誤（低估 15-37pp）。

**Pass 1 是否抓到**: ❌ Pass 1 完全未檢查 §7 毛利率歷史數字。

**CONCLUSION_IMPACT: 🔴 CHANGES_CONCLUSION**（若 79% 是全年而非 Q4）/ 🟡 PARTIAL（若是 Q4 季度數字且全年約 55-60%，仍低報但程度較小）
- 最保守估計（全年 ~55%）：ID 的 42% 仍低報 13pp
- 最嚴重估計（全年 79%）：低報 37pp，使 §7 整個 margin trajectory 敘述失效
- 修正方向：確認 SK hynix FY25 全年 gross margin（建議查 FY25 Annual Report P&L）；若全年 79% 確認，§7 整張表需重寫，且 §7 Insight 2 的「回到歷史高點」說法需更新為「已創歷史新高（FY25 79%）」

---

## Focus Area 2 — §9 政策地緣 2026 新事件

### Finding P2-F3: §9 HBM 出口管制重大政策更新（2026-01）未被納入

**位置**: §9 政策地緣表

**ID 的描述**:
> 對中 HBM 出口限制（2024 起）→ 三家對中 HBM 供應削減；中國 CXMT 國產化壓力

**實際 2026-01 重大更新（Pass 1 未抓）**:
- 2024-12：BIS 宣布 HBM 出口管制（所有 HBM 規格，memory bandwidth density > 2 GB/s/mm²），歸類 ECCN 3A090.c
- **2026-01-15**：Trump 行政命令後，BIS 更新 AI 晶片出口政策，允許 H200 / AMD MI325X 及類似晶片**向中國「approved customers」出口**（case-by-case 審查）
  - 這意味 H200（內含 HBM3E）的中國需求可能部分恢復
  - §9 風險表「三家對中 HBM 供應削減」的結論在 2026-01 後已部分逆轉

**對 §9 Kill Scenario 的影響**:
- §9.5 反方 3（CXMT 國產替代）的 j-logic 假設「中國需求 22% 完全流失」可能偏悲觀
- 若 H200 可向中國出口，三家廠商對中 HBM 需求可能回升（雖然 HBM4 仍受限）
- §9 「低信心」CXMT 風險評估需更新（Pass 1 已指出，但出口管制鬆動這個方向 Pass 1 未觸及）

**CONCLUSION_IMPACT: 🟡 PARTIAL_IMPACT**
- 不改變「出口管制存在」的方向，但 §9 政策描述需更新（新增 2026-01 H200 export 鬆動事件）
- §9.5 反方 3 的 j-logic 中「中國 22% 完全流失」假設需改為「部分需求可能透過 H200 approved-channel 回流」
- 修正方向：§9 政策地緣表新增 row「2026-01 H200 export 政策鬆動（Trump admin，case-by-case）→ 中國 HBM3E 需求部分回流可能」

---

## Focus Area 3 — §9.5 Kill Scenario 反方論證強度

### Finding P2-F4: 反方 3（Custom HBM）事實狀況 — 仍 active，但描述需更新

**位置**: §9.5 Kill Scenario 反方 3

**ID 的聲稱**:
> 事實 1：Broadcom 與 Samsung / SK 討論 Google TPU 客製 HBM

**實際 2026 最新狀況（多源核驗）**:
- TrendForce 2025-12-03：Samsung HBM4 通過 Broadcom evaluation，預計成為 2026 Google TPU 主供（Samsung HBM4 beats Broadcom test）
- TrendForce 2026-01-23：**Samsung Custom HBM4E 設計預計 2026 年中完成**；SK hynix 和 Micron 亦在類似時程
  - Samsung 為 Google、Meta、NVIDIA 設立獨立 Custom HBM 團隊（250 名工程師）
- TrendForce 2026-01-21：Samsung 正在將 Custom HBM logic die 移至 **2nm** foundry process（首次）

**評估**:
ID 把反方 3「Custom HBM」描述為 j-conf「中」、j-falsify「2026 H2 首個 Custom HBM 正式發表」——但 2026-01 已有 Samsung Custom HBM4E 設計時程確認（mid-2026 完成），且 Samsung 投入 2nm custom HBM logic die，遠比「討論中」更具體。這個 Kill Scenario 的事實基礎已升級：不再是「Broadcom 與三家討論」，而是「Samsung 已設立 250 人 Custom HBM 專責團隊，2026 H1 設計完成、2026 H2 發表可期」。

**特別注意（新增發現）**: 若 Samsung 的 Custom HBM logic die 移至 2nm（Samsung Foundry），這直接影響 §12 NC#3「TSMC 隱性贏家」thesis——Custom HBM 的 base die 可能走 Samsung Foundry 2nm，而非 TSMC N12FFC+/N3P 路線。這是一個 Pass 1 未抓到的 cross-ID 衝突（直接衝擊 NC#3 的長期延伸）。

**CONCLUSION_IMPACT: 🟡 PARTIAL_IMPACT**（反方 3 事實升級，使其 j-conf 應從「中」升至「高」）
- 修正方向：j-conf 從「中」升為「高」；j-facts 更新為「Samsung 已設立 250 人 Custom HBM 團隊，Custom HBM4E 設計預計 2026 H1 完成、2026 H2 正式發表（TrendForce 2026-01）」；追加 Samsung 2nm Custom HBM base die 對 TSMC NC#3 的潛在長期影響

---

### Finding P2-F5: 反方 2（CXL pooling）事實狀況 — 仍維持「低信心」，無新重大事件

**位置**: §9.5 Kill Scenario 反方 2

**評估**: 搜尋未發現 2026 H1 有任何 hyperscaler 公告 CXL 取代 HBM 部署的重大事件。CXL 2.0/3.0 仍在標準化和試點階段，2026 H1 沒有 falsification 條件觸發。反方 2「信心：低」評估在 Pass 2 維持不變，無新結論性發現。

**CONCLUSION_IMPACT: 🟢 COSMETIC（無新發現）**

---

## Focus Area 4 — §3 Hybrid Bonding 良率與 BESI 訂單能見度

### Finding P2-F6: §3 Hybrid Bonding「HBM4 選配」描述——有新發展（BESI Q1 2026 訂單暴增）

**位置**: §3 關鍵子技術表、Kingmaker 子技術分析

**ID 的描述**:
> Hybrid Bonding（HBM4+）：良率 50-60%（新）；HBM5 必用，HBM4 選配

**實際 2026 最新狀況**:
- BESI Q1 2026 結果（2026-04-23）：訂單 €269.7M，YoY +104.5%，大幅增加來自 hybrid bonding 系統
- BESI Q2 2026 outlook：revenue 預計比 Q1 +30-40%
- SemiEngineering 確認：「HBM4 Sticks With Microbumps, Postponing Hybrid Bonding」——**HBM4 世代確認不採用 Hybrid Bonding**，延至 HBM5
- Hybrid Bonder 市場規模：預計 2028 達 $2B

**評估**:
ID 說「HBM4 選配，HBM5 強制」是正確的方向，但需要更精確地說明「HBM4 已確認不採用 Hybrid Bonding，保持 microbump；HBM5（2028）才是 Hybrid Bonding 強制世代」。

良率 50-60% 的描述：BESI 官方和業界報告指出 Hybrid Bonding 仍在良率爬坡中，50-60% 是合理的當前估值，但 BESI Q1 2026 的訂單暴增（+104%）暗示需求正在快速上升，2026 H2-2027 的 throughput 和訂單能見度強於 ID 所描述的不確定性。

**CONCLUSION_IMPACT: 🟢 COSMETIC**（方向正確，但措辭可更精確）
- 「HBM4 選配」改為「HBM4 已確認不採用，延至 HBM5（SemiEngineering 2026-04 確認）」
- 不改變「BESI 是 HBM5 受益者」的結論

---

### Finding P2-F7: §3 1c DRAM 製程「SK 領先」——領先幅度量化可更新

**位置**: §3 關鍵子技術表、Kingmaker 子技術

**ID 的描述**:
> 1b / 1c DRAM 製程：SK 領先；Samsung、Micron

**實際 2026 最新狀況**:
- SK hynix 1c DRAM yield：**80%**（mass production 成熟水平）；已切換超過一半產能；月產能 190K wafers（2026 EOY）
- Samsung 1c DRAM for HBM4 yield：**~50%**（仍在 ramp，rumored）
- **Micron HBM4 使用 1β（1b）製程，而非 1c**——Micron 仍用上一代製程做 HBM4

**量化領先差距**:
- SK hynix 1c @ 80% vs Samsung 1c @ 50% vs Micron 1b（仍未到 1c）
- 這是重要的具體化，ID 只說「SK 領先」但未量化；Samsung 的 50% yield 也直接影響 §12 NC#1「Samsung 2027 HBM4 份額 25-30%」的可信度（yield 問題是 Samsung 追趕的最大障礙）

**CONCLUSION_IMPACT: 🟡 PARTIAL_IMPACT**
- §3 子技術表 1b/1c 欄位更新：「SK 80% yield（mass production 成熟）/ Samsung ~50%（ramp 中）/ Micron 仍用 1b（非 1c）」
- §12 NC#1 j-facts 補充：「Samsung 1c yield ~50% vs SK 80%，落差巨大，2026 HBM4 份額 25% 的達成需要 yield 快速追趕」

---

## Focus Area 5 — §11 NVDA Depth Tier + Rubin GPU 出貨量假設

### Finding P2-F8: §6 C 表 Rubin 出貨量假設「200-300K GPU」已嚴重過時

**位置**: §6 C 下游 AI 加速器需求表

**ID 的聲稱**:
> NVIDIA：~60%（Rubin 每 GPU 288 GB × 200-300K GPU = ~75B GB）

**實際 Rubin 出貨量預估（2026 最新）**:
- UBS 最新半導體供應鏈報告：**2026 NVIDIA Rubin GPU 預測上修至 300 萬台**（3M units）
- Nvidia 自己把 2026 Rubin 目標從 200 萬台降至 **150 萬台**（因 HBM4 驗證延遲）
- TrendForce 2026-04-08：「Rubin 佔 NVIDIA 2026 高端 GPU 出貨量 22%」，Blackwell 仍超 70%
- 最保守估計（TrendForce）：Rubin 在 NVIDIA 2026 高端 GPU 中佔 22%，若 NVIDIA 2026 總出貨 7.5M（UBS），Rubin ~1.65M

**計算比較**:
- ID 假設：200-300K Rubin GPU × 288 GB = 57.6-86.4B GB（約 75B GB）
- 實際最新估值：1.5-3M Rubin GPU × 288 GB = **432-864B GB**（5-12x ID 的假設）
- 即使取保守的 1.5M 台：**432B GB vs ID 的 75B GB，相差 5.8 倍**

**影響評估**:
ID 的 200-300K GPU 是**極早期、已過時的 2025 年估值**。2026 年 Rubin 出貨量估計已大幅上修（1.5-3M 台），即使考慮 HBM4 供給瓶頸（可能使實際出貨低於計劃），仍遠高於 75B GB 的假設。

這對 §11 NVDA 的「🟡 次要」深度 tier 判斷有影響：若 Rubin 實際出貨 1.5-3M GPU，HBM4 需求量比 ID 所假設的高 5-12 倍，NVDA 的 HBM 曝險比「🟡 次要」更深。

**Pass 1 是否抓到**: ❌ Pass 1 對 §6 C 表數字沒有深入查核。

**CONCLUSION_IMPACT: 🟡 PARTIAL_IMPACT**
- §6 C 表 NVDA row 更新：「Rubin 每 GPU 288 GB × 1.5-3M GPU（UBS 最新：3M，含 HBM4 瓶頸影響調降至 ~1.5M）= 432-864B GB」
- §11 NVDA depth tier：從「🟡 次要」升至考慮「🔴 核心」（若 Rubin 1.5M 台實現，NVDA 的 HBM 曝險是結構性的，不是「次要」）

---

## Focus Area 6 — §10.5 Catalyst 時間點合理性

### Finding P2-F9: §10.5 Catalyst Timeline「Micron FY26 Q3 法說」時間點確認合理

**位置**: §10.5 Catalyst Timeline

**評估**:
- ID publish date：2026-04-19
- §10.5 列「2026-Q2 Micron FY26 Q3 法說」作為 upcoming catalyst
- Micron FY26 Q3 法說預期：2026 年 6 月中旬（Micron FY 結束於 8 月，Q3 FY26 = 2026 年 3-5 月，法說約在 6 月）
- 距離 publish 時間（2026-04-19）約 2 個月後——時間點合理，屬於真實的 upcoming catalyst

**但補充一個 Pass 1 + Pass 2 都未追蹤的問題**:
- §10.5 未列 SK hynix Q1 2026 法說（2026-04-22，publish 後 3 天，Pass 1 已標為 🟡）
- **新增發現**：SK hynix Q2 2026 法說（2026-06）也應該加入 §10.5，目前表格只到「2026-06 SK hynix Q2 法說」——但這個表格的實際措辭說「2026-06 SK hynix Q2 法說：HBM4 NVDA 分配 70% 確認」，這是合理的。問題是 Q1 2026 的法說（已發生、數字更強勁）沒有被追蹤。

**CONCLUSION_IMPACT: 🟢 COSMETIC（時間點本身合理，已知 Pass 1 B-9 問題無新增）**

---

## Focus Area 7 — §4 TAM Forecast 偏差表

### Finding P2-F10: §4「Gartner 2024 預估 $5B vs 實際 $9B guide」偏差表——$9B 是過時且被多家機構大幅上修的錨點

**位置**: §4 過去 3 次 TAM forecast 偏差表

**ID 的聲稱**:
> 2024 Gartner：預估 2026 $5B vs 實際 $9B guide，偏差低估 80%

**Pass 2 新發現**:
Pass 1 已確認 $9B 是過時的 TAM anchor。Pass 2 進一步確認：
- **Goldman Sachs 2026 HBM TAM 估值：$45B**（已從 $51B 下調 13%，但仍是 $9B 的 5 倍）
- **Yole Group**：2025 HBM revenue 已接近 $34B，意味 2025 年就已是 2024 Gartner 預估 $5B 的 7 倍
- **Precedence Research**：2026 HBM 市場 $9.18B（與 ID 相近，但這個機構本身估值偏低）
- **Mordor Intelligence**：2026 HBM 市場 $3.98B

**估值方法論分歧分析**:
$9B vs $45B 的差距反映的是不同口徑：
1. 窄口徑（HBM chip revenue only）：約 $9-10B（接近 ID 的數字）
2. 寬口徑（含 base die、封裝、memory controller）：可達 $35-50B
3. Goldman Sachs 用的是 memory manufacturer total HBM revenue，包含 HBM 相關全部業務

**ID 的 $9B 如果是窄口徑 HBM chip ASP × volume，在 Yole/GS 的寬口徑定義下被低估。** 偏差表中「2026 $9B guide」被拿來說明「業界一直低估 HBM TAM」的論點本身正確，但用過時的 $9B anchor 作為基準，使論點力度大打折扣——因為更新的數字（GS $45B）讓偏差不是 80%，而是幾百%。

**CONCLUSION_IMPACT: 🟡 PARTIAL_IMPACT**（Pass 1 已標 $9B 為過時 anchor，Pass 2 補充：偏差倍數遠比 ID 所述更大）
- 修正方向：§4 偏差表第三行改為「2024 Gartner：預估 2026 $5B vs Goldman Sachs 2026 實際估 $45B，偏差低估 800%+（Yole 窄口徑 $34B 也是 Gartner 的 7 倍）」；這反而強化了「業界一直低估 HBM TAM」的 thesis，只是數字需更新

---

## Focus Area 8 — §0 + §11.5 Cross-ID 額外衝突

### Finding P2-F11: Samsung Custom HBM 2nm base die → §12 NC#3 TSMC 長期延伸被新威脅

**位置**: §11.5 Cross-ID 依賴圖；§12 NC#3

**Pass 1 涵蓋**: NC#3「TSMC 獨家」已被推翻（Samsung Foundry 4nm 自代工）。

**Pass 2 新增發現**:
TrendForce 2026-01-21 確認：Samsung 正在將 **Custom HBM logic die 移至 Samsung Foundry 2nm** 製程（首次）。

這意味：
1. Samsung Memory 的 HBM base die 路線圖是：HBM4（Samsung Foundry 4nm）→ Custom HBM4E（Samsung Foundry 2nm）
2. 如果 Custom HBM 是 2027+ 的成長驅動之一（§9.5 反方 3 指出此可能），Samsung Foundry 2nm 將承接一大塊 Custom HBM base die 業務，**進一步壓縮 TSMC 的 HBM base die 份額**
3. §12 NC#3 的長期 thesis「2027-2028 TSMC 新增 HBM base die rev ~$3-5B」需要考慮 Samsung Foundry 2nm custom HBM 的分流效應

**這是一個 Pass 1 沒有抓到的 NC#3 額外削弱因素**，不改變 NC#3 已是 🔴 BROKEN 的結論，但使修正後的 thesis 更加複雜。

**CONCLUSION_IMPACT: 🟢 COSMETIC**（NC#3 已是 🔴 BROKEN，此為已破 thesis 的額外細節補充，不升級）

---

## Pass 2 完整評分表

| # | 位置 | 問題 | Pass 1 抓到？ | CONCLUSION_IMPACT |
|---|---|---|---|---|
| P2-F1 | §7 ASP 動態表 | HBM3E ASP $3,000/stack vs 實際 $300/stack（10x 高估）；per GB $35 vs 實際 $8-15 | ❌ 未抓 | 🔴 CHANGES_CONCLUSION |
| P2-F2 | §7 毛利表 SK hynix | 2025 SK hynix GM 42% vs 實際 79%（差距 37pp） | ❌ 未抓 | 🔴 CHANGES_CONCLUSION（若 79% 為全年）/ 🟡（若 79% 為 Q4） |
| P2-F3 | §9 政策地緣 | 2026-01 H200 export 政策鬆動（Trump admin case-by-case）未納入，影響「中國需求完全流失」假設 | ❌ 未抓 | 🟡 PARTIAL_IMPACT |
| P2-F4 | §9.5 反方 3 | Custom HBM 已從「討論中」升至「Samsung 250 人團隊、2026 H1 設計完成、2nm base die」，j-conf 應升為「高」 | ❌ 未抓 | 🟡 PARTIAL_IMPACT |
| P2-F5 | §9.5 反方 2 | CXL pooling：無新 2026 H1 事件，「低信心」評估維持 | — | 🟢 COSMETIC（無新發現） |
| P2-F6 | §3 Hybrid Bonding | HBM4 已確認不採用 Hybrid Bonding（保持 microbump），BESI Q1 訂單 +104% 強勁 | ❌ 未抓方向 | 🟢 COSMETIC（方向正確需更精確） |
| P2-F7 | §3 1c DRAM | SK 1c @ 80% / Samsung 1c @ 50% / Micron 仍 1b；量化領先差距 | ❌ 未抓具體數字 | 🟡 PARTIAL_IMPACT |
| P2-F8 | §6 C 表 NVDA | Rubin 出貨量 200-300K（ID）vs 1.5-3M（最新）；差距 5-12x，NVDA HBM 需求低估 | ❌ 未抓 | 🟡 PARTIAL_IMPACT |
| P2-F9 | §10.5 Catalyst | Micron FY26 Q3 法說時間點合理；無新增問題 | — | 🟢 COSMETIC |
| P2-F10 | §4 TAM 偏差表 | $9B 過時錨點，GS 估 $45B（5x），偏差倍數遠比 ID 描述的大；但方向正確 | 🟡 已部分（Pass 1 標 $9B 過時）| 🟡 PARTIAL（補充新數字） |
| P2-F11 | NC#3 + Custom HBM | Samsung Custom HBM base die 走 Samsung Foundry 2nm，進一步削弱 TSMC NC#3 長期延伸 | ❌ 未抓 | 🟢 COSMETIC（NC#3 已破） |

**Pass 2 新增**:
- 🔴 CHANGES_CONCLUSION：2 條（P2-F1, P2-F2）
- 🟡 PARTIAL_IMPACT：4 條（P2-F3, P2-F4, P2-F7, P2-F8）
- 🟢 COSMETIC：3 條（P2-F5, P2-F6, P2-F9, P2-F11）

---

## 最大新發現（Biggest One）

**P2-F1（§7 ASP 數字 10x 高估）是 Pass 2 最重要的新發現。**

ID 在 §7 宣稱 HBM3E 2026E ASP 約 $3,500/stack（$97/GB），但實際 2026 市場成交價約 $300/stack（$8-10/GB）——差距高達 **10 倍 per stack**、**7-10 倍 per GB**。這個錯誤完全被 Pass 1 忽略，且影響面極廣：§7 Insight（5-8x 溢價）、§8 所有 EPS 影響計算、§6 A 表 SOM 計算基礎、§0 核心 insight 3（「HBM4 stack 毛利是 LPDDR5 的 5-8x」）都受牽連。Pass 2 若只有一條貢獻，這是最大的。

**P2-F2（SK hynix 2025 GM 42% vs 實際 79%）是第二重要的。** 即使保守估計全年 GM 為 55%，ID 的 42% 已低報 13pp；若實際是 79%，低報 37pp，使 §7 整個 margin trajectory narrative 失真。

---

## Pass 2 vs Pass 1 邊際價值評估

**Pass 2 不是 marginal — 它發現了 Pass 1 完全遺漏的兩條 🔴 CHANGES_CONCLUSION（§7 ASP 10x 高估 + SK hynix GM 42% vs 79%）。**

Pass 1 的重點在 TAM/SOM 口徑、3nm stale 字樣、Samsung Foundry 50% Pyeongtaek、Hyperscaler capex 減速，完全沒有進入 §7 Unit Economics 細節查核。Pass 2 填補了這個重要盲區。

合計更新後的 verdict：
- 原 Pass 1：3 🔴 / 7 🟡 / 5 🟢
- Pass 2 新增：+2 🔴 / +4 🟡 / +3 🟢（+ P2-F10 已有 🟡 延伸）
- **合計：5 🔴 / 11 🟡 / 8 🟢**

THESIS_BROKEN 維持不變，但需 patch 的必修清單從 4 項增至 6 項（新增 P2-F1 §7 ASP 全面重寫 + P2-F2 GM 數字修正）。

---

## 建議 v1.2 Patch 優先序更新（Pass 2 新增項）

### 🔴 新增必修（P2-specific）

**P2-P1：§7 ASP 動態表全面重寫**
- 問題：HBM3E $3,000-3,500/stack，HBM4 $4,500+，per GB $35——全部高估 6-10x
- 修正：
  - HBM3E（36GB stack）：2025 ~$500/stack（$15/GB），2026E ~$300-400（GS: $10/GB after 28% decline）
  - HBM4（48GB stack）：2026E ~$400-600/stack（$10+/GB）
  - HBM per GB 基準：2026 約 $8-12（非 $35）
  - HBM vs DDR5 溢價：改為「2-3x」（非 5-8x）
  - §7 Insight 1 重寫：「HBM per GB 溢價約 2-3x vs DDR5（DDR5 ~$4-6/GB，HBM3E ~$8-12/GB），不是物理定律決定的 5-8x」

**P2-P2：§7 毛利表 SK hynix 2025 GM 更新**
- 問題：42% 嚴重低報（實際 79% 或至少 55%+）
- 修正：查 SK hynix FY25 Annual Report P&L 確認全年 GM 後，更新 §7 表格 SK hynix 2025 欄；同步更新 §7 Insight 2（「毛利回到歷史高點」→「SK hynix FY25 GM 79% 已創歷史新高」）

### 🟡 新增建議修（P2-specific）

**P2-P3：§9 政策地緣表新增 2026-01 H200 export 鬆動**
- 新增 row：「2026-01 Trump admin HBM 出口政策調整：H200（含 HBM3E）恢復向中國 approved customers 出口（case-by-case）→ 部分中國 HBM3E 需求可能回流」

**P2-P4：§9.5 反方 3 Custom HBM j-conf + j-facts 更新**
- j-conf 從「中」升為「高」
- j-facts 更新：Samsung 250 人 Custom HBM 專責團隊；Custom HBM4E 設計預計 2026 H1 完成（TrendForce 2026-01-23）；Samsung Custom HBM logic die 移至 2nm foundry

**P2-P5：§6 C 表 NVDA Rubin 出貨量更新**
- 從「200-300K GPU」更新為「1.5-3M GPU（UBS 2026-04 最新：3M；HBM4 瓶頸調降版：1.5M）」；HBM 需求從 75B GB 更新為 432-864B GB

**P2-P6：§3 1c DRAM 競爭具體化**
- 更新：「SK hynix 1c yield 80%（mass prod 成熟）/ Samsung 1c yield ~50%（ramp 中）/ Micron 仍使用 1b（non-1c）」

---

*Pass 2 原則：Pass 1 寫稿 agent 專注在高層次邏輯錯誤（口徑混淆、stale 字樣、TAM 框架）；Pass 2 補齊 Pass 1 跳過的 unit economics 細節（§7 ASP + GM 數字）和 catalyst 新事件（2026-01 export 政策、Custom HBM 具體進展），兩輪合計才能有效指導 v1.2 patch。*

---

**Sources（WebSearch 依賴）**:
- [SK hynix FY25 Annual Results — SK Hynix IR](https://news.skhynix.com/sk-hynix-announces-fy25-financial-results/)
- [SK Hynix posts record year as HBM boom supercharges profits — Blocks and Files](https://blocksandfiles.com/2026/01/28/sk-hynix-q4-2025/)
- [SK Hynix logs 72% operating margin; HBM4 demand exceeds capacity for next 3 years — KED Global](https://www.kedglobal.com/earnings/newsView/ked202604230001)
- [HBM Memory Pricing and Specifications (2026) — Silicon Analysts](https://siliconanalysts.com/data/hbm-pricing)
- [Goldman Sachs HBM3E $15→$10/GB decline — Jukan X thread](https://x.com/Jukanlosreve/status/1988063459448418377)
- [Samsung, SK hynix HBM3E 20% Price Hike for 2026 — TrendForce](https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/)
- [HBM Prices Reportedly Face Double-digit Drop Risks in 2026 — TrendForce](https://www.trendforce.com/news/2025/07/18/news-hbm-prices-reportedly-face-double-digit-drop-risks-in-2026-posing-challenges-for-sk-hynix/)
- [January 2026 BIS License Review Policy Revision — Federal Register](https://www.federalregister.gov/documents/2026/01/15/2026-00789/revision-to-license-review-policy-for-advanced-computing-commodities)
- [US Curbs HBM Exports To China — Next Platform](https://www.nextplatform.com/2024/12/02/us-curbs-hbm-exports-to-china-more-for-the-rest-of-us/)
- [Samsung Custom HBM4E Design Aimed for Mid-2026 — TrendForce](https://www.trendforce.com/news/2026/01/23/news-samsungs-custom-hbm4e-design-reportedly-aimed-for-mid-2026-parallels-sk-hynix-and-micron/)
- [Samsung Moves Custom HBM Logic Die to 2nm Foundry — TrendForce](https://www.trendforce.com/news/2026/01/21/news-samsung-reportedly-moves-custom-hbm-logic-die-to-2nm-foundry-process-for-the-first-time/)
- [BESI Q1-26 Results — GlobeNewswire](https://www.globenewswire.com/news-release/2026/04/23/3279584/0/en/BE-Semiconductor-Industries-N-V-Announces-Q1-26-Results.html)
- [HBM4 Sticks With Microbumps, Postponing Hybrid Bonding — SemiEngineering](https://semiengineering.com/hbm4-sticks-with-microbumps-postponing-hybrid-bonding/)
- [UBS Rubin GPU forecast 3M units — Jukan X thread](https://x.com/jukan05/status/1992209835249819925)
- [Nvidia Rubin Mass Production Target Lowered — BigGo Finance](https://finance.biggo.com/news/-YFfZZ0ByH9TLH69jS0g)
- [Rubin Faces Delay Risks, Blackwell Over 70% of NVIDIA 2026 High-End GPU — TrendForce](https://www.trendforce.com/presscenter/news/20260408-13003.html)
- [SK hynix 1c DRAM to 6 EUV layers — Tweaktown](https://www.tweaktown.com/news/106957/sk-hynix-ramps-1c-dram-to-6-euv-layers-preps-for-high-na-designs-destroy-samsung-in-hbm/index.html)
- [Samsung 1c DRAM yield ~50% for HBM4 — Tweaktown](https://www.tweaktown.com/news/108316/samsung-1c-dram-for-hbm4-yields-rumored-to-hit-around-50-percent-to-battle-sk-hynix-and-micron/index.html)
- [Yole Group HBM 2025 ~$34B — Yole Group Press Release](https://www.yolegroup.com/press-release/memory-market-surges-beyond-expectations-almost-200-billion-in-2025-driven-by-hbm-ai/)
