你是 stock-analyst v17 判斷 agent，回來做**一輪定點修補**。標的 FIX（20260906）。判斷物已由跨模型閘（gate）冷讀過，下面是它點名的判斷級發現。你的任務只有一件：**針對被點名的欄位做最小修正**，不重寫判斷。

## 讀（判斷物全文附於本訊息之後，不要 Read 任何檔）

判斷物（judgment.json）全文接在本訊息最後（「===== BUNDLE =====」分隔行之後）。

不要重讀 bundle、evidence.json、gate_audit.md、`docs/dd/` 任何檔，也不要回讀你等一下寫出的新版 judgment。你需要的稽核意見全文已附在下方，判斷物全文已附在最後。

## 閘的發現（gate findings）

### 發現 1：3 其他結構變數 🔴
- **依據**：regulatory_antitrust#1（PFAS 冷卻劑／密封劑 phasedown，直指冷卻系統範疇）與 reg_tariff_export#2（301 關稅暫停一年、2025-11-10 起算即 2026-11 到期）在 contradictions／premortem／triggers／thesis.R／evidence_dismissed 皆無對應條目
- **建議改法**：catalysts 或 R3 增列 PFAS 合規成本與 301 到期兩項門檻與監測欄位，或寫入 evidence_dismissed 並說明不觸及任何假設
- **指向欄位**：thesis.R[2]、catalysts[3]、evidence_dismissed[]

**受影響子樹原文**：

`thesis.R[2]`：
```json
{
  "id": "R3",
  "text": "執行端瓶頸：技工短缺、變壓器與開關設備交期長達五年、關稅推升材料成本，讓 $14B 訂單無法按進度、按毛利轉成營收",
  "h_ref": "H1, H3",
  "clock": "🔥",
  "threshold": "訂單轉營收比（季營收÷期初訂單）連 2 季低於 20%；毛利連 2 季下滑 >1.5pp 且管理層歸因勞動力",
  "evidence_refs": [
    "supply_demand_durability#4",
    "geo_supply_chain#0",
    "geo_supply_chain#1",
    "geo_supply_chain#2",
    "reg_tariff_export#0"
  ]
}
```

`catalysts[3]`：
```json
{
  "date": "2027-12",
  "date_precision": "month",
  "type": "regulatory",
  "event": "鋼鋁銅 232 關稅修訂案效期至 2027-12-31，之後是否再延或加碼",
  "impact": "低",
  "watch": "材料占 40-45% 專案成本的通過能力"
}
```

**相關 evidence finding 原文**：

`regulatory_antitrust#1`：
```json
{
  "claim": "Industry commentary on the 2026 data-center/mechanical construction 'industrial supercycle' flags the phasedown of PFAS-based coolants and sealants (widely used in specialized cooling systems) as an emerging environmental-regulatory risk for the sector, with compliant players positioned to capture share as the rules tighten.",
  "source": "FinancialContent — \"Comfort Systems USA Shares Hit Record Highs as 'Industrial Supercycle' Ignites Infrastructure Demand\"",
  "as_of": "2026-02-20",
  "direction": "0",
  "affects": [
    "moat_trend",
    "thesis.R"
  ],
  "id": "regulatory_antitrust#1"
}
```

`reg_tariff_export#2`：
```json
{
  "claim": "The U.S. and China reached a preliminary trade agreement on 2025-10-30 easing tensions, and USTR Section 301 China tariffs were suspended for one year starting 2025-11-10 (with China suspending its retaliatory tariffs in kind), reducing near-term U.S.-China trade/tariff escalation risk broadly.",
  "source": "Morrison Foerster, \"United States and China Reach Trade Agreement: Takeaways for Export and Supply Chain Controls\"",
  "as_of": "2025-11-13",
  "direction": "+",
  "affects": [
    "thesis.R",
    "decision_inputs.bear"
  ],
  "id": "reg_tariff_export#2"
}
```


## 修補紀律

1. **只准改被點名的欄位**——findings 的「指向欄位」是你的動刀範圍。沒被點名的欄位一字不動，包含 `decision_out`（由 `dd_decision.py` 回填，你不要手改）與未涉及的 `reasoning` 段。
2. **裁決方向不由你主動翻**——修正欄位後若 `judge check` 重算出的 `decision_out.verdict` 自己翻面，那是機械層的結果，照實接受並在回報點名；但你不得為了配合閘的語氣直接改寫裁決字串。
3. **可以不採納**——閘的意見不是命令。判斷你認為原判正確時，該條不改欄位，改為在頂層 `evidence_dismissed[]` 補一條 `{"ref": "<閘點名的 finding ref 或欄位路徑>", "reason": "<不採納的具體理由>"}`。理由要指得出證據或推導本身的問題（口徑不可比、來源不可回溯、已被更新一季數字取代、閘誤讀了哪個欄位…），不得寫「影響不大」這類無內容句。**每一條 🔴 都必須有處置**：要嘛改欄位，要嘛進 `evidence_dismissed[]`，不得沉默略過。
4. **🟡 選擇性處理**——能一句話補上就補（通常是 `contradictions[]`／`triggers[]` 加一條或補 `formula_note`），代價過大就依第 3 條寫不採納理由。
5. **不得編造數字**——證據包未涵蓋的數字不准補；該欄位標「證據包未涵蓋」並在回報請 orchestrator 判斷是否回 Stage 0 補軸。
6. 禁 WebSearch／WebFetch。

## 寫（一次 Write 整檔）

改完後把**完整的 judgment.json**一次 `Write` 回 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20260906/judgment.json`（不要分次 Edit、不要只寫片段），接著跑：

```
python3 scripts/ddreport.py judge check FIX 20260906
```

這支會依序重跑 `dd_scenario.py`、`dd_decision.py run`、`validate_judgment.py --evidence --fix --report`，一次把結果回給你；你不需要也不得自行分別呼叫這三支腳本。

FAIL → **只准改 FAIL 訊息點名的欄位**，重跑同一條 `judge check`，**≤1 輪**。一輪後仍 FAIL 就照實回報，交給 orchestrator 處置，不得為湊過驗證而改動判斷實質。

**輪次上限 `6` 輪。** 逼近上限時停下並照實回報。

## 回報（≤200 字）

① 逐條列閘的發現與你的處置（改了哪個欄位／或進 `evidence_dismissed[]` 及理由摘要）
② `judge check` 最後一次的 `validate_judgment.py --report` 原文
③ `decision_out.verdict`／`role`／`row_hit`，以及是否與修補前不同（翻面要明講）
