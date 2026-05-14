# id-review Critic Report — DS Mode
**File**: `docs/ds/DS_FoundryGeography_20260514.html`  
**Theme**: Foundry Geography — 晶圓代工地理供應鏈、CHIPS Act 重組、Taiwan 集中度結構性悖論  
**Critic date**: 2026-05-14  
**Mode**: `--mode ds` (v1.4.1, 8 checks: DS-1 to DS-9, DS-7 removed)  
**Verdict**: **AT_RISK** — 0 🔴 CHANGES_CONCLUSION, 3 🟡 PARTIAL_ERROR, 1 🟢 COSMETIC

---

## Summary

| Check | Result | Severity |
|:------|:-------|:---------|
| DS-1 表格比例 | 4 tables, 13.7% ratio, max 8 rows | ✅ Pass |
| DS-2 §1→§3/§5 因果閉合 | All 5 inflections closed in §3 or §5 | ✅ Pass |
| DS-3 §3+§5 供需平衡明確結論 | 結論存在但缺顯式 surplus/shortage/balance 標記 | 🟡 PARTIAL_ERROR |
| DS-4 §6 三情境 trigger 可量化 | Trigger 欄有事件但缺可量化閾值 | 🟡 PARTIAL_ERROR |
| DS-5 §10 catalyst 雙路徑 | 8 節點全部有 if-hit/if-miss 雙路徑 | ✅ Pass |
| DS-6 §11 ticker 與 §3/§5 一致 | INTC beneficiary=True 有條件性需補充 | 🟢 COSMETIC |
| DS-8 §6 推導抽查 | 3Y 全三案有 derive；12M/5Y 均無 derive；bear 85% vs 80% 矛盾 | 🟡 PARTIAL_ERROR |
| DS-9 §1 雙錨點 | 5 段全部有 YYYY(-MM) + 量化錨點 | ✅ Pass |

---

## 🟡 PARTIAL_ERROR #1 — DS-3：§3+§5 缺顯式供需平衡結論標記

**Spec**: §5 結尾或 §6 開頭須出現「過剩 / surplus / oversupply」「平衡 / balance」「短缺 / shortage / undersupply」三選一，允許分 horizon 但每段必須明確。

**Finding**: §5 結論段寫「結構性 multi-hub 擴張 + Taiwan 仍主導 leading-edge」、「reshoring 是追加供給而非替代 Taiwan」，方向性清晰，但**全文沒有出現上述任一關鍵字**。對 PM 而言，leading-edge geography DS 的供需實質狀態是：需求方（美國 fabless 70% 市占）每年 +6-7%，供給方（Taiwan leading-edge reshore 速度）3-5%/yr，是結構性供給短缺（demand >> reshoring rate）；但報告沒有顯式說「leading-edge 在地理供給側呈結構性短缺（shortage）」。

**影響**: PM 讀 §5 結尾看不到供需平衡結論，需要自行推斷 → §6 推估的底層邏輯不完整。不影響 thesis 方向（結論是 Taiwan dominance 持續，與 shortage 一致），但破壞 DS-3 的 checkable 結構。

**建議修正**: 在 §5 最後一段「這個結論直接餵入 §6 三 horizon 推估」之前，插入一句明確結論，例如：「在供需維度：leading-edge 晶圓製造在地理上呈**結構性短缺**（短期 shortage）— demand growth 6-7%/yr 持續超越 reshoring supply 3-5%/yr，Taiwan 相對定價權（+30% premium）是此短缺的市場訊號；中長期隨 Arizona ramp 補量逐步走向**寬鬆平衡**（base: 2028-2030 gradual）或更深短缺（bear: 地緣衝突）。」

---

## 🟡 PARTIAL_ERROR #2 — DS-4：§6 trigger 欄缺可量化閾值

**Spec**: 「Trigger 欄非空（每 horizon 一個可量化 metric）」。

**Finding**: §6 表格的「關鍵 Trigger」欄每 horizon 有 2-3 個事件節點（法說、tariff review、選舉結果），但均為**事件描述**而非可量化閾值：

