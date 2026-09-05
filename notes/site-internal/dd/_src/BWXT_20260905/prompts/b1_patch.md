你是 stock-analyst v17 判斷 agent，回來做**一輪定點修補**。標的 BWXT（20260905）。判斷物已由跨模型閘（gate）冷讀過，下面是它點名的判斷級發現。你的任務只有一件：**針對被點名的欄位做最小修正**，不重寫判斷。

## 讀（判斷物全文附於本訊息之後，不要 Read 任何檔）

判斷物（judgment.json）全文接在本訊息最後（「===== BUNDLE =====」分隔行之後）。

不要重讀 bundle、evidence.json、gate_audit.md、`docs/dd/` 任何檔，也不要回讀你等一下寫出的新版 judgment。你需要的稽核意見全文已附在下方，判斷物全文已附在最後。

## 閘的發現（gate findings）

### 發現 1：6 量化模組完整性 🔴
- **依據**：roiic 的 formula_note 括號〔capex $247M − 折舊 $100M ＋ PCG $200M〕＝$347M，卻寫成「增量投入約 $450M」；且 $90M÷$450M＝20%、$90M÷$347M＝25.9%，皆非所寫的 17%——同一括號在 reinvest_rate 用的是 347（347÷355≈98%，對得上），故 ROIIC 一項推導不可複算，而 endo_ceiling 10.2＝17%×60% 全建立其上
- **建議改法**：增量投入統一為 $347M 並重算 ROIIC（稅前 90÷347≈26%、稅後 69÷347≈20%），據此重算 endo_ceiling；若天花板 ≥12% 則高於 Base EPS 五年年化 10.7%，reasoning.growth 現寫的「缺口 0.5pp 歸因 sourced PCG」需改為反向表述
- **指向欄位**：moat.roic_durability.roiic、moat.roic_durability.endo_ceiling

**受影響子樹原文**：

`moat.roic_durability.roiic`：
```json
"約 17%（代理：FY2026 增量營收約 $600M × 政府／商用混合增量 EBITDA 利潤率 15% ≈ $90M 增量 EBITDA，對 FY2026 增量投入約 $450M〔資本支出 $247M − 折舊估 $100M ＋ PCG $200M〕；折舊與投入資本證據包未涵蓋，標代理估算）"
```

`moat.roic_durability.endo_ceiling`：
```json
10.2
```

**相關 evidence finding 原文**：

（未定位到對應 evidence finding）


## 修補紀律

1. **只准改被點名的欄位**——findings 的「指向欄位」是你的動刀範圍。沒被點名的欄位一字不動，包含 `decision_out`（由 `dd_decision.py` 回填，你不要手改）與未涉及的 `reasoning` 段。
2. **裁決方向不由你主動翻**——修正欄位後若 `judge check` 重算出的 `decision_out.verdict` 自己翻面，那是機械層的結果，照實接受並在回報點名；但你不得為了配合閘的語氣直接改寫裁決字串。
3. **可以不採納**——閘的意見不是命令。判斷你認為原判正確時，該條不改欄位，改為在頂層 `evidence_dismissed[]` 補一條 `{"ref": "<閘點名的 finding ref 或欄位路徑>", "reason": "<不採納的具體理由>"}`。理由要指得出證據或推導本身的問題（口徑不可比、來源不可回溯、已被更新一季數字取代、閘誤讀了哪個欄位…），不得寫「影響不大」這類無內容句。**每一條 🔴 都必須有處置**：要嘛改欄位，要嘛進 `evidence_dismissed[]`，不得沉默略過。
4. **🟡 選擇性處理**——能一句話補上就補（通常是 `contradictions[]`／`triggers[]` 加一條或補 `formula_note`），代價過大就依第 3 條寫不採納理由。
5. **不得編造數字**——證據包未涵蓋的數字不准補；該欄位標「證據包未涵蓋」並在回報請 orchestrator 判斷是否回 Stage 0 補軸。
6. 禁 WebSearch／WebFetch。

## 寫（一次 Write 整檔）

改完後把**完整的 judgment.json**一次 `Write` 回 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20260905/judgment.json`（不要分次 Edit、不要只寫片段），接著跑：

```
python3 scripts/ddreport.py judge check BWXT 20260905
```

這支會依序重跑 `dd_scenario.py`、`dd_decision.py run`、`validate_judgment.py --evidence --fix --report`，一次把結果回給你；你不需要也不得自行分別呼叫這三支腳本。

FAIL → **只准改 FAIL 訊息點名的欄位**，重跑同一條 `judge check`，**≤1 輪**。一輪後仍 FAIL 就照實回報，交給 orchestrator 處置，不得為湊過驗證而改動判斷實質。

**輪次上限 `6` 輪。** 逼近上限時停下並照實回報。

## 回報（≤200 字）

① 逐條列閘的發現與你的處置（改了哪個欄位／或進 `evidence_dismissed[]` 及理由摘要）
② `judge check` 最後一次的 `validate_judgment.py --report` 原文
③ `decision_out.verdict`／`role`／`row_hit`，以及是否與修補前不同（翻面要明講）