- 12M Trigger: `NVDA Q2 法說 AZ ramp 進度` — 無「wpm ≥ X」門檻
- 3Y Trigger: `Intel 14A risk production 結果 + Apple 14A 決定` — 無「wpm ≥ X or ≤ Y 則判斷 bull/bear」
- 5Y Trigger: `中台政治情境` — 完全定性，無任何量化

DS-8 derive blocks（base/bull/bear 各 3Y 有推導）確實寫了關鍵 input（Arizona ramp wpm、Samsung leading-edge wpm），但這些數字沒有被「回寫」到 trigger 欄成為條件邏輯。對 PM 而言，trigger 欄應告訴他「當觀察到 X 超過 Y 時，切換情境判斷」，而非「下次法說看結果」。

**影響**: 投資組合再平衡決策點模糊 — §10 catalyst 有明確 if-hit/if-miss 門檻（做法更好），但 §6 trigger 欄更弱。不影響 thesis 正確性，影響 actionability。

**建議修正**: 每 horizon trigger 加一個具體量化條件，例如：
- 12M: 補「TSMC AZ Fab 1 月產 ≥ 90K wpm（法說揭示）且 Intel 18A 外部 wpm ≥ 10K → base 確認；否則 bear 評估升級」
- 3Y: 補「Intel 14A anchor 客戶 wpm ≥ 30K → US 第二強確認；Samsung 退出 leading-edge → bull 觸發」
- 5Y: 補「Taiwan leading-edge wpm 占比 ≤ 70% → Phase III 切換評估；中台衝突觸發 active blockade ≥ 30 天 → bear 確認」

---

## 🟡 PARTIAL_ERROR #3 — DS-8：12M/5Y 無推導 + 3Y/5Y bear Taiwan 占比矛盾

**Spec**: 「從 §6 表格中隨機抽 base / bull / bear 各一格，對每個：表外緊鄰段落是否有推導行（→）；推導行 input 數字是否能在 §2/§3/§4/§5 找到對應出處；bull/bear 偏離 base 是否由 input 假設改變推出。」

**Finding 1 — 覆蓋缺口**: 3Y 的三案全部有 `<div class="ds-derive">` 且 input 可追溯到 §2/§5（Arizona wpm、Samsung wpm 源自 SEMI/TSMC 數據）。但：
- **12M（短期）三案**：table 格子是完整 narrative，但**無任何 ds-derive block**。12M bull case 的 `TSMC AZ Fab 2 提前到 2026-Q4 量產` 從哪個 input 推出？bear case 的 `海外占比降至 7%` 是 how？無推導。
- **5Y（長期）三案**：同樣無 ds-derive block。5Y base 的 `TSMC CAGR 16%` 從哪來？5Y bull `CAGR 20%`？**黑盒**。

**Finding 2 — 3Y bear vs 5Y bear Taiwan 占比矛盾**:
- 3Y bear ds-derive: 「Taiwan 占比反升至 **85%**」
- 5Y bear 表格: 「Taiwan 占比反向上升至 **80%**」
- 5Y bear 情境比 3Y bear 時間更長（地緣衝突持續 → Arizona 擴張更停滯），但 Taiwan 占比 5Y bear 反而**低於** 3Y bear。邏輯矛盾：若 3Y bear 是 85%，5Y bear（同樣衝突環境但更長時間）應 ≥ 85%，不應降到 80%。

**影響**: 12M/5Y 推導缺口影響 PM 自主驗算能力。3Y/5Y bear 數字矛盾是可被質疑的內部一致性問題，但不改變 thesis 方向（兩者都是 Taiwan 占比上升）。

**建議修正**:
1. 12M 和 5Y 各補 ds-derive block（base 各一）：12M base 只需補 `推導：AZ Fab 1 100K wpm (Q4 2025 ramp 基礎 §2) + Kumamoto 55K wpm (JASM Phase 1 §3) → 海外占比 5%→8%`；5Y base 補 `推導：Arizona 6 fab = ~300K wpm (TSMC 2030 gigafab roadmap) / 全球 44M wpm = 17% + Taiwan 1.2M/44M = 約 72%`
2. 修正 5Y bear 台灣占比：從 80% 改為 85%+（或增加解釋為何長期 bear scenario 台灣占比反而低於中期 bear）

---

## 🟢 COSMETIC #1 — DS-6：INTC beneficiary=True 需補條件性 caveat

**Finding**: §11 table INTC 標 `beneficiary=True, depth=🟡`，角色說明「US foundry turnaround binary + Magdeburg 已退出 EU」。這是正確的，但 §3 明確說「Magdeburg 退出暗示 EU leading-edge foundry 計畫實質失敗」，兩者並置可能讓讀者以為 Intel 整體是直接受益者。實際上 INTC 是條件性受益者：若 18A/14A 獲客 → 受益；若不獲客（§11 表格自身也寫「若失敗 <30%」）→ 受損。

**建議修正**: §11 表格 INTC「角色」或「Forward 2028E 地理 exposure」欄加一行提醒：「受益條件：18A/14A 外部客戶體量 ≥ 30K wpm；未達則 foundry 業務重新評估」。或在 ds-meta JSON 的 INTC role 字段改為「conditional beneficiary」。

---

## 关鍵事實核查（Key Claims）

核查 DS 中的核心數字聲稱：

| Claim | 支持程度 | 備注 |
|:------|:---------|:-----|
| Taiwan leading-edge 82% (2024) → 75% (2028) base | ✅ §2/§5 有推導，源自 SEMI wpm 數據 | 82%→78% 2026E 已列表 |
| US 4% (2024) → 17% (2030) | ✅ §5 表格明列，§6 推導覆蓋 | 2030 base 數字一致 |
| TSMC AZ Fab 1 100K wpm Q4 2025, Fab 2 3nm 2027 H2 | ✅ §2/§3 均有提及，Tom's Hardware 來源 | 一致 |
| TSMC AZ +10% true cost / +30% pricing premium (TechInsights) | ✅ §0 thesis box + §8 §3 均引用 | TechInsights 2025 來源已列 |
| China 21% global capacity by 2030, leading-edge <5% | ✅ §3/§8 有清晰拆解 | 兩個來源交叉（SEMI + Global SMT） |
| Intel Magdeburg cancelled 2025-07 | ✅ §1/§3 均有，Politico 來源 | Wroclaw 也一併提及 |
| Taiwan M7.4 2024-04-03, $60M Q2 impact | ✅ §1 明文「Barclays 估 Q2 earnings 受影響 $60M」 | Bloomberg + Astute 來源 |
| US-Taiwan deal 2026-01-15, $250B | ✅ §0 thesis box + §1 均提及 | Global Policy Watch 來源 |
| TSMC Kumamoto Phase 1 55K wpm Dec 2024 | ✅ §2/§3 均有，Wikipedia 來源 | Phase 2 時點也有 |

---

## 結論

**Verdict: AT_RISK** — 三條 🟡 PARTIAL_ERROR 不影響 thesis 方向（Taiwan dominance、TSMC 受益、China 21% 是 mature node 偽命題），但削弱 PM 自主驗算與決策能力：
- DS-3 缺顯式 shortage/balance verdict → PM 需要自行解讀供需定性
- DS-4 trigger 無量化閾值 → 再平衡決策窗模糊
- DS-8 12M/5Y 黑盒 + bear 數字內部矛盾 → 推導可追溯性不完整

建議 patch 優先順序：DS-8 的 3Y/5Y bear 矛盾（最具體、最易修）> DS-3 顯式 shortage 段落 > DS-4 trigger 量化閾值（最複雜）> DS-6 INTC caveat（cosmetic）。

**Publish gate status**: AT_RISK，Q1 Standard → 警告非阻擋；建議 user 決定 ship (with banner) or fix 三條 🟡。
